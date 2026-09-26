#!/usr/bin/env python3
"""Size, budget, runtime and power calculator for DESIGN.md (OpenDecide v1.0).

Every count in DESIGN.md sections 9-10 is produced by this file. Re-run it whenever a quota changes:
    python3 design/design_plan.py            # prints JSON
    python3 design/design_plan.py --json out.json
Pure python + numpy/scipy; no network. Master seed 20260925.
v1.1 (review round 1): trap states (CondaQA DON'T KNOW, VitaminC NEI, NaN-NLI neutral), FR Q7 Score slot,
near-threshold rows not hard, 100-call unbundling check, echo parity in train, Holm-adjusted and
cluster-adjusted power. See DESIGN.md "Review log".
"""
from __future__ import annotations
import argparse, json, math
import numpy as np
from scipy import stats

SEED = 20260925
JEV_CALL_CAP, EVAL_ROW_CAP, TRAIN_CAP = 1500, 5000, 25000
JEV_PRICE, JEV_FIXED = 0.042e-6, 280

# ------------------------------------------------------------------------------------------------
# 1. Clean core: per dataset -> states, rows by type, relations. Fractions are realised by rank
#    parity (even/odd), so every count below is exact when states is even.
#    fields: track, states, noul, choice, score (rows), hard_noul (hard-gold, headline Noul rows),
#            rel {type: count}, state_tok (Ettin), K (avg options of Choice rows)
# ------------------------------------------------------------------------------------------------
C = {}
def ds(name, track, states, noul, choice, score, hard_noul, rel, state_tok, K):
    C[name] = dict(track=track, states=states, noul=noul, choice=choice, score=score,
                   rows=noul + choice + score, hard_noul=hard_noul, rel=rel, tok=state_tok, K=K)

# in-domain (8 datasets, 224 states)
ds("banking77", "ID", 40, 140, 60, 0, 140, dict(complement=40, paraphrase=40, choice_noul=40, dneg=20, choice2=20), 22, 12)
ds("clinc150", "ID", 40, 180, 60, 0, 180, dict(complement=40, paraphrase=40, choice_noul=40, dneg=20, choice2=20, monotone=40), 14, 12)
ds("goemotions", "ID", 24, 72, 24, 0, 72, dict(complement=24, paraphrase=24), 20, 7)
ds("clothing", "ID", 24, 84, 0, 48, 59,   # 10 states rated 3 or 4: threshold rows not hard (review #7)
   dict(complement=24, paraphrase=12, score_reversal=24, threshold_tail=24, human_floor=24), 90, 0)
ds("drug_reviews", "ID", 24, 60, 0, 72, 48,   # ~5 states rated 6 or 7: threshold rows not hard
   dict(complement=24, paraphrase=12, score_reversal=24, threshold_tail=24, rebin=24), 120, 0)
ds("boolq_bundle", "ID", 24, 96, 12, 0, 88, dict(complement=24, human_complement=20, human_paraphrase=16, choice2=12), 200, 2)
ds("condaqa", "ID", 24, 48, 12, 0, 48, dict(complement=24, choice3_noul=12, edit_contrast=6), 180, 3)
ds("vitaminc_real", "ID", 24, 72, 12, 0, 72, dict(complement=24, contrary=24, choice3_noul=12, edit_contrast=12), 45, 3)
# undecidable negation-frame TRAP states (review #1): scoped affirmative (gold 0) + scoped negation (gold 0) + Choice-3
# (gold "cannot tell"). Trap rows are excluded from E2-E4 and from the V4 yes-rate balance; hard_noul = 0 here.
ds("condaqa_dk_trap", "ID", 22, 44, 22, 0, 0, dict(trap=22, choice3_noul=22), 180, 3)
ds("vitaminc_nei_trap", "ID", 22, 44, 22, 0, 0, dict(trap=22, choice3_noul=22), 45, 3)
# zero-shot (10 datasets, 280 states); nlupp has 20 SLOT rows that are diagnostic (not headline)
ds("nlupp", "ZS", 40, 280, 0, 0, 260, dict(complement=40, paraphrase=40, conj_disj=40, dneg=20), 18, 0)
ds("hint3_v2", "ZS", 24, 84, 36, 0, 84, dict(complement=24, paraphrase=24, choice_noul=24, dneg=12, choice2=12), 10, 12)
ds("tfns", "ZS", 24, 96, 24, 0, 96, dict(complement=24, paraphrase=24, choice_noul=24, contrary=24), 25, 3)
ds("sst5", "ZS", 24, 84, 0, 48, 78,   # ~3 states within +-0.05 of 0.4 / 0.6: threshold rows not hard
   dict(complement=24, paraphrase=12, score_reversal=24, threshold_tail=24, contrary=24), 30, 0)
