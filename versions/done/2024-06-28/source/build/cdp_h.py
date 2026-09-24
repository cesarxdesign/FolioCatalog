#!/usr/bin/env python3
"""Headless Chrome via CDP: render site/index.html#1x from file:// at 1920 wide, DSF 1.
usage: cdp.py out.png [js_file_to_eval ...]
Prints every network request URL, then the JSON result of each JS file."""
import json, subprocess, sys, time, base64, urllib.request, os, shutil, tempfile
import websocket

CH = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
SITE = "/private/tmp/claude-501/-Users-cgair-Claude/a92997a1-610b-4dee-9a2e-79d3d6d097d6/scratchpad/done-folio-build/site/index.html"
W, H = 1920, 19325
out = sys.argv[1]
jsfiles = sys.argv[2:]
prof = tempfile.mkdtemp(dir="/private/tmp/claude-501/-Users-cgair-Claude/a92997a1-610b-4dee-9a2e-79d3d6d097d6/scratchpad")
port = 9333
p = subprocess.Popen([CH, "--headless=new", "--enable-unsafe-swiftshader", "--hide-scrollbars",
                      "--force-device-scale-factor=1", f"--window-size={W},1200",
                      f"--remote-debugging-port={port}", f"--user-data-dir={prof}",
                      "--no-first-run", "--no-default-browser-check", "about:blank"],
                     stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
try:
    for _ in range(100):
        try:
            tabs = json.load(urllib.request.urlopen(f"http://127.0.0.1:{port}/json"))
            pages = [t for t in tabs if t["type"] == "page"]
            if pages: break
        except Exception:
            pass
        time.sleep(0.2)
    ws = websocket.create_connection(pages[0]["webSocketDebuggerUrl"], timeout=120, suppress_origin=True)
    mid = [0]; events = []
    def call(method, **params):
        mid[0] += 1; my = mid[0]
        ws.send(json.dumps({"id": my, "method": method, "params": params}))
        while True:
            m = json.loads(ws.recv())
            if m.get("id") == my:
                if "error" in m: raise RuntimeError(m["error"])
                return m.get("result", {})
            events.append(m)
    call("Network.enable"); call("Page.enable"); call("Runtime.enable")
    call("Emulation.setDeviceMetricsOverride", width=W, height=H, deviceScaleFactor=1, mobile=False)
    call("Page.navigate", url="file://" + SITE + os.environ.get("HASH","#1x"))
    # wait for load, fonts and every image
    js_wait = """(async()=>{await document.fonts.ready;
      await Promise.all([...document.images].map(i=>i.complete?1:new Promise(r=>{i.onload=i.onerror=r})));
      await new Promise(r=>requestAnimationFrame(()=>requestAnimationFrame(r)));
      return [...document.images].filter(i=>!i.naturalWidth).map(i=>i.src)})()"""
    time.sleep(1.0)
    r = call("Runtime.evaluate", expression=js_wait, awaitPromise=True, returnByValue=True)
    print("broken images:", r["result"].get("value"))
    time.sleep(0.5)
    # capture in bands (a single >16k px capture wraps around the GPU texture limit)
    from PIL import Image
    import io
    full = Image.new("RGB", (W, H))
    for y0 in range(0, H, 4000):
        hh = min(4000, H - y0)
        shot = call("Page.captureScreenshot", format="png", captureBeyondViewport=True,
                    clip={"x": 0, "y": y0, "width": W, "height": hh, "scale": 1})
        full.paste(Image.open(io.BytesIO(base64.b64decode(shot["data"]))).convert("RGB"), (0, y0))
    full.save(out)
    urls = sorted({e["params"]["request"]["url"].split("#")[0] for e in events if e.get("method") == "Network.requestWillBeSent"})
    print("requests:", len(urls))
    for u in urls: print("  ", u.replace("file://" + os.path.dirname(SITE), "site"))
    for jf in jsfiles:
        r = call("Runtime.evaluate", expression=open(jf).read(), awaitPromise=True, returnByValue=True)
        print("==", os.path.basename(jf)); print(json.dumps(r["result"].get("value"), indent=None)[:20000])
finally:
    p.terminate()
    try: p.wait(5)
    except Exception: p.kill()
    shutil.rmtree(prof, ignore_errors=True)
