import sys, numpy as np
from PIL import Image
Image.MAX_IMAGE_PIXELS=None
# lines.py build sec x0 y0 x1 y1 bgthresh : prints ink rows bands and x extents for ref and build
b=sys.argv[1]; s=int(sys.argv[2]); x0,y0,x1,y1=map(int,sys.argv[3:7]); th=int(sys.argv[7]) if len(sys.argv)>7 else 40
SECY=[0,960,1698,3138,4886,7196,8294,9700,11192,12828,14080,15436,17425]
r=Image.open(f'ref/{s:02d}.png').convert('RGBA'); w=Image.new('RGBA',r.size,(255,255,255,255)); w.alpha_composite(r)
R=np.asarray(w.convert('RGB')).astype(int)[y0:y1,x0:x1]
B=np.asarray(Image.open(b).convert('RGB')).astype(int)[y0+SECY[s-1]:y1+SECY[s-1],x0:x1]
def bands(A):
  bg=np.median(A.reshape(-1,3),0)
  m=np.abs(A-bg).max(2)>th
  rows=m.any(1); out=[]; i=0
  while i<len(rows):
    if rows[i]:
      j=i
      while j<len(rows) and rows[j]: j+=1
      xs=np.where(m[i:j].any(0))[0]; out.append((i+y0,j-1+y0,xs.min()+x0,xs.max()+x0)); i=j
    else: i+=1
  return out
rb=bands(R); bb=bands(B)
print('ref  n=%d'%len(rb)); print('bld  n=%d'%len(bb))
for k in range(max(len(rb),len(bb))):
  a=rb[k] if k<len(rb) else None; c=bb[k] if k<len(bb) else None
  print(k, a, c, '' if not(a and c) else 'dy=%d/%d dx=%d/%d'%(c[0]-a[0],c[1]-a[1],c[2]-a[2],c[3]-a[3]))
