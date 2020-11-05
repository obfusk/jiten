#!/usr/bin/python3
# encoding: utf-8

# --                                                            ; {{{1
#
# File        : jiten/app.py
# Maintainer  : Felix C. Stegerman <flx@obfusk.net>
# Date        : 2020-11-05
#
# Copyright   : Copyright (C) 2020  Felix C. Stegerman
# Version     : v0.3.5
# License     : AGPLv3+
#
# --                                                            ; }}}1

                                                                # {{{1
r"""

Web interface.

"""                                                             # }}}1

import json, os, time

import jinja2

from flask import Flask, escape, make_response, redirect, request, \
                  render_template, url_for

from .version import __version__, py_version
from .kana import kana2romaji

from . import jmdict    as J
from . import kanji     as K
from . import misc      as M
from . import sentences as S

START   = int(time.time())
MAX     = 50
name    = "jiten"
HTTPS   = name.upper() + "_HTTPS"
DOMAIN  = name.upper() + "_DOMAIN"
PREFS   = "lang dark roma max".split()
app     = Flask(__name__)

if "ANDROID_PRIVATE" in os.environ:
  CONF = os.path.join(os.environ["ANDROID_PRIVATE"], "jiten-prefs.json")
  def get_prefs():
    try:
      with open(CONF) as f: return json.load(f)
    except (OSError, ValueError):
      return {}
  def set_prefs(d, resp):
    p = { **get_prefs(), **d }
    with open(CONF, "w") as f:
      json.dump(p, f, indent = 2, sort_keys = True)
      f.write("\n")
    return resp
else:
  def get_prefs():
    return { k: request.cookies[k] for k in PREFS
             if k in request.cookies }
  def set_prefs(d, resp):
    for k, v in d.items():
      resp.set_cookie(k, v, max_age = 3600*24*365*10)
    return resp

if os.environ.get(HTTPS) == "force":
  @app.before_request
  def https_required():
    if request.scheme != "https":
      return redirect(request.url.replace("http:", "https:", 1), code = 301)
  @app.after_request
  def after_request_func(response):
    response.headers["Strict-Transport-Security"] = 'max-age=63072000'
    return response

if os.environ.get(DOMAIN):
  domain = os.environ.get(DOMAIN)
  @app.before_request
  def redirect_domain():
    if request.host != domain:
      return redirect(request.url.replace(request.host, domain, 1), code = 301)

def arg(k, *a, **kw):
  return request.args.get(k, *a, **kw)

def arg_bool(k, *a, **kw):
  return arg(k, *a, **kw) == "yes"

def yesno(b):
  return "yes" if b else "no"

def respond(template, **data):
  prefs       = get_prefs()
  langs       = get_langs(prefs)
  dark, roma  = prefs.get("dark") == "yes", prefs.get("roma") == "yes"
  pref_langs  = prefs.get("lang", "").split() or [J.LANGS[0]]
  pref_max    = int(prefs.get("max", MAX))
  return make_response(render_template(
    template, mode = "dark" if dark else "light", langs = langs,
    roma = roma, pref_langs = pref_langs, pref_max = pref_max,
    ord = ord, hex = hex, J = J, K = K, M = M, S = S, START = START,
    VERSION = __version__, PY_VERSION = py_version,
    kana2romaji = kana2romaji, DEPS = DEPENDENCIES, **data
  ))

def get_langs(prefs = None):
  if prefs is None: prefs = get_prefs()
  ls = request.args.getlist("lang") or prefs.get("lang", "").split()
  return [ l for l in ls if l in J.LANGS ] or [J.LANGS[0]]

def get_sentence_langs():
  ls = request.args.getlist("lang")
  return [ l for l in ls if l in S.LANGS ]

def get_query_max():
  w, e, f = arg_bool("word"), arg_bool("exact"), arg_bool("1stword")
  return M.process_query(arg("query"), w, e, f), get_max()

# TODO
def get_max():
  return int(arg("max", get_prefs().get("max", MAX), type = int))

def get_nvp():
  return dict(noun = arg_bool("noun"), verb = arg_bool("verb"),
              prio = arg_bool("prio"))

@app.route("/")
def r_index():
  if not app.config.get("DBS_UP2DATE", True):
    return respond("download_dbs.html")
  return respond("index.html", page = "index")

