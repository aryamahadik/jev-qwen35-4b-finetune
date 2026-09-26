#!/usr/bin/env python3
"""Size, budget and power calculator for proposal_rigor.md (OpenDecide dataset spec).

Every number in the size/power tables of proposal_rigor.md is produced by this file, so the
tables can be regenerated whenever a size changes. Pure python + numpy/scipy; no network.

    python3 proposal_rigor_plan.py            # prints tables
    python3 proposal_rigor_plan.py --json out.json
"""
from __future__ import annotations
import argparse, json, math
import numpy as np
from scipy import stats

SEED = 20260925

# ----------------------------------------------------------------------------------------------
# 1. Row recipes: expected rows per clean state, and the relations / decisions they create.
#    Fractions are realised deterministically by the build (item rank mod k), not by coin flips.
# ----------------------------------------------------------------------------------------------
# keys: rows=question rows per state; noul/choice/score = decision rows by type;
# rel = relation counts per state (type -> expected count); tmpl_comp = template complement pairs
RECIPES = {
    # single-label Choice sources (intent, topic, finance, HINT3)
    "SL":      dict(rows=4.5,  noul=3.25, choice=1.25, score=0, rel=dict(complement_tmpl=1, para=1, dneg=.25, choice_noul=1, choice2_noul=.25, choice2_order=.25)),
    "SL_hier": dict(rows=5.5,  noul=4.25, choice=1.25, score=0, rel=dict(complement_tmpl=1, para=1, dneg=.25, choice_noul=1, choice2_noul=.25, choice2_order=.25, monotone=1)),
    "SL_clinc": dict(rows=6.5,  noul=4.25, choice=2.25, score=0, rel=dict(complement_tmpl=1, para=1, dneg=.25, choice_noul=1, choice2_noul=.25, choice2_order=.25, monotone=1, largeK_choice_noul=1)),
    "SL_tfns": dict(rows=5.5,  noul=4.25, choice=1.25, score=0, rel=dict(complement_tmpl=1, para=1, dneg=.25, choice_noul=1, choice2_noul=.25, choice2_order=.25, contrary=1)),
    # multi-label (NLU++): 3 module Nouls, neg, para, dneg, conjunction, numeric/date slot question
    "ML":      dict(rows=6.75, noul=6.75, choice=0, score=0, rel=dict(complement_tmpl=1, para=1, dneg=.25, conjunction=1)),
    # Score sources
    "SC":          dict(rows=4.5, noul=2.5, choice=0,  score=2, rel=dict(complement_tmpl=1, para=.5, score_rev=1, threshold_tail=1)),
    "SC_clothing": dict(rows=6.2, noul=3.5, choice=.7, score=2, rel=dict(complement_tmpl=1, para=.5, score_rev=1, threshold_tail=1, human_floor=1)),
    "SC_drug":     dict(rows=5.5, noul=2.5, choice=0,  score=3, rel=dict(complement_tmpl=1, para=.5, score_rev=1, threshold_tail=1, rebin=1)),
    "SC_sst":      dict(rows=5.5, noul=3.5, choice=0,  score=2, rel=dict(complement_tmpl=1, para=.5, score_rev=1, threshold_tail=1, contrary=1)),
    # proposition sources
    "PR_boolq":   dict(rows=6.1,  noul=5.6,  choice=.5, score=0, rel=dict(complement_tmpl=1, para=.5, human_complement=.5, human_para=.6, human_perturb=2, choice2_noul=.25, choice2_order=.25)),
    "PR_condaqa": dict(rows=2.35, noul=1.85, choice=.5, score=0, rel=dict(complement_tmpl=.85, choice3_noul=.5, edit_contrast=.75)),
    "PR_vitc":    dict(rows=3.4,  noul=2.9,  choice=.5, score=0, rel=dict(complement_tmpl=.9, contrary=1, choice3_noul=.5, edit_contrast=.5)),
    "PR_nannli":  dict(rows=7.375, noul=6.375, choice=1, score=0, rel=dict(complement_tmpl=1, choice3_noul=1)),
    "PR_becel":   dict(rows=4.5,  noul=4.0,  choice=.5, score=0, rel=dict(complement_tmpl=1, human_complement=1, human_para=1, choice3_noul=.5)),
    "PR_unli":    dict(rows=2.0,  noul=2.0,  choice=0,  score=0, rel=dict(soft_complement=1)),
    "PR_spam":    dict(rows=3.5,  noul=3.0,  choice=.5, score=0, rel=dict(complement_tmpl=1, para=1, choice2_noul=.25, choice2_order=.25)),
    "PR_toxic":   dict(rows=4.0,  noul=3.0,  choice=0,  score=1, rel=dict(complement_tmpl=.7, soft_complement=.3, para=1, threshold_tail=1)),
    # freshly authored items
    "FR":         dict(rows=6.0,  noul=4.5,  choice=1.5, score=0, rel=dict(complement_free=1, para_free=1, dneg=.5, choice_noul=1, choice2_noul=.25, choice2_order=.25)),
}

