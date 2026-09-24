"""Cut Figma's renders into the page's images, with every live string painted out.

Sources (all Figma renders, never redrawn):
  ref/sNN.png      get_screenshot of each section at scale 1
  exp/sNN@2.png    download_assets export of each section at scale 2
  exp/mask08@1/@2  08 "Mask group" 94:131036 export (the blurred map backdrop, no text);
                   its render bounds sit at 0,275 in section space (matched against the section render)
Live text covers: every line box of every live string (measured from the page itself, m.json),
padded 3px, is filled with what Figma has underneath it: interpolated down each column between
the untouched pixels above and below (white, or the mockups' soft drop shadow), or in 08 taken
from the Mask group backdrop export. Then each plate is trimmed to its remaining ink.
"""
import json, os, sys
from PIL import Image
import numpy as np
from secs import SECS, SEC, sec_of

W = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(W, '..', 'site', 'img')
os.makedirs(OUT, exist_ok=True)
Q = 88
PAD = 3
M = json.load(open(sys.argv[1] if len(sys.argv) > 1 else f'{W}/m.json'))['lines.js']

def ref(n): return Image.open(f'{W}/ref/s{n}.png').convert('RGB')
def ex(n):  return Image.open(f'{W}/exp/{n}.png').convert('RGB')

def backdrop(n, im1, im2):
    """what Figma has under the text in this section"""
    if n == '08':
        b1 = Image.new('RGB', im1.size, (255, 255, 255)); b2 = Image.new('RGB', im2.size, (255, 255, 255))
        b1.paste(ex('mask08@1'), (0, 275)); b2.paste(ex('mask08@2'), (0, 550))
        return b1, b2
    return Image.new('RGB', im1.size, (255, 255, 255)), Image.new('RGB', im2.size, (255, 255, 255))

def fill_vertical(a, m):
    """paint masked pixels by linear interpolation, per column, between the nearest unmasked
    pixels above and below"""
    a = a.astype(float)
    H = a.shape[0]
    for x in np.where(m.any(axis=0))[0]:
        ys = np.where(m[:, x])[0]
        br = np.where(np.diff(ys) > 1)[0]
        starts = np.r_[ys[0], ys[br + 1]]; ends = np.r_[ys[br], ys[-1]]
        for y0, y1 in zip(starts, ends):
            top = a[y0 - 1, x] if y0 > 0 else a[min(y1 + 1, H - 1), x]
            bot = a[y1 + 1, x] if y1 + 1 < H else top
            t = (np.arange(y0, y1 + 1) - (y0 - 1)) / (y1 + 2 - y0)
            a[y0:y1 + 1, x] = top[None, :] * (1 - t[:, None]) + bot[None, :] * t[:, None]
    return a

def inpaint(a, m, iters):
    """smooth fill of the masked pixels from their surroundings (harmonic, Jacobi iterations
    started from the column interpolation), so the soft drop shadows behind the text carry on
    without seams on any side. Works in place on the masked pixels' bounding window."""
    ys, xs = np.where(m)
    if len(ys) == 0: return a
    y0, y1 = max(0, ys.min() - 1), min(a.shape[0], ys.max() + 2)
    x0, x1 = max(0, xs.min() - 1), min(a.shape[1], xs.max() + 2)
    mm = m[y0:y1, x0:x1]
    sub = fill_vertical(a[y0:y1, x0:x1], mm)
    ring = (~mm) & (np.pad(mm, 1)[2:, 1:-1] | np.pad(mm, 1)[:-2, 1:-1] | np.pad(mm, 1)[1:-1, 2:] | np.pad(mm, 1)[1:-1, :-2])
    if np.ptp(sub[ring], axis=0).max() > 0:        # flat white needs no relaxation
        for _ in range(iters):
            nb = (np.roll(sub, 1, 0) + np.roll(sub, -1, 0) + np.roll(sub, 1, 1) + np.roll(sub, -1, 1)) / 4
            sub[mm] = nb[mm]
    a[y0:y1, x0:x1] = np.clip(np.rint(sub), 0, 255).astype(np.uint8)
    return a

