"""Shared code for the ejs-5 kit (github.com/ejs-5/jev-benchmark: Route / Triage / Size / Risk, 868 rows from n8n).

Blind by construction: nothing in this kit prints item text (commit prose) or gold labels. Scripts print counts,
file hashes, timings and aggregate numbers only. The benchmark files stay in bench/external_quarantine/ejs5/
(git-ignored).

Exactness: the task specs (question, criteria, level names) and the author's own decision / scoring functions are
taken from run_public_bench.py by AST (never imported: its module top reads OPENROUTER_API_KEY and it is an API
runner). `decide` below is our model's readout -> the author's answer space; tests/test_ejs5.py checks it against the
author's own `jev_pred` (rounding, clamping, the 0.5 cut) and the author's `summarize` (accuracy, no-answer = wrong).
"""
from __future__ import annotations

import ast
import hashlib
import json
import os
import statistics
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent.parent  # the jev repo on the Mac, the home directory on the VM (~/bench/ejs5)
QUAR = ROOT / "bench" / "external_quarantine" / "ejs5"
ROWS = QUAR / "ejs5_rows.jsonl"
RUNS = HERE / "runs"
TASKS = ("route", "triage", "score", "gate")  # run_public_bench.py's task keys, in its order
TASK_TITLE = {"route": "Route", "triage": "Triage", "score": "Size", "gate": "Risk"}  # the README's names
PUBLISHED = {"jev": "jev", "gpt": "openai/gpt-5.6-terra", "opus": "anthropic/claude-opus-5"}  # public_raw.json keys
PUBLISHED_SUMMARY_NAME = {"jev": "typesafe/jev-1.13", "gpt": "openai/gpt-5.6-terra", "opus": "anthropic/claude-opus-5"}
LATE_FROM = "2026-06-01"  # commit_dates.json: rows whose commit date is on or after this day (268 rows)
BOOT_B, BOOT_SEED = 10_000, 0


# ------------------------------------------------------------------ files

def sha256_file(p) -> str | None:
    try:
        h = hashlib.sha256()
        with open(p, "rb") as f:
            for b in iter(lambda: f.read(1 << 20), b""):
                h.update(b)
        return h.hexdigest()
    except OSError:
        return None


def read_jsonl(p):
    with open(p, encoding="utf-8") as f:
        return [json.loads(line) for line in f if line.strip()]


def write_jsonl_atomic(p, recs):
    p = Path(p)
    tmp = p.with_name(p.name + ".tmp")
    with open(tmp, "w", encoding="utf-8") as f:
        for r in recs:
            f.write(json.dumps(r, ensure_ascii=False) + "\n")
    os.replace(tmp, p)


def write_json_atomic(p, obj):
    p = Path(p)
    tmp = p.with_name(p.name + ".tmp")
    tmp.write_text(json.dumps(obj, indent=2))
    os.replace(tmp, p)


# ------------------------------------------------------------------ the author's code, by AST

def _assigns(tree, names):
    out = {}
    for node in tree.body:
        if isinstance(node, ast.Assign) and len(node.targets) == 1 and isinstance(node.targets[0], ast.Name) \
                and node.targets[0].id in names:
            out[node.targets[0].id] = ast.literal_eval(node.value)
    return out


def bench_spec(code_path) -> dict:
    """TASKS and LEVELS exactly as run_public_bench.py defines them (literal values, read by AST), + its sha256."""
    src = Path(code_path).read_text(encoding="utf-8")
    vals = _assigns(ast.parse(src), {"TASKS", "LEVELS"})
    missing = {"TASKS", "LEVELS"} - set(vals)
    if missing:
        raise SystemExit(f"{code_path}: could not read {sorted(missing)} as literals")
    if tuple(vals["TASKS"]) != TASKS:
        raise SystemExit(f"{code_path}: tasks {list(vals['TASKS'])} != expected {list(TASKS)}")
    return {"TASKS": vals["TASKS"], "LEVELS": vals["LEVELS"], "sha256": sha256_file(code_path)}


def author_functions(code_path, names=("jev_pred", "summarize")) -> dict:
    """The author's own functions, compiled from run_public_bench.py's source (no import, no API key, no calls)."""
    src = Path(code_path).read_text(encoding="utf-8")
    tree = ast.parse(src)
    consts = _assigns(tree, {"LEVELS"})
    ns = {"st": statistics, **consts}
    body = [n for n in tree.body if isinstance(n, ast.FunctionDef) and n.name in names]
    if {n.name for n in body} != set(names):
        raise SystemExit(f"{code_path}: functions {sorted(set(names) - {n.name for n in body})} not found")
    mod = ast.Module(body=body, type_ignores=[])
    exec(compile(mod, str(code_path), "exec"), ns)  # noqa: S102 (the benchmark author's published code, pure functions)
    return {k: ns[k] for k in names}


# ------------------------------------------------------------------ rows

def row_label(row) -> str:
    """The author's label string for a row (choice / size: the option; risk: 'yes' / 'no')."""
    if row["qtype"] == "noul":
        return "yes" if row["gold"] == 1 else "no"
    return row["gold"]


def valid_labels(rows, task) -> set:
    """summarize(): valid = {r["label"] for r in rows} (the labels present in that task)."""
    return {row_label(r) for r in rows if r["meta"]["task"] == task}


