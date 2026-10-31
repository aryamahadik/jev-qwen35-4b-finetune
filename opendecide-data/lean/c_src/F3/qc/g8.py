"""G8 AFLite-lite (independent F3 checker). Spec 8: frozen MiniLM-L6 (sentence-transformers/all-MiniLM-L6-v2,
Apache-2.0) embeddings, 64 partitions, linear models, tau 0.75; predictable share < 10% per family.
Embedding per row (MiniLM reads <= 256 word pieces, so long fields are cut into 120-word chunks and mean-pooled):
question paragraph, card-without-question, state; plus each option text on choice rows.
Linear models (logistic regression): yes/no rows predict gold from [q, card, state]; choice rows score (row, option)
pairs from [q, card, state, option, option*q] and take the argmax (ties broken at random).
Partitions: 64 random 50/50 splits; PRIMARY splits by card (meta.card_id; the drawn per-card yes rates of spec 2.1
cannot transfer to a held-out card); instance-level splits are reported too. A row's predictability = share of its
held-out predictions that are right; predictable if >= tau with >= 8 held-out reads.
Usage: g8.py <name> (embeddings cached in qc/tmp/g8_emb_<name>.npz)"""
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
    texts, own = [], []  # own: (row index, slot) ; slot 0 q, 1 card, 2 state, 3+ option j
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
    pos = {i: k for k, i in enumerate(ch)}
    pr = np.array([pos[i] for i, j in OI if i in pos]); keep = np.array([i in pos for i, j in OI])
    oi = OI[keep]; ov = OV[keep].astype(np.float32)
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
        # yes/no
        a = tr[yn]
        if a.any() and (~a).any() and len(set(yy[a])) > 1:
            # balanced class weights: the pool's yes rate (46%) is not the selected set's 50%, and a majority-label
            # lean would mark every majority-label row "predictable" without any cue
            m = LogisticRegression(C=1.0, max_iter=2000, class_weight="balanced").fit(Xy[a], yy[a]); pred = m.predict(Xy[~a])
            for k, i in enumerate(np.array(yn)[~a]):
                right[i] += int(pred[k] == yy[np.searchsorted(yn, i)]); reads[i] += 1
        # choice
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
    predictable = (score >= tau) & (reads >= min_reads)
    samp = {}; qts = {}
    side = L.load(NAME)[1]
    for i, r in enumerate(rows):
        s = r["meta"]["sampler"]; samp.setdefault(s, [0, 0]); samp[s][0] += int(predictable[i]); samp[s][1] += 1
        q = ("yn:" if L.is_yn(r) else "ch:") + str(side[r["id"]].get("qt")); qts.setdefault(q, [0, 0])
        qts[q][0] += int(predictable[i]); qts[q][1] += 1
    return {"predictable_share": float(predictable.mean()), "n_predictable": int(predictable.sum()),
            "yes_no_share": float(predictable[yn].mean()) if yn else None,
            "choice_share": float(predictable[ch].mean()) if ch else None,
            "rows_with_min_reads": int((reads >= min_reads).sum()), "mean_reads": float(reads.mean()),
            "by_sampler": {s: round(a / b, 4) for s, (a, b) in sorted(samp.items())},
            "by_qtype": {q: [a, b, round(a / b, 4)] for q, (a, b) in sorted(qts.items())}}


def main():
    rows, _ = L.load(NAME)
    if not CACHE.exists():
        embed(rows)
    D = np.load(CACHE); Z = D["rowemb"].astype(np.float32); OI = D["opt_idx"]; OV = D["opt_vec"]
    out = {"gate": "G8", "file": f"out/{NAME}.jsonl", "model": "sentence-transformers/all-MiniLM-L6-v2 (frozen)",
           "partitions": 64, "split": "50/50", "tau": 0.75, "min_reads": 8, "rule": "predictable share < 10%"}
    out["grouped_by_card"] = aflite(rows, Z, OI, OV, True)
    log(f"grouped {out['grouped_by_card']}")
    out["instance_level"] = aflite(rows, Z, OI, OV, False)
    log(f"instance {out['instance_level']}")
    # null control: same procedure with labels permuted (yes/no gold shuffled within each card; choice gold moved to a
    # seeded random option of the row); its predictable share is the floor that partition-to-partition model
    # stability gives without any real cue (report only; the gate rule stays the raw share < 10%)
    rng = random.Random(4242); perm = [dict(r) for r in rows]; byc = {}
    for i, r in enumerate(perm):
        if L.is_yn(r):
            byc.setdefault(r["meta"]["card_id"], []).append(i)
        else:
            r["gold"] = r["options"][rng.randrange(len(r["options"]))]
    for idx in byc.values():
        g = [perm[i]["gold"] for i in idx]; rng.shuffle(g)
        for i, v in zip(idx, g):
            perm[i]["gold"] = v
    out["control_permuted_labels_grouped"] = aflite(perm, Z, OI, OV, True)
    log(f"control {out['control_permuted_labels_grouped']}")
    out["pass"] = out["grouped_by_card"]["predictable_share"] < 0.10
    out["pass_instance_level"] = out["instance_level"]["predictable_share"] < 0.10
    out["seconds"] = round(time.time() - T0, 1)
    (L.QC / f"g8_{NAME}.json").write_text(json.dumps(out, indent=1))
    log(f"done pass={out['pass']}")


if __name__ == "__main__":
    main()
