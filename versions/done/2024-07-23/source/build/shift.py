import sys
from PIL import Image
import numpy as np
SEC={'01':0,'02':960,'03':1698,'04':2658,'05':4098,'06':5818,'07':8858,'08':11090,'09':13386,'10':15818,'11':17898}
build=np.asarray(Image.open(sys.argv[1]).convert('L')).astype(float)
def best(sec,x,y,w,h,R=4,sub=True):
    ref=np.asarray(Image.open(f'ref/s{sec}.png').convert('L')).astype(float)
    r=ref[y:y+h,x:x+w]; oy=SEC[sec]
    res=[]
    for dy in range(-R,R+1):
        for dx in range(-R,R+1):
            b=build[oy+y+dy:oy+y+dy+h,x+dx:x+dx+w]
            res.append((np.abs(b-r).mean(),dx,dy))
    res.sort(); return res[0]
if __name__=='__main__':
    for spec in sys.argv[2:]:
        sec,x,y,w,h=spec.split(','); print(spec, best(sec,int(x),int(y),int(w),int(h)))
