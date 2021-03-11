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
#   assumes setup-root.sh packages installed
#
######################################################################

set -xe
test "$#" -ge 2

remote="$1"; shift
branch="$( git branch --show-current )"

android_dir=.buildozer/android/platform
android_repo=https://dl.google.com/android/repository
ndk_dir=android-ndk-r22
ndk="$ndk_dir-linux-x86_64.zip"
ndk_sha512=0bef6fdd80f7ceb8a9e1390ff8cfbbe0342d821a692cf26c1928e44ba3164284d8dbfc6669f16b2044a6a44b5bbd335d974db17d7893feecdd5a93770c78550f

# test
if [ "$( ssh "$remote" 'echo OK' || true )" != OK ]; then
  echo 'not OK' 2>&1
  exit 1
fi

# cache ndk
if ! ssh "$remote" "test -d $android_dir/$ndk_dir"; then
  if ! test -e tmp/"$ndk"; then
    mkdir -p tmp
    wget -O tmp/"$ndk" -- "$android_repo/$ndk"
    sha512sum -c <<< "$ndk_sha512  tmp/$ndk"
  fi
  ssh "$remote" "mkdir -p $android_dir"
  scp tmp/"$ndk" "$remote:$android_dir/"
  ssh "$remote" "cd $android_dir && unzip $ndk"
fi

# push
ssh "$remote" 'test -e _jiten.git || git init --bare _jiten.git'
git push -f "$remote":_jiten.git "$branch":master --tags

# clone
ssh "$remote" '
  set -e
  rm -fr build
  git clone _jiten.git build/dev.obfusk.jiten
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
mkdir -p tmp/_build
scp "$remote:build/dev.obfusk.jiten/android/bin/*.apk" tmp/_build/
