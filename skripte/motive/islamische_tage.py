"""Islamische Fest- und Gedenktage (11 Motive).
"""
import math
from manifold3d import CrossSection
from basis import grundlagen as gl
from basis.zeichnen import linie, ring, poly, tropfen, muster_cs
from basis.platten import Platte

def stern5(r, x=0, y=0):
    return gl.stern(r, r * 0.45).translate([x, y])

def hilal(r=6.2, x=0, y=0):
    """Mondsichel, Öffnung nach rechts."""
    return (CrossSection.circle(r, 64) - CrossSection.circle(r * 0.82, 64).translate([r * 0.42, r * 0.12])).translate([x, y])

def neujahr():                       # Mondsichel + Stern
    return hilal(6.4, -1.6, 0) + stern5(2.8, 3.6, 0.4)

def aschura():                       # Schale (Aşure) mit Dampf
    schale = CrossSection.circle(6.4, 64).translate([0, 1.0]) ^ CrossSection.square([14, 6]).translate([-7, -5.4])
    rand = CrossSection.square([14.4, 1.4]).translate([-7.2, 0.3])
    fuss = CrossSection.square([5, 1.2]).translate([-2.5, -6.6])
    dampf = CrossSection()
    for x0 in (-2.6, 0.4, 3.4):
        pts = [(x0 + 0.7 * math.sin(k / 2.2), 2.6 + k * 0.4) for k in range(10)]
        for a, b in zip(pts, pts[1:]):
            dampf += linie(a, b, 1.2)
    return schale + rand + fuss + dampf

def mawlid():                        # Rose
    bluete = CrossSection.circle(4.2, 48).translate([0, 2.4])
    spirale = CrossSection()
    for k in range(26):              # Spiralschnitt in der Blüte
        w1, w2 = k * 0.42, (k + 1) * 0.42
        r1, r2 = 0.5 + w1 * 0.5, 0.5 + w2 * 0.5
        spirale += linie((r1 * math.cos(w1), 2.4 + r1 * math.sin(w1)), (r2 * math.cos(w2), 2.4 + r2 * math.sin(w2)), 0.8)
    stiel = linie((0, -1.6), (0, -6.1), 1.4)
    blaetter = CrossSection.circle(1, 32).scale([2.8, 1.2]).rotate(30).translate([2.2, -3.8]) + \
               CrossSection.circle(1, 32).scale([2.8, 1.2]).rotate(-30).translate([-2.2, -5.0])
    return (bluete - (spirale ^ CrossSection.circle(3.4, 48).translate([0, 2.4]))) + stiel + blaetter

def isra_miraj():                    # Nachthimmel: Mondsichel + Sterne
    return hilal(5.0, -5.0, 0.6) + stern5(2.2, 2.2, 3.6) + stern5(1.8, 7.2, 4.4) + stern5(2.0, 5.2, -2.6) + stern5(1.6, 0.6, -4.4)

def baraa():                         # Vollmond mit kleinen Sternen
    return CrossSection.circle(5.0, 64) + stern5(1.8, -8.6, 3.8) + stern5(1.6, 8.8, 4.2) + stern5(1.6, -8.0, -4.2) + stern5(1.8, 8.4, -3.6)

def ramadan():                       # Laterne (Fanoos)
    koerper = poly([(-3.4, -3.6), (3.4, -3.6), (4.2, 1.2), (2.4, 3.4), (-2.4, 3.4), (-4.2, 1.2)])
    fenster = poly([(-1.6, -2.2), (1.6, -2.2), (1.9, 1.0), (0, 2.2), (-1.9, 1.0)])
    sockel = CrossSection.square([8.4, 1.4]).translate([-4.2, -5.2])
    spitze = poly([(-2.0, 3.4), (2.0, 3.4), (0, 5.4)])
    oese = ring(1.3, 1.0).translate([0, 6.0])
    flamme = tropfen(0, -0.8, 0.9, 1.4)
    return (koerper - fenster + flamme + sockel + spitze + oese).translate([0, -0.4])

def qadr():                          # leuchtender Stern
    s = stern5(4.6)
    for k in range(10):
        w = math.pi / 2 + k * math.pi / 5 + math.pi / 10
        s += linie((5.4 * math.cos(w), 5.4 * math.sin(w)), (6.7 * math.cos(w), 6.7 * math.sin(w)), 1.2)
    return s

