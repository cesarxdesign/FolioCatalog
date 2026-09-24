import sys
from PIL import Image
import numpy as np
from secs import SEC
build=np.asarray(Image.open(sys.argv[1]).convert('L')).astype(float)
def sh(pr,pb,R=5):
    cs=[((np.roll(pb,-d)-pr)**2)[R+1:-R-1].sum() for d in range(-R,R+1)]
    i=int(np.argmin(cs))
    if 0<i<2*R:
        a,b,c=cs[i-1],cs[i],cs[i+1]; den=a-2*b+c; return i-R+(0.5*(a-c)/den if den else 0)
    return i-R
for spec in sys.argv[2:]:
    s,x,y,w,h=spec.split(','); x,y,w,h=map(int,(x,y,w,h))
    ref=np.asarray(Image.open(f'ref/s{s}.png').convert('L')).astype(float)[y:y+h,x:x+w]
    b=build[SEC[s]+y:SEC[s]+y+h,x:x+w]; bg=np.median(ref)
    ri=np.abs(ref-bg); bi=np.abs(b-bg); d=np.abs(ref-b)
    print(spec,'dx %+.2f dy %+.2f ink %.3f >24 %.2f%% max %d'%(sh(ri.sum(0),bi.sum(0)),sh(ri.sum(1),bi.sum(1)),bi.sum()/max(ri.sum(),1),(d>24).mean()*100,d.max()))
