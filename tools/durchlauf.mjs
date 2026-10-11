/* Durchlauf durch Kapitel 1 und 2 in echtem Chromium.
   jsdom reicht hier nicht: Canvas, Zeigerereignisse, Layout und Animation
   sind genau das, was schiefgeht.

   Aufruf: node tools/durchlauf.mjs [spiel.html] [bilderordner]
   Ohne Angaben: bau/nachtdienst.html und bau/durchlauf/ in diesem Repository. */
import { starteBrowser } from "./browser.mjs";
import fs from "fs";
import { fileURLToPath } from "url";

const BAU = fileURLToPath(new URL("../bau/", import.meta.url));
const DATEI = process.argv[2] || BAU + "nachtdienst.html";
const BILDER = process.argv[3] || BAU + "durchlauf";
fs.mkdirSync(BILDER, { recursive: true });

const fehler = [], warnungen = [];
let n = 0;
const schritte = [];

function ok(was, bedingung, zusatz = "") {
  schritte.push((bedingung ? "  ok  " : "FEHLER") + "  " + was + (zusatz ? "  — " + zusatz : ""));
  if (!bedingung) fehler.push(was + (zusatz ? ": " + zusatz : ""));
}

const browser = await starteBrowser();
const seite = await browser.newPage({ viewport: { width: 1340, height: 900 }, deviceScaleFactor: 1 });
/* Der Durchlauf prüft die deutschen Sätze — Sprache vor dem Laden festlegen. */
await seite.addInitScript(() => {
  try {
    window.__spracheBeimStart = !!window.localStorage.getItem("nachtdienst-sprache");
    window.__ursprung = window.origin;
    if (!window.__spracheBeimStart) {
      window.localStorage.setItem("nachtdienst-sprache", "de");
    }
    /* Still vermerken, was beim Dokumentstart im Speicher lag — damit ein verlorener Spielstand beim
       Neuladen (selten beobachtet, Herr Baum auf Bett 1) sich im Fehlertext selbst erklärt. */
    window.__speicherBeimStart = (window.localStorage.getItem("nachtdienst-1") || "").length;
  } catch (e) {}
});
seite.on("console", (m) => { if (m.type() === "error") fehler.push("Konsole: " + m.text().slice(0, 160)); });
seite.on("pageerror", (e) => fehler.push("Seitenfehler: " + String(e).slice(0, 200)));

/* Bricht ein Schritt ab (Zeitüberschreitung o. ä.), trotzdem alles Bisherige
   ausgeben und ein Bild vom Zustand machen — sonst sieht man nur den Stapel. */
let abgebrochen = false;
function abbruch(e) {
  if (abgebrochen) return;
  abgebrochen = true;
  console.log(schritte.join("\n"));
  if (fehler.length) console.log("\nBIS DAHIN GESAMMELT:\n - " + fehler.join("\n - "));
  console.log("\nABBRUCH: " + String((e && e.message) || e).split("\n")[0]);
  seite.screenshot({ path: `${BILDER}/abbruch.png` }).catch(() => {}).finally(() => process.exit(1));
}
process.on("uncaughtException", abbruch);
process.on("unhandledRejection", abbruch);

async function schuss(name) {
  n++;
  await seite.screenshot({ path: `${BILDER}/${String(n).padStart(2, "0")}_${name}.png` });
}
const warte = (ms) => seite.waitForTimeout(ms);

await seite.goto("file://" + DATEI);
await warte(900);

/* ---------------------------------------------------------- 1 Auftakt */
ok("Seite lebt", await seite.locator("#buehne").isVisible());
/* Gerenderte Räume haben keinen Vordergrund (nichts steht vor der Kamera); Hintergrund, Mittelgrund und
   Figuren müssen gezeichnet sein. */
for (const n of ["hintergrund", "mittelgrund", "figuren"])
  ok("Ebene " + n + " gezeichnet", (await seite.locator("#buehne .ebene-" + n + " svg").count()) === 1);
ok("Uhrzeiger in der Hintergrund-Ebene", (await seite.locator("#buehne .ebene-hintergrund svg #uhr-std").count()) === 1);
ok("Hotspots vorhanden", (await seite.locator(".feld").count()) >= 6);
ok("Auftakt-Dialog erscheint", await seite.locator(".dialog.an").isVisible());
/* Die Erzählstimme hat kein Porträt und keinen Namen — sie beschreibt Marlene, statt Marlene zu sein. */
ok("Auftakt: Erzähler ohne Porträt und ohne Namensschild", await seite.evaluate(() => {
  const d = document.querySelector(".dialog.an");
  return d.classList.contains("ohne-bild") && !d.querySelector(".dialog-bild svg") &&
         !d.querySelector(".dialog-name").textContent.trim();
}));
/* Bildschirme: auf dem EKG-Wagen läuft Herrn Baums Aufnahme aus data/ (Leinwand in der Mittelgrund-Ebene),
   Marlenes Verwaltungs-PC zeigt keine Kurve — in der Aufnahme gibt es genau diese eine Leinwand. */
const schirme1 = await seite.evaluate(() => window.Spiel.__schirme());
ok("EKG-Wagen: laufende Kurve aus data/", schirme1.length === 1 && schirme1[0].name === "wagen_schirm" &&
   schirme1[0].satz === 39 && schirme1[0].laeuft, JSON.stringify(schirme1));
ok("EKG-Wagen: Leinwand in der Mittelgrund-Ebene",
   (await seite.locator("#buehne .ebene-mittelgrund .schirm-lauf[data-schirm=wagen_schirm] canvas").count()) === 1);
ok("Marlenes PC zeigt kein EKG", (await seite.locator("#buehne .schirm-lauf").count()) === 1);
await schuss("auftakt");

async function dialogDurch(maxKlicks = 14) {
  for (let i = 0; i < maxKlicks; i++) {
    if (!(await seite.locator(".dialog.an").count())) return;
    await seite.locator(".dialog-text").click();          // Tippen überspringen
    await warte(140);
    /* War der Text schon fertig, hat dieser Klick bei einem Endknopf-Knoten bereits „weiter“ ausgelöst. */
    if (!(await seite.locator(".dialog.an").count())) return;
    const w = seite.locator(".dialog-antwort.weiter");
    if (await w.count()) { await w.first().click(); await warte(280); continue; }
    const a = seite.locator(".dialog-antwort");
    if ((await a.count()) === 1) { await a.first().click(); await warte(280); continue; }
    return;                                               // echte Wahl: nicht raten
  }
}
await dialogDurch();
ok("Auftakt beendet", (await seite.locator(".dialog.an").count()) === 0);
ok("Nach dem Auftakt leuchten die Klickfelder einmal von selbst auf",
   await seite.evaluate(() => document.querySelector(".felder").classList.contains("zeigen")));

/* Antwort im laufenden Dialog wählen (Text muss enthalten sein) */
async function antworte(teil) {
  await seite.locator(".dialog-text").click();
  await warte(120);
  const knopf = seite.locator(".dialog-antwort", { hasText: teil });
  if (!(await knopf.count())) return false;
  await knopf.first().click();
  await warte(320);
  return true;
}
const feld = (id) => seite.locator(`.feld[data-feld="${id}"]`);

/* -------------------------------------------- 1b Stand ganz am Anfang */
await seite.locator("#kopf-stand").click();
await warte(400);
ok("Stand öffnet sich", await seite.locator("#stand-hof.an").isVisible());
const offen0 = await seite.locator("#stand-hof .offen li").allTextContents();
ok("Stand nennt am Anfang offene Punkte", offen0.length >= 3, offen0.length + " Punkte");
ok("Stand verrät die Lösung nicht",
   !offen0.join(" ").match(/228|Block|Bisoprolol|AV-/), offen0.join(" | ").slice(0, 120));
await schuss("stand_anfang");
await seite.locator("#stand-hof .zu").click();
await warte(300);

