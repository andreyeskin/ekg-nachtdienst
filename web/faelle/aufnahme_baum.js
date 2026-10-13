/* Fall „aufnahme_baum" — Herr Konrad Baum, 68: Synkope. Dienst 1, 06:40, Aufnahme.
   Akte: docs/faelle/aufnahme_baum.md (Anamnese, Differenzialdiagnosen, Belege).
   Lehrbuch: Lektion 3 (PQ), 4 (QRS), 7 (Rhythmus, Frequenz), 8 (Sinusrhythmus), 10 (AV-Block I°);
   Synkope: ESC-Synkope-2018 (docs/QUELLEN.md §3, §8a). Lektionsnummern stehen nur hier, nie im Spieltext.

   Reines Datenobjekt für web/motor/fall.js: Texte als IDs (text/de/aufnahme_baum.json), Bedingungen
   und Wirkungen als Strings. Zahlen im Text sind Platzhalter: feste Werte des Falls aus `werte`
   (Pflegeanamnese), Messungen aus dem Zirkel (hf, rr, pq, qrs) — nie Literale.                  */
(function (global) {
  "use strict";

  /* Die Antwortlisten der Anamnese: Jede Frage verschwindet, sobald sie gestellt ist. */
  var EREIGNIS = [
    { text: "baum.herrk.f.prodrom", zu: "prodrom", wenn: "!hat:a_prodrom" },
    { text: "baum.herrk.f.situation", zu: "situation", wenn: "!hat:a_situation" },
    { text: "baum.herrk.f.dauer", zu: "dauer", wenn: "!hat:a_dauer" },
    { text: "baum.herrk.f.erholung", zu: "erholung", wenn: "!hat:a_erholung" },
    { text: "baum.herrk.f.drumherum", zu: "drumherum",
      wenn: "!hat:a_zeugin | !hat:a_verletzung | !hat:a_zunge | !hat:a_herzrasen | !hat:a_brust | !hat:a_neuro" },
    { text: "baum.knopf.zurueck", zu: "start" }
  ];
  var DRUMHERUM = [
    { text: "baum.herrk.f.zeugin", zu: "zeugin", wenn: "!hat:a_zeugin" },
    { text: "baum.herrk.f.verletzung", zu: "verletzung", wenn: "!hat:a_verletzung" },
    { text: "baum.herrk.f.zunge", zu: "zunge", wenn: "!hat:a_zunge" },
    { text: "baum.herrk.f.herzrasen", zu: "herzrasen", wenn: "!hat:a_herzrasen" },
    { text: "baum.herrk.f.brust", zu: "brust", wenn: "!hat:a_brust" },
    { text: "baum.herrk.f.neuro", zu: "neuro", wenn: "!hat:a_neuro" },
    { text: "baum.knopf.zurueck", zu: "start" }
  ];
  var MEDIS = [
    { text: "baum.herrk.f.aenderung", zu: "aenderung", wenn: "!hat:a_aenderung" },
    { text: "baum.herrk.f.diabetes", zu: "diabetes", wenn: "!hat:a_diabetes" },
    { text: "baum.herrk.f.alkohol", zu: "alkohol", wenn: "!hat:a_alkohol" },
    { text: "baum.knopf.zurueck", zu: "start" }
  ];
  var PERSON = [
    { text: "baum.herrk.f.frueher", zu: "frueher", wenn: "!hat:a_frueher" },
    { text: "baum.herrk.f.familie", zu: "familie", wenn: "!hat:a_familie" },
    { text: "baum.knopf.zurueck", zu: "start" }
  ];
  /* Marlenes Expertenfragen — die Denkwege, die eine Ärztin reflexhaft prüft (Akte §4, §5). */
  var FRAGEN = [
    { text: "baum.marlene.f.vorwarnung", zu: "vorwarnung", wenn: "!hat:m_vorwarnung" },
    { text: "baum.marlene.f.tia", zu: "tia", wenn: "!hat:m_tia" },
    { text: "baum.marlene.f.krampf", zu: "krampf", wenn: "!hat:m_krampf" },
    { text: "baum.marlene.f.zucker", zu: "zucker", wenn: "!hat:m_zucker" },
    { text: "baum.marlene.f.orthostase", zu: "orthostase", wenn: "!hat:m_orthostase" },
    { text: "baum.marlene.f.fertig", zu: "start" }
  ];
  /* Dr. Falk nimmt nur Zahlen an — beide. */
  var FALK_ZAHLEN = [
    { text: [{ wenn: "karte:b-qrs", text: "baum.falk.a.beide_qrs" }, { text: "baum.falk.a.beide" }],
      wenn: ["karte:b-frequenz", "karte:b-pq"], zu: "gut" },
    { text: "baum.falk.a.nur_hf", wenn: ["karte:b-frequenz", "!karte:b-pq"], zu: "halb" },
    { text: "baum.falk.a.nur_pq", wenn: ["karte:b-pq", "!karte:b-frequenz"], zu: "halb_pq" }
  ];
  var FALK_HUB = [
    { text: "baum.falk.a.tia", zu: "f_tia", wenn: "!hat:f_tia" },
    { text: "baum.falk.a.orthostase", zu: "f_orthostase", wenn: "!hat:f_orthostase" },
    { text: "baum.falk.a.weiter", zu: "entscheidung" }
  ];

  global.FAELLE = global.FAELLE || {};
  global.FAELLE.aufnahme_baum = {
    id: "aufnahme_baum", kuerzel: "baum",
    lektionen: "3, 4, 7, 8, 10; ESC-Synkope-2018",
    dienst: 1, zeit: 6 * 60 + 40,
    patient: { name: "Konrad Baum", alter: 68, figur: "herr_k" },
    /* LUDB 39: Sinusrhythmus 53/min (Etikett „Sinus bradycardia"; Lektion 8: Bradykardie erst < 50), PQ 228 ms →
       AV-Block I°, QRS 86 ms. Ersatz derselben Gruppe (Akte §2) — noch nicht gezogen, nur dokumentiert. */
    aufnahme: { haupt: 39, ersatz: [134, 78, 107] },

    /* Pflegeanamnese (Akte §3) — die Zahlen stehen nur hier, die Texte tragen Platzhalter. */
    werte: {
      puls: 52, rr_l_sys: 142, rr_l_dia: 84, rr_s1_sys: 136, rr_s1_dia: 82, rr_s3_sys: 134, rr_s3_dia: 80,
      spo2: 96, temp: 36.6, zucker: 104, zucker_mmol: 5.8,
      medi1: "Bisoprolol 5 mg", medi2: "Ramipril 5 mg", medi3: "ASS 100 mg"
    },

    /* Pflichtfragen der Synkopen-Anamnese (Akte §5; ESC-Practical-2018 Web Tables 5.1–5.6). */
    pflicht: [
      { marke: "a_ereignis", name: "baum.pflicht.ereignis" },
      { marke: "a_prodrom", name: "baum.pflicht.prodrom" },
      { marke: "a_situation", name: "baum.pflicht.situation" },
      { marke: "a_dauer", name: "baum.pflicht.dauer" },
      { marke: "a_erholung", name: "baum.pflicht.erholung" },
      { marke: "a_verletzung", name: "baum.pflicht.verletzung" },
      { marke: "a_zeugin", name: "baum.pflicht.zeugin" },
      { marke: "a_medis", name: "baum.pflicht.medis" },
      { marke: "a_vorerkrankungen", name: "baum.pflicht.vorerkrankungen" },
      { marke: "a_familie", name: "baum.pflicht.familie" }
    ],
    kern: ["b-rhythmus", "b-frequenz", "b-pq"],

    /* Regeln laufen nach jeder Wirkung. */
    regeln: [
      { wenn: ["pflicht", "!karte:b-anamnese"], tu: ["karte:anamnese"] },
      { wenn: ["mind:2:b-rhythmus,b-frequenz,b-pq", "!hat:falk_gerufen", "!hat:bericht{n_kern}", "!hat:wink{n_kern}"],
        tu: ["setze:wink{n_kern}", "melde:baum.meld.marlene"] },
      { wenn: ["hat:falk_schickt_zurueck", "karte:b-frequenz", "karte:b-pq", "!hat:wink_falk"],
        tu: ["setze:wink_falk", "melde:baum.meld.falk"] },
      { wenn: ["hat:falk_schickt_patient", "karte:b-medis", "!hat:wink_patient"],
        tu: ["setze:wink_patient", "melde:baum.meld.falk"] }
    ],

    /* ------------------------------------------------------------ Dialoge */
    dialoge: {
      auftakt: {
        figur: "erzaehler",
        knoten: {
          start: { text: "baum.auftakt.start", ende: "baum.knopf.zum_tresen", nach: ["felder:zeigen"] },
          falk_kommt: { text: "baum.auftakt.falk_kommt", weiter: "start", weiterBaum: "falk" },
          ende: { text: "baum.auftakt.ende", ende: "Weiter", nach: ["felder:zeigen"] },
          /* Epilog (KONZEPT §7, Entscheidung des Nutzers): Erzählung in einem späteren Dienst, ohne neues Lernziel.
             Pause > 3 s im Wachen ist nach ESC-Synkope-2018 §4.1.1 beweisend (QUELLEN §3); keine Kurve, kein Standbild. */
          epilog: { text: "baum.epilog.1", weiter: "epilog2" },
          epilog2: { text: "baum.epilog.2", weiter: "epilog3" },
          epilog3: { text: "baum.epilog.3", ende: "baum.knopf.ende" }
        }
      },

      marlene: {
        knoten: {
          /* Erstes Gespräch im Szenenbild: Marlene reicht den Aufnahmebogen (art/szenenbilder/aufnahme_tresen…). */
          erst: {
            text: "baum.marlene.erst",
            antworten: [
              { text: "baum.marlene.a.werte", zu: "werte" },
              { text: "baum.marlene.a.fragen", zu: "fragen_erst" },
              { text: "baum.marlene.a.zu_ihm", zu: "bogen" }
            ]
          },
          werte: {
            text: "baum.marlene.werte", tu: ["setze:werte_gehoert"],
            antworten: [
              { text: "baum.marlene.a.fragen", zu: "fragen_erst", wenn: "!hat:fragen_gehoert" },
              { text: "baum.marlene.a.danke_zu_ihm", zu: "bogen" }
            ]
          },
          fragen_erst: {
            text: "baum.marlene.fragen_erst", tu: ["setze:fragen_gehoert"],
            antworten: [
              { text: "baum.marlene.a.werte", zu: "werte", wenn: "!hat:werte_gehoert" },
              { text: "baum.marlene.a.gut_zu_ihm", zu: "bogen" }
            ]
          },
          bogen: {
            text: "baum.marlene.bogen", tu: ["setze:vorgestellt", "karte:aufnahmebogen"],
            ende: "baum.knopf.danke", nach: ["szenenbild:weg", "felder:zeigen"]
          },

          start: {
            text: [
              { wenn: "hat:fall_ende", text: "baum.marlene.start.oben" },
              { wenn: "hat:falk_wartet", text: "baum.marlene.start.falk" },
              { text: "baum.marlene.start.wieder" }
            ],
            antworten: [
              { text: "baum.marlene.a.zu_falk", wenn: ["hat:falk_wartet", "!hat:fall_ende"], zu: null, tu: ["dialog:falk.start"] },
              { text: [
                  { wenn: ["karte:b-frequenz", "karte:b-pq"], text: "baum.marlene.a.bericht_beide" },
                  { wenn: "karte:b-frequenz", text: "baum.marlene.a.bericht_hf" },
                  { wenn: "karte:b-pq", text: "baum.marlene.a.bericht_pq" },
                  { text: "baum.marlene.a.bericht_sinus" }
                ],
                wenn: ["mind:1:b-rhythmus,b-frequenz,b-pq", "!hat:bericht{n_kern}", "!hat:falk_gerufen"], zu: "bericht" },
              { text: "baum.marlene.a.fragen_hub",
                wenn: ["hat:a_ereignis", "!hat:m_vorwarnung | !hat:m_tia | !hat:m_krampf | !hat:m_zucker | !hat:m_orthostase"],
                zu: "fragen" },
              { text: "baum.marlene.a.sticker", wenn: "!hat:sticker", zu: "sticker" },
              { text: "baum.marlene.a.spaeter", zu: null }
            ]
          },
          bericht: {
            text: [
              { wenn: ["karte:b-pq", "karte:b-frequenz"], text: "baum.marlene.bericht.beide" },
              { wenn: "karte:b-pq", text: "baum.marlene.bericht.pq" },
              { wenn: "karte:b-frequenz", text: "baum.marlene.bericht.hf" },
              { text: "baum.marlene.bericht.sinus" }
            ],
            tu: ["setze:bericht{n_kern}",
                 { wenn: "mind:2:b-rhythmus,b-frequenz,b-pq", tu: ["setze:falk_gerufen", "zeit:+10"] }],
            ende: "baum.knopf.danke_marlene",
            nach: [{ wenn: ["hat:falk_gerufen", "!hat:falk_da"], tu: ["dialog:auftakt.falk_kommt"] }]
          },

          fragen: { text: "baum.marlene.fragen", antworten: FRAGEN },
          /* ESC-Synkope-2018 §4.1.1, Tab. 5/7: Prodrom spricht für Reflexsynkope; „ohne Prodrom" ist Risikomerkmal (QUELLEN §3). */
          vorwarnung: {
            text: "baum.marlene.vorwarnung", tu: ["setze:m_vorwarnung"],
            antworten: [{ text: "baum.marlene.a.beweis", zu: "beweis" }].concat(FRAGEN)
          },
          /* Beweisend (ESC §4.1.1, Klasse I C): Sinusbradykardie < 40 dauerhaft, Pause > 3 s im Wachen, Mobitz II, III°. */
          beweis: { text: "baum.marlene.beweis", antworten: FRAGEN },
          /* ESC Tab. 4, §8.1.3: TIA = fokales Defizit ohne Bewusstseinsverlust; vertebrobasilär nie ohne Herdzeichen. */
          tia: {
            text: "baum.marlene.tia", tu: ["setze:m_tia"],
            antworten: [{ text: "baum.marlene.a.hirnstamm", zu: "tia2" }].concat(FRAGEN)
          },
          tia2: { text: "baum.marlene.tia2", antworten: FRAGEN },
          /* ESC §8.1.2, Tab. 10: Myoklonien, seitlicher Zungenbiss, langsames Wiederklarwerden sprechen für einen Anfall. */
          krampf: { text: "baum.marlene.krampf", tu: ["setze:m_krampf"], antworten: FRAGEN },
          /* ESC Tab. 4; ESC-Practical Web Table 5.6: Hypoglykämie — kein Diabetes, Stix normal, Verlauf zu kurz. */
          zucker: { text: "baum.marlene.zucker", tu: ["setze:m_zucker"], antworten: FRAGEN },
          /* ESC Tab. 5: Orthostase beim/nach dem Aufstehen, Beginn/Wechsel blutdrucksenkender Mittel; Stehblutdruck bei allen. */
          orthostase: { text: "baum.marlene.orthostase", tu: ["setze:m_orthostase"], antworten: FRAGEN },
          sticker: { text: "baum.marlene.sticker", tu: ["setze:sticker"], antworten: [{ text: "baum.knopf.zurueck", zu: "start" }] }
        }
      },

      herr_k: {
        knoten: {
          start: {
            text: [{ wenn: "hat:k_begruesst", text: "baum.herrk.start.wieder" }, { text: "baum.herrk.start.erst" }],
            tu: ["setze:k_begruesst"],
            antworten: [
              { text: "baum.herrk.f.ereignis", zu: "ereignis", wenn: "!hat:a_ereignis" },
              { text: "baum.herrk.f.ereignis_mehr", zu: "ereignis_hub",
                wenn: ["hat:a_ereignis", "!hat:a_prodrom | !hat:a_situation | !hat:a_dauer | !hat:a_erholung | !hat:a_zeugin | !hat:a_verletzung | !hat:a_zunge | !hat:a_herzrasen | !hat:a_brust | !hat:a_neuro"] },
              { text: "baum.herrk.f.medis", zu: "medis", wenn: "!hat:a_medis" },
              { text: "baum.herrk.f.medis_mehr", zu: "medis_hub",
                wenn: ["hat:a_medis", "!hat:a_aenderung | !hat:a_diabetes | !hat:a_alkohol"] },
              { text: "baum.herrk.f.vorerkrankungen", zu: "vorerkrankungen", wenn: "!hat:a_vorerkrankungen" },
              { text: "baum.herrk.f.person_mehr", zu: "person_hub",
                wenn: ["hat:a_vorerkrankungen", "!hat:a_frueher | !hat:a_familie"] },
              { text: "baum.herrk.f.untersuchen", zu: "untersuchen", wenn: "!hat:untersucht" },
              { text: "baum.herrk.f.foto", zu: "foto", wenn: ["hat:a_ereignis", "!hat:foto_gefragt"] },
              { text: "baum.herrk.f.spaeter", zu: null }
            ]
          },
          /* Das Ereignis: alle vier T-LOC-Merkmale (ESC §4.1), kein Prodrom. */
          ereignis: { text: "baum.herrk.ereignis", tu: ["setze:a_ereignis", "zeit:+1"], antworten: EREIGNIS },
          ereignis_hub: { text: "baum.herrk.hub", antworten: EREIGNIS },
          prodrom: { text: "baum.herrk.prodrom", tu: ["setze:a_prodrom", "zeit:+1"], antworten: EREIGNIS },
          situation: { text: "baum.herrk.situation", tu: ["setze:a_situation", "zeit:+1"], antworten: EREIGNIS },
          dauer: { text: "baum.herrk.dauer", tu: ["setze:a_dauer", "zeit:+1"], antworten: EREIGNIS },
          erholung: { text: "baum.herrk.erholung", tu: ["setze:a_erholung", "zeit:+1"], antworten: EREIGNIS },
          drumherum: { text: "baum.herrk.drumherum", antworten: DRUMHERUM },
          zeugin: { text: "baum.herrk.zeugin", tu: ["setze:a_zeugin", "zeit:+1"], antworten: DRUMHERUM },
          verletzung: { text: "baum.herrk.verletzung", tu: ["setze:a_verletzung", "zeit:+1"], antworten: DRUMHERUM },
          zunge: { text: "baum.herrk.zunge", tu: ["setze:a_zunge", "zeit:+1"], antworten: DRUMHERUM },
          herzrasen: { text: "baum.herrk.herzrasen", tu: ["setze:a_herzrasen", "zeit:+1"], antworten: DRUMHERUM },
          brust: { text: "baum.herrk.brust", tu: ["setze:a_brust", "zeit:+1"], antworten: DRUMHERUM },
          neuro: { text: "baum.herrk.neuro", tu: ["setze:a_neuro", "zeit:+1"], antworten: DRUMHERUM },
          /* Medikamente: der Plan vom Hausarzt wird gereicht — Karte entsteht im Gespräch, nicht in der Tüte (KONZEPT §1.3). */
          medis: { text: "baum.herrk.medis", tu: ["setze:a_medis", "karte:medis", "zeit:+2"], antworten: MEDIS },
          medis_hub: { text: "baum.herrk.hub", antworten: MEDIS },
          aenderung: { text: "baum.herrk.aenderung", tu: ["setze:a_aenderung", "zeit:+1"], antworten: MEDIS },
          diabetes: { text: "baum.herrk.diabetes", tu: ["setze:a_diabetes", "zeit:+1"], antworten: MEDIS },
          alkohol: { text: "baum.herrk.alkohol", tu: ["setze:a_alkohol", "zeit:+1"], antworten: MEDIS },
          vorerkrankungen: { text: "baum.herrk.vorerkrankungen", tu: ["setze:a_vorerkrankungen", "zeit:+1"], antworten: PERSON },
          person_hub: { text: "baum.herrk.hub", antworten: PERSON },
          frueher: { text: "baum.herrk.frueher", tu: ["setze:a_frueher", "zeit:+1"], antworten: PERSON },
          familie: { text: "baum.herrk.familie", tu: ["setze:a_familie", "zeit:+1"], antworten: PERSON },
          untersuchen: { text: "baum.herrk.untersuchen", ende: "baum.knopf.nur_kurz", nach: ["aufgabe:untersuchung"] },
          foto: { text: "baum.herrk.foto", tu: ["setze:foto_gefragt"], antworten: [{ text: "baum.knopf.schoen", zu: "start" }] }
        }
      },

      /* Dr. Falk kommt an den Tresen: Porträt-Dialog ohne Raumfigur (UMBAU §2b, Entscheidung des Nutzers). */
      falk: {
        knoten: {
          start: {
            text: [{ wenn: "hat:falk_da", text: "baum.falk.start.wieder" }, { text: "baum.falk.start.erst" }],
            tu: ["setze:falk_da", "setze:falk_wartet"],
            antworten: FALK_ZAHLEN.concat([{ text: "baum.falk.a.anamnese", zu: "anamnese" }])
          },
          anamnese: { text: "baum.falk.anamnese", antworten: FALK_ZAHLEN },
          gut: {
            text: [{ wenn: "karte:b-qrs", text: "baum.falk.gut_qrs" }, { text: "baum.falk.gut" }],
            antworten: [
              { text: "baum.falk.a.bisoprolol", wenn: "karte:b-medis", zu: "tabletten" },
              { text: "baum.falk.a.weiss_nicht", wenn: "!karte:b-medis", zu: "ohne_medis" }
            ]
          },
          ohne_medis: { text: "baum.falk.ohne_medis", tu: ["setze:falk_schickt_patient"], ende: "baum.knopf.gleich_zurueck" },
          /* Betablocker bremsen Sinusknoten und AV-Überleitung (QUELLEN §3); das erklärt die Zahlen, nicht die Ohnmacht (§4). */
          tabletten: { text: "baum.falk.tabletten", tu: ["setze:falk_tabletten"], antworten: FALK_HUB },
          f_tia: { text: "baum.falk.tia", tu: ["setze:f_tia"], weiter: "f_tia2" },
          f_tia2: { text: "baum.falk.tia2", antworten: [{ text: "baum.falk.a.seitengleich", zu: "f_tia3" }] },
          f_tia3: { text: "baum.falk.tia3", antworten: FALK_HUB },
          f_orthostase: { text: "baum.falk.orthostase", tu: ["setze:f_orthostase"], antworten: FALK_HUB },
          /* Entscheidung (Akte §8): ohne Prodrom + auffälliges EKG → Beobachtung am Monitor (ESC §4.1.2, Tab. 6/7). Keine Therapie. */
          entscheidung: { text: "baum.falk.entscheidung", weiter: "entscheidung2" },
          entscheidung2: { text: "baum.falk.entscheidung2", weiter: "entscheidung3" },
          entscheidung3: {
            text: "baum.falk.entscheidung3", tu: ["setze:fall_ende", "loesche:falk_wartet", "zeit:+5"],
            ende: "baum.knopf.verstanden", nach: ["dialog:auftakt.ende"]
          },
          halb: { text: "baum.falk.halb", antworten: [{ text: "baum.falk.a.nicht_gemessen", zu: "zurueck" }] },
          halb_pq: { text: "baum.falk.halb_pq", antworten: [{ text: "baum.falk.a.hol_nach", zu: "zurueck" }] },
          zurueck: { text: "baum.falk.zurueck", tu: ["setze:falk_schickt_zurueck", "zeit:+3"], ende: "baum.knopf.gleich_zurueck" }
        }
      }
    },

    /* ------------------------------------------------------------ Karten der Mappe */
    karten: {
      aufnahmebogen: {
        id: "b-bogen", titel: "baum.karte.bogen.titel", text: "baum.karte.bogen.text", symbol: "bogen",
        vergleich: { "b-frequenz": "baum.karte.bogen.vs_frequenz" }
      },
      medis: {
        id: "b-medis", titel: "baum.karte.medis.titel", text: "baum.karte.medis.text", symbol: "tabletten",
        vergleich: { "b-frequenz": "baum.karte.medis.vs_frequenz", "b-pq": "baum.karte.medis.vs_pq" }
      },
      untersuchung: { id: "b-untersuchung", titel: "baum.karte.untersuchung.titel", text: "baum.karte.untersuchung.text", symbol: "stethoskop" },
      anamnese: { id: "b-anamnese", titel: "baum.karte.anamnese.titel", text: "baum.karte.anamnese.text", symbol: "notiz" },
      rhythmus: {
        id: "b-rhythmus", titel: "baum.karte.rhythmus.titel", text: "baum.karte.rhythmus.text",
        ekg: { satz: "haupt", mmProS: 25, von: 1.8, dauer: 6 }
      },
      /* Lektion 8: Norm 50–100/min, Sinusbradykardie < 50, Sinustachykardie > 100. */
      frequenz: {
        id: "b-frequenz", titel: "baum.karte.frequenz.titel",
        text: [
          { wenn: "hf<50", text: "baum.karte.frequenz.brady" },
          { wenn: "hf>100", text: "baum.karte.frequenz.tachy" },
          { wenn: "hf<=60", text: "baum.karte.frequenz.rand" },
          { text: "baum.karte.frequenz.norm" }
        ],
        ekg: { satz: "haupt", mmProS: 25, von: 1.9, dauer: 6 }
      },
      /* Lektion 3/10: PQ 120–200 ms; > 200 ms AV-Block I°, jeder Vorhofimpuls wird übergeleitet. */
      pq: {
        id: "b-pq", titel: "baum.karte.pq.titel",
        text: [{ wenn: "pq>200", text: "baum.karte.pq.block" }, { text: "baum.karte.pq.norm" }],
        ekg: { satz: "haupt", mmProS: 50, von: 2.9, dauer: 2.4 },
        vergleich: { "b-frequenz": "baum.karte.pq.vs_frequenz" }
      },
      /* Lektion 4: QRS 60–100 ms; schmal heißt: die Kammern werden über das normale Leitungssystem erregt (QUELLEN §3). */
      qrs: {
        id: "b-qrs", titel: "baum.karte.qrs.titel",
        text: [{ wenn: "qrs<=100", text: "baum.karte.qrs.schmal" }, { text: "baum.karte.qrs.breit" }],
        ekg: { satz: "haupt", mmProS: 50, von: 2.9, dauer: 2.4 },
        vergleich: { "b-pq": "baum.karte.qrs.vs_pq" }
      }
    },

    /* ------------------------------------------------------------ Aufgaben */
    aufgaben: {
      /* Reihenfolge nach Lektion 7/34: erst der Rhythmus, dann die Zahlen. Antworten sind bloße Diagnosen;
         die Kriterien tragen die Rückmeldungen (Lektion 8, 25, 26). */
      ekg: {
        art: "frage", einmal: "ekg_geschrieben", vorher: ["zeit:+8", "melde:baum.meld.ekg"],
        titel: "baum.ekg.titel", text: "baum.ekg.text",
        ekg: { mmProS: 25, von: 1.8, dauer: 7 },
        antworten: [
          { text: "baum.ekg.a.vhf", warum: "baum.ekg.w.vhf" },
          { text: "baum.ekg.a.sinus", richtig: true, warum: "baum.ekg.w.sinus" },
          { text: "baum.ekg.a.vt", warum: "baum.ekg.w.vt" }
        ],
        fertig: ["karte:rhythmus", "zeit:+3"]
      },
      wahl: {
        art: "wahl", titel: "baum.wahl.titel",
        text: [{ wenn: "hat:fall_ende", text: "baum.wahl.text_spaeter" }, { text: "baum.wahl.text" }],
        wahl: [
          { text: "baum.wahl.rr", karte: "b-frequenz", aufgabe: "rr" },
          { text: "baum.wahl.pq", karte: "b-pq", aufgabe: "pq" },
          { text: "baum.wahl.qrs", karte: "b-qrs", aufgabe: "qrs" }
        ]
      },
      /* Toleranzen (± 25 ms RR, ± 20 ms PQ/QRS) sind Spielentscheidungen, keine Lehrbuchwerte (FACHREGELN). */
      rr: {
        art: "zirkel", was: "rr", toleranz: 25, mmProS: 25, von: 1.9, dauer: 7,
        titel: "baum.zirkel.rr.titel", auftrag: "baum.zirkel.rr.auftrag",
        deutung: { aus: "hf", regeln: [
          { wenn: "hf<50", text: "baum.zirkel.rr.brady" }, { wenn: "hf>100", text: "baum.zirkel.rr.tachy" },
          { wenn: "hf<=60", text: "baum.zirkel.rr.rand" }, { text: "baum.zirkel.rr.norm" }
        ] },
        fertig: ["karte:frequenz", "zeit:+6"]
      },
      pq: {
        art: "zirkel", was: "pq", toleranz: 20, mmProS: 50, von: 2.9, dauer: 2.6,
        titel: "baum.zirkel.pq.titel", auftrag: "baum.zirkel.pq.auftrag",
        deutung: { aus: "ms", regeln: [{ wenn: "ms>200", text: "baum.zirkel.pq.block" }, { text: "baum.zirkel.pq.norm" }] },
        fertig: ["karte:pq", "zeit:+6"]
      },
      qrs: {
        art: "zirkel", was: "qrs", toleranz: 20, mmProS: 50, von: 2.9, dauer: 2.6,
        titel: "baum.zirkel.qrs.titel", auftrag: "baum.zirkel.qrs.auftrag",
        deutung: { aus: "ms", regeln: [{ wenn: "ms<=100", text: "baum.zirkel.qrs.schmal" }, { text: "baum.zirkel.qrs.breit" }] },
        fertig: ["karte:qrs", "zeit:+4"]
      },
      /* Kurzuntersuchung (Akte §3): Befundzeilen, kein Rätsel. */
      untersuchung: {
        art: "befundzeilen", titel: "baum.unters.titel", text: "baum.unters.text",
        zeilen: ["baum.unters.herz", "baum.unters.lunge", "baum.unters.neuro1", "baum.unters.neuro2"],
        fertig: ["setze:untersucht", "karte:untersuchung", "zeit:+6"]
      }
    },

    /* ------------------------------------------------------------ Raum */
    raum: {
      id: "aufnahme", titel: "Aufnahme", ersatzfarbe: "#2A3A42",
      klassen: { "baum-oben": "hat:fall_ende" },          /* Herr Baum und seine Tüte sind oben (stil.css) */
      felder: [
        { id: "marlene", name: "baum.feld.marlene", rueckfall: [16, 365, 548, 707],
          bei: [
            { wenn: "!hat:vorgestellt", tu: ["szenenbild:aufnahme_tresen>marlene.erst"] },
            { tu: ["dialog:marlene.start"] }
          ] },
        { id: "herrk", name: "baum.feld.herrk", rueckfall: [1279, 399, 1424, 737], sichtbar: "!hat:fall_ende",
          bei: [{ tu: ["dialog:herr_k.start"] }] },
        /* Klinische Reihenfolge: Anamnese (Ereignis, Medikamente), Untersuchung, dann das EKG (UMBAU §2a). */
        { id: "wagen", name: "baum.feld.wagen", rueckfall: [822, 422, 960, 738], erledigt: "karte:b-rhythmus",
          bei: [
            { wenn: "!hat:a_ereignis | !karte:b-medis | !hat:untersucht", tu: ["melde:baum.meld.erst_anamnese:warnung"] },
            { wenn: "!karte:b-rhythmus", tu: ["aufgabe:ekg"] },
            { tu: ["aufgabe:wahl"] }
          ] },
        { id: "uhr", name: "baum.feld.uhr", rueckfall: [1332, 167, 1466, 295],
          bei: [{ wenn: "minuten<420", tu: ["melde:baum.meld.uhr_frueh"] }, { tu: ["melde:baum.meld.uhr"] }] },
        { id: "pinnwand", name: "baum.feld.pinnwand", rueckfall: [284, 197, 486, 358],
          bei: [{ tu: ["melde:baum.meld.pinnwand"] }] }
      ],
      ausgaenge: [
        { name: "baum.feld.flur", nach: "monitor", zone: "ausgang", rueckfall: [1533, 228, 1600, 701],
          wenn: "hat:fall_ende",
          gesperrt: [
            { wenn: "!mind:2:b-rhythmus,b-frequenz,b-pq", tu: ["melde:baum.meld.flur_streifen:warnung"] },
            { wenn: "!hat:falk_gerufen", tu: ["melde:baum.meld.flur_marlene:warnung"] },
            { tu: ["melde:baum.meld.flur_falk:warnung"] }
          ] }
      ]
    },

    /* ------------------------------------------------------------ Stand der Schicht */
    stand: {
      titel: "baum.stand.titel",
      hat: [
        { wenn: "hat:vorgestellt", text: "baum.stand.hat.fall" },
        { wenn: "hat:a_ereignis", text: "baum.stand.hat.schilderung" },
        { wenn: "hat:fall_ende", text: "baum.stand.hat.ende" }
      ],
      offen: [
        { wenn: "!hat:vorgestellt", text: "baum.stand.offen.marlene" },
        { wenn: ["hat:vorgestellt", "!hat:a_ereignis", "!hat:fall_ende"], text: "baum.stand.offen.baum" },
        { wenn: ["hat:a_ereignis", "!pflicht", "!hat:fall_ende"], text: "baum.stand.offen.pflicht" },
        { wenn: ["hat:falk_schickt_patient", "!karte:b-medis"], text: "baum.stand.offen.falk_medis" },
        { wenn: ["hat:vorgestellt", "!hat:untersucht", "!hat:fall_ende"], text: "baum.stand.offen.untersuchung" },
        { wenn: "!hat:ekg_geschrieben", text: "baum.stand.offen.ekg" },
        { wenn: ["hat:ekg_geschrieben", "!karte:b-rhythmus"], text: "baum.stand.offen.rhythmus" },
        { wenn: ["hat:ekg_geschrieben", "!karte:b-frequenz"], text: "baum.stand.offen.frequenz" },
        { wenn: ["hat:ekg_geschrieben", "!karte:b-pq"], text: "baum.stand.offen.pq" },
        { wenn: ["hat:ekg_geschrieben", "!mind:2:b-rhythmus,b-frequenz,b-pq"], text: "baum.stand.offen.zwei" },
        { wenn: ["mind:2:b-rhythmus,b-frequenz,b-pq", "!hat:falk_gerufen"], text: "baum.stand.offen.marlene_bericht" },
        { wenn: ["hat:falk_wartet", "!hat:fall_ende", "!hat:falk_schickt_patient", "!karte:b-frequenz | !karte:b-pq"], text: "baum.stand.offen.falk_zahlen" },
        { wenn: ["hat:falk_wartet", "!hat:fall_ende", "!hat:falk_schickt_patient", "karte:b-frequenz", "karte:b-pq"], text: "baum.stand.offen.falk_wartet" },
        { wenn: ["hat:fall_ende", "raum:aufnahme"], text: "baum.stand.offen.flur" }
      ],
      fuss: [{ wenn: "!hat:vorgestellt", text: "baum.stand.fuss" }]
    },

    epilog: "auftakt.epilog"
  };
})(window);
