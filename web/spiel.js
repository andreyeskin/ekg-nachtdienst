/* „Nachtdienst" — Start, Kopfleiste, Kapitelfolge.
   Kapitel 1 (Aufnahme, 06:40) ist der Fall web/faelle/aufnahme_baum.js, gespielt vom Motor web/motor/fall.js.
   Kapitel 2 (Monitorzimmer, 09:15) liegt vorerst noch hier im alten Code (UMBAU §2c) und baut auf den
   Messungen aus Kapitel 1 auf (Z.werte, Z.befunde).
   Alle Kurven stammen aus echten Aufnahmen (LUDB), alle Zeiten aus deren Experten-Annotation.
   Erfunden sind nur die Menschen.                                                                   */
(function (global) {
  "use strict";

  var SCHLUESSEL = "nachtdienst-1";
  var FALL = "aufnahme_baum";
  var AUFNAHME_EKG = 39;          /* Herrn Baums Aufnahme — dieselbe wie im Fall (aufnahme.haupt); Kapitel 2 braucht sie an der Monitorwand */
  var LEHRSAAL_EKG = 142;         /* Jonas im Lehrsaal: Sinusrhythmus ohne Nebenbefund (docs/raeume/lehrsaal.md §4) */
  /* Kapitel 2: die beiden anderen Betten an der Monitorwand. Gewählt nach den
     Feldern rhythmus und mess in data/ekg_daten.json. Von den drei Merkmalen,
     an denen man Herrn Baum erkennen kann (P vor jedem QRS · Frequenz · PQ),
     trennen ihn Frequenz und PQ von beiden — „P vor jedem QRS" nur von einem. */
  var SCHIRM_FLIMMERN_EKG = 96;   /* "Atrial fibrillation.", mess.pq null: keine P-Welle, RR unregelmäßig,
                                     QRS schmal, mess.frequenz 90. Aufnahme 110 wäre ohne Nebendiagnose,
                                     hat aber einen großen aberranten Komplex im Fenster — verwirrt. */
  var SCHIRM_SCHNELL_EKG = 114;   /* "Sinus tachycardia.", mess.frequenz 91, mess.pq 140: P vor jedem QRS wie
                                     bei ihm, aber schneller und PQ normal. Im Text nur „Sinusrhythmus": Der
                                     Median über den Streifen liegt unter 100/min, „Tachykardie" wäre schief. */
  var KAP2_FENSTER = { von: 2.8, dauer: 6 };   /* auf allen drei Schirmen derselbe Ausschnitt */
  var SATZ = {};

  var Z = {
    raum: "aufnahme", zeit: 6 * 60 + 40, befunde: [], marken: {}, werte: {}, faelle: {}, kapitel: 1
  };

  function satz(id) { return SATZ[id]; }
  function hat(m) { return !!Z.marken[m]; }
  function setze(m) { Z.marken[m] = true; sichere(); }
  function fall(m) { return global.Fall.hat(FALL, m); }
  function zeitText(min) {
    var t = ((min === undefined ? Z.zeit : min) + 1440) % 1440;
    return ("0" + Math.floor(t / 60)).slice(-2) + ":" + ("0" + (t % 60)).slice(-2);
  }
  function zeitVor(min) { Z.zeit += min; kopfAuffrischen(); uhrStellen(); sichere(); }

  /* ------------------------------------------------------------ Speichern */
  function sichere() {
    try { global.localStorage.setItem(SCHLUESSEL, JSON.stringify(Z)); } catch (e) {}
  }
  function lade() {
    try {
      var r = global.localStorage.getItem(SCHLUESSEL);
      if (!r) return false;
      var g = JSON.parse(r);
      if (!g || !g.raum) return false;
      Z.raum = g.raum; Z.zeit = g.zeit; Z.befunde = g.befunde || [];
      Z.marken = g.marken || {}; Z.werte = g.werte || {}; Z.faelle = g.faelle || {}; Z.kapitel = g.kapitel || 1;
      return true;
    } catch (e) { return false; }
  }
  function vonVorn() {
    try { global.localStorage.removeItem(SCHLUESSEL); } catch (e) {}
    Z.raum = "aufnahme"; Z.zeit = 6 * 60 + 40; Z.befunde = []; Z.marken = {}; Z.werte = {}; Z.faelle = {}; Z.kapitel = 1;
    kopfAuffrischen(); global.Szene.zeige("aufnahme"); global.setTimeout(uhrStellen, 500);
    auftakt();
  }
  /* Für den Titelbildschirm (web/huelle.js): Gibt es einen Spielstand, und wo steht er? */
  function hatStand() {
    try {
      var g = JSON.parse(global.localStorage.getItem(SCHLUESSEL) || "null");
      return g && g.raum ? { raum: g.raum, zeit: zeitText(g.zeit), befunde: (g.befunde || []).length } : null;
    } catch (e) { return null; }
  }

  /* ------------------------------------------------------------ Anzeige: Uhr, Raum, Mappe im HUD (web/huelle.js) */
  function kopfAuffrischen() {
    if (global.Huelle) global.Huelle.anzeige({
      zeit: zeitText(), befunde: Z.befunde.length,
      ort: T((global.Szene.raum(global.Szene.aktueller()) || {}).titel || "")
    });
  }

  function uhrStellen() {
    var std = document.getElementById("uhr-std"), min = document.getElementById("uhr-min");
    if (!std || !min) return;
    var h = (Z.zeit / 60) % 12, m = Z.zeit % 60;
    var mitte = std.getAttribute("x1") + " " + std.getAttribute("y1");
    std.setAttribute("transform", "rotate(" + (h * 30) + " " + mitte + ")");
    min.setAttribute("transform", "rotate(" + (m * 6) + " " + mitte + ")");
  }

  var meldungen = null;
  function melde(text, art) {
    if (!meldungen) {
      meldungen = document.createElement("div");
      meldungen.className = "meldungen";
      document.body.appendChild(meldungen);
    }
    var d = document.createElement("div");
    d.className = "meldung" + (art ? " " + art : "");
    d.textContent = T(text);
    meldungen.appendChild(d);
    global.setTimeout(function () { d.classList.add("weg"); }, 3200);
    global.setTimeout(function () { if (d.parentNode) d.parentNode.removeChild(d); }, 3900);
  }

  /* ------------------------------------------------------------ Befunde */
  function befund(k) {
    if (global.Mappe.fuegeHinzu(k)) {
      global.Szene.aktualisiere();
      kopfAuffrischen();
    }
  }

  /* Was der Raum beim Betreten immer tut — der Fallmotor ruft es für seine Räume (Fall.start → api.betreten). */
  function betreten(raum) {
    Z.raum = raum; starteSchirme(raum); kopfAuffrischen(); uhrStellen(); sichere();
  }

  /* ------------------------------------------------------------ Dialoge, Kapitel 2 */
  var DIALOGE = {
    /* Lehrsaal, solange sein Fall fehlt (docs/UMBAU.md §2d): je ein Satz, Stimmen nach docs/raeume/lehrsaal.md §2.
       Wieser gibt eine Aufgabe statt einer Antwort; Jonas verrät nichts, er ist heute Patient. */
    wieser: {
      start: { text: "Bevor wir anfangen: Dein Zirkel liegt auf der Bank. Miss von einer R-Zacke zur nächsten.",
               endeText: "Mach ich." }
    },
    jonas: {
      start: { text: "Frag mich nichts. Heute bin ich Patient, ich lieg nur hier.", endeText: "Schon gut." }
    },
    /* Der Erzähler spricht ohne Porträt und nur an wenigen Stellen: Anfang, Kapitelwechsel, Schluss (TON.md). */
    auftakt: {
      monitor: {
        wer: "erzaehler",
        text: "09:15. Zweieinhalb Stunden später. Du hast Herrn Baum nach oben gebracht: ein Bett, ein Monitor, "
            + "drei Elektroden. Die Tochter war da und ist wieder gegangen. Jetzt hat der Oberarzt Zeit.",
        weiterBaum: "falk", weiter: "ende"
      },
      schluss: {
        wer: "erzaehler",
        text: function () {
          return T("{zeit}. Herr Baum sitzt im Bett und entschuldigt sich bei der Schwester, dass er geklingelt hat. "
                 + "Der Monitor zählt {hf}. Was vorhin war, als ihm komisch wurde, liegt irgendwo im Speicher.",
                   { zeit: zeitText(), hf: satz(AUFNAHME_EKG).mess.frequenz });
        },
        /* Danach der Epilog des Falls (Erzählung in einem späteren Dienst, KONZEPT §7) — er gehört dem Fall, nicht diesem Kapitel. */
        antworten: [{ text: "Weiter", zu: null, tu: function () {
          global.setTimeout(function () { global.Fall.epilog(FALL); }, 80);
        } }]
      }
    },

    falk: {
      /* Die Zahlen hat Dr. Falk schon unten am Tresen bekommen (Fall aufnahme_baum). Oben gibt es nur noch den Auftrag. */
      start: {
        umleiten: function () { return hat("k2_auftrag") ? "wieder" : "ende"; },
        text: ""
      },
      ende: {
        text: function () {
          /* Zweiter Satz: Monitor-EKG dient Rhythmus und Frequenz; Auffälligkeiten → 12-Kanal-EKG (FACHREGELN, Lektion 31). */
          return T("So. Jetzt wird beobachtet. Und beobachten heißt: hinschauen, nicht abwarten.") + " "
               + T("Und damit das klar ist: Der Monitor ist für Rhythmus und Frequenz da. Fällt dort etwas auf, "
                 + "schreiben wir wieder ein Zwölfkanal-EKG. Gemessen wird auf dem Papier, nicht am Schirm.");
        },
        weiter: "schirme"
      },

      /* ---------------------------------------------- Kapitel 2: Monitorzimmer */
      schirme: {
        text: "Da oben an der Wand hängen drei Betten. Eins davon ist Ihr Herr Baum. — Die Namen hab ich "
            + "ausgeblendet. Namen lesen kann jeder. Sagen Sie mir, welches Bett er ist. Und woran Sie es sehen.",
        tu: function () { setze("k2_auftrag"); global.Szene.aktualisiere(); },
        endeText: "Ich schau nach."
      },
      wieder: {
        text: function () {
          if (hat("k2_fertig")) return T("Ich bin am Speicher. — Bleiben Sie bei ihm.");
          if (hat("k2_klingel")) return T("Bett {n} klingelt. — Gehen Sie.", { n: bettVon(AUFNAHME_EKG) });
          if (hat("k2_bett")) return T("Bett {n}. Er gehört jetzt Ihnen. — Ich bin hier.", { n: bettVon(AUFNAHME_EKG) });
          return T("Und? Welches Bett?");
        },
        antworten: [
          { text: "Woran soll ich ihn erkennen?", zu: "tipp", wenn: function () { return !hat("k2_bett"); } },
          { text: "Ich schau noch.", zu: null, wenn: function () { return !hat("k2_bett"); } },
          {
            text: "Ich geh.", zu: null,
            wenn: function () { return hat("k2_klingel") && !hat("k2_fertig"); },
            tu: function () { global.setTimeout(ampelAusloesen, 300); }
          }
        ],
        endeText: "Gut."
      },
      tipp: {
        text: "An dem, was Sie heute früh gemessen haben. — Sonst an nichts.",
        endeText: "Verstanden."
      },
      k2_pq: {
        text: function () {
          return T("Die PQ-Zeit. Gut. — Langsam sind viele. Eine Überleitung, die sich so viel Zeit lässt, hat an "
                 + "dieser Wand nur er.")
               + (global.Mappe.hat("b-pq")
                  ? " " + T("Sie haben sie heute früh selbst gemessen. Darum sehen Sie sie jetzt.") : "");
        },
        weiter: "k2_wache"
      },
      k2_frequenz: {
        text: "Die Frequenz. — Stimmt. Heute. An dieser Wand ist er der einzige Langsame. Morgen hängen hier "
            + "vielleicht drei Langsame. Dann brauchen Sie die PQ-Zeit.",
        weiter: "k2_wache"
      },
      k2_wache: {
        text: function () {
          return T("Bett {n}. Ab jetzt gehört er Ihnen. — Ich bin hier.", { n: bettVon(AUFNAHME_EKG) });
        },
        endeText: "Verstanden."
      },

      /* Nach der Ampel. Keine Strafe: Jede Wahl, auch keine, endet in derselben
         Szene am Bett — nur der Weg dorthin ist ein anderer. */
      ampel_arzt: {
        text: "Gut. — Gerufen, und bei ihm geblieben. Beides. Er ist mit zwei Ohnmachten hier und wird blass. "
            + "Das will ich wissen. Sofort, nicht nachher.",
        weiter: "ampel_schluss"
      },
      ampel_beobachten: {
        text: "Ich hab die Klingel gehört. — Hinschauen ist richtig. Allein reicht es nicht. Er ist mit zwei "
            + "Ohnmachten hier und wird blass. Das sagen Sie mir. Sofort. Bleiben und rufen: Gelb, nicht Grün.",
        weiter: "ampel_schluss"
      },
      ampel_pacer: {
        text: "Ich hab die Klingel gehört. Langsam. — Er redet mit Ihnen. Seine Hände sind warm. Ob ein Pacer "
            + "nötig ist, entscheidet der Arzt am Bett, nicht der Monitor und nicht die Famulantin. Bleiben und mich rufen: "
            + "Gelb, nicht Rot.",
        weiter: "ampel_schluss"
      },
      ampel_zeit: {
        text: "Ich hab die Klingel gehört. — Zehn Sekunden sind lang, wenn man nichts tut. Er ist blass, aber "
            + "wach, und er redet. Bleiben und mich rufen: Gelb.",
        weiter: "ampel_schluss"
      },
      ampel_schluss: {
        text: function () {
          return T("Sinus, {hf} pro Minute. Vor jedem QRS ein P. Die Überleitung lang, wie heute früh. — Das ist "
                 + "jetzt. Was vorhin war, als ihm komisch wurde, zeigt der Speicher. Den schau ich mir an.",
                   { hf: satz(AUFNAHME_EKG).mess.frequenz });
        },
        weiter: "ende2"
      },
      /* Falk bleibt in der Rolle; was das Spiel über sich selbst sagt, sagt der Erzähler (auftakt.schluss).
         Pause über 3 s im Wachzustand spricht nach ESC-Synkope-2018 für eine arrhythmische Ursache (QUELLEN §3);
         vorsichtig formuliert, weil hier nur eine Präsynkope vorlag — kein „Beweis“. */
      ende2: {
        text: "Bleiben Sie bei ihm. Und wenn er wieder blass wird: nicht nachdenken, rufen. — Zeigt der Speicher von "
            + "vorhin eine Pause über drei Sekunden — und er war wach —, dann spricht sehr viel für das Herz. Zeigt er "
            + "nichts, fangen wir von vorn an.",
        antworten: [{ text: "Verstanden.", baum: "auftakt", zu: "schluss" }]
      }
    }
  };

  /* ============================================================ Kapitel 2: Monitorzimmer, 09:15
     Drei Schirme, drei echte Aufnahmen; welcher ist Herr Baum, und woran sieht
     man es? Danach klingelt sein Bett: die Ampel. Zwei Begründungen tragen
     (PQ-Zeit oder Frequenz), jede Ampel-Wahl führt weiter. Danach der Epilog des Falls. */

  /* Bettenfolge: einmal je Schicht gemischt und gespeichert, damit Herr Baum
     nicht immer auf demselben Platz liegt. */
  function betten() {
    var ids = Z.werte.betten, alle = [AUFNAHME_EKG, SCHIRM_FLIMMERN_EKG, SCHIRM_SCHNELL_EKG];
    var gueltig = ids && ids.length === alle.length &&
                  alle.every(function (id) { return ids.indexOf(id) >= 0 && SATZ[id]; });
    if (!gueltig) {
      ids = alle.slice();
      for (var i = ids.length - 1; i > 0; i--) {
        var j = Math.floor(Math.random() * (i + 1)), t = ids[i];
        ids[i] = ids[j]; ids[j] = t;
      }
      Z.werte.betten = ids;
      sichere();
    }
    return ids.map(function (id, i) { return { nr: i + 1, id: id, satz: satz(id) }; });
  }
  function bettVon(id) { return Math.max(0, betten().map(function (b) { return b.id; }).indexOf(id)) + 1; }

  /* Kleinster und größter Wert einer Strecke über alle annotierten Schläge —
     für ehrliche Vergleiche zwischen einem gemessenen Schlag und dem Median. */
  function spanne(s, von, bis, folge) {
    var sl = s.schlaege, w = [];
    for (var i = 0; i < sl.length; i++) {
      var a = sl[i][von], b = folge ? (sl[i + 1] && sl[i + 1][bis]) : sl[i][bis];
      if (a !== undefined && b !== undefined) w.push(Math.round((b - a) * 1000));
    }
    return { min: Math.min.apply(null, w), max: Math.max.apply(null, w) };
  }

  function fensterOffen() {
    return !!document.querySelector(".raetsel.an, .mappe.an");
  }

  function zentrale() {
    var B = betten();
    var nB = bettVon(AUFNAHME_EKG), nF = bettVon(SCHIRM_FLIMMERN_EKG), nS = bettVon(SCHIRM_SCHNELL_EKG);
    var mB = satz(AUFNAHME_EKG).mess, mF = satz(SCHIRM_FLIMMERN_EKG).mess, mS = satz(SCHIRM_SCHNELL_EKG).mess;

    var unter = {};
    unter[AUFNAHME_EKG] = T("Herr Baum. Sinusrhythmus, {hf}/min, langsam. Vor jedem QRS eine P-Welle, PQ {pq} ms — länger "
                          + "als ein großes Kästchen: AV-Block I. Grades.", { hf: mB.frequenz, pq: mB.pq });
    unter[SCHIRM_FLIMMERN_EKG] = T("Keine P-Wellen, die RR-Abstände springen, im Mittel etwa {hf}/min: Vorhofflimmern.",
                                   { hf: mF.frequenz });
    unter[SCHIRM_SCHNELL_EKG] = T("Sinusrhythmus, {hf}/min. Vor jedem QRS eine P-Welle, PQ {pq} ms — im Rahmen.",
                                  { hf: mS.frequenz, pq: mS.pq });
    var schirme = B.map(function (b) {
      return { name: T("Bett {n}", { n: b.nr }), satz: b.satz, von: KAP2_FENSTER.von, dauer: KAP2_FENSTER.dauer,
               unter: hat("k2_bett") ? unter[b.id] : null };
    });

    if (hat("k2_bett")) {
      global.Schirme.starte({
        titel: "Zentrale · drei Betten",
        text: "Zum Nachlesen: was auf jedem Schirm zu sehen ist.",
        schirme: schirme, hervor: nB - 1
      });
      return;
    }

    var warumBett = {};
    warumBett[AUFNAHME_EKG] = T("Bett {n} ist Herr Baum. Woran man das sieht, ist die nächste Frage.", { n: nB });
    warumBett[SCHIRM_FLIMMERN_EKG] = T("Auf Bett {n} steht vor keinem QRS eine P-Welle, und die Abstände springen — "
                                     + "Vorhofflimmern. Herr Baum hatte heute früh vor jedem QRS ein P, in gleichen "
                                     + "Abständen.", { n: nF });
    warumBett[SCHIRM_SCHNELL_EKG] = T("Auf Bett {n} steht vor jedem QRS eine P-Welle, wie bei ihm. Aber das Herz "
                                    + "schlägt {hf} pro Minute, und die PQ-Zeit ist mit {pq} ms kürzer als ein großes "
                                    + "Kästchen. Herr Baum ist langsamer, und seine Überleitung ist länger.",
                                      { n: nS, hf: mS.frequenz, pq: mS.pq });

    global.Schirme.starte({
      titel: "Zentrale · drei Betten",
      text: "Drei Schirme, drei Patienten, die Namen ausgeblendet. Ein großes Kästchen (5 mm) sind bei 25 mm/s 200 ms.",
      schirme: schirme,
      schritte: [
        {
          frage: "Welches Bett ist Herr Baum?",
          antworten: B.map(function (b) {
            return { text: T("Bett {n}", { n: b.nr }), richtig: b.id === AUFNAHME_EKG, warum: warumBett[b.id] };
          })
        },
        {
          frage: T("Woran siehst du, dass Bett {n} Herr Baum ist?", { n: nB }),
          hervor: nB - 1,
          antworten: [
            {
              merkmal: "p", text: "An den P-Wellen: Vor jedem QRS steht eine.",
              warum: T("Das stimmt für ihn und schließt Bett {f} aus, wo keine P-Welle zu finden ist. Aber Bett {s} "
                     + "hat auch vor jedem QRS eine P-Welle. Allein trennt dieses Merkmal ihn nicht von beiden.",
                       { f: nF, s: nS })
            },
            {
              merkmal: "frequenz", richtig: true, text: "An der Frequenz: Er ist der Langsamste.",
              warum: T("An dieser Wand ja: {hf} pro Minute gegen {hfs} auf Bett {s} und etwa {hff} auf Bett {f}. "
                     + "Heute reicht das. Langsam sind aber viele — was nur zu ihm gehört, ist die lange PQ-Zeit.",
                       { hf: mB.frequenz, hfs: mS.frequenz, hff: mF.frequenz, s: nS, f: nF })
            },
            {
              merkmal: "pq", richtig: true, text: "An der PQ-Zeit: länger als ein großes Kästchen.",
              warum: T("Nur auf Bett {n} braucht der Impuls vom Vorhof zur Kammer länger als 200 ms: {pq} ms, Median "
                     + "aller Schläge. Bett {s} kommt mit {pqs} ms aus, Bett {f} hat gar keine P-Welle und damit keine "
                     + "PQ-Zeit. Das ist das Merkmal, das nur er hat.",
                       { n: nB, pq: mB.pq, s: nS, pqs: mS.pq, f: nF })
            }
          ]
        }
      ],
      fertig: function (g) { bettGefunden(g[1].merkmal); }
    });
  }

  function bettGefunden(merkmal) {
    var s = satz(AUFNAHME_EKG), m = s.mess, n = bettVon(AUFNAHME_EKG);
    var pq = spanne(s, "p0", "q0"), rr = spanne(s, "r", "r", true);
    setze("k2_bett");
    Z.werte.merkmal = merkmal;
    zeitVor(7);
    befund({
      id: "b-monitor", titel: T("Monitor: Bett {n}", { n: n }), zeit: zeitText(),
      text: T("Herr Baum am Monitor: Sinusrhythmus, {hf}/min, langsam. Vor jedem QRS eine P-Welle, PQ {pq} ms — länger als "
            + "ein großes Kästchen. Monitorwerte sind der Median aller Schläge im Streifen.", { hf: m.frequenz, pq: m.pq })
          + " " + (merkmal === "pq"
                   ? T("Erkannt an der PQ-Zeit: Die hat an der Wand nur er.")
                   : T("Erkannt an der Frequenz: heute der einzige Langsame an der Wand.")),
      ekg: { satz: AUFNAHME_EKG, mmProS: 25, von: 3.0, dauer: 5 },
      vergleich: {
        "b-pq": T("Heute früh am Wagen, jetzt am Monitor: dieselbe lange Überleitung, und jede P-Welle kommt durch. "
                + "Nicht schlechter, nicht besser. Dein Wert von heute früh stammt aus einem Schlag; über alle Schläge "
                + "liegt die PQ-Zeit zwischen {min} und {max} ms. Das ist Messung, keine Veränderung.",
                  { min: pq.min, max: pq.max }),
        "b-frequenz": T("Dieselbe Frequenz wie am Morgen: langsam, aber gleichmäßig. Dein Wert kommt aus einem "
                      + "RR-Abstand; im ganzen Streifen liegen die RR-Abstände zwischen {min} und {max} ms.",
                        { min: rr.min, max: rr.max }),
        "b-rhythmus": T("Morgens wie jetzt: vor jedem QRS eine P-Welle, gleiche Abstände. Der Sinusknoten gibt den "
                      + "Takt."),
        "b-medis": T("Der Betablocker kann beides mit erklären, was der Monitor zeigt: den langsamen Takt und die lange "
                   + "Überleitung. Die Ohnmachten erklärt er allein nicht.")
      }
    });
    global.Dialog.starte("falk", merkmal === "pq" ? "k2_pq" : "k2_frequenz", function () {
      global.setTimeout(ampelAusloesen, 1800);
    });
  }

  /* Die Ampel. Ausgelöst einmal nach dem Fund; wer „Zurück" tippt, findet sie
     wieder am großen Monitor, an der Wand, bei Dr. Falk oder beim nächsten
     Betreten des Raums. Keine Sackgasse. */
  function ampelAusloesen() {
    if (!hat("k2_bett") || hat("k2_fertig")) return;
    if (!hat("k2_klingel")) { setze("k2_klingel"); zeitVor(11); }
    if (global.Szene.aktueller() !== "monitor" || global.Dialog.laeuft() || fensterOffen()) return;
    var s = satz(AUFNAHME_EKG), n = bettVon(AUFNAHME_EKG);
    global.Ampel.starte({
      titel: T("Bett {n} klingelt", { n: n }),
      lage: T("Ein paar Minuten später klingelt Bett {n}. Du bist als Erste bei ihm. Herr Baum sitzt auf der "
            + "Bettkante, er wollte aufstehen. Er ist blass. „Mir war gerade ganz komisch. Jetzt geht's schon wieder. "
            + "Entschuldigung.“ Er ist wach, antwortet in ganzen Sätzen, seine Hände sind warm. Der Monitor über dem "
            + "Bett zählt {hf} pro Minute.", { n: n, hf: s.mess.frequenz })
          + (fall("foto_gefragt") ? " " + T("Auf dem Nachtkästchen steht das Foto von Lena.") : ""),
      frage: "Was tust du?",
      ekg: { satz: s, name: T("Bett {n} · Herr Baum", { n: n }), von: KAP2_FENSTER.von, dauer: 5 },
      sekunden: 10,
      wahl: [
        { id: "beobachten", farbe: "gruen", ampel: "Grün", text: "Beobachten",
          wie: "Bei ihm bleiben, den Monitor im Blick. Niemanden rufen." },
        { id: "arzt", farbe: "gelb", ampel: "Gelb", text: "Arzt rufen",
          wie: "Bei ihm bleiben und Dr. Falk rufen." },
        { id: "pacer", farbe: "rot", ampel: "Rot", text: "Pacer vorbereiten",
          wie: "Elektroden für den externen Schrittmacher kleben." }
      ],
      danach: "Dr. Falk kommt.",
      fertig: ampelSzene,
      abbruch: function () { melde(T("Bett {n} klingelt noch.", { n: n }), "warnung"); }
    });
  }

  function ampelSzene(id) {
    var wahl = id || "zeit";
    Z.werte.ampel = wahl;
    setze("k2_fertig");
    zeitVor(4);
    global.Dialog.starte("falk", "ampel_" + wahl);
  }

  /* Vor Falks Auftrag gibt es an der Wand nichts zu raten: Er hat die Namen noch nicht ausgeblendet. */
  function vorAuftrag() {
    if (hat("k2_auftrag")) return false;
    melde("Erst Dr. Falk. Er wartet auf Zahlen.");
    return true;
  }

  function grosserMonitor() {
    if (vorAuftrag()) return;
    if (hat("k2_klingel") && !hat("k2_fertig")) { ampelAusloesen(); return; }
    if (hat("k2_bett")) {
      melde(T("Bett {n} · Herr Baum. Sinusrhythmus, {hf}/min, langsam, vor jedem QRS eine P-Welle.",
              { n: bettVon(AUFNAHME_EKG), hf: satz(AUFNAHME_EKG).mess.frequenz }));
      return;
    }
    zentrale();
  }

  function monitorwand() {
    if (vorAuftrag()) return;
    if (hat("k2_klingel") && !hat("k2_fertig")) { ampelAusloesen(); return; }
    zentrale();
  }

  /* ------------------------------------------------------------ Stand der Schicht */
  function kapitelStand() {
    /* Kapitel 1 kommt aus den Daten des Falls (web/faelle/aufnahme_baum.js, stand); hier nur Kapitel 2. */
    var k = global.Fall.stand(FALL), hatL = k.hat, offen = k.offen;

    if (Z.marken.ankunft_monitor && !Z.marken.k2_auftrag) offen.push("Dr. Falk steht im Monitorzimmer.");
    /* Kapitel 2 — nennt das Ziel, nie die Lösung: kein Bett, kein Merkmal, bevor
       der Spieler es selbst gefunden hat. */
    if (Z.marken.k2_fertig) {
      hatL.push(T("Bett {n} hat geklingelt: Herr Baum war blass. Dr. Falk sieht sich den Speicher an.",
                  { n: bettVon(AUFNAHME_EKG) }));
    }
    if (Z.marken.k2_auftrag && !Z.marken.k2_bett) {
      offen.push("Dr. Falk will wissen, welcher der drei Schirme an der Wand Herrn Baum gehört — und woran du es siehst.");
    }
    if (Z.marken.k2_klingel && !Z.marken.k2_fertig) {
      offen.push(T("Bett {n} hat geklingelt. Herr Baum wartet.", { n: bettVon(AUFNAHME_EKG) }));
    }

    var fuss = k.fuss || "";
    if (Z.marken.k2_fertig) {
      fuss = T("Der Epilog erzählt, was aus Herrn Baum wurde. Damit endet, was bisher gebaut ist.");
    }
    return {
      zeit: zeitText(), titel: Z.kapitel === 1 ? k.titel : "Kapitel 2 · Monitorzimmer",
      ort: (global.Szene.raum(global.Szene.aktueller()) || {}).titel || "",
      hat: hatL, offen: offen, fuss: fuss
    };
  }

  /* ------------------------------------------------------------ Räume */
  /* Klickfelder kommen aus den Klickzonen der gerenderten Szene (art/szenen/<raum>/hitboxes.json, über
     gen/kunst.py in kunst.szenen.<raum>.zonen) — so stimmen Bild und Feld nach jedem Render überein.
     Die Zahlen hier sind nur der Rückfall, falls eine Zone fehlt. */
  var KUNST = null;
  function zone(raum, id, rueckfall) {
    var z = KUNST && KUNST.szenen[raum] && KUNST.szenen[raum].zonen && KUNST.szenen[raum].zonen[id];
    if (!z) z = rueckfall;
    return [[z[0], z[1]], [z[2], z[1]], [z[2], z[3]], [z[0], z[3]]];
  }

  function baueRaeume(kunst) {
    KUNST = kunst;
    /* Die Aufnahme registriert der Fall (Fall.lade). Hier nur das Monitorzimmer (Kapitel 2, alter Code). */
    global.Szene.registriere("monitor", {
      titel: "Monitorzimmer", ebenen: kunst.szenen.monitor, ersatzfarbe: "#1C2A31",
      beiBetreten: function () {
        Z.kapitel = 2;
        if (!hat("ankunft_monitor")) { Z.zeit = Math.max(Z.zeit, 9 * 60 + 15); setze("ankunft_monitor"); }
        betreten("monitor");
        global.setTimeout(function () {
          if (global.Szene.aktueller() !== "monitor") return;
          if (!hat("k2_auftrag")) {
            /* Beim ersten Mal der Erzähler, dann Dr. Falk mit dem Auftrag; die Zahlen hat er schon unten bekommen. */
            global.Dialog.starte("auftakt", "monitor");
          } else if (hat("k2_bett") && !hat("k2_fertig")) {
            ampelAusloesen();                       /* Kapitel 2: Bett klingelt (wieder) */
          }
        }, 1400);
      },
      felder: [
        /* --- Kapitel 2: neue Felder --- */
        {
          id: "wand", name: "Monitorwand · drei Betten",
          punkte: zone("monitor", "schirme_klein", [500, 104, 1384, 352]),
          erledigt: function () { return hat("k2_bett"); },
          bei: function () { monitorwand(); }
        },
        /* --- Ende Kapitel 2: neue Felder --- */
        {
          id: "schirm", name: "Großer Monitor",
          punkte: zone("monitor", "schirm", [638, 308, 955, 498]),
          bei: function () {
            grosserMonitor();
          }
        },
        {
          id: "falk", name: "Dr. Falk",
          punkte: zone("monitor", "falk", [1159, 341, 1299, 717]),
          bei: function () { global.Dialog.starte("falk", "start"); }
        }
      ],
      ausgaenge: [
        {
          name: "Zurück in die Aufnahme", nach: "aufnahme",
          punkte: zone("monitor", "ausgang", [0, 286, 132, 656])
        }
      ]
    });

    /* Lehrsaal (Einschulungstag): gerendert im Haus (gen/blender/haus_blockout.py ebenen lehrsaal). Der Fall fehlt noch;
       erreichbar über das Menü (web/huelle.js), der Ausgang führt in die Aufnahme. Die eigene Bank öffnet den Zirkel an
       Jonas' Ableitung II, das Whiteboard „Reizleitung bauen" (Wunsch des Nutzers 26.10.2026). */
    global.Szene.registriere("lehrsaal", {
      titel: "Lehrsaal", ebenen: kunst.szenen.lehrsaal, ersatzfarbe: "#F6E8CF",
      beiBetreten: function () { betreten("lehrsaal"); },
      felder: [
        { id: "bank", name: T("Deine Bank · Zirkel"), punkte: zone("lehrsaal", "bank", [298, 741, 990, 900]),
          erledigt: function () { return hat("ls_zirkel"); },
          bei: function () {
            global.Zirkel.starte({ satz: satz(LEHRSAAL_EKG), was: "rr", auftrag: "Miss den RR-Abstand.",
              fertig: function (erg) {
                setze("ls_zirkel"); global.Szene.aktualisiere();
                melde(T("Gemessen: {ms} ms von R zu R.", { ms: erg.wahrheit }));
              } });
          } },
        { id: "whiteboard", name: T("Whiteboard"), punkte: zone("lehrsaal", "whiteboard", [1348, 154, 1549, 390]),
          bei: function () { global.Reizleitung.starte({ satz: satz }); } },
        /* Die Leinwand vor Dr. Wieser: das spätere Feld liegt oben, wer auf Wieser klickt, trifft sie; der Rest ist Leinwand. */
        { id: "projektion", name: T("Leinwand"), punkte: zone("lehrsaal", "projektion", [602, 131, 969, 360]),
          bei: function () { melde("Auf der Leinwand läuft dieselbe Ableitung, groß wie auf Papier."); } },
        { id: "wieser", name: T("Dr. Wieser"), punkte: zone("lehrsaal", "wieser", [637, 208, 815, 592]),
          bei: function () { global.Dialog.starte("wieser", "start"); } },
        { id: "jonas", name: T("Jonas"), punkte: zone("lehrsaal", "jonas", [330, 330, 600, 420]),
          sichtbar: function () { return !!(KUNST.szenen.lehrsaal.zonen || {}).jonas; },   /* erst mit seiner Figur */
          bei: function () { global.Dialog.starte("jonas", "start"); } },
        { id: "liege", name: T("Liege"), punkte: zone("lehrsaal", "liege", [263, 420, 642, 554]),
          bei: function () { melde("Die Klemmen an Armen und Beinen sitzen. Die Brustwand ist noch frei."); } },
        { id: "wagen", name: T("EKG-Wagen"), punkte: zone("lehrsaal", "wagen", [45, 295, 232, 584]),
          bei: function () {
            melde(T("Der Wagen schreibt Jonas' Ableitung II mit: {hf} pro Minute.", { hf: satz(LEHRSAAL_EKG).mess.frequenz }));
          } },
        { id: "lineale", name: T("Lineale"), punkte: zone("lehrsaal", "lineale", [1071, 402, 1151, 452]),
          erledigt: function () { return hat("ls_lineal"); },
          bei: function () {
            if (hat("ls_lineal")) { melde("Dein Lineal steckt schon in der Kitteltasche."); return; }
            setze("ls_lineal"); global.Szene.aktualisiere();
            melde("Du nimmst ein blaues Lineal aus der Schachtel.");
          } },
        { id: "uhr", name: T("Uhr"), punkte: zone("lehrsaal", "uhr", [753, 28, 817, 93]),
          bei: function () { melde(T("Es ist {zeit}.", { zeit: zeitText() })); } }
      ],
      ausgaenge: [
        { name: T("Zurück in die Aufnahme"), nach: "aufnahme", punkte: zone("lehrsaal", "ausgang", [1536, 600, 1600, 880]) }
      ]
    });
  }

  /* Bildschirme im Raum: jede Fläche aus art/szenen/<raum>/schirme.json (kunst.szenen.<raum>.schirme) bekommt
     eine Leinwand in ihrer eigenen Ebene (sie wandert mit der Parallaxe mit), darauf läuft eine echte Aufnahme
     aus data/ — nie ins Bild gemalt (ART_BIBLE §6). Nur der aktuelle Raum läuft; beim Wechsel wird gestoppt.
       wagen_schirm  EKG-Wagen der Aufnahme: Herrn Baums Ableitung II, Frequenz aus den Daten
       gross         großer Schirm der Zentrale: wie Papier (Entscheidung 10.10.2026), Herr Baum
       bett_1..3     Bettmonitore: dieselben drei Aufnahmen wie im Rätsel „Drei Schirme“, in Bettenfolge
     Marlenes Verwaltungs-PC hat keine Fläche: er zeigt kein EKG. */
  var schirmLauf = [];
  function stoppeSchirme() {
    schirmLauf.forEach(function (s) { s.streifen.stoppeLauf(); if (s.el.parentNode) s.el.parentNode.removeChild(s.el); });
    schirmLauf = [];
  }
  function schirmAufnahme(name, raum) {
    if (raum === "lehrsaal") return name === "whiteboard" ? null : satz(LEHRSAAL_EKG);   /* Whiteboard: nur Zeichnungen */
    if (name === "wagen_schirm" || name === "gross") return satz(AUFNAHME_EKG);
    var m = /^bett_(\d)$/.exec(name);
    if (m) { var b = betten()[+m[1] - 1]; return b ? b.satz : null; }
    return null;
  }
  function starteSchirme(raum) {
    stoppeSchirme();
    var liste = KUNST && KUNST.szenen[raum] && KUNST.szenen[raum].schirme;
    if (!liste) return;
    var buehne = document.getElementById("buehne");
    Object.keys(liste).forEach(function (name) {
      var f = liste[name], s = schirmAufnahme(name, raum);
      if (!s) return;
      var ebene = buehne.querySelector(".ebene-" + (f.ebene || "hintergrund"));
      if (!ebene) return;
      var k = f.kasten, b = k[2] - k[0], h = k[3] - k[1];
      var d = document.createElement("div");
      d.className = "schirm-lauf"; d.setAttribute("data-schirm", name); d.setAttribute("data-satz", String(s.id));
      d.style.left = (k[0] / 16).toFixed(3) + "%"; d.style.top = (k[1] / 9).toFixed(3) + "%";
      d.style.width = (b / 16).toFixed(3) + "%"; d.style.height = (h / 9).toFixed(3) + "%";
      if (f.ecken && f.ecken.length === 4) {         /* schräge Fläche: Leinwand auf die vier Ecken beschneiden */
        d.style.clipPath = "polygon(" + f.ecken.map(function (e) {
          return ((e[0] - k[0]) / b * 100).toFixed(2) + "% " + ((e[1] - k[1]) / h * 100).toFixed(2) + "%";
        }).join(", ") + ")";
      }
      d.innerHTML = "<canvas></canvas>";
      ebene.appendChild(d);
      var gross = name === "gross" || name === "projektion";      /* Leinwand im Lehrsaal: wie Papier */
      var streifen = global.EKG.Streifen(d.querySelector("canvas"), {
        werte: s.sig.werte, fs: s.sig.fs, mmProS: 25, dauer: gross ? 5.2 : 4.0,
        monitor: true, kalibrierung: false, stil: gross ? null : "phosphor",
        anzeige: gross ? null : { links: (s.sig.lead || "II").toUpperCase(), rechts: String(s.mess.frequenz) }
      });
      schirmLauf.push({ name: name, el: d, streifen: streifen, satz: s.id });
      global.requestAnimationFrame(function () { streifen.zeichne(); streifen.starteLauf(1); });
    });
  }
  function schirmeStand() {
    return schirmLauf.map(function (s) { return { name: s.name, satz: s.satz, laeuft: s.streifen.laeuftGerade() }; });
  }

  /* ------------------------------------------------------------ Start
     Aufgerufen vom Titelbildschirm (web/huelle.js): „Weiterspielen" lädt den Spielstand,
     „Neues Spiel" (opt.neu) beginnt die Schicht von vorn. */
  function start(kunst, ekgDaten, opt) {
    ekgDaten.forEach(function (r) { SATZ[r.id] = r; });
    global.Szene.start(document.getElementById("buehne"));
    global.Mappe.start(Z, satz);
    global.Stand.start(Z, kapitelStand);
    global.Fenster.start({ satz: satz });
    global.Szenenbild.lade(kunst.szenenbilder);
    KUNST = kunst;
    /* Der Fallmotor bekommt, was jeder Fall braucht — und kennt keinen Patienten. */
    global.Fall.start({
      Z: Z, satz: satz, befund: befund, melde: melde, zeitVor: zeitVor, zeitText: zeitText,
      zone: zone, kunst: kunst, betreten: betreten, sichere: sichere, kopf: kopfAuffrischen
    });
    global.Fall.lade(global.FAELLE[FALL]);
    var baeume = {}, k;
    for (k in global.Fall.baeume()) baeume[k] = global.Fall.baeume()[k];
    for (k in DIALOGE) baeume[k] = DIALOGE[k];
    global.Dialog.lade({
      baeume: baeume, portraits: kunst.portraits,
      namen: { marlene: "Schwester Marlene", herr_k: "Herr Baum", falk: "Oberarzt Dr. Falk", erzaehler: "",
               wieser: "Dr. Wieser", jonas: "Jonas" }
    });
    baueRaeume(kunst);

    /* HUD-Knöpfe und Menü (auch „Neues Spiel") gehören der Hülle, web/huelle.js. */
    document.addEventListener("keydown", function (e) {
      if (e.key === "h" && !global.Dialog.laeuft()) global.Szene.zeigeFelder(2400);
      if (e.key === "s" && !global.Dialog.laeuft()) global.Stand.oeffne();
    });

    var fortsetzung = !(opt && opt.neu) && lade();
    global.Szene.zeige(Z.raum || "aufnahme", true);
    kopfAuffrischen();
    global.setTimeout(uhrStellen, 120);

    if (!fortsetzung) auftakt();
  }

  /* Der Auftakt gehört dem Fall (Erzähler); danach leuchten die Felder einmal auf. */
  function auftakt() {
    global.setTimeout(function () { global.Fall.wirke(FALL, "dialog:auftakt.start"); }, 700);
  }

  /* Sprachwechsel: der Zustand liegt im Speicher, also ist Neuladen der
     sauberste Weg — alle Oberflächen werden neu und richtig aufgebaut. */
  function neuZeichnen() {
    sichere();
    try { global.location.reload(); } catch (e) {}
  }

  global.Spiel = {
    start: start, melde: melde, neuZeichnen: neuZeichnen, sichere: sichere, zaehlerAuffrischen: kopfAuffrischen,
    zustand: Z, satz: satz, hat: hat, vonVorn: vonVorn, hatStand: hatStand,
    FALL: FALL, fall: fall,
    __dialoge: DIALOGE,
    __betten: betten, __zentrale: zentrale, __ampel: ampelAusloesen, __schirme: schirmeStand,
    KAPITEL2_EKG: { baum: AUFNAHME_EKG, flimmern: SCHIRM_FLIMMERN_EKG, schnell: SCHIRM_SCHNELL_EKG }
  };
})(window);
