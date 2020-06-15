#!/usr/bin/python3
# encoding: utf-8

# --                                                            ; {{{1
#
# File        : jiten/cli.py
# Maintainer  : Felix C. Stegerman <flx@obfusk.net>
# Date        : 2020-06-15
#
# Copyright   : Copyright (C) 2020  Felix C. Stegerman
# Version     : v0.0.1
# License     : GPLv3+
#
# --                                                            ; }}}1

                                                                # {{{1
r"""

...

"""                                                             # }}}1

__version__ = "0.0.1"

import click

from . import jmdict as J
from . import kanji as K

@click.group()
@click.option("-v", "--verbose", is_flag = True, help = "Be verbose.")
@click.option("-c", "--colour/--no-colour", is_flag = True,
              default = None, help = "Use terminal colours.")
@click.version_option(__version__)
@click.pass_context
def cli(ctx, colour, **kw):
  if colour is not None: ctx.color = colour
  ctx.obj = dict(kw)

# TODO
@cli.command(help = "Search JMDict.")
@click.option("-l", "--lang", multiple = True, default = [J.DLANG],
              metavar = "LANG",
              help = "Choose language(s) ("+", ".join(J.LANGS)+").")
@click.option("-w", "--word", is_flag = True,
              help = "Match whole word (same as \\b...\\b).")
@click.option("-m", "--max", default = None, type = click.INT,
              help = "Maximum number of results.")
@click.argument("query", required = False)
@click.pass_context
def jmdict(ctx, lang, word, max, query):                        # {{{1
  q = query or click.prompt("query")
  if word: q = "\\b" + q + "\\b"
  if ctx.obj["verbose"]:
    click.echo("query: " + click.style(q, fg = "bright_red"))
    click.echo()
  for e, rank in J.search(q, lang, max):
    click.echo(" | ".join(
      click.style(k.elem, fg = "bright_yellow") for k in e.kanji
    ))
    click.echo(" | ".join(
      click.style(r.elem, fg = "bright_green") for r in e.reading
    ))
    for l in lang:
      click.echo(click.style("[" + l + "]", fg = "cyan"))
      for m in e.meanings(l):
        t = click.wrap_text("| ".join(m),
          click.get_terminal_size()[0], initial_indent = "  ",
          subsequent_indent = "  "
        )[2:].replace("|", click.style(" |", fg = "magenta"))
        click.echo(click.style("* ", fg = "magenta") + t)
    if e.usually_kana():
      click.echo("[" + J.USUKANA + "]")
    if ctx.obj["verbose"]:
      click.echo("seq# " + click.style(str(e.seq), fg = "blue")
                 + ", freq# " + click.style(str(rank), fg = "cyan"))
    click.echo()
                                                                # }}}1

# TODO
@cli.command(help = "Search KanjiDic.")
@click.option("-w", "--word", is_flag = True,
              help = "Match whole word (same as \\b...\\b).")
@click.option("-m", "--max", default = None, type = click.INT,
              help = "Maximum number of results.")
@click.argument("query", required = False)
@click.pass_context
def kanji(ctx, word, max, query):                               # {{{1
  q = query or click.prompt("query")
  if word: q = "\\b" + q + "\\b"
  if ctx.obj["verbose"]:
    click.echo("query: " + click.style(q, fg = "bright_red"))
    click.echo()
  for e in K.search(q, max):
    click.echo(e.char)
    click.echo(" | ".join(
      click.style(r, fg = "bright_yellow") for r in e.on
    ) or "[no on readings]")
    click.echo(" | ".join(
      click.style(r, fg = "bright_green") for r in e.kun
    ) or "[no kun readings]")
    click.echo(" | ".join(
      click.style(r, fg = "cyan") for r in e.nanori
    ) or "[no name readings]")
    for m in e.meaning:
      click.echo(click.style("* ", fg = "magenta") + m)
    if ctx.obj["verbose"]:
      click.echo(
        click.style(hex(ord(e.char)), fg = "blue")
        + ", " + click.style(str(e.strokes), fg = "yellow")
        + " strokes"
        + (", grade " + click.style(e.level, fg = "cyan")
           if e.level else "")
        + (", freq# " + click.style(str(e.freq), fg = "magenta")
           if e.freq else "")
        + (", old jlpt " + click.style(str(e.jlpt), fg = "blue")
           if e.jlpt else "")
        + (", skip " + click.style(e.skip, fg = "yellow")
           if e.skip else "")
      )
    click.echo()
                                                                # }}}1

# TODO
@cli.command(help = "Serve the web interface.")
@click.option("--host", default = "localhost", metavar = "HOST")
@click.option("--port", default = 8888, metavar = "PORT", type = click.INT)
@click.pass_context
def serve(ctx, host, port):
  click.echo(click.style("TODO", fg = "red"))
  ctx.exit(1)

# TODO
@cli.command(help = "Create sqlite databases from XML files.")
def setup():
  J.setup()
  K.setup()

if __name__ == "__main__":
  cli()

# vim: set tw=70 sw=2 sts=2 et fdm=marker :
