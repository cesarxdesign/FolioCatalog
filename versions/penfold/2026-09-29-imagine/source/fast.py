#!/usr/bin/env python3
"""The modular onboarding on mobile, as one row of live screens under "Now we were fast!": one screen per
column, each cropped to a regular phone screen (375 x 812), framed like the other strips; no numbered dots.

    python3 source/fast.py          rewrites the row between the FAST markers in site/index.html

Screens are CodeCatalog's mobile modular-* screens (snippet.html).
"""
import os, re
HERE = os.path.dirname(os.path.abspath(__file__))
SITE = os.path.join(HERE, '..', 'site', 'index.html')
MOB = os.path.abspath(os.path.join(HERE, *['..'] * 5, 'CodeCatalog', 'screens', 'penfold', 'mobile'))

SCREENS = ['modular-sign-up', 'modular-welcome', 'modular-fund', 'modular-welcome-75', 'modular-dashboard']
WIDTH, GAP, W, H = 894, 16, 375, 812                 # 894: the section's body column; 812: a regular phone screen
# the crop cuts into the next panel down; paint that sliver like the screen above it (on request, 2026-09-29)
COVER = {'modular-fund': (782, '#F6F6F6')}          # screen: (y where the white Risk acceptance panel starts, colour above)

def load(sid):
    src = open(os.path.join(MOB, sid, 'snippet.html'), encoding='utf-8').read()
    inner = re.search(r'<template shadowrootmode="open">([\s\S]*)</template>', src).group(1)
    css = re.search(r'<style>([\s\S]*?)</style>', inner).group(1)
    return css, re.sub(r'<style>[\s\S]*?</style>', '', inner, count=1).strip()

tw = (WIDTH - GAP * (len(SCREENS) - 1)) / len(SCREENS)
h = round(H * tw / W)
tiles = []
for sid in SCREENS:
    css, body = load(sid)
    if sid in COVER:
        y, col = COVER[sid]
        body += '<div style="position:absolute;left:0;top:%dpx;width:%dpx;height:%dpx;background:%s;z-index:99"></div>' % (y, W, H - y, col)
    css = ":host{display:block;width:%dpx;height:%dpx;font-family:'Montserrat',-apple-system,sans-serif;color:#133253}\n%s" % (W, H, css)
    tiles.append('<div class="stack"><div class="step" style="--fw:%d;--fb:%d" data-screen="penfold/mobile/%s"><div class="win"><div class="pg">'
                 '<template shadowrootmode="open"><style>\n%s\n</style>\n%s\n</template></div></div></div></div>' % (W, h, sid, css, body))
# a Cable-style annotation on the fund screen: ring on the frame, its line under the screens to a caption in the
# left gutter. Cesar's own draft, reviewed on request (2026-09-29)
ANN = dict(ring='modular-fund', title='The final piece of the puzzle.',
           body='Our little tracking exercise almost didn\'t work: money paid in immediately couldn\'t be received '
                'until all the IDs were corrected. But the investment fund took a few days to accept its first sum, so '
                'it acted as an unofficial escrow of sorts, covering every edge case.')
l = SCREENS.index(ANN['ring']) * (tw + GAP)
# the caption sits with its foot on the strip's foot (on request, 2026-09-29), so its line comes off the title
# wherever that lands: drawn by the title itself (.cap.low), running under the screens to the ring
ring = '<div class="ring" style="left:%.3f%%;top:0;width:%.3f%%;height:100%%"></div>' % (100 * l / WIDTH, 100 * tw / WIDTH)
cap = ('<figcaption class="cap low"><span class="ct" style="--reach:%.3fpx">%s</span><span class="cb">%s</span></figcaption>'
       % (l, ANN['title'], ANN['body']))
row = ('<!-- FAST start: built by source/fast.py from CodeCatalog screens, do not edit by hand -->\n'
       '<figure class="ann"><div class="sw">\n'
       '<div class="flow fast" style="--n:%d;--tw:%.3f;--h:%d" role="group" aria-label="The modular onboarding on mobile, screen by screen">\n' % (len(SCREENS), tw, h)
       + '\n'.join(tiles) + '\n</div>\n' + ring + '\n</div>\n' + cap + '\n</figure>\n<!-- FAST end -->')
page = open(SITE, encoding='utf-8').read()
if '<!-- FAST start' not in page:
    anchor = '<p class="txt closing">Now we were fast!</p>'           # under that line (moved, 2026-09-29)
    assert page.count(anchor) == 1, 'anchor line not found'
    page = page.replace(anchor, anchor + '\n<!-- FAST start -->\n<!-- FAST end -->')
page = re.sub(r'<!-- FAST start[\s\S]*?<!-- FAST end -->', lambda m: row, page)
open(SITE, 'w', encoding='utf-8').write(page)
print('%d screens, %.1fpx wide, %dpx tall' % (len(SCREENS), tw, h))
