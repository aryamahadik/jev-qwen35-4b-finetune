"""CPU dry run of the 4B top-up q35_4b_main500k_fix2 (A8-prime B/C): no GPU, no Modal call, no network.

What it runs, in order (any failure stops it):
  1. the exact config extra/fix2_spawn.build_cfg sends (fixed clock), and its differences from the main run's config;
  2. fix2_spawn.local_checks: data sha256 = fix2_counts.json, expect_kd_* = the built counts, epochs = one pass
     (replay_steps), the image's data mount listed with Modal's own walker = exactly the two fix2 files, frozen code =
     C1's train_meta "code";
  3. the init adapter = the local C1 backup (config r16/a32, targets, fp32, finite, parameter count = expect_trainable,
     sha256 = the gate's C1);
  4. the learning-rate schedule train_decoder applies (5% linear warm-up, then cosine to 0) and the 20% ramp of the
     consistency terms;
  5. the first batch exactly as train() draws it (replay_steps.stream): its units, their part (F7 / G_t / F4 / G_r) and
     the relation terms compute_loss will score (train_decoder.aux_counts), plus the totals over the whole pass;
  6. a speed estimate: padded tokens per step (train_decoder._micro_groups at micro_tokens 8192) of this pass vs the
     main run's first 3,000 steps on golden_train, times the main run's measured 2.720 s/step;
  7. train_decoder.train() itself on CPU, stopped at the model load (train_decoder.load replaced by a function that
     raises): the unknown-key check, style / layout, reading the data, check_rows, make_units and expect_kd_targets /
     expect_kd_full all run for real.

  PYTHONDONTWRITEBYTECODE=1 ../.venv/bin/python extra/fix2_dryrun.py [--out extra/fix2_dryrun.json]
"""
from __future__ import annotations

import argparse
import json
import math
import random
import statistics
import sys
import tempfile
from collections import Counter, defaultdict
from pathlib import Path

LEAN = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(LEAN))
sys.path.insert(0, str(LEAN / "extra"))
sys.dont_write_bytecode = True

import fix2_spawn as fs  # noqa: E402  (imports modal_od: defines the app and images, sends nothing)
import replay_steps as rs  # noqa: E402

MAIN_CFG = LEAN / "runs/q35_4b_main.json"
GOLDEN_STEPS = 3000


class StopBeforeModelLoad(Exception):
    pass


def init_adapter_checks(cfg) -> dict:
    import torch
    from safetensors import safe_open
    B = fs.BACKUP
    ac = json.loads((B / "adapter_config.json").read_text())
    bad = []
    for k, v in (("r", cfg["r"]), ("lora_alpha", cfg["alpha"]), ("lora_dropout", cfg["dropout"]),
                 ("target_modules", fs.QWEN35_TARGETS), ("use_dora", False), ("use_rslora", False),
                 ("peft_type", "LORA"), ("base_model_name_or_path", cfg["base"])):
        if ac.get(k) != v:
            bad.append(f"adapter_config {k} = {ac.get(k)!r}, expected {v!r}")
    n, dtypes, keys = 0, set(), 0
    with safe_open(str(B / "adapter_model.safetensors"), "pt") as f:
        for k in f.keys():
            t = f.get_tensor(k)
            n += t.numel()
            dtypes.add(str(t.dtype))
            keys += 1
            if not torch.isfinite(t).all():
                bad.append(f"{k} not finite")
    if n != cfg["expect_trainable"]:
        bad.append(f"adapter has {n} parameters, expect_trainable is {cfg['expect_trainable']}")
    if dtypes != {"torch.float32"}:
        bad.append(f"adapter dtypes {dtypes} (train() needs fp32 trainable parameters)")
    sha = {f: fs.sha256_file(B / f) for f in fs.INIT_FILES}
    if sha != fs.c1_sha():
        bad.append(f"backup sha256 {sha} differs from the gate's C1 {fs.c1_sha()}")
    meta = json.loads((B / "train_meta.json").read_text())
    return {"tensors": keys, "parameters": n, "dtypes": sorted(dtypes), "sha256": sha, "main_run_steps": meta.get("steps"),
            "problems": bad}


