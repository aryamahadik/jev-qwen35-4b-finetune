"""Our OHS-3 endpoint on ONE Modal H100 behind a direct tunnel (modal.forward), with CUDA graphs: the serving core of
hosting/modal_direct_host.py (same image, Volume, boot, graph capture, HTTP server; imported, not copied) with the
OHS-3 decider (prep89/ohs3_lib.A5Decider: A5 readout, pre-registered T, up to 255 options, yes/no cards).
NOT RUN ON MODAL YET (the CPU test checks import, objects and the decider; nothing here has been billed).

Only after the owner's GO (about $5-8: boot ~8 min + ~20-30 min serving at the narrow-region H100 rate):
  MODAL_PROFILE=<acct> ../.venv/bin/modal run prep89/modal_ohs3_host.py::main --config prep89/ohs3_config.json \\
      --model-key 4b --name ohs3_timing --go [--scored-name q35_4b_pxE] [--od-preds-name q35_4b_pxE] \\
      [--jev-preds-tag jev_guard] [--limit 0]
  The local entrypoint boots the server, runs prep89/ohs3_timing.py IN-PROCESS from this laptop (interleaved with Jev,
  concurrency 1), then POSTs /shutdown. Never pass --detach. Ctrl-C also stops the H100.
  GPU smoke on DEV rows only (no OHS-3, no Jev; ~$1-2, mostly boot), recommended before the OHS-3 pass:
    MODAL_PROFILE=<acct> ../.venv/bin/modal run prep89/modal_ohs3_host.py::main --config prep89/ohs3_config.json \
        --name h100_dev_smoke --dev-smoke dev_nc:60,devp_card:40 --go
  The 2B (PRISM-X I: no CUDA graphs, decoder_io.GraphRunner refuses it) and the 2B -> 4B cascade (both models on the
  same H100: the 4B on graphs, the 2B eager, routing rule = the config's cascade.tau / w_big / route_on):
    ... modal run prep89/modal_ohs3_host.py::main --config prep89/ohs3_config.json --model-key 2b --name ohs3_timing_2b ...
    ... modal run prep89/modal_ohs3_host.py::main --config prep89/ohs3_config.json --model-key cascade \\
        --name ohs3_timing_cascade ...      (same flags as the 4B pass; see ohs3_runbook.md for D1/D2 per system)
  C1 load test (DEV rows only; prep89/load_test_c1.py, its docstring has the method; `load_test_c1.py --plan` prints
  the commands and the cost from the config): add --then-load-test to the timing pass (same session, ~7.2 extra
  minutes, $0.51-0.90), or on its own (~16 min for the 4B, $1.16-2.03):
    ... modal run prep89/modal_ohs3_host.py::main --config prep89/ohs3_config.json --model-key 4b --name c1_load_4b \\
        --load-test --load-match logs/ohs3/timing/ohs3_timing/records.jsonl --go
Guards: max_containers=1; the server stops on /shutdown, after --seconds or after --idle seconds without a request;
the function timeout (75 min) is the hard cap. The adapter sha256 (for the 2B also prism_x.safetensors' sha256) and
layout are checked against the config before the URL is published; a mismatch stops the container. The 2B's PRISM-X control plane must be ACTIVE after the merge with
the config's parts (ohs3_lib.check_prism_x); the cascade loads the 4B first and the 2B last (decoder_io.load
uninstalls PRISM-X) and re-checks both. The region is the config's hosting.region (timing and C1 price use it).
"""
from __future__ import annotations

import json
import sys
import threading
import time
from pathlib import Path

import modal

PREP = Path(__file__).resolve().parent
# Modal 1.x ships only the entrypoint file (this one, at /root/) into the container: the hosting core is added to the
# image below at /root/hosting/, and found there in the container (locally: lean/hosting/).
REMOTE_HOSTING = Path("/root/hosting")
for _p in (PREP.parent / "hosting", REMOTE_HOSTING):
    if (_p / "modal_direct_host.py").exists():
        sys.path.insert(0, str(_p))
        break
