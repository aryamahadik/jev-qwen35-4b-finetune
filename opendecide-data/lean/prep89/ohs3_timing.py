"""(c) End-to-end latency on the SAME OHS-3 inputs: our directly hosted endpoint vs Jev, per
prereg_drafts/speed_cost_definition.md (S1/S2). Run from the laptop (the client both systems are timed from).

  REAL (owner's GO; our endpoint up via prep89/modal_ohs3_host.py, which can also call this in-process):
    ../.venv/bin/python prep89/ohs3_timing.py --config prep89/ohs3_config.json --od-url URL --od-token TOKEN \\
        --name ohs3_timing --go [--scored-name q35_4b_pxE] [--od-preds-name q35_4b_pxE] [--jev-preds-tag jev_guard]
  --model-key picks the OpenDecide SYSTEM the endpoint serves: 4b (CUDA graphs), 2b (PRISM-X I, eager: no graphs), or
  cascade (2B -> 4B on one endpoint, routing rule from the config; timed end to end, routing included). Each system
  gets at most one OHS-3 pass through this harness (rule 4). On real OHS-3 it stops before any call unless the
  system's T (and for the cascade tau / w_big / route_on) equal their dev-only fit logs (ohs3_lib.require_fit_logs).
  DRY RUN: prep89/dryrun_ohs3.py runs it against local tiny-model servers (4B, PRISM-X 2B, cascade) and the fake Jev.

Protocol (speed definition, every point):
  * clock: time.perf_counter on this client, from just before the first attempt's request to the moment the full
    response is received and parsed; network, TLS, provider queueing and retries are inside;
  * retries: up to max_attempts per call (SDK retries OFF, so none hides inside an attempt), backoff 0.5 s, 1 s
    (counted); a call that fails every attempt is recorded AT THE TIMEOUT (30 s) and reported separately;
  * concurrency 1, interleaved call by call in a seeded order (sha256(seed:call_id)); who goes first alternates;
  * warm-up: 20 DEV calls to each system first (never OHS-3), not recorded;
  * same request content as the scored runs: Jev gets run_jev.py's own question() objects with the guard, in its
    seeded question order; we get the row fields our batch path reads (prompt identical to the scored read);
  * recorded per call: client ms, attempts, first-attempt ms, server_ms / model ms / path (ours), model id and request
    id (Jev), and the INPUT and OUTPUT TOKEN COUNTS of both systems: Jev's from its API usage field, ours from the
    server's count of the tokenizer encodes its reads made (identity read, all reads, padded; output 0: our readout
    generates nothing), plus per question (type, options, tokens): counts only; answers kept for parity / optional
    preds, never printed;
  * resumable: records.jsonl is append-only; a call already timed for a system is skipped;
  * refill (only for a side whose answers are SCORED from this run: --od-preds-name / --jev-preds-tag): calls that
    failed every attempt are re-sent after the timed pass (up to --refill-rounds, like run_jev.py's resume passes).
    Their timed record stays at the timeout in S1/S2; the refill records are flagged "refill" and never timed.
Summary (summary.json): p50/p95/p99 per system, the paired stratified bootstrap of Jev - OD for p50 and p95 (10,000,
default_rng(0)), the S1 verdict, per-task p50, input/output tokens of both systems (C1 Jev side, the 2-view token
multiplier on the OHS-3 mix, the length target of the C1 load test), OD-vs-scored parity (option D1 = L4_batch; for
the cascade also its components and the routed set), the cascade's routed share and latency by route, and the wall
time first -> last timed call (for C2).
Options that make this run produce SCORED files (owner decisions D1/D2 in ohs3_runbook.md):
  --od-preds-name NAME   D1 = served_h100: the served answers ARE the one OHS-3 run of NAME (rule 4 ledger)
  --jev-preds-tag TAG    D2 = run1_via_harness: write preds_ohs3/TAG(_raw).jsonl in run_jev.py's exact format
Blind: nothing prints item text.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import math
import os
import socket
import sys
import time
from collections import Counter, defaultdict
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import ohs3_lib as L  # noqa: E402

S1_DEFAULT = "p50 CI (Jev - OD) entirely above 0 AND p95 point estimate lower"  # the only rule coded below
PARITY_BARS = {"argmax_agree_min": 0.99, "mean_row_max_dp_max": 0.005, "max_dp_max": 0.05}  # client_bench.py
OPENROUTER_BASE = "https://openrouter.ai/api"


# ------------------------------------------------------------------ clients

class OD:
    def __init__(self, url, token, timeout):
        import httpx
        tr = httpx.HTTPTransport(retries=0, socket_options=[(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)])
        self.c = httpx.Client(base_url=url.rstrip("/"), transport=tr, timeout=timeout,
                              headers={"Authorization": f"Bearer {token}"})

    def send(self, req):
        r = self.c.post("/decide", json=req)
        d = r.json()
        if r.status_code != 200:
            raise RuntimeError(f"HTTP {r.status_code}")
        return d

    def ping(self):
        t = time.perf_counter()
        self.c.get("/ping").raise_for_status()
        return (time.perf_counter() - t) * 1000

    def health(self):
        r = self.c.get("/health")
        r.raise_for_status()
        return r.json()

    def close(self):
        self.c.close()


class Jev:
    def __init__(self, timeout, fake_url=None, real=False):
        from typesafe_sdk import RetryPolicy, TypeSafeClient
        if fake_url:
            key, base, self.route = "dryrun-fake-key", fake_url, f"fake {fake_url}"
        else:
            for envf in (L.LEAN.parent / ".env", L.LEAN / ".env"):  # the files run_jev.py reads; never printed
                if envf.exists():
                    for line in envf.read_text().splitlines():
                        if "=" in line and not line.strip().startswith("#"):
                            k, v = line.split("=", 1)
                            os.environ.setdefault(k.strip(), v.strip().strip('"').strip("'"))
            key = os.environ.get("OPENROUTER_API_KEY")
            if not key:
                raise SystemExit("NO_KEY: OPENROUTER_API_KEY")
            base, self.route = OPENROUTER_BASE, "openrouter"
        self.model = L.JEV_REQUEST_MODEL_OPENROUTER
        self.client = TypeSafeClient(api_key=key, base_url=base, retry=RetryPolicy(max_retries=0), timeout=timeout)

    def send(self, state, qs):
        return self.client.system_one(state=state, questions=qs, model=self.model)

    def close(self):
        try:
            self.client.close()
        except Exception:  # noqa: BLE001
            pass


def timed(fn, max_attempts, timeout_s):
    """(result or None, record): first-attempt start -> success end; failures recorded at the timeout."""
    t0 = time.perf_counter()
    errs, first_ms, res = [], None, None
    for att in range(1, max_attempts + 1):
        ta = time.perf_counter()
        try:
            res = fn()
            first_ms = (time.perf_counter() - ta) * 1000
            break
        except Exception as e:  # noqa: BLE001
            errs.append(type(e).__name__ + (f": {getattr(e, 'status_code', '')}" if hasattr(e, "status_code") else ""))
            if att < max_attempts:
                time.sleep(0.5 * 2 ** (att - 1))
    ok = res is not None
    return res, {"attempts": att, "failed": not ok,
                 "client_ms": (time.perf_counter() - t0) * 1000 if ok else timeout_s * 1000.0,
                 "success_attempt_ms": first_ms, "errors": errs[:5]}


# ------------------------------------------------------------------ helpers

def stats(xs):
    xs = [x for x in xs if x is not None]
    if not xs:
        return {"n": 0}
    return {"n": len(xs), "p50": round(L.pct(xs, 0.5), 2), "p95": round(L.pct(xs, 0.95), 2),
            "p99": round(L.pct(xs, 0.99), 2), "mean": round(sum(xs) / len(xs), 2), "min": round(min(xs), 2),
            "max": round(max(xs), 2)}


def dev_warm_calls(n):
    rows, by = {}, {}
    for r in L.read_jsonl(L.LEAN / "data" / "dev.jsonl"):
        rows[r["id"]] = r
        by.setdefault(r["call_id"], {"call_id": r["call_id"], "state": r["state"], "row_ids": []})["row_ids"].append(r["id"])
    calls = sorted(by.values(), key=lambda c: hashlib.sha256(f"warm:{c['call_id']}".encode()).hexdigest())[:n]
    return calls, rows


def parity(od_ans, ref_path, view):
    """Served probabilities (view "raw" = pre-T readout, or "final" = served answer) vs the scored preds file."""
    ref = {o["id"]: o["probs"] for o in L.read_jsonl(ref_path)}
    rowmax, agree, dmax = [], 0, 0.0
    for rid, a in od_ans.items():
        if rid not in ref:
            continue
        p = a[view]
        rp = ref[rid]
        keys = [k for k in rp if not k.startswith("_")]
        d = max(abs(p[k] - rp[k]) for k in keys)
        rowmax.append(d)
        dmax = max(dmax, d)
        agree += max(keys, key=p.get) == max(keys, key=rp.get)
    n = len(rowmax)
    if not n:
        return {"rows": 0, "pass": None}
    out = {"ref": ref_path.name, "view": view, "rows": n, "argmax_agree": round(agree / n, 5),
           "mean_row_max_dp": round(sum(rowmax) / n, 7), "max_dp": round(dmax, 7), "bars": PARITY_BARS}
    out["pass"] = (out["argmax_agree"] >= PARITY_BARS["argmax_agree_min"]
                   and out["mean_row_max_dp"] <= PARITY_BARS["mean_row_max_dp_max"]
                   and out["max_dp"] <= PARITY_BARS["max_dp_max"])
    return out


def our_probs(ans, row):
    if row["qtype"] == "noul":
        p = float(ans["noul"])
        return {"yes": p, "no": 1 - p}
    return {o: float(ans["probabilities"][o]) for o in row["options"]}


# ------------------------------------------------------------------ the run

def od_pass_systems(tdir, exclude=None) -> dict:
    """{timing dir name: system name} of every earlier OD timing pass (records with who == "od"); the system comes from
    the records (field "system") or the dir's run settings; unknown = None (treated as the same system: refuse)."""
    out = {}
    for p in sorted(Path(tdir).glob("*/records.jsonl")):
        if p.parent.name == exclude:
            continue
        recs = [r for r in L.read_jsonl(p) if r.get("who") == "od"]
        if not recs:
            continue
        names = {r.get("system") for r in recs if r.get("system")}
        if not names:
            for sf in p.parent.glob("run_*.json"):
                names.add(json.loads(sf.read_text()).get("model"))
        out[p.parent.name] = sorted(n for n in names if n) or None
    return out


