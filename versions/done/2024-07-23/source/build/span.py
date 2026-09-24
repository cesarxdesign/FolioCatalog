import sys
from PIL import Image
import numpy as np
SEC={'01':0,'02':960,'03':1698,'04':2658,'05':4098,'06':5818,'07':8858,'08':11090,'09':13386,'10':15818,'11':17898}
build=np.asarray(Image.open(sys.argv[1]).convert('L')).astype(float)
def prof(a):  # subpixel ink extents using coverage-weighted edges
    ink=(255-a).clip(0)/255.; col=ink.sum(axis=0); row=ink.sum(axis=1)
    xs=np.where(col>0.3)[0]; ys=np.where(row>0.3)[0]
    cx=(col*np.arange(len(col))).sum()/col.sum(); cy=(row*np.arange(len(row))).sum()/row.sum()
    return xs.min(),xs.max(),ys.min(),ys.max(),cx,cy
for spec in sys.argv[2:]:
    sec,x,y,w,h=spec.split(','); x,y,w,h=map(int,(x,y,w,h)); oy=SEC[sec]
    ref=np.asarray(Image.open(f'ref/s{sec}.png').convert('L')).astype(float)
    bg=np.median(ref[y:y+h,x:x+w])
    r=prof(ref[y:y+h,x:x+w]-bg+255); b=prof(build[oy+y:oy+y+h,x:x+w]-bg+255)
    print(spec,'ref x[%d..%d] y[%d..%d] c(%.2f,%.2f)'%tuple(r),' build x[%d..%d] y[%d..%d] c(%.2f,%.2f)'%tuple(b), ' dcx %.2f dcy %.2f'%(b[4]-r[4],b[5]-r[5]))
