"""G10 balance (independent F1 checker), all v4 rules (spec 8 G10, 2.1) plus the F1 G0 section 8 targets that the
sidecar lets a checker compute. Counts only. NOTE: F1 G0 8 says these targets bind on the kept rows after G9 crowd
selection; G9 has not run, so difficulty_bin is empty and every check here is on the generated pool (pre-selection).
Usage: g10.py [candidates_r1|qc_sample]"""
import json, sys, math
from collections import Counter, defaultdict
from scipy.stats import chisquare, binomtest, fisher_exact
import qc_lib as q

NAME = sys.argv[1] if len(sys.argv) > 1 else "candidates_r1"
rows, side = q.load(NAME)
yn = [r for r in rows if q.is_yn(r)]; ch = [r for r in rows if not q.is_yn(r)]
S = lambda r: side.get(r["id"]) or {}
out = {"gate": "G10", "file": f"out/{NAME}.jsonl", "rows": len(rows), "yes_no": len(yn), "choice": len(ch),
       "note": "pre-selection pool (G9 bins absent); F1 G0 8 binds targets after crowd selection", "checks": {}}
C = out["checks"]


def rate(xs):
    return round(sum(xs) / len(xs), 4) if xs else None


# 1. yes rate cells: family x wording x bin x negation count (k_all); bin absent -> pooled
cells = defaultdict(list)
for r in yn:
    cells[(r["meta"]["wording_id"], str(r["meta"].get("difficulty_bin")), S(r).get("k_all"))].append(int(r["gold"]))
cl = []
for k, v in cells.items():
    rt = sum(v) / len(v); p = binomtest(sum(v), len(v), 0.5).pvalue
    cl.append({"cell": list(map(str, k)), "n": len(v), "yes_rate": round(rt, 4), "p": p})
lit = [c for c in cl if abs(c["yes_rate"] - 0.5) > 0.02]
sig = [c for c in cl if c["p"] < 0.01]
C["yes_rate_cells"] = {"aggregate": rate([int(r["gold"]) for r in yn]), "cells": len(cl),
                       "cells_outside_2pp": len(lit), "rows_in_cells_outside_2pp": sum(c["n"] for c in lit),
                       "cells_binom_p_lt_0.01": len(sig), "worst": sorted(cl, key=lambda c: c["p"])[:8],
                       "pass_literal": not lit, "pass_stat": not sig}
# F1 marginals one factor at a time, 50 +/- 3
marg = {}
for f in ("world", "policy", "n_amend", "X_role", "pol", "sampler"):
    d = defaultdict(list)
    for r in yn:
        d[str(S(r).get(f))].append(int(r["gold"]))
    marg[f] = {k: [len(v), round(sum(v) / len(v), 4)] for k, v in sorted(d.items())}
bad_m = {f: {k: v for k, v in d.items() if abs(v[1] - 0.5) > 0.03 and v[0] >= 50} for f, d in marg.items()
         if f in ("world", "policy", "n_amend", "X_role")}
C["yes_rate_marginals_F1"] = {"by": marg, "outside_3pp_n_ge_50": bad_m, "pass": not any(bad_m.values())}
# yes = bad outcome 50 +/- 5
yb = [bool(S(r).get("yes_bad")) for r in yn if S(r).get("yes_bad") is not None]
C["yes_bad_share"] = {"share": rate(yb), "pass": abs(rate(yb) - 0.5) <= 0.05}
# negation quotas (counted on yes/no rows)
ks = [S(r).get("k_syn") or 0 for r in yn]
short_neg = sum(1 for r in yn if S(r).get("short") and (S(r).get("k_syn") or 0) > 0)
C["negation"] = {"k_syn_ge1_share": rate([k >= 1 for k in ks]), "k_syn_ge2_share": rate([k >= 2 for k in ks]),
                 "short_rows_negated": short_neg,
                 "pass": rate([k >= 1 for k in ks]) >= 0.10 and rate([k >= 2 for k in ks]) >= 0.02 and short_neg == 0}
units = defaultdict(list)
for r in rows:
    units[r["call_id"]].append(r)
k2 = [r for r in yn if (S(r).get("k_syn") or 0) >= 2]
k2t = [r for r in k2 if any(x is not r and S(x).get("pol") == "aff" for x in units[r["call_id"]])]
C["negation"]["k_syn_ge2_with_aff_twin_share"] = round(len(k2t) / len(yn), 4)
C["negation"]["pass"] = C["negation"]["pass"] and len(k2t) / len(yn) >= 0.02
# 2. gold letter uniform per option-count bucket (canonical order)
pos = defaultdict(lambda: defaultdict(Counter))
for r in ch:
    k = len(r["options"]); pos[q.bucket(k)][k][r["options"].index(r["gold"])] += 1
