#!/usr/bin/env python3
"""Rebuild catalog.json and index.html from versions/*/*/meta.json."""
import hashlib, json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent


def when(m):
    """Sort key: when the version first existed in public, or was made."""
    return m.get("shipped") or m.get("made") or m["id"][:10]


def main():
    metas = [json.loads(p.read_text()) for p in sorted(ROOT.glob("versions/*/*/meta.json"))]
    for m in metas:
        m["path"] = f"versions/{m['project']}/{m['id']}/{m['page']}"
        # A changed page gets a new address, so no browser shows a cached copy of the old one.
        m["path"] += "?v=" + hashlib.sha1((ROOT / m["path"]).read_bytes()).hexdigest()[:8]
    # Projects A-Z, versions oldest first, so side by side reads left to right in time.
    metas.sort(key=lambda m: (m["project"], when(m), m["id"]))
    (ROOT / "catalog.json").write_text(json.dumps(metas, indent=2, ensure_ascii=False) + "\n")
    keep = ("project", "id", "name", "path", "width", "shipped", "until", "made")
    data = json.dumps([{k: m.get(k) for k in keep} for m in metas], ensure_ascii=False)
    (ROOT / "index.html").write_text(PAGE.replace("/*DATA*/[]", data))
    print(f"index.html: {len(metas)} versions")


