"""Gesetzliche und weitere Feiertage in Deutschland (20 Motive).
"""
import math
from manifold3d import CrossSection
from basis import kalender as mk
from basis.zeichnen import linie, ring, poly, tropfen, muster_cs
from basis.platten import Platte

def sektglas():
    kelch = poly([(-1, 0.5), (1, 0.5), (3.4, 6.6), (-3.4, 6.6)])
    stiel = CrossSection.square([1.4, 5.8]).translate([-0.7, -5.2])
    fuss = CrossSection.square([6.4, 1.4]).translate([-3.2, -6.6])
    perlen = sum((CrossSection.circle(0.8, 16).translate(p) for p in [(5.0, 5.2), (6.0, 2.6), (4.6, 0.4)]), CrossSection())
    return kelch + stiel + fuss + perlen

def krone():
    k = poly([(-6.5, -4.5), (6.5, -4.5), (6.5, 2.6), (3.25, -0.5), (0, 4.0), (-3.25, -0.5), (-6.5, 2.6)])
    kugeln = sum((CrossSection.circle(1.2, 24).translate(p) for p in [(-6.3, 3.6), (0, 5.4), (6.3, 3.6)]), CrossSection())
    return k + kugeln - linie((-7, -2.6), (7, -2.6), 0.9)

def herz():
    return mk.text_cs("♥", 12)

def frauentag():
    return ring(3.8, 1.5).translate([0, 2.4]) + linie((0, -1.4), (0, -6.2), 1.5) + linie((-2.6, -4.0), (2.6, -4.0), 1.5)

def kreuz():
    return CrossSection.square([2.2, 13.4]).translate([-1.1, -6.7]) + CrossSection.square([9, 2.2]).translate([-4.5, 1.4])

def hase():
    kopf = CrossSection.circle(4.2, 48).translate([0, -2.6])
    ohren = sum((CrossSection.circle(1, 32).scale([1.5, 4.0]).rotate(-s * 12).translate([s * 2.0, 3.0]) for s in (1, -1)),
                CrossSection())
    augen = CrossSection.circle(0.8, 16).translate([-1.5, -1.6]) + CrossSection.circle(0.8, 16).translate([1.5, -1.6])
    nase = poly([(-0.9, -3.4), (0.9, -3.4), (0, -4.4)])
    return kopf + ohren - augen - nase

def osterei():
    ei = CrossSection.circle(1, 64).scale([4.8, 6.4])
    zz = CrossSection()
    pts = [(-6 + k * 1.5, (0.9 if k % 2 else -0.9)) for k in range(9)]
    for a, b in zip(pts, pts[1:]):
        zz += linie(a, b, 1.0)
    return ei - zz

def hammer():
    stiel = linie((-5.0, -5.6), (2.4, 1.8), 1.9)
    kopf = CrossSection.square([9.5, 3.4], center=True).rotate(135).translate([3.4, 3.4])
    return (stiel + kopf).scale([0.9, 0.9]).translate([0, -0.3])

def blume():
    return mk.text_cs("✿", 12)

def wolke():
    w = CrossSection.circle(3.0, 40).translate([-4, -1.2]) + CrossSection.circle(4.2, 48).translate([0, 1.0]) \
        + CrossSection.circle(3.0, 40).translate([4.2, -1.0])
    return w + CrossSection.square([8.2, 3.0]).translate([-4, -4.2])

def flamme():
    return tropfen(0, -2.4, 4.2, 7.0) - tropfen(0, -3.4, 1.8, 1.6)

def tor():
    t = CrossSection.square([18, 1.4]).translate([-9, -6.6])
    for k in range(6):
        x = -7.6 + k * 3.04
        t += CrossSection.square([1.5, 7.6]).translate([x - 0.75, -5.2])
    t += CrossSection.square([18, 2.0]).translate([-9, 2.4])
    t += CrossSection.square([10, 1.6]).translate([-5, 4.4])
    t += CrossSection.square([3.2, 1.0]).translate([-1.6, 6.0])
    return t

def buch():
    links = poly([(-0.5, -5.2), (-7.4, -4.0), (-7.4, 5.0), (-0.5, 4.0)])
    rechts = poly([(0.5, -5.2), (7.4, -4.0), (7.4, 5.0), (0.5, 4.0)])
    zeilen = CrossSection()
    for y in (2.0, -0.4, -2.8):
        zeilen += linie((-6.0, y + 0.3), (-2.0, y - 0.2), 0.8) + linie((2.0, y - 0.2), (6.0, y + 0.3), 0.8)
    return links + rechts - zeilen

def kuerbis():
    k = CrossSection.circle(1, 48).scale([3.8, 5.0]).translate([-3.0, -1.4]) + \
        CrossSection.circle(1, 48).scale([3.8, 5.0]).translate([3.0, -1.4]) + CrossSection.circle(1, 48).scale([4.2, 5.4]).translate([0, -1.2])
    stiel = poly([(-0.9, 3.6), (0.9, 3.6), (1.6, 6.6), (0.2, 6.6)])
    augen = poly([(-4.2, -0.2), (-1.6, -0.2), (-2.9, 2.0)]) + poly([(1.6, -0.2), (4.2, -0.2), (2.9, 2.0)])
    mund = poly([(-4.6, -2.6), (4.6, -2.6), (3.4, -4.8), (1.7, -3.6), (0, -4.8), (-1.7, -3.6), (-3.4, -4.8)])
    return k + stiel - augen - mund

