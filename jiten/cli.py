#!/usr/bin/python3
# encoding: utf-8

# --                                                            ; {{{1
#
# File        : jiten/cli.py
# Maintainer  : Felix C. Stegerman <flx@obfusk.net>
# Date        : 2020-06-19
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

@cli.command(help = "Search JMDict.")
@click.option("-l", "--lang", "langs", multiple = True,
              default = [J.LANGS[0]], metavar = "LANG",
              help = "Choose language(s) ("+", ".join(J.LANGS)+").")
@click.option("-w", "--word", is_flag = True,
              help = "Match whole word (same as \\b...\\b).")
@click.option("-e", "--exact", is_flag = True,
              help = "Match exactly (same as ^...$).")
@click.option("-m", "--max", "max_results", default = None,
              type = click.INT, help = "Maximum number of results.")
@click.option("--noun", is_flag = True, help = "Select nouns.")
@click.option("--verb", is_flag = True, help = "Select verbs.")
@click.option("--prio", is_flag = True, help = "Select priority entries.")
@click.argument("query", required = False, metavar = "REGEX")
@click.pass_context
def jmdict(ctx, query, **kw):
  ctx.obj.update(kw)
  if query:
    click.echo_via_pager(jmdict_search(query, **ctx.obj))
  else:
    while True:
      q = click.prompt("query", "", show_default = False).strip()
      if not q: break
      click.echo_via_pager(jmdict_search(q, **ctx.obj))

def indent_and_wrap(xs, pre, fg):
  xs = list(xs)
  if not xs: return None
  t = click.wrap_text("| ".join(xs),
    click.get_terminal_size()[0], initial_indent = pre,
    subsequent_indent = " " * len(pre)
  )[len(pre):].replace("|", click.style(" |", fg = fg))
  return click.style(pre, fg = fg) + t + "\n"

def jmdict_search(q, verbose, word, exact, langs, **kw):  # {{{1
  q = M.process_query(q, word, exact)
  if verbose:
    yield "query: " + click.style(q, fg = "bright_red") + "\n\n"
  for e, rank in J.search(q, langs = langs, **kw):
    yield (" | ".join(
      click.style(k.elem, fg = "bright_yellow") for k in e.kanji
    ) or "[no kanji]") + "\n"
    yield (" | ".join(
      click.style(r.elem, fg = "bright_green") for r in e.reading
    ) or "[no readings]") + "\n"
    gloss, info = e.gloss_pos_info(langs)
    for l in langs:
      yield click.style("[" + l + "]", fg = "cyan") + "\n"
      for g in gloss[l]:
        yield indent_and_wrap(g, "* ", "magenta")
    t = indent_and_wrap(info, ">>> ", "green")
    if t: yield t
    if verbose:
      ti = indent_and_wrap(e.xinfo(), "~~~ ", "blue")
      if ti: yield ti
      tx = indent_and_wrap(e.xrefs(), "see ", "yellow")
      if tx: yield tx
      yield   "seq# " + click.style(str(e.seq), fg = "blue") \
        + (", freq# " + click.style(str(rank ), fg = "cyan")
                    if rank else "") \
        + (", prio" if e.isprio() else "") + "\n"
    yield "\n"
                                                                # }}}1

@cli.command(help = "Search KanjiDic.")
@click.option("-w", "--word", is_flag = True,
              help = "Match whole word (same as \\b...\\b).")
@click.option("-e", "--exact", is_flag = True,
              help = "Match exactly (same as ^...$).")
@click.option("-m", "--max", "max_results", default = None,
              type = click.INT, help = "Maximum number of results.")
@click.argument("query", required = False, metavar = "REGEX")
@click.pass_context
def kanji(ctx, query, **kw):
  ctx.obj.update(kw)
  if query:
    click.echo_via_pager(kanji_search(query, **ctx.obj))
  else:
    while True:
      q = click.prompt("query", "", show_default = False).strip()
      if not q: break
      click.echo_via_pager(kanji_search(q, **ctx.obj))

def kanji_search(q, verbose, word, exact, max_results):         # {{{1
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
