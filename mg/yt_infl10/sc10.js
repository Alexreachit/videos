
// ======================================================================
//  YT 10 – "Why is everything so expensive?"  scene types:
//  hook (coffee price tag), receipt, money ($100 -> x), m2, oil, shrink, wages
// ======================================================================
const paper=(x,y,w,h,inner,p,rot=0)=>p<=0?'':`<div style="position:absolute;left:${x}px;top:${y}px;width:${w}px;height:${h}px;border-radius:18px;background:linear-gradient(180deg,#ffffff,#eef6ff);box-shadow:0 30px 60px #0007;opacity:${Math.min(1,p*2)};transform:translateY(${((1-ez(p))*60).toFixed(1)}px) rotate(${rot}deg);overflow:hidden">${inner}</div>`;
const usd=(v,d=2)=>'$'+MG.fmt(v,d);
const bigBar=(x,base,w,hh,col,lab,val,p,o={})=>p<=0?'':`<div style="position:absolute;left:${x-w/2}px;top:${(base-hh).toFixed(1)}px;width:${w}px;height:${Math.max(6,hh).toFixed(1)}px;border-radius:16px 16px 4px 4px;background:${col};box-shadow:0 12px 30px #0006"></div>`+T(x,base-Math.max(6,hh)-46,val,{size:o.vs||56,col:COL.cream,p:Math.min(1,p*3)})+T(x,base+40,lab,{size:o.ls||32,p:Math.min(1,p*3)});

// ---------------- hook: coffee price tag 2020 -> today ----------------
SC.hook={mk(g,el){mkBg(el,g.spec.img);g.pan=mkPanel(el,g.spec.img,{x:60,y:200,w:1040,h:585});g.ov=mkOv(el)},
 cam(g,t){const c=ctx(g.i0,t),e=ei(cl(t,0,c.D+1)),p=ez(c.r(0,.5));
  g.pan.style.transform=`perspective(2000px) rotateY(${(7-9*e).toFixed(2)}deg) translateX(${((1-p)*-300).toFixed(1)}px) scale(${(.97+.04*e).toFixed(4)})`;g.pan.style.opacity=p;g.pan.img.style.transform=`scale(${(1.05+.06*e).toFixed(4)})`},
 ov(g,t){const c=ctx(g.i0,t);let h='';c.fx('whoosh',0,{d:.6});
  const tt=c.fx('cash',c.w(/today/i,.55)),q=ei(c.r(tt,.9));c.fx('impact',tt+.9);
  const v=lerp(4.17,9.33,q);
  let inner=`<div style="position:absolute;left:0;right:0;top:0;height:90px;background:#1d4f86;color:#fff;font:700 40px/90px P;text-align:center;letter-spacing:3px">COFFEE · 1 LB</div>`;
  inner+=`<div style="position:absolute;left:0;right:0;top:120px;text-align:center;font:500 34px P;color:#3c5a7a">${q>0?'TODAY':'2020'}</div>`;
  inner+=`<div style="position:absolute;left:0;right:0;top:170px;text-align:center;font:700 150px/1 P;color:${q>0?'#d6402e':'#1d4f86'}">${usd(v)}</div>`;
  if(q>=1)inner+=`<div style="position:absolute;left:0;right:0;top:350px;text-align:center;font:500 32px P;color:#3c5a7a">was $4.17 in Jan 2020</div>`;
  h+=paper(1170,230,660,440,inner,c.r(0,.4),3);
  h+=stamp(1500,640,'+124 %',c.r(tt+.9,.35),{size:80,rot:-8,bg:'#ffffffdd'});
  h+=T(960,110,'Why is everything so expensive?',{size:58,col:COL.gold,p:c.a(.05,.4)});
  h+=T(960,880,'U.S. average price, BLS',{size:24,w:500,col:'#d8ecff',p:c.a(.5,.5)});
  return h}};

