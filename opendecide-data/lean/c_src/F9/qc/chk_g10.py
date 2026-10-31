"""G10 balance (independent F9 checker, check:F9, c-lanes-v3). C_DATA_SPEC v4 2.1 / 8 G10 + F9 G0 section 5.
Part A (pool-level; gated):
 - yes/no share 45-55% of rows and 40-60% per sampler; per-card yes rate within 20-80%;
 - "yes = bad outcome" 50 +/- 5% of yes/no rows (side polarity_bad);
 - syntactic negation (shared negcount k_syn on the question) >= 10% and double negation (k_syn >= 2) with an
   affirmative twin (its unit, same call_id, holds the affirmative base row: twin_kind None, lower k_syn) >= 2% of yes/no rows;
 - yes rate 50 +/- 3 per container, sampler, subtype, live edge flag and on the no-card slice (cells >= 100 rows; a
   cell fails when outside +/- 3 pp and binomial p <= 0.01, since these cells are not generator-held);
 - gold letter uniform per option bucket (stored order; chi-square, expected sum 1/k; p > 0.01);
 - "longest option is gold" within +/- 2 pp of mean 1/k (ties split);
 - numeric options: P(gold is max or min) = 2/k +/- 2 pp (ties split) and gold value rank uniform (chi-square p > 0.01);
 - record-set picks: "gold = option with the smallest total set distance to the others" at 1/k +/- 2 pp (F9-A35);
 - abstain options: wrong on >= 50% of the rows that show them (spec 2.1) and gold at 1/k +/- 2 pp per k bucket and
   per abstain kind on the rows that show them (XF01; the gold slot is drawn at random, so a cell outside +/- 2 pp
   fails only if the two-sided binomial p <= 0.01), and per answer form (every form showing an abstain kind on >= 30 rows must have it gold at
   binomial p > 0.01);
 - attack present uncorrelated with the label (yes/no Fisher p > 0.01; choice: gold-is-abstain and gold relative
   position chi-square p > 0.01);
 - option buckets 35/35/15/15 +/- 3 pp (2.1 quota; F9 G0 5 claims no tolerance band, the F10 checker's +/- 3 used);
 - masked 10-15% and swapped 5 +/- 1% of choice rows; deep <= 10%; short / no card ~15% (10-20%); label-flip twin
   sets (fact-flip and premise-removal twins with their bases, G0 1.7 / XF03) 20-25% of rows; attack rows about 5% (3-7%); few-shot cards 5-10% and inverted cards 10-15% of cards;
 - decisive position uniform over deciles (side decile; chi-square p > 0.01).
Part B (after-selection cells; gated by feasibility): yes rate per wording x k_all cell (difficulty bin pooled: G9
not run); pool values reported; an exactly balanced selection inside every cell must keep >= 45% of the planned
round-1 F9 rows as yes/no rows.
v4 commit / ordinal / replay rules: not applicable to F9 (no commit, ordinal or replay rows; G0 1.3: no ordinal rows).
Usage: chk_g10.py <name>"""
import json, sys
from collections import Counter, defaultdict
from scipy.stats import chisquare, binomtest, fisher_exact, chi2_contingency
import chk_lib as q
sys.path.insert(0, str(q.LEAN / "c_src/common"))
import negcount  # noqa: E402

NAME = sys.argv[1] if len(sys.argv) > 1 else "candidates_r1"
rows, side = q.load(NAME)
S = lambda r: side.get(r["id"]) or {}
yn = [r for r in rows if q.is_yn(r)]; ch = [r for r in rows if not q.is_yn(r)]
P, out = {}, {"gate": "G10", "file": f"out/{NAME}.jsonl", "pool_sha256": q.sha(q.OUT / f"{NAME}.jsonl"), "rows": len(rows),
              "yes_no": len(yn), "choice": len(ch)}
BK = ("2-4", "5-9", "10-19", "20-60")
DEV = NAME == "mixdev_S5"


