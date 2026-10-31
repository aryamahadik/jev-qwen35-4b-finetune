"""l1_look.l1_cli: the CPU side of the L1 look (no Modal, no GPU, no network). Sealed-side program: it reads the sealed folder by program and prints
only file names, shas, counts of files, T values (dev-fitted) and the verdict table. It never prints an item, a label or a per-item score.

  cd lean && ../.venv/bin/python -B c2_build/train/l1_look/l1_cli.py check      every guard + the estimate; changes nothing (exit 0 = GO)
  cd lean && ../.venv/bin/python -B c2_build/train/l1_look/l1_cli.py finish     after the GPU job: freeze T (dev) -> answer files -> THE look -> L1_RESULT.json
  cd lean && ../.venv/bin/python -B c2_build/train/l1_look/l1_cli.py freeze-t   only the temperature freeze (dev data), to review T before `finish`
  cd lean && ../.venv/bin/python -B c2_build/train/l1_look/l1_cli.py shas       sha256 of every file of this tool (for A64_TOOLS.md)

`finish` order (everything refuses before it can take the look; the look is taken only when all of it is ready):
  1 hash pins (PREREG A38) -> 2 one-look guards -> 3 pre-gate/candidate still the ones of the GPU job -> 4 T fitted on the C2 MIXDEV reads of this job
  (dev only), written to L1_T_FROZEN.json BEFORE any sealed read is opened -> 5 T applied to the raw OHS-4 reads (calibrate.scaled, per type) ->
  answer files written read-only, validated (every call answered, valid probabilities) -> 6 the frozen scorer's look L1 (--c1 [--c2]) ->
  7 the S1-S6 table (l1verdict) -> L1_RESULT.json (read-only).
A crash after the scorer granted L1 is resumed by running `finish` again: it reads the saved scorer output and only recomputes the table.
"""
from __future__ import annotations

import argparse
import json
import os
import sys
import time
from pathlib import Path

if __package__ in (None, ""):
    sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
    __package__ = "l1_look"

from . import l1common as L  # noqa: E402
from . import l1temp as LT  # noqa: E402
from . import l1verdict as LV  # noqa: E402

TOOL_FILES = ("__init__.py", "l1common.py", "l1temp.py", "l1verdict.py", "l1reader.py", "l1session.py", "l1_cli.py", "modal_app_l1.py", "j_run.py")


def tool_shas() -> dict:
    return {f: L.sha256_file(L.HERE / f) for f in TOOL_FILES if (L.HERE / f).exists()}


def say(*a):
    print(*a, flush=True)


# ------------------------------------------------------------------ check
def check(p: L.L1Paths, pins=None, out=say, p_ref=None, spent_usd=None, trained_families=None) -> int:
    ok = True
    try:
        L.require_pins(p, pins)
        out("hash pins (PREREG A38 + manifest): OK")
    except L.Refused as e:
        out(str(e))
        return 2
    steps = (("one-look guards", lambda: (L.guard_one_look(p), L.guard_gpu_fresh(p))),
             ("owner GO #2 record", lambda: L.load_owner_go(p)),
             ("CANDIDATE_C2.json", lambda: L.load_candidate(p)))
    cand = None
    for name, fn in steps:
        try:
            r = fn()
            out(f"{name}: OK")
            if name == "CANDIDATE_C2.json":
                cand = r
        except L.Refused as e:
            out(f"{name}: {e}")
            ok = False
    if cand is not None:
        try:
            pg = L.load_pregate(p, cand)
            if pg["waived"]:
                out(f"pre-gate result ({p.pregate.name}): failed {pg['failed']} only, waived by the owner (PREREG {L.WAIVER_RECORD}, {p.waiver_b.name}) "
                    "-> PASS with (b) waived -> C1 + C2 in the look")
            else:
                out(f"pre-gate result ({p.pregate.name}): {'PASS -> C1 + C2 in the look' if pg['effective_pass'] else 'FAIL ' + str(pg['failed']) + ' -> C1 alone (spec 7.2)'}")
        except L.Refused as e:
            out(f"pre-gate: {e}")
            ok = False
    if ok:
        try:
            plan, _ = L.prepare_plan(p, "check", pins=pins, p_ref=p_ref, spent_usd=spent_usd, trained_families=trained_families)
            if plan["parity"]:
                out(f"parity record ({plan['parity']['file']}): argmax agreement {plan['parity']['argmax_agree']} on {plan['parity']['n']} rows, {plan['parity']['gpu']}: OK")
            out(f"A80 (c) trained families for the T fit: {len(plan['trained_families'])}; mixdev sha equals the gate's: {plan['gate_mixdev_sha256'] is not None}")
            v = plan["estimate"]["verdict"]
            out(f"mode {plan['mode']}; models {[m['read_name'] for m in plan['models']]}; estimate likely ${v['likely_usd']} high ${v['high_usd']} "
                f"(ledger spent ${v['spent_usd']}, stop-launch ${v['stop_launch_usd']}, fits {v['fits']}); "
                f"{plan['estimate']['scenarios']['likely']['total_min']} min likely")
            ok = bool(v["fits"])
        except L.Refused as e:
            out(str(e))
            ok = False
    out("GO" if ok else "STOP")
    return 0 if ok else 2


