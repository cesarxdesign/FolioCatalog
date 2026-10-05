#!/usr/bin/env python3
"""Ship Penfold Imagine to the live site: Portfolio/penfold/index.html, in the site's shell, taken from the
live Cable page (the other flagship): its head, the shared navbar and footer, the theme switch (folio0), the
fit-to-width zoom between 760 and 1440, the phone layout below 760, and analytics.

    python3 source/ship.py          writes Portfolio/penfold/ (index.html, vendor/, fonts/, img/)

The page's own nav, footer and theme button are dropped; the page follows the site theme. Project order on the
site (2026-09-30): Penfold, Cable, Confirmo, Mara, Starcount.
"""
import os, re, shutil
HERE = os.path.dirname(os.path.abspath(__file__))
SITE = os.path.join(HERE, '..', 'site')
PORT = os.path.abspath(os.path.join(HERE, *['..'] * 5, 'Portfolio'))
OUT = os.path.join(PORT, 'penfold')

src = open(os.path.join(SITE, 'index.html'), encoding='utf-8').read()
cable = open(os.path.join(PORT, 'cable', 'index.html'), encoding='utf-8').read()

# ---- the page's own CSS, with the rules that would reach the site's navbar and footer scoped or dropped
css = re.search(r'<style>([\s\S]*?)</style>\s*</head>', src).group(1)
css = css.replace('_vendor/', 'vendor/')
css = re.sub(r'\nnav\{[^}]*\}\nnav \.me\{[^}]*\}\nnav \.links\{[^}]*\}\n', '\n', css)
css = re.sub(r'\n/\* light/dark toggle in the nav \*/\n#theme\{[^}]*\}\n#theme:hover\{[^}]*\}\n', '\n', css)
css = re.sub(r'\nfooter\{[^}]*\}\nfooter \.next\{[^}]*\}\nfooter \.next a\{[^}]*\}\nfooter \.links\{[^}]*\}', '\n', css)
css = css.replace('a{color:var(--ink);text-decoration:none}a:hover{color:var(--acc)}', '.page a{color:var(--ink);text-decoration:none}.page a:hover{color:var(--acc)}')
css = css.replace('body{margin:0;background:#f2f5f7;', 'body{margin:0;background:#f2f5f7;overflow-x:clip;')
for bad in ['\nnav{', '\nfooter{', '#theme{']:
    assert bad not in css, bad

# ---- the phone layout (below 760): one column; strips and compositions scale down whole (see the script)
PHONE = r'''
/* phones: one column. Screen strips and compositions keep their layout and scale down to the column (script
   below); annotations drop their lead lines and sit under their strip. */
@media (max-width:760px){
 .page{width:auto;padding:0 20px}
 header{padding:56px 0 64px;gap:28px}
 header .kick{flex-wrap:wrap;gap:8px 12px;font-size:11px}
 h1{font-size:min(50px,12.2vw);line-height:.98;letter-spacing:-.05em}
 .lede{font-size:20px;line-height:1.4;letter-spacing:-.015em}
 .heroimg{height:280px;object-position:62% 50%;border-radius:8px;box-shadow:0 30px 70px -24px var(--halo)}
 .stats{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:28px 20px;padding-top:32px}
 .stat b{font-size:40px}.stat:last-child{grid-column:1/-1}
 .meta{flex-direction:column;align-items:stretch;gap:12px;padding-top:24px;font-size:15px}
 section.ch,section.ch.first{display:flex;flex-direction:column;gap:32px;padding:72px 0}
 .tag{flex-direction:row;align-items:baseline;gap:12px;padding-top:0}.tag b{font-size:30px}
 .body{gap:32px}
 h2{font-size:36px;line-height:1.06;letter-spacing:-.04em}
 .txt{font-size:17px}
 .two,.grid,.grid.three,.grid.four{grid-template-columns:minmax(0,1fr);gap:28px}
 .pull .big{font-size:28px}
 .ring{box-shadow:0 0 0 3px var(--glow)}
 .lead,.dot,.bracket,.cap.low .ct::before,.cap.low .ct::after{display:none}
 .ann{display:flex;flex-direction:column;gap:20px}
 .cap{position:static;width:auto}
 .cap .ct{font-size:18px}
 .st{grid-template-columns:minmax(0,1fr);justify-items:center;gap:24px}
 .st-list{width:100%}
 .box.split{grid-template-columns:minmax(0,1fr);gap:24px}
 .quote{padding:4px 0 4px 20px;gap:14px}.quote .q{font-size:30px}
 .qs{grid-template-columns:minmax(0,1fr);gap:16px}.qs-nav{justify-content:flex-end}
 .qs-head{flex-direction:column;align-items:flex-start;gap:12px}
 .closer{padding:88px 0 40px}.closer .big{font-size:44px;line-height:1.02}
 .proto{margin-bottom:12px}
}
'''

