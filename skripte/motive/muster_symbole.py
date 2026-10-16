"""Basis-Schubladen: leer, Muster, Symbole, Jahreszeiten & Feste, Wochentage (deutsch/englisch), Bildsymbole.
Linien ≥ 1,2 mm (0,6-mm-Düse).
"""
import math
from manifold3d import CrossSection, Manifold
from basis import kalender as mk
from basis.grundlagen import text_cs
from basis.zeichnen import W, H, FELD, L, linie, ring, muster_cs
from basis.platten import Platte

def rechteck(x, y, w, h):
    return CrossSection.square([w, h]).translate([x, y])

def streifen_h():
    return sum((rechteck(-W - 1, y, 2 * W + 2, L) for y in [k * 2.8 - H for k in range(6)]), CrossSection())

def streifen_diag():
    s = sum((rechteck(-30, k * 3.0 - 30, 60, L) for k in range(21)), CrossSection())
    return s.rotate(45)

def punkte():
    return sum((CrossSection.circle(1.1, 20).translate([x, y])
                for x in [k * 3.9 - 11.7 for k in range(7)] for y in [k * 4.2 - 4.2 for k in range(3)]), CrossSection())

def wellen():
    w = CrossSection()
    for y0 in (-4.6, 0, 4.6):
        pts = [(x / 10, y0 + 1.3 * math.sin(x / 10 * 1.1)) for x in range(-150, 151, 5)]
        lin = [(x, y + L / 2) for x, y in pts] + [(x, y - L / 2) for x, y in reversed(pts)]
        w += CrossSection([lin[::-1]]) if CrossSection([lin]).area() <= 0 else CrossSection([lin])
    return w

def zickzack():
    z = CrossSection()
    for y0 in (-4.5, 0, 4.5):
        pts = [(-15 + k * 2.5, y0 + (1.2 if k % 2 else -1.2)) for k in range(13)]
        for (x1, y1), (x2, y2) in zip(pts, pts[1:]):
            dx, dy = x2 - x1, y2 - y1
            n = math.hypot(dx, dy)
            ox, oy = -dy / n * L / 2, dx / n * L / 2
            seg = CrossSection([[(x1 - ox, y1 - oy), (x2 - ox, y2 - oy), (x2 + ox, y2 + oy), (x1 + ox, y1 + oy)]])
            z += seg + CrossSection.circle(L / 2, 12).translate([x2, y2])
    return z

def karo():
    return sum((rechteck(-W + i * 3.25, -H + j * 3.5, 3.25, 3.5)
                for i in range(8) for j in range(4) if (i + j) % 2 == 0), CrossSection()).offset(0.15)  # Ecken verbinden

def rauten():
    r = CrossSection([[(0, -2.2), (2.2, 0), (0, 2.2), (-2.2, 0)]])
    return sum((r.translate([x + (2.6 if j % 2 else 0), j * 3.6 - 5.4])
                for x in [k * 5.2 - 15.6 for k in range(8)] for j in range(4)), CrossSection())

def gitter():
    g = sum((rechteck(-W - 1, y - L / 2, 2 * W + 2, L) for y in (-H + 0.65, -2.3, 2.3, H - 0.65)), CrossSection())
    return g + sum((rechteck(x - L / 2, -H - 1, L, 2 * H + 2) for x in (-W + 0.65, -6.5, 0, 6.5, W - 0.65)), CrossSection())

def kreise():
    c = CrossSection()
    for r in (6.6, 3.9, 1.4):
        c += CrossSection.circle(r, 64) - (CrossSection.circle(r - L, 64) if r > L else CrossSection())
    return c.translate([-6.5, 0]) + c.translate([6.5, 0])

def sterne():
    return sum((mk.stern(2.9, 1.3).translate([x, y]) for x, y in
                [(-9.5, 3.3), (0, 3.3), (9.5, 3.3), (-4.75, -3.3), (4.75, -3.3)]), CrossSection())

def waben():
    r = 2.6
    hexa = CrossSection([[(r * math.cos(math.pi / 3 * k), r * math.sin(math.pi / 3 * k)) for k in range(6)]])
    ring = hexa - hexa.offset(-L * 0.9)
    return sum((ring.translate([i * 1.5 * r - 12, j * math.sqrt(3) * r + (i % 2) * math.sqrt(3) * r / 2 - 6.5])
                for i in range(9) for j in range(4)), CrossSection()).offset(0.1)

