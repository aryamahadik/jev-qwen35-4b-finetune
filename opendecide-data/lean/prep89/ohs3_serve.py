"""Our OHS-3 endpoint: the A5 serving readout (ohs3_lib.A5Decider) behind hosting/modal_direct_host.py's HTTP server
(same auth, keep-alive, one-write responses, /ping, /health, /decide, /shutdown). Used three ways:
  * on Modal's H100 through a direct tunnel: prep89/modal_ohs3_host.py imports build_decider() (CUDA graphs on for
    the 4B; the PRISM-X 2B and the cascade's 2B run eagerly);
  * locally on a GPU box (backend real, no graphs) for a smoke test;
  * in the CPU dry run (backend tiny / tiny_px):
      ../.venv/bin/python prep89/ohs3_serve.py --config prep89/dryrun/config_dryrun.json --model-key 4b \\
          --backend tiny --root prep89/dryrun/root --port 0 --token <24+ chars>
      the 2B:      --model-key 2b --backend tiny_px
      the cascade: --model-key cascade --backend tiny --small-backend tiny_px   (big model loaded first, then small)
Differences from hosting/modal_direct_host.Decider, all required by OHS-3: up to 255 options (OHS-3 has 40-option
tasks; the hosting parser stops at 26), definition cards on yes/no rows, the A5 2-view read, the pre-registered T,
"return_views" (raw / identity / identity-cal probabilities in the same response, for the one-run rule), per-call
token counts ("usage"), and the cascade (ohs3_lib.CascadeDecider: routing rule from the config).
"""
from __future__ import annotations

import argparse
import json
import sys
import threading
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import ohs3_lib as L  # noqa: E402


def build_decider(be, m, sync=None, lock=None):
    return L.A5Decider(be["dio"], be["model"], be["ro"], be["dev"], m["readout_choice"], m["T_primary"], m["T_single"],
                       sync=sync, lock=lock)


def build_cascade(cfg, be_small, be_big, sync=None, lock=None):
    """The served cascade from the pre-registered config (tau, w_big, route_on; never fitted here)."""
    import threading as th
    L.check_cascade(cfg)
    c = cfg["cascade"]
    lock = lock or th.Lock()
    small = build_decider(be_small, cfg["models"][c["small"]], sync=sync, lock=lock)
    big = build_decider(be_big, cfg["models"][c["big"]], sync=sync, lock=lock)
    return L.CascadeDecider(small, big, c["tau"], c["w_big"], c.get("route_on", "primary"), lock=lock)


def hosting_core():
    sys.path.insert(0, str(L.LEAN / "hosting"))
    import modal_direct_host as core  # local guards only; no Modal call
    return core


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument("--config", required=True)
    ap.add_argument("--model-key", default="4b", help="a model key, or 'cascade'")
    ap.add_argument("--backend", default="tiny", choices=["tiny", "tiny_px", "real"],
                    help="the model's backend (for the cascade: the big model's)")
    ap.add_argument("--small-backend", default="tiny_px", choices=["tiny", "tiny_px", "real"],
                    help="cascade only: the small model's backend")
    ap.add_argument("--root", default=None, help="tiny: the synthetic root (checked synthetic)")
    ap.add_argument("--host", default="127.0.0.1")
    ap.add_argument("--port", type=int, default=0)
    ap.add_argument("--token", required=True)
    ap.add_argument("--ready-file", default=None, help="write {url, health} here once serving")
    ap.add_argument("--max-s", type=int, default=3600)
    a = ap.parse_args(argv)
    if len(a.token) < 16:
        raise SystemExit("token: 16+ characters")
    import ohs3_backends as B
    cfg = L.load_config(a.config, require_complete=True, model_keys=[a.model_key])
    sysm = L.system(cfg, a.model_key)
    t0 = time.time()
    if sysm["kind"] == "cascade":
        mb, ms = cfg["models"][sysm["big"]], cfg["models"][sysm["small"]]
        be_big = B.load_backend(a.backend, mb, a.root)  # big FIRST: a later load must not uninstall the 2B's PRISM-X
        be_small = B.load_backend(a.small_backend, ms, a.root)
        dec = build_cascade(cfg, be_small, be_big)
        backend = {"small": be_small["info"], "big": be_big["info"],
                   "small_prism_x_after_both_loads": L.check_prism_x(ms, be_small["dio"], be_small["model"]),
                   "big_prism_x_after_both_loads": L.check_prism_x(mb, be_big["dio"], be_big["model"])}
        T = {"small": ms["T_primary"], "big": mb["T_primary"]}
        T1 = {"small": ms["T_single"], "big": mb["T_single"]}
    else:
        be = B.load_backend(a.backend, sysm, a.root)
        dec = build_decider(be, sysm)
        backend, T, T1 = be["info"], sysm["T_primary"], sysm["T_single"]
    core = hosting_core()
    info = {"model": sysm["name"], "system": sysm["kind"], "backend": backend, "readout": sysm["readout_choice"],
            "T": T, "T_single": T1, "config_sha256": cfg["_sha256"], "boot_s": round(time.time() - t0, 1),
            **({"cascade": {k: sysm[k] for k in ("tau", "w_big", "route_on", "small_name", "big_name")}}
               if sysm["kind"] == "cascade" else {})}
    stop = threading.Event()
    srv, st = core.make_server(a.port, a.token, dec.decide, lambda: info, stop.set, host=a.host)
    url = f"http://{a.host}:{srv.server_address[1]}"
    threading.Thread(target=srv.serve_forever, daemon=True).start()
    if a.ready_file:
        Path(a.ready_file).write_text(json.dumps({"url": url, "health": info}, default=str))
    L.blind_print(json.dumps({"url": url, "boot_s": info["boot_s"], "system": sysm["kind"]}))
    reason = core.wait_loop(stop, st, a.max_s, a.max_s)
    srv.shutdown()
    L.blind_print(json.dumps({"stop": reason, "served": st["n"], "errors": st["errors"], **dec.stats()}))


if __name__ == "__main__":
    main()
