#!/usr/bin/env python3
"""Build a Harmony round: the five live case studies, each with the one shared styling applied.

    python3 tools/harmony.py           content changed (words, names, colour): the newest round is rebuilt in place
    python3 tools/harmony.py --new     the styling changed: a new round, named by the time it was built (15:42:07)

A new version is for a change of styling only: rhythm, spacing, sizes. Anything else is content
and updates the round already there. Each page of the round is the stored `current-<page>` copy plus versions/harmony/_system/harmony.css,
which holds every size and spacing once. Edit that file, run this again, refresh the viewer: all
five change. `current-*` is never touched. Nothing here goes near Portfolio.
"""
import argparse, hashlib, json, re, shutil
from datetime import datetime, timezone
from pathlib import Path
import build

ROOT = Path(__file__).resolve().parent.parent
H = ROOT / "versions" / "harmony"
PAGES = ["penfold", "cable", "confirmo", "mara", "starcount"]   # as the home page lists them
LITE = {"confirmo", "mara", "starcount"}
FONTS = "e91c91b4d8-css2.css"    # Geist and Geist Mono, as stored with the Cable copy

# The flagships open on two lines, the second in the accent. Same words, set the same way.
H1 = {
    "confirmo": ("<h1>Tripled conversion. <em>$135M a year added</em>.</h1>",
                 "<h1>Tripled conversion.<br><em>+$135M yearly.</em></h1>"),   # shortened by Cesar to fit the column (2026-10-05)
    "mara": ('<h1 class="hh">20M users added.<br>$6.9M a year saved.</h1>',
             '<h1 class="hh">20M users added.<br><em>$6.9M saved.</em></h1>'),   # "a year" cut by Cesar to fit the column (2026-10-05)
    "starcount": ("<h1>Hit &pound;1M first-year target, in 91 days.</h1>",
                  "<h1>Hit &pound;1M first-year target, <em>in 91 days.</em></h1>"),
}
# The line beside the chip and the three facts under the numbers, as Penfold and Cable have them.
# Every word is from Portfolio/TheRecord/<page>.md (domain tags, home card, role, CV dates, users).
KICK = {
    "confirmo": "Crypto payments &middot; Checkout &middot; Web",
    "mara": "Digital wallet &middot; B2C fintech &middot; Android and iOS",
    "starcount": "Data intelligence &middot; Enterprise &middot; Desktop web",
}
FACTS = {
    "confirmo": ("Principal Product Designer, first designer", "Sep 2025 to Jul 2026", "Buyers and merchants"),
    "mara": ("Head of Design and Product Owner", "Nov 2022 to Feb 2024", "Wallet users in Africa, mostly Nigerian"),
    "starcount": ("Head of Product Design, first designer", "Dec 2015 to May 2019", "Enterprise marketing teams"),
}
# Chapter names changed for the label column, where they are now the big word (approved 2026-10-05).
LABS = {
    "confirmo": {"context": "constraint"},
    "mara": {"solution": "KYC", "iteration": "onboarding"},
    "starcount": {"context": "reports", "data visualization": "the&nbsp;lie"},   # one line, on request
}
# Trials that belong to one page, not to the system: colour stays with the page.
TRIAL = {
    # Penfold pink ("Pinkfold", #FF5081) as the accent in light too, as it already is in dark (on request, 2026-10-05)
    "penfold": ('<style>.page[data-theme="light"]{--acc:#FF5081;--acc2:#FF7A9F;--accg:#FF5081;--chip:#FF5081;'
                '--glow:rgba(255,80,129,.05);--halo:rgba(255,80,129,.14)}'
                ':root:not([data-theme="dark"]){--accent:#FF5081;--tint:#FFEEF3}'
                # the pension tags in Sep were the reverse of the accent (pink on indigo); with pink as the accent they turn indigo
                '.page[data-theme="light"] .relay code.pn{background:#6076DD}</style>'),
    # the accent fade started too pale on light (on request, 2026-10-05): a deeper first colour, as the
    # other pages' fades have. Penfold's is in its line above (#FFA9C1 before); Mara's was #f7bd77.
    "mara": '<style>:root:not([data-theme="dark"]){--accent2:#F4914A}</style>',
}
# Three numbers in the hero, as the flagships have (on request, 2026-10-05): one dropped per page.
STAT = lambda b, t: f'<div class="stat"><b>{b}</b><span>{t}</span></div>'
STATS = {
    "confirmo": [(STAT("0", "backend changes"), "")],
    "mara": [(STAT("-70%", "onboarding steps"), "")],
    "starcount": [(STAT("1 lie", "to make it work"), "")],
}
# The order of the hero numbers, given 2026-10-05: each number is found by the text it starts with.
ORDER = {
    "penfold": ["0 &rarr; 1", "&pound;4M", "3,000"],
    "cable": ["Free &rarr; Paid", "10x", "90%+"],
    "confirmo": ["$135M", "3x", "43%"],
    "mara": ["$5.7M", "+1.7M", "88%"],
}
BLOCK = {"penfold": r'<div class="stat"><b>(.*?)</b>.*?</div>', "cable": r'<div class="metric"><div class="n"><span class="acc">(.*?)</span>.*?</div></div>',
         "lite": r'<div class="stat"><b>(.*?)</b>.*?</div>'}


