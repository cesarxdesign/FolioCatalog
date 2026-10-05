#!/usr/bin/env python3
"""Iterate, iterate: the Combine iterations inside the Combine item, between its label and its title, over the chevron arrows that show the
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

SCREENS = [('master-combine-v10', '01 Bare minimum.'), ('master-combine-v11', '02 Required provider&rsquo;s address'),
           ('master-combine-v12', '03 Removed provider&rsquo;s address'), ('master-combine-v20-popup', '04 More info pop-ups'),
           ('master-combine-v20', '05 Brought back Employer'), ('master-combine-success', '06 Added Combine another')]   # 04 and 05 swapped, all six captions Cesar's own (2026-09-29)   # 05 and 06: captions of my own, the folio showed four
WIDTH, W, H, PGAP = 894, 375, 812, 16          # 894: the main column (the h2's width), as the other strips; 16: their gap
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
# the middle four screens fill the column; the first and last overflow it, one each side (on request, 2026-09-29)
# the middle four fill the main column at the other strips' 16px gap, so they match the strip below in size
k = (WIDTH - 3 * PGAP) / (4 * W)
OUT = W * k + PGAP                                          # how far the row reaches past the column on each side

# Page-only edits on request (2026-09-29), not in CodeCatalog: the pop-up's Request button is shown disabled, like
# the next screen's Combine; both v2.0 screens get their fields filled in (the values the success screen shows)
# and an enabled, pink Combine button.
VALUES = ['McDonalds', 'Aviva', 'PFL2918811', '&pound;4,299']   # Employer, Pension provider, scheme number, amount

def fill(body):
    n = 0
    def one(m):
        nonlocal n
        v = VALUES[n]; n += 1
        return (m.group(1).replace('tf-box', 'tf-val') + m.group(2).replace('tx-l t-nsb16', 'tx-c t-nb16')
                + '<span class="trk">%s</span></p>' % v)
    body = re.sub(r'(<div class="abs tf-box"></div>\s*)(<p class="tx tx-l t-nsb16"[^>]*>)[^<]*</p>', one, body)
    assert n == 4, n
    return body

def edit(sid, css, body):
    if sid == 'master-combine-v10':
        css += '\n.save { background: #E7EBED; }\n'                      # disabled, as v1.1's Combine
    if sid in ('master-combine-v20', 'master-combine-v20-popup'):
        body = fill(body)
        body = re.sub(r'(<div class="abs btn btn-auto") (data-node-id="136:(?:5933|7089)")', r'\1 style="background:var(--pinkfold)" \2', body)
        assert 'style="background:var(--pinkfold)"' in body
    return css, body

def load(sid):
    src = open(os.path.join(MOB, sid, 'snippet.html'), encoding='utf-8').read().replace('backdrop-filter:blur(20.39px);', '')   # the iOS bar's blur pulls the page in at the frame edge: a dark smear on the dark page
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
# A stepper (on request, 2026-09-29): one phone, and beside it all six iterations (number, title, note) always
# showing; picking one switches the phone and highlights it. Titles are the captions; notes are Cesar's own words, punctuation only.
NOTES = [
    ('Bare minimum.', 'Existed from the start, and wasn&rsquo;t prioritized for months.'),
    ('Required provider&rsquo;s address.', 'Required provider&rsquo;s address, as it was a mandatory field for us, and up &rsquo;til then, because usage was low, we did it ourselves. Now we couldn&rsquo;t.'),
    ('Removed provider&rsquo;s address.', 'The address added friction that immediately showed on analytics, so we created an exhaustive list of providers and their addresses: two improvements at once, a dropdown to pick from, and no address to type.'),
    ('More info pop-ups.', 'Our first pop-up, easier to dismiss than before (full page + Back button).'),
    ('Brought back Employer.', 'Added back Employer (from 01), to allow users to &ldquo;name&rdquo; their pensions, as more of them combined multiple pots.'),
    ('Added Combine another.', 'Added &ldquo;Combine another&rdquo;, no longer requiring the user to start the process from scratch.'),
]
PW = 260                                                    # the phone's width on the page
pk = PW / W
phones, tabs, texts = [], [], []
for n, (sid, cap) in enumerate(SCREENS):
    css, body = edit(sid, *load(sid))
    css = ":host{display:block;width:%dpx;height:%dpx;font-family:'Montserrat',-apple-system,sans-serif;color:#133253}\n%s" % (W, H, css)
    on = n == 0
    phones.append('<div class="st-screen" id="st-s%d" role="tabpanel" data-screen="penfold/mobile/%s"%s><div class="win"><div class="pg" style="--fw:%d;--tw:%.3f">'
                  '<template shadowrootmode="open"><style>\n%s\n</style>\n%s\n</template></div></div></div>'
                  % (n, sid, '' if on else ' hidden', W, PW, css, body))
    title, note = NOTES[n]
    tabs.append('<button type="button" class="st-row" role="tab" aria-selected="%s" aria-controls="st-s%d"><span class="st-n">%02d</span>'
                '<span class="st-tx"><span class="st-t">%s</span><span class="st-b">%s</span></span></button>'
                % ('true' if on else 'false', n, n + 1, title, note))
block = ('<!-- ITERATE start: built by source/iterate.py from CodeCatalog screens, do not edit by hand -->\n'
         '<div class="iter st" style="--pw:%d;--ph:%d" role="group" aria-label="Six iterations of the Combine screen">\n'
         '<div class="st-phone">%s</div>\n<div class="st-list" role="tablist" aria-orientation="vertical" aria-label="Iteration">%s</div>\n</div>\n'
         '<script>(function(){var r=document.currentScript.previousElementSibling;var t=r.querySelectorAll(\'[role=tab]\'),s=r.querySelectorAll(\'.st-screen\');'
         'function go(i){t.forEach(function(b,j){b.setAttribute(\'aria-selected\',j===i);b.tabIndex=j===i?0:-1});s.forEach(function(e,j){e.hidden=j!==i})}'
        # hovering a step selects it, and the last one hovered stays selected; a click or tap still works (2026-09-30)
         't.forEach(function(b,i){b.addEventListener(\'mouseenter\',function(){go(i)});b.addEventListener(\'click\',function(){go(i)});b.addEventListener(\'keydown\',function(e){var d=e.key===\'ArrowDown\'?1:e.key===\'ArrowUp\'?-1:0;if(d){e.preventDefault();var n=(i+d+t.length)%%t.length;go(n);t[n].focus()}})});go(0)})();</script>\n'
         '<!-- ITERATE end -->' % (PW, round(H * pk), '\n'.join(phones), ''.join(tabs)))
page = open(SITE, encoding='utf-8').read()
if '<!-- ITERATE start' not in page:
    i = page.index('<h3>A new flagship.</h3>'); j = page.index('</p>', i) + 4   # eyebrow, title and body, then the screens (2026-09-30)
    page = page[:j] + '\n<!-- ITERATE start -->\n<!-- ITERATE end -->' + page[j:]
page = re.sub(r'<!-- ITERATE start[\s\S]*?<!-- ITERATE end -->', lambda m: block, page)
open(SITE, 'w', encoding='utf-8').write(page)
print('stepper: %d iterations, phone %d x %d' % (len(SCREENS), PW, round(H * pk)))
