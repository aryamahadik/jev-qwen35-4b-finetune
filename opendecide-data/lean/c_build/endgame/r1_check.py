"""Round-1 pre-flight and in-run checks (RUNBOOK D; r1_chain.sh runs them). Read-only except its JSON records in
c_build/endgame/logs/ (and r1_stop_after_min.txt). EXIT CODE: 0 only on GO, 1 on REFUSED / ABORT / STOP, so every launch
is chained with `&&` (r1_chain.sh).

  preflight   before launch: config filled and equal to the template except the FILL keys; the training files match
              the mixer manifest; mix report clean; G13 logs (c_build/decontam_g13.py; RUNBOOK B) for every mixed
              family, the shared seeds (packs, formats; spec 7.2) and final_mix_r1: present, complete (no target
              missing / pending the owner, every method run), not stale (input sha256), seeds clean, and 0 hits
              left on the final mix; pre-smoke
              passed with every loss finite (A20 d; A4 finite on the smoke); init on aryamhd = C1 sha
              (COPY_RECORD.json); PROJECTED COST <= $55 (PREREG A28 a; was $35) incl. the +12% s/step sensitivity
              at parity arm A's 2.754 s/step, AND (A28, added) <= $55 at the measured real-mix s/step, central 4.63
              and high 4.9 (c_build/endgame/logs/r1_speed_analysis.md, Verification 2); no app running on
              aryamhd; aryamhd billing baseline recorded (proj uses it).
              Recipe 4 items 9-11 and 5 / 11 step 3 / 6, each a record or an OWNER waiver (see WAIVERS):
                F2   c_build/f2_l4.json == c_build/f2_local_mac.json (6 rendered-prompt sha256s; train == gate_serve)
                A4   tests/test_ordinal_a4.py passes (CPU unit test); finite: pre-smoke losses + check_rows + in-run abort
                snapmon     recipe 5 stop rule driver: endgame/snap_monitor.py + logs/snap_monitor_cputest.json pass,
                            and that record's sha256s are the current snap_monitor.py and tests/test_snap_monitor.py;
                            no monitor state / stop record of an earlier run (gate_c reads them: no candidate when the
                            rule fired or the snapshots were not all read) and no monitor already running
                fam1_step0  FAM-1 step-0 read on C1 (L4), PREREG A23: logs/fam1_step0_c1.json must exist with
                            wall_min, controls_pass (true OR false) and flags; all three are REPORTED in the
                            record. Report-only (recipe 11 step 6): controls need not pass and no waiver is needed;
                            failed controls mark the FAM-1 diagnostics invalid for round 1 (they decide nothing)
                gate_c      endgame/gate_c.py + its CPU tests (endgame/tests/test_gate_c.py) pass (recipe 11 step 3)
                score_nd_cli  endgame/SCORE_ND_CLI.json (score_nd_cli.py write): the A15 scorer sha256 still matches
                            the file, the commands are complete and the sandboxed fake-input dry run passed
  first100    after segment 0-100 (logs/relay_q35_4b_c_r1_stopped_at_100.json, log_every 1): PREREG A21 (c) abort
              rules: any NaN/inf loss; a loss > 3 x C1's start loss (3 x 0.9367 = 2.810); fewer than 95 step records
              (the trainer's check_rows / a crash stopped it); s/step over steps 10-99 > 2 x 2.754 = 5.508.
  proj        after segment 100-300 (..._stopped_at_300.json): s/step over steps 100-300 -> projected round-1 total
              = max(n_steps x s/step x $/h + $2, spent so far + rest x s/step x $/h + $2); STOP if > $55 (recipe 4;
              A28 a, was $35). Spent so far = max(aryamhd metered - preflight baseline, segment wall time x $4.09/h
              from logs/r1_segments.jsonl). The budget left = floor((55 - spent so far - 2) / 4.09 x 60) minutes.
              A28 segments: the 10 h function timeout of train_relay35 (modal_od.py) is shorter than the ~12 h
              rest, so the rest runs as k = ceil(rest_min / (540 - 8)) relay segments, each capped at
              min(budget left, 540) min (600 min timeout - 60 min margin), each resuming from the checkpoint the
              last one saved at its cap. On GO it writes the FIRST post-300 segment's cap to
              logs/r1_stop_after_min.txt (relay --stop-after-min: an absolute end time that survives a preemption
              restart). STOP also if the budget is shorter than the rest of the run + k x 8 min (load/save per
              segment; k = 1 is the old rule): a run cut by the cap ends without `final`, so the owner decides first.
  seg         (A28; r1_chain.sh runs it after a post-300 segment that stopped at its cap without `final`) the
              same checks from the latest logs/relay_q35_4b_c_r1_stopped_at_<N>.json, the spend so far and
              s/step = max(proj's s/step 100-300, s/step measured after step 300): STOP if the projection > $55,
              if the budget left < rest + k x 8 min, or if the segment made no progress; on GO writes the next
              segment's cap = min(budget left, 540) to logs/r1_stop_after_min.txt.

  cap         (after a post-300 segment crash, owner OK) the same budget left from the spend so far, capped at 540
              min (A28: one segment under the 10 h function timeout); GO only if >= 10 min.
  relaunch    (A28 R2; `r1_chain.sh relaunch` runs it, then launches ONE segment through the chain's seg() record in
              logs/r1_segments.jsonl) STOP if `final` exists or an app still runs on aryamhd (or the app list
              fails: A28 R3 calls `modal app list --json` itself, STOP on exit != 0 or output that is not a JSON
              list), or the recipe 5 stop rule driver is not clear (A28 R3, `mon`); else exactly `cap`. A relaunch
              by hand (`modal run` outside r1_chain.sh) is not logged, so the
              next cap would miss its wall time while billing lags (~75 min): never relaunch by hand.
  Spent so far (A28 R2): a launch whose closed line has rc != 0, or whose open line has no closed line, may have run
              on to its --stop-after-min cap (--detach); it is counted to that capped window, bounded by the billing
              delta + every logged window's part in the last 75 min (spend_guard's lag). All launches closed with
              rc 0 (the normal chain): max(billing delta, wall) as before.
  mon         (A28 R3; the relaunch's view of the recipe 5 stop rule driver, which is not its child) exit 3 = rule
              fired (logs/snap_monitor_stop.json or state fired), 4 = escalated, 5 = logs/r1_monitor_dead.json
              (the monitor died under the chain or a relaunch), 2 = alive (logs/snap_monitor.pid names a live
              process), 0 = done (state: 25/50/75% read, rule not fired; or no snap_monitor.py + the owner's snapmon
              waiver, as the chain), 1 = not running and not done (rule unwatched). relaunch GOes only on 0 or 2.

WAIVERS: only the OWNER writes them, one line each in PREREG_FINAL.md:  OWNER-WAIVER r1-preflight <key>: <reason>
  (<key> in snapmon, gate_c, score_nd_cli; fam1_step0 / fam1_flags are no longer read, A23). Agents never write
  these lines.

  cd lean && ../.venv/bin/python c_build/endgame/r1_check.py preflight|first100|proj|seg|cap|relaunch|mon
Prints GO / ABORT / REFUSED / STOP as the last line.
"""
from __future__ import annotations

