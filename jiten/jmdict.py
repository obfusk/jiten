#!/usr/bin/python3
# encoding: utf-8

# --                                                            ; {{{1
#
# File        : jiten/jmdict.py
# Maintainer  : Felix C. Stegerman <flx@obfusk.net>
# Date        : 2020-06-16
#
# Copyright   : Copyright (C) 2020  Felix C. Stegerman
# Version     : v0.0.1
# License     : AGPLv3+
#
# --                                                            ; }}}1

                                                                # {{{1
r"""

>>> jmdict = parse_jmdict()
>>> len(jmdict)
188250

>>> baka = [ x for x in jmdict if any( r.elem == "ばか" for r in x.reading ) ][0]
>>> baka.seq
1601260
>>> baka.definition()
('ばか', 'バカ', '馬鹿', '莫迦', '破家', '馬稼')
>>> baka.usually_kana()
True
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
[usu. in compounds]
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

>>> iku = [ x for x in jmdict if any( r.elem == "行く" for r in x.kanji) ][0]
>>> iku.seq
1578850
>>> iku.definition()
('いく', 'ゆく', '行く', '逝く', '往く')
>>> iku.usually_kana()
True
>>> print("\n".join(M.flatten(iku.meanings())))
to go
to move (in a direction or towards a specific location)
to head (towards)
to be transported (towards)
to reach
to proceed
to take place
[い sometimes omitted in auxiliary use]
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

"""                                                             # }}}1

import gzip, re, sys
import xml.etree.ElementTree as ET

from collections import namedtuple
from functools import lru_cache

import click

from . import freq as F
from . import misc as M
from .sql import sqlite_do

SQLITE_FILE   = M.resource_path("res/jmdict.sqlite3")
JMDICT_FILE   = M.resource_path("res/jmdict/jmdict.xml.gz")

USUKANA       = "word usually written using kana alone"

LANGS         = "eng dut ger".split()
DLANG         = "eng"

Entry         = namedtuple("Entry",
                """seq kanji reading sense""".split())
Kanji         = namedtuple("Kanji"  , """elem chars""".split())
Reading       = namedtuple("Reading", """elem restr""".split())
Sense         = namedtuple("Sense",
                """pos lang gloss info usually_kana""".split())

# TODO
# * include all readings if usually_kana? or only frequent ones?
@lru_cache(maxsize = None)
def definition(e):
  r, k  = [ list(x) for x in [e.reading, e.kanji] ]
  xs    = r + k if e.usually_kana() else k or r
  return tuple(M.uniq( x.elem for x in xs ))

@lru_cache(maxsize = None)
def words(e):
  return frozenset( x.elem for x in M.flatten([e.kanji, e.reading]) )

@lru_cache(maxsize = None)
def meanings(e, lang = DLANG):
  return tuple( tuple(M.flatten([s.gloss, s.info_notes()]))
                for s in e.sense if s.lang == lang )

@lru_cache(maxsize = None)
def meaning(e, lang = DLANG): return frozenset(M.flatten(e.meanings(lang)))

@lru_cache(maxsize = None)
def charsets(e): return frozenset( k.chars for k in e.kanji )

@lru_cache(maxsize = None)
def chars(e):
  return frozenset(M.flatten( k.chars for k in e.kanji ))

@lru_cache(maxsize = None)
def freq(e): return sum( F.freq.get(w, 0) for w in e.definition() )

@lru_cache(maxsize = None)
def rank(e): return min( F.rank(w) for w in e.definition() )

@lru_cache(maxsize = None)
def usually_kana(e):
  return any( s.usually_kana for s in e.sense )

Entry.definition      = definition
Entry.words           = words
Entry.meanings        = meanings
Entry.meaning         = meaning
Entry.charsets        = charsets
Entry.chars           = chars
Entry.freq            = freq
Entry.rank            = rank
Entry.usually_kana    = usually_kana
Entry.__hash__        = lambda e: hash(e.seq)

def isichidan(s): return any( "Ichidan verb" in x for x in s.pos )
def isgodan(s):   return any(   "Godan verb" in x for x in s.pos )

def istransitive(s):   return   "transitive verb" in s.pos
def isintransitive(s): return "intransitive verb" in s.pos

Sense.isichidan       = isichidan
Sense.isgodan         = isgodan
Sense.istransitive    = istransitive
Sense.isintransitive  = isintransitive
Sense.info_notes      = lambda s: [ "["+i+"]" for i in s.info ]

def _usually_kana(e):
  return any( USUKANA in x.text for x in e.findall("misc") )

def _kanji_chars(s): return frozenset( c for c in s if M.iskanji(c) )

