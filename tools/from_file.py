#!/usr/bin/env python3
"""Store a page that is a single HTML file (fonts and images inside it), whole.

    python3 tools/from_file.py cable ~/Claude/Portfolio/OlderVersions/cable.html \\
        --id 2024-07-06 --made 2026-09-21T14:42:00+01:00 --width 1920
"""
import argparse, re, shutil
from pathlib import Path
from common import vendor, write_meta, new_dest


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("project")
    ap.add_argument("file", type=Path)
    ap.add_argument("--id", required=True)
    ap.add_argument("--name", default="")
    ap.add_argument("--shipped")
    ap.add_argument("--until")
    ap.add_argument("--made", help="when it was made, for a version that never shipped")
    ap.add_argument("--width", type=int, default=1440)
    ap.add_argument("--source", default="", help="where the file came from, in words")
    ap.add_argument("--note", default="")
    a = ap.parse_args()

    dest = new_dest(a.project, a.id)
    (dest / "site").mkdir(parents=True)
    out = dest / "site" / "index.html"
    shutil.copyfile(a.file, out)
    text = out.read_text()
    if 'name="robots"' not in text:
        out.write_text(re.sub(r"<head>", '<head><meta name="robots" content="noindex">', text, count=1))
    vendored = vendor(dest / "site")
    write_meta(dest, {
        "project": a.project, "id": a.id, "name": a.name, "page": "site/index.html", "width": a.width,
        "shipped": a.shipped, "until": a.until, "made": a.made,
        "source": {"kind": "file", "from": a.source or str(a.file)}, "note": a.note,
    })
    print(f"stored {a.project}/{a.id}: {out.stat().st_size:,} bytes, {vendored} downloaded")


if __name__ == "__main__":
    main()
