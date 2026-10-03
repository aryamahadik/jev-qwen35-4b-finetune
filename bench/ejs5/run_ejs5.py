"""Run ONE OpenDecide system once on the 868 ejs-5 rows (C1 4B, the 2B, or the 2B -> 4B cascade). Blind: no gold is
read, nothing is scored here, no item text is printed (score with score_ejs5.py afterwards).

  # L4 VM (see README.md): one model per call; refuses a busy GPU and a second run under the same name / adapter
  ~/od/bin/python ~/bench/ejs5/run_ejs5.py --name c1_main500k --model ~/lean/models/q35_4b_main500k \
      --base Qwen/Qwen3.5-4B --revision 851bf6e806efd8d0a36b00ddf55e13ccb7b8cd0a \
      --adapter-sha256 507d1c29690579f928a265713cd14b9c54a34baa8b74abd1e641560d987db078 --rows-sha256 <PREREG value>
  # cascade: composed offline from the two models' runs (no GPU), rule = prep89/ohs3_lib.cascade_answer
  python run_ejs5.py --cascade --name cascade_2b_c1 --small <2B run> --big c1_main500k --fit-log <dev-only fit json>
  # CPU checks (no GPU): --dry-run (build + check every prompt, count tokens) / --fake-model (tiny random model)

Readout (PREREG_ejs5): decoder_io.cand_logits on ONE row per forward pass (batch 1, eager), probabilities =
decoder_io.to_probs at T = 1 (no temperature, no calibration, no TTA). --readout 2view (choice rows also read in the
exact reversed option order and averaged, A5 / prep89 READOUT_DEV) exists only so the owner can pre-register the shipped
A5 readout instead; the default is the single read. The model is loaded like prep89/ohs3_backends.load_real:
decoder_io.load(base, adapter=..., revision=...) (layout / style / PRISM-X from train_meta.json / prism_x.json),
adapter sha256 (and prism_x.safetensors sha256) checked BEFORE loading, base commit checked after, merge_and_unload,
PRISM-X control plane active iff prism_x.json exists.

Writes <out>/preds.jsonl (id, probs, latency_s, n_tokens, error), manifest.json (adapter + code sha256, versions, GPU),
timing.json, and appends started / complete to <runs>/ledger.jsonl.
"""
from __future__ import annotations

import argparse
import datetime as dt
import json
import math
import os
import platform
import subprocess
import sys
import time
from pathlib import Path

import ejs5lib as E


def utc():
    return dt.datetime.now(dt.timezone.utc).isoformat(timespec="seconds")


def default_lean():
    env = os.environ.get("EJS5_LEAN")
    if env:
        return env
    home = Path.home() / "lean"
    return str(home if (home / "decoder_io.py").exists() else E.ROOT / "opendecide-data" / "lean")


def gpu_users():
    """None: no nvidia-smi (no GPU); "": the GPU is free; else the compute processes using it."""
    try:
        out = subprocess.run(["nvidia-smi", "--query-compute-apps=pid,process_name,used_memory", "--format=csv,noheader"],
                             capture_output=True, text=True, timeout=30)
    except Exception:
        return None
    if out.returncode != 0:
        return None
    return out.stdout.strip()


# ------------------------------------------------------------------ ledger (one run per name and per adapter)

def ledger(runs: Path):
    p = runs / "ledger.jsonl"
    return E.read_jsonl(p) if p.exists() else []


def ledger_append(runs: Path, rec):
    runs.mkdir(parents=True, exist_ok=True)
    with open(runs / "ledger.jsonl", "a") as f:
        f.write(json.dumps({**rec, "utc": utc()}) + "\n")


def check_once(runs: Path, name: str, out: Path, adapter_sha=None, restart=False):
    """Refuses a second run under the same name, and a second completed run of the same adapter (weights) under any
    name. --restart-crashed: only a run that was started and never completed (nothing was scored) may be restarted."""
    L = ledger(runs)
    mine = [r for r in L if r["name"] == name]
    if adapter_sha:
        other = [r for r in L if r.get("adapter_sha256") == adapter_sha and r["event"] == "complete" and r["name"] != name]
        if other:
            raise SystemExit(f"STOP: adapter {adapter_sha[:16]} already has a complete ejs-5 run ({other[0]['name']})")
    if not mine and not out.exists():
        return False
    if restart and mine and not any(r["event"] == "complete" for r in mine):
        return True
    raise SystemExit(f"STOP: run {name!r} already exists ({out} / ledger: {[r['event'] for r in mine]}); each system runs "
                     "once (PREREG_ejs5). Only a started-but-never-completed run may use --restart-crashed.")


