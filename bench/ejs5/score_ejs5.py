"""Score ejs-5 runs exactly as the benchmark author scored Jev, and compare with Jev's published per-item answers.

  /Users/aryamahadik/Documents/jev/opendecide-data/.venv/bin/python bench/ejs5/score_ejs5.py c1_main500k [more runs]
  ... --check-published      only re-score the published models from public_raw.json (must equal public_summary.json)

Per row, our probabilities -> the author's answer space (ejs5lib.decide): route / triage argmax; size = expected level
over the 4 ordered levels, rounded and clamped like the author's jev_pred (LEVELS[max(0, min(3, int(round(E))))]);
risk 'yes' iff P(yes) >= 0.5. Accuracy per task = the author's own summarize() (taken from run_public_bench.py by
AST): hits / n, a row without a valid answer counts wrong. Overall = pooled over all rows (PRIMARY, PREREG_ejs5) and
the unweighted mean of the four tasks (secondary).

Comparison: paired bootstrap of (ours - Jev) over commits (a commit in several tasks carries all its rows), 10,000
resamples, numpy default_rng(seed 0). Jev's per-item answers are public_raw.json["<task>|jev"], counted correct only
when its pred is a valid label equal to the gold (summarize()). Also the rows whose commit is from 2026-06-01 on.
GPT-5.6 Terra and Claude Opus 5 are shown as published context (descriptive, no claim).

Prints aggregates only (accuracies, counts, intervals); never item text or labels.
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path

import ejs5lib as E


def load_published(src: Path):
    raw = json.loads((src / "public_raw.json").read_text())
    summ = json.loads((src / "public_summary.json").read_text())
    pub = {m: {t: {r["id"]: r for r in raw[f"{t}|{key}"]} for t in E.TASKS} for m, key in E.PUBLISHED.items()}
    acc = {(s["task"], s["model"]): s["accuracy"] for s in summ}
    return pub, acc


def author_rows(rows, task):
    """The author's row view for summarize(): only the label is used (valid label set)."""
    return [{"id": r["group_id"], "label": E.row_label(r)} for r in rows if r["meta"]["task"] == task]


def correct_vec(rows, recs_by_task):
    """0/1 per row (rows order): a valid pred equal to the label (summarize's hit)."""
    out = []
    for r in rows:
        t = r["meta"]["task"]
        rec = recs_by_task[t].get(r["group_id"])
        valid = recs_by_task["_valid"][t]
        p = rec.get("pred") if rec else None
        out.append(int(p in valid and p == E.row_label(r)))
    return out


def check_published(rows, src, summarize, quiet=False):
    """Re-score every published model with the author's summarize() and OUR gold: must equal public_summary.json.
    Also: the labels stored next to the published answers must equal our rows' gold (counts only)."""
    pub, acc = load_published(src)
    by_task = {t: [r for r in rows if r["meta"]["task"] == t] for t in E.TASKS}
    gold = {(r["meta"]["task"], r["group_id"]): E.row_label(r) for r in rows}
    mism = sum(1 for m in pub for t in E.TASKS for i, rec in pub[m][t].items() if gold.get((t, i)) != rec["label"])
    ok, n = 0, 0
    for m in pub:
        for t in E.TASKS:
            recs = [pub[m][t][r["group_id"]] for r in by_task[t]]
            recs = [{**x, "label": gold[(t, x["id"])]} for x in recs]
            s = summarize(E.PUBLISHED_SUMMARY_NAME[m], t, recs, author_rows(rows, t))
            want = acc.get((t, E.PUBLISHED_SUMMARY_NAME[m]))
            n += 1
            ok += want is not None and abs(s["accuracy"] - want) < 1e-12
    if not quiet:
        print(f"published check: {ok}/{n} (model x task) accuracies reproduced from public_raw.json with the author's "
              f"summarize(); stored labels that differ from our rows' gold: {mism}")
    if ok != n or mism:
        raise SystemExit("STOP: the scorer does not reproduce the published numbers")
    return pub, acc


