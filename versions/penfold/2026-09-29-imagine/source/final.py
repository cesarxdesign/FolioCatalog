#!/usr/bin/env python3
"""The final onboarding, mobile, as one strip of live screens under "Growth finally caught up" (was above "Now we were fast!", then above that line; 2026-09-29), in the same style
as the modular strip (source/modular.py): screens in order, stacked where they fit, all columns one height,
no numbered dots.
One column per screen, every screen cropped to a regular phone screen (375 x 812), on request 2026-09-29.

    python3 source/final.py         rewrites the strip between the FINAL markers in site/index.html

Screens are CodeCatalog's mobile login and final-* screens (snippet.html), each cropped to its first 812px.
"""
import itertools, os, re, importlib.util
HERE = os.path.dirname(os.path.abspath(__file__))
spec = importlib.util.spec_from_file_location('flow33', os.path.join(HERE, 'flow33.py'))
f = importlib.util.module_from_spec(spec); spec.loader.exec_module(f)
SITE = os.path.join(HERE, '..', 'site', 'index.html')
MOB = os.path.abspath(os.path.join(HERE, *['..'] * 5, 'CodeCatalog', 'screens', 'penfold', 'mobile'))

# (screen, frame height, the screen's own background at its foot, filling any room below it)
# login first; fund, details, payment and continue were cut on request (2026-09-29)
ORDER = [('login', 812, '#F4F4F4'), ('final-start', 812, '#F4F4F4'),
         ('final-finish', 812, '#F4F4F4'), ('final-dashboard', 812, '#F6F6F6')]
WIDTH, GAP, STACK_GAP, W, CROP = 894, 16, 12, 375, 812   # 894: the section's body column; 812: a regular phone screen
COLUMNS = len(ORDER)                                        # one screen per column

def load(sid):
    src = open(os.path.join(MOB, sid, 'snippet.html'), encoding='utf-8').read().replace('backdrop-filter:blur(20.39px);', '')   # the iOS bar's blur pulls the page in at the frame edge: a dark smear on the dark page
    inner = re.search(r'<template shadowrootmode="open">([\s\S]*)</template>', src).group(1)
    css = re.search(r'<style>([\s\S]*?)</style>', inner).group(1)
    return css, re.sub(r'<style>[\s\S]*?</style>', '', inner, count=1).strip()

def tile(sid, frame_h, bg, tw, n, last):
    css, body = load(sid)
    frame_h = min(frame_h, CROP)
    css = ":host{display:block;width:%dpx;height:%dpx;font-family:'Montserrat',-apple-system,sans-serif;color:#133253}\n%s" % (W, frame_h, css)
    # no numbered dots (cut on request, 2026-09-29)
    return ('<div class="step" style="--fw:%d;--fb:%d;--wb:%s" data-screen="penfold/mobile/%s">'
            '<div class="win"><div class="pg"><template shadowrootmode="open"><style>\n%s\n</style>\n%s\n</template></div>'
            '</div></div>' % (W, round(frame_h * tw / W), bg, sid, css, body))

def main():
    # of every split of the sequence into COLUMNS columns, the one with the shortest tallest column wins
    tw = (WIDTH - GAP * (COLUMNS - 1)) / COLUMNS
    best = None
    for cuts in itertools.combinations(range(1, len(ORDER)), COLUMNS - 1):
        e = (0,) + cuts + (len(ORDER),)
        c = [ORDER[a:b] for a, b in zip(e, e[1:])]
        fill = [sum(min(h, CROP) for _, h, _ in x) * tw / W + STACK_GAP * (len(x) - 1) for x in c]
        score = (max(fill), sum(v * v for v in fill))
        if best is None or score < best[0]: best = (score, c)
    cols, height = best[1], round(best[0][0])
    seq = [s for s, _, _ in ORDER]
    row = ('<!-- FINAL start: built by source/final.py from CodeCatalog screens, do not edit by hand -->\n'
           '<div class="flow final" style="--n:%d;--tw:%.3f;--h:%d" role="group" aria-label="The final onboarding, screen by screen">\n' % (len(cols), tw, height)
           + '\n'.join('<div class="stack">\n' + '\n'.join(tile(s, h, bg, tw, seq.index(s) + 1, s == seq[-1]) for s, h, bg in c) + '\n</div>' for c in cols)
           + '\n</div>\n<!-- FINAL end -->')
    page = open(SITE, encoding='utf-8').read()
    if '<!-- FINAL start' not in page:
        m = re.search(r'<p class="txt[^"]*">Growth finally caught up[^<]*</p>', page)   # under the closing line (2026-09-29)
        page = page[:m.end()] + '\n<!-- FINAL start -->\n<!-- FINAL end -->' + page[m.end():]
    page = re.sub(r'<!-- FINAL start[\s\S]*?<!-- FINAL end -->', lambda m: row, page)
    open(SITE, 'w', encoding='utf-8').write(page)
    print('%d screens in %d columns of %.1fpx, tallest column %dpx' % (len(ORDER), len(cols), tw, height))
    for c in cols: print('  ', ' + '.join(x for x, _, _ in c))

if __name__ == '__main__':
    main()
