import sys
from PIL import Image
Image.MAX_IMAGE_PIXELS=None
# cmp.py build.png sec(1-13) x0 y0 x1 y1 scale out
b=sys.argv[1]; s=int(sys.argv[2]); x0,y0,x1,y1=map(int,sys.argv[3:7]); sc=float(sys.argv[7]); out=sys.argv[8]
SECY=[0,960,1698,3138,4886,7196,8294,9700,11192,12828,14080,15436,17425]
r=Image.open(f'ref/{s:02d}.png').convert('RGBA'); w=Image.new('RGBA',r.size,(255,255,255,255)); w.alpha_composite(r); r=w.convert('RGB')
B=Image.open(b).convert('RGB')
rc=r.crop((x0,y0,x1,y1)); bc=B.crop((x0,y0+SECY[s-1],x1,y1+SECY[s-1]))
W,H=int((x1-x0)*sc),int((y1-y0)*sc)
o=Image.new('RGB',(W,2*H+6),(255,0,255)); o.paste(rc.resize((W,H),Image.NEAREST),(0,0)); o.paste(bc.resize((W,H),Image.NEAREST),(0,H+6)); o.save(out)
