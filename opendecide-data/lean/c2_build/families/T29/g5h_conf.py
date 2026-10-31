"""c2_build/families/T29/g5h_conf.py: the supplementary G5-H read of the decisive-confirmation rows (PILOT_VERDICT FIX-1).

The Stage B G5-H read 100 seeded rows and found exactly one row whose GO AHEAD depends on an explicit confirmation lifting a
needs-confirmation rule (both blind readers took the confirmation phrase for the request itself; 19 of the 1,001 rows were
of that class). FIX-1 adds one sentence to the card and drops three phrasings; its check is: "re-read every
decisive-confirmation row of the re-pilot (about 19) with two blind Haiku readers". The pilot's own G5-H sample
(pilot.g5h_chunks, pinned) is a seeded 100, so it holds only about 7 of them. This module builds the extra read in the
pilot's own layout (task files, key, manifest) under <pilot dir>/g5h_conf/ from the rows the pilot wrote: the rows tagged
prior_confirmation (a confirmation of this call decides a needs-confirmation rule, verdict GO AHEAD). Same prompt, same
contract, same chunker (gold-free items, opaque qids, two independent reads). It answers nothing and runs no model.

  ../.venv/bin/python -B -m families.T29.g5h_conf            (from lean/c2_build; needs pilot_i1/rows.jsonl)
"""
from __future__ import annotations

import hashlib
import sys
from pathlib import Path

sys.dont_write_bytecode = True
C2_BUILD = Path(__file__).resolve().parents[2]
if str(C2_BUILD) not in sys.path:
    sys.path.insert(0, str(C2_BUILD))

import pilot as PI  # noqa: E402
import pilot_loaders as PL  # noqa: E402
from c2_kit import chunker, g5h, paths  # noqa: E402

FAMILY = "T29"
HERE = Path(__file__).resolve().parent
PILOT_DIR = HERE / "pilot_i1"
TAG = "prior_confirmation"


def decisive_rows(rows: list) -> list:
    """The rows whose gold depends on a confirmation of this call (trap tag prior_confirmation), in row order."""
    return [r for r in rows if TAG in (r["meta"].get("edge") or [])]


def build(pdir: Path = PILOT_DIR, write: bool = True) -> dict:
    rows = PL.safe_jsonl(pdir / "rows.jsonl")
    chosen, refused = [], []
    for r in decisive_rows(rows):
        try:
            chunker.check_item("blind_read", g5h.read_item(r))
        except chunker.ChunkError as e:
            refused.append({"row_id": r["id"], "why": str(e)[:200]})
            continue
        chosen.append(r)
    seed = f"{FAMILY}|pilot-g5h-conf|{PI.PILOT_VERSION}"
    a, b = g5h.make_reads(chosen, FAMILY, seed=f"{FAMILY}-pilot-g5h-conf", prompt=PI.G5H_PROMPT)
    files, tasks = {}, []
    out = pdir / "g5h_conf"
    for reader, bt in (("A", a), ("B", b)):
        for c in bt.chunks:
            tid = c["task_id"]
            ans = out / "answers" / f"{tid}.json"
            tf = out / "tasks" / f"{tid}.md"
            text = PI._task_text("G5-H blind read (decisive confirmations)", FAMILY, tid, ans, len(c["items"]),
                                 PI.G5H_PROMPT, PI.G5H_CONTRACT, c["items"])
            files[f"tasks/{tid}.md"] = text
            tasks.append({"gate": "G5-H", "scope": "decisive-confirmation rows (FIX-1)", "reader": reader,
                          "task_id": tid, "task_file": str(tf), "answer_file": str(ans), "n_items": len(c["items"]),
                          "batch_id": bt.batch_id, "task_sha256": hashlib.sha256(text.encode()).hexdigest(),
                          "allowed_read": [str(tf)], "allowed_write": [str(ans)]})
    key = {"family": FAMILY, "gate": "G5-H", "scope": "decisive-confirmation rows (FIX-1)", "n_rows": len(chosen),
           "sample_seed": seed, "row_ids": [r["id"] for r in chosen], "refused_by_chunk_check": refused,
           "readers": {"A": PI._batch_record(a), "B": PI._batch_record(b)},
           "items": {iid: it for bt in (a, b) for iid, it in chunker.item_by_internal(bt).items()},
           "note": "orchestrator only: never give this file to a Haiku agent"}
    manifest = {"family": FAMILY, "gate": "G5-H", "scope": "decisive-confirmation rows (FIX-1)", "tasks": tasks,
                "prompt_sha": chunker.sha(PI.G5H_PROMPT)}
    if write:
        for rel, text in files.items():
            paths.write_text(out / rel, text)
        paths.write_text(out / "answers" / "README.txt",
                         "Haiku G5-H answer files: one <task_id>.json per task file in ../tasks/ (decisive-confirmation "
                         "rows of the re-pilot; FIX-1 check).\n")
        paths.write_json(out / "key.json", key)
        paths.write_json(out / "manifest.json", manifest)
    return {"rows": len(chosen), "tasks": len(tasks), "refused": len(refused),
            "by_qform": {q: sum(1 for r in chosen if r["meta"]["qform"] == q) for q in
                         sorted({r["meta"]["qform"] for r in chosen})}}


if __name__ == "__main__":
    print(build())