# ------------------------------------------------------------------ rows

def load_rows(path: Path, want_sha: str | None):
    sha = E.sha256_file(path)
    if sha is None:
        raise SystemExit(f"{path}: missing (run convert.py first)")
    if want_sha and sha != want_sha:
        raise SystemExit(f"{path.name}: sha256 {sha[:16]} != pre-registered {want_sha[:16]}")
    rows = E.read_jsonl(path)
    return rows, sha


def pick_spread(rows, n):
    """n rows for a smoke run, spread over the four tasks."""
    if not n or n >= len(rows):
        return rows
    per = max(1, math.ceil(n / len(E.TASKS)))
    out = []
    for t in E.TASKS:
        tr = [r for r in rows if r["meta"]["task"] == t]
        k = min(per, len(tr))
        out += [tr[int(i * len(tr) / k)] for i in range(k)] if k else []
    return out[:n]


# ------------------------------------------------------------------ pre-flight (every prompt, before any GPU time)

def preflight(dio, rows, tok, prism_x_on):
    """Each row's prompt is the real decoder_io prompt: the user message follows decoder_io.LAYOUT (cygnet_msg is inside
    the chat text), the candidate set has one entry per answer, and for PRISM-X the token-role spans are found."""
    import hashlib
    if prism_x_on:
        import prism_x
    ro = dio.Readout(tok)
    stats = []
    for r in rows:
        text = ro.prompt(r)
        if dio.STYLE == "cygnet" and dio.cygnet_msg(dio.as_letter_row(r)) not in text:
            raise SystemExit(f"{r['id']}: prompt does not follow decoder_io.LAYOUT={dio.LAYOUT!r}")
        n_ans = 2 if r["qtype"] == "noul" else len(r["options"])
        if len(ro.cand(r)) != n_ans:
            raise SystemExit(f"{r['id']}: {len(ro.cand(r))} candidate groups for {n_ans} answers")
        if prism_x_on:
            prism_x.row_char_spans(r, None, text)  # raises if PRISM-X cannot place its token roles
        n = len(tok(text, add_special_tokens=False)["input_ids"])
        stats.append({"id": r["id"], "task": r.get("_task"), "n_answers": n_ans, "n_tokens": n,
                      "prompt_sha256": hashlib.sha256(text.encode()).hexdigest()})
    return ro, stats


# ------------------------------------------------------------------ models

def load_gpu(dio, a, model_dir: Path):
    import torch
    if not torch.cuda.is_available():
        raise SystemExit("CUDA is not available")
    model, tok, info = dio.load(a.base, "cuda", adapter=str(model_dir), revision=a.revision, return_info=True)
    commit = getattr(getattr(model, "config", None), "_commit_hash", None)
    if a.revision and commit is not None and commit != a.revision:
        raise SystemExit(f"loaded base commit {commit}, pre-registered {a.revision}")
    model = model.merge_and_unload()  # as od_gcp predict / ohs3_backends.load_real; PRISM-X hooks survive the merge
    model.eval()
    return model, tok, {**info, "base_commit": commit}


def tiny_model(tok, dio, prism_x_on, seed=0):
    """A random Qwen3 (hidden 32) with the real vocabulary: the full readout path on CPU, answers are noise. With
    PRISM-X a control plane (authority + option head; shadow heads need Gated DeltaNet layers) is installed with seeded
    non-zero weights, as prep89/ohs3_backends.load_tiny_px."""
    import torch
    from transformers import Qwen3Config, Qwen3ForCausalLM
    torch.manual_seed(seed)
    cfg = Qwen3Config(vocab_size=len(tok), hidden_size=32, intermediate_size=64, num_hidden_layers=2 if prism_x_on else 1,
                      num_attention_heads=2, num_key_value_heads=1, head_dim=16, max_position_embeddings=32768,
                      tie_word_embeddings=False)
    model = Qwen3ForCausalLM(cfg).eval()
    if prism_x_on:
        import prism_x
        prism_x.install(model, prism_x.resolve({"authority": True, "option_head": True}), "cpu")
        g = torch.Generator().manual_seed(seed + 1)
        with torch.no_grad():
            for _, p in prism_x.PX.named_parameters():
                p.copy_(torch.randn(p.shape, generator=g) * 0.5)
        prism_x.PX.eval()
    return model


