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

