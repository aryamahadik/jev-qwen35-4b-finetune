"""SPEED-1 end-to-end verification on the Mac (CPU only; hosting/SPEED1_DESIGN.md). NEW file: nothing pinned or
existing is edited, nothing remote or paid runs, and only the gate dev splits, the stored C1 reads, speed/workloads/
and speed/cpu_ref/ are read (any split named ohs* is refused before a file is opened).

Default tests (tiny random Qwen3.5 hybrid model + the C1 tokenizer, emulated CUDA graphs; ~5-8 min on an M4):
  1. test_ids_hf_and_sglang_paths_equal_decoder_io: every P row (all 8,143 gate dev rows), both views: the API v1 body
     speed_bench sends -> fastcore work items (the HF arms' path) -> sglang_host.build_generate_body (the S1/S2 path).
     Prompt text == decoder_io.prompt_texts, input_ids == decoder_io.cand_logits' tokenizer call (truncation at
     MAX_LEN, pads removed), token_ids_logprob == Readout.cand(row) flattened, and the first-view token count == the
     server token check's reference (speed/workloads/token_profile.json).
  2. test_e2e_bench_all_arms: the real servers in-process over HTTP (fast_host: BF16 boot for A0/A1/A2 and an FP8 boot
     for A3; sglang_host's front end for S1 on a fake SGLang that returns the exact fp32 logprobs of the same tiny
     model), driven by the real speed_bench CLI (`ab --go` on small slices of the real P/S/N/R workloads with a short
     window, then `report`). Checks: every arm accepted, flags read back, all levels run without failed calls, P
     answers (and per-view answers) == decoder_io.predict on the same model, A1/A2/S1 parity PASS vs A0, the FP8 bar
     applied to A3, token check equal, reversed-view reconstruction valid, REPORT.md / report.json complete.
     SPEED1_E2E_OUT=DIR keeps the session there (default: pytest's tmp dir).
  3. test_pinned_files_unchanged: git diff of the pinned lean/*.py files and the existing hosting/*.py files is empty.

Opt-in, REAL C1 (Qwen3.5-4B @ 851bf6e8 + LoRA q35_4b_main500k merged in BF16, on CPU; needs the base snapshot in the
local HF cache, read offline; 1-4 h for the whole run, depending on swap: this CPU runs BF16 GEMMs slowly and the
8.4 GB model swaps on 16 GB):
  SPEED1_REAL_CPU=1 ../.venv/bin/python -m pytest hosting/tests/test_e2e_speed1.py -k real -s
      the cheapest noul and choice rows of the 36-row sample through the fast host (A1) == ref36.jsonl bit for bit
  ../.venv/bin/python hosting/tests/test_e2e_speed1.py real-cpu [--out speed/verify/real_cpu] [--quick]
      fast_host's HTTP server (FastEngine, CPU eager, no graphs) + cpu_parity_check.check() on the 36-row sample:
      A0 and A2 (2view as one batch of 2) on the 4 cheapest rows, then A1 (each view batch 1) on all 36; per-row
      records stream to rows_<arm>.jsonl, summary.json compares with the stored L4 reads and with ref36.jsonl
      (2view, identity view and reversed view).
Run from lean/:  ../.venv/bin/python -m pytest hosting/tests/test_e2e_speed1.py -q
Cost guards: no Modal object is created or called, no GPU, no network beyond 127.0.0.1, no OpenRouter call.
"""
from __future__ import annotations

import argparse
import copy
import json
import math
import os
import secrets
import shutil
import subprocess
import sys
import threading
import time
from pathlib import Path

import httpx
import pytest

HOSTING = Path(__file__).resolve().parents[1]
LEAN = HOSTING.parent
for _p in (str(HOSTING), str(LEAN)):
    if _p not in sys.path:
        sys.path.insert(0, _p)
import fast_host as FH  # noqa: E402
import speed_bench as SB  # noqa: E402
from fastcore import readout as R  # noqa: E402
from fastcore import testing as T  # noqa: E402

dio = R.dio
TOKEN = "e2e-speed1-token-0123456789"
ARMS_CFG = json.loads(FH.ARMS_FILE.read_text())
ARMS = ARMS_CFG["arms"]
WORKLOADS = LEAN / "speed" / "workloads"
REAL_OUT = LEAN / "speed" / "verify" / "real_cpu"
REAL_BOOT = {"graphs": False, "eager_warmup": {}, "warm_requests": 0, "selftest": False,
             "decide_timeout_s": 6 * 3600.0}
PINNED = ["decoder_io.py", "prism_x.py", "writeblock.py", "gate_dev.py", "hosting/modal_direct_host.py",
          "hosting/client_bench.py"]
