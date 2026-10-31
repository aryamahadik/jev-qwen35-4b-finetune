"""w9: card-view (choice) ablation on a dump_qc.py dump. usage: python -B ablate.py DUMP.jsonl [--max N]"""
import json, sys, argparse
from pathlib import Path
from collections import defaultdict, Counter
import numpy as np
C2 = Path(__file__).resolve().parents[3]; sys.path.insert(0, str(C2)); sys.dont_write_bytecode = True
import pilot
from scipy import sparse
from sklearn.feature_extraction import DictVectorizer
from sklearn.feature_extraction.text import HashingVectorizer
from sklearn.preprocessing import MaxAbsScaler
from types import SimpleNamespace as NS

ap = argparse.ArgumentParser(); ap.add_argument("dump", nargs="+"); ap.add_argument("--only", default=None)
ap.add_argument("--coef", action="store_true"); a = ap.parse_args()
infos = []
for f in a.dump:
    for l in open(f):
        d = json.loads(l)
        if d["row"]["qtype"] != "choice": continue
        infos.append(NS(row=d["row"], question=d["question"], context=d["context"], kinds=d["kinds"]))
if a.only: infos = [i for i in infos if i.row["meta"]["qform"] == a.only]
print("choice rows", len(infos), Counter(i.row["meta"]["qform"] for i in infos))
toks = pilot.toks

def feats(info, flags):
    r = info.row; opts = r["options"]; k = len(opts); clen = [len(o) for o in opts]
    order = sorted(range(k), key=lambda j: -clen[j]); rank = {j: n for n, j in enumerate(order)}
    vt = set(toks(info.context)); out = []
    for j, o in enumerate(opts):
        ou = toks(o); kd = info.kinds[j]
        tk = ["o:" + t for t in ou] + ["o2:" + x + "_" + c for x, c in zip(ou, ou[1:])]
        dn = {"k": float(k), "tlen": float(len(ou)), "clen": float(clen[j]), "len_rank": rank[j] / max(1, k - 1),
              "is_longest": float("kind:longest" in kd), "is_shortest": float("kind:shortest" in kd),
              "abstain": float("kind:abstain" in kd), "neg": float("kind:neg" in kd), "verbatim": float("kind:verbatim_in_text" in kd),
              "has_digit": float(any(ch.isdigit() for ch in o))}
        ov = set(ou) & vt
        if "ov" in flags: dn.update({"ov": len(ov) / max(1, len(set(ou))), "ov_n": float(len(ov))})
        if "cross" in flags and k <= 4:
            tk += ["x:" + x + "|" + c for x in sorted(set(ou))[:6] for c in vt]
        if "ov" in flags: tk.append("ov:%d" % min(5, len(ov)))
        out.append((tk, dn, int(o == r["gold"])))
    return out

def run(flags, sub=None, coef=False):
    I = infos if sub is None else [i for i in infos if sub(i)]
    T, D, Y, Rw = [], [], [], []
    for ri, i in enumerate(I):
        for tk, dn, y in feats(i, flags): T.append(tk); D.append(dn); Y.append(y); Rw.append(ri)
    Y, Rw = np.array(Y), np.array(Rw)
    Xs = HashingVectorizer(n_features=2 ** 18, analyzer=lambda x: x, alternate_sign=False, norm="l2").transform(T)
    Xd = DictVectorizer(sparse=False).fit_transform(D)
    groups = np.array([I[ri].row["meta"]["card_id"] for ri in Rw]); folds = pilot._folds(list(groups))
    sc = np.zeros(len(Y))
    for tr, te in folds:
        sca = MaxAbsScaler().fit(Xd[tr])
        Xtr = sparse.hstack([Xs[tr], sparse.csr_matrix(sca.transform(Xd[tr]))]).tocsr()
        Xte = sparse.hstack([Xs[te], sparse.csr_matrix(sca.transform(Xd[te]))]).tocsr()
        sc[te] = pilot._lr().fit(Xtr, Y[tr]).predict_proba(Xte)[:, 1]
    best = defaultdict(list)
    for s, ri, yy in zip(sc, Rw, Y): best[ri].append((s, yy))
    acc = np.zeros(len(I)); ch = np.array([1.0 / len(i.row["options"]) for i in I])
    for ri, lst in best.items():
        m = max(s for s, _ in lst); top = [yy for s, yy in lst if s >= m - 1e-12]; acc[ri] = sum(top) / len(top)
    return acc, ch, I

def rep(name, flags, by=None):
    acc, ch, I = run(flags)
    print(f"{name:28s} all: acc {acc.mean():.4f} chance {ch.mean():.4f} excess {100*(acc.mean()-ch.mean()):+.2f} pp")
    for q in sorted({i.row['meta']['qform'] for i in I}):
        m = np.array([i.row['meta']['qform'] == q for i in I])
        print(f"    {q:18s} n {m.sum():5d} acc {acc[m].mean():.4f} chance {ch[m].mean():.4f} excess {100*(acc[m].mean()-ch[m].mean()):+.2f}")
    return acc, ch, I
rep("full", {"ov", "cross"}); rep("no cross", {"ov"}); rep("cross only", {"cross"}); rep("neither", set())

if a.coef:
    from sklearn.feature_extraction.text import CountVectorizer
    from sklearn.linear_model import LogisticRegression
    for q in sorted({i.row['meta']['qform'] for i in infos}):
        I = [i for i in infos if i.row['meta']['qform'] == q]
        T, Y = [], []
        for i in I:
            for tk, dn, y in feats(i, {"cross"}):
                T.append([t for t in tk if t.startswith("x:")]); Y.append(y)
        cv = CountVectorizer(analyzer=lambda x: x, binary=True, min_df=15); X = cv.fit_transform(T)
        m = LogisticRegression(C=1.0, max_iter=3000, solver="liblinear").fit(X, np.array(Y))
        names = np.array(cv.get_feature_names_out()); w = m.coef_[0]
        o = np.argsort(-np.abs(w))[:25]
        print("=====", q, "features", X.shape[1])
        for j in o: print(f"  {w[j]:+.3f} {names[j]}")
