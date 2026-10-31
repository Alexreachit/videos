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
- TikToks: KEINE Hintergrundmusik (Alex 2026-10-22). Loop nahtlos: letzter Frame = erster Frame (gleiches Bild, gleicher Zaehler, Kamera zurueck auf Startzustand, Untertitel am Ende ausblenden), tail 0.1 s, letzter Satz geht grammatisch in den ersten ueber.
- Fakten vor jedem Video gegen Primaer-/serioese Quellen pruefen und Quellen nennen (Alex fand Zahlen verdaechtig).
- Figuren (2026-10-23): IMMER mg/lib/characters.py (SAM/VICTOR) woertlich nutzen; keine Ohren, keine Augenbrauen, keine Nase, nur Punktaugen + Strichmund. Alle Bilder eines Videos im selben Gemini-Chat erzeugen und auf das Referenzbild verweisen. Jedes Bild vor Verwendung auf Ohren/Brauen pruefen.

## Regel (Alex 2026-10-23): keine Phasen mehr, Musik folgt der Stimmung
- YT-Videos OHNE "Phase X"-Titelkarten. Übergänge sprachlich ("The first cause…", "So what can you do?"). YouTube-Kapitel nur in der Beschreibung.
- Musik: `"music":{"style":"adaptive","bpm":76,"gain":0.3}`. Im mk_project vor einer Zeile `M("tense"|"calm"|"bright")` setzen; gilt bis zur nächsten Änderung.
  calm = weiches E-Piano (C-Dur), tense = A-Moll-Pad + pulsierender Bass + leiser Herzschlag, bright = positiver Dur-Loop. Überblendung ~4 s, bleibt leise im Hintergrund.

## Stimme natürlicher (2026-10-23)
- Kein dynamisches loudnorm mehr pro Zeile (pumpte bei kurzen Sätzen den Anfang). Jetzt feste Verstärkung pro Zeile: `voice_gain()` in produce.py.
- Zusammengesetzte Wörter mit Bindestrich schreiben ("hundred-dollar bill"), sonst macht Andrew eine Pause ("hundred dollar … bill"). Wiederholungen wie "dollar … dollars" in einem Satz vermeiden.

