#!/usr/bin/python3
# encoding: utf-8

# --                                                            ; {{{1
#
# File        : jiten/app.py
# Maintainer  : Felix C. Stegerman <flx@obfusk.net>
# Date        : 2020-06-18
#
# Copyright   : Copyright (C) 2020  Felix C. Stegerman
# Version     : v0.0.1
# License     : AGPLv3+
#
# --                                                            ; }}}1

                                                                # {{{1
r"""

...

"""                                                             # }}}1

import os, re

import jinja2

from flask import Flask, make_response, redirect, request, render_template

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

# TODO
def respond(template, **data):
  langs = get_langs()
  dark  = "yes" == request.args.get("dark", request.cookies.get("dark"))
  resp  = make_response(render_template(
    template, dark = dark, LANGS = J.LANGS, langs = langs, **data
  ))
  if "yes" == request.args.get("save"):
    resp.set_cookie("dark", "yes" if dark else "no")
    resp.set_cookie("lang", " ".join(langs))
  return resp

def get_langs():
  ls = request.args.getlist("lang") or request.cookies.get("lang", "").split()
  return [ l for l in ls if l in J.LANGS ] or [J.LANGS[0]]

def get_word_exact_query_max():
  word  = "yes" == request.args.get("word")
  exact = "yes" == request.args.get("exact")
  query = M.process_query(request.args.get("query"), word, exact)
  max_r = request.args.get("max", MAX, type = int)
  return word, exact, query, max_r

@app.route("/")
def r_index():
  return respond("index.html", page = "index")

# TODO
# * --max
@app.route("/jmdict")
def r_jmdict():
  word, exact, query, max_r = get_word_exact_query_max()
  langs = get_langs()[0]
  data  = dict(page = "jmdict", query = query, isideo = M.isideo,
               USUKANA = J.USUKANA)
  try:
    if query:
      data["results"] = J.search(query, langs, max_results = max_r)
    return respond("jmdict.html", **data)
  except re.error as e:
    return "regex error: " + str(e)

# TODO
# * --max
@app.route("/kanji")
def r_kanji():
  word, exact, query, max_r = get_word_exact_query_max()
  data = dict(page = "kanji", query = query, ord = ord, hex = hex)
  try:
    if query:
      data["results"] = K.search(query, max_results = max_r)
    return respond("kanji.html", **data)
  except re.error as e:
    return "regex error: " + str(e)

@app.route("/stroke")
def r_stroke():
  query = request.args.get("query", "").strip()
  return respond("stroke.html", page= "stroke", query = query)

# vim: set tw=70 sw=2 sts=2 et fdm=marker :
