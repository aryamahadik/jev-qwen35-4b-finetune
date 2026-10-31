"""l1_look.j_run: the J step (Jev, read ONCE, after the L1 verdict is logged; PREREG A38 'Looks', A37 h, C2_DATA_SPEC 8.5 / 8.6). Sealed-side program.

The pinned runner (ohs4_sealed/scorer/run_jev_ohs4.py, sha5bc81eab... in PREREG A38) sends the same calls as the request file to Jev through OpenRouter
and writes answers/jev_ohs4.jsonl; the frozen scorer's look J compares Jev with the L1 answer files (it re-verifies their sha256 and refuses a second
J or a J before L1). This file adds only what those two do not do: the ordering guards, the LIVE balance check (key read from opendecide-data/.env,
never printed), a spend watchdog, the claims arithmetic of spec 8.6 and a content-free J_RESULT.json.

  cd lean && ../.venv/bin/python -B c2_build/train/l1_look/j_run.py check     guards + live OpenRouter balance (numbers only); spends nothing
  cd lean && ../.venv/bin/python -B c2_build/train/l1_look/j_run.py go        check -> the pinned runner (resumable) -> the J look -> J_RESULT.json
  cd lean && ../.venv/bin/python -B c2_build/train/l1_look/j_run.py score     only the J look + result (after a complete runner pass)

Guards (all must hold; each refusal is content-free): hash pins (A38); L1_RESULT.json exists AND the scorer's log holds a granted L1 (the L1 verdict is
logged); no granted J and no J_RESULT.json; the owner's GO #2 record exists; the balance is read live and must show at least MIN_REMAINING_USD left
(and not be unknown); the runner's spend is watched every 45 s and the runner is stopped (resumable) if usage rose by more than CAP_USD.
"""
from __future__ import annotations

import argparse
import json
import os
import re
import subprocess
import sys
import threading
import time
import urllib.error
import urllib.request
from pathlib import Path

if __package__ in (None, ""):
    sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
    __package__ = "l1_look"

from . import l1common as L  # noqa: E402
from . import l1verdict as LV  # noqa: E402

PINNED_MODEL = "jev-1.13"         # RULING_L1_PRELOOK item 6: the A38-frozen runner's REQUEST id binds; no substitute
SERVED_ID = "typesafe/jev-1.13-20260917"   # RULING item 6b: the ONE accepted SERVED id (what the provider resolves jev-1.13 to); anything else is refused before the look
FATAL_STATUS = (401, 402, 404, 410)      # auth / credit / model not found or gone: not transient, never scored as "Jev wrong"
MODEL_GONE_STATUS = (404, 410)
ONE_READ_LINE = ("Spec 8.6 asks for LB > 0 in both pinned Jev runs; A37 (h), A38 and A42-D 13.8 allow one OHS-4 Jev read, so every C2-vs-Jev claim here rests "
                 "on ONE pinned run and is weaker than the two-run test in spec 8.6.")
JEV_VERSION_LINE = ("The OHS-4 Jev comparator is jev-1.13 (served id typesafe/jev-1.13-20260917), pinned in the runner frozen by A38 (13 Oct 2026, sha 5bc81eab...). "
                    "Jev 1.14 (released 14 Oct) is the version served now and is NOT the OHS-4 comparator; every OHS-4 claim names 'Jev 1.13'.")
COMPARATOR_LINE = ("OHS-4 Jev comparator: Jev 1.13, requested as 'jev-1.13' by the A38-frozen runner (sha 5bc81eab...). {allr} reported the served id "
                   "'typesafe/jev-1.13-20260917' (a 17 Sep 2026 snapshot; the project's full id for Jev 1.13 since the OHS-3 era, HANDOFF.md:2642). Jev 1.14 (14 Oct) is "
                   "not the comparator. A first guard compared the bare string 'jev-1.13' and refused before any look; it was corrected by ruling 6b, and the same single "
                   "read was then scored once ({spend}). The records cannot show the alias's snapshot on 13 Oct; no other 1.13 snapshot is on record.")
CAP_USD = 1.50                    # round 1's J cap (RUNBOOK_FINAL (c)); the estimate for this suite is about USD 0.2-1
MIN_REMAINING_USD = 2.00
POLL_S = 45
MAX_PASSES = 3                    # the first pass + at most two resumes of the pinned runner for transient failures
BALANCE_URL = "https://openrouter.ai/api/v1/key"


