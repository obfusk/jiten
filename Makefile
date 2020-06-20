SHELL   := /bin/bash

CSSV    := https://jigsaw.w3.org/css-validator/validator
CSSOK   := Congratulations! No Error Found.

HTMLV   := https://html5.validator.nu
HTMLOK  := The document is valid HTML5

URL     := http://localhost:5000
H5VCMD  := html5validator --show-warnings --log INFO --no-langdetect

.PHONY: all test ci-test clean cleanup validate-css tmp-html
.PHONY: validate-html validate-html-curl validate-html-py

all:
	python3 -m jiten.cli setup

test:
	python3 -m jiten.app    --doctest --verbose
	python3 -m jiten.cli     _doctest --verbose
	python3 -m jiten.freq   --doctest --verbose
	python3 -m jiten.jmdict --doctest --verbose
	python3 -m jiten.kanji  --doctest --verbose
	python3 -m jiten.misc   --doctest --verbose

ci-test: test validate-css validate-html

clean: cleanup
	rm -f jiten/res/*.sqlite3

cleanup:
	find -name '*~' -delete -print
	rm -fr jiten/__pycache__/ tmp-html/

validate-css:
	curl -sF "file=@jiten/static/style.css;type=text/css" \
	  -- "$(CSSV)" | grep -qF '$(CSSOK)'

tmp-html:
	python3 -m jiten.cli serve & pid=$$!; \
	trap "kill $$pid" EXIT; mkdir -p tmp-html; sleep 5; \
	curl -sG $(URL) > tmp-html/index.html; \
	curl -sG $(URL)/jmdict -d max=10 --data-urlencode query=cat   \
	  > tmp-html/cat.html  ; \
	curl -sG $(URL)/jmdict -d max=10 --data-urlencode query=idiot \
	  > tmp-html/idiot.html; \
	curl -sG $(URL)/kanji  -d max=10 --data-urlencode query=ねこ  \
	  > tmp-html/neko.html ; \
	curl -sG $(URL)/kanji  -d max=10 --data-urlencode query=日    \
	  > tmp-html/hi.html   ; \
	curl -sG $(URL)/stroke > tmp-html/stroke.html

validate-html: tmp-html validate-html-curl validate-html-py

validate-html-curl:
	for file in $$( find tmp-html/ -name '*.html' | sort ); do \
	  echo "validating $$file..."; \
	  curl -sF "file=@$$file;type=text/html" -- "$(HTMLV)" \
	    | grep -qF '$(HTMLOK)' || exit 1; \
	done

validate-html-py:
	$(H5VCMD) --root tmp-html/
