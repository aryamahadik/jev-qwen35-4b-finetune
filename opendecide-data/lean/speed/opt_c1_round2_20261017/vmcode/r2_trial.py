"""r2_trial.py: one L4 trial = parity (8,143) + batch-1 latency (320 calls x2) + c64 throughput (660 calls) + GPU busy.

Runs on od-l4b with ~/od/bin/python, PYTHONPATH=~/lean/hosting:~/lean:~/opt_r2. Reuses the 17 Oct harness (oc1.*,
copied read-only to ~/opt_r2/oc1) and fast_read's tokenization (oc1.items.prepare_cached = fastcore.readout =
decoder_io byte for byte). Talks to ONE server on --port (never 30000). Counts and numbers only; no row text is printed.

  r2_trial.py --name T0a --port 30010 --backend generate [--phases parity,lat,thr] [--parity-conc 16]
"""
from __future__ import annotations

import argparse
import json
import os
import pathlib
import sys
import time
from pathlib import Path

_orig_exists = pathlib.Path.exists


def _safe_exists(self, *a, **k):  # /root/lean is unreadable on the VM
    try:
        return _orig_exists(self, *a, **k)
    except PermissionError:
        return False


pathlib.Path.exists = _safe_exists

HOME = Path.home()
W = HOME / "opt_r2"
os.environ.setdefault("OC1_TMP", str(W / "cache"))
(W / "cache").mkdir(parents=True, exist_ok=True)
for p in (str(HOME / "lean" / "hosting"), str(HOME / "lean"), str(W)):
    if p not in sys.path:
        sys.path.insert(0, p)

from oc1 import common as C  # noqa: E402
from oc1 import items as I  # noqa: E402
from oc1 import measure as M  # noqa: E402
from oc1.backend import GenerateBackend, ScoreBackend  # noqa: E402

C1_DIR = HOME / "lean" / "models" / "q35_4b_main500k"
DATA = W / "data"


def load_preps(name: str, limit: int | None = None):
    items = C.read_jsonl(DATA / f"{name}.jsonl")
    R = I.readout_mod()
    tok, ro, info = I.load_c1(C1_DIR)
    preps = I.prepare_cached(name, items, R, ro, tok)
    return items, preps


def client_for(port: int):
    SH = I.sglang_host_mod()
    return SH.SGLangClient(f"http://127.0.0.1:{port}", 300.0)


def backend_for(kind: str, client):
    if kind == "generate":
        return GenerateBackend(client)
    if kind == "score":
        return ScoreBackend(client)
    raise SystemExit(f"backend {kind}")


def jdump(p, obj):
    p = Path(p)
    p.parent.mkdir(parents=True, exist_ok=True)
    tmp = p.with_suffix(p.suffix + ".tmp")
    tmp.write_text(json.dumps(obj, indent=1, default=str))
    os.replace(tmp, p)


