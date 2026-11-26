/* Subscriptions v6, the live prototype (Cut page). A small app: one persistent shell (status bar, header), and a viewport under the
   header where screen bodies are mounted and pushed in and out. Every piece is cloned from the eight static screens the builder placed
   in the stage, so the look is theirs. Rates settled 2026-10-11: 1 USDC = 0.892363 EUR, 1 USDT = 0.891919 EUR, 1 USDG = 0.892478 EUR,
   1 ETH = 2237.55 EUR, 1 SOL = 98.37 EUR. Price: 29 EUR a month. */
(function(){
  function init(){
    var pr=document.querySelector('.protorow .pr'); if(!pr) return;
    var stage=pr.querySelector('.stage'), T={};
    stage.querySelectorAll('.ph').forEach(function(p){ var h=p.querySelector('.scr'); if(h&&h.shadowRoot) T[p.dataset.id.slice(-2)]=h.shadowRoot; });
    if(!T['01']||!T['08']) return;

    /* ---------- data ---------- */
    var EUR=29, TODAY='11 Oct 2026', NEXT='11 Nov 2026';
    var TOK={USDC:{name:'USD Coin',need:32.50,dp:2,ndp:2,bump:1.25,top:40},USDT:{name:'Tether',need:32.51,dp:2,ndp:2,bump:1.25,top:40},USDG:{name:'Global Dollar',need:32.49,dp:2,ndp:2,bump:1.25,top:40},
             ETH:{name:'Ether',need:0.012961,dp:4,ndp:6,bump:0.0021,top:0.02},SOL:{name:'Solana',need:0.2948,dp:4,ndp:4,bump:0.0500,top:0.5}};
    var WAL={
      'MetaMask':{addr:'0x4a…7f2c',tx:'0xa1…9e',tokens:[['USDC',{Ethereum:48.20,Arc:36.40,Solana:24.08,Polygon:0}],['USDT',{Ethereum:120.00,Polygon:41.75,Arc:12.10,Solana:0}],['USDG',{Ethereum:8.00,Solana:2.50}],['ETH',{Ethereum:0.0841,Polygon:0.0102}]]},
      'Phantom':{addr:'7xKp…3mNq',tx:'5hG2…kQ9',tokens:[['USDC',{Solana:212.40,Ethereum:35.00,Polygon:9.80}],['USDT',{Solana:60.25,Ethereum:0}],['USDG',{Solana:40.00}],['SOL',{Solana:1.8420}]]},
      'Binance Web3 Wallet':{addr:'0x9c…e41b',tx:'0x3d…b7',tokens:[['USDT',{Ethereum:305.10,Polygon:88.00,Arc:33.00,Solana:5.00}],['USDC',{Ethereum:64.00,Polygon:20.00}],['USDG',{Ethereum:0}],['ETH',{Ethereum:0.2210,Polygon:0.0510}]]}
    };
    var WORKING=['MetaMask','Phantom','Binance Web3 Wallet'];

    /* ---------- assets, read off the static screens ---------- */
    var IMG={w:{},t:{},n:{}};
    T['01'].querySelectorAll('.c137v').forEach(function(r){ IMG.w[r.querySelector('.c28h').textContent]=r.querySelector('.c27h img').src; });
    T['02'].querySelectorAll('.c150v,.c151v').forEach(function(r){ IMG.t[r.querySelector('.c28h').textContent]=r.querySelector('.c57h img').src; });
    T['03'].querySelectorAll('.c157v,.c159v').forEach(function(r){ IMG.n[r.querySelector('.c42h').textContent]=r.querySelector('img').src; });
    IMG.t.ETH=IMG.n.Ethereum; IMG.t.SOL=IMG.n.Solana;
    var PAIR0=T['04'].querySelector('.c90h img').src, HELP_OFF=T['01'].querySelector('.c133h img').src, HELP_ON=T['08'].querySelector('.c190h img').src;
    function pic(box,src,s){ box.innerHTML=''; var i=document.createElement('img'); i.className='ic'; i.alt=''; i.src=src; i.style.cssText='left:0;top:0;width:'+s+'px;height:'+s+'px'; box.appendChild(i); return i; }
    function fmt(v,dp){ return v.toFixed(dp); }

    /* ---------- the shell: one phone, built once ---------- */
    var first=stage.querySelector('.ph'), live=first.cloneNode(false); live.dataset.id='subs-live'; live.className='ph on live';
    var host=document.createElement('div'); host.className='scr'; live.appendChild(host);
    var root=host.attachShadow({mode:'open'});
    Object.keys(T).forEach(function(k){ T[k].querySelectorAll('style').forEach(function(s){ if(s.textContent.indexOf('cxr-pulse')<0) root.appendChild(s.cloneNode(true)); }); });
    var st=document.createElement('style'); st.textContent=
      /* under the header: a card. Its front is the screen (body, dock, stablecoins, terms); Support is printed on its back */
      /* the home bar is just the grabber, and the phone's frame does not clip: a turning card may bulge over the home bar and under the header */
      '.iph-hi{background:transparent!important}.iph-lay,.frame,.c49ar{overflow:visible!important}.iph-sb{position:relative;z-index:6}'+
      '.cardbox{position:relative;flex:1 1 0;min-height:0;align-self:stretch;perspective:1600px;transform-style:preserve-3d}'+
      '.card{position:absolute;left:0;top:0;width:100%;height:100%;display:flex;flex-direction:column;align-items:flex-start;background:#fff;backface-visibility:hidden;will-change:transform;transform-style:flat}.card.turning{transition:transform .52s cubic-bezier(.45,0,.2,1)}'+
      /* the reset from Success: the whole screen dissolves to white, header, clock, battery and grabber included, and Select wallet dissolves back out of it */
      '.wash{position:absolute;left:0;top:0;right:0;bottom:0;z-index:30;background:#fff;opacity:0;pointer-events:none;transition:opacity .48s cubic-bezier(.4,0,.2,1);will-change:opacity}.wash.on{opacity:1;pointer-events:auto}.wash.out{transition-duration:.56s}.inst,.inst *:not(.wash){transition:none!important}'+
      '.vp{position:relative;z-index:1;flex:1 1 0;min-height:0;align-self:stretch;overflow:visible;clip-path:inset(0 0 -48px 0);background:#fff}'+   /* clipped at the sides for the slides, open at the bottom so a button's shadow can fall past the edge */
      /* depth, bottom up: the page, the terms line, the body, the stablecoins block, the dock with its button, the header */
      '.c135v{z-index:5}.foot{position:relative;z-index:1;opacity:0;transition:opacity .36s cubic-bezier(.2,.7,.2,1);will-change:opacity}.foot-on .foot{opacity:1}'+   /* the terms line lives on 01 only; it dissolves with the stablecoins block. Success keeps its own manage line */
      '.dockL.ctaL{z-index:4}.ctaL .c74v{background:transparent;box-shadow:none;overflow:visible}.dockL:not(.ctaL) .c152v{visibility:hidden}'+
      '.mv{transition:transform .36s cubic-bezier(.2,.7,.2,1),opacity .36s cubic-bezier(.2,.7,.2,1)}'+
      '.dockL{position:absolute;left:0;right:0;bottom:0;z-index:2;display:flex;flex-direction:column;align-items:stretch;pointer-events:none;transform:translateY(calc(100% + var(--fh,0px) + 40px));transition:transform .24s cubic-bezier(.4,0,.8,.6);will-change:transform;backface-visibility:hidden}.dock-on .dockL{transform:none;transition:transform .36s cubic-bezier(.2,.7,.2,1)}'+   /* off: wholly below the screen, shadow included; it drops out quick and rises with the slide */
      /* the bottom button is one object from Select token to the end: it comes up once, with the dock, and after that only its styling dissolves */
      '.dockL.ctaL{transform:translateY(calc(100% + var(--fh,0px) + 40px));transition:transform .24s cubic-bezier(.4,0,.8,.6),opacity .3s ease}.btn-on .dockL.ctaL{transform:none;transition:transform .36s cubic-bezier(.2,.7,.2,1),opacity .3s ease}.ctaL.fadeout{opacity:0}'+
      '.slot{position:relative;flex:none;align-self:stretch;height:52px}.slot > *{position:absolute!important;left:0;right:0;top:0;pointer-events:auto;will-change:opacity}'+
      '.stablesL{position:absolute;left:22px;right:22px;z-index:1;display:flex;flex-direction:column;align-items:center;pointer-events:none;opacity:0;transition:opacity .36s cubic-bezier(.2,.7,.2,1);will-change:opacity}.stables-on .stablesL{opacity:1}'+   /* the stablecoins block stays put and dissolves; it is never pushed */
      '.view .c74v.spacer,.view .c142v.spacer{visibility:hidden}'+
      '.view .c48v,.view .c71v,.view .c74v,.view .c119v,.view .c189v{overflow:visible!important}'+   /* the screens' own containers were built with overflow hidden; here a button must float free, shadow and all */
      /* the network list flows out from under its token, and folds back under it */
      '.nwrap{align-self:stretch;overflow:hidden;flex:none}.nwrap.anim{transition:height .32s cubic-bezier(.2,.7,.2,1)}.nwrap.anim > .c88v{transition:transform .32s cubic-bezier(.2,.7,.2,1)}.nwrap.shut > .c88v{transform:translateY(-100%)}'+
      '.nclose{align-self:stretch;flex:none;overflow:hidden;margin-top:-8px;border-radius:0 0 12px 12px}'+
      '.c58h.dis{transition:opacity .32s cubic-bezier(.2,.7,.2,1)}'+
      '.wipe{display:inline-flex;overflow:hidden;white-space:nowrap;flex:none;transition:width .32s cubic-bezier(.2,.7,.2,1),margin-left .32s cubic-bezier(.2,.7,.2,1)}'+
      '.wipe.cp{position:relative;z-index:0;transition:clip-path .32s cubic-bezier(.2,.7,.2,1),opacity .32s cubic-bezier(.2,.7,.2,1)}.c155v .c144h{position:relative;z-index:1}.c67h.dis{transition:opacity .32s cubic-bezier(.2,.7,.2,1)}'+   /* RECOMMENDED wipes away rightwards-to-left and the dot follows; the preview logos dissolve in place */
      '.c156v .c57h,.c156v .c28h,.c156v .c54v{transition:opacity .32s cubic-bezier(.2,.7,.2,1)}.c156v.dimhd .c57h,.c156v.dimhd .c28h,.c156v.dimhd .c54v{opacity:.55}'+
      '.cpy{flex:none;width:22px;height:22px;display:grid;place-items:center;border-radius:6px;color:#a0a0aa;cursor:pointer;transition:color .2s ease,background .2s ease}.cpy:hover{color:#3d3b45;background:rgba(10,10,15,.05)}.cpy.done{color:#0a0a0f}'+
      '.c84h.skl > p{visibility:hidden}.skel{position:absolute;left:0;top:50%;height:10px;margin-top:-5px;border-radius:5px;background:linear-gradient(90deg,#e6e6ea 25%,#f3f3f5 50%,#e6e6ea 75%);background-size:200% 100%;animation:skm 1.1s linear infinite}@keyframes skm{from{background-position:200% 0}to{background-position:-200% 0}}.c84h.dis{transition:opacity .32s cubic-bezier(.2,.7,.2,1)}.c145h.busy{opacity:.45;transition-duration:.2s;pointer-events:none}'+
      '.c145h{transition:opacity .7s cubic-bezier(.4,0,.2,1)}.c145h.rfhide{opacity:0;pointer-events:none;transition-duration:.36s}'+   /* a calm dissolve in; the way out keeps the slide's pace */
      '.view{position:absolute;left:0;top:0;width:100%;height:100%;display:flex;flex-direction:column;align-items:flex-start;background:#fff}'+
      /* stable layers: the header, status bar and terms line each sit on their own compositing layer from the start, and so does every body view.
         Otherwise the browser creates a layer when a slide begins and re-rasterises the text around it, which reads as the header's type shifting a hair. */
      '.c135v,.iph-sb,.iph-hi,.foot{will-change:transform;transform:translateZ(0);backface-visibility:hidden}.view{will-change:transform;backface-visibility:hidden}'+
      '.c27h img,.c51h img,img.wl{border-radius:22%}'+   /* MetaMask's own art is square-cornered; every wallet logo gets the same corner */
      '[data-act]{cursor:pointer}[data-act].off{cursor:default;opacity:.35}.c137v.dis{opacity:.4}.c131h{transition:opacity .36s cubic-bezier(.2,.7,.2,1)}'+   /* Back dissolves on and off, in step with the slide */
      '.spin{animation:lvspin .9s linear infinite;transform-origin:50% 50%}@keyframes lvspin{to{transform:rotate(360deg)}}'+
      '.cf{position:relative;display:inline-block}.cf .dots{position:absolute;left:100%;top:0}'+
      '.c71v > .c34v{flex:0 1 auto;min-height:0;overflow-y:auto;scrollbar-width:none;padding-bottom:10px}.c71v > .c34v::-webkit-scrollbar{display:none}.c71v > .c34v > *{flex:none}.c71v > .c40v{display:none}'+
      '.foot{flex:none;align-self:stretch;padding:10px 22px 16px;background:#fff}.foot > *{flex:none;align-self:stretch}.view .c48v,.view .c74v{padding-bottom:0}'+   /* the terms line sits where screen 02 has it, under every body */
      '.w01 .c48v{gap:12px}.w01 .c142v{padding:2px 0}'+
      '.fly{overflow:visible!important}.fly .c129h{animation:lvbee 2s linear forwards;will-change:transform}'+
      '@keyframes lvbee{0%{transform:translate(-0.00px,-0.00px) rotate(0.00deg) rotate(-45deg) scale(1.000,1) rotate(45deg);opacity:1.00}0.5%{transform:translate(-0.01px,-0.00px) rotate(0.26deg) rotate(-45deg) scale(0.987,1) rotate(45deg);opacity:1.00}1%{transform:translate(-0.05px,-0.00px) rotate(1.03deg) rotate(-45deg) scale(0.975,1) rotate(45deg);opacity:1.00}1.5%{transform:translate(-0.11px,-0.01px) rotate(2.25deg) rotate(-45deg) scale(0.963,1) rotate(45deg);opacity:1.00}2%{transform:translate(-0.19px,-0.01px) rotate(3.90deg) rotate(-45deg) scale(0.952,1) rotate(45deg);opacity:1.00}2.5%{transform:translate(-0.29px,-0.01px) rotate(5.93deg) rotate(-45deg) scale(0.941,1) rotate(45deg);opacity:1.00}3%{transform:translate(-0.41px,-0.02px) rotate(8.29deg) rotate(-45deg) scale(0.932,1) rotate(45deg);opacity:1.00}3.5%{transform:translate(-0.54px,-0.03px) rotate(10.93deg) rotate(-45deg) scale(0.923,1) rotate(45deg);opacity:1.00}4%{transform:translate(-0.70px,-0.04px) rotate(13.82deg) rotate(-45deg) scale(0.916,1) rotate(45deg);opacity:1.00}4.5%{transform:translate(-0.86px,-0.05px) rotate(16.90deg) rotate(-45deg) scale(0.910,1) rotate(45deg);opacity:1.00}5%{transform:translate(-1.04px,-0.05px) rotate(20.13deg) rotate(-45deg) scale(0.905,1) rotate(45deg);opacity:1.00}5.5%{transform:translate(-1.22px,-0.06px) rotate(23.46deg) rotate(-45deg) scale(0.902,1) rotate(45deg);opacity:1.00}6%{transform:translate(-1.40px,-0.07px) rotate(26.84deg) rotate(-45deg) scale(0.900,1) rotate(45deg);opacity:1.00}6.5%{transform:translate(-1.59px,-0.08px) rotate(30.22deg) rotate(-45deg) scale(0.900,1) rotate(45deg);opacity:1.00}7%{transform:translate(-1.78px,-0.09px) rotate(33.55deg) rotate(-45deg) scale(0.902,1) rotate(45deg);opacity:1.00}7.5%{transform:translate(-1.96px,-0.10px) rotate(36.79deg) rotate(-45deg) scale(0.905,1) rotate(45deg);opacity:1.00}8%{transform:translate(-2.14px,-0.11px) rotate(39.88deg) rotate(-45deg) scale(0.910,1) rotate(45deg);opacity:1.00}8.5%{transform:translate(-2.30px,-0.12px) rotate(42.79deg) rotate(-45deg) scale(0.916,1) rotate(45deg);opacity:1.00}9%{transform:translate(-2.45px,-0.13px) rotate(45.47deg) rotate(-45deg) scale(0.923,1) rotate(45deg);opacity:1.00}9.5%{transform:translate(-2.59px,-0.14px) rotate(47.88deg) rotate(-45deg) scale(0.932,1) rotate(45deg);opacity:1.00}10%{transform:translate(-2.71px,-0.14px) rotate(49.97deg) rotate(-45deg) scale(0.941,1) rotate(45deg);opacity:1.00}10.5%{transform:translate(-2.81px,-0.15px) rotate(51.71deg) rotate(-45deg) scale(0.952,1) rotate(45deg);opacity:1.00}11%{transform:translate(-2.89px,-0.15px) rotate(53.05deg) rotate(-45deg) scale(0.963,1) rotate(45deg);opacity:1.00}11.5%{transform:translate(-2.95px,-0.15px) rotate(53.97deg) rotate(-45deg) scale(0.975,1) rotate(45deg);opacity:1.00}12%{transform:translate(-2.98px,-0.16px) rotate(54.43deg) rotate(-45deg) scale(0.987,1) rotate(45deg);opacity:1.00}12.5%{transform:translate(-3.00px,-0.16px) rotate(54.39deg) rotate(-45deg) scale(1.000,1) rotate(45deg);opacity:1.00}13%{transform:translate(-2.99px,-0.16px) rotate(54.07deg) rotate(-45deg) scale(1.000,1) rotate(45deg);opacity:1.00}13.5%{transform:translate(-2.97px,-0.16px) rotate(53.68deg) rotate(-45deg) scale(1.000,1) rotate(45deg);opacity:1.00}14%{transform:translate(-2.93px,-0.15px) rotate(53.25deg) rotate(-45deg) scale(1.000,1) rotate(45deg);opacity:1.00}14.5%{transform:translate(-2.88px,-0.15px) rotate(52.78deg) rotate(-45deg) scale(1.000,1) rotate(45deg);opacity:1.00}15%{transform:translate(-2.80px,-0.15px) rotate(52.28deg) rotate(-45deg) scale(1.000,1) rotate(45deg);opacity:1.00}15.5%{transform:translate(-2.71px,-0.14px) rotate(51.76deg) rotate(-45deg) scale(1.000,1) rotate(45deg);opacity:1.00}16%{transform:translate(-2.60px,-0.14px) rotate(51.24deg) rotate(-45deg) scale(1.000,1) rotate(45deg);opacity:1.00}16.5%{transform:translate(-2.46px,-0.13px) rotate(50.72deg) rotate(-45deg) scale(1.000,1) rotate(45deg);opacity:1.00}17%{transform:translate(-2.31px,-0.12px) rotate(50.22deg) rotate(-45deg) scale(1.000,1) rotate(45deg);opacity:1.00}17.5%{transform:translate(-2.13px,-0.11px) rotate(49.75deg) rotate(-45deg) scale(1.000,1) rotate(45deg);opacity:1.00}18%{transform:translate(-1.93px,-0.10px) rotate(49.32deg) rotate(-45deg) scale(1.000,1) rotate(45deg);opacity:1.00}18.5%{transform:translate(-1.70px,-0.09px) rotate(48.93deg) rotate(-45deg) scale(1.000,1) rotate(45deg);opacity:1.00}19%{transform:translate(-1.46px,-0.08px) rotate(48.61deg) rotate(-45deg) scale(1.000,1) rotate(45deg);opacity:1.00}19.5%{transform:translate(-1.19px,-0.06px) rotate(48.35deg) rotate(-45deg) scale(1.000,1) rotate(45deg);opacity:1.00}20%{transform:translate(-0.89px,-0.05px) rotate(48.16deg) rotate(-45deg) scale(1.000,1) rotate(45deg);opacity:1.00}20.5%{transform:translate(-0.58px,-0.03px) rotate(48.04deg) rotate(-45deg) scale(1.000,1) rotate(45deg);opacity:1.00}21%{transform:translate(-0.24px,-0.01px) rotate(48.00deg) rotate(-45deg) scale(1.000,1) rotate(45deg);opacity:1.00}21.5%{transform:translate(0.13px,0.01px) rotate(48.00deg) rotate(-45deg) scale(1.000,1) rotate(45deg);opacity:1.00}22%{transform:translate(0.52px,0.03px) rotate(48.00deg) rotate(-45deg) scale(1.000,1) rotate(45deg);opacity:1.00}22.5%{transform:translate(0.94px,0.05px) rotate(48.00deg) rotate(-45deg) scale(1.000,1) rotate(45deg);opacity:1.00}23%{transform:translate(1.38px,0.07px) rotate(48.00deg) rotate(-45deg) scale(1.000,1) rotate(45deg);opacity:1.00}23.5%{transform:translate(1.84px,0.10px) rotate(48.00deg) rotate(-45deg) scale(1.000,1) rotate(45deg);opacity:1.00}24%{transform:translate(2.34px,0.12px) rotate(48.00deg) rotate(-45deg) scale(1.000,1) rotate(45deg);opacity:1.00}24.5%{transform:translate(2.86px,0.15px) rotate(48.00deg) rotate(-45deg) scale(1.000,1) rotate(45deg);opacity:1.00}25%{transform:translate(3.40px,0.18px) rotate(48.00deg) rotate(-45deg) scale(1.000,1) rotate(45deg);opacity:1.00}25.5%{transform:translate(3.97px,0.21px) rotate(48.00deg) rotate(-45deg) scale(1.000,1) rotate(45deg);opacity:1.00}26%{transform:translate(4.57px,0.24px) rotate(48.00deg) rotate(-45deg) scale(1.000,1) rotate(45deg);opacity:1.00}26.5%{transform:translate(5.19px,0.27px) rotate(48.00deg) rotate(-45deg) scale(1.000,1) rotate(45deg);opacity:1.00}27%{transform:translate(5.84px,0.31px) rotate(48.00deg) rotate(-45deg) scale(1.000,1) rotate(45deg);opacity:1.00}27.5%{transform:translate(6.52px,0.34px) rotate(48.00deg) rotate(-45deg) scale(1.000,1) rotate(45deg);opacity:1.00}28%{transform:translate(7.22px,0.38px) rotate(48.00deg) rotate(-45deg) scale(1.000,1) rotate(45deg);opacity:1.00}28.5%{transform:translate(7.96px,0.42px) rotate(48.00deg) rotate(-45deg) scale(1.000,1) rotate(45deg);opacity:1.00}29%{transform:translate(8.71px,0.46px) rotate(48.00deg) rotate(-45deg) scale(1.000,1) rotate(45deg);opacity:1.00}29.5%{transform:translate(9.50px,0.50px) rotate(48.00deg) rotate(-45deg) scale(1.000,1) rotate(45deg);opacity:1.00}30%{transform:translate(10.32px,0.54px) rotate(48.00deg) rotate(-45deg) scale(1.000,1) rotate(45deg);opacity:1.00}30.5%{transform:translate(11.16px,0.58px) rotate(48.00deg) rotate(-45deg) scale(1.000,1) rotate(45deg);opacity:1.00}31%{transform:translate(12.03px,0.63px) rotate(48.00deg) rotate(-45deg) scale(1.000,1) rotate(45deg);opacity:1.00}31.5%{transform:translate(12.93px,0.68px) rotate(48.00deg) rotate(-45deg) scale(1.000,1) rotate(45deg);opacity:1.00}32%{transform:translate(13.86px,0.73px) rotate(48.00deg) rotate(-45deg) scale(1.000,1) rotate(45deg);opacity:1.00}32.5%{transform:translate(14.81px,0.78px) rotate(48.00deg) rotate(-45deg) scale(1.000,1) rotate(45deg);opacity:1.00}33%{transform:translate(15.80px,0.83px) rotate(48.00deg) rotate(-45deg) scale(1.000,1) rotate(45deg);opacity:1.00}33.5%{transform:translate(16.81px,0.88px) rotate(48.00deg) rotate(-45deg) scale(1.000,1) rotate(45deg);opacity:1.00}34%{transform:translate(17.85px,0.94px) rotate(48.00deg) rotate(-45deg) scale(1.000,1) rotate(45deg);opacity:1.00}34.5%{transform:translate(18.92px,0.99px) rotate(48.00deg) rotate(-45deg) scale(1.000,1) rotate(45deg);opacity:1.00}35%{transform:translate(20.02px,1.05px) rotate(48.00deg) rotate(-45deg) scale(1.000,1) rotate(45deg);opacity:1.00}35.5%{transform:translate(21.15px,1.11px) rotate(48.00deg) rotate(-45deg) scale(1.000,1) rotate(45deg);opacity:1.00}36%{transform:translate(22.31px,1.17px) rotate(48.00deg) rotate(-45deg) scale(1.000,1) rotate(45deg);opacity:1.00}36.5%{transform:translate(23.50px,1.23px) rotate(48.00deg) rotate(-45deg) scale(1.000,1) rotate(45deg);opacity:1.00}37%{transform:translate(24.72px,1.30px) rotate(48.00deg) rotate(-45deg) scale(1.000,1) rotate(45deg);opacity:1.00}37.5%{transform:translate(25.96px,1.36px) rotate(48.00deg) rotate(-45deg) scale(1.000,1) rotate(45deg);opacity:1.00}38%{transform:translate(27.23px,1.35px) rotate(41.42deg) rotate(-45deg) scale(1.000,1) rotate(45deg);opacity:1.00}38.5%{transform:translate(28.48px,1.20px) rotate(34.85deg) rotate(-45deg) scale(1.000,1) rotate(45deg);opacity:1.00}39%{transform:translate(29.70px,0.91px) rotate(28.30deg) rotate(-45deg) scale(1.000,1) rotate(45deg);opacity:1.00}39.5%{transform:translate(30.87px,0.49px) rotate(21.79deg) rotate(-45deg) scale(1.000,1) rotate(45deg);opacity:1.00}40%{transform:translate(31.99px,-0.07px) rotate(15.32deg) rotate(-45deg) scale(1.000,1) rotate(45deg);opacity:1.00}40.5%{transform:translate(33.02px,-0.73px) rotate(8.91deg) rotate(-45deg) scale(1.000,1) rotate(45deg);opacity:1.00}41%{transform:translate(33.96px,-1.51px) rotate(2.57deg) rotate(-45deg) scale(1.000,1) rotate(45deg);opacity:1.00}41.5%{transform:translate(34.80px,-2.36px) rotate(-3.70deg) rotate(-45deg) scale(1.000,1) rotate(45deg);opacity:1.00}42%{transform:translate(35.54px,-3.30px) rotate(-9.88deg) rotate(-45deg) scale(1.000,1) rotate(45deg);opacity:1.00}42.5%{transform:translate(36.16px,-4.29px) rotate(-15.97deg) rotate(-45deg) scale(1.000,1) rotate(45deg);opacity:1.00}43%{transform:translate(36.66px,-5.32px) rotate(-21.96deg) rotate(-45deg) scale(1.000,1) rotate(45deg);opacity:1.00}43.5%{transform:translate(37.05px,-6.38px) rotate(-27.84deg) rotate(-45deg) scale(1.000,1) rotate(45deg);opacity:1.00}44%{transform:translate(37.32px,-7.45px) rotate(-33.61deg) rotate(-45deg) scale(1.000,1) rotate(45deg);opacity:1.00}44.5%{transform:translate(37.48px,-8.52px) rotate(-39.26deg) rotate(-45deg) scale(1.000,1) rotate(45deg);opacity:1.00}45%{transform:translate(37.54px,-9.58px) rotate(-44.78deg) rotate(-45deg) scale(1.000,1) rotate(45deg);opacity:1.00}45.5%{transform:translate(37.50px,-10.62px) rotate(-50.18deg) rotate(-45deg) scale(1.000,1) rotate(45deg);opacity:1.00}46%{transform:translate(37.36px,-11.62px) rotate(-55.46deg) rotate(-45deg) scale(1.000,1) rotate(45deg);opacity:1.00}46.5%{transform:translate(37.13px,-12.58px) rotate(-60.60deg) rotate(-45deg) scale(1.000,1) rotate(45deg);opacity:1.00}47%{transform:translate(36.84px,-13.50px) rotate(-65.61deg) rotate(-45deg) scale(1.000,1) rotate(45deg);opacity:1.00}47.5%{transform:translate(36.47px,-14.36px) rotate(-70.50deg) rotate(-45deg) scale(1.000,1) rotate(45deg);opacity:1.00}48%{transform:translate(36.04px,-15.17px) rotate(-75.26deg) rotate(-45deg) scale(1.000,1) rotate(45deg);opacity:1.00}48.5%{transform:translate(35.56px,-15.92px) rotate(-79.89deg) rotate(-45deg) scale(1.000,1) rotate(45deg);opacity:1.00}49%{transform:translate(35.04px,-16.61px) rotate(-84.41deg) rotate(-45deg) scale(1.000,1) rotate(45deg);opacity:1.00}49.5%{transform:translate(34.48px,-17.24px) rotate(-88.82deg) rotate(-45deg) scale(1.000,1) rotate(45deg);opacity:1.00}50%{transform:translate(33.88px,-17.81px) rotate(-93.11deg) rotate(-45deg) scale(1.000,1) rotate(45deg);opacity:1.00}50.5%{transform:translate(33.27px,-18.33px) rotate(-97.31deg) rotate(-45deg) scale(1.000,1) rotate(45deg);opacity:1.00}51%{transform:translate(32.63px,-18.79px) rotate(-101.41deg) rotate(-45deg) scale(1.000,1) rotate(45deg);opacity:1.00}51.5%{transform:translate(31.97px,-19.19px) rotate(-105.43deg) rotate(-45deg) scale(1.000,1) rotate(45deg);opacity:1.00}52%{transform:translate(31.30px,-19.54px) rotate(-109.37deg) rotate(-45deg) scale(1.000,1) rotate(45deg);opacity:1.00}52.5%{transform:translate(30.62px,-19.84px) rotate(-113.25deg) rotate(-45deg) scale(1.000,1) rotate(45deg);opacity:1.00}53%{transform:translate(29.93px,-20.09px) rotate(-117.07deg) rotate(-45deg) scale(1.000,1) rotate(45deg);opacity:1.00}53.5%{transform:translate(29.23px,-20.29px) rotate(-120.84deg) rotate(-45deg) scale(1.000,1) rotate(45deg);opacity:1.00}54%{transform:translate(28.53px,-20.44px) rotate(-124.58deg) rotate(-45deg) scale(1.000,1) rotate(45deg);opacity:1.00}54.5%{transform:translate(27.82px,-20.55px) rotate(-128.30deg) rotate(-45deg) scale(1.000,1) rotate(45deg);opacity:1.00}55%{transform:translate(27.12px,-20.61px) rotate(-132.00deg) rotate(-45deg) scale(1.000,1) rotate(45deg);opacity:1.00}55.5%{transform:translate(26.40px,-20.62px) rotate(-135.70deg) rotate(-45deg) scale(1.000,1) rotate(45deg);opacity:1.00}56%{transform:translate(25.69px,-20.59px) rotate(-139.42deg) rotate(-45deg) scale(1.000,1) rotate(45deg);opacity:1.00}56.5%{transform:translate(24.98px,-20.51px) rotate(-143.16deg) rotate(-45deg) scale(1.000,1) rotate(45deg);opacity:1.00}57%{transform:translate(24.27px,-20.39px) rotate(-146.93deg) rotate(-45deg) scale(1.000,1) rotate(45deg);opacity:1.00}57.5%{transform:translate(23.55px,-20.21px) rotate(-150.75deg) rotate(-45deg) scale(1.000,1) rotate(45deg);opacity:1.00}58%{transform:translate(22.84px,-19.98px) rotate(-154.63deg) rotate(-45deg) scale(1.000,1) rotate(45deg);opacity:1.00}58.5%{transform:translate(22.14px,-19.71px) rotate(-158.57deg) rotate(-45deg) scale(1.000,1) rotate(45deg);opacity:1.00}59%{transform:translate(21.45px,-19.37px) rotate(-162.59deg) rotate(-45deg) scale(1.000,1) rotate(45deg);opacity:1.00}59.5%{transform:translate(20.76px,-18.98px) rotate(-166.69deg) rotate(-45deg) scale(1.000,1) rotate(45deg);opacity:1.00}60%{transform:translate(20.09px,-18.54px) rotate(-170.89deg) rotate(-45deg) scale(1.000,1) rotate(45deg);opacity:1.00}60.5%{transform:translate(19.44px,-18.03px) rotate(-175.18deg) rotate(-45deg) scale(1.000,1) rotate(45deg);opacity:1.00}61%{transform:translate(18.82px,-17.46px) rotate(-179.59deg) rotate(-45deg) scale(1.000,1) rotate(45deg);opacity:1.00}61.5%{transform:translate(18.23px,-16.83px) rotate(-184.11deg) rotate(-45deg) scale(1.000,1) rotate(45deg);opacity:1.00}62%{transform:translate(17.67px,-16.13px) rotate(-188.74deg) rotate(-45deg) scale(1.000,1) rotate(45deg);opacity:1.00}62.5%{transform:translate(17.16px,-15.37px) rotate(-193.50deg) rotate(-45deg) scale(1.000,1) rotate(45deg);opacity:1.00}63%{transform:translate(16.71px,-14.55px) rotate(-198.39deg) rotate(-45deg) scale(1.000,1) rotate(45deg);opacity:1.00}63.5%{transform:translate(16.31px,-13.67px) rotate(-203.40deg) rotate(-45deg) scale(1.000,1) rotate(45deg);opacity:1.00}64%{transform:translate(15.99px,-12.74px) rotate(-208.54deg) rotate(-45deg) scale(1.000,1) rotate(45deg);opacity:1.00}64.5%{transform:translate(15.75px,-11.76px) rotate(-213.82deg) rotate(-45deg) scale(1.000,1) rotate(45deg);opacity:1.00}65%{transform:translate(15.60px,-10.73px) rotate(-219.22deg) rotate(-45deg) scale(1.000,1) rotate(45deg);opacity:1.00}65.5%{transform:translate(15.54px,-9.67px) rotate(-224.74deg) rotate(-45deg) scale(1.000,1) rotate(45deg);opacity:1.00}66%{transform:translate(15.59px,-8.59px) rotate(-230.39deg) rotate(-45deg) scale(1.000,1) rotate(45deg);opacity:1.00}66.5%{transform:translate(15.75px,-7.50px) rotate(-236.16deg) rotate(-45deg) scale(1.000,1) rotate(45deg);opacity:1.00}67%{transform:translate(16.02px,-6.40px) rotate(-242.04deg) rotate(-45deg) scale(1.000,1) rotate(45deg);opacity:1.00}67.5%{transform:translate(16.42px,-5.32px) rotate(-248.03deg) rotate(-45deg) scale(1.000,1) rotate(45deg);opacity:1.00}68%{transform:translate(16.93px,-4.27px) rotate(-254.12deg) rotate(-45deg) scale(1.000,1) rotate(45deg);opacity:1.00}68.5%{transform:translate(17.56px,-3.27px) rotate(-260.30deg) rotate(-45deg) scale(1.000,1) rotate(45deg);opacity:1.00}69%{transform:translate(18.31px,-2.33px) rotate(-266.57deg) rotate(-45deg) scale(1.000,1) rotate(45deg);opacity:1.00}69.5%{transform:translate(19.17px,-1.46px) rotate(-272.91deg) rotate(-45deg) scale(1.000,1) rotate(45deg);opacity:1.00}70%{transform:translate(20.13px,-0.69px) rotate(-279.32deg) rotate(-45deg) scale(1.000,1) rotate(45deg);opacity:1.00}70.5%{transform:translate(21.17px,-0.02px) rotate(-285.79deg) rotate(-45deg) scale(1.000,1) rotate(45deg);opacity:1.00}71%{transform:translate(22.30px,0.52px) rotate(-292.30deg) rotate(-45deg) scale(1.000,1) rotate(45deg);opacity:1.00}71.5%{transform:translate(23.48px,0.94px) rotate(-298.85deg) rotate(-45deg) scale(1.000,1) rotate(45deg);opacity:1.00}72%{transform:translate(24.71px,1.22px) rotate(-305.42deg) rotate(-45deg) scale(1.000,1) rotate(45deg);opacity:1.00}72.5%{transform:translate(25.96px,1.36px) rotate(-312.00deg) rotate(-45deg) scale(1.000,1) rotate(45deg);opacity:1.00}73%{transform:translate(27.23px,1.42px) rotate(-312.83deg) rotate(-45deg) scale(1.000,1) rotate(45deg);opacity:1.00}73.5%{transform:translate(28.50px,1.46px) rotate(-313.64deg) rotate(-45deg) scale(1.001,1) rotate(45deg);opacity:1.00}74%{transform:translate(29.77px,1.48px) rotate(-314.44deg) rotate(-45deg) scale(1.002,1) rotate(45deg);opacity:1.00}74.5%{transform:translate(31.07px,1.48px) rotate(-315.22deg) rotate(-45deg) scale(1.003,1) rotate(45deg);opacity:1.00}75%{transform:translate(32.38px,1.47px) rotate(-315.99deg) rotate(-45deg) scale(1.004,1) rotate(45deg);opacity:1.00}75.5%{transform:translate(33.71px,1.44px) rotate(-316.75deg) rotate(-45deg) scale(1.006,1) rotate(45deg);opacity:1.00}76%{transform:translate(35.07px,1.39px) rotate(-317.51deg) rotate(-45deg) scale(1.008,1) rotate(45deg);opacity:1.00}76.5%{transform:translate(36.46px,1.32px) rotate(-318.26deg) rotate(-45deg) scale(1.011,1) rotate(45deg);opacity:1.00}77%{transform:translate(37.89px,1.22px) rotate(-319.00deg) rotate(-45deg) scale(1.014,1) rotate(45deg);opacity:1.00}77.5%{transform:translate(39.35px,1.11px) rotate(-319.75deg) rotate(-45deg) scale(1.017,1) rotate(45deg);opacity:1.00}78%{transform:translate(40.86px,0.98px) rotate(-320.49deg) rotate(-45deg) scale(1.021,1) rotate(45deg);opacity:1.00}78.5%{transform:translate(42.42px,0.82px) rotate(-321.24deg) rotate(-45deg) scale(1.025,1) rotate(45deg);opacity:1.00}79%{transform:translate(44.03px,0.63px) rotate(-321.98deg) rotate(-45deg) scale(1.029,1) rotate(45deg);opacity:1.00}79.5%{transform:translate(45.70px,0.42px) rotate(-322.73deg) rotate(-45deg) scale(1.034,1) rotate(45deg);opacity:1.00}80%{transform:translate(47.43px,0.17px) rotate(-323.47deg) rotate(-45deg) scale(1.039,1) rotate(45deg);opacity:1.00}80.5%{transform:translate(49.22px,-0.11px) rotate(-324.22deg) rotate(-45deg) scale(1.044,1) rotate(45deg);opacity:1.00}81%{transform:translate(51.08px,-0.42px) rotate(-324.97deg) rotate(-45deg) scale(1.050,1) rotate(45deg);opacity:1.00}81.5%{transform:translate(53.01px,-0.78px) rotate(-325.72deg) rotate(-45deg) scale(1.056,1) rotate(45deg);opacity:1.00}82%{transform:translate(55.02px,-1.17px) rotate(-326.47deg) rotate(-45deg) scale(1.062,1) rotate(45deg);opacity:1.00}82.5%{transform:translate(57.11px,-1.61px) rotate(-327.22deg) rotate(-45deg) scale(1.069,1) rotate(45deg);opacity:1.00}83%{transform:translate(59.28px,-2.10px) rotate(-327.97deg) rotate(-45deg) scale(1.076,1) rotate(45deg);opacity:1.00}83.5%{transform:translate(61.54px,-2.63px) rotate(-328.73deg) rotate(-45deg) scale(1.084,1) rotate(45deg);opacity:1.00}84%{transform:translate(63.89px,-3.22px) rotate(-329.48deg) rotate(-45deg) scale(1.091,1) rotate(45deg);opacity:1.00}84.5%{transform:translate(66.34px,-3.87px) rotate(-330.22deg) rotate(-45deg) scale(1.100,1) rotate(45deg);opacity:1.00}85%{transform:translate(68.88px,-4.58px) rotate(-330.97deg) rotate(-45deg) scale(1.108,1) rotate(45deg);opacity:1.00}85.5%{transform:translate(71.52px,-5.35px) rotate(-331.71deg) rotate(-45deg) scale(1.117,1) rotate(45deg);opacity:1.00}86%{transform:translate(74.26px,-6.20px) rotate(-332.45deg) rotate(-45deg) scale(1.126,1) rotate(45deg);opacity:1.00}86.5%{transform:translate(77.12px,-7.11px) rotate(-333.18deg) rotate(-45deg) scale(1.136,1) rotate(45deg);opacity:1.00}87%{transform:translate(80.08px,-8.11px) rotate(-333.90deg) rotate(-45deg) scale(1.145,1) rotate(45deg);opacity:1.00}87.5%{transform:translate(83.15px,-9.18px) rotate(-334.62deg) rotate(-45deg) scale(1.156,1) rotate(45deg);opacity:1.00}88%{transform:translate(86.34px,-10.34px) rotate(-335.33deg) rotate(-45deg) scale(1.166,1) rotate(45deg);opacity:1.00}88.5%{transform:translate(89.65px,-11.59px) rotate(-336.04deg) rotate(-45deg) scale(1.177,1) rotate(45deg);opacity:1.00}89%{transform:translate(93.08px,-12.93px) rotate(-336.73deg) rotate(-45deg) scale(1.188,1) rotate(45deg);opacity:1.00}89.5%{transform:translate(96.63px,-14.37px) rotate(-337.41deg) rotate(-45deg) scale(1.200,1) rotate(45deg);opacity:1.00}90%{transform:translate(100.31px,-15.92px) rotate(-338.09deg) rotate(-45deg) scale(1.212,1) rotate(45deg);opacity:1.00}90.5%{transform:translate(104.11px,-17.56px) rotate(-338.75deg) rotate(-45deg) scale(1.224,1) rotate(45deg);opacity:1.00}91%{transform:translate(108.05px,-19.32px) rotate(-339.40deg) rotate(-45deg) scale(1.237,1) rotate(45deg);opacity:1.00}91.5%{transform:translate(112.12px,-21.20px) rotate(-340.04deg) rotate(-45deg) scale(1.250,1) rotate(45deg);opacity:1.00}92%{transform:translate(116.33px,-23.19px) rotate(-340.67deg) rotate(-45deg) scale(1.263,1) rotate(45deg);opacity:0.99}92.5%{transform:translate(120.68px,-25.30px) rotate(-340.91deg) rotate(-45deg) scale(1.277,1) rotate(45deg);opacity:0.75}93%{transform:translate(125.20px,-27.50px) rotate(-340.91deg) rotate(-45deg) scale(1.291,1) rotate(45deg);opacity:0.50}93.5%{transform:translate(129.88px,-29.77px) rotate(-340.91deg) rotate(-45deg) scale(1.305,1) rotate(45deg);opacity:0.24}94%{transform:translate(134.74px,-32.13px) rotate(-340.91deg) rotate(-45deg) scale(1.320,1) rotate(45deg);opacity:0.00}94.5%{transform:translate(139.77px,-34.58px) rotate(-340.91deg) rotate(-45deg) scale(1.335,1) rotate(45deg);opacity:0.00}95%{transform:translate(144.98px,-37.11px) rotate(-340.91deg) rotate(-45deg) scale(1.350,1) rotate(45deg);opacity:0.00}95.5%{transform:translate(144.98px,-37.11px) rotate(-340.91deg) rotate(-45deg) scale(1.350,1) rotate(45deg);opacity:0.00}96%{transform:translate(144.98px,-37.11px) rotate(-340.91deg) rotate(-45deg) scale(1.350,1) rotate(45deg);opacity:0.00}96.5%{transform:translate(144.98px,-37.11px) rotate(-340.91deg) rotate(-45deg) scale(1.350,1) rotate(45deg);opacity:0.00}97%{transform:translate(144.98px,-37.11px) rotate(-340.91deg) rotate(-45deg) scale(1.350,1) rotate(45deg);opacity:0.00}97.5%{transform:translate(144.98px,-37.11px) rotate(-340.91deg) rotate(-45deg) scale(1.350,1) rotate(45deg);opacity:0.00}98%{transform:translate(144.98px,-37.11px) rotate(-340.91deg) rotate(-45deg) scale(1.350,1) rotate(45deg);opacity:0.00}98.5%{transform:translate(144.98px,-37.11px) rotate(-340.91deg) rotate(-45deg) scale(1.350,1) rotate(45deg);opacity:0.00}99%{transform:translate(144.98px,-37.11px) rotate(-340.91deg) rotate(-45deg) scale(1.350,1) rotate(45deg);opacity:0.00}99.5%{transform:translate(144.98px,-37.11px) rotate(-340.91deg) rotate(-45deg) scale(1.350,1) rotate(45deg);opacity:0.00}100%{transform:translate(144.98px,-37.11px) rotate(-340.91deg) rotate(-45deg) scale(1.350,1) rotate(45deg);opacity:0.00}}'+
      '.lbl{transition:opacity .3s}.lbl.out{opacity:0}'+
      '.pairimg{position:relative}.pairimg .nb{position:absolute;right:-2px;bottom:-2px;width:14px;height:14px;border-radius:50%;box-shadow:0 0 0 1.5px #fff;background:#fff;overflow:hidden}';
    root.appendChild(st);
    var app=document.createElement('div'); app.id='app'; root.appendChild(app);
    var shell=T['01'].querySelector('.iph').cloneNode(true); app.appendChild(shell);
    var ar=shell.querySelector('.c49ar'), hd=ar.querySelector('.c135v');
    [].slice.call(ar.children).forEach(function(k){ if(k!==hd) k.remove(); });
    var cardbox=document.createElement('div'), card=document.createElement('div'); cardbox.className='cardbox'; card.className='card'; ar.appendChild(cardbox); cardbox.appendChild(card);
    var vp=document.createElement('div'); vp.className='vp'; card.appendChild(vp);
    var foot=document.createElement('div'); foot.className='foot'; card.appendChild(foot);   /* the terms line: part of the shell, it never moves */
    var FOOT={terms:T['01'].querySelector('.c143v'),help:T['08'].querySelector('.c143v'),manage:T['06'].querySelector('.c182v')};
    /* the dock of Select token: one panel (behind the terms line) and its button (above them), both rise from below the screen */
    var dockL=document.createElement('div'), ctaL=document.createElement('div'); dockL.className='dockL'; ctaL.className='dockL ctaL';   /* the panel, and its button on a layer of its own (they part on the way to Confirm details) */
    [dockL,ctaL].forEach(function(L){ L.style.transition='none'; L.style.visibility='hidden'; card.appendChild(L); var d=T['02'].querySelector('.c74v').cloneNode(true); [].slice.call(d.querySelectorAll('.c143v')).forEach(function(k){ k.remove(); }); L.appendChild(d); });   /* parked without a move on the first paint */
    var slot=document.createElement('div'); slot.className='slot'; (function(){ var b=ctaL.firstChild.querySelector('.c152v'); b.parentNode.replaceChild(slot,b); })();
    var BTN={tokens:null,ready:'.c166v',signing:'.c175v',done:'.c181v',failed:'.c186v'}, ctaKey=null, ctaNext=null, ctaIn=null, ctaPark=null, STD='cubic-bezier(.2,.7,.2,1)';
    function takeCta(v){   /* lift a screen's button out of its body; the body keeps the empty place */
      ctaNext=null; if(!(S.scr in BTN)) return; var n;
      if(S.scr==='tokens') n=T['02'].querySelector('.c152v').cloneNode(true);
      else { var o=v.querySelector(BTN[S.scr]); n=o.cloneNode(true); o.style.visibility='hidden'; o.removeAttribute('data-act'); }
      ctaNext={n:n,key:S.scr+'|'+n.textContent.replace(/\.+$/,'')};
    }
    function prepCta(instant){   /* the next styling goes on top, unseen, until the move starts */
      if(!ctaNext) return; var nx=ctaNext; ctaNext=null, ctaIn=null;
      [].slice.call(slot.children).slice(0,-1).forEach(function(k){ k.remove(); });
      var old=slot.lastElementChild; if(old){ old.style.transition='none'; old.style.opacity='1'; old.style.boxShadow=''; }
      if(old&&ctaKey===nx.key) return;
      ctaKey=nx.key; var n=nx.n;
      if(!old||instant){ slot.innerHTML=''; slot.appendChild(n); return; }
      n.style.opacity='0'; slot.appendChild(n); ctaIn={n:n,old:old};
    }
    function fireCta(curve){   /* new styling dissolves in over the old; the old one's shadow fades with it; then the old is dropped */
      if(!ctaIn) return; var n=ctaIn.n, old=ctaIn.old, c=curve||STD; ctaIn=null;
      old.removeAttribute('data-act'); old.style.pointerEvents='none';
      var sh=getComputedStyle(old).boxShadow; void n.offsetWidth;
      n.style.transition='opacity .36s '+c; n.style.opacity='1';
      if(sh&&sh!=='none'){ old.style.transition='box-shadow .36s '+c; old.style.boxShadow=sh.replace(/rgba?\(([^,]+),([^,]+),([^,)]+)[^)]*\)/g,'rgba($1,$2,$3,0)'); }
      setTimeout(function(){ if(old.parentNode===slot&&slot.lastElementChild!==old) old.remove(); n.style.transition=''; },460);
    }
    function parkCta(){ ctaPark=null; ctaL.style.transition='none'; ar.classList.remove('btn-on'); ctaL.classList.remove('fadeout'); ctaL.style.visibility='hidden'; void ctaL.offsetWidth; ctaL.style.transition=''; }
    function dockPad(){ var h=foot.offsetHeight; [dockL,ctaL].forEach(function(L){ L.style.bottom=h+'px'; L.style.setProperty('--fh',h+'px'); L.firstChild.style.paddingBottom='0'; }); }   /* at rest the dock sits just above the terms line; on its way up it passes in front of them */
    var stablesL=document.createElement('div'); stablesL.className='stablesL'; stablesL.appendChild(T['01'].querySelector('.c142v').cloneNode(true)); card.appendChild(stablesL);
    var backBtn=hd.querySelector('.c131h'), backLbl=backBtn.querySelector('.c1h'), helpBtn=hd.querySelector('.c133h');
    stage.querySelectorAll('.ph').forEach(function(p){ p.style.display='none'; });
    stage.appendChild(live);

    /* ---------- state ---------- */
    var S, hist=[], timers=[];
    function fresh(){ return {scr:'wallets',wallet:null,token:null,open:false,net:null,bump:false}; }
    function snap(){ return JSON.parse(JSON.stringify(S)); }
    function clearT(){ timers.forEach(function(t){ clearTimeout(t); clearInterval(t); }); timers=[]; }
    function go(patch,fx,keep){ if(!keep) hist.push(snap()); for(var k in patch) S[k]=patch[k]; render(fx||'none'); }
    function back(){
      if(!hist.length) return; var from=S.scr;
      if(from==='tokens'){   /* from Select token or Select network, Back goes straight to Select wallet: the wallet stays connected, and whatever was selected stays selected */
        var keep=snap(); keep.scr='wallets'; hist=[]; S=keep; render('pop'); return; }
      var w=S.wallet, bp=S.bump; S=hist.pop(); if(from==='failed'&&S.scr==='signing'&&hist.length) S=hist.pop();   /* from Recovery, Back passes over Processing (Try again is what returns there) and lands on Confirm details */
      if(S.wallet===w) S.bump=bp;   /* Back never undoes a refresh */
      render(from==='help'?'flipb':(from==='ready'&&S.scr==='tokens'?'composeb':'pop'));
    }
    function reset(){ var was=S; hist=[]; S=fresh(); render(was&&(was.scr!=='wallets')?'pop':'none'); }
    var wash=document.createElement('div'), washT=[], washKeep=false; wash.className='wash'; (ar.closest('.iph')||ar).appendChild(wash);
    function washStop(){ if(!washT.length&&!wash.classList.contains('on')&&!wash.classList.contains('out')) return; washT.forEach(function(t){ clearTimeout(t); }); washT=[]; wash.style.transition='none'; wash.classList.remove('on','out'); void wash.offsetWidth; wash.style.transition=''; }
    function resetWhite(){   /* 480ms to white, a breath, 560ms back out of it; the swap happens unseen in between */
      if(washT.length) return; wash.classList.remove('out'); wash.classList.add('on');
      washT=[setTimeout(function(){
        ar.classList.add('inst'); ar.classList.remove('foot-on'); hist=[]; S=fresh(); washKeep=true; render('none'); washKeep=false; if(ctaPark) parkCta(); void ar.offsetWidth; ar.classList.remove('inst');
        washT=[setTimeout(function(){ wash.classList.add('out'); wash.classList.remove('on'); washT=[setTimeout(function(){ wash.classList.remove('out'); washT=[]; },580)]; },140)];
      },500)];
    }
    function num(){ return {wallets:1,tokens:S.open?3:2,ready:4,signing:5,done:6,failed:7,help:8}[S.scr]; }
    function toks(){ return WAL[S.wallet].tokens; }
    function bals(sym){ var t=toks().filter(function(x){return x[0]===sym;})[0][1], out=Object.keys(t).map(function(n){return [n,t[n]];}); out.sort(function(a,b){return b[1]-a[1];});
      if(S.bump){   /* the second set: a token that could pay holds a little more on its leading network; one that could not has been topped up on its smallest, which now leads */
        if(out[0][1]>=TOK[sym].need) out[0]=[out[0][0],out[0][1]+TOK[sym].bump];
        else { var lo=out[out.length-1]; out[out.length-1]=[lo[0],lo[1]+TOK[sym].top]; out.sort(function(a,b){return b[1]-a[1];}); } }
      return out; }
    function bal(){ return bals(S.token).filter(function(x){return x[0]===S.net;})[0][1]; }
    function needTxt(sym){ return fmt(TOK[sym].need,TOK[sym].ndp); }

    /* ---------- the header, updated in place ---------- */
    /* the header is one object, built once; nothing here is rewritten unless its value changed (re-setting an image's src, even to the same data, makes it flash) */
    var H={back:null,lbl:null,help:null};
    function setFoot(k){ if(foot.dataset.k===k) return; foot.dataset.k=k; foot.innerHTML=''; foot.appendChild(FOOT[k].cloneNode(true)); }
    function head(){
      var xit=isApp&&(S.scr==='wallets'||S.scr==='done'), off=!xit&&(S.scr==='wallets'||S.scr==='signing'), lbl=xit?'Exit':(S.scr==='done'?'Return':'Back'), act=xit?'exit':(S.scr==='done'?'reset':'back'), on=S.scr==='help';   /* in the prototype on a phone, the first screen and Success leave it: Exit */
      if(H.back!==off){ H.back=off; backBtn.classList.toggle('off',off); }
      if(H.lbl!==lbl){ H.lbl=lbl; backLbl.textContent=lbl; }
      if(backBtn.getAttribute('data-act')!==act) backBtn.setAttribute('data-act',act);
      if(H.help!==on){ H.help=on; helpBtn.className=on?'c190h':'c133h'; helpBtn.querySelector('img').src=on?HELP_ON:HELP_OFF; helpBtn.setAttribute('data-act',on?'back':'help'); }
    }

    /* ---------- pieces ---------- */
    function bodyOf(n){ var src=T[n].querySelector('.c49ar'), v=document.createElement('div'); v.className='view';
      [].slice.call(src.children).forEach(function(k){ if(!k.classList.contains('c135v')) v.appendChild(k.cloneNode(true)); });
      [].slice.call(v.querySelectorAll('.c143v,.c182v')).forEach(function(k){ k.remove(); }); return v; }
    function recap(el){
      var r=el.querySelector('.c147v'); pic(r.querySelector('.c51h'),IMG.w[S.wallet],26);
      r.querySelector('.c42h').textContent=S.wallet; r.querySelector('.c54v').textContent=WAL[S.wallet].addr;
      r.querySelector('.c146h').setAttribute('data-act','clearWallet'); return r;
    }
    function specs(el){
      el.querySelectorAll('.c161h,.c163h,.c164h').forEach(function(c){
        var k=c.querySelector('.c25v').textContent, v=c.querySelector('.c95h,.c95v,.c98v'), ic=c.querySelector('.c94h');
        if(k==='WALLET'){ v.textContent=S.wallet; pic(ic,IMG.w[S.wallet],18).classList.add('wl'); }
        if(k==='TOKEN'){ v.textContent=S.token; pic(ic,IMG.t[S.token],18); }
        if(k==='NETWORK'){ v.textContent=S.net; pic(ic,IMG.n[S.net],18); }
        if(k==='BALANCE') v.textContent=fmt(bal(),TOK[S.token].dp)+' '+S.token;
        if(k==='STARTED') v.textContent=TODAY;
        if(k==='NEXT CHARGE'||(k==='NEXT PAYMENT'&&S.scr!=='ready')) v.textContent=NEXT;
      });
    }
    function stack(box,sym){
      var b=bals(sym), n=b.length, show=n>3?2:n; box.innerHTML='';
      for(var i=0;i<show;i++){ var d=document.createElement('div'); d.className='c80h'+(i?' ngh600':''); pic(d,IMG.n[b[i][0]],22); box.appendChild(d); }
      if(n>3){ var p=T['02'].querySelector('.c149h').cloneNode(true); p.querySelector('.c65h').textContent='+'+(n-2); box.appendChild(p); }
    }

    /* ---------- screens: each returns the body under the header ---------- */
    function vWallets(){
      var el=bodyOf('01'); el.classList.add('w01'); el.querySelector('.c142v').classList.add('spacer');
      el.querySelectorAll('.c137v').forEach(function(r){ var nm=r.querySelector('.c28h').textContent; if(WORKING.indexOf(nm)>=0) r.setAttribute('data-act','wallet:'+nm); else r.classList.add('dis');   /* the rows that do nothing here are dimmed, a hard stop, deeper than a token that can't pay (that one still opens) */
        if(S.wallet===nm){ var d=T['03'].querySelector('.c144h').cloneNode(true); d.style.marginLeft='2px'; r.querySelector('.c28h').parentNode.appendChild(d); } });   /* still connected after Back: it carries the dot */
      return el;
    }
    var rfAt=0;
    function vTokens(){
      var el=bodyOf('03'); el.querySelector('.c74v').classList.add('spacer'); var rc=recap(el), rf=rc.querySelector('.c145h');
      /* Refresh balances is a fixture of this screen, whatever is selected. It dissolves in once the screen has finished arriving
         (coming back from Confirm details it is part of that move instead, which is the forward one in reverse) */
      rf.setAttribute('data-act','refresh');
      if(prevScr!=='tokens') rfAt=prevScr==='ready'?0:Date.now()+520;
      var rfWait=rfAt-Date.now(); if(rfWait>0){ rf.classList.add('rfhide'); timers.push(setTimeout(function(){ rf.classList.remove('rfhide'); },rfWait)); }
      var caps=el.querySelectorAll('.c136v'), ref=S.token||toks()[0][0];
      caps[1].querySelector('.c54h').textContent='need '+needTxt(ref)+(TOK[ref].dp>2?' '+ref:'')+' ≈ €'+EUR;
      var list=el.querySelector('.c71v > .c34v'), tExp=T['03'].querySelector('.c89v'), tCol=T['02'].querySelector('.c150v'), dot=T['03'].querySelector('.c144h');
      list.innerHTML='';
      toks().forEach(function(tk,i){
        var sym=tk[0], b=bals(sym), ok=b[0][1]>=TOK[sym].need, row;
        if(S.open&&S.token===sym){
          row=tExp.cloneNode(true); row.dataset.sym=sym; var hd2=row.querySelector('.c156v'); hd2.setAttribute('data-act','tok:'+sym); if(!ok) hd2.classList.add('dimhd');
          pic(hd2.querySelector('.c57h'),IMG.t[sym],32); hd2.querySelector('.c28h').textContent=sym; hd2.querySelector('.c155v').style.width='auto'; hd2.querySelector('.c54v').textContent=TOK[sym].name;
          var box=row.querySelector('.c88v'), tOn=box.querySelector('.c157v'), tOff=box.querySelector('.c159v'), hair=box.querySelector('.c158v');
          var nw=document.createElement('div'); nw.className='nwrap'; box.parentNode.insertBefore(nw,box); nw.appendChild(box);
          [].slice.call(box.querySelectorAll('.c157v,.c159v,.c158v')).forEach(function(x){ x.remove(); });
          b.forEach(function(nb,j){
            var can=nb[1]>=TOK[sym].need, r=(can?tOn:tOff).cloneNode(true); if(j) box.appendChild(hair.cloneNode(true));
            pic(r.querySelector('.c80h'),IMG.n[nb[0]],22); r.querySelector('.c42h').textContent=nb[0];
            var rec=r.querySelector('.c58h'); if(j===0&&can){ if(!rec){ rec=tOn.querySelector('.c58h').cloneNode(true); r.querySelector('.c81v').appendChild(rec); } } else if(rec) rec.remove();
            r.querySelector('.c82h').textContent=fmt(nb[1],TOK[sym].dp); r.querySelector('.c83h').textContent=sym;
            if(S.net===nb[0]){ var nd=dot.cloneNode(true); nd.style.alignSelf='center'; r.querySelector('.c81v').appendChild(nd); }   /* the selected network keeps its dot */
            if(can) r.setAttribute('data-act','net:'+nb[0]);
            box.appendChild(r);
          });
        } else {
          row=tCol.cloneNode(true); row.dataset.sym=sym; if(!ok) row.className='c151v';
          pic(row.querySelector('.c57h'),IMG.t[sym],32); row.querySelector('.c28h').textContent=sym; row.querySelector('.c54v').textContent=TOK[sym].name;
          var rec2=row.querySelector('.c58h'); if(i!==0||!ok||S.token!==null){ if(rec2) rec2.remove(); }   /* RECOMMENDED shows only while nothing is selected */
          stack(row.querySelector('.c67h'),sym);
          row.setAttribute('data-act','tok:'+sym);
        }
        list.appendChild(row);
      });
      return el;
    }
    function vReady(){
      var el=bodyOf('04'); recap(el);
      var p=el.querySelector('.c160v'), box=p.querySelector('.c90h');
      if(S.token==='USDC'&&S.net==='Ethereum') pic(box,PAIR0,30.5);
      else { box.classList.add('pairimg'); pic(box,IMG.t[S.token],28); var nb=document.createElement('div'); nb.className='nb'; pic(nb,IMG.n[S.net],14); box.appendChild(nb); }
      p.querySelector('.c42h').textContent=S.token+' on '+S.net; p.querySelector('.c91h').textContent=needTxt(S.token)+' '+S.token; p.querySelector('.c92h').textContent='≈ €'+EUR;
      p.querySelector('.c146h').setAttribute('data-act','clearPair'); specs(el);
      var c=el.querySelector('.c166v'); c.setAttribute('data-act','confirm'); pic(c.querySelector('.c80h'),IMG.w[S.wallet],22).classList.add('wl'); c.querySelector('.c104h').textContent='Confirm in '+S.wallet;
      return el;
    }
    function vSigning(){
      var el=bodyOf('05'); specs(el);
      el.querySelector('.c112v').textContent='Approving '+needTxt(S.token)+' '+S.token+' on '+S.net;
      el.querySelector('.c110h img').classList.add('spin'); el.querySelector('.c173h').setAttribute('data-act','cancel');
      var cta=el.querySelector('.c175v'); cta.style.justifyContent='center'; var p=cta.querySelector('.c72h'); p.innerHTML='<span class="cf">Confirming<span class="dots"></span></span>';
      var n=0;
      timers.push(setInterval(function(){ n=(n+1)%4; var d=slot.querySelector('.dots'); if(d) d.textContent=['','.','..','...'][n]; },420));
      if(!dead()) timers.push(setTimeout(function(){ go({scr:'done'},'push'); },6000));   /* on a phone's page the screens are pictures: it stays on Confirming */
      return el;
    }
    function vDone(){
      var el=bodyOf('06'); specs(el);
      el.querySelector('.c178v').textContent='Charged '+needTxt(S.token)+' '+S.token+' on '+S.net;
      el.querySelector('.c179v').textContent=WAL[S.wallet].tx+' ↗ · just now';
      var rb=el.querySelector('.c181v'), ck=rb.querySelector('.c94h'); ck.style.cssText='position:absolute;left:100%;top:50%;margin:-9px 0 0 10px'; rb.querySelector('.c104h').appendChild(ck);   /* the label alone is centred; the tick hangs off its right side */
      rb.setAttribute('data-act','reset'); return el;
    }
    function vFailed(){
      var el=bodyOf('07'); specs(el);
      el.querySelector('.c178v').textContent='You rejected the signature in '+S.wallet;
      el.querySelector('.c186v').setAttribute('data-act','retry'); return el;
    }
    var ICO_COPY='<svg width="12" height="12" viewBox="0 0 12 12" fill="none" stroke="currentColor" stroke-width="1.2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><rect x="4" y="4" width="6.5" height="6.5" rx="1.5"/><path d="M8 4V3a1.5 1.5 0 0 0-1.5-1.5H3A1.5 1.5 0 0 0 1.5 3v3.5A1.5 1.5 0 0 0 3 8h1"/></svg>',
        ICO_TICK='<svg width="12" height="12" viewBox="0 0 12 12" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M2.5 6.4l2.4 2.4 4.6-5.4"/></svg>';
    function vHelp(){
      var el=bodyOf('08'); el.querySelector('.c197v').setAttribute('data-act','email');
      var ref=el.querySelector('.c164h .c98v'), box=ref.parentNode; box.style.cssText+=';flex-direction:row;align-items:center;justify-content:flex-start;gap:4px;overflow:visible';   /* the reference, then its copy button */
      var cp=document.createElement('div'); cp.className='cpy'; cp.setAttribute('data-act','copyref'); cp.setAttribute('role','button'); cp.setAttribute('aria-label','Copy payment reference'); cp.innerHTML=ICO_COPY; box.appendChild(cp);
      var gap=el.querySelector('.c48v > .c40v'), xit=document.createElement('div'); xit.className='xit'; xit.setAttribute('data-act','exit'); xit.setAttribute('role','button'); xit.textContent='Exit prototype'; gap.style.cssText+=';display:flex;align-items:center;justify-content:center;overflow:visible'; gap.appendChild(xit);   /* app mode: the way back to the page, in the middle of the air between the references and the email note */
      return el;
    }
    var VIEWS={wallets:vWallets,tokens:vTokens,ready:vReady,signing:vSigning,done:vDone,failed:vFailed,help:vHelp};

    /* ---------- mounting a body: in place, or pushed in from the right (forward) or the left (back) ---------- */
    var EASE='transform .36s cubic-bezier(.2,.7,.2,1)', FLIP='transform .52s cubic-bezier(.45,0,.2,1)';
    function settle(){ [].slice.call(vp.children).slice(0,-1).forEach(function(k){ k.remove(); }); var k=vp.lastElementChild; if(k){ k.style.transition=''; k.style.transform=''; } }
    var cardB=null;   /* the back of the card: Support, while it is showing */
    function flipTo(view){   /* turn the card over to Support */
      noFlip();
      if(cardB) cardB.remove(); cardB=document.createElement('div'); cardB.className='card back'; var vp2=document.createElement('div'); vp2.className='vp'; cardB.appendChild(vp2); vp2.appendChild(view);
      cardB.style.transform='rotateY(-180deg)'; cardbox.appendChild(cardB); void cardB.offsetWidth;
      timers.push(setTimeout(function(){ card.classList.add('turning'); cardB.classList.add('turning'); card.style.transform='rotateY(180deg)'; cardB.style.transform='rotateY(0deg)'; },20));
      timers.push(setTimeout(function(){ card.classList.remove('turning'); cardB.classList.remove('turning'); },600));
    }
    function flipBack(){   /* and back to the front */
      if(!cardB) return; var b=cardB; cardB=null; noFlip();
      card.classList.add('turning'); b.classList.add('turning'); card.style.transform='rotateY(0deg)'; b.style.transform='rotateY(-180deg)';
      timers.push(setTimeout(function(){ card.classList.remove('turning'); card.style.transform=''; b.remove(); },600));
    }
    /* Select network <-> Confirm details: the wallet line stays; the list is pushed out and the details pushed in; the dock panel leaves through the bottom
       while its button dissolves into Confirm; the signature text rises from below, behind the dock, fading in */
    var REV='cubic-bezier(.8,0,.8,.3)';   /* cubic-bezier(.2,.7,.2,1), reversed in time */
    function compose(oldV,newV,fwd){
      var tokV=fwd?oldV:newV, rdyV=fwd?newV:oldV;
      var tokParts=[].slice.call(tokV.querySelectorAll('.c71v > *')).filter(function(k){ return !k.classList.contains('c147v')&&k!==tokV.querySelector('.c71v > .c136v'); });
      var rdyKids=[].slice.call(rdyV.querySelectorAll('.c48v > *')), rdyParts=rdyKids.filter(function(k){ return !k.classList.contains('c147v')&&k!==rdyV.querySelector('.c48v > .c136v')&&!k.classList.contains('c165v')&&!k.classList.contains('c166v')&&!k.classList.contains('c40v'); });
      var sig=rdyV.querySelector('.c165v'), rf=tokV.querySelector('.c145h');
      var W=vp.offsetWidth, hideWallet=[newV.querySelector('.c136v'),newV.querySelector('.c147v')], bodyBox=newV.querySelector('.c48v,.c71v');
      hideWallet.forEach(function(k){ if(k) k.style.visibility='hidden'; });   /* the new wallet line waits under the old one, pixel for pixel */
      newV.style.background='transparent'; if(bodyBox) bodyBox.style.background='transparent';   /* so the old wallet line shows through until then */
      function set(el,t,o){ el.style.transform=t; if(o!=null) el.style.opacity=o; }
      if(fwd){ rdyParts.forEach(function(k){ set(k,'translateX('+W+'px)'); }); set(sig,'translateY(110px)',0); }
      else { tokParts.forEach(function(k){ set(k,'translateX(-'+W+'px)'); }); if(rf){ rf.style.transitionDuration='.36s'; rf.classList.add('rfhide'); } dockL.style.visibility=''; }
      newV.style.transform='none'; vp.appendChild(newV);
      var all=tokParts.concat(rdyParts,[sig]); void vp.offsetWidth;
      timers.push(setTimeout(function(){
        all.forEach(function(k){ k.classList.add('mv'); });
        if(fwd){ tokParts.forEach(function(k){ set(k,'translateX(-'+W+'px)'); }); rdyParts.forEach(function(k){ set(k,'none'); }); set(sig,'none',1);
                 fireCta(); ar.classList.remove('dock-on'); if(rf) rf.classList.add('rfhide'); }
        else { all.forEach(function(k){ k.style.transitionTimingFunction=REV; });   /* every curve is the forward one run backwards */
               rdyParts.forEach(function(k){ set(k,'translateX('+W+'px)'); }); tokParts.forEach(function(k){ set(k,'none'); }); set(sig,'translateY(110px)',0);
               fireCta(REV); if(rf){ rf.style.transitionTimingFunction='cubic-bezier(.8,0,.6,1)'; rf.classList.remove('rfhide'); }
               dockL.style.transition='transform .24s cubic-bezier(.2,.4,.6,1) .12s'; ar.classList.add('dock-on'); }   /* its drop, backwards: last to move, slowing into place */
      },20));
      function end(){
        oldV.remove(); hideWallet.forEach(function(k){ if(k) k.style.visibility=''; }); newV.style.background=''; if(bodyBox) bodyBox.style.background='';
        all.forEach(function(k){ k.classList.remove('mv'); k.style.transform=''; k.style.opacity=''; k.style.transitionTimingFunction=''; });
        dockL.style.transition=''; if(rf){ rf.style.transitionDuration=''; rf.style.transitionTimingFunction=''; }
        if(fwd) dockL.style.visibility='hidden';
      }
      pendingEnd=end; timers.push(setTimeout(function(){ pendingEnd=null; end(); },440));
    }
    var pendingEnd=null;   /* a tap in the middle of the move finishes it cleanly first */
    var atStart=null;   /* something to move at the very moment the slide begins (the dock) */
    function mount(view,fx){
      settle(); var old=vp.firstElementChild;
      if(!old||fx==='none'){ vp.innerHTML=''; vp.appendChild(view); if(atStart){ atStart(); atStart=null; } return; }
      if(fx==='compose'||fx==='composeb'){ atStart=null; compose(old,view,fx==='compose'); return; }
      var ease=EASE, from=fx==='pop'?'translateX(-100%)':'translateX(100%)', to=fx==='pop'?'translateX(100%)':'translateX(-100%)', end='translateX(0)';
      view.style.transform=from; vp.appendChild(view);
      var imgs=[].slice.call(view.querySelectorAll('img')).map(function(i){ return i.decode?i.decode().catch(function(){}):Promise.resolve(); });
      var armed=false; function start(){ if(armed) return; armed=true;
        void view.offsetWidth;   /* the start position is laid out before the transition is armed */
        setTimeout(function(){
          if(atStart){ atStart(); atStart=null; }
          old.style.transition=ease; old.style.transform=to; view.style.transition=ease; view.style.transform=end;
        },20); }
      Promise.all(imgs).then(start); timers.push(setTimeout(start,120));
      timers.push(setTimeout(settle,560));
    }
    var prevScr=null, prevOpen=null;
    function unfold(wrap){ var H=wrap.offsetHeight; wrap.style.height='0px'; wrap.classList.add('shut'); void wrap.offsetWidth; wrap.classList.add('anim'); wrap.style.height=H+'px'; wrap.classList.remove('shut');
      timers.push(setTimeout(function(){ wrap.classList.remove('anim'); wrap.style.height=''; },340)); }
    function fold(box,afterRow){ var w=document.createElement('div'); w.className='nwrap nclose'; w.appendChild(box); afterRow.parentNode.insertBefore(w,afterRow.nextSibling);
      var H=w.offsetHeight; w.style.height=H+'px'; void w.offsetWidth; w.classList.add('anim'); w.style.height='0px'; w.classList.add('shut'); timers.push(setTimeout(function(){ w.remove(); },340)); }
    var REC=T['02'].querySelector('.c58h');
    function openRowFx(hd,sym,isRec){
      if(isRec){ var w=document.createElement('span'); w.className='wipe cp'; w.appendChild(REC.cloneNode(true)); var dt=hd.querySelector('.c144h'); dt.parentNode.insertBefore(w,dt.nextSibling);
        /* the label stays where it was, the dot lands on its first letters, and the label is wiped away from the dot outwards */
        w.style.marginLeft='-14px'; w.style.clipPath='inset(0 0 0 0)'; w.style.opacity='1'; void w.offsetWidth; w.style.clipPath='inset(0 0 0 100%)'; w.style.opacity='0'; timers.push(setTimeout(function(){ w.remove(); },340)); }
      var st=document.createElement('div'); st.className='c67h dis'; stack(st,sym); hd.insertBefore(st,hd.querySelector('.c6h')); void st.offsetWidth; st.style.opacity='0'; timers.push(setTimeout(function(){ st.remove(); },340));
    }
    function refreshFx(){   /* one button for the whole wallet, whatever is selected: it loads (900ms), then every balance switches to the wallet's other set */
      var v=vp.querySelector('.view'); if(!v||v.classList.contains('busy')) return; v.classList.add('busy');
      var rf=v.querySelector('.c145h'); if(rf) rf.classList.add('busy');
      function rowsOf(box){ return box?[].slice.call(box.querySelectorAll('.c157v,.c159v')):[]; }
      function nameOf(r){ return r.querySelector('.c42h').textContent; }
      function toks2(){ return [].slice.call(vp.querySelectorAll('.view .c71v > .c34v > [data-sym]')); }
      v.querySelectorAll('.c89v .c84h').forEach(function(c){ var sk=document.createElement('span'); sk.className='skel'; sk.style.width=c.offsetWidth+'px'; c.classList.add('skl'); c.appendChild(sk); });
      timers.push(setTimeout(function(){
        var pos={}, off={}, dim={}, hd0=vp.querySelector('.view .c89v .c156v'), wasDim=hd0?hd0.classList.contains('dimhd'):null;
        rowsOf(vp.querySelector('.view .c89v .c88v')).forEach(function(r){ pos[nameOf(r)]=r.offsetTop; off[nameOf(r)]=r.classList.contains('c159v'); });
        toks2().forEach(function(r){ dim[r.dataset.sym]=r.classList.contains('c151v'); });
        var patch={bump:!S.bump};
        if(S.net&&S.token){ S.bump=!S.bump; var bn=bals(S.token).filter(function(x){ return x[0]===S.net; })[0]; S.bump=!S.bump; if(!bn||bn[1]<TOK[S.token].need) patch.net=null; }   /* a network the other set can't pay with stops being the choice */
        go(patch,'none',true);
        var EZ='cubic-bezier(.2,.7,.2,1)';
        vp.querySelectorAll('.view .c89v .c84h').forEach(function(c){ c.classList.add('dis'); c.style.opacity='0'; void c.offsetWidth; c.style.opacity='1'; });
        timers.push(setTimeout(function(){ vp.querySelectorAll('.view .c89v .c84h.dis').forEach(function(c){ c.classList.remove('dis'); c.style.opacity=''; }); },360));
        /* closed token rows that changed sides dissolve between dimmed and full */
        toks2().forEach(function(r){ var k=r.dataset.sym, d=r.classList.contains('c151v'); if(r.classList.contains('c89v')||!(k in dim)||dim[k]===d) return;
          r.style.opacity=dim[k]?'.55':'1'; void r.offsetWidth; r.style.transition='opacity .4s cubic-bezier(.4,0,.2,1)'; r.style.opacity=d?'.55':'1'; timers.push(setTimeout(function(){ r.style.transition=''; r.style.opacity=''; },460)); });
        /* the open list is already in its new order: each row starts where it was, the new balances show, then rows travel to their new places */
        var box=vp.querySelector('.view .c89v .c88v'), rows=rowsOf(box), hdr=vp.querySelector('.view .c89v .c156v'), rec=box?box.querySelector('.c58h'):null, moved=false;
        var nowDim=hdr?hdr.classList.contains('dimhd'):null, flip=hdr&&wasDim!==null&&wasDim!==nowDim;
        rows.forEach(function(r){ var k=nameOf(r), dy=(pos[k]!=null?pos[k]:r.offsetTop)-r.offsetTop, o=r.classList.contains('c159v');
          if(k in off&&off[k]!==o){ r.style.opacity=off[k]?'.45':'1'; void r.offsetWidth; r.style.transition='opacity .32s '+EZ; r.style.opacity=o?'.45':'1'; }
          if(dy){ moved=true; r.style.transform='translateY('+dy+'px)'; r.style.background='#fdfcfb'; r.style.zIndex=dy>0?'2':'1'; } });
        if(flip) hdr.classList.toggle('dimhd',wasDim);
        if(moved&&rec){ rec.classList.add('dis'); rec.style.opacity='0'; }
        if(box) void box.offsetWidth;
        if(!moved&&!flip){ timers.push(setTimeout(function(){ rows.forEach(function(r){ r.style.transition=''; r.style.opacity=''; }); },360)); return; }
        timers.push(setTimeout(function(){ rows.forEach(function(r){ r.style.opacity=''; r.style.transition=r.style.transform?'transform .46s '+EZ:''; if(r.style.transform) r.style.transform='translateY(0)'; }); if(flip) hdr.classList.toggle('dimhd',nowDim); },420));
        timers.push(setTimeout(function(){ if(rec) rec.style.opacity='1'; },720));
        timers.push(setTimeout(function(){ rows.forEach(function(r){ r.style.transition=''; r.style.transform=''; r.style.zIndex=''; r.style.background=''; }); if(rec){ rec.classList.remove('dis'); rec.style.opacity=''; } },1240));
      },900));
    }
    function foldRowFx(row){
      var rec=row.querySelector('.c58h'); if(rec){ var w=document.createElement('span'); w.className='wipe cp'; rec.parentNode.insertBefore(w,rec); w.appendChild(rec);   /* the reverse: wiped back in towards where the dot was */
        w.style.clipPath='inset(0 0 0 100%)'; w.style.opacity='0'; void w.offsetWidth; w.style.clipPath='inset(0 0 0 0)'; w.style.opacity='1'; timers.push(setTimeout(function(){ w.parentNode.insertBefore(rec,w); w.remove(); },340)); }
      var st=row.querySelector('.c67h'); if(st){ st.classList.add('dis'); st.style.opacity='0'; void st.offsetWidth; st.style.opacity='1'; timers.push(setTimeout(function(){ st.classList.remove('dis'); st.style.opacity=''; },340)); }
    }
    function render(fx){
      if(pendingEnd){ var pe=pendingEnd; pendingEnd=null; pe(); }
      if(!washKeep) washStop();
      if(ctaPark) parkCta();
      var oldView=vp.querySelector('.view'), oldBox=(prevScr==='tokens'&&oldView)?oldView.querySelector('.c89v .c88v'):null;
      clearT(); head(); var v=VIEWS[S.scr](); takeCta(v); dockPad();
      if(fx==='flip'){ flipTo(v); prevScr=S.scr; sync(); return; }
      if(fx==='flipb'){ flipBack(); if(cardB===null&&vp.querySelector('.view')) { prevScr=S.scr; prevOpen=S.open?S.token:null; sync(); return; } }
      var base=S.scr==='help'?(hist.length?hist[hist.length-1].scr:'wallets'):S.scr;
      var wantDock=base==='tokens', wantSt=base==='wallets', wantFoot=base==='wallets'?'terms':(base==='done'?'manage':null), footOn=ar.classList.contains('foot-on');
      if(!footOn&&wantFoot) setFoot(wantFoot);   /* swap while invisible */
      var footLater=footOn&&wantFoot&&foot.dataset.k!==wantFoot;   /* one line fades out, the other fades in after it */
      if(footLater) timers.push(setTimeout(function(){ setFoot(wantFoot); ar.classList.add('foot-on'); },400));
      var wantBtn=(base in BTN), hadBtn=ar.classList.contains('btn-on'), hadDock=ar.classList.contains('dock-on');
      if(S.scr!=='help') prepCta(fx==='none'||!hadBtn);
      atStart=function(){
        if(wantDock) dockL.style.visibility='';
        ar.classList.toggle('dock-on',wantDock); ar.classList.toggle('stables-on',wantSt); ar.classList.toggle('foot-on',!!wantFoot&&!footLater);
        if(!wantDock) timers.push(setTimeout(function(){ if(!ar.classList.contains('dock-on')) dockL.style.visibility='hidden'; },300));
        if(wantBtn&&!hadBtn){ ctaL.style.visibility='';
          if(wantDock) ar.classList.add('btn-on');   /* the one time it travels: up, with the dock */
          else { ctaL.style.transition='none'; ctaL.classList.add('fadeout'); ar.classList.add('btn-on'); void ctaL.offsetWidth; ctaL.style.transition=''; ctaL.classList.remove('fadeout'); } }
        else if(!wantBtn&&hadBtn){
          if(hadDock){ ar.classList.remove('btn-on'); timers.push(setTimeout(function(){ if(!ar.classList.contains('btn-on')) ctaL.style.visibility='hidden'; },300)); }   /* back to Select wallet: down with the dock, the way it came */
          else { ctaL.classList.add('fadeout'); ctaPark=parkCta; timers.push(setTimeout(function(){ if(ctaPark) parkCta(); },320)); } }   /* a reset from further on: it dissolves where it stands */
        fireCta();
      };
      mount(v,fx);
      var sp=v.querySelector('.c142v.spacer'); if(sp) stablesL.style.top=(vp.offsetTop+sp.offsetTop)+'px';
      if(fx==='none'&&prevScr==='tokens'&&S.scr==='tokens'){   /* a token opened, folded or switched: the lists move, the screen does not */
        var nowOpen=S.open?S.token:null;
        var recSym=toks()[0][0], rr=v.querySelector('.c71v > .c34v > .c150v[data-sym="'+recSym+'"]');
        if(nowOpen&&nowOpen!==prevOpen){ var nwp=v.querySelector('.c89v .nwrap'); if(nwp) unfold(nwp); var hd2=v.querySelector('.c89v .c156v'); if(hd2) openRowFx(hd2,nowOpen,prevOpen===null&&nowOpen===recSym); }
        if(rr&&prevOpen===null&&nowOpen&&nowOpen!==recSym){ var lab=REC.cloneNode(true); lab.classList.add('dis'); rr.querySelector('.c59v').appendChild(lab); void lab.offsetWidth; lab.style.opacity='0'; timers.push(setTimeout(function(){ lab.remove(); },340)); }   /* another token selected: RECOMMENDED dissolves out */
        if(rr&&prevOpen&&prevOpen!==recSym&&nowOpen===null){ var lab2=rr.querySelector('.c58h'); if(lab2){ lab2.classList.add('dis'); lab2.style.opacity='0'; void lab2.offsetWidth; lab2.style.opacity='1'; timers.push(setTimeout(function(){ lab2.classList.remove('dis'); lab2.style.opacity=''; },340)); } }   /* deselected: it dissolves back in */
        if(prevOpen&&prevOpen!==nowOpen&&oldBox){ var row=v.querySelector('.c71v > .c34v > [data-sym="'+prevOpen+'"]'); if(row){ fold(oldBox,row); foldRowFx(row); } }
      }
      prevScr=S.scr; prevOpen=S.open?S.token:null;
      var ex=v.querySelector('.c71v > .c34v > .c89v'); if(ex){ var l=ex.parentNode, over=ex.offsetTop+ex.offsetHeight-l.offsetTop-l.clientHeight+10; if(over>0) l.scrollTop=over; }
      sync();
    }

    /* ---------- taps inside the phone ---------- */
    app.addEventListener('click',function(e){
      var el=e.target.closest?e.target.closest('[data-act]'):null; if(!el||el.classList.contains('off')) return;
      var a=el.getAttribute('data-act'), i=a.indexOf(':'), k=i<0?a:a.slice(0,i), v=i<0?'':a.slice(i+1);
      if(k==='back') back();
      else if(k==='reset'){ if(S.scr==='done') resetWhite(); else reset(); }
      else if(k==='help') go({scr:'help'},'flip');
      else if(k==='wallet'){ if(v===S.wallet) go({scr:'tokens'},'push'); else go({scr:'tokens',wallet:v,token:null,open:false,net:null,bump:false},'push'); }   /* the wallet that is still connected comes back as it was left; another one starts clean */
      else if(k==='clearWallet') reset();
      else if(k==='tok'){ if(S.token===v) go({token:null,open:false,net:null}); else go({token:v,open:true,net:null}); }   /* tap selects and opens; tap again deselects; tap another switches */
      else if(k==='refresh') refreshFx();
      else if(k==='net'){ S.net=v; go({scr:'ready',open:false},'compose'); }   /* the choice is made on this screen, so Back finds it selected; tapping it again just moves on */
      else if(k==='clearPair') go({scr:'tokens',token:null,net:null,open:false},'composeb');
      else if(k==='confirm') go({scr:'signing'},'push');
      else if(k==='cancel') go({scr:'failed'},'push');
      else if(k==='retry'){ if(hist.length&&hist[hist.length-1].scr==='signing') S=hist.pop(); else S.scr='signing'; render('pop'); }   /* the same selection, straight back into Processing */
      else if(k==='email') email(el);
      else if(k==='exit') exitApp();
      else if(k==='copyref'){   /* copies the reference; the icon turns to a tick for a moment */
        var tx=el.parentNode.querySelector('.c98v').textContent; try{ if(navigator.clipboard) navigator.clipboard.writeText(tx).catch(function(){}); }catch(err){}
        if(!el.classList.contains('done')){ el.classList.add('done'); el.innerHTML=ICO_TICK; timers.push(setTimeout(function(){ el.classList.remove('done'); el.innerHTML=ICO_COPY; },1400)); } }
    });
    function email(btn){
      if(btn.classList.contains('busy')) return; btn.classList.add('busy','fly');
      var lab=btn.querySelector('.c104h'), plane=btn.querySelector('.c129h'); lab.classList.add('lbl');
      timers.push(setTimeout(function(){ plane.style.display='none'; lab.textContent='Emailed'; },2000));   /* the plane's slot goes with it, so the word sits dead centre */
      timers.push(setTimeout(function(){ if(S.scr==='help') back(); },2700));   /* a beat on "Emailed", then out of Support the way a tap on Back leaves it: the card flips back */
    }

    /* ---------- beside the screen: its name, and what each part of it does ---------- */
    var INFO=[
      ['Start, select wallet',[
        ['Selection','Pick one of the first 3 wallets.',1],
        ['No back','Back would return to the merchant platform, with optional confirmation step.']]],
      ['Select token',[
        ['Selection','Pick any token to reveal network. This is fed by the user’s wallet balance so the same token can be held on multiple networks. Sorted by balance, except for the 3 stablecoins which are pinned on top.',1],
        ['Refresh balances','Fetches latest balances on the wallet. A single round trip updates all tokens.',1],
        ['Disconnect','X disconnects wallet and returns to initial screen. Back navigates to previous, keeping the network selection as a user may just want to double check the other options, without committing to change.',1]]],
      ['Select network',[
        ['Selection','Select a network with enough balance to cover payment.',1],
        ['Recommended','All enabled tokens will have a recommended network. Only one token will be recommended. (Criteria for what’s recommended can be adjusted by the merchant.)'],
        ['Disabled','A disabled token means the user holds this token, but without enough balance on any given network to cover the payment. We display it as a courtesy shortcut. If they go onto their wallet and top up, a tap on refresh balances should reflect the update.']]],
      ['Confirm details',[
        ['Confirm','A constant in all my transaction work is to give the user a beat to preview and calmly commit. Often in design the goal is to remove friction, but I find that with payments, the added moment has never really backfired with data showing a massive drop-off, or support tickets shouting at the extra tap. For the most part I believe users appreciate the reassurance it affords.',1]]],
      ['Processing',[
        ['Cancel','Tapping Cancel here shows the recovery and retry state.','!']]],
      ['Success',[
        ['Return','Handoff back to the merchant.',1]]],
      ['Recovery',[
        ['Try again','Loads the exact same selection and parameters into payment, and retries it for the user. We debated multiple behaviours based on the exception, like retry on rejected signature, but restart selection on insufficient balance, but decided on a single edge case mapping for launch.',1],
        ['Back',['Complements the decision to keep the mapping simple. If the user taps try again to the same result (what we’d potentially avoid by adapting behaviour to the exception) they always have the option to go back.','For most mobile web projects, I always consider the benefits of repeating navigation elements, which may be tuned to provide an enhanced experience. But a large number of users will just swipe from the screen’s edge, or use the browser’s UI to trigger an OS level event, which is a behaviour I can’t control and so I have to make sure the experience is also guaranteed in that scenario, albeit not enhanced.']]]],
      ['Support',[
        ['Email','This triggers a Zendesk form and sends off the user’s message complete with session ID and all the other relevant technical details, including the payment reference. I kept the small note on the bottom asking for it because I find it helps the user get the message started.',1]]]
    ];
    var side=pr.querySelector('.side'), strip=pr.querySelector('.steps');
    [].slice.call(strip.querySelectorAll('.arr')).forEach(function(x){ x.remove(); });
    pr.appendChild(strip); if(side) side.remove();
    var pinfo=document.createElement('div'); pinfo.className='pinfo'; pr.insertBefore(pinfo,strip);
    var pbox=document.createElement('div'); pbox.className='pbox'; pinfo.appendChild(pbox);
    function infoHtml(n){ var d=INFO[n-1], h='<p class="pt">'+d[0]+'</p><div class="st-list">';
      d[1].forEach(function(x,i){ h+='<div class="st-row"><span class="st-n'+(x[2]==='wip'?' wip':(x[2]==='!'?' bang':(x[2]?' hi':'')))+'">'+(x[2]==='wip'?'':(x[2]==='!'?'!':(i<9?'0':'')+(i+1)))+'</span><span class="st-tx"><span class="st-t">'+x[0].replace(/\.$/,'')+'</span>'+[].concat(x[1]).filter(Boolean).map(function(b){ return '<span class="st-b">'+b+'</span>'; }).join('')+'</span></div>'; });
      return h+'</div>'; }
    function info(n){   /* the name and the list dissolve from one screen's to the next, in step with the slide */
      var nx=document.createElement('div'); nx.className='pi'; nx.innerHTML=infoHtml(n);
      var old=pbox.querySelector('.pi:not(.pi-out)'); [].slice.call(pbox.querySelectorAll('.pi-out')).forEach(function(k){ k.remove(); });
      if(!old){ pbox.appendChild(nx); return; }
      old.classList.add('pi-out'); nx.classList.add('pi-in'); pbox.appendChild(nx);
      requestAnimationFrame(function(){ requestAnimationFrame(function(){ old.classList.add('gone'); nx.classList.remove('pi-in'); }); });
      setTimeout(function(){ old.remove(); },400);
    }

    /* ---------- the strip, reset, the maximised view ---------- */
    function rbtn(cls,label,svg){ var b=document.createElement('button'); b.type='button'; b.className=cls+' rsbtn'; b.setAttribute('aria-label',label);
      b.innerHTML='<svg width="16" height="16" viewBox="0 0 16 16" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">'+svg+'</svg>'; return b; }
    var rs=rbtn('restart','Back to the first screen','<path d="M2.5 8a5.5 5.5 0 1 0 1.7-4"/><path d="M2.5 2.5v3.2h3.2"/>');
    var ICO_IN='<path d="M9.5 2.5h4v4"/><path d="M13.5 2.5L9 7"/><path d="M6.5 13.5h-4v-4"/><path d="M2.5 13.5L7 9"/>', ICO_OUT='<path d="M13 7H9V3"/><path d="M9 7l4.5-4.5"/><path d="M3 9h4v4"/><path d="M7 9l-4.5 4.5"/>';
    var fsb=rbtn('fsbtn','Full screen',ICO_IN);
    rs.setAttribute('data-key','R'); rs.title='Reset (R)'; fsb.setAttribute('data-key','F'); fsb.title='Maximise (F)';   /* the key that does the same, shown above each */
    var fsx=document.createElement('button'); fsx.type='button'; fsx.className='fsx'; fsx.setAttribute('aria-label','Exit full screen');
    fsx.innerHTML='<svg width="28" height="28" viewBox="0 0 28 28" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" aria-hidden="true"><path d="M6 6l16 16M22 6L6 22"/></svg>'; pr.appendChild(fsx);
    var pbtns=document.createElement('div'); pbtns.className='pbtns'; pr.appendChild(pbtns);
    var zoom=document.createElement('div'); zoom.className='fszoom';   /* maximised only: top left, + and − step the screen's size */
    zoom.innerHTML='<button type="button" class="zb zminus" aria-label="Smaller screen"><svg width="28" height="28" viewBox="0 0 28 28" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" aria-hidden="true"><path d="M7 14h14"/></svg></button><button type="button" class="zb zplus" aria-label="Larger screen"><svg width="28" height="28" viewBox="0 0 28 28" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" aria-hidden="true"><path d="M7 14h14M14 7v14"/></svg></button>';
    pr.appendChild(zoom);
    var PW0=stage.style.getPropertyValue('--pw')||'367', IW=402, IH=874, isFs=false, fsZoom=0.8;   /* 0.8 = 20% under the largest that fits */
    function stepZoom(d){ fsZoom=Math.min(1,Math.max(0.4,Math.round((fsZoom+d)*10)/10)); zoom.querySelector('.zplus').disabled=fsZoom>=1; zoom.querySelector('.zminus').disabled=fsZoom<=0.4; size(); keep(); }
    function place(){ if(isFs){ strip.insertBefore(rs,strip.firstChild); strip.appendChild(fsb); } else { pbtns.appendChild(rs); pbtns.appendChild(fsb); } }   /* on the page: beside the screen, under the notes; maximised: either side of the strip */
    /* maximised: an overlay over the page (the page stays behind it, blurred), whatever size the window is; the screen 20% under the largest that fits, the strip mid-way in the air below it */
    var mpw=0;   /* the screen's width on a phone's page; 0 elsewhere */
    function size(){
      var pw=(mpw&&!isFs)?mpw:PW0; if(isFs){ var h=(window.innerHeight-2*(strip.offsetHeight+64))*fsZoom, w=window.innerWidth-2*(64+300); pw=Math.max(220,Math.floor(Math.min(h*IW/IH,w)));
        var H=window.innerHeight, ph=pw*IH/IW, band=Math.floor((H-ph)/2), sh=strip.offsetHeight; pr.style.setProperty('--band',band+'px');
        var mid=((H-band/2-sh/2)-ph)/2; pr.style.setProperty('--lift',Math.round(0.6*(band-mid))+'px'); }   /* lifted most of the way to the middle of the space above the strip; the rest is a deliberate downward bias */
      [stage,live].forEach(function(el){ el.style.setProperty('--pw',pw); }); alignTitle();
    }
    function capTop(el){ var g=document.createRange(); g.selectNodeContents(el); var r=g.getClientRects()[0]||el.getBoundingClientRect(); return r.top+0.2*r.height; }   /* the top of the capitals and digits: Inter's sit a fifth of the way down its text box */
    function alignTitle(){   /* the screen's name starts level with the top of the price, the 29; the first note's title starts level with the bottom of the header inside the screen */
      var cur=pinfo.querySelector('.pi:not(.pi-out)')||pinfo, pt=cur.querySelector('.pt'), t=cur.querySelector('.st-t'), price=root.querySelector('.c19h'); if(!pt||!t) return;
      pinfo.style.paddingTop='0px'; pt.style.marginBottom=''; if(dead()) return;   /* on a phone's page the notes start level with the top of the screen */
      if(price) pinfo.style.paddingTop=Math.max(0,Math.round((capTop(price)-capTop(pt))*10)/10)+'px';
      var mb=parseFloat(getComputedStyle(pt).marginBottom)||0, d=hd.getBoundingClientRect().bottom-capTop(t); pt.style.marginBottom=Math.max(4,Math.round((mb+d)*10)/10)+'px';
    }
    function keep(){ try{ sessionStorage.setItem('subs.fs',JSON.stringify({fs:isFs,z:fsZoom,n:num()})); }catch(e){} }   /* survives a reload of the page, so edits land in the open view */
    function setFs(on){
      isFs=on; pr.classList.toggle('fs',on); place(); document.documentElement.style.overflow=on?'hidden':'';
      fsb.setAttribute('aria-label',on?'Exit full screen':'Full screen'); fsb.querySelector('svg').innerHTML=on?ICO_OUT:ICO_IN; size(); relayout(); keep();
    }
    place();
    window.addEventListener('resize',function(){ if(isFs) size(); });
    /* R resets and F maximises, but only while the prototype is on screen: any part of the phone, plus a 10% margin all round it, or the maximised view open.
       Anywhere else on the page the keys are left alone. Esc closes the maximised view; Cmd+R still reloads. */
    function protoInView(){ var r=stage.getBoundingClientRect(), mx=r.width*0.1, my=r.height*0.1; return r.bottom+my>0&&r.top-my<window.innerHeight&&r.right+mx>0&&r.left-mx<window.innerWidth; }   /* any part of the phone on screen counts, and so does a 10% margin all round it */
    document.addEventListener('keydown',function(e){
      if(e.metaKey||e.ctrlKey||e.altKey||e.repeat) return; var t=e.target, tag=t&&t.tagName; if(tag==='INPUT'||tag==='TEXTAREA'||tag==='SELECT'||(t&&t.isContentEditable)) return;
      if(isFs&&e.key==='Escape'){ setFs(false); return; }
      if(!isFs&&!protoInView()) return;
      var k=(e.key||'').toLowerCase(); if(k==='r'){ e.preventDefault(); reset(); } else if(k==='f'){ e.preventDefault(); setFs(!isFs); }
    });
    var jumps=[].slice.call(pr.querySelectorAll('.steps .st')), shown=0;
    /* on the page, the reset block stands over the 7th screen of the strip and the maximise block over the 8th, centre on centre */
    function alignBtns(){
      if(isFs||jumps.length<8){ pbtns.style.cssText=''; [rs,fsb].forEach(function(b){ b.style.position=''; b.style.left=''; b.style.top=''; }); return; }
      pbtns.style.cssText='position:relative;display:block;height:36px;padding-left:0'; var pb=pbtns.getBoundingClientRect();
      [[rs,jumps[6]],[fsb,jumps[7]]].forEach(function(x){ var t=x[1].getBoundingClientRect(); x[0].style.position='absolute'; x[0].style.top='0'; x[0].style.left=(t.left+t.width/2-pb.left-18).toFixed(2)+'px'; });
    }
    /* on the page: the phone is indented to where the quoted text above it starts (the quote's line and padding, without the line),
       and the strip keeps its left edge but opens its gaps until its first six screens, as a block, are centred on the phone */
    function quoteIndent(){
      var row=pr.closest('.protorow')||pr, bars=[].slice.call(document.querySelectorAll('.bar')).filter(function(b){ return b.compareDocumentPosition(row)&Node.DOCUMENT_POSITION_FOLLOWING; }), b=bars[bars.length-1];
      if(!b) return 30; var cs=getComputedStyle(b); return (parseFloat(cs.borderLeftWidth)||0)+(parseFloat(cs.paddingLeft)||0);
    }
    function pageLayout(){
      if(isFs||jumps.length<8){ stage.style.marginLeft=''; strip.style.gap=''; return; }
      var I=quoteIndent(), room=pr.clientWidth-stage.offsetWidth; if(room<I+200) I=0;   /* no room beside the phone: no indent */
      stage.style.marginLeft=I?I+'px':'';
      var g=(2*I+stage.offsetWidth-6*jumps[0].offsetWidth)/5; strip.style.gap=(I&&g>=6)?g.toFixed(2)+'px':'';
    }
    function relayout(){ pageLayout(); alignBtns(); }
    relayout(); window.addEventListener('load',relayout); window.addEventListener('resize',relayout); setTimeout(relayout,400);
    function sync(){ var n=num(); jumps.forEach(function(b,i){ b.classList.toggle('on',i===n-1); }); if(n!==shown){ shown=n; info(n); if(isFs) keep(); } alignTitle(); }
    function preset(n){
      var s=fresh(); if(n===1) return s; s.wallet='MetaMask'; s.scr='tokens'; if(n===2) return s;
      if(n===8){ s=fresh(); s.scr='help'; return s; }
      s.token='USDC'; s.open=true; if(n===3) return s;
      s.open=false; s.net='Ethereum'; s.scr={4:'ready',5:'signing',6:'done',7:'failed'}[n]; return s;
    }
    function jump(n){   /* the strip: the happy path, selection reset; it slides the way the flow goes */
      if(n<1||n>jumps.length) return;
      if(n===8){ if(S.scr!=='help') go({scr:'help'},'flip'); return; }   /* Support from the strip is a tap on [?] wherever you are: the screen in view flips to it */
      var upto=n===7?5:n-1, onHelp=S.scr==='help', cur=num(); hist=[]; for(var i=1;i<=upto;i++) hist.push(preset(i));
      if(onHelp){   /* Support flips back to where it was opened from, unless a click here overrides that: the front of the card is set to the screen asked for, unseen, and the card turns straight to it */
        S=preset(n); card.classList.add('inst'); ar.classList.remove('foot-on'); render('none'); if(ctaPark) parkCta(); void card.offsetWidth; card.classList.remove('inst');
        flipBack(); return; }
      S=preset(n); render(n===cur?'none':((cur===3&&n===4)?'compose':((cur===4&&n===3)?'composeb':(n>cur?'push':'pop'))));
    }
    pr.addEventListener('click',function(e){
      if(isFs&&e.target===pr){ setFs(false); return; }   /* a click on the blurred page behind closes the view */
      var t=e.target.closest?e.target.closest('.st,.restart,.arr,.fsbtn,.fsx,.zb'):null; if(!t||!pr.contains(t)) return;
      if(t.classList.contains('zb')){ stepZoom(t.classList.contains('zplus')?0.1:-0.1); return; }
      e.stopImmediatePropagation(); e.preventDefault();
      if(t.classList.contains('fsx')) setFs(false);
      else if(t.classList.contains('fsbtn')){ if(isPhone()) setApp(true,true); else setFs(!isFs); }
      else if(t.classList.contains('restart')) reset();
      else jump(jumps.indexOf(t)+1);
    },true);
    pr.addEventListener('keydown',function(e){ if(e.key==='ArrowRight'||e.key==='ArrowLeft'){ e.stopImmediatePropagation(); jump(num()+(e.key==='ArrowRight'?1:-1)); } },true);
    /* ---------- app mode (phones): the prototype is the page. The phone drawn on the page goes; the screen fills the browser, without the drawn status bar
       and home bar (the real phone has its own). It is a history entry, so the browser's Back and the back-swipe leave it, and so does Exit in Support. ---------- */
    function dead(){ return isPhone()&&!isApp; }   /* a phone's page: the screens are pictures */
    function noFlip(){ if(!dead()) return; cardbox.classList.add('inst'); setTimeout(function(){ cardbox.classList.remove('inst'); },700); }   /* there Support just appears */
    var appLand=false;   /* opened straight into the prototype: leaving it lands on this section */
    var isApp=false, appPushed=false, appY=0, APPH=+((/apph=(\d+)/.exec(location.hash||'')||[])[1]||772), APPW=320, themeWas=null;   /* the least height the screens need (Select wallet and Review are the tight ones); the full design is 778 without the drawn status bar and home bar */
    function isPhone(){ return window.matchMedia('(max-width:760px)').matches; }
    var appCss=document.createElement('style'); appCss.textContent=
      'html.subs-app,html.subs-app body{overflow:hidden!important;overscroll-behavior:none}'+
      '.protorow .pr.stp.app{position:fixed;inset:0;z-index:1000;display:block;background:linear-gradient(var(--hdc,#fff) 0 calc(var(--hdh,0px) + env(safe-area-inset-top)),#fff calc(var(--hdh,0px) + env(safe-area-inset-top)));padding:env(safe-area-inset-top) env(safe-area-inset-right) env(safe-area-inset-bottom) env(safe-area-inset-left);touch-action:manipulation;-webkit-user-select:none;user-select:none;-webkit-tap-highlight-color:transparent}'+
      '.protorow .pr.stp.app .pinfo,.protorow .pr.stp.app .steps,.protorow .pr.stp.app .pbtns,.protorow .pr.stp.app .fsx,.protorow .pr.stp.app .fszoom{display:none!important}'+
      '.protorow .pr.stp.app .stage{display:block;width:100%;height:100%;margin:0!important}'+
      '.protorow .pr.stp.app .ph.live{position:relative;inset:auto;margin:0 auto;border-radius:0;box-shadow:none;content-visibility:visible}.protorow .pr.stp.app .ph:not(.live){display:none}'+
      /* on a phone's page: Try it out; under it one row, the screen and its notes, that rests in two places only (the screen on the left margin, or the notes ending on the right one); under that the strip, swiped sideways */
      '.protorow .mrow,.protorow .mtrack{display:contents}.protorow .pr.stp.app .mrow,.protorow .pr.stp.app .mtrack{display:block;width:100%;height:100%}'+
      /* a card, as the step cards of the 1-click dream: the title, the play button in the accent, the way out */
      '.subs-look{display:none!important}.tryrow{display:flex;flex-direction:column;align-items:flex-start;gap:18px;box-sizing:border-box;width:100%;max-width:var(--h-textW,640px);margin:36px 0 0;padding:28px 24px 28px 28px;border:1px solid var(--line);border-radius:16px;--sad:#98A0A8;background:repeating-linear-gradient(-45deg,color-mix(in srgb,var(--sad) 7.5%,transparent) 0 2px,transparent 2px 5px),rgba(255,255,255,.40)}:root[data-theme="dark"] .tryrow{--sad:#7C8188;background:repeating-linear-gradient(-45deg,color-mix(in srgb,var(--sad) 4.2%,transparent) 0 2px,transparent 2px 5px),rgba(255,255,255,.05)}'+   /* the work-in-progress stripes of the step numbers, very faint */
      '.tryrow .tryline{display:flex;align-items:center;gap:28px}.tryrow .tryt{margin:0;font:600 20px/1.2 var(--h-sans);letter-spacing:-.01em;color:var(--ink)}'+
      '.tryrow .tryhint{display:flex;align-items:center;gap:6px;font:400 13px/1 var(--h-sans);color:var(--mut);white-space:nowrap}.tryrow .tryhint .hq{flex:none;display:grid;place-items:center;width:20px;height:20px;border-radius:50%;background:#fff;box-shadow:0 0 0 1px var(--line)}.tryrow .tryhint .hq svg{display:block}'+   /* the screen's own Support button: its white disc and its question mark */
      '.tryrow .tryit{flex:none;display:grid;place-items:center;width:56px;height:56px;margin:0;padding:0 0 0 3px;appearance:none;border:0;border-radius:50%;background:var(--accent);color:#fff;box-shadow:0 0 0 5px color-mix(in srgb,var(--accent) 14%,transparent);cursor:pointer;-webkit-tap-highlight-color:transparent}:root[data-theme="dark"] .tryrow .tryit{color:color-mix(in srgb,var(--accent) 30%,#000)}'+
      '.tryrow .trydesk{display:flex;align-items:center;gap:28px}.tryrow .tryph{flex:none;display:block;color:var(--accent)}.tryrow .tryph rect{fill:color-mix(in srgb,#fff 40%,var(--bg))}:root[data-theme="dark"] .tryrow .tryph rect{fill:color-mix(in srgb,#fff 5%,var(--bg))}.tryrow .trylines{display:flex;flex-direction:column;align-items:flex-start;gap:6px;min-width:0}'+
      '.tryrow .tryl1{display:flex;align-items:center;gap:8px;margin:0;font:400 16px/1.5 var(--h-sans);color:var(--body)}.tryrow .tryl1 b{font-weight:600;color:var(--ink)}'+
      '.tryrow .trycopy{flex:none;display:grid;place-items:center;width:30px;height:30px;padding:0;appearance:none;border:0;border-radius:999px;background:transparent;color:var(--mut);cursor:pointer}.tryrow .trycopy:hover{color:var(--ink);background:var(--line)}.tryrow .trycopy.done{color:var(--accent)}.tryrow .trycopy svg{width:15px;height:15px}'+
      '@media(min-width:761px){.v0row.protorow .fig{padding:20px 0 32px}}'+   /* desktop: 76 from the line above to the screen and 100 from the strip's screens to the next title, as the page's other rows */
      '@media(min-width:761px){.tryrow .tryline{display:none}.tryrow{display:grid;grid-template-columns:max-content max-content;column-gap:28px;row-gap:18px;align-items:center;width:fit-content;max-width:100%;padding-right:35.5px}.tryrow .trydesk{display:contents}.tryrow .tryt{grid-column:1}.tryrow .tryph{grid-column:1;justify-self:center}.tryrow .trylines{grid-column:2}.tryrow{position:relative}.tryrow .trycopy{position:absolute;top:20px;right:27.5px}}'+   /* desktop: the phone is centred under the title, whose width sets the first column; the line ends as far from the right edge as the phone stands from the left */
      '@media(max-width:760px){'+
      '.tryrow .trydesk{display:none}.tryrow{cursor:pointer;-webkit-tap-highlight-color:transparent;margin-bottom:88px}.tryrow .tryline{align-self:stretch}.tryrow .tryline .tryhint{flex:1 1 0;justify-content:center}'+   /* phones: the exit line is centred in the space right of the play button */
      '.protorow .pr.stp:not(.app){display:block}'+
            '.protorow .pr.stp:not(.app) .mtrack{display:flex;align-items:flex-start;gap:16px;box-sizing:border-box;width:var(--mtw,auto);padding:0 0 48px var(--mb,22px);overflow:hidden}'+   /* the track is exactly the screen, the gap and the notes: nothing else can add to the travel */
      '.protorow .pr.stp:not(.app) .mrow{display:block;margin:0 calc(var(--mb,22px)*-1) -48px;padding:0;overflow-x:auto;overflow-y:hidden;scroll-snap-type:x mandatory;scroll-padding-left:var(--mb,22px);scrollbar-width:none;-webkit-overflow-scrolling:touch;overscroll-behavior-x:contain}'+
      '.protorow .pr.stp:not(.app) .mrow::-webkit-scrollbar,.protorow .pr.stp:not(.app) .steps::-webkit-scrollbar{display:none}'+
      '.protorow .pr.stp:not(.app) .mrow .stage{flex:none;margin:0!important;scroll-snap-align:start;scroll-snap-stop:always}.protorow .pr.stp:not(.app) .mrow .stage,.protorow .pr.stp:not(.app) .mrow .stage *{pointer-events:none!important}'+   /* the screen is a picture: only the strip changes it */
      '.protorow .pr.stp:not(.app) .mrow .pinfo{flex:none;box-sizing:border-box;max-width:none;padding-right:var(--mb,22px);scroll-snap-align:end;scroll-snap-stop:always}'+
      '.protorow .pr.stp:not(.app) .pinfo .pt{margin-left:0;font-size:calc(22px*var(--az,.79))}.protorow .pr.stp:not(.app) .pinfo .st-row{padding:8px 0;gap:10px}'+
      /* the notes are set as the page's other annotations are on a phone: the same title and body, at the same reduction */
      '.protorow .pr.stp:not(.app) .pinfo .st-t{font:500 calc(17px*var(--az,.79))/1.25 var(--h-sans);letter-spacing:-.02em;color:var(--ink)}.protorow .pr.stp:not(.app) .pinfo .st-b{font:400 calc(15px*var(--az,.79))/1.5 var(--h-sans);color:var(--mut)}.protorow .pr.stp:not(.app) .pinfo .st-tx{padding-top:5px;gap:3px}.protorow .pr.stp:not(.app) .pinfo .st-b + .st-b{display:none}'+   /* Recovery, Back: its second paragraph is left out on phones (the only note with one) */
      '.v0row.protorow .fig{padding:20px 0 32px}.protorow .pr.stp:not(.app) .steps{margin:21px calc(var(--mb,22px)*-1) 0;padding:1px var(--mb,22px) 0;overflow-x:auto;overflow-y:hidden;scrollbar-width:none;-webkit-overflow-scrolling:touch}.protorow .pr.stp:not(.app) .steps button.st{flex:none}'+
      '.protorow .pr.stp:not(.app) .pbtns{display:none!important}'+
      '}';
    document.head.appendChild(appCss);
    var appSt=document.createElement('style'); appSt.textContent=
      '#app.am .iph,#app.am .iph-lay,#app.am .frame,#app.am .c49ar{width:var(--W)!important;height:var(--H)!important}#app.am .iph-lay{top:0!important}#app.am .iph-sb,#app.am .iph-hi{display:none!important}'+
      '.xit{display:none;position:relative;flex:none;padding:5px 9px 4px;border-radius:999px;font:500 11px/1 "IBM Plex Mono",ui-monospace,monospace;letter-spacing:.08em;text-transform:uppercase;white-space:nowrap;color:rgb(209,37,37);background:rgba(209,37,37,.08);box-shadow:inset 0 0 0 1px rgba(209,37,37,.08)}.xit::before{content:"";position:absolute;inset:-12px}#app.am .xit{display:block}@media(max-width:760px){#app:not(.am),#app:not(.am) *{pointer-events:none!important}}';
    root.appendChild(appSt);
    function appSize(){
      if(!isApp) return; var cs=getComputedStyle(pr), w=pr.clientWidth-parseFloat(cs.paddingLeft)-parseFloat(cs.paddingRight), h=pr.clientHeight-parseFloat(cs.paddingTop)-parseFloat(cs.paddingBottom);
      var s=Math.min(1,w/APPW,h/APPH), W=w/s, H=h/s;   /* responsive: the screen is laid out at the browser's own size, 1 to 1. Select wallet needs 772 of height; in a shorter window the screen is laid out wider and scaled down to fit, still edge to edge */
      [stage,live].forEach(function(el){ el.style.setProperty('--pw',w.toFixed(3)); }); live.style.setProperty('--iw',W.toFixed(3)); live.style.setProperty('--ih',H.toFixed(3)); app.style.setProperty('--W',W.toFixed(3)+'px'); app.style.setProperty('--H',H.toFixed(3)+'px');
      var hc=getComputedStyle(hd).backgroundColor; pr.style.setProperty('--hdc',hc); pr.style.setProperty('--hdh',(hd.offsetHeight*s).toFixed(2)+'px'); setTheme(hc);   /* the header's band runs edge to edge, and the browser's bar takes its colour */
    }
    function setTheme(c){ var m=document.querySelector('meta[name="theme-color"]'); if(c!==null){ if(!m){ m=document.createElement('meta'); m.name='theme-color'; m.dataset.subs='1'; document.head.appendChild(m); } else if(themeWas===null) themeWas=m.content; m.content=c; }
      else if(m){ if(m.dataset.subs) m.remove(); else if(themeWas!==null){ m.content=themeWas; themeWas=null; } } }
    function setApp(on,tap){
      if(on===isApp) return; if(on&&isFs) setFs(false); isApp=on;
      if(on){ appY=window.scrollY; try{ history.scrollRestoration='manual'; }catch(e){} try{ history.pushState({subsApp:1},''); appPushed=true; }catch(e){}
        if(tap){ var de=document.documentElement; try{ if(de.requestFullscreen) de.requestFullscreen({navigationUI:'hide'}).catch(function(){}); }catch(e){} } }   /* Android hides the browser's bars; the iPhone has no such call and keeps Safari's bar */
      else { try{ if(document.fullscreenElement) document.exitFullscreen().catch(function(){}); }catch(e){} }
      if(on&&num()!==1){ ar.classList.add('inst'); jump(1); setTimeout(function(){ ar.classList.remove('inst'); },700); }   /* the prototype always starts at the start */
      pr.classList.toggle('app',on); app.classList.toggle('am',on); head(); document.documentElement.classList.toggle('subs-app',on); if(!on) setTheme(null);
      if(on) appSize(); else { live.style.removeProperty('--iw'); live.style.removeProperty('--ih'); app.style.removeProperty('--W'); app.style.removeProperty('--H'); size(); relayout(); msize(true); if(appLand){ appLand=false; appY=Math.max(0,window.scrollY+(pr.closest('.protorow')||pr).getBoundingClientRect().top-80); } window.scrollTo({top:appY,behavior:'instant'}); [60,300].forEach(function(t){ setTimeout(function(){ if(!isApp) window.scrollTo({top:appY,behavior:'instant'}); },t); }); setTimeout(function(){ try{ history.scrollRestoration='auto'; }catch(e){} },400); }   /* the page comes back where it was left */
      if(!on) msize(true); dockPad(); alignTitle(); if(!on&&num()!==1) jump(1);   /* back on the page, the picture is the first screen again */
    }
    var mrow=document.createElement('div'), mtrack=document.createElement('div'); mrow.className='mrow'; mtrack.className='mtrack'; pr.insertBefore(mrow,stage); mrow.appendChild(mtrack); mtrack.appendChild(stage); mtrack.appendChild(pinfo);
    var tryb=document.createElement('button'); tryb.type='button'; tryb.className='tryit'; tryb.innerHTML='<svg width="17" height="20" viewBox="0 0 12 14" fill="currentColor" aria-hidden="true"><path d="M1 1.2v11.6a.9.9 0 0 0 1.36.77l9.7-5.8a.9.9 0 0 0 0-1.54L2.36.43A.9.9 0 0 0 1 1.2z"/></svg>'; tryb.setAttribute('aria-label','Try it');
    var tryrow=document.createElement('div'), tryhint=document.createElement('span'); tryrow.className='tryrow'; tryhint.className='tryhint';
    tryhint.innerHTML='<span>Tap</span><span class="hq" role="img" aria-label="the question mark"><svg width="12" height="12" viewBox="485 260 12 12" fill="none" aria-hidden="true"><path d="M489.125 264.5C489.125 263.45 489.95 262.625 491 262.625C492.05 262.625 492.875 263.45 492.875 264.5C492.875 265.325 492.35 265.625 491.75 266C491.15 266.375 491 266.75 491 267.275" stroke="#3D3B45" stroke-width="1.2" stroke-linecap="round"/><path d="M491 269.674C491.373 269.674 491.675 269.372 491.675 268.999C491.675 268.626 491.373 268.324 491 268.324C490.627 268.324 490.325 268.626 490.325 268.999C490.325 269.372 490.627 269.674 491 269.674Z" fill="#3D3B45"/></svg></span><span>to exit prototype.</span>';
    var tryt=document.createElement('p'); tryt.className='tryt'; tryt.textContent='Try it'; var tryline=document.createElement('div'); tryline.className='tryline'; tryline.appendChild(tryb); tryline.appendChild(tryhint); tryrow.appendChild(tryt); tryrow.appendChild(tryline);
    var PROTO_URL=(/(^|\.)cesargx\.com$/.test(location.hostname)?'cesargx.com':'cesarxdesign.com')+'/proto',   /* each site names its own address, and its /proto opens its own page */
         trydesk=document.createElement('div'); trydesk.className='trydesk';
    trydesk.innerHTML='<svg class="tryph" width="32" height="56" viewBox="0 0 32 56" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" aria-hidden="true"><rect x="1.75" y="1.75" width="28.5" height="52.5" rx="6.5"/><path d="M12.5 6.5h7"/><path d="M11.5 49.5h9"/></svg>'+   /* a phone, where the play button is on a phone */
      '<div class="trylines"><p class="tryl1"><span>Open <b>'+PROTO_URL+'</b> on your mobile phone to try.</span><button type="button" class="trycopy" aria-label="Copy the link">'+ICO_COPY+'</button></p></div>';
    trydesk.querySelector('.trylines').appendChild(tryhint.cloneNode(true)); tryrow.appendChild(trydesk);
    trydesk.querySelector('.trycopy').addEventListener('click',function(e){ e.preventDefault(); e.stopPropagation(); var b=this; try{ if(navigator.clipboard) navigator.clipboard.writeText('https://'+PROTO_URL).catch(function(){}); }catch(err){}
      if(!b.classList.contains('done')){ b.classList.add('done'); b.innerHTML=ICO_TICK; setTimeout(function(){ b.classList.remove('done'); b.innerHTML=ICO_COPY; },1400); } });   /* copied on a Mac, it pastes on the phone */
    /* the card takes the place of the list of things to look for, under A transition (the list and its lead-in are hidden) */
    var look=null; [].forEach.call(document.querySelectorAll('.sub .txtg > p.txt'),function(x){ if(/^Things to look for/.test(x.textContent)) look=x; });
    if(look){ look.classList.add('subs-look'); var ul=look.nextElementSibling; if(ul&&ul.matches('ul.ans')){ ul.classList.add('subs-look'); ul.after(tryrow); } else look.after(tryrow); } else pr.insertBefore(tryrow,mrow);
    tryb.addEventListener('click',function(e){ e.preventDefault(); e.stopPropagation(); if(isPhone()) setApp(true,true); });
    tryrow.addEventListener('click',function(e){ if(isPhone()){ e.preventDefault(); setApp(true,true); } });   /* on a phone the whole card is the button */
    function msize(rest){   /* the screen is the size of the page's other phones (the Paying attention row's); in the notes' position 30% of the browser shows the screen and the notes have the other 70% */
      if(!isPhone()||isApp){ if(mpw){ mpw=0; mtrack.style.minHeight=''; pinfo.style.width=''; pr.style.removeProperty('--mb'); pr.style.removeProperty('--mtw'); if(!isApp){ size(); relayout(); } } return; }
      var was=mpw, vw=document.documentElement.clientWidth, mb=Math.round(pr.getBoundingClientRect().left+window.scrollX), ref=document.querySelector('.v0row.semrow .ph')||document.querySelector('.v0row:not(.protorow) .frow .ph'), rw=ref?ref.getBoundingClientRect().width:0, G=16;
      mpw=Math.round((rw>80?rw:0.542*vw)*100)/100; pr.style.setProperty('--mb',mb+'px'); var SPLIT=0.30, pwd=Math.max(140,Math.round((1-SPLIT)*vw-G)), az=parseFloat(getComputedStyle(document.querySelector('.v0row.semrow')||document.querySelector('.v0row:not(.protorow):not(.wfrow):not(.dsonly)')||pr).zoom)||0.79; pr.style.setProperty('--az',az); pinfo.style.width=pwd+'px'; pr.style.setProperty('--mtw',(mb+mpw+G+pwd)+'px'); size(); noteH();
      if(rest||!was) mrow.scrollLeft=0;   /* it opens on the screen, whole, on the left margin */
    }
    function noteH(){   /* the strip stays put: the row is as tall as the tallest notes (Select token's), plus a little, whichever screen is shown */
      var t=document.createElement('div'), mx=0; t.className='pi'; t.style.cssText='position:absolute;left:0;top:0;width:100%;visibility:hidden;pointer-events:none'; pbox.appendChild(t);
      for(var i=1;i<=INFO.length;i++){ t.innerHTML=infoHtml(i); mx=Math.max(mx,t.offsetHeight); } t.remove(); mtrack.style.minHeight=(Math.ceil(mx)+4+48)+'px'; }
    if(document.fonts&&document.fonts.ready) document.fonts.ready.then(function(){ if(mpw) noteH(); });
    window.addEventListener('resize',function(){ msize(); }); window.addEventListener('load',function(){ msize(true); });
    function exitApp(){ if(!isApp) return; if(appPushed){ appPushed=false; history.back(); } else setApp(false); }
    window.addEventListener('popstate',function(){ if(isApp){ appPushed=false; setApp(false); } });
    window.addEventListener('resize',appSize); if(window.visualViewport) window.visualViewport.addEventListener('resize',appSize);
    pr.addEventListener('touchmove',function(e){ if(isApp) e.preventDefault(); },{passive:false});   /* the page behind does not scroll or bounce */
    msize(true);
    window.__subs={get S(){return S;},get hist(){return hist;},root:root,jump:jump,setApp:setApp};
    S=fresh(); render('none'); setTimeout(function(){ dockL.style.transition=''; ctaL.style.transition=''; },80);
    var m=/proto=(\d)(?:,(\d+))?(,fs)?(,still|,slow)?/.exec(location.hash||''); if(m){ setTimeout(function(){ if(m[4]===',slow'){ var q2=document.createElement('style'); q2.textContent='*{transition-duration:40s!important}'; root.appendChild(q2); } if(m[4]===',still'){ var q=document.createElement('style'); q.textContent='*{transition:none!important;animation:none!important}'; root.appendChild(q); } if(m[3]) setFs(true); jump(+m[1]); if(!m[3]){ pr.scrollIntoView({block:'start'}); window.scrollBy(0,-40); } },+(m[2]||0)); }   /* #proto=N[,delay]: open at step N (for checking the build) */
    else if(/(^|#|&)app\b/.test(location.hash||'')){ setApp(true); }
    else if(/^#try\b/.test(location.hash||'')){ var row=pr.closest('.protorow')||pr, land=function(){ if(!isApp) window.scrollTo({top:Math.max(0,window.scrollY+row.getBoundingClientRect().top-80),behavior:'instant'}); };
      if(isPhone()){ setApp(true); appLand=true; } else { land(); window.addEventListener('load',function(){ land(); [150,500,1200].forEach(function(t){ setTimeout(land,t); }); }); } }
    else { var kept=null; try{ kept=JSON.parse(sessionStorage.getItem('subs.fs')||'null'); }catch(e){}
      if(kept&&kept.fs){ fsZoom=kept.z||0.8; stepZoom(0); setFs(true); if(kept.n>1) jump(kept.n); } }   /* reloaded while maximised: come back maximised, same size, same step */
  }
  if(document.readyState==='loading') document.addEventListener('DOMContentLoaded',init); else init();
})();
