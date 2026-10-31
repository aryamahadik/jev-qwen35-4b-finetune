"""PREREG A28 (a): round-1 hard stop $35 -> $55, preflight check at the measured real-mix s/step, and the post-300 run
split into relay segments under the 10 h function timeout. CPU only; nothing is launched.

- r1_check.py: the new caps / projection numbers, the segment arithmetic, `seg` and `cap`.
- old vs new: r1_check.py.pre_a28 and r1_chain.sh.pre_a28 (the $35 versions) against the new files on the same $35
  inputs (the new module's HARD_STOP set back to 35 in the test only): same verdicts, records and launches.
- r1_chain.sh end to end with the REAL r1_check.py (proj / seg) and a FAKE modal binary that simulates the relay
  (resume, absolute end time, 10 h timeout, billing), so the segment count, per-segment minutes and resume flags are
  checked."""
import importlib.machinery
import importlib.util
import json
import math
import os
import re
import shutil
import stat
import subprocess
import sys
import types
from pathlib import Path

import pytest

HERE = Path(__file__).resolve().parent
E = HERE.parent
LEAN = E.parents[1]
sys.path.insert(0, str(E))
import r1_check as rc  # noqa: E402


def load(path: Path, name: str):
    spec = importlib.util.spec_from_file_location(name, path,
                                                  loader=importlib.machinery.SourceFileLoader(name, str(path)))
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


OLD = load(E / "r1_check.py.pre_a28", "r1_check_pre_a28")


# ---------------------------------------------------------------- constants and the A28 numbers
def test_constants_only_the_cap_changed():
    assert rc.HARD_STOP == 55.0 and OLD.HARD_STOP == 35.0
    for k in ("ALLOW", "SENS", "PARITY_A_SPS", "USD_H", "LOAD_SAVE_MIN", "C1_START_LOSS", "INIT_SHA", "NAME"):
        assert getattr(rc, k) == getattr(OLD, k), k
    assert 2 * rc.PARITY_A_SPS == pytest.approx(5.508)          # D3 first-100 abort rule unchanged
    assert rc.SEG_MAX_MIN == 540 and rc.FN_TIMEOUT_MIN - rc.SEG_MAX_MIN == 60


def test_function_timeout_matches_modal_od():
    """The segment cap is derived from train_relay35's timeout (modal_od.py read only)."""
    src = (LEAN / "modal_od.py").read_text()
    m = re.search(r"@app\.function\(([^\n]*)\)\ndef train_relay35\(", src)
    assert m, "train_relay35 decorator not found"
    t = re.search(r"timeout=([0-9 *]+)", m.group(1)).group(1)
    assert eval(t) == rc.FN_TIMEOUT_MIN * 60                      # noqa: S307 (digits and * only)
    assert "stop_at_unix" in src and "expect_resume" in src


def test_preflight_cost_numbers():
    for n, a, s, c, h in ((9270, 31.0, 34.5, 50.8, 53.6), (9375, 31.3, 34.9, 51.3, 54.2)):
        rec, p = rc.cost_check(n)
        assert p == [] and rec["hard_stop"] == 55.0
        assert (rec["at_2.754"], rec["at_+12%"], rec["a28_at_4.63"], rec["a28_at_4.9"]) == (a, s, c, h)
    # refusal edges: high 4.9 above 9,520 steps, central 4.63 above 10,075, the old formula above 15,124
    assert rc.cost_check(9520)[1] == [] and len(rc.cost_check(9521)[1]) == 1 and "high 4.9" in rc.cost_check(9521)[1][0]
    assert rc.cost_check(10075)[1] and all("high" in x for x in rc.cost_check(10075)[1])
    assert len(rc.cost_check(10076)[1]) == 2
    assert not any("+12%" in x for x in rc.cost_check(15124)[1]) and any("+12%" in x for x in rc.cost_check(15125)[1])
    assert rc.cost_check(None) == ({}, ["config fill has no dry_run_steps (the planned step count)"])


def test_segments_needed_boundaries():
    assert [rc.segments_needed(x) for x in (0, 100, 532, 532.01, 1064, 1064.1)] == [1, 1, 1, 2, 2, 3]
    assert rc.budget_min(2.12) == 746 and rc.budget_min(38.93) == 206


# ---------------------------------------------------------------- sandboxes for the module-level checks
def sandbox(tmp: Path, mod, monkeypatch, spent=None):
    lean = tmp / "lean"
    here = lean / "c_build/endgame"
    for d in (here / "logs", lean / "logs", lean / "c_build/mix_r1"):
        d.mkdir(parents=True, exist_ok=True)
    monkeypatch.setattr(mod, "LEAN", lean)
    monkeypatch.setattr(mod, "HERE", here)
    monkeypatch.setattr(mod, "LOGS", here / "logs")
    monkeypatch.setattr(mod, "MODAL", str(tmp / "no_modal_here"))
    if spent is not None:
        monkeypatch.setattr(mod, "spent_so_far", lambda: (spent, "test"))
    return lean, here


def run(fn):
    with pytest.raises(SystemExit) as e:
        fn()
    return e.value.code


def write_stop(lean: Path, at: int, n: int, sps: float, start: int = 100, every: int = 50, min0: float = 10.0):
    log = [{"step": s, "loss": 0.5, "min": round(min0 + (s - start + 1) * sps / 60, 2), "of": n}
           for s in range(start, at) if s % every == 0]
    (lean / f"logs/relay_q35_4b_c_r1_stopped_at_{at}.json").write_text(
        json.dumps({"cfg": {}, "steps": n, "stopped_at_step": at, "log": log}))


def preflight_record(mod, tmp, monkeypatch, n):
    lean, here = sandbox(tmp, mod, monkeypatch)
    (lean / "c_build/mix_r1/config_fill_r1.json").write_text(json.dumps({"dry_run_steps": n}))
    monkeypatch.setattr(mod, "extra_checks", lambda p, rec: None)
    fake = types.ModuleType("decontam_g13")
    fake.log_problems = lambda names: []
    monkeypatch.setitem(sys.modules, "decontam_g13", fake)
    assert run(mod.preflight) == 1                               # the empty sandbox always refuses
    return json.loads((here / "logs/r1_check_preflight.json").read_text())


@pytest.mark.parametrize("n", [8880, 9270, 9375, 9416, 9417, 12000, 0])
def test_preflight_old_vs_new_on_35_inputs(tmp_path, monkeypatch, n):
    """Same record and problems as the $35 version when the new cap is set back to 35, except the added A28 check."""
    old = preflight_record(OLD, tmp_path / "old", monkeypatch, n)
    monkeypatch.setattr(rc, "HARD_STOP", 35.0)
    new = preflight_record(rc, tmp_path / "new", monkeypatch, n)
    a28 = [x for x in new["problems"] if x.startswith("A28:")]
    assert [x for x in new["problems"] if not x.startswith("A28:")] == old["problems"]
    po, pn = old.get("projection_usd"), new.get("projection_usd")
    assert (po is None) == (pn is None)
    if po:
        assert {k: pn[k] for k in po} == po
        assert len(a28) == sum(pn[f"a28_at_{s}"] > 35 for s in (4.63, 4.9))
    assert set(new) - set(old) == set() and set(old) - set(new) == set()
    if n == 9416:   # the old edge: $35 holds at the 2.754 x 1.12 rate (A28 adds the measured-rate refusal)
        assert not any("+12%" in x for x in old["problems"]) and a28


