import numpy as np
from PIL import Image
P=np.asarray(Image.open('page.png').convert('RGB')).astype(int)
g=P.mean(2)
def edges_x(y):
    r=g[y]; d=np.abs(np.diff(r)); idx=np.where(d>3)[0]; return idx[:3],idx[-3:]
for y in [100,1000,1800,2000,3200,3900,4100,5100,5620,6400,7600]:
    print(y, edges_x(y), P[y,2048], P[y,1100])
def edges_y(x,y0,y1):
    c=g[y0:y1,x]; d=np.abs(np.diff(c)); idx=np.where(d>3)[0]+y0; return idx
for x in [1080,3010]:
  for (a,b) in [(40,90),(1150,1200),(1760,1800),(2570,2610),(3100,3130),(3900,3940),(4040,4080),(5150,5180),(5590,5620),(6395,6420),(7490,7530)]:
    print(x,a,b,edges_y(x,a,b))
