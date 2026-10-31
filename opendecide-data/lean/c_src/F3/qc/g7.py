"""G7 feature z-test (independent F3 checker). Spec 8: one-sided binomial per unigram, bigram and metadata feature,
p0 = 1/k, alpha 0.01 Bonferroni over the tested features.
- Yes/no rows: feature = presence of a lower-cased word unigram or bigram in the model-visible text (card +
  instructions + state), or a metadata value (row meta, sidecar, binned counts of 'void'/'correction' tokens).
  x = rows with the feature's majority label; p = P(Bin(n, 0.5) >= x).
- Choice rows: feature = a unigram or bigram inside an option text, or an option kind (abstain, longest, shortest,
  look-alike siblings). Unit = (row, option holding f); success = option is gold; null p = m_r / k_r per row
  (Poisson-binomial, normal approximation with continuity correction), tested in both directions.
- Choice rows that show an abstain option: row-level text and metadata features vs "gold is the abstain option",
  p0 = 1/k per row, both directions.
Features with fewer than N_MIN occurrences cannot reach the Bonferroni bar and are not counted. Usage: g7.py <name>"""
import json, math, re, sys
from collections import Counter, defaultdict
from scipy.stats import binom, norm
import qc_lib as L

NAME = sys.argv[1] if len(sys.argv) > 1 else "qc_sample"
ALPHA = 0.01
N_MIN = 20
TOK = re.compile(r"[a-z0-9]+(?:['-][a-z0-9]+)*")


def ngrams(text):
    t = TOK.findall(text.lower())
    return set(t) | {a + " " + b for a, b in zip(t, t[1:])}


def meta_set(r, s):
    c, n = L.meta_feats(r, s)
    f = {f"meta:{k}={v}" for k, v in c.items()}
    for k, v in n.items():
        if k.startswith("len_") or k in ("state_n_ids",):
            v = int(math.log2(1 + v))
        f.add(f"meta:{k}={v}")
    txt = L.full_text(r).lower()
    f.add(f"meta:n_void_tok={min(txt.count('void'), 6)}"); f.add(f"meta:n_corr_tok={min(txt.count('correct'), 6)}")
    return f


def pb_test(x, ps):
    """Poisson-binomial z (continuity corrected); returns (z, p_upper, p_lower)."""
    mu = sum(ps); var = sum(p * (1 - p) for p in ps)
    if var <= 0:
        return 0.0, 1.0, 1.0
    sd = math.sqrt(var)
    return (x - mu) / sd, float(norm.sf((x - 0.5 - mu) / sd)), float(norm.cdf((x + 0.5 - mu) / sd))


