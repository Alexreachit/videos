from PIL import Image, ImageDraw, ImageFont, ImageFilter
import sys
F='/home/claude/videos/mg/ys_brinksmat/fonts/Inter-Black.otf'
bg=Image.open(sys.argv[1]).convert('RGB').resize((1280,720),Image.LANCZOS)
# leichte Abdunkelung oben links fuer Lesbarkeit
sh=Image.new('L',(1280,720),0); d=ImageDraw.Draw(sh); d.ellipse((-400,-300,760,420),fill=150); sh=sh.filter(ImageFilter.GaussianBlur(90))
bg=Image.composite(Image.new('RGB',(1280,720),(5,20,45)),bg,sh)
def text(img,xy,s,size,fill,stroke=14,rot=0):
    f=ImageFont.truetype(F,size); L=Image.new('RGBA',(1280,720)); dd=ImageDraw.Draw(L)
    dd.text((xy[0]+6,xy[1]+10),s,font=f,fill=(0,0,0,150),stroke_width=stroke,stroke_fill=(0,0,0,150))
    dd.text(xy,s,font=f,fill=fill,stroke_width=stroke,stroke_fill=(20,24,40))
    if rot: L=L.rotate(rot,center=xy,resample=Image.BICUBIC)
    img.alpha_composite(L)
im=bg.convert('RGBA')
text(im,(48,40),sys.argv[2],190,(255,209,102))
text(im,(48,225),sys.argv[3],120,(255,209,102))
# rotes Band
f=ImageFont.truetype(F,54); s=sys.argv[4]; w=ImageDraw.Draw(im).textlength(s,font=f)
B=Image.new('RGBA',(1280,720)); d=ImageDraw.Draw(B); x,y=56,380
d.rounded_rectangle((x-8,y-8,x+w+48,y+80),18,fill=(20,24,40)); d.rounded_rectangle((x,y,x+w+40,y+72),14,fill=(224,48,58))
d.text((x+20,y+6),s,font=f,fill='white'); B=B.rotate(3,center=(x,y),resample=Image.BICUBIC); im.alpha_composite(B)
im.convert('RGB').save(sys.argv[5],quality=92)