PROJ_GRID = [(sps, n, spent) for sps in (2.5, 2.754, 2.9, 3.1, 3.3, 4.63) for n in (8880, 9270, 9375)
             for spent in (1.0, 1.9, 3.0)]


def proj_out(mod, tmp, monkeypatch, sps, n, spent):
    lean, here = sandbox(tmp, mod, monkeypatch, spent=spent)
    write_stop(lean, 300, n, sps)
    code = run(mod.proj)
    rec = json.loads((here / "logs/r1_check_proj.json").read_text())
    f = here / "logs/r1_stop_after_min.txt"
    return code, rec, (f.read_text() if f.exists() else None)


@pytest.mark.parametrize("sps,n,spent", PROJ_GRID)
def test_proj_old_vs_new_on_35_inputs(tmp_path, monkeypatch, sps, n, spent):
    oc, orec, of = proj_out(OLD, tmp_path / "old", monkeypatch, sps, n, spent)
    monkeypatch.setattr(rc, "HARD_STOP", 35.0)
    nc, nrec, nf = proj_out(rc, tmp_path / "new", monkeypatch, sps, n, spent)
    assert (oc, of) == (nc, nf)
    assert {k: nrec[k] for k in orec if k != "decision"} == {k: v for k, v in orec.items() if k != "decision"}
    od, nd = orec["decision"], nrec["decision"]
    if nrec["a28"]["segments_left"] == 1:      # k = 1: the old one-segment rule, word for word
        assert nd.replace("(incl. 1 load/save)", "(incl. load/save)") == od
    else:                                      # k = 2 only when the rest exceeds 532 min: > the $35 budget anyway
        assert od.startswith("STOP") and nd.startswith("STOP")


@pytest.mark.parametrize("sps,n,spent", PROJ_GRID + [(4.9, 9270, 2.22), (4.0, 9270, 2.0)])
def test_proj_new_equals_old_formula_with_cap_55(tmp_path, monkeypatch, sps, n, spent):
    """Only the cap value differs: the $35 code with its cap set to 55 gives the same verdict whenever the rest fits
    one segment; the new file is the old one clamped at 540 (A28 segment cap)."""
    monkeypatch.setattr(OLD, "HARD_STOP", 55.0)
    oc, orec, of = proj_out(OLD, tmp_path / "old", monkeypatch, sps, n, spent)
    nc, nrec, nf = proj_out(rc, tmp_path / "new", monkeypatch, sps, n, spent)
    if nrec["a28"]["segments_left"] == 1:
        assert oc == nc and (of is None) == (nf is None)
        if of:
            assert int(nf) == min(int(of), 540)
    else:                                      # k = 2: stricter by one load/save, never looser
        assert nc >= oc and (nc == 0) <= (oc == 0)
        if nc == 0:
            assert int(nf) == 540 and int(of) == int(nrec["stop_after_min"])


def test_proj_a28_numbers(tmp_path, monkeypatch):
    c, rec, f = proj_out(rc, tmp_path / "a", monkeypatch, 4.63, 9270, 2.12)
    assert c == 0 and f == "540\n" and rec["projected_usd"] == 51.3 and rec["stop_after_min"] == 746
    assert rec["a28"]["segments_left"] == 2 and rec["need_min_for_rest"] == pytest.approx(692.2, abs=0.5)   # log "min" is rounded to 0.01
    c, rec, f = proj_out(rc, tmp_path / "b", monkeypatch, 4.9, 9270, 2.22)
    assert c == 1 and f is None and "incl. 2 load/save" in rec["decision"]       # 733 + 16 > 745
    c, rec, f = proj_out(rc, tmp_path / "c", monkeypatch, 4.9, 9375, 2.22)
    assert c == 1 and f is None
    c, rec, f = proj_out(rc, tmp_path / "d", monkeypatch, 5.3, 9270, 2.3)
    assert c == 1 and "projection above" in rec["decision"]                     # > $55


# ---------------------------------------------------------------- seg and cap
def seg_out(tmp, monkeypatch, at, n, sps_post, spent, proj_sps=4.63, prev=None, final=False, proj_go=True):
    lean, here = sandbox(tmp, rc, monkeypatch, spent=spent)
    (here / "logs/r1_check_proj.json").write_text(json.dumps({"s_per_step_100_300": proj_sps,
                                                              "decision": "GO" if proj_go else "STOP: x"}))
    if prev is not None:
        (here / "logs/r1_check_seg.json").write_text(json.dumps({"from_step": prev, "decision": "GO"}))
    write_stop(lean, 300, n, proj_sps)
    if at:
        write_stop(lean, at, n, sps_post, start=300, min0=30.0)
    if final:
        (lean / "logs/relay_q35_4b_c_r1_final.json").write_text("{}")
    code = run(rc.seg)
    rec = json.loads((here / "logs/r1_check_seg.json").read_text())
    f = here / "logs/r1_stop_after_min.txt"
    return code, rec, (f.read_text() if f.exists() else None)


def test_seg_next_cap_from_budget_left(tmp_path, monkeypatch):
    c, rec, f = seg_out(tmp_path / "a", monkeypatch, 7246, 9270, 4.63, 38.93)
    assert c == 0 and f == "206\n" and rec["a28"]["segments_left"] == 1 and rec["from_step"] == 7246
    assert rec["s_per_step_used"] == pytest.approx(4.63, abs=0.01)


def test_seg_uses_the_slower_rate_and_stops_when_rest_does_not_fit(tmp_path, monkeypatch):
    c, rec, f = seg_out(tmp_path / "a", monkeypatch, 7246, 9270, 5.6, 38.93)
    assert rec["s_per_step_used"] == pytest.approx(5.6, abs=0.02)
    # the rest (2,024 x 5.6 s = 189 + 8 min) fits the 206 min left, but the whole-run term of D4's max(),
    # 9,270 x 5.6 s = $61.0, is above $55
    assert c == 1 and f is None and "projection above" in rec["decision"]


