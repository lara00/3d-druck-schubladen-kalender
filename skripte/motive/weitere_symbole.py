"""Weitere Symbol-Schubladen: Tiere, Natur & Wetter, Essen & Trinken, Unterwegs, Zuhause, Büro & Schule,
Gesichter (30), Stimmung (5, für einen Stimmungskalender), Stunden (80: 15 min bis 20 h in Viertelstunden, z. B. Lernzeit), Zeichen, Feiern & Erfolg,
Kleidung & Pflege und Studium.
Platz für das Motiv: x −13 … 13, y −7 … 7 mm; Linien ≥ 1,2 mm.
"""
import math
from manifold3d import CrossSection, FillRule
from matplotlib.textpath import TextPath
from basis import grundlagen as gl
from basis.zeichnen import C, E, R, RC, linie, ring, poly, tropfen, stern5, bogen, muster_cs
from basis.platten import Platte
from motive.sport_hobby_alltag import LEER, kette, rrect, passend

def halbkreis(r, x=0, y=0, oben=True):
    return C(r, x, y) ^ RC(2 * r + 1, r + 0.5, x, y + (r + 0.5) / 2 if oben else y - (r + 0.5) / 2)

# ---------------------------------------------------------------- Tiere
def fisch():
    k = E(7.4, 4.6, -1.6, 0) + poly([(4.6, 0), (11.6, 5.0), (11.6, -5.0)])
    k -= C(1.0, -5.4, 1.2) + bogen(4.2, -40, 40, 0.8, -2.4, 0)
    return k

def vogel():
    k = E(6.0, 4.2, -0.4, -1.0) + C(3.0, -5.0, 2.8)
    k += poly([(-7.6, 3.4), (-11.4, 2.2), (-7.6, 1.6)])                           # Schnabel
    k += poly([(4.6, 0.6), (11.4, 3.6), (10.4, -1.0), (4.6, -2.6)])               # Schwanz
    k -= C(0.8, -5.6, 3.2) + bogen(3.6, 200, 320, 0.8, 0.8, 1.2)                  # Auge, Flügel
    return k + linie((-1.4, -5.0), (-2.2, -6.8), 1.2) + linie((1.4, -5.0), (1.0, -6.8), 1.2)

def schmetterling():
    s = E(4.4, 3.4, -4.6, 2.6, 25) + E(4.4, 3.4, 4.6, 2.6, -25) + E(3.4, 2.4, -3.8, -3.4, -25) + E(3.4, 2.4, 3.8, -3.4, 25)
    s -= C(1.3, -5.0, 3.0) + C(1.3, 5.0, 3.0)
    s += E(1.0, 5.6, 0, -0.4)
    return s + kette([(0, 4.6), (-1.6, 6.8)], 1.2) + kette([(0, 4.6), (1.6, 6.8)], 1.2)

def schnecke():
    haus = C(5.2, 1.4, 0.4)
    for r in (3.7, 1.4): haus -= ring(r + 0.2, 0.9).translate([1.4, 0.4])
    koerper = poly([(-11.4, -5.6), (9.0, -5.6), (9.0, -4.0), (-8.4, -4.0), (-10.4, -1.0), (-12.2, -1.4)])
    fuehler = linie((-10.6, -1.6), (-11.4, 3.2), 1.2) + linie((-9.6, -2.0), (-8.4, 2.8), 1.2)
    return haus + koerper + fuehler + C(0.9, -11.4, 3.4) + C(0.9, -8.4, 3.0)

def hase():
    kopf = C(4.4, 0, -2.6)
    ohren = E(2.0, 4.4, -2.1, 2.8, 10) + E(2.0, 4.4, 2.1, 2.8, -10)
    ohren -= E(0.6, 2.6, -2.2, 3.4, 10) + E(0.6, 2.6, 2.2, 3.4, -10)
    return kopf + ohren - C(0.8, -1.8, -1.8) - C(0.8, 1.8, -1.8) - E(1.0, 0.7, 0, -4.0)

def maus():
    k = poly([(-8.0, -4.6), (6.4, -4.6), (4.0, 1.4), (-1.0, 3.2), (-5.0, 2.0)]) + E(7.2, 4.2, -1.4, -0.6)
    k += C(2.6, 2.0, 3.6) - C(1.2, 2.0, 3.6)
    k -= C(0.8, 4.2, -0.6)
    schwanz = kette([(-8.4, -3.6), (-10.6, -1.8), (-11.4, 0.6), (-10.4, 2.6)], 1.2)
    return k + C(1.0, 7.0, -2.6) + schwanz

def eule():
    k = E(5.4, 6.6, 0, -0.2) + poly([(-5.2, 3.0), (-4.6, 7.0), (-1.6, 4.4), (1.6, 4.4), (4.6, 7.0), (5.2, 3.0)])
    for x in (-2.3, 2.3): k -= C(2.0, x, 1.6)
    k -= poly([(-0.9, -0.2), (0.9, -0.2), (0, -1.8)])
    k -= bogen(3.2, 220, 320, 0.8, 0, -1.2)
    return k + C(0.9, -2.3, 1.6) + C(0.9, 2.3, 1.6) + linie((-9.0, -6.6), (9.0, -6.6), 1.2)

def marienkaefer():
    k = C(5.8, 0, -1.0) + C(2.8, 0, 4.0)
    k -= RC(0.8, 11.6, 0, -1.6)
    for x, y in [(-2.8, 1.0), (2.8, 1.0), (-3.4, -2.6), (3.4, -2.6), (-1.6, -4.8), (1.6, -4.8)]: k -= C(1.0, x, y)
    beine = LEER
    for y in (1.0, -1.2, -3.4):
        beine += linie((-5.4, y), (-8.0, y + 0.8), 1.2) + linie((5.4, y), (8.0, y + 0.8), 1.2)
    return k + beine + linie((-1.4, 6.2), (-3.2, 7.0), 1.2) + linie((1.4, 6.2), (3.2, 7.0), 1.2)

def biene():
    k = E(5.8, 4.0, -0.6, -1.4)
    for x in (-2.0, 1.2): k -= RC(1.2, 9, x, -1.4)
    k += C(2.4, -6.4, -0.6) + poly([(5.0, -1.4), (7.8, -1.4), (5.0, 0.4)])
    k -= C(0.6, -7.0, 0.0)
    fl = (E(3.0, 2.0, -1.6, 4.4, -20) - E(1.8, 0.8, -1.6, 4.4, -20)) + (E(3.0, 2.0, 2.4, 4.0, 25) - E(1.8, 0.8, 2.4, 4.0, 25))
    return k + fl

def schildkroete():
    panzer = halbkreis(6.4, 0, -3.6)
    panzer -= linie((-3.2, -3.6), (-1.8, 1.6), 0.8) + linie((3.2, -3.6), (1.8, 1.6), 0.8) + linie((-5.4, -0.6), (5.4, -0.6), 0.8)
    kopf = C(2.2, 8.4, -1.6) + RC(3.4, 1.6, 6.4, -3.0)
    beine = RC(2.0, 2.8, -4.0, -5.0) + RC(2.0, 2.8, 4.0, -5.0)
    return panzer + kopf + beine + poly([(-6.4, -3.6), (-9.0, -4.0), (-6.4, -2.4)]) - C(0.6, 9.0, -1.2)

# ---------------------------------------------------------------- Natur & Wetter
def _wolke(s=1.0, x=0, y=0):
    w = C(3.2, -3.2, -1.0) + C(4.4, 0.6, 1.0) + C(3.0, 4.4, -1.2) + RC(11.0, 3.2, 0.4, -2.6)
    return w.scale([s, s]).translate([x, y])

def wolke():
    return _wolke(1.4, 0, 0.6)

def regen():
    s = _wolke(1.0, 0, 2.4)
    for x, y in [(-4.0, -3.4), (0.0, -4.4), (4.0, -3.4)]:
        s += tropfen(x, y - 1.2, 1.1, y + 1.4)
    return s

def mond():
    m = C(6.6, 0, 0) - C(5.8, 3.0, 1.6)
    return m + stern5(2.2, 7.4, -2.6) + stern5(1.5, 9.6, 4.2)

def regenbogen():
    s = LEER
    for r in (9.4, 7.2, 5.0):
        s += (ring(r, 1.4) ^ RC(22, 11, 0, 5.5)).translate([0, -5.0])
    return s + _wolke(0.55, -7.6, -5.0) + _wolke(0.55, 7.6, -5.0)

def berge():
    b = poly([(-12.4, -6.0), (-3.4, 5.4), (1.4, -0.6), (4.8, 3.0), (12.4, -6.0)])
    b -= poly([(-5.2, 3.1), (-3.4, 5.4 - 1.3), (-1.6, 3.1), (-2.6, 2.2), (-3.4, 3.0), (-4.2, 2.2)])
    return b + C(1.8, 9.0, 5.0)

def tanne():
    t = poly([(0, 7.0), (-4.0, 2.4), (-2.2, 2.4), (-6.0, -1.8), (-3.8, -1.8), (-7.4, -5.0),
              (7.4, -5.0), (3.8, -1.8), (6.0, -1.8), (2.2, 2.4), (4.0, 2.4)])
    return t + RC(2.2, 2.4, 0, -6.0)

