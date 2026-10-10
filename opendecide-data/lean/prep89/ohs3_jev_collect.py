"""(a) Collect Jev's OHS-3 answers with run_jev.py, EXACTLY as for OHS-2: the unchanged script, JEV_SPLIT=ohs3, the two
pre-registered runs JEV_TAG=jev_guard then JEV_TAG=jev_r2_guard (PREREG_OHS3 rules 2-3), OpenRouter route, default
model "jev-1.13" (responses report typesafe/jev-1.13-20260917), one call per call_id, concurrency 8 (run_jev.py's
Semaphore), resumable (run_jev.py skips calls already answered in preds_ohs3/<tag>_raw.jsonl).

  REAL (only after the owner's GO; paid OpenRouter calls):
    ../.venv/bin/python prep89/ohs3_jev_collect.py --go [--max-passes 3] [--cost-cap 3.0]
  DRY RUN (synthetic root, fake endpoint on 127.0.0.1; run by prep89/dryrun_ohs3.py):
    ../.venv/bin/python prep89/ohs3_jev_collect.py --root prep89/dryrun/root --fake-url http://127.0.0.1:PORT

What this wrapper adds around run_jev.py (it never edits it):
  * preflight: frozen OHS-3 sha256; run_jev.py identical to git HEAD (real) or a byte-identical copy (dry run); a key
    is present (never printed); no TYPESAFE_BASE_URL / JEV_MODEL / JEV_LIMIT override in the environment (real);
  * resume passes: run_jev.py is re-run (up to --max-passes) until every call has an answer; each pass only sends the
    calls still missing;
  * cost guard (real, optional --usage-check): OpenRouter key usage (GET /api/v1/key, free) before and after each run;
    stops before the next run if the spend exceeds --cost-cap;
  * a summary per run (counts only): calls answered/failed, raw records, model ids, rows not from the pinned model,
    run_jev.py's latency of the successful attempt (descriptive only: concurrency 8; speed is measured by
    ohs3_timing.py), preds rows. Written to <root>/logs/ohs3/jev_collect_<tag>.json. No item text is printed.
"""
from __future__ import annotations

import argparse
import json
import os
import subprocess
import sys
import time
from collections import Counter
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import ohs3_lib as L  # noqa: E402

TAGS = ("jev_guard", "jev_r2_guard")


def cost_estimate(n_calls=L.OHS3_CALLS, runs=2):
    """Two bounds. Billed rate seen so far: OHS-1 $0.12 / 3,694 calls ($0.032 per 1K), OHS-2 ~$0.1 / 2,640 calls
    (ledger). List-price ceiling: every call at the longest OHS-3 state (6,000 chars) plus 40 option definitions
    (~6,000 chars) ~ 12,000 chars ~ 3,400 tokens x $0.042/M."""
    n = n_calls * runs
    return {"calls": n, "billed_rate_usd": round(n * 0.032 / 1000, 2), "billed_rate_hi_usd": round(n * 0.038 / 1000, 2),
            "list_price_ceiling_usd": round(n * 3400 * L.JEV_USD_PER_M_INPUT / 1e6, 2),
            "task_brief_range_usd": [1.2, 2.7],
            "note": "the brief's $1.2-2.7 is above both bounds; use it as the cap"}


def openrouter_usage():
    """Total spend on the OpenRouter key (USD), or None. GET https://openrouter.ai/api/v1/key is free."""
    import httpx
    key = os.environ.get("OPENROUTER_API_KEY")
    if not key:
        return None
    try:
        r = httpx.get("https://openrouter.ai/api/v1/key", headers={"Authorization": f"Bearer {key}"}, timeout=20)
        return float(r.json()["data"]["usage"])
    except Exception:  # noqa: BLE001
        return None


def load_env_file():
    """The same .env files run_jev.py reads (values are never printed)."""
    for envf in (L.LEAN.parent / ".env", L.LEAN / ".env"):
        if envf.exists():
            for line in envf.read_text().splitlines():
                if "=" in line and not line.strip().startswith("#"):
                    k, v = line.split("=", 1)
                    os.environ.setdefault(k.strip(), v.strip().strip('"').strip("'"))


