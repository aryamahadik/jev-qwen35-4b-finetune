"""End-to-end DRY RUN of the OHS-3 harness on CPU, on the SYNTHETIC stand-in (dev rows), with fake predictors.
No GPU, no Modal, no paid call, no network beyond 127.0.0.1, and the real OHS-3 file is never opened.

  cd ~/Documents/jev/opendecide-data/lean && ../.venv/bin/python prep89/dryrun_ohs3.py

Steps (each is the same script, with the same flags, that the real run uses; only --root / --backend / fake URL differ):
  0. unit tests (prep89/test_ohs3_prep.py) and a fresh synthetic root (make_synthetic_ohs3.py) + a filled dry config;
  1. (a) Jev: ohs3_jev_collect.py runs a byte-identical copy of run_jev.py twice (jev_guard, jev_r2_guard) against a fake
     /v1/systemone on 127.0.0.1 (planted accuracy, 1% transient 503s, 3 states that fail every attempt of the first
     pass -> the resume pass must answer them); our raw->preds converter must equal run_jev.py's output byte for byte;
  2. (b) OpenDecide batch run (ohs3_od_run.py): tiny random Qwen3 + real 4B-E tokenizer through the real decoder_io
     path, interrupted after 2 chunks and resumed; a third start must be refused (rule 4); the "2B": tiny random Qwen3
     + real 2B tokenizer + an ACTIVE PRISM-X control plane (eager, the real decoder_io/prism_x code); an oracle model
     (planted accuracy); the offline cascade 2B -> 4B; then (d) the identity-view check: each batch run's <name>_1v
     equals a fresh decoder_io.predict() and <name> equals predict(tta_choice=True) of the same model, token counts
     are in the metas;
  3. (c) timing: ohs3_serve.py (tiny model, A5 decider) on 127.0.0.1 + ohs3_timing.py, interleaved with the fake Jev,
     first 300 calls then resumed to all 2,456; parity of the served answers with the scored batch read; the served
     answers also written as a scored run (D1 = served_h100) and the harness's Jev answers as a run (D2) to prove both
     options' plumbing; per-call input/output tokens of both systems in every record; the C1 load test
     (load_test_c1.py) against the same endpoint, length-matched to the pass's logged token counts, and its H100 plan
     (--plan: exact commands and cost for the 4B, the 2B and the cascade);
     then the 2B served EAGERLY (PRISM-X; 300 calls, parity with its batch run) and the CASCADE served on one endpoint
     (2B eager + 4B; dev smoke, all 2,456 calls timed with routing, parity with the offline cascade, the served
     cascade written as its scored run);
  4. (d) ohs3_final_table.py: score_ohs3.py (unchanged, --allow-deviation for the synthetic hashes, 10,000 resamples)
     on every configuration + the final table (C1 from the load test at the region rate; the 2B and cascade passes
     as extra speed rows; token rows);
  5. blind audit: no state or instruction text in any output this harness printed or logged.
Writes prep89/dryrun/DRYRUN_REPORT.json.
"""
from __future__ import annotations

import json
import os
import subprocess
import sys
import time
from pathlib import Path

PREP = Path(__file__).resolve().parent
sys.path.insert(0, str(PREP))
import fake_jev_server as F  # noqa: E402
import make_synthetic_ohs3 as MS  # noqa: E402
import ohs3_lib as L  # noqa: E402

DRY = PREP / "dryrun"
ROOT = DRY / "root"
CFG = DRY / "config_dryrun.json"
PY = str(L.PY)
LOGS = []  # every stdout/stderr text the harness produced (for the blind audit)
REPORT = {"started_utc": L.utc(), "steps": {}}


def sh(args, expect_rc=0, name=None):
    t = time.time()
    r = subprocess.run([PY, *args], cwd=str(L.LEAN), capture_output=True, text=True)
    out = r.stdout + r.stderr
    LOGS.append(out)
    tag = name or Path(args[0]).name
    print(f"--- {tag} (exit {r.returncode}, {time.time() - t:.0f}s)\n" + "\n".join(out.strip().splitlines()[-12:]), flush=True)
    if expect_rc is not None and r.returncode != expect_rc:
        raise SystemExit(f"{tag}: exit {r.returncode}, expected {expect_rc}")
    return r


