#!/usr/bin/python3
# encoding: utf-8

# --                                                            ; {{{1
#
# File        : jiten/kanji.py
# Maintainer  : Felix C. Stegerman <flx@obfusk.net>
# Date        : 2020-08-01
#
# Copyright   : Copyright (C) 2020  Felix C. Stegerman
# Version     : v0.2.0
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
Entry(char='猫', cat='KANJI', level='常用', strokes=11, freq=1702, jlpt=2, skip='1-3-8', rad=94, comp='⺨⽝⽥⾋犬犯猫田艸艹艾苗', on=('ビョウ',), kun=('ねこ',), nanori=(), meaning=('cat',))

>>> [ x for x in kanjidic if x.char == "日" ][0]
Entry(char='日', cat='KANJI', level='常用1', strokes=4, freq=1, jlpt=4, skip='3-3-1', rad=72, comp='⽇日', on=('ニチ', 'ジツ'), kun=('ひ', '-び', '-か'), nanori=('あ', 'あき', 'いる', 'く', 'くさ', 'こう', 'す', 'たち', 'に', 'にっ', 'につ', 'へ'), meaning=('day', 'sun', 'Japan', 'counter for days'))

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
>>> all( M.iskanji(c) for c in KAN2RAD.keys() )
True
>>> set( ord(c) - 0x2f00 for c in RAD2KAN.keys() ) == set(range(214))
True
>>> all( ord(x[0]) - 0x2f00 == i for i, x in enumerate(RADICALS) )
True

