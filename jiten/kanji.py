#!/usr/bin/python3
# encoding: utf-8

# --                                                            ; {{{1
#
# File        : jiten/kanji.py
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

KanjiDic.

>>> kanjidic = parse_kanjidic()
>>> len(kanjidic)
13108
>>> len(set( x.char for x in kanjidic ))
13108

>>> [ x for x in kanjidic if x.char == "猫" ][0]
Entry(char='猫', cat='KANJI', level='常用', strokes=11, freq=1702, jlpt=2, skip='1-3-8', on=('ビョウ',), kun=('ねこ',), nanori=(), meaning=('cat',))

>>> [ x for x in kanjidic if x.char == "日" ][0]
Entry(char='日', cat='KANJI', level='常用1', strokes=4, freq=1, jlpt=4, skip='3-3-1', on=('ニチ', 'ジツ'), kun=('ひ', '-び', '-か'), nanori=('あ', 'あき', 'いる', 'く', 'くさ', 'こう', 'す', 'たち', 'に', 'にっ', 'につ', 'へ'), meaning=('day', 'sun', 'Japan', 'counter for days'))

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
953
>>> len([ x for x in kanjidic if not len(x.kun) ])
3289
>>> len([ x for x in kanjidic if not len(x.meaning) ])
2753

"""                                                             # }}}1

import gzip, re, sys
import xml.etree.ElementTree as ET

from collections import namedtuple

import click

from . import misc as M
from .sql import sqlite_do

SQLITE_FILE   = M.resource_path("res/kanji.sqlite3")
KANJIDIC_FILE = M.resource_path("res/jmdict/kanjidic2.xml.gz")

NOFREQ        = 9999

Entry = namedtuple("Entry", """char cat level strokes freq jlpt
                               skip on kun nanori meaning""".split())

def level(l):
  if 1 <= l <= 6: return "常用" + str(l)
  if l == 8     : return "常用"
  if l == 9     : return "人名"
  if l == 10    : return "人名(常用)"
  raise ValueError("unexpected level: " + l)

def category(c):
  if M.iskanji(c) : return "KANJI"
  if M.iscompat(c): return "CJK COMPATIBILITY IDEOGRAPH"
  if M.isuniext(c): return "CJK UNIFIED IDEOGRAPH"
  raise ValueError("unexpected category for: " + c)

def maybe(x, f, d = None):
  return d if x is None else f(x)

# TODO
# * rmgroup?!
def parse_kanjidic(file = KANJIDIC_FILE):                       # {{{1
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
        on      = tuple( r.text.strip() for r in
                         e.findall(".//reading[@r_type='ja_on']") )
        kun     = tuple( r.text.strip() for r in
                         e.findall(".//reading[@r_type='ja_kun']") )
        nanori  = tuple( n.text.strip() for n in e.findall(".//nanori") )
        meaning = tuple( m.text.strip() for m in e.findall(".//meaning")
                                if "m_lang" not in m.attrib )
        assert len(char) == 1
        assert all( M.iskatakana(c) or c in ".-" for x in on for c in x )
        assert all( all( M.ishiragana(c) or c in ".-ー" for c in x ) or
                    all( M.iskatakana(c) for c in x ) for x in kun )
        assert all( "\n" not in x for x in on )
        assert all( "\n" not in x for x in kun )
        assert all( "\n" not in x for x in nanori )
        assert all( "\n" not in x for x in meaning )
        data.append(Entry(char, category(char), lvl, strokes, freq,
                          jlpt, skip, on, kun, nanori, meaning))
      return data
                                                                # }}}1

def kanjidic2sqldb(data, file = SQLITE_FILE):                   # {{{1
  with sqlite_do(file) as c:
    c.executescript(KANJIDIC_CREATE_SQL)
    with click.progressbar(data, width = 0, label = "writing kanjidic") as bar:
      for e in bar:
        c.execute("INSERT INTO entry VALUES ({})"
                  .format(",".join(["?"]*12)),
                  (ord(e.char), e.char, e.cat, e.level, e.strokes,
                   e.freq, e.jlpt, e.skip, "\n".join(e.on),
                   "\n".join(e.kun), "\n".join(e.nanori),
                   "\n".join(e.meaning)))
                                                                # }}}1

                                                                # {{{1
KANJIDIC_CREATE_SQL = """
  DROP TABLE IF EXISTS entry;
  CREATE TABLE entry(
    code INTEGER PRIMARY KEY ASC,
    char TEXT,
    cat TEXT,
    level TEXT,
    strokes INTEGER,
    freq INTEGER,
    jlpt INTEGER,
    skip TEXT,
    on_ TEXT,
    kun TEXT,
    nanori TEXT,
    meaning TEXT
  );
"""                                                             # }}}1

def setup(file = SQLITE_FILE):
  kanjidic = parse_kanjidic()
  kanjidic2sqldb(kanjidic, file)

def search(q, max_results = None, file = SQLITE_FILE):          # {{{1
  ent   = lambda r: Entry(*(list(r[1:8]) + [ tuple(x.splitlines())
                                             for x in r[8:] ]))
  ideo  = tuple(M.uniq(filter(M.isideo, q)))
  with sqlite_do(file) as c:
    if ideo:
      for char in ideo:
        for r in c.execute("SELECT * FROM entry WHERE code = ?", (ord(char),)):
          yield ent(r) # #=1
    else:
      rx    = re.compile(q, re.I | re.M)
      mat1  = lambda x: rx.search(x) is not None
      mat2  = lambda x: rx.search(x.replace(".", "")
                                   .replace("-", "")) is not None
      c.connection.create_function("matches1", 1, mat1)
      c.connection.create_function("matches2", 1, mat2)
      limit = "LIMIT " + str(int(max_results)) if max_results else ""
      for i, r in enumerate(c.execute("""
          SELECT * FROM entry
            WHERE
              matches1(on_) OR matches1(kun) OR matches1(nanori) OR
              matches2(on_) OR matches2(kun) OR matches2(nanori) OR
              matches1(meaning)
            ORDER BY
              IFNULL(freq, {}) ASC, code ASC
            {}
          """.format(NOFREQ, limit))):
        yield ent(r)
                                                                # }}}1

if __name__ == "__main__":
  if "--doctest" in sys.argv:
    verbose = "--verbose" in sys.argv
    import doctest
    if doctest.testmod(verbose = verbose)[0]: sys.exit(1)

# vim: set tw=70 sw=2 sts=2 et fdm=marker :
