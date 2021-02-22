SHELL := /bin/bash

.PHONY: all clean cleanup update

all: jmdict.xml.gz kanjidic2.xml.gz

%.xml.gz: %-unpatched.xml.gz %.patch
	rm -f $@  $*{-unpatched,}.xml
	gunzip -k $*-unpatched.xml.gz
	cp -a     $*{-unpatched,}.xml
	patch     $*.{xml,patch}
	gzip      $*.xml

clean: cleanup
	rm -f {jmdict,kanjidic2}.xml.gz

cleanup:
	rm -f {jmdict,kanjidic2}{,-unpatched}.xml

update: clean
	wget -O    jmdict.xml.gz    "https://www.edrdg.org/pub/Nihongo/JMdict.gz"
	wget -O    kanjidic2.xml.gz "https://www.edrdg.org/pub/Nihongo/kanjidic2.xml.gz"
	gunzip    {jmdict,kanjidic2}.xml.gz
	gunzip -k {jmdict,kanjidic2}-unpatched.xml.gz
	diff -Naur    jmdict{-unpatched,}.xml > jmdict.patch    || true
	diff -Naur kanjidic2{-unpatched,}.xml > kanjidic2.patch || true