def test_seg_cap_check_and_guards(tmp_path, monkeypatch):
    c, rec, f = seg_out(tmp_path / "a", monkeypatch, 6652, 9270, 4.63, 38.93)  # $54.7 fits, but 202 + 8 > 206 min
    assert c == 1 and f is None and "incl. 1 load/save" in rec["decision"] and rec["projected_usd"] <= 55
    c, rec, f = seg_out(tmp_path / "b", monkeypatch, 0, 9270, 4.63, 20.0)     # only stopped_at_300: no progress
    assert c == 1 and "no progress" in rec["problems"][0]
    c, rec, f = seg_out(tmp_path / "c", monkeypatch, 7246, 9270, 4.63, 38.0, prev=7246)
    assert c == 1 and "no progress" in rec["problems"][0]
    c, rec, f = seg_out(tmp_path / "d", monkeypatch, 7246, 9270, 4.63, 38.0, final=True)
    assert c == 1 and f is None
    c, rec, f = seg_out(tmp_path / "e", monkeypatch, 7246, 9270, 4.63, 38.0, proj_go=False)
    assert c == 1 and "proj" in rec["problems"][0]
    c, rec, f = seg_out(tmp_path / "f", monkeypatch, 3000, 9270, 4.63, 12.0)   # big budget: clamped at 540
    assert c == 0 and f == "540\n" and rec["a28"]["segments_left"] == 1
    # a stopped_at file older than the last segment's start (an earlier attempt) is not this segment's stop
    lean, here = sandbox(tmp_path / "g", rc, monkeypatch, spent=38.0)
    (here / "logs/r1_check_proj.json").write_text(json.dumps({"s_per_step_100_300": 4.63, "decision": "GO"}))
    write_stop(lean, 7246, 9270, 4.63, start=300)
    os.utime(lean / "logs/relay_q35_4b_c_r1_stopped_at_7246.json", (1e9, 1e9))
    (here / "logs/r1_segments.jsonl").write_text(json.dumps({"seg": "seg3", "start": 2e9, "end": 2e9, "rc": 0}) + "\n")
    monkeypatch.setattr(rc, "spent_so_far", lambda: (38.0, "test"))
    assert run(rc.seg) == 1 and "no progress" in json.loads((here / "logs/r1_check_seg.json").read_text())["problems"][0]


@pytest.mark.parametrize("spent,want_code,want", [(2.0, 0, "540\n"), (20.0, 0, "484\n"), (52.0, 0, "14\n"),
                                                  (52.4, 1, None)])
def test_cap_clamped_to_one_segment(tmp_path, monkeypatch, spent, want_code, want):
    lean, here = sandbox(tmp_path, rc, monkeypatch, spent=spent)
    assert run(rc.cap) == want_code
    f = here / "logs/r1_stop_after_min.txt"
    assert (f.read_text() if f.exists() else None) == want


@pytest.mark.parametrize("spent", [1.0, 5.0, 20.0, 32.5, 32.9])
def test_cap_old_vs_new_on_35_inputs(tmp_path, monkeypatch, spent):
    lo, ho = sandbox(tmp_path / "old", OLD, monkeypatch, spent=spent)
    oc = run(OLD.cap)
    monkeypatch.setattr(rc, "HARD_STOP", 35.0)
    ln, hn = sandbox(tmp_path / "new", rc, monkeypatch, spent=spent)
    nc = run(rc.cap)
    fo, fn = ho / "logs/r1_stop_after_min.txt", hn / "logs/r1_stop_after_min.txt"
    assert oc == nc and (fo.read_text() if fo.exists() else None) == (fn.read_text() if fn.exists() else None)


# ---------------------------------------------------------------- r1_chain.sh with a fake modal (relay simulator)
FAKE_PY = r"""#!/bin/bash
case "$1" in
  */r1_check.py)
    case "$2" in
      preflight) echo '{"baseline_metered_usd": 100.0, "decision": "GO"}' > c_build/endgame/logs/r1_check_preflight.json
                 echo GO; exit 0;;
      first100) echo GO; exit 0;;
      *) exec "$REAL_PY" "$@";;
    esac;;
  */spend_guard.py) shift; echo "$*" >> c_build/endgame/logs/ledger.txt; exit 0;;
  */snap_monitor.py) echo '{"ev": "start"}'; sleep 2; exit 0;;
esac
exit 0
"""

FAKE_MODAL = r'''
import json, math, os, sys
from pathlib import Path
st_dir = Path(os.environ["FAKE_STATE"]); st_dir.mkdir(exist_ok=True)
sf = st_dir / "state.json"
st = json.loads(sf.read_text()) if sf.exists() else {"next": 0, "min": 0.0, "billed": 0.0, "log": [], "runs": []}
a = sys.argv[1:]
LOAD, USD_H, TIMEOUT = 4.0, 4.09, 600.0
N, SPS = int(os.environ["FAKE_N"]), float(os.environ["FAKE_SPS"])
SPS_POST = float(os.environ.get("FAKE_SPS_POST") or SPS)
LAG_RUNS = int(os.environ.get("FAKE_BILL_LAG_RUNS") or 0)        # A28 R2: billing misses the last k runs
if a[:2] == ["billing", "summary"]:
    m = 100.0 + st["billed"] - sum(r.get("usd", 0.0) for r in (st["runs"][-LAG_RUNS:] if LAG_RUNS else []))
    print(json.dumps({"metered_cost": f"{m:.4f}", "billed_cost": f"{m:.4f}"})); sys.exit(0)
if a[:2] == ["app", "list"]:                  # A28 R3: the real CLI prints [] when nothing runs
    if int(os.environ.get("FAKE_APPLIST_RC") or 0):
        print("Token missing / network error", file=sys.stderr); sys.exit(int(os.environ["FAKE_APPLIST_RC"]))
    print(os.environ.get("FAKE_APPS", "[]")); sys.exit(0)
if not a or a[0] != "run":
    sys.exit(0)
def opt(k, d=0.0):
    return float(a[a.index(k) + 1]) if k in a else d
cap, at_step, le = opt("--stop-after-min"), int(opt("--stop-at-step")), int(opt("--log-every", 50))
resume = "--expect-resume" in a
run = {"cap": cap, "stop_at_step": at_step, "expect_resume": resume, "from": st["next"]}
st["runs"].append(run)
def save(): sf.write_text(json.dumps(st))
if resume and st["next"] == 0:
    run["error"] = "expect_resume: no checkpoint"; save(); print(run["error"]); sys.exit(1)
CRASH = os.environ.get("FAKE_CRASH")                            # "<run index>:<container min>": app crashes
crash_min = float(CRASH.split(":")[1]) if CRASH and int(CRASH.split(":")[0]) == len(st["runs"]) - 1 else None
start, t, s = st["next"], LOAD, st["next"]
if os.environ.get("FAKE_RUN_SLEEP"):        # A28 R3: a segment that takes real seconds (monitor polls during it)
    import time; time.sleep(float(os.environ["FAKE_RUN_SLEEP"]))
while s < N:                                  # the trainer: one step, then the stop checks (as train_decoder)
    sps = SPS if s < 300 else SPS_POST
    t += sps / 60; st["min"] += sps / 60
    if s % le == 0:
        st["log"].append({"step": s, "loss": 0.5, "min": round(st["min"], 2), "of": N})
    s += 1
    if s < N and ((at_step and s >= at_step) or (cap and t >= cap)):
        break
    if crash_min is not None and t >= crash_min:
        break
if crash_min is not None and s < N:           # crash (checkpoint at the crash step assumed; real: <= 10 min lost)
    usd = t / 60 * USD_H
    run.update({"to": s, "container_min": round(t, 2), "error": "crash", "usd": usd})
    st["billed"] += usd; st["next"] = s; st["clock"] = st.get("clock", float(os.environ.get("FAKE_CLOCK0") or 0)) + t * 60
    save(); print("crash"); sys.exit(1)
t += 0.1                                      # checkpoint / final save
run.update({"to": s, "container_min": round(t, 2)})
if os.environ.get("FAKE_CLOCK0"):             # fake wall clock (the fake `date +%s` reads it)
    st["clock"] = st.get("clock", float(os.environ["FAKE_CLOCK0"])) + t * 60
    run["usd"] = t / 60 * USD_H
if t > TIMEOUT:
    run["error"] = "FunctionTimeoutError"; st["billed"] += TIMEOUT / 60 * USD_H; save()
    print("FunctionTimeoutError"); sys.exit(1)
st["billed"] += t / 60 * USD_H; st["next"] = s
logs = Path("logs")
if s >= N:
    (logs / "relay_q35_4b_c_r1_final.json").write_text(json.dumps({"steps": N, "log": st["log"]}))
else:
    (logs / f"relay_q35_4b_c_r1_stopped_at_{s}.json").write_text(
        json.dumps({"cfg": {}, "steps": N, "stopped_at_step": s, "log": st["log"]}))
save(); print("ap-FAKE" + str(len(st["runs"]))); print(json.dumps({"stopped": s < N, "next_step": s, "of": N}))
'''


