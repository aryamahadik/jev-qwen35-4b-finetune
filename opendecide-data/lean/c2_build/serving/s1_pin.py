"""s1_pin: pin and verify the S1 serving configuration of od-l4b (C2 lane P7). CPU + read-only VM access.

What "the S1 config" is: the production C1 server of od-l4b (port 30000) = arm S1 of A35 / SPEED-2 (SGLang 0.5.20, merged BF16
checkpoint, fp32 LM head, hybrid prefix cache `extra_buffer`, triton linear-attention backends, no speculation, sampling
defaults pinned) as started by reads/start_server.sh --max-running 32 --max-mamba 128 --mem-fraction 0.8 --extra-args
"--attention-backend triton". Three hashes are pinned (all over canonical JSON, sort_keys):
  config_sha256         the parity-critical resolved server args (hosting/sglang_host.SERVER_ARGS_KEYS incl. model_path and
                        the graph keys), the server environment, the sampling and logprob mode, the context length, the
                        readout (layout / style / views / temps);
  path_sha256           the same with model_path masked: what two models served on the SAME path share (D9, parity);
  server_info_stable_sha256   every key of GET /server_info except the per-boot ones (internal_states, startup_time).
A candidate (C2) served for parity / D9 must have path_sha256 == the pin's (verify --mode path); the production C1 server must
still have config_sha256 == the pin's (verify --mode same).

  s1_pin.py collect [--out DIR]           read-only: run vm_collect.py on od-l4b -> DIR/vm_facts.json (+ vm_server_info.json)
  s1_pin.py pin     [--facts DIR] [--out S1_CONFIG_PIN.json]   build the pin record from collected facts (offline)
  s1_pin.py verify  [--mode same|path] [--pin ...] (--info FILE | --vm)  compare a server_info with the pin; exit 1 on drift

Nothing here writes to the VM except /tmp/p7_* files; it never stops, restarts, flushes or signals a server.
"""
from __future__ import annotations

import argparse
import json
import sys
import time
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import p7_common as C  # noqa: E402

PIN_PATH = HERE / "S1_CONFIG_PIN.json"
FACTS_DIR = C.BUILD / "staged/P7"
PER_BOOT_KEYS = ("internal_states", "startup_time")
MODEL_KEYS = ("model_path", "tokenizer_path", "served_model_name")
ENV_PINS = {"SGLANG_RETURN_ORIGINAL_LOGPROB": "1", "HF_HUB_OFFLINE": "1", "TOKENIZERS_PARALLELISM": "false"}
# Settings of the VM path that differ from the Modal H100 S1 arm but are outside the parity-critical list (reads/README.md 1).
VM_DEFAULTS = {"attention_backend": "triton", "mem_fraction_static": 0.8, "max_running_requests": 32, "max_mamba_cache_size": 128}
READOUT = {"api": "v1", "layout": C.LAYOUT, "style": C.STYLE, "choice": "2view_prob_avg (given + exact reversal)",
           "noul": "single read", "temps": {"noul": 1.0, "choice": 1.0}, "max_len": 16384}


def sh_mod():
    C.add_paths()
    import sglang_host
    return sglang_host


def stable_info(info: dict) -> dict:
    return {k: v for k, v in info.items() if k not in PER_BOOT_KEYS}


def config_view(info: dict, env: dict | None = None, mask_model: bool = False) -> dict:
    SH = sh_mod()
    args = SH.args_subset(info)
    graphs = SH.graphs_info(info)["cuda_graph"]
    if mask_model:
        args = {k: ("<model>" if k in MODEL_KEYS else v) for k, v in args.items()}
    return {"server_args": args, "graphs": graphs, "sampling": SH.SAMPLING, "logprobs": SH.LOGPROB_MODE,
            "context_len": SH.CONTEXT_LEN, "readout": READOUT, "env": {k: (env or {}).get(k) for k in ENV_PINS},
            "extra": {k: info.get(k) for k in ("attention_backend", "chunked_prefill_size", "page_size", "mem_fraction_static",
                                               "max_prefill_tokens", "schedule_policy", "cuda_graph_config")}}


def hashes(info: dict, env: dict | None = None) -> dict:
    stab = stable_info(info)
    masked = {k: ("<model>" if k in MODEL_KEYS else v) for k, v in stab.items()}
    return {"config_sha256": C.canon_sha(config_view(info, env)),
            "path_sha256": C.canon_sha(config_view(info, env, mask_model=True)),
            "server_info_stable_sha256": C.canon_sha(stab),
            "server_info_stable_masked_sha256": C.canon_sha(masked)}


