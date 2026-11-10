# Arbeitsregeln für dieses Repo

## Sichtprüfung – gilt für ALLE Videos (Anweisung von Alex, 10.11.2026)
Bevor ein Video, Short oder TikTok als fertig gemeldet oder verschickt wird, Bilder SELBST ansehen –
nicht nur Metriken, Logs oder Code auswerten.
1. Kontaktblätter erzeugen (1 Bild/Sekunde, mit Zeitstempel) – z. B. `cine.pov360.review_sheets()` oder
   `ffmpeg -vf "fps=1,scale=200:-1,tile=6x3"`.
2. Jedes Blatt mit dem Read-Tool öffnen und ansehen; bei Auffälligkeiten Einzelbilder in voller Größe.
3. Prüfen: Erkennt man etwas (nicht zu dunkel)? Stimmen Perspektive, Figuren, Hände, Text, Überlagerungen,
   Übergänge, Lesbarkeit auf dem Handy? Passt das Bild zu dem, was gerade gesagt/gezeigt werden soll?
4. Fehler beheben, neu rendern, erneut ansehen. Im Bericht kurz nennen, was angesehen und was korrigiert wurde.
Automatische Scores (z. B. QC 100) ersetzen diese Sichtprüfung nie.

## Zombie-/POV-Videos
Machart nach Alex' Referenz: 360°-Panorama-POV (Fischaugen-Kopfkamera), gezeichneter Cartoon-Look,
Handy-Benachrichtigungen, Untertitel, Abstimmungs-Endkarte. Renderer: `cine/pov360.py`,
Episoden: `episodes/pov_*.yaml`, Panoramen: `episodes/panos/` (gratis via Gemini).
