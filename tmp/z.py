import unicodedata as UD

import jiten.kanji as K
import jiten.misc as M

RADS = set("一丨丬丶丿乀乁乙乚乛乡亀亅二亠人亻儿入八冂冖冫几凵刀刁刂力勹匕匚匸十卜卩厂厶又口囗土士夂夊夕大夨女子孑孒孓宀寸小尢尣尸屮山巛工己已巳巾干幺广廴廾弋弓彐彑彡彳心忄戈戶户戸手扌才支攴文斉斗斤方无日曰月木欠止歯歹殳毋比毛氏气水火爪父爻爿片牙牛犬玄玉瓜瓦甘生用田疋疒癶白皮皿目矛矢石示禸禾穴立竜竹米糸纟缶网羊羽老而耒耳聿肉臣自至臼舌舛舟艮色艸虍虫血行衣襾見见角言讠谷豆豕豸貝贝赤走足身車辛辰辵邑酉釆里金钅長长門门阜隶隹雨靑非面革韋韦韭音頁页風风飛飞食饣首香馬马骨高髟鬥鬯鬲鬼魚鱼鳥鸟鹵鹿麥麦麻黃黍黑黹黽黾鼎鼓鼠鼻齊齐齒齿龍龙龜龟龠")

assert len(RADS) == 261

with open("tmp/WIKIPEDIA_RADS") as f:
  for i in range(1, 214+1):
    assert i == int(f.readline())
    l = f.readline().strip()
    x = set( c for c in l[1:] if (M.iscjk(c) or M.isradical(c))
               and not (c in K.RAD2KAN or c in K.KAN2RAD) )
    assert K.RAD2KAN[chr(0x2f00 - 1 + i)] == l[0]
    if x:
      y = set( c for c in x if M.isradical(c) )
      print("{:03} {} {} {}".format(i, l, x, y or "-"))
      for c in sorted(x):
        assert UD.category(c) != "Co"
        # if c not in RADS: print("NOT IN RADS:", c)
        print("==>", UD.name(c))
        print(c + l[0])
      print()
  assert () == tuple(f)
