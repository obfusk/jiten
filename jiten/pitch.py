#!/usr/bin/python3
# encoding: utf-8

# --                                                            ; {{{1
#
# File        : jiten/pitch.py
# Maintainer  : Felix C. Stegerman <flx@obfusk.net>
# Date        : 2021-02-04
#
# Copyright   : Copyright (C) 2021  Felix C. Stegerman
# Version     : v0.4.0
# License     : AGPLv3+
#
# --                                                            ; }}}1

                                                                # {{{1
r"""

Pitch Accent from Wadoku.

>>> pitch = parse_pitch()
>>> len(pitch) + len(BLACKLIST)
205092

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

>>> r = [ x for x in pitch if x[0] == "以心伝心" ][0]
>>> r
['以心伝心', 'いしん—でんしん', '1']
>>> with_pitch(dict(reading = r[1], accent = r[2]))
'いꜜしん･でんしん'

>>> r = [ x for x in pitch if x[0] == "精一杯" ][0]
>>> r
['精一杯', 'せい—いっぱい', '3']
>>> with_pitch(dict(reading = r[1], accent = r[2]))
'せꜛい･いꜜっぱい'

"""                                                             # }}}1

import functools, os, re, sys

from contextlib import contextmanager

import click

from . import misc as M
from .sql import sqlite_do

SQLITE_FILE = M.resource_path("res/pitch.sqlite3")
PITCH_FILE  = M.resource_path("res/pitch/PITCH")
DATA_FILES  = (SQLITE_FILE, PITCH_FILE)

# NB: skip ･ for e.g. せꜛい･いꜜっぱい
MORASPLIT   = re.compile(r"(･?.[ぁぃぅぇぉゃょゅァィゥェォャュョ]?)")

# TODO
BLACKLIST   = """ぎっこんばっこん ぎっこんばったん ぎったんばったん
                 電子マネー対応自販機 電子マネー自販機""".split()

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
        kanji, reading, accent = row = line.split()
        if kanji in BLACKLIST: continue
        assert len(reading.split("—")) >= len(accent.split("—"))
        data.append(row)
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

@contextmanager
def pitches(file = SQLITE_FILE):
  with sqlite_do(file) as c:
    yield lambda e: e.pitch(conn = c)

# TODO
def get_pitch(reading, kanjis, conn = None, file = SQLITE_FILE):
  rd = reading.replace("・", "")
  def f(c):
    for k in ( k.replace("・", "") for k in kanjis ):
      for r in c.execute("SELECT * FROM entry WHERE kanji = ?", (k,)):
        if r["reading"].replace("—", "") != rd: continue
        return with_pitch(r)
    return None
  if have_pitch(file):
    if conn is not None:
      return f(conn)
    with sqlite_do(file) as c:
      return f(c)
  return None

def with_pitch(r):
  sr, sa  = r["reading"].split("—"), r["accent"].split("—")
  rs      = sr[:len(sa)-1] + ["･".join(sr[len(sa)-1:])]
  return "･".join( with_accent(r, int(a)) for r, a in zip(rs, sa) )

@functools.lru_cache(maxsize = None)
def have_pitch(file = SQLITE_FILE):
  return os.path.exists(file)

if __name__ == "__main__":
  if "--doctest" in sys.argv:
    verbose = "--verbose" in sys.argv
    import doctest
    if doctest.testmod(verbose = verbose)[0]: sys.exit(1)

# vim: set tw=70 sw=2 sts=2 et fdm=marker :
