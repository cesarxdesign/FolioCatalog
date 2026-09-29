#!/usr/bin/env python3
"""The modular onboarding, desktop, as one strip of live screens, in the same style as the first
onboarding's strip in Shipping (source/flow33.py), but with three columns: screens in order, stacked where
they fit, all columns one height. A numbered dot on each frame and a tick on the last.

    python3 source/modular.py       rewrites the strip between the MODULAR markers in site/index.html

Screens are CodeCatalog's desktop modular-* screens, each shown whole at its own Figma frame height.
"""
import itertools, os, re, importlib.util
HERE = os.path.dirname(os.path.abspath(__file__))
spec = importlib.util.spec_from_file_location('flow33', os.path.join(HERE, 'flow33.py'))
f = importlib.util.module_from_spec(spec); spec.loader.exec_module(f)
SITE = os.path.join(HERE, '..', 'site', 'index.html')

# flow order: set up the plan, then the account, then pay, then done
# the welcome screen and the dashboard were cut from the strip on request (2026-09-29)
# (screen, height shown, the screen's own background at its foot). A frame taller than its screen
# is filled below with that colour, so the screen has no visible bottom edge. Payment is shown to
# 1637: below that its Figma frame is a stray 38px band of #FBFBFB left under the pasted pictures.
ORDER = [('modular-calculator', 1249, '#FBFBFB'), ('modular-fund', 1373, '#FBFBFB'), ('modular-details', 2478, '#FBFBFB'),
         ('modular-payment', 1637, '#F6F6F6'), ('modular-confirmation', 812, '#F6F6F6')]   # the dashboard was cut too
COLUMNS, WIDTH, GAP, STACK_GAP, W = 3, 820, 16, 12, 1200   # 820: it sits inside the Modular and Mobile list, which is 820 wide

def tile(sid, frame_h, bg, tw, n, last):
    css, body = f.load(sid)
    css = (":host{display:block;width:%dpx;font-family:'Montserrat',-apple-system,sans-serif;color:#133253}\n" % W
           + css + '\n.page{height:%dpx;overflow:hidden}\n' % frame_h)
    mark = f.CHECK if last else str(n)
    return ('<div class="step" style="--fw:%d;--fb:%d;--wb:%s" data-screen="penfold/desktop/%s">'
            '<div class="win"><div class="pg"><template shadowrootmode="open"><style>\n%s\n</style>\n%s\n</template></div>'
            '<b class="num" aria-label="Page %d">%s</b></div></div>' % (W, round(frame_h * tw / W), bg, sid, css, body, n, mark))

# a Cable-style annotation, as "Optimized for launch." on the Shipping strip: a ring on a screen, its line under
# the screens to a caption in the left gutter. Cesar's own draft, tightened on request (2026-09-29).
ANN = dict(ring='modular-details',
           title='Optimized for users.',
           body='Clean, with room to breathe, the revised onboarding had half the screens, and the information '
                'followed a logical flow. We\'d first help you figure out how much to save, then how to invest it, '
                'and only ask for personal information once you\'d committed. It spared you the infuriating '
                'experience of filling in every detail, only to discover the product doesn\'t fit your needs.')

def annotation(cols, tw, height):
    i = next(n for n, c in enumerate(cols) if any(s == ANN['ring'] for s, _, _ in c))
    assert len(cols[i]) == 1, 'the ringed screen must have its column to itself'
    l = i * (tw + GAP)
    ring = ('<div class="ring" style="left:%.3f%%;top:0;width:%.3f%%;height:100%%"></div>\n'
            '<div class="lead under" style="top:50%%;width:%.3f%%"></div>' % (100 * l / WIDTH, 100 * tw / WIDTH, 100 * l / WIDTH))
    cap = ('<div class="lead" style="top:50%%;width:40px"></div><div class="dot" style="top:calc(50%% - 3.5px)"></div>'
           '<figcaption class="cap" style="top:calc(50%% - 14px)"><span class="ct">%s</span><span class="cb">%s</span></figcaption>'
           % (ANN['title'], ANN['body']))
    return ring, cap

def main():
    # COLUMNS columns, screens in order, stacked where they fit; all columns one height, a column's
    # spare height shared out as room at the bottom of its frames. Of every split of the sequence, the one with the shortest tallest column wins.
    tw = (WIDTH - GAP * (COLUMNS - 1)) / COLUMNS
    best = None
    for cuts in itertools.combinations(range(1, len(ORDER)), COLUMNS - 1):
        e = (0,) + cuts + (len(ORDER),)
        c = [ORDER[a:b] for a, b in zip(e, e[1:])]
        fill = [sum(h for _, h, _ in x) * tw / W + STACK_GAP * (len(x) - 1) for x in c]
        score = (max(fill), sum(v * v for v in fill))
        if best is None or score < best[0]: best = (score, c)
    cols, height = best[1], round(best[0][0])
    seq = [s for s, _, _ in ORDER]
    ring, cap = annotation(cols, tw, height)
    row = ('<!-- MODULAR start: built by source/modular.py from CodeCatalog screens, do not edit by hand -->\n'
           '<figure class="ann"><div class="sw">\n'
           '<div class="flow" style="--n:%d;--tw:%.3f;--h:%d" role="group" aria-label="The modular onboarding, screen by screen">\n' % (len(cols), tw, height)
           + '\n'.join('<div class="stack">\n' + '\n'.join(tile(s, h, bg, tw, seq.index(s) + 1, s == seq[-1]) for s, h, bg in c) + '\n</div>' for c in cols)
           + '\n</div>\n' + ring + '\n</div>\n' + cap + '\n</figure>\n<!-- MODULAR end -->')
    page = open(SITE, encoding='utf-8').read()
    assert page.count('<!-- MODULAR start') == 1, 'markers missing'
    page = re.sub(r'<!-- MODULAR start[\s\S]*?<!-- MODULAR end -->', lambda m: row, page)
    open(SITE, 'w', encoding='utf-8').write(page)
    print('%d screens in %d columns of %.1fpx, tallest column %dpx' % (len(ORDER), len(cols), tw, height))
    for c in cols: print('  ', ' + '.join(x for x, _, _ in c))

if __name__ == '__main__':
    main()
