#!/usr/bin/python3
# encoding: utf-8

# --                                                            ; {{{1
#
# File        : jiten/jmdict.py
# Maintainer  : Felix C. Stegerman <flx@obfusk.net>
# Date        : 2021-02-11
#
# Copyright   : Copyright (C) 2021  Felix C. Stegerman
# Version     : v0.4.0
# License     : AGPLv3+
#
# --                                                            ; }}}1

                                                                # {{{1
r"""

JMDict.

>>> DBVERSION
13

>>> jmdict = parse_jmdict()
>>> len(jmdict)
190722

>>> print(jmdict[-1].sense[0].gloss[0])
Japanese-Multilingual Dictionary Project - Creation Date: 2021-01-19

>>> len([ x for x in jmdict if x.isprio() ])
22443
>>> len([ x for x in jmdict if x.isprio() and list(x.pitch()) ])
21269

>>> len([ x for x in jmdict if x.jlpt == 1 ])
3035
>>> len([ x for x in jmdict if x.jlpt == 2 ])
1725
>>> len([ x for x in jmdict if x.jlpt == 3 ])
1657
>>> len([ x for x in jmdict if x.jlpt == 4 ])
633
>>> len([ x for x in jmdict if x.jlpt == 5 ])
679

>>> len([ x for x in jmdict if x.jlpt == 1 and x.isprio() ])
2628
>>> len([ x for x in jmdict if x.jlpt == 2 and x.isprio() ])
1647
>>> len([ x for x in jmdict if x.jlpt == 3 and x.isprio() ])
1615
>>> len([ x for x in jmdict if x.jlpt == 4 and x.isprio() ])
615
>>> len([ x for x in jmdict if x.jlpt == 5 and x.isprio() ])
657

>>> baka = [ x for x in jmdict if any( r.elem == "ばか" for r in x.reading ) ][0]
>>> baka.seq
1601260
>>> baka.definition()
('ばか', 'バカ', '馬鹿', '莫迦', '破家', '馬稼')
>>> tuple(baka.pitch())
('ばꜜか',)
>>> baka.usually_kana()
True
>>> baka.jlpt
3
>>> baka.isprio()
True
>>> baka.prio_level()
11
>>> baka.isnoun()
True
>>> baka.isverb()
False
>>> print("\n".join(M.flatten(baka.meanings())))
idiot
moron
fool
trivial matter
folly
absurdity
stupid
foolish
dull
absurd
ridiculous
fervent enthusiast
nut
person singularly obsessed with something
Mactra chinensis (species of trough shell)
>>> print("\n".join(list(M.flatten(baka.meanings("ger")))[:10]))
Dummkopf
Idiot
Esel
Hohlkopf
Tor
Strohkopf
dumm
idiotisch
Dummheit
Unsinn
>>> print("\n".join(M.uniq(M.flatten( s.pos for s in baka.sense ))))
noun (common) (futsuumeishi)
adjectival nouns or quasi-adjectives (keiyodoshi)
>>> print("\n".join(M.uniq(M.flatten( s.info for s in baka.sense ))))
word usually written using kana alone
usu. in compounds
abbreviation
>>> print("\n".join(baka.xinfo()))
ateji (phonetic) reading
>>> print("\n".join(baka.xrefs()))
馬鹿貝

>>> iku = [ x for x in jmdict if any( r.elem == "行く" for r in x.kanji) ][0]
>>> iku.seq
1578850
>>> iku.definition()
('いく', 'ゆく', '行く', '逝く', '往く')
>>> tuple(iku.pitch())
('いꜛく', 'ゆꜛく')
>>> iku.usually_kana()
True
>>> iku.jlpt
5
>>> iku.isprio()
True
>>> iku.prio_level()
10
>>> iku.isnoun()
False
>>> iku.isverb()
True
>>> any( s.isichidan() for s in iku.sense )
False
>>> any( s.isgodan() for s in iku.sense )
True
>>> any( s.istrans() for s in iku.sense )
False
>>> any( s.isintrans() for s in iku.sense )
True
>>> print("\n".join(M.flatten(iku.meanings())))
to go
to move (in a direction or towards a specific location)
to head (towards)
to be transported (towards)
to reach
to proceed
to take place
to pass through
to come and go
to walk
to die
to pass away
to do (in a specific way)
to stream
to flow
to continue
to have an orgasm
to come
to cum
to trip
to get high
to have a drug-induced hallucination
>>> print("\n".join(list(M.flatten(iku.meanings("dut")))[:10]))
gaan
lopen
wandelen
zich begeven naar
aangaan op
naar wens lopen
lekker lopen
goed werken
succesvol zijn
sterven
>>> print("\n".join(M.uniq(M.flatten( s.pos for s in iku.sense ))))
Godan verb - Iku/Yuku special class
intransitive verb
auxiliary verb
>>> print("\n".join(M.uniq(M.flatten( s.info for s in iku.sense ))))
い sometimes omitted in auxiliary use
word usually written using kana alone
slang
>>> print("\n".join(iku.xinfo()))
word containing out-dated kanji
>>> print("\n".join(iku.xrefs()))
来る
くる
旨く行く


>>> from .kana import hiragana2katakana as h2k, katakana2hiragana as k2h
>>> from .kana import romaji2hiragana   as r2h, romaji2katakana   as r2k
>>> from .kana import kana2romaji       as k2r
>>> rs   = [ r.elem for e in jmdict for r in e.reading ]
>>> hira = [ r for r in rs if M.ishiragana(r) ]
>>> kata = [ r for r in rs if M.iskatakana(r) ]
>>> mixd = [ r for r in rs if not (M.ishiragana(r) or M.iskatakana(r)) ]
>>> len(rs)
228225
>>> len([ k2r(r) for r in rs ])
228225
>>> len([ k2r(p) for e in jmdict for p in e.pitch() ])
110153
>>> len(hira)
152312
>>> len(kata)
60127
>>> len(mixd)
15786
>>> len([ r for r in hira if r2h(k2r(r)) != r ])
0
>>> len([ r for r in kata if r2k(k2r(r, True)) != r ])
0
>>> len([ r for r in mixd if r2k(k2r(r, True)) != h2k(r) ])
0

"""                                                             # }}}1

