Kanji Stroke Order Font v4.003
==============================

   Released 15 March 2020
   ======================

   Latest version at: http://nihilist.org.uk

INTRODUCTION
This font provides an easy way to view stroke order diagrams for over 6500
kanji, over 180 kana symbols, the Latin characters and quite a few other
symbols. I have also used it as a dumping ground for my own character
creation doodles.

My hope is that this font will assist people who are learning kanji. I
also hope it will help teachers of Japanese in the preparation of
classroom material. Beware that Japanese stroke order can differ from the
stroke order used in other languages that use Chinese characters.

HOW TO INSTALL AND USE THIS FONT
Install this font as you would any other TrueType font. In the parts of
your document where you want the kanji to be annotated with stroke order
numbers simply set your document's font to KanjiStrokeOrders. You will
need to set the size of the font to be large to allow the stroke order
numbers to show up: 100pt seems to be the minimum usable size.

As of version v4.003, KSOF works with Microsoft Word on Macintosh as well
as with Microsoft Word for Windows. This was the most significant change
from v4.001 to v4.002.

If you use the Anki flashcard program then the Anki website includes some
instructions on using custom fonts (such as KSOF) with that package. One
user reported needing to rename the font filename to remove the version
number to get it to work with AnkiDroid.

I have had one report from the field of Mac OS X 10.4.11 complaining about
missing OpenType data, although this does not happen with OS X 10.5. I am
told that KSOF works fine on OS X 10.4.11 if you ignore the warning, so it's
nothing to worry about. Thanks are due to Phil for reporting this.

LICENCE
This font may be freely distributed under the terms of the BSD-style licence
included with this archive in the file copyright.txt. This licence is very
permissive. In particular, the licence permits:
1. Use of the font for producing documents, including commercial documents.
2. Redistribution of the font, provided you leave the copyright notice intact.
   This includes selling the font commercially for a profit.
3. Use of the font in non-commercial and commercial software.

The kanji stroke order diagrams remain under the copyright of Ulrich Apel
and the AAAA and Wadoku projects. If you find this font useful then please
consider making a donation to the Wadoku project by pointing your Web
browser at http://www.wadoku.de and clicking on "Spenden".

INTEGRATION WITH JWPCE
This font enables you to view kanji stroke orders in JWPce. Set the "Big
Kanji Font" to KanjiStrokeOrders in the Options dialog. Some kanji stroke
order diagrams might show a different stroke count to that reported by
JWPce in the same kanji information window. This is because some kanji
have more than one valid stroke count.

TECHNICAL INFORMATION
I created this font by using the Batik library to convert the AAAA and
Wadoku projects' SVG files into high-resolution PNG images. I turned these
into a font using Fontforge. I use Fontforge for ongoing development.

The Kanji Stroke Order Font includes all the characters defined by JIS X
0208:1997, plus many more.

EXAMPLES
Included in this archive are two examples of the use of this font with popular
office software. They are in PDF format.

CORRECTIONS
As the changelog below shows, users have found quite a few errors in the
stroke orders diagrams. There are probably more. If you find any errors
please let me know by email: mail |at| nihilist (dot) org (dot) uk. You
can expect your changes to appear once enough fixes have accumulated to
make a new release worthwhile. When reporting an error, please tell me
what you think is wrong with the kanji and provide a link to a reference
if possible.

While working on this font I was interested to find that references
generally considered to be authoratitive sometimes disagree on stroke
order and even stroke count. U+53CE 収 and U+6E1B 減 are examples of
kanji that vary in documented stroke order. Furthermore, the
well-respected reference Kanjidic lists hundreds of kanji with multiple
valid stroke counts. Appendix E of the Kanjidic documentation discusses
stroke counts in detail. If you are not sure whether a character needs
correcting please let me know anyway so I can investigate. My primary
reference is http://kakijun.jp/.

OPENTYPE FEATURES
+smcp Small capitals for a-z. For example, in XeTeX use
      \font\smallcaps="KanjiStrokeOrders:+smcp" at 10pt
+utop Thomas More's Utopian characters plus the product integral symbol.
      The lowercase Latin characters map to their Utopian counterparts and z
      maps to the product integral symbol. Note that Thomas More wrote
      "Utopia" in Latin and, as such, this range of characters does not
      include the letters j, u, w or z (but z maps to the product integral
      symbol).
+spec The Sinclair ZX spectrum block graphics characters. These originally
      occupied the range 0x80 to 0x8F in the Sinclair ZX Spectrum character
      set. The symbol @ maps to the blank block and the letters A to O
      correspond to the non-blank block graphics. Why @? Because in the ZX
      Spectrum character set @ was 0x40 and A-O were 0x41-0x4F.

CHANGELOG
2020/03/15  4.003 Corrected errors reported by users and added more glyphs
                  to provide coverage of all KanjiVG glyphs.
                  Jōyō and other common use kanji that have changed:
                    U+4E00 一 Adjusted vertical position
                    U+4E91 云 Adjusted size
                    U+4FFA 俺 Adjusted size
                    U+5099 備 Reverted to textbook form
                    U+515C 兜 Adjusted size
                    U+698A 榊 Improved appearance
                    U+79B0 禰 Improved appearance
                    U+82A5 芥 Adjusted vertical position
                  Non-Jōyō kanji that have changed:
                    U+00D0 Ð Added stroke numbers to character
                    U+00DE Þ Added stroke numbers to character
                    U+00F0 ð Added stroke numbers to character
                    U+00FE þ Added stroke numbers to character
                    U+0262 ɢ Added
                    U+0274 ɴ Added
                    U+0280 ʀ Added
                    U+028F ʏ Added
                    U+0299 ʙ Added
                    U+029C ʜ Added
                    U+029F ʟ Added
                    U+1D00 ᴀ Added
                    U+1D04 ᴄ Added
                    U+1D05 ᴅ Added
                    U+1D07 ᴇ Added
                    U+1D0A ᴊ Added
                    U+1D0B ᴋ Added
                    U+1D0D ᴍ Added
                    U+1D0E ᴎ Added
                    U+1D0F ᴏ Added
                    U+1D18 ᴘ Added
                    U+1D1B ᴛ Added
                    U+1D1C ᴜ Added
                    U+1D20 ᴠ Added
                    U+1D21 ᴡ Added
                    U+1D22 ᴢ Added
                    U+34C1 㓁 Added
                    U+5173 关 Added
                    U+5300 匀 Added
                    U+55BB 喻 Added
                    U+5653 噓 Added
                    U+5723 圣 Added
                    U+57F6 埶 Added
                    U+59F8 姸 Added
                    U+5C03 尃 Added
                    U+5C5B 屛 Added
                    U+5E77 幷 Added
                    U+6220 戠 Added
                    U+65BF 斿 Added
                    U+687C 桼 Added
                    U+6C10 氐 Improved appearance
                    U+701E 瀞 Improve appearance
                    U+79BB 离 Added
                    U+7FF3 翳 Changed to handwritten form
                    U+96E9 雩 Added
                    U+A730 ꜰ Added
                    U+A731 ꜱ Added
                    U+A764 Ꝥ Added
                    U+A765 ꝥ Added
                    U+A766 Ꝧ Added
                    U+A767 ꝧ Added
                    U+A7AF ꞯ Added
                    U+F92E 冷 Added, identical to U+51B7 冷
                    U+F9A8 令 Added, identical to U+4EE4 令
                    U+F9AB 嶺 Added, identical to U+5DBA 嶺
                    U+F9AD 玲 Added, identical to U+73B2 玲
                    U+F9AF 羚 Added, identical to U+7F9A 羚
                    U+F9B0 聆 Added, identical to U+8046 聆
                    U+F9B1 鈴 Added, identical to U+9234 鈴
                    U+F9B2 零 Added, identical to U+96F6 零
                    U+F9B4 領 Added, identical to U+9818 領
                    U+2008A 𠂊 Added to private use area at U+F780
                    U+200A4 𠂤 Added to private use area at U+F781
                    U+26951 𦥑 Added to private use area at U+F782