HAVE_TOKENIZER = (T.ADAPTER / "tokenizer.json").exists()


def quiet(*a, **k):
    pass


def _serve_fast(host, token=TOKEN):
    stop = threading.Event()
    srv, st = FH.make_fast_server(0, token, host, stop.set, bind="127.0.0.1")
    threading.Thread(target=srv.serve_forever, daemon=True).start()
    return srv, f"http://127.0.0.1:{srv.server_address[1]}", stop


def _maxdp(p, q, keys):
    return max(abs(float(p[k]) - float(q[k])) for k in keys)


def _top(p, keys):
    return max(keys, key=lambda k: float(p[k]))  # first maximum in key order (gate_dev's rule for choice)


# ====================================================================== REAL C1 on CPU (opt-in / CLI)

def _cheap_rows(rows, n_choice=3, n_noul=1):
    """The cheapest choice rows (2view) and noul rows of the sample, by identity tokens: where batching the two views
    (A0 / A2) differs from reading them one at a time (A1)."""
    ch = sorted((r for r in rows if r["qtype"] == "choice"), key=lambda r: (r["_tokens"], r["id"]))[:n_choice]
    nu = sorted((r for r in rows if r["qtype"] == "noul"), key=lambda r: (r["_tokens"], r["id"]))[:n_noul]
    return nu + ch


def _by_cost(rows):
    return sorted(rows, key=lambda r: (r["_tokens"] * (2 if r["qtype"] == "choice" else 1), r["id"]))


REAL_PLAN = (("A0", _cheap_rows), ("A2", _cheap_rows), ("A1", _by_cost))
QUICK_PLAN = (("A1", lambda rows: _cheap_rows(rows, 1, 1)),)


def view_parity(rows, recs, ref36, stored_identity) -> dict:
    """Per-view comparisons of the fast host's answers (return_views) on choice rows: identity view vs ref36's
    probs_identity (same CPU, same model: expected bit-identical for batch-1 reads) and vs the stored L4 identity read;
    reversed view vs ref36's probs_reversed; plus the 2view / noul answer vs ref36 probs."""
    out = {"identity_vs_ref36": [], "reversed_vs_ref36": [], "identity_vs_stored_L4": [], "answer_vs_ref36": [],
           "identity_flips_vs_ref36": 0, "reversed_flips_vs_ref36": 0, "identity_flips_vs_stored_L4": 0,
           "answer_flips_vs_ref36": 0}
    by = {r["id"]: r for r in rows}
    for rec in recs:
        r, a, x = by[rec["id"]], rec["answer"], ref36.get(rec["id"])
        if x is None or a is None:
            continue
        keys = ["yes", "no"] if r["qtype"] == "noul" else list(r["options"])
        got = {"yes": a["noul"], "no": 1 - a["noul"]} if r["qtype"] == "noul" else a["probabilities"]
        out["answer_vs_ref36"].append(_maxdp(got, x["probs"], keys[:1] if r["qtype"] == "noul" else keys))
        out["answer_flips_vs_ref36"] += _top(got, keys) != _top(x["probs"], keys)
        if r["qtype"] != "choice" or not a.get("view_probabilities"):
            continue
        vi, vr = a["view_probabilities"]
        out["identity_vs_ref36"].append(_maxdp(vi, x["probs_identity"], keys))
        out["identity_flips_vs_ref36"] += _top(vi, keys) != _top(x["probs_identity"], keys)
        out["reversed_vs_ref36"].append(_maxdp(vr, x["probs_reversed"], keys))
        out["reversed_flips_vs_ref36"] += _top(vr, keys) != _top(x["probs_reversed"], keys)
        if rec["id"] in stored_identity:
            s = stored_identity[rec["id"]]
            out["identity_vs_stored_L4"].append(_maxdp(vi, s, keys))
            out["identity_flips_vs_stored_L4"] += _top(vi, keys) != _top(s, keys)
    for k in ("identity_vs_ref36", "reversed_vs_ref36", "identity_vs_stored_L4", "answer_vs_ref36"):
        v = out[k]
        out[k] = {"n": len(v), "max_abs_dp": max(v) if v else None,
                  "mean_abs_dp": sum(v) / len(v) if v else None, "n_exact": sum(d == 0.0 for d in v)}
    return out