# approximate state length in tokens (Ettin/ModernBERT tokenizer ~= 1.3 tokens/word)
EVAL_CORE = [
    # name, track, states, recipe, state_tokens, choice_options(avg K) , hard-gold share of noul rows
    ("banking77",       "in_domain", 32, "SL",          22, 12, 1.0),
    ("clinc150",        "in_domain", 32, "SL_clinc",     14, 12, 1.0),
    ("dbpedia14",       "in_domain", 24, "SL_hier",     90, 14, 1.0),
    ("clothing",        "in_domain", 24, "SC_clothing", 100, 6, 1.0),
    ("drug_reviews",    "in_domain", 24, "SC_drug",     140, 0, 1.0),
    ("boolq_bundle",    "in_domain", 24, "PR_boolq",    150, 2, 0.9),
    ("condaqa",         "in_domain", 24, "PR_condaqa",  200, 3, 0.9),
    ("vitaminc_real",   "in_domain", 24, "PR_vitc",      45, 3, 0.9),
    ("nlupp",           "zero_shot", 40, "ML",           18, 0, 1.0),
    ("hint3_v2",        "zero_shot", 24, "SL",           10, 16, 1.0),
    ("tfns",            "zero_shot", 24, "SL_tfns",      25, 3, 1.0),
    ("sst5",            "zero_shot", 24, "SC_sst",       30, 0, 1.0),
    ("supertweeteval",  "zero_shot", 24, "SC",           35, 0, 1.0),
    ("nan_nli",         "zero_shot", 48, "PR_nannli",    22, 3, 0.85),
    ("becel_snli",      "zero_shot", 24, "PR_becel",     18, 3, 1.0),
    ("unli",            "zero_shot", 24, "PR_unli",      22, 0, 0.0),
    ("sms_spam",        "zero_shot", 24, "PR_spam",      25, 2, 1.0),
    ("civil_comments",  "zero_shot", 24, "PR_toxic",     70, 0, 0.7),
    ("mhs",             "zero_shot", 24, "SC",           45, 0, 0.8),
    ("fresh",           "fresh",     96, "FR",          120, 4, 1.0),
]

# ----------------------------------------------------------------------------------------------
# 2. Robustness, comparability, anchors, reliability
# ----------------------------------------------------------------------------------------------
INJ_ITEMS = 60           # base items (clean call already in core)
INJ_ARMS_JEV = ["neutral_twin", "C_authority_meta", "D_argue_selflabel", "F_encoding_multilingual",
                "H_structured_field", "S_seen_family_new_template"]