def check_decisions(a, cfg, m, root):
    """REAL OHS-3 only, before any call: the flags must match the pre-registered D1/D2 (config.decisions), and
    each OpenDecide system (4b, 2b, cascade) gets at most one OHS-3 pass through this harness (rule 4; resume it under
    the same --name). With D2 = run1_via_harness only the headline system's pass (speed.headline_system) collects the
    scored Jev run 1; any other system's pass may time against an unscored Jev pass or none (--no-jev)."""
    d1, d2 = cfg["decisions"]["od_scored_run"], cfg["decisions"]["jev_timing"]
    head = (cfg.get("speed") or {}).get("headline_system", "4b")
    is_head = getattr(a, "model_key", "4b") == head
    pd = root / f"preds_{L.SPLIT}"
    if a.od_url:
        if d1 == "served_h100":
            if a.od_preds_name != m["name"] or a.scored_name:
                raise SystemExit(f"D1 = served_h100: this pass IS the scored run: --od-preds-name {m['name']}, "
                                 "no --scored-name")
            import ohs3_od_run as R
            if L.completed_runs(root, m["name"]) or any(p.exists() for p in R.out_files(pd, m["name"]).values()):
                raise SystemExit(f"STOP (rule 4): {m['name']} already has an OHS-3 run")
        else:  # L4_batch: the scored run exists; this replay is for timing and the parity check only
            if a.od_preds_name or a.scored_name != m["name"]:
                raise SystemExit(f"D1 = L4_batch: --scored-name {m['name']} (parity only), no --od-preds-name")
            if not (pd / f"{m['name']}_cal.jsonl").exists():
                raise SystemExit("D1 = L4_batch: copy the completed L4 run to preds_ohs3/ before the H100 replay")
        tdir = root / "logs" / "ohs3" / "timing"
        others = sorted(d for d, names in od_pass_systems(tdir, exclude=a.name).items()
                        if names is None or m["name"] in names)
        if others:
            raise SystemExit(f"STOP (rule 4): {m['name']} already had an OHS-3 timing pass ({others}); resume it with "
                             "the same --name")
    if not a.no_jev:
        if a.jev_preds_tag and not is_head:
            raise SystemExit(f"only the headline system's pass ({head}) may collect a scored Jev run; time "
                             f"{a.model_key} against an unscored Jev pass (no --jev-preds-tag) or --no-jev")
        if d2 == "run1_via_harness" and a.od_url and is_head and a.jev_preds_tag != "jev_guard":
            raise SystemExit("D2 = run1_via_harness: Jev run 1 is collected here: --jev-preds-tag jev_guard")
        if d2 == "extra_pass" and a.jev_preds_tag:
            raise SystemExit("D2 = extra_pass: both scored Jev runs come from run_jev.py; no --jev-preds-tag")
        if a.jev_preds_tag and any((pd / f"{a.jev_preds_tag}{s}.jsonl").exists() for s in ("", "_raw")):
            raise SystemExit(f"preds_ohs3/{a.jev_preds_tag}(_raw).jsonl exist: refusing a second scored Jev run")


