import sys, numpy as np
from PIL import Image
Image.MAX_IMAGE_PIXELS=None
SECY=[0,960,1698,3138,4886,7196,8294,9700,11192,12828,14080,15436,17425]
H=[960,738,1440,1748,2310,1098,1406,1492,1636,1252,1356,1989,1900]
b=np.asarray(Image.open(sys.argv[1]).convert('RGB')).astype(int)
for s in map(int,sys.argv[2].split(',')):
  r=Image.open(f'ref/{s:02d}.png').convert('RGBA'); w=Image.new('RGBA',r.size,(255,255,255,255)); w.alpha_composite(r)
  R=np.asarray(w.convert('RGB')).astype(int); B=b[SECY[s-1]:SECY[s-1]+H[s-1]]
  bad=np.abs(R-B).max(2)>24
  p=np.pad(bad,1)
  solid=bad.copy()
  for dy in (-1,0,1):
    for dx in (-1,0,1):
      solid&=p[1+dy:1+dy+bad.shape[0],1+dx:1+dx+bad.shape[1]]
  ys,xs=np.where(solid)
  cells={}
  for y,x in zip(ys,xs): cells[(y//40*40,x//40*40)]=cells.get((y//40*40,x//40*40),0)+1
  top=sorted(cells.items(),key=lambda t:-t[1])[:6]
  print(f'sec {s:02d}: bad {bad.sum()} solid-core {solid.sum()} top cells (y,x):n', top)
