"""client_bench: end-to-end latency from THIS laptop, our direct-hosted 4B vs Jev (via OpenRouter), on the SAME dev
requests, one at a time (concurrency 1), interleaved per request (ours/Jev, then Jev/ours) so network drift hits both
alike. NEW file; plain Python (httpx + typesafe_sdk), no Modal needed.

  ../.venv/bin/python hosting/client_bench.py --url URL --token TOKEN [--no-jev] [--limit 100] [--name NAME]
  ../.venv/bin/python hosting/client_bench.py --jev-only [--limit 100]   (Jev alone, e.g. at another time of day)
  ../.venv/bin/python hosting/client_bench.py --dry-run                   (no network: the request set and its shapes)
modal_direct_host.py::main imports run_bench() and calls it in-process.

Request set: data/dev.jsonl (150 calls; each = one state + 4 typed questions: 1 choice of 9 options + 3 yes/no). It is
the dev counterpart of the eval mix that bench_api.py sent (logs/bench_api.json): same banking77/clinc150 sources,
the same bundled state + questions format. 100 calls are picked by sha256(seed:call_id) (order-independent) and the
questions keep the seeded order of run_jev.py / bench_api.py. --mix eval replays the 515 bench_api.py requests exactly
(ours only by default). OHS splits are refused. Report-only: nothing is selected or tuned on these numbers; Jev outputs
are kept for this report only and are never used for training (Jev ToS).

Timing = perf_counter around one HTTP call including JSON encode/decode (as bench_api.py and run_jev.py), one
keep-alive connection per endpoint; TCP_NODELAY on ours; Jev through the typesafe SDK exactly as run_jev.py, with
retries off so no retry hides inside a timing. Percentiles: nearest rank s[int(q*n)] (bench_api.py, serve_tunnel.py).
Writes hosting/results/<name>/{summary.json, ours.jsonl, jev.jsonl, pings.jsonl}.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import random
import socket
import statistics
import sys
import time
from collections import Counter
from pathlib import Path

import httpx

HERE = Path(__file__).resolve().parent
LEAN = HERE.parent
DATA = LEAN / "data"
RESULTS = HERE / "results"
SEED = "od-direct-host-v1"
PARITY_REF = {"dev": LEAN / "preds_dev" / "q35_4b_pxE_parity.jsonl"}  # 4B-E, L4, no TTA, revision pinned, raw temps


def parity_ref(mix, model):
    """The stored L4 `od_gcp predict` dev read of the HOSTED adapter. 4B-E: its clean 30 Sep read (PARITY_REF). Any
    other adapter (e.g. --model q35_4b_main500k): preds_dev/<model>.jsonl, the 4B gate job's L4 read, when it exists
    and its meta is a predict read (has a load record). Otherwise 4B-E's file, flagged same_model False: a different
    model then FAILS the check, which is the safe direction (latency marked invalid, never wrongly valid)."""
    if mix not in PARITY_REF:
        return None, None
    if model and model != "q35_4b_pxE":
        p = LEAN / f"preds_{mix}" / f"{model}.jsonl"
        m = p.with_name(f"{model}.meta.json")
        try:
            ok = p.exists() and "load" in json.loads(m.read_text())
        except (OSError, ValueError):
            ok = False
        if ok:
            return p, True
        return PARITY_REF[mix], False
    return PARITY_REF[mix], True
# H100 vs L4 bars of the teacher-label check (FINETUNE_PLAN 3.2, logs/label_check_30sep.md): same model -> pass
PARITY_BARS = {"argmax_agree_min": 0.99, "mean_row_max_dp_max": 0.005, "max_dp_max": 0.05}
OPENROUTER_BASE = "https://openrouter.ai/api"
TIMING_HEADER_WORDS = ("time", "duration", "latency", "processing")  # any server-side timing Jev/OpenRouter expose
HISTORY = {  # earlier end-to-end numbers from this laptop (ms), for context in the summary
    "modal_web_endpoint_L4_v05_client_p50": 410.3, "modal_web_endpoint_L4_v05_server_p50": 123.1,
    "cpu_echo_web_endpoint_p50": 356.4, "cpu_echo_tunnel_unpinned_p50": 71.9,
    "v10_h100_graphs_tunnel_unpinned_client_p50": 114.6, "v10_h100_graphs_tunnel_unpinned_server_p50": 44.8,
    "pxE_h100_graphs_one_decision_compute_p50": 16.6, "jev_openrouter_p50_range": [187, 248],
}


# ------------------------------------------------------------------ request set

def build_requests(mix: str = "dev", n: int = 100, seed: str = SEED):
    """-> (requests, rows by id, sha256 of the request bodies). requests: [{"call_id", "row_map", "request"}]."""
    if "ohs" in mix.lower():
        raise SystemExit("refusing an OHS split: OHS is never used for tuning or benchmarking here")
    if mix == "eval":  # the exact 515 requests of bench_api.py, in file order
        rows = {json.loads(l)["id"]: json.loads(l) for l in open(DATA / "eval.jsonl")}
        calls = [json.loads(l) for l in open(DATA / "eval_calls.jsonl")]
    else:
        rows, by_call = {}, {}
        for line in open(DATA / f"{mix}.jsonl"):
            r = json.loads(line)
            rows[r["id"]] = r
            c = by_call.setdefault(r["call_id"], {"call_id": r["call_id"], "state": r["state"], "row_ids": []})
            if c["state"] != r["state"]:
                raise SystemExit(f"{mix}: call {r['call_id']} mixes states")
            c["row_ids"].append(r["id"])
        calls = sorted(by_call.values(), key=lambda c: hashlib.sha256(f"{seed}:{c['call_id']}".encode()).hexdigest())
    if n:
        calls = calls[:n]
    out = []
    for c in calls:
        rid = list(c["row_ids"])
        random.Random(c["call_id"]).shuffle(rid)  # the seeded question order of run_jev.py / bench_api.py
        qmap = {f"q{i}": r for i, r in enumerate(rid)}
        qs = {}
        for k, v in qmap.items():
            r = rows[v]
            if r.get("card"):
                raise SystemExit(f"{v}: carded rows are not part of this bench")
            qs[k] = {"type": r["qtype"], "instructions": r["instructions"],
                     **({"options": r["options"]} if r["qtype"] == "choice" else {})}
        out.append({"call_id": c["call_id"], "row_map": qmap, "request": {"state": c["state"], "questions": qs}})
    sha = hashlib.sha256(json.dumps([o["request"] for o in out], sort_keys=True).encode()).hexdigest()
    return out, rows, sha


# ------------------------------------------------------------------ helpers

def pct(xs, q):
    s = sorted(xs)
    return s[min(len(s) - 1, int(q * len(s)))] if s else None


def stats(xs) -> dict:
    xs = [x for x in xs if x is not None]
    if not xs:
        return {"n": 0}
    r = lambda v: round(v, 1)
    return {"n": len(xs), "p50": r(pct(xs, 0.5)), "p95": r(pct(xs, 0.95)), "mean": r(statistics.fmean(xs)),
            "min": r(min(xs)), "max": r(max(xs))}


def load_env():
    for envf in (LEAN.parent / ".env", LEAN / ".env"):  # same files as run_jev.py
        if envf.exists():
            for line in envf.read_text().splitlines():
                if "=" in line and not line.strip().startswith("#"):
                    k, v = line.split("=", 1)
                    os.environ.setdefault(k.strip(), v.strip().strip('"').strip("'"))


class Ours:
    def __init__(self, url, token, timeout=60.0):
        tr = httpx.HTTPTransport(retries=0, socket_options=[(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)])
        self.c = httpx.Client(base_url=url.rstrip("/"), transport=tr, timeout=timeout,
                              headers={"Authorization": f"Bearer {token}"})

    def decide(self, req):
        t = time.perf_counter()
        try:
            r = self.c.post("/decide", json=req)
            d = r.json()
        except Exception as e:  # noqa: BLE001
            return None, (time.perf_counter() - t) * 1000, f"{type(e).__name__}: {e}"[:300]
        ms = (time.perf_counter() - t) * 1000
        return (d, ms, None) if r.status_code == 200 else (None, ms, f"HTTP {r.status_code}: {str(d)[:300]}")

    def ping(self):
        t = time.perf_counter()
        r = self.c.get("/ping")
        ms = (time.perf_counter() - t) * 1000
        r.raise_for_status()
        return ms

    def close(self):
        self.c.close()


class Jev:
    """Jev through the typesafe SDK, as run_jev.py: a direct TYPESAFE_API_KEY wins, else OpenRouter's endpoint."""

    def __init__(self, base_url=None, model=None, timeout=60.0):
        from typesafe_sdk import RetryPolicy, TypeSafeClient
        load_env()
        if os.environ.get("TYPESAFE_API_KEY"):
            key, base, dm, self.route = os.environ["TYPESAFE_API_KEY"], None, "jev-1.13.0", "typesafe direct"
        elif os.environ.get("OPENROUTER_API_KEY"):
            key, base, dm, self.route = os.environ["OPENROUTER_API_KEY"], OPENROUTER_BASE, "jev-1.13", "openrouter"
        else:
            raise SystemExit("NO_KEY: set OPENROUTER_API_KEY (env or opendecide-data/.env) or pass --no-jev")
        base = base_url or os.environ.get("JEV_BASE_URL") or base
        if base_url or os.environ.get("JEV_BASE_URL"):
            self.route = f"override {base}"
        self.model = model or os.environ.get("JEV_MODEL") or dm
        self.client = TypeSafeClient(api_key=key, base_url=base, retry=RetryPolicy(max_retries=0), timeout=timeout)

    def decide(self, req):
        from typesafe_sdk import Choice, Noul
        qs = {k: Noul(instructions=q["instructions"]) if q["type"] == "noul"
              else Choice(instructions=q["instructions"], criteria={o: None for o in q["options"]})
              for k, q in req["questions"].items()}  # built before the clock starts, as run_jev.py
        t = time.perf_counter()
        try:
            res = self.client.system_one(state=req["state"], questions=qs, model=self.model)
        except Exception as e:  # noqa: BLE001
            return None, (time.perf_counter() - t) * 1000, f"{type(e).__name__}: {e}"[:300]
        return res, (time.perf_counter() - t) * 1000, None

    def close(self):
        try:
            self.client.close()
        except Exception:  # noqa: BLE001
            pass


