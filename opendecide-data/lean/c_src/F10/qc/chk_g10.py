"""G10 balance (independent F10 checker, check:F10, c-lanes-v3). C_DATA_SPEC v4 2.1 / 8 G10 + F10 G0 section 8.
Part A (pool-level, structural; gated): gold letter uniform per option bucket (chi-square over displayed positions,
expected = sum of 1/k per row; p > 0.01), "longest option is gold" within +/- 2 pp of mean 1/k (ties split), abstain
options gold at 1/k +/- 2 pp per bucket and wrong on >= 50% of the rows showing them, option buckets 35/35/15/15 +/- 3,
name modes on choice rows 40/30/30 +/- 2 (all, program, S7), S6 rows 10 +/- 1 %, S7 rows 30 +/- 1 % (each dataset
25 +/- 3 % of S7), open-world 20 +/- 3 % of S1-S4 cards, open-world choice rows k >= 3 and show 'cannot be
determined'-type option, deep <= 10 %, few-shot cards 5-10 %, inverted cards 10-15 %, short rows 15 +/- 2 % overall and
per sampler, consequence lines 50 +/- 5 % of program cards, per-card yes rate within 20-80 %, gold card position
uniform per bucket (program forward choice rows whose gold is a term; chi-square p > 0.01), syntactic negation >= 10 %
and double negation >= 2 % of yes/no rows, yes = bad outcome 50 +/- 5 % of yes/no rows (qc_sample sidecar; the
candidates sidecar has no polarity field), swapped rows: name-prior answer = gold 50 +/- 5 % (choice, yes/no).
Part B (after-selection cells; gated by feasibility): yes rate per wording x negation-count (k_all) cell (difficulty
bin pooled: G9 not run); pool values reported; an exactly balanced selection inside every cell must keep >= 1,620
yes/no rows (45 % of the 3,600 round-1 rows); F10 additions (per wording kind, name mode, world, sampler, S7 dataset,
uncorrelated features) reported on the pool and on a seeded simulated balanced selection.
v4 commit / ordinal / replay rules: not applicable to F10 (no commit, ordinal or replay rows). Usage: chk_g10.py <name>"""
import json, random, re, sys
from collections import Counter, defaultdict
from scipy.stats import chisquare, binomtest
import chk_lib as q

NAME = sys.argv[1] if len(sys.argv) > 1 else "candidates_r1"
rows, side = q.load(NAME)
S = lambda r: side.get(r["id"]) or {}
yn = [r for r in rows if q.is_yn(r)]; ch = [r for r in rows if not q.is_yn(r)]
P, out = {}, {"gate": "G10", "file": f"out/{NAME}.jsonl", "rows": len(rows), "yes_no": len(yn), "choice": len(ch)}
UNIT_RX = re.compile(r"(?i)(1 day = 24 hours|one week equals|multiply a value given in|convert \w+ to \w+|by 24 before|by 7 before)")
BK = ("2-4", "5-9", "10-19", "20-60")
TGT = {"2-4": .35, "5-9": .35, "10-19": .15, "20-60": .15}


def chi_pos(lst):
    """lst of (pos, k): chi-square of observed positions vs expected sum 1/k."""
    K = max(k for _, k in lst); obs = [0] * K; exp = [0.0] * K
    for p, k in lst:
        obs[p] += 1
        for j in range(k):
            exp[j] += 1 / k
    keep = [j for j in range(K) if exp[j] > 0]
    o = [obs[j] for j in keep]; e = [exp[j] for j in keep]; e = [x * sum(o) / sum(e) for x in e]
    return float(chisquare(o, e).pvalue) if len(o) > 1 else 1.0


# ---------------- Part A
A = {}
byb = defaultdict(list)
for r in ch:
    byb[q.bucket(len(r["options"]))].append(r)
gl = {}
for b in BK:
    L = byb.get(b, [])
    if L:
        p = chi_pos([(q.gold_index(r), len(r["options"])) for r in L])
        first = sum(q.gold_index(r) == 0 for r in L) / len(L)
        gl[b] = {"n": len(L), "chi2_p": p, "gold_first_share": round(first, 4),
                 "expected_first": round(sum(1 / len(r["options"]) for r in L) / len(L), 4), "pass": p > 0.01}
