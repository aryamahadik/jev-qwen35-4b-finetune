"""auto_pipeline.py: zero-Claude-usage background driver for RUNBOOK A (crowd read), C1 (selection) and B (G13).

Advances every family the moment it qualifies, so nothing waits for the orchestrator. Every pass (default 240 s):
  status  autopilot_check.family() for every family, evaluated in a FRESH child process each time (`--status-json`;
          decontam_g13 / autopilot keep in-process caches that a long-lived process would see as stale).
  (a) crowd  at most one launch in flight (pgrep -f 'modal_crowd.py::crowd'). When none runs and a launch is pending:
          fetch labels for each family x model exactly as RUNBOOK A5 (atmosphor, `modal volume get`; --force only when
          the local labels dir already exists, i.e. a re-fetch), ledger AFTER (spend_guard.py), read each app log
          logs/crowd_<TAG>_<model>.log: a family whose missing models ALL show a stop there ({"status": "deadline..."}
          or a traceback) is relaunched ONCE with only those models (MODELS=... crowd_launch.sh); a family stopped
          again (its 2nd driver launch), or incomplete with no stop in the log -> held + NEEDS_ORCH (no blind
          relaunch). Then every family 'QC PASS; no crowd shards' or with crowd labels missing (not held) goes into
          ONE `bash c_build/endgame/crowd_launch.sh atmosphor <FAMS>` (MODELS only when every family lacks only some
          models); REFUSED -> those families held, NEEDS_ORCH and exit at once. A family is never in a 3rd driver
          launch (CROWD_LIMIT; --reset keeps the launch count).
  (b) select right after a family's labels are fetched, and for any crowd-complete family whose select_<F>.json is
          missing or bound to another candidates sha (states 'decontam done; no selection', 'selection is stale', or
          earlier: selection does not depend on G13): `crowd_select.py select --fam F` -> NEEDS_ORCH with pass,
          rows/target and the G5 re-read sizes. One automatic try per candidates sha.
  (c) G13    only when c_build/endgame/A25_READY exists, one batch at a time, and no other decontam_g13 process runs:
          families 'crowd done; no G13 counts log' or with a G13 problem other than a Claude-written seed hit (that
          one needs the builder first) -> `nice -n 5 python c_build/decontam_g13_batch.py --sets ...` in the background
          (log logs/g13_batch_<tag>.log). When it ends -> NEEDS_ORCH with per set complete flag, drop-id count and hit
          totals (counts only, from logs/decontam_counts/<set>.json); no new batch in that pass (its status predates
          the end). A set the driver already ran is re-run automatically only when its log went stale (inputs
          changed); otherwise (incl. still no counts log) NEEDS_ORCH once. Sets come from a status re-read after the
          pass's crowd / select actions.
  (d) a family turning PASS -> NEEDS_ORCH 'READY <F>' (the PASS set at the first-ever pass is the baseline).
Events: exactly one stdout line each, 'EVENT INFO ...' (no exit) or 'EVENT NEEDS_ORCH ...'. After a pass that printed
a NEEDS_ORCH event the driver exits 0 (REFUSED exits at once); any exception -> 'EVENT NEEDS_ORCH ERROR ...', exit 1.
Paid spend happens ONLY through crowd_launch.sh (atmosphor free credit; server-side cap). No other paid call, no git.
Counts and ids of families only; never a row text.

  cd lean && nohup ../.venv/bin/python c_build/endgame/auto_pipeline.py > c_build/endgame/logs/auto_pipeline.out 2>&1 &
  ../.venv/bin/python c_build/endgame/auto_pipeline.py --dry-run        # what one pass would do; launches nothing
  ../.venv/bin/python c_build/endgame/auto_pipeline.py --once           # one real pass
  ../.venv/bin/python c_build/endgame/auto_pipeline.py --until 1791400000
  ../.venv/bin/python c_build/endgame/auto_pipeline.py --reset F4       # release F4's crowd hold, G13/select counters
  touch c_build/endgame/AUTO_STOP                                        # stop the loop
State: logs/auto_pipeline_state.json. Action log: logs/auto_pipeline.log.
"""
from __future__ import annotations