def pilz():
    hut = halbkreis(7.4, 0, -0.4) + RC(14.8, 1.0, 0, -0.4)
    for x, y in [(-3.6, 2.4), (1.2, 4.0), (4.6, 1.4), (-0.8, 0.8)]: hut -= C(1.0, x, y)
    stiel = poly([(-2.2, -1.2), (2.2, -1.2), (2.8, -6.8), (-2.8, -6.8)])
    return hut + stiel

def blatt():
    b = E(8.4, 4.4) - linie((-8.0, 0), (6.6, 0), 0.9)
    for x in (-4.4, -0.8, 2.8):
        b -= linie((x, 0), (x + 2.4, 2.6), 0.8) + linie((x, 0), (x + 2.4, -2.6), 0.8)
    return (b + linie((-8.0, 0), (-11.8, -1.4), 1.4)).rotate(25).translate([0.6, 0])

def wind():
    s = kette([(-11.4, 3.0), (3.4, 3.0)]) + bogen(2.0, -90, 160, 1.4, 3.4, 5.0)
    s += kette([(-9.4, -0.4), (8.0, -0.4)]) + bogen(2.0, -90, 160, 1.4, 8.0, 1.6)
    s += kette([(-11.4, -3.8), (4.6, -3.8)]) + bogen(2.0, -160, 90, 1.4, 4.6, -5.8)
    return s

def thermometer():
    t = rrect(3.6, 11.4, 1.8, 0, 1.4) + C(3.0, 0, -4.4)
    t -= RC(1.2, 9.0, 0, 2.2) ^ R(2, 4.6, -1, 2.0)
    for y in (6.0, 4.4, 2.8, 1.2):
        t += linie((2.6, y), (4.4, y), 1.2)
    return t

# ---------------------------------------------------------------- Essen & Trinken
def kirschen():
    k = C(3.2, -4.2, -3.4) + C(3.2, 3.6, -2.4)
    k -= C(0.8, -5.2, -2.4) + C(0.8, 2.6, -1.4)
    stiele = kette([(-4.2, -0.4), (-1.6, 3.4), (1.4, 5.8)], 1.2) + kette([(3.6, 0.6), (2.2, 3.6), (1.4, 5.8)], 1.2)
    return k + stiele + E(2.8, 1.2, 4.0, 5.8, 15)

def erdbeere():
    e = poly([(-6.2, 2.6), (6.2, 2.6), (5.2, -1.6), (0.6, -7.0), (-0.6, -7.0), (-5.2, -1.6)]) + C(3.2, -3.0, 2.4) + C(3.2, 3.0, 2.4)
    for x, y in [(-3.0, 1.0), (0, 0.4), (3.0, 1.0), (-1.6, -2.4), (1.6, -2.4), (0, -4.6)]: e -= C(0.6, x, y)
    blatt = poly([(-5.0, 5.0), (-2.0, 4.0), (0, 6.6), (2.0, 4.0), (5.0, 5.0), (2.4, 3.2), (-2.4, 3.2)])
    return e + blatt

def banane():
    b = C(9.0, 0, 3.0, 64) - C(10.0, 0, 8.0, 64)
    return b + linie((-8.6, 3.4), (-10.2, 5.2), 1.5) + C(0.9, 8.6, 3.4)

def karotte():
    k = poly([(-11.4, -0.6), (5.0, -3.0), (6.4, 0.0), (5.0, 3.0)])
    for x in (-3.0, 1.0): k -= linie((x, -1.6), (x + 1.2, 0.2), 0.8)
    gruen = E(3.0, 1.0, 9.0, 2.4, 30) + E(3.2, 1.0, 9.6, 0, 0) + E(3.0, 1.0, 9.0, -2.4, -30)
    return k + gruen

def birne():
    b = C(4.8, 0, -2.0) + C(3.0, 0, 2.6) + poly([(-3.0, 2.6), (3.0, 2.6), (4.6, -1.2), (-4.6, -1.2)])
    return b + linie((0, 5.0), (0.8, 7.0), 1.3) + E(2.2, 1.0, 2.8, 6.0, 20) - E(0.9, 1.6, -2.0, -2.6, 20)

def brot():
    b = rrect(18.0, 6.6, 1.6, 0, -2.4) + E(9.0, 3.6, 0, 0.6)
    for x in (-4.4, 0, 4.4): b -= linie((x - 1.2, -0.4), (x + 1.2, 2.6), 0.9)
    return b

def spiegelei():
    w = E(8.6, 5.4, -0.6, -0.6) + C(4.0, 4.4, 1.4) + C(3.6, -5.2, -2.0)
    return (w - C(3.2, -0.4, 0)) + C(2.2, -0.4, 0)

def burger():
    oben = halbkreis(7.6, 0, 1.4)
    for x, y in [(-3.4, 4.2), (0, 5.4), (3.4, 4.2)]: oben -= E(0.9, 0.5, x, y)
    salat = kette([(-8.4, 0.0), (-6.0, 0.8), (-3.6, -0.2), (-1.2, 0.8), (1.2, -0.2), (3.6, 0.8), (6.0, -0.2), (8.4, 0.6)], 1.3)
    fleisch = rrect(16.4, 2.2, 1.1, 0, -2.4)
    unten = rrect(15.2, 2.6, 1.3, 0, -5.6)
    return oben + salat + fleisch + unten

def weinglas():
    kelch = poly([(-4.6, 6.8), (4.6, 6.8), (4.2, 1.8), (2.0, -0.6), (-2.0, -0.6), (-4.2, 1.8)])
    kelch -= kelch.offset(-1.2) ^ R(12, 6, -6, 3.0)
    return kelch + RC(1.4, 6.0, 0, -3.4) + RC(7.6, 1.4, 0, -6.3)

def teekanne():
    k = E(6.2, 4.6, -0.6, -1.8) + RC(12.0, 1.4, -0.6, -6.0) + RC(6.0, 1.2, -0.6, 3.0) + C(1.2, -0.6, 4.2)
    tuelle = poly([(4.4, -1.0), (5.6, -3.8), (10.6, 2.8), (11.6, 2.6), (10.6, 4.0), (5.0, 0.4)])
    henkel = bogen(2.8, 100, 260, 1.3, -6.8, -1.6)
    return k + tuelle + henkel

# ---------------------------------------------------------------- Unterwegs
def bus():
    k = rrect(23.0, 10.0, 1.8, 0, 0.6)
    for x in (-8.6, -4.0, 0.6): k -= rrect(3.6, 3.4, 0.6, x, 2.6)
    k -= rrect(4.0, 6.2, 0.6, 7.4, 0.8) + RC(23.4, 0.8, 0, -1.8)
    k -= C(2.6, -6.4, -4.6) + C(2.6, 6.4, -4.6)
    return k + C(1.8, -6.4, -4.6) + C(1.8, 6.4, -4.6)

def segelboot():
    rumpf = poly([(-10.0, -2.6), (10.0, -2.6), (7.0, -6.0), (-7.0, -6.0)])
    segel = poly([(-0.4, -1.4), (-0.4, 7.0), (-8.6, -1.4)]) + poly([(0.8, -1.4), (0.8, 6.0), (6.6, -1.4)])
    return rumpf + segel

def lkw():
    lade = rrect(14.0, 9.6, 0.8, -4.6, 1.2)
    kabine = poly([(3.4, -3.0), (3.4, 4.0), (8.6, 4.0), (11.6, 0.6), (11.6, -3.0)])
    kabine -= poly([(5.0, 2.6), (8.0, 2.6), (10.0, 0.6), (5.0, 0.6)])
    k = lade + kabine + RC(24, 1.2, 0, -3.4)
    k -= C(2.6, -7.6, -4.4) + C(2.6, 7.2, -4.4)
    return k + C(1.8, -7.6, -4.4) + C(1.8, 7.2, -4.4)

def ampel():
    a = rrect(7.4, 14.0, 1.8)
    for y in (4.2, 0, -4.2): a -= ring(1.7, 0.8).translate([0, y])
    a -= C(1.0, 0, 4.2)
    return a + linie((-5.4, 4.2), (-3.6, 4.2), 1.2) + linie((3.6, 4.2), (5.4, 4.2), 1.2)

def anker():
    a = ring(1.8, 1.3).translate([0, 5.0]) + RC(1.6, 10.6, 0, -0.6) + RC(7.0, 1.4, 0, 2.2)
    a += bogen(6.0, 200, 340, 1.6, 0, -0.4)
    a += poly([(-7.4, -1.4), (-5.0, -3.4), (-7.0, -4.2)]) + poly([(7.4, -1.4), (5.0, -3.4), (7.0, -4.2)])
    return a

def kompass():
    k = ring(6.8, 1.3)
    nadel = poly([(0, 5.0), (1.6, 0), (0, -5.0), (-1.6, 0)]).rotate(-30)
    k += nadel - C(0.6)
    for w in (0, 90, 180, 270):
        k += RC(1.2, 1.4, 4.6 * math.cos(math.radians(w)), 4.6 * math.sin(math.radians(w)), w)
    return k

def ortsmarker():
    m = CrossSection.batch_hull([C(5.0, 0, 2.0), RC(0.2, 0.2, 0, -7.0)])
    return m - C(2.2, 0, 2.0)

def tankstelle():
    s = rrect(9.0, 13.6, 1.0, -3.0, 0) - rrect(5.6, 3.8, 0.6, -3.0, 3.2)
    s += RC(12.0, 1.4, -3.0, -6.3)
    schlauch = kette([(1.4, 2.2), (3.6, 2.2), (4.4, 0.6), (4.4, -3.4), (6.0, -3.4), (6.6, -2.0), (6.6, 3.6), (5.0, 5.6)], 1.2)
    return s + schlauch

