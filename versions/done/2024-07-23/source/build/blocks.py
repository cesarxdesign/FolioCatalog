import sys
from PIL import Image
import numpy as np
SEC={'01':0,'02':960,'03':1698,'04':2658,'05':4098,'06':5818,'07':8858,'08':11090,'09':13386,'10':15818,'11':17898}
BLOCKS=[('02','kicker',120,90,450,54),('02','card',160,236,300,340),('02','role',1188,190,300,80),('02','details',1188,294,500,240),
('03','para',300,364,300,248),('03','title',1055,314,340,50),('03','list',1050,384,300,210),
('04','slash',140,428,26,62),('04','body',140,563,300,332),('04','caption',844,1004,285,44),
('05','path',140,448,230,62),('05','body',140,583,300,476),
('06','intro',270,410,1380,48),('07','note',840,344,240,44),('07','left',76,848,200,328),('07','source',76,1445,200,140),('07','tip',1422,615,200,172),
('07','hood',1504,933,153,36),('07','offline',1454,1648,152,36),('07','msource',1601,1404,171,36),
('08','intro',270,444,1380,48),('08','f91',158,1664,400,140),('09','h1',124,456,670,90),('09','lead',122,593,300,168),('09','f91',158,1908,400,172),
('10','f91',311,1312,400,460),('11','note',746,2096,430,44)]
def sh(pr,pb,R=4):
    cs=[((np.roll(pb,-d)-pr)**2)[R+1:-R-1].sum() for d in range(-R,R+1)]
    i=int(np.argmin(cs))
    if 0<i<2*R: a,b,c=cs[i-1],cs[i],cs[i+1]; return i-R+0.5*(a-c)/(a-2*b+c)
    return i-R
build=np.asarray(Image.open(sys.argv[1]).convert('L')).astype(float)
refs={}
for sec,name,x,y,w,h in BLOCKS:
    ref=refs.setdefault(sec,np.asarray(Image.open(f'ref/s{sec}.png').convert('L')).astype(float))
    r=ref[y:y+h,x:x+w]; b=build[SEC[sec]+y:SEC[sec]+y+h,x:x+w]
    bg=np.median(r); ri=np.abs(r-bg); bi=np.abs(b-bg)
    d=np.abs(r-b)
    print(f'{sec} {name:8} dx {sh(ri.sum(0),bi.sum(0)):+.2f} dy {sh(ri.sum(1),bi.sum(1)):+.2f}  ink ref/build {ri.sum()/1e3:.0f}/{bi.sum()/1e3:.0f}  maxd {d.max():.0f} >24 {(d>24).mean()*100:.2f}%')
