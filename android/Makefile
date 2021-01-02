SHELL       := /bin/bash
BUILDOZER   ?= buildozer
PIP_INSTALL ?= pip install

# for reproducible builds
export LC_ALL             := C
export TZ                 := UTC
export SOURCE_DATE_EPOCH  := $(shell git log -1 --pretty=%ct)
export PYTHONHASHSEED     := $(SOURCE_DATE_EPOCH)
export BUILD_DATE         := $(shell date +'%b %e %Y' -d @$(SOURCE_DATE_EPOCH))
export BUILD_TIME         := $(shell date +'%H:%M:%S' -d @$(SOURCE_DATE_EPOCH))

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

release-armeabi-v7a:
	APP_ANDROID_ARCH=armeabi-v7a \
	APP_ANDROID_NUMERIC_VERSION=$$(( $(NUMERIC) + 1 )) \
	./scripts/buildozer.sh release

release-arm64-v8a:
	APP_ANDROID_NUMERIC_VERSION=$$(( $(NUMERIC) + 2 )) \
	./scripts/buildozer.sh release

.PHONY: _setup_root _setup_user

_setup_root:
	apt-get update || apt-get update
	apt-get install -y build-essential git
	apt-get install -y openjdk-11-jdk-headless
	apt-get install -y zlib1g-dev zip unzip pkg-config libffi-dev
	apt-get install -y libltdl-dev libssl-dev
	apt-get install -y lld

_setup_user:
	$(PIP_INSTALL) --upgrade $(BUILDOZER)
	$(PIP_INSTALL) --upgrade Cython==0.29.19 virtualenv
	# FIXME
	buildozer="$$( python3 -c 'import buildozer.targets.android as x; print(x.__file__)' )"; \
	  sed -r 's!^( *_version *=) *re.search.*!\1 self.android_ndk_version!' "$$buildozer" -i
