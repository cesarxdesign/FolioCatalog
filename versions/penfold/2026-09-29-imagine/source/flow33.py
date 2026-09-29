#!/usr/bin/env python3
"""The first onboarding, as one straight row of live screens: one tile per screen.

Each tile is a CodeCatalog desktop screen (screens/penfold/desktop/<id>/screen.html) in its
longest, most complete state, shown whole: nothing is cropped or scrolled. Under it, a bar in
the colour of its square on the flow picture (the modules the flow was later split into) and
the numbers of the steps that screen covers. Nothing is clickable; each tile is one fixed state
in its own shadow root.

    python3 source/flow33.py        rewrites the row between the FLOW33 markers in site/index.html

Order and step counts follow the flow picture (Portfolio/penfold-air/img/onboarding-mvp.webp),
left to right, top to bottom. Two steps on the picture are left out by request: the assumptions
dialog and the "Hold on while we run some checks" screen.
"""
import os, re

HERE = os.path.dirname(os.path.abspath(__file__))
SITE = os.path.join(HERE, '..', 'site', 'index.html')
CAT = os.path.abspath(os.path.join(HERE, *['..'] * 5, 'CodeCatalog', 'screens', 'penfold', 'desktop'))

# Where each screen's content ends, in its own pixels, measured in Chrome (see NOTES.md).
ENDS = {'three-things': 2320, 'enter-email': 427, 'sign-up-upper': 936, 'savings-path': 428,
        'savings-calculator': 2325, 'monthly-payment': 473, 'plan-selection': 3512, 'document-consent': 1174,
        'sign-up-form': 2113, 'standing-order': 1157, 'confirmation': 1017}
BELOW = 96            # room left under a screen's last element, in screen pixels
FRAME = 326           # a frame's height on the page; taller only where the screen needs it


def load(sid):
    """(css, body) of a catalogue screen, made ready for a shadow root (as CodeCatalog's build does)."""
    src = open(os.path.join(CAT, sid, 'screen.html'), encoding='utf-8').read()
    css = "\n".join(m.group(1) for m in re.finditer(r'<style[^>]*>([\s\S]*?)</style>', src))
    body = re.search(r'<body[^>]*>([\s\S]*?)</body>', src).group(1)
    body = re.sub(r'<script[\s\S]*?</script>', '', body).strip()
    css = re.sub(r'(^|[}\n;])\s*html\s*,\s*body\s*\{[^}]*\}', r'\1', css)
    css = re.sub(r'(^|[}\n])\s*html\s*\{[^}]*\}', r'\1', css)
    css = re.sub(r'(^|[}\n])\s*body\s*\{', r'\1:host{', css)
    css = css.replace(':root{', ':host{')
    return css.strip(), body


class Screen:
    def __init__(self, sid, note, steps, colour, joins_next=False, width=1182):
        self.sid, self.note, self.steps, self.colour = sid, note, list(steps), colour
        self.joins_next, self.width = joins_next, width
        self.css, self.body = load(sid)

    def sub(self, old, new, count=1):
        assert self.body.count(old) == count, (self.sid, old, self.body.count(old))
        self.body = self.body.replace(old, new)
        return self

    def rsub(self, pattern, new, count=1):
        self.body, n = re.subn(pattern, new, self.body)
        assert n == count, (self.sid, pattern, n)
        return self


RED, AMBER, TEAL, YELLOW, PURPLE, BLUE = '#CE372F', '#ECB73E', '#72D4B7', '#F9FD56', '#A638D8', '#3D91F7'


def three_things():
    s = Screen('three-things', 'all three sections open', range(1, 7), RED, width=1231)
    s.sub('aria-expanded="false"', 'aria-expanded="true"', 3)
    s.rsub(r'(id="b[123]") hidden', r'\1', 3)
    return s

def calculator():
    s = Screen('savings-calculator', 'the whole plan', range(10, 17), TEAL)
    s.sub('<div class="page" data-step="1">', '<div class="page" data-step="4">')
    s.rsub(r'(<span class="val" id="v-have">)[^<]*', r'\g<1>&pound;5,500')
    s.rsub(r'(id="s-have"[^>]*style="--p:)[^"]*', r'\g<1>2.75%')
    return s

def plans():
    s = Screen('plan-selection', 'plan, risk level and risks accepted', range(19, 24), PURPLE)
    s.sub('<div class="page" data-state="plans">', '<div class="page" data-state="accept">')
    s.sub('<button class="pick">Pick this plan</button>', '<button class="pick">Selected</button>')
    s.sub('<article class="lvl" data-lvl="4">', '<article class="lvl chosen" data-lvl="4">')
    s.sub('<button class="choose" data-choose="4">Choose</button>', '<button class="choose" data-choose="4">Chosen</button>')
    return s


def screens():
    return [
        three_things(),
        Screen('enter-email', 'email', [7], AMBER, joins_next=True),
        Screen('sign-up-upper', 'name, phone and password', [8], AMBER),
        Screen('savings-path', 'know the amount, or get help', [9], RED),
        calculator(),
        Screen('monthly-payment', 'amount and day', [17, 18], YELLOW),
        plans(),
        Screen('document-consent', 'first doc open', range(24, 28), BLUE),   # four docs, one step each
        Screen('sign-up-form', 'the whole form, filled', range(28, 32), BLUE),
        Screen('standing-order', 'standing order details', [32], YELLOW, joins_next=True),
        Screen('confirmation', 'done', [33], YELLOW),
    ]


def tile(s):
    frame_h = max(FRAME, round((ENDS[s.sid] + BELOW) * 200 / s.width))
    # the screens are fixed 2640 frames that clip; here the frame is the tile, so let them run
    css = (":host{display:block;width:%dpx;font-family:'Montserrat',-apple-system,sans-serif;color:#133253}\n" % s.width
           + s.css + '\n.page{overflow:visible}\n')
    return ('<li class="step%s" style="--fw:%d;--fh:%d;--gc:%s" data-screen="penfold/desktop/%s" data-state="%s">'
            '<div class="win"><div class="pg"><template shadowrootmode="open"><style>\n%s\n</style>\n%s\n</template></div></div>'
            '<i class="bar"></i><span class="mono">%s</span></li>'
            % (' run' if s.joins_next else '', s.width, frame_h, s.colour, s.sid, s.note, css, s.body,
               ' '.join('%02d' % n for n in s.steps)))


def main():
    all_screens = screens()
    steps = [n for s in all_screens for n in s.steps]
    assert steps == list(range(1, 34)), steps
    row = ('<!-- FLOW33 start: built by source/flow33.py from CodeCatalog screens, do not edit by hand -->\n'
           '<ol class="flow" aria-label="The first onboarding, screen by screen">\n'
           + '\n'.join(tile(s) for s in all_screens) + '\n</ol>\n<!-- FLOW33 end -->')
    page = open(SITE, encoding='utf-8').read()
    assert page.count('<!-- FLOW33 start') == 1, 'markers missing in site/index.html'
    page = re.sub(r'<!-- FLOW33 start[\s\S]*?<!-- FLOW33 end -->', lambda m: row, page)
    open(SITE, 'w', encoding='utf-8').write(page)
    print('%d screens, %d steps, %.0f KB in the row' % (len(all_screens), len(steps), len(row) / 1024))


if __name__ == '__main__':
    main()