import gzip, os, re, sys
import xml.etree.ElementTree as ET

from collections import namedtuple

import click

from . import freq  as F
from . import misc  as M
from . import pitch as P
from .kana import katakana2hiragana
from .sql import sqlite_do, load_pcre_extension

DBVERSION       = 13 # NB: update this when data/schema changes
SQLITE_FILE     = M.resource_path("res/jmdict.sqlite3")
JMDICT_FILE     = M.resource_path("res/jmdict/jmdict.xml.gz")
JLPT_FILE_BASE  = M.resource_path("res/jlpt/N")
DATA_FILES      = (SQLITE_FILE, JMDICT_FILE)

MAXSEQ          = 10000000
PRIO            = dict(news1 = 10, news2 = 1, ichi1 = 10, ichi2 = 1,
                       spec1 = 10, spec2 = 5, gai1  = 10, gai2  = 1)
MINPRIO         = 5
USUKANA         = "word usually written using kana alone"
LANGS           = "eng dut ger fre spa swe".split()
JLPTKK, JLPTUK  = JLPTKANA = "[katakana]", "[usukana]"

Entry   = namedtuple("Entry"  , """seq jlpt kanji reading sense""".split())
Kanji   = namedtuple("Kanji"  , """elem chars info prio""".split())
Reading = namedtuple("Reading", """elem restr info prio""".split())
Sense   = namedtuple("Sense"  , """pos lang gloss info xref""".split())

# TODO
# * include all readings if usually_kana? or only frequent ones?
def definition(e):
  r, k  = e.reading, e.kanji
  xs    = r + k if e.usually_kana() else k or r
  return tuple(M.uniq( x.elem for x in xs ))

def words(e): return frozenset( x.elem for x in e.kanji + e.reading )

def meanings(e, *a):
  l = a or [LANGS[0]]
  return tuple( s.gloss for s in e.sense if s.lang in l )

def meaning(e, *a): return frozenset(M.flatten(e.meanings(*a)))

def charsets(e): return frozenset( k.chars for k in e.kanji )

