"""auto_pipeline.py with a mocked status function, subprocess runner, spawner and pgrep (no Modal, no CPU job). CPU only.

Covers: crowd batching (one launch for every qualifying family), REFUSED -> NEEDS_ORCH + immediate exit, a deadline
stop relaunched once (MODELS env) then NEEDS_ORCH on the second stop, select right after a fetch, G13 gated on
A25_READY (and its end report), READY, NEEDS_ORCH exits the loop with 0, an exception exits 1, restart dedupe.
"""
import copy
import io
import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent / "endgame"))
import auto_pipeline as ap  # noqa: E402

QC_FAIL = {"ok": False, "status": "QC pass=False", "next": "lane: repair + QC"}
NO_SHARDS = {"ok": False, "status": ap.ST_NO_SHARDS, "next": "RUNBOOK A (crowd read)"}


def missing(models):
    return {"ok": False, "status": "crowd: crowd labels of x incomplete", "next": "RUNBOOK A3-A5 (crowd read / fetch)",
            "crowd_missing": list(models)}


def no_g13(sha="s1", sel_need=False):
    return {"ok": False, "status": ap.ST_NO_G13, "next": "RUNBOOK B (decontam_g13.py --fam, counts-only)",
            "cand_sha": sha, "sel_need": sel_need}


PASS = {"ok": True, "status": "QC, crowd, decontam, selection", "next": "ready for mixer --final", "cand_sha": "s1",
        "sel_need": False}


class World:
    """Mocked backends. `status` is what autopilot would say; runs are recorded; hooks change the world."""

    def __init__(self, tmp: Path):
        self.E, self.lean = tmp / "endgame", tmp / "lean"
        (self.E / "logs").mkdir(parents=True)
        (self.lean / "c_build/crowd_r1").mkdir(parents=True)
        (self.lean / "logs/decontam_counts").mkdir(parents=True)
        self.status = {f: dict(QC_FAIL) for f in ap.FAMS}
        self.calls, self.spawned = [], []
        self.crowd_running = self.g13_running = self.other_g13 = False
        self.launch_out = "CAP_MIN=17\nLAUNCHED crowd"
        self.launch_rc = 0
        self.after_fetch = {}                  # fam -> status after the labels are fetched
        self.select_pass = True

    def drv(self):
        self.out = io.StringIO()
        return ap.Driver(status_fn=lambda: copy.deepcopy(self.status), run_fn=self.run, spawn_fn=self.spawn,
                         pgrep_fn=self.pgrep, alive_fn=lambda pid: self.g13_running, e_dir=self.E, lean=self.lean,
                         out=self.out)

    def events(self):
        return [ln for ln in self.out.getvalue().splitlines() if ln.startswith("EVENT ")]

    def kinds(self, name):
        return [c for c in self.calls if name in " ".join(c[0])]

    def pgrep(self, pat):
        return self.crowd_running if pat == ap.CROWD_PAT else (self.other_g13 or self.g13_running)

    def run(self, cmd, env=None, log=None, timeout=None):
        self.calls.append((list(cmd), dict(env or {})))
        s = " ".join(cmd)
        if "crowd_launch.sh" in s:
            if self.launch_rc == 0 and "REFUSED" not in self.launch_out:
                self.crowd_running = True
            return self.launch_rc, self.launch_out
        if "volume get" in s:
            fam = cmd[-1].split("/")[-2]
            if fam in self.after_fetch:
                self.status[fam] = dict(self.after_fetch[fam])
            return 0, ""
        if "spend_guard.py" in s:
            return 0, "| crowd: AFTER |"
        if "crowd_select.py" in s:
            fam = cmd[-1]
            d = self.lean / "c_build/crowd_r1"
            (d / f"select_{fam}.json").write_text(json.dumps(
                {"report": {"pass": self.select_pass, "rows": 900, "target": 1000}, "candidates_sha256": "s1"}))
            (d / f"g5_reread_{fam}.json").write_text(json.dumps(
                {"n_low": 2, "low_ids": ["a", "b"], "sample_ids": ["b"] + [f"r{i}" for i in range(299)]}))
            self.status[fam]["sel_need"] = False
            return 0, f"select {fam}: 900 rows"
        raise AssertionError(f"unexpected command {s}")

    def spawn(self, cmd, log):
        self.spawned.append(list(cmd))
        self.g13_running = True
        return 4242


