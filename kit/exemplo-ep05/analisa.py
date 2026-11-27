import json, re, numpy as np, soundfile as sf, os, sys
from faster_whisper import WhisperModel
m = WhisperModel("small", device="cpu", compute_type="int8", download_root=os.path.join(os.path.expanduser("~"), ".modelos", "whisper"))
segs = json.load(open("roteiro.json"))
ids = sys.argv[1:] or [s["id"] for s in segs]
for s in segs:
    if s["id"] not in ids: continue
    a, sr = sf.read(f"v_{s['id']}.wav", dtype="float32")
    idx = np.linspace(0, len(a)-1, int(len(a)*16000/sr)).astype(int); a16 = a[idx]
    r, _ = m.transcribe(a16, language="pt", word_timestamps=True); ws = [w for x in r for w in x.words]
    print(f"\n== {s['id']} ({len(a)/sr:.2f}s)\nROTEIRO: {s['text']}\nOUVIDO : {' '.join(w.word.strip() for w in ws)}")
    # frases: fim abrupto = energia alta nos últimos 25 ms antes de um silêncio
    env = np.sqrt(np.convolve(a**2, np.ones(int(0.02*sr))/int(0.02*sr), "same"))
    thr = 0.02
    voiced = env > thr
    # bordas de fala -> silêncio
    edges = np.where(voiced[:-1] & ~voiced[1:])[0]
    for e in edges:
        # silêncio seguinte com > 0,25 s ?
        nxt = np.argmax(voiced[e+1:]) if voiced[e+1:].any() else len(a)-e
        if nxt < 0.25*sr: continue
        drop = env[max(0,e-int(0.03*sr)):e].max() / (env[max(0,e-int(0.15*sr)):e].max()+1e-9)
        slope = env[e-int(0.01*sr)] if e>int(0.01*sr) else 0
        if env[max(0,e-int(0.012*sr))] > 0.08:
            print(f"   corte brusco? t={e/sr:.2f}s env_antes={env[max(0,e-int(0.012*sr))]:.3f}")
    gaps = [(ws[i].end, ws[i+1].start-ws[i].end) for i in range(len(ws)-1) if ws[i+1].start-ws[i].end > 0.9]
    for g in gaps: print(f"   pausa longa {g[1]:.2f}s em {g[0]:.2f}s")
