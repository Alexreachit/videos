
// ======================================================================
//  YT 9 – new scene types: hook (tax return), score, rule, loan, step, share
// ======================================================================
const paper=(x,y,w,h,inner,p,rot=0)=>p<=0?'':`<div style="position:absolute;left:${x}px;top:${y}px;width:${w}px;height:${h}px;border-radius:18px;background:linear-gradient(180deg,#ffffff,#eef6ff);box-shadow:0 30px 60px #0007;opacity:${Math.min(1,p*2)};transform:translateY(${((1-ez(p))*60).toFixed(1)}px) rotate(${rot}deg);overflow:hidden">${inner}</div>`;
const row=(y,lab,val,col,p,sz=40)=>p<=0?'':`<div style="position:absolute;left:36px;right:36px;top:${y}px;display:flex;justify-content:space-between;align-items:baseline;opacity:${Math.min(1,p*2)};transform:translateX(${((1-ez(p))*30).toFixed(1)}px);border-bottom:3px dashed #1d4f8622;padding-bottom:10px"><span style="font:500 30px P;color:#3c5a7a">${lab}</span><span style="font:700 ${sz}px P;color:${col}">${val}</span></div>`;
const bigM=v=>v>=1e9?'$'+MG.fmt(v/1e9,v<1e10?1:0)+' billion':v>=1e6?'$'+MG.fmt(v/1e6,0)+' million':MG.fmt(Math.round(v),0,'$');

// ---------------- hook: Bezos 2011 tax return ------------------------------------
SC.hook={mk(g,el){mkBg(el,g.spec.img);g.pan=mkPanel(el,g.spec.img,{x:60,y:200,w:1040,h:585});g.ov=mkOv(el)},
 cam(g,t){const c=ctx(g.i0,t),e=ei(cl(t,0,c.D+1)),p=ez(c.r(0,.6));
  g.pan.style.transform=`perspective(2000px) rotateY(${(7-9*e).toFixed(2)}deg) translateX(${((1-p)*-300).toFixed(1)}px) scale(${(.97+.04*e).toFixed(4)})`;g.pan.style.opacity=p;
  g.pan.img.style.transform=`scale(${(1.05+.06*e).toFixed(4)})`},
 ov(g,t){const c=ctx(g.i0,t);let h='';c.fx('whoosh',0,{d:.6});
  const te=c.fx('pop',.25),tE=c.w(/billion/i,.25),tz=c.fx('impact',c.w(/^zero/i,.45)),tf=c.fx('cash',c.w(/^four/i,.75));
  const pw=ei(c.r(te,Math.max(.8,tE-te))),nw=18e9*pw;c.fx('cash',tE);
  let inner=`<div style="position:absolute;left:0;right:0;top:0;height:92px;background:#1d4f86;color:#fff;font:700 38px/92px P;text-align:center;letter-spacing:3px">TAX RETURN · 2011</div>`;
  inner+=row(140,'Net worth','≈ '+bigM(nw),'#1d4f86',c.r(te-.2,.4),44);
  inner+=row(250,'Federal income tax',c.lt>=tz?'$0':'…',c.lt>=tz?'#22a95e':'#3c5a7a',c.r(te+.3,.4),c.lt>=tz?64:44);
  inner+=row(370,'Child tax credit','+ $4,000','#d6402e',c.r(tf,.4),44);
  h+=paper(1150,220,700,500,inner,c.r(0,.5),2);
  h+=stamp(1500,520,'PAID: $0',c.r(tz,.35),{size:70,col:'#22a95e',rot:-9,bg:'#ffffffdd'});
  h+=T(960,110,'One of the richest men alive · 2011',{size:58,col:COL.gold,p:c.a(.05,.5)});
  return h}};

