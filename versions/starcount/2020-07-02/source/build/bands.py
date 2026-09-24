from PIL import Image; import numpy as np
a=np.asarray(Image.open('page.png').convert('RGB')).astype(np.int16)
g=a.mean(2)
def runs(mask):
    out=[];y=None
    for i,v in enumerate(mask):
        if v and y is None: y=i
        if not v and y is not None: out.append((y,i));y=None
    if y is not None: out.append((y,len(mask)))
    return out
# rows: classify by fraction of non-white in column 1068..3028
col=g[:,1060:3036]
nonw=(np.abs(col-255)>3).mean(1)
for y0,y1 in runs(nonw>0):
    seg=col[y0:y1]
    # horizontal extent
    xs=np.where((np.abs(seg-255)>3).any(0))[0]
    print(f'{y0:5d}-{y1:5d} h={y1-y0:4d} css {y0/2:.1f}-{y1/2:.1f} x {xs.min()+1060}-{xs.max()+1060+1} maxfrac {nonw[y0:y1].max():.2f}')
