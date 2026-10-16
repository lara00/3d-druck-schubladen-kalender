"""Weitere Tage auf vier Platten: Religionen, Länder & regional, internationale Tage, lustige Aktionstage.
"""
import math
from manifold3d import CrossSection
from basis import grundlagen as gl
from basis.zeichnen import C, E, R, RC, linie, ring, poly, tropfen, stern5, bogen, muster_cs
from basis.platten import Platte

def herz(s=1.0, x=0, y=0):
    h = CrossSection.batch_hull([C(2.6 * s, -2.1 * s, 1.4 * s), C(0.05, 0, -4.6 * s)]) + \
        CrossSection.batch_hull([C(2.6 * s, 2.1 * s, 1.4 * s), C(0.05, 0, -4.6 * s)])
    return h.translate([x, y])

# ======================= 1. Religionen =======================
def apfel():          # Rosch ha-Schana: Apfel (mit Honig)
    a = C(4.6, -1.6, -1.2) + C(4.6, 1.6, -1.2) + C(4.0, 0, -3.0)
    stiel = linie((0, 2.6), (0.8, 5.6), 1.3)
    blatt = E(2.6, 1.2, 3.0, 5.0, 25)
    return a - C(1.0, 0, 3.2) + stiel + blatt

def schofar():        # Jom Kippur: Schofar-Horn
    s = CrossSection()
    prev = None
    for k in range(13):
        t = k / 12
        x, y = -7 + 14 * t, -4 + 7 * math.sin(t * math.pi * 0.9)
        c = C(0.7 + 2.1 * t ** 1.5, x, y, 24)
        if prev is not None: s += CrossSection.batch_hull([prev, c])
        prev = c
    return s.translate([0, -0.4])

def laubhuette():     # Sukkot: Laubhütte
    huette = R(13, 8, -6.5, -6.6) - R(10.4, 6.2, -5.2, -6.7)
    dach = sum((E(1.6, 1.0, x, 2.6, 20 if i % 2 else -20) for i, x in enumerate([-5.6, -3.4, -1.1, 1.1, 3.4, 5.6])), CrossSection())
    tisch = R(5, 1.2, -2.5, -3.6) + R(1.2, 3.0, -0.6, -6.6)
    return huette + dach + linie((-6.8, 1.6), (6.8, 1.6), 1.2) + tisch

def chanukkia():      # Chanukka: neunarmiger Leuchter
    c = R(22, 1.3, -11, -1.6) + R(1.6, 4.0, -0.8, -5.6) + R(7, 1.3, -3.5, -6.6)
    for i in range(9):
        x = -10.4 + i * 2.6
        h = 4.6 if i == 4 else 3.4
        c += R(1.3, h, x - 0.65, -0.4)
        c += tropfen(x, -0.4 + h + 0.8, 0.6, -0.4 + h + 2.2)
    return c

def matze():          # Pessach: Matze
    m = RC(14, 11.5, 0, 0, 4)
    for i in range(4):
        for j in range(3):
            m -= C(0.65, -4.5 + i * 3.0, -3.0 + j * 3.0, 16).rotate(4)
    return m - linie((-7, 4.2), (7, 5.2), 0.9).rotate(0)

def maske():          # Purim: Maske
    m = E(8.2, 4.4, 0, 0.6) - E(2.6, 1.8, -3.4, 1.2) - E(2.6, 1.8, 3.4, 1.2) - C(2.2, 0, -4.2)
    stab = linie((7.0, -1.6), (9.0, -5.8), 1.3)
    return m + stab

def zwiebelkirche():  # Orthodoxe Ostern: Kirche mit Zwiebelturm
    bau = R(10, 6, -5, -6.6) - (C(1.4, 0, -3.6) + R(2.8, 3.0, -1.4, -6.7))
    trommel = R(4.4, 2.0, -2.2, -0.6)
    zwiebel = CrossSection.batch_hull([C(2.8, 0, 2.6), C(0.05, 0, 5.6)])
    kreuz = R(0.9, 2.2, -0.45, 5.0) + R(2.2, 0.9, -1.1, 6.0)
    return (bau + trommel + zwiebel + kreuz).translate([0, -0.3])

