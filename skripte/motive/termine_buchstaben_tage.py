"""Termine (Arzt, Prüfung …), Buchstaben groß/klein mit Umlauten und Zahlen 1–366 (Tag im Jahr).
"""
import math
from matplotlib.textpath import TextPath
from manifold3d import CrossSection, FillRule, Manifold
from basis import grundlagen as gl
from basis.zeichnen import linie, ring, poly, tropfen, muster_cs
from basis.platten import Platte

SCHRIFTGROESSE = 12.3          # → Großbuchstaben ca. 9 mm hoch

def buchstabe_cs(z):
    tp = TextPath((0, 0), z, size=SCHRIFTGROESSE, prop=gl.SCHRIFT)
    polys = [p for p in tp.to_polygons() if len(p) > 2]
    cs = CrossSection([[tuple(pt) for pt in p] for p in polys], FillRule.EvenOdd)
    x0, _, x1, _ = cs.bounds()
    # waagerecht zentrieren, senkrecht: Mitte der Großbuchstaben-Höhe auf +1 mm
    return cs.translate([-(x0 + x1) / 2, -0.365 * SCHRIFTGROESSE + 1.0])

GROSS = list("ABCDEFGHIJKLMNOPQRSTUVWXYZÄÖÜ")
KLEIN = list("abcdefghijklmnopqrstuvwxyzäöüß")

# ---- Termin-Symbole ------------------------------------------------------------
def pruefung():                      # Blatt mit Stift
    blatt = CrossSection.square([9, 13]).translate([-7, -6.5])
    zeilen = sum((linie((-5.6, y), (-0.6, y), 0.9) for y in (3.6, 1.0, -1.6, -4.2)), CrossSection())
    stift = linie((0.6, -4.2), (6.6, 4.6), 2.2)
    spitze = poly([(-0.4, -5.6), (1.6, -4.4), (-0.0, -3.4)])
    stift_ges = stift + spitze
    return ((blatt - zeilen - stift_ges.offset(1.0)) + stift_ges).offset(0.02).offset(-0.02)

def arzt():                          # Kreuz im Kreis
    return ring(6.8, 1.3) + CrossSection.square([3.0, 8.4]).translate([-1.5, -4.2]) + CrossSection.square([8.4, 3.0]).translate([-4.2, -1.5])

def zahnarzt():                      # Zahn
    krone = CrossSection.batch_hull([CrossSection.circle(3.3, 40).translate([-2.4, 3.0]), CrossSection.circle(3.3, 40).translate([2.4, 3.0])])
    wurzel = poly([(-5.6, 2.0), (5.6, 2.0), (4.4, -6.6), (2.4, -6.6), (1.0, -2.2), (-1.0, -2.2), (-2.4, -6.6), (-4.4, -6.6)])
    return krone + wurzel - CrossSection.circle(1.3, 24).translate([0, 6.6])

def termin():                        # Uhr
    return ring(6.6, 1.4) + linie((0, 0), (0, 4.0), 1.4) + linie((0, 0), (3.0, -1.8), 1.4) + CrossSection.circle(1.2, 20)

def friseur():                       # Schere
    s = ring(2.3, 1.2).translate([-3.2, -4.4]) + ring(2.3, 1.2).translate([3.2, -4.4])
    s += linie((-1.8, -2.6), (3.5, 5.8), 1.6) + linie((1.8, -2.6), (-3.5, 5.8), 1.6)
    return s

def sport():                         # Hantel
    h = linie((-6, 0), (6, 0), 1.8)
    for sx in (1, -1):
        h += CrossSection.square([2.2, 10]).translate([sx * 5.0 - 1.1, -5])
        h += CrossSection.square([1.8, 6.4]).translate([sx * 7.6 - 0.9, -3.2])
    return h

def urlaub():                        # Koffer
    koffer = CrossSection.square([13, 8.4], center=True).offset(-1).offset(1).translate([0, -2.4])
    griff = ring(2.6, 1.3).translate([0, 1.8]) ^ CrossSection.square([8, 5]).translate([-4, 1.8])
    gurte = linie((-3.4, -6.0), (-3.4, 1.2), 0.9) + linie((3.4, -6.0), (3.4, 1.2), 0.9)
    return koffer - gurte + griff

