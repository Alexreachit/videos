// ======================= generic overlays for "img" scenes (data driven) =======================
const CK={gold:COL.gold,green:COL.green,red:COL.red,orange:'#ff9a4a',cream:COL.cream,grey:'#9a8a78',blue:'#7cc3ff'};
const RX=(s,f,c)=>{if(!s)return f*c.D;try{return c.w(new RegExp(s,'i'),f)}catch(e){return f*c.D}};
// free column geometry for a panel layout (full layout: left strip)
const colGeo=g=>g&&g.cx?{cx:g.cx,x0:g.x0,x1:g.x1,full:false}:{cx:330,x0:70,x1:700,full:true};
const OV={
// chip list with title; items [text,icon,regex,color]
chips(c,g){const sp=c.spec,G=colGeo(g);let h='';const t0=c.fx('swish',.05);const n=sp.items.length;
 const y0=G.full?170:250,dy=G.full?100:110;
 if(sp.title)h+=T(G.cx,G.full?100:170,sp.title,{size:G.full?38:52,col:COL.gold,p:c.a(t0,.5)});
 sp.items.forEach(([txt,icn,re,col],k)=>{const tt=c.fx('pop',RX(re,(k+.6)/(n+.4),c)),p=c.r(tt,.5);
  const size=Math.max(28,Math.min(50,Math.floor(610/(txt.length*.62+2.6))));
  const y=y0+k*dy+(sp.flow?k*34:0);
  h+=chip(G.cx,y,txt,{p,size,bg:col?CK[col]+'ee':'#24150cee',fg:'#fff',ic:icn?ic(icn,size*1.05,'#ffd48a'):''});
  if(sp.flow&&k<n-1){const pa=c.r(tt+.25,.4);if(pa>0)h+=T(G.cx,y+dy/2+17,'▼',{size:34,col:COL.gold,p:pa})}});
 return h},
// two big numbers: a / b = [label,value,colorKey,regex]
vs(c,g){const sp=c.spec,G=colGeo(g);let h='';const t0=c.fx('swish',.05);
 h+=T(G.cx,170,sp.title||'',{size:46,col:COL.gold,p:c.a(t0,.5)});
 [sp.a,sp.b].forEach(([lab,val,col,re],k)=>{const tt=c.fx(k?'impact':'pop',RX(re,.3+.4*k,c)),p=c.r(tt,.5),y=330+k*250,len=val.length,sz=Math.min(120,Math.round(560/(len*.62)));
  h+=T(G.cx,y-70,lab,{size:34,w:500,col:COL.cream2,p:Math.min(1,p*2)});
  h+=T(G.cx,y+10,val,{size:sz,col:CK[col],p,s:bo(p),sh:`0 0 40px ${CK[col]}44,${SH}`})});
 const pv=c.r(c.D*.5,.4);if(pv>0)h+=chip(G.cx,y_vs(),'vs',{p:pv,size:30,bg:'#ffffff22'});
 if(sp.foot)h+=T(G.cx,780,sp.foot,{size:24,w:500,col:COL.muted,p:c.a(.6,.5)});
 return h},
// rows: label (small) + value (big)
rows(c,g){const sp=c.spec,G=colGeo(g);let h='';const t0=c.fx('swish',.05);
 h+=T(G.cx,165,sp.title||'',{size:44,col:COL.gold,p:c.a(t0,.5)});
 sp.rows.forEach(([lab,val,col,re],k)=>{const tt=c.fx(k==sp.rows.length-1?'thud':'pop',RX(re,.25+.25*k,c)),p=c.r(tt,.5),y=270+k*165,sz=Math.min(86,Math.round(500/(val.length*.62)));
  h+=T(G.cx,y-50,lab,{size:30,w:500,col:COL.cream2,p:Math.min(1,p*2)});
  h+=T(G.cx,y+14,val,{size:sz,col:CK[col],p,s:bo(p),sh:`0 0 40px ${CK[col]}33,${SH}`})});
 if(sp.foot)h+=T(G.cx,780,sp.foot,{size:24,w:500,col:COL.muted,p:c.a(.6,.5)});
 return h},
// stamp: big statement
stamp(c,g){const sp=c.spec,G=colGeo(g);let h='';const t0=c.fx('swish',.05);const col=sp.col=='red'?COL.red:COL.gold;
 const tt=c.fx('impact',Math.min(c.D*.5,1.2));
 const cx=G.full?470:G.cx, cy=G.full?140:340;
 h+=stamp(cx,cy,sp.text,c.r(tt,.4),{size:G.full?60:(sp.text.length>16?40:50),col,rot:-4});
 if(sp.sub)h+=T(cx,cy+(G.full?90:130),sp.sub,{size:36,col:COL.cream,mw:600,lh:1.2,p:c.a(tt+.3,.5)});
 return h},
// numbered / crossed list of the five mistakes
five(c,g){const sp=c.spec,G=colGeo(g);let h='';const t0=c.fx('swish',.05);
 h+=T(G.cx,165,sp.title||'',{size:44,col:COL.gold,p:c.a(t0,.5)});
 const upto=sp.upto||5;
 sp.items.forEach((txt,k)=>{const re=sp.t[k];let tt=re?c.fx('pop',RX(re,.2+.15*k,c)):-1;
  const shown=k<upto&&(sp.upto?true:true),pre=sp.upto&&k<(upto>3?3:0);const p=pre?1:(tt<0?0:c.r(tt,.45));if(!shown)return;
  const y=260+k*100,size=Math.max(28,Math.min(38,Math.floor(500/(txt.length*.6+2))));
  const icon=sp.icon=='num'?`<div style="width:${size*1.3}px;height:${size*1.3}px;border-radius:50%;background:${COL.gold};color:${COL.brown};font:700 ${size}px/${size*1.3}px P;text-align:center">${k+1}</div>`:ic('cross',size*1.2,'#fff');
  h+=chip(G.cx,y,txt,{p,size,bg:sp.icon=='num'?'#24150cee':'#a8322aee',fg:'#fff',ic:icon})});
 return h}
};
function y_vs(){return 455}
