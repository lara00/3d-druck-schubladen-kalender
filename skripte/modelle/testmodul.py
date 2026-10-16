"""Testmodul (2 × 2 Fächer, symmetrisch) zum Ausprobieren von Schubladen, Rastung, Verbindern und Rand,
bevor die großen Module gedruckt werden. Gleiche Maße und Toleranzen wie der Monatskalender.
"""
import os
from manifold3d import Manifold, CrossSection
from basis import kalender as mk
from basis.kalender import FACH_B, FACH_H, STEG, RUECKWAND, TIEFE, RAND, RAST_Y
from basis.grundlagen import export
from modelle.abschlussleisten import halbzapfen, flach, T

SP, RE = 2, 2
B = 2 * RAND + SP * FACH_B + (SP - 1) * STEG
H = 2 * RAND + RE * FACH_H + (RE - 1) * STEG

def fach_pos(sp, re):
    return RAND + sp * (FACH_B + STEG) - B / 2, RAND + re * (FACH_H + STEG)

test = CrossSection.square([B, H]).translate([-B / 2, 0]).extrude(TIEFE)
for sp in range(SP):
    for re in range(RE):
        x, y = fach_pos(sp, re)
        test -= CrossSection.square([FACH_B, FACH_H]).translate([x, y]).extrude(TIEFE).translate([0, 0, RUECKWAND])
        oben = y + FACH_H - 2
        test += mk._r.translate([x, oben, TIEFE - RAST_Y])
        test += mk._r.mirror([1, 0, 0]).translate([x + FACH_B, oben, TIEFE - RAST_Y])

# je eine Nut pro Seite, genau in der Mitte (auf der Trennwand) → alle vier Seiten gleich,
# Testmodule lassen sich in jeder Richtung verbinden
nx = fach_pos(0, 0)[0] + FACH_B + STEG / 2      # = 0
ny = fach_pos(0, 1)[1] - STEG / 2               # = H / 2
for prof, px, py in [(mk.nut, nx, 0), (mk.nut.rotate(180), nx, H),
                     (mk.nut.rotate(-90), -B / 2, ny), (mk.nut.rotate(90), B / 2, ny)]:
    test -= prof.translate([px, py]).extrude(TIEFE + 2).translate([0, 0, -1])

# ---- Rand fürs Testmodul (je ein halber Zapfen in der mittigen Nut) ----
def leiste(seite):
    if seite == "oben":
        return Manifold.cube([B, T, TIEFE]).translate([-B / 2, H, 0]) + halbzapfen(-1).translate([nx, H, 0])
    if seite == "unten":
        return Manifold.cube([B, T, TIEFE]).translate([-B / 2, -T, 0]) + halbzapfen(+1).translate([nx, 0, 0])
    if seite == "links":
        return Manifold.cube([T, H + 2 * T, TIEFE]).translate([-B / 2 - T, -T, 0]) + halbzapfen(-1).rotate([0, 0, 90]).translate([-B / 2, ny, 0])
    return Manifold.cube([T, H + 2 * T, TIEFE]).translate([B / 2, -T, 0]) + halbzapfen(+1).rotate([0, 0, 90]).translate([B / 2, ny, 0])

SEITEN = ["oben", "unten", "links", "rechts"]

def erzeugen(ziel):
    ordner = os.path.join(ziel, "3_Testmodul")
    os.makedirs(ordner, exist_ok=True)
    p = lambda n: os.path.join(ordner, n)
    export(test, p("testmodul_2x2.stl"))
    export(mk.platte([mk.schublade(n) for n in range(1, 13)]), p("test_schubladen_1-12.stl"))
    # Passungs-Test: 1 Kerbe = stramm (0,05), 2 = mittel (0,10, Standard), 3 = locker (0,15) – je 2 Stück
    vp = Manifold()
    for k, (spiel, kerben) in enumerate([(0.05, 1), (0.05, 1), (0.10, 2), (0.10, 2), (0.15, 3), (0.15, 3)]):
        vp += mk.verbinder_mit(spiel, kerben).translate([k * 13, 0, 0])
    export(vp, p("test_verbinder_passungen_6x.stl"))
    teile, y = Manifold(), 0.0                     # 4 Randleisten untereinander auf eine Platte
    for s in ["oben", "unten", "links", "rechts"]:
        l = flach(leiste(s), s)
        x0, y0, z0, x1, y1, z1 = l.bounding_box()
        teile += l.translate([0, y - y0, 0]); y += (y1 - y0) + 6
    export(teile, p("test_abschlussleisten_4x.stl"))
