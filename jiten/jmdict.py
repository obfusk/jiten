#!/usr/bin/python3
# encoding: utf-8

# --                                                            ; {{{1
#
# File        : jiten/jmdict.py
# Maintainer  : Felix C. Stegerman <flx@obfusk.net>
# Date        : 2020-06-19
#
# Copyright   : Copyright (C) 2020  Felix C. Stegerman
# Version     : v0.0.1
# License     : AGPLv3+
#
# --                                                            ; }}}1

                                                                # {{{1
r"""

JMDict.

>>> DBVERSION
1

>>> jmdict = parse_jmdict()
>>> len(jmdict)
188250

>>> print(jmdict[-1].sense[0].gloss[0])
Japanese-Multilingual Dictionary Project - Creation Date: 2020-06-14

>>> baka = [ x for x in jmdict if any( r.elem == "ばか" for r in x.reading ) ][0]
>>> baka.seq
1601260
>>> baka.definition()
('ばか', 'バカ', '馬鹿', '莫迦', '破家', '馬稼')
>>> baka.usually_kana()
True
>>> baka.isprio()
True
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
>>> iku.usually_kana()
True
>>> iku.isprio()
True
>>> iku.isnoun()
False
>>> iku.isverb()
True
>>> any( s.isichidan() for s in iku.sense )
False
>>> any( s.isgodan() for s in iku.sense )
True
>>> any( s.istransitive() for s in iku.sense )
False
>>> any( s.isintransitive() for s in iku.sense )
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

"""                                                             # }}}1

import gzip, os, re, sys
import xml.etree.ElementTree as ET

from collections import namedtuple

import click

from . import freq as F
from . import misc as M
from .sql import sqlite_do

DBVERSION     = 1 # NB: update this when data/schema changes
SQLITE_FILE   = M.resource_path("res/jmdict.sqlite3")
JMDICT_FILE   = M.resource_path("res/jmdict/jmdict.xml.gz")

MAXSEQ        = 10000000
PRIO          = "news1 ichi1 spec1 spec2 gai1".split()
USUKANA       = "word usually written using kana alone"
LANGS         = "eng dut ger".split()

Entry         = namedtuple("Entry"  , """seq kanji reading sense""".split())
Kanji         = namedtuple("Kanji"  , """elem chars info prio""".split())
Reading       = namedtuple("Reading", """elem restr info prio""".split())
Sense         = namedtuple("Sense"  , """pos lang gloss info xref""".split())

# TODO
# * include all readings if usually_kana? or only frequent ones?
def definition(e):
  r, k  = [ list(x) for x in [e.reading, e.kanji] ]
  xs    = r + k if e.usually_kana() else k or r
  return tuple(M.uniq( x.elem for x in xs ))

def words(e):
  return frozenset( x.elem for x in M.flatten([e.kanji, e.reading]) )

def meanings(e, *a):
  l = a or [LANGS[0]]
  return tuple( s.gloss for s in e.sense if s.lang in l )

def meaning(e, *a): return frozenset(M.flatten(e.meanings(*a)))

def charsets(e): return frozenset( k.chars for k in e.kanji )

def chars(e):
  return frozenset(M.flatten( k.chars for k in e.kanji ))

# TODO: load from DB
def _freq(e): return sum( F.freq.get(w, 0) for w in e.definition() )

# TODO: load from DB
def _rank(e): return min( F.rank(w) for w in e.definition() )

def isprio(e):
  return any( x.prio for x in M.flatten([e.kanji, e.reading]) )

def usually_kana(e):
  return any( USUKANA in s.info for s in e.sense )

def gloss_pos_info(e, langs):
  gloss, pos, info = {}, [], []
  for l in langs:
    for s in e.sense:
      if not s.lang == l: continue
      pos.extend(s.pos); info.extend(s.info)
      gloss.setdefault(l, []).append(s.gloss)
  return gloss, M.uniq(pos + info)

def isnoun(e):
  return any( "noun" in p.split() for s in e.sense for p in s.pos )

def isverb(e):
  return any( "verb" in p.split() for s in e.sense for p in s.pos )

def xinfo(e):
  return M.uniq( z for x in [e.kanji, e.reading]
                   for y in x for z in y.info )

