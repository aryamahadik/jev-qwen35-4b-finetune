"""Decision Index 0.2 (github.com/apolinario/decision-index @19ad28e): an independent 40-benchmark suite for typed
decision engines, built by a third party, with Jev's score published. We never train on it (its rule and ours).
  build   : CPU job, rebuilds the frozen suite from pinned sources onto the Modal volume, then draws a stratified sample
  modal run modal_di.py::build --n 2400
  run     : GPU job, one engine over the sample (ours in-process, or decider-4b v2 through its own server), then the kit's
            own scorer; decider is also run on the 231 JevBench public items through JevBench's typesafe adapter
  modal run modal_di.py::run --label v10 --engine ours --adapter /vol/models/q35_4b_v10
  modal run modal_di.py::run --label decider4b --engine decider --jevbench
"""
import json
import subprocess
from pathlib import Path

import modal

HERE = Path(__file__).resolve().parent
KIT = "decision-index[rebuild] @ git+https://github.com/apolinario/decision-index@19ad28e"
app = modal.App("opendecide-di")
vol = modal.Volume.from_name("opendecide", create_if_missing=True)
SECRETS = [modal.Secret.from_name("opendecide-keys")]
cpu_image = (modal.Image.debian_slim(python_version="3.12").apt_install("git", "unzip")
             .pip_install(KIT).env({"HF_HUB_DISABLE_XET": "1", "HF_HOME": "/vol/hf"}))


from modal_od import image35  # noqa: E402  (torch 2.14 / transformers 5.17 / fla image)

gpu_image = (image35.pip_install(KIT, "decider-ai[serve]==1.2.2", "typesafe-sdk==0.7.1")
             .add_local_python_source("di_engine", "modal_od"))
DECIDER = {"DECIDER_MODEL": "Mapika/decider-4b", "DECIDER_REVISION": "7ab294cbdf6be6ac17fc818c10cdead744393d92"}


def _score(res_path, out_path):
    r = subprocess.run(["python", "-m", "decision_index", "score", "--results", res_path, "--suite-dir", "/vol/di/suite-0.2",
                        "--out", out_path], capture_output=True, text=True)
    return {"rc": r.returncode, "tail": (r.stdout[-3000:] + "\n" + r.stderr[-2000:])}


@app.function(image=gpu_image, gpu="H100", volumes={"/vol": vol}, secrets=SECRETS, timeout=3 * 3600)
def run_remote(label: str, engine: str, options: dict, rows: str, jevbench: bool = False) -> dict:
    import os
    import time
    os.environ["HF_HUB_DISABLE_XET"] = "1"
    out = f"/vol/di/runs/{label}"
    os.makedirs(out, exist_ok=True)
    log, server = {}, None
    if engine == "decider":
        from huggingface_hub import snapshot_download  # pin the exact weights JevBench measured (v2 revision)
        path = snapshot_download(DECIDER["DECIDER_MODEL"], revision=DECIDER["DECIDER_REVISION"], local_dir="/vol/models_ext/decider-4b-v2")
        env = {**os.environ, "DECIDER_MODEL": path}
        server = subprocess.Popen(["python", "-m", "uvicorn", "decider.serve:app", "--host", "127.0.0.1", "--port", "8000"],
                                  env=env, stdout=open(f"{out}/server.log", "w"), stderr=subprocess.STDOUT)
        import httpx
        for _ in range(360):
            try:
                if httpx.get("http://127.0.0.1:8000/health", timeout=2).status_code == 200:
                    break
            except Exception:
                pass
            time.sleep(5)
        spec, opts = "http", {"base_url": "http://127.0.0.1:8000", "model": options.get("model", "decider")}
    else:
        spec, opts = "di_engine:OpenDecideEngine", options
    cmd = ["python", "-m", "decision_index", "run", "--engine", spec, "--rows", rows, "--out", out, "--compact"]
    for k, v in opts.items():
        cmd += ["--option", f"{k}={v}"]
    t = time.time()
    r = subprocess.run(cmd, capture_output=True, text=True, cwd="/root")
    log["run_rc"], log["run_s"], log["run_tail"] = r.returncode, round(time.time() - t), (r.stdout[-3000:] + "\n" + r.stderr[-3000:])
    log["score"] = _score(f"{out}/results.jsonl", f"{out}/score.json")
    if jevbench and engine == "decider":
        r = subprocess.run(["python", "-m", "jevbench.cli", "run", "--tasks", "/root/jb_split/jevbench_all.jsonl", "--adapter", "typesafe",
                            "--endpoint", "http://127.0.0.1:8000", "--model", "decider", "--key-env", "HF_TOKEN",
                            "--results", f"{out}/jevbench_results.jsonl", "--ledger", f"{out}/jevbench_ledger.jsonl",
                            "--cap-usd", "100", "--price-in-per-m", "0.03", "--run-label", label],
                           capture_output=True, text=True, cwd="/root/jevbench_pkg", env={**os.environ, "PYTHONPATH": "/root/jevbench_pkg"})
        log["jevbench_rc"], log["jevbench_tail"] = r.returncode, (r.stdout[-2000:] + "\n" + r.stderr[-2000:])
    if server:
        server.terminate()
    vol.commit()
    files = {}
    for f in ("results.jsonl", "score.json", "jevbench_results.jsonl", "server.log"):
        pth = Path(out) / f
        if pth.exists():
            files[f] = pth.read_bytes()
    return {"log": log, "files": files}


