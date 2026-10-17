// ---------------------------------------------------------------- extra icons (100x100 box)
Object.assign(ICN,{
 house:c=>`<path d="M10 50 L50 14 L90 50 V90 H10 Z" fill="${c}"/><rect x=40 y=60 width=20 height=30 fill="#24150c"/><path d="M4 52 L50 10 L96 52" fill=none stroke="#24150c" stroke-width=6 stroke-linejoin=round />`,
 car:c=>`<path d="M10 62 L20 40 C24 32 30 30 38 30 H64 C72 30 78 34 82 42 L90 62 V76 H10 Z" fill="${c}"/><rect x=30 y=38 width=36 height=16 rx=4 fill="#24150c55"/><circle cx=30 cy=78 r=10 fill="#24150c"/><circle cx=72 cy=78 r=10 fill="#24150c"/>`,
 phone:c=>`<rect x=28 y=6 width=44 height=88 rx=10 fill="${c}"/><rect x=33 y=16 width=34 height=62 rx=3 fill="#24150c"/><circle cx=50 cy=86 r=4 fill="#24150c"/>`,
 plane:c=>`<path d="M48 8 C54 8 56 16 56 24 V40 L92 60 V70 L56 60 V80 L68 88 V94 L50 89 L32 94 V88 L44 80 V60 L8 70 V60 L44 40 V24 C44 16 44 8 48 8 Z" fill="${c}"/>`,
 bank:c=>`<path d="M50 6 L94 30 H6 Z" fill="${c}"/><rect x=8 y=82 width=84 height=12 fill="${c}"/><path d="M20 38 V76 M40 38 V76 M60 38 V76 M80 38 V76" stroke="${c}" stroke-width=10 />`,
 doc:c=>`<path d="M20 6 H64 L82 24 V94 H20 Z" fill="${c}"/><path d="M32 40 H70 M32 56 H70 M32 72 H58" stroke="#24150c66" stroke-width=6 stroke-linecap=round />`,
 cart:c=>`<path d="M6 16 H22 L32 66 H82 L92 30 H26" fill=none stroke="${c}" stroke-width=9 stroke-linejoin=round stroke-linecap=round /><circle cx=38 cy=84 r=8 fill="${c}"/><circle cx=76 cy=84 r=8 fill="${c}"/>`,
 bread:c=>`<path d="M14 44 C14 22 86 22 86 44 C86 52 80 54 78 56 V84 H22 V56 C20 54 14 52 14 44 Z" fill="${c}"/><path d="M38 40 L46 30 M54 40 L62 30" stroke="#24150c55" stroke-width=5 stroke-linecap=round />`,
 bolt:c=>`<path d="M58 4 L18 56 H46 L38 96 L82 40 H54 Z" fill="${c}"/>`,
 gear:c=>`<circle cx=50 cy=50 r=26 fill=none stroke="${c}" stroke-width=14 /><path d="M50 6 V22 M50 78 V94 M6 50 H22 M78 50 H94 M19 19 L30 30 M70 70 L81 81 M81 19 L70 30 M30 70 L19 81" stroke="${c}" stroke-width=13 stroke-linecap=round />`,
 bulb:c=>`<path d="M50 6 C28 6 18 22 18 38 C18 52 28 58 32 68 H68 C72 58 82 52 82 38 C82 22 72 6 50 6 Z" fill="${c}"/><rect x=34 y=74 width=32 height=8 rx=3 fill="${c}"/><rect x=38 y=86 width=24 height=8 rx=3 fill="${c}"/>`,
 ticket:c=>`<path d="M6 26 H94 V42 C86 42 86 58 94 58 V74 H6 V58 C14 58 14 42 6 42 Z" fill="${c}"/><path d="M66 30 V70" stroke="#24150c55" stroke-width=4 stroke-dasharray="6 6"/>`,
 oil:c=>`<path d="M50 6 C50 6 18 46 18 64 C18 82 32 94 50 94 C68 94 82 82 82 64 C82 46 50 6 50 6 Z" fill="${c}"/><path d="M34 66 C34 76 40 82 48 82" fill=none stroke="#ffffff66" stroke-width=6 stroke-linecap=round />`,
 bed:c=>`<rect x=8 y=50 width=84 height=22 rx=6 fill="${c}"/><rect x=12 y=36 width=26 height=16 rx=6 fill="${c}"/><path d="M8 30 V86 M92 60 V86" stroke="${c}" stroke-width=8 stroke-linecap=round />`,
 truck:c=>`<rect x=6 y=26 width=56 height=44 rx=4 fill="${c}"/><path d="M62 40 H80 L94 56 V70 H62 Z" fill="${c}"/><circle cx=24 cy=76 r=10 fill="#24150c"/><circle cx=78 cy=76 r=10 fill="#24150c"/>`,
 wheat:c=>`<path d="M50 94 V30" stroke="${c}" stroke-width=7 stroke-linecap=round />${[0,1,2].map(k=>`<ellipse cx=40 cy=${36+k*16} rx=10 ry=6 transform="rotate(-35 40 ${36+k*16})" fill="${c}"/><ellipse cx=60 cy=${36+k*16} rx=10 ry=6 transform="rotate(35 60 ${36+k*16})" fill="${c}"/>`).join('')}<ellipse cx=50 cy=20 rx=7 ry=12 fill="${c}"/>`,
 cross2:c=>`<rect x=36 y=10 width=28 height=80 rx=6 fill="${c}"/><rect x=10 y=36 width=80 height=28 rx=6 fill="${c}"/>`,
 brush:c=>`<rect x=44 y=6 width=12 height=50 rx=5 fill="${c}"/><path d="M30 56 H70 L76 94 H24 Z" fill="${c}"/>`,
 scissors:c=>`<circle cx=24 cy=74 r=13 fill=none stroke="${c}" stroke-width=8 /><circle cx=76 cy=74 r=13 fill=none stroke="${c}" stroke-width=8 /><path d="M32 64 L80 8 M68 64 L20 8" stroke="${c}" stroke-width=8 stroke-linecap=round />`,
});
// little cartoon face (matches the channel character)
function face(x,y,r,p,o={}){if(p<=0)return'';const s=bo(p);return `<g transform="translate(${x},${y}) scale(${s.toFixed(3)})" opacity=${Math.min(1,p*2).toFixed(2)}><circle r=${r} fill="${o.col||'#f6e3b4'}" stroke="#24150c" stroke-width=${Math.max(2,r/9)} /><circle cx=${-r*.32} cy=${-r*.12} r=${r*.09} fill="#24150c"/><circle cx=${r*.32} cy=${-r*.12} r=${r*.09} fill="#24150c"/><path d="M${-r*.4} ${r*.22} Q0 ${r*(o.sad?.05:.62)} ${r*.4} ${r*.22}" fill=${o.sad?'none':'"#fff"'} stroke="#24150c" stroke-width=${Math.max(2,r/12)} /></g>`}
// sequential chip list: items [text, icon, wordRegex, fallbackFrac, opts]
function clist(c,x,y0,dy,items,o={}){let h='';items.forEach(([txt,icn,re,f,io={}],k)=>{const tt=c.fx(io.sfx||o.sfx||'pop',re?c.w(re,f):f*c.D);
  h+=chip(x,y0+k*dy,txt,Object.assign({p:c.r(tt,.5),size:o.size||44,al:o.al,bg:o.bg||'#fbf0daf2',fg:o.fg||COL.brown,ic:icn?ic(icn,(o.size||44)*1.05,io.icol||o.icol||COL.brown):''},io))});return h}
// count a number between two times
function cnt(c,t0,d,a,b,pw=1){return lerp(a,b,Math.pow(ei(c.r(t0,d)),pw))}
const big=v=>v>=1e15?'$'+(v/1e15).toFixed(1)+' quadrillion':v>=1e12?'$'+(v/1e12).toFixed(v<1e13?1:0)+' trillion':v>=1e9?'$'+(v/1e9).toFixed(1)+' billion':v>=1e6?'$'+(v/1e6).toFixed(v<1e7?2:0)+' million':fmt(v);