def score_run(run_dir: Path, rows, rows_sha, summarize, pub, acc, B, seed):
    man = json.loads((run_dir / "manifest.json").read_text())
    if man.get("status") != "complete":
        raise SystemExit(f"{run_dir.name}: run not complete")
    if man.get("rows_sha256") != rows_sha:
        raise SystemExit(f"{run_dir.name}: read rows {str(man.get('rows_sha256'))[:16]}, the rows file is {rows_sha[:16]}")
    preds = {p["id"]: p for p in E.read_jsonl(run_dir / "preds.jsonl")}
    n_missing = sum(1 for r in rows if r["id"] not in preds)
    if n_missing and man.get("mode") in ("gpu", "cascade"):
        raise SystemExit(f"{run_dir.name}: {n_missing} rows have no record")
    rows = [r for r in rows if r["id"] in preds] if n_missing else rows  # CPU test runs (--limit) only
    tasks = [t for t in E.TASKS if any(r["meta"]["task"] == t for r in rows)]

    ours = {t: {} for t in E.TASKS}
    for r in rows:
        p = preds[r["id"]]
        pred, conf = E.decide(r, p.get("probs")) if p.get("probs") is not None else (None, None)
        ours[r["meta"]["task"]][r["group_id"]] = {"id": r["group_id"], "label": E.row_label(r), "pred": pred,
                                                   "confidence": conf, "latency_s": p.get("latency_s") or 0.0,
                                                   "error": p.get("error"), "cost": 0.0}
    valid = {t: E.valid_labels(rows, t) for t in E.TASKS}
    ours["_valid"] = valid
    per_task = {}
    for t in tasks:
        tr = [r for r in rows if r["meta"]["task"] == t]
        s = summarize(man["name"], t, [ours[t][r["group_id"]] for r in tr], author_rows(rows, t))
        hits = sum(1 for r in tr if ours[t][r["group_id"]]["pred"] == E.row_label(r))
        if abs(s["accuracy"] - hits / len(tr)) > 1e-12:
            raise SystemExit("internal: summarize() and the direct count disagree")
        per_task[t] = {"n": s["n"], "answered": s["answered"], "unanswered": s["unanswered"], "accuracy": s["accuracy"],
                       "calibration": s["calibration"]}
    a = correct_vec(rows, ours)
    units = [r["group_id"] for r in rows]
    res = {"name": man["name"], "mode": man.get("mode"), "readout": man.get("readout"), "n_rows": len(rows),
           "adapter_sha256": man.get("adapter_sha256"), "per_task": per_task,
           "overall_pooled": sum(a) / len(a), "overall_macro": sum(per_task[t]["accuracy"] for t in tasks) / len(tasks)}
    pubc = {}
    for m in E.PUBLISHED:
        recs = {t: pub[m][t] for t in E.TASKS}
        recs["_valid"] = valid
        pubc[m] = correct_vec(rows, recs)
    res["published_on_same_rows"] = {m: {"overall_pooled": sum(v) / len(v),
                                         "per_task": {t: sum(x for x, r in zip(v, rows) if r["meta"]["task"] == t)
                                                      / sum(1 for r in rows if r["meta"]["task"] == t) for t in tasks}}
                                     for m, v in pubc.items()}

    def comp(sel, ref):
        idx = [i for i, r in enumerate(rows) if sel(r)]
        if not idx:
            return None
        return E.paired_bootstrap([units[i] for i in idx], [a[i] for i in idx], [pubc[ref][i] for i in idx], B, seed)

    res["vs_jev"] = {"PRIMARY_overall_pooled": comp(lambda r: True, "jev"),
                     "per_task": {t: comp(lambda r, t=t: r["meta"]["task"] == t, "jev") for t in tasks},
                     "late_overall_pooled": comp(lambda r: r["meta"]["late"], "jev"),
                     "late_per_task": {t: comp(lambda r, t=t: r["meta"]["late"] and r["meta"]["task"] == t, "jev")
                                       for t in tasks}}
    prim = res["vs_jev"]["PRIMARY_overall_pooled"]
    res["vs_jev"]["PRIMARY_verdict"] = E.verdict(prim["ci95"])
    late = [i for i, r in enumerate(rows) if r["meta"]["late"]]
    res["late"] = {"n_rows": len(late), "n_commits": len({units[i] for i in late}),
                   "ours": sum(a[i] for i in late) / len(late) if late else None,
                   "jev": sum(pubc["jev"][i] for i in late) / len(late) if late else None}
    res["vs_context_descriptive"] = {m: comp(lambda r: True, m) for m in ("gpt", "opus")}
    tm = run_dir / "timing.json"
    if tm.exists():
        t = json.loads(tm.read_text())
        res["timing"] = {"latency_ms": t.get("latency_ms"), "device": t.get("device"), "errors": t.get("errors")}
    return res


def fmt_ci(c):
    if c is None:
        return "-"
    return f"{100 * c['diff']:+6.1f} [{100 * c['ci95'][0]:+5.1f}, {100 * c['ci95'][1]:+5.1f}] P>0 {c['p_better']:.2f}"


