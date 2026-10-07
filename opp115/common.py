import csv, glob, os, collections, random
csv.field_size_limit(10**9)
MAP={"First Party Collection/Use":"Collection","Data Retention":"Retention","Third Party Sharing/Collection":"Sharing",
"User Access, Edit and Deletion":"Access","User Choice/Control":"Control","Data Security":"Security","International and Specific Audiences":"Regulatory"}
CATS=["Collection","Retention","Sharing","Access","Control","Security","Regulatory"]
W=dict(zip(CATS,[0.1781,0.1233,0.1644,0.1370,0.1507,0.1370,0.1096]))
import os
base=os.environ.get("OPP115_DIR","OPP-115")
def load_all():
    data=[]
    for f in sorted(glob.glob(base+"/annotations/*.csv")):
        pid=os.path.basename(f)[:-4]
        segs=open(f"{base}/sanitized_policies/{pid}.html",encoding="utf-8",errors="ignore").read().split("|||")
        votes=collections.defaultdict(lambda: collections.defaultdict(set))
        for r in csv.reader(open(f,encoding="utf-8",errors="ignore")):
            if len(r)>5 and r[5] in MAP: votes[int(r[4])][MAP[r[5]]].add(r[2])
        gold=[{c for c,a in votes[i].items() if len(a)>=2} for i in range(len(segs))]
        data.append((pid,segs,gold))
    return data
def split(data,seed=2026,ntest=40):
    ids=sorted(d[0] for d in data); random.Random(seed).shuffle(ids); test=set(ids[:ntest])
    return [d for d in data if d[0] not in test],[d for d in data if d[0] in test]
def evaluate(data,detect,verbose=True):
    tp=collections.Counter();fp=collections.Counter();fn=collections.Counter();pol=[]
    for pid,segs,gold in data:
        gp=set();pp=set()
        for s,g in zip(segs,gold):
            p=detect(s); gp|=g; pp|=p
            for c in CATS:
                if c in g and c in p: tp[c]+=1
                elif c in p: fp[c]+=1
                elif c in g: fn[c]+=1
        pol.append((gp,pp))
    def prf(a,b,c):
        P=a/(a+b) if a+b else 0;R=a/(a+c) if a+c else 0;return P,R,(2*P*R/(P+R) if P+R else 0)
    out={}
    for c in CATS: out[c]=prf(tp[c],fp[c],fn[c])+(sum((c in g)==(c in p) for g,p in pol)/len(pol),)
    out["micro"]=prf(sum(tp.values()),sum(fp.values()),sum(fn.values()))
    import statistics as st
    gs=[sum(W[c] for c in g) for g,_ in pol]; ps=[sum(W[c] for c in p) for _,p in pol]
    band=lambda x:"Low" if x<.4 else ("Moderate" if x<.7 else "High")
    out["scores"]=(st.mean(abs(a-b) for a,b in zip(gs,ps)),st.correlation(gs,ps),sum(band(a)==band(b) for a,b in zip(gs,ps))/len(pol),
                   collections.Counter(band(x) for x in gs),collections.Counter(band(x) for x in ps))
    if verbose:
        for c in CATS: print(f"  {c:11s} P={out[c][0]:.3f} R={out[c][1]:.3f} F1={out[c][2]:.3f} polAcc={out[c][3]:.3f}")
        print(f"  micro      P={out['micro'][0]:.3f} R={out['micro'][1]:.3f} F1={out['micro'][2]:.3f}")
        s=out["scores"]; print(f"  scores MAE={s[0]:.3f} r={s[1]:.3f} sameBand={s[2]:.3f} gold={dict(s[3])} pred={dict(s[4])}")
    return out
