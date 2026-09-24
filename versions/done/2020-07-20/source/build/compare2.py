# pair text bands in order and compare ink centroids (sub-pixel) and widths
from PIL import Image; import numpy as np, sys
from compare import bands
W='/private/tmp/claude-501/-Users-cgair-Claude/a92997a1-610b-4dee-9a2e-79d3d6d097d6/scratchpad/done-sqsp-build/work/'
def merge(b):
    out=[]
    for x in b:
        if out and x[0]-out[-1][1]<=1.0 and x[1]-x[0]<3: out[-1]=(out[-1][0],x[1],min(out[-1][2],x[2]),max(out[-1][3],x[3]))
        else: out.append(x)
    return out
GS=np.asarray(Image.open(W+'page.png').convert('L')).astype(float)
GR=np.asarray(Image.open(W+'render.png').convert('L')).astype(float)
def centroid(G,b,pad=2):
    y0=int(b[0]*2)-pad; y1=int(b[1]*2)+pad; x0=1068+int(b[2]*2)-4; x1=1068+int(b[3]*2)+4
    R=G[y0:y1,x0:x1]; bg=np.median(np.concatenate([G[y0:y1,x0-20:x0-4],G[y0:y1,x1+4:x1+20]],1))
    w=np.abs(bg-R); w[w<6]=0
    ys=np.arange(y0,y1)+0.5
    return (w.sum(1)*ys).sum()/w.sum()/2, w.sum()/4/255
S=merge(bands(W+'page.png')); R=merge(bands(W+'render.png'))
print(len(S),len(R))
res=[]
for i,(s,r) in enumerate(zip(S,R)):
    h=s[1]-s[0]
    if h<40:
        cs,ms=centroid(GS,s); cr,mr=centroid(GR,r)
        d=cr-cs; res.append(d)
        print(f'{i:3d} text  S {s[0]:7.1f} c {cs:8.2f} w {s[3]-s[2]:6.1f} | R c {cr:8.2f} w {r[3]-r[2]:6.1f} | dc {d:+5.2f} dw {(r[3]-r[2])-(s[3]-s[2]):+4.1f} mass {mr/ms:4.2f}')
    else:
        print(f'{i:3d} block S {s[0]:7.1f}-{s[1]:7.1f} | R {r[0]:7.1f}-{r[1]:7.1f} | dtop {r[0]-s[0]:+5.1f} dbot {r[1]-s[1]:+5.1f}')
a=np.abs(np.array(res)); print('text lines',len(a),'<=0.5:',(a<=0.5).sum(),'<=1:',(a<=1).sum(),'max',a.max().round(2))
