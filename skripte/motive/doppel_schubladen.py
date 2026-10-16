"""Doppel- und Dreifach-Schubladen: zwei (drei) Motive auf einer Front, für Tage, an denen mehrere
Feier-/Aktionstage zusammenfallen. Welche Paare es gibt, steht in daten/doppel_paare_1…4.json.
"""
import json
import os
from manifold3d import CrossSection, JoinType
from basis.zeichnen import linie
from basis.platten import Platte
from motive import muster_symbole as ms, feiertage_deutschland as fe, islamische_tage as it
from motive import welt_feiertage as wf, laender_feiertage as lf

DATEN = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "daten")

def motiv_register():
    """Schlüssel → Motiv-Funktion für alle Motive, die in Doppel-Schubladen vorkommen können."""
    r = {}
    for k, f, *_ in fe.FEIERTAGE: r["f_" + k] = f
    for k, f in ms.FESTE: r["j_" + k] = f
    for k, f, *_ in it.TAGE: r["i_" + k] = f
    for key, _, liste in wf.GRUPPEN:
        for k, f, *_ in liste: r[f"w_{key}_{k}"] = f
    for k, f, *_ in lf.MOTIVE + lf.MOTIVE_2: r["n_" + k] = f
    return r

HALB_B, HALB_H, MITTE_X = 11.0, 13.4, 7.0      # Platz je Motiv, Mittelpunkt links/rechts

def einpassen(cs):
    x0, y0, x1, y1 = cs.bounds()
    s = min(HALB_B / (x1 - x0), HALB_H / (y1 - y0), 1.0)
    cs = cs.translate([-(x0 + x1) / 2, -(y0 + y1) / 2]).scale([s, s])
    if s < 0.85:                                 # verkleinerte Linien etwas dicker machen (0,6-mm-Düse)
        cs = cs.offset(0.12, JoinType.Miter).simplify(0.02)
    return cs

def kombi_cs(f_links, f_rechts):
    links = einpassen(f_links()).translate([-MITTE_X, 0])
    rechts = einpassen(f_rechts()).translate([MITTE_X, 0])
    trenner = linie((0, -5.0), (0, 5.0), 0.8)
    frei = CrossSection.square([2.6, 16], center=True)        # Abstand rund um den Trennstrich
    return (links + rechts - frei) + trenner

# ---- Dreifach: nutzt die Front fast ganz (30 × 16,5 mm über der Griffleiste) ----
DREI_B, DREI_H, DREI_ABST = 9.2, 16.0, 10.1
MIN_LINIE = 0.85                                   # Ziel-Linienbreite nach dem Verkleinern

def einpassen_box(cs, b, h, linie_orig=1.3):
    x0, y0, x1, y1 = cs.bounds()
    s = min(b / (x1 - x0), h / (y1 - y0), 1.0)
    cs = cs.translate([-(x0 + x1) / 2, -(y0 + y1) / 2]).scale([s, s])
    dick = max(0.0, (MIN_LINIE - linie_orig * s) / 2)
    if dick > 0:
        cs = cs.offset(dick, JoinType.Miter).simplify(0.02)
    return cs

def kombi3_cs(fa, fb, fc):
    teile = CrossSection()
    for f, x in zip((fa, fb, fc), (-DREI_ABST, 0, DREI_ABST)):
        teile += einpassen_box(f(), DREI_B, DREI_H).translate([x, 0])
    frei = CrossSection.square([1.8, 18], center=True)
    for x in (-DREI_ABST / 2, DREI_ABST / 2):
        teile -= frei.translate([x, 0])
        teile += linie((x, -6.0), (x, 6.0), 0.7)
    return teile.translate([0, 1.0])               # Mitte 17,5 mm über Unterkante (Griff bleibt frei)

DREIER = [("f_weihnachten_1", "w_religionen_chanukka", "i_isra_miraj", ["12-25.2027"]),
          ("n_taube", "w_international_tag_des_baumes", "w_aktionstage_pinguin", ["4-25 IT/PT, jedes Jahr"])]

def _paare(n):
    with open(os.path.join(DATEN, f"doppel_paare_{n}.json"), encoding="utf-8") as f:
        return json.load(f)

_reg = motiv_register()
E = "4_Extra_Schubladen/"
PLATTEN = []
for _n, _name in [(1, "doppel_schubladen_{}x.stl"), (2, "doppel_schubladen_2_{}x.stl"), (3, "doppel_schubladen_3_{}x.stl"),
                   (4, "doppel_schubladen_4_{}x.stl")]:
    _p = _paare(_n)
    PLATTEN.append(Platte(E + _name.format(len(_p)),
                          [(f"k_{a}__{b}", lambda a=a, b=b: kombi_cs(_reg[a], _reg[b])) for a, b, _ in _p]))
PLATTEN.append(Platte(E + f"dreifach_schubladen_{len(DREIER)}x.stl",
                      [(f"k3_{a}__{b}__{c}", lambda a=a, b=b, c=c: kombi3_cs(_reg[a], _reg[b], _reg[c])) for a, b, c, _ in DREIER]))