sys.path.insert(0, str(PREP))
import modal_direct_host as core  # noqa: E402  (local guards: PINNED35 == modal_od.py's)

APP_NAME = "od-ohs3-host"
FUNCTION_TIMEOUT_S = 75 * 60
image = (core.image
         .add_local_file(PREP.parent / "hosting" / "modal_direct_host.py", str(REMOTE_HOSTING / "modal_direct_host.py"))
         .add_local_file(PREP / "ohs3_lib.py", "/root/prep89/ohs3_lib.py")
         .add_local_file(PREP.parent / "calibrate.py", "/root/calibrate.py"))  # ohs3_lib.scaled reads it (AST only)
app = modal.App(APP_NAME)


def make_a5(dec, m, dev):
    if "/root/prep89" not in sys.path:
        sys.path.insert(0, "/root/prep89")
    import ohs3_lib as L
    return L.A5Decider(dec.dio, dec.model, dec.ro, dev, m["readout_choice"], m["T_primary"], m["T_single"],
                       sync=dec.sync, lock=dec.lock)


def a5_selfcheck(dec, a5) -> float:
    """The A5 decider's identity view must be the core decider's single read (same code path, T = 1): max |dp|."""
    ref = dec.decide(core.EXAMPLE)
    got = a5.decide({**core.EXAMPLE, "return_views": True})
    d = 0.0
    for k, ans in ref["answers"].items():
        v = got["answers"][k]["views"]["1v"]
        if ans["type"] == "noul":
            d = max(d, abs(ans["noul"] - v["yes"]))
        else:
            d = max(d, max(abs(ans["probabilities"][o] - v[o]) for o in v))
    return d


def boot_ohs3(m, graph_cfg, log=print):
    """core.boot_gpu (load + merge + warm-up + graphs + self-check), then the OHS-3 decider on the same model."""
    if m["base"] != core.BASE:
        raise SystemExit(f"this host serves {core.BASE} adapters only (got {m['base']})")
    if m["revision"] != core.REVISION:
        raise SystemExit(f"revision {m['revision']} != the host's pinned {core.REVISION}")
    dec, info = core.boot_gpu(m["name"], graph_cfg, log=log)
    if info["adapter_sha256"] != m["adapter_sha256"]:
        raise SystemExit(f"adapter sha256 {info['adapter_sha256'][:16]} != pre-registered {m['adapter_sha256'][:16]}")
    if (info["load"].get("layout"), info["load"].get("style")) != (m["layout"], m["style"]):
        raise SystemExit(f"layout/style {info['load']} != pre-registered {(m['layout'], m['style'])}")
    a5 = make_a5(dec, m, "cuda")
    d = a5_selfcheck(dec, a5)
    info["a5_selfcheck_max_dp_vs_core"] = d
    if d > 1e-4:
        raise SystemExit(f"A5 decider identity view differs from the core decider by {d}")
    dec.log.clear()
    a5.log.clear()
    info.update(readout=m["readout_choice"], T=m["T_primary"], T_single=m["T_single"])
    return a5, info


@app.function(image=image, gpu="H100!", cpu=2.0, memory=16384, volumes={"/vol": core.vol}, timeout=FUNCTION_TIMEOUT_S,
              max_containers=1)
def serve_ohs3(q: modal.Queue, token: str, m: dict, graph_cfg: dict, config_sha256: str, seconds: int = 3600,
               idle_s: int = 300) -> dict:
    t0 = time.time()
    a5, info = boot_ohs3(m, graph_cfg)
    info["config_sha256"] = config_sha256
    stop = threading.Event()
    srv, st = core.make_server(core.PORT, token, a5.decide, lambda: info, stop.set)
    threading.Thread(target=srv.serve_forever, daemon=True).start()
    with modal.forward(core.PORT) as tunnel:
        st["last"] = time.time()
        q.put({"url": tunnel.url, "health": info})
        reason = core.wait_loop(stop, st, seconds, idle_s)
    srv.shutdown()
    out = {"info": info, "served": st["n"], "errors": st["errors"], "server_side": a5.stats(), "stop": reason,
           "wall_s": round(time.time() - t0, 1)}
    print("DONE " + json.dumps(out), flush=True)
    return out


