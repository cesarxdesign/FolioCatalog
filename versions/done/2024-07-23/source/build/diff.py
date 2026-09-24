"""Per-section diff of the page capture against Figma's section renders.
usage: python3 diff.py build.png [tag]  -> prints table, writes heatmaps to heat/<tag>_sNN.png"""
import sys, os
from PIL import Image
import numpy as np
W = os.path.dirname(os.path.abspath(__file__))
SECS = [('01', 0, 960), ('02', 960, 738), ('03', 1698, 960), ('04', 2658, 1440), ('05', 4098, 1720),
        ('06', 5818, 3040), ('07', 8858, 2232), ('08', 11090, 2296), ('09', 13386, 2432),
        ('10', 15818, 2080), ('11', 17898, 2536)]
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
