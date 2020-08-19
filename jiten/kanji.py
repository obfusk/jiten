#!/usr/bin/python3
# encoding: utf-8

# --                                                            ; {{{1
#
# File        : jiten/kanji.py
# Maintainer  : Felix C. Stegerman <flx@obfusk.net>
# Date        : 2020-08-19
#
# Copyright   : Copyright (C) 2020  Felix C. Stegerman
# Version     : v0.3.0
# License     : AGPLv3+
#
# --                                                            ; }}}1

                                                                # {{{1
r"""

KanjiDic.

>>> kanjivg = parse_kanjivg()
>>> len(kanjivg)
6420

>>> kanjidic = parse_kanjidic(kanjivg)
>>> len(kanjidic)
13108
>>> len(set( x.char for x in kanjidic ))
13108

>>> [ x for x in kanjidic if x.char == "猫" ][0]
Entry(char='猫', cat='KANJI', level='常用', strokes=11, freq=1702, jlpt=2, skip='1-3-8', rad=94, comp='⺨⽝⽥⾋犬犯猫田艸艹艾苗', var='貓', on=('ビョウ',), kun=('ねこ',), nanori=(), meaning=('cat',))

>>> [ x for x in kanjidic if x.char == "日" ][0]
Entry(char='日', cat='KANJI', level='常用1', strokes=4, freq=1, jlpt=4, skip='3-3-1', rad=72, comp='⽇日', var='', on=('ニチ', 'ジツ'), kun=('ひ', '-び', '-か'), nanori=('あ', 'あき', 'いる', 'く', 'くさ', 'こう', 'す', 'たち', 'に', 'にっ', 'につ', 'へ'), meaning=('day', 'sun', 'Japan', 'counter for days'))

>>> len([ x for x in kanjidic if x.level == "常用1" ])
80
>>> len([ x for x in kanjidic if x.level == "常用2" ])
160
>>> len([ x for x in kanjidic if x.level == "常用3" ])
200
>>> len([ x for x in kanjidic if x.level == "常用4" ])
197
>>> len([ x for x in kanjidic if x.level == "常用5" ])
197
>>> len([ x for x in kanjidic if x.level == "常用6" ])
192
>>> len([ x for x in kanjidic if x.level == "常用" ])
1110
>>> len([ x for x in kanjidic if x.level == "人名" ])
650
>>> len([ x for x in kanjidic if x.level == "人名(常用)" ])
212
>>> len([ x for x in kanjidic if x.level is None ])
10110

>>> len([ x for x in kanjidic if x.freq is not None ])
2501
>>> len([ x for x in kanjidic if x.jlpt is not None ])
2230
>>> len([ x for x in kanjidic if x.new_jlpt() is not None ])
2211
>>> len([ x for x in kanjidic if x.skip is None ])
952
>>> len([ x for x in kanjidic if x.skip is None and x.cat == "KANJI" ])
403

>>> len([ x for x in kanjidic if x.strokes > 25 ])
94

>>> len([ x for x in kanjidic if x.cat == "KANJI" ])
12559
>>> len([ x for x in kanjidic if x.cat == "CJK COMPATIBILITY IDEOGRAPH" ])
82
>>> len([ x for x in kanjidic if x.cat == "CJK UNIFIED IDEOGRAPH" ])
467

>>> len([ x for x in kanjidic if len(x.nanori) ])
1353
>>> len([ x for x in kanjidic if not len(x.on) ])
952
>>> len([ x for x in kanjidic if not len(x.kun) ])
3288
>>> len([ x for x in kanjidic if not len(x.meaning) ])
2751

>>> len(RADICALS)
214
>>> M.iskanji(KAN2RAD.keys())
True
>>> M.isradical(RAD2KAN.keys())
True
>>> set( ord(c) - 0x2f00 for c in RAD2KAN.keys() ) == set(range(214))
True
>>> all( ord(x[0]) - 0x2f00 == i for i, x in enumerate(RADICALS) )
True

"""                                                             # }}}1

