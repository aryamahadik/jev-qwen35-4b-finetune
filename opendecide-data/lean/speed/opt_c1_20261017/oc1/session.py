"""oc1.session: the in-container orchestrator of the H100 session (runs in the SGLang image's python; stdlib + httpx).

  SglServer     starts / waits / inspects / stops ONE SGLang server for a Config (own process group; its GPU memory is
                confirmed free before the next boot; the resolved server args are checked against the config)
  run_runner    runs `python -m oc1.runner ...` under C1's pinned stack (/opt/fastpath/bin/python) and reads its result file
  Session       a list of config BLOCKS (boot -> measures -> specials -> stop), each gated by the running spend estimate:
                a block starts only if  prior + container elapsed x rate + block estimate  <=  STOP_LAUNCH (USD 4.50);
                above HARD_STOP (4.80) the loop ends at once. Every block's result is emitted (Queue + Volume) as it ends.

No Modal import here: the Modal function (modal_app.gpu_session) supplies `emit`, the e2e callback and the deadline, so
the whole thing runs on CPU in tests against a fake server.
"""
from __future__ import annotations

import json
import os
import signal
import subprocess
import sys
import threading
import time
from collections import deque
from pathlib import Path

from . import common as C
from . import configs as K


# ------------------------------------------------------------------ GPU helpers
def gpu_mem_used_mib() -> float | None:
    try:
        out = subprocess.run(["nvidia-smi", "--query-gpu=memory.used", "--format=csv,noheader,nounits"],
                             capture_output=True, text=True, timeout=10).stdout.strip().splitlines()[0]
        return float(out)
    except Exception:  # noqa: BLE001
        return None


def gpu_name() -> str | None:
    try:
        r = subprocess.run(["nvidia-smi", "--query-gpu=name,memory.total,driver_version", "--format=csv,noheader"],
                           capture_output=True, text=True, timeout=20)
        return r.stdout.strip() or None
    except Exception:  # noqa: BLE001
        return None


def wait_gpu_free(max_mib: float = 2500.0, timeout: float = 90.0) -> dict:
    t0 = time.time()
    while True:
        m = gpu_mem_used_mib()
        if m is None or m <= max_mib:
            return {"mem_mib": m, "waited_s": round(time.time() - t0, 1), "free": True}
        if time.time() - t0 > timeout:
            return {"mem_mib": m, "waited_s": round(time.time() - t0, 1), "free": False}
        time.sleep(1.0)


# ------------------------------------------------------------------ SGLang server
def want_args(cfg: K.Config, model_path) -> dict:
    """Resolved-arg expectations (SGLang /server_info) for a config. Mismatches on CRITICAL keys refuse the boot."""
    w = {"dtype": "bfloat16", "enable_fp32_lm_head": True, "speculative_algorithm": None, "model_path": str(model_path),
         "mamba_ssm_dtype": "float32", "context_length": K.CONTEXT_LEN, "sampling_defaults": "openai", "random_seed": 0,
         "max_running_requests": 64, "max_mamba_cache_size": 400, "version": C.SGLANG_VERSION,
         "quantization": None, "disable_radix_cache": False, "mamba_radix_cache_strategy": "extra_buffer",
         "linear_attn_backend": "triton", "linear_attn_prefill_backend": "triton"}
    cmd = cfg.cmd(model_path)
    for flag in ("--mamba-radix-cache-strategy", "--linear-attn-backend", "--linear-attn-prefill-backend"):
        if flag not in cmd:
            w.pop(flag[2:].replace("-", "_"), None)
    for i, a in enumerate(cmd):
        if a == "--quantization":
            w["quantization"] = cmd[i + 1]
        elif a == "--disable-radix-cache":
            w["disable_radix_cache"] = True
        elif a in ("--mamba-radix-cache-strategy", "--linear-attn-backend", "--linear-attn-prefill-backend"):
            w[a[2:].replace("-", "_")] = cmd[i + 1]
    return w


CRITICAL = ("dtype", "enable_fp32_lm_head", "quantization", "speculative_algorithm", "disable_radix_cache", "model_path",
            "mamba_ssm_dtype", "context_length", "sampling_defaults", "version", "mamba_radix_cache_strategy",
            "linear_attn_backend", "linear_attn_prefill_backend")


def norm(k, v):
    if k in ("quantization", "speculative_algorithm") and v in (None, "", "none", "None", False):
        return None
    if k == "model_path" and isinstance(v, str):
        return v.rstrip("/")
    return v


