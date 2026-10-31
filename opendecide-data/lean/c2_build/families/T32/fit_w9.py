"""W9 fit (T32 A49 d fix round): fits BASE_ACCEPT, TWIN_ACCEPT, NN_CUTS and a re-fitted STATUS_TWIN_KEEP so that the stratum mix
(NN tercile x depth) of the emitted ch_status rows is the same for every gold, with emitted gold shares at 20% each.
Spec-level only (no render, no model). python -B families/T32/fit_w9.py N OUT.json  (from lean/c2_build)."""
import json, sys, time, importlib, collections
from pathlib import Path
sys.dont_write_bytecode = True
C2 = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(C2))
import numpy as np
import gen_full_c2 as G

N = int(sys.argv[1]); OUT = sys.argv[2]
FIT_BASE = 61_000_000
t0 = time.time()
with G.loader_patch("T32"):
    with G.PL.open_family("T32") as kit:
        pl = kit.plugin
        P = sys.modules[type(pl).__module__]
        ON = "--on" in sys.argv
        P.BAL_OFF = not ON
        samplers = ["S1", "S2", "S3", "S4"]
        bases, k = [], 0
        while len(bases) < N:
            seed, smp = FIT_BASE + k // 4, samplers[k % 4]; k += 1
            if P._draw(P.BASE_SHARES, P._strat("qform", smp, idx=seed // 2, size=50)) != "ch_status":
                continue
            try:
                sp = pl.sample(seed, smp)
            except Exception as e:
                continue
            if sp.qform != "ch_status":
                continue
            bases.append(sp)
        print("bases", len(bases), round(time.time() - t0), "s", flush=True)

        def raw(spec):
            sl = spec.all_slots()
            nn = sum(1 + sum(1 for ss in m["bind"].values() if sl[ss].kind == "date") for m in spec.structure["msgs"])
            p = pl._plan(spec)
            dep = sum(1 for e in (p.cond, p.ext_reply, p.done, p.retract, p.release) if p.counted(e))
            return nn, min(dep, 3)
        info = []
        for sp in bases:
            st = pl._fold(sp)[0]
            pool = pl._twin_pool(sp)
            info.append({"status": st, "z": raw(sp), "seed": (sp.sampler, sp.seed),
                         "pool": [(c, raw(c[2])) for c in pool]})
        print("pools", round(time.time() - t0), "s", flush=True)

DEP_OK = (1, 2)
if "--hist" in sys.argv:
    for s_ in ("kept", "broken", "not_yet_due", "not_triggered", "waived"):
        h = collections.Counter(i["z"][0] for i in info if i["status"] == s_ and i["z"][1] in (1, 2)); n = sum(h.values())
        print("NNhist", s_, n, {k: round(h[k] / n, 3) for k in sorted(h)})
        h = collections.Counter(z[0] for i in info for c, z in i["pool"] if c[3] == s_ and z[1] in (1, 2)); n = sum(h.values())
        print("NNhist twin->", s_, n, {k: round(h[k] / n, 3) for k in sorted(h)})
def raw_ok(r):
    return r[1] in DEP_OK
nns = np.array([i["z"][0] for i in info if raw_ok(i["z"])] + [z[0] for i in info for _, z in i["pool"] if raw_ok(z)])
cuts = (8, 9, 10)
def zs(r):
    return f"{sum(r[0] > c for c in cuts)}{r[1]}"
for i in info:
    i["zs"] = zs(i["z"]); i["pool"] = [(c, zs(z)) for c, z in i["pool"]]
STAT = ["kept", "broken", "not_yet_due", "not_triggered", "waived"]
Z = [f"{a}{d}" for a in (0, 1, 2, 3) for d in DEP_OK]
R_CAP = 4.0
FLOOR = float(sys.argv[sys.argv.index("--floor") + 1]) if "--floor" in sys.argv else 0.0
keep = dict(P.STATUS_TWIN_KEEP)
if ON:
    keep = {k: 1.0 for k in keep}
W_BASE = 1.17
nat = {s: sum(1 for i in info if i["status"] == s) / len(info) for s in STAT}
b = {s: dict(P.STATUS_SHARES)[s] for s in STAT}
A = {s: {z: 1.0 for z in Z} for s in STAT}
if ON:
    A = {s: dict(P.TWIN_ACCEPT[s]) for s in STAT}

def emit(keep, A, b):
    """expected emitted rows per (status, stratum), bases re-weighted from the natural to the base shares b; ALL strata."""
    cnt = {s: collections.Counter() for s in STAT}
    for i in info:
        w = b[i["status"]] / nat[i["status"]]
        cnt[i["status"]][i["zs"]] += W_BASE * w
        zmap = {id(c[2]): z for c, z in i["pool"]}
        acc = (lambda c: A[c[3]].get(zmap[id(c[2])], 0.0)) if A else None
        for c in P.pick_choice_twins(i["seed"], [c for c, _ in i["pool"]], "ch_status", keep, P.P_SECOND_TWIN, accept=acc):
            cnt[c[3]][zmap[id(c[2])]] += w
    return cnt

def show(tag, cnt):
    tot = sum(sum(c.values()) for c in cnt.values())
    print(tag, "shares", {s: round(sum(cnt[s].values()) / tot, 3) for s in STAT}, "twin-share-of-rows n/a")
    zall = sorted({z for s in STAT for z in cnt[s]})
    print("   strata", zall)
    for s in STAT:
        n = sum(cnt[s].values()); print("   ", s, [round(cnt[s][z] / n, 3) for z in zall])

show("BEFORE", emit(keep, None, b))
# base acceptance on Z (strata with depth 1-2): common target = pooled natural base mix on Z
pi = {z: sum(1 for i in info if i["zs"] == z) for z in Z}; tz = sum(pi.values()); pi = {z: pi[z] / tz for z in Z}
BASE = {}
for s in STAT:
    c = collections.Counter(i["zs"] for i in info if i["status"] == s); n = sum(c[z] for z in Z)
    r = {z: min(R_CAP, pi[z] / ((c[z] + 1.0) / (n + len(Z)))) for z in Z}
    m = max(r.values()); BASE[s] = {z: round(r[z] / m, 4) for z in Z}
if ON:
    BASE = P.BASE_ACCEPT
print("BASE_ACCEPT", json.dumps(BASE))
for rnd in range(10):
    # twin acceptance toward pi (twin-only counts, bases removed)
    cnt = emit(keep, A, b)
    for st in STAT:
        base_c = collections.Counter()
        for i in info:
            if i["status"] == st:
                base_c[i["zs"]] += W_BASE * b[st] / nat[st]
        tw = {z: max(cnt[st][z] - base_c[z], 0.0) for z in Z}
        n = sum(tw.values())
        r = {z: A[st][z] * min(R_CAP, pi[z] / ((tw[z] + 0.5) / (n + 0.5 * len(Z)))) for z in Z}
        m = max(r.values()); A[st] = {z: round(max(FLOOR, min(1.0, r[z] / m)), 4) for z in Z}
    # supply at keep = 1 (A applied): Y1[B][G] twins landing on G per base of status B
    k1 = {k: 1.0 for k in keep}
    Y1 = {B: {G: 0.0 for G in STAT} for B in STAT}
    for i in info:
        zmap = {id(c[2]): z for c, z in i["pool"]}
        for c in P.pick_choice_twins(i["seed"], [c for c, _ in i["pool"]], "ch_status", k1, 1.0,
                                     accept=lambda c: A[c[3]].get(zmap[id(c[2])], 0.0)):
            Y1[i["status"]][c[3]] += 1.0 / (nat[i["status"]] * len(info))
    # LP: max c  s.t.  W b_g + u_g = c, 0 <= u_g <= sum_B b_B Y1[B][g] (second twins excluded: first-twin supply), sum b = 1, b in band
    from scipy.optimize import linprog
    n = 5   # variables: b(5), u(5), c
    cvec = np.zeros(11); cvec[10] = -1
    Aeq = np.zeros((6, 11)); beq = np.zeros(6)
    for g in range(5):
        Aeq[g, g] = W_BASE; Aeq[g, 5 + g] = 1; Aeq[g, 10] = -1
    Aeq[5, :5] = 1; beq[5] = 1
    Aub = np.zeros((5, 11)); bub = np.zeros(5)
    for g, G in enumerate(STAT):
        Aub[g, 5 + g] = 1
        for B_i, B in enumerate(STAT):
            Aub[g, B_i] = -Y1[B][G]
    bounds = [(0.125, 0.30)] * 5 + [(0, None)] * 5 + [(0, None)]
    res_lp = linprog(cvec, A_ub=Aub, b_ub=bub, A_eq=Aeq, b_eq=beq, bounds=bounds)
    bsol = res_lp.x[:5]; usol = res_lp.x[5:10]; csol = res_lp.x[10]
    print("LP round", rnd, "c", round(csol, 3), "twins/base", round(5 * csol - W_BASE, 3), "b", dict(zip(STAT, np.round(bsol, 4))))
    b = {s_: round(float(bsol[k_]), 4) for k_, s_ in enumerate(STAT)}
    b["kept"] = round(1 - sum(v for k_, v in b.items() if k_ != "kept"), 4)
    # keep per status from the LP (first-twin supply share), then corrected toward uniform emitted shares
    for k_, G in enumerate(STAT):
        sup = sum(b[B] * Y1[B][G] for B in STAT)
        keep[G] = round(float(min(1.0, max(0.02, usol[k_] / max(sup, 1e-9)))), 4)
    for _ in range(6):
        cnt = emit(keep, A, b)
        E = {s_: sum(cnt[s_].values()) for s_ in STAT}; T = sum(E.values()) / 5
        for G in STAT:
            keep[G] = round(float(min(1.0, max(0.02, keep[G] * T / E[G]))), 4)
cnt = emit(keep, A, b); show("AFTER twins thinned + keep + base shares refit", cnt)
print("b", b); print("keep", keep)
# union: bases accepted ~ pi on Z (BASE_ACCEPT): replace base part by b-weighted pi
cntu = {s: collections.Counter() for s in STAT}
for s in STAT:
    for i in info:
        if i["status"] == s:
            pass
    nb = b[s] * len(info)
    for z in Z:
        cntu[s][z] += W_BASE * nb * pi[z]
    base_c = collections.Counter()
    for i in info:
        if i["status"] == s:
            base_c[i["zs"]] += W_BASE * b[s] / nat[s]
    for z in Z:
        cntu[s][z] += max(cnt[s][z] - base_c[z], 0.0) * len(info) / len(info)
show("UNION (bases follow pi on Z)", cntu)
res = {"n_bases": len(info), "seed_base": FIT_BASE, "NN_CUTS": cuts, "BASE_ACCEPT": BASE, "TWIN_ACCEPT": A, "STATUS_TWIN_KEEP": keep,
       "STATUS_SHARES": b, "pi": pi, "seconds": round(time.time() - t0)}
Path(OUT).write_text(json.dumps(res, indent=1)); print("saved", OUT)