INJ_ROWS_PER_STATE = 2    # targeted question + its eval-template negation
INJ_LOCAL_ONLY_ARMS = ["E_echo_gold_control", "I_offtarget_bipia_test"]  # 1 row each, no Jev call
DIST_ITEMS, DIST_DOSES, DIST_PLACEBO, DIST_ROWS_PER_STATE = 64, 2, 20, 2
COMPARABILITY = dict(btzsc_agnews=100, btzsc_emotiondair=100, btzsc_banking77=100)
ANCHOR_CALLS, ANCHOR_ROWS = 12, 30
RELIABILITY_CALLS = dict(test_retest_repeats=24, unbundled_singles=24)

JEV_CALL_CAP, EVAL_ROW_CAP = 1500, 5000
JEV_PRICE_PER_TOKEN = 0.042e-6
JEV_FIXED_TOKENS = 280


def q_tokens(kind, K=0):
    return {"noul": 60, "choice": 25 + 14 * K, "score": 30 + 12 * 5}[kind]


def eval_plan():
    rows_tot = calls_tot = 0
    by_track, rel_tot, dec = {}, {}, {"noul": 0.0, "noul_hard": 0.0, "choice": 0.0, "score": 0.0}
    per_ds, tokens = [], 0.0
    for name, track, n, rec, stok, K, hard in EVAL_CORE:
        r = RECIPES[rec]
        rows = n * r["rows"]
        rows_tot += rows; calls_tot += n
        t = by_track.setdefault(track, dict(states=0, rows=0.0))
        t["states"] += n; t["rows"] += rows
        for k, v in r["rel"].items():
            rel_tot[k] = rel_tot.get(k, 0) + n * v
        dec["noul"] += n * r["noul"]; dec["noul_hard"] += n * r["noul"] * hard
        dec["choice"] += n * r["choice"]; dec["score"] += n * r["score"]
        call_tok = JEV_FIXED_TOKENS + stok + r["noul"] * q_tokens("noul") + r["choice"] * q_tokens("choice", max(K, 2)) + r["score"] * q_tokens("score")
        tokens += n * call_tok
        per_ds.append(dict(dataset=name, track=track, states=n, rows=round(rows), recipe=rec,
                           complement_pairs=round(n * (r["rel"].get("complement_tmpl", 0) + r["rel"].get("complement_free", 0))), jev_tokens=round(n * call_tok)))
    core_rows, core_calls = rows_tot, calls_tot
    inj_calls = INJ_ITEMS * len(INJ_ARMS_JEV)
    inj_rows = inj_calls * INJ_ROWS_PER_STATE + INJ_ITEMS * len(INJ_LOCAL_ONLY_ARMS)
    dist_calls = DIST_ITEMS * DIST_DOSES + DIST_PLACEBO
    dist_rows = dist_calls * DIST_ROWS_PER_STATE
    comp_calls = sum(COMPARABILITY.values())
    rel_calls = sum(RELIABILITY_CALLS.values())
    tokens += inj_calls * (JEV_FIXED_TOKENS + 140 + 2 * 60) + DIST_ITEMS * (JEV_FIXED_TOKENS + 60 + 120 + 120) \
        + DIST_ITEMS * (JEV_FIXED_TOKENS + 60 + 450 + 120) + DIST_PLACEBO * (JEV_FIXED_TOKENS + 60 + 120) \
        + 100 * (JEV_FIXED_TOKENS + 60 + 30 + 4 * 14) + 100 * (JEV_FIXED_TOKENS + 25 + 30 + 6 * 12) \
        + 100 * (JEV_FIXED_TOKENS + 20 + 30 + 72 * 14) + ANCHOR_CALLS * 420 + rel_calls * 450
    total_calls = core_calls + inj_calls + dist_calls + comp_calls + ANCHOR_CALLS + rel_calls
    total_rows = core_rows + inj_rows + dist_rows + comp_calls + ANCHOR_ROWS
    return dict(per_dataset=per_ds, by_track=by_track, relations={k: round(v) for k, v in rel_tot.items()},
                decisions={k: round(v) for k, v in dec.items()},
                core=dict(calls=core_calls, rows=round(core_rows)),
                injection=dict(calls=inj_calls, rows=inj_rows, jev_rows=inj_calls * INJ_ROWS_PER_STATE),
                distractor=dict(calls=dist_calls, rows=dist_rows),
                comparability=dict(calls=comp_calls, rows=comp_calls),
                anchor=dict(calls=ANCHOR_CALLS, rows=ANCHOR_ROWS),
                reliability=dict(calls=rel_calls, rows=0),
                total_calls=total_calls, total_rows=round(total_rows),
                jev_tokens=round(tokens), jev_cost_usd=round(tokens * JEV_PRICE_PER_TOKEN, 4),
                cap_ok=total_calls <= JEV_CALL_CAP and total_rows <= EVAL_ROW_CAP)