def fahrkarte():
    t = rrect(22.0, 11.0, 1.2)
    t -= C(1.6, -11.0, 0) + C(1.6, 11.0, 0)
    for y in (2.6, -0.2): t -= RC(9.0, 1.0, -2.6, y)
    for y in (3.6, 1.2, -1.2, -3.6): t -= RC(0.8, 1.2, 5.6, y)
    return t - RC(5.0, 1.0, -4.6, -3.0)

def heissluftballon():
    b = C(5.6, 0, 2.0) + poly([(-5.2, 0.0), (5.2, 0.0), (1.8, -3.6), (-1.8, -3.6)])
    b -= E(1.8, 5.6, 0, 2.0) - E(0.7, 5.6, 0, 2.0)
    korb = rrect(3.8, 2.6, 0.5, 0, -6.0)
    seile = linie((-1.8, -3.6), (-1.4, -4.8), 1.2) + linie((1.8, -3.6), (1.4, -4.8), 1.2)
    return b + korb + seile + _wolke(0.45, -9.4, -3.6) + _wolke(0.4, 9.4, 4.4)

# ---------------------------------------------------------------- Zuhause
def schluessel():
    s = C(4.2, -7.2, 0) - C(2.0, -7.2, 0)
    s += RC(14.0, 2.0, 2.8, 0)
    s += RC(1.6, 3.2, 6.8, -2.2) + RC(1.6, 2.4, 9.6, -1.8) + RC(1.4, 3.2, 3.8, -2.2)
    return s

def gluehbirne():
    g = C(5.0, 0, 1.8) + poly([(-3.6, -1.6), (3.6, -1.6), (2.2, -3.6), (-2.2, -3.6)])
    g -= C(3.6, 0, 1.8) - RC(1.2, 3.2, -0.9, -0.2) - RC(1.2, 3.2, 0.9, -0.2)
    g += RC(4.4, 1.2, 0, -4.4) + RC(4.4, 1.2, 0, -6.0)
    for w in (20, 160, 50, 130):
        c, s_ = math.cos(math.radians(w)), math.sin(math.radians(w))
        g += linie((6.4 * c, 1.8 + 6.4 * s_), (7.8 * c, 1.8 + 7.8 * s_), 1.3)
    return g

def kerze():
    k = RC(5.2, 9.4, 0, -2.2) + RC(9.0, 1.4, 0, -6.4)
    flamme = tropfen(0, 3.8, 1.5, 7.4) - tropfen(0, 3.6, 0.6, 5.2)
    return k + flamme + RC(1.2, 3.6, 0, 2.6) - RC(1.6, 1.0, 0, 2.6) + RC(0.8, 1.2, 0, 2.6)

def bett():
    b = RC(23.0, 3.6, 0, -2.4) + RC(1.6, 12.6, -10.8, -0.3) + RC(1.6, 7.4, 10.8, -2.9)
    b += rrect(5.0, 3.0, 1.2, -6.6, 1.2) + rrect(14.0, 2.4, 1.0, 2.6, 1.2)
    return b

def wecker():
    w = ring(5.6, 1.4).translate([0, -0.8]) + C(0.9, 0, -0.8)
    w += linie((0, -0.8), (0, 2.6), 1.2) + linie((0, -0.8), (2.4, -2.0), 1.2)
    w += (C(2.4) ^ RC(5, 2.6, 0, 1.3)).rotate(35).translate([-4.6, 4.4]) + (C(2.4) ^ RC(5, 2.6, 0, 1.3)).rotate(-35).translate([4.6, 4.4])
    w += linie((-3.2, -5.4), (-4.6, -7.0), 1.3) + linie((3.2, -5.4), (4.6, -7.0), 1.3)
    return w

def fernseher():
    f = rrect(19.0, 12.0, 1.6, 0, -0.6) - rrect(15.6, 8.6, 0.8, 0, -0.6)
    f += linie((-2.8, 5.4), (-5.0, 7.0), 1.2) + linie((2.8, 5.4), (5.0, 7.0), 1.2)
    return f + poly([(-1.2, -2.8), (-1.2, 1.6), (2.4, -0.6)])

def buegeleisen():
    b = poly([(-10.0, -4.4), (9.6, -4.4), (9.6, -2.4), (6.6, 2.6), (-6.4, 2.6), (-10.0, -2.0)])
    b -= poly([(-3.6, 1.4), (5.4, 1.4), (7.2, -1.4), (-3.6, -1.4)])
    griff = rrect(12.0, 1.6, 0.8, -0.4, 5.4) + RC(1.4, 3.0, -5.6, 4.0)
    return b + griff - C(0.6, -6.0, -1.0) - C(0.6, -3.4, -2.8)

def sofa():
    s = rrect(17.0, 7.0, 1.6, 0, 1.8) + rrect(4.0, 8.4, 1.6, -9.6, -0.6) + rrect(4.0, 8.4, 1.6, 9.6, -0.6)
    s += RC(17.0, 3.6, 0, -2.4)
    s -= RC(17.0, 0.8, 0, -0.4) + RC(0.8, 3.2, 0, -2.6)
    return s + RC(1.4, 2.2, -9.6, -5.8) + RC(1.4, 2.2, 9.6, -5.8)

def kuehlschrank():
    k = rrect(10.4, 14.0, 1.4) - RC(11, 0.9, 0, 2.2)
    return k - RC(1.0, 2.4, -3.2, 4.4) - RC(1.0, 3.6, -3.2, -0.6)

def hammer():
    stiel = rrect(2.4, 10.6, 1.0, 0, -0.6)
    kopf = rrect(4.4, 5.0, 0.6, -5.2, 5.0) + RC(5.6, 2.8, -1.0, 5.0)
    kopf += poly([(1.6, 3.6), (1.6, 6.4), (9.0, 5.4), (5.0, 5.0), (9.0, 3.2)])
    return (stiel + kopf).rotate(-30).translate([0.4, -0.6])

# ---------------------------------------------------------------- Büro & Schule
def bleistift():
    b = poly([(-8.4, -1.8), (6.0, -1.8), (6.0, 1.8), (-8.4, 1.8), (-12.0, 0)])
    b -= poly([(-12.4, -0.8), (-10.6, -0.8), (-10.6, 0.8), (-12.4, 0.8)]) - poly([(-12.0, 0), (-10.4, -0.9), (-10.4, 0.9)])
    b -= RC(14.0, 0.8, -1.2, 0) ^ R(14, 1, -8.4, -0.5)
    b -= RC(0.8, 4.0, -8.4, 0)
    return (b + rrect(4.0, 3.6, 1.2, 8.4, 0) - RC(0.8, 4, 6.8, 0)).rotate(20)

def brief():
    b = rrect(20.0, 13.0, 1.0) - rrect(17.4, 10.4, 0.4)
    b += kette([(-9.0, 5.4), (0, -1.4), (9.0, 5.4)], 1.3)
    return b

def kalenderblatt():
    k = rrect(16.0, 13.4, 1.4, 0, -0.6) - RC(13.6, 7.4, 0, -2.4)
    for x in (-4.4, 0, 4.4):
        for y in (-0.8, -4.0):
            k += RC(2.2, 2.0, x, y)
    k += RC(1.4, 3.2, -4.4, 6.0) + RC(1.4, 3.2, 4.4, 6.0)
    return k

def laptop():
    l = rrect(16.4, 10.4, 1.0, 0, 1.6) - RC(13.6, 7.6, 0, 1.8)
    l += poly([(-11.6, -4.6), (11.6, -4.6), (10.2, -6.4), (-10.2, -6.4)])
    return l + RC(17.2, 1.0, 0, -3.8)

def bueroklammer():
    k = linie((-8.0, -3.0), (8.6, -3.0), 1.3) + bogen(3.0, -90, 90, 1.3, 8.6, 0.0)
    k += linie((8.6, 3.0), (-9.4, 3.0), 1.3) + bogen(2.2, 90, 270, 1.3, -9.4, 0.8)
    k += linie((-9.4, -1.4), (6.4, -1.4), 1.3)
    return k.rotate(15)

def lupe():
    l = ring(5.0, 1.6).translate([-2.6, 1.8])
    return l + linie((1.4, -2.2), (7.4, -6.4), 2.4)

def taschenrechner():
    t = rrect(11.4, 14.0, 1.4) - rrect(8.6, 3.0, 0.4, 0, 3.8)
    for x in (-2.8, 0, 2.8):
        for y in (0.4, -2.2, -4.8):
            t -= rrect(1.6, 1.4, 0.3, x, y)
    return t

def ordner():
    o = poly([(-10.4, -6.2), (-10.4, 5.6), (-3.6, 5.6), (-2.0, 3.8), (10.4, 3.8), (10.4, -6.2)])
    o -= RC(19.0, 0.9, 0, 2.2)
    return o