def komet():          # Orthodoxe Weihnachten: Stern von Bethlehem
    return stern5(4.0, 3.4, 2.2) + poly([(1.4, 1.4), (-7.6, -6.2), (-8.6, -4.4), (0.6, 2.8)]) + poly([(2.0, 0.6), (-4.4, -6.6), (-6.0, -6.0), (1.0, 1.8)])

def diya():           # Diwali: Öllampe
    schale = E(7.0, 3.6, 0, -2.6) ^ R(16, 6, -8, -7)
    rand = linie((-7.4, -2.2), (7.4, -2.2), 1.3)
    tuelle = poly([(5.4, -2.2), (8.6, -0.6), (6.4, -3.4)])
    flamme = tropfen(0, 1.2, 1.7, 6.6) - tropfen(0, 1.0, 0.6, 3.4)
    return schale + rand + tuelle + flamme

def holi():           # Holi: Farbspritzer
    s = C(4.6, 0, 0)
    for k in range(8):
        w = k * math.pi / 4 + 0.3
        s += C(1.2 + (k % 3) * 0.4, 5.6 * math.cos(w), 5.0 * math.sin(w), 20)
        s += CrossSection.batch_hull([C(0.8, 3.6 * math.cos(w), 3.4 * math.sin(w), 12), C(0.6, 5.6 * math.cos(w), 5.0 * math.sin(w), 12)])
    return s

def lotus():          # Vesakh: Lotusblüte
    l = E(1.8, 4.6, 0, 1.0)
    for s in (1, -1):
        l += E(1.6, 4.2, s * 2.8, 0.2, -s * 28) + E(1.4, 3.4, s * 5.2, -1.4, -s * 58)
    return l + E(7.6, 1.2, 0, -4.6)

RELIGIONEN = [("rosch_haschana", apfel, "Rosch ha-Schana (Apfel)", "2.10.2027 (ab Vorabend)"),
              ("jom_kippur", schofar, "Jom Kippur (Schofar)", "11.10.2027 (ab Vorabend)"),
              ("sukkot", laubhuette, "Sukkot (Laubhütte)", "16.10.2027 (ab Vorabend)"),
              ("chanukka", chanukkia, "Chanukka (Leuchter)", "25.12.2027 (ab Vorabend, 8 Tage)"),
              ("pessach", matze, "Pessach (Matze)", "22.4.2027 (ab Vorabend)"),
              ("purim", maske, "Purim (Maske)", "23.3.2027 (ab Vorabend)"),
              ("orth_ostern", zwiebelkirche, "Orthodoxes Ostern", "2.5.2027"),
              ("orth_weihnachten", komet, "Orthodoxe Weihnachten", "7.1."),
              ("diwali", diya, "Diwali (Öllampe)", "29.10.2027"),
              ("holi", holi, "Holi (Farben)", "22.3.2027"),
              ("vesakh", lotus, "Vesakh (Lotus)", "20.5.2027 (je nach Land)")]

# ======================= 2. Länder & regional =======================
def flagge_at():
    stange = R(1.3, 13.4, -8.2, -6.7)
    rahmen = (R(14, 9.6, -6.6, -4.4) - R(12.6, 3.0, -5.9, -1.5))
    return stange + rahmen

def flagge_ch():
    return RC(13, 13) - (RC(2.6, 8.4) + RC(8.4, 2.6))

def bluetenkranz():
    k = ring(5.4, 1.3)
    for i in range(8):
        w = i * math.pi / 4
        k += C(1.5, 5.0 * math.cos(w), 5.0 * math.sin(w), 20)
    return k

def lilie():
    mitte = CrossSection.batch_hull([E(1.6, 2.4, 0, 1.0), C(0.05, 0, 6.8)])
    seiten = CrossSection()
    for s in (1, -1):
        seiten += CrossSection.batch_hull([E(1.3, 2.0, s * 3.6, 1.6, s * 30), C(0.05, s * 6.6, 4.2)]) + linie((0, -1.4), (s * 3.2, 0.4), 1.4)
    band = R(6, 1.4, -3, -2.6)
    fuss = poly([(-1.3, -2.6), (1.3, -2.6), (0, -6.6)])
    return mitte + seiten + band + fuss

def sternenkranz():
    return sum((stern5(1.9, 5.0 * math.cos(i * math.pi / 4 + math.pi / 2), 5.0 * math.sin(i * math.pi / 4 + math.pi / 2)) for i in range(8)), CrossSection())

