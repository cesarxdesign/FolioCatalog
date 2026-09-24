import numpy as np, sys, json
from PIL import Image
def runs(bool1d):
    r=[];s=None
    for i,v in enumerate(list(bool1d)+[False]):
        if v and s is None: s=i
        if not v and s is not None: r.append((s,i)); s=None
    return r
def bands(path, regions, x0=1060, x1=3040, thr=30):
    P=np.asarray(Image.open(path).convert('RGB')).astype(int); g=P.mean(2)
    out=[]
    for (a,b) in regions:
        R=g[a:b,x0:x1]; bg=np.median(R)
        m=np.abs(R-bg)>thr
        k=m[:,:-2]&m[:,1:-1]&m[:,2:]   # runs of >=3
        k=np.pad(k,((0,0),(0,2)))
        rows=k.sum(1)>0
        for (s,e) in runs(rows):
            if e-s<3: continue
            cols=np.where(k[s:e].any(0))[0]
            out.append(dict(top=a+s,bot=a+e,h=e-s,xl=int(x0+cols[0]),xr=int(x0+cols[-1]+3),bg=float(bg),ink=float(R[s:e].min())))
    return out
if __name__=='__main__':
    regs=[(1173,1781),(2589,3115),(3923,4061),(5165,5602),(6250,6400),(6409,7512),(7512,7787)]
    B=bands('page.png',regs)
    for b in B: print(b['top'],b['bot'],b['h'],b['xl'],b['xr'],b['xr']-b['xl'],round(b['bg']),round(b['ink']))
    json.dump(B,open('src_bands.json','w'))
