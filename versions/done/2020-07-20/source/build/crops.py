# Cut every picture from the stitched page (2x). Boxes are in page CSS px (x from column left).
from PIL import Image; import numpy as np, json
B='/private/tmp/claude-501/-Users-cgair-Claude/a92997a1-610b-4dee-9a2e-79d3d6d097d6/scratchpad/done-sqsp-build'
P=Image.open(B+'/work/page.png').convert('RGB')
X0=1068
def cut(name,x,y,w,h,q=90,edit=None):
    box=(X0+round(x*2),round(y*2),X0+round((x+w)*2),round((y+h)*2))
    im=P.crop(box)
    if edit: im=edit(im)
    im.save(f'{B}/site/img/{name}.webp',quality=q,method=6)
    return im.size
out={}
# hero: paint the rating text (5.0, out of 5, stars, counts) with the hero's own flat #2F2F2F; keep the bars.
def hero_edit(im):
    a=np.asarray(im).copy()
    def fill(x0,y0,x1,y1):  # css, relative to hero box (top 35)
        a[round(y0*2):round(y1*2), round(x0*2):round(x1*2)]=(47,47,47)
    fill(69,119.5,97,135.5)     # 5.0
    fill(71,137.5,95,145)       # out of 5
    fill(102.5,120,119.5,141.5) # stars
    fill(140,120,148,142)       # counts
    return Image.fromarray(a)
out['hero']=cut('hero',0,35,980,551.5,q=92,edit=hero_edit)
out['sketches']=cut('sketches',0,862,980,298.5,q=92)
out['photos']=cut('photos',0,3183.5,980,262,q=90)
out['watch']=cut('watch',0,3468.5,980,552,q=90)
# band 1 (top 1508.5): five iPhone X screens
for i,x in enumerate([30,219.5,409,598.5,788]):
    out[f'touch-{i+1}']=cut(f'touch-{i+1}',x,1508.5+122,161,348.5,q=92)
# band 2 (top 2346): SE, 8, 8 Plus, X, XS Max, bottoms on one line
b2=[(28.25,220.36,134.03,238.17),(194.17,179.15,157.13,279.57),(383.64,150.09,173.56,308.44),(588.83,118.31,157.28,340.44),(778.28,83.2,173.53,375.54)]
b2r=[]
for i,(x,y,w,h) in enumerate(b2):
    xa,ya=round(x*2)/2,round((2346+y)*2)/2; xb,yb=round((x+w)*2)/2,round((2346+y+h)*2)/2
    out[f'size-{i+1}']=cut(f'size-{i+1}',xa,ya,xb-xa,yb-ya,q=92); b2r.append((xa,ya-2346,xb-xa,yb-ya))
print('band2 boxes',b2r)
# dark band (top 4289.5): eight rendered devices, slot = device + its shadow on the panel fill
k=0
for r,yy in enumerate([36,444.5]):
    for c,xx in enumerate([40,257.5,474.5,692]):
        k+=1; out[f'device-{k}']=cut(f'device-{k}',xx,4289.5+yy,210,351,q=90)
print(json.dumps(out))
