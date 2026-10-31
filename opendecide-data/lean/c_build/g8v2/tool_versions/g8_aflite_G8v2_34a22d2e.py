"""G8v2: AFLite-lite judged against a label-permuted null (PREREG_FINAL Amendment A19; C_DATA_SPEC 8, G8 row).

One shared tool for every family. Features, partitions, models, tau and card grouping are the spec-8 set-up that
each family's own qc/g8.py used (frozen sentence-transformers/all-MiniLM-L6-v2, 64 partitions split 50/50 by card,
logistic regression, tau 0.75, >= 8 held-out reads). Family adapters below copy each family's row-text, label and
card_id extraction (family code is never imported, so nothing is written inside c_src/F*/).

Per family and per part (yes_no; choice):
  real    = grouped predictable share and pooled grouped held-out accuracy on the gold labels;
  null    = K = 20 seeded within-card label permutations + K = 20 global permutations, same 64 partitions;
  pass    = real share <= min(q95 within, q95 global) AND accuracy <= chance + 0.02
            (chance: yes/no = majority rate; choice = mean 1/k).
  The old raw share (all rows, grouped) and the old "< 10%" verdict stay in the report.
Choice "permutation": gold option positions are permuted among rows sharing (card_id, k) (within card) or k (global).
Embeddings are computed once on CPU and cached under c_build/g8v2/cache/ keyed by the pool's sha256.
Counts only: no row text is printed or written.

Usage:
  g8_aflite.py run   --family F2 --pool .../F2/out/candidates_r1.jsonl --out .../c_build/g8v2/F2.json [--jobs 4]
  g8_aflite.py embed --family F2 --pool ...                      (cache only)
  g8_aflite.py power --families F2,F6 --out .../c_build/g8v2/POWER.json [--jobs 6]
"""
import os
import sys

sys.dont_write_bytecode = True
for _v in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "MKL_NUM_THREADS", "VECLIB_MAXIMUM_THREADS"):
    os.environ.setdefault(_v, os.environ.get("G8_BLAS_THREADS", "1"))
os.environ.setdefault("HF_HUB_OFFLINE", "1")
os.environ.setdefault("TRANSFORMERS_OFFLINE", "1")
os.environ.setdefault("TOKENIZERS_PARALLELISM", "false")

import argparse, hashlib, json, random, re, time  # noqa: E402
from pathlib import Path  # noqa: E402
import numpy as np  # noqa: E402

LEAN = Path("/Users/aryamahadik/Documents/jev/opendecide-data/lean")
OUTDIR = LEAN / "c_build/g8v2"
CACHE = OUTDIR / "cache"
MODEL = "sentence-transformers/all-MiniLM-L6-v2"
P, TAU, MIN_READS, K_NULL, ACC_MARGIN = 64, 0.75, 8, 20, 0.02
PARTS = ("yes_no", "choice")
T0 = time.time()


def log(m):
    print(f"[{time.time() - T0:8.1f}s] {m}", flush=True)


# ---------------------------------------------------------------- text helpers (copied from the family qc_libs)
SENT_RX = re.compile(r"(?<=[.!?])\s+")


def split_q_para(ins):
    """F1, F3, F6: question = last paragraph of `instructions` holding '?'; rest = the other paragraphs."""
    paras = [p for p in ins.strip().split("\n\n") if p.strip()]
    qi = max((i for i, p in enumerate(paras) if "?" in p), default=len(paras) - 1)
    return paras[qi], "\n\n".join(paras[:qi] + paras[qi + 1:])


def split_q_sent(ins, nl_rest=True):
    """F2, F4 (nl_rest=True) and F5 (nl_rest=False): question = sentence(s) holding '?'; rest = the others."""
    qs, rest = [], []
    for line in ins.strip().split("\n"):
        for s in SENT_RX.split(line):
            (qs if "?" in s else rest).append(s)
        if nl_rest:
            rest.append("\n")
    return " ".join(qs).strip(), " ".join(rest).strip()


def chunks(text, n=120):
    w = text.split()
    return [" ".join(w[i:i + n]) for i in range(0, max(1, len(w)), n)] or [""]


def card_defs(card):
    """decoder_io.card_defs (F4 option definition lines)."""
    out = {}
    for line in (card or "").splitlines():
        if line.startswith("- ") and ": " in line:
            k, v = line[2:].split(": ", 1)
            out[k] = v
    return out


# ---------------------------------------------------------------- family adapters
# split: how the question is cut from `instructions`; sep: card + rest joiner; chunk_q: the question view is cut into
# 120-word chunks too; strip_card_choice: F4 drops the card text from the card view on choice rows (F4 7.6);
# opt_defs: F4 appends the card's definition line to each option; pca: per-block PCA dims fitted on the file (F4);
# ch_feats: "q" = [q, card, state, opt, opt*q] (F1-F3, F6), "qs" = [q, card, state, opt, opt*q, opt*state] (F4);
# yn_bal: class-balanced yes/no LR; it_yn / it_ch: LR max_iter; seed0: partition seed base of the family's g8.py;
# gold_eq: choice pair label by option-text equality (F1-F3, F6) or by options.index(gold) (F4).
_BASE = dict(split="para", sep="\n\n", chunk_q=False, strip_card_choice=False, opt_defs=False, pca=0, ch_feats="q",
             yn_bal=True, it_yn=2000, it_ch=2000, seed0=9100, gold_eq=True)
ADAPTERS = {
    "F1": dict(_BASE),
    "F2": dict(_BASE, split="sent", seed0=7000),
    "F3": dict(_BASE, seed0=7000),
    "F4": dict(_BASE, split="sent", chunk_q=True, strip_card_choice=True, opt_defs=True, pca=96, ch_feats="qs",
               it_yn=500, it_ch=300, seed0=1100, gold_eq=False),
    "F5": dict(_BASE, split="sent_nonl", sep="\n", chunk_q=True, yn_bal=False, seed0=5000),
    "F6": dict(_BASE),
}
FAMILY_G8 = {  # the family's own G8 output (read-only) used for the reproduction check
    f: LEAN / f"c_src/{f}/qc/g8_candidates_r1.json" for f in ADAPTERS}


def part_of(r):
    return "yes_no" if r["qtype"] == "noul" else "choice"


def row_views(ad, r):
    """-> ([q chunks, card chunks, state chunks], option texts or None), exactly as the family's g8.py embeds."""
    ins = r["instructions"]
    if ad["split"] == "para":
        q, rest = split_q_para(ins)
    else:
        q, rest = split_q_sent(ins, nl_rest=(ad["split"] == "sent"))
    card = ((r.get("card") or "") + ad["sep"] + rest).strip()
    if ad["strip_card_choice"] and r["qtype"] != "noul":
        card = card.replace(r.get("card") or "", "")
    segs = [chunks(q) if ad["chunk_q"] else [q], chunks(card), chunks(r["state"])]
    opts = None
    if r["qtype"] != "noul":
        if ad["opt_defs"]:
            d = card_defs(r.get("card"))
            opts = [o + (": " + d[o] if o in d else "") for o in r["options"]]
        else:
            opts = list(r["options"])
    return segs, opts