// ---------------- receipt: 2020 vs 2026 price rows --------------------
const RCPT=[['Coffee, 1 lb','$4.17','$9.33','+124 %',/coffee/i],['Ground beef, 1 lb','$3.89','$6.79','+75 %',/beef/i],['Gasoline, 1 gal','$2.57','$4.48','+75 %',/gasoline|gas/i],['Electricity, 1 kWh','$0.134','$0.196','+46 %',/electricity/i]];
SC.receipt={mk(g,el){mkBg(el,g.spec.img);g.pan=mkPanel(el,g.spec.img,{x:1260,y:600,w:580,h:326});g.ov=mkOv(el)},
 cam(g,t){g.el.querySelector('.blur').style.transform=`scale(${1.03+.04*cl(t,g.B,g.E)})`;const e=ei(cl(t,g.B,g.E));g.pan.style.transform=`perspective(2000px) rotateY(${(-6+8*e).toFixed(2)}deg)`;g.pan.img.style.transform=`scale(${(1.04+.05*e).toFixed(4)})`},
 ov(g,t){const {j}=SC.chart.step(g,t);const cs=[0,1,2].map(q=>q<g.n?ctx(g.i0+q,t):null);let h='';const c0=cs[0];
  const steps=(g.spec.rows||[[0],[1,2],[3]]);
  let inner=`<div style="position:absolute;left:0;right:0;top:0;height:86px;background:#1d4f86;color:#fff;font:700 36px/86px P;text-align:center;letter-spacing:3px">THE RECEIPT</div>`;
  inner+=`<div style="position:absolute;left:40px;right:40px;top:100px;display:flex;font:500 26px P;color:#3c5a7a"><span style="flex:2.2">Item</span><span style="flex:1;text-align:right">Jan 2020</span><span style="flex:1;text-align:right">Sep 2026</span><span style="flex:1;text-align:right">Change</span></div>`;
  let k=0;steps.forEach((rows,s)=>{if(s>j)return;const c=cs[s];rows.forEach((ri,m)=>{const r=RCPT[ri];const tt=c.fx('pop',RX(r[4].source,.15+.35*m,c)),p=c.r(tt,.4);
    inner+=`<div style="position:absolute;left:40px;right:40px;top:${150+ri*92}px;display:flex;align-items:center;font:700 38px P;color:#1d4f86;opacity:${Math.min(1,p*2)};transform:translateX(${((1-ez(p))*40).toFixed(1)}px);border-bottom:3px dashed #1d4f8622;padding-bottom:16px"><span style="flex:2.2;font-weight:500">${r[0]}</span><span style="flex:1;text-align:right;color:#3c5a7a">${r[1]}</span><span style="flex:1;text-align:right">${r[2]}</span><span style="flex:1;text-align:right;color:#d6402e">${r[3]}</span></div>`})});
  h+=paper(120,130,1060,560,inner,c0.r(0,.4),-1);
  h+=T(650,760,'BLS average prices, U.S. city average',{size:24,w:500,col:'#d8ecff',p:c0.a(.5,.5)});
  return h}};

// ---------------- money: $100 counter ----------------------------------
SC.money={mk(g,el){mkBg(el,g.spec.img);g.pan=mkPanel(el,g.spec.img,{x:80,y:190,w:900,h:506});g.ov=mkOv(el)},
 cam(g,t){const e=ei(cl(t,g.B,g.E));g.pan.style.transform=`perspective(2000px) rotateY(${(7-9*e).toFixed(2)}deg)`;g.pan.img.style.transform=`scale(${(1.04+.05*e).toFixed(4)})`},
 ov(g,t){const c=ctx(g.i0,t),sp=g.spec;let h='';c.fx('swish',.05);
  const tt=c.fx(sp.to>100?'cash':'error',RX(sp.re,.6,c)),q=ei(c.r(tt-.3,1));for(let k=0;k<6;k++)c.fx('tick',tt-.3+k*.15,{f:1500+(sp.to>100?k:-k)*100});
  h+=T(1430,250,sp.top,{size:46,col:COL.gold,p:c.a(.05,.4)});
  h+=T(1430,420,'$'+Math.round(lerp(100,sp.to,q)),{size:220,col:q>0?(sp.to>100?COL.red:COL.red):COL.cream,p:1,s:q>=1?1:1});
  h+=T(1430,580,sp.lab,{size:44,p:c.a(tt+.6,.5)});
  if(sp.sub)h+=T(1430,650,sp.sub,{size:26,w:500,col:'#d8ecff',p:c.a(tt+.9,.5)});
  return h}};

