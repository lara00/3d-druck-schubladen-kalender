"""Abschlussleisten für den Monatskalender (4 × 3 Module): glatter Rand rundherum.
Halbe Schwalbenschwanz-Zapfen (mit Quetschrippen) greifen in die äußeren Nuten. Die linken/rechten
Eckleisten sind um die Leistendicke länger und schließen die Ecken. Flach drucken, Sichtseite unten.
"""
import os
from manifold3d import Manifold
from basis import kalender as mk
from basis.kalender import B, H, TIEFE
from basis.grundlagen import export

T = 2.5                          # Leistendicke

def halbzapfen(richtung):
    """Halber Verbinder, der von der Außenfläche (y=0) in Richtung 'richtung' (-1/+1) in die Nut ragt."""
    v = mk.verbinder_mit()
    if richtung < 0:
        h = v ^ Manifold.cube([20, 10.3, 100]).translate([-10, -10, -1])     # y ≤ 0.3
    else:
        h = v ^ Manifold.cube([20, 10.3, 100]).translate([-10, -0.3, -1])    # y ≥ -0.3
    return h.translate([0, 0, 2])                                             # mittig in der Tiefe

def leiste(seite, y0=0.0, y1=H):
    """Leiste in Modul-Koordinaten. seite: oben/unten/links/rechts; y0/y1 nur für links/rechts."""
    if seite == "oben":
        l = Manifold.cube([B, T, TIEFE]).translate([-B / 2, H, 0])
        for x in mk.nx: l += halbzapfen(-1).translate([x, H, 0])
    elif seite == "unten":
        l = Manifold.cube([B, T, TIEFE]).translate([-B / 2, -T, 0])
        for x in mk.nx: l += halbzapfen(+1).translate([x, 0, 0])
    elif seite == "links":
        l = Manifold.cube([T, y1 - y0, TIEFE]).translate([-B / 2 - T, y0, 0])
        for y in mk.ny: l += halbzapfen(-1).rotate([0, 0, 90]).translate([-B / 2, y, 0])
    else:
        l = Manifold.cube([T, y1 - y0, TIEFE]).translate([B / 2, y0, 0])
        for y in mk.ny: l += halbzapfen(+1).rotate([0, 0, 90]).translate([B / 2, y, 0])
    return l

def flach(l, seite):
    """Sichtseite nach unten aufs Bett legen."""
    rot = {"oben": [-90, 0, 0], "unten": [90, 0, 0], "links": [0, -90, 0], "rechts": [0, 90, 0]}[seite]
    l = l.rotate(rot)
    (x0, y0, z0, x1, y1, z1) = l.bounding_box()
    return l.translate([-(x0 + x1) / 2, -(y0 + y1) / 2, -z0])

TEILE = [  # (Dateiname, Seite, y0, y1, Anzahl, wofür)
    ("leiste_oben_unten_8x", "oben", 0, H, 8, "oben über Jan–Apr und (umgedreht) unten unter Sep–Dez"),
    ("leiste_links_oben_ecke", "links", 0, H + T, 1, "links an Januar"),
    ("leiste_links_mitte", "links", 0, H, 1, "links an Mai"),
    ("leiste_links_unten_ecke", "links", -T, H, 1, "links an September"),
    ("leiste_rechts_oben_ecke", "rechts", 0, H + T, 1, "rechts an April"),
    ("leiste_rechts_mitte", "rechts", 0, H, 1, "rechts an August"),
    ("leiste_rechts_unten_ecke", "rechts", -T, H, 1, "rechts an Dezember"),
]

def erzeugen(ziel):
    ordner = os.path.join(ziel, "1_Monatskalender/4_Abschlussleisten")
    os.makedirs(ordner, exist_ok=True)
    for name, seite, y0, y1, n, wo in TEILE:
        export(flach(leiste(seite, y0, y1), seite), os.path.join(ordner, name + ".stl"))