A["gold_letter_uniform"] = gl; P["A.gold_letter_uniform"] = all(v["pass"] for v in gl.values())
lg, ek = 0.0, 0.0
for r in ch:
    Ls = [len(o) for o in r["options"]]; mx = max(Ls); t = [i for i, x in enumerate(Ls) if x == mx]
    lg += (q.gold_index(r) in t) / len(t); ek += 1 / len(Ls)
A["longest_is_gold"] = {"rate": round(lg / len(ch), 4), "mean_1_over_k": round(ek / len(ch), 4)}
P["A.longest_is_gold"] = abs(lg - ek) / len(ch) <= 0.02
ab = {}
for b in BK:
    L = [r for r in byb.get(b, []) if any(q.is_abstain(r, o) for o in r["options"])]
    if not L:
        continue
    g = sum(q.is_abstain(r, r["gold"]) for r in L); e = sum(sum(q.is_abstain(r, o) for o in r["options"]) / len(r["options"]) for r in L)
    ab[b] = {"rows_showing": len(L), "gold_abstain": g, "expected": round(e, 1), "rate": round(g / len(L), 4),
             "exp_rate": round(e / len(L), 4), "wrong_share": round(1 - g / len(L), 4),
             "k_lt_3_showing": sum(len(r["options"]) < 3 for r in L)}
    ab[b]["pass"] = abs(g - e) / len(L) <= 0.02 and ab[b]["wrong_share"] >= 0.5 and ab[b]["k_lt_3_showing"] == 0
A["abstain"] = ab; P["A.abstain"] = all(v["pass"] for v in ab.values())
bs = {b: round(len(byb.get(b, [])) / len(ch), 4) for b in BK}
A["option_buckets"] = bs; P["A.option_buckets"] = all(abs(bs[b] - TGT[b]) <= 0.03 for b in BK)
nm = {}
for part, L in (("all", ch), ("program", [r for r in ch if r["meta"]["sampler"] != "S7"]), ("S7", [r for r in ch if r["meta"]["sampler"] == "S7"])):
    c = Counter(S(r).get("mode") for r in L); n = len(L)
    nm[part] = {"n": n, "neutral": round(c["neutral"] / n, 4), "swapped": round(c["swapped"] / n, 4),
                "other": round(1 - (c["neutral"] + c["swapped"]) / n, 4), "modes": dict(c)}
    nm[part]["pass"] = abs(nm[part]["neutral"] - .4) <= .02 and abs(nm[part]["swapped"] - .3) <= .02 and abs(nm[part]["other"] - .3) <= .02
A["name_modes_choice"] = nm; P["A.name_modes"] = all(v["pass"] for v in nm.values())
sm = Counter(r["meta"]["sampler"] for r in rows); n = len(rows)
s7 = [r for r in rows if r["meta"]["sampler"] == "S7"]
dsc = Counter((r["meta"].get("text_source") or {}).get("dataset") for r in s7)
A["shares"] = {"S6": round(sm["S6"] / n, 4), "S7": round(sm["S7"] / n, 4),
               "S7_datasets": {k: round(v / max(1, len(s7)), 4) for k, v in dsc.items()}, "samplers": dict(sm)}
P["A.S6_10pm1"] = abs(sm["S6"] / n - .10) <= .01
P["A.S7_30pm1"] = abs(sm["S7"] / n - .30) <= .01
P["A.S7_datasets_25pm3"] = all(abs(v / len(s7) - .25) <= .03 for v in dsc.values()) if s7 else False
cards = defaultdict(list)
for r in rows:
    cards[r["meta"]["card_id"]].append(r)
def cflag(c, k):
    v = [S(r).get(k) for r in cards[c]]; v = [x for x in v if x is not None]
    return Counter(v).most_common(1)[0][0] if v else None