def labels_of(ad, r):
    """yes/no: int gold. choice: (gold index, per-option 0/1 labels as the family's g8.py set them)."""
    if r["qtype"] == "noul":
        return int(r["gold"])
    g = r["gold"]
    gi = g if isinstance(g, int) else r["options"].index(g)
    if ad["gold_eq"]:
        lab = [int(o == r["options"][gi]) for o in r["options"]]
    else:
        lab = [int(j == gi) for j in range(len(r["options"]))]
    return gi, lab


def plant_views(segs, opts, token, where):
    """Append `token` to the end of the row text: yes/no -> the state view (re-chunked); choice -> option j."""
    if where == "state":
        st = " ".join(" ".join(segs[2]).split() + [token])
        return [segs[0], segs[1], chunks(st)], opts
    opts = list(opts); opts[where] = opts[where] + " " + token
    return segs, opts


# ---------------------------------------------------------------- pool + embedding cache (keyed by pool sha256)
def load_pool(path):
    """Read the pool once; sha256 is taken over exactly the bytes parsed."""
    data = Path(path).read_bytes()
    rows = [json.loads(l) for l in data.decode("utf-8").splitlines() if l.strip()]
    return rows, hashlib.sha256(data).hexdigest()


def _key(t):
    return hashlib.sha1(t.encode("utf-8")).hexdigest().encode()


_MODEL = None


def _encode_worker(texts):
    global _MODEL
    if _MODEL is None:
        import torch
        from sentence_transformers import SentenceTransformer
        torch.set_num_threads(int(os.environ.get("G8_TORCH_THREADS", "4")))
        _MODEL = SentenceTransformer(MODEL, device="cpu")
    return _MODEL.encode(texts, batch_size=128, show_progress_bar=False, convert_to_numpy=True,
                         normalize_embeddings=True).astype(np.float32)


class EmbStore:
    """sha1(text) -> MiniLM vector. `base` file holds the pool's own texts; `plant` file holds planted-cue texts."""

    def __init__(self, fam, sha, plant=False):
        self.files = [CACHE / f"emb_{fam}_{sha[:16]}.npz"]
        if plant:
            self.files.append(CACHE / f"emb_{fam}_{sha[:16]}_plant.npz")
        self.write_to = self.files[-1]
        self.idx, mats, self.own = {}, [], []
        for f in self.files:
            if f.exists():
                d = np.load(f)
                for k in d["keys"]:
                    self.idx[bytes(k)] = len(self.idx)
                    if f == self.write_to:
                        self.own.append(bytes(k))
                mats.append(d["E"].astype(np.float32))
        self.E = np.concatenate(mats) if mats else np.zeros((0, 384), np.float32)
        self.model = None
        self.fam, self.sha = fam, sha

    def _reuse(self, keys):
        """Vectors for `keys` found in this family's caches of earlier pool versions (same text -> same vector)."""
        found = {}
        for f in sorted(CACHE.glob(f"emb_{self.fam}_*.npz")):
            if f in self.files or ".tmp" in f.name:
                continue
            d = np.load(f); fk = {bytes(k): i for i, k in enumerate(d["keys"])}
            hit = [k for k in keys if k in fk and k not in found]
            if hit:
                E = d["E"]
                for k in hit:
                    found[k] = E[fk[k]].astype(np.float32)
        return found

    def _encode(self, texts):
        """MiniLM runs in a spawned child, so this process never loads torch (a fork after torch crashes on macOS)."""
        if self.model is None:
            import multiprocessing as mp
            from concurrent.futures import ProcessPoolExecutor
            self.model = ProcessPoolExecutor(1, mp_context=mp.get_context("spawn"))
        return self.model.submit(_encode_worker, texts).result()

    def close(self):
        if self.model is not None:
            self.model.shutdown(); self.model = None

    def _save(self):
        rows = np.array([self.idx[k] for k in self.own], np.int64)
        tmp = self.write_to.with_name(f"{self.write_to.stem}.{os.getpid()}.tmp.npz")  # unique: runs share the cache
        np.savez(tmp, keys=np.array(self.own, dtype="S40"), E=self.E[rows].astype(np.float16))
        os.replace(tmp, self.write_to)

    def ensure(self, texts, block=8192):
        """Embed every text not yet cached (dedup); checkpoint after each block so a restart resumes."""
        miss, seen = [], set()
        for t in texts:
            k = _key(t)
            if k not in self.idx and k not in seen:
                seen.add(k); miss.append(t)
        if not miss:
            return 0
        old = self._reuse([_key(t) for t in miss])
        if old:
            ks = list(old); self.E = np.concatenate([self.E, np.stack([old[k] for k in ks])])
            for k in ks:
                self.idx[k] = len(self.idx); self.own.append(k)
            self._save(); miss = [t for t in miss if _key(t) not in old]
            log(f"reused {len(ks)} vectors from earlier pool versions' caches")
            if not miss:
                return 0
        log(f"embedding {len(miss)} new texts (cpu)")
        for s in range(0, len(miss), block):
            part = miss[s:s + block]; e = self._encode(part).astype(np.float16).astype(np.float32)  # = cached
            for t in part:
                k = _key(t); self.idx[k] = len(self.idx); self.own.append(k)
            self.E = np.concatenate([self.E, e]); self._save()
            log(f"  embedded {min(s + block, len(miss))}/{len(miss)}")
        self.close()
        return len(miss)

    def vec(self, t):
        return self.E[self.idx[_key(t)]]


def _rel(p):
    try:
        return str(Path(p).resolve().relative_to(LEAN))
    except ValueError:
        return str(p)


def pool_views(fam, rows):
    ad = ADAPTERS[fam]
    return [row_views(ad, r) for r in rows]


def all_texts(views):
    for segs, opts in views:
        for seg in segs:
            yield from seg
        if opts:
            yield from opts


def embed_family(fam, pool):
    t = time.time(); rows, sha = load_pool(pool)
    store = EmbStore(fam, sha); views = pool_views(fam, rows)
    n_new = store.ensure(list(all_texts(views)))
    log(f"{fam}: rows {len(rows)} sha {sha[:16]} unique texts {len(store.idx)} new {n_new}")
    return rows, sha, store, views, round(time.time() - t, 1)


