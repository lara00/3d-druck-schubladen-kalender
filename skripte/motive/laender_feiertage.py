"""Feiertage weiterer Länder: Flaggen mit Länderkürzel (Nationalfeiertage) und allgemeine Motive.
"""
import math
from manifold3d import CrossSection
from basis import grundlagen as gl
from basis.zeichnen import C, E, R, RC, linie, ring, poly, tropfen, stern5, bogen, muster_cs
from basis.platten import Platte

def flagge(code):
    stange = R(1.3, 12.6, -9.4, -6.6) + C(0.95, -8.75, 5.9, 20)
    tuch = R(16.4, 10.4, -7.6, -4.2)
    return stange + (tuch - gl.text_cs(code, 5.8).translate([0.6, 1.0]))

def kelch():          # Gründonnerstag
    schale = (C(5.0, 0, 3.0, 48) ^ R(12, 6, -6, -3.0 + 0.0)) + R(10, 1.2, -5, 2.6)
    return schale + R(1.6, 6.0, -0.8, -5.2) + E(4.0, 1.0, 0, -5.8) + C(1.4, 0, -1.6)

def mohn():           # Gedenktage / Veterans / Armistice
    bluete = sum((C(2.9, 2.6 * math.cos(w), 2.6 * math.sin(w) + 1.4, 32) for w in [k * math.pi / 2 + 0.6 for k in range(4)]), CrossSection())
    bluete = bluete - C(1.5, 0, 1.4, 24) + C(0.9, 0, 1.4, 16)
    stiel = linie((0, -3.0), (1.0, -6.2), 1.2)
    blatt = E(2.4, 1.0, 2.6, -4.6, 30)
    return (bluete + stiel + blatt).translate([0, -0.2])

def taube():          # Befreiung / Sieg / Frieden
    koerper = E(5.4, 2.6, -0.4, -0.4, -10)
    kopf = C(2.0, 4.4, 1.6)
    schnabel = poly([(6.1, 1.9), (8.2, 1.3), (6.1, 0.9)])
    fluegel = poly([(-2.6, 0.6), (2.4, 0.8), (-1.2, 6.8), (-5.0, 5.6)])
    schwanz = poly([(-5.0, -0.6), (-8.6, 1.6), (-8.6, -2.6)])
    zweig = linie((5.4, -1.4), (8.0, -4.2), 0.9) + E(1.0, 0.6, 7.0, -2.4, 40) + E(1.0, 0.6, 7.8, -3.6, -20)
    return (koerper + kopf + schnabel + fluegel + schwanz + zweig - C(0.5, 4.8, 2.0, 12)) ^ R(26, 14, -13, -7)

def paragraph():      # Verfassungstag
    return gl.text_cs("§", 12.5)

def lorbeer():        # Gedenktag an Personen
    rechts = CrossSection()
    for i in range(6):
        w = math.radians(-70 + i * 26)
        rechts += E(1.6, 0.75, 5.4 * math.cos(w), 5.4 * math.sin(w) + 0.4, math.degrees(w) + 60)
    rechts += bogen(5.4, -75, 62, 0.9, 0, 0.4)
    kranz = rechts + rechts.mirror([1, 0])
    return kranz + linie((-1.6, -5.8), (1.6, -4.4), 1.0) + linie((1.6, -5.8), (-1.6, -4.4), 1.0)

def liegestuhl():     # Bank Holiday (GB/IE): Sonnenschirm am Strand
    dach = C(7.6, 0, -0.4, 64) ^ R(16, 8, -8, -0.4)
    for x in (-5.1, 0, 5.1):
        dach -= C(2.55, x, -0.4, 32) ^ R(6, 3, x - 3, -0.4 - 3)
    dach = dach.translate([0, 0.6])
    stab = linie((0, 0.2), (0, -5.6), 1.3)
    sand = linie((-7.5, -6.2), (7.5, -6.2), 1.2)
    return (dach + stab + sand + C(0.8, 0, 7.6 - 0.4 + 0.6 - 0.3, 12)) ^ R(26, 14, -13, -7)

def drachen():        # Rosenmontag orthodox (Drachensteigen)
    d = poly([(0, 7.0), (4.0, 1.6), (0, -3.6), (-4.0, 1.6)]) - linie((0, 6.2), (0, -2.8), 0.7) - linie((-3.2, 1.6), (3.2, 1.6), 0.7)
    schnur = CrossSection()
    pts = [(0.9 * math.sin(k / 1.4), -3.6 - k * 0.42) for k in range(8)]
    for a, b in zip(pts, pts[1:]): schnur += linie(a, b, 0.9)
    schleifen = poly([(-1.4, -5.0), (0.2, -4.4), (-1.4, -3.8)]) + poly([(1.6, -6.4), (0.0, -5.8), (1.6, -5.2)])
    return d + schnur + schleifen

def europa():         # Europatag: Kreis aus 12 Sternen (als Punkte)
    return sum((C(1.0, 5.6 * math.cos(k * math.pi / 6), 5.6 * math.sin(k * math.pi / 6), 16) for k in range(12)), CrossSection()) + stern5(2.6)

def feiertag_allg():  # allgemeiner Feiertag
    return ring(6.6, 1.3) + stern5(4.4)

FLAGGEN = ["LI", "LU", "BE", "ES", "GR", "PL", "IT", "PT", "TR", "CZ", "HR", "CA"]
MOTIVE = [("kelch", kelch, "Gründonnerstag", "Maundy Thursday"),
          ("mohn", mohn, "Gedenktag (Mohnblume)", "Remembrance (poppy)"),
          ("taube", taube, "Befreiung / Frieden", "Liberation / Peace"),
          ("paragraph", paragraph, "Verfassungstag", "Constitution Day"),
          ("lorbeer", lorbeer, "Gedenktag (Lorbeer)", "Commemoration (laurel)"),
          ("liegestuhl", liegestuhl, "Bank Holiday (freier Tag)", "Bank Holiday"),
          ("drachen", drachen, "Rosenmontag (orthodox)", "Clean Monday"),
          ("europa", europa, "Europatag", "Europe Day"),
          ("feiertag", feiertag_allg, "Feiertag (allgemein)", "Public holiday (general)")]
MOTIVE += [(f"flagge_{c}", (lambda c=c: flagge(c)), f"Nationalfeiertag {c}", f"National Day {c}") for c in FLAGGEN]

# Flaggen für die übrigen wählbaren Länder (zweite Platte)
FLAGGEN_2 = ["DE", "AT", "CH", "NL", "FR", "DK", "GB", "IE", "US"]
MOTIVE_2 = [(f"flagge_{c}", (lambda c=c: flagge(c)), f"Nationalfeiertag {c}", f"National Day {c}") for c in FLAGGEN_2]

def _m(f):
    return lambda: muster_cs(f)

PLATTEN = [Platte(f"4_Extra_Schubladen/schubladen_laender_feiertage_{len(MOTIVE)}x.stl", [("n_" + k, _m(f)) for k, f, *_ in MOTIVE]),
           Platte(f"4_Extra_Schubladen/schubladen_flaggen_{len(MOTIVE_2)}x.stl", [("n_" + k, _m(f)) for k, f, *_ in MOTIVE_2])]
