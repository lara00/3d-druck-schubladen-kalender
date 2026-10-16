"""Symbol-Schubladen: Sport, Hobby & Freizeit, Alltag (je 12).
Platz für das Motiv: x −13 … 13, y −7 … 7 mm; Linien ≥ 1,2 mm.
"""
import math
from manifold3d import CrossSection, JoinType
from basis import grundlagen as gl
from basis.zeichnen import C, E, R, RC, linie, ring, poly, tropfen, bogen, muster_cs
from basis.platten import Platte

B = 1.4                                   # Standard-Linienbreite für Figuren
LEER = CrossSection()

def kette(pts, b=B):
    s = LEER
    for p, q in zip(pts, pts[1:]): s += linie(p, q, b)
    return s

def welle(y, x0=-11.5, x1=11.5, a=0.9, n=3, b=1.2):
    pts = [(x0 + (x1 - x0) * k / 48, y + a * math.sin(2 * math.pi * n * k / 48)) for k in range(49)]
    return kette(pts, b)

def figur(kopf, nacken, huefte, arme, beine, r=1.6, b=B):
    """Strichmännchen: Kopf (x, y), Rumpf nacken→hüfte, arme/beine: Listen von Punktketten."""
    s = C(r, *kopf) + linie(nacken, huefte, b + 0.3)
    for a in arme: s += kette([nacken] + a, b)
    for bn in beine: s += kette([huefte] + bn, b)
    return s

def rrect(w, h, r, x=0, y=0):
    """abgerundetes Rechteck, Mitte (x, y)"""
    s = CrossSection.square([w - 2 * r, h], center=True) + CrossSection.square([w, h - 2 * r], center=True)
    for sx in (-1, 1):
        for sy in (-1, 1): s += C(r, sx * (w / 2 - r), sy * (h / 2 - r), 24)
    return s.translate([x, y])

def ngon(n, r, x=0, y=0, w=90):
    return CrossSection([[(x + r * math.cos(math.radians(w + 360 * k / n)), y + r * math.sin(math.radians(w + 360 * k / n))) for k in range(n)]])

# ---------------------------------------------------------------- Sport
def schwimmen():
    k = C(1.7, 5.6, 3.0)
    koerper = linie((-7.5, 0.6), (3.4, 1.6), 1.7)
    arm = kette([(1.0, 1.4), (4.5, 4.6), (8.5, 3.6)])
    bein = linie((-7.5, 0.6), (-11, 2.0), 1.5)
    return k + koerper + arm + bein + welle(-3.4, n=3) + welle(-6.2, n=3)

def radfahren():
    r = 3.9
    s = ring(r, 1.3).translate([-7.6, -2.8]) + ring(r, 1.3).translate([7.6, -2.8])
    s += kette([(-7.6, -2.8), (-0.6, -2.8), (5.0, 2.6), (-2.6, 2.6), (-0.6, -2.8)], 1.3)
    s += kette([(-7.6, -2.8), (-2.6, 2.6)], 1.3) + kette([(7.6, -2.8), (4.6, 4.6), (2.6, 4.9)], 1.3)
    s += linie((-4.2, 4.6), (-1.4, 4.6), 1.4) + linie((-2.6, 2.6), (-2.8, 4.4), 1.3)   # Sattel
    return s + C(1.2, -0.6, -2.8)

def laufen():
    s = figur((3.4, 5.0), (2.4, 2.8), (0.2, -1.6),
              arme=[[(5.6, 0.6), (7.4, 2.2)], [(-1.2, 1.4), (-3.8, 2.8)]],
              beine=[[(3.8, -3.4), (2.8, -6.6)], [(-2.6, -3.6), (-6.2, -3.0)]])
    for y, x0 in [(3.0, -11.5), (0.2, -12.0), (-2.6, -11.5)]:
        s += linie((x0, y), (x0 + 3.6, y), 1.2)
    return s

