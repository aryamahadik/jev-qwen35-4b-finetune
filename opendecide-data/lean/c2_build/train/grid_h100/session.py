"""grid_h100.session: the in-container orchestrator of the grid reads (runs in the SGLang image's python; no Modal import, so the whole
flow runs on CPU in tests against fakes).

One container, one H100, in this order:
  0  GPU is an H100; SGLang is 0.5.20; the payer's Volume has the C2 run folder and C1's adapter (sha256 507d1c29...); data files == manifest
  1  base snapshot -> local disk (12 pins checked); C1 tokenizer files == the S1 pin's
  2  the 18 candidates rebuilt from the C2 checkpoints (gridbuild.rebuild) and held to GRID_RECORD.json (A42-D 9.6)
  3  the read client starts (reader.serve under /opt/fastpath): tokenizer, P7 prompt-sha check, every set tokenised once
  4  for each model in P6 order (C1 reference, final_a10, then the rest): merge (CPU, one model ahead of the server) -> boot on the frozen
     S1 command -> resolved args checked against the pin -> flush -> batch-1 latency + all sets -> stop -> outputs + DONE.json -> Volume commit
Every block starts only if  prior spend + this container's elapsed x rate + the block estimate  <=  STOP_LAUNCH (USD 3.60); above HARD_STOP the loop
ends. A model is complete only when DONE.json exists; a resumed job (same run id) skips complete models and re-runs the others.
"""
from __future__ import annotations

import json
import shutil
import subprocess
import sys
import threading
import time
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

from . import common as C
from . import gridbuild as GB
from . import hostops as HO
from . import merge_direct as MD
from . import servers as SV


class SessionRefused(SystemExit):
    pass


# ------------------------------------------------------------------ the read client as a child process
class ReaderProc:
    """`python -m grid_h100.reader serve` under C1's pinned stack; commands and results are files in ctl_dir."""

    def __init__(self, spec: dict, python: str = C.FASTPATH_PY, root: str = "/root", log=print):
        self.spec, self.python, self.root, self.log = spec, python, root, log
        self.ctl = Path(spec["ctl_dir"])
        self.p, self.tail = None, []
        self.k = 0

    def start(self):
        import os
        self.ctl.mkdir(parents=True, exist_ok=True)
        sp = self.ctl / "spec.json"
        sp.write_text(json.dumps(self.spec))
        env = {k: v for k, v in os.environ.items() if k not in ("PYTHONPATH", "VIRTUAL_ENV")}
        env.update({"PYTHONPATH": self.root, "TOKENIZERS_PARALLELISM": "false", "HF_HUB_OFFLINE": "1", "PYTHONDONTWRITEBYTECODE": "1",
                    "OD_LEAN": str(C.LEAN)})
        self.p = subprocess.Popen([self.python, "-m", "grid_h100.reader", "serve", "--spec", str(sp)], cwd=self.root, env=env,
                                  stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True, start_new_session=True)

        def pump():
            for line in self.p.stdout:
                self.tail.append(line.rstrip("\n"))
                self.tail = self.tail[-80:]
                self.log("[reader] " + line.rstrip("\n"))
        threading.Thread(target=pump, daemon=True).start()
        return self

    def alive(self) -> bool:
        return self.p is not None and self.p.poll() is None

    def wait_ready(self, timeout_s: float = 900.0) -> dict:
        t0 = time.time()
        f = self.ctl / "ready.json"
        while not f.exists():
            if not self.alive():
                raise SessionRefused("reader exited before it was ready:\n" + "\n".join(self.tail[-15:]))
            if time.time() - t0 > timeout_s:
                raise SessionRefused(f"reader not ready after {timeout_s} s")
            time.sleep(1.0)
        r = json.loads(f.read_text())
        if not r.get("ok"):
            raise SessionRefused("reader init failed: " + str(r.get("error")))
        return r

    def run(self, cmd: dict, timeout_s: float) -> dict:
        k = self.k
        self.k += 1
        C.write_json(self.ctl / f"cmd_{k}.json", cmd)
        t0 = time.time()
        f = self.ctl / f"res_{k}.json"
        while not f.exists():
            if not self.alive():
                return {"ok": False, "error": "reader exited:\n" + "\n".join(self.tail[-10:])}
            if time.time() - t0 > timeout_s:
                return {"ok": False, "error": f"reader timeout after {timeout_s:.0f} s"}
            time.sleep(1.0)
        return json.loads(f.read_text())

    def quit(self):
        try:
            (self.ctl / "quit").write_text("x")
            self.p.wait(timeout=20)
        except Exception:  # noqa: BLE001
            pass
        if self.alive():
            self.p.kill()


