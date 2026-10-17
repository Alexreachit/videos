// ---------------- hook: bank app shows $1,000,000 ------------------------
SC.hook={mk(g,el){mkBg(el,0);g.comp=document.createElement('div');g.comp.className='ov';el.appendChild(g.comp);g.pan=mkPanel(el,g.spec.img,{x:470,y:300,w:980,h:551});g.ov=mkOv(el)},
 tc(c){return Math.max(3.6,Math.min(4.6,c.D*.72))},
 cam(g,t){const c=ctx(g.i0,t),tc=this.tc(c),p=ei(c.r(tc,1));
  g.comp.style.transform=`translateY(${(-p*170).toFixed(1)}px) scale(${lerp(1,.48,p).toFixed(4)})`;g.comp.style.transformOrigin='960px 300px';
  const q=ez(c.r(tc+.15,.9));g.pan.style.opacity=q;g.pan.style.transform=`perspective(2000px) translateY(${((1-q)*500).toFixed(1)}px) rotateX(${((1-q)*35+2*Math.sin(c.lt*.4)).toFixed(2)}deg) scale(${(.9+.1*q+.02*cl(c.lt,tc,c.D+2)).toFixed(4)})`;
  g.pan.img.style.transform=`scale(${(1.05+.04*cl(c.lt,tc,c.D+3)).toFixed(4)})`;
  setH(g.comp,this.comp(c,tc))},
 comp(c,tc){let h='',s='';c.fx('air',-.3,{d:1});
  // phone with banking app
  const pp=bo(c.r(0,.7)),wake=c.w(/wake/i,.1),tb=c.w(/bank/i,.35),tm=c.w(/million/i,.85);c.fx('beep',tb,{f:1500});c.fx('beep',tb+.12,{f:2000});
  const v=c.lt<tm-.9?1243.57:lerp(1243.57,1001243.57,Math.pow(ei(c.r(tm-.9,1.1)),2));for(let k=0;k<6;k++)c.fx('tick',tm-.9+k*.17,{f:1700+k*160});c.fx('cash',tm+.25);
  h+=`<div style="position:absolute;left:760px;top:${(150+(1-pp)*400).toFixed(0)}px;width:400px;height:760px;border-radius:56px;background:#1b1b1f;box-shadow:0 40px 80px #000c,0 0 0 6px #3a3a40;opacity:${Math.min(1,pp*2)}">
   <div style="position:absolute;inset:18px;border-radius:42px;background:linear-gradient(180deg,#f7efe0,#efe2c6);overflow:hidden">
    <div style="position:absolute;left:0;right:0;top:40px;text-align:center;font:700 28px P;color:${COL.brown}">My Bank</div>
    <div style="position:absolute;left:0;right:0;top:150px;text-align:center;font:500 26px P;color:#8a6a4a">Balance</div>
    <div style="position:absolute;left:0;right:0;top:190px;text-align:center;font:700 ${v>1e6?40:46}px P;color:${v>1e6?COL.green2:COL.brown}">${MG.fmt(v,2,'$')}</div>
    ${[0,1,2].map(k=>`<div style="position:absolute;left:30px;right:30px;top:${330+k*90}px;height:66px;border-radius:16px;background:#ffffffaa"></div>`).join('')}
   </div></div>`;
  // notification
  const pn=c.r(tb,.5);if(pn>0)h+=`<div style="position:absolute;left:640px;top:${(60+ez(pn)*90).toFixed(0)}px;width:640px;height:110px;border-radius:26px;background:#fffdf6;box-shadow:0 20px 40px #0009;opacity:${Math.min(1,pn*2)};display:flex;align-items:center;gap:20px;padding:0 26px;box-sizing:border-box">${ic('coin',64,COL.gold)}<div><div style="font:500 22px P;color:#8a6a4a">My Bank · now</div><div style="font:700 30px P;color:${COL.brown}">Incoming transfer: +$1,000,000.00</div></div></div>`;
  const qp=c.r(tm+.3,.4);h+=T(1420,520,'?!',{size:200,col:COL.gold,p:qp,s:bo(qp)*(1+.06*Math.sin((c.lt-tm)*5)),sh:`${MG.outline(5)},0 10px 30px #000a`});
  h+=face(0,0,0,0);
  return h},
 ov(g,t){const c=ctx(g.i0,t),tc=this.tc(c);c.fx('whoosh',tc,{d:.9});let h='';
  h+=chip(1560,770,'for everyone?',{p:c.r(tc+.9,.5),size:40,bg:'#24150cee',rot:-3,ic:ic('globe',40,'#7cc3ff')});
  return h}};

