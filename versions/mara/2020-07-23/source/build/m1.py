import numpy as np
from PIL import Image
P=np.asarray(Image.open('page.png').convert('RGB')).astype(int)
g=P.mean(2)
# row classification over x 1000..3100
cols=g[:,1000:3100]
med=np.median(cols,1)
# segments of constant median
segs=[];s=0
def key(v): return int(round(v))
for y in range(1,len(med)+1):
    if y==len(med) or abs(med[y]-med[s])>1.5:
        segs.append((s,y,med[s])); s=y
for a,b,m in segs:
    if b-a>=4: print(a,b,b-a,round(m,1))
