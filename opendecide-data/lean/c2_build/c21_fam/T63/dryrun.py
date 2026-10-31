"""Dry run: rows built entirely in memory with FIXTURE sources (a seeded stand-in export and licence table, flagged `fixture`), a TEST-ONLY wording
pool and the stamp TEST DOUBLE. For unit tests and a smoke run only; it never writes rows, never calls a model and never executes anything.
`python -m T63.dryrun N` prints one line per row."""
import sys

from LP_COMMON import pipeline as pl
from LP_COMMON import util
from LP_COMMON.ns import Names

from . import checked, exists, lic


def fixture_exports(seed="fx"):
    nm = Names("T63fx", seed)
    out = {}
    k = 0
    for lang, n_mod in (("python", 14), ("node", 8), ("go", 8)):
        mods = {}
        for i in range(n_mod):
            mname = nm.get("ns.noun.module", "%s-m%d" % (lang, i))
            size = 12 + (i * 7) % 50
            names = set()
            j = 0
            while len(names) < size:
                j += 1
                k += 1
                s = nm.get("ns.noun.symbol", "s%d" % k)
                s = s.capitalize() if lang == "go" else s
                names.add(s)
            mods[mname] = sorted(names)
        out[lang] = mods
    data = {"fixture": True, "image_id": "fixture-image", "export_runs": 3, "exports": out}
    return exists.ExportSet(data)


def dry_rows(total=60, seed=1, hook=None, **kw):
    ex, tb = fixture_exports(), lic.fixture_table()
    hook = hook or pl.TestDoubleHook()
    return checked.run(total, seed, hook, standin=True, exports=ex, table=tb, **kw)


def main(argv=None):
    n = int((argv or sys.argv[1:] or [60])[0])
    rows, summary, log, report = dry_rows(n)
    for r in rows:
        print(r["row_id"], r["sub_block"], r["gold"], r["meta"]["ladder"], r["meta"]["construction_id"], r["meta"]["tokens"])
    print("rows", len(rows), summary)
    return 0


if __name__ == "__main__":
    sys.exit(main())