def schultuete():
    t = poly([(-6.0, 4.0), (6.0, 4.0), (0.4, -7.0), (-0.4, -7.0)])
    t -= linie((-6.0, 1.0), (4.6, 1.0), 0.8) ^ poly([(-6.0, 4.0), (6.0, 4.0), (0.4, -7.0), (-0.4, -7.0)])
    t -= poly([(-4.2, -1.6), (3.0, -1.6), (2.6, -2.4), (-3.8, -2.4)])
    tuch = poly([(-5.2, 4.0), (5.2, 4.0), (2.0, 6.0), (0, 5.4), (-2.0, 6.0)])
    return t + tuch + stern5(1.6, -9.0, 2.0) + stern5(1.3, 9.0, -2.0)

def glocke():
    g = poly([(-6.0, -3.4), (6.0, -3.4), (4.6, -1.6), (4.0, 3.0), (2.0, 5.0), (-2.0, 5.0), (-4.0, 3.0), (-4.6, -1.6)])
    g += C(1.4, 0, 5.6) + C(1.6, 0, -4.8)
    return g + bogen(8.6, 155, 180, 1.2, 1.4, -0.2) + bogen(8.6, 0, 25, 1.2, -1.4, -0.2)

# ---------------------------------------------------------------- Gesichter
def _kopf():
    return C(7.0)

def _augen(r=0.9, y=2.0, dx=2.6):
    return C(r, -dx, y) + C(r, dx, y)

def lachen():
    return _kopf() - _augen() - (halbkreis(3.8, 0, -1.0, oben=False))

def traurig():
    return _kopf() - _augen() - bogen(3.2, 30, 150, 1.2, 0, -5.4)

def zwinkern():
    return _kopf() - C(0.9, -2.6, 2.0) - bogen(1.2, 20, 160, 0.9, 2.6, 1.4) - bogen(3.6, 210, 330, 1.2, 0, 0.8)

def ueberrascht():
    return _kopf() - _augen(1.1, 2.4) - E(1.6, 2.0, 0, -2.8) - bogen(1.4, 30, 150, 0.8, -2.6, 4.6) - bogen(1.4, 30, 150, 0.8, 2.6, 4.6)

def _herz(s, x, y):
    return (C(1, -0.75, 0.4) + C(1, 0.75, 0.4) + poly([(-1.7, 0.1), (1.7, 0.1), (0, -1.9)])).scale([s, s]).translate([x, y])

def verliebt():
    k = _kopf() - _herz(1.0, -2.8, 2.0) - _herz(1.0, 2.8, 2.0) - bogen(3.6, 210, 330, 1.2, 0, 0.4)
    return k

def muede():
    k = C(5.6, -3.2, -1.2) - bogen(1.4, 200, 340, 0.8, -5.2, -0.2) - bogen(1.4, 200, 340, 0.8, -1.2, -0.2) - E(1.0, 0.8, -3.2, -4.0)
    z = kette([(3.4, 1.8), (6.0, 1.8), (3.4, -1.2), (6.0, -1.2)], 1.2) + kette([(7.4, 6.4), (11.6, 6.4), (7.4, 1.8), (11.6, 1.8)], 1.3)
    return k + z

def cool():
    k = _kopf() - bogen(3.4, 220, 320, 1.2, 0, -0.6)
    brille = k ^ (rrect(4.6, 2.8, 1.0, -2.6, 2.0) + rrect(4.6, 2.8, 1.0, 2.6, 2.0) + RC(14, 1.0, 0, 2.8))
    k -= rrect(5.8, 4.0, 1.4, -2.6, 2.0) + rrect(5.8, 4.0, 1.4, 2.6, 2.0) + RC(14, 2.2, 0, 2.8)
    return k + brille

def wuetend():
    k = _kopf() - _augen(0.9, 1.4) - bogen(3.2, 30, 150, 1.2, 0, -5.4)
    return k - linie((-4.2, 3.8), (-1.4, 2.8), 0.9) - linie((4.2, 3.8), (1.4, 2.8), 0.9)

def neutral():
    return _kopf() - _augen() - RC(5.6, 1.2, 0, -2.8)

def kuss():
    k = _kopf() - C(0.9, -2.6, 2.0) - bogen(1.2, 200, 340, 0.9, 2.6, 2.6)
    k -= bogen(0.9, -90, 90, 0.8, 0.4, -2.0) + bogen(0.9, -90, 90, 0.8, 0.4, -3.6)
    return k + _herz(1.4, 9.6, 3.4)

def _zu_auge(x, y=2.0, oben=True):
    """geschlossenes Auge als Bogen: oben=True → ∩ (fröhlich), sonst ∪ (entspannt)"""
    return bogen(1.4, 20, 160, 0.9, x, y - 0.6) if oben else bogen(1.4, 200, 340, 0.9, x, y + 0.6)

def traenenlachen():
    k = _kopf() - _zu_auge(-2.6, 2.4) - _zu_auge(2.6, 2.4) - halbkreis(3.8, 0, -0.8, oben=False)
    return k + tropfen(-9.0, -0.4, 1.3, 2.6) + tropfen(9.0, -0.4, 1.3, 2.6)

def grinsen():
    k = _kopf() - _augen(0.9, 2.4) - rrect(9.0, 3.6, 1.4, 0, -2.8)
    for x in (-2.2, 0, 2.2): k += RC(0.9, 3.6, x, -2.8)
    return k

def schuechtern():
    k = _kopf() - _zu_auge(-2.6) - _zu_auge(2.6) - bogen(1.6, 220, 320, 1.0, 0, -2.4)
    for x in (-4.4, 4.4):
        for dx in (-0.9, 0.9): k -= linie((x + dx - 0.4, -1.4), (x + dx + 0.4, 0.0), 0.7)
    return k

def nachdenklich():
    k = (_kopf() - C(0.9, -2.0, 2.6) - C(0.9, 2.2, 2.6) - linie((-2.0, -3.4), (2.4, -2.6), 1.1)).translate([-3.4, 0])
    return k + C(0.8, 5.0, 3.8) + C(1.2, 7.2, 5.0) + C(1.8, 10.4, 5.0)

def verwirrt():
    k = _kopf() - C(0.8, -2.6, 2.0) - (C(1.6, 2.6, 2.2) - C(0.7, 2.6, 2.2))
    return k - kette([(-3.6, -3.2), (-1.8, -2.4), (0, -3.2), (1.8, -2.4), (3.6, -3.2)], 0.9)

def gelangweilt():
    k = _kopf()
    for x in (-2.6, 2.6): k -= halbkreis(1.3, x, 2.0, oben=False) + RC(3.4, 0.8, x, 2.4)
    return k - RC(4.4, 1.1, 1.0, -3.0)

def gestresst():
    k = _kopf() - _augen() - kette([(-3.6, -3.0), (-1.8, -2.2), (0, -3.0), (1.8, -2.2), (3.6, -3.0)], 0.9)
    k -= linie((-4.2, 4.6), (-1.6, 3.6), 0.8) + linie((4.2, 4.6), (1.6, 3.6), 0.8)
    return k + tropfen(9.0, 2.2, 1.4, 5.6)

def krank():
    k = _kopf() - halbkreis(1.1, -2.6, 1.8, oben=False) - halbkreis(1.1, 2.6, 1.8, oben=False) - C(1.0, 1.4, -3.0)
    return k + linie((1.6, -3.2), (9.4, -5.6), 1.4) + C(1.3, 10.0, -5.8)

def weinen():
    k = _kopf() - _augen(0.9, 2.4) - bogen(2.8, 30, 150, 1.1, 0, -5.4)
    return k - tropfen(-2.6, -0.8, 0.9, 1.4) - tropfen(2.6, -0.8, 0.9, 1.4)

def schockiert():
    k = _kopf() - C(1.7, -2.6, 2.2) - C(1.7, 2.6, 2.2) - E(2.0, 2.4, 0, -3.2)
    k += C(0.7, -2.6, 2.2) + C(0.7, 2.6, 2.2)
    return k + linie((-11.6, 4.6), (-9.6, 3.0), 1.2) + linie((11.6, 4.6), (9.6, 3.0), 1.2) + linie((-11.6, 0), (-9.4, 0), 1.2) + linie((11.6, 0), (9.4, 0), 1.2)

def strahlend():
    return _kopf() - _zu_auge(-2.6, 2.4) - _zu_auge(2.6, 2.4) - halbkreis(4.0, 0, -0.6, oben=False)

def zunge():
    k = _kopf() - C(0.9, -2.6, 2.2) - bogen(1.2, 200, 340, 0.9, 2.6, 2.8)
    mund = halbkreis(3.6, 0, -1.2, oben=False)
    return k - mund + (E(1.5, 2.0, 1.2, -4.0) ^ mund.offset(-0.8))

def zufrieden():
    return _kopf() - _zu_auge(-2.6, 2.4, oben=False) - _zu_auge(2.6, 2.4, oben=False) - bogen(3.0, 210, 330, 1.1, 0, -0.6)

def sternaugen():
    return _kopf() - stern5(2.0, -2.6, 2.2) - stern5(2.0, 2.6, 2.2) - halbkreis(3.4, 0, -1.4, oben=False)

def augenrollen():
    k = _kopf() - C(1.6, -2.6, 2.2) - C(1.6, 2.6, 2.2) + C(0.7, -2.6, 3.0) + C(0.7, 2.6, 3.0)
    return k - linie((-2.4, -3.4), (2.6, -3.4), 1.1)

def fertig():                             # k. o.
    k = _kopf()
    for x in (-2.6, 2.6): k -= linie((x - 1.1, 1.0), (x + 1.1, 3.2), 0.9) + linie((x - 1.1, 3.2), (x + 1.1, 1.0), 0.9)
    return k - kette([(-3.6, -3.2), (-1.8, -2.4), (0, -3.2), (1.8, -2.4), (3.6, -3.2)], 0.9)