def chi_pos(lst):
    K = max(k for _, k in lst); obs = [0] * K; exp = [0.0] * K
    for p, k in lst:
        obs[p] += 1
        for j in range(k):
            exp[j] += 1 / k
    keep = [j for j in range(K) if exp[j] > 0]
    o = [obs[j] for j in keep]; e = [exp[j] for j in keep]; e = [x * sum(o) / sum(e) for x in e]
    return float(chisquare(o, e).pvalue)


def rate(n, x):
    return round(x / n, 4) if n else None


# ---------------- yes/no
yr = sum(int(r["gold"]) for r in yn) / max(1, len(yn))
sh = {"all": len(yn) / len(rows)}
for s in sorted({r["meta"]["sampler"] for r in rows}):
    rs = [r for r in rows if r["meta"]["sampler"] == s]; sh[s] = sum(q.is_yn(r) for r in rs) / len(rs)
out["yes_no_share"] = {k: round(v, 4) for k, v in sh.items()}
P["yn_share_45_55"] = 0.45 <= sh["all"] <= 0.55 and all(0.40 <= v <= 0.60 for k, v in sh.items() if k != "all")
cy = defaultdict(lambda: [0, 0])
for r in yn:
    c = cy[r["meta"]["card_id"]]; c[0] += 1; c[1] += int(r["gold"])
cr = {c: v[1] / v[0] for c, v in cy.items() if v[0] >= 10}
out["card_yes_rate"] = {"cards_ge10": len(cr), "min": round(min(cr.values()), 3), "max": round(max(cr.values()), 3),
                        "outside_20_80": sorted(c for c, v in cr.items() if not 0.2 <= v <= 0.8)}
P["card_yes_rate_20_80"] = not out["card_yes_rate"]["outside_20_80"]
pol = Counter(S(r).get("polarity_bad") for r in yn)
pb = pol.get("yes", 0) / max(1, pol.get("yes", 0) + pol.get("no", 0))
out["yes_is_bad"] = {"counts": {str(k): v for k, v in pol.items()}, "share": round(pb, 4)}
P["yes_is_bad_45_55"] = 0.45 <= pb <= 0.55
ks = {r["id"]: negcount.k_syn(q.qtext(r, S(r))) for r in yn}
ka = {r["id"]: negcount.k_all(q.qtext(r, S(r))) for r in yn}
grp = defaultdict(list)
for r in yn:
    grp[r["call_id"]].append(r)
dneg_tw = sum(1 for r in yn if ks[r["id"]] >= 2 and any(o["id"] != r["id"] and o["meta"].get("twin_kind") is None and
                                                         ks[o["id"]] < ks[r["id"]] for o in grp[r["call_id"]]))
out["negation"] = {"k_syn_ge1": round(sum(v >= 1 for v in ks.values()) / len(yn), 4),
                   "k_syn_ge2": round(sum(v >= 2 for v in ks.values()) / len(yn), 4),
                   "k_syn_ge2_with_affirmative_twin": round(dneg_tw / len(yn), 4),
                   "k_all_dist": dict(Counter(ka.values())),
                   "side_k_syn_agree": round(sum(ks[r["id"]] == S(r).get("k_syn") for r in yn) / len(yn), 4),
                   "side_k_all_agree": round(sum(ka[r["id"]] == S(r).get("k_all") for r in yn) / len(yn), 4)}
if not DEV:
    P["neg_ge10"] = out["negation"]["k_syn_ge1"] >= 0.10
    P["dneg_twin_ge2"] = out["negation"]["k_syn_ge2_with_affirmative_twin"] >= 0.02
cells = {}
def cell(name, key):
    c = defaultdict(lambda: [0, 0])
    for r in yn:
        for kk in key(r):
            c[kk][0] += 1; c[kk][1] += int(r["gold"])
    res = {str(k): {"n": v[0], "yes": rate(*v)} for k, v in c.items()}
    for k, v in res.items():
        v["binom_p"] = round(float(binomtest(round(v["yes"] * v["n"]), v["n"], 0.5).pvalue), 5)
    bad = [k for k, v in res.items() if v["n"] >= 100 and abs(v["yes"] - 0.5) > 0.03 and v["binom_p"] <= 0.01]
    cells[name] = {"cells": res, "bad_ge100": bad}
    return not bad