def real_cpu_parity(out_dir=REAL_OUT, plan=REAL_PLAN, threads=None, log=print) -> dict:
    """REAL C1 on CPU through the fast host's HTTP server (fast_host.boot_engine -> FastHost -> make_fast_server,
    FastEngine eager-only, no graphs), checked with hosting/cpu_parity_check.check() on the 36-row sample."""
    import cpu_parity_check as CP
    out_dir = Path(out_dir)
    if "ohs" in str(out_dir).lower():
        raise SystemExit("refused: protected path")
    out_dir.mkdir(parents=True, exist_ok=True)
    t_start = time.time()
    rows = CP.ref36_rows()
    ref36 = {x["id"]: x for x in CP.read_jsonl(CP.REF36)}
    stored_identity = CP.stored_reads("stored_identity", rows)
    dio_, model, tok, load = CP.load_c1_cpu(threads=threads, log=log)
    t = time.time()
    eng, rep = FH.boot_engine(model, tok, device="cpu", flags=ARMS["A1"]["flags"], boot_cfg=REAL_BOOT, log=log)
    info = {**FH.base_info(False, "shared"), "adapter_sha256": load["adapter_sha256"], "gpu": "cpu (Mac, eager only)",
            "boot_s": round(time.time() - t, 1), "boot": rep}
    host = FH.FastHost(eng, info, decide_timeout=REAL_BOOT["decide_timeout_s"])
    token = "real-" + secrets.token_hex(12)
    srv, url, _ = _serve_fast(host, token)
    hd = CP.http_decider(url, token, timeout=REAL_BOOT["decide_timeout_s"] + 60)
    admin = httpx.Client(base_url=url, headers={"Authorization": f"Bearer {token}"}, timeout=60.0, trust_env=False)
    summary = {"what": "SPEED-1 e2e: REAL C1 merged BF16 on CPU through fast_host's HTTP server (FastEngine eager, "
                       "no graphs), cpu_parity_check.check() on the 36-row sample vs the stored L4 reads and ref36",
               "created_utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()), "model": load,
               "plan": [[a, f.__name__ if hasattr(f, "__name__") else "custom"] for a, f in plan],
               "fast_host_boot": {k: rep.get(k) for k in ("pool_requested", "boot_cfg", "engine")}, "arms": {}}
    try:
        for arm, pick in plan:
            flags = ARMS[arm]["flags"]
            r = admin.post("/admin/config", json={"flags": flags})
            r.raise_for_status()
            SB.check_flags(r.json(), arm, flags)  # same read-back rule as speed_bench
            sub = pick(rows)
            recs, f = [], open(out_dir / f"rows_{arm}.jsonl", "w")

            def decide(req, _arm=arm, _f=f, _recs=recs, _n=len(sub)):
                req = {**req, "return_views": True}
                t0 = time.perf_counter()
                resp = hd(req)
                ms = (time.perf_counter() - t0) * 1000
                a = (resp.get("answers") or {}).get("q0")
                rec = {"arm": _arm, "id": req["id"], "client_ms": round(ms, 1), "server_ms": resp.get("server_ms"),
                       "timing": resp.get("timing"), "path": resp.get("path"), "shapes": resp.get("shapes"),
                       "batch_rows": resp.get("batch_rows"), "answer": a}
                _recs.append(rec)
                _f.write(json.dumps(rec) + "\n")
                _f.flush()
                log(f"[{_arm} {len(_recs)}/{_n}] {req['id']} {ms / 1000:.1f} s shapes {resp.get('shapes')}")
                return resp

            t_arm = time.time()
            try:
                res = CP.check(decide, sub, ref=["stored", str(CP.REF36)], log=None)
            finally:
                f.close()
            per = res.pop("per_row")
            res["views"] = view_parity(sub, recs, ref36, stored_identity)
            res["rows_ids"] = [x["id"] for x in sub]
            res["arm_wall_s"] = round(time.time() - t_arm, 1)
            res["shapes"] = {x["id"]: x["shapes"] for x in recs}
            summary["arms"][arm] = res
            (out_dir / f"check_rows_{arm}.jsonl").write_text("".join(json.dumps(x) + "\n" for x in per))
            (out_dir / "summary.json").write_text(json.dumps(summary, indent=1))
            v = res["vs"]
            log(f"[{arm}] rows {res['rows']} answered {res['answered']} clean {res['clean_run']} | vs stored 2view: "
                f"agree {v['stored_served']['argmax_agree']} max dp {v['stored_served']['dp']['max']:.4g} | vs ref36: "
                f"agree {v[str(CP.REF36)]['argmax_agree']} max dp {v[str(CP.REF36)]['dp']['max']:.4g} | views "
                f"{json.dumps({k: res['views'][k] for k in ('identity_vs_ref36', 'reversed_vs_ref36')})}")
    finally:
        admin.close()
        hd.close()
        srv.shutdown()
        srv.server_close()
        eng.close()
    summary["runtime"] = CP.runtime_info(model)
    summary["wall_s"] = round(time.time() - t_start, 1)
    (out_dir / "summary.json").write_text(json.dumps(summary, indent=1))
    return summary


