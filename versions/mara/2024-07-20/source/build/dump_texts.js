const frame = await figma.getNodeByIdAsync('98:75481');
let p = frame; while (p.type !== 'PAGE') p = p.parent;
await figma.setCurrentPageAsync(p);
const r2 = v => typeof v === 'number' ? Math.round(v*1000)/1000 : v;
const hex = ps => (ps===figma.mixed?'MIXED':(ps||[]).filter(x=>x.visible!==false).map(x => x.type==='SOLID' ? '#'+[x.color.r,x.color.g,x.color.b].map(c=>Math.round(c*255).toString(16).padStart(2,'0')).join('')+(x.opacity!==1?'@'+r2(x.opacity):'')+(x.blendMode&&x.blendMode!=='NORMAL'?'~'+x.blendMode:'') : x.type).join(','));
const out = [];
for (const id of IDS) {
  const n = await figma.getNodeByIdAsync(id);
  const segs = n.getStyledTextSegments(['fontName','fontSize','fills','lineHeight','letterSpacing','textCase','textDecoration','openTypeFeatures','listOptions','indentation']).map(s => [s.start, s.end, s.fontName.family+'/'+s.fontName.style, s.fontSize, s.lineHeight.unit==='AUTO'?'AUTO':(s.lineHeight.unit==='PIXELS'?s.lineHeight.value+'px':s.lineHeight.value+'%'), s.letterSpacing.unit==='PIXELS'?r2(s.letterSpacing.value)+'px':r2(s.letterSpacing.value)+'%', s.textCase, s.textDecoration, hex(s.fills), JSON.stringify(s.openTypeFeatures||{}), s.listOptions&&s.listOptions.type!=='NONE'?s.listOptions.type:'', s.indentation||0]);
  const sec = frame.children.find(s => { const b=s.absoluteBoundingBox, a=n.absoluteBoundingBox; return a.y>=b.y-200 && a.y < b.y+b.height; });
  const oy = sec.absoluteBoundingBox.y, ox = frame.absoluteBoundingBox.x;
  const a = n.absoluteBoundingBox, rb = n.absoluteRenderBounds;
  out.push({id, sec: sec.name.slice(0,2), ah:n.textAlignHorizontal, av:n.textAlignVertical, ar:n.textAutoResize, op:r2(n.opacity), bm:n.blendMode, ps:n.paragraphSpacing, eff:(n.effects||[]).length, strokes:hex(n.strokes), rot:r2(n.rotation),
    box:[r2(a.x-ox), r2(a.y-oy), r2(a.width), r2(a.height)], rb: rb?[r2(rb.x-ox), r2(rb.y-oy), r2(rb.width), r2(rb.height)]:null, par: n.parent.type+':'+n.parent.name+':'+(n.parent.layoutMode||'')+':op'+r2(n.parent.opacity)+':'+n.parent.blendMode, chars:n.characters, segs});
}
return out;