ok = True
ok &= cell("container", lambda r: [str(S(r).get("container"))])
ok &= cell("sampler", lambda r: [r["meta"]["sampler"]])
ok &= cell("subtype", lambda r: [r["meta"]["subtype"]])
ok &= cell("edge_flag", lambda r: list(r["meta"].get("edge") or []))
ok &= cell("no_card", lambda r: ["no_card"] if not (r.get("card") or "").strip() else [])
ok &= cell("attack", lambda r: [str(r.get("role") == "attacked")])
out["yes_rate_cells_50pm3"] = cells; P["yes_rate_cells_50pm3"] = ok
att = [[sum(int(r["gold"]) for r in yn if r.get("role") == a), sum(1 - int(r["gold"]) for r in yn if r.get("role") == a)]
       for a in ("attacked", "own")]
pa_yn = float(fisher_exact(att)[1]) if att[0][0] + att[0][1] else 1.0

# ---------------- choice
bk = defaultdict(list); lon = [0.0, 0.0]; mm = [0.0, 0.0, 0]; rk = []; cen = [0.0, 0.0, 0]
for r in ch:
    k = len(r["options"]); gi = q.gold_index(r); bk[q.bucket(k)].append((gi, k))
    L = [len(o) for o in r["options"]]; top = [i for i, x in enumerate(L) if x == max(L)]
    lon[0] += (1 / len(top)) if gi in top else 0.0; lon[1] += 1 / k
    nums = [q.as_num(o) for o in r["options"]]; idx = [i for i, x in enumerate(nums) if x is not None]
    if len(idx) >= 3 and gi in idx:
        vals = sorted(set(nums[i] for i in idx)); g = nums[gi]
        mm[0] += int(g in (vals[0], vals[-1])); mm[1] += min(1.0, 2 / len(vals)); mm[2] += 1
        if len(vals) == len(idx):
            rk.append((vals.index(g), len(vals)))
    sets = [q.set_ids(o) for o in r["options"]]
    if sum(x is not None for x in sets) >= 2:
        sets = [frozenset() if (x is None and q.abstain_kind(o) == "no_record") else x for x, o in zip(sets, r["options"])]
        sv = [i for i, x in enumerate(sets) if x is not None]
        if len(sv) >= 3 and gi in sv:
            dist = {i: sum(len(sets[i] ^ sets[j]) for j in sv) for i in sv}; m = min(dist.values())
            tops = [i for i in sv if dist[i] == m]
            cen[0] += (1 / len(tops)) if gi in tops else 0.0; cen[1] += 1 / k; cen[2] += 1
out["gold_letter_chi_p"] = {b: round(chi_pos(v), 4) for b, v in bk.items()}
P["gold_letter_uniform"] = all(p > 0.01 for p in out["gold_letter_chi_p"].values())
out["longest_gold"] = {"rate": rate(len(ch), lon[0]), "expected_mean_1_over_k": rate(len(ch), lon[1])}
P["longest_gold_pm2"] = abs(lon[0] - lon[1]) / len(ch) <= 0.02
out["numeric_options"] = {"rows": mm[2], "gold_max_or_min": rate(mm[2], mm[0]), "expected": rate(mm[2], mm[1]),
                          "rank_rows": len(rk), "rank_chi_p": round(chi_pos(rk), 6) if rk else None}
