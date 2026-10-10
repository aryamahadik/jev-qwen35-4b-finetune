"""Score OHS-3 exactly as pre-registered in PREREG_OHS3.md. New file; score_ohs.py is left unchanged (it stays the
scorer of record for OHS-1 and OHS-2).

What this fixes relative to score_ohs.py (audit, 30 Sep 2026; PREREG_OHS3.md lines 118-156):
  * Brier sign. PREREG: "The Brier difference is Jev minus OpenDecide" (positive = OpenDecide better). score_ohs.py
    reported OpenDecide minus Jev, so a Brier loss looked like a CI "entirely above 0".
  * Complement violation. PREREG: share of _neg pairs whose two decisions are not complementary (both yes or both no);
    a tie or a missing answer on either row counts as a violation. score_ohs.py reported mean |pa + pb - 1| as the
    endpoint and silently skipped pairs with a missing answer. Here the mean |pa + pb - 1| is a descriptive extra.
  * Option-order drift. A tie or a missing answer now counts as drift (score_ohs.py skipped missing answers and broke
    ties by dict order).
  * Consistency endpoints get the same paired cluster bootstrap (CI, p) as the accuracy endpoints, and every secondary
    endpoint gets a Benjamini-Hochberg adjustment. The verdicts "beats" / "matches" / "Jev is better" are computed.
  * One shared bootstrap: one stratified draw of groups per resample serves every endpoint (score_ohs.py re-drew a
    separate stream for the Brier endpoint).

Definitions implemented (all from PREREG_OHS3.md unless marked INTERPRETATION; the interpretations are listed for the
owner in prereg_drafts/score_ohs3_interpretations.md):
  * Base rows: every row that is not a twin (id ending _neg/_perm/_dneg/_para/_yn, or meta.variant_of set). Primary
    endpoints use base rows only; the 604 twins are used only for the consistency endpoints.
  * Task = row["source"] (OHS-3: source == meta.task == the builder's TASK; checked 1:1 here). Groups = group_id.
  * Prediction: the option with the highest probability; on a yes/no row yes if P(yes) > 0.5, no if P(yes) < 0.5.
    Ties (equal top probabilities, or P(yes) == 0.5, exact float equality) and missing answers count as wrong.
    A missing answer = no prediction record for the row, no "yes" key on a yes/no row, or a non-finite probability.
    Keys that are not options of the row (e.g. Jev's "_raw_sum") are ignored; an option absent from the record is 0.
  * Brier on yes/no base rows: (P(yes) - gold)^2; a yes/no row with no P(yes) scores 1.
  * Jev = mean of its runs, computed per row (per pair for the consistency endpoints): the per-row score of each run
    (correct 0/1, Brier, violation 0/1, ...) is averaged over the runs. Rows Jev fails to answer count as wrong for
    Jev and are reported separately (per run, per task, base and twin rows).
  * Complement violation (_neg pairs, relation "complement"): 1 if either decision is a tie/missing or both decisions
    are equal (both yes or both no), else 0. Also reported: mean |P_base(yes) + P_neg(yes) - 1| (INTERPRETATION: a
    missing P(yes) on either row scores 1, the maximum) and accuracy on the _neg rows.
  * Option-order drift (_perm pairs, relation "equiv" between choice rows): 1 if either prediction is a tie/missing or
    the predicted option names differ, else 0. Also reported: mean total-variation distance between the two
    probability vectors aligned by option name (each renormalised over the row's options; INTERPRETATION: missing
    or all-zero vector scores 1, the maximum) and accuracy on the _perm rows.
  * Differences: accuracy = OpenDecide - Jev; Brier, violation, drift (and the descriptive |.|, TV) = Jev - OpenDecide.
    Positive always means OpenDecide is better.
  * Bootstrap: paired cluster bootstrap over group_id, stratified by task. numpy.random.default_rng(0); for each of
    the 10,000 resamples, for each task in sorted order, rng.integers(0, n_t, n_t) draws that task's groups (the same
    draw order as score_ohs.py, so OHS-2 micro/macro intervals reproduce it exactly). All rows of a drawn group, and
    its pairs (a pair belongs to its base row's group), come with it. Every endpoint is a ratio of resampled sums
    (micro: pooled; macro: unweighted mean of per-task ratios). 95% percentile interval (numpy linear).
  * p = min(1, 2 * min(share of resamples with difference <= 0, share with difference >= 0)).
  * Primary family (Holm, 3): micro accuracy, macro accuracy, Brier (yes/no base rows).
    Beats: CI entirely above 0 and Holm p < 0.05. Matches: CI lower bound > -2.0 pp (accuracy) / > -0.010 (Brier).
    Label precedence as written: beats, else matches, else "jev_better" if the CI upper bound < 0, else "neither".
    The flags ci_above_0 / ci_below_0 / matches are also printed, so "matches but CI below 0" is visible.
  * Secondary family (Benjamini-Hochberg; INTERPRETATION of "the family"): accuracy per track (F, U); accuracy on
    base rows with > 26 options; complement violation; option-order drift; the three primary endpoints with batch
    calibration; accuracy per task; accuracy on OHS-A and OHS-S (only with --half all); exact McNemar for micro
    accuracy against each Jev run. "Also reported" quantities, each Jev run's own numbers and the run-to-run
    agreement are descriptive (CI and raw p where they are differences, no adjustment).
  * Speed and cost are NOT defined in PREREG_OHS3.md and are not scored here; see
    prereg_drafts/speed_cost_definition.md.

Usage:
  python score_ohs3.py --model q35_4b_X_cal [--model ...] [--jev jev_guard,jev_r2_guard] [--split ohs3]
                       [--half all|A|S] [--boot 10000] [--bc-suffix _bc] [--out results_ohs3/score_ohs3_all.json]
  For --split ohs3 the frozen sha256 (PREREG_OHS3.md "Frozen files"), the PREREG row/pair counts and the two Jev runs
  are enforced; --allow-deviation turns those stops into recorded deviations (never use it for the reported run).
"""
from __future__ import annotations

