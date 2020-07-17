SHELL := /bin/bash

.PHONY: debug release clean

debug:
	mkdir -p ../../_jiten_buildozer_
	buildozer android debug

release:
	mkdir -p ../../_jiten_buildozer_
	buildozer android release

clean:
	buildozer android clean
	rm -fr bin/

.PHONY: _setup_root _setup_user

_setup_root:
	apt-get install -y build-essential git
	apt-get install -y python3-pip python3-dev python3-setuptools python3-wheel
	apt-get install -y zlib1g-dev openjdk-11-jdk-headless zip unzip pkg-config lld libffi-dev
	apt-get install -y autoconf libtool libssl-dev                # ???
	apt-get install -y python3-click libsqlite3-dev libpcre3-dev  # for jiten ???

_setup_user:
	pip3 install --user --upgrade buildozer
	pip3 install --user --upgrade Cython==0.29.19 virtualenv