P["numeric_maxmin_pm2"] = mm[2] == 0 or abs(mm[0] - mm[1]) / mm[2] <= 0.02
P["numeric_rank_uniform"] = not rk or chi_pos(rk) > 0.01
out["set_centre"] = {"rows": cen[2], "gold_is_centre": rate(cen[2], cen[0]), "expected_1_over_k": rate(cen[2], cen[1])}
P["set_centre_pm2"] = cen[2] == 0 or abs(cen[0] - cen[1]) / cen[2] <= 0.02
# abstain
ab = defaultdict(lambda: [0, 0, 0.0]); abf = defaultdict(lambda: [0, 0, 0.0]); aball = [0, 0]
for r in ch:
    k = len(r["options"]); kinds = {q.abstain_kind(o) for o in r["options"]} - {None}
    if not kinds:
        continue
    gk = q.abstain_kind(r["gold"]); aball[0] += 1; aball[1] += int(gk is not None)
    for kd in kinds:
        for key in ((q.bucket(k), kd), ("all", kd)):
            e = ab[key]; e[0] += 1; e[1] += int(gk == kd); e[2] += 1 / k
        e = abf[(S(r).get("form"), kd)]; e[0] += 1; e[1] += int(gk == kd); e[2] += 1 / k
abres, abad = {}, []
for key, (n, x, e) in sorted(ab.items()):
    p = float(binomtest(x, n, e / n).pvalue) if n else 1.0
    good = abs(x - e) / n <= 0.02 or p > 0.01
    abres["/".join(key)] = {"n": n, "gold": x, "rate": rate(n, x), "expected_1_over_k": rate(n, e), "binom_p": round(p, 6), "ok": good}
    if not good:
        abad.append("/".join(key))
fres, fbad = {}, []
for key, (n, x, e) in sorted(abf.items(), key=str):
    p = float(binomtest(x, n, e / n).pvalue) if n else 1.0
    fres[f"{key[0]}/{key[1]}"] = {"n": n, "gold": x, "expected": round(e, 1), "binom_p": round(p, 6)}
    if n >= 30 and p <= 0.01:
        fbad.append(f"{key[0]}/{key[1]}")
out["abstain"] = {"rows_showing": aball[0], "abstain_gold_share_of_those": rate(*aball), "per_bucket_kind": abres,
                  "per_form_kind": fres, "bad_bucket_kind": abad, "bad_form_kind": fbad}
P["abstain_wrong_ge50"] = all(v["rate"] <= 0.5 for v in abres.values())
P["abstain_gold_1_over_k"] = not abad and not fbad
# attack
ga = [[0, 0], [0, 0]]; pos = defaultdict(lambda: [0, 0, 0, 0])
for r in ch:
    a = int(r.get("role") == "attacked"); gk = q.abstain_kind(r["gold"]) is not None
    ga[a][int(gk)] += 1
    k = len(r["options"]); pos[a][min(3, int(4 * q.gold_index(r) / k))] += 1
pa_ab = float(fisher_exact(ga)[1]) if ga[1][0] + ga[1][1] else 1.0
tab = [pos[0], pos[1]] if sum(pos[1]) else None
pa_pos = float(chi2_contingency([[x + 0.5 for x in t] for t in tab])[1]) if tab else 1.0
out["attack"] = {"yes_no_fisher_p": round(pa_yn, 4), "yes_no_yes_rate_attacked": rate(sum(att[0]), att[0][0]),
                 "choice_gold_abstain_fisher_p": round(pa_ab, 4), "choice_gold_relpos_chi_p": round(pa_pos, 4),
                 "attacked_rows": sum(r.get("role") == "attacked" for r in rows)}
P["attack_uncorrelated"] = pa_yn > 0.01 and pa_ab > 0.01 and pa_pos > 0.01
# quotas
bc = Counter(q.bucket(len(r["options"])) for r in ch)
out["option_buckets"] = {b: rate(len(ch), bc[b]) for b in BK}
TG = {"2-4": .35, "5-9": .35, "10-19": .15, "20-60": .15}
if not DEV:
    P["option_buckets_35_35_15_15_pm3"] = all(abs(bc[b] / len(ch) - TG[b]) <= 0.03 for b in BK)
