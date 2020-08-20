#!/usr/bin/python3
# encoding: utf-8

# --                                                            ; {{{1
#
# File        : jiten/misc.py
# Maintainer  : Felix C. Stegerman <flx@obfusk.net>
# Date        : 2020-08-19
#
# Copyright   : Copyright (C) 2020  Felix C. Stegerman
# Version     : v0.3.0
# License     : AGPLv3+
#
# --                                                            ; }}}1

                                                                # {{{1
r"""

Miscellaneous helper functions.

>>> ishiragana("ふ"), ishiragana("フ")
(True, False)
>>> iskatakana("ふ"), iskatakana("フ")
(False, True)

>>> iskana("ふ"), iskana("フ")
(True, True)

>>> iskanji("猫")
True

>>> ispunc("々")
True

>>> list(flatten([[1, 2], [3, 4]]))
[1, 2, 3, 4]

>>> list(uniq([1, 2, 3, 1, 4, 2, 2]))
[1, 2, 3, 4]

>>> q2like(r"+w foo")
'%foo%'
>>> q2like(r".foo.*bar[a-z]baz")
'%_foo%bar_baz%'
>>> q2like(r"[^あいうえお]")
'%_%'
>>> q2like(r"猫\pK{2}\d\S")
'%猫%__%'
>>> q2like(r"\bfoo\b") is None
True

"""                                                             # }}}1

import itertools, re, os, sys

class RegexError(RuntimeError): pass

OKPUNC      = "々"

ispunc1     = lambda c:  0x3000 <= ord(c) <=  0x303f
ishiragana1 = lambda c:  0x3040 <= ord(c) <=  0x309f
iskatakana1 = lambda c:  0x30a0 <= ord(c) <=  0x30ff

iskanji1    = lambda c:  0x4e00 <= ord(c) <=  0x9fff
iscompat1   = lambda c:  0xf900 <= ord(c) <=  0xfaff
isuniext1   = lambda c:  0x3400 <= ord(c) <=  0x4dbf or \
                        0x20000 <= ord(c) <= 0x2ebef

isradical1  = lambda c:  0x2e80 <= ord(c) <=  0x2eff or \
                         0x2f00 <= ord(c) <=  0x2fdf

iskana1     = lambda c: ishiragana1(c) or iskatakana1(c)
isideo1     = lambda c: iskanji1(c) or iscompat1(c) or isuniext1(c)
isjap1      = lambda c: iskanji1(c) or iskana1(c)               # TODO
isokjap1    = lambda c: isjap1(c) or c in OKPUNC                # TODO
iscjk1      = lambda c: isideo1(c) or iskana1(c) or ispunc1(c)  # TODO

for _n, _f in list(locals().items()):
  if _n.startswith("is") and _n.endswith("1"):
    locals()[_n[:-1]] = (lambda f: lambda s: all(map(f, s)))(_f)
del _n, _f

isascii     = getattr(str, "isascii",
                lambda s: all( ord(c) < 128 for c in s ))

flatten     = itertools.chain.from_iterable

def uniq(xs):
  seen = set()
  for x in xs:
    if x not in seen:
      seen.add(x); yield x

# TODO: use importlib.resources?!
def resource_path(path):
  return os.path.join(os.path.dirname(__file__), *path.split("/"))

def process_query(q, word, exact, fstwd):
  if not q: return ""
  q = q.strip()
  if word or exact or fstwd: q = without_e1w(q)
  if q.startswith("+~"): return q[2:].lstrip()
  if not q.startswith("+"):
    if exact: return "+= " + q
    if fstwd: return "+1 " + q
    if word : return "+w " + q
  return q

def without_e1w(q):
  return q[2:].lstrip() if any( q.startswith("+"+x) for x in "=1w" ) else q

LIKERX = re.compile("(" + "|".join([
  r"\.", r"\[\^?\]?[^]]*\]", r"\\[dDsSwW]", r"\\p[khK]",
  r"\\[pP]\{\w+\}"
]) + r")(([+*]|\{\d+(,\d+)?\})?)|[^^$*+?{}\\|()%_]")

# TODO: ^foo, foo$, \b, ...
def q2like(q):
  f = lambda c: "_" if not isascii(c) and c.upper() != c.lower() else c
  q, p = without_e1w(q), ""
  while q:
    m = LIKERX.match(q)
    if not m: return None
    p += "%" if m.group(2) else "_" if m.group(1) else f(m.group(0))
    q = q[m.end():]
  return re.sub(r"%%+", "%", "%" + p + "%")

def q2rx(q):
  if   q.startswith("+="): q = "^"   + q[2:].lstrip() +   "$"
  elif q.startswith("+1"): q = "^"   + q[2:].lstrip() + "\\b"
  elif q.startswith("+w"): q = "\\b" + q[2:].lstrip() + "\\b"
  return "(?im)" + q.replace(r"\pk", r"\p{Katakana}") \
                    .replace(r"\ph", r"\p{Hiragana}") \
                    .replace(r"\pK", r"\p{Han}")                # TODO

if __name__ == "__main__":
  if "--doctest" in sys.argv:
    verbose = "--verbose" in sys.argv
    import doctest
    if doctest.testmod(verbose = verbose)[0]: sys.exit(1)

# vim: set tw=70 sw=2 sts=2 et fdm=marker :