import argparse
import json
import os
import re
import subprocess
import sys
import time
import traceback
from pathlib import Path

HERE = Path(__file__).resolve().parent          # c_build/endgame
CB = HERE.parent
LEAN = CB.parent
PY = str(LEAN.parent / ".venv/bin/python")
MODAL = str(LEAN.parent / ".venv/bin/modal")
PROFILE = os.environ.get("CROWD_PROFILE", "atmosphor")  # owner 7 Oct 01:10 UTC: mahadikarya44 after atmosphor
MODELS = ["q35_4b_main500k", "q35_4b_pxE", "q35_4b_base0"]
FAMS = [f"F{i}" for i in range(1, 14)] + ["COMMIT"]
INTERVAL = 240
CROWD_PAT = "modal_crowd.py::crowd"
REFRESH_HINT = "`refresh` (mixdev only)"    # decontam_g13.log_problems: a log stale only in mixdev files
G13_PAT = "decontam_g13"            # a lone run, census, embed-cache or a batch: never two eval passes at once
ST_NO_SHARDS = "QC PASS; no crowd shards"
ST_NO_G13 = "crowd done; no G13 counts log"
ST_NO_SEL = "decontam done; no selection"
ST_STALE_SEL = "selection is stale"
ST_SEL_FAIL = "selection checks fail"
NX_CROWD = "RUNBOOK A3-A5"
NX_G13 = "RUNBOOK B (G13"
SEED_HIT = "builder fixes the seed"


class ExitNow(Exception):
    def __init__(self, code: int):
        super().__init__(code)
        self.code = code


def crowd_missing(d: dict) -> bool:
    return d["status"] == ST_NO_SHARDS or d["next"].startswith(NX_CROWD)


def post_crowd(d: dict) -> bool:
    s = d["status"]
    return bool(d["ok"]) or s in (ST_NO_G13, ST_NO_SEL, ST_SEL_FAIL) or s.startswith(ST_STALE_SEL) \
        or d["next"].startswith(NX_G13)


def g13_kind(p: str) -> str:
    """Kind of one decontam_g13.log_problems message ('G13 <set>: <what> ...'), judged by its head only (the
    incomplete reason text that follows may contain any word)."""
    what = p.split(": ", 1)[-1]
    for k in ("stale", "incomplete", "methods", "no drop_ids"):
        if what.startswith(k):
            return k.replace(" ", "_")
    return "seed_hit" if SEED_HIT in what else "other"


def stop_reason(text: str) -> str | None:
    if '"status": "deadline' in text:
        return "deadline"
    if "Traceback (most recent call last)" in text:
        return "traceback"
    return None


def hit_totals(rec: dict) -> tuple[int, int]:
    u = i = 0
    for ms in (rec.get("counts_by_eval_and_method") or {}).values():
        for v in (ms.values() if isinstance(ms, dict) else ()):
            if isinstance(v, dict):
                u += int(v.get("units") or 0)
                i += int(v.get("eval_items") or 0)
    return u, i


def jload(p: Path):
    try:
        return json.loads(Path(p).read_text())
    except Exception:  # noqa: BLE001
        return None


def read(p: Path) -> str:
    try:
        return Path(p).read_text(errors="replace")
    except OSError:
        return ""


# ------------------------------------------------------------------ real backends (mocked in tests)

def status_snapshot() -> dict:
    """Runs in the --status-json child: autopilot_check.family() (same wrapper as its main) + the details the driver
    needs (models missing per crowd family, full G13 problems, selection binding)."""
    sys.path.insert(0, str(HERE))
    sys.path.insert(0, str(CB))
    import autopilot_check as ap
    import crowd_select as cs
    import decontam_g13 as dg
    from mixio import sha256_file
    out = {}
    for fam in ap.FAMS:
        try:
            ok, status, nxt = ap.family(fam)
        except SystemExit as e:
            ok, status, nxt = False, f"refused: {str(e)[:50]}", "lane: fix MANIFEST / relations"
        except Exception as e:  # noqa: BLE001
            ok, status, nxt = False, f"check error {type(e).__name__}", "inspect"
        d = {"ok": ok, "status": status, "next": nxt}
        if nxt.startswith(NX_CROWD):
            probs = cs.crowd_complete(fam)
            d["crowd_missing"] = MODELS[:] if any("no crowd shards" in p for p in probs) else \
                [m for m in MODELS if any(f"labels of {m} " in p for p in probs)]
        if nxt.startswith(NX_G13):
            d["g13"] = dg.log_problems([fam])
        if post_crowd(d):
            sha = sha256_file(cs.fam_files(fam)["cand"])
            sel = jload(cs.OUT / f"select_{fam}.json")
            d["cand_sha"] = sha
            d["sel_need"] = sel is None or sel.get("candidates_sha256") != sha
        out[fam] = d
    return out


