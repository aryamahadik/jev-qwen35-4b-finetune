"""Tiny dry run: builds N (default 20) rows entirely in memory with the SimExecutor and a TEST-ONLY wording pool.
For unit tests only: never writes rows to disk, never calls the real executor, never executes generated code."""
import random
import sys

from LC_COMMON import sandbox_iface as S
from LC_COMMON import wording

from . import config as C
from . import rows as ROWS
from .build import build_rows


def dry_pool(n=60):
    return wording.make_test_pool(ROWS.ALL_FORMS, n, {f: s[0] for f, s in ROWS.FORM_SLOTS.items()})


def dry_rows(n=20, seed=1, executor=None):
    pool = dry_pool()
    picker = wording.Picker(pool, random.Random(seed))
    rows, stats, skips = build_rows(n, executor or S.SimExecutor(), picker, seed=seed)
    return rows, stats, skips, pool


def main(argv=None):
    n = int((argv or sys.argv[1:] or [20])[0])
    rows, stats, skips, _ = dry_rows(n)
    for r in rows:
        print(r["row_id"], r["head"], r["lang"], r["label"], r["meta"]["variant"], r["meta"]["tokens"])
    print("rows", len(rows), "drops", dict(stats.drops), "skips", dict(skips))
    return 0


if __name__ == "__main__":
    sys.exit(main())
