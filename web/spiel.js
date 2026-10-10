/* „Nachtdienst" — Kapitel 1: Aufnahme, 06:40 · Kapitel 2: Monitorzimmer, 09:15.
   Fall: Herr Konrad Baum, 68, zwei Synkopen ohne Vorwarnung.
   Alle Kurven stammen aus echten Aufnahmen (LUDB), alle Zeiten aus deren
   Experten-Annotation. Erfunden sind nur die Menschen.                        */
(function (global) {
  "use strict";

  var SCHLUESSEL = "nachtdienst-1";
  var AUFNAHME_EKG = 39;          /* Sinusrhythmus 53/min (Datenbank: „Sinus bradycardia“; Lehrbuch Lektion 8: Bradykardie erst < 50), PQ 228 ms — AV-Block I° */
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
        umleiten: function () { return hat("k2_auftrag") ? "wieder" : null; },
        text: "Sie sind die Neue. Falk. — Bevor Sie etwas sagen: Ich will nicht hören, was Sie vermuten. "
            + "Ich will hören, was Sie gemessen haben.",
        antworten: [
          {
            text: function () {
              return T("Sinusrhythmus, {hf} pro Minute, PQ {pq} Millisekunden.",
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
        text: "So. Jetzt wird beobachtet. Und beobachten heißt: hinschauen, nicht abwarten.",
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
      ende2: {
        text: "Bleiben Sie bei ihm. — Hier endet, was bisher gebaut ist. Der Rest der Schicht kommt noch.",
        endeText: "Ende des spielbaren Teils"
      }
    }
  };

  /* --- Reizleitung: Einstieg --- */
  /* Marlene zeigt ihr Schema, sobald das EKG geschrieben ist. Alles, was Kapitel 1
     dafür braucht, steht in diesem Block; das Rätsel liegt in web/raetsel_reizleitung.js. */
  DIALOGE.marlene.start.antworten.splice(DIALOGE.marlene.start.antworten.length - 1, 0, {
    text: "Wie kommt der Takt eigentlich von oben nach unten?",
    wenn: function () { return hat("ekg_geschrieben") && !!global.Reizleitung; },
    zu: "reizleitung"
  });
  DIALOGE.marlene.reizleitung = {
    text: "Bevor du misst, solltest du wissen, was du da misst. Hier, mein altes Schema: ein Herz ohne Leitung. "
        + "Bau sie ein. Sitzt ein Teil falsch, sagt es dir der Streifen — echte Streifen, von echten Patienten.",
    antworten: [
      {
        text: "Zeig her.", zu: null,
        tu: function () {
          /* Erst schließt der Dialog und gibt die Bühne frei, dann öffnet das Rätsel. */
          global.setTimeout(function () {
            global.Reizleitung.starte({
              satz: satz,
              anmerkungen: {
                39: "Den kennst du: Das ist der Streifen von Herrn Baum. Sein AV-Knoten sitzt am richtigen Platz — er leitet nur langsamer."
              },
              fertig: function () {
                setze("reizleitung_gebaut");
                melde("Reizleitung gebaut: richtige Anatomie, normales EKG.");
              }
            });
          }, 60);
        }
      },
      { text: "Später.", zu: "start" }
    ]
  };
  /* --- Ende Reizleitung --- */

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
          warum: "Die Komplexe sind schmal (Norm 60–100 ms, Lektion 4) und die Frequenz ist niedrig. Das Gegenteil davon."
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

  /* Lehrbuch, Lektion 8: normale Frequenz 50–100/min, Sinusbradykardie < 50/min, Sinustachykardie > 100/min. */
  function frequenzSatz(hf) {
    if (hf < 50) return T("Unter 50 — Sinusbradykardie.");
    if (hf > 100) return T("Über 100 — Sinustachykardie.");
    if (hf <= 60) return T("Norm 50–100: noch im Rahmen, aber am unteren Rand. Sinusbradykardie beginnt erst unter 50.");
    return T("Norm 50–100: im Rahmen.");
  }

  function messeFrequenz() {
    global.Zirkel.starte({
      satz: satz(AUFNAHME_EKG), was: "rr", toleranz: 25, mmProS: 25, von: 1.9, dauer: 7,
      titel: "Wie langsam ist langsam?",
      auftrag: "Miss einen RR-Abstand. Aus ihm kommt die Frequenz: 60 000 geteilt durch den RR-Abstand in Millisekunden.",
      deutung: function (ms) {
        return T("60 000 : {ms} = {hf} pro Minute. ", { ms: ms, hf: Math.round(60000 / ms) }) + frequenzSatz(Math.round(60000 / ms));
      },
      fertig: function (erg) {
        var hf = Math.round(60000 / erg.wahrheit);
        Z.werte.hf = hf; Z.werte.rr = erg.wahrheit;
        befund({
          id: "b-frequenz", titel: T("Frequenz: {hf}/min", { hf: hf }), zeit: zeitText(),
          text: T("RR {rr} ms. 60 000 : {rr} = {hf} pro Minute. ", { rr: erg.wahrheit, hf: hf }) + frequenzSatz(hf),
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
              + "Eine niedrige Frequenz unter bremsender Medikation ist erwartbar, nicht verdächtig.",
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

  /* ============================================================ Kapitel 2: Monitorzimmer, 09:15
     Drei Schirme, drei echte Aufnahmen; welcher ist Herr Baum, und woran sieht
     man es? Danach klingelt sein Bett: die Ampel. Zwei Begründungen tragen
     (PQ-Zeit oder Frequenz), jede Ampel-Wahl führt weiter. Das Kapitel endet
     offen — was der Speicher zeigt, ist noch nicht gebaut.                    */

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
    if (!hat("k2_auftrag")) setze("k2_auftrag");
    var B = betten();
    var nB = bettVon(AUFNAHME_EKG), nF = bettVon(SCHIRM_FLIMMERN_EKG), nS = bettVon(SCHIRM_SCHNELL_EKG);
    var mB = satz(AUFNAHME_EKG).mess, mF = satz(SCHIRM_FLIMMERN_EKG).mess, mS = satz(SCHIRM_SCHNELL_EKG).mess;

    var unter = {};
    unter[AUFNAHME_EKG] = T("Herr Baum. Sinusrhythmus, {hf}/min, langsam. Vor jedem QRS eine P-Welle, PQ {pq} ms — länger "
                          + "als ein großes Kästchen: AV-Block I. Grades.", { hf: mB.frequenz, pq: mB.pq });
    unter[SCHIRM_FLIMMERN_EKG] = T("Keine P-Wellen, die RR-Abstände springen, etwa {hf}/min: Vorhofflimmern.",
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
      text: "Drei Schirme, drei Patienten, die Namen ausgeblendet. Ein großes Kästchen sind 200 ms.",
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
            + "Bett zählt {hf} pro Minute.", { n: n, hf: s.mess.frequenz }),
      frage: "Was tust du?",
      ekg: { satz: s, name: T("Bett {n} · Herr Baum", { n: n }), von: KAP2_FENSTER.von, dauer: 5 },
      sekunden: 10,
      wahl: [
        { id: "beobachten", farbe: "gruen", ampel: "Grün", text: "Beobachten",
          wie: "Bei ihm bleiben, den Monitor im Blick." },
        { id: "arzt", farbe: "gelb", ampel: "Gelb", text: "Arzt rufen",
          wie: "Dr. Falk rufen." },
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

  function grosserMonitor() {
    if (hat("k2_klingel") && !hat("k2_fertig")) { ampelAusloesen(); return; }
    if (hat("k2_bett")) {
      melde(T("Bett {n} · Herr Baum. Sinusbradykardie, {hf}/min, vor jedem QRS eine P-Welle.",
              { n: bettVon(AUFNAHME_EKG), hf: satz(AUFNAHME_EKG).mess.frequenz }));
      return;
    }
    zentrale();
  }

  function monitorwand() {
    if (hat("k2_klingel") && !hat("k2_fertig")) { ampelAusloesen(); return; }
    zentrale();
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

    /* Kapitel 2 — nennt das Ziel, nie die Lösung: kein Bett, kein Merkmal, bevor
       der Spieler es selbst gefunden hat. */
    if (Z.marken.k2_fertig) {
      hat.push(T("Bett {n} hat geklingelt: Herr Baum war blass. Dr. Falk sieht sich den Speicher an.",
                 { n: bettVon(AUFNAHME_EKG) }));
    }
    if (Z.marken.falk_gesprochen && !Z.marken.k2_bett) {
      offen.push("Dr. Falk will wissen, welcher der drei Schirme an der Wand Herrn Baum gehört — und woran du es siehst.");
    }
    if (Z.marken.k2_klingel && !Z.marken.k2_fertig) {
      offen.push(T("Bett {n} hat geklingelt. Herr Baum wartet.", { n: bettVon(AUFNAHME_EKG) }));
    }

    var fuss = "";
    if (Z.marken.k2_fertig) {
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
          if (global.Szene.aktueller() !== "monitor") return;
          if (!hat("falk_gesprochen")) {
            setze("falk_gesprochen");
            global.Dialog.starte("falk", "start");
          } else if (hat("k2_bett") && !hat("k2_fertig")) {
            ampelAusloesen();                       /* Kapitel 2: Bett klingelt (wieder) */
          }
        }, 1400);
      },
      felder: [
        /* --- Kapitel 2: neue Felder --- */
        {
          id: "wand", name: "Monitorwand · drei Betten",
          punkte: [[500, 112], [1384, 104], [1384, 340], [500, 352]],
          erledigt: function () { return hat("k2_bett"); },
          bei: function () { monitorwand(); }
        },
        /* --- Ende Kapitel 2: neue Felder --- */
        {
          id: "schirm", name: "Großer Monitor",
          punkte: [[794, 372], [1116, 372], [1116, 604], [794, 604]],
          bei: function () {
            grosserMonitor();
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
    __tuete: tueteAnsehen,
    __betten: betten, __zentrale: zentrale, __ampel: ampelAusloesen,
    KAPITEL2_EKG: { baum: AUFNAHME_EKG, flimmern: SCHIRM_FLIMMERN_EKG, schnell: SCHIRM_SCHNELL_EKG }
  };
})(window);
