#!/bin/bash
set -xe
vsn=v3.7.10
git clone --depth 1 -b "$vsn" https://github.com/python/cpython
cd cpython
./configure
make -j`nproc`
make altinstall