@pytest.mark.skipif(os.environ.get("SPEED1_REAL_CPU") != "1",
                    reason="REAL C1 on CPU (~10-15 min, needs the base snapshot): run with SPEED1_REAL_CPU=1")
def test_real_c1_fast_host_matches_cpu_reference(tmp_path):
    s = real_cpu_parity(tmp_path, plan=QUICK_PLAN, log=print)
    a = s["arms"]["A1"]
    ref = a["vs"][str(LEAN / "speed" / "cpu_ref" / "ref36.jsonl")]
    assert a["clean_run"] and a["answered"] == 2
    assert ref["argmax_agree"] == 1.0 and ref["dp"]["max"] == 0.0  # same CPU, same model, batch 1: bit for bit
    assert a["vs"]["stored_served"]["argmax_agree"] == 1.0


# ====================================================================== tiny model: ids (HF path == SGLang path)

@pytest.fixture(scope="module")
def tiny():
    if not HAVE_TOKENIZER:
        pytest.skip("C1 tokenizer backup missing")
    tok, ro = T.c1_tokenizer(), T.readout()
    return tok, ro


def test_ids_hf_and_sglang_paths_equal_decoder_io(tiny):
    import sglang_host as S
    tok, ro = tiny
    man = json.loads((WORKLOADS / "manifest.json").read_text())
    P = SB.load_workload(WORKLOADS, "P", man)  # the bench's own request bodies (sha256-checked)
    prof = json.loads((WORKLOADS / "token_profile.json").read_text())
    assert prof["info"]["workloads_sha256"]["P"] == man["workloads"]["P"]["sha256"]
    per_row = prof["P"]["per_row"]
    dev = {r["id"]: r for r in T.dev_rows()}
    assert len(P) == len(dev) == 8143
    n_seq = n_trunc = n_wide = n_card_noul = 0
    chunk = []

    def flush():
        nonlocal n_seq
        texts = [x[1] for x in chunk]
        # decoder_io.cand_logits' tokenizer call minus the padding: truncation=True, max_length=MAX_LEN
        want = tok(texts, add_special_tokens=False, truncation=True, max_length=dio.MAX_LEN)["input_ids"]
        for (it, _, body_ids), w in zip(chunk, want):
            assert it.ids == list(w) and body_ids == list(w)
            n_seq += 1
        chunk.clear()

    for item in P:
        row = dev[item["id"]]
        named = R.parse_v1(item["request"])  # strict API v1: the bench's body must be accepted as is
        assert len(named) == 1
        items = R.build_items(ro, named, choice_views=2, render=True)
        R.tokenize_items(tok, items)
        body = S.build_generate_body(items)
        perms = [None] if row["qtype"] == "noul" else [None, list(range(len(row["options"])))[::-1]]
        assert [it.perm for it in items] == perms
        groups = ro.cand(row)  # decoder_io's candidate groups for the DEV row (cand_logits reads them per row)
        flat = [t for g in groups for t in g]
        for v, (it, perm) in enumerate(zip(items, perms)):
            assert it.text == dio.prompt_texts(ro, [row], [perm])[0]
            assert body["token_ids_logprob"][v] == flat and it.sizes == [len(g) for g in groups]
            n_trunc += it.n_raw > dio.MAX_LEN
            chunk.append((it, it.text, body["input_ids"][v]))
        assert items[0].n_tokens == per_row[item["id"]]  # speed_bench's server token check reference
        n_wide += row["qtype"] == "choice" and len(row["options"]) > 26
        n_card_noul += row["qtype"] == "noul" and bool(row.get("card"))
        if len(chunk) >= 256:
            flush()
    flush()
    print(f"\nids: {len(P)} rows, {n_seq} sequences identical on the HF and SGLang paths; {n_wide} rows with > 26 "
          f"options, {n_card_noul} carded noul rows, {n_trunc} sequences over MAX_LEN")
    assert n_seq == sum(1 if dev[i["id"]]["qtype"] == "noul" else 2 for i in P)
    assert n_wide > 100 and n_card_noul > 1000


# ====================================================================== tiny model: the whole stack over HTTP

