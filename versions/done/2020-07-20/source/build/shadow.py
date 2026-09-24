from PIL import Image; import numpy as np, sys
def prof(P,Y0,box):
    x,y,w,h=[v*2 for v in box]; X=1068+x; Y=Y0+y
    ym=slice(int(Y+h*0.35),int(Y+h*0.65)); xm=slice(int(X+w*0.3),int(X+w*0.7))
    L=P[ym, int(X)-12:int(X)].mean(0); R=P[ym, int(X+w):int(X+w)+12].mean(0)
    T=P[int(Y)-8:int(Y), xm].mean(1); B=P[int(Y+h):int(Y+h)+16, xm].mean(1)
    return np.concatenate([L,R,T,B])
S=np.asarray(Image.open('page.png').convert('L')).astype(float)
R=np.asarray(Image.open(sys.argv[1] if len(sys.argv)>1 else 'render.png').convert('L')).astype(float)
boxes=[(3017,(30,122,161,348.5)),(3017,(409,122,161,348.5)),(4692,(194,179,157.5,279.5)),(4692,(778.5,83,173.5,375.5))]
e=[]
for Y0,b in boxes:
    ps,pr=prof(S,Y0,b),prof(R,Y0,b); e.append(np.abs(ps-pr).mean())
    print(np.round(ps[:12]).astype(int), np.round(ps[36:52]).astype(int)); print(np.round(pr[:12]).astype(int), np.round(pr[36:52]).astype(int))
print('mean abs err', np.mean(e))
