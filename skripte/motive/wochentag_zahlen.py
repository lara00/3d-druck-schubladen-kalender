"""Zahlen mit Kürzel darüber, je Kürzel eine Platte:
- Wochentag (z. B. „MO“ über „13“): Zahlen 1–31 je Wochentag. Deutsch MO … SO, englisch zusätzlich TU WE TH SU
  (MO, FR, SA sind gleich). Passt nur für ein bestimmtes Jahr – der Konfigurator sucht die richtigen heraus.
- Monat (z. B. „JAN“ über „13“): je Monat seine Tage (Februar mit 29). Deutsch JAN … DEZ, englisch zusätzlich
  MAR MAY OCT DEC. Passt jedes Jahr.
"""
from matplotlib.textpath import TextPath
from manifold3d import CrossSection, FillRule
from basis import grundlagen as gl
from basis.platten import Platte

WOCHENTAGE = ["MO", "DI", "MI", "DO", "FR", "SA", "SO", "TU", "WE", "TH", "SU"]
ORDNER = "4_Extra_Schubladen/wochentag_zahlen/"

def wochentag_zahl_cs(wt, n):
    oben = gl.text_cs(wt, 4.6).translate([0, 4.4])
    unten = gl.text_cs(str(n), 7.4).translate([0, -3.0])
    return oben + unten

PLATTEN = [Platte(f"{ORDNER}zahlen_{wt.lower()}_01-31.stl",
                  [(None, lambda wt=wt, n=n: wochentag_zahl_cs(wt, n)) for n in range(1, 32)], 7)
           for wt in WOCHENTAGE]

MONATE = [("JAN", 31), ("FEB", 29), ("MÄR", 31), ("APR", 30), ("MAI", 31), ("JUN", 30), ("JUL", 31), ("AUG", 31),
          ("SEP", 30), ("OKT", 31), ("NOV", 30), ("DEZ", 31), ("MAR", 31), ("MAY", 31), ("OCT", 31), ("DEC", 31)]
MONAT_ORDNER = "4_Extra_Schubladen/monat_zahlen/"

def datei_name(kuerzel):
    return kuerzel.lower().replace("ä", "ae")

def kuerzel_cs(txt, cap=4.2, grundlinie=2.5):
    """Text mit fester Großbuchstaben-Höhe auf einer Grundlinie (Umlaut-Punkte und J dürfen herausragen)."""
    groesse = cap / 0.729                                # DejaVu Sans Bold: Großbuchstaben = 0,729 × Schriftgröße
    tp = TextPath((0, 0), txt, size=groesse, prop=gl.SCHRIFT)
    cs = CrossSection([[tuple(pt) for pt in p] for p in tp.to_polygons() if len(p) > 2], FillRule.EvenOdd)
    x0, _, x1, _ = cs.bounds()
    return cs.translate([-(x0 + x1) / 2, grundlinie])

def monat_zahl_cs(kuerzel, n):
    return kuerzel_cs(kuerzel) + gl.text_cs(str(n), 7.2).translate([0, -3.3])

PLATTEN += [Platte(f"{MONAT_ORDNER}zahlen_{datei_name(k)}_01-{tage}.stl",
                   [(None, lambda k=k, n=n: monat_zahl_cs(k, n)) for n in range(1, tage + 1)], 7)
            for k, tage in MONATE]