prog = [c for c in cards if cards[c][0]["meta"]["sampler"] in ("S1", "S2", "S3", "S4")]
ow = sum(cflag(c, "world") == "open" for c in prog)
A["open_world_cards"] = {"S1_S4_cards": len(prog), "open": ow, "share": round(ow / max(1, len(prog)), 4)}
P["A.open_world_20pm3"] = abs(ow / max(1, len(prog)) - .2) <= .03
owc = [r for r in ch if S(r).get("world") == "open"]
bad = [r for r in owc if len(r["options"]) < 3 or not any(re.match(r"(?i)(the record does not settle it|not decidable|cannot be determined|undetermined)", o) for o in r["options"])]
omc = sum(bool(S(r).get("omitted")) for r in owc); owy = [r for r in yn if S(r).get("world") == "open"]; omy = sum(bool(S(r).get("omitted")) for r in owy)
A["open_world_rows"] = {"choice": len(owc), "choice_without_k3_or_cbd": len(bad), "choice_omitted_share": round(omc / max(1, len(owc)), 4),
                        "yes_no": len(owy), "yes_no_omitted_share": round(omy / max(1, len(owy)), 4)}
P["A.open_world_choice_k3_cbd"] = len(bad) == 0
P["A.open_world_omitted_choice_60pm5"] = abs(omc / max(1, len(owc)) - .6) <= .05
P["A.open_world_omitted_yn_50pm5"] = abs(omy / max(1, len(owy)) - .5) <= .05
dp = sum(bool(r["meta"].get("deep")) for r in rows) / n
nC = len(cards); few = sum(bool(cflag(c, "fewshot_card")) for c in cards); inv = sum(bool(cflag(c, "inverted_card")) for c in cards)
con = sum(bool(cflag(c, "conseq_visible")) for c in cards if cards[c][0]["meta"]["sampler"] not in ("S7",))
npc = sum(1 for c in cards if cards[c][0]["meta"]["sampler"] not in ("S7",))
sh = sum(bool(S(r).get("short")) for r in rows) / n
shs = {s: round(sum(bool(S(r).get("short")) for r in rows if r["meta"]["sampler"] == s) / sm[s], 4) for s in sm}
A["card_quotas"] = {"deep_share": round(dp, 4), "cards": nC, "fewshot_cards": round(few / nC, 4), "inverted_cards": round(inv / nC, 4),
                    "conseq_program_cards": round(con / max(1, npc), 4), "short_rows": round(sh, 4), "short_by_sampler": shs}
P["A.deep_le_10"] = dp <= .10
P["A.fewshot_5_10"] = .05 <= few / nC <= .10
P["A.inverted_10_15"] = .10 <= inv / nC <= .15
P["A.conseq_50pm5"] = abs(con / max(1, npc) - .5) <= .05
P["A.short_15pm2"] = abs(sh - .15) <= .02 and all(abs(v - .15) <= .02 for v in shs.values())
cy = defaultdict(lambda: [0, 0])
for r in yn:
    cy[r["meta"]["card_id"]][0] += 1; cy[r["meta"]["card_id"]][1] += r["gold"]
outc = {c: {"n": m, "yes": y, "rate": round(y / m, 3),
            "p_vs_bound": float(binomtest(y, m, .2 if y / m < .2 else .8).pvalue)} for c, (m, y) in cy.items() if not (.2 <= y / m <= .8)}
A["card_yes_rate"] = {"cards": len(cy), "outside_20_80": outc,
                      "rule": "the drawn per-card rate is U[20,80]; a card fails only if its observed rate is outside 20-80 and a "
                              "two-sided binomial test against the nearer bound gives p < 0.01 (small cards are noisy)"}
P["A.card_yes_20_80"] = all(v["p_vs_bound"] >= .01 for v in outc.values())
gp = {}
for b in BK:
    L = [(S(r).get("gold_pos"), S(r).get("n_terms_card")) for r in byb.get(b, []) if r["meta"]["sampler"] != "S7"
         and not S(r).get("inverted_card") and S(r).get("gold_kind") == "term" and isinstance(S(r).get("gold_pos"), int)
         and isinstance(S(r).get("n_terms_card"), int)]
    if len(L) > 10:
        gp[b] = {"n": len(L), "chi2_p": chi_pos(L)}; gp[b]["pass"] = gp[b]["chi2_p"] > 0.01
A["gold_card_position"] = gp or "n/a (sidecar has no gold_pos / n_terms_card)"
if gp:
    P["A.gold_card_position"] = all(v["pass"] for v in gp.values())
