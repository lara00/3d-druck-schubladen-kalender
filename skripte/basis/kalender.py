"""Der Kalender selbst: Monatsmodul (6 × 6 Fächer + Kopfleiste), Nuten, Verbinder, Rastung und Schublade.
Hier stehen die wichtigsten Stellschrauben:
  RAST_H  = 0.75   Rastung (0.6 leichter / 0.9 fester)
  V_SPIEL = 0.10   Verbinder (0.05 stramm / 0.15 locker)
  TIEFE   = 48     Tiefe von Modul und Schublade
"""
from manifold3d import Manifold, CrossSection
from basis import grundlagen as gl
from basis.grundlagen import FACH_B, FACH_H, text_cs, text_cs_einzeln, stern, export

MONATE = [("JANUAR", 31), ("FEBRUAR", 28), ("MÄRZ", 31), ("APRIL", 30), ("MAI", 31), ("JUNI", 30),
          ("JULI", 31), ("AUGUST", 31), ("SEPTEMBER", 30), ("OKTOBER", 31), ("NOVEMBER", 30), ("DEZEMBER", 31)]
SPALTEN, REIHEN = 6, 6
TIEFE   = 48.0          # Regaltiefe (Advent: 48) – flacher spart viel Filament
RAND    = 4.0           # Außenwand (Platz für die Nuten)
STEG    = 1.4           # Trennwände = 2 Linien mit 0,6-mm-Düse
RUECKWAND = 1.2
KOPF    = 20.0          # Höhe der Kopfleiste
SCHRIFT_H = 11.0        # Höhe Monatsname
NUT_A, NUT_I, NUT_T = 5.0, 7.0, 2.5   # 1,5 mm Wand bleibt hinter der Nut
V_SPIEL, V_LEN = 0.10, TIEFE - 4  # Spiel pro Fläche; Verbinder 2 mm kürzer als das Modul
RIPPE_R = 0.3                     # Quetschrippen auf dem Verbinder (stehen 0,3 mm über)
RAST_Y  = 14.0          # Rastung: Abstand hinter der Schubladenfront
RAST_H  = 0.75          # Rippenhöhe (0,4 mm Luft → 0,35 mm Überdeckung pro Seite)
RAST_L  = 5.0           # Rippenlänge (oben im Fach, wo die Schubladenwand federt)
DT = TIEFE - RUECKWAND - 0.5   # Schubladenlänge
FB = FACH_B + STEG - 1         # Frontbreite (1 mm Fuge)
FH = FACH_H + STEG - 1         # Fronthöhe

B = 2 * RAND + SPALTEN * FACH_B + (SPALTEN - 1) * STEG
HF = 2 * RAND + REIHEN * FACH_H + (REIHEN - 1) * STEG     # Fachbereich
H = HF + KOPF

def fach_pos(sp, re):
    """linke untere Ecke des Fachs (Spalte sp, Reihe re; Reihe 0 = unten)."""
    return RAND + sp * (FACH_B + STEG) - B / 2, RAND + re * (FACH_H + STEG)

def fach_von_tag(k):
    """k = 0 … 35 → (Spalte, Reihe); Tag 1 oben links, zeilenweise."""
    return k % SPALTEN, REIHEN - 1 - k // SPALTEN

# ---- Grundmodul (ohne Namen) ------------------------------------------------
basis = CrossSection.square([B, H]).translate([-B / 2, 0]).extrude(TIEFE)
for sp in range(SPALTEN):
    for re in range(REIHEN):
        x, y = fach_pos(sp, re)
        basis -= CrossSection.square([FACH_B, FACH_H]).translate([x, y]).extrude(TIEFE).translate([0, 0, RUECKWAND])
# Kopfleiste von hinten aushöhlen (spart Material; Decke = 2 mm Front, kurze Brücke)
basis -= CrossSection.square([B - 2 * RAND, KOPF - 2 - (RAND - 0.5)]).translate([-B / 2 + RAND, HF - 2]).extrude(TIEFE - 2).translate([0, 0, -1])

nut = CrossSection([[(-NUT_A / 2, -0.01), (NUT_A / 2, -0.01), (NUT_I / 2, NUT_T), (-NUT_I / 2, NUT_T)]])
# je 4 Nuten pro Seite, mittig auf den Trennwänden (die mittlere Trennwand bleibt frei)
nx = [fach_pos(sp, 0)[0] + FACH_B + STEG / 2 for sp in (0, 1, 3, 4)]
ny = [fach_pos(0, re)[1] + FACH_H + STEG / 2 for re in (0, 1, 3, 4)]
def nuten(oben=True, unten=True, links=True, rechts=True):
    """Nuten nur an den Seiten, an denen ein Nachbarmodul anschließt."""
    n = []
    for x in nx:
        if unten:  n.append(nut.translate([x, 0]))
        if oben:   n.append(nut.rotate(180).translate([x, H]))
    for y in ny:
        if links:  n.append(nut.rotate(-90).translate([-B / 2, y]))
        if rechts: n.append(nut.rotate(90).translate([B / 2, y]))
    m = Manifold()
    for c in n:
        m += c.extrude(TIEFE + 2).translate([0, 0, -1])
    return m

RASTER_SPALTEN = 4      # Anordnung: Jan–Apr / Mai–Aug / Sep–Dez
# 4 × 3 Raster: 9 waagerechte + 8 senkrechte Kanten, je 4 Verbinder
VERBINDER_ANZAHL = (3 * (RASTER_SPALTEN - 1) + 2 * RASTER_SPALTEN) * 4