gl = {}
for b, byk in pos.items():
    ps = []
    for k, cnt in byk.items():
        n = sum(cnt.values())
        if n >= 5 * k:
            ps.append(chisquare([cnt[i] for i in range(k)]).pvalue)
    # pooled within bucket: relative position terciles
    terc = Counter()
    for k, cnt in byk.items():
        for i, c in cnt.items():
            terc[min(2, int(3 * i / k))] += c
    exp = [0, 0, 0]
    for k, cnt in byk.items():
        n = sum(cnt.values())
        for i in range(k):
            exp[min(2, int(3 * i / k))] += n / k
    pt = chisquare([terc[i] for i in range(3)], exp).pvalue
    gl[b] = {"rows": sum(sum(c.values()) for c in byk.values()), "min_p_per_k": min(ps) if ps else None,
             "k_tested": len(ps), "tercile_p": pt}
C["gold_letter_uniform"] = {"by_bucket": gl, "pass": all((v["min_p_per_k"] is None or v["min_p_per_k"] > 0.01)
                                                         and v["tercile_p"] > 0.01 for v in gl.values())}
# 3. longest option is gold within +/- 2 pp of 1/k (overall, per bucket, per gold source)
def longest(rr):
    L = [len(o) for o in rr["options"]]; m = max(L); idx = [i for i, x in enumerate(L) if x == m]
    return idx
grp = defaultdict(lambda: [0.0, 0.0, 0])
for r in ch:
    idx = longest(r); g = r["options"].index(r["gold"]); k = len(r["options"])
    hit = (1.0 / len(idx)) if g in idx else 0.0  # ties share credit
    for key in ("all", "b:" + q.bucket(k), "src:" + str(S(r).get("gold_source"))):
        grp[key][0] += hit; grp[key][1] += 1.0 / k; grp[key][2] += 1
lo = {k: {"n": v[2], "longest_gold": round(v[0] / v[2], 4), "mean_1_over_k": round(v[1] / v[2], 4),
          "diff_pp": round(100 * (v[0] - v[1]) / v[2], 2)} for k, v in grp.items()}
lo_bad = {k: v for k, v in lo.items() if abs(v["diff_pp"]) > 2 and v["n"] >= 100}
C["longest_option_gold"] = {"groups": lo, "outside_2pp_n_ge_100": sorted(lo_bad), "pass": not lo_bad}
# 4. abstain options (CBD, "none of these") wrong on >= 50% of rows that show them
ab = [r for r in ch if any(x in q.ABSTAIN_ROLES for x in (S(r).get("option_roles") or []))]
abg = [S(r)["option_roles"][r["options"].index(r["gold"])] in q.ABSTAIN_ROLES for r in ab]
C["abstain_wrong"] = {"rows_showing": len(ab), "abstain_gold_share": rate(abg),
                      "wrong_share": round(1 - (rate(abg) or 0), 4), "pass": (1 - (rate(abg) or 0)) >= 0.5}
# 5. attack present uncorrelated with label (yes/no: Fisher; choice: gold-role mix vs attack)
a1 = [int(r["gold"]) for r in yn if S(r).get("attack")]; a0 = [int(r["gold"]) for r in yn if not S(r).get("attack")]
p_att = fisher_exact([[sum(a1), len(a1) - sum(a1)], [sum(a0), len(a0) - sum(a0)]]).pvalue if a1 else 1.0
c1 = Counter(str(S(r).get("gold_role")) for r in ch if S(r).get("attack"))
c0 = Counter(str(S(r).get("gold_role")) for r in ch if not S(r).get("attack"))
C["attack_vs_label"] = {"yn_attacked_yes_rate": rate(a1), "yn_clean_yes_rate": rate(a0), "yn_fisher_p": p_att,
                        "choice_attacked_gold_roles": dict(c1), "pass": p_att > 0.01}
# 6. F1 role-rate rule: gold rate of a role on rows showing it = m/k +/- 2 pp per (qtype x k-bucket) cell
rr = defaultdict(lambda: [0, 0.0, 0])
for r in ch:
    s = S(r); roles = s.get("option_roles") or []; k = len(roles); g = roles[r["options"].index(r["gold"])] if roles else None
    for ro in set(roles):
        if ro in ("other", "case"):
            continue
        m = sum(1 for x in roles if x == ro)
        for key in (f"{ro}|{s.get('qtype')}|{q.bucket(k)}", f"{ro}|all"):
            rr[key][0] += int(g == ro); rr[key][1] += m / k; rr[key][2] += 1
rv = {k: {"n": v[2], "gold": round(v[0] / v[2], 4), "expected": round(v[1] / v[2], 4),
          "diff_pp": round(100 * (v[0] - v[1]) / v[2], 2)} for k, v in rr.items()}