msk = sum(bool(S(r).get("masked")) for r in ch) / len(ch); swp = sum(bool(S(r).get("swapped")) for r in ch) / len(ch)
deep = sum(bool(r["meta"].get("deep")) for r in rows) / len(rows)
shortc = sum(r["meta"]["defs_style"] in ("short", "none") for r in rows) / len(rows)
ids = {r["id"] for r in rows}; tw = set()
for r in rows:
    if r["meta"].get("twin_kind") in ("fact_flip", "premise_removal"):
        tw.add(r["id"])
        if r["meta"].get("twin_of") in ids:
            tw.add(r["meta"]["twin_of"])
twin = len(tw) / len(rows)
attk = sum(r.get("role") == "attacked" for r in rows) / len(rows)
cards = defaultdict(list)
for r in rows:
    cards[r["meta"]["card_id"]].append(r)
few = sum(any(S(r).get("fewshot_card") for r in v) for v in cards.values()) / len(cards)
inv = sum(any(S(r).get("inverted") for r in v) for v in cards.values()) / len(cards)
out["quotas"] = {"masked_choice": round(msk, 4), "swapped_choice": round(swp, 4), "deep": round(deep, 4),
                 "short_or_no_card": round(shortc, 4), "label_flip_twin_set_rows": round(twin, 4), "attack_rows": round(attk, 4),
                 "fewshot_cards": round(few, 4), "inverted_cards": round(inv, 4),
                 "twin_kinds": dict(Counter(str(r["meta"].get("twin_kind")) for r in rows))}
if not DEV:
    P["masked_10_15"] = 0.10 <= msk <= 0.15
    P["swapped_4_6"] = 0.04 <= swp <= 0.06
    P["deep_le10"] = deep <= 0.10
    P["short_card_10_20"] = 0.10 <= shortc <= 0.20
    P["twins_20_25"] = 0.20 <= twin <= 0.25
    P["attack_3_7"] = 0.03 <= attk <= 0.07
    P["fewshot_cards_5_10"] = 0.05 <= few <= 0.10
    P["inverted_cards_10_15"] = 0.10 <= inv <= 0.15
dec = Counter(S(r).get("decile") for r in rows if isinstance(S(r).get("decile"), int))
if sum(dec.values()) >= 50:
    obs = [dec.get(i, 0) for i in range(10)]
    out["decile"] = {"counts": obs, "chi_p": round(float(chisquare(obs).pvalue), 4)}
    P["decile_uniform"] = out["decile"]["chi_p"] > 0.01
# ---------------- Part B: wording x k_all cells (bin pooled)
wc = defaultdict(lambda: [0, 0])
for r in yn:
    c = wc[(r["meta"]["wording_id"], ka[r["id"]])]; c[0] += 1; c[1] += int(r["gold"])
dev = {f"{w}|k{k}": {"n": n, "yes": rate(n, y)} for (w, k), (n, y) in wc.items()}
keep = sum(2 * min(y, n - y) for n, y in wc.values())
out["partB_wording_x_kall"] = {"n_cells": len(wc), "cells_outside_50pm2_n_ge50": sorted(k for k, v in dev.items() if v["n"] >= 50 and abs(v["yes"] - .5) > .02),
                               "balanced_selection_keeps_yes_no_rows": keep, "of_yes_no_rows": len(yn),
                               "max_abs_dev_n_ge50": max([abs(v["yes"] - .5) for v in dev.values() if v["n"] >= 50] or [0])}
if NAME == "candidates_r1":  # round-1 F9 target 4,050 rows (G0 0: S1 900, S2 900, S3 750, S4 750, S6 750); 45% yes/no
    out["partB_wording_x_kall"]["required"] = 1823
    P["partB_feasible"] = keep >= 1823
out["pass_parts"] = P
out["pass"] = all(P.values())
(q.QC / f"g10_{NAME}.json").write_text(json.dumps(out, indent=1, default=str))
print(json.dumps({"pass": out["pass"], "fails": [k for k, v in P.items() if not v]}))