# ------------------------------------------------------------------ temperature freeze
def _jsonl(path) -> list:
    return [json.loads(l) for l in open(path) if l.strip()]


def raw_run(p: L.L1Paths) -> dict:
    rr = L.read_json(p.raw_dir / "RAW_RUN.json")
    if not isinstance(rr, dict):
        L.refuse("no raw reads of the look (answers/raw/RAW_RUN.json): run the GPU job first")
    return rr


def freeze_t(p: L.L1Paths, run_id: str, mode: str, trained: list | None = None) -> dict:
    """Fit T on the MIXDEV reads of this job (dev data only) by RULING_L1_PRELOOK item 1 and write L1_T_FROZEN.json. If it exists it must match its
    inputs (it is never re-fitted). `trained` = the A80 (c) families recorded by the GPU job's plan (RAW_RUN.json)."""
    run = p.out_root / run_id
    names = {"c1": L.C1_READ, **({"c2": L.C2_READ} if mode == "c1c2" else {})}
    if trained is None:
        trained = (L.read_json(p.raw_dir / "RAW_RUN.json") or {}).get("trained_families")
    if not trained:
        L.refuse("the A80 (c) trained families are not recorded for this job")
    gate_sha, mix_sha = L.gate_mixdev_sha(p), L.sha256_file(p.mixdev)
    if gate_sha and gate_sha != mix_sha:
        L.refuse(f"{p.mixdev.name} differs from the file the gate read")
    rows = L.mixdev_fit_rows(p, trained)
    inputs = {k: {"file": f"dev/{n}.jsonl", "sha256": L.sha256_file(run / "dev" / f"{n}.jsonl")} for k, n in names.items()}
    if p.tfrozen.exists():
        rec = L.read_json(p.tfrozen)
        if not isinstance(rec, dict) or rec.get("inputs") != inputs or rec.get("mixdev_sha256") != mix_sha or rec.get("run_id") != run_id \
                or rec.get("trained_families") != sorted(trained):
            L.refuse(f"{p.tfrozen.name} exists but does not match this job's dev reads (it is never re-fitted)")
        return rec
    fits, report, T = {}, {}, {}
    for k, n in names.items():
        preds = {d["id"]: d["probs"] for d in _jsonl(run / "dev" / f"{n}.jsonl")}
        try:
            r = LT.fit_all(rows, preds)
        except ValueError as e:
            L.refuse(f"temperature fit stopped (no fallback): {str(e)[:160]}")
        fits[k], report[k] = r["binding"], r["report_only"]
        T[k] = LT.T_of(fits[k])
    rec = {"what": "serving temperature per model and question type, fitted on the C2 MIXDEV only (dev; never OHS-4, never Jev)",
           "rule": LT.RULE, "ruling": "c2_build/zed_orch/RULING_L1_PRELOOK.md item 1", "grid": "calibrate.GRID 0.25..10.00 step 0.05", "clip": [LT.T_LO, LT.T_HI],
           "group_kind": "sampler + pack + register (union)", "run_id": run_id, "mode": mode, "mixdev_sha256": mix_sha, "gate_mixdev_sha256": gate_sha,
           "trained_families": sorted(trained), "fit_rows": len(rows), "inputs": inputs, "T": T, "fits": fits, "report_only_fits": report,
           "c1_shipped_A5_T_report_only": LT.SHIPPED_C1_A5, "frozen_utc": L.utc(), "frozen_before_any_sealed_read": True,
           "tool_sha256": L.sha256_file(L.HERE / "l1temp.py")}
    L.write_json(p.tfrozen, rec, mode=0o444)
    return rec


