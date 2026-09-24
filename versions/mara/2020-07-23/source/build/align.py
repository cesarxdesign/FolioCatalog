import numpy as np
from PIL import Image
S='source/screenshots/'
fs=['1-2024-07-07-19.30.47.png','2-2024-07-07-19.30.50.png','3-2024-07-07-19.30.52.png','4-2024-07-07-19.30.59.png']
A=[np.asarray(Image.open(S+f).convert('RGB')).astype(np.int16) for f in fs]
est=[-96,1960,4040,5482]
for i in range(3):
    a,b=A[i][:,1000:3100],A[i+1][:,1000:3100]
    e=est[i+1]-est[i]
    res=[]
    for d in range(e-80,e+81):
        n=2304-d
        if n<50: continue
        diff=np.abs(a[d:d+n]-b[:n]).mean()
        res.append((diff,d,n))
    res.sort()
    print(i,e,res[:4])
    # row-content: ink rows in overlap
