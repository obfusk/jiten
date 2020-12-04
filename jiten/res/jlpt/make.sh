#!/bin/bash
for i in {1..5}; do
  wget -- "https://www.tanos.co.uk/jlpt/jlpt$i/vocab/n$i-vocab-kanji-eng.anki"
  sqlite3 n$i-vocab-kanji-eng.anki \
    'SELECT value FROM fields WHERE ordinal = 0' \
    | sort > N$i-vocab
done