import gzip, itertools, re, sys, unicodedata as UD
import xml.etree.ElementTree as ET

from collections import namedtuple

import click

from . import jmdict as J
from . import misc   as M
from .sql import sqlite_do, load_pcre_extension

SQLITE_FILE     = M.resource_path("res/kanji.sqlite3")
KANJIDIC_FILE   = M.resource_path("res/jmdict/kanjidic2.xml.gz")
KANJIVG_FILE    = M.resource_path("res/radicals/kanjivg.xml.gz")
KRADFILE        = M.resource_path("res/radicals/kradfile.utf8")
KRADFILE2       = M.resource_path("res/radicals/kradfile2.utf8")
JLPT_FILE_BASE  = M.resource_path("res/jlpt/N")

MAXE   = 25                                                     # TODO
NOFREQ = 9999
LEVELS = "常用1 常用2 常用3 常用4 常用5 常用6 常用 人名 人名(常用)".split()

Entry = namedtuple("Entry", """
  char cat level strokes freq jlpt skip rad comp var
  on kun nanori meaning
""".split())

def components(e):
  r = e.radical()
  return "".join( c for c in e.comp if c not in RAD2KAN and c != r
                                    and c != e.char )

Entry.components  = components
Entry.canonical   = lambda e: canonical(e.char)
Entry.radical     = lambda e: RADICALS[e.rad-1][1]
Entry.name        = lambda e: UD.name(e.char)
Entry.jmdict      = lambda e: J.search(e.char, max_results = MAXE)
Entry.new_jlpt    = lambda e: JLPT.get(e.char)

def canonical(c): return UD.normalize("NFC", c)

def level(l):
  if 1 <= l <= 6: return "常用" + str(l)
  if l == 8     : return "常用"
  if l == 9     : return "人名"
  if l == 10    : return "人名(常用)"
  raise ValueError("unexpected level: " + l)

def level2int(l):
  try:
    return LEVELS.index(l)
  except ValueError:
    return 99

def category(c):
  if M.iskanji(c) : return "KANJI"
  if M.iscompat(c): return "CJK COMPATIBILITY IDEOGRAPH"
  if M.isuniext(c): return "CJK UNIFIED IDEOGRAPH"
  raise ValueError("unexpected category for: " + c)

def variants(char, vs):
  for v in vs:
    t = v.get("var_type")
    c = decode_variant(t, v.text)
    if t == "jis213": assert char in "泰"                       # TODO
    if c: yield c

def decode_variant(t, x):
  decode  = lambda b, x = "": b.decode("iso-2022-jp" + x)
  dekuten = lambda: bytes( int(i) + 32 for i in x.split("-") )
  if t == "jis208": return decode(b"\x1b$B"  + dekuten())
  if t == "jis212": return decode(b"\x1b$(D" + dekuten(), "-2")
  if t == "jis213": return decode(b"\x1b$(P" + dekuten(), "-2004")
  if t == "ucs"   : return chr(int(x, 16))
  return None

def maybe(x, f, d = None):
  return d if x is None else f(x)

