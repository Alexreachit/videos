// ---------------- hook: brokerage app, portfolio drops ------------------------
SC.hook={mk(g,el){mkBg(el,0);g.comp=document.createElement('div');g.comp.className='ov';el.appendChild(g.comp);g.pan=mkPanel(el,g.spec.img,{x:470,y:300,w:980,h:551});g.ov=mkOv(el)},
 tc(c){return Math.max(3.6,Math.min(4.6,c.D*.5))},
 cam(g,t){const c=ctx(g.i0,t),tc=this.tc(c),p=ei(c.r(tc,1));
  g.comp.style.transform=`translateY(${(-p*170).toFixed(1)}px) scale(${lerp(1,.48,p).toFixed(4)})`;g.comp.style.transformOrigin='960px 300px';
  const q=ez(c.r(tc+.15,.9));g.pan.style.opacity=q;g.pan.style.transform=`perspective(2000px) translateY(${((1-q)*500).toFixed(1)}px) rotateX(${((1-q)*35+2*Math.sin(c.lt*.4)).toFixed(2)}deg) scale(${(.9+.1*q+.02*cl(c.lt,tc,c.D+2)).toFixed(4)})`;
  g.pan.img.style.transform=`scale(${(1.05+.04*cl(c.lt,tc,c.D+3)).toFixed(4)})`;
  setH(g.comp,this.comp(c,tc))},
 comp(c,tc){let h='';c.fx('air',-.3,{d:1});
  const pp=bo(c.r(0,.7)),tl=c.w(/lose/i,.55),tm=c.w(/mistakes/i,.85);
  const pr=ei(c.r(.5,Math.max(1,tl-.2)));          // chart progress
  const dr=ei(c.r(tl-.1,.9));                      // drop progress
  c.fx('beep',.5,{f:1500});for(let k=0;k<5;k++)c.fx('tick',tl-.1+k*.17,{f:1500-k*110});c.fx('thud',tl+.9);
  const v=lerp(10000,10000+1800*pr,1)*(1-.37*dr);
  // chart points
  let d='',N=60;const X0=40,Y0=0;
  for(let k=0;k<=N;k++){const u=k/N;if(u>pr&&k>0&&u>pr+.017)break;let y=150-80*u*(0.8+0.2*Math.sin(u*9));
   d+=(k?'L':'M')+(X0+u*320).toFixed(1)+' '+y.toFixed(1)}
  let d2='';if(dr>0){const sx=X0+pr*320,sy=150-80*pr*(0.8+0.2*Math.sin(pr*9));for(let k=0;k<=20;k++){const u=k/20*dr;d2+=(k?'L':'M')+(sx+u*40).toFixed(1)+' '+(sy+u*110+Math.sin(k*1.7)*4).toFixed(1)}}
  const col=dr>.05?COL.red:COL.green2;
  h+=`<div style="position:absolute;left:760px;top:${(150+(1-pp)*400).toFixed(0)}px;width:400px;height:760px;border-radius:56px;background:#1b1b1f;box-shadow:0 40px 80px #000c,0 0 0 6px #3a3a40;opacity:${Math.min(1,pp*2)}">
   <div style="position:absolute;inset:18px;border-radius:42px;background:linear-gradient(180deg,#f7efe0,#efe2c6);overflow:hidden">
    <div style="position:absolute;left:0;right:0;top:40px;text-align:center;font:700 28px P;color:${COL.brown}">My Portfolio</div>
    <div style="position:absolute;left:0;right:0;top:150px;text-align:center;font:500 26px P;color:#8a6a4a">Total value</div>
    <div style="position:absolute;left:0;right:0;top:190px;text-align:center;font:700 46px P;color:${dr>.05?COL.red:COL.brown}">${MG.fmt(v,0,'$')}</div>
    <svg style="position:absolute;left:0;top:290px" width=360 height=240 viewBox="0 0 400 260"><path d="${d}" fill=none stroke="${COL.green2}" stroke-width=9 stroke-linecap=round stroke-linejoin=round /><path d="${d2}" fill=none stroke="${COL.red}" stroke-width=9 stroke-linecap=round /></svg>
    ${[0,1].map(k=>`<div style="position:absolute;left:30px;right:30px;top:${560+k*74}px;height:56px;border-radius:16px;background:#ffffffaa"></div>`).join('')}
   </div></div>`;
  const qp=c.r(tm,.4);h+=T(1420,520,'5',{size:260,col:COL.gold,p:qp,s:bo(qp)*(1+.05*Math.sin((c.lt-tm)*5)),sh:`${MG.outline(5)},0 10px 30px #000a`});
  return h},
 ov(g,t){const c=ctx(g.i0,t),tc=this.tc(c);c.fx('whoosh',tc,{d:.9});let h='';
  h+=chip(1560,770,'5 simple mistakes',{p:c.r(tc+.9,.5),size:40,bg:'#24150cee',rot:-3,ic:ic('warn',40,COL.gold)});
  return h}};

