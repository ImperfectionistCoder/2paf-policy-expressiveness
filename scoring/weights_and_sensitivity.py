import numpy as np
cats=["Collection","Retention","Sharing","Access","Control","Security","Regulatory"]
R={42:"1011100",43:"1011010",14:"1001111",30:"1111111",33:"1111111",37:"1111111",50:"1111111",
   38:"1111111",32:"1111101",41:"1111111",46:"1110010",47:"1110110",48:"1010100"}
# AWS, Firebase (corrected: all seven categories), GlucoseInsights (synthetic policy)
P=np.array([[1]*7,[1]*7,[1,0,1,0,1,1,0]]); names=["AWS","Firebase","Glucose"]
old=np.array([22,15,17,13,22,10,11])/110
band=lambda s:"Low" if s<.4 else ("Moderate" if s<.7 else "High")
def run(tag,rows):
    M=np.array([[int(c) for c in r] for r in rows.values()]); n=len(M)
    w=M.sum(0)/M.sum()
    print(f"\n=== {tag}: {n} studies, total marks {M.sum()}")
    for c,k,x,o in zip(cats,M.sum(0),w,old): print(f"  {c:11s} count {k:2d}/{n}  w={x:.4f}  (old {o:.4f})")
    s=P@w; print("  scores:",{a:(round(b,4),band(b)) for a,b in zip(names,s)})
    lo=[P@(np.delete(M,i,0).sum(0)/np.delete(M,i,0).sum()) for i in range(n)]; lo=np.array(lo)
    print("  LOSO Glucose range",lo[:,2].min().round(4),lo[:,2].max().round(4)," Firebase",lo[:,1].min().round(4),lo[:,1].max().round(4))
    rng=np.random.default_rng(42); S=[]
    for _ in range(10000):
        m=M[rng.integers(0,n,n)]; S.append(P@(m.sum(0)/m.sum()))
    S=np.array(S); print("  boot 95% Glucose",np.percentile(S[:,2],[2.5,97.5]).round(4),"Firebase",np.percentile(S[:,1],[2.5,97.5]).round(4))
    print("  boot Glucose High %:",round(100*np.mean(S[:,2]>=.7),1),"  ranking stable %:",round(100*np.mean((S[:,0]>=S[:,1])&(S[:,1]>S[:,2])),1))
    return w
run("13 coded studies",R)

print("\n##### Table 7 / Table 10 numbers (13 coded studies)")
import itertools
M=np.array([[int(c) for c in r] for r in R.values()]); n=len(M); w=M.sum(0)/M.sum()
rng=np.random.default_rng(42); W=[];S=[]
for _ in range(10000):
    m=M[rng.integers(0,n,n)]; ww=m.sum(0)/m.sum(); W.append(ww); S.append(P@ww)
W=np.array(W); S=np.array(S)
lo,hi=np.percentile(W,[2.5,97.5],0)
for c,x,a,b,k in sorted(zip(cats,w,lo,hi,M.sum(0)),key=lambda t:-t[1]): print(f"{c:11s} {k}/13 {100*k/13:.0f}% w={x:.4f} [{a:.4f}, {b:.4f}]")
print("equal:",(P@(np.ones(7)/7)).round(4))
L=np.array([P@(np.delete(M,i,0).sum(0)/np.delete(M,i,0).sum()) for i in range(n)])
print("LOSO min",L.min(0).round(4),"max",L.max(0).round(4),"band changes",sum(any(band(x)!=band(y) for x,y in zip(s,P@w)) for s in L))
print("boot score CI",np.percentile(S,[2.5,97.5],0).round(4))
bb=np.array([[band(x) for x in s] for s in S])
for j,nm in enumerate(names): print(nm,"same band %",round(100*np.mean(bb[:,j]==band((P@w)[j])),1))
fl=[]
for a in np.arange(.30,.51,.05):
  for b in np.arange(.60,.81,.05):
    bs=["Low" if x<a else ("Moderate" if x<b else "High") for x in P@w]
    if bs!=["High","High","Moderate"]: fl.append((round(a,2),round(b,2),bs))
print("threshold changes",fl)
for k in (1,2,3,4):
  sc=[1-sum(w[list(c)]) for c in itertools.combinations(range(7),k)]
  print(f"missing {k}: min {min(sc):.4f} max {max(sc):.4f}")
# which pairs drop below .7
print([ (cats[i],cats[j],round(1-w[i]-w[j],4)) for i,j in itertools.combinations(range(7),2) if 1-w[i]-w[j]<.7])
print("Glucose exact", P[2]@M.sum(0), "/", M.sum(), " Firebase", P[1]@M.sum(0),"/",M.sum())
