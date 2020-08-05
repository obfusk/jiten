#!/usr/bin/python3

import re, xml.etree.ElementTree as ET
import jiten.misc as M
import click

NS = "{http://www.wadoku.de/xml/entry}"

with open("wadoku-xml-20200705/wadoku.xml") as f:
  with click.progressbar(ET.parse(f).getroot(), width = 0,
                         label = "parsing wadoku") as bar:
    for e in bar:
      assert e.tag == NS+"entry"
      orth    = e.find(".//"+NS+"orth")
      hatsuon = e.find(".//"+NS+"hatsuon")
      accent  = e.find(".//"+NS+"accent")
      assert orth is not None
      assert hatsuon is not None
      assert "—" not in hatsuon.text
      if accent is not None and accent.text != "-":
        o = re.sub(r"[_＿…。  　･・'’×△(){}〈〉]", "", orth.text)
        h = re.sub(r"[_＿…。  　･・'’0-9<>/~:]|\[\w+\]", "",
                   hatsuon.text.replace("[Akz]", "—"))
        a = accent.text
        if o.isascii(): continue
        assert all( M.ishiragana(x) or x in "ー—" for x in h )
        assert all( x.isdigit() for x in a.split("—") )
        print(o, h, a)