// ---------------- calc: $1M × 8.2 billion ---------------------------------
SC.calc={mk(g,el){mkBg(el,g.spec.img);g.ov=mkOv(el)},
 cam(g,t){const e=cl(t,g.B,g.E);g.el.querySelector('.blur').style.transform=`scale(${1.03+.04*e}) translateX(${-20*e}px)`},
 ov(g,t){const c=ctx(g.i0,t);let h='';
  const t1=c.fx('pop',.15),t2=c.fx('pop',c.w(/each/i,.2)),te=c.fx('impact',c.w(/quadrillion/i,.45)),tz=c.w(/fifteen/i,.85);
  const up=ez(c.r(c.w(/That/,.6)-.2,.8)),Y=lerp(330,190,up),S=lerp(1,.75,up);
  let r='';
  r+=T(450,0,'$1,000,000',{size:96,p:c.r(t1,.4)});r+=T(450,82,'per person',{size:28,w:500,col:COL.muted,p:c.r(t1,.4)});
  r+=T(860,0,'×',{size:96,col:COL.muted,p:c.r(t2-.1,.3)});
  r+=T(1270,0,'8.2 billion',{size:96,p:c.r(t2,.4)});r+=T(1270,82,'people',{size:28,w:500,col:COL.muted,p:c.r(t2,.4)});
  h+=`<div style="position:absolute;left:0;top:${Y}px;width:1920px;height:0;transform:scale(${S});transform-origin:960px 0">${r}</div>`;
  h+=T(960,Y+200*S,'=',{size:100,col:COL.muted,p:c.r(te-.2,.3)});
  h+=T(960,Y+330*S,'$8.2 quadrillion',{size:Math.round(lerp(140,110,up)),col:COL.gold,p:c.r(te,.4),s:bo(c.r(te,.5)),sh:`0 0 50px #ffc94a66,${SH}`});
  // zeros appear one by one
  if(c.lt>tz-.6){const digits='8,200,000,000,000,000';let shown='',z=0;const nz=Math.floor(cl(c.lt,tz-.4,tz+1.3)*15+1e-6);
   for(const ch of digits){if(ch=='0'){z++;shown+=`<span style="color:${z<=nz?COL.cream:'#ffffff22'}">0</span>`}else shown+=ch}
   for(let k=0;k<15;k+=3)c.fx('tick',tz-.4+k/15*1.7,{f:2200+k*40});
   h+=T(960,760,shown,{size:72,p:c.r(tz-.6,.4),sh:SH});
   h+=chip(960,850,`${nz} zeros`,{p:c.r(tz-.4,.4),size:30,bg:'#24150cee',s:1})}
  return h}};

