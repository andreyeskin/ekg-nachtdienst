/* Motor: kleine Fenster, die kein Patient kennt.
     Fenster.frage(opt)         — eine Frage mit Antworten, optional ein Streifen darüber
     Fenster.waehle(opt)        — eine Auswahl ohne Bewertung (z. B. „Was willst du messen?")
     Fenster.befundzeilen(opt)  — Befundzeilen zum Lesen, dann „In die Mappe" (kein Rätsel)
   Alle drei sind .raetsel-Fenster: solange eines offen ist, bleibt die Bühne stumm.    */
(function (global) {
  "use strict";

  var satzFinden = null;
  function start(opt) { satzFinden = opt && opt.satz; }

  /* ------------------------------------------------------------ Kleine Frage */
  function frage(opt) {
    var hof = document.getElementById("frage-hof");
    if (!hof) {
      hof = document.createElement("div");
      hof.id = "frage-hof"; hof.className = "raetsel frage";
      hof.innerHTML = '<div class="raetsel-innen"><div class="raetsel-kopf"><h2></h2>' +
        '<button class="knopf zu" type="button">' + T("Zurück") + '</button></div>' +
        '<p class="raetsel-auftrag"></p><div class="frage-bild"></div>' +
        '<div class="frage-wahl"></div><div class="rueck"></div>' +
        '<div class="raetsel-knoepfe"><button class="knopf haupt weiter" type="button" hidden>' + T("Weiter") + '</button></div></div>';
      document.body.appendChild(hof);
      hof.querySelector(".zu").addEventListener("click", function () {
        hof.classList.remove("an"); global.Szene.sperre(false); global.Szene.aktualisiere();
      });
      /* Nichts schließt sich von allein (LEHRPLAN §5.7): Nach der richtigen Antwort
         bleibt die Begründung stehen, bis „Weiter" getippt ist. */
      hof.querySelector(".weiter").addEventListener("click", function () {
        hof.querySelector(".weiter").hidden = true;
        hof.classList.remove("an"); global.Szene.sperre(false);
        var f = hof.__fertig; hof.__fertig = null;
        if (f) f();
      });
      document.addEventListener("keydown", function (e) {
        if (!hof.classList.contains("an")) return;
        var w = hof.querySelector(".weiter");
        if ((e.key === "Enter" || e.key === " ") && !w.hidden) { e.preventDefault(); w.click(); }
        else if (/^[1-9]$/.test(e.key)) {
          var k = hof.querySelectorAll(".frage-wahl .knopf")[+e.key - 1];
          if (k && !k.disabled) { e.preventDefault(); k.click(); }
        } else if (e.key === "Escape") { e.preventDefault(); hof.querySelector(".zu").click(); }
      });
    }
    hof.__fertig = opt.fertig || null;
    hof.querySelector(".weiter").hidden = true;
    hof.querySelector("h2").textContent = T(opt.titel, opt.vars);
    hof.querySelector(".raetsel-auftrag").textContent = T(opt.text, opt.vars);
    var bild = hof.querySelector(".frage-bild");
    bild.innerHTML = opt.ekg ? '<canvas height="172" style="width:100%"></canvas>' : "";
    var rueck = hof.querySelector(".rueck");
    rueck.className = "rueck"; rueck.innerHTML = "";
    var wahl = hof.querySelector(".frage-wahl");
    wahl.innerHTML = "";
    opt.antworten.forEach(function (a) {
      var b = document.createElement("button");
      b.className = "knopf wahl"; b.type = "button"; b.textContent = T(a.text, opt.vars);
      b.addEventListener("click", function () {
        Array.prototype.forEach.call(wahl.children, function (c) { c.disabled = true; });
        b.classList.add(a.richtig ? "richtig" : "falsch");
        rueck.className = "rueck " + (a.richtig ? "gut" : "fast");
        rueck.innerHTML = "<strong>" + T(a.richtig ? "Richtig." : "Nicht ganz.") + "</strong> " + T(a.warum, opt.vars);
        if (a.richtig) {
          var w = hof.querySelector(".weiter");
          w.hidden = false;
          try { w.focus({ preventScroll: true }); } catch (x) { w.focus(); }
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
      var satz = typeof opt.ekg.satz === "object" ? opt.ekg.satz : satzFinden(opt.ekg.satz);
      var lw = bild.querySelector("canvas");
      var s = global.EKG.Streifen(lw, {
        werte: satz.sig.werte, fs: satz.sig.fs,
        mmProS: opt.ekg.mmProS || 25, von: opt.ekg.von || 0, dauer: opt.ekg.dauer || 6
      });
      global.requestAnimationFrame(s.zeichne);
      global.setTimeout(s.zeichne, 80);
    }
  }

  /* ------------------------------------------------------------ Auswahl ohne Bewertung */
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
    hof.querySelector("h2").textContent = T(opt.titel, opt.vars);
    hof.querySelector(".raetsel-auftrag").textContent = T(opt.text, opt.vars);
    var feld = hof.querySelector(".frage-wahl");
    feld.innerHTML = "";
    opt.wahl.forEach(function (w) {
      var b = document.createElement("button");
      b.type = "button"; b.className = "knopf wahl" + (w.fertig ? " erledigt" : "");
      b.textContent = T(w.text, opt.vars) + (w.fertig ? "  ✓" : "");
      b.addEventListener("click", function () { hof.classList.remove("an"); w.tu(); });
      feld.appendChild(b);
    });
    hof.classList.add("an");
    global.Szene.sperre(true);
  }

  /* ------------------------------------------------------------ Befundzeilen
     Was eine Untersuchung oder ein Bogen hergibt, zum Lesen — und dann als Karte in die Mappe.
     Kein Rätsel, keine Bewertung (KONZEPT §1.3). */
  function befundzeilen(opt) {
    var hof = document.getElementById("befund-hof");
    if (!hof) {
      hof = document.createElement("div");
      hof.id = "befund-hof"; hof.className = "raetsel befund";
      hof.innerHTML = '<div class="raetsel-innen schmal"><div class="raetsel-kopf"><h2></h2>' +
        '<button class="knopf zu" type="button">' + T("Zurück") + '</button></div>' +
        '<p class="raetsel-auftrag"></p><ul class="befund-zeilen"></ul>' +
        '<div class="raetsel-knoepfe"><button class="knopf haupt uebernehmen" type="button">' + T("In die Mappe") + '</button></div></div>';
      document.body.appendChild(hof);
      hof.querySelector(".zu").addEventListener("click", function () {
        hof.classList.remove("an"); global.Szene.sperre(false); global.Szene.aktualisiere();
      });
      hof.querySelector(".uebernehmen").addEventListener("click", function () {
        hof.classList.remove("an"); global.Szene.sperre(false);
        var f = hof.__fertig; hof.__fertig = null;
        if (f) f();
      });
      document.addEventListener("keydown", function (e) {
        if (!hof.classList.contains("an")) return;
        if (e.key === "Enter" || e.key === " ") { e.preventDefault(); hof.querySelector(".uebernehmen").click(); }
        else if (e.key === "Escape") { e.preventDefault(); hof.querySelector(".zu").click(); }
      });
    }
    hof.__fertig = opt.fertig || null;
    hof.querySelector("h2").textContent = T(opt.titel, opt.vars);
    hof.querySelector(".raetsel-auftrag").textContent = T(opt.text || "", opt.vars);
    hof.querySelector(".befund-zeilen").innerHTML = opt.zeilen.map(function (z) {
      return "<li>" + T(z, opt.vars) + "</li>";
    }).join("");
    hof.querySelector(".uebernehmen").textContent = T(opt.knopf || "In die Mappe");
    hof.classList.add("an");
    global.Szene.sperre(true);
    try { hof.querySelector(".uebernehmen").focus({ preventScroll: true }); } catch (x) {}
  }

  global.Fenster = { start: start, frage: frage, waehle: waehle, befundzeilen: befundzeilen };
})(window);