@app.function(image=cpu_image, cpu=8, memory=32768, volumes={"/vol": vol}, secrets=SECRETS, timeout=4 * 3600)
def build_remote(n: int) -> dict:
    import os
    os.makedirs("/vol/di", exist_ok=True)
    os.chdir("/vol/di")
    log = {}
    rel = "work/artifacts/benchmark-suite/release-v2-rebuilt"
    if not Path(f"/vol/di/{rel}/added-rows.jsonl.gz").exists():
        r = subprocess.run(["python", "-m", "decision_index", "suite", "rebuild", "--work", "work"], capture_output=True, text=True)
        log["rebuild_rc"], log["rebuild_tail"] = r.returncode, (r.stdout[-3000:] + "\n" + r.stderr[-3000:])
        vol.commit()
    r = subprocess.run(["python", "-m", "decision_index", "suite", "import", "--dir", "/vol/di/suite-0.2",
                        "--rows", f"{rel}/selected-rows.jsonl.gz", "--added-rows", f"{rel}/added-rows.jsonl.gz"],
                       capture_output=True, text=True)
    log["import_rc"], log["import_tail"] = r.returncode, (r.stdout[-2000:] + "\n" + r.stderr[-2000:])
    r = subprocess.run(["python", "-m", "decision_index", "suite", "sample", "--dir", "/vol/di/suite-0.2", "--n", str(n),
                        "--out", f"/vol/di/sample-{n}.jsonl.gz"], capture_output=True, text=True)
    log["sample_rc"], log["sample_out"] = r.returncode, (r.stdout[-2000:] + "\n" + r.stderr[-2000:])
    vol.commit()
    p = Path(f"/vol/di/sample-{n}.jsonl.gz")
    log["sample_bytes"] = p.read_bytes() if p.exists() else None
    return log


@app.local_entrypoint()
def build(n: int = 2400):
    log = build_remote.remote(n)
    data = log.pop("sample_bytes")
    if data:
        (HERE / "data/di").mkdir(parents=True, exist_ok=True)
        (HERE / f"data/di/sample-{n}.jsonl.gz").write_bytes(data)
    (HERE / "logs/di_build.json").write_text(json.dumps(log, indent=1))
    print(json.dumps({k: (v if not isinstance(v, str) else v[-800:]) for k, v in log.items()}, indent=1))


@app.local_entrypoint()
def run(label: str, engine: str = "ours", adapter: str = "", base: str = "Qwen/Qwen3.5-4B", rows: str = "/vol/di/sample-2400.jsonl.gz",
        t_noul: float = 1.15, t_choice: float = 1.0, alpha: float = 1.0, jevbench: bool = False, gpu: str = "H100"):
    opts = {"base": base, "adapter": adapter, "t_noul": t_noul, "t_choice": t_choice, "alpha": alpha} if engine == "ours" else {}
    res = run_remote.with_options(gpu=gpu).remote(label, engine, opts, rows, jevbench)
    d = HERE / f"runs_di/{label}"
    d.mkdir(parents=True, exist_ok=True)
    for f, b in res["files"].items():
        (d / f).write_bytes(b)
    (d / "log.json").write_text(json.dumps(res["log"], indent=1))
    print(json.dumps({k: (v[-1500:] if isinstance(v, str) else v) for k, v in res["log"].items()}, indent=1)[-5000:])
