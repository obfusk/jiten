SHELL = /bin/bash

.PHONY: all test clean cleanup

all:
	python3 -m jiten.cli setup

test:
	python3 -m jiten.freq   --doctest
	python3 -m jiten.jmdict --doctest
	python3 -m jiten.kanji  --doctest
	python3 -m jiten.misc   --doctest

clean: cleanup
	rm -f jiten/res/*.sqlite3

cleanup:
	find -name '*~' -delete -print
