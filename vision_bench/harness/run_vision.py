"""Run the Vision Index suites with C1 (base + LoRA) or the plain base model on the L4.

  python run_vision.py smoke --model c1|base            10 items, readout sanity + shared-ViT path vs stock path; for c1 the
                                                         adapter proof (every LoRA tensor equals the file, LoRA on != LoRA off)
  python run_vision.py eval  --model c1|base [--out DIR] full run: warm pass, timed batch-1 pass (failed items retried once and
                                                         flagged), labelled diagnostic arms (count_prefixed, yn_swapped), batched
                                                         throughput, local HTTP end-to-end sample (40 items per suite)
Everything writes into --out (default ~/vision_bench/results). No network. One process holds the model for all stages.
"""
import argparse
import base64
import hashlib
import http.server
import json
import os
import socketserver
import subprocess
import sys
import threading
import time

os.environ.setdefault("HF_HUB_OFFLINE", "1")
os.environ.setdefault("TRANSFORMERS_OFFLINE", "1")
os.environ.setdefault("TRITON_CACHE_DIR", os.path.expanduser("~/vision_bench/triton_cache"))
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import torch  # noqa: E402

import vb_core as vb  # noqa: E402
from vb_core import dio  # noqa: E402

HERE = os.path.dirname(os.path.abspath(__file__))


def pct(xs, p):
    xs = sorted(xs)
    if not xs:
        return None
    k = (len(xs) - 1) * p / 100
    f = int(k)
    return xs[f] + (xs[min(f + 1, len(xs) - 1)] - xs[f]) * (k - f)


