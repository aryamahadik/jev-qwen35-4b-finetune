"""A8-prime (prereg_drafts/A8prime.md): every condition on C4 = q35_4b_main500k_fix2 other than the ship look, computed
exactly as written there. CPU, read-only. Nothing is written to logs/ship_looks.jsonl: none of these is a ship look
(4B-E, the REF, is not in any of them).

  python gate/fix2_conditions.py pairs                    [A8' 0a] write the frozen aff/dneg pair lists of the F7 probe
                                                          and devx (gate/fix2_pairs.json); refuses to overwrite a
                                                          different list. Run once, before any read of the probe.
  python gate/fix2_conditions.py probe-go C1P REFP        [A8' 0b] BEFORE LAUNCH: does the probe reproduce the failure?
                                                          C1's aff/dneg flip rate >= 4B-E's + 3 pp AND the paired
                                                          bootstrap lower bound of that difference > 0
  python gate/fix2_conditions.py c1parity C1R C1          [A8' R] the job-3 re-read of C1 reproduces its job-1 read
                                                          (PREREG_FINAL 4 parity bar, 9 gate splits)
  python gate/fix2_conditions.py precheck C4 C1R          [A8' P] held-out probe: C4's aff/dneg flips <= 0.5 x C1R's,
                                                          C4's probe accuracy >= C1R's on all probe rows AND on the
                                                          held-out probe rows (dev_kind holdout), both without the
                                                          frozen accuracy-excluded rows; devx: C4's accuracy >= C1R's
                                                          and C4's devx aff/dneg flips <= C1R's
  python gate/fix2_conditions.py noninf C4 C1R            [A8' N] non-inferiority vs C1 (same job) + (e) without the
                                                          hate pairs (see NONINF below)
  python gate/fix2_conditions.py all C4 C1R C1            R, then P, then N; stops at the first failure.
                                                          Exit 0 = C4 may get its one ship look; 1 = it may not.

Exit codes: 0 = pass, 1 = fail (a verdict; the JSON record is written), 2 = NO VERDICT: a pipeline problem (a non-od_gcp
read, mixed base / host / GPU / torch / CUDA / revision / chat template over the reads, ...) or a missing / incomplete
read. Exit 2 writes no JSON, so gate_4b_fix2_l4.sh's cond() stops the job without a record and the step is re-run after
a repair (A8-prime D / F: a pipeline problem decides nothing, PREREG_FINAL 3.4).

Accuracy-excluded probe rows (A8-prime F.P): every probe row of a ladder built from a real-text source row that the
probe source-label audit flagged (yn2b/f7_fix2_drops.json probe_report_only; yn2b/f7_source_label_audit.json 'probe').
`pairs` freezes the list into gate/fix2_pairs.json (accuracy_excluded_rows); P's accuracy comparisons leave those rows
out and report them separately; the flip counts keep every frozen pair (flips do not use gold).

Every subcommand takes --json OUT and --root (tests). Definitions are those of gate_dev.py (imported read-only):
answers = gate_dev.argmax_label (yes/no: P(yes) > 0.5), accuracy = gate_dev.score (ties wrong), flips = two rows of a
pair with different answers (gate_dev.relation_flips), calibrated Brier = gate_dev.crossfit, permutation flips =
gate_dev.perm_flips over the `_perm` reads, ASR = gate_dev.jagged_units / opi_units. A missing prediction stops the
tool (no verdict), as in the ship rule.

Which probe pairs count (fixed by `pairs`, before any read): `equiv` relations in data/<probe>_relations.jsonl whose
two rows are (i) the ladder's anchor (rung aff / R0, scoping depth 0) and (ii) a yes/no row of the same ladder whose
number of scoping negations is even and >= 2 (rung dneg / N2 / N4), not a distractor-only, rewrite or choice rung
(D / AR / CH). Either row may carry NON-scoping distractors: each one is program-verified to leave the gold unchanged
(F7 checklist 2.5, f7_precheck 2.2), so the pair is still "affirmative vs double negation"; the pure subset (no
distractor on either row) is listed and reported, never decisive (v2: 16 probe pairs, too few to decide on). The
fields rung / depth / n_distractor / dev_kind come from the F7 sidecar data/<split>_meta.jsonl when it exists (the
rows themselves carry only rung and dev_kind). Held out: rows with dev_kind "holdout" (the probe's held-out ladders)
or "devx" (the blind devx is held out as a whole); without any dev_kind field the whole file is held out (F7 v1).
The frozen list records the sha256 of the data, relations and sidecar files; any later change stops every step.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import math
import sys
from collections import Counter, defaultdict
from pathlib import Path

import numpy as np

LEAN = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(LEAN))
sys.path.insert(0, str(LEAN / "gate"))
import gate_dev as gd  # noqa: E402

ROOT = LEAN
SPLITS9 = gd.SPLITS.split(",")
PROBE, DEVX = "f7_probe", "f7_devx"
PAIRS_FILE = "gate/fix2_pairs.json"
DROPS_FILE = "yn2b/f7_fix2_drops.json"   # probe_report_only: the probe ladders the source-label audit flagged
PERM = "_perm"

# ---- pre-registered numbers (A8-prime) ------------------------------------------------------------------------------
GO_MIN_PP = 3.0          # 0b: C1 probe flip rate >= 4B-E's + 3 pp, and bootstrap LB > 0
P_CUT = 0.5              # P: C4 probe aff/dneg flips <= 0.5 x C1R's
# N (non-inferiority vs C1R + (e) without the hate pairs): its numbers and code live in gate/noninf_check.py
EPS = 1e-9

ANCHOR_RUNGS = {"aff", "R0"}
NON_PURE_RUNGS = {"D", "AR", "CH", "distractor", "rewrite", "para", "choice"}
RUNG_DEPTH = {"aff": 0, "R0": 0, "neg": 1, "N1": 1, "dneg": 2, "N2": 2, "N3": 3, "N4": 4}


class NoVerdict(Exception):
    """A pipeline problem: the step gives no verdict (exit 2, no JSON record)."""


def stop(msg):
    sys.exit(f"fix2_conditions: {msg}")


def no_verdict(issues):
    raise NoVerdict("; ".join(issues))


def pf(ok):
    return "PASS" if ok else "FAIL"


def _f(path):
    return ROOT / path


def read_jsonl(path):
    with open(path, encoding="utf-8") as f:
        return [json.loads(l) for l in f if l.strip()]


def sha256_file(p):
    h = hashlib.sha256()
    with open(p, "rb") as f:
        for b in iter(lambda: f.read(1 << 20), b""):
            h.update(b)
    return h.hexdigest()


# ------------------------------------------------------------------------------------------------ the frozen pair lists
HELD_KINDS = {"holdout", "devx"}


def field(r, k):
    """A row field: the F7 sidecar entry first (attached as r["_side"]), then the row, then its meta."""
    side = r.get("_side") or {}
    if k in side and side[k] is not None:
        return side[k]
    if k in r and r[k] is not None:
        return r[k]
    return (r.get("meta") or {}).get(k)


def rung_of(r):
    return field(r, "rung") or r.get("role")


def depth_of(r):
    d = field(r, "depth")
    if isinstance(d, int):
        return d
    return RUNG_DEPTH.get(rung_of(r))


def is_anchor(r):
    return rung_of(r) in ANCHOR_RUNGS and depth_of(r) == 0


def is_even_depth(r):
    """An even-depth (>= 2) rung that is not a distractor-only, rewrite or choice rung."""
    d = depth_of(r)
    return d is not None and d >= 2 and d % 2 == 0 and rung_of(r) not in NON_PURE_RUNGS


def has_distractor(r):
    nd = field(r, "n_distractor")
    return isinstance(nd, int) and nd > 0


def select_pairs(split):
    """(pairs [(a_id, b_id, unit)], info): the aff/dneg equiv pairs of data/<split>.jsonl (see the module text)."""
    dp, rp, mp = _f(f"data/{split}.jsonl"), _f(f"data/{split}_relations.jsonl"), _f(f"data/{split}_meta.jsonl")
    if not dp.exists():
        return None, {"file": str(dp.relative_to(ROOT)), "missing": True}
    rows = {r["id"]: r for r in read_jsonl(dp)}
    if mp.exists():
        side = {m["id"]: m for m in read_jsonl(mp)}
        if set(side) != set(rows):
            stop(f"data/{split}_meta.jsonl ids differ from data/{split}.jsonl")
        for i, r in rows.items():
            r["_side"] = side[i]
    has_kind = any(field(r, "dev_kind") is not None for r in rows.values())
    out, why, pure = [], Counter(), []
    if rp.exists():
        for rel in read_jsonl(rp):
            if rel.get("type") != "equiv":
                why["not equiv"] += 1
                continue
            a, b = rows.get(rel["a"]), rows.get(rel["b"])
            if a is None or b is None:
                why["row not in file"] += 1
                continue
            if is_anchor(b) and not is_anchor(a):
                a, b = b, a
            if not (is_anchor(a) and is_even_depth(b)):
                why["not anchor + even depth >= 2"] += 1
                continue
            if a["qtype"] != "noul" or b["qtype"] != "noul" or a.get("call_id") != b.get("call_id"):
                why["not two yes/no rows of one ladder"] += 1
                continue
            if has_kind and not (field(a, "dev_kind") in HELD_KINDS and field(b, "dev_kind") in HELD_KINDS):
                why["not held out (dev_kind holdout / devx)"] += 1
                continue
            out.append((a["id"], b["id"], a.get("group_id") or a.get("call_id")))
            if not has_distractor(a) and not has_distractor(b):
                pure.append([a["id"], b["id"]])
    info = {"file": str(dp.relative_to(ROOT)), "sha256": sha256_file(dp), "rows": len(rows),
            "relations_sha256": sha256_file(rp) if rp.exists() else None,
            "sidecar_sha256": sha256_file(mp) if mp.exists() else None, "holdout_rule": has_kind,
            "pairs": len(out), "units": len({u for _, _, u in out}), "excluded": dict(why),
            "depths": dict(Counter(depth_of(rows[b]) for _, b, _ in out)),
            "with_distractor": sum(1 for a_, b_, _ in out if has_distractor(rows[a_]) or has_distractor(rows[b_])),
            "pure_subset_report_only": pure}
    return out, info


def cmd_pairs(a):
    res = {"rule": "Which probe pairs count" + __doc__.split("Which probe pairs count")[1].rstrip(), "splits": {}}
    for sp in (a.probe, a.devx):
        if not _f(f"data/{sp}.jsonl").exists():
            stop(f"data/{sp}.jsonl missing: freeze the pairs only when the probe AND the blind devx both exist")
        pairs, info = select_pairs(sp)
        res["splits"][sp] = {**info, "list": [list(p) for p in pairs] if pairs is not None else None}
        print(f"{sp}: " + ("file missing" if pairs is None else
                           f"{info['pairs']} aff/dneg pairs in {info['units']} ladders (rows {info['rows']}, sha256 "
                           f"{info['sha256'][:16]}; depths {info['depths']}; excluded {info['excluded']})"))
    if res["splits"][a.probe]["list"] in (None, []):
        stop(f"no aff/dneg pairs in data/{a.probe}.jsonl: the probe is missing or has no qualifying pair")
    res["accuracy_excluded"] = accuracy_excluded_rows(a.probe)
    ex = res["accuracy_excluded"]
    print(f"{a.probe}: {len(ex['rows'])} rows of {len(ex['ladders'])} audit-flagged ladders are left out of P's accuracy "
          f"comparisons ({ex['source']})")
    out = _f(PAIRS_FILE)
    blob = (json.dumps(res, indent=1, sort_keys=True) + "\n").encode()
    if out.exists() and out.read_bytes() != blob:
        stop(f"{PAIRS_FILE} exists and differs: the pair lists are frozen before any read (never rewritten)")
    out.write_bytes(blob)
    print(f"wrote {PAIRS_FILE} (sha256 {hashlib.sha256(blob).hexdigest()})")
    return res


def accuracy_excluded_rows(split):
    """The probe rows P's accuracy comparisons leave out: every row of a ladder listed in the drops file's
    probe_report_only (the probe source-label audit). Frozen into the pair file by `pairs`."""
    p = _f(DROPS_FILE)
    if not p.exists():
        return {"source": f"{DROPS_FILE} (missing: no row excluded)", "sha256": None, "ladders": [], "rows": []}
    lads = set((json.loads(p.read_text()).get("probe_report_only") or {}))
    rows = [r for r in read_jsonl(_f(f"data/{split}.jsonl")) if (r.get("meta") or {}).get("latent_id") in lads]
    missing = sorted(lads - {(r.get("meta") or {}).get("latent_id") for r in rows})
    return {"source": DROPS_FILE + " probe_report_only", "sha256": sha256_file(p), "ladders": sorted(lads),
            "ladders_not_in_file": missing, "rows": sorted(r["id"] for r in rows)}


def frozen_excluded():
    """The frozen accuracy-excluded probe row ids (empty for a pair file frozen before this rule)."""
    fz = json.loads(_f(PAIRS_FILE).read_text())
    return set((fz.get("accuracy_excluded") or {}).get("rows") or [])


def frozen_pairs(split):
    """The frozen pair list of a split; stops when the data file changed after the freeze."""
    p = _f(PAIRS_FILE)
    if not p.exists():
        stop(f"{PAIRS_FILE} missing: run `python gate/fix2_conditions.py pairs` before any read of the probe")
    fz = json.loads(p.read_text())["splits"].get(split)
    if fz is None or fz.get("list") is None:
        return None, fz
    dp = _f(f"data/{split}.jsonl")
    if not dp.exists() or sha256_file(dp) != fz["sha256"]:
        stop(f"data/{split}.jsonl is missing or differs from the file whose pairs were frozen ({fz['sha256'][:16]})")
    for key, path in (("relations_sha256", _f(f"data/{split}_relations.jsonl")),
                      ("sidecar_sha256", _f(f"data/{split}_meta.jsonl"))):
        want = fz.get(key)
        if want is not None and (not path.exists() or sha256_file(path) != want):
            stop(f"{path.relative_to(ROOT)} is missing or differs from the file whose pairs were frozen ({want[:16]})")
    return [tuple(x) for x in fz["list"]], fz


# ------------------------------------------------------------------------------------------------ shared pieces
def preds_complete(split, names):
    """{name: {id: probs}} for every name on data/<split>.jsonl; stops on a missing file or row."""
    rows = read_jsonl(_f(f"data/{split}.jsonl"))
    out = {}
    for n in names:
        P = gd.load(split, n)
        if P is None:
            stop(f"preds_{split}/{n}.jsonl missing")
        miss = [r["id"] for r in rows if r["id"] not in P]
        if miss:
            stop(f"preds_{split}/{n}.jsonl lacks {len(miss)} of {len(rows)} rows (first {miss[0]}): must be complete")
        out[n] = P
    return rows, out


def answer(r, p):
    return gd.argmax_label(r, p)


def pair_flips(rows_by_id, P, pairs):
    """Per pair: 1.0 if the two rows get different answers."""
    return [float(answer(rows_by_id[a], P[a]) != answer(rows_by_id[b], P[b])) for a, b, _ in pairs]


def boot_diff(units, xs, ys, boots=gd.BOOTS, seed=gd.SEED):
    """Paired bootstrap over units of mean(xs) - mean(ys), in pp: (lo, hi)."""
    by = defaultdict(lambda: [0.0, 0.0, 0])
    for u, x, y in zip(units, xs, ys):
        g = by[u]
        g[0] += x; g[1] += y; g[2] += 1
    G = np.array(list(by.values()))
    rng = np.random.default_rng(seed)
    bs = np.empty(boots)
    for k in range(boots):
        s = G[rng.integers(0, len(G), len(G))]
        bs[k] = (s[:, 0].sum() - s[:, 1].sum()) / s[:, 2].sum() * 100
    lo, hi = np.percentile(bs, [2.5, 97.5])
    return float(lo), float(hi)


def extra_reads(splits):
    return [(sp, f"preds_{sp}", "", None, "dev") for sp in splits]


# ------------------------------------------------------------------------------------------------ 0b: probe go rule
def cmd_probe_go(a):
    pairs, fz = frozen_pairs(a.probe)
    if not pairs:
        stop(f"no frozen aff/dneg pairs for {a.probe}")
    rows, P = preds_complete(a.probe, [a.c1, a.ref])
    by = {r["id"]: r for r in rows}
    fc, fr = pair_flips(by, P[a.c1], pairs), pair_flips(by, P[a.ref], pairs)
    n = len(pairs)
    rc, rr = 100 * sum(fc) / n, 100 * sum(fr) / n
    lo, hi = boot_diff([u for _, _, u in pairs], fc, fr)
    issues, _ = gd.pipeline_check([a.c1, a.ref], extra_reads([a.probe]))
    ok = bool(rc - rr >= GO_MIN_PP - EPS and lo > 0)
    res = {"step": "0b probe-go", "c1": a.c1, "ref": a.ref, "probe": a.probe, "pairs": n, "units": len({u for *_, u in pairs}),
           "c1_flips": int(sum(fc)), "ref_flips": int(sum(fr)), "c1_rate": rc, "ref_rate": rr, "diff_pp": rc - rr,
           "lo": lo, "hi": hi, "min_pp": GO_MIN_PP, "pass": ok, "pipeline_issues": issues,
           "report_accuracy": {n_: 100 * sum(gd.score(r, P[n_][r["id"]])[0] for r in rows) / len(rows) for n_ in (a.c1, a.ref)}}
    print(f"[0b] PROBE GO RULE ({a.probe}, {n} aff/dneg pairs in {res['units']} ladders): {pf(ok)}")
    print(f"     C1 {a.c1}: {res['c1_flips']} flips ({rc:.2f}%); 4B-E {a.ref}: {res['ref_flips']} flips ({rr:.2f}%); "
          f"diff {rc - rr:+.2f} pp [{lo:+.2f}, {hi:+.2f}] (needs >= +{GO_MIN_PP:.1f} and LB > 0)")
    print(f"     report only: probe accuracy {', '.join(f'{k} {v:.2f}' for k, v in res['report_accuracy'].items())}")
    if issues:
        print("     PIPELINE (no verdict: repair, then re-run the step):\n       " + "\n       ".join(issues))
        no_verdict(issues)
    return res


# ------------------------------------------------------------------------------------------------ R: C1 re-read parity
def cmd_c1parity(a):
    rows = gd.complete_rows(SPLITS9, a.c1r, a.c1)
    n = len(rows)
    agree = dps = 0.0
    mx = 0.0
    for x in rows:
        keys = ["yes", "no"] if x["qtype"] == "noul" else x["options"]
        dp = max(abs(float(x["p_c"].get(k, 0.0)) - float(x["p_r"].get(k, 0.0))) for k in keys)
        agree += answer(x, x["p_c"]) == answer(x, x["p_r"])
        dps += dp
        mx = max(mx, dp)
    pt = gd.point(rows)
    checks = [("argmax agreement >= 99%", 100 * agree / n >= gd.PARITY_MIN_AGREE - EPS, f"{100 * agree / n:.2f}%"),
              ("mean |dp| <= 0.005", dps / n <= gd.PARITY_MAX_MEAN_DP + 1e-12, f"{dps / n:.5f}"),
              ("max |dp| <= 0.05", mx <= gd.PARITY_MAX_DP + 1e-12, f"{mx:.4f}"),
              ("accuracy within 0.3 pp", abs(pt["diff"]) <= gd.PARITY_MAX_ACC + EPS, f"{pt['cand']:.2f} vs {pt['ref']:.2f}")]
    issues, _ = gd.pipeline_check([a.c1r], gd.std_reads(SPLITS9, attacks=False))
    if issues:
        print("     PIPELINE (no verdict: repair, then re-run the step):\n       " + "\n       ".join(issues))
        no_verdict(issues)
    ok = all(c[1] for c in checks)
    res = {"step": "R c1parity", "c1r": a.c1r, "c1": a.c1, "n": n, "checks": [{"name": c, "pass": bool(o), "value": v}
                                                                               for c, o, v in checks],
           "pipeline_issues": issues, "pass": ok}
    print(f"[R] C1 RE-READ PARITY: {a.c1r} (job 3) vs {a.c1} (job 1), {n} rows: {pf(ok)}")
    for c, o, v in checks:
        print(f"     [{pf(o)}] {c}: {v}")
    if issues:
        print("     PIPELINE:\n       " + "\n       ".join(issues))
    return res


# ------------------------------------------------------------------------------------------------ P: pre-check
def cmd_precheck(a):
    out = {"step": "P precheck", "c4": a.c4, "c1r": a.c1r, "parts": {}}
    ok_all = True
    # probe (held out)
    pairs, fz = frozen_pairs(a.probe)
    if not pairs:
        stop(f"no frozen aff/dneg pairs for {a.probe}")
    rows, P = preds_complete(a.probe, [a.c4, a.c1r])
    reads = extra_reads([a.probe, a.devx]) + gd.std_reads(SPLITS9) + gd.perm_reads(SPLITS9, PERM)
    issues, _ = gd.pipeline_check([a.c4, a.c1r], reads)
    out["pipeline_issues"] = issues
    if issues:
        print("     PIPELINE (no verdict: one clean od_gcp predict job is required; repair, then re-run P):\n       "
              + "\n       ".join(issues))
        no_verdict(issues)
    by = {r["id"]: r for r in rows}
    f4, f1 = pair_flips(by, P[a.c4], pairs), pair_flips(by, P[a.c1r], pairs)
    k4, k1 = int(sum(f4)), int(sum(f1))
    excl = frozen_excluded()
    if excl - set(by):
        stop(f"{len(excl - set(by))} frozen accuracy-excluded rows are not in data/{a.probe}.jsonl")

    def acc(name, rs):
        return 100 * sum(gd.score(r, P[name][r["id"]])[0] for r in rs) / len(rs) if rs else float("nan")
    kept = [r for r in rows if r["id"] not in excl]
    has_kind = any(field(x, "dev_kind") is not None for x in rows)   # no dev_kind at all: the whole file is held out
    held = [r for r in kept if not has_kind or field(r, "dev_kind") in HELD_KINDS]
    held_ids = {r["id"] for r in held}
    iid = [r for r in kept if r["id"] not in held_ids]
    acc4, acc1 = acc(a.c4, kept), acc(a.c1r, kept)
    h4, h1 = acc(a.c4, held), acc(a.c1r, held)
    flip_ok = k4 <= P_CUT * k1 + EPS
    acc_ok = acc4 >= acc1 - EPS
    hacc_ok = bool(held) and h4 >= h1 - EPS
    out["parts"]["probe"] = {"pairs": len(pairs), "c4_flips": k4, "c1r_flips": k1, "c4_rate": 100 * k4 / len(pairs),
                             "c1r_rate": 100 * k1 / len(pairs), "flip_pass": flip_ok, "rows": len(rows),
                             "accuracy_rows": len(kept), "accuracy_excluded_rows": len(excl),
                             "c4_acc": acc4, "c1r_acc": acc1, "acc_pass": acc_ok,
                             "holdout_rows": len(held), "c4_acc_holdout": h4, "c1r_acc_holdout": h1,
                             "acc_holdout_pass": hacc_ok,
                             "report_only": {"iid_rows": len(iid), "c4_acc_iid": acc(a.c4, iid),
                                             "c1r_acc_iid": acc(a.c1r, iid),
                                             "c4_acc_all_rows": acc(a.c4, rows), "c1r_acc_all_rows": acc(a.c1r, rows),
                                             "c4_acc_excluded_rows": acc(a.c4, [by[i] for i in sorted(excl)]),
                                             "c1r_acc_excluded_rows": acc(a.c1r, [by[i] for i in sorted(excl)])}}
    print(f"[P] PRE-CHECK on the held-out F7 probe ({a.probe}, {len(pairs)} aff/dneg pairs, {len(rows)} rows, "
          f"{len(excl)} audit-flagged rows left out of the accuracy bars)")
    print(f"     [{pf(flip_ok)}] aff/dneg flips C4 {k4} ({100 * k4 / len(pairs):.2f}%) <= {P_CUT} x C1R {k1} "
          f"({100 * k1 / len(pairs):.2f}%) = {P_CUT * k1:.1f}")
    print(f"     [{pf(acc_ok)}] probe accuracy ({len(kept)} rows) C4 {acc4:.2f} >= C1R {acc1:.2f}")
    print(f"     [{pf(hacc_ok)}] held-out probe accuracy ({len(held)} rows) C4 {h4:.2f} >= C1R {h1:.2f}")
    rep = out["parts"]["probe"]["report_only"]
    print(f"     report only: iid ({len(iid)} rows) C4 {rep['c4_acc_iid']:.2f} vs C1R {rep['c1r_acc_iid']:.2f}; all "
          f"{len(rows)} rows C4 {rep['c4_acc_all_rows']:.2f} vs C1R {rep['c1r_acc_all_rows']:.2f}")
    ok_all &= flip_ok and acc_ok and hacc_ok
    # devx (blind-written)
    dpairs, dfz = frozen_pairs(a.devx)
    if not _f(f"data/{a.devx}.jsonl").exists() or dfz is None or dfz.get("missing"):
        stop(f"data/{a.devx}.jsonl missing (or not frozen in {PAIRS_FILE}): A8-prime needs the blind devx")
    drows, D = preds_complete(a.devx, [a.c4, a.c1r])
    dby = {r["id"]: r for r in drows}
    d4 = 100 * sum(gd.score(r, D[a.c4][r["id"]])[0] for r in drows) / len(drows)
    d1 = 100 * sum(gd.score(r, D[a.c1r][r["id"]])[0] for r in drows) / len(drows)
    dacc_ok = d4 >= d1 - EPS
    part = {"rows": len(drows), "c4_acc": d4, "c1r_acc": d1, "acc_pass": dacc_ok}
    print(f"[P] PRE-CHECK on devx ({a.devx}, {len(drows)} blind-written rows)")
    print(f"     [{pf(dacc_ok)}] accuracy C4 {d4:.2f} >= C1R {d1:.2f}")
    dflip_ok = True
    if dpairs:
        g4, g1 = int(sum(pair_flips(dby, D[a.c4], dpairs))), int(sum(pair_flips(dby, D[a.c1r], dpairs)))
        dflip_ok = g4 <= g1
        part.update({"pairs": len(dpairs), "c4_flips": g4, "c1r_flips": g1, "flip_pass": dflip_ok})
        print(f"     [{pf(dflip_ok)}] aff/dneg flips C4 {g4} <= C1R {g1} ({len(dpairs)} pairs)")
    else:
        part.update({"pairs": 0, "flip_pass": None})
        print("     devx has no aff/dneg pairs: the devx flip part does not apply (accuracy only)")
    out["parts"]["devx"] = part
    ok_all &= dacc_ok and dflip_ok
    out["pass"] = bool(ok_all)
    print(f"[P] RESULT: {pf(out['pass'])}")
    return out


# ------------------------------------------------------------------------------------------------ N: non-inferiority
def cmd_noninf(a):
    """Step N lives in gate/noninf_check.py (the job-3 entry point and its tests); this subcommand runs the same code."""
    import noninf_check as nc
    nc.gd.ROOT = gd.ROOT
    return nc.run(a.c4, a.c1r)


def cmd_all(a):
    out = {"step": "all", "c4": a.c4, "c1r": a.c1r, "c1": a.c1, "results": []}
    for fn, ns in ((cmd_c1parity, argparse.Namespace(c1r=a.c1r, c1=a.c1)),
                   (cmd_precheck, argparse.Namespace(c4=a.c4, c1r=a.c1r, probe=a.probe, devx=a.devx)),
                   (cmd_noninf, argparse.Namespace(c4=a.c4, c1r=a.c1r))):
        r = fn(ns)
        out["results"].append(r)
        if not r["pass"]:
            out["pass"] = False
            out["stopped_at"] = r["step"]
            print(f"\nA8-prime: {r['step']} FAILED -> no ship look for {a.c4}; fallback per A8-prime (4B-E, PREREG 5.7)")
            return out
    out["pass"] = True
    print(f"\nA8-prime: R, P and N PASS -> {a.c4} may get its one ship look vs the fresh 4B-E read")
    return out


def main(argv=None):
    global ROOT
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    sub = ap.add_subparsers(dest="cmd", required=True)
    ps = {"pairs": sub.add_parser("pairs"), "probe-go": sub.add_parser("probe-go"), "c1parity": sub.add_parser("c1parity"),
          "precheck": sub.add_parser("precheck"), "noninf": sub.add_parser("noninf"), "all": sub.add_parser("all")}
    ps["probe-go"].add_argument("c1")
    ps["probe-go"].add_argument("ref")
    ps["c1parity"].add_argument("c1r")
    ps["c1parity"].add_argument("c1")
    for k in ("precheck", "noninf", "all"):
        ps[k].add_argument("c4")
        ps[k].add_argument("c1r")
    ps["all"].add_argument("c1")
    for p in ps.values():
        p.add_argument("--probe", default=PROBE)
        p.add_argument("--devx", default=DEVX)
        p.add_argument("--json", default=None)
        p.add_argument("--root", default=None, help=argparse.SUPPRESS)
    a = ap.parse_args(argv)
    if a.root:
        ROOT = Path(a.root).resolve()
        gd.ROOT = ROOT
    gd._MODE = "fix2_conditions"
    fn = {"pairs": cmd_pairs, "probe-go": cmd_probe_go, "c1parity": cmd_c1parity, "precheck": cmd_precheck,
          "noninf": cmd_noninf, "all": cmd_all}[a.cmd]
    res = fn(a)
    if a.json:
        Path(a.json).parent.mkdir(parents=True, exist_ok=True)
        Path(a.json).write_text(json.dumps(gd._clean(res), indent=2) + "\n")
    return res


if __name__ == "__main__":
    try:
        r = main()
    except Exception as e:  # NoVerdict here or in noninf_check (step N through `noninf` / `all`)
        if type(e).__name__ != "NoVerdict":
            raise
        print(f"fix2_conditions: NO VERDICT (pipeline problem; nothing recorded): {e}")
        sys.exit(2)
    except SystemExit as e:   # stop(): a missing / incomplete read or file -> no verdict either
        if e.code not in (0, 1, None):
            print(e.code if isinstance(e.code, str) else f"fix2_conditions: stopped ({e.code})", file=sys.stderr)
            sys.exit(2)
        raise
    sys.exit(0 if (r or {}).get("pass", True) else 1)
