"""GPU runner: read a rows file in BOTH displayed orders with decoder_io.predict and write the two prediction files.

NOT run on the Mac and NOT run by L-E (queue: od-l4b, priority 3, orchestrator only). It only wraps decoder_io, so the
prompt, the option letters and the one-token readout are exactly the product's.

  python -m c21_eval.run_readout --model <path-or-id> [--adapter A] --rows rows_x.jsonl --views views_x.json \
      --run c2_1_when2call --out preds_dir

Writes <out>/<run>.fwd.jsonl and <out>/<run>.rev.jsonl ({"id","model","probs"} with probs keyed by the ORIGINAL option text)
plus <out>/<run>.meta.json (model, rows sha, views sha, decoder_io load info). Score with the harness `score` command.
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from . import common as C


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument("--model", required=True)
    ap.add_argument("--adapter")
    ap.add_argument("--rows", required=True)
    ap.add_argument("--views", required=True)
    ap.add_argument("--run", required=True)
    ap.add_argument("--out", required=True)
    ap.add_argument("--batch-size", type=int, default=8)
    ap.add_argument("--token-budget", type=int, default=12000)
    a = ap.parse_args(argv)
    sys.path.insert(0, str(C.LEAN))
    import decoder_io as D  # lean/decoder_io.py (torch; GPU host only)

    rows = C.read_jsonl(a.rows)
    views = json.load(open(a.views))
    if set(views) != {r["id"] for r in rows}:
        raise SystemExit("views do not cover exactly the rows")
    model, tok, info = D.load(a.model, adapter=a.adapter, return_info=True)
    dev = next(model.parameters()).device
    out = Path(a.out)
    for order in ("fwd", "rev"):
        perms = [views[r["id"]][order] for r in rows]
        preds = D.predict(model, tok, rows, batch_size=a.batch_size, dev=str(dev), perms=perms, token_budget=a.token_budget)
        out.mkdir(parents=True, exist_ok=True)
        with open(out / f"{a.run}.{order}.jsonl", "w", encoding="utf-8") as f:
            for r, p in zip(rows, preds):
                f.write(json.dumps({"id": r["id"], "model": a.run, "probs": p}) + "\n")
    C.write_json(out / f"{a.run}.meta.json", {"model": a.model, "adapter": a.adapter, "rows_sha256": C.sha256_file(a.rows),
                                              "views_sha256": C.sha256_file(a.views), "load_info": str(info), "orders": ["fwd", "rev"]})


if __name__ == "__main__":
    main()
