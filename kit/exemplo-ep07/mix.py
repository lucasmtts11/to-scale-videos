# Trilha original + efeitos sincronizados + narração -> audio_final.wav
import json, re, numpy as np, soundfile as sf
import os
D = os.environ.get("EP", os.getcwd()); SR = 44100
TL = json.load(open(f"{D}/timeline.json")); total = TL["total"]; N = int(total * SR)
rng = np.random.default_rng(5)
L = np.zeros(N); R = np.zeros(N)
SEG = {s["id"]: s for s in TL["segs"]}
def wt(seg, w):
    for x in TL["words"]:
        if x["seg"] == seg and re.sub(r"[^a-zà-ú0-9]", "", x["w"].lower()).startswith(w): return x["s"]
    return None
def add(sig, t0, g=1.0, pan=0.0):
    i = int(t0 * SR)
    if i >= N or i < 0: return
    sig = sig[:N - i]; L[i:i+len(sig)] += sig * g * (1 - max(0, pan)); R[i:i+len(sig)] += sig * g * (1 + min(0, pan))
def env(n, a, d): t = np.arange(n) / SR; return np.minimum(1, t / max(a, 1e-4)) * np.exp(-t / d)
def lp(x, w): return np.convolve(x, np.ones(w) / w, "same")
def tone(f, dur, kind="sin", a=0.01, d=0.3):
    n = int(dur * SR); t = np.arange(n) / SR; ph = f * t
    return (np.sin(2*np.pi*ph) if kind == "sin" else 2*(ph % 1) - 1) * env(n, a, d)
note = lambda m: 440 * 2 ** ((m - 69) / 12)

# ---- música de fundo: pad + baixo + batida leve (Dm Bb F C), 100 bpm
BEAT = 0.6; CH = [[62, 65, 69], [58, 62, 65], [53, 57, 60], [60, 64, 67]]; ROOT = [38, 34, 41, 36]
bar = BEAT * 4
for b in range(int(total / bar) + 1):
    t0 = b * bar; ch = CH[b % 4]
    pad = sum(tone(note(m), bar + 0.1, "saw", 0.3, 4.0) for m in ch); add(lp(pad, 30) * 0.035, t0)
    for k in range(4): add(lp(tone(note(ROOT[b % 4]), BEAT * 0.9, "saw", 0.005, 0.25), 40) * 0.12, t0 + k * BEAT)
    for k in range(8):
        m = ch[k % 3] + 12 + (12 if k in (3, 7) else 0)
        add(lp(tone(note(m), 0.25, "saw", 0.002, 0.08), 8) * 0.025, t0 + k * BEAT / 2, pan=0.3 if k % 2 else -0.3)
def kick():
    n = int(0.35 * SR); t = np.arange(n) / SR; f = 48 + 90 * np.exp(-t * 30)
    return np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-t * 9)
def hat():
    n = int(0.08 * SR); x = np.diff(np.concatenate([[0], rng.standard_normal(n)])); return x * env(n, 0.001, 0.02) * 0.4
for k in range(int(total / BEAT)):
    t0 = k * BEAT
    if t0 > total - 1.5: break
    add(kick(), t0, 0.35 if k % 2 == 0 else 0.0); add(hat(), t0 + BEAT / 2, 0.18)
# ---- efeitos
def whoosh(dur=0.5):
    n = int(dur * SR); x = rng.standard_normal(n); x = x - lp(x, 40); t = np.arange(n) / n; return lp(x, 6) * (t ** 2) * 0.8
def impact():
    n = int(1.2 * SR); t = np.arange(n) / SR; f = 40 + 60 * np.exp(-t * 12)
    boom = np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-t * 4)
    crunch = lp(rng.standard_normal(n), 3) * np.exp(-t * 7) * 0.6
    return boom + crunch
def crackle(dur):
    n = int(dur * SR); x = np.zeros(n)
    for _ in range(int(dur * 25)):
        i = rng.integers(0, n - 2000); x[i:i+2000] += lp(rng.standard_normal(2000), 2) * np.exp(-np.arange(2000) / 200) * rng.uniform(0.3, 1)
    return x
def rumble(dur):
    n = int(dur * SR); t = np.arange(n) / SR; x = lp(rng.standard_normal(n), 120) * 6
    return x * np.minimum(1, t / 0.4) * np.minimum(1, (dur - t) / 0.4)
def ding(f=1320): return tone(f, 0.6, "sin", 0.002, 0.18) + 0.5 * tone(f * 1.5, 0.6, "sin", 0.002, 0.12)
def honk(f=420, dur=0.5):
    n = int(dur * SR); t = np.arange(n) / SR
    x = (np.sign(np.sin(2*np.pi*f*t)) + np.sign(np.sin(2*np.pi*f*1.26*t))) * 0.5
    return lp(x, 6) * np.minimum(1, t / 0.02) * np.minimum(1, (dur - t) / 0.05) * 0.5
def clink(f=2600): return tone(f, 0.25, "sin", 0.001, 0.05) + 0.6 * tone(f * 1.37, 0.25, "sin", 0.001, 0.04)
def burp(dur=0.7):
    n = int(dur * SR); t = np.arange(n) / SR; f = 70 + 25 * np.sin(t * 9)
    x = np.sign(np.sin(2 * np.pi * np.cumsum(f) / SR)) * (1 + 0.5 * lp(rng.standard_normal(n), 20))
    return lp(x, 10) * np.minimum(1, t / 0.03) * np.minimum(1, (dur - t) / 0.15) * 0.6