# ------------------------------------------------------------------ answers
def validate_answers(suite: list, answers: dict, name: str):
    """Before the look is taken: every call answered, keys exactly the item's options (yes/no: yes, no), finite, sum 1. Content-free refusals."""
    import math
    ids = {it["id"] for it in suite}
    if set(answers) != ids:
        L.refuse(f"{name}: the answer file does not cover exactly the suite's calls")
    for it in suite:
        pr = answers[it["id"]]
        keys = ["yes", "no"] if it["qtype"] == "noul" else list(it["options"])
        if set(pr) != set(keys) or any(not isinstance(v, (int, float)) or not math.isfinite(v) or v < 0 for v in pr.values()) \
                or abs(sum(pr.values()) - 1.0) > 1e-6:
            L.refuse(f"{name}: an answer is not a valid probability vector")


def write_answers(p: L.L1Paths, suite: list, T: dict, mode: str) -> dict:
    """raw (T = 1 as served) -> T applied per type -> answers/c?_ohs4.jsonl (read-only). Returns {key: path}. BOTH models' answers are computed and validated
    before either file is written; a re-run must reproduce the same bytes."""
    qt = {it["id"]: it["qtype"] for it in suite}
    todo = []
    for key, name, dest in (("c1", L.C1_READ, p.c1_answers), ("c2", L.C2_READ, p.c2_answers)):
        if key == "c2" and mode != "c1c2":
            continue
        rows = _jsonl(p.raw_dir / f"{name}_raw.jsonl")
        ans = {r["id"]: LT.apply_T(r["probs"], qt[r["id"]], T[key]) for r in rows if r["id"] in qt}
        validate_answers(suite, ans, key)
        data = "".join(json.dumps({"id": it["id"], "probs": ans[it["id"]]}) + "\n" for it in suite).encode()
        if dest.exists() and dest.read_bytes() != data:
            L.refuse(f"{dest.name} exists and differs from a recomputation")
        todo.append((key, dest, data))
    files = {}
    for key, dest, data in todo:                                  # nothing is written unless every model's answers are valid
        if not dest.exists():
            p.answers.mkdir(parents=True, exist_ok=True)
            tmp = dest.with_name(dest.name + ".tmp")
            tmp.write_bytes(data)
            os.replace(tmp, dest)
            os.chmod(dest, 0o444)
        files[key] = dest
    return files


def check_raw_files(p: L.L1Paths, rec: dict, mode: str):
    """The raw reads must be the bytes the GPU job returned: sha256 against run_record.json (and RAW_RUN.json)."""
    rr = L.read_json(p.raw_dir / "RAW_RUN.json") or {}
    for name in (L.C1_READ, *( [L.C2_READ] if mode == "c1c2" else [])):
        f = p.raw_dir / f"{name}_raw.jsonl"
        want = (rec.get("files") or {}).get(f"sealed raw {name}")
        if not f.exists() or not want or L.sha256_file(f) != want or (rr.get("files") or {}).get(f"sealed raw {name}") not in (None, want):
            L.refuse(f"{name}_raw.jsonl differs from the sha256 in the GPU job's run record (or is missing)")


def recompute_scorer_output(S, p: L.L1Paths, suite: list, files: dict) -> dict:
    """What run_look("L1") prints, rebuilt WITHOUT a look from the sha-checked answer files with the scorer's own pure functions (report, compare)."""
    recs = {k: S.evaluate(suite, S.load_answers(str(f))) for k, f in files.items()}
    res = {"look": "L1", "suite_sha256": L.sha256_file(p.suite), "reports": [S.report(suite, recs[k], k) for k in recs]}
    if "c2" in recs:
        res["comparisons"] = [S.compare(suite, recs["c2"], recs["c1"], "C2 - C1")]
    res["recomputed_without_a_second_look"] = True
    return res