class FailProxy:
    """127.0.0.1 proxy in front of our dry-run endpoint. The next N /decide requests for chosen states get HTTP 503, so
    the timing harness's refill of a SCORED side (D1 = served_h100) is exercised. Dry run only."""

    def __init__(self, target):
        import threading
        from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

        import httpx
        self.fail_left, self.lock, self.injected = {}, threading.Lock(), 0
        client = httpx.Client(base_url=target, timeout=60)
        px = self

        class H(BaseHTTPRequestHandler):
            protocol_version = "HTTP/1.1"

            def _send(self, code, body, ctype="application/json"):
                self.send_response(code)
                self.send_header("Content-Type", ctype)
                self.send_header("Content-Length", str(len(body)))
                self.end_headers()
                self.wfile.write(body)

            def do_POST(self):
                body = self.rfile.read(int(self.headers.get("Content-Length") or 0))
                st = json.loads(body).get("state") if self.path.rstrip("/") == "/decide" else None
                with px.lock:
                    left = px.fail_left.get(st, 0)
                    if left > 0:
                        px.fail_left[st] = left - 1
                        px.injected += 1
                if left > 0:
                    return self._send(503, b'{"error": "dry-run injected failure"}')
                r = client.post(self.path, content=body, headers={"Authorization": self.headers.get("Authorization", ""),
                                                                  "Content-Type": "application/json"})
                self._send(r.status_code, r.content, r.headers.get("content-type", "application/json"))

            def do_GET(self):
                r = client.get(self.path, headers={"Authorization": self.headers.get("Authorization", "")})
                self._send(r.status_code, r.content, r.headers.get("content-type", "application/json"))

            def log_message(self, *a):
                pass

        class S(ThreadingHTTPServer):
            daemon_threads = True

        self.srv = S(("127.0.0.1", 0), H)
        self.url = f"http://127.0.0.1:{self.srv.server_address[1]}"
        threading.Thread(target=self.srv.serve_forever, daemon=True).start()

    def fail_next(self, states, n):
        with self.lock:
            for s in states:
                self.fail_left[s] = n


def start_server(tag, args, tok):
    """ohs3_serve.py on 127.0.0.1 in a subprocess -> (process, url, log file)."""
    ready = DRY / f"serve_ready_{tag}.json"
    ready.unlink(missing_ok=True)
    slog = open(DRY / f"serve_stdout_{tag}.txt", "w")
    sp = subprocess.Popen([PY, "prep89/ohs3_serve.py", "--config", str(CFG), "--root", str(ROOT), "--token", tok,
                           "--ready-file", str(ready), "--max-s", "3000", *args],
                          cwd=str(L.LEAN), stdout=slog, stderr=subprocess.STDOUT)
    t0 = time.time()
    while not ready.exists():
        if sp.poll() is not None or time.time() - t0 > 300:
            raise SystemExit(f"server {tag} did not start")
        time.sleep(0.5)
    time.sleep(0.2)
    return sp, json.loads(ready.read_text())["url"], slog


def stop_server(sp, url, tok, slog, tag):
    import httpx
    try:
        httpx.post(url + "/shutdown", headers={"Authorization": f"Bearer {tok}"}, timeout=10)
    except Exception:  # noqa: BLE001
        pass
    try:
        sp.wait(timeout=30)
    except subprocess.TimeoutExpired:
        sp.kill()
    slog.close()
    LOGS.append((DRY / f"serve_stdout_{tag}.txt").read_text())


def identity_view_check(name, be, n=150):
    """(d) The batch run saved the identity view next to the 2-view average from the same reads: on a seeded subset
    (+ the 40-option rows) <name>_1v == decoder_io.predict() and <name> == predict(tta_choice=True) of the same model
    (tolerance for padding noise; argmax identical), yes/no rows identical in both files, choice rows differ, and the
    run's token counts in the meta."""
    import hashlib
    pd = ROOT / "preds_ohs3"
    f1 = {o["id"]: o["probs"] for o in L.read_jsonl(pd / f"{name}_1v.jsonl")}
    f2 = {o["id"]: o["probs"] for o in L.read_jsonl(pd / f"{name}.jsonl")}
    rows = L.read_jsonl(ROOT / "data" / "ohs3.jsonl")
    sub = sorted(rows, key=lambda r: hashlib.sha256(f"idv:{r['id']}".encode()).hexdigest())[:n]
    sub += [r for r in rows if r["qtype"] == "choice" and len(r["options"]) >= 40 and r not in sub][:10]
    dio = be["dio"]
    r1 = dio.predict(be["model"], be["tok"], sub, dev="cpu")
    r2 = dio.predict(be["model"], be["tok"], sub, dev="cpu", tta_choice=True, tta_noul=False)
    d1 = max(abs(f1[r["id"]][k] - r1[i][k]) for i, r in enumerate(sub) for k in r1[i])
    d2 = max(abs(f2[r["id"]][k] - r2[i][k]) for i, r in enumerate(sub) for k in r2[i])
    am = lambda P, Q: all(max(P, key=P.get) == max(Q, key=Q.get) for P, Q in zip(P, Q))  # noqa: E731
    yn_same = all(f1[r["id"]] == f2[r["id"]] for r in rows if r["qtype"] == "noul")
    ch_diff = sum(f1[r["id"]] != f2[r["id"]] for r in rows if r["qtype"] == "choice")
    tokm = json.loads((pd / f"{name}.meta.json").read_text())["tokens"]
    out = {"rows_checked": len(sub), "max_abs_diff_1v_vs_predict": d1, "max_abs_diff_2view_vs_predict_tta": d2,
           "argmax_identical": am([f1[r["id"]] for r in sub], r1) and am([f2[r["id"]] for r in sub], r2),
           "yes_no_rows_identical_in_both_files": yn_same, "choice_rows_where_2view_differs": ch_diff,
           "tokens": {k: tokm.get(k) for k in ("rows_counted", "input_tokens_first_view", "input_tokens_all_reads",
                                               "all_reads_over_first_view", "output_tokens")}}
    out["pass"] = (d1 <= 1e-5 and d2 <= 1e-5 and out["argmax_identical"] and yn_same and ch_diff > 0
                   and tokm["rows_counted"] == len(rows) and tokm["all_reads_over_first_view"] > 1)
    return out


