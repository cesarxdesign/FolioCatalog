#!/usr/bin/env python3
"""The 33-step first onboarding, as one straight row of live screens.

Each step is a CodeCatalog desktop screen (screens/penfold/desktop/<id>/screen.html) put into
the state the step shows: sections shown or hidden, values changed, the page scrolled. Nothing
is clickable; each tile is one fixed state in its own shadow root.

    python3 source/flow33.py        rewrites the row between the FLOW33 markers in site/index.html

Under each step, a bar in the colour of its square on the flow picture; the bar runs unbroken
across one square.

Order and states follow the flow picture (Portfolio/penfold-air/img/onboarding-mvp.webp),
left to right, top to bottom. Values that differ from the catalogue screen were read off that
picture. Three things are not in the catalogue and were drawn here from the picture: the
assumptions dialog (step 13), the accepted docs state (step 26) and the checks screen (step 31).
"""
import os, re, sys

HERE = os.path.dirname(os.path.abspath(__file__))
SITE = os.path.join(HERE, '..', 'site', 'index.html')
CAT = os.path.abspath(os.path.join(HERE, *['..'] * 5, 'CodeCatalog', 'screens', 'penfold', 'desktop'))

WIN_H = 1925          # how much of a 1182-wide frame the picture shows


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


class Step:
    def __init__(self, sid, note, y=0, css='', width=1182):
        self.sid, self.note, self.y, self.extra, self.width = sid, note, y, css, width
        self.css, self.body = load(sid)

    def sub(self, old, new, count=1):
        assert self.body.count(old) >= count, (self.sid, self.note, old)
        self.body = self.body.replace(old, new, count)
        return self

    def rsub(self, pattern, new, count=1):
        self.body, n = re.subn(pattern, new, self.body, count=count)
        assert n == count, (self.sid, self.note, pattern, n)
        return self


# ---------------------------------------------------------------- 3 things (steps 1-6)
def things(note, opened=None, **kw):
    s = Step('three-things', note, width=1231, **kw)
    if opened:
        s.sub('aria-expanded="false" aria-controls="b%d"' % opened, 'aria-expanded="true" aria-controls="b%d"' % opened)
        s.sub('id="b%d" hidden' % opened, 'id="b%d"' % opened)
    return s

def things_blank():
    s = things('nothing filled in', css='.acc,.body,.cta,.foot{display:none}')
    s.sub('<span class="box">34</span>', '<span class="box"></span>')
    s.sub('<span class="box wide">&pound;50,000</span>', '<span class="box wide"></span>')
    return s

def things_cash_100():
    s = things('2 open, paying in 100', 2)
    s.sub('<span class="val out">&pound;309</span>', '<span class="val out">&pound;100</span>')
    s.sub('<span class="val mid">&pound;77</span>', '<span class="val mid">&pound;25</span>')
    s.sub('<span class="val tot">&pound;386</span>', '<span class="val tot">&pound;125</span>')
    return s

def things_einstein_21():
    s = things('3 open, paying in at 21', 3)
    # 386 growing at 5% from 21 to 68, less the 386 paid in: 3,440. The bar and knob follow.
    s.sub('<div style="width:333px;background:var(--pink);border-radius:3px"></div>',
          '<div style="width:697px;background:var(--pink);border-radius:3px"></div>')
    s.sub('<span class="val" style="left:470px">&pound;1,643</span>', '<span class="val" style="left:834px">&pound;3,440</span>')
    s.sub('<div class="fill" style="width:81px"></div>', '<div class="fill" style="width:20px"></div>')
    s.sub('<div class="knob" style="left:208px">34</div>', '<div class="knob" style="left:120px">21</div>')
    return s


# ---------------------------------------------------------------- calculator (steps 10-17)
def calc(note, step, **kw):
    s = Step('savings-calculator', note, **kw)
    s.sub('<div class="page" data-step="1">', '<div class="page" data-step="%d">' % step)
    return s

