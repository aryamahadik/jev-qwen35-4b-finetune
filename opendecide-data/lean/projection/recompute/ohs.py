import json, sys, os
from collections import defaultdict
import numpy as np
os.chdir("/Users/aryamahadik/Documents/jev/opendecide-data/lean")
SPLIT = sys.argv[1]
MODELS = sys.argv[2].split(",")
JEVS = ["jev_guard", "jev_r2_guard"]
rows = {json.loads(l)["id"]: json.loads(l) for l in open(f"data/{SPLIT}.jsonl")}
rp = f"data/{SPLIT}_relations.jsonl"
rels = [json.loads(l) for l in open(rp)] if os.path.exists(rp) else []
base = [i for i, r in rows.items() if r["role"] in ("aff", "choice") and not any(i.endswith(s) for s in ("_neg", "_dneg", "_para", "_yn", "_perm"))]
P = {n: {json.loads(l)["id"]: json.loads(l)["probs"] for l in open(f"preds_{SPLIT}/{n}.jsonl")} for n in MODELS + JEVS}
def probs(n, i):
    r, pr = rows[i], P[n].get(i)
    if pr is None: return None
    keys = ["yes", "no"] if r["qtype"] == "noul" else r["options"]
    return {k: float(pr.get(k, 0.0)) for k in keys}
def correct(n, i):
    pr = probs(n, i)
    if pr is None: return 0.0
    r = rows[i]; g = ("yes" if r["gold"] == 1 else "no") if r["qtype"] == "noul" else r["gold"]
    b = max(pr.values()); return float([k for k, v in pr.items() if v == b] == [g])
def acc(n, i): return float(np.mean([correct(j, i) for j in JEVS])) if n == "JEV" else correct(n, i)
def brier(n, i):
    if n == "JEV": return float(np.mean([brier(j, i) for j in JEVS]))
    pr = probs(n, i); return 1.0 if pr is None else (pr["yes"] - rows[i]["gold"]) ** 2
task = lambda i: rows[i]["source"]
groups = defaultdict(list)
for i in base: groups[(task(i), rows[i]["group_id"])].append(i)
by_task = defaultdict(list)
for k in groups: by_task[k[0]].append(k)
def boot(n, ids_filter, val=acc, B=10000):
    keys = [k for k in groups if any(ids_filter(i) for i in groups[k])]
    sm = np.array([sum(val(n, i) for i in groups[k] if ids_filter(i)) for k in keys])
    sj = np.array([sum(val("JEV", i) for i in groups[k] if ids_filter(i)) for k in keys])
    cnt = np.array([sum(1 for i in groups[k] if ids_filter(i)) for k in keys], float)
    kidx = {k: j for j, k in enumerate(keys)}
    per = [np.array([kidx[k] for k in by_task[t] if k in kidx]) for t in sorted(by_task)]
    per = [a for a in per if len(a)]
    rng = np.random.default_rng(0)
    obs = (sm.sum() - sj.sum()) / cnt.sum()
    res = np.empty(B)
    for b in range(B):
        ix = np.concatenate([a[rng.integers(0, len(a), len(a))] for a in per])
        res[b] = (sm[ix].sum() - sj[ix].sum()) / cnt[ix].sum()
    p = min(1.0, 2 * min((res <= 0).mean(), (res >= 0).mean()))
    return obs, np.percentile(res, [2.5, 97.5]), p
isyn = lambda i: rows[i]["qtype"] == "noul"; isch = lambda i: rows[i]["qtype"] == "choice"; isall = lambda i: True
N = len(base); nyn = sum(map(isyn, base)); nch = N - nyn
print(f"{SPLIT}: base {N} rows = yes/no {nyn} ({100*nyn/N:.1f}%) + choice {nch} ({100*nch/N:.1f}%), groups {len(groups)}, tasks {len(by_task)}")
def m(n, f): ids = [i for i in base if f(i)]; return 100 * np.mean([acc(n, i) for i in ids])
for n in JEVS + ["JEV"] + MODELS:
    yb = np.mean([brier(n, i) for i in base if isyn(i)])
    print(f"  {n:24s} micro {m(n,isall):6.2f} | yes/no {m(n,isyn):6.2f} | choice {m(n,isch):6.2f} | yes/no Brier {yb:.4f}")
