#!/usr/bin/python3
# encoding: utf-8

# --                                                            ; {{{1
#
# File        : jiten/sql.py
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

SQL helper functions.

"""                                                             # }}}1

import sqlite3

from contextlib import contextmanager

@contextmanager
def sqlite_do(file):
  conn = sqlite3.connect(file)
  conn.row_factory = sqlite3.Row
  yield conn.cursor()
  conn.commit()
  conn.close()

# vim: set tw=70 sw=2 sts=2 et fdm=marker :
