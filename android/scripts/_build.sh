#!/bin/bash

######################################################################
#
# Usage:
#   android/scripts/_build.sh USER@HOST TARGET...
#
# Example:
#   android/scripts/_build.sh build@HOST clean {debug,release}-arm64-v8a
#
# NB:
#   assumes setup-root.sh packages installed
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
ssh "$remote" 'rm -fr jiten && git clone _jiten.git jiten'

# setup & build
ssh "$remote" '
  set -e && cd jiten/android
  export PATH="$HOME/.local/bin:$PATH"
  ./scripts/setup-user.sh
  for target in '"$*"'; do make "$target" || exit $?; done
'

# show shasums
ssh "$remote" '
  set -e && cd jiten/android/bin
  sha1sum *.apk && sha256sum *.apk && sha512sum *.apk
'

# copy APKs
mkdir -p tmp/_build
scp "$remote:jiten/android/bin/*.apk" tmp/_build/
