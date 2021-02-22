from pathlib import Path
import os, setuptools, subprocess, sys

from jiten.version import __version__

vsn   = __version__.replace("-", ".dev", 1).replace("-", "+", 1) \
          if __version__.count("-") >= 2 else __version__

clean = "clean" in sys.argv[1:]

info  = Path(__file__).with_name("README.md").read_text(encoding = "utf8")
pcre  = setuptools.Extension("jiten._sqlite3_pcre", ["sqlite3-pcre.c"],
                             libraries = "pcre sqlite3".split())

data  = [ "res/jlpt/N" + l + "-" + x for l in "12345"
          for x in "kanji vocab-eng vocab-hiragana".split() ] \
      + [ "res/jlpt/" + x for x in "SOURCES *.sh *.html".split() ] \
      + [ "static/*." + x for x in "svg png css js txt".split() ] \
      + [ "static/audio/*.mp3" ] \
      + [ "static/font/*." + x for x in "ttf txt".split() ] \
      + [ "static/licenses/*.txt" ] \
      + [ "templates/*.html" ]

if clean:
  subprocess.run("make clean", shell = True, check = True)
else:
  # "build" *.xml.gz
  subprocess.run("make patch", shell = True, check = True)

if os.environ.get("JITEN_ANDROID") == "yes" or \
    os.environ.get("JITEN_FINAL") == "yes":
  if not clean:
    subprocess.run("make _version", shell = True, check = True)
  data += [ ".version" ]

  if os.environ.get("JITEN_NODB") != "yes":
    if not clean:
      # "build" *.sqlite3
      import jiten.cli
      jiten.cli.cli("-v setup".split(), standalone_mode = False)
    data += [ "res/*.sqlite3" ]
else:
  data += [ "res/freq/" + x for x in """SOURCES base_aggregates.txt.nobom
                                        wordfreq_ck.utf8""".split() ] \
        + [ "res/jmdict/" + x for x in "*.html Makefile".split() ] \
        + [ "res/jmdict/"+x+".xml.gz" for x in "jmdict kanjidic2".split() ] \
        + [ "res/pitch/" + x for x in "PITCH SOURCES *.html *.py *.sh".split() ] \
        + [ "res/radicals/" + x for x in "SOURCES *.xml.gz *.utf8".split() ] \
        + [ "res/sentences/" + x for x in "Makefile SENTENCES *.py".split() ]

setuptools.setup(
  name              = "jiten",
  url               = "https://github.com/obfusk/jiten",
  description       = "japanese cli&web dictionary based on jmdict/kanjidic",
  long_description  = info,
  long_description_content_type = "text/markdown",
  version           = vsn,
  author            = "Felix C. Stegerman",
  author_email      = "flx@obfusk.net",
  license           = "AGPLv3+",
  classifiers       = [
    "Development Status :: 5 - Production/Stable",
    "Environment :: Console",
    "Environment :: Web Environment",
    "Intended Audience :: End Users/Desktop",
    "License :: Free for non-commercial use",
    "License :: OSI Approved :: GNU Affero General Public License v3 or later (AGPLv3+)",
    "Natural Language :: Dutch",
    "Natural Language :: English",
    "Natural Language :: German",
    "Natural Language :: Japanese",
    "Operating System :: Android",
    "Operating System :: POSIX :: Linux",
    "Programming Language :: Python :: 3",
    "Programming Language :: Python :: 3.5",
    "Programming Language :: Python :: 3.6",
    "Programming Language :: Python :: 3.7",
    "Programming Language :: Python :: 3.8",
    "Programming Language :: Python :: 3.9",
  # "Programming Language :: Python :: 3.10",
    "Programming Language :: Python :: Implementation :: CPython",
    "Programming Language :: Python :: Implementation :: PyPy",
    "Topic :: Education",
    "Topic :: Utilities",
  ],
  keywords          = "japanese kanji dictionary cli web jmdict kanjidic",
  packages          = setuptools.find_packages(),
  package_data      = dict(jiten = data),
  entry_points      = dict(
    console_scripts = ["jiten = jiten.cli:main"],
    gui_scripts     = ["jiten-gui = jiten.cli:gui_main [gui]"],
  ),
  python_requires   = ">=3.5",
  install_requires  = ["Flask", "click>=6.0"],
  extras_require    = dict(gui = ["pywebview>=3.3.5"]),
  ext_modules       = [pcre],
)
