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
# License     : GPLv3+
#
# --                                                            ; }}}1

                                                                # {{{1
r"""

...

"""                                                             # }}}1

import re, sqlite3

from contextlib import contextmanager

def _regexp(p, s):
  return re.search(p, s) is not None

@contextmanager
def sqlite_do(file):
  conn = sqlite3.connect(file)
  conn.create_function("regexp", 2, _regexp)
  c = conn.cursor()
  yield c
  conn.commit()
  conn.close()

# vim: set tw=70 sw=2 sts=2 et fdm=marker :