2018/07/27  4.002 Added support for Microsoft Word on Macintosh.
                  Corrected errors reported by users, general clean-up and added some more glyphs
                  Jōyō and other common use kanji that have changed:
                    U+5026 倦 Updated to JIS2004 appearance
                    U+5099 備 Updated appearance to more common form
                    U+53A9 厩 Improved appearance by raising character
                    U+5FD7 巷 Improved appearance
                    U+76E1 盡 Corrected stroke order
                  Non-Jōyō kanji that have changed:
                    U+2150 ⅐ Removed hole
                    U+2151 ⅑ Removed hole
                    U+2152 ⅒ Removed hole
                    U+2153 ⅓ Removed hole
                    U+2154 ⅔ Removed hole
                    U+2155 ⅕ Removed hole
                    U+2156 ⅖ Removed hole
                    U+2157 ⅗ Removed hole
                    U+2158 ⅘ Removed hole
                    U+215A ⅚ Removed hole
                    U+215B ⅛ Removed hole
                    U+215C ⅜ Removed hole
                    U+215F ⅟ Removed hole
                    U+23FB ⏻ Added IEC Power symbol
                    U+23FC ⏼ Added IEC Power On-Off symbol
                    U+23FD ⏽ Added IEC Power On symbol
                    U+23FE ⏾ Added IEC Power Sleep symbol
                    U+2B58 ⭘ Added Heavy Circle = IEC Power Off symbol
                    U+4E02 丂 Added
                    U+4E04 丄 Added
                    U+4E05 丅 Added
                    U+4E0C 丌 Added
                    U+4E29 丩 Added
                    U+4E40 乀 Added
                    U+4E41 乁 Added
                    U+4E47 乇 Added
                    U+4E61 乡 Improved appearance
                    U+4E8D 亍 Added
                    U+4E96 亖 Added
                    U+53AD 厭 Improved appearance by raising character
                    U+58D7 壗 Corrected stroke order, clarified numbering
                    U+6108 愈 Updated to JIS2004 appearance
                    U+6260 扁 Improved appearance
2016/09/25  4.001 Corrected errors reported by users
                  Jōyō and other common use kanji that have changed:
                    U+5265 剥 Added numer for stroke 1
                    U+584A 塊 Clarified numbering
                    U+5EDF 廟 Updated to JIS2004 appearance
                    U+63C3 揃 Updated to JIS2004 appearance
                    U+6F81 澁 Clarified numbering
                    U+714E 煎 Improved appearance
                    U+76E3 監 Clarified numbering
                    U+840E 萎 Adjusted position relative to baseline
                    U+8888 袈 Corrected stroke order
                    U+88CF 裏 Clarified numbering
                    U+8AD6 論 Clarified numbering
                    U+8CBC 貼 Corrected appearance
                    U+9061 遡 Added extra stroke in line with JIS X 0213:2004
                    U+9A57 驗 Corrected stroke order and clarified numbering
                    U+9A5A 驚 Clarified numbering
                  Non-Jōyō kanji that have changed:
                    U+34B5 㒵 Corrected appearance
                    U+5078 偸 Corrected appearance
                    U+5118 儘 Corrected stroke order
                    U+516A 兪 Corrected appearance
                    U+5614 嘔 Clarified numbering
                    U+56C0 囀 Updated to JIS2004 appearance
                    U+56CE 囎 Corrected appearance
                    U+589F 墟 Corrected stroke order
                    U+58D7 壗 Clarified numbering
                    U+58E4 壤 Clarified numbering
                    U+5910 夐 Improved appearance
                    U+5C28 尨 Corrected stroke order
                    U+5D90 嶐 Clarified numbering
                    U+601B 怛 Corrected appearance
                    U+6026 怦 Corrected stroke order
                    U+60BD 悽 Corrected stroke order
                    U+61CB 懋 Corrected stroke order
                    U+6260 扠 Clarified numbering
                    U+63C4 揄 Corrected appearance
                    U+6801 栁 Increased size
                    U+6961 楡 Corrected appearance
                    U+69DD 槝 Clarified numbering
                    U+6A62 橢 Corrected stroke order
                    U+6B16 欖 Clarified numbering
                    U+6B1F 欟 Clarified numbering
                    U+6B54 歔 Corrected stroke order and clarified numbering
                    U+6BB2 殲 Corrected stroke order
                    U+6CEA 泪 Corrected appearance
                    U+6E1D 渝 Corrected appearance
                    U+6E76 湶 Corrected stroke order
                    U+6F80 澀 Corrected to 17 strokes
                    U+701B 瀛 Corrected stroke order and clarified numbering
                    U+71E0 燠 Corrected stroke order
                    U+7228 爨 Corrected stroke order
                    U+745C 瑜 Corrected appearance
                    U+7609 瘉 Corrected appearance
                    U+7AC4 竄 Corrected appearance
                    U+7AC7 竇 Clarified numbering
                    U+7BAD 箭 Updated to JIS2004 appearance
                    U+7BDD 篝 Corrected appearance of stroke 15
                    U+7CB2 粲 Corrected stroke order
                    U+7C6C 籬 Corrected appearance
                    U+7E90 纐 Corrected stroke order
                    U+7FB8 羸 Corrected stroke order
                    U+81BD 膽 Corrected stroke order and appearance
                    U+84AD 蒭 Corrected stroke order
                    U+8590 薐 Corrected stroke order
                    U+8753 蝓 Corrected appearance
                    U+8805 蠅 Improved appearance of stroke 13 and clarified numbering
                    U+8836 蠶 Clarified numbering
                    U+891E 褞 Clarified numbering
                    U+8960 襠 Clarified numbering
                    U+89A6 覦 Corrected appearance
                    U+8A85 誅 Corrected stroke order
                    U+8B6B 譫 Corrected stroke order and appearance
                    U+8B96 讖 Corrected stroke order and clarified numbering
                    U+8D0A 贊 Clarified numbering
                    U+8D0D 贍 Corrected stroke order
                    U+8D0F 贏 Corrected stroke order
                    U+8E10 踐 Corrected stroke order
                    U+8E50 蹐 Corrected stroke order
                    U+8E81 躁 Corrected stroke order and clarified numbering
                    U+8EAA 躪 Clarified numbering
                    U+8EDB 軛 Clarified numbering
                    U+8F15 輕 Clarified numbering
                    U+8F57 轗 Corrected stroke order and appearance, clarified numbering
                    U+903E 逾 Corrected appearance
                    U+905E 遞 Corrected stroke order
                    U+91C1 釁 Corrected stroke order
                    U+936E 鍮 Corrected appearance
                    U+95CC 闌 Clarified numbering
                    U+974D 靍 Clarified numbering
                    U+991E 餞 Corrected stroke order
                    U+9AE3 髣 Added missing stroke 6, clarified numbering
                    U+9B06 鬆 Clarified numbering
                    U+9B22 鬢 Clarified numbering
                    U+9B43 魃 Clarified numbering
                    U+9C47 鱇 Clarified numbering
                    U+9ED0 黐 Corrected to 23 strokes
                               The character U+9ED0 黐 has changed twice before in
                               KSOF. The reference I use is http://kakijun.jp and
                               this shows 22 strokes in the image but 23 strokes in
                               the reference information. For this release I have
                               settled on 23 strokes.
                    U+FA1E 羽 Corrected appearance
                    U+FA1F 﨟 Corrected size
                    U+FA49 爫 Added
                    U+FA66 辶 Added
                  Cleaned up self-intersecting paths in font (no significant visible effect).
                  Cleaned up inconsistent directions in font (no visible effect).