import json
import math
import os
import re
import subprocess
import sys
import time
from pathlib import Path

HERE = Path(__file__).resolve().parent
LEAN = HERE.parents[1]
LOGS = HERE / "logs"
NAME = "q35_4b_c_r1"
C1_START_LOSS = 0.9367          # C1's first logged loss (backups/modal_models/q35_4b_main500k/train_meta.json, step 0)
PARITY_A_SPS = 2.754            # A20 (c) parity arm A, 1 x H100 (c_build/ddp/PARITY_RESULT.json)
USD_H = 4.09                    # recipe 4 rate (Modal lists $3.95/h on 6 Oct; the higher one is used)
BILL_LAG_S = 75 * 60            # = spend_guard.LAG_S: Modal billing lags by up to about 1 h (A28 R2)
ALLOW, HARD_STOP, SENS = 2.0, 55.0, 1.12     # HARD_STOP: PREREG A28 (a), owner 6 Oct ~18:28 UTC (was 35.0)
LOAD_SAVE_MIN = 8.0             # per segment: image + 4B load + checkpoint / final save, inside its time cap
# A28: measured real-mix s/step (c_build/endgame/logs/r1_speed_analysis.md, Verification 2: central 4.63, range to 4.9).
# Preflight ADDS a check that the planned steps fit the hard stop at these rates too (the 2.754 x 1.12 check is kept).
A28_SPS_CENTRAL, A28_SPS_HIGH = 4.63, 4.9
# A28: train_relay35's Modal function timeout (modal_od.py: timeout=10 * 3600). Each post-300 segment is capped at
# 60 min under it (the end time counts from the client launch, so queue + load sit inside the cap).
FN_TIMEOUT_MIN, SEG_MARGIN_MIN = 600, 60
SEG_MAX_MIN = FN_TIMEOUT_MIN - SEG_MARGIN_MIN   # 540
INIT_SHA = "507d1c29690579f928a265713cd14b9c54a34baa8b74abd1e641560d987db078"
MODAL = str(LEAN.parent / ".venv/bin/modal")
PY = str(LEAN.parent / ".venv/bin/python")
PREREG = LEAN / "PREREG_FINAL.md"
WAIVER_RE = re.compile(r"^[>\s*-]*OWNER-WAIVER r1-preflight ([a-z0-9_]+):", re.M)   # a line of its own


def j(p: Path):
    try:
        return json.loads(p.read_text())
    except Exception:  # noqa: BLE001
        return None


def out(kind: str, rec: dict, verdict: str):
    LOGS.mkdir(parents=True, exist_ok=True)
    (LOGS / f"r1_check_{kind}.json").write_text(json.dumps({**rec, "decision": verdict}, indent=1))
    for k, v in rec.items():
        print(f"{k}: {json.dumps(v)[:150]}")
    print(verdict)
    sys.exit(0 if verdict == "GO" else 1)


def projection(n_steps: int, sps: float) -> float:
    return n_steps * sps * USD_H / 3600 + ALLOW


def budget_min(spent: float) -> int:
    """Minutes of H100 time left under the hard stop after `spent` dollars (the $2 allowance kept)."""
    return math.floor((HARD_STOP - spent - ALLOW) / USD_H * 60)