# TODO
# * extract & use more fields!?
# * stagk, stagr, xref, ...; adjective?
# * ke_inf -> ateji!
# * assert kanji, reading only contain kanji, kana?
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
          kanji.append(Kanji(keb, _kanji_chars(keb)))
        for re in e.findall("r_ele"):           # 1+ reading elem
          reb   = re.find("reb").text.strip()   # reading elem
          restr = tuple( x.text.strip() for x in re.findall("re_restr") )
                  # reading only applies to keb subset
          assert all( "\n" not in x for x in restr )
          reading.append(Reading(reb, restr))
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
          assert all( "\n" not in x for x in pos )
          assert all( "\n" not in x for x in gloss )
          assert all( "\n" not in x for x in s_inf )
          assert all( "" not in x for x in gloss )
          assert all( "" not in x for x in s_inf )
          sense.append(Sense(pos, lang, tuple(gloss), s_inf, _usually_kana(se)))
        data.append(Entry(seq, *( tuple(x) for x in [kanji, reading, sense] )))
      return data
                                                                # }}}1

# NB: kanji/reading/sense are retrieved in insertion order!
def jmdict2sqldb(data, file = SQLITE_FILE):                     # {{{1
  with sqlite_do(file) as c:
    c.executescript(JMDICT_CREATE_SQL)
    with click.progressbar(data, width = 0, label = "writing jmdict") as bar:
      for e in bar:
        c.execute("INSERT INTO entry VALUES (?,?,?,?)",
                  (e.seq, str(e.freq()), e.rank(), e.usually_kana()))
        for k in e.kanji:
          c.execute("INSERT INTO kanji VALUES (?,?,?)",
                    (e.seq, k.elem, "".join(k.chars)))
        for r in e.reading:
          c.execute("INSERT INTO reading VALUES (?,?,?)",
                    (e.seq, r.elem, "\n".join(r.restr)))
        for s in e.sense:
          c.execute("INSERT INTO sense VALUES (?,?,?,?,?,?)",
                    (e.seq, "\n".join(s.pos), s.lang,
                     "\n".join(s.gloss), "\n".join(s.info),
                     s.usually_kana))
                                                                # }}}1

                                                                # {{{1
JMDICT_CREATE_SQL = """
  DROP TABLE IF EXISTS entry;
  DROP TABLE IF EXISTS kanji;
  DROP TABLE IF EXISTS reading;
  DROP TABLE IF EXISTS sense;
  CREATE TABLE entry(
    seq INTEGER PRIMARY KEY ASC,
    freq INTEGER,
    rank INTEGER,
    usually_kana BOOLEAN
  );
  CREATE TABLE kanji(
    entry INTEGER,
    elem TEXT,
    chars TEXT,
    FOREIGN KEY(entry) REFERENCES entry(seq)
  );
  CREATE TABLE reading(
    entry INTEGER,
    elem TEXT,
    restr TEXT,
    FOREIGN KEY(entry) REFERENCES entry(seq)
  );
  CREATE TABLE sense(
    entry INTEGER,
    pos TEXT,
    lang TEXT,
    gloss TEXT,
    info TEXT,
    usually_kana BOOLEAN,
    FOREIGN KEY(entry) REFERENCES entry(seq)
  );
"""                                                             # }}}1

def setup():
  F.setup()
  jmdict = parse_jmdict()
  jmdict2sqldb(jmdict)

def search(q, langs = [DLANG], max_results = None,              # {{{1
           file = SQLITE_FILE):
  entries = set()
  with sqlite_do(file) as c:
    rx  = re.compile(q, re.I | re.M)
    mat = lambda x: rx.search(x) is not None
    c.connection.create_function("matches", 1, mat)
    for r in c.execute("SELECT entry FROM kanji WHERE matches(elem)"):
      entries.add(r["entry"])
    for r in c.execute("SELECT entry FROM reading WHERE matches(elem)"):
      entries.add(r["entry"])
    for lang in langs:
      for r in c.execute("SELECT entry FROM sense WHERE" +
                         " lang = ? AND matches(gloss)", (lang,)):
        entries.add(r["entry"])
    ents = sorted( tuple(r) for e in entries for r in c.execute(
      "SELECT rank, seq FROM entry WHERE seq = ?", (e,) # #=1
    ))
    for i, (rank, seq) in enumerate(ents):
      if max_results and i >= max_results: break
      k = tuple(
        Kanji(r["elem"], frozenset(r["chars"]))
        for r in c.execute("SELECT * FROM kanji WHERE entry = ?" +
                           " ORDER BY rowid ASC", (seq,))
      )
      r = tuple(
        Reading(r["elem"], tuple(r["restr"].splitlines()))
        for r in c.execute("SELECT * FROM reading WHERE entry = ?" +
                           " ORDER BY rowid ASC", (seq,))
      )
      s = tuple(
        Sense(tuple(r["pos"].splitlines()), r["lang"],
              tuple(r["gloss"].splitlines()),
              tuple(r["info"].splitlines()), bool(r["usually_kana"]))
        for r in c.execute("SELECT * FROM sense WHERE entry = ?" +
                           " ORDER BY rowid ASC", (seq,))
      )
      yield (Entry(seq, *( tuple(x) for x in [k, r, s] )),
             (rank if rank != F.NOFREQ else None))
                                                                # }}}1

if __name__ == "__main__":
  if "--doctest" in sys.argv:
    import doctest
    if doctest.testmod(verbose = True)[0]: sys.exit(1)

# vim: set tw=70 sw=2 sts=2 et fdm=marker :
