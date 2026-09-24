import numpy as np, subprocess, os, itertools, time
from PIL import Image
D=os.path.dirname(os.path.abspath(__file__))
S=np.asarray(Image.open(D+'/../page.png').convert('L')).astype(int)
def box(a):
    m=a>138; ys=np.where(m.any(1))[0]; xs=np.where(m.any(0))[0]
    ink=np.clip(a-6,0,None).sum()/249
    return xs.min(),xs.max()+1,ys.min(),ys.max()+1,ink
src={'a':box(S[940:1010,1170:1340]),'b':box(S[940:1010,1340:1362]),'c':box(S[940:1010,1364:1560])}
# convert to css relative to hero (x from 1068, y from 70)
srcabs={'a':(1170,940),'b':(1340,940),'c':(1364,940)}
for k,v in src.items(): print(k,'src w %.1f h %.1f ink %.0f'%((v[1]-v[0])/2,(v[3]-v[2])/2,v[4]))
cands=[]
for s in np.arange(15.4,17.01,0.2):
    for l in (-1.3,-1.2,-1.1,-1.0,-0.9):
        cands.append(('a',f"font-family:WS;font-size:{s:.2f}px;letter-spacing:{l}px",'STARCOUNT',(s,l)))
for w in ('P5','P6'):
    for s in np.arange(15.0,16.61,0.2):
        for l in (-.2,-.1,0,.1,.2):
            cands.append(('c',f"font-family:{w};font-size:{s:.2f}px;letter-spacing:{l}px",'AUDIENCES',(w,s,l)))
for w in ('P1','P3'):
    for s in np.arange(19,24.1,0.5):
        cands.append(('b',f"font-family:{w};font-size:{s:.2f}px",'/',(w,s)))
H=50
html='''<html><head><style>
@font-face{font-family:WS;src:url(../../site/fonts/bodoni72-book-starcount.woff2)}
@font-face{font-family:P5;src:url(../../site/fonts/plexsans-500-wordmark.woff2)}
@font-face{font-family:P6;src:url(../../site/fonts/plexsans-600-wordmark.woff2)}
@font-face{font-family:P1;src:url(../../site/fonts/plexsans-100-wordmark.woff2)}
@font-face{font-family:P3;src:url(../../site/fonts/plexsans-300-wordmark.woff2)}
body{margin:0;background:#060606;-webkit-font-smoothing:antialiased}
div{position:absolute;left:20px;white-space:nowrap;color:#F6F6F6;line-height:1}
</style></head><body>'''
for i,(k,st,t,p) in enumerate(cands):
    html+=f'<div style="top:{10+i*H}px;{st}">{t}</div>'
html+='</body></html>'
open(D+'/cand.html','w').write(html)
out=D+'/cand.png'
if os.path.exists(out): os.remove(out)
pr=subprocess.Popen(['/Applications/Google Chrome.app/Contents/MacOS/Google Chrome','--headless=new','--disable-gpu','--hide-scrollbars','--force-device-scale-factor=2',f'--window-size=400,{len(cands)*H+20}','--user-data-dir=/private/tmp/claude-501/-Users-cgair-Claude/a92997a1-610b-4dee-9a2e-79d3d6d097d6/scratchpad/aud-chrome','--screenshot='+out,'file://'+D+'/cand.html'],stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL)
for _ in range(60):
    time.sleep(1)
    if os.path.exists(out) and os.path.getsize(out)>0: time.sleep(1); break
pr.kill(); subprocess.run(['pkill','-f','aud-chrome'])
A=np.asarray(Image.open(out).convert('L')).astype(int)
best={}
for i,(k,st,t,p) in enumerate(cands):
    y0=(10+i*H)*2-10; cell=A[y0:y0+H*2,:]
    b=box(cell); s=src[k]
    e=abs((b[1]-b[0])-(s[1]-s[0]))+abs((b[3]-b[2])-(s[3]-s[2]))+abs(b[4]-s[4])/max(s[4],1)*20
    # position: left css, top css so that bbox aligns
    left=((srcabs[k][0]+s[0])-1068)/2-(b[0]-40)/2
    top=((srcabs[k][1]+s[2])-70)/2-(b[2]-(y0+20)+y0-y0)/2 - 0  # b[2] relative to cell start y0; span top at y0+10 px*2? 
    top=((srcabs[k][1]+s[2])-70)/2-((b[2]+y0)-(10+i*H)*2)/2
    best.setdefault(k,[]).append((e,p,st,(b[1]-b[0])/2,(b[3]-b[2])/2,b[4],round(left,2),round(top,2)))
for k in best:
    best[k].sort(key=lambda r:r[0])
    for r in best[k][:4]: print(k,r)
