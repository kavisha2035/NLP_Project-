TH = {"minilm": 0.5, "tfidf": 0.2}


def emb(txt):
    try:
        from sentence_transformers import SentenceTransformer
        return SentenceTransformer("all-MiniLM-L6-v2").encode(txt, normalize_embeddings=True), "minilm"
    except Exception:
        from sklearn.feature_extraction.text import TfidfVectorizer
        from sklearn.preprocessing import normalize
        x = TfidfVectorizer(stop_words="english", ngram_range=(1, 2)).fit_transform(txt)
        return normalize(x).toarray(), "tfidf"


def align(ev, th=None):
    # greedy cross-source merge by similarity; a cluster never holds two sentences of one source
    e, how = emb([x["s"] for x in ev]); S = e @ e.T
    th = th if th is not None else TH[how]
    n = len(ev)
    for i in range(n):                      # time overlap: same normalized date -> likelier same event
        for j in range(i + 1, n):
            a, b = ev[i], ev[j]
            if a["lo"] is not None and (a["lo"], a["hi"]) == (b["lo"], b["hi"]): S[i, j] += 0.15; S[j, i] += 0.15
    n = len(ev); par = list(range(n)); ss = [{x["src"]} for x in ev]

    def f(i):
        while par[i] != i: par[i] = par[par[i]]; i = par[i]
        return i

    pr = sorted(((S[i, j], i, j) for i in range(n) for j in range(i + 1, n)
                 if ev[i]["src"] != ev[j]["src"]), reverse=True)
    for s, i, j in pr:
        if s < th: break
        a, b = f(i), f(j)
        if a != b and not (ss[a] & ss[b]):
            par[b] = a; ss[a] |= ss[b]
    for i, x in enumerate(ev): x["cl"] = f"E{f(i)}"
    return ev, how