def arg_problems(info: dict, env: dict | None = None) -> tuple[list, list]:
    """sglang_host.check_server_args against the S1 requirements (with the VM's max-running / mamba sizes), plus the
    environment pins. (problems, warnings)."""
    SH = sh_mod()
    want = SH.want_server_args(info.get("model_path"), False, {"max_running_requests": VM_DEFAULTS["max_running_requests"],
                                                                "max_mamba_cache_size": VM_DEFAULTS["max_mamba_cache_size"]})
    problems, warnings = SH.check_server_args(info, want)
    for k, v in VM_DEFAULTS.items():
        if info.get(k) != v:
            problems.append(f"{k}: {info.get(k)!r} (VM production setting {v!r})")
    if env is not None:
        for k, v in ENV_PINS.items():
            if env.get(k) != v:
                problems.append(f"env {k}={env.get(k)!r} (pinned {v!r})")
    return problems, warnings


# ---- collect (read-only VM access) -------------------------------------------------------------------------------------
def collect(out_dir: Path = FACTS_DIR, vm: C.Vm | None = None) -> dict:
    vm = vm or C.Vm()
    out_dir.mkdir(parents=True, exist_ok=True)
    vm.put(HERE / "vm_collect.py", "od-l4b:/tmp/p7_collect.py")
    vm.ssh(f"python3 /tmp/p7_collect.py {C.PROD_PORT} > /tmp/p7_collect_out.json")
    tmp = out_dir / "vm_collect_out.json"
    vm.get("od-l4b:/tmp/p7_collect_out.json", tmp)
    line = tmp.read_text().strip()
    if not line.startswith("P7JSON:"):
        raise RuntimeError("vm_collect output has no P7JSON line")
    facts = json.loads(line[len("P7JSON:"):])
    tmp.unlink()
    (out_dir / "vm_server_info.json").write_text(facts["server_info_text"])
    (out_dir / "vm_server_info_second.json").write_text(facts["server_info_second_text"])
    (out_dir / "vm_get_model_info.json").write_text(facts["get_model_info_text"])
    slim = {k: v for k, v in facts.items() if k not in ("server_info_text", "server_info_second_text", "get_model_info_text")}
    (out_dir / "vm_facts.json").write_text(json.dumps(slim, indent=1, sort_keys=True) + "\n")
    return slim


# ---- pin ---------------------------------------------------------------------------------------------------------------
def build_pin(facts: dict, info: dict, info2: dict | None = None, mac_code: dict | None = None) -> dict:
    SH = sh_mod()
    env = facts.get("env") or {}
    problems, warnings = arg_problems(info, env)
    h = hashes(info, env)
    pin = {
        "pin_record": 1, "lane": "P7-serving-freeze", "utc": facts.get("utc") or time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "what": "S1 serving configuration of the production C1 server on od-l4b (read-only GET /server_info; server untouched)",
        "host": {"vm": "od-l4b", "zone": "us-east4-c", "port": facts.get("port"), "server_pid": facts.get("pid"),
                 "server_age_s_at_read": facts.get("etimes_s"), "gpu": facts.get("gpu")},
        **h,
        "stable_hash_repeats": None if info2 is None else C.canon_sha(stable_info(info2)) == h["server_info_stable_sha256"],
        "checks": {"problems": problems, "warnings": warnings, "ok": not problems,
                   "sglang_version": info.get("version"), "pinned_sglang_version": SH.SGLANG_VERSION},
        "argv": facts.get("argv"), "env": facts.get("env"),
        "server_args": SH.args_subset(info), "graphs": SH.graphs_info(info)["cuda_graph"],
        "vm_defaults_vs_h100_s1": {"vm": VM_DEFAULTS, "note": "outside the parity-critical list; reads/README.md section 1. "
                                   "The A49 (f) parity test (99.90%) is what binds the VM path."},
        "readout": READOUT, "env_pins": ENV_PINS, "sampling": SH.SAMPLING, "logprobs": SH.LOGPROB_MODE, "context_len": SH.CONTEXT_LEN,
        "model": {"path": facts.get("model_path"), "merge_manifest_sha256": facts.get("merge_manifest_sha256"),
                  "adapter_sha256": (facts.get("merge_manifest") or {}).get("adapter_sha256"),
                  "is_c1": (facts.get("merge_manifest") or {}).get("adapter_sha256") == C.C1_ADAPTER_SHA256,
                  "base": (facts.get("merge_manifest") or {}).get("base"),
                  "revision": (facts.get("merge_manifest") or {}).get("revision"),
                  "layout": (facts.get("merge_manifest") or {}).get("layout"),
                  "tokenizer_pins": (facts.get("merge_manifest") or {}).get("c1_tokenizer")},
        "versions": {"sgl_venv": facts.get("versions_sgl_venv"), "client_venv_od": facts.get("versions_client_venv_od")},
        "code_sha256": {"vm": facts.get("code_sha256"), "mac": mac_code},
        "code_differs_vm_vs_mac": None if not (facts.get("code_sha256") and mac_code) else sorted(
            k for k, v in facts["code_sha256"].items() if k in mac_code and mac_code[k] != v),
        "how_to_use": ["a candidate server must satisfy `s1_pin.py verify --mode path` before its parity / D9 numbers count",
                       "the production server must still satisfy `s1_pin.py verify --mode same` after any window"],
    }
    pin["pin_sha256"] = C.canon_sha({k: pin[k] for k in ("config_sha256", "path_sha256", "server_info_stable_sha256")})
    return pin


