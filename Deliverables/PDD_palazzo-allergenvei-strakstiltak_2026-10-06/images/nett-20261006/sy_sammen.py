# Setter sammen skjermbilder av samme side tatt ved ulike rulleposisjoner til ett bilde av kortet.
#   python3 sy_sammen.py ut.png cardTop cardH cardLeft cardW  fil1:scrollY1 fil2:scrollY2 ...
# Skjermbildene er 1430 x 840 bildepunkter for et vindu paa 1280 x 752 punkter (foerste fane), og 1421 x 840 for
# 1280 x 757 (andre fane; sett VH=757).
import sys
from PIL import Image
ut = sys.argv[1]; top, h, left, w = map(int, sys.argv[2:6])
deler = [(a.rsplit(":", 1)[0], int(a.rsplit(":", 1)[1])) for a in sys.argv[6:]]
import os
VW, VH = 1280, int(os.environ.get('VH', '752'))
ims = [(Image.open(p).convert("RGB"), s) for p, s in deler]
W, H = ims[0][0].size
sx, sy = W / VW, H / VH
m = 12
y0, y1 = top - m, top + h + m          # sideomraadet som skal med, i punkter
x0, x1 = max(0, left - m), min(VW, left + w + m)
out = Image.new("RGB", (round((x1 - x0) * sx), round((y1 - y0) * sy)), "white")
dekket = y0
for im, s in ims:
    a = max(dekket, s); b = min(y1, s + VH)
    if b <= a: continue
    box = (round(x0 * sx), round((a - s) * sy), round(x1 * sx), round((b - s) * sy))
    out.paste(im.crop(box), (0, round((a - y0) * sy)))
    dekket = b
assert dekket >= y1, "skjermbildene dekker ikke hele kortet: %d < %d" % (dekket, y1)
out.save(ut)
print(ut, out.size, "deler:", len(ims))
