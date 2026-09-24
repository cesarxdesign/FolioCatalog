from PIL import Image; import numpy as np
a=np.asarray(Image.open('page.png').convert('RGB')).astype(np.float64); g=a.mean(2)
def edge(prof, i_out, direction):
    # prof: 1D; i_out: index of last fully-white pixel outside; direction +1 moves inward
    # coverage-weighted edge: walk inward up to 3 px
    inner=np.median(prof[i_out+direction*4:i_out+direction*7:direction])
    cov=0; i=i_out+direction
    for k in range(3):
        c=(255-prof[i+direction*k])/(255-inner) if inner<250 else 0
        cov+=min(max(c,0),1)
    # edge position (as boundary coordinate)
    if direction>0: return i_out+1+3-cov   # boundary before first covered
    else: return i_out-3+cov
def box(y0,y1,x0,x1):
    # approximate box; refine
    cols=g[y0+20:y1-20, :]
    rows=g[:, x0+20:x1-20]
    px=cols.mean(0); py=rows.mean(1)
    # left: find last white col before x0+... 
    L=x0-3
    while px[L+1]>253: L+=1
    R=x1+2
    while px[R-1]>253: R-=1
    T=y0-3
    while py[T+1]>253: T+=1
    B=y1+2
    while py[B-1]>253: B-=1
    l=edge(px,L,1); r=edge(px,R,-1)+1; t=edge(py,T,1); b=edge(py,B,-1)+1
    return l/2,r/2,t/2,b/2
boxes={'hero':(70,1173,1067,3029),'band':(1782,2884,1067,3029),
 'w1':(3435,3896,1067,1715),'w2':(3435,3896,1724,2372),'w3':(3435,3896,2382,3029),
 'flow':(4513,5262,1067,3029),'g1':(5801,6346,1067,2037),'g2':(5801,6346,2059,3029),
 'g3':(6367,6914,1067,2037),'g4':(6367,6914,2059,3029),'mac':(7473,8577,1067,3029)}
for k,v in boxes.items():
    l,r,t,b=box(*v); print(f'{k:5s} x {l:.2f}-{r:.2f} (w {r-l:.2f}, rel {l-512:.2f})  y {t:.2f}-{b:.2f} (h {b-t:.2f})')