def say(*a):
    print(*a, flush=True)


# ------------------------------------------------------------------ OpenRouter balance (numbers only)
def read_key(env_file: Path) -> str:
    for line in Path(env_file).read_text().splitlines():
        if "=" in line and not line.strip().startswith("#"):
            k, v = line.split("=", 1)
            if k.strip() == "OPENROUTER_API_KEY":
                v = v.strip().strip('"').strip("'")
                if v:
                    return v
    L.refuse("OPENROUTER_API_KEY is missing in opendecide-data/.env")


def balance(key: str, url: str = BALANCE_URL, timeout: float = 20.0, opener=urllib.request.urlopen) -> dict:
    """GET /api/v1/key -> {usage, limit, limit_remaining} (numbers). The key is never printed or returned."""
    req = urllib.request.Request(url, headers={"Authorization": "Bearer " + key})
    try:
        d = json.load(opener(req, timeout=timeout))["data"]
    except (urllib.error.URLError, OSError, ValueError, KeyError) as e:
        L.refuse("the OpenRouter balance could not be read live (" + type(e).__name__ + "): J does not start blind")
    return {x: d.get(x) for x in ("usage", "limit", "limit_remaining")}


def balance_ok(b: dict, min_remaining: float = MIN_REMAINING_USD) -> str | None:
    rem = b.get("limit_remaining")
    if not isinstance(rem, (int, float)):
        return "the remaining balance is unknown (no limit on the key): the owner must confirm the balance"
    if rem < min_remaining:
        return f"only ${rem:.2f} left on the OpenRouter key (need ${min_remaining:.2f})"
    return None


# ------------------------------------------------------------------ guards
def guards(p: L.L1Paths, pins=None, allow_resume: bool = False):
    L.require_pins(p, pins)
    if not p.result.exists():
        L.refuse(f"{p.result.name} missing: J runs only after the L1 verdict is logged")
    looks = L.read_looks(p)
    if not L.granted(looks, "L1"):
        L.refuse("the scorer's look log holds no granted L1: J needs L1 first")
    prior = L.read_json(p.j_result) if p.j_result.exists() else None
    result_taken = p.j_result.exists() and not (isinstance(prior, dict) and prior.get("status") == "not_run")
    if result_taken or (L.granted(looks, "J") and not allow_resume):
        L.refuse("J was already taken (Jev is read once)")
    L.load_owner_go(p)
    res = L.read_json(p.result) or {}
    for k, f in (("c1", p.c1_answers), ("c2", p.c2_answers)):
        want = (res.get("answer_files_sha256") or {}).get(k)
        if want and (not f.exists() or L.sha256_file(f) != want):
            L.refuse(f"{f.name} differs from the file the L1 look scored")
    return res


def jev_model(p: L.L1Paths) -> str | None:
    m = re.search(r'^MODEL\s*=\s*"([^"]+)"', p.jev_runner.read_text(), re.M)
    return m.group(1) if m else None


