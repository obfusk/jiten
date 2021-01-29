#!/usr/bin/python3
# encoding: utf-8

# --                                                            ; {{{1
#
# File        : android/main.py
# Maintainer  : Felix C. Stegerman <flx@obfusk.net>
# Date        : 2021-01-29
#
# Copyright   : Copyright (C) 2021  Felix C. Stegerman
# Version     : v0.4.0
# License     : AGPLv3+
#
# --                                                            ; }}}1

import os, secrets, sys

from jiten.misc import SERVERS, resource_path

HOST, PORT    = "127.0.0.1", 29483
LOCAL         = "http://{}:{}".format(HOST, PORT)
ANDROID       = "ANDROID_APP_PATH" in os.environ
RUNNING, URL  = False, None   # mutable state

# FIXME: workaround for bug in older versions of p4a
def fix_stdio():                                                # {{{1
  if isinstance(getattr(sys.stdout, "buffer", None), str):
    print("*** Fixing stdout/stderr ***")
    import androidembed
    class LogFile:
      def __init__(self):
        self.__buf = ""
      def write(self, s):
        s = self.__buf + s
        lines = s.split("\n")
        for l in lines[:-1]:
          androidembed.log(l)
        self.__buf = lines[-1]
      def flush(self):
        return
    sys.stdout = sys.stderr = LogFile()
                                                                # }}}1

# FIXME: workaround for webview bug
# https://github.com/obfusk/jiten/issues/41
def fix_fonts():                                                # {{{1
  from os.path import exists
  from pathlib import Path

  def get_font(ttc, name):
    for f in ttc.fonts:
      for n in f["name"].names:
        if name in n.string: return f
    return None

  c1 = "/system/fonts/NotoSansCJK-Regular.ttc"
  c2 = "/system/fonts/NotoSerifCJK-Regular.ttc"
  fd = resource_path("static/font/noto")
  f1 = resource_path("static/font/noto/NotoSansJP-Regular.otf")
  f2 = resource_path("static/font/noto/NotoSerifJP-Regular.otf")
  fc = ((f1, c1, b"Sans CJK JP"), (f2, c2, b"Serif CJK JP"))

  try:
    from fontTools.ttLib import TTCollection
    for f, c, n in fc:
      if not exists(f) and exists(c):
        Path(fd).mkdir(parents = True, exist_ok = True)
        if ttf := get_font(TTCollection(c), n):
          print("*** saving {} ***".format(f))
          ttf.save(f)
  except Exception as e:
    print("*** ERROR in fix_fonts ***\n  ", str(e))
                                                                # }}}1

def debug_mode(act):
  priv = os.environ["ANDROID_PRIVATE"]
  info = act.getApplicationInfo()
  return info.flags & type(info).FLAG_DEBUGGABLE and \
    os.path.exists(os.path.join(priv, "__debug__"))

def setup_flask(dbg):
  global app, request
  if dbg: os.environ["FLASK_ENV"] = "development"
  from jiten.app import app, request
  token = app.config["WEBVIEW_TOKEN"] = secrets.token_hex()
  return token

def setup_debug_mode():
  token = secrets.token_hex()
  print("*** DEBUG MODE ***\n * token:", token)

  @app.route("/__debug__/" + token)
  def r_debug(): raise RuntimeError

def setup_activities(act, dbg, token):
  @app.before_first_request
  def before_first_request():
    global RUNNING
    RUNNING = True
    act.loadUrl("{}#webview_token={}".format(URL or LOCAL, token))

  def on_new_intent(intent):
    global URL
    if (data := intent.getData()) and (url := data.toString()):
      if dbg: print("*** on_new_intent ***\n * url:", url)
      for server in SERVERS:
        if url.startswith(server):
          url = url.replace(server, LOCAL, 1).split("#")[0]
          if RUNNING:
            act.loadUrl(url)
          else:
            URL = url
          break

  android.activity.bind(on_new_intent = on_new_intent)
  if intent := act.getIntent(): on_new_intent(intent)

def setup_clipboard(act, token):
  CD    = jnius.autoclass("android.content.ClipData")
  ctx   = act.getApplicationContext()
  clp   = ctx.getSystemService(type(ctx).CLIPBOARD_SERVICE)

  @app.route("/__copy_to_clipboard__/" + token, methods = ["POST"])
  def r_copy_to_clipboard():
    clp.setPrimaryClip(CD.newPlainText("text", request.data))
    return "" # FIXME

def setup_webview(cls):
  cls.enableZoom()
  cls.mOpenExternalLinksInBrowser = True

if __name__ == "__main__":
  if ANDROID:
    fix_stdio()
    fix_fonts()
    import android.activity, android.config, certifi, jnius
    from android.runnable import run_on_ui_thread
    setup_clipboard = run_on_ui_thread(setup_clipboard)
    os.environ["SSL_CERT_FILE"] = certifi.where()
    cls   = jnius.autoclass(android.config.ACTIVITY_CLASS_NAME)
    act   = cls.mActivity
    dbg   = debug_mode(act)
    token = setup_flask(dbg)
    if dbg: setup_debug_mode()
    setup_clipboard(act, token)
    setup_activities(act, dbg, token)
    setup_webview(cls)

  from jiten.cli import serve_app
  serve_app(host = HOST, port = PORT, use_reloader = False)

# vim: set tw=70 sw=2 sts=2 et fdm=marker :
