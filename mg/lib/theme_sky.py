# Farbschema "Himmelblau" (Alex' Wahl 2026-10-19) fuer alle neuen YT-Videos im Video-2-Remaster-Stil.
# Benutzung in build_scene.py:  from theme_sky import apply;  html = apply(html)
# Dazu Gemini-Bilder mit kraeftigen, sonnigen Farben erzeugen (Prompt-Zusatz siehe GEMINI_STYLE).
GEMINI_STYLE = ("vibrant, rich, fully saturated colors, bright cheerful daylight, clean bright lighting, "
                "no grey or brown tint, no sepia")
BG_IN, BG_MID, BG_OUT, DARK = '#62bdf0', '#3a8ad0', '#2569ad', '#1d4f86'
def apply(s):
    R = [('radial-gradient(110% 90% at 28% 18%,#5a3820 0%,#36210f 45%,#1b0f07 100%)',
          f'radial-gradient(110% 90% at 28% 18%,{BG_IN} 0%,{BG_MID} 45%,{BG_OUT} 100%)'),
         ('background:#1d120b', f'background:{BG_OUT}'),
         ('height:1160px;opacity:.55}', 'height:1160px;opacity:.18}'),
         ('#0f0804b0', DARK + '38'), ('#0f0804d0', DARK + '60'), ('#24150c', DARK),
         ("MG.finish($('stage'),1920,1080,.05)", "MG.finish($('stage'),1920,1080,.05,'#0000001a',65)")]
    for a, b in R:
        s = s.replace(a, b)
    return s
