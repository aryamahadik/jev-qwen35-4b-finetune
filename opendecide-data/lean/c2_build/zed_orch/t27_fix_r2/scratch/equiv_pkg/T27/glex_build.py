"""families/T27/glex_build.py: the G-LEX extraction tasks for T27's kept lexicon forms (G0_SPEC.md section 6,
"Admission"; c2_build/README.md "Haiku task flow" steps 1-3; A37 b). Code only until A38, then it writes chunk files.

Every kept lexicon form (request, mention, task form, question wording) that passes its unit test needs 2/2 independent
extractions to be admitted (lexicon.LexiconRegistry.required). T27 has no "precedence" or "window" kind, so the 3/3 rule
never applies here. Each independent read uses its own seeds: its own opaque qids, its own groups (chunk files) and its
own order of the meaning list, so a form's two reads never share a chunk file, a qid or a list order.

  python -m families.T27.glex_build plan     # in memory: forms, unit tests, groups, counts; writes nothing
  python -m families.T27.glex_build write    # after A38: write the chunk files, prompts, key and manifest, then TASKS.json

Cost choice (the user asked to save the limit): the kit's default extract_lex item carries its kind's full meaning list
in every item. For 'deontic' that is 69 meanings per item, about 1.5M input tokens across both reads. Here each group
of up to 50 forms is one chunk whose items carry only the rendered 'text'; the group's closed meaning list (the same
meanings, in a group-specific seeded order) sits in the group's prompt. The admission rule is unchanged: a Haiku pick
must be one of the list's meanings, any other pick rejects the form (lexicon.record_extraction), and no pick sets a label.
Items are the rendered forms from authoring.lex_items (the family's ITEM and SOURCE stand-in values).
"""
from __future__ import annotations

import argparse
import hashlib
import json
import sys
from collections import Counter
from pathlib import Path

HERE = Path(__file__).resolve().parent
_C2 = HERE.parents[1]
if str(_C2) not in sys.path:
    sys.path.insert(0, str(_C2))

from c2_kit import chunker, paths  # noqa: E402

from . import authoring as A  # noqa: E402
from . import vocab as V  # noqa: E402

FAMILY = V.FAMILY
EXTRACT = HERE / "haiku" / "extract"
READS = ("read1", "read2")                        # 2/2 admission (G0 section 6); no 3/3 kind in T27
KIND_ORDER = ("deontic", "other", "question")     # lexicon kinds present in T27
GROUP = 50                                        # forms per chunk (chunker maximum)
PROMPT_HEAD = (
    "You name the meaning of short English text lines. Read your task file (one JSON file). It holds a list of items. "
    "Each item has an opaque 'qid' and a 'text' (one line). The closed list of meanings for this task file is given "
    "below, in its order. For every item, read the text and pick the ONE meaning in the list that the text expresses. "
    "Copy that meaning exactly as written, character for character. Judge each text on its own words, not on the other "
    "items or on the order of the list. "
    "Write ONE JSON object to the answer file that your instructions name: its keys are the qid values of ALL items in "
    "your task file, and each value is the copied meaning (a string). Valid JSON only: double quotes, no comments, no "
    "trailing commas. Do not open any other file."
)


def group_seed(read: str, kind: str, g: int) -> str:
    return f"{FAMILY}-glex-{read}-{kind}-{g:02d}"


def group_prompt(meanings: list) -> str:
    return PROMPT_HEAD + "\n\nCLOSED LIST (one meaning per line):\n" + "\n".join(f"- {m}" for m in meanings) + "\n"


def _admissible(kept: dict) -> tuple:
    """(registry, admissible form ids, dropped [{form, why}]) for the kept lexicon pools of authoring.load()."""
    reg = A.registry(kept)
    ok, dropped = [], []
    for fid in sorted(reg.forms):
        f = reg.forms[fid]
        if f.unit_ok:
            ok.append(fid)
        else:
            dropped.append({"form": fid, "why": ["unit test: " + "; ".join(f.unit_problems[:2])]})
    return reg, ok, dropped


