#!/usr/bin/env python3
"""Prove every stored page is whole: everything it loads is inside its own folder, in git.

    python3 tools/check.py            exit 0 means every version stands on its own

Fails on: a file the page loads that comes from outside (http, //host), a local file that
is missing or sits outside the version's folder, a symlink, anything under versions/ that
git does not hold as committed. Links a reader clicks (other case studies, LinkedIn, mail)
are navigation, not part of the page, and are only counted.
"""
import posixpath, re, subprocess, sys
from pathlib import Path
from urllib.parse import unquote

ROOT = Path(__file__).resolve().parent.parent
EXTERNAL = re.compile(r"^(?:https?:)?//", re.I)
SCHEME = re.compile(r"^[a-z][a-z0-9+.-]*:", re.I)   # data:, mailto:, javascript: ...

# Every place HTML and CSS can pull in a file.
LOADS = [
    re.compile(r"""<(?:img|script|source|video|audio|iframe|embed|input|track)\b[^>]*?\ssrc=["']([^"']+)""", re.I),
    re.compile(r"""<link\b[^>]*?\shref=["']([^"']+)["'][^>]*>""", re.I),
    re.compile(r"""\s(?:poster|data|xlink:href)=["']([^"']+)""", re.I),
    re.compile(r"""<(?:image|use|feImage)\b[^>]*?\shref=["']([^"'#][^"']*)""", re.I),
    re.compile(r"""url\(\s*(?:&quot;|["'])?([^"')\s&]+(?:&(?!quot;)[^"')\s&]*)*)""", re.I),
    re.compile(r"""@import\s+["']([^"']+)""", re.I),
]
SRCSET = re.compile(r"""\s(?:srcset|imagesrcset)=["']([^"']+)""", re.I)
LINK_REL = re.compile(r"""\brel=["']?([\w\s-]+)""", re.I)
ANCHOR = re.compile(r"""<a\b[^>]*?\shref=["']([^"']+)""", re.I)
# Scripts can fetch too: any quoted http(s) URL to a file type that would be loaded.
SCRIPT_URL = re.compile(r"""["'`](https?://[^"'`\s]+\.(?:js|mjs|css|woff2?|ttf|otf|png|jpe?g|gif|webp|avif|svg|json|mp4|webm)(?:\?[^"'`\s]*)?)["'`]""", re.I)
SCRIPT = re.compile(r"<script\b[^>]*>(.*?)</script>", re.S | re.I)
IGNORE_LINK_RELS = {"preconnect", "dns-prefetch", "canonical", "alternate", "author", "license", "me"}


DATA_URL = re.compile(r'''url\(\s*(?:"data:[^"]*"|'data:[^']*'|&quot;data:.*?&quot;)\s*\)''', re.S)


def urls(text, is_css):
    text = DATA_URL.sub("", text)   # an embedded file is part of the page already
    out = []
    for rx in LOADS:
        for m in rx.finditer(text):
            if rx is LOADS[1]:
                rel = LINK_REL.search(m.group(0))
                if rel and set(rel.group(1).lower().split()) <= IGNORE_LINK_RELS:
                    continue
            out.append(m.group(1))
    for m in SRCSET.finditer(text):
        # Candidates are "url [descriptor]" separated by commas; a data: URL has a comma inside
        # but never whitespace, so read whitespace-delimited URLs rather than splitting on ",".
        out += [u.rstrip(",") for u in re.findall(r"(\S+)(?:\s+[\d.]+[wxh])?", m.group(1)) if u.rstrip(",")]
    if not is_css:
        for body in SCRIPT.findall(text):
            out += SCRIPT_URL.findall(body)
    return out


def main():
    problems, pages, files, links = [], 0, 0, 0
    tracked = set(subprocess.run(["git", "-C", str(ROOT), "ls-files", "versions"],
                                 capture_output=True, text=True, check=True).stdout.split("\n")) - {""}
    dirty = subprocess.run(["git", "-C", str(ROOT), "status", "--porcelain", "--ignored", "versions"],
                           capture_output=True, text=True, check=True).stdout.strip()
    if dirty:
        problems += [f"not committed as is: {l}" for l in dirty.split("\n")]

    for vdir in sorted(p for p in (ROOT / "versions").glob("*/*") if p.is_dir()):
        for f in sorted(vdir.rglob("*")):
            rel = f.relative_to(ROOT).as_posix()
            if f.is_symlink():
                problems.append(f"symlink: {rel}")
                continue
            if not f.is_file():
                continue
            files += 1
            if rel not in tracked:
                problems.append(f"not in git: {rel}")
            if f.suffix not in (".html", ".css") or "/source/" in "/" + f.relative_to(vdir).as_posix():
                continue
            pages += f.suffix == ".html"
            text = f.read_text(errors="ignore")
            links += sum(1 for u in ANCHOR.findall(text) if EXTERNAL.match(u))
            for u in urls(text, f.suffix == ".css"):
                u = u.replace("&amp;", "&")
                if EXTERNAL.match(u):
                    problems.append(f"loads from outside: {rel} -> {u}")
                    continue
                if SCHEME.match(u) or u.startswith(("#", "%23", "{{")):
                    continue
                path = unquote(u.split("#")[0].split("?")[0])
                if not path:
                    continue
                target = (f.parent / path).resolve() if not path.startswith("/") else None
                if target is None:
                    problems.append(f"site-root path, breaks outside the folio: {rel} -> {u}")
                elif vdir.resolve() not in target.parents:
                    problems.append(f"reaches outside its version: {rel} -> {u}")
                elif not target.is_file():
                    problems.append(f"missing: {rel} -> {u}")

    for p in problems:
        print("FAIL", p)
    n = len([p for p in (ROOT / "versions").glob("*/*") if p.is_dir()])
    print(f"{n} versions, {pages} pages, {files} files, {links} outbound links (navigation, fine)")
    print("OK: every page stands on its own" if not problems else f"{len(problems)} problems")
    sys.exit(1 if problems else 0)


if __name__ == "__main__":
    main()
