"""Cut the Figma renders into the page's images.

Sources (all Figma renders, never redrawn):
  ref/sNN.png      get_screenshot of each section at scale 1 (== download_assets export at 1x; checked on 06/07)
  exp/sNN@2.png    download_assets export of each section at scale 2
  exp/hero@1/@2    01 hero instance export
  exp/hex06@1/@2   06 "hexa grid" (15:3888) export
  exp/bg08@1/@2    08 "bg" (15:4745) export, render bounds 0,207 1920x1842 in section space
Crops are in section coordinates; the @2 crop is the same box at 2x.
"""
import json, os, sys
from PIL import Image
import numpy as np

W = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(W, '..', 'site', 'img')
os.makedirs(OUT, exist_ok=True)
Q = 88  # WebP quality

def ref(n): return Image.open(f'{W}/ref/s{n}.png').convert('RGB')
def ex(n):  return Image.open(f'{W}/exp/{n}.png').convert('RGB')

def trim_box(im1, box, bg=(255, 255, 255)):
    """shrink a crop box to the non-background ink of the 1x image (plus 1px), in section coords"""
    x, y, w, h = box
    a = np.asarray(im1.crop((x, y, x + w, y + h))).astype(int)
    m = (np.abs(a - np.array(bg)).max(axis=2) > 0)
    ys, xs = np.where(m)
    x0, x1 = max(0, xs.min() - 1), min(w, xs.max() + 2)
    y0, y1 = max(0, ys.min() - 1), min(h, ys.max() + 2)
    return tuple(int(v) for v in (x + x0, y + y0, x1 - x0, y1 - y0))

def save(name, im1, im2, box, holes=None, only1x=False):
    x, y, w, h = box
    c1 = im1.crop((x, y, x + w, y + h))
    c2 = None if only1x else im2.crop((2 * x, 2 * y, 2 * (x + w), 2 * (y + h)))
    if holes:
        c1 = c1.convert('RGBA'); c2 = c2.convert('RGBA')
        a1 = np.asarray(c1).copy(); a2 = np.asarray(c2).copy()
        for hx, hy, hw, hh in holes:
            a1[max(0, hy - y):max(0, hy - y + hh), max(0, hx - x):max(0, hx - x + hw), 3] = 0
            a2[max(0, 2 * (hy - y)):max(0, 2 * (hy - y + hh)), max(0, 2 * (hx - x)):max(0, 2 * (hx - x + hw)), 3] = 0
        c1 = Image.fromarray(a1); c2 = Image.fromarray(a2)
    kw = dict(quality=Q, method=6)
    if holes: kw['exact'] = True
    c1.save(f'{OUT}/{name}@1x.webp', **kw)
    if c2 is not None: c2.save(f'{OUT}/{name}.webp', **kw)
    # AVIF 4:4:4 alongside: lossy WebP is 4:2:0 and smears thin coloured UI text (>24 levels);
    # AVIF 4:4:4 q80 stays within 24 levels at a smaller size
    akw = dict(quality=80, subsampling='4:4:4', speed=4)
    c1.save(f'{OUT}/{name}@1x.avif', **akw)
    if c2 is not None: c2.save(f'{OUT}/{name}.avif', **akw)
    return {'name': name, 'box': box, 'only1x': only1x}

out = []
# 01 hero: the whole instance
out.append(save('hero', ex('hero@1'), ex('hero@2'), (0, 0, 1920, 960)))
# 03 emoji 15:3583 - the download_assets renderer has no emoji font (its export is blank white),
# so only get_screenshot's 1x render exists
out.append(save('emoji', ref('03'), None, (869, 565, 32, 40), only1x=True))
# 04 SF Symbol hexagon glyph of 15:3600 ("/" is live text; the glyph starts after x=168)
s04_1, s04_2 = ref('04'), ex('s04@2')
out.append(save('hexagon-glyph', s04_1, s04_2, (168, 432, 53, 55)))
# 04 twelve 144x264 "iPhone 8 - N" cards (840..1784 x 408..984, no effects)
out.append(save('hexagon-cards', s04_1, s04_2, (840, 408, 944, 576)))
# 05 Frame 1742
out.append(save('hood', ref('05'), ex('s05@2'), (645, 428, 1227, 852)))
# 06 hexa grid 15:3888 (bottom layer, rendered over the white section fill)
out.append(save('main-grid', ex('hex06@1'), ex('hex06@2'), (0, 0, 1920, 3040)))
# 06 Frame 1743 / 1744 at their render bounds (drop shadow r80), cut from the section render
s06_1, s06_2 = ref('06'), ex('s06@2')
out.append(save('main-row1', s06_1, s06_2, (58, 584, 1804, 1012)))
out.append(save('main-row2', s06_1, s06_2, (58, 1628, 1804, 1012)))
# 07 plate: everything that is not live text, over the CSS gradient, text lines punched out
holes = json.load(open(f'{W}/holes07.json')) if os.path.exists(f'{W}/holes07.json') else []
out.append(save('details', ref('07'), ex('s07@2'), (400, 600, 1520, 1100), holes=holes or None))
# 08 bg 15:4745 (render bounds 0,207 1920x1842) and Frame 1745 at its render bounds
bg1, bg2 = ex('bg08@1'), ex('bg08@2')
out.append(save('secondary-bg', bg1, bg2, (0, 0, 1920, 1842)))
out.append(save('secondary-row', ref('08'), ex('s08@2'), (58, 620, 1804, 1012)))
# 09 Frame 1751, 10 Frame 1752 at render bounds, trimmed to ink
s09_1 = ref('09'); out.append(save('onboarding-row', s09_1, ex('s09@2'), trim_box(s09_1, (58, 864, 1804, 1012))))
s10_1 = ref('10'); out.append(save('assessment-row', s10_1, ex('s10@2'), trim_box(s10_1, (0, 268, 1920, 1012))))
# 11 hexa grid 15:5407 + Frame 144895 (its LINEAR_BURN fill needs the grid behind it), above the caption
s11_1 = ref('11'); out.append(save('hero-grid', s11_1, ex('s11@2'), trim_box(s11_1, (0, 0, 1920, 2072))))

json.dump(out, open(f'{W}/images.json', 'w'), indent=1)
for o in out: print(o)
for f in sorted(os.listdir(OUT)): print(f, os.path.getsize(f'{OUT}/{f}'))
