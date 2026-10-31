"""decontam_g13_batch.py: several G13 sets in ONE pass over the eval side (RUNBOOK B; spec 7). CPU / local GPU, $0.

Why: a `decontam_g13.py --fam F` run spends almost all its time on the eval side (reading, hashing, MinHashing and
embedding-lookup of ~7M eval items), which is the same for every set. This runs decontam_g13.run_sets once on the
UNION of the sets' training units and splits every hit back to its own set, so N sets cost about one run.

  ../.venv/bin/python c_build/decontam_g13_batch.py --sets F3 F6 F9 [packs formats final_mix_r1]

Output: one logs/decontam_counts/<set>.json per set, the same schema as a lone decontam_g13.py run, plus a "batch"
block. Counts only; no eval text is ever printed or written.

Equivalence (tests/test_decontam_g13_batch.py): for each set the record equals a lone run of that set (except wall
time, unix and the batch block). Exact, segment, table, substring, 10-gram, Tulu 8-gram and MinHash hits are per
training text, so a union index finds the same texts; the embedding top-5 is computed per set (Embed.cols), and the
mixdev sub-index (A25 c), methods 6-8 and the sealed-side child are per set as in a lone run.
"""
from __future__ import annotations

import argparse
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import decontam_g13 as g  # noqa: E402

SETS = g.SETS


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description="G13 counts-only decontamination, several sets in one eval pass")
    ap.add_argument("--sets", nargs="+", required=True, choices=SETS)
    ap.add_argument("--dry", action="store_true", help="build the training side only (no eval file is read)")
    ap.add_argument("--side-serial", action="store_true",
                    help="run the sealed-side child after the open scan, not beside it (one G13 process at a time)")
    a = ap.parse_args(argv)
    sets = {n: g.build_set(n) for n in dict.fromkeys(a.sets)}
    if a.dry:
        for n, (us, ts, ss, _) in sets.items():
            print(f"{n}: train units {sum(not u['seed'] for u in us)} rows {sum(len(u['rows']) for u in us)} "
                  f"seed literals {sum(u['seed'] for u in us)} | train files {len(ts)} seed files {len(ss)}")
        return 0
    recs = g.run_sets(sets, g.targets(), g.OUT, side_parallel=not a.side_serial)
    for n, rec in recs.items():
        print(f"G13 {n}: train units {rec['train_units']} rows {rec['train_rows']} seed literals "
              f"{rec['seed_literals']} | drop units {rec['drop_units']} rows {len(rec['drop_ids'])} | seeds_clean "
              f"{rec['seeds_clean']} | complete {rec['complete']} ({len(rec['incomplete_why'])} reasons)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
