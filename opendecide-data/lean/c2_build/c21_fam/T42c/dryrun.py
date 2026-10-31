"""Tiny dry run: builds N (default 20) rows entirely in memory with the SimExecutor and a TEST-ONLY wording pool.

For unit tests only. It never writes rows to disk, never calls the real executor, and never executes generated code.
`python -m T42c.dryrun` prints one line per row (id, head, language, label, planned vs final trace bin).
"""
import random
import sys

from LC_COMMON import sandbox_iface as S
from LC_COMMON import wording

from . import config as C
from .build import build_rows


def dry_rows(n=20, seed=1, executor=None, chunk=10):
    pool = wording.make_test_pool(list(C.QUESTION_FORM.values()), 60)
    picker = wording.Picker(pool, random.Random(seed))
    rows, log, skips = build_rows(n, executor or S.SimExecutor(), picker, seed=seed, chunk=chunk)
    return rows, log, skips, pool


def main(argv=None):
    n = int((argv or sys.argv[1:] or [20])[0])
    rows, log, skips, _ = dry_rows(n)
    for r in rows:
        print(r["row_id"], r["head"], r["lang"], r["label"], r["meta"]["trace_bin_planned"], "->", r["meta"]["trace_bin"], r["meta"]["tokens"])
    print("rows", len(rows), "drops", dict(log.counts), "skips", dict(skips))
    return 0


if __name__ == "__main__":
    sys.exit(main())
