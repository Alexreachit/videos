# Stellt Gemini-Objekte auf Magenta-Hintergrund frei -> PNG mit Alpha (quadratisch, zentriert).
# Nutzung: python3 mg/lib/keyout.py quelle.jpg ziel.png [size]
import sys
import numpy as np
from PIL import Image, ImageFilter

src, dst = sys.argv[1], sys.argv[2]
size = int(sys.argv[3]) if len(sys.argv) > 3 else 1024
im = np.asarray(Image.open(src).convert("RGB")).astype(np.float32)
r, g, b = im[..., 0], im[..., 1], im[..., 2]
# Hintergrundfarbe aus den Ecken schaetzen
c = np.concatenate([im[:20, :20].reshape(-1, 3), im[:20, -20:].reshape(-1, 3), im[-20:, :20].reshape(-1, 3), im[-20:, -20:].reshape(-1, 3)])
bg = np.median(c, 0)
d = np.sqrt(((im - bg) ** 2).sum(-1))
# "Magenta-Anteil": r und b hoch, g niedrig
mag = np.clip((np.minimum(r, b) - g) / 255.0, 0, 1)
a = np.clip((d - 60) / 90.0, 0, 1)
a = np.minimum(a, 1 - np.clip((mag - .35) / .35, 0, 1) * (d < 200))
alpha = Image.fromarray((a * 255).astype(np.uint8)).filter(ImageFilter.MinFilter(3)).filter(ImageFilter.GaussianBlur(.8))
# Despill: Magenta-Stich an Kanten entfernen
spill = np.clip(np.minimum(r, b) - g, 0, None)
k = (np.asarray(alpha) < 250)[..., None] * 1.0
im2 = im.copy()
im2[..., 0] = r - spill * .6 * k[..., 0]
im2[..., 2] = b - spill * .6 * k[..., 0]
out = Image.fromarray(np.clip(im2, 0, 255).astype(np.uint8)).convert("RGBA")
out.putalpha(alpha)
bb = out.getbbox()
out = out.crop(bb)
w, h = out.size
s = max(w, h)
sq = Image.new("RGBA", (int(s * 1.06), int(s * 1.06)), (0, 0, 0, 0))
sq.paste(out, ((sq.width - w) // 2, (sq.height - h) // 2), out)
sq.resize((size, size), Image.LANCZOS).save(dst)
print(dst, bb, "bg", bg.round())
