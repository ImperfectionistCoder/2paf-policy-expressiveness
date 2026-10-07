import re, html, spacy
from keywords import KEYWORDS
nlp = spacy.load("en_core_web_sm", disable=["parser","ner"])
CATS = list(KEYWORDS)
def lem(text):
    return [t.lemma_.lower() for t in nlp(text) if not t.is_stop and not t.is_punct and not t.is_space]
# lemmatize the keyword phrases the same way (stop-words removed), so matching is consistent
KW = {c: [" ".join(lem(k)) or k for k in ks] for c, ks in KEYWORDS.items()}
def clean(seg):
    seg = re.sub(r"<[^>]+>", " ", seg); return html.unescape(re.sub(r"\s+", " ", seg)).strip()
def detect(seg_text):
    toks = lem(clean(seg_text)); s = " " + " ".join(toks) + " "
    return {c for c, ks in KW.items() if any((" "+k+" ") in s for k in ks if k)}
