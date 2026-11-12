# Roundhead Island LIVE

Interaktives Aufbau-Spiel für TikTok LIVE. Die Zuschauer bauen die Insel mit Likes, Follows, Geschenken und dem Chat.
**Bürgermeister Sam** kommentiert mit Andrews Stimme und beantwortet Fragen aus dem Chat.
Alles läuft lokal und kostenlos. Du brauchst keine Passwörter und keine API-Schlüssel.

## Was im Spiel passiert
| Zuschauer macht | Spiel |
|---|---|
| tritt bei | wird ein Rundkopf mit Namen auf der Insel |
| Likes (doppelt tippen) | füllen das Stadt-Ziel → Brunnen, Leuchtturm, Sam-Statue, Riesenrad, goldenes Rathaus |
| folgt | bekommt ein eigenes Haus und „NEUER EINWOHNER!“, alle 10 Follows gibt es ein Feuerwerk |
| Geschenk | Haus wächst (Wohnpunkte): Starterhaus → … → Luxus-Villa, mit Rangliste |
| schreibt „wo bin ich“ | ein Pfeil zeigt auf sein Haus oder seine Figur |
| Frage im Chat | Sam antwortet mit Stimme (lokale KI) |
| alle 4 Minuten | Happy Hour: alles zählt ×3 |

## Einmalig einrichten
1. **Node.js** (LTS) installieren: https://nodejs.org
2. **Python** installieren und danach `pip install edge-tts` ausführen (das ist die Stimme).
3. **Ollama** installieren (https://ollama.com) und danach `ollama pull qwen2.5:7b` ausführen (das ist die KI für Sam). Bei schwacher Grafikkarte nimmst du `qwen2.5:3b` und trägst das in `config.json` ein.
4. In `config.json` deinen TikTok-Namen bei `tiktokUser` eintragen. Die Datei wird beim ersten Start aus `config.example.json` erstellt.

## Starten
- **Test ohne TikTok:** `START.bat --sim`. Fake-Zuschauer, die KI und die Stimme laufen dabei echt.
- **Nur das Spiel ansehen:** `game.html?sim=1` im Browser öffnen. Das läuft ohne Server, Sam spricht dann mit Vorlagen.
- **Echtes Live:**
  1. In TikTok LIVE Studio live gehen.
  2. Doppelklick auf `START.bat`.
  3. In LIVE Studio das Browserfenster `http://localhost:8787/live/game.html` als Quelle (Fenster- oder Browser-Quelle, Hochformat) hinzufügen.
  4. Damit Sams Stimme im Stream zu hören ist, den Ton des Browsers in LIVE Studio mit aufnehmen.

## Hinweise
- `tiktok-live-connector` ist inoffiziell. Wenn TikTok etwas ändert, hilft meistens `npm update`.
- Sam ignoriert Beleidigungen und heikle Themen und redet nicht über echte Personen.
- Ab und zu selbst in den Chat schreiben. TikTok mag Lives mit echter Interaktion.