# TODO
# * rmgroup?!
def parse_kanjidic(kanjivg = None, file = KANJIDIC_FILE):       # {{{1
  if kanjivg is None: kanjivg = parse_kanjivg()
  data = []
  with gzip.open(file) as f:
    with click.progressbar(ET.parse(f).getroot(), width = 0,
                           label = "parsing kanjidic") as bar:
      for e in bar:
        if e.tag != "character": continue
        char    = e.find("literal").text.strip()
        lvl     = maybe(e.find(".//grade"), lambda e: level(int(e.text)))
        strokes = int(e.find(".//stroke_count").text)
        freq    = maybe(e.find(".//freq"), lambda e: int(e.text))
        jlpt    = maybe(e.find(".//jlpt"), lambda e: int(e.text)) # *OLD* JLPT (1-4)
        skip    = maybe(e.find(".//q_code[@qc_type='skip']"),
                        lambda e: e.text.strip())
        rad     = int(e.find(".//rad_value[@rad_type='classical']").text)
        comp    = kanjivg.get(char, set())
        var_    = set(variants(char, e.findall(".//variant")))
        var     = "".join(sorted(var_ - set([char, canonical(char)])))
        on      = tuple( r.text.strip() for r in
                         e.findall(".//reading[@r_type='ja_on']") )
        kun     = tuple( r.text.strip() for r in
                         e.findall(".//reading[@r_type='ja_kun']") )
        nanori  = tuple( n.text.strip() for n in e.findall(".//nanori") )
        meaning = tuple( m.text.strip() for m in e.findall(".//meaning")
                                        if m.get("m_lang") is None )
        if comp and not set(RADICALS[rad-1]).issubset(comp):
          for x, y in "肉⽉ 白⽇ 曰⽇ 臼𦥑 匸⼕ 夊⼡ 夂久 人⼊ 入⼈".split():
            if x == RADICALS[rad-1][1] and y in comp: break
          else:
            assert char in "為亀巨尭壮争単壷丗舅关"
        comp = "".join(sorted(comp | set(RADICALS[rad-1] + char)))
        assert len(char) == 1
        assert 1 <= rad <= 214
        assert all( M.iskatakana(c) or c in ".-" for x in on for c in x )
        assert all( all( M.ishiragana(c) or c in ".-ー" for c in x ) or
                         M.iskatakana(x) for x in kun )
        assert all( "\n" not in x for x in on )
        assert all( "\n" not in x for x in kun )
        assert all( "\n" not in x for x in nanori )
        assert all( "\n" not in x for x in meaning )
        data.append(Entry(char, category(char), lvl, strokes, freq, jlpt,
                          skip, rad, comp, var, on, kun, nanori, meaning))
      return data
                                                                # }}}1

# NB: kanjivg & kradfile & kradfile2
def parse_kanjivg(file = KANJIVG_FILE, kradfile = KRADFILE,     # {{{1
                  kradfile2 = KRADFILE):
  elem = "{http://kanjivg.tagaini.net}element"
  data = {}
  with gzip.open(file) as f:
    for e in ET.parse(f).getroot():
      if e.tag != "kanji": continue
      code  = int(e.get("id").replace("kvg:kanji_", ""), 16)
      char  = chr(code)
      elems = set( r.get(elem) for r in e.findall(".//g")
                               if elem in r.keys() )
      if M.iskana(char) or M.ispunc(char): continue
      if not M.iscjk(char) and not M.isradical(char): continue
      elems.add(char)
      assert char not in data
      assert all( M.isideo(c) or M.iskana(c) or M.isradical(c)
                  for c in elems )
      data[char] = elems
  with open(kradfile) as f1:
    with open(kradfile2) as f2:
      for line in ( line for f in [f1, f2] for line in f ):
        if re.match(r"^$|^#", line): continue
        char, rest = line.split(" : ")
        elems = set( rest.replace("｜", "丨").split() )
        assert M.iskanji(char)
        assert char in data[char]
        assert all( M.iskanji(c) or M.iskana(c) for c in elems )
        data[char].update(elems)
  for elems in data.values():
    elems.update(set( VAR2RAD[x] for x in elems if x in VAR2RAD ))
    elems.update(set( KAN2RAD[x] for x in elems if x in KAN2RAD ))
    elems.update(set( RAD2KAN[x] for x in elems if x in RAD2KAN ))
  return data
                                                                # }}}1

def load_jlpt(base = JLPT_FILE_BASE):
  data = {}
  for level in "12345":
    with open(base + level) as f:
      for c in f.readline().strip():
        assert M.iskanji(c)
        assert c not in data
        data[c] = int(level)
  return data

JLPT = load_jlpt()

