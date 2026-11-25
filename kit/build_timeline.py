# Junta a narração dos trechos, mede tempos e alinha palavras do roteiro com os tempos do whisper
import json, re, subprocess, numpy as np, soundfile as sf
from faster_whisper import WhisperModel

import os
D = os.environ.get("EP", os.getcwd())
segs = json.load(open(f"{D}/roteiro.json"))
GAP = 0.6          # respiro entre trechos
SPEED = 1.0        # acelera um pouco a fala
EXTRA = {'tira': 1.3, 'domino': 3.4, 'cta': 1.6}
LEAD = 0.25         # silêncio no começo
model = WhisperModel("small", device="cpu", compute_type="int8", download_root=os.path.join(os.path.expanduser("~"), ".modelos", "whisper"))

def load16k(p):
    a, sr = sf.read(p, dtype="float32")
    if a.ndim > 1: a = a.mean(1)
    idx = np.linspace(0, len(a) - 1, int(len(a) * 16000 / sr)).astype(int)
    return a[idx]

def norm(w): return re.sub(r"[^a-zà-ú0-9]", "", w.lower())

pieces, t, out_segs, words = [], LEAD, [], []
for s in segs:
    src = f"{D}/voz_{s['id']}.wav"; dst = f"{D}/v_{s['id']}.wav"
    # acelera, corta silêncio das pontas, normaliza para 24 kHz mono
    subprocess.run(["ffmpeg", "-loglevel", "error", "-y", "-i", src, "-af",
                    f"silenceremove=start_periods=1:start_threshold=-45dB,areverse,silenceremove=start_periods=1:start_threshold=-45dB,areverse,atempo={SPEED}",
                    "-ar", "24000", "-ac", "1", dst], check=True)
    a, sr = sf.read(dst, dtype="float32"); dur = len(a) / sr
    res, _ = model.transcribe(load16k(dst), language="pt", word_timestamps=True)
    hw = [w for r in res for w in r.words]
    if hw and dur - hw[-1].end > 2.0:   # corta "cauda" estranha depois da última palavra
        cut = hw[-1].end + 0.6
        subprocess.run(["ffmpeg", "-loglevel", "error", "-y", "-i", dst, "-t", f"{cut:.3f}", "-af", "afade=t=out:st=%.3f:d=0.25" % (cut - 0.25), dst + ".tmp.wav"], check=True)
        import os; os.replace(dst + ".tmp.wav", dst); a, sr = sf.read(dst, dtype="float32"); dur = len(a) / sr
    # alinha as palavras do roteiro com as do whisper pela ordem (o whisper às vezes erra a grafia)
    sw = s["text"].replace("|", " ").split()
    if len(hw) == len(sw):
        times = [(w.start, w.end) for w in hw]
    else:
        # distribui proporcionalmente ao tamanho das palavras, ancorado no início/fim da fala detectada
        st = hw[0].start if hw else 0.0; en = hw[-1].end if hw else dur
        L = np.array([len(norm(x)) + 2 for x in sw], float); c = np.concatenate([[0], np.cumsum(L)]) / L.sum()
        times = [(st + c[i] * (en - st), st + c[i + 1] * (en - st)) for i in range(len(sw))]
    for w, (a0, a1) in zip(sw, times): words.append({"w": w, "s": round(t + a0, 3), "e": round(t + a1, 3), "seg": s["id"]})
    out_segs.append({"id": s["id"], "start": round(t - (LEAD if s is segs[0] else GAP / 2), 3), "voice": round(t, 3), "len": round(dur, 3)})
    pieces.append((dst, t)); t += dur + GAP + EXTRA.get(s['id'], 0)
    print(s["id"], round(dur, 2), "palavras", len(sw), "whisper", len(hw))

total = round(t - GAP + 0.6, 3)
for i, s in enumerate(out_segs): s["end"] = out_segs[i + 1]["start"] if i + 1 < len(out_segs) else total
out_segs[0]["start"] = 0.0
# a fala do "tira" precisa de um respiro antes do golpe: nada a fazer aqui, a cena usa os tempos
json.dump({"segs": out_segs, "words": words, "total": total}, open(f"{D}/timeline.json", "w"), ensure_ascii=False, indent=1)
open(f"{D}/timeline.js", "w").write("window.TL = " + json.dumps({"segs": out_segs, "words": words, "total": total}, ensure_ascii=False) + ";")
# monta a trilha de voz
SR = 24000; voice = np.zeros(int(total * SR), np.float32)
for p, st in pieces:
    a, _ = sf.read(p, dtype="float32"); i = int(st * SR); voice[i:i + len(a)] += a[:len(voice) - i]
sf.write(f"{D}/voz_total.wav", voice, SR)
print("total", total)
