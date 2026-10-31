"""G8v3: AFLite-lite judged by an exact within-card permutation test (PREREG_FINAL A19, as fixed after the verifier's
review of G8v2 on 5 Oct; C_DATA_SPEC 8, G8 row). One shared tool for every family.

Unchanged spec-8 set-up (as each family's own qc/g8.py): frozen sentence-transformers/all-MiniLM-L6-v2 embeddings,
64 partitions split 50/50 by card, logistic regression, tau 0.75, >= 8 held-out reads, grouped by card. Family
adapters copy each family's row-text, label and card_id extraction (family code is never imported; nothing is written
inside c_src/F*/). Counts only: no row text is printed or written.

Rule G8v3 (every constant is in RULE below and is written into each report; fixed before any G8v3 run):
  statistics  per part (yes_no; choice): share = grouped predictable share; acc = pooled grouped held-out accuracy.
              Real data: each is the mean over 4 partition seeds (seed0 + 100000 s, s = 0..3).
  null        within-card label permutations only (choice: gold positions permuted among rows sharing card_id and k).
              Null draw j is scored on partition seed j % 4 (one seed per draw). A one-seed statistic is a
              mean-preserving spread of the 4-seed mean, so the test is conservative; it is 4x cheaper, so K is 4x
              larger. A global-permutation null is report-only (location check).
  test        M = max(rank of share, rank of acc) over {real} + nulls (rank = fraction of draws <= value);
              b = #{null draws with M >= M_real}; p = (1 + b) / (K + 1): an exact Monte Carlo permutation p-value.
  alpha       0.009 per part (family-wise 0.10 over the 11 F1-F6 parts, Bonferroni).
  K and band  K = 340 first. One-sided 95% Clopper-Pearson bounds on the true p from (b, K): PASS if lower > alpha;
              FAIL if upper <= alpha (and p <= alpha); otherwise the band: extend to K = 1000 and decide p <= alpha
              there ("decided inside band" is flagged).
  chance      no fixed chance level: accuracy is judged against its own permutation null, which is right for both
              class-balanced and unbalanced LR. The legacy "acc <= chance + 2 pp" (majority / mean 1/k) is reported.
  shuffled    target: >= 1 - alpha of within-card label shuffles PASS (shuffles are scored exactly like real data).
  moderate    the token cue at strength 0.20 (yes/no: 20% of gold-yes rows, ~10% of the part; choice: the gold option
              of 20% of rows). Reliably caught = FAIL in >= 4 of 5 plant seeds in every part checked. If not, A19 is
              void and G8 stays as written. The 5%-of-rows level (yes/no 0.10, choice 0.05) and non-token cues
              (word swap; distractors shortened; repeated state sentence) are reported too.
  blind spot  G8 does not see length / redundancy cues (a repeated state sentence): G6(d) metadata baselines gate them.

Usage:
  g8_aflite.py run   --family F2 --pool .../F2/out/candidates_r1.jsonl --out .../c_build/g8v2/F2.json [--jobs 4]
  g8_aflite.py embed --family F2 --pool ...                      (cache only)
  g8_aflite.py power --family F2 [--pool ...] [--jobs 6]          (-> c_build/g8v2/power_F2.json)
  g8_aflite.py power-merge --families F1,F2,... --out .../c_build/g8v2/POWER.json
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
P, TAU, MIN_READS, ACC_MARGIN = 64, 0.75, 8, 0.02
PARTS = ("yes_no", "choice")
T0 = time.time()
RULE = dict(version="G8v3", seeds=4, seed_step=100000, null="within-card permutations, draw j on partition seed j % 4",
            alpha=0.009, alpha_note="family-wise 0.10 / 11 parts (F1-F6), Bonferroni", k_stages=(340, 1000),
            cp_one_sided=0.95, stat="M = max(rank share, rank acc); p = (1 + #null M >= real M) / (K + 1)",
            k_global_report=60, n_shuffle=40, moderate=dict(cue="token", strength=0.20, min_fail=4, of=5),
            null_seed0=10000, shuffle_seed0=50000, global_seed0=90000)


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


# ---------------------------------------------------------------- planted cues (power check): view-level edits
TOKEN = "[ref]"  # short neutral token appended to the end of the row text
THE_RX = re.compile(r"\bthe\b")
CUES = {  # part -> cue -> (strengths, what changes on the gold side). yes/no gold side = gold-yes rows.
    "yes_no": {"token": ((0.10, 0.20, 0.40), "token appended to the state (end of the row text)"),
               "swap": ((0.10, 0.20, 0.40), "first 'the' -> 'this' in the question (rows whose question has 'the')"),
               "repeat": ((0.40,), "last state sentence repeated: length/redundancy cue, no new words")},
    "choice": {"token": ((0.05, 0.10, 0.20, 0.40), "token appended to the gold option"),
               "shorter": ((0.10, 0.20, 0.40), "every distractor of >= 2 words loses its last word (gold longer)")}}
N_PLANT_SEEDS = 5


def cue_views(part, cue, segs, opts, gi=None, lab=None):
    """Planted views of one row, or None when the row cannot carry the cue (labels never change)."""
    if part == "yes_no":
        if cue == "token":
            return plant_views(segs, opts, TOKEN, "state")
        if cue == "swap":
            for c, t in enumerate(segs[0]):
                if THE_RX.search(t):
                    q = list(segs[0]); q[c] = THE_RX.sub("this", t, count=1)
                    return [q, segs[1], segs[2]], opts
            return None
        if cue == "repeat":
            st = " ".join(" ".join(segs[2]).split()); sents = [x for x in SENT_RX.split(st) if x.strip()]
            return ([segs[0], segs[1], chunks(st + " " + sents[-1])], opts) if sents else None
        raise ValueError(cue)
    if cue == "token":
        return plant_views(segs, opts, TOKEN, gi)
    if cue == "shorter":
        o2 = [(" ".join(o.split()[:-1]) if (not lab[j] and len(o.split()) >= 2) else o) for j, o in enumerate(opts)]
        return (segs, o2) if o2 != list(opts) else None
    raise ValueError(cue)


def plant_uniforms(n, part, cue, pseed):
    """One uniform per part row for (cue, plant seed); a row is marked at strength d when eligible and u < d, so the
    marked sets nest across strengths."""
    return np.random.default_rng([pseed, PARTS.index(part), sorted(CUES[part]).index(cue), 4242]).random(n)


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
    m = PCA(n_components=min(d, X.shape[1]), random_state=0)
    return m.fit_transform(X).astype(np.float32), m


def _lin(m, dv):
    """The linear part of a fitted PCA (or identity): transform(a) - transform(b) = lin(a - b)."""
    return dv if m is None else (dv @ m.components_.T).astype(np.float32)


def _group_ids(keys):
    return np.unique(keys, return_inverse=True)[1].ravel().astype(np.int64)


def features(fam, rows, views, store):
    """-> ({part: dict(rows=global row idx, cards, X (yes/no) or X/pair_row/pair_opt/k (choice), labels, group ids)},
    cards, fit). fit keeps the per-row blocks and PCA maps, so planted rows can be re-featured without a refit."""
    ad = ADAPTERS[fam]; n = len(rows)
    Z = np.zeros((n, 3, 384), np.float32)
    for i, (segs, _) in enumerate(views):
        for s, seg in enumerate(segs):
            Z[i, s] = np.mean([store.vec(t) for t in seg], axis=0)
    cards = np.array([str(r["meta"]["card_id"]) for r in rows])
    yn = np.array([i for i, r in enumerate(rows) if r["qtype"] == "noul"], np.int64)
    ch = np.array([i for i, r in enumerate(rows) if r["qtype"] != "noul"], np.int64)
    fit = {"Z": Z, "pca_row": [None] * 3, "pca_opt": None}
    if ad["pca"]:
        B = []
        for s in range(3):
            b_, m_ = _pca(Z[:, s], ad["pca"]); B.append(b_); fit["pca_row"][s] = m_
        R = np.hstack(B)
    else:
        B = [Z[:, s] for s in range(3)]
        R = Z.reshape(n, -1)
    fit["B"] = B
    out = {}
    if len(yn):
        out["yes_no"] = dict(rows=yn, cards=cards[yn], X=R[yn].astype(np.float32),
                             y=np.array([labels_of(ad, rows[i]) for i in yn], np.int64),
                             g_within=_group_ids(cards[yn]), g_global=np.zeros(len(yn), np.int64))
    if len(ch):
        OV = [np.stack([store.vec(o) for o in views[i][1]]) for i in ch]
        if ad["pca"]:
            from sklearn.decomposition import PCA
            po = PCA(n_components=ad["pca"], random_state=0).fit(np.concatenate(OV)); fit["pca_opt"] = po
            OV = [po.transform(o).astype(np.float32) for o in OV]
        X, pr, po_, ks, gi, lab = [], [], [], [], [], []
        for j, (i, ov) in enumerate(zip(ch, OV)):
            g, lb = labels_of(ad, rows[i]); k = len(ov); base = np.repeat(R[i][None], k, 0)
            blk = [base, ov, ov * B[0][i]] + ([ov * B[2][i]] if ad["ch_feats"] == "qs" else [])
            X.append(np.hstack(blk)); pr += [j] * k; po_ += list(range(k)); ks.append(k); gi.append(g); lab += lb
        ks = np.array(ks, np.int64); cc = cards[ch]
        out["choice"] = dict(rows=ch, cards=cc, X=np.concatenate(X).astype(np.float32),
                             pair_row=np.array(pr, np.int64), pair_opt=np.array(po_, np.int64),
                             k=ks, gi=np.array(gi, np.int64), lab=np.array(lab, np.int64),
                             g_within=_group_ids(np.char.add(np.char.add(cc, "|"), ks.astype(str))),
                             g_global=_group_ids(ks.astype(str)))
    return out, cards, fit


def _cue_rows(fam, views, F, part, cue):
    """Yield (part-local row a, global row i, base views, planted views) for every row that can carry `cue`."""
    starts = np.searchsorted(F["pair_row"], np.arange(len(F["rows"]))) if part == "choice" else None
    for a, i in enumerate(F["rows"].tolist()):
        segs, opts = views[i]
        if part == "yes_no":
            if F["y"][a] != 1:
                continue
            nv = cue_views(part, cue, segs, opts)
        else:
            st, k = int(starts[a]), int(F["k"][a])
            nv = cue_views(part, cue, segs, opts, gi=int(F["gi"][a]), lab=F["lab"][st:st + k].tolist())
        if nv is not None:
            yield a, i, (segs, opts), nv


def plant_store(fam, views, feats, fit, store, part, cue):
    """Feature shifts when every eligible row carries `cue`: dict(idx = unit indices into X (rows for yes/no, pairs
    for choice), D = float32 shifts, unit_row = part-local row of each unit, elig = part-local row mask). A planted
    data set (strength d, seed) shifts the units of its marked rows; PCA maps stay those fitted on the base file."""
    ad = ADAPTERS[fam]; F = feats[part]; n = len(F["rows"]); elig = np.zeros(n, bool); idx, D, ur = [], [], []
    store.ensure([t for _, _, _, nv in _cue_rows(fam, views, F, part, cue)
                  for t in ([x for seg in nv[0] for x in seg] + list(nv[1] or []))])
    dims = [b.shape[1] for b in fit["B"]]; drow = sum(dims)
    starts = np.searchsorted(F["pair_row"], np.arange(n)) if part == "choice" else None
    for a, i, (segs, opts), nv in _cue_rows(fam, views, F, part, cue):
        if part == "yes_no":
            parts_ = []
            for s in range(3):
                if nv[0][s] == segs[s]:
                    parts_.append(np.zeros(dims[s], np.float32)); continue
                dz = np.mean([store.vec(t) for t in nv[0][s]], axis=0) - fit["Z"][i, s]
                parts_.append(_lin(fit["pca_row"][s], dz[None])[0])
            d = np.concatenate(parts_)
            if np.any(d != 0):
                elig[a] = True; idx.append(a); D.append(d); ur.append(a)
            continue
        st = int(starts[a]); B0, B2 = fit["B"][0][i], fit["B"][2][i]
        for j, (o_new, o_old) in enumerate(zip(nv[1], opts)):
            if o_new == o_old:
                continue
            dv = _lin(fit["pca_opt"], (store.vec(o_new) - store.vec(o_old))[None])[0]
            if not np.any(dv != 0):
                continue
            blk = [np.zeros(drow, np.float32), dv, dv * B0] + ([dv * B2] if ad["ch_feats"] == "qs" else [])
            idx.append(st + j); D.append(np.concatenate(blk).astype(np.float32)); ur.append(a); elig[a] = True
    d_x = F["X"].shape[1]
    return {"idx": np.array(idx, np.int64), "D": (np.stack(D) if D else np.zeros((0, d_x))).astype(np.float32),
            "unit_row": np.array(ur, np.int64), "elig": elig}


def plant_marks(ps, part, cue, delta, pseed):
    """Part-local rows marked in the planted data set (cue, strength delta, plant seed)."""
    return ps["elig"] & (plant_uniforms(len(ps["elig"]), part, cue, pseed) < delta)


def partitions(cards, seed0):
    """64 seeded 50/50 splits of the family's cards (the scheme of the F1-F3, F5, F6 g8.py): train masks over rows."""
    uc = sorted(set(cards.tolist())); trs = []
    for p in range(P):
        trc = set(random.Random(seed0 + p).sample(uc, len(uc) // 2))
        trs.append(np.array([c in trc for c in cards.tolist()]))
    return trs


# ---------------------------------------------------------------- AFLite-lite core
def lr_batch(X, tr, Y, SW=None, C=1.0, max_iter=2000, tol=1e-4, m=10, groups=None, rep=None):
    """L2 logistic regression fitted for L label columns at once on the rows `tr` of X (batched L-BFGS, Armijo).
    Same objective, scaling and stopping rule as sklearn 1.6 LogisticRegression(lbfgs): per column,
    sum_i sw_i logloss_i / S + ||w||^2 / (2 C S), S = sum_i sw_i, intercept unpenalized, stop at max|grad| <= tol.
    SW: None (all ones) or per-cell weights. groups (planted cues): list of (cols, idx, D, M) meaning columns `cols`
    see rows idx of X shifted by D where M (len(idx) x len(cols), 0/1) is set, so many data sets share one X.
    rep: per column None or (idx, V) = rows idx replaced by V (turned into groups). Returns W (d, L), b (L,), n_iter."""
    groups = list(groups or [])
    if rep is not None:
        groups += [(np.array([c]), r[0], (r[1] - X[r[0]]).astype(np.float32), np.ones((len(r[0]), 1), np.float32))
                   for c, r in enumerate(rep) if r is not None]
    pos = np.cumsum(tr) - 1; GR = []
    for cols, idx, D, M in groups:
        k = tr[idx]
        if k.any():
            GR.append((np.asarray(cols), pos[idx[k]], D[k].astype(np.float32), M[k].astype(np.float32)))
    X = X[tr]; Y = Y[tr].astype(np.float64); SW = None if SW is None else SW[tr].astype(np.float64)
    n, d = X.shape; L = Y.shape[1]
    S = SW.sum(0) if SW is not None else np.full(L, float(n)); lam = 1.0 / (C * S)
    W = np.zeros((d, L)); b = np.zeros(L); n_iter = np.zeros(L, np.int64); cpos = np.full(L, -1)

    def fg(W_, b_, cols):
        cpos[:] = -1; cpos[cols] = np.arange(len(cols))
        W32 = W_.astype(np.float32); Z = (X @ W32).astype(np.float64) + b_; GA = []
        for gc, ii, Dk, Mk in GR:
            c = cpos[gc]; s = c >= 0
            if s.any():
                cc, Ms = c[s], Mk[:, s]
                Z[np.ix_(ii, cc)] += (Ms * (Dk @ W32[:, cc])).astype(np.float64); GA.append((ii, cc, Dk, Ms))
        y = Y[:, cols]; e = np.exp(-np.abs(Z)); lse = np.maximum(Z, 0) + np.log1p(e)  # = logaddexp(0, Z)
        sig = np.where(Z >= 0, 1.0, e) / (1.0 + e)                                    # = 1 / (1 + exp(-Z))
        if SW is None:
            f = (lse - y * Z).sum(0) / S[cols] + 0.5 * lam[cols] * (W_ ** 2).sum(0); R = (sig - y) / S[cols]
        else:
            sw = SW[:, cols]
            f = (sw * (lse - y * Z)).sum(0) / S[cols] + 0.5 * lam[cols] * (W_ ** 2).sum(0); R = sw * (sig - y) / S[cols]
        gW = (X.T @ R.astype(np.float32)).astype(np.float64) + lam[cols] * W_
        for ii, cc, Dk, Ms in GA:
            gW[:, cc] += (Dk.T @ (R[np.ix_(ii, cc)].astype(np.float32) * Ms)).astype(np.float64)
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


def lin_scores(X, te, W, b, groups=None):
    """X_col[te] @ W + b for every column, with the planted shifts of `groups` (te: bool mask over X's rows)."""
    post = np.cumsum(te) - 1; W32 = W.astype(np.float32)
    Z = (X[te] @ W32).astype(np.float64) + b
    for cols, idx, D, M in groups or []:
        k = te[idx]
        if k.any():
            cols = np.asarray(cols)
            Z[np.ix_(post[idx[k]], cols)] += (M[k].astype(np.float32) * (D[k] @ W32[:, cols])).astype(np.float64)
    return Z


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
    Returns y (yes/no) or pair labels (choice). Vectorised: rows sorted by (group, uniform) = a uniform permutation
    inside every group."""
    rng = np.random.default_rng(seed); g = F.get("g_" + kind)
    if g is None:
        if part == "yes_no":
            keys = F["cards"] if kind == "within" else np.zeros(len(F["y"]), dtype="U1")
        else:
            keys = np.char.add(np.char.add(F["cards"], "|"), F["k"].astype(str)) if kind == "within" else F["k"].astype(str)
        g = _group_ids(keys)
    y = F["y"] if part == "yes_no" else F["gi"]
    base = np.lexsort((np.arange(len(g)), g)); shuf = np.lexsort((rng.random(len(g)), g))
    out = y.copy(); out[base] = y[shuf]
    return out if part == "yes_no" else (F["pair_opt"] == out[F["pair_row"]]).astype(np.int64)


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


# ---------------------------------------------------------------- G8v3 engine: label columns x partition seeds
# A column is (lab, lab_seed, plant): lab 'real' | 'within' | 'global'; plant None or (cue, strength, plant seed).
# A column is scored on one or more partition seeds s (partitions(cards, seed0 + seed_step * s)); its statistic is
# the mean over those seeds. Every (part, s, chunk of <= CHUNK columns, partition p) is one batched solve.
CHUNK = 256


def tool_sha():
    return hashlib.sha256(Path(__file__).read_bytes()).hexdigest()


def ckey(col):
    lab, ls, pl = col
    return f"{lab}:{ls}" + ("" if pl is None else f":{pl[0]}:{pl[1]}:{pl[2]}")


def _chunk_groups(part, cols):
    """Planted-cue groups (cols, idx, D, M) for the columns of one chunk."""
    out = []
    for cue, ps in (_G.get("pstores", {}).get(part) or {}).items():
        jj = [j for j, c in enumerate(cols) if c[2] is not None and c[2][0] == cue]
        if jj and len(ps["idx"]):
            M = np.stack([plant_marks(ps, part, cue, cols[j][2][1], cols[j][2][2])[ps["unit_row"]] for j in jj], 1)
            out.append((np.array(jj), ps["idx"], ps["D"], M.astype(np.float32)))
    return out


def _job_cols(task):
    part, s, ci, p = task
    F, ad = _G["feats"][part], ADAPTERS[_G["fam"]]; cols = _G["chunks"][(part, s, ci)]; lk = ("Y", part, s, ci)
    if lk not in _G:
        old = _G.pop("_last", None)
        if old is not None:
            _G.pop(old, None); _G.pop(("grp",) + old, None)
        _G[lk] = np.stack([(F["y"] if part == "yes_no" else F["lab"]) if c[0] == "real" else
                           permute_labels(part, F, c[0], c[1]) for c in cols], 1)
        _G[("grp",) + lk] = _chunk_groups(part, cols); _G["_last"] = lk
    Y, groups = _G[lk], _G[("grp",) + lk]; tk = ("trs", s)
    if tk not in _G:
        _G[tk] = partitions(_G["cards"], _G["seed0"] + RULE["seed_step"] * s)
    trr = _G[tk][p][F["rows"]]
    if part == "yes_no":
        tr, SW = trr, None
        if ad["yn_bal"]:  # sklearn class_weight="balanced" on the training labels, per column
            npos = (Y[tr] == 1).sum(0); nneg = tr.sum() - npos
            SW = np.where(Y == 1, tr.sum() / (2.0 * np.maximum(npos, 1)), tr.sum() / (2.0 * np.maximum(nneg, 1)))
        W, b, _ = lr_batch(F["X"], tr, Y, SW, max_iter=ad["it_yn"], groups=groups)
        Z = lin_scores(F["X"], ~tr, W, b, groups)
        return task, np.flatnonzero(~tr), ((Z > 0) == (Y[~tr] == 1)).astype(np.float32)
    tr = trr[F["pair_row"]]
    W, b, _ = lr_batch(F["X"], tr, Y, None, max_iter=ad["it_ch"], groups=groups)
    tp = np.flatnonzero(~tr); Z = lin_scores(F["X"], ~tr, W, b, groups)
    Z += np.random.default_rng([s, p, 17]).random(Z.shape) * 1e-9  # random tie-break
    rows = F["pair_row"][tp]; starts = np.flatnonzero(np.r_[True, rows[1:] != rows[:-1]])
    mx = np.maximum.reduceat(Z, starts, axis=0); seg = np.repeat(np.arange(len(starts)), np.diff(np.r_[starts, len(tp)]))
    hit = (Z >= mx[seg]) * Y[tp]
    return task, rows[starts], np.add.reduceat(hit, starts, axis=0).clip(0, 1).astype(np.float32)


def _save_cache(path, new):
    """Merge `new` into the JSON cache at `path` (atomic; other processes may write the same file)."""
    path.parent.mkdir(parents=True, exist_ok=True); cur = {}
    if path.exists():
        try:
            cur = json.loads(path.read_text())
        except ValueError:
            cur = {}
    cur.update(new); tmp = path.with_name(f"{path.stem}.{os.getpid()}.tmp")
    tmp.write_text(json.dumps(cur)); os.replace(tmp, path)


def summarize6(reads, right):
    """summarize() at 6 decimals (fewer artificial ties in the permutation ranks)."""
    sc = np.divide(right, reads, out=np.zeros_like(right), where=reads > 0)
    pred = (sc >= TAU) & (reads >= MIN_READS)
    return {"share": round(float(pred.mean()), 6), "acc": round(float(right.sum() / max(1.0, reads.sum())), 6),
            "n_predictable": int(pred.sum()), "n": int(len(pred)), "rows_with_min_reads": int((reads >= MIN_READS).sum())}


def score(fam, feats, cards, want, jobs, pstores=None, cache_path=None):
    """want: {part: {col: seeds}} -> {(part, ckey, s): summary}. Evaluations already in the cache file are reused;
    each finished (part, s, chunk) is saved at once, so a killed run resumes where it stopped."""
    import multiprocessing as mp
    have = json.loads(cache_path.read_text()) if cache_path is not None and cache_path.exists() else {}
    res, chunks = {}, {}
    for part, cols in want.items():
        for s in range(RULE["seeds"]):
            need = []
            for col, seeds in cols.items():
                if s in seeds:
                    k = f"{part}|{s}|{ckey(col)}"
                    if k in have:
                        res[(part, ckey(col), s)] = have[k]
                    else:
                        need.append(col)
            nch = -(-len(need) // CHUNK); size = -(-len(need) // max(1, nch))  # even chunks of <= CHUNK
            for c0 in range(0, len(need), max(1, size)):
                chunks[(part, s, c0 // max(1, size))] = need[c0:c0 + size]
    if not chunks:
        return res
    _G.clear(); _G.update(fam=fam, feats=feats, cards=cards, chunks=chunks, pstores=pstores or {},
                          seed0=ADAPTERS[fam]["seed0"])
    tasks = sorted(((part, s, ci, p) for (part, s, ci) in chunks for p in range(P)),
                   key=lambda t: (t[0] != "choice", t[1], t[2], t[3]))
    log(f"{fam}: scoring {sum(len(c) for c in chunks.values())} column-seeds, {len(tasks)} batched solves")
    acc, t = {}, time.time()
    pool = mp.get_context("fork").Pool(jobs) if jobs > 1 else None
    it = pool.imap_unordered(_job_cols, tasks) if pool else map(_job_cols, tasks)
    for k, ((part, s, ci, p), te, R) in enumerate(it):
        key = (part, s, ci)
        if key not in acc:
            n = len(feats[part]["rows"]); acc[key] = [np.zeros(n), np.zeros((n, R.shape[1])), 0]
        a = acc[key]; a[0][te] += 1; a[1][te] += R; a[2] += 1
        if a[2] == P:
            new = {}
            for j, col in enumerate(chunks[key]):
                sm = summarize6(a[0], a[1][:, j]); res[(part, ckey(col), s)] = sm; new[f"{part}|{s}|{ckey(col)}"] = sm
            del acc[key]
            if cache_path is not None:
                _save_cache(cache_path, new)
        if (k + 1) % 64 == 0 or k + 1 == len(tasks):
            log(f"{fam}: {k + 1}/{len(tasks)} solves ({time.time() - t:.0f}s)")
    if pool:
        pool.close(); pool.join()
    return res


SEEDS_ALL = tuple(range(RULE["seeds"]))
REAL = ("real", 0, None)


def null_cols(K, k0=0, kind="within", plant=None):
    """Null draw j: label permutation seed (null_seed0 | global_seed0) + j, scored on partition seed j % 4."""
    base = RULE["null_seed0"] if kind == "within" else RULE["global_seed0"]
    return {(kind, base + j, plant): (j % RULE["seeds"],) for j in range(k0, K)}


def stat(res, part, col, seeds):
    v = [res[(part, ckey(col), s)] for s in seeds]
    return float(np.mean([x["share"] for x in v])), float(np.mean([x["acc"] for x in v]))


def null_stats(res, part, K, kind="within", plant=None):
    return np.array([stat(res, part, c, sd) for c, sd in null_cols(K, kind=kind, plant=plant).items()])


# ---------------------------------------------------------------- G8v3 test: exact Monte Carlo permutation p-value
def cp_bounds(b, K, conf):
    """One-sided Clopper-Pearson bounds (each at `conf`) on the true p from b exceedances in K draws."""
    from scipy.stats import beta
    lo = float(beta.ppf(1 - conf, b, K - b + 1)) if b > 0 else 0.0
    hi = float(beta.ppf(conf, b + 1, K - b)) if b < K else 1.0
    return lo, hi


def mc_test(real, nulls):
    """real (share, acc); nulls (K, 2). M = max(rank share, rank acc) over the K + 1 draws (rank = fraction <= value,
    ties counted, the same map for every draw, so real and nulls stay exchangeable). -> b, K, p = (1 + b) / (K + 1)."""
    A = np.vstack([np.asarray(real, float)[None], np.asarray(nulls, float).reshape(-1, 2)])
    rk = np.stack([np.searchsorted(np.sort(A[:, c]), A[:, c], side="right") for c in range(2)], 1) / len(A)
    M = rk.max(1); K = len(A) - 1; b = int((M[1:] >= M[0]).sum())
    return b, K, (1 + b) / (K + 1)


def decide(b, K, final, alpha=None):
    a = RULE["alpha"] if alpha is None else alpha
    lo, hi = cp_bounds(b, K, RULE["cp_one_sided"]); p = (1 + b) / (K + 1); band = not (lo > a or hi <= a)
    if lo > a and p > a:
        v = "PASS"
    elif hi <= a and p <= a:
        v = "FAIL"
    elif final:
        v = "FAIL" if p <= a else "PASS"
    else:
        v = "EXTEND"
    return {"verdict": v, "p": round(p, 6), "b": b, "K": K, "cp_lo": round(lo, 6), "cp_hi": round(hi, 6),
            "inside_band": bool(band), "decided_inside_band": bool(band and v != "EXTEND")}


def judge(real, NS, alpha=None):
    """Stage 1 on the first K1 null draws; when inside the band and K2 draws exist, stage 2 (final) on K2.
    verdict EXTEND = stage 2 draws are needed."""
    K1, K2 = RULE["k_stages"]
    d = decide(*mc_test(real, NS[:K1])[:2], final=False, alpha=alpha); d["stage"] = 1
    if d["verdict"] == "EXTEND" and len(NS) >= K2:
        d = decide(*mc_test(real, NS[:K2])[:2], final=True, alpha=alpha); d["stage"] = 2
    return d


def location(real, NS):
    """Null location / slack (issue: real cue-free data can sit below the null). crit = Gaussian marginal critical
    value at alpha / 2 per statistic; slack = crit - real (how much a cue could add before that marginal fails)."""
    from scipy.stats import norm
    mu, sd = NS.mean(0), NS.std(0, ddof=1); z = norm.ppf(1 - RULE["alpha"] / 2); crit = mu + z * sd
    r = np.asarray(real, float)
    return {"K": int(len(NS)), "share_mean": round(float(mu[0]), 5), "share_sd": round(float(sd[0]), 5),
            "acc_mean": round(float(mu[1]), 5), "acc_sd": round(float(sd[1]), 5),
            "z_real_share": round(float((r[0] - mu[0]) / sd[0]), 3), "z_real_acc": round(float((r[1] - mu[1]) / sd[1]), 3),
            "crit_share": round(float(crit[0]), 5), "crit_acc": round(float(crit[1]), 5),
            "slack_share": round(float(crit[0] - r[0]), 5), "slack_acc": round(float(crit[1] - r[1]), 5)}


def loo_size(NS, alpha=None):
    """Each null draw judged against the others with the final rule: the rule's size on null-like data."""
    f = 0
    for j in range(len(NS)):
        rest = np.delete(NS, j, axis=0); f += decide(*mc_test(NS[j], rest)[:2], final=True, alpha=alpha)["verdict"] == "FAIL"
    return {"n": int(len(NS)), "n_fail": int(f), "fail_rate": round(f / max(1, len(NS)), 5)}


def legacy_acc(part, F, acc, null_acc_mean):
    c = chance(part, F)
    return {"chance_majority_or_1_over_k": c, "pass_acc_chance_plus_2pp": bool(acc <= c + ACC_MARGIN),
            "null_mean_acc": round(float(null_acc_mean), 5),
            "pass_acc_null_mean_plus_2pp": bool(acc <= null_acc_mean + ACC_MARGIN)}


# ---------------------------------------------------------------- per-family G8v3 report
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


def _real_block(res, part):
    per = [res[(part, ckey(REAL), s)] for s in SEEDS_ALL]; sh = [x["share"] for x in per]
    r = stat(res, part, REAL, SEEDS_ALL)
    return r, {"share": round(r[0], 5), "acc": round(r[1], 5), "per_seed": [{k: x[k] for k in ("share", "acc",
               "n_predictable", "n")} for x in per]}, {"shares": sh, "sd": round(float(np.std(sh, ddof=1)), 5)}


def family_report(fam, pool, out_path, jobs, k_global=None):
    t0 = time.time(); ad = ADAPTERS[fam]; K1, K2 = RULE["k_stages"]
    k_global = RULE["k_global_report"] if k_global is None else k_global
    rows, sha, store, views, t_emb = embed_family(fam, pool)
    feats, cards, _ = features(fam, rows, views, store); t_feat = time.time()
    cpath = OUTDIR / f"runs_v3/{fam}_{sha[:16]}.json"
    want = {part: {REAL: SEEDS_ALL, **null_cols(K1), **null_cols(k_global, kind="global")} for part in feats}
    res = score(fam, feats, cards, want, jobs, cache_path=cpath)
    dec = {part: judge(stat(res, part, REAL, SEEDS_ALL), null_stats(res, part, K1)) for part in feats}
    ext = [part for part in feats if dec[part]["verdict"] == "EXTEND"]
    if ext:
        log(f"{fam}: inside the band at K = {K1} for {ext}: extending the null to K = {K2}")
        res.update(score(fam, feats, cards, {part: null_cols(K2, K1) for part in ext}, jobs, cache_path=cpath))
        for part in ext:
            dec[part] = judge(stat(res, part, REAL, SEEDS_ALL), null_stats(res, part, K2))
    t_af = time.time(); parts = {}
    for part, F in feats.items():
        real, rb, spread = _real_block(res, part); NS = null_stats(res, part, dec[part]["K"])
        d = {"n_rows": int(len(F["rows"])), "n_cards": int(len(set(F["cards"].tolist()))), "real": rb,
             "partition_seed_spread": spread, "test": dec[part], "pass": dec[part]["verdict"] == "PASS",
             "null_within_card": location(real, NS),
             "null_global_report_only": location(real, null_stats(res, part, k_global, kind="global")) if k_global else None,
             "legacy_acc_rules_report_only": legacy_acc(part, F, real[1], NS[:, 1].mean())}
        if part == "choice":
            d["rows_with_duplicate_gold_text"] = int((np.bincount(F["pair_row"], weights=F["lab"]) > 1).sum())
        parts[part] = d
    s0 = {p: res[(p, ckey(REAL), 0)] for p in feats}
    npred = sum(v["n_predictable"] for v in s0.values()); nall = sum(v["n"] for v in s0.values())
    old = {"raw_share_all_rows_seed0": round(npred / max(1, nall), 4), "verdict_lt_10pct": bool(npred / max(1, nall) < 0.10),
           "per_part_seed0": {p: v["share"] for p, v in s0.items()}}
    rep = {"gate": "G8v3 (PREREG_FINAL A19, fixed after the verifier's review)", "family": fam, "pool": _rel(pool),
           "pool_sha256": sha, "tool_sha256": tool_sha(), "n_rows": len(rows), "cache": _rel(store.files[0]),
           "runs_cache": _rel(cpath),
           "model": MODEL + " (frozen, local HF cache, offline, cpu)", "partitions": P, "split": "50/50 by card",
           "partition_seed0": ad["seed0"], "tau": TAU, "min_reads": MIN_READS, "rule": RULE, "adapter": ad,
           "solver": SOLVER_DESC["batch"], "solver_check": solver_check(fam, feats, cards),
           "parts": parts, "old_rule": old, "reproduction": reproduction(fam, pool, parts),
           "pass": bool(all(d["pass"] for d in parts.values())),
           "seconds": {"embed": t_emb, "features": round(t_feat - t0 - t_emb, 1), "aflite": round(t_af - t_feat, 1),
                       "total": round(time.time() - t0, 1)}, "jobs": jobs}
    Path(out_path).parent.mkdir(parents=True, exist_ok=True)
    Path(out_path).write_text(json.dumps(rep, indent=1))
    log(f"{fam}: pass={rep['pass']} " + " ".join(f"{p}: {d['test']['verdict']} p {d['test']['p']} (K {d['test']['K']})"
                                                  for p, d in parts.items()))
    return rep


# ---------------------------------------------------------------- power check (A19 "power check before use")
N_PNULL = 40  # null draws on planted data (token 0.20, plant seed 0), paired with base null draws 0..39


def _subjects(part):
    """Columns judged like real data (scored on all 4 seeds): real, within-card shuffles, planted data sets."""
    out = {REAL: SEEDS_ALL}
    out.update({("within", RULE["shuffle_seed0"] + i, None): SEEDS_ALL for i in range(RULE["n_shuffle"])})
    out.update({("real", 0, (cue, d, ps)): SEEDS_ALL for cue, (ds, _) in CUES[part].items() for d in ds
                for ps in range(N_PLANT_SEEDS)})
    return out


def power_family(fam, pool, jobs):
    """Shuffled labels + planted cues (CUES x N_PLANT_SEEDS), judged with the full G8v3 rule against the base
    within-card null; every planted data set is the base file with the marked rows' features shifted."""
    t0 = time.time(); K1, K2 = RULE["k_stages"]
    rows, sha, _, views, _ = embed_family(fam, pool)
    store = EmbStore(fam, sha, plant=True); feats, cards, fit = features(fam, rows, views, store)
    pstores = {part: {cue: plant_store(fam, views, feats, fit, store, part, cue) for cue in CUES[part]} for part in feats}
    store.close(); log(f"{fam}: planted stores ready ({time.time() - t0:.0f}s)")
    cpath = OUTDIR / f"runs_v3/{fam}_{sha[:16]}.json"
    want = {part: {**_subjects(part), **null_cols(K1), **null_cols(N_PNULL, plant=("token", 0.20, 0))} for part in feats}
    res = score(fam, feats, cards, want, jobs, pstores=pstores, cache_path=cpath)
    ext = [part for part in feats if any(judge(stat(res, part, c, sd), null_stats(res, part, K1))["verdict"] == "EXTEND"
                                         for c, sd in _subjects(part).items())]
    if ext:
        log(f"{fam}: inside the band at K = {K1} for {ext}: extending the null to K = {K2}")
        res.update(score(fam, feats, cards, {part: null_cols(K2, K1) for part in ext}, jobs, pstores=pstores,
                         cache_path=cpath))
    rep = {"family": fam, "pool": _rel(pool), "pool_sha256": sha, "tool_sha256": tool_sha(), "rule": RULE, "cues": {p: {c: {"strengths": v[0],
           "what": v[1]} for c, v in CUES[p].items()} for p in feats}, "plant_seeds": N_PLANT_SEEDS,
           "design": "planted data = base file with the cue on the gold side of the marked rows (P(cue | gold side) "
                     "= strength among rows that can carry it); judged against the base within-card null with the "
                     "full G8v3 rule (stage 2 when inside the band)", "parts": {}}
    for part, F in feats.items():
        NS = null_stats(res, part, K2 if part in ext else K1); n = len(F["rows"])
        J = lambda c, alpha=None: judge(stat(res, part, c, SEEDS_ALL), NS, alpha)  # noqa: E731
        real = stat(res, part, REAL, SEEDS_ALL)
        sh = [dict(zip(("share", "acc"), map(lambda x: round(x, 5), stat(res, part, c, SEEDS_ALL))), **J(c))
              for c in _subjects(part) if c[0] == "within"]
        nf = sum(x["verdict"] == "FAIL" for x in sh)
        from scipy.stats import binom
        pr = {"real": dict(J(REAL), share=round(real[0], 5), acc=round(real[1], 5)),
              "null_within_card": location(real, NS), "loo_size_of_rule_on_null_draws": loo_size(NS),
              "shuffled": {"n": len(sh), "n_fail": nf, "pass_rate": round(1 - nf / len(sh), 4),
                           "target": f">= 1 - alpha = {1 - RULE['alpha']}",
                           "consistent_with_target": bool(nf <= binom.ppf(0.95, len(sh), RULE["alpha"])),
                           "sd_4seed_shuffles_over_sd_1seed_nulls": [round(float(np.std([x[k] for x in sh], ddof=1)
                               / NS[:, i].std(ddof=1)), 3) for i, k in enumerate(("share", "acc"))],
                           "runs": sh}, "planted": {}}
        pn = null_stats(res, part, N_PNULL, plant=("token", 0.20, 0)); bn = NS[:N_PNULL]; dlt = pn - bn
        pr["planted_null_check"] = {"what": "null draws 0..39 re-scored on planted data (token 0.20, seed 0) minus "
                                    "the same draws on the base file", "mean_shift_share": round(float(dlt[:, 0].mean()), 5),
                                    "se_share": round(float(dlt[:, 0].std(ddof=1) / np.sqrt(len(dlt))), 5),
                                    "mean_shift_acc": round(float(dlt[:, 1].mean()), 5),
                                    "se_acc": round(float(dlt[:, 1].std(ddof=1) / np.sqrt(len(dlt))), 5)}
        for cue, (ds, _) in CUES[part].items():
            ps = pstores[part][cue]; out = {}
            for d in ds:
                runs = []
                for s in range(N_PLANT_SEEDS):
                    c = ("real", 0, (cue, d, s)); st_ = stat(res, part, c, SEEDS_ALL); j = J(c)
                    j.update(share=round(st_[0], 5), acc=round(st_[1], 5), n_marked=int(plant_marks(ps, part, cue, d, s).sum()),
                             verdict_alpha_0_05=J(c, 0.05)["verdict"], verdict_alpha_0_01=J(c, 0.01)["verdict"])
                    runs.append(j)
                out[str(d)] = {"detect_rate": round(sum(r["verdict"] == "FAIL" for r in runs) / len(runs), 4),
                               "detect_rate_alpha_0_05": round(sum(r["verdict_alpha_0_05"] == "FAIL" for r in runs) / len(runs), 4),
                               "detect_rate_alpha_0_01": round(sum(r["verdict_alpha_0_01"] == "FAIL" for r in runs) / len(runs), 4),
                               "mean_frac_part_rows_marked": round(float(np.mean([r["n_marked"] for r in runs])) / n, 4),
                               "mean_share_gain": round(float(np.mean([r["share"] for r in runs])) - real[0], 5),
                               "mean_acc_gain": round(float(np.mean([r["acc"] for r in runs])) - real[1], 5), "runs": runs}
            pr["planted"][cue] = {"n_rows_eligible": int(ps["elig"].sum()), "by_strength": out}
        rep["parts"][part] = pr
        log(f"{fam}/{part}: real {pr['real']['verdict']} shuffled fails {nf}/{len(sh)} detect " + "; ".join(
            f"{cue} " + str({d: v['detect_rate'] for d, v in pr['planted'][cue]['by_strength'].items()}) for cue in CUES[part]))
    rep["seconds"] = round(time.time() - t0, 1)
    (OUTDIR / f"power_{fam}.json").write_text(json.dumps(rep, indent=1))
    return rep


def power_merge(fams, out_path):
    """POWER.json: per-family results + the plain A19 statement (moderate = token at 0.20, >= 4 of 5 seeds FAIL)."""
    reps = {f: json.loads((OUTDIR / f"power_{f}.json").read_text()) for f in fams}
    mod = RULE["moderate"]; table, moderate, five, shuffled, slack, real, loo = {}, {}, {}, {}, {}, {}, {}
    for f, r in reps.items():
        for part, pr in r["parts"].items():
            k = f"{f}/{part}"
            table[k] = {cue: {d: v["detect_rate"] for d, v in c["by_strength"].items()} for cue, c in pr["planted"].items()}
            runs = pr["planted"][mod["cue"]]["by_strength"][str(mod["strength"])]["runs"]
            nfail = sum(x["verdict"] == "FAIL" for x in runs)
            moderate[k] = {"fails": nfail, "of": len(runs), "caught": bool(nfail >= mod["min_fail"])}
            d5 = "0.1" if part == "yes_no" else "0.05"  # ~5% of the part's rows
            v5 = pr["planted"]["token"]["by_strength"][d5]
            five[k] = {"strength": float(d5), "frac_rows": v5["mean_frac_part_rows_marked"], "detect_rate": v5["detect_rate"]}
            shuffled[k] = {x: pr["shuffled"][x] for x in ("n", "n_fail", "pass_rate", "consistent_with_target")}
            slack[k] = {x: pr["null_within_card"][x] for x in ("z_real_share", "z_real_acc", "slack_share", "slack_acc")}
            real[k] = {x: pr["real"][x] for x in ("verdict", "p", "K", "share", "acc")}
            loo[k] = pr["loo_size_of_rule_on_null_draws"]
    caught = all(v["caught"] for v in moderate.values()); shuf_ok = all(v["consistent_with_target"] for v in shuffled.values())
    status = "A19 HOLDS (G8v3 rule)" if (caught and shuf_ok) else "A19 VOID: G8 stays as written"
    miss = [k for k, v in moderate.items() if not v["caught"]]
    res = {"gate": "G8v3 power check (PREREG_FINAL A19)", "rule": RULE, "families": fams, "cues": CUES,
           "plant_seeds": N_PLANT_SEEDS, "a19_status": status, "moderate_definition": mod,
           "moderate_cue_caught": moderate, "five_pct_rows_token": five, "detect_rate_table": table,
           "shuffled": shuffled, "loo_size": loo, "null_location_and_slack": slack, "real_data_verdicts": real,
           "blind_spot": "G8 is not built to see length/redundancy cues (cue 'repeat'); G6(d) metadata baselines gate them",
           "pool_sha256": {f: r["pool_sha256"] for f, r in reps.items()},
           "tool_sha256": {f: r.get("tool_sha256") for f, r in reps.items()}, "per_family": reps}
    res["statement"] = (
        f"{status}. Moderate cue (token, strength {mod['strength']}) FAILs in >= {mod['min_fail']} of {mod['of']} seeds in "
        + ("every part" if caught else f"{len(moderate) - len(miss)} of {len(moderate)} parts; NOT reliably caught in "
           + ", ".join(miss)) + ". Shuffled labels: " + "; ".join(f"{k} {v['n_fail']}/{v['n']} fail" for k, v in shuffled.items())
        + (" (consistent with alpha)." if shuf_ok else " (above alpha in at least one part)."))
    Path(out_path).write_text(json.dumps(res, indent=1))
    return res


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("cmd", choices=["run", "embed", "power", "power-merge"])
    ap.add_argument("--family"); ap.add_argument("--families"); ap.add_argument("--pool"); ap.add_argument("--out")
    ap.add_argument("--jobs", type=int, default=4)
    ap.add_argument("--k-global", type=int, default=None, help="report-only global-permutation draws (run)")
    ap.add_argument("--spread", type=int, default=None, help="ignored (G8v2 option; G8v3 always uses 4 seeds)")
    ap.add_argument("--no-validate-null", action="store_true", help="ignored (G8v2 option)")
    a = ap.parse_args(argv)
    CACHE.mkdir(parents=True, exist_ok=True)
    pool = a.pool or (str(LEAN / f"c_src/{a.family}/out/candidates_r1.jsonl") if a.family else None)
    if a.cmd == "embed":
        embed_family(a.family, pool)
    elif a.cmd == "run":
        family_report(a.family, pool, a.out or OUTDIR / f"{a.family}.json", a.jobs, k_global=a.k_global)
    elif a.cmd == "power":
        power_family(a.family, pool, a.jobs)
    else:
        power_merge(a.families.split(","), a.out or OUTDIR / "POWER.json")


if __name__ == "__main__":
    main()