def splat():
    n = int(0.5 * SR); t = np.arange(n) / SR; return lp(rng.standard_normal(n), 25) * np.exp(-t * 9) * 3
def siren(dur):
    n = int(dur * SR); t = np.arange(n) / SR; f = np.where((t % 0.9) < 0.45, 960, 770)
    return np.sin(2 * np.pi * np.cumsum(f) / SR) * 0.35 * np.minimum(1, t / 0.2) * np.minimum(1, (dur - t) / 0.3)
for s in TL["segs"][1:]: add(whoosh(), s["start"] - 0.45, 0.35)
def ploc():
    n = int(0.25 * SR); t = np.arange(n) / SR; f = 900 * np.exp(-t * 18) + 200
    return np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-t * 14) * 0.8
def creak(dur=0.8):
    n = int(dur * SR); t = np.arange(n) / SR; f = 180 + 60 * np.sin(t * 7)
    x = np.sign(np.sin(2 * np.pi * np.cumsum(f) / SR)) * (0.5 + 0.5 * np.abs(np.sin(t * 40)))
    return lp(x, 12) * np.minimum(1, t / 0.05) * np.minimum(1, (dur - t) / 0.1) * 0.35
def sizzle(dur):
    n = int(dur * SR); x = rng.standard_normal(n); x = x - lp(x, 8); t = np.arange(n) / SR
    return x * 0.12 * (0.6 + 0.4 * np.sin(t * 3)) * np.minimum(1, t / 0.5) * np.minimum(1, (dur - t) / 0.5)
def cricket(dur):
    n = int(dur * SR); t = np.arange(n) / SR
    return np.sin(2 * np.pi * 4200 * t) * (np.sin(2 * np.pi * 30 * t) > 0.3) * ((t % 0.9) < 0.25) * 0.06
x = wt("hook", "pingar")
if x: add(ploc(), x + 0.25, 0.7); add(splat() * 0.3, x + 0.27, 0.4)
# casa sendo montada (as peças caem com mola, escalonadas)
r = SEG["escala"]["start"] + 0.2
for k in range(9): add(impact() * 0.25, r + k * 0.18 + 0.35, 0.22, pan=rng.uniform(-.4, .4))
for w in ("dezessete", "duzentas"):
    x = wt("escala", w)
    if x: add(ding(), x, 0.2)
x = wt("escala", "isso")
if x: add(impact() * 0.4, x + 0.3, 0.3)
x = wt("porque", "trinta")
if x: add(ding(), x, 0.16)
x = wt("porque", "boca")
if x: add(ploc() * 0.6, x + 0.1, 0.4)
for sid in ("manha", "meiodia", "tarde", "colapso"):
    add(ding(1760), SEG[sid]["start"] + 0.15, 0.12)
x = wt("manha", "perfeita")
if x:
    for k in range(3): add(ding(2000 + 300 * k), x + 0.4 * k + 0.4, 0.08)
add(sizzle(SEG["tarde"]["end"] - SEG["meiodia"]["start"]), SEG["meiodia"]["start"], 0.5)
x = wt("meiodia", "começa")
if x:
    for k in range(10): add(ploc() * 0.5, x + 0.3 + k * 0.35 + 0.1 * rng.random(), 0.3, pan=rng.uniform(-.5, .5))
x = wt("tarde", "porta")
if x: add(creak(), x + 0.1, 0.6)
x = wt("tarde", "janela")
if x: add(whoosh(0.6), x + 0.1, 0.4)
x = wt("tarde", "casa")
if x: add(rumble(2.5), x - 0.3, 0.5)
x = wt("colapso", "o")
if x: add(creak(1.6), x, 0.5)
x = wt("colapso", "desaba")
if x: add(impact(), x + 0.25, 0.9); add(splat(), x + 0.27, 0.8); add(rumble(2.0), x + 0.25, 0.6)
x = wt("colapso", "agora")
if x: add(sizzle(3.0) * 0.6, x, 0.4)
add(cricket(SEG["virada"]["end"] - SEG["virada"]["start"]), SEG["virada"]["start"], 1.0)
for w in ("essas", "dava"):
    x = wt("virada", w)
    if x: add(ding(), x, 0.2)
# ---- abaixa a música durante a fala (ducking simples) e soma a voz
voz, vsr = sf.read(f"{D}/voz_total.wav", dtype="float32")
vi = np.interp(np.arange(N) / SR, np.arange(len(voz)) / vsr, voz)
envv = lp(np.abs(vi), 4000); duck = 1 - 0.45 * np.clip(envv / (envv.max() * 0.25 + 1e-9), 0, 1)
mus = np.stack([L, R], 1); mus /= (np.abs(mus).max() + 1e-9)
mix = mus * 0.32 * duck[:, None] + np.stack([vi, vi], 1) * (0.92 / (np.abs(vi).max() + 1e-9))
fade = np.ones(N); nf = int(1.0 * SR); fade[-nf:] = np.linspace(1, 0, nf); mix *= fade[:, None]
mix /= max(1.0, np.abs(mix).max() / 0.97)
sf.write(f"{D}/audio_final.wav", mix.astype(np.float32), SR)
print("ok", round(total, 2))
