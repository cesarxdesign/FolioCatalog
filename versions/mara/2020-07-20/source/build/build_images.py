"""Cut Figma renders into the page's images (method of the Done2 build).
Sources (Figma renders, never redrawn):
  ref/sNN.png   get_screenshot of each section at scale 1
  exp/sNN@2.png download_assets export of each section at scale 2
  exp/sketches@1/@2, exp/rectangz@1/@2  node exports of 10 "sketches" (98:79050) and "rectangz" (98:79093)
Boxes are section coordinates (1x); the @2 crop is the same box at 2x.
Holes: rectangles where a live Figma text node sits inside a plate; they are painted with the
section background of that row (sampled at the section's left edge), so no text stays in a render."""
import json, os
from PIL import Image
import numpy as np
W = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(W, '..', 'site', 'img'); os.makedirs(OUT, exist_ok=True)
def ref(n): return Image.open(f'{W}/ref/s{n}.png').convert('RGB')
def ex(n):  return Image.open(f'{W}/exp/{n}.png').convert('RGB')

def rowbg(a, x=2):
    return a[:, x:x+1, :]  # (H,1,3)

def trim_box(im1, box, holes=(), thr=3):
    x, y, w, h = box
    a = np.asarray(im1).astype(int)
    bg = rowbg(a)[y:y+h]
    c = a[y:y+h, x:x+w]
    m = np.abs(c - bg).max(axis=2) > thr
    for hx, hy, hw, hh in holes:
        m[max(0,hy-y):max(0,hy-y+hh), max(0,hx-x):max(0,hx-x+hw)] = False
    ys, xs = np.where(m)
    x0, x1 = xs.min(), xs.max() + 1; y0, y1 = ys.min(), ys.max() + 1
    return (int(x + x0), int(y + y0), int(x1 - x0), int(y1 - y0))

def fill_holes(im, holes, s):
    a = np.asarray(im).copy()
    bg = a[:, 2*s:2*s+1, :]
    for hx, hy, hw, hh in holes:
        y0, y1, x0, x1 = s*hy, s*(hy+hh), s*hx, s*(hx+hw)
        a[y0:y1, x0:x1] = bg[y0:y1]
    return Image.fromarray(a)

def save(name, im1, im2, box, holes=(), s2=True):
    x, y, w, h = box
    if holes:
        im1 = fill_holes(im1, holes, 1); im2 = fill_holes(im2, holes, 2)
    c1 = im1.crop((x, y, x + w, y + h)); c2 = im2.crop((2*x, 2*y, 2*(x + w), 2*(y + h)))
    for c, suf in ((c1, '@1x'), (c2, '')):
        c.save(f'{OUT}/{name}{suf}.webp', quality=88, method=6)
        c.save(f'{OUT}/{name}{suf}.avif', quality=80, subsampling='4:4:4', speed=4)
    return {'name': name, 'box': [int(v) for v in box]}

def hole(rb, pad=3):
    x, y, w, h = rb
    return (int(np.floor(x)) - pad, int(np.floor(y)) - pad, int(np.ceil(x + w) - np.floor(x)) + 2*pad, int(np.ceil(y + h) - np.floor(y)) + 2*pad)

out = []
ONLY = os.environ.get('ONLY', '').split(',') if os.environ.get('ONLY') else None
prev = {o['name']: o for o in json.load(open(f'{W}/images.json'))} if os.path.exists(f'{W}/images.json') else {}
def plate(name, sec, region, holes=(), exact=False):
    if ONLY and name not in ONLY: out.append(prev[name]); return
    im1, im2 = ref(sec), ex(f's{sec}@2')
    box = region if exact else trim_box(im1, region, holes)
    o = save(name, im1, im2, box, holes); o['sec'] = sec; out.append(o); print(o)

plate('hero', '01', (0, 0, 1920, 960), exact=True)
plate('send', '03', (540, 520, 840, 1220))
# 04: phone + callout lines; the callout texts on the right are live, punched out
h04 = [hole(r) for r in [(1316.078,716,345.199,82.234), (1315.586,859.703,163.477,22.301), (1316.137,976.586,353.379,57.418), (1315.105,1294,330.176,87.121), (1155.105,578,339.891,87.121)]]
plate('audit', '04', (610, 560, 1100, 1080), h04)
plate('home-row', '05', (60, 700, 1800, 660))
plate('profile', '06', (500, 600, 920, 560), exact=True)
h07a = [hole((45.897,1404.072,31.867,10.162), 2), hole((1823.564,1404.115,25.625,10.119), 2)]
plate('bb-row', '07', (20, 975, 1880, 450), h07a)
h07b = [hole((160.149,1766.5,736.444,181.549), 3)]
plate('analysis-frame', '07', (125, 1735, 800, 246), h07b)
plate('bb-row2', '07', (20, 2270, 1880, 460))
plate('drawer', '07', (120, 2950, 220, 222))
plate('onb1', '08', (40, 1005, 1840, 180))
plate('onb2', '08', (40, 1396, 590, 180))
plate('warn', '08', (1410, 985, 22, 22))
plate('kyc', '09', (200, 830, 730, 720))
plate('faceid', '09', (990, 830, 730, 720))
plate('essentials', '11', (820, 530, 1010, 710), [hole((840.488,1178,304.445,47.268), 3)])
plate('system', '12', (800, 370, 960, 620))
plate('dress', '13', (60, 500, 1800, 640))
plate('catch', '14', (150, 690, 1620, 850))
plate('nop', '15', (150, 60, 1620, 850))
plate('rings', '16', (60, 692, 1800, 668))
plate('grid', '17', (30, 240, 1860, 2240))
# SF Symbol glyphs inside live 04 callouts, and the emoji of 14: small renders over spacers in the live text
plate('sf-octagon', '04', (1350, 606, 32, 28))
plate('sf-xx', '04', (1477, 975, 60, 30))
plate('emoji-up', '14', (445, 436, 34, 36))
plate('emoji-down', '14', (366, 476, 34, 36))
# 10: sketches and highlight rectangles, node exports (flattened on white), laid over the live 4.0 with multiply
for n in ('sketches', 'rectangz'):
    if ONLY and n not in ONLY: out.append(prev[n]); continue
    i1, i2 = ex(f'{n}@1'), ex(f'{n}@2')
    o = save(n, i1, i2, (0, 0, i1.size[0], i1.size[1])); o['sec'] = '10'; out.append(o); print(o)
json.dump(out, open(f'{W}/images.json', 'w'), indent=1)
