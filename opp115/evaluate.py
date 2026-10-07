import csv, glob, os, collections, json
from pipeline import detect, CATS
csv.field_size_limit(10**9)
MAP={"First Party Collection/Use":"Collection","Data Retention":"Retention","Third Party Sharing/Collection":"Sharing",
"User Access, Edit and Deletion":"Access","User Choice/Control":"Control","Data Security":"Security","International and Specific Audiences":"Regulatory"}
W=dict(zip(CATS,[0.1781,0.1233,0.1644,0.1370,0.1507,0.1370,0.1096]))
import os
base=os.environ.get("OPP115_DIR","OPP-115")
seg_tp=collections.Counter(); seg_fp=collections.Counter(); seg_fn=collections.Counter()
pol=[]
for f in sorted(glob.glob(base+"/annotations/*.csv")):
    pid=os.path.basename(f)[:-4]
    segs=open(f"{base}/sanitized_policies/{pid}.html",encoding="utf-8",errors="ignore").read().split("|||")
    votes=collections.defaultdict(lambda: collections.defaultdict(set))
    for r in csv.reader(open(f,encoding="utf-8",errors="ignore")):
        if len(r)>5 and r[5] in MAP: votes[int(r[4])][MAP[r[5]]].add(r[2])
    gold_pol=set(); pred_pol=set()
    for i,s in enumerate(segs):
        g={c for c,a in votes[i].items() if len(a)>=2}; p=detect(s)
        gold_pol|=g; pred_pol|=p
        for c in CATS:
            if c in g and c in p: seg_tp[c]+=1
            elif c in p: seg_fp[c]+=1
            elif c in g: seg_fn[c]+=1
    pol.append((pid,gold_pol,pred_pol))
def prf(tp,fp,fn):
    P=tp/(tp+fp) if tp+fp else 0; R=tp/(tp+fn) if tp+fn else 0; F=2*P*R/(P+R) if P+R else 0; return P,R,F
res={"segment":{},"policy":{}}
print("SEGMENT LEVEL (paragraphs)            P      R      F1   support")
T=[0,0,0]
for c in CATS:
    P,R,F=prf(seg_tp[c],seg_fp[c],seg_fn[c]); T[0]+=seg_tp[c];T[1]+=seg_fp[c];T[2]+=seg_fn[c]
    print(f"  {c:11s}                     {P:.3f}  {R:.3f}  {F:.3f}  {seg_tp[c]+seg_fn[c]}"); res["segment"][c]=(P,R,F)
P,R,F=prf(*T); print(f"  micro-average                   {P:.3f}  {R:.3f}  {F:.3f}"); res["segment"]["micro"]=(P,R,F)
print("\nPOLICY LEVEL (category present anywhere)   P      R      F1   accuracy")
for c in CATS:
    tp=sum(c in g and c in p for _,g,p in pol); fp=sum(c not in g and c in p for _,g,p in pol); fn=sum(c in g and c not in p for _,g,p in pol)
    acc=sum((c in g)==(c in p) for _,g,p in pol)/len(pol); P,R,F=prf(tp,fp,fn)
    print(f"  {c:11s}                          {P:.3f}  {R:.3f}  {F:.3f}  {acc:.3f}"); res["policy"][c]=(P,R,F,acc)
band=lambda x:"Low" if x<.4 else ("Moderate" if x<.7 else "High")
gs=[sum(W[c] for c in g) for _,g,_ in pol]; ps=[sum(W[c] for c in p) for _,_,p in pol]
import statistics as st
mae=st.mean(abs(a-b) for a,b in zip(gs,ps)); r=st.correlation(gs,ps)
ba=sum(band(a)==band(b) for a,b in zip(gs,ps))/len(pol)
print(f"\nSCORES: gold vs pipeline  MAE={mae:.3f}  Pearson r={r:.3f}  same band={ba:.3f}")
print("gold bands",collections.Counter(band(x) for x in gs),"  pipeline bands",collections.Counter(band(x) for x in ps))
json.dump(res,open("results.json","w"),indent=1)
