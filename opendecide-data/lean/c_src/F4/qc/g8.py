"""G8 AFLite-lite (independent F4 checker). C_DATA_SPEC 8 G8: frozen MiniLM-L6 (sentence-transformers/all-MiniLM-L6-v2,
Apache-2.0, local HF cache, offline) embeddings, 64 partitions, linear models, tau 0.75; predictable share < 10%.
Row views (model-visible text only): question sentence(s), card-without-question (the card on yes/no rows; the clause
text in `instructions` on choice rows, F4 7.6), record (`state`); long fields cut into 120-word chunks and mean-pooled;
on choice rows each option text + its definition line. Each block is reduced by PCA(96) fitted on the file.
Yes/no: logistic regression (class-balanced) on [q, card, state]. Choice: pointwise logistic regression over (row,
option) pairs on [q, card, state, option, option*q, option*state], argmax per row.
Partitions: 64 random 50/50 splits. PRIMARY grouped by card_id (per-card yes rates are drawn 20-80% by design, spec
2.1; F4 G0 8 asks for card-grouped folds); instance-level splits reported too. A row is predictable when its held-out
reads are right in >= tau of reads (>= 8 reads). Control: the same pipeline with labels permuted within card (yes/no)
or the gold slot redrawn uniformly (choice) gives the null share. Usage: g8.py <name> [--control]"""
import json, os, sys, time, hashlib
import numpy as np
import qc_lib as L

NAME = sys.argv[1] if len(sys.argv) > 1 and not sys.argv[1].startswith("--") else "candidates_r1"
CONTROL = "--control" in sys.argv
CACHE = L.TMP / f"g8_emb_{NAME}.npz"
P, TAU, MIN_READS, PCA_D = 64, 0.75, 8, 96
T0 = time.time()


def log(m):
    print(f"[{time.time() - T0:7.1f}s] {m}", flush=True)


def chunks(text, n=120):
    w = text.split()
    return [" ".join(w[i:i + n]) for i in range(0, max(1, len(w)), n)] or [""]


def embed_all(rows):
    os.environ.setdefault("HF_HUB_OFFLINE", "1"); os.environ.setdefault("TRANSFORMERS_OFFLINE", "1")
    from sentence_transformers import SentenceTransformer
    model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2", device="cpu")
    d = L.dio()
    texts = {}  # sha -> text

    def key(t):
        h = hashlib.sha1(t.encode()).hexdigest(); texts.setdefault(h, t); return h
    plan = []
    for r in rows:
        v = L.views(r); defs = d.card_defs(r.get("card"))
        card = v["cardnoq"] if r["qtype"] == "noul" else v["cardnoq"].replace(r.get("card") or "", "")
        item = {"q": [key(c) for c in chunks(v["q"])], "card": [key(c) for c in chunks(card)],
                "state": [key(c) for c in chunks(r["state"])]}
        if r["qtype"] != "noul":
            item["opts"] = [key(o + (": " + defs[o] if o in defs else "")) for o in r["options"]]
        plan.append(item)
    keys = list(texts)
    log(f"unique texts {len(keys)}")
    E = model.encode([texts[k] for k in keys], batch_size=128, show_progress_bar=False, normalize_embeddings=True,
                     convert_to_numpy=True)
    idx = {k: i for i, k in enumerate(keys)}
    pool = lambda ks: E[[idx[k] for k in ks]].mean(0)
    Q = np.stack([pool(p["q"]) for p in plan]); C = np.stack([pool(p["card"]) for p in plan])
    S = np.stack([pool(p["state"]) for p in plan])
    O = [np.stack([E[idx[k]] for k in p["opts"]]) if "opts" in p else None for p in plan]
    return Q, C, S, O


def pca(X, d=PCA_D):
    from sklearn.decomposition import PCA
    return PCA(n_components=min(d, X.shape[1]), random_state=0).fit_transform(X).astype(np.float32)


def aflite(Xrows, y, groups, fit_pred, seed, grouped):
    """Xrows: per-row features (yes/no) or per-row option blocks (choice); returns per-row (n_reads, n_right)."""
    rng = np.random.default_rng(seed); n = len(y)
    reads = np.zeros(n); right = np.zeros(n)
    ug = sorted(set(groups)); gidx = {g: i for i, g in enumerate(ug)}; gi = np.array([gidx[g] for g in groups])
    for p in range(P):
        if grouped:
            tg = rng.random(len(ug)) < 0.5; tr = tg[gi]
        else:
            tr = rng.random(n) < 0.5
        te = ~tr
        if tr.sum() < 10 or te.sum() < 10:
            continue
        ok = fit_pred(np.where(tr)[0], np.where(te)[0])
        reads[te] += 1; right[np.where(te)[0]] += ok
    return reads, right


