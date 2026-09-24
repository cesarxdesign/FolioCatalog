import numpy as np, subprocess, os, json, sys
from PIL import Image
CH="/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
HERE=os.path.dirname(os.path.abspath(__file__))
def render(html, w, h, out):
    p=os.path.join(HERE,'test','_t.html'); open(p,'w').write(html)
    subprocess.run([CH,'--headless=new','--disable-gpu','--hide-scrollbars','--force-device-scale-factor=2',f'--window-size={w},{h}',f'--screenshot={out}','file://'+p],capture_output=True)
    return np.asarray(Image.open(out).convert('L')).astype(int)
def fit(items, size=20):
    # items: list of (text_html, css) ; each rendered at font-size=size in its own row of 60px
    rows=''.join(f'<div style="position:absolute;left:10px;top:{10+i*80}px;white-space:nowrap;font-size:{size}px;line-height:1;{css}">{t}</div>' for i,(t,css) in enumerate(items))
    html=f'''<html><head><style>@font-face{{font-family:Inter;src:url(../site/fonts/inter-latin.woff2) format('woff2');font-weight:100 900}}body{{margin:0;background:#fff;color:#000;-webkit-font-smoothing:antialiased}}</style></head><body>{rows}</body></html>'''
    g=render(html,1600,20+80*len(items),os.path.join(HERE,'test','_t.png'))
    res=[]
    for i in range(len(items)):
        R=g[(10+i*80)*2-10:(10+i*80+70)*2]; m=R<128
        xs=np.where(m.any(0))[0]; ys=np.where(m.any(1))[0]
        res.append((xs[-1]+1-xs[0], ys[-1]+1-ys[0], ys[0]-10, (255-R).sum()))
    return res
if __name__=='__main__':
    items=[('Download on the','font-family:system-ui;font-weight:500'),('App Store','font-family:system-ui;font-weight:500'),
           ('GET IT ON','font-family:system-ui;font-weight:500'),('Google Play','font-family:system-ui;font-weight:500'),
           ('Mara app 2.0','font-family:Inter;font-weight:700'),('Mara app 2.0','font-family:Inter;font-weight:600'),
           ('Screens: 24 down to <b>8</b>','font-family:Inter;font-weight:400'),('66% reduction','font-family:Inter;font-weight:400'),
           ('Mara app 1.0','font-family:Inter;font-weight:500'),('Mara app 2.0','font-family:Inter;font-weight:500')]
    tgt=[108,116,54,118,761,761,455,290,143,149]
    for it,t,r in zip(items,tgt,fit(items)):
        print(it[0][:20],it[1][-3:],'w20',r[0],'h',r[1],'-> size',round(20*t/r[0],2))
