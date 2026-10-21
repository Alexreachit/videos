# Baut scene.html aus der Video-8-Engine (yt_invest5/scene.html) + sc9.js, Farbschema Himmelblau
import os,sys
D=os.path.dirname(os.path.abspath(__file__));sys.path.insert(0,os.path.join(D,'..','lib'))
from theme_sky import apply
src=open(os.path.join(D,'..','yt_invest5','scene.html')).read()
a=src.index('// ---------------- hook:');b=src.index('// ---------------- dots:');c=src.index('// ---------------- lever:')
o=src.index('// ---------------- outro:');e=src.index('// ======================================================================\n//  ENGINE')
html=src[:a]+src[b:c]+src[o:e]+open(os.path.join(D,'sc9.js')).read()+'\n'+src[e:]
R=[('YT – "5 Things You Should NEVER Do With Your Money"','YT 9 – "Why Rich People Pay Less Tax Than You"'),
   ('for(let k=1;k<=9;k++)','for(let k=1;k<=7;k++)'),('`${sp.n} / 9`','`${sp.n} / 7`'),
   ('30 years of small deposits','Everyone gets $1 million'),
   ("const TRANS=['slide','zoom','wipe','iris','up'];","const TRANS=['slide','zoom','wipe','iris','up','zoom'];")]
for x,y in R:
    assert x in html,x;html=html.replace(x,y)
html=apply(html)
# sky theme: muted text colours that were tuned for brown
html=html.replace("muted:'#cfb08a'","muted:'#d8ecff'").replace("cream2:'#f2dcb5'","cream2:'#e6f2ff'")
for x,y in [("'#1d120bcc'","'#1d4f86dd'"),('0 0 0 10px #f6e6c6,0 0 0 13px #b88a4e','0 0 0 10px #ffffff,0 0 0 13px #9cc8ee'),('#fffbe8 0%,#ffd98a 35%,#d08a2a 75%','#ffffff 0%,#bfe6ff 35%,#3a8ad0 75%'),("bg:o.bg||'#fbf0daf2'","bg:o.bg||'#ffffffee'"),
 ("const cx=G.full?470:G.cx, cy=G.full?140:340;","const cx=sp.x||(G.full?470:G.cx), cy=sp.y||(G.full?140:340);"),
 ("if(sp.sub)h+=T(cx,cy+(G.full?90:130),sp.sub,{size:36,col:COL.cream,mw:600,lh:1.2,p:c.a(tt+.3,.5)});","if(sp.sub)h+=G.full?chip(cx,cy+92,sp.sub,{p:c.r(tt+.3,.5),size:32,bg:'#1d4f86ee'}):T(cx,cy+130,sp.sub,{size:36,col:COL.cream,mw:600,lh:1.2,p:c.a(tt+.3,.5)});")]:
    assert x in html,x;html=html.replace(x,y)
open(os.path.join(D,'scene.html'),'w').write(html)
print('ok',len(html))
