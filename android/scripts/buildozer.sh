#!/bin/bash
set -e
mkdir -p ../../_jiten_buildozer_
buildozer android p4a -- --version  # install requirements
./scripts/patch.py
exec buildozer android "$@"