ds("supertweeteval", "ZS", 24, 60, 0, 48, 60, dict(complement=24, paraphrase=12, score_reversal=24, threshold_tail=24), 35, 0)
# nan_nli: 46 premises have decidable hypotheses (Q1-Q3 + NEG(Q1)); 2 premises are neutral-only (trap pair + Choice-3);
# the 19 premises with a neutral hypothesis add a scoped trap pair (Q6, Q7): 184 + 38 = 222 Noul rows.
ds("nan_nli", "ZS", 48, 222, 48, 0, 184, dict(complement=46, trap=19, choice3_noul=48), 22, 3)
ds("becel_snli", "ZS", 24, 72, 12, 0, 72, dict(complement=24, human_complement=12, human_paraphrase=12, choice3_noul=12), 18, 3)
ds("sms_spam", "ZS", 24, 72, 24, 0, 72, dict(complement=24, paraphrase=24, choice2=24), 25, 2)
ds("civil_comments", "ZS", 24, 72, 0, 24, 36, dict(complement=12, soft_complement=12, paraphrase=24, threshold_tail=24), 70, 0)
ds("mhs", "ZS", 24, 60, 0, 48, 45, dict(complement=19, soft_complement=5, paraphrase=12, score_reversal=24, threshold_tail=24), 45, 0)
# fresh (6 families x 16 accepted); FR-NUM and FR-DATE (32 states) are diagnostic (not headline)
# fresh: + Q7 Score on FR-LIT (K=4 on 8, K=7 on 8), FR-HOP (K=7, 8) and FR-PHISH (K=7, 8) (review #8)
ds("fresh", "FR", 96, 408, 144, 56, 272, dict(free_complement=96, free_paraphrase=96, dneg=48, choice2=48, choice_noul=96, criteria_variant=16), 130, 4)

# ------------------------------------------------------------------------------------------------
# 2. Robustness, comparability, reliability, local diagnostics
# ------------------------------------------------------------------------------------------------
INJ_ITEMS = 60
INJ_ARMS = {  # arm: (states, rows per state)
    "N_neutral_twin": (60, 2), "C_authority_meta": (60, 2), "D_argue_selflabel": (60, 2),
    "F_encoding_multilingual": (60, 2), "H_structured_field": (30, 2), "HN_field_neutral": (30, 2),
    "S_seen_family_new_template": (30, 2), "E_echo_control": (60, 1), "O_offtarget_bipia_test": (60, 1)}
HELD_OUT = ["C_authority_meta", "D_argue_selflabel", "F_encoding_multilingual", "H_structured_field"]
DIST_ITEMS = 64
DIST_ARMS = {"short_dose": (64, 2), "long_dose": (64, 2), "hard_reference": (24, 2), "placebo": (20, 2)}
CMP = {"btzsc_banking77_replay": (100, 100), "typesafe_doc_tickets": (2, 4), "colinmcnamara_pairs": (10, 40)}
REL = {"test_retest_resend": 16, "unbundled_singles": 100}   # 50 complement pairs x 2 single-question calls (review #12)   # re-sends of existing rows; 0 new rows
LOCAL_DIAG = {"diag_wording": 304, "diag_option_perm": 160}   # option-perm: seeded stratified subset of primary Choices  # local models only, counted in the 5k cap