// ---------------- bars: new money vs world economy (rescaling) ------------
SC.bars={mk(g,el){mkBg(el,g.spec.img);g.ov=mkOv(el)},
 cam(g,t){g.el.querySelector('.blur').style.transform=`scale(${1.03+.04*cl(t,g.B,g.E)})`},
 ov(g,t){const {j}=SC.chart.step(g,t);let h='';const c0=ctx(g.i0,t),pin=c0.a(-.4,.6),X0=520,W0=1180;
  const tim=[];for(let q=0;q<g.n;q++){const cq=ctx(g.i0+q,t),tv=q==0?cq.w(/hundred/i,.75):q==1?cq.w(/four/i,.8):cq.w(/seventy/i,.4);cq.fx(q==2?'impact':'swish',q==2?tv:.05);cq.fx(q==2?'thud':'cash',q==2?cq.w(/eighteen/i,.85):tv+.9);tim.push([cq,tv])}
  const R=[['World economy / year',115,'#7cc3ff','≈ $115 trillion'],['All wealth on Earth',450,COL.cream2,'≈ $450 trillion'],['The new money',8200,COL.gold,'$8,200 trillion']];
  // scale: max visible value eases between steps
  const MX=[150,520,8200];let mx=MX[0];for(let q=1;q<=j;q++){const [cq,tv]=tim[q];mx=Math.exp(lerp(Math.log(MX[q-1]),Math.log(MX[q]),ei(cq.r(tv-.4,1.2))))}
  h+=T(140,130,'Trillions of dollars',{al:'l',size:58,p:pin});
  h+=T(140,192,'rounded estimates (IMF, UBS)',{al:'l',size:26,w:500,col:COL.muted,p:pin});
  R.forEach(([lab,v,col,txt],r)=>{if(r>j)return;const y=360+r*170,[cq,tv]=tim[r],p=ei(cq.r(tv,1.1)),bw=Math.max(4,v/mx*W0*p);
   h+=T(X0-30,y,lab,{al:'r',size:36,col:r==j?COL.cream:COL.cream2,p:Math.min(1,cq.r(tv-.3,.4)*2)});
   h+=`<div style="position:absolute;left:${X0}px;top:${y-40}px;height:80px;width:${bw.toFixed(1)}px;border-radius:0 18px 18px 0;background:${col};box-shadow:${r==j?'0 0 30px '+col+'88,':''}0 10px 20px #0007"></div>`;
   h+=T(Math.min(X0+bw+24,1500),y,txt,{al:'l',size:44,col:r==2?COL.brown:col,sh:r==2&&bw>1000?0:SH,p:Math.min(1,p*3),css:r==2&&bw>1000?`left:${X0+30}px`:''})});
  if(j==2){const [cq]=tim[2];h+=chip(1450,860-60,'≈ 70× the world economy',{p:cq.r(cq.w(/seventy/i,.4)+.2,.5),size:34,bg:'#24150cee'});h+=chip(1450,860+10-60+70,'≈ 18× all wealth',{p:cq.r(cq.w(/eighteen/i,.85),.5),size:34,bg:'#24150cee'})}
  return h}};

// ---------------- scale: money vs stuff ----------------------------------
SC.scale={mk(g,el){mkBg(el,g.spec.img);g.ov=mkOv(el)},
 cam(g,t){g.el.querySelector('.blur').style.transform=`scale(${1.03+.04*cl(t,g.B,g.E)})`},
 ov(g,t){const c=ctx(g.i0,t),tilt=g.spec.mode=='tilt';let h='',s='';const cx=960,cy=380,arm=430;
  const t0=c.fx('swish',.05),tg=c.fx('pop',c.w(/cars|stuff/i,.35)),tm=c.w(/money/i,.85);
  const m=ez(c.r(tm-.5,1.6)),ang=lerp(0,14,m)+Math.sin(c.lt*2)*.4;for(let k=0;k<6;k++)c.fx('coin',tm-.5+k*.25,{n:2});
  const a=ang*Math.PI/180,lx=cx-arm*Math.cos(a),ly=cy+arm*Math.sin(a),rx=cx+arm*Math.cos(a),ry=cy-arm*Math.sin(a),op=c.a(t0,.5);
  s+=`<g opacity=${op}><path d="M${cx-70} 830 L${cx} ${cy+10} L${cx+70} 830 Z" fill="#c58a4a"/><rect x=${cx-150} y=820 width=300 height=24 rx=10 fill="#8a5a36"/>
   <line x1=${lx} y1=${ly} x2=${rx} y2=${ry} stroke="#e0b070" stroke-width=18 stroke-linecap=round /><circle cx=${cx} cy=${cy} r=22 fill="#e0b070"/>
   <line x1=${lx} y1=${ly} x2=${lx-110} y2=${ly+200} stroke="#e0b070" stroke-width=5 /><line x1=${lx} y1=${ly} x2=${lx+110} y2=${ly+200} stroke="#e0b070" stroke-width=5 />
   <line x1=${rx} y1=${ry} x2=${rx-110} y2=${ry+200} stroke="#e0b070" stroke-width=5 /><line x1=${rx} y1=${ry} x2=${rx+110} y2=${ry+200} stroke="#e0b070" stroke-width=5 />
   <path d="M${lx-150} ${ly+200} H${lx+150} Q${lx} ${ly+260} ${lx-150} ${ly+200} Z" fill="#c58a4a"/><path d="M${rx-150} ${ry+200} H${rx+150} Q${rx} ${ry+260} ${rx-150} ${ry+200} Z" fill="#c58a4a"/></g>`;
  // money stacks grow on the left
  const n=Math.round(lerp(2,22,m));for(let k=0;k<n;k++){const col=k%3,row=Math.floor(k/3);s+=`<rect x=${lx-120+col*82} y=${ly+176-row*20} width=76 height=20 rx=4 fill="#8fc77f" stroke="#2f6b3a" stroke-width=3 />`}
  h+=svg(s);
  ['car','phone','plane'].forEach((icn,k)=>{h+=icAt(icn,rx-90+k*90,ry+150,80,COL.cream2,c.r(tg+k*.1,.4))});
  h+=chip(lx,ly+320,tilt?'much more money':'money: ×thousands',{p:c.r(tm,.5),size:36,bg:COL.green2+'f0'});
  h+=chip(rx,ry+320,tilt?'not more stuff':'stuff: unchanged',{p:c.r(tg+.4,.5),size:36,bg:'#24150cee'});
  h+=T(960,150,tilt?'Every time: the same mistake':'Money changed. Stuff did not.',{size:52,p:c.a(t0,.5)});
  return h}};

