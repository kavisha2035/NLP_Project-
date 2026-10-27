INF = 10 ** 9
# Simple Temporal Network: edge (u, v, w, src) means t(v) - t(u) <= w. "Z" is the time origin.


def edges(ev):
    cl = {x["id"]: x["cl"] for x in ev}; E = []
    for x in ev:
        c = x["cl"]
        if x["lo"] is not None:
            E += [("Z", c, x["hi"], x["src"]), (c, "Z", -x["lo"], x["src"])]   # lo <= t(c) <= hi
        elif x["k"] is not None and x["prev"]:
            p = cl[x["prev"]]
            if p != c:
                E += [(p, c, x["k"], x["src"]), (c, p, -x["k"], x["src"])]     # t(c) - t(p) = k
    return E


def bounds(E):
    # Floyd-Warshall closure -> tightest [lo, hi] implied for every cluster by this edge set
    N = sorted({e[0] for e in E} | {e[1] for e in E} | {"Z"}); ix = {n: i for i, n in enumerate(N)}; n = len(N)
    D = [[INF] * n for _ in range(n)]
    for i in range(n): D[i][i] = 0
    for u, v, w, s in E: D[ix[u]][ix[v]] = min(D[ix[u]][ix[v]], w)
    for k in range(n):
        for i in range(n):
            a = D[i][k]
            if a >= INF: continue
            for j in range(n):
                b = D[k][j]
                if b < INF and a + b < D[i][j]: D[i][j] = a + b
    r = {}
    for c in N:
        if c == "Z": continue
        h, l = D[ix["Z"]][ix[c]], D[ix[c]][ix["Z"]]
        r[c] = (-l if l < INF else -INF, h if h < INF else INF)
    return r


def disjoint(a, b):
    return a[1] < b[0] or b[1] < a[0]


def neg_cycle(E):
    # Bellman-Ford; a negative cycle = inconsistent constraints, and the cycle is the explanation
    N = {e[0] for e in E} | {e[1] for e in E}; d = {n: 0 for n in N}; p = {}; x = None
    for _ in range(len(N) + 1):
        x = None
        for u, v, w, s in E:
            if d[u] + w < d[v]: d[v] = d[u] + w; p[v] = (u, v, w, s); x = v
        if x is None: return None
    for _ in range(len(N)): x = p[x][0]
    c, y = [], x
    while True:
        e = p[y]; c.append(e); y = e[0]
        if y == x: break
    return c[::-1]


def all_conf(E, mx=10):
    out, E = [], list(E)
    while len(out) < mx and (c := neg_cycle(E)):
        out.append(c); E.remove(c[0])
    return out
