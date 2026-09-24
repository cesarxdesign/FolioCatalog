import numpy as np
from PIL import Image
P=np.asarray(Image.open('page.png').convert('RGB')).astype(float);g=P.mean(2)
def edge(p):
    # p: profile crossing from outside (bg-ish) to inside (white). subpixel edge = where crosses midpoint
    a=p[0];b=p[-1];m=(a+b)/2
    for i in range(1,len(p)):
        if (p[i-1]-m)*(p[i]-m)<=0 and p[i]!=p[i-1]:
            return i-1+(m-p[i-1])/(p[i]-p[i-1])+0.5
def measure(x0,x1,y0,y1):
    ym=(y0+y1)//2; xm=(x0+x1)//2
    L=[x0-8+edge(g[y,x0-8:x0+8]) for y in range(ym-150,ym+150,10)]
    R=[x1-8+(16-edge(g[y,x1-8:x1+8][::-1])) for y in range(ym-150,ym+150,10)]
    T=[y0-8+edge(g[y0-8:y0+8,x]) for x in range(xm-60,xm+60,6)]
    B=[y1-8+(16-edge(g[y1-8:y1+8,x][::-1])) for x in range(xm-60,xm+60,6)]
    f=lambda v: round(float(np.median([q for q in v if q is not None])),2)
    return f(L),f(R),f(T),f(B)
import sys
for (x0,x1,y0,y1) in [(1306,1583,1885,2486),(1603,1880,1885,2486),(1913,2183,1885,2486),(2216,2494,1885,2486),(2513,2790,1885,2486)]:
    l,r,t,b=measure(x0,x1,y0,y1); print(l,r,t,b,'w',round((r-l)/2,2),'h',round((b-t)/2,2),'cssx',round((l-1067.6)/2,2),'cssy',round(t/2,2))
print('---')
def radius(L,T,xs_dir=1):
    # measure left edge per row near top
    ds=[];xs=[]
    for d in range(0,40):
        y=int(T)+d
        p=g[y,int(L)-8:int(L)+60]
        e=edge(p[:])
        if e is None: continue
        ds.append(y+0.5-T); xs.append(int(L)-8+e-L)
    best=None
    for r in np.arange(4,60,0.5):
        pred=[ (r-np.sqrt(max(r*r-(r-d)**2,0))) if d<r else 0 for d in ds]
        err=np.mean((np.array(pred)-np.array(xs))**2)
        if best is None or err<best[0]: best=(err,r)
    return best
print(radius(1306.0,1884.68), radius(1609.39,1884.68))
# shadow profiles
print('left of phone1', [int(v) for v in g[2200,1260:1310]])
print('below phone1', [int(v) for v in g[2480:2560,1440]])
print('above phone1', [int(v) for v in g[1830:1890,1440]])
print('right phone5', [int(v) for v in g[2200,2785:2840]])
