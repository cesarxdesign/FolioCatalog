"""Shared by the tools that store a version: vendoring, meta, paths."""
import hashlib, json, posixpath, re, urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
LIVE = "https://cesarxdesign.com"
UA = ("Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 "
      "(KHTML, like Gecko) Chrome/128.0 Safari/537.36")  # Google Fonts serves woff2 only to modern browsers

# Things a page LOADS (as opposed to links it navigates to).
LOADS = [
    re.compile(r'''(<link\b[^>]*?\brel=["']?(?:stylesheet|preload|icon|modulepreload)["']?[^>]*?\bhref=["'])(https?://[^"']+)'''),
    re.compile(r'''(<link\b[^>]*?\bhref=["'])(https?://[^"']+)(?=["'][^>]*?\brel=["']?(?:stylesheet|preload|icon|modulepreload))'''),
    re.compile(r'''(<(?:script|img|source|video|audio|iframe)\b[^>]*?\bsrc=["'])(https?://[^"']+)'''),
    re.compile(r'''(url\(\s*["']?)(https?://[^"')\s]+)'''),
    re.compile(r'''(@import\s+["'])(https?://[^"']+)'''),
]
PRECONNECT = re.compile(r'''<link\b[^>]*\brel=["']?(?:preconnect|dns-prefetch)["']?[^>]*>\s*''')


def fetch(url):
    req = urllib.request.Request(url.replace("&amp;", "&"), headers={"User-Agent": UA})
    with urllib.request.urlopen(req, timeout=60) as r:
        return r.read(), r.headers.get_content_type()


def vendor(site: Path):
    """Download every external resource the pages load into site/_vendor/ and point at the copy.

    Links to other pages stay as they are: they are navigation, not part of this page."""
    cache = {}

    def local_name(url, ctype):
        ext = {"text/css": ".css", "font/woff2": ".woff2", "font/woff": ".woff", "font/ttf": ".ttf",
               "application/javascript": ".js", "text/javascript": ".js", "image/png": ".png",
               "image/jpeg": ".jpg", "image/svg+xml": ".svg", "image/webp": ".webp"}.get(ctype)
        tail = posixpath.basename(url.split("?")[0]) or "file"
        if ext and not tail.endswith(ext):
            tail += ext
        return f"_vendor/{hashlib.sha1(url.encode()).hexdigest()[:10]}-{tail}"

    def get(url):
        if url not in cache:
            data, ctype = fetch(url)
            name = local_name(url, ctype)
            if name.endswith(".css"):
                data = rewrite(data.decode(), name).encode()
            (site / name).parent.mkdir(parents=True, exist_ok=True)
            (site / name).write_bytes(data)
            cache[url] = name
        return cache[url]

    def rewrite(text, rel_to):
        for rx in LOADS:
            text = rx.sub(lambda m: m.group(1) + posixpath.relpath(get(m.group(2)), posixpath.dirname(rel_to) or "."), text)
        return PRECONNECT.sub("", text)

    for f in sorted(site.rglob("*")):
        if f.suffix in (".html", ".css") and "_vendor" not in f.parts:
            rel = f.relative_to(site).as_posix()
            text = f.read_text()
            new = rewrite(text, rel)
            if new != text:
                f.write_text(new)
    return len(cache)


def external_loads(site: Path):
    """Every external resource still loaded by a page under site/ (should be none)."""
    out = []
    for f in site.rglob("*"):
        if f.suffix in (".html", ".css"):
            text = f.read_text(errors="ignore")
            for rx in LOADS:
                out += [f"{f.relative_to(site)}: {m.group(2)}" for m in rx.finditer(text)]
    return out


def write_meta(dest: Path, meta: dict):
    (dest / "meta.json").write_text(json.dumps(meta, indent=2, ensure_ascii=False) + "\n")


def new_dest(project, vid):
    dest = ROOT / "versions" / project / vid
    if dest.exists():
        raise SystemExit(f"{dest.relative_to(ROOT)} already exists")
    return dest