// ---------------- double: prices doubling --------------------------------
const DBL={dbl:['Germany, 1923','prices doubled every 3–4 days',k=>'Day '+Math.round(k*3.5)],dbl2:['Zimbabwe, 2008','prices doubled about every day',k=>'Day '+k],dbl3:['Hungary, 1946','prices doubled about every 15 hours',k=>(k*15)+' h']};
SC.double={mk(g,el){mkBg(el,0);g.pan=mkPanel(el,g.spec.img,{x:1440,y:90,w:400,h:225});g.ov=mkOv(el)},
 cam(g,t){const e=ei(cl(t,g.B,g.E));g.pan.style.transform=`rotate(${(3-2*e).toFixed(2)}deg) scale(${(.98+.03*e).toFixed(3)})`;g.pan.img.style.transform=`scale(${(1.04+.05*e).toFixed(4)})`},
 ov(g,t){const c=ctx(g.i0,t),[ti,sub,lab]=DBL[g.spec.group];let h='';const t0=c.fx('swish',.05);
  h+=T(120,150,ti,{al:'l',size:66,col:COL.gold,p:c.a(t0,.5)});
  h+=T(120,222,sub,{al:'l',size:36,p:c.a(t0+.2,.5)});
  const base=820,N=8,t1=.7,t2=Math.max(t1+2.5,c.D*.88);
  for(let k=0;k<N;k++){const tt=lerp(t1,t2,k/(N-1));c.fx(k==N-1?'impact':'pop',tt);const p=c.r(tt,.45),v=Math.pow(2,k),hh=v/128*480*ez(p),x=200+k*150;if(p<=0)continue;
   h+=`<div style="position:absolute;left:${x-50}px;top:${base-hh-6}px;width:100px;height:${(hh+6).toFixed(1)}px;border-radius:12px 12px 4px 4px;background:${k>5?COL.red:k>3?'#ff8a5a':COL.gold}"></div>`;
   h+=T(x,base-hh-40,'$'+v,{size:k>5?44:34,col:k>5?COL.red:COL.cream,p});
   h+=T(x,base+34,lab(k),{size:24,w:500,col:COL.muted,p})}
  h+=chip(1640,400,`${ic('bread',36,COL.brown)}<span>a loaf of bread</span>`,{p:c.a(t1,.4),size:30,bg:'#fbf0daf2',fg:COL.brown,s:1});
  return h}};