# ----------------------------------------------------------------------------------------------
# 3. Train plan (question rows), <= 25k including dev
# ----------------------------------------------------------------------------------------------
TRAIN = [
    # component, source, states, rows
    ("base", "banking77 train (label-noise filtered)", 770, 1540),
    ("base", "clinc150 plus train (incl. oos)", 750, 1725),
    ("base", "massive en-US train", 360, 830),
    ("base", "dbpedia_14 train", 560, 1400),
    ("base", "go_emotions raw (>=2-rater Ekman majority)", 700, 1400),
    ("base", "womens clothing reviews train", 600, 1620),
    ("base", "uci drug reviews train (regrouped)", 400, 920),
    ("base", "multi_nli train (promptID groups)", 600, 1980),
    ("base", "wanli train (rebalanced)", 800, 1200),
    ("base", "boolq train (eval passages removed)", 1000, 1000),
    ("base", "condaqa train (passage groups)", 350, 500),
    ("base", "vitaminc train (whole cases)", 400, 800),
    ("consistency", "negation (train templates)", 0, 1500),
    ("consistency", "paraphrase frame/proposition (train)", 0, 950),
    ("consistency", "double negation (train)", 0, 350),
    ("consistency", "choice2-of-noul (+reversed order)", 0, 400),
    ("consistency", "score reversal + rebin", 0, 350),
    ("injection", "families A,B,E,G targeted", 1300, 1300),
    ("injection", "family I off-target (BIPIA train cats)", 200, 200),
    ("injection", "echo controls (payload names gold)", 250, 250),
    ("injection", "neutral twins", 150, 150),
    ("injection", "fresh hard negatives (legit in-content instructions)", 120, 180),
    ("distractor", "wikitext-103 + boilerplate A, doses 0.5-4x", 1150, 1300),
]
DEV_ROWS = 2000


def train_plan():
    tot = sum(r for *_, r in TRAIN)
    by = {}
    for comp, _, _, r in TRAIN:
        by[comp] = by.get(comp, 0) + r
    return dict(rows=tot, dev_rows=DEV_ROWS, total_with_dev=tot + DEV_ROWS, by_component=by,
                cap_ok=tot + DEV_ROWS <= 25000)


# ----------------------------------------------------------------------------------------------
# 4. Power
# ----------------------------------------------------------------------------------------------
Z = stats.norm.ppf(0.975); ZB = stats.norm.ppf(0.80)


def wilson_hw(p, n):
    z = Z
    den = 1 + z * z / n
    return z * math.sqrt(p * (1 - p) / n + z * z / (4 * n * n)) / den


def _r(x, k=3):
    return None if x is None else round(x, k)


def mcnemar_mde(n, p_disc):
    # smallest delta with power .8 at alpha .05 (two-sided), Connor (1987) approximation
    lo, hi = 1e-4, p_disc
    for _ in range(60):
        d = (lo + hi) / 2
        need = (Z * math.sqrt(p_disc) + ZB * math.sqrt(max(p_disc - d * d, 1e-9))) ** 2 / (d * d)
        lo, hi = (d, hi) if need > n else (lo, d)
    return None if hi >= 0.999 * p_disc else hi