PAGE = """<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<meta name="robots" content="noindex">
<title>FolioCatalog</title>
<style>
:root{
  --bg:#EDEFF2; --panel:#FFFFFF; --ink:#16202B; --muted:#5E6C7A; --line:#D3DAE2; --accent:#C9204E;
  --sans:system-ui,-apple-system,'Segoe UI',sans-serif;
}
@media (prefers-color-scheme:dark){:root:not([data-theme="light"]){
  --bg:#2C2C2C; --panel:#1F1F1F; --ink:#E8EAED; --muted:#969CA4; --line:#3C3C3C; --accent:#FF5081;}}
:root[data-theme="dark"]{
  --bg:#2C2C2C; --panel:#1F1F1F; --ink:#E8EAED; --muted:#969CA4; --line:#3C3C3C; --accent:#FF5081;}
*{box-sizing:border-box}
html,body{height:100%;overflow:hidden}
body{margin:0;background:var(--bg);color:var(--ink);font-family:var(--sans);display:flex;flex-direction:column}
header{flex:none;display:flex;align-items:center;gap:14px;padding:8px 16px;white-space:nowrap;overflow:hidden;
       background:var(--panel);border-bottom:1px solid var(--line)}
h1{font-size:14px;font-weight:600;margin:0 4px 0 0;letter-spacing:-.01em}
label{display:flex;align-items:center;gap:6px;font-size:12px;color:var(--muted)}
select,button{font:inherit;font-size:13px;color:var(--ink);background:var(--bg);border:1px solid var(--line);border-radius:6px;cursor:pointer}
select{padding:4px 24px 4px 8px;appearance:none;max-width:260px;
       background-image:linear-gradient(45deg,transparent 50%,var(--muted) 50%),linear-gradient(135deg,var(--muted) 50%,transparent 50%);
       background-position:calc(100% - 12px) 55%,calc(100% - 8px) 55%;background-size:4px 4px;background-repeat:no-repeat}
.step{display:flex;align-items:center;gap:6px;font-size:12px;color:var(--muted);font-variant-numeric:tabular-nums}
.step[hidden]{display:none}
.step button{width:28px;height:26px;padding:0;font-size:15px;line-height:1}
.step button:disabled{opacity:.35;cursor:default}
#theme{margin-left:auto;display:flex;align-items:center;gap:6px;padding:4px 10px;font-size:12px}
#theme svg{width:14px;height:14px}
select:focus-visible,button:focus-visible,a:focus-visible{outline:2px solid var(--accent);outline-offset:2px}
main{flex:1;min-height:0;display:flex;gap:10px;padding:10px 16px 0}
.pane{flex:1 1 0;min-width:0;display:flex;flex-direction:column;background:var(--panel);border:1px solid var(--line);
      border-bottom:0;border-radius:8px 8px 0 0;overflow:hidden}
.cap{flex:none;padding:7px 10px;border-bottom:1px solid var(--line);font-size:12px;font-weight:600;
     white-space:nowrap;overflow:hidden;text-overflow:ellipsis}
.view{flex:1;min-height:0;position:relative;overflow:hidden;background:#fff}
.view iframe{position:absolute;top:0;border:0;transform-origin:0 0;background:#fff}
/* A pane is a picture of the page: nothing inside can be clicked, hovered or focused.
   The shield takes every pointer event and passes only the wheel on, as scrolling. */
.shield{position:absolute;inset:0;z-index:1}
.empty{margin:auto;color:var(--muted);font-size:14px}
</style>
</head>
<body>
<header>
  <h1>FolioCatalog</h1>
  <label>Project <select id="project"></select></label>
  <label>Version <select id="version"></select></label>
  <label>Compare <select id="count"></select></label>
  <div class="step" id="step" hidden>
    <button type="button" id="prev" aria-label="Show earlier">&lsaquo;</button>
    <button type="button" id="next" aria-label="Show later">&rsaquo;</button>
    <span id="range"></span>
  </div>
  <button type="button" id="theme" aria-label="Dark mode" aria-pressed="false" title="Light or dark, for every page shown that has both"></button>
</header>
<main id="panes"></main>
<script>
const ALL = /*DATA*/[];
const MIN_PANE = 360;               // narrower than this and a pane stops being readable
const $ = id => document.getElementById(id);
const el = (tag, props = {}, ...kids) => { const e = Object.assign(document.createElement(tag), props); e.append(...kids); return e; };
const projects = [...new Set(ALL.map(v => v.project))];
const cap = s => s.charAt(0).toUpperCase() + s.slice(1);
const state = {project: projects[0], id: null, n: 1, off: 0};

// One switch for the viewer and every page shown. Folio pages keep their theme on <html>
// (and read localStorage "folio0" when they load); Claude Design pages on their root element.
// Pages with a single look have no data-theme, so they are left as they are.
const store = {get: k => { try { return localStorage.getItem(k); } catch (e) { return null; } },
               set: (k, v) => { try { localStorage.setItem(k, v); } catch (e) {} }};
let theme = store.get('fc-theme') || (matchMedia('(prefers-color-scheme: dark)').matches ? 'dark' : 'light');
const ICON = {light: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" aria-hidden="true"><circle cx="12" cy="12" r="4.5"/><path d="M12 2v2.5M12 19.5V22M2 12h2.5M19.5 12H22M4.9 4.9l1.8 1.8M17.3 17.3l1.8 1.8M19.1 4.9l-1.8 1.8M6.7 17.3l-1.8 1.8"/></svg>',
              dark: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linejoin="round" aria-hidden="true"><path d="M20 14.5A8 8 0 0 1 9.5 4a8 8 0 1 0 10.5 10.5z"/></svg>'};
function themeFrame(f) {
  try { f.contentDocument.querySelectorAll('[data-theme]').forEach(e => e.setAttribute('data-theme', theme)); } catch (e) {}
}
function applyTheme() {
  document.documentElement.dataset.theme = theme;
  store.set('fc-theme', theme);
  store.set('folio0', theme);
  $('theme').innerHTML = ICON[theme] + (theme === 'dark' ? 'Dark' : 'Light');
  $('theme').setAttribute('aria-pressed', theme === 'dark');
  document.querySelectorAll('.view iframe').forEach(themeFrame);
}

const label = v => v.id.slice(0, 10) + (v.name ? ' · ' + v.name : '');
const list = () => ALL.filter(v => v.project === state.project);

function readHash() {
  const [p, id, n, off] = decodeURIComponent(location.hash.slice(1)).split('/');
  state.project = projects.includes(p) ? p : projects[0];
  const vs = list();
  state.id = vs.some(v => v.id === id) ? id : vs[vs.length - 1].id;
  state.n = Math.min(6, Math.max(1, +n || 1));
  state.off = Math.max(0, +off || 0);
}

function window_() {
  // The n versions being compared: the chosen one and those after it, pulled back at the end.
  const vs = list(), i = vs.findIndex(v => v.id === state.id);
  const n = Math.min(state.n, vs.length), start = Math.min(i, vs.length - n);
  return vs.slice(start, start + n);
}

function render() {
  const vs = list();
  $('project').value = state.project;
  $('version').replaceChildren(...vs.map(v => el('option', {value: v.id, textContent: label(v)})));
  $('version').value = state.id;
  $('count').value = state.n;

  const set = window_();
  const room = $('panes').clientWidth + 10;
  const fit = Math.max(1, Math.min(set.length, Math.floor(room / (MIN_PANE + 10))));
  state.off = Math.min(state.off, set.length - fit);
  const shown = set.slice(state.off, state.off + fit);
  $('step').hidden = fit >= set.length;
  $('prev').disabled = state.off === 0;
  $('next').disabled = state.off + fit >= set.length;
  $('range').textContent = `${state.off + 1}–${state.off + fit} of ${set.length}`;

  const have = [...$('panes').children].map(p => p.dataset.path).join('|');
  if (have !== shown.map(v => v.path).join('|')) {
    $('panes').replaceChildren(...shown.map(v => {
      const frame = el('iframe', {src: v.path, title: label(v), loading: 'eager', tabIndex: -1, inert: true});
      frame.addEventListener('load', () => themeFrame(frame));
      const shield = el('div', {className: 'shield'});
      shield.addEventListener('wheel', e => {
        e.preventDefault();
        const px = e.deltaMode === 1 ? 16 : e.deltaMode === 2 ? shield.clientHeight : 1;
        try { frame.contentWindow.scrollBy(0, e.deltaY * px / +pane.dataset.scale); } catch (err) {}
      }, {passive: false});
      const pane = el('section', {className: 'pane'},
        el('div', {className: 'cap', textContent: label(v)}),
        el('div', {className: 'view'}, frame, shield));
      pane.dataset.path = v.path;
      pane.dataset.width = v.width || 1440;
      return pane;
    }));
  }
  fitFrames();
  const hash = `#${state.project}/${state.id}/${state.n}/${state.off}`;
  if (location.hash !== hash) history.replaceState(null, '', hash);
}

function fitFrames() {
  // Each page is drawn at the width it was designed for and scaled down to its pane.
  for (const pane of $('panes').children) {
    const view = pane.querySelector('.view'), f = view.querySelector('iframe');
    const w = +pane.dataset.width, pw = view.clientWidth, s = Math.min(1, pw / w);
    f.style.width = w + 'px';
    f.style.height = view.clientHeight / s + 'px';
    f.style.left = Math.max(0, (pw - w * s) / 2) + 'px';
    f.style.transform = `scale(${s})`;
    pane.dataset.scale = s;
  }
}

if (!ALL.length) {
  $('panes').append(el('p', {className: 'empty', textContent: 'Nothing stored yet.'}));
  document.querySelectorAll('header label').forEach(e => e.hidden = true);
} else {
  projects.forEach(p => $('project').append(el('option', {value: p, textContent: cap(p)})));
  for (let i = 1; i <= 6; i++) $('count').append(el('option', {value: i, textContent: i === 1 ? '1 page' : `${i} side by side`}));
  $('project').onchange = e => { state.project = e.target.value; const vs = list(); state.id = vs[vs.length - 1].id; state.off = 0; render(); };
  $('version').onchange = e => { state.id = e.target.value; state.off = 0; render(); };
  $('count').onchange = e => { state.n = +e.target.value; state.off = 0; render(); };
  $('prev').onclick = () => { state.off--; render(); };
  $('next').onclick = () => { state.off++; render(); };
  window.onhashchange = () => { readHash(); render(); };
  let t; window.onresize = () => { clearTimeout(t); t = setTimeout(render, 60); };
  $('theme').onclick = () => { theme = theme === 'dark' ? 'light' : 'dark'; applyTheme(); };
  applyTheme();
  readHash();
  render();
}
</script>
</body>
</html>
"""

if __name__ == "__main__":
    main()
