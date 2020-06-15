#!/usr/bin/python3
# encoding: utf-8

# --                                                            ; {{{1
#
# File        : jiten/jmdict.py
# Maintainer  : Felix C. Stegerman <flx@obfusk.net>
# Date        : 2020-06-15
#
# Copyright   : Copyright (C) 2020  Felix C. Stegerman
# Version     : v0.0.1
# License     : GPLv3+
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
>>> print("\n".join(flatten(baka.meanings())))
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
>>> print("\n".join(list(flatten(baka.meanings("ger")))[:10]))
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
>>> print("\n".join(flatten(iku.meanings())))
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
>>> print("\n".join(list(flatten(iku.meanings("dut")))[:10]))
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

import gzip, itertools, sqlite3, sys
import xml.etree.ElementTree as ET

from collections import namedtuple
from functools import lru_cache

import click

iskanji = lambda c: 0x4e00 <= ord(c) <= 0x9faf
flatten = itertools.chain.from_iterable

def uniq(xs):
  seen = set()
  for x in xs:
    if x not in seen:
      seen.add(x); yield x

SQLITE_FILE   = "res/jmdict.sqlite3"
JMDICT_FILE   = "res/jmdict/jmdict.xml.gz"

USUKANA       = "word usually written using kana alone"

LANGS         = "eng dut ger".split()
DLANG         = "eng"

Entry         = namedtuple("Entry",
                """seq kanji reading sense""".split())
Kanji         = namedtuple("Kanji"  , """elem chars""".split())
Reading       = namedtuple("Reading", """elem restr""".split())
Sense         = namedtuple("Sense",
                """pos lang gloss info usually_kana""".split())

@lru_cache(maxsize = None)
def usually_kana(e):
  return any( s.usually_kana for s in e.sense )

# TODO
# * include all readings if usually_kana? or only frequent ones?
@lru_cache(maxsize = None)
def definition(e):
  r, k  = [ list(x) for x in [e.reading, e.kanji] ]
  xs    = r + k if e.usually_kana() else k or r
  return tuple(uniq( x.elem for x in xs ))

@lru_cache(maxsize = None)
def words(e):
  return frozenset( x.elem for x in flatten([e.kanji, e.reading]) )

@lru_cache(maxsize = None)
def meanings(e, lang = DLANG):
  return tuple( tuple(flatten([s.gloss, s.info_notes()]))
                for s in e.sense if s.lang == lang )

@lru_cache(maxsize = None)
def meaning(e, lang = DLANG): return frozenset(flatten(e.meanings(lang)))

@lru_cache(maxsize = None)
def charsets(e): return frozenset( k.chars for k in e.kanji )

@lru_cache(maxsize = None)
def chars(e):
  return frozenset(flatten( k.chars for k in e.kanji ))

Entry.usually_kana    = usually_kana
Entry.definition      = definition
Entry.words           = words
Entry.meanings        = meanings
Entry.meaning         = meaning
Entry.charsets        = charsets
Entry.chars           = chars
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

def _kanji_chars(s): return frozenset( c for c in s if iskanji(c) )

# TODO
# * stagk, stagr, xref, ...; adjective?
# * ke_inf -> ateji!
# * assert kanji, reading only contain kanji, kana?
def parse_jmdict(file = JMDICT_FILE):                           # {{{1
  alang = "{http://www.w3.org/XML/1998/namespace}lang"
  data  = []
  with gzip.open(file) as f:
    with click.progressbar(ET.parse(f).getroot(),
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
          sense.append(Sense(pos, lang, tuple(gloss), s_inf, _usually_kana(se)))
        data.append(Entry(seq, *( tuple(x) for x in [kanji, reading, sense] )))
      return data
                                                                # }}}1

# TODO
def jmdict2sqldb(data, file = SQLITE_FILE):                     # {{{1
  conn = sqlite3.connect(file); c = conn.cursor()
  c.executescript(JMDICT_CREATE_SQL)
  with click.progressbar(data, label = "writing jmdict") as bar:
    for e in bar:
      c.execute("INSERT INTO jmdict VALUES (?,?)",
                (e.seq, e.usually_kana()))
      for k in e.kanji:
        c.execute("INSERT INTO jmdict_kanji VALUES (?,?,?)",
                  (e.seq, k.elem, "".join(k.chars)))
      for r in e.reading:
        c.execute("INSERT INTO jmdict_reading VALUES (?,?,?)",
                  (e.seq, r.elem, "\n".join(r.restr)))
      for s in e.sense:
        c.execute("INSERT INTO jmdict_sense VALUES (?,?,?,?,?,?)",
                  (e.seq, "\n".join(s.pos), s.lang,
                   "\n".join(s.gloss), "\n".join(s.info),
                   s.usually_kana))
  conn.commit(); conn.close()
                                                                # }}}1

                                                                # {{{1
JMDICT_CREATE_SQL = """
  DROP TABLE IF EXISTS jmdict;
  DROP TABLE IF EXISTS jmdict_kanji;
  DROP TABLE IF EXISTS jmdict_reading;
  DROP TABLE IF EXISTS jmdict_sense;
  CREATE TABLE jmdict(
    seq INTEGER PRIMARY KEY ASC,
    usually_kana BOOLEAN
  );
  CREATE TABLE jmdict_kanji(
    entry INTEGER,
    elem TEXT,
    chars TEXT,
    FOREIGN KEY(entry) REFERENCES jmdict(seq)
  );
  CREATE TABLE jmdict_reading(
    entry INTEGER,
    elem TEXT,
    restr TEXT,
    FOREIGN KEY(entry) REFERENCES jmdict(seq)
  );
  CREATE TABLE jmdict_sense(
    entry INTEGER,
    pos TEXT,
    lang TEXT,
    gloss TEXT,
    info TEXT,
    usually_kana BOOLEAN,
    FOREIGN KEY(entry) REFERENCES jmdict(seq)
  );
"""                                                             # }}}1

def setup():
  jmdict = parse_jmdict()
  jmdict2sqldb(jmdict)

# ...

# if __name__ == "__main__":
#   import doctest
#   if doctest.testmod()[0]: sys.exit(1)

# vim: set tw=70 sw=2 sts=2 et fdm=marker :
