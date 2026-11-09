# Technologie-Auswahl (Stand: 10. November 2026)

Preise sind Listenpreise laut Anbieter-/Vergleichsseiten im November 2026 und ändern sich oft.
Vor jeder Freigabe zeigt `estimate` die Kosten aus `cine/config/default.yaml` – dort pflegen.

## Videogenerierung

| Modell | Bildqualität | Bewegung | POV-Eignung | Konsistenz | API | Preis 720p | Clip | Ton |
|---|---|---|---|---|---|---|---|---|
| **Gemini Omni 1.2 Flash** (gewählt) | sehr hoch (Arena-Platz 1, vorläufig) | sehr gut | gut – Kamera per Text steuerbar | Startbild, Endbild, bis 6 Referenzbilder | Replicate, Gemini API | ~0,07 $/s | 3–15 s | ja, synchron |
| Kling 4.0 (Fallback) | hoch | sehr gut | gut | Startbild | Kling, fal, Replicate | ~0,16 $/s | bis 30 s | ja |
| Veo 3.1 Fast / Lite | hoch / mittel | gut | gut | Startbild | Vertex AI, Replicate | 0,10 / 0,05 $/s | 4–8 s | ja |
| Seedance 2.0 | hoch | gut | gut | Referenzen | BytePlus | ~0,15 $/s | 15 s | ja |
| Runway Gen-4.5 | hoch | gut | mittel | Referenzbild | Runway | 0,12 $/s | 10 s | nein |
| Wan 2.2 (Open Source) | mittel–hoch | mittel | mittel | Startbild | lokal | 0 $ + GPU | 5 s | nein |
| Sora 2 | – | – | – | – | API seit 24.09.2026 eingestellt | – | – | – |

**Begründung:** Omni ist aktuell eines der bestbewerteten Modelle, gehört zu den günstigsten
Spitzenmodellen und kann das, was POV-Konsistenz braucht: Startbild (letzter Frame der Vorszene
→ nahtloser Anschluss) und Referenzbilder (Hände, Zombie, Schauplatz). Der Ton entsteht synchron
zum Bild – das löst das schwierigste Sound-Sync-Problem schon im Modell. Kling 4.0 ist als
Ausweichmodell eingetragen.

**Wichtig:**
- Laut Google ist das *Bearbeiten/Verlängern hochgeladener Videos* mit Omni im EWR (also Deutschland)
  nicht verfügbar. Die Pipeline nutzt das deshalb bewusst nicht – sie arbeitet mit Startbild-Verkettung.
- Jeder Omni-Clip trägt ein unsichtbares SynthID-Wasserzeichen. Auf TikTok/YouTube sollte KI-Inhalt
  ohnehin als solcher gekennzeichnet werden.
- Nutzungsrechte vor kommerzieller Nutzung in den aktuellen Bedingungen von Google und Replicate prüfen.

**Lokal/Open Source:** Wan 2.2 (Apache 2.0) braucht eine Nvidia-GPU mit mind. ca. 8 GB VRAM und
mehrere Minuten pro 5-s-Clip. GitHub Actions hat keine GPU, ein älterer Laptop auch nicht – daher
nicht im Standard-Stack. Ein `wan`-Provider lässt sich bei vorhandener GPU nachrüsten (neue
Unterklasse von `VideoProvider`).

**Kostenloser Weg (`manual`):** Google bietet 15-s-Omni-Clips in Google Vids ohne Zusatzkosten mit
einem Google-Konto an. Die Pipeline erzeugt dafür fertige Prompt-Karten samt Startbild; du legst die
Clips in `inbox/` ab, der Rest läuft automatisch.

## Bilder (Referenzen)

| Option | Kosten | Automatisierbar |
|---|---|---|
| Gemini im Browser (wie bisher) | 0 $ (Tageslimit) | über `manual`-Karten |
| Bildmodell über Replicate | ca. 0,04 $/Bild | ja |

## Ton

| Option | Qualität | Kosten | Sync |
|---|---|---|---|
| Originalton der Videomodelle | gut, szenengenau | im Clippreis enthalten | automatisch |
| `procedural` (eingebaut) | solide Basis, exakt timebar | 0 $ | per Cue-Zeitpunkt |
| eigene CC0-Dateien in `cine/assets/sfx/` | so gut wie die Datei | 0 $ | per Cue-Zeitpunkt |
| ElevenLabs Sound Effects | sehr gut | ~0,002 $/s, kommerziell ab Starter-Plan | per Cue-Zeitpunkt |

## Schnitt und Postproduktion

ffmpeg (frei): Szenen auf exakte Länge, Übergänge (Reißschwenk-Unschärfe, Abblende, Blitz),
Farbkorrektur (Nacht-Horror-Grade), Vignette, Filmkorn, Lautheit −14 LUFS, H.264-Export.
Hochskalierung übernimmt Omni selbst (1080p-Option, Aufpreis). Stabilisierung ist bei POV bewusst
nicht aktiv – das Wackeln gehört zum Look.

## Kosten für ein 60-Sekunden-Video (720p, Omni)

| Posten | USD |
|---|---:|
| 7 Clips, 60 s | 4,20 |
| 3 Referenzbilder | 0,12 |
| Ton (eingebaut, lokal) | 0,00 |
| Schnitt/Rendering (GitHub Actions, öffentliches Repo) | 0,00 |
| **Ein Durchgang** | **4,32** |
| inkl. 50 % Reserve für Neuversuche | 6,48 |
| 1080p statt 720p | ca. +2 |
| optional KI-Bildprüfung (Gemini) | ca. 0,07 |
| optional ElevenLabs-SFX | ca. 0,10 |

## Quellen

- teamday.ai – Best AI Video Models (Preise/Rankings, Stand 8. Nov. 2026)
- devtk.ai – AI Video API Pricing 2026
- blog.google – Gemini Omni 1.2 Flash, Veo 3.1 Lite
- replicate.com/google/gemini-omni-1.2-flash (Eingabefelder)
- github.com/google-gemini/gemini-skills (Omni-API-Hinweise, EWR-Einschränkung)
- insiderllm.com – Lokale Videogenerierung (VRAM, Wan-Lizenz)
- stork.ai – ElevenLabs Sound Effects 2026
