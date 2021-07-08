#!/usr/bin/python3
# encoding: utf-8

# --                                                            ; {{{1
#
# File        : jiten/sentences.py
# Maintainer  : Felix C. Stegerman <flx@obfusk.net>
# Date        : 2021-07-05
#
# Copyright   : Copyright (C) 2021  Felix C. Stegerman
# Version     : v1.0.2
# License     : AGPLv3+
#
# --                                                            ; }}}1

                                                                # {{{1
r"""

Sentences from Tatoeba.

>>> from contextlib import contextmanager
>>> @contextmanager
... def _progressbar(it, **kw): yield it
>>> click.progressbar = _progressbar

>>> sentences = parse_sentences()
>>> len(sentences)
207995

>>> len([ x for x in sentences if x.jap ])
207995
>>> len([ x for x in sentences if x.eng ])
203308
>>> len([ x for x in sentences if x.dut ])
4860
>>> len([ x for x in sentences if x.ger ])
43208
>>> len([ x for x in sentences if x.fre ])
37491
>>> len([ x for x in sentences if x.spa ])
32690
>>> len([ x for x in sentences if x.swe ])
939
>>> len([ x for x in sentences if x.audio ])
1281
>>> len([ x for x in sentences if x.eng and x.dut and x.ger ])
2662
>>> len([ x for x in sentences if x.eng and x.dut and x.ger and x.audio ])
544
>>> len([ x for x in sentences if x.eng and x.dut and x.ger and x.fre and x.spa ])
810
>>> len([ x for x in sentences if x.eng and x.dut and x.ger and x.fre and x.spa and x.audio ])
205

>>> [ x for x in sentences if "子猫" in x.jap ][0]
Entry(id=74794, jap='「お前、どこの子だ？」足に纏わりついてきたのは、小さな子猫だった。灰色の縞模様のふわふわした猫だ。', eng='"Who do you belong to?" Wrapped around his feet was a small cat. It was a fluffy grey striped cat.', dut=None, ger=None, fre=None, spa=None, swe=None, audio=None)

>>> [ x for x in sentences if "猫" in x.jap and x.ger and x.audio ][0]
Entry(id=2260050, jap='最後にあの猫を見たのはいつですか？', eng='When was the last time you saw the cat?', dut=None, ger='Wann hast du die Katze zum letzten Mal gesehen?', fre=None, spa=None, swe=None, audio='Mizu (CC BY-NC 4.0)')

>>> sorted(set( x.audio for x in sentences if x.audio ))
['Mizu (CC BY-NC 4.0)', 'huizi99 (CC BY-NC 4.0)', 'yomi (CC BY-NC 4.0)']

"""                                                             # }}}1

import functools, os, re, sys

from collections import namedtuple

import click

from . import misc as M
from .sql import sqlite_do

SQLITE_FILE     = M.resource_path("res/sentences.sqlite3")
SENTENCES_FILE  = M.resource_path("res/sentences/SENTENCES")
AUDIO_DIR       = M.resource_path("static/audio")
DATA_FILES      = (SQLITE_FILE, SENTENCES_FILE)

LANGSFULL = "english dutch german french spanish swedish".split()
LANGS     = [ l[:3] for l in LANGSFULL ]
Entry     = namedtuple("Entry", "id jap".split() + LANGS + ["audio"])

def parse_sentences(file = SENTENCES_FILE):
  data = []
  with open(file) as f:
    with click.progressbar(f, width = 0, label = "reading sentences") as bar:
      for line in bar:
        id, *rest = [ None if x == "-" else x
                      for x in line.rstrip("\n").split("\t") ]
        data.append(Entry(int(id), *rest))
  return data

def sentences2sqldb(data, file = SQLITE_FILE):
  with sqlite_do(file, write = True) as c:
    c.executescript(SENTENCES_CREATE_SQL)
    with click.progressbar(data, width = 0, label = "writing sentences") as bar:
      for e in bar:
        c.execute("INSERT INTO entry VALUES (?,?,?,?,?,?,?,?,?)", e)

                                                                # {{{1
SENTENCES_CREATE_SQL = """
  DROP TABLE IF EXISTS entry;
  CREATE TABLE entry(
    id INTEGER PRIMARY KEY ASC,
    jap TEXT,
    eng TEXT,
    dut TEXT,
    ger TEXT,
    fre TEXT,
    spa TEXT,
    swe TEXT,
    audio TEXT
  );
"""                                                             # }}}1

def setup(file = SQLITE_FILE):
  sentences = parse_sentences()
  sentences2sqldb(sentences, file)

# TODO
def search(q, langs = [], max_results = None, audio = False,
           file = SQLITE_FILE):
  lang  = " ".join( "AND " + l + " IS NOT NULL"
                    for l in langs if l in LANGS )
  aud   = "AND audio IS NOT NULL" if audio else ""
  lim   = "LIMIT " + str(int(max_results)) if max_results else ""
  with sqlite_do(file) as c:
    if q.lower() == "+random":
      for r in c.execute("""
          SELECT * FROM entry WHERE 1=1 {} {} ORDER BY RANDOM() {}
          """.format(lang, aud, lim)):                        # safe!
        yield Entry(*r)
    elif re.fullmatch(r"\+#\s*\d+", q):
      id = int(q[2:].strip())
      for r in c.execute("SELECT * FROM entry WHERE id = ?", (id,)):
        yield Entry(*r) # #=1
    else:
      sel = ["jap"] + ([] if M.iscjk(q) else LANGS)
      s   = " OR ".join( x + " LIKE :q" for x in sel )
      for r in c.execute("""
          SELECT * FROM entry WHERE ({}) {} {} ORDER BY id {}
          """.format(s, lang, aud, lim), dict(q="%"+q+"%")):  # safe!
        yield Entry(*r)

@functools.lru_cache(maxsize = None)
def have_audio(id):
  return os.path.exists(os.path.join(AUDIO_DIR, "{}.mp3".format(id)))

if __name__ == "__main__":
  if "--doctest" in sys.argv:
    verbose = "--verbose" in sys.argv
    import doctest
    if doctest.testmod(verbose = verbose)[0]: sys.exit(1)

# vim: set tw=70 sw=2 sts=2 et fdm=marker :