class FakeSGLang:
    """In-process stand-in for SGLang /generate (prefill-only scoring) on the tiny model: per sequence, the exact fp32
    log_softmax of h_last @ lm_head.T read at the requested candidate ids (what SGLANG_RETURN_ORIGINAL_LOGPROB=1
    returns), batch 1, no padding."""

    def __init__(self, model):
        self.model, self.lock, self.calls, self.flushes = model, threading.Lock(), 0, 0
        self.base_url = "fake://sglang"

    def generate(self, body, timeout=None):
        import torch
        out = []
        body_m, head = dio._parts(self.model)
        with self.lock, torch.no_grad():
            self.calls += 1
            for i, (ids, cand) in enumerate(zip(body["input_ids"], body["token_ids_logprob"])):
                h = body_m(input_ids=torch.tensor([ids])).last_hidden_state[0, -1]
                lp = torch.log_softmax(h.float() @ head.weight.float().T, -1)
                out.append({"text": "", "meta_info": {"id": body["rid"][i], "prompt_tokens": len(ids),
                                                      "completion_tokens": 0, "cached_tokens": 0, "e2e_latency": 0.001,
                                                      "output_token_ids_logprobs": [[[float(lp[t]), int(t), None]
                                                                                     for t in cand]]}})
        return out

    def abort(self, rids):
        pass

    def flush(self):
        self.flushes += 1
        return {"ok": True, "tries": 1}

    def alive(self, timeout=5.0):
        return True

    def close(self):
        pass


def _resolved_args():
    import sglang_host as S
    return {"model_path": "/vol/models/q35_4b_main500k_merged", "dtype": "bfloat16", "quantization": None,
            "enable_fp32_lm_head": True, "context_length": S.CONTEXT_LEN, "disable_radix_cache": False,
            "mamba_radix_cache_strategy": "extra_buffer", "mamba_ssm_dtype": "float32", "linear_attn_backend": "triton",
            "linear_attn_prefill_backend": "triton", "speculative_algorithm": None, "sampling_defaults": "openai",
            "random_seed": 0, "max_running_requests": 64, "max_mamba_cache_size": 400, "version": S.SGLANG_VERSION,
            "enable_lora": False, "lora_paths": None}


def _slice(items, n, prof_rows, max_tokens, want=None):
    """The first n items in workload order whose identity view is <= max_tokens (CPU time), optionally a quota per
    bucket {bucket: count} so each slice holds every kind of row."""
    out, got = [], {}
    for it in items:
        if prof_rows[it["id"]] > max_tokens:
            continue
        if want is not None:
            b = it["bucket"]
            if got.get(b, 0) >= want.get(b, 0):
                continue
            got[b] = got.get(b, 0) + 1
        out.append(it)
        if len(out) == n:
            break
    return out


def write_slices(wl_out, tok, ro, max_tokens=1600):
    """Small slices of the real SPEED-2 workloads (same request bodies, same order) + manifest + token profile, so
    speed_bench's `ab` / `report` run on them unchanged."""
    man = json.loads((WORKLOADS / "manifest.json").read_text())
    full = {W: SB.load_workload(WORKLOADS, W, man) for W in SB.WORKLOAD_NAMES}
    prof = json.loads((WORKLOADS / "token_profile.json").read_text())
    w = {"P": _slice(full["P"], 40, prof["P"]["per_row"], max_tokens,
                     {"noul": 14, "2-4": 10, "5-9": 8, "10-25": 5, "26+": 3}),
         "S": _slice(full["S"], 24, prof["S"]["per_row"], max_tokens, {"noul": 10, "10-25": 8, "26+": 6}),
         "N": _slice(full["N"], 12, prof["N"]["per_row"], max_tokens),
         "R": _slice(full["R"], 20, prof["R"]["per_row"], max_tokens)}
    for W, items in w.items():
        w[W] = [{**it, "i": i} for i, it in enumerate(items)]
    wl_out = Path(wl_out)
    wl_out.mkdir(parents=True, exist_ok=True)
    for W, items in w.items():
        (wl_out / f"{W}.jsonl").write_bytes(SB.workload_bytes(items))
    m2 = SB.manifest_for(w, man.get("R_tasks") or [], LEAN, man["splits"])
    SB.write_json(wl_out / "manifest.json", m2)

    def count(texts):
        return [len(x) for x in tok(list(texts), add_special_tokens=False)["input_ids"]]
    tp = SB.token_profile(w, count, ro.prompt)
    info = {"tokenizer": str(T.ADAPTER), "layout": dio.LAYOUT, "style": dio.STYLE, "max_len": dio.MAX_LEN,
            "workloads_sha256": {W: m2["workloads"][W]["sha256"] for W in SB.WORKLOAD_NAMES}}
    SB.write_json(wl_out / "token_profile.json", {"info": info, **tp})
    for W in w:  # the slice's counts are the full profile's counts (same tokenizer, same prompts)
        assert all(tp[W]["per_row"][i] == prof[W]["per_row"][i] for i in tp[W]["per_row"])
    return w, m2