def eval_plan():
    core_states = sum(d["states"] for d in C.values())
    core_rows = sum(d["rows"] for d in C.values())
    by_track = {}
    for d in C.values():
        t = by_track.setdefault(d["track"], dict(states=0, rows=0, noul=0, choice=0, score=0, hard_noul=0))
        for k in ("states", "rows", "noul", "choice", "score", "hard_noul"):
            t[k] += d[k]
    rel = {}
    for d in C.values():
        for k, v in d["rel"].items():
            rel[k] = rel.get(k, 0) + v
    inj_calls = sum(s for s, _ in INJ_ARMS.values()); inj_rows = sum(s * r for s, r in INJ_ARMS.values())
    dist_calls = sum(s for s, _ in DIST_ARMS.values()); dist_rows = sum(s * r for s, r in DIST_ARMS.values())
    cmp_calls = sum(c for c, _ in CMP.values()); cmp_rows = sum(r for _, r in CMP.values())
    rel_calls = sum(REL.values()); diag_rows = sum(LOCAL_DIAG.values())
    total_calls = core_states + inj_calls + dist_calls + cmp_calls + rel_calls
    total_rows = core_rows + inj_rows + dist_rows + cmp_rows + diag_rows
    # tokens
    def qt(kind, K=0):
        return {"noul": 60, "choice": 25 + 14 * K, "score": 30 + 12 * 6}[kind]
    tok = 0
    for d in C.values():
        tok += d["states"] * JEV_FIXED + d["states"] * d["tok"] + d["noul"] * qt("noul") \
            + d["choice"] * qt("choice", max(d["K"], 2)) + d["score"] * qt("score")
    tok += inj_calls * (JEV_FIXED + 200 + 2 * 90) + dist_calls * (JEV_FIXED + 60 + 330 + 2 * 90) \
        + 100 * (JEV_FIXED + 25 + 30 + 72 * 14) + 12 * 420 + rel_calls * 500
    return dict(core=dict(states=core_states, rows=core_rows, by_track=by_track),
                per_dataset={k: dict(track=v["track"], states=v["states"], rows=v["rows"], noul=v["noul"],
                                     choice=v["choice"], score=v["score"]) for k, v in C.items()},
                relations=rel,
                injection=dict(calls=inj_calls, rows=inj_rows, arms=INJ_ARMS),
                distractor=dict(calls=dist_calls, rows=dist_rows, arms=DIST_ARMS),
                comparability=dict(calls=cmp_calls, rows=cmp_rows), reliability=dict(calls=rel_calls, rows=0),
                local_diag_rows=diag_rows, total_calls=total_calls, total_rows=total_rows,
                jev_input_tokens=int(tok), jev_cost_usd=round(tok * JEV_PRICE, 3),
                caps_ok=total_calls <= JEV_CALL_CAP and total_rows <= EVAL_ROW_CAP)


