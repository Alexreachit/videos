# Baut scene.html aus der Video-2-Vorlage (yt02/scene.html) + ov.js + sc.js
import os
D=os.path.dirname(os.path.abspath(__file__));src=open(os.path.join(D,'..','yt02','scene.html')).read().split('\n')
L=lambda a,b:'\n'.join(src[a-1:b])
head=L(1,97).replace("const fmt=(v,pre='€')","const fmt=(v,pre='$')").replace('font-size=44 fill="#7a4507">€</text>','font-size=44 fill="#7a4507">$</text>').replace('YT02 – "Does one coffee a day make you a millionaire?"','YT – "5 Things You Should NEVER Do With Your Money"')
mid='\nconst BADGE={};\nconst SC={};\n'+L(405,418)+'\n'+L(448,463)+'\n'+L(501,511).replace("dec=sp.value<20&&p<1?1:0","dec=sp.dec!=null?sp.dec:(sp.value<20&&p<1?1:0)")+'\nSC.chart={step(g,t){let j=0;for(let k=0;k<g.n;k++)if(t>=MG.L(g.i0+k).start-.3)j=k;return {j,c:ctx(g.i0+j,t)}}};\n'
open(os.path.join(D,'scene.html'),'w').write(head+'\n'+open(os.path.join(D,'ov_head.js')).read()+open(os.path.join(D,'ov_body.js')).read()+mid+open(os.path.join(D,'sc.js')).read()+'\n'+L(659,711))
