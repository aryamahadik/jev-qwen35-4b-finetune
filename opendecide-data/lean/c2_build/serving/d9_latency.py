"""d9_latency: the D9 latency harness on the S1 served path (C2 lane P7; C_TRAIN_RECIPE D9, gate_c2 c7, symmetrise 10.2).

D9: p50 latency of the candidate <= 1.05 x C1's p50 on the SAME served path. Both are measured by this one tool:
one decision at a time (concurrency 1), through reads/fast_read.Reader (tokenise + POST /generate + parse + combine, on the
VM next to the server), over the SAME fixed request list (speed/workloads/S.jsonl, sha256-pinned by its manifest), the same
warm-up, the same number of calls, the same views. Per-call milliseconds are kept.

  measure --label C1|C2 --adapter DIR [--workload S] [--n 400] [--warmup 20] [--views 1|2] [--port P] [--flush] --out FILE
          one server, one model. --flush empties the server's prefix cache first (POST /flush_cache): refused on the
          production C1 server while it is serving (it is only legal in the window its owner opened).
  combine --c1 FILE --cand FILE --out logs/latency_c2.json
          refuses unless both records name the same path_sha256 (server args with the model path masked), workload, n, views,
          warm-up and flush setting, and the same GPU; writes the record gate_c2.latency_rule reads:
          {"cand_p50_ms", "ref_p50_ms", "served_path", ...}.

Which model was served: `measure` reads the server's own /server_info model_path and requires <model_path>/merge_manifest.json to
name the sha256 of --adapter (it must run on the machine that holds the model; a forgotten server swap stops here, before any
call or flush), and records served_model_path / served_manifest_sha256 / served_manifest_adapter_sha256; it re-reads the config
after the run and writes nothing if it changed. `combine` additionally requires the C1 record's adapter to be C1's pinned sha
(p7_common.C1_ADAPTER_SHA256), both records' manifest sha to equal their adapter sha, and the two records to differ in
served_model_path, served_manifest_sha256 and config_sha256 (one server measured twice is not C1 against a candidate).

"Single view" (C_TRAIN_RECIPE D9) is the default: --views 1 reads a choice question once, in the given order. --views 2 (the A5
readout of the dev gate: given + reversed) is also supported; the record states which. p50 = nearest rank s[int(q*n)] (the
convention of client_bench.py / bench_api.py). The ratio's 95% bootstrap interval is report-only.
"""
from __future__ import annotations

import argparse
import json
import random
import sys
import time
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import p7_common as C  # noqa: E402
import merge_parity as MP  # noqa: E402
import s1_pin  # noqa: E402

D9_MAX = 1.05
WORKLOAD_DIR = Path(__import__("os").environ.get("P7_WORKLOAD_DIR") or C.BUILD.parent / "speed/workloads")


def pct(xs: list, q: float) -> float:
    s = sorted(xs)
    return s[min(len(s) - 1, int(q * len(s)))]


def load_workload(name: str = "S", wl_dir: Path = WORKLOAD_DIR) -> tuple[list, str]:
    """The requests of speed/workloads/<name>.jsonl, refused unless the file's sha256 is the manifest's."""
    man = json.loads((wl_dir / "manifest.json").read_text())["workloads"][name]
    p = wl_dir / man["file"]
    sha = C.sha256_file(p)
    if sha != man["sha256"]:
        raise SystemExit(f"d9: {p}: sha256 {sha[:16]} != manifest {man['sha256'][:16]}")
    return [json.loads(l)["request"] for l in p.read_text().splitlines() if l.strip()], sha


def pick(requests: list, n: int, warmup: int, seed: int = 0) -> tuple[list, list]:
    """(warm-up requests, measured requests): the first warmup+n of a seeded shuffle; the two lists are disjoint."""
    if warmup + n > len(requests):
        raise SystemExit(f"d9: {warmup}+{n} calls asked, the workload has {len(requests)}")
    order = list(range(len(requests)))
    random.Random(seed).shuffle(order)
    sel = [requests[i] for i in order[:warmup + n]]
    return sel[:warmup], sel[warmup:]


def bootstrap_ratio(a: list, b: list, reps: int = 2000, seed: int = 0) -> list:
    """95% interval of p50(a)/p50(b) (independent resamples; report-only)."""
    rng = random.Random(seed)
    rs = []
    for _ in range(reps):
        ra = [a[rng.randrange(len(a))] for _ in a]
        rb = [b[rng.randrange(len(b))] for _ in b]
        rs.append(pct(ra, .5) / pct(rb, .5))
    rs.sort()
    return [round(rs[int(.025 * reps)], 4), round(rs[int(.975 * reps)], 4)]


