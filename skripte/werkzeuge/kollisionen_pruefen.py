"""Prüft für alle Länder, Bundesländer und Jahre (mit allen Kästchen im Konfigurator angehakt), ob es für jeden
Tag, an dem mehrere Motive zusammenfallen, eine Doppel-Schublade gibt. Fehlende Paare werden aufgelistet
(→ in daten/doppel_paare_N.json eintragen und alles neu erzeugen).
Die Feiertage werden mit daten/feiertage.js berechnet (wie im Konfigurator) – dafür wird Node.js gebraucht.
    python3 -m werkzeuge.kollisionen_pruefen            (2026–2030)
    python3 -m werkzeuge.kollisionen_pruefen 2026 2040
"""
import calendar
import collections
import json
import os
import subprocess
import sys
import pfade

GRUPPEN = ["gesetzlich", "feste", "jahreszeiten", "islamisch", "juedisch", "orthodox", "hindu", "laender", "international", "aktion"]
LAENDER = "BW BY BE BB HB HH HE MV NI NW RP SL SN ST SH TH".split()

def main():
    lade = lambda n: json.load(open(os.path.join(pfade.DATEN, n), encoding="utf-8"))
    ic, staaten = lade("motivliste.json"), lade("laender.json")["staaten"]
    von, bis = (int(sys.argv[1]), int(sys.argv[2])) if len(sys.argv) > 2 else (2026, 2030)
    js = os.path.join(pfade.DATEN, "feiertage.js").replace("\\", "/")
    code = f"const F=require({json.dumps(js)});const r={{}};for(let y={von};y<={bis};y++)r[y]=F.jahr(y);console.log(JSON.stringify(r))"
    ev = {"events": json.loads(subprocess.run(["node", "-e", code], capture_output=True, text=True, check=True).stdout)}
    kombi = set()
    for k in ic:
        if k.startswith("k_"):
            a, b = k[2:].split("__"); kombi |= {(a, b), (b, a)}
    k3 = [set(k[3:].split("__")) for k in ic if k.startswith("k3_")]
    fehlt = collections.defaultdict(set)
    for y, g in ev["events"].items():
        for st in staaten:
            for land in (LAENDER if st == "DE" else [None]):
                tage = {}
                for gid in GRUPPEN:
                    if gid == "gesetzlich":
                        rows = g.get("gesetzlich", []) if st == "DE" else g.get("gesetzlich_" + st, [])
                    else:
                        rows = [r for r in g.get(gid, []) if not (gid == "laender" and len(r) > 5 and r[5] == st)]
                    for r in rows:
                        d, k = r[0], r[1]
                        nur = r[2] if len(r) > 2 else None
                        if nur and land not in nur: continue
                        m, t = map(int, d.split("-"))
                        if t > calendar.monthrange(int(y), m)[1] or k not in ic: continue
                        tage.setdefault(d, [])
                        if k not in tage[d]: tage[d].append(k)
                for d, l in tage.items():
                    if len(l) < 2 or any(s <= set(l) for s in k3): continue
                    if any((l[i], l[j]) in kombi for i in range(len(l)) for j in range(i + 1, len(l))): continue
                    fehlt[(l[0], l[1])].add(f"{d}.{y} {st}")
    if not fehlt:
        print(f"Alles gut ({von}–{bis}): für jeden doppelten Tag gibt es eine Doppel-Schublade.")
    for (a, b), w in sorted(fehlt.items(), key=lambda x: -len(x[1])):
        print(f"fehlt: {a} + {b}   ({len(w)}×, z. B. {sorted(w)[0]})")

if __name__ == "__main__":
    main()
