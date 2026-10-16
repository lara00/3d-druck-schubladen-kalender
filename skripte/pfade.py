"""Wohin die Skripte schreiben (relativ zu diesem Ordner)."""
import os
HIER = os.path.dirname(os.path.abspath(__file__))
STL = os.path.normpath(os.path.join(HIER, "..", "stl"))          # alle Druckdateien
KONFIGURATOR = os.path.normpath(os.path.join(HIER, "..", "index.html"))
DATEN = os.path.join(HIER, "daten")
