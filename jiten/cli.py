#!/usr/bin/python3
# encoding: utf-8

# --                                                            ; {{{1
#
# File        : jiten/cli.py
# Maintainer  : Felix C. Stegerman <flx@obfusk.net>
# Date        : 2020-06-21
#
# Copyright   : Copyright (C) 2020  Felix C. Stegerman
# Version     : v0.0.1
# License     : AGPLv3+
#
# --                                                            ; }}}1

                                                                # {{{1
r"""

CLI

>>> click.get_terminal_size = lambda: [80, None]
>>> run = lambda a: cli(args = a.split(), standalone_mode = False, prog_name = name)

=== JMDict ===

>>> run("jmdict -m1 -w cat")
猫
ねこ | ネコ
[eng]
* cat (esp. the domestic cat, Felis catus)
* shamisen
* geisha
* wheelbarrow
* clay bed-warmer
* bottom | submissive partner of a homosexual relationship
--> noun (common) (futsuumeishi) | abbreviation | word usually written using
    kana alone | colloquialism
<BLANKLINE>
<BLANKLINE>

>>> run("-v jmdict -m1 -w cat")
query: \bcat\b
<BLANKLINE>
猫
ねこ | ネコ
[eng]
* cat (esp. the domestic cat, Felis catus)
* shamisen
* geisha
* wheelbarrow
* clay bed-warmer
* bottom | submissive partner of a homosexual relationship
--> noun (common) (futsuumeishi) | abbreviation | word usually written using
    kana alone | colloquialism
see 猫車 | 猫火鉢
seq# 1467640, freq# 2201, prio
<BLANKLINE>
<BLANKLINE>

>>> run("-v jmdict -m1 -w kat -l dut")
query: \bkat\b
<BLANKLINE>
猫
ねこ | ネコ
[dut]
* {dierk.} kat | poes | {Barg.} mauwerik | Felis ocreata domestica | {i.h.b.}
  katachtige
* geisha | poes | {Barg.} minette
* kruiwagen
--> noun (common) (futsuumeishi)
see 猫車 | 猫火鉢
seq# 1467640, freq# 2201, prio
<BLANKLINE>
<BLANKLINE>

>>> run("-v jmdict -m1 -w idiot")
query: \bidiot\b
<BLANKLINE>
馬鹿 | 莫迦 | 破家 | 馬稼
ばか | バカ
[eng]
* idiot | moron | fool
* trivial matter | folly | absurdity
* stupid | foolish | dull | absurd | ridiculous
* fervent enthusiast | nut | person singularly obsessed with something
* Mactra chinensis (species of trough shell)
--> noun (common) (futsuumeishi) | adjectival nouns or quasi-adjectives
    (keiyodoshi) | word usually written using kana alone | usu. in compounds |
    abbreviation
~~> ateji (phonetic) reading
see 馬鹿貝
seq# 1601260, freq# 2472, prio
<BLANKLINE>
<BLANKLINE>

>>> run("-v jmdict -m1 -e 誤魔化す")
query: ^誤魔化す$
<BLANKLINE>
誤魔化す | 誤摩化す | 胡麻化す | 誤魔かす | 胡魔化す
ごまかす
[eng]
* to deceive | to falsify | to misrepresent | to cheat | to swindle | to
  tamper | to juggle | to manipulate
* to dodge | to beg the question (issue, difficulties)
* to varnish over | to gloss over
--> Godan verb with `su' ending | transitive verb | word usually written using
    kana alone
~~> ateji (phonetic) reading
seq# 1271480, freq# 10495, prio
<BLANKLINE>
<BLANKLINE>

>>> run("-v jmdict -m1 -w まる")
query: \bまる\b
<BLANKLINE>
丸 | 円
まる
[eng]
* circle
* entirety | whole | full | complete
* money | dough | moola
* enclosure inside a castle's walls
* soft-shelled turtle
* suffix for ship names | suffix for names of people (esp. infants) | suffix for
  names of swords, armour, musical instruments, etc. | suffix for names of dogs,
  horses, etc.
--> noun (common) (futsuumeishi) | noun, used as a prefix | suffix | slang |
    esp. 丸
see ○ | まる | スッポン | 麻呂
seq# 1216250, freq# 63, prio
<BLANKLINE>
<BLANKLINE>

>>> run("-v jmdict -m1 -w cat --verb")
query: \bcat\b
<BLANKLINE>
逆撫で | 逆なで
さかなで | ぎゃくなで
[eng]
* rubbing the wrong way (e.g. a cat) | irritating
--> noun (common) (futsuumeishi) | noun or participle which takes the aux. verb
    suru
~~> word containing irregular kana usage
seq# 1227180, freq# 30500
<BLANKLINE>
<BLANKLINE>

>>> run("-v jmdict -m1 -w みる --noun")
query: \bみる\b
<BLANKLINE>
海松 | 水松
みる | すいしょう | ミル
[eng]
* stag seaweed (Codium fragile) | green sea fingers | dead man's fingers | felty
  fingers | forked felt-alga | sponge seaweed | green sponge | green fleece |
  oyster thief
--> noun (common) (futsuumeishi) | word usually written using kana alone
seq# 1772790, freq# 75
<BLANKLINE>
<BLANKLINE>

>>> run("-v jmdict -m1 -w みる --noun --prio")
query: \bみる\b
<BLANKLINE>
<BLANKLINE>


=== Kanji ===

>>> run("kanji -m1 -w cat")
猫
ビョウ
ねこ
[no name readings]
* cat
<BLANKLINE>
<BLANKLINE>

>>> run("-v kanji -m1 -e cat")
query: ^cat$
<BLANKLINE>
猫
ビョウ
ねこ
[no name readings]
* cat
0x732b, 11 strokes, grade 常用, freq# 1702, old jlpt 2, skip 1-3-8
<BLANKLINE>
<BLANKLINE>

>>> run("-v kanji -m1 -w 日")
query: \b日\b
<BLANKLINE>
日
ニチ | ジツ
ひ | -び | -か
あ | あき | いる | く | くさ | こう | す | たち | に | にっ | につ | へ
* day
* sun
* Japan
* counter for days
0x65e5, 4 strokes, grade 常用1, freq# 1, old jlpt 4, skip 3-3-1
<BLANKLINE>
<BLANKLINE>

"""                                                             # }}}1