2016/07/04  4.000 Corrected errors reported by users and added some characters.
                  Many of the changes relate to JIS X 0213:2004. In detail:
                  Jōyō kanji that have changed:
                    U+5099 備 Improved appearence
                    U+50C5 僅 Corrected appearence and added stroke in line with JIS X 0213:2004
                    U+525D 剝 Added
                    U+52E7 勧 Adjusted position of some stroke order numbers for clarity without changing the order
                    U+55C5 嗅 Changed appearence
                    U+5632 嘲 Corrected appearence slightly in line with JIS X 0213:2004
                    U+5861 塡 Corrected appearence
                    U+5C5E 属 Corrected direction of stroke 4 (slightly controversial)
                    U+60E7 惧 Corrected appearence
                    U+6144 慄 Corrected order of strokes 7,8 and 9
                    U+6975 極 Adjusted position of the number for stroke 7 slightly for clarity.
                    U+6BC0 毀 Corrected stroke order
                    U+6DEB 淫 Corrected appearence in line with JIS X 0213:2004
                    U+6E80 満 Improved appearence slightly
                    U+6EBA 溺 Corrected appearence in line with JIS X 0213:2004
                    U+6F5F 潟 Corrected order of strokes 6 and 7
                    U+7B8B 箋 Corrected appearence
                    U+8108 脈 Improved appearence
                    U+81A8 膨 Improved appearence
                    U+81FC 臼 Reversed strokes 3 and 4
                    U+8328 茨 Corrected appearence in line with JIS X 0213:2004
                    U+845B 葛 Corrected appearence in line with JIS X 0213:2004
                    U+8511 蔑 Corrected appearence in line with JIS X 0213:2004
                    U+853D 蔽 Corrected appearence in line with JIS X 0213:2004
                    U+8AE7 諧 Reversed strokes 10 and 11
                    U+8AFE 諾 Clarified numbering
                    U+8B0E 謎 Added an extra stroke in line with JIS X 0213:2004
                    U+8CED 賭 Corrected appearence
                    U+905C 遜 Added an extra stroke in line with JIS X 0213:2004
                    U+9061 遡 Corrected appearence in line with JIS X 0213:2004
                    U+91C8 釈 Improved appearence slightly by unmerging stroke 10 from the stroke itself
                    U+9699 隙 Corrected appearence in line with JIS X 0213:2004
                    U+96E2 離 Improved appearence (more like handwritten version)
                    U+96EA 雪 Improved appearence slightly
                    U+9905 餅 Corrected appearence in line with JIS X 0213:2004
                    U+990C 餌 Corrected appearence in line with JIS X 0213:2004
                  Non-Jōyō kanji that have changed:
                    U+2E84 ⺄ Added
                    U+2EA9 ⺩ Added
                    U+2EAC ⺬ Added
                    U+2EBA ⺺ Added
                    U+2ECF ⻏ Added
                    U+2ED6 ⻖ Added
                    U+2ED7 ⻗ Added
                    U+342C 㐬 Added
                    U+353E 㔾 Added
                    U+38FA 㣺 Added
                    U+4ECD 仍 Swapped strokes 3 and 4
                    U+4FAB 侫 Corrected stroke order
                    U+5026 倦 Corrected stroke order and appearence
                    U+502A 倪 Corrected stroke order
                    U+5055 偕 Corrected stroke order
                    U+5080 傀 Clarified stroke order by adjusting position of number 6
                    U+5109 儉 Repositioned numbers for clarity
                    U+5132 儲 Corrected stroke order and appearence
                    U+514E 兎 Corrected stroke order and appearence
                    U+5152 兒 Corrected stroke order
                    U+51A4 冤 Corrected stroke order and corrected appearence in line with JIS X 0213:2004
                    U+524F 剏 Corrected stroke order
                    U+52F5 勵 Corrected stroke order
                    U+5333 匳 Corrected stroke order
                    U+5342 卂 Added
                    U+537F 卿 Corrected appearence in line with JIS X 0213:2004
                    U+53A9 厩 Corrected appearence in line with JIS X 0213:2004
                    U+53DA 叚 Added
                    U+53DB 叛 Corrected appearence in line with JIS X 0213:2004
                    U+53DF 叟 Corrected appearence in line with JIS X 0213:2004
                    U+53F1 叱 Moved stroke 4 back to starting on right side. See also U+FAFF.
                    U+54C8 哈 Corrected stroke order
                    U+54E8 哨 Corrected appearence in line with JIS X 0213:2004
                    U+5557 啗 Corrected stroke order
                    U+558A 喊 Corrected stroke order
                    U+55B0 喰 Corrected appearence in line with JIS X 0213:2004
                    U+55BF 喿 Added
                    U+5618 嘘 Improved appearence of numbering
                    U+5642 噂 Corrected appearence in line with JIS X 0213:2004
                    U+564C 噌 Corrected appearence in line with JIS X 0213:2004
                    U+57A0 垠 Corrected stroke order
                    U+582F 堯 Reversed strokes 8 and 9
                    U+5835 堵 Corrected appearence in line with JIS X 0213:2004
                    U+583A 堺 Corrected stroke order
                    U+583D 堽 Corrected appearence and stroke order
                    U+590C 夌 Added
                    U+590D 复 Added
                    U+5967 奧 Corrected stroke order by swapping strokes 7 and 8
                    U+5969 奩 Corrected stroke order
                    U+5A29 娩 Corrected appearence in line with JIS X 0213:2004
                    U+5A29 娩 Corrected stroke order
                    U+5A36 娶 Corrected stroke order
                    U+5A40 婀 Corrected stroke order
                    U+5A41 婁 Clarified numbering
                    U+5A6A 婪 Corrected stroke order
                    U+5ABD 媽 Corrected stroke order
                    U+5AC2 嫂 Corrected stroke order
                    U+5AE3 嫣 Corrected stroke order
                    U+5B70 孰 Corrected stroke order
                    U+5BEB 寫 Corrected stroke order
                    U+5C05 尅 Corrected stroke order
                    U+5C08 專 Corrected stroke order
                    U+5C1E 尞 Added
                    U+5C51 屑 Corrected appearence in line with JIS X 0213:2004
                    U+5C60 屠 Corrected stroke order and appearence in line with JIS X 0213:2004
                    U+5CEF 峯 Corrected stroke order
                    U+5D6C 嵬 Adjusted position of some stroke order numbers for clarity without changing the order
                    U+5DAC 嶬 Corrected stroke order
                    U+5DCD 巍 Adjusted position of some stroke order numbers for clarity without changing the order
                    U+5DF7 巷 Corrected appearence in line with JIS X 0213:2004
                    U+5E43 幃 Corrected stroke count
                    U+5E96 庖 Corrected appearence in line with JIS X 0213:2004
                    U+5F98 徘 Corrected appearence in line with JIS X 0213:2004
                    U+5FBD 徽 Corrected appearence and stroke order in line with JIS X 0213:2004
                    U+6062 恢 Corrected appearence in line with JIS X 0213:2004
                    U+60FB 惻 Corrected stroke order
                    U+6108 愈 Corrected appearence in line with JIS X 0213:2004
                    U+6127 愧 Clarified numbering
                    U+6173 慳 Corrected stroke order
                    U+61FD 懽 Corrected stroke order
                    U+6221 戡 Corrected stroke order
                    U+6241 扁 Corrected appearence in line with JIS X 0213:2004
                    U+6283 抃 Corrected stroke order
                    U+6302 挂 Corrected stroke order
                    U+633D 挽 Corrected appearence in line with JIS X 0213:2004
                    U+6372 捲 Corrected appearence and stroke order in line with JIS X 0213:2004
                    U+6406 搆 Corrected stroke order
                    U+641C 搜 Corrected stroke order
                    U+647A 摺 Corrected appearence in line with JIS X 0213:2004
                    U+64B0 撰 Corrected appearence and stroke order in line with JIS X 0213:2004
                    U+64BB 撻 Corrected stroke order
                    U+64D4 擔 Corrected stroke order
                    U+64E2 擢 Corrected appearence in line with JIS X 0213:2004
                    U+6505 攅 Corrected stroke order
                    U+651C 攜 Corrected stroke order
                    U+6666 晦 Corrected appearence and stroke order in line with JIS X 0213:2004
                    U+66C9 曉 Reversed strokes 11 and 12
                    U+6736 朶 Corrected stroke order by swapping strokes 1 and 2
                    U+6753 杓 Corrected appearence in line with JIS X 0213:2004
                    U+6801 栁 Added
                    U+6883 梃 Corrected stroke order
                    U+688F 梏 Corrected stroke order
                    U+691B 椛 Changed appearence
                    U+6962 楢 Corrected appearence in line with JIS X 0213:2004
                    U+698A 榊 Corrected appearence and stroke order in line with JIS X 0213:2004
                    U+6994 榔 Corrected appearence and stroke order in line with JIS X 0213:2004
                    U+69CC 槌 Corrected appearence and stroke order in line with JIS X 0213:2004
                    U+69D0 槐 Corrected appearence and improved number placement
                    U+69F9 槹 Corrected stroke order
                    U+6A0B 樋 Corrected appearence and stroke order in line with JIS X 0213:2004
                    U+6A3D 樽 Corrected appearence in line with JIS X 0213:2004
                    U+6A48 橈 Improved position of numbers 9 and 12
                    U+6A9C 檜 Corrected stroke order
                    U+6ADB 櫛 Corrected appearence and stroke order in line with JIS X 0213:2004
                    U+6B1D 欝 Corrected stroke order
                    U+6B4E 歎 Corrected appearence and stroke order in line with JIS X 0213:2004
                    U+6C10 氐 Added
                    U+6C72 汲 Corrected appearence and stroke order in line with JIS X 0213:2004
                    U+6C9B 沛 Corrected in line with JIS X 0213:2004
                    U+6EA2 溢 Corrected appearence in line with JIS X 0213:2004
                    U+6ED4 滔 Corrected stroke order
                    U+6F23 漣 Corrected appearence and stroke order in line with JIS X 0213:2004
                    U+6F91 澑 Corrected stroke order
                    U+7009 瀉 Corrected stroke order
                    U+7015 瀕 Corrected appearence and stroke order in line with JIS X 0213:2004
                    U+701E 瀞 Corrected appearence and stroke order in line with JIS X 0213:2004
                    U+7026 瀦 Corrected appearence and stroke order in line with JIS X 0213:2004
                    U+7058 灘 Corrected appearence and stroke order in line with JIS X 0213:2004
                    U+707C 灼 Corrected appearence in line with JIS X 0213:2004
                    U+70AC 炬 Improved appearence
                    U+7109 焉 Corrected stroke order
                    U+7130 焰 Corrected stroke order
                    U+7149 煉 Corrected appearence and stroke order in line with JIS X 0213:2004
                    U+7155 煕 Corrected stroke order
                    U+717D 煽 Corrected appearence and stroke order in line with JIS X 0213:2004
                    U+723C 爼 Adjusted position digit 9
                    U+724C 牌 Corrected appearence and stroke order in line with JIS X 0213:2004
                    U+727D 牽 Fixed stroke order
                    U+7296 犖 Corrected stroke order
                    U+72E0 狠 Corrected stroke order
                    U+730A 猊 Corrected stroke order
                    U+7337 猷 Corrected appearence in line with JIS X 0213:2004
                    U+73F1 珱 Corrected stroke order
                    U+7425 琥 Reversed strokes 7 and 8
                    U+7470 瑰 Corrected appearence
                    U+74A2 璢 Corrected stroke order
                    U+74F2 瓲 Corrected stroke order
                    U+7511 甑 Corrected appearence and stroke order in line with JIS X 0213:2004
                    U+751E 甞 Improved position of numbering
                    U+754B 畋 Corrected stroke order
                    U+7550 畐 Added
                    U+75BC 疼 Corrected appearence in line with JIS X 0213:2004
                    U+75FA 痺 Improved appearence
                    U+7620 瘠 Corrected stroke order
                    U+7627 瘧 Corrected stroke order
                    U+7661 癡 Corrected stroke order
                    U+7758 睘 Added
                    U+7768 睨 Corrected stroke order
                    U+77A5 瞥 Corrected appearence in line with JIS X 0213:2004
                    U+77DA 矚 Corrected stroke order
                    U+78FD 磽 Improved position of number 10
                    U+7907 礇 Corrected stroke order
                    U+7941 祁 Corrected appearence and stroke order in line with JIS X 0213:2004
                    U+7947 祇 Corrected appearence and stroke order in line with JIS X 0213:2004
                    U+79B0 禰 Corrected appearence and stroke order in line with JIS X 0213:2004
                    U+79E3 秣 Corrected stroke order
                    U+79E4 秤 Corrected appearence in line with JIS X 0213:2004
                    U+79EC 秬 Corrected appearence
                    U+7A0D 稍 Corrected stroke order
                    U+7A17 稗 Corrected appearence and stroke order in line with JIS X 0213:2004
                    U+7A3B 稻 Corrected stroke order
                    U+7A62 穢 Adjusted position of some numbers
                    U+7A63 穣 Improved number spacing for 11 and 12
                    U+7A7F 穿 Corrected appearence and stroke order in line with JIS X 0213:2004
                    U+7AC4 竄 Corrected stroke order
                    U+7AC8 竈 Corrected stroke order in line with JIS X 0213:2004
                    U+7ACA 竊 Corrected appearence and corrected stroke count to 22
                    U+7B08 笈 Corrected appearence and stroke order in line with JIS X 0213:2004
                    U+7BC7 篇 Corrected appearence and stroke order in line with JIS X 0213:2004
                    U+7BF6 篶 Corrected stroke order
                    U+7C3E 簾 Corrected appearence in line with JIS X 0213:2004
                    U+7C6C 籬 Corrected appearence
                    U+7C7E 籾 Corrected appearence in line with JIS X 0213:2004
                    U+7CA6 粦 Added
                    U+7CAE 粮 Corrected stroke order
                    U+7CC0 糀 Corrected stroke order
                    U+7DBD 綽 Corrected stroke order
                    U+7E21 縡 Corrected stroke order
                    U+7E8E 纎 Corrected stroke order
                    U+7FDF 翟 Added
                    U+7FEB 翫 Improved number positions and corrected appearence in line with JIS X 0213:2004
                    U+7FF0 翰 Corrected appearence in line with JIS X 0213:2004
                    U+80D6 胖 Corrected stroke order
                    U+817F 腿 Corrected appearence and stroke order in line with JIS X 0213:2004
                    U+81DF 臟 Corrected stroke order
                    U+81E7 臧 Corrected stroke order
                    U+8201 舁 Corrected stroke order
                    U+8202 舂 Corrected stroke order
                    U+8205 舅 Corrected stroke order
                    U+820A 舊 Corrected stroke order
                    U+821B 舛 Corrected stroke order
                    U+8258 艘 Corrected appearence and stroke order in line with JIS X 0213:2004
                    U+8271 艱 Corrected stroke order
                    U+8277 艷 Reversed order of strokes 16 and 17
                    U+8292 芒 Corrected appearence in line with JIS X 0213:2004
                    U+82A6 芦 Corrected appearence in line with JIS X 0213:2004
                    U+82E1 苡 Corrected stroke order
                    U+83DF 菟 Corrected stroke order
                    U+8479 葹 Reversed order of strokes 10 and 11
                    U+8490 蒐 Adjusted position of number for stroke 7 without changing the stroke order
                    U+84D9 蓙 Corrected stroke order
                    U+84EC 蓬 Corrected appearence and stroke order in line with JIS X 0213:2004
                    U+854B 蕋 Corrected appearence and stroke order
                    U+8588 薈 Adjusted position of some numbers
                    U+85A9 薩 Corrected appearence in line with JIS X 0213:2004
                    U+85AF 薯 Corrected appearence and stroke order in line with JIS X 0213:2004
                    U+85F7 藷 Corrected stroke order and appearence in line with JIS X 0213:2004
                    U+86A4 蚤 Corrected stroke order
                    U+86F8 蛸 Corrected appearence in line with JIS X 0213:2004
                    U+8755 蝕 Corrected appearence and stroke order in line with JIS X 0213:2004
                    U+877F 蝿 Corrected position of numeral 6 and improved appearence of number 11
                    U+8782 螂 Corrected stroke order
                    U+87EF 蟯 Improved position of numbers 11 and 14
                    U+8836 蠶 Clarified numbering
                    U+88F2 裲 Corrected stroke order
                    U+8938 褸 Corrected stroke order
                    U+8956 襖 Corrected appearence and stroke order in line with JIS X 0213:2004
                    U+8974 襴 Corrected stroke order
                    U+89E7 觧 Corrected stroke order
                    U+8A0A 訊 Corrected appearence in line with JIS X 0213:2004
                    U+8A3B 註 Corrected appearence in line with JIS X 0213:2004
                    U+8AB9 誹 Corrected appearence in line with JIS X 0213:2004
                    U+8AC2 諂 Corrected stroke order
                    U+8AFA 諺 Corrected appearence in line with JIS X 0213:2004
                    U+8B14 謔 Corrected stroke order
                    U+8B2C 謬 Corrected appearence in line with JIS X 0213:2004
                    U+8C50 豐 Reversed order of strokes 16 and 17
                    U+8C79 豹 Corrected appearence in line with JIS X 0213:2004
                    U+8C8E 貎 Corrected stroke order
                    U+8CB2 貲 Corrected stroke order
                    U+8D13 贓 Corrected stroke order
                    U+8DA8 趨 Reversed order of strokes 1 and 2.
                    U+8E30 踰 Improved appearence
                    U+8E48 蹈 Corrected stroke order
                    U+8F45 轅 Corrected stroke order
                    U+8F61 轡 Corrected stroke order
                    U+8FBB 辻 Corrected stroke order and appearence in line with JIS X 0213:2004
                    U+8FBF 辿 Corrected stroke order and appearence in line with JIS X 0213:2004
                    U+8FC2 迂 Corrected stroke order and appearence in line with JIS X 0213:2004
                    U+8FC4 迄 Corrected appearence and stroke order in line with JIS X 0213:2004
                    U+8FE6 迦 Corrected appearence and stroke order in line with JIS X 0213:2004
                    U+9017 逗 Corrected stroke order and appearence in line with JIS X 0213:2004
                    U+9019 這 Corrected appearence and stroke order in line with JIS X 0213:2004
                    U+9022 逢 Corrected appearence and stroke order in line with JIS X 0213:2004
                    U+903C 逼 Corrected appearence and stroke order in line with JIS X 0213:2004
                    U+9041 遁 Corrected appearence and stroke order in line with JIS X 0213:2004
                    U+9112 鄒 Corrected stroke order
                    U+912D 鄭 Corrected appearence and stroke order in line with JIS X 0213:2004
                    U+9130 鄰 Corrected shape and stroke order
                    U+914B 酋 Corrected appearence in line with JIS X 0213:2004
                    U+91C6 釆 Swapped strokes 4 and 5
                    U+91C9 釉 Reversed strokes 4 and 5
                    U+91F5 釵 Reversed order of strokes 10 and 11
                    U+9248 鉈 Corrected stroke order
                    U+9306 錆 Corrected appearence and stroke order in line with JIS X 0213:2004
                    U+939A 鎚 Corrected appearence and stroke order in line with JIS X 0213:2004
                    U+9453 鑓 Corrected appearence and stroke order in line with JIS X 0213:2004
                    U+95AD 閭 Adjusted position of some numbers
                    U+95BB 閻 Corrected stroke order
                    U+9677 陷 Corrected stroke order
                    U+9697 隗 Corrected appearence and reversed order of strokes 5 and 6
                    U+9708 霈 Corrected stroke order
                    U+9713 霓 Corrected stroke order
                    U+974D 靍 Added
                    U+974F 靏 Added
                    U+9768 靨 Corrected stroke order
                    U+9784 鞄 Corrected appearence and stroke order in line with JIS X 0213:2004
                    U+9798 鞘 Corrected appearence in line with JIS X 0213:2004
                    U+97DC 韜 Corrected stroke order
                    U+97DC 韜 Corrected stroke order
                    U+9824 頤 Corrected stroke order
                    U+98F4 飴 Corrected appearence and stroke order in line with JIS X 0213:2004
                    U+9910 餐 Corrected appearence in line with JIS X 0213:2004
                    U+9912 餒 Corrected stroke order
                    U+9921 餡 Corrected stroke order
                    U+992E 餮 Corrected stroke order
                    U+993D 餽 Improved appearence
                    U+9957 饗 Corrected appearence and stroke order in line with JIS X 0213:2004
                    U+9A19 騙 Corrected appearence and stroke order in line with JIS X 0213:2004
                    U+9A37 騷 Corrected strokes 12 & 13
                    U+9A55 驕 Corrected stroke order by swapping strokes 1 and 2
                    U+9A64 驤 Reversed order of strokes 26 and 27
                    U+9AE2 髢 Corrected stroke order
                    U+9B29 鬩 Corrected stroke order
                    U+9B2F 鬯 Corrected stroke order
                    U+9B43 魃 Adjusted position of some numbers slightly without changing the stroke order
                    U+9B44 魄 Adjusted position of some numbers slightly without changing the stroke order
                    U+9B4D 魍 Adjusted position of some numbers slightly without changing the stroke order
                    U+9B4F 魏 Adjusted position of some numbers slightly without changing the stroke order
                    U+9B51 魑 Improved positioning of numbers 4 and 5
                    U+9BD6 鯖 Corrected appearence and stroke order in line with JIS X 0213:2004
                    U+9BE2 鯢 Corrected stroke order
                    U+9C2F 鰯 Corrected appearence in line with JIS X 0213:2004
                    U+9C52 鱒 Corrected appearence in line with JIS X 0213:2004
                    U+9D60 鵠 Corrected stroke order and appearence in line with JIS X 0213:2004
                    U+9DBA 鶺 Corrected stroke order and improved appearence
                    U+9E91 麑 Corrected stroke order
                    U+9E91 麑 Corrected stroke order
                    U+9EA5 麥 Corrected stroke order
                    U+9ED0 黐 Corrected stroke count to 22
                    U+9ED4 黔 Corrected stroke order
                    U+9EE5 黥 Corrected stroke order
                    U+9EF6 黶 Improved appearence
                    U+9F07 鼇 Corrected stroke order
                    U+9F08 鼈 Corrected stroke order
                    U+9F20 鼠 Corrected order of strokes 3 and 4
                    U+9F2C 鼬 Corrected stroke order
                    U+F9DC 隆 Added
                    U+FA10 塚 Added
                    U+FA1F 﨟 Added
                    U+FA32 免 Added
                  Other characters:
                    U+2261 ≡ Corrected width
                    U+226B ≫ Corrected width
                    U+2536 ┶ Corrected location within bounding box
                    U+25DD ◝ Corrected location within bounding box
                    U+2400-U+2426 Added
                    U+FAFF 𠮟 Version of 叱 with stroke 4 starting on the left side,
                           in line with the official Joyo standard. This character
                           is supposed to live at U+20B9F and that is outside of
                           KSOF's encoding space so I have put it in a private use
                           area for users who would like to use this version.
