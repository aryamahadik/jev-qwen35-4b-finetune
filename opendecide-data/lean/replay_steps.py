"""CPU replay of train_decoder's data stream (no model, no GPU): how many batches one real pass takes, and the `epochs`
value that makes a run exactly that pass (FINETUNE_PLAN.md section 2.2, key `epochs`).

  ../.venv/bin/python replay_steps.py --config runs/q35_4b_main.json
  ../.venv/bin/python replay_steps.py --config runs/q35_4b_main.json --last-batch-at 100,150,300

The random calls are exactly those of train_decoder.train(): random.seed(seed); batches() shuffles the units on the
global stream when the first batch is drawn; each step then draws one permutation per row (random.sample), and
pick_twins draws from its own random.Random(seed + 1). batches() drops the leftover units (fewer than `batch` rows) at
the end of a pass, so a pass is every batch drawn before the first one that repeats a unit.
--last-batch-at K prints the hash of the batch at step K-1: what a checkpoint's state.pt holds as "last_batch" when it
stopped at step K (compare with a real run's checkpoint).
"""
from __future__ import annotations

import argparse
import json
import math
import random
import sys
import time
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import train_decoder as td  # noqa: E402

# train()'s own defaults for the keys the data stream depends on; style: the launchers' default (decoder_io.STYLE)
STREAM_DEFAULTS = {"recipe": "A3", "batch": 16, "seed": 20260925, "epochs": 1.0, "perm_twin": 0.0, "style": "od",
                   "train_file": "train.jsonl", "rel_file": "train_relations.jsonl"}


def stream_cfg(cfg: dict) -> dict:
    return {**STREAM_DEFAULTS, **{k: v for k, v in cfg.items() if k in STREAM_DEFAULTS}}


def load_data(c: dict, data_dir: Path):
    """(rows_all, rows, rels, units, inv_merged), built exactly as train() builds them."""
    rows_all = td.read_jsonl(Path(data_dir) / c["train_file"])
    rels_all = td.read_jsonl(Path(data_dir) / c["rel_file"])
    rows = [r for r in rows_all if c["recipe"] != "A0" or r["track"] == "L0"]
    ids = {r["id"] for r in rows}
    rels = [x for x in rels_all if c["recipe"] != "A0" and x["a"] in ids and x["b"] in ids]
    units, merged = td.make_units(rows, rels)
    return rows_all, rows, rels, units, merged


def unit_ids(units) -> dict:
    """Row id -> unit index, as train() builds `uid` (before the first shuffle)."""
    return {r["id"]: k for k, u in enumerate(units) for r in u}


def stream(units, c: dict):
    """Yields (step, batch, perms, twins) in train()'s order. Reseeds the global `random` (as train() does); `units` is
    copied, so the caller's list keeps make_units order and the stream can be replayed again."""
    random.seed(c["seed"])
    twin_rng = random.Random(c["seed"] + 1)
    cyg = c["style"] == "cygnet"
    gen = td.batches(list(units), c["batch"])
    step = 0
    while True:
        batch = next(gen)
        perms = [random.sample(range(len(r["options"])), len(r["options"])) if r["qtype"] == "choice"
                 else (random.sample([0, 1], 2) if cyg else None) for r in batch]
        tw = td.pick_twins(batch, perms, c["perm_twin"], twin_rng)
        yield step, batch, perms, tw
        step += 1


def first_pass(units, c: dict, on_step=None, limit: int = 0) -> dict:
    """Replays the first pass (or its first `limit` batches). on_step(step, batch, perms, twins) sees every batch of it."""
    uid = unit_ids(units)
    seen, n, rows = set(), 0, 0
    for step, batch, perms, tw in stream(units, c):
        us = {uid[r["id"]] for r in batch}
        if us & seen:  # the pass is over: batches() reshuffled
            break
        seen |= us
        n, rows = n + 1, rows + len(batch)
        if on_step is not None:
            on_step(step, batch, perms, tw)
        if limit and n >= limit:
            break
    left = [u for k, u in enumerate(units) if k not in seen]
    return {"batches": n, "rows": rows, "mean_rows_per_batch": rows / max(1, n), "complete": not (limit and n >= limit),
            "dropped_units": len(left), "dropped_rows": sum(map(len, left))}


