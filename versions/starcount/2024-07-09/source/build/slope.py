import sys, json, collections
from PIL import Image
import numpy as np
from secs import SEC, sec_of
build=np.asarray(Image.open(sys.argv[1]).convert('L')).astype(float)
M=json.load(open(sys.argv[2]))['lines.js']
CL=json.load(open(sys.argv[3])) if len(sys.argv)>3 else {}
def sh(pr,pb,R=4):
    cs=[((np.roll(pb,-d)-pr)**2)[R+1:-R-1].sum() for d in range(-R,R+1)]
    i=int(np.argmin(cs))
    if 0<i<2*R:
        a,b,c=cs[i-1],cs[i],cs[i+1]; den=a-2*b+c; return i-R+(0.5*(a-c)/den if den else 0)
    return i-R
refs={}
res=collections.defaultdict(list)
for e in M:
    if len(e['lines'])<1: continue
    s=sec_of(e['box'][1]+1); ref=refs.setdefault(s,np.asarray(Image.open(f'ref/s{s}.png').convert('L')).astype(float))
    tot_w=sum(l[2] for l in e['lines']); nch=len(e['txt'])
    num=den=0
    for x,y,w,h in e['lines']:
        if w<250: continue
        y0=int(y)-SEC[s]-2; y1=int(y+h)-SEC[s]+2
        q=w/3
        dd=[]
        for xa in (x, x+2*q):
            xa=int(xa)-5; xb=int(xa+q)+10
            r=ref[y0:y1,xa:xb]; b=build[SEC[s]+y0:SEC[s]+y1,xa:xb]; bg=np.median(r)
            dd.append(sh(np.abs(r-bg).sum(0),np.abs(b-bg).sum(0)))
        num+=dd[1]-dd[0]; den+=2*q
    if den: res[CL.get(str(e['i']),'?')].append((e['i'],e['txt'][:20],num/den))
for k,v in res.items():
    sl=[x[2] for x in v]; print(k, 'slope px/px %.5f'%np.median(sl), [(i,t,round(z*1000,2)) for i,t,z in v][:6])
