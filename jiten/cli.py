#!/usr/bin/python3
# encoding: utf-8

# --                                                            ; {{{1
#
# File        : jiten/cli.py
# Maintainer  : Felix C. Stegerman <flx@obfusk.net>
# Date        : 2021-01-22
#
# Copyright   : Copyright (C) 2021  Felix C. Stegerman
# Version     : v0.3.5
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
ねꜜこ
[eng]
= cat (esp. the domestic cat, Felis catus)
= shamisen
= geisha
= wheelbarrow
= clay bed-warmer
= bottom | submissive partner of a homosexual relationship
--> noun (common) (futsuumeishi) | abbreviation | word usually written using
    kana alone | colloquialism
<BLANKLINE>
<BLANKLINE>

>>> run("-v jmdict -m1 -w cat")
DB v11 up to date.
query: +w cat
<BLANKLINE>
猫
ねこ | ネコ
ねꜜこ
[eng]
= cat (esp. the domestic cat, Felis catus)
= shamisen
= geisha
= wheelbarrow
= clay bed-warmer
= bottom | submissive partner of a homosexual relationship
--> noun (common) (futsuumeishi) | abbreviation | word usually written using
    kana alone | colloquialism
see 猫車 | 猫火鉢
seq# 1467640, freq# 2201, jlpt N5, prio; 1
<BLANKLINE>
<BLANKLINE>

>>> run("-v jmdict -m1 -w kat -l dut")
DB v11 up to date.
query: +w kat
<BLANKLINE>
猫
ねこ | ネコ
ねꜜこ
[dut]
= {dierk.} kat | poes | {Barg.} mauwerik | Felis ocreata domestica | {i.h.b.}
  katachtige
= geisha | poes | {Barg.} minette
= kruiwagen
--> noun (common) (futsuumeishi)
see 猫車 | 猫火鉢
seq# 1467640, freq# 2201, jlpt N5, prio; 1
<BLANKLINE>
<BLANKLINE>

>>> run("-v jmdict -m1 -w idiot")
DB v11 up to date.
query: +w idiot
<BLANKLINE>
馬鹿 | 莫迦 | 破家 | 馬稼
ばか | バカ
ばꜜか
[eng]
= idiot | moron | fool
= trivial matter | folly | absurdity
= stupid | foolish | dull | absurd | ridiculous
= fervent enthusiast | nut | person singularly obsessed with something
= Mactra chinensis (species of trough shell)
--> noun (common) (futsuumeishi) | adjectival nouns or quasi-adjectives
    (keiyodoshi) | word usually written using kana alone | usu. in compounds |
    abbreviation
~~> ateji (phonetic) reading
see 馬鹿貝
seq# 1601260, freq# 2472, jlpt N3, prio; 1
<BLANKLINE>
<BLANKLINE>

>>> run("-v jmdict -m1 -e 誤魔化す")
DB v11 up to date.
query: += 誤魔化す
<BLANKLINE>
誤魔化す | 誤摩化す | 胡麻化す | 誤魔かす | 胡魔化す
ごまかす
ごꜛまかꜜす
[eng]
= to deceive | to falsify | to misrepresent | to cheat | to swindle | to
  tamper | to juggle | to manipulate
= to dodge | to beg the question (issue, difficulties)
= to varnish over | to gloss over
--> Godan verb with 'su' ending | transitive verb | word usually written using
    kana alone
~~> ateji (phonetic) reading
seq# 1271480, freq# 10495, jlpt N1, prio; 1
<BLANKLINE>
<BLANKLINE>

>>> run("-v jmdict -m1 -w まる")
DB v11 up to date.
query: +w まる
<BLANKLINE>
丸 | 円
まる
まꜛる
[eng]
= circle
= entirety | whole | full | complete
= money | dough | moola
= enclosure inside a castle's walls
= soft-shelled turtle
= suffix for ship names | suffix for names of people (esp. infants) | suffix for
  names of swords, armour, musical instruments, etc. | suffix for names of dogs,
  horses, etc.
--> noun (common) (futsuumeishi) | noun, used as a prefix | suffix | slang |
    esp. 丸
see ○ | まる | スッポン | 麻呂
seq# 1216250, freq# 63, jlpt N3, prio; 1
<BLANKLINE>
<BLANKLINE>

