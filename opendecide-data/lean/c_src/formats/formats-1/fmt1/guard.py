"""Mixer guard (program form): refuse TRAINING rows that use a held-out format style or the held-out S5 sampler.

    python -m fmt1.guard rows.jsonl [more.jsonl ...] [--strict-unknown]      (run from the formats-1 folder)

Prints counts only (never row text). Exit 0 = clean, 1 = refused rows, 2 = usage or read error. The mixer runs this (or
calls fmt1.pool.refuse_held_out) on every training shard before a freeze; dev and mix-tuning shards are not passed.
"""
from __future__ import annotations

import json
import sys

from . import pool


def _rows(paths):
    for p in paths:
        with open(p, encoding="utf-8") as f:
            for line in f:
                if line.strip():
                    yield json.loads(line)


def main(argv=None) -> int:
    args = list(sys.argv[1:] if argv is None else argv)
    strict = "--strict-unknown" in args
    paths = [a for a in args if not a.startswith("--")]
    if not paths:
        print(__doc__)
        return 2
    try:
        out = pool.refuse_held_out(_rows(paths), strict_unknown=strict)
    except pool.HeldOutStyleError as e:
        print(json.dumps({"verdict": "refused", "detail": str(e).split("; first ids")[0]}))
        return 1
    except (OSError, ValueError) as e:
        print(json.dumps({"verdict": "error", "detail": type(e).__name__}))
        return 2
    print(json.dumps({"verdict": "pass", **out}))
    return 0


if __name__ == "__main__":
    sys.exit(main())
