# 3D-Druck Schubladen-Kalender

<!-- TODO: Foto vom echten Kalender einfügen, z. B. bilder/foto_kalender.jpg -->
![Kalender mit 365 Schubladen](bilder/kalender_3d.png)

Ein Wandkalender mit **365 Schubladen**, eine für jeden Tag. 12 Monatsmodule (je 6 × 6 Fächer) werden zusammengesteckt,
die Schubladen rasten ein. Dazu über 400 Motiv-Schubladen und ein Konfigurator im Browser.

## Konfigurator

**[Konfigurator öffnen](https://lara00.github.io/3d-druck-schubladen-kalender/)**: Land wählen, Feiertage einsetzen, Fächer
anpassen, und dann **STL-Dateien für den eigenen Kalender** herunterladen, eine Druckplatte pro Monat. Läuft komplett im Browser.

## Drucken

| Teil | Datei | Anzahl |
|---|---|---|
| Monatsmodule | `stl/1_Monatskalender/1_Module/` | je 1× |
| Schubladen 1–31 | `schubladen_tag_01-31_12x_drucken.stl` | 12× |
| Verbinder | `verbinder_68x.stl` | 1× |
| Extra-Schubladen | `stl/4_Extra_Schubladen/` | nach Wunsch |
| Stimmungskalender (eigenständig) | `stl/5_Stimmungskalender/` | [Druckliste](stl/5_Stimmungskalender/DRUCKLISTE.txt) |
| Lernkalender (eigenständig) | `stl/6_Lernkalender/` | [Druckliste](stl/6_Lernkalender/DRUCKLISTE.txt) |

Getestet mit Prusa CORE One L, 0,6-mm-Düse, PLA, ohne Stützmaterial. Zum Ausprobieren gibt es ein Testmodul in `stl/3_Testmodul/`.
Genaue Liste: [`DRUCKLISTE.txt`](stl/1_Monatskalender/DRUCKLISTE.txt)

## Skripte

```bash
cd skripte && pip install -r requirements.txt
python3 alles_erzeugen.py                              # alles neu bauen
python3 -m werkzeuge.eigene_schublade "Oma" "♥" "42"   # eigene Schubladen
```

# Kalender – Druckzeit & Materialbedarf
 
Grobe Hochrechnung auf Basis der PrusaSlicer-Werte (Stand 12.10.2026).
 
## Druckeinstellungen
 
| | |
|---|---|
| Drucker | Prusa CORE One L, Düse 0,6 mm |
| Profil | 0.32mm STRUCTURAL |
| Filament | Sunlu PLA |
| Infill | 20 % |
| Stützen | nur für Stützverstärker |
 
## Einzelteile (laut Slicer)
 
| Teil | Datei | Größe (mm) | Druckzeit | Filament |
|---|---|---|---|---|
| Monatsmodul | `modul_01_januar.stl` | 207 × 191 × 49,2 | 9 h 39 min | 366,1 g |
| Schublade | `bg_3.stl` | 32,4 × 51,8 × 26,4 | 23 min | 9,4 g |
| Leiste | `leiste_rechts_mitte.stl` | 48 × 191 × 5,2 | 37 min | 30,2 g |
| Verbinder (68 Stück, 1 Platte) | `verbinder_68x.stl` | 132,8 × 77,4 × 44 | 4 h 16 min | 85,8 g |
 
## Hochrechnung: 12 Module à 6 × 6 Schubladen
 
| Teil | Anzahl | Druckzeit | Filament |
|---|---|---|---|
| Monatsmodule | 12 | 115 h 48 min | 4,39 kg |
| Schubladen | 432 (12 × 36) | 165 h 36 min | 4,06 kg |
| Verbinder | 68 | 4 h 16 min | 0,09 kg |
| **Summe** | | **≈ 286 h (≈ 11,9 Tage Dauerdruck)** | **≈ 8,54 kg** |
 
Die Leisten sind nicht eingerechnet, weil die Anzahl noch offen ist. Pro Leiste kommen ca. 37 min und 30 g dazu.

## Adventskalender (24 Türchen)
 
| Teil | Datei | Größe (mm) | Druckzeit | Filament |
|---|---|---|---|---|
| Regal | `advent_regal.stl` | Höhe 47,9 | 5 h 23 min | 224,1 g |
| 24 Schubladen (1 Platte) | `advent_schubladen_1-24.stl` | 212,4 × 213,8 × 26,4 | 6 h 15 min | 223,3 g |
| **Summe** | | | **11 h 38 min** | **≈ 0,45 kg** |

**Lizenz:** [CC BY-NC 4.0](LICENSE): nachdrucken und verändern erlaubt, mit Namensnennung, nicht kommerziell.

<sub>Konstruktion und Code mit KI-Unterstützung (Claude)</sub>