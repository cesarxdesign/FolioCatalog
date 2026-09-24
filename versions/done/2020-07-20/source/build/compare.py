from PIL import Image; import numpy as np, sys
W='/private/tmp/claude-501/-Users-cgair-Claude/a92997a1-610b-4dee-9a2e-79d3d6d097d6/scratchpad/done-sqsp-build/work/'
def bands(path):
    P=np.asarray(Image.open(path).convert('RGB')).astype(float)[:11075]
    G=P.mean(2)
    H=G.shape[0]
    reg=G[:,1000:3100]
    bg=np.median(np.concatenate([G[:,900:1000],G[:,3100:3200]],1),1)[:,None]
    m=np.abs(reg-bg)>8
    k=(m[:,:-2]&m[:,1:-1]&m[:,2:])
    ink=k.any(1)
    out=[];y=0
    while y<H:
        if ink[y]:
            s=y
            while y<H and ink[y]: y+=1
            cols=np.where(k[s:y].any(0))[0]
            out.append((s/2,(y)/2,(cols[0]+1000-1068)/2,(cols[-1]+3+1000-1068)/2))
        else: y+=1
    return out
S=bands(W+'page.png'); R=bands(W+(sys.argv[1] if len(sys.argv)>1 else 'render.png'))
print(len(S),len(R))
n=max(len(S),len(R))
for i in range(n):
    s=S[i] if i<len(S) else None; r=R[i] if i<len(R) else None
    if s and r:
        print(f'{i:3d} S top {s[0]:7.1f} bot {s[1]:7.1f} x {s[2]:6.1f}-{s[3]:6.1f} | R top {r[0]:7.1f} bot {r[1]:7.1f} x {r[2]:6.1f}-{r[3]:6.1f} | dtop {r[0]-s[0]:+5.1f} dbot {r[1]-s[1]:+5.1f} dx0 {r[2]-s[2]:+5.1f} dx1 {r[3]-s[3]:+5.1f}')
    else: print(i,s,r)
