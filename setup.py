from pathlib import Path
import setuptools

import jiten.cli

long_description    = Path(__file__).with_name("README.md") \
                      .read_text(encoding = "utf8")

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
  package_data      = { "jiten":
    [ "res/freq/" + x for x in """SOURCES base_aggregates.txt.nobom
                                  wordfreq_ck.utf8""".split() ] +
    [ "res/jmdict/*." + x for x in "xml.gz html".split() ] +
    [ "static/*." + x for x in "svg css js".split() ] +
    [ "static/font/*." + x for x in "ttf txt".split() ] +
    [ "templates/*.html" ]
  },
  scripts           = ["bin/jiten"],
  python_requires   = ">=3.5",
  install_requires  = ["Flask", "click>=6.0"],
)
