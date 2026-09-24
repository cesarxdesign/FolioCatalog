(async () => { await document.fonts.ready;
 const faces=[...document.fonts].map(f=>`${f.family} ${f.style} ${f.weight} ${f.status}`);
 // width probe: same string in the face vs a guaranteed fallback
 const probe=(fam,w,st)=>{const s=document.createElement('span');s.style.cssText=`font:${st} ${w} 40px ${fam};position:absolute;white-space:nowrap`;s.textContent='Wishlist x capacity 0123 fi';document.body.appendChild(s);const x=s.getBoundingClientRect().width;s.remove();return x;};
 const P=[["'Roboto'",300,'normal'],["'Roboto'",800,'normal'],["'Roboto'",300,'italic'],["'Roboto Mono'",300,'normal'],["'Roboto Mono'",300,'italic'],["'IBM Plex Mono'",500,'normal']];
 return {faces, probes:P.map(([f,w,st])=>[f,w,st,probe(f,w,st).toFixed(2),probe('serif',w,st).toFixed(2),probe('monospace',w,st).toFixed(2)])};
})()
