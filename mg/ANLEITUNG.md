# Motion-Graphics-Engine: Anleitung fuer Projekte (mg/<projekt>/)

Ein Projekt = ein Ordner `mg/<projekt>/` mit `project.json` und `scene.html` (plus optional `img/`).
`mg/produce.py` macht daraus: Stimme Andrew (edge-tts, nur auf GitHub erreichbar) -> Timeline mit Wortzeiten ->
Frames (Playwright/Chromium) -> Musik + SFX (selbst synthetisiert) -> MP4.

## project.json
```json
{
 "title": "TikTok 2: ...",
 "size": [1080, 1920], "fps": 30, "scene": "scene.html",
 "voice": "en-US-AndrewMultilingualNeural", "rate": "+10%",
 "lead": 0.4, "gap": 0.25, "tail": 1.8,
 "music": {"bpm": 100, "mood": "minor", "energy": 0.7},
 "lines": [ {"text": "First sentence.", "min_start": 0.5}, {"text": "..."} ]
}
```
- Stimme und Rate NIE aendern. `mood`: minor | major | tense. `energy` 0..1 (Drums ab 0.3).
- `min_start` (Sekunden) zwingt eine Zeile spaeter zu starten (z. B. Platz fuer ein Intro ohne Sprache).
- Eine Zeile = ein Satz bzw. ein Szenenschritt. Optional pro Zeile `"spec": {...}` (frei, die Szene liest es aus `MG.TL.lines[i].spec`).

## scene.html (Vertrag)
- Laedt `<script src="../lib/core.js"></script>` (Objekt `MG`).
- `window.setTimeline(tl)`: bekommt `{lines:[{text,start,end,words:[[wort,von,bis],...],spec}], dur}` (Wortzeiten relativ zum Zeilenstart). Mindestens `MG.TL = tl` setzen.
- `window.draw(t)`: zeichnet den Zustand zur Zeit t (Sekunden) **deterministisch** (kein Date.now, kein Math.random, keine CSS-Transitions/Animations; alles aus t berechnen). Frames werden einzeln und parallel in mehreren Browsern gerendert.
- `window.sfxEvents()`: Liste `{k, t, ...}`. Arten: whoosh(d), swish(d,pan), tap, beep(f), chime, riser(d), impact, shimmer, pop, ding, tick(f), cash, error, thud, type(n), heartbeat(n). Zeiten aus der Timeline ableiten (`MG.L(i).start`).
- Bilder: `MG.preload([...])` aufrufen, dann wartet der Renderer auf `window.ready`.
- Helfer: `MG.cl(t,a,b)` (0..1), `MG.ez` (ease-out), `MG.ei` (ease-in-out), `MG.bo` (Overshoot), `MG.el` (elastisch), `MG.lerp`, `MG.L(i)` (Zeile i, negativ = von hinten), `MG.cur(t)` (aktuelle Zeile), `MG.fmt(v,d,pre,suf)`, `MG.rnd(seed)`,
  `MG.captions(t,{y,size,maxWords,hl,stageW})` -> HTML fuer Untertitel mit Wort-Hervorhebung, `MG.finish(stage,w,h)` (Vignette + Filmkorn einmal einfuegen), `MG.grainTick(t)` pro Frame.

