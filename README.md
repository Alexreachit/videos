# Video-Pipeline

Aus Skript und Bildprompts entsteht automatisch ein Video mit Sprecherstimme und Wort-für-Wort-Untertiteln. Die Bilder erzeugt ein kostenloser Bilddienst, alles läuft auf GitHub.

## Dateien

| Datei | Wofür |
|-------|-------|
| `script.txt` | Der Sprechertext. Eine Zeile = eine Szene = ein Bild |
| `prompts.txt` | Ein Bildprompt pro Szene, gleiche Zeilennummer wie in `script.txt` |
| `stil.txt` | Stil und Figurenbeschreibung, wird jedem Prompt vorangestellt |
| `generate_images.py` | Holt die Bilder vom Gratis-Bilddienst (macht dort weiter, wo es aufgehört hat) |
| `build_video.py` | Baut aus Bildern, Stimme und Untertiteln das Video |
| `bilder/` | Die fertigen Bilder `01.jpg`, `02.jpg`, ... |

## So läuft ein Video

Alles startet unter **Actions**, links **Video bauen**, rechts **Run workflow**. Dort wählst du bei *Was soll passieren?*:

1. **bilder**: Erzeugt bis zu 37 fehlende Bilder (Wert bei *max_bilder*) und speichert sie im Ordner `bilder/`. Reicht das Tageslimit nicht, starte es später noch einmal. Es macht dort weiter, wo es aufgehört hat. Die zweite Hälfte also gern am nächsten Tag.
2. **video**: Baut das echte Video, sobald alle Bilder da sind. Fertige `video.mp4` unten im Lauf unter **Artifacts** herunterladen.
3. **testlauf**: Baut ein Probevideo mit stiller Tonspur und Platzhalterbildern, falls etwas schiefläuft.

## Einzelne Bilder austauschen

Gefällt dir ein Bild nicht, lösche `bilder/NN.jpg` im Repo (Datei öffnen, Papierkorb) und starte **bilder** noch einmal. Oder lade ein eigenes Bild mit demselben Namen hoch.

## Neues Video

Sag Claude das Thema. Es ersetzt `script.txt`, `prompts.txt` und bei Bedarf `stil.txt`. Lösche vorher den Inhalt von `bilder/` (außer `LIES_MICH.txt`).

## Grenzen

- Die Stimme kommt von edge-tts. Fällt der Dienst aus, nimmt das Programm automatisch Piper (offline, klingt etwas robotischer).
- Die Wort-Timings werden aus der Sprechdauer berechnet, nicht gemessen. Sie passen meist gut.
- Der Gratis-Bilddienst kann die Figur leicht unterschiedlich zeichnen und hat Tageslimits.
- Das Repo ist öffentlich, damit GitHub die Rechenzeit gratis stellt.