def xrefs(e):
  return M.uniq( x for s in e.sense for x in s.xref )

Entry.definition      = definition
Entry.words           = words
Entry.meanings        = meanings
Entry.meaning         = meaning
Entry.charsets        = charsets
Entry.chars           = chars
Entry._freq           = _freq
Entry._rank           = _rank
Entry.isprio          = isprio
Entry.usually_kana    = usually_kana
Entry.gloss_pos_info  = gloss_pos_info
Entry.isnoun          = isnoun
Entry.isverb          = isverb
Entry.xinfo           = xinfo
Entry.xrefs           = xrefs
Entry.__hash__        = lambda e: hash(e.seq)

def isichidan(s): return any( "Ichidan verb" in x for x in s.pos )
def isgodan(s):   return any(   "Godan verb" in x for x in s.pos )

def istransitive(s):   return   "transitive verb" in s.pos
def isintransitive(s): return "intransitive verb" in s.pos

Sense.isichidan       = isichidan
Sense.isgodan         = isgodan
Sense.istransitive    = istransitive
Sense.isintransitive  = isintransitive

def _isprio_k(e):
  return any( x.text.strip() in PRIO for x in e.findall("ke_pri") )

def _isprio_r(e):
  return any( x.text.strip() in PRIO for x in e.findall("re_pri") )

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
          assert all( "\n" not in x and "" not in x for x in info )
          kanji.append(Kanji(keb, _kanji_chars(keb), info, _isprio_k(ke)))
        for re in e.findall("r_ele"):           # 1+ reading elem
          reb   = re.find("reb").text.strip()   # reading elem
          restr = tuple( x.text.strip() for x in re.findall("re_restr") )
                  # reading only applies to keb subset
          info  = tuple( x.text.strip() for x in re.findall("re_inf") )
          assert all( "\n" not in x and "" not in x for xs in
                      [restr, info] for x in xs )
          reading.append(Reading(reb, restr, info, _isprio_r(re)))
        for se in e.findall("sense"):           # 1+ sense elem
          pos   = tuple( x.text.strip() for x in se.findall("pos") ) or pos
                  # part of speech, applies to following senses too
          lang, gloss = None, []
          for x in se.findall("gloss"):
            if x.attrib[alang] in LANGS and x.text:
              assert lang is None or lang == x.attrib[alang]
              lang = x.attrib[alang]
              gloss.append(x.text.strip())
          if lang is None: continue
          s_inf = tuple( x.text.strip() for x in se.findall("s_inf") )
          misc  = tuple( x.text.strip() for x in se.findall("misc") )
          xref  = tuple( y.strip() for x in se.findall("xref")
                                   for y in x.text.split("・")
                                   if not y.strip().isdigit() )
          assert seq < MAXSEQ
          assert all( "\n" not in x and "" not in x for xs in
                      [pos, gloss, s_inf, misc, xref] for x in xs )
          sense.append(Sense(pos, lang, tuple(gloss), s_inf + misc, xref))
        data.append(Entry(seq, *( tuple(x) for x in [kanji, reading, sense] )))
      return data
                                                                # }}}1

# NB: kanji/reading/sense are retrieved in insertion (i.e. rowid) order!
def jmdict2sqldb(data, file = SQLITE_FILE):                     # {{{1
  with sqlite_do(file) as c:
    c.executescript(JMDICT_CREATE_SQL)
    with click.progressbar(data, width = 0, label = "writing jmdict") as bar:
      for e in bar:
        c.execute("INSERT INTO entry VALUES (?,?,?,?,?,?)",
                  (e.seq, e._rank(), str(e._freq()),
                   e.isprio(), e.isnoun(), e.isverb()))
        for k in e.kanji:
          c.execute("INSERT INTO kanji VALUES (?,?,?,?,?)",
                    (e.seq, k.elem, "".join(k.chars),
                     "\n".join(k.info), k.prio))
        for r in e.reading:
          c.execute("INSERT INTO reading VALUES (?,?,?,?,?)",
                    (e.seq, r.elem, "\n".join(r.restr),
                     "\n".join(r.info), r.prio))
        for s in e.sense:
          c.execute("INSERT INTO sense VALUES (?,?,?,?,?,?)",
                    (e.seq, "\n".join(s.pos), s.lang,
                     "\n".join(s.gloss), "\n".join(s.info),
                     "\n".join(s.xref)))
                                                                # }}}1

                                                                # {{{1