def fussball():
    s = ring(6.7, 1.3) + ngon(5, 2.4)
    for k in range(5):
        w = math.radians(90 + 72 * k)
        s += linie((2.2 * math.cos(w), 2.2 * math.sin(w)), (6.0 * math.cos(w), 6.0 * math.sin(w)), 1.3)
    return s

def fitness():                            # Kettlebell
    korper = C(5.0, 0, -1.8)
    griff = (E(4.2, 3.6, 0, 3.4) - E(2.8, 2.2, 0, 3.6)) - R(12, 3, -6, -1.6)
    return korper + griff + R(5.2, 1.6, -2.6, 2.0) - C(1.2, 0, -1.8)

def yoga():
    s = C(1.7, 0, 5.0) + poly([(-1.7, 3.0), (1.7, 3.0), (2.6, -2.6), (-2.6, -2.6)])
    s += E(7.6, 1.6, 0, -4.4)
    s += kette([(-1.6, 2.4), (-4.4, -0.2), (-6.0, -1.8)]) + kette([(1.6, 2.4), (4.4, -0.2), (6.0, -1.8)])
    return s + C(0.95, -6.4, -2.0) + C(0.95, 6.4, -2.0)

def wandern():
    s = figur((1.2, 5.2), (0.6, 3.0), (-0.6, -1.8),
              arme=[[(2.6, 0.4), (4.4, 0.6)]],
              beine=[[(1.6, -4.0), (2.0, -6.6)], [(-2.4, -4.2), (-3.8, -6.6)]])
    s += rrect(3.6, 5.0, 1.0, -2.8, 1.4)                                   # Rucksack
    s += linie((5.0, 3.0), (6.4, -6.6), 1.3)                               # Stock
    s += kette([(7.0, -6.4), (9.4, -3.6), (11.0, -5.2), (12.6, -2.6)], 1.2)  # Berg
    return s

def ski():
    s = figur((1.6, 4.8), (0.4, 2.8), (-1.4, -0.8),
              arme=[[(2.4, 0.6), (4.6, 1.2)], [(-1.8, 1.4), (-4.4, 0.4)]],
              beine=[[(1.0, -3.0), (-0.2, -4.6)], [(-3.0, -3.2), (-3.6, -4.8)]])
    s += kette([(-8.6, -3.8), (6.2, -6.4), (7.4, -5.6)], 1.3)              # Ski
    s += linie((4.6, 1.2), (5.8, -4.2), 1.2) + linie((-4.4, 0.4), (-6.8, -3.6), 1.2)
    return s

def tennis():
    kopf = (E(4.6, 5.6) - E(3.3, 4.3))
    saiten = LEER
    for x in (-1.2, 1.2): saiten += RC(1.2, 9.2, x, 0)
    for y in (-1.6, 1.6): saiten += RC(7.2, 1.2, 0, y)
    schlaeger = (kopf + (saiten ^ E(3.6, 4.6))) + linie((0, -5.4), (0, -9.6), 1.6)
    schlaeger = schlaeger.rotate(-35).translate([-2.8, 1.6])
    ball = C(2.4, 7.6, -3.4) - bogen(2.2, 120, 240, 0.7, 9.6, -3.4) - bogen(2.2, -60, 60, 0.7, 5.6, -3.4)
    return schlaeger + ball

def basketball():
    s = C(6.7)
    nahte = RC(0.9, 14, 0, 0) + RC(14, 0.9, 0, 0) + bogen(6.2, -50, 50, 0.9, -8.2, 0) + bogen(6.2, 130, 230, 0.9, 8.2, 0)
    return s - nahte

def tanzen():
    s = C(1.6, 0.6, 5.2) + poly([(-0.4, 3.2), (1.6, 3.2), (4.6, -3.0), (-3.4, -3.0)])
    s += kette([(0.4, 3.0), (-3.0, 4.6), (-5.0, 6.4)]) + kette([(0.8, 3.0), (4.4, 2.0), (6.6, 3.2)])
    s += linie((-0.8, -3.0), (-2.0, -6.6), 1.4) + linie((1.8, -3.0), (3.2, -6.4), 1.4)
    for x, y in [(-9.0, 2.0), (8.8, -1.6)]:                                # Notenköpfe
        s += E(1.2, 0.9, x, y, 20) + linie((x + 1.0, y + 0.2), (x + 1.0, y + 4.4), 1.25)
    return s

