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

import jiten.jmdict as J

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
@click.option("--lang", multiple = True, default = [J.DLANG])
@click.argument("query")
@click.pass_context
def jmdict(ctx, lang, query):                                   # {{{1
  if ctx.obj["verbose"]:
    click.echo("query: " + click.style(query, fg = "bright_red"))
    click.echo()
  for e in J.search(query, lang):
    if ctx.obj["verbose"]:
      click.echo("#" + click.style(str(e.seq), fg = "blue"))
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
    click.echo()
                                                                # }}}1

# TODO
@cli.command(help = "Search KanjiDic.")
@click.argument("query")
@click.pass_context
def kanji(ctx, query):                                          # {{{1
  click.echo(click.style("TODO", fg = "red"))
  ctx.exit(1)
                                                                # }}}1

# TODO
@cli.command(help = "Serve the web interface.")
@click.option("--host", default = "localhost")
@click.option("--port", default = 8888, type = click.INT)
@click.pass_context
def serve(ctx, host, port):
  click.echo(click.style("TODO", fg = "red"))
  ctx.exit(1)

# TODO
@cli.command(help = "Create sqlite databases from XML files.")
def setup():
  J.setup()

if __name__ == "__main__":
  cli()

# vim: set tw=70 sw=2 sts=2 et fdm=marker :
