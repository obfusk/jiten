SHELL   := /bin/bash

CSSV    := https://jigsaw.w3.org/css-validator/validator
CSSOK   := Congratulations! No Error Found.

HTMLV   := https://html5.validator.nu
HTMLOK  := The document is valid HTML5

URL     := http://localhost:5000
H5VCMD  := html5validator --show-warnings --log INFO --no-langdetect

.PHONY: all test ci-test clean cleanup validate-css tmp-html
.PHONY: check-html validate-html validate-html-curl validate-html-py

all: ext
	python3 -m jiten.cli setup

test: all
	python3 -m jiten.app       --verbose --doctest
	python3 -m jiten.cli       --verbose  _doctest
	python3 -m jiten.freq      --verbose --doctest
	python3 -m jiten.jmdict    --verbose --doctest
	python3 -m jiten.kanji     --verbose --doctest
	python3 -m jiten.misc      --verbose --doctest
	python3 -m jiten.pitch     --verbose --doctest
	python3 -m jiten.sentences --verbose --doctest

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
	$(MAKE) -C jiten/res/jmdict cleanup

validate-css:
	curl -sF "file=@jiten/static/style.css;type=text/css" \
	  -- "$(CSSV)" | grep -qF '$(CSSOK)'

tmp-html:
	python3 -m jiten.cli serve & pid=$$!; \
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
	$(H5VCMD) --root tmp-html/

.PHONY: ext patch _package _publish

ext:
	python3 setup.py build_ext -i

patch:
	$(MAKE) -C jiten/res/jmdict all
	$(MAKE) -C jiten/res/jmdict cleanup

_package:
	python3 setup.py sdist bdist_wheel
	twine check dist/*

_publish: cleanup _package
	read -r -p "Are you sure? "; \
	[[ "$$REPLY" == [Yy]* ]] && twine upload dist/*.tar.gz
