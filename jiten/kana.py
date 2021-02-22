#!/usr/bin/python3
# encoding: utf-8

# --                                                            ; {{{1
#
# File        : jiten/kana.py
# Maintainer  : Felix C. Stegerman <flx@obfusk.net>
# Date        : 2021-02-07
#
# Copyright   : Copyright (C) 2021  Felix C. Stegerman
# Version     : v0.4.0
# License     : AGPLv3+
#
# --                                                            ; }}}1

                                                                # {{{1
r"""

Kana conversion functions.

>>> kana2romaji("いかなきゃ")
'ikanakya'
>>> kana2romaji("フェリックス")
'ferikkusu'
>>> kana2romaji("ヴァイオリン")
'vaiorinn'
>>> kana2romaji("ウヰスキー")
'uwisukii'
>>> kana2romaji("コース")
'koosu'

>>> kana2romaji("こんにちは")
'konnnichiha'
>>> kana2romaji("ウィルス")
'uxirusu'
>>> kana2romaji("こうちゃ")
'koucha'

>>> kana2romaji("し じ ち つ ふ")
'shi ji chi tsu fu'
>>> kana2romaji("ゃ ゎ っ")
'xya xwa xtsu'
>>> kana2romaji("なっちゃう")
'nacchau'


>>> romaji2hiragana("ikanakya")
'いかなきゃ'
>>> romaji2katakana("ferikkusu")
'フェリックス'
>>> romaji2katakana("vaiorinn")
'ヴァイオリン'
>>> romaji2katakana("uwisuki-")
'ウヰスキー'
>>> romaji2katakana("ko-su")
'コース'

>>> romaji2hiragana("konnnichiha")
'こんにちは'
>>> romaji2katakana("uxirusu")
'ウィルス'
>>> romaji2hiragana("koucha")
'こうちゃ'

>>> romaji2hiragana("shi ji chi tsu fu")
'し じ ち つ ふ'
>>> romaji2hiragana("xya xwa xtsu")
'ゃ ゎ っ'
>>> romaji2hiragana("nacchau")
'なっちゃう'

"""                                                             # }}}1

import re, sys

from functools import reduce

from . import misc as M

def with_romaji(s, long = False):
  return "{} [{}]".format(s, kana2romaji(s, long))

def kana2romaji(s, long = False):
  if long: s = s.replace("ー", "-")
  return "".join( PMOR.get(x, x) for x in _kana2romaji(s) )

def _kana2romaji(s):
  return reduce(_k2r_f, map(_k2r_lookup, s), [])

# TODO
def _k2r_f(t, x):
  u, v = t[:], []
  while u and u[-1] in "ꜛꜜ": v.append(u.pop())
  w, y = _k2r_g(u, x)
  return w + v[::-1] + [y]

# TODO
def _k2r_g(t, x):
  if not t: return (t, x)
  *ti, tl = t
  if x[:2] == "xy" and tl[-1] == "i":
                      return (ti, tl[:-1] + x[1:])
  elif tl == "xtu" and isroma(x) and x not in ".-":
                      return (ti, x[0] + x)
  elif x[0] == "x" and len(x) == 2 and x != "xu":
    if tl == "hu":    return (ti, "f" + x[1])
    elif tl == "vu":  return (ti, "v" + x[1])
  elif x == "ー":     return (t , tl[-1]) # .replace("o", "u")
  elif x in "ゝヽ":   return (t , tl)
  elif x in "ゞヾ":   return (t , voiced(tl))
  return (t, x)

