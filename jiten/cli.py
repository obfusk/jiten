#!/usr/bin/python3
# encoding: utf-8

# --                                                            ; {{{1
#
# File        : jiten/cli.py
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

__version__ = "0.0.1"
name        = "jiten"

import os

import click

from . import jmdict as J
from . import kanji  as K
from . import misc   as M

@click.group()
@click.option("-v", "--verbose", is_flag = True, help = "Be verbose.")
@click.option("-c", "--colour/--no-colour", is_flag = True,
              default = None, help = "Use terminal colours.")
@click.version_option(__version__)
@click.pass_context
def cli(ctx, colour, **kw):
  if colour is not None: ctx.color = colour
  ctx.obj = dict(kw)
  os.environ["PAGER"] = "less -FR"                              # TODO

# TODO
@cli.command(help = "Search JMDict.")
@click.option("-l", "--lang", multiple = True,
              default = [J.LANGS[0]], metavar = "LANG",
              help = "Choose language(s) ("+", ".join(J.LANGS)+").")
@click.option("-w", "--word", is_flag = True,
              help = "Match whole word (same as \\b...\\b).")
@click.option("-e", "--exact", is_flag = True,
              help = "Match exactly (same as ^...$).")
@click.option("-m", "--max", default = None, type = click.INT,
              help = "Maximum number of results.")
@click.argument("query", required = False, metavar = "REGEX")
@click.pass_context
def jmdict(ctx, lang, word, exact, max, query):
  args = (ctx.obj["verbose"], lang, word, exact, max)
  if query:
    click.echo_via_pager(jmdict_search(*args, query))
  else:
    while True:
      q = click.prompt("query", "", show_default = False).strip()
      if not q: break
      click.echo_via_pager(jmdict_search(*args, q))

def jmdict_search(verbose, lang, word, exact, max_results, q):  # {{{1
  q = M.process_query(q, word, exact)
  if verbose:
    yield "query: " + click.style(q, fg = "bright_red") + "\n\n"
  for e, rank in J.search(q, lang, max_results):
    yield (" | ".join(
      click.style(k.elem, fg = "bright_yellow") for k in e.kanji
    ) or "[no kanji]") + "\n"
    yield (" | ".join(
      click.style(r.elem, fg = "bright_green") for r in e.reading
    ) or "[no readings]") + "\n"
    gloss, info = e.gloss_pos_info(lang)
    for l in lang:
      yield click.style("[" + l + "]", fg = "cyan") + "\n"
      for g in gloss[l]:
        t = click.wrap_text("| ".join(g),
          click.get_terminal_size()[0], initial_indent = "  ",
          subsequent_indent = "  "
        )[2:].replace("|", click.style(" |", fg = "magenta"))
        yield click.style("* ", fg = "magenta") + t + "\n"
    t = click.wrap_text("| ".join(info),
      click.get_terminal_size()[0], initial_indent = "   ",
      subsequent_indent = "   "
    )[3:].replace("|", click.style(" |", fg = "green"))
    if t: yield click.style(">> ", fg = "green") + t + "\n"
    if verbose:
      yield   "seq# " + click.style(str(e.seq), fg = "blue") \
        + (", freq# " + click.style(str(rank ), fg = "cyan")
            if rank else "") + "\n"
    yield "\n"
                                                                # }}}1

# TODO
@cli.command(help = "Search KanjiDic.")
@click.option("-w", "--word", is_flag = True,
              help = "Match whole word (same as \\b...\\b).")
@click.option("-e", "--exact", is_flag = True,
              help = "Match exactly (same as ^...$).")
@click.option("-m", "--max", default = None, type = click.INT,
              help = "Maximum number of results.")
@click.argument("query", required = False, metavar = "REGEX")
@click.pass_context
def kanji(ctx, word, exact, max, query):
  args = (ctx.obj["verbose"], word, exact, max)
  if query:
    click.echo_via_pager(kanji_search(*args, query))
  else:
    while True:
      q = click.prompt("query", "", show_default = False).strip()
      if not q: break
      click.echo_via_pager(kanji_search(*args, q))

def kanji_search(verbose, word, exact, max_results, q):         # {{{1
  q = M.process_query(q, word, exact)
  if verbose:
    yield "query: " + click.style(q, fg = "bright_red") + "\n\n"
  for e in K.search(q, max_results):
    yield e.char + "\n"
    yield (" | ".join(
      click.style(r, fg = "bright_yellow") for r in e.on
    ) or "[no on readings]") + "\n"
    yield (" | ".join(
      click.style(r, fg = "bright_green") for r in e.kun
    ) or "[no kun readings]") + "\n"
    yield (" | ".join(
      click.style(r, fg = "cyan") for r in e.nanori
    ) or "[no name readings]") + "\n"
    for m in e.meaning:
      yield click.style("* ", fg = "magenta") + m + "\n"
    if verbose:
      yield (click.style(hex(ord(e.char)), fg = "blue")
        + ", " + click.style(str(e.strokes), fg = "yellow")
        + " strokes"
        + (", grade " + click.style(e.level, fg = "cyan")
           if e.level else "")
        + (", freq# " + click.style(str(e.freq), fg = "magenta")
           if e.freq else "")
        + (", old jlpt " + click.style(str(e.jlpt), fg = "blue")
           if e.jlpt else "")
        + (", skip " + click.style(e.skip, fg = "yellow")
           if e.skip else "")) + "\n"
    yield "\n"
                                                                # }}}1

@cli.command(help = "Serve the web interface.")
@click.option("-h", "--host", default = "localhost", metavar = "HOST")
@click.option("-p", "--port", default = 5000, metavar = "PORT", type = click.INT)
def serve(host, port):
  from .app import app
  app.run(host = host, port = port, load_dotenv = False)

# TODO
@cli.command(help = "Create sqlite databases from XML files.")
def setup():
  J.setup()
  K.setup()

if __name__ == "__main__":
  cli(prog_name = name)

# vim: set tw=70 sw=2 sts=2 et fdm=marker :
