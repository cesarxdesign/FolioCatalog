#!/usr/bin/env python3
"""The website, under "A new target." in December: one composition laid out as the Figma frame Penfold _new
155:37933 (3217 x 2220; inside its 80px margins, 3057 wide) scaled to the 894 body column: the hero
(1600 x 920), a minimap of the whole page (144 x 920) with a red square on the Combine section, and a callout
of that section (1104 x 637, on the row's foot). It shows the redesign; a "Previously" button at its top right
shows the earlier site while hovered (or focused, or tapped): the red square travels to the old Combine
section while hero, minimap and callout dissolve into the old ones (on request, 2026-09-30).

    python3 source/website.py       rewrites the composition between the WEBSITE markers in site/index.html

Images in site/img/websites/, rendered from CodeCatalog's website-home (the redesign, "bot") and
website-home-simplest (the earlier site, "top") screens at 2x their size here.
"""
import os, re
HERE = os.path.dirname(os.path.abspath(__file__))
SITE = os.path.join(HERE, '..', 'site', 'index.html')
X0, FW, RH = 80, 3057, 920                     # the frame's inner box and a row's height
HERO, MINI, CALL = (80, 1600), (1780.4, 144.3), (2033, 1104)   # x and width of each part, in the frame
CALL_H = 637
RED = dict(left=(1770 - 1780.4) / 144.3, width=165 / 144.3, height=92 / 920)   # the red square, measured on the frame
# state: (image set, where the red square sits, the hero's secondary line, minimap caption, callout caption)
STATES = [('after', 'bot', 30.1, 'Create a new pension, or Combine existing ones.', 'Redesign', '3rd section from top: promoted 6 spots'),
          ('before', 'top', 66.7, 'Create a new pension in minutes', 'Previously', '9th section from top')]

def pct(x, w): return 'left:%.3f%%;width:%.3f%%' % (100 * (x - X0) / FW, 100 * w / FW)
cy = RH - CALL_H
call = '%s;top:%.3f%%;height:%.3f%%' % (pct(*CALL), 100 * cy / RH, 100 * CALL_H / RH)
parts = []
for v, n, top, sub, mcap, ccap in STATES:
    parts.append(
        '<img class="web-hero" data-v="%s" style="%s" src="img/websites/hero-%s.webp" alt="" width="936" height="538" loading="lazy">'
        '<span class="it-cap web-cap" data-v="%s" style="%s;top:calc(100%% + 10px)">Tag: %s</span>'
        '<img class="web-mimg" data-v="%s" style="%s" src="img/websites/minimap-%s.webp" alt="" width="84" height="538" loading="lazy">'
        '<span class="it-cap web-cap web-mcap" data-v="%s" style="%s;top:calc(100%% + 10px)">%s</span>'
        '<img class="web-call" data-v="%s" style="%s" src="img/websites/combine-%s.webp" alt="" width="646" height="373" loading="lazy">'
        '<span class="it-cap web-cap" data-v="%s" style="%s;bottom:calc(%.3f%% + 10px)">%s</span>'
        '<span class="it-cap web-cap" data-v="%s" style="%s;top:calc(100%% + 10px)">Combine section</span>'
        % (v, pct(*HERO), n, v, pct(*HERO), sub, v, pct(*MINI), n, v, pct(*MINI), mcap, v, call, n, v, pct(*CALL), 100 * (RH - cy) / RH, ccap, v, pct(*CALL)))
# the red square: one element, moved between the two sections
red = ('<i class="web-red" style="left:calc(%.3f%% + %.3f * %.3f%%);width:%.3f%%;height:%.3f%%;--at:%.2f%%;--was:%.2f%%"></i>'
       % (100 * (MINI[0] - X0) / FW, RED['left'], 100 * MINI[1] / FW, 100 * RED['width'] * MINI[1] / FW, 100 * RED['height'], STATES[0][2], STATES[1][2]))
block = ('<!-- WEBSITE start: built by source/website.py, do not edit by hand -->\n'
         '<div class="webs" style="--rh:%.4f">\n'
         '<div class="web-head"><button type="button" class="web-prev" aria-pressed="false">Previously</button></div>\n'
         '<div class="web" id="web" role="img" aria-label="The Penfold website home, redesigned: Combine old pensions is the 3rd section. '
         'Previously, Find and combine was the 9th.">\n%s\n%s\n</div>\n</div>\n'
         '<script>/* "Previously": hovering (or focusing, or tapping) shows the earlier site; leaving restores the redesign */\n'
         '(function(){var w=document.getElementById("web"),b=w.previousElementSibling.firstElementChild;'
         'function set(on){w.classList.toggle("prev",on);b.setAttribute("aria-pressed",on)}'
         'b.addEventListener("mouseenter",function(){set(true)});b.addEventListener("mouseleave",function(){set(false)});'
         'b.addEventListener("focus",function(){set(true)});b.addEventListener("blur",function(){set(false)});'
         'b.addEventListener("pointerup",function(e){if(e.pointerType!=="mouse")set(!w.classList.contains("prev"))})})();</script>\n'
         '<!-- WEBSITE end -->' % (RH / FW, '\n'.join(parts), red))
page = open(SITE, encoding='utf-8').read()
page = re.sub(r'<!-- WEBSITE start[\s\S]*?<!-- WEBSITE end -->', lambda m: block, page)
open(SITE, 'w', encoding='utf-8').write(page)
print('composition written')
