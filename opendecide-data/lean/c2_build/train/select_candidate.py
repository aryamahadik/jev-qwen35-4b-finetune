"""select_candidate.py: the pre-registered choice among the 18 grid candidates (PREREG A42-D 9.3-9.6). CPU only.

Score (9.3). S = the unweighted mean of three accuracies in points: the G-proxy, the R mixdev (program-family mixdev,
spec 7.1) and the pooled own-dev splits (4.4) of the new families that entered C2. With no new family in C2, S is the
mean of the first two ("own_dev" absent for EVERY candidate). Accuracy of a component = mean of item correctness.
Eligibility (9.4). A candidate must pass pre-gate (a)-(d) of spec 7.2 (D1-D6, D9, complement) and the G-proxy rule of
item 4.3 versus C1: the booleans below, one per check, all True. A missing or null value is NOT a pass.
Choice (9.5), in this order and nothing else:
  1. the final step (final_a10, alpha = 1.0) if it is eligible, unless the eligible candidate with the highest S has a paired
     95% CI of its S gain over the final step, clustered (items of one source document or complement pair = one cluster),
     10,000 resamples, seed 0, with lower bound > 0; then that candidate. If the highest-S candidate IS the final step: final.
  2. if the final step is not eligible: the eligible candidate with the highest S (no CI).
  3. if no candidate is eligible: NO CANDIDATE, the pre-gate fails (spec 7.2): no C2 look.
Ties in S go to the final step, then the larger alpha, then the order final < last3 < earlylate. Only the one best
candidate gets a CI (S of every candidate is reported, nothing else is searched). Freeze (9.6): the output records the
chosen adapter's sha256 and the grid sha256 (from merge_avg.py grid.json) for the next PREREG addendum; no Jev, OHS-4 or
OHS-AC file is read here.

Input: --reads DIR with <candidate>.json per candidate (names as merge_avg.py):
  {"candidate": "last3_a07",
   "items": {"gproxy": {"id": [...], "cluster": [...], "correct": [1,0,...]}, "rmixdev": {...}, "own_dev": {...}},
   "eligibility": {"a_learning": true, "b_transfer": true, "c1_D1": true, "c2_D2": true, "c3_D3": true, "c4_D4": true,
                   "c5_D5": true, "c6_D6": true, "c7_D9": true, "d_complement": true, "gproxy_rule_4_3": true}}
  select_candidate.py --reads DIR --grid DIR/grid.json --out chosen.json [--resamples 10000] [--seed 0]
"""
from __future__ import annotations

import argparse
import json
import sys
import time
from pathlib import Path

import numpy as np

_HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(_HERE.parent))
import waiver_a100 as wv  # noqa: E402   PREREG A100: the owner's waiver of check (b); inactive unless WAIVER_B_A100.json is valid

COMPONENTS = ("gproxy", "rmixdev", "own_dev")
ELIG_KEYS = ("a_learning", "b_transfer", "c1_D1", "c2_D2", "c3_D3", "c4_D4", "c5_D5", "c6_D6", "c7_D9", "d_complement",
             "gproxy_rule_4_3")
FINAL = "final_a10"
BASE_RANK = {"final": 0, "last3": 1, "earlylate": 2}
N_BOOT, SEED = 10_000, 0


def components_of(rec: dict) -> tuple:
    return tuple(c for c in COMPONENTS if c in (rec.get("items") or {}))


def acc(rec: dict, comp: str) -> float:
    return 100.0 * float(np.mean(rec["items"][comp]["correct"]))


def score(rec: dict, comps: tuple) -> float:
    return float(np.mean([acc(rec, c) for c in comps]))


def eligible(rec: dict, waived: tuple = ()) -> tuple:
    """(ok, blocking failures). `waived` (PREREG A100: only ("b_transfer",)) lets a check that FAILED (False) not block; a
    missing or null value is still not a pass. With waived == () this is the original function."""
    el = rec.get("eligibility") or {}
    bad = [k for k in ELIG_KEYS if el.get(k) is not True and not (k in waived and el.get(k) is False)]
    return not bad, bad


def paired_ci(cand: dict, ref: dict, comps: tuple, n_boot: int = N_BOOT, seed: int = SEED, chunk: int = 500) -> dict:
    """95% CI of S(cand) - S(ref): clusters resampled with replacement within each component, the same draw for both
    candidates (paired); S recomputed on every resample as the mean of the components' accuracies."""
    rng = np.random.default_rng(seed)
    gain = np.zeros(n_boot)
    for comp in comps:
        a, b = cand["items"][comp], ref["items"][comp]
        if list(a["id"]) != list(b["id"]) or list(a["cluster"]) != list(b["cluster"]):
            raise SystemExit(f"{comp}: candidate and final step are not read on the same items / clusters")
        labels, idx = np.unique(np.asarray([str(x) for x in a["cluster"]]), return_inverse=True)
        n_c = np.bincount(idx).astype(float)
        d_c = np.bincount(idx, weights=np.asarray(a["correct"], float) - np.asarray(b["correct"], float))
        C, parts = len(labels), []
        for lo in range(0, n_boot, chunk):
            m = min(chunk, n_boot - lo)
            counts = rng.multinomial(C, np.full(C, 1.0 / C), size=m).astype(float)     # (m, C) cluster draws
            parts.append(100.0 * (counts @ d_c) / (counts @ n_c))
        gain += np.concatenate(parts)
    gain /= len(comps)
    point = score(cand, comps) - score(ref, comps)
    return {"point_pt": round(point, 4), "lo": round(float(np.percentile(gain, 2.5)), 4),
            "hi": round(float(np.percentile(gain, 97.5)), 4), "resamples": n_boot, "seed": seed}