FAKE_DATE = r"""#!/bin/bash
if [ "${1:-}" = "+%s" ] && [ -n "${FAKE_CLOCK0:-}" ]; then
  exec "$REAL_PY" -c 'import json, os, pathlib
f = pathlib.Path(os.environ["FAKE_STATE"]) / "state.json"
st = json.loads(f.read_text()) if f.exists() else {}
print(int(st.get("clock", float(os.environ["FAKE_CLOCK0"]))))'
fi
exec /bin/date "$@"
"""


def chain_sim(tmp: Path, n: int, sps: float, sps_post=None, chain_src=None, check_src=None, cap35=False):
    lean, e, env = sim_setup(tmp, n, sps, sps_post, chain_src, check_src, cap35)
    r = subprocess.run(["bash", str(e / "r1_chain.sh")], cwd=str(lean), capture_output=True, text=True, timeout=120,
                       env=env)
    sf = tmp / "state/state.json"
    st = json.loads(sf.read_text()) if sf.exists() else {"runs": [], "billed": 0.0}
    return r, st, e


def sim_setup(tmp: Path, n: int, sps: float, sps_post=None, chain_src=None, check_src=None, cap35=False, extra=None):
    lean = tmp / "lean"
    e = lean / "c_build/endgame"
    (e / "logs").mkdir(parents=True)
    (lean / "logs").mkdir()
    shutil.copy(chain_src or E / "r1_chain.sh", e / "r1_chain.sh")
    src = (check_src or E / "r1_check.py").read_text()
    if cap35:      # the test's own copy only: the new code with the old $35 cap
        src, k = re.subn(r"^ALLOW, HARD_STOP, SENS = 2\.0, 55\.0, 1\.12", "ALLOW, HARD_STOP, SENS = 2.0, 35.0, 1.12", src,
                         flags=re.M)
        assert k == 1
    (e / "r1_check.py").write_text(src)
    (e / "snap_monitor.py").write_text("# fake\n")
    shutil.copy(E / "spend_guard.py", e / "spend_guard.py")      # r1_check.py relaunch: running_apps (fake app list)
    (lean / "PREREG_FINAL.md").write_text("")
    vb = tmp / ".venv/bin"
    vb.mkdir(parents=True)
    for name, body in (("python", FAKE_PY), ("modal", f"#!{sys.executable}\n" + FAKE_MODAL)):
        (vb / name).write_text(body)
        (vb / name).chmod((vb / name).stat().st_mode | stat.S_IEXEC)
    env = {**os.environ, "REAL_PY": sys.executable, "FAKE_STATE": str(tmp / "state"), "FAKE_N": str(n),
           "FAKE_SPS": str(sps), "FAKE_SPS_POST": str(sps_post or ""), "R1_MON_START_S": "1", "R1_MON_POLL_S": "0.2",
           **(extra or {})}
    if env.get("FAKE_CLOCK0"):
        fb = tmp / "fakebin"
        fb.mkdir()
        (fb / "date").write_text(FAKE_DATE)
        (fb / "date").chmod(0o755)
        env["PATH"] = f"{fb}:{env['PATH']}"
    return lean, e, env


needs_bash = pytest.mark.skipif(shutil.which("bash") is None, reason="needs bash")


@needs_bash
def test_chain_a28_central_two_relay_segments_to_final(tmp_path):
    r, st, e = chain_sim(tmp_path, 9270, 4.63)
    assert r.returncode == 0 and "ROUND 1 FINAL" in r.stdout, r.stdout[-600:]
    runs = st["runs"]
    assert [x["cap"] for x in runs[:3]] == [30, 35, 540] and len(runs) == 4
    assert [x["stop_at_step"] for x in runs] == [100, 300, 0, 0]
    assert [x["expect_resume"] for x in runs] == [False, True, True, True]
    assert all(x["from"] == y["to"] for x, y in zip(runs[1:], runs[:-1]))       # each resumes where the last stopped
    assert all("error" not in x and x["container_min"] < 600 for x in runs)
    assert all(x["cap"] <= 540 for x in runs) and runs[-1]["to"] == 9270
    seg_rec = json.loads((e / "logs/r1_check_seg.json").read_text())
    assert seg_rec["decision"] == "GO" and runs[3]["cap"] == seg_rec["a28"]["seg_cap_min"]
    assert 150 < runs[3]["cap"] < 540 and st["billed"] + 2.0 <= 55.0
    lines = [json.loads(x) for x in (e / "logs/r1_segments.jsonl").read_text().splitlines()]
    closed, opened = [x for x in lines if "end" in x], [x for x in lines if x.get("open") is True]
    assert [x["seg"] for x in closed] == ["seg1", "seg2", "seg3", "seg4"]          # A28 R2: + one open line each
    assert [(x["seg"], x["start"], x["args"]) for x in opened] == [(x["seg"], x["start"], x["args"]) for x in closed]
    assert len(lines) == 8 and all(x["rc"] == 0 for x in closed)
    print(json.dumps({"caps": [x["cap"] for x in runs], "to": [x["to"] for x in runs], "usd": round(st["billed"], 2)}))


