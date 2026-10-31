"""grid_h100.servers: ONE SGLang 0.5.20 server per model on the frozen S1 command (hosting/sglang_host.server_cmd, fp8 False), its resolved
args checked before a single read counts, and the GPU confirmed free between models. Runs in the SGLang image's python (stdlib + httpx);
nothing here imports Modal.

The frozen S1 config (P7 serving freeze, c2_build/serving/S1_CONFIG_PIN.json) is the L4 production server; the H100 arm differs only in
settings OUTSIDE its parity-critical list (reads/README.md 1; the pin's `vm_defaults_vs_h100_s1`): max running requests 64 / mamba cache
400 (the S1 arm's own SERVER_DEFAULTS), the default attention backend and the default memory fraction, because the H100 is not the L4.
Every parity-critical argument is compared with the pin's after each boot (pin_problems) and the hash of the path-defining arguments
with the model path masked (s1_pin.hashes) must be one value over all 19 boots. `--mm-feature-transport` is an image-path flag and is not
used for text. No speculative flags, no LoRA, no quantization.
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

PIN_KEYS = ("dtype", "quantization", "enable_fp32_lm_head", "context_length", "disable_radix_cache", "mamba_radix_cache_strategy",
            "mamba_ssm_dtype", "linear_attn_backend", "linear_attn_prefill_backend", "sampling_defaults", "speculative_algorithm",
            "random_seed", "version")
ENV_PINS = {"SGLANG_RETURN_ORIGINAL_LOGPROB": "1", "HF_HUB_OFFLINE": "1", "TOKENIZERS_PARALLELISM": "false"}


def add_lean_paths() -> Path:
    for d in (C.LEAN, C.LEAN / "hosting"):
        if str(d) not in sys.path:
            sys.path.insert(0, str(d))
    return C.LEAN


def sh():
    add_lean_paths()
    import sglang_host
    return sglang_host


def serving_mod(name: str):
    """p7 serving tools (s1_pin, merge_parity, d9_latency, prompt_sha_check): /root/serving in the container, else c2_build/serving."""
    for d in (os.environ.get("P7_SERVING_DIR"), "/root/serving", str(C.LEAN / "c2_build" / "serving")):
        if d and (Path(d) / f"{name}.py").exists():
            if d not in sys.path:
                sys.path.insert(0, d)
            os.environ.setdefault("OD_LEAN", str(C.LEAN))
            return __import__(name)
    raise SystemExit(f"servers: serving tool {name}.py not found (set P7_SERVING_DIR)")


def load_pin(path=None) -> dict:
    for p in (path, os.environ.get("S1_PIN"), "/root/serving/S1_CONFIG_PIN.json", C.LEAN / "c2_build/serving/S1_CONFIG_PIN.json"):
        if p and Path(p).exists():
            return json.loads(Path(p).read_text())
    raise SystemExit("servers: S1_CONFIG_PIN.json not found")


def pin_problems(resolved: dict, pin: dict, env: dict | None = None) -> list:
    """Parity-critical arguments of a booted server vs the S1 pin (everything outside this list may differ on the H100)."""
    probs = []
    pa = pin.get("server_args") or {}
    for k in PIN_KEYS:
        a, b = resolved.get(k), pa.get(k)
        if k == "version":
            if a != b:
                probs.append(f"version {a!r} != pinned {b!r}")
            continue
        if sh()._norm_arg(k, a) != sh()._norm_arg(k, b):
            probs.append(f"{k}: {a!r} (pin {b!r})")
    if resolved.get("enable_lora") or resolved.get("lora_paths"):
        probs.append("LoRA is enabled")
    for k, v in ENV_PINS.items():
        if env is not None and env.get(k) != v:
            probs.append(f"env {k}={env.get(k)!r} (pinned {v!r})")
    return probs


def gpu_mem_used_mib() -> float | None:
    try:
        out = subprocess.run(["nvidia-smi", "--query-gpu=memory.used", "--format=csv,noheader,nounits"], capture_output=True,
                             text=True, timeout=10).stdout.strip().splitlines()[0]
        return float(out)
    except Exception:  # noqa: BLE001
        return None


def gpu_name() -> str | None:
    try:
        r = subprocess.run(["nvidia-smi", "--query-gpu=name,memory.total,driver_version", "--format=csv,noheader"], capture_output=True,
                           text=True, timeout=20)
        return r.stdout.strip() or None
    except Exception:  # noqa: BLE001
        return None


def wait_gpu_free(max_mib: float = 2500.0, timeout: float = 90.0, probe=gpu_mem_used_mib, sleep=time.sleep) -> dict:
    t0 = time.time()
    while True:
        m = probe()
        if m is None or m <= max_mib:
            return {"mem_mib": m, "waited_s": round(time.time() - t0, 1), "free": True}
        if time.time() - t0 > timeout:
            return {"mem_mib": m, "waited_s": round(time.time() - t0, 1), "free": False}
        sleep(1.0)


def torch_versions(python: str = sys.executable) -> dict:
    """torch / CUDA of the python that RUNS the server (the one that computes the logits), for the pred metas."""
    try:
        r = subprocess.run([python, "-c", "import json,torch;print(json.dumps({'torch':torch.__version__,'cuda':torch.version.cuda}))"],
                           capture_output=True, text=True, timeout=300)
        return json.loads(r.stdout.strip().splitlines()[-1])
    except Exception:  # noqa: BLE001
        return {"torch": None, "cuda": None}


class SglServer:
    def __init__(self, model_dir, python: str = sys.executable, port: int = C.PORT, log=print, log_file=None, server=None,
                 extra_env=None):
        SH = sh()
        self.model_dir, self.python, self.port, self.log = str(model_dir), python, port, log
        self.server = {**C.SERVER_ARGS, **(server or {})}
        self.url = f"http://127.0.0.1:{port}"
        self.cmd = SH.server_cmd(self.model_dir, fp8=False, port=port, max_running_requests=self.server["max_running_requests"],
                                 max_mamba_cache_size=self.server["max_mamba_cache_size"], python=python)
        self.env = {**SH.server_env(), "TRITON_CACHE_DIR": "/tmp/grid_triton", **(extra_env or {})}
        self.proc, self.tail, self.log_file = None, deque(maxlen=300), log_file
        self.resolved = None

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
        threading.Thread(target=pump, daemon=True).start()
        return self

    def alive(self) -> bool:
        return self.proc is not None and self.proc.poll() is None

    def _http(self, method: str, path: str, timeout: float = 30.0):
        import httpx
        return httpx.request(method, self.url + path, timeout=timeout)

    def wait_ready(self, timeout_s: float = 900.0) -> float:
        import httpx
        t0 = time.time()
        while True:
            if self.proc.poll() is not None:
                raise RuntimeError(f"SGLang exited ({self.proc.returncode}) during boot; last lines:\n" + "\n".join(list(self.tail)[-30:]))
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
                    self.resolved = r.json()
                    return self.resolved
            except httpx.HTTPError:
                continue
        raise RuntimeError("SGLang /server_info unavailable")

    def check(self, info: dict, pin: dict) -> tuple:
        """(problems, warnings): sglang_host.check_server_args for this arm + the S1 pin's parity-critical arguments + the env pins."""
        SH = sh()
        bad, warn = SH.check_server_args(info, SH.want_server_args(self.model_dir, False, self.server))
        bad = bad + pin_problems(info, pin, self.env)
        return bad, warn

    def flush(self, tries: int = 20) -> dict:
        import httpx
        last = None
        for i in range(tries):
            try:
                r = httpx.post(self.url + "/flush_cache", timeout=30.0)
                last = (r.status_code, r.text[:200])
                if r.status_code == 200:
                    return {"ok": True, "tries": i + 1}
            except httpx.HTTPError as e:
                last = str(e)[:200]
            time.sleep(0.5)
        raise RuntimeError(f"SGLang /flush_cache failed {tries} times: {last}")

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
        return {"stop_s": round(time.time() - t0, 1), "gpu": wait_gpu_free()}
