"""c2_build/families/T29/g6_pool.py: the pilot's G6 on K pilot-size builds pooled (about the 5,000-row QC sample of the full
generation, spec 6.3), in memory, nothing written. A view's accuracy over ~5,000 rows has a standard error of about 0.7 pp
(yes/no) so a real leak of 2 pp shows; the pilot's own 500-row numbers scatter by +- 3 pp.

  ../.venv/bin/python -B -m families.T29.g6_pool [--k 6] [--first 20]      (from lean/c2_build; about 12 minutes)
"""
from __future__ import annotations

import argparse
import sys
from pathlib import Path

sys.dont_write_bytecode = True
C2_BUILD = Path(__file__).resolve().parents[2]
if str(C2_BUILD) not in sys.path:
    sys.path.insert(0, str(C2_BUILD))

import pilot as PI  # noqa: E402
import pilot_loaders as PL  # noqa: E402


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument("--k", type=int, default=6)
    ap.add_argument("--first", type=int, default=20)
    a = ap.parse_args(argv)
    infos = []
    with PL.open_family("T29") as kit:
        for j in range(a.first, a.first + a.k):
            b = PI.build_pilot(kit, 1000, seed_base=900_000 + j * 3_200_000, run_g15=False)
            infos += b.infos
            print(f"build {j}: {len(b.infos)} rows", flush=True)
    g = PI.g6(infos)
    for part in ("yes_no", "choice"):
        p = g[part]
        print(f"{part}: n {p['n']} chance {p['chance']}")
        for v in ("a_question", "b_options", "c_card_without_question", "d_meta"):
            if v in p:
                print(f"  {v:24s} lr {p[v]['lr']:.4f} ({100 * (p[v]['lr'] - p['chance']):+.2f} pp)  gbt {p[v]['gbt']:.4f} "
                      f"({100 * (p[v]['gbt'] - p['chance']):+.2f} pp)")
        if p.get("d_meta_drivers"):
            print("  drivers", p["d_meta_drivers"])
    print("fails:", [(f['part'], f['view'], f['model'], round(100 * (f['acc'] - f['chance']), 2)) for f in g["fails"]])


if __name__ == "__main__":
    main()