@pytest.fixture(scope="module")
def stack(tiny, tmp_path_factory):
    import sglang_host as S
    tok, ro = tiny
    out_root = Path(os.environ.get("SPEED1_E2E_OUT") or tmp_path_factory.mktemp("e2e"))
    if "ohs" in str(out_root).lower():
        raise SystemExit("refused: protected path")
    if out_root.exists():
        for d in ("workloads", "e2e"):
            shutil.rmtree(out_root / d, ignore_errors=True)
    w, man = write_slices(out_root / "workloads", tok, ro)
    model = T.tiny_model(seed=0)
    servers, closers = {}, []
    t = time.time()
    cov = {1: 1024, 2: 1024, 4: 512, 8: 256, 16: 256}  # reduced plan (CPU time); B1/B2 <= 1024 keep A0's rule
    eng, rep = FH.boot_engine(model, tok, flags=ARMS["A2"]["flags"], ro=ro, log=quiet,
                              boot_cfg={"coverage": cov, "legacy_shapes": False, "eager_warmup": {},
                                        "warm_requests": 1})
    host = FH.FastHost(eng, {**FH.base_info(False, "shared"), "adapter_sha256": FH.ADAPTER_SHA256,
                             "gpu": "cpu (e2e)", "boot_s": 0.0, "boot": rep})
    srv, url, _ = _serve_fast(host)
    servers["hf_bf16"] = url
    closers += [srv.shutdown, srv.server_close, eng.close]
    m8 = copy.deepcopy(model)
    eng8, rep8 = FH.boot_engine(m8, tok, fp8=True, flags=ARMS["A3"]["flags"], ro=ro, log=quiet,
                                boot_cfg={"coverage": {1: 512, 2: 512}, "legacy_shapes": False, "eager_warmup": {},
                                          "warm_requests": 1, "selftest_tol": 0.5})
    host8 = FH.FastHost(eng8, {**FH.base_info(True, "shared"), "adapter_sha256": FH.ADAPTER_SHA256,
                               "gpu": "cpu (e2e)", "boot_s": 0.0, "boot": rep8})
    srv8, url8, _ = _serve_fast(host8)
    servers["hf_fp8"] = url8
    closers += [srv8.shutdown, srv8.server_close, eng8.close]
    fake = FakeSGLang(model)
    fe = S.SGLangFrontEnd(fake, tok, ro, server_args=_resolved_args(), log=quiet)
    sinfo = {"model": S.C1_MODEL, "adapter_sha256": S.C1_ADAPTER_SHA256, "base": S.BASE, "revision": S.REVISION,
             "gpu": "fake SGLang (tiny model)", "region": None, "boot_s": 0.0, "boot": {}}
    ssrv, _ = S.make_frontend_server(0, TOKEN, fe, sinfo, threading.Event().set, host="127.0.0.1")
    threading.Thread(target=ssrv.serve_forever, daemon=True).start()
    servers["sglang"] = f"http://127.0.0.1:{ssrv.server_address[1]}"
    closers += [ssrv.shutdown, ssrv.server_close]
    tf = out_root / "token.txt"
    tf.write_text(TOKEN + "\n")
    print(f"\nstack up in {time.time() - t:.0f} s: {servers}")
    yield {"tok": tok, "ro": ro, "model": model, "w": w, "man": man, "out": out_root, "token_file": tf,
           "servers": servers, "boot": rep, "boot8": rep8, "fake": fake}
    for c in closers:
        try:
            c()
        except Exception:  # noqa: BLE001
            pass


def _ab(stack, url, arms, window_s=4.0):
    return SB.main(["ab", "--url", url, "--token-file", str(stack["token_file"]), "--session", "e2e", "--arms", arms,
                    "--go", "--overwrite", "--workloads", str(stack["out"] / "workloads"),
                    "--out-root", str(stack["out"]), "--warmup-s", "0.5", "--window-s", str(window_s),
                    "--timeout-s", "120"])