def sha_file(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for b in iter(lambda: f.read(1 << 20), b""):
            h.update(b)
    return h.hexdigest()


def meta(rd, probe_case=None):
    import transformers
    m = {"model": rd.which, "base": vb.BASE, "revision": vb.REVISION, "layout": rd.layout, "style": rd.style,
         "temps": vb.TEMPS, "torch": torch.__version__, "transformers": transformers.__version__,
         "gpu": torch.cuda.get_device_name(), "dtype": "bfloat16", "attn": "sdpa", "pad_multiple": vb.PAD_MULTIPLE,
         "decoder_io_sha256": sha_file(os.path.join(HERE, "vendor", "decoder_io.py")), "load_s": rd.load_s,
         "image_processor": type(rd.imgproc).__name__, "loadavg_start": os.getloadavg(),
         "score_options": "criteria strings as Jev receives them (no index prefix); diagnostic variant count_prefixed = C1's '<i>: '"}
    if rd.which == "c1":
        m["adapter"] = vb.ADAPTER
        m["adapter_sha256"] = sha_file(os.path.join(vb.ADAPTER, "adapter_model.safetensors"))
        assert m["adapter_sha256"].startswith("507d1c29"), m["adapter_sha256"]
        m["adapter_renamed"] = vb.ADAPTER_RENAMED
        m["adapter_renamed_sha256"] = sha_file(os.path.join(vb.ADAPTER_RENAMED, "adapter_model.safetensors"))
        # hard gates: the LoRA must really be in the model. Raises (and the chain stops) if it is not.
        chk = rd.adapter_check
        assert chk and chk["n_lora_B"] == vb.ADAPTER_N_LORA_B and chk["n_lora_B_nonzero"] == vb.ADAPTER_N_LORA_B \
            and chk["n_tensors"] == vb.ADAPTER_N_TENSORS and chk["n_no_home"] == 0 and chk["n_unequal_to_file"] == 0, chk
        m["adapter_check"] = chk
        if probe_case is not None:
            qid, q = next(iter(probe_case["questions"].items()))
            prep = rd.prepare(open(probe_case["_image_file"], "rb").read(), q)
            eff = rd.adapter_effect(prep)
            m["adapter_effect_max_logit_diff_on_vs_off"] = eff
            assert eff > 1e-3, f"C1 and base give the same logits on a probe item (diff {eff}): the adapter is not applied"
    return m


def run_item(rd, c, variant="main"):
    """One decision at batch 1: file bytes -> prepared inputs -> forward -> typed probabilities. Returns the record."""
    qid, q = next(iter(c["questions"].items()))
    gold = vb.gold_index(q, c["gold"][qid])
    raw = open(c["_image_file"], "rb").read()
    rec = {"id": c["id"], "suite": c["suite"], "qid": qid, "type": q["type"], "gold": gold, "variant": variant}
    try:
        vb.sync()
        t0 = time.perf_counter()
        prep = rd.prepare(raw, q, variant)
        t1 = time.perf_counter()
        lg = rd.read([prep])[0]
        probs = rd.decide(prep, lg)
        vb.sync()
        t2 = time.perf_counter()
        pred = max(range(len(probs)), key=probs.__getitem__)
        rec.update({"pred": pred, "correct": int(pred == gold), "probs": probs, "conf": max(probs),
                    "view_logits": [[float(x) for x in l.tolist()] for l in lg], "views": prep["views"],
                    "prep_ms": (t1 - t0) * 1000, "fwd_ms": (t2 - t1) * 1000, "compute_ms": (t2 - t0) * 1000,
                    "n_tokens": [len(s) for s in prep["seqs"]], "n_image_tokens": prep["n_img"], "image_size": prep["size"]})
    except Exception as e:  # noqa: BLE001  a failed decision is logged, never hidden
        rec["error"] = f"{type(e).__name__}: {str(e)[:300]}"
        torch.cuda.empty_cache()
    return rec


def write_jsonl(path, rows):
    with open(path, "w") as f:
        for r in rows:
            f.write(json.dumps(r) + "\n")


# ------------------------------------------------------------------ smoke
def smoke(rd, out):
    cases = vb.load_cases()
    by = {}
    for c in cases:
        by.setdefault(c["suite"], []).append(c)
    pick = [c for s in vb.SUITES for c in by[s][:2]]
    rep = {"meta": meta(rd, probe_case=by["img_sst2"][0]), "items": [], "checks": {}}
    max_diff, sums_ok, confs = 0.0, True, []
    for c in pick:
        qid, q = next(iter(c["questions"].items()))
        prep = rd.prepare(open(c["_image_file"], "rb").read(), q)
        lg = rd.read([prep])[0]
        probs = rd.decide(prep, lg)
        st = rd.read_stock(prep)
        probs_stock = rd.decide(prep, st)
        d = max(abs(a - b) for a, b in zip(probs, probs_stock))
        lgd = max(float((a - b).abs().max()) for a, b in zip(lg, st))
        max_diff = max(max_diff, d)
        sums_ok &= abs(sum(probs) - 1) < 1e-4
        confs.append(max(probs))
        gold = vb.gold_index(q, c["gold"][qid])
        rep["items"].append({"id": c["id"], "type": q["type"], "gold": gold, "pred": max(range(len(probs)), key=probs.__getitem__),
                             "conf": round(max(probs), 4), "prob_sum": round(sum(probs), 6), "n_options": len(probs),
                             "max_prob_diff_vs_stock": d, "max_logit_diff_vs_stock": lgd,
                             "top3": sorted(([round(p, 4), i] for i, p in enumerate(probs)), reverse=True)[:3]})
    # the two labelled diagnostic variants must run end to end (a failure here is a failure of the chain, not hidden later)
    diag = []
    for c in by["img_count"][:2] + by["img_sst2"][:2] + by["img_vqa_yesno"][:2]:
        qid, q = next(iter(c["questions"].items()))
        v = "count_prefixed" if c["suite"] == "img_count" else "yn_swapped"
        prep = rd.prepare(open(c["_image_file"], "rb").read(), q, v)
        probs = rd.decide(prep, rd.read([prep])[0])
        main = next(it for it in rep["items"] if it["id"] == c["id"])
        diag.append({"id": c["id"], "variant": v, "n_options": len(probs), "prob_sum": round(sum(probs), 6),
                     "pred": max(range(len(probs)), key=probs.__getitem__), "pred_main": main["pred"], "conf": round(max(probs), 4)})
        sums_ok &= abs(sum(probs) - 1) < 1e-4
    rep["diag_items"] = diag
    rep["checks"] = {"probs_sum_to_one": bool(sums_ok), "max_prob_diff_shared_vit_vs_stock": max_diff,
                     "conf_min": min(confs), "conf_max": max(confs), "conf_distinct": len({round(x, 3) for x in confs}),
                     "not_constant": len({round(x, 3) for x in confs}) > 3,
                     "adapter_effect_max_logit_diff_on_vs_off": rep["meta"].get("adapter_effect_max_logit_diff_on_vs_off"),
                     "adapter_check": rep["meta"].get("adapter_check")}
    json.dump(rep, open(f"{out}/smoke_{rd.which}.json", "w"), indent=1)
    print(json.dumps(rep["checks"]), flush=True)
    for it in rep["items"]:
        print(it, flush=True)


# ------------------------------------------------------------------ http (end-to-end)
class Handler(http.server.BaseHTTPRequestHandler):
    protocol_version = "HTTP/1.1"
    reader = None
    lock = threading.Lock()

    def log_message(self, *a):  # silence
        pass

    def do_POST(self):
        n = int(self.headers.get("Content-Length", 0))
        body = json.loads(self.rfile.read(n))
        t0 = time.perf_counter()
        try:
            img = body["state"][0]["image"]
            raw = base64.b64decode(img.split(",", 1)[1])
            answers = {}
            with Handler.lock:
                for qid, q in body["questions"].items():
                    prep = Handler.reader.prepare(raw, q)
                    lg = Handler.reader.read([prep])[0]
                    vb.sync()
                    probs = Handler.reader.decide(prep, lg)
                    answers[qid] = vb.decision_record(q, None, probs)
            payload = json.dumps({"answers": answers, "server_ms": (time.perf_counter() - t0) * 1000}).encode()
            code = 200
        except Exception as e:  # noqa: BLE001
            payload, code = json.dumps({"error": f"{type(e).__name__}: {str(e)[:200]}"}).encode(), 500
        self.send_response(code)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(payload)))
        self.end_headers()
        self.wfile.write(payload)