def run(a):
    root = Path(a.root).resolve()
    real = L.is_real_ohs3(root)
    cfg = L.load_config(a.config, require_complete=True, model_keys=[a.model_key])
    m, sp = L.system(cfg, a.model_key), cfg["speed"]
    if real:
        if not a.go:
            raise SystemExit("REAL OHS-3 timing: needs --go (owner's GO)")
        if a.fake_jev_url:
            raise SystemExit("--fake-jev-url is for the synthetic dry run only")
        if a.limit:
            raise SystemExit("--limit is for the dry run only: any partial pass on real OHS-3 is part of the one run")
        L.require_frozen(root)
        check_decisions(a, cfg, m, root)
        L.require_fit_logs(cfg, [a.model_key], rehash=True)  # T (and the cascade rule) == their dev-only fit logs
    else:
        L.require_synthetic(root)
    timeout_s, max_att = float(sp["timeout_s"]), int(sp["max_attempts"])
    rows = {r["id"]: r for r in L.read_jsonl(root / "data" / f"{L.SPLIT}.jsonl")}
    if real:
        for r in rows.values():
            r.pop("gold", None)  # blind: timing never needs gold
    calls = L.read_jsonl(root / "data" / f"{L.SPLIT}_calls.jsonl")
    task_of = {c["call_id"]: rows[c["row_ids"][0]]["source"] for c in calls}
    seed = sp["interleave_seed"]
    order = sorted(calls, key=lambda c: hashlib.sha256(f"{seed}:{c['call_id']}".encode()).hexdigest())
    if a.limit:  # stratified by task, the first share of each task in the seeded order
        by = defaultdict(list)
        for c in order:
            by[task_of[c["call_id"]]].append(c)
        keep = set()
        for t, cs in by.items():
            keep |= {c["call_id"] for c in cs[:max(1, math.ceil(a.limit * len(cs) / len(order)))]}
        order = [c for c in order if c["call_id"] in keep]
    out = root / "logs" / "ohs3" / "timing" / a.name
    out.mkdir(parents=True, exist_ok=True)
    recf, odf, jvf = out / "records.jsonl", out / "od_answers.jsonl", out / "jev_raw.jsonl"
    done = set()
    if recf.exists():  # the timed (interleaved) pass only; refill records never count as timed
        done = {(r["who"], r["call_id"]) for r in L.read_jsonl(recf) if not r.get("refill")}
    settings = {"name": a.name, "config_sha256": cfg["_sha256"], "model": m["name"], "system": m["key"],
                "kind": m["kind"], "readout": m["readout_choice"],
                "timeout_s": timeout_s, "max_attempts": max_att, "concurrency": 1, "seed": seed, "calls": len(order),
                "limit": a.limit, "od_url_host": a.od_url.split("//")[-1].split("/")[0] if a.od_url else None,
                "jev_route": "fake" if a.fake_jev_url else "openrouter", "real": real, "started_utc": L.utc(),
                "resumed_records": len(done)}
    od = OD(a.od_url, a.od_token, timeout_s) if a.od_url else None
    if od:  # the endpoint must serve THIS system under THIS config (its /health says so)
        h = od.health()
        settings["endpoint_health"] = {k: h.get(k) for k in ("model", "system", "readout", "config_sha256", "cascade",
                                                              "boot_s", "graphs", "path", "prism_x", "region", "gpu")}
        bad = {k: (h.get(k), v) for k, v in (("model", m["name"]), ("config_sha256", cfg["_sha256"])) if h.get(k) != v}
        if bad:
            od.close()
            raise SystemExit(f"the endpoint does not serve the pre-registered system/config: {bad}")
    (out / f"run_{int(time.time())}.json").write_text(json.dumps(settings, indent=1, default=str))
    jv = Jev(timeout_s, a.fake_jev_url, real) if not a.no_jev else None
    if a.jev_preds_tag and not a.jev_preds_tag.endswith("guard"):
        raise SystemExit("PREREG_OHS3 rule 2: Jev gets the guard; a scored tag must end with 'guard'")
    question, rj_sha = L.run_jev_question_fn(a.jev_preds_tag or cfg["jev"]["timing_tag"])
    L.blind_print(f"timing {a.name}: {len(order)} calls, OD={'yes' if od else 'no'} Jev={jv.route if jv else 'no'}, "
                  f"resume: {len(done)} records done; run_jev.py sha256 {rj_sha[:16]}")
    pings = {"before": [], "after": []}
    try:
        # ---- warm-up on DEV inputs (never OHS-3), not recorded
        wc, wrows = dev_warm_calls(int(sp["warmup_dev_calls"]))
        wq, _ = L.run_jev_question_fn(cfg["jev"]["timing_tag"])
        werr = Counter()
        for c in wc:
            if od:
                _, rec = timed(lambda: od.send(L.od_request(c, wrows)[0]), 1, timeout_s)
                werr["od"] += rec["failed"]
            if jv:
                qm = L.run_jev_qmap(c)
                qs = {k: wq(wrows[v]) for k, v in qm.items()}
                _, rec = timed(lambda: jv.send(c["state"], qs), 1, timeout_s)
                werr["jev"] += rec["failed"]
        L.blind_print(f"warm-up: {len(wc)} dev calls each, failures {dict(werr)}")
        if od:
            pings["before"] = [od.ping() for _ in range(20)]
        t_first = t_last = None
        n_new = 0
        def one(who, c, first, refill=0):
            """Send one call to one system (timed), log its answers and its record."""
            cid = c["call_id"]
            if who == "od":
                req, qmap = L.od_request(c, rows)  # built before the clock starts
                res, rec = timed(lambda: od.send(req), max_att, timeout_s)
                if res is not None:
                    rec.update(server_ms=res.get("server_ms"), timing=res.get("timing"), path=res.get("path"),
                               shape=res.get("shape"), **od_usage_fields(res, qmap, rows))
                    ans = {}
                    for k, rid in qmap.items():
                        v = res["answers"][k].get("views") or {}
                        ans[rid] = {"final": our_probs(res["answers"][k], rows[rid]), **v}
                    with open(odf, "a") as f:
                        f.write(json.dumps({"call_id": cid, "answers": ans}) + "\n")
            else:
                qmap = L.run_jev_qmap(c)
                qs = {k: question(rows[v]) for k, v in qmap.items()}  # built before the clock starts
                res, rec = timed(lambda: jv.send(c["state"], qs), max_att, timeout_s)
                raw = {"call_id": cid, "latency_ms": rec["client_ms"] if res is not None else None,
                       "model": getattr(res, "model", None) if res is not None else None, "row_map": qmap,
                       "answers": {k: v.model_dump() for k, v in res.answers.items()} if res is not None else None,
                       "error": None if res is not None else "; ".join(rec["errors"])}
                with open(jvf, "a") as f:
                    f.write(json.dumps(raw) + "\n")
                if res is not None:
                    u = getattr(res, "usage", None)
                    ud = u.model_dump() if u is not None else None
                    rec.update(model=res.model, usage=ud, request_id=res.__dict__.get("_request_id"),
                               input_tokens=(ud or {}).get("input_tokens"), output_tokens=(ud or {}).get("output_tokens"))
            rec.update(who=who, call_id=cid, task=task_of[cid], first=first, utc=L.utc(),
                       system=m["name"] if who == "od" else "jev")
            if refill:
                rec["refill"] = refill
            with open(recf, "a") as f:
                f.write(json.dumps(rec) + "\n")
            return rec

        for i, c in enumerate(order):
            cid = c["call_id"]
            sides = ("od", "jev") if i % 2 == 0 else ("jev", "od")
            for who in sides:
                if (who, cid) in done or (who == "od" and not od) or (who == "jev" and not jv):
                    continue
                one(who, c, sides[0] == who)
                now = time.time()
                t_first = t_first or now
                t_last = now
                n_new += 1
            if (i + 1) % 200 == 0:
                L.blind_print(f"  {i + 1}/{len(order)} calls")
        # ---- refill: a call that failed every attempt keeps its timed record (at the timeout, counted in S1/S2), but
        # a system whose answers are SCORED from this run (D1 served_h100: od; D2 run1_via_harness: jev) must answer
        # every call, as run_jev.py's resume passes do. Refill records carry "refill" and are never timed.
        sides_scored = [w for w, on in (("od", bool(a.od_preds_name and od)), ("jev", bool(a.jev_preds_tag and jv))) if on]
        for rnd in range(1, int(a.refill_rounds) + 1):
            ok = {(r["who"], r["call_id"]) for r in L.read_jsonl(recf) if not r["failed"]} if recf.exists() else set()
            todo = [(w, c) for w in sides_scored for c in order if (w, c["call_id"]) not in ok]
            if not todo:
                break
            L.blind_print(f"refill round {rnd}: {len(todo)} unanswered calls ({dict(Counter(w for w, _ in todo))})")
            for w, c in todo:
                time.sleep(2.0 ** rnd)  # spaced out: these follow failures
                one(w, c, False, refill=rnd)
        if od:
            pings["after"] = [od.ping() for _ in range(20)]
    finally:
        if od:
            od.close()
        if jv:
            jv.close()
    return summarize(a, root, cfg, m, order, task_of, rows, out, pings, real)


