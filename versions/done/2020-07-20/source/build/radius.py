from PIL import Image; import numpy as np, sys, json
P=np.asarray(Image.open('page.png').convert('RGB')).astype(float).mean(2)
def fit(Y0,X0,box,corner='tl',fill=232):
    x,y,w,h=[v*2 for v in box]; x+=X0; y+=Y0
    pts=[]
    for dy in range(0,50):
        if corner=='tl': yy=int(round(y))+dy; row=P[yy, int(x)-6:int(x)+60]; base=int(x)-6
        else: yy=int(round(y+h))-1-dy; row=P[yy, int(x)-6:int(x)+60]; base=int(x)-6
        inner=np.median(P[yy,int(x)+60:int(x)+80])
        if abs(inner-fill)<40: continue
        thr=(fill+inner)/2
        s=np.sign(row-thr); ch=np.where(np.diff(s)!=0)[0]
        if len(ch)==0: continue
        i=ch[0]; a,b=row[i],row[i+1]; f=(thr-a)/(b-a) if b!=a else 0
        pts.append((dy+0.5, base+i+0.5+f - x))
    pts=np.array(pts)
    best=None
    for r in np.arange(4,50,0.5):
        dy=pts[:,0]; pred=np.where(dy<r, r-np.sqrt(np.maximum(r*r-(r-dy)**2,0)),0)
        e=np.abs(pred-pts[:,1]).mean()
        if best is None or e<best[0]: best=(e,r)
    return best[1]/2, round(best[0],2)
Y0=int(sys.argv[1]); fill=float(sys.argv[3]) if len(sys.argv)>3 else 232
for b in json.loads(sys.argv[2]):
    print(b, fit(Y0,1068,b,'tl',fill), fit(Y0,1068,b,'bl',fill))