def chars(e): return frozenset(M.flatten( k.chars for k in e.kanji ))

# TODO: load from DB
def _freq(e): return sum( F.freq.get(w, 0) for w in e.definition() )

# TODO: load from DB
def _rank(e): return min( F.rank(w) for w in e.definition() )

def isprio(e):      return _isprio(e.kanji + e.reading)
def _isprio(xs):    return (_prio_level(xs) or 0) >= MINPRIO
def prio_level(e):  return _prio_level(e.kanji + e.reading)
def _prio_level(xs):
  ps = [ x.prio for x in xs if x.prio ]
  return max(ps) if ps else None

def usually_kana(e): return _usukana(e.sense)
def _usukana(sense): return any( USUKANA in s.info for s in sense )

def gloss_pos_info(e, langs):
  gloss, pos, info = { l: [] for l in langs }, [], []
  for l in langs:
    for s in e.sense:
      if s.lang != l: continue
      pos.extend(s.pos); info.extend(s.info)
      gloss[l].append(s.gloss)
  return gloss, tuple(M.uniq(pos + info))

def isnoun(e):
  return any( "noun" in p.split() for s in e.sense for p in s.pos )

def isverb(e):
  return any( "verb" in p.split() for s in e.sense for p in s.pos )

def xinfo(e):
  return M.uniq( z for x in [e.kanji, e.reading]
                   for y in x for z in y.info )

def xrefs(e): return M.uniq( x for s in e.sense for x in s.xref )

def pitch(e, conn = None): return M.uniq(pitch_w_dups(e, conn))

# TODO
def pitch_w_dups(e, conn = None):
  ks = tuple( x.elem for x in e.kanji or e.reading )
  rs = tuple( r.elem for r in e.reading )
  hr = tuple( katakana2hiragana(r) for r in rs )
  for r in rs + tuple( r for r in hr if r not in rs ):
    p = P.get_pitch(r, ks, conn = conn)
    if p: yield p

# TODO
def jlpt_level(kanji, reading, usukana):                        # {{{1
  kana, prio  = not kanji or usukana, _isprio(kanji + reading)
  ls, ka      = set(), set( k.elem for k in kanji )
  for k in ka:
    jlpt = JLPT.get(k)
    if not jlpt: continue
    for r in reading:
      ls.update( n for x, n in jlpt if r.elem == x )
  for r in reading:
    if r.elem in JLPT_COMMON:
      if (ka and not ka & JLPT_CO_KA) or \
         (not ka and r.elem not in JLPT_CO_NK): continue
    jlpt = JLPT.get(r.elem)
    if not jlpt: continue
    for x, n in jlpt:
      assert x in JLPTKANA
      if x == JLPTUK and not kana:
        if ka & JLPT_BLACK: continue
        if not ka & JLPT_WHITE and not prio: continue
      ls.add(n)
  return max(ls) if ls else None
                                                                # }}}1

JLPT_BLACK  = set(""" 滑降 保母 """.split())
JLPT_WHITE  = set(""" お先に お待たせしました お邪魔します 一昨昨日
                      明々後日 """.split())
JLPT_CO_KA  = set(""" 彼れ 一杯 斯う 此処 事 此の 先 為る 然う 其処
                      其の 同 何の 成る 白 又 良く """.split())
JLPT_CO_NK  = set(""" さん じゃ そう ちゃん と どうか なんか ね はい
                  """.split())
JLPT_COMMON = set(""" あ あした あと あれ いく いち いっぱい えい こう
                      ここ こと この さっき さん し じゃ すり する
                      せっけん そう そこ その たて ちゃん つき と どう
                      どうか どの なる なんか ね はい はく ほんとう
                      また よい よく """.split())               # TODO

Entry.definition      = definition
Entry.words           = words
Entry.meanings        = meanings
Entry.meaning         = meaning
Entry.charsets        = charsets
Entry.chars           = chars
Entry._freq           = _freq
Entry._rank           = _rank
Entry.isprio          = isprio
Entry.prio_level      = prio_level
Entry.usually_kana    = usually_kana
Entry.gloss_pos_info  = gloss_pos_info
Entry.isnoun          = isnoun
Entry.isverb          = isverb
Entry.xinfo           = xinfo
Entry.xrefs           = xrefs
Entry.pitch           = pitch
Entry.__hash__        = lambda e: hash(e.seq)