@needs_bash
def test_chain_a28_high_stops_at_proj(tmp_path):
    r, st, e = chain_sim(tmp_path, 9375, 4.9)
    assert r.returncode == 1 and "proj STOP" in r.stdout and len(st["runs"]) == 2


@needs_bash
def test_chain_seg_stop_when_slower_after_300(tmp_path):
    r, st, e = chain_sim(tmp_path, 9270, 4.63, sps_post=5.6)
    assert r.returncode == 1 and "seg STOP after seg3" in r.stdout and len(st["runs"]) == 3
    assert "ROUND 1 FINAL" not in r.stdout and not (e / "logs/r1_stop_after_min.txt").exists()


@needs_bash
@pytest.mark.parametrize("sps,n", [(2.9, 8880), (2.754, 9270), (3.3, 9270)])
def test_chain_old_vs_new_on_35_inputs(tmp_path, sps, n):
    """$35-era inputs: the $35 chain + checker and the new ones (cap set back to 35 in the copy) launch the same
    segments with the same flags and caps and end the same way."""
    ro, so, _ = chain_sim(tmp_path / "old", n, sps, chain_src=E / "r1_chain.sh.pre_a28",
                          check_src=E / "r1_check.py.pre_a28")
    rn, sn, _ = chain_sim(tmp_path / "new", n, sps, cap35=True)
    assert ro.returncode == rn.returncode
    assert so["runs"] == sn["runs"] and math.isclose(so["billed"], sn["billed"])
    assert ("ROUND 1 FINAL" in ro.stdout) == ("ROUND 1 FINAL" in rn.stdout)


# ---------------------------------------------------------------- A28 R2: crash relaunches are logged and counted
# Reviewer defect (round 2): the D5 manual relaunch (`modal run` by hand) never reached logs/r1_segments.jsonl, so the
# next `cap` saw max(wall without it, lagging billing) and could hand out ~60-75 min too much. Fix: `r1_chain.sh
# relaunch` launches through the chain's seg() (open line + closed line), and spent_so_far counts a launch that was
# not closed with rc 0 to its capped window (bounded by billing + the last 75 min of every logged window).
MIN_S = 60.0


def bill_modal(tmp: Path, mod, monkeypatch, metered: float | None):
    f = tmp / "fake_modal_bill"
    f.write_text("#!/bin/bash\n" + (f"echo '{{\"metered_cost\": \"{metered}\", \"billed_cost\": \"0\"}}'\n"
                                     if metered is not None else "exit 1\n"))
    f.chmod(0o755)
    monkeypatch.setattr(mod, "MODAL", str(f))


def write_segs(here: Path, segs, base=100.0):
    """segs: (name, start_s, end_s | None, rc, cap_min). Writes the lines exactly as r1_chain.sh seg() does."""
    lines = []
    for name, s, e, rc_, capm in segs:
        args = f"--expect-resume --stop-after-min {capm}" if capm is not None else "--expect-resume"
        lines.append('{"seg":"%s","start":%d,"open":true,"args":"%s"}' % (name, s, args))
        if e is not None:
            lines.append('{"seg":"%s","start":%d,"end":%d,"rc":%d,"args":"%s"}' % (name, s, e, rc_, args))
    (here / "logs/r1_segments.jsonl").write_text("\n".join(lines) + "\n")
    if base is not None:
        (here / "logs/r1_check_preflight.json").write_text(json.dumps({"baseline_metered_usd": base}))


def usd(minutes: float) -> float:
    return minutes / 60 * rc.USD_H


def test_bill_lag_is_spend_guards():
    import spend_guard
    assert rc.BILL_LAG_S == spend_guard.LAG_S == 75 * 60


@pytest.mark.parametrize("metered_extra_min", [0.0, 25.0, 31.3, 80.0])
def test_spend_all_closed_rc0_unchanged_vs_old(tmp_path, monkeypatch, metered_extra_min):
    """The chain's normal path (every launch closed with rc 0, open lines present): same spend and text as the
    $35-era spent_so_far (which skips the open lines: no `end`)."""
    t0 = 1_000_000
    segs = [("seg1", t0, t0 + 11.8 * MIN_S, 0, 30), ("seg2", t0 + 900, t0 + 900 + 19.5 * MIN_S, 0, 35),
            ("seg3", t0 + 3000, t0 + 3000 + 540.1 * MIN_S, 0, 540)]
    got = []
    for mod, sub in ((OLD, "old"), (rc, "new")):
        lean, here = sandbox(tmp_path / sub, mod, monkeypatch)
        write_segs(here, segs)
        bill_modal(tmp_path / sub, mod, monkeypatch, round(100 + usd(metered_extra_min), 4))
        got.append(mod.spent_so_far())
    assert got[0] == got[1]


def defect_case(tmp, monkeypatch, logged: bool):
    """seg3 crashed at 520 min (closed rc 1); relaunch1 (cap 100) stopped at its cap; now = 5 min later; billing has
    everything up to now - 60 min. True spend 652 min = $44.44 -> true budget left 125 min under $55."""
    t3 = 2_000_000
    r = t3 + 530 * MIN_S
    segs = [("seg1", t3 - 300 * MIN_S, t3 - 288.2 * MIN_S, 0, 30), ("seg2", t3 - 280 * MIN_S, t3 - 260.5 * MIN_S, 0, 35),
            ("seg3", t3, t3 + 520 * MIN_S, 1, 540)]
    if logged:
        segs.append(("relaunch1", r, r + 100 * MIN_S, 0, 100))
    lean, here = sandbox(tmp, rc, monkeypatch)
    write_segs(here, segs)
    now = r + 105 * MIN_S
    billed_min = 11.8 + 19.5 + 520 + 45                     # relaunch1's last 55 min not billed yet
    bill_modal(tmp, rc, monkeypatch, round(100 + usd(billed_min), 4))
    monkeypatch.setattr(rc.time, "time", lambda: now)
    return here


def test_defect_unlogged_relaunch_overruns_logged_one_does_not(tmp_path, monkeypatch):
    true_spent = usd(11.8 + 19.5 + 520 + 100)
    true_left = (rc.HARD_STOP - rc.ALLOW - true_spent) / rc.USD_H * 60          # 125.5 min
    caps = {}
    for logged in (False, True):
        here = defect_case(tmp_path / str(logged), monkeypatch, logged)
        assert run(rc.cap) == 0
        caps[logged] = int((here / "logs/r1_stop_after_min.txt").read_text())
    assert caps[False] > true_left + 50          # by hand: 180 min -> ~$56.7 + $2 in all, over the hard stop
    assert caps[True] <= true_left               # through r1_chain.sh relaunch: 110 min (75 min lag bound)
    assert usd(11.8 + 19.5 + 520 + 100 + caps[True]) + rc.ALLOW <= rc.HARD_STOP
    assert usd(11.8 + 19.5 + 520 + 100 + caps[False]) + rc.ALLOW > rc.HARD_STOP
    print(json.dumps({"cap_by_hand": caps[False], "cap_logged": caps[True], "true_left": round(true_left, 1)}))