2014/03/18  3.001 Corrected errors reported by users and added a few characters. In detail:
                  U+0126 Ħ added Maltese H-bar
                  U+0127 ħ added Maltese h-bar
                  U+01C0 ǀ added Nama dental click
                  U+01C1 ǁ added Nama lateral click
                  U+01C2 ǂ added Nama alveolar click
                  U+058F ֏ added Armenian Dram symbol
                  U+20B9 ₹ added Indian Rupee symbol
                  U+20BA ₺ added Turkish Lira symbol
                  U+2217 ∗ added mathematical asterisk operator
                  U+2248 ≈ added mathematical almost equal to
                  U+41F3 䇳 added new Jōyō character
                  U+4EC2 丬 added
                  U+5099 備 converted to handwritten version
                  U+529E 办 added
                  U+53F1 叱 corrected to bring into line with Jōyō standard
                  U+55A9 喩 updated to look more like Jōyō standard
                  U+5631 嘱 improved placement of stroke order numbers
                  U+5632 嘲 updated to look more like Jōyō standard
                  U+5C5E 属 improved placement of stroke order numbers
                  U+67F5 柵 removed unwanted spike from glyph
                  U+6975 極 changed back to 12 strokes
                  U+6F5F 潟 corrected stroke order again
                  U+714E 煎 updated to look more like Jōyō standard
                  U+7259 牙 converted to handwritten version, changed stroke count
                  U+7BB8 箸 added dot to bring into line with Jōyō standard
                  U+7C60 籠 improved placement of stroke order numbers
                  U+7DFB 緻 improved appearance of glyph
                  U+7E7D 繭 improved placement of stroke order numbers
                  U+8877 衷 changed to 10 strokes
                  U+8A6E 詮 updated to look more like Jōyō standard
                  U+8CED 賭 added dot to bring into line with Jōyō standard
                  U+8EB1 躱 corrected stroke order
                  U+9009 选 added
                  U+90B8 邸 clarified numbering
                  U+96BE 难 added
                  U+97CB 韋 improved appearance
                  U+97D3 韓 updated to look more like Jōyō standard
                  U+9905 餅 corrected to bring into line with Jōyō standard
                  U+990C 餌 corrected to bring into line with Jōyō standard
                  U+F981 女 added CJK compatibility version of 'woman'
                  U+F9D1 六 added CJK compatibility version of 'six'
