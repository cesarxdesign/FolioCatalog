import json,subprocess,sys,numpy as np
from PIL import Image
S='/private/tmp/claude-501/-Users-cgair-Claude/a92997a1-610b-4dee-9a2e-79d3d6d097d6/scratchpad/observatory-sqsp-build'
P=np.asarray(Image.open(S+'/source/page.png').convert('L')).astype(int)[70:1173,1068:3028]
def boxes(a):
    reg=a[870:925,90:530]; m=reg>138
    out=[]
    for x0,x1 in [(0,185),(185,205),(205,440)]:
        sub=m[:,x0:x1]; ys=np.where(sub.any(1))[0]; xs=np.where(sub.any(0))[0]
        out.append((xs.min()+x0+90,xs.max()+x0+90,ys.min()+870,ys.max()+870, int(sub.sum())))
    return out
src=boxes(P)
def run(p):
    html=f'''<html><head><style>
@font-face{{font-family:WMSerif;src:url(moda.woff2)}}
@font-face{{font-family:WMSans;src:url(ibm-plex-sans-var-wordmark.woff2);font-weight:100 700}}
body{{margin:0;-webkit-font-smoothing:antialiased}}
.h{{position:relative;width:980px;height:551.5px;background:url(hero.webp) 0 0/980px 551.5px}}
.h span{{position:absolute;white-space:nowrap;color:#F6F6F6;line-height:1}}
</style></head><body><div class="h">
<span style="font-family:WMSerif;font-size:{p['s1']}px;letter-spacing:{p['l1']}px;left:{p['x1']}px;top:{p['y1']}px">STARCOUNT</span>
<span style="font-family:WMSans;font-weight:{p['w2']};font-size:{p['s2']}px;left:{p['x2']}px;top:{p['y2']}px">/</span>
<span style="font-family:WMSans;font-weight:{p['w3']};font-size:{p['s3']}px;letter-spacing:{p['l3']}px;left:{p['x3']}px;top:{p['y3']}px">OBSERVATORY</span>
</div></body></html>'''
    open('wm2.html','w').write(html)
    subprocess.run(['./render.sh',S+'/fit/wm2.html',S+'/fit/wm2.png','980','560'])
    a=np.asarray(Image.open('wm2.png').convert('L')).astype(int)[:1103]
    return boxes(a),a
p=json.loads(sys.argv[1])
r,a=run(p)
for n,s,t in zip(['star','slash','obs'],src,r):
    print(n,'src',s,'ren',t,'dx0',t[0]-s[0],'dw',(t[1]-t[0])-(s[1]-s[0]),'dy0',t[2]-s[2],'dh',(t[3]-t[2])-(s[3]-s[2]),'ink%',round(t[4]/s[4],3))
