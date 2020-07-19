SHELL       := /bin/bash
BUILDOZER   ?= buildozer
PIP_INSTALL ?= pip install

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
	apt-get install -y openjdk-11-jdk-headless
	apt-get install -y zlib1g-dev zip unzip pkg-config lld libffi-dev

_setup_user:
	$(PIP_INSTALL) --upgrade $(BUILDOZER)
	$(PIP_INSTALL) --upgrade Cython==0.29.19 virtualenv