def segments_needed(need_min: float) -> int:
    """A28: relay segments for `need_min` minutes of training when each segment is capped at SEG_MAX_MIN, of which
    LOAD_SAVE_MIN go to load/save (1 for every rest that fits one segment: the old one-segment rule)."""
    return max(1, math.ceil(need_min / (SEG_MAX_MIN - LOAD_SAVE_MIN)))


def cost_check(n) -> tuple[dict, list]:
    """D1 cost (preflight): (record, problems). The recipe-4 formula at parity arm A's 2.754 s/step x 1.12 (unchanged,
    cap $55 under A28), plus the A28 check: the planned steps must also fit the hard stop at the measured real-mix
    s/step, central 4.63 and high 4.9 (r1_speed_analysis.md Verification 2). No +12% is applied to the measured rates:
    4.9 is the top of their measured range."""
    if not isinstance(n, int) or n <= 0:
        return {}, ["config fill has no dry_run_steps (the planned step count)"]
    p = []
    base, sens = projection(n, PARITY_A_SPS), projection(n, PARITY_A_SPS * SENS)
    rec = {"steps": n, "at_2.754": round(base, 1), "at_+12%": round(sens, 1), "hard_stop": HARD_STOP, "usd_per_h": USD_H}
    if sens > HARD_STOP:
        p.append(f"projected ${sens:.1f} at +12% s/step > ${HARD_STOP} hard stop")
    for tag, sps in (("central", A28_SPS_CENTRAL), ("high", A28_SPS_HIGH)):
        usd = projection(n, sps)
        rec[f"a28_at_{sps}"] = round(usd, 1)
        if usd > HARD_STOP:
            p.append(f"A28: projected ${usd:.1f} at the measured {tag} {sps} s/step > ${HARD_STOP} hard stop")
    return rec, p


def waivers() -> set:
    try:
        return set(WAIVER_RE.findall(PREREG.read_text()))
    except OSError:
        return set()


def pytest_ok(path: Path) -> bool:
    try:
        r = subprocess.run([PY, "-m", "pytest", "-q", "-p", "no:cacheprovider", str(path)], cwd=str(LEAN),
                           capture_output=True, text=True, timeout=140)
        return r.returncode == 0
    except Exception:  # noqa: BLE001
        return False


def f2_ok() -> str | None:
    """None if the F2 records agree, else the problem."""
    a, b = j(LEAN / "c_build/f2_l4.json"), j(LEAN / "c_build/f2_local_mac.json")
    if not a or not b:
        return "F2 rendered-prompt records missing (c_build/f2_l4.json, c_build/f2_local_mac.json)"
    if not a.get("sha") or a.get("sha") != b.get("sha") or len(a.get("sha") or {}) < 6:
        return "F2: rendered-prompt sha256s differ between the L4 and the Mac (or fewer than 6 views)"
    for rec in (a, b):
        pt = rec.get("paths") or {}
        tr, gs = pt.get("train") or {}, pt.get("gate_serve") or {}
        if not tr or any(tr.get(k) != gs.get(k) for k in ("chat_template_sha", "layout", "style", "chat_kwargs")):
            return f"F2: train and gate_serve paths differ ({rec.get('where')})"
    return None


def fam1_report(path: Path | None = None) -> tuple[dict, str | None]:
    """PREREG A23: the FAM-1 step-0 record must exist and is REPORTED (controls status, flags, wall time); it is
    report-only, so neither passing controls nor an owner waiver is required. Returns (report, problem or None)."""
    path = path or LOGS / "fam1_step0_c1.json"
    f1 = j(path)
    if not isinstance(f1, dict):
        return {"exists": False}, (f"FAM-1 step-0 record missing ({path.name}; PREREG A23: it must exist and be "
                                   "reported: run l4/fam1_rerun.sh)")
    cp, fl, wm = f1.get("controls_pass"), f1.get("flags"), f1.get("wall_min")
    rep = {"exists": True, "wall_min": wm, "controls_pass": cp,
           "valid_for_round1": cp is True,
           "flags": len(fl) if isinstance(fl, list) else fl,
           "flag_families": sorted({str(x).split(":")[0] for x in fl}) if isinstance(fl, list) else None,
           "a23": "report-only; " + ("controls passed" if cp is True else
                                    "controls FAILED: FAM-1 diagnostics invalid for round 1, they decide nothing")}
    v1 = j(path.with_name("fam1_step0_c1.v1_randlabel.json"))
    if isinstance(v1, dict):
        rep["v1_randlabel"] = {"controls_pass": v1.get("controls_pass"), "wall_min": v1.get("wall_min"),
                               "flags": len(v1.get("flags") or [])}
    miss = [k for k, ok in (("wall_min", isinstance(wm, (int, float)) and not isinstance(wm, bool)),
                            ("controls_pass", isinstance(cp, bool)), ("flags", isinstance(fl, list))) if not ok]
    if miss:
        return rep, f"FAM-1 step-0 record incomplete: {miss} not reported (PREREG A23)"
    return rep, None