def engel():
    k = (C(6.2, 0, -0.8) - C(0.8, -2.3, 0.8) - C(0.8, 2.3, 0.8) - bogen(3.0, 210, 330, 1.1, 0, -0.8))
    return k + (E(5.0, 1.5, 0, 6.2) - E(3.6, 0.6, 0, 6.2))

def teufel():
    k = C(6.2, 0, -0.8) - C(0.8, -2.3, 0.6) - C(0.8, 2.3, 0.6) - halbkreis(3.0, 0, -2.4, oben=False)
    k -= linie((-4.0, 3.0), (-1.4, 2.0), 0.8) + linie((4.0, 3.0), (1.4, 2.0), 0.8)
    return k + poly([(-5.6, 2.6), (-7.0, 7.0), (-2.8, 4.8)]) + poly([(5.6, 2.6), (7.0, 7.0), (2.8, 4.8)])

def partygesicht():
    k = C(6.0, -1.6, -1.0) - _zu_auge(-3.8, 0.8) - _zu_auge(0.6, 0.8) - halbkreis(2.8, -1.6, -2.4, oben=False)
    hut = poly([(-4.8, 3.4), (1.6, 5.6), (-3.6, 7.0)])
    konfetti = C(0.9, 7.6, 4.8) + C(0.9, 10.4, 1.6) + C(0.9, 7.8, -3.2) + RC(1.4, 1.4, 10.6, -5.6, 30)
    return k + hut + C(1.1, -3.8, 7.0) + konfetti

def nerd():
    k = _kopf() - halbkreis(3.2, 0, -1.6, oben=False) + RC(2.6, 1.6, 0, -2.4) - RC(0.6, 1.8, 0, -2.4)
    k -= ring(2.5, 0.9).translate([-3.0, 2.0]) + ring(2.5, 0.9).translate([3.0, 2.0]) + RC(1.6, 0.9, 0, 2.6)
    k -= linie((-5.4, 2.6), (-7.4, 3.4), 0.9) + linie((5.4, 2.6), (7.4, 3.4), 0.9)
    return k - C(0.7, -3.0, 2.0) - C(0.7, 3.0, 2.0)

# ---------------------------------------------------------------- Stimmung (Stimmungskalender)
def _stimmung(stufe):
    """Gesicht links, Signal-Balken rechts: 5 = super … 1 = mies"""
    k = C(6.4, -5.4, 0) - C(0.9, -7.7, 2.0) - C(0.9, -3.1, 2.0)
    k -= {5: halbkreis(3.4, -5.4, -1.0, oben=False),
          4: bogen(3.0, 210, 330, 1.2, -5.4, -0.4),
          3: RC(5.0, 1.2, -5.4, -2.8),
          2: bogen(3.0, 30, 150, 1.2, -5.4, -5.6),
          1: bogen(3.0, 30, 150, 1.2, -5.4, -5.6) + tropfen(-3.1, -0.6, 0.8, 1.2)}[stufe]
    for i in range(5):
        x = 2.6 + 2.4 * i
        k += R(1.6, 2.6 + 2.6 * i, x - 0.8, -6.5) if i < stufe else C(0.8, x, -5.7)
    return k

def stimmung_super(): return _stimmung(5)
def stimmung_gut(): return _stimmung(4)
def stimmung_okay(): return _stimmung(3)
def stimmung_schlecht(): return _stimmung(2)
def stimmung_mies(): return _stimmung(1)

# ---------------------------------------------------------------- Stunden (z. B. Lernzeit)
def _text_grundlinie(txt, hoehe, x=0.0):
    """Text mit Ziffern-/Großbuchstabenhöhe hoehe auf der Grundlinie y = 0, linker Rand bei x."""
    tp = TextPath((0, 0), txt, size=hoehe / 0.729, prop=gl.SCHRIFT)     # DejaVu Sans Bold: Ziffern = 0,729 × Schriftgröße
    cs = CrossSection([[tuple(pt) for pt in q] for q in tp.to_polygons() if len(q) > 2], FillRule.EvenOdd)
    return cs.translate([x - cs.bounds()[0], 0])

def _stunden(zahl, einheit="h"):
    if einheit == "min":                  # zu breit für eine Zeile → untereinander
        return gl.text_cs(zahl, 7.0).translate([0, 3.3]) + gl.text_cs("MIN", 5.0).translate([0, -4.4])
    if ":" in zahl:                       # Viertelstunden: ganze Zahl groß, „:15“ klein auf derselben Grundlinie
        ganz, rest = zahl.split(":")
        z = _text_grundlinie(ganz, 9.4)
        s = z + _text_grundlinie(":" + rest, 6.2, z.bounds()[2] + 0.3)      # ohne „h“: „1:15“ ist eindeutig eine Zeit
    else:
        z = gl.text_cs(zahl, 9.4)
        e = gl.text_cs(einheit, 6.2)
        zx0, zy0, zx1, _ = z.bounds()
        ex0, ey0, ex1, _ = e.bounds()
        e = e.translate([zx1 - ex0 + 0.9, zy0 - ey0])
        s = z + e
    x0, y0, x1, y1 = s.bounds()
    return s.translate([-(x0 + x1) / 2, -(y0 + y1) / 2])

def _stunden_f(zahl, einheit="h"):
    return lambda: _stunden(zahl, einheit)

def _stunden_liste():
    """15, 30, 45 min, dann 1 h bis 20 h in Viertelstunden. Schlüssel nach Dezimalwert (1_25h = 1:15, 1_5h = 1:30)."""
    liste = [(f"{m}min", _stunden_f(str(m), "min"), f"{m} Minuten", f"{m} minutes") for m in (15, 30, 45)]
    for q in range(4, 81):
        h, r = divmod(q, 4)
        key = f"{h}h" if not r else f"{h}_{('25', '5', '75')[r - 1]}h"
        txt = str(h) if not r else f"{h}:{r * 15}"
        de = f"{h} Stunde" if q == 4 else (f"{h} Stunden" if not r else f"{h}:{r * 15} Stunden")
        en = f"{h} hour" if q == 4 else (f"{h} hours" if not r else f"{h}:{r * 15} hours")
        liste.append((key, _stunden_f(txt), de, en))
    return liste

STUNDEN = _stunden_liste()

# ---------------------------------------------------------------- Zeichen
def haken():
    return kette([(-6.6, 0.2), (-2.2, -4.6), (7.0, 5.6)], 2.4)

def kreuz():
    return linie((-5.4, -5.4), (5.4, 5.4), 2.4) + linie((-5.4, 5.4), (5.4, -5.4), 2.4)

def plus():
    return RC(12.4, 3.0) + RC(3.0, 12.4)

def pfeil():
    return RC(14.0, 3.0, -3.6, 0) + poly([(2.4, 6.0), (10.4, 0), (2.4, -6.0)])

def wiederholen():
    s = bogen(5.6, 30, 170, 1.6) + bogen(5.6, 210, 350, 1.6)
    for w in (30, 210):
        c, si = math.cos(math.radians(w)), math.sin(math.radians(w))
        x, y = 5.6 * c, 5.6 * si
        tx, ty = si, -c                                     # Pfeilspitze am Bogenanfang, im Uhrzeigersinn
        s += poly([(x + 2.0 * c, y + 2.0 * si), (x - 2.0 * c, y - 2.0 * si), (x + 2.8 * tx, y + 2.8 * ty)])
    return s

def warnung():
    d = poly([(0, 7.0), (8.0, -6.6), (-8.0, -6.6)])
    d -= poly([(0, 4.4), (5.6, -5.2), (-5.6, -5.2)])
    return d + rrect(1.6, 4.4, 0.7, 0, -0.4) + C(0.9, 0, -3.8)

def verbot():
    return ring(6.8, 1.6) + RC(1.6, 12.0, 0, 0, 45)

def info():
    return ring(6.8, 1.3) + C(1.1, 0, 3.4) + RC(1.8, 5.4, 0, -1.4) + RC(3.4, 1.2, -0.4, 1.0) + RC(4.0, 1.2, 0, -4.0)

def zielflagge():
    f = R(13.6, 8.4, -5.0, -1.4)
    loch = LEER
    for i in range(6):
        for j in range(4):
            if (i + j) % 2: loch += R(13.6 / 6, 8.4 / 4, -5.0 + i * 13.6 / 6, -1.4 + j * 2.1)
    f -= loch.offset(-0.2)                               # Ecken der schwarzen Felder verbinden
    rand = R(13.6, 8.4, -5.0, -1.4) - R(12.4, 7.2, -4.4, -0.8)
    return f + rand + RC(1.6, 14.0, -5.8, 0)

def zielscheibe():
    s = ring(6.8, 1.4) + ring(4.2, 1.4) + C(1.6)
    return s + linie((1.2, 1.2), (9.0, 6.0), 1.3) + poly([(8.0, 6.4), (11.6, 6.6), (9.6, 4.0)])

