#!/usr/bin/env python3
"""diff.py build.png tag -> per-section diff % (>24 on any channel), max channel delta, heatmaps."""
import sys, os
import numpy as np
from PIL import Image
Image.MAX_IMAGE_PIXELS = None
SECS = [("01 hero",0,960),("02 desc",960,738),("03 essentials",1698,1440),("04 starting blocks",3138,1748),
        ("05 inputs",4886,2310),("06 sketches",7196,1098),("07 exploration",8294,1406),("08 swap",9700,1492),
        ("09 testing",11192,1636),("10 onboarding",12828,1252),("11 home",14080,1356),("12 done",15436,1989),
        ("13 closer",17425,1900)]
D = os.path.dirname(os.path.abspath(__file__))
b = np.asarray(Image.open(sys.argv[1]).convert("RGB")).astype(int)
tag = sys.argv[2] if len(sys.argv) > 2 else "x"
os.makedirs(f"{D}/heat", exist_ok=True)
tot = 0; totpx = 0
for i, (name, y, h) in enumerate(SECS):
    r = Image.open(f"{D}/ref/{i+1:02d}.png").convert("RGBA")
    bg = Image.new("RGBA", r.size, (255, 255, 255, 255)); bg.alpha_composite(r)
    ref = np.asarray(bg.convert("RGB")).astype(int)
    bb = b[y:y+h]
    d = np.abs(bb - ref).max(2)
    bad = d > 24
    pct = bad.mean() * 100; tot += bad.sum(); totpx += bad.size
    print(f"{name:20s} diff {pct:6.3f}%  max {d.max():3d}  mean {np.abs(bb-ref).mean():.3f}")
    hm = (ref * 0.35 + 165).astype(np.uint8); hm[bad] = [255, 0, 0]
    Image.fromarray(hm).save(f"{D}/heat/{tag}_{i+1:02d}.png")
print(f"{'whole page':20s} diff {tot/totpx*100:6.3f}%")
