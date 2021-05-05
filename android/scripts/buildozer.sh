#!/bin/bash
set -xe -o pipefail
commit="$( < p4a-commit )"
urls=(
  https://github.com/pallets/click/archive/7.1.2.zip
  https://github.com/pallets/flask/archive/1.1.2.zip
  https://www.python.org/ftp/python/3.9.5/Python-3.9.5.tgz
  https://github.com/libffi/libffi/archive/v3.3.tar.gz
  https://ftp.pcre.org/pub/pcre/pcre-8.44.tar.bz2
  https://www.openssl.org/source/openssl-1.1.1k.tar.gz
  https://github.com/kivy/pyjnius/archive/1.3.0.zip
  https://www.python.org/ftp/python/3.9.5/Python-3.9.5.tgz
  https://pypi.python.org/packages/source/s/setuptools/setuptools-56.0.0.tar.gz
  https://pypi.python.org/packages/source/s/six/six-1.15.0.tar.gz
  https://www.sqlite.org/2021/sqlite-amalgamation-3350500.zip
)
sums=(
  'f4c96399ed484c77c35ca81b53fb9c4b4175eb88bafb078ce2518d2ddb2452928bbb13596d4042d2e97c0a7191ce9d9b6c1cc22bd992e8013fdbf75e5f91441e  click/7.1.2.zip'
  '0b96c822c1641d9a464211605f16585e6f14989cea0919b2d0c0f87a421fc35100e608dfb7fce03f5ffb345e9ff511d2c28ce52603a4d6e454e8a4329cf973c6  flask/1.1.2.zip'
  '06e5664ae097ceae0e1499839c567bf8c41140a50d002213623d7fdac644f637701dbeca10ddf147840e932d57c9521b7fc1c0095b068d0aa491192249ee9c1c  hostpython3/Python-3.9.5.tgz'
  '62798fb31ba65fa2a0e1f71dd3daca30edcf745dc562c6f8e7126e54db92572cc63f5aa36d927dd08375bb6f38a2380ebe6c5735f35990681878fc78fc9dbc83  libffi/v3.3.tar.gz'
  'f26d850aab5228799e58ac8c2306fb313889332c39e29b118ef1de57677c5c90f970d68d3f475cabc64f8b982a77f04eca990ff1057f3ccf5e19bd137997c4ac  libpcre/pcre-8.44.tar.bz2'
  '73cd042d4056585e5a9dd7ab68e7c7310a3a4c783eafa07ab0b560e7462b924e4376436a6d38a155c687f6942a881cfc0c1b9394afcde1d8c46bf396e7d51121  openssl/openssl-1.1.1k.tar.gz'
  '5a3475afcda5afbef6e1a67bab508e3c24bd564efda5ac38ae7669d39b4bfdbfaaa83f435f26d39b3d849d3a167a9c136c9ac6b2bfcc0bda09ef1c00aa66cf25  pyjnius/1.3.0.zip'
  '06e5664ae097ceae0e1499839c567bf8c41140a50d002213623d7fdac644f637701dbeca10ddf147840e932d57c9521b7fc1c0095b068d0aa491192249ee9c1c  python3/Python-3.9.5.tgz'
  '951d43a0192b9dddacd7bd7ff6b76e281c14071771096db3c413fde6ea67b0c534f17a770cb3464cd3a6a4e8145b82f4cf5c0228e76e6f2cefe88d33748816e9  setuptools/setuptools-56.0.0.tar.gz'
  'eb840ac17f433f1fc4af56de75cfbfe0b54e6a737bb23c453bf09a4a13d768d153e46064880dc763f4c5cc2785b78ea6d3d3b4a41fed181cb9064837e3f699a9  six/six-1.15.0.tar.gz'
  '9684fee89224f0c975c280cb6b2c64adb040334bc5517dfe0e354b0557459fa3ae642c4289a7a5265f65b3ad5b6747db8068a1e5172fbb8edec7f6d964ecbb20  sqlite3/sqlite-amalgamation-3350500.zip'
)
ant_vsn=apache-ant-1.9.4
ant_url=https://archive.apache.org/dist/ant/binaries/$ant_vsn-bin.tar.gz
ant_sum=ee13c915a18f3c6e1283c43ce3716e2ed1b03fd87abe27d0e4964a84cba54474f95655c8d75ee12de2516f4df62402acfc9df064aa05f2cc80560a144b2128f8

mkdir -p ~/.buildozer/android/platform
(
  cd ~/.buildozer/android/platform
  mkdir -p "$ant_vsn"
  cd "$ant_vsn"
  if [ ! -e "$ant_vsn-bin.tar.gz" ]; then
    wget -O "$ant_vsn-bin.tar.gz" -- "$ant_url"
  fi
  printf "$ant_sum  $ant_vsn-bin.tar.gz\n" | sha512sum -c
  if [ ! -e "$ant_vsn" ]; then
    tar xf "$ant_vsn-bin.tar.gz"
  fi
)

for arch in armeabi-v7a arm64-v8a; do
  mkdir -p ../../_jiten_buildozer_/android/platform/build-$arch/packages
  (
    cd ../../_jiten_buildozer_/android/platform/build-$arch/packages
    for (( i = 0; i < ${#urls[@]}; ++i )); do
      url="${urls[i]}" sum="${sums[i]}"; file="${sum:130}"
      mkdir -p "$(dirname "$file")"
      if [ ! -e "$file" ]; then
        wget -O "$file" -- "$url"
      fi
      printf "$sum\n" | sha512sum -c
      touch "$(dirname "$file")/.mark-$(basename "$file")"
    done
  )
done

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
