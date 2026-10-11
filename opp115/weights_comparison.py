"""Weighted vs equal-weight scores on the 115 OPP-115 policies (Section 5.6).

A category is present in a policy when at least 2 of the 3 annotators assigned it
to at least one segment. Weights are those of Table 7 (counts from the 13 coded studies).
"""
import csv, glob, os, collections, itertools, statistics as st
csv.field_size_limit(10**9)
MAP = {"First Party Collection/Use": "Collection", "Data Retention": "Retention",
       "Third Party Sharing/Collection": "Sharing", "User Access, Edit and Deletion": "Access",
       "User Choice/Control": "Control", "Data Security": "Security",
       "International and Specific Audiences": "Regulatory"}
CATS = ["Collection", "Retention", "Sharing", "Access", "Control", "Security", "Regulatory"]
COUNTS = dict(zip(CATS, [13, 9, 12, 10, 11, 10, 8]))
W = {c: COUNTS[c] / sum(COUNTS.values()) for c in CATS}
E = {c: 1 / 7 for c in CATS}

pol = {}
for f in glob.glob(os.path.join(os.environ.get("OPP115_DIR", "OPP-115"), "annotations", "*.csv")):
    votes = collections.defaultdict(set)
    for r in csv.reader(open(f, encoding="utf-8", errors="ignore")):
        if len(r) > 5 and r[5] in MAP:
            votes[MAP[r[5]]].add(r[2])
    pol[os.path.basename(f)] = {c for c, a in votes.items() if len(a) >= 2}

band = lambda x: "Low" if x < 0.4 - 1e-9 else ("Moderate" if x < 0.7 - 1e-9 else "High")
sw = {p: sum(W[c] for c in s) for p, s in pol.items()}
se = {p: sum(E[c] for c in s) for p, s in pol.items()}

def ranks(d):
    order = sorted(d, key=d.get); r = {}; i = 0
    while i < len(order):
        j = i
        while j + 1 < len(order) and abs(d[order[j + 1]] - d[order[i]]) < 1e-9:
            j += 1
        for k in order[i:j + 1]:
            r[k] = (i + j) / 2 + 1
        i = j + 1
    return r

keys = list(pol); rw, re_ = ranks(sw), ranks(se)
pairs = [(a, b) for a, b in itertools.combinations(keys, 2) if len(pol[a]) == len(pol[b]) and pol[a] != pol[b]]
print("Policies:", len(keys))
print("Band changes, weighted vs equal:", sum(band(sw[p]) != band(se[p]) for p in keys))
print("Spearman rank correlation:", round(st.correlation([rw[k] for k in keys], [re_[k] for k in keys]), 3))
print("Pairs tied under equal weights:", len(pairs), "| separated by the weights:", sum(abs(sw[a] - sw[b]) > 1e-9 for a, b in pairs))
print("Distinct score values: weighted", len({round(v, 6) for v in sw.values()}), "| equal", len({round(v, 6) for v in se.values()}))
