"""G10 balance (independent F5 checker). C_DATA_SPEC 2.1 quotas + 8 G10 (v4) + F5 G0 sec 8 targets, on
out/<name>.jsonl with its sidecar, cards and relations files. Every F5 row is yes/no (no options list), so the
gold-letter, longest-option and abstain rules are n/a by construction (reported). Part A = construction-level targets
checkable on a generated pool. Part B = the G10 aggregate cell rule (family x wording x row bin x k_all, 50 +/- 2):
`difficulty_bin` is null on every row (G9 crowd scoring has not run), so bin = 'unscored'. F5 G0 F5-R2-14 says the
targets are checked on the final selected set; Part B is reported raw on this pool plus a feasibility test (can
exact within-cell downsampling keep >= 3,600 rows?). Usage: g10.py <name>"""
import json, sys
from collections import defaultdict, Counter
from scipy.stats import chi2_contingency
import qc_lib as L

NAME = sys.argv[1] if len(sys.argv) > 1 else "candidates_r1"
res = {}


def rate(rows):
    return (sum(int(r["gold"]) for r in rows) / len(rows)) if rows else None


def cells(rows, keyf, tol, nmin=1):
    g = defaultdict(list)
    for r in rows:
        for k in keyf(r):
            g[k].append(r)
    out, bad = {}, []
    for k, rr in sorted(g.items(), key=lambda kv: str(kv[0])):
        y = rate(rr); out[str(k)] = {"n": len(rr), "yes": round(y, 4)}
        if len(rr) >= nmin and abs(y - 0.5) > tol:
            bad.append(str(k))
    return {"cells": out, "tol": tol, "n_min": nmin, "fail_cells": bad, "pass": not bad}


def bucket(v):
    return str(v) if v < 4 else "4+"


def pooled(rows, field, tol):
    """count buckets 0,1,2,3,4+; a bucket < 200 rows is pooled with the adjacent bucket toward 0 (F5-R2-20)."""
    order = ["0", "1", "2", "3", "4+"]
    g = defaultdict(list)
    for r in rows:
        g[bucket(S[r["id"]][field])].append(r)
    merged, cur, lab = [], [], []
    for b in reversed(order):
        cur += g.get(b, []); lab.append(b)
        if len(cur) >= 200:
            merged.append(("+".join(reversed(lab)), cur)); cur, lab = [], []
    if cur:
        if merged:
            k, rr = merged.pop(); merged.append((k + "+" + "+".join(reversed(lab)), rr + cur))
        else:
            merged.append(("+".join(reversed(lab)), cur))
    out = {k: {"n": len(rr), "yes": round(rate(rr), 4)} for k, rr in merged}
    bad = [k for k, v in out.items() if abs(v["yes"] - 0.5) > tol]
    return {"cells": out, "tol": tol, "fail_cells": bad, "pass": not bad}


rows = L.load(NAME); S = L.load_side(NAME)
cards = {d["card_id"]: d for d in (json.loads(l) for l in open(L.OUT / f"{NAME}.cards.jsonl"))}
rels = L.load_relations(NAME)
n = len(rows); sd = lambda r: S[r["id"]]
A = {}
A["overall"] = {"n": n, "yes": round(rate(rows), 4), "pass": abs(rate(rows) - 0.5) <= 0.02}
A["row_type"] = cells(rows, lambda r: [sd(r)["row_type"]], 0.02)
A["k_neg"] = cells(rows, lambda r: [sd(r)["k_neg"]], 0.02)
A["k_all"] = cells(rows, lambda r: [sd(r)["k_all"]], 0.02)
A["j_q"] = pooled(rows, "j_q", 0.02)
A["j_t"] = pooled(rows, "j_t", 0.03)
A["t_txt"] = pooled(rows, "t_txt", 0.03)
A["sampler"] = cells(rows, lambda r: [r["meta"]["sampler"]], 0.02)
A["wording"] = cells(rows, lambda r: [r["meta"]["wording_id"]], 0.02)
A["cue_family"] = cells(rows, lambda r: sd(r)["families"], 0.03, nmin=200)
A["world"] = cells(rows, lambda r: [sd(r)["world_cell"]], 0.03)
A["location"] = cells(rows, lambda r: [sd(r)["location"]], 0.03)
A["sem_key"] = cells(rows, lambda r: sd(r)["sem_keys"], 0.03)
A["A_rows_op_x_world"] = cells([r for r in rows if sd(r)["row_type"] == "A"],
                               lambda r: [(sd(r)["core"], sd(r)["world_cell"])], 0.03, nmin=200)
