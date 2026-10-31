"""The 2B -> 4B cascade on LongBench v2 in the same longjev protocol (run AFTER both single-model runs, once).

  # on od-l4 after the owner's OK, when run_lb.py has finished for the 2B and for the 4B
  cd ~/bench/longbench_v2 && HF_HOME=$HOME/hf HF_HUB_OFFLINE=1 ~/od/bin/python cascade_lb.py \\
      --config cascade_lb.json --items ~/bench/external_quarantine/longbench_v2/kit/lb_items.jsonl
  # CPU test: --fake-model (tiny random models) with two fake single-model runs on synthetic items

The rule is prep89/ohs3_lib's (FINETUNE_PLAN 5.3): the small model answers every decision; a decision goes to the big
model when the top of the small model's routing probabilities (route_on "raw" = its A5 readout before T, "primary" =
after its T), renormalised over the row's answers, is below tau; a routed decision is w_big * big PRIMARY +
(1 - w_big) * small PRIMARY (PRIMARY = A5 readout + that model's T). It is applied to EVERY decision of the protocol:
  * chunk relevance (yes/no): offline from the two finished runs' stored reads of the same chunk rows (deterministic
    reads; this is what ohs3_cascade.py does), so the cascade's relevance = cascade_answer(...)["yes"];
  * the final four-option question over the cascade's own kept text: read live, the small model on every item, the
    big model on the routed ones (one model on the GPU at a time).
The functions here are ohs3_lib's, re-written keyed by option INDEX (ohs3_lib keys by option text, which merges the one
LongBench item with two identical options); tests/test_lb.py checks them against ohs3_lib on distinct options.
tau / w_big / route_on / T come from the config only, which must name the dev-only fit log (prep89/cascade_rule_fit.py
--json) and its sha256; every one of those values must equal the log's (config_values, small.T, big.T), or it refuses.

cascade_lb.json:
  {"name": "cascade_2b_4b", "tau": <from fit log>, "w_big": <from fit log>, "route_on": "raw" | "primary",
   "fit_log": "<path>", "fit_log_sha256": "<sha256>",
   "small": {"run": "runs/lb2_<2b>", "model": "<adapter dir>", "base": "Qwen/Qwen3.5-2B", "revision": "<commit>",
             "choice_readout": "2view" | "single", "T": {"noul": t, "choice": t}},
   "big":   {"run": "runs/lb2_<4b>", "model": "<adapter dir>", "base": "Qwen/Qwen3.5-4B", "revision": "<commit>",
             "choice_readout": "2view", "T": {"noul": t, "choice": t}}}
"""
from __future__ import annotations

import argparse
import gc
import json
import math
import sys
import time
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import lb_lib as lb  # noqa: E402
import lb_select as sel  # noqa: E402
import run_lb as R  # noqa: E402


# ---------------------------------------------------------------- the rule (ohs3_lib / calibrate.scaled, index-keyed)

def scaled(p: list, T: float) -> list:
    """calibrate.scaled: softmax(log max(p, 1e-12) / T) over the row's answers, in order."""
    lg = [math.log(max(x, 1e-12)) / T for x in p]
    m = max(lg)
    ex = [math.exp(x - m) for x in lg]
    s = sum(ex)
    return [e / s for e in ex]


def norm(p: list) -> list:
    s = sum(p) or 1.0
    return [x / s for x in p]


def routed(p_route: list, tau: float) -> bool:
    return max(norm(p_route)) < float(tau)


def answer(p_small: list, p_big: list | None, is_routed: bool, w_big: float) -> list:
    ps = norm(p_small)
    if is_routed:
        pb = norm(p_big)
        ps = [float(w_big) * x + (1 - float(w_big)) * y for x, y in zip(pb, ps)]
    return ps


def noul_p(p_yes: float) -> list:
    """decoder_io.to_probs for a cygnet yes/no row: {"yes": p, "no": 1 - p}, in that key order."""
    return [p_yes, 1 - p_yes]


def cascade_rel(c: dict, ps_yes: float, pb_yes: float) -> tuple:
    """(cascade P(yes), routed) for one chunk relevance decision."""
    Ts, Tb = c["small"]["T"]["noul"], c["big"]["T"]["noul"]
    raw = noul_p(ps_yes)
    s_pri = scaled(raw, Ts)
    rt = routed(s_pri if c["route_on"] == "primary" else raw, c["tau"])
    fin = answer(s_pri, scaled(noul_p(pb_yes), Tb) if rt else None, rt, c["w_big"])
    return fin[0], rt


