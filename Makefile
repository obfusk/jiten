SHELL   := /bin/bash
PYTHON  ?= python3

CSSV    := https://jigsaw.w3.org/css-validator/validator
CSSOK   := Congratulations! No Error Found.

HTMLV   := https://html5.validator.nu
HTMLOK  := The document is valid HTML5

URL     := http://localhost:5000
H5VCMD  := html5validator --show-warnings --log INFO --no-langdetect

.PHONY: all test ci-test clean cleanup validate-css tmp-html
.PHONY: check-html validate-html validate-html-curl validate-html-py

all: ext
	$(PYTHON) -m jiten.cli setup

test: all
	$(PYTHON) -m jiten.app       --verbose --doctest
	$(PYTHON) -m jiten.cli       --verbose  _doctest
	$(PYTHON) -m jiten.freq      --verbose --doctest
	$(PYTHON) -m jiten.jmdict    --verbose --doctest
	$(PYTHON) -m jiten.kana      --verbose --doctest
	$(PYTHON) -m jiten.kanji     --verbose --doctest
	$(PYTHON) -m jiten.misc      --verbose --doctest
	$(PYTHON) -m jiten.pitch     --verbose --doctest
	$(PYTHON) -m jiten.sentences --verbose --doctest
	node jiten/static/script.js

ci-test: test validate-css validate-html check-html

clean: cleanup
	rm -f jiten/res/*.sqlite3
	rm -f jiten/_sqlite3_pcre.*.so
	$(MAKE) -C jiten/res/jmdict clean
	$(MAKE) -C jiten/res/sentences clean

cleanup:
	find -name '*~' -delete -print
	rm -fr jiten/__pycache__/ tmp-html/
	rm -fr build/ dist/ jiten.egg-info/
	rm -fr jiten/.version
	$(MAKE) -C jiten/res/jmdict cleanup

validate-css:
	curl -sF "file=@jiten/static/style.css;type=text/css" \
	  -- "$(CSSV)" | grep -qF '$(CSSOK)'

tmp-html:
	$(PYTHON) -m jiten.cli serve & pid=$$!; \
	trap "kill $$pid" EXIT; mkdir -p tmp-html; sleep 5; \
	curl -sG $(URL) > tmp-html/index.html; \
	curl -sG $(URL)/jmdict -d max=10 -d word=yes \
	  --data-urlencode query=cat   > tmp-html/cat.html  ; \
	curl -sG $(URL)/jmdict -d max=10 -d word=yes \
	  --data-urlencode query=idiot > tmp-html/idiot.html; \
	curl -sG $(URL)/kanji  -d max=10 -d word=yes \
	  --data-urlencode query=ねこ  > tmp-html/neko.html ; \
	curl -sG $(URL)/kanji  -d max=10 -d word=yes \
	  --data-urlencode query=日    > tmp-html/hi.html   ; \
	curl -sG $(URL)/stroke > tmp-html/stroke.html

# TODO
check-html:
	grep -qF 猫 tmp-html/cat.html
	grep -qF "cat (esp. the domestic cat, Felis catus)" tmp-html/cat.html
	grep -qF "word usually written using kana alone" tmp-html/cat.html
	grep -qF 0x732b tmp-html/neko.html
	grep -qF "counter for days" tmp-html/hi.html

validate-html: tmp-html validate-html-py

validate-html-curl:
	for file in $$( find tmp-html/ -name '*.html' | sort ); do \
	  echo "validating $$file..."; \
	  curl -sF "file=@$$file;type=text/html" -- "$(HTMLV)" \
	    | grep -qF '$(HTMLOK)' || exit 1; \
	done

validate-html-py:
	unset JAVA_TOOL_OPTIONS && $(H5VCMD) --root tmp-html/

.PHONY: ext patch _version _package _publish

ext:
	$(PYTHON) setup.py build_ext -i

patch:
	$(MAKE) -C jiten/res/jmdict all
	$(MAKE) -C jiten/res/jmdict cleanup

_version:
	if [ -n "$$JITEN_VERSION" ]; then \
	  echo "v$$JITEN_VERSION"; \
	else \
	  git describe --always; \
	fi > jiten/.version

_package:
	$(PYTHON) setup.py sdist bdist_wheel
	twine check dist/*

_publish: cleanup _package
	read -r -p "Are you sure? "; \
	[[ "$$REPLY" == [Yy]* ]] && twine upload dist/*.tar.gz
