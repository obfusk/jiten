.PHONY: all

all: kradfile.utf8

%.utf8: %
	iconv -f euc-jp -t utf8 < $< > $@
