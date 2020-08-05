#!/usr/bin/python3
# encoding: utf-8

# --                                                            ; {{{1
#
# File        : jiten/pitch.py
# Maintainer  : Felix C. Stegerman <flx@obfusk.net>
# Date        : 2020-08-05
#
# Copyright   : Copyright (C) 2020  Felix C. Stegerman
# Version     : v0.2.0
# License     : AGPLv3+
#
# --                                                            ; }}}1

                                                                # {{{1
r"""

Pitch Accent from Wadoku.

>>> pitch = parse_pitch()
>>> len(pitch)
141798

>>> [ x for x in pitch if x[0] == "小猫" ][0]
['小猫', 'こねこ', '2']
>>> with_accent("こねこ", 2)
'こꜛねꜜこ'

>>> [ x for x in pitch if x[0] == "端" and x[1] == "はし" ][0]
['端', 'はし', '0']
>>> [ x for x in pitch if x[0] == "箸" and x[1] == "はし" ][0]
['箸', 'はし', '1']
>>> [ x for x in pitch if x[0] == "橋" and x[1] == "はし" ][0]
['橋', 'はし', '2']

>>> with_accent("はし", 0)
'はꜛし'
>>> with_accent("はし", 1)
'はꜜし'
>>> with_accent("はし", 2)
'はꜛしꜜ'

"""                                                             # }}}1

import re, sys

import click

from . import misc as M
from .sql import sqlite_do

SQLITE_FILE = M.resource_path("res/pitch.sqlite3")
PITCH_FILE  = M.resource_path("res/pitch/PITCH")

MORASPLIT   = re.compile(r"(.[ぁぃぅぇぉゃょゅァィゥェォャュョ]?)")

# TODO
def with_accent(text, pos):
  moras = [ x for x in re.split(MORASPLIT, text) if x ]
  if pos == 0:
    return moras[0] + "ꜛ" + "".join(moras[1:])
  elif pos == 1:
    return moras[0] + "ꜜ" + "".join(moras[1:])
  else:
    return moras[0] + "ꜛ" + "".join(moras[1:pos]) \
                    + "ꜜ" + "".join(moras[pos:])

def parse_pitch(file = PITCH_FILE):
  data = []
  with open(file) as f:
    with click.progressbar(f, width = 0, label = "reading pitch") as bar:
      for line in bar:
        data.append(line.split())
  return data

def pitch2sqldb(data, file = SQLITE_FILE):
  with sqlite_do(file) as c:
    c.executescript(PITCH_CREATE_SQL)
    with click.progressbar(data, width = 0, label = "writing pitch") as bar:
      for e in bar:
        c.execute("INSERT INTO entry VALUES (?,?,?)", e)

                                                                # {{{1
PITCH_CREATE_SQL = """
  DROP TABLE IF EXISTS entry;
  CREATE TABLE entry(
    kanji TEXT,
    reading TEXT,
    accent TEXT
  );
  CREATE INDEX idx_kanji ON entry (kanji);
"""                                                             # }}}1

def setup(file = SQLITE_FILE):
  pitch = parse_pitch()
  pitch2sqldb(pitch, file)

# TODO
def get_pitch(reading, kanjis, file = SQLITE_FILE):
  rd = reading.replace("・", "")
  with sqlite_do(file) as c:
    for k in ( k.replace("・", "") for k in kanjis ):
      for r in c.execute("SELECT * FROM entry WHERE kanji = ?", (k,)):
        if r["reading"].replace("—", "") != rd: continue
        ra = zip(r["reading"].split("—"), r["accent"].split("—"))
        return "".join( with_accent(r, int(a)) for r, a in ra )
  return None

if __name__ == "__main__":
  if "--doctest" in sys.argv:
    verbose = "--verbose" in sys.argv
    import doctest
    if doctest.testmod(verbose = verbose)[0]: sys.exit(1)

# vim: set tw=70 sw=2 sts=2 et fdm=marker :
