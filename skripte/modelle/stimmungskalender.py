"""Stimmungskalender: eigenständiger Kalender für einen Monat → ../stl/5_Stimmungskalender/
- Modul 6 × 6 mit „STIMMUNGSKALENDER“ (englisch „MOOD CALENDAR“), ohne Nuten (steht allein) oder mit Nuten
- Platte 1–31 für den Start; die 5 Stimmungs-Schubladen kommen aus motive/weitere_symbole.py (gleicher Ordner)
"""
import os
from basis import kalender as mk
from basis.grundlagen import export

ORDNER = "5_Stimmungskalender/"
NAMEN = [("STIMMUNGSKALENDER", "stimmungskalender"), ("MOOD CALENDAR", "mood_calendar")]

def module(ziel, ordner, namen):
    """Modul je Name ohne und mit Nuten, dazu die Platte 1–31."""
    os.makedirs(os.path.join(ziel, ordner), exist_ok=True)
    for text, datei in namen:
        export(mk.modul(text, False, False, False, False, einzeln=True), os.path.join(ziel, ordner, f"{datei}_modul.stl"))
        export(mk.modul(text, einzeln=True), os.path.join(ziel, ordner, f"{datei}_modul_mit_nuten.stl"))
    export(mk.platte([mk.schublade(n) for n in range(1, 32)], spalten=7), os.path.join(ziel, ordner, "schubladen_tag_01-31.stl"))

def erzeugen(ziel):
    module(ziel, ORDNER, NAMEN)