def calc_val(s, vid, sid, text, pct):
    s.rsub(r'(<span class="val" id="%s">)[^<]*' % vid, r'\g<1>%s' % text)
    s.rsub(r'(id="%s"[^>]*style="--p:)[^"]*' % sid, r'\g<1>%s' % pct)

def calc_plan(s, pay, pct, share, monthly, pays, key, donut, have=None):
    calc_val(s, 'v-pay', 's-pay', pay, pct)
    s.sub('<b>31.5%</b>', '<b>%s</b>' % share)
    s.sub('&pound;1,049 per month', '%s per month' % monthly)
    for old, new in zip(('&pound;970', '&pound;1,012', '&pound;1,055'), pays):
        s.rsub(r'(<span class="p\d">)%s' % re.escape(old), r'\g<1>%s' % new)
    for old, new in zip(('&pound;5,500', '&pound;423,629', '&pound;105,907', '&pound;301,283'), key):
        s.sub('<b>%s</b><em>' % old, '<b>%s</b><em>' % new)
    s.extra += '.donut{background:conic-gradient(%s)}' % donut
    return s

def calc_step2():
    s = calc('what you need each month', 2)
    calc_val(s, 'v-need', 's-need', '&pound;2,792', '30.6%')
    return s

ASSUMPTIONS_CSS = '''
.dim{position:absolute;inset:0;background:rgba(0,0,0,.5)}
.dlg{position:absolute;left:216px;top:396px;width:743px;height:1114px;padding:68px 68px 0;background:#fff;border-radius:3px;color:var(--navy)}
.dlg h2{margin:0;font:700 24px/1 'Montserrat',sans-serif}
.dlg h3{margin:52px 0 0;font:700 20px/1 'Montserrat',sans-serif}
.dlg h2+h3{margin-top:50px}
.dlg p{margin:22px 0 0;font:400 17px/28px 'Montserrat',sans-serif;color:var(--slate)}
.dlg .ok{display:block;width:100%;height:60px;margin-top:34px;border:1px solid var(--line);border-radius:5px;background:#fff;
  color:var(--navy);font:400 14.2px 'Montserrat',sans-serif}
.dlg .x{position:absolute;right:22px;top:16px;font:400 20px/1 'Montserrat',sans-serif;color:#C8C8C8}
'''
ASSUMPTIONS = '''<div class="dim"></div>
<div class="dlg"><span class="x">&times;</span>
<h2>Widely used assumptions</h2>
<h3>General assumptions</h3>
<p>These calculations assume your money grows at 5% each year after deducting all fees, an inflation rate of 2.5% each year, and that you increase your payments each year by 2.5%. All numbers are shown in today&rsquo;s money, and your retirement income is based on 4% of your retirement pot including state pension at current levels.</p>
<h3>Today&rsquo;s money &#129300;</h3>
<p>To make things simple, all the numbers we show you are in &ldquo;today&rsquo;s money&rdquo;. This means they are based on what money is worth &amp; what things cost today.</p>
<p>So, when thinking about how much you might need to live when you retire, just think about how much bills, shopping, holidays, school fees, socialising, all cost today.</p>
<p>In real life, things get more expensive every year as you get older (by about 2-3% per year), but there&rsquo;s a simple trick. Each new year, increase your monthly payment by that same small amount and you&rsquo;ll stay on track. Don&rsquo;t worry though, we&rsquo;ll tell you exactly how much when the time comes.</p>
<p>The very best thing to do is every time you start earning more money add a bit of that extra into your pension payment. Again, we&rsquo;ll help you decide how much on your Penfold Anniversary!</p>
<button class="ok">OK, got it</button></div>
'''
def calc_assumptions():
    s = calc('the assumptions, opened', 1, css=ASSUMPTIONS_CSS)
    s.sub('<div class="col">', ASSUMPTIONS + '<div class="col" style="z-index:-1">')
    s.extra += '.page{isolation:isolate}.dim,.dlg{z-index:1}'
    return s