2012/05/27  3.000 Added missing Jinmeiyou kanji and miscellaneous other kanji
                  and symbols. Corrected errors reported by users. In detail:
                  U+9B31 鬱 corrected order
                  U+9EFD 黽 corrected order
                  U+9F9C 龜 corrected order
                  U+8805 蠅 corrected order
                  U+7E69 繩 corrected order
                  U+9F9D 龝 corrected order
                  U+9EA9 麩 extended stroke 6 downwards
                  U+85CF 藏 corrected order
                  U+624D 才 corrected appearance
                  U+6F5F 潟 corrected order
                  U+8FB6 辶 added controversial fourth stroke back in
                  U+74E7 瓧 added missing stroke
                  U+7511 甑 added missing stroke
                  U+74EE 瓮 corrected order
                  U+74F8 瓸 corrected order
                  U+7483 璃 added (controversial) extra stroke
                  U+96E2 離 added (controversial) extra stroke
                  U+6A8E 檎 added (controversial) extra stroke
                  U+79BD 禽 added (controversial) extra stroke
                  U+7ACA 竊 added (controversial) extra stroke
                  U+9ED0 黐 added (controversial) extra stroke
                  U+753A 町 beautified
                  U+7DFB 緻 added extra stroke
                  U+5750 坐 corrected (controversial) stroke order
                  U+632B 挫 corrected (controversial) stroke order
                  U+805E 聞 beautified
                  U+53D6 取 beautified
                  U+767A 発 beautified
                  U+31C0 ㇀ added
                  U+31C1 ㇁ added
                  U+31C2 ㇂ added
                  U+31C3 ㇃ added
                  U+31C4 ㇄ added
                  U+31C5 ㇅ added
                  U+31C6 ㇆ added
                  U+31C7 ㇇ added
                  U+31C8 ㇈ added
                  U+31C9 ㇉ added
                  U+31CA ㇊ added
                  U+31CB ㇋ added
                  U+31CC ㇌ added
                  U+31CD ㇍ added
                  U+31CE ㇎ added
                  U+31CF ㇏ added
                  U+31D0 ㇐ added
                  U+31D1 ㇑ added
                  U+31D2 ㇒ added
                  U+31D3 ㇓ added
                  U+31D4 ㇔ added
                  U+31D5 ㇕ added
                  U+31D6 ㇖ added
                  U+31D7 ㇗ added
                  U+31D8 ㇘ added
                  U+31D9 ㇙ added
                  U+31DA ㇚ added
                  U+31DB ㇛ added
                  U+31DC ㇜ added
                  U+31DD ㇝ added
                  U+31DE ㇞ added
                  U+31DF ㇟ added
                  U+31E0 ㇠ added
                  U+31E1 ㇡ added
                  U+31E2 ㇢ added
                  U+31E3 ㇣ added
                  U+9A6C 马 added
                  U+4E44 乄 added
                  U+3514 㔔 added
                  U+5861 塡 added
                  U+9830 頰 added
                  U+6B65 步 added
                  U+6D89 涉 added
                  U+6BCF 每 added
                  U+FA41 敏 added
                  U+FA30 侮 added
                  U+FA45 海 added
                  U+FA3D 悔 added
                  U+FA44 梅 added
                  U+4FF1 俱 added
                  U+4FE0 俠 added
                  U+FA47 漢 added
                  U+FA22 諸 added
                  U+FA5B 者 added
                  U+FA5A 署 added
                  U+FA43 暑 added
                  U+FA5C 臭 added
                  U+5DE2 巢 added
                  U+FA4C 社 added
                  U+FA4E 祈 added
                  U+FA51 祝 added
                  U+FA19 神 added
                  U+FA1A 祥 added
                  U+FA4D 祉 added
                  U+FA4F 祐 added
                  U+FA50 祖 added
                  U+FA52 禍 added
                  U+FA53 禎 added
                  U+FA1B 福 added
                  U+FA61 視 added
                  U+79B1 禱 added
                  U+72C0 狀 added
                  U+90DE 郞 added
                  U+FA26 都 added
                  U+F929 朗 added
                  U+FA64 賓 added
                  U+8CF4 賴 added
                  U+665A 晚 added
                  U+FA67 逸 added
                  U+F928 廊 added
                  U+FA48 煮 added
                  U+FA5F 著 added
                  U+FA33 勉 added
                  U+7028 瀨 added
                  U+FA55 突 added
                  U+6DDA 淚 added
                  U+F9D0 類 added
                  U+FA65 贈 added
                  U+589E 增 added
                  U+FA57 練 added
                  U+FA3F 憎 added
                  U+FA37 嘆 added
                  U+FA38 器 added
                  U+537D 卽 added
                  U+FA62 謁 added
                  U+FA31 僧 added
                  U+6A6B 橫 added
                  U+6EAB 溫 added
                  U+6E34 渴 added
                  U+FA69 響 added
                  U+FA56 節 added
                  U+FA68 難 added
                  U+FA63 謹 added
                  U+6B77 歷 added
                  U+66C6 曆 added
                  U+F936 虜 added
                  U+FA54 穀 added
                  U+FA3B 層 added
                  U+FA3A 墨 added
                  U+FA34 勤 added
                  U+FA59 繁 added
                  U+7DA0 綠 added
                  U+7DE3 緣 added
                  U+5BEC 寬 added
                  U+5FB7 德 added
                  U+FA40 懲 added
                  U+5FB5 徵 added
                  U+F91D 欄 added
                  U+FA4B 碑 added
                  U+7DD6 緖 added
                  U+9304 錄 added
                  U+85B0 薰 added
                  U+934A 鍊 added
                  U+865B 虛 added
                  U+64CA 擊 added
                  U+7626 瘦 added
                  U+63ED 揭 added
                  U+7E61 繡 added
                  U+7130 焰 added
                  U+91AC 醬 added
                  U+9DD7 鷗 added
                  U+FA16 猪 added
                  U+840A 萊 added
                  U+6451 摑 added
                  U+985A 顚 added
                  U+FA46 渚 added
                  U+541E 吞 added
                  U+87EC 蟬 added
                  U+7C1E 簞 added
                  U+7E6B 繫 added
                  U+8523 蔣 added
                  U+881F 蠟 added
                  U+FA4A 琢 added
                  U+9EB5 麵 added
                  U+5020 倠 added
                  U+34B5 㒵 added
                  U+4E37 丷 added
                  U+3031 〱 added
                  U+3032 〲 added
                  U+3033 〳 added
                  U+3034 〴 added
                  U+3035 〵 added
                  U+3018 〘 added
                  U+3019 〙 added
                  U+2022 • added
                  U+2023 ‣ added
                  U+30A0 ゠ added
                  U+2E2E ⸮ added
                  U+303D 〽 added
                  U+303F 〿 added
                  U+303E 〾 added
                  U+3038 〸 added
                  U+3039 卄 added
                  U+303A 〺 added
                  U+5344 卄 added
                  U+3037 〷 added
                  U+303B 〻 added
                  U+3030 〰 added
                  U+2460-U+24FF added (circled and parenthesized numbers and
                              letters)
                  U+2150-U+215f added (fractions)
                  U+2160-U+2188 added (Roman numerals)
                  U+2189 ↉ added
                  U+2126 Ω added
                  U+2127 ℧ added
                  U+213A ℺ added
                  U+2141 ⅁ added
                  U+2100 ℀ added
                  U+2101 ℁ added
                  U+2104 ℄ added
                  U+2105 ℅ added
                  U+2106 ℆ added
                  U+2109 ℉ added
                  U+2116 № added
                  U+2117 ℗ added
                  U+2120 ℠ added
                  U+2121 ℡ added
                  U+212A K added
                  U+2132 Ⅎ added
                  U+213B ℻ added
                  U+2142 ⅂ added
                  U+2143 ⅃ added
                  U+2144 ⅄ added
                  U+214B ⅋ added
                  U+214D ⅍ added
                  U+214E ⅎ added
                  U+2654-2667 added (chess and playing card suits)
                  U+3004 〄 added
                  U+2614 ☔ added
                  U+2602 ☂ added
                  U+F81A new JIS symbol added as private use character. Can be
                         accessed as 〄 with +smcp feature.
                  U+32CF ㋏ added
                  U+3250 ㉐ added
                  U+327F ㉿ added
                  U+2690 ⚐ added
                  U+2691 ⚑ added
                  U+26AD ⚭ added
                  U+26AE ⚮ added
                  U+26AF ⚯ added
                  U+26A0 ⚠ added
                  U+26A1 ⚡ added
                  U+F81B KPS ACA1 added
                  U+F81C KPS ACA2 added