"""                                                             # }}}1

import gzip, re, sys
import xml.etree.ElementTree as ET

from collections import namedtuple

import click

from . import misc as M
from .sql import sqlite_do, load_pcre_extension

SQLITE_FILE   = M.resource_path("res/kanji.sqlite3")
KANJIDIC_FILE = M.resource_path("res/jmdict/kanjidic2.xml.gz")
KANJIVG_FILE  = M.resource_path("res/radicals/kanjivg.xml.gz")
KRADFILE      = M.resource_path("res/radicals/kradfile.utf8")
KRADFILE2     = M.resource_path("res/radicals/kradfile2.utf8")

NOFREQ = 9999
LEVELS = "常用1 常用2 常用3 常用4 常用5 常用6 常用 人名 人名(常用)".split()

Entry = namedtuple("Entry", """char cat level strokes freq jlpt skip
                               rad comp on kun nanori meaning""".split())

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
        on      = tuple( r.text.strip() for r in
                         e.findall(".//reading[@r_type='ja_on']") )
        kun     = tuple( r.text.strip() for r in
                         e.findall(".//reading[@r_type='ja_kun']") )
        nanori  = tuple( n.text.strip() for n in e.findall(".//nanori") )
        meaning = tuple( m.text.strip() for m in e.findall(".//meaning")
                                if "m_lang" not in m.attrib )
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
                    all( M.iskatakana(c) for c in x ) for x in kun )
        assert all( "\n" not in x for x in on )
        assert all( "\n" not in x for x in kun )
        assert all( "\n" not in x for x in nanori )
        assert all( "\n" not in x for x in meaning )
        data.append(Entry(char, category(char), lvl, strokes, freq, jlpt,
                          skip, rad, comp, on, kun, nanori, meaning))
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
      code  = int(e.attrib["id"].replace("kvg:kanji_", ""), 16)
      char  = chr(code)
      elems = set( r.attrib[elem] for r in e.findall(".//g")
                                  if elem in r.attrib )
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
        elems = set( "丨" if c == "｜" else c for c in rest.split() )
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

def kanjidic2sqldb(data, file = SQLITE_FILE):                   # {{{1
  with sqlite_do(file) as c:
    c.executescript(KANJIDIC_CREATE_SQL)
    with click.progressbar(data, width = 0, label = "writing kanjidic") as bar:
      for e in bar:
        c.execute("INSERT INTO entry VALUES ({})"
                  .format(",".join(["?"]*14)),
                  (ord(e.char), e.char, e.cat, e.level, e.strokes,
                   e.freq, e.jlpt, e.skip, e.rad, e.comp,
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

# TODO: +r(ad(ical))
def search(q, max_results = None, file = SQLITE_FILE):          # {{{1
  ent   = lambda r: Entry(*(list(r[1:10]) + [ tuple(x.splitlines())
                                              for x in r[10:] ]))
  ideo  = tuple(M.uniq(filter(M.isideo, q)))
  order = """ORDER BY IFNULL(freq, {}) ASC, level2int(level) ASC,
             code ASC""".format(NOFREQ)                       # safe!
  limit = "LIMIT " + str(int(max_results)) if max_results else ""
  with sqlite_do(file) as c:
    c.connection.create_function("level2int", 1, level2int)
    if ideo:
      for char in ideo:
        for r in c.execute("SELECT * FROM entry WHERE code = ?", (ord(char),)):
          yield ent(r) # #=1
    else:
      m = re.fullmatch(r"\+s(?:kip)?\s*([\d-]+)", q, re.I)
      if m:
        for r in c.execute("""
            SELECT * FROM entry WHERE skip = ? {} {}
            """.format(order, limit), (m[1],)):               # safe!
          yield ent(r)
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
          yield ent(r)
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

                                                                # {{{1
RADICALS = tuple("""⼀一 ⼁丨 ⼂丶 ⼃丿 ⼄乙 ⼅亅 ⼆二 ⼇亠 ⼈人 ⼉儿
⼊入 ⼋八 ⼌冂 ⼍冖 ⼎冫 ⼏几 ⼐凵 ⼑刀 ⼒力 ⼓勹 ⼔匕 ⼕匚 ⼖匸 ⼗十
⼘卜 ⼙卩 ⼚厂 ⼛厶 ⼜又 ⼝口 ⼞囗 ⼟土 ⼠士 ⼡夂 ⼢夊 ⼣夕 ⼤大 ⼥女
⼦子 ⼧宀 ⼨寸 ⼩小 ⼪尢 ⼫尸 ⼬屮 ⼭山 ⼮巛 ⼯工 ⼰己 ⼱巾 ⼲干 ⼳幺
⼴广 ⼵廴 ⼶廾 ⼷弋 ⼸弓 ⼹彐 ⼺彡 ⼻彳 ⼼心 ⼽戈 ⼾戶 ⼿手 ⽀支 ⽁攴
⽂文 ⽃斗 ⽄斤 ⽅方 ⽆无 ⽇日 ⽈曰 ⽉月 ⽊木 ⽋欠 ⽌止 ⽍歹 ⽎殳 ⽏毋
⽐比 ⽑毛 ⽒氏 ⽓气 ⽔水 ⽕火 ⽖爪 ⽗父 ⽘爻 ⽙爿 ⽚片 ⽛牙 ⽜牛 ⽝犬
⽞玄 ⽟玉 ⽠瓜 ⽡瓦 ⽢甘 ⽣生 ⽤用 ⽥田 ⽦疋 ⽧疒 ⽨癶 ⽩白 ⽪皮 ⽫皿
⽬目 ⽭矛 ⽮矢 ⽯石 ⽰示 ⽱禸 ⽲禾 ⽳穴 ⽴立 ⽵竹 ⽶米 ⽷糸 ⽸缶 ⽹网
⽺羊 ⽻羽 ⽼老 ⽽而 ⽾耒 ⽿耳 ⾀聿 ⾁肉 ⾂臣 ⾃自 ⾄至 ⾅臼 ⾆舌 ⾇舛
⾈舟 ⾉艮 ⾊色 ⾋艸 ⾌虍 ⾍虫 ⾎血 ⾏行 ⾐衣 ⾑襾 ⾒見 ⾓角 ⾔言 ⾕谷
⾖豆 ⾗豕 ⾘豸 ⾙貝 ⾚赤 ⾛走 ⾜足 ⾝身 ⾞車 ⾟辛 ⾠辰 ⾡辵 ⾢邑 ⾣酉
⾤釆 ⾥里 ⾦金 ⾧長 ⾨門 ⾩阜 ⾪隶 ⾫隹 ⾬雨 ⾭靑 ⾮非 ⾯面 ⾰革 ⾱韋
⾲韭 ⾳音 ⾴頁 ⾵風 ⾶飛 ⾷食 ⾸首 ⾹香 ⾺馬 ⾻骨 ⾼高 ⾽髟 ⾾鬥 ⾿鬯
⿀鬲 ⿁鬼 ⿂魚 ⿃鳥 ⿄鹵 ⿅鹿 ⿆麥 ⿇麻 ⿈黃 ⿉黍 ⿊黑 ⿋黹 ⿌黽 ⿍鼎
⿎鼓 ⿏鼠 ⿐鼻 ⿑齊 ⿒齒 ⿓龍 ⿔龜 ⿕龠""".split())

RAD2KAN = { x[0]: x[1] for x in RADICALS }
KAN2RAD = { x[1]: x[0] for x in RADICALS }

RADSTROKEGRPS = (
  1, 7, 30, 61, 95, 118, 147, 167, 176, 187, 195, 201, 205, 209, 211,
  212, 214
)
RADSTROKES = tuple(
    k+1
  for k, (m, n) in enumerate(zip(RADSTROKEGRPS,
                                 RADSTROKEGRPS[1:]+(len(RADICALS)+1,)))
  for i in range(m-1, n-1)
)
RADGROUPS = tuple(
    tuple( x[1] for x in RADICALS[m-1:n-1] )
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
