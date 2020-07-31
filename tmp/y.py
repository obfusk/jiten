import unicodedata as UD

import jiten.misc as M
import jiten.kanji as K

VAR = { "⺍": "小" }
FIX = { "": "牙", "": "瓜", "": "韋",
        "⺐": "尢", "⺓": "幺", "⻑": "長" }
REV = { "羽": "羽" }

assert all( c in K.KAN2RAD for c in VAR.values() )
assert all( c in K.KAN2RAD for c in FIX.values() )

def kanji(x):
  return K.RAD2KAN.get(x, FIX.get(x, x))

with open("tmp/RADS") as f:
  for line in f:
    fields  = line.split("\t")
    kan     = kanji(fields[1])
    out     = []
    if kan in VAR:
      out += ["VAR!", VAR[kan]]
    elif "variant" in line:
      fld = fields[5].split()[-1][0]
      var = kanji(fld)
      if var in REV:
        kan, var = var, kan
        out.append("REV")
      if fld in FIX: out += ["FIX", fld]
      if kan == var:
        if fld in K.RAD2KAN: continue
        kan = fld
        out.append("SWP")
      assert not M.isradical(var)
      assert var in K.KAN2RAD
      out += ["VAR", var]
    else:
      assert UD.category(kan) != "Co"
      if kan in REV:
        kan = REV[kan]
        out.append("REV")
    assert kan not in K.RAD2KAN
    if M.isradical(kan)           : out.append("RAD")
    elif kan in K.KAN2RAD         : out.append("KAN")
    elif UD.category(kan) == "Co" : out.append("PRV")
    print(kan, *out)