def make_config():
    t = json.loads((PREP / "ohs3_config.template.json").read_text())
    t["_doc"] = "DRY RUN config (synthetic stand-in, CPU). Dummy values; NOT a pre-registration."
    # the template leaves the shipped 4B to gate job 3 (A8-prime); the tiny backend reads 4B-E's tokenizer folder, so
    # the dry run's adapter sha256 is 4B-E's (ohs3_backends.TINY_TOKENIZER_DIR)
    t["models"]["4b"].update(name="dry_4b", adapter_sha256=t["models"]["4b"]["_candidates"]["q35_4b_pxE"]["adapter_sha256"],
                             readout_choice="2view", T_primary={"noul": 0.95, "choice": 1.05},
                             T_single={"noul": 0.95, "choice": 1.0}, T_fit_log="(dry run)")
    # the 2B: tiny random Qwen3 + the real 2B tokenizer + PRISM-X (authority + option head; the shadow heads need
    # Qwen3.5 Gated DeltaNet layers that the Mac's transformers lacks), eager, T != 1 so T and routing are exercised
    t["models"]["2b"].update(run_on_ohs3=True, name="dry_2b", revision="0" * 40, adapter_sha256="0" * 64,
                             readout_choice="2view", T_primary={"noul": 0.9, "choice": 1.1},
                             T_single={"noul": 1.0, "choice": 1.0}, T_fit_log="(dry run)",
                             prism_x={"authority": True, "option_head": True}, prism_x_sha256="0" * 64,
                             cuda_graphs=False)
    t["models"]["oracle"] = {**t["models"]["2b"], "_note": "dry run only: planted logits from the synthetic gold",
                             "name": "dry_oracle", "prism_x": None, "T_primary": {"noul": 1.0, "choice": 1.0}}
    t["cascade"].update(run=True, name="dry_cascade", small="2b", big="4b", tau=0.6, w_big=0.8, route_on="primary",
                        tau_fit_log="(dry run)")
    t["decisions"].update(od_scored_run="L4_batch", jev_timing="extra_pass")
    t["hosting"].update(endpoint="local_cpu_dryrun", customer_usable="no (dry run)")
    t["speed"]["rule_S1"] = "p50 CI (Jev - OD) entirely above 0 AND p95 point estimate lower"
    t["cost"].update(od_decisions_per_hour_sustained="load_test", utilisation_for_claim=0.4, l4_usd_per_hour=0.85,
                     c3_od_usd_per_1k=0.039)
    CFG.write_text(json.dumps(t, indent=2))