def kirche():
    schiff = poly([(-7, -6.6), (2, -6.6), (2, -1.0), (-2.5, 2.4), (-7, -1.0)])
    turm = R(4, 9.6, 2, -6.6) + poly([(2, 3.0), (6, 3.0), (4, 5.4)])
    kreuz = R(0.9, 2.0, 3.55, 5.0) + R(2.0, 0.9, 3.0, 5.7)
    tuer = C(1.2, -2.5, -4.0) + R(2.4, 2.6, -3.7, -6.7)
    return schiff + turm + kreuz - tuer

def eiffelturm():
    t = poly([(-5.6, -6.6), (5.6, -6.6), (1.0, 4.8), (0.4, 7.0), (-0.4, 7.0), (-1.0, 4.8)])
    t -= C(2.6, 0, -6.6) ^ R(8, 3, -4, -6.6)
    t -= linie((-4, -2.2), (4, -2.2), 0.9) + linie((-2.2, 2.0), (2.2, 2.0), 0.8)
    return t

def windmuehle():
    turm = poly([(-3.4, -6.6), (3.4, -6.6), (1.8, 1.6), (-1.8, 1.6)]) + poly([(-2.2, 1.6), (2.2, 1.6), (0, 3.8)])
    fluegel = CrossSection()
    for w in (45, 135):
        fluegel += RC(15, 1.6, 0, 1.6, w)
    for w in (45, 135, 225, 315):
        r = math.radians(w)
        fluegel += RC(1.8, 3.2, 4.6 * math.cos(r), 1.6 + 4.6 * math.sin(r), w + 90)
    tuer = R(1.8, 2.4, -0.9, -6.7)
    return (turm - tuer + fluegel + C(1.1, 0, 1.6)) ^ R(26, 14, -13, -7)

def flagge_us():
    f = sum((R(15, 1.3, -7.5, -6.4 + i * 2.6) for i in range(5)), CrossSection())
    feld = R(6.6, 5.4, -7.5, -0.2) - stern5(1.9, -4.2, 2.5)
    return f + feld

def truthahn():
    schwanz = sum((C(1.8, 5.2 * math.cos(math.radians(a)), -0.4 + 5.2 * math.sin(math.radians(a)), 20) for a in range(20, 161, 28)), CrossSection())
    koerper = E(3.6, 3.4, 0, -1.6)
    kopf = C(1.6, 0, 2.6)
    beine = linie((-1.2, -4.6), (-1.6, -6.8), 1.0) + linie((1.2, -4.6), (1.6, -6.8), 1.0)
    return ((schwanz - koerper.offset(0.7)) + koerper + kopf + beine - C(0.45, 0.5, 3.0, 12)).scale([0.9, 0.9])

def kobold_hut():
    hut = poly([(-4.4, -3.6), (4.4, -3.6), (5.2, 5.6), (-5.2, 5.6)])
    krempe = E(8.4, 1.8, 0, -4.4)
    band = R(9.6, 2.0, -4.8, -2.4)
    schnalle = R(3.2, 2.6, -1.6, -2.7) - R(1.6, 1.2, -0.8, -2.0)
    return (hut - band.offset(0.0)) + krempe + (band - R(3.2, 2.6, -1.6, -2.7)) + schnalle

def calavera():
    s = C(5.0, 0, 1.2) + R(6, 3.4, -3, -4.4)
    s -= E(1.6, 1.8, -2.0, 1.0) + E(1.6, 1.8, 2.0, 1.0) + poly([(-0.8, -1.4), (0.8, -1.4), (0, 0.2)])
    for x in (-1.6, 0, 1.6):
        s -= R(0.8, 2.0, x - 0.4, -4.5)
    return s + C(0.8, 0, 5.4) - C(0.4, 0, 5.4, 12)

