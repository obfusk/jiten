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
# License     : AGPLv3+
#
# --                                                            ; }}}1

                                                                # {{{1
r"""

...

"""                                                             # }}}1

import itertools, sys

OKPUNC = "々"

ispunc      = lambda c:  0x3000 <= ord(c) <=  0x303f
ishiragana  = lambda c:  0x3040 <= ord(c) <=  0x309f
iskatakana  = lambda c:  0x30a0 <= ord(c) <=  0x30ff

iskanji     = lambda c:  0x4e00 <= ord(c) <=  0x9faf
iscompat    = lambda c:  0xf900 <= ord(c) <=  0xfaff
isuniext    = lambda c:  0x3400 <= ord(c) <=  0x4dbf or \
                        0x20000 <= ord(c) <= 0x2ebef

iskana      = lambda c: ishiragana(c) or iskatakana(c)
isideo      = lambda c: iskanji(c) or iscompat(c) or isuniext(c)
isjap       = lambda c: iskanji(c) or iskana(c)  # probably
isokjap     = lambda c: isjap(c) or c in OKPUNC  # probably

flatten = itertools.chain.from_iterable

def uniq(xs):
  seen = set()
  for x in xs:
    if x not in seen:
      seen.add(x); yield x

if __name__ == "__main__":
  if "--doctest" in sys.argv:
    import doctest
    if doctest.testmod(verbose = True)[0]: sys.exit(1)

# vim: set tw=70 sw=2 sts=2 et fdm=marker :