print("  per-run Jev yes/no:", [round(100*np.mean([correct(j,i) for i in base if isyn(i)]),2) for j in JEVS], "choice:", [round(100*np.mean([correct(j,i) for i in base if isch(i)]),2) for j in JEVS])
for n in MODELS:
    print(f"  == {n} minus JEV (paired cluster bootstrap by group, stratified by task, 10k, seed 0)")
    for lab, f in (("micro", isall), ("yes/no", isyn), ("choice", isch)):
        o, ci, p = boot(n, f)
        print(f"     {lab:7s} {100*o:+.2f} pp [{100*ci[0]:+.2f}, {100*ci[1]:+.2f}] p={p:.4f}")
    o, ci, p = boot(n, isyn, val=brier)
    print(f"     brier   {o:+.4f} [{ci[0]:+.4f}, {ci[1]:+.4f}] (model minus Jev; positive = model worse) p={p:.4f}")
    # decomposition of Jev's lead: lead = sum over rows of (jev - model) / N
    gy = (m("JEV", isyn) - m(n, isyn)); gc = (m("JEV", isch) - m(n, isch)); tot = m("JEV", isall) - m(n, isall)
    cy, cc = gy * nyn / N, gc * nch / N
    print(f"     DECOMP Jev lead {tot:+.2f} pp = yes/no {cy:+.2f} (gap {gy:+.2f} x share {nyn/N:.3f}) + choice {cc:+.2f} (gap {gc:+.2f} x share {nch/N:.3f})")
    per = []
    for t in sorted(by_task):
        ids = [i for i in base if task(i) == t]
        g = 100 * (np.mean([acc("JEV", i) for i in ids]) - np.mean([acc(n, i) for i in ids]))
        per.append((g * len(ids) / N, t, rows[ids[0]]["qtype"], len(ids), g))
    per.sort()
    print("     per-task contribution to Jev lead (pp of micro), qtype, n, task gap:")
    for c, t, q, k, g in per[::-1]:
        print(f"        {t:32s} {q:6s} n={k:4d} gap {g:+6.2f} -> {c:+.2f}")
# consistency (PREREG_OHS3 definitions applied to OHS-1 relations)
if rels:
    def pyes(n, i):
        pr = probs(n, i); return None if pr is None else pr["yes"]
    def dec(n, i):
        p = pyes(n, i)
        if p is None or p == 0.5: return None
        return p > 0.5
    print("  consistency (decision-based; tie or missing = violation):")
    for n in JEVS + MODELS:
        comp = []; compneg = []; mabs = []; dn = []; pa = []
        for x in rels:
            a, b = x["a"], x["b"]
            if a not in rows or b not in rows: continue
            if x["type"] == "complement":
                da, db = dec(n, a), dec(n, b)
                v = 1.0 if (da is None or db is None or da == db) else 0.0
                comp.append(v)
                if b.endswith("_neg"): compneg.append(v)
                if pyes(n, a) is not None and pyes(n, b) is not None: mabs.append(abs(pyes(n, a) + pyes(n, b) - 1))
            elif b.endswith("_dneg"):
                da, db = dec(n, a), dec(n, b); dn.append(1.0 if (da is None or db is None or da != db) else 0.0)
            elif b.endswith("_para"):
                da, db = dec(n, a), dec(n, b); pa.append(1.0 if (da is None or db is None or da != db) else 0.0)
        print(f"     {n:24s} complement viol {100*np.mean(comp):5.2f}% (n={len(comp)}) | _neg only {100*np.mean(compneg):5.2f}% (n={len(compneg)}) | mean|pa+pb-1| {np.mean(mabs):.4f} | dneg flip {100*np.mean(dn):5.2f}% (n={len(dn)}) | para flip {100*np.mean(pa):5.2f}% (n={len(pa)})")
    # paired bootstrap of complement violation Jev(mean) minus model, over base group
    def compvec(n):
        out = {}
        for x in rels:
            if x["type"] != "complement" or x["a"] not in rows or x["b"] not in rows: continue
            da, db = dec(n, x["a"]), dec(n, x["b"])
            out[(x["a"], x["b"])] = 1.0 if (da is None or db is None or da == db) else 0.0
        return out
    J = [compvec(j) for j in JEVS]
    for n in MODELS:
        C = compvec(n)
        byg = defaultdict(lambda: [0.0, 0.0, 0])
        for k in C:
            g = (task(k[0]), rows[k[0]]["group_id"]); byg[g][0] += np.mean([Jj[k] for Jj in J]); byg[g][1] += C[k]; byg[g][2] += 1
        keys = list(byg); A = np.array([byg[k] for k in keys])
        kidx = {k: j for j, k in enumerate(keys)}
        per = [np.array([kidx[k] for k in keys if k[0] == t]) for t in sorted({k[0] for k in keys})]
        rng = np.random.default_rng(0); res = []
        for _ in range(10000):
            ix = np.concatenate([a[rng.integers(0, len(a), len(a))] for a in per]); s = A[ix]
            res.append((s[:, 0].sum() - s[:, 1].sum()) / s[:, 2].sum())
        lo, hi = np.percentile(res, [2.5, 97.5])
        print(f"     complement viol Jev(mean of runs) minus {n}: {100*(A[:,0].sum()-A[:,1].sum())/A[:,2].sum():+.2f} pp [{100*lo:+.2f}, {100*hi:+.2f}] (positive = model better)")