LAENDER = [("at_nationalfeiertag", flagge_at, "Österreich: Nationalfeiertag", "26.10."),
           ("ch_bundesfeier", flagge_ch, "Schweiz: Bundesfeier", "1.8."),
           ("fronleichnam", bluetenkranz, "Fronleichnam (DE regional, AT, CH)", "27.5.2027"),
           ("mariae_himmelfahrt", lilie, "Mariä Himmelfahrt (AT, BY/SL)", "15.8."),
           ("mariae_empfaengnis", sternenkranz, "Mariä Empfängnis (AT)", "8.12."),
           ("buss_bettag", kirche, "Buß- und Bettag (Sachsen)", "17.11.2027"),
           ("fr_nationalfeiertag", eiffelturm, "Frankreich: Nationalfeiertag", "14.7."),
           ("nl_koningsdag", windmuehle, "Niederlande: Königstag", "27.4."),
           ("us_independence", flagge_us, "USA: Unabhängigkeitstag", "4.7."),
           ("us_thanksgiving", truthahn, "USA: Thanksgiving", "25.11.2027"),
           ("ie_st_patrick", kobold_hut, "Irland: St. Patrick's Day", "17.3."),
           ("mx_dia_muertos", calavera, "Mexiko: Tag der Toten", "1.–2.11.")]

# ======================= 3. Internationale Tage =======================
def laterne_rund():
    l = E(5.6, 4.6, 0, 0) - (sum((linie((x, -4), (x, 4), 0.8) for x in (-2.6, 0, 2.6)), CrossSection()) ^ E(5.0, 4.0))
    return l + R(5, 1.4, -2.5, 4.2) + R(5, 1.4, -2.5, -5.6) + linie((0, 5.6), (0, 6.3), 1.1) + linie((0, -5.6), (0, -6.3), 1.1)

def wassertropfen():
    t = tropfen(0, -2.2, 4.4, 6.8)
    welle = CrossSection()
    pts = [(x / 10, -2.0 + 0.8 * math.sin(x / 10 * 1.4)) for x in range(-50, 51, 5)]
    for p, q in zip(pts, pts[1:]): welle += linie(p, q, 0.9)
    return t - welle

def erde():
    e = C(6.4, 0, 0, 64)
    schnitte = (ring(3.4, 0.9).scale([1, 1.9]) ^ C(5.6, 0, 0, 64)) + linie((-5.6, 0), (5.6, 0), 0.9) \
        + linie((-5.0, 3.2), (5.0, 3.2), 0.8) + linie((-5.0, -3.2), (5.0, -3.2), 0.8) + linie((0, -5.6), (0, 5.6), 0.9)
    return e - schnitte

def buecher():
    b = R(13, 3.0, -6.5, -6.6) + R(12, 3.0, -6.0, -3.0) + RC(11, 3.0, 0, 2.0, 6)
    return b - linie((-5.4, -5.1), (5.4, -5.1), 0.8) - linie((-4.8, -1.5), (4.8, -1.5), 0.8)

def baum():
    krone = C(3.6, 0, 3.0) + C(3.0, -3.2, 1.0) + C(3.0, 3.2, 1.0) + C(2.6, 0, 0.2)
    return krone + R(2.4, 5.4, -1.2, -6.6)

def blatt_kreis():
    blatt = E(4.4, 2.4, 0.6, 0.6, 40) - linie((-2.4, -1.8), (3.2, 2.8), 0.8) + linie((-2.6, -2.0), (-4.0, -3.4), 1.0)
    return ring(6.6, 1.3) + blatt

def gitarre():
    korpus = C(3.6, -3.4, -2.4) + C(2.8, 0.6, 0.2) - C(1.2, -1.6, -1.0)
    hals = linie((1.6, 1.4), (7.4, 5.4), 1.5)
    kopf = RC(2.4, 3.4, 8.4, 6.0, -56)
    return (korpus + hals + kopf) ^ R(26, 14, -13, -7)

def zwei_herzen():
    h1 = herz(1.0, -2.6, 1.0); h2 = herz(1.0, 2.6, -0.4)
    return h1 + (h2 - h1.offset(0.8))

def windrad():
    w = CrossSection()
    for k in range(4):
        w += poly([(0, 0), (5.0, 0.4), (3.0, 3.4)]).rotate(k * 90 + 10)
    return w.translate([0, 1.6]) + C(1.0, 0, 1.6) + linie((0, 1.6), (0, -6.2), 1.3)

def herz_pfote():
    h = herz(1.35, 0, 0.6)
    pf = E(1.7, 1.3, 0, -0.8)
    for x, y in [(-2.1, 1.1), (-0.75, 2.5), (0.75, 2.5), (2.1, 1.1)]: pf += E(0.7, 0.9, x, y)
    return h - pf

