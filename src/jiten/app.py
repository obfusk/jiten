#!/usr/bin/python3
# encoding: utf-8

# --                                                            ; {{{1
#
# File        : jiten/app.py
# Maintainer  : Felix C. Stegerman <flx@obfusk.net>
# Date        : 2020-06-16
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

import os

import jinja2

from flask import Flask, redirect, request, render_template, url_for

from . import jmdict as J
from . import kanji  as K

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

@app.route("/")
def r_index():
  return render_template("index.html", page = "index")

# TODO
@app.route("/jmdict")
def r_jmdict():
  query = request.args.get("query", "")
  lang  = [ l for l in request.args.getlist("lang") if l in J.LANGS ]
  return render_template("jmdict.html", page = "jmdict",
                         query = query, lang = lang)

# TODO
@app.route("/kanji")
def r_kanji():
  query = request.args.get("query", "")
  return render_template("kanji.html", page = "kanji", query = query)

@app.route("/stroke")
def r_stroke():
  query = request.args.get("query", "")
  return render_template("stroke.html", page= "stroke", query = query)

# vim: set tw=70 sw=2 sts=2 et fdm=marker :