def prism_active(dio, model) -> bool:
    pxm = dio._prism_x()
    return bool(pxm is not None and pxm.active_for(dio._parts(model)[0]))


# ------------------------------------------------------------------ the read

def read_all(dio, model, ro, rows, dev, readout, ntok, log_every=100, max_consecutive_errors=5):
    import torch
    sync = torch.cuda.synchronize if dev == "cuda" else (lambda: None)
    recs, consecutive = [], 0
    with torch.no_grad():
        for i, r in enumerate(rows):
            t0 = time.perf_counter()
            p1 = probs = None
            err = None
            try:
                lg = dio.cand_logits(model, ro, [r], dev)[0]
                p1 = dio.to_probs(r, lg)  # temp = 1.0
                probs = p1
                if readout == "2view" and r["qtype"] == "choice":
                    rev = list(range(len(r["options"])))[::-1]
                    lg2 = dio.cand_logits(model, ro, [r], dev, perms=[rev])[0]
                    p2 = dio.to_probs(r, lg2, rev)
                    probs = {o: (p1[o] + p2[o]) / 2 for o in r["options"]}
                sync()
                consecutive = 0
            except Exception as e:  # an unanswered row counts wrong (the author's rule); the error type is kept
                p1 = probs = None
                err = type(e).__name__
                consecutive += 1
            rec = {"id": r["id"], "task": r["_task"], "probs": probs, "latency_s": time.perf_counter() - t0,
                   "n_tokens": ntok[i], "error": err}
            if readout == "2view":
                rec["probs_1v"] = p1
            recs.append(rec)
            if consecutive >= max_consecutive_errors:
                raise SystemExit(f"STOP: {consecutive} consecutive rows failed ({err}); the run is incomplete")
            if (i + 1) % log_every == 0 or i + 1 == len(rows):
                print(f"  read {i + 1}/{len(rows)}", flush=True)
    return recs


def timing_summary(recs, extra):
    lat = [r["latency_s"] * 1000 for r in recs if not r["error"]]
    by = {}
    for t in E.TASKS:
        lt = [r["latency_s"] * 1000 for r in recs if r["task"] == t and not r["error"]]
        if lt:
            by[t] = {"n": len(lt), "p50_ms": E.pct(lt, .5), "p95_ms": E.pct(lt, .95)}
    nt = [r["n_tokens"] for r in recs if r.get("n_tokens")]
    return {**extra, "n": len(recs), "errors": sum(1 for r in recs if r["error"]),
            "latency_ms": {"p50": E.pct(lat, .5), "p95": E.pct(lat, .95), "mean": sum(lat) / len(lat) if lat else None,
                           "max": max(lat) if lat else None},
            "by_task": by, "input_tokens": {"mean": sum(nt) / len(nt) if nt else None, "max": max(nt) if nt else None,
                                            "total": sum(nt)},
            "note": "per-row model time: tokenisation + one prefill forward pass (two on 2-view choice rows) at batch 1, "
                    "eager, CUDA-synchronised; no network, no server. Not an end-to-end API latency."}


# ------------------------------------------------------------------ cascade (offline, from the two runs)