def od_usage_fields(res, qmap, rows):
    """Token counts of one served call (counts only, no text): the totals of the server's usage (every forward pass of
    the call: identity read, reversed read on 2-view rows, the big model's reads on routed cascade rows) and per
    question, in the request order, [type, number of options, identity-read tokens, all-read tokens]: the length
    target of the C1 load test (load_test_c1.py)."""
    u = res.get("usage") or {}
    qs = []
    for k, rid in qmap.items():
        au = res["answers"][k].get("usage") or {}
        r = rows[rid]
        qs.append([r["qtype"], len(r["options"] or []), au.get("input_tokens_first_view"), au.get("input_tokens")])
    out = {"input_tokens": u.get("input_tokens"), "output_tokens": u.get("output_tokens"),
           "input_tokens_first_view": u.get("input_tokens_first_view"), "forward_passes": u.get("forward_passes"),
           "padded_tokens": u.get("padded_tokens"), "qs": qs}
    if "routed_rows" in u:
        out.update(routed_rows=u["routed_rows"], small_input_tokens=u.get("small_input_tokens"),
                   big_input_tokens=u.get("big_input_tokens"))
    return out


def token_block(d, task_of, fields):
    """Per-call token counts of the answered timed calls: totals, mean and percentiles per field, per-task means, and
    complete = every answered call has an input-token count."""
    ok = [r for r in d.values() if not r["failed"]]
    out = {"calls_answered": len(ok)}
    for f in fields:
        xs = [r[f] for r in ok if r.get(f) is not None]
        out[f] = {"calls_with_count": len(xs), "total": sum(xs), **stats(xs)}
    by = defaultdict(list)
    for r in ok:
        if r.get("input_tokens") is not None:
            by[task_of[r["call_id"]]].append(r["input_tokens"])
    out["input_tokens_mean_by_task"] = {t: round(sum(v) / len(v), 1) for t, v in sorted(by.items())}
    if "input_tokens" in fields:  # false when some answered call carried no count (e.g. a Jev route without usage)
        out["complete"] = out["input_tokens"]["calls_with_count"] == out["calls_answered"]
    return out