import argparse
import hashlib
import json
import math
import sys
from collections import Counter, defaultdict
from fractions import Fraction
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve().parent
PINNED_JEV = "typesafe/jev-1.13-20260917"
FROZEN_OHS3 = {  # PREREG_OHS3.md, "Frozen files"
    "ohs3.jsonl": "68cb27da139010a9d9b00bfedc32e3ba8f1b963bf68c6cca85fd5e491868fd66",
    "ohs3_relations.jsonl": "c2e1dcee9ba40faea316140d423d5acf85644a6aa9af953ac5b0d95b3f5a04dc",
}
EXPECTED_OHS3 = {"rows": 2456, "base_rows": 1852, "tasks": 13, "groups": 1806, "yes_no_base": 716,
                 "choice_base": 1136, "over_26_base": 284, "neg_pairs": 300, "perm_pairs": 304}
TWIN_SUFFIXES = ("_neg", "_perm", "_dneg", "_para", "_yn")
ALPHA = 0.05
ACC_MARGIN_PP = 2.0      # "matches": CI lower bound above -2.0 percentage points (accuracy endpoints)
BRIER_MARGIN = 0.010     # "matches": CI lower bound above -0.010 (Brier, Jev minus OpenDecide)
WIDE = 26                # "more than 26 options"


# ---------------------------------------------------------------------------------------------- row-level rules
def _finite(x):
    try:
        v = float(x)
    except (TypeError, ValueError):
        return None
    return v if math.isfinite(v) else None


def p_yes(probs):
    """P(yes) of a yes/no answer, or None when the answer is missing (no record, no "yes" key, non-finite)."""
    if not isinstance(probs, dict):
        return None
    return _finite(probs.get("yes"))


def option_probs(row, probs):
    """{option: probability} over the row's options, by name (absent option = 0); None if missing/non-finite."""
    if not isinstance(probs, dict):
        return None
    out = {}
    for o in row["options"]:
        v = _finite(probs.get(o, 0.0))
        if v is None:
            return None
        out[o] = v
    return out


def decision(row, probs):
    """The predicted answer ("yes"/"no" or an option name), or None for a tie or a missing answer."""
    if row["qtype"] == "noul":
        p = p_yes(probs)
        if p is None or p == 0.5:
            return None
        return "yes" if p > 0.5 else "no"
    q = option_probs(row, probs)
    if not q:
        return None
    best = max(q.values())
    top = [o for o, v in q.items() if v == best]
    return top[0] if len(top) == 1 else None


def gold_label(row):
    return ("yes" if row["gold"] == 1 else "no") if row["qtype"] == "noul" else row["gold"]


def correct(row, probs):
    d = decision(row, probs)
    return float(d is not None and d == gold_label(row))


def brier(row, probs):
    p = p_yes(probs)
    return 1.0 if p is None else (p - row["gold"]) ** 2


def _dist(row, probs):
    q = option_probs(row, probs)
    if q is None:
        return None
    s = sum(q.values())
    return None if s <= 0 else {o: v / s for o, v in q.items()}


def complement_pair(ra, pa, rb, pb):
    """(violation 0/1, |P_a(yes) + P_b(yes) - 1|) for a complement pair; tie/missing = violation, missing |.| = 1."""
    da, db = decision(ra, pa), decision(rb, pb)
    viol = float(da is None or db is None or da == db)
    ya, yb = p_yes(pa), p_yes(pb)
    dev = 1.0 if ya is None or yb is None else abs(ya + yb - 1.0)
    return viol, dev


def perm_pair(ra, pa, rb, pb):
    """(drift 0/1, total-variation distance aligned by option name) for an option-order pair."""
    da, db = decision(ra, pa), decision(rb, pb)
    drift = float(da is None or db is None or da != db)
    qa, qb = _dist(ra, pa), _dist(rb, pb)
    if qa is None or qb is None:
        return drift, 1.0
    return drift, 0.5 * sum(abs(qa.get(o, 0.0) - qb.get(o, 0.0)) for o in set(qa) | set(qb))