rv_bad = {k: v for k, v in rv.items() if abs(v["diff_pp"]) > 2 and v["n"] >= 200}
C["role_rate"] = {"cells": rv, "outside_2pp_n_ge_200": sorted(rv_bad), "pass": not rv_bad}
# Q2 special-code basis share vs mean code-option share
q2 = [r for r in ch if S(r).get("qtype") == "Q2" and S(r).get("gold_basis") in ("rule", "code")]
if q2:
    gc = rate([S(r)["gold_basis"] == "code" for r in q2]); cs = round(sum(float(S(r)["code_share"]) for r in q2) / len(q2), 4)
    C["q2_code_share"] = {"n": len(q2), "gold_code_share": gc, "mean_code_option_share": cs,
                          "diff_pp": round(100 * (gc - cs), 2), "pass": abs(gc - cs) <= 0.02}
# 7. distribution targets (F1 G0 8, v4 2.1)
def shares(vals):
    c = Counter(vals); n = sum(c.values()); return {str(k): round(v / n, 4) for k, v in sorted(c.items(), key=lambda x: str(x[0]))}
bk = shares(q.bucket(len(r["options"])) for r in ch)
tgt = {"2-4": 0.35, "5-9": 0.35, "10-19": 0.15, "20-60": 0.15}
C["option_count_buckets"] = {"shares": bk, "target": tgt, "pass": all(abs(bk.get(k, 0) - v) <= 0.05 for k, v in tgt.items())}
cbd_shown = rate([any(x == "cbd" for x in (S(r).get("option_roles") or [])) for r in ch])
C["cbd_shown_share"] = {"share": cbd_shown, "target": "0.35-0.40", "pass": 0.33 <= cbd_shown <= 0.42}
dn = [S(r).get("depth") for r in rows if not S(r).get("deep")]
ds = shares(dn); dtg = {"1": 0.22, "2": 0.33, "3": 0.28, "4": 0.17}
deep = rate([bool(S(r).get("deep")) for r in rows])
C["depth"] = {"nondeep_shares": ds, "target": dtg, "deep_share": deep,
              "pass": all(abs(ds.get(k, 0) - v) <= 0.03 for k, v in dtg.items()) and deep <= 0.10}
am = shares(S(r).get("n_amend") for r in rows); atg = {"0": 0.35, "1": 0.30, "2": 0.20, "3": 0.15}
C["amendment_count"] = {"shares": am, "target": atg, "pass": all(abs(am.get(k, 0) - v) <= 0.03 for k, v in atg.items())}
gs = Counter(str(S(r).get("gold_source")) for r in rows if S(r).get("gold_source") not in ("CBD", "mixed", "none", None))
nd = sum(gs.values()); gsv = {k: round(v / nd, 4) for k, v in gs.items()}
C["gold_source_monitor"] = {"shares_determined": gsv, "ranges": {"D": "0.15-0.25", "T": "0.08-0.15", "F": "0.05-0.10"},
                            "in_range": {"D": 0.15 <= gsv.get("D", 0) <= 0.25, "T": 0.08 <= gsv.get("T", 0) <= 0.15,
                                         "F": 0.05 <= gsv.get("F", 0) <= 0.10}, "binding": False}
ids = {r["id"] for r in rows}
tw = [r for r in rows if r["meta"].get("twin_of")]
cset = {r["id"] for r in tw} | {r["meta"]["twin_of"] for r in tw if r["meta"]["twin_of"] in ids}
att = sum(1 for r in rows if S(r).get("role") == "attacked")
inert = sum(1 for r in rows if S(r).get("unit_kind") == "U-inert" and S(r).get("role") == "variant")
C["twins_units"] = {"contrast_set_row_share": round(len(cset) / len(rows), 4), "target_contrast": "0.20-0.25",
                    "attacked_row_share": round(att / len(rows), 4), "target_attacked": "about 0.05",
                    "inert_variant_share": round(inert / len(rows), 4), "target_inert": "<= 0.05",
                    "pass": 0.20 <= len(cset) / len(rows) <= 0.25 and 0.03 <= att / len(rows) <= 0.07 and inert / len(rows) <= 0.05}
yq = sum(1 for r in yn); C["yes_no_vs_choice"] = {"yes_no_share": round(yq / len(rows), 4), "target": "0.45-0.55",
                                                  "pass": 0.45 <= yq / len(rows) <= 0.55}
binding = ["yes_rate_cells", "yes_rate_marginals_F1", "yes_bad_share", "negation", "gold_letter_uniform",
           "longest_option_gold", "abstain_wrong", "attack_vs_label", "role_rate", "q2_code_share"]
out["v4_and_F1_balance_checks"] = binding
out["distribution_checks"] = ["option_count_buckets", "cbd_shown_share", "depth", "amendment_count", "twins_units",
                              "yes_no_vs_choice"]
out["failed"] = [k for k, v in C.items() if isinstance(v, dict) and v.get("pass") is False]
out["pass"] = not out["failed"]
(q.QC / f"g10_{NAME}.json").write_text(json.dumps(out, indent=1, default=str))
print(json.dumps({"failed": out["failed"], "pass": out["pass"]}))