// ---------------- score: ProPublica 25 richest -------------------------------------
SC.score={mk(g,el){mkBg(el,g.spec.img);g.pan=mkPanel(el,g.spec.img,{x:1160,y:560,w:640,h:360});g.ov=mkOv(el)},
 cam(g,t){g.el.querySelector('.blur').style.transform=`scale(${1.03+.04*cl(t,g.B,g.E)})`;const e=ei(cl(t,g.B,g.E));
  const {j}=SC.chart.step(g,t);const q=j>=3?ez(cl(t-MG.L(g.i0+3).start,0,.6)):0;
  g.pan.style.transform=`perspective(2000px) rotateY(${(-6+8*e).toFixed(2)}deg) translateY(${(q*700).toFixed(1)}px)`;g.pan.style.opacity=1-q;g.pan.img.style.transform=`scale(${(1.04+.05*e).toFixed(4)})`},
 ov(g,t){const {j}=SC.chart.step(g,t);const cs=[0,1,2,3].map(q=>q<g.n?ctx(g.i0+q,t):null);let h='';
  const c0=cs[0],base=780,HM=520,BW=260,XA=380,XB=760;
  h+=T(960,92,'The 25 richest Americans · 2014–2018',{size:44,col:COL.gold,p:c0.a(.05,.5)});
  h+=T(960,146,'Source: ProPublica, “The Secret IRS Files” (2021)',{size:24,w:500,col:'#d8ecff',p:c0.a(.3,.5)});
  const col=(x,v,hh,c1,lab,val,p)=>`<div style="position:absolute;left:${x-BW/2}px;top:${(base-hh).toFixed(1)}px;width:${BW}px;height:${Math.max(6,hh).toFixed(1)}px;border-radius:14px 14px 4px 4px;background:${c1};box-shadow:0 10px 30px #0006"></div>`+T(x,base-Math.max(6,hh)-44,val,{size:50,col:COL.cream,p:Math.min(1,p*3)})+T(x,base+38,lab,{size:30,p:Math.min(1,p*3)});
  const ta=c0.fx('pop',c0.w(/four/i,.45)),pa=ei(c0.r(ta,1.3));c0.fx('cash',ta+1.3);
  h+=col(XA,401,HM*pa,'linear-gradient(180deg,#ffd76a,#f0a22a)','Wealth growth','$'+Math.round(401*pa)+'B',c0.r(ta,.3));
  if(j>=1){const c1=cs[1],tb=c1.fx('thud',c1.w(/thirteen/i,.4)),pb=ei(c1.r(tb,.8));
   h+=col(XB,13.6,HM*13.6/401*pb,'#ff5b4a','Income tax paid','$'+(13.6*pb).toFixed(1)+'B',c1.r(tb,.3));
   h+=chip(XB,base-150,'tiny!',{p:c1.r(tb+.9,.4),size:34,bg:'#c8432f',rot:-6})}
  if(j>=2){const c2=cs[2],tc=c2.fx('impact',c2.w(/three/i,.7)),pc=c2.r(tc,.5);
   h+=T(1450,260,'13.6 ÷ 401 =',{size:44,col:'#d8ecff',w:500,p:c2.a(.3,.5)});
   h+=T(1450,380,'3.4 %',{size:170,col:COL.gold,p:pc,s:bo(pc),sh:`0 0 60px #ffc94a66,${SH}`});
   h+=T(1450,490,'“true tax rate”',{size:44,p:c2.a(tc+.3,.5)})}
  if(j>=3){const c3=cs[3],td=c3.fx('pop',c3.w(/fourteen/i,.75)),p1=ei(c3.r(.2,.8)),p2=ei(c3.r(td,.9));
   const bar=(y,lab,v,c1,p)=>T(1080,y-46,lab,{al:'l',size:30,col:COL.cream,p:Math.min(1,p*3)})+`<div style="position:absolute;left:1080px;top:${y-20}px;width:${(Math.max(.02,v/14*640*p)).toFixed(1)}px;height:56px;border-radius:0 14px 14px 0;background:${c1};box-shadow:0 8px 20px #0006"></div>`+T(1080+v/14*640*p+22,y+8,(v*Math.min(1,p*1.1)).toFixed(1)+' %',{al:'l',size:48,col:c1,p:Math.min(1,p*3)});
   h+=bar(640,'Top 25 richest (true rate)',3.4,COL.gold,p1);
   h+=bar(780,'Typical household (≈ $70k income)',14,'#7cf0b0',p2)}
  return h}};

