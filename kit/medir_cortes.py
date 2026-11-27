import subprocess, sys, numpy as np, json
W,H=72,128
out={}
for f in sys.argv[1:]:
    raw=subprocess.run(["ffmpeg","-v","error","-i",f,"-vf",f"fps=30,scale={W}:{H},format=gray","-f","rawvideo","-"],capture_output=True).stdout
    fr=np.frombuffer(raw,np.uint8).reshape(-1,H,W).astype(np.float32)
    d=np.abs(np.diff(fr,axis=0)).mean((1,2))
    cuts=[]
    for i in range(len(d)):
        loc=np.median(d[max(0,i-8):i+9])
        if d[i]>max(12,5*loc+3) and (not cuts or i-cuts[-1]>8): cuts.append(i)
    t=np.array(cuts)/30; dur=len(fr)/30
    shots=np.diff(np.concatenate([[0],t,[dur]]))
    # movimento no começo: diferença média nos 3 primeiros segundos vs resto
    mov0=float(d[:15].mean()); movall=float(np.median(d))
    out[f]=dict(dur=round(dur,1),cortes=len(cuts),tomada_media=round(dur/(len(cuts)+1),2),mediana=round(float(np.median(shots)),2),maior=round(float(shots.max()),1),
                primeiro_corte=round(float(t[0]),2) if len(t) else None,mov_meio_s_inicial=round(mov0,2),mov_mediano=round(movall,2),quadros_parados_pct=round(float((d<0.3).mean()*100),1))
    print(f,out[f],flush=True)
json.dump(out,open("cortes.json","w"),indent=1)
