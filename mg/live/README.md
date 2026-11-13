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

## Einmalig einrichten (Laptop)
1. Den Ordner `RoundheadLive` irgendwohin entpacken, z. B. auf den Desktop.
2. In `RoundheadLive\live` **SETUP.bat** doppelklicken. Es installiert Node.js und Python (falls sie fehlen) sowie die Stimme und die Live-Verbindung.
   Wenn es etwas installiert hat, SETUP.bat danach **noch einmal** starten.
3. Am Ende öffnet sich `config.json`. Dort bei `tiktokUser` deinen TikTok-Namen ohne @ eintragen und speichern.

## Starten
- **Test ohne TikTok:** `TEST.bat`. Es kommen Fake-Zuschauer, Sam spricht echt.
- **Echtes Live:**
  1. In TikTok LIVE Studio live gehen.
  2. `START.bat` doppelklicken. Der Browser öffnet das Spiel.
  3. In LIVE Studio das Browserfenster als Quelle (Fensteraufnahme, Hochformat) hinzufügen und den Ton des Browsers mit aufnehmen.

## Laptop-Modus (Standard)
- Das Spiel läuft mit halber Auflösung und 30 Bildern pro Sekunde (`?q=0.5&fps=30`). Das lief im Test auf dem HP 255 G7 flüssig.
- Sam antwortet mit festen Antworten und echtem Spielstand (Haus, Likes, Ziele, Rangliste, Begrüßungen …). Es läuft keine KI auf dem Laptop.
- Pro Person antwortet Sam höchstens alle 30 Sekunden, gleiche Sätze wiederholt er nicht direkt.
- Später mit KI: Ollama installieren, ein Modell laden und in `config.json` `"ki": true` setzen. Auf dem Laptop nicht empfohlen.

## Streaming-Einstellungen für den Laptop
- Ausgabe 720×1280, 30 FPS, Hardware-Encoder (AMD/AMF), nur das Spielfenster aufnehmen.
- Ladekabel dran, Energiemodus „Beste Leistung“, Discord/Spotify/Steam schließen.

## Hinweise
- `tiktok-live-connector` ist inoffiziell. Wenn TikTok etwas ändert, hilft meistens `npm update`.
- Sam ignoriert Beleidigungen und heikle Themen und redet nicht über echte Personen.
- Ab und zu selbst in den Chat schreiben. TikTok mag Lives mit echter Interaktion.