// ---------------- rule: Sam vs Victor ------------------------------------------------
SC.rule={mk(g,el){mkBg(el,0);g.pa=mkPanel(el,72,{x:70,y:110,w:820,h:461});g.pb=mkPanel(el,74,{x:1030,y:110,w:820,h:461});g.ov=mkOv(el)},
 cam(g,t){const {j}=SC.chart.step(g,t),e=ei(cl(t,g.B,g.E));const c2=g.n>2?ctx(g.i0+2,t):null;const pb=j>=2?ez(c2.r(-.2,.7)):0;
  g.pa.style.transform=`perspective(2000px) rotateY(${(6-6*e).toFixed(2)}deg) scale(${(j>=2?.97:1).toFixed(3)})`;g.pa.img.style.transform=`scale(${(1.04+.05*e).toFixed(4)})`;
  g.pb.style.opacity=pb;g.pb.style.transform=`perspective(2000px) rotateY(${(-6+6*e).toFixed(2)}deg) translateX(${((1-pb)*400).toFixed(1)}px)`;g.pb.img.style.transform=`scale(${(1.04+.05*e).toFixed(4)})`},
 ov(g,t){const {j}=SC.chart.step(g,t);const cs=[0,1,2,3,4].map(q=>q<g.n?ctx(g.i0+q,t):null);let h='';
  const c0=cs[0];c0.fx('swish',.05);
  h+=chip(480,70,'SAM · delivers food',{p:c0.r(.1,.5),size:34,bg:'#22a95eee',ic:ic('truck',38,'#fff')});
  // paycheck
  const tp=c0.fx('paper',c0.w(/paycheck/i,.35)),tt=c0.fx('error',c0.w(/taxes/i,.65)),pp=c0.r(tp,.5),cut=ez(c0.r(tt,.6));
  let inner=`<div style="position:absolute;left:30px;top:22px;font:700 30px P;color:#1d4f86">PAYCHECK</div><div style="position:absolute;right:30px;top:22px;font:500 26px P;color:#3c5a7a">every 2 weeks</div>`;
  inner+=`<div style="position:absolute;left:30px;top:80px;font:700 54px P;color:#1d4f86">${cut>0?'$1,540':'$1,540'}</div>`;
  inner+=`<div style="position:absolute;left:30px;top:150px;font:700 44px P;color:#d6402e;opacity:${cut}">− taxes, before you see it</div>`;
  h+=paper(160,600,640,200,inner,pp,-1.5);
  if(j>=1){const c1=cs[1],ti=c1.fx('pop',c1.w(/income/i,.2)),ts=c1.fx('pop',c1.w(/social/i,.6));
   h+=chip(310,850,'Income tax: 10 – 37 %',{p:c1.r(ti,.5),size:32,bg:'#c8432f'});
   h+=chip(700,850,'+ 7.65 % payroll',{p:c1.r(ts,.5),size:32,bg:'#c8432f'})}
  if(j>=2){const c2=cs[2];c2.fx('whoosh',.05,{d:.6});const ts=c2.fx('pop',c2.w(/salary/i,.8));
   h+=chip(1440,70,'VICTOR · founder',{p:c2.r(.1,.5),size:34,bg:'#7a3bd1ee',ic:ic('up',38,'#fff')});
   h+=chip(1440,630,'Salary: almost $0',{p:c2.r(ts,.5),size:40,bg:'#1d4f86ee'})}
  if(j>=3){const c3=cs[3],tb=c3.fx('cash',c3.w(/billion/i,.4)),pv=ei(c3.r(tb-.6,1.2)),tq=c3.fx('pop',c3.w(/owe/i,.8));
   h+=T(1440,730,'Shares: +'+bigM(1e9*pv),{size:58,col:COL.green,p:c3.a(tb-.6,.4),sh:`0 0 40px #3ddc8455,${SH}`});
   h+=T(1440,815,c3.lt>=tq?'Tax owed: ?':'',{size:44,col:COL.cream,p:c3.a(tq,.4)})}
  if(j>=4){const c4=cs[4],tz=c4.fx('impact',.15);h+=stamp(1440,330,'$0 TAX',c4.r(tz,.35),{size:110,col:'#22a95e',rot:-8,bg:'#ffffffdd'})}
  return h}};