def real_hooks() -> dict:
    return {
        "gpu_name": SV.gpu_name, "torch_versions": SV.torch_versions, "sglang_version": HO.sglang_version,
        "prepare_base": HO.prepare_base, "prepare_c1_tok": HO.prepare_c1_tok,
        "merge": MD.merge_adapter, "crosscheck": MD.cross_check_export, "server_cls": SV.SglServer,
        "reader": lambda spec, log: ReaderProc(spec, log=log).start(),
        "load_pin": SV.load_pin,
    }


# ------------------------------------------------------------------ the session
def inputs_digest(plan: dict, grid_sha: str) -> str:
    return C.canon_sha({"grid": grid_sha, "manifest": plan["data_manifest"], "sets": plan["set_specs"], "server": C.SERVER_ARGS,
                        "run_id": plan.get("run_id")})


class GridSession:
    def __init__(self, plan: dict, emit=lambda ev: None, hooks: dict | None = None, clock=time.time, rate_usd_h: float = C.FN_RATE_USD_H,
                 prior_usd: float = 0.0, out_root="/out/runs", work_root="/tmp/grid_work", vol="/vol", data_dir="/root/data",
                 c1tok_dir="/root/c1tok", workload_dir="/root/workloads", commit=lambda: None, log=print,
                 stop_launch: float = C.STOP_LAUNCH_USD, hard_stop: float = C.HARD_STOP_USD):
        self.plan, self.emit, self.h = plan, emit, {**real_hooks(), **(hooks or {})}
        self.clock, self.rate, self.prior = clock, rate_usd_h, prior_usd
        self.out_root = Path(out_root) / plan["run_id"]
        self.work, self.vol = Path(work_root), Path(vol)
        self.data_dir, self.c1tok_dir, self.workload_dir = Path(data_dir), Path(c1tok_dir), Path(workload_dir)
        self.commit, self.log = commit, log
        self.stop_launch, self.hard_stop = stop_launch, hard_stop
        self.t0 = clock()
        self.results, self.errors, self.path_sha = {}, [], None
        self.per_model_usd = plan["estimate"]["scenarios"]["likely"]["per_model"]["total_s"] / 3600.0 * rate_usd_h

    # -- money
    def spent(self) -> float:
        return self.prior + C.container_cost_usd(self.clock() - self.t0, self.rate)

    def gate(self, extra_usd: float) -> tuple:
        s = self.spent()
        if s >= self.hard_stop:
            return False, f"hard stop: spent ${s:.2f} >= ${self.hard_stop:.2f}"
        if s + extra_usd > self.stop_launch:
            return False, f"budget gate: spent ${s:.2f} + estimate ${extra_usd:.2f} > stop-launch ${self.stop_launch:.2f}"
        return True, f"spent ${s:.2f} + ${extra_usd:.2f} <= ${self.stop_launch:.2f}"

    def ev(self, kind: str, **kw):
        self.emit({"event": kind, "t": round(self.clock() - self.t0, 1), "spent_usd": round(self.spent(), 3), **kw})

    # -- steps
    def setup(self) -> dict:
        h, plan = self.h, self.plan
        gpu = h["gpu_name"]()
        HO.check_gpu(gpu)
        ver = h["sglang_version"]()
        if ver != C.SGLANG_VERSION:
            raise SessionRefused(f"sglang {ver or '(import failed)'} != pinned {C.SGLANG_VERSION}")
        tv = h["torch_versions"]()
        self.pin = h["load_pin"]()
        self.env_meta = {"gpu": gpu.split(",")[0].strip(), "torch": tv["torch"], "cuda": tv["cuda"], "sglang_version": ver}
        self.ev("container_up", gpu_full=gpu, **self.env_meta)
        for rel, m in plan["data_manifest"].items():
            p = self.data_dir / rel
            if m.get("missing") or not p.exists() or C.sha256_file(p) != m["sha256"]:
                raise SessionRefused(f"data file {rel} is missing or differs from the plan's manifest")
        base = h["prepare_base"](str(self.vol / "hf"), str(self.work / "base"), self.log)
        self.base_dir = Path(base["base_dir"])
        self.c1_tok = h["prepare_c1_tok"](self.c1tok_dir, (self.pin.get("model") or {}).get("tokenizer_pins") or {})
        self.ev("base_ready", **{k: base[k] for k in ("source", "fetched")})
        # the grid
        c1_dir = GB.locate_c1_adapter()
        run_dir = Path(plan["c2_run_dir"])
        ri = GB.check_run_dir(run_dir, (self.pin.get("model") or {}).get("tokenizer_pins") or {})
        if ri["problems"]:
            raise SessionRefused("the C2 run folder is not usable: " + "; ".join(ri["problems"]))
        grid_dir = self.work / "grid"
        if plan.get("grid_source", "rebuild") == "volume":
            grid = GB.load_existing(self.vol / "models" / "q35_4b_c2_grid", plan["grid_record"])
            grid_dir = self.vol / "models" / "q35_4b_c2_grid"
        else:
            grid = GB.rebuild(c1_dir, run_dir, grid_dir, plan["grid_record"])
        self.c1_dir, self.grid, self.grid_dir, self.run_info = c1_dir, grid, grid_dir, ri
        self.adapters = {m["cand"]: grid_dir / m["cand"] for m in plan["models"] if m["kind"] == "cand"}
        for m in plan["models"]:
            if m["kind"] == "cand":
                want = next(c["adapter_sha256"] for c in grid["candidates"] if c["name"] == m["cand"])
                m["adapter_sha256"] = want
        self.digest = inputs_digest(plan, grid["grid_sha256"])
        self.ev("grid_ready", grid_sha256=grid["grid_sha256"], worst_verify_err=grid.get("worst_verify_err"),
                c1_adapter=str(c1_dir), run=ri.get("steps"))
        return {"gpu": gpu, **self.env_meta, "grid_sha256": grid["grid_sha256"], "run_folder": ri, "base": base}

    def adapter_dir(self, m: dict) -> Path:
        return self.c1_dir if m["kind"] == "ref" else self.adapters[m["cand"]]

    def model_out(self, m) -> Path:
        return self.out_root / "models" / m["read_name"]

    def is_done(self, m) -> bool:
        f = self.model_out(m) / "DONE.json"
        if not f.exists():
            return False
        try:
            d = json.loads(f.read_text())
        except ValueError:
            return False
        return d.get("inputs_digest") == self.digest and d.get("adapter_sha256") == m["adapter_sha256"]

    def start_reader(self):
        plan = self.plan
        spec = {"c1_dir": str(self.c1_tok), "data_dir": str(self.data_dir), "sets": plan["set_specs"], "manifest": plan["data_manifest"],
                "recorded_check": plan["prompt_check_record"], "ctl_dir": str(self.work / "reader_ctl"), "port": C.PORT}
        self.reader = self.h["reader"](spec, self.log)
        return self.reader

    def merge_job(self, m) -> dict:
        mdir = self.work / "merged" / m["read_name"]
        if mdir.exists():
            shutil.rmtree(mdir)
        man = self.h["merge"](str(self.base_dir), str(self.adapter_dir(m)), str(mdir), str(self.c1_tok), label=m["read_name"],
                              dev="cpu", expect_adapter_sha=m["adapter_sha256"], log=self.log)
        return {"dir": mdir, "manifest": man}

    def run_model(self, m: dict, merged: dict) -> dict:
        SH = SV.sh()
        mdir, man = merged["dir"], merged["manifest"]
        out = self.model_out(m)
        out.mkdir(parents=True, exist_ok=True)
        blk = {"read_name": m["read_name"], "kind": m["kind"], "cand": m["cand"], "adapter_sha256": m["adapter_sha256"],
               "merge_manifest_sha256": C.sha256_file(mdir / MD.MANIFEST), "merge_s": man.get("merge_s"),
               "merge_checks": man.get("checks"), "started_s": round(self.clock() - self.t0, 1)}
        s1 = SV.serving_mod("s1_pin")
        mp = SV.serving_mod("merge_parity")
        srv = self.h["server_cls"](mdir, log=self.log, log_file=str(out / "sglang.log"))
        hashed, xc, xth = {}, {}, None
        th = threading.Thread(target=lambda: hashed.update(problems=MD.verify_files(mdir, man)), daemon=True)
        if m["kind"] == "ref":         # C1 merged here == the production export on the Volume? (report only; the parity bar is what binds)
            exp = self.vol / "models" / (C.C1_NAME + "_merged")
            if (exp / MD.MANIFEST).exists():
                xth = threading.Thread(target=lambda: xc.update(self.h["crosscheck"](str(mdir), str(exp))), daemon=True)
            else:
                blk["c1_vs_export"] = {"compared": 0, "note": "no exported C1 merged checkpoint on the Volume"}
        try:
            th.start()
            if xth:
                xth.start()
            srv.start()
            blk["boot_s"] = srv.wait_ready(float(self.plan.get("boot_timeout_s", 900)))
            info = srv.server_info()
            bad, warn = srv.check(info, self.pin)
            blk["args_problems"], blk["args_warnings"] = bad, warn
            if bad:
                raise RuntimeError("resolved server args refused: " + "; ".join(bad))
            th.join(timeout=600)
            if th.is_alive() or hashed.get("problems"):
                raise RuntimeError(f"merged checkpoint differs from its manifest: {hashed.get('problems') or 'timeout'}")
            hs = s1.hashes(info, srv.env)
            blk["config_sha256"], blk["path_sha256"] = hs["config_sha256"], hs["path_sha256"]
            if self.path_sha is None:
                self.path_sha = hs["path_sha256"]
            elif hs["path_sha256"] != self.path_sha:
                raise RuntimeError("the served path differs from the first model's (path_sha256): not one serving path")
            ident = mp.served_identity(info, m["adapter_sha256"])
            blk["served"] = ident
            srv_args = SH.args_subset(info)
            blk["server_args"] = srv_args
            srv.flush()
            label = "C1" if m["kind"] == "ref" else m["cand"]
            lc = self.plan["latency"]
            cmd = {"read_name": m["read_name"], "out_dir": str(out), "env_meta": {**self.env_meta, "server_args": srv_args},
                   "progress_every": 0,
                   "provenance": {"run_id": self.plan["run_id"], "kind": m["kind"], "cand": m["cand"], "adapter_sha256": m["adapter_sha256"],
                                  "grid_sha256": self.grid["grid_sha256"], "merge_manifest_sha256": blk["merge_manifest_sha256"],
                                  "path_sha256": hs["path_sha256"], "config_sha256": hs["config_sha256"],
                                  "served_model_path": ident["served_model_path"], "inputs_digest": self.digest},
                   "latency": {"label": label, "n": lc["n"], "warmup": lc["warmup"], "workload": lc["workload"], "seed": lc.get("seed", 0),
                               "workload_dir": str(self.workload_dir),
                               "meta": {"gpu": self.env_meta["gpu"], "adapter_sha256": m["adapter_sha256"], **ident, **hs,
                                        "server_version": info.get("version")}}}
            res = self.reader.run(cmd, timeout_s=float(self.plan.get("read_timeout_s", 1800)))
            if not res.get("ok"):
                raise RuntimeError("reader: " + str(res.get("error")))
            if xth:
                xth.join(timeout=300)
                blk["c1_vs_export"] = dict(xc) if xc else {"error": "cross-check did not finish in 300 s"}
            blk["read"] = {k: v for k, v in res.items() if k != "latency"}
            blk["latency"] = res.get("latency")
            self.check_complete(res)
            blk["ended_s"] = round(self.clock() - self.t0, 1)
            blk["stop"] = srv.stop()
            files = {str(p.relative_to(out)): C.sha256_file(p) for p in sorted(out.rglob("preds_*/*")) if p.is_file()}
            C.write_json(out / "block.json", blk)
            C.write_json(out / "DONE.json", {"read_name": m["read_name"], "adapter_sha256": m["adapter_sha256"],
                                             "inputs_digest": self.digest, "files": files, "path_sha256": hs["path_sha256"],
                                             "latency_p50_ms": (res.get("latency") or {}).get("p50_ms"), "done_utc": C.utc()})
            return blk
        except BaseException as e:  # noqa: BLE001
            blk["error"] = f"{type(e).__name__}: {str(e)[:700]}"
            blk["server_tail"] = list(srv.tail)[-25:]
            self.log(f"MODEL {m['read_name']} FAILED: {blk['error']}")
            blk["stop"] = srv.stop()
            C.write_json(out / "block.json", blk)
            return blk
        finally:
            if srv.alive():
                srv.stop()
            shutil.rmtree(mdir, ignore_errors=True)

    def check_complete(self, res: dict) -> None:
        """Every set of the plan was read, with the manifest's row count (a short or missing set is a failed model, never a pass)."""
        bad = []
        for s in self.plan["set_specs"]:
            n = res["sets"].get(s["split"] + s["tag"], {}).get("rows")
            want = self.plan["data_manifest"][s["file"]]["rows"]
            if n != want:
                bad.append(f"{s['split']}{s['tag']}: {n} rows, manifest {want}")
        if bad:
            raise RuntimeError("incomplete read: " + "; ".join(bad[:5]))

    # -- the loop
    def run(self) -> dict:
        plan = self.plan
        C.write_json(self.out_root / "plan.json", {k: v for k, v in plan.items() if k not in ("grid_record", "prompt_check_record")})
        info = self.setup()
        C.write_json(self.out_root / "setup.json", info)
        models = plan["models"]
        todo = [m for m in models if not self.is_done(m)]
        for m in models:
            if m not in todo:
                self.results[m["read_name"]] = {"skipped": "DONE.json present (resumed run)"}
                self.ev("block_skipped", read_name=m["read_name"], why="done")
        if not todo:
            return self.finish()
        self.start_reader()
        pool = ThreadPoolExecutor(max_workers=1)
        futs = {}
        try:
            futs[todo[0]["read_name"]] = pool.submit(self.merge_job, todo[0])
            ready = self.reader.wait_ready(float(plan.get("reader_ready_timeout_s", 900))) if hasattr(self.reader, "wait_ready") else None
            self.ev("reader_ready", **((ready or {}).get("info") or {}))
            for i, m in enumerate(todo):
                ok, why = self.gate(self.per_model_usd)
                if not ok:
                    self.ev("block_skipped", read_name=m["read_name"], why=why)
                    for r in todo[i:]:
                        self.results[r["read_name"]] = {"skipped": why}
                    break
                try:
                    fut = futs.pop(m["read_name"], None) or pool.submit(self.merge_job, m)
                    merged = fut.result()
                except BaseException as e:  # noqa: BLE001 - a failed merge is this model's error; the job goes on
                    err = f"merge failed: {type(e).__name__}: {str(e)[:600]}"
                    self.results[m["read_name"]] = {"error": err}
                    self.errors.append({"read_name": m["read_name"], "error": err})
                    self.log(f"MODEL {m['read_name']} FAILED: {err}")
                    shutil.rmtree(self.work / "merged" / m["read_name"], ignore_errors=True)
                    self.ev("block_end", read_name=m["read_name"], error=err)
                    continue
                if i + 1 < len(todo) and self.gate(2 * self.per_model_usd)[0]:     # merge one model ahead (CPU, hidden behind the reads)
                    futs[todo[i + 1]["read_name"]] = pool.submit(self.merge_job, todo[i + 1])
                self.ev("block_start", read_name=m["read_name"])
                blk = self.run_model(m, merged)
                self.results[m["read_name"]] = blk
                if blk.get("error"):
                    self.errors.append({"read_name": m["read_name"], "error": blk["error"]})
                self.commit()
                self.ev("block_end", read_name=m["read_name"], error=blk.get("error"), latency_p50_ms=(blk.get("latency") or {}).get("p50_ms"))
                if i + 1 < len(todo) and todo[i + 1]["read_name"] not in futs and self.gate(self.per_model_usd)[0]:
                    futs[todo[i + 1]["read_name"]] = pool.submit(self.merge_job, todo[i + 1])
        finally:
            pool.shutdown(wait=False, cancel_futures=True)
            try:
                self.reader.quit()
            except Exception:  # noqa: BLE001
                pass
        return self.finish()

    def finish(self) -> dict:
        done = [m["read_name"] for m in self.plan["models"] if self.is_done(m)]
        res = {"run_id": self.plan["run_id"], "wall_s": round(self.clock() - self.t0, 1), "spent_usd": round(self.spent(), 3),
               "models_done": done, "models_total": len(self.plan["models"]), "complete": len(done) == len(self.plan["models"]),
               "errors": self.errors, "path_sha256": self.path_sha,
               "blocks": {k: {kk: v.get(kk) for kk in ("boot_s", "error", "skipped", "path_sha256")} for k, v in self.results.items()}}
        C.write_json(self.out_root / "session_result.json", res)
        self.commit()
        self.ev("session_done", complete=res["complete"], done=len(done))
        return res