# ---------------------------------------------------------------------------------------------- multiplicity / tests
def holm(pvals: dict) -> dict:
    """Holm step-down adjusted p-values."""
    items = sorted(pvals.items(), key=lambda kv: (kv[1], kv[0]))
    m, out, run = len(items), {}, 0.0
    for r, (k, p) in enumerate(items):
        run = max(run, min(1.0, (m - r) * p))
        out[k] = run
    return out


def bh(pvals: dict) -> dict:
    """Benjamini-Hochberg adjusted p-values (q-values)."""
    items = sorted(pvals.items(), key=lambda kv: (kv[1], kv[0]))
    m, out, run = len(items), {}, 1.0
    for r in range(m - 1, -1, -1):
        k, p = items[r]
        run = min(run, min(1.0, p * m / (r + 1)))
        out[k] = run
    return out


def mcnemar_exact(b: int, c: int) -> float:
    """Exact two-sided McNemar p (binomial, p = 0.5, on the b + c discordant pairs), computed with exact fractions."""
    n = b + c
    if n == 0:
        return 1.0
    tail = Fraction(sum(math.comb(n, i) for i in range(min(b, c) + 1)), 2 ** n)
    return float(min(Fraction(1), 2 * tail))


def boot_p(res) -> float:
    res = res[~np.isnan(res)]
    if not len(res):
        return float("nan")
    return float(min(1.0, 2 * min((res <= 0).mean(), (res >= 0).mean())))


def verdict_primary(lo, hi, p_adj, margin):
    """PREREG 'Beats' and 'matches': lo/hi/margin in the endpoint's reporting unit (pp for accuracy)."""
    beats = bool(lo > 0 and p_adj < ALPHA)
    matches = bool(beats or lo > -margin)
    label = "beats" if beats else "matches" if matches else "jev_better" if hi < 0 else "neither"
    return {"label": label, "beats": beats, "matches": matches, "ci_above_0": bool(lo > 0), "ci_below_0": bool(hi < 0)}


def verdict_secondary(lo, hi, q):
    if lo > 0 and q < ALPHA:
        return "od_better"
    if hi < 0 and q < ALPHA:
        return "jev_better"
    return "no_clear_difference"


# ---------------------------------------------------------------------------------------------- data
def load_jsonl(path):
    with open(path) as f:
        return [json.loads(l) for l in f if l.strip()]


def load_preds(path):
    """{row id: record}; the last record wins on a duplicate id (as score_ohs.py), duplicates are counted."""
    out, dup = {}, 0
    for r in load_jsonl(path):
        dup += r["id"] in out
        out[r["id"]] = r
    return out, dup


