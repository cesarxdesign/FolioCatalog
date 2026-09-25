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
#lock,#theme{display:flex;align-items:center;gap:6px;padding:4px 10px;font-size:12px}
#lock{margin-left:auto}
#lock[aria-pressed="true"]{border-color:var(--accent);color:var(--accent)}
#lock svg,#theme svg{width:14px;height:14px}
select:focus-visible,button:focus-visible,a:focus-visible{outline:2px solid var(--accent);outline-offset:2px}
main{flex:1;min-height:0;display:flex;gap:10px;padding:10px 16px 0}
.pane{flex:1 1 0;min-width:0;display:flex;flex-direction:column;background:var(--panel);border:1px solid var(--line);
      border-bottom:0;border-radius:8px 8px 0 0;overflow:hidden}
.cap{flex:none;padding:5px 6px;border-bottom:1px solid var(--line)}
.cap select{width:100%;max-width:none;font-size:12px;font-weight:600;text-overflow:ellipsis}
.view{flex:1;min-height:0;position:relative;overflow:hidden;background:#fff}
.view iframe{position:absolute;top:0;border:0;transform-origin:0 0;background:#fff}

.empty{margin:auto;color:var(--muted);font-size:14px}
</style>
</head>
<body>
<header>
  <h1>FolioCatalog</h1>
  <label>Project <select id="project"></select></label>
  <label>Show <select id="count"></select></label>
  <div class="step" id="step" hidden>
    <button type="button" id="prev" aria-label="Show earlier">&lsaquo;</button>
    <button type="button" id="next" aria-label="Show later">&rsaquo;</button>
    <span id="range"></span>
  </div>
  <button type="button" id="lock" aria-pressed="false" title="Scroll every pane together"></button>
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
// project is one project or 'all'. picks holds what each pane shows, as "project:id", left to right.
const state = {project: projects[0], n: 1, off: 0, picks: []};

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
// A pane shows a page, it does not run it: text selects and the page scrolls, but no link,
// button or menu does anything. Done here, not in the stored pages, so a page taken out of
// versions/ still works in full.
const CLICKABLE = 'a,button,summary,select,label,input,textarea,[role=button],[role=link],[onclick],[tabindex]';
function unlink(root) {
  root.querySelectorAll('a[href]').forEach(a => { a.dataset.href = a.getAttribute('href'); a.removeAttribute('href'); });
}
function stillFrame(f) {
  try {
    const d = f.contentDocument;
    if (!d || !d.documentElement) return;
    unlink(d);
    if (d.__still) return;          // listeners once per document; unlink runs every time
    d.__still = true;
    new MutationObserver(() => unlink(d)).observe(d.documentElement, {subtree: true, childList: true, attributes: true, attributeFilter: ['href']});
    d.querySelectorAll('form').forEach(form => form.addEventListener('submit', e => e.preventDefault(), true));
    const stop = e => { if (e.target.closest && e.target.closest(CLICKABLE)) { e.preventDefault(); e.stopImmediatePropagation(); } };
    for (const t of ['click', 'auxclick', 'dblclick', 'pointerdown', 'mousedown', 'touchstart']) d.addEventListener(t, stop, true);
    d.addEventListener('keydown', e => { if ((e.key === 'Enter' || e.key === ' ') && e.target.closest && e.target.closest(CLICKABLE)) { e.preventDefault(); e.stopImmediatePropagation(); } }, true);
    const st = d.createElement('style');
    // The viewer draws each page at its design width and scales it itself, so a page's own
    // shrink-to-fit zoom (the Cable and Penfold Figma pages) is switched off here.
    st.textContent = `${CLICKABLE}{cursor:text !important} html{zoom:1 !important}`;
    (d.head || d.documentElement).append(st);
  } catch (e) {}
}

// Links die while the page is still being read in: the watcher attaches as soon as the new
// document exists, and from then on every link is stripped the moment it is parsed.
function watchFrame(f) {
  const t = setInterval(() => {
    try {
      const d = f.contentDocument;
      if (d && d.documentElement && d.location.href !== 'about:blank') { stillFrame(f); clearInterval(t); }
    } catch (e) { clearInterval(t); }
  }, 10);
  setTimeout(() => clearInterval(t), 20000);
}

// Scroll lock. Panes move by the same distance on screen, whatever each page's scale. So every
// page can travel as far as the longest one, shorter pages get a blank "ghost" space after
// their last line while the lock is on. Like the link-killing, this lives in the viewer only.
let locked = store.get('fc-lock') === '1';
const LOCK = {on: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" aria-hidden="true"><rect x="5" y="11" width="14" height="10" rx="2"/><path d="M8 11V7a4 4 0 0 1 8 0v4"/></svg>',
              off: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" aria-hidden="true"><rect x="5" y="11" width="14" height="10" rx="2"/><path d="M8 11V7a4 4 0 0 1 7.5-2"/></svg>'};
const frames = () => [...document.querySelectorAll('.view iframe')];
const scaleOf = f => Math.min(1, f.parentElement.clientWidth / +f.closest('.pane').dataset.width);
const docOf = f => { try { const d = f.contentDocument; return d && d.body && d.location.href !== 'about:blank' ? d : null; } catch (e) { return null; } };

function ghostOf(d, make) {
  let g = d.getElementById('fc-ghost');
  if (!g && make) {
    g = d.createElement('div');
    g.id = 'fc-ghost';
    g.setAttribute('aria-hidden', 'true');
    d.documentElement.append(g);
  }
  return g;
}

function equalize() {
  // Page heights on screen (design px times scale), without any ghost already added.
  frames().forEach(hookScroll);
  const fs = frames().map(f => ({f, d: docOf(f), s: scaleOf(f)})).filter(x => x.d);
  for (const x of fs) { const g = ghostOf(x.d); x.h = x.d.documentElement.scrollHeight - (g ? g.offsetHeight : 0); }
  const top = Math.max(0, ...fs.map(x => x.h * x.s));
  for (const x of fs) {
    const need = locked ? (top - x.h * x.s) / x.s : 0;
    const g = ghostOf(x.d, need >= 1);
    if (!g) continue;
    if (need < 1) { g.remove(); continue; }
    // Placed at the page's own end in document coordinates, so absolutely positioned layouts
    // (the Figma builds) and in-flow ones end at the same place.
    g.style.cssText = `position:absolute;left:0;right:0;top:${x.h}px;height:${need}px;margin:0;padding:${24 / x.s}px 0 0;box-sizing:border-box;` +
      `text-align:center;font:${11 / x.s}px/1.4 system-ui,sans-serif;letter-spacing:.04em;text-transform:uppercase;` +
      `color:#9AA3AD;background:repeating-linear-gradient(135deg,rgba(128,128,128,.07) 0 ${8 / x.s}px,transparent 0 ${16 / x.s}px);pointer-events:none`;
    g.textContent = 'End of page';
  }
}

function follow(from) {
  // Move every other pane to the same on-screen distance as the one being scrolled.
  const px = from.contentWindow.scrollY * scaleOf(from);
  for (const f of frames()) {
    if (f === from) continue;
    try {
      const w = f.contentWindow, y = px / scaleOf(f);
      if (Math.abs(w.scrollY - y) < 1) continue;
      w.__fcQuiet = performance.now() + 120;   // its own scroll event is ours, not the user's
      w.scrollTo({top: y, behavior: 'instant'});
    } catch (e) {}
  }
}

function hookScroll(f) {
  // On the loaded document, never the blank one an iframe starts with (the browser can keep
  // that window object for the real page, and a flag on it would claim a listener that is gone).
  const d = docOf(f);
  if (!d || d.__fcHooked) return;
  d.__fcHooked = true;
  d.addEventListener('scroll', () => {
    const w = d.defaultView;
    if (!locked || !w || performance.now() < (w.__fcQuiet || 0)) return;
    follow(f);
  }, {passive: true});
}

function joinIn(f) {
  // A pane that (re)loads while locked starts where the others are.
  hookScroll(f);
  if (!locked) return;
  equalize();
  const other = frames().find(g => g !== f && docOf(g));
  if (other) follow(other);
}

function applyLock() {
  store.set('fc-lock', locked ? '1' : '0');
  $('lock').innerHTML = LOCK[locked ? 'on' : 'off'] + 'Scroll lock';
  $('lock').setAttribute('aria-pressed', locked);
  equalize();
  const first = frames().find(docOf);
  if (locked && first) follow(first);
}
// Pages settle as images and fonts load; keep the ghosts right while locked.
setInterval(() => { if (locked) equalize(); }, 1500);

function applyTheme() {
  document.documentElement.dataset.theme = theme;
  store.set('fc-theme', theme);
  store.set('folio0', theme);
  $('theme').innerHTML = ICON[theme] + (theme === 'dark' ? 'Dark' : 'Light');
  $('theme').setAttribute('aria-pressed', theme === 'dark');
  document.querySelectorAll('.view iframe').forEach(themeFrame);
}

const key = v => v.project + ':' + v.id;
const byKey = Object.fromEntries(ALL.map(v => [key(v), v]));
const label = v => (state.project === 'all' ? cap(v.project) + ' · ' : '') + v.id.slice(0, 10) + (v.name ? ' · ' + v.name : '');
const pool = () => state.project === 'all' ? ALL : ALL.filter(v => v.project === state.project);

function defaults() {
  // One project: its latest n versions, oldest on the left. All: each project's live page, A-Z.
  const vs = pool();
  if (state.project !== 'all') return vs.slice(-state.n).map(key);
  // A project's face is the page live on the folio now, or its newest if none is.
  return projects.map(p => { const vs = ALL.filter(v => v.project === p), live = vs.filter(v => v.shipped && !v.until);
                             return key((live.length ? live : vs).pop()); });
}

function fill() {
  // Keep what each pane shows; drop what no longer belongs; add the next unused version to new panes.
  const vs = pool(), n = Math.min(state.n, vs.length);
  let picks = state.picks.filter(k => byKey[k] && vs.includes(byKey[k]));
  if (!picks.length) picks = defaults();
  picks = picks.slice(0, n);
  // New panes take the defaults not yet shown first (under All: the next project's latest).
  for (const k of defaults()) if (picks.length < n && !picks.includes(k)) picks.push(k);
  let i = vs.indexOf(byKey[picks[picks.length - 1]]);
  for (let tries = 0; picks.length < n && tries < vs.length; tries++) {
    i = (i + 1) % vs.length;
    if (!picks.includes(key(vs[i]))) picks.push(key(vs[i]));
  }
  state.picks = picks;
}

function readHash() {
  // #project/n/off/project:id,project:id,...   (older links, #project/id/n/off, still open)
  const [p, a, b, c] = decodeURIComponent(location.hash.slice(1)).split('/');
  state.project = p === 'all' || projects.includes(p) ? p : projects[0];
  if (a && isNaN(+a)) {
    state.n = Math.min(6, Math.max(1, +b || 1));
    const vs = pool(), i = Math.max(0, vs.findIndex(v => v.id === a)), start = Math.max(0, Math.min(i, vs.length - state.n));
    state.picks = vs.slice(start, start + state.n).map(key);
    state.off = Math.max(0, +c || 0);
  } else {
    state.n = Math.min(6, Math.max(1, +a || 1));
    state.off = Math.max(0, +b || 0);
    state.picks = (c || '').split(',').filter(k => byKey[k]);
  }
  fill();
}

function pickerFor(i) {
  // The pane's caption: choose what this pane shows. Under All, grouped by project.
  const s = el('select', {'aria-label': `Pane ${i + 1}`});
  const opt = v => el('option', {value: key(v), textContent: label(v)});
  if (state.project === 'all') {
    for (const p of projects) s.append(el('optgroup', {label: cap(p)}, ...ALL.filter(v => v.project === p).map(opt)));
  } else s.append(...pool().map(opt));
  s.value = state.picks[i];
  s.onchange = () => { state.picks[i] = s.value; render(); };
  return s;
}

function render() {
  $('project').value = state.project;
  fill();
  $('count').value = state.n;

  const set = state.picks;
  const room = $('panes').clientWidth + 10;
  const fit = Math.max(1, Math.min(set.length, Math.floor(room / (MIN_PANE + 10))));
  state.off = Math.max(0, Math.min(state.off, set.length - fit));
  const idx = [...Array(fit).keys()].map(j => state.off + j);
  $('step').hidden = fit >= set.length;
  $('prev').disabled = state.off === 0;
  $('next').disabled = state.off + fit >= set.length;
  $('range').textContent = `${state.off + 1}–${state.off + fit} of ${set.length}`;

  // Reuse a pane whose page is unchanged, so picking in one pane doesn't reload the others.
  const old = {};
  for (const p of $('panes').children) (old[p.dataset.path] = old[p.dataset.path] || []).push(p);
  const panes = idx.map(i => {
    const v = byKey[set[i]];
    let pane = (old[v.path] || []).shift();
    if (!pane) {
      // #1x: the Figma-built pages shrink themselves to a 1280 column unless told otherwise.
      const frame = el('iframe', {src: v.path + '#1x', title: v.project + ' ' + v.id, loading: 'eager'});
      frame.addEventListener('load', () => { themeFrame(frame); stillFrame(frame); joinIn(frame); });
      watchFrame(frame);
      pane = el('section', {className: 'pane'}, el('div', {className: 'cap'}), el('div', {className: 'view'}, frame));
      pane.dataset.path = v.path;
      pane.dataset.width = v.width || 1440;
    }
    pane.querySelector('.cap').replaceChildren(pickerFor(i));
    return pane;
  });
  const same = panes.length === $('panes').children.length && panes.every((p, j) => $('panes').children[j] === p);
  if (!same) $('panes').replaceChildren(...panes);
  fitFrames();
  if (locked) equalize();
  const hash = `#${state.project}/${state.n}/${state.off}/${set.join(',')}`;
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
  }
}

if (!ALL.length) {
  $('panes').append(el('p', {className: 'empty', textContent: 'Nothing stored yet.'}));
  document.querySelectorAll('header label').forEach(e => e.hidden = true);
} else {
  $('project').append(el('option', {value: 'all', textContent: 'All projects'}));
  projects.forEach(p => $('project').append(el('option', {value: p, textContent: cap(p)})));
  for (let i = 1; i <= 6; i++) $('count').append(el('option', {value: i, textContent: i === 1 ? '1 page' : `${i} side by side`}));
  $('project').onchange = e => { state.project = e.target.value; state.picks = []; state.off = 0; render(); };
  $('count').onchange = e => { state.n = +e.target.value; render(); };
  $('prev').onclick = () => { state.off--; render(); };
  $('next').onclick = () => { state.off++; render(); };
  window.onhashchange = () => { readHash(); render(); };
  let t; window.onresize = () => { clearTimeout(t); t = setTimeout(render, 60); };
  $('theme').onclick = () => { theme = theme === 'dark' ? 'light' : 'dark'; applyTheme(); };
  $('lock').onclick = () => { locked = !locked; applyLock(); };
  applyTheme();
  applyLock();
  readHash();
  render();
}
</script>
</body>
</html>
"""

if __name__ == "__main__":
    main()
