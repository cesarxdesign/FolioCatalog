(()=>{
 const out=[]; const secs=[...document.querySelectorAll('section')];
 const els=[...document.querySelectorAll('main p, main h2, main h3, main span.a, main dd, main dt, main li, main div.kicker, main div.analysis > p')];
 for(const e of els){
   if(e.closest('.four')) continue;
   const sec=e.closest('section'); const si=secs.indexOf(sec); const st=sec.getBoundingClientRect().top+scrollY;
   // line boxes via range over text nodes
   const r=document.createRange(); r.selectNodeContents(e);
   const rects=[...r.getClientRects()].filter(q=>q.width>0);
   const lines={};
   for(const q of rects){const k=Math.round(q.top+scrollY-st); const L=lines[k]||(lines[k]={l:1e9,r:-1e9,b:0}); L.l=Math.min(L.l,q.left); L.r=Math.max(L.r,q.right); L.b=Math.max(L.b,q.bottom+scrollY-st);}
   const ks=Object.keys(lines).map(Number).sort((a,b)=>a-b);
   // merge rects within 4px
   const merged=[]; for(const k of ks){const L=lines[k]; const m=merged[merged.length-1]; if(m && k-m.t<4){m.l=Math.min(m.l,L.l);m.r=Math.max(m.r,L.r);m.b=Math.max(m.b,L.b);} else merged.push({t:k,l:L.l,r:L.r,b:L.b});}
   out.push({sec:si+1, txt:e.textContent.slice(0,30), lines:merged.map(m=>[Math.round(m.l),m.t,Math.round(m.r),Math.round(m.b)])});
 }
 return out;})()
