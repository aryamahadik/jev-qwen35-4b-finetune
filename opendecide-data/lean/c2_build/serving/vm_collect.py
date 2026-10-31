"""vm_collect.py: runs ON od-l4b (python3, stdlib only), READ-ONLY: GET /server_info and /get_model_info of the production
SGLang server, its argv and a few environment values from /proc, package versions, GPU, the sha256 of the code files on the
VM and of the merged checkpoint's manifest. It writes nothing but its stdout (one line, prefix P7JSON:). It never signals,
stops, restarts or flushes anything.
"""
import hashlib
import json
import os
import subprocess
import sys
import time
import urllib.request
from pathlib import Path

H = Path.home()
PORT = int(sys.argv[1]) if len(sys.argv) > 1 else 30000
ENV_WANT = ("SGLANG_RETURN_ORIGINAL_LOGPROB", "HF_HUB_OFFLINE", "TOKENIZERS_PARALLELISM", "TORCH_CUDA_ARCH_LIST", "CXX",
            "CUDA_HOME")
PKGS = ("sglang", "sglang_kernel", "torch", "transformers", "tokenizers", "flashinfer_python", "triton", "jinja2")


def sha(p):
    h = hashlib.sha256()
    with open(p, "rb") as f:
        for c in iter(lambda: f.read(1 << 20), b""):
            h.update(c)
    return h.hexdigest()


def get(path, timeout=30):
    return urllib.request.urlopen(f"http://127.0.0.1:{PORT}{path}", timeout=timeout).read().decode()


def versions(site):
    out = {}
    for d in Path(site).glob("*.dist-info"):
        name, _, ver = d.name[:-len(".dist-info")].rpartition("-")
        if name.replace("-", "_").lower() in PKGS:
            out[name.replace("-", "_").lower()] = ver
    return out


out = {"utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()), "port": PORT}
pid = int((H / "jobs/sglang.pid").read_text())
argv = open(f"/proc/{pid}/cmdline", "rb").read().split(b"\0")
out["pid"], out["argv"] = pid, [a.decode() for a in argv if a]
out["is_launch_server"] = any(b"sglang.launch_server" in a for a in argv)
env = {}
for kv in open(f"/proc/{pid}/environ", "rb").read().split(b"\0"):
    k, _, v = kv.decode(errors="replace").partition("=")
    if k in ENV_WANT:
        env[k] = v
out["env"] = env
out["etimes_s"] = int(subprocess.check_output(["ps", "-o", "etimes=", "-p", str(pid)]).decode().strip())
out["server_info_text"] = get("/server_info")
out["get_model_info_text"] = get("/get_model_info")
out["server_info_second_text"] = get("/server_info")
out["versions_sgl_venv"] = versions(H / "sgl/lib/python3.12/site-packages")
try:
    out["versions_client_venv_od"] = json.loads(subprocess.check_output(
        [str(H / "od/bin/python"), "-B", "-c",
         "import json,transformers,tokenizers,jinja2;print(json.dumps({'transformers':transformers.__version__,"
         "'tokenizers':tokenizers.__version__,'jinja2':jinja2.__version__}))"], stderr=subprocess.DEVNULL).decode())
except Exception as e:  # noqa: BLE001
    out["versions_client_venv_od"] = {"error": str(e)[:200]}
try:
    out["gpu"] = subprocess.check_output(["nvidia-smi", "--query-gpu=name,driver_version,memory.total,memory.used",
                                          "--format=csv,noheader"]).decode().strip()
except Exception as e:  # noqa: BLE001
    out["gpu"] = f"error: {e}"
code = {"lean": ["decoder_io.py", "od_gcp.py", "gate_dev.py", "train_decoder.py", "prism_x.py", "writeblock.py",
                 "shard_golden.py", "hosting/sglang_host.py", "hosting/fastcore/readout.py"],
        "reads": ["fast_read.py", "export_merged.py", "start_server.sh"]}
out["code_sha256"] = {f"{d}/{f}": sha(H / d / f) for d, fs in code.items() for f in fs if (H / d / f).exists()}
mp = Path(json.loads(out["get_model_info_text"])["model_path"])
out["model_path"] = str(mp)
out["merge_manifest_sha256"] = sha(mp / "merge_manifest.json") if (mp / "merge_manifest.json").exists() else None
out["merge_manifest"] = json.loads((mp / "merge_manifest.json").read_text()) if out["merge_manifest_sha256"] else None
print("P7JSON:" + json.dumps(out))