/* ---------------------------------------------------------- 2 Marlene */
await feld("marlene").click();
await warte(450);
ok("Marlene spricht", await seite.locator(".dialog.an").isVisible());
const gruss = await dialogLesen();                     /* erst fertig tippen lassen, dann lesen */
ok("Erstbegrüßung, nicht die Wiederholung", gruss.includes("Famulantin"), gruss.slice(0, 60));
ok("Porträt im Dialog", (await seite.locator(".dialog-bild svg").count()) === 1);
await schuss("marlene");
ok("Frage nach dem Fall", await antworte("Was ist passiert"));
ok("Nachfrage ohne Vorwarnung", await antworte("Ohne Vorwarnung"));
ok("Nachfrage nach dem Beweiswert", await antworte("Beweist das etwas"));
await seite.locator(".dialog-text").click();   // Schreibmaschine überspringen
await warte(200);
const streng = (await seite.locator(".dialog-text").textContent()) || "";
ok("Antwort nennt die harten Kriterien, nicht nur ein Gefühl (Puls unter 40, Pause über 3 s, plötzlicher Ausfall)",
   /unter vierzig/.test(streng) && /drei Sekunden/.test(streng) && /plötzlich/.test(streng), streng.slice(0, 80));
await antworte("Verstanden");
await dialogDurch();
ok("Auftrag gesetzt", await seite.evaluate(() => window.Spiel.hat("auftrag_ekg")));

/* ---------------------------------------------------------- 3 EKG schreiben */
const wagen = feld("wagen");
await wagen.click();
await warte(500);
ok("Rhythmusfrage erscheint", await seite.locator("#frage-hof.an").isVisible());
ok("EKG in der Frage gezeichnet", (await seite.locator("#frage-hof canvas").count()) === 1);
await schuss("rhythmusfrage");
/* Die Antworten sind bloße Diagnosen; die Kriterien tragen die Rückmeldungen (Fachabgleich, Lektion 8, 25, 26). */
ok("Rhythmusfrage: Antworten ohne Spickzettel (keine Kriterien im Antworttext)",
   (await seite.locator("#frage-hof .wahl").allTextContents()).every((t) => !/P-Welle|regelmäßig|breite|schnell/.test(t)));
await seite.locator("#frage-hof .wahl", { hasText: "Vorhofflimmern" }).click();
await warte(300);
const rFlimmern = (await seite.locator("#frage-hof .rueck").textContent()) || "";
ok("Falsch „Vorhofflimmern“: beide Kriterien genannt und am Streifen widerlegt",
   /keine P-Wellen/.test(rFlimmern) && /unregelmäßig/.test(rFlimmern) && /vor jedem QRS eine P-Welle/.test(rFlimmern),
   rFlimmern.slice(0, 100));
await warte(2300);                                            /* Knöpfe wieder frei */
await seite.locator("#frage-hof .wahl", { hasText: "Sinusrhythmus" }).click();
await warte(300);
const rSinus = (await seite.locator("#frage-hof .rueck").textContent()) || "";
ok("Richtig „Sinusrhythmus“: P vor jedem QRS, normal geformt, gleiche Abstände; Frequenz bleibt dem Zirkel",
   /Vor jedem QRS eine P-Welle/.test(rSinus) && /normal geformt/.test(rSinus) && /Abstände bleiben gleich/.test(rSinus) &&
   /Zirkel/.test(rSinus), rSinus.slice(0, 120));
await warte(3000);
ok("Nichts schließt sich von allein: Fenster nach 3 s noch offen, „Weiter“ sichtbar",
   (await seite.locator("#frage-hof.an").count()) === 1 && await seite.locator("#frage-hof .weiter").isVisible());
ok("Kein Befund, bevor „Weiter“ getippt ist", !(await seite.evaluate(() => window.Mappe.hat("b-rhythmus"))));
await seite.keyboard.press("Enter");                          /* Eingabe führt weiter */
await warte(400);
ok("Befund Rhythmus in der Mappe", await seite.evaluate(() => window.Mappe.hat("b-rhythmus")));

/* ---------------------------------------------------------- 4 Zirkel: RR */
await wagen.click();
await warte(400);
ok("Messwahl erscheint", await seite.locator("#wahl-hof.an").isVisible());
await seite.locator("#wahl-hof .wahl", { hasText: "RR-Abstand" }).click();
await warte(600);
ok("Zirkel offen", await seite.locator("#zirkel-hof.an").isVisible());
await schuss("zirkel_rr");

/* Zieht den Zirkel über eine echte Strecke aus der Annotation. */
async function messe(vonSek, bisSek) {
  const geo = await seite.evaluate(() => {
    const hof = document.getElementById("zirkel-hof");
    const lw = hof.querySelector("canvas");
    const r = lw.getBoundingClientRect();
    return { x: r.left, y: r.top, h: r.height, s: hof.__streifen.stand.von };
  });
  const xv = await seite.evaluate((s) => document.getElementById("zirkel-hof").__streifen.sekundeZuX(s), vonSek);
  const xb = await seite.evaluate((s) => document.getElementById("zirkel-hof").__streifen.sekundeZuX(s), bisSek);
  const y = geo.y + geo.h / 2;
  await seite.mouse.move(geo.x + xv, y);
  await seite.mouse.down();
  await seite.mouse.move(geo.x + (xv + xb) / 2, y, { steps: 4 });
  await seite.mouse.move(geo.x + xb, y, { steps: 4 });
  await seite.mouse.up();
  await warte(350);
}

const wahrheit = await seite.evaluate(() => {
  const s = window.Spiel.satz(39).schlaege;
  return { r1: s[2].r, r2: s[3].r, p0: s[3].p0, q0: s[3].q0, q1: s[3].q1 };
});
await messe(wahrheit.r1, wahrheit.r2);
ok("RR richtig gemessen", await seite.locator("#zirkel-hof .rueck.gut").isVisible(),
   (await seite.locator("#zirkel-hof .rueck").textContent() || "").slice(0, 110));
await schuss("zirkel_rr_richtig");
await seite.locator("#zirkel-hof .uebernehmen").click();
await warte(400);
ok("Befund Frequenz in der Mappe", await seite.evaluate(() => window.Mappe.hat("b-frequenz")));
/* Lehrbuch Lektion 8: Norm 50–100/min, Sinusbradykardie erst unter 50 — nirgends mehr „unter 60“. */
const karteHf = await seite.evaluate(() => window.Spiel.zustand.befunde.filter((b) => b.id === "b-frequenz")[0].text);
ok("Frequenz-Karte: Norm 50–100, Grenze der Sinusbradykardie bei 50",
   /50–100/.test(karteHf) && /unter 50/.test(karteHf) && !/60–100|unter 60/.test(karteHf), karteHf.slice(-90));

/* ---------------------------------------------------------- 5 Zirkel: PQ, erst falsch */
await wagen.click(); await warte(400);
await seite.locator("#wahl-hof .wahl", { hasText: "PQ-Zeit" }).click();
await warte(600);
await messe(wahrheit.q0, wahrheit.q1);                     /* QRS statt PQ gemessen */
const meckern = (await seite.locator("#zirkel-hof .rueck").textContent()) || "";
ok("Falsche Strecke wird erkannt", /andere Strecke|zu spät|zu früh/.test(meckern), meckern.slice(0, 110));
await schuss("zirkel_pq_falsch");
await seite.locator("#zirkel-hof .nochmal").click();
await warte(250);
await messe(wahrheit.p0, wahrheit.q0);
ok("PQ richtig gemessen", await seite.locator("#zirkel-hof .rueck.gut").isVisible(),
   (await seite.locator("#zirkel-hof .rueck").textContent() || "").slice(0, 110));
await schuss("zirkel_pq_richtig");
await seite.locator("#zirkel-hof .uebernehmen").click();
await warte(400);
ok("Befund PQ in der Mappe", await seite.evaluate(() => window.Mappe.hat("b-pq")));

/* ---------------------------------------------------------- 6 Mappe und Vergleich */
await seite.locator("#kopf-mappe").click();
await warte(600);
ok("Mappe offen mit drei Karten", (await seite.locator(".mappe .karte").count()) === 3);
ok("EKG auf den Karten", (await seite.locator(".mappe .karte-ekg").count()) >= 2);
await schuss("mappe");
await seite.locator(".mappe .karte").nth(1).click();
await seite.locator(".mappe .karte").nth(2).click();
await warte(200);
ok("Vergleichen freigeschaltet", await seite.locator(".mappe .vergleich").isEnabled());
await seite.locator(".mappe .vergleich").click();
await warte(700);
ok("Zwei Karten nebeneinander", (await seite.locator(".mappe-vergleich.an canvas").count()) === 2);
await schuss("vergleich");
await seite.locator(".mappe .zu").click();
await warte(300);

