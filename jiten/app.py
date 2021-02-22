#!/usr/bin/python3
# encoding: utf-8

# --                                                            ; {{{1
#
# File        : jiten/app.py
# Maintainer  : Felix C. Stegerman <flx@obfusk.net>
# Date        : 2021-01-30
#
# Copyright   : Copyright (C) 2021  Felix C. Stegerman
# Version     : v0.4.0
# License     : AGPLv3+
#
# --                                                            ; }}}1

                                                                # {{{1
r"""

Web interface.

>>> import re

>>> app.testing = True
>>> client = app.test_client()

>>> def get(*a, **k):
...   r = client.get(*a, **k)
...   print(r.status)
...   return r.data.decode("utf8")

>>> d = get("/")
200 OK
>>> "Jiten Japanese Dictionary" in d
True
>>> "Search JMDict" in d
True
>>> "Search Kanji" in d
True
>>> "Search Sentences" in d
True
>>> "筆順を示す" in d
True

>>> d = get("/jmdict?query=kitten&word=yes")
200 OK
>>> "こꜛねꜜこ" in d
True
>>> "koꜛneꜜko" in d
True
>>> "kitten" in d
True
>>> "small cat" in d
True
>>> "query=猫" in d
True

>>> d = get("/jmdict?query=%2Brandom&jlpt=5", follow_redirects = True)
200 OK
>>> re.search(r"»\s*jlpt\s*<[^>]*>\s*N5", d) is not None
True

>>> d = get("/kanji?query=ねこ")
200 OK
>>> "ビョウ" in d
True
>>> "ねこ" in d
True
>>> "neko" in d
True
>>> "0x732b" in d
True
>>> re.search(r"»\s*jlpt\s*<[^>]*>\s*N3", d) is not None
True
>>> re.search(r"»\s*skip\s*<[^>]*>\s*1-3-8", d) is not None
True

>>> d = get("/kanji?query=日")
200 OK
>>> "ニチ" in d
True
>>> "counter for days" in d
True
>>> "0x65e5" in d
True
>>> re.search(r"»\s*jlpt\s*<[^>]*>\s*N5", d) is not None
True
>>> re.search(r"»\s*skip\s*<[^>]*>\s*3-3-1", d) is not None
True

>>> d = get("/sentences?query=kitten")
200 OK
>>> "I will care for your kitten during your absence." in d
True
>>> re.search(r"任\s*<[^>]*>\s*せてください", d) is not None
True

>>> d = get("/stroke")
200 OK
>>> ">漢字と仮名の筆順<" in d
True

>>> d = get("/stroke?query=何か")
200 OK
>>> ">何か<" in d
True

>>> d = get("/jmdict/by-freq")
200 OK
>>> "する、為る" in d
True

>>> d = get("/jmdict/by-jlpt/1")
200 OK
>>> "あたし、あたくし、あたい、あて、私" in d
True

>>> d = get("/jmdict/by-jlpt/2")
200 OK
>>> "きっかけ、キッカケ、切っ掛け、切掛け、切っかけ、切掛、切っ掛、切かけ" in d
True

>>> d = get("/jmdict/by-jlpt/3")
200 OK
>>> "恐ろしい、怖ろしい" in d
True

>>> d = get("/jmdict/by-jlpt/4")
200 OK
>>> "ああ、あー、あぁ、アー、アア、アァ、嗚呼、噫、嗟" in d
True

>>> d = get("/jmdict/by-jlpt/5")
200 OK
>>> "みる、見る、観る、視る" in d
True

>>> d = get("/kanji/by-freq")
200 OK
>>> "1 | day; sun; Japan; counter for days" in d
True

>>> d = get("/kanji/by-level")
200 OK
>>> d.index("常用1") < d.index("森") < d.index("常用2")
True

>>> d = get("/kanji/by-jlpt")
200 OK
>>> d.index("JLPT N3") < d.index("歯", d.index("JLPT N5")) < d.index("JLPT N2")
True

>>> sorted( (c.name, c.value) for c in client.cookie_jar )
[]
>>> p = dict(dark = "yes", lang = "eng ger oops".split())
>>> r = client.post("/_save_prefs", data = p, follow_redirects = True)
>>> r.status
'200 OK'
>>> sorted( (c.name, c.value) for c in client.cookie_jar )
[('dark', 'yes'), ('lang', '"eng ger"'), ('max', '50'), ('nor2h', 'no'), ('roma', 'no')]

"""                                                             # }}}1

import json, os, sys, time

from pathlib import Path

import click, jinja2, werkzeug

os.environ["FLASK_SKIP_DOTENV"] = "yes"                       #  FIXME
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
  n, v, p = arg("noun"), arg("verb"), arg("prio")
  j       = "-".join(filter(None, request.args.getlist("jlpt"))) or None
  jlpt    = M.JLPT_LEVEL.convert(j) if j else j
  args    = dict(noun = n, verb = v, prio = p, jlpt = j)
  filters = dict(noun = n == "yes", verb = v == "yes",
                 prio = p == "yes", jlpt = jlpt)
  return filters, { k: v for k, v in args.items() if v is not None }

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
  filters, fargs = get_filters()
  if arg("query", "").strip().lower() == "+random":
    q = "+#{}".format(J.random_seq(**filters))
    return redirect(url_for("r_jmdict", query = q, lang = get_langs(),
                            **fargs))
  query, max_r = get_query_max()
  opts = dict(langs = get_langs(), max_results = max_r, **filters)
  data = dict(page = "jmdict", query = query)
  if query: data["results"] = J.search(query, **opts)
  with K.readmeans() as f, P.pitches() as g:
    return respond("jmdict.html", krm = f, elem_pitch = g, **data)

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

if __name__ == "__main__":
  if "--doctest" in sys.argv:
    verbose = "--verbose" in sys.argv
    import doctest
    if doctest.testmod(verbose = verbose)[0]: sys.exit(1)

# vim: set tw=70 sw=2 sts=2 et fdm=marker :
