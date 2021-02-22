#!/usr/bin/python3

import csv, xml.etree.ElementTree as ET

langs = "eng nld deu fra spa swe jpn".split()
data  = { k: {} for k in langs }
out   = {}

for lang in langs:
  with open(lang + "_sentences.tsv") as f:
    for line in f:
      i, _, x = line.strip().split("\t", maxsplit = 2)
      assert "\t" not in x
      data[lang][int(i)] = x

with open("links.csv") as f:
  for line in f:
    a, b = map(int, line.strip().split("\t"))
    if a not in data["jpn"]: continue
    out.setdefault(a, {})
    for lang in langs[:-1]:
      if b in data[lang]: out[a].setdefault(lang, data[lang][b])

with open("sentences_with_audio.csv") as f:
  for line in f:
    i, user, lic, url = line.rstrip("\n").split("\t")
    i = int(i)
    if "CC" not in lic or i not in out: continue
    info = url if url and url != "\\N" else user
    out[i]["audio"] = info + " (" + lic + ")"

for i, x in out.items():
  rest = ( x.get(k) or "-" for k in langs[:-1] + ["audio"] )
  print("\t".join([str(i), data["jpn"][i], *rest]))