def summarize(a, root, cfg, m, order, task_of, rows, out, pings, real):
    recs = L.read_jsonl(out / "records.jsonl")
    want = {c["call_id"] for c in order}
    timed_rec, refilled = {}, Counter()
    for r in recs:
        if r["call_id"] not in want:
            continue
        if r.get("refill"):  # answers only (scored systems); never timed
            refilled[(r["who"], r["call_id"], not r["failed"])] += 1
            continue
        timed_rec.setdefault((r["who"], r["call_id"]), r)  # the one interleaved, timed send of this call
    od = {cid: r for (w, cid), r in timed_rec.items() if w == "od"}
    jv = {cid: r for (w, cid), r in timed_rec.items() if w == "jev"}
    S = {"name": a.name, "config_sha256": cfg["_sha256"], "model": m["name"], "system": m["key"], "kind": m["kind"],
         "readout": m["readout_choice"], "calls_planned": len(order), "real": real,
         "definition": "prereg_drafts/speed_cost_definition.md S1/S2", "do_not_train_on_jev_outputs": True}
    for who, d in (("od", od), ("jev", jv)):
        if not d:
            continue
        S[who] = {"client_ms": stats([r["client_ms"] for r in d.values()]),
                  "client_ms_success_only": stats([r["client_ms"] for r in d.values() if not r["failed"]]),
                  "failed_calls": sum(r["failed"] for r in d.values()),
                  "retried_calls": sum(r["attempts"] > 1 and not r["failed"] for r in d.values()),
                  "calls_timed": len(d),
                  "client_ms_when_first": stats([r["client_ms"] for r in d.values() if r["first"]]),
                  "client_ms_when_second": stats([r["client_ms"] for r in d.values() if not r["first"]]),
                  "refill_calls_answered": len({c for (w, c, ok) in refilled if w == who and ok}),
                  "refill_note": "failed calls stay in the percentiles at the timeout; refill answers are scored only"}
    if od:
        S["od"].update(server_ms=stats([r.get("server_ms") for r in od.values() if not r["failed"]]),
                       model_ms=stats([(r.get("timing") or {}).get("model_ms") for r in od.values() if not r["failed"]]),
                       network_http_ms=stats([r["client_ms"] - r["server_ms"] for r in od.values()
                                              if not r["failed"] and r.get("server_ms") is not None]),
                       reads_per_call=dict(Counter((r.get("timing") or {}).get("reads") for r in od.values())),
                       paths=dict(Counter(r.get("path") for r in od.values())),
                       ping_ms_before=stats(pings["before"]), ping_ms_after=stats(pings["after"]))
        tb = token_block(od, task_of, ("input_tokens", "output_tokens", "input_tokens_first_view", "forward_passes",
                                       "padded_tokens"))
        f, t = tb["input_tokens_first_view"]["total"], tb["input_tokens"]["total"]
        tb["all_reads_over_first_view"] = round(t / f, 4) if f else None
        tb["note"] = ("our counts: tokenizer encodes of the served reads (unpadded, add_special_tokens=False); output 0 "
                      "(the readout reads the next-token distribution, it generates nothing)")
        S["od"]["tokens"] = tb
        if m["kind"] == "cascade":
            ok = [r for r in od.values() if not r["failed"] and r.get("routed_rows") is not None]
            n_rows = sum(len(r.get("qs") or []) for r in ok)
            rt = [r for r in ok if r["routed_rows"] > 0]
            S["od"]["cascade"] = {
                "routed_rows": sum(r["routed_rows"] for r in ok), "rows": n_rows,
                "routed_share": round(sum(r["routed_rows"] for r in ok) / n_rows, 4) if n_rows else None,
                "client_ms_routed_calls": stats([r["client_ms"] for r in rt]),
                "client_ms_not_routed_calls": stats([r["client_ms"] for r in ok if r["routed_rows"] == 0]),
                "small_ms": stats([(r.get("timing") or {}).get("small_ms") for r in ok]),
                "big_ms_routed_calls": stats([(r.get("timing") or {}).get("big_ms") for r in rt]),
                "small_input_tokens_total": sum(r.get("small_input_tokens") or 0 for r in ok),
                "big_input_tokens_total": sum(r.get("big_input_tokens") or 0 for r in ok),
                "rule": {k: m[k] for k in ("tau", "w_big", "route_on", "small_name", "big_name")}}
    if jv:
        toks = [r["usage"]["input_tokens"] for r in jv.values() if r.get("usage") and r["usage"].get("input_tokens")]
        models = Counter(r.get("model") for r in jv.values() if not r["failed"])
        S["jev"].update(models=dict(models), calls_not_pinned_model=sum(v for k, v in models.items() if k != L.PINNED_JEV),
                        input_tokens_total=sum(toks), input_tokens_per_call_mean=round(sum(toks) / len(toks), 1) if toks else None,
                        list_price_usd_per_1k_calls=round(sum(toks) / len(toks) * L.JEV_USD_PER_M_INPUT / 1e3, 6) if toks else None)
        S["jev"]["tokens"] = token_block(jv, task_of, ("input_tokens", "output_tokens"))
        jt = S["jev"]["tokens"]
        jt["note"] = ("Jev's API usage field per call (input_tokens, output_tokens); complete false = the route returned "
                      "no usage on some answered calls (the means then cover only the calls that had it; Jev's tokenizer "
                      "is unknown, so there is no fallback count)")
    if od and jv:  # descriptive: both systems' measured tokens on these calls at token list prices (C3-style)
        ci = S["od"]["tokens"]["input_tokens"].get("mean")
        co = S["od"]["tokens"]["output_tokens"].get("mean") or 0
        ji = S["jev"]["tokens"]["input_tokens"].get("mean")
        jo = S["jev"]["tokens"]["output_tokens"].get("mean") or 0
        cst = cfg.get("cost") or {}
        S["token_priced_usd_per_1k_calls"] = {
            "od": round((ci * 0.03 + co * 0.15) / 1e3, 6) if ci is not None else None,
            "jev": round((ji * float(cst.get("jev_usd_per_m_input", L.JEV_USD_PER_M_INPUT))
                          + jo * float(cst.get("jev_usd_per_m_output", 0.0))) / 1e3, 6) if ji is not None else None,
            "note": "descriptive: OD tokens at the frozen Qwen3.5-4B reference price of JevBench v1.5.4 ($0.03/M in, "
                    "$0.15/M out), Jev at list price; not C1 (C1 = GPU $/h / load-tested throughput)"}
    both = sorted(set(od) & set(jv))
    if both:
        o, j, t = [od[c]["client_ms"] for c in both], [jv[c]["client_ms"] for c in both], [task_of[c] for c in both]
        sp = cfg["speed"]
        bs = L.speed_bootstrap(o, j, t, n_boot=int(sp["n_boot"]), seed=int(sp["seed"]))
        S["paired"] = {"calls": len(both), "missing_od": len(want) - len(od), "missing_jev": len(want) - len(jv),
                       **bs, "share_calls_od_faster": round(sum(x < y for x, y in zip(o, j)) / len(both), 4)}
        S["S1_faster"] = {"rule": sp["rule_S1"], "p50_ci_above_0": bs["p50"]["ci95"][0] > 0,
                          "p95_point_lower": bs["p95"]["diff_jev_minus_od_ms"] > 0,
                          "verdict": "faster" if bs["p50"]["ci95"][0] > 0 and bs["p95"]["diff_jev_minus_od_ms"] > 0
                          else ("slower" if bs["p50"]["ci95"][1] < 0 else "not shown faster"),
                          "complete": len(both) == len(want)}
        if " ".join(str(sp["rule_S1"]).split()) != S1_DEFAULT:  # the owner pre-registered another rule
            S["S1_faster"]["verdict_default_rule"] = S["S1_faster"]["verdict"]
            S["S1_faster"]["verdict"] = "rule differs from the coded default: apply the pre-registered rule by hand"
        S["per_task_p50_ms"] = {tk: {"od": L.pct([od[c]["client_ms"] for c in both if task_of[c] == tk], 0.5),
                                     "jev": L.pct([jv[c]["client_ms"] for c in both if task_of[c] == tk], 0.5)}
                                for tk in sorted(set(t))}
    utcs = sorted(r["utc"] for r in recs if r["call_id"] in want)
    S["wall"] = {"first_utc": utcs[0] if utcs else None, "last_utc": utcs[-1] if utcs else None}
    # ---- OD answers: parity with the scored batch run (D1 = L4_batch) and/or the scored files (D1 = served_h100)
    od_ans = {}
    if (out / "od_answers.jsonl").exists():
        for rec in L.read_jsonl(out / "od_answers.jsonl"):
            if rec["call_id"] in want:
                od_ans.update(rec["answers"])
    pd = root / f"preds_{L.SPLIT}"
    if a.scored_name and od_ans:
        if m["kind"] == "cascade":
            S["parity_vs_scored"] = cascade_parity(od_ans, pd, a.scored_name, m)
        else:
            S["parity_vs_scored"] = {
                "raw_vs_" + a.scored_name: parity({k: v for k, v in od_ans.items() if v.get("raw")},
                                                  pd / f"{a.scored_name}.jsonl", "raw"),
                "final_vs_" + a.scored_name + "_cal": parity(od_ans, pd / f"{a.scored_name}_cal.jsonl", "final")}
        S["parity_pass"] = all(v.get("pass") is not False for v in S["parity_vs_scored"].values()) and any(
            v.get("pass") for v in S["parity_vs_scored"].values())
    if a.od_preds_name:
        S["od_preds"] = (write_cascade_preds if m["kind"] == "cascade" else write_od_preds)(a, root, cfg, m, rows,
                                                                                            od_ans, out)
    if a.jev_preds_tag:
        S["jev_preds"] = write_jev_preds(a, root, rows, out)
    (out / "summary.json").write_text(json.dumps(S, indent=1))
    report(S)
    L.blind_print(f"wrote {out}/summary.json")
    return S


