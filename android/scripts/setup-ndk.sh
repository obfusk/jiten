#!/bin/bash
set -xe -o pipefail
ndk_vsn=r22b
ndk_rev=22.1.7171670
ndk_sha512=6f7e52ef68b2ab465d43e0392e21fb0eecc33c5bea29ee8bdfbf47754bb90f9abf9aaf48eee0bb94b763852055586756238398ba0d0bbf2a2380cc60840adec7
android_repo=https://dl.google.com/android/repository
ndk="android-ndk-$ndk_vsn-linux-x86_64"

[ -e "$ndk.zip" ] || wget -O "$ndk.zip" -- "$android_repo/$ndk.zip"
printf "$ndk_sha512  $ndk.zip\n" | sha512sum -c
unzip -q "$ndk.zip"
rm "$ndk.zip"
mkdir -p /opt/android-sdk/ndk
mv "android-ndk-$ndk_vsn" "/opt/android-sdk/ndk/$ndk_rev"
