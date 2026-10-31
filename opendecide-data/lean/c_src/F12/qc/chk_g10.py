"""G10 balance (independent F12 checker, check:F12, c-lanes-v3; structure adapted from the F9 checker's chk_g10.py).
C_DATA_SPEC v4 2.1 / 8 G10 + F12 G0 section 8 ("Balance targets (G10)").
Part A (pool-level; gated):
 - yes/no share 45-55% of rows; per-card yes rate within 20-80% (cards with >= 10 yes/no rows);
 - "yes = bad outcome" (N framing, G0 8 framing table) 50 +/- 5% of yes/no rows;
 - syntactic negation (shared negcount k_syn on the question) >= 10% and double negation (k_syn >= 2) with an
   affirmative twin in its unit (same call_id, a row with lower k_syn) >= 2% of yes/no rows;
 - yes rate 50 +/- 3 per framing, form, sampler, attack flag, card mode (cells >= 100 rows; a cell fails when outside
   +/- 3 pp and binomial p <= 0.01);
 - gold letter uniform per option bucket (stored order; chi-square, expected sum 1/k; p > 0.01);
 - "longest option is gold" within +/- 2 pp of mean 1/k (ties split);
 - abstain options (C-TOOL None, C-PARAM Nothing, C-VALUE No usable value, C-DEFECT Nothing): wrong on >= 50% of the
   rows that show them (spec 2.1) and gold at 1/k +/- 2 pp per k bucket and kind (G0 8 XF01; a cell outside +/- 2 pp
   fails only if the two-sided binomial p <= 0.01);
 - C-ACT fixed options "Say it cannot be done" / "Answer directly from what is shown" (and their masked / swapped
   forms, via the option-definition lines): gold at 1/k +/- 2 pp per k bucket (G0 8 R3-SC2; same binomial rule);
 - attack present uncorrelated with the label (yes/no Fisher p > 0.01; choice: gold-is-abstain Fisher and gold
   relative position chi-square p > 0.01);
 - G0 8 max lexical overlap: "option with max word overlap (tool name vs latest request) is gold" (ties split) <=
   mean 1/k + 5 pp on C-TOOL and C-ACT rows;
 - G0 8 C-OUT outcome per sampler 25 +/- 3 (n >= 40 per sampler; binomial p <= 0.01 to fail);
 - option buckets 35/35/15/15 +/- 3 pp (2.1 quota);
 - masked 10-15% and swapped 4-6% of choice rows; deep <= 10%; label-flip twin sets 20-25% of rows; attack rows 3-7%;
   few-shot cards 5-10%; inverted cards 10-15% of cards (2.1 quotas; dev pool: reported only).
Part B (after-selection cells; gated by feasibility): yes rate per wording x k_all cell (difficulty bin pooled: G9 not
run); an exactly balanced selection inside every cell must keep >= 45% of the planned round-1 F12 rows (2,700) as
yes/no rows. v4 commit / ordinal / replay rules: not applicable to F12 (no commit, ordinal or replay rows).
Reported only: short / no card share (spec 8 ~15%; tmp/repair/SHORTCARD_NOTE.md asks for a ruling; gated in G11),
choice-form shares, S3 valid share. Usage: chk_g10.py <name>"""
import json, re, sys
from collections import Counter, defaultdict
from scipy.stats import chisquare, binomtest, fisher_exact, chi2_contingency
import chk_lib as q
from chk_g7 import opt_tool, overlap_max, request_text, tool_words, WRD
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


def attacked(r):
    return r.get("role") == "attacked" or r["meta"].get("twin_kind") == "T-ATTACK"


def qonly(r):
    return S(r).get("question") or q.qtext(r, S(r))


# ---------------- yes/no
sh = {"all": len(yn) / len(rows)}
for s in sorted({r["meta"]["sampler"] for r in rows}):
    rs = [r for r in rows if r["meta"]["sampler"] == s]; sh[s] = sum(q.is_yn(r) for r in rs) / len(rs)
out["yes_no_share"] = {k: round(v, 4) for k, v in sh.items()}
P["yn_share_45_55"] = 0.45 <= sh["all"] <= 0.55
out["yes_rate_all"] = rate(len(yn), sum(int(r["gold"]) for r in yn))
cy = defaultdict(lambda: [0, 0])
for r in yn:
    c = cy[r["meta"]["card_id"]]; c[0] += 1; c[1] += int(r["gold"])
cr = {c: v[1] / v[0] for c, v in cy.items() if v[0] >= 10}
out["card_yes_rate"] = {"cards_ge10": len(cr), "min": round(min(cr.values()), 3) if cr else None,
                        "max": round(max(cr.values()), 3) if cr else None,
                        "outside_20_80": sorted(c for c, v in cr.items() if not 0.2 <= v <= 0.8)}