def test_open_line_without_close_counted_to_now(tmp_path, monkeypatch):
    """The chain / relaunch died mid-segment (no closed line): the launch counts up to now (relaunch refuses while
    an app runs, so it has ended), bounded by billing + its last 75 min."""
    lean, here = sandbox(tmp_path, rc, monkeypatch)
    t3 = 3_000_000
    write_segs(here, [("seg1", t3 - 400 * MIN_S, t3 - 388 * MIN_S, 0, 30), ("seg3", t3, None, None, 540)])
    monkeypatch.setattr(rc.time, "time", lambda: t3 + 100 * MIN_S)
    bill_modal(tmp_path, rc, monkeypatch, round(100 + usd(12 + 40), 4))       # billing lags 60 min
    spent, how = rc.spent_so_far()
    assert spent == pytest.approx(usd(12 + 100)) and "not closed with rc 0" in how      # wall bound 112 < 52 + 75
    bill_modal(tmp_path, rc, monkeypatch, round(100 + usd(12 + 25), 4))        # billing lags the full 75 min
    assert rc.spent_so_far()[0] == pytest.approx(usd(12 + 100), abs=1e-3)      # both bounds 112 min
    bill_modal(tmp_path, rc, monkeypatch, None)                                # billing call fails: wall bound
    assert rc.spent_so_far()[0] == pytest.approx(usd(12 + 100))


def test_crashed_close_bounded_by_billing(tmp_path, monkeypatch):
    """rc != 0 long ago (billing caught up): the billing delta bounds the capped window (no over-count)."""
    lean, here = sandbox(tmp_path, rc, monkeypatch)
    t3 = 3_000_000
    write_segs(here, [("seg3", t3, t3 + 30 * MIN_S, 1, 540)])
    monkeypatch.setattr(rc.time, "time", lambda: t3 + 2000 * MIN_S)
    bill_modal(tmp_path, rc, monkeypatch, round(100 + usd(31), 4))
    assert rc.spent_so_far()[0] == pytest.approx(usd(31), abs=1e-3)
    bill_modal(tmp_path, rc, monkeypatch, None)                                # unknown billing: the whole cap
    assert rc.spent_so_far()[0] == pytest.approx(usd(540))


APPLIST = {   # A28 R3: (exit code, stdout, stderr) of a fake `modal app list --json`
    "ok": (0, "[]\n", ""), "final": (0, "[]\n", ""),
    "running": (0, json.dumps([{"App ID": "ap-1", "State": "detached", "Tasks": 1}]), ""),
    "stopped_app": (0, json.dumps([{"App ID": "ap-0", "State": "stopped", "Tasks": 0}]), ""),
    "rc1_stderr": (1, "", "Token missing. Could not authenticate client."),     # the usual failure
    "rc0_empty": (0, "", ""), "not_json": (0, "Error: something\n", ""), "not_list": (0, '{"apps": []}', ""),
    "no_binary": None,
}


def fake_applist(tmp: Path, case: str) -> str:
    if APPLIST[case] is None:
        return str(tmp / "no_modal_here")
    code, so, se = APPLIST[case]
    f = tmp / f"modal_{case}"
    f.write_text(f"#!{sys.executable}\nimport sys\nassert sys.argv[1:] == ['app', 'list', '--json']\n"
                 f"sys.stdout.write({so!r}); sys.stderr.write({se!r}); sys.exit({code})\n")
    f.chmod(0o755)
    return str(f)


def mon_done(here: Path, name="q35_4b_c_r1", **kw):
    """The snap monitor's state after it read 25/50/75% and the rule did not fire (it has exited: no pid file)."""
    (here / "logs/snap_monitor_state.json").write_text(json.dumps(
        {"name": name, "reads": {f: {} for f in ("0.25", "0.5", "0.75")}, **kw}))


@pytest.mark.parametrize("case", list(APPLIST))
def test_relaunch_check(tmp_path, monkeypatch, case):
    """A28 R3: relaunch STOPs unless `modal app list --json` exits 0 with a JSON list and nothing runs."""
    lean, here = sandbox(tmp_path / "r", rc, monkeypatch, spent=20.0)
    (here / "snap_monitor.py").write_text("# fake\n")
    mon_done(here)
    monkeypatch.setattr(rc, "MODAL", fake_applist(tmp_path, case))
    if case == "final":
        (lean / "logs/relay_q35_4b_c_r1_final.json").write_text("{}")
    code = run(rc.relaunch)
    f = here / "logs/r1_stop_after_min.txt"
    if case in ("ok", "stopped_app"):                  # exactly `cap`
        assert code == 0 and f.read_text() == "484\n"
        assert json.loads((here / "logs/r1_check_cap.json").read_text())["decision"] == "GO"
    else:
        assert code == 1 and not f.exists()
        rec = json.loads((here / "logs/r1_check_relaunch.json").read_text())
        assert rec["decision"] == "STOP"
        if case not in ("final", "running"):
            assert any("app list failed" in x for x in rec["problems"]), rec


def test_spend_guard_reads_a_failed_app_list_as_no_apps(tmp_path, monkeypatch):
    """The defect A28 R3 fixes (spend_guard.py itself is unchanged): exit 1 + stderr only -> [] there, STOP here."""
    import spend_guard as sg
    monkeypatch.setattr(sg, "MODAL", fake_applist(tmp_path, "rc1_stderr"))
    assert sg.running_apps("aryamhd") == []
    monkeypatch.setattr(rc, "MODAL", sg.MODAL)
    with pytest.raises(RuntimeError, match="exit 1"):
        rc.running_apps_strict("aryamhd")
    assert "app list failed" in rc.app_list_problem("x")


@pytest.mark.parametrize("case", ["ok", "rc1_stderr", "rc0_empty", "running"])
def test_preflight_app_list_is_strict_too(tmp_path, monkeypatch, case):
    """extra_checks (preflight) uses the same strict list (before A28 R3: spend_guard.running_apps, same gap)."""
    monkeypatch.setattr(rc, "MODAL", fake_applist(tmp_path, case))
    src = (E / "r1_check.py").read_text()
    body = src[src.index("def extra_checks("):src.index("def preflight(")]
    assert 'app_list_problem("already running on aryamhd' in body and "spend_guard" not in body
    e = rc.app_list_problem("already running on aryamhd (two writers / unknown spend)")
    assert (e is None) == (case == "ok")