def plan(root: Path = A.ROOT) -> dict:
    """Every batch the write step writes, computed in memory: nothing is written."""
    rep = A.load(root)
    reg, ok, dropped = _admissible(rep["kept"])
    batches = []                                  # [(read, kind, group index, batch)]
    for read in READS:
        for kind in KIND_ORDER:
            fids = [f for f in ok if reg.forms[f].kind == kind]
            meanings = sorted((s.meaning for s in reg.sems.values() if s.kind == kind))
            for g in range(0, len(fids), GROUP):
                part = fids[g:g + GROUP]
                seed = group_seed(read, kind, g // GROUP)
                order = sorted(meanings, key=lambda m: hashlib.sha256(f"{seed}|{m}".encode()).hexdigest())
                items = [(fid, {"text": it["text"]}) for fid, it in A.lex_items(reg, part, seed=seed)]
                b = chunker.make_batch("extract_lex", FAMILY, items, seed=seed, prompt=group_prompt(order),
                                       max_items=GROUP)
                if len(b.chunks) != 1:
                    raise chunker.ChunkError(f"{seed}: one chunk per group")
                batches.append((read, kind, g // GROUP, b))
    return {"rep": rep, "reg": reg, "ok": ok, "dropped_unit": dropped, "batches": batches}


def summary(p: dict) -> dict:
    per_read = Counter()
    for read, _kind, _g, b in p["batches"]:
        per_read[read] += sum(len(c["items"]) for c in b.chunks)
    by_kind = Counter(p["reg"].forms[f].kind for f in p["ok"])
    sizes = [len(json.dumps(c, ensure_ascii=False)) + len(b.prompt) for _r, _k, _g, b in p["batches"]
             for c in b.chunks]
    return {
        "lexicon_forms_kept": len(p["reg"].forms),
        "forms_unit_ok": len(p["ok"]),
        "forms_unit_failed": len(p["dropped_unit"]),
        "forms_needing_admission_by_kind": dict(by_kind),
        "extractions_required_per_form": 2,
        "item_reads_per_read": dict(per_read),
        "item_reads_total": sum(per_read.values()),
        "chunk_files": sum(len(b.chunks) for _r, _k, _g, b in p["batches"]),
        "chunks_by_read_kind": dict(Counter(f"{r}/{k}" for r, k, _g, _b in p["batches"])),
        "max_chunk_bytes_with_prompt": max(sizes),
        "lint_counts": p["rep"]["counts"],
        "lint_shortfall": p["rep"]["shortfall"],
    }


def write(root: Path = EXTRACT) -> list:
    """After A38 only (paths.write_files refuses before). Writes every chunk, prompt, key and manifest, then TASKS.json
    (orchestrator side). Refuses when TASKS.json already exists (the tasks are written once)."""
    root = Path(root)
    if (root / "TASKS.json").exists():
        raise FileExistsError(f"{root}/TASKS.json exists: the G-LEX extraction tasks are written once")
    p = plan()
    tasks, forms = [], {}
    for read, kind, g, b in p["batches"]:
        paths.write_files(root, b.files())
        tid = b.chunks[0]["task_id"]
        tasks.append({"read": read, "kind": kind, "group": g, "batch_id": b.batch_id, "task_id": tid,
                      "task_file": str(root / b.chunk_path(tid)), "answer_file": str(root / b.answer_path(tid)),
                      "n_items": len(b.chunks[0]["items"]), "prompt_sha": b.prompt_sha})
        for qid, fid in b.key.items():
            forms.setdefault(fid, {"sem_id": p["reg"].forms[fid].sem_id, "kind": kind})
    paths.write_json(root / "TASKS.json", {"family": FAMILY, "gate": "G-LEX 2/2", "reads": list(READS),
                                           "summary": summary(p), "tasks": tasks, "forms": forms,
                                           "dropped_unit": p["dropped_unit"]})
    return tasks


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(prog="families.T27.glex_build")
    ap.add_argument("cmd", choices=("plan", "write"))
    ap.add_argument("--root", default=str(EXTRACT))
    a = ap.parse_args(argv)
    if a.cmd == "plan":
        print(json.dumps(summary(plan()), indent=1))
    else:
        tasks = write(Path(a.root))
        print(json.dumps([{"task_file": t["task_file"], "answer_file": t["answer_file"], "kind": "extract_lex",
                           "read": t["read"], "n_items": t["n_items"]} for t in tasks], indent=1))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
