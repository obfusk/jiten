SHELL   := /bin/bash
PYTHON  ?= python3
VERBOSE ?= --verbose

CSSV    := https://jigsaw.w3.org/css-validator/validator
CSSOK   := Congratulations! No Error Found.

HTMLV   := https://html5.validator.nu
HTMLOK  := The document is valid HTML5

URL     := http://localhost:5000
H5VCMD  := html5validator --show-warnings --log INFO --no-langdetect \
             --ignore 'Unicode Normalization Form'

PYCOV   := $(PYTHON) -mcoverage run --source jiten

.PHONY: all test test-js ci-test coverage clean cleanup
.PHONY: validate-css tmp-html check-html validate-html
.PHONY: validate-html-curl validate-html-py

all: ext
	$(PYTHON) -m jiten.cli setup

test: all test-js
	$(PYTHON) -m jiten.app       $(VERBOSE) --doctest
	$(PYTHON) -m jiten.cli       $(VERBOSE)  _doctest
	$(PYTHON) -m jiten.freq      $(VERBOSE) --doctest
	$(PYTHON) -m jiten.jmdict    $(VERBOSE) --doctest
	$(PYTHON) -m jiten.kana      $(VERBOSE) --doctest
	$(PYTHON) -m jiten.kanji     $(VERBOSE) --doctest
	$(PYTHON) -m jiten.misc      $(VERBOSE) --doctest
	$(PYTHON) -m jiten.pitch     $(VERBOSE) --doctest
	$(PYTHON) -m jiten.sentences $(VERBOSE) --doctest

test-js:
	node jiten/static/script.js

ci-test: test-js coverage validate-css validate-html check-html

coverage: tmp-html
	$(PYCOV) -a -m jiten.app       --doctest
	$(PYCOV) -a -m jiten.cli        _doctest
	$(PYCOV) -a -m jiten.freq      --doctest
	$(PYCOV) -a -m jiten.jmdict    --doctest
	$(PYCOV) -a -m jiten.kana      --doctest
	$(PYCOV) -a -m jiten.kanji     --doctest
	$(PYCOV) -a -m jiten.misc      --doctest
	$(PYCOV) -a -m jiten.pitch     --doctest
	$(PYCOV) -a -m jiten.sentences --doctest
	$(PYTHON) -mcoverage html
	$(PYTHON) -mcoverage report

clean: cleanup
	rm -f jiten/res/*.sqlite3
	rm -f jiten/_sqlite3_pcre.*.so
	$(MAKE) -C jiten/res/jmdict clean
	$(MAKE) -C jiten/res/sentences clean

cleanup:
	find -name '*~' -delete -print
	rm -fr jiten/__pycache__/ tmp-html/
	rm -fr build/ dist/ jiten.egg-info/
	rm -fr .coverage htmlcov/
	rm -fr jiten/.version
	$(MAKE) -C jiten/res/jmdict cleanup

validate-css:
	curl -sF "file=@jiten/static/style.css;type=text/css" \
	  -- "$(CSSV)" | grep -qF '$(CSSOK)'

# TODO
tmp-html:
	$(PYCOV) -m jiten.cli _serve_for 30 & pid=$$!; \
	mkdir -p tmp-html; sleep 5; \
	dl() { f="$$1"; shift; curl -sG $(URL)"$$@" > tmp-html/"$$f".html; }; \
	dl index ; \
	dl cat    /jmdict    -d max=10 -d word=yes --data-urlencode query=cat    ; \
	dl idiot  /jmdict    -d max=10 -d word=yes --data-urlencode query=idiot  ; \
	dl neko   /kanji     -d max=10 -d word=yes --data-urlencode query=ねこ   ; \
	dl hi     /kanji     -d max=10 -d word=yes --data-urlencode query=日     ; \
	dl kitten /sentences -d max=10             --data-urlencode query=kitten ; \
	dl stroke /stroke           ; \
	dl j-b-f  /jmdict/by-freq   ; \
	dl j-b-n1 /jmdict/by-jlpt/1 ; \
	dl j-b-n2 /jmdict/by-jlpt/2 ; \
	dl j-b-n3 /jmdict/by-jlpt/3 ; \
	dl j-b-n4 /jmdict/by-jlpt/4 ; \
	dl j-b-n5 /jmdict/by-jlpt/5 ; \
	dl k-b-f  /kanji/by-freq    ; \
	dl k-b-l  /kanji/by-level   ; \
	dl k-b-j  /kanji/by-jlpt    ; \
	wait $$pid

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
