# Video-Pipeline

Aus einem Skript und Bildern wird automatisch ein Video mit Sprecherstimme und Wort-für-Wort-Untertiteln.

## Was wo liegt

| Datei | Wofür |
|-------|-------|
| `script.txt` | Dein Text. Eine Zeile = eine Szene = ein Bild |
| `bilder/` | Deine Bilder: `01.png`, `02.png`, ... |
| `bildprompts.md` | Vorlage, damit die Figuren in allen Bildern gleich aussehen |
| `build_video.py` | Das Programm, das alles zusammenbaut |
| `.github/workflows/video.yml` | Sagt GitHub, wie es das Programm startet |

## Einmalig einrichten

1. Auf github.com ein neues Repository anlegen (Plus oben rechts, New repository, Name z. B. `videos`, **Public**).
2. Alle Dateien aus diesem Ordner hochladen: Im Repo auf **Add file**, dann **Upload files**, den Inhalt des Ordners hineinziehen, **Commit changes**.
   Wichtig: Der versteckte Ordner `.github` muss mit hoch. Geht das auf dem iPad nicht, lasse Claude Code die Dateien ins Repo schieben.
3. Im Repo auf **Actions** gehen. Falls GitHub fragt, Workflows mit der grünen Taste aktivieren.

## Testlauf (ohne Bilder, ohne Stimme)

1. **Actions**, links **Video bauen**, **Run workflow**, Haken bei *Testlauf* setzen, bestätigen.
2. Nach 1 bis 3 Minuten ist der Lauf grün. Öffne ihn und lade unten unter **Artifacts** die Datei `video` herunter (ZIP mit `test.mp4`).
3. Du siehst farbige Platzhalter und die Untertitel. So weißt du, dass alles funktioniert.

## Ein echtes Video machen

1. Thema wählen und `script.txt` ersetzen. Kurze Sätze, eine Zeile pro Szene.
   Claude Code schreibt es dir: *„Schreibe script.txt zu [Thema], 40 Szenen, kurze Sätze wie ein Erzähler. Schreibe in bildprompts.md pro Szene einen Bildprompt im selben Stil.“*
2. Bilder erzeugen, immer im selben Dienst, mit dem Stil-Block aus `bildprompts.md`:
   Bing Image Creator (bing.com/images/create), Leonardo (leonardo.ai), Ideogram (ideogram.ai) oder Gemini (gemini.google.com). Gratis-Limits sind klein, verteile es auf mehrere Tage.
3. Bilder als `01.png`, `02.png`, ... in den Ordner `bilder/` hochladen. Genau so viele Bilder wie Zeilen in `script.txt`.
4. **Actions**, **Video bauen**, **Run workflow** (ohne Haken), warten, `video` herunterladen. Darin liegt `video.mp4`.
5. Passt etwas nicht, sage Claude Code genau, was (z. B. „Szene 12 ist zu schnell“), und baue neu.
6. Auf studio.youtube.com hochladen.

## Einstellungen ändern

Oben in `build_video.py`: Stimme (`VOICE`), Sprechtempo (`VOICE_RATE`), Schriftgröße (`SUB_SIZE`), Farbe des aktuellen Wortes (`COLOR_HIGHLIGHT`).
Weitere deutsche Stimmen: `de-DE-KatjaNeural`, `de-DE-KillianNeural`.

## Bekannte Grenzen

- Die Stimme kommt von edge-tts. Fällt der Dienst auf GitHub aus, nimmt das Programm automatisch Piper (offline, klingt etwas robotischer).
- Die Wort-Timings werden aus der Sprechdauer berechnet, nicht aus der Audiodatei gemessen. Sie passen meist gut, können aber bei langen Wörtern leicht abweichen.
- Das Repo ist öffentlich, damit GitHub die Rechenzeit gratis stellt. Dein Skript ist also für alle sichtbar. Bei privaten Repos gibt es ein monatliches Freikontingent.