def reorder(html, page, kind):
    found = list(re.finditer(BLOCK[kind], html))
    by = {m.group(1): m.group(0) for m in found}
    want = ORDER[page]
    if sorted(by) != sorted(want):
        raise SystemExit(f"{page} stats: found {sorted(by)}, wanted {sorted(want)}")
    out, last = [], 0
    for m, key in zip(found, want):   # each slot keeps its place and whitespace; only its block changes
        out += [html[last:m.start()], by[key]]
        last = m.end()
    return "".join(out) + html[last:]


# Lines reworded by Cesar, set exactly as given.
COPY = {
    "confirmo": [("above the crypto average of 24%.", "above the 24% crypto average.")],
}
FIT = ('<script>/* between phone and full width the page keeps its 1440 layout and scales, as Penfold and Cable do;'
       ' a figure drawn wider than the content column is scaled down to it, as every flagship image is */'
       '(function(){var el=document.querySelector(".page"),W=1440,M=760;'
       'function fit(){var w=document.documentElement.clientWidth,on=w>M;el.style.zoom=(on&&w<W)?(w/W):"";'
       'document.querySelectorAll(".sec").forEach(function(s){var h=s.querySelector("h2");if(!h)return;'
       's.querySelectorAll(":scope>*:not(.lab):not(.wrap),:scope>.wrap>*:not(.lab)").forEach(function(e){'
       'e.style.zoom="";if(!on)return;var c=h.getBoundingClientRect().width,x=e.getBoundingClientRect().width;'
       'if(x>c+1)e.style.zoom=c/x;});});}'
       'fit();addEventListener("resize",fit);addEventListener("load",fit);if(document.fonts)document.fonts.ready.then(fit);})();</script>')


def once(text, old, new, what):
    if text.count(old) != 1:
        raise SystemExit(f"{what}: expected one match, found {text.count(old)}")
    return text.replace(old, new)


SKETCH = H / "_system" / "penfold" / "sketches-strip-pink.webp"


def dress(html, page, links):
    """One page, with the system's stylesheet linked and its content edits made. Used for a round
    here and, with --ship, for the pages in Portfolio: the same function, so the same result."""
    kind = "lite" if page in LITE else page
    if kind == "lite":
        html = once(html, *H1[page], f"{page} headline")
        for old, new in STATS[page]:
            html = once(html, old, new, f"{page} stat")
        for old, new in COPY.get(page, []):
            html = once(html, old, new, f"{page} copy")
        for old, new in LABS[page].items():
            html = once(html, f'<p class="lab">{old}</p>', f'<p class="lab">{new}</p>', f"{page} label {old}")
        html = re.sub(r'(<header class="[^"]*\bhd\b[^"]*">)',
                      rf'\1<div class="hkick"><span class="hchip">{page.capitalize()}</span><span>{KICK[page]}</span></div>', html, count=1)
        facts = "".join(f'<div><span class="k">{k}</span><span>{v}</span></div>'
                        for k, v in zip(("Role", "Timeline", "Users"), FACTS[page]))
        html, n = re.subn(r'<p class="roleline">.*?</p>', f'<div class="hfacts">{facts}</div>', html, count=1, flags=re.S)
        if n != 1:
            raise SystemExit(f"{page}: role line not found")
        html = once(html, '<footer class="sfoot">', FIT + '<footer class="sfoot">', f"{page} footer")
    if page in ORDER:
        html = reorder(html, page, kind)
    if page == "cable":
        # v2.0's feature grid: Risk Assessment and Assurance change places (on request, 2026-10-05)
        feats = list(re.finditer(r'<div class="feat">.*?</div>', html, re.S))
        at = {re.search(r"<h3>\s*(.*?)\s*</h3>", m.group(0), re.S).group(1): m for m in feats}
        x, y = sorted((at["Assurance"], at["Risk Assessment"]), key=lambda m: m.start())
        html = html[:x.start()] + y.group(0) + html[x.end():y.start()] + x.group(0) + html[y.end():]
    if page == "penfold":
        # the day-one sketches in light: their blue ink redrawn in the accent, as the dark file already has it
        # (sketches-strip-pink.webp, recoloured from sketches-strip.webp; a new name, so no cache serves the old one)
        html = once(html, "img/sketches-strip.webp", "img/sketches-strip-pink.webp", "penfold sketches")
    # After every stylesheet the page already has, before anything it draws.
    html = once(html, '<div class="flag">', links + TRIAL.get(page, '') + '<div class="flag">', f"{page} navbar")
    return html.replace("<body", f'<body data-h="{kind}"', 1)