def party():                         # Luftballon
    ballon = CrossSection.circle(1, 48).scale([4.4, 5.0]).translate([0, 2.0])
    knoten = poly([(-1.1, -3.6), (1.1, -3.6), (0, -2.6)])
    schnur = CrossSection()
    pts = [(0.7 * math.sin(k / 1.6), -3.6 - k * 0.38) for k in range(9)]
    for a, b in zip(pts, pts[1:]):
        schnur += linie(a, b, 1.1)
    glanz = CrossSection.circle(1, 24).scale([0.9, 1.6]).rotate(-25).translate([-1.8, 3.6])
    return (ballon - glanz + knoten + schnur).scale([0.92, 0.92])

def muell():                         # Mülltonne
    tonne = poly([(-4.4, 3.8), (4.4, 3.8), (3.6, -6.6), (-3.6, -6.6)])
    deckel = CrossSection.square([11, 1.6]).translate([-5.5, 4.4])
    griff = CrossSection.square([3.4, 1.2]).translate([-1.7, 6.0])
    rillen = sum((linie((x, -4.8), (x, 2.2), 0.9) for x in (-1.8, 0, 1.8)), CrossSection())
    return (tonne - rillen + deckel + griff).scale([0.92, 0.92])

def rechnung():                      # Euro
    return gl.text_cs("€", 12)

def werkstatt():                     # Schraubenschlüssel
    griff = linie((-5.4, -5.4), (2.0, 2.0), 2.4)
    kopf = CrossSection.circle(3.6, 40).translate([3.4, 3.4])
    maul = CrossSection.square([2.6, 5.0]).translate([-1.3, 0]).rotate(-45).translate([3.4, 3.4])
    return griff + kopf - maul

def tierarzt():                      # Pfote
    p = CrossSection.circle(1, 40).scale([3.8, 3.0]).translate([0, -3.0])
    for x, y in [(-4.4, 1.2), (-1.6, 3.8), (1.6, 3.8), (4.4, 1.2)]:
        p += CrossSection.circle(1, 24).scale([1.5, 1.9]).translate([x, y])
    return p

TERMINE = [("pruefung", pruefung, "Prüfung"), ("arzt", arzt, "Arztbesuch"), ("zahnarzt", zahnarzt, "Zahnarzt"),
           ("termin", termin, "Termin / Uhrzeit"), ("friseur", friseur, "Friseur"), ("sport", sport, "Sport"),
           ("urlaub", urlaub, "Urlaub"), ("party", party, "Party"), ("muell", muell, "Müllabfuhr"),
           ("rechnung", rechnung, "Rechnung / Bezahlen"), ("werkstatt", werkstatt, "Werkstatt"), ("tierarzt", tierarzt, "Tierarzt")]

def zahl_cs(n):
    return gl.text_cs(str(n), 11 if n < 100 else 10)

def _m(f):
    return lambda: muster_cs(f)

E = "4_Extra_Schubladen/"
_tage = list(range(1, 367))
PLATTEN = [Platte(E + f"tage_im_jahr/tage_{p // 36 + 1:02d}_{_tage[p]:03d}-{_tage[min(p + 35, 365)]:03d}.stl",
                  [(None, lambda n=n: zahl_cs(n)) for n in _tage[p:p + 36]], 8) for p in range(0, 366, 36)]   # 36 pro Datei, 8 × 5 auf dem Bett
PLATTEN += [Platte(E + "buchstaben_gross_29x.stl", [(f"bg_{i}", lambda z=z: buchstabe_cs(z)) for i, z in enumerate(GROSS)]),
            Platte(E + "buchstaben_klein_30x.stl", [(f"bk_{i}", lambda z=z: buchstabe_cs(z)) for i, z in enumerate(KLEIN)]),
            Platte(E + "schubladen_termine_12x.stl", [("x_" + k, _m(f)) for k, f, _ in TERMINE])]
