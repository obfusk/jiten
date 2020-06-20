SHELL = /bin/bash

.PHONY: all test clean cleanup

all:
	python3 -m jiten.cli setup

test:
	python3 -m jiten.app    --doctest --verbose
	python3 -m jiten.cli     _doctest --verbose
	python3 -m jiten.freq   --doctest --verbose
	python3 -m jiten.jmdict --doctest --verbose
	python3 -m jiten.kanji  --doctest --verbose
	python3 -m jiten.misc   --doctest --verbose

clean: cleanup
	rm -f jiten/res/*.sqlite3

cleanup:
	find -name '*~' -delete -print