def test_crowd_batching_one_launch(tmp_path):
    w = World(tmp_path)
    w.status["F4"] = dict(NO_SHARDS)
    w.status["F7"] = dict(NO_SHARDS)
    w.status["F8"] = missing(["q35_4b_pxE"])
    d = w.drv()
    d.one_pass()
    launches = w.kinds("crowd_launch.sh")
    assert len(launches) == 1
    assert launches[0][0] == ["bash", "c_build/endgame/crowd_launch.sh", "atmosphor", "F4", "F7", "F8"]
    assert "MODELS" not in launches[0][1]                       # first launch: all 3 models
    assert d.state["crowd_pending"]["fams"] == ["F4", "F7", "F8"]
    assert any("INFO CROWD_LAUNCHED fams=F4,F7,F8" in e and "cap_min=17" in e for e in w.events())
    assert not d.orch
    # in flight: nothing new is launched, nothing fetched
    w.status["F9"] = dict(NO_SHARDS)
    d.one_pass()
    assert len(w.kinds("crowd_launch.sh")) == 1 and not w.kinds("volume get")


def test_refused_exits_at_once(tmp_path):
    w = World(tmp_path)
    w.status["F4"] = dict(NO_SHARDS)
    w.status["F5"] = no_g13()
    (w.E / "A25_READY").write_text("")
    w.launch_rc, w.launch_out = 1, "REFUSED: crowd F4 on atmosphor -> owner decides"
    d = w.drv()
    rc = ap.run_loop(d, sleep=lambda s: (_ for _ in ()).throw(AssertionError("slept")))
    assert rc == 0
    ev = w.events()
    assert len(ev) == 1 and ev[0].startswith("EVENT NEEDS_ORCH CROWD_REFUSED fams=F4")
    assert d.state["crowd_pending"] is None and not w.spawned     # exited before G13 started
    s = json.loads((w.E / "logs/auto_pipeline_state.json").read_text())
    assert s["crowd_pending"] is None and "F4" in s["crowd_hold"] and not s["fam_launches"].get("F4")
    # restarted driver: F4 is held (owner decides), so no REFUSED loop and G13 / selection keep moving
    w.launch_rc, w.launch_out = 0, "CAP_MIN=17\nLAUNCHED crowd"
    d = w.drv()
    assert ap.run_loop(d, once=True) == 0
    assert len(w.kinds("crowd_launch.sh")) == 1 and len(w.spawned) == 1 and not any("NEEDS_ORCH" in e for e in w.events())
    # --reset releases the hold: the next pass launches F4 (its first real launch)
    d = w.drv()
    d.reset(["F4"])
    d.one_pass()
    assert len(w.kinds("crowd_launch.sh")) == 2 and d.state["fam_launches"]["F4"] == 1


def test_incomplete_without_stop_is_held_not_relaunched(tmp_path):
    w = World(tmp_path)
    w.status["F4"] = dict(NO_SHARDS)
    w.after_fetch["F4"] = missing(["q35_4b_pxE"])
    d = w.drv()
    d.one_pass()
    for m in ap.MODELS:                                       # every app log ends normally: no deadline, no traceback
        (w.E / f"logs/crowd_F4_{m}.log").write_text('{"status": "done"}\n')
    w.crowd_running = False
    d.one_pass()
    assert len(w.kinds("crowd_launch.sh")) == 1 and d.orch
    assert any("NEEDS_ORCH CROWD_INCOMPLETE_NO_STOP tag=F4 fams=F4 models=q35_4b_pxE" in e for e in w.events())
    d2 = w.drv()
    d2.one_pass()
    assert len(w.kinds("crowd_launch.sh")) == 1 and not d2.orch


