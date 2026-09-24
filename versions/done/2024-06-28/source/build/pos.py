import xml.etree.ElementTree as ET,sys
r=ET.parse('meta.xml').getroot()
par={}
for p in r.iter():
  for c in p: par[c]=p
sections=list(r)
def rel(e):
  # section-relative coords: sum x/y of ancestors below section. Note: metadata children of groups ('contents') may already be relative to frame.
  x=float(e.get('x'));y=float(e.get('y'))
  p=par.get(e)
  while p is not None and p not in sections and p is not r:
    if p.tag in ('frame','instance','component','section'): # groups don't add offset
      x+=float(p.get('x')); y+=float(p.get('y'))
    p=par.get(p)
  return x,y
for id in sys.argv[1].split(','):
  for e in r.iter():
    if e.get('id')==id:
      x,y=rel(e); print(id, e.tag, repr(e.get('name')[:30]), 'x=%g y=%g w=%g h=%g'%(x,y,float(e.get('width')),float(e.get('height'))))
