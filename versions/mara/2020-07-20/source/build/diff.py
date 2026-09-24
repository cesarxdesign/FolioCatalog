"""Per-section diff of the page capture against Figma's section renders.
usage: python3 diff.py build.png [tag]"""
import sys, os
from PIL import Image
import numpy as np
W = os.path.dirname(os.path.abspath(__file__))
H = [960,762,2264,2343,1960,1912,3561,2040,2264,1858,1535,1241,1518,2161,1679,2189,2715]
SECS = []; y = 0
for i, h in enumerate(H): SECS.append(('%02d' % (i+1), y, h)); y += h
T = 24
build = np.asarray(Image.open(sys.argv[1]).convert('RGB')).astype(int)
tag = sys.argv[2] if len(sys.argv) > 2 else 'run'
os.makedirs(f'{W}/heat', exist_ok=True)
tot_bad = tot = 0
print(f"{'sec':4}{'diff%>24':>10}{'maxΔ':>6}{'meanΔ':>8}{'>8 %':>8}")
for n, y, h in SECS:
    ref = np.asarray(Image.open(f'{W}/ref/s{n}.png').convert('RGB')).astype(int)
    b = build[y:y + h]
    d = np.abs(b - ref).max(axis=2)
    bad = d > T
    tot_bad += bad.sum(); tot += bad.size
    print(f"{n:4}{100 * bad.mean():10.3f}{d.max():6d}{d.mean():8.3f}{100 * (d > 8).mean():8.3f}")
    hm = (np.asarray(Image.open(f'{W}/ref/s{n}.png').convert('L')) * 0.25 + 190).astype(np.uint8)
    hm = np.stack([hm] * 3, axis=2)
    hm[bad] = [255, 0, 0]
    hm[(d > 8) & ~bad] = [255, 190, 0]
    Image.fromarray(hm).save(f'{W}/heat/{tag}_s{n}.png')
print(f"all {100 * tot_bad / tot:.3f}%")
