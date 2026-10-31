"""families/T01/haiku_heldout.py: Haiku authoring of DEV-ONLY (held-out) question wordings for the T01 S5 mixdev
(C2_DATA_SPEC 7.1; PREREG A53 follow-up, 16 Oct 2026). T01's wording pool has no held-out wording (0 of 271), and
plugin.pick() defaults to held_out=False, so S5 mixdev rows reuse training wordings (55 of 55 shared ids). This module
writes the authoring tasks for held-out wordings (same prompt, briefs, rules and checks as haiku_author.py), loads their
answers through the family's own check_wording, and writes the G-LEX 2/2 extraction tasks. It does NOT touch the pools,
the plugin or the mixdev: merging admitted wordings (held_out=True) into pools_v2 and rebuilding the mixdev is the
orchestrator's step.

  ids       t01h.wording.<qform>.<000..004>   (5 held-out wordings per question form, 26 forms, 130 items)
  folders   haiku/heldout/ (authoring: tasks/, answers/, chunks/, prompts/, key/, manifest/, plan/, TASKS.json)
            haiku/heldout/extract/ (G-LEX reads glex-r1, glex-r2: tasks/, answers/, ...; TASKS.json)
Run (from lean/):  ../.venv/bin/python c2_build/families/T01/haiku_heldout.py plan | write | admit | glex
A Haiku agent reads ONLY its task file and writes ONLY the answer file it names (TASKS.json lists both for the audit).
"""
from __future__ import annotations

import contextlib
import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
C2_BUILD = HERE.parents[1]
if str(C2_BUILD) not in sys.path:
    sys.path.insert(0, str(C2_BUILD))

from c2_kit import chunker, paths  # noqa: E402
from families.T01 import haiku_author as H  # noqa: E402

FAMILY = "T01"
ROOT = HERE / "haiku" / "heldout"
EXTRACT = ROOT / "extract"
SEED = "t01-heldout-a53-v1"
HELD_N = 5
PREFIX = "t01h"


def held_items():
    """The family's own wording items for indices n .. n+HELD_N-1 of each form (the style and slot-set cycles continue
    past the training items), renamed t01h.wording.<q>.<k>, plan held_out True."""
    base = dict(H.WORDING_N)
    H.WORDING_N = {q: n + HELD_N for q, n in base.items()}
    try:
        items, plan = H._wording_items()
    finally:
        H.WORDING_N = base
    out_i, out_p = [], {}
    for iid, body in items:
        q, i = plan[iid]["qform"], int(iid.rsplit(".", 1)[1])
        if i < base[q]:
            continue
        nid = f"{PREFIX}.wording.{q}.{i - base[q]:03d}"
        out_i.append((nid, body))
        out_p[nid] = {**plan[iid], "held_out": True}
    return out_i, out_p


SPECS = (("wordings", "author_wording", held_items, H.WORDING_PROMPT, H.QSTRINGS, 48),)


@contextlib.contextmanager
def patched():
    old = (H.BATCH_SPECS, H.SEED)
    H.BATCH_SPECS, H.SEED = SPECS, SEED
    try:
        yield
    finally:
        H.BATCH_SPECS, H.SEED = old


def plan_counts() -> dict:
    with patched():
        b, plan = H.build_batches()["wordings"]
    return {"items": len(plan), "chunks": len(b.chunks), "forms": len({p["qform"] for p in plan.values()}),
            "task_ids": [c["task_id"] for c in b.chunks]}


def write() -> list:
    with patched():
        return H.write_tasks(ROOT)


def _training_texts() -> set:
    rows = [json.loads(x) for x in (HERE / "pools_v2" / "wordings.jsonl").read_text().splitlines() if x.strip()]
    return {H._norm(r["text"]) for r in rows}


def admit(root: Path = ROOT) -> dict:
    """Answers -> admitted held-out wordings (family check_wording: G-SL, exact negcount, H38 lists, slot round trip),
    minus any text equal (normalised) to a training wording. Writes root/ADMITTED.json and PROBLEMS.json."""
    with patched():
        out, probs = H.load_wordings(root)
    train = _training_texts()
    ok, dup = [], []
    for q, text, slots, tid, psha in out:
        (dup if H._norm(text) in train else ok).append(
            {"qform": q, "text": text, "slots": slots, "task_id": tid, "prompt_sha": psha, "held_out": True})
    rep = {"asked": HELD_N * len(H.WORDING_N), "accepted": len(ok), "duplicate_of_training": len(dup),
           "problems": len(probs), "by_form": {q: sum(1 for r in ok if r["qform"] == q) for q in H.WORDING_N}}
    paths.write_json(root / "ADMITTED.json", {"admitted": ok, "dropped_duplicates": dup, "report": rep})
    paths.write_json(root / "PROBLEMS.json", probs)
    return rep


def glex(root: Path = ROOT) -> dict:
    """G-LEX extraction reads over the admitted held-out wordings: glex-r1 and glex-r2 (2/2; independent seeds and
    instances). Needs root/ADMITTED.json (run `admit` first). Writes root/extract/."""
    from families.T01 import extract as X
    LX = X.LX
    adm = json.loads((root / "ADMITTED.json").read_text())["admitted"]
    reg = LX.LexiconRegistry(FAMILY)
    for qf, meaning in X.FX.QUESTION_MEANINGS.items():
        reg.declare(LX.question_sem(FAMILY, qf), "question", meaning)
    for r in adm:
        reg.add(r["text"], LX.question_sem(FAMILY, r["qform"]), slots=r["slots"], source="haiku", family=FAMILY,
                haiku_task_id=r["task_id"], haiku_prompt_sha=r["prompt_sha"])
    reg.unit_test_all()
    ok = sorted(fid for fid, f in reg.forms.items() if f.unit_ok)
    batches = []
    for instance, label in enumerate(("glex-r1", "glex-r2")):
        seed = f"t01-heldout-extract-{label}"
        items = X.glex_items(reg, ok, seed, instance)
        batches.append((label, "extract_lex", chunker.make_batch("extract_lex", FAMILY, items, seed=seed,
                                                                 prompt=X.GLEX_PROMPT, max_items=X.LEX_CHUNK)))
    files, manifest = X.files_for(root / "extract", batches)
    paths.write_files(root / "extract", files)
    return {"forms_admitted": len(adm), "forms_unit_ok": len(ok), "tasks": manifest["n_tasks"]}


if __name__ == "__main__":
    cmd = sys.argv[1] if len(sys.argv) > 1 else "plan"
    print(json.dumps({"plan": plan_counts, "write": lambda: {"tasks": len(write())}, "admit": admit,
                      "glex": glex}[cmd](), indent=1))
