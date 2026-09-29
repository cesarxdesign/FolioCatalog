#!/usr/bin/env python3
"""The four nominate-a-beneficiary screens, in a row under the "But what if I die?" title.

    python3 source/nobeni.py        rewrites the row between the NOBENI markers in site/index.html

Each is the live CodeCatalog mobile screen (screens/penfold/mobile/nominate-beneficiary-*/snippet.html),
375 x 812, scaled to a quarter of the text column. Nothing is clickable.
"""
import os, re
HERE = os.path.dirname(os.path.abspath(__file__))
SITE = os.path.join(HERE, '..', 'site', 'index.html')
CAT = os.path.abspath(os.path.join(HERE, *['..'] * 5, 'CodeCatalog', 'screens', 'penfold', 'mobile'))
SCREENS = ['nominate-beneficiary-form', 'nominate-beneficiary-popup', 'nominate-beneficiary-filled', 'nominate-beneficiary-done']
WIDTH, GAP, W, H = 894, 16, 375, 812

def load(sid):
    src = open(os.path.join(CAT, sid, 'snippet.html'), encoding='utf-8').read()
    inner = re.search(r'<template shadowrootmode="open">([\s\S]*)</template>', src).group(1)
    css = re.search(r'<style>([\s\S]*?)</style>', inner).group(1)
    body = re.sub(r'<style>[\s\S]*?</style>', '', inner, count=1).strip()
    return css, body

tw = (WIDTH - GAP * (len(SCREENS) - 1)) / len(SCREENS)
h = round(H * tw / W)
tiles = []
for sid in SCREENS:
    css, body = load(sid)
    css = ":host{display:block;width:%dpx;height:%dpx;font-family:'Montserrat',-apple-system,sans-serif;color:#133253}\n" % (W, H) + css
    tiles.append('<div class="stack"><div class="step" style="--fw:%d;--fb:%d" data-screen="penfold/mobile/%s"><div class="win"><div class="pg">'
                 '<template shadowrootmode="open"><style>\n%s\n</style>\n%s\n</template></div></div></div></div>' % (W, h, sid, css, body))
row = ('<!-- NOBENI start: built by source/nobeni.py from CodeCatalog screens, do not edit by hand -->\n'
       '<div class="flow nobeni" style="--n:%d;--tw:%.3f;--h:%d" role="group" aria-label="Nominating a beneficiary, screen by screen">\n' % (len(SCREENS), tw, h)
       + '\n'.join(tiles) + '\n</div>\n<!-- NOBENI end -->')
page = open(SITE, encoding='utf-8').read()
assert page.count('<!-- NOBENI start') == 1, 'markers missing in site/index.html'
page = re.sub(r'<!-- NOBENI start[\s\S]*?<!-- NOBENI end -->', lambda m: row, page)
open(SITE, 'w', encoding='utf-8').write(page)
print('%d screens, %.1fpx wide, %dpx tall' % (len(SCREENS), tw, h))