def sha256_file(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def is_twin(r):
    return r["id"].endswith(TWIN_SUFFIXES) or "variant_of" in (r.get("meta") or {})


class Bench:
    """Rows, base rows, scored pairs, tasks and groups of one split (optionally one half)."""

    def __init__(self, rows: list, rels: list, half: str = "all", strict_tasks: bool = True):
        if half != "all":
            rows = [r for r in rows if r["meta"]["half"] == half]
        self.half = half
        self.rows = {r["id"]: r for r in rows}
        if len(self.rows) != len(rows):
            raise SystemExit("duplicate row ids in the data file")
        self.base = [r["id"] for r in rows if not is_twin(r)]
        self.twins = [r["id"] for r in rows if is_twin(r)]
        tmap = defaultdict(set)
        for r in rows:
            tmap[r["source"]].add((r.get("meta") or {}).get("task") or r["source"])
        inv = defaultdict(set)
        for s, ts in tmap.items():
            for t in ts:
                inv[t].add(s)
        self.task_partition_ok = all(len(v) == 1 for v in tmap.values()) and all(len(v) == 1 for v in inv.values())
        if strict_tasks and not self.task_partition_ok:  # OHS-3: source == meta.task == the builder's TASK
            raise SystemExit("source and meta.task do not define the same task partition")
        self.neg_pairs, self.perm_pairs, self.unscored = [], [], Counter()
        for x in rels:
            a, b = x["a"], x["b"]
            if a not in self.rows or b not in self.rows:
                continue
            ra, rb = self.rows[a], self.rows[b]
            if ra["group_id"] != rb["group_id"]:
                raise SystemExit(f"pair {a} / {b} spans two groups: the cluster bootstrap would split it")
            if x["type"] == "complement" and ra["qtype"] == rb["qtype"] == "noul" and is_twin(rb) and not is_twin(ra):
                if rb["gold"] != 1 - ra["gold"]:
                    raise SystemExit(f"complement pair {a} / {b}: gold is not complementary")
                self.neg_pairs.append((a, b))
            elif x["type"] == "equiv" and ra["qtype"] == rb["qtype"] == "choice" and is_twin(rb) and not is_twin(ra):
                if rb["gold"] != ra["gold"] or sorted(rb["options"]) != sorted(ra["options"]):
                    raise SystemExit(f"option-order pair {a} / {b}: gold or option set differs")
                self.perm_pairs.append((a, b))
            else:  # OHS-1 style relations (paraphrase, double negation, base-base complements): not OHS-3 endpoints
                self.unscored[f"{x['type']}:{ra['qtype']}/{rb['qtype']}"] += 1
        self.task = {i: r["source"] for i, r in self.rows.items()}
        order = {}
        for i in self.base:  # group order = first appearance among base rows in file order (as score_ohs.py)
            order.setdefault(self.task[i], {}).setdefault(self.rows[i]["group_id"], None)
        for i in self.twins:
            if self.rows[i]["group_id"] not in order.get(self.task[i], {}):
                raise SystemExit(f"twin {i} has no base row in its group")
        self.task_groups = {t: list(g) for t, g in order.items()}
        self.tasks = sorted(self.task_groups)

    def counts(self):
        base = [self.rows[i] for i in self.base]
        return {"rows": len(self.rows), "base_rows": len(base), "tasks": len(self.tasks),
                "groups": sum(len(v) for v in self.task_groups.values()),
                "yes_no_base": sum(r["qtype"] == "noul" for r in base),
                "choice_base": sum(r["qtype"] == "choice" for r in base),
                "over_26_base": sum(r["qtype"] == "choice" and len(r["options"]) > WIDE for r in base),
                "neg_pairs": len(self.neg_pairs), "perm_pairs": len(self.perm_pairs)}


class Boot:
    """Paired cluster bootstrap over group_id, stratified by task; one draw serves every endpoint."""

    def __init__(self, bench: Bench, n_boot: int = 10000, seed: int = 0):
        self.tasks = bench.tasks
        self.blocks, self.index, off = [], {}, 0
        for t in self.tasks:
            gs = bench.task_groups[t]
            self.blocks.append(slice(off, off + len(gs)))
            for j, g in enumerate(gs):
                self.index[(t, g)] = off + j
            off += len(gs)
        self.G, self.n_boot = off, n_boot
        sizes = [len(bench.task_groups[t]) for t in self.tasks]
        assert max(sizes) < 65535
        rng = np.random.default_rng(seed)
        self.W = np.zeros((n_boot, off), dtype=np.uint16)
        for b in range(n_boot):
            for blk, n in zip(self.blocks, sizes):
                self.W[b, blk] = np.bincount(rng.integers(0, n, n), minlength=n)
        self.bench = bench

    def gvec(self, items):
        """items: iterable of (row id whose group gets the value, value) -> per-group sums (G,)."""
        v = np.zeros(self.G)
        for i, x in items:
            v[self.index[(self.bench.task[i], self.bench.rows[i]["group_id"])]] += x
        return v

    def task_sums(self, Q):
        """Q (G, K) -> observed per-task sums (T, K) and resampled per-task sums (B, T, K)."""
        T, K = len(self.blocks), Q.shape[1]
        obs = np.stack([Q[blk].sum(0) for blk in self.blocks])
        out = np.empty((self.n_boot, T, K))
        step = 2000
        for ti, blk in enumerate(self.blocks):
            for s in range(0, self.n_boot, step):
                out[s:s + step, ti] = self.W[s:s + step, blk].astype(np.float64) @ Q[blk]
        return obs, out


def ratio_endpoint(boot, num_od, num_jev, den, kind="micro", higher_better=True, scale=1.0):
    """OD and Jev ratios (micro: pooled; macro: unweighted mean over tasks present) and the paired difference with its
    bootstrap CI and p. Difference = OD - Jev when higher_better, else Jev - OD. Values multiplied by scale."""
    obs, bs = boot.task_sums(np.stack([num_od, num_jev, den], 1))
    present = obs[:, 2] > 0

    def stat(S):
        with np.errstate(invalid="ignore", divide="ignore"):
            if kind == "micro":
                n = S[..., 2].sum(-1)
                return S[..., 0].sum(-1) / n, S[..., 1].sum(-1) / n
            r = S[..., present, :]
            return (r[..., 0] / r[..., 2]).mean(-1), (r[..., 1] / r[..., 2]).mean(-1)

    def exact(S):
        """The same difference in exact rational arithmetic on the (float) resampled sums S (T, 3)."""
        F = [[Fraction(float(x)) for x in t] for t in S]
        if kind == "micro":
            n = sum(t[2] for t in F)
            if n == 0:
                return None
            d = (sum(t[0] for t in F) - sum(t[1] for t in F)) / n
        else:
            ts = [t for t, keep in zip(F, present) if keep]
            if any(t[2] == 0 for t in ts):
                return None
            d = sum((t[0] - t[1]) / t[2] for t in ts) / len(ts)
        return d if higher_better else -d

    od, jv = stat(obs)
    bod, bjv = stat(bs)
    diff = (od - jv) if higher_better else (jv - od)
    res = (bod - bjv) if higher_better else (bjv - bod)
    # A paired difference that is exactly 0 counts in both tails of p. The macro mean of per-task ratios is not exact in
    # floating point (1/60 - 1/60 + ... can come out as +-1e-17), so near-zero resamples are re-evaluated exactly.
    for r in np.flatnonzero(np.abs(res) < 1e-9):
        e = exact(bs[r])
        res[r] = np.nan if e is None else (0.0 if e == 0 else float(e))
    ok = res[~np.isnan(res)]
    lo, hi = (np.percentile(ok, [2.5, 97.5]) if len(ok) else (float("nan"), float("nan")))
    out = {"od": float(od) * scale, "jev": float(jv) * scale, "diff": float(diff) * scale,
           "ci95": [float(lo) * scale, float(hi) * scale], "p": boot_p(res), "n": int(round(obs[:, 2].sum()))}
    if len(ok) < len(res):
        out["n_resamples_undefined"] = int(len(res) - len(ok))
    return out


# ---------------------------------------------------------------------------------------------- scoring
def _probs(P, i):
    rec = P.get(i)
    return None if rec is None else rec.get("probs")


def sys_rows(bench, runs, fn, ids):
    """{id: mean over runs of fn(row, probs)} (a single OpenDecide run is a list of one)."""
    return {i: float(np.mean([fn(bench.rows[i], _probs(P, i)) for P in runs])) for i in ids}


def sys_pairs(bench, runs, fn, pairs):
    """[(base id, (mean over runs of each component of fn(...)))] for each pair."""
    out = []
    for a, b in pairs:
        vals = np.array([fn(bench.rows[a], _probs(P, a), bench.rows[b], _probs(P, b)) for P in runs], dtype=float)
        out.append((a, vals.mean(0)))
    return out


def plain_metrics(bench, runs):
    """Point values for one system (no bootstrap): used for each Jev run on its own."""
    base = bench.base
    acc = sys_rows(bench, runs, correct, base)
    yn = [i for i in base if bench.rows[i]["qtype"] == "noul"]
    br = sys_rows(bench, runs, brier, yn)
    per_task = defaultdict(list)
    for i in base:
        per_task[bench.task[i]].append(acc[i])
    out = {"micro_pct": 100 * float(np.mean(list(acc.values()))),
           "macro_pct": 100 * float(np.mean([np.mean(v) for v in per_task.values()])),
           "brier_yesno": float(np.mean(list(br.values()))) if yn else None}
    if bench.neg_pairs:
        cp = sys_pairs(bench, runs, complement_pair, bench.neg_pairs)
        out["complement_violation"] = float(np.mean([v[0] for _, v in cp]))
        out["complement_mean_abs_dev"] = float(np.mean([v[1] for _, v in cp]))
    if bench.perm_pairs:
        pp = sys_pairs(bench, runs, perm_pair, bench.perm_pairs)
        out["option_order_drift"] = float(np.mean([v[0] for _, v in pp]))
        out["option_order_tv"] = float(np.mean([v[1] for _, v in pp]))
    return out


def answer_report(bench, P):
    """Missing answers and ties of one prediction file, on base and twin rows."""
    rep = {"missing_base": 0, "missing_twin": 0, "tie_base": 0, "missing_base_by_task": Counter()}
    for i in bench.base:
        pr = _probs(P, i)
        if (p_yes(pr) if bench.rows[i]["qtype"] == "noul" else option_probs(bench.rows[i], pr)) is None:
            rep["missing_base"] += 1
            rep["missing_base_by_task"][bench.task[i]] += 1
        elif decision(bench.rows[i], pr) is None:
            rep["tie_base"] += 1
    for i in bench.twins:
        pr = _probs(P, i)
        if (p_yes(pr) if bench.rows[i]["qtype"] == "noul" else option_probs(bench.rows[i], pr)) is None:
            rep["missing_twin"] += 1
    rep["missing_base_by_task"] = dict(sorted(rep["missing_base_by_task"].items()))
    rep["extra_ids_not_in_data"] = sum(1 for i in P if i not in bench.rows)
    return rep


def primary_endpoints(bench, boot, od_runs, jev_runs):
    base = bench.base
    yn = [i for i in base if bench.rows[i]["qtype"] == "noul"]
    a_od, a_j = sys_rows(bench, od_runs, correct, base), sys_rows(bench, jev_runs, correct, base)
    b_od, b_j = sys_rows(bench, od_runs, brier, yn), sys_rows(bench, jev_runs, brier, yn)
    one = boot.gvec((i, 1.0) for i in base)
    num_od, num_j = boot.gvec(a_od.items()), boot.gvec(a_j.items())
    out = {"micro": ratio_endpoint(boot, num_od, num_j, one, "micro", True, 100.0),
           "macro": ratio_endpoint(boot, num_od, num_j, one, "macro", True, 100.0)}
    if yn:
        out["brier_yesno"] = ratio_endpoint(boot, boot.gvec(b_od.items()), boot.gvec(b_j.items()),
                                            boot.gvec((i, 1.0) for i in yn), "micro", False, 1.0)
    return out


def score_model(bench, boot, od_runs, jev_runs, bc_runs=None, jev_names=None):
    """All PREREG_OHS3 endpoints for one OpenDecide model (primary configuration od_runs, batch-cal bc_runs)."""
    rows, base = bench.rows, bench.base
    res = {"primary": primary_endpoints(bench, boot, od_runs, jev_runs)}
    pr = res["primary"]
    holm_p = holm({k: v["p"] for k, v in pr.items()})
    for k, v in pr.items():
        v["p_holm"] = holm_p[k]
        v["diff_definition"] = "Jev - OD (lower Brier is better)" if k == "brier_yesno" else "OD - Jev, pp"
        margin = BRIER_MARGIN if k == "brier_yesno" else ACC_MARGIN_PP
        v["verdict"] = verdict_primary(v["ci95"][0], v["ci95"][1], v["p_holm"], margin)

    # ---- secondary family
    sec = {}
    a_od, a_j = sys_rows(bench, od_runs, correct, base), sys_rows(bench, jev_runs, correct, base)

    def acc_on(ids):
        ids = list(ids)
        return ratio_endpoint(boot, boot.gvec((i, a_od[i]) for i in ids), boot.gvec((i, a_j[i]) for i in ids),
                              boot.gvec((i, 1.0) for i in ids), "micro", True, 100.0)

    for t in sorted({rows[i]["track"] for i in base}):
        sec[f"acc_track_{t}"] = acc_on(i for i in base if rows[i]["track"] == t)
    wide = [i for i in base if rows[i]["qtype"] == "choice" and len(rows[i]["options"]) > WIDE]
    if wide:
        sec["acc_over_26_options"] = acc_on(wide)
    desc = {}
    if bench.neg_pairs:
        c_od = sys_pairs(bench, od_runs, complement_pair, bench.neg_pairs)
        c_j = sys_pairs(bench, jev_runs, complement_pair, bench.neg_pairs)
        cnt = boot.gvec((a, 1.0) for a, _ in c_od)
        sec["complement_violation"] = ratio_endpoint(boot, boot.gvec((a, v[0]) for a, v in c_od),
                                                     boot.gvec((a, v[0]) for a, v in c_j), cnt, "micro", False, 1.0)
        desc["complement_mean_abs_dev"] = ratio_endpoint(boot, boot.gvec((a, v[1]) for a, v in c_od),
                                                         boot.gvec((a, v[1]) for a, v in c_j), cnt, "micro", False, 1.0)
        negs = [b for _, b in bench.neg_pairs]
        n_od, n_j = sys_rows(bench, od_runs, correct, negs), sys_rows(bench, jev_runs, correct, negs)
        desc["acc_neg_rows"] = ratio_endpoint(boot, boot.gvec(n_od.items()), boot.gvec(n_j.items()),
                                              boot.gvec((i, 1.0) for i in negs), "micro", True, 100.0)
    if bench.perm_pairs:
        p_od = sys_pairs(bench, od_runs, perm_pair, bench.perm_pairs)
        p_j = sys_pairs(bench, jev_runs, perm_pair, bench.perm_pairs)
        cnt = boot.gvec((a, 1.0) for a, _ in p_od)
        sec["option_order_drift"] = ratio_endpoint(boot, boot.gvec((a, v[0]) for a, v in p_od),
                                                   boot.gvec((a, v[0]) for a, v in p_j), cnt, "micro", False, 1.0)
        desc["option_order_tv"] = ratio_endpoint(boot, boot.gvec((a, v[1]) for a, v in p_od),
                                                 boot.gvec((a, v[1]) for a, v in p_j), cnt, "micro", False, 1.0)
        perms = [b for _, b in bench.perm_pairs]
        q_od, q_j = sys_rows(bench, od_runs, correct, perms), sys_rows(bench, jev_runs, correct, perms)
        desc["acc_perm_rows"] = ratio_endpoint(boot, boot.gvec(q_od.items()), boot.gvec(q_j.items()),
                                               boot.gvec((i, 1.0) for i in perms), "micro", True, 100.0)
    if bc_runs is not None:
        for k, v in primary_endpoints(bench, boot, bc_runs, jev_runs).items():
            sec[f"bc_{k}"] = v
    for t in bench.tasks:
        sec[f"acc_task_{t}"] = acc_on(i for i in base if bench.task[i] == t)
    if bench.half == "all":
        for h in ("A", "S"):
            ids = [i for i in base if rows[i]["meta"].get("half") == h]
            if ids:
                sec[f"acc_half_{h}"] = acc_on(ids)
    mc = {}
    jev_names = jev_names or [f"run{j}" for j in range(len(jev_runs))]
    for j, P in zip(jev_names, jev_runs):
        cj = sys_rows(bench, [P], correct, base)
        b = sum(1 for i in base if a_od[i] == 1 and cj[i] == 0)
        c = sum(1 for i in base if a_od[i] == 0 and cj[i] == 1)
        mc[j] = {"od_right_jev_wrong": b, "od_wrong_jev_right": c, "p": mcnemar_exact(b, c)}
    fam = {k: v["p"] for k, v in sec.items() if not math.isnan(v["p"])}
    fam.update({f"mcnemar_vs_{j}": v["p"] for j, v in mc.items()})
    q = bh(fam)
    for k, v in sec.items():
        v["q_bh"] = q.get(k)  # None when the endpoint is undefined (p is NaN): not in the family
        lower_better = k in ("complement_violation", "option_order_drift", "bc_brier_yesno")
        v["diff_definition"] = "Jev - OD (lower is better)" if lower_better else "OD - Jev, pp"
        if v["q_bh"] is None:
            v["verdict"] = "undefined"
        elif k.startswith("bc_"):  # the primary endpoints under batch calibration: the PREREG rule, with BH q
            margin = BRIER_MARGIN if k == "bc_brier_yesno" else ACC_MARGIN_PP
            v["verdict"] = verdict_primary(v["ci95"][0], v["ci95"][1], v["q_bh"], margin)
        else:
            v["verdict"] = verdict_secondary(v["ci95"][0], v["ci95"][1], v["q_bh"])
    for j, v in mc.items():
        v["q_bh"] = q[f"mcnemar_vs_{j}"]
        better = "od_better" if v["od_right_jev_wrong"] > v["od_wrong_jev_right"] else "jev_better"
        v["verdict"] = better if v["q_bh"] < ALPHA else "no_clear_difference"
    for k, v in desc.items():
        v["diff_definition"] = "OD - Jev, pp" if k.startswith("acc_") else "Jev - OD (lower is better)"
    res["secondary"] = sec
    res["mcnemar"] = {f"vs_{j}": v for j, v in mc.items()}
    res["secondary_family"] = sorted(fam)
    res["descriptive"] = desc
    res["od_answers"] = answer_report(bench, od_runs[0])
    if bc_runs is not None:
        res["od_bc_answers"] = answer_report(bench, bc_runs[0])
    return res


def jev_report(bench, jev_runs, names):
    out = {"runs": names, "per_run": {}}
    for n, P in zip(names, jev_runs):
        ids = Counter(rec.get("jev_model") for i, rec in P.items() if i in bench.rows)
        out["per_run"][n] = {**plain_metrics(bench, [P]), **answer_report(bench, P),
                             "model_ids": dict(ids),
                             "rows_not_pinned_model": sum(v for k, v in ids.items() if k != PINNED_JEV)}
    if len(jev_runs) == 2:
        P1, P2 = jev_runs
        d1 = {i: decision(bench.rows[i], _probs(P1, i)) for i in bench.base}
        d2 = {i: decision(bench.rows[i], _probs(P2, i)) for i in bench.base}
        c1, c2 = sys_rows(bench, [P1], correct, bench.base), sys_rows(bench, [P2], correct, bench.base)
        out["run_agreement"] = {
            "decision": float(np.mean([d1[i] is not None and d1[i] == d2[i] for i in bench.base])),
            "correctness": float(np.mean([c1[i] == c2[i] for i in bench.base])),
            "note": "decision = both runs give the same non-tie, non-missing answer; correctness = both right or "
                    "both wrong (score_ohs.py's 'jev_run_agreement')"}
    out["mean_of_runs"] = plain_metrics(bench, jev_runs)
    return out


# ---------------------------------------------------------------------------------------------- CLI
def _r(x, nd=4):
    if isinstance(x, float):
        return round(x, nd)
    if isinstance(x, dict):
        return {k: _r(v, nd) for k, v in x.items()}
    if isinstance(x, list):
        return [_r(v, nd) for v in x]
    return x


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--model", action="append", required=True, help="OpenDecide primary-configuration preds name")
    ap.add_argument("--jev", default="jev_guard,jev_r2_guard")
    ap.add_argument("--split", default="ohs3")
    ap.add_argument("--half", default="all", choices=["all", "A", "S"])
    ap.add_argument("--boot", type=int, default=10000)
    ap.add_argument("--seed", type=int, default=0)
    ap.add_argument("--bc-suffix", default="_bc", help="secondary configuration = preds <model><suffix> if present")
    ap.add_argument("--root", default=str(HERE), help="directory holding data/ and preds_<split>/ (tests)")
    ap.add_argument("--out", default=None)
    ap.add_argument("--allow-deviation", action="store_true",
                    help="record (instead of stopping on) frozen-hash / count / Jev-run deviations")
    a = ap.parse_args(argv)
    root = Path(a.root)
    deviations = []

    def stop(msg):
        if not a.allow_deviation:
            raise SystemExit(f"STOP: {msg} (use --allow-deviation only for non-reported runs)")
        deviations.append(msg)

    if a.boot != 10000:
        deviations.append(f"--boot {a.boot} (PREREG: 10,000)")
    if a.seed != 0:
        deviations.append(f"--seed {a.seed} (PREREG: default_rng(0))")
    dpath, rpath = root / f"data/{a.split}.jsonl", root / f"data/{a.split}_relations.jsonl"
    frozen = {}
    if a.split == "ohs3":
        for fn, want in FROZEN_OHS3.items():
            got = sha256_file(root / "data" / fn)
            frozen[fn] = got == want
            if got != want:
                stop(f"data/{fn} sha256 {got[:12]} != frozen {want[:12]}")
    rows = load_jsonl(dpath)
    rels = load_jsonl(rpath) if rpath.exists() else []
    bench = Bench(rows, rels, a.half, strict_tasks=a.split == "ohs3")
    counts = bench.counts()
    if a.split == "ohs3" and a.half == "all":
        bad = {k: (counts[k], v) for k, v in EXPECTED_OHS3.items() if counts[k] != v}
        if bad:
            stop(f"counts differ from PREREG_OHS3: {bad}")
    jev_names = [x for x in a.jev.split(",") if x]
    if a.split == "ohs3" and len(jev_names) != 2:
        stop(f"PREREG rule 3 needs the two Jev runs, got {jev_names}")
    pdir = root / f"preds_{a.split}"
    jev_runs, dups = [], {}
    for n in jev_names:
        P, d = load_preds(pdir / f"{n}.jsonl")  # a missing file is an error, never a silent drop
        jev_runs.append(P)
        dups[n] = d
    boot = Boot(bench, a.boot, a.seed)
    out = {"scorer": "score_ohs3.py", "prereg": "PREREG_OHS3.md", "split": a.split, "half": a.half,
           "n_boot": a.boot, "seed": a.seed, "data": {**counts, "unscored_relations": dict(bench.unscored),
                                                      "task_key": "source",
                                                      "source_equals_meta_task_partition": bench.task_partition_ok,
                                                      "frozen_sha256_ok": frozen or None},
           "deviations": deviations,
           "speed_cost": "not defined in PREREG_OHS3.md; not scored (see prereg_drafts/speed_cost_definition.md)",
           "jev": jev_report(bench, jev_runs, jev_names), "models": {}}
    for m in a.model:
        P, d = load_preds(pdir / f"{m}.jsonl")
        dups[m] = d
        bc_path = pdir / f"{m}{a.bc_suffix}.jsonl"
        bc = None
        if bc_path.exists():
            bc, dups[m + a.bc_suffix] = load_preds(bc_path)
        res = score_model(bench, boot, [P], jev_runs, [bc] if bc is not None else None, jev_names)
        res["config_primary"] = m
        res["config_bc"] = f"{m}{a.bc_suffix}" if bc is not None else None
        if bc is None:
            res["note"] = f"secondary configuration {m}{a.bc_suffix} not found: bc_* endpoints not scored"
        out["models"][m] = res
    out["duplicate_pred_ids"] = dups
    out = _r(out, 6)
    op = Path(a.out) if a.out else root / f"results_{a.split}" / f"score_ohs3_{a.half}.json"
    op.parent.mkdir(parents=True, exist_ok=True)
    op.write_text(json.dumps(out, indent=1))
    print_summary(out)
    print(f"wrote {op}")
    return out


def print_summary(out):
    d = out["data"]
    print(f"split {out['split']} half {out['half']}: {d['base_rows']} base rows, {d['tasks']} tasks, {d['groups']} "
          f"groups, {d['neg_pairs']} _neg pairs, {d['perm_pairs']} _perm pairs; boot {out['n_boot']}")
    if out["deviations"]:
        print("DEVIATIONS:", out["deviations"])
    J = out["jev"]
    for n, v in J["per_run"].items():
        print(f"  Jev run {n}: micro {v['micro_pct']:.2f} macro {v['macro_pct']:.2f} brier {v['brier_yesno']} "
              f"missing base {v['missing_base']} twin {v['missing_twin']} ties {v['tie_base']} "
              f"not-pinned rows {v['rows_not_pinned_model']}")
    if "run_agreement" in J:
        print(f"  Jev run-to-run agreement: decision {J['run_agreement']['decision']:.4f}, "
              f"correctness {J['run_agreement']['correctness']:.4f}")
    for m, r in out["models"].items():
        print(f"== {m}  (bc: {r['config_bc']})")
        for k, v in r["primary"].items():
            print(f"  PRIMARY {k:14s} OD {v['od']:8.4f} Jev {v['jev']:8.4f} diff {v['diff']:+8.4f} "
                  f"[{v['ci95'][0]:+.4f}, {v['ci95'][1]:+.4f}] p {v['p']:.4f} holm {v['p_holm']:.4f} "
                  f"-> {v['verdict']['label']}")
        for k, v in r["secondary"].items():
            lab = v["verdict"]["label"] if isinstance(v["verdict"], dict) else v["verdict"]
            q = "  n/a " if v["q_bh"] is None else f"{v['q_bh']:.4f}"
            print(f"  sec {k:30s} OD {v['od']:8.4f} Jev {v['jev']:8.4f} diff {v['diff']:+8.4f} "
                  f"[{v['ci95'][0]:+.4f}, {v['ci95'][1]:+.4f}] p {v['p']:.4f} q {q} -> {lab}")
        for k, v in r["mcnemar"].items():
            print(f"  sec mcnemar {k}: b={v['od_right_jev_wrong']} c={v['od_wrong_jev_right']} p {v['p']:.4f} "
                  f"q {v['q_bh']:.4f} -> {v['verdict']}")
        for k, v in r["descriptive"].items():
            print(f"  desc {k:29s} OD {v['od']:8.4f} Jev {v['jev']:8.4f} diff {v['diff']:+8.4f} "
                  f"[{v['ci95'][0]:+.4f}, {v['ci95'][1]:+.4f}] p {v['p']:.4f}")
        oa = r["od_answers"]
        print(f"  OD answers: missing base {oa['missing_base']} twin {oa['missing_twin']} ties {oa['tie_base']}")


if __name__ == "__main__":
    main()
