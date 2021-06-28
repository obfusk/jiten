#!/bin/bash
set -xe -o pipefail
year=2021 vsn=3350500
sha512sum=9684fee89224f0c975c280cb6b2c64adb040334bc5517dfe0e354b0557459fa3ae642c4289a7a5265f65b3ad5b6747db8068a1e5172fbb8edec7f6d964ecbb20
dir=sqlite-amalgamation-$vsn
url=https://www.sqlite.org/$year/$dir.zip
wget -O "$dir.zip" -- "$url"
printf "$sha512sum  $dir.zip\n" | sha512sum -c
unzip "$dir.zip"
cd "$dir"
cc -shared -fPIC -ldl -lm -lpthread -o libsqlite3.so sqlite3.c
mv libsqlite3.so /usr/lib/x86_64-linux-gnu/
mv *.h /usr/include/
