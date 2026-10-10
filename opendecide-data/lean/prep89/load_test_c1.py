"""(C1) DEV-ONLY load test of OUR endpoint: sustained decisions per hour under concurrency, at the serving batch policy
(one request = one call = its rows read together; the server reads one request at a time under its GPU lock), on DEV
rows only, never OHS-3. NOT RUN on a GPU yet (the CPU dry run runs it against the local tiny-model server).

Exact commands (after the owner's GO; one Modal H100, the pre-registered serving config: same host, readout, T,
graphs/eager path and region as the timing pass):
  (1) recommended: right after the OHS-3 timing pass, in the SAME H100 session (no second boot). The load test is
      length-matched to the per-question token counts that pass logged (counts only; no OHS-3 text is read):
        MODAL_PROFILE=<acct> ../.venv/bin/modal run prep89/modal_ohs3_host.py::main --config prep89/ohs3_config.json \\
            --model-key 4b --name ohs3_timing --scored-name <4b name> --go --then-load-test
  (2) on its own (new session), matched to an earlier timing pass's records:
        MODAL_PROFILE=<acct> ../.venv/bin/modal run prep89/modal_ohs3_host.py::main --config prep89/ohs3_config.json \\
            --model-key 4b --name c1_load_4b --load-test --load-match logs/ohs3/timing/ohs3_timing/records.jsonl --go
  (3) a pre-run ESTIMATE (before any OHS-3 call; not the C1 claim): no --load-match; the call mix is PREREG_OHS3's
      type counts (1,016 yes/no, 1,440 choice with >= 10 options), lengths as the dev pool has them.
  (--model-key 2b / cascade time the eager PRISM-X 2B / the cascade the same way.)
  Against an endpoint that is already up (any host; no Modal call from this script):
        ../.venv/bin/python prep89/load_test_c1.py --config prep89/ohs3_config.json --model-key 4b --od-url URL \\
            --od-token TOKEN --name c1_load_4b --match-records logs/ohs3/timing/ohs3_timing/records.jsonl
  --plan prints these commands and the cost estimate below from the config alone (no endpoint, nothing billed):
        ../.venv/bin/python prep89/load_test_c1.py --config prep89/ohs3_config.json --model-key 4b --plan
Cost estimate (cost.od_usd_per_hour 4.31 all-in x the hosting.region multiplier; us-east is "narrow": x1.75 = 7.54/h;
the --plan numbers for the template's cost.load_test):
  in-session time = levels (1, 2, 4, 8, 16) x (10 s warm-up + 60 s window) = 350 s + the token check (20 calls, <= 20 s)
      + the dev-row token counting and length fit on the laptop while the server waits (~60 s) = about 7.2 min;
  (1) inside the timing session: + 7.2 min = $0.51 (any region) to $0.90 (us-east), for any system;
  (2)/(3) a new session: boot (estimates: 4B on CUDA graphs ~8 min, 2B eager ~4 min, cascade ~10 min) + 7.2 min +
      ~1 min shutdown = 4B 16 min $1.16-2.03, 2B 12 min $0.87-1.53, cascade 18 min $1.30-2.28 (any region - us-east).

Method (pre-registered with the config, numbers in cost.load_test):
  1. Calls: one dev row per call (OHS-3 has one row per call). Pool: load_test.splits (dev only; a split whose name
     starts with "ohs" is refused).
  2. Length match. Target: the OHS-3 timing pass's per-question [type, options, identity-read tokens] (the server's own
     counts, logged by ohs3_timing.py). Each target gets a pool row of the same type (and, only for the 2view_ge10
     readout, the same options bucket < 10 / >= 10: it changes the number of reads), drawn (seeded) among the 6 rows
     nearest in token count; then its state is lengthened with other dev text or cut so that its identity-read token
     count is within max(2 tokens, 1%) of the target (the dev pool is thin for long 40-option rows: plain nearest
     matching gave KS 0.146 on the synthetic stand-in). All text stays dev text. Tokens are counted here with the
     model's own tokenizer and decoder_io's prompt (the server's count); the first token_check_calls calls check
     server count == local count. Match bar: KS distance
     <= ks_max and |mean ratio - 1| <= mean_ratio_tol, same type shares. A failed bar or token check makes the
     result INVALID for C1 (the final table then gives no C1 verdict).
  3. Load: per concurrency level c, c client threads (one keep-alive connection each) send the matched calls in a
     seeded cyclic order back to back; warm-up warmup_s, then a window of seconds_per_level. A decision counts when
     its call completes inside the window. Throughput = decisions completed in the window / window seconds x 3600.
  4. Sustained decisions per hour = the highest throughput over the levels with 0 failed calls (sustained_rule).
     The cascade also needs the dev routed share within routed_share_tol (0.05) of the OHS-3 pass's (its cost depends
     on how many rows go to the 4B), else INVALID.
  5. C1 = od_usd_per_hour x region multiplier / sustained decisions per hour x 1000 $ per 1,000 decisions, at 100%
     and at cost.utilisation_for_claim. Written to logs/ohs3/load_test/<name>/summary.json for ohs3_final_table.py.
Blind: prints counts, rates and timings only.
"""
from __future__ import annotations