Sense.isichidan = lambda s: any( "Ichidan verb" in x for x in s.pos )
Sense.isgodan   = lambda s: any(   "Godan verb" in x for x in s.pos )
Sense.istrans   = lambda s:   "transitive verb" in s.pos
Sense.isintrans = lambda s: "intransitive verb" in s.pos

Sense.istransitive    = Sense.istrans
Sense.isintransitive  = Sense.isintrans

def _prio_l(tags):
  return sum( PRIO.get(t, 0) for t in set(tags) ) # or None   # FIXME

def _prio_k(e):
  return _prio_l( x.text.strip() for x in e.findall("ke_pri") )

def _prio_r(e):
  return _prio_l( x.text.strip() for x in e.findall("re_pri") )

def _kanji_chars(s): return frozenset( c for c in s if M.iskanji(c) )

# TODO
# * extract & use more fields!?
#   - stagk, stagr, ...
#   - adjective?
# * assert kanji&reading only contain kanji&kana?
def parse_jmdict(file = JMDICT_FILE):                           # {{{1
  alang = "{http://www.w3.org/XML/1998/namespace}lang"
  data  = []
  with gzip.open(file) as f:
    with click.progressbar(ET.parse(f).getroot(), width = 0,
                           label = "parsing jmdict") as bar:
      for e in bar:
        seq, pos = int(e.find("ent_seq").text), ()
        kanji, reading, sense = [], [], []
        for ke in e.findall("k_ele"):           # 0+ kanji elem
          keb   = ke.find("keb").text.strip()   # word/phrase w/ kanji
          info  = tuple( x.text.strip() for x in ke.findall("ke_inf") )
          assert all( "\n" not in x and "\x1e" not in x for x in info )
          kanji.append(Kanji(keb, _kanji_chars(keb), info, _prio_k(ke)))
        for re in e.findall("r_ele"):           # 1+ reading elem
          reb   = re.find("reb").text.strip()   # reading elem
          restr = tuple( x.text.strip() for x in re.findall("re_restr") )
                  # reading only applies to keb subset
          info  = tuple( x.text.strip() for x in re.findall("re_inf") )
          assert all( "\n" not in x and "\x1e" not in x for xs in
                      [restr, info] for x in xs )
          reading.append(Reading(reb, restr, info, _prio_r(re)))
        for se in e.findall("sense"):           # 1+ sense elem
          pos   = tuple( x.text.strip() for x in se.findall("pos") ) or pos
                  # part of speech, applies to following senses too
          lang, gloss = None, []
          for x in se.findall("gloss"):
            l = x.get(alang, "eng")
            if l in LANGS and x.text:
              assert lang is None or lang == l
              lang = l
              gloss.append(x.text.strip())
          if lang is None: continue
          s_inf = tuple( x.text.strip() for x in se.findall("s_inf") )
          misc  = tuple( x.text.strip() for x in se.findall("misc") )
          xref  = tuple( y.strip() for x in se.findall("xref")
                                   for y in x.text.split("・")
                                   if not y.strip().isdigit() )
          assert seq < MAXSEQ
          assert all( "\n" not in x and "\x1e" not in x for xs in
                      [pos, gloss, s_inf, misc, xref] for x in xs )
          sense.append(Sense(pos, lang, tuple(gloss), s_inf + misc, xref))
        krs   = ( tuple(x) for x in [kanji, reading, sense] )
        jlpt  = jlpt_level(kanji, reading, _usukana(sense))
        data.append(Entry(seq, jlpt, *krs))
      return data
                                                                # }}}1