P["card_yes_rate_20_80"] = not out["card_yes_rate"]["outside_20_80"]
fr = Counter(S(r).get("framing") for r in yn)
pb = fr.get("N", 0) / max(1, fr.get("N", 0) + fr.get("P", 0))
out["yes_is_bad_N_framing"] = {"counts": {str(k): v for k, v in fr.items()}, "share": round(pb, 4)}
P["yes_is_bad_45_55"] = 0.45 <= pb <= 0.55
ks = {r["id"]: negcount.k_syn(qonly(r)) for r in yn}
ka = {r["id"]: negcount.k_all(qonly(r)) for r in yn}
grp = defaultdict(list)
for r in yn:
    grp[r["call_id"]].append(r)
dneg_tw = sum(1 for r in yn if ks[r["id"]] >= 2 and any(o["id"] != r["id"] and ks[o["id"]] < ks[r["id"]] for o in grp[r["call_id"]]))
out["negation"] = {"k_syn_ge1": round(sum(v >= 1 for v in ks.values()) / len(yn), 4),
                   "k_syn_ge2": round(sum(v >= 2 for v in ks.values()) / len(yn), 4),
                   "k_syn_ge2_with_affirmative_twin": round(dneg_tw / len(yn), 4),
                   "k_all_dist": dict(Counter(ka.values())),
                   "side_neg_agree_k_syn": round(sum(ks[r["id"]] == S(r).get("neg") for r in yn) / len(yn), 4)}
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
ok &= cell("framing", lambda r: [str(S(r).get("framing"))])
ok &= cell("form", lambda r: [r["meta"]["subtype"]])
ok &= cell("sampler", lambda r: [r["meta"]["sampler"]])
ok &= cell("attack", lambda r: [str(attacked(r))])
ok &= cell("card_mode", lambda r: [str(S(r).get("card_mode"))])
out["yes_rate_cells_50pm3"] = cells; P["yes_rate_cells_50pm3"] = ok
cell("form_x_framing_report_only", lambda r: [r["meta"]["subtype"] + "|" + str(S(r).get("framing"))])
att = [[sum(int(r["gold"]) for r in yn if attacked(r) == a), sum(1 - int(r["gold"]) for r in yn if attacked(r) == a)]
       for a in (True, False)]
pa_yn = float(fisher_exact(att)[1]) if att[0][0] + att[0][1] else 1.0
# S3 valid share (report): Y-VALID / Y-CORRECT base truth = yes under P, no under N
vs = defaultdict(lambda: [0, 0])
for r in yn:
    if r["meta"]["subtype"] in ("Y-VALID", "Y-CORRECT"):
        f = S(r).get("framing"); g = int(r["gold"]); kneg = ks[r["id"]] % 2
        base = g if f == "P" else 1 - g
        base = base if kneg == 0 else 1 - base
        vs[r["meta"]["subtype"]][0] += 1; vs[r["meta"]["subtype"]][1] += base
out["s3_valid_share_report"] = {k: rate(*v) for k, v in vs.items()}

# ---------------- choice


def defs_kind(r, o):
    d = q.dio().card_defs(r.get("card"))
    t = (d.get(o) or "").lower()
    if o in q.ACT_FIXED:
        return q.ACT_FIXED[o]
    if t.startswith("say it cannot be done"):
        return "act_unable"
    if t.startswith("answer directly"):
        return "act_answer"
    return None


bk = defaultdict(list); lon = [0.0, 0.0]
for r in ch:
    k = len(r["options"]); gi = q.gold_index(r); bk[q.bucket(k)].append((gi, k))
    L = [len(o) for o in r["options"]]; top = [i for i, x in enumerate(L) if x == max(L)]
    lon[0] += (1 / len(top)) if gi in top else 0.0; lon[1] += 1 / k
out["gold_letter_chi_p"] = {b: round(chi_pos(v), 4) for b, v in bk.items()}
P["gold_letter_uniform"] = all(p > 0.01 for p in out["gold_letter_chi_p"].values())
out["longest_gold"] = {"rate": rate(len(ch), lon[0]), "expected_mean_1_over_k": rate(len(ch), lon[1])}
P["longest_gold_pm2"] = abs(lon[0] - lon[1]) / len(ch) <= 0.02


def kind_cells(kfun):
    ab = defaultdict(lambda: [0, 0, 0.0])
    for r in ch:
        k = len(r["options"]); kinds = {kfun(r, o) for o in r["options"]} - {None}
        gk = kfun(r, r["gold"])
        for kd in kinds:
            for key in ((q.bucket(k), kd), ("all", kd)):
                e = ab[key]; e[0] += 1; e[1] += int(gk == kd); e[2] += 1 / k
    res, bad = {}, []
    for key, (n, x, e) in sorted(ab.items()):
        p = float(binomtest(x, n, e / n).pvalue) if n else 1.0
        good = abs(x - e) / n <= 0.02 or p > 0.01
        res["/".join(key)] = {"n": n, "gold": x, "rate": rate(n, x), "expected_1_over_k": rate(n, e), "binom_p": round(p, 8), "ok": good}
        if not good:
            bad.append("/".join(key))
    return res, bad


