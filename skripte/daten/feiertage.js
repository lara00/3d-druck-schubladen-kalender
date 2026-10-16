// Feiertage für jedes Jahr berechnen (statt fester Liste). Wird in den Konfigurator eingebaut.
// FEIERTAGE.jahr(y) liefert { gruppe: [[ "M-T", motiv, bundesländer|null, name_en, name_de, land ], …], … }
// Rechenwege: Ostern (Gauß/Meeus), orthodoxes Ostern (julianisch), n-ter Wochentag, Jahreszeiten (Meeus),
// Neumond für das chinesische Neujahr (Meeus), islamischer (Umm al-Qura) und jüdischer Kalender über den Browser (Intl).
const FEIERTAGE = (() => {
  const md = d => `${d.getUTCMonth() + 1}-${d.getUTCDate()}`;
  const tag = (y, m, d) => new Date(Date.UTC(y, m - 1, d));
  const plus = (d, n) => new Date(d.getTime() + n * 864e5);
  function ostern(y) {                                   // westlich (gregorianisch)
    const a = y % 19, b = Math.floor(y / 100), c = y % 100, d = Math.floor(b / 4), e = b % 4, f = Math.floor((b + 8) / 25),
      g = Math.floor((b - f + 1) / 3), h = (19 * a + b - d - g + 15) % 30, i = Math.floor(c / 4), k = c % 4,
      l = (32 + 2 * e + 2 * i - h - k) % 7, m = Math.floor((a + 11 * h + 22 * l) / 451);
    return tag(y, Math.floor((h + l - 7 * m + 114) / 31), ((h + l - 7 * m + 114) % 31) + 1);
  }
  function ostern_orth(y) {                              // orthodox: julianisch berechnet, +13 Tage (1900–2099)
    const a = y % 4, b = y % 7, c = y % 19, d = (19 * c + 15) % 30, e = (2 * a + 4 * b - d + 34) % 7;
    const m = Math.floor((d + e + 114) / 31), t = ((d + e + 114) % 31) + 1;
    return plus(tag(y, m, t), 13);
  }
  function wtag(y, m, wd, n) {                           // n-ter Wochentag (0 = So) im Monat, n = -1: letzter
    if (n > 0) { const d1 = tag(y, m, 1); return plus(d1, ((wd - d1.getUTCDay() + 7) % 7) + 7 * (n - 1)); }
    const dl = tag(y, m + 1, 0); return plus(dl, -((dl.getUTCDay() - wd + 7) % 7));
  }
  // ---- Astronomie (Meeus) ----
  const RAD = Math.PI / 180;
  function jdZuDatum(jd, zone) {                         // Julianisches Datum → Kalendertag in einer Zeitzone
    const ms = (jd - 2440587.5) * 864e5;
    const p = new Intl.DateTimeFormat("en-CA", { timeZone: zone, year: "numeric", month: "numeric", day: "numeric" }).formatToParts(new Date(ms));
    const w = t => +p.find(x => x.type === t).value;
    return tag(w("year"), w("month"), w("day"));
  }
  const deltaT = y => (62.92 + 0.32217 * (y - 2000) + 0.005589 * (y - 2000) ** 2) / 86400;   // TT − UT in Tagen (NASA, 2005–2050)
  const JZ_TERME = [[485,324.96,1934.136],[203,337.23,32964.467],[199,342.08,20.186],[182,27.85,445267.112],[156,73.14,45036.886],
    [136,171.52,22518.443],[77,222.54,65928.934],[74,296.72,3034.906],[70,243.58,9037.513],[58,119.81,33718.147],[52,297.17,150.678],
    [50,21.02,2281.226],[45,247.54,29929.562],[44,325.15,31555.956],[29,60.93,4443.417],[18,155.12,67555.328],[17,288.79,4562.452],
    [16,198.04,62894.029],[14,199.76,31436.921],[12,95.39,14577.848],[12,287.11,31931.756],[12,320.81,34777.259],[9,227.73,1222.114],[8,15.45,16859.074]];
  function jahreszeit(y, k) {                            // k: 0 Frühling, 1 Sommer, 2 Herbst, 3 Winter → Datum (Berlin)
    const Y = (y - 2000) / 1000;
    const j0 = [2451623.80984 + 365242.37404 * Y + 0.05169 * Y ** 2 - 0.00411 * Y ** 3 - 0.00057 * Y ** 4,
                2451716.56767 + 365241.62603 * Y + 0.00325 * Y ** 2 + 0.00888 * Y ** 3 - 0.00030 * Y ** 4,
                2451810.21715 + 365242.01767 * Y - 0.11575 * Y ** 2 + 0.00337 * Y ** 3 + 0.00078 * Y ** 4,
                2451900.05952 + 365242.74049 * Y - 0.06223 * Y ** 2 - 0.00823 * Y ** 3 + 0.00032 * Y ** 4][k];
    const T = (j0 - 2451545.0) / 36525, W = 35999.373 * T - 2.47, dl = 1 + 0.0334 * Math.cos(W * RAD) + 0.0007 * Math.cos(2 * W * RAD);
    const S = JZ_TERME.reduce((s, [a, b, c]) => s + a * Math.cos((b + c * T) * RAD), 0);
    return jdZuDatum(j0 + 0.00001 * S / dl - deltaT(y), "Europe/Berlin");
  }
  function neumond(k) {                                  // k-ter Neumond seit 2000 (Meeus Kap. 49) → JDE
    const T = k / 1236.85, E = 1 - 0.002516 * T - 0.0000074 * T * T;
    const M = (2.5534 + 29.10535670 * k) * RAD, Mp = (201.5643 + 385.81693528 * k + 0.0107582 * T * T) * RAD;
    const F = (160.7108 + 390.67050284 * k - 0.0016118 * T * T) * RAD, Om = (124.7746 - 1.56375588 * k + 0.0020672 * T * T) * RAD;
    let jde = 2451550.09766 + 29.530588861 * k + 0.00015437 * T * T;
    jde += -0.40720 * Math.sin(Mp) + 0.17241 * E * Math.sin(M) + 0.01608 * Math.sin(2 * Mp) + 0.01039 * Math.sin(2 * F)
      + 0.00739 * E * Math.sin(Mp - M) - 0.00514 * E * Math.sin(Mp + M) + 0.00208 * E * E * Math.sin(2 * M) - 0.00111 * Math.sin(Mp - 2 * F)
      - 0.00057 * Math.sin(Mp + 2 * F) + 0.00056 * E * Math.sin(2 * Mp + M) - 0.00042 * Math.sin(3 * Mp) + 0.00042 * E * Math.sin(M + 2 * F)
      + 0.00038 * E * Math.sin(M - 2 * F) - 0.00024 * E * Math.sin(2 * Mp - M) - 0.00017 * Math.sin(Om) - 0.00007 * Math.sin(Mp + 2 * M);
    return jde;
  }
  function chin_neujahr(y) {                             // 2. Neumond nach der Wintersonnenwende (Zeit in China)
    const ws = jahreszeit(y - 1, 3).getTime();
    let k = Math.floor((y - 1 - 2000) * 12.3685) + 8, n = 0;
    for (; ; k++) {
      const d = jdZuDatum(neumond(k) - deltaT(y), "Asia/Shanghai");
      if (d.getTime() > ws && ++n === 2) return d;
    }
  }
  // ---- islamischer und jüdischer Kalender (über den Browser) ----
  const KAL = {};
  function kalender(y, art) {                            // {"Monat-Tag": [Datum, …]} für alle Tage im Jahr y
    const sch = art + y;
    if (KAL[sch]) return KAL[sch];
    const fmt = new Intl.DateTimeFormat("en-u-ca-" + art, { timeZone: "UTC", month: art === "hebrew" ? "long" : "numeric", day: "numeric" });
    const r = {};
    for (let d = tag(y, 1, 1); d.getUTCFullYear() === y; d = plus(d, 1)) {
      const p = fmt.formatToParts(d), m = p.find(x => x.type === "month").value, t = p.find(x => x.type === "day").value;
      (r[`${m}-${t}`] ||= []).push(d);
    }
    return (KAL[sch] = r);
  }
  const hijri = (y, m, d) => kalender(y, "islamic-umalqura")[`${m}-${d}`] || [];
  const hebr = (y, m, d) => kalender(y, "hebrew")[`${m}-${d}`] || [];

  // ---- Regeln: [Regel, Motiv, Name EN, Name DE, Bedingung] ----
  // Regel: "M-T" fest · "E±n" Ostern · "O±n" orth. Ostern · "W:Monat:Wochentag:n" · "H:Monat:Tag[:Tage]" islamisch · Funktion(y)
  const SONNTAG_NICHT = (y, d) => d.getUTCDay() !== 0;   // (Spanien: fällt auf Sonntag → nicht im Kalender)
  const L = {
    AT: [["1-1","f_neujahr"],["1-6","f_drei_koenige"],["E+1","f_ostermontag"],["5-1","f_tag_der_arbeit"],["E+39","f_himmelfahrt"],["E+50","f_pfingstmontag"],
         ["E+60","w_laender_fronleichnam"],["8-15","w_laender_mariae_himmelfahrt"],["10-26","w_laender_at_nationalfeiertag"],["11-1","f_allerheiligen"],
         ["12-8","w_laender_mariae_empfaengnis"],["12-25","f_weihnachten_1"],["12-26","f_weihnachten_2"]],
    CH: [["1-1","f_neujahr"],["E-2","f_karfreitag"],["E+1","f_ostermontag"],["E+39","f_himmelfahrt"],["E+50","f_pfingstmontag"],["8-1","w_laender_ch_bundesfeier"],
         ["12-25","f_weihnachten_1"],["12-26","f_weihnachten_2"]],
    LI: [["1-1","f_neujahr","New Year's Day","Neujahr"],["1-6","f_drei_koenige","Epiphany","Heilige Drei Könige"],["2-2","f_allerheiligen","Candlemas","Mariä Lichtmess"],
         ["3-19","n_lorbeer","Saint Joseph's Day","Josefstag"],["E+0","f_ostersonntag","Easter Sunday","Ostersonntag"],["E+1","f_ostermontag","Easter Monday","Ostermontag"],
         ["5-1","f_tag_der_arbeit","Labor Day","Tag der Arbeit"],["E+39","f_himmelfahrt","Ascension Day","Christi Himmelfahrt"],["E+49","f_pfingstmontag","Pentecost","Pfingstsonntag"],
         ["E+50","f_pfingstmontag","Pentecost Monday","Pfingstmontag"],["E+60","w_laender_fronleichnam","Corpus Christi","Fronleichnam"],["8-15","n_flagge_LI","National Day","Nationalfeiertag"],
         ["9-8","w_laender_mariae_empfaengnis","Nativity of Mary","Mariä Geburt"],["11-1","f_allerheiligen","All Saints' Day","Allerheiligen"],
         ["12-8","w_laender_mariae_empfaengnis","Immaculate Conception","Mariä Empfängnis"],["12-25","f_weihnachten_1","Christmas Day","1. Weihnachtstag"],["12-26","f_weihnachten_2","Saint Stephen's Day","Stephanstag"]],
    LU: [["1-1","f_neujahr","New Year's Day","Neujahr"],["E+1","f_ostermontag","Easter Monday","Ostermontag"],["5-1","f_tag_der_arbeit","Labor Day","Tag der Arbeit"],
         ["5-9","n_europa","Europe Day","Europatag"],["E+39","f_himmelfahrt","Ascension Day","Christi Himmelfahrt"],["E+50","f_pfingstmontag","Pentecost Monday","Pfingstmontag"],
         ["6-23","n_flagge_LU","National Day","Nationalfeiertag"],["8-15","w_laender_mariae_himmelfahrt","Assumption Day","Mariä Himmelfahrt"],["11-1","f_allerheiligen","All Saints' Day","Allerheiligen"],
         ["12-25","f_weihnachten_1","Christmas Day","1. Weihnachtstag"],["12-26","f_weihnachten_2","Saint Stephen's Day","Stephanstag"]],
    BE: [["1-1","f_neujahr","New Year's Day","Neujahr"],["E+0","f_ostersonntag","Easter Sunday","Ostersonntag"],["E+1","f_ostermontag","Easter Monday","Ostermontag"],
         ["5-1","f_tag_der_arbeit","Labor Day","Tag der Arbeit"],["E+39","f_himmelfahrt","Ascension Day","Christi Himmelfahrt"],["E+49","f_pfingstmontag","Pentecost","Pfingstsonntag"],
         ["E+50","f_pfingstmontag","Pentecost Monday","Pfingstmontag"],["7-21","n_flagge_BE","National Day","Nationalfeiertag"],["8-15","w_laender_mariae_himmelfahrt","Assumption Day","Mariä Himmelfahrt"],
         ["11-1","f_allerheiligen","All Saints' Day","Allerheiligen"],["11-11","n_mohn","Armistice Day","Waffenstillstandstag"],["12-25","f_weihnachten_1","Christmas Day","1. Weihnachtstag"]],
    NL: [["1-1","f_neujahr","New Year's Day","Neujahr"],["E-2","f_karfreitag","Good Friday","Karfreitag"],["E+0","f_ostersonntag","Easter Sunday","Ostersonntag"],
         ["E+1","f_ostermontag","Easter Monday","Ostermontag"],[y => koningsdag(y),"w_laender_nl_koningsdag","King's Day","Königstag"],
         ["5-5","n_taube","Liberation Day","Tag der Befreiung",y => y % 5 === 0],
         ["E+39","f_himmelfahrt","Ascension Day","Christi Himmelfahrt"],["E+49","f_pfingstmontag","Pentecost","Pfingstsonntag"],["E+50","f_pfingstmontag","Pentecost Monday","Pfingstmontag"],
         ["12-25","f_weihnachten_1","Christmas Day","1. Weihnachtstag"],["12-26","f_weihnachten_2","Second Day of Christmas","2. Weihnachtstag"]],
    FR: [["1-1","f_neujahr","New Year's Day","Neujahr"],["E+1","f_ostermontag","Easter Monday","Ostermontag"],["5-1","f_tag_der_arbeit","Labor Day","Tag der Arbeit"],
         ["5-8","n_taube","Victory Day","Tag des Sieges"],["E+39","f_himmelfahrt","Ascension Day","Christi Himmelfahrt"],["E+50","f_pfingstmontag","Pentecost Monday","Pfingstmontag"],
         ["7-14","w_laender_fr_nationalfeiertag","National Day","Nationalfeiertag"],["8-15","w_laender_mariae_himmelfahrt","Assumption Day","Mariä Himmelfahrt"],
         ["11-1","f_allerheiligen","All Saints' Day","Allerheiligen"],["11-11","n_mohn","Armistice Day","Waffenstillstandstag"],["12-25","f_weihnachten_1","Christmas Day","1. Weihnachtstag"]],
    IT: [["1-1","f_neujahr","New Year's Day","Neujahr"],["1-6","f_drei_koenige","Epiphany","Heilige Drei Könige"],["E+0","f_ostersonntag","Easter Sunday","Ostersonntag"],
         ["E+1","f_ostermontag","Easter Monday","Ostermontag"],["4-25","n_taube","Liberation Day","Tag der Befreiung"],["5-1","f_tag_der_arbeit","Labor Day","Tag der Arbeit"],
         ["6-2","n_flagge_IT","Republic Day","Tag der Republik"],["8-15","w_laender_mariae_himmelfahrt","Assumption Of Mary Day","Mariä Himmelfahrt"],
         ["10-4","n_lorbeer","Saint Francis of Assisi, Patron Saint of Italy","Franz von Assisi (Schutzpatron)",y => y >= 2026],
         ["11-1","f_allerheiligen","All Saints' Day","Allerheiligen"],["W:11:0:1","n_flagge_IT","National Unity Day","Tag der nationalen Einheit",y => y >= 2026],
         ["12-8","w_laender_mariae_empfaengnis","Immaculate Conception","Mariä Empfängnis"],["12-25","f_weihnachten_1","Christmas Day","1. Weihnachtstag"],["12-26","f_weihnachten_2","Saint Stephen's Day","Stephanstag"]],
    ES: [["1-1","f_neujahr","New Year's Day","Neujahr"],["1-6","f_drei_koenige","Epiphany","Heilige Drei Könige",SONNTAG_NICHT],["E-2","f_karfreitag","Good Friday","Karfreitag"],
         ["5-1","f_tag_der_arbeit","Labor Day","Tag der Arbeit"],["8-15","w_laender_mariae_himmelfahrt","Assumption Day","Mariä Himmelfahrt",SONNTAG_NICHT],
         ["10-12","n_flagge_ES","National Day","Nationalfeiertag"],["11-1","f_allerheiligen","All Saints' Day","Allerheiligen",SONNTAG_NICHT],
         ["12-6","n_paragraph","Constitution Day","Verfassungstag",SONNTAG_NICHT],["12-8","w_laender_mariae_empfaengnis","Immaculate Conception","Mariä Empfängnis",SONNTAG_NICHT],
         ["12-25","f_weihnachten_1","Christmas Day","1. Weihnachtstag"]],
    PT: [["1-1","f_neujahr","New Year's Day","Neujahr"],["E-2","f_karfreitag","Good Friday","Karfreitag"],["E+0","f_ostersonntag","Easter Sunday","Ostersonntag"],
         ["4-25","n_taube","Freedom Day","Tag der Freiheit"],["5-1","f_tag_der_arbeit","Labor Day","Tag der Arbeit"],["E+60","w_laender_fronleichnam","Corpus Christi","Fronleichnam"],
         ["6-10","n_flagge_PT","Day of Portugal, Camões, and the Portuguese Communities","Tag Portugals"],["8-15","w_laender_mariae_himmelfahrt","Assumption Day","Mariä Himmelfahrt"],
         ["10-5","n_flagge_PT","Republic Day","Tag der Republik"],["11-1","f_allerheiligen","All Saints' Day","Allerheiligen"],
         ["12-1","n_flagge_PT","Restoration of Independence Day","Wiederherstellung der Unabhängigkeit"],["12-8","w_laender_mariae_empfaengnis","Immaculate Conception","Mariä Empfängnis"],
         ["12-25","f_weihnachten_1","Christmas Day","1. Weihnachtstag"]],
    PL: [["1-1","f_neujahr","New Year's Day","Neujahr"],["1-6","f_drei_koenige","Epiphany","Heilige Drei Könige"],["E+0","f_ostersonntag","Easter Sunday","Ostersonntag"],
         ["E+1","f_ostermontag","Easter Monday","Ostermontag"],["5-1","f_tag_der_arbeit","Labour Day","Tag der Arbeit"],["5-3","n_paragraph","National Day of the Third of May","Verfassungstag (3. Mai)"],
         ["E+49","f_pfingstmontag","Pentecost","Pfingstsonntag"],["E+60","w_laender_fronleichnam","Corpus Christi","Fronleichnam"],["8-15","w_laender_mariae_himmelfahrt","Assumption Day","Mariä Himmelfahrt"],
         ["11-1","f_allerheiligen","All Saints' Day","Allerheiligen"],["11-11","n_flagge_PL","National Independence Day","Unabhängigkeitstag"],
         ["12-24","f_heiligabend","Christmas Eve","Heiligabend",y => y >= 2025],["12-25","f_weihnachten_1","Christmas Day","1. Weihnachtstag"],["12-26","f_weihnachten_2","Second Day of Christmas","2. Weihnachtstag"]],
    CZ: [["1-1","n_flagge_CZ","Independent Czech State Restoration Day","Tag der Erneuerung des Staates"],["1-1","f_neujahr","New Year's Day","Neujahr"],
         ["E-2","f_karfreitag","Good Friday","Karfreitag"],["E+1","f_ostermontag","Easter Monday","Ostermontag"],["5-1","f_tag_der_arbeit","Labor Day","Tag der Arbeit"],
         ["5-8","n_taube","Victory Day","Tag des Sieges"],["7-5","n_lorbeer","Saints Cyril and Methodius Day","Tag der Heiligen Kyrill und Method"],["7-6","n_lorbeer","Jan Hus Day","Jan-Hus-Tag"],
         ["9-28","n_flagge_CZ","Statehood Day","Tag der Eigenstaatlichkeit"],["10-28","n_flagge_CZ","Independent Czechoslovak State Day","Gründung der Tschechoslowakei"],
         ["11-17","n_taube","Struggle for Freedom and Democracy Day","Tag des Kampfes für Freiheit und Demokratie"],["12-24","f_heiligabend","Christmas Eve","Heiligabend"],
         ["12-25","f_weihnachten_1","Christmas Day","1. Weihnachtstag"],["12-26","f_weihnachten_2","Second Day of Christmas","2. Weihnachtstag"]],
    DK: [["1-1","f_neujahr","New Year's Day","Neujahr"],["E-3","n_kelch","Maundy Thursday","Gründonnerstag"],["E-2","f_karfreitag","Good Friday","Karfreitag"],
         ["E+0","f_ostersonntag","Easter Sunday","Ostersonntag"],["E+1","f_ostermontag","Easter Monday","Ostermontag"],["E+39","f_himmelfahrt","Ascension Day","Christi Himmelfahrt"],
         ["E+49","f_pfingstmontag","Pentecost","Pfingstsonntag"],["E+50","f_pfingstmontag","Pentecost Monday","Pfingstmontag"],["12-25","f_weihnachten_1","Christmas Day","1. Weihnachtstag"],
         ["12-26","f_weihnachten_2","Second Day of Christmas","2. Weihnachtstag"]],
    GR: [["1-1","f_neujahr","New Year's Day","Neujahr"],["1-6","f_drei_koenige","Epiphany","Heilige Drei Könige"],["O-48","n_drachen","Green Monday","Rosenmontag (orthodox)"],
         ["3-25","n_flagge_GR","Independence Day","Unabhängigkeitstag"],["O-2","f_karfreitag","Good Friday","Karfreitag"],["O+1","f_ostermontag","Easter Monday","Ostermontag"],
         ["5-1","f_tag_der_arbeit","Labor Day","Tag der Arbeit"],["O+50","f_pfingstmontag","Pentecost Monday","Pfingstmontag"],
         ["8-15","w_laender_mariae_himmelfahrt","Dormition of the Mother of God","Mariä Entschlafung"],["10-28","n_flagge_GR","Ohi Day","Ochi-Tag (Nationalfeiertag)"],
         ["12-25","f_weihnachten_1","Christmas Day","1. Weihnachtstag"],["12-26","n_lorbeer","Glorifying Mother of God","Synaxis der Gottesmutter"]],
    HR: [["1-1","f_neujahr","New Year's Day","Neujahr"],["1-6","f_drei_koenige","Epiphany","Heilige Drei Könige"],["E+0","f_ostersonntag","Easter Sunday","Ostersonntag"],
         ["E+1","f_ostermontag","Easter Monday","Ostermontag"],["5-1","f_tag_der_arbeit","Labor Day","Tag der Arbeit"],["5-30","n_flagge_HR","Statehood Day","Tag der Eigenstaatlichkeit"],
         ["E+60","w_laender_fronleichnam","Corpus Christi","Fronleichnam"],["6-22","n_taube","Anti-Fascist Struggle Day","Tag des antifaschistischen Kampfes"],
         ["8-5","n_taube","Victory and Homeland Thanksgiving Day","Tag des Sieges und der Heimatdankbarkeit"],["8-15","w_laender_mariae_himmelfahrt","Assumption Day","Mariä Himmelfahrt"],
         ["11-1","f_allerheiligen","All Saints' Day","Allerheiligen"],["11-18","n_mohn","Remembrance Day","Gedenktag"],["12-25","f_weihnachten_1","Christmas Day","1. Weihnachtstag"],
         ["12-26","f_weihnachten_2","Saint Stephen's Day","Stephanstag"]],
    TR: [["1-1","f_neujahr","New Year's Day","Neujahr"],["H:10:1:3","i_zuckerfest","Eid al-Fitr","Zuckerfest"],
         ["4-23","w_international_weltkindertag","National Sovereignty and Children's Day","Tag der nationalen Souveränität und Kinderfest"],
         ["5-1","f_tag_der_arbeit","Labour and Solidarity Day","Tag der Arbeit"],["5-19","n_lorbeer","Commemoration of Atatürk, Youth and Sports Day","Gedenken an Atatürk, Tag der Jugend und des Sports"],
         ["H:12:10:4","i_opferfest","Eid al-Adha","Opferfest"],["7-15","n_flagge_TR","Democracy and National Unity Day","Tag der Demokratie und nationalen Einheit"],
         ["8-30","n_taube","Victory Day","Tag des Sieges"],["10-29","n_flagge_TR","Republic Day","Tag der Republik"]],
    GB: [["1-1","f_neujahr","New Year's Day","Neujahr"],["E-2","f_karfreitag","Good Friday","Karfreitag"],["W:5:1:1","f_tag_der_arbeit","May Day","Maifeiertag"],
         ["W:5:1:-1","n_liegestuhl","Spring Bank Holiday","Bank Holiday (Frühling)"],["12-25","f_weihnachten_1","Christmas Day","1. Weihnachtstag"],
         ["12-26","f_weihnachten_2","Boxing Day","2. Weihnachtstag (Boxing Day)"]],
    IE: [["1-1","f_neujahr","New Year's Day","Neujahr"],[y => tag(y, 2, 1).getUTCDay() === 5 ? tag(y, 2, 1) : wtag(y, 2, 1, 1),"n_lorbeer","Saint Brigid's Day","St. Brigid's Day"],
         ["3-17","w_laender_ie_st_patrick","Saint Patrick's Day","St. Patrick's Day"],["E+1","f_ostermontag","Easter Monday","Ostermontag"],["W:5:1:1","f_tag_der_arbeit","May Day","Maifeiertag"],
         ["W:6:1:1","n_liegestuhl","June Bank Holiday","Bank Holiday (Juni)"],["W:8:1:1","n_liegestuhl","August Bank Holiday","Bank Holiday (August)"],
         ["W:10:1:-1","n_liegestuhl","October Bank Holiday","Bank Holiday (Oktober)"],["12-25","f_weihnachten_1","Christmas Day","1. Weihnachtstag"],
         ["12-26","f_weihnachten_2","Saint Stephen's Day","Stephanstag"]],
    US: [["1-1","f_neujahr","New Year's Day","Neujahr"],["W:1:1:3","n_lorbeer","Martin Luther King Jr. Day","Martin-Luther-King-Tag"],["W:2:1:3","n_lorbeer","Washington's Birthday","Presidents' Day"],
         ["W:5:1:-1","n_mohn","Memorial Day","Memorial Day (Gedenktag)"],["6-19","n_taube","Juneteenth National Independence Day","Juneteenth"],
         ["7-4","w_laender_us_independence","Independence Day","Unabhängigkeitstag"],["W:9:1:1","f_tag_der_arbeit","Labor Day","Tag der Arbeit"],
         ["W:10:1:2","n_lorbeer","Columbus Day","Columbus Day"],["11-11","n_mohn","Veterans Day","Veteranentag"],["W:11:4:4","w_laender_us_thanksgiving","Thanksgiving Day","Thanksgiving"],
         ["12-25","f_weihnachten_1","Christmas Day","1. Weihnachtstag"]],
    CA: [["1-1","f_neujahr","New Year's Day","Neujahr"],["E-2","f_karfreitag","Good Friday","Karfreitag"],["7-1","n_flagge_CA","Canada Day","Canada Day (Nationalfeiertag)"],
         ["W:9:1:1","f_tag_der_arbeit","Labor Day","Tag der Arbeit"],["12-25","f_weihnachten_1","Christmas Day","1. Weihnachtstag"]],
  };
  // Deutschland: [Regel, Motiv, nur in diesen Bundesländern]
  const DE = [["1-1","f_neujahr"],["1-6","f_drei_koenige",["BW","BY","ST"]],["3-8","f_frauentag",["BE","MV"]],["E-2","f_karfreitag"],["E+1","f_ostermontag"],
    ["5-1","f_tag_der_arbeit"],["E+39","f_himmelfahrt"],["E+50","f_pfingstmontag"],["E+60","w_laender_fronleichnam",["BW","BY","HE","NW","RP","SL"]],
    ["8-15","w_laender_mariae_himmelfahrt",["SL","BY"]],["9-20","w_international_weltkindertag",["TH"]],["10-3","f_einheit"],
    ["10-31","f_reformationstag",["BB","HB","HH","MV","NI","SN","ST","SH","TH"]],["11-1","f_allerheiligen",["BW","BY","NW","RP","SL"]],
    [y => plus(tag(y, 11, 23), -((tag(y, 11, 23).getUTCDay() + 4) % 7 || 7)),"w_laender_buss_bettag",["SN"]],["12-25","f_weihnachten_1"],["12-26","f_weihnachten_2"]];
  function koningsdag(y) { const d = tag(y, 4, 27); return d.getUTCDay() === 0 ? plus(d, -1) : d; }

  function daten(y, regel) {                             // Regel → Liste von Daten
    if (typeof regel === "function") return [regel(y)];
    if (regel[0] === "E") return [plus(ostern(y), +regel.slice(1))];
    if (regel[0] === "O") return [plus(ostern_orth(y), +regel.slice(1))];
    if (regel[0] === "W") { const [, m, wd, n] = regel.split(":").map(Number); return [wtag(y, m, wd, n)]; }
    if (regel[0] === "H") {
      const [, m, d, n = 1] = regel.split(":").map(Number), r = [];
      for (const start of hijri(y, m, d)) for (let i = 0; i < n; i++) if (plus(start, i).getUTCFullYear() === y) r.push(plus(start, i));
      return r;
    }
    const [m, d] = regel.split("-").map(Number); return [tag(y, m, d)];
  }
  const NATIONAL = [  // Nationalfeiertage der anderen Länder (Kästchen „Andere Länder“)
    ["10-3","f_einheit","German Unity Day","Tag der Deutschen Einheit","DE"],["10-26","w_laender_at_nationalfeiertag","Austrian National Day","Nationalfeiertag Österreich","AT"],
    ["8-1","w_laender_ch_bundesfeier","Swiss National Day","Schweizer Bundesfeier","CH"],["8-15","n_flagge_LI","Liechtenstein National Day","Staatsfeiertag Liechtenstein","LI"],
    ["6-23","n_flagge_LU","Luxembourg National Day","Nationalfeiertag Luxemburg","LU"],["7-21","n_flagge_BE","Belgian National Day","Nationalfeiertag Belgien","BE"],
    [koningsdag,"w_laender_nl_koningsdag","King's Day (Netherlands)","Königstag Niederlande","NL"],["7-14","w_laender_fr_nationalfeiertag","Bastille Day (France)","Nationalfeiertag Frankreich","FR"],
    ["6-2","n_flagge_IT","Republic Day (Italy)","Tag der Republik Italien","IT"],["10-12","n_flagge_ES","National Day of Spain","Nationalfeiertag Spanien","ES"],
    ["6-10","n_flagge_PT","Portugal Day","Nationalfeiertag Portugal","PT"],["11-11","n_flagge_PL","Independence Day (Poland)","Unabhängigkeitstag Polen","PL"],
    ["10-28","n_flagge_CZ","Independent Czechoslovak State Day","Staatsgründungstag Tschechien","CZ"],["6-5","n_flagge_DK","Constitution Day (Denmark)","Verfassungstag Dänemark","DK"],
    ["3-25","n_flagge_GR","Independence Day (Greece)","Unabhängigkeitstag Griechenland","GR"],["5-30","n_flagge_HR","Statehood Day (Croatia)","Tag der Staatlichkeit Kroatien","HR"],
    ["10-29","n_flagge_TR","Republic Day (Türkiye)","Tag der Republik Türkei","TR"],["3-17","w_laender_ie_st_patrick","St. Patrick's Day (Ireland)","St. Patrick's Day Irland","IE"],
    ["7-4","w_laender_us_independence","Independence Day (USA)","Unabhängigkeitstag USA","US"],["W:11:4:4","w_laender_us_thanksgiving","Thanksgiving (USA)","Thanksgiving USA","US"],
    ["7-1","n_flagge_CA","Canada Day","Kanadatag","CA"],["11-2","w_laender_mx_dia_muertos","Day of the Dead (Mexico)","Tag der Toten Mexiko","MX"]];
  // Diwali, Holi, Vesakh hängen am indischen Mondkalender – den kann der Browser nicht, daher feste (geprüfte) Daten
  const HINDU = { 2026: { diwali: "11-8" }, 2027: { diwali: "10-29", holi: "3-22", vesakh: "5-20" } };
  const HINDU_NAMEN = { diwali: "Diwali", holi: "Holi", vesakh: "Vesakh" };

  const CACHE = {};
  function jahr(y) {
    if (CACHE[y]) return CACHE[y];
    const r = {}, add = (g, d, ...rest) => (r[g] ||= []).push([md(d), ...rest]);
    for (const [regel, k, nur] of DE) for (const d of daten(y, regel)) add("gesetzlich", d, k, nur || null);
    for (const [land, liste] of Object.entries(L))
      for (const [regel, k, en, de, bed] of liste)
        for (const d of daten(y, regel)) if (!bed || bed(y, d)) add("gesetzlich_" + land, d, k, null, ...(en ? [en, de] : []));
    const e = ostern(y);
    for (const [d, k] of [[tag(y, 2, 14), "f_valentinstag"], [e, "f_ostersonntag"], [wtag(y, 5, 0, 2), "f_muttertag"], [tag(y, 10, 31), "f_halloween"],
                          [tag(y, 12, 6), "f_nikolaus"], [tag(y, 12, 24), "f_heiligabend"], [tag(y, 12, 31), "f_silvester"]]) add("feste", d, k);
    for (const [m, t, k] of [[7, 27, "i_isra_miraj"], [8, 15, "i_baraa"], [9, 1, "i_ramadan"], [9, 27, "i_qadr"], [10, 1, "i_zuckerfest"],
                             [12, 9, "i_arafat"], [12, 10, "i_opferfest"], [1, 1, "i_neujahr"], [1, 10, "i_aschura"], [3, 12, "i_mawlid"]])
      for (const d of hijri(y, m, t)) add("islamisch", d, k);
    const adar = Object.keys(kalender(y, "hebrew")).some(s => s.startsWith("Adar II")) ? "Adar II" : "Adar";
    for (const [m, t, k] of [["Tishri", 1, "rosch_haschana"], ["Tishri", 10, "jom_kippur"], ["Tishri", 15, "sukkot"], ["Kislev", 25, "chanukka"],
                             ["Nisan", 15, "pessach"], [adar, 14, "purim"]])
      for (const d of hebr(y, m, t)) add("juedisch", d, "w_religionen_" + k);
    add("orthodox", tag(y, 1, 7), "w_religionen_orth_weihnachten"); add("orthodox", ostern_orth(y), "w_religionen_orth_ostern");
    r.hindu = Object.entries(HINDU[y] || {}).map(([k, d]) => [d, "w_religionen_" + k]);
    for (const [regel, k, en, de, land] of NATIONAL) for (const d of daten(y, regel)) add("laender", d, k, null, en, de, land);
    for (const [d, k] of [[chin_neujahr(y), "chin_neujahr"], [tag(y, 3, 22), "weltwassertag"], [tag(y, 4, 22), "tag_der_erde"], [tag(y, 4, 23), "welttag_buch"],
                          [tag(y, 4, 25), "tag_des_baumes"], [tag(y, 6, 5), "weltumwelttag"], [tag(y, 6, 21), "fete_musique"], [tag(y, 7, 30), "freundschaft"],
                          [tag(y, 9, 20), "weltkindertag"], [tag(y, 10, 4), "welttierschutztag"], [tag(y, 10, 30), "weltspartag"], [wtag(y, 5, 0, 1), "weltlachtag"],
                          [tag(y, 11, 19), "maennertag"]]) add("international", d, "w_international_" + k);
    for (const [d, k] of [[tag(y, 2, 9), "pizza"], [tag(y, 3, 14), "pi"], [tag(y, 5, 4), "weltraum"], [tag(y, 4, 25), "pinguin"], [tag(y, 7, 7), "schokolade"],
                          [tag(y, 7, 17), "emoji"], [tag(y, 7, 13), "pommes"], [wtag(y, 7, 0, 3), "eis"], [tag(y, 8, 8), "katze"], [tag(y, 8, 26), "hund"],
                          [tag(y, 10, 1), "kaffee"], [tag(y, 12, 4), "keks"]]) add("aktion", d, "w_aktionstage_" + k);
    ["j_fruehling", "j_sommer", "j_herbst", "j_winter"].forEach((k, i) => add("jahreszeiten", jahreszeit(y, i), k));
    return (CACHE[y] = r);
  }
  const fehlt = y => Object.keys(HINDU_NAMEN).filter(k => !(HINDU[y] || {})[k]).map(k => HINDU_NAMEN[k]);
  return { jahr, fehlt, ostern, ostern_orth, jahreszeit, chin_neujahr };
})();
if (typeof module !== "undefined") module.exports = FEIERTAGE;