// ---------------- dots: 100 dots = 100 percent -----------------------------------
SC.dots={mk(g,el){mkBg(el,g.spec.img);g.pan=mkPanel(el,g.spec.img,{x:80,y:170,w:711,h:400});g.ov=mkOv(el)},
 cam(g,t){const e=ei(cl(t,g.B,g.E));g.pan.style.transform=`perspective(2000px) rotateY(${(7-9*e).toFixed(2)}deg) scale(${(.98+.03*e).toFixed(4)})`;g.pan.img.style.transform=`scale(${(1.04+.05*e).toFixed(4)})`},
 ov(g,t){const c=ctx(g.i0,t),sp=g.spec;let h='';const t0=c.fx('swish',.05);
  h+=T(960,92,sp.title,{size:sp.title.length>40?38:44,col:COL.gold,p:c.a(t0,.5)});
  const gx=1100,gy=190,st=58,R=21;let idx=0;const cum=[];
  sp.groups.forEach(([n,col,lab,re],j)=>{const tg=c.fx(j==0?'pop':'tick',RX(re,.25+.3*j,c)-.05+(j==0?0:0));cum.push([idx,n,tg,CK[col],lab]);idx+=n});
  let dots='';for(let k=0;k<100;k++){let col='#ffffff14',p=0;for(const [i0,n,tg,cc] of cum){if(k>=i0&&k<i0+n){p=c.r(tg+(k-i0)*.011,.3);col=cc}}
   const x=gx+(k%10)*st,y=gy+Math.floor(k/10)*st;dots+=`<circle cx=${x} cy=${y} r=${(R*(p>0?bo(p):1)*(p>0?1:.55)).toFixed(1)} fill="${p>0?col:'#ffffff1a'}" />`}
  h+=svg(dots);
  const tb=cum[0][2];h+=T(436,660,sp.big,{size:150,col:CK[sp.bigcol],p:c.a(tb,.5),s:bo(c.r(tb,.5)),sh:`0 0 50px ${CK[sp.bigcol]}55,${SH}`});
  {const sz=22,ws=sp.groups.map(gp=>gp[2].length*sz*.62+sz*1.3),tot=ws.reduce((x,y)=>x+y,0)+(ws.length-1)*14;let lx=1390-tot/2;
   sp.groups.forEach(([n,col,lab],j)=>{const tg=cum[j][2];h+=chip(lx+ws[j]/2,778,lab,{p:c.r(tg+.1,.4),size:sz,bg:CK[col]+'dd',fg:col=='gold'||col=='green'||col=='grey'?COL.brown:'#fff'});lx+=ws[j]+14})}
  if(sp.foot)h+=T(960,862,sp.foot,{size:24,w:500,col:COL.muted,p:c.a(.8,.5)});
  return h}};

