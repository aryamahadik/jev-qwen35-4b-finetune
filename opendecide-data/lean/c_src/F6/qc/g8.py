"""G8 AFLite-lite (independent F6 checker). Spec 8: frozen sentence-transformers/all-MiniLM-L6-v2 (Apache-2.0),
64 partitions, linear models, tau 0.75; predictable share < 10%. Embedding per row: question paragraph,
card-without-question and state, each cut into 120-word chunks (MiniLM reads <= 256 word pieces) and mean-pooled;
plus each option text on choice rows. Yes/no: logistic regression (balanced classes) on [q, card, state];
choice: (row, option) pair scorer on [q, card, state, option, option*q], argmax per row (random tie-break).
Partitions: 64 random 50/50 splits by card (meta.card_id; primary, the per-card yes rates of spec 2.1 cannot
transfer) and 64 instance-level splits (reported). A row is predictable if >= tau of its >= 8 held-out reads are
right. Usage: g8.py [candidates_r1]. Embeddings cached in tmp/qc/g8_emb_<name>.npz."""
import json, random, sys, time
import numpy as np
import qc_lib as q

NAME = sys.argv[1] if len(sys.argv) > 1 else "candidates_r1"
import hashlib
POOL_SHA = hashlib.sha256((q.OUT / f"{NAME}.jsonl").read_bytes()).hexdigest()
CACHE = q.TMP / f"g8_emb_{NAME}_{POOL_SHA[:16]}.npz"  # keyed by pool sha (recheck fix: a name-keyed cache went stale, F6-QC-19)
T0 = time.time()


def log(m):
    print(f"[{time.time() - T0:7.1f}s] {m}", flush=True)


def chunks(t, n=120):
    w = t.split(); return [" ".join(w[i:i + n]) for i in range(0, max(1, len(w)), n)] or [""]


def embed(rows):
    from sentence_transformers import SentenceTransformer
    import torch
    dev = "mps" if torch.backends.mps.is_available() else "cpu"
    m = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2", device=dev); log(f"model on {dev}")
    texts, own = [], []
    for i, r in enumerate(rows):
        v = q.views(r)
        texts.append(v["q"]); own.append((i, 0))
        for c in chunks(v["cardnoq"]):
            texts.append(c); own.append((i, 1))
        for c in chunks(v["state"]):
            texts.append(c); own.append((i, 2))
        if not q.is_yn(r):
            for j, o in enumerate(r["options"]):
                texts.append(o); own.append((i, 3 + j))
    log(f"texts {len(texts)}")
    E = m.encode(texts, batch_size=256, show_progress_bar=False, convert_to_numpy=True, normalize_embeddings=True)
    n, d = len(rows), E.shape[1]
    acc = np.zeros((n, 3, d), np.float32); cnt = np.zeros((n, 3), np.float32); oi, ov = [], []
    for (i, s), e in zip(own, E):
        if s < 3:
            acc[i, s] += e; cnt[i, s] += 1
        else:
            oi.append((i, s - 3)); ov.append(e)
    acc /= np.maximum(cnt, 1)[..., None]
    np.savez_compressed(CACHE, rowemb=acc.astype(np.float16), opt_idx=np.array(oi, np.int32), opt_vec=np.array(ov, np.float16))
    log("cached")


def aflite(rows, side, Z, OI, OV, grouped, P=64, tau=0.75, min_reads=8):
    from sklearn.linear_model import LogisticRegression
    n = len(rows); cards = [r["meta"]["card_id"] for r in rows]; uc = sorted(set(cards))
    yn = np.array([i for i, r in enumerate(rows) if q.is_yn(r)]); ch = [i for i, r in enumerate(rows) if not q.is_yn(r)]
    Xy = Z[yn].reshape(len(yn), -1); yy = np.array([int(rows[i]["gold"]) for i in yn])
    chs = set(ch); keep = np.array([int(i) in chs for i, j in OI]); oi = OI[keep]; ov = OV[keep]
    qv = Z[oi[:, 0], 0]
    Xc = np.hstack([Z[oi[:, 0]].reshape(len(oi), -1), ov, ov * qv])
    yc = np.array([int(rows[i]["options"][j] == rows[i]["gold"]) for i, j in oi])
    right = np.zeros(n); reads = np.zeros(n)
    for p in range(P):
        rng = random.Random(9100 + p)
        if grouped:
            trc = set(rng.sample(uc, len(uc) // 2)); tr = np.array([c in trc for c in cards])
        else:
            tr = np.zeros(n, bool); tr[rng.sample(range(n), n // 2)] = True
        a = tr[yn]
        m = LogisticRegression(C=1.0, max_iter=2000, class_weight="balanced").fit(Xy[a], yy[a])
        pred = m.predict(Xy[~a])
        for k, i in enumerate(yn[~a]):
            right[i] += int(pred[k] == yy[~a][k]); reads[i] += 1
        b = tr[oi[:, 0]]
        m = LogisticRegression(C=1.0, max_iter=2000).fit(Xc[b], yc[b]); s = m.decision_function(Xc[~b])
        best = {}
        for (i, j), sc, gl in zip(oi[~b], s, yc[~b]):
            best.setdefault(int(i), []).append((float(sc) + rng.random() * 1e-9, gl))
        for i, lst in best.items():
            right[i] += max(lst)[1]; reads[i] += 1
        if p % 16 == 15:
            log(f"{'grouped' if grouped else 'instance'} {p + 1}/{P}")
    score = np.where(reads > 0, right / np.maximum(reads, 1), 0.0)
    pr = (score >= tau) & (reads >= min_reads)
    by = {}
    for i, r in enumerate(rows):
        key = (side.get(r["id"]) or {}).get("form"); by.setdefault(key, [0, 0]); by[key][0] += int(pr[i]); by[key][1] += 1
    return {"predictable_share": round(float(pr.mean()), 4), "n_predictable": int(pr.sum()),
            "yes_no_share": round(float(pr[yn].mean()), 4), "choice_share": round(float(pr[ch].mean()), 4),
            "rows_with_min_reads": int((reads >= min_reads).sum()), "mean_reads": round(float(reads.mean()), 2),
            "by_form": {k: [a, b, round(a / b, 4)] for k, (a, b) in sorted(by.items())}}


def main():
    rows, side = q.load(NAME)
    if not CACHE.exists():
        embed(rows)
    D = np.load(CACHE); Z = D["rowemb"].astype(np.float32); OI = D["opt_idx"]; OV = D["opt_vec"].astype(np.float32)
    out = {"gate": "G8", "file": f"out/{NAME}.jsonl", "model": "sentence-transformers/all-MiniLM-L6-v2 (frozen)",
           "partitions": 64, "tau": 0.75, "rule": "predictable share < 10%", "pool_sha256": POOL_SHA}
    out["grouped_by_card"] = aflite(rows, side, Z, OI, OV, True); log(f"grouped {out['grouped_by_card']}")
    out["instance_level"] = aflite(rows, side, Z, OI, OV, False); log(f"instance {out['instance_level']}")
    out["pass"] = out["grouped_by_card"]["predictable_share"] < 0.10
    out["pass_instance_level"] = out["instance_level"]["predictable_share"] < 0.10
    (q.QC / f"g8_{NAME}.json").write_text(json.dumps(out, indent=1)); log(f"done pass={out['pass']}")


if __name__ == "__main__":
    main()
