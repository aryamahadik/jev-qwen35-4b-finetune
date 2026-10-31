"""Dry run: rows built entirely in memory (SimExecutor/PyEval for the dynamic witnesses, TEST-ONLY wording pool, stamp TEST DOUBLE). Writes nothing."""
import sys

from LP_COMMON import pipeline as pl

from . import checked


def dry_rows(total=60, seed=1, hook=None, **kw):
    return checked.run(total, seed, hook or pl.TestDoubleHook(), standin=True, **kw)


def main(argv=None):
    n = int((argv or sys.argv[1:] or [60])[0])
    rows, summary, log, report = dry_rows(n)
    for r in rows[:40]:
        print(r["row_id"], r["head"], r["sub_block"], r["gold"], r["meta"]["construction_id"], r["meta"]["ladder"], r["meta"]["tokens"])
    print("rows", len(rows), summary)
    return 0


if __name__ == "__main__":
    sys.exit(main())