def test_refused_relaunch_leaves_exactly_one_more_launch(tmp_path):
    w = World(tmp_path)
    w.status["F4"] = dict(NO_SHARDS)
    w.after_fetch["F4"] = missing(["q35_4b_pxE"])
    d = w.drv()
    d.one_pass()                                              # launch 1 (all models)
    (w.E / "logs/crowd_F4_q35_4b_pxE.log").write_text('{"status": "deadline", "done": 3}\n')
    w.crowd_running = False
    w.launch_rc, w.launch_out = 1, "REFUSED: crowd F4 on atmosphor"
    assert ap.run_loop(d, once=True) == 0                     # the relaunch is REFUSED -> held, exit
    assert any("CROWD_REFUSED fams=F4" in e for e in w.events()) and d.state["fam_launches"]["F4"] == 1
    w.launch_rc, w.launch_out = 0, "CAP_MIN=17\nLAUNCHED crowd"
    d = w.drv()
    d.reset(["F4"])
    d.one_pass()                                              # its one relaunch: only the missing model
    rel = w.kinds("crowd_launch.sh")
    assert len(rel) == 3 and rel[2][1] == {"MODELS": "q35_4b_pxE"} and d.state["crowd_pending"]["attempt"] == 2
    w.crowd_running = False
    d.one_pass()                                              # stopped again -> held, never a 3rd real launch
    assert len(w.kinds("crowd_launch.sh")) == 3 and any("CROWD_STOPPED_TWICE tag=F4" in e for e in w.events())
    d = w.drv()
    d.reset(["F4"])                                           # even after --reset: launch count kept -> CROWD_LIMIT
    d.one_pass()
    assert len(w.kinds("crowd_launch.sh")) == 3 and any("CROWD_LIMIT F4" in e for e in w.events())


def test_stray_models_env_is_not_inherited(tmp_path, monkeypatch):
    monkeypatch.setenv("MODELS", "q35_4b_pxE")
    rc, out = ap.real_run(["/bin/sh", "-c", 'echo "M=${MODELS:-unset}"'], log=tmp_path / "x.log", timeout=30)
    assert rc == 0 and "M=unset" in out
    rc, out = ap.real_run(["/bin/sh", "-c", 'echo "M=${MODELS:-unset}"'], env={"MODELS": "a b"}, log=tmp_path / "y.log",
                          timeout=30)
    assert "M=a b" in out


def test_deadline_relaunch_once_then_needs_orch(tmp_path):
    w = World(tmp_path)
    w.status["F4"] = dict(NO_SHARDS)
    w.after_fetch["F4"] = missing(["q35_4b_pxE"])
    d = w.drv()
    d.one_pass()                                              # launch 1 (all models)
    (w.E / "logs/crowd_F4_q35_4b_pxE.log").write_text('{"launch": "x"}\n{"status": "deadline", "done": 3}\n')
    (w.E / "logs/crowd_F4_q35_4b_main500k.log").write_text('{"status": "done"}\n')
    w.crowd_running = False
    d.one_pass()
    assert len(w.kinds("volume get")) == 3                    # A5: one get per model
    assert len(w.kinds("spend_guard.py")) == 1                # ledger AFTER
    rel = w.kinds("crowd_launch.sh")
    assert len(rel) == 2 and rel[1][1] == {"MODELS": "q35_4b_pxE"} and rel[1][0][-1] == "F4"
    p = d.state["crowd_pending"]
    assert p["attempt"] == 2 and p["models"] == ["q35_4b_pxE"]
    assert not d.orch and not w.kinds("crowd_select.py")
    # second stop of the same model -> NEEDS_ORCH, no third launch
    w.crowd_running = False
    d.one_pass()
    assert len(w.kinds("crowd_launch.sh")) == 2
    assert d.orch and any("NEEDS_ORCH CROWD_STOPPED_TWICE tag=F4" in e and "q35_4b_pxE:deadline" in e
                          for e in w.events())
    # restarted driver: the family is not launched a 3rd time and the event is not repeated
    n_ev = len(w.events())
    d2 = w.drv()
    d2.one_pass()
    assert len(w.kinds("crowd_launch.sh")) == 2 and not w.events() and not d2.orch and n_ev >= 1


