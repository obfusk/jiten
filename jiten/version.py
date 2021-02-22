#!/usr/bin/python3
# encoding: utf-8

# --                                                            ; {{{1
#
# File        : jiten/version.py
# Maintainer  : Felix C. Stegerman <flx@obfusk.net>
# Date        : 2021-02-20
#
# Copyright   : Copyright (C) 2021  Felix C. Stegerman
# Version     : v1.0.0
# License     : AGPLv3+
#
# --                                                            ; }}}1

import os.path as _pth, subprocess as _subp, sys

_dir = _pth.dirname(__file__)
_vsn = _pth.join(_dir, ".version")
if _pth.exists(_pth.join(_pth.dirname(_dir), ".git")):
  __version__ = _subp.check_output("git describe --always",
                  shell = True, cwd = _dir) \
                .decode().strip().replace("v", "", 1)
elif _pth.exists(_vsn):
  with open(_vsn) as f:
    __version__ = f.readline().strip().replace("v", "", 1)
else:
  __version__ = "1.0.0"

py_version = "Python " + sys.version.split()[0]
if "PyPy" in sys.version:
  py_version += ", PyPy {}".format(
    sys.version[sys.version.index("PyPy"):].split()[1]
  )

# vim: set tw=70 sw=2 sts=2 et fdm=marker :