ng = sum((S(r).get("neg") or 0) >= 1 for r in yn) / len(yn); dn = sum((S(r).get("neg") or 0) >= 2 for r in yn) / len(yn)
A["negation"] = {"neg_ge1": round(ng, 4), "neg_ge2": round(dn, 4)}
P["A.negation_ge10"] = ng >= .10; P["A.double_neg_ge2"] = dn >= .02
yb = [S(r).get("yes_bad") for r in yn if S(r).get("yes_bad") is not None]
if yb:
    A["yes_bad"] = {"n": len(yb), "share": round(sum(yb) / len(yb), 4), "of_yes_no": len(yn)}
    P["A.yes_bad_50pm5"] = abs(sum(yb) / len(yb) - .5) <= .05 and len(yb) == len(yn)
else:
    A["yes_bad"] = "not in this file's sidecar (judged on qc_sample)"
npr = {}
for part, L in (("choice", ch), ("yes_no", yn)):
    v = [(S(r).get("name_prior"), r) for r in L if S(r).get("mode") == "swapped"]
    c = Counter(json.dumps(x) for x, _ in v)
    if part == "yes_no":  # yes/no name-prior answer is 1 (yes) / 0 (no): compare with gold
        d = [int(x == r["gold"]) for x, r in v if x in (0, 1)]
        npr[part] = {"swapped_rows": len(v), "values": dict(c), "decided": len(d), "prior_eq_gold": round(sum(d) / max(1, len(d)), 4)}
    else:  # choice: the sidecar stores a term id (t0..) with no visible name map -> not verifiable by the checker
        npr[part] = {"swapped_rows": len(v), "values": dict(c), "note": "report only: term ids cannot be mapped to options from visible data"}
A["name_prior_swapped"] = npr
P["A.name_prior_yes_no_50pm5"] = abs(npr["yes_no"]["prior_eq_gold"] - .5) <= .05
# recheck:F10 r1 fix (script gap vs spec 8 G10 "attack present uncorrelated with the label", not gated before):
# yes/no: attack-present x gold independence (Fisher 2x2 vs the other yes/no rows) and attack rows' yes rate vs 1/2, both
# p > 0.01; choice: gold letter uniform on attack rows (chi-square p > 0.01, when >= 20 rows). G0 7 (AR16): in-record
# labels / term mentions in attack text agree with gold on 50 +/- 5 % of the rows that carry one (sidecar attack.agrees).
from scipy.stats import fisher_exact  # noqa: E402
att_yn = [r for r in yn if S(r).get("attack")]; non_yn = [r for r in yn if not S(r).get("attack")]
att_ch = [r for r in ch if S(r).get("attack")]
ay = sum(int(r["gold"]) for r in att_yn); ny = sum(int(r["gold"]) for r in non_yn)
p_ind = float(fisher_exact([[ay, len(att_yn) - ay], [ny, len(non_yn) - ny]])[1]) if att_yn and non_yn else 1.0
p_half = float(binomtest(ay, len(att_yn), .5).pvalue) if att_yn else 1.0
agk = defaultdict(lambda: [0, 0])
for r in att_yn + att_ch:
    a = S(r)["attack"]
    if isinstance(a, dict) and a.get("agrees") is not None:
        agk[a.get("kind")][0] += 1; agk[a.get("kind")][1] += int(bool(a["agrees"]))
ag_n = sum(v[0] for v in agk.values()); ag_y = sum(v[1] for v in agk.values())
A["attack"] = {"yes_no_rows": len(att_yn), "yes_no_yes_rate": round(ay / max(1, len(att_yn)), 4),
               "other_yes_no_yes_rate": round(ny / max(1, len(non_yn)), 4), "fisher_p": round(p_ind, 5), "binom_half_p": round(p_half, 5),
               "choice_rows": len(att_ch), "label_agrees": {"rows": ag_n, "agree": ag_y, "share": round(ag_y / max(1, ag_n), 4),
               "by_kind": {k: {"rows": v[0], "agree": v[1], "share": round(v[1] / v[0], 4)} for k, v in sorted(agk.items(), key=str)}},
               "rule": "spec 8 G10 attack present uncorrelated with the label (pool independence p > 0.01; the +/- 2 pp after-selection "
                       "band is the selection's); G0 7 AR16 agree 50 +/- 5 % of the rows that carry a label or term mention"}