// ---------------- lever: borrowed money, 4 steps ---------------------------------
SC.lever={mk(g,el){mkBg(el,g.spec.img);g.ov=mkOv(el)},
 cam(g,t){g.el.querySelector('.blur').style.transform=`scale(${1.03+.04*cl(t,g.B,g.E)})`},
 ov(g,t){const {j}=SC.chart.step(g,t);const cs=[0,1,2,3].map(q=>q<g.n?ctx(g.i0+q,t):null);let h='',s='';
  const base=740,K=24,W=260,X=[520,960,1400];
  h+=T(960,100,'Investing with borrowed money',{size:46,col:COL.gold,p:cs[0].a(.05,.5)});
  const blk=(x,top,hh,col,txt,sub,p)=>{if(p<=0||hh<1)return'';return `<div style="position:absolute;left:${x-W/2}px;top:${top.toFixed(1)}px;width:${W}px;height:${hh.toFixed(1)}px;border-radius:14px;background:${col};opacity:${Math.min(1,p*2)};box-shadow:0 10px 24px #0007;display:flex;flex-direction:column;align-items:center;justify-content:center;font:700 ${hh<150?26:30}px/1.15 P;color:#fff;overflow:hidden"><div>${txt}</div><div style="font:500 24px P;opacity:.9">${sub}</div></div>`};
  const lab=(x,txt,p)=>T(x,base+42,txt,{size:30,col:COL.cream2,w:500,p});
  // step 0: both directions
  const c0=cs[0];c0.fx('swish',.05);
  if(j==0){const ta=c0.fx('pop',c0.w(/smart/i,.5)),tb=c0.fx('impact',c0.w(/directions/i,.85));
   h+=chip(560,420,'gains × 2',{p:c0.r(ta,.5),size:54,bg:COL.green2+'ee',ic:ic('up',60,'#fff')});
   h+=chip(1360,420,'losses × 2',{p:c0.r(tb,.5),size:54,bg:'#c8432f',ic:ic('down',60,'#fff')});
   h+=chip(960,600,'borrowed from your broker',{p:c0.r(c0.w(/broker/i,.6),.5),size:38,bg:'#24150cee',ic:ic('bank',44,COL.gold)})}
  // step 1: stack of 20k
  if(j>=1){const c1=cs[1],pk=j==1?1:1;const a=c1.r(c1.w(/ten/i,.25),.5),b=c1.r(c1.w(/another/i,.55),.5),tt=c1.r(c1.w(/twenty/i,.85),.5);c1.fx('pop',c1.w(/ten/i,.25));c1.fx('pop',c1.w(/another/i,.55));c1.fx('cash',c1.w(/twenty/i,.85));
   const ea=ez(a),eb=ez(b);
   h+=blk(X[0],base-240*ea,240*ea,COL.green2,'Your money','$10,000',a);
   h+=blk(X[0],base-240-240*eb,240*eb,'#c8432f','Borrowed','$10,000',b);
   // mark: loan is bottom, own on top in later columns -> keep consistent: swap order visually
   h+=lab(X[0],'Start',a);
   if(tt>0)h+=chip(X[0],base-480-52,'$20,000 in stocks',{p:tt,size:30,bg:COL.gold,fg:COL.brown})}
  if(j>=2){const c2=cs[2],td=c2.fx('impact',c2.w(/drops/i,.1)),tl=c2.w(/left|five/i,.6),tc=c2.fx('thud',c2.w(/half/i,.88));
   const q=ei(c2.r(td,.9)),ownH=lerp(240,120,q),p0=c2.r(-.1,.5);
   h+=blk(X[1],base-240,240,'#c8432f','Borrowed','$10,000',p0);
   h+=blk(X[1],base-240-ownH,ownH,COL.green2,'Your money',q>.95?'$5,000':'',p0);
   h+=lab(X[1],'Market −25 %',p0);
   h+=chip(X[1],base-240-ownH-52,q>.5?`$${MG.fmt(Math.round(lerp(20,15,q)*1000),0)}`:'$20,000',{p:p0,size:30,bg:'#24150cee'});
   h+=chip(1010,180,'−50 % of YOUR money',{p:c2.r(tc,.5),size:44,bg:'#c8432f',fg:'#fff',ic:ic('warn',44,'#fff')})}
  if(j>=3){const c3=cs[3],td=c3.fx('impact',c3.w(/fifty/i,.15)),ts=c3.fx('error',c3.w(/wiped/i,.45)),tm=c3.w(/margin/i,.8);
   const q=ei(c3.r(td,.9)),p0=c3.r(-.1,.5);
   h+=blk(X[2],base-240,240,'#c8432f','Borrowed','$10,000',p0);
   h+=lab(X[2],'Market −50 %',p0);
   h+=chip(X[2],base-240-52,q>.5?'$10,000':'$20,000',{p:p0,size:30,bg:'#24150cee'});
   h+=T(X[2],base-240-100,'$0 left',{size:56,col:COL.red,p:c3.a(ts,.5),s:bo(c3.r(ts,.5))});
   h+=stamp(X[2],285,'WIPED OUT',c3.r(ts,.35),{size:50,rot:-6});
   h+=chip(X[2],205,'margin call',{p:c3.r(tm,.5),size:32,bg:'#24150cee',ic:ic('bell',34,COL.gold)})}
  return h}};