/* ---------------------------------------------------------- 7 Dialog mit Bedingung */
/* Ohne Marlenes Bericht bleibt der Flur zu — auch mit drei Befunden in der Mappe. */
await seite.locator("#buehne .felder polygon.ausgang").first().click();
await warte(400);
ok("Flur vor dem Bericht an Marlene gesperrt", await seite.evaluate(() => window.Szene.aktueller() === "aufnahme"));
ok("Sperrmeldung sagt, wer anmeldet", /Marlene/.test((await seite.locator(".meldung").last().textContent()) || ""));
await feld("marlene").click();
await warte(450);
await seite.locator(".dialog-text").click();
await warte(150);
ok("Antwort erscheint erst mit Befund",
   (await seite.locator(".dialog-antwort", { hasText: "Ich hab gemessen" }).count()) === 1);
const gemessen = await seite.evaluate(() => window.Spiel.zustand.werte.pq);
const hfGemessen = await seite.evaluate(() => window.Spiel.zustand.werte.hf);
const berichtKnopf = (await seite.locator(".dialog-antwort", { hasText: "Ich hab gemessen" }).textContent()) || "";
ok("Dialog nennt die selbst gemessenen Werte",
   berichtKnopf.includes(String(gemessen)) && berichtKnopf.includes(String(hfGemessen)), "gemessen: " + hfGemessen + " / " + gemessen);
await seite.locator(".dialog-antwort", { hasText: "Ich hab gemessen" }).click();
await warte(400);
const bericht = await dialogLesen();
ok("Marlene: Monitor begründet, Dr. Falk entscheidet, die zwei Stunden sind erklärt",
   /Monitor/.test(bericht) && /Falk/.test(bericht) && /gegen neun/.test(bericht), bericht.slice(-100));
await dialogDurch();
ok("Monitorzimmer freigegeben", await seite.evaluate(() => window.Spiel.hat("monitor_frei")));

/* -------------------------------------------- 7b Stand mit drei Befunden */
await seite.locator("#kopf-stand").click();
await warte(400);
const habe = await seite.locator("#stand-hof .hat li").allTextContents();
ok("Stand zählt die Befunde auf", habe.length >= 3, habe.length + " Einträge");
const offen1 = await seite.locator("#stand-hof .offen li").allTextContents();
ok("Stand weist auf das Monitorzimmer hin",
   /Flur|Monitorzimmer/.test(offen1.join(" ")), offen1.join(" | ").slice(0, 120));
ok("Stand nennt Marlenes Schema — ausdrücklich keine Pflicht", /Keine Pflicht/.test(offen1.join(" ")));
await schuss("stand_mitte");
await seite.locator("#stand-hof .zu").click();
await warte(300);

/* -------------------------------------------- 7c Rätsel „Reizleitung bauen" */
await feld("marlene").click();
await warte(450);
ok("Marlene bietet ihr Schema an — nach der PQ-Messung als Frage nach den Millisekunden",
   await antworte("zwischen P und QRS"));
ok("Marlene knüpft an die gemessene PQ-Zeit an", /wo sie bleiben/.test(await dialogLesen()));
ok("Schema öffnet sich", await antworte("Zeig her"));
await warte(500);
const rl = (sel) => seite.locator("#reizleitung-hof " + sel);
ok("Reizleitung offen", await seite.locator("#reizleitung-hof.an").isVisible());
ok("Herzschema aus kunst.json", (await rl(".rl-herz svg.schema-herz").count()) === 1);
ok("Kein Text im Herzbild", (await rl("svg.schema-herz text").count()) === 0);
ok("Fünf Bauteile, sieben Plätze",
   (await rl(".rl-teil").count()) === 5 && (await rl(".rl-platz").count()) === 7);
const kleinste = await seite.evaluate(() => {
  const hof = document.getElementById("reizleitung-hof");
  const masse = [...hof.querySelectorAll("button:not([hidden]), .rl-platz .rl-treffer")].map((e) => {
    const r = e.getBoundingClientRect(); return Math.min(r.width, r.height);
  });
  return Math.round(Math.min(...masse));
});
ok("Alles Antippbare mindestens 44 px", kleinste >= 44, kleinste + " px");
const tabelle = await seite.evaluate(() => window.Reizleitung.__pruefeTabelle());
ok("Fall-Tabelle passt zu den Daten (Rhythmus, PQ, QRS je Aufnahme)",
   tabelle.length >= 5 && tabelle.every((z) => z.da && z.passt),
   tabelle.map((z) => z.fall + ":" + z.aufnahme + (z.passt ? "" : "!")).join(" "));
ok("Jede Zeile der Fall-Tabelle nennt ihre Lehrbuchlektion (im Code, nicht im Spieltext)",
   await seite.evaluate(() => Object.keys(window.Reizleitung.FAELLE).every((k) => typeof window.Reizleitung.FAELLE[k].lektion === "string")));
/* Lehrbuch Lektion 1 und 14: der linke Schenkel teilt sich in zwei Faszikel — rechts, Stamm, hinten, vorn. */
const bahnen = await seite.evaluate(() => window.KUNST.schemata.herz_geo.teile.schenkel.bahnen.length);
ok("Herzschema: linker Schenkel in zwei Faszikel geteilt (vier Schenkelbahnen)", bahnen === 4, String(bahnen));
await schuss("reizleitung_leer");

/* Setzt ein Bauteil (Ziffer oder Antippen) und wartet, bis Welle und Streifen durch sind. */
async function setzeTeil(teil, platz, mitTaste) {
  if (mitTaste) await seite.keyboard.press(String(["sinus", "av", "his", "schenkel", "purkinje"].indexOf(teil) + 1));
  else await rl(`.rl-teil[data-teil="${teil}"]`).click();
  await rl(`.rl-platz[data-platz="${platz}"]`).click();
  await seite.waitForSelector('#reizleitung-hof .rl-herz[data-bereit="ja"]', { timeout: 15000 });
  await warte(200);
  return seite.evaluate(() => {
    const hof = document.getElementById("reizleitung-hof"), z = window.Reizleitung.zustand();
    const sp = hof.__streifen && hof.__streifen.stand.zirkel;
    return { fall: z.fall, aufnahme: z.aufnahme,
             ms: sp ? Math.round((sp.ende - sp.start) * 1000) : null,
             unter: hof.querySelector(".rl-unterschrift").textContent,
             rueck: hof.querySelector(".rl-rueck").textContent,
             streifen: !hof.querySelector(".rl-streifen").classList.contains("ohne") };
  });
}

/* Richtiger Aufbau, Schritt für Schritt — jeder Zwischenstand hat seine eigene echte Kurve. */
let st = await setzeTeil("sinus", "sinus", true);
ok("Nur Sinusknoten: kompletter Block, Schrittmacher-Aufnahme 74",
   st.fall === "block" && st.aufnahme === 74 && /AV-Block III/.test(st.rueck), st.fall + "/" + st.aufnahme);
ok("Block: Ersatzfrequenzen nach Lage des Blocks (40–60 schmal, 30–40 breit) und Schrittmacher benannt",
   /40–60/.test(st.rueck) && /30–40/.test(st.rueck) && /Schrittmacher/.test(st.rueck) && /schenkelblockartig/.test(st.rueck));
st = await setzeTeil("av", "av", true);
ok("Ohne His-Bündel weiterhin Block", st.fall === "block" && st.aufnahme === 74, st.fall + "/" + st.aufnahme);
st = await setzeTeil("his", "his");
ok("Ohne Schenkel: breiter QRS, Aufnahme 24 (Linksschenkelblock)",
   st.fall === "schenkel" && st.aufnahme === 24 && st.ms >= 120 && /Linksschenkelblock/.test(st.unter),
   st.fall + "/" + st.aufnahme + "/" + st.ms + " ms");
/* Die Datenbank nennt Nr. 24 „Sinusbradykardie“ (51/min); das Spiel ordnet das Etikett an seiner Grenze (50) ein. */
ok("Datenbank-Etikett „Sinusbradykardie“ bei 51/min wird eingeordnet, nicht übernommen",
   /Sinusbradykardie/.test(st.unter) && /unter 50/.test(st.rueck) && /nicht zum Modell/.test(st.rueck), st.rueck.slice(-140));