def extra_checks(p: list, rec: dict) -> None:
    """Recipe 4 items 9-11, recipe 5 stop-rule driver, FAM-1 step 0, gate path (recipe 11 steps 3 and 6)."""
    w = waivers()
    rec["waivers"] = sorted(w)
    e = f2_ok()
    if e:
        p.append(e)
    if not pytest_ok(LEAN / "tests/test_ordinal_a4.py"):
        p.append("A4 unit test (tests/test_ordinal_a4.py) fails: the A4 fallback (lam_ord 0, logged) needs the owner")
    sm_err = "endgame/snap_monitor.py missing"
    if (HERE / "snap_monitor.py").exists():
        try:
            import snap_monitor  # noqa: E402
            sm_err = snap_monitor.cputest_ok()
        except Exception as ex:  # noqa: BLE001
            sm_err = f"snap_monitor import failed ({type(ex).__name__})"
    if sm_err and "snapmon" not in w:
        p.append(f"recipe 5 stop rule has no driver (B6): {sm_err}; run snap_monitor.py cputest, or OWNER-WAIVER "
                 "r1-preflight snapmon")
    stale = [q.name for q in (LOGS / "snap_monitor_state.json", LOGS / "snap_monitor_stop.json",
                              LOGS / "snap_monitor_escalation.json") if q.exists()]
    if stale:
        p.append(f"stop-rule monitor files of an earlier run exist ({stale}): round 1 needs a fresh monitor (recipe 5; "
                 "a re-run needs an amendment; owner)")
    try:
        import os
        os.kill(int((LOGS / "snap_monitor.pid").read_text().strip()), 0)
        p.append("a snap_monitor.py is already running (logs/snap_monitor.pid)")
    except (OSError, ValueError):
        pass
    f1, e = fam1_report()
    rec["fam1_step0"] = f1
    if e:
        p.append(e)
    gc = next((q for q in (HERE / "gate_c.py", LEAN / "gate_c.py", LEAN / "c_build/gate_c.py") if q.exists()), None)
    gt = next((q for q in (HERE / "tests/test_gate_c.py", LEAN / "tests/test_gate_c.py",
                           LEAN / "c_build/tests/test_gate_c.py") if q.exists()), None)
    if not (gc and gt and pytest_ok(gt)) and "gate_c" not in w:
        p.append("gate_c.py + CPU tests missing or failing (B2; recipe 11 step 3), or OWNER-WAIVER r1-preflight gate_c")
    try:
        import score_nd_cli  # noqa: E402
        sc_err = score_nd_cli.verify(HERE / "SCORE_ND_CLI.json")
    except Exception as ex:  # noqa: BLE001
        sc_err = f"score_nd_cli check failed ({type(ex).__name__})"
    if sc_err and "score_nd_cli" not in w:
        p.append(f"sealed scorer CLI record (B5): {sc_err}; run score_nd_cli.py write, or OWNER-WAIVER "
                 "r1-preflight score_nd_cli")
    e = app_list_problem("already running on aryamhd (two writers / unknown spend)")   # A28 R3: strict app list
    if e:
        p.append(e)


def preflight():
    from fill_config import KEYS, TEMPLATE, sha  # noqa: E402
    p, rec = [], {}
    cfg, tmpl = j(LEAN / f"runs/{NAME}.json") or {}, j(TEMPLATE)
    fill = j(LEAN / "c_build/mix_r1/config_fill_r1.json") or {}
    man = j(LEAN / "data/c_parts/c_mix_r1_manifest.json") or {}
    rep = j(LEAN / "c_build/mix_r1/mix_report_r1.json") or {}
    left = sorted(k for k, v in cfg.items() if isinstance(v, str) and v.startswith("FILL"))
    if left:
        p.append(f"config still FILL: {left}")
    if not tmpl:
        p.append("no config template (run fill_config.py)")
    else:
        diff = sorted(k for k in set(cfg) | set(tmpl) if cfg.get(k) != tmpl.get(k) and k not in KEYS)
        if diff:
            p.append(f"config differs from the template outside the FILL keys: {diff}")
    for name in ("c_train_r1.jsonl", "c_rel_r1.jsonl"):
        f = LEAN / "data/c_parts" / name
        if not f.exists() or sha(f) != ((man.get("files") or {}).get(name) or {}).get("sha256"):
            p.append(f"{name} missing or sha256 != manifest")
    if rep.get("problems"):
        p.append(f"mix report problems: {len(rep['problems'])}")
    sc = rep.get("sealed_check") or {}
    if sc.get("rows_hit") != 0:
        p.append(f"sealed_check on the mix: rows_hit {sc.get('rows_hit')}")
    fams = sorted({b for b in (man.get("counts") or {}).get("by_block", {}) if b.startswith("F") or b == "COMMIT"})
    try:
        sys.path.insert(0, str(HERE.parent))
        import decontam_g13  # noqa: E402
        g13 = decontam_g13.log_problems(fams + ["packs", "formats", "final_mix_r1"])
    except Exception as e:  # noqa: BLE001
        g13 = [f"G13 check failed ({type(e).__name__}: {str(e)[:80]})"]
    rec["g13"] = {"logs": fams + ["packs", "formats", "final_mix_r1"], "problems": len(g13)}
    p += g13
    sm = j(LEAN / "logs/pilot/speed_h100_mt8192_log_every-1.json") or {}
    if sm.get("oom") or not sm.get("probe_ok") or (sm.get("steps_run") or 0) < 30:
        p.append("pre-smoke (A20 d) missing or failed (RUNBOOK P1)")
    sl = [r.get("loss") for r in (sm.get("log") or []) if isinstance(r, dict) and "loss" in r]
    if sm and (not sl or any(not isinstance(x, (int, float)) or not math.isfinite(x) for x in sl)):
        p.append("pre-smoke: a non-finite or missing loss (A4 finite check on the smoke fails)")
    if ((j(HERE / "COPY_RECORD.json") or {}).get("aryamhd") or {}).get("q35_4b_main500k_init") != INIT_SHA:
        p.append("init adapter on aryamhd not verified (RUNBOOK D0)")
    cr, cp = cost_check(fill.get("dry_run_steps"))
    if cr:
        rec["projection_usd"] = cr
    p += cp
    try:
        b = json.loads(subprocess.run([MODAL, "billing", "summary", "--for", "this month", "--json", "--profile",
                                       "aryamhd"], capture_output=True, text=True, timeout=60).stdout)
        rec["aryamhd_billing"] = {"metered": b["metered_cost"][:7], "billed": b["billed_cost"][:7]}
        rec["baseline_metered_usd"] = float(b["metered_cost"])
        rec["baseline_unix"] = round(time.time())
    except Exception as e:  # noqa: BLE001
        p.append(f"billing check failed ({type(e).__name__})")
    extra_checks(p, rec)
    rec["problems"] = p
    out("preflight", rec, "REFUSED" if p else "GO")


