"""G7 feature z-test (independent F11 checker, check:F11, c-lanes-v3; adapted from the F8 checker's g7.py, v4 test
unchanged). C_DATA_SPEC 8 G7 + F11 G0 6 (A22, A40, K14, F11-R2-18): one-sided binomial per unigram, bigram and
metadata feature, p0 = 1/k, alpha 0.01 Bonferroni over the tested features (n >= 20).
- Yes/no rows: feature = presence of a lower-cased word unigram/bigram in the model-visible text (card + instructions +
  state + options) or an observable metadata value (chk_lib.meta_feats), plus the F11 yes/no features (asked code or
  group marked; asked name content word in the report; negation word in the report; asked value mentions; asked code
  written in the report; asked code first / last in the card list). Both directions: x = rows with the feature's
  majority label, p = P(Bin(n, .5) >= x).
- Choice rows: feature = a unigram/bigram inside an option text, a v4 option kind (abstain, longest, shortest, numeric
  first / last, listing-order first / last in the card-without-question + state), row-metadata x option-kind crosses,
  and the F11 option features (first / last in the card list; residual code; most connected; max-overlap option;
  option written in the report (suggestion / correction / echo proxy); marked; worked item gold or example code;
  inverted rows: the option's report first / last in `state`). Unit = (row, option set holding f); success = gold
  holds f; null = Poisson-binomial with p = m_r / k_r (normal approx with continuity), both directions (F11-R2-18).
  F11 features are computed from the visible text only (the checker never reads generator internals); lure / echo
  targets are not visible as such, so the max-overlap and written-in-report features stand in for them.
Each failing feature is reported with its distinct card count. Usage: g7.py <name>"""
import json, math, re, sys
from collections import defaultdict
from scipy.stats import binom, norm
import chk_lib as L
import f11_feats as X

NAME = sys.argv[1] if len(sys.argv) > 1 else "qc_sample"
ALPHA = 0.01
N_MIN = 20
TOK = re.compile(r"[a-z0-9]+(?:['.-][a-z0-9]+)*")


def ngrams(text):
    t = TOK.findall(text.lower())
    return set(t) | {a + " " + b for a, b in zip(t, t[1:])}


def binlog(v):
    return int(math.log2(1 + abs(v))) * (1 if v >= 0 else -1)


def meta_set(r, s=None):
    c, n = L.meta_feats(r)
    f = {f"meta:{k}={v}" for k, v in c.items()}
    for k, v in n.items():
        if k.startswith("sem:"):
            f.add(f"meta:{k}")
        elif k.endswith("_log"):
            f.add(f"meta:{k}={int(v)}")
        elif k.startswith(("len_", "ntok", "n_lines", "opt_len", "n_stated")):
            f.add(f"meta:{k}={binlog(v)}")
        else:
            f.add(f"meta:{k}={v}")
    return f


def onum(o):
    n = L.nums(o)
    return n[0] if n else None


def opt_kinds(r):
    opts = r["options"]; ls = [len(o) for o in opts]; out = []
    vals = [onum(o) for o in opts]; nv = sorted(v for v in vals if v is not None)
    v = L.views(r)["cardnoq"] + "\n" + r["state"]; pos = [v.find(o) for o in opts]; ok = sorted(set(p for p in pos if p >= 0))
    for i, o in enumerate(opts):
        k = set()
        if L.is_abstain(o): k.add("kind:abstain")
        if ls[i] == max(ls): k.add("kind:longest")
        if ls[i] == min(ls): k.add("kind:shortest")
        if vals[i] is not None and len(set(nv)) >= 2:
            if vals[i] == nv[0]: k.add("kind:num_first")
            if vals[i] == nv[-1]: k.add("kind:num_last")
        if pos[i] >= 0 and len(ok) >= 2:
            if pos[i] == ok[0]: k.add("kind:list_first")
            if pos[i] == ok[-1]: k.add("kind:list_last")
        out.append(k)
    return out


def pb_test(x, ps):
    mu = sum(ps); var = sum(p * (1 - p) for p in ps)
    if var <= 0:
        return 1.0, 1.0
    z_hi = (x - 0.5 - mu) / math.sqrt(var); z_lo = (mu - x - 0.5) / math.sqrt(var)
    return float(norm.sf(z_hi)), float(norm.sf(z_lo))


