/* „Nachtdienst" — Kapitel 1: Aufnahme, 06:40.
   Fall: Herr Konrad Baum, 68, zwei Synkopen ohne Vorwarnung.
   Alle Kurven stammen aus echten Aufnahmen (LUDB), alle Zeiten aus deren
   Experten-Annotation. Erfunden sind nur die Menschen.                        */
(function (global) {
  "use strict";

  var SCHLUESSEL = "nachtdienst-1";
  var AUFNAHME_EKG = 39;          /* Sinusbradykardie, PQ 228 ms — AV-Block I° */
  var SATZ = {};

  var Z = {
    raum: "aufnahme", zeit: 6 * 60 + 40, befunde: [], marken: {}, werte: {}, kapitel: 1
  };

  function satz(id) { return SATZ[id]; }
  function hat(m) { return !!Z.marken[m]; }
  function setze(m) { Z.marken[m] = true; sichere(); }
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
      Z.marken = g.marken || {}; Z.werte = g.werte || {}; Z.kapitel = g.kapitel || 1;
      return true;
    } catch (e) { return false; }
  }
  function vonVorn() {
    try { global.localStorage.removeItem(SCHLUESSEL); } catch (e) {}
    Z.raum = "aufnahme"; Z.zeit = 6 * 60 + 40; Z.befunde = []; Z.marken = {}; Z.werte = {}; Z.kapitel = 1;
    kopfAuffrischen(); global.Szene.zeige("aufnahme"); global.setTimeout(uhrStellen, 500);
  }

  /* ------------------------------------------------------------ Kopfleiste */
  function kopfAuffrischen() {
    var u = document.getElementById("kopf-zeit");
    if (u) u.textContent = zeitText();
    var m = document.getElementById("kopf-mappe");
    if (m) {
      m.textContent = T("Befundmappe") + " · " + Z.befunde.length;
      m.classList.toggle("voll", Z.befunde.length > 0);
    }
    var o = document.getElementById("kopf-ort");
    if (o) o.textContent = T((global.Szene.raum(global.Szene.aktueller()) || {}).titel || "");
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

  /* ------------------------------------------------------------ Kleine Frage */
  function frage(opt) {
    var hof = document.getElementById("frage-hof");
    if (!hof) {
      hof = document.createElement("div");
      hof.id = "frage-hof"; hof.className = "raetsel frage";
      hof.innerHTML = '<div class="raetsel-innen"><div class="raetsel-kopf"><h2></h2>' +
        '<button class="knopf zu" type="button">' + T("Zurück") + '</button></div>' +
        '<p class="raetsel-auftrag"></p><div class="frage-bild"></div>' +
        '<div class="frage-wahl"></div><div class="rueck"></div></div>';
      document.body.appendChild(hof);
      hof.querySelector(".zu").addEventListener("click", function () {
        hof.classList.remove("an"); global.Szene.sperre(false); global.Szene.aktualisiere();
      });
    }
    hof.querySelector("h2").textContent = T(opt.titel);
    hof.querySelector(".raetsel-auftrag").textContent = T(opt.text);
    var bild = hof.querySelector(".frage-bild");
    bild.innerHTML = opt.ekg ? '<canvas height="172" style="width:100%"></canvas>' : "";
    var rueck = hof.querySelector(".rueck");
    rueck.className = "rueck"; rueck.innerHTML = "";
    var wahl = hof.querySelector(".frage-wahl");
    wahl.innerHTML = "";
    opt.antworten.forEach(function (a, i) {
      var b = document.createElement("button");
      b.className = "knopf wahl"; b.type = "button"; b.textContent = T(a.text);
      b.addEventListener("click", function () {
        Array.prototype.forEach.call(wahl.children, function (c) { c.disabled = true; });
        b.classList.add(a.richtig ? "richtig" : "falsch");
        rueck.className = "rueck " + (a.richtig ? "gut" : "fast");
        rueck.innerHTML = "<strong>" + T(a.richtig ? "Richtig." : "Nicht ganz.") + "</strong> " + T(a.warum);
        if (a.richtig) {
          global.setTimeout(function () {
            hof.classList.remove("an"); global.Szene.sperre(false);
            if (opt.fertig) opt.fertig();
          }, 2600);
        } else {
          global.setTimeout(function () {
            Array.prototype.forEach.call(wahl.children, function (c) {
              c.disabled = false; c.classList.remove("falsch");
            });
          }, 2200);
        }
      });
      wahl.appendChild(b);
    });
    hof.classList.add("an");
    global.Szene.sperre(true);
    if (opt.ekg) {
      var lw = bild.querySelector("canvas");
      var s = global.EKG.Streifen(lw, {
        werte: satz(opt.ekg.satz).sig.werte, fs: satz(opt.ekg.satz).sig.fs,
        mmProS: opt.ekg.mmProS || 25, von: opt.ekg.von || 0, dauer: opt.ekg.dauer || 6
      });
      global.requestAnimationFrame(s.zeichne);
      global.setTimeout(s.zeichne, 80);
    }
  }

  /* ------------------------------------------------------------ Befunde */
  function befund(k) {
    if (global.Mappe.fuegeHinzu(k)) {
      global.Szene.aktualisiere();
      kopfAuffrischen();
    }
  }

  function anzahlKernbefunde() {
    var n = 0;
    ["b-rhythmus", "b-frequenz", "b-pq"].forEach(function (id) { if (global.Mappe.hat(id)) n++; });
    return n;
  }

  /* ------------------------------------------------------------ Dialoge */
  var DIALOGE = {
    auftakt: {
      start: {
        wer: "marlene",
        text: "06:40. Dein erster Dienst allein auf der Aufnahme. Draußen wird es hell, drinnen riecht es nach "
            + "Kaffee und Desinfektion. Am Tresen steht Marlene. Auf dem Stuhl sitzt ein alter Herr mit "
            + "Schiebermütze und einer Plastiktüte.",
        weiter: "zwei"
      },
      zwei: {
        wer: "marlene",
        text: "Tipp dir an, was dich interessiert. Oben rechts liegt deine Befundmappe — dort hinein kommt, was du "
            + "selbst gemessen hast. Nicht, was du vermutest.",
        endeText: "Los."
      }
    },

    marlene: {
      start: {
        text: function () {
          return hat("vorgestellt")
            ? T("Na, schon schlauer?")
            : T("Du bist die Famulantin. Gut. Dann fang gleich an — der Herr dort sitzt seit zwanzig Minuten und "
              + "entschuldigt sich alle fünf Minuten dafür, dass er da ist.");
        },
        tu: function () { setze("vorgestellt"); },
        antworten: [
          { text: "Was ist passiert?", zu: "fall" },
          { text: "Was soll ich tun?", zu: "auftrag" },
          { text: "Was hältst du davon?", zu: "meinung", wenn: function () { return hat("fall_gehoert"); } },
          {
            text: function () { return T("Ich hab die PQ-Zeit gemessen: {pq} ms.", { pq: Z.werte.pq }); },
            zu: "pq", wenn: function () { return global.Mappe.hat("b-pq"); }
          },
          { text: "Später.", zu: null }
        ]
      },
      fall: {
        text: "Konrad Baum, 68. Zweimal umgekippt. Einmal vorgestern an der Bushaltestelle, einmal heute früh in "
            + "der Küche. Beide Male im Stehen, beide Male ohne Vorwarnung.",
        tu: function () { setze("fall_gehoert"); },
        antworten: [
          { text: "Ohne Vorwarnung — ist das wichtig?", zu: "vorwarnung" },
          { text: "Hat er sich verletzt?", zu: "verletzt" },
          { text: "Zurück.", zu: "start" }
        ]
      },
      vorwarnung: {
        text: "Das ist das Einzige, was mich an der Sache stört. Wem erst schwarz vor Augen wird, wer schwitzt und "
            + "sich noch hinsetzen kann — das ist der gewöhnliche Weg, und der spricht für eine Kreislaufsache. "
            + "Hier fehlt genau das. Es steht in jeder Liste der Warnzeichen. Ein Beweis ist es nicht, aber es "
            + "heißt: nicht nach Hause schicken, bevor man nachgesehen hat.",
        antworten: [
          { text: "Also nachsehen.", zu: "auftrag" },
          { text: "Beweist das etwas?", zu: "beweis" },
          { text: "Zurück.", zu: "start" }
        ]
      },
      beweis: {
        text: "Nichts beweist es. Beweisen würde: ein Puls dauerhaft unter vierzig, eine Pause über drei Sekunden "
            + "im Wachen, oder ein Block, bei dem Schläge ausfallen. Das steht alles noch nicht auf dem Papier. "
            + "Deswegen schreibst du jetzt eines.",
        antworten: [{ text: "Verstanden.", zu: "auftrag" }]
      },
      verletzt: {
        text: "Eine Schramme am Ellbogen, sonst nichts. Er sagt, er hat sich am Regal festgehalten. Beim zweiten Mal "
            + "war er allein. Das ist der Teil, der mir nicht gefällt.",
        antworten: [{ text: "Zurück.", zu: "start" }]
      },
      auftrag: {
        text: "Schreib ihm ein EKG. Der Wagen steht da drüben, die Elektroden kleben schon. Den Puls hab ich "
            + "gefühlt — langsam. Aber „langsam“ ist keine Zahl, und von einem Gefühl schreibt man keinen Befund.",
        tu: function () { setze("auftrag_ekg"); global.Szene.aktualisiere(); },
        antworten: [{ text: "Mach ich.", zu: null }]
      },
      meinung: {
        text: "Ich bin seit zwanzig Jahren hier und sag trotzdem nichts, bevor ich einen Streifen gesehen habe. "
            + "Sonst suchst du nachher nur noch das, was ich dir in den Kopf gesetzt hab.",
        antworten: [{ text: "Fair.", zu: "start" }]
      },
      pq: {
        text: function () {
          return T("Über zweihundert. Dann leitet er über — aber er lässt sich Zeit dabei. Das allein lässt keinen "
                 + "umfallen. Aber eine Leitung, die heute {pq} Millisekunden braucht, kann morgen stehenbleiben. "
                 + "Und genau dafür gibt es den Monitor. Geh rüber, ich meld dich an.", { pq: Z.werte.pq });
        },
        tu: function () { setze("monitor_frei"); global.Szene.aktualisiere(); },
        antworten: [{ text: "Danke, Marlene.", zu: null }]
      }
    },

    herr_k: {
      start: {
        text: function () {
          return hat("k_begruesst")
            ? T("Ja, Frau Doktor?")
            : T("Entschuldigen Sie. Ich wollte eigentlich gar nicht herkommen. Meine Tochter hat gesagt, ich soll. "
              + "Da war ich dann halt brav.");
        },
        tu: function () { setze("k_begruesst"); },
        antworten: [
          { text: "Erzählen Sie mir, was passiert ist.", zu: "was" },
          { text: "Hatten Sie Schmerzen in der Brust?", zu: "schmerz" },
          { text: "Nehmen Sie Medikamente?", zu: "medis" },
          { text: "Wer ist auf dem Foto?", zu: "foto", wenn: function () { return hat("tuete_gesehen"); } },
          { text: "Ich komme gleich wieder.", zu: null }
        ]
      },
      was: {
        text: "Ich stand an der Haltestelle. Und dann stand ich nicht mehr. Dazwischen — nichts. Kein Schwindel, "
            + "kein Herzklopfen, gar nichts. Als hätte jemand das Licht ausgemacht und gleich wieder an.",
        tu: function () { setze("k_anamnese"); },
        antworten: [
          { text: "Wie lange waren Sie weg?", zu: "dauer" },
          { text: "Und heute früh?", zu: "heute" },
          { text: "Zurück.", zu: "start" }
        ]
      },
      dauer: {
        text: "Die Frau neben mir sagt, eine halbe Minute vielleicht. Sie hat sich mehr erschreckt als ich. "
            + "Ich bin aufgestanden und hab mich entschuldigt.",
        antworten: [{ text: "Zurück.", zu: "start" }]
      },
      heute: {
        text: "In der Küche. Beim Wasserkocher. Aufgewacht bin ich auf den Fliesen, der Kocher lief noch. "
            + "Das Komische ist: hinterher war mir sofort wieder gut. Ich hätte frühstücken können.",
        antworten: [{ text: "Zurück.", zu: "start" }]
      },
      schmerz: {
        text: "Nein. Nie. Ich geh jeden Tag mit dem Hund, zweimal um den Block, das geht alles. "
            + "Nur langsamer als früher, aber das ist das Alter.",
        antworten: [{ text: "Zurück.", zu: "start" }]
      },
      medis: {
        text: "Die Tochter hat alles eingepackt. Die Tüte da. Ich kann Ihnen die Namen nicht sagen, "
            + "ich kenn sie nach der Farbe.",
        tu: function () { setze("k_zeigt_tuete"); global.Szene.aktualisiere(); },
        antworten: [{ text: "Darf ich reinschauen?", zu: null, tu: function () { setze("darf_tuete"); } }]
      },
      foto: {
        text: "Das ist die Lena. Die hat mir das Bändchen da geknüpft, als sie sechs war. Jetzt ist sie elf und "
            + "findet es peinlich. Ich trag's trotzdem.",
        antworten: [{ text: "Schön.", zu: "start" }]
      }
    },

    falk: {
      start: {
        text: "Sie sind die Neue. Falk. — Bevor Sie etwas sagen: Ich will nicht hören, was Sie vermuten. "
            + "Ich will hören, was Sie gemessen haben.",
        antworten: [
          {
            text: function () {
              return T("Sinusbradykardie, {hf} pro Minute, PQ {pq} Millisekunden.",
                       { hf: Z.werte.hf, pq: Z.werte.pq });
            },
            wenn: function () { return global.Mappe.hat("b-pq") && global.Mappe.hat("b-frequenz"); },
            zu: "gut"
          },
          {
            text: function () { return T("Der Puls ist langsam, etwa {hf} pro Minute.", { hf: Z.werte.hf }); },
            wenn: function () { return global.Mappe.hat("b-frequenz"); },
            zu: "halb"
          },
          { text: "Er ist zweimal ohne Vorwarnung umgekippt.", zu: "anamnese" }
        ]
      },
      gut: {
        text: "Gut. Zwei Zahlen, kein Roman. — Also: Der Knoten ist langsam, die Überleitung ist lang, und er "
            + "nimmt etwas, das beides macht. Das erklärt die Zahlen. Es erklärt nicht, warum er umfällt. "
            + "Was es sagt, ist: Die Leitung ist angeschlagen. Und eine angeschlagene Leitung fällt nicht "
            + "gleichmäßig aus, sie fällt plötzlich aus. Beweisen würde das erst eine Pause oder ein Block, "
            + "bei dem Schläge ausfallen — und den sieht man nur, wenn jemand hinschaut, wenn es passiert. "
            + "Deshalb hängt er am Monitor und sitzt nicht zu Hause am Wasserkocher.",
        weiter: "ende"
      },
      halb: {
        text: "Langsam. Und weiter? Langsam allein lässt niemanden umfallen, sonst läge die halbe Sportmannschaft "
            + "auf dem Boden. Schauen Sie sich die Überleitung an — wie lang braucht der Vorhof bis zur Kammer?",
        weiter: "ende"
      },
      anamnese: {
        text: "Das hat mir Schwester Marlene schon erzählt, und sie erzählt es besser. Von Ihnen wollte ich Zahlen. "
            + "Gehen Sie zurück an den Streifen.",
        weiter: "ende"
      },
      ende: {
        text: "So. Jetzt wird beobachtet. Und beobachten heißt: hinschauen, nicht abwarten. — "
            + "Hier endet das, was bisher gebaut ist. Der Rest der Schicht kommt noch.",
        endeText: "Ende des spielbaren Teils"
      }
    }
  };

  /* ------------------------------------------------------------ Handlungen */
  function ekgSchreiben() {
    if (!hat("ekg_geschrieben")) {
      setze("ekg_geschrieben");
      zeitVor(8);
      melde(T("EKG geschrieben · {zeit}", { zeit: zeitText() }));
    }
    var s = satz(AUFNAHME_EKG);
    frage({
      titel: "Der Streifen liegt vor dir",
      text: "Erst der Rhythmus, dann die Zahlen. Schau: Kommt vor jedem Kammerkomplex eine P-Welle, "
          + "und sind die Abstände gleich?",
      ekg: { satz: AUFNAHME_EKG, mmProS: 25, von: 1.8, dauer: 7 },
      antworten: [
        {
          text: "Vorhofflimmern — keine P-Wellen, unregelmäßig.",
          warum: "Sieh genauer hin: Vor jedem QRS steht eine eigene kleine Welle, und die Abstände sind gleich lang. "
               + "Bei Vorhofflimmern wäre beides nicht so."
        },
        {
          text: "Sinusrhythmus — vor jedem QRS eine P-Welle, regelmäßig.",
          richtig: true,
          warum: "Jede Kammeraktion hat ihre P-Welle, die Abstände sind gleich. Der Sinusknoten gibt den Takt. "
               + "Nur gibt er ihn langsam — das ist die nächste Frage."
        },
        {
          text: "Kammertachykardie — breite Komplexe, schnell.",
          warum: "Die Komplexe sind schmal (unter 120 ms) und die Frequenz ist niedrig. Das Gegenteil davon."
        }
      ],
      fertig: function () {
        befund({
          id: "b-rhythmus", titel: "Rhythmus: Sinus", zeit: zeitText(),
          text: "Vor jedem QRS eine P-Welle, RR-Abstände gleich. Der Sinusknoten führt.",
          ekg: { satz: AUFNAHME_EKG, mmProS: 25, von: 1.8, dauer: 6 }
        });
        zeitVor(3);
      }
    });
  }

  function messeFrequenz() {
    global.Zirkel.starte({
      satz: satz(AUFNAHME_EKG), was: "rr", toleranz: 25, mmProS: 25, von: 1.9, dauer: 7,
      titel: "Wie langsam ist langsam?",
      auftrag: "Miss einen RR-Abstand. Aus ihm kommt die Frequenz: 60 000 geteilt durch den RR-Abstand in Millisekunden.",
      deutung: function (ms) {
        return T("60 000 : {ms} = {hf} pro Minute. Unter 60 — Bradykardie.",
                 { ms: ms, hf: Math.round(60000 / ms) });
      },
      fertig: function (erg) {
        var hf = Math.round(60000 / erg.wahrheit);
        Z.werte.hf = hf; Z.werte.rr = erg.wahrheit;
        befund({
          id: "b-frequenz", titel: T("Frequenz: {hf}/min", { hf: hf }), zeit: zeitText(),
          text: T("RR {rr} ms. 60 000 : {rr} = {hf} pro Minute. Norm 60–100, also Bradykardie.",
                  { rr: erg.wahrheit, hf: hf }),
          ekg: { satz: AUFNAHME_EKG, mmProS: 25, von: 1.9, dauer: 6 }
        });
        zeitVor(6);
      }
    });
  }

  function messePq() {
    global.Zirkel.starte({
      satz: satz(AUFNAHME_EKG), was: "pq", toleranz: 20, mmProS: 50, von: 2.9, dauer: 2.6,
      titel: "Wie lange braucht der Impuls nach unten?",
      auftrag: "Miss die PQ-Zeit. Bei 50 mm/s ist ein kleines Kästchen 20 Millisekunden breit.",
      deutung: function (ms) {
        return ms > 200
          ? T("Norm 120–200 ms. {ms} ms ist zu lang: AV-Block I. Grades.", { ms: ms })
          : T("Norm 120–200 ms — das liegt im Rahmen.");
      },
      fertig: function (erg) {
        Z.werte.pq = erg.wahrheit;
        befund({
          id: "b-pq", titel: T("PQ-Zeit: {ms} ms", { ms: erg.wahrheit }), zeit: zeitText(),
          text: T("Norm 120–200 ms. {ms} ms — AV-Block I. Grades. Die Überleitung ist verzögert, aber jeder "
                + "Vorhofimpuls kommt noch an. (Der P-Beginn liegt nie ganz scharf; von Schlag zu Schlag schwanken "
                + "die Werte um einige Millisekunden. Im Zweifel mehrere Schläge messen.)", { ms: erg.wahrheit }),
          ekg: { satz: AUFNAHME_EKG, mmProS: 50, von: 2.9, dauer: 2.4 },
          vergleich: {
            "b-frequenz": "Beides zusammen: Der Taktgeber ist langsam UND die Leitung dorthin ist lang. "
                        + "Zwei Etagen, die beide zäh sind."
          }
        });
        zeitVor(6);
        if (!hat("monitor_frei")) melde("Das solltest du Marlene sagen.");
      }
    });
  }

  function tueteAnsehen() {
    setze("tuete_gesehen");
    frage({
      titel: "Die Tüte",
      text: "Drei Schachteln und ein Foto. Bisoprolol 5 mg · Ramipril 5 mg · ASS 100 mg. "
          + "Welche davon geht dich beim langsamen Puls etwas an?",
      antworten: [
        { text: "ASS 100 — der Blutverdünner.", warum: "ASS beeinflusst die Gerinnung, nicht die Frequenz." },
        { text: "Ramipril — der Blutdrucksenker.", warum: "ACE-Hemmer senken den Druck, bremsen aber weder Sinusknoten noch AV-Knoten." },
        {
          text: "Bisoprolol — der Betablocker.", richtig: true,
          warum: "Betablocker bremsen den Sinusknoten und verlangsamen die AV-Überleitung. Das zählt doppelt: "
               + "Eine langsame Frequenz gilt nur dann als verdächtig, wenn kein bremsendes Medikament im Spiel "
               + "ist — und hier ist eins im Spiel. Erklärt aber immer noch nicht die Bewusstlosigkeit: "
               + "Ein Betablocker macht langsam, nicht ohnmächtig."
        }
      ],
      fertig: function () {
        befund({
          id: "b-medis", titel: "Medikamente", zeit: zeitText(),
          text: "Bisoprolol 5 mg, Ramipril 5 mg, ASS 100 mg. Der Betablocker bremst Sinusknoten und AV-Knoten — "
              + "er erklärt die langsame Frequenz mit, aber keine Bewusstlosigkeit ohne Vorwarnung. "
              + "Eine Bradykardie unter bremsender Medikation ist erwartbar, nicht verdächtig.",
          symbol: tablettenBild()
        });
        zeitVor(4);
      }
    });
  }

  function tablettenBild() {
    return '<svg viewBox="0 0 220 80" style="width:100%;height:auto">' +
      '<rect x="8" y="14" width="56" height="52" rx="4" fill="#F4E6D2" stroke="#10212B" stroke-width="2"/>' +
      '<rect x="16" y="24" width="40" height="5" fill="#C2185B"/>' +
      '<rect x="16" y="36" width="30" height="4" fill="#10212B" opacity=".45"/>' +
      '<rect x="78" y="20" width="52" height="46" rx="4" fill="#F4E6D2" stroke="#10212B" stroke-width="2"/>' +
      '<rect x="86" y="30" width="36" height="4" fill="#10212B" opacity=".45"/>' +
      '<rect x="144" y="26" width="48" height="40" rx="4" fill="#F4E6D2" stroke="#10212B" stroke-width="2"/>' +
      '<rect x="152" y="36" width="32" height="4" fill="#10212B" opacity=".45"/></svg>';
  }

  /* ------------------------------------------------------------ Stand der Schicht */
  function kapitelStand() {
    var hat = [], offen = [], M = global.Mappe;
    Z.befunde.forEach(function (b) { hat.push(T(b.titel) + " <em>" + b.zeit + "</em>"); });
    if (Z.marken.fall_gehoert) hat.push("Die Geschichte des Falls von Marlene");
    if (Z.marken.k_anamnese) hat.push("Herrn Baums eigene Schilderung");

    if (!Z.marken.fall_gehoert) offen.push("Marlene weiß, warum der Mann hier sitzt. Du noch nicht.");
    if (!Z.marken.k_anamnese) offen.push("Mit Herrn Baum selbst hast du noch nicht gesprochen.");
    if (!Z.marken.auftrag_ekg) offen.push("Es ist noch kein EKG geschrieben.");
    else {
      if (!M.hat("b-rhythmus")) offen.push("Der Rhythmus ist noch nicht bestimmt.");
      if (!M.hat("b-frequenz")) offen.push("Die Frequenz ist noch nicht gemessen — RR-Abstand, Zirkel.");
      if (!M.hat("b-pq")) offen.push("Die PQ-Zeit ist noch nicht gemessen.");
    }
    if (!M.hat("b-medis")) {
      offen.push(Z.marken.darf_tuete
        ? "In die Plastiktüte hast du noch nicht geschaut."
        : "Was Herr Baum einnimmt, weißt du nicht. Frag ihn.");
    }
    if (anzahlKernbefunde() < 2) {
      if (Z.marken.auftrag_ekg) {
        offen.push(T("Zwei Befunde aus dem EKG brauchst du, bevor dich jemand weiterschickt. Du hast {n}.",
                     { n: anzahlKernbefunde() }));
      }
    } else if (!Z.marken.ankunft_monitor) {
      offen.push("Der Flur rechts steht offen. Marlene meldet dich an.");
    }
    if (Z.marken.ankunft_monitor && !Z.marken.falk_gesprochen) {
      offen.push("Dr. Falk steht im Monitorzimmer und wartet auf Zahlen.");
    }

    var fuss = "";
    if (Z.marken.ankunft_monitor && Z.marken.falk_gesprochen) {
      fuss = "Damit endet, was bisher gebaut ist. Der Rest der Schicht — Station, Intensiv, "
           + "Aufwachraum, Chefvisite — kommt noch.";
    } else if (!Z.befunde.length) {
      fuss = "Alles, was du selbst misst, landet in der Befundmappe. Vermutungen nicht.";
    }
    return {
      zeit: zeitText(), titel: Z.kapitel === 1 ? "Kapitel 1 · Aufnahme" : "Kapitel 2 · Monitorzimmer",
      ort: (global.Szene.raum(global.Szene.aktueller()) || {}).titel || "",
      hat: hat, offen: offen, fuss: fuss
    };
  }

  /* ------------------------------------------------------------ Räume */
  function baueRaeume(kunst) {
    global.Szene.registriere("aufnahme", {
      titel: "Aufnahme", ebenen: kunst.szenen.aufnahme, ersatzfarbe: "#2A3A42",
      beiBetreten: function () {
        Z.raum = "aufnahme"; stoppeMonitor(); kopfAuffrischen(); uhrStellen(); sichere();
      },
      felder: [
        {
          id: "marlene", name: "Schwester Marlene",
          punkte: [[16, 365], [548, 365], [548, 707], [16, 707]],
          bei: function () { global.Dialog.starte("marlene", "start"); }
        },
        {
          id: "herrk", name: "Herr Baum",
          punkte: [[1279, 399], [1424, 399], [1424, 737], [1279, 737]],
          bei: function () { global.Dialog.starte("herr_k", "start"); }
        },
        {
          id: "tuete", name: "Plastiktüte",
          punkte: [[1241, 628], [1307, 628], [1307, 728], [1241, 728]],
          sichtbar: function () { return hat("darf_tuete"); },
          erledigt: function () { return global.Mappe.hat("b-medis"); },
          bei: tueteAnsehen
        },
        {
          id: "wagen", name: "EKG-Wagen",
          punkte: [[822, 422], [960, 422], [960, 738], [822, 738]],
          erledigt: function () { return global.Mappe.hat("b-rhythmus"); },
          bei: function () {
            if (!hat("auftrag_ekg")) {
              melde("Erst fragen, dann schreiben. Marlene weiß, worum es geht.");
              return;
            }
            if (!global.Mappe.hat("b-rhythmus")) { ekgSchreiben(); return; }
            wahlMessung();
          }
        },
        {
          id: "uhr", name: "Wanduhr",
          punkte: [[1332, 167], [1466, 167], [1466, 295], [1332, 295]],
          bei: function () {
            melde(T("{zeit} · Schichtbeginn war 06:30.", { zeit: zeitText() }));
          }
        },
        {
          id: "pinnwand", name: "Pinnwand",
          punkte: [[284, 197], [486, 197], [486, 358], [284, 358]],
          bei: function () {
            melde("Dienstplan, ein Zettel über die Kaffeekasse, ein Kinderbild ohne Namen.");
          }
        }
      ],
      ausgaenge: [
        {
          name: "Flur zum Monitorzimmer", nach: "monitor",
          punkte: [[1533, 228], [1600, 228], [1600, 701], [1533, 701]],
          wenn: function () { return anzahlKernbefunde() >= 2; },
          gesperrt: function () {
            melde("Noch nicht. Mit leerer Mappe meldet dich Marlene nirgends an.", "warnung");
          }
        }
      ]
    });

    global.Szene.registriere("monitor", {
      titel: "Monitorzimmer", ebenen: kunst.szenen.monitor, ersatzfarbe: "#1C2A31",
      beiBetreten: function () {
        Z.raum = "monitor"; Z.kapitel = 2;
        if (!hat("ankunft_monitor")) { Z.zeit = Math.max(Z.zeit, 9 * 60 + 15); setze("ankunft_monitor"); }
        kopfAuffrischen(); sichere();
        starteMonitor();
        global.setTimeout(function () {
          if (!hat("falk_gesprochen")) {
            setze("falk_gesprochen");
            global.Dialog.starte("falk", "start");
          }
        }, 1400);
      },
      felder: [
        {
          id: "schirm", name: "Großer Monitor",
          punkte: [[794, 372], [1116, 372], [1116, 604], [794, 604]],
          bei: function () {
            melde("Sinusbradykardie, 53/min. Keine Pause in den letzten Minuten.");
          }
        },
        {
          id: "falk", name: "Dr. Falk",
          punkte: [[1178, 348], [1292, 348], [1300, 700], [1166, 700]],
          bei: function () { global.Dialog.starte("falk", "start"); }
        }
      ],
      ausgaenge: [
        {
          name: "Zurück in die Aufnahme", nach: "aufnahme",
          punkte: [[0, 300], [150, 300], [150, 880], [0, 880]]
        }
      ]
    });
  }

  function wahlMessung() {
    waehle({
      titel: "Was willst du messen?",
      text: "Der Streifen liegt auf dem Wagen. Nimm den Zirkel.",
      wahl: [
        { text: "Den RR-Abstand — die Frequenz", fertig: global.Mappe.hat("b-frequenz"), tu: messeFrequenz },
        { text: "Die PQ-Zeit — die Überleitung", fertig: global.Mappe.hat("b-pq"), tu: messePq }
      ]
    });
  }

  function waehle(opt) {
    var hof = document.getElementById("wahl-hof");
    if (!hof) {
      hof = document.createElement("div");
      hof.id = "wahl-hof"; hof.className = "raetsel wahl-hof";
      hof.innerHTML = '<div class="raetsel-innen schmal"><div class="raetsel-kopf"><h2></h2>' +
        '<button class="knopf zu" type="button">' + T("Zurück") + '</button></div>' +
        '<p class="raetsel-auftrag"></p><div class="frage-wahl"></div></div>';
      document.body.appendChild(hof);
      hof.querySelector(".zu").addEventListener("click", function () {
        hof.classList.remove("an"); global.Szene.sperre(false); global.Szene.aktualisiere();
      });
    }
    hof.querySelector("h2").textContent = T(opt.titel);
    hof.querySelector(".raetsel-auftrag").textContent = T(opt.text);
    var feld = hof.querySelector(".frage-wahl");
    feld.innerHTML = "";
    opt.wahl.forEach(function (w) {
      var b = document.createElement("button");
      b.type = "button"; b.className = "knopf wahl" + (w.fertig ? " erledigt" : "");
      b.textContent = T(w.text) + (w.fertig ? "  ✓" : "");
      b.addEventListener("click", function () { hof.classList.remove("an"); w.tu(); });
      feld.appendChild(b);
    });
    hof.classList.add("an");
    global.Szene.sperre(true);
  }

  /* Monitor: die Kurve läuft wirklich, aus derselben Aufnahme. */
  var monitorStreifen = null;
  function stoppeMonitor() {
    if (monitorStreifen) { monitorStreifen.stoppeLauf(); monitorStreifen = null; }
    var alt = document.getElementById("monitor-lauf");
    if (alt && alt.parentNode) alt.parentNode.removeChild(alt);
  }
  function starteMonitor() {
    stoppeMonitor();
    var buehne = document.getElementById("buehne");
    var d = document.createElement("div");
    d.id = "monitor-lauf"; d.className = "monitor-lauf";
    d.innerHTML = '<canvas height="150"></canvas>';
    buehne.appendChild(d);
    var s = satz(AUFNAHME_EKG);
    monitorStreifen = global.EKG.Streifen(d.querySelector("canvas"), {
      werte: s.sig.werte, fs: s.sig.fs, mmProS: 25, dauer: 5.2,
      monitor: true, kalibrierung: false
    });
    global.requestAnimationFrame(function () {
      monitorStreifen.zeichne();
      monitorStreifen.starteLauf(1);
    });
  }

  /* ------------------------------------------------------------ Start */
  function start(kunst, ekgDaten) {
    ekgDaten.forEach(function (r) { SATZ[r.id] = r; });
    global.Szene.start(document.getElementById("buehne"));
    global.Mappe.start(Z, satz);
    global.Stand.start(Z, kapitelStand);
    global.Dialog.lade({
      baeume: DIALOGE, portraits: kunst.portraits,
      namen: { marlene: "Schwester Marlene", herr_k: "Herr Baum", falk: "Oberarzt Dr. Falk" }
    });
    baueRaeume(kunst);

    document.getElementById("kopf-mappe").addEventListener("click", global.Mappe.oeffne);
    document.getElementById("kopf-stand").addEventListener("click", global.Stand.oeffne);
    global.Sprache.waehler(document.getElementById("kopf-sprache"));
    document.getElementById("kopf-zeigen").addEventListener("click", function () {
      global.Szene.zeigeFelder(2400);
    });
    document.addEventListener("keydown", function (e) {
      if (e.key === "h" && !global.Dialog.laeuft()) global.Szene.zeigeFelder(2400);
      if (e.key === "s" && !global.Dialog.laeuft()) global.Stand.oeffne();
    });
    document.getElementById("kopf-neu").addEventListener("click", function () {
      if (global.confirm(T("Schicht von vorn beginnen? Die Befundmappe wird geleert."))) vonVorn();
    });

    var fortsetzung = lade();
    global.Szene.zeige(Z.raum || "aufnahme", true);
    kopfAuffrischen();
    global.setTimeout(uhrStellen, 120);

    if (!fortsetzung) {
      global.setTimeout(function () { global.Dialog.starte("auftakt", "start"); }, 700);
    }
  }

  /* Sprachwechsel: der Zustand liegt im Speicher, also ist Neuladen der
     sauberste Weg — alle Oberflächen werden neu und richtig aufgebaut. */
  function neuZeichnen() {
    sichere();
    try { global.location.reload(); } catch (e) {}
  }

  global.Spiel = {
    start: start, melde: melde, neuZeichnen: neuZeichnen, sichere: sichere, zaehlerAuffrischen: kopfAuffrischen,
    zustand: Z, satz: satz, hat: hat, vonVorn: vonVorn,
    __dialoge: DIALOGE, __ekgSchreiben: ekgSchreiben, __messePq: messePq, __messeFrequenz: messeFrequenz,
    __tuete: tueteAnsehen
  };
})(window);
