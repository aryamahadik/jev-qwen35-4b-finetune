"""l1_look.l1session: the in-container orchestrator of the L1 look. Runs in the SGLang image's python (stdlib + httpx; no Modal import), so the
whole flow runs on CPU in tests against fakes, exactly as grid_h100.session does for the grid.

ONE container, ONE H100, ONE job (A42-D 9 / spec 7.3 / 8.5):  C1 (adapter sha 507d1c29) and, if the pre-gate passed, the chosen C2 candidate.
For each model, in this order, on the SAME frozen S1 path the 19 grid reads used (grid_h100.servers.SglServer = sglang_host.server_cmd, SGLang 0.5.20,
merged BF16, the resolved args held to the S1 pin, one path_sha256 over the boots):
    merge (CPU, one model ahead) -> boot -> check args -> flush -> read the C2 MIXDEV (dev; for the temperature fit) and the look's rows
    (in memory) with the A5 readout (choice rows: given + exact reversal averaged; yes/no once; T = 1 as served) -> stop.
Nothing sealed is written to a Modal Volume: the container returns the reads to the laptop. Errors are reported by class name only once the sealed
rows exist in the process; no server log is kept. The container prints counts and seconds only.

Money: same rule as the grid: a block starts only if prior spend + elapsed x rate + the block estimate <= stop-launch; above the hard stop the loop ends.
"""
from __future__ import annotations

import json
import shutil
import threading
import time
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

from grid_h100 import common as C
from grid_h100 import gridbuild as GB
from grid_h100 import hostops as HO
from grid_h100 import merge_direct as MD
from grid_h100 import servers as SV
from grid_h100.session import ReaderProc, SessionRefused, real_hooks

from . import l1common as L

MIXDEV_SPLIT, FINAL_SPLIT = L.MIXDEV_SPLIT, L.FINAL_SPLIT


class L1ReaderProc(ReaderProc):
    """grid_h100.session.ReaderProc, but the child is l1_look.l1reader and only its 'L1R:' lines are forwarded (it prints nothing else on
    purpose; a traceback of the child never reaches the container log)."""

    def start(self):
        import os
        import subprocess
        self.ctl.mkdir(parents=True, exist_ok=True)
        sp = self.ctl / "spec.json"
        sp.write_text(json.dumps(self.spec))
        env = {k: v for k, v in os.environ.items() if k not in ("PYTHONPATH", "VIRTUAL_ENV")}
        env.update({"PYTHONPATH": self.root, "TOKENIZERS_PARALLELISM": "false", "HF_HUB_OFFLINE": "1", "PYTHONDONTWRITEBYTECODE": "1",
                    "OD_LEAN": str(C.LEAN)})
        self.p = subprocess.Popen([self.python, "-m", "l1_look.l1reader", "serve", "--spec", str(sp)], cwd=self.root, env=env,
                                  stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True, start_new_session=True)

        def pump():
            for line in self.p.stdout:
                if line.startswith("L1R: "):
                    self.log("[reader] " + line.rstrip("\n")[5:])
        threading.Thread(target=pump, daemon=True).start()
        return self


def l1_hooks() -> dict:
    h = real_hooks()
    h["reader"] = lambda spec, log: L1ReaderProc(spec, log=log).start()
    return h


def safe_err(e: BaseException) -> str:
    """Our own refusals (SystemExit) carry authored text; any other exception is reported by its class only."""
    return str(e)[:300] if isinstance(e, SystemExit) else type(e).__name__