def model_row(row) -> dict:
    """What the model is given: no gold, no meta beyond ids (the readout never sees a label)."""
    return {k: row[k] for k in ("id", "group_id", "call_id", "state", "instructions", "qtype", "options", "card")
            if k in row}


# ------------------------------------------------------------------ readout -> the author's answer space

def norm_probs(row, probs):
    keys = ["yes", "no"] if row["qtype"] == "noul" else list(row["options"])
    p = [float(probs.get(k, 0.0)) for k in keys]
    s = sum(p)
    if not s > 0:
        raise ValueError(f"row {row['id']}: probabilities sum to {s}")
    return keys, [x / s for x in p]


def decide(row, probs):
    """(pred, confidence) in the author's label space, from our probabilities (T = 1, one read):
      choice (route, triage): argmax (the first option on an exact tie);
      score  (size): expected level E = sum_i i * p_i over the 4 ordered levels, then the author's jev_pred rule
                     LEVELS[max(0, min(3, int(round(E))))] (Python round);
      noul   (risk): 'yes' iff P(yes) >= 0.5, confidence abs(P(yes) - 0.5) * 2 (the author's jev_pred rule).
    probs None (no answer) -> (None, None): counted wrong by summarize()."""
    if probs is None:
        return None, None
    kind = row["meta"]["kind"]
    keys, ps = norm_probs(row, probs)
    if kind == "noul":
        n = ps[0]
        return ("yes" if n >= .5 else "no"), abs(n - .5) * 2
    if kind == "choice":
        i = max(range(len(keys)), key=lambda k: ps[k])
        return keys[i], ps[i]
    if kind == "score":
        ev = sum(i * p for i, p in enumerate(ps))
        i = max(0, min(len(keys) - 1, int(round(ev))))
        return keys[i], ps[i]
    raise ValueError(f"unknown kind {kind!r}")


def expected_level(row, probs) -> float:
    _, ps = norm_probs(row, probs)
    return sum(i * p for i, p in enumerate(ps))


# ------------------------------------------------------------------ the 2B -> 4B cascade (prep89/ohs3_lib's rule)

def cascade_norm(r, pr):
    """ohs3_lib.cascade_norm: the row's answers in order, probabilities renormalised over them."""
    keys = ["yes", "no"] if r["qtype"] == "noul" else r["options"]
    p = [float(pr.get(k, 0.0)) for k in keys]
    s = sum(p) or 1.0
    return keys, [x / s for x in p]


def cascade_routed(r, p_route, tau) -> bool:
    """ohs3_lib.cascade_routed (FINETUNE_PLAN 5.3): routed to the big model when the small top probability < tau."""
    return max(cascade_norm(r, p_route)[1]) < float(tau)


def cascade_answer(r, p_small, p_big, routed, w_big) -> dict:
    """ohs3_lib.cascade_answer: small probabilities, or on a routed row w_big * big + (1 - w_big) * small."""
    ks, ps = cascade_norm(r, p_small)
    if routed:
        _, pb = cascade_norm(r, p_big)
        ps = [float(w_big) * x + (1 - float(w_big)) * y for x, y in zip(pb, ps)]
    return dict(zip(ks, ps))


# ------------------------------------------------------------------ statistics

def paired_bootstrap(units, a, b, B=BOOT_B, seed=BOOT_SEED):
    """Paired bootstrap of mean(a) - mean(b) (a, b: 0/1 per row, in the same row order), resampling the unique units
    (commits) with replacement: numpy.random.default_rng(seed).integers(0, U, (B, U)). A commit that appears in
    several rows (tasks) carries all its rows. Returns point difference, 95 % percentile interval (sorted draws
    [int(0.025 B)], [int(0.975 B) - 1]), P(diff > 0) and counts."""
    import numpy as np
    uniq = sorted(set(units))
    idx = {u: i for i, u in enumerate(uniq)}
    U = len(uniq)
    n = np.zeros(U)
    d = np.zeros(U)
    for u, x, y in zip(units, a, b):
        n[idx[u]] += 1
        d[idx[u]] += float(x) - float(y)
    rng = np.random.default_rng(seed)
    draws = rng.integers(0, U, size=(B, U))
    W = np.bincount((np.arange(B)[:, None] * U + draws).ravel(), minlength=B * U).reshape(B, U).astype(float)
    den = W @ n
    diffs = np.sort((W @ d) / den)
    point = float(d.sum() / n.sum())
    return {"diff": point, "ci95": [float(diffs[int(0.025 * B)]), float(diffs[int(0.975 * B) - 1])],
            "p_better": float((diffs > 0).mean()), "n_rows": int(n.sum()), "n_units": U, "B": B, "seed": seed}


def verdict(ci) -> str:
    """PREREG_ejs5 rule: a win (or a loss) only when the paired 95 % interval excludes 0."""
    lo, hi = ci
    return "WIN (CI excludes 0, above)" if lo > 0 else "LOSS (CI excludes 0, below)" if hi < 0 else "TIE (CI includes 0)"


def pct(xs, q):
    """Linear-interpolation percentile (numpy's default)."""
    v = sorted(xs)
    if not v:
        return None
    k = (len(v) - 1) * q
    f = int(k)
    c = min(f + 1, len(v) - 1)
    return v[f] + (v[c] - v[f]) * (k - f)