# ---- the site palette the navbar and footer read, in Penfold's colours (light accent blue, dark accent pink)
PALETTE = r''':root{--sysFont:'Inter',system-ui,-apple-system,'Segoe UI',Roboto,Helvetica,Arial,sans-serif;--sysMono:'IBM Plex Mono',ui-monospace,monospace;
 --bg:#f2f5f7;--ink:#151515;--body:#5b6470;--mut:#6b737b;--line:#e7e8ea;--hair:#e7e8ea;--line2:#C9D0DB;--accent:#6076DD;--band:#F8F8F8;--deep:#151515;--tint:#EEF1FC;--lab:#151515;
 --paperT:rgba(242,245,247,.86);--flagink:#6b737b;--ctl:rgba(20,30,40,.05);--ctlbd:rgba(20,30,40,.18)}
:root[data-theme="dark"]{--bg:#101519;--ink:#eef0f2;--body:#b3b7bd;--mut:#8b9198;--line:#2a2d33;--hair:#2a2d33;--line2:#3A404A;--accent:#FF5081;--band:#161B22;--deep:#1A2742;--tint:#2a1a22;--lab:#eef0f2;
 --paperT:rgba(16,21,25,.86);--flagink:#8b9198;--ctl:rgba(255,255,255,.06);--ctlbd:rgba(255,255,255,.18)}
.sfoot{--sfootW:1200px}
'''

# ---- the body: the page without its own nav, footer and theme script
body = re.search(r'<body>\s*([\s\S]*?)\s*</body>', src).group(1)
body = re.sub(r'<script>\s*\(function\(\)\{var page=document\.querySelector\(\'\.page\'\),b=document\.getElementById\(\'theme\'\);[\s\S]*?</script>', '', body)
body = re.sub(r'\n<nav>[\s\S]*?</nav>\n', '\n', body, count=1)
body = re.sub(r'\n<footer>[\s\S]*?</footer>\n', '\n', body, count=1)
body = body.replace('<div class="page" data-theme="light">', '<div class="page" id="case" data-theme="light">', 1)
body = body.replace('_vendor/', 'vendor/')
assert '<nav>' not in body and '<footer>' not in body and 'id="theme"' not in body

ORDER = [('penfold', 'Penfold'), ('cable', 'Cable'), ('confirmo', 'Confirmo'), ('mara', 'Mara'), ('starcount', 'Starcount')]
pjd = ''.join('<a class="on" href="index.html">%s</a>' % n if k == 'penfold' else '<a href="../%s/index.html">%s</a>' % (k, n) for k, n in ORDER)
flag = re.search(r'<div class="flag">[\s\S]*?</nav></div>', cable).group(0)
flag = re.sub(r'<nav class="pjd" aria-label="Projects">[\s\S]*?</nav>', '<nav class="pjd" aria-label="Projects">%s</nav>' % pjd, flag)
flag = flag.replace('<summary>Cable <svg', '<summary>Penfold <svg').replace('<span class="bn">Cable</span>', '<span class="bn">Penfold</span>')
foot = '<footer class="sfoot"><div class="snx"><span class="slab">Next</span><a class="snext" href="/cable">Cable <span>&rarr;</span></a></div><a class="smail" href="mailto:cesarxdesign@gmail.com">cesarxdesign@gmail.com</a></footer>'

