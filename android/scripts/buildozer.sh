#!/bin/bash
set -xe -o pipefail
commit="$( < p4a-commit )"
urls=(
  https://github.com/pallets/click/archive/8.0.0.zip
  https://github.com/pallets/flask/archive/2.0.0.zip
  https://www.python.org/ftp/python/3.9.5/Python-3.9.5.tgz
  https://github.com/libffi/libffi/archive/v3.3.tar.gz
  https://ftp.pcre.org/pub/pcre/pcre-8.44.tar.bz2
  https://www.openssl.org/source/openssl-1.1.1k.tar.gz
  https://github.com/kivy/pyjnius/archive/1.3.0.zip
  https://www.python.org/ftp/python/3.9.5/Python-3.9.5.tgz
  https://pypi.python.org/packages/source/s/setuptools/setuptools-56.2.0.tar.gz
  https://pypi.python.org/packages/source/s/six/six-1.16.0.tar.gz
  https://www.sqlite.org/2021/sqlite-amalgamation-3350500.zip
)
sums=(
  '85a423b10199f9b7f34813af187977d689367f925cf795fe99e86ca7bf6c2bd3538669b7881bd7d50d0023a753f8e37e0e2a65cc0b9b4fde9d99fd2873d0e289  click/8.0.0.zip'
  '789be598075213f8dad991342771afc14b63a1239affa55cff5d1d10d1cde0339835e7cf37c644437d16c6b72458239c3bd0675c51b01029d86751dcb5130296  flask/2.0.0.zip'
  '06e5664ae097ceae0e1499839c567bf8c41140a50d002213623d7fdac644f637701dbeca10ddf147840e932d57c9521b7fc1c0095b068d0aa491192249ee9c1c  hostpython3/Python-3.9.5.tgz'
  '62798fb31ba65fa2a0e1f71dd3daca30edcf745dc562c6f8e7126e54db92572cc63f5aa36d927dd08375bb6f38a2380ebe6c5735f35990681878fc78fc9dbc83  libffi/v3.3.tar.gz'
  'f26d850aab5228799e58ac8c2306fb313889332c39e29b118ef1de57677c5c90f970d68d3f475cabc64f8b982a77f04eca990ff1057f3ccf5e19bd137997c4ac  libpcre/pcre-8.44.tar.bz2'
  '73cd042d4056585e5a9dd7ab68e7c7310a3a4c783eafa07ab0b560e7462b924e4376436a6d38a155c687f6942a881cfc0c1b9394afcde1d8c46bf396e7d51121  openssl/openssl-1.1.1k.tar.gz'
  '5a3475afcda5afbef6e1a67bab508e3c24bd564efda5ac38ae7669d39b4bfdbfaaa83f435f26d39b3d849d3a167a9c136c9ac6b2bfcc0bda09ef1c00aa66cf25  pyjnius/1.3.0.zip'
  '06e5664ae097ceae0e1499839c567bf8c41140a50d002213623d7fdac644f637701dbeca10ddf147840e932d57c9521b7fc1c0095b068d0aa491192249ee9c1c  python3/Python-3.9.5.tgz'
  '858d46909335ff0b0441d5860788803100a8fe9f5a1d1f17353bf961bc77191c3237501c1838fdb6ec8e4b2c66874ffd4e8342b42cc2673cb866706660704ea6  setuptools/setuptools-56.2.0.tar.gz'
  '076fe31c8f03b0b52ff44346759c7dc8317da0972403b84dfe5898179f55acdba6c78827e0f8a53ff20afe8b76432c6fe0d655a75c24259d9acbaa4d9e8015c0  six/six-1.16.0.tar.gz'
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
