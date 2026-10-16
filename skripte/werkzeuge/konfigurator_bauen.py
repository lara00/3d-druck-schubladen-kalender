"""Baut den Konfigurator (eine einzige HTML-Datei) aus der Vorlage und den Daten zusammen:
daten/konfigurator_vorlage.html + motivliste.json + laender.json + schrift.json + feiertage.js → ../index.html
Dazu die Bausteine für Module (Modul ohne Text, Buchstaben) aus ../stl/einzeln, komprimiert eingebettet –
so lassen sich Module auch ohne den Ordner „einzeln“ erzeugen.
    python3 -m werkzeuge.konfigurator_bauen
"""
import base64
import glob
import gzip
import json
import os
import pfade

def bausteine():
    teile = {}
    for pfad in sorted(glob.glob(os.path.join(pfade.STL, "einzeln", "modul_leer*.stl")) + glob.glob(os.path.join(pfade.STL, "einzeln", "zeichen_*.stl"))):
        with open(pfad, "rb") as f:
            teile[os.path.basename(pfad)[:-4]] = base64.b64encode(gzip.compress(f.read(), 9, mtime=0)).decode()
    assert "modul_leer" in teile and "zeichen_0041" in teile, "erst alles_erzeugen.py laufen lassen"
    return json.dumps(teile)

def main(ziel=pfade.KONFIGURATOR):
    def lies(n):
        with open(os.path.join(pfade.DATEN, n), encoding="utf-8") as f:
            return f.read().replace("</", "<\\/")          # darf das <script>-Element nicht beenden
    with open(os.path.join(pfade.DATEN, "konfigurator_vorlage.html"), encoding="utf-8") as f:
        h = f.read()
    for sid, datei in [("icons", "motivliste.json"), ("events", "laender.json"), ("schrift", "schrift.json")]:
        alt = f'<script id="{sid}" type="application/json">…</script>'
        assert alt in h, sid
        h = h.replace(alt, f'<script id="{sid}" type="application/json">{lies(datei)}</script>', 1)
    alt = '<script id="bausteine" type="application/json">…</script>'
    assert alt in h
    h = h.replace(alt, f'<script id="bausteine" type="application/json">{bausteine()}</script>', 1)
    with open(os.path.join(pfade.DATEN, "feiertage.js"), encoding="utf-8") as f:
        js = f.read()
    assert "</script" not in js
    h = h.replace("<script>…FEIERTAGE_JS…</script>", "<script>\n" + js + "</script>", 1)
    with open(ziel, "w", encoding="utf-8") as f:
        f.write(h)
    print(f"  Konfigurator: {os.path.basename(ziel)} ({len(h) // 1024} KB)")

if __name__ == "__main__":
    main()