// ---------------- spiral: wage-price loop ---------------------------------
SC.spiral={mk(g,el){mkBg(el,g.spec.img);g.ov=mkOv(el)},
 cam(g,t){g.el.querySelector('.blur').style.transform=`scale(${1.03+.04*cl(t,g.B,g.E)}) rotate(${(-1+2*cl(t,g.B,g.E)).toFixed(2)}deg)`},
 ov(g,t){const c=ctx(g.i0,t);let h='',s='';const cx=720,cy=500,R=270,t0=c.fx('swish',.05);
  const N=[['Higher wages','coin'],['Higher costs','gear'],['Higher prices','up'],['Workers need more','house']];
  const t1=c.w(/pay/i,.3),loop=Math.max(1.2,(c.D-t1)/1.6);
  s+=`<circle cx=${cx} cy=${cy} r=${R} fill=none stroke="#ffffff22" stroke-width=10 stroke-dasharray="4 18" opacity=${c.a(t0,.4)} />`;
  const ph=Math.max(0,c.lt-t1)/loop,ang=-Math.PI/2+ph*2*Math.PI;
  // trail
  let d='';const st=Math.max(0,ph-.35);for(let k=0;k<=30;k++){const u=lerp(st,ph,k/30),a=-Math.PI/2+u*2*Math.PI;d+=(k?'L':'M')+(cx+R*Math.cos(a)).toFixed(1)+' '+(cy+R*Math.sin(a)).toFixed(1)}
  if(c.lt>t1)s+=`<path d="${d}" fill=none stroke="${COL.red}" stroke-width=12 stroke-linecap=round opacity=.9 /><circle cx=${cx+R*Math.cos(ang)} cy=${cy+R*Math.sin(ang)} r=18 fill="#fff"/>`;
  h+=svg(s);
  N.forEach(([lab,icn],k)=>{const a=-Math.PI/2+k*Math.PI/2,x=cx+R*Math.cos(a),y=cy+R*Math.sin(a),tt=t1+k*loop/4;c.fx('tick',tt,{f:1800+k*150});if(k==0)c.fx('tick',tt+loop,{f:1800});
   const hot=c.lt>tt&&((ph*4)%4)>=k&&((ph*4)%4)<k+1;
   h+=chip(x,y,lab,{p:c.r(tt-.3,.5),size:hot?40:34,bg:hot?COL.red:'#24150cee',fg:'#fff',ic:ic(icn,34,'#fff')})});
  h+=T(cx,cy,'↻',{size:120,col:'#ffffff33',p:c.a(t0,.5)});
  const lp=Math.floor(ph)+(ph>0?1:0);h+=T(1500,380,'Prices',{size:46,col:COL.muted,p:c.a(t1,.4)});
  h+=T(1500,480,'+'+Math.round(lerp(0,100,ph)*1.0)+' %',{size:110,col:COL.red,p:c.a(t1,.4),sh:`0 0 30px #ff5b4a55,${SH}`});
  h+=T(1500,580,'and climbing',{size:32,col:COL.cream2,p:c.a(t1+1,.4)});
  h+=chip(1500,700,'wage-price spiral',{p:c.r(c.fx('impact',c.w(/further/i,.9)),.5),size:36,bg:'#7a2318ee'});
  return h}};

// ---------------- supply vs demand -----------------------------------------
SC.supplydemand={mk(g,el){mkBg(el,g.spec.img);g.ov=mkOv(el)},
 cam(g,t){g.el.querySelector('.blur').style.transform=`scale(${1.03+.04*cl(t,g.B,g.E)})`},
 ov(g,t){const c=ctx(g.i0,t);let h='',s='';const t0=c.fx('swish',.05),ts=c.fx('thud',c.w(/supply/i,.2)),td=c.fx('riser',Math.max(0,c.w(/demand/i,.5)-.8),{d:1}),tw=c.fx('impact',c.w(/worst/i,.85));
  const ps=ez(c.r(ts,.8)),pd=ez(c.r(c.w(/demand/i,.5),.8));
  const arrowBig=(x,dir,col,p,lab)=>p<=0?'':`<div style="position:absolute;left:${x-150}px;top:${dir>0?250:270}px;width:300px;height:380px;opacity:${Math.min(1,p*2)};transform:translateY(${((1-p)*dir*80).toFixed(0)}px)">${ic(dir>0?'up':'down',300,col)}</div>`+T(x,720,lab,{size:46,col,p});
  h+=arrowBig(420,-1,COL.red,ps,'Supply');h+=arrowBig(1500,1,COL.green,pd,'Demand');
  // gauge
  const gv=ez(c.r(c.w(/demand/i,.5)+.3,1.2)),a=lerp(-80,80,gv)+(gv>.9?Math.sin(c.lt*40)*3:0);
  s+=`<g opacity=${c.a(t0,.4)}><path d="M760 560 A200 200 0 0 1 1160 560" fill=none stroke="#ffffff22" stroke-width=40 /><path d="M760 560 A200 200 0 0 1 1160 560" fill=none stroke="${COL.red}" stroke-width=40 pathLength=100 stroke-dasharray="${(gv*100).toFixed(1)} 100" /><line x1=960 y1=560 x2=${960+170*Math.sin(a*Math.PI/180)} y2=${560-170*Math.cos(a*Math.PI/180)} stroke="#fff" stroke-width=10 stroke-linecap=round /><circle cx=960 cy=560 r=20 fill="#fff"/></g>`;
  h=svg(s)+h;h+=T(960,640,'Prices',{size:46,p:c.a(t0,.4)});
  h+=stamp(960,200,'WORST COMBINATION',c.r(tw,.35),{size:54,rot:-4});
  return h}};