def cascade_parity(od_ans, pd, scored, m):
    """The served cascade vs the scored offline cascade (ohs3_cascade.py from the two models' scored runs): the final
    answer, the routed set, and (when the components' scored files are there) the small model's readout on every row
    and the big model's readout on the routed rows."""
    out = {"final_vs_" + scored + "_cal": parity(od_ans, pd / f"{scored}_cal.jsonl", "final")}
    ref = pd / f"{scored}_cal.jsonl"
    if ref.exists():
        off = {o["id"]: o.get("routed") for o in L.read_jsonl(ref)}
        both = [k for k in od_ans if k in off and off[k] is not None and od_ans[k].get("routed") is not None]
        agree = sum(bool(od_ans[k]["routed"]) == bool(off[k]) for k in both)
        out["routed_set_vs_" + scored] = {"rows": len(both), "agree": round(agree / len(both), 5) if both else None,
                                          "served_routed": sum(bool(od_ans[k]["routed"]) for k in both),
                                          "offline_routed": sum(bool(off[k]) for k in both),
                                          "pass": (agree / len(both) >= PARITY_BARS["argmax_agree_min"]) if both else None}
    for view, comp in (("small_raw", m["small_name"]), ("big_raw", m["big_name"])):
        p = pd / f"{comp}.jsonl"
        sub = {k: v for k, v in od_ans.items() if v.get(view) is not None}
        if p.exists() and sub:
            out[f"{view}_vs_{comp}"] = parity(sub, p, view)
    return out


def write_od_preds(a, root, cfg, m, rows, od_ans, out):
    """D1 = served_h100: the served run is the one OHS-3 run of this model (rule 4)."""
    import ohs3_od_run as R
    name = a.od_preds_name
    if name != m["name"] and L.is_real_ohs3(root):
        raise SystemExit(f"--od-preds-name {name} must be the pre-registered model name {m['name']}")
    if L.completed_runs(root, name) or any(p.exists() for p in R.out_files(root / f"preds_{L.SPLIT}", name).values()):
        raise SystemExit(f"STOP (rule 4): {name} already has an OHS-3 run")
    order = [r for r in L.read_jsonl(root / "data" / f"{L.SPLIT}.jsonl")]
    missing = [r["id"] for r in order if r["id"] not in od_ans or od_ans[r["id"]].get("raw") is None]
    if missing:
        raise SystemExit(f"{len(missing)} rows have no served answer: re-run the timing harness to resume first")
    meta = {"config": cfg["_path"], "config_sha256": cfg["_sha256"], "model_key": a.model_key,
            "path": f"served (ohs3_serve A5Decider via {a.od_url.split('//')[-1].split('/')[0]}); timing run {a.name}",
            "timing_records": str(out / "records.jsonl")}
    shas = R.write_outputs(root, name, order, {i: v["1v"] for i, v in od_ans.items()}, {i: v["raw"] for i, v in od_ans.items()},
                           m, meta)
    L.ledger_append(root, {"name": name, "status": "complete", "kind": "served", "config_sha256": cfg["_sha256"],
                           "files_sha256": shas})
    # the served final answer must equal T applied to the served raw readout (one code path)
    cal = {o["id"]: o["probs"] for o in L.read_jsonl(root / f"preds_{L.SPLIT}" / f"{name}_cal.jsonl")}
    dmax = max(abs(cal[i][k] - v["final"][k]) for i, v in od_ans.items() if i in cal for k in v["final"])
    return {"name": name, "sha256": shas, "max_abs_diff_cal_vs_served_final": dmax}


def write_cascade_preds(a, root, cfg, m, rows, od_ans, out):
    """D1 = served_h100 for the cascade: the served cascade pass IS the cascade's one OHS-3 run (rule 4). Writes
    preds_ohs3/<name>_cal.jsonl (the scored file ohs3_cascade.py would write offline, same format, + routed) after
    recomputing every served answer from the served component readouts with ohs3_lib's cascade rule (one code path).
    The component reads inside this pass are never scored as the 2B or the 4B."""
    name = a.od_preds_name
    pd = root / f"preds_{L.SPLIT}"
    if name != m["name"] and L.is_real_ohs3(root):
        raise SystemExit(f"--od-preds-name {name} must be the pre-registered cascade name {m['name']}")
    outp = pd / f"{name}_cal.jsonl"
    if L.completed_runs(root, name) or outp.exists():
        raise SystemExit(f"STOP (rule 4): the cascade {name} already has an OHS-3 run")
    order = L.read_jsonl(root / "data" / f"{L.SPLIT}.jsonl")
    missing = [r["id"] for r in order if r["id"] not in od_ans or od_ans[r["id"]].get("small_raw") is None]
    if missing:
        raise SystemExit(f"{len(missing)} rows have no served answer: re-run the timing harness to resume first")
    ms, mb = cfg["models"][m["small"]], cfg["models"][m["big"]]
    dmax, recs, routed = 0.0, [], 0
    for r in order:
        v = od_ans[r["id"]]
        sf = L.apply_T(v["small_raw"], r, ms["T_primary"])
        rt = L.cascade_routed(r, sf if m["route_on"] == "primary" else v["small_raw"], m["tau"])
        if rt != bool(v["routed"]):
            raise SystemExit("served routing differs from the cascade rule recomputed from the served readout")
        bf = L.apply_T(v["big_raw"], r, mb["T_primary"]) if rt else None
        fin = L.cascade_answer(r, sf, bf, rt, m["w_big"])
        dmax = max(dmax, max(abs(fin[k] - v["final"][k]) for k in fin))
        routed += rt
        recs.append({"id": r["id"], "model": f"{name}_cal", "probs": v["final"], "routed": rt})
    if dmax > 1e-9:
        raise SystemExit(f"served cascade answers differ from the cascade rule by {dmax}")
    pd.mkdir(parents=True, exist_ok=True)
    L.write_jsonl_atomic(outp, recs)
    meta = {"name": f"{name}_cal", "small": m["small_name"], "big": m["big_name"], "tau": m["tau"], "w_big": m["w_big"],
            "route_on": m["route_on"], "rows": len(order), "routed": routed, "routed_share": round(routed / len(order), 4),
            "config_sha256": cfg["_sha256"], "kind": "served_cascade", "timing_run": a.name,
            "timing_records": str(out / "records.jsonl"),
            "path": f"served (ohs3_lib.CascadeDecider via {a.od_url.split('//')[-1].split('/')[0]})",
            "max_abs_diff_served_vs_rule": dmax, "utc": L.utc(),
            "note": "component reads inside this pass are part of the cascade system; never scored as the 2B or the 4B"}
    (pd / f"{name}_cal.meta.json").write_text(json.dumps(meta, indent=2))
    sha = L.sha256_file(outp)
    L.ledger_append(root, {"name": name, "status": "complete", "kind": "served_cascade", "config_sha256": cfg["_sha256"],
                           "files_sha256": {"_cal": sha}, "routed": routed})
    return {"name": name, "sha256": {"_cal": sha}, "routed": routed, "max_abs_diff_served_vs_rule": dmax}