// ---------------- m2: money supply bars --------------------------------
SC.m2={mk(g,el){mkBg(el,g.spec.img);g.pan=mkPanel(el,g.spec.img,{x:1180,y:180,w:660,h:371});g.ov=mkOv(el)},
 cam(g,t){g.el.querySelector('.blur').style.transform=`scale(${1.03+.04*cl(t,g.B,g.E)})`;const e=ei(cl(t,g.B,g.E));g.pan.style.transform=`perspective(2000px) rotateY(${(-6+8*e).toFixed(2)}deg)`;g.pan.img.style.transform=`scale(${(1.04+.05*e).toFixed(4)})`},
 ov(g,t){const {j}=SC.chart.step(g,t);const cs=[0,1].map(q=>q<g.n?ctx(g.i0+q,t):null);let h='';const c0=cs[0],base=780,HM=450;
  h+=T(560,100,'M2 money supply (U.S.)',{size:48,col:COL.gold,p:c0.a(.05,.5)});
  const t1=c0.fx('pop',c0.w(/stimulus/i,.3)),p1=ei(c0.r(t1,.8));h+=bigBar(330,base,260,HM*15.49/21.79*p1,'#7cc3ff','Feb 2020','$15.5 T',c0.r(t1,.3));
  h+=chip(560,185,'stimulus checks + Fed',{p:c0.r(c0.w(/federal|trillions/i,.65),.5),size:32,bg:'#1d4f86ee',ic:ic('bank',34,COL.gold)});
  if(j>=1){const c1=cs[1],t2=c1.fx('cash',c1.w(/twenty/i,.5)),p2=ei(c1.r(t2,1));h+=bigBar(790,base,260,HM*p2,COL.gold,'Mar 2022','$21.8 T',c1.r(t2,.3));
   const t3=c1.fx('impact',c1.w(/forty/i,.85));h+=stamp(560,240,'+40 %',c1.r(t3,.35),{size:90,rot:-8,bg:'#ffffffdd'})}
  h+=T(560,850,'Source: Federal Reserve (FRED, M2SL)',{size:24,w:500,col:'#d8ecff',p:c0.a(.5,.5)});
  return h}};

// ---------------- oil: Brent Q1 2026 -----------------------------------
SC.oil={mk(g,el){mkBg(el,g.spec.img);g.pan=mkPanel(el,g.spec.img,{x:80,y:180,w:900,h:506});g.ov=mkOv(el)},
 cam(g,t){g.el.querySelector('.blur').style.transform=`scale(${1.03+.04*cl(t,g.B,g.E)})`;const e=ei(cl(t,g.B,g.E));g.pan.style.transform=`perspective(2000px) rotateY(${(7-9*e).toFixed(2)}deg)`;g.pan.img.style.transform=`scale(${(1.04+.05*e).toFixed(4)})`},
 ov(g,t){const {j}=SC.chart.step(g,t);const cs=[0,1].map(q=>q<g.n?ctx(g.i0+q,t):null);let h='';const c0=cs[0],base=780,HM=400;
  h+=T(1420,110,'2026: Strait of Hormuz',{size:48,col:COL.gold,p:c0.a(.05,.5)});
  h+=chip(1420,200,'shipping nearly stopped',{p:c0.r(c0.w(/stopped|shipping/i,.7),.5),size:36,bg:'#c8432f',ic:ic('warn',36,'#fff')});
  if(j>=1){const c1=cs[1],t1=c1.fx('pop',c1.w(/sixty/i,.35)),t2=c1.fx('cash',c1.w(/hundred/i,.6)),p1=ei(c1.r(t1,.6)),p2=ei(c1.r(t2,1));
   h+=bigBar(1250,base,220,HM*61/118*p1,'#7cc3ff','Jan 2026','$61',c1.r(t1,.3),{vs:64});
   h+=bigBar(1600,base,220,HM*p2,COL.red,'Mar 2026','$118',c1.r(t2,.3),{vs:64});
   h+=T(1420,265,'Brent crude, per barrel',{size:30,w:500,col:'#d8ecff',p:c1.a(.2,.5)});
   const t3=c1.fx('impact',c1.D*.9);h+=chip(1425,850,'+93 % in 3 months',{p:c1.r(t3,.4),size:40,bg:COL.red2})}
  h+=T(530,760,'Source: U.S. Energy Information Administration',{size:24,w:500,col:'#d8ecff',p:c0.a(.5,.5)});
  return h}};

