.PHONY: all

all: base_aggregates.txt.nobom wordfreq_ck.utf8

base_aggregates.txt.nobom: base_aggregates.txt
	tail -c +4 $< > $@

wordfreq_ck.utf8: wordfreq_ck
	iconv -f EUC-JISX0213 -t utf8 < $< > $@