def check_args(resolved: dict, want: dict) -> tuple:
    problems, warnings = [], []
    for k, w in want.items():
        if k not in resolved:
            (problems if k in ("dtype", "quantization", "disable_radix_cache") else warnings).append(f"{k}: absent (wanted {w!r})")
            continue
        if norm(k, resolved[k]) != norm(k, w):
            (problems if k in CRITICAL else warnings).append(f"{k}: {resolved[k]!r} (wanted {w!r})")
    if resolved.get("enable_lora") or resolved.get("lora_paths"):
        problems.append("LoRA is enabled")
    return problems, warnings


KEEP_KEYS = ("model_path", "dtype", "quantization", "enable_fp32_lm_head", "context_length", "disable_radix_cache",
             "mamba_radix_cache_strategy", "mamba_ssm_dtype", "linear_attn_backend", "linear_attn_prefill_backend",
             "max_running_requests", "max_mamba_cache_size", "mem_fraction_static", "chunked_prefill_size",
             "max_prefill_tokens", "page_size", "attention_backend", "schedule_policy", "disable_overlap_schedule",
             "cuda_graph_config", "cuda_graph_backend_prefill", "cuda_graph_backend_decode", "disable_prefill_cuda_graph",
             "enable_multimodal", "version", "speculative_algorithm", "sampling_defaults", "random_seed", "radix_cache_backend")


class SglServer:
    def __init__(self, cfg: K.Config, model_path, python: str = sys.executable, port: int = K.PORT, log=print,
                 log_file=None, extra_env=None):
        self.cfg, self.model_path, self.python, self.port, self.log = cfg, str(model_path), python, port, log
        self.url = f"http://127.0.0.1:{port}"
        self.proc, self.tail = None, deque(maxlen=300)
        self.cmd = cfg.cmd(self.model_path, python, port)
        self.env = {**cfg.server_env(), **(extra_env or {})}
        self.log_file = log_file
        self._pump = None

    def start(self):
        self.log("SGLANG_CMD " + " ".join(self.cmd))
        self.proc = subprocess.Popen(self.cmd, env=self.env, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True,
                                     start_new_session=True)
        fh = open(self.log_file, "a") if self.log_file else None

        def pump():
            for line in self.proc.stdout:
                line = line.rstrip("\n")
                self.tail.append(line)
                if fh:
                    fh.write(line + "\n")
                    fh.flush()
        self._pump = threading.Thread(target=pump, daemon=True)
        self._pump.start()
        return self

    def wait_ready(self, timeout_s: float = 900.0) -> float:
        import httpx
        t0 = time.time()
        while True:
            if self.proc.poll() is not None:
                raise RuntimeError(f"SGLang exited ({self.proc.returncode}) during boot; last lines:\n" +
                                   "\n".join(list(self.tail)[-30:]))
            try:
                if httpx.get(self.url + "/health", timeout=5.0).status_code == 200:
                    return round(time.time() - t0, 1)
            except httpx.HTTPError:
                pass
            if time.time() - t0 > timeout_s:
                raise RuntimeError(f"SGLang not ready after {timeout_s} s; last lines:\n" + "\n".join(list(self.tail)[-15:]))
            time.sleep(2)

    def server_info(self) -> dict:
        import httpx
        for path in ("/server_info", "/get_server_info"):
            try:
                r = httpx.get(self.url + path, timeout=30.0)
                if r.status_code == 200:
                    return r.json()
            except httpx.HTTPError:
                continue
        raise RuntimeError("SGLang /server_info unavailable")

    def alive(self) -> bool:
        return self.proc is not None and self.proc.poll() is None

    def stop(self, grace: float = 30.0) -> dict:
        t0 = time.time()
        if self.proc is not None and self.proc.poll() is None:
            for sig, wait in ((signal.SIGTERM, grace), (signal.SIGKILL, 10.0)):
                try:
                    os.killpg(os.getpgid(self.proc.pid), sig)
                except (ProcessLookupError, PermissionError):
                    pass
                try:
                    self.proc.wait(timeout=wait)
                    break
                except subprocess.TimeoutExpired:
                    continue
        free = wait_gpu_free()
        return {"stop_s": round(time.time() - t0, 1), "gpu": free}


