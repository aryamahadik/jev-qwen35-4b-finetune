"""oc1.runner: the measurement process of one SGLang boot (run under C1's pinned stack, /opt/fastpath/bin/python).

  python -m oc1.runner prep    --spec S --out O    tokenize + render the workloads once (pickles in /tmp), no server needed
  python -m oc1.runner measure --spec S --out O    parity / latency / throughput / prefix / score readout against a server
  python -m oc1.runner front   --spec S --out O    the end-to-end HTTP front (oc1.front) until /shutdown (token: env OC1_TOKEN)

`measure` writes its result file after EVERY step, so a timeout or crash keeps what finished. Parity is computed here, the
moment a config's answers exist, against the S1 baseline of the SAME session (out_dir/../s1/answers_P.jsonl) and, when the
file is shipped, against SPEED-2's stored S1 answers (work_dir/ref_speed2_S1_answers_P.jsonl); the full answer files are
also kept on the Volume for the laptop-side re-analysis (accuracy needs the gold labels, which stay on the laptop).
"""
from __future__ import annotations

import argparse
import json
import os
import sys
import time
import traceback
from pathlib import Path

from . import common as C
from . import items as I
from . import parity as PAR

SUB_N = 2500            # stratified parity subsample (seed 0): identical ids in every config
LAT_N, LAT_S = 320, 140  # batch-1 latency: natural mix N, heavy mix S
LAT_B_ROUNDS = 40
TP_CONC = (16, 64)
PREFIX_N, PREFIX_CONC = 800, 8


class Ctx:
    def __init__(self, spec: dict, log=print):
        self.spec, self.log = spec, log
        self.work = spec["work_dir"]
        self.out_dir = Path(spec["out_dir"])
        self.params = spec.get("params", {})
        self.R = I.readout_mod()
        self.SH = I.sglang_host_mod()
        t0 = time.time()
        self.tok, self.ro, self.info = I.load_c1(spec["c1_dir"])
        log(f"tokenizer + readout ready in {time.time() - t0:.0f} s")
        self._items, self._preps = {}, {}

    def items(self, name):
        if name not in self._items:
            self._items[name] = I.load_items(self.work, name)
        return self._items[name]

    def preps(self, name):
        if name not in self._preps:
            self._preps[name] = I.prepare_cached(name, self.items(name), self.R, self.ro, self.tok, self.log)
        return self._preps[name]


def wait_go(spec: dict, log=print):
    """Initialization is done; wait until the session says the server passed its argument check (go_file exists), or give up
    when abort_file appears. Lets the tokenizer / Readout / workload preparation overlap with the SGLang boot."""
    g = spec.get("go_file")
    if not g:
        return
    t0 = time.time()
    while not Path(g).exists():
        if spec.get("abort_file") and Path(spec["abort_file"]).exists():
            raise SystemExit("aborted before the go signal")
        if time.time() - t0 > float(spec.get("go_timeout_s", 1800)):
            raise SystemExit("no go signal")
        time.sleep(0.5)
    log(f"go after {time.time() - t0:.0f} s of waiting")


def pick(preps, ids):
    by = {p.id: p for p in preps}
    return [by[i] for i in ids if i in by]


def save_answers(path, answers):
    C.write_jsonl(path, [{"id": k, **v} for k, v in answers.items()])


def load_answers(path):
    if not path or not Path(path).exists():
        return None
    return {r["id"]: r["probs"] for r in C.read_jsonl(path)}


def step_parity(ctx: Ctx, backend, sampler, full: bool, tag: str, ref_paths: dict) -> dict:
    from . import measure as M
    items = ctx.items("P")
    sub = items if full else PAR.stratified_sample(items, int(ctx.params.get("sub_n", SUB_N)), seed=0)
    preps = pick(ctx.preps("P"), [it["id"] for it in sub])
    res = M.parity_pass(backend, preps, conc=int(ctx.params.get("parity_conc", 16)), sampler=sampler)
    ans_path = ctx.out_dir / f"answers_P{tag}.jsonl"
    save_answers(ans_path, res.pop("answers"))
    cand = load_answers(ans_path)
    out = {"n_requested": len(preps), "answers_file": str(ans_path), **res}
    for label, path in ref_paths.items():
        ref = load_answers(path)
        if ref:
            sub_items = [it for it in sub if it["id"] in ref]
            out[f"parity_vs_{label}"] = PAR.compare_items(sub_items, cand, ref)
    return out