const OV={
// ---- 1: everyone got it
everyone(c){const t0=c.fx('swish',.05);let h='',s='';
 h+=box(110,90,1700,300,{p:c.a(t0,.5)});
 const P=[['Your neighbor',/neighbor/i,.18],['Your boss',/boss/i,.32],['The barista',/barista/i,.55]];
 P.forEach(([lab,re,f],k)=>{const tt=c.fx('pop',c.w(re,f)),p=c.r(tt,.5),x=330+k*420;s+=face(x,195,62,p);
  h+=T(x,300,lab,{size:34,p});h+=chip(x+70,140,'+$1M',{p:c.r(tt+.25,.45),size:28,bg:COL.green2+'f2'});if(p>0)c.fx('coin',tt+.25,{n:2})});
 const te=c.fx('impact',c.w(/Every/,.8)),pe=c.r(te,.6);
 for(let k=0;k<40;k++){const p=c.r(te+k*.02,.4);s+=face(1440+(k%10)*34,140+Math.floor(k/10)*40,14,p)}
 h+=svg(s);
 h+=chip(960,470,`${ic('globe',58,'#7cc3ff')}<span>Every person on Earth</span>`,{p:pe,size:52,bg:`linear-gradient(90deg,${COL.gold2},${COL.gold})`,fg:COL.brown});
 return h},
// ---- 2: no catch
nocatch(c,g){const cx=g.cx;let h='';const t0=c.fx('swish',.05);
 h+=T(cx,165,'The deal',{size:46,col:COL.gold,p:c.a(t0,.5)});
 [['No catch',/catch/i,.15],['No taxes',/taxes/i,.3],['No strings',/strings/i,.45]].forEach(([s,re,f],k)=>{const tt=c.fx('tick',c.w(re,f),{f:2000+k*200});
  h+=chip(cx,270+k*105,s,{p:c.r(tt,.45),size:44,bg:'#ffffff14',ic:ic('cross',40,COL.red)})});
 const tm=c.fx('cash',c.w(/moment/i,.9)),pm=c.r(tm,.6);
 h+=chip(cx,640,`${ic('coin',56,'#ffe08a')}$1,000,000`,{p:pm,size:62,bg:`linear-gradient(90deg,${COL.gold2},${COL.gold})`,fg:COL.brown});
 h+=T(cx,730,'for everyone · same moment',{size:30,w:500,col:COL.cream2,p:pm});
 return h},
// ---- 3: honest notepad
honest(c){const x=1225,y=150,t0=c.fx('swish',.05);let h='';
 const items=[['Play it through',c.w(/play/i,.45)],['Step by step',c.w(/step/i,.65)],['Real numbers',c.w(/real/i,.85)]];
 let rules='';for(let k=0;k<9;k++)rules+=`<div style="position:absolute;left:0;right:0;top:${120+k*60}px;height:2px;background:#c9a87a55"></div>`;
 h+=box(x,y,600,600,{p:c.a(t0,.6),bg:'#fbf0da',bd:'0',html:rules+`<div style="position:absolute;left:66px;top:0;bottom:0;width:3px;background:#e0786a88"></div>`});
 h+=T(x+300,y+66,'The plan',{size:48,col:COL.brown,sh:0,p:c.a(t0+.2,.5)});
 items.forEach(([s,tt],k)=>{c.fx('tick',tt,{f:2200});const p=c.a(tt-.15,.35),yy=y+190+k*130;
  h+=`<div style="position:absolute;left:${x+90}px;top:${yy-30}px;width:60px;height:60px;border-radius:12px;border:5px solid ${COL.brown};opacity:${c.a(t0+.3,.4)}"></div>`;
  h+=icAt('check',x+122,yy-4,78,COL.green2,p);
  h+=T(x+180,yy,s,{al:'l',size:42,col:COL.brown,sh:0,p:c.a(t0+.3+k*.1,.4)});
  if(p>0)h+=`<div style="position:absolute;left:${x+176}px;top:${yy+28}px;height:6px;border-radius:3px;background:${COL.gold2};width:${(ez(p)*330).toFixed(0)}px"></div>`});
 return h},
// ---- 4: spoiler
spoiler(c){const t0=c.fx('swish',.05),te=c.fx('impact',c.w(/expensive/i,.75));let h='';
 h+=box(100,100,720,330,{p:c.a(t0,.5)});
 h+=chip(220,165,'SPOILER',{p:c.a(t0+.1,.4),size:30,bg:COL.red,fg:'#fff',r:10});
 h+=T(140,260,'Free money<br>for everyone',{al:'l',size:62,lh:1.1,p:c.a(t0+.2,.5)});
 h+=stamp(1340,250,'MOST EXPENSIVE IDEA?',c.r(te,.35),{size:60,rot:-5,col:COL.gold});
 return h},
// ---- 8: 22 million years
spendtime(c,g){const cx=g.cx,t0=c.fx('swish',.05),t1=c.w(/spent/i,.3),t2=c.w(/twenty/i,.75);let h='';
 h+=T(cx,165,'Spend $1,000,000 …',{size:44,p:c.a(t0,.5)});h+=T(cx,225,'… every single day',{size:36,col:COL.muted,p:c.a(t0+.2,.5)});
 const flip=Math.floor(Math.max(0,c.lt-t1)*6);if(c.lt>t1&&c.lt<t2+1.5&&flip%2==0)c.lt;
 for(let k=0;k<3;k++){const p=c.a(t1+k*.12,.4);h+=`<div style="position:absolute;left:${cx-210+k*140}px;top:300px;width:120px;height:130px;border-radius:16px;background:#fbf0da;opacity:${p};transform:translateY(${((1-p)*30).toFixed(0)}px) rotate(${(k-1)*4}deg);box-shadow:0 12px 24px #0008;overflow:hidden"><div style="height:34px;background:#c8432f"></div><div style="font:700 50px/90px P;color:${COL.brown};text-align:center">${(Math.floor(cnt(c,t1,Math.max(1,t2-t1),1,365))+k*7)%31+1}</div></div>`}
 const yrs=cnt(c,t2-.6,1.6,0,22000000,1.3);c.fx('tick',t2-.6,{f:1800});const td=c.fx('ding',t2+1.1);
 h+=T(cx,560,MG.fmt(Math.round(yrs/1000)*1000),{size:96,col:COL.gold,p:c.r(t2-.6,.3),sh:`0 0 40px #ffc94a55,${SH}`});
 h+=T(cx,640,'years to spend it all',{size:38,p:c.r(t2-.4,.4)});
 h+=chip(cx,740,'≈ 22 million years',{p:c.r(td,.5),size:36,bg:COL.green2+'f0'});
 return h},
// ---- 13: money printer
printer(c,g){const cx=g.cx,t0=c.fx('whoosh',.05,{d:.8});let h='',s='';
 h+=T(cx,160,'New money needed',{size:44,p:c.a(t0,.5)});
 const pp=c.a(t0+.2,.5);
 s+=`<g opacity=${pp}><rect x=${cx-200} y=300 width=400 height=170 rx=24 fill="#5b4636" stroke="#2c1a0f" stroke-width=6 /><rect x=${cx-150} y=270 width=300 height=40 rx=8 fill="#3a2a20"/><rect x=${cx-170} y=440 width=340 height=24 rx=6 fill="#1d120b"/><circle cx=${cx+150} cy=345 r=12 fill="${COL.green}"/><circle cx=${cx+150} cy=345 r=${12+6*Math.abs(Math.sin(c.lt*6))} fill=none stroke="${COL.green}" stroke-width=3 opacity=.6 /></g>`;
 for(let k=0;k<6;k++){const ph=((c.lt-.6)*1.4+k/6)%1;if(c.lt<.6+k*.12)continue;const y=455+ph*230,op=ph<.85?1:(1-ph)/.15;
  s+=`<g transform="translate(${cx-120+Math.sin(k*2.1)*20},${y.toFixed(1)}) rotate(${(Math.sin(k*1.7+ph*4)*12).toFixed(1)})" opacity=${(op*pp).toFixed(2)}><rect width=240 height=110 rx=10 fill="#7fbf7a" stroke="#2f6b3a" stroke-width=5 /><circle cx=120 cy=55 r=30 fill="#a9dba1" stroke="#2f6b3a" stroke-width=4 /><text x=120 y=70 text-anchor=middle font-family="P" font-weight=700 font-size=40 fill="#2f6b3a">$</text></g>`}
 if(c.lt>.6&&Math.floor(c.lt*4)!=Math.floor((c.lt-1/30)*4));for(let k=0;k<5;k++)c.fx('paper',.8+k*.7);
 h=svg(s)+h;
 const tth=c.fx('impact',c.w(/thin/i,.45)),tc=c.fx('error',c.w(/crack/i,.85));
 h+=stamp(cx,740,'OUT OF THIN AIR',c.r(tth,.35),{size:46,rot:-4,col:COL.gold});
 h+=chip(cx,860-40,'first crack in the dream',{p:c.r(tc,.5),size:30,bg:'#7a2318ee',ic:ic('warn',32,COL.gold)});
 return h},
// ---- 15: debts gone
debtsgone(c,g){const cx=g.cx,t0=c.fx('swish',.05);let h='';
 h+=T(cx,165,'Debts',{size:46,col:COL.gold,p:c.a(t0,.5)});
 [['Credit cards','−$6,000',/Credit/i,.35],['Student loans','−$35,000',/student/i,.5],['Mortgage','−$240,000',/mortgages/i,.7]].forEach(([lab,v,re,f],k)=>{const y=280+k*130,tt=c.fx('cash',c.w(re,f)+.2),p=c.a(t0+.15+k*.1,.4),q=ez(c.r(tt,.4));
  h+=box(cx-280,y-50,560,100,{p,r:20,bg:'#24150cee'});
  h+=T(cx-250,y,lab,{al:'l',size:36,p,col:q>0?'#cdb495':COL.cream});h+=T(cx+250,y,v,{al:'r',size:36,col:COL.red,p:p*(1-q)});
  if(q>0)h+=`<div style="position:absolute;left:${cx-260}px;top:${y-4}px;height:8px;width:${(q*300).toFixed(0)}px;background:${COL.red};border-radius:4px"></div>`;
  h+=stamp(cx+170,y,'PAID',q,{size:34,rot:-8,col:COL.green})});
 const tk=c.fx('tap',c.w(/click/i,.9));h+=chip(cx,700,'one click',{p:c.r(tk,.5),size:38,bg:COL.green2+'f0',ic:ic('check',38,'#fff')});
 return h},
// ---- 16: shopping
cart(c){const t0=c.fx('swish',.05);let h='',s='';
 h+=box(1170,90,660,560,{p:c.a(t0,.5)});
 h+=T(1500,150,'Shopping list',{size:42,col:COL.gold,p:c.a(t0+.1,.4)});
 const it=[['plane','Vacation',4800,/vacations/i,.25],['phone','New phone',1200,/phones/i,.5],['car','Dream car',85000,/car/i,.85]];let tot=0;
 it.forEach(([icn,lab,v,re,f],k)=>{const tt=c.fx('cash',c.w(re,f)),p=c.r(tt,.5),y=250+k*110;tot+=v*ez(c.r(tt,.6));
  h+=icAt(icn,1240,y,64,COL.cream2,p);h+=T(1290,y,lab,{al:'l',size:38,p});h+=T(1790,y,fmt(v,'$'),{al:'r',size:36,col:COL.gold,p});if(p>0)h+=icAt('check',1770-0,y-36,0,COL.green,0)});
 h+=`<div style="position:absolute;left:1210px;top:560px;width:580px;height:3px;background:#ffffff33;opacity:${c.a(t0+.2,.4)}"></div>`;
 h+=T(1240,605,'Spent',{al:'l',size:34,col:COL.muted,p:c.a(t0+.3,.4)});h+=T(1790,605,fmt(tot,'$'),{al:'r',size:44,col:COL.green,p:c.a(t0+.3,.4)});
 return h},
// ---- 17: sold out
soldout(c,g){const cx=g.cx,t0=c.fx('swish',.05);let h='';
 const tr=c.w(/Restaurants/i,.2),tw=c.w(/weeks/i,.45);
 h+=T(cx,160,'Restaurant: next free table',{size:36,p:c.a(t0,.5)});
 for(let k=0;k<28;k++){const p=c.r(tr+.2+k*.04,.25),x=cx-245+(k%7)*72,y=215+Math.floor(k/7)*58;if(k%7==0)c.fx('tick',tr+.2+k*.04,{f:1600+k*30});
  h+=`<div style="position:absolute;left:${x}px;top:${y}px;width:62px;height:48px;border-radius:8px;background:${p>0?'#c8432f':'#ffffff14'};opacity:${(.4+.6*Math.min(1,p*2)).toFixed(2)};font:700 22px/48px P;color:#fff;text-align:center">${p>0?'✕':''}</div>`}
 h+=chip(cx,480,'booked out for weeks',{p:c.r(tw+.3,.5),size:30,bg:'#24150cee'});
 const tc=c.fx('impact',c.w(/weekend/i,.9));
 h+=icAt('car',cx-150,640,120,COL.cream2,c.a(c.w(/Car/i,.6),.4));
 h+=stamp(cx+90,640,'SOLD OUT',c.r(tc,.35),{size:56,rot:-8});
 return h},
// ---- 18: quit on the spot
quit(c,g){const cx=g.cx,x=cx-280,y=170,t0=c.fx('swish',.05),t1=.5,msg='Dear boss, I quit. Have a nice life!',t2=Math.max(t1+1.6,c.D*.6);c.fx('type',t1,{n:12});c.fx('type',t1+.9,{n:12});let h='';
 const n=Math.floor(msg.length*cl(c.lt,t1,t2));
 h+=box(x,y,560,420,{p:c.a(t0,.5),bg:'#fbf0da',bd:'0',html:`<div style="position:absolute;left:36px;top:30px;font:700 34px P;color:${COL.brown}">Resignation</div><div style="position:absolute;left:36px;top:80px;width:470px;height:3px;background:#c9a87a"></div><div style="position:absolute;left:36px;top:110px;width:480px;font:500 40px/1.35 P;color:${COL.brown}">${msg.slice(0,n)}<span style="opacity:${Math.floor(c.lt*2.2)%2&&c.lt<t2+.5?1:0};color:${COL.gold2}">|</span></div>`});
 const tq=c.fx('impact',c.w(/quit/i,.9));h+=stamp(cx,650,'QUIT!',c.r(tq,.35),{size:70,rot:-6});
 return h},
// ---- 19: orders explode
orders(c,g){const x0=110,x1=690,y0=230,y1=640,t0=c.fx('swish',.05),ts=c.fx('riser',c.w(/shoot/i,.55)-1.2,{d:1.4}),tc=c.fx('error',c.w(/crash/i,.15)+.3);let h='',s='';
 const P=[.1,.12,.11,.13,.12,.14,.13,.15];const ts2=c.w(/shoot/i,.55);
 s+=`<rect x=${x0-30} y=${y0-60} width=${x1-x0+60} height=${y1-y0+110} rx=24 fill="#24150cdd" opacity=${c.a(t0,.4)} />`;
 const up=ez(c.r(ts2,1.2));const pts=P.map((v,k)=>[x0+k/10*(x1-x0),y1-v*(y1-y0)]);for(let k=8;k<=10;k++)pts.push([x0+k/10*(x1-x0),y1-lerp(.15,[.35,.7,1.02][k-8],up)*(y1-y0)]);
 const pd=ei(c.r(.2,1.2))*(pts.length-1);let d='';for(let k=0;k<=Math.floor(pd)&&k<pts.length;k++)d+=(k?'L':'M')+pts[k][0].toFixed(1)+' '+pts[k][1].toFixed(1);
 s+=`<path d="${d}" fill=none stroke="${COL.green}" stroke-width=8 stroke-linejoin=round stroke-linecap=round />`;
 h+=svg(s);h+=T(x0,y0-20,'Online orders',{al:'l',size:36,p:c.a(t0,.5)});
 h+=icAt('up',x1-20,y0+20,70,COL.green,up);
 h+=chip(400,y1+110,'Error 503 · server overloaded',{p:c.r(tc,.5),size:28,bg:'#7a2318ee',ic:ic('warn',30,COL.gold)});
 return h},
// ---- 20: everyone a lottery winner
winner(c){const t0=c.fx('swish',.05),tw=c.fx('chime',c.w(/winner/i,.5)),te=c.fx('pop',c.w(/everyone/i,.85));let h='';
 h+=box(1180,110,640,330,{p:c.a(t0,.5),bg:'#fbf0da',bd:'4px dashed #c8432f'});
 h+=T(1500,180,'LOTTERY TICKET',{size:38,col:COL.brown,sh:0,ls:4,p:c.a(t0+.1,.4)});
 for(let k=0;k<6;k++){const p=c.a(t0+.2+k*.08,.3);h+=`<div style="position:absolute;left:${1240+k*96}px;top:230px;width:78px;height:78px;border-radius:50%;background:${COL.gold};font:700 36px/78px P;color:${COL.brown};text-align:center;opacity:${p};transform:scale(${bo(p).toFixed(3)})">${[7,13,21,28,35,42][k]}</div>`}
 h+=stamp(1500,380,'WINNER',c.r(tw,.35),{size:58,rot:-5,col:COL.green});
 h+=chip(1500,520,'… everyone',{p:c.r(te,.5),size:42,bg:'#24150cee',ic:ic('globe',44,'#7cc3ff')});
 return h},
// ---- 23: price tags
tags(c){const t0=c.fx('swish',.05),tr=c.fx('cash',c.w(/raise/i,.8));let h='',s='';
 const T3=[['Bread',3,'bread'],['Jeans',60,'doc'],['Rent',1500,'house']];
 T3.forEach(([lab,v,icn],k)=>{const x=1240+k*210,sw=Math.sin(c.lt*2.2+k)*4,p=c.a(t0+k*.15,.5),q=ez(c.r(tr+k*.15,.6)),vv=v*lerp(1,3,q);
  s+=`<line x1=${x+70} y1=60 x2=${x+70} y2=${130} stroke="#f2dcb5" stroke-width=3 opacity=${p} />`;
  h+=`<div style="position:absolute;left:${x}px;top:130px;width:140px;height:210px;transform-origin:70px 0;transform:rotate(${sw.toFixed(2)}deg) translateY(${((1-p)*-80).toFixed(0)}px);opacity:${p}"><div style="position:absolute;inset:0;border-radius:18px 18px 18px 18px;background:#fbf0da;box-shadow:0 14px 26px #0008"></div><div style="position:absolute;left:58px;top:12px;width:24px;height:24px;border-radius:50%;background:#24150c"></div><div style="position:absolute;left:0;right:0;top:46px;text-align:center">${ic(icn,56,COL.coffee)}</div><div style="position:absolute;left:0;right:0;top:110px;text-align:center;font:500 24px P;color:${COL.brown}">${lab}</div><div style="position:absolute;left:0;right:0;top:146px;text-align:center;font:700 ${vv>999?32:38}px P;color:${q>0?COL.red:COL.brown}">${fmt(vv,'$')}</div></div>`;
  h+=icAt('up',x+130,150,44,COL.red,q)});
 return svg(s)+h},
// ---- 24: auction
auction(c,g){const cx=g.cx,t0=c.fx('swish',.05);let h='',s='';
 h+=box(cx-220,140,440,300,{p:c.a(t0,.5),bg:'#6b4a2a',bd:'10px solid #c8a060',html:`<div style="position:absolute;inset:18px;background:linear-gradient(160deg,#7cc3ff,#3a6f9a 60%,#2d5a3a 61%,#3f7a4a);border-radius:6px"></div><div style="position:absolute;left:150px;top:60px;width:70px;height:70px;border-radius:50%;background:#ffe08a"></div>`});
 const tp=c.fx('tick',c.w(/painting/i,.55),{f:2000}),tb=c.w(/bids/i,.85);
 h+=chip(cx,490,'same painting',{p:c.r(tp,.5),size:32,bg:'#24150cee',ic:ic('check',32,COL.green)});
 const v=c.lt<tb-.2?1000:cnt(c,tb-.2,1.2,1000,1000000,2.2);for(let k=0;k<4;k++)c.fx('beep',tb-.2+k*.3,{f:1300+k*180});
 h+=T(cx,620,'Highest bid',{size:30,col:COL.muted,p:c.a(.6,.4)});
 h+=T(cx,690,fmt(v,'$'),{size:80,col:c.lt>tb?COL.gold:COL.cream,p:c.a(.6,.4),sh:`0 0 30px #ffc94a44,${SH}`});
 const pb=c.r(tb,.4);if(pb>0)h+=`<div style="position:absolute;left:${cx+150}px;top:${560-20*Math.sin(pb*Math.PI)}px;transform:rotate(${(-20+20*Math.sin(c.lt*3)).toFixed(1)}deg)"><div style="width:90px;height:90px;border-radius:50%;background:${COL.red};border:5px solid #fff;font:700 36px/80px P;color:#fff;text-align:center">${Math.floor(cl(c.lt,tb,tb+1.2)*40)+12}</div><div style="width:14px;height:70px;background:#c8a060;margin:-4px auto 0;border-radius:4px"></div></div>`;
 return h},
// ---- 25: coffee price ×10 ×10
coffeeprice(c,g){const cx=g.cx,t0=c.fx('swish',.05);let h='';
 const st=[['Yesterday',4,/four/i,.2],['Next week',40,/forty/i,.5],['Weeks later',400,/hundred/i,.85]];
 h+=icAt('cup',cx,190,120,COL.cream2,c.a(t0,.5));
 st.forEach(([lab,v,re,f],k)=>{const tt=c.fx(k?'impact':'pop',c.w(re,f)),p=c.r(tt,.5),y=360+k*150;
  h+=T(cx-260,y,lab,{al:'l',size:32,col:COL.muted,p});
  h+=chip(cx+150,y,fmt(v,'$'),{p,size:k==2?78:k?64:50,bg:k==2?COL.red:k?'#c8601f':'#24150cee',fg:'#fff'});
  if(k)h+=T(cx+150+(k==2?170:140),y-50,'×10',{al:'l',size:34,col:COL.gold,p:c.r(tt+.2,.4)})});
 return h},
// ---- 26: rent
rent(c){const t0=c.fx('swish',.05),tj=c.fx('riser',Math.max(0,c.w(/jump/i,.15)-.6),{d:.9}),th=c.fx('thud',c.w(/homes/i,.9));let h='',s='';
 h+=box(100,100,700,460,{p:c.a(t0,.5)});
 h+=T(140,160,'Monthly rent',{al:'l',size:40,p:c.a(t0+.1,.4)});
 const v=cnt(c,c.w(/jump/i,.15),2.2,1500,6000,1.6);h+=T(760,160,fmt(v,'$'),{al:'r',size:56,col:v>1600?COL.red:COL.cream,p:c.a(t0+.1,.4)});
 for(let k=0;k<5;k++){const p=c.a(t0+.2+k*.08,.4),x=170+k*120;h+=icAt('house',x,320,90,k<5?COL.cream2:COL.cream,p)}
 const pe=c.r(c.w(/everybody/i,.55),.8);for(let k=0;k<12;k++)s+=face(150+k*52,450,20,c.r(c.w(/everybody/i,.55)+k*.05,.35));
 h+=svg(s);
 h+=chip(450,620,'more buyers · same number of homes',{p:c.r(th,.5),size:30,bg:'#7a2318ee'});
 return h},
// ---- 27: re-tagging all day
retag(c,g){const cx=g.cx,t0=c.fx('swish',.05);let h='';
 h+=T(cx,165,'Same product, same day',{size:40,p:c.a(t0,.5)});
 [['9:00',5],['12:00',8],['15:00',12],['18:00',19]].forEach(([tm,v],k)=>{const tt=c.fx('click',.6+k*Math.max(.5,(c.D-1.5)/4)),p=c.r(tt,.4),y=270+k*120;
  h+=chip(cx-160,y,tm,{p,size:34,bg:'#24150cee',ic:ic('clock',34,COL.gold)});
  h+=chip(cx+120,y,fmt(v,'$'),{p,size:44,bg:'#fbf0daf2',fg:k?COL.red:COL.brown,rot:-3+k*2})});
 return h},
// ---- 28: essentials first
essentials(c,g){const cx=g.cx,t0=c.fx('swish',.05);let h='';
 h+=T(cx,165,'Rises first',{size:46,col:COL.red,p:c.a(t0,.5)});
 [['bread','Food',/food/i,.3],['house','Housing',/housing/i,.4],['bolt','Energy',/energy/i,.5]].forEach(([icn,lab,re,f],k)=>{const tt=c.fx('pop',c.w(re,f)),p=c.r(tt,.5),x=cx-200+k*200,u=ez(c.r(tt+.3,1));
  h+=icAt(icn,x,330,110,COL.cream2,p);h+=T(x,420,lab,{size:34,p});
  h+=`<div style="position:absolute;left:${x-26}px;top:${720-200*u}px;width:52px;height:${(200*u).toFixed(0)}px;border-radius:10px 10px 0 0;background:linear-gradient(180deg,${COL.red},#7a2318)"></div>`;h+=icAt('up',x,700-200*u,50,COL.red,u)});
 h+=chip(cx,780,'nobody can do without',{p:c.r(c.w(/without/i,.9),.5),size:30,bg:'#24150cee'});
 return h},
// ---- 29: inflation gauge
hyper(c){const t0=c.fx('swish',.05),ti=c.fx('pop',c.w(/inflation\./i,.25)),th=c.fx('impact',c.w(/hyperinflation/i,.85));let h='',s='';
 const x=230,y0=180,y1=700,lev=c.lt<th?lerp(.05,.32,ez(c.r(ti,.8))):lerp(.32,1,ez(c.r(th,.5)))+.01*Math.sin(c.lt*30)*(c.lt>th?1:0);
 s+=`<g opacity=${c.a(t0,.5)}><rect x=${x-40} y=${y0} width=80 height=${y1-y0} rx=40 fill="#fbf0da"/><circle cx=${x} cy=${y1+40} r=70 fill="${lev>.5?COL.red:COL.gold2}"/><rect x=${x-22} y=${y1-(y1-y0-30)*lev} width=44 height=${(y1-y0-30)*lev+40} rx=22 fill="${lev>.5?COL.red:COL.gold2}"/></g>`;
 h+=svg(s);
 h+=chip(x+90,y1-(y1-y0)*.3,'Inflation · a few % a year',{al:'l',p:c.r(ti,.5),size:34,bg:'#24150cee'});
 h+=chip(x+90,y0+40,'HYPERINFLATION',{al:'l',p:c.r(th,.4),size:52,bg:COL.red,fg:'#fff'});
 h+=T(x+110,y0+120,'often defined as 50 %+ per month',{al:'l',size:28,w:500,col:COL.cream2,p:c.r(th+.4,.5)});
 return h},
// ---- 30: history timeline
history(c,g){const cx=g.cx,t0=c.fx('swish',.05),tb=c.fx('thud',c.w(/badly/i,.9));let h='',s='';
 h+=T(cx,165,'It happened before',{size:46,p:c.a(t0,.5)});
 const pl=ez(c.r(.4,1.2));s+=`<line x1=${cx} y1=260 x2=${cx} y2=${260+460*pl} stroke="${COL.gold}" stroke-width=6 stroke-linecap=round />`;h+=svg(s);
 [['1923','Germany'],['1946','Hungary'],['2008','Zimbabwe']].forEach(([y,n],k)=>{const tt=c.fx('pop',.6+k*.45),p=c.r(tt,.5),yy=300+k*170;
  h+=`<div style="position:absolute;left:${cx-16}px;top:${yy-16}px;width:32px;height:32px;border-radius:50%;background:${COL.gold};transform:scale(${bo(p).toFixed(3)})"></div>`;
  h+=T(cx-40,yy,y,{al:'r',size:52,col:COL.gold,p});h+=T(cx+40,yy,n,{al:'l',size:42,p})});
 h+=chip(cx,790,'it went very badly',{p:c.r(tb,.5),size:32,bg:'#7a2318ee'});
 return h},
// ---- 33: paid twice a day
wages(c){const t0=c.fx('swish',.05);let h='',s='';
 h+=box(1160,100,660,520,{p:c.a(t0,.5)});
 const tp=c.fx('bell',c.w(/twice/i,.35));
 h+=T(1490,165,'Payday',{size:44,col:COL.gold,p:c.a(t0+.1,.4)});
 h+=chip(1490,240,'once or twice a day',{p:c.r(tp,.5),size:34,bg:'#24150cee',ic:ic('clock',36,COL.gold)});
 const hr=Math.max(0,c.lt-c.w(/rushed/i,.55));const v=Math.max(.05,Math.pow(.5,hr*1.1));
 h+=T(1200,330,'What your wage buys',{al:'l',size:32,col:COL.muted,p:c.a(t0+.3,.4)});
 h+=`<div style="position:absolute;left:1200px;top:370px;width:580px;height:60px;border-radius:14px;background:#ffffff14;opacity:${c.a(t0+.3,.4)}"><div style="height:100%;width:${(v*100).toFixed(1)}%;border-radius:14px;background:linear-gradient(90deg,${COL.red},${COL.gold})"></div></div>`;
 h+=T(1490,480,`${ic('clock',44,COL.cream2,'vertical-align:-10px;margin-right:12px')}+${Math.floor(hr*3)} hours`,{size:40,p:c.a(c.w(/rushed/i,.55),.4)});
 h+=chip(1490,560,'spend it NOW',{p:c.r(c.w(/hour/i,.95),.5),size:36,bg:COL.red,fg:'#fff'});c.fx('error',c.w(/hour/i,.95));
 return h},
// ---- 34: bundles as toys
toys(c,g){const cx=g.cx,t0=c.fx('swish',.05);let h='',s='';
 h+=T(cx,160,'Banknote building blocks',{size:40,p:c.a(t0,.5)});
 const PY=[];for(let r=0;r<5;r++)for(let i=0;i<5-r;i++)PY.push([r,i]);for(let k=0;k<15;k++){const [row,idx]=PY[k];const x=cx-225+idx*90+row*45,y=700-row*62;const tt=.5+k*.13,p=c.r(tt,.35);if(k%3==0)c.fx('thud',tt+.3);
  if(p>0)s+=`<g transform="translate(${x},${(y-(1-ez(p))*200).toFixed(1)})" opacity=${Math.min(1,p*2)}><rect width=84 height=56 rx=6 fill="#9fcf8f" stroke="#2f6b3a" stroke-width=4 /><rect x=34 y=-2 width=16 height=60 fill="#e8d7a8"/></g>`}
 h+=svg(s);
 h+=chip(cx,790,'worth more as a toy',{p:c.r(c.w(/toy/i,.85),.5),size:34,bg:'#24150cee'});
 return h},
// ---- 37: 100 trillion note
note(c,g){const cx=g.cx,t0=c.fx('swish',.05),tn=c.fx('cash',c.w(/hundred/i,.3)),tw=c.fx('thud',c.w(/worthless/i,.9));let h='';
 const p=c.r(tn,.6);
 h+=`<div style="position:absolute;left:${cx-300}px;top:200px;width:600px;height:290px;border-radius:18px;background:linear-gradient(135deg,#d9c6a0,#b9d1a0);border:6px solid #6b5a3a;box-shadow:0 24px 50px #000a;transform:rotate(-4deg) scale(${bo(p).toFixed(3)});opacity:${Math.min(1,p*2)};filter:grayscale(${cl(c.lt,tw,tw+1.2).toFixed(2)})"><div style="position:absolute;left:20px;top:16px;font:700 30px P;color:#3a2a14">RESERVE BANK</div><div style="position:absolute;left:20px;right:20px;top:80px;text-align:center;font:700 64px P;color:#3a2a14">100 TRILLION</div><div style="position:absolute;left:20px;right:20px;top:160px;text-align:center;font:500 30px P;color:#3a2a14">DOLLARS · 2008</div></div>`;
 h+=T(cx,560,'100,000,000,000,000',{size:44,col:COL.gold,p:c.r(tn+.3,.5)});
 const v=1-.97*ez(c.r(tw-.6,1));h+=T(cx-250,660,'Value',{al:'l',size:30,col:COL.muted,p:c.a(1,.4)});
 h+=`<div style="position:absolute;left:${cx-140}px;top:640px;width:390px;height:40px;border-radius:12px;background:#ffffff14;opacity:${c.a(1,.4)}"><div style="height:100%;width:${(v*100).toFixed(1)}%;border-radius:12px;background:${v<.3?COL.red:COL.green}"></div></div>`;
 h+=stamp(cx,760,'≈ WORTHLESS',c.r(tw,.35),{size:46,rot:-5});
 return h},
// ---- 39: Rentenmark
newmark(c,g){const cx=g.cx,t0=c.fx('swish',.05),tt=c.fx('impact',c.w(/trillion/i,.75));let h='',s='';
 h+=T(cx,165,'Germany, 1923: reset',{size:42,p:c.a(t0,.5)});
 h+=chip(cx,300,'1 new mark',{p:c.r(c.fx('pop',c.w(/One/,.5)),.5),size:56,bg:`linear-gradient(90deg,${COL.gold2},${COL.gold})`,fg:COL.brown});
 h+=T(cx,420,'=',{size:90,col:COL.muted,p:c.r(tt-.3,.3)});
 h+=T(cx,540,'1,000,000,000,000',{size:66,col:COL.cream,p:c.r(tt,.5),sh:`0 0 30px #ff5b4a55,${SH}`});
 h+=T(cx,615,'old marks',{size:36,col:COL.muted,p:c.r(tt,.5)});
 h+=chip(cx,740,'a new currency',{p:c.r(c.w(/currency/i,.4),.5),size:32,bg:'#24150cee',ic:ic('check',32,COL.green)});
 return h},
// ---- 41: alarm clock
alarm(c){const t0=c.fx('swish',.05),ta=c.fx('beep',c.w(/work/i,.75),{f:1900});c.fx('beep',ta+.2,{f:1900});c.fx('beep',ta+.4,{f:1900});let h='';
 const ring=c.lt>ta&&c.lt<ta+2.5,rot=ring?Math.sin(c.lt*48)*9:0;
 h+=box(1200,100,620,460,{p:c.a(t0,.5)});
 h+=`<div style="position:absolute;left:1380px;top:150px;transform:rotate(${rot.toFixed(1)}deg);opacity:${c.a(t0+.1,.4)}">${ic('clock',200,COL.cream)}</div>`;
 h+=T(1510,420,'Still go to work?',{size:44,p:c.a(c.w(/would/i,.3),.5)});
 h+=chip(1400,500,'Yes',{p:c.r(ta+.6,.5),size:34,bg:COL.green2+'f0'});h+=chip(1620,500,'No way',{p:c.r(ta+.8,.5),size:34,bg:'#7a2318ee'});
 return h},
// ---- 42: Swedish lottery study
lottery(c,g){const cx=g.cx,t0=c.fx('swish',.05);let h='',s='';
 h+=chip(cx,170,'Study: Sweden',{p:c.a(t0,.5),size:40,bg:'#24150cee',ic:ic('lens',40,COL.gold)});
 const tw=c.w(/thousands/i,.6),n=Math.round(cnt(c,tw,1.4,0,1000));c.fx('tick',tw,{f:2100});
 for(let k=0;k<60;k++){const p=c.r(tw+k*.02,.3);s+=face(cx-250+(k%10)*55,280+Math.floor(k/10)*58,20,p)}
 h+=svg(s);
 h+=T(cx,680,'large lottery winners',{size:36,p:c.r(c.w(/lottery/i,.85),.5)});
 h+=T(cx,740,'followed for years',{size:28,w:500,col:COL.muted,p:c.r(c.w(/prizes/i,.95),.5)});
 return h},
// ---- 43: cut back a little
cutback(c,g){const cx=g.cx,t0=c.fx('swish',.05),tk=c.fx('ding',c.w(/kept/i,.2));let h='';
 h+=chip(cx,170,'Most kept working',{p:c.r(tk,.5),size:44,bg:COL.green2+'f0',ic:ic('check',44,'#fff')});
 const tw=c.fx('pop',c.w(/won/i,.55)),tl=c.fx('thud',c.w(/less/i,.85));
 h+=T(cx-200,330,'Won',{al:'l',size:36,col:COL.muted,p:c.r(tw,.4)});h+=T(cx+200,330,'$100',{al:'r',size:64,col:COL.gold,p:c.r(tw,.4)});
 h+=`<div style="position:absolute;left:${cx-200}px;top:370px;height:40px;width:${(400*ez(c.r(tw,.7))).toFixed(0)}px;border-radius:10px;background:${COL.gold}"></div>`;
 h+=T(cx-200,500,'Earned less per year',{al:'l',size:32,col:COL.muted,p:c.r(tl,.4)});h+=T(cx+200,570,'≈ $1',{al:'r',size:64,col:COL.red,p:c.r(tl,.4)});
 h+=`<div style="position:absolute;left:${cx-200}px;top:540px;height:40px;width:${(4*ez(c.r(tl,.7))+2).toFixed(0)}px;border-radius:6px;background:${COL.red}"></div>`;
 h+=T(cx,700,'Cesarini et al., Swedish lottery data',{size:24,w:500,col:COL.muted,p:c.a(1,.5)});
 return h},
// ---- 44: few winners vs everyone
everyonemath(c){const t0=c.fx('swish',.05);let h='',s='';
 h+=box(90,90,1740,330,{p:c.a(t0,.5)});
 h+=T(420,150,'A few winners',{size:40,p:c.a(t0+.1,.4)});for(let k=0;k<3;k++)s+=face(320+k*100,280,40,c.a(t0+.2+k*.1,.4));
 const te=c.fx('impact',c.w(/everyone/i,.45)),pe=c.r(te,.5);
 h+=T(1340,150,'Everyone at once',{size:40,col:COL.gold,p:pe});
 for(let k=0;k<64;k++)s+=face(1000+(k%16)*44,230+Math.floor(k/16)*44,17,c.r(te+k*.012,.3));
 h+=svg(s);h+=T(960,280,'vs',{size:60,col:COL.muted,p:c.a(t0+.3,.4)});
 h+=chip(960,480,'the math changes completely',{p:c.r(c.fx('whoosh',c.w(/changes/i,.85),{d:.6}),.5),size:40,bg:`linear-gradient(90deg,${COL.gold2},${COL.gold})`,fg:COL.brown});
 return h},
// ---- 45: tenfold prices
tenfold(c,g){const cx=g.cx,t0=c.fx('swish',.05),tp=c.fx('impact',c.w(/tenfold/i,.25)),th=c.fx('thud',c.w(/hundred/i,.55));let h='';
 h+=chip(cx,170,'Prices ×10',{p:c.r(tp,.5),size:56,bg:COL.red,fg:'#fff',ic:ic('up',50,'#fff')});
 h+=T(cx,330,'$1,000,000',{size:90,col:COL.gold,p:c.a(t0,.5)});
 h+=T(cx,430,'now buys what',{size:34,col:COL.muted,p:c.r(th-.3,.4)});
 h+=T(cx,530,'$100,000',{size:90,col:COL.cream,p:c.r(th,.5)});
 h+=T(cx,600,'used to buy',{size:34,col:COL.muted,p:c.r(th,.5)});
 h+=chip(cx,740,'back to work',{p:c.r(c.fx('pop',c.w(/jobs/i,.9)),.5),size:36,bg:'#24150cee',ic:ic('clock',36,COL.gold)});
 return h},
// ---- 46: help wanted
jobs(c){const t0=c.fx('swish',.05);let h='';
 [['Cleaner','brush',/Cleaners/i,.35],['Delivery driver','truck',/delivery/i,.55],['Night nurse','cross2',/nurses/i,.8]].forEach(([lab,icn,re,f],k)=>{const tt=c.fx('thud',c.w(re,f)),p=c.r(tt,.5),x=420+k*540,sw=Math.sin(c.lt*1.8+k)*3*(p>=1?1:0);
  if(p>0)h+=`<div style="position:absolute;left:${x-200}px;top:${(110-(1-ez(p))*300).toFixed(0)}px;width:400px;height:300px;transform-origin:200px -40px;transform:rotate(${sw.toFixed(2)}deg)"><div style="position:absolute;left:0;right:0;top:0;bottom:0;border-radius:22px;background:#fbf0da;box-shadow:0 20px 40px #000a"></div><div style="position:absolute;left:0;right:0;top:20px;text-align:center;font:700 36px P;color:${COL.red};letter-spacing:3px">HELP WANTED</div><div style="position:absolute;left:0;right:0;top:80px;text-align:center">${ic(icn,110,COL.coffee)}</div><div style="position:absolute;left:0;right:0;top:220px;text-align:center;font:700 40px P;color:${COL.brown}">${lab}</div></div>`});
 return h},
// ---- 47: who keeps the basics running
supply(c,g){const cx=g.cx,t0=c.fx('swish',.05);let h='';
 h+=T(cx,165,'Fewer workers here …',{size:42,p:c.a(t0,.5)});
 [['wheat','Harvest',/harvests/i,.25],['truck','Trucks',/trucks/i,.4],['bolt','Power lines',/power/i,.55]].forEach(([icn,lab,re,f],k)=>{const tt=c.fx('pop',c.w(re,f)),p=c.r(tt,.5),y=290+k*130;
  h+=box(cx-260,y-50,520,100,{p,r:20,bg:'#24150cee'});h+=icAt(icn,cx-190,y,64,COL.gold,p);h+=T(cx-130,y,lab,{al:'l',size:40,p});h+=icAt('down',cx+200,y,56,COL.red,c.r(tt+.3,.4))});
 h+=chip(cx,720,'… even less stuff to buy',{p:c.r(c.fx('thud',c.w(/less/i,.9)),.5),size:36,bg:'#7a2318ee'});
 return h},
// ---- 48: empty shelves, empty wards
empty(c){const t0=c.fx('swish',.05);let h='',s='';
 h+=box(100,100,700,500,{p:c.a(t0,.5)});
 h+=T(140,160,`${ic('cross2',40,COL.red,'vertical-align:-8px;margin-right:12px')}Hospital staff`,{al:'l',size:36,p:c.a(t0+.1,.4)});
 const th=c.w(/half/i,.3);for(let k=0;k<10;k++){const gone=k>=5&&c.lt>th+.2+k*.08;s+=face(170+k*62,250,24,c.a(t0+.2+k*.04,.3),{col:gone?'#ffffff22':'#f6e3b4'})}
 h+=T(760,250,c.lt>th+.8?'50 %':'100 %',{al:'r',size:40,col:c.lt>th+.8?COL.red:COL.green,p:c.a(t0+.2,.4)});
 h+=T(140,350,`${ic('cart',40,COL.gold,'vertical-align:-8px;margin-right:12px')}Supermarket shelf`,{al:'l',size:36,p:c.a(t0+.3,.4)});
 const ts=c.w(/supermarket/i,.75);const col=['#ffc94a','#3ddc84','#ff8a5a','#7cc3ff','#e06b8b'];
 s+=`<rect x=150 y=520 width=600 height=10 fill="#c58a4a" opacity=${c.a(t0+.3,.4)} />`;
 for(let k=0;k<12;k++){const gone=c.r(ts+k*.12,.3);if(gone>=1)continue;s+=`<rect x=${160+k*49} y=${430+gone*-20} width=40 height=88 rx=6 fill="${col[k%5]}" opacity=${(c.a(t0+.35,.4)*(1-gone)).toFixed(2)} />`}
 for(let k=0;k<4;k++)c.fx('click',ts+k*.36);
 h+=svg(s);
 return h},
// ---- 52: debtors win
debtwin(c,g){const cx=g.cx,t0=c.fx('swish',.05),tw=c.fx('chime',c.w(/winners/i,.5));let h='';
 h+=chip(cx,170,'Winners: people with big debts',{p:c.r(tw,.5),size:36,bg:COL.green2+'f0',ic:ic('up',36,'#fff')});
 const p=c.a(t0+.2,.5);
 h+=T(cx-220,330,'Debt',{al:'l',size:36,p});h+=`<div style="position:absolute;left:${cx-220}px;top:360px;height:56px;width:${(90*p).toFixed(0)}px;border-radius:12px;background:${COL.red}"></div>`;h+=T(cx-110,388,'$200k',{al:'l',size:34,p});
 h+=T(cx-220,500,'New money',{al:'l',size:36,p:c.r(tw,.5)});h+=`<div style="position:absolute;left:${cx-220}px;top:530px;height:56px;width:${(450*ez(c.r(tw,.9))).toFixed(0)}px;border-radius:12px;background:${COL.green}"></div>`;h+=T(cx+240,558,'$1M',{al:'r',size:34,col:COL.brown,sh:0,p:c.r(tw+.6,.4)});
 return h},
// ---- 53: mortgage paid off
mortgage(c){const t0=c.fx('swish',.05),ts=c.w(/second/i,.5);let h='';
 h+=box(1180,100,650,420,{p:c.a(t0,.5)});
 h+=T(1220,165,`${ic('house',48,COL.cream2,'vertical-align:-10px;margin-right:12px')}Mortgage`,{al:'l',size:42,p:c.a(t0+.1,.4)});
 const q=ez(c.r(ts-.3,.7)),v=200000*(1-q);c.fx('cash',ts+.4);
 h+=T(1790,165,fmt(v,'$'),{al:'r',size:44,col:q>=1?COL.green:COL.red,p:c.a(t0+.1,.4)});
 h+=`<div style="position:absolute;left:1220px;top:230px;width:570px;height:44px;border-radius:12px;background:#ffffff14;opacity:${c.a(t0+.2,.4)}"><div style="height:100%;width:${(q*100).toFixed(1)}%;border-radius:12px;background:${COL.green}"></div></div>`;
 h+=stamp(1505,340,'PAID OFF',c.r(ts+.4,.35),{size:54,rot:-6,col:COL.green});
 h+=chip(1505,450,'debt does not grow with inflation',{p:c.r(c.fx('pop',c.w(/grow/i,.85)),.5),size:28,bg:'#24150cee'});
 return h},
// ---- 54: banks lose
banklose(c,g){const cx=g.cx,t0=c.fx('swish',.05),tl=c.fx('thud',c.w(/lose/i,.2));let h='';
 h+=icAt('bank',cx,220,140,COL.cream2,c.a(t0,.5));
 h+=stamp(cx+150,170,'LOSES',c.r(tl,.35),{size:40,rot:10});
 h+=T(cx-230,390,'Loan given',{al:'l',size:32,col:COL.muted,p:c.a(.5,.4)});h+=T(cx+230,390,'$200,000',{al:'r',size:44,p:c.a(.5,.4)});
 const tb=c.w(/worth/i,.75),q=ez(c.r(tb,1));
 h+=T(cx-230,470,'Paid back, real value',{al:'l',size:30,col:COL.muted,p:c.r(c.w(/paid/i,.55),.4)});h+=T(cx+230,520,fmt(lerp(200000,20000,q),'$'),{al:'r',size:44,col:COL.red,p:c.r(c.w(/paid/i,.55),.4)});
 h+=`<div style="position:absolute;left:${cx-230}px;top:560px;width:460px;height:36px;border-radius:10px;background:#ffffff14"><div style="height:100%;width:${(100-90*q).toFixed(1)}%;border-radius:10px;background:${COL.red}"></div></div>`;
 h+=T(cx,650,'in today’s buying power (illustration)',{size:24,w:500,col:COL.muted,p:c.r(tb,.5)});
 return h},
// ---- 55: savers lose
savers(c,g){const cx=g.cx,t0=c.fx('swish',.05),tl=c.fx('error',c.w(/losers/i,.2));let h='';
 h+=chip(cx,165,'Losers: savers',{p:c.r(tl,.5),size:42,bg:'#7a2318ee',ic:ic('down',40,'#fff')});
 const ts=c.w(/saved/i,.4),v=cnt(c,ts,1.4,0,500000);
 h+=T(cx,280,'30 years of saving',{size:32,col:COL.muted,p:c.r(ts,.4)});h+=T(cx,350,fmt(v,'$'),{size:72,col:COL.gold,p:c.r(ts,.4)});
 const te=c.w(/same/i,.6);h+=T(cx,450,'= same head start as everyone',{size:30,p:c.r(te,.5)});
 const tm=c.fx('thud',c.w(/melt/i,.9)),m=ez(c.r(tm,1.5));
 h+=`<div style="position:absolute;left:${cx-90}px;top:${520+80*m}px;width:180px;height:${(180-80*m).toFixed(0)}px;border-radius:${30+60*m}px ${30+60*m}px 30px 30px;background:linear-gradient(180deg,${COL.gold},${COL.gold2});opacity:${c.r(te,.4)}"></div>`;
 if(m>0)h+=`<div style="position:absolute;left:${cx-150*m-40}px;top:690px;width:${300*m+80}px;height:20px;border-radius:10px;background:${COL.gold2};opacity:.7"></div>`;
 return h},
// ---- 56: real things
realthings(c,g){const cx=g.cx,t0=c.fx('swish',.05);let h='';
 h+=T(cx,165,'Owners of real things',{size:42,p:c.a(t0,.5)});
 h+=clist(c,cx,290,120,[['Houses','house',/houses/i,.3],['Land','wheat',/land/i,.4],['Companies','gear',/companies/i,.5]],{size:46});
 h+=chip(cx,690,'prices rise with inflation',{p:c.r(c.fx('ding',c.w(/rise/i,.85)),.5),size:32,bg:COL.green2+'f0',ic:ic('up',32,'#fff')});
 return h},
// ---- 57: reshuffle
reshuffle(c){const t0=c.fx('swish',.05);let h='',s='';
 h+=box(560,90,800,360,{p:c.a(t0,.5)});
 h+=T(960,150,'Rich ↔ poor',{size:44,p:c.a(t0+.1,.4)});
 const ts=c.w(/reshuffled/i,.7),q=ei(c.r(ts,1.2));const ord=[[0,2],[1,0],[2,1]];c.fx('swish',ts,{d:.5});c.fx('swish',ts+.4,{d:.5,pan:-.4});
 const L3=[['Debtors',COL.green],['Owners',COL.gold],['Savers',COL.red]];
 L3.forEach(([lab,col],k)=>{const x=lerp(720+ord[k][0]*240,720+ord[k][1]*240,q),y=330-Math.sin(q*Math.PI)*(k-1)*60;s+=face(x,y-30,46,c.a(t0+.2+k*.1,.4));h+=T(x,y+50,lab,{size:30,col,p:c.a(t0+.2+k*.1,.4)})});
 h+=svg(s);h+=chip(960,510,'the gap stays',{p:c.r(c.fx('pop',c.w(/disappear/i,.4)),.5),size:34,bg:'#24150cee'});
 return h},
// ---- 60: everyone a millionaire
meaningless(c){const t0=c.fx('swish',.05),tn=c.fx('thud',c.w(/nothing/i,.9));let h='';
 const g=cl(c.lt,tn,tn+1.2);
 for(let k=0;k<12;k++){const tt=.3+k*.12,p=c.r(tt,.4);if(k%3==0)c.fx('pop',tt);const x=200+(k%6)*300,y=150+Math.floor(k/6)*110;
  h+=chip(x,y,'MILLIONAIRE',{p,size:30,bg:`linear-gradient(90deg,${COL.gold2},${COL.gold})`,fg:COL.brown,css:'',rot:(k%2?3:-3),s:bo(p)*(1-.1*g)})}
 h=`<div style="filter:grayscale(${g.toFixed(2)}) brightness(${(1-.35*g).toFixed(2)})">${h}</div>`;
 h+=stamp(960,420,'= ALMOST NOTHING',c.r(tn,.35),{size:56,rot:-4});
 return h},
// ---- 61: prices settle higher
settle(c,g){const x0=110,x1=690,y0=230,y1=640,t0=c.fx('swish',.05);let h='',s='';
 s+=`<rect x=${x0-30} y=${y0-70} width=${x1-x0+60} height=${y1-y0+120} rx=24 fill="#24150cdd" opacity=${c.a(t0,.4)} />`;
 const pd=ei(c.r(.3,Math.max(1.8,c.D*.6)));let d='';for(let k=0;k<=60;k++){const u=k/60*pd,v=.08+.82/(1+Math.exp(-(u-.35)*14));d+=(k?'L':'M')+(x0+u*(x1-x0)).toFixed(1)+' '+(y1-v*(y1-y0)).toFixed(1)}
 s+=`<path d="${d}" fill=none stroke="${COL.red}" stroke-width=8 stroke-linecap=round /><line x1=${x0} x2=${x1} y1=${y1} y2=${y1} stroke="#ffffff55" stroke-width=3 />`;
 h+=svg(s);h+=T(x0,y0-30,'Price level',{al:'l',size:36,p:c.a(t0,.4)});
 h+=chip(x1-150,y0+40,'new, higher normal',{p:c.r(c.fx('ding',c.w(/higher/i,.4)),.5),size:28,bg:'#24150cee'});
 h+=chip(400,y1+80,'richer? not really',{p:c.r(c.fx('error',c.w(/richer/i,.85)),.5),size:32,bg:'#7a2318ee'});
 return h},
// ---- 62: some even poorer
poorer(c,g){const cx=g.cx,t0=c.fx('swish',.05);let h='';
 h+=T(cx,165,'Fixed income',{size:44,p:c.a(t0,.5)});
 h+=chip(cx,260,'Pension: $1,500 / month',{p:c.r(c.fx('pop',c.w(/pensions/i,.7)),.5),size:36,bg:'#24150cee'});
 const tv=c.w(/value/i,.9),q=ez(c.r(tv-.8,1.4));
 h+=T(cx,380,'buys this much:',{size:30,col:COL.muted,p:c.r(tv-.9,.4)});
 for(let k=0;k<10;k++){const on=k<10-9*q;h+=icAt('bread',cx-243+k*54,470,52,on?COL.gold:'#ffffff22',c.r(tv-.9+k*.03,.3))}
 h+=chip(cx,600,'some end up poorer',{p:c.r(c.fx('thud',tv+.4),.5),size:34,bg:'#7a2318ee'});
 return h},
// ---- 63: cut off zeros
zeros(c){const t0=c.fx('swish',.05),tz=c.w(/zeros/i,.6);let h='';
 h+=box(560,90,800,330,{p:c.a(t0,.5)});
 h+=T(960,150,'New currency',{size:40,col:COL.gold,p:c.a(t0+.1,.4)});
 const n=6-Math.min(6,Math.floor(cl(c.lt,tz,tz+1.2)*7));for(let k=0;k<6-n;k++)c.fx('swish',tz+k*.2,{d:.25});
 const str='$1'+',000,000'.replace(/0/g,'0').slice(0,0)+'0'.repeat(n).replace(/(\d)(?=(\d{3})+$)/g,'$1,');
 h+=T(960,280,MG.fmt(Math.pow(10,n),0,'$'),{size:110,p:c.a(t0+.2,.4),sh:`0 0 30px #ffc94a44,${SH}`});
 h+=icAt('scissors',1290,280,80,COL.red,c.r(tz-.3,.4),Math.sin(c.lt*12)*15);
 h+=chip(960,470,'readable prices again',{p:c.r(c.fx('ding',c.w(/readable/i,.9)),.5),size:34,bg:COL.green2+'f0'});
 return h},
// ---- 64: renegotiate everything
contracts(c,g){const cx=g.cx,t0=c.fx('swish',.05);let h='';
 [['Contracts',/Contracts/i,.1],['Wages',/wages/i,.2],['Savings plans',/savings/i,.3]].forEach(([lab,re,f],k)=>{const tt=c.fx('paper',c.w(re,f)),p=c.r(tt,.5);
  h+=`<div style="position:absolute;left:${cx-170+k*30}px;top:${170+k*70}px;width:340px;height:220px;border-radius:16px;background:#fbf0da;box-shadow:0 14px 30px #0009;transform:rotate(${(k-1)*5}deg) translateY(${((1-ez(p))*-60).toFixed(0)}px);opacity:${Math.min(1,p*2)}"><div style="position:absolute;left:24px;top:22px;font:700 34px P;color:${COL.brown}">${lab}</div>${[0,1,2].map(j=>`<div style="position:absolute;left:24px;top:${84+j*36}px;width:${260-j*50}px;height:10px;border-radius:5px;background:#c9a87a"></div>`).join('')}</div>`});
 h+=stamp(cx,470,'RENEGOTIATE',c.r(c.fx('impact',c.w(/renegotiated/i,.5)),.35),{size:44,rot:-8});
 h+=T(cx,660,'What is anything worth?',{size:38,col:COL.gold,p:c.r(c.w(/worth/i,.85),.5)});
 return h},
// ---- 66: money is a ticket
ticket(c){const t0=c.fx('swish',.05),tt=c.fx('pop',c.w(/ticket/i,.3));let h='';
 h+=box(100,90,820,520,{p:c.a(t0,.5)});
 h+=T(510,150,'Money is not wealth',{size:44,p:c.a(t0+.1,.4)});
 const p=c.r(tt,.5);h+=`<div style="position:absolute;left:180px;top:200px;transform:scale(${bo(p).toFixed(3)}) rotate(-4deg);opacity:${Math.min(1,p*2)}">${ic('ticket',220,COL.gold)}</div>`;
 h+=T(262,312,'$',{size:70,col:COL.brown,sh:0,p});h+=T(560,300,'a ticket',{size:54,col:COL.gold,p:c.r(tt+.2,.4)});
 h+=T(470,420,'trade it for:',{size:30,col:COL.muted,p:c.r(tt+.3,.4)});
 [['bread','food',/food/i,.6],['house','homes',/homes/i,.72],['brush','haircuts',/haircuts/i,.85],['clock','time',/time/i,.95]].forEach(([icn,lab,re,f],k)=>{const tk=c.fx('pop',c.w(re,f)),q=c.r(tk,.5);h+=chip(250+k*180,520,lab,{p:q,size:28,bg:'#fbf0daf2',fg:COL.brown,ic:ic(icn,28,COL.brown)})});
 return h},
// ---- 67: what people produce
produce(c,g){const cx=g.cx,t0=c.fx('swish',.05);let h='';
 h+=T(cx,165,'Real wealth = production',{size:40,p:c.a(t0,.5)});
 [['bread','Bread',/bread/i,.45],['house','Houses',/houses/i,.6],['gear','Tools',/tools/i,.78],['bulb','Ideas',/ideas/i,.92]].forEach(([icn,lab,re,f],k)=>{const tt=c.fx('pop',c.w(re,f)),u=ez(c.r(tt,.9)),x=cx-225+k*150,base=700,hh=120+k*70;
  h+=`<div style="position:absolute;left:${x-50}px;top:${base-hh*u}px;width:100px;height:${(hh*u).toFixed(0)}px;border-radius:14px 14px 0 0;background:linear-gradient(180deg,${COL.green},${COL.green2})"></div>`;
  h+=icAt(icn,x,base-hh*u-50,64,COL.cream,c.r(tt,.4));h+=T(x,base+34,lab,{size:26,w:500,p:c.r(tt,.4)})});
 return h},
// ---- 68: print your way out of poverty?
printpoor(c,g){const cx=g.cx,t0=c.fx('swish',.05);let h='';
 h+=T(cx,190,'Print money →',{size:52,p:c.a(t0,.5)});h+=T(cx,280,'end poverty?',{size:52,col:COL.gold,p:c.a(t0+.3,.5)});
 const tn=c.fx('impact',c.w(/None/,.9));
 h+=icAt('cross',cx,450,160,COL.red,c.r(tn-.2,.4));
 h+=stamp(cx,640,'NONE EVER HAS',c.r(tn,.35),{size:52,rot:-5});
 return h},
// ---- 70: central banks
centralbank(c,g){const cx=g.cx,t0=c.fx('swish',.05);let h='',s='';
 h+=icAt('bank',cx,240,170,COL.cream2,c.a(t0,.5));
 h+=T(cx,400,'Central bank',{size:40,p:c.a(t0+.2,.4)});
 const tc=c.w(/careful/i,.4);for(let k=0;k<6;k++){const ph=((c.lt-tc)*.7+k/6)%1;if(c.lt<tc)continue;s+=`<circle cx=${cx} cy=${460+ph*220} r=${10*(1-ph*.5)} fill="${COL.green}" opacity=${(1-ph).toFixed(2)} />`}
 h=svg(s)+h;c.fx('click',tc);
 h+=chip(cx,720,'new money: drop by drop',{p:c.r(tc,.5),size:32,bg:'#24150cee',ic:ic('oil',32,COL.green)});
 return h},
// ---- 71: Alaska dividend
alaska(c){const t0=c.fx('swish',.05);let h='';
 h+=box(100,100,760,440,{p:c.a(t0,.5)});
 h+=T(140,165,'Alaska',{al:'l',size:56,col:'#7cc3ff',p:c.a(t0+.1,.4)});
 h+=T(140,225,'Permanent Fund Dividend',{al:'l',size:32,col:COL.cream2,p:c.a(t0+.2,.4)});
 const to=c.fx('pop',c.w(/oil/i,.7));h+=icAt('oil',220,360,110,'#e8d7a8',c.r(to,.5));h+=icAt('ticket',400,360,110,COL.gold,c.r(to+.3,.5));
 h+=svg(arrow(270,360,340,360,c.r(to+.15,.4),{bend:0,w:6}));
 const tt=c.fx('cash',c.w(/thousands/i,.9));
 h+=chip(650,360,'low $ thousands / year',{p:c.r(tt,.5),size:30,bg:`linear-gradient(90deg,${COL.gold2},${COL.gold})`,fg:COL.brown});
 h+=T(140,480,'paid to residents every year',{al:'l',size:28,w:500,col:COL.muted,p:c.a(1.2,.4)});
 return h},
// ---- 72: size matters
size(c,g){const cx=g.cx,t0=c.fx('swish',.05),te=c.fx('ding',c.w(/employment/i,.3));let h='';
 h+=chip(cx,165,'employment: no overall drop',{p:c.r(te,.5),size:32,bg:COL.green2+'f0',ic:ic('check',32,'#fff')});
 h+=T(cx-230,290,'A little extra',{al:'l',size:34,p:c.r(c.w(/little/i,.6),.4)});
 h+=`<div style="position:absolute;left:${cx-230}px;top:320px;height:50px;width:${(30*ez(c.r(c.w(/little/i,.6),.6))).toFixed(0)}px;border-radius:10px;background:${COL.green}"></div>`;
 h+=T(cx-230,440,'$1M for everyone',{al:'l',size:34,p:c.r(c.w(/million/i,.85),.4)});
 const tb=c.fx('impact',c.w(/breaks/i,.92)),u=ez(c.r(c.w(/million/i,.85),.8)),sh=c.lt>tb&&c.lt<tb+.4?Math.sin(c.lt*90)*6:0;
 h+=`<div style="position:absolute;left:${cx-230+sh}px;top:470px;height:50px;width:${(460*u).toFixed(0)}px;border-radius:10px;background:${COL.red}"></div>`;
 h+=stamp(cx,620,'BREAKS THE SYSTEM',c.r(tb,.35),{size:42,rot:-6});
 return h},
// ---- 73: waves of money
wave(c,g){const x0=1220,x1=1820,y0=240,y1=640,t0=c.fx('swish',.05);let h='',s='';
 s+=`<rect x=${x0-30} y=${y0-70} width=${x1-x0+60} height=${y1-y0+130} rx=24 fill="#24150cdd" opacity=${c.a(t0,.4)} />`;
 const pd=ei(c.r(.3,Math.max(2,c.D*.6)));let dm='',dg='';for(let k=0;k<=50;k++){const u=k/50*pd,x=x0+u*(x1-x0);dm+=(k?'L':'M')+x.toFixed(1)+' '+(y1-(.1+.75*u*u)*(y1-y0)).toFixed(1);dg+=(k?'L':'M')+x.toFixed(1)+' '+(y1-(.1+.25*u)*(y1-y0)).toFixed(1)}
 s+=`<path d="${dg}" fill=none stroke="${COL.cream2}" stroke-width=7 stroke-dasharray="14 10"/><path d="${dm}" fill=none stroke="${COL.green}" stroke-width=8 stroke-linecap=round />`;
 h+=svg(s);h+=T(x0,y0-30,'New money vs. new goods',{al:'l',size:32,p:c.a(t0,.4)});
 h+=T(x1,y1+40,`<span style="color:${COL.green}">●</span> money&nbsp;&nbsp;<span style="color:${COL.cream2}">●</span> goods`,{al:'r',size:24,w:500,p:c.a(t0+.3,.4)});
 h+=chip(1520,y0+60,'gap = higher prices',{p:c.r(c.fx('pop',c.w(/faster/i,.6)),.5),size:28,bg:'#7a2318ee'});
 return h},
// ---- 75: the honest answer
answer(c){const t0=c.fx('swish',.05),tn=c.fx('impact',c.w(/^No\.?$/,.35));let h='';
 h+=box(100,100,640,500,{p:c.a(t0,.5)});
 h+=T(420,180,'All rich?',{size:60,p:c.a(t0+.1,.4)});
 h+=stamp(420,290,'NO',c.r(tn,.35),{size:84,rot:-6});
 const tm=c.fx('pop',c.w(/millionaires/i,.6)),tsm=c.fx('ding',c.w(/same/i,.92));
 h+=chip(420,420,'All millionaires',{p:c.r(tm,.5),size:40,bg:`linear-gradient(90deg,${COL.gold2},${COL.gold})`,fg:COL.brown});
 h+=T(420,520,'≠ rich',{size:60,col:COL.red,p:c.r(tsm,.5)});
 return h},
// ---- 76: what makes a society richer
richer(c,g){const cx=g.cx,t0=c.fx('swish',.05);let h='';
 h+=T(cx,165,'Society gets richer by …',{size:40,p:c.a(t0,.5)});
 h+=clist(c,cx,300,120,[['producing more','up',/more/i,.35],['producing better','check',/better/i,.5]],{size:46});
 h+=chip(cx,620,'and for you?',{p:c.r(c.fx('whoosh',c.w(/personally/i,.75),{d:.5}),.5),size:40,bg:'#24150cee',ic:ic('lens',40,COL.gold)});
 return h},
// ---- 77: your own million
ownmillion(c){const t0=c.fx('swish',.05);let h='',s='';
 h+=box(260,90,1400,300,{p:c.a(t0,.5)});
 h+=T(960,150,'Your own million comes from',{size:42,p:c.a(t0+.1,.4)});
 const tn=c.fx('error',c.w(/printer/i,.3));h+=chip(1500,150,'printer',{p:c.r(tn,.4),size:26,bg:'#7a2318ee',ic:ic('cross',26,'#fff')});
 const W2=[['Earning','coin',/earning/i,.55],['Saving','shield',/saving/i,.65],['Investing','up',/investing/i,.75],['Time','clock',/time/i,.95]];
 W2.forEach(([lab,icn,re,f],k)=>{const tt=c.fx(k==3?'chime':'pop',c.w(re,f)),p=c.r(tt,.5),x=420+k*360;
  h+=chip(x,280,lab,{p,size:k==3?50:42,bg:k==3?`linear-gradient(90deg,${COL.gold2},${COL.gold})`:'#fbf0daf2',fg:COL.brown,ic:ic(icn,40,k==3?COL.brown:COL.coffee)});if(k)h+=T(x-180,280,'+',{size:50,col:COL.gold,p})});
 return h},
// ---- 78: comment
comment(c,g){const x=90,y=230,t0=c.fx('swish',.05),t1=.7,msg='I would buy my parents a house and invest the rest!',t2=Math.max(t1+2.2,c.D*.7);let h='';
 c.fx('type',t1,{n:14});c.fx('type',t1+1.1,{n:14});const tp=c.fx('pop',t2+.2);
 h+=T(g.cx,160,'Only you get $1,000,000:',{size:40,p:c.a(t0,.5)});
 const n=Math.floor(msg.length*cl(c.lt,t1,t2)),blink=Math.floor(c.lt*2.2)%2==0;
 h+=box(x,y,630,400,{p:c.a(t0+.1,.5),bg:'#fbf0da',bd:'0',html:`<div style="position:absolute;left:30px;top:30px;width:70px;height:70px;border-radius:50%;background:${COL.coffee};display:flex;align-items:center;justify-content:center">${ic('coin',44,COL.gold)}</div><div style="position:absolute;left:120px;top:44px;font:700 30px P;color:${COL.brown}">You</div><div style="position:absolute;left:30px;top:130px;width:570px;font:500 38px/1.35 P;color:${COL.brown}">${msg.slice(0,n)}<span style="opacity:${blink&&c.lt<t2+.6?1:0};color:${COL.gold2}">|</span></div>`});
 const pp=c.r(tp,.4);h+=chip(x+520,y+340,'Post',{p:c.a(t0+.3,.4),size:34,bg:pp>0?COL.green2:COL.coffee,s:pp>0&&pp<1?1-.12*Math.sin(pp*Math.PI):1});
 return h},
};