def main():
    rows, side = L.load(NAME)
    yn = [r for r in rows if L.is_yn(r)]; ch = [r for r in rows if not L.is_yn(r)]
    out = {"gate": "G7", "file": f"out/{NAME}.jsonl", "alpha": ALPHA, "n_min": N_MIN}
    # ---- yes/no
    cnt = Counter(); yes = Counter(); mu_c = Counter(); var_c = Counter()
    cy = Counter(); cn = Counter()
    for r in yn:
        cy[r["meta"]["card_id"]] += int(r["gold"]); cn[r["meta"]["card_id"]] += 1
    base = sum(cy.values()) / max(1, len(yn))
    for r in yn:
        fs = ngrams(L.full_text(r)) | meta_set(r, side.get(r["id"]))
        g = int(r["gold"]); pc = cy[r["meta"]["card_id"]] / cn[r["meta"]["card_id"]]
        for f in fs:
            cnt[f] += 1; yes[f] += g; mu_c[f] += pc; var_c[f] += pc * (1 - pc)
    tested = [f for f, n in cnt.items() if n >= N_MIN]
    bar = ALPHA / max(1, len(tested)); fails = []
    for f in tested:
        n = cnt[f]; x = max(yes[f], n - yes[f]); p = float(binom.sf(x - 1, n, 0.5))
        if p < bar:
            fails.append({"feature": f if f.startswith("meta:") else "<ngram>", "n": n, "major_share": round(x / n, 4),
                          "major": "yes" if yes[f] * 2 >= n else "no", "p": p, "_f": f})
    out["yes_no"] = {"rows": len(yn), "yes_rate": round(sum(int(r["gold"]) for r in yn) / max(1, len(yn)), 4),
                     "features_tested": len(tested), "bonferroni_p": bar, "n_fail": len(fails)}
    out["yes_no"]["fails_top"] = sorted(fails, key=lambda d: d["p"])[:40]
    # sensitivity nulls: (i) p0 = the pool's yes rate; (ii) p0 = the row's card yes rate (spec 2.1: per-card rates
    # vary 20-80% by design), Poisson-binomial z with continuity correction, both directions
    fb, fc = [], []
    for f in tested:
        n = cnt[f]; x = yes[f]
        pb = min(float(binom.sf(x - 1, n, base)), float(binom.cdf(x, n, base)))
        if pb < bar:
            fb.append({"feature": f if f.startswith("meta:") else "<ngram>", "n": n, "yes_share": round(x / n, 4), "p": pb, "_f": f})
        if var_c[f] > 0:
            sd = math.sqrt(var_c[f]); pu = float(norm.sf((x - 0.5 - mu_c[f]) / sd)); pl = float(norm.cdf((x + 0.5 - mu_c[f]) / sd))
            if min(pu, pl) < bar / 2:
                fc.append({"feature": f if f.startswith("meta:") else "<ngram>", "n": n, "yes": x, "expected": round(mu_c[f], 1),
                           "z": round((x - mu_c[f]) / sd, 2), "p": min(pu, pl), "_f": f})
    out["yes_no"]["null_base_rate"] = {"p0": round(base, 4), "n_fail": len(fb), "fails_top": sorted(fb, key=lambda d: d["p"])[:40]}
    out["yes_no"]["null_card_rate"] = {"n_fail": len(fc), "fails_top": sorted(fc, key=lambda d: d["p"])[:40]}
    # primary card-conditioned null (generator contract, F3 G0 R2-05): base rows (no twin_of) ~ Bernoulli(the card's
    # drawn yes rate, sidecar card_yes_rate); Poisson-binomial z with continuity correction, both directions
    cntb = Counter(); yb = Counter(); mub = Counter(); vb = Counter()
    for r in yn:
        if r["meta"].get("twin_of"):
            continue
        s = side.get(r["id"]) or {}; pd = float(s.get("card_yes_rate") or 0.5); g = int(r["gold"])
        for f in ngrams(L.full_text(r)) | meta_set(r, s):
            cntb[f] += 1; yb[f] += g; mub[f] += pd; vb[f] += pd * (1 - pd)
    tb = [f for f, n in cntb.items() if n >= N_MIN]; barb = ALPHA / max(1, 2 * len(tb)); fd = []
    for f in tb:
        sd = math.sqrt(vb[f]); x = yb[f]
        pu = float(norm.sf((x - 0.5 - mub[f]) / sd)); pl = float(norm.cdf((x + 0.5 - mub[f]) / sd))
        if min(pu, pl) < barb:
            fd.append({"feature": f if f.startswith("meta:") else "<ngram>", "n": cntb[f], "yes": x, "expected": round(mub[f], 1),
                       "z": round((x - mub[f]) / sd, 2), "p": min(pu, pl), "_f": f})
    out["yes_no"]["null_drawn_card_rate_base_rows"] = {"rows": sum(1 for r in yn if not r["meta"].get("twin_of")),
        "features_tested": len(tb), "bonferroni_p": barb, "n_fail": len(fd), "fails_top": sorted(fd, key=lambda d: d["p"])[:40]}
    choice_tests(ch, side, out)
    out["pass_literal_p0_half"] = out["yes_no"]["n_fail"] == 0
    out["pass"] = (out["yes_no"]["null_drawn_card_rate_base_rows"]["n_fail"] == 0 and out["choice_options"]["n_fail"] == 0
                   and out["choice_abstain"]["n_fail"] == 0)
    return out