def our_probs(ans, row):
    if ans["type"] == "noul":
        p = float(ans["noul"])
        return {"yes": p, "no": 1 - p}
    return {o: float(ans["probabilities"][o]) for o in row["options"]}


def jev_probs(ans, row):
    if row["qtype"] == "noul":
        p = float(ans["noul"])
        return {"yes": p, "no": 1 - p}
    pr = {k: float(v) for k, v in ans["probabilities"].items()}
    s = sum(pr.values()) or 1.0
    return {**{o: pr.get(o, 0.0) / s for o in row["options"]}, "_raw_sum": s}  # as run_jev.py


def cold_connect(url, token, k=3) -> dict:
    """First request on a NEW connection (DNS + TCP + TLS handshake + request): what keep-alive saves per call."""
    ms = []
    for _ in range(k):
        c = Ours(url, token)
        try:
            ms.append(c.ping())
        finally:
            c.close()
    return stats(ms)


def network_series(url, token, n=60, body=None) -> dict:
    """Network-only numbers on one keep-alive connection: GET /ping and POST /decide (echo server: no model)."""
    c = Ours(url, token)
    try:
        cold = cold_connect(url, token, 3)
        for _ in range(3):
            c.ping()
        pings, decs, errs = [], [], 0
        for _ in range(n):
            pings.append(c.ping())
            if body is not None:
                d, ms, err = c.decide(body)
                decs.append(ms if err is None else None)
                errs += err is not None
        return {"cold_connect_ms": cold, "ping_ms": stats(pings), "decide_ms": stats(decs), "errors": errs}
    finally:
        c.close()


