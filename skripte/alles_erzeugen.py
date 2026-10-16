"""Erzeugt alles neu: alle STL-Dateien, die Motivliste, die Einzelteile für den Konfigurator und den Konfigurator.
    python3 alles_erzeugen.py            (dauert ca. 30 Sekunden)
    python3 alles_erzeugen.py nur-stl    (nur die Druckdateien)
Die Dateien landen direkt in ../stl in der fertigen Ordnerstruktur.
"""
import sys
import time
import pfade
from basis.platten import bauen
from modelle import monatskalender, abschlussleisten, testmodul, adventskalender, stimmungskalender, lernkalender, eigenes_modul
from motive import (muster_symbole, feiertage_deutschland, islamische_tage, welt_feiertage,
                    laender_feiertage, termine_buchstaben_tage, sport_hobby_alltag, weitere_symbole, wochentag_zahlen,
                    doppel_schubladen)

MODELLE = [monatskalender, abschlussleisten, testmodul, adventskalender, stimmungskalender, lernkalender, eigenes_modul]
MOTIVE = [muster_symbole, feiertage_deutschland, islamische_tage, welt_feiertage,
          laender_feiertage, termine_buchstaben_tage, sport_hobby_alltag, weitere_symbole, wochentag_zahlen,
          doppel_schubladen]

def stl_erzeugen(ziel=pfade.STL):
    for m in MODELLE:
        m.erzeugen(ziel)
        print(f"  {m.__name__.split('.')[-1]:28s} fertig")
    for m in MOTIVE:
        for p in m.PLATTEN:
            t = bauen(p, ziel)
            if not t.is_watertight:
                sys.exit(f"Fehler: {p.datei} ist nicht geschlossen")
        print(f"  {m.__name__.split('.')[-1]:28s} {len(m.PLATTEN):2d} Platten")

if __name__ == "__main__":
    t0 = time.time()
    print("Druckdateien →", pfade.STL)
    stl_erzeugen()
    if "nur-stl" not in sys.argv:
        from werkzeuge import motivliste_erzeugen, einzeln_web, konfigurator_bauen
        motivliste_erzeugen.main()
        einzeln_web.main()
        konfigurator_bauen.main()
    print(f"Fertig in {time.time() - t0:.0f} s")