await schuss("reizleitung_ohne_schenkel");
st = await setzeTeil("schenkel", "schenkel");
ok("Ohne Purkinje: nächstliegende Aufnahme 59, ehrlich benannt",
   st.fall === "purkinje" && st.aufnahme === 59 && /Am nächsten kommt/.test(st.rueck), st.fall + "/" + st.aufnahme);
st = await setzeTeil("purkinje", "purkinje");
ok("Vollständig und richtig: Sinusrhythmus, Aufnahme 119",
   st.fall === "richtig" && st.aufnahme === 119 && /LUDB Nr\. 119/.test(st.unter) && /Sinusrhythmus/.test(st.unter),
   st.unter.slice(0, 90));
ok("Markierte PQ-Zeit im Normbereich", st.ms >= 120 && st.ms <= 200, st.ms + " ms");
ok("Lernziel im Text: richtige Anatomie, normales EKG", /Richtige Anatomie, normales EKG/.test(st.rueck));
ok("Kein Lehrbuchverweis im Spieltext (Lektionsnummern bleiben in Code und docs)", !/Lektion/.test(st.rueck), st.rueck.slice(0, 80));
ok("Alle vier Schenkelbahnen gezeichnet (rechts, Stamm, zwei Faszikel)",
   (await rl('.rl-teil-bild[data-teil="schenkel"] path.rl-strang').count()) === 4);
ok("Abschluss-Knopf erscheint", await rl(".rl-fertig").isVisible());
await schuss("reizleitung_richtig");

/* Fehlaufbau 1: AV-Knoten in den linken Vorhof — PQ über 200 ms (Herrn Baums Streifen). */
st = await setzeTeil("av", "linker_vorhof");
ok("AV-Knoten falsch: PQ > 200 ms, Aufnahme 39",
   st.fall === "av_umweg" && st.aufnahme === 39 && st.ms > 200 && /PQ über 200 ms/.test(st.rueck),
   st.fall + "/" + st.aufnahme + "/" + st.ms + " ms");
ok("Rückmeldung sagt, warum (und was im echten Herzen passiert)",
   /Umweg/.test(st.rueck) && /AV-Block I\. Grades/.test(st.rueck) && /Herrn Baum/.test(st.rueck));
await schuss("reizleitung_av_falsch");
await setzeTeil("av", "av");

/* Fehlaufbau 2: Sinusknoten heraus — Knotenersatzrhythmus (Lektion 11), keine annotierte Aufnahme, kein Streifen. */
await rl('.rl-teil[data-teil="sinus"]').click();
await rl(".rl-raus").click();
await seite.waitForSelector('#reizleitung-hof .rl-herz[data-bereit="ja"]', { timeout: 15000 });
st = await seite.evaluate(() => ({ ...window.Reizleitung.zustand(),
  rueck: document.querySelector("#reizleitung-hof .rl-rueck").textContent,
  unter: document.querySelector("#reizleitung-hof .rl-unterschrift").textContent }));
ok("Ohne Sinusknoten: Ersatzzentrum im AV-Übergang, kein Streifen (Lektion 11)",
   st.fall === "ohne_sinus" && st.aufnahme === null && /Ersatz/.test(st.rueck) && /kein Streifen/.test(st.rueck),
   st.fall + "/" + st.aufnahme);
await schuss("reizleitung_ohne_sinus");
await setzeTeil("sinus", "sinus");

/* Fehlaufbau 3: Schenkel auf den Klappenring — breiter QRS. */
st = await setzeTeil("schenkel", "klappenring");
ok("Schenkel falsch: QRS > 120 ms, Aufnahme 24", st.fall === "schenkel" && st.aufnahme === 24 && st.ms > 120,
   st.fall + "/" + st.aufnahme + "/" + st.ms + " ms");

await seite.keyboard.press("Escape");
await warte(300);
ok("Escape schließt das Rätsel", (await seite.locator("#reizleitung-hof.an").count()) === 0);
ok("Bühne danach wieder bedienbar",
   await seite.evaluate(() => !document.getElementById("buehne").classList.contains("stumm")));

/* ---------------------------------------------------------- 8 Raumwechsel */
const ausgang = seite.locator("#buehne .felder polygon.ausgang").first();
await ausgang.click();
await warte(1100);
ok("Im Monitorzimmer", await seite.evaluate(() => window.Szene.aktueller() === "monitor"));
ok("Monitorkurve läuft (großer Schirm, Papier)", (await seite.locator("#buehne .ebene-hintergrund .schirm-lauf[data-schirm=gross] canvas").count()) === 1);
/* Bettmonitore: drei Leinwände, je eine der drei Aufnahmen der Zentrale, in Bettenfolge, alle laufend */
const schirme2 = await seite.evaluate(() => window.Spiel.__schirme());
const bettenJetzt = await seite.evaluate(() => window.Spiel.__betten().map((b) => b.id));
const kleine = schirme2.filter((s) => /^bett_\d$/.test(s.name)).sort((a, b) => a.name < b.name ? -1 : 1);
ok("Bettmonitore: drei laufende Kurven in Bettenfolge",
   kleine.length === 3 && kleine.every((s, i) => s.laeuft && s.satz === bettenJetzt[i]) &&
   new Set(kleine.map((s) => s.satz)).size === 3, JSON.stringify(kleine) + " Betten " + bettenJetzt.join(","));
ok("Keine Leinwand der Aufnahme mehr aktiv", schirme2.every((s) => s.name !== "wagen_schirm"));
await warte(1600);
ok("Kapitelwechsel: der Erzähler erklärt die zweieinhalb Stunden, ohne Porträt",
   (await seite.locator(".dialog.an.ohne-bild").count()) === 1 && /Zweieinhalb Stunden/.test(await dialogLesen()));
await schuss("monitorzimmer");
await seite.locator(".dialog-antwort.weiter").click();
await warte(350);
ok("Dr. Falk spricht an", (await seite.locator(".dialog-bild svg").count()) === 1 && /Falk/.test(await dialogLesen()));
ok("Beste Antwort nur mit beiden Befunden",
   (await seite.locator(".dialog-antwort", { hasText: "Sinusrhythmus," }).count()) === 1);
await seite.locator(".dialog-antwort", { hasText: "Sinusrhythmus," }).click();
await warte(500);
/* Die Tüte wurde übersprungen: Falk fragt nach dem Medikament und reicht es aus dem Aufnahmebogen nach. */
ok("Falk fragt nach dem Medikament, das beides bremst",
   /Nimmt er etwas/.test(await dialogLesen()) && (await seite.locator(".dialog-antwort", { hasText: "Das weiß ich nicht" }).count()) === 1);
const textFalk = await dialogDurchLesen();
ok("Falk nennt das Bisoprolol aus dem Aufnahmebogen und behält den Beweis-Satz (plötzlich)",
   /Aufnahmebogen/.test(textFalk) && /Bisoprolol/.test(textFalk) && /plötzlich Schläge ausfallen/.test(textFalk), textFalk.slice(0, 120));
ok("Medikamentenkarte ohne Tüte: als Aufnahmebogen benannt",
   await seite.evaluate(() => { const b = window.Spiel.zustand.befunde.find((x) => x.id === "b-medis"); return !!b && /Aufnahmebogen/.test(b.titel); }));
ok("Falk: der Monitor ersetzt das Zwölfkanal-EKG nicht", /Zwölfkanal/.test(textFalk));
ok("Auftrag mit den drei Betten erst nach beiden Zahlen", await seite.evaluate(() => window.Spiel.hat("k2_auftrag")));
await schuss("nach_falk");

