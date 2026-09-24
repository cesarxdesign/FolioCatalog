import numpy as np
from PIL import Image
from bands import runs
P=np.asarray(Image.open('page.png').convert('RGB')).astype(float);g=P.mean(2)
def boxes(y0,y1,bg=238,thr=6,midrow=None):
    R=np.abs(g[y0:y1,1067:3028]-bg)>thr
    colany=R.mean(0)>0.3
    out=[]
    for (a,b) in runs(colany):
        if b-a<20: continue
        rows=R[:,a+5:b-5].mean(1)>0.3
        rr=[r for r in runs(rows) if r[1]-r[0]>20]
        out.append(((a+1067,b+1067),[(r[0]+y0,r[1]+y0) for r in rr]))
    return out
for nm,(a,b) in dict(b1=(1782,2589),b2=(3116,3923),b3=(5602,6409)).items():
    print(nm)
    for bx in boxes(a,b): print('  ',bx, (bx[0][1]-bx[0][0])/2)
