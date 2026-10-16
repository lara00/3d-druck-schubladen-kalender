"""Adventskalender: Regal mit 6 × 4 Fächern und Schubladen 1–24, gleiche Fächer, Rastung und Schubladen
wie der Monatskalender. Regal auf dem Rücken liegend drucken, ohne Stützmaterial.
"""
import os
from manifold3d import CrossSection
from basis import kalender as mk
from basis import grundlagen as gl
from basis.kalender import FACH_B, FACH_H, STEG, RUECKWAND, TIEFE, RAST_Y
from basis.grundlagen import export

SP, RE = 6, 4
RAND = 3.0                      # keine Nuten nötig → dünnere Außenwand
B = 2 * RAND + SP * FACH_B + (SP - 1) * STEG
H = 2 * RAND + RE * FACH_H + (RE - 1) * STEG

def fach_pos(sp, re):
    return RAND + sp * (FACH_B + STEG) - B / 2, RAND + re * (FACH_H + STEG)

regal = CrossSection.square([B, H]).translate([-B / 2, 0]).extrude(TIEFE)
for sp in range(SP):
    for re in range(RE):
        x, y = fach_pos(sp, re)
        regal -= CrossSection.square([FACH_B, FACH_H]).translate([x, y]).extrude(TIEFE).translate([0, 0, RUECKWAND])
        oben = y + FACH_H - 2
        regal += mk._r.translate([x, oben, TIEFE - RAST_Y])
        regal += mk._r.mirror([1, 0, 0]).translate([x + FACH_B, oben, TIEFE - RAST_Y])

def in_regal(schub, sp, re):
    x, y = fach_pos(sp, re)
    return schub.rotate([-90, 0, 0]).translate([x + FACH_B / 2, y + gl.LUFT, TIEFE])

def fach_von_tag(n):
    """Tag 1 oben links, zeilenweise."""
    k = n - 1
    return k % SP, RE - 1 - k // SP

def erzeugen(ziel):
    ordner = os.path.join(ziel, "2_Adventskalender")
    os.makedirs(ordner, exist_ok=True)
    export(regal, os.path.join(ordner, "advent_regal.stl"))
    export(mk.platte([mk.schublade(n) for n in range(1, 25)]), os.path.join(ordner, "advent_schubladen_1-24.stl"))
