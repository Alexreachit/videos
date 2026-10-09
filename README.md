# Video-Pipeline

Aus Skript und Bildern entsteht automatisch ein Video mit Sprecherstimme, Wort-für-Wort-Untertiteln, Phasen-Titelkarten und sanften Zooms. Alles läuft kostenlos auf GitHub.

## Dateien

| Datei | Wofür |
|-------|-------|
| `script.txt` / `script_en.txt` | Sprechertext deutsch / englisch. Eine Zeile = eine Szene = ein Bild |
| `prompts.txt` | Bildprompt pro Szene (gleiche Zeilennummer wie im Skript) |
| `stil.txt` | Stil- und Figurenbeschreibung |
| `bilder/` | Die fertigen Bilder `01.jpg`, `02.jpg`, ... (1280x720). Sie entstehen in Gemini (im Chrome des Nutzers) |
| `build_video.py` | Baut aus Bildern, Stimme und Untertiteln das Video |
| `voices_test.py` | Erzeugt Hörproben mit mehreren Gratis-Stimmen |

## Video bauen

Auf GitHub unter **Actions**, links **Video bauen**, rechts **Run workflow**. Optionen bei *Was soll passieren?*:

- **video**: deutsches Video (Stimme Florian). Fertige Datei unten im Lauf unter **Artifacts**.
- **video_en**: englisches Video (Stimme Andrew), gleiche Bilder.
- **testlauf**: Probe mit stiller Tonspur und Platzhalterbildern.
- **stimmen**: Hörproben von 12 Stimmen.
- *max_szenen*: nur die ersten N Szenen bauen (Vorschau), `0` = ganzes Video.

## Wie es gemacht ist

- Die Wort-Timings der Untertitel kommen aus den gemessenen Wortgrenzen der Stimme (edge-tts). Fehlen sie, wird geschätzt.
- Szenen, die mit `Phase <Zahl>:` beginnen, werden zu einer abgedunkelten Titelkarte.
- Jede Szene bekommt abwechselnd Zoom hinein, Zoom heraus oder Schwenk.
- Das Repo ist öffentlich, damit GitHub die Rechenzeit gratis stellt.

## Neues Video

Neues `script.txt` (und `script_en.txt`), `prompts.txt` und bei Bedarf `stil.txt` schreiben, `bilder/` leeren, Bilder erzeugen, bauen.