JMDICT_CREATE_SQL = """
  DROP TABLE IF EXISTS entry;
  DROP TABLE IF EXISTS kanji;
  DROP TABLE IF EXISTS reading;
  DROP TABLE IF EXISTS sense;
  DROP TABLE IF EXISTS version;

  CREATE TABLE entry(
    seq INTEGER PRIMARY KEY ASC,
    rank INTEGER,
    freq INTEGER,
    prio BOOLEAN,
    noun BOOLEAN,
    verb BOOLEAN
  );
  CREATE TABLE kanji(
    entry INTEGER,
    elem TEXT,
    chars TEXT,
    info TEXT,
    prio BOOLEAN,
    FOREIGN KEY(entry) REFERENCES entry(seq)
  );
  CREATE TABLE reading(
    entry INTEGER,
    elem TEXT,
    restr TEXT,
    info TEXT,
    prio BOOLEAN,
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
  INSERT INTO version VALUES ({});

  CREATE INDEX idx_kanji ON kanji (entry);
  CREATE INDEX idx_reading ON reading (entry);
  CREATE INDEX idx_sense ON sense (entry);
""".format(DBVERSION)                                           # }}}1

def setup(file = SQLITE_FILE):                                  # {{{1
  if os.path.exists(file):
    with sqlite_do(file) as c:
      if c.execute("SELECT name FROM sqlite_master WHERE" +
                   " type = 'table' AND name = 'version'").fetchone():
        v = c.execute("SELECT version FROM version").fetchone()[0]
        if v == DBVERSION: return False # up to date
  F.setup()
  jmdict = parse_jmdict()
  jmdict2sqldb(jmdict, file)
  return True
                                                                # }}}1

def nvp(noun, verb, prio):
  if not any([noun, verb, prio]): return ""
  s = []
  if noun and verb: s.append("(noun = 1 OR verb = 1)")
  elif noun       : s.append("noun = 1")
  elif verb       : s.append("verb = 1")
  if prio         : s.append("prio = 1")
  return "WHERE " + " AND ".join(s)

def search(q, langs = [LANGS[0]], max_results = None,           # {{{1
           noun = False, verb = False, prio = False,
           file = SQLITE_FILE):
  with sqlite_do(file) as c:
    rx      = re.compile(q, re.I | re.M)
    mat     = lambda x: rx.search(x) is not None
    c.connection.create_function("matches", 1, mat)
    lang    = ",".join( "'" + l + "'" for l in langs if l in LANGS )
    limit   = "LIMIT " + str(int(max_results)) if max_results else ""
    entries = [ tuple(r) for r in c.execute("""
      SELECT rank, seq FROM (
          SELECT entry FROM kanji WHERE matches(elem)
        UNION
          SELECT entry FROM reading WHERE matches(elem)
        UNION
          SELECT entry FROM sense WHERE
            lang IN ({}) AND matches(gloss)
      )
      INNER JOIN entry ON seq = entry
      {}
      ORDER BY prio DESC, rank ASC, seq ASC
      {}
    """.format(lang, nvp(noun, verb, prio), limit)) ]
    for i, (rank, seq) in enumerate(entries):
      k = tuple(
          Kanji(r["elem"], frozenset(r["chars"]),
                tuple(r["info"].splitlines()), bool(r["prio"]))
        for r in c.execute("SELECT * FROM kanji WHERE entry = ?" +
                           " ORDER BY rowid ASC", (seq,))
      )
      r = tuple(
          Reading(r["elem"], tuple(r["restr"].splitlines()),
                  tuple(r["info"].splitlines()), bool(r["prio"]))
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
      e = Entry(seq, *( tuple(x) for x in [k, r, s] ))
      yield e, (rank if rank != F.NOFREQ else None)
                                                                # }}}1

if __name__ == "__main__":
  if "--doctest" in sys.argv:
    verbose = "--verbose" in sys.argv
    import doctest
    if doctest.testmod(verbose = verbose)[0]: sys.exit(1)

# vim: set tw=70 sw=2 sts=2 et fdm=marker :
