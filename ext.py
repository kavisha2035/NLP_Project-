import os, re
from datetime import datetime
os.environ["TZ"] = "UTC"  # dateparser/tzlocal crash on some non-zoneinfo TZ names
import spacy, dateparser

nlp = spacy.load("en_core_web_sm")
NUM = dict(a=1, one=1, two=2, three=3, four=4, five=5, six=6, seven=7)
OFF = re.compile(r"\b(a|one|two|three|four|five|six|seven|\d+)\s+days?\s+(later|after)\b"
                 r"|\b(the\s+(next|following)\s+day|the\s+day\s+after)\b", re.I)


def off(t):
    # "two days later" / "the next day" -> offset in days from the previous event
    m = OFF.search(t)
    if not m: return None
    g = m.group(1)
    return 1 if g is None else (int(g) if g.isdigit() else NUM[g.lower()])


def when(s, pub):
    # first usable DATE entity -> (lo, hi) as day ordinals; vague "week" -> interval
    for e in s.ents:
        if e.label_ != "DATE" or OFF.search(e.text): continue
        if not re.search(r"[A-Za-z]+\s+\d{1,2}|\d{1,2}\s+[A-Za-z]+|week", e.text): continue  # skip bare years
        d = dateparser.parse(e.text, settings={"RELATIVE_BASE": pub, "PREFER_DATES_FROM": "past"})
        if d:
            o = d.toordinal()
            return (o - 3, o + 3) if "week" in e.text.lower() else (o, o)
    return None, None


def ext(d):
    pub = datetime.fromisoformat(d["pub"]); out = []
    for i, t in enumerate(d["sents"]):
        s = nlp(t)
        if not any(w.pos_ in ("VERB", "AUX") for w in s): continue
        lo, hi = when(s, pub)
        k = None if lo is not None else off(t)
        out.append(dict(id=f'{d["src"]}{i}', src=d["src"], s=t, lo=lo, hi=hi, k=k,
                        prev=out[-1]["id"] if out else None,
                        ents=sorted({e.text for e in s.ents})))
    return out