A["template_n50"] = cells(rows, lambda r: [sd(r)["template"]], 0.10, nmin=50)
A["template_n50"]["report_only"] = True
Q = {}
yb = sum(1 for r in rows if sd(r)["yes_is_bad"]) / n
Q["yes_is_bad_share"] = {"v": round(yb, 4), "rule": "0.45-0.55", "pass": 0.45 <= yb <= 0.55}
npol = sum(1 for r in rows if sd(r)["no_polarity"]) / n
Q["no_polarity_share"] = {"v": round(npol, 4), "rule": "<= 0.05", "pass": npol <= 0.05}
dn = sum(1 for r in rows if sd(r)["k_all"] >= 2) / n
Q["double_negation_k_all>=2"] = {"v": round(dn, 4), "rule": ">= 0.25 (spec 2.2)", "pass": dn >= 0.25}
ks1 = sum(1 for r in rows if sd(r)["k_syn"] >= 1) / n
Q["k_syn>=1_share"] = {"v": round(ks1, 4), "rule": ">= 0.10", "pass": ks1 >= 0.10}
ids = {r["id"] for r in rows}
ks2 = sum(1 for r in rows if sd(r)["k_syn"] >= 2 and r["meta"].get("twin_of") in ids) / n
Q["k_syn>=2_with_affirmative_twin"] = {"v": round(ks2, 4), "rule": ">= 0.02", "pass": ks2 >= 0.02}
att = [r for r in rows if sd(r)["row_type"] == "Vp"]
Q["attack_rows_share"] = {"v": round(len(att) / n, 4), "rule": "0.04-0.06", "pass": 0.04 <= len(att) / n <= 0.06}
tab = [[sum(1 for r in rows if (sd(r)["row_type"] == "Vp") == a and int(r["gold"]) == g) for g in (0, 1)] for a in (False, True)]
p_att = float(chi2_contingency(tab)[1])
Q["attack_present_vs_label"] = {"table": tab, "chi2_p": round(p_att, 4), "rule": "p > 0.01", "pass": p_att > 0.01}
cs = sum(1 for r in rows if sd(r)["pair_member"] and sd(r)["row_type"] != "Vp") / n
Q["contrast_set_share"] = {"v": round(cs, 4), "rule": "0.20-0.25", "pass": 0.20 <= cs <= 0.25}
deep = sum(1 for r in rows if r["meta"].get("deep")) / n
Q["deep_rows"] = {"v": round(deep, 4), "rule": "<= 0.10", "pass": deep <= 0.10}
bases = {}
for r in rows:
    bases.setdefault(sd(r)["base_id"], sd(r))
d3 = sum(1 for b in bases.values() if b["base_depth"] >= 3) / len(bases)
Q["depth>=3_bases"] = {"v": round(d3, 4), "rule": "<= 0.04", "pass": d3 <= 0.04}
dec = sum(1 for r in rows if sd(r)["decoy"]) / n
Q["decoy_rows"] = {"v": round(dec, 4), "rule": ">= 0.10", "pass": dec >= 0.10}
tneg = sum(1 for r in rows if sd(r)["location"] in ("text", "both")) / n
Q["text_side_negation"] = {"v": round(tneg, 4), "rule": ">= 0.30", "pass": tneg >= 0.30}
lc = sum(1 for r in rows if "is the correct answer" in r["instructions"].lower())
Q["label_check_form_rows"] = {"v": lc, "rule": "0", "pass": lc == 0}
vq = [r for r in rows if sd(r)["j_q"] >= 1]
vv = [r for r in vq if sd(r)["p_clause"] and sd(r)["p_clause"].lower() in r["state"].lower()]
Q["verbatim_overlap"] = {"share_of_jq>=1": round(len(vv) / max(1, len(vq)), 4), "yes": round(rate(vv) or 0, 4),
                         "rule": ">= 0.15 share; yes 0.47-0.53",
                         "pass": len(vv) / max(1, len(vq)) >= 0.15 and abs((rate(vv) or 0) - 0.5) <= 0.03}
