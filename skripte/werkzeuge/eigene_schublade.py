"""Eigene Schubladen mit beliebigen Zeichen erzeugen – Own drawers with any text or symbol.

    python3 -m werkzeuge.eigene_schublade "Oma" "♥" "A" "42"
    python3 -m werkzeuge.eigene_schublade "Oma" "Oma" "Opa" -o geburtstage.stl

Bis zu 4 Zeichen pro Schublade (Buchstaben, Ziffern, Symbole aus der Schrift DejaVu Sans Bold).
Gleiche Maße und Rastung wie alle anderen Schubladen. Max. 30 Schubladen pro Platte, sonst mehrere Dateien.
Up to 4 characters per drawer; same size and detent as all other drawers; max. 30 per plate.
"""
import argparse
from manifold3d import CrossSection
from basis import kalender as mk
from basis.grundlagen import text_cs

FELD_B, FELD_H = 26.0, 11.0        # Platz auf der Front (mm) / space on the drawer front

def zeichen_cs(txt):
    cs = text_cs(txt, FELD_H)                      # zentriert, Höhe 11 mm
    x0, y0, x1, y1 = cs.bounds()
    if x1 - x0 > FELD_B:                           # zu breit → kleiner / too wide → scale down
        s = FELD_B / (x1 - x0)
        cs = cs.scale([s, s])
    return cs, (y1 - y0) * min(1.0, FELD_B / (x1 - x0))

if __name__ == "__main__":
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("texte", nargs="+", help="ein Text pro Schublade / one text per drawer")
    ap.add_argument("-o", "--ausgabe", default="eigene_schubladen.stl", help="Dateiname / output file")
    a = ap.parse_args()
    teile = []
    for t in a.texte:
        if len(t) > 4:
            print(f"Hinweis: „{t}“ hat mehr als 4 Zeichen – wird sehr klein.")
        cs, h = zeichen_cs(t)
        if cs.is_empty():
            print(f"Übersprungen: „{t}“ (Zeichen nicht in der Schrift)"); continue
        if h < 6:
            print(f"Hinweis: „{t}“ ist nur {h:.1f} mm hoch – für eine 0,6-mm-Düse evtl. zu fein.")
        teile.append(mk.schublade_mit(cs))
    for p in range(0, len(teile), 30):
        name = a.ausgabe if len(teile) <= 30 else a.ausgabe.replace(".stl", f"_{p // 30 + 1}.stl")
        t = mk.export(mk.platte(teile[p:p + 30]), name)
        print(f"{name}: {len(teile[p:p + 30])} Schubladen, dicht={t.is_watertight}")
