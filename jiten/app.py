#!/usr/bin/python3
# encoding: utf-8

# --                                                            ; {{{1
#
# File        : jiten/app.py
# Maintainer  : Felix C. Stegerman <flx@obfusk.net>
# Date        : 2020-08-12
#
# Copyright   : Copyright (C) 2020  Felix C. Stegerman
# Version     : v0.2.0
# License     : AGPLv3+
#
# --                                                            ; }}}1

                                                                # {{{1
r"""

Web interface.

"""                                                             # }}}1

import json, os, time

import jinja2

from flask import Flask, make_response, redirect, request, \
                  render_template, url_for

from . import jmdict    as J
from . import kanji     as K
from . import misc      as M
from . import sentences as S

START   = int(time.time())
MAX     = 50
name    = "jiten"
HTTPS   = name.upper() + "_HTTPS"
DOMAIN  = name.upper() + "_DOMAIN"
app     = Flask(__name__)

if "ANDROID_PRIVATE" in os.environ:
  CONF = os.path.join(os.environ["ANDROID_PRIVATE"], "jiten-prefs.json")
  def load_prefs():
    try:
      with open(CONF) as f: return json.load(f)
    except (OSError, ValueError):
      return {}
  def save_prefs(p):
    with open(CONF, "w") as f:
      json.dump(p, f, indent = 2, sort_keys = True)
      f.write("\n")
  def get_pref(k, d = None):
    return load_prefs().get(k, d)
  def set_pref(k, v, _resp):
    save_prefs({ **load_prefs(), k: v })
else:
  def get_pref(k, d = None):
    return request.cookies.get(k, d)
  def set_pref(k, v, resp):
    resp.set_cookie(k, v, max_age = 3600*24*365*10)

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

def dark_toggle_link(dark):
  targs = request.args.copy()
  targs.setlist("dark", ["no" if dark else "yes"])
  targs.setlist("save", ["yes"])
  return url_for(request.endpoint, **dict(targs.lists()))

def respond(template, **data):
  langs, dark = get_langs(), arg_bool("dark", get_pref("dark"))
  if arg_bool("save"):
    k, v = ("dark", "yes" if dark else "no") \
           if "dark" in request.args else ("lang", " ".join(langs))
    resp = redirect(request.url.replace("&save=yes", ""))       # TODO
    set_pref(k, v, resp)
    return resp
  return make_response(render_template(
    template, dark = dark, langs = langs, J = J, K = K, M = M, S = S,
    toggle = dark_toggle_link(dark), ord = ord, hex = hex,
    START = START, **data
  ))

def get_langs():
  ls = request.args.getlist("lang") or get_pref("lang", "").split()
  return [ l for l in ls if l in J.LANGS ] or [J.LANGS[0]]

def get_sentence_langs():
  ls = request.args.getlist("lang")
  return [ l for l in ls if l in S.LANGS ]

def get_query_max():
  w, e, f = arg_bool("word"), arg_bool("exact"), arg_bool("1stword")
  return M.process_query(arg("query"), w, e, f), arg("max", MAX, type = int)

@app.route("/")
def r_index():
  return respond("index.html", page = "index")

# TODO
# * --max
@app.route("/jmdict")
def r_jmdict():
  if arg("query", "").strip().lower() == "+random":
    return redirect(url_for("r_jmdict_random"))
  query, max_r = get_query_max()
  opts = dict(langs = get_langs(), max_results = max_r,
              noun = arg_bool("noun"), verb = arg_bool("verb"))
  data = dict(page = "jmdict", query = query)
  try:
    if query: data["results"] = J.search(query, **opts)
    return respond("jmdict.html", **data)
  except M.RegexError as e:
    return "regex error: " + str(e), 400

@app.route("/jmdict/by-freq")
def r_jmdict_by_freq():
  offset  = arg("offset", 0, type = int)
  results = list(J.by_freq(offset, 1000))
  return respond("jmdict-by-freq.html", page = "jmdict/by-freq",
                 offset = offset, results = results)

@app.route("/jmdict/random")
def r_jmdict_random():
  q = "+#{}".format(J.random_seq())
  return redirect(url_for("r_jmdict", query = q))

# TODO
# * --max
@app.route("/kanji")
def r_kanji():
  if arg("query", "").strip().lower() == "+random":
    return redirect(url_for("r_kanji_random"))
  query, max_r = get_query_max()
  data = dict(page = "kanji", query = query)
  try:
    if query: data["results"] = K.search(query, max_results = max_r)
    return respond("kanji.html", **data)
  except M.RegexError as e:
    return "regex error: " + str(e), 400

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

@app.route("/kanji/random")
def r_kanji_random():
  return redirect(url_for("r_kanji", query = K.random().char))

# TODO: langs
@app.route("/sentences")
def r_sentences():
  query, max_r = arg("query", "").strip(), arg("max", MAX, type = int)
  opts = dict(langs = get_sentence_langs(), max_results = max_r,
              audio = arg_bool("audio"))
  data = dict(page = "sentences", query = query)
  if query: data["results"] = S.search(query, **opts)
  return respond("sentences.html", **data)

@app.route("/stroke")
def r_stroke():
  return respond("stroke.html", page = "stroke",
                 query = arg("query", "").strip())

# vim: set tw=70 sw=2 sts=2 et fdm=marker :