/* ---------------------------------------------------------- 9 Neu laden */
const gespeichert = await seite.evaluate(() => {
  try { const g = JSON.parse(window.localStorage.getItem("nachtdienst-1") || "null"); return g ? g.raum + "/" + g.befunde.length : "leer"; }
  catch (e) { return "kaputt: " + e; }
});
ok("Zustand vor dem Neuladen gespeichert (Raum/Befunde)", gespeichert === "monitor/4", gespeichert);
await seite.reload();
await warte(1200);
const nachLaden = await seite.evaluate(() => ({
  raum: window.Szene && window.Szene.aktueller(),
  befunde: window.Spiel && window.Spiel.zustand.befunde.length,
  dialogOffen: document.querySelectorAll(".dialog.an").length,
  dialog: ((document.querySelector(".dialog.an .dialog-text") || {}).textContent || "").slice(0, 60),
  zeichenBeimStart: window.__speicherBeimStart,
  spracheBeimStart: window.__spracheBeimStart,
  ursprung: window.__ursprung,
  betten: (window.Spiel.zustand.werte.betten || []).join(","),
  speicher: (() => { try { const g = JSON.parse(window.localStorage.getItem("nachtdienst-1") || "null"); return g ? g.raum + "/" + g.befunde.length : "leer"; } catch (e) { return "kaputt"; } })()
}));
/* Beobachtet (selten, Herr Baum auf Bett 1): Chromium reicht dem neu geladenen Dokument einen ganz leeren
   file://-Speicher — auch ohne den Sprachschlüssel, den nur dieser Durchlauf setzt und nichts löscht. Dann hat
   der Browser verworfen, nicht das Spiel. Die Prüfung bleibt streng; der Text sagt nur, wo man suchen muss. */
const browserVerwarf = nachLaden.zeichenBeimStart === 0 && nachLaden.spracheBeimStart === false;
ok("Zustand übersteht Neuladen", nachLaden.raum === "monitor",
   JSON.stringify(nachLaden) + (browserVerwarf
     ? " — Browser lieferte beim Neuladen einen leeren file://-Speicher (auch ohne Sprachschlüssel); vorher war gespeichert: " + gespeichert
     : ""));
ok("Befunde noch da", nachLaden.befunde === 4, String(nachLaden.befunde));
ok("Kein Auftakt bei Fortsetzung", nachLaden.dialogOffen === 0, nachLaden.dialog);
await schuss("nach_neuladen");

/* --------------------------------------------------- 9b Hotspots zeigen */
await seite.locator("#kopf-zeigen").click();
await warte(300);
ok("Hotspot-Hilfe schaltet sich ein", await seite.evaluate(
  () => document.querySelector(".felder").classList.contains("zeigen")));
await schuss("hotspots_gezeigt");

/* ================================================== Kapitel 2: Monitorzimmer
   Vier Wege durch dasselbe Kapitel, alle bis zum offenen Ende:
     A  Tastatur · erst zwei falsche Betten · Begründung PQ · Ampel: Arzt rufen
     B  großer Monitor · Begründung Frequenz · Ampel weggeklickt, über Dr. Falk
        wieder geholt · Zeit läuft ab
     C  Neubetreten nach dem Fund · Ampel: Pacer
     D  Neubetreten · Ampel weggeklickt, über den großen Monitor · Beobachten   */
await warte(2600);                                         /* Hotspot-Hilfe aus */

async function dialogLesen() {
  if (!(await seite.locator(".dialog-antworten.an").count())) {   /* tippt noch */
    await seite.locator(".dialog-text").click();
    await warte(120);
  }
  return (await seite.locator(".dialog-text").textContent()) || "";
}
/* Klickt einen Dialog bis zum Ende durch und sammelt Texte und Knöpfe. */
async function dialogDurchLesen(max = 16) {
  const texte = [];
  for (let i = 0; i < max; i++) {
    if (!(await seite.locator(".dialog.an").count())) break;
    texte.push(await dialogLesen());
    const w = seite.locator(".dialog-antwort.weiter");
    if (await w.count()) {
      texte.push("[" + ((await w.first().textContent()) || "").trim() + "]");
      await w.first().click(); await warte(300); continue;
    }
    const a = seite.locator(".dialog-antwort");
    if ((await a.count()) === 1) {
      texte.push("[" + ((await a.first().textContent()) || "").trim() + "]");
      await a.first().click(); await warte(300); continue;
    }
    break;
  }
  return texte.join(" | ");
}
const zustand = () => seite.evaluate(() => JSON.parse(JSON.stringify(window.Spiel.zustand)));
const K2 = await seite.evaluate(() => window.Spiel.KAPITEL2_EKG);
const MESS = await seite.evaluate((k) => ({
  baum: window.Spiel.satz(k.baum).mess, flimmern: window.Spiel.satz(k.flimmern).mess,
  schnell: window.Spiel.satz(k.schnell).mess
}), K2);
/* Wo liegt welches Bett? Die Folge wird je Schicht gemischt. */
async function bettIndex() {
  await seite.evaluate(() => { window.Spiel.__betten(); });
  const b = (await zustand()).werte.betten;
  return { baum: b.indexOf(K2.baum), flimmern: b.indexOf(K2.flimmern), schnell: b.indexOf(K2.schnell) };
}
/* Alle sichtbaren Knöpfe eines Fensters mindestens 44 × 44 px? */
async function fingergross(wurzel) {
  return seite.evaluate((sel) => {
    const zuKlein = [];
    document.querySelectorAll(sel + " button").forEach((b) => {
      const r = b.getBoundingClientRect();
      if (r.width === 0 && r.height === 0) return;              /* versteckt */
      if (r.width < 44 || r.height < 44) zuKlein.push((b.textContent || "").trim().slice(0, 24) + " " +
                                                       Math.round(r.width) + "×" + Math.round(r.height));
    });
    return zuKlein;
  }, wurzel);
}
/* Nichts blinkt: keine CSS-Animation in den neuen Fenstern. */
async function ohneBlinken(wurzel) {
  return seite.evaluate((sel) => {
    const an = [];
    document.querySelectorAll(sel + ", " + sel + " *").forEach((el) => {
      const n = getComputedStyle(el).animationName;
      if (n && n !== "none") an.push(el.className + ":" + n);
    });
    return an;
  }, wurzel);
}
const rueckText = async (sel) => ((await seite.locator(sel + " .rueck").textContent()) || "").trim();

ok("K2: Falk hat den Auftrag gegeben", await seite.evaluate(() => window.Spiel.hat("k2_auftrag")));
ok("K2: Neues Feld an der Monitorwand", (await feld("wand").count()) === 1);
await seite.locator("#kopf-stand").click();
await warte(400);
const offenK2 = (await seite.locator("#stand-hof .offen li").allTextContents()).join(" | ");
ok("K2: Stand nennt den Auftrag", /drei Schirme/.test(offenK2), offenK2.slice(0, 140));
ok("K2: Stand verrät weder Bett noch Merkmal",
   !/Bett \d|Vorhofflimmern|PQ \d|\b228\b/.test(offenK2), offenK2.slice(0, 140));
ok("K2: Kapitel 2 im Stand", /Kapitel 2/.test((await seite.locator("#stand-hof .stand-zeile").textContent()) || ""));
await seite.locator("#stand-hof .zu").click();
await warte(300);
const vorZentrale = await seite.evaluate(() => window.localStorage.getItem("nachtdienst-1"));

/* ------------------------------------------------------------ Weg A */
await feld("wand").click();
await warte(700);
ok("A: Zentrale öffnet sich", await seite.locator("#schirme-hof.an").isVisible());
ok("A: drei Schirme mit Kurve", (await seite.locator("#schirme-hof .schirm canvas").count()) === 3);
const auftragZentrale = (await seite.locator("#schirme-hof .raetsel-auftrag").textContent()) || "";
ok("A: Kästchengröße mit Papiervorschub genannt (5 mm bei 25 mm/s = 200 ms)",
   /5 mm/.test(auftragZentrale) && /25 mm\/s/.test(auftragZentrale) && /200 ms/.test(auftragZentrale), auftragZentrale.slice(-60));
const bilder = await seite.evaluate(() => Array.from(document.querySelectorAll("#schirme-hof .schirm canvas"))
  .map((c) => c.getContext("2d").getImageData(0, 0, c.width, c.height).data.some((v, i) => i % 4 === 1 && v > 200)));
ok("A: auf jedem Schirm leuchtet eine Kurve", bilder.length === 3 && bilder.every(Boolean), JSON.stringify(bilder));
ok("A: „Zurück“ oben rechts", await seite.evaluate(() => {
  const k = document.querySelector("#schirme-hof .raetsel-kopf"), z = k.querySelector(".zu");
  return z.textContent.trim() === "Zurück" && k.getBoundingClientRect().right - z.getBoundingClientRect().right < 40;
}));
let zuKlein = await fingergross("#schirme-hof");
ok("A: Knöpfe der Zentrale fingergroß", !zuKlein.length, zuKlein.join(", "));
let blinkt = await ohneBlinken("#schirme-hof");
ok("A: nichts blinkt in der Zentrale", !blinkt.length, blinkt.join(", "));
await schuss("k2_zentrale");

