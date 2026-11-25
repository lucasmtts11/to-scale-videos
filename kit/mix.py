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
for s in TL["segs"][1:]: add(whoosh(), s["start"] - 0.45, 0.35)
tImpact = (wt("tira", "ele") or SEG["tira"]["start"] + 1.2) + 0.3
add(whoosh(0.4), tImpact - 0.42, 0.5); add(impact(), tImpact, 0.9)
add(crackle(SEG["trincas"]["end"] - SEG["trincas"]["start"] - 0.5), SEG["trincas"]["start"] + 0.3, 0.35)
tv2 = wt("domino", "efeito") or SEG["domino"]["start"] + 2
add(rumble(SEG["domino"]["end"] - tv2 + 0.3), tv2 - 0.3, 0.9); add(crackle(1.5), tv2, 0.5)
for w in ["escora", "engenheiro", "viga"]:
    x = wt("certo", w)
    if x: add(ding(), x, 0.18)
x = wt("certo", "viga")
if x: add(impact() * 0.4, x + 0.55, 0.35)
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
