import json
from pipeline import lem, clean
KW=json.load(open(__import__("os").path.join(__import__("os").path.dirname(__file__),"keywords_v2.json")))
def detect(seg):
    s=" "+" ".join(lem(clean(seg)))+" "
    return {c for c,ks in KW.items() if any((" "+k+" ") in s for k in ks)}