def kerze():
    k = CrossSection.square([4.6, 8.4]).translate([-2.3, -6.8])
    return k + tropfen(0, 3.2, 1.5, 7.0) + linie((0, 1.6), (0, 1.9), 0.8)

def stiefel():
    s = poly([(-4.2, 6.8), (1.4, 6.8), (1.4, -1.8), (6.4, -3.2), (6.8, -6.6), (-4.2, -6.6)])
    return s - linie((-5, 4.2), (2, 4.2), 0.9)

def glocke():
    g = poly([(-6.2, -4.0), (6.2, -4.0), (5.0, -2.6), (4.2, 3.0), (2.2, 5.2), (-2.2, 5.2), (-4.2, 3.0), (-5.0, -2.6)])
    return g + CrossSection.circle(1.5, 24).translate([0, -5.4]) + CrossSection.circle(1.2, 24).translate([0, 5.8])

def tannenbaum():
    t = poly([(-6.4, -3.6), (6.4, -3.6), (0, 1.8)]) + poly([(-5.0, -0.6), (5.0, -0.6), (0, 4.6)]) \
        + poly([(-3.6, 2.2), (3.6, 2.2), (0, 7.0)])
    return t + CrossSection.square([2.4, 3.2]).translate([-1.2, -6.8])

def kugel():
    k = CrossSection.circle(5.0, 64).translate([0, -2.0])
    kappe = CrossSection.square([3.0, 1.8]).translate([-1.5, 2.7])
    oese = ring(1.7, 1.2).translate([0, 5.1])
    return k - linie((-6, -1.6), (6, -1.6), 0.9) - linie((-6, -3.6), (6, -3.6), 0.9) + kappe + oese

def rakete():
    koerper = poly([(-1.9, -3.0), (1.9, -3.0), (1.9, 2.8), (0, 6.6), (-1.9, 2.8)])
    fl_l = poly([(-1.9, -0.6), (-1.9, -3.0), (-4.2, -4.6)])
    fl_r = poly([(1.9, -0.6), (4.2, -4.6), (1.9, -3.0)])
    feuer = tropfen(0, -3.9, 1.3, -7.0)          # überlappt den Körper
    fenster = CrossSection.circle(0.9, 20).translate([0, 1.2])
    funken = sum((CrossSection.circle(0.8, 16).translate(p) for p in [(5.0, 4.2), (-5.2, 4.6), (6.2, 0.8), (-6.0, 0.4)]),
                 CrossSection())
    return koerper - fenster + fl_l + fl_r + feuer + funken

# (Dateiname, Anzeigename, Datum 2027, Art)  – b = bundesweiter Feiertag, r = regional, f = Festtag (kein Feiertag)
FEIERTAGE = [
    ("neujahr", sektglas, "Neujahr", "1.1.", "b"),
    ("drei_koenige", krone, "Heilige Drei Könige", "6.1.", "r"),
    ("valentinstag", herz, "Valentinstag", "14.2.", "f"),
    ("frauentag", frauentag, "Internationaler Frauentag", "8.3.", "r"),
    ("karfreitag", kreuz, "Karfreitag", "26.3.2027", "b"),
    ("ostersonntag", hase, "Ostersonntag", "28.3.2027", "f"),
    ("ostermontag", osterei, "Ostermontag", "29.3.2027", "b"),
    ("tag_der_arbeit", hammer, "Tag der Arbeit", "1.5.", "b"),
    ("muttertag", blume, "Muttertag", "9.5.2027", "f"),
    ("himmelfahrt", wolke, "Christi Himmelfahrt / Vatertag", "6.5.2027", "b"),
    ("pfingstmontag", flamme, "Pfingstmontag", "17.5.2027", "b"),
    ("einheit", tor, "Tag der Deutschen Einheit", "3.10.", "b"),
    ("reformationstag", buch, "Reformationstag", "31.10.", "r"),
    ("halloween", kuerbis, "Halloween", "31.10.", "f"),
    ("allerheiligen", kerze, "Allerheiligen", "1.11.", "r"),
    ("nikolaus", stiefel, "Nikolaus", "6.12.", "f"),
    ("heiligabend", glocke, "Heiligabend", "24.12.", "f"),
    ("weihnachten_1", tannenbaum, "1. Weihnachtstag", "25.12.", "b"),
    ("weihnachten_2", kugel, "2. Weihnachtstag", "26.12.", "b"),
    ("silvester", rakete, "Silvester", "31.12.", "f"),
]

def _m(f):
    return lambda: muster_cs(f)

PLATTEN = [Platte("4_Extra_Schubladen/schubladen_feiertage_20x.stl", [("f_" + k, _m(f)) for k, f, *_ in FEIERTAGE])]