import argparse
import bisect
import hashlib
import json
import random
import socket
import sys
import threading
import time
from collections import Counter, defaultdict
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import ohs3_lib as L  # noqa: E402

DEFAULTS = {"levels": [1, 2, 4, 8, 16], "seconds_per_level": 60, "warmup_s": 10, "seed": 0, "token_check_calls": 20,
            "splits": ["dev_nc", "pg_dev", "taskbank_dev", "devp_card", "hard_dev", "dev_claims", "devzs", "dev",
                       "dev_negwords"],
            "match_bar": {"ks_max": 0.05, "mean_ratio_tol": 0.02},
            "sustained_rule": "max throughput over levels with 0 failed calls", "timeout_s": 30,
            "routed_share_tol": 0.05}
PREREG_CALL_MIX = {("noul", False): 1016, ("choice", True): 1440}  # PREREG_OHS3: 716 + 300 _neg; 1,136 + 304 _perm


def settings(cfg):
    lt = dict(DEFAULTS)
    lt.update((cfg.get("cost") or {}).get("load_test") or {})
    return lt


def tokenizer_dir_for(cfg, key, override=None):
    """The tokenizer the served model reads with (for the cascade: the small model's, which reads every row)."""
    if override:
        return Path(override)
    m = cfg["models"][cfg["cascade"]["small"]] if key == "cascade" else cfg["models"][key]
    for d in ("gcp_models", "modal_models"):
        p = L.REPO / "backups" / d / m["name"]
        if (p / "tokenizer_config.json").exists():
            return p
    raise SystemExit(f"no local tokenizer for {m['name']} in backups/; pass --tokenizer-dir")


def prompt_counter(m, tokenizer_dir):
    """row -> the identity-read token count the server reports for it: decoder_io's prompt in the model's layout/style,
    the model's tokenizer, add_special_tokens=False, capped at decoder_io.MAX_LEN (cand_logits' truncation).
    The full decoder_io.Readout is built (its vocabulary scan sets the two-letter labels used after Z, as on the
    server). Sets decoder_io's LAYOUT/STYLE in THIS process (a client process; never call it inside a server)."""
    from transformers import AutoTokenizer
    if str(L.LEAN) not in sys.path:
        sys.path.insert(0, str(L.LEAN))
    import decoder_io as dio
    dio.LAYOUT, dio.STYLE = m["layout"], m["style"]
    tok = AutoTokenizer.from_pretrained(str(tokenizer_dir))
    tok.padding_side = "right"
    if tok.pad_token is None:
        tok.pad_token = tok.eos_token
    ro = dio.Readout(tok)

    def count(row):
        return min(len(tok(ro.prompt(row), add_special_tokens=False)["input_ids"]), dio.MAX_LEN)
    return count