def step_latency(ctx: Ctx, backend, sampler) -> dict:
    from . import measure as M
    out = {}
    lat_n, lat_s = int(ctx.params.get("lat_n", LAT_N)), int(ctx.params.get("lat_s", LAT_S))
    warm = int(ctx.params.get("lat_warm", 20))
    N, S = ctx.preps("N"), ctx.preps("S")
    for p in N[:warm]:
        backend.read(p, False)       # extra warm-up (Triton / graph shapes) before anything is timed
    out["batch1_N"] = M.latency_batch1(backend, N[:lat_n + warm], warm=warm, sampler=sampler)
    out["batch1_S_heavy"] = M.latency_batch1(backend, S[:lat_s + warm], warm=warm, sampler=sampler)
    out["batched_N"] = M.latency_batched(backend, N[lat_n + warm:], b=8, rounds=int(ctx.params.get("lat_rounds", LAT_B_ROUNDS)))
    return out


def step_throughput(ctx: Ctx, backend, client, sampler) -> dict:
    from . import measure as M
    conc = tuple(ctx.params.get("tp_conc", TP_CONC))
    out = {"S": M.throughput(backend, ctx.preps("S"), conc, client=client, sampler=sampler)}
    out["N_c64"] = M.throughput(backend, ctx.preps("N"), (max(conc),), client=client, sampler=sampler)
    n_p = int(ctx.params.get("tp_p_rows", 2500 if ctx.spec.get("config") == "s1" else 0))
    if n_p:        # a long saturation run on the natural mix (the ramp-up/down of a 660-row set is a visible share of it)
        out["P_sat"] = M.throughput(backend, ctx.preps("P")[:n_p], (max(conc),), client=client, sampler=sampler)
    return out


def step_prefix(ctx: Ctx, backend, client) -> dict:
    from . import measure as M
    return M.prefix_hit(backend, ctx.preps("R"), client=client, conc=int(ctx.params.get("prefix_conc", PREFIX_CONC)),
                        n=int(ctx.params.get("prefix_n", PREFIX_N)))


def quant_report(path="/tmp/oc1_quant_report.jsonl") -> dict | None:
    p = Path(path)
    if not p.exists():
        return None
    recs = [json.loads(x) for x in p.read_text().splitlines() if x.strip()]
    by = {}
    for r in recs:
        if "prefix" in r:
            by.setdefault(r["mode"], set()).add(r["prefix"])
    import re
    from . import configs as K
    allp = sorted({p for v in by.values() for p in v})
    groups = {g: sum(1 for p in allp if any(re.search(rx, p) for rx in rxs)) for g, rxs in K.FP8_GROUP_REGEX.items()}
    return {"patched": [r for r in recs if "patched" in r][:1], "errors": [r for r in recs if "patch_error" in r][:3],
            "counts": {k: len(v) for k, v in by.items()}, "group_matches": groups,       # a 0 here = fix that group's regex
            "all_prefix_sample": allp[:6] + allp[-6:],
            "bf16_prefix_sample": sorted(by.get("bf16", []))[:12],
            "quantized_prefix_sample": sorted(by.get("fp8", set()) | by.get("int8", set()))[:12]}