# ---------------------------------------------------------------- features (spec-8 set-up of each family's g8.py)
def _pca(X, d):
    from sklearn.decomposition import PCA
    return PCA(n_components=min(d, X.shape[1]), random_state=0).fit_transform(X).astype(np.float32)


def features(fam, rows, views, store):
    """-> {part: dict(rows=global row idx, cards, X (yes/no) or X/pair_row/pair_opt/k (choice), labels)}."""
    ad = ADAPTERS[fam]; n = len(rows)
    Z = np.zeros((n, 3, 384), np.float32)
    for i, (segs, _) in enumerate(views):
        for s, seg in enumerate(segs):
            Z[i, s] = np.mean([store.vec(t) for t in seg], axis=0)
    cards = np.array([str(r["meta"]["card_id"]) for r in rows])
    yn = np.array([i for i, r in enumerate(rows) if r["qtype"] == "noul"], np.int64)
    ch = np.array([i for i, r in enumerate(rows) if r["qtype"] != "noul"], np.int64)
    if ad["pca"]:
        B = [_pca(Z[:, s], ad["pca"]) for s in range(3)]
        R = np.hstack(B)
    else:
        B = [Z[:, s] for s in range(3)]
        R = Z.reshape(n, -1)
    out = {}
    if len(yn):
        out["yes_no"] = dict(rows=yn, cards=cards[yn], X=R[yn].astype(np.float32),
                             y=np.array([labels_of(ad, rows[i]) for i in yn], np.int64))
    if len(ch):
        OV = [np.stack([store.vec(o) for o in views[i][1]]) for i in ch]
        if ad["pca"]:
            from sklearn.decomposition import PCA
            po = PCA(n_components=ad["pca"], random_state=0).fit(np.concatenate(OV))
            OV = [po.transform(o).astype(np.float32) for o in OV]
        X, pr, po_, ks, gi, lab = [], [], [], [], [], []
        for j, (i, ov) in enumerate(zip(ch, OV)):
            g, lb = labels_of(ad, rows[i]); k = len(ov); base = np.repeat(R[i][None], k, 0)
            blk = [base, ov, ov * B[0][i]] + ([ov * B[2][i]] if ad["ch_feats"] == "qs" else [])
            X.append(np.hstack(blk)); pr += [j] * k; po_ += list(range(k)); ks.append(k); gi.append(g); lab += lb
        out["choice"] = dict(rows=ch, cards=cards[ch], X=np.concatenate(X).astype(np.float32),
                             pair_row=np.array(pr, np.int64), pair_opt=np.array(po_, np.int64),
                             k=np.array(ks, np.int64), gi=np.array(gi, np.int64), lab=np.array(lab, np.int64))
    return out, cards


