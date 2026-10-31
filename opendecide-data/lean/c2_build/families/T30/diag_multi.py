"""families/T30/diag_multi.py: several independent pilot-size builds, one line per gate (in memory; no file written).

  cd lean/c2_build && ../../.venv/bin/python -B families/T30/diag_multi.py 6000000 5 1000
"""
import sys
from pathlib import Path

sys.dont_write_bytecode = True
C2 = Path(__file__).resolve().parents[2]
if str(C2) not in sys.path:
    sys.path.insert(0, str(C2))
import pilot as PI  # noqa: E402
import pilot_loaders as PL  # noqa: E402


def main(base: int, reps: int, n: int) -> None:
    with PL.open_family("T30") as kit:
        for i in range(reps):
            sb = base + i * 100_000
            b = PI.build_pilot(kit, n, seed_base=sb, run_g15=False, log=None)
            g6 = PI.g6(b.infos)
            g7 = PI.g7(b.infos)
            g10 = PI.g10(b.infos, b.units, kit.plugin)
            ov = PI.overlay(b.units, kit.plugin)
            sp = PI.spec30(b.infos, kit.plugin)
            ch = g6["choice"]
            yn = g6["yes_no"]
            print(f"seed_base {sb}: rows {b.stats['rows_written']} drops {b.stats['drops_by_gate']} | "
                  f"G6 {g6['verdict']} fails {[(f['part'][:2], f['view'][:2], f['model'], f['acc'], f['chance']) for f in g6['fails']]} | "
                  f"G7 {g7['verdict']} ch {g7['n_choice_fails']} yn {g7['n_yes_no_raw_fails']}/{g7['n_yes_no_card_adjusted_fails']} | "
                  f"G10 {g10['verdict']} {g10['failing']} | overlay {ov['verdict']} {ov['failing']} "
                  f"tw {ov['checks']['twin_share']['value']} eq {ov['checks']['equiv_share']['value']} | "
                  f"tok {sp['checks']['mean_tokens']['value']} max {sp['checks']['max_tokens']['value']}", flush=True)
            print("    choice", {v: ch[v] for v in ("a_question", "b_options", "c_card_without_question", "d_meta")},
                  "chance", ch["chance"], flush=True)
            print("    yes/no", {v: yn[v] for v in ("a_question", "c_card_without_question", "d_meta")}, flush=True)


if __name__ == "__main__":
    main(int(sys.argv[1]), int(sys.argv[2]), int(sys.argv[3]))