def steps_of(meta: dict) -> list[dict]:
    return [r for r in (meta.get("log") or []) if isinstance(r, dict) and "step" in r]


def first100():
    meta = j(LEAN / f"logs/relay_{NAME}_stopped_at_100.json")
    if meta is None:
        return out("first100", {"problems": ["no logs/relay_q35_4b_c_r1_stopped_at_100.json (segment 1 not done "
                                             "or it crashed: read c_build/endgame/logs/r1_seg1.log)"]}, "ABORT")
    recs = [r for r in steps_of(meta) if r["step"] < 100]
    p = []
    losses = [r.get("loss") for r in recs]
    if any(x is None or not math.isfinite(x) for x in losses):
        p.append("NaN/inf (or missing) loss in the first 100 steps")
    fin = [x for x in losses if x is not None and math.isfinite(x)]
    if fin and max(fin) > 3 * C1_START_LOSS:
        p.append(f"loss {max(fin):.3f} > 3 x C1 start loss ({3 * C1_START_LOSS:.3f})")
    if len(recs) < 95:
        p.append(f"only {len(recs)} step records (log_every 1 expected 100): check_rows / crash?")
    t = {r["step"]: r.get("min") for r in recs}
    sps = None
    if 10 in t and 99 in t and t[99] is not None and t[10] is not None:
        sps = (t[99] - t[10]) * 60 / 89
        if sps > 2 * PARITY_A_SPS:
            p.append(f"s/step {sps:.2f} > 2 x parity arm A ({2 * PARITY_A_SPS:.3f})")
    else:
        p.append("cannot time steps 10-99")
    n = recs[0].get("of") if recs else None
    rec = {"records": len(recs), "loss_first": fin[:1], "loss_max": max(fin) if fin else None,
           "s_per_step_10_99": round(sps, 3) if sps else None, "n_steps": n,
           "projection_usd_at_this_rate": round(projection(n, sps), 1) if n and sps else None, "problems": p}
    out("first100", rec, "ABORT" if p else "GO")


def proj():
    meta = j(LEAN / f"logs/relay_{NAME}_stopped_at_300.json")
    if meta is None:
        return out("proj", {"problems": ["no logs/relay_q35_4b_c_r1_stopped_at_300.json"]}, "STOP")
    recs = [r for r in steps_of(meta) if 100 <= r["step"] <= 300 and r.get("min") is not None]
    seg, last = [], None                     # keep the records after the last restart of the clock
    for r in recs:
        if last is not None and r["min"] < last:
            seg = []
        seg.append(r)
        last = r["min"]
    if len(seg) < 2:
        return out("proj", {"problems": ["fewer than 2 timed records in steps 100-300"]}, "STOP")
    sps = (seg[-1]["min"] - seg[0]["min"]) * 60 / (seg[-1]["step"] - seg[0]["step"])
    n = seg[-1].get("of")
    if not isinstance(n, int) or n <= 300:
        return out("proj", {"problems": [f"n_steps unknown ({n!r})"]}, "STOP")
    spent, how = spent_so_far()
    if spent is None:
        return out("proj", {"problems": [how]}, "STOP")
    return _rest_verdict("proj", {"s_per_step_100_300": round(sps, 3)}, n, 300, sps, spent, how)


