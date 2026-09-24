import sys, xml.etree.ElementTree as ET
t=ET.fromstring(open('meta.xml').read())
F=lambda n,k: float(n.get(k,0))
def isgroup(n):
    ch=[c for c in n if not c.get('hidden')] or list(n)
    if n.tag!='frame' or not ch: return False
    x0=min(F(c,'x') for c in ch); y0=min(F(c,'y') for c in ch)
    x1=max(F(c,'x')+F(c,'width') for c in ch); y1=max(F(c,'y')+F(c,'height') for c in ch)
    ok=abs(x0-F(n,'x'))<0.02 and abs(y0-F(n,'y'))<0.02 and abs(x1-x0-F(n,'width'))<0.05 and abs(y1-y0-F(n,'height'))<0.05
    return ok and (n.get('name','').lower().startswith(('group','mask group')) or (F(n,'x')!=0 or F(n,'y')!=0))
def walk(n,px,py,d,maxd,out):
    # px,py = absolute origin of n's coordinate parent
    x=px+F(n,'x'); y=py+F(n,'y'); g=isgroup(n)
    out.append((d,n,x,y,g))
    if d<maxd:
        cx,cy=(px,py) if g else (x,y)
        for c in n: walk(c,cx,cy,d+1,maxd,out)
    return out
def section(name):
    for s in t:
        if s.get('name').startswith(name) or s.get('id')==name: return s
if __name__=='__main__':
    maxd=int(sys.argv[2]) if len(sys.argv)>2 else 3
    s=section(sys.argv[1])
    for d,n,x,y,g in walk(s,-F(s,'x'),-F(s,'y'),0,maxd,[]):
        print('  '*d+f"{n.tag[:4]}{'G' if g else ''} {n.get('id')} '{(n.get('name') or '')[:70]}' ({x:g},{y:g}) {F(n,'width'):g}x{F(n,'height'):g}"+(' HID' if n.get('hidden') else '')+(f' [{len(list(n))}ch]' if d==maxd and len(list(n)) else ''))
