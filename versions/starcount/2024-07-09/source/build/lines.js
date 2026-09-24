(() => {
  const out = [];
  document.querySelectorAll('.lt').forEach((el, i) => {
    const r = document.createRange(); r.selectNodeContents(el);
    // merge fragment rects into lines (same top)
    const lines = [];
    for (const q of r.getClientRects()) {
      if (q.width < 0.5) continue;
      const L = lines.find(l => Math.abs(l.t - q.top) < 3 && Math.abs(l.b - q.bottom) < 12);
      if (L) { L.l = Math.min(L.l, q.left); L.r = Math.max(L.r, q.right); L.t=Math.min(L.t,q.top); L.b=Math.max(L.b,q.bottom);} else lines.push({l:q.left, r:q.right, t:q.top, b:q.bottom});
    }
    const b = el.getBoundingClientRect();
    out.push({i, txt: el.textContent.slice(0, 40), box: [b.left, b.top + scrollY, b.width, b.height], lines: lines.map(l => [l.l, l.t + scrollY, l.r - l.l, l.b - l.t])});
  });
  return out;
})()
