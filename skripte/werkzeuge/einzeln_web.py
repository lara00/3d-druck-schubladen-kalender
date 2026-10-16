"""Einzelne Schubladen mit kurzen, festen Namen für den Konfigurator (index.html):
  zahl_01 … zahl_31, tag_001 … tag_366, wz_mo_01 … wz_su_31 (Zahl mit Wochentag),
  mz_jan_01 … mz_dec_31 (Zahl mit Monat)
  und <motiv-schlüssel>.stl (z. B. f_neujahr.stl), dazu die fertigen Module zum Mit-Herunterladen:
  modul_monat_de_01 … _12, modul_monat_en_01 … _12, modul_stimmungskalender, modul_lernkalender usw.
Der Konfigurator lädt diese Dateien und baut daraus die Druckplatten für deinen Kalender.
Ausführen (im Ordner skripte):  python3 -m werkzeuge.einzeln_web
"""
import glob
import os
import shutil
from werkzeuge import einzeln as e
from motive import wochentag_zahlen

ZIEL = os.path.join(e.BASIS, "einzeln")

def speichern(teil, name):
    t = teil.copy()
    lo, hi = t.bounds
    t.apply_translation([-(lo[0] + hi[0]) / 2, -(lo[1] + hi[1]) / 2, -lo[2]])
    t.export(os.path.join(ZIEL, name + ".stl"))

def main():
    os.makedirs(ZIEL, exist_ok=True)
    S2 = "1_Monatskalender/2_Schubladen/"
    n = 0
    for i, t in enumerate(e.teile(S2 + "schubladen_tag_01-31_12x_drucken.stl"), 1):
        speichern(t, f"zahl_{i:02d}"); n += 1
    k = 0
    for datei in sorted(os.listdir(os.path.join(e.BASIS, "4_Extra_Schubladen/tage_im_jahr"))):
        for t in e.teile("4_Extra_Schubladen/tage_im_jahr/" + datei):
            k += 1; speichern(t, f"tag_{k:03d}"); n += 1
    for wt in wochentag_zahlen.WOCHENTAGE:
        for i, t in enumerate(e.teile(f"{wochentag_zahlen.ORDNER}zahlen_{wt.lower()}_01-31.stl"), 1):
            speichern(t, f"wz_{wt.lower()}_{i:02d}"); n += 1
    for k, tage in wochentag_zahlen.MONATE:
        dn = wochentag_zahlen.datei_name(k)
        for i, t in enumerate(e.teile(f"{wochentag_zahlen.MONAT_ORDNER}zahlen_{dn}_01-{tage}.stl"), 1):
            speichern(t, f"mz_{dn}_{i:02d}"); n += 1
    for key, v in e.motivliste().items():
        speichern(e.teile(v["file"])[v["pos"] - 1], key); n += 1
    # fertige Module (unverändert kopiert, Originallage) – der Konfigurator gibt sie mit den Schubladen aus
    for sprache, ordner in (("de", "1_Module"), ("en", "1_Module_EN")):
        for i, datei in enumerate(sorted(glob.glob(os.path.join(e.BASIS, "1_Monatskalender", ordner, "*.stl"))), 1):
            shutil.copyfile(datei, os.path.join(ZIEL, f"modul_monat_{sprache}_{i:02d}.stl")); n += 1
    for ordner in ("5_Stimmungskalender", "6_Lernkalender"):
        for datei in glob.glob(os.path.join(e.BASIS, ordner, "*_modul*.stl")):
            shutil.copyfile(datei, os.path.join(ZIEL, "modul_" + os.path.basename(datei).replace("_modul", ""))); n += 1
    print(f"  Einzelteile für den Konfigurator: {n}")

if __name__ == "__main__":
    main()
