#!/usr/bin/python3
# encoding: utf-8

# --                                                            ; {{{1
#
# File        : jiten/misc.py
# Maintainer  : Felix C. Stegerman <flx@obfusk.net>
# Date        : 2020-12-02
#
# Copyright   : Copyright (C) 2020  Felix C. Stegerman
# Version     : v0.3.5
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
>>> q2like(r"\bfoo\b")
'%foo%'
>>> q2like(r"^foo*bar?baz$")
'%fo%ba%baz%'
>>> q2like(r"\\") is None
True

"""                                                             # }}}1

import hashlib, itertools, re, os, sys, urllib.request

import click

class RegexError(RuntimeError): pass

class DownloadError(RuntimeError):
  def __init__(self, msg, file, url):
    super().__init__(msg)
    self.file, self.url = file, url

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

# FIXME: return False for ""?!
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

def process_query(q, word, exact, fstwd, cli = False):
  if not q: return ""
  q = q.strip()
  if not cli and (word or exact or fstwd): q = without_e1w(q)
  if q.startswith("+~"): return q[2:].lstrip()
  if not q.startswith("+"):
    if exact: return "+= " + q
    if fstwd: return "+1 " + q
    if word : return "+w " + q
  return q

def without_e1w(q):
  return q[2:].lstrip() if any( q.startswith("+"+x) for x in "=1w" ) else q

LIKERX = re.compile("(?P<one>" + "|".join([
  r"\.", r"\[\^?\]?[^]]*\]", r"\\[dDsSwW]", r"\\p[khK]",
  r"\\[pP]\{\w+\}"
]) + r")" + "|".join([
  r"(?P<many>([*+?]|\{\d+(,\d*)?\})?)", r"(?P<zero>\\b)",
  r"[^^$*+?{}\\|()](?P<quant>([*+?]|\{\d+(,\d*)?\})?)"
]))

# TODO
def q2like(q):                                                  # {{{1
  f = lambda c: "_" if c in "%_" or (not isascii(c)
                       and c.upper() != c.lower()) else c
  q, p = without_e1w(q), ""
  if q.startswith("^"): q = q[1:]
  if q.endswith("$"): q = q[:-1]
  while q:
    m = LIKERX.match(q)
    if not m: return None
    if not m.group("zero"):
      if m.group("many") or m.group("quant"): p += "%"
      else: p += "_" if m.group("one") else f(m.group(0))
    q = q[m.end():]
  return re.sub(r"%%+", "%", "%" + p + "%")
                                                                # }}}1

def q2rx(q):
  if   q.startswith("+="): q = "^"   + q[2:].lstrip() +   "$"
  elif q.startswith("+1"): q = "^"   + q[2:].lstrip() + "\\b"
  elif q.startswith("+w"): q = "\\b" + q[2:].lstrip() + "\\b"
  return "(?im)" + q.replace(r"\pk", r"\p{Katakana}") \
                    .replace(r"\ph", r"\p{Hiragana}") \
                    .replace(r"\pK", r"\p{Han}")                # TODO

def download_file(url, file, sha512 = None, tmp = ".tmp"):      # {{{1
  label = "downloading " + os.path.basename(file)
  sha   = hashlib.sha512()
  with open(file + tmp, "wb") as fo:
    try:
      with urllib.request.urlopen(url) as fi:
        chunks = iter((lambda: fi.read(1024)), b'')
        with click.progressbar(chunks, width = 0, label = label) as bar:
          for chunk in bar:
            fo.write(chunk)
            sha.update(chunk)
    except urllib.error.URLError as e:
      os.remove(file + tmp)
      raise DownloadError(str(e), file, url)
  if sha512 is not None and sha.hexdigest() != sha512:
    os.remove(file + tmp)
    raise DownloadError("sha512 did not match: expected {}, got {}"
                        .format(sha512, sha.hexdigest()), file, url)
  os.replace(file + tmp, file)
  return sha.hexdigest()
                                                                # }}}1

J_O_D     = "https://jiten.obfusk.dev"
SERVERS   = os.environ.get("JITEN_SERVERS", "").split() or [J_O_D]
SERVER    = SERVERS[0]

DB_URLFMT = "https://github.com/obfusk/jiten/releases/download/{}/{}.sqlite3"
DB_URLS   = {
  8: { k: DB_URLFMT.format("v0.3.5", k)
       for k in "jmdict kanji pitch sentences".split() }
}

DB_SHA512SUMS = {
  8: dict(
    jmdict    = "c94830335a9176001fbc4400a4176a135b475e87a5f91d7fe3eccdcdc777219d7132a2ef56f99563bde7d6ed614dfd1ae8a9fed3a9ae4331159b9e675e60e9e7",
    kanji     = "f16fcca818bf9dc8a63dbcae37a1d9220db1bb5b76a006ced6ac26b6d7fc549522f9cf6620277a2b692e902224e185a7263463643715f0ff502950971f2ba9d6",
    pitch     = "8bac0a6a1cd74c901ffa5d222a336cf3b2c033ceb00a10c7f442056aae764d5110519085892777bfa4b0b8b7adfcaf3266da3ac5388bb094343e383dbc87777b",
    sentences = "5f9d1968832457f096f55b30af90311ac681dc1456fdc12f293879adba93ed5a267984b87872ef514f84b5ecaba7fe7d2f17601018ea0fccb6198059d6a8b79a",
  )
}

DEPENDENCIES = dict(                                            # {{{1
  p4a = dict(
    name  = "python-for-android",
    url   = "https://github.com/kivy/python-for-android"
  ),

  libffi        = dict(url = "https://github.com/libffi/libffi"),
  libpcre       = dict(url = "https://www.pcre.org"),
  openssl       = dict(url = "https://www.openssl.org"),
  pyjnius       = dict(url = "https://github.com/kivy/pyjnius"),
  python3       = dict(url = "https://www.python.org"),
  sqlite3       = dict(url = "https://www.sqlite.org"),

  certifi       = dict(url = "https://github.com/certifi/python-certifi"),
  click         = dict(url = "https://github.com/pallets/click"),
  flask         = dict(url = "https://github.com/pallets/flask"),
  itsdangerous  = dict(url = "https://github.com/pallets/itsdangerous"),
  jinja2        = dict(url = "https://github.com/pallets/jinja"),
  markupsafe    = dict(url = "https://github.com/pallets/markupsafe"),
  setuptools    = dict(url = "https://github.com/pypa/setuptools"),
  six           = dict(url = "https://github.com/benjaminp/six"),
  werkzeug      = dict(url = "https://github.com/pallets/werkzeug"),
)                                                               # }}}1

if __name__ == "__main__":
  if "--doctest" in sys.argv:
    verbose = "--verbose" in sys.argv
    import doctest
    if doctest.testmod(verbose = verbose)[0]: sys.exit(1)

# vim: set tw=70 sw=2 sts=2 et fdm=marker :