# ---------------------------------------------------------------- Feiern & Erfolg
def krone():
    k = poly([(-8.0, -4.0), (8.0, -4.0), (9.0, 4.0), (4.6, 0.4), (0, 5.4), (-4.6, 0.4), (-9.0, 4.0)])
    k += C(1.1, -9.0, 4.6) + C(1.1, 9.0, 4.6) + C(1.1, 0, 6.0)
    k += RC(16.0, 1.8, 0, -5.8)
    return k - C(0.9, 0, -1.2) - C(0.8, -4.4, -1.8) - C(0.8, 4.4, -1.8)

def pokal():
    p = (C(5.0, 0, 3.0) ^ RC(11, 6, 0, 0.0)) + RC(10.0, 4.0, 0, 5.0)
    p += bogen(2.4, 90, 270, 1.3, -5.0, 3.4) + bogen(2.4, -90, 90, 1.3, 5.0, 3.4)
    p += RC(1.8, 3.6, 0, -3.4) + RC(7.6, 1.6, 0, -6.2) + RC(5.0, 1.2, 0, -5.0)
    return p - stern5(1.8, 0, 3.0)

def medaille():
    band = poly([(-5.0, 7.0), (-1.6, 7.0), (1.4, 0.6), (-1.6, 0.0)]) + poly([(5.0, 7.0), (1.6, 7.0), (-1.4, 0.6), (1.6, 0.0)])
    m = C(4.6, 0, -2.6) - ring(3.2, 0.8).translate([0, -2.6])
    return band + m

def diamant():
    d = poly([(-8.0, 2.4), (-4.6, 6.0), (4.6, 6.0), (8.0, 2.4), (0, -7.0)])
    for p, q in [((-8.0, 2.4), (8.0, 2.4)), ((-3.0, 2.4), (0, -6.0)), ((3.0, 2.4), (0, -6.0)),
                 ((-4.6, 6.0), (-3.0, 2.4)), ((4.6, 6.0), (3.0, 2.4)), ((0, 6.0), (-3.0, 2.4)), ((0, 6.0), (3.0, 2.4))]:
        d -= linie(p, q, 0.8)
    return d

def anstossen():
    def glas():
        g = poly([(-2.6, 5.0), (2.6, 5.0), (2.2, -1.0), (-2.2, -1.0)]) - RC(3.4, 0.9, 0, 3.0)
        return g + RC(1.4, 3.6, 0, -2.6) + RC(4.6, 1.4, 0, -4.8)
    s = glas().rotate(15).translate([-4.0, -1.0]) + glas().rotate(-15).translate([4.0, -1.0])
    for p, q in [((0, 5.6), (0, 7.0)), ((-2.4, 5.4), (-3.4, 6.8)), ((2.4, 5.4), (3.4, 6.8))]:
        s += linie(p, q, 1.2)
    return s

def hufeisen():
    h = (C(6.6, 0, 0.6) - C(3.6, 0, 0.6)) - poly([(-2.8, -1.0), (2.8, -1.0), (4.6, -7.0), (-4.6, -7.0)])
    for w in (200, 160, 120, 60, 20, -20):
        h -= C(0.55, 5.1 * math.cos(math.radians(w)), 0.6 + 5.1 * math.sin(math.radians(w)))
    return h

def ringe():
    stein = poly([(1.0, 5.0), (2.0, 6.4), (3.6, 6.4), (4.6, 5.0), (2.8, 2.8)])
    return ring(4.6, 1.3).translate([-2.8, -1.4]) + ring(4.6, 1.3).translate([2.8, -1.4]) + stein

def feuerwerk():
    s = C(1.3)
    for k in range(12):
        w = math.radians(30 * k)
        r0, r1 = 2.4, (6.6 if k % 2 == 0 else 5.0)
        s += linie((r0 * math.cos(w), r0 * math.sin(w)), (r1 * math.cos(w), r1 * math.sin(w)), 1.2)
    return s.translate([-4.0, 0.4]) + stern5(2.2, 8.0, 3.8) + stern5(1.6, 8.6, -3.6) + C(0.8, 4.6, -6.0)

def zauberhut():
    h = rrect(17.0, 1.8, 0.8, -1.6, -5.4) + poly([(-7.0, -4.6), (3.8, -4.6), (3.4, 6.4), (-6.6, 6.4)])
    h -= RC(11.4, 1.2, -1.6, -2.6)
    stab = linie((5.2, 0.6), (10.0, -4.4), 1.4)
    return h + stab + stern5(2.4, 9.0, 3.4) + stern5(1.5, 11.6, 0.0)

def daumen():
    d = rrect(4.0, 9.0, 1.0, -7.0, -2.0)
    hand = poly([(-4.4, 2.0), (-0.8, 3.4), (0.6, 7.0), (2.4, 6.6), (2.2, 2.6), (7.6, 2.6), (8.4, 1.2),
                 (7.6, -6.6), (-4.4, -6.6)])
    for y in (0.6, -1.8, -4.2): hand -= linie((3.6, y), (8.6, y), 0.8)
    return d + hand

# ---------------------------------------------------------------- Kleidung & Pflege
def tshirt():
    t = poly([(-3.6, 6.4), (-9.6, 3.6), (-11.4, -0.6), (-7.6, -1.4), (-6.0, 1.0), (-6.0, -7.0),
              (6.0, -7.0), (6.0, 1.0), (7.6, -1.4), (11.4, -0.6), (9.6, 3.6), (3.6, 6.4)])
    return t - E(3.2, 2.4, 0, 6.6)

def kleid():
    k = poly([(-3.0, 7.0), (-2.4, 2.0), (-8.6, -7.0), (8.6, -7.0), (2.4, 2.0), (3.0, 7.0), (1.4, 7.0), (0, 4.6), (-1.4, 7.0)])
    return k - RC(6.2, 0.9, 0, 1.4) - kette([(-6.0, -4.6), (-3.0, -3.6), (0, -4.6), (3.0, -3.6), (6.0, -4.6)], 0.8)

def schuh():
    s = poly([(-11.4, 4.6), (-5.0, 4.6), (-4.0, 1.6), (4.6, -0.6), (10.8, -1.8), (11.6, -4.6), (-11.4, -4.6)])
    s -= RC(23.4, 0.9, 0, -2.9)
    for x in (-3.2, -0.6, 2.0): s -= linie((x, 0.8), (x + 0.6, -1.4), 0.8)
    return s

def muetze():
    m = halbkreis(7.0, 0, -3.2) + rrect(16.0, 3.4, 1.0, 0, -4.8) + C(2.2, 0, 4.6)
    for x in (-3.0, 0, 3.0): m -= RC(0.8, 5.0, x, 0.2)
    return m

def socke():
    s = kette([(0, 6.0), (0, -1.4), (3.4, -4.6), (7.0, -4.6)], 5.2)
    s -= RC(6.4, 0.9, 0, 3.2)
    return s.translate([-3.4, 0])

def brille():
    g = (rrect(8.0, 6.2, 2.4, -5.4, -0.6) - rrect(5.4, 3.6, 1.2, -5.4, -0.6)) + (rrect(8.0, 6.2, 2.4, 5.4, -0.6) - rrect(5.4, 3.6, 1.2, 5.4, -0.6))
    return g + bogen(1.8, 20, 160, 1.2, 0, 1.4) + linie((-9.4, 1.4), (-12.2, 3.6), 1.2) + linie((9.4, 1.4), (12.2, 3.6), 1.2)

def zahnbuerste():
    z = rrect(16.0, 2.4, 1.2, 2.0, -1.4) + rrect(7.4, 2.0, 0.6, -7.4, -0.6)
    for k in range(5): z += RC(1.2, 3.6, -10.2 + k * 1.4, 2.2)
    return z.rotate(10) + tropfen(9.0, 4.0, 1.2, 6.8)

def dusche():
    s = kette([(-8.0, -7.0), (-8.0, 5.0), (-6.0, 6.6), (-1.2, 6.6), (0, 5.2)], 1.4)
    s += halbkreis(3.6, 0, 1.6) + RC(1.4, 1.6, 0, 4.6)
    for x, y in [(-2.4, -1.6), (0, -2.4), (2.4, -1.6), (-1.2, -5.2), (1.6, -5.4)]:
        s += tropfen(x, y - 0.6, 0.7, y + 1.0)
    return s

def schnuller():
    s = E(8.4, 3.6, 0, -0.6) - E(5.8, 1.6, 0, -0.6)
    s += C(1.6, 0, -0.6) + ring(3.4, 1.3).translate([0, 4.6])
    s += tropfen(0, -5.0, 1.8, -2.6)
    return s

def kinderwagen():
    k = halbkreis(6.4, -1.0, -2.0, oben=False) + (C(6.4, -1.0, -2.0) ^ R(6.4, 6.4, -1.0, -2.0))
    k -= RC(14, 0.9, -1.0, -1.6)
    griff = kette([(5.4, -1.6), (8.0, 4.6), (10.4, 4.6)], 1.3)
    return k + griff + C(1.6, -5.0, -7.4 + 1.6) + C(1.6, 3.0, -7.4 + 1.6) - C(0.6, -5.0, -5.8) - C(0.6, 3.0, -5.8)

# ---------------------------------------------------------------- Studium
def _blatt(w, h, ohr=0.0, x=0, y=0):
    """Blatt (Mitte x, y), optional mit Eselsohr oben rechts"""
    pts = [(-w / 2, -h / 2), (w / 2, -h / 2), (w / 2, h / 2 - ohr), (w / 2 - ohr, h / 2), (-w / 2, h / 2)]
    return poly([(px + x, py + y) for px, py in pts])

