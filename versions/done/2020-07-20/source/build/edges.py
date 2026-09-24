from PIL import Image; import numpy as np, json, sys
P=np.asarray(Image.open('page.png').convert('RGB')).astype(float).mean(2)
X0=1068
def edge(profile, lo, hi):
    g=np.abs(np.diff(profile[lo:hi]))
    i=int(np.argmax(g))
    if 0<i<len(g)-1:
        a,b,c=g[i-1],g[i],g[i+1]; d=0.5*(a-c)/(a-2*b+c) if (a-2*b+c)!=0 else 0
    else: d=0
    return lo+i+0.5+d  # boundary position in pixel coords (between i and i+1)
def box(Y0, cx0,cx1, cy0,cy1, win=14):
    # approx box in css relative to band top Y0 (img), column X0
    L=[];R=[];T=[];B=[]
    x0=X0+int(cx0*2); x1=X0+int(cx1*2); y0=Y0+int(cy0*2); y1=Y0+int(cy1*2)
    for f in np.linspace(0.3,0.7,9):
        y=int(y0+(y1-y0)*f); row=P[y]
        L.append(edge(row,x0-win,x0+win)); R.append(edge(row,x1-win,x1+win))
        x=int(x0+(x1-x0)*f); col=P[:,x]
        T.append(edge(col,y0-win,y0+win)); B.append(edge(col,y1-win,y1+win))
    m=lambda v: float(np.median(v))
    l,r,t,b=m(L)-X0,m(R)-X0,m(T)-Y0,m(B)-Y0
    return dict(x=l/2,y=t/2,w=(r-l)/2,h=(b-t)/2, spread=[float(np.ptp(L)),float(np.ptp(R)),float(np.ptp(T)),float(np.ptp(B))])
if __name__=='__main__':
    Y0=int(sys.argv[1]); boxes=json.loads(sys.argv[2])
    for bx in boxes: print(bx, {k:(round(v,2) if isinstance(v,float) else v) for k,v in box(Y0,*bx).items()})
