/* Mini-Spiel „Ampel am Monitor": eine Lage, drei Handlungen, etwa zehn Sekunden.
   Grün beobachten · Gelb Arzt rufen · Rot Pacer vorbereiten.

   Zeitdruck gehört hier zur Sache (LEHRPLAN 5, Regel 7) — aber ohne Strafe.
   Was immer gewählt wird, auch nichts, führt in eine Szene, nie in ein Game
   Over. Die Uhr läuft erst, wenn man die Lage gelesen und „Los" getippt hat;
   vorher drängt nichts. Der Balken schrumpft gleichmäßig, nichts blinkt.

   Was richtig ist und warum, sagt nicht dieses Fenster, sondern die Szene
   danach (fertig(id) — id ist null, wenn die Zeit abgelaufen ist).          */
(function (global) {
  "use strict";

  var hof = null, S = null, schirm = null, uhr = null, ende = 0, phase = 0, nachlauf = null;

  function bau() {
    hof = document.createElement("div");
    hof.className = "raetsel ampel";
    hof.id = "ampel-hof";
    hof.innerHTML =
      '<div class="raetsel-innen">' +
      '  <div class="raetsel-kopf"><h2></h2><button class="knopf zu" type="button">' + T("Zurück") + '</button></div>' +
      '  <p class="ampel-lage"></p>' +
      '  <figure class="schirm ampel-schirm"><figcaption class="schirm-kopf"><span class="schirm-name"></span>' +
      '    <span class="schirm-info"></span></figcaption><canvas height="130"></canvas></figure>' +
      '  <div class="ampel-start">' +
      '    <p class="ampel-hinweis"></p>' +
      '    <div class="raetsel-knoepfe"><button class="knopf haupt ampel-los" type="button">' + T("Los") + '</button></div>' +
      '  </div>' +
      '  <div class="ampel-entscheidung" hidden>' +
      '    <p class="ampel-frage"></p>' +
      '    <div class="ampel-zeit"><div class="ampel-balken"></div></div>' +
      '    <p class="ampel-sek" aria-live="off"></p>' +
      '    <div class="ampel-wahl"></div>' +
      '    <div class="rueck"></div>' +
      '  </div>' +
      '</div>';
    document.body.appendChild(hof);
    hof.querySelector(".zu").addEventListener("click", function () {
      var ab = S && S.abbruch;
      schliesse();
      if (ab) ab();
    });
    hof.querySelector(".ampel-los").addEventListener("click", los);
    document.addEventListener("keydown", taste);
  }

  function offen() { return !!hof && hof.classList.contains("an"); }

  function taste(e) {
    if (!offen()) return;
    if (e.key === "Escape") { e.preventDefault(); hof.querySelector(".zu").click(); return; }
    if (phase === 1 && (e.key === "Enter" || e.key === " ")) { e.preventDefault(); los(); return; }
    if (phase === 2 && /^[1-9]$/.test(e.key)) {
      var k = hof.querySelectorAll(".ampel-wahl .knopf")[+e.key - 1];
      if (k && !k.disabled) { e.preventDefault(); k.click(); }
    }
  }

  function los() {
    if (phase !== 1) return;
    phase = 2;
    hof.querySelector(".ampel-start").hidden = true;
    hof.querySelector(".ampel-entscheidung").hidden = false;
    var balken = hof.querySelector(".ampel-balken");
    balken.style.transition = "none";
    balken.style.width = "100%";
    void balken.offsetWidth;                                 /* Übergang neu ansetzen */
    balken.style.transition = "width " + S.sekunden + "s linear";
    balken.style.width = "0%";
    ende = Date.now() + S.sekunden * 1000;
    tick();
    uhr = global.setInterval(tick, 200);
    /* Auf kleinen Schirmen liegen die Knöpfe sonst unter dem Rand — sichtbar machen, ohne Schwung. */
    try { hof.querySelector(".ampel-entscheidung").scrollIntoView({ block: "nearest" }); } catch (x) {}
    var erster = hof.querySelector(".ampel-wahl .knopf");
    if (erster) { try { erster.focus({ preventScroll: true }); } catch (x) { erster.focus(); } }
  }

  function tick() {
    var rest = Math.max(0, Math.ceil((ende - Date.now()) / 1000));
    hof.querySelector(".ampel-sek").textContent = T("noch {s} s", { s: rest });
    if (Date.now() >= ende) abgelaufen();
  }

  function anhalten() {
    global.clearInterval(uhr); uhr = null;
    var balken = hof.querySelector(".ampel-balken");
    var b = global.getComputedStyle(balken).width;
    balken.style.transition = "none";
    balken.style.width = b;
  }

  function sperreWahl() {
    Array.prototype.forEach.call(hof.querySelectorAll(".ampel-wahl .knopf"), function (k) { k.disabled = true; });
  }

  function abgelaufen() {
    if (phase !== 2) return;
    phase = 3;
    anhalten();
    sperreWahl();
    hof.querySelector(".ampel-balken").style.width = "0%";
    hof.querySelector(".ampel-sek").textContent = T("noch {s} s", { s: 0 });
    var r = hof.querySelector(".rueck");
    r.className = "rueck fast";
    r.innerHTML = "<strong>" + T("Die Zeit ist um.") + "</strong> " + T("Nichts zu tun ist auch eine Entscheidung.");
    nachlauf = global.setTimeout(function () { beende(null); }, 1600);
  }

  function waehle(w, knopf) {
    if (phase !== 2) return;
    phase = 3;
    anhalten();
    sperreWahl();
    knopf.classList.add("gewaehlt");
    var r = hof.querySelector(".rueck");
    r.className = "rueck";
    r.innerHTML = "<strong>" + T(w.text) + ".</strong> " + T(S.danach || "");
    nachlauf = global.setTimeout(function () { beende(w.id); }, 1100);
  }

  function beende(id) {
    var f = S.fertig;
    schliesse();
    if (f) f(id);
  }

  function starte(opt) {
    if (!hof) bau();
    S = opt;
    S.sekunden = S.sekunden || 10;
    phase = 1;
    global.clearTimeout(nachlauf);
    hof.querySelector("h2").textContent = T(S.titel);
    hof.querySelector(".ampel-lage").textContent = T(S.lage);
    hof.querySelector(".ampel-hinweis").textContent =
      T(S.hinweis || "Wenn du „Los“ tippst, hast du etwa {s} Sekunden.", { s: S.sekunden });
    hof.querySelector(".ampel-frage").textContent = T(S.frage);
    hof.querySelector(".ampel-start").hidden = false;
    hof.querySelector(".ampel-entscheidung").hidden = true;
    hof.querySelector(".ampel-sek").textContent = "";
    var r = hof.querySelector(".rueck");
    r.className = "rueck"; r.innerHTML = "";
    var balken = hof.querySelector(".ampel-balken");
    balken.style.transition = "none"; balken.style.width = "100%";

    var feld = hof.querySelector(".ampel-wahl");
    feld.innerHTML = "";
    S.wahl.forEach(function (w, i) {
      var b = document.createElement("button");
      b.type = "button";
      b.className = "knopf ampel-knopf " + (w.farbe || "");
      b.innerHTML = '<span class="ampel-kopf"><span class="nr"></span><span class="ampel-farbe"></span></span>' +
                    '<span class="ampel-was"></span><span class="ampel-wie"></span>';
      b.querySelector(".nr").textContent = String(i + 1);
      b.querySelector(".ampel-farbe").textContent = T(w.ampel || "");
      b.querySelector(".ampel-was").textContent = T(w.text);
      b.querySelector(".ampel-wie").textContent = T(w.wie || "");
      b.addEventListener("click", function () { waehle(w, b); });
      feld.appendChild(b);
    });

    hof.querySelector(".schirm-name").textContent = T(S.ekg.name || "");
    hof.querySelector(".schirm-info").textContent =
      T("Ableitung {lead} · 25 mm/s", { lead: (S.ekg.satz.sig.lead || "II").toUpperCase() });
    hof.classList.add("an");
    if (global.Szene) global.Szene.sperre(true);

    var lw = hof.querySelector("canvas");
    if (schirm) schirm.stoppeLauf();
    schirm = global.EKG.Streifen(lw, {
      werte: S.ekg.satz.sig.werte, fs: S.ekg.satz.sig.fs, mmProS: 25,
      von: S.ekg.von || 0, dauer: S.ekg.dauer || 5, monitor: true, kalibrierung: false
    });
    global.requestAnimationFrame(function () {
      if (!schirm) return;
      schirm.zeichne();
      schirm.starteLauf(1);
    });
  }

  function schliesse() {
    global.clearInterval(uhr); uhr = null;
    global.clearTimeout(nachlauf);
    if (schirm) { schirm.stoppeLauf(); schirm = null; }
    phase = 0;
    if (hof) hof.classList.remove("an");
    if (global.Szene) { global.Szene.sperre(false); global.Szene.aktualisiere(); }
  }

  global.Ampel = { starte: starte, schliesse: schliesse, offen: offen };
})(window);