>>> run("-v jmdict -m1 -w cat --verb")
DB v11 up to date.
query: +w cat
<BLANKLINE>
逆撫で | 逆なで
さかなで | ぎゃくなで
さꜛかなで
[eng]
= rubbing the wrong way (e.g. a cat) | irritating
--> noun (common) (futsuumeishi) | noun or participle which takes the aux. verb
    suru
~~> word containing irregular kana usage
seq# 1227180, freq# 30500; 1
<BLANKLINE>
<BLANKLINE>

>>> run("-v jmdict -m1 -w みる --noun")
DB v11 up to date.
query: +w みる
<BLANKLINE>
海松 | 水松
みる | すいしょう | ミル
みꜜる
[eng]
= stag seaweed (Codium fragile) | green sea fingers | dead man's fingers | felty
  fingers | forked felt-alga | sponge seaweed | green sponge | green fleece |
  oyster thief
--> noun (common) (futsuumeishi) | word usually written using kana alone
seq# 1772790, freq# 75; 1
<BLANKLINE>
<BLANKLINE>

>>> run("-v jmdict -m1 -w みる --noun --prio")
DB v11 up to date.
query: +w みる
<BLANKLINE>
<BLANKLINE>


=== Kanji ===

>>> run("kanji -m1 -w cat")
猫
ビョウ
ねこ
[no name readings]
= cat
<BLANKLINE>
<BLANKLINE>

>>> run("-v kanji -m1 -e cat")
DB v11 up to date.
query: += cat
<BLANKLINE>
猫
ビョウ
ねこ
[no name readings]
= cat
--> 猫 【ねこ】 | 子猫 【こねこ】 | 猫背 【ねこぜ】 |
    山猫 【やまねこ】 | 猫舌 【ねこじた】 | 野良猫 【のらねこ】 |
    黒猫 【くろねこ】 | 飼い猫 【かいねこ】 | 猫 【ねこま】 |
    猫撫で声 【ねこなでごえ】 | 猫又 【ねこまた】 | 招き猫 【まねきねこ】 |
    猫足 【ねこあし】 | 斑猫 【はんみょう】 | 猫かぶり 【ねこかぶり】 |
    海猫 【うみねこ】 | 猫柳 【ねこやなぎ】 | 猫板 【ねこいた】 |
    トラ猫 【トラねこ】 | 猫可愛がり 【ねこかわいがり】 |
    シャム猫 【シャムねこ】 | 猫娘 【ねこむすめ】 | どら猫 【どらねこ】 |
    メス猫 【メスねこ】 | 猫じゃらし 【ねこじゃらし】
部: 犬 (94) ⺨ 犯 田 艸 艹 艾 苗
variants: 貓
0x732b CJK UNIFIED IDEOGRAPH-732B; 1
11 strokes, level 常用, freq# 1702, old jlpt N2, jlpt N3, skip 1-3-8
<BLANKLINE>
<BLANKLINE>

>>> run("-v kanji -m1 -w 日")
DB v11 up to date.
query: +w 日
<BLANKLINE>
日
ニチ | ジツ
ひ | -び | -か
あ | あき | いる | く | くさ | こう | す | たち | に | にっ | につ | へ
= day | sun | Japan | counter for days
--> 日 【ひ】 | 日 【にち】 | 日本 【にほん】 | 今日 【きょう】 |
    日本人 【にほんじん】 | 毎日 【まいにち】 | 日米 【にちべい】 |
    同日 【どうじつ】 | 一日 【いちにち】 | 一日 【ついたち】 |
    日夜 【にちや】 | 明日 【あした】 | 来日 【らいにち】 |
    昨日 【きのう】 | 前日 【ぜんじつ】 | 日程 【にってい】 |
    日本語 【にほんご】 | 日中 【にっちゅう】 | 全日 【ぜんじつ】 |
    二十日 【はつか】 | 日常 【にちじょう】 | 翌日 【よくじつ】 |
    訪日 【ほうにち】 | 三十日 【さんじゅうにち】 | 三十日 【みそか】
部: 日 (72)
0x65e5 CJK UNIFIED IDEOGRAPH-65E5; 1
4 strokes, level 常用1, freq# 1, old jlpt N4, jlpt N5, skip 3-3-1
<BLANKLINE>
<BLANKLINE>