def abgabe():                             # Dokument wandert in die Ablage
    d = _blatt(8.6, 12.4, 2.6, -7.6, 0.4)
    for y, b in [(2.6, 4.0), (0.2, 5.6), (-2.2, 5.6), (-4.6, 5.6)]: d -= RC(b, 0.9, -7.6 - (5.6 - b) / 2, y)
    ablage = kette([(3.0, -2.0), (3.0, -6.2), (12.0, -6.2), (12.0, -2.0)], 1.4)
    pfeil = linie((7.5, 6.6), (7.5, 0.8), 1.8) + poly([(4.8, 1.2), (10.2, 1.2), (7.5, -2.6)])
    return d + ablage + pfeil

def deadline():                           # Uhr mit Ausrufezeichen
    u = ring(6.0, 1.4).translate([-3.6, 0]) + C(0.9, -3.6, 0)
    u += linie((-3.6, 0), (-3.6, 3.6), 1.3) + linie((-3.6, 0), (-1.0, -1.6), 1.3)
    return u + rrect(2.4, 8.6, 1.0, 8.2, 2.0) + C(1.4, 8.2, -5.0)

def klausur():                            # Ankreuzbogen mit Stoppuhr
    b = _blatt(11.6, 13.0, 2.6, -5.4, 0)
    for y in (3.2, -0.2, -3.6):
        b -= RC(2.4, 2.4, -8.4, y) + RC(4.6, 0.9, -3.8, y)
    b += RC(1.2, 1.2, -8.4, 3.2)                       # angekreuzt
    uhr = ring(3.8, 1.3).translate([7.4, -1.8]) + RC(1.6, 1.8, 7.4, 2.8) + RC(3.2, 1.2, 7.4, 3.8)
    return b + uhr + linie((7.4, -1.8), (7.4, 0.6), 1.2)

def muendlich():                          # zwei Sprechblasen
    b1 = rrect(13.0, 7.6, 2.4, -4.8, 2.6) + poly([(-8.6, -0.6), (-9.8, -4.0), (-5.0, -0.6)])
    b2 = rrect(11.0, 6.4, 2.2, 5.6, -3.0) + poly([(8.4, -5.6), (10.6, -7.0), (10.0, -4.0)])
    b1 -= b2.offset(1.1)
    for x in (-8.0, -4.8, -1.6): b1 -= C(0.9, x, 2.8)
    return b1 + b2

def vorlesung():                          # Tafel mit Dozent
    tafel = rrect(18.4, 12.0, 0.8, 3.4, 0.6) - rrect(15.6, 9.2, 0.4, 3.4, 0.6)
    tafel += kette([(-2.4, -2.2), (0.6, 1.6), (3.0, -0.6), (6.0, 2.8), (8.6, 0.6)], 1.2)
    person = C(1.8, -10.6, 2.2) + rrect(3.8, 6.4, 1.4, -10.6, -3.6)
    return tafel + person + linie((-9.6, -0.6), (-4.6, 2.6), 1.2)

def lernen():                             # Bücherstapel
    s = LEER
    for w, x, y, a in [(17.0, 0, -5.2, 0), (15.0, 1.0, -1.4, 4), (14.0, -0.6, 2.6, -3)]:
        buch = rrect(w, 3.4, 0.8) - RC(4.0, 0.8, w / 2 - 2.6, 0) - RC(0.9, 3.6, -w / 2 + 2.4, 0)
        s += buch.rotate(a).translate([x, y])
    return s

def referat():                            # Leinwand mit Diagramm
    l = rrect(18.0, 10.4, 0.8, 0, 1.4) - RC(15.4, 7.8, 0, 1.4)
    for x, h in [(-4.0, 2.4), (-0.8, 4.0), (2.4, 5.6)]: l += R(2.2, h, x, -2.5)
    l += RC(21.0, 1.4, 0, 6.2)
    return l + linie((0, -3.8), (0, -5.0), 1.4) + linie((0, -4.6), (-4.0, -6.6), 1.3) + linie((0, -4.6), (4.0, -6.6), 1.3)

def uni():                                # Gebäude mit Säulen
    g = poly([(-11.6, 2.0), (0, 7.0), (11.6, 2.0)]) - C(1.2, 0, 3.8)
    for x in (-7.5, -2.5, 2.5, 7.5): g += RC(2.2, 6.4, x, -2.4)
    return g + RC(20.0, 1.2, 0, 1.0) + RC(23.0, 1.6, 0, -6.2)

def hausarbeit():                         # Blätterstapel
    vorne = _blatt(11.4, 12.4, 3.2, -1.6, -0.8)
    for y, b in [(2.8, 5.0), (0.4, 7.4), (-2.0, 7.4), (-4.4, 7.4)]: vorne -= RC(b, 0.9, -1.6 - (7.4 - b) / 2, y)
    hinten = _blatt(11.4, 12.4, 0, 2.0, 0.6) - vorne.offset(1.0)
    return vorne + hinten

def abschluss():                          # Doktorhut
    oben = poly([(-11.4, 3.4), (0, 7.0), (11.4, 3.4), (0, -0.2)])
    kappe = (RC(12.0, 4.2, 0, -1.6) + E(6.0, 1.6, 0, -3.7)) - oben.offset(0.9)
    quaste = linie((8.6, 2.8), (8.6, -2.8), 1.2) + poly([(7.6, -2.6), (9.6, -2.6), (10.2, -6.4), (7.0, -6.4)])
    return oben + kappe + quaste

def lerngruppe():                         # drei Personen
    def person(x, k):
        return C(2.3 * k, x, 1.6 * k + 0.4) + halbkreis(4.4 * k, x, -7.0)
    mitte = person(0, 1.15)
    return (person(-7.6, 0.95) + person(7.6, 0.95)) - mitte.offset(1.0) + mitte

def labor():                              # Erlenmeyerkolben
    k = poly([(-1.8, 5.8), (1.8, 5.8), (1.8, 1.6), (7.4, -6.6), (-7.4, -6.6), (-1.8, 1.6)])
    innen = k.offset(-1.3)
    k = (k - innen) + (innen ^ R(16, 4.4, -8, -7.0)) + RC(6.0, 1.4, 0, 6.2)
    return k + C(1.0, 4.4, 4.0) + C(0.8, 6.2, 6.0) + C(0.7, -0.6, -0.6)