def main():
    rows = L.load(NAME)
    yn = [r for r in rows if L.is_yn(r)]; ch = [r for r in rows if not L.is_yn(r)]
    cy = defaultdict(lambda: [0, 0])
    for r in yn:
        c = cy[r["meta"]["card_id"]]; c[0] += 1; c[1] += int(r["gold"])
    F = defaultdict(lambda: [0, 0, set(), 0.0, 0.0])
    for r in yn:
        g = int(r["gold"]); cid = r["meta"]["card_id"]; n_c, y_c = cy[cid]
        pr = (y_c - g) / (n_c - 1) if n_c > 1 else 0.5  # leave-one-out card yes rate (report-only adjusted test)
        for f in ngrams(L.full_text(r)) | meta_set(r) | X.yn_feats(r):
            e = F[f]; e[0] += 1; e[1] += g; e[2].add(cid); e[3] += pr; e[4] += pr * (1 - pr)
    C = defaultdict(lambda: [0, [], set()])
    for r in ch:
        k = len(r["options"]); kinds = [a | b for a, b in zip(opt_kinds(r), X.opt_feats(r))]; cid = r["meta"]["card_id"]
        gi = L.gold_index(r)
        ms = {m for m in meta_set(r) if not m.startswith(("meta:sem:", "meta:format_style", "meta:domain_pack",
                                                         "meta:wording_id"))}
        per = defaultdict(lambda: [0, 0])
        for i, o in enumerate(r["options"]):
            gold = int(i == gi)
            fs = {"opt:" + t for t in ngrams(o)} | kinds[i]
            fs |= {f"x:{m}&{kd}" for m in ms for kd in kinds[i]}
            for f in fs:
                per[f][0] += 1; per[f][1] += gold
        for f, (m, x) in per.items():
            e = C[f]; e[0] += x; e[1].append(m / k); e[2].add(cid)
        if X.short(r):  # F11 G0 6 short-card slice: p0 = 1/t inside the tied-at-max set
            T, sf = X.short_slice(r)
            if T:
                for f, idx in sf.items():
                    e = C[f]; e[0] += int(gi in idx); e[1].append(len(idx) / len(T)); e[2].add(cid)
    tested_yn = {f: v for f, v in F.items() if N_MIN <= v[0] < len(yn)}
    tested_ch = {f: v for f, v in C.items() if len(v[1]) >= N_MIN and 0 < sum(v[1]) < len(v[1])}
    n_tests = len(tested_yn) + len(tested_ch)
    bar = ALPHA / max(1, n_tests)
    fails, adj_fails, near = [], [], 0
    for f, (n, y, cards, mu, var) in tested_yn.items():
        x = max(y, n - y); p = float(binom.sf(x - 1, n, 0.5))
        if p < bar:
            fails.append({"part": "yes_no", "feature": f, "n": n, "yes_rate": round(y / n, 4), "p": p, "n_cards": len(cards)})
        elif p < bar * 100:
            near += 1
        if var > 0:
            pa = float(min(norm.sf((y - 0.5 - mu) / math.sqrt(var)), norm.sf((mu - y - 0.5) / math.sqrt(var))))
            if pa < bar:
                adj_fails.append({"part": "yes_no", "feature": f, "n": n, "yes_rate": round(y / n, 4),
                                  "card_expected_rate": round(mu / n, 4), "p": pa, "n_cards": len(cards)})
    for f, (x, ps, cards) in tested_ch.items():
        p_hi, p_lo = pb_test(x, ps)
        if min(p_hi, p_lo) < bar:
            fails.append({"part": "choice", "feature": f, "n_rows": len(ps), "gold_hits": x, "expected": round(sum(ps), 2),
                          "dir": "over" if p_hi < p_lo else "under", "p": min(p_hi, p_lo), "n_cards": len(cards)})
        elif min(p_hi, p_lo) < bar * 100:
            near += 1
    fails.sort(key=lambda d: d["p"]); adj_fails.sort(key=lambda d: d["p"])
    yn_raw = [f for f in fails if f["part"] == "yes_no"]; chf = [f for f in fails if f["part"] == "choice"]
    yn_multi = [f for f in yn_raw if f["n_cards"] > 1]
    f11 = {f: {"n_rows": len(v[1]), "gold_hits": v[0], "expected": round(sum(v[1]), 2)} for f, v in sorted(tested_ch.items())
           if f.startswith(("f11:", "f11s:"))}
    f11y = {f: {"n": v[0], "yes_rate": round(v[1] / v[0], 4)} for f, v in sorted(tested_yn.items()) if f.startswith("f11:")}
    ok = not chf and not adj_fails and not yn_multi
    out = {"gate": "G7", "file": f"out/{NAME}.jsonl", "alpha": ALPHA, "n_min": N_MIN, "n_tests": n_tests,
           "bonferroni_p": bar, "n_yes_no_rows": len(yn), "n_choice_rows": len(ch),
           "n_tested_yes_no": len(tested_yn), "n_tested_choice": len(tested_ch),
           "n_fail": len(fails), "n_fail_choice": len(chf), "n_fail_yes_no_raw": len(yn_raw),
           "n_fail_yes_no_raw_multi_card": len(yn_multi), "n_fail_yes_no_card_adjusted": len(adj_fails),
           "near_within_100x": near,
           "pass_rule": "no choice failure, no card-adjusted yes/no failure, no raw (p0 = .5) yes/no failure spanning > 1 card "
                        "(the F6 checker's rule; a single-card raw yes/no failure is the card's designed U[20,80] yes rate)",
           "f11_choice_features": f11, "f11_yes_no_features": f11y,
           "fails": fails[:200], "card_adjusted_fails": adj_fails[:100], "pass": ok}
    (L.QC / f"g7_{NAME}.json").write_text(json.dumps(out, indent=1))
    print(json.dumps({k: v for k, v in out.items() if k not in ("fails", "card_adjusted_fails", "f11_choice_features",
                                                               "f11_yes_no_features", "pass_rule")}))


if __name__ == "__main__":
    main()
