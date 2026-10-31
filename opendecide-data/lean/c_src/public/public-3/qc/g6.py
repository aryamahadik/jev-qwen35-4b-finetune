#!/usr/bin/env python3
"""G6 partial-input and metadata baselines on our framings, public-3 (independent checker, prep5/B4; counts only).

Spec 8 G6 for public rows: "G6 (on our framings)": the baselines see only what the builder wrote around the human
record (wording, card, guidance, option set, metadata), never the human record text itself (the state's record, or
options that are records). Sample: every public-3 row (rows_r1 + reserve + mtdev = 3,223; public rows have no
generator to draw a separate >= 5,000-row sample from, like F8/F12/F13's "fewer real rows").
5-fold GroupKFold by group_id (twin sets stay together). Models: logistic regression on TF-IDF word 1-2 grams (or
one-hot features), HistGradientBoosting on dense features (64-d SVD of the sparse matrix; one-hot metadata as is).
Yes/no (noul): (a) question wording (instructions), (c) card + guidance without the question, (d) metadata
  (source, wording_id, format_style, defs_style, card_render, card_id, role, depth, deep, k, log2 lengths of the
  instructions / card / state). Chance = majority-class rate of the sample.
Choice: pointwise (row, option) scorer, argmax per row (ties split), chance = mean 1/k.
  (a) option n-grams + question-token x option crosses + "option written in the question";
  (b) option n-grams + option-set structure (k, option set id x option, length rank);
  (c) option n-grams + card listing order of the option (first / last / index / absent) + defs_style x option;
  (d) row metadata x option kind (longest, shortest, card first / last, canonical index).
  Options that are records (several record ids) give no n-grams (length rank only).
Rule (spec 8 G6 exactly, repair r1): accuracy <= chance + 2 pp, point estimate, no p-value condition. Checked for
every view x model (1) on the pooled public-3 sample, (2) per dataset on the pooled-trained CV predictions, and (3) per
dataset with the CV run on that dataset's rows only (spec "per family": a public dataset is the family analogue).
Any cell above chance + 2 pp fails. Every cell's point estimate is written to qc/g6.json. Writes qc/g6.json."""
import json, math, re
from collections import defaultdict
import numpy as np
from scipy import sparse
from sklearn.decomposition import TruncatedSVD
from sklearn.ensemble import HistGradientBoostingClassifier
from sklearn.feature_extraction import DictVectorizer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import GroupKFold
import qclib as Q

FILES = Q.MIXED + ("public3_mtdev.jsonl",)
TOK = re.compile(r"\w+")


def lb(x):
    return int(math.log2(1 + len(TOK.findall(x or ""))))


def qline(r):
    return r["instructions"].split("\n")[-1]


def guide(r):
    return "\n".join(r["instructions"].split("\n")[:-1])


def meta_d(r):
    m = r["meta"]
    return {f"{k}={m.get(k)}": 1 for k in ("wording_id", "format_style", "defs_style", "card_render", "card_id",
                                            "depth", "deep", "k")} | {
        f"src={r['source']}": 1, f"role={r['role']}": 1, f"len_ins={lb(r['instructions'])}": 1,
        f"len_card={lb(r['card'])}": 1, f"len_state={lb(r['state'])}": 1}


def is_rec_opts(r):
    u = r["meta"].get("record_uid")
    return isinstance(u, list) and len(u) > 1


