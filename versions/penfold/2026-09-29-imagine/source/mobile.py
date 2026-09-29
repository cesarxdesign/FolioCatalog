#!/usr/bin/env python3
"""Two pairs above the Mobile item: each a desktop screen with its mobile twin laid over its left edge,
the same components derived for both platforms. Fund first, then the dashboard.

    python3 source/mobile.py        rewrites the pairs between the MOBILE markers in site/index.html

Screens are CodeCatalog's modular-* screens (desktop/screen.html, mobile/snippet.html), both cropped
to the first 812px of their frames. The two pairs share one geometry: the phone is as tall as the
desktop frame, dropped by a fifth of that height, and stops short of where the desktop content starts,
so it covers only the desktop's empty left margin.
"""
import os, re, importlib.util
HERE = os.path.dirname(os.path.abspath(__file__))
spec = importlib.util.spec_from_file_location('flow33', os.path.join(HERE, 'flow33.py'))
f = importlib.util.module_from_spec(spec); spec.loader.exec_module(f)
SITE = os.path.join(HERE, '..', 'site', 'index.html')
MOB = os.path.abspath(os.path.join(HERE, *['..'] * 5, 'CodeCatalog', 'screens', 'penfold', 'mobile'))

PAIRS = [('modular-fund', 'Choosing a fund'), ('modular-dashboard', 'The dashboard')]
WIDTH, GAP, FH = 820, 32, 812                      # 820: the Modular and Mobile list; 812: the crop
DW, MW = 1200, 375
PW = (WIDTH - GAP) / 2                             # one pair
EDGE = 223 / DW                                    # the earliest desktop content, dashboard's title, as a share of the width
D = (PW - 12) / (1 + MW / DW - EDGE)               # desktop width, so the phone ends 12px short of that content
H = D * FH / DW                                    # desktop height = phone height
M = H * MW / FH                                    # phone width
DROP = round(H / 5)

# the crop cuts into the next panel down; paint that sliver like the screen above it (on request, 2026-09-29)
COVER = {'modular-fund': (782, '#F6F6F6')}         # screen: (y where the white Risk acceptance panel starts, colour above)

def mobile(sid):
    src = open(os.path.join(MOB, sid, 'snippet.html'), encoding='utf-8').read()
    inner = re.search(r'<template shadowrootmode="open">([\s\S]*)</template>', src).group(1)
    css = re.search(r'<style>([\s\S]*?)</style>', inner).group(1)
    body = re.sub(r'<style>[\s\S]*?</style>', '', inner, count=1).strip()
    if sid in COVER:
        y, col = COVER[sid]
        body += '<div style="position:absolute;left:0;top:%dpx;width:%dpx;height:%dpx;background:%s;z-index:99"></div>' % (y, MW, FH - y, col)
    return css, body

def win(cls, sid, kind, fw, tw, css, body):
    css = ":host{display:block;width:%dpx;font-family:'Montserrat',-apple-system,sans-serif;color:#133253}\n%s" % (fw, css)
    return ('<div class="%s" style="--fw:%d;--tw:%.3f" data-screen="penfold/%s/%s"><div class="win"><div class="pg">'
            '<template shadowrootmode="open"><style>\n%s\n</style>\n%s\n</template></div></div></div>' % (cls, fw, tw, kind, sid, css, body))

pairs = []
for sid, label in PAIRS:
    pairs.append('<div class="pair" role="img" aria-label="%s, on desktop and on mobile">\n%s\n%s\n</div>' % (
        label, win('dt', sid, 'desktop', DW, D, *f.load(sid)), win('mb', sid, 'mobile', MW, M, *mobile(sid))))
block = ('<!-- MOBILE start: built by source/mobile.py from CodeCatalog screens, do not edit by hand -->\n'
         '<div class="duo" style="--pw:%.3f;--dw:%.3f;--mw:%.3f;--sh:%.3f;--drop:%d">\n%s\n</div>\n<!-- MOBILE end -->'
         % (PW, D, M, H, DROP, '\n'.join(pairs)))
page = open(SITE, encoding='utf-8').read()
if '<!-- MOBILE start' not in page:
    lab = '<div class="item"><span class="mono">Mobile + Desktop</span>'   # eyebrow, then the screens, then title and body (2026-09-29)
    page = page.replace(lab, lab + '\n<!-- MOBILE start -->\n<!-- MOBILE end -->\n')
page = re.sub(r'<!-- MOBILE start[\s\S]*?<!-- MOBILE end -->', lambda m: block, page)
open(SITE, 'w', encoding='utf-8').write(page)
print('pair %.1f wide: desktop %.1f x %.1f, phone %.1f x %.1f, dropped %d, overhang %.1f' % (PW, D, H, M, H, DROP, PW - D))