# TODO
def _k2r_lookup(c):
  if "a" <= c.lower() <= "z":
    raise ValueError("kana2romaji: ascii letter in input")
  if not M.iskana1(c) or c in "ー・ヶゝゞヽヾ": return c
  i = (HIRAGANA if M.ishiragana1(c) else KATAKANA).index(c)
  return (COLS[i // 5] + ROWS[i % 5]).replace("-", "")

def hiragana2katakana(t, long = False):
  return "".join(_h2k(t, long))

def _h2k(t, long = False):                                      # {{{1
  col = None
  for c in t:
    if c in HIRAGANA:
      i = HIRAGANA.index(c)
      o = col == 4 and i == 2
      k = "ー" if long and (i == col or o) else KATAKANA[i]
      if not o: col = i % 5
      yield k
    else:
      col = None
      yield c
                                                                # }}}1

def katakana2hiragana(t):
  return "".join( HIRAGANA[KATAKANA.index(c)] if c in KATAKANA else c
                  for c in t )

def romaji2hiragana(t):
  return "".join(_r2h(t))

# TODO: ヴャ, punctuation?!
def _r2h(t):                                                    # {{{1
  i, rx = 0, re.compile(RORX)
  while True:
    m = rx.match(t, i)
    if not m: break
    g, i = (m.group(0),) + m.groups(), m.end()
    if g[1] or g[4]:
      yield g[4] or ROSP["nn" if g[1] == "n" else g[1]]
    elif len(g[0]) == 1:
      yield HIRAGANA[ROWS.index(g[0])]
    else:
      s, x = "", (ROMP[g[2]] if g[2] else g[0])
      if x[0] == x[1]:
        s, x = "っ", x[1:]
      try:
        if len(x) == 3 and x[1] == "y" and x[0] != "x":
          s += HIRAGANA[5*COLS.index(x[0])+1] \
             + HIRAGANA[5*(COLS.index("y")+1)+ROWS.index(x[2])]
        else:
          s += HIRAGANA[5*COLS.index(x[:-1])+ROWS.index(x[-1])]
      except (KeyError, ValueError):
        yield g[0]                                              # TODO
      else:
        yield g[0] if "〇" in s else s                          # TODO
                                                                # }}}1

def romaji2katakana(t, long = False):
  return hiragana2katakana(romaji2hiragana(t), long)

# TODO
def voiced(x): return COLS_[COLS_.index(x[0])+1]+x[1:]

def isroma(t): return bool(t) and all( c in ROMA for c in t )

# KANA TABLES                                                   # {{{1
HIRAGANA = """
  あ   い う   え   お
  ぁ   ぃ ぅ   ぇ   ぉ
ゔぁ ゔぃ ゔ ゔぇ ゔぉ
  か   き く   け   こ
  が   ぎ ぐ   げ   ご
  さ   し す   せ   そ
  ざ   じ ず   ぜ   ぞ
  た   ち つ   て   と
  だ   ぢ づ   で   ど
  〇   〇 っ   〇   〇
  な   に ぬ   ね   の
  は   ひ ふ   へ   ほ
  ば   び ぶ   べ   ぼ
  ぱ   ぴ ぷ   ぺ   ぽ
ふぁ ふぃ ふ ふぇ ふぉ
  ま   み む   め   も
  や   〇 ゆ   〇   よ
  ゃ   〇 ゅ   〇   ょ
  ら   り る   れ   ろ
  わ   ゐ 〇   ゑ   を
  ゎ   〇 〇   〇   〇
  ん   〇 〇   〇   〇
  ゝ   ゞ 〇   〇   〇
""".split()

KATAKANA = """
  ア   イ ウ   エ   オ
  ァ   ィ ゥ   ェ   ォ
ヴァ ヴィ ヴ ヴェ ヴォ
  カ   キ ク   ケ   コ
  ガ   ギ グ   ゲ   ゴ
  サ   シ ス   セ   ソ
  ザ   ジ ズ   ゼ   ゾ
  タ   チ ツ   テ   ト
  ダ   ヂ ヅ   デ   ド
  〇   〇 ッ   〇   〇
  ナ   ニ ヌ   ネ   ノ
  ハ   ヒ フ   ヘ   ホ
  バ   ビ ブ   ベ   ボ
  パ   ピ プ   ペ   ポ
ファ フィ フ フェ フォ
  マ   ミ ム   メ   モ
  ヤ   〇 ユ   〇   ヨ
  ャ   〇 ュ   〇   ョ
  ラ   リ ル   レ   ロ
  ワ   ヰ 〇   ヱ   ヲ
  ヮ   〇 〇   〇   〇
  ン   〇 〇   〇   〇
  ヽ   ヾ 〇   〇   〇
""".split()
                                                                # }}}1

ROWS, COLS_ = "aiueo", "-xvkgsztdTnhbpfmyYrwWN-"
COLS  = [ "x" + c.lower() if c in "TYW" else c for c in COLS_ ]

ROMP_ = dict(
  shi =  "si",  ji =  "zi", chi =  "ti", tsu = "tu", xtsu = "xtu",
  sha = "sya", sho = "syo", shu = "syu",
   ja = "zya",  jo = "zyo",  ju = "zyu",
  cha = "tya", cho = "tyo", chu = "tyu",
   fu =  "hu",
)
ROMP  = { **ROMP_, **{ k[0]+k : v[0]+v for k, v in ROMP_.items()
                                       if not k[0] == "x" } }
PMOR  = { v: k for k, v in ROMP.items() }
PMOR.update(Na = "nn", NNa = "xtsunn")

COLS2 = COLS[1:-2] + [ x[0]+x for x in COLS[1:-2] if x[0] != "x" ]

ROSP  = { "nn":"ん", "-":"ー", "~":"〜", ",":"、", ".":"。", "?":"？",
          "!":"！", "(":"（", ")":"）" }                        # TODO

RORX  = r"(" + r"|".join(map(re.escape, ROSP.keys())) \
             + r"|n(?![aiueoy]))|" + \
        r"(" + r"|".join(reversed(sorted(ROMP.keys()))) + r")|" + \
        r"(" + r"|".join(reversed(sorted(COLS2))) + r")?y?" \
             + r"[" + ROWS + r"]|(.)"

ROMA  = frozenset(ROWS + COLS_.lower() + "".join(ROMP.keys())
                                       + "".join(ROSP.keys()))

if __name__ == "__main__":
  if "--doctest" in sys.argv:
    verbose = "--verbose" in sys.argv
    import doctest
    if doctest.testmod(verbose = verbose)[0]: sys.exit(1)

# vim: set tw=70 sw=2 sts=2 et fdm=marker :