let idx = await bettIndex();
await seite.keyboard.press(String(idx.flimmern + 1));         /* Ziffer wählt */
await warte(250);
let r = await rueckText("#schirme-hof");
ok("A: falsches Bett (Flimmern) per Ziffer, mit Begründung",
   (await seite.locator("#schirme-hof .rueck.fast").count()) === 1 && /P-Welle/.test(r) && /Vorhofflimmern/.test(r),
   r.slice(0, 120));
await seite.locator("#schirme-hof .frage-wahl .knopf").nth(idx.schnell).click();
await warte(250);
r = await rueckText("#schirme-hof");
ok("A: falsches Bett (schnell) nennt Zahlen aus den Daten",
   r.includes(String(MESS.schnell.frequenz)) && r.includes(String(MESS.schnell.pq)), r.slice(0, 160));
await schuss("k2_zentrale_falsch");
await seite.keyboard.press(String(idx.baum + 1));
await warte(250);
ok("A: richtiges Bett erkannt", (await seite.locator("#schirme-hof .rueck.gut").count()) === 1);
await seite.keyboard.press("Enter");                         /* Enter führt weiter */
await warte(300);
ok("A: Begründungsfrage nennt das Bett",
   ((await seite.locator("#schirme-hof .schirme-frage").textContent()) || "").includes("Bett " + (idx.baum + 1)));
ok("A: sein Schirm ist hervorgehoben",
   (await seite.locator(`#schirme-hof .schirm.hervor[data-i="${idx.baum}"]`).count()) === 1);
await seite.keyboard.press("1");                             /* P-Wellen: reicht allein nicht */
await warte(250);
r = await rueckText("#schirme-hof");
ok("A: „P vor jedem QRS“ allein reicht nicht — mit Grund",
   (await seite.locator("#schirme-hof .rueck.fast").count()) === 1 && /nicht von beiden/.test(r), r.slice(0, 140));
await seite.keyboard.press("3");                             /* PQ */
await warte(250);
r = await rueckText("#schirme-hof");
ok("A: Begründung PQ angenommen, Zahlen aus den Daten",
   (await seite.locator("#schirme-hof .rueck.gut").count()) === 1 &&
   r.includes(String(MESS.baum.pq)) && r.includes(String(MESS.schnell.pq)), r.slice(0, 160));
await schuss("k2_zentrale_begruendet");
await seite.locator("#schirme-hof .weiter").click();
await warte(600);
ok("A: Befund „Monitor“ in der Mappe", await seite.evaluate(() => window.Mappe.hat("b-monitor")));
ok("A: Dr. Falk antwortet auf die PQ-Begründung", /PQ-Zeit/.test(await dialogLesen()));
await schuss("k2_falk_pq");
const textA1 = await dialogDurchLesen();
ok("A: Falk übergibt das Bett", /Ab jetzt gehört er Ihnen/.test(textA1), textA1.slice(-120));
await warte(2400);
ok("A: Bett klingelt — Ampel öffnet sich", await seite.locator("#ampel-hof.an").isVisible());
const lage = (await seite.locator("#ampel-hof .ampel-lage").textContent()) || "";
ok("A: Lage nennt Frequenz aus den Daten", lage.includes(MESS.baum.frequenz + " pro Minute"), lage.slice(-60));
ok("A: Lage behauptet keinen höhergradigen Block",
   !/Block|Pause|fällt aus|Wenckebach|Mobitz/i.test(lage), lage.slice(0, 80));
ok("A: Monitor läuft in der Ampel", (await seite.locator("#ampel-hof canvas").count()) === 1);
ok("A: Zeit läuft erst nach „Los“", (await seite.locator("#ampel-hof .ampel-entscheidung").isHidden()));
await schuss("k2_ampel_lage");
await seite.keyboard.press("Enter");                         /* Los */
await warte(250);
const breite1 = await seite.evaluate(() => document.querySelector("#ampel-hof .ampel-balken").getBoundingClientRect().width);
await warte(1200);
const breite2 = await seite.evaluate(() => document.querySelector("#ampel-hof .ampel-balken").getBoundingClientRect().width);
ok("A: Zeitbalken schrumpft sichtbar", breite2 < breite1 - 20, Math.round(breite1) + " → " + Math.round(breite2));
ok("A: drei Handlungen", (await seite.locator("#ampel-hof .ampel-knopf").count()) === 3);
ok("A: Gelb heißt bleiben und rufen — so, wie Falk es danach lobt",
   /bleiben/.test((await seite.locator("#ampel-hof .ampel-knopf").nth(1).textContent()) || ""));
zuKlein = await fingergross("#ampel-hof");
ok("A: Ampel-Knöpfe fingergroß", !zuKlein.length, zuKlein.join(", "));
blinkt = await ohneBlinken("#ampel-hof");
ok("A: nichts blinkt in der Ampel", !blinkt.length, blinkt.join(", "));
await schuss("k2_ampel_entscheidung");
await seite.keyboard.press("2");                             /* Arzt rufen */
await seite.locator(".dialog.an").waitFor({ timeout: 4000 });
ok("A: Falk zur richtigen Wahl", /Gerufen, und bei ihm geblieben/.test(await dialogLesen()));
await schuss("k2_ampel_falk");
const textA2 = await dialogDurchLesen();
ok("A: Schlussszene nennt die Frequenz aus den Daten",
   textA2.includes("Sinus, " + MESS.baum.frequenz + " pro Minute"), textA2.slice(0, 120));
ok("A: Kapitel endet offen", /Speicher/.test(textA2) && /Ende des spielbaren Teils/.test(textA2), textA2.slice(-140));
ok("A: Falk bleibt in der Rolle (Pause über drei Sekunden, wach); was das Spiel über sich sagt, sagt danach der Erzähler",
   /Pause über drei Sekunden/.test(textA2) && textA2.indexOf("Verstanden.]") >= 0 &&
   textA2.indexOf("Verstanden.]") < textA2.indexOf("Hier endet"), textA2.slice(-200));
let z = await zustand();
ok("A: Ziel erreicht (Wahl: Arzt)", z.marken.k2_fertig && z.werte.ampel === "arzt", JSON.stringify(z.werte.ampel));
ok("A: fünf Befunde (Medikamente kamen über Dr. Falk)", z.befunde.length === 5, String(z.befunde.length));

await seite.locator("#kopf-stand").click();
await warte(400);
const fussA = (await seite.locator("#stand-hof .stand-fuss").textContent()) || "";
const hatA = (await seite.locator("#stand-hof .hat li").allTextContents()).join(" | ");
ok("A: Stand sagt, dass hier das Gebaute endet", /Damit endet/.test(fussA), fussA.slice(0, 80));
ok("A: Stand führt die Episode auf", /geklingelt/.test(hatA), hatA.slice(-100));
await schuss("k2_stand_ende");
await seite.locator("#stand-hof .zu").click();
await warte(300);

/* Vergleich der neuen Karte mit dem Aufnahme-EKG */
await seite.locator("#kopf-mappe").click();
await warte(600);
const titel = await seite.locator(".mappe .karte h3").allTextContents();
const iMon = titel.findIndex((t) => /^Monitor/.test(t)), iPq = titel.findIndex((t) => /^PQ-Zeit/.test(t));
await seite.locator(".mappe .karte").nth(iMon).click();
await seite.locator(".mappe .karte").nth(iPq).click();
await seite.locator(".mappe .vergleich").click();
await warte(700);
const pqSpanne = await seite.evaluate((id) => {
  const w = window.Spiel.satz(id).schlaege.filter((s) => s.p0 !== undefined).map((s) => Math.round((s.q0 - s.p0) * 1000));
  return { min: Math.min(...w), max: Math.max(...w) };
}, K2.baum);
const vergleich = (await seite.locator(".mappe-vergleich .verg-frage").textContent()) || "";
ok("A: Monitorkarte lässt sich mit dem Aufnahme-EKG vergleichen",
   (await seite.locator(".mappe-vergleich.an canvas").count()) === 2 &&
   vergleich.includes(pqSpanne.min + " und " + pqSpanne.max + " ms"), vergleich.slice(0, 160));