CALC_Y = 440   # the page scrolled until the second question sits at the top

def calc_480():
    s = calc('the plan, paying 480', 4, y=CALC_Y)
    return calc_plan(s, '&pound;480', '34.5%', '32%', '&pound;1,065',
                     ('&pound;480', '&pound;793', '&pound;1,106'),
                     ('&pound;0', '&pound;430,086', '&pound;107,521', '&pound;293,213'),
                     '#5686E3 0 51.77%,#142E4E 51.77% 64.71%,#EBC97E 64.71% 100%')

def calc_3000():
    s = calc('the plan, paying 3,000', 4, css='#v-pay{border:2px solid #B4C2E2;box-shadow:0 0 0 3px #9FB5E4;line-height:58px}')
    return calc_plan(s, '&pound;3,000', '100%', '32%', '&pound;1,065',
                     ('&pound;3,000', '&pound;1,965', '&pound;930'),
                     ('&pound;0', '&pound;408,428', '&pound;102,107', '&pound;320,285'),
                     '#5686E3 0 49.16%,#142E4E 49.16% 61.45%,#EBC97E 61.45% 100%')

def calc_970(note, **kw):
    s = calc(note, 4, **kw)
    calc_val(s, 'v-have', 's-have', '&pound;5,500', '2.75%')
    return s


# ---------------------------------------------------------------- monthly payment (18-19)
def monthly_zero():
    return Step('monthly-payment', 'nothing entered').sub('value="&pound;970"', 'value="&pound;0"')


# ---------------------------------------------------------------- plans (20-24)
PLAN_Y = 540     # scrolled until the three plan cards sit at the top
ACCEPT_Y = 1505  # scrolled until the risk scale sits at the top

def plan(note, state, **kw):
    s = Step('plan-selection', note, **kw)
    s.sub('<div class="page" data-state="plans">', '<div class="page" data-state="%s">' % state)
    if state != 'plans':
        s.sub('<button class="pick">Pick this plan</button>', '<button class="pick">Selected</button>')
    return s

def plan_risk_later():
    return plan('risk levels 3 to 5', 'risk', y=PLAN_Y, css='.levels{transform:translateX(-536px)}')

def plan_accept(note, ticked):
    css = '' if ticked else ('.ack i{border:1px solid #E8E8E8;border-radius:3px}.ack svg{display:none}'
                             '.accept .go{background:#D2D2D2;color:#EFEFEF}')
    s = plan(note, 'accept', y=ACCEPT_Y, css=css)
    s.sub('<article class="lvl" data-lvl="4">', '<article class="lvl chosen" data-lvl="4">')
    s.sub('<button class="choose" data-choose="4">Choose</button>', '<button class="choose" data-choose="4">Chosen</button>')
    return s


# ---------------------------------------------------------------- docs (25-26)
def docs_accepted():
    css = ('.doc h2{background:#6BC950;justify-content:space-between}.doc .body{display:none}'
           '.doc h2::after{content:"";width:26px;height:26px;border:2px solid #fff;border-radius:3px;'
           'background:url("data:image/svg+xml,%3Csvg xmlns=\'http://www.w3.org/2000/svg\' viewBox=\'0 0 24 24\'%3E%3Cpath d=\'M4 12.5 L9.5 18 L20 6.5\' fill=\'none\' stroke=\'%23fff\' stroke-width=\'3\' stroke-linecap=\'round\' stroke-linejoin=\'round\'/%3E%3C/svg%3E") center/18px no-repeat}'
           '.all{background:var(--pink);color:#fff}')
    return Step('document-consent', 'every doc accepted', css=css)


# ---------------------------------------------------------------- sign-up form (27-31)
SIGN_Y = 157

def sign(note, **kw):
    return Step('sign-up-form', note, **kw)

def sign_clear(s, ids):
    for i in ids:
        s.rsub(r'(id="%s"[^>]*?) value="[^"]*"' % i, r'\1 value=""')

