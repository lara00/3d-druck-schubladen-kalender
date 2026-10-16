# Skripte

Alle Druckdateien, die Motivliste und der Konfigurator werden aus diesen Python-Skripten erzeugt.

```bash
pip install -r requirements.txt
python3 alles_erzeugen.py                             # alles neu bauen (ca. 10 s) → ../stl und ../index.html
python3 -m werkzeuge.eigene_schublade "Oma" "♥" "42"  # eigene Schubladen → eigene_schubladen.stl
python3 -m werkzeuge.einzeln                          # alle Schubladen einzeln mit lesbaren Namen
python3 -m werkzeuge.kollisionen_pruefen              # fehlen Doppel-Schubladen?
```

Alle Befehle im Ordner `skripte` ausführen.

## Aufbau

| Ordner | Inhalt |
|---|---|
| `basis/` | **Grundlagen**: `grundlagen.py` (Fachmaß, Spiel, Schrift, Export), `kalender.py` (Modul, Nuten, Verbinder, Rastung, Schublade), `zeichnen.py` (Linie, Kreis, Bogen … für die Motive), `platten.py` (Druckplatten bauen) |
| `modelle/` | **Große Teile**: `monatskalender.py` (12 Module DE/EN, Platte 1–31, Verbinder), `abschlussleisten.py`, `testmodul.py`, `adventskalender.py`, `stimmungskalender.py`, `lernkalender.py`, `eigenes_modul.py` (Modul ohne Text + Buchstaben für „Eigenes Modul“) |
| `motive/` | **Motiv-Schubladen**, je Datei ein Thema: `muster_symbole`, `feiertage_deutschland`, `islamische_tage`, `welt_feiertage`, `laender_feiertage`, `termine_buchstaben_tage`, `sport_hobby_alltag`, `weitere_symbole`, `wochentag_zahlen`, `doppel_schubladen` |
| `werkzeuge/` | `motivliste_erzeugen`, `konfigurator_bauen`, `einzeln`, `einzeln_web`, `eigene_schublade`, `kollisionen_pruefen` |
| `daten/` | `motiv_namen.json` (Namen DE/EN), `feiertage.js` (berechnet die Feiertage für jedes Jahr), `laender.json`, `doppel_paare_1…4.json`, `konfigurator_vorlage.html`, `motivliste.json` (wird erzeugt) |
| `pfade.py` | wohin geschrieben wird (`../stl`, `../index.html`) |

## Wichtigste Stellschrauben (`basis/kalender.py`)

| Wert | Standard | Wirkung |
|---|---|---|
| `RAST_H` | 0.75 | Rastung (0.6 leichter / 0.9 fester) |
| `V_SPIEL` | 0.10 | Verbinder (0.05 stramm / 0.15 locker) |
| `TIEFE` | 48 | Tiefe von Modul und Schublade |

## Neues Motiv hinzufügen

1. In der passenden Datei in `motive/` eine Funktion schreiben, die die 2D-Form zurückgibt (Fläche x −13 … 13, y −7 … 7 mm, Linien ≥ 1,2 mm).
2. Sie in die Liste der Datei eintragen (z. B. `SPORT`) – dann landet sie automatisch auf der Platte (`PLATTEN`).
3. Namen in `daten/motiv_namen.json` eintragen (Schlüssel = Präfix + Name, z. B. `y_sport_rudern`).
4. `python3 alles_erzeugen.py` – fertig, auch im Konfigurator.

## Feiertage

Die Feiertage werden nicht gespeichert, sondern im Konfigurator für jedes Jahr ausgerechnet (`daten/feiertage.js`):
Ostern und alles, was daran hängt, orthodoxes Ostern, „n-ter Wochentag“-Regeln, Jahreszeiten und chinesisches Neujahr
(astronomisch nach Meeus), islamischer (Umm al-Qura) und jüdischer Kalender über den Browser. Nur Diwali, Holi und Vesakh
stehen als feste Daten drin (indischer Mondkalender). Die Doppel-Schubladen decken alle Überschneidungen 2026–2030 ab;
`python3 -m werkzeuge.kollisionen_pruefen 2026 2040` zeigt, was in späteren Jahren dazukäme (braucht Node.js).