def time_calls(read_one, rows: list) -> list:
    out = []
    for r in rows:
        t = time.perf_counter()
        read_one(r)
        out.append((time.perf_counter() - t) * 1000.0)
    return out


def summarise(ms: list) -> dict:
    return {"n": len(ms), "p50_ms": round(pct(ms, .5), 3), "p95_ms": round(pct(ms, .95), 3), "p99_ms": round(pct(ms, .99), 3),
            "mean_ms": round(sum(ms) / len(ms), 3), "min_ms": round(min(ms), 3), "max_ms": round(max(ms), 3)}


def measure(read_one, parse, requests: list, n: int, warmup: int, label: str, meta: dict, seed: int = 0) -> dict:
    """read_one(row) reads one decision; parse(request) -> decoder_io rows (one question each is expected)."""
    warm, meas = pick(requests, n, warmup, seed)
    rows_w = [r for q in warm for _, r in parse(q)]
    rows_m = []
    for q in meas:
        named = parse(q)
        if len(named) != 1:
            raise SystemExit("d9: a workload request must hold exactly one question (single decision)")
        rows_m.append(named[0][1])
    time_calls(read_one, rows_w)                      # warm-up: discarded
    ms = time_calls(read_one, rows_m)
    return {"label": label, **summarise(ms), "calls_ms": [round(x, 3) for x in ms], "warmup": len(rows_w),
            "workload_seed": seed, "utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()), **meta}


def combine(c1: dict, cand: dict, max_ratio: float = D9_MAX) -> dict:
    """The latency record for gate_c2.latency_rule. Refuses records that do not describe one served path."""
    must_equal = ("path_sha256", "workload", "workload_sha256", "n", "warmup", "views", "flushed", "gpu", "workload_seed")
    for k in must_equal:
        if c1.get(k) != cand.get(k) or c1.get(k) is None:
            raise SystemExit(f"d9: the two records differ (or lack) {k}: C1 {c1.get(k)!r} vs candidate {cand.get(k)!r}")
    if c1.get("label") != "C1" or cand.get("label") == "C1":
        raise SystemExit("d9: --c1 must be the C1 record and --cand a candidate record")
    if c1.get("adapter_sha256") == cand.get("adapter_sha256"):
        raise SystemExit("d9: both records are the same adapter")
    if c1.get("adapter_sha256") != C.C1_ADAPTER_SHA256:
        raise SystemExit(f"d9: the C1 record's adapter sha256 {str(c1.get('adapter_sha256'))[:16]} is not C1's {C.C1_ADAPTER_SHA256[:16]}")
    for r, who in ((c1, "C1"), (cand, "candidate")):          # each record must be tied to the model its server really served
        for k in ("served_model_path", "served_manifest_sha256", "config_sha256"):
            if not r.get(k):
                raise SystemExit(f"d9: the {who} record lacks {k} (it does not show which model was served)")
        if r.get("served_manifest_adapter_sha256") != r.get("adapter_sha256"):
            raise SystemExit(f"d9: the {who} record's served model was merged from a different adapter than the one it names")
    for k in ("served_model_path", "served_manifest_sha256", "config_sha256"):
        if c1[k] == cand[k]:
            raise SystemExit(f"d9: both records have the same {k}: one server (one model) was measured twice, not C1 against the candidate")
    if not c1.get("flushed"):
        print("d9: WARNING: neither read started from an empty prefix cache; the ratio carries cache-state noise", file=sys.stderr)
    ratio = cand["p50_ms"] / c1["p50_ms"]
    return {"cand_p50_ms": cand["p50_ms"], "ref_p50_ms": c1["p50_ms"], "served_path": f"sglang_s1_l4:{c1['path_sha256'][:16]}",
            "ratio": round(ratio, 4), "bar": max_ratio, "pass": ratio <= max_ratio + 1e-9,
            "ratio_ci95_bootstrap_report_only": bootstrap_ratio(cand["calls_ms"], c1["calls_ms"]),
            "views": c1["views"], "n": c1["n"], "warmup": c1["warmup"], "workload": c1["workload"], "workload_sha256": c1["workload_sha256"],
            "gpu": c1["gpu"], "path_sha256": c1["path_sha256"], "flushed": c1["flushed"],
            "cand": {k: cand[k] for k in ("label", "adapter_sha256", "p50_ms", "p95_ms", "p99_ms", "mean_ms", "utc", "config_sha256", "served_model_path", "served_manifest_sha256")},
            "ref": {k: c1[k] for k in ("label", "adapter_sha256", "p50_ms", "p95_ms", "p99_ms", "mean_ms", "utc", "config_sha256", "served_model_path", "served_manifest_sha256")},
            "p95_ratio_report_only": round(cand["p95_ms"] / c1["p95_ms"], 4),
            "note": "D9 = p50 only (C_TRAIN_RECIPE D9; gate_c2 c7). Same server args (path hash), same requests, same warm-up."}


def cmd_measure(a) -> int:
    if a.flush and a.port == C.PROD_PORT and not a.i_own_the_window:       # checked before anything is sent
        raise SystemExit("d9: --flush on the production port needs --i-own-the-window (its owner has stopped and restarted it)")
    fr = MP.load_fast_read()
    SH = s1_pin.sh_mod()
    for p in (a.adapter, a.out):
        C.refuse_path(p)
    requests, wsha = load_workload(a.workload, Path(a.workload_dir))
    adapter = Path(a.adapter).expanduser()
    adapter_sha = C.sha256_file(adapter / "adapter_model.safetensors")
    info = MP.fetch_server_info(a.port)
    ident = MP.served_identity(info, adapter_sha)         # refuses unless the server serves THIS adapter's merge (before any call)
    h = s1_pin.hashes(info, SH.SERVER_ENV)
    flushed = False
    if a.flush:
        import urllib.request
        req = urllib.request.Request(f"http://127.0.0.1:{a.port}/flush_cache", method="POST", data=b"")
        urllib.request.urlopen(req, timeout=120).read()
        flushed = True
    reader = fr.Reader(a.port, adapter, workers=1, chunk=1, views=a.views)
    from fastcore import readout as R
    parse = lambda q: R.parse_v1(q)  # noqa: E731
    gpu = None
    try:
        import subprocess
        gpu = subprocess.run(["nvidia-smi", "--query-gpu=name", "--format=csv,noheader"], capture_output=True, text=True).stdout.strip()
    except Exception:  # noqa: BLE001
        pass
    meta = {"workload": a.workload, "workload_sha256": wsha, "views": a.views, "flushed": flushed, "port": a.port, "gpu": gpu,
            "adapter_sha256": adapter_sha, **ident, **h,
            "server_version": info.get("version"), "fast_read_sha256": C.sha256_file(fr.__file__)}
    rec = measure(lambda row: reader._read_chunk([row]), parse, requests, a.n, a.warmup, a.label, meta, a.seed)
    after = s1_pin.hashes(MP.fetch_server_info(a.port), SH.SERVER_ENV)["config_sha256"]
    if after != h["config_sha256"]:
        raise SystemExit("d9: the server's config changed while it was being measured; record not written")
    Path(a.out).expanduser().write_text(json.dumps(rec, indent=1))
    print(json.dumps({k: rec[k] for k in ("label", "n", "p50_ms", "p95_ms", "p99_ms", "path_sha256")}))
    return 0


def cmd_combine(a) -> int:
    c1, cand = (json.loads(Path(p).read_text()) for p in (a.c1, a.cand))
    rec = combine(c1, cand)
    Path(a.out).write_text(json.dumps(rec, indent=1) + "\n")
    print(json.dumps({k: rec[k] for k in ("cand_p50_ms", "ref_p50_ms", "ratio", "pass", "served_path")}))
    return 0 if rec["pass"] else 2


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)
    m = sub.add_parser("measure")
    m.add_argument("--label", required=True)
    m.add_argument("--adapter", required=True, help="adapter dir of the model the server serves (tokenizer + train_meta)")
    m.add_argument("--workload", default="S")
    m.add_argument("--workload-dir", dest="workload_dir", default=str(WORKLOAD_DIR),
                   help="folder with S.jsonl + manifest.json (lean/speed/workloads; on the VM copy it and set this)")
    m.add_argument("--n", type=int, default=400)
    m.add_argument("--warmup", type=int, default=20)
    m.add_argument("--views", type=int, choices=(1, 2), default=1)
    m.add_argument("--seed", type=int, default=0)
    m.add_argument("--port", type=int, default=C.PROD_PORT)
    m.add_argument("--flush", action="store_true")
    m.add_argument("--i-own-the-window", dest="i_own_the_window", action="store_true")
    m.add_argument("--out", required=True)
    c = sub.add_parser("combine")
    c.add_argument("--c1", required=True)
    c.add_argument("--cand", required=True)
    c.add_argument("--out", default=str(C.BUILD / "logs/latency_c2.json"))
    a = ap.parse_args(argv)
    return {"measure": cmd_measure, "combine": cmd_combine}[a.cmd](a)


if __name__ == "__main__":
    sys.exit(main())
