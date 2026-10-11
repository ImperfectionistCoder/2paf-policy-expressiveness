"""Category detection (Algorithm 1, lines 6 to 8) with the keywords reported in Section 5.6."""
import json, os
from textproc import lem, clean
KW = json.load(open(os.path.join(os.path.dirname(__file__), "keywords.json")))

def detect(seg):
    """Return the set of categories whose keywords occur in the lemmatized segment."""
    s = " " + " ".join(lem(clean(seg))) + " "
    return {c for c, ks in KW.items() if any((" " + k + " ") in s for k in ks)}