GRUPPEN = [
    ("tiere", "Tiere", "Animals", [
        ("fisch", fisch, "Fisch", "Fish"), ("vogel", vogel, "Vogel", "Bird"),
        ("schmetterling", schmetterling, "Schmetterling", "Butterfly"), ("schnecke", schnecke, "Schnecke", "Snail"),
        ("hase", hase, "Hase", "Rabbit"), ("maus", maus, "Maus", "Mouse"), ("eule", eule, "Eule", "Owl"),
        ("marienkaefer", marienkaefer, "Marienkäfer", "Ladybird"), ("biene", biene, "Biene", "Bee"),
        ("schildkroete", schildkroete, "Schildkröte", "Turtle")]),
    ("natur", "Natur & Wetter", "Nature & weather", [
        ("wolke", wolke, "Wolke", "Cloud"), ("regen", regen, "Regen", "Rain"), ("mond", mond, "Mond & Sterne", "Moon & stars"),
        ("regenbogen", regenbogen, "Regenbogen", "Rainbow"), ("berge", berge, "Berge", "Mountains"),
        ("tanne", tanne, "Tanne", "Fir tree"), ("pilz", pilz, "Pilz", "Mushroom"), ("blatt", blatt, "Blatt", "Leaf"),
        ("wind", wind, "Wind", "Wind"), ("thermometer", thermometer, "Thermometer", "Thermometer")]),
    ("essen", "Essen & Trinken", "Food & drink", [
        ("kirschen", kirschen, "Kirschen", "Cherries"), ("erdbeere", erdbeere, "Erdbeere", "Strawberry"),
        ("banane", banane, "Banane", "Banana"), ("karotte", karotte, "Karotte", "Carrot"), ("birne", birne, "Birne", "Pear"),
        ("brot", brot, "Brot", "Bread"), ("spiegelei", spiegelei, "Spiegelei / Frühstück", "Fried egg / breakfast"),
        ("burger", burger, "Burger", "Burger"), ("weinglas", weinglas, "Weinglas", "Wine glass"),
        ("teekanne", teekanne, "Tee", "Tea")]),
    ("unterwegs", "Unterwegs", "Getting around", [
        ("bus", bus, "Bus", "Bus"), ("segelboot", segelboot, "Segelboot", "Sailing boat"), ("lkw", lkw, "Lkw / Umzug", "Truck / moving"),
        ("ampel", ampel, "Ampel", "Traffic light"), ("anker", anker, "Anker", "Anchor"), ("kompass", kompass, "Kompass", "Compass"),
        ("ortsmarker", ortsmarker, "Ort / Treffpunkt", "Location / meeting point"),
        ("tankstelle", tankstelle, "Tanken", "Refuel"), ("fahrkarte", fahrkarte, "Ticket / Fahrkarte", "Ticket"),
        ("heissluftballon", heissluftballon, "Heißluftballon", "Hot-air balloon")]),
    ("zuhause", "Zuhause", "Home", [
        ("schluessel", schluessel, "Schlüssel", "Key"), ("gluehbirne", gluehbirne, "Glühbirne / Idee", "Light bulb / idea"),
        ("kerze", kerze, "Kerze", "Candle"), ("bett", bett, "Bett / Ausschlafen", "Bed / sleep in"),
        ("wecker", wecker, "Wecker", "Alarm clock"), ("fernseher", fernseher, "Fernsehen", "TV"),
        ("buegeleisen", buegeleisen, "Bügeln", "Ironing"), ("sofa", sofa, "Sofa / Entspannen", "Sofa / relax"),
        ("kuehlschrank", kuehlschrank, "Kühlschrank", "Fridge"), ("hammer", hammer, "Heimwerken", "DIY")]),
    ("buero", "Büro & Schule", "Office & school", [
        ("bleistift", bleistift, "Bleistift", "Pencil"), ("brief", brief, "Brief / E-Mail", "Letter / e-mail"),
        ("kalender", kalenderblatt, "Kalender", "Calendar"), ("laptop", laptop, "Laptop", "Laptop"),
        ("bueroklammer", bueroklammer, "Büroklammer", "Paper clip"), ("lupe", lupe, "Lupe / Suchen", "Magnifier / search"),
        ("taschenrechner", taschenrechner, "Taschenrechner", "Calculator"), ("ordner", ordner, "Ordner", "Folder"),
        ("schultuete", schultuete, "Schultüte / Einschulung", "School cone / first day"),
        ("glocke", glocke, "Glocke / Erinnerung", "Bell / reminder")]),
    ("gesichter", "Gesichter", "Faces", [
        ("lachen", lachen, "Lachen", "Laughing"), ("traurig", traurig, "Traurig", "Sad"), ("zwinkern", zwinkern, "Zwinkern", "Wink"),
        ("ueberrascht", ueberrascht, "Überrascht", "Surprised"), ("verliebt", verliebt, "Verliebt", "In love"),
        ("muede", muede, "Müde", "Sleepy"), ("cool", cool, "Cool", "Cool"), ("wuetend", wuetend, "Wütend", "Angry"),
        ("neutral", neutral, "Neutral", "Neutral"), ("kuss", kuss, "Kuss", "Kiss")]),
    ("gesichter2", "Gesichter", "Faces", [
        ("traenenlachen", traenenlachen, "Tränen lachen", "Tears of joy"), ("grinsen", grinsen, "Grinsen", "Grin"),
        ("schuechtern", schuechtern, "Schüchtern", "Shy"), ("nachdenklich", nachdenklich, "Nachdenklich", "Thinking"),
        ("verwirrt", verwirrt, "Verwirrt", "Confused"), ("gelangweilt", gelangweilt, "Gelangweilt", "Bored"),
        ("gestresst", gestresst, "Gestresst", "Stressed"), ("krank", krank, "Krank", "Sick"),
        ("weinen", weinen, "Weinen", "Crying"), ("schockiert", schockiert, "Schockiert", "Shocked"),
        ("strahlend", strahlend, "Strahlend", "Beaming"), ("zunge", zunge, "Albern", "Silly"),
        ("zufrieden", zufrieden, "Zufrieden", "Content"), ("sternaugen", sternaugen, "Begeistert", "Star-struck"),
        ("augenrollen", augenrollen, "Genervt", "Eye roll"), ("fertig", fertig, "Fix und fertig", "Knocked out"),
        ("engel", engel, "Engel", "Angel"), ("teufel", teufel, "Teufelchen", "Little devil"),
        ("partygesicht", partygesicht, "Partylaune", "Party mood"), ("nerd", nerd, "Nerd", "Nerd")]),
    ("stimmung", "Stimmung", "Mood", [
        ("super", stimmung_super, "Stimmung 5 – super (grün)", "Mood 5 – great (green)"),
        ("gut", stimmung_gut, "Stimmung 4 – gut (hellgrün)", "Mood 4 – good (light green)"),
        ("okay", stimmung_okay, "Stimmung 3 – okay (gelb)", "Mood 3 – okay (yellow)"),
        ("schlecht", stimmung_schlecht, "Stimmung 2 – schlecht (orange)", "Mood 2 – bad (orange)"),
        ("mies", stimmung_mies, "Stimmung 1 – mies (rot)", "Mood 1 – awful (red)")]),
    ("stunden", "Stunden", "Hours", STUNDEN),
    ("zeichen", "Zeichen", "Signs", [
        ("haken", haken, "Häkchen / Erledigt", "Tick / done"), ("kreuz", kreuz, "Kreuz / Abgesagt", "Cross / cancelled"),
        ("plus", plus, "Plus", "Plus"), ("pfeil", pfeil, "Pfeil", "Arrow"), ("wiederholen", wiederholen, "Wiederholen", "Repeat"),
        ("warnung", warnung, "Achtung", "Warning"), ("verbot", verbot, "Verbot / Nein", "Prohibited / no"),
        ("info", info, "Info", "Info"), ("zielflagge", zielflagge, "Zielflagge", "Chequered flag"),
        ("zielscheibe", zielscheibe, "Ziel", "Target")]),
    ("feiern", "Feiern & Erfolg", "Celebration & success", [
        ("krone", krone, "Krone", "Crown"), ("pokal", pokal, "Pokal", "Trophy"), ("medaille", medaille, "Medaille", "Medal"),
        ("diamant", diamant, "Diamant", "Diamond"), ("anstossen", anstossen, "Anstoßen", "Cheers"),
        ("hufeisen", hufeisen, "Hufeisen / Glück", "Horseshoe / luck"), ("ringe", ringe, "Hochzeit / Jahrestag", "Wedding / anniversary"),
        ("feuerwerk", feuerwerk, "Feuerwerk", "Fireworks"), ("zauberhut", zauberhut, "Zauberei", "Magic"),
        ("daumen", daumen, "Daumen hoch", "Thumbs up")]),
    ("pflege", "Kleidung & Pflege", "Clothes & care", [
        ("tshirt", tshirt, "T-Shirt", "T-shirt"), ("kleid", kleid, "Kleid", "Dress"), ("schuh", schuh, "Schuh", "Shoe"),
        ("muetze", muetze, "Mütze", "Beanie"), ("socke", socke, "Socke", "Sock"), ("brille", brille, "Brille / Optiker", "Glasses / optician"),
        ("zahnbuerste", zahnbuerste, "Zähneputzen", "Brush teeth"), ("dusche", dusche, "Duschen", "Shower"),
        ("schnuller", schnuller, "Baby (Schnuller)", "Baby (dummy)"), ("kinderwagen", kinderwagen, "Kinderwagen", "Pram")]),
    ("studium", "Studium", "University", [
        ("abgabe", abgabe, "Abgabe", "Submission"), ("deadline", deadline, "Deadline / Frist", "Deadline"),
        ("klausur", klausur, "Klausur", "Written exam"), ("muendlich", muendlich, "Mündliche Prüfung", "Oral exam"),
        ("vorlesung", vorlesung, "Vorlesung", "Lecture"), ("lernen", lernen, "Lernen", "Studying"),
        ("referat", referat, "Referat / Präsentation", "Presentation"), ("uni", uni, "Uni / Campus", "University / campus"),
        ("hausarbeit", hausarbeit, "Hausarbeit", "Term paper"), ("abschluss", abschluss, "Abschluss", "Graduation"),
        ("lerngruppe", lerngruppe, "Lerngruppe", "Study group"), ("labor", labor, "Labor / Praktikum", "Lab / practical")]),
]

GRUPPEN = [(key, de, en, [(k, passend(f), nde, nen) for k, f, nde, nen in liste]) for key, de, en, liste in GRUPPEN]

def _m(f):
    return lambda: muster_cs(f)

# Stimmung und Stunden liegen beim Stimmungs- bzw. Lernkalender (eigene Platten unten), alles andere bei den Extra-Schubladen
ORDNER = {}

PLATTEN = [Platte(f"{ORDNER.get(key, '4_Extra_Schubladen/weitere_symbole/')}schubladen_{key}_{len(liste)}x.stl",
                  [(f"z_{key}_{k}", _m(f)) for k, f, *_ in liste], 6 if len(liste) % 6 == 0 else 5)
           for key, _, _, liste in GRUPPEN if key not in ("stimmung", "stunden")]
# Lernkalender: 80 Stunden-Schubladen auf 3 Platten (je höchstens 30, 6 × 5)
_std = dict((g[0], g[3]) for g in GRUPPEN)["stunden"]
_zeit = lambda k: k.replace("_25h", "h15").replace("_75h", "h45").replace("_5h", "h30")
PLATTEN += [Platte(f"6_Lernkalender/schubladen_stunden_{_zeit(_std[i][0])}-{_zeit(_std[min(i + 29, len(_std) - 1)][0])}_{len(_std[i:i + 30])}x.stl",
                   [(f"z_stunden_{k}", _m(f)) for k, f, *_ in _std[i:i + 30]], 6)
            for i in range(0, len(_std), 30)]
# Stimmungskalender: jede Stimmung auf eigener Platte (10 gleiche), damit sie in ihrer Farbe gedruckt werden kann
PLATTEN += [Platte(f"5_Stimmungskalender/stimmung_{nr}_{k}_10x.stl", [(f"z_stimmung_{k}", _m(f))] + [(None, _m(f))] * 9, 5)
            for nr, (k, f, *_) in zip((5, 4, 3, 2, 1), dict((g[0], g[3]) for g in GRUPPEN)["stimmung"])]