def kanjidic2sqldb(data, file = SQLITE_FILE):                   # {{{1
  with sqlite_do(file) as c:
    c.executescript(KANJIDIC_CREATE_SQL)
    with click.progressbar(data, width = 0, label = "writing kanjidic") as bar:
      for e in bar:
        c.execute("INSERT INTO entry VALUES ({})"
                  .format(",".join("?"*(len(Entry._fields)+1))),
                  (ord(e.char), e.char, e.cat, e.level, e.strokes,
                   e.freq, e.jlpt, e.skip, e.rad, e.comp, e.var,
                   "\n".join(e.on), "\n".join(e.kun),
                   "\n".join(e.nanori), "\n".join(e.meaning)))
        for k in e.comp:
          c.execute("INSERT INTO comp VALUES(?,?)", (ord(e.char), ord(k)))
                                                                # }}}1

                                                                # {{{1
KANJIDIC_CREATE_SQL = """
  DROP TABLE IF EXISTS entry;
  DROP TABLE IF EXISTS comp;

  CREATE TABLE entry(
    code INTEGER PRIMARY KEY ASC,
    char TEXT,
    cat TEXT,
    level TEXT,
    strokes INTEGER,
    freq INTEGER,
    jlpt INTEGER,
    skip TEXT,
    rad INTEGER,
    comp TEXT,
    var TEXT,
    on_ TEXT,
    kun TEXT,
    nanori TEXT,
    meaning TEXT
  );
  CREATE TABLE comp(
    entry INTEGER,
    code INTEGER,
    FOREIGN KEY(entry) REFERENCES entry(code)
  );

  CREATE INDEX idx_comp ON comp (code);
"""                                                             # }}}1

def setup(file = SQLITE_FILE):
  kanjivg   = parse_kanjivg()
  kanjidic  = parse_kanjidic(kanjivg)
  kanjidic2sqldb(kanjidic, file)

def row2entry(r):
  i = r.keys().index("on_")
  return Entry(*(list(r[1:i]) + [ tuple(x.splitlines()) for x in r[i:] ]))

def search(q, max_results = None, file = SQLITE_FILE):          # {{{1
  ideo  = tuple(M.uniq(filter(M.isideo, q)))
  order = """ORDER BY IFNULL(freq, {}) ASC, level2int(level) ASC,
             code ASC""".format(NOFREQ)                       # safe!
  limit = "LIMIT " + str(int(max_results)) if max_results else ""
  with sqlite_do(file) as c:
    c.connection.create_function("level2int", 1, level2int)
    ms = re.fullmatch(r"\+s(?:kip)?\s*([\d-]+)", q, re.I)
    mr = re.fullmatch(r"\+r(?:ad(?:icals?)?)?\s*(\S+)", q, re.I)
    if q.lower() == "+random":
      yield random(file)
    elif ms:
      for r in c.execute("""
          SELECT * FROM entry WHERE skip = ? {} {}
          """.format(order, limit), (ms.group(1),)):          # safe!
        yield row2entry(r)
    elif mr:
      rads = [ VAR2RAD.get(c, c) for c in mr.group(1)
               if M.isideo(c) or M.iskana(c) or M.isradical(c) ]
      if not rads: return                                       # TODO
      radp = [ str(ord(c)) for c in rads ]
      subq = "SELECT entry FROM comp WHERE code = ?"
      isct = " INTERSECT ".join( subq for _ in radp )
      for r in c.execute("""
          SELECT entry.* FROM ({})
          INNER JOIN entry ON code = entry
          {} {}
          """.format(isct, order, limit), radp):              # safe!
        yield row2entry(r)
    elif ideo:
      for char in ideo:
        for r in c.execute("SELECT * FROM entry WHERE code = ?", (ord(char),)):
          yield row2entry(r) # #=1
    else:
      load_pcre_extension(c.connection)
      for r in c.execute("""
          SELECT * FROM entry WHERE
                            on_                        REGEXP :re OR
                            kun                        REGEXP :re OR
                            nanori                     REGEXP :re OR
            replace(replace(on_   , '.', ''), '-', '') REGEXP :re OR
            replace(replace(kun   , '.', ''), '-', '') REGEXP :re OR
            replace(replace(nanori, '.', ''), '-', '') REGEXP :re OR
                            meaning                    REGEXP :re
            {} {}
          """.format(order, limit), dict(re = M.q2rx(q))):    # safe!
        yield row2entry(r)
                                                                # }}}1