def test_e2e_bench_all_arms(stack, capsys):
    s, out = stack, stack["out"]
    assert s["boot"]["parity_selftest"]["ok"] and s["boot"]["parity_selftest"]["graph_forwards"] > 0
    r0 = _ab(s, s["servers"]["hf_bf16"], "A0,A1,A2")
    r3 = _ab(s, s["servers"]["hf_fp8"], "A3")
    rs = _ab(s, s["servers"]["sglang"], "S1")
    assert (r0["done"], r3["done"], rs["done"]) == (["A0", "A1", "A2"], ["A3"], ["S1"]), (r0, r3, rs)
    assert not (r0["refused"] or r3["refused"] or rs["refused"])
    # an arm on the wrong boot is refused before any timing (A3 needs quantization fp8; S1 needs engine sglang)
    bad = _ab(s, s["servers"]["hf_bf16"], "A3")
    assert bad["refused"].get("A3") and "quantization" in bad["refused"]["A3"]
    bad = _ab(s, s["servers"]["hf_bf16"], "S1")
    assert bad["refused"].get("S1") and "engine" in bad["refused"]["S1"]
    rep = SB.main(["report", "--session", "e2e", "--out-root", str(out), "--workloads", str(out / "workloads")])
    sdir = out / "e2e"
    md = (sdir / "REPORT.md").read_text()
    assert (sdir / "report.json").exists() and md.startswith("# SPEED-2 report")
    w = s["w"]
    nP = len(w["P"])
    expect_levels = {"P": [16], "S": [1, 2, 4, 8, 16], "N": [1], "R": [1, 8]}

    # ---- every arm: levels ran, no failed call, answers complete, token check, health snapshots
    for arm in ("A0", "A1", "A2", "A3", "S1"):
        x = rep["arms"][arm]
        assert f"| {arm} |" in md
        for W, cs in expect_levels.items():
            lv = x["workloads"][W]["levels"]
            assert [v["concurrency"] for v in lv] == cs, (arm, W)
            for v in lv:
                assert v["failed_calls"] == 0 and v["calls_ok_in_window"] > 0, (arm, W, v["concurrency"],
                                                                               v["error_examples"])
                assert v["decisions_per_hour"] > 0 and v["client_ms"]["p50"] >= v["server_ms"]["p50"] > 0
        assert x["workloads"]["P"]["answers"] == nP and x["workloads"]["P"]["levels"][0]["calls_sent"] == nP
        tc = x["token_check_P"]
        assert tc["checked"] == nP and tc["equal"] == nP and tc["server_missing"] == 0, (arm, tc)
        assert x["sustained_decisions_per_hour"] and x["sustained_at_concurrency"] in (1, 2, 4, 8, 16)
        usd = x["cost"]["usd_per_1k"]
        assert set(usd) == {"any", "us-east"} and usd["us-east"]["40%"] > usd["any"]["100%"] > 0
        for f in ("health_before.json", "health.json", "health_after.json", "config.json", "summary.json",
                  "answers_P.jsonl", "answers_S.jsonl", "answers_N.jsonl", "answers_R.jsonl"):
            assert (sdir / arm / f).exists(), (arm, f)
        h = json.loads((sdir / arm / "health.json").read_text())
        assert h["adapter_sha256"] == FH.ADAPTER_SHA256 and h["ok"] is True
        assert h["engine"] == ("sglang" if arm == "S1" else "hf")
        assert (h["quantization"] == "fp8") == (arm == "A3")
        engines = {e for v in x["workloads"]["S"]["levels"] for e in v["engines"]}
        assert engines == {h["engine"]}

    # ---- HF arms: cross-request batching only where the flags allow it (batch_rows over every level of every
    # workload: whether a given level batches depends on timing, so the claim is per arm, not per level)
    def max_rows(arm):
        return max(int(k) for W in expect_levels for v in rep["arms"][arm]["workloads"][W]["levels"]
                   for k in v["batch_rows"]["hist"])
    assert max_rows("A1") == 1  # each view its own batch-1 forward
    assert max_rows("A0") == 2  # one request = one batch (2view as a batch of 2)
    assert max_rows("A2") > 2  # opportunistic cross-request batches under concurrency

    # ---- parity vs the baseline A0 (same session)
    for arm in ("A1", "A2", "S1"):
        par = rep["arms"][arm]["parity"]
        pb = par["P_vs_baseline"]
        assert par["gate"] == "PASS" and pb["n"] == nP and pb["argmax_agree"] == 1.0, (arm, pb)
        assert pb["dp_max"] <= 1e-4 and pb["acc_diff_pt"] == 0.0, (arm, pb["dp_max"])
        assert par["R_vs_baseline"]["n"] > 0 and par["R_vs_baseline"]["argmax_agree"] == 1.0
        assert par["acc_bar_pt"] == 0.3
    p3 = rep["arms"]["A3"]["parity"]
    assert p3["acc_bar_pt"] == 1.0 and p3["P_vs_baseline"]["n"] == nP  # FP8 bar applied to the FP8 arm
    assert rep["arms"]["A0"]["parity"]["gate"] == "BASELINE"

    # ---- reversed-view check: HF arms return per-view answers (p_request_extra return_views), S1 does not
    for arm in ("A0", "A1", "A2", "A3"):
        rv = rep["arms"][arm]["parity"]["reversed_view"]
        assert rv["available"] and rv["source"] == "per-view answers" and rv["cand_reversed_consistency"]["pass"]
    assert rep["arms"]["S1"]["parity"]["reversed_view"]["available"] is False
    assert rep["stored"]["reversed_view_consistency"]["pass"]
    ctx = rep["arms"]["A0"]["parity"]["P_vs_stored_L4_context"]  # random tiny model vs C1's L4 reads: context only
    assert ctx["n"] == nP and ctx["missing_ref"] == 0

    # ---- P answers through the whole stack == decoder_io.predict on the same model (2view and each view)
    rows = [{**SB.request_row(it["request"]), "id": it["id"]} for it in w["P"]]
    ref2 = dio.predict(s["model"], s["tok"], rows, dev="cpu", tta_choice=True)
    ref1 = dio.predict(s["model"], s["tok"], rows, dev="cpu", tta_choice=False)
    rev = [list(range(len(r["options"])))[::-1] if r["qtype"] == "choice" else None for r in rows]
    refr = dio.predict(s["model"], s["tok"], rows, dev="cpu", perms=rev)
    worst = {}
    for arm in ("A0", "A1", "A2", "S1"):
        ans, views = SB.read_answers(sdir / arm / "answers_P.jsonl")
        d = 0.0
        for r, p2, p1, pr in zip(rows, ref2, ref1, refr):
            keys = ["yes", "no"] if r["qtype"] == "noul" else list(r["options"])
            d = max(d, _maxdp(ans[r["id"]], p2, keys))
            if r["qtype"] == "choice" and arm != "S1":
                v = views[r["id"]]
                d = max(d, _maxdp(v["identity"], p1, keys), _maxdp(v["reversed"], pr, keys))
        worst[arm] = d
    print(f"\nmax |p - decoder_io.predict| over P slice ({nP} rows): {worst}; A3 (fp8) vs A0 P: "
          f"{json.dumps({k: p3['P_vs_baseline'][k] for k in ('argmax_agree', 'acc_diff_pt', 'dp_max')})}")
    assert all(v <= 1e-4 for v in worst.values()), worst

    # ---- the SGLang front end returns per-view answers too (speed_arms.json S1/S2 do not request them)
    with httpx.Client(base_url=s["servers"]["sglang"], headers={"Authorization": f"Bearer {TOKEN}"}, timeout=60,
                      trust_env=False) as c:
        n_views = 0
        for it, r, p1, pr in zip(w["P"], rows, ref1, refr):
            if r["qtype"] == "choice" and n_views < 3:
                a = c.post("/decide", json={**it["request"], "return_views": True}).json()["answers"]["q0"]
                vi, vr = a["view_probabilities"]
                assert max(_maxdp(vi, p1, r["options"]), _maxdp(vr, pr, r["options"])) <= 1e-4
                n_views += 1
        assert n_views == 3

    # ---- S1 really went through the fake SGLang; the HF A0 arm through captured (emulated) graphs and eager
    assert s["fake"].calls > 0 and s["fake"].flushes > 0
    paths = {p for v in rep["arms"]["A0"]["workloads"]["S"]["levels"] for p in v["paths"]}
    assert paths & {"graph", "mixed"} and paths & {"eager", "mixed"}