def load_jlpt(base = JLPT_FILE_BASE):                           # {{{1
  skip        = set("×|Ͼ立|あげる (=やる)|より、ほう".split("|"))
  kata        = "ローマじ ジェットき けしゴム".split()
  repl        = { "あたたか(い)": "あたたかい" }
  data, seen  = {}, set()
  for level in "12345":
    with open(base + level + "-vocab-hiragana") as f:
      for line in f:
        word, read = line.rstrip("\n").split("\t")
        if word in skip: continue
        if read.endswith("・する"): read = read[:-3]
        words = word.replace("  ", "/").split("/")
        reads = read.replace("  ", "/").replace(" / ", "/").split("/")
        reads = [ repl.get(r, r) for r in reads ]
        reads = [ r for r in reads if r in kata or M.ishiragana(r) ]
        if not reads: continue
        assert words and all( M.isokjap(w) for w in words )
        assert not (len(words) > 1 and len(reads) > 1)
        for w in words:
          for r in reads:
            assert w != r or M.iskana(w)
            if w == r: r = JLPTUK
            else: seen.add(w)
            data.setdefault(w, []).append((r, int(level)))
  for level in "12345":
    with open(base + level + "-vocab-eng") as f:
      for line in f:
        words = line.rstrip("\n").replace("  ", "/").split("/")
        words = [ w.strip() for w in words if w ]
        if skip & set(words): continue
        assert words and all( M.isokjap(w) for w in words )
        for w in words:
          if w not in seen:
            assert M.iskana(w)
            what = JLPTKK if M.iskatakana(w) else JLPTUK
            data.setdefault(w, []).append((what, int(level)))
  return data
                                                                # }}}1

JLPT = load_jlpt()                                              # TODO

# NB: kanji/reading/sense are retrieved in insertion (i.e. rowid) order!
def jmdict2sqldb(data, file = SQLITE_FILE):                     # {{{1
  with sqlite_do(file) as c:
    c.executescript(JMDICT_CREATE_SQL)
    with click.progressbar(data, width = 0, label = "writing jmdict") as bar:
      for e in bar:
        c.execute("INSERT INTO entry VALUES (?,?,?,?,?,?,?)",
                  (e.seq, e.jlpt, e._rank(), str(e._freq()),
                   e.prio_level(), e.isnoun(), e.isverb()))
        for k in e.kanji:
          c.execute("INSERT INTO kanji VALUES (?,?,?,?,?)",
                    (e.seq, k.elem, "".join(sorted(k.chars)),
                     "\n".join(k.info), k.prio))
        for k in sorted(e.chars()):
          c.execute("INSERT INTO kanji_code VALUES (?,?)",
                    (e.seq, ord(k)))
        for r in e.reading:
          c.execute("INSERT INTO reading VALUES (?,?,?,?,?)",
                    (e.seq, r.elem, "\n".join(r.restr),
                     "\n".join(r.info), r.prio))
        for s in e.sense:
          c.execute("INSERT INTO sense VALUES (?,?,?,?,?,?)",
                    (e.seq, "\n".join(s.pos), s.lang,
                     "\n".join(s.gloss), "\n".join(s.info),
                     "\n".join(s.xref)))
    c.execute("INSERT INTO version VALUES (?)", (DBVERSION,))
                                                                # }}}1

                                                                # {{{1
JMDICT_CREATE_SQL = """
  DROP TABLE IF EXISTS entry;
  DROP TABLE IF EXISTS kanji;
  DROP TABLE IF EXISTS kanji_code;
  DROP TABLE IF EXISTS reading;
  DROP TABLE IF EXISTS sense;
  DROP TABLE IF EXISTS version;

  CREATE TABLE entry(
    seq INTEGER PRIMARY KEY ASC,
    jlpt INTEGER,
    rank INTEGER,
    freq INTEGER,
    prio INTEGER,
    noun BOOLEAN,
    verb BOOLEAN
  );
  CREATE TABLE kanji(
    entry INTEGER,
    elem TEXT,
    chars TEXT,
    info TEXT,
    prio INTEGER,
    FOREIGN KEY(entry) REFERENCES entry(seq)
  );
  CREATE TABLE kanji_code(
    entry INTEGER,
    code INTEGER,
    FOREIGN KEY(entry) REFERENCES entry(seq)
  );
  CREATE TABLE reading(
    entry INTEGER,
    elem TEXT,
    restr TEXT,
    info TEXT,
    prio INTEGER,
    FOREIGN KEY(entry) REFERENCES entry(seq)
  );
  CREATE TABLE sense(
    entry INTEGER,
    pos TEXT,
    lang TEXT,
    gloss TEXT,
    info TEXT,
    xref TEXT,
    FOREIGN KEY(entry) REFERENCES entry(seq)
  );
  CREATE TABLE version(
    version INTEGER
  );

  CREATE INDEX idx_kanji ON kanji (entry);
  CREATE INDEX idx_kanji_code ON kanji_code (code);
  CREATE INDEX idx_reading ON reading (entry);
  CREATE INDEX idx_sense ON sense (entry);
"""                                                             # }}}1

