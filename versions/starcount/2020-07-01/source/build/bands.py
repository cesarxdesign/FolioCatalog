from PIL import Image;import numpy as np,sys
def bands(P, x0=0, x1=None, thr=12, gap=1):
    G=P[:,x0:x1].astype(int)
    bgc=np.median(G[:, :20].reshape(-1,3),axis=0) if False else None
    rows=[]
    for y in range(G.shape[0]):
        r=G[y]; ref=np.array([255,255,255]) 
        m=(np.abs(r-ref).max(axis=1)>thr)
        # runs >=3
        if m.sum()<3: rows.append(None); continue
        idx=np.where(m)[0]
        # require a run of >=3
        d=np.diff(np.concatenate([[0],m.astype(int),[0]]))
        st=np.where(d==1)[0]; en=np.where(d==-1)[0]
        ok=[(s,e) for s,e in zip(st,en) if e-s>=3]
        if not ok: rows.append(None); continue
        rows.append((ok[0][0]+x0, ok[-1][1]-1+x0))
    out=[];cur=None
    for y,r in enumerate(rows):
        if r is None:
            if cur: out.append(cur); cur=None
        else:
            if cur is None: cur=[y,y,r[0],r[1]]
            else: cur[1]=y; cur[2]=min(cur[2],r[0]); cur[3]=max(cur[3],r[1])
    if cur: out.append(cur)
    return out
if __name__=='__main__':
    P=np.asarray(Image.open('page.png').convert('RGB'))
    for b in bands(P,0,3700): print(b, 'h',b[1]-b[0]+1,'w',b[3]-b[2]+1)
