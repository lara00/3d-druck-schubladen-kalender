"""Baut daten/motivliste.json neu: für jedes Motiv Name (deutsch/englisch), Kategorie, Druckplatte, Platz
und Umriss (für die Vorschaubilder im Konfigurator).
Namen und Kategorien stehen in daten/motiv_namen.json, alles andere kommt aus den Motiv-Skripten.
    python3 -m werkzeuge.motivliste_erzeugen
"""
import json
import os
import pfade
from alles_erzeugen import MOTIVE

def umriss(cs):
    """2D-Form als SVG-Pfad (y nach unten)."""
    return "".join("M" + " L".join(f"{x:.2f} {-y:.2f}" for x, y in p) + "Z" for p in cs.to_polygons())

def main():
    with open(os.path.join(pfade.DATEN, "motiv_namen.json"), encoding="utf-8") as f:
        namen = json.load(f)
    gefunden = {}
    for m in MOTIVE:
        for p in m.PLATTEN:
            for pos, (key, form) in enumerate(p.teile, 1):
                if key and key not in gefunden:
                    gefunden[key] = (p.datei, pos, form)
    liste, fehlt = {}, [k for k in gefunden if k not in namen]
    for key, info in namen.items():                    # Reihenfolge wie in motiv_namen.json
        if key not in gefunden:
            print("  Hinweis: kein Motiv für", key); continue
        datei, pos, form = gefunden[key]
        liste[key] = {**info, "file": datei, "pos": pos, "d": umriss(form())}
    with open(os.path.join(pfade.DATEN, "motivliste.json"), "w", encoding="utf-8") as f:
        json.dump(liste, f, ensure_ascii=False)
    print(f"  Motivliste: {len(liste)} Motive" + (f", ohne Namen (bitte in motiv_namen.json eintragen): {fehlt}" if fehlt else ""))

if __name__ == "__main__":
    main()
