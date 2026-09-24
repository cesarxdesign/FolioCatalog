"""Minimal headless-Chrome driver over CDP: render a file:// page at 1920 x H, DPR 1, and run JS.
usage: python3 cdp.py <out.png> [js-file-to-eval -> prints JSON]"""
import json, os, subprocess, sys, tempfile, time, base64, urllib.request
import websocket

CHROME = '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome'
SITE = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'site', 'index.html'))
PORT = 9337
W, H = 1920, 25263

def run(out_png, js_files=(), hash_='#1x'):
    prof = tempfile.mkdtemp(prefix='cdp-', dir=os.path.dirname(__file__))
    p = subprocess.Popen([CHROME, '--headless=new', f'--remote-debugging-port={PORT}', f'--user-data-dir={prof}',
                          '--hide-scrollbars', '--force-device-scale-factor=1', '--enable-unsafe-swiftshader',
                          f'--remote-allow-origins=http://127.0.0.1:{PORT}', '--no-first-run', '--no-default-browser-check', f'--window-size={W},1200', 'about:blank'],
                         stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    try:
        for _ in range(100):
            try:
                tabs = json.load(urllib.request.urlopen(f'http://127.0.0.1:{PORT}/json'))
                tab = [t for t in tabs if t['type'] == 'page'][0]; break
            except Exception: time.sleep(.1)
        ws = websocket.create_connection(tab['webSocketDebuggerUrl'], max_size=None)
        mid = [0]
        def call(method, **params):
            mid[0] += 1; ws.send(json.dumps({'id': mid[0], 'method': method, 'params': params}))
            while True:
                m = json.loads(ws.recv())
                if m.get('id') == mid[0]:
                    if 'error' in m: raise RuntimeError(m['error'])
                    return m['result']
        def ev(expr):
            r = call('Runtime.evaluate', expression=expr, awaitPromise=True, returnByValue=True)
            if 'exceptionDetails' in r: raise RuntimeError(r['exceptionDetails'])
            return r['result'].get('value')
        call('Page.enable'); call('Network.enable')
        call('Emulation.setDeviceMetricsOverride', width=W, height=1200, deviceScaleFactor=1, mobile=False)
        call('Page.navigate', url='file://' + SITE + hash_)
        ev("""new Promise(r=>{const go=()=>document.fonts.ready.then(()=>{
              const imgs=[...document.images]; imgs.forEach(i=>{i.loading='eager'});
              Promise.all(imgs.map(i=>i.complete&&i.naturalWidth?1:new Promise(res=>{i.onload=i.onerror=res}))).then(()=>setTimeout(r,300))});
              document.readyState==='complete'?go():addEventListener('load',go)})""")
        res = {}
        res['broken'] = ev("[...document.images].filter(i=>!i.naturalWidth).map(i=>i.currentSrc||i.src)")
        res['srcs'] = ev("[...document.images].map(i=>i.currentSrc.split('/').pop())")
        for f in js_files:
            res[os.path.basename(f)] = ev(open(f).read())
        # capture in bands: one tall surface exceeds the GPU texture limit and comes back blank
        from PIL import Image
        import io
        full = Image.new('RGB', (W, H), (255, 0, 255))
        # scroll the 1920x1200 viewport down the page and capture what is on screen
        y = 0
        while y < H:
            h = min(1200, H - y)
            ev(f"new Promise(r=>{{scrollTo(0,{y});requestAnimationFrame(()=>requestAnimationFrame(()=>setTimeout(r,150)))}})")
            sy = ev("scrollY")
            shot = call('Page.captureScreenshot', format='png',
                        clip={'x': 0, 'y': sy, 'width': W, 'height': 1200, 'scale': 1})
            im = Image.open(io.BytesIO(base64.b64decode(shot['data']))).convert('RGB')
            off = y - sy                      # the last band: scroll stops at H-1200
            full.paste(im.crop((0, off, W, off + h)), (0, y))
            y += h
        full.save(out_png)
        ws.close()
        return res
    finally:
        p.kill(); p.wait()
        subprocess.run(['rm', '-rf', prof])

if __name__ == '__main__':
    for attempt in range(3):
        try:
            r = run(sys.argv[1], sys.argv[2:]); break
        except Exception as e:
            print('retry', e, file=sys.stderr)
    print(json.dumps(r, indent=1, ensure_ascii=False))
