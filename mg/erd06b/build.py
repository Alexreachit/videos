# Erdkern Tag 4 mit neuem Anfang (Wunsch Alex 2026-11-20: jedes Video beginnt mit "Wir graben ein Loch bis zum Erdkern" + wie man mitmacht).
# Ohne Neurendern: 2 neue Zeilen vorne (Schacht-Abfahrt + Erde aus dem Tag-4-Render), "Tag vier" aus der 750-Zeile raus, Rest um D verschoben.
import json, os, re, shutil, numpy as np
HERE = os.path.dirname(os.path.abspath(__file__)); OLD = os.path.join(HERE, "..", "erd06"); os.chdir(HERE)
LEAD, GAP, FPS, TAIL = .05, .12, 30, 1.4
# ---- Stimme: tmpv/voice 00..02 neu, alte 01..08 dahinter
os.makedirs("voice", exist_ok=True)
dnew = json.load(open("tmpv/voice/durs.json")); wnew = json.load(open("tmpv/voice/words.json"))
dold = json.load(open(f"{OLD}/voice/durs.json")); wold = json.load(open(f"{OLD}/voice/words.json"))
D, W = [], []
for i in range(3): shutil.copy(f"tmpv/voice/{i:02d}.mp3", f"voice/{i:02d}.mp3"); D.append(dnew[i]); W.append(wnew[i])
for k in range(1, 9): shutil.copy(f"{OLD}/voice/{k:02d}.mp3", f"voice/{k + 2:02d}.mp3"); D.append(dold[k]); W.append(wold[k])
json.dump(D, open("voice/durs.json", "w")); json.dump(W, open("voice/words.json", "w"), ensure_ascii=False)
p = json.load(open(f"{OLD}/project.json")); Lo = p["lines"]; newl = json.load(open("tmpv/project.json"))["lines"]
p["lines"] = newl + Lo[1:]; p["title"] += " – mit Intro"; p["voice"] = p["voice"].replace("erd06/", "erd06b/")
json.dump(p, open("project.json", "w"), ensure_ascii=False, indent=1)
# ---- Bilder-Zuordnung
def starts(d):
    s = []; t = LEAD
    for x in d: s.append(t); t += x + GAP
    return s, t - GAP
So, endo = starts(dold); Sn, endn = starts(D)
old = json.load(open(f"{OLD}/anchors_tt.json")); TTo = old["TT"]; NF_OLD = TTo["nf"]
NF = int(np.ceil((endn + TAIL) * FPS))
SH_ = Sn[3] - So[1]                       # Verschiebung: alte Zeile 1 (fosa) = neue Zeile 3
TA = Sn[1] - .05; T2 = Sn[2] - .05        # Schnitte: Abfahrt -> Erde, Erde -> Luftbild
DESC0 = 520; E0, E1 = 840, int(round(TTo["back"] * FPS)) - 1   # Abfahrt ab Bild 520; Erde 840..(Rueckblende-1)
EST = 870                                  # ab hier steht das Erdbild still -> langsamer Zoom im Overlay
MAP = []
for f in range(NF):
    t = f / FPS
    if t < TA: MAP.append(DESC0 + f)
    elif t < T2: MAP.append(min(E1, E0 + f - int(round(TA * FPS))))
    else: MAP.append(min(NF_OLD - 1, max(0, int(round((t - SH_) * FPS)))))
assert MAP[int(round(T2 * FPS))] >= 0
# Zoom-Faktor je Bild (stehendes Erdbild): ab erstem Bild >= EST im jeweiligen Abschnitt
ZS = []; zt = None; seg = None
for f in range(NF):
    t = f / FPS; s = 0 if t < TA else 1 if t < T2 else 2
    if s != seg: seg = s; zt = None
    m = MAP[f]
    if EST <= m <= E1 and s in (1, 2):
        if zt is None: zt = t
        ZS.append(round(1 + .025 * (t - zt), 4))
    else: ZS.append(1)
bg = "bg"; shutil.rmtree(bg, ignore_errors=True); os.makedirs(bg)
for f_ in os.listdir(f"{OLD}/bg"): os.link(f"{OLD}/bg/{f_}", f"{bg}/{f_}")
if not os.path.exists("fonts"): shutil.copytree(f"{OLD}/fonts", "fonts")
TT = dict(TTo); TT["nf"] = NF
for k in ("space", "zoomEnd", "back", "d0", "d1", "follow", "up"): TT[k] = TTo[k] + SH_
TT["ia"] = TA; TT["i2"] = T2
# ---- Overlay: Zeilennummern +2, Intro-Karten, Zoom, HUD erst ab der 750-Zeile
js = open(f"{OLD}/overlay.js").read()
js = re.sub(r"\b(Lt|wt|L)\((\d)\b", lambda m: f"{m.group(1)}({int(m.group(2)) + 2}", js)
js = js.replace("const anc = (k, t) => ANCH[k][MAP[fr(t)]];",
                "const zs = t => ZS[fr(t)];\nconst anc = (k, t) => { const p = ANCH[k][MAP[fr(t)]], z = zs(t); return (p && z !== 1) ? [540 + (p[0] - 540) * z, 960 + (p[1] - 960) * z] : p };")