// ---------------- loan: shares vs debt over 20 years ------------------------------------
SC.loan={mk(g,el){mkBg(el,g.spec.img);g.pan=mkPanel(el,g.spec.img,{x:1380,y:520,w:470,h:264});g.ov=mkOv(el)},
 cam(g,t){g.el.querySelector('.blur').style.transform=`scale(${1.03+.04*cl(t,g.B,g.E)})`;const e=ei(cl(t,g.B,g.E));g.pan.style.transform=`perspective(2000px) rotateY(${(-6+8*e).toFixed(2)}deg)`;g.pan.img.style.transform=`scale(${(1.04+.05*e).toFixed(4)})`},
 ov(g,t){const {j}=SC.chart.step(g,t);const cs=[0,1,2].map(q=>q<g.n?ctx(g.i0+q,t):null);let h='',s='';
  const c0=cs[0];h+=T(960,92,'Living on loans: an example',{size:46,col:COL.gold,p:c0.a(.05,.5)});
  h+=T(960,146,'illustrative numbers, not a forecast',{size:26,w:500,col:'#d8ecff',p:c0.a(.3,.5)});
  const X=y=>220+y/20*800,Y=v=>760-v/480*540;
  const S=y=>100*Math.pow(1.08,y),Dd=y=>2*(Math.pow(1.05,y)-1)/.05;
  // axes
  s+=`<line x1=200 y1=760 x2=1050 y2=760 stroke="#ffffff66" stroke-width=3 /><line x1=200 y1=760 x2=200 y2=200 stroke="#ffffff44" stroke-width=3 />`;
  for(let y=0;y<=20;y+=5)s+=`<text x=${X(y)} y=800 text-anchor=middle font-family="P,Arial" font-weight=500 font-size=26 fill="#d8ecff">year ${y}</text>`;
  h+=svg(s);s='';
  const tq=c0.fx('pop',c0.w(/interest/i,.4));if(j==0)h+=chip(620,420,'Interest costs money …',{p:c0.r(tq,.5),size:44,bg:'#c8432f',ic:ic('pct',44,'#fff')});
  if(j>=1){const c1=cs[1],t8=c1.fx('pop',c1.w(/eight/i,.3)),t5=c1.fx('pop',c1.w(/five/i,.5)),tr=c1.fx('ding',c1.w(/richer/i,.8));
   const p=ei(c1.r(t8,Math.max(1.5,c1.D*.6))),ye=20*p;let d1='',d2='';
   for(let k=0;k<=60;k++){const y=ye*k/60;d1+=(k?'L':'M')+X(y).toFixed(1)+' '+Y(S(y)).toFixed(1);d2+=(k?'L':'M')+X(y).toFixed(1)+' '+Y(Dd(y)).toFixed(1)}
   let area='';for(let k=0;k<=60;k++){const y=ye*k/60;area+=(k?'L':'M')+X(y).toFixed(1)+' '+Y(S(y)).toFixed(1)}for(let k=60;k>=0;k--){const y=ye*k/60;area+='L'+X(y).toFixed(1)+' '+Y(Dd(y)).toFixed(1)}
   s+=`<path d="${area}Z" fill="#3ddc8433" opacity=${c1.a(tr,.6)} />`;
   s+=`<path d="${d1}" fill=none stroke="${COL.green}" stroke-width=12 stroke-linecap=round stroke-linejoin=round /><path d="${d2}" fill=none stroke="${COL.red}" stroke-width=12 stroke-linecap=round stroke-linejoin=round opacity=${c1.a(t5,.3)} />`;
   s+=`<circle cx=${X(ye)} cy=${Y(S(ye))} r=13 fill="#fff"/>`;h+=svg(s);
   h+=chip(X(ye)+20,Y(S(ye))-40,'Shares +8 % / year',{p:c1.r(t8,.4),size:30,bg:COL.green2+'ee',al:'l'});
   h+=chip(X(ye)+20,Y(Dd(ye))+40,'Debt, 5 % interest',{p:c1.r(t5,.4),size:30,bg:'#c8432f',al:'l'});
   if(ye>8)h+=T(X(ye*.62),(Y(S(ye*.62))+Y(Dd(ye*.62)))/2+10,'Victor gets richer',{size:34,col:'#eafff2',p:c1.a(tr,.5)})}
  if(j>=2){const c2=cs[2],tb=c2.fx('pop',c2.w(/borrow/i,.25)),tf=c2.fx('cash',c2.w(/faster/i,.85));
   h+=chip(560,250,'New loan pays the interest',{p:c2.r(tb,.5),size:36,bg:'#1d4f86ee',ic:ic('bank',38,COL.gold)});
   h+=chip(1600,330,'shares grow faster',{p:c2.r(tf,.5),size:36,bg:COL.green2+'ee',ic:ic('up',38,'#fff')})}
  return h}};

