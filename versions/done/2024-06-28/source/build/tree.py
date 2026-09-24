import xml.etree.ElementTree as ET,sys
r=ET.parse('meta.xml').getroot()
def f(v):
  v=float(v); return str(int(v)) if v==int(v) else '%.2f'%v
def walk(e,d,maxd):
  n=len(list(e.iter()))-1
  extra=' hidden' if e.get('hidden')=='true' else ''
  print('  '*d+f"{e.tag[:4]} {e.get('id')} '{e.get('name')[:40]}' {f(e.get('x'))},{f(e.get('y'))} {f(e.get('width'))}x{f(e.get('height'))}"+(f" [{n}]" if n else '')+extra)
  if d<maxd:
    for c in e: walk(c,d+1,maxd)
ids=sys.argv[1].split(',');maxd=int(sys.argv[2])
for e in r.iter():
  if e.get('id') in ids: walk(e,0,maxd)