def _rest_verdict(kind: str, head: dict, n: int, at: int, sps: float, spent: float, how: str):
    """Recipe 4 / D4 on the rest of the run from step `at` (proj: at = 300; seg: the latest stop). Same formulas as
    the one-segment rule; A28 only adds the segment split (k segments, k load/saves, each cap <= SEG_MAX_MIN)."""
    rest_usd = (n - at) * sps * USD_H / 3600
    usd = max(projection(n, sps), spent + rest_usd + ALLOW)
    stop_min = budget_min(spent)
    need_min = (n - at) * sps / 60
    k = segments_needed(need_min)
    seg_min = min(stop_min, SEG_MAX_MIN)
    rec = {**head, "n_steps": n, "spent_so_far_usd": round(spent, 2), "spent_how": how,
           "projected_usd": round(usd, 1), "hard_stop": HARD_STOP, "stop_after_min": stop_min,
           "need_min_for_rest": round(need_min, 1),
           "a28": {"from_step": at, "segments_left": k, "seg_cap_min": seg_min, "seg_max_min": SEG_MAX_MIN,
                   "need_min_incl_load_save": round(need_min + k * LOAD_SAVE_MIN, 1)}}
    if usd > HARD_STOP or stop_min <= 0:
        return out(kind, rec, "STOP: projection above the hard stop, ask the owner")
    if stop_min < need_min + k * LOAD_SAVE_MIN:   # the cap would cut the run before `final`: no candidate, $ lost
        return out(kind, rec, f"STOP: the rest needs {need_min + k * LOAD_SAVE_MIN:.0f} min (incl. {k} load/save) but "
                              f"the ${HARD_STOP:g} cap leaves {stop_min} min; ask the owner")
    (LOGS / "r1_stop_after_min.txt").write_text(f"{seg_min}\n")
    out(kind, rec, "GO")


def last_seg_start() -> float:
    """Start (unix) of the last segment in logs/r1_segments.jsonl (0 if none)."""
    t = 0.0
    segf = LOGS / "r1_segments.jsonl"
    for line in (segf.read_text().splitlines() if segf.exists() else []):
        try:
            t = max(t, float(json.loads(line)["start"]))
        except (ValueError, KeyError, TypeError):
            continue
    return t


def stopped_at() -> dict:
    """{N: path} of logs/relay_<NAME>_stopped_at_<N>.json (relay writes one per segment that stopped), only files
    written since the last segment started (a file left by an earlier attempt is not this segment's stop)."""
    got, t0 = {}, last_seg_start()
    for q in (LEAN / "logs").glob(f"relay_{NAME}_stopped_at_*.json"):
        m = re.fullmatch(rf"relay_{NAME}_stopped_at_(\d+)\.json", q.name)
        if m and q.stat().st_mtime >= t0 - 1:
            got[int(m.group(1))] = q
    return got


def seg():
    """A28: after a post-300 segment ended at its time cap without `final` (r1_chain.sh runs this between segments):
    the next segment's cap from the budget left under the hard stop, with the D4 checks on the rest of the run."""
    if (LEAN / f"logs/relay_{NAME}_final.json").exists():
        return out("seg", {"problems": ["logs/relay_q35_4b_c_r1_final.json exists: nothing left to run"]}, "STOP")
    pr = j(LOGS / "r1_check_proj.json") or {}
    if pr.get("decision") != "GO" or not isinstance(pr.get("s_per_step_100_300"), (int, float)):
        return out("seg", {"problems": ["no GO record of r1_check.py proj (D4)"]}, "STOP")
    prev = max(300, int((j(LOGS / "r1_check_seg.json") or {}).get("from_step") or 0))
    got = stopped_at()
    at = max(got) if got else None
    if at is None or at <= prev:
        return out("seg", {"problems": [f"no progress: latest stopped_at {at} <= {prev} (the step the last segment "
                                        "started from)"], "from_step": prev}, "STOP")
    meta = j(got[at]) or {}
    recs = [r for r in steps_of(meta) if r["step"] >= 300 and r.get("min") is not None]
    run, last = [], None                     # keep the records after the last restart of the clock (as proj)
    for r in recs:
        if last is not None and r["min"] < last:
            run = []
        run.append(r)
        last = r["min"]
    sps_post = None
    if len(run) >= 2 and run[-1]["step"] > run[0]["step"]:
        sps_post = (run[-1]["min"] - run[0]["min"]) * 60 / (run[-1]["step"] - run[0]["step"])
    sps = max(x for x in (float(pr["s_per_step_100_300"]), sps_post) if x is not None)
    n = meta.get("steps") or (recs[-1].get("of") if recs else None)
    if not isinstance(n, int) or n <= at:
        return out("seg", {"problems": [f"n_steps unknown ({n!r}) or not above the stop {at}"], "from_step": at}, "STOP")
    spent, how = spent_so_far()
    if spent is None:
        return out("seg", {"problems": [how], "from_step": at}, "STOP")
    head = {"from_step": at, "s_per_step_100_300": pr["s_per_step_100_300"],
            "s_per_step_after_300": round(sps_post, 3) if sps_post else None, "s_per_step_used": round(sps, 3)}
    return _rest_verdict("seg", head, n, at, sps, spent, how)


def cap():
    """Relaunch cap after a post-300 segment crash (owner OK first): minutes left under the hard stop from the spend
    so far, at most SEG_MAX_MIN (A28: one segment must end under the 10 h function timeout)."""
    spent, how = spent_so_far()
    if spent is None:
        return out("cap", {"problems": [how]}, "STOP")
    stop_min = budget_min(spent)
    rec = {"spent_so_far_usd": round(spent, 2), "spent_how": how, "stop_after_min": stop_min, "hard_stop": HARD_STOP,
           "seg_cap_min": min(stop_min, SEG_MAX_MIN)}
    if stop_min < 10:
        return out("cap", rec, f"STOP: under 10 min left before the ${HARD_STOP:g} hard stop")
    (LOGS / "r1_stop_after_min.txt").write_text(f"{min(stop_min, SEG_MAX_MIN)}\n")
    out("cap", rec, "GO")


