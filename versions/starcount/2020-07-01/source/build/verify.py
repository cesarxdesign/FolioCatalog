import json,subprocess,sys,numpy as np
from PIL import Image
S='/private/tmp/claude-501/-Users-cgair-Claude/a92997a1-610b-4dee-9a2e-79d3d6d097d6/scratchpad/observatory-sqsp-build'
DEF=dict(TITLE_MT=48.6,INTRO_MT=24,PANEL_MT=70,S1_MT=69.2,GRID_MT=75.6,S2_MT=69.2,PHOTO_MT=70.1,LINK_MT=22.9,DIV_MT=75.1,NEXT_MT=82.5,FOOT_MT=68.5)
p=dict(DEF); p.update(json.loads(sys.argv[1]) if len(sys.argv)>1 else {})
t=open(S+'/fit/index.tpl.html').read()
for k,v in p.items(): t=t.replace(k+'px',f'{v:g}px')
assert '_MT' not in t
open(S+'/site/index.html','w').write(t)
json.dump(p,open(S+'/fit/params.json','w'))
subprocess.run([S+'/fit/render.sh',S+'/site/index.html',S+'/fit/render.png','2048','3556'])
R=np.asarray(Image.open(S+'/fit/render.png').convert('RGB')).astype(int)
P=np.asarray(Image.open(S+'/source/page.png').convert('RGB')).astype(int)
print('render',R.shape,'src',P.shape)
REG=[('introL',1270,1650,1068,2040),('introR',1270,1650,2060,3030),('s1',2900,3350,1440,2660),('s2',4600,5080,1440,2660),
     ('end',6280,6760,1440,2660),('foot',6840,7110,1068,2000)]
def bands(A,y0,y1,x0,x1):
    G=A[y0:y1,x0:x1]; bg=np.median(G.reshape(-1,3),axis=0)
    m=np.abs(G-bg).max(axis=2)>12
    d=np.diff(np.concatenate([np.zeros((m.shape[0],1),int),m.astype(int),np.zeros((m.shape[0],1),int)],axis=1),axis=1)
    rowok=[]
    for y in range(m.shape[0]):
        st=np.where(d[y]==1)[0]; en=np.where(d[y]==-1)[0]
        ok=[(s,e) for s,e in zip(st,en) if e-s>=3]
        rowok.append((ok[0][0],ok[-1][1]) if ok else None)
    out=[];cur=None
    for y,r in enumerate(rowok):
        if r is None:
            if cur: out.append(cur); cur=None
        elif cur is None: cur=[y,y,r[0],r[1]]
        else: cur[1]=y;cur[2]=min(cur[2],r[0]);cur[3]=max(cur[3],r[1])
    if cur: out.append(cur)
    mg=[]
    for b in out:
        if mg and b[0]-mg[-1][1]<=3: mg[-1]=[mg[-1][0],b[1],min(mg[-1][2],b[2]),max(mg[-1][3],b[3])]
        else: mg.append(list(b))
    out=mg
    return [(a+y0,b+y0,c+x0,e+x0) for a,b,c,e in out]
def ctr(A,b):
    # ink-weighted centroid row (sub-pixel) of the band
    G=A[b[0]:b[1]+1,b[2]:b[3]+1]; bg=255 if A[b[0]-2,b[2]-2].mean()>250 else A[b[0]-2,b[2]-2].mean()
    w=np.abs(G.mean(axis=2)-bg).sum(axis=1); return b[0]+(w*np.arange(len(w))).sum()/w.sum()
allr=[]
for n,y0,y1,x0,x1 in REG:
    bs=bands(P,y0,y1,x0,x1); br=bands(R,y0,y1,x0,x1)
    print(n,len(bs),len(br)); print('   S',[b[0] for b in bs]); print('   R',[b[0] for b in br])
    for i,(s,r) in enumerate(zip(bs,br)):
        dc=(ctr(R,r)-ctr(P,s))/2
        allr.append((n,i,dc,(r[0]-s[0])/2,((r[3]-r[2])-(s[3]-s[2]))/2,(r[2]-s[2])/2))
        print(f'  {n}{i} src y{s[0]}-{s[1]} x{s[2]}-{s[3]} | dtop {(r[0]-s[0])/2:+.1f} dctr {dc:+.2f} dx {(r[2]-s[2])/2:+.1f} dw {((r[3]-r[2])-(s[3]-s[2]))/2:+.1f}')
d=np.array([abs(a[2]) for a in allr]); print('lines',len(d),'<=0.5',int((d<=0.5).sum()),'<=1',int((d<=1).sum()),'max',round(d.max(),2))
# big blocks: edges
def edge(A,x,y0,y1):
    col=A[y0:y1:(1 if y1>y0 else -1),x].mean(axis=1); k=int(np.argmax(np.abs(col-col[0])>8)); return y0+k if y1>y0 else y0-k
for n,x,y0,y1 in [('hero',1500,40,120),('panel',1100,1700,1800),('panelbot',1100,2900,2800),('grid1',1500,3380,3460),('grid1bot',1500,3990,3900),('grid2',1500,3970,4020),('grid2bot',1500,4580,4500),('photo',1500,5100,5180),('photobot',1500,6280,6200),('divider',1800,6440,6520),('next',2000,6600,6700),('footer',1500,6800,6860)]:
    print(n,'src',edge(P,x,y0,y1),'ren',edge(R,x,y0,y1))
