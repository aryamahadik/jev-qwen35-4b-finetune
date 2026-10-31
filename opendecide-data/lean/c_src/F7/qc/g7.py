"""G7 feature z-test (independent F7 checker). C_DATA_SPEC 8 G7 + F7 G0 6.5. Every F7 row is a K-option ordinal choice
row; p0 = 1/K. Label classes = (K, gold level index). Feature = presence of a lower-cased word unigram / bigram in the
model-visible text (card + instructions + state), or a metadata value (data spec G6 (d) list and the G0 6.5 list,
as visible in the prompt). Test per (feature, K, level) with n >= N_MIN rows of that K carrying the feature:
one-sided exact binomial upper tail, p0 = 1/K; alpha 0.01 Bonferroni over all tests (gate). Option-level features
(G0 6.5: gold level name / number in the case text; longest option): among rows where m of K options carry the
property (0 < m < K), the number of rows whose gold carries it vs the Poisson-binomial null sum(m_i / K_i), one-sided
normal with continuity correction; same Bonferroni (gate). Hidden meta (sampler, row_kind, twin_kind, case_features)
is tested and reported separately (info). Usage: g7.py <name>"""
import json, math, re, sys
import numpy as np
from collections import defaultdict, Counter
from scipy.stats import binom, norm
from scipy.sparse import csr_matrix
import qc_lib as L

NAME = sys.argv[1] if len(sys.argv) > 1 else "candidates_r1"
ALPHA, N_MIN = 0.01, 20


def b4(v):
    return str(v) if v < 4 else "4+"


def meta_vis(r):
    m = r["meta"]; st = r["state"]; nu = L.nums(st)
    f = {f"meta:{k}={v}" for k, v in (("K", len(r["options"])), ("mode", m.get("mode")), ("defs", m.get("defs_style")),
                                      ("container", m.get("container")), ("style", m.get("format_style")),
                                      ("wording", m.get("wording_id")), ("label_form", m.get("label_form")),
                                      ("defs_variant", m.get("defs_variant")), ("fewshot", m.get("fewshot_template")),
                                      ("pack", m.get("domain_pack")), ("depth", m.get("depth")), ("deep", m.get("deep")),
                                      ("attack", bool((m.get("case_features") or {}).get("injected"))))}
    f.add(f"meta:len_state~{min(len(st) // 200, 10)}")
    f.add(f"meta:n_nums~{min(len(nu), 8)}")
    if nu:
        f.add(f"meta:mag_max~{int(math.log10(max(abs(x) for x in nu) + 1))}")
    f.add(f"meta:n_absence~{min(len(L.NEG_RX.findall(st)), 8)}")
    f.add(f"meta:n_lines~{min(st.count(chr(10)), 12)}")
    return f


def meta_hidden(r):
    m = r["meta"]; cf = m.get("case_features") or {}
    f = {f"hid:sampler={m['sampler']}", f"hid:row_kind={m.get('row_kind')}", f"hid:twin_kind={m.get('twin_kind')}"}
    for k, v in cf.items():
        f.add(f"hid:cf_{k}={b4(v) if isinstance(v, int) and not isinstance(v, bool) else v}")
    return f


def binom_tests(rows, feats_per_row):
    """-> list of (feature, K, level, n, x, p)."""
    vocab = {}
    ind, ptr = [], [0]
    for fs in feats_per_row:
        for f in fs:
            ind.append(vocab.setdefault(f, len(vocab)))
        ptr.append(len(ind))
    X = csr_matrix((np.ones(len(ind), np.int32), ind, ptr), shape=(len(rows), len(vocab)))
    names = np.array(sorted(vocab, key=vocab.get))
    out = []
    for k in sorted({len(r["options"]) for r in rows}):
        ix = np.array([i for i, r in enumerate(rows) if len(r["options"]) == k])
        Xk = X[ix]; n_f = np.asarray(Xk.sum(0)).ravel()
        keep = np.flatnonzero(n_f >= N_MIN)
        lv = np.array([L.level(rows[i]) for i in ix])
        for j in range(k):
            x = np.asarray(Xk[lv == j][:, keep].sum(0)).ravel()
            p = binom.sf(x - 1, n_f[keep], 1.0 / k)
            for f, nn, xx, pp in zip(names[keep], n_f[keep], x, p):
                out.append((str(f), k, j, int(nn), int(xx), float(pp)))
    return out


