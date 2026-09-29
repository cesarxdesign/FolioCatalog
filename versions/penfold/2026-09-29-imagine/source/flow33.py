#!/usr/bin/env python3
"""The first onboarding, as one strip of live screens that fits the column: one tile per screen.

Each tile is a CodeCatalog desktop screen (screens/penfold/desktop/<id>/screen.html) in its
longest, most complete state, shown whole: nothing is cropped or scrolled. The strip has five columns,
laid out by hand (see screens()). All columns are the height of the tallest one: a column's
spare height is shared between its frames, as room at the bottom of each.
Nothing is drawn on the frames: no dots, no counts. Which steps a screen covers and its module
colour are kept in its data-steps and data-module attributes. Nothing is clickable; each tile is one fixed state
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
ENDS = {'three-things': 2320, 'enter-email': 427, 'sign-up-upper': 1032, 'savings-path': 428,
        'savings-calculator': 2325, 'monthly-payment': 473, 'plan-selection': 3512, 'document-consent': 1174,
        'sign-up-form': 2200, 'standing-order': 1157, 'confirmation': 1017}
WIDTH = 894           # the text column the strip has to fit, px on the page
GAP = 16              # between columns
BELOW = 170           # least room under a screen's last element, in screen pixels; clears the dot
SHORTEST = 900        # no frame is shorter than this, in screen pixels: it still has to look like a screen
STACK_GAP = 12        # between two screens in one column, px on the page


def need(s):
    """A screen's height at the 1182 frame width: its content and the least room under it, and
    never less than the shortest frame allowed."""
    return max(SHORTEST, (ENDS[s.sid] + BELOW) * 1182 / s.width)


def measure(cols):
    """(width of a column on the page, height of the tallest column in screen pixels)"""
    n = len(cols)
    tw = (WIDTH - GAP * (n - 1)) / n
    extra = STACK_GAP * 1182 / tw                        # what one more screen in a column costs
    return tw, max(sum(need(x) for x in c) + extra * (len(c) - 1) for c in cols)


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
    def __init__(self, sid, note, steps, colour, width=1182):
        self.sid, self.note, self.steps, self.colour = sid, note, list(steps), colour
        self.width = width
        self.css, self.body = load(sid)

    def sub(self, old, new, count=1):
        assert self.body.count(old) == count, (self.sid, old, self.body.count(old))
        self.body = self.body.replace(old, new)
        return self

    def rsub(self, pattern, new, count=1):
        self.body, n = re.subn(pattern, new, self.body)
        assert n == count, (self.sid, pattern, n)
        return self


# One colour per module, to show which screens belong together. The names are the colours on the
# flow picture; the values are a set picked to tell apart at dot size on the light frames.
RED    = '#D6409F'    # pink:   3 things, savings path
AMBER  = '#F76B15'    # orange: sign-up with email
TEAL   = '#00A2C7'    # cyan:   savings calculator
YELLOW = '#46A758'    # green:  monthly payment, standing order, confirmation
PURPLE = '#8E4EC6'    # purple: plan selection
BLUE   = '#3E63DD'    # indigo: sign-up form, docs


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


def sign_up_upper():
    # Enter your email (step 07) is not shown as a screen of its own: its field sits here, before
    # the password. Same field and placeholder as the catalogue's enter-email screen.
    s = Screen('sign-up-upper', 'name, phone, email and password', [7, 8], AMBER)
    s.sub('<div class="row" style="margin-top:18px">\n      <label class="lab" for="f-pass">Password</label>',
          '<div class="row" style="margin-top:18px">\n      <label class="lab" for="f-email">Email</label>\n'
          '      <input class="f" id="f-email" type="email" style="width:377px" placeholder="you@somewhere.com">\n    </div>\n\n'
          '    <div class="row">\n      <label class="lab" for="f-pass">Password</label>')
    return s


def screens():
    """The columns of the strip, left to right, each top to bottom. Laid out by hand."""
    return [
        [three_things(), sign_up_upper()],
        [Screen('savings-path', 'know the amount, or get help', [9], RED), calculator()],
        [plans()],
        [Screen('sign-up-form', 'the whole form, filled', range(28, 32), BLUE),
         Screen('document-consent', 'first doc open', range(24, 28), BLUE)],   # four docs, one step each
        [Screen('monthly-payment', 'amount and day', [17, 18], YELLOW),
         Screen('standing-order', 'standing order details', [32], YELLOW),
         Screen('confirmation', 'done', [33], YELLOW)],
    ]


# Annotations on the grid, in the live Cable page's form: rings on screens, one line out to a caption
# in the left gutter. The line leaves from the first ringed screen, which has to touch the left edge.
ANNOTATIONS = [
    dict(rings=['sign-up-upper', 'sign-up-form'],
         title='Unoptimized.',
         body='The sequence was not ideal, breaking in and out of topic repeatedly. But to save engineering effort, '
              'I made the call to keep it as close to the source code as possible, minimizing chances a dependency '
              'would break or some data was needed before we actually captured it. A conscious tradeoff.'),   # Cesar's words
]


def boxes(cols, tw, height):
    """Where each frame lands in the strip, in page pixels: {screen: (left, top, width, height)}.
    Mirrors the CSS: a column's spare height is shared equally between its frames."""
    out = {}
    for i, c in enumerate(cols):
        base = [round(need(s) * tw / 1182) for s in c]
        spare = (height - sum(base) - STACK_GAP * (len(c) - 1)) / len(c)
        top = 0
        for s, b in zip(c, base):
            out[s.sid] = (i * (tw + GAP), top, tw, b + spare)
            top += b + spare + STACK_GAP
    return out