def rahmen():
    aussen = CrossSection.square([2 * W, 2 * H], center=True)
    innen = aussen.offset(-L)
    eck = sum((CrossSection.circle(1.6, 24).translate([sx * (W - 3.5), sy * (H - 3.5)]) for sx in (1, -1) for sy in (1, -1)),
              CrossSection())
    return (aussen - innen) + eck

MUSTER = [("streifen", streifen_h), ("diagonal", streifen_diag), ("punkte", punkte), ("wellen", wellen),
          ("zickzack", zickzack), ("karo", karo), ("rauten", rauten), ("gitter", gitter),
          ("kreise", kreise), ("sterne", sterne), ("waben", waben), ("rahmen", rahmen)]

# ---- Symbole (selbst gezeichnet, Linien ≥ 1,3 mm) ----------------------------
def ausrufezeichen():
    return mk.text_cs("!", 13)

def fragezeichen():
    return mk.text_cs("?", 13)

def play():
    dreieck = CrossSection([[(-3.6, -6), (6.4, 0), (-3.6, 6)]])
    return dreieck.offset(-0.6).offset(0.6)          # Ecken leicht abrunden

def todo():
    box = CrossSection.square([9, 9], center=True)
    box = (box - box.offset(-1.4)).translate([-7.5, 0])
    haken = linie((-10.3, 0.4), (-8.2, -2.0), 1.5) + linie((-8.2, -2.0), (-3.8, 4.6), 1.5)
    zeilen = linie((-0.5, 2.6), (11, 2.6)) + linie((-0.5, -0.4), (11, -0.4)) + linie((-0.5, -3.4), (7, -3.4))
    return box + haken + zeilen

def kaffeetasse():
    tasse = CrossSection([[(-5, -3.6), (3, -3.6), (4, 4), (-6, 4)]]).offset(0.3)
    henkel = (ring(2.7, 1.4)).translate([4.6, 1.0])
    unterteller = CrossSection.square([15, 1.4]).translate([-8.5, -5.6])
    dampf = CrossSection()
    for x0 in (-3.2, 0.8):
        pts = [(x0 + 0.9 * math.sin(k / 2.5), 4.8 + k * 0.35) for k in range(0, 9)]
        for a, b in zip(pts, pts[1:]):
            dampf += linie(a, b, 1.2)
    return (tasse + henkel + unterteller + dampf).translate([0, -1.4])

def einkaufstasche():
    tasche = CrossSection([[(-5.5, -6), (5.5, -6), (6.3, 3), (-6.3, 3)]])
    henkel = ring(3.2, 1.4).translate([0, 3]) ^ CrossSection.square([10, 5]).translate([-5, 3])
    loecher = CrossSection.circle(0.8, 16).translate([-3.2, 1.2]) + CrossSection.circle(0.8, 16).translate([3.2, 1.2])
    return tasche + henkel - loecher

# ---- Jahreszeiten & Feste ------------------------------------------------------
def fruehling():                      # Tulpe
    bluete = CrossSection([[(4, 0.5), (4.4, 6.2), (2, 4.2), (0, 6.8), (-2, 4.2), (-4.4, 6.2), (-4, 0.5)]])
    bluete += CrossSection.circle(4, 48).translate([0, 0.9]) ^ CrossSection.square([10, 5]).translate([-5, -4])
    stiel = linie((0, -2.8), (0, -6.4), 1.4)
    blatt = CrossSection.circle(1, 32).scale([3.4, 1.3]).rotate(35).translate([2.6, -5.0])
    return bluete + stiel + blatt

def sommer():                         # Sonne
    s = CrossSection.circle(3.6, 48)
    for k in range(8):
        w = k * math.pi / 4
        s += linie((5.2 * math.cos(w), 5.2 * math.sin(w)), (6.6 * math.cos(w), 6.6 * math.sin(w)), 1.4)
    return s

def herbst():                         # Blatt mit Stiel und Mittelrippe
    blatt = CrossSection.circle(1, 64).scale([6.2, 3.6]).rotate(30)
    rippe = linie((-4.6, -2.65), (4.0, 2.3), 0.9)
    seiten = sum((linie((x, x * 0.577), (x - 1.0, x * 0.577 + 2.0), 0.8) + linie((x, x * 0.577), (x + 1.0, x * 0.577 - 2.0), 0.8)
                  for x in (-1.6, 1.0)), CrossSection())
    stiel = linie((-5.0, -2.9), (-7.2, -4.6), 1.3)
    return blatt - rippe - seiten + stiel