def run_cascade(a, runs: Path):
    if not (a.small and a.big and a.fit_log):
        raise SystemExit("--cascade needs --small, --big and --fit-log")
    sd = Path(a.small) if Path(a.small).is_dir() else runs / a.small
    bd = Path(a.big) if Path(a.big).is_dir() else runs / a.big
    ms, mb = (json.loads((d / "manifest.json").read_text()) for d in (sd, bd))
    for d, m in ((sd, ms), (bd, mb)):
        if m.get("status") != "complete" or not (d / "preds.jsonl").exists():
            raise SystemExit(f"{d.name}: not a complete run")
    test = not (ms["mode"] == mb["mode"] == "gpu")
    if ms["rows_sha256"] != mb["rows_sha256"]:
        raise SystemExit("the two runs read different rows files")
    fit = json.loads(Path(a.fit_log).read_text())
    cv = fit["config_values"]
    tau, w, route_on = float(cv["tau"]), float(cv["w_big"]), cv["route_on"]
    names = {"small": Path(ms["adapter"]).name, "big": Path(mb["adapter"]).name}
    fit_names = {"small": fit["small"]["model"], "big": fit["big"]["model"]}
    if names != fit_names and not a.allow_fit_mismatch:
        raise SystemExit(f"STOP: the fit log is for {fit_names}, the runs are {names}; a cascade needs the dev-only fit "
                         "of THESE two models (or the owner's recorded --allow-fit-mismatch)")
    t_small = fit["small"].get("T") or {"noul": 1.0, "choice": 1.0}
    if route_on == "primary" and any(abs(float(v) - 1.0) > 1e-12 for v in t_small.values()):
        raise SystemExit(f"STOP: route_on 'primary' with the small model's T {t_small} != 1, but this protocol reads "
                         "at T = 1 (route_on 'raw' routes on exactly the T = 1 probabilities)")
    name = a.name + ("_test" if test else "")
    out = Path(a.out) if a.out else runs / name
    restart = False if test else check_once(runs, name, out, None, a.restart_crashed)
    rows, rsha = load_rows(Path(a.rows), a.rows_sha256)
    if rsha != ms["rows_sha256"]:
        raise SystemExit("the rows file differs from the one the runs read")
    Ps = {p["id"]: p for p in E.read_jsonl(sd / "preds.jsonl")}
    Pb = {p["id"]: p for p in E.read_jsonl(bd / "preds.jsonl")}
    if test:  # CPU test runs may cover a subset (--limit): compose on the rows both runs read
        rows = [r for r in rows if r["id"] in Ps and r["id"] in Pb]
    elif len(Ps) != len(rows) or len(Pb) != len(rows):
        raise SystemExit(f"component runs cover {len(Ps)} / {len(Pb)} rows, the rows file has {len(rows)}")
    if not test:
        ledger_append(runs, {"name": name, "event": "restarted" if restart else "started", "mode": "cascade",
                             "rows_sha256": rsha})
    recs, routed = [], 0
    for r in rows:
        s, b = Ps.get(r["id"]), Pb.get(r["id"])
        if s is None or b is None:
            raise SystemExit("a row is missing from a component run (counts only)")
        if s["probs"] is None:  # the small model gave no answer: the cascade gives none either (counted wrong)
            recs.append({"id": r["id"], "task": r["meta"]["task"], "probs": None, "routed": None,
                         "latency_s": s["latency_s"], "n_tokens": s.get("n_tokens"), "error": "small:" + str(s["error"])})
            continue
        rt = E.cascade_routed(r, s["probs"], tau)
        if rt and b["probs"] is None:
            recs.append({"id": r["id"], "task": r["meta"]["task"], "probs": None, "routed": True,
                         "latency_s": s["latency_s"] + b["latency_s"], "n_tokens": s.get("n_tokens"),
                         "error": "big:" + str(b["error"])})
            routed += 1
            continue
        routed += rt
        recs.append({"id": r["id"], "task": r["meta"]["task"],
                     "probs": E.cascade_answer(r, s["probs"], b["probs"] if rt else None, rt, w), "routed": rt,
                     "latency_s": s["latency_s"] + (b["latency_s"] if rt else 0.0), "n_tokens": s.get("n_tokens"),
                     "error": None})
    out.mkdir(parents=True, exist_ok=True)
    E.write_jsonl_atomic(out / "preds.jsonl", recs)
    tm = timing_summary(recs, {"composed": "small latency + big latency on routed rows (offline composition of two "
                                           "batch-1 runs on the same GPU; no routing overhead, no second load)"})
    by_task = {t: sum(1 for x in recs if x["task"] == t and x["routed"]) for t in E.TASKS}
    E.write_json_atomic(out / "timing.json", tm)
    man = {"name": name, "mode": "cascade" if not test else "cascade-test", "status": "complete",
           "small": {"run": sd.name, "adapter": ms["adapter"], "adapter_sha256": ms.get("adapter_sha256"),
                     "readout": ms.get("readout")},
           "big": {"run": bd.name, "adapter": mb["adapter"], "adapter_sha256": mb.get("adapter_sha256"),
                   "readout": mb.get("readout")},
           "tau": tau, "w_big": w, "route_on": route_on, "fit_log": str(a.fit_log),
           "fit_log_sha256": E.sha256_file(a.fit_log), "fit_models": fit_names, "fit_mismatch_allowed": names != fit_names,
           "rule": "ejs5lib.cascade_answer == prep89/ohs3_lib.cascade_answer (tests/test_ejs5.py checks equality)",
           "rows": str(a.rows), "rows_sha256": rsha, "n_rows": len(rows), "routed": routed,
           "routed_share": round(routed / len(rows), 4) if rows else None, "routed_by_task": by_task,
           "readout": "cascade", "T": 1.0,
           "code_sha256": {"run_ejs5.py": E.sha256_file(__file__), "ejs5lib.py": E.sha256_file(E.__file__)},
           "finished_utc": utc()}
    E.write_json_atomic(out / "manifest.json", man)
    if not test:
        ledger_append(runs, {"name": name, "event": "complete", "mode": "cascade", "rows_sha256": rsha})
    print(f"cascade {name}: routed {routed}/{len(rows)} rows to {bd.name} (tau {tau:.4f}, w_big {w}, route_on "
          f"{route_on}); wrote {out}")
    return man


