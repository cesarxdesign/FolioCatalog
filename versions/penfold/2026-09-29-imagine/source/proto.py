#!/usr/bin/env python3
"""The annotated prototype, built into the page: site/craft.html is embedded as the iframe's srcdoc instead of
being loaded from its own file, so no browser or viewer can show a stale cached copy of it (2026-09-29).

    python3 source/proto.py         rewrites the iframe between the PROTO markers in site/index.html

craft.html reads its options from location.hash, which a srcdoc frame does not have, so the options this page
uses (bare, crop) are written into the copy directly. Relative URLs (fonts/) resolve against the page, as before.
"""
import html, os, re
HERE = os.path.dirname(os.path.abspath(__file__))
SITE = os.path.join(HERE, '..', 'site', 'index.html')
CRAFT = os.path.join(HERE, '..', 'site', 'craft.html')
OPTS = '#bare&crop=0,30,2178,1320'   # widened when the notes moved clear of the frame (2026-09-29)
TITLE = ('The savings estimate prototype: twelve screens, wireframe to high fidelity, wired up with interaction lines and '
         'annotated in handwriting: review copy, more contrast, check touch targets, not helpful for small values, allows '
         'inconsistent state, spacing')

doc = open(CRAFT, encoding='utf-8').read()
assert doc.count('location.hash') == 2, doc.count('location.hash')
doc = doc.replace('location.hash', repr(OPTS))
frame = ('<!-- PROTO start: built by source/proto.py from site/craft.html, do not edit by hand -->'
         '<div class="proto"><iframe srcdoc="%s" title="%s" scrolling="no"></iframe></div>'
         '<!-- PROTO end -->' % (html.escape(doc, quote=True), TITLE))
page = open(SITE, encoding='utf-8').read()
if '<!-- PROTO start' not in page:
    m = re.search(r'<div class="proto"><iframe src="craft\.html[^"]*"[^>]*></iframe></div>', page)
    assert m, 'prototype iframe not found'
    page = page[:m.start()] + '<!-- PROTO start --><!-- PROTO end -->' + page[m.end():]
page = re.sub(r'<!-- PROTO start[\s\S]*?<!-- PROTO end -->', lambda m: frame, page)
open(SITE, 'w', encoding='utf-8').write(page)
print('prototype embedded, %d bytes' % len(doc))
