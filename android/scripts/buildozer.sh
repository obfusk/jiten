#!/bin/bash
set -xe
mkdir -p ../../_jiten_buildozer_
buildozer android p4a -- --version  # install requirements
cat patches/*.patch | ( cd .p4a && patch -N -r- -p1 )
exec buildozer android "$@"
