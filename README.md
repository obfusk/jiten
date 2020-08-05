<!-- {{{1 -->

    File        : README.md
    Maintainer  : Felix C. Stegerman <flx@obfusk.net>
    Date        : 2020-08-05

    Copyright   : Copyright (C) 2020  Felix C. Stegerman
    Version     : v0.2.0
    License     : AGPLv3+

<!-- }}}1 -->

[![PyPI Version](https://img.shields.io/pypi/v/jiten.svg)](https://pypi.python.org/pypi/jiten)
[![CI](https://github.com/obfusk/jiten/workflows/CI/badge.svg)](https://github.com/obfusk/jiten/actions?query=workflow%3ACI)
[![Android Build](https://github.com/obfusk/jiten/workflows/Android/badge.svg)](https://github.com/obfusk/jiten/actions?query=workflow%3AAndroid)
[![AGPLv3+](https://img.shields.io/badge/license-AGPLv3+-blue.svg)](https://www.gnu.org/licenses/agpl-3.0.html)

## Description

jiten - japanese cli&web dictionary based on jmdict/kanjidic

→ https://jiten.obfusk.dev

![CLI screenshot](screenshot-cli.png)

![app screenshot](screenshot-app.png)

## Features

* Fine-grained search using
  [regexes](https://docs.python.org/3/library/re.html#regular-expression-syntax)
  (regular expressions)
* JMDict multilingual japanese dictionary
  - kanji, readings, meanings (eng, dut, ger) & more
  - by frequency
  - random entry
* Kanji dictionary
  - readings, meanings (eng) & more
  - search using
    [SKIP codes](https://en.wikipedia.org/wiki/Kodansha_Kanji_Learner%27s_Dictionary#SKIP)
  - by frequency/level
* Stroke order
* Web interface
  - can be run on your own computer or android phone
  - light/dark mode
* Command-line interface

## CLI

### JMDict

```bash
$ jiten -v jmdict --max 1 --word cat
$ jiten -v jmdict --max 1 --word kat --lang dut
$ jiten -v jmdict --max 1 --exact 誤魔化す
```

### Kanji

```bash
$ jiten -v kanji --max 1 --word cat
$ jiten -v kanji --max 1 --exact cat
$ jiten -v kanji --max 1 --word 日
```

## Web Interface

```bash
$ jiten -v serve
```

## Help

```bash
$ jiten --help
```

## Requirements

Python >= 3.5 + Flask + click.

To build the (not yet optional) SQLite PCRE C extension: a C compiler
(e.g. `gcc`/`clang`) and the `sqlite3` & `pcre` libraries & headers.

### Debian/Ubuntu

```bash
$ apt install python3-dev build-essential libsqlite3-dev libpcre3-dev
$ apt install python3-flask   # optional: Flask & click w/o pip
```

## Installing

### Using pip

```bash
$ pip install jiten
```

### From git

NB: this installs the latest development version, not the latest
release.

```bash
$ git clone https://github.com/obfusk/jiten.git
$ cd jiten
$ pip install -e .
```

NB: you may need to add e.g. `~/.local/bin` to your `$PATH` in order
to run `jiten`.

## Android

There's no app (yet?), but you can run the web interface locally (&
off-line) on your android phone.  First, install
[termux](https://termux.com/), then run:

```bash
$ apt install clang python
$ pip install jiten
```

You can then run the web interface with:

```bash
$ jiten serve
```

and open http://localhost:5000 in your browser.

The web interface will keep running until you close termux or reboot.

## Miscellaneous

### Generating the DB

```bash
$ jiten setup
```

### Forcing HTTPS

```bash
$ export JITEN_HTTPS=force
```

### Forcing Domain Name

```bash
$ export JITEN_DOMAIN=jiten.obfusk.dev
```

## License

### Code

© Felix C. Stegerman

[![AGPLv3+](https://www.gnu.org/graphics/agplv3-155x51.png)](https://www.gnu.org/licenses/agpl-3.0.html)

### JMDict & KanjiDic

© James William BREEN and The Electronic Dictionary Research and
Development Group

[![CC-BY-SA](https://licensebuttons.net/l/by-sa/2.0/88x31.png)](https://www.edrdg.org/edrdg/licence.html)

### Wadoku (pitch)

© Ulrich Apel & Wadoku.de contributors

[Non-commercial](https://www.wadoku.de/wiki/display/WAD/Wadoku.de-Daten+Lizenz)

### KanjiVG (radicals)

© Ulrich Apel

[![CC-BY-SA](https://licensebuttons.net/l/by-sa/3.0/88x31.png)](https://github.com/KanjiVG/kanjivg/blob/master/COPYING)

### Stroke Order Font

© Ulrich Apel, the AAAA project and the Wadoku project

[BSD-3-Clause](https://www.nihilist.org.uk)

### Kana Tables

© Wikipedia contributors

[![CC-BY-SA](https://licensebuttons.net/l/by-sa/3.0/88x31.png)](https://en.wikipedia.org/wiki/File:Table_hiragana.svg)
[![CC-BY-SA](https://licensebuttons.net/l/by-sa/3.0/88x31.png)](https://en.wikipedia.org/wiki/File:Table_katakana.svg)

<!-- vim: set tw=70 sw=2 sts=2 et fdm=marker : -->