def winter():                         # Schneeflocke
    s = CrossSection()
    for k in range(6):
        w = k * math.pi / 3
        c, d = math.cos(w), math.sin(w)
        s += linie((0, 0), (6.5 * c, 6.5 * d), 1.4)
        for a in (1, -1):              # Seitenzweige
            w2 = w + a * math.pi / 4
            p = (3.8 * c, 3.8 * d)
            s += linie(p, (p[0] + 2.2 * math.cos(w2), p[1] + 2.2 * math.sin(w2)), 1.3)
    return s

def geburtstag():                     # Torte mit Kerze
    torte = CrossSection.square([13, 6.2]).translate([-6.5, -6.6])
    schicht = linie((-7, -3.6), (7, -3.6), 0.9)
    guss = sum((CrossSection.circle(1.3, 24).translate([x, -0.5]) for x in (-5.2, -2.6, 0, 2.6, 5.2)), CrossSection())
    kerze = CrossSection.square([1.8, 4]).translate([-0.9, -0.4])
    flamme = CrossSection([[(0, 3.9), (1.2, 4.6), (0, 6.6), (-1.2, 4.6)]]).offset(0.3)
    return torte - schicht + guss + kerze + flamme

def geschenk():                       # Paket mit Schleife
    box = CrossSection.square([12, 8]).translate([-6, -7])
    deckel = CrossSection.square([13.6, 2.6]).translate([-6.8, 1.2 - 0.2])
    band = CrossSection.square([1.4, 11]).translate([-0.7, -7])
    luecke = CrossSection.square([14, 0.7]).translate([-7, 0.7])
    schleife = ring(2.0, 1.2).scale([1.3, 1]).translate([-2.4, 5.4]) + ring(2.0, 1.2).scale([1.3, 1]).translate([2.4, 5.4])
    return ((box + deckel - luecke) + band + schleife).scale([0.9, 0.9])

FESTE = [("fruehling", fruehling), ("sommer", sommer), ("herbst", herbst), ("winter", winter),
         ("geburtstag", geburtstag), ("geschenk", geschenk)]

WOCHENTAGE = ["MO", "DI", "MI", "DO", "FR", "SA", "SO"]

SYMBOLE = [("ausrufezeichen", ausrufezeichen), ("fragezeichen", fragezeichen), ("play", play),
           ("todo", todo), ("kaffeetasse", kaffeetasse), ("einkaufstasche", einkaufstasche),
           ("leer", lambda: CrossSection())]

WOCHENTAGE_EN = ["MO", "TU", "WE", "TH", "FR", "SA", "SU"]

# Bildsymbole: Smiley (selbst gezeichnet) + Zeichen aus DejaVu Sans Bold
BILDSYMBOLE = "S♥★☀❄✈♫✿⚡☘☂⌂"

def smiley(r=6.8):
    gesicht = CrossSection.circle(r, 64)
    augen = CrossSection.circle(1.15, 24).translate([-2.3, 1.9]) + CrossSection.circle(1.15, 24).translate([2.3, 1.9])
    mund = CrossSection.circle(4.4, 64) - CrossSection.circle(2.9, 64)
    unten = CrossSection([[(-5, -6), (5, -6), (5, -0.4), (-5, -0.4)]])
    return gesicht - augen - (mund ^ unten)

def bildsymbol(z):
    return smiley() if z == "S" else text_cs(z, 13)

def _m(f):
    return lambda: muster_cs(f)

LEER = lambda: CrossSection()
E = "4_Extra_Schubladen/"
PLATTEN = [
    Platte(E + "schubladen_leer_12x.stl", [("leer", LEER)] + [(None, LEER)] * 11),
    Platte(E + "schubladen_muster_12x.stl", [("m_" + k, _m(f)) for k, f in MUSTER]),
    Platte(E + "schubladen_symbole_7x.stl", [(None if k == "leer" else "s_" + k, _m(f)) for k, f in SYMBOLE]),
    Platte(E + "schubladen_jahreszeiten_feste_6x.stl", [("j_" + k, _m(f)) for k, f in FESTE]),
    Platte(E + "schubladen_wochentage_7x.stl", [("w_" + w.lower(), lambda w=w: text_cs(w, 11)) for w in WOCHENTAGE]),
    Platte(E + "schubladen_wochentage_en_7x.stl", [("we_" + w.lower(), lambda w=w: text_cs(w, 11)) for w in WOCHENTAGE_EN]),
    Platte(E + "schubladen_bildsymbole_12x.stl", [(f"t_{i}", lambda z=z: bildsymbol(z)) for i, z in enumerate(BILDSYMBOLE)]),
]
