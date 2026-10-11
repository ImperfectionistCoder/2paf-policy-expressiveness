"""Text processing shared by detection and keyword selection (Algorithm 1, lines 3 to 5)."""
import re, html, spacy
nlp = spacy.load("en_core_web_sm", disable=["parser", "ner"])

def lem(text):
    """Tokenize, remove stop-words and punctuation, and lemmatize."""
    return [t.lemma_.lower() for t in nlp(text) if not t.is_stop and not t.is_punct and not t.is_space]

def clean(seg):
    """Strip HTML tags and normalize whitespace."""
    seg = re.sub(r"<[^>]+>", " ", seg)
    return html.unescape(re.sub(r"\s+", " ", seg)).strip()
