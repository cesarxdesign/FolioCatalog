#!/usr/bin/env python3
# REMOVED from the page on request (2026-09-29): the "More than a home" strip is no longer shown. Do not rerun.
"""The five live-product phone screens from the Lite version's Impact strip (versions/penfold/2026-07-30),
in a row between the big App Store review and the other three, framed like the other strips on this page.

    python3 source/impact.py        rewrites the row between the IMPACT markers in site/index.html

The screens are taken as coded on the Lite page (each a self-scaling shadow root, 375 x 812); their
screens/assets/ files are inlined as data: URIs so nothing needs publishing beside the page.
"""
import base64, mimetypes, os, re
HERE = os.path.dirname(os.path.abspath(__file__))
SITE = os.path.join(HERE, '..', 'site', 'index.html')
LITE = os.path.abspath(os.path.join(HERE, '..', '..', '2026-07-30', 'site', 'penfold'))
WIDTH, GAP, N, FW, FH = 894, 16, 5, 375, 812          # 894: the section's body column; N: the Lite strip's screens
CUT = [0]                                              # the Lite strip's first screen (Final step) was cut on request, 2026-09-29

src = open(os.path.join(LITE, 'index.html'), encoding='utf-8').read().replace('>9:24<', '>8:24<')   # every mobile clock reads 8:24, as in CodeCatalog (2026-09-29)
start = src.index('<div class="rack five">')
screens = re.findall(r'<div class="scr ph">(<template shadowrootmode="open">[\s\S]*?</template>)</div>', src[start:])[:N]
assert len(screens) == N, len(screens)

cache = {}
def inline(m):
    path = m.group(1)
    if path not in cache:
        data = open(os.path.join(LITE, path), 'rb').read()
        mime = mimetypes.guess_type(path)[0] or ('image/svg+xml' if path.endswith('.svg') else 'application/octet-stream')
        cache[path] = 'data:%s;base64,%s' % (mime, base64.b64encode(data).decode())
    return cache[path]

# aesthetic edits on request, 2026-09-29: the dashboard (Lite screen 1) loses its right chevron and its bell moves to
# the right edge, where the chevron was; the activity screen (Lite screen 4) swaps its burger for that same bell
BELL_X = '319.046875px'                                # the chevron's slot, 16px in from the right edge
def sub(s, old, new):
    assert s.count(old) == 1, old
    return s.replace(old, new)
s1 = screens[1]
s1 = sub(s1, '<div class="chev"><div class="slot"><i><i><img src="screens/assets/ic-chevron-small.svg" alt=""></i></i></div></div>', '')
s1 = sub(s1, '.notif{position:absolute;left:279.046875px;', '.notif{position:absolute;left:%s;' % BELL_X)
s4 = screens[4]
s4 = sub(s4, '<div class="menu"><i><img src="screens/assets/ic-menu-dropdown.svg" alt=""></i></div>', '')
head, tail = s4.rsplit('</div></template>', 1)          # the bell goes last in the frame, over the header
s4 = head + '<div class="notif"><img src="screens/assets/ic-notification.svg" alt=""></div></div></template>' + tail
s4 = s4.replace('</style>', '.notif{position:absolute;left:%s;top:79px;width:40px;height:40px}</style>' % BELL_X, 1)
screens[1], screens[4] = s1, s4
for i in (2, 3):                                       # both Saving screens are titled Payment (on request, 2026-09-29)
    screens[i] = sub(screens[i], '<div class="title"><p>Saving</p></div>', '<div class="title"><p>Payment</p></div>')
    # the title box was sized to "Saving" (left 248, 95 wide, ends 32px from the right); anchor it right so the longer word grows leftward
    screens[i] = sub(screens[i], '.title{position:absolute;left:248px;top:21px;width:95px;', '.title{position:absolute;right:32px;top:21px;width:max-content;')
screens = [s for i, s in enumerate(screens) if i not in CUT]
n = len(screens)
tw = (WIDTH - GAP * (n - 1)) / n
h = round(FH * tw / FW)
tiles = []
for t in screens:
    t = re.sub(r'(screens/assets/[\w.-]+)', inline, t)
    tiles.append('<div class="stack"><div class="step" style="--fb:%d"><div class="win"><div class="lite">%s</div></div></div></div>' % (h, t))
# a Cable-style annotation: a ring on the dashboard's Paused button, its line to a caption in the left gutter
# (Cesar's own words; punctuation only may change, never the words)
ANN = dict(screen=0, box=(196, 194, 147, 40), pad=4,      # the Paused pill in the dashboard, in its 375-wide frame
           title='More than a home.',
           body='The main screen gave users access to all features and info in one single moment. Both buttons at the '
                'top showed you Fund and Payment, and tapping them triggered the respective flows. Same for the donut, '
                'the bottom trio, and notifications. No extra menus needed.')
k = tw / FW
x, y, w, hh = ANN['box']; p = ANN['pad']
l = ANN['screen'] * (tw + GAP) + (x - p) * k; top = (y - p) * k; rw = (w + 2 * p) * k; rh = (hh + 2 * p) * k
mid = 100 * (top + rh / 2) / h
ring = ('<div class="ring" style="left:%.3f%%;top:%.3f%%;width:%.3f%%;height:%.3f%%"></div>\n'
        '<div class="lead under" style="top:%.3f%%;width:%.3f%%"></div>' % (100 * l / WIDTH, 100 * top / h, 100 * rw / WIDTH, 100 * rh / h, mid, 100 * l / WIDTH))
cap = ('<div class="lead" style="top:%.3f%%;width:40px"></div><div class="dot" style="top:calc(%.3f%% - 3.5px)"></div>'
       '<figcaption class="cap" style="top:calc(%.3f%% - 14px)"><span class="ct">%s</span><span class="cb">%s</span></figcaption>'
       % (mid, mid, mid, ANN['title'], ANN['body']))
row = ('<!-- IMPACT start: built by source/impact.py from the Lite version\'s screens, do not edit by hand -->\n'
       '<figure class="ann"><div class="sw">\n'
       '<div class="flow impact" style="--n:%d;--tw:%.3f;--h:%d" role="group" aria-label="Penfold today: screens of the live app">\n' % (n, tw, h)
       + '\n'.join(tiles) + '\n</div>\n' + ring + '\n</div>\n' + cap + '\n</figure>\n<!-- IMPACT end -->')
page = open(SITE, encoding='utf-8').read()
if '<!-- IMPACT start' not in page:
    a = '<p class="txt closing">Growth finally caught up with the product, as the new strategy yielded 6x the signups.</p>\n'
    assert page.count(a) == 1   # under that line (moved from under the reviews, on request, 2026-09-29)
    page = page.replace(a, a + '<!-- IMPACT start -->\n<!-- IMPACT end -->\n')
page = re.sub(r'<!-- IMPACT start[\s\S]*?<!-- IMPACT end -->', lambda m: row, page)
open(SITE, 'w', encoding='utf-8').write(page)
print('%d screens, %.1fpx wide, %dpx tall, %d assets inlined' % (n, tw, h, len(cache)))