def opt_feats(r):
    """[(option index, {view: dict of features})] for a choice row."""
    o = r["options"]
    lens = [len(x) for x in o]
    card = (r["card"] or "").lower()
    pos = [card.find(x.lower()) for x in o]
    shown = sorted(p for p in pos if p >= 0)
    q = set(TOK.findall(qline(r).lower()))
    rec = is_rec_opts(r)
    md = meta_d(r)
    out = []
    for i, x in enumerate(o):
        ng = {} if rec else {f"o:{t}": 1 for t in TOK.findall(x.lower())} | {f"ot:{x.lower()}": 1}
        lr = "longest" if lens[i] == max(lens) else "shortest" if lens[i] == min(lens) else "mid"
        cp = "absent" if pos[i] < 0 else "first" if pos[i] == shown[0] else "last" if pos[i] == shown[-1] else "mid"
        kinds = [f"len={lr}", f"card={cp}", f"idx={i}"]
        a = dict(ng) | {f"q:{t}|{x.lower() if not rec else lr}": 1 for t in q} | {
            f"inq={x.lower() in qline(r).lower()}": 1}
        b = dict(ng) | {f"k={len(o)}": 1, f"len={lr}": 1, f"set={'|'.join(sorted(o)) if not rec else 'rec'}|{x if not rec else lr}": 1}
        c = dict(ng) | {f"card={cp}": 1, f"cidx={shown.index(pos[i]) if pos[i] >= 0 else -1}": 1,
                        f"defs={r['meta'].get('defs_style')}|{x.lower() if not rec else lr}": 1}
        d = {f"{k}|{kd}": 1 for k in md for kd in kinds}
        out.append((i, {"a": a, "b": b, "c": c, "d": d}))
    return out


T0 = __import__("time").time()


def log(msg):
    print(f"[{__import__('time').time() - T0:7.1f}s] {msg}", flush=True)


def cv_rows(X, y, groups, model):
    log(f"cv {model} X={X.shape}")
    pred = np.zeros(len(y))
    for tr, te in GroupKFold(5).split(X, y, groups):
        if model == "lr":
            m = LogisticRegression(max_iter=2000, C=1.0)
            m.fit(X[tr], y[tr])
        else:
            m = HistGradientBoostingClassifier(max_iter=200, random_state=0)
            m.fit(X[tr], y[tr])
        pred[te] = m.predict_proba(X[te])[:, 1]
    return pred


def dense(X):
    if X.shape[1] > 64:
        return TruncatedSVD(64, random_state=0).fit_transform(X)
    return X.toarray() if sparse.issparse(X) else X


def bucket_check(acc_by, chance_by, n_by):
    """Spec 8 G6: a cell fails when its accuracy point estimate exceeds chance + 2 pp (no p-value add-on)."""
    cells, fails = {}, []
    for k in sorted(acc_by):
        n, a, c = n_by[k], acc_by[k], chance_by[k]
        cells[k] = {"acc": round(a, 4), "chance": round(c, 4), "margin_pp": round(100 * (a - c), 2), "n": n}
        if a > c + 0.02:
            fails.append((k, round(a, 4), round(c, 4), n))
    return cells, fails


def eval_yn(yn):
    """{view:model -> (acc, chance, per-source cells, per-source fails)} for yes/no rows."""
    y = np.array([int(r["gold"] == 1) for r in yn])
    g = np.array([r["group_id"] for r in yn])
    chance = max(y.mean(), 1 - y.mean())
    views = {"a_question": [qline(r) for r in yn], "c_card_guidance": [(r["card"] or "") + "\n" + guide(r) for r in yn]}
    out = {}
    for v, txt in list(views.items()) + [("d_metadata", None)]:
        if txt is None:
            X = DictVectorizer().fit_transform([meta_d(r) for r in yn]).tocsr()
            Xd = X.toarray()
        else:
            X = TfidfVectorizer(ngram_range=(1, 2), min_df=1, token_pattern=r"\w+").fit_transform(txt).tocsr()
            Xd = dense(X)
        for model, M in (("lr", X), ("hgb", Xd)):
            p = cv_rows(M, y, g, model)
            hit = ((p > 0.5).astype(int) == y).astype(float)
            hit[p == 0.5] = 0.5
            by = defaultdict(list)
            for r, h_, yy in zip(yn, hit, y):
                by[r["source"]].append((h_, yy))
            acc_by = {k: float(np.mean([a for a, _ in v_])) for k, v_ in by.items()}
            ch_by = {k: max(np.mean([b for _, b in v_]), 1 - np.mean([b for _, b in v_])) for k, v_ in by.items()}
            out[f"yn:{v}:{model}"] = (float(hit.mean()), float(chance)) + bucket_check(acc_by, ch_by, {k: len(v_) for k, v_ in by.items()})
    return out


