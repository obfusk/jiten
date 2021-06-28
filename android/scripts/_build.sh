#!/bin/bash

######################################################################
#
# Usage:
#   android/scripts/_build.sh USER@HOST TARGET...
#
# Example:
#   android/scripts/_build.sh vagrant@HOST clean {debug,release}-arm64-v8a
#
# NB:
#   assumes setup-{root,python,sqlite}.sh has been run
#
######################################################################

set -xe
test "$#" -ge 2

remote="$1"; shift
branch="$( git branch --show-current )"
ndk_vsn=r22b
ndk_rev=22.1.7171670

# test
if [ "$( ssh "$remote" 'echo OK' || true )" != OK ]; then
  echo 'not OK' 2>&1
  exit 1
fi

# cache ndk
if ! ssh "$remote" "test -d /opt/android-sdk/ndk/$ndk_rev"; then
  if test -e tmp/android-ndk-$ndk_vsn-linux-x86_64.zip; then
    scp tmp/android-ndk-$ndk_vsn-linux-x86_64.zip "$remote:"
  fi
  scp android/scripts/setup-ndk.sh "$remote:"
  ssh "$remote" ./setup-ndk.sh
fi

# push
ssh "$remote" 'test -e _jiten.git || git init --bare _jiten.git'
git push -f "$remote":_jiten.git "$branch":master --tags

# clone
ssh "$remote" '
  set -e
  rm -fr build
  git clone --recurse-submodules _jiten.git build/dev.obfusk.jiten
'

# setup & build
ssh "$remote" '
  set -e && cd build/dev.obfusk.jiten/android
  export PATH=/usr/local/bin:/bin:/usr/bin
  if grep -q stretch /etc/os-release; then
    [ -e ~/env ] || python3.7 -mvenv ~/env
    source ~/env/bin/activate
    PIP_INSTALL="pip3 install" ./scripts/setup-user.sh
  else
    export PATH="$HOME/.local/bin:$PATH"
    PIP_INSTALL="pip3 install --user" ./scripts/setup-user.sh
  fi
  for target in '"$*"'; do
    if [ "$target" = clean ]; then
      make "$target" || true
    else
      make "$target"
    fi
  done
'

# show shasums
ssh "$remote" '
  set -e && cd build/dev.obfusk.jiten/android/bin
  sha1sum *.apk && sha256sum *.apk && sha512sum *.apk
'

# copy APKs
mkdir -p tmp/_build/"$remote"
scp "$remote:build/dev.obfusk.jiten/android/bin/*.apk" tmp/_build/"$remote"/
