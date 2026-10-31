"""c2_build/families/T29/g6_probe.py: how often the pilot's G6 views exceed the bar over several pilot-size builds.

The G6 bars are chance + 2 pp on about 500 yes/no and 450 choice rows, where one view's accuracy has a standard error of
about 2 pp, so one pilot says little about a real leak. This builds K pilots (different seed bases, the pilot's own
build_pilot and g6, in memory, nothing written) and prints each view's accuracy minus chance: a real leak shows the same
sign every time (mean > 0), noise averages to about zero with a spread near 2 pp.

  ../.venv/bin/python -B -m families.T29.g6_probe [--k 4] [--first 3]      (from lean/c2_build; about 3 minutes per build)
"""
from __future__ import annotations

import argparse
import statistics as st
import sys
from collections import defaultdict
from pathlib import Path

sys.dont_write_bytecode = True
C2_BUILD = Path(__file__).resolve().parents[2]
if str(C2_BUILD) not in sys.path:
    sys.path.insert(0, str(C2_BUILD))

import pilot as PI  # noqa: E402
import pilot_loaders as PL  # noqa: E402


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument("--k", type=int, default=4)
    ap.add_argument("--first", type=int, default=3)
    a = ap.parse_args(argv)
    acc = defaultdict(list)
    with PL.open_family("T29") as kit:
        for j in range(a.first, a.first + a.k):
            b = PI.build_pilot(kit, 1000, seed_base=900_000 + j * 3_200_000, run_g15=False)
            g = PI.g6(b.infos)
            line = []
            for part in ("yes_no", "choice"):
                p = g[part]
                for v in ("a_question", "b_options", "c_card_without_question", "d_meta"):
                    if v not in p:
                        continue
                    for m in ("lr", "gbt"):
                        d = 100 * (p[v][m] - p["chance"])
                        acc[(part, v, m)].append(d)
                        line.append(f"{part[:2]}:{v[:1]}:{m}={d:+.1f}")
            print(f"build {j} (n {g['yes_no']['n']} + {g['choice']['n']}): " + " ".join(line), flush=True)
    print("mean (sd) of accuracy - chance, pp:")
    for k, v in acc.items():
        print(f"  {k[0]:6s} {k[1]:24s} {k[2]:3s} {st.mean(v):+.2f} ({st.pstdev(v):.2f})")


if __name__ == "__main__":
    main()
