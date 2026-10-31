"""families/T33/dneg_stage2.py: stage 2 of the double-negation wordings (fix iteration 2; G0_SPEC section 9 G2).

Input : the Haiku authoring answers of haiku/dneg_i2/tasks/ (written by `python -m families.T33.dneg_i2 write-tasks`).
Does  : admits every candidate wording through the family's own authoring checks (haiku_author.load_pieces): one
        question, the {STEP} slot once (yn_dneg_step_ok) or no slot, <= 25 words, the word bans, the form's must-have
        words (explicit outer frame; `not` on meeting the criterion / before every or all), the negation count (2, 2),
        the polarity rules of c2_kit.polarity (P1 negation over a negative predicate, P2 parity, P3 contracted frame,
        P4 strict frame), the lexicon unit test and G-SL. A candidate that fails is dropped with its reason. Then it
        writes the G-LEX task files, two independent reads (each read its own chunk files), under
        haiku/dneg_i2/glex_tasks/, and haiku/dneg_i2/stage2_report.json.
Output: the orchestrator runs one fresh Haiku agent per G-LEX task file, then `dneg_stage3`.
No Haiku, no model, no network.

  ../../.venv/bin/python -B -m families.T33.dneg_stage2 [--root <haiku/dneg_i2>]      (from lean/c2_build)

Exit code: 0 when every form has >= 8 candidates left for G-LEX, 1 otherwise (the report says which form is short:
re-author it; the target of 8 admitted wordings per form is never lowered).
"""
from __future__ import annotations

import argparse
import json
import sys
from collections import Counter
from pathlib import Path

sys.dont_write_bytecode = True
C2_BUILD = Path(__file__).resolve().parents[2]
if str(C2_BUILD) not in sys.path:
    sys.path.insert(0, str(C2_BUILD))

from c2_kit import paths  # noqa: E402
from families.T33 import dneg_i2 as D  # noqa: E402
from families.T33 import haiku_author as H  # noqa: E402


def candidates(pieces: dict) -> dict:
    """{qform: [wording skins that passed the checks]}"""
    out = {q: [] for q in D.FORMS}
    for s in pieces["skins"].values():
        if s.kind == "wording" and s.qform in out:
            out[s.qform].append(s)
    return out


def run(root: Path = D.ROOT) -> dict:
    root = Path(root)
    tasks_root, glex_root = root / "tasks", root / "glex_tasks"
    pieces = H.load_pieces(tasks_root)
    reg = pieces["registry"]
    cand = candidates(pieces)
    reasons = Counter({k: v for k, v in pieces["drops"].items()})
    batches = H.extraction_batches(reg, glex_root)
    files = {}
    for _n, b in batches:
        files.update(b.files())
    tasks = [{"task_file": str(glex_root / b.chunk_path(c["task_id"])), "answer_file": c["answer_file"],
              "kind": f"extract_lex:{n}"} for n, b in batches for c in b.chunks]
    files["TASKS.json"] = json.dumps({"family": H.F, "version": D.VERSION, "n_tasks": len(tasks), "tasks": tasks,
                                      "batches": {n: b.batch_id for n, b in batches},
                                      "reads_per_form": len(batches)}, indent=1) + "\n"
    if batches:
        paths.write_files(glex_root, files)
        for t in tasks:                                      # the answer folder exists before the reads run
            Path(t["answer_file"]).parent.mkdir(parents=True, exist_ok=True)
    short = {q: len(v) for q, v in cand.items() if len(v) < D.MIN_ADMITTED}
    report = {"family": H.F, "stage": 2, "candidates_per_form": {q: len(v) for q, v in cand.items()},
              "short_forms": short, "min_per_form": D.MIN_ADMITTED, "drops": dict(reasons),
              "problems": pieces["problems"][:60], "n_glex_tasks": len(tasks), "glex_tasks": tasks,
              "dropped_examples": [p for p in pieces["problems"] if p.startswith("drop")][:30],
              "next": ("one fresh Haiku agent per glex task file (read only its task_file, write only its answer_file), "
                       "then: python -B -m families.T33.dneg_stage3")}
    root.mkdir(parents=True, exist_ok=True)
    paths.write_text(root / "stage2_report.json", json.dumps(report, indent=1) + "\n")
    return report


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--root", default=str(D.ROOT))
    a = ap.parse_args(argv)
    rep = run(Path(a.root))
    print(json.dumps({k: rep[k] for k in ("candidates_per_form", "short_forms", "drops", "n_glex_tasks")}, indent=1))
    return 1 if rep["short_forms"] or not rep["n_glex_tasks"] else 0


if __name__ == "__main__":
    raise SystemExit(main())
