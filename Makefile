SHELL = /bin/bash

.PHONY: test

test:
	export PYTHONPATH=$$PWD/src       ;\
	python3 -m jiten.jmdict --doctest ;\
	python3 -m jiten.misc   --doctest
