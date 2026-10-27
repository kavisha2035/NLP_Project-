import json, itertools
from main import run

docs = json.load(open("data/docs.json")); g = json.load(open("data/gold.json"))
r = run(docs)
ids = [x["id"] for x in r["ev"]]
allp = {frozenset(p) for p in itertools.combinations(ids, 2) if p[0][0] != p[1][0]}
gc = {frozenset(p) for p in g["conf"]}
ga = {p for p in allp if len({g["ev"][i] for i in p}) == 1}


def prf(P, G):
    tp = len(P & G); p = tp / len(P) if P else 0; rc = tp / len(G) if G else 0
    return p, rc, (2 * p * rc / (p + rc) if p + rc else 0), len(P)


S = [("1. NLI only (no alignment)", r["nli"]),
     ("2. NLI + alignment", r["nli"] & r["al"]),
     ("3. STN temporal only", r["tmp"]),
     ("4. Full: alignment + STN + NLI", (r["nli"] & r["al"]) | r["tmp"])]
L = [f"pairs={len(allp)}  gold conflicts={len(gc)}  align={r['how']}  nli={r['mode']}\n",
     "| system | P | R | F1 | #pred |", "|---|---|---|---|---|"]
for n, P in S:
    p, rc, f, k = prf(P, gc); L.append(f"| {n} | {p:.2f} | {rc:.2f} | {f:.2f} | {k} |")
p, rc, f, k = prf(r["al"], ga)
L += ["", f"Event alignment (aligned pairs vs gold same-event pairs): P={p:.2f} R={rc:.2f} F1={f:.2f}"]
for n, P in S[-1:]:
    L += ["", "Full-system errors:", "  FP: " + str(sorted(map(sorted, P - gc))), "  FN: " + str(sorted(map(sorted, gc - P)))]
t = "\n".join(L); print(t); open("out/results.md", "w").write(t)
