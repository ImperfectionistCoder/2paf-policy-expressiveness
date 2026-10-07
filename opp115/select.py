import pickle, collections, math
from common import CATS
from pipeline import lem
L=pickle.load(open("dev_lem.pkl","rb"))
# candidate pool: hand-written phrases per category + top discriminative uni/bi-grams mined from DEV only
HAND={
"Collection":["collect","gather","obtain","personal information","information collect","use information","purpose","provide information","automatically collect","log file","ip address","device information"],
"Retention":["retain","retention","keep information","keep personal information","long necessary","delete","period time","store information","retain information","archive","dispose","backup"],
"Sharing":["share","disclose","disclosure","third party","sell","sale","transfer","affiliate","partner","service provider","rent","merger acquisition"],
"Access":["access information","access personal information","review","update information","correct","edit","delete account","deletion","erase","request access","update account","change information","inaccurate"],
"Control":["opt","consent","choice","choose","preference","unsubscribe","withdraw","disable cookie","track","setting","decline","refuse cookie"],
"Security":["secure","security","encrypt","encryption","safeguard","protect information","ssl","tls","firewall","unauthorized access","breach","technical measure"],
"Regulatory":["law","regulation","coppa","california","child","13","european","eu","comply","jurisdiction","international","safe harbor","resident","parent","age"],
}
def grams(s):
    t=s.split(); return set(t)|{" ".join(t[i:i+2]) for i in range(len(t)-1)}
pos=collections.Counter(); df=collections.Counter(); seglab=[]
for s,g in L:
    gs=grams(s); seglab.append((s,g))
    for x in gs:
        df[x]+=1
        for c in g: pos[(c,x)]+=1
def has(s,k): return (" "+k+" ") in s
def f1(sel,c):
    tp=fp=fn=0
    for s,g in L:
        p=any(has(s,k) for k in sel)
        if p and c in g: tp+=1
        elif p: fp+=1
        elif c in g: fn+=1
    P=tp/(tp+fp) if tp+fp else 0; R=tp/(tp+fn) if tp+fn else 0
    return (2*P*R/(P+R) if P+R else 0),P,R
final={}
for c in CATS:
    hand=[" ".join(lem(h)) or h for h in HAND[c]]
    ncat=sum(c in g for _,g in L)
    mined=[x for (cc,x),n in pos.items() if cc==c and n>=5 and n/df[x]>=0.5]
    mined=sorted(mined,key=lambda x:-pos[(c,x)])[:40]
    pool=list(dict.fromkeys([h for h in hand if h]+mined))
    sel=[]; best=0
    while True:
        cand=[(f1(sel+[k],c)[0],k) for k in pool if k not in sel]
        if not cand: break
        sc,k=max(cand)
        if sc<=best+0.002: break
        sel.append(k); best=sc
    F,P,R=f1(sel,c); final[c]=sel
    print(f"{c:11s} F1={F:.3f} P={P:.3f} R={R:.3f} n={ncat}  keywords={sel}")
import json; json.dump(final,open("keywords_v2.json","w"),indent=1)
