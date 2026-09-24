from PIL import Image; import numpy as np, sys
S=np.asarray(Image.open(__import__('os').path.dirname(__file__)+'/page.png').convert('L')).astype(np.int16)
R=np.asarray(Image.open(__import__('os').path.dirname(__file__)+'/render.png').convert('L')).astype(np.int16)
def runs(m):
    out=[];s=None
    for i,v in enumerate(m):
        if v and s is None:s=i
        if not v and s is not None: out.append((s,i));s=None
    if s is not None: out.append((s,len(m)))
    return out
def ink_rows(img,x0,x1,y0,y1,bg=None):
    seg=img[y0:y1,x0:x1]
    b = np.median(seg,axis=1,keepdims=True) if bg is None else bg
    d=np.abs(seg-b)>12
    # runs >=3 horizontally: approximate via convolution
    k=d[:,:-2]&d[:,1:-1]&d[:,2:]
    return k.any(1)
def bands(img,x0,x1,y0,y1):
    m=ink_rows(img,x0,x1,y0,y1)
    out=[]
    for s,e in runs(m):
        seg=img[y0+s:y0+e,x0:x1]
        b=np.median(img[y0+s:y0+e,x0:x1]);d=(np.abs(seg-b)>12)
        xs=np.where(d.any(0))[0]
        out.append((y0+s,y0+e,x0+xs.min(),x0+xs.max()+1))
    return out
regions=[('left',1060,2040,1200,1700),('right',2060,3040,1400,1700),('main',1060,3040,0,9440)]
allres=[]
for name,x0,x1,y0,y1 in regions:
    bs=bands(S,x0,x1,y0,y1); br=bands(R,x0,x1,y0,y1)
    print(f'== {name}: src {len(bs)} bands, render {len(br)}')
    for i in range(max(len(bs),len(br))):
        a=bs[i] if i<len(bs) else None; b=br[i] if i<len(br) else None
        if a and b:
            print(f'{i:3d} src {a[0]/2:8.1f}-{a[1]/2:8.1f} x{a[2]/2:7.1f}-{a[3]/2:7.1f} | ren {b[0]/2:8.1f}-{b[1]/2:8.1f} x{b[2]/2:7.1f}-{b[3]/2:7.1f} | dy {(b[0]-a[0])/2:+6.1f} {(b[1]-a[1])/2:+6.1f} dw {((b[3]-b[2])-(a[3]-a[2]))/2:+5.1f}')
        else: print(i,'src',a,'ren',b)