def zuckerfest():                    # Bonbon
    bonbon = CrossSection.circle(1, 64).scale([4.6, 3.6])
    streifen = sum((linie((x - 2, -4), (x + 2, 4), 0.9) for x in (-2.0, 0.6, 3.2)), CrossSection()) ^ bonbon.offset(-0.6)
    links = poly([(-4.2, 0), (-9.4, 3.8), (-9.4, -3.8)])
    rechts = poly([(4.2, 0), (9.4, 3.8), (9.4, -3.8)])
    return (bonbon - streifen) + links + rechts

def arafat():                        # Berg
    berg = poly([(-10, -5.6), (10, -5.6), (5.6, 0.6), (3.6, -1.0), (0, 5.4), (-4.6, -0.8), (-6.6, 0.8)])
    schnee = poly([(-1.3, 3.5), (1.4, 3.6), (0, 5.6)])
    return berg + schnee + CrossSection.circle(1.8, 32).translate([7.8, 4.6])     # Sonne

def opferfest():                     # Schaf
    wolle = sum((CrossSection.circle(r, 32).translate(p) for p, r in
                 [((-3.6, 0.4), 2.6), ((-1.0, 1.4), 2.8), ((1.8, 1.2), 2.6), ((-2.2, -1.6), 2.4), ((1.0, -1.4), 2.6)]),
                CrossSection())
    kopf = CrossSection.circle(1, 40).scale([2.2, 1.7]).rotate(-20).translate([5.4, 1.4])
    ohr = CrossSection.circle(1, 24).scale([1.4, 0.7]).rotate(30).translate([4.6, 3.2])
    beine = sum((CrossSection.square([1.4, 3.0]).translate([x, -6.0]) for x in (-3.8, -1.4, 0.6, 2.8)), CrossSection())
    auge = CrossSection.circle(0.55, 16).translate([5.8, 1.9])
    return wolle + kopf + ohr + beine - auge

def moschee():                       # Moschee-Silhouette
    kuppel = CrossSection.circle(4.0, 64).translate([0, 0.6]) ^ CrossSection.square([9, 5]).translate([-4.5, 0.6])
    spitze = poly([(-0.8, 4.4), (0.8, 4.4), (0, 6.4)])
    bau = CrossSection.square([10, 5.6]).translate([-5, -5.0])
    tuer = CrossSection.circle(1.4, 32).translate([0, -2.4]) + CrossSection.square([2.8, 2.6]).translate([-1.4, -5.1])
    minarette = CrossSection()
    for s in (1, -1):
        minarette += CrossSection.square([1.8, 11.2]).translate([s * 8.0 - 0.9, -5.0])
        minarette += poly([(s * 8.0 - 0.9, 6.2), (s * 8.0 + 0.9, 6.2), (s * 8.0, 7.6)])
    boden = CrossSection.square([20, 1.4]).translate([-10, -6.4])
    return (kuppel + spitze + bau - tuer + minarette + boden).scale([0.92, 0.92]).translate([0, 0.1])

# (Name, Funktion, Anzeigename, Datum 2027 – je nach Mondsichtung ±1 Tag)
TAGE = [
    ("isra_miraj", isra_miraj, "Isra und Miradsch (Nacht zum)", "5.1. und 25.12."),
    ("baraa", baraa, "Laylat al-Bara'a (Nacht zum)", "23.1."),
    ("ramadan", ramadan, "Beginn des Ramadan", "8.2."),
    ("qadr", qadr, "Laylat al-Qadr (Nacht zum)", "6.3."),
    ("zuckerfest", zuckerfest, "Zuckerfest / Eid al-Fitr", "9.3."),
    ("arafat", arafat, "Tag von Arafat", "15.5."),
    ("opferfest", opferfest, "Opferfest / Eid al-Adha", "16.5."),
    ("neujahr", neujahr, "Islamisches Neujahr (1449)", "6.6."),
    ("aschura", aschura, "Aschura", "15.6."),
    ("mawlid", mawlid, "Mawlid an-Nabi", "14.8."),
    ("moschee", moschee, "Moschee – frei verwendbar (z. B. Festgebet)", "–"),
]

def _m(f):
    return lambda: muster_cs(f)

PLATTEN = [Platte("4_Extra_Schubladen/schubladen_islamische_tage_11x.stl", [("i_" + k, _m(f)) for k, f, *_ in TAGE])]