def child_status() -> dict:
    r = subprocess.run([PY, str(Path(__file__).resolve()), "--status-json"], cwd=LEAN, capture_output=True, text=True,
                       timeout=900, stdin=subprocess.DEVNULL)
    for line in reversed(r.stdout.splitlines()):
        if line.startswith("STATUS_JSON "):
            return json.loads(line[len("STATUS_JSON "):])
    raise RuntimeError(f"status child rc={r.returncode}")


def real_run(cmd, env=None, log=None, timeout=1800):
    log = Path(log)
    log.parent.mkdir(parents=True, exist_ok=True)
    base = {k: v for k, v in os.environ.items() if k != "MODELS"}    # a stray MODELS must never narrow a launch
    with open(log, "w") as fh:
        try:
            rc = subprocess.run(cmd, cwd=LEAN, env={**base, **(env or {})}, stdin=subprocess.DEVNULL, stdout=fh,
                                stderr=subprocess.STDOUT, timeout=timeout, start_new_session=True).returncode
        except subprocess.TimeoutExpired:
            rc = 124
    return rc, read(log)


def real_pgrep(pat: str) -> bool:
    return subprocess.run(["pgrep", "-f", pat], capture_output=True).returncode == 0


# ------------------------------------------------------------------ driver

class Driver:
    def __init__(self, dry=False, status_fn=None, run_fn=None, spawn_fn=None, pgrep_fn=None, alive_fn=None,
                 e_dir: Path = HERE, lean: Path = LEAN, out=None):
        self.dry = dry
        self.E, self.lean = Path(e_dir), Path(lean)
        self.LOGS = self.E / "logs"
        self.state_path = self.LOGS / "auto_pipeline_state.json"
        self.log_path = self.LOGS / "auto_pipeline.log"
        self.sel_dir = self.lean / "c_build/crowd_r1"
        self.dec_dir = self.lean / "logs/decontam_counts"
        self.shards = self.lean / "data/c_crowd_r1_shards"
        self.status_fn = status_fn or child_status
        self.run_fn = run_fn or real_run
        self.spawn_fn = spawn_fn or self._spawn
        self.pgrep_fn = pgrep_fn or real_pgrep
        self.alive_fn = alive_fn or self._alive
        self.out = out or sys.stdout
        self._children: dict[int, subprocess.Popen] = {}
        self.state = self._load()
        self.orch = False
        self.crowd_blocked = False
        self.acted = False

    # ---- state / output
    def _load(self) -> dict:
        s = jload(self.state_path) or {}
        for k, v in (("crowd_pending", None), ("fam_launches", {}), ("crowd_hold", {}), ("g13_batch", None),
                     ("g13_runs", {}), ("select_done", {}), ("pass_set", None), ("emitted", [])):
            s.setdefault(k, v)
        return s

    def save(self):
        if self.dry:
            return
        self.LOGS.mkdir(parents=True, exist_ok=True)
        tmp = self.state_path.with_suffix(".tmp")
        tmp.write_text(json.dumps(self.state, indent=1, sort_keys=True))
        tmp.replace(self.state_path)

    def log(self, msg: str):
        if self.dry:
            return
        self.LOGS.mkdir(parents=True, exist_ok=True)
        with open(self.log_path, "a") as f:
            f.write(time.strftime("%Y-%m-%dT%H:%M:%SZ ", time.gmtime()) + msg + "\n")

    def say(self, line: str):
        print(line, file=self.out, flush=True)

    def info(self, text: str):
        self.say(("DRY would: INFO " if self.dry else "EVENT INFO ") + text)
        self.log("EVENT INFO " + text)

    def needs_orch(self, text: str, key: str | None = None, also: list[str] = ()):
        if key and key in self.state["emitted"]:
            return
        self.say(("DRY would: NEEDS_ORCH " if self.dry else "EVENT NEEDS_ORCH ") + text)
        self.log("EVENT NEEDS_ORCH " + text)
        if not self.dry:
            self.orch = True
            self.state["emitted"] += [k for k in ([key] if key else []) + list(also) if k not in self.state["emitted"]]

    def note(self, text: str):
        if self.dry:
            self.say("DRY " + text)
        else:
            self.log(text)

    # ---- process helpers
    def _spawn(self, cmd, log) -> int:
        Path(log).parent.mkdir(parents=True, exist_ok=True)
        fh = open(log, "a")
        p = subprocess.Popen(cmd, cwd=self.lean, stdin=subprocess.DEVNULL, stdout=fh, stderr=subprocess.STDOUT,
                             start_new_session=True)
        fh.close()
        self._children[p.pid] = p
        return p.pid

    def _alive(self, pid: int) -> bool:
        p = self._children.get(pid)
        if p is not None:
            return p.poll() is None
        try:
            os.kill(pid, 0)
        except ProcessLookupError:
            return False
        except PermissionError:
            return True
        cmd = subprocess.run(["ps", "-p", str(pid), "-o", "command="], capture_output=True, text=True).stdout
        return "decontam_g13_batch" in cmd

    # ---- one pass
    def one_pass(self):
        self.orch = self.crowd_blocked = self.acted = False
        st = self.status_fn()
        st = self.step_crowd(st)
        self.step_select(st)
        st = self.fresh(st)                 # G13 picks its sets from a status taken after this pass's actions
        self.step_g13(st)
        st = self.fresh(st)
        self.step_ready(st)
        self.save()

    def fresh(self, st: dict) -> dict:
        if self.acted and not self.dry:
            self.acted = False
            return self.status_fn()
        return st

    def hold(self, fams: dict, text: str, key: str | None = None):
        """Never launch these families again (until --reset): the orchestrator / owner decides. One NEEDS_ORCH."""
        self.state["crowd_hold"].update(fams)
        self.needs_orch(text, key=key)

    # ---- (a) crowd
    def step_crowd(self, st: dict) -> dict:
        if self.pgrep_fn(CROWD_PAT):
            self.note("crowd: a launch is in flight (modal_crowd.py::crowd running); wait")
            return st
        if self.state["crowd_pending"]:
            st = self.finish_pending(st)
            if self.state["crowd_pending"] or self.crowd_blocked:
                return st
        fams, need = [], set()
        for f, d in st.items():
            if not crowd_missing(d) or f in self.state["crowd_hold"]:
                continue
            n = self.state["fam_launches"].get(f, 0)
            if n >= 2:
                self.hold({f: "launch limit"}, f"CROWD_LIMIT {f}: still missing crowd labels after {n} driver launches "
                          f"(missing {','.join(d.get('crowd_missing') or []) or '?'})", key=f"crowd_limit:{f}")
                continue
            fams.append(f)
            need |= set(d.get("crowd_missing") or MODELS)
        if fams:
            # all 3 models unless every family only lacks some (e.g. its one relaunch after a REFUSED relaunch:
            # only the models still missing, RUNBOOK A MODELS form); a family with 1 driver launch gets its 2nd = last
            models = [m for m in MODELS if m in need]
            self.launch(fams, models=None if len(models) == len(MODELS) else models,
                        attempt=1 + max(self.state["fam_launches"].get(f, 0) for f in fams))
        return st

    def fetch(self, fam: str, model: str) -> int:
        dest = self.shards / fam
        force = ["--force"] if (dest / f"labels_{model}").exists() else []
        cmd = [MODAL, "volume", "get", *force, "opendecide", f"crowd_r1_shards/{fam}/labels_{model}",
               f"data/c_crowd_r1_shards/{fam}/"]
        rc, _ = self.run_fn(cmd, env={"MODAL_PROFILE": PROFILE}, log=self.LOGS / f"auto_fetch_{fam}_{model}.log",
                            timeout=900)
        self.log(f"fetch {fam} labels_{model}: rc {rc}{' (--force re-fetch)' if force else ''}")
        return rc

    def finish_pending(self, st: dict) -> dict:
        p = self.state["crowd_pending"]
        fams, models, tag = p["fams"], p["models"], p["tag"]
        stops = {m: stop_reason(read(self.LOGS / f"crowd_{tag}_{m}.log")) for m in models}
        if self.dry:
            self.note(f"would fetch labels {fams} x {models} (A5), ledger AFTER; app-log stops now: "
                      f"{ {m: r for m, r in stops.items() if r} or 'none'}; then relaunch incomplete models once "
                      f"(attempt {p['attempt']}) and select the complete families")
            return st
        self.acted = True
        fails = [(f, m) for f in fams for m in models if self.fetch(f, m) != 0]
        retry = [f"{f}/{m}" for f, m in fails if not stops[m]]
        if retry and p.get("fetch_tries", 0) < 2:
            p["fetch_tries"] = p.get("fetch_tries", 0) + 1
            self.log(f"crowd {tag}: fetch failed for {retry} with no stop in the app log; retry next pass "
                     f"({p['fetch_tries']}/2)")
            self.save()
            return st
        rc, out = self.run_fn([PY, "c_build/endgame/spend_guard.py", "ledger", PROFILE,
                               f"crowd {','.join(fams)}: AFTER", "--payer", "credit"],
                              log=self.LOGS / f"auto_ledger_{tag}.log", timeout=300)
        self.log(f"ledger AFTER crowd {tag}: rc {rc}")
        st = self.status_fn()
        inc = {f: list(st[f].get("crowd_missing") or MODELS) for f in fams if crowd_missing(st[f])}
        done = [f for f in fams if post_crowd(st[f])]
        self.state["crowd_pending"] = None
        self.info(f"CROWD_FETCHED tag={tag} attempt={p['attempt']} complete={','.join(done) or '-'} "
                  f"incomplete={','.join(f'{f}:{len(ms)}' for f, ms in inc.items()) or '-'} fetch_fail={len(fails)} "
                  f"stops={','.join(f'{m}:{r}' for m, r in stops.items() if r) or '-'}")
        for f in done:
            self.select(f, st[f], why="labels fetched")
        # relaunch ONLY models the app log shows stopped (deadline / traceback), at most once per family (its 2nd
        # driver launch); a model incomplete with no stop in its log (e.g. a dead client while the app may still run)
        # or a 2nd stop -> hold the family + NEEDS_ORCH, never a blind relaunch
        rel, twice, nostop = [], {}, {}
        for f, ms in inc.items():
            ns = [m for m in ms if m not in models or not stops.get(m)]
            if ns:
                nostop[f] = ns
            elif self.state["fam_launches"].get(f, 0) >= 2:
                twice[f] = ms
            else:
                rel.append(f)
        if twice:
            ms = sorted({m for v in twice.values() for m in v}, key=MODELS.index)
            self.hold({f: "stopped twice" for f in twice}, f"CROWD_STOPPED_TWICE tag={tag} fams={','.join(twice)} "
                      f"models={','.join(f'{m}:{stops.get(m)}' for m in ms)}")
        if nostop:
            ms = sorted({m for v in nostop.values() for m in v}, key=MODELS.index)
            self.hold({f: "incomplete, no stop in the app log" for f in nostop},
                      f"CROWD_INCOMPLETE_NO_STOP tag={tag} fams={','.join(nostop)} models={','.join(ms)} (labels "
                      f"incomplete but the app log shows no deadline / traceback: check the app before any relaunch)")
        if twice or nostop:
            self.crowd_blocked = True     # no fresh launch this pass (the orchestrator looks first, e.g. A6 rate)
        if rel:
            bad = sorted({m for f in rel for m in inc[f]}, key=MODELS.index)
            why = ",".join(f"{m}:{stops.get(m)}" for m in bad)
            self.log(f"crowd {tag}: relaunch once for {','.join(rel)} {why}")
            self.launch(rel, models=bad, attempt=p["attempt"] + 1)
        return st

    def launch(self, fams: list[str], models: list[str] | None = None, attempt: int = 1):
        tag = "_".join(fams)
        cmd = ["bash", "c_build/endgame/crowd_launch.sh", PROFILE, *fams]
        env = {"MODELS": " ".join(models)} if models else None
        shown = (f"MODELS=\"{env['MODELS']}\" " if env else "") + " ".join(cmd)
        if self.dry:
            self.note(f"would launch (attempt {attempt}): {shown}")
            return
        self.acted = True
        self.log(f"launch: {shown}")
        rc, out = self.run_fn(cmd, env=env, log=self.LOGS / f"auto_launch_{tag}_a{attempt}.log", timeout=1800)
        if "REFUSED" in out:
            # held until `--reset <F>` (RUNBOOK A6: stop launching, the owner decides), so a restarted driver does not
            # re-hit the same REFUSED on every start and its selections / G13 keep moving
            self.hold({f: "REFUSED" for f in fams}, f"CROWD_REFUSED fams={','.join(fams)} "
                      f"models={len(models or MODELS)} rc={rc} (owner decides: spill to the aryamhd card or wait; "
                      f"then --reset {' '.join(fams)})")
            self.crowd_blocked = True
            self.save()
            raise ExitNow(0)
        ok = rc == 0 and "LAUNCHED" in out
        if ok or self.pgrep_fn(CROWD_PAT):
            self.state["crowd_pending"] = {"tag": tag, "fams": fams, "models": models or MODELS[:], "attempt": attempt,
                                           "start": time.time(), "fetch_tries": 0}
            for f in fams:
                self.state["fam_launches"][f] = self.state["fam_launches"].get(f, 0) + 1
            self.save()
        if ok:
            cap = re.search(r"CAP_MIN=(\d+)", out)
            self.info(f"CROWD_LAUNCHED fams={','.join(fams)} models={','.join(models or MODELS)} attempt={attempt} "
                      f"cap_min={cap.group(1) if cap else '?'}")
        else:
            self.needs_orch(f"CROWD_LAUNCH_FAILED fams={','.join(fams)} rc={rc} (no LAUNCHED line; see "
                            f"logs/auto_launch_{tag}_a{attempt}.log)")
            self.crowd_blocked = True

    # ---- (b) selection
    def step_select(self, st: dict):
        for f, d in st.items():
            if post_crowd(d) and d.get("sel_need") and self.state["select_done"].get(f) != d.get("cand_sha"):
                self.select(f, d, why=d["status"][:40])

    def select(self, fam: str, d: dict, why: str):
        cmd = [PY, "c_build/crowd_select.py", "select", "--fam", fam]
        if self.dry:
            self.note(f"would select {fam} ({why}): {' '.join(cmd[1:])}")
            return
        self.acted = True
        t0 = time.time()
        rc, out = self.run_fn(cmd, log=self.LOGS / f"auto_select_{fam}.log", timeout=3600)
        self.state["select_done"][fam] = d.get("cand_sha")
        sp = self.sel_dir / f"select_{fam}.json"
        rec = jload(sp) if sp.exists() and sp.stat().st_mtime >= t0 - 1 else None
        if rc != 0 or rec is None:
            err = next((m.group(1) for ln in reversed(out.splitlines())
                        if (m := re.match(r"^([A-Za-z_][\w.]*(?:Error|Exception|Exit))\b", ln.strip()))), "?")
            self.needs_orch(f"SELECT {fam} FAILED rc={rc} error={err} fresh_record={rec is not None}")
            return
        rep = rec.get("report") or {}
        g5 = jload(self.sel_dir / f"g5_reread_{fam}.json") or {}
        low, smp = g5.get("low_ids") or [], g5.get("sample_ids") or []
        self.needs_orch(f"SELECT {fam} pass={rep.get('pass')} rows={rep.get('rows')}/{rep.get('target', rec.get('target'))}"
                        f" g5_low={g5.get('n_low', len(low))} g5_sample={len(smp)} g5_total={len(set(low) | set(smp))}"
                        " (start the G9 re-read agent)")

    # ---- (c) G13
    def step_g13(self, st: dict):
        b = self.state["g13_batch"]
        if b:
            if self.alive_fn(b["pid"]):
                self.note(f"G13 batch {b['tag']} running (pid {b['pid']})")
                return
            self.finish_g13(b)
            return              # this pass's status may predate the batch end: never start the next batch on it
        sets, refresh_only = [], set()
        for f, d in st.items():
            if d["status"] == ST_NO_G13:
                runs = self.state["g13_runs"].get(f, 0)
                if runs >= 1:     # the driver's batch left no counts log for it (crashed / killed): no blind loop
                    self.needs_orch(f"G13_STUCK {f}: driver ran it {runs}x, still no counts log",
                                    key=f"g13_nolog:{f}:{runs}")
                    continue
                sets.append(f)
            elif d["next"].startswith(NX_G13):
                probs = d.get("g13") or []
                if not probs or all(g13_kind(p) == "seed_hit" for p in probs):
                    continue                  # a Claude-written seed hit: the builder fixes the seed first
                if all(g13_kind(p) == "stale" and REFRESH_HINT in p for p in probs if g13_kind(p) != "seed_hit") \
                        and any(g13_kind(p) == "stale" for p in probs):
                    refresh_only.add(f)       # only mixdev files changed: re-scan mixdev alone (minutes, not hours)
                runs = self.state["g13_runs"].get(f, 0)
                if runs >= 1 and not any(g13_kind(p) == "stale" for p in probs):
                    self.needs_orch(f"G13_STUCK {f}: driver ran it {runs}x, still "
                                    f"{','.join(sorted({g13_kind(p) for p in probs}))} (not stale)",
                                    key=f"g13_stuck:{f}:{runs}")
                    continue
                sets.append(f)
        if not sets:
            return
        if not (self.E / "A25_READY").exists():
            self.note(f"G13 skipped: no A25_READY (would batch {' '.join(sets)})")
            return
        if self.pgrep_fn(G13_PAT):
            self.note(f"G13 waits: another decontam_g13 process is running (would batch {' '.join(sets)})")
            return
        full = [f for f in sets if f not in refresh_only]
        if full:                              # one process at a time: a full batch first (it covers mixdev too)
            sets = full
        tag = time.strftime("%m%d_%H%M", time.gmtime()) + "_" + ("refresh_" if not full else "") + "_".join(sets)
        log = self.LOGS / f"g13_batch_{tag}.log"
        cmd = ["nice", "-n", "5", PY, "c_build/decontam_g13_batch.py", "--sets", *sets] if full else \
            ["nice", "-n", "5", PY, "c_build/decontam_g13.py", "refresh", *sets]
        if self.dry:
            self.note(f"would start G13 batch: {' '.join(cmd)} > {log.name}")
            return
        self.acted = True
        wrapped = ["/bin/sh", "-c", '"$@"; echo "AUTO_EXIT $?"', "sh", *cmd]
        pid = self.spawn_fn(wrapped, log)
        self.state["g13_batch"] = {"pid": pid, "sets": sets, "tag": tag, "log": str(log), "start": time.time()}
        self.save()
        self.info(f"G13_STARTED sets={','.join(sets)} pid={pid} log={log.name}")

    def finish_g13(self, b: dict):
        if self.dry:
            self.note(f"would report G13 batch {b['tag']} (ended) and clear it")
            return
        self.acted = True
        ex = re.findall(r"AUTO_EXIT (\d+)", read(Path(b["log"])))
        parts = []
        for s in b["sets"]:
            p = self.dec_dir / f"{s}.json"
            rec = jload(p) if p.exists() and p.stat().st_mtime >= b["start"] - 1 else None
            self.state["g13_runs"][s] = self.state["g13_runs"].get(s, 0) + 1
            if rec is None:
                parts.append(f"{s}:no_fresh_record")
                continue
            u, i = hit_totals(rec)
            parts.append(f"{s}:complete={rec.get('complete')},drop_ids={len(rec.get('drop_ids') or [])},"
                         f"drop_units={rec.get('drop_units')},hit_units={u},hit_items={i},"
                         f"seeds_clean={rec.get('seeds_clean')},incomplete_reasons={len(rec.get('incomplete_why') or [])}")
        self.state["g13_batch"] = None
        self.save()
        self.needs_orch(f"G13_DONE tag={b['tag']} rc={ex[-1] if ex else '?'} " + " ; ".join(parts))

    # ---- (d) READY
    def step_ready(self, st: dict):
        now = sorted(f for f, d in st.items() if d["ok"])
        prev = self.state["pass_set"]
        if prev is None:
            self.note(f"READY baseline (first pass): {','.join(now) or 'none'}")
            self.state["pass_set"] = now
            return
        for f in now:
            if f not in prev:
                self.needs_orch(f"READY {f}")
        self.state["pass_set"] = now

    def reset(self, fams: list[str]):
        """Release crowd holds and clear the G13 / select counters. The per-family launch count is KEPT: the driver
        never launches a family a 3rd time (one relaunch per family, ever); beyond that the orchestrator acts by hand."""
        for f in fams:
            for k in ("crowd_hold", "g13_runs", "select_done"):
                self.state[k].pop(f, None)
            self.state["emitted"] = [k for k in self.state["emitted"] if k.split(":")[1:2] != [f]]
        self.log(f"reset holds / G13 / select counters for {fams} (launch counts kept: "
                 f"{ {f: self.state['fam_launches'].get(f, 0) for f in fams} })")
        self.save()


