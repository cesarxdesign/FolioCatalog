#!/usr/bin/env python3
"""The sketches image, in its two files.

    python3 source/sketches.py

From the untouched Figma export (CodeCatalog/images/penfold/sketches-strip/export.png):
  - the ink is darkened: each pixel multiplied by itself three times, as three stacked multiply layers would
  - ink inside the two masks in source/ is Penfold blue in light and Penfold pink in dark
  - site/img/sketches-strip.webp       light: coloured ink on white, blended with multiply
  - site/img/sketches-strip-dark.webp  dark: white and coloured ink on black, blended with screen
The masks are the areas Cesar outlined on screenshots, 2026-09-29.
"""
import os
import numpy as np
from PIL import Image
Image.MAX_IMAGE_PIXELS = None
HERE = os.path.dirname(os.path.abspath(__file__))
EXPORT = os.path.join(HERE, *['..'] * 5, 'CodeCatalog', 'images', 'penfold', 'sketches-strip', 'export.png')
SIZE = (3974, 1210)
PINK, BLUE = (255, 80, 129), (80, 129, 255)          # #FF5081, #5081FF

v = np.asarray(Image.open(EXPORT).convert('L').resize(SIZE, Image.LANCZOS)).astype(np.float32) / 255
ink = (1 - v ** 3)[..., None]
def mask(name): return np.asarray(Image.open(os.path.join(HERE, name)).convert('L')).astype(np.float32)[..., None] / 255
mp, mb = mask('sketch-mask-pink.png'), mask('sketch-mask-blue.png')
mb = mb * (1 - mp)
both = mp + mb                                       # the two outlined areas share one colour per theme
light = 1 - ink * (1 - both * np.array(BLUE, np.float32) / 255)             # blue in light, black elsewhere
dark = ink * (both * np.array(PINK, np.float32) / 255 + (1 - both))         # pink in dark, white elsewhere
for name, a in (('sketches-strip.webp', light), ('sketches-strip-dark.webp', dark)):
    Image.fromarray((a * 255).round().astype(np.uint8)).save(os.path.join(HERE, '..', 'site', 'img', name), 'WEBP', quality=88, method=6)
print('sketches written')