# ------------------------------------------------------------------------------------------------
# 3. Train / dev plan
# ------------------------------------------------------------------------------------------------
TRAIN = [  # layer, component, states, rows
    ("L0_base", "banking77", 900, 1800), ("L0_base", "clinc150_plus", 800, 1600),
    ("L0_base", "massive_en_US", 500, 1000), ("L0_base", "dbpedia14", 450, 900),
    ("L0_base", "goemotions_raw", 600, 1200), ("L0_base", "clothing", 450, 1200),
    ("L0_base", "drug_reviews", 400, 900), ("L0_base", "multi_nli", 500, 1500),
    ("L0_base", "wanli", 700, 700), ("L0_base", "boolq", 1000, 1000),
    ("L0_base", "condaqa", 600, 600), ("L0_base", "vitaminc", 300, 600),
    ("L2_consistency", "negation_template", 0, 1700), ("L2_consistency", "trap_undecidable", 0, 300),
    ("L2_consistency", "trap_contrary", 0, 250), ("L2_consistency", "paraphrase", 0, 900),
    ("L2_consistency", "double_negation", 0, 350), ("L2_consistency", "choice2_twin", 0, 450),
    ("L2_consistency", "score_transforms", 0, 400), ("L2_consistency", "hierarchy", 0, 250),
    ("L3_injection", "targeted_ABEG", 700, 800), ("L3_injection", "echo_controls", 800, 800),   # parity (review #6)
    ("L3_injection", "neutral_twins", 350, 350), ("L3_injection", "offtarget_bipia_train", 200, 200),
    ("L3_injection", "hard_negatives_authored", 120, 240),
    ("L3_distractor", "wikitext_boilerplateA", 800, 1600), ("L3_distractor", "reference_A_hard", 150, 150),
]
DEV_ROWS, DEV_ZS_ROWS = 2000, 600


def train_plan():
    by = {}
    for layer, _, _, r in TRAIN:
        by[layer] = by.get(layer, 0) + r
    tot = sum(r for *_, r in TRAIN)
    return dict(train_rows=tot, by_layer=by, dev_rows=DEV_ROWS, dev_zs_rows=DEV_ZS_ROWS,
                total=tot + DEV_ROWS + DEV_ZS_ROWS, cap_ok=tot + DEV_ROWS + DEV_ZS_ROWS <= TRAIN_CAP,
                base_states=sum(s for l, _, s, _ in TRAIN if l == "L0_base"))


# ------------------------------------------------------------------------------------------------
# 4. Power
# ------------------------------------------------------------------------------------------------
Z = stats.norm.ppf(0.975); ZB = stats.norm.ppf(0.80)
HOLM_K = 4                       # E1, E3, E4, E5 (E2 is estimation only, outside Holm; review #11)
ALPHA_HOLM_FIRST = 0.05 / HOLM_K # the most stringent Holm step
# expected retention after verification (planning assumptions; the build recomputes from real outcomes)
RET_HUMAN_NEG = 0.85             # BECEL tag=negation / NP negator questions that both verifiers read unambiguously
RET_C6_SINGLE = 0.85             # C6 OTHER-THAN pairs confirmed single-request (else SUM_GE_1, outside E1)
C6_PAIRS = 26                    # half of the unseen-class pairs on banking77 / clinc150 / hint3
TWO_OF_TWO = 0.90                # share of hard rows verified 2of2 (E4 uses 2of2 only)
E5_ATTACKS_PER_ITEM, E5_ICC = 3.5, 0.3

def zq(alpha):
    return stats.norm.ppf(1 - alpha / 2)

def wilson_hw(p, n):
    den = 1 + Z * Z / n
    return Z * math.sqrt(p * (1 - p) / n + Z * Z / (4 * n * n)) / den

def mcnemar_mde(n, p_disc, alpha=0.05):
    za = zq(alpha); lo, hi = 1e-4, p_disc
    for _ in range(60):
        d = (lo + hi) / 2
        need = (za * math.sqrt(p_disc) + ZB * math.sqrt(max(p_disc - d * d, 1e-9))) ** 2 / (d * d)
        lo, hi = (d, hi) if need > n else (lo, d)
    return None if hi >= 0.999 * p_disc else round(hi, 3)

def mean_mde(sd, n, deff=1.0, alpha=0.05):
    return round((zq(alpha) + ZB) * sd / math.sqrt(n / deff), 4)

def cp_upper(k, n, a=0.05):
    return 1.0 if k >= n else stats.beta.ppf(1 - a, k + 1, n - k)

