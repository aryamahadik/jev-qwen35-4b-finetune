"""G7 feature z-test (independent F5 checker). C_DATA_SPEC 8 G7 + F5 G0 8 (G7 row cap, F5-R2-15) and 9.
Every F5 row is yes/no, p0 = 1/2. Feature = presence of a lower-cased word unigram / bigram in the model-visible text
(card + instructions + state), or a metadata value (spec G6 (d) list + F5 G0 9 sidecar additions; label-derived
fields gold, v_P, pair_change never used). Test per feature with n >= N_MIN rows: one-sided exact binomial in the
majority direction, alpha 0.01 Bonferroni over the tested features (gate). Also reported: the spec's normal-approx
z rule, the bar with the spec's 50K-feature denominator, and a card-adjusted variant (null p_r = the row's card yes
rate, leave-one-out; normal approx) because per-card yes rates are drawn 20-80% by design (report only).
Usage: g7.py <name>"""
import json, math, sys
from collections import defaultdict, Counter
from scipy.stats import binom, norm
import qc_lib as L

NAME = sys.argv[1] if len(sys.argv) > 1 else "candidates_r1"
ALPHA, N_MIN = 0.01, 20


def bucket(v):
    return str(v) if v < 4 else "4+"


def meta_set(r, s, attacked):
    m = r["meta"]; f = set()
    for k, v in (("sampler", m["sampler"]), ("wording", m["wording_id"]), ("style", m["format_style"]),
                 ("defs", m["defs_style"]), ("pack", m["domain_pack"]), ("row_type", s["row_type"]),
                 ("template", s["template"]), ("core", s["core"]), ("frame", s["frame"]), ("frame_id", s["frame_id"]),
                 ("location", s["location"]), ("world", s["world_cell"]), ("card_form", s["card_form"]),
                 ("tag_P", s["tag_P"]), ("polarity_P", s["polarity_P"]), ("yes_is_bad", s["yes_is_bad"]),
                 ("no_pol", s["no_polarity"]), ("inverted", s["inverted"]), ("fewshot", s["fewshot"]),
                 ("decoy", s["decoy"]), ("two_lcore", s["two_lcore"]), ("vcore", s["vcore"]),
                 ("attack_push", s["attack_push"]), ("base_attacked", attacked), ("pair_member", s["pair_member"]),
                 ("k_neg", s["k_neg"]), ("k_syn", s["k_syn"]), ("k_all", s["k_all"]), ("j_q", bucket(s["j_q"])),
                 ("j_t", bucket(s["j_t"])), ("t_txt", bucket(s["t_txt"])), ("depth", s["base_depth"]),
                 ("deep", m.get("deep")), ("n_fam", len(s["families"])), ("twin_kind", m.get("twin_kind"))):
        f.add(f"meta:{k}={v}")
    for x in s["families"]:
        f.add("meta:fam=" + x)
    for x in s["sem_keys"]:
        f.add("meta:sem=" + x)
    f.add("meta:fams=" + "+".join(sorted(s["families"])))
    ls = len(r["state"]); f.add(f"meta:len_state~{min(ls // 400, 8)}")
    f.add(f"meta:n_nums~{min(len(L.nums(r['state'])) // 3, 6)}")
    return f


def main():
    rows = L.load(NAME); side = L.load_side(NAME)
    att = {side[r["id"]]["base_id"] for r in rows if side[r["id"]]["row_type"] == "Vp"}
    y = [int(r["gold"]) for r in rows]
    card = [r["meta"]["card_id"] for r in rows]
    cs = defaultdict(lambda: [0, 0])
    for c, v in zip(card, y):
        cs[c][0] += v; cs[c][1] += 1
    pr = [((cs[c][0] - v) / (cs[c][1] - 1)) if cs[c][1] > 1 else 0.5 for c, v in zip(card, y)]
    occ = defaultdict(list)
    for i, r in enumerate(rows):
        s = side[r["id"]]
        for f in L.ngrams(L.full_text(r)) | meta_set(r, s, s["base_id"] in att):
            occ[f].append(i)
    tested = {f: ix for f, ix in occ.items() if len(ix) >= N_MIN}
    nf = len(tested); thr = ALPHA / nf; thr50 = ALPHA / 50000
    zc = norm.isf(thr)
    fails, adj_fails, near = [], [], []
    for f, ix in tested.items():
        n = len(ix); x = sum(y[i] for i in ix); k = max(x, n - x)
        p = float(binom.sf(k - 1, n, 0.5))
        z = (k - n / 2) / math.sqrt(n / 4)
        mu = sum(pr[i] for i in ix); var = sum(pr[i] * (1 - pr[i]) for i in ix) or 1e-9
        za = (abs(x - mu) - 0.5) / math.sqrt(var); pa = float(norm.sf(za))
        rec = {"feature": f, "n": n, "yes": x, "share_major": round(k / n, 4), "p": p, "z": round(z, 2),
               "n_cards": len({card[i] for i in ix}), "p_card_adj": pa}
        if p < thr:
            fails.append(rec)
        elif p < thr * 100:
            near.append(rec)
        if pa < thr:
            adj_fails.append(rec)
    fails.sort(key=lambda d: d["p"]); adj_fails.sort(key=lambda d: d["p_card_adj"]); near.sort(key=lambda d: d["p"])
    out = {"set": NAME, "rows": len(rows), "yes_rate": round(sum(y) / len(y), 4), "n_min": N_MIN,
           "features_tested": nf, "alpha_bonf": thr, "z_crit": round(float(zc), 3),
           "n_fail": len(fails), "fails": fails[:60],
           "n_fail_at_50k_denominator": sum(1 for d in fails if d["p"] < thr50),
           "n_fail_text": sum(1 for d in fails if not d["feature"].startswith("meta:")),
           "n_fail_meta": sum(1 for d in fails if d["feature"].startswith("meta:")),
           "n_near_within_100x": len(near), "near": near[:30],
           "card_adjusted": {"n_fail": len(adj_fails), "fails": adj_fails[:30], "note": "report only"},
           "pass": len(fails) == 0}
    json.dump(out, open(L.QC / f"g7_{NAME}.json", "w"), indent=1)
    print(json.dumps({k: out[k] for k in ("set", "features_tested", "n_fail", "n_fail_text", "n_fail_meta", "pass")}))
    for d in fails[:15]:
        print(d["feature"], d["n"], d["share_major"], d["n_cards"], "%.2e" % d["p"])


if __name__ == "__main__":
    main()
