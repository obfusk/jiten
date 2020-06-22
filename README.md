<!-- {{{1 -->

    File        : README.md
    Maintainer  : Felix C. Stegerman <flx@obfusk.net>
    Date        : 2020-06-21

    Copyright   : Copyright (C) 2020  Felix C. Stegerman
    Version     : v0.1.0
    License     : AGPLv3+

<!-- }}}1 -->

[![PyPI Version](https://img.shields.io/pypi/v/jiten.svg)](https://pypi.python.org/pypi/jiten)
[![CI](https://github.com/obfusk/jiten/workflows/CI/badge.svg)](https://github.com/obfusk/jiten/actions?query=workflow%3ACI)
[![AGPLv3+](https://img.shields.io/badge/license-AGPLv3+-blue.svg)](https://www.gnu.org/licenses/agpl-3.0.html)

## Description

jiten - japanese cli&web dictionary based on jmdict/kanjidic

→ https://jiten-py.herokuapp.com

![CLI screenshot](screenshot-cli.png)

![app screenshot](screenshot-app.png)

## Help

```bash
$ jiten --help
```

## Requirements

Python >= 3.5 + Flask + click.

## Installing

### Using pip

```bash
$ pip install jiten
```

## Generating the DB

You'll need to run this after installing (or updating).

```bash
$ jiten setup
```

## Miscellaneous

### Forcing HTTPS

```bash
$ export JITEN_HTTPS=force
```

## License

### Code

[![AGPLv3+](https://www.gnu.org/graphics/agplv3-155x51.png)](https://www.gnu.org/licenses/agpl-3.0.html)

### JMDict & KanjiDic

[![CC-BY-SA](https://licensebuttons.net/l/by-sa/2.0/88x31.png)](https://www.edrdg.org/edrdg/licence.html)

<!-- vim: set tw=70 sw=2 sts=2 et fdm=marker : -->