2011/03/29  2.016 Added Thomas More's Utopian characters (see +utop above) at
                  U+F800 to U+F818. Added Product Integral symbol (see +utop
                  above) at U+F919. Added Sinclair ZX Spectrum block graphics
                  at U+F7F0 to U+F7FF. Added radicals at U+91D2, U+2ECA, U+8A01,
                  U+2EB6, U+2EAA, U+2EB7, U+2EA7, U+2EBB, U+7529, U+9763,
                  U+2EBC. Improved readability of U+9751. Adding missing character
                  glyph at U+0000.
2010/10/05  2.015 Removed one stroke from U+6357, notionally in compliance with
                  JIS X 0213 and the Unicode reference table but actually
                  because someone suggested it. There are many other characters
                  in KSOF that don't match JIS X 0213 but I don't intend to
                  change those; I made an exception for U+6357 because it's slated
                  to become a Joyo kanji. Corrected U+6E90, U+646F, U+7D68,
                  U+8650, U+6F5F, U+6557, U+8FB6 (controversial: it is unclear
                  whether this radical has 3 or 4 strokes). Added the following
                  extra radicals thanks to the generous help of Durand D'souza:
                  U+722B, U+2E99 (an unusual radical), U+6236, U+4E5A, U+725C,
                  U+2F21, U+8980, U+72AD, U+9751, U+6C35, U+9578, U+2EAE,
                  U+8FB5, U+5C23, U+5DDC, U+4E61, U+6237, U+6B7A, U+7CF9, U+8080.
                  Corrected U+718A. Added U+FA35 (variant of U+5351). Corrected
                  U+62C9. Shortened first stroke of U+308A. Shortened U+30FC.
