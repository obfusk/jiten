#!/usr/bin/python3
# encoding: utf-8

# --                                                            ; {{{1
#
# File        : android/main.py
# Maintainer  : Felix C. Stegerman <flx@obfusk.net>
# Date        : 2020-12-01
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
ANDROID_PRIV  = os.environ.get("ANDROID_PRIVATE") or None
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

def debug_mode(activ):
  info = activ.getApplicationInfo()
  return info.flags & type(info).FLAG_DEBUGGABLE and \
    os.path.exists(os.path.join(ANDROID_PRIV, "__debug__"))

def setup_flask(debug):
  global app
  if debug: os.environ["FLASK_ENV"] = "development"
  from jiten.app import app

def setup_debug_mode():
  token = secrets.token_hex()
  print("*** DEBUG MODE ***\n * token:", token)
  @app.route("/__debug__/" + token)
  def r_debug(): raise RuntimeError

def setup_activities(activ):
  @app.before_first_request
  def before_first_request():
    global RUNNING
    RUNNING = True
    if URL: activ.loadUrl(URL)
  def on_new_intent(intent):
    global URL
    if data := intent.getData():
      if (url := data.toString()).startswith(SERVER):
        url = url.replace(SERVER, LOCAL, 1)
        if RUNNING:
          activ.loadUrl(url)
        else:
          URL = url
  android.activity.bind(on_new_intent = on_new_intent)
  if intent := activ.getIntent(): on_new_intent(intent)

if __name__ == "__main__":
  fix_stdio()
  if ANDROID_PRIV:
    try:
      import android.activity, android.config, jnius
    except ImportError:
      pass
    else:
      activ = jnius.autoclass(android.config.ACTIVITY_CLASS_NAME).mActivity
      setup_flask(debug := debug_mode(activ))
      if debug: setup_debug_mode()
      setup_activities(activ)
  try:
    import certifi
  except ImportError:
    pass
  else:
    os.environ["SSL_CERT_FILE"] = certifi.where()
  from jiten.cli import serve_app
  serve_app(host = HOST, port = PORT, use_reloader = False)

# vim: set tw=70 sw=2 sts=2 et fdm=marker :