## Qualitaetsregeln (vom Kanalbesitzer)
- Echte Animation: Objekte bewegen, bauen sich auf, verwandeln sich, Kamera faehrt durch 3D-Raeume (CSS 3D / SVG). **Keine** billigen Filter als Ersatz (kein reiner Ken-Burns-Zoom auf ein Standbild, kein Glitch, kein Wackeln, kein Staub-Overlay, keine fallenden Muenzen als Deko-Overlay).
- Filmreifer Einstieg: die ersten 3–5 s sind eine kleine, konkrete Kinoszene zum Thema (Beispiel tt01: Karte tippt aufs Terminal, Close-up, Flash-Uebergang). Starker Text-Hook oben.
- Alle 3–6 s ein neuer visueller Schritt; saubere Uebergaenge (Wischen, Match-Cut, Kamerafahrt, Flash), Sound-Effekt auf jedem Uebergang/Einblenden.
- Eine Zahl pro Szene, gross und lesbar. Untertitel-Zone (9:16: y 1330–1560) frei halten.
- Farben: dunkler, satter Hintergrund mit Tiefe (Verlaeufe, Licht), kraeftige Akzente (#ffd166 Gold, #35e08a Gruen, #ff5d5d Rot, #60a5fa Blau). Schrift Arial/Helvetica fett.
- Fakten: nur gerundete, belegbare Groessen, "roughly/typically/about" wo noetig. Keine Anlageberatung.

## Testen (lokal, ohne echte Stimme)
```
python3 mg/produce.py <projekt> --fake-tts --stills 0.5,2,4,8,15,30     # Einzelbilder -> output/mg_<projekt>/still_*.jpg
python3 mg/produce.py <projekt> --fake-tts --limit 8 --workers 4        # kurzes Testvideo der ersten 8 s
```
Die Fake-Stimme ist langsamer/ungenauer als Andrew; Zeiten immer aus der Timeline ableiten, nie fest verdrahten.
Rendern auf GitHub: Projektname in `mg/render_queue.txt` eintragen und pushen (Workflow "Motion Graphics Warteschlange").

## Farbschema ab 2026-10-19 (Alex' Wahl)
- Hintergrund: Himmelblau mit nur leicht dunklen Ecken -> `lib/theme_sky.py` (`apply(html)` in build_scene.py aufrufen).
- Gemini-Bilder: kraeftige, sonnige Farben, kein Grau/Braun/Sepia (Prompt-Zusatz `GEMINI_STYLE` in theme_sky.py).
- TikToks: immer Vollbild 9:16 (Vorlage mg/tt_million), kein dunkler Balken in der Mitte, obere Texte etwas tiefer.
- YouTube-Hook (ab 2026-10-19): die ersten ~5 Sekunden müssen packen – überraschende Zahl/These sofort im Bild und im ersten Satz, offene Frage ("…aber bis zum Ende siehst du, warum…"), kein ruhiger Titel-Einstieg; erste Szene mit Bewegung.
- TikToks (ab 2026-10-19): Englisch, ca. 30 s, eigenständig (keine Part-Serien); Aufbau: Hook + große Zahl ab Sekunde 0, offene Frage, Auflösung/Wendung, Kommentar-Frage am Ende (Vorlage mg/tt_banker).
- Sounds (ab 2026-10-20): KEIN 'riser' (anschwellendes Summen) mehr; nur etablierte Sounds: whoosh, swish, pop, ding, cash (Ka-ching), click, impact (Boom), tick, bell.
- Video 9 (yt_tax9, 2026-10-21): neue Szenentypen in mg/yt_tax9/sc9.js (hook=Steuerbescheid, score, rule=Splitscreen 2 Figuren, loan=Chart, step=Balken-Reset, share); Story mit wiederkehrenden Figuren Sam vs. Victor; Gegenargumente-Kapitel. Stempel in Vollbild-Szenen per x/y positionieren (nie ueber Gesichter).
- Workflow: Videos >95 MB werden als *.part in renders/ abgelegt (zusammensetzen: cat *.part > x.mp4).
- Musik (ab Video 9): leises Musikbett "music":{"style":"soft","bpm":76,"gain":0.3} + "sfx_vary":true (E-Piano, kein Schlagzeug, ca. 17 dB unter der Stimme, Ducking).
- TTS: Aufzaehlungen wie 'buy, borrow, die' rattert Andrew ohne Pause herunter -> als 'Step one: buy. Step two: borrow. ...' oder mit 'and' schreiben.
- TikTok-Regeln (Analyse 2026-10-22): 20-30 s; Loop (letzter Satz fuehrt in den ersten, z.B. '...the next time you hear:' -> 'You just won...'); Bildwechsel alle ~3-4 s (kurze Saetze, je eigenes Bild); Aufloesung am Ende; Beschreibung mit Keyword + 2-3 Hashtags; Vorlage mg/tt_lotto (laufender Zaehler oben).
- Gemini: Bilder kommen teils als kaputte <img> (naturalWidth 0) -> src neu setzen; bei 'nur textbasierte KI' ist das Tageslimit erreicht.
