"""Druckplatten aus Motiven bauen. Jedes Motiv-Skript beschreibt seine Platten als Liste:
    Platte(datei, [(schlüssel, form), ...], spalten)
schlüssel = Name des Motivs (für Konfigurator und Einzelteile, None = ohne Namen),
form      = Funktion, die die 2D-Form für die Schubladenfront liefert.
"""
import os
from dataclasses import dataclass, field
from basis import kalender as mk
from basis.grundlagen import export

@dataclass
class Platte:
    datei: str                       # Pfad relativ zum stl-Ordner
    teile: list = field(default_factory=list)
    spalten: int = 6                 # Schubladen nebeneinander (Raster 36 × 54 mm)

def bauen(platte, ziel):
    """Platte als STL in den Zielordner schreiben, gibt das trimesh-Objekt zurück."""
    pfad = os.path.join(ziel, platte.datei)
    os.makedirs(os.path.dirname(pfad), exist_ok=True)
    teile = [mk.schublade_mit(form()) for _, form in platte.teile]
    return export(mk.platte(teile, platte.spalten), pfad)
