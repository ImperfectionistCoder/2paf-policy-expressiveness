"""Worked example of Section 5.7: AHP prioritization between a patient preference and the
GlucoseInsights policy for the purpose-of-use conflict.

Criteria priorities are taken from Sadki and El Bakkali [29], Fig. 4.2 (consistency ratio 0.048).
Pairwise judgments between the two alternatives are the authors' assumptions for this example,
on Saaty's 1-9 scale: a value a means the patient preference is a times more important than the
provider policy with respect to that criterion.
"""
criteria = {                 # priority from [29]   judgment (preference vs policy)
    "Category of data":        (0.04355, 5),  # blood glucose and heart rate are health data
    "Purpose":                 (0.47402, 7),  # feature improvement is not a care purpose
    "Laws and regulation":     (0.2570,  5),  # health data: GDPR Art. 9 conditions
    "Reputation":              (0.1480,  3),  # Fundamentalist profile weighs reputation
    "Type of organization":    (0.04277, 3),  # private app provider, not a care provider
    "Time of retention":       (0.0346,  1),  # not involved in this conflict
}
pref = policy = 0.0
for name, (w, a) in criteria.items():
    lp = a / (1 + a)          # local priority of the preference (2x2 matrix, always consistent)
    pref += w * lp; policy += w * (1 - lp)
    print(f"{name:22s} weight {w:.4f}  preference {lp:.3f}  policy {1-lp:.3f}")
tot = pref + policy
print(f"\nGlobal priority: patient preference {pref/tot:.3f}, GlucoseInsights policy {policy/tot:.3f}")
