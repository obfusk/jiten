#!/bin/bash
set -xe
export DEBIAN_FRONTEND=noninteractive
apt-get update || apt-get update
apt-get install -y build-essential git
apt-get install -y python3-pip python3-dev libsqlite3-dev libpcre3-dev
apt-get install -y openjdk-11-jdk-headless
apt-get install -y zlib1g-dev zip unzip pkg-config libffi-dev
apt-get install -y libltdl-dev libssl-dev
apt-get install -y lld