def run_loop(drv: Driver, once=False, until=None, interval=INTERVAL, sleep=time.sleep) -> int:
    stop = drv.E / "AUTO_STOP"
    drv.log(f"driver start pid {os.getpid()} once={once} until={until}")
    while True:
        if stop.exists() or (until and time.time() >= until):
            drv.info("STOPPED " + ("AUTO_STOP file" if stop.exists() else "--until reached"))
            return 0
        try:
            drv.one_pass()
        except ExitNow as e:
            drv.save()
            return e.code
        except Exception as e:  # noqa: BLE001
            drv.log(traceback.format_exc()[-2000:])
            drv.needs_orch(f"ERROR {type(e).__name__}")
            try:
                drv.save()
            except Exception:  # noqa: BLE001
                pass
            return 1
        if drv.orch or once:
            return 0
        t_end = time.time() + interval
        while time.time() < t_end:
            if stop.exists():
                break
            sleep(min(10, max(0.0, t_end - time.time())))


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description="zero-Claude-usage driver for RUNBOOK A / C1 / B")
    ap.add_argument("--dry-run", action="store_true", help="print what one pass would do; launch / write nothing")
    ap.add_argument("--once", action="store_true", help="one real pass, then exit")
    ap.add_argument("--until", type=float, default=None, help="stop at this unix time")
    ap.add_argument("--interval", type=int, default=INTERVAL)
    ap.add_argument("--reset", nargs="+", metavar="F",
                    help="release crowd holds, clear G13 / select counters (launch counts kept)")
    ap.add_argument("--status-json", action="store_true", help=argparse.SUPPRESS)
    a = ap.parse_args(argv)
    if a.status_json:
        print("STATUS_JSON " + json.dumps(status_snapshot()), flush=True)
        return 0
    if a.dry_run:
        drv = Driver(dry=True)
        try:
            drv.one_pass()
        except ExitNow:
            pass
        return 0
    import fcntl
    (HERE / "logs").mkdir(parents=True, exist_ok=True)
    lock = open(HERE / "logs/auto_pipeline.lock", "w")
    try:
        fcntl.flock(lock, fcntl.LOCK_EX | fcntl.LOCK_NB)
    except OSError:
        print("EVENT INFO ALREADY_RUNNING (another auto_pipeline holds the lock)", flush=True)
        return 3
    drv = Driver()
    if a.reset:
        drv.reset(a.reset)
        return 0
    return run_loop(drv, once=a.once, until=a.until, interval=a.interval)


if __name__ == "__main__":
    sys.exit(main())