cs_used = {r["meta"]["card_id"] for r in rows}
cl = [cards[c] for c in cs_used]
inv = sum(1 for c in cl if c["inverted"]) / len(cl); few = sum(1 for c in cl if c["fewshot"]) / len(cl)
Q["cards"] = {"v": len(cl), "rule": ">= 80", "pass": len(cl) >= 80}
Q["inverted_cards"] = {"v": round(inv, 4), "rule": "0.10-0.15", "pass": 0.10 <= inv <= 0.15}
Q["fewshot_cards"] = {"v": round(few, 4), "rule": "0.05-0.10", "pass": 0.05 <= few <= 0.10}
sh = sum(1 for b in bases.values() if b["card_form"] == "short") / len(bases)
Q["short_card_bases"] = {"v": round(sh, 4), "rule": "0.12-0.18", "pass": 0.12 <= sh <= 0.18}
pc = defaultdict(list); nb = defaultdict(set)
for r in rows:
    pc[r["meta"]["card_id"]].append(int(r["gold"])); nb[r["meta"]["card_id"]].add(sd(r)["base_id"])
off = []
for c, g in pc.items():
    real = sum(g) / len(g); tol = 0.05 if len(nb[c]) >= 20 else max(0.05, 5.0 / len(g))
    if abs(real - cards[c]["r_card"]) > tol:
        off.append({"card": c, "r_card": round(cards[c]["r_card"], 3), "real": round(real, 3), "rows": len(g)})
Q["per_card_rate_vs_r_card"] = {"n_off": len(off), "examples": off[:10],
                                "rule": "+/-5 pp (within one base when < 20 bases)", "pass": not off}
Q["gold_letter_uniform"] = {"pass": True, "note": "n/a: yes/no rows have no options list (trainer shows Yes/No)"}
Q["longest_option_gold"] = {"pass": True, "note": "n/a: yes/no rows"}
Q["abstain_wrong"] = {"pass": True, "note": "n/a: no abstain options on F5 rows"}
B = defaultdict(list)
for r in rows:
    B[(r["meta"]["wording_id"], r["meta"]["difficulty_bin"] or "unscored", sd(r)["k_all"])].append(int(r["gold"]))
bad = {str(k): {"n": len(v), "yes": round(sum(v) / len(v), 3)} for k, v in B.items() if abs(sum(v) / len(v) - 0.5) > 0.02}
keep = sum(2 * min(sum(v), len(v) - sum(v)) for v in B.values())
res = {"set": NAME, "rows": n, "A_construction": A, "A_quotas": Q,
       "B_wording_bin_kall": {"n_cells": len(B), "n_fail_raw": len(bad), "fail_examples": dict(list(bad.items())[:15]),
                              "feasible_rows_after_exact_balancing": keep, "target_rows": 3600,
                              "feasible": keep >= 3600, "note": "bins unscored (G9 not run)"}}
a_fail = [k for k, v in A.items() if not v.get("pass", True) and not v.get("report_only")]
q_fail = [k for k, v in Q.items() if not v["pass"]]
res["fails"] = {"A": a_fail, "quotas": q_fail, "B_raw_cells": len(bad), "B_feasible": keep >= 3600}
res["pass"] = not a_fail and not q_fail and keep >= 3600 and not bad
json.dump(res, open(L.QC / f"g10_{NAME}.json", "w"), indent=1)
print(json.dumps(res["fails"]), "pass", res["pass"])
