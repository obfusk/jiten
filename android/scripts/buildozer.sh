#!/bin/bash
set -xe
commit="$( < p4a-commit )"

mkdir -p ../../_jiten_buildozer_
buildozer android p4a -- --version  # install requirements

dir="$PWD" p=( patch -N -r- -p1 )
(
  cd .p4a
  git status ; git checkout -- . ; git clean -f ; git status
  git fetch --all ; git reset --hard "$commit"  # pin p4a commit
  for f in "$dir"/patches/*.patch; do
    echo "applying patch $(basename "$f") ..."
    err="$( "${p[@]}" --dry-run < "$f" 2>&1 | grep -iF failed || true )"
    [ "$err" = "" ] || { echo FAILED; false; }
    "${p[@]}" < "$f" || true
  done
)

exec buildozer android "$@"