def relaunch():
    """A28 R2: the D5 crash relaunch (owner OK first). `r1_chain.sh relaunch` runs this and then ONE segment through
    the chain's seg() record (logs/r1_segments.jsonl), so the next `cap` / `relaunch` counts that segment's wall time
    even while billing lags. STOP if `final` exists or an app still runs on aryamhd (two writers on one folder, spend
    not yet known; also STOP when the app list fails); else exactly `cap` (record r1_check_cap.json, cap file)."""
    p = []
    if (LEAN / f"logs/relay_{NAME}_final.json").exists():
        p.append(f"logs/relay_{NAME}_final.json exists: nothing left to run")
    e = app_list_problem("still running on aryamhd (two writers / spend not known yet)")   # A28 R3: strict
    if e:
        p.append(e)
    code, why = mon_status()                       # A28 R3: never resume training past the recipe 5 stop rule
    if code not in (0, 2):
        p.append(f"recipe 5 stop rule driver (mon {code}): {why}")
    if p:
        return out("relaunch", {"problems": p}, "STOP")
    return cap()


def running_apps_strict(profile: str = "aryamhd") -> list[dict]:
    """A28 R3: `modal app list --json`, called here and checked. spend_guard.running_apps reads an empty stdout as
    no apps and never looks at the exit code, so an auth / network failure (exit != 0, the error on stderr) looked
    like "nothing running". Here: raise on exit != 0, a timeout, a missing binary, or output that is not a JSON
    list (the real CLI prints [] when nothing runs). The running filter is spend_guard.running_apps's, unchanged."""
    r = subprocess.run([MODAL, "app", "list", "--json"], capture_output=True, text=True, timeout=90,
                       env={**os.environ, "MODAL_PROFILE": profile})
    if r.returncode != 0:
        raise RuntimeError(f"exit {r.returncode}: {(r.stderr or '').strip()[-120:]}")
    rows = json.loads(r.stdout)                   # empty / not JSON: ValueError
    if not isinstance(rows, list) or not all(isinstance(a, dict) for a in rows):
        raise ValueError("app list output is not a JSON list of apps")
    apps = []
    for a in rows:
        state = str(a.get("State") or a.get("state") or "").lower()
        tasks = int(a.get("Tasks") or a.get("tasks") or 0)
        if state != "stopped" and (tasks > 0 or "ephemeral" in state or "detached" in state):
            apps.append({"id": a.get("App ID") or a.get("app_id"), "desc": a.get("Description") or a.get("description"),
                         "state": state, "tasks": tasks})
    return apps


def app_list_problem(what: str) -> str | None:
    """A problem line when the aryamhd app list fails (any error: STOP) or shows a running app; None when clear."""
    try:
        run = running_apps_strict("aryamhd")
    except Exception as ex:  # noqa: BLE001
        return f"aryamhd app list failed ({type(ex).__name__}: {str(ex)[:120]})"
    return f"{len(run)} app(s) {what}: {run[:2]}" if run else None


MON_FRACS = ("0.25", "0.5", "0.75")             # = snap_monitor.FRACS (the 25/50/75% snapshot reads)


def _pid_alive(f: Path) -> int | None:
    try:
        pid = int(f.read_text().strip())
    except (OSError, ValueError):
        return None
    if pid <= 1:                                  # os.kill(0, 0) would signal our own process group
        return None
    try:
        os.kill(pid, 0)
    except OSError:                               # gone (or not ours): not alive
        return None
    return pid


def mon_status() -> tuple[int, str]:
    """A28 R3: the recipe 5 stop rule driver as a relaunch sees it (codes in the module doc, `mon`). The chain's own
    records first (logs/snap_monitor_stop.json, snap_monitor_escalation.json, r1_monitor_dead.json), then the
    monitor's state and lock file (snap_monitor.py writes logs/snap_monitor.pid while it runs)."""
    for code, name, why in ((3, "snap_monitor_stop.json", "recipe 5 stop rule fired: NO candidate this round"),
                            (4, "snap_monitor_escalation.json", "snap monitor ESCALATED: NO candidate until the owner "
                                                                "decides"),
                            (5, "r1_monitor_dead.json", "snap monitor died (stop rule unwatched): owner decides")):
        if (LOGS / name).exists():
            return code, f"logs/{name} exists: {why}"
    st = j(LOGS / "snap_monitor_state.json") or {}
    if st.get("fired"):
        return 3, "snap_monitor_state.json: rule fired: NO candidate this round"
    if st.get("escalated"):
        return 4, "snap_monitor_state.json: escalated: NO candidate until the owner decides"
    pid = _pid_alive(LOGS / "snap_monitor.pid")
    if pid:
        return 2, f"snap monitor running (pid {pid})"
    if not (HERE / "snap_monitor.py").exists():
        pre = LEAN / "PREREG_FINAL.md"
        if "snapmon" in set(WAIVER_RE.findall(pre.read_text() if pre.exists() else "")):
            return 0, "no snap_monitor.py; owner snapmon waiver (as the chain's seg3)"
        return 1, "no snap_monitor.py and no owner snapmon waiver"
    reads = st.get("reads") or {}
    if st.get("name") == NAME and all(f in reads for f in MON_FRACS):
        return 0, "snap monitor done: 25/50/75% read, rule did not fire"
    return 1, (f"snap monitor not running and not done (reads {sorted(reads)}): start it first, from lean/: nohup "
               f"../.venv/bin/python c_build/endgame/snap_monitor.py watch --profile aryamhd --name {NAME} >> "
               "c_build/endgame/logs/snap_monitor.log 2>&1 &")