def print_run(res, acc):
    print(f"\n=== {res['name']} ({res['mode']}, readout {res['readout']}, {res['n_rows']} rows) ===")
    print(f"{'task':8s} {'n':>4s} {'ours':>6s} {'Jev':>6s} {'GPT':>6s} {'Opus':>6s}   ours - Jev, paired 95% CI (commits)")
    for t, s in res["per_task"].items():
        p = res["published_on_same_rows"]
        print(f"{E.TASK_TITLE[t]:8s} {s['n']:4d} {100 * s['accuracy']:5.1f}% {100 * p['jev']['per_task'][t]:5.1f}% "
              f"{100 * p['gpt']['per_task'][t]:5.1f}% {100 * p['opus']['per_task'][t]:5.1f}%   "
              f"{fmt_ci(res['vs_jev']['per_task'][t])}  (unanswered {s['unanswered']})")
    p = res["published_on_same_rows"]
    print(f"{'ALL':8s} {res['n_rows']:4d} {100 * res['overall_pooled']:5.1f}% {100 * p['jev']['overall_pooled']:5.1f}% "
          f"{100 * p['gpt']['overall_pooled']:5.1f}% {100 * p['opus']['overall_pooled']:5.1f}%   "
          f"{fmt_ci(res['vs_jev']['PRIMARY_overall_pooled'])}  <- PRIMARY (pooled)")
    jm = sum(p["jev"]["per_task"].values()) / len(p["jev"]["per_task"])
    print(f"macro (mean of tasks, secondary): ours {100 * res['overall_macro']:.1f}% vs Jev {100 * jm:.1f}%")
    L = res["late"]
    if L["n_rows"]:
        print(f"from {E.LATE_FROM} ({L['n_rows']} rows, {L['n_commits']} commits): ours {100 * L['ours']:.1f}% vs Jev "
              f"{100 * L['jev']:.1f}%   {fmt_ci(res['vs_jev']['late_overall_pooled'])}")
    print(f"PRIMARY verdict vs Jev: {res['vs_jev']['PRIMARY_verdict']}")
    for m in ("gpt", "opus"):
        print(f"context (descriptive, no claim) ours - {E.PUBLISHED[m]}: {fmt_ci(res['vs_context_descriptive'][m])}")
    if res.get("timing") and (res["timing"].get("latency_ms") or {}).get("p50") is not None:
        lt = res["timing"]["latency_ms"]
        print(f"model time per row ({res['timing']['device']}): p50 {lt['p50']:.1f} ms, p95 {lt['p95']:.1f} ms "
              "(prefill only, not an API round trip)")


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("runs", nargs="*", help="run names under --runs, or run dirs")
    ap.add_argument("--rows", default=str(E.ROWS))
    ap.add_argument("--src", default=str(E.QUAR), help="the benchmark folder (public_raw.json, run_public_bench.py)")
    ap.add_argument("--runs-dir", default=str(E.RUNS))
    ap.add_argument("--check-published", action="store_true", help="only the published-numbers check")
    ap.add_argument("--B", type=int, default=E.BOOT_B)
    ap.add_argument("--seed", type=int, default=E.BOOT_SEED)
    ap.add_argument("--json-out", default=None, help="write all results (aggregates only) here")
    a = ap.parse_args(argv)
    src = Path(a.src).resolve()
    rows_path = Path(a.rows).resolve()
    rows = E.read_jsonl(rows_path)
    rows_sha = E.sha256_file(rows_path)
    fns = E.author_functions(src / "run_public_bench.py")
    pub, acc = check_published(rows, src, fns["summarize"])
    if a.check_published:
        return None
    if (a.B, a.seed) != (E.BOOT_B, E.BOOT_SEED):
        print(f"NOTE: bootstrap B={a.B}, seed={a.seed} differ from PREREG_ejs5 (10000, 0)")
    out = {"rows_sha256": rows_sha, "run_public_bench_sha256": E.sha256_file(src / "run_public_bench.py"),
           "public_raw_sha256": E.sha256_file(src / "public_raw.json"), "B": a.B, "seed": a.seed, "runs": {}}
    for name in a.runs:
        d = Path(name) if Path(name).is_dir() else Path(a.runs_dir) / name
        res = score_run(d, rows, rows_sha, fns["summarize"], pub, acc, a.B, a.seed)
        print_run(res, acc)
        out["runs"][res["name"]] = res
    if a.json_out:
        E.write_json_atomic(Path(a.json_out), out)
        print(f"\nwrote {a.json_out}")
    return out


if __name__ == "__main__":
    main()