def test_mon_status_codes(tmp_path, monkeypatch):
    lean, here = sandbox(tmp_path / "m", rc, monkeypatch)
    L = here / "logs"
    assert rc.mon_status()[0] == 1                                     # no snap_monitor.py, no waiver
    (lean / "PREREG_FINAL.md").write_text("> OWNER-WAIVER r1-preflight snapmon: test\n")
    assert rc.mon_status()[0] == 0                                     # the chain's waiver path
    (here / "snap_monitor.py").write_text("# fake\n")
    assert rc.mon_status()[0] == 1                                     # a driver exists: it must run or be done
    (L / "snap_monitor_state.json").write_text(json.dumps({"name": "q35_4b_c_r1", "reads": {"0.25": {}}}))
    assert rc.mon_status()[0] == 1                                     # partial reads, not running
    sl = subprocess.Popen(["sleep", "30"])
    try:
        (L / "snap_monitor.pid").write_text(str(sl.pid))
        assert rc.mon_status()[0] == 2                                 # alive
    finally:
        sl.kill(); sl.wait()
    assert rc.mon_status()[0] == 1                                     # its pid is gone
    for bad in ("0", "1", "x", ""):
        (L / "snap_monitor.pid").write_text(bad)
        assert rc.mon_status()[0] == 1
    mon_done(here, name="other_run")
    assert rc.mon_status()[0] == 1
    mon_done(here)
    assert rc.mon_status()[0] == 0                                     # done, rule not fired
    mon_done(here, fired=True)
    assert rc.mon_status()[0] == 3
    mon_done(here, escalated=True)
    assert rc.mon_status()[0] == 4
    mon_done(here)
    for code, name in ((5, "r1_monitor_dead.json"), (4, "snap_monitor_escalation.json"),
                       (3, "snap_monitor_stop.json")):
        (L / name).write_text("{}")
        assert rc.mon_status()[0] == code
    assert rc.mon_status()[0] == 3                                     # stop record wins


@pytest.mark.parametrize("mon", ["stop", "esc", "dead", "not_running", "fired_state"])
def test_relaunch_check_refuses_on_monitor(tmp_path, monkeypatch, mon):
    lean, here = sandbox(tmp_path / "r", rc, monkeypatch, spent=20.0)
    (here / "snap_monitor.py").write_text("# fake\n")
    monkeypatch.setattr(rc, "MODAL", fake_applist(tmp_path, "ok"))
    if mon != "not_running":
        mon_done(here, fired=mon == "fired_state")
    f = {"stop": "snap_monitor_stop.json", "esc": "snap_monitor_escalation.json", "dead": "r1_monitor_dead.json"}
    if mon in f:
        (here / "logs" / f[mon]).write_text("{}")
    assert run(rc.relaunch) == 1 and not (here / "logs/r1_stop_after_min.txt").exists()
    rec = json.loads((here / "logs/r1_check_relaunch.json").read_text())
    assert rec["decision"] == "STOP" and any("stop rule driver" in x for x in rec["problems"])


def sim_run(cmd, lean, env, **extra):
    return subprocess.run(cmd, cwd=str(lean), capture_output=True, text=True, timeout=120, env={**env, **extra})


def state(tmp: Path) -> dict:
    return json.loads((tmp / "state/state.json").read_text())


@needs_bash
def test_chain_relaunch_logged_reaches_final(tmp_path):
    """seg3 crashes at 400 min; `r1_chain.sh relaunch` (billing lagging) resumes and reaches final."""
    import time as _t
    lean, e, env = sim_setup(tmp_path, 9270, 4.63, extra={"FAKE_CLOCK0": str(int(_t.time()) - 10 * 86400),
                                                           "FAKE_CRASH": "2:400"})
    r = sim_run(["bash", str(e / "r1_chain.sh")], lean, env)
    assert r.returncode == 1 and "seg3 client exit 1" in r.stdout, r.stdout[-400:]
    mon_done(e)                                   # A28 R3: the monitor read every snapshot (else REFUSED)
    r = sim_run(["bash", str(e / "r1_chain.sh"), "relaunch"], lean, env, FAKE_BILL_LAG_RUNS="1")
    assert r.returncode == 0 and "ROUND 1 FINAL after relaunch1" in r.stdout, r.stdout[-600:]
    st = state(tmp_path)
    runs = st["runs"]
    assert len(runs) == 4 and runs[2]["error"] == "crash" and runs[3]["expect_resume"] and runs[3]["from"] == runs[2]["to"]
    assert runs[3]["to"] == 9270 and runs[3]["cap"] <= 540 and st["billed"] + 2.0 <= 55.0
    lines = [json.loads(x) for x in (e / "logs/r1_segments.jsonl").read_text().splitlines()]
    assert [(x["seg"], "end" in x) for x in lines][-2:] == [("relaunch1", False), ("relaunch1", True)]
    assert lines[-1]["rc"] == 0 and f"--stop-after-min {int(runs[3]['cap'])}" in lines[-1]["args"]


@needs_bash
def test_chain_relaunch_logged_vs_by_hand_under_billing_lag(tmp_path):
    """seg3 crashes at 520 min (post-300 at 5.2 s/step); relaunch1 stops at its cap; billing misses the last run.
    Through `r1_chain.sh relaunch` the next cap counts relaunch1 and refuses (budget used up; total <= $55). By hand
    (the old D5 text: `cap && modal run`), the next cap misses relaunch1 and the run ends above $55."""
    import time as _t
    out = {}
    for mode in ("logged", "by_hand"):
        tmp = tmp_path / mode
        lean, e, env = sim_setup(tmp, 9270, 4.63, sps_post=5.2,
                                 extra={"FAKE_CLOCK0": str(int(_t.time()) - 10 * 86400), "FAKE_CRASH": "2:520"})
        r = sim_run(["bash", str(e / "r1_chain.sh")], lean, env)
        assert r.returncode == 1 and "seg3 client exit 1" in r.stdout, r.stdout[-400:]
        mon_done(e)                               # A28 R3: the monitor read every snapshot (else REFUSED)
        caps = []
        for _ in range(2):
            if mode == "logged":
                r = sim_run(["bash", str(e / "r1_chain.sh"), "relaunch"], lean, env, FAKE_BILL_LAG_RUNS="1")
                caps.append(state(tmp)["runs"][-1]["cap"] if "== D5 relaunch" in r.stdout else None)
                if "RELAUNCH REFUSED" in r.stdout:
                    break
            else:
                c = sim_run([sys.executable, str(e / "r1_check.py"), "cap"], lean, env, FAKE_BILL_LAG_RUNS="1")
                if c.returncode:
                    caps.append(None)
                    break
                m = int((e / "logs/r1_stop_after_min.txt").read_text())
                sim_run([str(tmp / ".venv/bin/modal"), "run", "--detach", "modal_od.py::relay", "--config",
                         "runs/q35_4b_c_r1.json", "--expect-resume", "--stop-after-min", str(m)], lean, env)
                caps.append(m)
        st = state(tmp)
        out[mode] = {"caps": caps, "usd": round(st["billed"], 2), "to": st["runs"][-1]["to"],
                     "final": (lean / "logs/relay_q35_4b_c_r1_final.json").exists()}
    assert out["logged"]["caps"][0] == out["by_hand"]["caps"][0] == 226        # the first relaunch is the same
    assert out["logged"]["caps"][1] is None and out["logged"]["usd"] + 2.0 <= 55.0 and not out["logged"]["final"]
    assert out["by_hand"]["caps"][1] == 226 and out["by_hand"]["usd"] + 2.0 > 55.0 and out["by_hand"]["final"]
    print(json.dumps(out))