def sign_untick(s, group):
    s.rsub(r'(<div class="opts %s"[^>]*>\s*<label><input type="checkbox") checked' % group, r'\1')

def sign_select(s, fid, text):
    s.rsub(r'(<select class="f" id="%s"[^>]*><option>)[^<]*' % fid, r'\g<1>%s' % text)

def sign_bank_empty(s):
    sign_clear(s, ['f-acct', 'f-sort'])
    s.sub('<label><input type="checkbox" checked><span>Business</span></label>', '<label><input type="checkbox"><span>Business</span></label>')
    s.rsub(r'<div class="cono">[\s\S]*?</div>', '')
    s.rsub(r'(<select class="f" style="width:207px[^>]*><option>)Self Employed', r'\1Please select')

def sign_address(s):
    s.sub('id="f-search" placeholder="Find your address"', 'id="f-search" placeholder="Find your address" value="Wandsworth Road, London, UK"')
    s.sub('<input class="f" id="f-a1" value="d">', '<input class="f auto" id="f-a1" value="2301, 155 Wandsworth Road">')

def sign_not_resident():
    s = sign('not yet answered, the form waits',
             css='.opts.yesno label:first-child span{color:var(--navy)}.opts.yesno~*{opacity:.3}')
    s.sub('<label><input type="checkbox" checked><span>Yes</span></label>\n      <label><input type="checkbox"><span>No</span></label>',
          '<label><input type="checkbox"><span>Yes</span></label>\n      <label><input type="checkbox" checked><span>No</span></label>')
    sign_clear(s, ['f-house', 'f-a1', 'f-town', 'f-county', 'f-post', 'f-ni'])
    s.body = s.body.replace('class="f auto"', 'class="f"')
    sign_untick(s, 'gender')
    sign_select(s, 'f-cob', 'Please select'); sign_select(s, 'f-cit', 'Please select')
    sign_bank_empty(s)
    return s

def sign_address_found():
    s = sign('the address, filled from the search')
    sign_address(s)
    s.sub('<input class="f auto" id="f-house"', '<input class="f auto focus" id="f-house"')
    sign_untick(s, 'gender')
    sign_select(s, 'f-cit', 'Please select')
    sign_clear(s, ['f-ni'])
    sign_bank_empty(s)
    return s

def sign_account_missing():
    s = sign('sent without an account number', y=SIGN_Y,
             css='.f.err{border:2px solid var(--pink)}.errmsg{margin:10px 0 0;font:400 16.8px/1 \'Montserrat\',sans-serif;color:var(--pink)}')
    sign_address(s)
    sign_select(s, 'f-cob', 'Portugal'); sign_select(s, 'f-cit', 'Portugal')
    sign_bank_empty(s)
    s.sub('<input class="f" id="f-acct"', '<input class="f err" id="f-acct"')
    s.sub('<p class="help" style="margin-top:10px">Make sure', '<p class="errmsg">Please enter an account number</p>\n    <p class="help" style="margin-top:10px">Make sure')
    return s

def sign_problem():
    s = sign('the account could not be made', y=SIGN_Y,
             css='.oops{margin:52px 0 0;height:50px;display:flex;align-items:center;padding:0 22px;border-radius:4px;'
                 'background:#D93A49;color:#fff;font:400 16.8px/1 \'Montserrat\',sans-serif}.oops+.q{margin-top:17px}')
    s.sub('<p class="q">', '<p class="oops">There was a problem creating your account</p>\n    <p class="q">')
    return s

def sign_checks():
    s = sign('identity checks running',
             css='.wait{margin:117px 0 0;display:flex;justify-content:center;gap:16px}'
                 '.wait i{width:14px;height:14px;border-radius:50%;background:var(--pink)}.wait i:first-child{opacity:.18;transform:scale(.6)}'
                 '.waitmsg{margin:50px 0 0;text-align:center;font:400 19.4px/1 \'Montserrat\',sans-serif;color:var(--navy)}')
    s.rsub(r'<div class="col">[\s\S]*</div>\s*</div>\s*$',
           '<div class="col">\n    <h1>Hold on while we run some<br>checks</h1>\n'
           '    <div class="wait"><i></i><i></i></div>\n    <p class="waitmsg">Verifying identity..</p>\n  </div>\n</div>')
    return s


