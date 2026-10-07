import csv,glob,os,collections,sys
os.chdir(os.environ.get("OPP115_DIR","OPP-115"))
csv.field_size_limit(10**9)
MAP={"First Party Collection/Use":"Collection","Data Retention":"Retention","Third Party Sharing/Collection":"Sharing",
"User Access, Edit and Deletion":"Access","User Choice/Control":"Control","Data Security":"Security","International and Specific Audiences":"Regulatory"}
CATS=["Collection","Retention","Sharing","Access","Control","Security","Regulatory"]
def load(folder,majority=False):
    out={}
    for f in sorted(glob.glob(folder+"/*.csv")):
        pid=os.path.basename(f)[:-4]
        if not majority:
            cats={MAP[r[5]] for r in csv.reader(open(f,encoding="utf-8",errors="ignore")) if len(r)>5 and r[5] in MAP}
        else:
            by=collections.defaultdict(set)
            for r in csv.reader(open(f,encoding="utf-8",errors="ignore")):
                if len(r)>5 and r[5] in MAP: by[MAP[r[5]]].add(r[2])
            cats={c for c,a in by.items() if len(a)>=2}
        out[pid]=cats
    return out
w=[0.1781,0.1233,0.1644,0.1370,0.1507,0.1370,0.1096]
for name,data in [("consolidated 0.75",load("consolidation/threshold-0.75-overlap-similarity")),("raw, >=2 of annotators",load("annotations",True))]:
    n=len(data); print(f"\n== {name}: {n} policies")
    for c in CATS: print(f"  {c:11s} {sum(c in s for s in data.values()):3d}/{n}")
    k=collections.Counter(len(s) for s in data.values()); print("  #categories per policy:",dict(sorted(k.items())))
    sc=[sum(wi for wi,c in zip(w,CATS) if c in s) for s in data.values()]
    full=sum(abs(x-1)<1e-9 for x in sc)
    print(f"  score=1.0: {full}/{n}  High(>=.7): {sum(x>=.7 for x in sc)}  Moderate: {sum(.4<=x<.7 for x in sc)}  Low: {sum(x<.4 for x in sc)}  min {min(sc):.3f} median {sorted(sc)[n//2]:.3f}")