// ---------------- melt: the million shrinks ---------------------------------
SC.melt={mk(g,el){mkBg(el,0);g.pan=mkPanel(el,g.spec.img,{x:90,y:190,w:820,h:461});g.ov=mkOv(el)},
 cam(g,t){const e=ei(cl(t,g.B,g.E));g.pan.style.transform=`perspective(2000px) rotateY(${(8-10*e).toFixed(2)}deg) scale(${(.98+.03*e).toFixed(4)})`;g.pan.img.style.transform=`scale(${(1.04+.05*e).toFixed(4)})`},
 ov(g,t){const c=ctx(g.i0,t);let h='';const t1=c.fx('pop',.3),t2=Math.max(t1+2.2,c.D*.85);
  const q=ei(c.r(t1+.4,t2-t1)),mo=Math.round(q*6),v=1000000*Math.pow(.6,q*6);for(let k=1;k<=6;k++)c.fx('tick',t1+.4+(t2-t1)*k/6,{f:2300-k*120});c.fx('thud',t2+.1);
  h+=T(1420,230,`Month ${mo}`,{size:44,col:COL.muted,p:c.a(t1,.4)});
  h+=T(1420,330,'Your $1,000,000 buys what',{size:36,p:c.a(t1,.4)});
  h+=T(1420,460,fmt(Math.round(v/1000)*1000,'$'),{size:120,col:lerp(0,1,q)>.5?COL.red:COL.gold,p:c.a(t1,.4),sh:`0 0 50px #ffc94a44,${SH}`});
  h+=T(1420,560,'bought on day one',{size:36,p:c.a(t1,.4)});
  h+=`<div style="position:absolute;left:1120px;top:620px;width:600px;height:40px;border-radius:12px;background:#ffffff14"><div style="height:100%;width:${(v/1e4).toFixed(2)}%;border-radius:12px;background:linear-gradient(90deg,${COL.red},${COL.gold})"></div></div>`;
  h+=T(1420,700,'illustration, not a forecast',{size:24,w:500,col:COL.muted,p:c.a(1,.4)});
  return h}};

