# Video 7 (komplett animiert)
- szenen.tsv: Sprechertext | Keyframe-Prompt | Bewegungs-Prompt (53 Szenen, je ein 8-s-Flow-Clip, Clip wird auf Sprechdauer ~0.8x gedehnt)
- status.tsv: Fortschritt je Szene (keyframe / clip)
- Ablauf: Keyframes (Gemini, gratis) -> Flow Bild-zu-Video (10 Credits/Clip) -> Stimme Andrew -> Schnitt

## Qualitaetsregeln (Alex, 15.10.)
- Bewegung nur durch echte Animation (Flow-Clips). Keine Billig-Filter: kein Ken-Burns-Zoom auf Standbildern, keine Wackel-/Glitch-/Vintage-Filter als Ersatz fuer Animation.
- Clip fehlt oder misslingt -> neu generieren, nicht mit Filter ueberbruecken.
- Schnitt: Szenenwechsel an Satzgrenzen, Bewegungsrichtung der Clips passt zum naechsten (Match Cut), Tempo variieren, kurze Ueberblendungen nur wo sie Sinn haben.
- Ton: Andrew-Stimme, dezente Musik unter der Stimme, gezielte Soundeffekte (Piepton, Papier, Muenzen) synchron zum Bild.
- Einblendungen: wenige, saubere Schlagworte/Zahlen passend zur Szene, nicht dauerhaft.
