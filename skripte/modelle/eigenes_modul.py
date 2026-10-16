"""Bausteine für „Eigenes Modul“ im Konfigurator: Modul ohne Beschriftung und jeder Buchstabe als 3D-Teil.
Der Konfigurator setzt daraus das Modul mit der selbst eingegebenen Überschrift zusammen (ohne Geometrie-Rechnung):
  ../stl/einzeln/modul_leer.stl, modul_leer_mit_nuten.stl   Modul in Originallage (Front bei z = TIEFE)
  ../stl/einzeln/zeichen_XXXX.stl                           Buchstabe (Unicode hex), Schriftgröße 10, Grundlinie y = 0,
                                                            1,2 mm hoch extrudiert (z = 0 … 1,2)
  daten/schrift.json                                        Vorschub und Umriss je Zeichen + Maße des Moduls
"""
import json
import os
from matplotlib.textpath import TextPath, text_to_path
from manifold3d import CrossSection, FillRule
import pfade
from basis import kalender as mk
from basis import grundlagen as gl
from basis.grundlagen import export

ZEICHEN = "ABCDEFGHIJKLMNOPQRSTUVWXYZÄÖÜ0123456789 -&!?.,:'+/()#"
GROESSE = 10.0                                  # Schriftgröße der Buchstaben-Teile (Großbuchstaben 7,29 hoch)

def _breite(txt):
    return text_to_path.get_text_width_height_descent(txt, gl.SCHRIFT, ismath=False)[0] / gl.SCHRIFT.get_size_in_points() * GROESSE

def erzeugen(ziel):
    ordner = os.path.join(ziel, "einzeln")
    os.makedirs(ordner, exist_ok=True)
    export(mk.basis, os.path.join(ordner, "modul_leer.stl"))
    export(mk.basis - mk.nuten(), os.path.join(ordner, "modul_leer_mit_nuten.stl"))
    schrift = {"modul": {"hf": mk.HF, "kopf": mk.KOPF, "tiefe": mk.TIEFE, "hoehe": mk.SCHRIFT_H,
                         "breite_max": mk.B - 2 * mk.RAND - 16, "cap": 0.729 * GROESSE},
               "zeichen": {}}
    for z in ZEICHEN:
        adv = _breite("A" + z + "A") - _breite("AA") if z == " " else _breite(z)
        eintrag = {"adv": round(adv, 3)}
        if z != " ":
            tp = TextPath((0, 0), z, size=GROESSE, prop=gl.SCHRIFT)
            cs = CrossSection([[tuple(p) for p in q] for q in tp.to_polygons() if len(q) > 2], FillRule.EvenOdd)
            export(cs.extrude(1.2), os.path.join(ordner, f"zeichen_{ord(z):04x}.stl"))
            eintrag["box"] = [round(v, 3) for v in cs.bounds()]
        schrift["zeichen"][z] = eintrag
    with open(os.path.join(pfade.DATEN, "schrift.json"), "w", encoding="utf-8") as f:
        json.dump(schrift, f, ensure_ascii=False)
