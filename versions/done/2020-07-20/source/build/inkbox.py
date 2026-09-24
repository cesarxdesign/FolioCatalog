from PIL import Image; import numpy as np
P=np.asarray(Image.open('page.png').convert('RGB')).astype(float)
def inkbox(y0,y1,x0,x1,img=P):
    R=img[y0:y1,x0:x1].mean(2)
    fill=np.median(R); dark=R.min() if fill>128 else R.max()
    thr=(fill+dark)/2
    M=(R<thr) if fill>128 else (R>thr)
    ys=np.where(M.any(1))[0]; xs=np.where(M.any(0))[0]
    # ink mass: sum of (fill - v)/(fill-dark)
    mass=np.clip((fill-R)/(fill-dark),0,1).sum() if fill>128 else np.clip((R-fill)/(dark-fill),0,1).sum()
    return dict(top=(y0+ys[0])/2,bot=(y0+ys[-1]+1)/2,left=(x0+xs[0]-1068)/2,right=(x0+xs[-1]+1-1068)/2,w=(xs[-1]+1-xs[0])/2,h=(ys[-1]+1-ys[0])/2,fill=fill,dark=dark,mass=mass/4, color=np.median(img[y0:y1,x0:x1][M],0) if M.any() else None)
if __name__=='__main__':
    B1=3017;B2=4692
    for nm,(y0,y1,x0,x1) in {'cap1':(B1+960,B1+995,1068+150,1068+300),'cap5':(B1+960,B1+995,1068+1700,1068+1800),'touch':(B1+140,B1+170,1068+50,1068+200),
      'se':(B2+945,B2+975,1068+120,1068+260),'max':(B2+945,B2+975,1068+1650,1068+1820)}.items():
        print(nm, inkbox(y0,y1,x0,x1))
