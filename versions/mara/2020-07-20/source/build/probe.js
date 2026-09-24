(() => {
  const r = {};
  const g = id => { const e = document.getElementById(id); const b = e.getBoundingClientRect(); return [b.left, b.top + scrollY, b.width]; };
  r.oct = g('g-oct'); r.xx = g('g-xx');
  // width probe: Roboto vs fallback
  const c = document.createElement('canvas').getContext('2d');
  r.fonts = [...document.fonts].map(f => f.family + ' ' + f.weight + ' ' + f.style + ' ' + f.status);
  return r;
})()