def mon():
    code, why = mon_status()
    print(json.dumps({"mon": code, "why": why}))
    sys.exit(code)


CAP_RE = re.compile(r"--stop-after-min\s+(\d+(?:\.\d+)?)")


def _seg_launches():
    """A28 R2: the launches in logs/r1_segments.jsonl as (start, end, ok, cap_s). r1_chain.sh seg() writes an OPEN
    line ({"seg", "start", "open": true, "args"}) right before each launch and the closed line ({"seg", "start",
    "end", "rc", "args"}) after it. ok = closed with rc 0 (the client saw the app end: its wall time is the segment's
    time). Not ok = closed with rc != 0 (the client died or the app crashed: a --detach app may run on to its cap) or
    an open line without its closed line (the chain / relaunch died mid-segment): end None. cap_s from the
    --stop-after-min in args (None if absent)."""
    segf = LOGS / "r1_segments.jsonl"
    opened, out_ = {}, []
    for line in (segf.read_text().splitlines() if segf.exists() else []):
        try:
            r = json.loads(line)
            s = float(r["start"])
        except (ValueError, KeyError, TypeError):
            continue
        m = CAP_RE.search(str(r.get("args") or ""))
        cap_s = float(m.group(1)) * 60 if m else None
        if r.get("open") is True:
            opened[(str(r.get("seg")), s)] = cap_s
            continue
        try:
            e = float(r["end"])
        except (ValueError, KeyError, TypeError):
            continue
        opened.pop((str(r.get("seg")), s), None)
        out_.append((s, e, r.get("rc") == 0, cap_s))
    out_ += [(s, None, False, cap_s) for (_, s), cap_s in opened.items()]
    return out_


def spent_so_far():
    """(usd, how): max of the billing delta since preflight and the segments' wall time x $4.09/h.
    A28 R2: when a logged launch is not ok (client exit != 0, or no closed line: the app may have run on to its cap
    under --detach), it is counted up to its capped window too, but never above what billing + the last BILL_LAG_S
    of every logged window can hold: spent = max(wall, billing delta, min(wall with the capped windows, billing delta
    + the windows' part in the last 75 min)). With every launch ok (the chain's normal path) this is the old
    max(wall, billing delta) exactly."""
    pf = j(LOGS / "r1_check_preflight.json") or {}
    base = pf.get("baseline_metered_usd")
    wall_s = 0.0
    segf = LOGS / "r1_segments.jsonl"
    if segf.exists():
        for line in segf.read_text().splitlines():
            try:
                r = json.loads(line)
                wall_s += float(r["end"]) - float(r["start"])
            except (ValueError, KeyError, TypeError):
                continue
    if base is None and wall_s == 0:
        return None, "no preflight billing baseline and no logs/r1_segments.jsonl: spend so far unknown"
    wall_usd = wall_s / 3600 * USD_H
    bill_usd, bill_known = 0.0, False
    try:
        b = json.loads(subprocess.run([MODAL, "billing", "summary", "--for", "this month", "--json", "--profile",
                                       "aryamhd"], capture_output=True, text=True, timeout=60).stdout)
        if base is not None:
            bill_usd = float(b["metered_cost"]) - float(base)
            bill_known = True
    except Exception:  # noqa: BLE001
        pass
    how = f"wall {wall_usd:.2f} (segments {wall_s / 60:.0f} min), billing delta {bill_usd:.2f}"
    launches = _seg_launches()
    unsure = [x for x in launches if not x[2]]
    if not unsure:
        return max(wall_usd, bill_usd), how
    now = time.time()
    ub_wall_s = lag_s = 0.0
    for s, e, ok, cap_s in launches:
        if ok:
            hi = e
        else:                                # may have run on to its cap (to now if no cap is known)
            hi = min(now, s + cap_s) if cap_s is not None else now
            hi = max(hi, e if e is not None else s)
        ub_wall_s += max(0.0, hi - s)
        lag_s += max(0.0, hi - max(s, now - BILL_LAG_S))
    ub_wall = ub_wall_s / 3600 * USD_H
    ub_bill = bill_usd + lag_s / 3600 * USD_H if bill_known else math.inf
    unsure_usd = min(ub_wall, ub_bill)
    how += (f"; {len(unsure)} launch(es) not closed with rc 0 counted to their caps: wall bound {ub_wall:.2f}, "
            f"billing + last {BILL_LAG_S // 60} min bound " + (f"{ub_bill:.2f}" if bill_known else "unknown"))
    return max(wall_usd, bill_usd, unsure_usd), how


if __name__ == "__main__":
    sys.path.insert(0, str(HERE))
    {"preflight": preflight, "first100": first100, "proj": proj, "seg": seg, "cap": cap,
     "relaunch": relaunch, "mon": mon}[sys.argv[1] if len(sys.argv) > 1 else "preflight"]()