def up2date(file = SQLITE_FILE):
  if os.path.exists(file):
    with sqlite_do(file) as c:
      if c.execute("SELECT name FROM sqlite_master WHERE" +
                   " type = 'table' AND name = 'version'").fetchone():
        v = c.execute("SELECT version FROM version").fetchone()[0]
        if v == DBVERSION: return True
  return False

def setup(file = SQLITE_FILE):                                  # {{{1
  F.setup()
  jmdict = parse_jmdict()
  jmdict2sqldb(jmdict, file)
                                                                # }}}1

def search_filter(noun, verb, prio, jlpt):
  if not any([noun, verb, prio, jlpt]): return ""
  s = []
  if noun and verb: s.append("(noun = 1 OR verb = 1)")
  elif noun       : s.append("noun = 1")
  elif verb       : s.append("verb = 1")
  if prio         : s.append("prio >= {}".format(MINPRIO))
  if jlpt         : s.append("({} <= jlpt AND jlpt <= {})"
                             .format(*map(int, jlpt)))
  return "WHERE " + " AND ".join(s)

def load_entry(c, seq, jlpt):                                   # {{{1
  k = tuple(
      Kanji(r["elem"], frozenset(r["chars"]),
            tuple(r["info"].splitlines()), r["prio"])
    for r in c.execute("SELECT * FROM kanji WHERE entry = ?" +
                       " ORDER BY rowid ASC", (seq,))
  )
  r = tuple(
      Reading(r["elem"], tuple(r["restr"].splitlines()),
              tuple(r["info"].splitlines()), r["prio"])
    for r in c.execute("SELECT * FROM reading WHERE entry = ?" +
                       " ORDER BY rowid ASC", (seq,))
  )
  s = tuple(
      Sense(tuple(r["pos"].splitlines()), r["lang"],
            tuple(r["gloss"].splitlines()),
            tuple(r["info"].splitlines()),
            tuple(r["xref"].splitlines()))
    for r in c.execute("SELECT * FROM sense WHERE entry = ?" +
                       " ORDER BY rowid ASC", (seq,))
  )
  return Entry(seq, jlpt, *(k, r, s))
                                                                # }}}1