def klettern():                           # Karabiner + Seil
    ring_ = E(4.4, 6.8) - E(3.0, 5.4)
    luecke = RC(2.4, 5.0, 3.8, 0.6)
    tor = linie((3.7, -2.6), (3.7, 3.8), 1.3)
    seil = kette([(-3.6, 3.6), (-7.0, 5.6), (-10.4, 4.4), (-11.6, 0.0), (-10.0, -4.4), (-7.4, -6.2)], 1.5)
    return (ring_ - luecke) + tor + seil

# ---------------------------------------------------------------- Hobby & Freizeit
def gitarre():
    k = C(3.6, 0, -2.6) + C(2.7, 0, 2.2) - C(1.25, 0, 0.4)
    s = k + RC(1.6, 6.4, 0, 5.8) + RC(2.6, 2.4, 0, 9.4) + RC(4.0, 1.0, 0, -4.4)
    return s.rotate(-40).translate([1.0, -1.6])

def malen():
    pal = E(7.6, 5.6, -2.4, 0, -10) - E(1.3, 1.1, -6.8, -1.6)
    for x, y in [(-4.0, 3.0), (-0.6, 3.6), (2.6, 2.4), (2.6, -1.0)]: pal -= C(1.15, x, y)
    pinsel = linie((4.0, -5.6), (11.6, 3.6), 1.4) + E(1.0, 2.2, 3.2, -6.4, 40)
    return pal + pinsel

def kochen():
    topf = rrect(13.0, 7.4, 1.6, 0, -2.6) + RC(15.6, 1.4, 0, 1.4)
    topf += linie((-8.6, -0.8), (-6.4, -0.8), 1.4) + linie((6.4, -0.8), (8.6, -0.8), 1.4)
    topf += RC(2.4, 1.2, 0, 2.6)
    dampf = LEER
    for x in (-3.4, 0, 3.4):
        dampf += kette([(x, 4.0), (x + 0.8, 5.0), (x, 6.0), (x + 0.8, 6.8)], 1.1)
    return topf + dampf

def backen():                             # Muffin
    form = poly([(-5.0, -0.6), (5.0, -0.6), (3.6, -6.8), (-3.6, -6.8)])
    for x in (-2.0, 0.0, 2.0): form -= linie((x * 1.3, -1.6), (x, -5.8), 0.8)
    haube = C(3.0, -2.6, 1.6) + C(3.0, 2.6, 1.6) + C(3.4, 0, 2.8) + RC(10.4, 1.6, 0, 0.0)
    return form + haube + C(1.3, 0.8, 6.4) + linie((1.4, 7.4), (2.6, 8.2), 0.9)

def gaming():
    k = E(4.2, 4.2, -5.4, -0.8) + E(4.2, 4.2, 5.4, -0.8) + rrect(12.0, 7.4, 2.6, 0, 0.4)
    k -= RC(4.2, 1.2, -5.6, 0) + RC(1.2, 4.2, -5.6, 0)
    for x, y in [(4.6, 1.3), (6.6, -0.6), (4.6, -2.4), (2.8, -0.6)]: k -= C(0.75, x, y)
    return k

def fotografie():
    k = rrect(18.0, 10.6, 1.8, 0, -1.2) + rrect(6.0, 3.0, 1.0, -3.6, 4.6)
    k -= C(3.8, 0.6, -1.4) - C(2.4, 0.6, -1.4)
    k -= RC(2.2, 1.2, 6.4, 1.8)
    return k