def run_measure(spec: dict, log=print) -> dict:
    from . import measure as M
    from .backend import GenerateBackend, ScoreBackend
    ctx = Ctx(spec, log)
    out_path = Path(spec["out_path"])
    meas0 = spec["measures"]
    need = ["N"] + (["S"] if {"latency", "throughput", "score_readout"} & set(meas0) else []) \
        + (["R"] if "prefix" in meas0 else []) + (["P"] if {"parity_full", "parity_sub", "score_readout"} & set(meas0) else [])
    for name in need:                  # tokenized / rendered while the server is still booting
        ctx.preps(name)
    wait_go(spec, log)
    client = ctx.SH.SGLangClient(spec["sgl_url"], timeout=120.0, max_connections=300)
    gen = GenerateBackend(client)
    res = {"config": spec["config"], "started_utc": C.utc(), "steps": {}, "errors": {}}
    base = Path(spec["out_dir"]).parent / "s1" / "answers_P.jsonl"
    refs = {}
    if spec["config"] != "s1" and base.exists():
        refs["s1_same_session"] = str(base)
    stored = Path(ctx.work) / "ref_speed2_S1_answers_P.jsonl"
    if stored.exists():
        refs["speed2_S1_stored"] = str(stored)

    def flush_out():
        C.write_json(out_path, res)

    def run(name, fn):
        t0 = time.time()
        try:
            res["steps"][name] = fn()
            res["steps"][name]["step_wall_s"] = round(time.time() - t0, 1)
            log(f"STEP {name} done in {time.time() - t0:.0f} s")
        except Exception as e:  # noqa: BLE001
            res["errors"][name] = f"{type(e).__name__}: {str(e)[:300]}"
            log(f"STEP {name} FAILED: {res['errors'][name]}\n{traceback.format_exc()[-800:]}")
        flush_out()

    meas = spec["measures"]
    with M.GpuSampler(0.5) as sampler:
        # warm-up: JIT / graph shapes, then an empty cache
        t0 = time.time()
        try:
            M.closed_loop(gen.read, ctx.preps("N")[:60], 4)
            M.flush(client)
        except Exception as e:  # noqa: BLE001
            res["errors"]["warmup"] = f"{type(e).__name__}: {e}"
        res["warmup_s"] = round(time.time() - t0, 1)
        full = "parity_full" in meas
        if full or "parity_sub" in meas:
            M.flush(client)
            run("parity_full" if full else "parity_sub",
                lambda: step_parity(ctx, gen, sampler, full, "" if full else "_sub", refs))
            if full and "s1_same_session" not in refs:   # the baseline itself: compare with SPEED-2's stored S1 (done above)
                pass
        if "latency" in meas:
            run("latency", lambda: step_latency(ctx, gen, sampler))
        if "throughput" in meas:
            run("throughput", lambda: step_throughput(ctx, gen, client, sampler))
        if "prefix" in meas:
            run("prefix", lambda: step_prefix(ctx, gen, client))
        if "score_readout" in meas:
            sc = ScoreBackend(client)

            def score_all():
                o = {"parity": step_parity(ctx, sc, sampler, False, "_score", {**refs, "generate_same_boot": str(ctx.out_dir / "answers_P.jsonl")})}
                w, n = int(ctx.params.get("lat_warm", 20)), int(ctx.params.get("lat_n", LAT_N))
                o["latency_batch1_N"] = M.latency_batch1(sc, ctx.preps("N")[:n + w], warm=w, sampler=sampler)
                o["throughput_S"] = M.throughput(sc, ctx.preps("S"), (min(TP_CONC),), client=client, sampler=sampler)
                return o
            run("score_readout", score_all)
    qr = quant_report()
    if qr:
        res["quant_report"] = qr
    res["finished_utc"] = C.utc()
    flush_out()
    return res


def run_prep(spec: dict, log=print) -> dict:
    ctx = Ctx(spec, log)
    out = {}
    for name in spec.get("workloads", ["N", "S", "R", "P"]):
        t0 = time.time()
        preps = ctx.preps(name)
        out[name] = {"rows": len(preps), "tokens": sum(p.n_tokens for p in preps), "s": round(time.time() - t0, 1)}
        log(f"prep {name}: {out[name]}")
    return out