# TODO
# * --max
@app.route("/jmdict")
def r_jmdict():
  if arg("query", "").strip().lower() == "+random":
    q = "+#{}".format(J.random_seq(**get_nvp()))
    return redirect(url_for("r_jmdict", query = q))
  query, max_r = get_query_max()
  opts = dict(langs = get_langs(), max_results = max_r, **get_nvp())
  data = dict(page = "jmdict", query = query)
  try:
    if query: data["results"] = J.search(query, **opts)
    with K.readmeans() as f:
      return respond("jmdict.html", krm = f, **data)
  except M.RegexError as e:
    return "regex error: " + escape(str(e)), 400

@app.route("/jmdict/by-freq")
def r_jmdict_by_freq():
  offset  = arg("offset", 0, type = int)
  results = list(J.by_freq(offset, 1000))
  return respond("jmdict-by-freq.html", page = "jmdict/by-freq",
                 offset = offset, results = results)

# FIXME: legacy route
@app.route("/jmdict/random")
def r_jmdict_random():
  return redirect(url_for("r_jmdict", query = "+random"))

# TODO
# * --max
@app.route("/kanji")
def r_kanji():
  if arg("query", "").strip().lower() == "+random":
    return redirect(url_for("r_kanji", query = K.random().char))
  query, max_r = get_query_max()
  data = dict(page = "kanji", query = query)
  try:
    if query: data["results"] = K.search(query, max_results = max_r)
    return respond("kanji.html", **data)
  except M.RegexError as e:
    return "regex error: " + escape(str(e)), 400

@app.route("/kanji/by-freq")
def r_kanji_by_freq():
  return respond("kanji-by-freq.html", page = "kanji/by-freq",
                 kanji = K.by_freq())

@app.route("/kanji/by-level")
def r_kanji_by_level():
  levels = [ (l, list(K.by_level(l))) for l in K.LEVELS ]
  return respond("kanji-by-level.html", page = "kanji/by-level",
                 levels = levels)

@app.route("/kanji/by-jlpt")
def r_kanji_by_jlpt():
  return respond("kanji-by-jlpt.html", page = "kanji/by-jlpt")

# FIXME: legacy route
@app.route("/kanji/random")
def r_kanji_random():
  return redirect(url_for("r_kanji", query = "+random"))

# TODO: langs
@app.route("/sentences")
def r_sentences():
  query, max_r = arg("query", "").strip(), get_max()
  opts = dict(langs = get_sentence_langs(), max_results = max_r,
              audio = arg_bool("audio"))
  data = dict(page = "sentences", query = query)
  if query: data["results"] = S.search(query, **opts)
  with K.readmeans() as f:
    return respond("sentences.html", krm = f, **data)

@app.route("/stroke")
def r_stroke():
  return respond("stroke.html", page = "stroke",
                 query = arg("query", "").strip())

@app.route("/_db/v<int:db_version>/<base>")
def r_db(db_version, base):
  return redirect(M.DB_URLS[db_version][base])

@app.route("/_download_dbs", methods = ["POST"])
def r_download_dbs():
  if app.config.get("DBS_UP2DATE", True):
    return "dbs up2date", 400
  try:
    app.config["DOWNLOAD_DBS"]()
  except M.DownloadError as e:
    return "download error: {} (file: {}, url: {})" \
           .format(escape(str(e)), e.file, e.url), 500
  del app.config["DBS_UP2DATE"], app.config["DOWNLOAD_DBS"]
  return redirect(url_for("r_index"))

@app.route("/_save_prefs", methods = ["POST"])
def r_save_prefs():
  return set_prefs(dict(
    lang  = " ".join( l for l in request.form.getlist("lang")
                        if l in J.LANGS ),
    dark  = yesno(request.form.get("dark") == "yes"),
    roma  = yesno(request.form.get("roma") == "yes"),
    max   = str(request.form.get("max", MAX, type = int)),
  ), redirect(request.form.get("url", url_for("r_index"))))

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

  click         = dict(url = "https://github.com/pallets/click"),
  flask         = dict(url = "https://github.com/pallets/flask"),
  itsdangerous  = dict(url = "https://github.com/pallets/itsdangerous"),
  jinja2        = dict(url = "https://github.com/pallets/jinja"),
  markupsafe    = dict(url = "https://github.com/pallets/markupsafe"),
  setuptools    = dict(url = "https://github.com/pypa/setuptools"),
  six           = dict(url = "https://github.com/benjaminp/six"),
  werkzeug      = dict(url = "https://github.com/pallets/werkzeug"),
)                                                               # }}}1

# vim: set tw=70 sw=2 sts=2 et fdm=marker :
