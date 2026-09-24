"""For every live text element: best sub-pixel dx,dy of the build vs Figma's render, and ink ratio.
usage: python3 tshift.py capture.png measure.json [section filter]"""
import sys, json
from PIL import Image
import numpy as np
from secs import SECS, sec_of, SEC
build = np.asarray(Image.open(sys.argv[1]).convert('L')).astype(float)
M = json.load(open(sys.argv[2]))['lines.js']
flt = sys.argv[3].split(',') if len(sys.argv) > 3 else None
refs = {}
def sh(pr, pb, R=5):
    cs = [((np.roll(pb, -d) - pr) ** 2)[R + 1:-R - 1].sum() for d in range(-R, R + 1)]
    i = int(np.argmin(cs))
    if 0 < i < 2 * R:
        a, b, c = cs[i - 1], cs[i], cs[i + 1]
        den = a - 2 * b + c
        return i - R + (0.5 * (a - c) / den if den else 0)
    return i - R
for e in M:
    x, y, w, h = e['box']
    s = sec_of(y + 1)
    if flt and s not in flt: continue
    ref = refs.setdefault(s, np.asarray(Image.open(f'ref/s{s}.png').convert('L')).astype(float))
    oy = SEC[s]
    x0, y0, x1, y1 = int(x) - 6, int(y) - 6, int(x + w) + 7, int(y + h) + 7
    x0 = max(0, x0); x1 = min(1920, x1)
    r = ref[y0 - oy:y1 - oy, x0:x1]; b = build[y0:y1, x0:x1]
    bg = np.median(r)
    ri = np.abs(r - bg); bi = np.abs(b - bg)
    d = np.abs(r - b)
    print(f"{s} {e['i']:3} {e['txt'][:28]:28} dx {sh(ri.sum(0), bi.sum(0)):+.2f} dy {sh(ri.sum(1), bi.sum(1)):+.2f} ink {bi.sum()/max(ri.sum(),1):.3f} lines {len(e['lines'])} h {h:.0f} >24 {(d>24).mean()*100:.2f}%")