def mean_diff_mde(sd, n, deff=1.0):
    return (Z + ZB) * sd / math.sqrt(n / deff)


def cp_upper(k, n, a=0.05):  # one-sided 95% Clopper-Pearson upper bound
    return 1.0 if k >= n else stats.beta.ppf(1 - a, k + 1, n - k)


def cp_two_sided(k, n):
    lo = 0.0 if k == 0 else stats.beta.ppf(0.025, k, n - k + 1)
    hi = 1.0 if k == n else stats.beta.ppf(0.975, k + 1, n - k)
    return lo, hi


def ece_top(conf, correct, bins=10):
    idx = np.minimum((conf * bins).astype(int), bins - 1)
    e = 0.0
    for b in range(bins):
        m = idx == b
        if m.any():
            e += m.mean() * abs(correct[m].mean() - conf[m].mean())
    return e


def ece_noise_floor(n, k_classes=2, reps=2000, rng=None):
    """ECE of a *perfectly calibrated* model at sample size n (jujumilk3 'noise floor').
    Confidence profile ~ what fine-tuned encoders / Jev produce: most mass near 1."""
    rng = rng or np.random.default_rng(SEED)
    lo = 1.0 / k_classes
    out = []
    for _ in range(reps):
        conf = lo + (1 - lo) * rng.beta(4.0, 0.9, n)
        correct = (rng.random(n) < conf).astype(float)
        out.append(ece_top(conf, correct))
    return float(np.mean(out)), float(np.quantile(out, 0.95))


def power_tables(ep):
    d, rel = ep["decisions"], ep["relations"]
    rng = np.random.default_rng(SEED)
    acc = {f"n={n}": {f"p={p}": round(wilson_hw(p, n), 3) for p in (0.5, 0.8, 0.9, 0.95)}
           for n in (24, 48, 100, 208, 300, 600, 1000, 1800)}
    # template complement pairs: half seen-style, half unseen-style (assignment by item hash)
    comp_pairs = rel["complement_tmpl"]
    e1_n = comp_pairs / 2 + rel.get("human_complement", 0) + rel.get("complement_free", 0)
    e1 = {sd: round(mean_diff_mde(sd, e1_n, deff=1.15), 4) for sd in (0.06, 0.10, 0.15, 0.25)}
    zs_base = 2 * sum(n for name, tr, n, *_ in EVAL_CORE if tr == "zero_shot")  # ~2 base rows/state
    e2 = {pdisc: _r(mcnemar_mde(zs_base / 1.3, pdisc), 3) for pdisc in (0.10, 0.20, 0.30)}
    zs_noul = sum(n * RECIPES[rec]["noul"] for name, tr, n, rec, *_ in EVAL_CORE if tr == "zero_shot")
    e3 = {sd: round(mean_diff_mde(sd, zs_noul, deff=1.5), 4) for sd in (0.10, 0.15, 0.20)}
    pooled_noul = d["noul_hard"]
    fold = pooled_noul / 2
    cov = {}
    for c in (0.3, 0.5, 0.7):
        acc_n = int(fold * c)
        for err in (0.005, 0.01):
            k = int(round(acc_n * err))
            cov[f"coverage={c},true_risk={err}"] = dict(accepted_per_fold=acc_n, errors=k,
                                                          cp95_two_sided=[round(x, 4) for x in cp_two_sided(k, acc_n)],
                                                          cp95_upper=round(cp_upper(k, acc_n), 4))
    cov["coverage_halfwidth_pp"] = round(100 * Z * math.sqrt(0.25 / pooled_noul) * math.sqrt(1.5), 1)
    cov["min_accepted_to_certify_1pct_with_0_errors"] = next(n for n in range(50, 2000) if cp_upper(0, n) <= 0.01)
    cov["min_accepted_to_certify_1pct_with_2_errors"] = next(n for n in range(50, 4000) if cp_upper(2, n) <= 0.01)
    inj_attacks = INJ_ITEMS * 4
    e5 = dict(pooled_heldout_n=inj_attacks,
              wilson_hw={f"asr={p}": round(wilson_hw(p, inj_attacks), 3) for p in (0.1, 0.2, 0.3, 0.5)},
              per_family_hw={f"asr={p}": round(wilson_hw(p, INJ_ITEMS), 3) for p in (0.1, 0.2, 0.3)},
              paired_mde={pd_: _r(mcnemar_mde(inj_attacks, pd_), 3) for pd_ in (0.2, 0.3, 0.4)})
    dist_rows = DIST_ITEMS * DIST_ROWS_PER_STATE
    e6 = dict(rows_per_dose=dist_rows,
              mean_abs_dp_se={sd: round(sd / math.sqrt(dist_rows / 1.3), 4) for sd in (0.05, 0.10, 0.15)},
              delta_acc_mde={pd_: _r(mcnemar_mde(dist_rows / 1.3, pd_), 3) for pd_ in (0.05, 0.10, 0.15)})
    floors = {}
    for label, n, k in (("noul_pooled", int(d["noul"]), 2), ("noul_zero_shot", int(zs_noul), 2),
                        ("choice_pooled", int(d["choice"] + 300), 8), ("score_pooled", int(d["score"]), 5),
                        ("slice_100", 100, 4)):
        m, q95 = ece_noise_floor(n, k, reps=2000, rng=rng)
        floors[label] = dict(n=n, mean_floor=round(m, 4), p95_floor=round(q95, 4))
    return dict(accuracy_wilson_halfwidth=acc,
                E1_complement_violation=dict(pairs_novel_negation_forms=round(e1_n), pairs_all_template=comp_pairs,
                                             mde_by_sd_of_paired_diff=e1),
                E2_zero_shot_accuracy=dict(base_decisions=zs_base, mde_by_discordance=e2),
                E3_brier_noul_zero_shot=dict(n=round(zs_noul), mde_by_sd=e3),
                E4_coverage_at_1pct=cov, E5_injection=e5, E6_distractor=e6, ece_noise_floor=floors)


