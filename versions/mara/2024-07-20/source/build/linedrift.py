import numpy as np, sys
from PIL import Image
H=[960,762,2264,2343,1960,1912,3561,2040,2264,1858,1535,1241,1518,2161,1679,2189,2715]
SEC={};y=0
for i,h in enumerate(H): SEC['%02d'%(i+1)]=y; y+=h
def sh(pr,pb,R=5):
    cs=[((np.roll(pb,-d)-pr)**2)[R+1:-R-1].sum() for d in range(-R,R+1)]
    i=int(np.argmin(cs))
    if 0<i<2*R: a,b,c=cs[i-1],cs[i],cs[i+1]; den=(a-2*b+c); return i-R+(0.5*(a-c)/den if den else 0)
    return i-R
build=np.asarray(Image.open(sys.argv[1]).convert('L')).astype(float)
for sec,y0,x0,x1,lh in [('09',559,160,1760,42),('07',661,160,1760,42),('14',1660,188,1732,42),('16',1625,188,1732,42),('12',447,160,690,32),('02',242,168,1064,24)]:
    ref=np.asarray(Image.open(f'ref/s{sec}.png').convert('L')).astype(float)
    out=[]
    for xs in range(x0,x1-150,150):
        r=ref[y0:y0+lh,xs:xs+150]; b=build[SEC[sec]+y0:SEC[sec]+y0+lh,xs:xs+150]
        bg=np.median(r); out.append('%+.2f'%sh(np.abs(r-bg).sum(0),np.abs(b-bg).sum(0)))
    print(sec,' '.join(out))