2009/10/04  2.014 Added missing stroke order numbers to U+30EE, U+4EDD, U+9FA0.
2009/08/30  2.013 Changed U+53CE to 4-stroke version. Updated U+5099 with more
                  common version of cliff radical. Clarified U+6163. Corrected
                  U+7CA5, U+8258, U+5396
2008/12/29  2.012 Corrected U+544E, U+9D28, U+6388, U+5D8B
2008/10/01  2.011 Corrected U+9280, U+8607, U+6089, U+6955, U+7566, U+79A6,
                  U+7B08, U+9803, U+86E4, U+88DF. Clarified U+8511.
2008/07/17  2.010 Corrected U+74DC, U+9CE9, U+79BD, U+8DA8, U+82BB, U+50FB,
                  U+4FB6, U+586B, U+5835, U+5C3B, U+63F7, U+64E2. Clarified
                  U+50AD. Thanks once again to Scott Krogh.
2008/01/02: 2.009 Corrected U+76FE, U+8846, U+885B, U+5171. Thanks to Aaron
                  and Scott Krogh for spotting these.
2008/04/04: 2.008 Corrected U+5440, U+5BDE, U+6357, U+6E76, U+74DC, U+7C6C,
                  U+6A8E, U+6A23, U+9244, U+85AC, U+7CDE. Merged in the
                  Choumei v1.10 glyphs, thus providing KanjiStrokeOrders with
                  all the JIS 0208 characters. Added support for small caps.
