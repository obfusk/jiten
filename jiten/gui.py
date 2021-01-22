#!/usr/bin/python3
# encoding: utf-8

# --                                                            ; {{{1
#
# File        : jiten/gui.py
# Maintainer  : Felix C. Stegerman <flx@obfusk.net>
# Date        : 2021-01-22
#
# Copyright   : Copyright (C) 2021  Felix C. Stegerman
# Version     : v0.3.5
# License     : AGPLv3+
#
# --                                                            ; }}}1

                                                                # {{{1
r"""

WebView GUI.

"""                                                             # }}}1

import os, platform

from . import misc as M

title     = "Jiten Japanese Dictionary"
win_opts  = dict(width = 1280, height = 720, text_select = True)
system    = platform.system()

def start(link = None, title = title, win_opts = win_opts):
  _fix_profile()

  import webview
  os.environ["JITEN_GUI_TOKEN"] = webview.token
  from .app import app

  opts = dict(debug = bool(app.config.get("DEBUG")))
  if system == "Linux" and "PYWEBVIEW_GUI" not in os.environ:
    opts["gui"] = "qt"

  def f():
    if not link: return
    base_url = window.get_current_url().rstrip("/")
    for server in M.SERVERS:
      if link.startswith(server):
        url = link.replace(server, base_url, 1).split("#")[0]
        window.load_url(url)
        break

  window = webview.create_window(title, app, **win_opts)
  webview.start(f, **opts)

# FIXME
def _fix_profile():
  """use OTR profile"""
  gui = os.environ.get("PYWEBVIEW_GUI")
  if system == "Windows": return
  if system == "Linux" and gui and gui != "qt": return
  if system != "Linux" and gui != "qt": return
  try:
    from PyQt5.QtWidgets import QApplication
    from PyQt5.QtWebEngineWidgets import QWebEnginePage, QWebEngineProfile
  except ImportError:
    pass
  else:
    app       = _fix_profile.app      = QApplication([])
    profile   = _fix_profile.profile  = QWebEngineProfile()
    old_init  = QWebEnginePage.__init__
    def new_init(self, *a):
      if len(a) == 1: a = (profile, *a)
      old_init(self, *a)
    QWebEnginePage.__init__ = new_init

# vim: set tw=70 sw=2 sts=2 et fdm=marker :