"""                                                             # }}}1

import os, sys

from .version import __version__, py_version
name = "jiten"

import click

from . import jmdict    as J
from . import kanji     as K
from . import misc      as M
from . import pitch     as P
from . import sentences as S

from .kana import with_romaji
from .misc import SERVER

HOST, PORT    = "localhost", 5000
MODS          = [K, P, S, J] # J last!
ANDROID_PRIV  = os.environ.get("ANDROID_PRIVATE") or None

def setup_db(verbose, dl = False):
  msg = "up to date"
  if not J.up2date():
    if dl or missing_data():
      msg = "downloaded"
      download_dbs()
    else:
      msg = "set up"
      for m in MODS: m.setup()
  if verbose:
    click.secho("DB v{} {}.".format(J.DBVERSION, msg), fg = "green")

def missing_data():
  for m in MODS:
    for f in m.DATA_FILES[1:]:
      if not os.path.exists(f): return True
  return False

def download_dbs():
  url = lambda x: "{}/_db/v{}/{}".format(SERVER, J.DBVERSION, x)
  for file in [ m.DATA_FILES[0] for m in MODS ]:
    fname = os.path.basename(file)
    base  = os.path.splitext(fname)[0]
    f     = os.path.join(ANDROID_PRIV, fname) if ANDROID_PRIV else file
    M.download_file(url(base), f, M.DB_SHA512SUMS[J.DBVERSION][base])
  if ANDROID_PRIV: android_link_dbs()

def android_link_dbs():
  for file in [ m.DATA_FILES[0] for m in MODS ]:
    f = os.path.join(ANDROID_PRIV, os.path.basename(file))
    if os.path.exists(f) and not os.path.islink(file):
      os.symlink(f, file)

@click.group(help = """
  jiten - japanese android/cli/web dictionary based on jmdict/kanjidic
