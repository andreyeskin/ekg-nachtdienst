/* Durchlauf durch Kapitel 1 in echtem Chromium.
   jsdom reicht hier nicht: Canvas, Zeigerereignisse, Layout und Animation
   sind genau das, was schiefgeht.                                            */
import { starteBrowser } from "./browser.mjs";
import fs from "fs";

const DATEI = process.argv[2] || "/home/claude/spiel/bau/nachtdienst.html";
const BILDER = process.argv[3] || "/home/claude/spiel/bau/durchlauf";
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
seite.on("console", (m) => { if (m.type() === "error") fehler.push("Konsole: " + m.text().slice(0, 160)); });
seite.on("pageerror", (e) => fehler.push("Seitenfehler: " + String(e).slice(0, 200)));

async function schuss(name) {
  n++;
  await seite.screenshot({ path: `${BILDER}/${String(n).padStart(2, "0")}_${name}.png` });
}
const warte = (ms) => seite.waitForTimeout(ms);

await seite.goto("file://" + DATEI);
await warte(900);

/* ---------------------------------------------------------- 1 Auftakt */
ok("Seite lebt", await seite.locator("#buehne").isVisible());
ok("Vier Ebenen gezeichnet", (await seite.locator("#buehne .ebene svg").count()) === 4,
   "gefunden: " + (await seite.locator("#buehne .ebene svg").count()));
ok("Hotspots vorhanden", (await seite.locator(".feld").count()) >= 6);
ok("Auftakt-Dialog erscheint", await seite.locator(".dialog.an").isVisible());
await schuss("auftakt");

async function dialogDurch(maxKlicks = 14) {
  for (let i = 0; i < maxKlicks; i++) {
    if (!(await seite.locator(".dialog.an").count())) return;
    await seite.locator(".dialog-text").click();          // Tippen überspringen
    await warte(140);
    const w = seite.locator(".dialog-antwort.weiter");
    if (await w.count()) { await w.first().click(); await warte(280); continue; }
    const a = seite.locator(".dialog-antwort");
    if ((await a.count()) === 1) { await a.first().click(); await warte(280); continue; }
    return;                                               // echte Wahl: nicht raten
  }
}
await dialogDurch();
ok("Auftakt beendet", (await seite.locator(".dialog.an").count()) === 0);

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

/* ---------------------------------------------------------- 2 Marlene */
await feld("marlene").click();
await warte(450);
ok("Marlene spricht", await seite.locator(".dialog.an").isVisible());
ok("Erstbegrüßung, nicht die Wiederholung",
   ((await seite.locator(".dialog-text").textContent()) || "").includes("Famulantin"),
   ((await seite.locator(".dialog-text").textContent()) || "").slice(0, 60));
ok("Porträt im Dialog", (await seite.locator(".dialog-bild svg").count()) === 1);
await schuss("marlene");
ok("Frage nach dem Fall", await antworte("Was ist passiert"));
ok("Nachfrage ohne Vorwarnung", await antworte("Ohne Vorwarnung"));
await antworte("Vom Herzen");
await dialogDurch();
ok("Auftrag gesetzt", await seite.evaluate(() => window.Spiel.hat("auftrag_ekg")));

/* ---------------------------------------------------------- 3 EKG schreiben */
const wagen = feld("wagen");
await wagen.click();
await warte(500);
ok("Rhythmusfrage erscheint", await seite.locator("#frage-hof.an").isVisible());
ok("EKG in der Frage gezeichnet", (await seite.locator("#frage-hof canvas").count()) === 1);
await schuss("rhythmusfrage");
await seite.locator("#frage-hof .wahl", { hasText: "Sinusrhythmus" }).click();
await warte(3000);
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
await feld("marlene").click();
await warte(450);
await seite.locator(".dialog-text").click();
await warte(150);
ok("Antwort erscheint erst mit Befund",
   (await seite.locator(".dialog-antwort", { hasText: "PQ-Zeit gemessen" }).count()) === 1);
const gemessen = await seite.evaluate(() => window.Spiel.zustand.werte.pq);
ok("Dialog nennt den selbst gemessenen Wert",
   ((await seite.locator(".dialog-antwort", { hasText: "PQ-Zeit gemessen" }).textContent()) || "")
     .includes(String(gemessen)), "gemessen: " + gemessen);
await seite.locator(".dialog-antwort", { hasText: "PQ-Zeit gemessen" }).click();
await warte(400);
await dialogDurch();
ok("Monitorzimmer freigegeben", await seite.evaluate(() => window.Spiel.hat("monitor_frei")));

/* ---------------------------------------------------------- 8 Raumwechsel */
const ausgang = seite.locator("#buehne .felder polygon.ausgang").first();
await ausgang.click();
await warte(1100);
ok("Im Monitorzimmer", await seite.evaluate(() => window.Szene.aktueller() === "monitor"));
ok("Monitorkurve läuft", (await seite.locator("#monitor-lauf canvas").count()) === 1);
await warte(1600);
ok("Dr. Falk spricht an", await seite.locator(".dialog.an").isVisible());
await schuss("monitorzimmer");
ok("Beste Antwort nur mit beiden Befunden",
   (await seite.locator(".dialog-antwort", { hasText: "Sinusbradykardie" }).count()) === 1);
await seite.locator(".dialog-antwort", { hasText: "Sinusbradykardie" }).click();
await warte(500);
await dialogDurch();
await schuss("nach_falk");

/* ---------------------------------------------------------- 9 Neu laden */
await seite.reload();
await warte(1200);
ok("Zustand übersteht Neuladen", await seite.evaluate(() => window.Szene.aktueller() === "monitor"));
ok("Befunde noch da", (await seite.evaluate(() => window.Spiel.zustand.befunde.length)) === 3);
ok("Kein Auftakt bei Fortsetzung", (await seite.locator(".dialog.an").count()) === 0);
await schuss("nach_neuladen");

/* --------------------------------------------------- 9b Hotspots zeigen */
await seite.locator("#kopf-zeigen").click();
await warte(300);
ok("Hotspot-Hilfe schaltet sich ein", await seite.evaluate(
  () => document.querySelector(".felder").classList.contains("zeigen")));
await schuss("hotspots_gezeigt");

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

await browser.close();

console.log(schritte.join("\n"));
console.log("\n" + (fehler.length ? "FEHLER (" + fehler.length + "):\n - " + fehler.join("\n - ")
                                  : "Alle Prüfungen bestanden."));
process.exit(fehler.length ? 1 : 0);
