"""Alle Schubladen als einzelne STL-Dateien (eine Datei pro Schublade), sortiert nach Kategorie.
Holt die Teile aus den fertigen Druckplatten, damit sie exakt gleich sind.
Ausführen (im Ordner skripte):  python3 -m werkzeuge.einzeln   → ../einzelne_schubladen/
"""
import json, os, re, sys
import numpy as np, trimesh

import pfade
BASIS = pfade.STL
ZIEL = os.path.join(pfade.HIER, "..", "einzelne_schubladen")
def motivliste():
    with open(os.path.join(pfade.DATEN, "motivliste.json"), encoding="utf-8") as f:
        return json.load(f)

_cache = {}
def teile(datei):
    """Platte in Einzelteile zerlegen, Reihenfolge wie beim Erzeugen: Reihe für Reihe, links → rechts."""
    if datei not in _cache:
        ps = trimesh.load(os.path.join(BASIS, datei)).split(only_watertight=True)
        ps = sorted(ps, key=lambda p: p.bounds[0][1])
        reihen, akt = [], [ps[0]]
        for p in ps[1:]:
            if p.bounds[0][1] - akt[0].bounds[0][1] > 5: reihen.append(akt); akt = [p]
            else: akt.append(p)
        reihen.append(akt)
        _cache[datei] = [p for r in reihen for p in sorted(r, key=lambda p: p.bounds[0][0])]
    return _cache[datei]

def sauber(s):
    """Nur einfache Zeichen in Datei- und Ordnernamen (keine Umlaute, kein ß, keine Sonderzeichen)."""
    import unicodedata
    for a, b in {"ä": "ae", "ö": "oe", "ü": "ue", "Ä": "Ae", "Ö": "Oe", "Ü": "Ue", "ß": "ss",
                 "&": " und ", "+": " und ", "/": "-", ":": " -", "–": "-", "’": "", "'": ""}.items():
        s = s.replace(a, b)
    s = unicodedata.normalize("NFKD", s).encode("ascii", "ignore").decode()   # é → e, Rest weg
    s = re.sub(r"[^A-Za-z0-9 ()._-]", "", s)
    return re.sub(r"\s+", " ", s).strip(" .")

def speichern(teil, ordner, name, schon):
    os.makedirs(os.path.join(ZIEL, ordner), exist_ok=True)
    n, i = name, 2
    while (ordner, n.lower()) in schon: n = f"{name} ({i})"; i += 1
    schon.add((ordner, n.lower()))
    t = teil.copy()
    lo, hi = t.bounds
    t.apply_translation([-(lo[0] + hi[0]) / 2, -(lo[1] + hi[1]) / 2, -lo[2]])
    t.export(os.path.join(ZIEL, ordner, n + ".stl"))

def main():
    schon, anzahl = set(), 0
    S2 = "1_Monatskalender/2_Schubladen/"
    # Zahlen 1–31
    for n, t in enumerate(teile(S2 + "schubladen_tag_01-31_12x_drucken.stl"), 1):
        speichern(t, "01 Zahlen 1-31", f"{n:02d}", schon); anzahl += 1
    # Tag im Jahr 1–366
    n = 0
    for datei in sorted(os.listdir(os.path.join(BASIS, "4_Extra_Schubladen/tage_im_jahr"))):
        for t in teile("4_Extra_Schubladen/tage_im_jahr/" + datei):
            n += 1
            speichern(t, "02 Tag im Jahr 1-366", f"{n:03d}", schon); anzahl += 1
    # Zahlen mit Wochentag
    from motive import wochentag_zahlen
    for wt in wochentag_zahlen.WOCHENTAGE:
        for n, t in enumerate(teile(f"{wochentag_zahlen.ORDNER}zahlen_{wt.lower()}_01-31.stl"), 1):
            speichern(t, "02 Zahlen mit Wochentag", f"{wt} {n:02d}", schon); anzahl += 1
    for k, tage in wochentag_zahlen.MONATE:
        dn = wochentag_zahlen.datei_name(k)
        for n, t in enumerate(teile(f"{wochentag_zahlen.MONAT_ORDNER}zahlen_{dn}_01-{tage}.stl"), 1):
            speichern(t, "02 Zahlen mit Monat", f"{sauber(k)} {n:02d}", schon); anzahl += 1
    # alle Motive aus der Motivliste
    reihenfolge = []
    for k, v in motivliste().items():
        if v["cat"] not in reihenfolge: reihenfolge.append(v["cat"])
    for k, v in motivliste().items():
        nr = reihenfolge.index(v["cat"]) + 3
        speichern(teile(v["file"])[v["pos"] - 1], f"{nr:02d} {sauber(v['cat'])}", sauber(v["name"]), schon); anzahl += 1
    print("Einzelne Schubladen:", anzahl)

if __name__ == "__main__":
    main()
