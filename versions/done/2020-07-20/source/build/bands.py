from PIL import Image; import numpy as np
P=np.asarray(Image.open('page.png').convert('RGB')).astype(int)
H=P.shape[0]
# container edges: color at x=1070 (inside column left edge) and x=1060 (outside)
inside=P[:,1072]; outside=P[:,1060]
prev=None; start=0
def key(y): return (tuple(inside[y]//3*3), tuple(outside[y]//3*3))
segs=[]
cur=None
for y in range(H):
    k=(tuple(inside[y]),tuple(outside[y]))
    if cur is None or np.abs(np.array(k[0])-np.array(cur[0])).max()>4 or np.abs(np.array(k[1])-np.array(cur[1])).max()>4:
        if cur is not None: segs.append((start,y-1,cur))
        cur=k; start=y
segs.append((start,H-1,cur))
for s in segs:
    if s[1]-s[0]>=3: print(s[0],s[1],s[1]-s[0]+1,s[2])