P["A.attack_uncorrelated_yes_no"] = p_ind > 0.01 and p_half > 0.01
if len(att_ch) >= 20:
    A["attack"]["choice_gold_letter_chi2_p"] = chi_pos([(q.gold_index(r), len(r["options"])) for r in att_ch])
    P["A.attack_uncorrelated_choice"] = A["attack"]["choice_gold_letter_chi2_p"] > 0.01
if ag_n:
    P["A.attack_label_agrees_50pm5"] = abs(ag_y / ag_n - .5) <= .05
out["A"] = A

# ---------------- Part B
def unit(r):
    return bool(UNIT_RX.search(q.full_text(r)))
FEATS = {"wkind": lambda r: S(r).get("wkind"), "mode": lambda r: S(r).get("mode"), "world": lambda r: S(r).get("world"),
         "sampler": lambda r: r["meta"]["sampler"], "s7_dataset": lambda r: (r["meta"].get("text_source") or {}).get("dataset"),
         "neg": lambda r: S(r).get("neg"), "lookalike": lambda r: S(r).get("lookalike"), "inert": lambda r: S(r).get("inert"),
         "attack": lambda r: bool(S(r).get("attack")), "threshold": lambda r: S(r).get("threshold"),
         "conseq_visible": lambda r: S(r).get("conseq_visible"), "override_word": lambda r: bool(S(r).get("override_words")),
         "omitted": lambda r: bool(S(r).get("omitted")), "unit_conversion": unit, "short": lambda r: S(r).get("short"),
         "layout": lambda r: S(r).get("layout")}
def rates(L):
    o = {}
    for f, fn in FEATS.items():
        d = defaultdict(lambda: [0, 0])
        for r in L:
            k = json.dumps(fn(r)); d[k][0] += 1; d[k][1] += r["gold"]
        o[f] = {k: {"n": m, "yes": round(y / m, 4), "p": round(binomtest(y, m, .5).pvalue, 5)} for k, (m, y) in d.items()}
    return o
cell = defaultdict(list)
for r in yn:
    cell[(r["meta"]["wording_id"], S(r).get("k_all"))].append(r)
dev = sorted(((abs(sum(x["gold"] for x in L) / len(L) - .5), len(L), f"{k[0]}|k_all={k[1]}") for k, L in cell.items()), reverse=True)
rng = random.Random(10010); sel = []
for k, L in sorted(cell.items(), key=lambda t: str(t[0])):
    y = [r for r in L if r["gold"] == 1]; nn = [r for r in L if r["gold"] == 0]; m = min(len(y), len(nn))
    sel += rng.sample(y, m) + rng.sample(nn, m)
B = {"cells": len(cell), "cells_outside_2pp_pool": sum(d > .02 for d, _, _ in dev), "worst_pool": [list(x) for x in dev[:5]],
     "balanced_selection_keeps": len(sel), "needed": 1620, "pool_yes_rate": round(sum(r["gold"] for r in yn) / len(yn), 4)}
pr = rates(yn); sr = rates(sel)
B["additions_pool_outside_2pp"] = {f: {k: v for k, v in d.items() if abs(v["yes"] - .5) > .02 and v["n"] >= 20} for f, d in pr.items()}
B["additions_simsel_outside_2pp"] = {f: {k: v for k, v in d.items() if abs(v["yes"] - .5) > .02 and v["n"] >= 20} for f, d in sr.items()}
B["additions_pool_sig_p01"] = sorted(f"{f}={k} n={v['n']} yes={v['yes']}" for f, d in pr.items() for k, v in d.items() if v["p"] < .01)
out["B"] = B
P["B.cells_feasible"] = len(sel) >= 1620
cl = {}
for b in BK:
    L = byb.get(b, [])
    for f in ("lookalike", "inert", "attack", "conseq_visible", "override_word", "unit_conversion", "threshold"):
        G = [r for r in L if FEATS[f](r)]
        if len(G) >= 20:
            cl[f"{b}|{f}"] = {"n": len(G), "chi2_p": chi_pos([(q.gold_index(r), len(r["options"])) for r in G])}
out["B"]["choice_feature_gold_letter_p"] = cl
out["pass_parts"] = P; out["failed"] = [k for k, v in P.items() if not v]; out["pass"] = all(P.values())
(q.QC / f"g10_{NAME}.json").write_text(json.dumps(out, indent=1, default=str))
print(json.dumps({"pass": out["pass"], "failed": out["failed"], "keep": len(sel)}))