def write_jev_preds(a, root, rows, out):
    """D2 = run1_via_harness: preds_ohs3/<tag>_raw.jsonl + <tag>.jsonl, run_jev.py's raw format and conversion."""
    tag = a.jev_preds_tag
    pd = root / f"preds_{L.SPLIT}"
    raw_dst, pf = pd / f"{tag}_raw.jsonl", pd / f"{tag}.jsonl"
    if raw_dst.exists() or pf.exists():
        raise SystemExit(f"{raw_dst.name} / {pf.name} exist: refusing to overwrite a Jev run")
    raw_dst.write_bytes((out / "jev_raw.jsonl").read_bytes())
    preds = L.jev_raw_to_preds(raw_dst, rows, tag)
    with open(pf, "w") as f:
        for o in preds:
            f.write(json.dumps(o) + "\n")
    return {"tag": tag, "rows": len(preds), "raw_sha256": L.sha256_file(raw_dst), "preds_sha256": L.sha256_file(pf)}


# Stored L4 reads that the DEV smoke compares the served answers with: (single read, 2-view read of the choice rows).
# 4B-E: its job-1 fresh read and its legacy --tta read. Any other 4B (C4 = q35_4b_main500k_fix2, or C1 after an owner
# override): its untagged gate read and its od_gcp predict --tta-choice read <name>_2v (prereg_drafts/A8prime.md:
# made in gate job 3 when C4 ships). The shipped 4B is TBD by gate job 3, so the refs follow the configured name.
SMOKE_REFS = {"q35_4b_pxE": ("q35_4b_pxE_fresh", "q35_4b_pxE_tta")}


def smoke_refs(name):
    return SMOKE_REFS.get(name, (name, name + "_2v"))


def dev_smoke(a):
    """GPU smoke of OUR endpoint on DEV rows only (never OHS-3): wide label sets (dev_nc up to 56 options) and cards on
    yes/no rows (devp_card), one row per call as in OHS-3. The served identity view must match the stored L4 single
    read of the same adapter (--smoke-ref-1v), and on choice rows the served 2-view readout the stored L4 TTA read
    (--smoke-ref-2v; its yes/no rows also swapped letters, so only choice rows are compared). Bars: client_bench.py's
    H100-vs-L4 parity bars. Latency is reported for information only (dev rows, not the claim).
    Cascade (--model-key cascade): the refs are the SMALL model's (--smoke-ref-1v / -2v); --smoke-ref-big-1v is the
    big model's single read, compared on the routed rows; every served answer must equal the cascade rule recomputed
    from the served readouts. The endpoint's /health must name this system and config."""
    cfg = L.load_config(a.config, require_complete=True, model_keys=[a.model_key])
    m = L.system(cfg, a.model_key)
    od = OD(a.od_url, a.od_token, 60.0)
    ref_root = Path(a.smoke_ref_root).resolve()
    casc = m["kind"] == "cascade"
    v1, vr = ("small_1v", "small_raw") if casc else ("1v", "raw")
    d1, d2 = smoke_refs(m["small_name"] if casc else m["name"])
    a.smoke_ref_1v, a.smoke_ref_2v = a.smoke_ref_1v or d1, a.smoke_ref_2v or d2
    out = {"specs": a.dev_smoke, "system": m["key"], "ref_1v": a.smoke_ref_1v, "ref_2v": a.smoke_ref_2v,
           "ref_big_1v": a.smoke_ref_big_1v, "splits": {}}
    try:
        h = od.health()
        out["health"] = {k: h.get(k) for k in ("model", "config_sha256", "readout", "path", "prism_x", "cascade")}
        if h.get("model") != m["name"] or h.get("config_sha256") != cfg["_sha256"]:
            raise SystemExit(f"the endpoint serves {h.get('model')} / config {str(h.get('config_sha256'))[:16]}, not "
                             f"{m['name']} / {cfg['_sha256'][:16]}")
        for spec in a.dev_smoke.split(","):
            split, n = spec.split(":")
            if split.startswith("ohs"):
                raise SystemExit("dev smoke: DEV splits only")
            rows = [r for r in L.read_jsonl(L.LEAN / "data" / f"{split}.jsonl")]
            rows = sorted(rows, key=lambda r: hashlib.sha256(f"smoke:{r['id']}".encode()).hexdigest())[:int(n)]
            ans, ms, errs, toks = {}, [], 0, []
            for r in rows:
                req, qmap = L.od_request({"call_id": "smoke-" + r["id"], "state": r["state"], "row_ids": [r["id"]]},
                                         {r["id"]: r})
                res, rec = timed(lambda: od.send(req), 2, 60.0)
                if res is None:
                    errs += 1
                    continue
                ms.append(rec["client_ms"])
                toks.append((res.get("usage") or {}).get("input_tokens"))
                ans[r["id"]] = {"final": our_probs(res["answers"]["q0"], r), **res["answers"]["q0"]["views"]}
            s = {"rows": len(rows), "errors": errs, "client_ms": stats(ms),
                 "max_options": max((len(r["options"] or []) for r in rows), default=0),
                 "yes_no_with_card": sum(1 for r in rows if r["qtype"] == "noul" and r.get("card")),
                 "input_tokens": stats([t for t in toks if t is not None]),
                 "token_counts_present": all(t is not None for t in toks)}
            p1 = ref_root / f"preds_{split}" / f"{a.smoke_ref_1v}.jsonl"
            if p1.exists():
                s["parity_1v"] = parity(ans, p1, v1)
            if a.smoke_ref_2v:
                p2 = ref_root / f"preds_{split}" / f"{a.smoke_ref_2v}.jsonl"
                ch = {k: v for k, v in ans.items() if next(r for r in rows if r["id"] == k)["qtype"] == "choice"}
                if p2.exists() and ch:
                    s["parity_2view_choice"] = parity(ch, p2, vr)
            if casc:
                rmap = {r["id"]: r for r in rows}
                ms_, mb_ = cfg["models"][m["small"]], cfg["models"][m["big"]]
                dmax = 0.0
                for k, v in ans.items():
                    r = rmap[k]
                    sf = L.apply_T(v["small_raw"], r, ms_["T_primary"])
                    rt = L.cascade_routed(r, sf if m["route_on"] == "primary" else v["small_raw"], m["tau"])
                    fin = L.cascade_answer(r, sf, L.apply_T(v["big_raw"], r, mb_["T_primary"]) if rt else None, rt,
                                           m["w_big"])
                    dmax = max(dmax, 1.0 if rt != bool(v["routed"]) else max(abs(fin[x] - v["final"][x]) for x in fin))
                s["cascade_rule_check"] = {"max_abs_diff": dmax, "pass": dmax <= 1e-9,
                                           "routed": sum(bool(v["routed"]) for v in ans.values())}
                if a.smoke_ref_big_1v:
                    pb = ref_root / f"preds_{split}" / f"{a.smoke_ref_big_1v}.jsonl"
                    sub = {k: v for k, v in ans.items() if v.get("big_1v") is not None}
                    if pb.exists() and sub:
                        s["parity_big_1v_routed"] = parity(sub, pb, "big_1v")
            out["splits"][split] = s
    finally:
        od.close()
    out["pass"] = all(v.get("errors") == 0 and v.get("token_counts_present")
                      and all(x.get("pass") is not False for k, x in v.items() if k.startswith(("parity", "cascade_rule")))
                      and any(k.startswith("parity") for k in v) for v in out["splits"].values())
    d = Path(a.root).resolve() / "logs" / "ohs3" / "timing" / a.name
    d.mkdir(parents=True, exist_ok=True)
    (d / "dev_smoke.json").write_text(json.dumps(out, indent=1))
    for sp_, v in out["splits"].items():
        L.blind_print(f"smoke {sp_}: {v['rows']} rows, errors {v['errors']}, max options {v['max_options']}, "
                      f"client p50 {v['client_ms'].get('p50')} ms, input tokens p50 {v['input_tokens'].get('p50')}; "
                      + "; ".join(f"{k} pass={x.get('pass')} agree={x.get('argmax_agree')} max_dp={x.get('max_dp')}"
                                  for k, x in v.items() if k.startswith(("parity", "cascade_rule"))))
    L.blind_print(f"DEV SMOKE {'PASS' if out['pass'] else 'FAIL'} -> {d / 'dev_smoke.json'}")
    return out