await schuss("k2_vergleich");
await seite.locator(".mappe .zu").click();
await warte(300);

await feld("falk").click();
await warte(450);
ok("A: Falk danach, ohne neue Begrüßung", /Speicher/.test(await dialogLesen()));
await dialogDurchLesen();
await feld("wand").click();
await warte(600);
ok("A: Monitorwand danach als Rückschau mit Befund je Schirm",
   (await seite.locator("#schirme-hof.an.rueckschau .schirm-unter").count()) === 3);
await schuss("k2_rueckschau");
await seite.keyboard.press("Escape");
await warte(300);
ok("A: Escape schließt die Rückschau", (await seite.locator("#schirme-hof.an").count()) === 0);
/* Der große Monitor nach dem Fund: 53/min ist nach Lektion 8 Sinusrhythmus am unteren Rand, keine Bradykardie. */
await feld("schirm").click();
await warte(300);
const meldungSchirm = (await seite.locator(".meldung").last().textContent()) || "";
ok("A: großer Monitor nennt Sinusrhythmus, langsam — nicht „Sinusbradykardie“ bei " + MESS.baum.frequenz + "/min",
   /Sinusrhythmus/.test(meldungSchirm) && !/Sinusbradykardie/.test(meldungSchirm) &&
   meldungSchirm.includes(MESS.baum.frequenz + "/min"), meldungSchirm.slice(0, 90));

/* ------------------------------------------------------------ Weg B */
await seite.evaluate((s) => window.localStorage.setItem("nachtdienst-1", s), vorZentrale);
await seite.reload();
await warte(2000);
ok("B: wieder vor der Zentrale", !(await zustand()).marken.k2_bett && (await seite.locator(".dialog.an").count()) === 0);
await feld("schirm").click();                                /* der große Monitor führt auch hin */
await warte(700);
ok("B: großer Monitor öffnet die Zentrale", await seite.locator("#schirme-hof.an").isVisible());
idx = await bettIndex();
await seite.locator("#schirme-hof .frage-wahl .knopf").nth(idx.baum).click();
await warte(250);
await seite.locator("#schirme-hof .weiter").click();
await warte(300);
await seite.locator("#schirme-hof .frage-wahl .knopf", { hasText: "Frequenz" }).click();
await warte(250);
r = await rueckText("#schirme-hof");
ok("B: Begründung Frequenz angenommen, Zahlen aus den Daten",
   (await seite.locator("#schirme-hof .rueck.gut").count()) === 1 &&
   r.includes(String(MESS.baum.frequenz)) && r.includes(String(MESS.schnell.frequenz)) &&
   r.includes(String(MESS.flimmern.frequenz)), r.slice(0, 160));
await seite.locator("#schirme-hof .weiter").click();
await warte(600);
ok("B: Falk antwortet auf die Frequenz-Begründung", /Die Frequenz/.test(await dialogLesen()));
const nachFund = await seite.evaluate(() => window.localStorage.getItem("nachtdienst-1"));
await dialogDurchLesen();
await warte(2400);
ok("B: Ampel öffnet sich", await seite.locator("#ampel-hof.an").isVisible());
await seite.locator("#ampel-hof .zu").click();               /* weggeklickt: keine Sackgasse */
await warte(400);
ok("B: „Zurück“ schließt die Ampel", (await seite.locator("#ampel-hof.an").count()) === 0);
await seite.locator("#kopf-stand").click();
await warte(400);
const offenB = (await seite.locator("#stand-hof .offen li").allTextContents()).join(" | ");
ok("B: Stand erinnert an die Klingel", /hat geklingelt/.test(offenB), offenB.slice(-90));
await seite.locator("#stand-hof .zu").click();
await warte(300);
await feld("falk").click();
await warte(450);
ok("B: Falk schickt zum Bett", /klingelt/.test(await dialogLesen()));
await seite.locator(".dialog-antwort", { hasText: "Ich geh" }).click();
await warte(900);
ok("B: Ampel über Dr. Falk wieder da", await seite.locator("#ampel-hof.an").isVisible());
await seite.locator("#ampel-hof .ampel-los").click();
await seite.locator("#ampel-hof .rueck.fast").waitFor({ timeout: 13000 });   /* niemand entscheidet */
ok("B: Zeit abgelaufen, mit Satz statt Strafe",
   /Zeit ist um/.test(await rueckText("#ampel-hof")), await rueckText("#ampel-hof"));
await schuss("k2_ampel_zeit");
await seite.locator(".dialog.an").waitFor({ timeout: 4000 });
ok("B: Falk korrigiert trocken", /Zehn Sekunden/.test(await dialogLesen()));
const textB = await dialogDurchLesen();
z = await zustand();
ok("B: Ziel erreicht (Zeit abgelaufen)", z.marken.k2_fertig && z.werte.ampel === "zeit" &&
   /Ende des spielbaren Teils/.test(textB), z.werte.ampel);
ok("B: Karte nennt die Frequenz als Merkmal",
   /Erkannt an der Frequenz/.test(z.befunde.find((b) => b.id === "b-monitor").text));

/* ------------------------------------------------------------ Weg C */
await seite.evaluate((s) => window.localStorage.setItem("nachtdienst-1", s), nachFund);
await seite.reload();
await warte(2600);
ok("C: beim Betreten klingelt das Bett (wieder)", await seite.locator("#ampel-hof.an").isVisible());
await seite.locator("#ampel-hof .ampel-los").click();
await warte(300);
await seite.locator("#ampel-hof .ampel-knopf", { hasText: "Pacer" }).click();
await seite.locator(".dialog.an").waitFor({ timeout: 4000 });
ok("C: Falk korrigiert den Pacer", /Gelb, nicht Rot/.test(await dialogLesen()));
await schuss("k2_ampel_pacer");
await dialogDurchLesen();
z = await zustand();
ok("C: Ziel erreicht (Pacer)", z.marken.k2_fertig && z.werte.ampel === "pacer", z.werte.ampel);

/* ------------------------------------------------------------ Weg D */
await seite.evaluate((s) => window.localStorage.setItem("nachtdienst-1", s), nachFund);
await seite.reload();
await warte(2600);
await seite.keyboard.press("Escape");                        /* Escape schließt auch die Ampel */
await warte(300);
ok("D: Escape schließt die Ampel", (await seite.locator("#ampel-hof.an").count()) === 0);
await feld("schirm").click();
await warte(500);
ok("D: großer Monitor holt die Ampel zurück", await seite.locator("#ampel-hof.an").isVisible());
await seite.keyboard.press(" ");                             /* Leertaste: Los */
await warte(250);
await seite.keyboard.press("1");                             /* Beobachten */
await seite.locator(".dialog.an").waitFor({ timeout: 4000 });
ok("D: Falk korrigiert das bloße Beobachten", /Gelb, nicht Grün/.test(await dialogLesen()));
await dialogDurchLesen();
z = await zustand();
ok("D: Ziel erreicht (Beobachten)", z.marken.k2_fertig && z.werte.ampel === "beobachten", z.werte.ampel);
ok("Kapitel 2: vier Wege, alle am offenen Ende", true);

/* ------------------------------------------------- 9c Drei Sprachen */
for (const [kurz, probe] of [["en", "Findings"], ["ru", "Папка находок"]]) {
  await seite.evaluate((k) => { window.localStorage.setItem("nachtdienst-sprache", k); }, kurz);
  await seite.reload();
  await warte(900);
  const kopf = (await seite.locator("#kopf-mappe").textContent()) || "";
  ok("Sprache " + kurz + " schaltet um", kopf.includes(probe), kopf.trim());
  await schuss("sprache_" + kurz);
}
await seite.evaluate(() => { window.localStorage.setItem("nachtdienst-sprache", "de"); });
await seite.reload();
await warte(900);

/* ---------------------------------------------------------- 10 Zurück, Sperre */
await seite.evaluate(() => { window.localStorage.clear(); });
await seite.reload();
await warte(1200);
await dialogDurch();
const gesperrt = seite.locator("#buehne .felder polygon.ausgang").first();
await gesperrt.click();
await warte(400);
ok("Ausgang ohne Befunde gesperrt", await seite.evaluate(() => window.Szene.aktueller() === "aufnahme"));
ok("Begründung als Meldung", (await seite.locator(".meldung").count()) >= 1);
await schuss("gesperrt");

