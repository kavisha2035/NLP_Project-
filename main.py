import json, itertools, os
from datetime import date
from ext import ext
from align import align
from stn import edges, bounds, disjoint, all_conf, INF
from nli import contra, mode


def run(docs):
    ev = [x for d in docs for x in ext(d)]
    ev, how = align(ev)
    E = edges(ev)
    B = {s: bounds([e for e in E if e[3] == s]) for s in sorted({x["src"] for x in ev})}
    pairs = [(a, b) for a, b in itertools.combinations(ev, 2) if a["src"] != b["src"]]
    fs = lambda a, b: frozenset((a["id"], b["id"]))
    nli = {fs(a, b) for a, b in pairs if contra(a["s"], b["s"])}        # all cross-source pairs
    al = {fs(a, b) for a, b in pairs if a["cl"] == b["cl"]}             # aligned pairs
    tmp = set()                                                         # temporal conflicts (STN)
    for a, b in pairs:
        if a["cl"] == b["cl"]:
            x, y = B[a["src"]].get(a["cl"]), B[b["src"]].get(b["cl"])
            if x and y and disjoint(x, y): tmp.add(fs(a, b))
    return dict(ev=ev, E=E, B=B, al=al, nli=nli, tmp=tmp, cyc=all_conf(E), how=how, mode=mode())


def d(o): return date.fromordinal(o).isoformat()


def iv(x):
    if x is None or (x[0] <= -INF and x[1] >= INF): return "?"
    lo = d(x[0]) if x[0] > -INF else "?"; hi = d(x[1]) if x[1] < INF else "?"
    return lo if lo == hi else f"{lo}..{hi}"


def main():
    docs = json.load(open("data/docs.json")); r = run(docs); ev = r["ev"]; os.makedirs("out", exist_ok=True)
    cl = {}
    for x in ev: cl.setdefault(x["cl"], []).append(x)
    nm = {c: f'{c}: {" ".join(v[0]["s"].split()[:6])}...' for c, v in cl.items()}
    nm["Z"] = "origin"
    conf = r["tmp"] | (r["nli"] & r["al"])
    byid = {x["id"]: x for x in ev}
    rows = []
    for c, v in cl.items():
        ivs = {x["src"]: r["B"][x["src"]].get(c) for x in v}
        fin = [i for i in ivs.values() if i and i[0] > -INF and i[1] < INF]
        lo = max([i[0] for i in fin], default=None); hi = min([i[1] for i in fin], default=None)
        tc = lo is not None and lo > hi
        nc = any(frozenset((a["id"], b["id"])) in r["nli"] for a, b in itertools.combinations(v, 2))
        rows.append(dict(c=c, v=v, ivs=ivs, tc=tc, nc=nc, key=min([i[0] for i in fin], default=10 ** 9)))
    rows.sort(key=lambda z: z["key"])

    L = [f"# Consensus timeline (align={r['how']}, nli={r['mode']})\n"]
    for z in rows:
        flag = "CONFLICT" + (" [temporal]" if z["tc"] else "") + (" [claim]" if z["nc"] else "") if (z["tc"] or z["nc"]) else "ok"
        L.append(f"## {nm[z['c']]}  -> {flag}")
        for x in z["v"]: L.append(f"- [{x['src']}] {iv(z['ivs'][x['src']]):<23} {x['s']}")
        L.append("")
    L.append("# Conflict pairs")
    for p in sorted(map(sorted, conf)):
        a, b = byid[p[0]], byid[p[1]]
        why = ("temporal" if frozenset(p) in r["tmp"] else "") + ("+" if frozenset(p) in r["tmp"] and frozenset(p) in r["nli"] else "") + ("claim(NLI)" if frozenset(p) in r["nli"] else "")
        L.append(f"- {p[0]} vs {p[1]} ({why})\n    {a['s']}\n    {b['s']}")
    L.append("\n# Negative cycles in the merged STN (why the sources are inconsistent)")
    def ed(e):
        u, v, w, s = e
        if u == "Z": return f"[{s}] {nm[v]} <= {d(w)}"
        if v == "Z": return f"[{s}] {nm[u]} >= {d(-w)}"
        return f"[{s}] t({nm[v]}) - t({nm[u]}) <= {w}d"
    for i, c in enumerate(r["cyc"], 1):
        L.append(f"- cycle {i} (total weight {sum(e[2] for e in c)}, sources {sorted({e[3] for e in c})}):")
        L += [f"    {ed(e)}" for e in c]
    txt = "\n".join(L); open("out/timeline.md", "w").write(txt); print(txt)
    json.dump(dict(conflicts=sorted(map(sorted, conf))), open("out/conflicts.json", "w"), indent=1)

    try:
        from pyvis.network import Network
        net = Network(height="700px", width="100%", directed=True, cdn_resources="in_line")
        col = dict(A="#378ADD", B="#D85A30", C="#1D9E75")
        for s in r["B"]: net.add_node(f"src_{s}", label=f"source {s}", color=col.get(s, "#888"), shape="box")
        for z in rows:
            bad = z["tc"] or z["nc"]
            net.add_node(z["c"], label=nm[z["c"]], color="#E24B4A" if bad else "#97C459", shape="dot", size=18,
                         title="<br>".join(f"[{x['src']}] {x['s']}" for x in z["v"]))
            for x in z["v"]: net.add_edge(z["c"], f"src_{x['src']}", label="REPORTED_BY", dashes=True, color="#AAAAAA", font={"size": 8})
        dated = [z["c"] for z in rows if z["key"] < 10 ** 9]
        for a, b in zip(dated, dated[1:]): net.add_edge(a, b, label="BEFORE", color="#444444", width=2)
        net.write_html("out/graph.html")
    except Exception as e:
        print("graph skipped:", e)


if __name__ == "__main__":
    main()
