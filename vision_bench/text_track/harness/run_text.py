"""Run the System One Bench TEXT suites (16 suites, 3,250 cases, 4,850 decisions) with C1 and with plain Qwen3.5-4B.

  python run_text.py eval [--out DIR] [--stages gates,main,lat,diag] [--arms c1,base] [--deadline-s N] [--max-cases N] [--dev cuda]

One process, one model load: the C1 LoRA is on for the 'c1' arm and disabled (peft disable_adapter) for the 'base' arm, so both read
identical prompts through identical weights. Stages, in priority order, each writing its files as it goes:
  gates  hash/identity checks, adapter proof (every LoRA tensor equals the file, LoRA on != off), smoke items; aborts on failure
  main   headline decisions, batched, suite by suite (c1 then base within a suite)   -> preds_<arm>.jsonl
  lat    timed batch-1 sample (all questions of one case read as one batch, like one API call) + agreement with the batched pass
                                                                                      -> lat_<arm>.jsonl
  diag   labelled diagnostics: score options without "<i>: ", yes/no letters swapped -> diag_<arm>.jsonl
A stage or suite that would start after --deadline-s seconds is skipped and listed in skipped.json (never silently).
No network, no training, no Jev: evaluation only.
"""
import argparse
import hashlib
import json
import os
import sys
import time

T_START = time.time()
os.environ.setdefault("HF_HUB_OFFLINE", "1")
os.environ.setdefault("TRANSFORMERS_OFFLINE", "1")
os.environ.setdefault("PYTORCH_CUDA_ALLOC_CONF", "expandable_segments:True")
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

import torch  # noqa: E402

import lockcheck  # noqa: E402
import tt_core as tt  # noqa: E402
from tt_core import dio  # noqa: E402

LAT_PER_SUITE = 20     # cases timed one at a time per suite
LAT_WARM = 8           # untimed warm-up cases before the timed sample
SUITE_ORDER = ["sst2", "ag_news", "emotion", "sst5", "boolq", "xnli_en", "xnli_fr", "xnli_ar", "ar_sentiment", "ar_offensive",
               "ar_massive_scenario", "ar_massive_intent", "ar_miracl_pair", "ar_miracl_rerank", "banking77", "typed-decisions"]