__version__ = "0.1.0"
name        = "jiten"

import os, sys

import click

from . import jmdict as J
from . import kanji  as K
from . import misc   as M

def check_db(ctx):
  if not os.path.exists(J.SQLITE_FILE):
    click.secho("DB not found; please run setup first.",
                fg = "red", err = True)
    ctx.exit(1)

@click.group(help = """
  jiten - japanese cli&web dictionary based on jmdict/kanjidic
""")
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
@click.option("-1", "--1stword", "--first-word", "fstwd", is_flag = True,
              help = "Match first word (same as ^...\\b).")
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
  check_db(ctx)
  ctx.obj.update(kw)
  if query:
    click.echo_via_pager(jmdict_search(query, **ctx.obj))
  else:
    while True:
      q = click.prompt("query", "", show_default = False).strip()
      if not q: break
      click.echo_via_pager(jmdict_search(q, **ctx.obj))

def jmdict_search(q, verbose, word, exact, fstwd, langs, **kw): # {{{1
  q = M.process_query(q, word, exact, fstwd)
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
    t = indent_and_wrap(info, "--> ", "green")
    if t: yield t
    if verbose:
      ti = indent_and_wrap(e.xinfo(), "~~> ", "blue")
      if ti: yield ti
      tx = indent_and_wrap(e.xrefs(), "see ", "yellow")
      if tx: yield tx
      yield   "seq# " + click.style(str(e.seq), fg = "blue") \
        + (", freq# " + click.style(str(rank ), fg = "cyan")
                    if rank else "") \
        + (", prio" if e.isprio() else "") + "\n"
    yield "\n"
                                                                # }}}1

def indent_and_wrap(xs, pre, fg):
  xs = list(xs)
  if not xs: return None
  t = click.wrap_text("| ".join(xs),
    click.get_terminal_size()[0], initial_indent = pre,
    subsequent_indent = " " * len(pre)
  )[len(pre):].replace("|", click.style(" |", fg = fg))
  return click.style(pre, fg = fg) + t + "\n"

@cli.command(help = "Search KanjiDic.")
@click.option("-w", "--word", is_flag = True,
              help = "Match whole word (same as \\b...\\b).")
@click.option("-1", "--1stword", "--first-word", "fstwd", is_flag = True,
              help = "Match first word (same as ^...\\b).")
@click.option("-e", "--exact", is_flag = True,
              help = "Match exactly (same as ^...$).")
@click.option("-m", "--max", "max_results", default = None,
              type = click.INT, help = "Maximum number of results.")
@click.argument("query", required = False, metavar = "REGEX")
@click.pass_context
def kanji(ctx, query, **kw):
  check_db(ctx)
  ctx.obj.update(kw)
  if query:
    click.echo_via_pager(kanji_search(query, **ctx.obj))
  else:
    while True:
      q = click.prompt("query", "", show_default = False).strip()
      if not q: break
      click.echo_via_pager(kanji_search(q, **ctx.obj))

def kanji_search(q, verbose, word, exact, fstwd, max_results):  # {{{1
  q = M.process_query(q, word, exact, fstwd)
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
@click.pass_context
def serve(ctx, host, port):
  check_db(ctx)
  from .app import app
  app.run(host = host, port = port, load_dotenv = False)

# TODO
@cli.command(help = "Create sqlite databases from XML files.")
def setup():
  msg = "up to date"
  if J.setup():
    msg = "set up"
    K.setup()
  click.secho("DB v{} {}.".format(J.DBVERSION, msg), fg = "green")

@cli.command("_doctest", hidden = True)
@click.option("-v", "--verbose", is_flag = True)
@click.pass_context
def doctest(ctx, verbose):
  check_db(ctx)
  import doctest
  if doctest.testmod(verbose = verbose)[0]: ctx.exit(1)

if __name__ == "__main__":
  cli(prog_name = name)

# vim: set tw=70 sw=2 sts=2 et fdm=marker :