def summarize(reads, right, mask=None):
    m = reads >= MIN_READS if mask is None else (reads >= MIN_READS) & mask
    frac = np.divide(right, reads, out=np.zeros_like(right), where=reads > 0)
    pred = (frac >= TAU) & m
    return {"rows": int(m.sum()), "n_predictable": int(pred.sum()),
            "predictable_share": round(float(pred.sum() / max(1, m.sum())), 4),
            "mean_reads": round(float(reads[m].mean()), 1) if m.any() else 0.0,
            "mean_heldout_acc": round(float((right[m] / reads[m]).mean()), 4) if m.any() else 0.0}, pred


def main():
    from sklearn.linear_model import LogisticRegression
    rows = L.load(NAME)
    if CACHE.exists():
        z = np.load(CACHE, allow_pickle=True); Q, C, S = z["Q"], z["C"], z["S"]; O = list(z["O"])
        log("embeddings from cache")
    else:
        Q, C, S, O = embed_all(rows)
        np.savez(CACHE, Q=Q, C=C, S=S, O=np.array(O, dtype=object)); log("embedded")
    Qp, Cp, Sp = pca(Q), pca(C), pca(S)
    allO = np.concatenate([o for o in O if o is not None])
    from sklearn.decomposition import PCA
    po = PCA(n_components=PCA_D, random_state=0).fit(allO)
    yi = [i for i, r in enumerate(rows) if r["qtype"] == "noul"]; ci = [i for i, r in enumerate(rows) if r["qtype"] != "noul"]
    rng = np.random.default_rng(7)
    # yes/no
    y = np.array([int(rows[i]["gold"]) for i in yi]); gy = [rows[i]["meta"]["card_id"] for i in yi]
    if CONTROL:
        by = {}
        for j, g in enumerate(gy):
            by.setdefault(g, []).append(j)
        y = y.copy()
        for g, js in by.items():
            y[js] = rng.permutation(y[js])
    Xy = np.hstack([Qp[yi], Cp[yi], Sp[yi]])

    def fp_y(tr, te):
        m = LogisticRegression(C=1.0, max_iter=500, class_weight="balanced").fit(Xy[tr], y[tr])
        return (m.predict(Xy[te]) == y[te]).astype(float)
    # choice pairs
    pr, px, pl = [], [], []
    gold = []
    for j, i in enumerate(ci):
        r = rows[i]; k = len(r["options"]); g = r["options"].index(r["gold"])
        if CONTROL:
            g = int(rng.integers(k))
        gold.append(g)
        op = po.transform(O[i]).astype(np.float32)
        base = np.hstack([Qp[i], Cp[i], Sp[i]])
        for t in range(k):
            px.append(np.hstack([base, op[t], op[t] * Qp[i], op[t] * Sp[i]])); pr.append(j); pl.append(int(t == g))
    px = np.array(px, dtype=np.float32); pr = np.array(pr); pl = np.array(pl)
    gc = [rows[i]["meta"]["card_id"] for i in ci]
    rows_of = {}
    for t, j in enumerate(pr):
        rows_of.setdefault(j, []).append(t)

    def fp_c(tr, te):
        trp = np.concatenate([rows_of[j] for j in tr]); m = LogisticRegression(C=1.0, max_iter=300).fit(px[trp], pl[trp])
        out = []
        for j in te:
            ts = rows_of[j]; s = m.decision_function(px[ts]); top = np.flatnonzero(s >= s.max() - 1e-9)
            out.append(float(rng.choice(top) == gold[j]))
        return np.array(out)
    res = {"gate": "G8", "file": f"out/{NAME}.jsonl", "control": CONTROL,
           "model": "sentence-transformers/all-MiniLM-L6-v2 (frozen, local cache)", "partitions": P, "split": "50/50",
           "tau": TAU, "min_reads": MIN_READS, "pca_dims_per_block": PCA_D, "rule": "predictable share < 10%"}
    for mode, grouped in (("grouped_by_card", True), ("instance_level", False)):
        ry, wy = aflite(Xy, y, gy, fp_y, 11, grouped); log(f"{mode} yes/no done")
        rc, wc = aflite(None, np.zeros(len(ci)), gc, fp_c, 13, grouped); log(f"{mode} choice done")
        sy, _ = summarize(ry, wy); sc_, _ = summarize(rc, wc)
        tot_pred = sy["n_predictable"] + sc_["n_predictable"]; tot_rows = sy["rows"] + sc_["rows"]
        res[mode] = {"predictable_share": round(tot_pred / max(1, tot_rows), 4), "n_predictable": tot_pred,
                     "rows": tot_rows, "yes_no": sy, "choice": sc_}
        log(f"{mode}: {res[mode]['predictable_share']}")
    res["pass"] = res["grouped_by_card"]["predictable_share"] < 0.10
    out = L.QC / f"g8_{NAME}{'_control' if CONTROL else ''}.json"
    json.dump(res, open(out, "w"), indent=1); log(f"DONE pass={res['pass']}")


if __name__ == "__main__":
    main()