abres, abad = kind_cells(lambda r, o: q.abstain_kind(o))
aball = [sum(1 for r in ch if any(q.abstain_kind(o) for o in r["options"])), sum(1 for r in ch if q.abstain_kind(r["gold"]))]
out["abstain"] = {"rows_showing": aball[0], "abstain_gold": aball[1], "per_bucket_kind": abres, "bad_bucket_kind": abad}
P["abstain_wrong_ge50"] = all(v["rate"] <= 0.5 for v in abres.values())
P["abstain_gold_1_over_k"] = not abad
actres, actbad = kind_cells(lambda r, o: defs_kind(r, o) if r["meta"]["subtype"] == "C-ACT" else None)
out["c_act_fixed_options"] = {"per_bucket_kind": actres, "bad_bucket_kind": actbad}
P["c_act_fixed_options_1_over_k"] = not actbad
# attack
ga = [[0, 0], [0, 0]]; pos = defaultdict(lambda: [0, 0, 0, 0])
for r in ch:
    a = int(attacked(r)); gk = q.abstain_kind(r["gold"]) is not None
    ga[a][int(gk)] += 1
    k = len(r["options"]); pos[a][min(3, int(4 * q.gold_index(r) / k))] += 1
pa_ab = float(fisher_exact(ga)[1]) if ga[1][0] + ga[1][1] else 1.0
tab = [pos[0], pos[1]] if sum(pos[1]) else None
pa_pos = float(chi2_contingency([[x + 0.5 for x in t] for t in tab])[1]) if tab else 1.0
out["attack"] = {"yes_no_fisher_p": round(pa_yn, 4), "yes_no_yes_rate_attacked": rate(sum(att[0]), att[0][0]),
                 "choice_gold_abstain_fisher_p": round(pa_ab, 4), "choice_gold_relpos_chi_p": round(pa_pos, 4),
                 "attacked_rows": sum(attacked(r) for r in rows), "attack_def": "role attacked or meta.twin_kind T-ATTACK"}
P["attack_uncorrelated"] = pa_yn > 0.01 and pa_ab > 0.01 and pa_pos > 0.01
# G0 8 max lexical overlap
mo = defaultdict(lambda: [0, 0.0, 0.0])
for r in ch:
    if r["meta"]["subtype"] not in ("C-TOOL", "C-ACT"):
        continue
    s = S(r); names = {t["name"] for t in (s.get("S") or {}).get("tools") or []}
    req = set(WRD.findall(request_text(s).lower())); k = len(r["options"]); gi = q.gold_index(r)
    sc = [len(tool_words(t) & req) if t else -1 for t in (opt_tool(o, names) for o in r["options"])]
    if max(sc) <= 0:
        continue
    top = [i for i, v in enumerate(sc) if v == max(sc)]
    for key in (r["meta"]["subtype"], "all"):
        e = mo[key]; e[0] += 1; e[1] += (1 / len(top)) if gi in top else 0.0; e[2] += 1 / k
out["max_overlap_gold"] = {k: {"rows": n, "rate_ties_split": rate(n, x), "mean_1_over_k": rate(n, e), "excess_pp": round(100 * (x - e) / n, 2)}
                           for k, (n, x, e) in mo.items()}
P["max_overlap_gold_le_1k_plus5"] = all((x - e) / n <= 0.05 for n, x, e in mo.values() if n >= 30)
# G0 8 C-OUT outcome per sampler 25 +/- 3
co = defaultdict(Counter)
for r in ch:
    if r["meta"]["subtype"] == "C-OUT":
        co[r["meta"]["sampler"]][S(r).get("outcome")] += 1
cores, cobad = {}, []
for smp, c in co.items():
    n = sum(c.values())
    for oc in ("CALL", "ASK", "UNABLE", "ANSWER"):
        x = c.get(oc, 0); p = float(binomtest(x, n, 0.25).pvalue) if n else 1.0
        cores[f"{smp}/{oc}"] = {"n": n, "rate": rate(n, x), "binom_p": round(p, 5)}
        if n >= 40 and abs(x / n - 0.25) > 0.03 and p <= 0.01:
            cobad.append(f"{smp}/{oc}")
