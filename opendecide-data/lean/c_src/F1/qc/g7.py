"""G7 feature z-test (independent F1 checker). Spec 8: one-sided binomial per unigram, bigram and metadata feature,
p0 = 1/k, alpha 0.01 Bonferroni over tested features (n >= N_MIN).
Yes/no: feature = lower-cased word unigram/bigram present in the model-visible text (card + instructions + state),
or a metadata value (qc_lib.meta_feats, incl. X_role). Tests: (1) literal p0 = 0.5 (spec), (2) card-conditioned
null (each row's p0 = its card's empirical yes rate; spec 2.1 draws per-card rates 20-80% by design), both
directions, Poisson-binomial normal approximation. (3) Choice rows: feature = option n-gram or option kind (role,
longest, shortest, shares-outcome / shares-basis counts); unit = (row, option); success = option is gold; null
m_r/k_r per row; both directions. Pass = 0 fails in (2) and (3); (1) reported. Counts only (no row text)."""
import json, math, re, sys
from collections import Counter, defaultdict
from scipy.stats import binom, norm
import qc_lib as q
from g6 import optset, split_opt

NAME = sys.argv[1] if len(sys.argv) > 1 else "qc_sample"
ALPHA, N_MIN = 0.01, 20
TOK = re.compile(r"[a-z0-9]+(?:['-][a-z0-9]+)*")


def ngrams(t):
    t = TOK.findall(t.lower()); return set(t) | {a + " " + b for a, b in zip(t, t[1:])}


def meta_set(r, s):
    c, n = q.meta_feats(r, s); f = {f"meta:{k}={v}" for k, v in c.items()}
    for k, v in n.items():
        if k.startswith("len_") or k == "sc_len_tokens":
            v = int(math.log2(1 + max(v, 0)))
        f.add(f"meta:{k}={v}")
    return f


def pb(x, ps):
    mu = sum(ps); var = sum(p * (1 - p) for p in ps)
    if var <= 0:
        return 0.0, 1.0
    sd = math.sqrt(var); z = (x - mu) / sd
    return z, min(float(norm.sf((x - 0.5 - mu) / sd)), float(norm.cdf((x + 0.5 - mu) / sd)))


rows, side = q.load(NAME)
yn = [r for r in rows if q.is_yn(r)]; ch = [r for r in rows if not q.is_yn(r)]
cy, cn = Counter(), Counter()
for r in yn:
    cy[r["meta"]["card_id"]] += int(r["gold"]); cn[r["meta"]["card_id"]] += 1
cnt, yes, ps = Counter(), Counter(), defaultdict(list)
for r in yn:
    fs = ngrams(q.full_text(r)) | meta_set(r, side.get(r["id"])); gld = int(r["gold"])
    pc = cy[r["meta"]["card_id"]] / cn[r["meta"]["card_id"]]
    for f in fs:
        cnt[f] += 1; yes[f] += gld; ps[f].append(pc)
tested = [f for f, n in cnt.items() if n >= N_MIN]
bar = ALPHA / max(1, len(tested)); lit, card = [], []
for f in tested:
    n = cnt[f]; x = max(yes[f], n - yes[f]); p = float(binom.sf(x - 1, n, 0.5))
    lab = f if f.startswith("meta:") else "<ngram>"
    if p < bar:
        lit.append({"feature": lab, "n": n, "yes_share": round(yes[f] / n, 4), "p": p})
    z, p2 = pb(yes[f], ps[f])
    if p2 < bar / 2:
        card.append({"feature": lab, "n": n, "yes": yes[f], "expected": round(sum(ps[f]), 1), "z": round(z, 2), "p": p2})
out = {"gate": "G7", "file": f"out/{NAME}.jsonl", "alpha": ALPHA, "n_min": N_MIN,
       "yes_no": {"rows": len(yn), "features_tested": len(tested), "bonferroni_p": bar,
                  "literal_p0_half": {"n_fail": len(lit), "n_fail_meta": sum(1 for d in lit if d["feature"] != "<ngram>"),
                                      "fails_top": sorted(lit, key=lambda d: d["p"])[:30]},
                  "card_rate_null": {"n_fail": len(card), "n_fail_meta": sum(1 for d in card if d["feature"] != "<ngram>"),
                                     "fails_top": sorted(card, key=lambda d: d["p"])[:30]}}}
xs, pp = Counter(), defaultdict(list)
for r in ch:
    s = side.get(r["id"]) or {}; roles = s.get("option_roles") or ["?"] * len(r["options"])
    os_ = optset(r, roles); k = len(r["options"]); per = defaultdict(int); gh = set()
    for i, o in enumerate(r["options"]):
        fs = {"opt:" + g for g in ngrams(o)} | {f"kind:role={roles[i]}", f"kind:share_outcome={min(int(os_[i]['share_outcome']), 4)}",
                                               f"kind:share_basis={min(int(os_[i]['share_basis']), 4)}"}
        if os_[i]["is_longest"]:
            fs.add("kind:longest")
        if os_[i]["is_shortest"]:
            fs.add("kind:shortest")
        for f in fs:
            per[f] += 1
            if o == r["gold"]:
                gh.add(f)
    for f, m in per.items():
        pp[f].append(m / k); xs[f] += int(f in gh)
tc = [f for f, p in pp.items() if len(p) >= N_MIN]; barc = ALPHA / max(1, 2 * len(tc)); fc = []
for f in tc:
    z, p = pb(xs[f], pp[f])
    if p < barc:
        fc.append({"feature": f if f.startswith("kind:") else "<opt-ngram>", "rows": len(pp[f]), "gold_hits": xs[f],
                   "expected": round(sum(pp[f]), 1), "z": round(z, 2), "p": p})
out["choice_options"] = {"rows": len(ch), "features_tested": len(tc), "bonferroni_p": barc, "n_fail": len(fc),
                         "n_fail_kind": sum(1 for d in fc if d["feature"] != "<opt-ngram>"),
                         "fails_top": sorted(fc, key=lambda d: d["p"])[:40]}
out["pass"] = out["yes_no"]["card_rate_null"]["n_fail"] == 0 and out["choice_options"]["n_fail"] == 0
(q.QC / f"g7_{NAME}.json").write_text(json.dumps(out, indent=1))
print(json.dumps({"yn_literal_fail": len(lit), "yn_card_fail": len(card), "choice_fail": len(fc), "pass": out["pass"]}))
