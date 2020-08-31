[app]
title = Jiten
package.name = jiten
package.domain = dev.obfusk
source.dir = .
source.include_exts = py
source.exclude_dirs = bin,p4a-recipes
source.exclude_patterns = Makefile,*.png
requirements = python3,jiten
requirements.source.jiten = ..
icon.filename = %(source.dir)s/icon.png
orientation = portrait
fullscreen = 0
android.api = 29
android.minapi = 21
android.ndk = 20b
#android.ndk_path =
#android.sdk_path =
android.accept_sdk_license = True
android.arch = arm64-v8a
p4a.branch = develop
#p4a.source_dir =
p4a.local_recipes = ./p4a-recipes
p4a.bootstrap = webview
p4a.port = 29483

# === DON'T FORGET TO UPDATE THIS ===
version = 0.3.3
android.numeric_version = 1000303002
# always "1" -------------^|||||||||
# 0.3.3 ----> 00 03 03 ----^^^^^^|||
# #commits since last tag -------^^|
# 1 = armeabi-v7a, 2 = arm64-v8a --^
# ===================================

[buildozer]
log_level = 2
warn_on_root = 1