def by_freq(file = SQLITE_FILE):
  with sqlite_do(file) as c:
    for r in c.execute("""
        SELECT char, freq FROM entry
          WHERE freq IS NOT NULL ORDER BY freq ASC
        """):
      yield r["char"], r["freq"]

def by_level(level, file = SQLITE_FILE):
  with sqlite_do(file) as c:
    for r in c.execute("""
        SELECT char FROM entry WHERE level = ? ORDER BY code ASC
        """, (level,)):
      yield r["char"]

def by_jlpt():
  data = { int(l): [] for l in "12345" }
  for char, level in JLPT.items():
    data[level].append(char)
  for level in "54321":
    yield int(level), "".join(sorted(data[int(level)]))

def random(file = SQLITE_FILE):
  with sqlite_do(file) as c:
    q = "SELECT * FROM entry ORDER BY RANDOM() LIMIT 1"
    return row2entry(c.execute(q).fetchone())

RADICALS      = tuple( chr(i) + UD.normalize("NFKC", chr(i))    # {{{1
                       for i in range(0x2f00, 0x2fd6) )
RAD2KAN       = { x[0]: x[1] for x in RADICALS }
KAN2RAD       = { x[1]: x[0] for x in RADICALS }

RADSTROKEGRPS = (1, 7, 30, 61, 95, 118, 147, 167, 176, 187, 195, 201,
                 205, 209, 211, 212, 214)

RADGROUPS = tuple(
  "".join( x[1] for x in RADICALS[m-1:n-1] )
  for m, n in zip(RADSTROKEGRPS, RADSTROKEGRPS[1:]+(len(RADICALS)+1,))
)

RADVARS  = tuple("""𠆢人 𦉰网 ⺃乙 ⺅人 ⺇几 ⺉刀 ⺌小 ⺍小 ⺔彐 ⺕彐
⺖心 ⺗心 ⺘手 ⺙攴 ⺛无 ⺝月 ⺡水 ⺣火 ⺤爪 ⺨犬 ⺪疋 ⺫网 ⺭示 ⺮竹
⺷羊 ⺹老 ⺾艸 ⻂衣 ⻃襾 ⻊足 ⻌辵 ⻏邑 ⻖阜 ⻗雨 ⻘靑 ⻟食 ⻨麥 ⻩黃
⻫齊 ⻭齒 ⻲龜 㓁网 川巛 氺水 爫爪 黒黑 羽羽""".split())

RADVARS2 = tuple("""⺊卜 ⺮竹 ⺳网 ⺼肉 ⻊足 ⻗雨 〇囗 丬爿 乀丿 乁丿
乚乙 乛乙 亻人 刁刀 刂刀 夨大 孑子 孒子 尣尢 巜巛 川巛 已己 巳己 彑彐
忄心 戸戶 扌手 才手 攵攴 斉齊 旡无 朩木 歺歹 毌毋 氵水 灬火 爫爪 牜牛
犭犬 玊玉 王玉 甩用 由田 甲田 申田 甴田 礻示 罒网 罓网 耂老 考老 艹艸
草艸 衤衣 西襾 覀襾 訁言 赱走 辶辵 釒金 镸長 阝邑 阝阜 青靑 靣面 飠食
髙高 麦麥 黄黃 黒黑 鼔鼓 鼡鼠""".split())

RADVARS3 = tuple("""𩙿食 歯齒""".split())

VAR2RAD = { x[0]: x[1] for y in [RADVARS, RADVARS2, RADVARS3] for x in y }

STROKEVARS = {                                                  # TODO
  2: "亻刂", 3: "⺌⻌⻏⻖忄扌氵犭艹", 4: "攵灬王礻耂辶",
  5: "氺玊罒衤", 6: "西", 7: "麦", 8: "斉鼡", 11: "黄黒", 12: "歯"
}

