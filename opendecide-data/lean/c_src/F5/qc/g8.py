"""G8 AFLite-lite (independent F5 checker). C_DATA_SPEC 8 G8: frozen MiniLM-L6 (sentence-transformers/all-MiniLM-L6-v2,
Apache-2.0, local HF cache) embeddings, 64 partitions, linear models (logistic regression), tau 0.75; predictable
share < 10%. Row embedding = concat of 3 mean-pooled views: question sentence(s), card + non-question wording, state
(long views cut into 120-word chunks). Partitions: 64 random 50/50 splits. PRIMARY (gated): grouped by card_id (a
card's rows sit on one side), because per-card yes rates are drawn 20-80% by design (spec 2.1; F5 G0 9 uses card-
grouped folds for G6 for the same reason). Instance-level (classic AFLite) and a within-card label-shuffle null of the
instance-level run are reported. Predictable = held-out reads right / reads >= tau, with >= 8 reads.
Usage: g8.py <name>  (embeddings cached in tmp/chk/g8/)"""
import json, os, random, sys, time
import numpy as np
import qc_lib as L

NAME = sys.argv[1] if len(sys.argv) > 1 else "candidates_r1"
CACHE = L.TMP / f"g8/emb_{NAME}.npy"
T0 = time.time()


def log(m):
    print(f"[{time.time() - T0:7.1f}s] {m}", flush=True)


def chunks(text, n=120):
    w = text.split()
    return [" ".join(w[i:i + n]) for i in range(0, max(1, len(w)), n)] or [""]


def embed(rows):
    os.environ.setdefault("HF_HUB_OFFLINE", "1")
    from sentence_transformers import SentenceTransformer
    import torch
    torch.set_num_threads(2)
    dev = "mps" if torch.backends.mps.is_available() else "cpu"
    m = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2", device=dev)
    log(f"model on {dev}")
    texts, own = [], []
    for i, r in enumerate(rows):
        q, rest = L.split_q(r["instructions"])
        for s, t in ((0, q), (1, ((r.get("card") or "") + "\n" + rest).strip()), (2, r["state"])):
            for c in chunks(t):
                texts.append(c); own.append((i, s))
    log(f"texts {len(texts)}")
    E = m.encode(texts, batch_size=128, show_progress_bar=False, convert_to_numpy=True, normalize_embeddings=True)
    acc = np.zeros((len(rows), 3, E.shape[1]), np.float32); cnt = np.zeros((len(rows), 3), np.float32)
    for (i, s), e in zip(own, E):
        acc[i, s] += e; cnt[i, s] += 1
    acc /= np.maximum(cnt, 1)[..., None]
    np.save(CACHE, acc.reshape(len(rows), -1).astype(np.float32)); log("cached")


def aflite(X, y, cards, mode, P=64, tau=0.75, min_reads=8):
    from sklearn.linear_model import LogisticRegression
    n = len(y); uc = sorted(set(cards)); right = np.zeros(n); reads = np.zeros(n)
    for p in range(P):
        rng = random.Random(5000 + p)
        if mode == "grouped":
            tc = set(rng.sample(uc, len(uc) // 2)); tr = np.array([c in tc for c in cards])
        else:
            tr = np.zeros(n, bool); tr[rng.sample(range(n), n // 2)] = True
        m = LogisticRegression(C=1.0, max_iter=2000).fit(X[tr], y[tr])
        pr = m.predict(X[~tr]); right[~tr] += (pr == y[~tr]); reads[~tr] += 1
    ok = reads >= min_reads; share = float(((right / np.maximum(reads, 1)) >= tau)[ok].mean())
    return {"mode": mode, "partitions": P, "tau": tau, "rows_scored": int(ok.sum()),
            "predictable_share": round(share, 4), "mean_heldout_acc": round(float((right / np.maximum(reads, 1))[ok].mean()), 4)}


def main():
    rows = L.load(NAME)
    if not CACHE.exists():
        embed(rows)
    X = np.load(CACHE); y = np.array([int(r["gold"]) for r in rows]); cards = [r["meta"]["card_id"] for r in rows]
    out = {"set": NAME, "rows": len(rows), "model": "sentence-transformers/all-MiniLM-L6-v2 (local cache)"}
    out["grouped"] = aflite(X, y, cards, "grouped"); log(out["grouped"])
    out["instance"] = aflite(X, y, cards, "instance"); log(out["instance"])
    rng = np.random.default_rng(0); yn = y.copy()
    for c in set(cards):
        ix = np.array([i for i, cc in enumerate(cards) if cc == c]); yn[ix] = rng.permutation(y[ix])
    out["instance_null_within_card_shuffle"] = aflite(X, yn, cards, "instance"); log(out["instance_null_within_card_shuffle"])
    out["bar"] = 0.10; out["gated"] = "grouped"
    out["pass"] = out["grouped"]["predictable_share"] < 0.10
    json.dump(out, open(L.QC / f"g8_{NAME}.json", "w"), indent=1); log(f"pass={out['pass']}")


if __name__ == "__main__":
    main()