// ---------------- fees: $10,000, 30 years, 7% vs 6% ------------------------------
SC.fees={mk(g,el){mkBg(el,g.spec.img);g.ov=mkOv(el)},
 cam(g,t){g.el.querySelector('.blur').style.transform=`scale(${1.03+.04*cl(t,g.B,g.E)})`},
 ov(g,t){const {j}=SC.chart.step(g,t);const cs=[0,1,2].map(q=>q<g.n?ctx(g.i0+q,t):null);let h='';
  const base=740,MAX=76123,HM=470,BW=300,XA=620,XB=1300;
  const c0=cs[0];h+=T(960,95,'$10,000 · 30 years · no new deposits',{size:42,col:COL.gold,p:c0.a(.05,.5)});
  h+=T(960,150,'illustrative example, not a forecast',{size:26,w:500,col:COL.muted,p:c0.a(.3,.5)});
  const bar=(x,v,col,lab,sub,p,showv)=>{const hh=v/MAX*HM;return `<div style="position:absolute;left:${x-BW/2}px;top:${(base-hh).toFixed(1)}px;width:${BW}px;height:${hh.toFixed(1)}px;border-radius:16px 16px 4px 4px;background:${col};box-shadow:0 10px 30px #0008"></div>`+
    T(x,base-hh-44,MG.fmt(Math.round(v),0,'$'),{size:56,col:COL.cream,p:Math.min(1,p*3)})+T(x,base+36,lab,{size:34,p:Math.min(1,p*3)})+T(x,base+78,sub,{size:24,w:500,col:COL.muted,p:Math.min(1,p*3)})};
  const t1=c0.fx('pop',c0.w(/seven/i,.45)),pa=ei(c0.r(t1,Math.max(1.2,c0.D*.35)));c0.fx('cash',t1+Math.max(1.2,c0.D*.35));for(let k=0;k<4;k++)c0.fx('tick',t1+k*.3,{f:1600+k*120});
  const A=10000*Math.pow(1.07,30*pa),B6=10000*Math.pow(1.06,30*pa);
  h+=bar(XA,A,COL.green2,'7 % per year','the market',c0.r(t1,.4));
  h+=T(960,400,j>=1?'':`Year ${Math.round(30*pa)}`,{size:46,col:COL.cream2,p:c0.a(t1,.4)});
  if(j>=1){const c1=cs[1],t2=c1.fx('pop',c1.w(/fee/i,.1)),pb=ei(c1.r(t2,Math.max(1.2,c1.D*.45)));c1.fx('cash',t2+Math.max(1.2,c1.D*.45));
   const Bv=10000*Math.pow(1.06,30*pb),Av=76123;
   h+=bar(XB,Bv,'#d97a3c','6 % per year','7 % − 1 % fee',c1.r(t2,.4));if(j==1)h+=T(960,400,`Year ${Math.round(30*pb)}`,{size:46,col:COL.cream2,p:c1.a(t2,.4)});}
  if(j>=2){const c2=cs[2],t3=c2.fx('impact',c2.w(/nineteen/i,.2)),p3=c2.r(t3,.6),hA=76123/MAX*HM,hB=57435/MAX*HM;
   h+=`<div style="position:absolute;left:${XB-BW/2}px;top:${(base-hA).toFixed(1)}px;width:${BW}px;height:${(hA-hB).toFixed(1)}px;border-radius:16px 16px 0 0;border:5px dashed ${COL.red};box-sizing:border-box;background:#ff5b4a33;opacity:${Math.min(1,p3*2)}"></div>`;
   h+=T(XB,base-(hA+hB)/2,'−$18,688',{size:58,col:COL.red,p:p3,s:bo(p3),sh:`0 0 30px #000,${SH}`});
   h+=chip(960,330,'≈ 25 % less',{p:c2.r(c2.w(/quarter/i,.65),.5),size:46,bg:'#c8432f',fg:'#fff',ic:ic('warn',46,'#fff')})}
  return h}};

