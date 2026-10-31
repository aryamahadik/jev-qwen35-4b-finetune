"""merge_parity: merge a C2 candidate adapter into BF16, serve it on the S1 path, and prove it reads like the HF adapter
(C2 lane P7). The same bar as A49 (f) for C1: argmax agreement >= 99.5% and |d p(label)| <= 0.02 on >= 99% of rows, on a
seeded sample of >= 2,000 rows, both option orders averaged (A5 readout) as the reference.

  merge   --adapter DIR --expect-sha SHA --out DIR [--dev cpu|cuda] [--extra DIR]
          reads/export_merged.py's merge (hosting/export_c1_merged.export_local, every check it runs) for a NON-C1 adapter.
          Refuses: a non-empty --out, the production model dir, an adapter whose sha256 differs from --expect-sha, --dev cuda
          while any SGLang server is alive (the L4 holds 21 of 24 GB for production).
  serve   --model DIR --expect-sha SHA [--port 30000]       (VM; only when the GPU is free: production stopped by its owner)
          the S1 command of sglang_host.server_cmd with the production flags; refuses to start while the port is alive or the
          GPU holds > 2,000 MiB; checks the booted server against the pin (path hash); writes ~/jobs/p7_cand.pid.
  stop    [--pidfile ~/jobs/p7_cand.pid]      stops ONLY the process this tool started (its own pidfile, cmdline checked).
  parity  --adapter DIR --split NAME --ref PREDS.jsonl --n 2000 --seed S --out FILE [--port P] [--limit-check]
          reads the sample through the running server, compares with the HF-adapter reference (od_gcp.py predict
          --tta-choice of the SAME adapter), writes the record; exit 0 only on PASS.

The reference is produced by the existing tool on the L4 (one GPU job at a time):
  ~/od/bin/python -B od_gcp.py predict --name <cand> --splits <split> --tta-choice      -> preds_<split>/<cand>.jsonl (+ .meta.json)
Nothing here reads a dev or sealed split on its own: --split names a file the caller chose; sealed / OHS / benchmark names are
refused. C1 output and the candidate's output are routing / parity signals only, never labels.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import random
import signal
import subprocess
import sys
import time
import types
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import p7_common as C  # noqa: E402
import s1_pin  # noqa: E402

BAR_AGREE, BAR_DLABEL, DLABEL_TOL, MIN_N = 0.995, 0.99, 0.02, 2000
ACC_BAR_PT = 0.3                                  # SPEED-2 parity bar on accuracy (reported, strict verdict only)
GPU_FREE_MIB = 2000
CAND_PIDFILE = "~/jobs/p7_cand.pid"


# ---- pure: comparison --------------------------------------------------------------------------------------------------
def argmax(p: dict) -> str:
    return max(p, key=p.get)


def compare(ref: list, got: list) -> dict:
    """[(ref probs, fast probs)] -> metrics. label = the reference's argmax answer. Same formulas as reads/fast_read.compare
    (a test keeps them equal)."""
    n = len(ref)
    if n == 0:
        return {"n": 0}
    agree = sum(argmax(r) == argmax(g) for r, g in zip(ref, got))
    d_label = [abs(r[argmax(r)] - g[argmax(r)]) for r, g in zip(ref, got)]
    d_max = [max(abs(r[k] - g[k]) for k in r) for r, g in zip(ref, got)]
    q = lambda xs, f: sorted(xs)[min(len(xs) - 1, int(f * len(xs)))]  # noqa: E731
    return {"n": n, "argmax_agree": round(agree / n, 5), "n_disagree": n - agree,
            "frac_dlabel_le_0.02": round(sum(x <= DLABEL_TOL for x in d_label) / n, 5),
            "frac_dmax_le_0.02": round(sum(x <= DLABEL_TOL for x in d_max) / n, 5),
            "dlabel_p50_p99_max": [round(q(d_label, .5), 5), round(q(d_label, .99), 5), round(max(d_label), 5)],
            "dmax_p50_p99_max": [round(q(d_max, .5), 5), round(q(d_max, .99), 5), round(max(d_max), 5)]}


def score_row(r: dict, pr: dict) -> float:
    """gate_dev.score: argmax correct, a tie for the top counts as wrong."""
    keys, g = (["yes", "no"], "yes" if r["gold"] == 1 else "no") if r["qtype"] == "noul" else (r["options"], r["gold"])
    p = {k: float(pr.get(k, 0.0)) for k in keys}
    best = max(p.values())
    return float([k for k, v in p.items() if v == best] == [g])


def accuracy_diff(rows: list, ref: list, got: list) -> dict | None:
    if not rows or any(r.get("gold") is None for r in rows):
        return None
    a = sum(score_row(r, p) for r, p in zip(rows, ref)) / len(rows)
    b = sum(score_row(r, p) for r, p in zip(rows, got)) / len(rows)
    return {"acc_ref": round(100 * a, 3), "acc_served": round(100 * b, 3), "diff_pt": round(100 * (b - a), 3),
            "within_0.3pt": abs(100 * (b - a)) <= ACC_BAR_PT + 1e-9}


def verdict(rep_all: dict, n_requested: int, acc: dict | None = None, min_n: int = MIN_N) -> dict:
    bar = {f"n>={min_n}": rep_all.get("n", 0) >= min_n, "argmax_agree>=0.995": rep_all.get("argmax_agree", 0) >= BAR_AGREE,
           "frac_dlabel_le_0.02>=0.99": rep_all.get("frac_dlabel_le_0.02", 0) >= BAR_DLABEL}
    bar["min_n_used"] = min_n
    bar["n>=2000 (A49 f bar)"] = rep_all.get("n", 0) >= MIN_N
    bar["PASS"] = all(v for k, v in bar.items() if k not in ("min_n_used", "n>=2000 (A49 f bar)"))
    bar["PASS_gate"] = bar["PASS"] and bar["n>=2000 (A49 f bar)"]       # what counts: a --allow-small-n record is never a gate PASS
    if acc is not None:
        bar["acc_within_0.3pt (strict, SPEED-2 bar)"] = acc["within_0.3pt"]
    bar["PASS_strict"] = bar["PASS_gate"] and (acc is None or acc["within_0.3pt"])
    return bar


def sample_rows(rows: list, n: int, seed: int) -> list:
    if n > len(rows):
        raise SystemExit(f"parity: asked for {n} rows, the split has {len(rows)}")
    return [rows[i] for i in sorted(random.Random(seed).sample(range(len(rows)), n))]


def check_ref_meta(meta: dict | None, views: int) -> list:
    """The HF-adapter reference must be the same readout as the served path: schema_branch_mark / cygnet, A5 two-order average
    for choice rows, no permutation seed."""
    if meta is None:
        return ["reference meta file missing (cannot confirm layout / style / tta_choice)"]
    p = []
    if meta.get("layout") != C.LAYOUT:
        p.append(f"reference layout {meta.get('layout')!r} != {C.LAYOUT!r}")
    if meta.get("style", C.STYLE) != C.STYLE:
        p.append(f"reference style {meta.get('style')!r} != {C.STYLE!r}")
    if bool(meta.get("tta_choice")) != (views == 2):
        p.append(f"reference tta_choice={meta.get('tta_choice')!r} but the served read uses {views} view(s)")
    if meta.get("perm_seed") not in (None,):
        p.append("reference was read with a permutation seed")
    if meta.get("tta") or meta.get("tta_noul"):
        p.append("reference used the legacy tta / tta_noul switches")
    return p


def run_parity(reader, rows_all: list, refp: dict, n: int, seed: int, views: int = 2, ref_meta: dict | None = None,
               min_n: int = MIN_N) -> dict:
    """Pure given a reader with .read(rows, views=True) -> API v1 answers and Reader.probs. Raises SystemExit on id / option-key
    problems (a mismatch there is a bug, not a parity number)."""
    sample = sample_rows(rows_all, n, seed)
    missing = [r["id"] for r in sample if r["id"] not in refp]
    if missing:
        raise SystemExit(f"parity: {len(missing)} sampled rows have no reference prediction (first {missing[0]})")
    t = time.time()
    ans = reader.read(sample, views=True)
    sec = time.time() - t
    got = [reader.probs(x) for x in ans]
    ref = [refp[r["id"]] for r in sample]
    bad = [r["id"] for r, g in zip(sample, got) if set(refp[r["id"]]) != set(g)]
    if bad:
        raise SystemExit(f"parity: option keys differ from the reference on {len(bad)} rows, e.g. {bad[:3]}")
    out = {"seed": seed, "n": n, "views": views, "sample_ids_sha256": hashlib.sha256("\n".join(r["id"] for r in sample).encode()).hexdigest(),
           "label_definition": "the HF adapter reference's argmax answer", "all": compare(ref, got),
           "ref_meta_problems": check_ref_meta(ref_meta, views)}
    for t_ in ("choice", "noul"):
        idx = [i for i, r in enumerate(sample) if r["qtype"] == t_]
        out[t_] = compare([ref[i] for i in idx], [got[i] for i in idx])
    out["accuracy"] = accuracy_diff(sample, ref, got)
    out["disagreements"] = [{"id": r["id"], "qtype": r["qtype"],
                             "ref_margin": round(sorted(rf.values(), reverse=True)[0] - sorted(rf.values(), reverse=True)[1], 4),
                             "served_margin": round(sorted(g.values(), reverse=True)[0] - sorted(g.values(), reverse=True)[1], 4)}
                            for r, rf, g in zip(sample, ref, got) if argmax(rf) != argmax(g)][:60]
    out["bar"] = verdict(out["all"], n, out["accuracy"], min_n)
    if out["ref_meta_problems"]:
        out["bar"]["PASS"] = out["bar"]["PASS_strict"] = out["bar"]["PASS_gate"] = False
    out["read_sec"] = round(sec, 1)
    out["utc"] = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
    return out


# ---- which model is the server serving? ------------------------------------------------------------------------------------
def fetch_server_info(port: int, host: str = "127.0.0.1", timeout: int = 60) -> dict:
    import urllib.request
    return json.loads(urllib.request.urlopen(f"http://{host}:{port}/server_info", timeout=timeout).read().decode())


def served_identity(info: dict, adapter_sha: str) -> dict:
    """Tie a record to the model the server really serves: the server's own model_path must hold a merge_manifest.json whose
    adapter_sha256 is the sha256 of the adapter the caller names. Run it on the machine that holds the model (the VM). Raises
    SystemExit on a missing model_path / manifest or a different adapter (a forgotten server swap lands here)."""
    mp = info.get("model_path")
    if not mp:
        raise SystemExit("served: /server_info has no model_path; cannot tell which model is served")
    mf = Path(mp) / "merge_manifest.json"
    if not mf.exists():
        raise SystemExit(f"served: {mf}: no merge manifest on this machine (run this tool next to the server)")
    man_sha = json.loads(mf.read_text()).get("adapter_sha256")
    if man_sha != adapter_sha:
        raise SystemExit(f"served: the server's model {mp} was merged from adapter {str(man_sha)[:16]}, the adapter named here is "
                         f"{adapter_sha[:16]}: the server is not serving this adapter")
    return {"served_model_path": str(mp), "served_manifest_sha256": C.sha256_file(mf), "served_manifest_adapter_sha256": man_sha}


# ---- merge (candidate adapter -> BF16 checkpoint) -----------------------------------------------------------------------
def server_alive(port: int = C.PROD_PORT, host: str = "127.0.0.1", timeout: float = 2.0) -> bool:
    import http.client
    try:
        c = http.client.HTTPConnection(host, port, timeout=timeout)
        c.request("GET", "/health")
        return c.getresponse().status == 200
    except Exception:  # noqa: BLE001
        return False


def gpu_used_mib(run=subprocess.run) -> int | None:
    try:
        r = run(["nvidia-smi", "--query-gpu=memory.used", "--format=csv,noheader,nounits"], capture_output=True, text=True, timeout=20)
        return int(r.stdout.strip().splitlines()[0])
    except Exception:  # noqa: BLE001
        return None


def merge_guard(adapter_dir: Path, out_dir: Path, expect_sha: str, dev: str, prod_model: str | None, alive=server_alive) -> str:
    """The refusals of `merge`; returns the adapter sha256."""
    asha = C.sha256_file(adapter_dir / "adapter_model.safetensors")
    if asha != expect_sha:
        raise SystemExit(f"merge: adapter sha256 {asha[:16]} != --expect-sha {expect_sha[:16]}")
    if out_dir.exists() and any(out_dir.iterdir()):
        raise SystemExit(f"merge: {out_dir} is not empty")
    if prod_model and Path(prod_model).resolve() == out_dir.resolve():
        raise SystemExit("merge: --out is the production model dir")
    if dev == "cuda" and alive():
        raise SystemExit("merge: an SGLang server is alive on this machine; merge on --dev cpu (the GPU belongs to production)")
    return asha


def _import_exporter(lean: Path):
    """hosting/export_c1_merged without Modal (the stub reads/export_merged.py uses)."""
    from unittest import mock
    for p in (lean, lean / "hosting"):
        if str(p) not in sys.path:
            sys.path.insert(0, str(p))
    import decoder_io
    core = types.ModuleType("modal_direct_host")
    core.BASE, core.REVISION, core.lean_import = C.BASE, C.REVISION, lambda: decoder_io
    core.sha256_file, core.image, core.base_snapshot_complete = C.sha256_file, mock.MagicMock(), lambda *_: True
    fake_modal = mock.MagicMock()
    fake_modal.is_local.return_value = False
    sys.modules.setdefault("modal", fake_modal)
    sys.modules["modal_direct_host"] = core
    import export_c1_merged as ex
    return ex


def cmd_merge(a) -> int:
    lean = C.find_lean()
    adapter, out = Path(a.adapter).expanduser(), Path(a.out).expanduser()
    C.refuse_path(adapter)
    prod = None
    try:
        prod = json.loads(s1_pin.PIN_PATH.read_text())["model"]["path"]
    except Exception:  # noqa: BLE001
        pass
    asha = merge_guard(adapter, out, a.expect_sha, a.dev, prod)
    ex = _import_exporter(lean)
    snap = Path.home() / ".cache/huggingface/hub/models--Qwen--Qwen3.5-4B/snapshots" / C.REVISION
    extra = {p.name: p for p in sorted(Path(a.extra).expanduser().iterdir())} if a.extra else {}
    man = ex.export_local(C.BASE, snap, adapter, out, layout="base", dev=a.dev, revision=C.REVISION, fresh=True, sample=32,
                          adapter_sha=None, extra_files=extra, base_pins=ex.BASE_PINS)
    if man["adapter_sha256"] != asha:
        raise SystemExit("merge: manifest adapter sha256 differs from the adapter file")
    rec = {"adapter": str(adapter), "adapter_sha256": asha, "out": str(out), "manifest_sha256": C.sha256_file(out / "merge_manifest.json"),
           "manifest_model_field": man.get("model"),     # export_local writes the constant C1_MODEL here for any adapter; the sha is the identity
           "checks": man.get("checks"), "dev": a.dev, "utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())}
    Path(str(out) + ".p7_merge.json").write_text(json.dumps(rec, indent=1, default=str))
    print(json.dumps({k: rec[k] for k in ("adapter_sha256", "manifest_sha256", "out")}, indent=1))
    return 0 if (man.get("checks") or {}).get("passed", True) else 1


# ---- serve / stop (only a process this tool started) ---------------------------------------------------------------------
def candidate_cmd(model: str, port: int, python: str = "python3") -> list:
    """The production S1 command (reads/start_server.sh --max-running 32 --max-mamba 128 --mem-fraction 0.8 --extra-args
    "--attention-backend triton") for another model path / port. A test keeps it equal to the pinned argv."""
    SH = s1_pin.sh_mod()
    cmd = SH.server_cmd(model, fp8=False, port=port, max_running_requests=s1_pin.VM_DEFAULTS["max_running_requests"],
                        max_mamba_cache_size=s1_pin.VM_DEFAULTS["max_mamba_cache_size"],
                        mem_fraction_static=s1_pin.VM_DEFAULTS["mem_fraction_static"], python=python)
    return cmd + ["--attention-backend", s1_pin.VM_DEFAULTS["attention_backend"]]


def serve_guard(model: Path, expect_sha: str, port: int, alive=server_alive, gpu_used=gpu_used_mib) -> dict:
    mp = model / "merge_manifest.json"
    if not mp.exists():
        raise SystemExit(f"serve: {model}: no merge_manifest.json")
    man = json.loads(mp.read_text())
    if man.get("adapter_sha256") != expect_sha:
        raise SystemExit(f"serve: manifest adapter sha256 {str(man.get('adapter_sha256'))[:16]} != --expect-sha {expect_sha[:16]}")
    if alive(port):
        raise SystemExit(f"serve: port {port} is alive: a server is running; this tool never stops one it did not start")
    used = gpu_used()
    if used is None or used > GPU_FREE_MIB:
        raise SystemExit(f"serve: the GPU holds {used} MiB (> {GPU_FREE_MIB}): production (or another job) is running. Its owner "
                         "must stop it first (prod_stop.sh); this tool does not")
    return man


def cmd_serve(a) -> int:
    SH = s1_pin.sh_mod()
    model = Path(a.model).expanduser()
    serve_guard(model, a.expect_sha, a.port)
    pin = json.loads(Path(a.pin).read_text())
    cmd = candidate_cmd(str(model), a.port, str(Path(a.sgl_python).expanduser()))
    log = open(Path(a.log).expanduser(), "ab")
    p = subprocess.Popen(cmd, env=SH.server_env(), stdout=log, stderr=subprocess.STDOUT, start_new_session=True)
    Path(a.pidfile).expanduser().write_text(str(p.pid))
    print(f"launched candidate SGLang pid {p.pid}", flush=True)
    t0 = time.time()
    while time.time() - t0 < a.boot_timeout:
        if p.poll() is not None:
            raise SystemExit(f"serve: SGLang exited rc={p.returncode}; see {a.log}")
        if server_alive(a.port):
            break
        time.sleep(5)
    else:
        os.killpg(os.getpgid(p.pid), signal.SIGTERM)
        raise SystemExit("serve: not up in time; stopped the process this tool started")
    import urllib.request
    info = json.loads(urllib.request.urlopen(f"http://127.0.0.1:{a.port}/server_info", timeout=60).read().decode())
    env = {k: os.environ.get(k) for k in s1_pin.ENV_PINS} | s1_pin.sh_mod().SERVER_ENV
    res = s1_pin.verify(info, pin, "path", env)
    res["boot_s"] = round(time.time() - t0, 1)
    print(json.dumps(res, indent=1))
    if not res["ok"]:
        os.killpg(os.getpgid(p.pid), signal.SIGTERM)
        Path(a.pidfile).expanduser().unlink(missing_ok=True)
        raise SystemExit("serve: the booted server differs from the S1 pin; stopped the process this tool started")
    return 0


def stop_guard(pid: int, cmdline: list, own_pid_text: str | None, prod_pid_text: str | None, prod_model: str | None) -> None:
    joined = " ".join(cmdline)
    if "sglang.launch_server" not in joined:
        raise SystemExit(f"stop: pid {pid} is not an SGLang server")
    if prod_pid_text and str(pid) == prod_pid_text.strip():
        raise SystemExit("stop: that is the production server's pid")
    if prod_model and f"--model-path {prod_model}" in joined:
        raise SystemExit("stop: that process serves the production model")
    if own_pid_text is None or str(pid) != own_pid_text.strip():
        raise SystemExit("stop: pid is not the one in this tool's own pidfile")


def cmd_stop(a) -> int:
    pf = Path(a.pidfile).expanduser()
    if not pf.exists():
        print("no candidate pidfile: nothing to stop")
        return 0
    pid = int(pf.read_text())
    try:
        cmdline = [x.decode() for x in open(f"/proc/{pid}/cmdline", "rb").read().split(b"\0") if x]
    except FileNotFoundError:
        print("candidate already gone")
        pf.unlink()
        return 0
    prod_pid = Path("~/jobs/sglang.pid").expanduser()
    prod_model = None
    try:
        prod_model = json.loads(s1_pin.PIN_PATH.read_text())["model"]["path"]
    except Exception:  # noqa: BLE001
        pass
    stop_guard(pid, cmdline, pf.read_text(), prod_pid.read_text() if prod_pid.exists() else None, prod_model)
    os.killpg(os.getpgid(pid), signal.SIGTERM)
    pf.unlink()
    print("stopped candidate pid", pid)
    return 0


# ---- parity (live) --------------------------------------------------------------------------------------------------------
def load_fast_read():
    for d in (os.environ.get("P7_FAST_READ_DIR"), C.BUILD / "reads", Path.home() / "reads"):
        if d and (Path(d) / "fast_read.py").exists():
            if str(d) not in sys.path:
                sys.path.insert(0, str(d))
            import fast_read
            return fast_read
    raise SystemExit("p7: fast_read.py not found (set P7_FAST_READ_DIR)")


def read_jsonl(p) -> list:
    return [json.loads(l) for l in open(p) if l.strip()]


def cmd_parity(a) -> int:
    root = Path(a.root).expanduser().resolve()
    for p in (a.split, a.ref, a.adapter):
        C.refuse_path(p)
    split = Path(a.split)
    sp = split if split.exists() else root / "data" / f"{a.split}.jsonl"
    rows = read_jsonl(sp)
    refp = {x["id"]: x["probs"] for x in read_jsonl(root / a.ref if not Path(a.ref).is_absolute() else a.ref)}
    meta_p = Path(str(a.ref)[:-len(".jsonl")] + ".meta.json")
    meta_p = meta_p if meta_p.is_absolute() else root / meta_p
    ref_meta = json.loads(meta_p.read_text()) if meta_p.exists() else None
    if a.min_n < MIN_N and not a.allow_small_n:
        raise SystemExit(f"parity: --min-n {a.min_n} is below the {MIN_N}-row bar; --allow-small-n is for tests (the record is never a gate PASS)")
    adapter = Path(a.adapter).expanduser()
    adapter_sha = C.sha256_file(adapter / "adapter_model.safetensors")
    info = fetch_server_info(a.port)
    ident = served_identity(info, adapter_sha)                       # refuses before any read if the server serves another model
    hashes = s1_pin.hashes(info, s1_pin.sh_mod().SERVER_ENV)
    fr = load_fast_read()
    reader = fr.Reader(a.port, adapter, a.workers, a.chunk, views=a.views)
    rep = run_parity(reader, rows, refp, a.n, a.seed, a.views, ref_meta, a.min_n)
    rep.update({"split": a.split, "split_sha256": C.sha256_file(sp), "ref": str(a.ref), "ref_sha256": C.sha256_file(root / a.ref if not Path(a.ref).is_absolute() else a.ref),
                "adapter": str(a.adapter), "adapter_sha256": adapter_sha, **ident,
                "server_info_path_sha256": hashes["path_sha256"], "config_sha256": hashes["config_sha256"],
                "throughput": dict(reader.stats)})
    after = s1_pin.hashes(fetch_server_info(a.port), s1_pin.sh_mod().SERVER_ENV)["config_sha256"]
    if after != hashes["config_sha256"]:                             # the server changed while it was being read
        rep["bar"]["PASS"] = rep["bar"]["PASS_strict"] = rep["bar"]["PASS_gate"] = False
        rep["served_problems"] = ["server config changed during the parity read"]
    Path(a.out).expanduser().write_text(json.dumps(rep, indent=1, default=str))
    print(json.dumps({k: rep[k] for k in ("all", "choice", "noul", "accuracy", "bar")}, indent=1, default=str))
    return 0 if rep["bar"]["PASS"] else 2


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)
    m = sub.add_parser("merge")
    m.add_argument("--adapter", required=True)
    m.add_argument("--expect-sha", dest="expect_sha", required=True)
    m.add_argument("--out", required=True)
    m.add_argument("--dev", choices=("cpu", "cuda"), default="cpu")
    m.add_argument("--extra", default="")
    s = sub.add_parser("serve")
    s.add_argument("--model", required=True)
    s.add_argument("--expect-sha", dest="expect_sha", required=True)
    s.add_argument("--port", type=int, default=C.PROD_PORT)
    s.add_argument("--pin", default=str(s1_pin.PIN_PATH))
    s.add_argument("--sgl-python", default="~/sgl/bin/python")
    s.add_argument("--log", default="~/jobs/p7_cand_server.log")
    s.add_argument("--pidfile", default=CAND_PIDFILE)
    s.add_argument("--boot-timeout", type=int, default=1200)
    t = sub.add_parser("stop")
    t.add_argument("--pidfile", default=CAND_PIDFILE)
    p = sub.add_parser("parity")
    p.add_argument("--root", default=str(C.find_lean()))
    p.add_argument("--adapter", required=True)
    p.add_argument("--split", required=True)
    p.add_argument("--ref", required=True)
    p.add_argument("--n", type=int, default=2000)
    p.add_argument("--min-n", dest="min_n", type=int, default=MIN_N, help=f"below {MIN_N} only with --allow-small-n")
    p.add_argument("--allow-small-n", dest="allow_small_n", action="store_true", help="tests only: a record under the bar is never PASS_gate")
    p.add_argument("--seed", type=int, required=True)
    p.add_argument("--views", type=int, choices=(1, 2), default=2)
    p.add_argument("--port", type=int, default=C.PROD_PORT)
    p.add_argument("--workers", type=int, default=12)
    p.add_argument("--chunk", type=int, default=8)
    p.add_argument("--out", default="~/jobs/p7_parity.json")
    a = ap.parse_args(argv)
    return {"merge": cmd_merge, "serve": cmd_serve, "stop": cmd_stop, "parity": cmd_parity}[a.cmd](a)


if __name__ == "__main__":
    sys.exit(main())
