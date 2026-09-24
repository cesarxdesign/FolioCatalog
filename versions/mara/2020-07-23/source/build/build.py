import json
p=json.load(open('params.json'))
C=lambda l,r:(l-1067.6)/2
def f(v): return ('%.2f'%v).rstrip('0').rstrip('.')
b1=[(1306.0,1576.58),(1609.39,1880.05),(1912.69,2183.42),(2215.97,2486.76),(2519.43,2790.03)]
b3=[(1148.21,1425.8,6279.21,'ip'),(1444.08,1721.88,6279.21,'ip'),(1740.33,2017.93,6279.21,'ip'),(2098.35,2369.19,6284.73,'an'),(2387.83,2658.61,6284.74,'an'),(2676.98,2947.81,6284.74,'an')]
w1=''.join(f'<div class="screen" style="left:{f(C(l,0))}px"><img src="img/wallet-{i+1}.webp" alt="{a}"></div>\n    ' for i,((l,r),a) in enumerate(zip(b1,["Home: balance and portfolio","Market: tokens","Send: contacts","Academy: articles","Profile"])))
w3=''.join(f'<div class="screen {k}" style="left:{f(C(l,0))}px"><img src="img/redesign-{i+1}.webp" alt="{a}"></div>\n    ' for i,((l,r,b,k),a) in enumerate(zip(b3,["Mara app 1.0: peer to peer deposit","Mara app 1.0: withdrawal amount","Mara app 1.0: send","Mara app 2.0: add funds","Mara app 2.0: withdraw","Mara app 2.0: send"])))
bd=p['badge']
html=f'''<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=1100">
<meta name="robots" content="noindex">
<title>Mara · Cesar Garcia</title>
<!-- The Mara case study as it was live on the old Squarespace site, rebuilt from screenshots
     (Figma frame "mara", captured 2024-07-07). Every length is measured from those screenshots in
     the old site's own CSS pixels (2x captures of a 2048px window). Text is live text, transcribed
     as written. The hero, the sketch board and the screen montage are crops of the screenshots,
     with the text they carried painted out and set here as live text. Phone screens are cut from
     the screenshots, each clipped to its measured box, so an original can replace one without
     moving anything. -->
<style>
@font-face{{font-family:"Inter";src:url(fonts/inter-latin.woff2) format("woff2");font-weight:100 900;font-style:normal}}
*{{box-sizing:border-box}}
p,h1,h2,h3,ul,figure,figcaption,blockquote{{margin:0}}
ul{{padding:0;list-style:none}}
img{{display:block}}
html{{background:#FFFFFF}}
body{{margin:0;background:#FFFFFF;color:#757575;
     font:11px/17px "Helvetica Neue",Helvetica,Arial,sans-serif;letter-spacing:.4px;
     -webkit-font-smoothing:antialiased}}

/* the bottom of the site header, which the capture cuts through */
.hdr{{height:24.2px;background:#FAFAFA}}
.page{{width:980px;margin:0 auto;padding-top:{f(p['pad'])}px}}

/* ---------- hero and intro ---------- */
.hero{{position:relative;height:551.5px}}
.hero img{{width:980px;height:551.5px}}
.badge{{position:absolute;left:91px;color:#FFFFFF;font-family:system-ui,-apple-system,"Helvetica Neue",sans-serif;font-weight:500;white-space:nowrap;letter-spacing:0}}
.badge span{{display:block}}
.title{{margin-top:{f(p['title_mt'])}px;font-weight:700;font-size:60px;line-height:60px;letter-spacing:.6px;color:#000}}
.intro{{display:grid;grid-template-columns:479px 479px;column-gap:22px;margin-top:{f(p['intro_mt'])}px}}
.role{{font-weight:700;font-size:13.5px;letter-spacing:.05px;color:#333}}
.meta{{margin-top:11px}}

/* ---------- text sections: a 578px column in the middle of the page ---------- */
.text{{width:578px;margin-left:201px}}
.text h2{{font-weight:700;font-size:13.5px;letter-spacing:.05px;color:#333}}
.text p{{margin-top:11px}}
.quote{{width:578px;margin-left:201px;font-style:italic;text-align:center}}

/* ---------- grey bands ---------- */
.band{{position:relative;background:#EEEEEE}}
.screen{{position:absolute;overflow:hidden;border-radius:6px;box-shadow:0 0 8px rgba(0,0,0,.1);background:#FFFFFF}}
.screen img{{width:100%;height:100%}}
.wallet{{height:403.56px}}
.wallet .screen{{top:51.4px;width:135.33px;height:300.79px}}
.redesign{{height:403.82px}}
.redesign .screen{{top:40.12px}}
.redesign .ip{{width:138.8px;height:298.46px}}
.redesign .an{{width:135.41px;height:301.22px}}
.arrow{{position:absolute;left:{f(C(1972,0))}px;top:{f((6310-5602.06)/2)}px;width:73px;height:25px}}
.cap{{position:absolute;font:500 12px/14px "Inter",sans-serif;letter-spacing:0;white-space:nowrap;top:{f(p['cap_top'])}px}}
.cap.old{{left:{f(C(1150,0)-0.9)}px;color:#D0D0D0}}
.cap.new{{right:{f(980-C(2948,0)-0.9)}px;color:#FF7302}}
.screens{{height:403.82px}}
.montage{{position:absolute;left:{f(C(1156,0))}px;top:{f((3328-3115.35)/2)}px;width:892px;height:191px}}
.montage img{{width:892px;height:191px}}
.montage p{{position:absolute;left:303.5px;width:577.8px;top:{f(p['mo_top'])}px;text-align:center;font:400 21.4px/23.5px "Inter",sans-serif;letter-spacing:0;color:#4B4B4B}}
.montage b{{font-weight:700}}

/* ---------- the sketch board ---------- */
.sketches{{position:relative;height:551.6px}}
.sketches img{{width:980px;height:551.6px}}
.sketches h2{{position:absolute;left:{f(C(1112,0)-2.5)}px;top:{f(p['sk_top'])}px;font:700 60.4px/60px "Inter",sans-serif;letter-spacing:0;color:#FA7302;white-space:nowrap}}

/* ---------- end of page ---------- */
.divider{{width:579px;height:.5px;margin:{f(p['div_mt'])}px 0 0 200.45px;background:#DDDDDD}}
.next{{display:block;width:60.65px;height:27.17px;margin:{f(p['next_mt'])}px auto 0;background:#262524;color:#FFFFFF;
      font-weight:500;font-size:8.5px;line-height:27.17px;letter-spacing:1.2px;text-align:center}}
.foot{{margin-top:{f(p['foot_mt'])}px;background:#F5F5F5;height:137.15px}}
.foot .in{{width:980px;margin:0 auto;padding-top:{f(p['foot_pt'])}px;display:grid;grid-template-columns:55.5px 72px auto}}
.foot h3{{margin:0;font-weight:700;font-size:10px;line-height:14px;letter-spacing:.15px;color:#333}}
.foot li{{font-size:8px;line-height:15.3px;letter-spacing:.05px;color:#333}}
.foot ul{{margin-top:6.6px}}
</style>
</head>
<body>
<div class="hdr"></div>
<main class="page">

  <figure class="hero"><img src="img/hero.webp" width="980" height="552" alt="Mara on two phones, Balance and Portfolio, beside the Mara logo">
    <p class="badge" style="top:{f(bd[0])}px;font-size:6.48px;line-height:9px">Download on the</p>
    <p class="badge" style="top:{f(bd[1])}px;font-size:12.67px;line-height:14px">App Store</p>
    <p class="badge" style="top:{f(bd[2])}px;font-size:5.11px;line-height:8px">GET IT ON</p>
    <p class="badge" style="top:{f(bd[3])}px;font-size:10.41px;line-height:13px">Google Play</p>
  </figure>

  <h1 class="title">Mara wallet</h1>
  <div class="intro">
    <div>
      <p class="role">Head of Product and Design</p>
      <p class="meta">Maracoin</p>
      <p class="meta">B2C Fintech, Blockchain</p>
    </div>
    <p>Led the existing design team, and expanded my responsibilities to Engineering, Marketing, and Customer Support, effectively touching all points Product. These responsibilities included sharing progress with stakeholders, and negotiating timelines. A complete change in processes and way of working, ensured our teams had a consistent and dependable delivery cadence and priorities were handled in alignment with our product roadmap.</p>
  </div>

  <figure class="band wallet" style="margin-top:{f(p['band1_mt'])}px">
    {w1}</figure>

  <section class="text" style="margin-top:{f(p['simp_mt'])}px">
    <h2>Simplify</h2>
    <p>The initial app needed an overhaul due to inconsistencies in both UI and UX, such as the navigation metaphors, how certain elements were displayed (account balance, user’s input, primary action) and overall behaviour.</p>
    <p>My first course of action was to simplify the main flows, and cut down to the bare essential screens and components.</p>
  </section>

  <figure class="band screens" style="margin-top:{f(p['band2_mt'])}px">
    <div class="montage"><img src="img/montage.webp" width="892" height="191" alt="Every onboarding screen before, 24 of them, and after, 8">
      <p>Screens: 24 down to <b>8</b><br>66% reduction</p></div>
  </figure>

  <figure class="sketches" style="margin-top:{f(p['sk_mt'])}px"><img src="img/sketches.webp" width="980" height="552" alt="The sketch board for Mara app 2.0: hand-drawn screens and notes">
    <h2>Mara app 2.0</h2></figure>

  <section class="text" style="margin-top:{f(p['full_mt'])}px">
    <h2>Full redesign</h2>
    <p>After simplifying and trimming down all major flows, the inconsistencies in the components and metaphors remained, so I took to redesign the whole app. This way I could further simplify the UX and also unify the component library, making sure each component had high reusability.</p>
  </section>

  <figure class="band redesign" style="margin-top:{f(p['band3_mt'])}px">
    {w3}<img class="arrow" src="img/arrow.webp" width="73" height="25" alt="">
    <figcaption class="cap old">Mara app 1.0</figcaption>
    <figcaption class="cap new">Mara app 2.0</figcaption>
  </figure>

  <section class="text" style="margin-top:{f(p['beyond_mt'])}px">
    <h2>Beyond the pixels</h2>
    <p>My responsibilities extended to the engineering team, as well as customer support and regular discussions with the companies executives. This ensured everyone was aligned at all times, in regards to product direction, vision, objectives, as well as deadlines and expectations.</p>
    <p>The product reached over 4 millions registered users, and established important partnerships with Coinbase and others.</p>
  </section>

  <p class="quote" style="margin-top:{f(p['quote_mt'])}px">Mara is a digital wallet for the Nigerian market, with the goal of enabling quick and free transfers between Mara users, and giving them access to crypto currencies.</p>

  <div class="divider"></div>
  <span class="next">NEXT</span>
</main>

<footer class="foot">
  <div class="in">
    <div><h3>Apps</h3><ul><li>Mara</li><li>Penfold</li><li>Done</li><li>Orbis</li></ul></div>
    <div><h3>Desktop</h3><ul><li>Audiences</li><li>Observatory</li></ul></div>
    <div><h3>Agency</h3><ul><li>Savr</li><li>Pockted</li></ul></div>
  </div>
</footer>
</body>
</html>
'''
open('site/index.html','w').write(html)