def main():
    DRY.mkdir(exist_ok=True)
    # ---- 0
    sh(["prep89/test_ohs3_prep.py"], name="unit tests")
    built = MS.build(ROOT)
    make_config()
    REPORT["steps"]["synthetic"] = {"counts": built["counts"], "tracks": built["tracks"], "sha256": built["sha256"]}
    rows = {r["id"]: r for r in L.read_jsonl(ROOT / "data" / "ohs3.jsonl")}
    # ---- 1: Jev through run_jev.py (byte-identical copy) and the fake endpoint
    srv, jurl, fake = F.start_in_thread(ROOT, hard_fail_calls=3, fail_rate=0.01)
    sh(["prep89/ohs3_jev_collect.py", "--root", str(ROOT), "--fake-url", jurl], name="(a) ohs3_jev_collect")
    pd = ROOT / "preds_ohs3"
    conv = {}
    for tag in ("jev_guard", "jev_r2_guard"):
        mine = "".join(json.dumps(o) + "\n" for o in L.jev_raw_to_preds(pd / f"{tag}_raw.jsonl", rows, tag))
        conv[tag] = mine == (pd / f"{tag}.jsonl").read_text()
        s = json.loads((ROOT / "logs" / "ohs3" / f"jev_collect_{tag}.json").read_text())
        REPORT["steps"][f"jev_{tag}"] = {k: s[k] for k in ("calls_answered", "calls_missing", "passes",
                                                           "failed_attempt_records", "calls_not_pinned_model")}
    assert all(conv.values()), conv
    assert REPORT["steps"]["jev_jev_guard"]["passes"] >= 2, "the hard failures should need a resume pass"
    REPORT["steps"]["jev_converter_equals_run_jev"] = conv
    # ---- 2: OpenDecide batch runs (interrupt + resume, rule-4 refusal), oracle, cascade
    base = ["prep89/ohs3_od_run.py", "--root", str(ROOT), "--config", str(CFG)]
    sh(base + ["--model-key", "4b", "--backend", "tiny", "--stop-after-chunks", "2"], name="(b) od_run tiny, interrupted")
    sh(base + ["--model-key", "4b", "--backend", "tiny"], name="(b) od_run tiny, resumed")
    r = sh(base + ["--model-key", "4b", "--backend", "tiny"], expect_rc=1, name="(b) od_run tiny, 3rd start")
    assert "rule 4" in r.stdout + r.stderr
    sh(base + ["--model-key", "2b", "--backend", "tiny_px"], name="(b) od_run 2B (tiny + PRISM-X, eager)")
    sh(base + ["--model-key", "oracle", "--backend", "oracle"], name="(b) od_run oracle")
    sh(["prep89/ohs3_cascade.py", "--root", str(ROOT), "--config", str(CFG)], name="(b) cascade (offline)")
    REPORT["steps"]["od_runs"] = [x for x in L.ledger(ROOT)]
    # ---- (d) the identity view is saved next to the 2-view average (same reads), for the 4B and the PRISM-X 2B
    import ohs3_backends as B
    cfg = L.load_config(CFG)
    be = B.load_tiny(cfg["models"]["4b"])
    be2 = B.load_tiny_px(cfg["models"]["2b"])  # after the 4B, as on the cascade host
    idv = {"dry_4b": identity_view_check("dry_4b", be), "dry_2b": identity_view_check("dry_2b", be2)}
    REPORT["steps"]["identity_view_saved"] = idv
    assert all(v["pass"] for v in idv.values()), idv
    # ---- 3: timing, served by the A5 decider on 127.0.0.1
    tok = "dryrun-token-" + "x" * 16
    ready = DRY / "serve_ready.json"
    ready.unlink(missing_ok=True)
    slog = open(DRY / "serve_stdout.txt", "w")
    sp = subprocess.Popen([PY, "prep89/ohs3_serve.py", "--config", str(CFG), "--model-key", "4b", "--backend", "tiny",
                           "--root", str(ROOT), "--token", tok, "--ready-file", str(ready), "--max-s", "3000"],
                          cwd=str(L.LEAN), stdout=slog, stderr=subprocess.STDOUT)
    try:
        t0 = time.time()
        while not ready.exists():
            if sp.poll() is not None or time.time() - t0 > 300:
                raise SystemExit("server did not start")
            time.sleep(0.5)
        ourl = json.loads(ready.read_text())["url"]
        # dev smoke of the served path (the GPU pre-check of the real run), refs = the batch read of the same rows
        import hashlib
        for split, n in (("dev_nc", 40), ("devp_card", 30)):
            drows = sorted(L.read_jsonl(L.LEAN / "data" / f"{split}.jsonl"),
                           key=lambda r: hashlib.sha256(f"smoke:{r['id']}".encode()).hexdigest())[:n]
            (ROOT / f"preds_{split}").mkdir(exist_ok=True)
            for b_, tag_ in ((be, ""), (be2, "2b_")):
                p1, pr = L.a5_read(b_["dio"], b_["model"], b_["ro"], drows, "cpu", "2view")
                for nm, P in ((f"dry_ref_{tag_}1v", p1), (f"dry_ref_{tag_}2v", pr)):
                    L.write_jsonl_atomic(ROOT / f"preds_{split}" / f"{nm}.jsonl",
                                         [{"id": r["id"], "model": nm, "probs": p} for r, p in zip(drows, P)])
        sh(["prep89/ohs3_timing.py", "--root", str(ROOT), "--config", str(CFG), "--od-url", ourl, "--od-token", tok,
            "--name", "dry_smoke", "--dev-smoke", "dev_nc:40,devp_card:30", "--smoke-ref-root", str(ROOT),
            "--smoke-ref-1v", "dry_ref_1v", "--smoke-ref-2v", "dry_ref_2v"], name="(c0) dev smoke of the endpoint")
        sm = json.loads((ROOT / "logs" / "ohs3" / "timing" / "dry_smoke" / "dev_smoke.json").read_text())
        REPORT["steps"]["dev_smoke"] = {"pass": sm["pass"], **{k: {kk: vv for kk, vv in v.items() if kk != "client_ms"}
                                                               for k, v in sm["splits"].items()}}
        assert sm["pass"], "dev smoke failed"
        proxy = FailProxy(ourl)  # injects failures in front of our endpoint (refill check)
        tb = ["prep89/ohs3_timing.py", "--root", str(ROOT), "--config", str(CFG), "--od-url", proxy.url, "--od-token",
              tok, "--fake-jev-url", jurl, "--name", "dry_timing"]
        sh(tb + ["--limit", "300"], name="(c) timing, first 300 calls")
        # 3 not-yet-timed calls per system fail every timed attempt (3) and the first refill attempt: their timed
        # records must sit at the 30 s timeout and the refill must still answer them (both sides are scored below)
        trec = ROOT / "logs" / "ohs3" / "timing" / "dry_timing" / "records.jsonl"
        timed_ids = {r["call_id"] for r in L.read_jsonl(trec)}
        all_calls = L.read_jsonl(ROOT / "data" / "ohs3_calls.jsonl")
        n_state = {}
        for c in all_calls:  # a twin call has its base call's state: inject only on states used by one call
            n_state[c["state"]] = n_state.get(c["state"], 0) + 1
        calls = sorted((c for c in all_calls if c["call_id"] not in timed_ids and n_state[c["state"]] == 1),
                       key=lambda c: L.sha256_bytes(f"dryfail:{c['call_id']}".encode()))
        fail_od, fail_jev = calls[0:3], calls[2:5]  # one call fails on both sides
        proxy.fail_next([c["state"] for c in fail_od], 4)
        fake.fail_next([c["state"] for c in fail_jev], 4)
        sh(tb + ["--scored-name", "dry_4b", "--od-preds-name", "dry_4b_served", "--jev-preds-tag", "jevh_guard"],
           name="(c) timing, resumed to all calls (+ injected failures, refill)")
        recs = L.read_jsonl(trec)
        refill_check = {}
        for who, cs in (("od", fail_od), ("jev", fail_jev)):
            ids = {c["call_id"] for c in cs}
            timed_r = [r for r in recs if r["who"] == who and r["call_id"] in ids and not r.get("refill")]
            refill_ok = {r["call_id"] for r in recs if r["who"] == who and r["call_id"] in ids and r.get("refill")
                         and not r["failed"]}
            refill_check[who] = {"injected_calls": len(ids), "timed_failed_at_timeout":
                                 sum(r["failed"] and r["client_ms"] == 30000.0 for r in timed_r),
                                 "refill_answered": len(refill_ok)}
            assert refill_check[who]["timed_failed_at_timeout"] == 3 and len(refill_ok) == 3, refill_check
        refill_check["proxy_injected_requests"] = proxy.injected
        REPORT["steps"]["refill"] = refill_check
        proxy.srv.shutdown()
        # ---- C1 load test (DEV rows) against the same endpoint, length-matched to the pass's logged token counts
        sh(["prep89/load_test_c1.py", "--config", str(CFG), "--model-key", "4b", "--od-url", ourl, "--od-token", tok,
            "--name", "dry_c1", "--root", str(ROOT), "--match-records", str(trec), "--tokenizer-dir",
            str(B.TINY_TOKENIZER_DIR), "--levels", "1,2,4", "--seconds-per-level", "3", "--warmup-s", "1"],
           name="(c) C1 load test (dev rows, length-matched)")
        lts = json.loads((ROOT / "logs" / "ohs3" / "load_test" / "dry_c1" / "summary.json").read_text())
        REPORT["steps"]["load_test"] = {k: lts[k] for k in ("sustained_decisions_per_hour", "sustained_at_concurrency",
                                                             "valid_for_c1", "invalid_reasons", "token_check", "c1")}
        REPORT["steps"]["load_test"]["match"] = {k: lts["match"][k] for k in ("calls", "pool_rows", "length_fit", "distinct_dev_rows", "ks",
                                                                               "mean_ratio", "match_key", "pass")}
        REPORT["steps"]["load_test"]["levels"] = [{k: lv[k] for k in ("concurrency", "decisions_per_hour", "failed_calls",
                                                                      "model_ms_sum_share_of_window")} for lv in lts["levels"]]
        assert lts["valid_for_c1"] and lts["token_check"]["pass"] and lts["match"]["pass"], lts["invalid_reasons"]
        plans = {}
        for k in ("4b", "2b", "cascade"):  # the H100 plan (exact commands + cost) from the same config, no endpoint
            r_ = sh(["prep89/load_test_c1.py", "--config", str(CFG), "--model-key", k, "--plan"],
                    name=f"(c) C1 load test plan ({k})")
            pl = json.loads(r_.stdout)
            plans[k] = {x: pl[x] for x in ("kind", "in_session_min", "new_session_min", "usd_in_timing_session",
                                           "usd_new_session")}
        REPORT["steps"]["load_test"]["h100_plan"] = plans
    finally:
        import httpx
        try:
            httpx.post(ourl + "/shutdown", headers={"Authorization": f"Bearer {tok}"}, timeout=10)
        except Exception:  # noqa: BLE001
            pass
        try:
            sp.wait(timeout=30)
        except subprocess.TimeoutExpired:
            sp.kill()
        slog.close()
        LOGS.append((DRY / "serve_stdout.txt").read_text())
    tsum = json.loads((ROOT / "logs" / "ohs3" / "timing" / "dry_timing" / "summary.json").read_text())
    REPORT["steps"]["timing"] = {"od": tsum["od"]["client_ms"], "jev": tsum["jev"]["client_ms"],
                                 "paired_calls": tsum["paired"]["calls"], "S1": tsum["S1_faster"],
                                 "parity_pass": tsum.get("parity_pass"), "parity": tsum.get("parity_vs_scored"),
                                 "od_preds": tsum.get("od_preds"), "jev_preds": tsum.get("jev_preds"),
                                 "jev_tokens_per_call": tsum["jev"].get("input_tokens_per_call_mean")}
    assert tsum["paired"]["calls"] == 2456 and tsum["S1_faster"]["complete"], "timing incomplete"
    assert tsum["od"]["failed_calls"] >= 3 and tsum["jev"]["failed_calls"] >= 3, "injected failures not timed"
    assert tsum["jev_preds"]["rows"] == len(rows), "harness Jev run must answer every row after the refill"
    assert tsum["parity_pass"], "served answers differ from the scored batch read"
    tko, tkj = tsum["od"]["tokens"], tsum["jev"]["tokens"]
    REPORT["steps"]["timing"]["tokens"] = {"od": {k: tko[k] for k in ("input_tokens", "output_tokens",
                                                                      "input_tokens_first_view")},
                                           "od_all_reads_over_first_view": tko["all_reads_over_first_view"],
                                           "jev": {k: tkj[k] for k in ("input_tokens", "output_tokens")},
                                           "token_priced_usd_per_1k_calls": tsum.get("token_priced_usd_per_1k_calls")}
    assert tko["input_tokens"]["calls_with_count"] == tko["calls_answered"] == tsum["od"]["calls_timed"] - \
        tsum["od"]["failed_calls"], "every answered OD call must log its token counts"
    assert tkj["input_tokens"]["calls_with_count"] == tkj["calls_answered"] and tkj["output_tokens"]["calls_with_count"] \
        == tkj["calls_answered"], "every answered Jev call must log its input and output tokens"
    assert tko["output_tokens"]["total"] == 0 and tko["all_reads_over_first_view"] > 1
    assert tko["complete"] is True and tkj["complete"] is True, "token counts must be complete on both sides"
    REPORT["steps"]["timing"]["tokens"]["complete"] = {"od": tko["complete"], "jev": tkj["complete"]}
    # ---- 3b: the 2B served EAGERLY (PRISM-X I path) and timed (300 calls; parity with its batch run)
    try:
        sp2, url2, log2 = start_server("2b", ["--model-key", "2b", "--backend", "tiny_px"], tok)
        try:
            sh(["prep89/ohs3_timing.py", "--root", str(ROOT), "--config", str(CFG), "--model-key", "2b", "--od-url",
                url2, "--od-token", tok, "--name", "dry_smoke_2b", "--dev-smoke", "dev_nc:20,devp_card:20",
                "--smoke-ref-root", str(ROOT), "--smoke-ref-1v", "dry_ref_2b_1v", "--smoke-ref-2v", "dry_ref_2b_2v"],
               name="(c0) dev smoke of the 2B endpoint (eager, PRISM-X)")
            sm2 = json.loads((ROOT / "logs" / "ohs3" / "timing" / "dry_smoke_2b" / "dev_smoke.json").read_text())
            assert sm2["pass"], "2B dev smoke failed"
            sh(["prep89/ohs3_timing.py", "--root", str(ROOT), "--config", str(CFG), "--model-key", "2b", "--od-url",
                url2, "--od-token", tok, "--fake-jev-url", jurl, "--name", "dry_timing_2b", "--limit", "300",
                "--scored-name", "dry_2b"], name="(c) timing, 2B (eager), 300 calls")
        finally:
            stop_server(sp2, url2, tok, log2, "2b")
        t2 = json.loads((ROOT / "logs" / "ohs3" / "timing" / "dry_timing_2b" / "summary.json").read_text())
        REPORT["steps"]["timing_2b"] = {"od": t2["od"]["client_ms"], "paths": t2["od"]["paths"],
                                        "paired_calls": t2["paired"]["calls"], "S1": t2["S1_faster"]["verdict"],
                                        "parity_pass": t2["parity_pass"], "tokens_mean": t2["od"]["tokens"]["input_tokens"]["mean"],
                                        "dev_smoke_pass": sm2["pass"]}
        assert set(t2["od"]["paths"]) == {"eager"} and t2["parity_pass"], "2B must be served eagerly, = its batch run"
        # ---- 3c: the cascade on ONE endpoint (4B tiny first, then the PRISM-X 2B), timed end to end with routing
        spc, urlc, logc = start_server("cascade", ["--model-key", "cascade", "--backend", "tiny",
                                                   "--small-backend", "tiny_px"], tok)
        try:
            sh(["prep89/ohs3_timing.py", "--root", str(ROOT), "--config", str(CFG), "--model-key", "cascade",
                "--od-url", urlc, "--od-token", tok, "--name", "dry_smoke_cascade", "--dev-smoke",
                "dev_nc:20,devp_card:20", "--smoke-ref-root", str(ROOT), "--smoke-ref-1v", "dry_ref_2b_1v",
                "--smoke-ref-2v", "dry_ref_2b_2v", "--smoke-ref-big-1v", "dry_ref_1v"],
               name="(c0) dev smoke of the cascade endpoint")
            smc = json.loads((ROOT / "logs" / "ohs3" / "timing" / "dry_smoke_cascade" / "dev_smoke.json").read_text())
            assert smc["pass"], "cascade dev smoke failed"
            sh(["prep89/ohs3_timing.py", "--root", str(ROOT), "--config", str(CFG), "--model-key", "cascade",
                "--od-url", urlc, "--od-token", tok, "--fake-jev-url", jurl, "--name", "dry_timing_cascade",
                "--scored-name", "dry_cascade", "--od-preds-name", "dry_cascade_served"],
               name="(c) timing, cascade end to end (all calls; parity with the offline cascade; served preds)")
        finally:
            stop_server(spc, urlc, tok, logc, "cascade")
    finally:
        srv.shutdown()
    tc_ = json.loads((ROOT / "logs" / "ohs3" / "timing" / "dry_timing_cascade" / "summary.json").read_text())
    offm = json.loads((ROOT / "preds_ohs3" / "dry_cascade_cal.meta.json").read_text())
    REPORT["steps"]["timing_cascade"] = {"od": tc_["od"]["client_ms"], "paired_calls": tc_["paired"]["calls"],
                                         "S1": tc_["S1_faster"]["verdict"], "cascade": tc_["od"]["cascade"],
                                         "offline_routed": offm["routed"], "parity": tc_["parity_vs_scored"],
                                         "parity_pass": tc_["parity_pass"], "od_preds": tc_.get("od_preds"),
                                         "paths": tc_["od"]["paths"], "dev_smoke_pass": smc["pass"],
                                         "dev_smoke": {k: {kk: vv for kk, vv in v.items() if kk not in ("client_ms",
                                                                                                      "input_tokens")}
                                                       for k, v in smc["splits"].items()}}
    pv = tc_["parity_vs_scored"]
    # bars, not exact equality: the served reads are batch 1 and the offline cascade used batch reads (padding noise
    # of ~1e-6 could move a row whose top probability sits on tau); the exact numbers are in the report
    assert tc_["paired"]["calls"] == 2456 and tc_["parity_pass"], "cascade timing incomplete or parity failed"
    assert pv["routed_set_vs_dry_cascade"]["pass"] and abs(tc_["od"]["cascade"]["routed_rows"] - offm["routed"]) <= \
        0.01 * offm["rows"] and abs(tc_["od_preds"]["routed"] - offm["routed"]) <= 0.01 * offm["rows"], pv
    exact_c = pv["routed_set_vs_dry_cascade"]["agree"] == 1.0 and pv["final_vs_dry_cascade_cal"]["argmax_agree"] == 1.0
    REPORT["steps"]["timing_cascade"]["routing_and_argmax_identical_to_offline"] = exact_c
    # ---- 4: score_ohs3.py + final table
    models = ("dry_4b_cal,dry_4b_1v_cal,dry_2b_cal,dry_2b_1v_cal,dry_oracle_cal,dry_cascade_cal,dry_4b_served_cal,"
              "dry_cascade_served_cal")
    td_ = ROOT / "logs" / "ohs3" / "timing"
    sh(["prep89/ohs3_final_table.py", "--root", str(ROOT), "--config", str(CFG), "--models", models, "--timing",
        str(td_ / "dry_timing" / "summary.json"), "--timing-extra",
        f"2b={td_ / 'dry_timing_2b' / 'summary.json'},cascade={td_ / 'dry_timing_cascade' / 'summary.json'}",
        "--load-test", str(ROOT / "logs" / "ohs3" / "load_test" / "dry_c1" / "summary.json"), "--allow-deviation"],
       name="(d) score + final table")
    LOGS.append((ROOT / "logs" / "ohs3" / "score_ohs3_stdout.txt").read_text())
    sc = json.loads((ROOT / "results_ohs3" / "score_ohs3_all.json").read_text())
    dev = sc["deviations"]
    assert all("sha256" in d for d in dev), dev  # only the synthetic-hash deviations
    a, b = sc["models"]["dry_4b_cal"]["primary"], sc["models"]["dry_4b_served_cal"]["primary"]
    same = all(abs(a[k]["od"] - b[k]["od"]) < 1e-9 for k in a)
    REPORT["steps"]["score"] = {"deviations": dev, "n_boot": sc["n_boot"], "models": sorted(sc["models"]),
                                "served_equals_batch_scores": same,
                                "primary": {m: {k: [round(v["od"], 4), round(v["jev"], 4), round(v["diff"], 4), v["verdict"]["label"]]
                                                for k, v in r["primary"].items()} for m, r in sc["models"].items()}}
    assert same, "the served run must score exactly like the batch run of the same model"
    a, b = sc["models"]["dry_cascade_cal"]["primary"], sc["models"]["dry_cascade_served_cal"]["primary"]
    same_c = all(abs(a[k]["od"] - b[k]["od"]) < 1e-6 for k in a)
    REPORT["steps"]["score"]["served_cascade_equals_offline_cascade_scores"] = same_c
    REPORT["steps"]["score"]["served_minus_offline_cascade"] = {k: b[k]["od"] - a[k]["od"] for k in a}
    if exact_c:  # identical routing and argmax: the scores must be identical
        assert same_c, "the served cascade must score like the offline cascade (same rule, same reads)"
    ft = json.loads((ROOT / "results_ohs3" / "final_table.json").read_text())
    REPORT["steps"]["final_table"] = {"rows": [(r["condition"], r["metric"], r["verdict"], r["win"]) for r in ft["rows"]],
                                      "extra_system_rows": [(r["condition"], r["metric"], r["verdict"])
                                                            for r in ft["extra_system_rows"]],
                                      "C1": ft["cost"]["C1"], "all_measured_won": ft["all_measured_won"],
                                      "file": str(ROOT / "results_ohs3" / "final_table.md")}
    assert ft["cost"]["C1"].get("od_decisions_per_hour_sustained") == lts["sustained_decisions_per_hour"] and \
        ft["cost"]["C1"]["region_multiplier"] == L.region_multiplier(cfg["hosting"]["region"]), ft["cost"]["C1"]
    assert any("2b" in r[0] for r in REPORT["steps"]["final_table"]["extra_system_rows"]) and \
        any("cascade" in r[0] for r in REPORT["steps"]["final_table"]["extra_system_rows"])
    # ---- 5: blind audit over every text the harness printed or logged
    for p in (ROOT / "logs").rglob("*"):
        if p.is_file() and p.suffix in (".log", ".txt"):
            LOGS.append(p.read_text())
    text = "\n".join(LOGS)
    snippets = set()
    for r in rows.values():
        for fld in ("state", "instructions", "card"):
            v = (r.get(fld) or "").strip()
            if len(v) >= 40:
                snippets.add(v[:40])
    hits = [s for s in snippets if s in text]
    REPORT["steps"]["blind_audit"] = {"texts_scanned": len(LOGS), "chars": len(text), "snippets_checked": len(snippets),
                                      "hits": len(hits)}
    assert not hits, f"{len(hits)} item-text snippets found in harness output"
    REPORT["finished_utc"] = L.utc()
    REPORT["result"] = "PASS"
    (DRY / "DRYRUN_REPORT.json").write_text(json.dumps(REPORT, indent=1, default=str))
    print("\nDRY RUN PASS: " + json.dumps({k: REPORT["steps"][k] for k in ("blind_audit",)}) +
          f"\nreport: {DRY / 'DRYRUN_REPORT.json'}\ntable:  {ROOT / 'results_ohs3' / 'final_table.md'}")


if __name__ == "__main__":
    main()