def nachbarn(k):
    """Für Monat k (0 = Januar): an welchen Seiten sitzt ein Nachbar?"""
    sp, re = k % RASTER_SPALTEN, k // RASTER_SPALTEN
    zeilen = (len(MONATE) + RASTER_SPALTEN - 1) // RASTER_SPALTEN
    return dict(oben=re > 0, unten=re < zeilen - 1, links=sp > 0, rechts=sp < RASTER_SPALTEN - 1)

# Rastrippen: 45°-Dreieck, je eine an der linken und rechten Fachwand, oben im Fach
_r = CrossSection([[(-0.01, -RAST_H - 0.01), (RAST_H, 0), (-0.01, RAST_H + 0.01)]]).extrude(RAST_L).rotate([90, 0, 0])
for sp in range(SPALTEN):
    for re in range(REIHEN):
        x, y = fach_pos(sp, re)
        oben = y + FACH_H - 2
        basis += _r.translate([x, oben, TIEFE - RAST_Y])
        basis += _r.mirror([1, 0, 0]).translate([x + FACH_B, oben, TIEFE - RAST_Y])

def modul(name, oben=True, unten=True, links=True, rechts=True, einzeln=False):
    """einzeln=True: Buchstaben einzeln vereinigen (für Namen mit überlappenden Buchstaben wie „KA“)."""
    tf = text_cs_einzeln if einzeln else text_cs
    cs = tf(name, SCHRIFT_H)
    x0, _, x1, _ = tf(name, SCHRIFT_H).bounds()          # an einer Kopie messen (lässt cs unverändert)
    if x1 - x0 > B - 2 * RAND - 16:                    # lange Namen (z. B. STIMMUNGSKALENDER) passend verkleinern
        k = (B - 2 * RAND - 16) / (x1 - x0)
        cs = cs.scale([k, k])
    txt = cs.translate([0, HF + KOPF / 2 - 1]).extrude(1.2).translate([0, 0, TIEFE - 0.01])
    return basis - nuten(oben, unten, links, rechts) + txt

# ---- Verbinder ---------------------------------------------------------------
def verbinder_mit(spiel=V_SPIEL, kerben=0):
    """Doppel-Schwalbenschwanz mit Quetschrippen (Stirnflächen + Schrägen).
    kerben = Anzahl Markierungskerben oben (für das Passungs-Test-Set)."""
    a, i, t = NUT_A - 2 * spiel, NUT_I - 2 * spiel, NUT_T - spiel
    prof = CrossSection([[(-a / 2, 0), (-i / 2, -t), (i / 2, -t), (a / 2, 0), (i / 2, t), (-i / 2, t)]])
    rippe = CrossSection.circle(RIPPE_R, 16)
    for s in (1, -1):
        prof += rippe.translate([0, s * t])                         # Mitte der Stirnfläche
        for sx in (1, -1):
            prof += rippe.translate([sx * (a + i) / 4, s * t / 2])  # Mitte jeder Schräge
    v = prof.extrude(V_LEN)
    for k in range(kerben):                                         # Markierung oben
        v -= Manifold.cube([0.9, 2 * t + 2, 1.6]).translate([(k - (kerben - 1) / 2) * 1.7 - 0.45 + 0.13, -t - 1, V_LEN - 1.6])
    return v

verbinder = verbinder_mit()

# ---- Schubladen ----------------------------------------------------
def schublade_mit(symbol_cs, laenge=DT, griff=True, wand=None):
    """Schublade mit Motiv (2D-Form) auf der Front, Rastschlitz und Griffleiste."""
    w = wand or gl.SW
    korpus = Manifold.cube([gl.DB, laenge, gl.DH]).translate([-gl.DB / 2, 0, 0])
    korpus -= Manifold.cube([gl.DB - 2 * w, laenge - 2 * w, gl.DH]).translate([-gl.DB / 2 + w, w, gl.SW])
    # Rastschlitz in beiden Seitenwänden (Gegenstück zur Rippe im Fach)
    z0 = FACH_H - 2 - RAST_L - gl.LUFT - 0.5
    korpus -= Manifold.cube([gl.DB + 2, 2.6, RAST_L + 1.0]).translate([-gl.DB / 2 - 1, RAST_Y - 1.3, z0])
    ft = gl.FRONT_T
    s = korpus + Manifold.cube([FB, ft, FH]).translate([-FB / 2, -ft, 0])
    if not symbol_cs.is_empty():
        s += symbol_cs.translate([0, 16.5 if griff else FH / 2]).extrude(0.9).rotate([90, 0, 0]).translate([0, -ft + 0.1, 0])
    if griff:
        g = CrossSection([[(-ft + 0.1, 2.5), (-ft + 0.1, 8), (-ft - 3.5, 8), (-ft - 3.5, 6)]])
        s += g.extrude(14).rotate([90, 0, 90]).translate([-7, 0, 0])
    return s

def schublade(n):
    return schublade_mit(text_cs(str(n), 11))

def platte(teile, spalten=6):
    p = Manifold()
    for k, s in enumerate(teile):
        p += s.translate([(k % spalten - (spalten - 1) / 2) * 36, (k // spalten) * 54, 0])
    return p

def in_modul(schub, sp, re):
    x, y = fach_pos(sp, re)
    return schub.rotate([-90, 0, 0]).translate([x + FACH_B / 2, y + gl.LUFT, TIEFE])
