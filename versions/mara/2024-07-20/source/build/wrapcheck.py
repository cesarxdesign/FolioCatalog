import json, numpy as np, sys
from PIL import Image
H=[960,762,2264,2343,1960,1912,3561,2040,2264,1858,1535,1241,1518,2161,1679,2189,2715]
SEC={};y=0
for i,h in enumerate(H): SEC[i+1]=y; y+=h
L=json.load(open('lines.json'))
build=np.asarray(Image.open(sys.argv[1]).convert('L')).astype(int)
refs={}
bad=0; n=0
for e in L:
    s=e['sec']; ref=refs.setdefault(s,np.asarray(Image.open('ref/s%02d.png'%s).convert('L')).astype(int))
    for (l,t,r,b) in e['lines']:
        x0=max(0,l-60); x1=min(1920,r+60); y0=t+2; y1=b-2
        if y1<=y0: continue
        def ext(a):
            band=a[y0:y1,x0:x1]; bg=np.median(np.concatenate([band[:,:3].ravel(),band[:,-3:].ravel()]))
            cols=np.where((np.abs(band-bg)>40).any(0))[0]
            return (x0+cols.min(), x0+cols.max()) if len(cols) else None
        er=ext(ref); eb=ext(build[SEC[s]+0:SEC[s]+H[s-1]])
        n+=1
        if er is None or eb is None or abs(er[0]-eb[0])>2 or abs(er[1]-eb[1])>2:
            bad+=1; print(s, repr(e['txt']), 'line@',t, 'ref',er,'build',eb)
print('lines checked',n,'mismatch',bad)