/* ------------------------------------------------- 11 Falk verlangt beide Zahlen: der Rückweg
   Nur die Frequenz gemessen → Marlene meldet an, warnt aber → Falk schickt zum Wagen zurück, ohne
   Auftrag → unten sitzt Herr Baum nicht mehr, der Wagen schon → PQ nachgemessen → Falk nimmt an.
   Danach derselbe Weg mit nur der PQ-Zeit.                                                   */
await feld("marlene").click(); await warte(450);
await antworte("Was soll ich tun"); await dialogDurch();
await wagen.click(); await warte(500);
await seite.locator("#frage-hof .wahl", { hasText: "Sinusrhythmus" }).click(); await warte(300);
await seite.locator("#frage-hof .weiter").click(); await warte(400);
const nachRhythmus = await seite.evaluate(() => window.localStorage.getItem("nachtdienst-1"));
async function zirkel(was, von, bis) {
  await wagen.click(); await warte(400);
  await seite.locator("#wahl-hof .wahl", { hasText: was }).click(); await warte(600);
  await messe(von, bis);
  await seite.locator("#zirkel-hof .uebernehmen").click(); await warte(400);
}
const letzteMeldung = async () => ((await seite.locator(".meldung").last().textContent()) || "").trim();
await zirkel("RR-Abstand", wahrheit.r1, wahrheit.r2);
ok("R: nach der zweiten Karte der Hinweis auf Marlene", /Marlene/.test(await letzteMeldung()), await letzteMeldung());
await feld("marlene").click(); await warte(450);
ok("R: Bericht mit der Frequenz allein", await antworte("Ich hab gemessen"));
const warnung = await dialogLesen();
ok("R: Marlene meldet an, warnt aber vor Falks Frage nach der Überleitung",
   /meld dich oben an/.test(warnung) && /Überleitung/.test(warnung), warnung.slice(-90));
await dialogDurch();
ok("R: Flur offen mit Rhythmus und Frequenz", await seite.evaluate(() => window.Spiel.hat("monitor_frei")));
await seite.locator("#buehne .felder polygon.ausgang").first().click(); await warte(1100); await warte(1600);
await seite.locator(".dialog-antwort.weiter").click(); await warte(350);        /* Erzähler → Falk */
ok("R: ohne PQ gibt es nur die halbe Antwort",
   (await seite.locator(".dialog-antwort", { hasText: "Sinusrhythmus," }).count()) === 0 && await antworte("Der Puls ist langsam"));
ok("R: Falk fragt nach der Überleitung", /Überleitung/.test(await dialogLesen()));
await antworte("nicht gemessen");
const zurueck = await dialogLesen();
ok("R: Falk schickt zum Wagen zurück — und gibt keinen Auftrag", /Wagen/.test(zurueck) && !/drei Betten/.test(zurueck), zurueck.slice(0, 90));
await dialogDurch();
ok("R: kein Bett-Auftrag ohne beide Zahlen",
   !(await seite.evaluate(() => window.Spiel.hat("k2_auftrag"))) && (await seite.evaluate(() => window.Spiel.hat("falk_schickt_zurueck"))));
await schuss("rueckweg_falk");
await feld("wand").click(); await warte(300);
ok("R: die Monitorwand verweist vor dem Auftrag auf Falk",
   (await seite.locator("#schirme-hof.an").count()) === 0 && /Falk/.test(await letzteMeldung()), await letzteMeldung());
await seite.locator("#kopf-stand").click(); await warte(400);
const offenR = (await seite.locator("#stand-hof .offen li").allTextContents()).join(" | ");
ok("R: Stand nennt beide Zahlen und den Wagen", /zwei Zahlen/.test(offenR) && /Wagen/.test(offenR), offenR.slice(0, 160));
ok("R: Stand ohne tote Fäden aus der Aufnahme", !/Mit Herrn Baum selbst|Marlene weiß|Frag ihn/.test(offenR), offenR.slice(0, 160));
await seite.locator("#stand-hof .zu").click(); await warte(300);
await seite.locator("#buehne .felder polygon.ausgang").first().click(); await warte(1100);
ok("R: wieder in der Aufnahme", await seite.evaluate(() => window.Szene.aktueller() === "aufnahme"));
ok("R: Herr Baum sitzt nicht mehr da — Klickfeld weg, Figur ausgeblendet",
   (await feld("herrk").count()) === 0 && (await feld("tuete").count()) === 0 &&
   await seite.evaluate(() => { const f = document.querySelector("#fig-herrk"); return !!f && getComputedStyle(f).display === "none"; }));
ok("R: der EKG-Wagen steht noch da", (await feld("wagen").count()) === 1);
/* Nur Herr Baum geht: Die Kurve auf dem Wagen läuft weiter — der Streifen von heute früh liegt ja noch dort. */
const schirmeUnten = await seite.evaluate(() => window.Spiel.__schirme());
ok("R: auf dem EKG-Wagen läuft weiter die Kurve von heute früh",
   schirmeUnten.some((s) => s.name === "wagen_schirm" && s.satz === 39 && s.laeuft) &&
   (await seite.locator("#buehne .ebene-mittelgrund .schirm-lauf[data-schirm=wagen_schirm] canvas").isVisible()),
   JSON.stringify(schirmeUnten));
await schuss("aufnahme_ohne_baum");
await feld("marlene").click(); await warte(450);
const grussUnten = await dialogLesen();
ok("R: Marlene kennt Falks Art", /zurückgeschickt/.test(grussUnten));
ok("R: Marlene sagt einmal, dass die Tüte mit ihm oben ist (das Foto steht am Bett)",
   /Tüte .*mit ihm hoch/.test(grussUnten) && /Foto/.test(grussUnten), grussUnten.slice(-80));
ok("R: die Tüte steht nicht mehr in der Aufnahme",
   await seite.evaluate(() => { const f = document.querySelector("#fig-tuete"); return !!f && getComputedStyle(f).display === "none"; }));
ok("R: kein „Schreib ihm ein EKG“ mehr", (await seite.locator(".dialog-antwort", { hasText: "Was soll ich tun" }).count()) === 0);
await antworte("Später");
await zirkel("PQ-Zeit", wahrheit.p0, wahrheit.q0);
ok("R: nach der fehlenden Zahl der Hinweis auf Falk", /Falk/.test(await letzteMeldung()), await letzteMeldung());
await seite.locator("#buehne .felder polygon.ausgang").first().click(); await warte(1100); await warte(1600);
ok("R: Falk spricht beim Wiederkommen von selbst an", /Haben Sie, was fehlt/.test(await dialogLesen()));
ok("R: jetzt die ganze Antwort", await antworte("Sinusrhythmus,"));
await dialogDurchLesen();
ok("R: Auftrag mit beiden Zahlen", await seite.evaluate(() => window.Spiel.hat("k2_auftrag")));

/* Nur die PQ-Zeit: Falk fragt nach der Frequenz. */
await seite.evaluate((s) => window.localStorage.setItem("nachtdienst-1", s), nachRhythmus);
await seite.reload(); await warte(1200);
await zirkel("PQ-Zeit", wahrheit.p0, wahrheit.q0);
await feld("marlene").click(); await warte(450);
await antworte("Ich hab gemessen");
const berichtPq = await dialogLesen();
ok("R2: Marlene mit PQ ohne Frequenz mahnt die Frequenz an", /miss die Frequenz/.test(berichtPq), berichtPq.slice(-90));
await dialogDurch();
await seite.locator("#buehne .felder polygon.ausgang").first().click(); await warte(1100); await warte(1600);
await seite.locator(".dialog-antwort.weiter").click(); await warte(350);
ok("R2: mit der PQ-Zeit allein lässt sich die Zahl nennen", await antworte("Sinusrhythmus, PQ"));
ok("R2: Falk fragt nach der Frequenz", /wie langsam/.test(await dialogLesen()));
await antworte("Hol ich nach");
await dialogDurch();
ok("R2: zurück zum Wagen, kein Auftrag", !(await seite.evaluate(() => window.Spiel.hat("k2_auftrag"))));

await browser.close();

console.log(schritte.join("\n"));
console.log("\n" + (fehler.length ? "FEHLER (" + fehler.length + "):\n - " + fehler.join("\n - ")
                                  : "Alle Prüfungen bestanden."));
process.exit(fehler.length ? 1 : 0);