# ------------------------------------------------------------------ the 2B (PRISM-X I: eager) and the 2B -> 4B cascade

EAGER_WARMUP = {"max_tokens": 8192, "batch_sizes": [1]}  # OHS-3 requests are one row; the 2-view second read too
CASCADE_MIN_FREE_GB = 12.0  # after the 4B + its graphs: room for the 2B (~4.5 GB bf16 + PRISM-X) and eager activations


def snapshot_complete(hf_home, base, revision) -> bool:
    """core.base_snapshot_complete for any base/revision (the test checks both agree on the 4B)."""
    snap = Path(hf_home) / "hub" / ("models--" + base.replace("/", "--")) / "snapshots" / str(revision)
    if not (snap / "config.json").exists():
        return False
    idx = snap / "model.safetensors.index.json"
    if idx.exists():
        files = set(json.loads(idx.read_text())["weight_map"].values())
        return all((snap / f).exists() for f in files)
    return (snap / "model.safetensors").exists()


def hf_env_for(models, hf_home="/vol/hf") -> str:
    """Choose the Hugging Face cache for EVERY base this container loads, before any Hugging Face import (huggingface_hub
    reads HF_HOME / HF_HUB_OFFLINE once, at import): all snapshots complete on the Volume -> read them offline; else
    download every base to the container's own disk (/tmp/hf). The Volume is never written. core.boot_gpu decides the
    same way for the 4B; when a 2B snapshot is missing its check is overridden so both bases come from /tmp/hf."""
    import os
    if all(snapshot_complete(hf_home, m["base"], m["revision"]) for m in models):
        os.environ["HF_HUB_OFFLINE"] = "1"
        return f"{hf_home} snapshots (offline)"
    os.environ.pop("HF_HUB_OFFLINE", None)
    os.environ["HF_HOME"] = "/tmp/hf"
    core.base_snapshot_complete = lambda h: False  # core.boot_gpu then downloads the 4B base to /tmp/hf as well
    return "downloaded to /tmp/hf"


def seed_triton_cache() -> str:
    """As core.boot_gpu: a private copy of the Volume's Triton cache (read only)."""
    import os
    import shutil
    tc = Path("/tmp/triton_cache")
    try:
        shutil.copytree("/vol/triton_cache", tc, dirs_exist_ok=True)
        msg = "seeded from /vol/triton_cache"
    except Exception as e:  # noqa: BLE001
        msg = f"not seeded: {type(e).__name__}"
    os.environ["TRITON_CACHE_DIR"] = str(tc)
    return msg