def option_tests(rows):
    props = defaultdict(list)  # prop -> list of (m, K, gold_has)
    for r in rows:
        k = len(r["options"]); st = r["state"].lower(); g = r["gold"]
        inj = bool((r["meta"].get("case_features") or {}).get("injected")) or r["meta"].get("twin_kind") == "inv"
        defs = L.card_defs(r.get("card")); lens = {o: len(o) for o in r["options"]}
        served = {o: len(o + (": " + defs[o] if o in defs else "")) for o in r["options"]}
        P = {}
        P["name_in_state"] = {o for o in r["options"]
                              if any(len(w) >= 3 and re.search(r"\b" + re.escape(w) + r"\b", st) for w in L.toks(L.opt_name(o)))}
        P["num_in_state"] = {o for o in r["options"] if L.opt_num(o) and re.search(r"(?<![\d.])" + L.opt_num(o) + r"(?![\d.])", st)}
        P["longest_label"] = {o for o in r["options"] if lens[o] == max(lens.values())}
        P["shortest_label"] = {o for o in r["options"] if lens[o] == min(lens.values())}
        if defs:
            P["longest_served"] = {o for o in r["options"] if served[o] == max(served.values())}
            P["shortest_served"] = {o for o in r["options"] if served[o] == min(served.values())}
        for nm, s in P.items():
            if 0 < len(s) < k:
                props[nm].append((len(s), k, int(g in s)))
                props[nm + ("[attack rows]" if inj else "[clean rows]")].append((len(s), k, int(g in s)))
    res = []
    for nm, v in props.items():
        n = len(v)
        if n < N_MIN:
            continue
        mu = sum(m / k for m, k, _ in v); var = sum((m / k) * (1 - m / k) for m, k, _ in v); x = sum(g for *_, g in v)
        z = (abs(x - mu) - 0.5) / math.sqrt(var) if var else 0.0
        res.append({"feature": "opt:" + nm, "n": n, "gold_has": x, "expected": round(mu, 1), "z": round(z, 2),
                    "p_two_sided": float(2 * norm.sf(z)), "share": round(x / n, 4), "null_share": round(mu / n, 4)})
    return res


def main():
    rows = L.load(NAME)
    text_f = [L.ngrams(L.full_text(r)) | meta_vis(r) for r in rows]
    T = binom_tests(rows, text_f)
    Hd = binom_tests(rows, [meta_hidden(r) for r in rows])
    O = option_tests(rows)
    for o in O:
        o["gated"] = "[" not in o["feature"]
    # recheck:F7 fix (spec 8 G7): "alpha 0.01 Bonferroni over FEATURES" (yes/no: 50K features -> per-test p < 2e-7, each
    # label direction tested at that bar). The old denominator counted every (feature, K, level) test, which made the
    # per-test bar ~K x strata times stricter than spec (a more lenient gate). Gate = spec bar; old bar kept as info.
    ntests = len(T) + len(O); thr_old = ALPHA / ntests
    nfeat = len({t[0] for t in T}) + sum(1 for o in O if o["gated"]); thr = ALPHA / nfeat
    fails = sorted([t for t in T if t[5] < thr], key=lambda t: t[5])
    ofails = [o for o in O if o["gated"] and o["p_two_sided"] < thr]
    hthr = ALPHA / max(1, len(Hd)); hf = sorted([t for t in Hd if t[5] < hthr], key=lambda t: t[5])
    near = sorted([t for t in T if thr <= t[5] < thr * 100], key=lambda t: t[5])
    cards_of = {}
    for i, fs in enumerate(text_f):
        pass
    def ncards(f, K):
        return len({r["meta"]["card_id"] for r, fs in zip(rows, text_f) if len(r["options"]) == K and f in fs})
    fmt = lambda t: {"feature": t[0], "K": t[1], "level": t[2], "n": t[3], "x": t[4], "share": round(t[4] / t[3], 4),
                     "p": t[5], "n_cards": ncards(t[0], t[1]) if not t[0].startswith("hid:") else None}
    out = {"set": NAME, "rows": len(rows), "n_min": N_MIN, "tests": ntests, "features_tested": len({t[0] for t in T}),
           "alpha_bonf": thr, "bonf_denominator": "features (spec 8)", "n_features_bonf": nfeat,
           "alpha_bonf_old_over_tests": thr_old, "n_fail_old_bar": sum(1 for t in fails if t[5] < thr_old)
           + sum(1 for o in ofails if o["p_two_sided"] < thr_old), "n_fail": len(fails) + len(ofails),
           "n_fail_text": sum(1 for t in fails if not t[0].startswith("meta:")),
           "n_fail_meta": sum(1 for t in fails if t[0].startswith("meta:")), "fails": [fmt(t) for t in fails[:60]],
           "option_level_tests": O, "option_level_fails": ofails,
           "n_near_within_100x": len(near), "near": [fmt(t) for t in near[:25]],
           "hidden_meta_info": {"tests": len(Hd), "alpha_bonf": hthr, "n_fail": len(hf), "fails": [fmt(t) for t in hf[:30]],
                                "note": "not visible in the prompt; report only"},
           "pass": len(fails) == 0 and len(ofails) == 0}
    json.dump(out, open(L.QC / f"g7_{NAME}.json", "w"), indent=1)
    print(json.dumps({k: out[k] for k in ("set", "tests", "n_features_bonf", "alpha_bonf", "n_fail", "n_fail_old_bar", "n_fail_text", "n_fail_meta", "pass")}))
    for t in fails[:15]:
        print(fmt(t))
    for o in O:
        print(o)
    print("hidden fails", len(hf), [fmt(t) for t in hf[:8]])


if __name__ == "__main__":
    main()
