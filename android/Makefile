SHELL := /bin/bash

# for reproducible builds
export LC_ALL             := C
export TZ                 := UTC
export SOURCE_DATE_EPOCH  := $(shell git log -1 --pretty=%ct)
export PYTHONHASHSEED     := $(SOURCE_DATE_EPOCH)
export BUILD_DATE         := $(shell LC_ALL=C TZ=UTC date +'%b %e %Y' -d @$(SOURCE_DATE_EPOCH))
export BUILD_TIME         := $(shell LC_ALL=C TZ=UTC date +'%H:%M:%S' -d @$(SOURCE_DATE_EPOCH))

export APP_VERSION := $(shell git describe | sed 's/^v//')
ifndef APP_VERSION
  $(error git describe failed)
endif

NUMERIC := $(shell python3 -c 'import sys,functools; print(10*functools.reduce(lambda x,y: x*100+int(y),([1]+sys.argv[1].replace("-",".").split(".")+[0])[:5],0))' $(APP_VERSION))
ifndef NUMERIC
  $(error numeric version command failed)
endif

.PHONY: debug release clean

debug: debug-armeabi-v7a debug-arm64-v8a
release: release-armeabi-v7a release-arm64-v8a

clean:
	mkdir -p ../../_jiten_buildozer_
	APP_ANDROID_ARCH=armeabi-v7a buildozer android clean
	buildozer android clean
	rm -fr bin/

.PHONY: debug-armeabi-v7a debug-arm64-v8a
.PHONY: release-armeabi-v7a release-arm64-v8a

debug-armeabi-v7a:
	APP_ANDROID_ARCH=armeabi-v7a \
	APP_ANDROID_NUMERIC_VERSION=$$(( $(NUMERIC) + 1 )) \
	./scripts/buildozer.sh debug

debug-arm64-v8a:
	APP_ANDROID_NUMERIC_VERSION=$$(( $(NUMERIC) + 2 )) \
	./scripts/buildozer.sh debug

debug-x86:
	APP_ANDROID_ARCH=x86 \
	APP_ANDROID_NUMERIC_VERSION=$$(( $(NUMERIC) + 3 )) \
	./scripts/buildozer.sh debug

debug-x86_64:
	APP_ANDROID_ARCH=x86_64 \
	APP_ANDROID_NUMERIC_VERSION=$$(( $(NUMERIC) + 4 )) \
	./scripts/buildozer.sh debug

release-armeabi-v7a:
	APP_ANDROID_ARCH=armeabi-v7a \
	APP_ANDROID_NUMERIC_VERSION=$$(( $(NUMERIC) + 1 )) \
	./scripts/buildozer.sh release

release-arm64-v8a:
	APP_ANDROID_NUMERIC_VERSION=$$(( $(NUMERIC) + 2 )) \
	./scripts/buildozer.sh release

release-x86:
	APP_ANDROID_ARCH=x86 \
	APP_ANDROID_NUMERIC_VERSION=$$(( $(NUMERIC) + 3 )) \
	./scripts/buildozer.sh release

release-x86_64:
	APP_ANDROID_ARCH=x86_64 \
	APP_ANDROID_NUMERIC_VERSION=$$(( $(NUMERIC) + 4 )) \
	./scripts/buildozer.sh release

.PHONY: _setup_root _setup_user

_setup_root:
	./scripts/setup-root.sh

_setup_user:
	./scripts/setup-user.sh
