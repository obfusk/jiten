#!/usr/bin/python3
# encoding: utf-8

# --                                                            ; {{{1
#
# File        : jiten/app.py
# Maintainer  : Felix C. Stegerman <flx@obfusk.net>
# Date        : 2020-06-20
#
# Copyright   : Copyright (C) 2020  Felix C. Stegerman
# Version     : v0.0.1
# License     : AGPLv3+
#
# --                                                            ; }}}1

                                                                # {{{1
r"""

Web interface.

"""                                                             # }}}1

import os, re

import jinja2

from flask import Flask, make_response, redirect, request, \
                  render_template, url_for

from . import jmdict as J
from . import kanji  as K
from . import misc   as M

MAX   = 50
name  = "jiten"
app   = Flask(__name__)

if os.environ.get(name.upper() + "_HTTPS") == "force":
  @app.before_request
  def https_required():
    if request.scheme != "https":
      return redirect(request.url.replace("http:", "https:"), code = 301)
  @app.after_request
  def after_request_func(response):
    response.headers["Strict-Transport-Security"] = 'max-age=63072000'
    return response

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
  langs, dark = get_langs(), arg_bool("dark", request.cookies.get("dark"))
  resp = make_response(render_template(
    template, dark = dark, LANGS = J.LANGS, langs = langs,
    toggle = dark_toggle_link(dark), **data
  ))
  if arg_bool("save"):
    if "dark" in request.args:
      resp.set_cookie("dark", "yes" if dark else "no")
    else:
      resp.set_cookie("lang", " ".join(langs))
  return resp

def get_langs():
  ls = request.args.getlist("lang") or request.cookies.get("lang", "").split()
  return [ l for l in ls if l in J.LANGS ] or [J.LANGS[0]]

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
  query, max_r = get_query_max()
  opts = dict(langs = get_langs(), max_results = max_r,
              noun = arg_bool("noun"), verb = arg_bool("verb"))
  data = dict(page = "jmdict", query = query, isideo = M.isideo)
  try:
    if query: data["results"] = J.search(query, **opts)
    return respond("jmdict.html", **data)
  except re.error as e:
    return "regex error: " + str(e)

# TODO
# * --max
@app.route("/kanji")
def r_kanji():
  query, max_r = get_query_max()
  data = dict(page = "kanji", query = query, ord = ord, hex = hex)
  try:
    if query: data["results"] = K.search(query, max_results = max_r)
    return respond("kanji.html", **data)
  except re.error as e:
    return "regex error: " + str(e)

@app.route("/stroke")
def r_stroke():
  return respond("stroke.html", page= "stroke",
                 query = arg("query", "").strip())

# vim: set tw=70 sw=2 sts=2 et fdm=marker :