## TikTok-Animationsstil (2026-10-25, Vorlage: mg/tt_debt)
- Dunkler Hintergrund + Punktmuster + blauer Glow, freigestellte Objekte (Gemini auf Magenta #FF00FF, 1:1), `python3 mg/lib/keyout.py src dst.png 900`.
- Pro Satz ein Objekt: Pop-in (elastisch), Wackeln/3D-Drehung, Ausgang nach oben; UI-Karten (iOS-Stil), Pills, Zähler. Sam als kleine freigestellte Figur.
- Loop: Hintergrund-Animation über ganze Zyklen von TL.dur, Hook-Objekt bei lt=0 ruhig (bob:0).

## TikTok-Musik (2026-10-25, Alex wollte eigene leise Musik passend zu Abschnitten)
- `"music":{"style":"tt","bpm":96,"gain":0.2,"duck_ratio":2}` (Alex 26.10.: 0.14 war zu leise) – leiser Groove (Kick/Shaker/Bass/Pluck), ~20 dB unter der Stimme.
- `spec.mood` = tense/calm/bright (gilt bis zur nächsten Änderung), `spec.cut: true` = kurzer Musik-Stopp vor der Zeile + tiefer Bass-Hit (Wendepunkte der Story).
- Kein Fade, damit der Loop nahtlos bleibt. Vorbild: @schraffur (Musik bricht bei Abschnittswechseln kurz ab).

## Feedback Alex zu tt_debt (2026-10-25) – fürs NÄCHSTE TikTok umsetzen
- Video gut. Nächstes Mal MEHR Animation. NUR WENN ES INHALTLICH PASST: Objekte bleiben über Satzgrenzen hinweg im Bild und bewegen sich weiter,
  statt zu verschwinden (z. B. Kreditkarte fliegt von der Mitte in die Ecke/zur Rechnung, schrumpft, dreht sich, wird Teil der nächsten Szene).
- Umsetzung: persistente Objekte mit Keyframes über die ganze Timeline (Position/Größe/Rotation je Zeile), Übergänge per Interpolation statt Exit/Pop-in.

## Referenz für mehr Animation: @wissentogo16 (ETF-Video, analysiert 2026-10-25)
- Maskottchen bleibt die GANZE Zeit klein unten rechts im Bild und reagiert (wackelt, wechselt Pose) -> bei uns Sam.
- Kleines Themen-Label oben (Emoji + 2–3 Wörter, z. B. "Der Motor", "Und die Kosten?"), wechselt pro Abschnitt.
- Alle ~2 s passiert etwas: 2–3 Beats pro Satz statt einem Objekt pro Satz.
- Objekte VERÄNDERN sich statt nur zu erscheinen: Baum wächst mit dem Zähler (57.000 -> 260.000 €), Glitzer-Partikel + pulsierender Ring beim Höhepunkt.
- Objekt verwandelt sich in Diagramm (Baum -> grüner Balken, zweiter Vergleichsbalken wächst dazu).
- Crash-Moment: roter Pfeil stürzt in Staubwolke, Bild wackelt, dann "-50 %" groß.
- Übergänge: schnelles Wegblenden mit Unschärfe, neues Objekt ploppt mit Sparkles rein.

## TikTok-Sprache (2026-10-25, final)
- Deutsch-Versuch mit Florian verworfen (Stimme gefiel Alex nicht). TikToks bleiben ENGLISCH mit Andrew (en-US-AndrewMultilingualNeural, +10%).
- Kompromiss (Alex ok): Themen mit internationalem Reiz wählen, Caption + Hashtags englisch/international (#money #finance #investing #personalfinance #fyp), keine deutschen Hashtags.

## Andrew mit mehr Emotion (2026-10-26, erster Test tt_car)
- Pro Zeile in project.json: `"rate"`, `"pitch"` (z. B. "+8Hz"), `"volume"` (z. B. "+10%"), `"pause"` (Sek. Stille davor).
- Faustregeln: Schock/Pointe schneller + höher + lauter; dramatische Zahl langsamer + tiefer; Wendung mit kurzer Pause davor.
- Text für Emotion schreiben: kurze Sätze, Fragen ("The worst?"), "..." für Spannungspausen, Ausrufe, "For nothing!".
- KEINE Stichwort-Fragen wie "The worst? ..." / "The best? ..." – klingt vorgelesen. Ganze, gesprochene Sätze: "The worst one is ...". "..." sparsam.

## Animationsstil YT 11 als Standard (Feedback 2026-10-26)
- Alex findet die Weltkarten-Animationen und alle anderen Animationen aus yt_bank11 "toll".
- Ab jetzt auch fuer TikToks (9:16) in diesem Stil arbeiten: Karten-Engine (mg/lib/mapdata.js, MAPP, Kamera-Zoom auf Land/Stadt, Pins, CLOSED-Stempel, Punkte-Wolken, Boegen fuer Wege/Lieferungen, Laender-Highlight), Zaehler, Balken-/Rangvergleiche, Scheck-/Karten-Objekte, Checklisten.
- Darauf aufbauen und pro Video etwas Neues ausprobieren (neue Kartentypen, Routen-Animationen, Vergleiche), nicht nur kopieren.

## Stimme & Musik am Stueck (Feedback 2026-10-26, tt_suez)
- Keine Pitch-Verschiebung (pitch) und keine Lautstaerke-Spruenge (volume) pro Zeile: ab +7 Hz/+8 % klingt Andrew wie eine andere Person. Emotion nur ueber Text, Satzzeichen und leichte rate-Unterschiede (+8 % bis +12 %).
- Musik-Stimmung hoechstens 2-3 Wechsel pro TikTok; keinen "bright"-Wechsel mit Cut kurz vor dem Ende – das faellt als Bruch auf.

## Hook-Format ab 2026-10-27 (Wunsch Kanalbesitzer)
- Videos (TikTok, wo passend auch YT) beginnen mit "Why you should never ..." / "Why you shouldn't ..." / "Why you should ..." als erstem Satz.
- Themen muessen wirklich spannend sein und viele Leute betreffen (Alltag + Geld + Geschichte), nicht trocken. Die Begruendung kommt als ueberraschende, belegte Geschichte/Zahl.
- Erster Satz = Hook (Titel gross im Bild ab Frame 0), danach sofort die erste ueberraschende Zahl.

## TikTok-Laenge ab 2026-10-27
- Ziel ca. 25 s (max. ~30 s): ~70 Woerter, 7-8 kurze Saetze, rate +16 %, lead 0.05 / gap 0.08, Szenenwechsel alle ~3 s, Ueberblendungen 0.25 s.
- Zaehler/Diagramme muessen exakt beim gesprochenen Wort stehen (bei kurzen Zeilen frueh starten: ab ~20 % der Zeile).

## TikTok-Themenliste (vom Kanalbesitzer abgesegnet, 2026-10-28)
- Why you should never buy a diamond ring (De Beers 1947 "A diamond is forever", Wiederverkaufswert)
- Why you should never tell a car dealer how you're paying (Gewinn ueber Finanzierung)
- Why you should never exchange money at the airport
- Why you should never go grocery shopping hungry
- Why you should never buy bottled water
- Why you should never accept the first salary offer
- Why you should never buy a phone on release day
- Why you should never buy a timeshare
- Why you should never ignore compound interest (Manhattan fuer 24 $)
- erledigt: Why you should never throw away your old LEGO (tt_lego)
- NICHT: Hyperinflation/"Geld unter der Matratze" (gefiel ihm nicht)

## Algorithmus-Erkenntnisse (dmscales, "Longform/Shorts Algorithm Explained", vom Kanalbesitzer geschickt 2026-10-28)
- YouTube muss sofort verstehen, WORUM es geht und FUER WEN: klarer Titel (Thema woertlich), Beschreibung mit Keywords + Kapiteln, Thumbnail mit klar erkennbaren Objekten/Gesichtern/wenig grossem Text (YouTube "liest" das Thumbnail).
- Nische konsequent halten (Geld/Wirtschaft erklaert) -> Zielgruppe wird schneller erkannt; keine Themen-Spruenge.
- Getestet wird in Wellen (kleine Gruppe -> mehr Impressions). Entscheidend: 1) CTR (Thumbnail+Titel+Idee, Schnitt ~4-5 %, <3 % wird nicht gepusht), 2) Retention (wichtiger als CTR: Kurve flach + hoch, kleiner Anfangs-Knick -> Hook!), 3) Session-Zeit.
- Steiler Abfall am Anfang = Hook schlecht; steile Kurve insgesamt = Story/Idee schlecht.
- Shorts: Hook ab Frame 0, perfekte Retention kann ein Short retten; Loop -> >100 % Wiedergabe; breit verstaendliche Animations-Themen gehen auch auf neuen Kanaelen viral.
- Kanal "legit" wirken lassen: Profilbild, Banner, Beschreibung, gleichmaessiges Branding.