def wait_ready(url, token, timeout=900):
    t0 = time.time()
    with httpx.Client(base_url=url.rstrip("/"), timeout=10, headers={"Authorization": f"Bearer {token}"}) as c:
        while True:
            try:
                r = c.get("/health")
                if r.status_code == 200:
                    return r.json()
                if r.status_code == 401:
                    raise SystemExit("401 from /health: wrong token")
            except httpx.HTTPError:
                pass
            if time.time() - t0 > timeout:
                raise SystemExit(f"{url} not ready after {timeout} s")
            time.sleep(2)


def shutdown(url, token):
    with httpx.Client(timeout=10, headers={"Authorization": f"Bearer {token}"}) as c:
        return c.post(url.rstrip("/") + "/shutdown").json()


def parity(recs, ref_path) -> dict:
    """Hosted probabilities vs the stored dev preds of the same adapter (another GPU): proves the server reads the model
    in the right layout/prompt. A failure makes the latency numbers meaningless (wrong model or prompt)."""
    ref = {}
    for line in open(ref_path):
        o = json.loads(line)
        ref[o["id"]] = o["probs"]
    rowmax, agree, dmax = [], 0, 0.0
    for rec in recs:
        for rid, p in (rec.get("probs") or {}).items():
            if rid not in ref:
                continue
            rp = ref[rid]
            keys = [k for k in rp if not k.startswith("_")]
            d = max(abs(p[k] - rp[k]) for k in keys)
            rowmax.append(d)
            dmax = max(dmax, d)
            agree += max(keys, key=p.get) == max(keys, key=rp.get)
    n = len(rowmax)
    if not n:
        return {"rows": 0, "pass": None}
    out = {"ref": str(ref_path.relative_to(LEAN)), "rows": n, "argmax_agree": round(agree / n, 4),
           "mean_row_max_dp": round(statistics.fmean(rowmax), 5), "max_dp": round(dmax, 5), "bars": PARITY_BARS}
    out["pass"] = (out["argmax_agree"] >= PARITY_BARS["argmax_agree_min"]
                   and out["mean_row_max_dp"] <= PARITY_BARS["mean_row_max_dp_max"]
                   and out["max_dp"] <= PARITY_BARS["max_dp_max"])
    return out