ALTRADS  = tuple("""ノ01 ハ02 マ02 ユ02 ヨ03 一01 世05 丨01 个02 丶01
乃02 久03 乙01 九02 乞02 也03 亀11 亅01 二02 五04 井04 亠02 亡03 人02
儿02 元04 免08 入02 冂02 冊05 冖02 冫02 几02 凵02 刀02 刈02 初05 力02
勹02 勿04 匕02 化02 匚02 十02 卜02 卩02 厂02 厶02 又02 及03 口03 品09
囗03 土03 士03 夂03 夕03 大03 奄08 女03 子03 宀03 寸03 小03 尚03 尢03
尤04 尸03 屮03 屯04 山03 岡08 巛03 川03 工03 巨05 已03 巴04 巾03 干03
并02 幺03 广03 廴03 廾03 弋03 弓03 彑03 彡03 彳03 心04 忙03 戈04 戸04
手04 扎03 支04 攵04 文04 斉08 斗04 斤04 方04 无04 日04 曰04 月04 木04
杰04 欠04 止04 歯12 歹04 殳04 毋04 母05 比04 毛04 氏04 气04 水04 汁03
滴11 火04 無12 爪04 父04 爻04 爿04 片04 牙05 牛04 犬04 犯03 玄05 王04
瓜06 瓦05 甘05 生05 用05 田05 疋05 疔05 癶05 白05 皮05 皿05 目05 矛05
矢05 石05 示05 礼04 禹05 禾05 穴05 立05 竜10 竹06 米06 糸06 缶06 羊06
羽06 老04 而06 耒06 耳06 聿06 肉06 臣07 自06 至06 臼06 舌06 舛07 舟06
艮06 色06 艾03 虍06 虫06 血06 行06 衣06 西06 見07 角07 言07 谷07 豆07
豕07 豸07 貝07 買05 赤07 走07 足07 身07 車07 辛07 辰07 込03 邦03 酉07
釆07 里07 金08 長08 門08 阡03 隶08 隹08 雨08 青08 非08 面09 革09 韋10
韭09 音09 頁09 風09 飛09 食09 首09 香09 馬10 骨10 高10 髟10 鬥10 鬯10
鬲10 鬼10 魚11 鳥11 鹵11 鹿11 麦07 麻11 黄11 黍12 黒11 黹12 黽13 鼎13
鼓13 鼠13 鼻14 齊14 龠17""".split())

ALTSTROKES  = { x[0]: int(x[1:]) for x in ALTRADS }
STROKEALTS  = { k: "".join(sorted( x[0] for x in g ))
                for k, g in itertools.groupby(
                  sorted(ALTSTROKES.items(), key = lambda x: x[1]),
                  lambda x: x[1]) }

RADTABLE = tuple(
  tuple(sorted(itertools.chain(
    ( (x, "rad") for x in g ),
    ( (x, "alt") for x in STROKEALTS.get(i, ()) if not x in g ),
    ( (x, "var") for x in STROKEVARS.get(i, ()) if not x in STROKEALTS[i] )
  ))) for i, g in ( (i+1, set(g)) for i, g in enumerate(RADGROUPS) )
)

RADVARSPRIV = tuple("""穴 麻 舟 歹 言 巾 白 八 日 火 矛 骨
方 石 至 糸 貝 金 片 牙 木 子 米 口 車 豆 目 身 耳
虫 釆 丿 女 玉 士 里 走 寸 田 工 谷 立 戶 酉 土 角
馬 魚 牛 矢 山 山 弓 韋 牙 舛 肉 目""".split())   # TODO
                                                                # }}}1

if __name__ == "__main__":
  if "--doctest" in sys.argv:
    verbose = "--verbose" in sys.argv
    import doctest
    if doctest.testmod(verbose = verbose)[0]: sys.exit(1)

# vim: set tw=70 sw=2 sts=2 et fdm=marker :