# ------------------------------------------------------------------ main

def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--name", required=True, help="run name (one run per name, PREREG_ejs5)")
    ap.add_argument("--model", help="adapter dir (adapter_model.safetensors, train_meta.json, prism_x.* for the 2B)")
    ap.add_argument("--base", help="base model id, e.g. Qwen/Qwen3.5-4B")
    ap.add_argument("--revision", default=None, help="exact Hugging Face commit of the base")
    ap.add_argument("--adapter-sha256", default=None, help="pre-registered sha256 of adapter_model.safetensors (gpu)")
    ap.add_argument("--prism-x-sha256", default=None, help="pre-registered sha256 of prism_x.safetensors (2B, gpu)")
    ap.add_argument("--rows", default=str(E.ROWS), help="rows file from convert.py")
    ap.add_argument("--rows-sha256", default=None, help="pre-registered sha256 of the rows file (required for gpu)")
    ap.add_argument("--readout", default="single", choices=("single", "2view"), help="single (default) or A5 2-view")
    ap.add_argument("--lean", default=default_lean(), help="lean code dir (decoder_io.py, prism_x.py)")
    ap.add_argument("--runs", default=str(E.RUNS), help="runs dir (ledger.jsonl lives here)")
    ap.add_argument("--out", default=None, help="output dir (default <runs>/<name>[_dry|_fake])")
    ap.add_argument("--limit", type=int, default=0, help="dry-run / fake-model only: N rows spread over the tasks")
    ap.add_argument("--ids", nargs="*", default=None, help=argparse.SUPPRESS)  # tests only
    ap.add_argument("--warmup-tokens", type=int, default=0, help="largest warm-up bucket (default: from the pre-flight)")
    ap.add_argument("--dry-run", action="store_true", help="CPU: build and check every prompt, count tokens; no model")
    ap.add_argument("--fake-model", action="store_true", help="CPU: tiny random model through the real readout path")
    ap.add_argument("--allow-shared-gpu", action="store_true", help="start even if another process uses the GPU")
    ap.add_argument("--restart-crashed", action="store_true", help="restart a run that started and never completed")
    ap.add_argument("--cascade", action="store_true", help="compose the cascade from two finished runs (no GPU)")
    ap.add_argument("--small", help="cascade: the 2B run (name under --runs, or a dir)")
    ap.add_argument("--big", help="cascade: the 4B run")
    ap.add_argument("--fit-log", help="cascade: the dev-only fit json (prep89/cascade_rule_fit.py output)")
    ap.add_argument("--allow-fit-mismatch", action="store_true", help="cascade: owner-recorded use of another pair's fit")
    a = ap.parse_args(argv)
    runs = Path(a.runs).expanduser().resolve()
    if a.cascade:
        return run_cascade(a, runs)
    if not (a.model and a.base):
        raise SystemExit("--model and --base are required")
    mode = "dry-run" if a.dry_run else "fake-model" if a.fake_model else "gpu"
    if mode == "gpu":
        if a.limit or a.ids:
            raise SystemExit("--limit is for --dry-run / --fake-model only: the GPU run reads every row once")
        if not (a.adapter_sha256 and a.rows_sha256 and a.revision):
            raise SystemExit("the GPU run needs --adapter-sha256, --rows-sha256 and --revision (PREREG_ejs5 values)")
    model_dir = Path(a.model).expanduser().resolve()
    lean = Path(a.lean).expanduser().resolve()
    out = Path(a.out).expanduser().resolve() if a.out else runs / f"{a.name}{'_dry' if a.dry_run else ''}" \
        f"{'_fake' if a.fake_model else ''}"
    px_json = (model_dir / "prism_x.json").exists()
    adapter_sha = E.sha256_file(model_dir / "adapter_model.safetensors")
    px_sha = E.sha256_file(model_dir / "prism_x.safetensors") if px_json else None

    users, restart = None, False
    if mode == "gpu":
        restart = check_once(runs, a.name, out, adapter_sha, a.restart_crashed)
        if adapter_sha != a.adapter_sha256:
            raise SystemExit(f"adapter sha256 {str(adapter_sha)[:16]} != pre-registered {a.adapter_sha256[:16]}")
        if px_json and px_sha != a.prism_x_sha256:
            raise SystemExit(f"prism_x.safetensors sha256 {str(px_sha)[:16]} != pre-registered "
                             f"{str(a.prism_x_sha256)[:16]}")
        if not px_json and a.prism_x_sha256:
            raise SystemExit("--prism-x-sha256 given but the adapter has no prism_x.json")
        users = gpu_users()
        if users is None:
            raise SystemExit("nvidia-smi not found: no GPU here (use --dry-run or --fake-model for CPU checks)")
        if users and not a.allow_shared_gpu:
            raise SystemExit("the GPU is in use (a training run?), refusing to start so it is not disturbed:\n" + users)
    elif out.exists():
        raise SystemExit(f"{out} exists (delete it to repeat a CPU check)")

    rows_all, rsha = load_rows(Path(a.rows).expanduser().resolve(), a.rows_sha256)
    rows_all = [r for r in rows_all if not a.ids or r["id"] in a.ids]
    rows_all = pick_spread(rows_all, a.limit) if mode != "gpu" else rows_all
    mrows = [{**E.model_row(r), "_task": r["meta"]["task"]} for r in rows_all]  # no gold, no labels

    sys.path.insert(0, str(lean))
    import torch
    import decoder_io as dio
    from transformers import AutoTokenizer
    info = dio.resolve_prompt([str(model_dir)], a.base, None, None, a.revision)
    dio.LAYOUT = info["layout"] or dio.LAYOUT
    dio.STYLE = info["style"] or dio.STYLE
    if px_json:
        px = json.loads((model_dir / "prism_x.json").read_text())
        if (px["layout"], px["style"]) != (dio.LAYOUT, dio.STYLE):
            raise SystemExit(f"prism_x.json layout/style {(px['layout'], px['style'])} != train_meta "
                             f"{(dio.LAYOUT, dio.STYLE)}")
    tok0 = AutoTokenizer.from_pretrained(str(model_dir))
    ro0, stats = preflight(dio, mrows, tok0, px_json)
    ntok = [s["n_tokens"] for s in stats]
    print(json.dumps({"run_ejs5": {"name": a.name, "mode": mode, "rows": len(mrows), "layout": dio.LAYOUT,
                                   "style": dio.STYLE, "prism_x": px_json, "readout": a.readout}}), flush=True)
    print(f"pre-flight OK on {len(stats)} prompts (layout followed{', PRISM-X spans found' if px_json else ''}); "
          f"tokens mean {sum(ntok) / max(1, len(ntok)):.0f}, max {max(ntok) if ntok else '-'}", flush=True)

    started = utc()
    manifest = {
        "name": a.name, "mode": mode, "status": "running", "base": a.base, "revision": a.revision,
        "adapter": str(model_dir), "adapter_sha256": adapter_sha, "adapter_sha256_preregistered": a.adapter_sha256,
        "prism_x": px_json, "prism_x_sha256": px_sha, "readout": a.readout, "T": 1.0,
        "rows": str(Path(a.rows).resolve()), "rows_sha256": rsha, "rows_sha256_preregistered": a.rows_sha256,
        "n_rows": len(mrows), "limit": a.limit or None,
        "layout": dio.LAYOUT, "style": dio.STYLE, "resolve_prompt": info,
        "code_sha256": {"decoder_io.py": E.sha256_file(dio.__file__), "prism_x.py": E.sha256_file(lean / "prism_x.py"),
                        "run_ejs5.py": E.sha256_file(__file__), "ejs5lib.py": E.sha256_file(E.__file__),
                        "convert.py": E.sha256_file(Path(__file__).with_name("convert.py"))},
        "code_paths": {"decoder_io": dio.__file__, "lean": str(lean)},
        "host": platform.node(), "python": sys.version.split()[0], "torch": torch.__version__,
        "hf_hub_offline": os.environ.get("HF_HUB_OFFLINE"), "hf_home": os.environ.get("HF_HOME"),
        "started_utc": started, "preflight": {"n": len(stats), "tokens_mean": sum(ntok) / max(1, len(ntok)),
                                              "tokens_max": max(ntok) if ntok else None},
    }
    try:
        import transformers
        manifest["transformers"] = transformers.__version__
    except Exception:
        pass
    out.mkdir(parents=True, exist_ok=mode == "gpu" and restart)
    if mode == "dry-run":
        E.write_jsonl_atomic(out / "prompts.jsonl", stats)
        manifest.update(status="complete", finished_utc=utc())
        E.write_json_atomic(out / "manifest.json", manifest)
        print(f"dry-run: wrote {out}/prompts.jsonl (token counts and prompt sha256 only)")
        return manifest

    E.write_json_atomic(out / "manifest.json", manifest)  # status "running" until the read completes
    t0 = time.time()
    if mode == "gpu":
        ledger_append(runs, {"name": a.name, "event": "restarted" if restart else "started", "mode": mode,
                             "adapter_sha256": adapter_sha, "rows_sha256": rsha})
        model, tok, linfo = load_gpu(dio, a, model_dir)
        if (dio.LAYOUT, dio.STYLE) != (manifest["layout"], manifest["style"]):
            raise SystemExit(f"layout/style after load {(dio.LAYOUT, dio.STYLE)} != pre-flight "
                             f"{(manifest['layout'], manifest['style'])}")
        if prism_active(dio, model) != px_json:
            raise SystemExit(f"PRISM-X active {prism_active(dio, model)} but prism_x.json present {px_json}")
        ro = dio.Readout(tok)
        dev = "cuda"
        manifest.update(load={k: v for k, v in linfo.items() if k != "adapters"}, gpu=torch.cuda.get_device_name(0),
                        gpu_users_before_load=users, cuda=torch.version.cuda)
    else:
        tok, ro, dev = tok0, ro0, "cpu"
        model = tiny_model(tok, dio, px_json)
        manifest["load"] = {"note": "fake-model: random Qwen3 (hidden 32) + the real tokenizer; answers are noise",
                            "prism_x_tiny": px_json}
    manifest["prism_x_active"] = prism_active(dio, model)
    if manifest["prism_x_active"] != px_json:
        raise SystemExit("PRISM-X control plane state does not match prism_x.json")
    load_s = time.time() - t0
    tw = time.time()
    if mode == "gpu":  # server start-up: every padded length bucket once, filler text only (no item text)
        wt = a.warmup_tokens or max(1024, dio.PAD_MULTIPLE * math.ceil((max(ntok) + 64) / dio.PAD_MULTIPLE))
        dio.warmup(model, ro, max_tokens=wt, batch_sizes=(1,), dev=dev)
        manifest["warmup_tokens"] = wt
    warm_s = time.time() - tw
    print(f"loaded in {load_s:.0f}s, warm-up {warm_s:.0f}s; reading {len(mrows)} rows once (batch 1, "
          f"{a.readout} read, T=1)", flush=True)
    tr = time.time()
    recs = read_all(dio, model, ro, mrows, dev, a.readout, ntok)
    run_s = time.time() - tr
    E.write_jsonl_atomic(out / "preds.jsonl", recs)
    tm = timing_summary(recs, {"load_s": round(load_s, 1), "warmup_s": round(warm_s, 1), "run_s": round(run_s, 1),
                               "rows_per_s": round(len(recs) / run_s, 2) if run_s else None,
                               "device": manifest.get("gpu", "cpu (fake model)")})
    if mode == "gpu":
        tm["max_memory_gb"] = round(torch.cuda.max_memory_allocated() / 2 ** 30, 2)
    E.write_json_atomic(out / "timing.json", tm)
    manifest.update(status="complete", finished_utc=utc(), n_errors=tm["errors"])
    E.write_json_atomic(out / "manifest.json", manifest)
    if mode == "gpu":
        ledger_append(runs, {"name": a.name, "event": "complete", "mode": mode, "adapter_sha256": adapter_sha,
                             "rows_sha256": rsha})
    lat = tm["latency_ms"]
    print(f"{a.name}: {len(recs)} rows read, {tm['errors']} errors, latency p50 {lat['p50']:.1f} ms p95 "
          f"{lat['p95']:.1f} ms; wrote {out}\nscore (Mac): python score_ejs5.py {out.name}")
    return manifest


if __name__ == "__main__":
    main()
