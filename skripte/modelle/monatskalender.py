"""Monatskalender: 12 Monatsmodule (deutsch und englisch), Schubladen 1–31 und Verbinder.
Module auf dem Rücken liegend drucken (Monatsname oben). Die Platte 1–31 wird 12× gedruckt.
"""
import os
from manifold3d import Manifold
from basis import kalender as mk
from basis.grundlagen import export

MONATE_EN = ["JANUARY", "FEBRUARY", "MARCH", "APRIL", "MAY", "JUNE", "JULY", "AUGUST",
             "SEPTEMBER", "OCTOBER", "NOVEMBER", "DECEMBER"]
M = "1_Monatskalender/"

def erzeugen(ziel):
    def pfad(rel):
        p = os.path.join(ziel, rel); os.makedirs(os.path.dirname(p), exist_ok=True); return p
    for k, (name, _) in enumerate(mk.MONATE):
        export(mk.modul(name), pfad(f"{M}1_Module/modul_{k + 1:02d}_{name.replace('Ä', 'AE').lower()}.stl"))
    for k, name in enumerate(MONATE_EN):
        export(mk.modul(name), pfad(f"{M}1_Module_EN/module_{k + 1:02d}_{name.lower()}.stl"))
    # alle Tage 1–31 auf einer Platte (7 × 5, ca. 25 × 27 cm) – für den ganzen Kalender 12× drucken
    export(mk.platte([mk.schublade(n) for n in range(1, 32)], spalten=7), pfad(f"{M}2_Schubladen/schubladen_tag_01-31_12x_drucken.stl"))
    vp = Manifold()
    for k in range(mk.VERBINDER_ANZAHL):
        vp += mk.verbinder.translate([(k % 10 - 4.5) * 14, (k // 10) * 12, 0])
    export(vp, pfad(f"{M}3_Verbinder/verbinder_{mk.VERBINDER_ANZAHL}x.stl"))
