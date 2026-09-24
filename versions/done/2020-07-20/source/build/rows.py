from PIL import Image; import numpy as np
P=np.asarray(Image.open('page.png').convert('RGB')).astype(int)
G=P[:,:3500].max(2)*0+P[:,:3500].mean(2)
def runs_ink(row,bg,thr=8):
    m=np.abs(row-bg)>thr
    # runs >=3
    k=np.convolve(m.astype(int),np.ones(3,int),'same')>=3
    return k
ink=np.zeros(P.shape[0],bool); xs={}
for y in range(P.shape[0]):
    r=G[y,1000:3100]
    bg=np.median(np.concatenate([G[y,900:1000],G[y,3100:3200]]))
    k=runs_ink(r,bg)
    if k.any():
        ink[y]=True; w=np.where(k)[0]; xs[y]=(w[0]+1000,w[-1]+1000)
# bands
y=0;H=len(ink)
while y<H:
    if ink[y]:
        s=y
        while y<H and ink[y]: y+=1
        x0=min(xs[i][0] for i in range(s,y)); x1=max(xs[i][1] for i in range(s,y))
        print(f'{s:6d} {y-1:6d} h={y-s:5d}  x {x0}-{x1}  css y {s/2:.1f} h {(y-s)/2:.1f} x {(x0-1068)/2:.1f}-{(x1+1-1068)/2:.1f}')
    else: y+=1