def test_select_right_after_fetch(tmp_path):
    w = World(tmp_path)
    w.status["F4"] = dict(NO_SHARDS)
    w.after_fetch["F4"] = no_g13(sel_need=True)
    d = w.drv()
    d.one_pass()
    w.crowd_running = False
    d.one_pass()
    sel = w.kinds("crowd_select.py")
    assert len(sel) == 1 and sel[0][0][-3:] == ["select", "--fam", "F4"]
    ev = [e for e in w.events() if "SELECT F4" in e]
    assert len(ev) == 1 and "pass=True" in ev[0] and "rows=900/1000" in ev[0] and "g5_sample=300" in ev[0] \
        and "g5_low=2" in ev[0] and "g5_total=301" in ev[0]
    assert d.orch and not w.spawned                            # no A25_READY: G13 not started
    # the same candidates sha is not selected twice
    d.one_pass()
    assert len(w.kinds("crowd_select.py")) == 1


def test_select_for_no_selection_state(tmp_path):
    w = World(tmp_path)
    w.status["F6"] = {"ok": False, "status": ap.ST_NO_SEL, "next": "RUNBOOK C1 (crowd_select select)",
                      "cand_sha": "s1", "sel_need": True}
    w.select_pass = False
    d = w.drv()
    d.one_pass()
    assert any("NEEDS_ORCH SELECT F6 pass=False" in e for e in w.events())


def test_g13_gated_on_a25_ready_and_reported(tmp_path):
    w = World(tmp_path)
    w.status["F5"] = no_g13()
    w.status["F3"] = {"ok": False, "status": "incomplete (6 reasons; first: x)", "next": "RUNBOOK B (G13: re-run / "
                      "owner items)", "g13": ["G13 F3: incomplete (6 reasons; first: stale-looking text)"],
                      "cand_sha": "s1", "sel_need": False}
    w.status["F7"] = {"ok": False, "status": "1 Claude-written", "next": "RUNBOOK B (G13: re-run / owner items)",
                      "g13": ["G13 F7: 1 Claude-written seed literal(s) hit an eval set (builder fixes the seed, then "
                              "re-run)"], "cand_sha": "s1", "sel_need": False}
    d = w.drv()
    d.one_pass()
    assert not w.spawned and not d.orch                       # no A25_READY
    (w.E / "A25_READY").write_text("")
    w.other_g13 = True                                        # another decontam_g13 process (census) runs
    d.one_pass()
    assert not w.spawned
    w.other_g13 = False
    d.one_pass()
    assert len(w.spawned) == 1
    cmd = w.spawned[0]
    i = cmd.index("nice")
    assert cmd[i:i + 3] == ["nice", "-n", "5"] and cmd[i + 4:] == ["c_build/decontam_g13_batch.py", "--sets", "F3",
                                                                     "F5"]
    assert any("INFO G13_STARTED sets=F3,F5" in e for e in w.events()) and not d.orch
    d.one_pass()                                              # still running: no second batch
    assert len(w.spawned) == 1
    # the batch ends: counts-only report, then NEEDS_ORCH
    dec = w.lean / "logs/decontam_counts"
    (dec / "F5.json").write_text(json.dumps({"complete": True, "drop_ids": ["i1", "i2"], "drop_units": 1,
                                             "seeds_clean": True, "incomplete_why": [],
                                             "counts_by_eval_and_method": {"ev1": {"exact": {"units": 1,
                                                                                             "eval_items": 3}}}}))
    Path(d.state["g13_batch"]["log"]).write_text("G13 F5: ...\nAUTO_EXIT 0\n")
    w.g13_running = False
    # race: the pass's status was taken while the batch still ran (F5 still 'no G13 counts log') -> report only,
    # never a second batch on that stale status
    d.one_pass()
    ev = [e for e in w.events() if "G13_DONE" in e]
    assert len(ev) == 1 and "rc=0" in ev[0] and "F5:complete=True,drop_ids=2" in ev[0] and "hit_units=1" in ev[0] \
        and "hit_items=3" in ev[0] and "F3:no_fresh_record" in ev[0]
    assert d.orch and d.state["g13_batch"] is None and len(w.spawned) == 1
    # restarted driver, fresh status: F3 was run by the driver and is still incomplete (not stale) -> no automatic
    # re-run, NEEDS_ORCH once; F5 now has its counts log
    w.status["F5"] = {"ok": False, "status": ap.ST_NO_SEL, "next": "RUNBOOK C1", "cand_sha": "s1", "sel_need": False}
    w.status["F3"]["g13"] = ["G13 F3: incomplete (2 reasons; first: y)"]
    d2 = w.drv()
    d2.one_pass()
    assert len(w.spawned) == 1 and any("G13_STUCK F3" in e for e in w.events()) and d2.orch
    d3 = w.drv()
    d3.one_pass()
    assert not any("G13_STUCK" in e for e in w.events()) and len(w.spawned) == 1
    # a set the driver ran that still has no counts log (batch crashed) -> NEEDS_ORCH once, no blind re-run loop
    w.status["F3"] = no_g13()
    d4 = w.drv()
    d4.one_pass()
    assert len(w.spawned) == 1 and any("G13_STUCK F3" in e and "no counts log" in e for e in w.events())


