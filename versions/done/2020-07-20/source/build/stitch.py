from PIL import Image; import numpy as np
order=[9,6,3,5,1,11]
imgs=[np.asarray(Image.open(f'raw/raw_{i}.png').convert('RGB')).astype(np.float32) for i in order]
X0,X1=1068,3028
def prof(a):
    g=a[:,X0:X1].mean(2)
    return g.reshape(g.shape[0],49,40).mean(2)  # 49 blocks of 40px
offs=[]
for k in range(5):
    A,B=imgs[k],imgs[k+1]; pa,pb=prof(A),prof(B)
    H=A.shape[0]; best=[]
    for d in range(1,H-60):
        n=H-d
        e=np.abs(pa[d:]-pb[:n]).mean()
        # require information: variance
        best.append((e,d))
    best.sort()
    cands=best[:5]
    res=[]
    for e,d in cands:
        n=H-d
        full=np.abs(A[d:,X0:X1]-B[:n,X0:X1]).mean()
        res.append((round(float(full),3),d,n))
    print(order[k],order[k+1],res)