def save_answers(path, answers: dict):
    with open(path, "w") as f:
        for k, v in answers.items():
            f.write(json.dumps({"id": k, **v}) + "\n")


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument("--name", required=True)
    ap.add_argument("--port", type=int, required=True)
    ap.add_argument("--backend", default="generate")
    ap.add_argument("--phases", default="parity,lat,thr")
    ap.add_argument("--parity-conc", type=int, default=16)
    ap.add_argument("--thr-conc", type=int, default=64)
    ap.add_argument("--extra-parity-conc", type=int, default=0, help="second parity pass at this concurrency (BF16 batching floor)")
    ap.add_argument("--lat-warm", type=int, default=20)
    ap.add_argument("--lat-n", type=int, default=320)
    ap.add_argument("--no-flush", action="store_true")
    a = ap.parse_args(argv)
    if a.port == 30000:
        raise SystemExit("refusing port 30000 (production)")
    out_dir = W / "results" / a.name
    out_dir.mkdir(parents=True, exist_ok=True)
    phases = a.phases.split(",")
    client = client_for(a.port)
    if not client.alive():
        raise SystemExit(f"server on {a.port} not healthy")
    info = client.server_info()
    jdump(out_dir / "server_info.json", info)
    backend = backend_for(a.backend, client)
    res = {"name": a.name, "port": a.port, "backend": a.backend, "utc_start": C.utc(), "phases": {}}
    t_all = time.time()
    flush = (lambda: M.flush(client)) if not a.no_flush else (lambda: None)

    with M.GpuSampler(0.5) as sampler:
        itemsN, prepsN = load_preps("N")
        # ---- warm-up (N decisions; discarded)
        for p in prepsN[:30]:
            backend.read(p, False)
        flush()
        if "parity" in phases:
            itemsP, prepsP = load_preps("P")
            t0 = time.time()
            r = M.parity_pass(backend, prepsP, conc=a.parity_conc, sampler=sampler)
            exp_tok = sum(p.n_tokens for p in prepsP)
            got_tok = None
            answers = r.pop("answers")
            save_answers(out_dir / "answers_P.jsonl", answers)
            r["answers_file"] = str(out_dir / "answers_P.jsonl")
            r["n_answers"] = len(answers)
            r["expected_tokens"] = exp_tok
            r["wall_s"] = round(time.time() - t0, 1)
            r["conc"] = a.parity_conc
            res["phases"]["parity"] = r
            print(f"[{a.name}] parity {len(answers)}/{len(prepsP)} in {r['wall_s']} s; missing {r['n_missing']}; "
                  f"gpu {r.get('gpu')}", flush=True)
            jdump(out_dir / "summary.json", res)
            if a.extra_parity_conc:
                flush()
                r2 = M.parity_pass(backend, prepsP, conc=a.extra_parity_conc, sampler=sampler)
                ans2 = r2.pop("answers")
                save_answers(out_dir / f"answers_P_c{a.extra_parity_conc}.jsonl", ans2)
                r2["n_answers"], r2["conc"] = len(ans2), a.extra_parity_conc
                res["phases"][f"parity_c{a.extra_parity_conc}"] = r2
                print(f"[{a.name}] parity c{a.extra_parity_conc}: {len(ans2)}/{len(prepsP)}; gpu {r2.get('gpu')}", flush=True)
                jdump(out_dir / "summary.json", res)
        if "lat" in phases:
            for rep in (1, 2):
                if rep == 2 and "thr" in phases:
                    pass
                flush()
                r = M.latency_batch1(backend, prepsN[: a.lat_n + a.lat_warm], warm=a.lat_warm, sampler=sampler)
                res["phases"][f"lat{rep}"] = r
                w = r["wall_ms"]
                print(f"[{a.name}] batch1 rep{rep}: n={r['n']} p50 {w.get('p50')} p95 {w.get('p95')} p99 {w.get('p99')} "
                      f"mean {w.get('mean')} ms; server_e2e p50 {r['server_e2e_ms'].get('p50')}; gpu {r.get('gpu')}", flush=True)
                jdump(out_dir / "summary.json", res)
                if rep == 1 and "thr" in phases:
                    flush()
                    t = M.throughput(backend, prepsN, conc_list=(a.thr_conc,), flush_between=not a.no_flush, client=client,
                                     sampler=sampler)
                    res["phases"]["thr"] = t
                    s = t[f"c{a.thr_conc}"]
                    print(f"[{a.name}] c{a.thr_conc}: ok {s['ok']}/{s['calls']} {s['decisions_per_h']} dec/h "
                          f"{s['tokens_per_s']} tok/s; gpu {s.get('gpu')}; cached {s.get('cached_token_share')}", flush=True)
                    jdump(out_dir / "summary.json", res)
        elif "thr" in phases:
            t = M.throughput(backend, prepsN, conc_list=(a.thr_conc,), flush_between=not a.no_flush, client=client,
                             sampler=sampler)
            res["phases"]["thr"] = t
            jdump(out_dir / "summary.json", res)
        if "prefix" in phases:
            itemsR, prepsR = load_preps("R")
            r = M.prefix_hit(backend, prepsR, client=client, conc=8, n=800)
            res["phases"]["prefix"] = r
            print(f"[{a.name}] R prefix: cached share {r['cached_token_share']}", flush=True)
    res["utc_end"] = C.utc()
    res["wall_s"] = round(time.time() - t_all, 1)
    jdump(out_dir / "summary.json", res)
    print(f"[{a.name}] done in {res['wall_s']} s", flush=True)


if __name__ == "__main__":
    main()
