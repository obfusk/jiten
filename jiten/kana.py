#!/usr/bin/python3
# encoding: utf-8

# --                                                            ; {{{1
#
# File        : jiten/kana.py
# Maintainer  : Felix C. Stegerman <flx@obfusk.net>
# Date        : 2021-01-21
#
# Copyright   : Copyright (C) 2021  Felix C. Stegerman
# Version     : v0.3.5
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
'kousu'

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

"""                                                             # }}}1

import sys

from functools import reduce

from . import misc as M

def with_romaji(s):
  return "{} [{}]".format(s, kana2romaji(s))

def kana2romaji(s):
  return "".join( PMOR.get(x, x) for x in _kana2romaji(s) )

def _kana2romaji(s):
  return reduce(_k2r_f, map(_k2r_lookup, s), [])

# TODO
def _k2r_f(t, x):
  if not t: return [x]
  *ti, tl = t
  if x[:2] == "xy":   return ti + [tl[:-1] + x[1:]]
  elif tl == "xtu":   return ti + [x[0] + x]
  elif x[0] == "x":
    if tl == "hu":    return ti + ["f" + x[1]]
    elif tl == "vu":  return ti + ["v" + x[1]]
  elif x == "ー":     return ti + [tl + tl[-1].replace("o", "u")]
  return t + [x]

# TODO
def _k2r_lookup(c):
  if "a" <= c.lower() <= "z":
    raise ValueError("kana2romaji: ascii letter in input")
  if not M.iskana1(c) or c in "ー・ヶ": return c
  i = (HIRAGANA if M.ishiragana1(c) else KATAKANA).index(c)
  return (COLS[i // 5] + ROWS[i % 5]).replace("-", "")

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
COLS = [ "x" + c.lower() if c in "TYW" else c for c in COLS_ ]
ROMP = dict(
  shi =  "si",  ji =  "zi", chi =  "ti", tsu = "tu", xtsu = "xtu",
  sha = "sya", sho = "syo", shu = "syu",
   ja = "zya",  jo = "zyo",  ju = "zyu",
  cha = "tya", cho = "tyo", chu = "tyu",
   fu =  "hu",
)
PMOR = { v: k for k, v in ROMP.items() }; PMOR.update(Na = "nn")

if __name__ == "__main__":
  if "--doctest" in sys.argv:
    verbose = "--verbose" in sys.argv
    import doctest
    if doctest.testmod(verbose = verbose)[0]: sys.exit(1)

# vim: set tw=70 sw=2 sts=2 et fdm=marker :