def angeln():
    fisch = E(5.2, 2.8, -2.0, -2.6) + poly([(2.6, -2.6), (6.6, 0.2), (6.6, -5.4)]) - C(0.75, -5.0, -1.9)
    rute = kette([(-12.0, -6.6), (-9.0, 1.0), (-5.4, 5.6), (-2.6, 6.8)], 1.3)
    leine = linie((-2.6, 6.8), (-2.0, 1.4), 1.15) + bogen(1.0, 180, 360, 1.15, -3.0, 1.4)
    return fisch + rute + leine

def garten():                             # Pflanze im Topf
    topf = poly([(-4.4, -1.2), (4.4, -1.2), (3.2, -6.8), (-3.2, -6.8)]) + RC(10.6, 1.6, 0, -0.6)
    stiel = linie((0, 0), (0, 4.6), 1.3)
    blatt_l = E(3.8, 1.6, -3.4, 4.0, 30)
    blatt_r = E(3.8, 1.6, 3.4, 5.2, -30)
    return topf + stiel + blatt_l + blatt_r

def camping():
    zelt = poly([(-10.0, -5.4), (0, 6.4), (10.0, -5.4)]) - poly([(-2.6, -5.4), (0, -0.6), (2.6, -5.4)])
    boden = linie((-12.0, -6.4), (12.0, -6.4), 1.2)
    return zelt + boden + C(0.9, -9.6, 5.0) + C(0.7, 9.0, 4.0)

def strand():                             # Palme mit Sonne
    stamm = kette([(-1.0, -5.6), (-1.6, -2.0), (-1.2, 1.2), (0.0, 3.6)], 1.6)
    blaetter = E(4.2, 1.3, -3.6, 4.0, 25) + E(4.2, 1.3, 3.4, 4.6, -15) + E(3.6, 1.2, -2.8, 6.0, -25) + E(3.6, 1.2, 3.0, 2.8, -55)
    insel = E(8.0, 1.5, -1.0, -5.8)
    sonne = C(2.4, 9.0, 3.4)
    welle_ = kette([(4.0, -6.6), (6.0, -5.6), (8.0, -6.6), (10.0, -5.6), (12.0, -6.6)], 1.2)
    return stamm + blaetter + insel + sonne + welle_

def konzert():                            # Mikrofon
    kopf = E(3.2, 3.6, 0, 3.2)
    kopf -= RC(7, 0.9, 0, 3.0)
    return kopf + RC(2.0, 6.4, 0, -2.6) + bogen(5.0, 200, 340, 1.2, 0, 0.8) + linie((0, -4.2), (0, -6.4), 1.3) + RC(6.0, 1.2, 0, -6.4)

def spieleabend():                        # zwei Würfel
    w1 = rrect(9.0, 9.0, 1.6).rotate(-12).translate([-5.6, 0])
    for x, y in [(-2.3, 2.3), (0, 0), (2.3, -2.3)]: w1 -= C(1.0, x, y).rotate(-12).translate([-5.6, 0])
    w2 = rrect(9.0, 9.0, 1.6).rotate(15).translate([5.6, 0])
    for x, y in [(-2.2, 2.2), (2.2, 2.2), (-2.2, -2.2), (2.2, -2.2)]: w2 -= C(1.0, x, y).rotate(15).translate([5.6, 0])
    return w1 + w2

# ---------------------------------------------------------------- Alltag
def waesche():                            # Waschmaschine
    m = rrect(12.0, 13.6, 1.6) - (C(4.0, 0, -1.4) - C(2.6, 0, -1.4))
    m -= RC(9.6, 1.0, 0, 3.8)
    for x in (2.6, 4.2): m -= C(0.55, x, 5.4)
    return m

def putzen():                             # Besen
    stiel = linie((7.0, 6.6), (0.6, 0.0), 1.5)
    kopf = poly([(1.6, 0.8), (-0.4, -1.2), (-6.4, -6.8), (3.4, -6.8)])
    for x in (-2.2, 0.8): kopf -= linie((x + 1.4, -2.6), (x, -6.4), 0.9)
    return stiel + kopf

