[app]
title = Jiten
package.name = jiten
package.domain = dev.obfusk
source.dir = .
source.include_exts = py
source.exclude_dirs = bin,p4a-recipes
source.exclude_patterns = Makefile
version.regex = __version__ *= *['"](.*)['"]
version.filename = ../jiten/cli.py
requirements = python3,jiten
requirements.source.jiten = ..
#icon.filename = %(source.dir)s/data/icon.png
orientation = portrait
fullscreen = 0
#android.ndk_path =
#android.sdk_path =
android.accept_sdk_license = True
android.arch = armeabi-v7a
p4a.branch = develop
p4a.local_recipes = ./p4a-recipes
p4a.bootstrap = webview

[buildozer]
log_level = 2
warn_on_root = 1