def boot_eager(m, log=print, env_done=False, lock=None):
    """A model that cannot run on CUDA graphs (the PRISM-X I 2B): load + merge from the Volume, checks against the
    config (adapter sha256, prism_x.safetensors sha256, base commit, layout/style, PRISM-X parts ACTIVE after the
    merge), eager Triton warm-up,
    then the A5 decider; self-check: its identity view == decoder_io.predict on the same rows (same eager code)."""
    import torch
    if "/root/prep89" not in sys.path:
        sys.path.insert(0, "/root/prep89")
    import ohs3_lib as L
    t0 = time.time()
    info = {"app": APP_NAME, "model": m["name"], "base": m["base"], "revision": m["revision"], "path": "eager",
            "cuda_graphs": False, "started_utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())}
    if not env_done:
        info["triton_cache"] = seed_triton_cache()
        info["base_source"] = hf_env_for([m])
    model_dir = Path("/vol/models") / m["name"]
    if not (model_dir / "adapter_model.safetensors").exists():
        raise SystemExit(f"{model_dir} missing on this account's Volume")
    info["adapter_sha256"] = core.sha256_file(model_dir / "adapter_model.safetensors")
    if info["adapter_sha256"] != m["adapter_sha256"]:
        raise SystemExit(f"adapter sha256 {info['adapter_sha256'][:16]} != pre-registered {m['adapter_sha256'][:16]}")
    info["prism_x_sha256"] = L.check_prism_x_file(m, model_dir)  # PRISM-X weights == the config's (before any load)
    dio = core.lean_import()
    info["code_sha256"] = {n: core.sha256_file(Path(core.REMOTE_LEAN) / n) for n in core.LEAN_FILES}
    model, tok, load_info = dio.load(m["base"], "cuda", adapter=str(model_dir), revision=m["revision"],
                                     layout=m["layout"], style=m["style"], return_info=True)
    commit = getattr(getattr(model, "config", None), "_commit_hash", None)
    if commit is not None and commit != m["revision"]:
        raise SystemExit(f"loaded base commit {commit}, pre-registered {m['revision']}")
    model = model.merge_and_unload()
    model.eval()
    for c in (model.config, getattr(model.config, "text_config", None)):
        if c is not None:
            c.use_cache = True
    if (dio.LAYOUT, dio.STYLE) != (m["layout"], m["style"]):
        raise SystemExit(f"layout/style {(dio.LAYOUT, dio.STYLE)} != pre-registered {(m['layout'], m['style'])}")
    info["load"] = {k: load_info.get(k) for k in ("layout", "style", "revision", "prism_x", "chat_template_sha")}
    info["prism_x"] = L.check_prism_x(m, dio, model)
    info["load_s"] = round(time.time() - t0, 1)
    ro = dio.Readout(tok)
    tw = time.time()
    dio.warmup(model, ro, max_tokens=EAGER_WARMUP["max_tokens"], batch_sizes=tuple(EAGER_WARMUP["batch_sizes"]))
    torch.cuda.empty_cache()
    info["warmup_s"] = round(time.time() - tw, 1)
    a5 = L.A5Decider(dio, model, ro, "cuda", m["readout_choice"], m["T_primary"], m["T_single"],
                     sync=torch.cuda.synchronize, lock=lock)
    rows = [r for _, r in L.parse_rows(core.EXAMPLE)]
    ref = dio.predict(model, tok, rows, dev="cuda")
    got = a5.decide({**core.EXAMPLE, "return_views": True})
    d = max(max(abs(ref[i][k] - got["answers"][n]["views"]["1v"][k]) for k in ref[i])
            for i, n in enumerate(core.EXAMPLE["questions"]))
    info["a5_selfcheck_max_dp_vs_predict"] = d
    if d > 1e-4:
        raise SystemExit(f"A5 decider identity view differs from decoder_io.predict by {d}")
    if info["prism_x"]["active"]:  # informational: the control plane changes the read (it is on)
        pxm = dio._prism_x()
        pxm.STATE["enabled"] = False
        try:
            off = dio.predict(model, tok, rows, dev="cuda")
        finally:
            pxm.STATE["enabled"] = True
        info["prism_x_effect_max_dp"] = max(abs(ref[i][k] - off[i][k]) for i in range(len(rows)) for k in ref[i])
    for _ in range(3):
        a5.decide(core.EXAMPLE)
    a5.log.clear()
    info.update(readout=m["readout_choice"], T=m["T_primary"], T_single=m["T_single"],
                memory_gb={"max_allocated": round(torch.cuda.max_memory_allocated() / 2 ** 30, 2),
                           "free": round(torch.cuda.mem_get_info()[0] / 2 ** 30, 2)},
                gpu=torch.cuda.get_device_name(0), region=__import__("os").environ.get("MODAL_REGION"),
                boot_s=round(time.time() - t0, 1))
    log("BOOT " + json.dumps(info, default=str))
    return a5, info


def boot_cascade(m_small, m_big, casc, graph_cfg, log=print):
    """Both models on ONE H100: the 4B first (core boot: graphs, its checks), then the 2B eagerly (decoder_io.load
    uninstalls any PRISM-X control plane, so the PRISM-X model must be the last one loaded), one GPU lock; then the
    cascade decider with the pre-registered tau / w_big / route_on. Checks: both PRISM-X states as configured after
    both loads, the 4B still replays graphs, the cascade answers equal the rule on the served readouts."""
    import torch
    if "/root/prep89" not in sys.path:
        sys.path.insert(0, "/root/prep89")
    import ohs3_lib as L
    t0 = time.time()
    src = hf_env_for([m_big, m_small])
    big, info_big = boot_ohs3(m_big, graph_cfg, log=log)  # core.boot_gpu seeds the Triton cache
    free = torch.cuda.mem_get_info()[0] / 2 ** 30
    if free < CASCADE_MIN_FREE_GB:
        raise SystemExit(f"{free:.1f} GB free after the 4B and its graphs: the 2B needs {CASCADE_MIN_FREE_GB} GB")
    small, info_small = boot_eager(m_small, log=log, env_done=True, lock=big.lock)
    dio = small.dio
    if (dio.LAYOUT, dio.STYLE) != (m_big["layout"], m_big["style"]):
        raise SystemExit("cascade: the 2B load changed decoder_io's layout/style away from the 4B's")
    px = {"small": L.check_prism_x(m_small, dio, small.model), "big": L.check_prism_x(m_big, dio, big.model)}
    dec = L.CascadeDecider(small, big, casc["tau"], casc["w_big"], casc.get("route_on", "primary"), lock=big.lock)
    got = dec.decide({**core.EXAMPLE, "return_views": True})
    big_path = big.decide(core.EXAMPLE)["path"]
    for _ in range(2):
        dec.decide(core.EXAMPLE)
    dec.log.clear()
    small.log.clear()
    big.log.clear()
    info = {"app": APP_NAME, "model": casc["name"], "system": "cascade", "base_source": src,
            "cascade": {k: casc.get(k) for k in ("tau", "w_big", "route_on")} | {"small": m_small["name"],
                                                                                 "big": m_big["name"]},
            "big": info_big, "small": info_small, "prism_x_after_both_loads": px, "big_path_after_2b_load": big_path,
            "example_routed": {k: v["routed"] for k, v in got["answers"].items()},
            "readout": dec.decide(core.EXAMPLE)["readout"], "boot_s": round(time.time() - t0, 1),
            "memory_free_gb": round(torch.cuda.mem_get_info()[0] / 2 ** 30, 2), "gpu": torch.cuda.get_device_name(0)}
    dec.log.clear()
    log("BOOT cascade " + json.dumps({k: info[k] for k in ("cascade", "prism_x_after_both_loads", "big_path_after_2b_load",
                                                           "boot_s")}, default=str))
    return dec, info


def _serve_until_stopped(dec, info, q, token, seconds, idle_s, t0):
    stop = threading.Event()
    srv, st = core.make_server(core.PORT, token, dec.decide, lambda: info, stop.set)
    threading.Thread(target=srv.serve_forever, daemon=True).start()
    with modal.forward(core.PORT) as tunnel:
        st["last"] = time.time()
        q.put({"url": tunnel.url, "health": info})
        reason = core.wait_loop(stop, st, seconds, idle_s)
    srv.shutdown()
    out = {"info": info, "served": st["n"], "errors": st["errors"], "server_side": dec.stats(), "stop": reason,
           "wall_s": round(time.time() - t0, 1)}
    print("DONE " + json.dumps(out, default=str), flush=True)
    return out


@app.function(image=image, gpu="H100!", cpu=2.0, memory=16384, volumes={"/vol": core.vol}, timeout=FUNCTION_TIMEOUT_S,
              max_containers=1)
def serve_ohs3_eager(q: modal.Queue, token: str, m: dict, config_sha256: str, seconds: int = 3600,
                     idle_s: int = 300) -> dict:
    """The PRISM-X 2B (or any model with cuda_graphs false): eager serving, same HTTP server and decider."""
    t0 = time.time()
    a5, info = boot_eager(m)
    info["config_sha256"] = config_sha256
    return _serve_until_stopped(a5, info, q, token, seconds, idle_s, t0)


@app.function(image=image, gpu="H100!", cpu=2.0, memory=16384, volumes={"/vol": core.vol}, timeout=FUNCTION_TIMEOUT_S,
              max_containers=1)
def serve_ohs3_cascade(q: modal.Queue, token: str, m_small: dict, m_big: dict, casc: dict, graph_cfg: dict,
                       config_sha256: str, seconds: int = 3600, idle_s: int = 300) -> dict:
    """The 2B -> 4B cascade on one H100 (4B on graphs, 2B eager), timed end to end with routing."""
    t0 = time.time()
    dec, info = boot_cascade(m_small, m_big, casc, graph_cfg)
    info["config_sha256"] = config_sha256
    return _serve_until_stopped(dec, info, q, token, seconds, idle_s, t0)


def serve_fn_for(cfg, model_key):
    """(Modal function, its spawn args after (q, token), what) for a system: the 4B with graphs, an eager model
    (cuda_graphs false / PRISM-X), or the cascade."""
    import ohs3_lib as L
    s = L.system(cfg, model_key)
    clean = lambda m: {k: v for k, v in m.items() if not k.startswith("_")}  # noqa: E731
    if s["kind"] == "cascade":
        c = cfg["cascade"]
        return serve_ohs3_cascade, (clean(cfg["models"][c["small"]]), clean(cfg["models"][c["big"]]),
                                    {k: c.get(k) for k in ("name", "tau", "w_big", "route_on")},
                                    cfg["hosting"]["graph_cfg"], cfg["_sha256"]), "cascade (4B graphs + 2B eager)"
    m = cfg["models"][model_key]
    if m.get("cuda_graphs") is False or m.get("prism_x"):
        return serve_ohs3_eager, (clean(m), cfg["_sha256"]), "eager"
    return serve_ohs3, (clean(m), cfg["hosting"]["graph_cfg"], cfg["_sha256"]), "CUDA graphs"


@app.local_entrypoint()
def main(config: str, model_key: str = "4b", name: str = "ohs3_timing", region: str = "", seconds: int = 3600,
         idle: int = 300, limit: int = 0, scored_name: str = "", od_preds_name: str = "", jev_preds_tag: str = "",
         no_jev: bool = False, go: bool = False, boot_wait: int = 1500, dev_smoke: str = "", smoke_ref_1v: str = "",
         smoke_ref_2v: str = "", smoke_ref_big_1v: str = "", load_test: bool = False, then_load_test: bool = False,
         load_match: str = "", load_name: str = "", tokenizer_dir: str = ""):
    """--model-key 4b | 2b | cascade picks the served system (graphs / eager / both on one H100). Modes:
    OHS-3 timing pass (default; then_load_test: the C1 dev load test right after it, same session, length-matched to
    this pass's logged token counts); dev_smoke (DEV rows only); load_test (DEV rows only; load_match = an earlier
    pass's records.jsonl, or none for a pre-run estimate). The region is the config's hosting.region (the C1 rate)."""
    import secrets
    import ohs3_lib as L
    import ohs3_timing as T
    if not go:
        raise SystemExit("needs --go (owner's GO): this bills an H100")
    cfg = L.load_config(config, require_complete=True, model_keys=[model_key])
    sysm = L.system(cfg, model_key)
    if seconds + 900 > FUNCTION_TIMEOUT_S:
        raise SystemExit(f"--seconds must be <= {FUNCTION_TIMEOUT_S - 900}")
    region = region or cfg["hosting"]["region"]
    if region != cfg["hosting"]["region"] and not dev_smoke:
        raise SystemExit(f"--region {region} differs from the pre-registered hosting.region {cfg['hosting']['region']} "
                         "(timing and the C1 load test run in the serving region; only a dev smoke may differ)")
    if sum(bool(x) for x in (dev_smoke, load_test)) > 1 or (then_load_test and (dev_smoke or load_test)):
        raise SystemExit("choose one mode: OHS-3 timing (optionally --then-load-test), --dev-smoke, or --load-test")
    fn, args, what = serve_fn_for(cfg, model_key)
    reg, mult = core._region_opt(region)
    token = secrets.token_urlsafe(24)
    t0 = time.time()
    res, msg, up_s = None, {}, None
    with modal.Queue.ephemeral() as q:
        call = fn.with_options(gpu="H100!", **({"region": reg} if reg else {})).spawn(q, token, *args, seconds, idle)
        msg = core._wait_url(q, call, boot_wait, f"OHS-3 H100 server, {sysm['name']} ({what}, {region})")
        url = msg["url"]
        up_s = round(time.time() - t0, 1)  # cold start (spawn -> URL published): reported apart from S1
        print(f"server up after {up_s:.0f} s; health: {json.dumps(msg['health'], default=str)[:1500]}", flush=True)
        try:
            import client_bench as cb
            cb.wait_ready(url, token)
            if dev_smoke:  # DEV rows only: GPU check of the served path before the OHS-3 pass
                T.main(["--config", config, "--model-key", model_key, "--name", name, "--od-url", url,
                        "--od-token", token, "--dev-smoke", dev_smoke]
                       + (["--smoke-ref-1v", smoke_ref_1v] if smoke_ref_1v else [])
                       + (["--smoke-ref-2v", smoke_ref_2v] if smoke_ref_2v else [])  # default: ohs3_timing.smoke_refs
                       + (["--smoke-ref-big-1v", smoke_ref_big_1v] if smoke_ref_big_1v else []))
            elif load_test:  # DEV rows only: the C1 throughput (no OHS-3 call, no Jev)
                lt_main(config, model_key, load_name or name, url, token, load_match, tokenizer_dir)
            else:
                argv = ["--config", config, "--model-key", model_key, "--od-url", url, "--od-token", token, "--name",
                        name, "--go", "--limit", str(limit)]
                argv += ["--scored-name", scored_name] if scored_name else []
                argv += ["--od-preds-name", od_preds_name] if od_preds_name else []
                argv += ["--jev-preds-tag", jev_preds_tag] if jev_preds_tag else []
                argv += ["--no-jev"] if no_jev else []
                T.main(argv)
                if then_load_test:  # same session: matched to the token counts this pass just logged
                    lt_main(config, model_key, load_name or f"{name}_c1", url, token,
                            str(L.LEAN / "logs" / "ohs3" / "timing" / name / "records.jsonl"), tokenizer_dir)
        except KeyboardInterrupt:
            print("interrupted: shutting the server down", flush=True)
        finally:
            import client_bench as cb
            res = core._finish(call, cb, url, token)
    wall_h = (time.time() - t0) / 3600
    est = {"wall_min": round(wall_h * 60, 1), "rate_usd_h": round(core.GPU_RATE_USD_H * mult, 2),
           "est_usd_upper": round(wall_h * core.GPU_RATE_USD_H * mult, 2), "served": what, "region": region}
    sub = "load_test" if load_test else "timing"
    out = L.LEAN / "logs" / "ohs3" / sub / ((load_name or name) if load_test else name)
    out.mkdir(parents=True, exist_ok=True)
    (out / "server_return.json").write_text(json.dumps({"server": res, "cost_estimate": est, "cold_start": {
        "spawn_to_url_s": up_s, "boot_s": (msg.get("health") or {}).get("boot_s"),
        "note": "speed definition: cold start is reported separately and is not in S1"}}, indent=2, default=str))
    print(json.dumps({"cost_estimate": est, "server_stop": (res or {}).get("stop")}, indent=1))


def lt_main(config, model_key, name, url, token, match, tokenizer_dir):
    import load_test_c1 as LT
    argv = ["--config", config, "--model-key", model_key, "--od-url", url, "--od-token", token, "--name", name]
    argv += ["--match-records", match] if match else []
    argv += ["--tokenizer-dir", tokenizer_dir] if tokenizer_dir else []
    return LT.main(argv)
