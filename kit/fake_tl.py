import json
segs=json.load(open("roteiro.json")); t=0.25; out=[]; words=[]
EXTRA={'erro':0.6,'alcool':1.4,'dia':0.8,'virada':1.4,'cta':1.6}
for s in segs:
    st=t
    for p in s["text"].split("|"):
        for w in p.split():
            d=0.12+0.055*len(w); words.append({"w":w,"s":round(t,3),"e":round(t+d,3),"seg":s["id"]}); t+=d+0.04
        t+=0.55
    out.append({"id":s["id"],"start":st-0.3,"voice":st,"len":t-st}); t+=0.6+EXTRA.get(s["id"],0)
for i,s in enumerate(out): s["end"]=out[i+1]["start"] if i+1<len(out) else t
out[0]["start"]=0
open("timeline.js","w").write("window.TL = "+json.dumps({"segs":out,"words":words,"total":t},ensure_ascii=False)+";")
print(t); [print(s["id"],round(s["start"],1),round(s["end"],1)) for s in out]
