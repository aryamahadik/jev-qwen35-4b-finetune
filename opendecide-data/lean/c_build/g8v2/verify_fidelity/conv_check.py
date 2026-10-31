"""Counts only: batched L-BFGS vs sklearn on F2 (yes/no, choice), partition 0, real labels: iterations, objective, grad."""
import json, sys, time
import numpy as np
from pathlib import Path
sys.dont_write_bytecode = True
V = Path(__file__).resolve().parent
sys.path.insert(0, "/Users/aryamahadik/Documents/jev/opendecide-data/lean/c_src/common")
import g8_aflite as G
from sklearn.linear_model import LogisticRegression
G.CACHE = V / "cache"; fam = "F2"; ad = G.ADAPTERS[fam]
rows, sha = G.load_pool(G.LEAN / f"c_src/{fam}/out/candidates_r1.jsonl"); assert sha.startswith("1420da3d")
store = G.EmbStore(fam, sha); views = G.pool_views(fam, rows); assert store.ensure(list(G.all_texts(views))) == 0
feats, cards = G.features(fam, rows, views, store); trs = G.partitions(cards, ad["seed0"])
def obj(X, y, sw, w, b):
    z = X @ w + b; S = sw.sum(); return float((sw * (np.logaddexp(0, z) - y * z)).sum() / S + 0.5 / S * (w @ w))
res = {}
for part in ("yes_no", "choice"):
    F = feats[part]; tr = trs[0][F["rows"]]
    if part == "choice":
        tr = tr[F["pair_row"]]; Y = F["lab"][:, None]
    else:
        Y = F["y"][:, None]
    sw = np.ones(Y.shape)
    if part == "yes_no" and ad["yn_bal"]:
        npos = Y[tr].sum(); sw = np.where(Y == 1, tr.sum() / (2.0 * npos), tr.sum() / (2.0 * (tr.sum() - npos)))
    t = time.time(); W, b, it = G.lr_batch(F["X"], tr, Y, sw, max_iter=ad["it_yn" if part == "yes_no" else "it_ch"]); tb = time.time() - t
    t = time.time(); m = LogisticRegression(C=1.0, max_iter=2000, class_weight="balanced" if (part == "yes_no" and ad["yn_bal"]) else None)
    m.fit(F["X"][tr], Y[tr, 0]); ts = time.time() - t
    X = F["X"][tr].astype(np.float64); y = Y[tr, 0].astype(np.float64); s = sw[tr, 0]
    te = ~tr; zb = F["X"][te] @ W[:, 0] + b[0]; zs = m.decision_function(F["X"][te])
    res[part] = dict(iters_batch=int(it[0]), iters_sklearn=int(m.n_iter_[0]), obj_batch=obj(X, y, s, W[:, 0], b[0]),
                     obj_sklearn=obj(X, y, s, m.coef_[0], m.intercept_[0]),
                     coef_maxabs_diff=float(np.abs(W[:, 0] - m.coef_[0]).max()), coef_maxabs=float(np.abs(m.coef_[0]).max()),
                     heldout_score_corr=float(np.corrcoef(zb, zs)[0, 1]), sec_batch=round(tb, 1), sec_sklearn=round(ts, 1))
    print(part, res[part], flush=True)
(V / "conv_check.json").write_text(json.dumps(res, indent=1))
print("DONE", flush=True)
