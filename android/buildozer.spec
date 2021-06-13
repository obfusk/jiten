[app]
title = Jiten
package.name = jiten
package.domain = dev.obfusk
source.dir = .
source.include_exts = py
source.exclude_dirs = bin,patches,p4a-recipes,scripts
source.exclude_patterns = makefile,p4a-commit,*.png,*.xml
requirements =
  click==8.0.0,flask==2.0.0,jiten,openssl,sqlite3,
  certifi==2020.12.5,kanjidraw==0.2.1,libpcre==8.44,
  hostpython3==3.9.5,python3==3.9.5,
  android,genericndkbuild,
  itsdangerous==2.0.0,jinja2==3.0.0,markupsafe==2.0.0,werkzeug==2.0.0,
  libffi==v3.3,pyjnius==1.3.0,
  setuptools==56.2.0,six==1.16.0
requirements.source.jiten = ..
icon.filename = %(source.dir)s/icon.png
orientation = portrait
fullscreen = 0
android.api = 30
android.minapi = 23

# https://gitlab.com/fdroid/android-sdk-transparency-log/-/raw/master/checksums.json
android.ndk = 22b
android.ndk_path = /opt/android-sdk/ndk/22.1.7171670

#android.sdk_path =
android.accept_sdk_license = True
android.manifest.intent_filters = %(source.dir)s/intent.xml
android.manifest.launch_mode = singleTask
android.arch = arm64-v8a
p4a.branch = develop
#p4a.source_dir =
p4a.local_recipes = ./p4a-recipes
p4a.bootstrap = webview
p4a.port = 29483

# === DON'T FORGET TO UPDATE THIS ===
version = 1.0.0
android.numeric_version = 1010000002
# always "1" -------------^|||||||||
# 1.0.0 ----> 01 00 00 ----^^^^^^|||
# #commits since last tag -------^^|
# 1 = armeabi-v7a, 2 = arm64-v8a --^
# ===================================

[buildozer]
log_level = 2
warn_on_root = 1
