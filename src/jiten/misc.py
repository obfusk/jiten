#!/usr/bin/python3
# encoding: utf-8

# --                                                            ; {{{1
#
# File        : jiten/misc.py
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

import itertools

flatten = itertools.chain.from_iterable

def uniq(xs):
  seen = set()
  for x in xs:
    if x not in seen:
      seen.add(x); yield x

# vim: set tw=70 sw=2 sts=2 et fdm=marker :