""")
@click.option("-v", "--verbose", is_flag = True, help = "Be verbose.")
@click.option("-c", "--colour/--no-colour", is_flag = True,
              default = None, help = "Use terminal colours.")
@click.version_option(
  "{} [{}] [DB v{}]".format(__version__, py_version, J.DBVERSION),
  message = "%(prog)s 「辞典」 %(version)s"
)
@click.pass_context
def cli(ctx, colour, **kw):
  if colour is not None: ctx.color = colour
  ctx.obj = dict(kw)
  os.environ["PAGER"] = "less -FR"                              # TODO

@cli.command(help = "Search JMDict.")
@click.option("-l", "--lang", "langs", multiple = True,
              default = [J.LANGS[0]], metavar = "LANG",
              envvar = name.upper() + "_LANGS",
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
@click.option("-n", "--jlpt", type = M.JLPT_LEVEL,
              help = "Select entries by JLPT level(s); e.g. 1 or 3-5.")
@click.option("--romaji", is_flag = True, help = "Show romaji.")
@click.argument("query", required = False)
@click.pass_context
def jmdict(ctx, query, **kw):
  setup_db(ctx.obj["verbose"])
  ctx.obj.update(kw)
  if query:
    click.echo_via_pager(jmdict_search(query, **ctx.obj))
  else:
    while True:
      q = click.prompt("query", "", show_default = False).strip()
      if not q: break
      click.echo_via_pager(jmdict_search(q, **ctx.obj))

def jmdict_search(q, verbose, word, exact, fstwd, langs, romaji,
                  **kw):                                        # {{{1
  langs = [ l for ls in langs for l in ls.split(",") ]
  q     = M.process_query(q, word, exact, fstwd, True)
  w     = click.get_terminal_size()[0]
  f     = with_romaji if romaji else lambda x: x
  if verbose:
    yield "query: " + click.style(q, fg = "bright_red") + "\n\n"
  for i, (e, rank) in enumerate(J.search(q, langs = langs, **kw)):
    yield (" | ".join(
      click.style(k.elem, fg = "bright_yellow") for k in e.kanji
    ) or "[no kanji]") + "\n"
    yield (" | ".join(
      click.style(f(r.elem), fg = "bright_green") for r in e.reading
    ) or "[no readings]") + "\n"
    if P.have_pitch():
      yield (" | ".join(
        click.style(f(p), fg = "cyan") for p in e.pitch()
      ) or "[no pitch data]") + "\n"
    else:
      yield "[pitch data unavailable]\n"
    gloss, info = e.gloss_pos_info(langs)
    for l in langs:
      yield click.style("[" + l + "]", fg = "blue") + "\n"
      for g in gloss[l]:
        yield indent_and_wrap(w, g, "= ", "magenta")
    t = indent_and_wrap(w, info, "--> ", "green")
    if t: yield t
    if verbose:
      ti = indent_and_wrap(w, e.xinfo(), "~~> ", "blue")
      if ti: yield ti
      tx = indent_and_wrap(w, e.xrefs(), "see ", "yellow")
      if tx: yield tx
      yield  ("seq# " + click.style(str(e.seq), fg = "blue")
        + (", freq# " + click.style(str(rank ), fg = "cyan")
                    if rank else "")
        + (", jlpt " + click.style("N"+str(e.jlpt), fg = "yellow")
                    if e.jlpt else "")
        + (", prio" if e.isprio() else "") + "; " + str(i+1) + "\n")
    yield "\n"
                                                                # }}}1

# TODO: handle width properly!
def indent_and_wrap(w, xs, pre, fg):
  xs = list(xs)
  if not xs: return None
  t = click.wrap_text("| ".join(xs), w, initial_indent = pre,
    subsequent_indent = " " * len(pre)
  )[len(pre):].replace("|", click.style(" |", fg = fg))
  return click.style(pre, fg = fg) + t + "\n"

# TODO: currently only works for "猫 【ねこ】 | ..." etc.
def indent_and_wrap_jap(w, xs, pre, fg):
  xs = list(xs)
  if not xs: return None
  n = (w - 1 - len(pre)) // 2       # space for wide chars
  k = max(map(len, xs)) + 1         # width of longest word + sep
  w = len(pre) + n + (n // k * 2)   # 2 extra chars per word per line
  return indent_and_wrap(w, xs, pre, fg).replace("_【", " 【")

@cli.command(help = "Search kanji.")
@click.option("-w", "--word", is_flag = True,
              help = "Match whole word (same as \\b...\\b).")
@click.option("-1", "--1stword", "--first-word", "fstwd", is_flag = True,
              help = "Match first word (same as ^...\\b).")
@click.option("-e", "--exact", is_flag = True,
              help = "Match exactly (same as ^...$).")
@click.option("-m", "--max", "max_results", default = None,
              type = click.INT, help = "Maximum number of results.")
@click.option("--romaji", is_flag = True, help = "Show romaji.")
@click.argument("query", required = False)
@click.pass_context
def kanji(ctx, query, **kw):
  setup_db(ctx.obj["verbose"])
  ctx.obj.update(kw)
  if query:
    click.echo_via_pager(kanji_search(query, **ctx.obj))
  else:
    while True:
      q = click.prompt("query", "", show_default = False).strip()
      if not q: break
      click.echo_via_pager(kanji_search(q, **ctx.obj))

def kanji_search(q, verbose, word, exact, fstwd, max_results,
                 romaji):                                       # {{{1
  q = M.process_query(q, word, exact, fstwd, True)
  w = click.get_terminal_size()[0]
  f = with_romaji if romaji else lambda x: x
  if verbose:
    yield "query: " + click.style(q, fg = "bright_red") + "\n\n"
  for i, e in enumerate(K.search(q, max_results)):
    yield e.char + "\n"
    yield (" | ".join(
      click.style(f(r), fg = "bright_yellow") for r in e.on
    ) or "[no on readings]") + "\n"
    yield (" | ".join(
      click.style(f(r), fg = "bright_green") for r in e.kun
    ) or "[no kun readings]") + "\n"
    yield (" | ".join(
      click.style(f(r), fg = "cyan") for r in e.nanori
    ) or "[no name readings]") + "\n"
    if e.meaning:
      yield click.style("= ", fg = "magenta") + \
        click.style(" | ", fg = "magenta").join(e.meaning) + "\n"
    else:
      yield "[no meanings]\n"
    if verbose:
      js = ( "{}_【{}】".format(e.kanji[0].elem, e.reading[0].elem)
             for e, r in e.jmdict() )
      tj = indent_and_wrap_jap(w, js, "--> ", "blue")
      if tj: yield tj
      co = " ".join(e.components())
      yield "部: {} ({})".format(e.radical(), e.rad) \
        + (co and " " + co) + "\n"
      ca = e.canonical()
      tv = (["canonical: " + ca] if ca != e.char else []) \
         + (["variants: " + " ".join(e.var)] if e.var else [])
      if tv: yield ", ".join(tv) + "\n"
      yield (click.style(hex(ord(e.char)), fg = "blue")
        + " " + click.style(e.name(), fg = "cyan")
        + "; " + str(i+1) + "\n"
        + click.style(str(e.strokes), fg = "yellow")
        + " strokes"
        + (", level " + click.style(e.level, fg = "cyan")
           if e.level else "")
        + (", freq# " + click.style(str(e.freq), fg = "magenta")
           if e.freq else "")
        + (", old jlpt " + click.style("N"+str(e.jlpt), fg = "blue")
           if e.jlpt else "")
        + (", jlpt " + click.style("N"+str(e.new_jlpt), fg = "cyan")
           if e.new_jlpt else "")
        + (", skip " + click.style(e.skip, fg = "yellow")
           if e.skip else "") + "\n")
    yield "\n"
                                                                # }}}1

@cli.command(help = "Search Tatoeba example sentences.")
@click.option("-l", "--lang", "langs", multiple = True,
              default = [], metavar = "LANG",
              envvar = name.upper() + "_LANGS",
              help = "Filter language(s) ("+", ".join(S.LANGS)+").")
@click.option("-m", "--max", "max_results", default = None,
              type = click.INT, help = "Maximum number of results.")
@click.argument("query", required = False)
@click.pass_context
def sentences(ctx, query, **kw):
  setup_db(ctx.obj["verbose"])
  ctx.obj.update(kw)
  if query:
    click.echo_via_pager(sentence_search(query, **ctx.obj))
  else:
    while True:
      q = click.prompt("query", "", show_default = False).strip()
      if not q: break
      click.echo_via_pager(sentence_search(q, **ctx.obj))

# TODO: audio
def sentence_search(q, verbose, langs, max_results):            # {{{1
  q = q.strip()
  if verbose:
    yield "query: " + click.style(q, fg = "bright_red") + "\n\n"
  for i, e in enumerate(S.search(q, langs, max_results)):
    yield click.style("[jap] ", "bright_yellow") + e.jap + "\n"
    for l in S.LANGS:
      x = getattr(e, l)
      yield (click.style("["+l+"] ", fg = "bright_green") + x if x
             else "[no "+l+"]") + "\n"
    if verbose:
      yield "tatoeba #" + str(e.id) + "; " + str(i+1) + "\n"
    yield "\n"
                                                                # }}}1

@cli.command(help = "Serve the web interface.")
@click.option("-h", "--host", default = HOST, metavar = "HOST",
              help = "Host to listen on.", show_default = True)
@click.option("-p", "--port", default = PORT, metavar = "PORT",
              help = "Port to listen on.", show_default = True,
              type = click.INT)
@click.pass_context
def serve(ctx, host, port):
  serve_app(host, port, ctx.obj["verbose"])

def serve_app(host = HOST, port = PORT, verbose = True, **opts):
  from .app import app
  if ANDROID_PRIV:
    android_link_dbs()
    app.config["DBS_UP2DATE"]   = J.up2date()
    app.config["DOWNLOAD_DBS"]  = download_dbs
  else:
    setup_db(verbose)
  app.run(host = host, port = port, load_dotenv = False, **opts)

@cli.command(help = """
  WebView GUI.  Wraps the web interface.  Requires pywebview.
""")
@click.argument("link", required = False)
@click.pass_context
def gui(ctx, link):
  setup_db(ctx.obj["verbose"])
  from .gui import start
  start(link)

@cli.command(help = "Build (or download) sqlite databases.")
@click.option("--download", is_flag = True,
              help = "Always download DBs, never build them.")
def setup(download):
  click.echo("Creating databases...")
  setup_db(True, download)

@cli.command("_doctest", hidden = True)
@click.pass_context
def doctest(ctx):
  setup_db(ctx.obj["verbose"])
  import doctest
  if doctest.testmod(verbose = ctx.obj["verbose"])[0]: ctx.exit(1)

if __name__ == "__main__":
  try:
    cli(prog_name = name)
  except M.RegexError as e:
    click.echo("regex error: " + str(e), err = True)
    sys.exit(1)

# vim: set tw=70 sw=2 sts=2 et fdm=marker :