def covered(n):
    im1, im2 = ref(n), ex(f's{n}@2')
    a1, a2 = np.asarray(im1).copy(), np.asarray(im2).copy()
    m1 = np.zeros(a1.shape[:2], bool); m2 = np.zeros(a2.shape[:2], bool)
    oy = SEC[n]
    b1, b2 = backdrop(n, im1, im2)
    for e in M:
        if sec_of(e['box'][1] + 1) != n: continue
        e1 = np.zeros(a1.shape[:2], bool); e2 = np.zeros(a2.shape[:2], bool)  # (bool: cheap)
        for x, y, w, h in e['lines']:
            y -= oy
            x0, y0 = int(np.floor(x - PAD)), int(np.floor(y - PAD))
            x1, y1 = int(np.ceil(x + w + PAD)), int(np.ceil(y + h + PAD))
            x0, y0 = max(0, x0), max(0, y0)
            e1[y0:y1, x0:x1] = True
            e2[2 * y0:2 * y1, 2 * x0:2 * x1] = True
        if n == '08':
            # textured backdrop: take it from the Mask group's own export
            a1[e1] = np.asarray(b1)[e1]; a2[e2] = np.asarray(b2)[e2]
        else:
            a1 = inpaint(a1, e1, 400); a2 = inpaint(a2, e2, 800)
    return Image.fromarray(a1), Image.fromarray(a2)

def trim_box(im1, box, bg=(255, 255, 255)):
    x, y, w, h = box
    a = np.asarray(im1.crop((x, y, x + w, y + h))).astype(int)
    m = (np.abs(a - np.array(bg)).max(axis=2) > 0)
    ys, xs = np.where(m)
    x0, x1 = max(0, xs.min() - 1), min(w, xs.max() + 2)
    y0, y1 = max(0, ys.min() - 1), min(h, ys.max() + 2)
    return tuple(int(v) for v in (x + x0, y + y0, x1 - x0, y1 - y0))

def save(name, im1, im2, box):
    x, y, w, h = box
    c1 = im1.crop((x, y, x + w, y + h))
    c2 = im2.crop((2 * x, 2 * y, 2 * (x + w), 2 * (y + h)))
    c1.save(f'{OUT}/{name}@1x.webp', quality=Q, method=6)
    c2.save(f'{OUT}/{name}.webp', quality=Q, method=6)
    # AVIF 4:4:4: lossy WebP is 4:2:0 and smears thin coloured UI text
    akw = dict(quality=80, subsampling='4:4:4', speed=4)
    c1.save(f'{OUT}/{name}@1x.avif', **akw)
    c2.save(f'{OUT}/{name}.avif', **akw)
    return {'name': name, 'box': list(box)}

out = []
# 01 hero: the whole instance (the logo is a vector, not text)
out.append(save('hero', ref('01'), ex('s01@2'), (0, 0, 1920, 960)))
# 03 Frame 34 (Twitter, Royal Mail, Toyota logos), 548.824,753 822.351x167: its pixel box
out.append(save('partners', ref('03'), ex('s03@2'), (548, 753, 824, 167)))
# 09 SF Symbol U+10004D in the live paragraph: its 25 x 36 line cell, cut before the text is painted out
out.append(save('sfglyph', ref('09'), ex('s09@2'), (1527, 706, 25, 36)))
PLATES = [('04', 'products'), ('06', 'v0'), ('08', 'v2'), ('09', 'toggles'), ('10', 'v3'),
          ('11', 'heat'), ('12', 'tiny'), ('14', 'final')]
for n, name in PLATES:
    c1, c2 = covered(n)
    h = [s[2] for s in SECS if s[0] == n][0]
    if n == '08':
        box = (0, 0, 1920, h)            # the backdrop spans the section
    else:
        box = trim_box(c1, (0, 0, 1920, h))
    c1.save(f'{W}/plate_s{n}.png')
    out.append(save(name, c1, c2, box))
# 13 vBIG: one product screen, whole section
out.append(save('big', ref('13'), ex('s13@2'), (0, 0, 1920, 1080)))

json.dump(out, open(f'{W}/images.json', 'w'), indent=1)
for o in out: print(o)
tot = 0
for f in sorted(os.listdir(OUT)):
    tot += os.path.getsize(f'{OUT}/{f}')
print('img total MB', tot / 1e6)