def report(S):
    for who in ("od", "jev"):
        if who in S:
            c = S[who]["client_ms"]
            tk = (S[who].get("tokens") or {}).get("input_tokens") or {}
            L.blind_print(f"{who:4s} client p50 {c.get('p50')} p95 {c.get('p95')} p99 {c.get('p99')} ms; failed "
                          f"{S[who]['failed_calls']}, retried {S[who]['retried_calls']}, timed {S[who]['calls_timed']}; "
                          f"input tokens/call mean {tk.get('mean')} (counted on {tk.get('calls_with_count')} calls)")
    if "cascade" in S.get("od", {}):
        cs = S["od"]["cascade"]
        L.blind_print(f"cascade: routed {cs['routed_rows']}/{cs['rows']} rows ({cs['routed_share']}); client p50 routed "
                      f"{cs['client_ms_routed_calls'].get('p50')} ms, not routed {cs['client_ms_not_routed_calls'].get('p50')} ms")
    if "paired" in S:
        p = S["paired"]
        L.blind_print(f"Jev - OD p50 {p['p50']['diff_jev_minus_od_ms']:+.1f} ms CI [{p['p50']['ci95'][0]:+.1f}, "
                      f"{p['p50']['ci95'][1]:+.1f}]; p95 {p['p95']['diff_jev_minus_od_ms']:+.1f} ms; S1: "
                      f"{S['S1_faster']['verdict']} (complete {S['S1_faster']['complete']})")
    if "parity_vs_scored" in S:
        L.blind_print("parity vs scored run: " + json.dumps({k: (v.get("pass"), v.get("argmax_agree", v.get("agree")),
                                                                 v.get("max_dp"))
                                                             for k, v in S["parity_vs_scored"].items()}))


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--root", default=str(L.LEAN))
    ap.add_argument("--config", required=True)
    ap.add_argument("--model-key", default="4b", help="the system the endpoint serves: a model key (4b, 2b) or cascade")
    ap.add_argument("--od-url", default=None)
    ap.add_argument("--od-token", default=None)
    ap.add_argument("--no-jev", action="store_true")
    ap.add_argument("--fake-jev-url", default=None)
    ap.add_argument("--name", required=True)
    ap.add_argument("--limit", type=int, default=0, help="0 = every OHS-3 call (the reported run)")
    ap.add_argument("--scored-name", default=None, help="D1 = L4_batch: parity vs preds_ohs3/<name>(_cal).jsonl")
    ap.add_argument("--od-preds-name", default=None, help="D1 = served_h100: write the scored OD preds")
    ap.add_argument("--jev-preds-tag", default=None, help="D2 = run1_via_harness: write preds_ohs3/<tag>.jsonl")
    ap.add_argument("--refill-rounds", type=int, default=3,
                    help="re-send calls that failed every attempt, for the SCORED side(s) only (untimed; 0 = off)")
    ap.add_argument("--summary-only", action="store_true", help="recompute summary.json from the records")
    ap.add_argument("--dev-smoke", default=None, help="DEV-only GPU smoke of our endpoint, e.g. dev_nc:60,devp_card:40")
    ap.add_argument("--smoke-ref-root", default=str(L.LEAN))
    ap.add_argument("--smoke-ref-1v", default=None, help="stored L4 single read of the hosted adapter "
                                                         "(default: smoke_refs(<configured name>))")
    ap.add_argument("--smoke-ref-2v", default=None, help="stored L4 2-view read (choice rows compared) "
                                                         "(default: smoke_refs(<configured name>))")
    ap.add_argument("--smoke-ref-big-1v", default=None, help="cascade: the big model's stored L4 single read (routed rows)")
    ap.add_argument("--go", action="store_true")
    a = ap.parse_args(argv)
    if a.dev_smoke:
        return dev_smoke(a)
    if not a.od_url and not a.summary_only and a.no_jev:
        raise SystemExit("nothing to time")
    if a.summary_only:
        root = Path(a.root).resolve()
        cfg = L.load_config(a.config, require_complete=True, model_keys=[a.model_key])
        rows = {r["id"]: r for r in L.read_jsonl(root / "data" / f"{L.SPLIT}.jsonl")}
        calls = L.read_jsonl(root / "data" / f"{L.SPLIT}_calls.jsonl")
        task_of = {c["call_id"]: rows[c["row_ids"][0]]["source"] for c in calls}
        recs = L.read_jsonl(root / "logs" / "ohs3" / "timing" / a.name / "records.jsonl")
        ids = {r["call_id"] for r in recs}
        order = [c for c in calls if c["call_id"] in ids]
        return summarize(a, root, cfg, L.system(cfg, a.model_key), order, task_of, rows,
                         root / "logs" / "ohs3" / "timing" / a.name, {"before": [], "after": []}, L.is_real_ohs3(root))
    return run(a)


if __name__ == "__main__":
    main()
