import sys, xml.etree.ElementTree as ET
t=ET.fromstring(open('meta.xml').read())
ids=sys.argv[1].split(','); maxd=int(sys.argv[2]) if len(sys.argv)>2 else 99
def find(n,ax,ay,target):
    for c in n:
        x=ax+float(c.get('x',0)); y=ay+float(c.get('y',0))
        if c.get('id')==target: return c,x,y
        r=find(c,x,y,target)
        if r: return r
def walk(n,x,y,d,sx,sy):
    print('  '*d+f"{n.tag[:4]} {n.get('id')} '{(n.get('name') or '')[:60]}' rel({x-sx:g},{y-sy:g}) {float(n.get('width')):g}x{float(n.get('height')):g}"+(' HID' if n.get('hidden') else ''))
    if d<maxd and n.tag!='instance':
        for c in n: walk(c,x+float(c.get('x',0)),y+float(c.get('y',0)),d+1,sx,sy)
for i in ids:
    n,x,y=find(t,0,0,i)
    sec=None
    for s in t:
        sy=float(s.get('y'))
        if sy<=y< sy+float(s.get('height')) : sec=s
    print('# abs',x,y,'section',sec.get('name'))
    walk(n,x,y,0,0,float(sec.get('y')))
