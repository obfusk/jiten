[app]
title = Jiten
package.name = jiten
package.domain = dev.obfusk
source.dir = .
source.include_exts = py
source.exclude_dirs = bin,p4a-recipes
source.exclude_patterns = Makefile,*.png
version = 0.2.0
requirements = python3,jiten
requirements.source.jiten = ..
icon.filename = %(source.dir)s/icon.png
orientation = portrait
fullscreen = 0
android.api = 29
android.minapi = 21
android.ndk = 19c
#android.ndk_path =
#android.sdk_path =
android.accept_sdk_license = True
android.arch = armeabi-v7a
# !!! DON'T FORGET TO UPDATE THIS !!!
# arch (7 = armeabi-v7a, 8 = arm64-v8a) + minapi + version (%02d%02d%02d)
# e.g. armeabi-v7a + minapi 27 + v0.1.1 = 721000101
android.numeric_version = 721000200
p4a.branch = develop
#p4a.source_dir =
p4a.local_recipes = ./p4a-recipes
p4a.bootstrap = webview
p4a.port = 29483

[buildozer]
log_level = 2
warn_on_root = 1