def eval_choice(ch):
    feats, lab, grp, rid = [], [], [], []
    for j, r in enumerate(ch):
        gi = r["options"].index(r["gold"])
        for i, fd in opt_feats(r):
            feats.append(fd)
            lab.append(int(i == gi))
            grp.append(r["group_id"])
            rid.append(j)
    lab, grp, rid = np.array(lab), np.array(grp), np.array(rid)
    ch_chance = float(np.mean([1 / len(r["options"]) for r in ch]))
    out = {}
    for v in ("a", "b", "c", "d"):
        X = DictVectorizer().fit_transform([f[v] for f in feats]).tocsr()
        for model, M in (("lr", X), ("hgb", dense(X))):
            s = cv_rows(M, lab, grp, model)
            hits = np.zeros(len(ch))
            for j in range(len(ch)):
                idx = np.where(rid == j)[0]
                best = idx[s[idx] == s[idx].max()]
                hits[j] = lab[best].sum() / len(best)
            by = defaultdict(list)
            for r, h_ in zip(ch, hits):
                by[r["source"]].append((h_, 1 / len(r["options"])))
            acc_by = {k: float(np.mean([a for a, _ in v_])) for k, v_ in by.items()}
            ch_by = {k: float(np.mean([b for _, b in v_])) for k, v_ in by.items()}
            out[f"choice:{v}:{model}"] = (float(hits.mean()), ch_chance) + bucket_check(acc_by, ch_by, {k: len(v_) for k, v_ in by.items()})
    return out


def main():
    rows = [r for f in FILES for r in Q.load(f)]
    res, prob = {"rows": len(rows)}, []
    yn = [r for r in rows if r["qtype"] == "noul"]
    ch = [r for r in rows if r["qtype"] == "choice"]
    out, per_ds = {}, {}
    for kind, sub, fn in (("yn", yn, eval_yn), ("choice", ch, eval_choice)):
        for key, (acc, chance, cells, fails) in fn(sub).items():
            out[key] = {"acc": round(acc, 4), "chance": round(chance, 4), "margin_pp": round(100 * (acc - chance), 2),
                        "per_dataset_pooled_cv": cells, "per_dataset_fails": fails}
            if acc > chance + 0.02 or fails:
                prob.append(f"pooled:{key}" + (f" {[f[0] for f in fails]}" if fails else ""))
        for src in sorted({r["source"] for r in sub}):
            part = [r for r in sub if r["source"] == src]
            log(f"per-dataset CV {kind} {src} n={len(part)}")
            for key, (acc, chance, cells, fails) in fn(part).items():
                c = cells[src]
                per_ds.setdefault(src, {})[key] = c
                if c["acc"] > c["chance"] + 0.02:
                    prob.append(f"own_cv:{src}:{key}")
    res |= {"yn_rows": len(yn), "choice_rows": len(ch), "results": out, "per_dataset_own_cv": per_ds}
    o = {"gate": "G6", "pass": not prob, "problems": prob,
         "rule": "spec 8 G6: accuracy <= chance + 2 pp (point estimate; no p-value condition) for every view x model, "
                 "pooled, per dataset on pooled CV, and per dataset with its own 5-fold GroupKFold(group_id) CV",
         **res}
    (Q.HERE / "g6.json").write_text(json.dumps(o, indent=1))
    print(json.dumps({"pass": o["pass"], "problems": prob, "yn_rows": len(yn), "choice_rows": len(ch)}))
    worst = sorted(((float(c["margin_pp"]), s_, k) for s_, d in per_ds.items() for k, c in d.items()), reverse=True)[:8]
    worst2 = sorted(((float(c["margin_pp"]), s_, k) for k, v in out.items() for s_, c in v["per_dataset_pooled_cv"].items()),
                    reverse=True)[:8]
    print("worst own-cv:", worst)
    print("worst pooled-cv per dataset:", worst2)


if __name__ == "__main__":
    main()