# TODO
def search(q, langs = [LANGS[0]], max_results = None,           # {{{1
           noun = False, verb = False, prio = False,
           jlpt = None, file = SQLITE_FILE):
  fix_rank = lambda r: (r if r != F.NOFREQ else None)
  with sqlite_do(file) as c:
    if q.lower() == "+random":
      q = "+#{}".format(random_seq(noun, verb, prio, jlpt, file))
    if re.fullmatch(r"\+#\s*\d+", q):
      seq = int(q[2:].strip())
      for r in c.execute("SELECT rank, jlpt FROM entry WHERE seq = ?", (seq,)):
        yield load_entry(c, seq, r[1]), fix_rank(r[0]) # #=1
    elif "幸猫" in q:
      yield SACHINEKO, None
    else:
      lang  = ",".join( "'" + l + "'" for l in langs if l in LANGS )
      limit = "LIMIT " + str(int(max_results)) if max_results else ""
      fltr  = search_filter(noun, verb, prio, jlpt)
      ordr  = """ORDER BY IFNULL(prio, 0) >= {} DESC,
                          rank = {} ASC, prio IS NULL ASC,
                          rank ASC, jlpt DESC, prio DESC, seq ASC
              """.format(MINPRIO, F.NOFREQ)                     # TODO
      if len(q) == 1 and M.iskanji(q):
        query = ("""
          SELECT rank, seq, jlpt FROM (
            SELECT entry FROM kanji_code WHERE code = ?
          )
          INNER JOIN entry ON seq = entry
          {} {} {}
        """.format(fltr, ordr, limit), (ord(q),))             # safe!
      elif M.iscjk(q):
        query = ("""
          SELECT rank, seq, jlpt FROM (
              SELECT entry FROM kanji WHERE elem LIKE :q
            UNION
              SELECT entry FROM reading WHERE elem LIKE :q
          )
          INNER JOIN entry ON seq = entry
          {} {} {}
        """.format(fltr, ordr, limit), dict(q = "%"+q+"%"))   # safe!
      elif M.q2like(q):
        load_pcre_extension(c.connection)
        prms  = dict(q = M.q2like(q), re = M.q2rx(q))
        query = ("""
          SELECT rank, seq, jlpt FROM (
              SELECT entry FROM kanji WHERE
                elem LIKE :q AND elem REGEXP :re
            UNION
              SELECT entry FROM reading WHERE
                elem LIKE :q AND elem REGEXP :re
        """ + ("" if M.iscjk(M.without_e1w(q)) else """
            UNION
              SELECT entry FROM sense WHERE
                lang IN ({}) AND gloss LIKE :q AND gloss REGEXP :re
        """.format(lang)) + """
          )
          INNER JOIN entry ON seq = entry
          {} {} {}
        """.format(fltr, ordr, limit), prms)                  # safe!
      else:
        load_pcre_extension(c.connection)
        query = ("""
          SELECT rank, seq, jlpt FROM (
              SELECT entry FROM kanji WHERE elem REGEXP :re
            UNION
              SELECT entry FROM reading WHERE elem REGEXP :re
            UNION
              SELECT entry FROM sense WHERE
                lang IN ({}) AND gloss REGEXP :re
          )
          INNER JOIN entry ON seq = entry
          {} {} {}
        """.format(lang, fltr, ordr, limit),                  # safe!
          dict(re = M.q2rx(q)))
      for r, s, j in [ tuple(r) for r in c.execute(*query) ]: # eager!
        yield load_entry(c, s, j), fix_rank(r)
                                                                # }}}1

def by_freq(offset = 0, limit = 1000, file = SQLITE_FILE):
  with sqlite_do(file) as c:
    q = """ SELECT seq, rank, jlpt FROM entry
              WHERE prio >= {} AND rank != {}
              ORDER BY rank ASC LIMIT ? OFFSET ?
        """.format(MINPRIO, F.NOFREQ)                         # safe!
    ents = [ tuple(r) for r in c.execute(q, (int(limit), int(offset))) ]
    for seq, rank, jlpt in ents:
      yield load_entry(c, seq, jlpt), rank

def by_jlpt(n, offset = 0, limit = 1000, file = SQLITE_FILE):
  with sqlite_do(file) as c:
    query =  (""" SELECT seq, jlpt FROM entry
                    WHERE prio >= {} AND jlpt = ?
                    ORDER BY rank ASC LIMIT ? OFFSET ?
              """.format(MINPRIO), (int(n), int(limit), int(offset)))
    for seq, jlpt in [ tuple(r) for r in c.execute(*query) ]:
      yield load_entry(c, seq, jlpt)

def random_seq(noun = False, verb = False, prio = False, jlpt = None,
               file = SQLITE_FILE):
  f = search_filter(noun, verb, prio, jlpt)
  with sqlite_do(file) as c:
    q = "SELECT seq FROM entry {} ORDER BY RANDOM() LIMIT 1".format(f)
    return c.execute(q).fetchone()[0]                       # ^ safe!

SACHINEKO = Entry(
  29483, None,
  (Kanji("幸猫", frozenset("幸猫"), (), None),),
  (Reading("フェリックス", (), (), None),),
  (Sense((), "eng", ("(=^・^=)",), (), ()),)
)

if __name__ == "__main__":
  if "--doctest" in sys.argv:
    verbose = "--verbose" in sys.argv
    import doctest
    if doctest.testmod(verbose = verbose)[0]: sys.exit(1)

# vim: set tw=70 sw=2 sts=2 et fdm=marker :