# ---------------------------------------------------------------- checks

def load_config(path):
    c = json.loads(Path(path).read_text())
    for k in ("name", "tau", "w_big", "route_on", "small", "big"):
        if k not in c:
            raise SystemExit(f"config lacks {k}")
    flat = json.dumps(c)
    if '"<' in flat:
        raise SystemExit("config still has <placeholders>; fill them from the dev-only fit log")
    if c["route_on"] not in ("raw", "primary"):
        raise SystemExit("route_on must be raw or primary")
    for m in ("small", "big"):
        for k in ("run", "model", "base", "choice_readout", "T"):
            if k not in c[m]:
                raise SystemExit(f"config {m} lacks {k}")
    check_fit_log(c)
    return c


def _same(a, b) -> bool:
    try:
        return abs(float(a) - float(b)) <= 1e-12
    except (TypeError, ValueError):
        return False


def check_fit_log(c):
    """tau / w_big / route_on and both T come ONLY from the dev-only fit log (prep89/cascade_rule_fit.py --json),
    named in the config with its sha256 (as ohs3_lib.check_cascade_log): a missing log, another sha256, a non-dev fit or
    any value that differs from the log is refused."""
    if not c.get("fit_log") or not c.get("fit_log_sha256"):
        raise SystemExit("config must name the dev-only fit log and its sha256 (fit_log, fit_log_sha256)")
    p = Path(c["fit_log"]).expanduser()
    if not p.exists():
        raise SystemExit(f"fit log not found: {p}")
    got = lb.sha256_file(p)
    if got != c["fit_log_sha256"]:
        raise SystemExit(f"fit log sha256 {got} != config's {c['fit_log_sha256']}")
    d = json.loads(p.read_text())
    if d.get("dev_only") is not True or any(str(s).startswith("ohs") for s in d.get("splits", [])):
        raise SystemExit("fit log is not a dev-only fit")
    cv = d.get("config_values")
    if not cv:
        raise SystemExit("fit log chose no cascade (no config_values)")
    bad = [k for k in ("tau", "w_big") if not _same(c[k], cv.get(k))]
    if c["route_on"] != cv.get("route_on"):
        bad.append("route_on")
    for m in ("small", "big"):
        ft = (d.get(m) or {}).get("T") or {}
        bad += [f"{m}.T.{q}" for q in ("noul", "choice") if not _same((c[m]["T"] or {}).get(q), ft.get(q))]
    if bad:
        raise SystemExit(f"config differs from its fit log on {bad}")
    return d


def load_run(run_dir, items_sha):
    run_dir = Path(run_dir)
    m = json.loads((run_dir / "manifest.json").read_text())
    if m.get("status") != "complete":
        raise SystemExit(f"{run_dir}: run not complete")
    if m["settings"]["items_sha256"] != items_sha:
        raise SystemExit(f"{run_dir}: ran on a different items file")
    cs = {r["id"]: r for r in lb.read_jsonl(run_dir / "chunk_scores.jsonl")}
    ran = {r["id"] for r in lb.read_jsonl(run_dir / "preds.jsonl") if r.get("arm", "keep8k") == "keep8k"}
    if ran - set(cs):
        raise SystemExit(f"{run_dir}: {len(ran - set(cs))} finished items have no stored chunk scores")
    return m, cs