def n_steps(n_rows_all: int, batch: int, epochs: float) -> int:
    """train()'s step count, the same float expression."""
    return math.ceil(n_rows_all / batch * epochs)


def epochs_for(n_batches: int, n_rows_all: int, batch: int) -> float:
    """The `epochs` giving exactly n_batches steps: n_batches / (rows / batch), moved down one float at a time if
    rounding would make ceil() add a step."""
    e = n_batches / (n_rows_all / batch)
    while n_steps(n_rows_all, batch, e) > n_batches:
        e = math.nextafter(e, 0.0)
    if n_steps(n_rows_all, batch, e) != n_batches:
        raise AssertionError(f"no epochs value gives {n_batches} steps for {n_rows_all} rows / batch {batch}")
    return e


def last_batch_hashes(units, c: dict, at) -> dict:
    """{K: hash of the batch at step K-1} (a checkpoint saved at next_step K stores it as last_batch)."""
    want, out = set(int(k) for k in at), {}
    if not want:
        return out
    for step, batch, _, _ in stream(units, c):
        if step + 1 in want:
            out[step + 1] = td._batch_hash(batch)
        if step + 1 >= max(want):
            return out


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--config", default="runs/q35_4b_main.json", help="run config (relative to this folder); '' = none")
    ap.add_argument("--data-dir", default=str(HERE / "data"))
    ap.add_argument("--train-file")
    ap.add_argument("--rel-file")
    ap.add_argument("--seed", type=int)
    ap.add_argument("--batch", type=int)
    ap.add_argument("--style")
    ap.add_argument("--perm-twin", type=float)
    ap.add_argument("--last-batch-at", default="", help="comma list of K: hash of the batch at step K-1")
    ap.add_argument("--out", default="", help="also write the summary JSON here")
    a = ap.parse_args(argv)
    cfg = json.loads((HERE / a.config).read_text()) if a.config else {}
    for k, v in (("train_file", a.train_file), ("rel_file", a.rel_file), ("seed", a.seed), ("batch", a.batch),
                 ("style", a.style), ("perm_twin", a.perm_twin)):
        if v is not None:
            cfg[k] = v
    c = stream_cfg(cfg)
    t0 = time.time()
    rows_all, rows, rels, units, merged = load_data(c, Path(a.data_dir))
    t_load = time.time() - t0
    p = first_pass(units, c)
    n = p["batches"]
    e = epochs_for(n, len(rows_all), c["batch"])
    out = {"train_file": c["train_file"], "rel_file": c["rel_file"], "seed": c["seed"], "batch": c["batch"],
           "style": c["style"], "perm_twin": c["perm_twin"], "rows": len(rows_all), "rows_used": len(rows),
           "relations": len(rels), "units": len(units), "inv_merged": merged,
           "pass_batches": n, "pass_rows": p["rows"], "mean_rows_per_batch": round(p["mean_rows_per_batch"], 4),
           "dropped_units": p["dropped_units"], "dropped_rows": p["dropped_rows"],
           "epochs": e, "epochs_check": f"ceil({len(rows_all)}/{c['batch']}*{e!r}) = {n_steps(len(rows_all), c['batch'], e)}",
           "warmup_steps": int(0.05 * n), "ramp_full_from_step": math.ceil(0.2 * n)}
    if "epochs" in cfg:
        k = n_steps(len(rows_all), c["batch"], cfg["epochs"])
        out.update({"config_epochs": cfg["epochs"], "config_n_steps": k, "config_is_one_pass": k == n})
    if a.last_batch_at:
        out["last_batch"] = {str(k): h for k, h in
                             last_batch_hashes(units, c, [int(x) for x in a.last_batch_at.split(",")]).items()}
    out["seconds"] = {"load": round(t_load, 1), "total": round(time.time() - t0, 1)}
    print(json.dumps(out, indent=1))
    if a.out:
        Path(a.out).write_text(json.dumps(out, indent=1) + "\n")
    return out


if __name__ == "__main__":
    main()