def cpu_runtime(ep):
    """Seconds on the measured M4 CPU (scout_formats 2.4): q/s at 25/400/1024 tokens."""
    pts = {"edge": [(25, 442), (400, 43.5), (1024, 14.4)], "modern_base": [(25, 77), (400, 7.1), (1024, 2.6)]}

    def qps(model, tok):
        xs = [math.log(t) for t, _ in pts[model]]; ys = [math.log(q) for _, q in pts[model]]
        return math.exp(np.interp(math.log(max(tok, 25)), xs, ys))
    out = {}
    for model in pts:
        s = 0.0
        for name, tr, n, rec, stok, K, _ in EVAL_CORE:
            r = RECIPES[rec]
            nrows = n * r["rows"]
            tok = stok + 40 + (14 * K if r["choice"] else 12)
            s += nrows / qps(model, tok)
        s += ep["injection"]["rows"] / qps(model, 220) + (DIST_ITEMS * 2) / qps(model, 200) \
            + (DIST_ITEMS * 2) / qps(model, 620) + 40 / qps(model, 120) \
            + 100 / qps(model, 1024) + 200 / qps(model, 120)
        out[model] = round(s / 60, 1)
    return out


def main():
    ap = argparse.ArgumentParser(); ap.add_argument("--json")
    a = ap.parse_args()
    ep = eval_plan(); tp = train_plan(); pw = power_tables(ep); cpu = cpu_runtime(ep)
    res = dict(eval=ep, train=tp, power=pw, cpu_minutes=cpu)
    print(json.dumps(res, indent=1))
    if a.json:
        json.dump(res, open(a.json, "w"), indent=1)


if __name__ == "__main__":
    main()