def test_ready_and_loop_exit_codes(tmp_path):
    w = World(tmp_path)
    d = w.drv()
    assert ap.run_loop(d, once=True) == 0                    # baseline pass: no event
    assert not w.events()
    w.status["F9"] = dict(PASS)
    d = w.drv()
    assert ap.run_loop(d, sleep=lambda s: (_ for _ in ()).throw(AssertionError("slept"))) == 0
    assert w.events() == ["EVENT NEEDS_ORCH READY F9"]
    d = w.drv()                                              # restart: READY not repeated
    assert ap.run_loop(d, once=True) == 0 and not w.events()

    def boom():
        raise KeyError("x")
    d = w.drv()
    d.status_fn = boom
    assert ap.run_loop(d, once=True) == 1
    assert w.events() == ["EVENT NEEDS_ORCH ERROR KeyError"]


def test_auto_stop_and_dry_run_launch_nothing(tmp_path):
    w = World(tmp_path)
    w.status["F4"] = dict(NO_SHARDS)
    w.status["F5"] = no_g13(sel_need=True)
    (w.E / "A25_READY").write_text("")
    d = w.drv()
    d.dry = True
    d.one_pass()
    assert not w.calls and not w.spawned and not (w.E / "logs/auto_pipeline_state.json").exists()
    txt = w.out.getvalue()
    assert "would launch" in txt and "would select F5" in txt and "would start G13 batch" in txt
    (w.E / "AUTO_STOP").write_text("")
    d = w.drv()
    assert ap.run_loop(d) == 0 and not w.calls


def test_g13_mixdev_only_staleness_runs_refresh_not_a_batch(tmp_path):
    w = World(tmp_path)
    stale = "G13 F3: stale eval side (opendecide-data/lean/c_src/F12/out/mixdev_S5.jsonl changed or gone; " \
            "`refresh` (mixdev only))"
    w.status["F3"] = {"ok": False, "status": "stale", "next": "RUNBOOK B (G13: re-run / owner items)",
                      "g13": [stale, "G13 F3: 1 Claude-written seed literal(s) hit an eval set (builder fixes the "
                                     "seed, then re-run)"], "cand_sha": "s1", "sel_need": False}
    w.status["F9"] = {"ok": False, "status": "stale", "next": "RUNBOOK B (G13: re-run / owner items)",
                      "g13": [stale.replace("F3", "F9")], "cand_sha": "s1", "sel_need": False}
    (w.E / "A25_READY").write_text("")
    d = w.drv()
    d.one_pass()
    assert len(w.spawned) == 1
    cmd = w.spawned[0]
    assert cmd[cmd.index("nice") + 4:] == ["c_build/decontam_g13.py", "refresh", "F3", "F9"]
    # a set that needs a full run goes first, alone (the batch covers mixdev too)
    w2 = World(tmp_path / "b")
    w2.status["F9"] = dict(w.status["F9"])
    w2.status["F5"] = no_g13()
    (w2.E / "A25_READY").write_text("")
    d2 = w2.drv()
    d2.one_pass()
    cmd = w2.spawned[0]
    assert cmd[cmd.index("nice") + 4:] == ["c_build/decontam_g13_batch.py", "--sets", "F5"]