def count_pool(cfg, key, splits, tokenizer_dir):
    """Dev rows with the identity-read token count the server would report (prompt_counter)."""
    m = cfg["models"][cfg["cascade"]["small"]] if key == "cascade" else cfg["models"][key]
    count = prompt_counter(m, tokenizer_dir)
    pool = []
    for sp in splits:
        if sp.startswith("ohs"):
            raise SystemExit(f"load test: DEV splits only ({sp} refused)")
        for r in L.read_jsonl(L.LEAN / "data" / f"{sp}.jsonl"):
            row = {k: r.get(k) for k in ("id", "state", "instructions", "qtype", "options", "card")}
            pool.append({"row": row, "split": sp, "qtype": r["qtype"], "ge10": len(r["options"] or []) >= 10,
                         "tok": count(row)})
    return pool


def routed_share_of_records(path):
    """The cascade's routed share in the OHS-3 timing pass (counts only), or None for a single model."""
    n = rt = 0
    for r in L.read_jsonl(path):
        if r.get("who") == "od" and not r.get("refill") and not r.get("failed") and r.get("routed_rows") is not None:
            n += len(r.get("qs") or [])
            rt += r["routed_rows"]
    return rt / n if n else None


def target_from_records(path):
    """[(qtype, ge10, identity-read tokens)] from a timing pass's records (timed, answered OD calls; counts only)."""
    out = []
    for r in L.read_jsonl(path):
        if r.get("who") != "od" or r.get("refill") or r.get("failed"):
            continue
        for q in r.get("qs") or []:
            if q[2] is None:
                raise SystemExit(f"{path}: a record has no token count (an old harness?)")
            out.append((q[0], q[1] >= 10, int(q[2])))
    if not out:
        raise SystemExit(f"{path}: no answered OD calls with token counts")
    return out


def ks(a, b):
    """Two-sample Kolmogorov-Smirnov distance sup |F_a - F_b|."""
    a, b = sorted(a), sorted(b)
    pts = sorted(set(a) | set(b))
    return max(abs(bisect.bisect_right(a, x) / len(a) - bisect.bisect_right(b, x) / len(b)) for x in pts)


def qs(xs):
    return {k: L.pct(xs, q) for k, q in (("p10", 0.1), ("p50", 0.5), ("p90", 0.9), ("p99", 0.99))} | {
        "mean": round(sum(xs) / len(xs), 1), "max": max(xs)}


def filler_text(splits, seed, chars=400_000):
    """Dev text only: the states of the dev splits in a seeded order, joined (used to lengthen a dev row's state)."""
    sts = []
    for sp in splits:
        if sp.startswith("ohs"):
            raise SystemExit(f"load test: DEV splits only ({sp} refused)")
        sts += [r["state"] for r in L.read_jsonl(L.LEAN / "data" / f"{sp}.jsonl") if r.get("state")]
    random.Random(seed).shuffle(sts)
    out, n = [], 0
    for x in sts:
        out.append(x)
        n += len(x) + 2
        if n >= chars:
            break
    return "\n\n".join(out)


def fit_length(row, target, count, filler):
    """The dev row with its state lengthened (dev filler text appended) or shortened (cut at the end) so that its
    identity-read token count is within max(2, 1%) of target; options, card and question unchanged. Returns
    (row, tokens, how). Token count grows with the state's length, so a bisection on the character count is used."""
    tol = max(2, round(0.01 * target))
    n0 = count(row)
    if abs(n0 - target) <= tol:
        return row, n0, "as_is"
    st = row["state"]
    if n0 < target:
        make, lo, hi, how = (lambda k: {**row, "state": st + "\n\n" + filler[:k]}), 0, len(filler), "lengthened"
    else:
        make, lo, hi, how = (lambda k: {**row, "state": st[:k]}), 1, len(st), "shortened"
    best = (abs(n0 - target), row, n0)
    for _ in range(40):
        if lo > hi:
            break
        mid = (lo + hi) // 2
        r = make(mid)
        n = count(r)
        if abs(n - target) < best[0]:
            best = (abs(n - target), r, n)
        if abs(n - target) <= tol:
            break
        if n < target:
            lo = mid + 1
        else:
            hi = mid - 1
    if best[0] > tol:  # e.g. a row whose length is mostly options: the state alone cannot be cut enough
        how += "_miss"
    return best[1], best[2], how


