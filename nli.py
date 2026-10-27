import re

_m = None
MON = r"(January|February|March|April|May|June|July|August|September|October|November|December)"
WORDS = "one two three four five six seven eight nine ten".split()


def load():
    global _m
    if _m is None:
        try:
            from transformers import pipeline
            _m = pipeline("text-classification", model="cross-encoder/nli-deberta-v3-small", top_k=None)
        except Exception:
            _m = False
    return _m


def mode():
    return "deberta" if load() else "heuristic"


def nums(t):
    t = re.sub(MON + r"\s+\d{1,2}", "", t); t = re.sub(r"\b\d{4}\b", "", t)
    return set(re.findall(r"\d+", t)) | {w for w in t.lower().split() if w.strip(".,") in WORDS}


def heur(a, b):
    # fallback if the NLI model cannot be downloaded: differing numbers or negation mismatch
    na, nb = nums(a), nums(b)
    neg = lambda t: bool(re.search(r"\b(no|not|never|denied)\b", t.lower()))
    return (bool(na) and bool(nb) and na != nb) or neg(a) != neg(b)


def contra(a, b):
    m = load()
    if m is False: return heur(a, b)
    for x, y in ((a, b), (b, a)):
        r = m({"text": x, "text_pair": y}, top_k=None)
        if r and isinstance(r[0], list): r = r[0]
        if max(r, key=lambda z: z["score"])["label"].lower().startswith("contra"): return True
    return False