def annotations(cols, tw, height):
    """(rings and lines that sit inside the grid, captions and brackets that sit in the gutter)"""
    pos, inside, gutter = boxes(cols, tw, height), [], []
    for a in ANNOTATIONS:
        mids = []
        for sid in a['rings']:
            l, t, w, h = pos[sid]
            inside.append('<div class="ring" style="left:%.3f%%;top:%.3f%%;width:%.3f%%;height:%.3f%%"></div>'
                          % (100 * l / WIDTH, 100 * t / height, 100 * w / WIDTH, 100 * h / height))
            mids.append(100 * (t + h / 2) / height)
            if l > 0:       # not at the left edge: its line runs under the screens to the gutter
                inside.append('<div class="lead under" style="top:%.3f%%;width:%.3f%%"></div>' % (mids[-1], 100 * l / WIDTH))
        cap = '<span class="ct">%s</span><span class="cb">%s</span>' % (a['title'], a['body'])
        if len(mids) == 1:
            gutter.append('<div class="lead" style="top:%.3f%%;width:40px"></div><div class="dot" style="top:calc(%.3f%% - 3.5px)"></div>'
                          '<figcaption class="cap" style="top:calc(%.3f%% - 14px)">%s</figcaption>' % (mids[0], mids[0], mids[0], cap))
        else:               # a bracket from the highest line to the lowest, the caption at its middle
            gutter.append('<div class="bracket" style="top:%.3f%%;bottom:%.3f%%"><div class="dot"></div>'
                          '<figcaption class="cap">%s</figcaption></div>' % (min(mids), 100 - max(mids), cap))
    return '\n'.join(inside), '\n'.join(gutter)


def tile(s, tw):
    # the screens are fixed 2640 frames that clip; here the frame is the tile, so let them run
    css = (":host{display:block;width:%dpx;font-family:'Montserrat',-apple-system,sans-serif;color:#133253}\n" % s.width
           + s.css + '\n.page{overflow:visible}\n')
    return ('<div class="step" style="--fw:%d;--fb:%d" data-screen="penfold/desktop/%s" data-steps="%s" data-module="%s" data-state="%s">'
            '<div class="win"><div class="pg"><template shadowrootmode="open"><style>\n%s\n</style>\n%s\n</template></div>'
            '</div></div>'
            % (s.width, round(need(s) * tw / 1182), s.sid, ' '.join('%02d' % n for n in s.steps), s.colour, s.note, css, s.body))


def main():
    cols = screens()
    all_screens = [s for c in cols for s in c]
    steps = [n for s in all_screens for n in s.steps]
    assert sorted(steps) == list(range(1, 34)), steps
    tw, room = measure(cols)
    height = round(room * tw / 1182)
    rings, caps = annotations(cols, tw, height)
    row = ('<!-- FLOW33 start: built by source/flow33.py from CodeCatalog screens, do not edit by hand -->\n'
           '<figure class="ann"><div class="sw">\n'
           '<div class="flow" style="--n:%d;--tw:%.3f;--h:%d" role="group" aria-label="The first onboarding, screen by screen">\n' % (len(cols), tw, height)
           + '\n'.join('<div class="stack">\n' + '\n'.join(tile(s, tw) for s in c) + '\n</div>' for c in cols)
           + '\n</div>\n' + rings + '\n</div>\n' + caps + '\n</figure>\n<!-- FLOW33 end -->')
    page = open(SITE, encoding='utf-8').read()
    assert page.count('<!-- FLOW33 start') == 1, 'markers missing in site/index.html'
    page = re.sub(r'<!-- FLOW33 start[\s\S]*?<!-- FLOW33 end -->', lambda m: row, page)
    open(SITE, 'w', encoding='utf-8').write(page)
    print('%d screens in %d columns of %.1fpx, strip %dpx tall' % (len(all_screens), len(cols), tw, height))
    for c in cols: print('  ', ' + '.join('%s (%s)' % (x.sid, ' '.join('%02d' % n for n in x.steps)) for x in c))


if __name__ == '__main__':
    main()