def lr_points(lr, n_steps):
    warm = int(0.05 * n_steps)
    f = lambda s: (s + 1) / max(1, warm) if s < warm else 0.5 * (1 + math.cos(math.pi * (s - warm) / max(1, n_steps - warm)))  # noqa: E731
    pts = sorted({0, warm - 1, warm, n_steps // 4, n_steps // 2, (3 * n_steps) // 4, n_steps - 1})
    mean = sum(lr * f(s) for s in range(n_steps)) / n_steps
    return {"warmup_steps": warm, "ramp_full_from_step": math.ceil(0.2 * n_steps),
            "lr_at_step": {str(s): float(f"{lr * f(s):.3e}") for s in pts if s >= 0},
            "mean_lr": float(f"{mean:.3e}"), "sum_lr": round(sum(lr * f(s) for s in range(n_steps)), 5)}


def part_of(r, gt_calls):
    if r["source"] == "gd_gen3_nested_negation":
        return "F7"
    if r["source"] == "gd_gen3_polarity_ladder":
        return "F4"
    return "golden_dneg_unit" if r["call_id"] in gt_calls else "golden_other"


def padded_tokens(units, c, steps_limit=0):
    """Per step: sum over micro-batches of sequences x padded max length (the cost train() packs to), and the number of
    micro-batches, for the first pass (or its first steps_limit steps)."""
    import train_decoder as td
    uid = rs.unit_ids(units)
    budget = int(c.get("micro_tokens", 0) or 0)
    pad = max(1, td.decoder_io.PAD_MULTIPLE)
    tok, nmic = [], []

    def on_step(step, batch, perms, tw):
        groups = td._micro_groups(batch, uid, tw, budget) if budget else [list(range(len(batch)))]
        twin_n = Counter(i for i, _ in tw)
        t = 0
        for g in groups:
            ln = max(td._est_tokens(batch[i]) for i in g)
            t += sum(1 + twin_n[i] for i in g) * (-(-ln // pad) * pad)
        tok.append(t)
        nmic.append(len(groups))

    p = rs.first_pass(units, c, on_step=on_step, limit=steps_limit)
    return {"steps": p["batches"], "mean_padded_tokens": round(statistics.mean(tok), 1),
            "mean_micro_batches": round(statistics.mean(nmic), 3), "mean_rows": round(p["mean_rows_per_batch"], 3)}


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", default=str(LEAN / "extra/fix2_dryrun.json"))
    ap.add_argument("--no-speed", action="store_true", help="skip the golden_train speed comparison (about 2 min)")
    a = ap.parse_args(argv)
    res = {}
    # 1. the exact cfg the launcher sends
    name, cfg = fs.build_cfg(fs.CONFIG, expect_resume=False, stop_after_min=0, stop_at_step=0, log_every=0, now=0.0)
    res["name"], res["cfg_sent"] = name, cfg
    main_cfg = json.loads(MAIN_CFG.read_text())
    raw = json.loads((LEAN / fs.CONFIG).read_text())
    res["differs_from_main_run"] = {k: [main_cfg.get(k), raw.get(k)] for k in sorted(set(main_cfg) | set(raw))
                                    if main_cfg.get(k) != raw.get(k)}
    # 2. local checks (data, kd guards, one pass, data mount, frozen code)
    res["local_checks"] = fs.local_checks(cfg)
    # 3. init adapter
    res["init_adapter"] = init_adapter_checks(cfg)
    if res["init_adapter"]["problems"]:
        raise SystemExit(f"init adapter problems: {res['init_adapter']['problems']}")
    # 4. schedule
    n_steps = res["local_checks"]["steps"]
    res["lr_schedule"] = lr_points(cfg["lr"], n_steps)
    # 5. first batch + whole-pass relation terms
    import train_decoder as td
    c = {**rs.STREAM_DEFAULTS, **{k: v for k, v in cfg.items() if k in rs.STREAM_DEFAULTS}}
    rows_all, rows, rels, units, merged = rs.load_data(c, LEAN / "data")
    if merged:
        raise SystemExit(f"make_units merged {merged} inv pairs across call_ids")
    rel_by_row = defaultdict(list)
    for x in rels:
        rel_by_row[x["a"]].append(x)
    gt_calls = {r["call_id"] for r in rows if r.get("role") == "dneg" and r["source"] not in
                ("gd_gen3_nested_negation", "gd_gen3_polarity_ladder")}
    counts = json.loads(fs.COUNTS.read_text())
    first = {}
    tot = Counter()
    per_part = Counter()
    skipped_inv = 0

    def on_step(step, batch, perms, tw):
        nonlocal skipped_inv
        ac = td.aux_counts(cfg, batch, rel_by_row)
        tot.update(ac)
        tot["rows"] += len(batch)
        tot["twins"] += len(tw)
        for r in batch:
            per_part[part_of(r, gt_calls)] += 1
        pos = {r["id"]: i for i, r in enumerate(batch)}
        for r in batch:
            for x in rel_by_row.get(r["id"], []):
                if x["type"] == "inv" and (x["a"] not in pos or x["b"] not in pos
                                           or not td._align_ok(batch[pos[x["a"]]], batch[pos[x["b"]]])):
                    skipped_inv += 1
        if step == 0:
            us = defaultdict(list)
            for r in batch:
                us[r["call_id"]].append(r)
            ids = {r["id"] for r in batch}
            first.update({
                "rows": len(batch), "twins": len(tw), "aux_counts": dict(ac),
                "units": [{"call_id": k, "rows": len(u), "part": part_of(u[0], gt_calls), "source": u[0]["source"],
                           "roles": [r.get("role") for r in u],
                           "relations": dict(Counter(x["type"] for r in u for x in rel_by_row.get(r["id"], [])
                                                     if x["b"] in ids))} for k, u in us.items()]})

    p = rs.first_pass(units, c, on_step=on_step)
    res["first_batch"] = first
    res["pass_relation_terms"] = {"batches": p["batches"], "rows": tot["rows"], "twins": tot["twins"],
                                  "complement_terms": tot["comp"], "equiv_terms": tot["equiv"], "inv_terms": tot["inv"],
                                  "relations_in_file": dict(Counter(x["type"] for x in rels)),
                                  "dropped_units_at_pass_end": p["dropped_units"],
                                  "dropped_rows_at_pass_end": p["dropped_rows"], "inv_not_scorable": skipped_inv,
                                  "rows_by_part": dict(per_part), "rows_by_part_in_file": counts["parts"]}
    if skipped_inv:
        raise SystemExit(f"{skipped_inv} inv relations could not be scored in their batch")
    # 6. speed estimate
    if not a.no_speed:
        fx = padded_tokens(units, {**c, "micro_tokens": cfg["micro_tokens"]})
        gcfg = json.loads(MAIN_CFG.read_text())
        gc = {**rs.STREAM_DEFAULTS, **{k: v for k, v in gcfg.items() if k in rs.STREAM_DEFAULTS}}
        _, _, _, gunits, _ = rs.load_data(gc, LEAN / "data")
        gx = padded_tokens(gunits, {**gc, "micro_tokens": gcfg["micro_tokens"]}, steps_limit=GOLDEN_STEPS)
        ratio = fx["mean_padded_tokens"] / gx["mean_padded_tokens"]
        step_s = fs.STEP_S_MAIN * ratio
        res["speed"] = {"fix2": fx, "golden_first_steps": gx, "token_ratio": round(ratio, 4),
                        "step_s_main_measured": fs.STEP_S_MAIN, "step_s_estimate": round(step_s, 3),
                        "cost_at_main_step_time": fs.cost(n_steps), "cost_at_estimated_step_time": fs.cost(n_steps, step_s)}
    # 7. train() itself, stopped at the model load
    import decoder_io
    decoder_io.STYLE = cfg.get("style", "od")
    seen = {}

    def stop_load(base, dev, **kw):
        seen.update({"base": base, "dev": dev, **kw})
        raise StopBeforeModelLoad()

    td.load = stop_load
    try:
        import peft  # noqa: F401
    except ModuleNotFoundError:
        import types

        def _never(*a_, **k_):
            raise RuntimeError("peft stand-in used: the dry run went past the model load")
        sys.modules["peft"] = types.SimpleNamespace(LoraConfig=_never, get_peft_model=_never, PeftModel=_never)
        res["peft_stand_in"] = True
    with tempfile.TemporaryDirectory() as out:
        try:
            td.train(dict(cfg), LEAN / "data", Path(out) / name, dev="cpu")
            raise SystemExit("train() returned without loading a model (unexpected)")
        except StopBeforeModelLoad:
            res["train_reached_model_load"] = {"load_args": seen, "layout": decoder_io.LAYOUT, "style": decoder_io.STYLE}
    print(json.dumps({k: v for k, v in res.items() if k not in ("cfg_sent",)}, indent=1))
    print("DRY RUN OK: config built, data verified, data mount = the 2 fix2 files, init adapter verified, first batch "
          "replayed, train() stopped at the model load")
    if a.out:
        Path(a.out).write_text(json.dumps(res, indent=1) + "\n")


if __name__ == "__main__":
    main()