PROTOCOL_KEYS = ("protocol", "budget", "chunk_tokens", "chars_per_token", "cap_tokens", "jev_proxy_cpt", "gap_tokens",
                 "too_long_retries", "items_sha256", "data_sha256", "sets")


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--config", required=True)
    ap.add_argument("--items", required=True)
    ap.add_argument("--out", default=None)
    ap.add_argument("--lean", default=R.default_lean())
    ap.add_argument("--fake-model", action="store_true")
    ap.add_argument("--allow-shared-gpu", action="store_true")
    a = ap.parse_args(argv)
    c = load_config(a.config)
    fit = check_fit_log(c)
    items_path = Path(a.items).expanduser().resolve()
    meta_items, items_sha, real = R.check_items(items_path)
    if real and a.fake_model:
        raise SystemExit("--fake-model on REAL items is not allowed")
    ms, cs_s = load_run(c["small"]["run"], items_sha)
    mb, cs_b = load_run(c["big"]["run"], items_sha)
    for k in PROTOCOL_KEYS:
        if ms["settings"].get(k) != mb["settings"].get(k):
            raise SystemExit(f"the two runs differ on {k}")
    for m, mm in (("small", ms), ("big", mb)):
        if mm["settings"]["choice_readout"] != c[m]["choice_readout"]:
            raise SystemExit(f"{m}: config readout != the run's")
        if mm["settings"]["adapter_sha256"] != R.adapter_files_sha(Path(c[m]["model"]).expanduser()).get(
                "adapter_model.safetensors"):
            raise SystemExit(f"{m}: config model is not the adapter of its run")
    if (ms["load"]["layout"], ms["load"]["style"]) != (mb["load"]["layout"], mb["load"]["style"]):
        raise SystemExit("the two models use different prompt layouts/styles")
    out = Path(a.out).expanduser().resolve() if a.out else HERE / "runs" / f"lb2_{c['name']}{'_fake' if a.fake_model else ''}"
    if out.exists():
        raise SystemExit(f"{out} exists: the cascade runs once")
    pair = [ms["settings"]["adapter_sha256"], mb["settings"]["adapter_sha256"]]
    if real and R.LEDGER.exists() and any(e.get("name") == c["name"] or (e.get("kind") == "cascade" and e.get("adapters") == pair)
                                          for e in lb.read_jsonl(R.LEDGER)):
        raise SystemExit("STOP (run once): the ledger already has this cascade (same name or same small/big adapters)")
    items = [it for it in lb.read_jsonl(items_path) if it["id"] in cs_s and it["id"] in cs_b]
    if not items:
        raise SystemExit("no items in both runs")
    users = None
    if not a.fake_model:
        users = R.gpu_users()
        if users is None:
            raise SystemExit("nvidia-smi not found")
        if users and not a.allow_shared_gpu:
            raise SystemExit("the GPU is in use:\n" + users)
    out.mkdir(parents=True)
    R.ledger_append(real, {"event": "start", "name": c["name"], "kind": "cascade", "adapters": pair,
                           "data_sha256": lb.DATA_SHA256, "out": str(out), "utc": R.utc()})
    sys.path.insert(0, str(Path(a.lean).expanduser().resolve()))
    import torch
    import decoder_io as dio

    # 1) chunk relevance: offline cascade of the stored reads; selection on the cascade's scores
    plan, n_ch, n_rt = {}, 0, 0
    big_chunk_tokens = 0
    for it in items:
        s, b = cs_s[it["id"]], cs_b[it["id"]]
        if s["tokens"] != b["tokens"]:
            raise SystemExit("chunk token counts differ between the runs (different tokenizers)")
        chunks = lb.recalibrate(lb.chunk_state(it["context"]), s["tokens"])
        rel, rts = [], []
        for ys, yb in zip(s["p_yes"], b["p_yes"]):
            p, rt = cascade_rel(c, ys, yb)
            rel.append(p)
            rts.append(rt)
        kept, budget = sel.keep(it, chunks, rel)
        plan[it["id"]] = (chunks, kept, budget, sum(rts), len(rts))
        n_ch += len(rts)
        n_rt += sum(rts)
        big_chunk_tokens += sum(t for t, r in zip(s["tokens"], rts) if r)

    # 2) final reads: the small model on every item, then the big model on the routed ones
    def reads(which, rows_by_id):
        m = c[which]
        model, tok, info, dev = R.load_reader(dio, Path(m["model"]).expanduser().resolve(), m["base"], m.get("revision"),
                                              a.fake_model)
        rd = R.Reader(dio, model, tok, dev, m["choice_readout"], 16, 12000)
        res = {}
        t0 = time.perf_counter()
        for iid, (chunks, kept) in rows_by_id.items():
            res[iid] = R.final_read(rd, next(x for x in items if x["id"] == iid), chunks, kept, dio.MAX_LEN)
        R.sync(dev)
        dt_ = time.perf_counter() - t0
        info_out = {"layout": info.get("layout"), "style": info.get("style"), "prism_x": rd.px, "final_s": round(dt_, 1)}
        del model, rd
        gc.collect()
        if dev == "cuda":
            torch.cuda.empty_cache()
        return res, info_out

    small_res, small_info = reads("small", {i: (p[0], p[1]) for i, p in plan.items()})
    route = {}
    for iid, r in small_res.items():
        if r["p"] is None:
            route[iid] = False
            continue
        raw = r["p"]
        pri = scaled(raw, c["small"]["T"]["choice"])
        route[iid] = routed(pri if c["route_on"] == "primary" else raw, c["tau"])
    big_ids = [i for i, x in route.items() if x]
    big_res, big_info = reads("big", {i: (plan[i][0], plan[i][1]) for i in big_ids}) if big_ids else ({}, None)
    with open(out / "preds.jsonl", "w") as fp:
        for iid, (chunks, kept, budget, crt, cn) in plan.items():
            sr = small_res[iid]
            rec = {"id": iid, "arm": "keep8k_cascade", "sets": [s for s in lb.SETS if lb.in_set(
                next(x for x in items if x["id"] == iid), s)], "budget": budget, "chunks_routed": crt, "n_chunks": cn,
                   **{k: sr[k] for k in ("kept", "n_kept", "kept_tokens", "kept_chars", "too_long_drops",
                                         "final_prompt_tokens")}, "final_routed": route[iid]}
            if sr["p"] is None:
                rec.update(final_failed=sr["final_failed"], p=None, pred=None, pred_1view=None, p1=None)
            else:
                s_pri = scaled(sr["p"], c["small"]["T"]["choice"])
                br = big_res.get(iid)
                if route[iid] and (br is None or br["p"] is None):
                    rec.update(final_failed="big_read_failed", p=None, pred=None, pred_1view=None, p1=None)
                else:
                    b_pri = scaled(br["p"], c["big"]["T"]["choice"]) if route[iid] else None
                    fin = answer(s_pri, b_pri, route[iid], c["w_big"])
                    rec.update(final_failed=None, p=fin, pred=lb.argmax_letter(fin), p1=None,
                               pred_1view=lb.argmax_letter(sr["p1"]))
            fp.write(json.dumps(rec) + "\n")
    manifest = {"name": c["name"], "status": "complete", "config": c, "config_sha256": lb.sha256_file(a.config),
                "items": str(items_path), "items_sha256": items_sha, "n_items": len(items),
                "chunks": n_ch, "chunks_routed": n_rt, "chunk_routed_share": round(n_rt / max(1, n_ch), 4),
                "big_chunk_tokens_if_served": big_chunk_tokens,
                "final_routed": len(big_ids), "final_routed_share": round(len(big_ids) / len(items), 4),
                "small": small_info, "big": big_info,
                "runs": {"small": str(c["small"]["run"]), "big": str(c["big"]["run"])},
                "adapters_sha256": {"small": pair[0], "big": pair[1]},
                "fit_log_models": {m: (fit.get(m) or {}).get("model") for m in ("small", "big")},
                "code_sha256": {"cascade_lb.py": lb.sha256_file(__file__), "run_lb.py": lb.sha256_file(R.__file__),
                                "lb_lib.py": lb.sha256_file(lb.__file__), "lb_select.py": lb.sha256_file(sel.__file__),
                                "decoder_io.py": lb.sha256_file(dio.__file__),
                                "prism_x.py": lb.sha256_file(Path(dio.__file__).parent / "prism_x.py")
                                if (Path(dio.__file__).parent / "prism_x.py").exists() else None},
                "mode": "fake-model" if a.fake_model else "gpu", "finished_utc": R.utc()}
    (out / "manifest.json").write_text(json.dumps(manifest, indent=2))
    R.ledger_append(real, {"event": "complete", "name": c["name"], "kind": "cascade", "adapters": pair,
                           "data_sha256": lb.DATA_SHA256, "out": str(out), "utc": R.utc()})
    print(json.dumps({"cascade": {k: manifest[k] for k in ("n_items", "chunks", "chunk_routed_share", "final_routed",
                                                           "final_routed_share")}, "out": str(out)}))
    return out


if __name__ == "__main__":
    main()
