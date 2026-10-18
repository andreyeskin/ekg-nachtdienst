/* Prototyp Fall 1 „Darf Herr Baum heim?" — die Geschichte (docs/REDESIGN_FALL1.md §3–§7, §14, §15).

   Repliken, Optionen, Rückmeldungen und Karten wörtlich aus dem Drehbuch; Belege in Klammern stehen dort,
   nie im Spiel. Messwerte nur als Platzhalter ({hf}, {pq}, {qrs}, {mess_pq}); feste Fallwerte über `werte`
   (wie web/faelle/aufnahme_baum.js). Wo das Drehbuch eine Lücke hat, steht eine kurze Zeile mit dem Vermerk
   NEU (Liste im Bericht). Der Motor (motor.js) stellt `P` bereit.                                          */
(function (global) {
  "use strict";
  var P = global.P;
  function hat(f) { return P.hat(f); }
  function setze(f) { P.setze(f); }
  function X() { return P.Z.x; }
  var FALK = P.FALK_MIN;

  /* ================================================================ Verdachtsliste (§4.1) */
  var VERDACHT = [
    { id: "reflex", name: "Reflex (vasovagal, situativ)", kurz: "Reflex" },
    { id: "kreislauf", name: "Kreislauf im Stehen (orthostatisch)", kurz: "Kreislauf im Stehen" },
    { id: "rhythmus", name: "Herzrhythmus (Pause, Block, Rasen)", kurz: "Herzrhythmus" },
    { id: "struktur", name: "Herz-Struktur (Klappe, Muskel, Durchblutung)", kurz: "Herz-Struktur" },
    { id: "krampf", name: "Krampfanfall", kurz: "Krampfanfall" },
    { id: "tia", name: "Schlaganfall / TIA", kurz: "Schlaganfall / TIA" },
    { id: "zucker", name: "Unterzucker", kurz: "Unterzucker" },
    { id: "sturz", name: "Sturz ohne Bewusstlosigkeit", kurz: "Sturz ohne Bewusstlosigkeit" }
  ];
  var vd = function (id, z, g) { P.verdacht(id, z, g); };

  /* ================================================================ Karten der Mappe */
  function zeilen(liste) { return liste.filter(function (z) { return z; }).join("\n"); }
  var KARTEN = {
    bogen: {
      titel: "Aufnahmebogen",
      text: "Triage 06:20. Puls {puls}/min, regelmäßig. Blutdruck liegend {rr_l_sys}/{rr_l_dia}, nach 1 min Stehen " +
        "{rr_s1_sys}/{rr_s1_dia}, nach 3 min {rr_s3_sys}/{rr_s3_dia}, ohne Schwindel. SpO₂ {spo2} %, {temp} °C, " +
        "Blutzucker {zucker} mg/dl. Schürfung linker Ellbogen, blauer Fleck linke Hüfte. Labor abgenommen 06:30. " +
        "Notiz Dr. Steiner 06:25: V. a. vasovagale Synkope, Schellong unauffällig, EKG ausständig."
    },
    /* Die Anamnese-Karte hat im Drehbuch keinen Text: sie sammelt, was er geantwortet hat (seine Worte, knapp). */
    anamnese: {
      titel: "Anamnese",
      text: function () {
        return zeilen([
          hat("r1_erz") && "Küche, beim Wasserkocher: auf einmal am Boden, dazwischen nichts.",
          hat("r1_1") && "Keine Vorwarnung.",
          hat("r1_2") && "Seit sechs auf, eine Minute beim Kocher gestanden; nicht beim Aufstehen.",
          hat("r1_3") && "Laut Tochter eine halbe Minute weg, danach gleich klar.",
          hat("r1_4") && "Schürfung Ellbogen, blauer Fleck Hüfte: Verletzung durch die Synkope.",
          hat("r1_5") && "Gezuckt? Weiß er nicht, die Tochter fragen.",
          hat("r2_2") && "Kein Zucker. Blutdruck seit zehn Jahren, das Knie, das Hörgerät.",
          hat("r2_3") && "Herz nie gespürt, kein Druck; bergauf langsamer, aber er kommt rauf.",
          hat("r2_4") && "Danach geredet, gesehen, gehört.",
          hat("r2_5") && "Ein Bier am Sonntag, keine Schlafmittel.",
          hat("r3_1") && "Familie: Vater mit 80 Schlaganfall, Mutter 91; niemand jung und plötzlich.",
          hat("zweites_ereignis") && "Gestern an der Haltestelle beim Friedhof schon einmal weg, ohne Vorwarnung; niemandem gesagt.",
          hat("r3_n2") && "Gestern eine Viertelstunde gestanden.",
          hat("r3_n3") && "Gestern nicht verletzt."
        ]);
      }
    },
    medis: {
      titel: "Medikamente (Medikationsplan)",
      text: function () {
        return "{medi1}, {medi2}, {medi3}, 1-0-0" + (hat("r2_1b") ? ", seit Jahren unverändert" : "") +
          (hat("heute_nicht") ? "; heute noch nicht genommen (zuletzt gestern früh)" : "") +
          ". Der Betablocker bremst Sinusknoten und AV-Knoten: Er erklärt eine langsame Frequenz und eine zähe " +
          "Überleitung, aber keine Bewusstlosigkeit ohne Vorwarnung.";
      }
    },
    fremd: {
      titel: "Fremdanamnese (Tochter)",
      text: "Krach gehört, am Boden gefunden, grau, Augen offen, kein Zucken, kein Zungenbiss, nach 20–30 s " +
        "angesprochen und sofort klar. Tabletten heute nicht genommen."
    },
    unters: {
      titel: "Kurzuntersuchung",
      text: "Puls am Handgelenk langsam, regelmäßig. Herztöne regelmäßig, langsam, kein Geräusch. Lunge frei, keine " +
        "Beinödeme. Schürfung linker Ellbogen, blauer Fleck linke Hüfte. Sprache klar, Gesicht symmetrisch, Arme und " +
        "Beine seitengleich kräftig, kein Doppeltsehen, Finger-Nase sicher."
    },
    rhythmus: {
      titel: "Rhythmus: Sinus",
      text: "Vor jedem QRS eine P-Welle, in II positiv, die Abstände gleich. Der Sinusknoten führt.",
      ekg: { mmProS: 25, von: 1.8, dauer: 6 }
    },
    frequenz: {
      titel: "Frequenz: {hf}/min",
      text: "RR {rr} ms. 60 000 : {rr} = {hf} pro Minute. Im Kurs heißt Sinusbradykardie unter 50 (so auch die " +
        "Synkopen-Leitlinie); andere Quellen sagen 60, und der Datensatz nennt diese Kurve Sinusbradykardie. " +
        "Wichtiger: unter Betablocker erwartbar, nicht verdächtig.",
      ekg: { mmProS: 25, von: 1.9, dauer: 6 }
    },
    pq: {
      titel: "PQ-Zeit: {pq} ms",
      text: function () {
        return "{pq} ms, über 200: AV-Block I°. Damit ist das EKG nicht normal. Mehr sagt es nicht: jeder " +
          "Vorhofimpuls kommt an, keine Pause, kein ausgefallener Schlag in zehn Sekunden. Der P-Beginn liegt nie " +
          "ganz scharf; von Schlag zu Schlag schwanken die Werte um einige Millisekunden. Im Zweifel mehrere " +
          "Schläge messen." + (hat("falk_zirkel") ? "\nVon Dr. Falk nachgemessen: {mess_pq} ms (Median aller Schläge)." : "");
      },
      ekg: { mmProS: 50, von: 2.9, dauer: 2.4 }
    },
    qrs: {
      titel: "QRS-Breite: {qrs} ms",
      text: "{qrs} ms, schmal. Die Kammern laufen über das normale Leitungssystem; die Bremse sitzt oben, in der Überleitung.",
      ekg: { mmProS: 50, von: 2.9, dauer: 2.4 }
    },
    /* Die Karte ordnet die Zeilen wieder richtig (I, S, B, A, R) und sagt, warum Falk umgestellt hat (§6.2). */
    uebergabe: {
      titel: "Übergabe (ISBAR)",
      text: function () {
        var u = X().ueb || {};
        return zeilen([
          "I/S: " + (u.is || "…"),
          "B: " + ((u.b && u.b.length) ? u.b.join(" ") : "…"),
          "A: " + (u.a || "…"),
          "R: " + ((u.r && u.r.length) ? u.r.join(" ") : "…"),
          "Falk hat das EKG vorgezogen, weil er zuerst die Zahlen hören will."          /* NEU */
        ]);
      }
    },
    entscheidung: {
      titel: "Entscheidung",
      text: "Beobachtung am Monitor; Bisoprolol heute pausiert, Ramipril und ASS gegeben; Dr. Falk."
    },
    epilog: {
      titel: "Epilog: Was der Monitor gezeigt hat",
      text: "Pause über drei Sekunden (Sinusstillstand oder Block, der Speicher sagt's), im Wachen, mit Beschwerden, " +
        "ohne bremsendes Medikament (letzte Bisoprolol-Dosis Sonntag früh, zweite Nacht rund 65 Stunden später, mehr " +
        "als fünf Halbwertszeiten, also praktisch nichts mehr da): eines der Kriterien, die eine arrhythmische Synkope " +
        "beweisen. Weil der Betablocker nicht mehr beteiligt war, war die Ursache nicht reversibel; deshalb " +
        "Schrittmacher, Zweikammer, statt Abwarten."
    }
  };

  /* Vergleiche in der Mappe (§5.9) */
  var VERGLEICHE = [
    { a: "pq", b: "medis", text: "Der Betablocker bremst beide Etagen: Taktgeber und Überleitung. Die Ohnmacht erklärt er trotzdem nicht." },
    { a: "rhythmus", b: "anamnese", text: "Zehn Sekunden Papier gegen zwei Ohnmachten. Der Streifen war nicht dabei. Was er beweisen könnte, hat er nicht gezeigt: keine Pause, kein Block mit ausgefallenen Schlägen." },
    { a: "frequenz", b: "bogen", text: "Puls {puls} getastet, {hf} gemessen: dieselbe Zahl." }
  ];

  /* ================================================================ kleine Abläufe */
  function bogenGelesen() {
    if (P.karte("bogen")) {
      vd("reflex", "dafuer", "Notiz 06:25: V. a. vasovagal");
      vd("kreislauf", "dagegen", "kein Abfall nach drei Minuten Stehen");
      vd("zucker", "dagegen", "{zucker}, kein Diabetes");
    }
  }
  function anamnese() { P.karte("anamnese"); }

  function untersuchung(dann) {
    P.befund({
      titel: "Kurzuntersuchung",
      text: "Herz, Lunge, ein Blick auf die Nerven. Was du findest, kommt als Karte in die Mappe.",
      zeilen: ["Puls am Handgelenk langsam, regelmäßig.", "Herztöne regelmäßig, langsam, kein Geräusch.",
               "Lunge frei, keine Beinödeme.", "Schürfung linker Ellbogen, blauer Fleck linke Hüfte.",
               "Sprache klar, Gesicht symmetrisch, Arme und Beine seitengleich kräftig, kein Doppeltsehen, Finger-Nase sicher."],
      fertig: function () {
        P.vor(2);
        setze("untersucht");
        P.karte("unters");
        vd("struktur", "dagegen", "kein Geräusch, keine Beschwerden; Auskultation und eine Ableitung schließen bei 68 mit Bluthochdruck nichts aus, das Echo macht die Station");
        vd("tia", "unwahrscheinlich", "Bewusstsein weg, Ausfälle keine");
        if (dann) dann();
      }
    });
  }

  /* ---------------------------------------------------------------- Runden der Anamnese (§4.4, §5.3–5.5)
     Kern als Engpass, Rest auslassbar; „Das reicht mir" erscheint, sobald der Kern steht. Was fehlt, fragt Falk. */
  var FRAGEN = {
    1: [
      { id: "r1_1", text: "Haben Sie vorher etwas gespürt? Übel, heiß, Schwitzen?" },
      { id: "r1_2", text: "Waren Sie grad erst aufgestanden?" },
      { id: "r1_3", text: "Wie lange weg, und danach gleich klar?" },
      { id: "r1_4", text: "Woher ist die Schramme?" },
      { id: "r1_5", text: "Hat Ihre Tochter gesehen, ob Sie gezuckt haben?" }
    ],
    2: [
      { id: "r2_1", text: "Welche Tabletten nehmen Sie?" },
      { id: "r2_1a", text: "Haben Sie die heute schon genommen?", wenn: function () { return hat("r2_1"); } },
      { id: "r2_1b", text: "Ist in letzter Zeit etwas geändert worden?", wenn: function () { return hat("r2_1"); } },
      { id: "r2_2", text: "Haben Sie Zucker? Andere Krankheiten?" },
      { id: "r2_3", text: "Herzrasen, Stolpern, Druck in der Brust, Luftnot?" },
      { id: "r2_4", text: "Konnten Sie danach reden, sehen, die Arme heben?" },
      { id: "r2_5", text: "Alkohol? Schlaftabletten?" }
    ],
    3: [
      { id: "r3_1", text: "Ist in Ihrer Familie jemand jung und plötzlich gestorben?" },
      { id: "r3_2", text: "Ist das schon einmal passiert?" }
    ]
  };
  var FRAGE_TEXT = {};
  [1, 2, 3].forEach(function (n) { FRAGEN[n].forEach(function (q) { FRAGE_TEXT[q.id] = q; }); });
  var KERN = {
    1: function () { return hat("r1_1") && hat("r1_2"); },
    2: function () { return hat("r2_1") && hat("r2_1a"); },
    3: function () { return hat("r3_2"); }
  };
  var REICHT = { 1: "Das reicht mir fürs Erste.", 2: "Das reicht mir." };
  var RUNDE_ENDE = { 1: "r1_ende", 2: "r2_ende", 3: "r3_schluss" };
  var UNTERS_TEXT = "Darf ich Sie kurz anschauen? Herz, Lunge, Nerven.";

  function untersOpt(n) {
    return { text: UNTERS_TEXT, z: 0, zu: "u_0", tu: function () { X().uZurueck = n; } };
  }
  function menu(n) {
    return function () {
      if (X().rueckweg && X().rueckweg.art === "herrk") return rueckwegMenu();
      var liste = [];
      FRAGEN[n].forEach(function (q) {
        if (!hat(q.id) && (!q.wenn || q.wenn())) liste.push({ text: q.text, zu: q.id, tu: setzeFn(q.id) });
      });
      if (!liste.length) return [];
      if (!hat("untersucht") && (n > 1 || KERN[1]())) liste.push(untersOpt(n));
      if (REICHT[n] && KERN[n]()) {
        liste.push({ text: REICHT[n], z: 0, zu: RUNDE_ENDE[n],
                     warum: n === 1 ? "Was du nicht gefragt hast, fragt Falk. Oder die Tochter sagt es dir." : null });
      }
      return liste;
    };
  }
  function setzeFn(f) { return function () { setze(f); }; }

  /* Rückweg zum Patienten (Falk schickt, §6.2): nur die gefragten Fragen, dann zurück. */
  function rueckwegMenu() {
    var rw = X().rueckweg, liste = [];
    rw.fragen.forEach(function (id) {
      var q = FRAGE_TEXT[id];
      if (q && !hat(id) && (!q.wenn || q.wenn())) liste.push({ text: q.text, zu: id, tu: setzeFn(id) });
    });
    if (!liste.length) return [{ text: "Bin gleich zurück.", z: 0, zu: null, dann: zurueckMeldung }];
    return liste;
  }
  function rueckwegErfuellt(rw) {
    if (!rw) return true;
    if (rw.art === "wagen") return P.hatKarte("pq") && P.hatKarte("frequenz");
    if (rw.art === "tochter") return P.hatKarte("fremd");
    if (rw.luecke === "r3_2") return hat("zweites_ereignis");
    for (var i = 0; i < rw.fragen.length; i++) if (!hat(rw.fragen[i])) return false;
    return true;
  }
  function zurueckMeldung() {
    if (X().rueckweg && rueckwegErfuellt(X().rueckweg)) P.melde("Dr. Falk wartet am Tresen.");
  }

  /* ---------------------------------------------------------------- EKG, Streifen, Zirkel (§5.7, §5.9) */
  function ekgGeschrieben() {
    setze("ekg_geschrieben");
    P.melde("EKG geschrieben · " + P.zeitText());
    rhythmusFrage();
  }
  function rhythmusFrage() {
    P.frage({
      titel: "Der Streifen liegt vor dir",
      text: "Erst der Rhythmus. Was führt hier?",
      ekg: { mmProS: 25, von: 1.8, dauer: 7 },
      antworten: [
        { text: "Ersatzrhythmus aus dem AV-Knoten", warum: "Dann fehlte die P vor dem QRS, oder sie wäre in II negativ, im oder hinter dem QRS. Hier steht vor jedem QRS eine positive P. Langsam heißt nicht Ersatz." },
        { text: "Sinusrhythmus", richtig: true, warum: "Vor jedem QRS eine P-Welle, in II positiv, die Abstände gleich. Der Sinusknoten führt. Ob er langsam ist, sagt erst die Frequenz: der Zirkel." },
        { text: "Sinusrhythmus mit ausgefallenen Schlägen (AV-Block II°)", warum: "Dann gäbe es P-Wellen, auf die kein QRS folgt, eine Lücke. Hier folgt auf jede P ein QRS, und zwischen den Komplexen liegt keine zweite P. In zehn Sekunden fällt nichts aus." },
        { text: "Vorhofflimmern", warum: "Kein P, flimmernde Grundlinie, Abstände springen. Hier: P vor jedem QRS, Abstände gleich." }
      ],
      fertig: function () {
        P.vor(1);
        setze("rhythmus");
        P.karte("rhythmus");
        messWahl();
      }
    });
  }
  var MESSUNG = {
    rr: { toleranz: 25, mmProS: 25, von: 1.9, dauer: 7, karte: "frequenz", text: "Den RR-Abstand, die Frequenz",
          titel: "Wie langsam ist langsam?",
          auftrag: "Miss einen RR-Abstand. Aus ihm kommt die Frequenz: 60 000 geteilt durch den RR-Abstand in Millisekunden.",
          deutung: function (ms) {
            return T("60 000 : {ms} = {hf} pro Minute. Im Kurs heißt Sinusbradykardie unter 50 (so auch die Synkopen-Leitlinie); " +
                     "andere Quellen sagen 60, und der Datensatz nennt diese Kurve Sinusbradykardie. Wichtiger: unter Betablocker " +
                     "erwartbar, nicht verdächtig.", { ms: ms, hf: Math.round(60000 / ms) });
          } },
    pq: { toleranz: 20, mmProS: 50, von: 2.9, dauer: 2.6, karte: "pq", text: "Die PQ-Zeit, die Überleitung",
          titel: "Wie lange braucht der Impuls nach unten?",
          auftrag: "Miss die PQ-Zeit. Bei 50 mm/s ist ein kleines Kästchen 20 Millisekunden breit.",
          deutung: function (ms) {
            return ms > 200
              ? T("{ms} ms, über 200: AV-Block I°. Damit ist das EKG nicht normal. Mehr sagt es nicht: jeder Vorhofimpuls " +
                  "kommt an, keine Pause, kein ausgefallener Schlag in zehn Sekunden.", { ms: ms })
              : "Norm 120–200 ms, das liegt im Rahmen.";
          } },
    qrs: { toleranz: 20, mmProS: 50, von: 2.9, dauer: 2.6, karte: "qrs", text: "Die QRS-Breite, die Kammer",
           titel: "Wie breit ist die Kammer?",
           auftrag: "Miss die QRS-Breite. Bei 50 mm/s ist ein kleines Kästchen 20 Millisekunden breit.",
           deutung: function (ms) {
             return T("{ms} ms, schmal. Die Kammern laufen über das normale Leitungssystem; die Bremse sitzt oben, in der Überleitung.", { ms: ms });
           } }
  };
  function messWahl() {
    P.wahl({
      titel: "Was willst du messen?",
      text: "Der Streifen liegt auf dem Wagen. Nimm den Zirkel.",
      genug: "Genug gemessen",
      wahl: ["rr", "pq", "qrs"].map(function (was) {
        var m = MESSUNG[was];
        return { text: m.text, fertig: P.hatKarte(m.karte), tu: function () { messe(was); } };
      }),
      zu: streifenFertig
    });
  }
  function messe(was) {
    var m = MESSUNG[was];
    P.zirkel({
      was: was, toleranz: m.toleranz, mmProS: m.mmProS, von: m.von, dauer: m.dauer, titel: m.titel, auftrag: m.auftrag,
      deutung: m.deutung,
      zu: messWahl,
      fertig: function (erg) {
        var w = P.Z.werte;
        P.vor(2);
        if (was === "rr") {
          w.rr = erg.wahrheit; w.hf = Math.round(60000 / erg.wahrheit);
          P.karte("frequenz");
          vd("rhythmus", null, "{hf} unter Betablocker: erwartbar, nicht verdächtig");
        } else if (was === "pq") {
          w.pq = erg.wahrheit;
          P.karte("pq");
          vd("rhythmus", "dafuer", "EKG nicht normal: AV-Block I°, PQ {pq}; kein Beweis");
        } else {
          w.qrs = erg.wahrheit;
          P.karte("qrs");
          vd("rhythmus", null, "schmal: die Bremse sitzt oben");
        }
        if (!P.Z.falkDa && P.Z.zeit >= FALK) streifenFertig(true);   /* Falk kommt um 07:15 in jedem Fall */
        else messWahl();
      }
    });
  }
  function streifenFertig(still) {
    var rw = X().rueckweg;
    if (rw && rw.art === "wagen") { zurueckMeldung(); return; }
    if (hat("streifen_fertig")) return;
    setze("streifen_fertig");
    P.leben("ekg_aus");
    if (still) return;
    if (hat("anruf_spaeter") && !P.hatKarte("fremd")) zweiterAnruf();
    else takt5();
  }
  /* Takt 5 (Sequel): der Stand sagt in einem Satz, was ansteht, und bietet den Knopf zum Tresen. */
  function takt5() {
    if (hat("takt5")) return;
    setze("takt5");
    P.stand();
  }
  function zweiterAnruf() {
    X().anruf = "zweit";
    P.leben("handy"); P.handyLicht();
    P.dialog(B, "t_zweit");
  }
  function anrufFertig() {
    var art = X().anruf; X().anruf = null;
    if (art === "erst") ekgGeschrieben();
    else if (art === "zweit") takt5();
    else zurueckMeldung();
  }

  /* ---------------------------------------------------------------- Falk (§6) */
  function falkKommt() {
    P.Z.falkDa = true;
    P.zeitMin(FALK);
    P.dialog(B, "f0");
  }
  function falkJetzt() {
    if (!P.Z.falkDa) { P.zeitMin(FALK); falkKommt(); } else falkTresen();
  }
  function falkTresen() {
    if (!hat("ekg_geschrieben")) { P.melde("Dr. Falk liest am Tresen. Schreib das EKG."); return; }
    if (!hat("rhythmus")) { rhythmusFrage(); return; }
    if (!hat("isbar_start")) { P.dialog(B, "f2"); return; }
    var rw = X().rueckweg;
    if (rw) {
      if (!rueckwegErfuellt(rw)) { P.dialog(B, "rw_nochmal"); return; }
      X().rueckweg = null;
      if (X().zeile === "luecke") { P.dialog(B, luecke() ? "luecke" : "f_und_r"); return; }
      P.dialog(B, "f_und");
      return;
    }
    P.dialog(B, "f_und");
  }
  /* Was ausgelassen wurde, fragt Falk ab: eine Lücke je Durchgang, Rückweg zum Patienten (§6.2). */
  var LUECKEN = [
    { id: "r1_4", art: "herrk", fragen: ["r1_4"], satz: "Verletzt hat er sich? Wissen Sie nicht, dann fragen Sie ihn, drei Meter." },
    { id: "r3_2", art: "herrk", fragen: ["r3_2"], satz: "Schon einmal gehabt? Das fragt man als Erstes." },
    { id: "r2_2", art: "herrk", fragen: ["r2_2"], satz: "Zucker, andere Krankheiten? Fragen Sie." },
    { id: "r3_1", art: "herrk", fragen: ["r3_1"], satz: "Familie?" },
    { id: "fremd", art: "tochter", fragen: [], satz: "Wer hat ihn gefunden? Die Tochter, und die haben Sie nicht gefragt?" }
  ];
  function luecke() {
    for (var i = 0; i < LUECKEN.length; i++) {
      var l = LUECKEN[i];
      if (l.id === "fremd" ? !P.hatKarte("fremd") : (l.id === "r3_2" ? !hat("zweites_ereignis") : !hat(l.id))) return l;
    }
    return null;
  }
  function ueb() { var x = X(); if (!x.ueb) x.ueb = { b: [], r: [] }; return x.ueb; }

  /* Zeilen der Übergabe (§6.2) */
  function isMenu() {
    return [
      { text: "Herr Baum, 68. Zweimal weg ohne Vorwarnung, gestern und heute.", zitat: true, zu: "is_ok1",
        wenn: function () { return hat("zweites_ereignis"); },
        tu: function () { ueb().is = "Herr Baum, 68. Zweimal weg ohne Vorwarnung, gestern und heute."; },
        warum: "Wer, Alter, was, wie oft: das Entscheidende zuerst. Das zweite Ereignis gehört in den ersten Satz, weil die Notiz nur die halbe Geschichte kannte." },
      { text: "Herr Baum, 68. Heute früh weg, ohne Vorwarnung.", zitat: true, zu: "is_ok0",            /* NEU (ohne Wendung) */
        wenn: function () { return !hat("zweites_ereignis"); },
        tu: function () { ueb().is = "Herr Baum, 68. Heute früh weg, ohne Vorwarnung."; },
        warum: "Wer, Alter, was: das Entscheidende zuerst." },                                            /* NEU */
      { text: "Herr Baum, 68, Synkope, vermutlich vasovagal.", zitat: true, zu: "is_vage",
        wenn: function () { return !hat("is_vage"); }, tu: setzeFn("is_vage"),
        warum: "Du hast ihm seine eigene Notiz vorgelesen. Situation heißt: was passiert ist, nicht was jemand vermutet." },
      { text: "Ein älterer Herr, dem schwindlig geworden ist.", zitat: true, zu: "is_falsch",
        wenn: function () { return !hat("is_falsch"); }, tu: setzeFn("is_falsch"),
        warum: "Schwindel ist kein Bewusstseinsverlust. Vier Merkmale: kurz, umgesunken, keine Reaktion, Erinnerungslücke. Alle vier da." }
    ];
  }
  function aMenu() {
    var f = P.hatKarte("frequenz"), q = P.hatKarte("pq");
    return [
      { text: "Sinus, {hf}, PQ {pq}, QRS schmal. Nicht normal, kein Beweis.", zitat: true, zu: "a_ok",
        wenn: function () { return f && q; },
        tu: function () { ueb().a = T("Sinus, {hf}, PQ {pq}, QRS schmal. Nicht normal, kein Beweis.", P.vars()); },
        warum: "Rhythmus, Frequenz, Überleitung, Kammer, und was es bedeutet: nicht normal (PQ > 200), aber nichts, was eine arrhythmische Synkope beweist." },
      { text: "Bradykardie, {hf}. Das erklärt die Ohnmacht.", zitat: true, zu: "a_brady",
        wenn: function () { return f && !hat("a_brady"); },
        tu: function () { setze("a_brady"); setze("brady_argument"); },
        warum: "{hf} erklärt keine Ohnmacht und ist unter Betablocker erwartbar. Ein Warnzeichen wäre erst ein Puls dauerhaft unter 40 im Wachen, und die Leitlinie nimmt bremsende Medikamente ausdrücklich aus. Ob man {hf} Bradykardie nennt, hängt von der Quelle ab; die Folgerung ist falsch, nicht das Wort." },
      { text: "EKG unauffällig.", zitat: true, zu: "a_unauff",
        wenn: function () { return !hat("a_unauff"); }, tu: setzeFn("a_unauff"),
        warum: "PQ über 200 ms ist ein AV-Block I°. Ein EKG mit AV-Block I° ist nicht normal, auch wenn es niemanden umwirft." },
      { text: "PQ hab ich nicht gemessen.", zitat: true, zu: "a_rueck", wenn: function () { return !q; } },
      { text: "Die Frequenz hab ich nicht gemessen.", zitat: true, zu: "a_rueck", wenn: function () { return q && !f; } }  /* NEU */
    ];
  }
  var B_LANG = "Bluthochdruck seit zehn Jahren, Betablocker seit Jahren, heute nicht genommen, Stehversuch unauffällig.";
  function bMenu() {
    return [
      { text: "Betablocker seit Jahren, heute nicht. Schellong negativ.", zu: "b1",
        zitat: function () { return hat("r2_2") ? B_LANG : "Betablocker seit Jahren, heute nicht. Schellong negativ."; },
        wenn: function () { return P.hatKarte("medis") && hat("heute_nicht") && !hat("b1"); },
        tu: function () { setze("b1"); ueb().b.unshift(hat("r2_2") ? B_LANG : "Betablocker seit Jahren, heute nicht. Schellong negativ."); },
        warum: "Vorerkrankung, Medikation mit Änderung (keine) und Einnahme (heute nicht), Stehversuch: das, was die Einschätzung trägt." },
      { text: "Die Tochter hat's gesehen: kein Zucken, Augen offen, sofort da.", zitat: true, zu: "b2",
        wenn: function () { return P.hatKarte("fremd") && !hat("b2"); },
        tu: function () { setze("b2"); ueb().b.push("Die Tochter hat's gesehen: kein Zucken, Augen offen, sofort da."); },
        warum: "Die Zeugin trennt Synkope von Anfall: keine Zuckungen, sofort klar." },
      { text: "Er geht täglich mit dem Hund, ist fit für sein Alter.", zitat: true, zu: "b_vage",
        wenn: function () { return !hat("b_vage") && !hat("b1"); }, tu: setzeFn("b_vage"),
        warum: "Belastbarkeit ist ein Befund gegen die strukturelle Herzkrankheit, aber Hintergrund heißt zuerst: Vorerkrankungen, Medikamente." },
      { text: "Drei Tabletten, welche weiß ich nicht.", zitat: true, zu: "b_rueck",
        wenn: function () { return !P.hatKarte("medis"); } }
    ];
  }
  /* Nach der ersten richtigen B-Zeile: die zweite freiwillig, dann die Lücken, dann R. */
  function nachBMenu() {
    if (!hat("b1")) return bMenu();
    var l = [];
    if (P.hatKarte("fremd") && !hat("b2")) l.push(bMenu()[1]);
    if (l.length) { l.push({ text: "Weiter", z: 0, zu: nachB }); return l; }
    X().zeile = "luecke";
    return luecke() ? [] : rMenu();
  }
  function nachB() { X().zeile = "luecke"; return luecke() ? "luecke" : "f_und_r"; }
  function rMenu() {
    X().zeile = "r";
    return [
      { text: "Er bleibt. Monitor.", zitat: true, zu: "r_ok",
        tu: function () { ueb().r.push("Er bleibt. Monitor."); P.karte("uebergabe"); },
        warum: "Die Empfehlung in einem Satz. Jetzt muss sie begründet werden; die Tabletten kommen danach." },
      { text: "Er kann heim, Kontrolle beim Hausarzt.", zitat: true, zu: "r_heim",
        wenn: function () { return !hat("heim_empfohlen"); },
        tu: function () { setze("heim_empfohlen"); ueb().r.push("Er kann heim, Kontrolle beim Hausarzt."); P.karte("uebergabe"); },
        warum: "Vertretbar wäre das nur bei niedrigem Risiko: Vorwarnung, normales EKG, keine Herzkrankheit. Prüf, ob du das hast." },
      { text: "Noch einen Stehversuch, dann sehen wir weiter.", zitat: true, zu: "r_steh",
        wenn: function () { return !hat("r_steh"); }, tu: setzeFn("r_steh"),
        warum: "Der Stehversuch ist gemacht und negativ; er prüft die Orthostase, nicht das Risiko. Wiederholen beantwortet die Frage nicht." }
    ];
  }

  /* Gegenrede (§6.3): Nachgeben nur mit beiden tragenden Argumenten (keine Vorwarnung UND EKG nicht normal). */
  var ARGS = [
    { id: "zweimal", text: "Zweimal in zwei Tagen. Das erste Mal mit 68.",
      wenn: function () { return hat("zweites_ereignis"); },
      falk: "Mit achtundsechzig fängt man nicht mit Kreislaufgeschichten an, geb ich Ihnen. {fehlt}",
      warum: "Die Reflexsynkope hat meist eine lange Vorgeschichte, oft seit der Jugend. Ein erstes Mal mit 68, und gleich zweimal, ist das Gegenteil davon; ein Risikomerkmal der Tabelle ist es nicht." },
    { id: "stehen", text: "Stehversuch negativ, beim Kocher eine Minute gestanden.",
      falk: "Gut, dann ist es nicht der Kreislauf. Und was ist es dann?",
      warum: "Kein Abfall ≥ 20/10 mmHg nach drei Minuten, kein Sturz beim Aufstehen, nur eine Minute gestanden: Orthostase unwahrscheinlich. Das schließt aus, es beweist nichts." },
    { id: "vorwarnung", text: "Keine Vorwarnung. Beide Male.", tragend: true,
      wenn: function () { return hat("zweites_ereignis"); },
      falk: function () {
        return benutzt("pq") ? "Zählt. Mit dem EKG zusammen ist er nicht mehr niedrig."
          : "Zählt, mit dem EKG zusammen, das Sie mir vorhin gesagt haben. Sagen Sie's als Argument.";
      },
      warum: "Fehlende Vorwarnung ist ein Minor-Merkmal: Es zählt nur zusammen mit einer Herzkrankheit oder einem nicht normalen EKG." },
    { id: "verletzt", text: "Er hat sich verletzt. Ellbogen, Hüfte.",
      falk: "Die Schramme allein ist mir egal, die Schramme bei dem Rest nicht. {fehlt}",
      warum: "Verletzung durch die Synkope spricht für Aufnahme, wenn Risikomerkmale da sind; allein trägt sie nichts." },
    { id: "brady", text: "Puls {hf}, das ist eine Bradykardie.",
      tu: function () { setze("brady_argument"); },
      falk: "Unter Betablocker ist {hf} erwartbar. Was noch?",
      warum: "{hf} erklärt keine Ohnmacht und ist unter Betablocker erwartbar; Warnzeichen erst dauerhaft unter 40 im Wachen, und die Leitlinie nimmt bremsende Medikamente aus. Das Wort hängt von der Quelle ab, die Folgerung ist falsch." },
    { id: "pq", text: "PQ {pq}. Das EKG ist nicht normal.", tragend: true,
      falk: function () {
        return benutzt("vorwarnung") ? "Nicht normal, nicht gefährlich. Mit der fehlenden Vorwarnung zusammen aber nicht mehr niedrig."
          : "Nicht normal, nicht gefährlich, allein ist das nichts. Was macht es zu etwas?";
      },
      warum: "Niedriges Risiko verlangt ein normales EKG. AV-Block I° ist nicht normal. Allein ist er kein Risikomerkmal; mit „keine Vorwarnung“ zusammen ist der Patient nicht mehr niedrig." },
    { id: "tochter", text: "Die Tochter hat kein Zucken gesehen.",
      wenn: function () { return P.hatKarte("fremd"); },
      falk: "Kein Anfall, gut. Und warum bleibt er?",
      warum: "Zeugenbericht trennt Anfall und Synkope. Für die Risikofrage ist das kein Argument." },
    { id: "vater", text: "Der Vater hatte einen Schlaganfall.",
      falk: "Mit achtzig. Wer ist bei Ihnen jung und plötzlich gestorben?", spielerin: "Niemand.", falk2: "Dann weiter.",
      warum: "Das Familien-Merkmal heißt: plötzlicher Herztod in jungen Jahren. Ein Schlaganfall mit 80 ist keines." },
    { id: "tia", text: "Könnte es eine TIA gewesen sein?",
      falk: "Eine TIA nimmt etwas weg, Sprache, Kraft, ein Gesichtsfeld, das Bewusstsein lässt sie in Ruhe. Haben Sie ihn reden und gehen lassen?",
      spielerin: "Ja. Alles seitengleich.", falk2: "Dann war's keine.",
      warum: "TIA = fokaler Ausfall ohne Bewusstseinsverlust; vertebrobasilär nie ohne Hirnstammzeichen. Hier: Bewusstsein weg, Ausfälle keine." }
  ];
  function benutzt(id) { return (X().args || []).indexOf(id) >= 0; }
  function beide() { return benutzt("vorwarnung") && benutzt("pq"); }
  function hinweisFaellig() { return (X().args || []).length >= 4 && !beide() && !X().hinweis; }
  /* {fehlt}: was Falk nach einem Stützargument noch fehlt (§6.3). */
  function fehlt() {
    var v = benutzt("vorwarnung"), e = benutzt("pq");
    if (!v && !e) return "Fehlt mir trotzdem der Grund, warum er nicht niedrig ist.";
    if (v && !e) return "Fehlt mir, was das EKG dazu sagt.";
    if (!v && e) return "Fehlt mir trotzdem der Grund, warum die Vorwarnung zählt.";
    return "";
  }
  function argMenu() {
    var x = X();
    if (!x.args) x.args = [];
    return ARGS.filter(function (a) { return !benutzt(a.id) && (!a.wenn || a.wenn()); }).map(function (a) {
      return { text: a.text, zitat: true, zu: "arg_" + a.id, warum: a.warum,
               tu: function () { x.args.push(a.id); if (a.tu) a.tu(); } };
    });
  }
  function nachArg() { return (beide() || hinweisFaellig()) ? [] : argMenu(); }
  function nachArgWeiter() { return beide() ? "nachgeben" : "hinweis"; }

  function tabMenu() {
    return [
      { text: "Alle drei, wie immer.", zitat: true, zu: "tab1", wenn: function () { return !hat("tab1"); }, tu: setzeFn("tab1"),
        warum: "Das Bisoprolol ist das einzige Mittel auf dem Plan, das Frequenz und Überleitung bremst; es jetzt zu geben, bevor der Monitor gezeigt hat, was die Leitung ohne Bremse macht, verwischt die Frage, die ihr gerade gestellt habt." },
      { text: "Ramipril und ASS. Bisoprolol erst nach dem Monitor.", zitat: true, zu: "tab2",
        tu: function () { setze("tabletten"); P.karte("entscheidung"); },
        warum: "Betablocker bremsen Sinusknoten und AV-Überleitung; bei einer Bradyarrhythmie unter einem solchen Medikament ist Dosisreduktion oder Absetzen der erste Schritt, bevor man an mehr denkt. ACE-Hemmer und ASS bremsen keinen Knoten; der Blutdruck ist {rr_l_sys}/{rr_l_dia}, der Stehversuch unauffällig: kein Grund, sie wegzulassen." },
      { text: "Nichts, bis alles geklärt ist.", zitat: true, zu: "tab3", wenn: function () { return !hat("tab3"); }, tu: setzeFn("tab3"),
        warum: "Nicht gefährlich, aber ohne Grund: Ramipril und ASS haben mit der Ohnmacht nichts zu tun; wer ohne Grund absetzt, schafft ein neues Problem." }
    ];
  }

  /* Schlussgespräch (§7.1) */
  function sMenu() {
    return [
      { text: "Das ist jetzt nicht wichtig. Sie bleiben.", zu: "s1", wenn: function () { return !hat("s1"); }, tu: setzeFn("s1"),
        warum: "„Nicht wichtig“ ist für ihn das Wichtigste. Wer die Sorge wegwischt, verliert den Patienten, nicht das Argument." },
      { text: "Dann unterschreiben Sie einen Revers.", zu: "s2", wenn: function () { return !hat("revers"); }, tu: setzeFn("revers"),
        warum: "Den Revers nimmt der Arzt, nach Aufklärung. Du hast weder das eine noch das andere getan." },
      { text: "Gestern und heute waren Sie weg, ohne es zu merken.", zu: "s3",
        warum: "Richtig: seine Worte („weg“), nicht deine (Synkope, Risiko). Dann der Grund in einem Bild (Aussetzer) und was der Schirm kann." },
      { text: "Wegen der Senta: Die Frau Kainz hat den Schlüssel.", zu: "s4",
        wenn: function () { return hat("kainz_bekannt") && !hat("s4"); }, tu: setzeFn("s4"),
        warum: "Die Senta zuerst löst das Hindernis, aber nicht die Frage; er fragt zu Recht „wieso überhaupt“." }
    ];
  }
  function s3Menu() {
    return [
      { text: "Das kann vom Herzen kommen. Ein Aussetzer.", zu: "s5" },
      { text: "Ihr Herz schlägt langsam, die Überleitung auch.", zu: "s6", wenn: function () { return !hat("s6"); }, tu: setzeFn("s6"),
        warum: "Das ist dein Befund, nicht sein Problem; er hört „Alter“ und hat recht." }
    ];
  }

  /* ================================================================ Dialogknoten */
  var B = {
    /* ---------- §5.1 Auftakt */
    a1: { wer: "erzaehler", text: "06:40. Dein erster Tag der Rotation auf der Notaufnahme, zwanzig Minuten zu früh, weil du den Weg nicht kanntest.", weiter: "a2" },
    a2: { wer: "erzaehler", text: "Die Nachtschicht räumt auf, Marlene telefoniert hinter dem Tresen. In der Koje rechts ein Mann mit Schiebermütze, der die Jacke schon anhat und ein Sackerl in der Hand hält.",
          antworten: [{ text: "Zum Tresen.", z: 2, zu: null, dann: function () { marleneTresen(); } }] },

    /* ---------- §5.2 Marlene am Tresen */
    m0: { wer: "marlene", text: "Du bist die KPJ-lerin? Marlene, seit gestern sieben Uhr da, also red langsam mit mir.",
          tu: function () { setze("marlene_tresen"); }, antworten: function () { return marleneMenu(); }, weiter: "m_ende1" },
    m1a: { wer: "marlene", text: "Herr Baum, achtundsechzig, heut in der Früh in der Küche umgefallen, die Tochter hat ihn gebracht. Ihm fehlt nix, sagt er, und der Hund muss raus.", weiter: "m1b" },
    m1b: { wer: "marlene", text: "Die Monitorkojen sind voll, drum ist er in der Drei.", antworten: function () { return marleneMenu(); }, weiter: "m_ende1" },
    m2: { wer: "marlene", regie: "reicht den Bogen", text: "Die Steiner hat Journal, die ist seit halb sieben im Schockraum, die Rettung hat eine Reanimation gebracht. Vorher hat sie ihn kurz gesehen und das da hingeschrieben.",
          tu: bogenGelesen, antworten: function () { return marleneMenu(); }, weiter: "m_ende1" },
    m3: { wer: "marlene", text: "Red mit ihm und schau ihn an. Das EKG schreibst du, ich komm nicht dazu, um sieben geb ich der Andrea acht Leute über.",
          antworten: function () { return marleneMenu(); }, weiter: "m_ende1" },
    m_ende1: { wer: "marlene", text: "Und der Falk kommt um viertel nach sieben runter und fragt dich, ob der Mann heimdarf. Nicht mich.", weiter: "m_ende2" },
    /* Ohne Frage 2 reicht sie den Bogen hier (sonst fehlte ihn die Spielerin für den Stehversuch). */
    m_ende2: { wer: "marlene", text: "Stehversuch und Zucker hab ich gemacht, Blut ist weg, Labor kommt um acht. So.",
               regie: function () { return P.hatKarte("bogen") ? "" : "reicht den Bogen"; }, tu: bogenGelesen,
               antworten: [{ text: "Danke. Ich geh zu ihm.", z: 0, zu: null }] },
    m_idle: { wer: "marlene", text: "Und der Falk kommt um viertel nach sieben runter und fragt dich, ob der Mann heimdarf. Nicht mich.", endeText: "Danke." },

    /* ---------- §5.3 Runde 1 */
    b0: { wer: "herrk", text: "Ah, Frau Doktor. Entschuldigen S', die Schwester hat gesagt, ich soll warten, aber die Senta muss um acht raus, und mir fehlt nix.",
          tu: function () { setze("r1_start"); }, antworten: function () { return b0Menu(); } },
    b_senta: { wer: "herrk", text: "Die Senta, unser Hund, also der von der Sabine, aber ausführen tu ich. Neun Jahre, Dackel mit was drin, die wartet jetzt an der Tür.",
               antworten: function () { return b0Menu(); } },
    b_bogen: { wer: "herrk", text: "Bitte, bitte, ich hab Zeit. Also keine, aber bitte.", tu: bogenGelesen, antworten: function () { return b0Menu(); } },
    b_erz: { wer: "herrk", regie: "setzt sich auf die Liegenkante, Jacke bleibt an",
             text: "In der Küche, ich hab den Wasserkocher angestellt wie immer. Und dann lieg ich am Boden, und die Sabine schreit, dazwischen nix, wie wenn einer das Licht ausdreht.",
             tu: function () { setze("r1_erz"); anamnese(); vd("sturz", "unwahrscheinlich", "weg, umgesunken, keine Erinnerung"); },
             antworten: menu(1), weiter: "r1_ende" },
    r1_1: { wer: "herrk", text: "Nix, gar nix. Ich hab grad an die Senta gedacht, und dann war der Boden da.",
            tu: function () { vd("reflex", "dagegen", "keine Vorwarnung"); vd("rhythmus", "dafuer", "ohne Vorwarnung"); },
            antworten: menu(1), weiter: "r1_ende" },
    r1_2: { wer: "herrk", text: "Nein, seit sechs auf, die Senta gefüttert, dann der Kocher. Eine Minute hab ich dort gestanden, höchstens.",
            tu: function () { vd("kreislauf", "dagegen", "nicht beim Aufstehen, kurz gestanden"); }, antworten: menu(1), weiter: "r1_ende" },
    r1_3: { wer: "herrk", text: "Eine halbe Minute, sagt die Sabine, sie hat den Krach gehört und ist gleich gekommen. Dann hab ich gesagt, Sabine, mach keinen Zirkus, und sie hat trotzdem einen gemacht.",
            tu: function () { vd("krampf", "dagegen", "sofort klar, keine Verwirrtheit"); }, antworten: menu(1), weiter: "r1_ende" },
    r1_4: { wer: "herrk", text: "Vom Tisch, glaub ich, oder vom Sessel. Die Sabine weiß es, ich nicht.", antworten: menu(1), weiter: "r1_ende" },
    r1_5: { wer: "herrk", text: "Das fragen S' sie selber, sie ruft eh an. Gezuckt hab ich im Leben noch nie.", antworten: menu(1), weiter: "r1_ende" },
    r1_ende: { wer: "herrk", text: "Mehr weiß ich nicht, ich war halt weg. Fragen S' die Sabine, die hat alles gesehen.",
               tu: function () { setze("r1_fertig"); }, endeText: "Weiter", dann: function () { P.melde("Der EKG-Wagen ist frei. Herrn Baum kannst du weiter fragen."); } },

    /* ---------- §5.4 Runde 2 */
    r2_0: { wer: "herrk", text: "Fragen S' nur. Die Sabine hat auch schon alles gefragt.", antworten: menu(2), weiter: "r2_ende" },
    r2_1: { wer: "herrk", regie: "reicht den Plan", text: "Drei in der Früh, die Sabine hat den Zettel vom Hausarzt eingepackt, da im Sackerl. Die Farben kenn ich, die Namen nicht.",
            tu: function () { P.karte("medis"); }, antworten: menu(2), weiter: "r2_ende" },
    r2_1a: { wer: "herrk", text: "Heut nein, heut war ja die Küche zuerst. Die liegen noch am Tisch, neben dem Kaffee.",
             tu: function () { setze("heute_nicht"); }, antworten: menu(2), weiter: "r2_ende" },
    r2_1b: { wer: "herrk", text: "Nein, seit Jahren das Gleiche. Der Doktor Reiter sagt, so lang's passt, bleibt's.",
             tu: function () { vd("kreislauf", "dagegen", "keine neue oder geänderte Tablette"); }, antworten: menu(2), weiter: "r2_ende" },
    r2_2: { wer: "herrk", text: "Zucker nein. Den Blutdruck, seit zehn Jahren, das Knie, und das Hörgerät.",
            tu: function () { anamnese(); vd("zucker", "unwahrscheinlich", "kein Diabetes, Stix {zucker}"); }, antworten: menu(2), weiter: "r2_ende" },
    r2_3: { wer: "herrk", text: "Nie, mein Herz hab ich noch nie gespürt. Bergauf mit der Senta werd ich langsamer, aber ich komm rauf.",
            tu: function () { vd("struktur", "dagegen", "nicht unter Belastung, keine Beschwerden"); }, antworten: menu(2), weiter: "r2_ende" },
    r2_4: { wer: "herrk", text: "Alles. Ich hab der Sabine gesagt, sie soll den Wasserkocher abdrehen, der pfeift, also gehört und gesehen hab ich.",
            tu: function () { vd("tia", "dagegen", "reden, sehen, bewegen sofort wie immer"); }, antworten: menu(2), weiter: "r2_ende" },
    r2_5: { wer: "herrk", text: "Ein Bier am Sonntag, nach dem Friedhof. Schlafen tu ich wie ein Stein, ohne was.",
            warum: "Alkohol und Schlafmittel gehören zu den Nicht-Synkopen, die man abfragt; hier beides nein.",
            antworten: menu(2), weiter: "r2_ende" },
    r2_ende: { wer: "herrk", text: "Sonst bin ich gesund. Sagt der Reiter.", tu: function () { setze("r2_fertig"); }, endeText: "Weiter" },

    /* ---------- §5.5 Runde 3, die Wendung */
    r3_0: { wer: "herrk", text: "Noch was, Frau Doktor? Die Senta wartet.", antworten: menu(3) },          /* NEU: Einstieg der Runde */
    r3_1: { wer: "herrk", text: "Der Vater mit achtzig, Schlaganfall, die Mutter einundneunzig. Jung ist bei uns keiner gestorben.",
            tu: function () { anamnese(); vd("rhythmus", null, "niemand jung und plötzlich"); }, antworten: menu(3), weiter: "r3_schluss" },
    r3_2: { wer: "herrk", regie: "schaut auf das Sackerl", text: "Frau Doktor. Sagen S' es der Sabine nicht.",
            tu: function () { P.leben("uhr_blick"); },
            antworten: function () { return versprechenMenu(); } },
    r3_rev1: { wer: "herrk", text: "Gestern, an der Haltestelle beim Friedhof. Der Bus ist nicht gekommen, und auf einmal lieg ich am Boden, und eine Frau redet auf mich ein.",
               tu: function () {
                 setze("zweites_ereignis"); anamnese();
                 vd("rhythmus", "dafuer", "zweimal in zwei Tagen, beide Male ohne Vorwarnung, das erste Mal mit 68");
               }, weiter: "r3_rev2" },
    r3_rev2: { wer: "herrk", text: "Ich hab gesagt, der Kreislauf, und bin heimgefahren wie nix. Die Sabine hat genug mit der Lena und dem Kindergarten, bitte.",
               antworten: function () { return X().versprechen === "frage" ? versprechenMenu() : []; },
               weiter: function () { return X().versprechen === "unter_uns" ? "r3_danke" : "r3_arzt"; } },
    r3_danke: { wer: "herrk", text: "Danke. Sie sind eine Gute.", antworten: function () { return nachMenu(); }, weiter: "r3_schluss" },
    r3_arzt: { wer: "herrk", text: "Der Arzt ist der Arzt. Aber die Sabine macht sonst noch mehr Zirkus, und die Lena kriegt's mit.",
               antworten: function () { return nachMenu(); }, weiter: "r3_schluss" },
    r3_n1: { wer: "herrk", text: "Auch nix, gestanden und auf den Bus geschaut. Und dann die Frau mit dem Zuckerl, vor der Kirche, alle haben geschaut.",
             antworten: function () { return nachMenu(); }, weiter: "r3_schluss" },
    r3_n2: { wer: "herrk", text: "Eine Viertelstunde sicher. Sonntag fährt er nur alle halbe Stunde, und ich war zu früh, wie immer.",
             tu: function () { anamnese(); vd("reflex", null, "eine Viertelstunde Stehen spräche dafür, die fehlende Vorwarnung dagegen"); },
             antworten: function () { return nachMenu(); }, weiter: "r3_schluss" },
    r3_n3: { wer: "herrk", text: "Nein, die Frau hat gesagt, ich bin umgesunken wie ein nasser Sack, langsam. Der Ellbogen, das ist von heut.",
             tu: anamnese, antworten: function () { return nachMenu(); }, weiter: "r3_schluss" },
    r3_schluss: { wer: "herrk", text: "So, jetzt wissen Sie's. Und ich darf trotzdem heim, gell?",
                  tu: function () { setze("r3_fertig"); P.leben("uhr_blick"); },
                  antworten: [{ text: "Das entscheidet der Oberarzt. Vorher schau ich Sie an.", z: 0, zu: null,
                                dann: function () {
                                  if (hat("wagen_da") && !hat("marlene_weiss")) {
                                    setze("marlene_weiss");
                                    P.melde("Marlene, vom Tresen: „Das hat er mir nicht gesagt. Schreib's auf den Bogen, mit Uhrzeit.“");
                                  }
                                  zurueckMeldung();
                                } }] },

    /* ---------- §5.6 Untersuchung (freiwillig) */
    u_0: { wer: "herrk", text: "Bitte, die Jacke lass ich an, oder? Es zieht da herinnen.", endeText: "Untersuchen",
           dann: function () { untersuchung(function () { P.dialog(B, "u_1"); }); } },
    u_1: { wer: "herrk", text: "Sehen S', mir fehlt nix.",                                                    /* NEU: nach der Untersuchung */
           antworten: function () { var n = X().uZurueck; return n ? menu(n)() : []; },
           weiter: function () { var n = X().uZurueck; return n && n < 3 ? RUNDE_ENDE[n] : null; }, endeText: "Weiter" },
    b_idle: { wer: "herrk", text: "Ich wart ja eh, Frau Doktor. Die Senta auch.",                          /* NEU: nichts mehr offen */
              antworten: function () {
                return hat("untersucht") ? [] : [{ text: UNTERS_TEXT, z: 0, zu: "u_0", tu: function () { X().uZurueck = null; } },
                                                 { text: "Bin gleich zurück.", z: 0, zu: null }];
              }, endeText: "Bin gleich zurück." },
    rw_start: { wer: "herrk", text: "Ja, Frau Doktor?", antworten: rueckwegMenu },                         /* NEU: Rückweg von Falk */

    /* ---------- Marlene mit dem Wagen (fester Engpass, §5.6) */
    w1: { wer: "marlene", text: "Da, ich übergeb.", tu: function () { setze("wagen_da"); }, weiter: "w2" },
    w2: { wer: "marlene", text: "Und? Darf er?", antworten: [
      { text: "Es war gestern schon einmal. Er hat's niemandem gesagt.", z: 0, zu: "w3a",
        wenn: function () { return hat("zweites_ereignis"); }, tu: function () { setze("marlene_weiss"); } },
      { text: "Noch nicht. Erst das EKG.", z: 0, zu: "w3b" }] },
    w3a: { wer: "marlene", text: "Was, dem hab ich den ganzen Morgen Zuckerl angeboten, und er sagt mir nix? Schreib's auf den Bogen, mit Uhrzeit, und sag's dem Falk als Erstes.", weiter: "e1" },
    w3b: { wer: "marlene", text: "Dann mach. Papier ist drin.", weiter: "e1" },

    /* ---------- §5.7 Das EKG */
    e1: { wer: "herrk", regie: "Der Wagen steht an der Koje. Herr Baum legt sich hin, die Mütze bleibt auf.",
          text: "Muss ich das Hemd aufmachen? Kalt ist das Zeug.", antworten: function () { return eMenu(); } },
    e2: { wer: "herrk", text: "Beim Reiter, vor Jahren, da war's in Ordnung. Damals hab ich auch noch die Elfriede gehabt.", antworten: function () { return eMenu(); } },
    e_ruhig: { wer: "herrk", text: "Nicht reden kann ich nicht, fragen S' die Sabine.", weiter: "e_handy" },
    e_handy: { wer: "herrk", regie: "Das Handy im Sackerl leuchtet und vibriert. Herr Baum hebt den Kopf, legt ihn wieder hin.",
               text: "Das ist die Sabine. Gehen S' ran, bitte, ich darf mich ja nicht rühren, und ich hör eh nix mit dem Ding, wenn ich lieg.",
               tu: function () { P.leben("handy"); P.handyLicht(); },
               antworten: [
                 { text: "Ich geh ran.", zu: "t0", tu: function () { X().anruf = "erst"; } },
                 { text: "Das kann warten, erst das EKG.", zu: "e_spaeter", tu: function () { setze("anruf_spaeter"); },
                   warum: "Ein Angehöriger, der dabei war, ist die beste Zeugin, die du kriegst; am Telefon ist sie jetzt. Beides ist vertretbar." }] },
    e_spaeter: { wer: "herrk", text: "Dann ruft sie dreimal. Sie kennen sie nicht.", dann: ekgGeschrieben },

    /* ---------- §5.8 Das Telefon */
    t_zweit: { wer: "herrk", regie: "Das Handy im Sackerl leuchtet und vibriert.", text: "Das ist wieder die Sabine. Gehen S' ran, bitte.", weiter: "t0" },   /* NEU */
    t0: { wer: "tochter", text: "Papa, wer ist da? Ah, Entschuldigung, ich hab nur fünf Minuten, bevor meine Gruppe kommt.", weiter: "t0b" },
    t0b: { wer: "tochter", text: function () { return hat("anruf_spaeter") ? "Ich hab dreimal angerufen. Wie geht's ihm?" : "Wie geht's ihm?"; },
           antworten: function () { return tMenu(); }, weiter: "t_ende1" },
    t1a: { wer: "tochter", text: "Einen Krach, wie wenn der Tisch umfällt, und dann ist er am Boden gelegen, grau im Gesicht, die Augen offen. Ich hab Papa gesagt, und er hat gleich geschaut.", weiter: "t1b" },
    t1b: { wer: "tochter", text: "Zwanzig Sekunden vielleicht, dreißig. Mir ist es wie eine Stunde vorgekommen.", antworten: function () { return tMenu(); }, weiter: "t_ende1" },
    t2: { wer: "tochter", text: "Gezuckt hat er nicht, er ist dagelegen wie ein Sack, das war das Schlimme. Gebissen hat er sich auch nicht, ich hab geschaut.",
          tu: function () { vd("krampf", "unwahrscheinlich", "keine Zuckungen, sofort klar, keine Zunge"); }, antworten: function () { return tMenu(); }, weiter: "t_ende1" },
    t3: { wer: "tochter", text: "Nein, die liegen noch am Tisch, ich hab's gesehen, wie wir gegangen sind. Sonst nimmt er die um sieben mit dem Kaffee, soll ich sie bringen, ich kann erst um zwölf?",
          tu: function () { setze("heute_nicht"); }, antworten: function () { return tMenu(); }, weiter: "t_ende1" },
    t_ende1: { wer: "tochter", text: "Ist das was Schlimmes, darf er heim? Ich kann ihn erst um halb eins holen.", weiter: "t_ende2" },
    t_ende2: { wer: "tochter", text: "Und wegen dem Hund: Die Frau Kainz nebenan hat einen Schlüssel, ich ruf sie an, wenn er bleibt. Sagen S' ihm das, von mir glaubt er's nicht.",
               tu: function () { setze("kainz_bekannt"); P.karte("fremd"); },
               antworten: [
                 { text: "Das entscheidet der Oberarzt gleich. Ich ruf Sie an.", z: 0, zu: "t_a1" },
                 { text: "Wahrscheinlich nur der Kreislauf. Keine Sorge.", z: 0, zu: "t_a2", tu: function () { setze("tochter_beruhigt"); },
                   warum: "Zu früh. Du weißt es noch nicht, und die Tochter wird jedem erzählen, was du gesagt hast; „der Oberarzt entscheidet gleich“ ist keine Ausrede, es ist der Stand." },
                 { text: "Er hat uns gesagt, dass es gestern schon einmal war.", z: 0, zu: "t_a3", wenn: function () { return hat("zweites_ereignis"); },
                   tu: function () { setze("tochter_verraten"); },
                   warum: "Er hat dich gebeten, es ihr nicht zu sagen, und er ist bei klarem Verstand. Was die Tochter erfährt, entscheidet er." }] },
    t_a1: { wer: "tochter", text: "Gut, bitte. Die Lena fragt schon.", weiter: "t_tschuess" },
    t_a2: { wer: "tochter", text: "Gott sei Dank, das hab ich mir gedacht, der Kreislauf halt. Dann bis zwölf.", weiter: "t_tschuess" },
    t_a3: { wer: "tochter", text: "Gestern, was gestern? Der sagt mir nichts, nie, und zum Friedhof will er allein, mit dem Bus, damit ich meine Ruhe hab.", weiter: "t_tschuess" },
    t_tschuess: { wer: "tochter", text: "Ich muss, die Gruppe kommt. Danke, Frau, ich weiß gar nicht, wie Sie heißen.", endeText: "Auflegen", dann: anrufFertig },

    /* ---------- §6.1 Falk kommt */
    f0: { wer: "erzaehler", text: "{zeit}. Die Tür, Dr. Falk, Kaffee in der einen Hand, die Übergabeliste in der anderen; er liest, bevor er grüßt.", weiter: "f1" },
    f1: { wer: "falk", text: "Sie sind neu, Falk. Koje drei, Herr Baum, vasovagal, steht da.", weiter: "f2" },
    f2: { wer: "falk", text: "Ich brauch die Koje um halb acht, die Rettung hat zwei angemeldet. Kann er heim?",
          tu: function () { if (hat("ekg_geschrieben")) setze("isbar_start"); },
          antworten: function () {
            if (!hat("ekg_geschrieben")) return [];
            return [
              { text: "Darf ich kurz übergeben?", zu: "f_kurz" },
              { text: "Nein.", zu: "f_antw", warum: "Ein Oberarzt mit zwölf Minuten will zuerst den Patienten, nicht dein Urteil. ISBAR: Identifikation, Situation, Hintergrund, Einschätzung, Empfehlung." },
              { text: "Ja, wahrscheinlich.", zu: "f_antw", warum: "Ein Oberarzt mit zwölf Minuten will zuerst den Patienten, nicht dein Urteil. ISBAR: Identifikation, Situation, Hintergrund, Einschätzung, Empfehlung." }];
          },
          weiter: function () { return hat("ekg_geschrieben") ? null : "f_warten"; } },
    f_warten: { wer: "falk", text: "Kein EKG? Schreiben Sie, ich les solang.", tu: function () { setze("falk_gewartet"); }, endeText: "Bin gleich zurück." },
    f_kurz: { wer: "falk", text: "Kurz. Wer, was, was Sie denken, was Sie wollen, in der Reihenfolge, wenn's geht.", antworten: isMenu },
    f_antw: { wer: "falk", text: "Das ist eine Antwort, keine Übergabe. Wer, was, was Sie denken, was Sie wollen, dann reden wir über ja oder nein.", antworten: isMenu },

    /* ---------- §6.2 I/S */
    is_ok1: { wer: "falk", text: "Zweimal? Da steht einmal, Küche.", weiter: "is_ok1b" },
    is_ok1b: { wer: "spielerin", text: "Gestern an der Haltestelle. Er hat's niemandem gesagt.", weiter: "is_ok1c" },
    is_ok1c: { wer: "falk", text: "Hm.", weiter: function () { return hat("versprochen") ? "v1" : "unterbrechung"; } },
    is_ok0: { wer: "falk", text: "Ohne Vorwarnung, steht nicht da. Gut.", weiter: "unterbrechung" },          /* NEU */
    is_vage: { wer: "falk", text: "Vermutlich steht schon da. Was ist passiert?", antworten: isMenu },
    is_falsch: { wer: "falk", text: "Schwindlig? Er lag am Boden und weiß nichts davon, das ist nicht schwindlig, noch einmal.", antworten: isMenu },
    v1: { wer: "falk", text: "Und Ihnen hat er's gesagt, weil?", weiter: "v2" },
    v2: { wer: "spielerin", text: "Weil ich gefragt hab.", weiter: "v3" },
    v3: { wer: "falk", text: "Steht nicht am Bogen, schreiben Sie's drauf.", weiter: "unterbrechung" },
    unterbrechung: { wer: "falk", text: "EKG, bevor Sie weiterreden.", tu: function () { X().zeile = "a"; }, antworten: aMenu },

    /* ---------- A (vorgezogen) und der stumme Zirkel-Takt */
    a_ok: { wer: "falk", text: "{hf}, {pq}. Gut.", weiter: "zirkel1" },
    a_brady: { wer: "falk", text: "{hf} unter Betablocker ist erwartbar, damit fällt niemand um. Was noch?", antworten: aMenu },
    a_unauff: { wer: "falk", text: "{pq} ist nicht unauffällig. Haben Sie gemessen oder geschaut?", antworten: aMenu },
    a_rueck: { wer: "falk", text: "Dann messen Sie, der Wagen steht da. Ich hab zwölf Minuten.",
               tu: function () { X().rueckweg = { art: "wagen", fragen: [], satz: "Dann messen Sie, der Wagen steht da. Ich hab zwölf Minuten." }; X().rueckwege = (X().rueckwege || 0) + 1; },
               endeText: "Bin gleich zurück." },
    zirkel1: { wer: "erzaehler", text: "Falk zieht den Messingzirkel aus der Brusttasche und setzt ihn auf den Streifen, P-Anfang, QRS-Anfang. Drei Schläge, ohne ein Wort.", weiter: "zirkel2" },
    zirkel2: { wer: "falk", text: "{mess_pq}. Passt.", tu: function () { setze("falk_zirkel"); X().zeile = "b"; }, antworten: bMenu },

    /* ---------- B */
    b1: { wer: "falk", text: "Heute nicht genommen. Merken wir uns.", antworten: nachBMenu, weiter: function () { return luecke() ? "luecke" : null; } },
    b2: { wer: "falk", text: "Dann ist es kein Anfall. Das nehm ich.", antworten: nachBMenu, weiter: function () { return luecke() ? "luecke" : null; } },
    b_vage: { wer: "falk", text: "Schön für den Hund. Was nimmt er?", antworten: bMenu },
    b_rueck: { wer: "falk", text: "Dann holen Sie den Zettel. Drei Meter.",
               tu: function () { X().rueckweg = { art: "herrk", fragen: ["r2_1", "r2_1a"], satz: "Dann holen Sie den Zettel. Drei Meter." }; X().rueckwege = (X().rueckwege || 0) + 1; },
               endeText: "Bin gleich zurück." },
    luecke: { wer: "falk", text: function () { return luecke().satz; },
              tu: function () {
                var l = luecke();
                X().rueckweg = { art: l.art, fragen: l.fragen, satz: l.satz, luecke: l.id };
                (X().luecken = X().luecken || []).push(l.id);
                X().zeile = "luecke";
              }, endeText: "Bin gleich zurück." },
    rw_nochmal: { wer: "falk", text: function () { return X().rueckweg.satz; }, endeText: "Bin gleich zurück." },
    f_und: { wer: "falk", text: "Und? Ich hör.",                                                              /* NEU: Wiederaufnahme */
             antworten: function () { var z = X().zeile; return z === "a" ? aMenu() : z === "b" ? bMenu() : rMenu(); } },
    f_und_r: { wer: "falk", text: "Und? Ich hör.", antworten: rMenu },

    /* ---------- R */
    r_ok: { wer: "falk", text: "Monitor, für einen Mann, der lang gestanden ist und Betablocker nimmt. Überzeugen Sie mich.", weiter: "g0" },
    r_heim: { wer: "falk", text: "Das wollte ich hören. Sagen Sie mir, warum, und nicht, weil ich die Koje brauch.", antworten: function () { return heimMenu(); }, weiter: "h_ende" },
    r_steh: { wer: "falk", text: "Marlene hat ihn gemacht, dreimal gemessen, nichts. Was wollen Sie beim zweiten Mal sehen, was beim ersten gefehlt hat?", antworten: rMenu },

    /* ---------- §6.3 Gegenrede */
    g0: { wer: "falk", text: "Lange gestanden, Betablocker, achtundsechzig, Kreislauf, die Steiner hat's auch so gesehen. Ich brauch die Koje, überzeugen Sie mich.",
          tu: function () { X().zeile = "gegenrede"; }, antworten: argMenu },
    h1: { wer: "falk", text: "Dann ist es nicht der Kreislauf. Darf er deshalb heim?", antworten: function () { return heimMenu(); }, weiter: "h_ende" },
    h2: { wer: "falk", text: "Fast.", antworten: function () { return heimMenu(); }, weiter: "h_ende" },
    h3: { wer: "falk", text: "Das hat er gestern auch, und heute lag er in der Küche.", antworten: function () { return heimMenu(); }, weiter: "h_ende" },
    h_ende: { wer: "falk", text: "Sie überzeugen mich nicht. Andersrum: Warum soll er bleiben?",
              warum: "Entlassung aus der Notaufnahme nur bei niedrigem Risiko; prüf die Liste, nicht das Gefühl des Patienten.",
              tu: function () { X().zeile = "gegenrede"; }, antworten: argMenu },
    hinweis: { wer: "falk", text: "Schauen Sie auf Ihre Liste. Was macht aus der fehlenden Vorwarnung ein Warnzeichen?",
               tu: function () { X().hinweis = true; }, antworten: argMenu },
    nachgeben: { wer: "falk", text: "Gut, keine Vorwarnung und ein EKG, das nicht sauber ist, das ist nicht niedrig. Er bleibt am Monitor, bis ich den Speicher gesehen hab.",
                 warum: "Fehlende Vorwarnung zählt nur mit Herzkrankheit oder nicht normalem EKG. Mit PQ {pq} ist er nicht mehr niedrig; das heißt Beobachtung am Monitor, nicht Entlassung. Das Ruhe-EKG beweist nichts; beweisen würde eine Pause über drei Sekunden im Wachen, ein Mobitz II, ein AV-Block III° oder ein Puls dauerhaft unter 40, und die sieht man nur, wenn jemand hinschaut, während es passiert.",
                 tu: function () {
                   setze("entscheidung");
                   if (hat("heim_empfohlen")) ueb().r.push("Dr. Falk: Er bleibt am Monitor, bis ich den Speicher gesehen hab.");
                   vd("rhythmus", "beides", "Ohne Vorwarnung, zweimal, EKG nicht normal (PQ {pq}): nicht niedrig. Beweis bräuchte eine Pause > 3 s im Wachen, Mobitz II, III° oder Sinus < 40. Dafür der Monitor.");
                   vd("reflex", "unwahrscheinlich", "keine Vorwarnung, erstes Mal mit 68, EKG nicht normal");
                   vd("kreislauf", "unwahrscheinlich", "Stehversuch ohne Abfall, nicht beim Aufstehen, keine neue Tablette");
                 }, weiter: "nachgeben2" },
    nachgeben2: { wer: "falk", text: "Die Koje kriegt die Rettung trotzdem, oben ist ein Bett frei. Ich ruf an.", weiter: "tab0" },

    /* ---------- §6.4 Die Tabletten */
    tab0: { wer: "falk", text: "Die Tochter sagt, seine Tabletten liegen daheim am Tisch. Was kriegt er jetzt von uns?",
            antworten: function () { return hat("brady_argument") ? [] : tabMenu(); }, weiter: "tab_brady" },
    tab_brady: { wer: "falk", text: "Vorhin war Ihnen {hf} zu langsam. Jetzt geben Sie ihm die Bremse dazu?", antworten: tabMenu },
    tab1: { wer: "falk", text: "Mit {hf} und einer Überleitung von {pq} geben Sie ihm das Einzige, das beide bremst? Noch einmal.", antworten: tabMenu },
    tab2: { wer: "falk", text: "Gut, der Blutdrucksenker bremst keinen Knoten, den kann er haben. Der Betablocker wartet, ich schreib's auf.", weiter: "bett0" },
    tab3: { wer: "falk", text: "Warum soll er ohne Blutdrucksenker dastehen? Das Einzige, das bremst, ist das Bisoprolol, das andere kann er haben.", antworten: tabMenu },

    /* ---------- §6.5 Falk am Bett */
    bett0: { wer: "falk", text: "Herr Baum, Falk. Ich hör kurz.", tu: function () { P.zeitMin(7 * 60 + 26); },
             weiter: function () { return hat("untersucht") ? "bett1a" : "bett1b"; } },
    bett1a: { wer: "falk", text: "Regelmäßig, langsam, kein Geräusch, wie die Kollegin.", weiter: "bett2" },
    bett1b: { wer: "falk", regie: "zur Spielerin", text: "Haben Sie ihn abgehört? Dann jetzt.", endeText: "Untersuchen",
              dann: function () { untersuchung(function () { P.dialog(B, "bett2"); }); } },
    bett2: { wer: "falk", text: "Ihr Herz leitet zu langsam, und Sie sind zweimal umgefallen. Das will ich über Nacht am Schirm sehen.", weiter: "bett3" },
    bett3: { wer: "falk", text: "Echo macht die Station morgen. Die Kollegin bleibt bei Ihnen.",
             tu: function () { vd("struktur", null, "nicht unter Belastung, kein Geräusch; das Echo macht die Station morgen"); }, weiter: "bett4" },
    bett4: { wer: "herrk", text: "Aber die Senta.", weiter: "bett5" },
    bett5: { wer: "falk", regie: "schon im Gehen, zur Spielerin", text: "Dreiviertel acht, Morgenbesprechung. Sie kommen nach, wenn er oben ist.", weiter: "s0" },

    /* ---------- §7.1 Schlussgespräch */
    s0: { wer: "herrk", regie: "sitzt wieder, Jacke an", text: "Frau Doktor, der Doktor hat was von Schirm gesagt, verstanden hab ich's nicht. Sie sagen's mir, und dann geh ich, die Senta sitzt daheim.",
          tu: function () { P.zeitMin(7 * 60 + 30); }, weiter: "s0b" },
    s0b: { wer: "herrk", text: "Ich unterschreib Ihnen alles.", antworten: sMenu },
    s1: { wer: "herrk", regie: "dreht sich zum Fenster", text: "Für Sie nicht.", antworten: sMenu },
    s2: { wer: "herrk", text: "Her damit. Was steht da drauf, dass ich selber schuld bin?", antworten: sMenu },
    s4: { wer: "herrk", text: "Die Kainz? Und wieso soll ich überhaupt bleiben, der Doktor hat was von Schirm gesagt und ist gegangen.", antworten: sMenu },
    s3: { wer: "herrk", text: "Ja, und? Jetzt bin ich ja da.", antworten: s3Menu },
    s6: { wer: "herrk", text: "Langsam bin ich überall. Das ist das Alter, nicht das Herz.", antworten: s3Menu },
    s5: { wer: "spielerin", text: "Das kann vom Herzen kommen, ein Aussetzer, ein paar Sekunden. Den sieht man nur, wenn Sie am Schirm hängen, während er passiert.", weiter: "s5b" },
    s5b: { wer: "herrk", text: "Ein Aussetzer. Und wenn's keiner ist?", weiter: "s5c" },
    s5c: { wer: "spielerin", text: "Dann wissen wir morgen, dass es keiner war. Heute wissen wir's nicht, deshalb bleiben S' heut am Schirm.", weiter: "s5d" },
    s5d: { wer: "herrk", text: "Und die Senta?", weiter: "s5e" },
    s5e: { wer: "spielerin", text: "Die Frau Kainz hat den Schlüssel, Ihre Tochter ruft sie an. Das soll ich Ihnen sagen, von ihr glauben Sie's nicht.", weiter: "s5f" },
    s5f: { wer: "herrk", regie: function () { return hat("tochter_verraten") ? "" : "zieht die Jacke aus, legt sie über den Sessel"; },
           text: "Die Kainz, die mag sie eh, mehr als mich. Dann bleib ich halt, aber die Mütze bleibt auf.",
           tu: function () { setze("senta_geloest"); },
           weiter: function () { return (hat("versprochen") && !hat("tochter_verraten")) ? "sv1" : hat("tochter_verraten") ? "st1" : "ab0"; } },
    sv1: { wer: "herrk", text: "Sie haben's ihm gesagt, von gestern.", weiter: "sv2" },
    sv2: { wer: "spielerin", text: "Dem Arzt. Nicht der Sabine.", weiter: "sv3" },
    sv3: { wer: "herrk", text: "Passt, der Arzt ist der Arzt.", weiter: "ab0" },
    st1: { wer: "herrk", regie: "zieht die Jacke trotzdem aus", text: "Die Sabine hat's gewusst, wie sie angerufen hat, von Ihnen. Die Kainz hat die Sabine ausgemacht, nicht Sie.", weiter: "ab0" },

    /* ---------- §7.2 Marlenes Abschied und Schlussbild */
    ab0: { wer: "marlene", regie: "mit Kanne, Jacke über dem Arm, an der Koje", text: "So, ich geh. Herr Baum, oben haben's bessere Betten als da, und Sie lassen die Mütze auf, ich kenn Sie.",
           tu: function () { P.zeitMin(7 * 60 + 35); }, weiter: "ab1" },
    ab1: { wer: "marlene", regie: "zur Spielerin", text: "So. Schlaf du auch irgendwann.",
           weiter: function () { return hat("revers") ? "ab_rev" : hat("falk_gewartet") ? "ab_falk" : "ab_e1"; } },
    ab_rev: { wer: "marlene", text: "Revers hat er dir angeboten. Hast ihn nicht gebraucht.", weiter: function () { return hat("falk_gewartet") ? "ab_falk" : "ab_e1"; } },
    ab_falk: { wer: "marlene", text: "Den Falk hast du warten lassen. Der merkt sich das, aber nicht lang.", weiter: "ab_e1" },
    ab_e1: { wer: "erzaehler", text: "{zeit}. Eine Pflegerin und der Transportdienst holen Herrn Baum ab, mit Transportmonitor, die Mütze auf dem Kopf, das Sackerl auf dem Bauch.",
             tu: function () { P.zeitMin(7 * 60 + 40); }, weiter: "ab_e2" },
    ab_e2: { wer: "erzaehler", text: "Die Jacke bleibt über dem Sessel, du nimmst sie mit. Marlenes Stuhl ist leer, die Kanne ist weg; du gehst mit nach oben, dann zur Morgenbesprechung.",
             tu: function () { P.figurAus("herrk"); P.figurAus("marlene"); P.leben("vorbei"); }, endeText: "Weiter", dann: epilog }
  };
  /* Zeitstempel im Text der Erzählerzeile f0/ab_e1: die tatsächliche Uhr (07:15 bzw. 07:40, später bei Verzug). */

  /* Antwortlisten, die Knoten teilen */
  function marleneMenu() {
    var l = [];
    if (!hat("m1")) l.push({ text: "Was ist mit dem Herrn in der Koje?", zu: "m1a", tu: setzeFn("m1") });
    if (!hat("m2")) l.push({ text: "Wo ist der Arzt?", zu: "m2", tu: setzeFn("m2") });
    if (!hat("m3")) l.push({ text: "Was soll ich machen?", zu: "m3", tu: setzeFn("m3") });
    if (l.length) l.push({ text: "Ich geh zu ihm.", z: 0, zu: "m_ende1" });
    return l;
  }
  function b0Menu() {
    var l = [{ text: "KPJ-Studentin, keine Ärztin. Setzen Sie sich, erzählen Sie.", zu: "b_erz" }];
    if (!hat("b_senta")) l.push({ text: "Wer ist die Senta?", zu: "b_senta", tu: setzeFn("b_senta") });
    if (!hat("b_bogen")) l.push({ text: "Ich schau zuerst auf den Bogen.", zu: "b_bogen", tu: setzeFn("b_bogen"),
                                  warum: "Lesen ist richtig; der Bogen hat schon eine Antwort drauf, lies sie als Frage, nicht als Befund." });
    return l;
  }
  function versprechenMenu() {
    var x = X(), l = [];
    if (!x.versprechen) l.push({ text: "Was soll ich ihr nicht sagen?", zu: "r3_rev1", tu: function () { x.versprechen = "frage"; } });
    /* Nach „Was soll ich ihr nicht sagen?" hat er schon erzählt: dann gleich seine Antwort auf das Versprechen. */
    l.push({ text: "Das bleibt unter uns.", zu: function () { return x.vNach ? "r3_danke" : "r3_rev1"; },
             tu: function () { x.vNach = x.versprechen === "frage"; x.versprechen = "unter_uns"; setze("versprochen"); },
             warum: "Versprich nur, was du halten kannst. Was er dir sagt, gehört in die Akte und zum Oberarzt, sonst entscheidet der mit der halben Geschichte; die Tochter erfährt es nur von ihm oder mit seinem Einverständnis." });
    l.push({ text: "Dem Arzt sag ich alles. Der Tochter nur, wenn Sie wollen.", zu: function () { return x.vNach ? "r3_arzt" : "r3_rev1"; },
             tu: function () { x.vNach = x.versprechen === "frage"; x.versprechen = "arzt"; },
             warum: "Richtig: Die Akte ist nicht die Familie. Er entscheidet, was die Tochter erfährt; du entscheidest nicht, was der Oberarzt erfährt." });
    return l;
  }
  function nachMenu() {
    var l = [];
    if (!hat("r3_n1")) l.push({ text: "Gestern vorher etwas gespürt?", zu: "r3_n1", tu: setzeFn("r3_n1") });
    if (!hat("r3_n2")) l.push({ text: "Wie lange sind Sie dort gestanden?", zu: "r3_n2", tu: setzeFn("r3_n2") });
    if (!hat("r3_n3")) l.push({ text: "Haben Sie sich gestern verletzt?", zu: "r3_n3", tu: setzeFn("r3_n3") });
    if (l.length) l.push({ text: "Das reicht mir.", z: 0, zu: "r3_schluss" });
    return l;
  }
  function eMenu() {
    var l = [{ text: "Zehn Sekunden ganz ruhig liegen. Nicht reden.", zu: "e_ruhig", tu: function () { P.leben("ekg"); } }];
    if (!hat("e2")) l.push({ text: "Haben Sie schon einmal ein EKG gehabt?", zu: "e2", tu: setzeFn("e2") });
    return l;
  }
  function tMenu() {
    var l = [];
    if (!hat("t1")) l.push({ text: "Er liegt gerade am EKG. Was haben Sie heute früh gesehen?", zu: "t1a", tu: setzeFn("t1") });
    if (!hat("t2")) l.push({ text: "Hat er gezuckt? Waren die Augen offen?", zu: "t2", tu: setzeFn("t2") });
    if (!hat("t3")) l.push({ text: "Hat er seine Tabletten heute genommen?", zu: "t3", tu: setzeFn("t3") });
    return l;
  }
  function heimMenu() {
    var l = [];
    if (!hat("h1")) l.push({ text: "Stehversuch negativ.", zitat: true, zu: "h1", tu: setzeFn("h1") });
    if (!hat("h2")) l.push({ text: "Das EKG ist fast normal.", zitat: true, zu: "h2", tu: setzeFn("h2") });
    if (!hat("h3")) l.push({ text: "Er fühlt sich gut und will heim.", zitat: true, zu: "h3", tu: setzeFn("h3") });
    return l;
  }
  /* Antworten der Gegenrede als Knoten (eine Replik Falks, bei Vater und TIA mit Einwurf der Spielerin). */
  ARGS.forEach(function (a) {
    var id = "arg_" + a.id;
    if (a.spielerin) {
      B[id] = { wer: "falk", text: a.falk, weiter: id + "_s" };
      B[id + "_s"] = { wer: "spielerin", text: a.spielerin, weiter: id + "_f" };
      B[id + "_f"] = { wer: "falk", text: a.falk2, antworten: nachArg, weiter: nachArgWeiter };
    } else {
      B[id] = { wer: "falk", text: a.falk, antworten: nachArg, weiter: nachArgWeiter };
    }
  });

  /* ---------------------------------------------------------------- Takte, die nicht im Dialog liegen */
  function marleneTresen() {
    P.szenenbild(true);
    P.dialog(B, "m0", function () { P.szenenbild(false); P.zeigeFelder(); });
  }
  function epilog() {
    P.karte("epilog");
    vd("rhythmus", "bewiesen", "Dienst 3: Pause über drei Sekunden im Wachen, ohne Betablocker. Bewiesen.");
    var abs = [
      "Dienst 3, eine Woche später, 18:40, auf dem Weg zur Intensivstation. Marlene fängt dich am Flur ab, die Kanne in der Hand; sie hat's von oben gehört.",
      "In der zweiten Nacht, als vom Betablocker praktisch nichts mehr da war, hat der Monitor eine Pause aufgezeichnet, länger als drei Sekunden. Er war wach, ihm war schwindlig, er hat geklingelt.",
      "Am Donnerstag hat er einen Zweikammer-Schrittmacher bekommen, am Samstag ist er heim, die Mütze auf dem Kopf."
    ];
    if (hat("senta_geloest")) abs.push("Die Senta hat die Frau Kainz bis zum Parkplatz gebracht. Weiter durfte sie nicht.");
    if (hat("tochter_beruhigt")) abs.push("Die Tochter hat dich gefragt, warum du am Montag „Kreislauf“ gesagt hast. Du hast es ihr erklärt, es hat gedauert.");
    P.epilog(abs, function () { P.ende(); });
  }

  /* ================================================================ Schnittstelle zum Motor */
  global.FALL1 = {
    werte: { puls: 52, rr_l_sys: 142, rr_l_dia: 84, rr_s1_sys: 136, rr_s1_dia: 82, rr_s3_sys: 134, rr_s3_dia: 80,
             spo2: 96, temp: 36.6, zucker: 104, medi1: "Bisoprolol 5 mg", medi2: "Ramipril 5 mg", medi3: "ASS 100 mg" },
    verdacht: VERDACHT,
    karten: KARTEN,
    vergleiche: VERGLEICHE,
    baeume: B,
    vars: function (v) { v.fehlt = fehlt(); },
    flags: [
      { id: "versprochen", wenn: "„Das bleibt unter uns“ (Wendung, Runde 3)" },
      { id: "anruf_spaeter", wenn: "„Das kann warten, erst das EKG“" },
      { id: "tochter_beruhigt", wenn: "am Telefon „Wahrscheinlich nur der Kreislauf“" },
      { id: "tochter_verraten", wenn: "am Telefon das zweite Ereignis erzählt" },
      { id: "heim_empfohlen", wenn: "Übergabe, Zeile R: „Er kann heim“" },
      { id: "brady_argument", wenn: "„Bradykardie … erklärt die Ohnmacht“ oder „Puls …, das ist eine Bradykardie“" },
      { id: "falk_gewartet", wenn: "07:15 ohne geschriebenes EKG" },
      { id: "revers", wenn: "„Dann unterschreiben Sie einen Revers“" },
      { id: "senta_geloest", wenn: "Frau Kainz genannt (Schlussgespräch)" }
    ],
    start: function () {
      P.leben("uhr_blick");
      P.dialog(B, "a1");
    },
    feld: function (name) {
      var x = X(), rw = x.rueckweg;
      if (name === "marlene") {
        if (P.Z.falkDa && !hat("entscheidung")) { falkTresen(); return; }
        P.vor(1);
        P.dialog(B, "m_idle");
        return;
      }
      if (name === "wagen") {
        if (!(hat("r1_1") && hat("r1_2"))) { P.melde("Marlene, vom Tresen: „Lass den Wagen noch. Du weißt ja nicht einmal, was passiert ist.“"); return; }
        if (!hat("wagen_da")) { P.vor(1); P.dialog(B, "w1"); return; }
        if (!hat("ekg_geschrieben")) { P.dialog(B, "e1"); return; }
        if (!hat("rhythmus")) { rhythmusFrage(); return; }
        messWahl();
        return;
      }
      /* Herr Baum (und das Sackerl) */
      if (rw && rw.art === "herrk" && !rueckwegErfuellt(rw)) { P.dialog(B, "rw_start"); return; }
      if (rw && rw.art === "tochter" && !P.hatKarte("fremd")) { x.anruf = "rueck"; P.dialog(B, "t0"); return; }
      if (!hat("r1_start")) { P.dialog(B, "b0"); return; }
      if (!hat("r2_fertig")) { P.dialog(B, "r2_0"); return; }
      if (!hat("r3_fertig")) { P.dialog(B, "r3_0"); return; }
      P.vor(1);
      P.dialog(B, "b_idle");
    },
    leerlauf: function () {
      if (!P.Z.falkDa && P.Z.zeit >= FALK) falkKommt();
    },
    zeitGeht: function (vorher, jetzt) {
      if (vorher < 7 * 60 && jetzt >= 7 * 60) P.leben("vorbei");        /* 07:00: Andrea kommt, jemand geht vorbei */
    },
    stand: function () {
      var z = P.Z, x = z.x, rw = x.rueckweg, s = [], knopf = null, frist;
      if (hat("entscheidung")) frist = "Entschieden: Beobachtung am Monitor.";
      else if (z.falkDa) frist = "Dr. Falk ist da. Es ist " + P.zeitText() + ".";
      else frist = "Dr. Falk fragt um 07:15. Jetzt ist es " + P.zeitText() + ".";
      if (!hat("marlene_tresen")) s.push("Marlene ist am Tresen und übergibt dir den Fall.");
      else if (z.falkDa && rw) {
        if (rueckwegErfuellt(rw)) s.push("Du hast, was Dr. Falk wissen wollte.");
        else if (rw.art === "wagen") s.push("Dr. Falk will die Zahlen.", "Miss am EKG-Wagen nach, dann zurück zum Tresen.");
        else if (rw.art === "tochter") s.push("Dr. Falk will wissen, was die Tochter gesehen hat.", "Ruf sie von Herrn Baums Handy aus an, dann zurück zum Tresen.");
        else s.push("Dr. Falk hat gefragt: „" + rw.satz + "“", "Frag Herrn Baum in der Koje, dann zurück zum Tresen.");
        knopf = { text: "Zurück zu Falk", tu: falkTresen };
      } else if (z.falkDa && !hat("ekg_geschrieben")) {
        s.push("Dr. Falk liest am Tresen und wartet auf das EKG.", "Der Wagen steht bereit.");
      } else if (z.falkDa) {
        s.push("Dr. Falk wartet am Tresen.");
        knopf = { text: "Zum Tresen", tu: falkTresen };
      } else if (hat("ekg_geschrieben")) {
        s.push("Falk kommt um viertel nach sieben. Was sagst du ihm zuerst?", "Mappe und Verdacht liegen bereit.");
        knopf = { text: "Zum Tresen, Falk ist da", tu: function () { if (!hat("rhythmus")) rhythmusFrage(); else falkJetzt(); } };
      } else if (!hat("r1_start")) {
        s.push("Herr Baum wartet in der Koje drei, die Jacke schon an.", "Red mit ihm.");
      } else {
        s.push("Der EKG-Wagen ist frei, sobald du willst.");
        if (!hat("r2_fertig") || !hat("r3_fertig")) s.push("Herrn Baum kannst du weiter fragen; die Uhr läuft mit jeder Frage.");
      }
      return { frage: "Darf Herr Baum heim?", frist: frist, saetze: s, knopf: knopf };
    },
    ende: function () {
      var namen = { r1_4: "Verletzung", r3_2: "„Schon einmal?“", r2_2: "Zucker und Krankheiten", r3_1: "Familie", fremd: "die Tochter" };
      var l = (X().luecken || []).map(function (id) { return namen[id]; });
      var t = l.length ? "Dr. Falk hat nachgefragt: " + l.join(", ") + "." : "Dr. Falk musste nichts nachfragen.";
      if (X().rueckwege) t += " Rückwege von der Übergabe zum Wagen oder Zettel: " + X().rueckwege + ".";
      return t;
    },
    /* für pruefe.mjs */
    __luecke: luecke,
    __rw: function () { var rw = X().rueckweg; return rw ? { art: rw.art, erfuellt: rueckwegErfuellt(rw), satz: rw.satz } : null; }
  };
})(window);