# ---------------------------------------------------------------- A28 R3: relaunch vs the stop rule and the app list
def crashed_chain(tmp: Path, **extra):
    """seg3 crashes at 400 min (the D5 relaunch case); returns lean, e, env."""
    import time as _t
    lean, e, env = sim_setup(tmp, 9270, 4.63, extra={"FAKE_CLOCK0": str(int(_t.time()) - 10 * 86400),
                                                     "FAKE_CRASH": "2:400", **extra})
    r = sim_run(["bash", str(e / "r1_chain.sh")], lean, env)
    assert r.returncode == 1 and "seg3 client exit 1" in r.stdout, r.stdout[-400:]
    return lean, e, env


def relaunch_lines(e: Path) -> list:
    return [x for x in (e / "logs/r1_segments.jsonl").read_text().splitlines() if '"relaunch' in x]


@needs_bash
@pytest.mark.parametrize("why", ["stop", "esc", "dead", "not_running", "partial_reads", "applist_rc1",
                                 "applist_empty"])
def test_chain_relaunch_refused(tmp_path, why):
    """A28 R3: nothing is launched (no fake run, no open line, no cap) while a stop record exists, the monitor is
    neither running nor done, or the app list fails (exit 1 with stderr only / empty stdout)."""
    lean, e, env = crashed_chain(tmp_path)
    if why not in ("not_running", "partial_reads"):
        mon_done(e)
    if why == "partial_reads":
        (e / "logs/snap_monitor_state.json").write_text(json.dumps({"name": "q35_4b_c_r1", "reads": {"0.25": {}}}))
    f = {"stop": "snap_monitor_stop.json", "esc": "snap_monitor_escalation.json", "dead": "r1_monitor_dead.json"}
    if why in f:
        (e / "logs" / f[why]).write_text("{}")
    extra = {"applist_rc1": {"FAKE_APPLIST_RC": "1"}, "applist_empty": {"FAKE_APPS": ""}}.get(why, {})
    n0 = len(state(tmp_path)["runs"])
    r = sim_run(["bash", str(e / "r1_chain.sh"), "relaunch"], lean, env, **extra)
    assert r.returncode == 1 and "RELAUNCH REFUSED" in r.stdout and "== D5 relaunch" not in r.stdout, r.stdout[-500:]
    assert len(state(tmp_path)["runs"]) == n0 and relaunch_lines(e) == []
    assert not (e / "logs/r1_stop_after_min.txt").exists()
    mon_done(e)                                   # the same state with everything clear: GO (control)
    for k in f.values():
        (e / "logs" / k).unlink(missing_ok=True)
    r = sim_run(["bash", str(e / "r1_chain.sh"), "relaunch"], lean, env)
    assert r.returncode == 0 and "ROUND 1 FINAL after relaunch1" in r.stdout, r.stdout[-500:]


def fake_monitor(e: Path, after_s: float, then: str) -> int:
    """A live 'snap monitor' (its pid in logs/snap_monitor.pid) that after `after_s` s: dies without reading
    everything ('die'), fires the rule ('fire': stop record + state fired), or finishes its reads ('done')."""
    L = e / "logs"
    (L / "snap_monitor_state.json").write_text(json.dumps({"name": "q35_4b_c_r1", "reads": {"0.25": {}}}))
    code = (f"import json, pathlib, time\nL = pathlib.Path({str(L)!r})\ntime.sleep({after_s})\n"
            "st = {'name': 'q35_4b_c_r1', 'reads': {'0.25': {}}}\n")
    if then == "fire":
        code += "st['fired'] = True\n(L / 'snap_monitor_stop.json').write_text('{}')\n"
    if then == "done":
        code += "st['reads'] = {f: {} for f in ('0.25', '0.5', '0.75')}\n"
    code += "(L / 'snap_monitor_state.json').write_text(json.dumps(st))\n"
    # detached (as the chain's nohup monitor once the chain died): reaped by init, so its pid really goes away
    sh = subprocess.run(["sh", "-c", 'nohup "$0" -c "$1" >/dev/null 2>&1 & echo $!', sys.executable, code],
                        capture_output=True, text=True, timeout=30)
    pid = int(sh.stdout.strip())
    (L / "snap_monitor.pid").write_text(str(pid))
    return pid


def kill_quiet(pid: int) -> None:
    try:
        os.kill(pid, 9)
    except OSError:
        pass


@needs_bash
@pytest.mark.parametrize("then", ["die", "fire"])
def test_chain_relaunch_watches_the_monitor_during_the_segment(tmp_path, then):
    """A28 R3: the monitor is alive at launch and dies (or fires) while the relaunched segment trains: 'die' is
    recorded in r1_monitor_dead.json and the relaunch ends STOPPED with no candidate; the next relaunch is REFUSED."""
    lean, e, env = crashed_chain(tmp_path)
    pr = fake_monitor(e, 3.0, then)
    try:
        r = sim_run(["bash", str(e / "r1_chain.sh"), "relaunch"], lean, env, FAKE_RUN_SLEEP="6")
    finally:
        kill_quiet(pr)
    assert "== D5 relaunch1" in r.stdout and r.returncode == 1 and "RELAUNCH STOPPED" in r.stdout, r.stdout[-600:]
    dead = (e / "logs/r1_monitor_dead.json").exists()
    if then == "die":
        assert dead and "not running during relaunch1" in r.stdout
        assert json.loads((e / "logs/r1_monitor_dead.json").read_text())["during"] == "during relaunch1"
    else:
        assert not dead and "stop rule fired" in r.stdout
    r2 = sim_run(["bash", str(e / "r1_chain.sh"), "relaunch"], lean, env)
    assert r2.returncode == 1 and "RELAUNCH REFUSED" in r2.stdout and len(relaunch_lines(e)) == 2


@needs_bash
def test_chain_relaunch_waits_for_a_live_monitor_after_final(tmp_path):
    """A28 R3: the monitor runs at launch; the segment reaches final at once; the relaunch waits until the monitor
    has read every snapshot (rule not fired) before it reports FINAL (as the chain does)."""
    lean, e, env = crashed_chain(tmp_path)
    pr = fake_monitor(e, 2.5, "done")
    try:
        r = sim_run(["bash", str(e / "r1_chain.sh"), "relaunch"], lean, env)
    finally:
        kill_quiet(pr)
    assert r.returncode == 0 and "waiting for the snap monitor" in r.stdout, r.stdout[-600:]
    assert "ROUND 1 FINAL after relaunch1" in r.stdout and not (e / "logs/r1_monitor_dead.json").exists()

