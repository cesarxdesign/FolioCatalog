from PIL import Image; import numpy as np
def m(f):
    G=np.asarray(Image.open(f).convert('L')).astype(float)
    col=G[1270:1400,1082]; s=np.where(np.diff((col<128).astype(int))!=0)[0]
    ys=[(1270+i+(128-col[i])/(col[i+1]-col[i])+0.5)/2 for i in s]
    row=G[1330,1068:2100]; s=np.where(np.diff((row<128).astype(int))!=0)[0]
    xs=[(i+(128-row[i])/(row[i+1]-row[i])+0.5)/2 for i in s]
    mass=(255-G[1280:1390,1068:2000]).sum()/255/4
    return ys[0],ys[-1],xs[0],xs[-1],mass
a=m('page.png'); b=m('render.png')
print('S top %.2f bot %.2f x0 %.2f x1 %.2f mass %.0f'%a); print('R top %.2f bot %.2f x0 %.2f x1 %.2f mass %.0f'%b)