def ship():
    """Put the system on the five pages in Portfolio's working tree. Nothing is committed or pushed here."""
    folio = ROOT.parent / "Portfolio"
    css = (H / "_system" / "harmony.css").read_text()
    pages = {p: (folio / p / "index.html") for p in PAGES}
    links = f'<link rel="stylesheet" href="/harmony.css?v={hashlib.sha1(css.encode()).hexdigest()[:8]}">'
    done = [p for p, f in pages.items() if "data-h=" in f.read_text()]
    if len(done) == len(pages):   # already on the system: only the stylesheet moves, and its address with it
        (folio / "harmony.css").write_text(css)
        for p, f in pages.items():
            html, n = re.subn(r'<link rel="stylesheet" href="/harmony\.css\?v=[0-9a-f]+">', links, f.read_text())
            if n != 1:
                raise SystemExit(f"{p}: stylesheet link not found")
            f.write_text(html)
            print(f"Portfolio/{p}/index.html: stylesheet updated")
        return
    if done:
        raise SystemExit(f"only some pages carry the system: {', '.join(done)}")
    out = {p: dress(f.read_text(), p, links) for p, f in pages.items()}   # all five, or none
    (folio / "harmony.css").write_text(css)
    shutil.copy(SKETCH, folio / "penfold" / "img")
    for p, f in pages.items():
        f.write_text(out[p])
        print(f"Portfolio/{p}/index.html")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--new", action="store_true", help="the styling changed: make a new round")
    ap.add_argument("--note", default="")
    ap.add_argument("--ship", action="store_true", help="apply the system to the pages in Portfolio (working tree only)")
    a = ap.parse_args()
    if a.ship:
        return ship()
    css = (H / "_system" / "harmony.css").read_text()
    t = datetime.now(timezone.utc).astimezone()
    now, a.name, a.round = t.isoformat(timespec="seconds"), t.strftime("%H:%M:%S"), t.strftime("%Y%m%d-%H%M%S")
    rounds = sorted(d.name[:15] for d in H.glob("[0-9]*-penfold"))
    if not a.new and rounds:   # content only: the newest round keeps its name and its place in time
        a.round = rounds[-1]
        old = json.loads((H / f"{a.round}-penfold" / "meta.json").read_text())
        now, a.name = old["made"], old["name"]

    for i, page in enumerate(PAGES, 1):
        src, dest = H / f"current-{page}", H / f"{a.round}-{page}"
        made = now
        if dest.exists():
            shutil.rmtree(dest)
        shutil.copytree(src, dest)
        (dest / "site" / "harmony.css").write_text(css)
        f = dest / "site" / page / "index.html"
        # The address changes with the file, so a refresh never shows an old copy of it.
        links = f'<link rel="stylesheet" href="../harmony.css?v={hashlib.sha1(css.encode()).hexdigest()[:8]}">'
        if page in LITE:   # Geist, for the rounds made before the system moved to Inter
            vend = dest / "site" / "_vendor"
            cable = H / "current-cable" / "site" / "_vendor"
            shutil.copy(cable / FONTS, vend / FONTS)
            for name in re.findall(r"url\(([^)]+\.woff2)\)", (cable / FONTS).read_text()):
                shutil.copy(cable / name, vend / name)
            links = f'<link rel="stylesheet" href="../_vendor/{FONTS}">' + links
        if page == "penfold":
            shutil.copy(SKETCH, dest / "site" / "penfold" / "img")
        f.write_text(dress(f.read_text(), page, links))

        meta = json.loads((dest / "meta.json").read_text())
        meta.update(id=f"{a.round}-{page}", name=a.name, made=made, order=i,
                    note=a.note or f"Harmony {a.name}: the live page with the shared styling (harmony.css) applied.")
        (dest / "meta.json").write_text(json.dumps(meta, indent=2, ensure_ascii=False) + "\n")
        print(f"{a.round}-{page}")
    build.main()


if __name__ == "__main__":
    main()