def run_summary(root, tag, calls, rows):
    raw = Path(root) / f"preds_{L.SPLIT}" / f"{tag}_raw.jsonl"
    recs = L.read_jsonl(raw) if raw.exists() else []
    ok = {r["call_id"]: r for r in recs if r["answers"]}
    lat = [r["latency_ms"] for r in ok.values() if r["latency_ms"] is not None]
    models = Counter(r["model"] for r in ok.values())
    pf = Path(root) / f"preds_{L.SPLIT}" / f"{tag}.jsonl"
    preds = L.read_jsonl(pf) if pf.exists() else []
    n_q = sum(len(c["row_ids"]) for c in calls)
    answered_rows = sum(1 for p in preds if p["id"] in rows)
    return {"tag": tag, "calls": len(calls), "calls_answered": len(ok), "calls_missing": len(calls) - len(ok),
            "raw_records": len(recs), "failed_attempt_records": sum(1 for r in recs if not r["answers"]),
            "models": dict(models), "calls_not_pinned_model": sum(v for k, v in models.items() if k != L.PINNED_JEV),
            "questions": n_q, "pred_rows": len(preds), "pred_rows_in_data": answered_rows,
            "latency_ms_success_attempt": {"p50": L.pct(lat, 0.5), "p95": L.pct(lat, 0.95), "n": len(lat),
                                           "note": "run_jev.py timing: success attempt only, concurrency 8; descriptive"},
            "raw_sha256": L.sha256_file(raw) if raw.exists() else None,
            "preds_sha256": L.sha256_file(pf) if pf.exists() else None}


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--root", default=str(L.LEAN))
    ap.add_argument("--tags", default=",".join(TAGS))
    ap.add_argument("--max-passes", type=int, default=3)
    ap.add_argument("--go", action="store_true", help="REAL run: paid OpenRouter calls (owner's GO)")
    ap.add_argument("--fake-url", default=None, help="dry run: the fake /v1/systemone base URL (127.0.0.1)")
    ap.add_argument("--usage-check", action="store_true", help="real: read OpenRouter key usage before/after")
    ap.add_argument("--cost-cap", type=float, default=3.0)
    ap.add_argument("--config", default=str(L.PREP / "ohs3_config.json"),
                    help="real: the committed run config (its D2 decides which tags run here)")
    a = ap.parse_args(argv)
    root = Path(a.root).resolve()
    real = root == L.LEAN.resolve()
    tags = [t for t in a.tags.split(",") if t]
    log_dir = root / "logs" / "ohs3"
    log_dir.mkdir(parents=True, exist_ok=True)
    env = dict(os.environ)
    if real:
        if not a.go:
            raise SystemExit("REAL OHS-3 Jev collection needs --go (owner's GO). Estimate: "
                             + json.dumps(cost_estimate(runs=len(tags))))
        if a.fake_url:
            raise SystemExit("--fake-url is for the synthetic dry run only")
        L.require_frozen(root)
        d2 = L.load_config(a.config, require_complete=True)["decisions"]["jev_timing"]
        if (d2 == "run1_via_harness") != (tags == ["jev_r2_guard"]):
            raise SystemExit(f"decisions.jev_timing = {d2}: tags must be "
                             + ("jev_r2_guard only (run 1 comes from ohs3_timing.py)" if d2 == "run1_via_harness"
                                else ",".join(TAGS)))
        if d2 == "run1_via_harness" and not (root / f"preds_{L.SPLIT}" / "jev_guard.jsonl").exists():
            raise SystemExit("D2 = run1_via_harness: run E (timing, --jev-preds-tag jev_guard) before run 2")
        if tags == ["jev_r2_guard"]:
            L.blind_print("D2 = run1_via_harness: only run 2 is collected here; run 1 (jev_guard) comes from "
                          "ohs3_timing.py --jev-preds-tag jev_guard (disclose)")
        elif tags != list(TAGS):
            raise SystemExit(f"PREREG_OHS3 rule 3: the two runs are {TAGS}, in that order (or jev_r2_guard alone "
                             "when D2 = run1_via_harness)")
        dirty = L.git("diff", "--quiet", "HEAD", "--", "run_jev.py").returncode
        if dirty:
            raise SystemExit("run_jev.py differs from git HEAD: it must be the OHS-1/OHS-2 collector, unchanged")
        for k in ("TYPESAFE_BASE_URL", "JEV_MODEL", "JEV_LIMIT", "JEV_SPLIT", "JEV_TAG", "TYPESAFE_DEFAULT_MODEL"):
            if os.environ.get(k):
                raise SystemExit(f"unset {k}: OHS-2 ran run_jev.py with its defaults")
        load_env_file()
        if not (os.environ.get("OPENROUTER_API_KEY") or os.environ.get("TYPESAFE_API_KEY")):
            raise SystemExit("NO_KEY: OPENROUTER_API_KEY not found (env or opendecide-data/.env)")
        if os.environ.get("TYPESAFE_API_KEY"):
            L.blind_print("note: TYPESAFE_API_KEY is set, so run_jev.py takes the direct TypeSafe route (OHS-2 used "
                          "OpenRouter); unset it to match OHS-2")
            raise SystemExit("STOP: TYPESAFE_API_KEY set; OHS-2 used the OpenRouter route")
        script = L.LEAN / "run_jev.py"
        env = dict(os.environ)
    else:
        L.require_synthetic(root)
        if not a.fake_url:
            raise SystemExit("dry run needs --fake-url")
        script = root / "run_jev.py"
        if not script.exists() or L.sha256_file(script) != L.sha256_file(L.LEAN / "run_jev.py"):
            script.write_bytes((L.LEAN / "run_jev.py").read_bytes())  # byte-identical copy, run from the root
        assert L.sha256_file(script) == L.sha256_file(L.LEAN / "run_jev.py")
        env = {k: v for k, v in os.environ.items() if k not in ("OPENROUTER_API_KEY", "TYPESAFE_API_KEY")}
        # run_jev.py reads <root>/../.env and <root>/.env: make sure no real key can be picked up there
        for envf in (root.parent / ".env", root / ".env"):
            if envf.exists():
                raise SystemExit(f"{envf} exists: the dry run must never see a real key")
        env.update(TYPESAFE_API_KEY="dryrun-fake-key", TYPESAFE_BASE_URL=a.fake_url, JEV_MODEL=L.JEV_REQUEST_MODEL_OPENROUTER)
    calls = L.read_jsonl(root / "data" / f"{L.SPLIT}_calls.jsonl")
    rows = {r["id"] for r in L.read_jsonl(root / "data" / f"{L.SPLIT}.jsonl")}
    L.blind_print(f"Jev collection: {len(calls)} calls x {len(tags)} runs; script sha256 "
                  f"{L.sha256_file(script)[:16]}; {'REAL' if real else 'DRY RUN (fake endpoint)'}")
    L.blind_print("estimate: " + json.dumps(cost_estimate(len(calls), len(tags))))
    used0 = openrouter_usage() if (real and a.usage_check) else None
    summaries = {}
    for tag in tags:
        t0 = time.time()
        for p in range(1, a.max_passes + 1):
            e = {**env, "JEV_SPLIT": L.SPLIT, "JEV_TAG": tag}
            logf = log_dir / f"run_jev_{tag}_pass{p}.log"
            with open(logf, "w") as lf:
                rc = subprocess.run([str(L.PY), str(script)], cwd=str(script.parent), env=e, stdout=lf,
                                    stderr=subprocess.STDOUT).returncode
            s = run_summary(root, tag, calls, rows)
            L.blind_print(f"  {tag} pass {p}: exit {rc}, answered {s['calls_answered']}/{s['calls']} calls, "
                          f"failed attempt records {s['failed_attempt_records']} (log {logf.name})")
            if rc != 0:
                raise SystemExit(f"run_jev.py exited {rc}: see {logf}")
            if s["calls_missing"] == 0:
                break
        s["passes"], s["wall_s"] = p, round(time.time() - t0, 1)
        summaries[tag] = s
        (log_dir / f"jev_collect_{tag}.json").write_text(json.dumps(s, indent=1))
        if s["calls_missing"]:
            L.blind_print(f"  WARNING {tag}: {s['calls_missing']} calls still unanswered after {p} passes "
                          f"(they count as wrong for Jev and are reported; re-run this script to retry them)")
        if s["calls_not_pinned_model"]:
            L.blind_print(f"  DISCLOSE {tag}: {s['calls_not_pinned_model']} calls answered by a model other than "
                          f"{L.PINNED_JEV}: {s['models']}")
        if used0 is not None:
            used = openrouter_usage()
            if used is not None:
                L.blind_print(f"  OpenRouter spend so far in this job: ${used - used0:.3f}")
                if used - used0 > a.cost_cap and tag != tags[-1]:
                    raise SystemExit(f"cost cap ${a.cost_cap} exceeded: stopping before the next run")
    L.blind_print(json.dumps({t: {k: s[k] for k in ("calls_answered", "calls_missing", "pred_rows", "calls_not_pinned_model")}
                              for t, s in summaries.items()}))
    return summaries


if __name__ == "__main__":
    main()