# ------------------------------------------------------------------ the runner (C1's pinned stack)
class Runner:
    """`python -m oc1.runner <cmd> --spec S --out O` as a child process (own process group). start() returns at once, wait()
    blocks for the result file (or an error record); kill() ends it."""

    def __init__(self, cmd: str, spec: dict, out_path: str, python: str = C.FASTPATH_PY, cwd: str | None = None,
                 env_extra: dict | None = None, log=print):
        self.cmd, self.spec, self.out_path, self.python, self.log = cmd, spec, str(out_path), python, log
        self.cwd, self.env_extra = cwd, env_extra or {}
        self.p, self.tail, self.t0, self._th = None, deque(maxlen=60), None, None

    def start(self):
        d = Path(self.out_path).parent
        d.mkdir(parents=True, exist_ok=True)
        spec_path = str(Path(self.out_path).with_suffix(".spec.json"))
        Path(spec_path).write_text(json.dumps(self.spec))
        env = {k: v for k, v in os.environ.items() if k not in ("PYTHONPATH", "VIRTUAL_ENV")}
        root = str(Path(C.HERE).parent)                   # the dir holding the oc1 package (/root in a container)
        env.update({"PYTHONPATH": root, "TOKENIZERS_PARALLELISM": "false", "HF_HUB_OFFLINE": "1", "PYTHONDONTWRITEBYTECODE": "1"})
        env.update(self.env_extra)
        self.t0 = time.time()
        self.p = subprocess.Popen([self.python, "-m", "oc1.runner", self.cmd, "--spec", spec_path, "--out", self.out_path],
                                  cwd=self.cwd or root, env=env, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True,
                                  start_new_session=True)

        def pump():
            for line in self.p.stdout:
                self.tail.append(line.rstrip("\n"))
                self.log("[runner:%s] %s" % (self.cmd, line.rstrip("\n")))
        self._th = threading.Thread(target=pump, daemon=True)
        self._th.start()
        return self

    def alive(self) -> bool:
        return self.p is not None and self.p.poll() is None

    def kill(self):
        if self.alive():
            try:
                os.killpg(os.getpgid(self.p.pid), signal.SIGKILL)
            except (ProcessLookupError, PermissionError):
                pass

    def wait(self, timeout_s: float) -> dict:
        err = None
        try:
            self.p.wait(timeout=timeout_s)
        except subprocess.TimeoutExpired:
            self.kill()
            err = f"runner timeout after {timeout_s:.0f} s"
        self._th.join(timeout=5)
        res = None
        try:
            res = json.loads(Path(self.out_path).read_text())
        except (OSError, ValueError):
            pass
        if res is None:
            res = {"error": err or f"no result file (rc {self.p.returncode})", "tail": list(self.tail)[-25:]}
        elif err:
            res["error"] = err
        res["runner_wall_s"] = round(time.time() - self.t0, 1)
        res["runner_rc"] = self.p.returncode
        return res


def run_runner(cmd: str, spec: dict, out_path: str, timeout_s: float, python: str = C.FASTPATH_PY, cwd: str | None = None,
               env_extra: dict | None = None, log=print) -> dict:
    """Blocking form: Runner(...).start().wait(timeout_s)."""
    return Runner(cmd, spec, out_path, python, cwd, env_extra, log).start().wait(timeout_s)


class Front:
    """The end-to-end HTTP front (oc1.front) as a child process, started EARLY so that its tokenizer / Readout build overlaps
    with the measurements; go() releases it (it then warms up, opens its port and writes ready_file)."""

    def __init__(self, session, cfg, srv, out_dir: Path, token: str, host_info=None):
        self.out_dir = Path(out_dir)
        self.go_file, self.ready_file, self.done_file = (self.out_dir / "front_go"), (self.out_dir / "front_ready.json"), (self.out_dir / "front_done.json")
        plan_e2e = session.plan.get("e2e", {})
        spec = {"sglang_url": srv.url, "c1_tokenizer_dir": session.c1_dir(), "port": session.plan.get("front_port", 8000), "host": "0.0.0.0",
                "seconds": plan_e2e.get("front_seconds", 700), "idle_s": 150, "wait_ms": 0.0, "shed_at": 10 ** 9,
                "ready_file": str(self.ready_file), "done_file": str(self.done_file), "go_file": str(self.go_file),
                "abort_file": str(self.out_dir / "front_abort"), "warm_requests": 6, "max_inflight": 256, "t0": session.t0,
                "host_info": host_info or {}}
        self.spec = spec
        self.runner = Runner("front", spec, str(self.out_dir / "front_out.json"), python=session.runner_python,
                             env_extra={"OC1_TOKEN": token}, log=session.log)

    def start(self):
        self.runner.start()
        return self

    def go(self, server_args=None):
        self.go_file.write_text("go")

    def wait_ready(self, timeout_s: float = 420.0) -> dict:
        t0 = time.time()
        while not self.ready_file.exists():
            if not self.runner.alive() or time.time() - t0 > timeout_s:
                return {"ok": False, "error": "front did not start", "tail": list(self.runner.tail)[-15:]}
            time.sleep(0.5)
        return json.loads(self.ready_file.read_text())

    def finish(self, timeout_s: float = 60.0) -> dict:
        done = {}
        try:
            self.runner.p.wait(timeout=timeout_s)
        except subprocess.TimeoutExpired:
            self.runner.kill()
        try:
            done = json.loads(self.done_file.read_text())
        except (OSError, ValueError):
            pass
        return {"front_done": done, "front_rc": self.runner.p.returncode, "tail": list(self.runner.tail)[-5:]}

    def abort(self):
        try:
            (self.out_dir / "front_abort").write_text("x")
        except OSError:
            pass
        self.runner.kill()