def test_pinned_files_unchanged():
    root = LEAN.parent.parent  # the git work tree (~/Documents/jev)
    rel = [str(Path("opendecide-data/lean") / p) for p in PINNED]
    r = subprocess.run(["git", "-C", str(root), "diff", "--stat", "HEAD", "--", *rel], capture_output=True, text=True)
    assert r.returncode == 0 and r.stdout.strip() == "", r.stdout


# ====================================================================== CLI (the long real-model run)

def main(argv=None):
    ap = argparse.ArgumentParser(description="SPEED-1 e2e: real C1 on CPU through the fast host")
    sub = ap.add_subparsers(dest="cmd", required=True)
    r = sub.add_parser("real-cpu")
    r.add_argument("--out", default=str(REAL_OUT))
    r.add_argument("--threads", type=int, default=None)
    r.add_argument("--quick", action="store_true", help="A1 on the cheapest noul + choice row only")
    a = ap.parse_args(argv)
    if a.cmd == "real-cpu":
        def log(*x):
            print(time.strftime("%H:%M:%S"), *x, flush=True)
        s = real_cpu_parity(Path(a.out), QUICK_PLAN if a.quick else REAL_PLAN, threads=a.threads, log=log)
        log(json.dumps({arm: {"rows": v["rows"], "clean_run": v["clean_run"],
                              "vs": {k: {"agree": x["argmax_agree"], "dp_max": x["dp"]["max"]}
                                     for k, x in v["vs"].items()}} for arm, v in s["arms"].items()}, indent=1))


if __name__ == "__main__":
    main()