// ---------------- crash: S&P 500 2007-2013 (simplified) --------------------------
SC.crash={mk(g,el){mkBg(el,g.spec.img);g.ov=mkOv(el)},
 cam(g,t){g.el.querySelector('.blur').style.transform=`scale(${1.03+.04*cl(t,g.B,g.E)})`},
 ov(g,t){const {j}=SC.chart.step(g,t);const c0=ctx(g.i0,t),c1=g.n>1?ctx(g.i0+1,t):null;let h='',s='';
  const X=y=>220+(y-2007.8)/(2013.2-2007.8)*1420,Y=v=>250+(100-v)/60*450;
  const f=yr=>{if(yr<=2009.2){const u=(yr-2007.8)/1.4;return 100-57*ei(u)+2.4*Math.sin(yr*29)*Math.sin(Math.PI*u)}const u=(yr-2009.2)/4;return 43+57*(.3*u+.7*ez(u))+2.2*Math.sin(yr*23)*Math.sin(Math.PI*Math.min(1,u))};
  const tp=c0.fx('pop',c0.w(/peak/i,.3)),tf=c0.w(/fifty/i,.8),tlow=c0.w(/^low/i,.6);
  const p0=j>=1?1:ei(c0.r(tp+.2,Math.max(1.2,tf+.7-tp-.2)));
  const t2s=c1?.2:0,p1=j>=1?ei(c1.r(t2s,Math.max(1.5,c1.w(/thirteen/i,.5)+.5-t2s))):0;
  const yEnd=j>=1?lerp(2009.2,2013.2,p1):lerp(2007.8,2009.2,p0);
  // axes
  s+=`<line x1=200 y1=720 x2=1700 y2=720 stroke="#ffffff44" stroke-width=3 />`;for(let y=2008;y<=2013;y++){s+=`<line x1=${X(y)} y1=715 x2=${X(y)} y2=725 stroke="#ffffff66" stroke-width=3 /><text x=${X(y)} y=760 text-anchor=middle font-family="P,Arial" font-weight=500 font-size=26 fill="${COL.muted}">${y}</text>`}
  s+=`<line x1=${X(2007.8)} y1=${Y(100)} x2=${X(2013.2)} y2=${Y(100)} stroke="${COL.gold}" stroke-width=3 stroke-dasharray="4 14" opacity=${c0.a(tp,.5)*.8} />`;
  let d1='',d2='';for(let y=2007.8;y<=Math.min(yEnd,2009.2)+1e-6;y+=.02)d1+=(d1?'L':'M')+X(y).toFixed(1)+' '+Y(f(y)).toFixed(1);
  if(yEnd>2009.2)for(let y=2009.2;y<=yEnd+1e-6;y+=.03)d2+=(d2?'L':'M')+X(y).toFixed(1)+' '+Y(f(y)).toFixed(1);
  s+=`<path d="${d1}" fill=none stroke="${COL.red}" stroke-width=12 stroke-linecap=round stroke-linejoin=round />`;if(d2)s+=`<path d="${d2}" fill=none stroke="${COL.green}" stroke-width=12 stroke-linecap=round stroke-linejoin=round />`;
  const hy=Math.min(yEnd,2013.2);s+=`<circle cx=${X(hy)} cy=${Y(f(hy))} r=14 fill="#fff" />`;
  h+=svg(s);
  h+=T(960,110,'S&P 500, price index (simplified)',{size:44,col:COL.gold,p:c0.a(.05,.5)});
  h+=chip(X(2007.8)+110,Y(100)-48,'Oct 2007: peak',{p:c0.r(tp,.5),size:30,bg:'#24150cee'});
  const pl=c0.r(Math.max(tf,tlow)+.5,.5);h+=chip(X(2009.2)+130,Y(43)-18,'Mar 2009: low',{p:pl,size:30,bg:'#24150cee'});
  h+=T(300,640,'−57 %',{size:88,col:COL.red,p:c0.r(tf+.3,.5),s:bo(c0.r(tf+.3,.5)),sh:`0 0 40px #ff5b4a55,${SH}`});
  c0.fx('thud',tf+.4);
  if(j>=1){const t3=c1.fx('impact',c1.w(/thirteen/i,.55)+.45),t4=c1.fx('pop',c1.w(/years/i,.75));
   h+=chip(X(2013.2)-60,Y(100)-48,'Mar 2013: back at the old peak',{p:c1.r(t3,.5),size:30,bg:COL.green2+'ee',al:'r'});
   h+=chip(X(2011.2),585,'more than 5 years',{p:c1.r(t4,.5),size:40,bg:'#c8432f',ic:ic('clock',40,'#fff')});
   s='';h+=svg(`<path d="M${X(2009.2)} 585 H${X(2013.2)}" stroke="#ffffff88" stroke-width=4 stroke-dasharray="10 8" opacity=${c1.a(t4,.4)} /><path d="M${X(2009.2)} 570 V600 M${X(2013.2)} 570 V600" stroke="#ffffffaa" stroke-width=4 />`)}
  return h}};

