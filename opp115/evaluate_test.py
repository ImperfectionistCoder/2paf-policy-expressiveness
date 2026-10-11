"""Evaluation on the 40 held-out OPP-115 test policies (Section 5.6, Table 11)."""
from common import load_all, split, evaluate
import detect
dev, test = split(load_all())
print("Test set:", len(test), "policies")
evaluate(test, detect.detect)