# ---------------------------------------------------------------- the 33, in order
def steps():
    return [
        things_blank(),
        things('1 open', 1),
        things_cash_100(),
        things('2 open, paying in 309', 2),
        things('3 open, paying in at 34', 3),
        things_einstein_21(),
        Step('enter-email', 'email'),
        Step('sign-up-upper', 'name, phone and password'),
        Step('savings-path', 'know the amount, or get help'),
        calc('what you earn', 1),
        calc_step2(),
        calc('what you need saved, what you have', 3),
        calc_assumptions(),
        calc_480(),
        calc_3000(),
        calc_970('the plan, paying 970'),
        calc_970('the plan, ready to move on', y=CALC_Y, css='.plan button.go{outline:4px solid #A9AEB5;outline-offset:8px}'),
        Step('monthly-payment', 'the amount carried over'),
        monthly_zero(),
        plan('three plans', 'plans'),
        plan('risk levels 1 to 3', 'risk', y=PLAN_Y),
        plan_risk_later(),
        plan_accept('level 4 chosen, risks to accept', False),
        plan_accept('risks accepted', True),
        Step('document-consent', 'first doc open'),
        docs_accepted(),
        sign_not_resident(),
        sign_address_found(),
        sign_account_missing(),
        sign_problem(),
        sign_checks(),
        Step('standing-order', 'standing order details'),
        Step('confirmation', 'done'),
    ]


# The squares on the flow picture: the modules the flow was later split into, and their colours there.
GROUPS = [(6, '#CE372F'), (8, '#ECB73E'), (9, '#CE372F'), (17, '#72D4B7'), (19, '#F9FD56'),
          (24, '#A638D8'), (26, '#3D91F7'), (31, '#3D91F7'), (33, '#F9FD56')]   # (last step, colour)

def group(n):
    """(colour, whether the next step is in the same square)"""
    for last, colour in GROUPS:
        if n <= last:
            return colour, n < last

def tile(n, s):
    colour, run = group(n)
    css = (":host{display:block;width:%dpx;min-height:2640px;font-family:'Montserrat',-apple-system,sans-serif;color:#133253}\n" % s.width
           + s.css + '\n' + s.extra)
    return ('<li class="step%s" style="--fw:%d;--fy:%d;--gc:%s" data-screen="penfold/desktop/%s" data-state="%s">'
            '<div class="win"><div class="pg"><template shadowrootmode="open"><style>\n%s\n</style>\n%s\n</template></div></div>'
            '<i class="bar"></i><span class="mono">%02d</span></li>'
            % (' run' if run else '', s.width, s.y, colour, s.sid, s.note, css, s.body, n))


def main():
    all_steps = steps()
    assert len(all_steps) == 33
    row = ('<!-- FLOW33 start: built by source/flow33.py from CodeCatalog screens, do not edit by hand -->\n'
           '<ol class="flow" aria-label="The first onboarding, 33 steps in order">\n'
           + '\n'.join(tile(i + 1, s) for i, s in enumerate(all_steps))
           + '\n</ol>\n<!-- FLOW33 end -->')
    page = open(SITE, encoding='utf-8').read()
    assert page.count('<!-- FLOW33 start') == 1, 'markers missing in site/index.html'
    page = re.sub(r'<!-- FLOW33 start[\s\S]*?<!-- FLOW33 end -->', lambda m: row, page)
    open(SITE, 'w', encoding='utf-8').write(page)
    print('33 steps, %.0f KB in the row' % (len(row) / 1024))


if __name__ == '__main__':
    main()
