# segment-aware comparison: split band lists at big blocks (h>=100 css*2) and compare within segments
import importlib.util,sys,os
sys.argv=['x']
exec(open(os.path.dirname(os.path.abspath(__file__))+'/cmp.py').read().split('regions=')[0])
def seg(bl):
    segs=[[]]
    for b in bl:
        if b[1]-b[0]>=200: segs.append([b]); segs.append([])
        else: segs[-1].append(b)
    return segs
reg=[('left',1060,2040,1200,1700),('right',2060,3040,1400,1700)]
tot=[];
for name,x0,x1,y0,y1 in reg:
    for a,b in zip(bands(S,x0,x1,y0,y1),bands(R,x0,x1,y0,y1)):
        tot.append((name,a,b))
SS=seg(bands(S,1060,3040,1000,9440)); RR=seg(bands(R,1060,3040,1000,9440))
print('segments',len(SS),len(RR))
for i,(sa,ra) in enumerate(zip(SS,RR)):
    if len(sa)!=len(ra): print('seg',i,'count mismatch',len(sa),len(ra))
    for a,b in zip(sa,ra): tot.append((f'seg{i}',a,b))
for name,a,b in tot:
    print(f'{name:6s} src {a[0]/2:7.1f}-{a[1]/2:7.1f} x{a[2]/2:7.1f}-{a[3]/2:7.1f} | dtop {(b[0]-a[0])/2:+5.1f} dbot {(b[1]-a[1])/2:+5.1f} dx {(b[2]-a[2])/2:+5.1f} dw {((b[3]-b[2])-(a[3]-a[2]))/2:+5.1f}')