2008/03/03: 2.007 Corrected U+641C, U+854B, U+6F80, U+83DF, U+5C65, U+65C6,
                  U+6F01, U+750D, U+750E, U+750C, U+7504, U+7503, U+74E9,
                  U+821B, U+74F1, U+5178, U+82E1, U+5BC3, U+9B42, U+6F11,
                  U+5E43, U+91D0, U+74F8, U+74EE, U+74F0, U+74F7, U+7513,
                  U+7505, U+7E4A, U+7515, U+6975, U+64D2, U+79BD, U+6F13,
                  U+6A8E, U+9B51, U+7DFB. Removed glyph list and moved &, ', (,
                  ) and * into their correct encoding slots. Correction from
                  Aaron: U+6E1B.
2008/02/29: 2.006 Corrections from Aaron: U+5EA7, U+51F8. Fixed
                  appearance of many characters and increased the overall
                  size of the glyphs.
2008/02/27: 2.005 More corrections from Scott Krogh: U+6570, U+6551, U+7B20,
                  U+4FC4, U+4F3C, U+74F6, U+629E, U+96EA, U+4E21, U+6E80,
                  U+5EFB, U+5EB6, U+534A, U+7554, U+754F, U+5224, U+5C04,
                  U+8DEF, U+96A3, U+9F62, U+5B9B, U+6028, U+990A, U+8A55.
                  Replaced Tuffy glyphs with those from Choumei, thus making
                  the font more consistent in appearence. Added a list of
                  glyphs provided by the font.
2008/01/14: 2.004 Fixed bugs in U+5BA2, U+843D, U+539F, U+9ED2, U+9B5A, U+5B89,
                  U+6728, U+837B, U+56E0, U+5EAB, U+78E8, U+61BE, U+6545,
                  U+790E, U+96F2, U+8328, U+596E, U+97FB, U+9054, U+5742,
                  U+70AD, U+5897 and U+66DC. Many thanks to the eagle-eyed
                  Scott Krogh for pointing out the errors.
2007/12/13: 2.003 Fixed bug with missing stroke number at U+5144 and adjusted
                  offset of U+4E2D.
2007/05/08: 2.002 Fixed bug whereby hiragana 'mo' was missing.
2007/01/08: 2.001 Improved the character 'n'. Corrected the character U+5E83.
                  Fixed the character spacing.
2006/12/28: 2.0   Greatly expanded with new stroke order diagrams to cover many
                  more kanji, the Latin alphabet, punctuation and some other
                  symbols. This used a fresh set of SVG data from Ulrich Apel.
2006/10/31: 1.01  Corrected the text strings embedded in the font.
2006/10/27: 1.0   Initial revision

ACKNOWLEDGEMENTS
Almost all the work for this font was done by the AAAA and Wadoku projects
under the supervision of Ulrich Apel. I just had the idea of turning the
SVG data into a font and did so. Thanks are due to Scott, Aaron, Paul,
Jeremy, Mifune-san, Gerrit, Brian, Noli, William, Alex, Jerome, Neale,
Nicolas, Przemyslaw, Piotrek, James, Tobias, Jakob, Edgar, Olga, Reinaert,
Mr. Yoon, Meirav, Alfredo, Josh, Sebastian, Samuli, Eugene, Jeff, Gerard,
Inoue-san, Ahmed, Grant, Takao-san, Michael, Kitamura-san, Shibuya-san,
Minh and Herouth for reporting errors in the stroke order data and making
suggestions for improvements. I have fixed all these errors in the current
version. Thanks also to Durand D'souza for doing the background research
on the Kanji radicals I added in version 2.015.

An especially big thank you is due to Toshirō-san, who sent me corrections
for literally hundreds of characters for the V4.0 release.

Please keep the feedback coming; I always welcome corrections and suggestions.

Tim Eyre

mail |at| nihilist (dot) org (dot) uk

