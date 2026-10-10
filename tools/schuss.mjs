import { chromium } from "/home/claude/patho1/node_modules/playwright-core/index.mjs";
const [,, datei, ziel, breite, hoehe] = process.argv;
const b = await chromium.launch({ executablePath: "/opt/pw-browsers/chromium-1194/chrome-linux/chrome", args: ["--no-sandbox"] });
const p = await b.newPage({ viewport: { width: +(breite||1200), height: +(hoehe||900) }, deviceScaleFactor: 2 });
await p.goto("file://" + datei);
await p.waitForTimeout(400);
await p.screenshot({ path: ziel, fullPage: !hoehe });
await b.close();
