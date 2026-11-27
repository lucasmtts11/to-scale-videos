# Gera a narração FRASE POR FRASE (separadas por "|"), confere com o whisper,
# corta sobras e monta cada trecho com pausas reais entre as frases.
import json, re, torch, torchaudio as ta, time, numpy as np, soundfile as sf, subprocess
from chatterbox.mtl_tts import ChatterboxMultilingualTTS
from faster_whisper import WhisperModel
import os
D = os.environ.get("EP", os.getcwd())
import sys, difflib
segs = json.load(open(f"{D}/roteiro.json"))
ONLY = sys.argv[1:]
if ONLY: segs = [x for x in segs if x["id"] in ONLY]
m = ChatterboxMultilingualTTS.from_pretrained(device="cpu")
wm = WhisperModel("small", device="cpu", compute_type="int8", download_root=os.path.join(os.path.expanduser("~"), ".modelos", "whisper"))
SR = m.sr
# voz de referência do canal (VOZ.md): mantém o MESMO timbre em todos os episódios
REF = next((p for p in [os.environ.get("VOZ_REF", ""), os.path.join(os.path.dirname(os.path.abspath(__file__)), "voz_referencia.wav"), f"{D}/voz_referencia.wav"] if p and os.path.exists(p)), None)
print("voz de referência:", REF, flush=True)
def pause_after(s):
    s = s.strip()
    if s.endswith("?"): return 0.75
    if s.endswith("..."): return 0.65
    if s.endswith(":"): return 0.45
    if s.endswith("."): return 0.5
    return 0.3
SYN = {"pras": "para", "pros": "para", "pra": "para", "lage": "laje", "bigas": "vigas", "biga": "viga"}
from num2words import num2words
def n(w):
    w = re.sub(r"[^a-zà-ú0-9]", "", w.lower()); return SYN.get(w, w)
def words(txt):
    # o whisper escreve números em dígitos ("213", "60 kg"): converte para extenso para comparar TUDO,
    # inclusive os números (no ep05 v2 "treze" saiu "três" e passou porque números eram ignorados)
    out = []
    for x in txt.replace("-", " ").replace("kg", " quilos").split():
        x = n(x)
        if not x: continue
        if x.isdigit(): out += [n(y) for y in num2words(int(x), lang="pt_BR").replace("-", " ").split()]
        else: out.append(x)
    return out
def fim_da_fala(w, t_end, t_next=None):
    # corta no fim REAL do som (envelope), não no fim estimado pelo whisper, que costuma vir cedo e comia
    # a última sílaba ("contrá-", "porta-", "país in-") — eram as "travadas" do ep05 v2
    env = np.sqrt(np.convolve(w ** 2, np.ones(int(0.02 * SR)) / int(0.02 * SR), "same"))
    thr = max(0.01, 0.06 * env.max()); i = int(t_end * SR); quiet = int(0.18 * SR); lim = min(len(w), i + int(0.9 * SR), int((t_next - 0.04) * SR) if t_next else len(w))
    while i < lim:
        if (env[i:i + quiet] < thr).all(): return i + int(0.06 * SR)
        i += int(0.01 * SR)
    return lim
def gen(text, seed):
    torch.manual_seed(seed)
    w = m.generate(text, language_id="pt", audio_prompt_path=REF, exaggeration=0.8, cfg_weight=0.3).squeeze().numpy()
    a16 = w[np.linspace(0, len(w) - 1, int(len(w) * 16000 / SR)).astype(int)].astype(np.float32)
    r, _ = wm.transcribe(a16, language="pt", word_timestamps=True); ws = [x for s in r for x in s.words]
    return w, ws
for s in segs:
    parts = [p.strip() for p in s["text"].split("|") if p.strip()]
    out = []
    for i, p in enumerate(parts):
        best = None; want = words(p)
        for seed in (7, 19, 31, 43):
            w, ws = gen(p, seed); got = words(" ".join(x.word for x in ws))
            sim = difflib.SequenceMatcher(None, want, got).ratio()
            if best is None or sim > best[0]: best = (sim, w, ws)
            if sim >= 0.85: break
        sim, w, ws = best
        if ws:
            # última palavra do roteiro no que o whisper ouviu (ignora palavra extra inventada no fim)
            # (busca de trás para frente a ÚLTIMA palavra do roteiro; contar palavras falha quando o whisper
            #  escreve "pro" como "para o" ou inventa um "E" no começo: cortava "contrário" e "inteiro")
            k = len(ws) - 1
            for j in range(len(ws) - 1, -1, -1):
                if want and want[-1] in words(ws[j].word): k = j; break
                if want and difflib.SequenceMatcher(None, want[-1], "".join(words(ws[j].word))).ratio() > 0.75: k = j; break
            a0 = max(0, int((ws[0].start - 0.08) * SR)); a1 = fim_da_fala(w, ws[k].end, ws[k + 1].start if k + 1 < len(ws) else None); w = w[a0:a1]
        fade = min(len(w), int(0.04 * SR)); w[-fade:] *= np.linspace(1, 0, fade)
        out.append(w); out.append(np.zeros(int(pause_after(p) * SR), np.float32) if i < len(parts) - 1 else np.zeros(0, np.float32))
        print(s["id"], i, round(sim, 2), repr(p), "->", " ".join(x.word.strip() for x in ws), flush=True)
    a = np.concatenate(out).astype(np.float32)
    sf.write(f"{D}/voz_raw_{s['id']}.wav", a, SR)
    # um pouco mais devagar, sem mudar o tom
    subprocess.run(["ffmpeg", "-loglevel", "error", "-y", "-i", f"{D}/voz_raw_{s['id']}.wav", "-af", "atempo=0.94", f"{D}/voz_{s['id']}.wav"], check=True)
print("FIM", flush=True)
