"""G8 AFLite-lite (independent F2 checker). C_DATA_SPEC 8: frozen MiniLM-L6 (sentence-transformers/all-MiniLM-L6-v2,
Apache-2.0, local HF cache) embeddings, 64 partitions, linear models, tau 0.75; predictable share < 10% per family.
Row embedding: question, card-without-question, state (long fields cut into 120-word chunks, mean-pooled); plus each
option text on choice rows. Yes/no: logistic regression (balanced) on [q, card, state]. Choice: pointwise LR over
(row, option) pairs [q, card, state, option, option*q], argmax per row (random tie-break).
Partitions: 64 random 50/50 splits, PRIMARY grouped by card (per-card yes rates are drawn 20-80% by design, spec 2.1);
instance-level reported too. Predictable = share of held-out reads right >= tau with >= 8 reads.
Usage: g8.py <name>  (embeddings cached in qc/tmp/g8_emb_<name>.npz)"""
import json, sys, time, random
import numpy as np
import qc_lib as L

NAME = sys.argv[1] if len(sys.argv) > 1 else "candidates_r1"
CACHE = L.QC / f"tmp/g8_emb_{NAME}.npz"
T0 = time.time()


def log(m):
    print(f"[{time.time() - T0:7.1f}s] {m}", flush=True)


def chunks(text, n=120):
    w = text.split()
    return [" ".join(w[i:i + n]) for i in range(0, max(1, len(w)), n)] or [""]


def embed(rows):
    from sentence_transformers import SentenceTransformer
    import torch
    dev = "mps" if torch.backends.mps.is_available() else "cpu"
    m = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2", device=dev)
    log(f"model on {dev}")
    texts, own = [], []
    for i, r in enumerate(rows):
        v = L.views(r)
        texts.append(v["q"]); own.append((i, 0))
        for c in chunks(v["cardnoq"]):
            texts.append(c); own.append((i, 1))
        for c in chunks(v["state"]):
            texts.append(c); own.append((i, 2))
        if not L.is_yn(r):
            for j, o in enumerate(r["options"]):
                texts.append(o); own.append((i, 3 + j))
    log(f"texts {len(texts)}")
    E = m.encode(texts, batch_size=128, show_progress_bar=False, convert_to_numpy=True, normalize_embeddings=True)
    n = len(rows); d = E.shape[1]
    acc = np.zeros((n, 3, d), np.float32); cnt = np.zeros((n, 3), np.float32)
    opt_idx, opt_vec = [], []
    for (i, s), e in zip(own, E):
        if s < 3:
            acc[i, s] += e; cnt[i, s] += 1
        else:
            opt_idx.append((i, s - 3)); opt_vec.append(e)
    acc /= np.maximum(cnt, 1)[..., None]
    np.savez_compressed(CACHE, rowemb=acc.astype(np.float16), opt_idx=np.array(opt_idx, np.int32),
                        opt_vec=np.array(opt_vec, np.float16))
    log("embeddings cached")


def aflite(rows, Z, OI, OV, grouped, P=64, tau=0.75, min_reads=8):
    from sklearn.linear_model import LogisticRegression
    n = len(rows); cards = [r["meta"]["card_id"] for r in rows]; uc = sorted(set(cards))
    yn = [i for i, r in enumerate(rows) if L.is_yn(r)]; ch = [i for i, r in enumerate(rows) if not L.is_yn(r)]
    Xy = Z[yn].reshape(len(yn), -1).astype(np.float32); yy = np.array([int(rows[i]["gold"]) for i in yn])
    ynpos = {i: k for k, i in enumerate(yn)}
    pos = set(ch); keep = np.array([int(i) in pos for i, j in OI]); oi = OI[keep]; ov = OV[keep].astype(np.float32)
    q = Z[oi[:, 0], 0].astype(np.float32)
    Xc = np.hstack([Z[oi[:, 0]].reshape(len(oi), -1).astype(np.float32), ov, ov * q])
    yc = np.array([int(rows[i]["options"][j] == rows[i]["gold"]) for i, j in oi])
    right = np.zeros(n); reads = np.zeros(n)
    for p in range(P):
        rng = random.Random(7000 + p)
        if grouped:
            tr_c = set(rng.sample(uc, len(uc) // 2)); tr = np.array([c in tr_c for c in cards])
        else:
            tr = np.zeros(n, bool); tr[rng.sample(range(n), n // 2)] = True
        a = tr[yn]
        if a.any() and (~a).any() and len(set(yy[a])) > 1:
            m = LogisticRegression(C=1.0, max_iter=2000, class_weight="balanced").fit(Xy[a], yy[a])
            pred = m.predict(Xy[~a])
            for k, i in enumerate(np.array(yn)[~a]):
                right[i] += int(pred[k] == yy[ynpos[int(i)]]); reads[i] += 1
        b = tr[oi[:, 0]]
        if b.any() and (~b).any():
            m = LogisticRegression(C=1.0, max_iter=2000).fit(Xc[b], yc[b]); s = m.decision_function(Xc[~b])
            best = {}
            for (i, j), sc, g in zip(oi[~b], s, yc[~b]):
                best.setdefault(int(i), []).append((float(sc) + rng.random() * 1e-9, g))
            for i, lst in best.items():
                right[i] += max(lst)[1]; reads[i] += 1
        if p % 8 == 7:
            log(f"{'grouped' if grouped else 'instance'} partition {p + 1}/{P}")
    score = np.where(reads > 0, right / np.maximum(reads, 1), 0.0)
    pred_ = (score >= tau) & (reads >= min_reads)
    samp = {}
    for i, r in enumerate(rows):
        s = r["meta"]["sampler"] + (":yn" if L.is_yn(r) else ":ch"); samp.setdefault(s, [0, 0])
        samp[s][0] += int(pred_[i]); samp[s][1] += 1
    return {"predictable_share": float(pred_.mean()), "n_predictable": int(pred_.sum()),
            "yes_no_share": float(pred_[yn].mean()) if yn else None,
            "choice_share": float(pred_[ch].mean()) if ch else None,
            "rows_with_min_reads": int((reads >= min_reads).sum()), "mean_reads": float(reads.mean()),
            "by_sampler_qtype": {s: [a, b, round(a / b, 4)] for s, (a, b) in sorted(samp.items())}}


def main():
    rows = L.load(NAME)
    if not CACHE.exists():
        embed(rows)
    D = np.load(CACHE); Z = D["rowemb"].astype(np.float32); OI = D["opt_idx"]; OV = D["opt_vec"]
    out = {"gate": "G8", "file": f"out/{NAME}.jsonl", "model": "sentence-transformers/all-MiniLM-L6-v2 (frozen)",
           "partitions": 64, "split": "50/50", "tau": 0.75, "min_reads": 8, "rule": "predictable share < 10%"}
    out["grouped_by_card"] = aflite(rows, Z, OI, OV, True); log(f"grouped {out['grouped_by_card']}")
    out["instance_level"] = aflite(rows, Z, OI, OV, False); log(f"instance {out['instance_level']}")
    out["pass"] = out["grouped_by_card"]["predictable_share"] < 0.10
    out["pass_instance_level"] = out["instance_level"]["predictable_share"] < 0.10
    out["seconds"] = round(time.time() - T0, 1)
    (L.QC / f"g8_{NAME}.json").write_text(json.dumps(out, indent=1))
    log(f"done pass={out['pass']}")


if __name__ == "__main__":
    main()
