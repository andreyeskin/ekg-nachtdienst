/* Dialogsystem: Gespräche als Daten. Knoten mit Sprecher, Text, Antworten,
   Bedingungen (wenn) und Wirkungen (tu). Schreibmaschine, Überspringen per
   Klick, Tastatur: Leertaste/Enter weiter, Ziffern wählen eine Antwort.      */
(function (global) {
  "use strict";

  var baeume = {}, portraits = {}, namen = {};
  var hof = null, feldPortrait = null, feldName = null, feldText = null, feldAntw = null;
  var aktiv = null, tippt = null, volltext = "", beiEnde = null;

  function bau() {
    hof = document.createElement("div");
    hof.className = "dialog";
    hof.innerHTML =
      '<div class="dialog-innen">' +
      '  <div class="dialog-kopf"><div class="dialog-bild"></div>' +
      '    <div class="dialog-name"></div></div>' +
      '  <div class="dialog-text"></div>' +
      '  <div class="dialog-antworten"></div>' +
      '</div>';
    document.body.appendChild(hof);
    feldPortrait = hof.querySelector(".dialog-bild");
    feldName = hof.querySelector(".dialog-name");
    feldText = hof.querySelector(".dialog-text");
    feldAntw = hof.querySelector(".dialog-antworten");
    hof.addEventListener("click", function (e) {
      if (e.target.closest(".dialog-antwort")) return;
      if (tippt) fertigTippen(); else if (aktiv && aktiv.weiterKnopf) weiter();
    });
    document.addEventListener("keydown", function (e) {
      if (!hof.classList.contains("an")) return;
      if (e.key === " " || e.key === "Enter") {
        e.preventDefault();
        if (tippt) fertigTippen(); else if (aktiv && aktiv.weiterKnopf) weiter();
      } else if (/^[1-9]$/.test(e.key)) {
        var k = feldAntw.getElementsByClassName("dialog-antwort")[+e.key - 1];
        if (k) k.click();
      } else if (e.key === "Escape" && aktiv && aktiv.abbrechbar) schliesse();
    });
  }

  function lade(daten) {
    baeume = daten.baeume || {};
    portraits = daten.portraits || {};
    namen = daten.namen || {};
  }

  function tippe(text) {
    volltext = text;
    feldText.textContent = "";
    var i = 0;
    clearInterval(tippt);
    tippt = setInterval(function () {
      i += 1;
      feldText.textContent = text.slice(0, i);
      if (i >= text.length) fertigTippen();
    }, 16);
    feldAntw.classList.remove("an");
  }

  function fertigTippen() {
    clearInterval(tippt); tippt = null;
    feldText.textContent = volltext;
    feldAntw.classList.add("an");
  }

  function zeigeKnoten(baum, id) {
    var k = baeume[baum] && baeume[baum][id];
    if (!k) { schliesse(); return; }
    aktiv = { baum: baum, id: id, weiterKnopf: null, abbrechbar: !!k.abbrechbar };
    /* Erst den Text bilden, dann die Wirkung auslösen — sonst beschreibt der
       Knoten einen Zustand, den er selbst gerade erst hergestellt hat. */
    var inhalt = typeof k.text === "function" ? k.text() : T(k.text);
    if (k.tu) k.tu();
    var wer = k.wer || baum;
    feldPortrait.innerHTML = portraits[wer] || "";
    feldName.textContent = T(namen[wer] || "");
    hof.classList.add("an");
    hof.classList.toggle("ohne-bild", !portraits[wer]);
    tippe(inhalt);

    feldAntw.innerHTML = "";
    var moegliche = (k.antworten || []).filter(function (a) { return !a.wenn || a.wenn(); });
    if (moegliche.length) {
      moegliche.forEach(function (a, i) {
        var b = document.createElement("button");
        b.className = "dialog-antwort";
        b.innerHTML = '<span class="nr">' + (i + 1) + '</span>' +
                      (typeof a.text === "function" ? a.text() : T(a.text));
        b.addEventListener("click", function (ev) {
          ev.stopPropagation();
          if (tippt) { fertigTippen(); return; }
          if (a.tu) a.tu();
          if (a.zu) zeigeKnoten(a.baum || baum, a.zu); else schliesse();
        });
        feldAntw.appendChild(b);
      });
    } else if (k.weiter) {
      aktiv.weiterKnopf = { baum: k.weiterBaum || baum, id: k.weiter };
      var w = document.createElement("button");
      w.className = "dialog-antwort weiter";
      w.textContent = T("Weiter");
      w.addEventListener("click", function (ev) { ev.stopPropagation(); weiter(); });
      feldAntw.appendChild(w);
    } else {
      aktiv.weiterKnopf = { ende: true };
      var s = document.createElement("button");
      s.className = "dialog-antwort weiter";
      s.textContent = T(k.endeText || "Danke.");
      s.addEventListener("click", function (ev) { ev.stopPropagation(); weiter(); });
      feldAntw.appendChild(s);
    }
  }

  function weiter() {
    var w = aktiv && aktiv.weiterKnopf;
    if (!w) return;
    if (w.ende) schliesse(); else zeigeKnoten(w.baum, w.id);
  }

  function schliesse() {
    clearInterval(tippt); tippt = null;
    hof.classList.remove("an");
    aktiv = null;
    if (global.Szene) { global.Szene.sperre(false); global.Szene.aktualisiere(); }
    if (beiEnde) { var f = beiEnde; beiEnde = null; f(); }
  }

  function starte(baum, id, fertig) {
    if (!hof) bau();
    beiEnde = fertig || null;
    if (global.Szene) global.Szene.sperre(true);
    zeigeKnoten(baum, id || "start");
  }

  global.Dialog = {
    lade: lade, starte: starte, schliesse: schliesse,
    laeuft: function () { return !!aktiv; }
  };
})(window);