def giessen():                            # Gießkanne
    k = poly([(-5.4, 3.4), (2.6, 3.4), (3.6, -5.6), (-6.4, -5.6)])
    tuelle = linie((2.8, -2.6), (8.6, 3.6), 1.5) + RC(3.2, 1.5, 9.2, 4.0, 45)
    griff = bogen(3.4, 90, 270, 1.4, -6.0, -0.6)
    tropfen_ = tropfen(11.2, 0.4, 0.9, 2.2) + tropfen(9.6, -2.0, 0.9, -0.2) + tropfen(12.0, -3.8, 0.9, -2.0)
    return k + tuelle + griff + tropfen_

def medikament():
    kapsel = rrect(11.0, 4.6, 2.3).rotate(30).translate([-4.0, 1.0])
    kapsel -= RC(0.8, 5.0, -4.0, 1.0, 30)
    tablette = C(3.6, 6.0, -2.2) - RC(7.6, 0.9, 6.0, -2.2, -30)
    return kapsel + tablette

def schule():
    return gl.text_cs("ABC", 10)

def arbeit():                             # Aktentasche
    t = rrect(17.0, 10.4, 1.6, 0, -1.6) - RC(17.4, 0.9, 0, -0.2)
    griff = rrect(7.0, 4.0, 1.4, 0, 4.2) - rrect(4.2, 2.6, 0.6, 0, 3.6)
    return t + griff + RC(2.6, 2.2, 0, -0.2)

def auto():
    k = poly([(-11.4, -3.6), (-11.4, 0.6), (-6.6, 1.2), (-3.6, 5.0), (4.0, 5.0), (7.6, 1.2), (11.4, 0.4), (11.4, -3.6)])
    k -= poly([(-2.8, 3.8), (-0.6, 3.8), (-0.6, 1.4), (-5.0, 1.4)]) + poly([(0.6, 3.8), (3.4, 3.8), (5.8, 1.4), (0.6, 1.4)])
    k -= C(3.2, -6.2, -3.6) + C(3.2, 6.2, -3.6)
    return k + C(2.4, -6.2, -3.6) + C(2.4, 6.2, -3.6)

def zug():
    k = rrect(11.0, 11.4, 2.4, 0, 1.0)
    k -= rrect(8.0, 3.8, 0.8, 0, 3.4)
    k -= C(1.0, -3.0, -2.4) + C(1.0, 3.0, -2.4)
    schienen = linie((-4.0, -5.0), (-6.8, -7.0), 1.3) + linie((4.0, -5.0), (6.8, -7.0), 1.3)
    return k + schienen

def paket():
    p = poly([(-8.0, 2.4), (0, 5.6), (8.0, 2.4), (8.0, -5.0), (0, -7.0), (-8.0, -5.0)])
    p -= linie((0, -6.8), (0, 2.4), 0.8) + linie((-8.0, 2.4), (0, -0.8), 0.8) + linie((8.0, 2.4), (0, -0.8), 0.8)
    return p

def kino():                               # Filmklappe
    tafel = R(17.0, 9.2, -8.5, -7.0)
    tafel -= RC(14.6, 0.8, 0, -3.4)
    klappe = R(17.0, 3.0, -8.5, 3.0).rotate(10)
    for x in (-5.4, -1.0, 3.4): klappe -= poly([(x, 3.0), (x + 2.2, 3.0), (x + 3.4, 6.2), (x + 1.2, 6.2)]).rotate(10)
    return tafel + klappe

def buch():
    l = poly([(-11.6, 4.0), (-0.6, 5.6), (-0.6, -5.6), (-11.6, -4.0)])
    r = poly([(11.6, 4.0), (0.6, 5.6), (0.6, -5.6), (11.6, -4.0)])
    for k in range(3):
        y = 2.6 - 2.4 * k
        l -= linie((-9.6, y - 0.3), (-2.6, y + 0.7), 0.8)
        r -= linie((9.6, y - 0.3), (2.6, y + 0.7), 0.8)
    return l + r + RC(1.0, 12.4, 0, -0.4)