def opt_kinds(r):
    opts = r["options"]; lens = [len(o) for o in opts]; out = []
    for i, o in enumerate(opts):
        ks = set()
        if L.is_abstain(o):
            ks.add("kind:abstain")
        if lens[i] == max(lens):
            ks.add("kind:longest")
        if lens[i] == min(lens):
            ks.add("kind:shortest")
        if L.ID_RX.fullmatch(o):
            ks.add("kind:id")
            sib = sum(1 for j, p in enumerate(opts) if j != i and len(p) == len(o) and sum(a != b for a, b in zip(o, p)) <= 1)
            ks.add(f"kind:id_sib1={min(sib, 3)}")
        out.append(ks)
    return out


def choice_tests(ch, side, out):
    xs = Counter(); ps = defaultdict(list)
    for r in ch:
        k = len(r["options"]); per = defaultdict(int); gold_has = set()
        kinds = opt_kinds(r)
        for i, o in enumerate(r["options"]):
            fs = {"opt:" + g for g in ngrams(o)} | kinds[i]
            for f in fs:
                per[f] += 1
                if o == r["gold"]:
                    gold_has.add(f)
        for f, m in per.items():
            ps[f].append(m / k); xs[f] += int(f in gold_has)
    tested = [f for f, p in ps.items() if len(p) >= N_MIN]
    bar = ALPHA / max(1, 2 * len(tested)); fails = []
    for f in tested:
        z, pu, pl = pb_test(xs[f], ps[f])
        if min(pu, pl) < bar:
            fails.append({"feature": f if f.startswith("kind:") else "<opt-ngram>", "rows": len(ps[f]), "gold_hits": xs[f],
                          "expected": round(sum(ps[f]), 2), "z": round(z, 2), "p": min(pu, pl), "_f": f})
    out["choice_options"] = {"rows": len(ch), "features_tested": len(tested), "bonferroni_p": bar, "n_fail": len(fails),
                             "fails_top": sorted(fails, key=lambda d: d["p"])[:40]}
    # abstain-gold vs row-level features
    ab = [r for r in ch if any(L.is_abstain(o) for o in r["options"])]
    xs = Counter(); ps = defaultdict(list)
    for r in ab:
        k = len(r["options"]); gold_ab = int(L.is_abstain(r["gold"]))
        fs = ngrams(r["instructions"] + "\n" + (r.get("card") or "") + "\n" + r["state"]) | meta_set(r, side.get(r["id"]))
        for f in fs:
            ps[f].append(1 / k); xs[f] += gold_ab
    tested = [f for f, p in ps.items() if len(p) >= N_MIN]
    bar = ALPHA / max(1, 2 * len(tested)); fails = []
    for f in tested:
        z, pu, pl = pb_test(xs[f], ps[f])
        if min(pu, pl) < bar:
            fails.append({"feature": f if f.startswith("meta:") else "<ngram>", "rows": len(ps[f]), "abstain_gold": xs[f],
                          "expected": round(sum(ps[f]), 2), "z": round(z, 2), "p": min(pu, pl), "_f": f})
    out["choice_abstain"] = {"rows": len(ab), "abstain_gold": sum(int(L.is_abstain(r["gold"])) for r in ab),
                             "expected": round(sum(1 / len(r["options"]) for r in ab), 2), "features_tested": len(tested),
                             "bonferroni_p": bar, "n_fail": len(fails), "fails_top": sorted(fails, key=lambda d: d["p"])[:40]}


if __name__ == "__main__":
    res = main()
    (L.QC / f"g7_{NAME}.json").write_text(json.dumps(res, indent=1))
    print(json.dumps({k: (v if not isinstance(v, dict) else {kk: vv for kk, vv in v.items() if kk != "fails_top"})
                      for k, v in res.items()}))
