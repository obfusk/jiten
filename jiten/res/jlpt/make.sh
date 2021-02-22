#!/bin/bash
set -e
tab=$'\t'
for i in {1..5}; do
  url="https://www.tanos.co.uk/jlpt/jlpt$i/kanji"
  kan="n$i-kanji-char-eng.anki"
  [ -e "$kan" ] || wget -- "$url/$kan"
  sqlite3 "$kan" <<__EOF | sort | tr -d '\n' > "N$i-kanji"
    SELECT value FROM fields WHERE ordinal = 0
__EOF
  echo >> "N$i-kanji"
done
for i in {1..5}; do
  url="https://www.tanos.co.uk/jlpt/jlpt$i/vocab"
  hir="n$i-vocab-kanji-hiragana.anki"
  eng="n$i-vocab-kanji-eng.anki"
  [ -e "$hir" ] || wget -- "$url/$hir"
  [ -e "$eng" ] || wget -- "$url/$eng"
  sqlite3 "$hir" <<__EOF | sort > "N$i-vocab-hiragana"
    SELECT a.value || '$tab' || b.value
    FROM fields AS a INNER JOIN fields AS b
    ON a.ordinal = 0 AND b.ordinal = 1 AND a.factId = b.factId
__EOF
  sqlite3 "$eng" <<__EOF | sort > "N$i-vocab-eng"
    SELECT value FROM fields WHERE ordinal = 0
__EOF
done