def ece_top(conf, correct, bins=10):
    idx = np.minimum((conf * bins).astype(int), bins - 1); e = 0.0
    for b in range(bins):
        m = idx == b
        if m.any():
            e += m.mean() * abs(correct[m].mean() - conf[m].mean())
    return e

def ece_floor(n, k, reps=2000, rng=None):
    lo = 1.0 / k; out = []
    for _ in range(reps):
        conf = lo + (1 - lo) * rng.beta(4.0, 0.9, n)
        out.append(ece_top(conf, (rng.random(n) < conf).astype(float)))
    return round(float(np.mean(out)), 4), round(float(np.quantile(out, 0.95)), 4)


def power(ep):
    rel = ep["relations"]; bt = ep["core"]["by_track"]; rng = np.random.default_rng(SEED)
    tmpl = rel["complement"]
    unseen = tmpl // 2
    c6_out = round(C6_PAIRS * (1 - RET_C6_SINGLE))
    human = round(rel.get("human_complement", 0) * RET_HUMAN_NEG)
    e1_n = unseen - c6_out + human + rel.get("free_complement", 0)
    zs_base = sum(v["states"] for v in C.values() if v["track"] == "ZS") * 2   # ~2 base decisions/state
    e3_n = bt["ZS"]["hard_noul"]                                             # hard_ok ZS Noul rows (review #28)
    pooled_hard = sum(t["hard_noul"] for t in bt.values())
    e4_n = int(pooled_hard * TWO_OF_TWO)                                     # text-decided, 2of2 only (review #7)
    fold = e4_n // 2
    held = sum(INJ_ARMS[a][0] for a in HELD_OUT)
    e5_deff = 1 + (E5_ATTACKS_PER_ITEM - 1) * E5_ICC
    e5_eff = held / e5_deff
    trap = rel.get("trap", 0)
    out = dict(
        holm=dict(endpoints=["E1", "E3", "E4", "E5"], alpha_first_step=ALPHA_HOLM_FIRST, E2="estimation only"),
        accuracy_wilson_hw={n: {p: round(wilson_hw(p, n), 3) for p in (0.5, 0.8, 0.9)} for n in (24, 40, 96, 224, 280, 560, 1000, 2000)},
        E1=dict(pairs=e1_n, unseen_class_template=unseen, c6_moved_to_sum_ge_1=c6_out, human_retained=human,
                free=rel.get("free_complement", 0), template_pairs_all=tmpl,
                mde_alpha05={sd: mean_mde(sd, e1_n, 1.15) for sd in (0.06, 0.10, 0.15)},
                mde_holm={sd: mean_mde(sd, e1_n, 1.15, ALPHA_HOLM_FIRST) for sd in (0.06, 0.10, 0.15)},
                trap_pairs=trap, trap_pass_wilson_hw={p: round(wilson_hw(p, trap), 3) for p in (0.5, 0.7, 0.9)},
                trap_pairs_plus_both_no_contraries=trap + 13),
        E2=dict(zs_base_decisions=zs_base, mcnemar_mde={pd: mcnemar_mde(zs_base / 1.3, pd) for pd in (0.10, 0.20, 0.30)},
                wilson_hw_p80=round(wilson_hw(0.8, zs_base / 1.3), 3), in_holm=False),
        E3=dict(zs_hard_noul_rows=e3_n, mde_alpha05={sd: mean_mde(sd, e3_n, 1.5) for sd in (0.10, 0.15, 0.20)},
                mde_holm={sd: mean_mde(sd, e3_n, 1.5, ALPHA_HOLM_FIRST) for sd in (0.10, 0.15, 0.20)}),
        E4=dict(pooled_hard_noul=pooled_hard, e4_rows_2of2=e4_n, per_fold=fold,
                coverage_ci_halfwidth_pp=round(100 * Z * math.sqrt(0.25 / e4_n) * math.sqrt(1.5), 1),
                cp_upper_at_50pct_cov_05pct_risk=round(cp_upper(round(fold * .5 * .005), int(fold * .5)), 4),
                min_accepted_0_err=next(n for n in range(50, 3000) if cp_upper(0, n) <= 0.01),
                min_accepted_2_err=next(n for n in range(50, 4000) if cp_upper(2, n) <= 0.01)),
        E5=dict(held_out_attacks=held, items=INJ_ITEMS, design_effect=round(e5_deff, 2), n_eff=round(e5_eff, 1),
                wilson_hw_naive={p: round(wilson_hw(p, held), 3) for p in (0.1, 0.2, 0.3)},
                wilson_hw_clustered={p: round(wilson_hw(p, e5_eff), 3) for p in (0.1, 0.2, 0.3)},
                per_family_hw_n60_clustered={p: round(wilson_hw(p, 60 / (1 + (60 / INJ_ITEMS - 1) * E5_ICC)), 3) for p in (0.1, 0.2, 0.3)},
                paired_mde_clustered_alpha05={pd: mcnemar_mde(e5_eff, pd) for pd in (0.2, 0.3)},
                paired_mde_clustered_holm={pd: mcnemar_mde(e5_eff, pd, ALPHA_HOLM_FIRST) for pd in (0.2, 0.3)}),
        rel_unbundled=dict(pairs=REL["unbundled_singles"] // 2,
                           se_mean_abs_dsum_sd05=round(0.05 / math.sqrt(REL["unbundled_singles"] // 2), 4),
                           mde_dsum_sd05=mean_mde(0.05, REL["unbundled_singles"] // 2)),
        distractor=dict(rows_per_dose=DIST_ITEMS * 2, se_mean_abs_dp={sd: round(sd / math.sqrt(DIST_ITEMS * 2 / 1.3), 4) for sd in (0.05, 0.10, 0.15)},
                        dacc_mde={pd: mcnemar_mde(DIST_ITEMS * 2 / 1.3, pd) for pd in (0.10, 0.15)}),
        ece_noise_floor={"noul_pooled": ece_floor(bt["ID"]["noul"] + bt["ZS"]["noul"] + bt["FR"]["noul"], 2, rng=rng),
                         "noul_ZS": ece_floor(e3_n, 2, rng=rng),
                         "choice_pooled": ece_floor(sum(t["choice"] for t in bt.values()), 8, rng=rng),
                         "score_pooled": ece_floor(sum(t["score"] for t in bt.values()), 5, rng=rng),
                         "slice_100": ece_floor(100, 4, rng=rng)})
    return out


def cpu(ep):
    pts = {"edge": [(25, 442), (400, 43.5), (1024, 14.4)], "modern_base": [(25, 77), (400, 7.1), (1024, 2.6)]}
    def qps(m, t):
        xs = [math.log(a) for a, _ in pts[m]]; ys = [math.log(b) for _, b in pts[m]]
        return math.exp(np.interp(math.log(max(t, 25)), xs, ys))
    res = {}
    for m in pts:
        s = sum(d["rows"] / qps(m, d["tok"] + 40 + (14 * d["K"] if d["choice"] else 12)) for d in C.values())
        s += ep["injection"]["rows"] / qps(m, 260) + 128 / qps(m, 270) + 128 / qps(m, 620) \
            + 88 / qps(m, 200) + 100 / qps(m, 1024) + 44 / qps(m, 80) + sum(LOCAL_DIAG.values()) / qps(m, 120)
        res[m] = round(s / 60, 1)
    return res


def main():
    ap = argparse.ArgumentParser(); ap.add_argument("--json"); a = ap.parse_args()
    ep = eval_plan(); res = dict(eval=ep, train=train_plan(), power=power(ep), cpu_minutes_m4=cpu(ep))
    print(json.dumps(res, indent=1, default=str))
    if a.json:
        json.dump(res, open(a.json, "w"), indent=1, default=str)


if __name__ == "__main__":
    main()
