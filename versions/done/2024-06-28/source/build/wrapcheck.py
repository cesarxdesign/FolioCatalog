import sys, numpy as np
from PIL import Image
Image.MAX_IMAGE_PIXELS=None
SECY=[0,960,1698,3138,4886,7196,8294,9700,11192,12828,14080,15436,17425]
B_=np.asarray(Image.open(sys.argv[1]).convert('RGB')).astype(int)
regions=[(2,160,230,1100,620),(2,1180,180,1800,560),(3,290,750,900,1050),(3,1060,790,1600,1010),(3,420,440,1500,520),(4,240,680,640,1310),(4,180,380,700,480),
(5,270,550,1650,710),(5,330,1730,960,1960),(5,980,1730,1600,1960),(5,700,330,1250,400),
(7,180,140,900,240),(7,180,360,800,800),(7,1410,760,1820,950),(7,1410,1060,1820,1340),(8,700,640,1600,960),(9,270,1260,1650,1500),(9,780,360,1140,430),
(10,130,280,460,345),(10,130,370,460,790),(11,130,180,460,245),(11,130,270,460,870),(12,120,440,600,540),
(12,130,720,700,820),(12,130,930,700,1050),(12,130,1140,700,1290),(12,130,1320,700,1530),(12,1300,695,1790,810),(12,1300,855,1790,970),(12,1300,995,1790,1175),(12,1300,1192,1790,1405),(12,1300,1420,1790,1505)]
def bands(A,x0,y0,th=40):
  bg=np.median(A.reshape(-1,3),0); m=np.abs(A-bg).max(2)>th
  rows=m.any(1); out=[]; i=0
  while i<len(rows):
    if rows[i]:
      j=i
      while j<len(rows) and rows[j]: j+=1
      xs=np.where(m[i:j].any(0))[0]; out.append((i+y0,j-1+y0,xs.min()+x0,xs.max()+x0)); i=j
    else: i+=1
  return out
tot=0;bad=0
for s,x0,y0,x1,y1 in regions:
  r=Image.open(f'ref/{s:02d}.png').convert('RGBA'); w=Image.new('RGBA',r.size,(255,255,255,255)); w.alpha_composite(r)
  R=np.asarray(w.convert('RGB')).astype(int)[y0:y1,x0:x1]; B=B_[SECY[s-1]+y0:SECY[s-1]+y1,x0:x1]
  rb=bands(R,x0,y0); bb=bands(B,x0,y0)
  msg=[]
  if len(rb)!=len(bb): msg.append(f'line bands {len(rb)} vs {len(bb)}')
  for a,c in zip(rb,bb):
    tot+=1
    d=[c[k]-a[k] for k in range(4)]
    if max(abs(v) for v in d)>2: msg.append(f'{a}->{c}'); bad+=1
  print(f'sec{s:02d} ({x0},{y0}) lines {len(rb)}/{len(bb)}', 'OK' if not msg else msg)
print('line bands compared',tot,'off by >2px:',bad)