class Server(socketserver.ThreadingMixIn, http.server.HTTPServer):
    daemon_threads = True
    allow_reuse_address = True


def e2e(rd, out, n_per_suite=40, port=8765):
    Handler.reader = rd
    srv = Server(("127.0.0.1", port), Handler)
    th = threading.Thread(target=srv.serve_forever, daemon=True)
    th.start()
    res = {}
    for conc in (1, 8):
        path = f"{out}/e2e_{rd.which}_c{conc}.jsonl"
        r = subprocess.run([sys.executable, os.path.join(HERE, "e2e_client.py"), "--port", str(port), "--n", str(n_per_suite),
                            "--conc", str(conc), "--out", path, "--data", vb.data_root()], capture_output=True, text=True)
        print(r.stdout[-600:], r.stderr[-600:], flush=True)
        rows = [json.loads(l) for l in open(path)]
        ok = [x["e2e_ms"] for x in rows if "error" not in x]
        res[f"c{conc}"] = {"n": len(rows), "ok": len(ok), "p50": pct(ok, 50), "p95": pct(ok, 95), "mean": sum(ok) / max(1, len(ok)),
                           "server_ms_p50": pct([x["server_ms"] for x in rows if "server_ms" in x], 50)}
    srv.shutdown()
    json.dump(res, open(f"{out}/e2e_{rd.which}.json", "w"), indent=1)
    print("e2e", json.dumps(res), flush=True)


