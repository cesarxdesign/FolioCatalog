from PIL import Image; import numpy as np
import inkbox as K
R=np.asarray(Image.open('render.png').convert('RGB')).astype(float)
S=K.P
B1=3017;B2=4692;X=1068
regs={'touch':(B1+140,B1+172,X+50,X+200)}
for i,cx in enumerate([110.5,300,489.5,679,868.5]):
    regs[f'cap1-{i+1}']=(B1+960,B1+995,X+int((cx-40)*2),X+int((cx+40)*2))
for i,(x,w) in enumerate([(28,134.5),(194,157.5),(383.5,173.5),(589,157),(778.5,173.5)]):
    cx=x+w/2; regs[f'cap2-{i+1}']=(B2+945,B2+975,X+int((cx-40)*2),X+int((cx+40)*2))
regs['score']=(305,345,X+138,X+194); regs['of']=(344,360,X+140,X+190)
for i,c in enumerate([314.75,323.1,331.6,340,348.5]):
    regs[f'star{i}']=(int(c-4),int(c+4),X+204,X+240); regs[f'cnt{i}']=(int(c-4),int(c+4),X+280,X+296)
out={}
for k,(y0,y1,x0,x1) in regs.items():
    a=K.inkbox(y0,y1,x0,x1,S); b=K.inkbox(y0,y1,x0,x1,R)
    out[k]=(a,b)
    print(f"{k:8s} S t{a['top']:7.1f} b{a['bot']:7.1f} l{a['left']:6.1f} r{a['right']:6.1f} w{a['w']:5.1f} h{a['h']:4.1f} dark{a['dark']:5.0f} m{a['mass']:6.1f} | R dt{b['top']-a['top']:+4.1f} db{b['bot']-a['bot']:+4.1f} dl{b['left']-a['left']:+4.1f} dr{b['right']-a['right']:+4.1f} dark{b['dark']:5.0f} mass x{b['mass']/a['mass']:4.2f}")