// ---------------- best: missing the best days (J.P. Morgan 2005-2024) -------------
SC.best={mk(g,el){mkBg(el,g.spec.img);g.ov=mkOv(el)},
 cam(g,t){g.el.querySelector('.blur').style.transform=`scale(${1.03+.04*cl(t,g.B,g.E)})`},
 ov(g,t){const {j}=SC.chart.step(g,t);const cs=[0,1,2].map(q=>q<g.n?ctx(g.i0+q,t):null);let h='';
  const R=[['Stayed fully invested',10.4,COL.green,'≈ $72,000',0,/^stayed|^fully/i],['Missed the 10 best days',6.1,'#ffb347','≈ $33,000',1,/^missed/i],['Missed the 20 best days',3.6,'#ff7a45','≈ $20,000',2,/^twenty$/i],['Missed the 30 best days',1.4,COL.red,'≈ $13,000',2,/^thirty$/i]];
  h+=T(960,92,'S&P 500, 2005–2024 · $10,000 start',{size:44,col:COL.gold,p:cs[0].a(.05,.5)});
  h+=T(960,146,'return per year · final value of $10,000',{size:26,w:500,col:COL.muted,p:cs[0].a(.2,.5)});
  R.forEach(([lab,v,col,dol,step,re],r)=>{if(step>j)return;const c=cs[step],tt=c.fx(r==0?'pop':'thud',c.w(re,.3)+(r==3?.9:0)),p=ei(c.r(tt,.9)),y=290+r*135,bw=Math.max(8,v/10.4*1000*p);
   h+=T(150,y-52,lab,{al:'l',size:32,col:COL.cream,p:Math.min(1,p*3)});
   h+=`<div style="position:absolute;left:150px;top:${y-24}px;width:${bw.toFixed(1)}px;height:62px;border-radius:0 16px 16px 0;background:${col};box-shadow:0 8px 20px #0007"></div>`;
   h+=T(150+bw+24,y+7,`${(v*Math.min(1,p*1.2)).toFixed(1)} %`,{al:'l',size:56,col,p:Math.min(1,p*3)});
   h+=T(150+bw+24+(v>5?210:190),y+7,dol,{al:'l',size:34,col:COL.cream2,w:500,p:Math.min(1,p*3)})});
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
  const pn=c.r(tn,.6);if(pn>0)h+=`<div style="position:absolute;left:1100px;top:110px;width:740px;height:150px;border-radius:26px;background:#24150cee;box-shadow:0 20px 40px #0009;border:3px solid ${COL.gold}66;transform:translateX(${((1-ez(pn))*800).toFixed(1)}px);display:flex;align-items:center;gap:26px;padding:0 30px;box-sizing:border-box">${ic('cal',90,COL.gold)}<div><div style="font:500 26px P;color:${COL.muted}">Next video</div><div style="font:700 38px/1.15 P;color:${COL.cream}">30 years of small deposits</div></div></div>`;
  return h}};
