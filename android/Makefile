SHELL       := /bin/bash
BUILDOZER   ?= buildozer
PIP_INSTALL ?= pip install

export APP_VERSION := $(shell git describe | sed 's/^v//')

_arm64a     := arm64-v8a
_arm64n     := $(shell sed -n '/numeric_version/ s/.* 7/8/ p' buildozer.spec)
_arm64      := APP_ANDROID_ARCH=$(_arm64a) APP_ANDROID_NUMERIC_VERSION=$(_arm64n)

.PHONY: debug clean _dir

debug: debug-armeabi-v7a debug-arm64-v8a

clean:
	buildozer android clean
	rm -fr bin/

_dir:
	mkdir -p ../../_jiten_buildozer_

.PHONY: debug-armeabi-v7a debug-arm64-v8a
.PHONY: release-armeabi-v7a release-arm64-v8a

debug-armeabi-v7a: _dir
	buildozer android debug

debug-arm64-v8a: _dir
	$(_arm64) buildozer android debug

release-armeabi-v7a: _dir
	buildozer android release

release-arm64-v8a: _dir
	$(_arm64) buildozer android release

.PHONY: _setup_root _setup_user

_setup_root:
	apt-get install -y build-essential git
	apt-get install -y openjdk-11-jdk-headless
	apt-get install -y zlib1g-dev zip unzip pkg-config lld libffi-dev

_setup_user:
	$(PIP_INSTALL) --upgrade $(BUILDOZER)
	$(PIP_INSTALL) --upgrade Cython==0.29.19 virtualenv
