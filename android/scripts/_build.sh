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
#   installed (& umask 022)
#
# TODO:
#   * override PIP_INSTALL?
#
######################################################################

set -xe

test "$#" -ge 2
remote="$1"; shift
branch="$( git branch --show-current )"

# push
ssh "$remote" 'test -e _jiten.git || git init --bare _jiten.git'
git push -f "$remote":_jiten.git "$branch":master --tags

# clone
ssh "$remote" 'mkdir -p work/jiten && \
  rm -fr work/jiten/jiten && git clone _jiten.git work/jiten/jiten'

# setup & build
ssh "$remote" 'cd work/jiten/jiten && \
  export PATH="$HOME/.local/bin:$PATH" && \
  make -C android _setup_user PIP_INSTALL="pip3 install --user" && \
  for target in '"$*"'; do make -C android "$target" || exit $?; done'

# show shasums
ssh "$remote" 'cd work/jiten/jiten/android/bin && \
  sha1sum *.apk && sha256sum *.apk && sha512sum *.apk'

# copy APKs
mkdir -p tmp/_build
scp "$remote:work/jiten/jiten/android/bin/*.apk" tmp/_build/
