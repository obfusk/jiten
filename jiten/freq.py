#!/usr/bin/python3
# encoding: utf-8

# --                                                            ; {{{1
#
# File        : jiten/freq.py
# Maintainer  : Felix C. Stegerman <flx@obfusk.net>
# Date        : 2020-08-19
#
# Copyright   : Copyright (C) 2020  Felix C. Stegerman
# Version     : v0.3.0
# License     : AGPLv3+
#
# --                                                            ; }}}1

                                                                # {{{1
r"""

Word frequencies.

>>> len(news_freq)
142193
>>> len(book_freq)
89222

>>> most_freq_kanji = "人一日大年出本中子見"
>>> some_words = '''ブログ について 日 人 日本 学校 問題 世界 大学
...                 見る する として 場所 場合 女性 時間 必要 放送
...                 という 情報 可愛い 猫 事件 自分 使う 馬鹿 出来る
...                 歴史 可能 アニメ 英語 ロボット'''
>>> [ w+" "+str(rank(w)) for w in most_freq_kanji ]
['人 22', '一 59', '日 21', '大 98', '年 33', '出 5145', '本 162', '中 47', '子 147', '見 17675']
>>> [ w+" "+str(rank(w)) for w in some_words.split() ]
['ブログ 999999', 'について 89', '日 21', '人 22', '日本 52', '学校 444', '問題 86', '世界 148', '大学 358', '見る 54', 'する 8', 'として 187', '場所 426', '場合 250', '女性 210', '時間 140', '必要 180', '放送 726', 'という 45', '情報 345', '可愛い 4036', '猫 2201', '事件 200', '自分 71', '使う 197', '馬鹿 2472', '出来る 504', '歴史 860', '可能 711', 'アニメ 20625', '英語 2371', 'ロボット 6291']

"""                                                             # }}}1

import sys

from collections import defaultdict
from fractions import Fraction

from . import misc as M

NEWSFREQ_FILE   = M.resource_path("res/freq/wordfreq_ck.utf8")
BOOKFREQ_FILE   = M.resource_path("res/freq/base_aggregates.txt.nobom")

EXCEPTIONS      = "Tシャツ".split()
NOFREQ          =  999999
MAXFREQ         = 1000000

# TODO
# * is isokjap OK?
def parse_freq(file, word_first):                               # {{{1
  data = {}
  with open(file) as f:
    for line in f:
      if line.startswith("#") or not line.strip(): continue
      fields      = line.split("\t")[:2]
      word, freq  = fields if word_first else fields[::-1]
      freq        = int(freq)
      if word and (word in EXCEPTIONS or M.isokjap(word)):
        assert word not in data or data[word] == freq
        data[word] = freq
  return data
                                                                # }}}1

def process_freq(data):
  tot, data_ = sum(data.values()), {}
  for k, v in data.items(): data_[k] = Fraction(v, tot)
  return data_

def merge_freq(*fs):
  data = defaultdict(Fraction)
  for f in fs:
    for k, v in f.items(): data[k] += v
  return dict(data)

def rank_freq(data):
  d = dict( (k,float(v)) for k, v in data.items() )
  l = sorted(d, key = lambda k: (d[k], k), reverse = True)
  return dict( (x,i) for i, x in enumerate(l, 1) )

def rank(w): return freq_rank.get(w, NOFREQ)

def setup():
  global news_freq, book_freq, freq, freq_rank
  if setup.done: return
  setup.done = True

  news_freq = process_freq(parse_freq(NEWSFREQ_FILE, True))
  book_freq = process_freq(parse_freq(BOOKFREQ_FILE, False))

  freq      = merge_freq(news_freq, book_freq)
  freq_rank = rank_freq(freq)
setup.done = False

if __name__ == "__main__":
  if "--doctest" in sys.argv:
    verbose = "--verbose" in sys.argv
    setup()
    import doctest
    if doctest.testmod(verbose = verbose)[0]: sys.exit(1)

# vim: set tw=70 sw=2 sts=2 et fdm=marker :
