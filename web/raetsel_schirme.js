/* Rätsel „Drei Schirme": mehrere echte Aufnahmen untereinander, wie an einer
   Monitorzentrale, dazu eine Folge kleiner Fragen.

   Die Kurven stehen (Standbild), damit man in Ruhe lesen kann: Wer eine
   PQ-Zeit gegen ein großes Kästchen halten soll, braucht eine Kurve, die
   stillhält. Ohne Fragen ist es eine Rückschau mit Unterschrift je Schirm.

   Bedienung wie überall: antippen, Ziffern wählen, Enter führt weiter,
   Escape und „Zurück" oben rechts schließen.                                 */
(function (global) {
  "use strict";

  var hof = null, S = null, schritt = 0, gewaehlt = [], streifen = [];

  function bau() {
    hof = document.createElement("div");
    hof.className = "raetsel schirme";
    hof.id = "schirme-hof";
    hof.innerHTML =
      '<div class="raetsel-innen">' +
      '  <div class="raetsel-kopf"><h2></h2><button class="knopf zu" type="button">' + T("Zurück") + '</button></div>' +
      '  <p class="raetsel-auftrag"></p>' +
      '  <div class="schirm-liste"></div>' +
      '  <p class="schirme-frage"></p>' +
      '  <div class="frage-wahl"></div>' +
      '  <div class="rueck"></div>' +
      '  <div class="raetsel-knoepfe"><button class="knopf haupt weiter" type="button" hidden>' + T("Weiter") + '</button></div>' +
      '</div>';
    document.body.appendChild(hof);
    hof.querySelector(".zu").addEventListener("click", function () {
      var ab = S && S.abbruch;
      schliesse();
      if (ab) ab();
    });
    hof.querySelector(".weiter").addEventListener("click", weiter);
    document.addEventListener("keydown", taste);
    global.addEventListener("resize", function () { if (offen()) zeichneAlle(); });
  }

  function offen() { return !!hof && hof.classList.contains("an"); }

  function taste(e) {
    if (!offen()) return;
    if (/^[1-9]$/.test(e.key)) {
      var k = hof.querySelectorAll(".frage-wahl .knopf")[+e.key - 1];
      if (k && !k.disabled) { e.preventDefault(); k.click(); }
    } else if (e.key === "Enter" || e.key === " ") {
      var w = hof.querySelector(".weiter");
      if (!w.hidden) { e.preventDefault(); w.click(); }
    } else if (e.key === "Escape") {
      e.preventDefault();
      hof.querySelector(".zu").click();
    }
  }

  function zeichneAlle() {
    streifen.forEach(function (s) { s.zeichne(); });
  }

  function maleSchirme() {
    var liste = hof.querySelector(".schirm-liste");
    liste.innerHTML = S.schirme.map(function (s, i) {
      return '<figure class="schirm" data-i="' + i + '">' +
        '<figcaption class="schirm-kopf"><span class="schirm-name">' + T(s.name) + '</span>' +
        '<span class="schirm-info">' + T("Ableitung {lead} · 25 mm/s · Standbild",
                                        { lead: (s.satz.sig.lead || "II").toUpperCase() }) + '</span></figcaption>' +
        '<canvas height="116"></canvas>' +
        (s.unter ? '<p class="schirm-unter">' + T(s.unter) + '</p>' : '') +
        '</figure>';
    }).join("");
    streifen = [];
    Array.prototype.forEach.call(liste.getElementsByTagName("canvas"), function (lw, i) {
      var s = S.schirme[i];
      streifen.push(global.EKG.Streifen(lw, {
        werte: s.satz.sig.werte, fs: s.satz.sig.fs, mmProS: 25,
        von: s.von || 0, dauer: s.dauer || 6, monitor: true, kalibrierung: false
      }));
    });
    global.requestAnimationFrame(zeichneAlle);
    global.setTimeout(zeichneAlle, 80);
  }

  function hervorheben(i) {
    Array.prototype.forEach.call(hof.querySelectorAll(".schirm"), function (el) {
      el.classList.toggle("hervor", +el.dataset.i === i);
    });
  }

  function rueck(art, titel, text) {
    var r = hof.querySelector(".rueck");
    r.className = "rueck" + (art ? " " + art : "");
    r.innerHTML = titel ? "<strong>" + T(titel) + "</strong> " + T(text || "") : "";
  }

  function zeigeSchritt() {
    var st = S.schritte[schritt];
    hof.querySelector(".schirme-frage").textContent = T(st.frage);
    rueck("", "");
    hof.querySelector(".weiter").hidden = true;
    var wahl = hof.querySelector(".frage-wahl");
    wahl.innerHTML = "";
    st.antworten.forEach(function (a, i) {
      var b = document.createElement("button");
      b.type = "button"; b.className = "knopf wahl";
      var nr = document.createElement("span");
      nr.className = "nr"; nr.textContent = String(i + 1);
      b.appendChild(nr);
      b.appendChild(document.createTextNode(T(a.text)));
      b.addEventListener("click", function () { waehle(a, b); });
      wahl.appendChild(b);
    });
    hervorheben(st.hervor === undefined ? -1 : st.hervor);
  }

  function waehle(a, b) {
    var wahl = hof.querySelector(".frage-wahl");
    b.disabled = true;
    b.classList.add(a.richtig ? "richtig" : "falsch");
    rueck(a.richtig ? "gut" : "fast", a.richtig ? "Richtig." : "Nicht ganz.", a.warum);
    if (!a.richtig) return;                 /* die anderen bleiben wählbar */
    gewaehlt[schritt] = a;
    Array.prototype.forEach.call(wahl.children, function (c) { c.disabled = true; });
    var w = hof.querySelector(".weiter");
    w.hidden = false;
    try { w.scrollIntoView({ block: "nearest" }); w.focus({ preventScroll: true }); } catch (e) { w.focus(); }
  }

  function weiter() {
    if (schritt < S.schritte.length - 1) { schritt++; zeigeSchritt(); return; }
    var f = S.fertig, g = gewaehlt.slice();
    schliesse();
    if (f) f(g);
  }

  function starte(opt) {
    if (!hof) bau();
    S = opt; schritt = 0; gewaehlt = [];
    S.schritte = S.schritte || [];
    hof.querySelector("h2").textContent = T(S.titel);
    hof.querySelector(".raetsel-auftrag").textContent = T(S.text);
    var rueckschau = !S.schritte.length;
    hof.classList.toggle("rueckschau", rueckschau);
    hof.classList.add("an");
    if (global.Szene) global.Szene.sperre(true);
    maleSchirme();
    if (rueckschau) {
      hof.querySelector(".schirme-frage").textContent = "";
      hof.querySelector(".frage-wahl").innerHTML = "";
      hof.querySelector(".weiter").hidden = true;
      rueck("", "");
      hervorheben(S.hervor === undefined ? -1 : S.hervor);
    } else {
      zeigeSchritt();
    }
  }

  function schliesse() {
    if (hof) hof.classList.remove("an");
    streifen = [];
    if (global.Szene) { global.Szene.sperre(false); global.Szene.aktualisiere(); }
  }

  global.Schirme = { starte: starte, schliesse: schliesse, offen: offen };
})(window);
