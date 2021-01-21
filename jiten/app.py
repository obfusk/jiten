#!/usr/bin/python3
# encoding: utf-8

# --                                                            ; {{{1
#
# File        : jiten/app.py
# Maintainer  : Felix C. Stegerman <flx@obfusk.net>
# Date        : 2021-01-21
#
# Copyright   : Copyright (C) 2021  Felix C. Stegerman
# Version     : v0.3.5
# License     : AGPLv3+
#
# --                                                            ; }}}1

                                                                # {{{1
r"""

Web interface.

"""                                                             # }}}1

import json, os, time

from pathlib import Path

import click, jinja2, werkzeug

from flask import Flask, abort, escape, make_response, redirect, \
                  request, render_template, url_for

from .version import __version__, py_version
from .kana import kana2romaji

from . import jmdict    as J
from . import kanji     as K
from . import misc      as M
from . import pitch     as P
from . import sentences as S

START         = int(time.time())
MAX           = 50
NAME          = "jiten"
HTTPS         = NAME.upper() + "_HTTPS"
DOMAIN        = NAME.upper() + "_DOMAIN"
PREFS         = "lang dark roma nor2h max".split()

GUI_TOKEN     = os.environ.get("JITEN_GUI_TOKEN") or None
ANDROID_PRIV  = os.environ.get("ANDROID_PRIVATE") or None

app           = Flask(__name__)

if GUI_TOKEN:
  CONF_PATH   = Path.home() / ".config" / "jiten"             #  FIXME
  CONF_PREFS  = str(CONF_PATH / "prefs.json")
  CONF_HIST   = str(CONF_PATH / "history.json")
  CONF_PATH.mkdir(parents = True, exist_ok = True)
elif ANDROID_PRIV:
  CONF_PREFS  = os.path.join(ANDROID_PRIV, "jiten-prefs.json")
else:
  CONF_PREFS  = None

if CONF_PREFS:
  def get_prefs():
    try:
      with open(CONF_PREFS) as f: return json.load(f)
    except (OSError, ValueError):
      return {}
  def set_prefs(d, resp):
    p = { **get_prefs(), **d }
    with open(CONF_PREFS, "w") as f:
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
  dark        = prefs.get("dark") == "yes"
  roma        = prefs.get("roma") == "yes"
  nor2h       = prefs.get("nor2h") == "yes"
  pref_langs  = prefs.get("lang", "").split() or [J.LANGS[0]]
  pref_max    = int(prefs.get("max", MAX))
  return make_response(render_template(
    template, mode = "dark" if dark else "light", langs = langs,
    roma = roma, nor2h = nor2h, pref_langs = pref_langs,
    pref_max = pref_max, int = int, ord = ord, hex = hex,
    J = J, K = K, M = M, P = P, S = S, START = START,
    VERSION = __version__, PY_VERSION = py_version,
    kana2romaji = kana2romaji, SEARCH = SEARCH,
    GUI = bool(GUI_TOKEN), **data
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

def get_filters():
  jlpt = "-".join(filter(None, request.args.getlist("jlpt"))) or None
  if jlpt: jlpt = M.JLPT_LEVEL.convert(jlpt)
  return dict(noun = arg_bool("noun"), verb = arg_bool("verb"),
              prio = arg_bool("prio"), jlpt = jlpt)

@app.errorhandler(M.RegexError)
def handle_regexerror(e):
  return respond("error.html", name = "Regex Error", info = str(e)), 400

@app.errorhandler(click.exceptions.BadParameter)
def handle_paramerror(e):
  return respond("error.html", name = "Param Error", info = str(e)), 400

@app.errorhandler(werkzeug.exceptions.HTTPException)
def handle_httperror(e):
  return respond("error.html", name = e.name, info = e.description), e.code

def check_token(f):
  def g(*a, **k):
    token = GUI_TOKEN or app.config.get("WEBVIEW_TOKEN")
    if token and token != request.form.get("token"): abort(403)
    return f(*a, **k)
  return g

@app.route("/")
def r_index():
  if not app.config.get("DBS_UP2DATE", True):
    return respond("download_dbs.html")
  return respond("index.html", page = "index")

@app.route("/jmdict")
def r_jmdict():
  filters = get_filters()
  if arg("query", "").strip().lower() == "+random":
    q = "+#{}".format(J.random_seq(**filters))
    return redirect(url_for("r_jmdict", query = q, lang = get_langs()))
  query, max_r = get_query_max()
  opts = dict(langs = get_langs(), max_results = max_r, **filters)
  data = dict(page = "jmdict", query = query)
  if query: data["results"] = J.search(query, **opts)
  with K.readmeans() as f:
    return respond("jmdict.html", krm = f, **data)

@app.route("/jmdict/by-freq")
def r_jmdict_by_freq():
  offset  = arg("offset", 0, type = int)
  results = list(J.by_freq(offset, 1000))
  return respond("jmdict-by-freq.html", page = "jmdict/by-freq",
                 offset = offset, results = results)

@app.route("/jmdict/by-jlpt/1")
@app.route("/jmdict/by-jlpt/2")
@app.route("/jmdict/by-jlpt/3")
@app.route("/jmdict/by-jlpt/4")
@app.route("/jmdict/by-jlpt/5")
def r_jmdict_by_jlpt():
  n       = int(request.path.split("/")[-1])
  offset  = arg("offset", 0, type = int)
  results = list(J.by_jlpt(n, offset, 1000))
  return respond("jmdict-by-jlpt.html", page = request.path[1:],
                 level = n, offset = offset, results = results)

# FIXME: legacy route
@app.route("/jmdict/random")
def r_jmdict_random():
  return redirect(url_for("r_jmdict", query = "+random"))

@app.route("/kanji")
def r_kanji():
  if arg("query", "").strip().lower() == "+random":
    return redirect(url_for("r_kanji", query = K.random().char))
  query, max_r = get_query_max()
  data = dict(page = "kanji", query = query)
  if query: data["results"] = K.search(query, max_results = max_r)
  return respond("kanji.html", **data)

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
    name  = "Download Error"
    info  = "{} (file: {}, url: {})".format(str(e), e.file, e.url)
    return respond("error.html", name = name, info = info), 500
  del app.config["DBS_UP2DATE"], app.config["DOWNLOAD_DBS"]
  return redirect(url_for("r_index"))

@app.route("/_save_prefs", methods = ["POST"])
@check_token
def r_save_prefs():
  return set_prefs(dict(
    lang  = " ".join( l for l in request.form.getlist("lang")
                        if l in J.LANGS ),
    dark  = yesno(request.form.get("dark") == "yes"),
    roma  = yesno(request.form.get("roma") == "yes"),
    nor2h = yesno(request.form.get("nor2h") == "yes"),
    max   = str(request.form.get("max", MAX, type = int)),
  ), redirect(request.form.get("url", url_for("r_index"))))

if GUI_TOKEN:
  @app.route("/__load_history__/" + GUI_TOKEN, methods = ["POST"])
  def r_load_history():
    try:
      with open(CONF_HIST) as f: return f.read()
    except OSError:
      return ""
  @app.route("/__save_history__/" + GUI_TOKEN, methods = ["POST"])
  def r_save_history():
    with open(CONF_HIST, "wb") as f: f.write(request.data)
    return "" # FIXME

SEARCH = (
  ("jmdict"   , "Search JMDict"   ),
  ("kanji"    , "Search Kanji"    ),
  ("sentences", "Search Sentences"),
  ("stroke"   , "筆順を示す"      ),
)

# vim: set tw=70 sw=2 sts=2 et fdm=marker :
