#!/usr/bin/env python3
"""Store a folio page as it was at a Portfolio git ref, whole.

    python3 tools/from_portfolio.py cable --ref 78b4426 --id 2026-09-23-shipped --name Shipped \\
        --shipped 2026-09-23T23:12:11+01:00

Copies <project>/ plus everything outside it the page loads (shared CSS, fonts), from git,
never from the working tree: what is committed is what Vercel served. Then:
  - root-absolute paths (/cable/fonts/x) become relative, so the copy works in any folder
  - links to other pages point at the live folio
  - Google Fonts and any other external file the page loads is downloaded into the copy
  - analytics scripts are removed and the page is marked noindex
"""
import argparse, posixpath, re, subprocess, sys
from common import ROOT, LIVE, DATA_URL, outside_data, vendor, write_meta, new_dest

PORTFOLIO = ROOT.parent / "Portfolio"
TEXT = (".html", ".css")
# url(...) inside an HTML attribute writes its quotes as &quot;
REF_RE = re.compile(r'''((?:href|src)=["']|url\(\s*(?:&quot;|["'])?)([^"')\s>&]+(?:&(?!quot;)[^"')\s>&]*)*)''')
ANALYTICS = re.compile(r"<script\b[^>]*>(?:(?!</script>).)*?posthog(?:(?!</script>).)*?</script>", re.S | re.I)


def git(*args, binary=False):
    out = subprocess.run(["git", "-C", str(PORTFOLIO), *args], capture_output=True, check=True)
    return out.stdout if binary else out.stdout.decode()


def is_local(url):
    # "%23x" is "#x" encoded: a reference inside the page (an SVG gradient), not a file
    return not re.match(r"^(?:[a-z][a-z0-9+.-]*:|//|#|%23)", url, re.I) and url != ""


def resolve(from_file, url):
    """Repo path a local URL points at, from the file that contains it."""
    path = url.split("#")[0].split("?")[0]
    if not path:
        return None
    base = "" if path.startswith("/") else posixpath.dirname(from_file)
    return posixpath.normpath(posixpath.join(base, path.lstrip("/")))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("project")
    ap.add_argument("--ref", default="HEAD")
    ap.add_argument("--id", required=True, help="folder name, e.g. 2026-09-21")
    ap.add_argument("--name", default="", help="what the version is called, e.g. Noir")
    ap.add_argument("--shipped", help="when it went live, ISO 8601 with offset")
    ap.add_argument("--until", help="when it left the live folio, ISO 8601 with offset")
    ap.add_argument("--width", type=int, default=1440, help="width it was designed at")
    ap.add_argument("--note", default="")
    a = ap.parse_args()

    commit = git("rev-parse", a.ref + "^{commit}").strip()
    files = set(git("ls-tree", "-r", "--name-only", commit).split("\n")) - {""}
    page = f"{a.project}/index.html"
    if page not in files:
        sys.exit(f"{page} is not in Portfolio at {a.ref}")

    # The project folder, plus the closure of what its HTML and CSS load from outside it.
    take = {f for f in files if f.startswith(a.project + "/") and not f.endswith(".ui")}
    queue = [f for f in take if f.endswith(TEXT)]
    while queue:
        f = queue.pop()
        for _, url in REF_RE.findall(DATA_URL.sub("", git("show", f"{commit}:{f}"))):
            if not is_local(url):
                continue
            p = resolve(f, url)
            # Other pages are navigation, not something this page loads: they stay live links.
            if p in files and p not in take and not p.endswith(".html"):
                take.add(p)
                if p.endswith(TEXT):
                    queue.append(p)

    dest = new_dest(a.project, a.id)

    def rewrite(from_file, text):
        def sub(m):
            lead, url = m.groups()
            if not is_local(url):
                return m.group(0)
            p = resolve(from_file, url)
            suffix = url[len(url.split("#")[0].split("?")[0]):]
            if p not in take and p + "/index.html" in take:
                p += "/index.html"
            if p in take:
                return lead + posixpath.relpath(p, posixpath.dirname(from_file) or ".") + suffix
            if not lead.startswith("href"):
                return m.group(0)   # a file that was missing on the live site too: leave it as it was
            live = re.sub(r"(^|/)index\.html$", "", "" if p == "." else p).rstrip("/")
            return lead + LIVE + "/" + live + suffix
        return outside_data(text, lambda part: REF_RE.sub(sub, part))

    for f in sorted(take):
        out = dest / "site" / f
        out.parent.mkdir(parents=True, exist_ok=True)
        data = git("show", f"{commit}:{f}", binary=True)
        if f.endswith(TEXT):
            text = rewrite(f, data.decode())
            if f.endswith(".html"):
                text = ANALYTICS.sub("", text)
                if 'name="robots"' not in text:
                    text = re.sub(r"<head>", '<head><meta name="robots" content="noindex">', text, count=1)
            data = text.encode()
        out.write_bytes(data)
    vendored = vendor(dest / "site")

    tags = [t for t in git("tag", "--points-at", commit).split() if t]
    write_meta(dest, {
        "project": a.project,
        "id": a.id,
        "name": a.name,
        "page": f"site/{page}",
        "width": a.width,
        "shipped": a.shipped,
        "until": a.until,
        "source": {"kind": "portfolio", "ref": tags[0] if tags else commit[:7], "commit": commit,
                   "committed": git("show", "-s", "--format=%cI", commit).strip()},
        "note": a.note,
    })
    print(f"stored {a.project}/{a.id}: {len(take)} files from {commit[:7]}, {vendored} downloaded")


if __name__ == "__main__":
    main()