def sha_file(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for b in iter(lambda: f.read(1 << 20), b""):
            h.update(b)
    return h.hexdigest()


def pct(xs, p):
    xs = sorted(xs)
    if not xs:
        return None
    k = (len(xs) - 1) * p / 100
    f = int(k)
    return xs[f] + (xs[min(f + 1, len(xs) - 1)] - xs[f]) * (k - f)


def log(*a):
    print(f"[{time.time() - T_START:7.1f}s]", *a, flush=True)


class Out:
    def __init__(self, path):
        self.path = path
        os.makedirs(path, exist_ok=True)
        self.skipped = []

    def jsonl(self, name, mode="w"):
        return open(os.path.join(self.path, name), mode)

    def json(self, name, obj):
        json.dump(obj, open(os.path.join(self.path, name), "w"), indent=1)

    def skip(self, what):
        self.skipped.append(what)
        self.json("skipped.json", self.skipped)
        log("SKIPPED (deadline):", what)


def late(a):
    return a.deadline_s is not None and time.time() - T_START > a.deadline_s


def by_suite(ds):
    out = {}
    for d in ds:
        out.setdefault(d["suite"], []).append(d)
    return out


def meta(rd, a, ds):
    import transformers
    m = {"arms": {"c1": "Qwen3.5-4B + LoRA q35_4b_main500k (unmerged, fp32 adapter weights)", "base": "Qwen3.5-4B, LoRA disabled"},
         "base": tt.BASE, "revision": tt.REVISION, "route": rd.route, "model_class": type(rd.top).__name__ if rd.model else None,
         "layout": rd.layout, "style": rd.style, "temps": tt.TEMPS, "pad_multiple": tt.PAD_MULTIPLE, "token_budget": tt.TOKEN_BUDGET,
         "max_batch": tt.MAX_BATCH, "torch": torch.__version__, "transformers": transformers.__version__,
         "gpu": torch.cuda.get_device_name() if torch.cuda.is_available() else None, "dtype": "bfloat16", "attn": "sdpa",
         "decoder_io_sha256": sha_file(os.path.join(HERE, "vendor", "decoder_io.py")),
         "cases_file": tt.data_path(), "cases_file_sha256": sha_file(tt.data_path()), "n_decisions": len(ds),
         "adapter": tt.ADAPTER, "adapter_sha256": sha_file(os.path.join(tt.ADAPTER, "adapter_model.safetensors")),
         "load_s": getattr(rd, "load_s", None), "loadavg_start": os.getloadavg(),
         "score_options": "headline: C1's shipped '<i>: <level>' form; diagnostic score_noprefix: bare criteria strings (as Jev)"}
    try:
        import peft
        m["peft"] = peft.__version__
    except Exception:  # noqa: BLE001
        pass
    assert m["adapter_sha256"].startswith("507d1c29"), m["adapter_sha256"]
    m["adapter_check"] = getattr(rd, "adapter_check", None)
    return m


# ------------------------------------------------------------------ gates
def gates(rd, a, ds, out):
    """Hard checks before any long work. Raises (and the chain stops) on any failure."""
    rep = {}
    # 1) frozen data
    lock = os.path.join(os.path.dirname(tt.data_path()), "data.lock.cases.json")
    problems = lockcheck.check(tt.data_path(), lock) if not a.max_cases else ["skipped (partial run)"]
    rep["data_lock_problems"] = problems
    assert not problems or a.max_cases, problems
    # 2) one prompt set for both arms: C1's adapter-folder tokenizer and the base tokenizer render and tokenize identically
    preps = rd.prepare_many(ds, "main")
    preps_b = rd.prepare_many(ds, "main", tok=rd.tok_base)
    same_text = all(p["texts"] == q["texts"] for p, q in zip(preps, preps_b))
    same_ids = all(p["seqs"] == q["seqs"] for p, q in zip(preps, preps_b))
    same_groups = rd.ro.groups == rd.ro_base.groups and rd.ro.wide == rd.ro_base.wide
    rep["tokenizers_identical_on_all_prompts"] = {"text": same_text, "ids": same_ids, "candidate_groups": same_groups,
                                                   "n_decisions": len(preps), "n_sequences": sum(len(p["seqs"]) for p in preps)}
    assert same_text and same_ids and same_groups, rep["tokenizers_identical_on_all_prompts"]
    # 3) the adapter is applied: logits with it on differ from logits with it off
    probe = [p for p in preps if p["d"]["suite"] in ("sst2", "ag_news", "xnli_en", "typed-decisions")][:8] or preps[:8]
    eff = rd.adapter_effect(probe)
    rep["adapter_effect_max_logit_diff_on_vs_off"] = eff
    assert eff > 1e-3, f"C1 and base give the same logits on probe items (diff {eff}): the adapter is not applied"
    # 4) smoke items: 2 per suite; batched read vs one-sequence-at-a-time read; probabilities sane; C1 differs from base
    pick = []
    for s, lst in by_suite(ds).items():
        pick += [d for d in lst[:2]]
    sp = rd.prepare_many(pick, "main")
    jobs = [(s, p["groups"]) for p in sp for s in p["seqs"]]
    items, res = [], {}
    for arm in ("c1", "base"):
        with rd.arm(arm):
            bat, _ = rd.read_jobs(jobs)
            one = [rd.read_jobs([j])[0][0] for j in jobs]
        k, rows = 0, []
        for p in sp:
            n = len(p["seqs"])
            pb = rd.decide(p, bat[k:k + n])
            p1 = rd.decide(p, one[k:k + n])
            k += n
            rows.append({"id": p["d"]["id"], "suite": p["d"]["suite"], "type": p["d"]["q"]["type"], "gold": p["d"]["gold"],
                         "pred": max(range(len(pb)), key=pb.__getitem__), "conf": max(pb), "sum": sum(pb),
                         "max_prob_diff_batched_vs_single": max(abs(x - y) for x, y in zip(pb, p1)),
                         "argmax_same": max(range(len(pb)), key=pb.__getitem__) == max(range(len(p1)), key=p1.__getitem__)})
        res[arm] = rows
    for arm, rows in res.items():
        assert all(abs(r["sum"] - 1) < 1e-4 for r in rows), arm
        assert max(r["max_prob_diff_batched_vs_single"] for r in rows) < 0.1, (arm, max(r["max_prob_diff_batched_vs_single"] for r in rows))
        assert len({round(r["conf"], 3) for r in rows}) > 5 or a.min_conf_diff == 0, f"{arm}: confidences are nearly constant"
    cd = [abs(x["conf"] - y["conf"]) for x, y in zip(res["c1"], res["base"])]
    rep["smoke_c1_vs_base_mean_abs_conf_diff"] = sum(cd) / len(cd)
    assert rep["smoke_c1_vs_base_mean_abs_conf_diff"] > a.min_conf_diff, "C1 and base answer alike on the smoke items: adapter not applied"
    rep["smoke"] = res
    rep["smoke_max_prob_diff_batched_vs_single"] = {arm: max(r["max_prob_diff_batched_vs_single"] for r in rows) for arm, rows in res.items()}
    # 5) sanity on a known-easy task: C1 reads SST-2 (first 40) well above chance
    s2 = [p for p in preps if p["d"]["suite"] == "sst2"][:40]
    if s2:
        jobs2 = [(s, p["groups"]) for p in s2 for s in p["seqs"]]
        lg, _ = rd.read_jobs(jobs2)   # yes/no: one sequence per decision, so lg[i] is decision i
        hit = 0
        for i, p in enumerate(s2):
            pr = rd.decide(p, [lg[i]])
            hit += int(max(range(2), key=pr.__getitem__) == p["d"]["gold"])
        acc = hit / len(s2)
        rep["sst2_first40_c1_acc"] = acc
        assert acc >= a.min_sst2_acc, f"C1 gets {acc:.2f} on {len(s2)} SST-2 reviews: the readout is broken"
    out.json("gates.json", rep)
    log("gates ok", json.dumps({k: v for k, v in rep.items() if k != "smoke"})[:700])
    return preps


# ------------------------------------------------------------------ main pass
def run_suite(rd, preps, arm):
    """Candidate logits for every view of every prepared decision of one suite, with the arm's LoRA state. Returns records."""
    jobs = [(s, p["groups"]) for p in preps for s in p["seqs"]]
    err = None
    for attempt in (0, 1):  # a failed batch is retried once (after freeing cached memory) and flagged
        try:
            with rd.arm(arm):
                lg, stats = rd.read_jobs(jobs)
            err = None
            break
        except Exception as e:  # noqa: BLE001  a failure is logged, never hidden
            err = f"{type(e).__name__}: {str(e)[:300]}"
            torch.cuda.empty_cache()
            log("batch failure", arm, preps[0]["d"]["suite"], err, "(retrying)" if attempt == 0 else "(giving up)")
    recs, k = [], 0
    for p in preps:
        n = len(p["seqs"])
        if err:
            recs.append(tt.error_record(p, err))
        else:
            recs.append(tt.result_record(p, lg[k:k + n], rd.decide(p, lg[k:k + n])))
            if attempt == 1:
                recs[-1]["retried"] = True
        k += n
    return recs, (None if err else stats)


def main_stage(rd, a, ds, preps_all, out, arms):
    groups = {}
    for p in preps_all:
        groups.setdefault(p["d"]["suite"], []).append(p)
    files = {arm: out.jsonl(f"preds_{arm}.jsonl") for arm in arms}
    timing = {arm: {"wall_s": 0.0, "real_tokens": 0, "padded_tokens": 0, "oom_splits": 0, "batches": 0, "suites": {}} for arm in arms}
    done = {arm: [] for arm in arms}
    for suite in SUITE_ORDER:
        if suite not in groups:
            continue
        if late(a):
            out.skip(f"main:{suite}")
            continue
        for arm in arms:
            tt.sync(rd.dev)
            t0 = time.time()
            recs, st = run_suite(rd, groups[suite], arm)
            tt.sync(rd.dev)
            dt = time.time() - t0
            for r in recs:
                files[arm].write(json.dumps(r) + "\n")
            files[arm].flush()
            ok = [r for r in recs if "error" not in r]
            acc = sum(r["correct"] for r in ok) / max(1, len(ok))
            timing[arm]["wall_s"] += dt
            timing[arm]["suites"][suite] = {"wall_s": dt, "n": len(recs), "errors": len(recs) - len(ok), "acc_micro": acc}
            if st:
                for k in ("real_tokens", "padded_tokens", "oom_splits", "batches"):
                    timing[arm][k] += st[k]
            done[arm].append(suite)
            log(f"main {arm:4s} {suite:20s} n={len(recs):4d} err={len(recs) - len(ok)} acc={acc:.3f} {dt:6.1f}s "
                f"{(st or {}).get('real_tokens', 0) / max(dt, 1e-9):8.0f} tok/s  total {sum(timing[x]['wall_s'] for x in arms):6.0f}s")
    for f in files.values():
        f.close()
    for arm in arms:
        timing[arm]["suites_done"] = done[arm]
        timing[arm]["peak_gpu_mem_gb"] = torch.cuda.max_memory_allocated() / 2 ** 30 if torch.cuda.is_available() else None
    out.json("summary_main.json", timing)


# ------------------------------------------------------------------ latency sample (batch 1)
def lat_stage(rd, a, ds, out, arms):
    cases = {}
    for d in ds:
        cases.setdefault(d["suite"], {}).setdefault(d["id"], []).append(d)
    sample = []
    for s in SUITE_ORDER:
        sample += list(cases.get(s, {}).items())[:LAT_PER_SUITE]
    main_probs = {}
    for arm in arms:
        path = os.path.join(out.path, f"preds_{arm}.jsonl")
        if os.path.exists(path):
            for line in open(path):
                r = json.loads(line)
                if "error" not in r:
                    main_probs[(arm, r["id"], r["qid"])] = r["probs"]
    for arm in arms:
        if late(a):
            out.skip(f"lat:{arm}")
            continue
        f = out.jsonl(f"lat_{arm}.jsonl")
        order = sample[:LAT_WARM] + sample  # the first LAT_WARM cases run twice; only the second pass is kept
        with rd.arm(arm):
            for n, (cid, qs) in enumerate(order):
                timed = n >= LAT_WARM
                tt.sync(rd.dev)
                t0 = time.perf_counter()
                try:
                    preps = rd.prepare_many(qs, "main")
                    t1 = time.perf_counter()
                    jobs = [(s, p["groups"]) for p in preps for s in p["seqs"]]
                    lg, _ = rd.read_jobs(jobs, token_budget=10 ** 9, max_batch=10 ** 6)  # all questions of the call in ONE batch
                    probs = []
                    k = 0
                    for p in preps:
                        nseq = len(p["seqs"])
                        probs.append(rd.decide(p, lg[k:k + nseq]))
                        k += nseq
                    tt.sync(rd.dev)
                    t2 = time.perf_counter()
                    rec = {"id": cid, "suite": qs[0]["suite"], "nq": len(qs), "n_seq": len(jobs), "n_tokens": sum(len(j[0]) for j in jobs),
                           "prep_ms": (t1 - t0) * 1000, "fwd_ms": (t2 - t1) * 1000, "total_ms": (t2 - t0) * 1000,
                           "max_prob_diff_vs_batched": max((max(abs(x - y) for x, y in zip(pr, main_probs[(arm, cid, p['d']['qid'])]))
                                                            for pr, p in zip(probs, preps) if (arm, cid, p["d"]["qid"]) in main_probs),
                                                           default=None),
                           "argmax_same_as_batched": all(max(range(len(pr)), key=pr.__getitem__) ==
                                                         max(range(len(main_probs[(arm, cid, p['d']['qid'])])),
                                                             key=main_probs[(arm, cid, p['d']['qid'])].__getitem__)
                                                         for pr, p in zip(probs, preps) if (arm, cid, p["d"]["qid"]) in main_probs)}
                except Exception as e:  # noqa: BLE001
                    torch.cuda.empty_cache()
                    rec = {"id": cid, "suite": qs[0]["suite"], "error": f"{type(e).__name__}: {str(e)[:300]}"}
                if timed:
                    f.write(json.dumps(rec) + "\n")
                    f.flush()
        f.close()
        rows = [json.loads(x) for x in open(os.path.join(out.path, f"lat_{arm}.jsonl"))]
        ok = [r for r in rows if "error" not in r]
        log(f"lat {arm}: {len(ok)}/{len(rows)} calls, total p50/p95 {pct([r['total_ms'] for r in ok], 50):.0f}/"
            f"{pct([r['total_ms'] for r in ok], 95):.0f} ms; argmax same as batched pass on {sum(r['argmax_same_as_batched'] for r in ok)}/{len(ok)} calls")


# ------------------------------------------------------------------ diagnostics
def diag_stage(rd, a, ds, out, arms):
    for arm in arms:
        f = out.jsonl(f"diag_{arm}.jsonl")
        for variant in ("score_noprefix", "yn_swapped"):
            for suite in SUITE_ORDER:
                sub = [d for d in ds if d["suite"] == suite and tt.variant_applies(d, variant)]
                if not sub:
                    continue
                if late(a):
                    out.skip(f"diag:{arm}:{variant}:{suite}")
                    continue
                preps = rd.prepare_many(sub, variant)
                t0 = time.time()
                recs, st = run_suite(rd, preps, arm)
                for r in recs:
                    f.write(json.dumps(r) + "\n")
                f.flush()
                ok = [r for r in recs if "error" not in r]
                log(f"diag {arm:4s} {variant:14s} {suite:20s} n={len(recs):4d} err={len(recs) - len(ok)} "
                    f"acc={sum(r['correct'] for r in ok) / max(1, len(ok)):.3f} {time.time() - t0:5.1f}s")
        f.close()


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("mode", choices=["eval"])
    ap.add_argument("--out", default=os.path.expanduser("~/text_track/results"))
    ap.add_argument("--stages", default="gates,main,lat,diag")
    ap.add_argument("--arms", default="c1,base")
    ap.add_argument("--dev", default="cuda")
    ap.add_argument("--deadline-s", type=float, default=None, help="do not start new work after this many seconds")
    ap.add_argument("--max-cases", type=int, default=None, help="per suite, for dry runs only (the gates skip the data-lock check)")
    ap.add_argument("--route", default="causal", choices=["causal", "mm"])
    ap.add_argument("--min-conf-diff", type=float, default=0.005, help="gate: mean |conf(c1) - conf(base)| on the smoke items")
    ap.add_argument("--min-sst2-acc", type=float, default=0.75, help="gate: C1 accuracy on the first 40 SST-2 items (dry runs lower it)")
    a = ap.parse_args()
    stages = a.stages.split(",")
    arms = a.arms.split(",")
    out = Out(a.out)
    rd = tt.Reader(dev=a.dev, route=a.route)
    log("loaded", f"{rd.load_s:.0f}s", "class", type(rd.top).__name__, "layout", rd.layout, "style", rd.style, "adapter", json.dumps(rd.adapter_check))
    ds = tt.load_decisions(max_cases=a.max_cases)
    mt = meta(rd, a, ds)
    out.json("meta.json", mt)
    log("meta written; decisions", len(ds))
    preps = None
    if "gates" in stages:
        preps = gates(rd, a, ds, out)
    if "main" in stages:
        preps = preps or rd.prepare_many(ds, "main")
        main_stage(rd, a, ds, preps, out, arms)
    if "lat" in stages:
        lat_stage(rd, a, ds, out, arms)
    if "diag" in stages:
        diag_stage(rd, a, ds, out, arms)
    mt["process_wall_s"] = time.time() - T_START
    mt["loadavg_end"] = os.getloadavg()
    out.json("meta.json", mt)
    log("done", f"{mt['process_wall_s']:.0f}s")


if __name__ == "__main__":
    main()