// ---------------- shrink: shrinkflation (BLS example) -----------------
SC.shrink={mk(g,el){mkBg(el,g.spec.img);g.pan=mkPanel(el,g.spec.img,{x:1180,y:180,w:660,h:371});g.ov=mkOv(el)},
 cam(g,t){g.el.querySelector('.blur').style.transform=`scale(${1.03+.04*cl(t,g.B,g.E)})`;const e=ei(cl(t,g.B,g.E));g.pan.style.transform=`perspective(2000px) rotateY(${(-6+8*e).toFixed(2)}deg)`;g.pan.img.style.transform=`scale(${(1.04+.05*e).toFixed(4)})`},
 ov(g,t){const {j}=SC.chart.step(g,t);const cs=[0,1].map(q=>q<g.n?ctx(g.i0+q,t):null);let h='';const c0=cs[0];
  h+=T(560,100,'Shrinkflation',{size:64,col:COL.gold,p:c0.a(.05,.5)});
  h+=chip(560,190,'same price · smaller package',{p:c0.r(c0.w(/smaller/i,.5),.5),size:38,bg:'#1d4f86ee'});
  const c1=j>=1?cs[1]:null,ts=c1?c1.fx('error',c1.w(/hundred/i,.5)):0,q=c1?ei(c1.r(ts,.9)):0,sheets=Math.round(lerp(220,200,q));
  // toilet roll
  const rw=lerp(300,272,q),cx=560,cy=470;
  h+=`<div style="position:absolute;left:${cx-rw/2}px;top:${cy-110}px;width:${rw}px;height:220px;border-radius:30px;background:linear-gradient(90deg,#e8f1ff,#ffffff 40%,#dfe9f7);box-shadow:0 20px 40px #0006;opacity:${Math.min(1,c0.r(.2,.4)*2)}"></div>`;
  h+=`<div style="position:absolute;left:${cx-38}px;top:${cy-38}px;width:76px;height:76px;border-radius:50%;background:#c9b48a;border:6px solid #a8916a;opacity:${Math.min(1,c0.r(.2,.4)*2)}"></div>`;
  h+=T(cx,cy+165,sheets+' sheets',{size:52,col:q>0?COL.red:COL.cream,p:c0.a(.3,.4)});
  h+=T(cx,cy+225,'price: the same',{size:34,col:'#d8ecff',p:c0.a(.5,.4)});
  if(j>=1){const t2=c1.fx('impact',c1.w(/ten/i,.8));h+=stamp(cx,cy-185,'+10 % per sheet',c1.r(t2,.35),{size:46,rot:-8,bg:'#ffffffdd'})}
  h+=T(560,860,'Example from the U.S. Bureau of Labor Statistics',{size:24,w:500,col:'#d8ecff',p:c0.a(.5,.5)});
  return h}};

// ---------------- wages vs prices since 2020 ---------------------------
SC.wages={mk(g,el){mkBg(el,g.spec.img);g.pan=mkPanel(el,g.spec.img,{x:1180,y:180,w:660,h:371});g.ov=mkOv(el)},
 cam(g,t){g.el.querySelector('.blur').style.transform=`scale(${1.03+.04*cl(t,g.B,g.E)})`;const e=ei(cl(t,g.B,g.E));g.pan.style.transform=`perspective(2000px) rotateY(${(-6+8*e).toFixed(2)}deg)`;g.pan.img.style.transform=`scale(${(1.04+.05*e).toFixed(4)})`},
 ov(g,t){const {j}=SC.chart.step(g,t);const cs=[0,1,2].map(q=>q<g.n?ctx(g.i0+q,t):null);let h='';const c0=cs[0],base=780,HM=430;
  h+=T(560,100,'Jan 2020 → Sep 2026',{size:50,col:COL.gold,p:c0.a(.05,.5)});
  const t1=c0.fx('pop',c0.w(/thirty/i,.5)),p1=ei(c0.r(t1,.8));h+=bigBar(340,base,240,HM*30.6/33*p1,COL.red,'Prices','+30.6 %',c0.r(t1,.3));
  if(j>=1){const c1=cs[1],t2=c1.fx('cash',c1.w(/thirty/i,.8)),p2=ei(c1.r(t2,.9));h+=bigBar(780,base,240,HM*p2,COL.green2,'Wages','+33.0 %',c1.r(t2,.3));
   h+=T(780,base+86,'$28.43 → $37.81 / hour',{size:28,w:500,col:'#d8ecff',p:c1.a(c1.w(/twenty/i,.3),.5)})}
  if(j>=2){const c2=cs[2],t3=c2.fx('ding',c2.w(/faster/i,.7));h+=chip(560,205,'wages slightly ahead, on average',{p:c2.r(t3,.5),size:38,bg:COL.green2+'ee',ic:ic('check',40,'#fff')})}
  h+=T(560,150,'BLS: CPI-U and average hourly earnings, total private',{size:24,w:500,col:'#d8ecff',p:c0.a(.5,.5)});
  return h}};
