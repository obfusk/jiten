#!/usr/bin/python3
# encoding: utf-8

# --                                                            ; {{{1
#
# File        : jiten/version.py
# Maintainer  : Felix C. Stegerman <flx@obfusk.net>
# Date        : 2020-10-17
#
# Copyright   : Copyright (C) 2020  Felix C. Stegerman
# Version     : v0.3.4
# License     : AGPLv3+
#
# --                                                            ; }}}1

import os.path as _pth, subprocess as _subp

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
  __version__ = "0.3.4"

# vim: set tw=70 sw=2 sts=2 et fdm=marker :