# the site's scripts from Cable: theme switch, bar layout, fit zoom, analytics (retargeted to this page)
scripts = cable[cable.index('<script>', cable.index('<footer class="sfoot">')):cable.rindex('</body>')]
scripts = scripts.replace("var PAGE='cable'", "var PAGE='penfold'")
scripts = scripts.replace("document.querySelectorAll('section.sec')", "document.querySelectorAll('section.ch,section.closer')")
scripts = scripts.replace("var lab=e.target.querySelector('.lab');", "var lab=e.target.querySelector('.tag b');")
assert "var PAGE='penfold'" in scripts and 'section.ch' in scripts
SYNC = r'''<script>
/* the page follows the site theme: mirror the root's data-theme onto .page, which the page's CSS and the
   prototype frame read */
(function(){var p=document.getElementById("case"),r=document.documentElement;
 function s(){p.setAttribute("data-theme",r.getAttribute("data-theme")==="dark"?"dark":"light")}
 s();new MutationObserver(s).observe(r,{attributes:true,attributeFilter:["data-theme"]});})();
</script>
<script>
/* phones: strips and compositions keep their desktop layout (894 wide; the "what if I die?" screens 600) and
   scale down whole to the column */
(function(){var Q=".sw,.flow:not(.final):not(.sw .flow),.duo,.proto,.webs",M=760;
 function fit(){var w=document.documentElement.clientWidth,on=w<=M;
  document.querySelectorAll(Q).forEach(function(e){if(!on){e.style.zoom="";e.style.width="";e.style.flex="";return}
   var nat=e.matches(".box.split .flow")?600:894,box=e.parentElement.clientWidth;
   e.style.width=nat+"px";e.style.flex="none";e.style.zoom=Math.min(1,box/nat).toFixed(4)})}
 if(document.readyState!=="loading")fit();else addEventListener("DOMContentLoaded",fit);addEventListener("resize",fit);})();
</script>
'''

head = cable[:cable.index('<style>')]
head = head.replace('<title>Cable &middot; Cesar Garcia</title>', '<title>Penfold &middot; Cesar Garcia</title>')
head = re.sub(r'<meta name="description" content="[^"]*">', '<meta name="description" content="Penfold, a founding designer case study. Pensions took days; ours took minutes. From a 7-day first version to 3,000 savers and £4M under management in a year.">', head)
head = head.replace('<link rel="preload" as="image" href="/cable/img/v3/hero.webp" fetchpriority="high">', '<link rel="preload" as="image" href="/penfold/img/hero.webp" fetchpriority="high">\n<link rel="stylesheet" href="/penfold/vendor/25028d0170-css2.css">')
assert '<title>Penfold' in head and '/penfold/img/hero.webp' in head

page = (head + '<style>\n' + PALETTE + css + PHONE + '</style>\n</head>\n<body>\n' + flag + '\n' + body + '\n' + foot + '\n' + SYNC + scripts + '</body>\n</html>\n')
# the page's own stylesheet link was relative; the head already loads it from /penfold/vendor
page = page.replace('<link rel="stylesheet" href="vendor/25028d0170-css2.css">', '')
# the live URL is /penfold (no trailing slash), so relative paths would resolve from the site root: make them absolute
page = page.replace('src="img/', 'src="/penfold/img/').replace('url(vendor/', 'url(/penfold/vendor/').replace('url(fonts/', 'url(/penfold/fonts/')
assert 'src="img/' not in page and 'url(vendor/' not in page and 'url(fonts/' not in page

os.makedirs(OUT, exist_ok=True)
open(os.path.join(OUT, 'index.html'), 'w', encoding='utf-8').write(page)
for d_src, d_out in [('_vendor', 'vendor'), ('fonts', 'fonts'), ('img', 'img')]:
    shutil.copytree(os.path.join(SITE, d_src), os.path.join(OUT, d_out), dirs_exist_ok=True)
print('wrote %s (%d KB)' % (os.path.join(OUT, 'index.html'), len(page.encode()) // 1024))