js = js.replace("await setBg(t);\n", "await setBg(t); $('bg').style.transform = zs(t) !== 1 ? `scale(${zs(t)})` : '';\n")
js = js.replace("const hide = (t >", "const hide = t < TT.i2 + .1 || (t >")
js = js.replace("s = pop(t, .3, .4) * (hide ? 0 : 1)", "s = pop(t, TT.i2 + .1, .4) * (hide ? 0 : 1)")
js = js.replace("function dayTag(t) {\n  const s = pop(t, .05, .4) * fade(t, Lt(3).start - .2, Lt(3).start + .1);",
                "function dayTag(t) {\n  const s = pop(t, .05, .4) * fade(t, TT.ia - .2, TT.ia) + pop(t, TT.i2 + .05, .4) * fade(t, Lt(3).start - .2, Lt(3).start + .1);")
INTRO = r"""
// ---- Intro (immer): worum es geht + wie man mitmacht
function introCard(t) {
  const t0 = wt(0, /loch/i) - .25, s = pop(t, t0, .4) * fade(t, TT.ia - .15, TT.ia); if (s <= .01) return '';
  const g = pop(t, wt(0, /erdkern/i) - .2, .4);
  return `<div class="glass" style="left:50%;top:1010px;width:900px;transform:translateX(-50%) scale(${s});padding:22px 30px 26px;text-align:center">
    <div class="sub">die Mission</div><div style="font-size:74px;line-height:1.05">Ein Loch bis zum</div>
    <div style="font-size:112px;line-height:1.05;color:${ORANGE};transform:scale(${.6 + .4 * g});opacity:${Math.min(1, g)}">ERDKERN ⛏️</div>
    <div class="sub" style="margin-top:6px;opacity:${Math.min(1, g)}">6.370 km tief</div></div>`;
}
function rulesCard(t) {
  const t0 = Lt(1).start - .05, t1 = TT.i2 - .15, s = pop(t, t0, .4) * fade(t, t1, t1 + .15); if (s <= .01) return '';
  const r = (re, ic, html) => { const p = pop(t, wt(1, re) - .25, .35); return `<div style="display:flex;align-items:center;gap:22px;margin-top:14px;opacity:${.15 + .85 * Math.min(1, p)};transform:scale(${.7 + .3 * p});transform-origin:0 50%"><div style="width:92px;height:92px;flex:none;border-radius:50%;background:rgba(255,255,255,.12);font:900 52px/92px IB,Arial;text-align:center">${ic}</div><div style="font-size:54px">${html}</div></div>` };
  return `<div class="glass" style="left:50%;top:330px;width:900px;transform:translateX(-50%) scale(${s});padding:20px 34px 28px">
    <div style="text-align:center;font-size:44px;letter-spacing:3px;color:${ORANGE}">SO MACHST DU MIT</div>` +
    r(/folg/i, '👷', `Folgen = <span style="color:${ORANGE}">Arbeiter</span>`) +
    r(/like/i, '❤️', `1 Like = 1 Schaufel`) +
    r(/share/i, '↗️', `1 Share = 5 Schaufeln`) + `</div>`;
}
"""
js = js.replace("function flash(t) {", INTRO + "function flash(t) {")
js = js.replace("1 - Math.abs(t - TT.d0) / .18);", "1 - Math.abs(t - TT.d0) / .18, 1 - Math.abs(t - TT.ia) / .18, 1 - Math.abs(t - TT.i2) / .18);")
js = js.replace("let ui = dayTag(t) +", "let ui = introCard(t) + rulesCard(t) + dayTag(t) +")
js = js.replace("E.push({ k: 'whoosh', t: .05, d: 1.4 }, { k: 'chime', t: .3 });\n  for (let x = .5; x < TT.d0; x += .55)",
                "E.push({ k: 'whoosh', t: .05, d: TT.ia - .1 }, { k: 'chime', t: .3 }, { k: 'impact', t: wt(0, /erdkern/i) - .1 });\n"
                "  E.push({ k: 'impact', t: TT.ia }, { k: 'swish', t: L(1).start, d: .4 }, { k: 'pop', t: wt(1, /folg/i) - .25 }, { k: 'pop', t: wt(1, /like/i) - .25 }, { k: 'pop', t: wt(1, /share/i) - .25 });\n"
                "  E.push({ k: 'impact', t: TT.i2 }, { k: 'whoosh', t: TT.i2 + .05, d: 1.2 });\n  for (let x = TT.i2 + .4; x < TT.d0; x += .55)")
for need in ("introCard(t) + rulesCard", "TT.ia) / .18", "const zs", "TT.i2 + .4", "scale(${zs(t)})", "fade(t, TT.ia - .2, TT.ia)", "const hide = t < TT.i2"):
    assert need in js, need
open("overlay.js", "w").write(js); shutil.copy(f"{OLD}/head.html", "head.html")
head = open("head.html").read()
open("scene.html", "w").write(head + "const ANCH = " + json.dumps(old["ANCH"], separators=(",", ":")) + ";\nconst TT = " + json.dumps(TT) + ";\nconst MAP = " + json.dumps(MAP, separators=(",", ":")) + ";\nconst ZS = " + json.dumps(ZS, separators=(",", ":")) + ";\n" + js)
print("Zeilen", len(D), "Dauer", round(endn + TAIL, 2), "s NF", NF, "| Schnitte", round(TA, 2), round(T2, 2), "| Verschiebung", round(SH_, 2), "| alt-Start", MAP[int(round(T2 * FPS))])