def partitions(cards, seed0):
    """64 seeded 50/50 splits of the family's cards (the scheme of the F1-F3, F5, F6 g8.py): train masks over rows."""
    uc = sorted(set(cards.tolist())); trs = []
    for p in range(P):
        trc = set(random.Random(seed0 + p).sample(uc, len(uc) // 2))
        trs.append(np.array([c in trc for c in cards.tolist()]))
    return trs


# ---------------------------------------------------------------- AFLite-lite core
def lr_batch(X, tr, Y, SW, C=1.0, max_iter=2000, tol=1e-4, m=10, rep=None):
    """L2 logistic regression fitted for L label columns at once on the rows `tr` of X (batched L-BFGS, Armijo).
    Same objective, scaling and stopping rule as sklearn 1.6 LogisticRegression(lbfgs): per column,
    sum_i sw_i logloss_i / S + ||w||^2 / (2 C S), S = sum_i sw_i, intercept unpenalized, stop at max|grad| <= tol.
    Only the train rows are used (one float32 copy). rep (power check): per column None or (idx, V), meaning
    that column's data set has rows idx of X replaced by V (planted-cue rows), so many data sets share one X.
    Returns W (d, L), b (L,), n_iter (L,)."""
    pos = np.cumsum(tr) - 1; RP = None
    X = X[tr]; Y = Y[tr].astype(np.float64); SW = SW[tr].astype(np.float64)
    if rep is not None:
        RP = []
        for r in rep:
            k = tr[r[0]] if r is not None else None
            if r is None or not k.any():
                RP.append(None); continue
            ii = pos[r[0][k]]; RP.append((ii, r[1][k].astype(np.float32), X[ii]))
    n, d = X.shape; L = Y.shape[1]
    S = SW.sum(0); lam = 1.0 / (C * S)
    W = np.zeros((d, L)); b = np.zeros(L); n_iter = np.zeros(L, np.int64)

    def fg(W_, b_, cols):
        W32 = W_.astype(np.float32); Z = (X @ W32).astype(np.float64) + b_
        if RP is not None:
            for c, col in enumerate(cols):
                if RP[col] is not None:
                    Z[RP[col][0], c] = (RP[col][1] @ W32[:, c]).astype(np.float64) + b_[c]
        sw, y = SW[:, cols], Y[:, cols]
        f = (sw * (np.logaddexp(0, Z) - y * Z)).sum(0) / S[cols] + 0.5 * lam[cols] * (W_ ** 2).sum(0)
        R = sw * (1.0 / (1.0 + np.exp(-Z)) - y) / S[cols]
        gW = (X.T @ R.astype(np.float32)).astype(np.float64) + lam[cols] * W_
        if RP is not None:
            for c, col in enumerate(cols):
                if RP[col] is not None:
                    ii, V, X0 = RP[col]; gW[:, c] += ((V - X0).T @ R[ii, c].astype(np.float32)).astype(np.float64)
        return f, np.vstack([gW, R.sum(0)[None]])
    act = np.arange(L); f, g = fg(W, b, act); hist = []
    for it in range(max_iter):
        done = np.abs(g).max(0) <= tol
        if done.all():
            break
        if done.any():  # freeze converged columns
            keep = ~done; act = act[keep]; f, g = f[keep], g[:, keep]
            hist = [(s_[:, keep], y_[:, keep], r_[keep]) for s_, y_, r_ in hist]
        q = g.copy(); al = []
        for s_, y_, r_ in reversed(hist):
            a = r_ * (s_ * q).sum(0); q -= a * y_; al.append(a)
        if hist:
            s_, y_, _ = hist[-1]; yy = (y_ * y_).sum(0); q *= np.where(yy > 0, (s_ * y_).sum(0) / np.where(yy > 0, yy, 1), 1)
        else:
            q /= np.maximum(1.0, np.abs(g).sum(0))
        for (s_, y_, r_), a in zip(hist, reversed(al)):
            q += s_ * (a - r_ * (y_ * q).sum(0))
        dr = -q; gd = (g * dr).sum(0); t = np.ones(len(act))
        Wa, ba = W[:, act], b[act]
        for _ in range(50):
            f2, g2 = fg(Wa + t * dr[:-1], ba + t * dr[-1], act)
            bad = f2 > f + 1e-4 * t * gd
            if not bad.any():
                break
            t = np.where(bad, t * 0.5, t)
        sv = t * dr; yv = g2 - g; sy = (sv * yv).sum(0)
        W[:, act] = Wa + sv[:-1]; b[act] = ba + sv[-1]; n_iter[act] += 1
        okp = sy > 1e-12
        hist.append((sv * okp, yv * okp, np.where(okp, 1.0 / np.where(okp, sy, 1.0), 0.0)))
        hist = hist[-m:]; f, g = f2, g2
    return W, b, n_iter


def run_yes_no(X, y, trs, bal, it):
    from sklearn.linear_model import LogisticRegression
    n = len(y); reads = np.zeros(n); right = np.zeros(n)
    for tr in trs:
        if tr.all() or not tr.any() or len(set(y[tr].tolist())) < 2:
            continue
        m = LogisticRegression(C=1.0, max_iter=it, class_weight="balanced" if bal else None).fit(X[tr], y[tr])
        te = ~tr; right[te] += (m.predict(X[te]) == y[te]); reads[te] += 1
    return reads, right


def run_choice(X, pair_row, lab, trs, it, seed):
    """Pointwise LR over (row, option) pairs; a read is right when the row's top-scored option is gold (random ties)."""
    from sklearn.linear_model import LogisticRegression
    n = int(pair_row.max()) + 1; reads = np.zeros(n); right = np.zeros(n); rng = np.random.default_rng(seed)
    for tr in trs:
        b = tr[pair_row]
        if b.all() or not b.any() or len(set(lab[b].tolist())) < 2:
            continue
        m = LogisticRegression(C=1.0, max_iter=it).fit(X[b], lab[b])
        s = m.decision_function(X[~b]) + rng.random(int((~b).sum())) * 1e-9
        prs, lb = pair_row[~b], lab[~b]
        order = np.lexsort((-s, prs)); ps = prs[order]
        top = order[np.flatnonzero(np.r_[True, ps[1:] != ps[:-1]])]
        right[prs[top]] += lb[top]; reads[prs[top]] += 1
    return reads, right


def summarize(reads, right):
    sc = np.divide(right, reads, out=np.zeros_like(right), where=reads > 0)
    pred = (sc >= TAU) & (reads >= MIN_READS)
    return {"share": round(float(pred.mean()), 4), "n_predictable": int(pred.sum()), "n": int(len(pred)),
            "acc": round(float(right.sum() / max(1.0, reads.sum())), 4),
            "rows_with_min_reads": int((reads >= MIN_READS).sum()), "mean_reads": round(float(reads.mean()), 2)}


def permute_labels(part, F, kind, seed):
    """kind 'within': permute inside card (choice: inside card x k); 'global': across the part (choice: inside k).
    Returns y (yes/no) or pair labels (choice)."""
    rng = np.random.default_rng(seed)
    if part == "yes_no":
        y = F["y"].copy()
        keys = F["cards"] if kind == "within" else np.zeros(len(y), dtype="U1")
    else:
        y = F["gi"].copy()
        keys = np.char.add(np.char.add(F["cards"], "|"), F["k"].astype(str)) if kind == "within" else F["k"].astype(str)
    for key in sorted(set(keys.tolist())):
        ix = np.flatnonzero(keys == key); y[ix] = rng.permutation(y[ix])
    if part == "yes_no":
        return y
    return (F["pair_opt"] == y[F["pair_row"]]).astype(np.int64)


def chance(part, F):
    if part == "yes_no":
        p = float(F["y"].mean()); return round(max(p, 1 - p), 4)
    return round(float(np.mean(1.0 / F["k"])), 4)


# ---------------------------------------------------------------- jobs (forked workers share the feature arrays)
_G = {}


def _job(spec):
    """spec = (ds, part, kind, seed, pseed): ds = feature set id; kind 'real' | 'within' | 'global';
    pseed = partition seed base."""
    ds, part, kind, seed, pseed = spec
    F, ad = _G["feats"][ds][part], ADAPTERS[_G["fam"]]
    tk = ("trs", pseed)
    if tk not in _G:
        _G[tk] = partitions(_G["cards"], pseed)
    trs = [tr[F["rows"]] for tr in _G[tk]]
    if part == "yes_no":
        y = F["y"] if kind == "real" else permute_labels(part, F, kind, seed)
        reads, right = run_yes_no(F["X"], y, trs, ad["yn_bal"], ad["it_yn"])
    else:
        lab = F["lab"] if kind == "real" else permute_labels(part, F, kind, seed)
        reads, right = run_choice(F["X"], F["pair_row"], lab, trs, ad["it_ch"], seed + 7 * pseed)
    return spec, reads, right


def run_specs_sklearn(fam, feats_by_ds, cards, specs, jobs):
    import multiprocessing as mp
    _G.clear(); _G.update(fam=fam, feats=feats_by_ds, cards=cards)
    specs = sorted(specs, key=lambda s: s[1] != "choice")  # heavy choice jobs first
    out, t = {}, time.time()
    if jobs <= 1:
        it = map(_job, specs)
    else:
        pool = mp.get_context("fork").Pool(jobs); it = pool.imap_unordered(_job, specs)
    for k, (spec, reads, right) in enumerate(it):
        out[spec] = (reads, right)
        if (k + 1) % 5 == 0 or k + 1 == len(specs):
            log(f"{fam}: {k + 1}/{len(specs)} AFLite runs ({time.time() - t:.0f}s)")
    if jobs > 1:
        pool.close(); pool.join()
    return out


def _labels(F, part, keys):
    """Label matrix (rows or pairs) x len(keys) for keys (kind, seed)."""
    cols = []
    for kind, seed in keys:
        if kind == "real":
            cols.append(F["y"] if part == "yes_no" else F["lab"])
        else:
            cols.append(permute_labels(part, F, kind, seed))
    return np.stack(cols, 1)


def _job_batch(task):
    """task = (ds, part, pseed, keys, p): fit every label column of `keys` on partition p in one batched solve."""
    ds, part, pseed, keys, p = task
    F, ad = _G["feats"][ds][part], ADAPTERS[_G["fam"]]
    lk = ("lab", ds, part, keys)
    if lk not in _G:
        _G[lk] = _labels(F, part, keys)
    Y = _G[lk]; tk = ("trs", pseed)
    if tk not in _G:
        _G[tk] = partitions(_G["cards"], pseed)
    trr = _G[tk][p][F["rows"]]
    if part == "yes_no":
        tr = trr; SW = np.ones(Y.shape, np.float64)
        if ad["yn_bal"]:  # sklearn class_weight="balanced" on the training labels, per column
            npos = (Y[tr] == 1).sum(0); nneg = tr.sum() - npos
            SW = np.where(Y == 1, tr.sum() / (2.0 * np.maximum(npos, 1)), tr.sum() / (2.0 * np.maximum(nneg, 1)))
        W, b, _ = lr_batch(F["X"], tr, Y, SW, max_iter=ad["it_yn"])
        te = np.flatnonzero(~tr); Z = (F["X"][te] @ W.astype(np.float32)) + b
        return task, te, ((Z > 0).astype(np.int64) == Y[te]).astype(np.float64)
    pr = F["pair_row"]; tr = trr[pr]
    W, b, _ = lr_batch(F["X"], tr, Y, np.ones(Y.shape, np.float64), max_iter=ad["it_ch"])
    tp = np.flatnonzero(~tr); Z = (F["X"][tp] @ W.astype(np.float32)).astype(np.float64) + b
    Z += np.random.default_rng([pseed, p, 17]).random(Z.shape) * 1e-9  # random tie-break
    rows = pr[tp]; starts = np.flatnonzero(np.r_[True, rows[1:] != rows[:-1]])
    mx = np.maximum.reduceat(Z, starts, axis=0); seg = np.repeat(np.arange(len(starts)), np.diff(np.r_[starts, len(tp)]))
    hit = (Z >= mx[seg]) * Y[tp]
    return task, rows[starts], np.add.reduceat(hit, starts, axis=0).clip(0, 1).astype(np.float64)


def run_specs_batch(fam, feats_by_ds, cards, specs, jobs):
    """Same results layout as run_specs; one task per (feature set, part, partition seed, partition)."""
    import multiprocessing as mp
    _G.clear(); _G.update(fam=fam, feats=feats_by_ds, cards=cards)
    groups = {}
    for ds, part, kind, seed, pseed in specs:
        groups.setdefault((ds, part, pseed), []).append((kind, seed))
    tasks = [(ds, part, pseed, tuple(keys), p) for (ds, part, pseed), keys in groups.items() for p in range(P)]
    tasks.sort(key=lambda t: (t[1] != "choice", -len(t[3])))
    acc = {}
    for (ds, part, pseed), keys in groups.items():
        n = len(feats_by_ds[ds][part]["rows"])
        for kind, seed in keys:
            acc[(ds, part, kind, seed, pseed)] = (np.zeros(n), np.zeros(n))
    t = time.time()
    pool = mp.get_context("fork").Pool(jobs) if jobs > 1 else None
    it = pool.imap_unordered(_job_batch, tasks) if pool else map(_job_batch, tasks)
    for k, ((ds, part, pseed, keys, p), te, R) in enumerate(it):
        for j, (kind, seed) in enumerate(keys):
            rd, rt = acc[(ds, part, kind, seed, pseed)]; rd[te] += 1; rt[te] += R[:, j]
        if (k + 1) % 64 == 0 or k + 1 == len(tasks):
            log(f"{fam}: {k + 1}/{len(tasks)} partition fits ({time.time() - t:.0f}s)")
    if pool:
        pool.close(); pool.join()
    return acc


SOLVER = os.environ.get("G8_SOLVER", "batch")
SOLVER_DESC = {"batch": "batched L-BFGS (lr_batch): sklearn 1.6 lbfgs objective and gtol 1e-4, all label sets of a "
                        "partition fitted in one pass", "sklearn": "sklearn LogisticRegression(lbfgs), one fit per run"}


def run_specs(fam, feats_by_ds, cards, specs, jobs):
    return (run_specs_batch if SOLVER == "batch" else run_specs_sklearn)(fam, feats_by_ds, cards, specs, jobs)


def solver_check(fam, feats, cards, n_part=3):
    """Agreement of the batched solver with sklearn LogisticRegression on real labels, first n_part partitions."""
    global P
    keep, P = P, n_part
    try:
        specs = [("base", part, "real", 0, ADAPTERS[fam]["seed0"]) for part in feats]
        a = run_specs_batch(fam, {"base": feats}, cards, specs, 1); b = run_specs_sklearn(fam, {"base": feats}, cards, specs, 1)
    finally:
        P = keep
    out = {}
    for k in a:
        (ra, wa), (rb, wb) = a[k], b[k]; m = ra > 0
        out[k[1]] = {"partitions": n_part, "reads": int(ra.sum()), "same_reads": bool((ra == rb).all()),
                     "read_agreement": round(float((wa[m] == wb[m]).mean()), 4),
                     "acc_batch": round(float(wa.sum() / ra.sum()), 4), "acc_sklearn": round(float(wb.sum() / rb.sum()), 4)}
    return out


def q95(xs):
    return round(float(np.percentile(xs, 95)), 4)


def verdict(part, F, real, nw, ng):
    """A19 pass rule for one part from summaries: real, nulls within (list), nulls global (list)."""
    c = chance(part, F); qw = q95([s["share"] for s in nw]); qg = q95([s["share"] for s in ng])
    thr = min(qw, qg)
    return {"chance": c, "q95_within": qw, "q95_global": qg, "threshold": thr,
            "pass_share": bool(real["share"] <= thr), "pass_acc": bool(real["acc"] <= c + ACC_MARGIN),
            "pass": bool(real["share"] <= thr and real["acc"] <= c + ACC_MARGIN)}


# ---------------------------------------------------------------- per-family G8v2 report
def null_block(sums):
    sh = [s["share"] for s in sums]
    return {"shares": sh, "accs": [s["acc"] for s in sums], "mean": round(float(np.mean(sh)), 4), "q95": q95(sh)}


def family_g8_shares(fam):
    """The family's own G8 grouped shares per part (read-only), or {} when absent."""
    p = FAMILY_G8[fam]
    if not p.exists():
        return {}
    d = json.loads(p.read_text()); g = d.get("grouped_by_card") or d.get("grouped") or {}
    if "yes_no" in g and isinstance(g["yes_no"], dict):  # F4 layout
        return {"yes_no": g["yes_no"]["predictable_share"], "choice": g["choice"]["predictable_share"],
                "all": g["predictable_share"], "file_mtime": p.stat().st_mtime}
    if "yes_no_share" in g:
        return {"yes_no": g["yes_no_share"], "choice": g["choice_share"], "all": g["predictable_share"],
                "file_mtime": p.stat().st_mtime}
    return {"yes_no": g.get("predictable_share"), "all": g.get("predictable_share"), "file_mtime": p.stat().st_mtime}


def reproduction(fam, pool, parts):
    fg = family_g8_shares(fam); out = {"family_g8_file": _rel(FAMILY_G8[fam]), "parts": {}}
    if not fg:
        out["note"] = "no family G8 output"; return out
    out["pool_newer_than_family_g8"] = bool(Path(pool).stat().st_mtime > fg["file_mtime"])
    for part, d in parts.items():
        if fg.get(part) is None:
            continue
        sh = d["partition_seed_spread"]["shares"]; sd = float(np.std(sh, ddof=1)) if len(sh) > 1 else 0.0
        # run-to-run spread: partition-seed reruns of the real labels, floored at 1 pp (= 2 x the 0.5-0.6 pp sd
        # seen with 4 seeds on F2 and F5), since 2 reruns alone can understate it
        tol = round(max(2 * sd, max(sh) - min(sh), 0.01), 4); delta = round(d["real"]["share"] - fg[part], 4)
        out["parts"][part] = {"family_share": round(fg[part], 4), "g8v2_share": d["real"]["share"], "delta": delta,
                              "tolerance_run_to_run": tol, "within_spread": bool(abs(delta) <= tol)}
    return out


def family_report(fam, pool, out_path, jobs, n_spread=3):
    t0 = time.time(); ad = ADAPTERS[fam]; seed0 = ad["seed0"]
    rows, sha, store, views, t_emb = embed_family(fam, pool)
    feats, cards = features(fam, rows, views, store); t_feat = time.time()
    specs = []
    for part in feats:
        specs += [("base", part, "real", 0, seed0 + 100000 * s) for s in range(n_spread + 1)]
        specs += [("base", part, "within", 1000 + k, seed0) for k in range(K_NULL)]
        specs += [("base", part, "global", 2000 + k, seed0) for k in range(K_NULL)]
    res = run_specs(fam, {"base": feats}, cards, specs, jobs); t_af = time.time()
    S = {k[1:]: summarize(*v) for k, v in res.items()}
    (OUTDIR / "logs").mkdir(parents=True, exist_ok=True)  # raw summaries first, so a report bug never loses a run
    (OUTDIR / f"logs/{fam}_{sha[:16]}_runs.json").write_text(json.dumps({"|".join(map(str, k)): v for k, v in S.items()}))
    parts = {}
    for part, F in feats.items():
        real = S[(part, "real", 0, seed0)]
        nw = [S[(part, "within", 1000 + k, seed0)] for k in range(K_NULL)]
        ng = [S[(part, "global", 2000 + k, seed0)] for k in range(K_NULL)]
        sp = [S[(part, "real", 0, seed0 + 100000 * s)]["share"] for s in range(n_spread + 1)]
        d = {"n_rows": int(len(F["rows"])), "n_cards": int(len(set(F["cards"].tolist()))), "real": real,
             "partition_seed_spread": {"shares": sp, "sd": round(float(np.std(sp, ddof=1)), 4)},
             "null_within_card": null_block(nw), "null_global": null_block(ng)}
        d.update(verdict(part, F, real, nw, ng))
        if part == "choice":
            d["rows_with_duplicate_gold_text"] = int(sum(1 for j in range(len(F["rows"]))
                                                         if F["lab"][F["pair_row"] == j].sum() > 1))
        parts[part] = d
    npred = sum(d["real"]["n_predictable"] for d in parts.values()); nall = sum(d["n_rows"] for d in parts.values())
    old = {"raw_share_all_rows": round(npred / max(1, nall), 4), "verdict_lt_10pct": bool(npred / max(1, nall) < 0.10),
           "per_part": {p: d["real"]["share"] for p, d in parts.items()}}
    rep = {"gate": "G8v2 (PREREG_FINAL A19)", "family": fam, "pool": _rel(pool),
           "pool_sha256": sha, "n_rows": len(rows), "cache": _rel(store.files[0]),
           "model": MODEL + " (frozen, local HF cache, offline, cpu)", "partitions": P, "split": "50/50 by card",
           "partition_seed0": seed0, "tau": TAU, "min_reads": MIN_READS, "K_within": K_NULL, "K_global": K_NULL,
           "q95_method": "numpy.percentile linear", "acc_margin": ACC_MARGIN, "adapter": ad,
           "rule": "pass = real share <= min(q95 within, q95 global) AND pooled acc <= chance + 0.02, per part",
           "solver": SOLVER_DESC[SOLVER], "solver_check": solver_check(fam, feats, cards) if SOLVER == "batch" else None,
           "parts": parts, "old_rule": old, "reproduction": reproduction(fam, pool, parts),
           "pass": bool(all(d["pass"] for d in parts.values())),
           "seconds": {"embed": t_emb, "features": round(t_feat - t0 - t_emb, 1), "aflite": round(t_af - t_feat, 1),
                       "total": round(time.time() - t0, 1)}, "jobs": jobs}
    Path(out_path).parent.mkdir(parents=True, exist_ok=True)
    Path(out_path).write_text(json.dumps(rep, indent=1))
    log(f"{fam}: pass={rep['pass']} " + " ".join(f"{p}: real {d['real']['share']} thr {d['threshold']} acc "
                                                  f"{d['real']['acc']} chance {d['chance']}" for p, d in parts.items()))
    return rep


# ---------------------------------------------------------------- power check (A19 "power check before use")
TOKEN = "[ref]"  # short neutral token appended to the end of the row text
STRENGTHS = (0.05, 0.10, 0.20, 0.40)
N_PLANT_SEEDS, N_SHUFFLE = 5, 20


def plant(fam, rows, views, part, delta, seed):
    """Cue on the gold side only: P(token | gold side) = delta, P(token | other) = 0.
    yes/no: gold side = rows with gold yes (token at the end of the state view); choice: the gold option text."""
    ad = ADAPTERS[fam]; rng = np.random.default_rng([seed, int(round(delta * 1000)), PARTS.index(part)])
    out, n = list(views), 0
    for i, r in enumerate(rows):
        if part_of(r) != part:
            continue
        u = rng.random()
        if part == "yes_no" and int(r["gold"]) == 1 and u < delta:
            out[i] = plant_views(*views[i], TOKEN, "state"); n += 1
        elif part == "choice" and u < delta:
            out[i] = plant_views(*views[i], TOKEN, labels_of(ad, r)[0]); n += 1
    return out, n


def base_thresholds(fam, sha, feats, cards, jobs):
    """Real-data null thresholds per part: taken from c_build/g8v2/<fam>.json when it was run on this pool sha."""
    p = OUTDIR / f"{fam}.json"
    if p.exists():
        d = json.loads(p.read_text())
        if d.get("pool_sha256") == sha:
            return {pt: {k: v[k] for k in ("q95_within", "q95_global", "threshold", "chance")}
                    for pt, v in d["parts"].items()}, "from " + _rel(p)
    seed0 = ADAPTERS[fam]["seed0"]; specs = []
    for part in feats:
        specs += [("base", part, "within", 1000 + k, seed0) for k in range(K_NULL)]
        specs += [("base", part, "global", 2000 + k, seed0) for k in range(K_NULL)]
    res = run_specs(fam, {"base": feats}, cards, specs, jobs); S = {k[1:]: summarize(*v) for k, v in res.items()}
    out = {}
    for part, F in feats.items():
        nw = [S[(part, "within", 1000 + k, seed0)] for k in range(K_NULL)]
        ng = [S[(part, "global", 2000 + k, seed0)] for k in range(K_NULL)]
        v = verdict(part, F, {"share": 0, "acc": 0}, nw, ng)
        out[part] = {k: v[k] for k in ("q95_within", "q95_global", "threshold", "chance")}
    return out, "computed here"


def judge(s, th):
    ps, pa = s["share"] <= th["threshold"], s["acc"] <= th["chance"] + ACC_MARGIN
    return {"share": s["share"], "acc": s["acc"], "pass_share": bool(ps), "pass_acc": bool(pa), "pass": bool(ps and pa)}


def _job_power(task):
    """task = (part, p): one batched solve of every power column of `part` on partition p (shared base X)."""
    part, p = task
    F, ad, cols = _G["feats"]["base"][part], ADAPTERS[_G["fam"]], _G["pcols"][part]
    lk = ("plab", part)
    if lk not in _G:
        _G[lk] = _labels(F, part, tuple(c[0] for c in cols))
    Y = _G[lk]; tk = ("trs", _G["seed0"])
    if tk not in _G:
        _G[tk] = partitions(_G["cards"], _G["seed0"])
    trr = _G[tk][p][F["rows"]]; rep = [c[1] for c in cols]
    tr = trr if part == "yes_no" else trr[F["pair_row"]]
    SW = np.ones(Y.shape, np.float64)
    if part == "yes_no" and ad["yn_bal"]:
        npos = (Y[tr] == 1).sum(0); nneg = tr.sum() - npos
        SW = np.where(Y == 1, tr.sum() / (2.0 * np.maximum(npos, 1)), tr.sum() / (2.0 * np.maximum(nneg, 1)))
    W, b, _ = lr_batch(F["X"], tr, Y, SW, max_iter=ad["it_yn" if part == "yes_no" else "it_ch"], rep=rep)
    te = np.flatnonzero(~tr); W32 = W.astype(np.float32)
    Z = (F["X"][te] @ W32).astype(np.float64) + b; post = np.cumsum(~tr) - 1
    for j, r in enumerate(rep):
        if r is not None:
            k = ~tr[r[0]]
            if k.any():
                Z[post[r[0][k]], j] = (r[1][k].astype(np.float32) @ W32[:, j]).astype(np.float64) + b[j]
    if part == "yes_no":
        return task, te, ((Z > 0).astype(np.int64) == Y[te]).astype(np.float64)
    Z += np.random.default_rng([_G["seed0"], p, 29]).random(Z.shape) * 1e-9
    rows = F["pair_row"][te]; starts = np.flatnonzero(np.r_[True, rows[1:] != rows[:-1]])
    mx = np.maximum.reduceat(Z, starts, axis=0); seg = np.repeat(np.arange(len(starts)), np.diff(np.r_[starts, len(te)]))
    hit = (Z >= mx[seg]) * Y[te]
    return task, rows[starts], np.add.reduceat(hit, starts, axis=0).clip(0, 1).astype(np.float64)


def power_family(fam, pool, jobs, validate_null=True):
    """Shuffled-label check + planted cues (STRENGTHS x N_PLANT_SEEDS) + null on planted rows, all as columns of
    one batched solve per (part, partition) on the base features; a planted data set differs from the base only in
    the rows (yes/no) or option pairs (choice) that carry the token, which enter as row replacements."""
    import multiprocessing as mp
    t0 = time.time(); seed0 = ADAPTERS[fam]["seed0"]
    assert not ADAPTERS[fam]["pca"], "row replacement needs features that do not refit on the file (no PCA)"
    rows, sha = load_pool(pool); store = EmbStore(fam, sha, plant=True); views = pool_views(fam, rows)
    store.ensure(list(all_texts(views)))
    feats, cards = features(fam, rows, views, store)
    th, src = base_thresholds(fam, sha, feats, cards, jobs)
    plans = {(part, d, s): plant(fam, rows, views, part, d, s) for part in feats for d in STRENGTHS
             for s in range(N_PLANT_SEEDS)}
    store.ensure([t for pv, _ in plans.values() for t in all_texts(pv)])
    reps, nm = {}, {}
    for key, (pv, n) in plans.items():
        Xp = features(fam, rows, pv, store)[0][key[0]]["X"]; Xb = feats[key[0]]["X"]
        idx = np.flatnonzero((Xp != Xb).any(1)); reps[key] = (idx, Xp[idx].copy()); nm[key] = n
    del plans
    log(f"{fam}: planted sets ready ({time.time() - t0:.0f}s)")
    pcols = {}
    for part in feats:
        c = [(("within", 3000 + s), None) for s in range(N_SHUFFLE)]
        c += [(("real", 0), reps[(part, d, s)]) for d in STRENGTHS for s in range(N_PLANT_SEEDS)]
        if validate_null:  # A19 null on the planted data itself (seed 0 of each strength), within card + global
            c += [((kind, base + k), reps[(part, d, 0)]) for d in STRENGTHS
                  for kind, base in (("within", 1000), ("global", 2000)) for k in range(K_NULL)]
        pcols[part] = c
    _G.clear(); _G.update(fam=fam, feats={"base": feats}, cards=cards, pcols=pcols, seed0=seed0)
    tasks = [(part, p) for part in feats for p in range(P)]; tasks.sort(key=lambda t: t[0] != "choice")
    acc = {part: [np.zeros((len(feats[part]["rows"]), len(pcols[part]))) for _ in range(2)] for part in feats}
    pool_ = mp.get_context("fork").Pool(jobs) if jobs > 1 else None
    it = pool_.imap_unordered(_job_power, tasks) if pool_ else map(_job_power, tasks)
    for k, ((part, p), te, R) in enumerate(it):
        acc[part][0][te] += 1; acc[part][1][te] += R
        if (k + 1) % 16 == 0 or k + 1 == len(tasks):
            log(f"{fam}: power {k + 1}/{len(tasks)} partition solves ({time.time() - t0:.0f}s)")
    if pool_:
        pool_.close(); pool_.join()
    rep = {"family": fam, "pool": _rel(pool), "pool_sha256": sha, "token": TOKEN, "solver": SOLVER_DESC["batch"],
           "design": "P(token | gold side) = delta, P(token | other) = 0; yes/no gold side = gold yes rows (token "
                     "appended to the state, the end of the row text); choice gold side = the gold option text",
           "thresholds": th, "thresholds_source": src, "shuffled": {}, "planted": {}}
    for part in feats:
        S = [summarize(acc[part][0][:, j], acc[part][1][:, j]) for j in range(len(pcols[part]))]
        js = [judge(S[j], th[part]) for j in range(N_SHUFFLE)]
        rep["shuffled"][part] = {"kind": "labels permuted within card (same law as the within-card null)",
                                 "runs": js, "pass_rate": round(sum(j["pass"] for j in js) / len(js), 4),
                                 "meets_95pct": bool(sum(j["pass"] for j in js) >= 0.95 * len(js))}
        j0 = N_SHUFFLE; jn = N_SHUFFLE + len(STRENGTHS) * N_PLANT_SEEDS
        for d in STRENGTHS:
            tp = None
            if validate_null:
                nw = S[jn:jn + K_NULL]; ng = S[jn + K_NULL:jn + 2 * K_NULL]; jn += 2 * K_NULL
                v = verdict(part, feats[part], {"share": 0, "acc": 0}, nw, ng)
                tp = {k: v[k] for k in ("q95_within", "q95_global", "threshold", "chance")}
                tp.update(null_within_mean=round(float(np.mean([x["share"] for x in nw])), 4),
                          null_global_mean=round(float(np.mean([x["share"] for x in ng])), 4))
            runs = []
            for s in range(N_PLANT_SEEDS):
                jj = judge(S[j0], tp or th[part]); jb = judge(S[j0], th[part])
                jj.update(n_marked=nm[(part, d, s)], pass_vs_base_thresholds=jb["pass"]); runs.append(jj); j0 += 1
            rep["planted"].setdefault(part, {})[str(d)] = {
                "thresholds_used": "null on this planted data (seed 0 of this strength)" if tp else "base data null",
                "planted_null": tp, "runs": runs,
                "detect_rate": round(sum(not j["pass"] for j in runs) / len(runs), 4),
                "detect_rate_vs_base_thresholds": round(sum(not j["pass_vs_base_thresholds"] for j in runs) / len(runs), 4)}
        log(f"{fam}/{part}: shuffled pass {rep['shuffled'][part]['pass_rate']} detect " +
            str({d: rep['planted'][part][str(d)]['detect_rate'] for d in STRENGTHS}))
    rep["seconds"] = round(time.time() - t0, 1)
    (OUTDIR / f"power_{fam}.json").write_text(json.dumps(rep, indent=1))
    return rep


def power_merge(fams, out_path):
    """POWER.json: per-family results + the plain statement of the smallest strength reliably caught (5/5 seeds)."""
    reps = {f: json.loads((OUTDIR / f"power_{f}.json").read_text()) for f in fams}
    table, smallest = {}, {}
    for f, r in reps.items():
        for part, by in r["planted"].items():
            row = {d: by[d]["detect_rate"] for d in sorted(by, key=float)}
            table[f"{f}/{part}"] = row
            ok = [float(d) for d in row if all(row[e] == 1.0 for e in row if float(e) >= float(d))]
            smallest[f"{f}/{part}"] = min(ok) if ok else None
    shuffled = {f"{f}/{p}": v["pass_rate"] for f, r in reps.items() for p, v in r["shuffled"].items()}
    vals = list(smallest.values())
    overall = None if (not vals or any(v is None for v in vals)) else max(vals)
    res = {"gate": "G8v2 power check (PREREG_FINAL A19)", "families": fams, "token": TOKEN, "strengths": STRENGTHS,
           "seeds_per_strength": N_PLANT_SEEDS, "shuffle_seeds": N_SHUFFLE,
           "detect_rate_table": table, "smallest_strength_caught_5_of_5": smallest,
           "smallest_strength_caught_everywhere": overall, "shuffled_pass_rate": shuffled,
           "shuffled_meets_95pct": {k: v >= 0.95 for k, v in shuffled.items()},
           "per_family": reps}
    res["fail_reasons"] = {f"{f}/{p}": {d: {"share_rule_fails": sum(not r["pass_share"] for r in b[d]["runs"]),
                                             "acc_rule_fails": sum(not r["pass_acc"] for r in b[d]["runs"]),
                                             "mean_share": round(float(np.mean([r["share"] for r in b[d]["runs"]])), 4),
                                             "mean_acc": round(float(np.mean([r["acc"] for r in b[d]["runs"]])), 4)}
                                         for d in b} for f, r in reps.items() for p, b in r["planted"].items()}
    res["base_thresholds"] = {f"{f}/{p}": v for f, r in reps.items() for p, v in r["thresholds"].items()}
    res["null_on_planted_data"] = {f"{f}/{p}": {d: b[d].get("planted_null") or b[d].get("null_on_planted_rows_within_card")
                                                for d in b if b[d].get("planted_null") or
                                                b[d].get("null_on_planted_rows_within_card")}
                                   for f, r in reps.items() for p, b in r["planted"].items()}
    res["statement"] = (
        "Smallest planted-cue strength caught in 5 of 5 seeds: "
        + "; ".join(f"{k} {v}" for k, v in smallest.items())
        + f". Caught everywhere from strength {overall}. "
        + "Shuffled labels pass rate: " + "; ".join(f"{k} {v}" for k, v in shuffled.items())
        + (" (meets >= 95% everywhere)." if all(v >= 0.95 for v in shuffled.values()) else
           " (below the 95% target in at least one part)."))
    Path(out_path).write_text(json.dumps(res, indent=1))
    return res


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("cmd", choices=["run", "embed", "power", "power-merge"])
    ap.add_argument("--family"); ap.add_argument("--families"); ap.add_argument("--pool"); ap.add_argument("--out")
    ap.add_argument("--jobs", type=int, default=4)
    ap.add_argument("--spread", type=int, default=3, help="extra partition-seed runs of the real labels (run-to-run)")
    ap.add_argument("--no-validate-null", action="store_true")
    a = ap.parse_args(argv)
    CACHE.mkdir(parents=True, exist_ok=True)
    pool = a.pool or (str(LEAN / f"c_src/{a.family}/out/candidates_r1.jsonl") if a.family else None)
    if a.cmd == "embed":
        embed_family(a.family, pool)
    elif a.cmd == "run":
        family_report(a.family, pool, a.out or OUTDIR / f"{a.family}.json", a.jobs, n_spread=a.spread)
    elif a.cmd == "power":
        power_family(a.family, pool, a.jobs, validate_null=not a.no_validate_null)
    else:
        power_merge(a.families.split(","), a.out or OUTDIR / "POWER.json")


if __name__ == "__main__":
    main()
