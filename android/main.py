#!/usr/bin/python3
# encoding: utf-8

# --                                                            ; {{{1
#
# File        : android/main.py
# Maintainer  : Felix C. Stegerman <flx@obfusk.net>
# Date        : 2020-12-02
#
# Copyright   : Copyright (C) 2020  Felix C. Stegerman
# Version     : v0.3.5
# License     : AGPLv3+
#
# --                                                            ; }}}1

import os, secrets, sys

from jiten.misc import SERVER

HOST, PORT    = "127.0.0.1", 29483
LOCAL         = "http://{}:{}".format(HOST, PORT)
ANDROID       = "ANDROID_APP_PATH" in os.environ
RUNNING, URL  = False, None

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

def debug_mode(act):
  priv = os.environ["ANDROID_PRIVATE"]
  info = act.getApplicationInfo()
  return info.flags & type(info).FLAG_DEBUGGABLE and \
    os.path.exists(os.path.join(priv, "__debug__"))

def setup_flask(dbg):
  global app
  if dbg: os.environ["FLASK_ENV"] = "development"
  from jiten.app import app

def setup_debug_mode():
  token = secrets.token_hex()
  print("*** DEBUG MODE ***\n * token:", token)
  @app.route("/__debug__/" + token)
  def r_debug(): raise RuntimeError

def setup_activities(act):
  @app.before_first_request
  def before_first_request():
    global RUNNING
    RUNNING = True
    if URL: act.loadUrl(URL)
  def on_new_intent(intent):
    global URL
    if data := intent.getData():
      if (url := data.toString()).startswith(SERVER):
        url = url.replace(SERVER, LOCAL, 1)
        if RUNNING:
          act.loadUrl(url)
        else:
          URL = url
  android.activity.bind(on_new_intent = on_new_intent)
  if intent := act.getIntent(): on_new_intent(intent)

if __name__ == "__main__":
  if ANDROID:
    fix_stdio()
    import android.activity, android.config, certifi, jnius
    os.environ["SSL_CERT_FILE"] = certifi.where()
    act = jnius.autoclass(android.config.ACTIVITY_CLASS_NAME).mActivity
    dbg = debug_mode(act)
    setup_flask(dbg)
    if dbg: setup_debug_mode()
    setup_activities(act)
  from jiten.cli import serve_app
  serve_app(host = HOST, port = PORT, use_reloader = False)

# vim: set tw=70 sw=2 sts=2 et fdm=marker :