# ------------------------------------------------------------------ the pinned runner, watched
def run_runner(p: L.L1Paths, key: str, extra_args: list, balance_url: str, before: dict, cap_usd: float = CAP_USD, poll_s: float = POLL_S,
               python: str = sys.executable, opener=urllib.request.urlopen) -> dict:
    """Run the pinned runner as a subprocess (it prints counts only) and poll the live usage; stop it (resumable) above the cap."""
    cmd = [python, str(p.jev_runner), *extra_args]
    proc = subprocess.Popen(cmd, cwd=str(p.jev_runner.parent), stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
    state = {"stopped_at_cap": False, "polls": 0, "last": before}
    done = threading.Event()

    def watch():
        while not done.wait(poll_s):
            try:
                b = balance(key, balance_url, opener=opener)
            except L.Refused:
                continue
            state["polls"] += 1
            state["last"] = b
            if isinstance(b.get("usage"), (int, float)) and isinstance(before.get("usage"), (int, float)) \
                    and b["usage"] - before["usage"] > cap_usd and proc.poll() is None:
                state["stopped_at_cap"] = True
                proc.terminate()
                return

    th = threading.Thread(target=watch, daemon=True)
    th.start()
    out, _ = proc.communicate()
    done.set()
    th.join(timeout=2)
    lines = [l for l in (out or "").splitlines() if l.strip()]
    last = lines[-1] if lines else ""
    summary = None
    try:
        summary = json.loads(last)
    except ValueError:
        pass
    return {"returncode": proc.returncode, "stopped_at_cap": state["stopped_at_cap"], "polls": state["polls"], "summary": summary}


def unanswered_transient(p: L.L1Paths) -> int:
    """Calls whose last attempt failed for a transient reason (HTTP 429 / 5xx, or no HTTP status: timeout or connection error). 0 = nothing left worth a resume."""
    f = p.answers / "jev_ohs4_usage.jsonl"
    if not f.exists():
        return 0
    last = {}
    for l in open(f):
        if l.strip():
            r = json.loads(l)
            last[r["id"]] = r
    return sum(1 for r in last.values() if r.get("error") and (r.get("status") is None or r.get("status") == 429 or (isinstance(r.get("status"), int) and r["status"] >= 500)))


def usage_totals(p: L.L1Paths) -> dict:
    """Counts and token sums from the runner's usage file (no text): calls, errors, HTTP statuses, numeric usage fields summed, latency p50 / p95."""
    f = p.answers / "jev_ohs4_usage.jsonl"
    if not f.exists():
        return {}
    rows = [json.loads(l) for l in open(f) if l.strip()]
    last = {}
    for r in rows:                      # a resumed run appends: the last line per call id wins
        last[r["id"]] = r
    sums, status, ms = {}, {}, []
    for r in last.values():
        status[str(r.get("status"))] = status.get(str(r.get("status")), 0) + 1
        if isinstance(r.get("ms"), (int, float)):
            ms.append(r["ms"])
        u = r.get("usage")
        if isinstance(u, dict):
            for k, v in u.items():
                if isinstance(v, (int, float)) and not isinstance(v, bool):
                    sums[k] = sums.get(k, 0) + v
    ms.sort()
    q = lambda f_: round(ms[min(len(ms) - 1, int(f_ * len(ms)))], 1) if ms else None  # noqa: E731
    return {"calls": len(last), "errors": sum(1 for r in last.values() if r.get("error")), "http_status": status, "usage_sums": sums,
            "ms_p50": q(0.5), "ms_p95": q(0.95)}


# ------------------------------------------------------------------ the pinned model must be the one that answered (RULING item 6)
def served_matches(served, accepted: str = None) -> bool:
    """EXACT equality with the one accepted served id (no prefix, suffix or namespace tolerance)."""
    return served == (SERVED_ID if accepted is None else accepted)


def served_check(p: L.L1Paths) -> dict:
    """Before the J look: from the runner's usage file (statuses, error classes and the served model field; no content). The look is NOT taken when a call
    failed because the model is gone (404 / 410), when an answered call names another model than the pin, when most calls failed as bad requests (a wrong or
    deprecated model id answers 400), when a non-transient auth / credit error remains, or when nothing was answered: otherwise an all-error run would score
    Jev at 0% and spend the one look. Transient failures (429 / 5xx / timeouts) are retried by running `go` again; what stays unanswered then counts wrong."""
    f = p.answers / "jev_ohs4_usage.jsonl"
    rows = [json.loads(l) for l in open(f) if l.strip()] if f.exists() else []
    last = {}
    for r in rows:
        last[r["id"]] = r
    answered = [r for r in last.values() if r.get("status") == 200 and not r.get("error")]
    status = {}
    for r in last.values():
        status[str(r.get("status"))] = status.get(str(r.get("status")), 0) + 1
    served, no_id = {}, 0
    for r in answered:
        if isinstance(r.get("model"), str) and r["model"]:
            served[r["model"]] = served.get(r["model"], 0) + 1
        else:
            no_id += 1
    bad_models = sorted(m for m in served if not served_matches(m))
    gone = sum(1 for r in last.values() if r.get("status") in MODEL_GONE_STATUS)
    fatal = sum(1 for r in last.values() if r.get("status") in FATAL_STATUS)
    bad_req = sum(1 for r in last.values() if r.get("status") in (400, 422))
    not_served = []
    if gone:
        not_served.append(f"{gone} call(s) failed with HTTP 404/410 (model not found or gone)")
    if bad_models:
        not_served.append(f"answered by served model id(s) {bad_models}, not the accepted {SERVED_ID}")
    if no_id:
        not_served.append(f"{no_id} answered call(s) report no served model id")
    if len(served) > 1:
        not_served.append(f"more than one distinct served model id ({len(served)})")
    if last and bad_req / len(last) > 0.5:
        not_served.append(f"{bad_req} of {len(last)} calls failed as bad requests (HTTP 400/422: what a wrong or deprecated model id returns)")
    blocking = []
    if not last:
        blocking.append("the usage file records no call")
    elif not answered:
        blocking.append("no call was answered")
    if fatal - gone:
        blocking.append(f"{fatal - gone} call(s) ended in HTTP 401/402 (auth or credit): resolve, then run `go` again")
    return {"ok": not not_served and not blocking, "model_not_served": bool(not_served), "reasons": not_served + blocking, "pinned_model": PINNED_MODEL, "accepted_served_id": SERVED_ID,
            "served_models": served, "answered_without_id": no_id, "status_counts": status, "calls": len(last), "answered": len(answered)}


def jev_spend_total(p: L.L1Paths, extra: dict | None = None) -> float | None:
    """The Jev spend this read cost: the archived not-run records (the paid pass) plus the current run's own OpenRouter delta, if any."""
    vals = []
    for f in sorted(p.train.glob("J_RESULT_NOTRUN_*.json")):
        d = L.read_json(f)
        sp = ((d or {}).get("openrouter") or {}).get("spent_usd")
        if isinstance(sp, (int, float)):
            vals.append(sp)
    sp = ((extra or {}).get("openrouter") or {}).get("spent_usd")
    if isinstance(sp, (int, float)):
        vals.append(sp)
    return round(sum(vals), 2) if vals else None


def disclosures(p: L.L1Paths, extra_lines: list | None = None, chk: dict | None = None, extra: dict | None = None) -> list:
    """The one-read line, the comparator line (RULING 6b, once the served id passed the check), the SPEED-3 line, then any extra line."""
    if chk and chk.get("ok") and chk.get("served_models") == {SERVED_ID: chk.get("answered")}:
        n, calls = chk["answered"], chk["calls"]
        sp = jev_spend_total(p, extra)
        comp = COMPARATOR_LINE.format(allr=(f"All {n:,} responses" if n == calls else f"All {n:,} answered responses ({calls - n:,} calls unanswered)"),
                                      spend=f"Jev spend ${sp:.2f}" if sp is not None else "Jev spend: see the OpenRouter before / after in the archived not-run record")
    else:
        comp = JEV_VERSION_LINE
    return [ONE_READ_LINE, comp, L.SPEED3_LINE, *(extra_lines or [])]


def archive_not_run(p: L.L1Paths):
    """Rename (never delete) an existing not-run J_RESULT.json to J_RESULT_NOTRUN_<HHMM>Z.json, so a later record never overwrites it. A TAKEN result is never moved."""
    if not p.j_result.exists():
        return None
    rec = L.read_json(p.j_result)
    if not (isinstance(rec, dict) and rec.get("status") == "not_run"):
        L.refuse("J_RESULT.json is not a not-run record: it is never moved or replaced")
    stamp = str(rec.get("utc") or L.utc())[11:16].replace(":", "") + "Z"
    dest = p.train / f"J_RESULT_NOTRUN_{stamp}.json"
    k = 1
    while dest.exists():
        k += 1
        dest = p.train / f"J_RESULT_NOTRUN_{stamp}_{k}.json"
    os.replace(p.j_result, dest)
    return dest


def write_not_run(p: L.L1Paths, check: dict, extra: dict | None = None):
    """J_RESULT.json with status not_run (read-only). It does NOT use up the J look; an earlier not-run record is renamed (never deleted or overwritten)."""
    archive_not_run(p)
    L.write_json(p.j_result, {"look": "J", "status": "not_run", "utc": L.utc(),
                              "reason": f"J not run: pinned {PINNED_MODEL} not served (accepted served id {SERVED_ID})" if check["model_not_served"] else "J look not taken: " + "; ".join(check["reasons"]),
                              "claims": "not evaluable (spec 8.6 claims against Jev are not evaluable; no substitute model id is used)",
                              "served_check": check, "disclosure": disclosures(p), **(extra or {}),
                              "note": "no J look was taken; no other model id was used. Report to the owner (A89: a rule question stops the step)."}, mode=0o444)


# ------------------------------------------------------------------ the J look
def recompute_j_output(S, p: L.L1Paths, suite: list, rj: dict) -> dict:
    """What run_look("J") prints, rebuilt WITHOUT a look (after a crash that came after the scorer logged the J look): the scorer's own pure functions."""
    l1 = next(x for x in L.read_looks(p) if x.get("look") == "L1" and x.get("status") == "granted")
    recs = {k: S.evaluate(suite, S.load_answers(path)) for k, path in l1["files"].items()}
    return {"look": "J", "suite_sha256": L.sha256_file(p.suite), "reports": [S.report(suite, rj, "jev")],
            "comparisons": [S.compare(suite, recs[k], rj, f"{k.upper()} - Jev") for k in sorted(recs)], "recomputed_without_a_second_look": True}


def score_j(p: L.L1Paths, *, pins=None, scorer_sha: str | None = None, extra: dict | None = None, out=say) -> dict:
    res = guards(p, pins, allow_resume=True)
    jl = [x for x in L.read_looks(p) if x.get("look") == "J" and x.get("status") == "granted"]
    resumed = bool(jl)                       # the J look was granted before a crash: finish from the files, no second look and no second Jev read
    pinned = jev_model(p)
    if pinned != PINNED_MODEL:
        L.refuse(f"the runner's model id is {pinned!r}, not the A38 pin {PINNED_MODEL}")
    chk = served_check(p)
    if not chk["ok"] and not resumed:
        if chk["model_not_served"]:
            write_not_run(p, chk, extra)
        L.refuse("no J look was taken: " + "; ".join(chk["reasons"]))
    if not p.jev_answers.exists():
        L.refuse(f"{p.jev_answers.name} missing: run the pinned runner first")
    S = LV.load_scorer(p.scorer, scorer_sha or L.sha256_file(p.scorer))
    suite = S.load_suite(str(p.suite))
    got = S.load_answers(str(p.jev_answers))
    ids = {it["id"] for it in suite}
    if not got or not set(got) <= ids:
        L.refuse("the Jev answer file holds calls that are not the suite's")
    missing = len(ids - set(got))
    if missing:
        out(f"note: {missing} calls have no usable Jev answer; the frozen scorer counts them wrong for Jev and prints the coverage")
    rj = S.evaluate(suite, got)
    extra_disclosure = []
    if resumed:
        if (jl[0].get("sha256") or {}).get("jev") != L.sha256_file(p.jev_answers):
            L.refuse("the Jev answer file differs from the one the granted J look scored")
        sc = L.read_json(p.j_scorer_out)
        if not isinstance(sc, dict):
            sc = recompute_j_output(S, p, suite, rj)
            L.write_json(p.j_scorer_out, sc, mode=0o444)
            extra_disclosure.append("The scorer's printed output of the J look was not saved (a crash after the look was granted). The aggregates here were recomputed from the "
                                    "sha-checked answer files with the scorer's own report and compare functions. No second J look and no second Jev read were made.")
        out("J was already granted: finishing from the saved files (no second look, no second read)")
    else:
        buf = []
        rc = S.run_look("J", {"jev": str(p.jev_answers)}, suite_path=str(p.suite), looks_path=str(p.looks), out=buf.append)
        if rc != 0:
            L.refuse("the frozen scorer refused the J look: " + str((json.loads(buf[0]) if buf else {}).get("refused", ""))[:120])
        sc = json.loads(buf[0])
        L.write_json(p.j_scorer_out, sc, mode=0o444)
    claims = {}
    for k in ("c2", "c1"):
        f = p.c2_answers if k == "c2" else p.c1_answers
        if f.exists():
            claims[k] = LV.j_claims(S, suite, S.evaluate(suite, S.load_answers(str(f))), rj, k.upper())
            claims[k]["comparator"] = f"Jev 1.13 (requested {PINNED_MODEL}; served {SERVED_ID})"
    archive_not_run(p)                       # a not-run record from an earlier attempt is renamed, never overwritten or deleted
    result = {"disclosure": disclosures(p, extra_disclosure, chk, extra), "look": "J", "status": "taken", "utc": L.utc(), "mode": res.get("mode"), "L1_result_sha256": L.sha256_file(p.result),
              "jev_model": pinned, "served_check": chk, "jev_answers_sha256": L.sha256_file(p.jev_answers), "answered_calls": len(got), "unanswered_calls": missing,
              "claims_report_only": claims, "scorer_output": sc, "jev_usage_totals": usage_totals(p), "rules_sha256": LV.RULES_SHA,
              "pins": {"MANIFEST.json": L.sha256_file(p.manifest), "scorer": L.sha256_file(p.scorer), "jev_runner": L.sha256_file(p.jev_runner)},
              **(extra or {}),
              "note": "aggregates only. Jev is read ONCE (A37 h, A38 'Looks', A42-D 13.8): spec 8.6's 'both pinned Jev runs' cannot be shown. Jev outputs are used for nothing else."}
    L.write_json(p.j_result, result, mode=0o444)
    out(f"{p.j_result.name} written")
    return result


def go(p: L.L1Paths, *, pins=None, env_file: Path | None = None, balance_url: str = BALANCE_URL, runner_args: list | None = None,
       key: str | None = None, concurrency: int = 4, cap_usd: float = CAP_USD, poll_s: float = POLL_S, opener=urllib.request.urlopen,
       min_remaining: float = MIN_REMAINING_USD, out=say) -> dict:
    guards(p, pins, allow_resume=True)
    if L.granted(L.read_looks(p), "J"):               # a crash after the J look was granted: finish from the files; NO runner, NO balance call, NO second read
        out("the J look is already granted: finishing from the saved files (no second Jev read)")
        return score_j(p, pins=pins, out=out)
    key = key or read_key(env_file or p.env_file)
    before = balance(key, balance_url, opener=opener)
    out("OpenRouter before: " + json.dumps(before))
    why = balance_ok(before, min_remaining)
    if why:
        L.refuse(why)
    args = runner_args if runner_args is not None else ["--go", "--concurrency", str(concurrency)]
    passes, run = 0, None
    while True:
        passes += 1
        run = run_runner(p, key, args, balance_url, before, cap_usd, poll_s, opener=opener)
        if run["stopped_at_cap"] or run["returncode"] != 0:
            break
        left = unanswered_transient(p)
        # transient failures (429 / 5xx / timeouts) are retried ONLY by the pinned runner's own resume, a few passes, before anything is scored
        if left == 0 or passes >= MAX_PASSES:
            break
    after = balance(key, balance_url, opener=opener)
    delta = round(after["usage"] - before["usage"], 4) if isinstance(after.get("usage"), (int, float)) and isinstance(before.get("usage"), (int, float)) else None
    out("OpenRouter after: " + json.dumps(after) + f" (spent {delta}); runner passes {passes}")
    out("runner: " + json.dumps(run))
    if run["stopped_at_cap"] or run["returncode"] != 0:
        L.refuse("the runner did not finish (stopped at the spend cap or failed); run `go` again to resume (answered calls are skipped)")
    return score_j(p, pins=pins, extra={"openrouter": {"before": before, "after": after, "spent_usd": delta, "cap_usd": cap_usd}, "runner_passes": passes},
                   out=out)


def check(p: L.L1Paths, pins=None, env_file: Path | None = None, balance_url: str = BALANCE_URL, key: str | None = None, opener=urllib.request.urlopen,
          out=say) -> int:
    try:
        guards(p, pins, allow_resume=True)
        if L.granted(L.read_looks(p), "J"):
            out("the J look is already granted: run `go` or `score` to finish from the saved files (no second read)")
            out("GO")
            return 0
        out("guards: OK (hash pins; L1 verdict logged; no J yet; owner GO #2 record present)")
        b = balance(key or read_key(env_file or p.env_file), balance_url, opener=opener)
        out("OpenRouter live: " + json.dumps(b))
        why = balance_ok(b)
        if why:
            out(why)
            out("STOP")
            return 2
        if jev_model(p) != PINNED_MODEL:
            out(f"the runner's model id is {jev_model(p)!r}, not the A38 pin {PINNED_MODEL}")
            out("STOP")
            return 2
        out(f"model {jev_model(p)} (the A38 pin); cap ${CAP_USD}; GO")
        return 0
    except L.Refused as e:
        out(str(e))
        out("STOP")
        return 2


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("cmd", choices=["check", "go", "score"])
    ap.add_argument("--lean", default=str(L.LEAN_DEFAULT))
    ap.add_argument("--concurrency", type=int, default=4)
    a = ap.parse_args(argv)
    p = L.L1Paths(a.lean)
    try:
        if a.cmd == "check":
            return check(p)
        if a.cmd == "score":
            score_j(p)
            return 0
        go(p, concurrency=a.concurrency)
        return 0
    except L.Refused as e:
        say(str(e))
        return 2


if __name__ == "__main__":
    sys.exit(main())
