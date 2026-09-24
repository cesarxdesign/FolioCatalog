import numpy as np, subprocess, os, json, sys
from PIL import Image
from bands import runs
CH="/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
HERE=os.path.dirname(os.path.abspath(__file__))
def render(out='render.png',H=3894):
    subprocess.run([CH,'--headless=new','--disable-gpu','--hide-scrollbars','--force-device-scale-factor=2','--window-size=2048,%d'%H,'--screenshot='+os.path.join(HERE,out),'file://'+os.path.join(HERE,'site/index.html')],capture_output=True)
def load(p): 
    P=np.asarray(Image.open(p).convert('RGB')).astype(int); return P, P.mean(2)
def colleft(g,y):
    r=g[y]; return None
def panels(g,xl):
    # rows where the column (xl+20 .. xl+1940) median is not white
    med=np.median(g[:,xl+4:xl+30],1)
    pr=[(a,b) for a,b in runs(med<252.5) if b-a>100]
    return pr
def lines(g,y0,y1,x0,x1,thr=30):
    R=g[y0:y1,x0:x1]; bg=np.median(R); m=np.abs(R-bg)>thr
    k=m[:,:-2]&m[:,1:-1]&m[:,2:]
    out=[]
    rr=[]
    for a,b in runs(k.any(1)):
        if rr and a-rr[-1][1]<=2: rr[-1]=(rr[-1][0],b)
        else: rr.append((a,b))
    for a,b in rr:
        if b-a<3: continue
        cols=np.where(k[a:b].any(0))[0]
        out.append((y0+a,y0+b,x0+cols[0],x0+cols[-1]+3))
    return out
def measure(path, xl):
    P,g=load(path)
    pn=panels(g,xl)
    res={'panels':pn}
    gaps=[(pn[i][1],pn[i+1][0]) for i in range(len(pn)-1)]
    T=[]
    for gi,(a,b) in enumerate(gaps):
        if gi==0:  # intro: split cols
            L=lines(g,a,b,xl-8,xl+960); Rr=lines(g,a,b,xl+960,xl+1972)
            # title is the first L band spanning both? title is left only
            T+= [('g%d'%gi,)+t for t in L]+[('g%dR'%gi,)+t for t in Rr]
        else:
            T+= [('g%d'%gi,)+t for t in lines(g,a,b,xl-8,xl+1972)]
    # divider: single dark row between last text and NEXT
    res['text']=T
    # inside panels
    hero,b1,b2,sk,b3,foot=pn[0],pn[1],pn[2],pn[3],pn[4],pn[-1]
    ins=[]
    for nm,(y0,y1,x0,x1),pnl,thr in [('badgeA',(hero[0]+160,hero[0]+215,xl+180,xl+310),hero,120),('badgeG',(hero[0]+250,hero[0]+305,xl+180,xl+310),hero,120),
                        ('mont',(b2[0]+452,b2[0]+564,xl+710,xl+1840),b2,60),('sktitle',(sk[0]+20,sk[0]+200,xl+20,xl+830),sk,60),
                        ('capold',(b3[0]+720,b3[0]+780,xl+60,xl+300),b3,10),('capnew',(b3[0]+720,b3[0]+780,xl+1700,xl+1900),b3,20),
                        ('foot',(foot[0]+20,foot[1]-10,xl-4,xl+700),foot,30)]:
        for t in lines(g,y0,y1,x0,x1,thr): ins.append((nm,t[0]-pnl[0],t[1]-pnl[0],t[2]-xl,t[3]-xl,t[0],t[1]))
    # divider: darkest thin row in last text gap between quote and NEXT
    ga,gb=gaps[-1]
    col=g[ga:gb,xl+600:xl+1400].mean(1)
    cand=[i for i in range(len(col)) if col[i]<245 and (g[ga+i,xl+600:xl+1400]<245).mean()>0.95]
    if cand: ins.append(('divider',cand[0]+ga-foot[0],0,0,0,cand[0]+ga,cand[-1]+ga+1))
    res['inside']=ins
    return res
def group(L):
    d={}
    for t in L: d.setdefault(t[0],[]).append(t)
    return d
if __name__=='__main__':
    if '--norender' not in sys.argv: render()
    S=measure('page.png',1068); R=measure('render.png',1068)
    print('panels src',S['panels']); print('panels rnd',R['panels'])
    print('panel top diff (css):',[ (a[0]-b[0])/2 for a,b in zip(R['panels'],S['panels'])], 'bottom', [ (a[1]-b[1])/2 for a,b in zip(R['panels'],S['panels'])])
    allrows=[]
    for kind in ('text','inside'):
        gs=group(S[kind]); gr=group(R[kind])
        for k in gs:
            a=gs[k]; b=gr.get(k,[])
            if len(a)!=len(b): print('COUNT MISMATCH',k,len(a),len(b))
            for s,r in zip(a,b):
                if kind=='text': st,sb,sl,sr,rt,rb,rl,rr=s[1],s[2],s[3],s[4],r[1],r[2],r[3],r[4]
                else: st,sb,sl,sr,rt,rb,rl,rr=s[5],s[6],s[3],s[4],r[5],r[6],r[3],r[4]
                dt=(rt-st)/2; db=(rb-sb)/2; dl=(rl-sl)/2; dr=(rr-sr)/2
                allrows.append((k,st,dt,db,dl,dr))
                print('%-8s src %5d (css %7.1f) dtop %+5.1f dbot %+5.1f dxl %+5.1f dxr %+5.1f  w %d/%d'%(k,st,st/2,dt,db,dl,dr,sr-sl,rr-rl))
    import json; json.dump(allrows,open('verify_rows.json','w'))
    v=[abs(r[2]) for r in allrows]
    print('lines',len(v),'within .5:',sum(x<=0.5 for x in v),'within 1:',sum(x<=1 for x in v),'worst',max(v))