# ------------------------------------------------------------------ the look
def take_look(p: L.L1Paths, S, files: dict) -> dict:
    buf = []
    rc = S.run_look("L1", {k: str(v) for k, v in files.items()}, suite_path=str(p.suite), looks_path=str(p.looks), out=buf.append)
    if rc != 0:
        why = ""
        try:
            why = json.loads(buf[0]).get("refused", "") if buf else ""
        except ValueError:
            pass
        L.refuse("the frozen scorer refused the look: " + str(why)[:120])
    out = json.loads(buf[0])
    L.write_json(p.scorer_out, out, mode=0o444)
    return out


def finish(p: L.L1Paths, *, pins=None, scorer_sha: str | None = None, out=say, trained_families=None) -> dict:
    L.require_pins(p, pins)
    if p.result.exists():
        L.refuse(f"{p.result.name} exists: the L1 look was already taken (one look only)")
    rr = raw_run(p)
    run_id, mode = rr["run_id"], rr["mode"]
    rec = L.read_json(p.out_root / run_id / "run_record.json") or {}
    if not rec.get("ok"):
        L.refuse("the GPU job's run record is missing or not ok")
    check_raw_files(p, rec, mode)
    go = L.load_owner_go(p)
    cand = L.load_candidate(p)
    pg = L.load_pregate(p, cand)
    if ("c1c2" if pg["effective_pass"] else "c1") != mode:
        L.refuse("the pre-gate result changed since the GPU job (mode differs)")
    was = rr.get("pregate") or {}
    if was.get("waiver_sha256") != pg["waiver_sha256"] or sorted(was.get("waived") or []) != sorted(pg["waived"]):
        L.refuse("the pre-gate waiver record changed since the GPU job")
    parity = None
    if mode == "c1c2":
        parity = L.load_parity(p, cand)
        if (rr.get("parity") or {}).get("sha256") != parity["sha256"]:
            L.refuse("the parity record changed since the GPU job")
        if pg["waived"]:
            L.check_a100_preconditions(p, cand)
    scorer_sha = scorer_sha or L.sha256_file(p.scorer)
    S = LV.load_scorer(p.scorer, scorer_sha)
    suite = S.load_suite(str(p.suite))
    problems = LV.suite_problems(suite)
    if problems:
        L.refuse("the suite lacks fields the rules need (checked before the look): " + "; ".join(problems[:6]))
    already = L.granted(L.read_looks(p), "L1")
    # 4: the temperature, from dev reads, BEFORE any sealed read is opened
    t = freeze_t(p, run_id, mode, trained_families)
    out(f"T frozen ({p.tfrozen.name}, sha256 {L.sha256_file(p.tfrozen)[:16]}): " + json.dumps(t["T"]))
    # 5: answers
    files = write_answers(p, suite, t["T"], mode)
    out("answer files written (read-only): " + ", ".join(f.name for f in files.values()))
    # 6: the look
    extra_disclosure = []
    if already:
        looks = [x for x in L.read_looks(p) if x.get("look") == "L1" and x.get("status") == "granted"]
        for k, f in files.items():
            if (looks[0].get("sha256") or {}).get(k) != L.sha256_file(f):
                L.refuse("an answer file differs from the one the granted L1 look scored")
        scorer_out = L.read_json(p.scorer_out)
        if isinstance(scorer_out, dict):
            out("L1 was already granted: the saved scorer output is used (no second look)")
        else:                                           # crash after the scorer logged the look, before its output was saved
            scorer_out = recompute_scorer_output(S, p, suite, files)
            L.write_json(p.scorer_out, scorer_out, mode=0o444)
            extra_disclosure.append("The scorer's printed output of the L1 look was not saved (a crash after the look was granted). The aggregates in this result were "
                                    "recomputed from the sha-checked answer files with the scorer's own report and compare functions. No second look was taken: the "
                                    "look log holds one granted L1.")
            out("L1 was already granted and its output was not saved: recomputed from the sha-checked answer files (no second look)")
    else:
        scorer_out = take_look(p, S, files)
        out("L1 look taken (scorer granted)")
    # 7: the table
    recs = {k: S.evaluate(suite, S.load_answers(str(f))) for k, f in files.items()}
    if mode == "c1c2":
        tbl = LV.l1_rules(S, suite, recs["c1"], recs["c2"], bool(pg["effective_pass"]), waived={c_: L.WAIVER_RECORD for c_ in pg["waived"]},
                          scorer_out=scorer_out, parity=parity)
        verdict, report_only = tbl["rules"], tbl["report_only"]
    else:
        verdict = {"overall": {"all_pass": None, "text": "pre-gate FAILED (spec 7.2): C2 gets no OHS-4 look; C1 was read for J (C1 vs Jev) only"},
                   "S6": {"rule": LV.RULES["S6"], "pass": False}}
        report_only = {"ece_yesno_G+R+X": {"c1": round(LV.ece_yesno(suite, recs["c1"]), 4)}}
    sums = {f.name: L.sha256_file(f) for f in sorted(p.answers.glob("*.jsonl"))}
    sums.update({f"raw/{f.name}": L.sha256_file(f) for f in sorted(p.raw_dir.glob("*.jsonl"))})
    L.write_json(p.sums, sums, mode=0o444)
    result = {"disclosure": L.build_disclosures(p, pg, cand) + extra_disclosure,
              "look": "L1", "utc": L.utc(), "run_id": run_id, "mode": mode,
              "verdict": verdict, "report_only": report_only, "parity": parity,
              "pregate": {"pass": pg["pass"], "effective_pass": pg["effective_pass"], "failed": pg["failed"], "waived": pg["waived"],
                          "waiver_sha256": pg["waiver_sha256"], "decision": pg.get("decision"), "file": p.pregate.name},
              "candidate": {k: cand.get(k) for k in ("name", "grid_candidate", "adapter_sha256", "grid_sha256")},
              "owner_go2": {k: go.get(k) for k in ("go", "written_utc")},
              "T_frozen": {"file": p.tfrozen.name, "sha256": L.sha256_file(p.tfrozen), "T": t["T"], "group_kind": t["group_kind"],
                           "trained_families": t["trained_families"], "fit_rows": t["fit_rows"]},
              "answer_files_sha256": {k: L.sha256_file(f) for k, f in files.items()},
              "pins": {"MANIFEST.json": L.sha256_file(p.manifest), "suite": L.sha256_file(p.suite), "requests": L.sha256_file(p.requests),
                       "scorer": L.sha256_file(p.scorer), "jev_runner": L.sha256_file(p.jev_runner)},
              "rules": LV.RULES, "rules_sha256": LV.RULES_SHA,
              "job": {k: rec.get(k) for k in ("wall_s", "spent_usd", "path_sha256", "env")},
              "models": {n: {k: b.get(k) for k in ("adapter_sha256", "merge_manifest_sha256", "boot_s", "path_sha256", "config_sha256")}
                         for n, b in (rec.get("models") or {}).items()},
              "carried_rulings": list(L.CARRIED_RULINGS),
              "scorer_output": scorer_out, "tool_shas": tool_shas(),
              "note": "aggregates only; the answer files stay in the sealed folder, read-only, for J (the scorer re-verifies their sha256)"}
    L.write_json(p.result, result, mode=0o444)
    out(f"{p.result.name} written")
    out(verdict["overall"]["text"])
    return result


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("cmd", choices=["check", "finish", "freeze-t", "shas"])
    ap.add_argument("--lean", default=str(L.LEAN_DEFAULT))
    a = ap.parse_args(argv)
    p = L.L1Paths(a.lean)
    try:
        if a.cmd == "check":
            return check(p)
        if a.cmd == "shas":
            say(json.dumps(tool_shas(), indent=1))
            return 0
        if a.cmd == "freeze-t":
            L.require_pins(p)
            rr = raw_run(p)
            t = freeze_t(p, rr["run_id"], rr["mode"])
            say(json.dumps({"T": t["T"], "report_only_fits": t["report_only_fits"], "trained_families": t["trained_families"], "fit_rows": t["fit_rows"], "sha256": L.sha256_file(p.tfrozen)}, indent=1))
            return 0
        finish(p)
        return 0
    except L.Refused as e:
        say(str(e))
        return 2


if __name__ == "__main__":
    sys.exit(main())