# ------------------------------------------------------------------ eval
def eval_all(rd, out, do_e2e=True):
    cases = vb.load_cases()
    mt = meta(rd, probe_case=cases[0])
    json.dump(mt, open(f"{out}/meta_{rd.which}.json", "w"), indent=1)
    print("meta ok", json.dumps({k: mt[k] for k in mt if k.startswith("adapter_")}), flush=True)
    t_start = time.time()
    # 1) warm pass (all items, batch 1): compiles/autotunes every length bucket; also a determinism reference
    t0 = time.time()
    warm = [run_item(rd, c) for c in cases]
    write_jsonl(f"{out}/preds_{rd.which}_warm.jsonl", warm)
    print(f"warm pass {time.time() - t0:.0f}s errors={sum('error' in r for r in warm)}", flush=True)
    # 2) timed pass at batch 1 (one decision per forward; the choice items' two views are one batch of 2 sequences)
    torch.cuda.reset_peak_memory_stats()
    t0 = time.time()
    load_a = os.getloadavg()
    rows = [run_item(rd, c) for c in cases]
    wall1 = time.time() - t0
    # a failed decision is retried ONCE (same inputs, after freeing cached memory) and flagged; if it fails again it stays failed.
    # The bench's scorer turns a failure into a uniform answer whose argmax is option 0, so failures must be visible, not absorbed.
    n_first_fail = 0
    for i, r in enumerate(rows):
        if "error" in r:
            n_first_fail += 1
            torch.cuda.empty_cache()
            r2 = run_item(rd, cases[i])
            r2["retried"], r2["first_error"] = True, r["error"]
            rows[i] = r2
    print(f"timed pass {wall1:.0f}s first-attempt failures={n_first_fail} still failed={sum('error' in r for r in rows)}", flush=True)
    write_jsonl(f"{out}/preds_{rd.which}.jsonl", rows)
    ok = [r for r in rows if "error" not in r]
    acc = sum(r["correct"] for r in ok) / max(1, len(ok))
    det = max((max(abs(a - b) for a, b in zip(r["probs"], w["probs"])) for r, w in zip(rows, warm) if "error" not in r and "error" not in w),
              default=None)
    summ = {"loadavg_timed_pass_start": load_a, "loadavg_timed_pass_end": os.getloadavg(), "first_attempt_failures": n_first_fail,
            "batch1": {"wall_s": wall1, "items": len(rows), "errors": len(rows) - len(ok), "items_per_s": len(rows) / wall1,
                       "compute_p50": pct([r["compute_ms"] for r in ok], 50), "compute_p95": pct([r["compute_ms"] for r in ok], 95),
                       "fwd_p50": pct([r["fwd_ms"] for r in ok], 50), "fwd_p95": pct([r["fwd_ms"] for r in ok], 95),
                       "prep_p50": pct([r["prep_ms"] for r in ok], 50), "prep_p95": pct([r["prep_ms"] for r in ok], 95)},
            "overall_acc_micro": acc, "determinism_max_prob_diff_warm_vs_timed": det,
            "peak_gpu_mem_gb": torch.cuda.max_memory_allocated() / 2 ** 30}
    print("batch1", json.dumps(summ["batch1"]), "acc", round(acc, 4), "det", det, flush=True)
    # 2b) labelled diagnostics (NOT part of the headline): count options with C1's "<i>: " prefix; yes/no with the letters swapped
    t0 = time.time()
    diag = []
    for c in cases:
        q = next(iter(c["questions"].values()))
        v = "count_prefixed" if c["suite"] == "img_count" else ("yn_swapped" if q["type"] == "noul" else None)
        if v:
            diag.append(run_item(rd, c, variant=v))
    write_jsonl(f"{out}/diag_{rd.which}.jsonl", diag)
    print(f"diagnostics {len(diag)} items {time.time() - t0:.0f}s errors={sum('error' in r for r in diag)}", flush=True)
    # 3) throughput: micro-batches of B items (their views are all in one padded forward); CPU prep is serial, not overlapped
    byid = {r["id"]: r for r in rows}
    summ["throughput"] = {}
    for B in (4, 8):
        order = sorted(cases, key=lambda c: sum(byid[c["id"]].get("n_tokens", [0])) if "error" not in byid[c["id"]] else 0)
        preds = {}
        vb.sync()
        t0 = time.perf_counter()
        for i in range(0, len(order), B):
            chunk = order[i:i + B]
            try:
                preps = [rd.prepare(open(c["_image_file"], "rb").read(), next(iter(c["questions"].values()))) for c in chunk]
                lgs = rd.read(preps)
                for c, p, lg in zip(chunk, preps, lgs):
                    preds[c["id"]] = rd.decide(p, lg)
            except Exception as e:  # noqa: BLE001
                print("batch error", type(e).__name__, str(e)[:200], flush=True)
                torch.cuda.empty_cache()
        vb.sync()
        wall = time.perf_counter() - t0
        agree = sum(1 for k, p in preds.items() if "error" not in byid[k] and
                    max(range(len(p)), key=p.__getitem__) == byid[k]["pred"])
        dmax = max((max(abs(a - b) for a, b in zip(p, byid[k]["probs"])) for k, p in preds.items() if "error" not in byid[k]), default=None)
        summ["throughput"][f"B{B}"] = {"wall_s": wall, "items": len(preds), "items_per_s": len(preds) / wall, "argmax_agree_with_batch1": agree,
                                       "max_prob_diff_vs_batch1": dmax, "peak_gpu_mem_gb": torch.cuda.max_memory_allocated() / 2 ** 30}
        print(f"B{B}", json.dumps(summ["throughput"][f"B{B}"]), flush=True)
    json.dump(summ, open(f"{out}/summary_{rd.which}.json", "w"), indent=1)
    # 4) end-to-end through a local HTTP server
    if do_e2e:
        e2e(rd, out)
    summ["gpu_process_wall_s"] = time.time() - t_start
    json.dump(summ, open(f"{out}/summary_{rd.which}.json", "w"), indent=1)


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("mode", choices=["smoke", "eval"])
    ap.add_argument("--model", required=True, choices=["c1", "base"])
    ap.add_argument("--out", default=os.path.expanduser("~/vision_bench/results"))
    ap.add_argument("--no-e2e", action="store_true")
    a = ap.parse_args()
    os.makedirs(a.out, exist_ok=True)
    rd = vb.Reader(a.model)
    print("loaded", a.model, f"{rd.load_s:.0f}s", "layout", rd.layout, "style", rd.style, flush=True)
    if a.mode == "smoke":
        smoke(rd, a.out)
    else:
        eval_all(rd, a.out, do_e2e=not a.no_e2e)
