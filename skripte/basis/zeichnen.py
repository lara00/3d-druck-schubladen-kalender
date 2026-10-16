"""Zeichen-Werkzeuge für die Motive (2D-Formen) und die Standard-Druckplatte.
Motivfläche auf der Schublade: x −13 … 13, y −7 … 7 mm (über der Griffleiste).
Linien mindestens 1,2 mm breit, damit sie mit einer 0,6-mm-Düse sauber drucken.
"""
import math
from manifold3d import CrossSection
from basis import grundlagen as gl
from basis import kalender as mk

W, H = 13.0, 7.0                          # halbe Breite/Höhe der Motivfläche
FELD = CrossSection.square([2 * W, 2 * H], center=True)
L = 1.3                                   # Standard-Linienbreite

C = lambda r, x=0, y=0, n=40: CrossSection.circle(r, n).translate([x, y])                         # Kreis
E = lambda rx, ry, x=0, y=0, w=0: CrossSection.circle(1, 48).scale([rx, ry]).rotate(w).translate([x, y])  # Ellipse
R = lambda w, h, x=0, y=0: CrossSection.square([w, h]).translate([x, y])                          # Rechteck (linke untere Ecke)
RC = lambda w, h, x=0, y=0, a=0: CrossSection.square([w, h], center=True).rotate(a).translate([x, y])  # Rechteck (Mitte)

def linie(p1, p2, b=L):
    """Linie von p1 nach p2 mit runden Enden, Breite b."""
    (x1, y1), (x2, y2) = p1, p2
    n = math.hypot(x2 - x1, y2 - y1)
    ox, oy = -(y2 - y1) / n * b / 2, (x2 - x1) / n * b / 2
    s = CrossSection([[(x1 - ox, y1 - oy), (x2 - ox, y2 - oy), (x2 + ox, y2 + oy), (x1 + ox, y1 + oy)]])
    return s + CrossSection.circle(b / 2, 12).translate([x1, y1]) + CrossSection.circle(b / 2, 12).translate([x2, y2])

def ring(r, b=L):
    return CrossSection.circle(r, 48) - CrossSection.circle(r - b, 48)

def poly(pts):
    """Polygon unabhängig von der Punkt-Reihenfolge."""
    cs = CrossSection([pts])
    return cs if cs.area() > 0 else CrossSection([pts[::-1]])

def tropfen(cx, cy, r, spitze_y):
    return CrossSection.batch_hull([CrossSection.circle(r, 32).translate([cx, cy]),
                                    CrossSection.square([0.05, 0.05], center=True).translate([cx, spitze_y])])

def stern5(r, x=0, y=0):
    return gl.stern(r, r * 0.45).translate([x, y])

def bogen(r, a0, a1, b, x=0, y=0, n=24):
    """Kreisbogen von a0 bis a1 Grad als Linie mit Breite b."""
    s = CrossSection()
    pts = [(x + r * math.cos(math.radians(a0 + (a1 - a0) * k / n)), y + r * math.sin(math.radians(a0 + (a1 - a0) * k / n))) for k in range(n + 1)]
    for p, q in zip(pts, pts[1:]): s += linie(p, q, b)
    return s

def muster_cs(f):
    """Motiv auf die Motivfläche zuschneiden."""
    return f() ^ FELD

def muster_schublade(f):
    return mk.schublade_mit(muster_cs(f))

def leer_schublade():
    return mk.schublade_mit(CrossSection())
