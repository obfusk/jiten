#!/usr/bin/python3
# encoding: utf-8

# --                                                            ; {{{1
#
# File        : jiten/sql.py
# Maintainer  : Felix C. Stegerman <flx@obfusk.net>
# Date        : 2020-07-15
#
# Copyright   : Copyright (C) 2020  Felix C. Stegerman
# Version     : v0.1.1
# License     : AGPLv3+
#
# --                                                            ; }}}1

                                                                # {{{1
r"""

SQL helper functions.

"""                                                             # }}}1

import importlib, sqlite3

from contextlib import contextmanager

from . import misc as M

@contextmanager
def sqlite_do(file):
  conn = sqlite3.connect(file)
  conn.row_factory = sqlite3.Row
  try:
    yield conn.cursor()
    conn.commit()
  except sqlite3.OperationalError as e:
    if not str(e).startswith("[REGEXP] "): raise e
    raise M.RegexError(str(e)[9:])
  finally:
    conn.close()

def load_pcre_extension(conn):
  spec = importlib.util.find_spec("jiten._sqlite3_pcre")
  if spec is None: raise RuntimeError("jiten._sqlite3_pcre not found")
  conn.enable_load_extension(True)
  conn.load_extension(spec.origin)
  conn.enable_load_extension(False)

# vim: set tw=70 sw=2 sts=2 et fdm=marker :