def sparschwein():
    k = E(6.0, 4.4, -0.6, -0.6) + poly([(-3.2, 2.6), (-1.0, 3.4), (-2.6, 5.4)]) + E(1.3, 1.8, 5.6, -0.4)
    k += R(1.6, 2.4, -4.6, -6.6) + R(1.6, 2.4, 1.6, -6.6)
    k -= R(3.4, 0.9, -2.2, 2.6) + C(0.4, 5.3, -0.1, 12) + C(0.4, 5.9, -0.7, 12)
    schwanz = bogen(1.0, 90, 330, 0.8, -7.4, 0.2)
    return k + schwanz - C(0.5, -2.8, 0.6, 12)

def lachgesicht():
    g = C(6.6, 0, 0, 64)
    g -= bogen(1.3, 20, 160, 1.0, -2.4, 1.6) + bogen(1.3, 20, 160, 1.0, 2.4, 1.6)
    return g - (C(3.6, 0, -1.2) ^ R(8, 4, -4, -6))

def maennertag():                    # Männer-Symbol
    kreis = ring(3.9, 1.5).translate([-1.6, -1.8])
    pfeil = linie((1.0, 0.8), (5.4, 5.2), 1.5) + poly([(6.4, 6.2), (1.8, 6.0), (6.2, 1.6)])
    return kreis + pfeil

INTERNATIONAL = [("chin_neujahr", laterne_rund, "Chinesisches Neujahr", "6.2.2027"),
                 ("weltwassertag", wassertropfen, "Weltwassertag", "22.3."),
                 ("tag_der_erde", erde, "Tag der Erde", "22.4."),
                 ("welttag_buch", buecher, "Welttag des Buches", "23.4."),
                 ("tag_des_baumes", baum, "Tag des Baumes", "25.4."),
                 ("weltumwelttag", blatt_kreis, "Weltumwelttag", "5.6."),
                 ("fete_musique", gitarre, "Fête de la Musique", "21.6."),
                 ("freundschaft", zwei_herzen, "Tag der Freundschaft", "30.7."),
                 ("weltkindertag", windrad, "Weltkindertag (DE; in Thüringen Feiertag)", "20.9."),
                 ("welttierschutztag", herz_pfote, "Welttierschutztag", "4.10."),
                 ("weltspartag", sparschwein, "Weltspartag", "30.10."),
                 ("weltlachtag", lachgesicht, "Weltlachtag", "2.5.2027 (1. Sonntag im Mai)"),
                 ("maennertag", maennertag, "Internationaler Männertag", "19.11. (in AT/DE oft auch 3.11.)")]

# ======================= 4. Lustige Aktionstage =======================
def pizza():
    dreieck = poly([(-6.6, 5.0), (6.6, 5.0), (0, -6.8)])
    kruste = R(14.4, 2.2, -7.2, 4.6)
    p = (dreieck - R(14, 0.8, -7, 4.0)) + (kruste ^ dreieck.offset(0.8))
    return p - C(1.2, -2.2, 1.6) - C(1.2, 1.8, 1.0) - C(1.0, 0, -2.6)

def pi_zeichen():
    return gl.text_cs("π", 12)

def planet():
    kugel = C(4.4, 0, 0, 48)
    reif = E(9.6, 2.8, 0, 0, -15) - E(7.2, 1.6, 0, 0, -15)
    return (kugel - reif.offset(0.7)) + reif + stern5(1.6, -8.6, 5.0) + stern5(1.3, 8.8, 5.2)

def pinguin():
    k = E(4.6, 6.0, 0, -0.6) - E(3.0, 3.6, 0, -2.0) - C(0.6, -1.3, 3.2, 12) - C(0.6, 1.3, 3.2, 12)
    schnabel = poly([(-1.0, 2.2), (1.0, 2.2), (0, 0.8)])
    fuesse = E(1.6, 0.8, -1.8, -6.2) + E(1.6, 0.8, 1.8, -6.2)
    return k + schnabel + fuesse

def schokolade():
    t = RC(12, 13, 0, 0, 0)
    for x in (-2, 2): t -= linie((x, -7), (x, 7), 0.9)
    for y in (-2.2, 2.2): t -= linie((-7, y), (7, y), 0.9)
    return t - C(2.6, 6.0, 6.5) - C(2.0, 3.6, 7.4)

def zwinker():
    g = C(6.6, 0, 0, 64) - C(1.1, -2.4, 1.8) - linie((1.4, 1.8), (3.6, 1.8), 1.0)
    return g - bogen(3.6, 200, 340, 1.1, 0, 0.4)