// ---------------- step: step-up in basis ----------------------------------------------
SC.step={mk(g,el){mkBg(el,g.spec.img);g.pan=mkPanel(el,g.spec.img,{x:1150,y:170,w:700,h:394});g.ov=mkOv(el)},
 cam(g,t){g.el.querySelector('.blur').style.transform=`scale(${1.03+.04*cl(t,g.B,g.E)})`;const e=ei(cl(t,g.B,g.E));g.pan.style.transform=`perspective(2000px) rotateY(${(-7+9*e).toFixed(2)}deg)`;g.pan.img.style.transform=`scale(${(1.04+.05*e).toFixed(4)})`},
 ov(g,t){const {j}=SC.chart.step(g,t);const cs=[0,1,2].map(q=>q<g.n?ctx(g.i0+q,t):null);let h='';
  const c0=cs[0],base=800,HM=560,BW=300,X0=560;
  h+=T(560,92,"Victor's shares",{size:46,col:COL.gold,p:c0.a(.05,.5)});
  const t1=c0.fx('pop',c0.w(/million/i,.25)),t2=c0.fx('cash',c0.w(/billion/i,.45)),t3=c0.fx('thud',c0.w(/ninety/i,.7));
  const pw=ei(c0.r(t2,1.2)),worth=HM*pw;
  // value column
  h+=`<div style="position:absolute;left:${X0-BW/2}px;top:${(base-Math.max(10,worth)).toFixed(1)}px;width:${BW}px;height:${Math.max(10,worth).toFixed(1)}px;border-radius:16px 16px 4px 4px;background:linear-gradient(180deg,#7cf0b0,#22a95e);box-shadow:0 10px 30px #0006;opacity:${Math.min(1,c0.r(t1,.3)*3)}"></div>`;
  // basis bar (blue), rises in step 2
  const c1=j>=1?cs[1]:null,tu=c1?c1.fx('impact',c1.w(/day/i,.75)):0,pu=c1?ei(c1.r(tu,1)):0,bh=lerp(10,HM,pu);
  h+=`<div style="position:absolute;left:${X0-BW/2-14}px;top:${(base-bh).toFixed(1)}px;width:${BW+28}px;height:${bh.toFixed(1)}px;border-radius:10px;border:7px solid #ffc94a;box-sizing:border-box;background:#ffc94a22;opacity:${Math.min(1,c0.r(t1,.3)*3)}"></div>`;
  h+=chip(X0-BW/2-30,base-bh-4,pu>.9?'New basis: $1 billion':'Bought for: $1 million',{p:c0.r(t1,.4),size:30,bg:'#ffc94a',fg:'#1d4f86',al:'r'});
  if(pw>.05)h+=chip(X0+BW/2+30,base-worth+30,'Worth: '+bigM(1e6+999e6*pw),{p:1,size:30,bg:COL.green2+'ee',al:'l'});
  const pg=c0.r(t3,.5);
  if(pu<.95&&pg>0)h+=T(X0,base-worth/2,'Untaxed gain<br>$999 million',{size:46,col:'#fff',lh:1.15,p:pg*(1-pu),s:bo(pg)});
  if(j>=1){h+=chip(960,860-0,'“as if bought on the day he died”',{p:c1.r(c1.w(/treats/i,.5),.5),size:32,bg:'#1d4f86ee'});
   h+=T(1500,640,'Step-up in basis',{size:60,col:COL.gold,p:c1.a(c1.w(/step/i,.25),.5)})}
  if(j>=2){const c2=cs[2],te=c2.fx('impact',c2.w(/disappears/i,.7));
   h+=stamp(X0,base-HM/2,'GAIN: ERASED',c2.r(te,.35),{size:66,rot:-8,bg:'#ffffffdd'});
   h+=T(1500,740,'Taxable gain: $999M → $0',{size:48,col:COL.cream,p:c2.a(te+.3,.5)})}
  return h}};

// ---------------- share: top 1 % income vs taxes -----------------------------------------
SC.share={mk(g,el){mkBg(el,g.spec.img);g.pan=mkPanel(el,g.spec.img,{x:80,y:170,w:640,h:360});g.ov=mkOv(el)},
 cam(g,t){const e=ei(cl(t,g.B,g.E));g.pan.style.transform=`perspective(2000px) rotateY(${(7-9*e).toFixed(2)}deg)`;g.pan.img.style.transform=`scale(${(1.04+.05*e).toFixed(4)})`},
 ov(g,t){const c=ctx(g.i0,t);let h='';c.fx('swish',.05);
  h+=T(960,92,'The top 1 % of US taxpayers (tax year 2023)',{size:44,col:COL.gold,p:c.a(.05,.5)});
  const bar=(y,lab,v,col,re,f)=>{const tt=c.fx('pop',RX(re,f,c)),p=ei(c.r(tt,1)),W=1000;
   return T(800,y-58,lab,{al:'l',size:34,col:COL.cream,p:Math.min(1,p*3)})+`<div style="position:absolute;left:800px;top:${y-28}px;width:${W}px;height:70px;border-radius:16px;background:#ffffff22;overflow:hidden;opacity:${Math.min(1,p*3)}"><div style="height:100%;width:${(v*p*10).toFixed(1)}px;background:${col}"></div></div>`+T(800+v*p*10+24,y+7,(v*p).toFixed(1)+' %',{al:'l',size:52,col,p:Math.min(1,p*3)})};
  h+=bar(330,'Share of all income they earned',20.6,'#7cc3ff','twenty',.45);
  h+=bar(520,'Share of all federal income taxes they paid',38.4,COL.gold,'thirty',.75);
  h+=T(960,700,'Source: Tax Foundation, IRS data, tax year 2023',{size:26,w:500,col:'#d8ecff',p:c.a(.8,.5)});
  return h}};
