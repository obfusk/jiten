#!/bin/bash
set -xe
mkdir -p ../../_jiten_buildozer_
buildozer android p4a -- --version  # install requirements
dir="$PWD" p=( patch -N -r- -p1 )
(
  cd .p4a
  for f in "$dir"/patches/*.patch; do
    ! "${p[@]}" --dry-run < "$f" | grep -iF failed
    "${p[@]}" < "$f" || true
  done
)
exec buildozer android "$@"
