#!/bin/bash
set -xe -o pipefail
year=2021 vsn=3360000
sha512sum=5c18f158a599b1e91d95c91de3aa5c5de52f986845ad0cb49dfd56b650587e55e24d469571b5b864229b870d0eaf85d78893f61ef950b95389cb41692be37f58
dir=sqlite-amalgamation-$vsn
url=https://www.sqlite.org/$year/$dir.zip
wget -O "$dir.zip" -- "$url"
printf "$sha512sum  $dir.zip\n" | sha512sum -c
unzip "$dir.zip"
cd "$dir"
cc -shared -fPIC -ldl -lm -lpthread -o libsqlite3.so sqlite3.c
mv libsqlite3.so /usr/lib/x86_64-linux-gnu/
mv *.h /usr/include/
