[app]
title = Jiten
package.name = jiten
package.domain = dev.obfusk
source.dir = .
source.include_exts = py
source.exclude_dirs = bin,patches,p4a-recipes,scripts
source.exclude_patterns = makefile,p4a-commit,*.png,*.xml
requirements =
  click==7.1.2,flask==1.1.2,jiten,openssl,sqlite3,
  certifi==2020.12.5,libpcre==8.44,
  hostpython3==3.9.1,python3==3.9.1,
  android,genericndkbuild,
  itsdangerous==1.1.0,jinja2==2.11.2,markupsafe==1.1.1,werkzeug==1.0.1,
  libffi==v3.3,pyjnius==1.3.0,
  setuptools==51.3.3,six==1.15.0
requirements.source.jiten = ..
icon.filename = %(source.dir)s/icon.png
orientation = portrait
fullscreen = 0
android.api = 29
android.minapi = 21
android.ndk = 22
#android.ndk_path =
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
version = 0.3.5
android.numeric_version = 1000305002
# always "1" -------------^|||||||||
# 0.3.5 ----> 00 03 05 ----^^^^^^|||
# #commits since last tag -------^^|
# 1 = armeabi-v7a, 2 = arm64-v8a --^
# ===================================

[buildozer]
log_level = 2
warn_on_root = 1