def run_voice_c1(spec: dict, log=print) -> dict:
    """C1 on the ORIGINAL spoken states vs on the ASR transcripts (per mode): argmax agreement and mean |dp| of the answers,
    and the C1-side latency of a transcript decision cold vs with the static prefix already cached (the prefix = system +
    instructions + options + definitions, everything before the state: it can be prefilled while the person speaks)."""
    from . import measure as M
    from . import voice as V
    from .backend import GenerateBackend, answer_probs
    ctx = Ctx(spec, log)
    voice = json.loads(Path(spec["voice_result"]).read_text())
    prompts = json.loads(Path(spec["prompts_file"]).read_text())
    by_id = {p["id"]: p for p in prompts}
    client = ctx.SH.SGLangClient(spec["sgl_url"], timeout=120.0, max_connections=64)
    gen = GenerateBackend(client)
    modes = ["offline", "stream160", "stream560"]
    texts = {m: {it["id"]: (it.get(m) or {}).get("text") for it in voice["items"]} for m in modes}
    texts["orig"] = {p["id"]: p["request"]["state"] for p in prompts}
    out = {"n_prompts": len(prompts), "modes": {}}

    def answers_for(mode):
        items = [{"id": f"{pid}|{mode}", "bucket": "noul" if by_id[pid]["qtype"] == "noul" else "choice",
                  "qtype": by_id[pid]["qtype"], "n_options": 0,
                  "request": V.with_state(by_id[pid]["request"], t)} for pid, t in texts[mode].items() if t is not None]
        preps = [I.prepare_one(it, ctx.R, ctx.ro, ctx.tok) for it in items]
        M.flush(client)
        recs, wall = M.closed_loop(gen.read, preps, 8)
        ans = {}
        for r in recs:
            if r["ok"]:
                pid = r["id"].split("|")[0]
                a = next(iter(r["answers"].values()))
                ans[pid] = answer_probs(a, by_id[pid]["qtype"])
        return items, preps, ans, M.loop_summary(recs, wall)

    ref_items, ref_preps, ref_ans, _ = answers_for("orig")
    cmp_items = [{**it, "id": it["id"].split("|")[0]} for it in ref_items]
    for m in modes:
        items, preps, ans, summ = answers_for(m)
        rep = PAR.compare_items(cmp_items, ans, ref_ans, agree_min=0.0)
        dps = []
        for pid, a in ans.items():
            if pid in ref_ans:
                opts = PAR.item_options(next(i for i in cmp_items if i["id"] == pid))
                dps.append(PAR.row_dp(opts, a, ref_ans[pid]))
        out["modes"][m] = {"n": rep["n"], "argmax_agree": rep["argmax_agree"], "dp_mean": round(sum(dps) / len(dps), 5) if dps else None,
                           "dp_p90": round(C.pct(dps, 0.9), 5) if dps else None, "flips": rep["n_flips"], "loop": summ,
                           "wer_mean": voice.get("modes", {}).get(m, {}).get("wer_mean")}
        log(f"voice_c1 {m}: agree {rep['argmax_agree']} on {rep['n']}")
        if m == "stream560":
            cold, warm = [], []
            for p in preps[:80]:
                M.flush(client)
                t0 = time.perf_counter()
                gen.read(p, False)
                cold.append((time.perf_counter() - t0) * 1000.0)
            for it, p in zip(items[:80], preps[:80]):
                M.flush(client)
                req0 = V.with_state(it["request"], ".")
                gen.read(I.prepare_one({"id": "warm", "bucket": "", "request": req0}, ctx.R, ctx.ro, ctx.tok), False)
                t0 = time.perf_counter()
                _, meta = gen.read(p, False)
                warm.append(((time.perf_counter() - t0) * 1000.0, meta.get("cached_tokens"), meta.get("prompt_tokens")))
            out["c1_latency_ms"] = {"cold_flushed": C.summarize(cold), "prefix_warm": C.summarize([w[0] for w in warm]),
                                    "prefix_cached_share": round(sum((w[1] or 0) for w in warm) / max(sum((w[2] or 0) for w in warm), 1), 4)}
    return out


def run_vision_cmd(spec: dict, log=print) -> dict:
    from . import vision as V
    return V.run_vision(spec, log)


def run_front_cmd(spec: dict, log=print) -> dict:
    from . import front as F
    token = os.environ.get("OC1_TOKEN") or ""
    if not token:
        raise SystemExit("OC1_TOKEN is not set")
    return F.run_front(spec, token, log=log)


def main(argv=None) -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("cmd", choices=["prep", "measure", "front", "voice_c1", "vision"])
    ap.add_argument("--spec", required=True)
    ap.add_argument("--out", required=True)
    a = ap.parse_args(argv)
    spec = json.loads(Path(a.spec).read_text())
    spec["out_path"] = a.out
    try:
        fn = {"prep": run_prep, "measure": run_measure, "front": run_front_cmd, "voice_c1": run_voice_c1, "vision": run_vision_cmd}[a.cmd]
        res = fn(spec, log=lambda s: print(s, flush=True))
        if a.cmd != "measure":
            C.write_json(a.out, res)
        return 0
    except BaseException as e:  # noqa: BLE001
        traceback.print_exc()
        try:
            prev = json.loads(Path(a.out).read_text())
        except (OSError, ValueError):
            prev = {}
        prev["fatal"] = f"{type(e).__name__}: {str(e)[:400]}"
        C.write_json(a.out, prev)
        return 1


if __name__ == "__main__":
    sys.exit(main())
