#!/bin/bash

######################################################################
#
# Usage:
#   android/scripts/_build.sh USER@HOST TARGET...
#
# Example:
#   android/scripts/_build.sh runner@HOST clean {debug,release}-arm64-v8a
#
# NB:
#   assumes a (ubuntu LTS) host w/ _setup_root packages + python3-pip
#   installed
#
# TODO:
#   * specify branch != master?
#   * force push?
#   * override PIP_INSTALL?
#
######################################################################

set -xe
test "$#" -ge 2
remote="$1"; shift

# push
ssh "$remote" 'test -e jiten.git || git init --bare jiten.git'
git push "$remote":jiten.git master --tags

# clone
ssh "$remote" 'mkdir -p work/jiten && \
  rm -fr work/jiten/jiten && git clone jiten.git work/jiten/jiten'

# setup & build
ssh "$remote" 'cd work/jiten/jiten && \
  export PATH="$HOME/.local/bin:$PATH" && \
  make -C android _setup_user PIP_INSTALL="pip3 install --user" && \
  for target in '"$*"'; do make -C android "$target"; done'

# copy APKs
mkdir -p tmp/_build
scp "$remote:work/jiten/jiten/android/bin/*.apk" tmp/_build/
