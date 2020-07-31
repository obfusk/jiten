import csv, unicodedata as UD

import jiten.misc as M
import jiten.kanji as K

seen = set()
alts = set()
nora = set()

with open("tmp/kanji-radicals.csv", newline = "") as f:
  for r in csv.DictReader(f):
    kan = r["Radical"]
    if not kan or UD.category(kan) == "Co": continue
    alt = "".join(sorted( K.RAD2KAN.get(c, c) for c in r["Alternate"]
                          if UD.category(c) != "Co" ))
    if kan in K.RAD2KAN:
      rad, kan = kan, K.RAD2KAN[kan]
    else:
      rad = K.KAN2RAD.get(kan)
    if not rad and any( c in K.KAN2RAD for c in alt ):
      kans = [ c for c in alt if c in K.KAN2RAD ]
      alt   = "".join(sorted((set(alt) - set(kans[0:1])) | set(kan)))
      kan   = kans[0]
      rad   = K.KAN2RAD[kan]
    if rad:
      cod = ord(rad) - 0x2f00 + 1
      seen.add(cod)
      print("{:03} {}".format(cod, kan), end = "")
      if alt:
        for x in alt: alts.add(x)
        print(" ALT", alt)
      else:
        print()
    elif alt:
      print("WTF", kan, alt)
    else:
      nora.add(kan)

for k in nora - alts:
  print("NORAD", k, UD.name(k))

for k in sorted(set(range(1, 214+1)) - seen):
  print("-->", k, K.RADICALS[k-1])
