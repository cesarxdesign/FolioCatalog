"""Expand {{img name|alt|extra-class|x,y override}} in index.src.html into <picture> tags from images.json."""
import json, os, re
W = os.path.dirname(os.path.abspath(__file__))
imgs = {o['name']: o for o in json.load(open(f'{W}/images.json'))}
src = open(f'{W}/index.src.html').read()
def pic(m):
    parts = m.group(1).split('|')
    name, alt = parts[0], parts[1]
    cls = parts[2] if len(parts) > 2 and parts[2] else ''
    x, y, w, h = imgs[name]['box']
    if len(parts) > 3 and parts[3]:
        x, y = [float(v) for v in parts[3].split(',')]
        x = f'{x:g}'; y = f'{y:g}'
    lazy = '' if name == 'hero' else ' loading="lazy" decoding="async"'
    fp = ' fetchpriority="high"' if name == 'hero' else ''
    return (f'<picture><source type="image/avif" srcset="img/{name}@1x.avif 1x, img/{name}.avif 2x">'
            f'<img class="a{(" " + cls) if cls else ""}" src="img/{name}.webp" srcset="img/{name}@1x.webp 1x, img/{name}.webp 2x" '
            f'alt="{alt}" width="{w}" height="{h}" style="left:{x}px;top:{y}px"{lazy}{fp}></picture>')
out = re.sub(r'\{\{img ([^}]*)\}\}', pic, src)
open(f'{W}/../site/index.html', 'w').write(out)
print('ok', len(out))
