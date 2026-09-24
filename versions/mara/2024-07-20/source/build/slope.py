import numpy as np, sys
from PIL import Image
H=[960,762,2264,2343,1960,1912,3561,2040,2264,1858,1535,1241,1518,2161,1679,2189,2715]
SEC={};y=0
for i,h in enumerate(H): SEC['%02d'%(i+1)]=y; y+=h
def sh(pr,pb,R=4):
    cs=[((np.roll(pb,-d)-pr)**2)[R+1:-R-1].sum() for d in range(-R,R+1)]
    i=int(np.argmin(cs))
    if 0<i<2*R: a,b,c=cs[i-1],cs[i],cs[i+1]; den=(a-2*b+c); return i-R+(0.5*(a-c)/den if den else 0)
    return i-R
build=np.asarray(Image.open(sys.argv[1]).convert('L')).astype(float)
# style: list of (sec, y0, x0, x1, lh) first lines
L={'lead':[('09',559,160,1740,42),('07',661,160,1740,42),('14',1660,188,1720,42),('16',1625,188,1720,42)],
   'body':[('04',1877,160,1200,32),('05',1504,89,930,32),('06',1262,569,1340,32)],
   'body2':[('12',447,160,680,32),('12',479,160,680,32),('11',945,160,680,32),('12',695,160,680,32)],
   'small':[('09',1672,228,890,30),('09',1702,228,890,30),('09',1672,1020,1690,30),('07',3000,409,945,30)],
   'small28':[('08',1444,751,1830,28)],
   'card':[('02',290,168,1060,24),('02',314,168,1060,24),('02',338,168,1060,24)],
   'note':[('14',435,114,450,40)],'list':[('07',1822,185,900,32),('07',1854,185,900,32)],
   'h1':[('04',304,160,530,81),('09',374,160,690,81),('07',452,160,670,81)]}
for st,lines in L.items():
    xs=[];ds=[]
    for sec,y0,x0,x1,lh in lines:
        ref=np.asarray(Image.open(f'ref/s{sec}.png').convert('L')).astype(float)
        for xw in range(x0,x1-100,100):
            r=ref[y0:y0+lh,xw:xw+100]; b=build[SEC[sec]+y0:SEC[sec]+y0+lh,xw:xw+100]
            bg=np.median(r); pr=np.abs(r-bg).sum(0)
            if pr.sum()<500: continue
            xs.append(xw+50-x0); ds.append(sh(pr,np.abs(b-bg).sum(0)))
    xs=np.array(xs);ds=np.array(ds); ok=np.abs(ds)<3
    p=np.polyfit(xs[ok],ds[ok],1)
    print(f'{st:8} slope/1000px {p[0]*1000:+.3f}  intercept {p[1]:+.2f}  n={ok.sum()}')
