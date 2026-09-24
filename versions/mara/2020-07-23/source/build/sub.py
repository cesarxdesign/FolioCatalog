import numpy as np
from PIL import Image
P=np.asarray(Image.open('page.png').convert('RGB')).astype(float)
g=P.mean(2)
def step(prof,i0,i1):
    # subpixel location of a single monotone step between levels at ends
    p=prof[i0:i1]; a=np.median(p[:3]); b=np.median(p[-3:])
    if abs(b-a)<2: return None
    t=(p-a)/(b-a); t=np.clip(t,0,1)
    return i0+ (len(p)-t.sum()) - 0.5 +0.5  # count of pixels at level a
def ystep(y0,y1,xs):
    return np.median([step(g[:,x],y0,y1) for x in xs])
xs=range(1100,3000,37)
for nm,(a,b) in dict(head=(40,60),herotop=(60,80),herobot=(1165,1180),b1t=(1775,1790),b1b=(2580,2596),b2t=(3108,3122),b2b=(3914,3930),skt=(4055,4070),skb=(5157,5172),b3t=(5595,5610),b3b=(6400,6416),foot=(7505,7520)).items():
    xx=xs
    if nm in('skt','skb'): xx=range(1070,1100,3)
    print(nm, round(ystep(a,b,xx),2), round(ystep(a,b,xx)/2,2))
for y in (500,2000,3500,5700):
    r=g[y]; print('x',y, step(r,1055,1080), step(r,3015,3040))