## Ablauf ab 2026-10-29 (Wunsch Kanalbesitzer)
- VOR jedem neuen Video/TikTok/Short erst die Idee (Thema + Hook + kurzer Ablauf) vorschlagen und auf sein OK warten – erst dann recherchieren/Bilder erzeugen/bauen.
- Nicht jedes Video mit Schiffen/Karten "auf Krampf" – Karte und Schiffsthemen nur, wenn es wirklich passt; Themen abwechseln.

## Bewertung von Aufrufen (Alex 2026-10-29)
- Shorts-Aufrufe sind viel leichter zu bekommen als Aufrufe auf langen Videos. 100 Aufrufe auf einem langen Video zählen mehr als 1.000 auf einem Short.
- In Analysen Shorts und lange Videos getrennt bewerten. Bei langen Videos vor allem auf Aufrufe, CTR, Wiedergabezeit und Abos achten, nicht auf rohe Shorts-Zahlen.

## Langform-Einstieg für Hover-Vorschau (Erkenntnis Alex 2026-10-30)
- Viele Aufrufe langer Videos kommen aus der YouTube-Suche per Hover-Vorschau (Video spielt kurz an, ohne Klick). Beim Bank-Video wurde in den ersten Sekunden nicht klar, was passiert -> niemand blieb.
- Darum ab Sekunde 0: worum es geht + größte Zahl/These sofort als großer Text im Bild (Vorschau läuft oft stumm) und im ersten Satz; Bewegung ab Frame 0; kein Titel-/Logo-Intro.
- Die ersten ~5 s müssen auch ohne Ton verständlich und neugierig machend sein (Frage/Konflikt sichtbar).

## Shorts-Stil verbindlich (Alex 2026-10-31)
- Shorts IMMER im hellen Sky-Stil wie tt_svb / ys_felicity / tt_suez (Vorlage: mg/tt_svb/scene.html bzw. mg/ys_eiffel): heller Himmel-Verlauf, Karte (hellblau/weiß) wo passend, große Gemini-Hauptobjekte, Überblendungen. KEIN dunkler Navy-Hintergrund wie ys_knight (Knight + Eiffel v1 wurden deshalb abgelehnt / liefen schlecht).
- Gemini-Bilder holen: im Gemini-Tab per JS als PNG herunterladen (<a download>) -> landet in C:\Users\Alex\Downloads -> device_stage_files -> keyout.py.

## Musik "suspense" (ab 31.10.2026, Wunsch Alex: Musik soll Spannung aufbauen, damit Leute länger schauen)
- style="suspense": Hook leise (Drone, tickende Uhr, Herzschlag) -> ab Zeile 1 Aufbau (Puls-Bass, Streicher-Tremolo wird heller,
  Uhr doppelt so schnell, Riser) -> am ersten spec.cut 0,4 s Stille + Boom + voller ttdark-Beat (Drop) -> letzte Zeile zurück auf Hook-Niveau (Loop).
- spec.cut deshalb auf den Höhepunkt der Story legen (die krasse Zahl / der Wendepunkt), nur EIN cut pro Short.
- Helle Hintergründe bevorzugt (Alex 31.10.: "hellere Hintergründe kommen besser an").