def pommes():
    tuete = poly([(-4.8, 0.8), (4.8, 0.8), (3.6, -6.6), (-3.6, -6.6)])
    fries = CrossSection()
    for i, (x, h, w) in enumerate([(-3.4, 5.4, 4), (-1.7, 6.6, -3), (0, 6.0, 2), (1.7, 6.8, -2), (3.4, 5.2, 5)]):
        fries += RC(1.3, 7.0, x, 0.8 + h / 2 - 1.6, w)
    return (fries - tuete.offset(0.8)) + tuete - E(2.2, 1.6, 0, -2.6) + E(1.4, 0.9, 0, -2.6)

def eis():
    waffel = poly([(-3.4, -0.4), (3.4, -0.4), (0, -6.8)])
    for k in range(-2, 3): waffel -= linie((k * 1.8 - 3, -6), (k * 1.8 + 1.6, 0), 0.6)
    kugeln = C(2.8, -1.6, 2.2) + C(2.8, 1.6, 2.2) + C(2.4, 0, 4.4)
    return (waffel - kugeln.offset(0.6)) + kugeln

def katze():
    k = C(5.2, 0, -1.2, 48) + poly([(-5.0, 0.4), (-4.6, 6.4), (-1.0, 3.6)]) + poly([(5.0, 0.4), (4.6, 6.4), (1.0, 3.6)])
    k -= E(0.9, 1.3, -2.0, -0.2) + E(0.9, 1.3, 2.0, -0.2) + poly([(-0.9, -2.0), (0.9, -2.0), (0, -3.0)])
    for s in (1, -1):
        k -= linie((s * 1.6, -3.4), (s * 3.6, -3.0), 0.7) + linie((s * 1.6, -4.0), (s * 3.4, -4.4), 0.7)
    return k

def knochen():
    b = RC(10, 2.6, 0, 0, 20)
    for sx in (1, -1):
        for sy in (1, -1):
            b += C(1.9, sx * 5.0 + sy * 0.6 * -0.34, sy * 1.6 + sx * 5.0 * 0.36)
    return b

def kaffeebohne():
    b = E(4.4, 6.2, 0, 0, -20)
    s = CrossSection()
    pts = [(0.9 * math.sin(t / 10 * 2.2), t / 10) for t in range(-55, 56, 5)]
    for p, q in zip(pts, pts[1:]): s += linie(p, q, 1.0)
    return b - s.rotate(-20)

def keks():
    k = C(6.4, 0, 0, 56) - C(2.6, 5.6, 4.2)
    for x, y in [(-2.8, 2.2), (1.4, 1.0), (-1.0, -2.6), (3.0, -2.4), (-3.8, -1.0), (0.2, 4.0)]:
        k -= C(0.9, x, y, 16)
    return k

LUSTIG = [("pizza", pizza, "Tag der Pizza", "9.2."), ("pi", pi_zeichen, "Pi-Tag", "14.3."),
          ("weltraum", planet, "Weltraum-Tag", "4.5."), ("pinguin", pinguin, "Weltpinguintag", "25.4."),
          ("schokolade", schokolade, "Welttag der Schokolade", "7.7."), ("emoji", zwinker, "Welt-Emoji-Tag", "17.7."),
          ("pommes", pommes, "Tag der Pommes", "13.7."), ("eis", eis, "Tag des Speiseeises", "18.7.2027 (3. So im Juli)"),
          ("katze", katze, "Weltkatzentag", "8.8."), ("hund", knochen, "Internationaler Hundetag", "26.8."),
          ("kaffee", kaffeebohne, "Tag des Kaffees", "1.10."), ("keks", keks, "Tag des Kekses", "4.12.")]

GRUPPEN = [("religionen", "Religionen", RELIGIONEN), ("laender", "Länder & regional", LAENDER),
           ("international", "Internationale Tage", INTERNATIONAL), ("aktionstage", "Lustige Aktionstage", LUSTIG)]

def _m(f):
    return lambda: muster_cs(f)

PLATTEN = [Platte(f"4_Extra_Schubladen/welt_feiertage/schubladen_{key}_{len(liste)}x.stl",
                  [(f"w_{key}_{k}", _m(f)) for k, f, *_ in liste]) for key, _, liste in GRUPPEN]