def telefon():                            # Smartphone
    h = rrect(8.4, 14.0, 1.6) - RC(6.0, 9.4, 0, 0.4)
    return h

SPORT = [("schwimmen", schwimmen, "Schwimmen", "Swimming"), ("radfahren", radfahren, "Radfahren", "Cycling"),
         ("laufen", laufen, "Laufen", "Running"), ("fussball", fussball, "Fußball", "Football"),
         ("fitness", fitness, "Fitness (Kettlebell)", "Fitness (kettlebell)"), ("yoga", yoga, "Yoga", "Yoga"),
         ("wandern", wandern, "Wandern", "Hiking"), ("ski", ski, "Skifahren", "Skiing"),
         ("tennis", tennis, "Tennis", "Tennis"), ("basketball", basketball, "Basketball", "Basketball"),
         ("tanzen", tanzen, "Tanzen", "Dancing"), ("klettern", klettern, "Klettern", "Climbing")]
HOBBY = [("gitarre", gitarre, "Musik (Gitarre)", "Music (guitar)"), ("malen", malen, "Malen", "Painting"),
         ("kochen", kochen, "Kochen", "Cooking"), ("backen", backen, "Backen", "Baking"),
         ("gaming", gaming, "Gaming", "Gaming"), ("fotografie", fotografie, "Fotografieren", "Photography"),
         ("angeln", angeln, "Angeln", "Fishing"), ("garten", garten, "Garten", "Gardening"),
         ("camping", camping, "Camping", "Camping"), ("strand", strand, "Strand", "Beach"),
         ("konzert", konzert, "Konzert / Singen", "Concert / singing"), ("spieleabend", spieleabend, "Spieleabend", "Games night")]
ALLTAG = [("waesche", waesche, "Wäsche waschen", "Laundry"), ("putzen", putzen, "Putzen", "Cleaning"),
          ("giessen", giessen, "Blumen gießen", "Water the plants"), ("medikament", medikament, "Medikament", "Medicine"),
          ("schule", schule, "Schule", "School"), ("arbeit", arbeit, "Arbeit", "Work"),
          ("auto", auto, "Auto", "Car"), ("zug", zug, "Zug / Bahn", "Train"),
          ("paket", paket, "Paket / Post", "Parcel / post"), ("kino", kino, "Kino", "Cinema"),
          ("buch", buch, "Lesen", "Reading"), ("telefon", telefon, "Telefonieren", "Phone call")]
def passend(f, b=26.0, h=14.0):
    """Motiv auf die Fläche 26 × 14 mm verkleinern (statt abzuschneiden)."""
    def g():
        cs = f()
        x0, y0, x1, y1 = cs.bounds()
        s = min(1.0, b / (x1 - x0), h / (y1 - y0))
        cs = cs.translate([-(x0 + x1) / 2, -(y0 + y1) / 2]).scale([s, s])
        return cs.offset(0.02, JoinType.Miter).offset(-0.02, JoinType.Miter).simplify(0.005)   # Berührpunkte sauber verschmelzen
    return g

SPORT = [(k, passend(f), de, en) for k, f, de, en in SPORT]
HOBBY = [(k, passend(f), de, en) for k, f, de, en in HOBBY]
ALLTAG = [(k, passend(f), de, en) for k, f, de, en in ALLTAG]
GRUPPEN = [("sport", "Sport", "Sport", SPORT), ("hobby", "Hobby & Freizeit", "Hobbies & leisure", HOBBY),
           ("alltag", "Alltag", "Everyday", ALLTAG)]

def _m(f):
    return lambda: muster_cs(f)

PLATTEN = [Platte(f"4_Extra_Schubladen/schubladen_{key}_{len(liste)}x.stl", [(f"y_{key}_{k}", _m(f)) for k, f, *_ in liste])
           for key, _, _, liste in GRUPPEN]
