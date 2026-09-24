import json, re, subprocess, sys, os
B='/private/tmp/claude-501/-Users-cgair-Claude/a92997a1-610b-4dee-9a2e-79d3d6d097d6/scratchpad/done-sqsp-build'
W=B+'/work'
PARAMS=W+'/params.json'
def build(p):
    t=open(W+'/template.html').read()
    b2=[(28.0,220.5,134.5,238.0),(194.0,179.0,157.5,279.5),(383.5,150.0,173.5,308.5),(589.0,118.5,157.0,340.5),(778.5,83.0,173.5,375.5)]
    names=['iPhone SE','iPhone 8','iPhone 8 Plus','iPhone X','iPhone X Max']
    alts=['Select workout on iPhone SE','Select workout on iPhone 8','Select workout on iPhone 8 Plus','Select workout on iPhone X','Select workout on iPhone XS Max']
    L=[]
    for i,(x,y,w,h) in enumerate(b2):
        cls='screen notch' if i>=3 else 'screen'
        L.append(f'    <div class="{cls}" style="left:{x:g}px;top:{y:g}px;width:{w:g}px;height:{h:g}px"><img src="img/size-{i+1}.webp" alt="{alts[i]}"></div>')
    for i,(x,y,w,h) in enumerate(b2):
        L.append(f'    <figcaption style="left:{x:g}px;width:{w:g}px">{names[i]}</figcaption>')
    p=dict(p); p['sizes']='\n'.join(L)
    def rep(m):
        k=m.group(1); v=p[k]
        return f'{v:g}' if isinstance(v,(int,float)) else str(v)
    html=re.sub(r'\{\{(\w+)\}\}',rep,t)
    assert '{{' not in html
    open(B+'/site/index.html','w').write(html)
def render(out):
    chrome='/Applications/Google Chrome.app/Contents/MacOS/Google Chrome'
    subprocess.run([chrome,'--headless=new','--disable-gpu','--hide-scrollbars','--force-device-scale-factor=2',
        '--window-size=2048,5538',f'--screenshot={out}','--virtual-time-budget=3000','file://'+B+'/site/index.html'],
        check=True,capture_output=True)
if __name__=='__main__':
    p=json.load(open(PARAMS)); build(p); render(W+'/render.png'); print('ok')