# ------------------------------------------------------------------ plan -> blocks
def block_estimate_s(cfg: K.Config, plan: dict | None = None) -> float:
    from . import plan as PL
    return PL.block_seconds(cfg, plan or {})


class Session:
    """Runs blocks until the plan ends or the budget gate says stop. `emit(event)` is called for every event."""

    def __init__(self, plan: dict, emit, models_root: str = "/out/models", work_dir: str = "/root/work",
                 results_root: str = "/out/results", rate_usd_h: float = 4.33, prior_usd: float = 0.0,
                 stop_launch: float = C.STOP_LAUNCH_USD, hard_stop: float = C.HARD_STOP_USD, clock=time.time,
                 python: str = sys.executable, e2e_cb=None, extra_cb=None, log=print, commit=lambda: None,
                 runner_python: str = C.FASTPATH_PY, front_token: str = "", host_info: dict | None = None):
        self.plan, self.emit, self.models_root, self.work_dir = plan, emit, models_root, work_dir
        self.results_root, self.rate, self.prior = results_root, rate_usd_h, prior_usd
        self.stop_launch, self.hard_stop, self.clock = stop_launch, hard_stop, clock
        self.python, self.e2e_cb, self.extra_cb, self.log, self.commit = python, e2e_cb, extra_cb, log, commit
        self.runner_python = runner_python
        self.front_token, self.host_info = front_token, host_info or {}
        self.t0 = clock()
        self.results = {}
        self.server = None

    # -- money
    def spent(self) -> float:
        return self.prior + C.container_cost_usd(self.clock() - self.t0, self.rate, overhead_s=C.CONTAINER_OVERHEAD_S)

    def block_cost(self, cfg: K.Config) -> float:
        return block_estimate_s(cfg, self.plan) / 3600.0 * self.rate

    def gate(self, cfg: K.Config) -> tuple:
        s, e = self.spent(), self.block_cost(cfg)
        if s >= self.hard_stop:
            return False, f"hard stop: spent ${s:.2f} >= ${self.hard_stop:.2f}"
        if s + e > self.stop_launch:
            return False, f"budget gate: spent ${s:.2f} + block estimate ${e:.2f} > stop-launch ${self.stop_launch:.2f}"
        return True, f"spent ${s:.2f} + block ${e:.2f} <= ${self.stop_launch:.2f}"

    # -- one block
    def model_dir(self, cfg: K.Config) -> str:
        name = {"merged": C.MERGED_NAME}.get(cfg.model, f"{C.MERGED_NAME}__{cfg.model}")
        return str(Path(self.models_root) / name)

    def run_block(self, cfg: K.Config) -> dict:
        ok, why = self.gate(cfg)
        if not ok:
            res = {"config": cfg.name, "skipped": why}
            self.emit({"event": "block_skipped", **res})
            return res
        mdir = self.model_dir(cfg)
        res = {"config": cfg.name, "desc": cfg.desc, "started_s": round(self.clock() - self.t0, 1), "gate": why}
        out_dir = Path(self.results_root) / cfg.name
        out_dir.mkdir(parents=True, exist_ok=True)
        try:
            Path(K.QUANT_REPORT).unlink()            # the online-quantization report of the PREVIOUS block must not leak in
        except OSError:
            pass
        srv = SglServer(cfg, mdir, self.python, log=self.log, log_file=str(out_dir / "sglang.log"))
        self.server = srv
        self.emit({"event": "block_start", "config": cfg.name, "spent_usd": round(self.spent(), 3), "cmd": " ".join(srv.cmd)})
        runner, front = None, None
        try:
            free = wait_gpu_free()
            res["gpu_before"] = free
            srv.start()
            ms = [m for m in cfg.measures if m in ("parity_full", "parity_sub", "latency", "throughput", "prefix", "score_readout")]
            go_file, abort_file = out_dir / "measure_go", out_dir / "measure_abort"
            for f in (go_file, abort_file):
                if f.exists():
                    f.unlink()
            if ms:        # tokenizer + Readout + workload preparation overlap with the SGLang boot
                spec = {"config": cfg.name, "sgl_url": srv.url, "work_dir": self.work_dir, "c1_dir": self.c1_dir(), "out_dir": str(out_dir),
                        "measures": ms, "params": self.plan.get("params", {}), "fp8": cfg.fp8, "go_file": str(go_file),
                        "abort_file": str(abort_file)}
                runner = Runner("measure", spec, str(out_dir / "measure.json"), python=self.runner_python, log=self.log).start()
                measure_timeout = min(float(self.plan.get("measure_timeout_s", 1500)), 2.0 * sum(
                    __import__("oc1.plan", fromlist=["x"]).PIECES.get(m, 60) for m in ms) + 150.0)
            res["boot_s"] = srv.wait_ready(float(self.plan.get("boot_timeout_s", 900)))
            info = srv.server_info()
            try:
                C.write_json(out_dir / "server_info.json", info)        # everything SGLang resolved (graph config, backends, ...)
            except Exception:  # noqa: BLE001
                pass
            res["server_args"] = {k: info.get(k) for k in KEEP_KEYS if k in info}
            bad, warn = check_args(info, want_args(cfg, mdir))
            res["args_warnings"], res["args_problems"] = warn, bad
            if bad:
                abort_file.write_text("refused")
                raise RuntimeError("resolved server args refused: " + "; ".join(bad))
            self.emit({"event": "booted", "config": cfg.name, "boot_s": res["boot_s"], "problems": bad, "warnings": warn[:5],
                       "server_args": res["server_args"]})
            go_file.write_text("go")
            if "e2e" in cfg.measures and self.e2e_cb is not None and self.plan.get("e2e", {}).get("enabled", True):
                front = Front(self, cfg, srv, out_dir, self.front_token, {**self.host_info, "config": cfg.name}).start()
            if runner is not None:
                res["measure"] = runner.wait(measure_timeout)
            if front is not None:
                ok2, why2 = self.gate_extra(float(self.plan.get("e2e", {}).get("est_s", 420)))
                if ok2:
                    front.go()
                    res["e2e"] = self.e2e_cb(cfg, srv, out_dir, front)
                else:
                    front.abort()
                    res["e2e"] = {"skipped": why2}
            for extra in ("vision", "voice_c1"):
                if extra in cfg.measures and self.extra_cb is not None and self.plan.get(extra, {}).get("enabled", True):
                    ok3, why3 = self.gate_extra(float(self.plan.get(extra, {}).get("est_s", 150)))
                    res[extra] = self.extra_cb(extra, cfg, srv, out_dir) if ok3 else {"skipped": why3}
        except BaseException as e:  # noqa: BLE001
            res["error"] = f"{type(e).__name__}: {str(e)[:600]}"
            res["server_tail"] = list(srv.tail)[-25:] if srv else None
            self.log(f"BLOCK {cfg.name} FAILED: {res['error']}")
        finally:
            if runner is not None and runner.alive():
                runner.kill()
            if front is not None:
                front.abort()
            res["stop"] = srv.stop()
            res["ended_s"] = round(self.clock() - self.t0, 1)
            res["spent_usd"] = round(self.spent(), 3)
            self.server = None
        self.results[cfg.name] = res
        C.write_json(out_dir / "block.json", res)
        self.commit()
        self.emit({"event": "block_end", "config": cfg.name, "spent_usd": res["spent_usd"], "error": res.get("error"),
                   "result": res})
        return res

    def gate_extra(self, est_s: float) -> tuple:
        s, e = self.spent(), est_s / 3600.0 * self.rate
        if s >= self.hard_stop or s + e > self.stop_launch:
            return False, f"budget gate: spent ${s:.2f} + extra ${e:.2f} > ${self.stop_launch:.2f}"
        return True, "ok"

    def c1_dir(self) -> str:
        return str(Path(self.models_root) / C.MERGED_NAME / "c1_tokenizer")

    # -- the plan
    def run(self) -> dict:
        names = self.plan.get("configs") or K.order()
        for name in names:
            cfg = K.CONFIGS[name]
            if self.spent() >= self.hard_stop:
                self.emit({"event": "hard_stop", "spent_usd": round(self.spent(), 3)})
                break
            self.run_block(cfg)
        return {"results": self.results, "spent_usd": round(self.spent(), 3), "wall_s": round(self.clock() - self.t0, 1)}
