"""Lernkalender: eigenständiger Kalender für einen Monat → ../stl/6_Lernkalender/
- Modul 6 × 6 mit „LERNKALENDER“ (englisch „STUDY CALENDAR“), ohne Nuten (steht allein) oder mit Nuten
- Platte 1–31 für den Start; die Stunden-Schubladen kommen aus motive/weitere_symbole.py (gleicher Ordner)
"""
from modelle.stimmungskalender import module

ORDNER = "6_Lernkalender/"
NAMEN = [("LERNKALENDER", "lernkalender"), ("STUDY CALENDAR", "study_calendar")]

def erzeugen(ziel):
    module(ziel, ORDNER, NAMEN)