class L1Session:
    def __init__(self, plan: dict, final_rows: list, emit=lambda ev: None, hooks: dict | None = None, clock=time.time,
                 rate_usd_h: float = C.FN_RATE_USD_H, prior_usd: float = 0.0, work_root="/tmp/l1_work", vol="/vol", data_dir="/root/data",
                 c1tok_dir="/root/c1tok", log=print, stop_launch: float = C.STOP_LAUNCH_USD, hard_stop: float = C.HARD_STOP_USD):
        self.plan, self.final_rows, self.emit = plan, final_rows, emit
        self.h = {**l1_hooks(), **(hooks or {})}
        self.clock, self.rate, self.prior = clock, rate_usd_h, prior_usd
        self.work, self.vol = Path(work_root), Path(vol)
        self.data_dir, self.c1tok_dir = Path(data_dir), Path(c1tok_dir)
        self.log, self.stop_launch, self.hard_stop = log, stop_launch, hard_stop
        self.t0 = clock()
        self.errors, self.path_sha, self.models = [], None, {}
        est = (plan.get("estimate") or {}).get("scenarios", {}).get("likely", {})
        self.per_model_usd = float(est.get("per_model_s", 400.0)) / 3600.0 * rate_usd_h

    # -- money
    def spent(self) -> float:
        return self.prior + C.container_cost_usd(self.clock() - self.t0, self.rate)

    def gate(self, extra_usd: float) -> tuple:
        s = self.spent()
        if s >= self.hard_stop:
            return False, f"hard stop: spent ${s:.2f} >= ${self.hard_stop:.2f}"
        if s + extra_usd > self.stop_launch:
            return False, f"budget gate: spent ${s:.2f} + estimate ${extra_usd:.2f} > stop-launch ${self.stop_launch:.2f}"
        return True, "ok"

    def ev(self, kind: str, **kw):
        self.emit({"event": kind, "t": round(self.clock() - self.t0, 1), "spent_usd": round(self.spent(), 3), **kw})

    # -- setup
    def setup(self) -> dict:
        h, plan = self.h, self.plan
        gpu = h["gpu_name"]()
        HO.check_gpu(gpu)
        ver = h["sglang_version"]()
        if ver != C.SGLANG_VERSION:
            raise SessionRefused(f"sglang {ver or '(import failed)'} != pinned {C.SGLANG_VERSION}")
        tv = h["torch_versions"]()
        self.pin = h["load_pin"]()
        tok_pins = (self.pin.get("model") or {}).get("tokenizer_pins") or {}
        self.env_meta = {"gpu": gpu.split(",")[0].strip(), "torch": tv["torch"], "cuda": tv["cuda"], "sglang_version": ver}
        self.ev("container_up", gpu_full=gpu, **self.env_meta)
        mx = plan["mixdev"]
        f = self.data_dir / mx["file"]
        if not f.exists() or C.sha256_file(f) != mx["sha256"]:
            raise SessionRefused("the mixdev file is missing or differs from the plan's sha256")
        if C.canon_sha(self.final_rows) != plan["final"]["rows_sha256"] or len(self.final_rows) != plan["final"]["n_rows"]:
            raise SessionRefused("the rows of the look differ from the plan's hash")
        base = h["prepare_base"](str(self.vol / "hf"), str(self.work / "base"), self.log)
        self.base_dir = Path(base["base_dir"])
        self.c1_tok = h["prepare_c1_tok"](self.c1tok_dir, tok_pins)
        self.ev("base_ready", **{k: base[k] for k in ("source", "fetched")})
        self.c1_dir = GB.locate_c1_adapter()                       # held to sha256 507d1c29...
        self.adapters = {C1_KEY: self.c1_dir}
        if plan["mode"] == "c1c2":
            run_dir = Path(plan["c2_run_dir"])
            ri = GB.check_run_dir(run_dir, tok_pins)
            if ri["problems"]:
                raise SessionRefused("the C2 run folder is not usable: " + "; ".join(ri["problems"]))
            cand_dir = self.work / "cand"
            if cand_dir.exists():
                shutil.rmtree(cand_dir)
            built = GB.build_one(self.c1_dir, run_dir, plan["cand"], cand_dir, plan["grid_record"])
            want = next(m["adapter_sha256"] for m in plan["models"] if m["kind"] == "cand")
            if built["adapter_sha256"] != want:
                raise SessionRefused("the candidate rebuilt from the run folder is not the one CANDIDATE_C2.json records")
            self.adapters[C2_KEY] = cand_dir
            self.ev("candidate_built", name=built["name"], rank=built["rank"], adapter_sha256=built["adapter_sha256"])
        return {"gpu": gpu, **self.env_meta, "base": {k: base[k] for k in ("source", "fetched")}}

    def reader_spec(self) -> dict:
        plan = self.plan
        sets = [
            {"split": MIXDEV_SPLIT, "tag": "", "views": 2, "perm_seed": None, "job": "L1", "file": plan["mixdev"]["file"],
             "pred_dir": f"preds_{MIXDEV_SPLIT}", "tta_choice": True},
            {"split": FINAL_SPLIT, "tag": "", "views": 2, "perm_seed": None, "job": "L1", "file": "(memory)", "pred_dir": f"preds_{FINAL_SPLIT}",
             "tta_choice": True, "rows": self.final_rows, "rows_sha256": plan["final"]["rows_sha256"]},
        ]
        return {"c1_dir": str(self.c1_tok), "data_dir": str(self.data_dir), "sets": sets,
                "manifest": {plan["mixdev"]["file"]: {"sha256": plan["mixdev"]["sha256"], "rows": plan["mixdev"]["rows"]}},
                "recorded_check": plan["prompt_check_record"], "ctl_dir": str(self.work / "reader_ctl"), "port": C.PORT}

    def merge_job(self, m: dict) -> dict:
        mdir = self.work / "merged" / m["read_name"]
        if mdir.exists():
            shutil.rmtree(mdir)
        man = self.h["merge"](str(self.base_dir), str(self.adapters[C1_KEY if m["kind"] == "ref" else C2_KEY]), str(mdir), str(self.c1_tok),
                              label=m["read_name"], dev="cpu", expect_adapter_sha=m["adapter_sha256"], log=self.log)
        return {"dir": mdir, "manifest": man}

    # -- one model
    def run_model(self, m: dict, merged: dict) -> dict:
        SH = SV.sh()
        mdir, man = merged["dir"], merged["manifest"]
        out = self.work / "out" / m["read_name"]
        out.mkdir(parents=True, exist_ok=True)
        blk = {"read_name": m["read_name"], "kind": m["kind"], "adapter_sha256": m["adapter_sha256"],
               "merge_manifest_sha256": C.sha256_file(mdir / MD.MANIFEST), "merge_s": man.get("merge_s"), "started_s": round(self.clock() - self.t0, 1),
               "reads_started": False}
        s1 = SV.serving_mod("s1_pin")
        mp = SV.serving_mod("merge_parity")
        srv = self.h["server_cls"](mdir, log=lambda s: None, log_file=None)           # no server log is kept
        hashed = {}
        th = threading.Thread(target=lambda: hashed.update(problems=MD.verify_files(mdir, man)), daemon=True)
        try:
            th.start()
            srv.start()
            blk["boot_s"] = srv.wait_ready(float(self.plan.get("boot_timeout_s", 900)))
            info = srv.server_info()
            bad, warn = srv.check(info, self.pin)
            blk["args_problems"], blk["args_warnings"] = bad, warn
            if bad:
                raise SessionRefused("resolved server args refused: " + "; ".join(bad))
            th.join(timeout=600)
            if th.is_alive() or hashed.get("problems"):
                raise SessionRefused("merged checkpoint differs from its manifest")
            hs = s1.hashes(info, srv.env)
            blk["config_sha256"], blk["path_sha256"] = hs["config_sha256"], hs["path_sha256"]
            if self.path_sha is None:
                self.path_sha = hs["path_sha256"]
            elif hs["path_sha256"] != self.path_sha:
                raise SessionRefused("the served path differs from the first model's (path_sha256): not one serving path")
            blk["served"] = mp.served_identity(info, m["adapter_sha256"])
            blk["server_args"] = SH.args_subset(info)
            srv.flush()
            cmd = {"read_name": m["read_name"], "out_dir": str(out), "env_meta": {**self.env_meta, "server_args": blk["server_args"]},
                   "progress_every": 0,
                   "provenance": {"run_id": self.plan["run_id"], "kind": m["kind"], "adapter_sha256": m["adapter_sha256"],
                                  "merge_manifest_sha256": blk["merge_manifest_sha256"], "path_sha256": hs["path_sha256"],
                                  "config_sha256": hs["config_sha256"], "served_model_path": blk["served"]["served_model_path"], "look": "L1"}}
            blk["reads_started"] = True
            res = self.reader.run(cmd, timeout_s=float(self.plan.get("read_timeout_s", 1800)))
            if not res.get("ok"):
                raise SessionRefused("reader: " + str(res.get("error")))
            want = {MIXDEV_SPLIT: self.plan["mixdev"]["rows"], FINAL_SPLIT: self.plan["final"]["n_rows"]}
            bad = [s for s, n in want.items() if (res["sets"].get(s) or {}).get("rows") != n]
            if bad:
                raise SessionRefused(f"incomplete read of {bad}")
            blk["read"] = {s: {k: v for k, v in r.items() if k in ("rows", "sec", "input_tokens", "cached_tokens", "reads_per_sec")}
                           for s, r in res["sets"].items()}
            blk["stop"] = srv.stop()
            blk["ended_s"] = round(self.clock() - self.t0, 1)
            sets = {}
            for s in (MIXDEV_SPLIT, FINAL_SPLIT):
                f = out / f"preds_{s}" / f"{m['read_name']}.jsonl"
                sets[s] = [{"id": d["id"], "probs": d["probs"]} for d in (json.loads(l) for l in open(f) if l.strip())]
            blk["_sets"] = sets
            return blk
        except BaseException as e:  # noqa: BLE001
            blk["error"] = safe_err(e)
            if not blk["reads_started"]:
                blk["server_tail"] = list(getattr(srv, "tail", []))[-8:]
            self.log(f"MODEL {m['read_name']} FAILED: {blk['error']}")
            blk["stop"] = srv.stop()
            return blk
        finally:
            if srv.alive():
                srv.stop()
            shutil.rmtree(mdir, ignore_errors=True)

    # -- the job
    def run(self) -> dict:
        plan = self.plan
        reads, blocks = {}, {}
        try:
            info = self.setup()
        except BaseException as e:  # noqa: BLE001
            return self.finish({"ok": False, "errors": [{"step": "setup", "error": safe_err(e)}]}, reads, blocks)
        models = plan["models"]
        self.reader = self.h["reader"](self.reader_spec(), self.log)
        pool = ThreadPoolExecutor(max_workers=1)
        futs = {}
        try:
            futs[models[0]["read_name"]] = pool.submit(self.merge_job, models[0])
            ready = self.reader.wait_ready(float(plan.get("reader_ready_timeout_s", 900)))
            self.ev("reader_ready", **{k: v for k, v in (ready.get("info") or {}).items() if k in ("sets", "rows", "tokens", "init_s")})
            for i, m in enumerate(models):
                ok, why = self.gate(self.per_model_usd)
                if not ok:
                    self.errors.append({"step": m["read_name"], "error": why})
                    break
                try:
                    merged = (futs.pop(m["read_name"], None) or pool.submit(self.merge_job, m)).result()
                except BaseException as e:  # noqa: BLE001
                    self.errors.append({"step": m["read_name"], "error": "merge failed: " + safe_err(e)})
                    shutil.rmtree(self.work / "merged" / m["read_name"], ignore_errors=True)
                    continue
                if i + 1 < len(models) and self.gate(2 * self.per_model_usd)[0]:
                    futs[models[i + 1]["read_name"]] = pool.submit(self.merge_job, models[i + 1])
                self.ev("block_start", read_name=m["read_name"])
                blk = self.run_model(m, merged)
                sets = blk.pop("_sets", None)
                blocks[m["read_name"]] = blk
                if blk.get("error"):
                    self.errors.append({"step": m["read_name"], "error": blk["error"]})
                elif sets:
                    reads[m["read_name"]] = sets
                self.ev("block_end", read_name=m["read_name"], error=blk.get("error"))
        except BaseException as e:  # noqa: BLE001
            self.errors.append({"step": "job", "error": safe_err(e)})
        finally:
            pool.shutdown(wait=False, cancel_futures=True)
            try:
                self.reader.quit()
            except Exception:  # noqa: BLE001
                pass
        ok = not self.errors and all(m["read_name"] in reads for m in models)
        return self.finish({"ok": ok, "errors": self.errors, "env": self.env_meta}, reads, blocks)

    def finish(self, base: dict, reads: dict, blocks: dict) -> dict:
        res = {**base, "run_id": self.plan["run_id"], "mode": self.plan["mode"], "wall_s": round(self.clock() - self.t0, 1),
               "spent_usd": round(self.spent(), 3), "path_sha256": self.path_sha, "models": blocks, "reads": reads if base.get("ok") else {}}
        self.ev("session_done", ok=res["ok"])
        return res


C1_KEY, C2_KEY = "c1", "c2"
