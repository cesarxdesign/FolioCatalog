#!/usr/bin/env python3
"""Build a Harmony round: the five live case studies, each with the one shared styling applied.

    python3 tools/harmony.py

Every run is a new round, named by the time it was built (15:42:07), so rounds sit side by side
in the viewer and none is overwritten. Each page of the round is the stored `current-<page>` copy plus versions/harmony/_system/harmony.css,
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
                 "<h1>Tripled conversion.<br><em>$135M a year added.</em></h1>"),
    "mara": ('<h1 class="hh">20M users added.<br>$6.9M a year saved.</h1>',
             '<h1 class="hh">20M users added.<br><em>$6.9M a year saved.</em></h1>'),
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


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--note", default="")
    a = ap.parse_args()
    css = (H / "_system" / "harmony.css").read_text()
    t = datetime.now(timezone.utc).astimezone()
    now, a.name, a.round = t.isoformat(timespec="seconds"), t.strftime("%H:%M:%S"), t.strftime("%Y%m%d-%H%M%S")

    for i, page in enumerate(PAGES, 1):
        src, dest = H / f"current-{page}", H / f"{a.round}-{page}"
        made = now
        shutil.copytree(src, dest)
        (dest / "site" / "harmony.css").write_text(css)

        kind = "lite" if page in LITE else page
        f = dest / "site" / page / "index.html"
        html = f.read_text()
        # The address changes with the file, so a refresh never shows an old copy of it.
        links = f'<link rel="stylesheet" href="../harmony.css?v={hashlib.sha1(css.encode()).hexdigest()[:8]}">'
        if kind == "lite":
            vend = dest / "site" / "_vendor"
            cable = H / "current-cable" / "site" / "_vendor"
            shutil.copy(cable / FONTS, vend / FONTS)
            for name in re.findall(r"url\(([^)]+\.woff2)\)", (cable / FONTS).read_text()):
                shutil.copy(cable / name, vend / name)
            links = f'<link rel="stylesheet" href="../_vendor/{FONTS}">' + links
            html = once(html, *H1[page], f"{page} headline")
            html = re.sub(r'(<header class="[^"]*\bhd\b[^"]*">)',
                          rf'\1<div class="hkick"><span class="hchip">{page.capitalize()}</span><span>{KICK[page]}</span></div>', html, count=1)
            facts = "".join(f'<div><span class="k">{k}</span><span>{v}</span></div>'
                            for k, v in zip(("Role", "Timeline", "Users"), FACTS[page]))
            html, n = re.subn(r'<p class="roleline">.*?</p>', f'<div class="hfacts">{facts}</div>', html, count=1, flags=re.S)
            if n != 1:
                raise SystemExit(f"{page}: role line not found")
            html = once(html, '<footer class="sfoot">', FIT + '<footer class="sfoot">', f"{page} footer")
        # After every stylesheet the page already has, before anything it draws.
        html = once(html, '<div class="flag">', links + '<div class="flag">', f"{page} navbar")
        html = html.replace("<body", f'<body data-h="{kind}"', 1)
        f.write_text(html)

        meta = json.loads((dest / "meta.json").read_text())
        meta.update(id=f"{a.round}-{page}", name=a.name, made=made, order=i,
                    note=a.note or f"Harmony {a.name}: the live page with the shared styling (harmony.css) applied.")
        (dest / "meta.json").write_text(json.dumps(meta, indent=2, ensure_ascii=False) + "\n")
        print(f"{a.round}-{page}")
    build.main()


if __name__ == "__main__":
    main()
