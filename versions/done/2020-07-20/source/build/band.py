from PIL import Image; import numpy as np, sys
P=np.asarray(Image.open('page.png').convert('RGB')).astype(int)
y0,y1=int(sys.argv[1]),int(sys.argv[2]); thr=int(sys.argv[3]) if len(sys.argv)>3 else 6
R=P[y0:y1+1,1068:3028]
fill=np.median(R.reshape(-1,3),axis=0); print('fill',fill)
D=np.abs(R-fill).max(2)>thr
rows=D.any(1)
def spans(v):
    out=[];i=0
    while i<len(v):
        if v[i]:
            s=i
            while i<len(v) and v[i]: i+=1
            out.append((s,i-1))
        else: i+=1
    return out
for s,e in spans(rows):
    cols=D[s:e+1].any(0)
    cs=spans(cols)
    print(f'rows {s}-{e} (css {s/2}-{(e+1)/2}, h {(e-s+1)/2})', [(a/2,(b+1)/2,(b-a+1)/2) for a,b in cs][:12])