def mac_code_shas(lean: Path) -> dict:
    mp = {"lean/decoder_io.py": "decoder_io.py", "lean/od_gcp.py": "od_gcp.py", "lean/gate_dev.py": "gate_dev.py",
          "lean/train_decoder.py": "train_decoder.py", "lean/prism_x.py": "prism_x.py", "lean/writeblock.py": "writeblock.py",
          "lean/shard_golden.py": "shard_golden.py", "lean/hosting/sglang_host.py": "hosting/sglang_host.py",
          "lean/hosting/fastcore/readout.py": "hosting/fastcore/readout.py", "reads/fast_read.py": "c2_build/reads/fast_read.py",
          "reads/export_merged.py": "c2_build/reads/export_merged.py", "reads/start_server.sh": "c2_build/reads/vm_scripts/start_server.sh"}
    return {k: C.sha256_file(lean / v) for k, v in mp.items() if (lean / v).exists()}


def verify(info: dict, pin: dict, mode: str = "same", env: dict | None = None) -> dict:
    """Problems (empty = identical on the chosen scope). mode same: config_sha256 (incl. model_path); path: path_sha256."""
    h = hashes(info, env if env is not None else pin.get("env"))
    key = "config_sha256" if mode == "same" else "path_sha256"
    problems, warnings = arg_problems(info, env if env is not None else pin.get("env"))
    if h[key] != pin[key]:
        pa, ia = pin["server_args"], sh_mod().args_subset(info)
        diff = {k: (pa.get(k), ia.get(k)) for k in sorted(set(pa) | set(ia)) if pa.get(k) != ia.get(k)
                and not (mode == "path" and k in MODEL_KEYS)}
        problems.append(f"{key} {h[key][:16]} != pinned {pin[key][:16]}; differing server args: {diff or 'none (other keys)'}")
    return {"mode": mode, "ok": not problems, "problems": problems, "warnings": warnings, **h}


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)
    c = sub.add_parser("collect")
    c.add_argument("--out", default=str(FACTS_DIR))
    p = sub.add_parser("pin")
    p.add_argument("--facts", default=str(FACTS_DIR))
    p.add_argument("--out", default=str(PIN_PATH))
    v = sub.add_parser("verify")
    v.add_argument("--mode", choices=("same", "path"), default="same")
    v.add_argument("--pin", default=str(PIN_PATH))
    v.add_argument("--info", default="")
    v.add_argument("--vm", action="store_true", help="read /server_info of the VM's production port (GET only)")
    a = ap.parse_args(argv)
    if a.cmd == "collect":
        facts = collect(Path(a.out))
        print(json.dumps({k: facts[k] for k in ("utc", "pid", "etimes_s", "model_path", "merge_manifest_sha256")}))
        return 0
    if a.cmd == "pin":
        d = Path(a.facts)
        facts = json.loads((d / "vm_facts.json").read_text())
        info = json.loads((d / "vm_server_info.json").read_text())
        info2 = json.loads((d / "vm_server_info_second.json").read_text())
        pin = build_pin(facts, info, info2, mac_code_shas(C.find_lean()))
        Path(a.out).write_text(json.dumps(pin, indent=1, sort_keys=True) + "\n")
        print(json.dumps({k: pin[k] for k in ("config_sha256", "path_sha256", "server_info_stable_sha256", "pin_sha256",
                                              "stable_hash_repeats")}, indent=1))
        print("checks:", json.dumps(pin["checks"]))
        return 0 if pin["checks"]["ok"] else 1
    pin = json.loads(Path(a.pin).read_text())
    if a.vm:
        d = Path(C.BUILD / "staged/P7/verify_now")
        facts = collect(d)
        info, env = json.loads((d / "vm_server_info.json").read_text()), facts.get("env")
    else:
        info, env = json.loads(Path(a.info).read_text()), None
    res = verify(info, pin, a.mode, env)
    print(json.dumps(res, indent=1))
    return 0 if res["ok"] else 1


if __name__ == "__main__":
    sys.exit(main())