def sort_key(name: str, s: float) -> tuple:
    base, a = name.rsplit("_a", 1)
    return (-s, name != FINAL, -int(a), BASE_RANK.get(base, 9))


def choose(recs: dict, n_boot: int = N_BOOT, seed: int = SEED, waived: tuple = ()) -> dict:
    if FINAL not in recs:
        raise SystemExit(f"{FINAL} (the final step) is missing from the reads")
    sets = {components_of(r) for r in recs.values()}
    if len(sets) != 1 or not {"gproxy", "rmixdev"} <= set(next(iter(sets))):
        raise SystemExit(f"every candidate needs the same components incl. gproxy and rmixdev; got {sets}")
    comps = next(iter(sets))
    rows = {}
    for n, r in recs.items():
        ok, bad = eligible(r, waived)
        rows[n] = {"S": round(score(r, comps), 4), "components": {c: round(acc(r, c), 3) for c in comps},
                   "eligible": ok, "failed_checks": bad}
        if waived:                                    # PREREG A100: report every failed check, mark the waived ones
            el = r.get("eligibility") or {}
            rows[n]["failed_checks"] = [k for k in ELIG_KEYS if el.get(k) is not True]
            rows[n]["waived_failed"] = [k for k in waived if el.get(k) is False]
    out = {"components_in_S": list(comps), "candidates": rows, "rule": "A42-D 9.5"}
    if waived:
        out["waiver"] = {"record": "A100", "waived": list(waived), "banner": wv.BANNER,
                         "meaning": "check (b) still fails and is reported as failed, waived by the owner; every other check binds"}
    elig = sorted((n for n in rows if rows[n]["eligible"]), key=lambda n: sort_key(n, rows[n]["S"]))
    if not elig:
        return {**out, "chosen": None, "status": "NO CANDIDATE: no eligible candidate; the pre-gate fails (spec 7.2)"}
    best = elig[0]
    if not rows[FINAL]["eligible"]:
        return {**out, "chosen": best, "status": "final step not eligible: the eligible candidate with the highest S",
                "best_eligible": best}
    if best == FINAL:
        return {**out, "chosen": FINAL, "status": "final step is the highest-S eligible candidate", "best_eligible": best}
    ci = paired_ci(recs[best], recs[FINAL], comps, n_boot, seed)
    won = ci["lo"] > 0
    return {**out, "best_eligible": best, "ci_vs_final": ci, "chosen": best if won else FINAL,
            "status": ("CI lower bound > 0: the grid candidate replaces the final step" if won else
                       "CI lower bound <= 0: the final step stays (A42-D 9.5)")}


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--reads", required=True)
    ap.add_argument("--grid", required=True)
    ap.add_argument("--out", required=True)
    ap.add_argument("--candidate-out", default=None,
                    help="also write a CANDIDATE_C2.json that gate_c2.py accepts (name q35_4b_c2 + the chosen adapter sha256)")
    ap.add_argument("--resamples", type=int, default=N_BOOT)
    ap.add_argument("--seed", type=int, default=SEED)
    ap.add_argument("--root", default=str(wv.LEAN), help=argparse.SUPPRESS)
    a = ap.parse_args(argv)
    on, why = wv.waiver_active(Path(a.root))                      # PREREG A100; no record or a bad one = no waiver, as before
    waived = tuple(wv.WAIVED_ELIG_KEYS) if on else ()
    if on:
        print(wv.BANNER)
    elif why:
        print(f"note: {wv.RECORD} is present but not valid ({why}); no waiver applied", file=sys.stderr)
    grid = json.loads(Path(a.grid).read_text())
    names = [c["name"] for c in grid["candidates"]]
    recs = {}
    for n in names:
        p = Path(a.reads) / f"{n}.json"
        if p.exists():
            recs[n] = json.loads(p.read_text())
    missing = [n for n in names if n not in recs]
    if missing:
        raise SystemExit(f"reads missing for {missing}: all 18 candidates are read (A42-D 9.2)")
    res = choose(recs, a.resamples, a.seed, waived)
    sha = {c["name"]: c["adapter_sha256"] for c in grid["candidates"]}
    res.update({"grid_sha256": grid["grid_sha256"], "chosen_adapter_sha256": sha.get(res["chosen"]),
                "n_candidates": len(names)})
    Path(a.out).write_text(json.dumps(res, indent=2))
    if a.candidate_out and res["chosen"]:
        Path(a.candidate_out).write_text(json.dumps(
            {"name": "q35_4b_c2", "grid_candidate": res["chosen"], "adapter_sha256": res["chosen_adapter_sha256"],
             "grid_sha256": res["grid_sha256"], "rule": "PREREG A42-D 9.5", "written_unix": time.time()}, indent=2))
    print(json.dumps({k: res[k] for k in ("chosen", "status", "chosen_adapter_sha256")}))
    return 0 if res["chosen"] else 1


if __name__ == "__main__":
    sys.exit(main())
