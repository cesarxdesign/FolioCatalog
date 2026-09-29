#!/usr/bin/env python3
"""Iterate, iterate: the Combine iterations above the Combine item, over the chevron arrows that show the
progression, laid out as on the Figma folio's "12 iterate" section (CG-Folio-WIP 1:30377) and scaled to the column.

    python3 source/iterate.py       rewrites the block between the ITERATE markers in site/index.html

Screens are CodeCatalog's mobile master-combine-* screens (snippet.html), read from the master file (Penfold _new,
Section 2). The arrows are CodeCatalog/images/penfold/combine-iterations/arrows.svg, the Figma vector as exported,
placed by the geometry in that folder's README.
"""
import os, re
HERE = os.path.dirname(os.path.abspath(__file__))
SITE = os.path.join(HERE, '..', 'site', 'index.html')
CAT = os.path.abspath(os.path.join(HERE, *['..'] * 5, 'CodeCatalog'))
MOB = os.path.join(CAT, 'screens', 'penfold', 'mobile')
ARROWS = os.path.join(CAT, 'images', 'penfold', 'combine-iterations', 'arrows.svg')

SCREENS = [('master-combine-v10', '01 Pop up'), ('master-combine-v11', '02 Full view w/ nav'),
           ('master-combine-v12', '03 Baked in addresses'), ('master-combine-v20', '04 Add &lt;employer&gt;'),
           ('master-combine-v20-popup', '05 Help pop-up'), ('master-combine-success', '06 Success')]   # 05 and 06: captions of my own, the folio showed four
WIDTH, W, H = 820, 375, 812                   # 820: the Targeting list's width
# Figma geometry (Frame 87 = 1920 x 832; the screens' Frame 197 at 150,10, 1620 wide, screens 40 apart;
# arrows.svg at -95.299,-15.4287, 2001.95 x 863.429; 24px fades top and bottom)
FX, FY, FH, GAP = 150, 10, 832, 40
FW = len(SCREENS) * W + (len(SCREENS) - 1) * GAP          # the screens' span (1620 for the folio's four)
BAND = FW + 2 * FX                                          # the art band keeps the folio's 150 margins (1920 for four)
AX, AY, AW0, AH = -95.299, -15.4287, 2001.95, 863.429
PITCH = 511.661                                             # the four chevrons in arrows.svg sit 511.661 apart
N = 4
while AX + AW0 + (N - 4) * PITCH < BAND: N += 1            # more chevrons, same pitch, until the band is covered
AW = AW0 + (N - 4) * PITCH
k = WIDTH / FW

def load(sid):
    src = open(os.path.join(MOB, sid, 'snippet.html'), encoding='utf-8').read()
    inner = re.search(r'<template shadowrootmode="open">([\s\S]*)</template>', src).group(1)
    css = re.search(r'<style>([\s\S]*?)</style>', inner).group(1)
    return css, re.sub(r'<style>[\s\S]*?</style>', '', inner, count=1).strip()

src = open(ARROWS, encoding='utf-8').read()
d = re.search(r'<path d="([^"]+)"', src).group(1)       # the first chevron; the others are copies of it at PITCH
stops = re.search(r'<linearGradient id="paint0[^>]*>([\s\S]*?)</linearGradient>', src).group(1)
op = re.search(r'<g id="Vector" opacity="([\d.]+)"', src).group(1)
svg = ('<svg preserveAspectRatio="none" viewBox="0 0 %.3f %s" fill="none" xmlns="http://www.w3.org/2000/svg" aria-hidden="true">'
       '<defs><linearGradient id="itg" x1="%.3f" y1="431.714" x2="-11.034" y2="431.714" gradientUnits="userSpaceOnUse">%s</linearGradient></defs>'
       '<g opacity="%s">%s</g></svg>' % (AW, AH, AW + 1.68, stops, op,
       ''.join('<path transform="translate(%.3f 0)" d="%s" fill="url(#itg)"/>' % (i * PITCH, d) for i in range(N))))
tw, h = W * k, H * k
tiles = []
for sid, cap in SCREENS:
    css, body = load(sid)
    css = ":host{display:block;width:%dpx;height:%dpx;font-family:'Montserrat',-apple-system,sans-serif;color:#133253}\n%s" % (W, H, css)
    tiles.append('<figure class="it-step"><div class="step" style="--fw:%d;--fb:%d" data-screen="penfold/mobile/%s"><div class="win"><div class="pg">'
                 '<template shadowrootmode="open"><style>\n%s\n</style>\n%s\n</template></div></div></div><figcaption class="mono">%s</figcaption></figure>'
                 % (W, round(h), sid, css, body, cap))
block = ('<!-- ITERATE start: built by source/iterate.py from CodeCatalog screens and art, do not edit by hand -->\n'
         '<div class="iter" style="--tw:%.3f;--k:%.5f" role="group" aria-label="Four iterations of the Combine screen">\n'
         '<div class="it-arrows" style="left:%.3fpx;top:%.3fpx;width:%.3fpx;height:%.3fpx">'
         '<div style="position:absolute;left:%.3fpx;top:%.3fpx;width:%.3fpx;height:%.3fpx">%s</div></div>\n'
         '<div class="it-row" style="gap:%.3fpx">\n%s\n</div>\n</div>\n<!-- ITERATE end -->'
         % (tw, k, -FX * k, -FY * k, BAND * k, FH * k, AX * k, AY * k, AW * k, AH * k, svg, GAP * k, '\n'.join(tiles)))
page = open(SITE, encoding='utf-8').read()
if '<!-- ITERATE start' not in page:
    anchor = '<div class="item"><span class="mono">Combine</span>'
    assert page.count(anchor) == 1, 'anchor not found'
    page = page.replace(anchor, '<!-- ITERATE start -->\n<!-- ITERATE end -->\n' + anchor)
page = re.sub(r'<!-- ITERATE start[\s\S]*?<!-- ITERATE end -->', lambda m: block, page)
open(SITE, 'w', encoding='utf-8').write(page)
print('%d screens %.1f x %.1f, %.1fpx apart; %d chevrons, band %.1f x %.1f' % (len(SCREENS), tw, h, GAP * k, N, BAND * k, FH * k))
