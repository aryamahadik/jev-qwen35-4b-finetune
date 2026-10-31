"""T46 diagnosis (scratch): which d_meta choice features carry the gbt excess. Usage (from c2_build): g6_choice_diag.py SEEDBASE N"""
import sys, json, itertools
from pathlib import Path
sys.dont_write_bytecode = True
C2 = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(C2))
import numpy as np
import gen_full_c2 as G
from sklearn.feature_extraction import DictVectorizer
sb, n = int(sys.argv[1]), int(sys.argv[2])
with G.loader_patch("T46"):
    with G.PL.open_family("T46") as kit0:
        kit, xrep = G.apply_exclusions(kit0, set())
        b = G.pilot.build_pilot(kit, n, seed_base=sb, run_g15=False)
P = G.pilot
ch = [i for i in b.infos if i.row["qtype"] == "choice"]
T, D, Y, Rw = P._pair_rows(ch, "d_meta")
Y, Rw = np.array(Y), np.array(Rw)
groups = [i.row["meta"]["card_id"] for i in ch]
folds = P._folds([groups[r] for r in Rw])
chance = float(np.mean([1 / len(i.row["options"]) for i in ch]))
def acc(keys):
    Dk = [{k: d[k] for k in keys} for d in D]
    X = DictVectorizer(sparse=False).fit_transform(Dk)
    sc = np.zeros(len(Y))
    for tr, te in folds:
        sc[te] = P._gbt().fit(X[tr], Y[tr]).predict_proba(X[te])[:, 1]
    best = {}
    for s, r, y in zip(sc, Rw, Y): best.setdefault(r, []).append((s, y))
    a = []
    for r, l in best.items():
        m = max(s for s, _ in l); top = [y for s, y in l if s >= m - 1e-12]; a.append(sum(top) / len(top))
    return round(float(np.mean(a)), 4)
allk = list(D[0])
print("n choice", len(ch), "chance", round(chance, 4), "all", acc(allk))
optk = ["k", "tlen", "clen", "len_rank", "is_longest", "is_shortest", "abstain", "neg", "verbatim", "has_digit"]
rowk = [k for k in allk if k not in optk]
print("option-only", acc(optk), "row-only", acc(rowk) if rowk else None)
for k in rowk:
    print("drop", k, acc([x for x in allk if x != k]), "| only opt+", k, acc(optk + [k]))
for k in optk:
    print("drop-opt", k, acc([x for x in allk if x != k]))
print("META KEYS", sorted(ch[0].row["meta"].keys()))
print("C2 KEYS", sorted(ch[0].row["meta"]["c2"].keys()))
print("T46 META", json.dumps(ch[0].row["meta"]["t46"])[:600])
from collections import Counter, defaultdict
tab = defaultdict(Counter)
for i in ch:
    t = i.row["meta"]["t46"]
    _, num = P.meta_features(i)
    tab[(t["wf"], round(num["mag_max"]))][t["cls"]] += 1
for k in sorted(tab): print(k, dict(tab[k]))
tab2 = defaultdict(Counter)
for i in ch:
    t = i.row["meta"]["t46"]; tab2[t["typ"]][t["cls"]] += 1
print({k: dict(v) for k, v in tab2.items()})
tab3 = defaultdict(Counter)
for i in ch:
    t = i.row["meta"]["t46"]; tab3[t["wf"]][t["cls"]] += 1
print({k: dict(v) for k, v in tab3.items()})