def match(target, pool, seed, by_ge10=True, fit=None):
    """Per target [type, options bucket, identity-read tokens]: a dev pool row of the same type (and options bucket
    < 10 / >= 10 when by_ge10: 2view_ge10 reads the two buckets a different number of times), drawn at random (seeded)
    among the 6 rows nearest in token count; then (fit = a fit_length closure) its state is lengthened with dev text or
    shortened to the target's token count, so the length distribution matches even where the dev pool is thin (long
    40-option rows). Rows may repeat: the server has no cache across requests."""
    key = (lambda q, g: (q, g)) if by_ge10 else (lambda q, g: (q, None))  # noqa: E731
    by = defaultdict(list)
    for i, p in enumerate(pool):
        by[key(p["qtype"], p["ge10"])].append((p["tok"], i))
    for v in by.values():
        v.sort()
    rng = random.Random(seed)
    picked, how = [], Counter()
    adj = []
    for qt, ge, t in target:
        k = key(qt, ge)
        lst = by.get(k)
        if not lst:
            raise SystemExit(f"dev pool has no rows of kind {k}")
        j = bisect.bisect_left(lst, (t, -1))
        near = sorted(lst[max(0, j - 6):j + 6], key=lambda x: (abs(x[0] - t), x[1]))[:6]
        base = pool[rng.choice(near)[1]]
        if fit is None:
            picked.append(base)
            how["as_is"] += 1
            continue
        row, n, h = fit(base["row"], t)
        how[h] += 1
        adj.append(abs(n - base["tok"]) / max(1, base["tok"]))
        picked.append({**base, "row": row, "tok": n, "base_tok": base["tok"]})
    tt, mt = [x[2] for x in target], [p["tok"] for p in picked]
    rep = {"calls": len(target), "pool_rows": len(pool), "ks": round(ks(tt, mt), 5),
           "mean_ratio": round(sum(mt) / sum(tt), 5), "target_tokens": qs(tt), "matched_tokens": qs(mt),
           "pool_tokens_before_fit": qs([p.get("base_tok", p["tok"]) for p in picked]),
           "length_fit": dict(how), "median_relative_length_change": round(sorted(adj)[len(adj) // 2], 4) if adj else 0.0,
           "distinct_dev_rows": len({p["row"].get("id") for p in picked}),
           "match_key": "type + options bucket" if by_ge10 else "type",
           "type_shares_target": dict(Counter(f"{a}{'_ge10' if b and by_ge10 else ''}" for a, b, _ in target)),
           "type_shares_matched": dict(Counter(f"{p['qtype']}{'_ge10' if p['ge10'] and by_ge10 else ''}"
                                               for p in picked)),
           "splits_used": dict(Counter(p["split"] for p in picked))}
    return picked, rep


def prerun_calls(pool, seed):
    """Pre-run estimate: PREREG_OHS3's call mix by type, rows drawn at random from the dev pool (not length-matched)."""
    rng = random.Random(seed)
    out = []
    for (qt, ge), n in PREREG_CALL_MIX.items():
        cand = [p for p in pool if p["qtype"] == qt and (p["ge10"] or not ge)]
        out += [cand[rng.randrange(len(cand))] for _ in range(n)]
    rng.shuffle(out)
    return out


def client(url, token, timeout):
    import httpx
    tr = httpx.HTTPTransport(retries=0, socket_options=[(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)])
    return httpx.Client(base_url=url.rstrip("/"), transport=tr, timeout=timeout,
                        headers={"Authorization": f"Bearer {token}"})


def build_requests(picked):
    out = []
    for i, p in enumerate(picked):
        r = p["row"]
        req, _ = L.od_request({"call_id": f"lt-{i}", "state": r["state"], "row_ids": [r["id"]]}, {r["id"]: r},
                              return_views=False)
        out.append((req, 1, p["tok"]))
    return out


def token_check(url, token, reqs, n, timeout):
    """The server's identity-read count must equal the local count the match used (same unit)."""
    c = client(url, token, timeout)
    try:
        rows = []
        for req, _, tok_local in reqs[:n]:
            d = c.post("/decide", json=req).json()
            au = d["answers"]["q0"].get("usage") or {}
            rows.append((tok_local, au.get("input_tokens_first_view")))
    finally:
        c.close()
    eq = sum(a == b for a, b in rows)
    return {"calls": len(rows), "equal": eq, "pass": eq == len(rows) and len(rows) > 0,
            "max_abs_diff": max((abs(a - (b or 0)) for a, b in rows), default=None)}


def run_level(url, token, reqs, conc, warm_s, win_s, timeout, start_at):
    lock, nxt, recs = threading.Lock(), [start_at], []
    t_start = time.perf_counter()
    t_warm, t_end = t_start + warm_s, t_start + warm_s + win_s

    def worker():
        c = client(url, token, timeout)
        try:
            while time.perf_counter() < t_end:
                with lock:
                    i = nxt[0]
                    nxt[0] += 1
                req, nrows, _ = reqs[i % len(reqs)]
                t0 = time.perf_counter()
                ok, d = False, {}
                try:
                    r = c.post("/decide", json=req)
                    ok = r.status_code == 200
                    d = r.json() if ok else {}
                except Exception:  # noqa: BLE001 - counted as a failed call
                    pass
                t1 = time.perf_counter()
                with lock:
                    recs.append((t0, t1, ok, nrows, d.get("server_ms"), (d.get("timing") or {}).get("model_ms"),
                                 (d.get("usage") or {}).get("input_tokens"), (d.get("usage") or {}).get("routed_rows")))
        finally:
            c.close()

    th = [threading.Thread(target=worker, daemon=True) for _ in range(conc)]
    for t in th:
        t.start()
    for t in th:
        t.join(timeout + win_s + warm_s + 60)
    win = [r for r in recs if t_warm <= r[1] <= t_end]
    okw = [r for r in win if r[2]]
    lat = [(r[1] - r[0]) * 1000 for r in okw]
    out = {"concurrency": conc, "window_s": win_s, "warmup_s": warm_s, "calls_sent": len(recs),
           "calls_completed_in_window": len(okw), "decisions_in_window": sum(r[3] for r in okw),
           "failed_calls": sum(1 for r in recs if not r[2]),
           "decisions_per_hour": round(sum(r[3] for r in okw) / win_s * 3600, 1),
           "client_ms": {k: round(L.pct(lat, q), 2) for k, q in (("p50", 0.5), ("p95", 0.95), ("p99", 0.99))} if lat else {},
           "server_ms_p50": L.pct([r[4] for r in okw if r[4] is not None], 0.5),
           "model_ms_sum_share_of_window": round(sum(r[5] or 0 for r in okw) / (win_s * 1000), 4),
           "input_tokens_per_call_mean": round(sum(r[6] or 0 for r in okw) / len(okw), 1) if okw else None}
    rr = [r for r in okw if r[7] is not None]
    if rr:  # the cascade: share of rows the 2B routed to the 4B in this level's window
        out["routed_share"] = round(sum(r[7] for r in rr) / sum(r[3] for r in rr), 4)
    return out, nxt[0]


def c1_block(cfg, sustained):
    c = cfg.get("cost") or {}
    region = (cfg.get("hosting") or {}).get("region", "any")
    base = c.get("od_usd_per_hour")
    mult = L.region_multiplier(region)
    util = c.get("utilisation_for_claim")
    out = {"rate_usd_h_base": base, "region": region, "region_multiplier": mult,
           "rate_usd_h_effective": round(base * mult, 4) if isinstance(base, (int, float)) else None,
           "utilisation_for_claim": util}
    if sustained and out["rate_usd_h_effective"]:
        out["usd_per_1k_at_100pct"] = out["rate_usd_h_effective"] / sustained * 1000
        if isinstance(util, (int, float)) and util > 0:
            out["usd_per_1k_at_claim_util"] = out["usd_per_1k_at_100pct"] / util
    return out


BOOT_MIN = {"model_graphs": 8.0, "model_eager": 4.0, "cascade": 10.0}  # observed/expected H100 boots (estimates)
LAPTOP_PREP_S = 60.0  # dev pool token counting + length fitting on the laptop while the server waits (dry run: ~45 s)
TOKEN_CHECK_S_PER_CALL = 1.0  # upper bound per sequential token-check call (network round trip + one read)
SHUTDOWN_MIN = 1.0


def plan(cfg, key):
    """The exact commands and the cost estimate of this load test for one system, from the config alone (no endpoint,
    no network): serving time = levels x (warm-up + window) + token check + laptop prep; rate = od_usd_per_hour x the
    hosting.region multiplier (and the "any region" rate for comparison); boot from BOOT_MIN."""
    lt = settings(cfg)
    m = L.system(cfg, key)
    kind = "cascade" if m["kind"] == "cascade" else ("model_eager" if (m.get("prism_x") or m.get("cuda_graphs") is False)
                                                     else "model_graphs")
    serve_s = len(lt["levels"]) * (float(lt["warmup_s"]) + float(lt["seconds_per_level"]))
    sess_s = serve_s + int(lt["token_check_calls"]) * TOKEN_CHECK_S_PER_CALL + LAPTOP_PREP_S
    base = float((cfg.get("cost") or {}).get("od_usd_per_hour", 4.31))
    region = (cfg.get("hosting") or {}).get("region", "any")
    mult = L.region_multiplier(region)
    new_min = BOOT_MIN[kind] + sess_s / 60 + SHUTDOWN_MIN
    usd = lambda minutes, r: round(minutes / 60 * r, 2)  # noqa: E731
    name = {"4b": "c1_load_4b", "2b": "c1_load_2b"}.get(key, f"c1_load_{key}")
    mh = "MODAL_PROFILE=<acct> ../.venv/bin/modal run prep89/modal_ohs3_host.py::main --config prep89/ohs3_config.json"
    return {"system": key, "model": m["name"], "kind": kind, "levels": lt["levels"],
            "serving_s": serve_s, "in_session_min": round(sess_s / 60, 2), "new_session_min": round(new_min, 2),
            "rate_usd_h": {"any": base, region: round(base * mult, 4)},
            "usd_in_timing_session": {"any": usd(sess_s / 60, base), region: usd(sess_s / 60, base * mult)},
            "usd_new_session": {"any": usd(new_min, base), region: usd(new_min, base * mult)},
            "commands": {
                "in_timing_session": f"{mh} --model-key {key} --name ohs3_timing{'' if key == '4b' else '_' + key} "
                                     "<the timing pass's flags> --go --then-load-test",
                "own_session": f"{mh} --model-key {key} --name {name} --load-test --load-match "
                               f"logs/ohs3/timing/ohs3_timing{'' if key == '4b' else '_' + key}/records.jsonl --go",
                "prerun_estimate_dev_only": f"{mh} --model-key {key} --name {name}_prerun --load-test --go",
                "endpoint_already_up": f"../.venv/bin/python prep89/load_test_c1.py --config prep89/ohs3_config.json "
                                       f"--model-key {key} --od-url URL --od-token TOKEN --name {name} "
                                       f"--match-records logs/ohs3/timing/ohs3_timing{'' if key == '4b' else '_' + key}"
                                       "/records.jsonl"},
            "note": "estimates: boot minutes and laptop prep are not measured on an H100 yet; nothing here bills"}


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--config", required=True)
    ap.add_argument("--model-key", default="4b", help="the system the endpoint serves: 4b, 2b or cascade")
    ap.add_argument("--plan", action="store_true", help="print the exact commands and the cost estimate; no endpoint")
    ap.add_argument("--od-url", default=None)
    ap.add_argument("--od-token", default=None)
    ap.add_argument("--name", default=None)
    ap.add_argument("--root", default=str(L.LEAN), help="where logs/ohs3/load_test/<name>/ is written")
    ap.add_argument("--match-records", default=None, help="records.jsonl of the OHS-3 timing pass (token counts)")
    ap.add_argument("--tokenizer-dir", default=None)
    ap.add_argument("--levels", default=None, help="override cost.load_test.levels (dry run only)")
    ap.add_argument("--seconds-per-level", type=float, default=None, help="override (dry run only)")
    ap.add_argument("--warmup-s", type=float, default=None, help="override (dry run only)")
    a = ap.parse_args(argv)
    if a.plan:  # the config's numbers only (the template works: placeholders do not enter the estimate)
        cfg = L.load_config(a.config, require_complete=False)
        P = plan(cfg, a.model_key)
        print(json.dumps(P, indent=1))
        return P
    if not (a.od_url and a.od_token and a.name):
        raise SystemExit("--od-url, --od-token and --name are required (or --plan)")
    cfg = L.load_config(a.config, require_complete=True, model_keys=[a.model_key])
    m = L.system(cfg, a.model_key)
    lt = settings(cfg)
    overrides = {k: v for k, v in (("levels", a.levels), ("seconds_per_level", a.seconds_per_level),
                                   ("warmup_s", a.warmup_s)) if v is not None}
    if overrides:
        lt.update(levels=[int(x) for x in str(a.levels).split(",")] if a.levels else lt["levels"],
                  **{k: float(v) for k, v in overrides.items() if k != "levels"})
    out = Path(a.root).resolve() / "logs" / "ohs3" / "load_test" / a.name
    out.mkdir(parents=True, exist_ok=True)
    t0 = time.time()
    tdir = tokenizer_dir_for(cfg, a.model_key, a.tokenizer_dir)
    pool = count_pool(cfg, a.model_key, lt["splits"], tdir)
    readouts = ([cfg["models"][cfg["cascade"]["small"]]["readout_choice"], cfg["models"][cfg["cascade"]["big"]]["readout_choice"]]
                if m["kind"] == "cascade" else [m["readout_choice"]])
    if a.match_records:
        target = target_from_records(a.match_records)
        m_tok = cfg["models"][cfg["cascade"]["small"]] if m["kind"] == "cascade" else cfg["models"][a.model_key]
        count = prompt_counter(m_tok, tdir)
        filler = filler_text(lt["splits"], lt["seed"])
        picked, mrep = match(target, pool, lt["seed"], by_ge10="2view_ge10" in readouts,
                             fit=lambda row, t: fit_length(row, t, count, filler))
        bar = lt["match_bar"]
        mrep["bar"] = bar
        mrep["pass"] = (mrep["ks"] <= bar["ks_max"] and abs(mrep["mean_ratio"] - 1) <= bar["mean_ratio_tol"]
                        and mrep["type_shares_target"] == mrep["type_shares_matched"])
        mrep["target_records"] = str(a.match_records)
        mrep["target_records_sha256"] = L.sha256_file(a.match_records)
    else:
        picked = prerun_calls(pool, lt["seed"])
        mrep = {"prerun_estimate": True, "calls": len(picked), "pass": None,
                "note": "PREREG_OHS3 type mix, dev lengths; NOT length-matched to OHS-3: not the C1 claim"}
    reqs = build_requests(picked)
    random.Random(lt["seed"]).shuffle(reqs)
    L.blind_print(f"load test {a.name}: {m['kind']} {m['name']}, pool {len(pool)} dev rows ({tdir.name} tokenizer, "
                  f"{time.time() - t0:.0f}s), {len(reqs)} calls, match pass={mrep.get('pass')} ks={mrep.get('ks')}")
    c = client(a.od_url, a.od_token, lt["timeout_s"])
    try:
        h = c.get("/health").json()
    finally:
        c.close()
    if h.get("model") != m["name"] or h.get("config_sha256") != cfg["_sha256"]:
        raise SystemExit(f"the endpoint serves {h.get('model')} / config {str(h.get('config_sha256'))[:16]}, not the "
                         f"pre-registered {m['name']} / {cfg['_sha256'][:16]}")
    tc = token_check(a.od_url, a.od_token, reqs, int(lt["token_check_calls"]), lt["timeout_s"])
    L.blind_print(f"token check: server == local on {tc['equal']}/{tc['calls']} calls")
    levels, nxt = [], int(lt["token_check_calls"])
    for conc in lt["levels"]:
        res, nxt = run_level(a.od_url, a.od_token, reqs, int(conc), float(lt["warmup_s"]), float(lt["seconds_per_level"]),
                             float(lt["timeout_s"]), nxt)
        levels.append(res)
        L.blind_print(f"  c={conc:2d}: {res['decisions_per_hour']:.0f} decisions/h, failed {res['failed_calls']}, "
                      f"client p50 {res['client_ms'].get('p50')} ms, GPU busy {res['model_ms_sum_share_of_window']}")
    good = [lv for lv in levels if lv["failed_calls"] == 0 and lv["decisions_in_window"] > 0]
    best = max(good, key=lambda lv: lv["decisions_per_hour"]) if good else None
    sustained = best["decisions_per_hour"] if best else None
    reasons = []
    if not a.match_records:
        reasons.append("pre-run estimate: not length-matched to the OHS-3 run")
    elif not mrep["pass"]:
        reasons.append("length match failed the pre-registered bar")
    if not tc["pass"]:
        reasons.append("server token count != local token count")
    if sustained is None:
        reasons.append("no level without failed calls")
    routed = None
    if m["kind"] == "cascade":  # the cascade's throughput also depends on how many rows go to the 4B
        lt_share = best.get("routed_share") if best else None
        ohs_share = routed_share_of_records(a.match_records) if a.match_records else None
        tol = float(lt.get("routed_share_tol", 0.05))
        routed = {"load_test": lt_share, "ohs3_timing_pass": ohs_share, "tol": tol,
                  "pass": None if ohs_share is None or lt_share is None else abs(lt_share - ohs_share) <= tol}
        if routed["pass"] is False:
            reasons.append(f"cascade routed share on dev ({lt_share}) differs from the OHS-3 pass ({ohs_share}) by > {tol}")
    S = {"name": a.name, "config_sha256": cfg["_sha256"], "system": m["key"], "kind": m["kind"], "model": m["name"],
         "readout": m["readout_choice"], "dev_only": True, "url_host": a.od_url.split("//")[-1].split("/")[0],
         "endpoint_health": {k: h.get(k) for k in ("model", "readout", "path", "graphs", "region", "gpu", "prism_x")},
         "script_sha256": L.sha256_file(Path(__file__)), "settings": lt, "overrides": overrides, "match": mrep,
         "token_check": tc, "levels": levels, "sustained_rule": lt["sustained_rule"],
         "sustained_decisions_per_hour": sustained, "sustained_at_concurrency": best["concurrency"] if best else None,
         "cascade_routed_share": routed,
         "c1": c1_block(cfg, sustained), "valid_for_c1": not reasons, "invalid_reasons": reasons, "utc": L.utc(),
         "note": "serving batch policy = one request at a time under the GPU lock (as served); dev rows only"}
    (out / "summary.json").write_text(json.dumps(S, indent=1, default=str))
    c1 = S["c1"]
    L.blind_print(f"sustained {sustained} decisions/h at c={S['sustained_at_concurrency']}; C1 $/1K at 100% "
                  f"{c1.get('usd_per_1k_at_100pct')}, at util {c1.get('utilisation_for_claim')}: "
                  f"{c1.get('usd_per_1k_at_claim_util')} (rate {c1.get('rate_usd_h_effective')}/h); valid for C1: "
                  f"{S['valid_for_c1']} {reasons}")
    L.blind_print(f"wrote {out / 'summary.json'}")
    return S


if __name__ == "__main__":
    main()