// ---------------- pie: same cake, more slices -----------------------------
SC.pie={mk(g,el){mkBg(el,g.spec.img);g.ov=mkOv(el)},
 cam(g,t){g.el.querySelector('.blur').style.transform=`scale(${1.03+.04*cl(t,g.B,g.E)})`},
 ov(g,t){const c=ctx(g.i0,t);let h='',s='';const cx=620,cy=520,R=290,t0=c.fx('swish',.05);
  const tp=c.w(/print/i,.15),tc=c.w(/cake/i,.8);const steps=[tp+.4,tp+1.3,tc-.6,tc+.3];let n=4;steps.forEach((st,k)=>{if(c.lt>st)n=4*Math.pow(2,k+1)>64?64:[8,16,32,64][k];c.fx('swish',st,{d:.3})});
  s+=`<g opacity=${c.a(t0,.5)}><ellipse cx=${cx} cy=${cy+70} rx=${R+30} ry=70 fill="#0006"/><ellipse cx=${cx} cy=${cy+40} rx=${R} ry=${R*.38} fill="#8a4f2a"/><rect x=${cx-R} y=${cy-60} width=${2*R} height=100 fill="#8a4f2a"/><ellipse cx=${cx} cy=${cy-60} rx=${R} ry=${R*.38} fill="#f6d7a7"/>`;
  for(let k=0;k<n;k++){const a=k/n*2*Math.PI;s+=`<line x1=${cx} y1=${cy-60} x2=${(cx+R*Math.cos(a)).toFixed(1)} y2=${(cy-60+R*.38*Math.sin(a)).toFixed(1)} stroke="#8a4f2a" stroke-width=${n>16?2:4} />`}
  s+=`</g>`;h+=svg(s);
  h+=T(cx,170,'The economy = one cake',{size:48,p:c.a(t0,.5)});
  h+=T(1420,330,'slices (money)',{size:36,col:COL.muted,p:c.a(tp,.4)});
  h+=T(1420,440,String(n),{size:140,col:COL.gold,p:c.a(tp,.4),sh:`0 0 40px #ffc94a55,${SH}`});
  h+=T(1420,560,'each slice: '+(n==4?'25 %':(100/n).toFixed(n>16?1:1)+' %'),{size:40,p:c.a(tp,.4)});
  h+=chip(1420,700,'same cake',{p:c.r(c.fx('ding',tc),.5),size:42,bg:`linear-gradient(90deg,${COL.gold2},${COL.gold})`,fg:COL.brown});
  return h}};

// ---------------- outro: subscribe -------------------------------------
SC.outro={mk(g,el){g.im=mkImg(el,g.spec.img);g.ov=mkOv(el)},
 cam(g,t){const e=ei(cl(t,g.B,g.E+2));g.im.style.transform=`scale(${(1.04+.05*e).toFixed(4)}) translate(${(-10+16*e).toFixed(1)}px,0)`},
 ov(g,t){const c=ctx(g.i0,t),tcur=1,tcl=c.fx('tap',c.w(/subscribe/i,.15)+.3),tn=c.fx('whoosh',c.w(/next/i,.55),{d:.8});c.fx('ding',tcl+.25);c.fx('chime',tn+.6);let h='';
  const done=c.lt>=tcl,pr=c.r(tcl,.25),press=pr>0&&pr<1?1-.1*Math.sin(pr*Math.PI):1;
  h+=chip(1560,640,done?'Subscribed':'Subscribe',{p:c.a(.2,.5),s:bo(c.a(.2,.5))*press,size:52,bg:done?'#5a4a3c':'#d6402e',fg:'#fff',ic:ic(done?'check':'bell',50,'#fff'),r:20});
  const cp=ei(c.r(tcur,Math.max(.4,tcl-tcur))),cx=lerp(1900,1600,cp),cy=lerp(1000,660,cp);
  if(c.lt>tcur-.1&&c.lt<tcl+1.2)h+=`<svg style="position:absolute;left:${cx}px;top:${cy}px;opacity:${1-c.r(tcl+.7,.5)}" width=60 height=70 viewBox="0 0 60 70"><path d="M4 4 L4 56 L18 44 L28 66 L38 62 L28 40 L46 40 Z" fill="#fff" stroke="#000" stroke-width=4 stroke-linejoin=round /></svg>`;
  const rr=c.r(tcl,.7);if(rr>0&&rr<1)h+=`<div style="position:absolute;left:${1560-160*ez(rr)}px;top:${640-160*ez(rr)}px;width:${320*ez(rr)}px;height:${320*ez(rr)}px;border-radius:50%;border:5px solid #fff;opacity:${1-rr}"></div>`;
  const pn=c.r(tn,.6);if(pn>0)h+=`<div style="position:absolute;left:1100px;top:110px;width:740px;height:150px;border-radius:26px;background:#24150cee;box-shadow:0 20px 40px #0009;border:3px solid ${COL.gold}66;transform:translateX(${((1-ez(pn))*800).toFixed(1)}px);display:flex;align-items:center;gap:26px;padding:0 30px;box-sizing:border-box">${ic('down',90,COL.red)}<div><div style="font:500 26px P;color:${COL.muted}">Next video</div><div style="font:700 38px/1.15 P;color:${COL.cream}">Why prices almost never go down</div></div></div>`;
  return h}};
