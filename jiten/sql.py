#!/usr/bin/python3
# encoding: utf-8

# --                                                            ; {{{1
#
# File        : jiten/sql.py
# Maintainer  : Felix C. Stegerman <flx@obfusk.net>
# Date        : 2020-06-15
#
# Copyright   : Copyright (C) 2020  Felix C. Stegerman
# Version     : v0.0.1
# License     : AGPLv3+
#
# --                                                            ; }}}1

                                                                # {{{1
r"""

...

"""                                                             # }}}1

import hashlib, sqlite3, threading

from contextlib import contextmanager

MEMDBS  = {}
LOCK    = threading.Lock()

@contextmanager
def sqlite_do(file, memcached = False):
  conn = sqlite3.connect(file) if not memcached else sqlite_memcached(file)
  conn.row_factory = sqlite3.Row
  yield conn.cursor()
  conn.commit()
  if not memcached: conn.close()

# NB: Python >= 3.7
def sqlite_memcached(file):
  print("tid", threading.get_ident())
  with LOCK:
    tid = threading.get_ident()
    sha = hashlib.sha1(file.encode()).hexdigest()
    uri = ":memory:" # "file:{}?mode=memory&cache=shared".format(sha)
    if sha in MEMDBS:
      # if not tid in MEMDBS[sha]:
      #   MEMDBS[sha][tid] = sqlite3.connect(uri)
      # return MEMDBS[sha][tid]
      print("found.")
      return MEMDBS[sha]
    dst = sqlite3.connect(uri)
    src = sqlite3.connect(file)
    src.backup(dst)
    src.close()
    # MEMDBS[sha] = dict(tid = dst)
    MEMDBS[sha] = dst
    return dst

# vim: set tw=70 sw=2 sts=2 et fdm=marker :
