/* Rätsel „Zirkel": am echten Streifen messen.

   Geprüft wird gegen die Experten-Annotation der Datenbank — und zwar zweierlei:
   ob die Strecke die richtige Länge hat UND ob sie an der richtigen Stelle liegt.
   Wer 200 ms irgendwo misst, hat nicht die PQ-Zeit gemessen.                 */
(function (global) {
  "use strict";

  var AUFGABEN = {
    rr: {
      name: "RR-Abstand", von: "r", bis: "r", folge: true,
      wie: "Von einer R-Zacke zur nächsten.",
      anfang: "R-Zacke", ende: "nächste R-Zacke"
    },
    pq: {
      name: "PQ-Zeit", von: "p0", bis: "q0",
      wie: "Vom Beginn der P-Welle bis zum Beginn des QRS-Komplexes — nicht bis zur R-Zacke.",
      anfang: "Beginn der P-Welle", ende: "Beginn des QRS"
    },
    qrs: {
      name: "QRS-Breite", von: "q0", bis: "q1",
      wie: "Vom ersten bis zum letzten Ausschlag des Kammerkomplexes.",
      anfang: "Beginn des QRS", ende: "Ende des QRS"
    },
    qt: {
      name: "QT-Zeit", von: "q0", bis: "t1",
      wie: "Vom Beginn des QRS bis zum Ende der T-Welle.",
      anfang: "Beginn des QRS", ende: "Ende der T-Welle"
    }
  };

  var hof = null, S = null, streifen = null, versuche = 0, letzte = null;

  function bau() {
    hof = document.createElement("div");
    hof.className = "raetsel";
    hof.id = "zirkel-hof";
    hof.innerHTML =
      '<div class="raetsel-innen">' +
      '  <div class="raetsel-kopf"><h2></h2><button class="knopf zu" type="button">Zurück</button></div>' +
      '  <p class="raetsel-auftrag"></p>' +
      '  <div class="raetsel-papier"><canvas height="196"></canvas></div>' +
      '  <div class="raetsel-anzeige"><span class="wert">—</span><span class="einheit">ms</span>' +
      '    <span class="raetsel-tempo"></span></div>' +
      '  <div class="rueck"></div>' +
      '  <div class="raetsel-knoepfe">' +
      '    <button class="knopf loesung" type="button">Lösung zeigen</button>' +
      '    <button class="knopf nochmal" type="button">Nochmal</button>' +
      '    <button class="knopf haupt uebernehmen" type="button" hidden>In die Mappe</button>' +
      '  </div>' +
      '</div>';
    document.body.appendChild(hof);
    hof.querySelector(".zu").addEventListener("click", schliesse);
    hof.querySelector(".loesung").addEventListener("click", zeigeLoesung);
    hof.querySelector(".nochmal").addEventListener("click", function () {
      streifen.setze({ zirkel: null, loesung: null, marken: null });
      rueck("", "");
      hof.querySelector(".wert").textContent = "—";
      hof.querySelector(".uebernehmen").hidden = true;
    });
    hof.querySelector(".uebernehmen").addEventListener("click", function () {
      hof.querySelector(".uebernehmen").hidden = true;
      var f = S.fertig; var erg = letzte;
      schliesse();
      if (f) f(erg);
    });
  }

  function rueck(art, titel, text) {
    var r = hof.querySelector(".rueck");
    r.className = "rueck" + (art ? " " + art : "");
    r.innerHTML = titel ? "<strong>" + titel + "</strong>" + (text ? " " + text : "") : "";
  }

  /* Welcher Schlag war gemeint? Der, dessen Anfangsmarke dem Messanfang am nächsten liegt. */
  function passenderSchlag(a, start, ende) {
    var sl = S.satz.schlaege, best = null;
    for (var i = 0; i < sl.length; i++) {
      var s1 = sl[i][a.von], s2;
      if (a.folge) {
        if (i + 1 >= sl.length) break;
        s2 = sl[i + 1][a.bis];
      } else s2 = sl[i][a.bis];
      if (s1 === undefined || s2 === undefined) continue;
      if (s1 < S.von - 0.02 || s2 > S.von + S.dauer + 0.02) continue;
      var d = Math.abs(start - s1) + Math.abs(ende - s2);
      if (!best || d < best.d) best = { d: d, a: s1, b: s2, i: i };
    }
    return best;
  }

  function pruefe(ms, start, ende) {
    versuche++;
    var a = AUFGABEN[S.was];
    hof.querySelector(".wert").textContent = ms;
    var t = passenderSchlag(a, start, ende);
    if (!t) {
      rueck("fast", "Kein Schlag in Reichweite.", "Setz den Zirkel an eine Welle im Streifen an.");
      return;
    }
    var wahr = Math.round((t.b - t.a) * 1000);
    var dStart = (start - t.a) * 1000, dEnde = (ende - t.b) * 1000;
    var ab = ms - wahr;

    if (Math.abs(dStart) > 170 || Math.abs(dEnde) > 170) {
      rueck("fast", "Das war eine andere Strecke.",
            "Gemessen werden soll: " + a.anfang + " → " + a.ende + ". " + a.wie +
            " Tipp: „Lösung zeigen" + "“ blendet die richtige Strecke ein.");
      return;
    }
    if (Math.abs(ab) <= S.toleranz) {
      letzte = { ok: true, gemessen: ms, wahrheit: wahr, abweichung: ab, versuche: versuche, schlag: t.i };
      rueck("gut", a.name + " = " + wahr + " ms.",
            (Math.abs(ab) <= 4 ? "Auf die Millisekunde." : "Deine Messung: " + ms + " ms, " +
             (ab > 0 ? "+" : "") + ab + " ms daneben — innerhalb der Toleranz.") +
            " " + (S.deutung ? S.deutung(wahr) : ""));
      streifen.setze({ loesung: { start: t.a, ende: t.b } });
      hof.querySelector(".uebernehmen").hidden = false;
      return;
    }
    var hinweis;
    if (Math.abs(dStart) > Math.abs(dEnde)) {
      hinweis = "Dein Anfang liegt " + Math.abs(Math.round(dStart)) + " ms " +
                (dStart > 0 ? "zu spät" : "zu früh") + ". Der " + a.anfang + " ist gemeint.";
    } else {
      hinweis = "Dein Ende liegt " + Math.abs(Math.round(dEnde)) + " ms " +
                (dEnde > 0 ? "zu spät" : "zu früh") + ". Das " + a.ende + " ist gemeint.";
    }
    letzte = { ok: false, gemessen: ms, wahrheit: wahr, abweichung: ab, versuche: versuche };
    rueck("fast", ms + " ms — noch nicht.", hinweis +
          " (Toleranz ±" + S.toleranz + " ms.)");
  }

  function zeigeLoesung() {
    var a = AUFGABEN[S.was], sl = S.satz.schlaege;
    for (var i = 0; i < sl.length; i++) {
      var s1 = sl[i][a.von], s2 = a.folge ? (sl[i + 1] && sl[i + 1][a.bis]) : sl[i][a.bis];
      if (s1 === undefined || s2 === undefined) continue;
      if (s1 < S.von || s2 > S.von + S.dauer) continue;
      streifen.setze({ loesung: { start: s1, ende: s2 },
                       marken: [{ s: s1 }, { s: s2 }] });
      rueck("", a.name + ": " + Math.round((s2 - s1) * 1000) + " ms.",
            a.wie + " Jetzt selbst nachmessen — „Nochmal" + "“.");
      return;
    }
  }

  function starte(opt) {
    if (!hof) bau();
    S = opt;
    S.toleranz = S.toleranz || 20;
    S.mmProS = S.mmProS || (S.was === "rr" ? 25 : 50);
    S.von = S.von || 0;
    S.dauer = S.dauer || (S.was === "rr" ? 6 : 3);
    versuche = 0; letzte = null;
    var a = AUFGABEN[S.was];
    hof.querySelector("h2").textContent = S.titel || ("Messen: " + a.name);
    hof.querySelector(".raetsel-auftrag").innerHTML =
      (S.auftrag || ("Miss die " + a.name + ".")) + " <em>" + a.wie + "</em>";
    hof.querySelector(".raetsel-tempo").textContent =
      S.mmProS + " mm/s · 10 mm/mV · Ableitung " + (S.satz.sig.lead || "II").toUpperCase();
    hof.querySelector(".wert").textContent = "—";
    hof.querySelector(".uebernehmen").hidden = true;
    rueck("", "Zieh mit Finger, Pencil oder Maus über den Streifen.", "");
    hof.classList.add("an");
    if (global.Szene) global.Szene.sperre(true);

    /* Nur ein Streifen je Leinwand — sonst zeigen alte Zeigerzuhörer auf alte Zustände. */
    var lw = hof.querySelector("canvas");
    lw.style.width = "100%";
    if (!streifen) {
      streifen = global.EKG.Streifen(lw, { werte: [], fs: 250 });
      streifen.messbar(pruefe, function (ms) { hof.querySelector(".wert").textContent = ms; });
      hof.__streifen = streifen;
    }
    streifen.setze({
      werte: S.satz.sig.werte, fs: S.satz.sig.fs, mmProS: S.mmProS,
      von: S.von, dauer: S.dauer, zirkel: null, loesung: null, marken: null
    });
    global.requestAnimationFrame(function () { streifen.zeichne(); });
    global.setTimeout(function () { streifen.zeichne(); }, 80);
  }

  function schliesse() {
    if (hof) hof.classList.remove("an");
    if (global.Szene) { global.Szene.sperre(false); global.Szene.aktualisiere(); }
  }

  global.Zirkel = { starte: starte, schliesse: schliesse, AUFGABEN: AUFGABEN,
                    __pruefe: function (ms, a, b) { return pruefe(ms, a, b); } };
})(window);
