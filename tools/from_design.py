#!/usr/bin/env python3
"""Store a Claude Design canvas (claude.ai artifact) as one plain HTML page, whole.

    python3 tools/from_design.py cable --id 2026-09-23-crazy --name Crazy \\
        --canvas https://claude.ai/artifact/2xjjdZJBfFqQ3EUsddf3Nu --made 2026-09-23T22:19:48+01:00 \\
        --boards dl/project/Main.dc.html dl/project/Main-2.dc.html --blobs dl/blobs \\
        --vals '{"theme":"dark","accFf":"inherit"}'

A canvas artboard (.dc.html) only renders inside the canvas editor. This writes what it
renders: the artboards stacked top to bottom as one page, each {{value}} filled in as the
artboard's current settings give it (--vals, plus any plain string renderVals returns),
every /_blob/ image copied into img/, links like /cv pointed at the live folio, and
Google Fonts downloaded. The artboard files and canvas.json go in source/ beside it, unchanged.
"""
import argparse, json, re, shutil
from pathlib import Path
from common import LIVE, vendor, write_meta, new_dest

HELMET = re.compile(r"<helmet>(.*?)</helmet>", re.S)
XDC = re.compile(r"<x-dc>(.*?)</x-dc>", re.S)
HOLE = re.compile(r"\{\{\s*([\w.]+)\s*\}\}")
LITERAL = re.compile(r"""\b(\w+):\s*'([^'\\]*)'""")  # renderVals entries that are plain strings


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("project")
    ap.add_argument("--id", required=True)
    ap.add_argument("--name", default="")
    ap.add_argument("--canvas", required=True, help="the claude.ai artifact it came from")
    ap.add_argument("--made", help="when it was made")
    ap.add_argument("--edited", help="when it was last saved")
    ap.add_argument("--boards", nargs="+", type=Path, required=True, help="artboards, top to bottom")
    ap.add_argument("--extra", nargs="*", type=Path, default=[], help="other source files to keep (canvas.json)")
    ap.add_argument("--blobs", type=Path, help="folder holding the downloaded /_blob/<id>.<ext> images")
    ap.add_argument("--vals", default="{}", help="JSON: values for {{holes}} that renderVals computes")
    ap.add_argument("--note", default="")
    a = ap.parse_args()

    dest = new_dest(a.project, a.id)
    site = dest / "site"
    (site / "img").mkdir(parents=True)
    (dest / "source").mkdir()
    given = json.loads(a.vals)

    heads, bodies, width = [], [], 0
    for board in a.boards:
        src = board.read_text()
        shutil.copyfile(board, dest / "source" / board.name)
        if re.search(r"<(sc-for|sc-if|dc-import|x-import)\b", src):
            raise SystemExit(f"{board.name} uses components this converter does not expand")
        script = src[src.find("data-dc-script"):]
        vals = {k: v for k, v in LITERAL.findall(script.split("renderVals", 1)[-1])}
        vals.update(given)
        body = XDC.search(src).group(1)
        for h in HELMET.findall(body):
            if h.strip() not in heads:
                heads.append(h.strip())
        body = HELMET.sub("", body)
        missing = sorted({k for k in HOLE.findall(body) if k not in vals})
        if missing:
            raise SystemExit(f"{board.name}: no value for {missing}; pass them in --vals")
        bodies.append(HOLE.sub(lambda m: vals[m.group(1)], body).strip())
        preview = json.loads(re.search(r"data-props='([^']*)'", src).group(1)).get("$preview", {})
        width = max(width, preview.get("width", 0))
    for f in a.extra:
        shutil.copyfile(f, dest / "source" / f.name)

    title = re.search(r"<title>(.*?)</title>", a.boards[0].read_text()).group(1)
    title = re.sub(r",? (mobile )?part \d+$", "", title)
    page = (f'<!doctype html>\n<html lang="en">\n<head>\n<meta charset="utf-8">\n'
            f'<meta name="viewport" content="width={width}">\n<meta name="robots" content="noindex">\n'
            f"<title>{title}</title>\n" + "\n".join(heads) +
            f"\n</head>\n<body>\n" + "\n".join(bodies) + "\n</body>\n</html>\n")

    def blob(m):
        hits = list(a.blobs.glob(m.group(1) + ".*")) if a.blobs else []
        if not hits:
            raise SystemExit(f"image {m.group(1)} not found in {a.blobs}")
        shutil.copyfile(hits[0], site / "img" / hits[0].name)
        return "img/" + hits[0].name
    page = re.sub(r"/_blob/([0-9a-f]{32})", blob, page)
    # Site-relative links (/cv) meant the folio; outside it they need its address.
    page = re.sub(r'href="/(?!/)', f'href="{LIVE}/', page)
    (site / "index.html").write_text(page)
    if not any((site / "img").iterdir()):
        (site / "img").rmdir()
    vendored = vendor(site)

    write_meta(dest, {
        "project": a.project, "id": a.id, "name": a.name, "page": "site/index.html", "width": width,
        "shipped": None, "made": a.made, "edited": a.edited,
        "source": {"kind": "claude-design", "canvas": a.canvas, "boards": [b.name for b in a.boards],
                   "values": given},
        "note": a.note,
    })
    print(f"stored {a.project}/{a.id}: {len(a.boards)} artboards, {width} wide, {vendored} downloaded")


if __name__ == "__main__":
    main()
