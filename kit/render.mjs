// Uso: node render.mjs preview 1.5 4.3 ...   (salva frames JPEG)
//      node render.mjs video saida.mp4       (renderiza o MP4 inteiro)
import { chromium } from "/opt/npm-tools/node_modules/playwright/index.mjs";
import { spawn } from "node:child_process";
import { writeFileSync, renameSync, mkdirSync } from "node:fs";
import path from "node:path";

const FPS = 30;
const [mode, ...args] = process.argv.slice(2);
const html = "file://" + path.resolve(process.env.HTML || "cena.html");

const browser = await chromium.launch({ executablePath: "/usr/bin/google-chrome", args: ["--use-angle=swiftshader","--enable-unsafe-swiftshader","--ignore-gpu-blocklist","--allow-file-access-from-files"] });
const page = await browser.newPage({ viewport: { width: 1080, height: 1920 } });
page.on("console", m => console.log("PAGE:", m.text())); page.on("pageerror", e => console.log("ERR:", e.message));
await page.goto(html);
await page.waitForFunction(() => window.READY === true);

const grab = t => page.evaluate(t => { window.seek(t); return document.getElementById("out").toDataURL("image/jpeg", 0.92); }, t)
  .then(d => Buffer.from(d.split(",")[1], "base64"));

if (mode === "preview") {
  const PD = process.env.PD || "preview"; mkdirSync(PD, { recursive: true });
  for (const t of args.map(Number)) writeFileSync(`${PD}/t_${t.toFixed(2)}.jpg`, await grab(t));
} else {
  const out = args[0] || "nova.mp4", tmp = out.replace(/\.mp4$/, ".tmp.mp4");
  const duration = await page.evaluate(() => window.DURATION);
  const ff = spawn("ffmpeg", ["-y", "-f", "image2pipe", "-c:v", "mjpeg", "-framerate", String(FPS), "-i", "-",
    "-c:v", "libx264", "-crf", "18", "-preset", "veryfast", "-pix_fmt", "yuv420p", "-movflags", "+faststart", tmp],
    { stdio: ["pipe", "ignore", "inherit"] });
  const f0 = Math.round(Number(args[1] ?? 0) * FPS), f1 = Math.round(Number(args[2] ?? duration) * FPS), total = f1 - f0;
  for (let f = f0; f < f1; f++) {
    const buf = await grab(f / FPS);
    if (!ff.stdin.write(buf)) await new Promise(r => ff.stdin.once("drain", r));
  }
  ff.stdin.end();
  const code = await new Promise(r => ff.on("close", r));
  if (code === 0) { renameSync(tmp, out); console.log(`ok: ${out} (${total} frames)`); }
  else { console.error("ffmpeg falhou", code); process.exitCode = 1; }
}
await browser.close();
