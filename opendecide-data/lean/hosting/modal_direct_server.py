"""OPTIONAL step 3, the production form of the same server: a Modal Server (`@app.server`, modal >= 1.5; Modal's
low-latency HTTP path, formerly "Flash"): a proxy in routing_region talks straight to the container over a tunnel, with
no web-endpoint layer. Containers pinned to compute_region (us-east, next to this laptop and to the proxy).
NOT TESTED ON MODAL (the CPU test only checks that it imports and that Modal accepts the configuration locally).
Run it only after the tunnel test (modal_direct_host.py::main), and stop it right after.

  export OD_HOST_TOKEN=$(../.venv/bin/python -c 'import secrets; print(secrets.token_urlsafe(24))')
  MODAL_PROFILE=<acct> ../.venv/bin/modal deploy hosting/modal_direct_server.py      # prints the Server URL
  ../.venv/bin/python hosting/client_bench.py --url <URL> --token $OD_HOST_TOKEN --shutdown   # waits out the cold start
  MODAL_PROFILE=<acct> ../.venv/bin/modal app stop od-direct-server                  # always, even after --shutdown

Cost guards: min_containers=0 (nothing runs until the first request), max_containers=1, scaledown_window=120 s, and
the container exits itself on POST /shutdown or after OD_HOST_MAX_S seconds (default 1800). Same image, model, graphs
and HTTP API as modal_direct_host.py (its serving core is imported, not copied).
"""
import os
import sys
import threading
from pathlib import Path

import modal

sys.path.insert(0, str(Path(__file__).resolve().parent))
import modal_direct_host as core  # noqa: E402

TOKEN = os.environ.get("OD_HOST_TOKEN", "")
MAX_S = int(os.environ.get("OD_HOST_MAX_S", "1800"))
if modal.is_local() and len(TOKEN) < 16:
    raise SystemExit("set OD_HOST_TOKEN (16+ characters) before deploying: the Server URL is public")

app = modal.App("od-direct-server")


@app.server(image=core.image.add_local_python_source("modal_direct_host"), gpu="H100!", volumes={"/vol": core.vol},
            port=core.PORT, routing_region="us-east", compute_region="us-east", min_containers=0, max_containers=1,
            target_concurrency=1, scaledown_window=120, startup_timeout=900, unauthenticated=True,
            env={"OD_HOST_TOKEN": TOKEN, "OD_HOST_MAX_S": str(MAX_S)})
class DirectServer:
    @modal.enter()
    def start(self):
        dec, info = core.boot_gpu(core.MODEL, dict(core.GRAPH_CFG))
        stop = threading.Event()
        srv, st = core.make_server(core.PORT, os.environ["OD_HOST_TOKEN"], dec.decide, lambda: info, stop.set)
        threading.Thread(target=srv.serve_forever, daemon=True).start()

        def guard():  # /shutdown or the hard cap ends the container; with min_containers=0 nothing restarts it
            reason = core.wait_loop(stop, st, int(os.environ.get("OD_HOST_MAX_S", "1800")), 10 ** 9)
            print(f"stopping: {reason}; served {st['n']}; {core.json.dumps(dec.stats())}", flush=True)
            os._exit(0)

        threading.Thread(target=guard, daemon=True).start()
