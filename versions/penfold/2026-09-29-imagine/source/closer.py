#!/usr/bin/env python3
"""Above the reviews and their divider (moved on request, 2026-09-29 and 30): the Figma grid of twelve live app screens (__Folio-study, node 92:18503), six across and two
down. All six columns fit the main column. One gap throughout, as the other strips (on request, 2026-09-29).

    python3 source/closer.py        rewrites the grid between the CLOSER markers in site/index.html

Screens are CodeCatalog's mobile screens in its "closer" flow, in the grid's reading order.
"""
import os, re
HERE = os.path.dirname(os.path.abspath(__file__))
SITE = os.path.join(HERE, '..', 'site', 'index.html')
MOB = os.path.abspath(os.path.join(HERE, *['..'] * 5, 'CodeCatalog', 'screens', 'penfold', 'mobile'))

SCREENS = ['closer-sign-up', 'closer-welcome', 'closer-dashboard', 'closer-dashboard-paused', 'closer-pause', 'master-combine-success',
           'closer-transactions', 'growth', 'closer-payment', 'closer-beneficiary', 'nominate-beneficiary-popup', 'closer-estimate']
# second row: first and last swapped from the Figma order (on request, 2026-09-29)
COLS, INNER, WIDTH, GAP, W, H = 6, 6, 894, 16, 375, 812    # all six fit the main (body) column (on request, 2026-09-29)

def load(sid):
    src = open(os.path.join(MOB, sid, 'snippet.html'), encoding='utf-8').read().replace('backdrop-filter:blur(20.39px);', '')   # the iOS bar's blur pulls the page in at the frame edge: a dark smear on the dark page
    inner = re.search(r'<template shadowrootmode="open">([\s\S]*)</template>', src).group(1)
    css = re.search(r'<style>([\s\S]*?)</style>', inner).group(1)
    return css, re.sub(r'<style>[\s\S]*?</style>', '', inner, count=1).strip()

tw = (WIDTH - GAP * (INNER - 1)) / INNER
out = (COLS - INNER) // 2 * (tw + GAP)                # how far the grid reaches past the column on each side
h = round(H * tw / W)
tiles = []
for sid in SCREENS:
    css, body = load(sid)
    css = ":host{display:block;width:%dpx;height:%dpx;font-family:'Montserrat',-apple-system,sans-serif;color:#133253}\n%s" % (W, H, css)
    tiles.append('<div class="stack"><div class="step" style="--fw:%d;--fb:%d" data-screen="penfold/mobile/%s"><div class="win"><div class="pg">'
                 '<template shadowrootmode="open"><style>\n%s\n</style>\n%s\n</template></div></div></div></div>' % (W, h, sid, css, body))
grid = ('<!-- CLOSER start: built by source/closer.py from CodeCatalog screens, do not edit by hand -->\n'
        '<div class="flow wall" style="--n:%d;--tw:%.3f;--h:%d;--gap:%d;--out:%.3f" role="group" aria-label="Penfold, twelve screens of the app">\n'
        % (COLS, tw, h, GAP, out) + '\n'.join(tiles) + '\n</div>\n<!-- CLOSER end -->')
page = open(SITE, encoding='utf-8').read()
if '<!-- CLOSER start' not in page:
    a = '<div class="voices">'   # above the reviews and their divider (2026-09-30)
    page = page.replace(a, '<!-- CLOSER start -->\n<!-- CLOSER end -->\n' + a)
page = re.sub(r'<!-- CLOSER start[\s\S]*?<!-- CLOSER end -->', lambda m: grid, page)
open(SITE, 'w', encoding='utf-8').write(page)
print('%d screens, %d across, %.1fpx wide, %dpx tall, gap %d, %.1fpx past the column each side' % (len(SCREENS), COLS, tw, h, GAP, out))
