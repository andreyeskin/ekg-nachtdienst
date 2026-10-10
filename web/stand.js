/* „Stand der Schicht" — der Ersatz für den Fortschrittsbalken.

   Kein Prozentwert und keine Leiste: beides verrät, wie viel noch kommt, und
   macht aus einer Schicht eine Hausaufgabe. Stattdessen steht hier, was man
   getan hat und welche Fäden offen sind — in Sätzen, wie ein Dienstzettel.
   Die offenen Punkte nennen das Ziel, nie die Lösung.                        */
(function (global) {
  "use strict";

  var hof = null, Z = null, kapitel = null;

  function bau() {
    hof = document.createElement("div");
    hof.className = "raetsel stand";
    hof.id = "stand-hof";
    hof.innerHTML =
      '<div class="raetsel-innen schmal"><div class="raetsel-kopf"><h2>Stand der Schicht</h2>' +
      '<button class="knopf zu" type="button">Zurück</button></div>' +
      '<div class="stand-zeile"></div>' +
      '<h3 class="stand-ueber">Was du hast</h3><ul class="stand-liste hat"></ul>' +
      '<h3 class="stand-ueber">Was offen ist</h3><ul class="stand-liste offen"></ul>' +
      '<p class="stand-fuss"></p></div>';
    document.body.appendChild(hof);
    hof.querySelector(".zu").addEventListener("click", schliesse);
  }

  function liste(el, eintraege, leerText) {
    el.innerHTML = eintraege.length
      ? eintraege.map(function (t) { return "<li>" + t + "</li>"; }).join("")
      : '<li class="leer">' + leerText + "</li>";
  }

  function oeffne() {
    if (!hof) bau();
    var k = kapitel();
    hof.querySelector(".stand-zeile").innerHTML =
      '<span class="stand-uhr">' + k.zeit + "</span> · " + k.ort +
      ' · <span class="stand-kap">' + k.titel + "</span>";
    liste(hof.querySelector(".hat"), k.hat, "Noch nichts. Sieh dich um — oben „Was geht hier?" + "“ zeigt, was anklickbar ist.");
    liste(hof.querySelector(".offen"), k.offen, "Für dieses Kapitel nichts mehr.");
    hof.querySelector(".stand-fuss").textContent = k.fuss || "";
    hof.classList.add("an");
    if (global.Szene) global.Szene.sperre(true);
  }

  function schliesse() {
    if (hof) hof.classList.remove("an");
    if (global.Szene) { global.Szene.sperre(false); global.Szene.aktualisiere(); }
  }

  global.Stand = {
    start: function (zustand, kapitelFn) { Z = zustand; kapitel = kapitelFn; },
    oeffne: oeffne, schliesse: schliesse
  };
})(window);