out["c_out_outcome_per_sampler"] = {"cells": cores, "bad": cobad}
P["c_out_outcome_25pm3"] = not cobad
# quotas
bc = Counter(q.bucket(len(r["options"])) for r in ch)
out["option_buckets"] = {b: rate(len(ch), bc[b]) for b in BK}
TG = {"2-4": .35, "5-9": .35, "10-19": .15, "20-60": .15}
if not DEV:
    P["option_buckets_35_35_15_15_pm3"] = all(abs(bc[b] / len(ch) - TG[b]) <= 0.03 for b in BK)
sch = Counter(((S(r).get("names") or {}).get("scheme") if isinstance(S(r).get("names"), dict) else None) for r in ch
              if r["meta"]["subtype"] in ("C-OUT", "C-ACT"))  # names are masked / swapped on C-OUT and C-ACT options only (G0 8)
msk = sum(v for k, v in sch.items() if k and k != "swap") / len(ch); swp = sch.get("swap", 0) / len(ch)
deep = sum(bool(r["meta"].get("deep")) for r in rows) / len(rows)
FLIP = {"T-REMOVE-VALUE", "T-REMOVE-TOOL", "T-NEAR-MISS-SWAP", "T-BOUNDARY", "T-DEFECT-FIX", "T-STALE", "T-CORRECTION",
        "T-ROLE", "T-TIE", "T-KIND"}
ids = {r["id"] for r in rows}; tw = set()
for r in rows:
    if r["meta"].get("twin_kind") in FLIP:
        tw.add(r["id"])
        if r["meta"].get("twin_of") in ids:
            tw.add(r["meta"]["twin_of"])
twin = len(tw) / len(rows)
attk = sum(attacked(r) for r in rows) / len(rows)
cards = defaultdict(list)
for r in rows:
    cards[r["meta"]["card_id"]].append(r)
WK = re.compile(r"(?i)worked examples?")
few = sum(any(WK.search((r.get("card") or "") + r["instructions"]) for r in v) for v in cards.values()) / len(cards)
inv = sum(any(r["meta"]["subtype"] == "C-INV" for r in v) for v in cards.values()) / len(cards)
shortc = sum(r["meta"]["defs_style"] in ("short", "no_card") for r in rows) / len(rows)
out["quotas"] = {"masked_choice": round(msk, 4), "swapped_choice": round(swp, 4), "masked_swapped_def": "C-OUT / C-ACT rows on masked / swapped cards, share of all choice rows", "deep": round(deep, 4),
                 "label_flip_twin_set_rows": round(twin, 4), "attack_rows": round(attk, 4),
                 "fewshot_cards": round(few, 4), "inverted_cards": round(inv, 4), "short_or_no_card_rows_report": round(shortc, 4),
                 "twin_kinds": dict(Counter(str(r["meta"].get("twin_kind")) for r in rows)),
                 "choice_form_shares_report": {k: rate(len(ch), v) for k, v in Counter(r["meta"]["subtype"] for r in ch).items()}}
if not DEV:
    P["masked_10_15"] = 0.10 <= msk <= 0.15
    P["swapped_4_6"] = 0.04 <= swp <= 0.06
    P["deep_le10"] = deep <= 0.10
    P["twins_20_25"] = 0.20 <= twin <= 0.25
    P["attack_3_7"] = 0.03 <= attk <= 0.07
    P["fewshot_cards_5_10"] = 0.05 <= few <= 0.10
    P["inverted_cards_10_15"] = 0.10 <= inv <= 0.15
# ---------------- Part B: wording x k_all cells (bin pooled)
wc = defaultdict(lambda: [0, 0])
for r in yn:
    c = wc[(r["meta"]["wording_id"], ka[r["id"]])]; c[0] += 1; c[1] += int(r["gold"])
dev = {f"{w}|k{k}": {"n": n, "yes": rate(n, y)} for (w, k), (n, y) in wc.items()}
keep = sum(2 * min(y, n - y) for n, y in wc.values())
out["partB_wording_x_kall"] = {"n_cells": len(wc), "cells_outside_50pm2_n_ge50": sorted(k for k, v in dev.items() if v["n"] >= 50 and abs(v["yes"] - .5) > .02),
                               "balanced_selection_keeps_yes_no_rows": keep, "of_yes_no_rows": len(yn),
                               "max_abs_dev_n_ge50": max([abs(v["yes"] - .5) for v in dev.values() if v["n"] >= 50] or [0])}
if NAME == "candidates_r1":  # round-1 F12 target 2,700 rows; 45% yes/no
    out["partB_wording_x_kall"]["required"] = 1215
    P["partB_feasible"] = keep >= 1215
out["pass_parts"] = P
out["pass"] = all(P.values())
(q.QC / f"g10_{NAME}.json").write_text(json.dumps(out, indent=1, default=str))
print(json.dumps({"pass": out["pass"], "fails": [k for k, v in P.items() if not v]}))
