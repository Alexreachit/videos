"""cine – modulare KI-Kinopipeline (POV-Thriller, Zombie-Serie).

Ablauf: Story -> Szenenplan -> Prompts -> Referenzbilder -> Clips -> Sound ->
Schnitt/Grading -> Qualitätskontrolle -> gezielte Neugenerierung -> Export.
Jeder Schritt hat ein eigenes Modul unter cine/stages, jeder Anbieter einen
Provider unter cine/providers. Kostenpflichtige Aufrufe laufen ausschließlich
über cine.cost.CostGuard und brauchen eine ausdrückliche Freigabe.
"""
__version__ = "1.0.0"
