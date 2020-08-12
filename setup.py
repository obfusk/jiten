from pathlib import Path
import os, setuptools, subprocess, sys

import jiten.cli

android_build       = os.environ.get("JITEN_ANDROID") == "yes"
long_description    = Path(__file__).with_name("README.md") \
                      .read_text(encoding = "utf8")
mod_sqlite3_pcre    = setuptools.Extension(
  "jiten._sqlite3_pcre", ["sqlite3-pcre.c"],
  libraries = "pcre sqlite3".split()
)
data    = [ "res/jlpt/N" + l for l in "12345" ] \
        + [ "static/*." + x for x in "svg css js".split() ] \
        + [ "static/audio/*.mp3" ] \
        + [ "static/font/*." + x for x in "ttf txt".split() ] \
        + [ "templates/*.html" ]

# "build" *.xml.gz
subprocess.run("make patch", shell = True, check = True)

if android_build:
  # "build" *.sqlite3
  jiten.cli.cli("-v setup".split(), standalone_mode = False)

  data += [ "res/*.sqlite3" ]
else:
  data += [ "res/freq/" + x for x in """SOURCES base_aggregates.txt.nobom
                                        wordfreq_ck.utf8""".split() ] \
        + [ "res/jmdict/*.html" ] \
        + [ "res/jmdict/"+x+".xml.gz" for x in "jmdict kanjidic2".split() ] \
        + [ "res/pitch/" + x for x in "PITCH SOURCES *.html *.py".split() ] \
        + [ "res/radicals/*." + x for x in "xml.gz utf8".split() ] \
        + [ "res/sentences/" + x for x in "Makefile SENTENCES *.py".split() ]

setuptools.setup(
  name              = "jiten",
  url               = "https://github.com/obfusk/jiten",
  description       = "japanese cli&web dictionary based on jmdict/kanjidic",
  long_description  = long_description,
  long_description_content_type = "text/markdown",
  version           = jiten.cli.__version__,
  author            = "Felix C. Stegerman",
  author_email      = "flx@obfusk.net",
  license           = "AGPLv3+",
  classifiers       = [
    "Development Status :: 4 - Beta",
    "Environment :: Console",
    "Environment :: Web Environment",
    "Intended Audience :: End Users/Desktop",
    "License :: OSI Approved :: GNU Affero General Public License v3 or later (AGPLv3+)",
    "Natural Language :: Dutch",
    "Natural Language :: English",
    "Natural Language :: German",
    "Natural Language :: Japanese",
    "Operating System :: POSIX :: Linux",
    "Programming Language :: Python :: 3",
    "Programming Language :: Python :: 3.5",
    "Programming Language :: Python :: 3.6",
    "Programming Language :: Python :: 3.7",
    "Programming Language :: Python :: 3.8",
    "Programming Language :: Python :: Implementation :: CPython",
    "Topic :: Education",
    "Topic :: Utilities",
  ],
  keywords          = "japanese kanji dictionary cli web jmdict kanjidic",
  packages          = setuptools.find_packages(),
  package_data      = { "jiten": data },
  scripts           = ["bin/jiten"],
  python_requires   = ">=3.5",
  install_requires  = ["Flask", "click>=6.0"],
  ext_modules       = [mod_sqlite3_pcre],
)
