import json, re, sys
def code(path):
    d=json.load(open(path)); return '\n'.join(x['text'] for x in d if x['type']=='text')
def element(src, nid):
    i=src.find(f'data-node-id="{nid}"')
    if i<0: return None
    s=src.rfind('<',0,i); tag=re.match(r'<(\w+)',src[s:]).group(1)
    depth=0; pos=s
    for m in re.finditer(r'<(/?)(\w+)([^>]*?)(/?)>', src[s:]):
        if m.group(2)!=tag: continue
        if m.group(4): 
            if depth==0: return src[s:s+m.end()]
            continue
        depth += -1 if m.group(1) else 1
        if depth==0: return src[s:s+m.end()]
def texts(src):  # all text-bearing elements with a node id and a font class
    out=[]
    for m in re.finditer(r'<(p|div|span)\s+className="([^"]*font-\[[^"]*)"\s+data-node-id="([^"]+)"', src):
        out.append(m.group(3))
    return out
if __name__=='__main__':
    src=code(sys.argv[1])
    for nid in sys.argv[2:]:
        print('=====',nid); print(element(src,nid))
