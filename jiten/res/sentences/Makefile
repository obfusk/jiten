SHELL := /bin/bash

AUDIO := https://downloads.tatoeba.org/exports/sentences_with_audio.tar.bz2
LINKS := https://downloads.tatoeba.org/exports/links.tar.bz2
BASE  := https://downloads.tatoeba.org/exports/per_language
ENG   := $(BASE)/eng/eng_sentences.tsv.bz2
DUT   := $(BASE)/nld/nld_sentences.tsv.bz2
GER   := $(BASE)/deu/deu_sentences.tsv.bz2
JAP   := $(BASE)/jpn/jpn_sentences.tsv.bz2

.PHONY: all download sentences audio clean

all: download sentences

download: clean
	wget -O "$$(basename "$(AUDIO)")" -- "$(AUDIO)"
	wget -O "$$(basename "$(LINKS)")" -- "$(LINKS)"
	wget -O "$$(basename "$(ENG)"  )" -- "$(ENG)"
	wget -O "$$(basename "$(DUT)"  )" -- "$(DUT)"
	wget -O "$$(basename "$(GER)"  )" -- "$(GER)"
	wget -O "$$(basename "$(JAP)"  )" -- "$(JAP)"
	tar xf links.tar.bz2 links.csv
	rm -f  links.tar.bz2
	tar xf sentences_with_audio.tar.bz2 sentences_with_audio.csv
	rm -f  sentences_with_audio.tar.bz2
	bunzip2 "$$(basename "$(ENG)")"
	bunzip2 "$$(basename "$(DUT)")"
	bunzip2 "$$(basename "$(GER)")"
	bunzip2 "$$(basename "$(JAP)")"

sentences:
	./tatoeba.py > SENTENCES

audio:
	set -e; \
	for i in $$( grep -Pv '\t-$$' SENTENCES | awk '{print $$1}' ); do \
	  [ -e audio/"$$i".mp3 ] || wget -O audio/"$$i".mp3 -- \
	    "https://audio.tatoeba.org/sentences/jpn/$$i.mp3"; \
	done

clean:
	rm -f *.bz2 *.csv *.tsv