def accuracy(recs, rows, n_rows_sent) -> dict:
    """Report-only micro accuracy (ties and missing answers = wrong, as gate_dev.py). Too small to compare models."""
    ok, seen, by = 0, 0, Counter()
    for rec in recs:
        for rid, p in (rec.get("probs") or {}).items():
            r = rows[rid]
            seen += 1
            if r["qtype"] == "noul":
                good = p["yes"] != 0.5 and int(p["yes"] > 0.5) == int(r["gold"])
            else:
                vals = {o: p.get(o, 0.0) for o in r["options"]}
                top = [o for o, v in vals.items() if v == max(vals.values())]
                good = len(top) == 1 and top[0] == r["gold"]
            ok += good
            by[r["qtype"] + ("_ok" if good else "_bad")] += 1
    return {"rows_sent": n_rows_sent, "rows_answered": seen, "acc": round(ok / n_rows_sent, 4) if n_rows_sent else None,
            "by_type": dict(by), "note": "report-only; 100 calls cannot separate the models"}


# ------------------------------------------------------------------ the bench

def run_bench(url, token, mix="dev", n=100, jev=True, name=None, health=None, out_dir=None, jev_base_url=None,
              jev_model=None, warm=5, pings=50, log=print) -> dict:
    reqs, rows, sha = build_requests(mix, n)
    name = name or f"bench_{mix}_{time.strftime('%Y%m%d_%H%M%S', time.gmtime())}"
    out_dir = Path(out_dir) if out_dir else RESULTS / name
    out_dir.mkdir(parents=True, exist_ok=True)
    ours = Ours(url, token) if url else None
    jv = Jev(jev_base_url, jev_model) if jev else None
    if ours and health is None:
        health = ours.c.get("/health").json()
    n_rows = sum(len(r["row_map"]) for r in reqs)
    log(f"bench {name}: {len(reqs)} requests ({n_rows} decisions) from {mix}, sha256 {sha[:16]}; "
        f"ours={'yes' if ours else 'no'} jev={jv.route + ' ' + jv.model if jv else 'no'}")
    summary = {"name": name, "utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()), "mix": mix,
               "n_requests": len(reqs), "n_decisions": n_rows, "request_set_sha256": sha, "seed": SEED,
               "questions_per_request": dict(Counter(len(r["row_map"]) for r in reqs)), "concurrency": 1,
               "percentiles": "nearest rank s[int(q*n)] (bench_api.py convention)",
               "url_host": httpx.URL(url).host if url else None, "health": health,
               "jev_route": f"{jv.route} model={jv.model}" if jv else None, "history_ms": HISTORY,
               "do_not_train_on_jev_outputs": True}
    try:
        if ours:
            summary["ours_cold_connect_ms"] = cold_connect(url, token, 3)
        for item in reqs[:warm]:  # warm-up: not recorded (connections, server caches, OpenRouter routing)
            if ours:
                ours.decide(item["request"])
            if jv:
                jv.decide(item["request"])
        ping_a = [ours.ping() for _ in range(pings // 2)] if ours else []
        o_recs, j_recs = [], []
        t_loop = time.time()
        for i, item in enumerate(reqs):
            order = ("ours", "jev") if i % 2 == 0 else ("jev", "ours")
            for who in order:
                if who == "ours" and ours:
                    d, ms, err = ours.decide(item["request"])
                    rec = {"call_id": item["call_id"], "client_ms": ms, "error": err, "first": order[0] == "ours"}
                    if d:
                        rec.update(server_ms=d.get("server_ms"), timing=d.get("timing"), path=d.get("path"),
                                   shape=d.get("shape"),
                                   probs={rid: our_probs(d["answers"][k], rows[rid]) for k, rid in item["row_map"].items()})
                    o_recs.append(rec)
                elif who == "jev" and jv:
                    res, ms, err = jv.decide(item["request"])
                    rec = {"call_id": item["call_id"], "client_ms": ms, "error": err, "first": order[0] == "jev"}
                    if res is not None:
                        raw = res.__dict__.get("_raw")
                        rec.update(model=res.model, request_id=res.__dict__.get("_request_id"),
                                   timing_headers={k: v for k, v in (raw.headers.items() if raw is not None else [])
                                                   if any(w in k.lower() for w in TIMING_HEADER_WORDS)},
                                   usage=res.usage.model_dump() if res.usage else None,
                                   probs={rid: jev_probs(res.answers[k].model_dump(), rows[rid])
                                          for k, rid in item["row_map"].items() if k in res.answers})
                    j_recs.append(rec)
            if (i + 1) % 25 == 0:
                log(f"  {i + 1}/{len(reqs)} requests, {time.time() - t_loop:.0f} s")
        ping_b = [ours.ping() for _ in range(pings - pings // 2)] if ours else []
    finally:
        if ours:
            ours.close()
        if jv:
            jv.close()
    ok = lambda recs: [r for r in recs if r["error"] is None]
    if ours:
        good = ok(o_recs)
        summary["ours"] = {
            "client_ms": stats([r["client_ms"] for r in good]),
            "server_ms": stats([r["server_ms"] for r in good]),
            "model_ms": stats([(r.get("timing") or {}).get("model_ms") for r in good]),
            "network_and_http_ms": stats([r["client_ms"] - r["server_ms"] for r in good]),
            "client_ms_when_first": stats([r["client_ms"] for r in good if r["first"]]),
            "client_ms_when_second": stats([r["client_ms"] for r in good if not r["first"]]),
            "paths": dict(Counter(r.get("path") for r in good)),
            "shapes": dict(Counter(str(r.get("shape")) for r in good)),
            "errors": len(o_recs) - len(good), "ping_ms": stats(ping_a + ping_b),
            "ping_ms_before": stats(ping_a), "ping_ms_after": stats(ping_b),
            "accuracy_report_only": accuracy(o_recs, rows, n_rows)}
        ref, same = parity_ref(mix, (health or {}).get("model"))
        if ref is not None and ref.exists():
            pv = {**parity(o_recs, ref), "hosted_model": (health or {}).get("model"), "ref_is_hosted_model": same}
            if not same:  # no stored L4 read of this adapter: the check cannot vouch for it
                pv.update({"pass": False if pv.get("pass") is not None else None,
                           "note": "no stored L4 predict read of the hosted model in preds_dev/; compared with 4B-E"})
            summary["ours"]["parity_vs_stored_dev_preds"] = pv
    if jv:
        good = ok(j_recs)
        usage = [r["usage"]["input_tokens"] for r in good if r.get("usage") and r["usage"].get("input_tokens")]
        summary["jev"] = {"client_ms": stats([r["client_ms"] for r in good]),
                          "client_ms_when_first": stats([r["client_ms"] for r in good if r["first"]]),
                          "client_ms_when_second": stats([r["client_ms"] for r in good if not r["first"]]),
                          "errors": len(j_recs) - len(good), "error_examples": [r["error"] for r in j_recs if r["error"]][:3],
                          "models": dict(Counter(r.get("model") for r in good)),
                          "input_tokens_per_request_mean": round(statistics.fmean(usage), 1) if usage else None,
                          "accuracy_report_only": accuracy(j_recs, rows, n_rows)}
    if ours and jv and summary["ours"]["client_ms"]["n"] and summary["jev"]["client_ms"]["n"]:
        o, j = summary["ours"]["client_ms"], summary["jev"]["client_ms"]
        paired = [jr["client_ms"] - orr["client_ms"] for orr, jr in zip(o_recs, j_recs)
                  if orr["error"] is None and jr["error"] is None and orr["call_id"] == jr["call_id"]]
        summary["comparison"] = {"ours_p50_lt_jev_p50": o["p50"] < j["p50"], "ours_p95_lt_jev_p95": o["p95"] < j["p95"],
                                 "speedup_p50": round(j["p50"] / o["p50"], 2), "speedup_p95": round(j["p95"] / o["p95"], 2),
                                 "paired_jev_minus_ours_ms": stats(paired),
                                 "share_of_requests_ours_faster": round(sum(x > 0 for x in paired) / len(paired), 3)
                                 if paired else None}
    for fn, recs in (("ours.jsonl", o_recs if ours else []), ("jev.jsonl", j_recs if jv else [])):
        if recs:
            (out_dir / fn).write_text("".join(json.dumps(r) + "\n" for r in recs))
    if ours:
        (out_dir / "pings.jsonl").write_text(json.dumps({"before": ping_a, "after": ping_b}) + "\n")
    (out_dir / "summary.json").write_text(json.dumps(summary, indent=2))
    log(f"wrote {out_dir}/summary.json")
    return summary


def short_report(s) -> str:
    L = [f"== {s['name']}: {s['n_requests']} requests x {list(s['questions_per_request'])} questions, concurrency 1"]
    if "ours" in s:
        o = s["ours"]
        L.append(f"ours  client p50 {o['client_ms'].get('p50')} / p95 {o['client_ms'].get('p95')} ms | server p50 "
                 f"{o['server_ms'].get('p50')} (model {o['model_ms'].get('p50')}) | network+http p50 "
                 f"{o['network_and_http_ms'].get('p50')} | ping p50 {o['ping_ms'].get('p50')} | paths {o['paths']} | "
                 f"errors {o['errors']}")
        if "parity_vs_stored_dev_preds" in o:
            p = o["parity_vs_stored_dev_preds"]
            L.append(f"      parity vs stored dev preds: {'PASS' if p['pass'] else 'FAIL'} (argmax {p.get('argmax_agree')},"
                     f" mean max|dp| {p.get('mean_row_max_dp')}, max {p.get('max_dp')})")
    if "jev" in s:
        j = s["jev"]
        L.append(f"jev   client p50 {j['client_ms'].get('p50')} / p95 {j['client_ms'].get('p95')} ms | errors "
                 f"{j['errors']} | models {j['models']}")
    if "comparison" in s:
        c = s["comparison"]
        L.append(f"=> ours faster at p50: {c['ours_p50_lt_jev_p50']}, at p95: {c['ours_p95_lt_jev_p95']}; "
                 f"speed-up p50 x{c['speedup_p50']}, p95 x{c['speedup_p95']}; ours faster on "
                 f"{c['share_of_requests_ours_faster']} of paired requests")
    return "\n".join(L)


def dry_run(mix, n):
    """No network. The request set, and (if the local adapter copy exists) prompt tokens and padded graph shapes."""
    reqs, rows, sha = build_requests(mix, n)
    out = {"mix": mix, "n_requests": len(reqs), "n_decisions": sum(len(r["row_map"]) for r in reqs),
           "questions_per_request": dict(Counter(len(r["row_map"]) for r in reqs)), "sha256": sha,
           "qtypes": dict(Counter(rows[v]["qtype"] for r in reqs for v in r["row_map"].values())),
           "state_chars_p50": pct([len(r["request"]["state"]) for r in reqs], 0.5),
           "request_bytes_p50": pct([len(json.dumps(r["request"])) for r in reqs], 0.5)}
    adapter = LEAN.parent.parent / "backups/gcp_models/q35_4b_pxE"
    if (adapter / "tokenizer.json").exists():
        sys.path.insert(0, str(LEAN))
        import decoder_io as dio
        from transformers import AutoTokenizer
        info = dio.resolve_prompt([str(adapter)], "Qwen/Qwen3.5-4B", None, None, None)
        dio.LAYOUT, dio.STYLE = info["layout"], info["style"]
        tok = AutoTokenizer.from_pretrained(str(adapter))
        ro = dio.Readout.__new__(dio.Readout)  # prompt() only needs the tokenizer (skip the vocabulary scan)
        ro.tok = tok
        shapes, padded = [], []
        for r in reqs:
            ns = []
            for k, rid in r["row_map"].items():
                q = r["request"]["questions"][k]
                row = {"state": r["request"]["state"], "instructions": q["instructions"], "qtype": q["type"],
                       "options": q.get("options")}
                ns.append(len(tok(ro.prompt(row), add_special_tokens=False)["input_ids"]))
            B = next(b for b in (1, 2, 4, 8, 16) if b >= len(ns))
            L = -(-max(ns) // 64) * 64
            shapes.append((B, L))
            padded.append(B * L)
        # compute estimate: 16.6 ms for one decision at ~832 padded tokens (H100, graphs), scaled linearly (an upper-ish
        # bound: v10's eval mix measured 44.8 ms server p50 where linear scaling gives ~51 ms)
        out.update(layout=dio.LAYOUT, style=dio.STYLE, padded_shapes=dict(Counter(map(str, shapes))),
                   padded_tokens_p50=pct(padded, 0.5), padded_tokens_max=max(padded),
                   est_gpu_ms_p50_linear=round(16.6 * pct(padded, 0.5) / 832, 1))
    return out


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--url", help="our server (the tunnel URL modal_direct_host.py prints)")
    ap.add_argument("--token", help="the bearer token modal_direct_host.py prints")
    ap.add_argument("--mix", default="dev", help="dev (default) or eval (the 515 bench_api.py requests)")
    ap.add_argument("--limit", type=int, default=100, help="requests (0 = all)")
    ap.add_argument("--no-jev", action="store_true")
    ap.add_argument("--jev-only", action="store_true")
    ap.add_argument("--name", default=None)
    ap.add_argument("--pings", type=int, default=50)
    ap.add_argument("--warm", type=int, default=5)
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("--shutdown", action="store_true", help="POST /shutdown when done (ends the GPU bill)")
    a = ap.parse_args()
    if a.dry_run:
        print(json.dumps(dry_run(a.mix, a.limit), indent=2))
        return
    if a.jev_only:
        s = run_bench(None, None, mix=a.mix, n=a.limit, jev=True, name=a.name, warm=a.warm, pings=0)
    else:
        if not (a.url and a.token):
            ap.error("--url and --token are required (or --jev-only / --dry-run)")
        wait_ready(a.url, a.token)
        s = run_bench(a.url, a.token, mix=a.mix, n=a.limit, jev=not a.no_jev, name=a.name, warm=a.warm, pings=a.pings)
        if a.shutdown:
            print(shutdown(a.url, a.token))
    print(short_report(s))


if __name__ == "__main__":
    main()
