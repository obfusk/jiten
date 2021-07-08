#!/bin/bash
set -xe -o pipefail
commit="$( < p4a-commit )"
urls=(
  https://pypi.python.org/packages/source/c/certifi/certifi-2021.5.30.tar.gz
  https://github.com/pallets/click/archive/8.0.1.zip
  https://github.com/pallets/flask/archive/2.0.1.zip
  https://www.python.org/ftp/python/3.9.6/Python-3.9.6.tgz
  https://github.com/pallets/itsdangerous/archive/2.0.1.zip
  https://github.com/pallets/jinja/archive/3.0.1.zip
  https://github.com/obfusk/kanjidraw/archive/v0.2.3.tar.gz
  https://github.com/libffi/libffi/archive/v3.4.2.tar.gz
  https://ftp.pcre.org/pub/pcre/pcre-8.45.tar.bz2
  https://github.com/pallets/markupsafe/archive/2.0.1.zip
  https://www.openssl.org/source/openssl-1.1.1k.tar.gz
  https://github.com/kivy/pyjnius/archive/1.3.0.zip
  https://www.python.org/ftp/python/3.9.6/Python-3.9.6.tgz
  https://pypi.python.org/packages/source/s/setuptools/setuptools-57.1.0.tar.gz
  https://pypi.python.org/packages/source/s/six/six-1.16.0.tar.gz
  https://www.sqlite.org/2021/sqlite-amalgamation-3360000.zip
  https://github.com/pallets/werkzeug/archive/2.0.1.zip
)
sums=(
  '77a5ce25d3ea297160d3dd8e97a582cc79985acf989257755a3693696aeeefbba31b8f9e4b6afca101058a4ef7075fc5fc8780b389800354d7a1de6398612d03  certifi/certifi-2021.5.30.tar.gz'
  'e191ac41acb9060cf733fca714da179b46170b93d35c5212816052f69d706e47ffe146f6758fa040e58b3cb82ff4e61e02692a840052fdb3261cf14f31b3100a  click/8.0.1.zip'
  'a2c722fca9ce1da5b61eecb15709e5d099bb6fa1857e2f6f1f6098dd9308c85cc78c383757df1fefd9e5af472f12c264b275d7b8813267a5e8887a44cebeef33  flask/2.0.1.zip'
  '668f28a6cd2266eea568c5b4482f3904dcb117c65a336981c6d0843fdd39431abb1cb058e608db77d7678b8cbec996f23f02969c83cba40413f38de675636783  hostpython3/Python-3.9.6.tgz'
  '5ba80b87f889bf7e6842f832f40bf9e749944a4c6d2c090de544fed591cdf8475833f62acbd7703f86673fb68f7cddbc7c7a2c350098195fda8d785e2932ce36  itsdangerous/2.0.1.zip'
  '465482b6dbd0d2d7126bc3620b63d55bb597bc99ff5280765b587f4c2a2575067140ac99d8ad06c9767941eeb551863000bea91d11363599e8a1adfe74b61c74  jinja2/3.0.1.zip'
  'b2a67fb5141d2a6f5007776679a28927219aeb3a2d72a7f49362f4a52e18cd027ccc0f3a9b9ffc8a095382c6388c90024d554a4b2ddd7e1acb9d8f99fa1d352c  kanjidraw/v0.2.3.tar.gz'
  'd399319efcca375fe901b05722e25eca31d11a4261c6a5d5079480bbc552d4e4b42de2026912689d3b2f886ebb3c8bebbea47102e38a2f6acbc526b8d5bba388  libffi/v3.4.2.tar.gz'
  '91bff52eed4a2dfc3f3bfdc9c672b88e7e2ffcf3c4b121540af8a4ae8c1ce05178430aa6b8000658b9bb7b4252239357250890e20ceb84b79cdfcde05154061a  libpcre/pcre-8.45.tar.bz2'
  '5f77e711b02d2ca0a44855097a5a46adad57735bf50e7b3b40dbfb129c01aec89576d26739f7eb080cdb3bd4467b2e8e0a427f22388c39c89d2d2be8a21df095  markupsafe/2.0.1.zip'
  '73cd042d4056585e5a9dd7ab68e7c7310a3a4c783eafa07ab0b560e7462b924e4376436a6d38a155c687f6942a881cfc0c1b9394afcde1d8c46bf396e7d51121  openssl/openssl-1.1.1k.tar.gz'
  '5a3475afcda5afbef6e1a67bab508e3c24bd564efda5ac38ae7669d39b4bfdbfaaa83f435f26d39b3d849d3a167a9c136c9ac6b2bfcc0bda09ef1c00aa66cf25  pyjnius/1.3.0.zip'
  '668f28a6cd2266eea568c5b4482f3904dcb117c65a336981c6d0843fdd39431abb1cb058e608db77d7678b8cbec996f23f02969c83cba40413f38de675636783  python3/Python-3.9.6.tgz'
  'dfcf75584b3d7ae07e0f58ce8f596d7e9cbe3a0c178411053b066fb4362226bcf6467a79aed0853acd0b9f6a3371c47ddb07d77cbd780fe9782b8c19bce2e5fb  setuptools/setuptools-57.1.0.tar.gz'
  '076fe31c8f03b0b52ff44346759c7dc8317da0972403b84dfe5898179f55acdba6c78827e0f8a53ff20afe8b76432c6fe0d655a75c24259d9acbaa4d9e8015c0  six/six-1.16.0.tar.gz'
  '5c18f158a599b1e91d95c91de3aa5c5de52f986845ad0cb49dfd56b650587e55e24d469571b5b864229b870d0eaf85d78893f61ef950b95389cb41692be37f58  sqlite3/sqlite-amalgamation-3360000.zip'
  'd17eae8b3f267967651619e554afb804a74fa97572f1c58a75866bca17cc03df6c4a86aeb66700a9e24e759940014cb4048d79c88fada657f4ddb17af542032d  werkzeug/2.0.1.zip'
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
