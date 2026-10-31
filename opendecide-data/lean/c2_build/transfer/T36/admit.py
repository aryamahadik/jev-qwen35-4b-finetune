"""transfer/T36/admit.py: fold the T36 redo answers into the pools (G0_SPEC.md v2.1, sections 6 and 7).

freeze.py rebuilds its records from haiku/author/ and haiku/extract/ only, so the two redo rounds never reached the
pools. This step adds the Mode T pieces that the redo rounds keep, then runs freeze.run unchanged (freeze.py is not
edited):

  round 1  haiku/redo/answers/    one {qid, text} per item: lint_piece (the authoring lint and the H32 slot check)
  round 2  haiku/redo2/answers/   one {qid, texts} per item: the first candidate in written order that passes
                                  lint_piece (the redo2.select rule)

A kept text must differ from every text authored before the redo rounds (normalised), so a re-run gives the same
pools. Mode F candidates from round 2 are NOT admitted here: each needs its G3-H read first (redo2 g3h, then
g3h-check). Answers listed in IGNORED_ANSWERS (failed file-access audit) are dropped; the list is empty for this fold.

  cd lean/c2_build && ../../.venv/bin/python -m transfer.T36.admit            (dry run: counts, writes nothing)
  cd lean/c2_build && ../../.venv/bin/python -m transfer.T36.admit --write    (after A38: writes pools/ and verifies)
"""
from __future__ import annotations

import json
import sys
from collections import Counter
from pathlib import Path

sys.dont_write_bytecode = True
HERE = Path(__file__).resolve().parent
C2_BUILD = HERE.parents[1]
if str(C2_BUILD) not in sys.path:
    sys.path.insert(0, str(C2_BUILD))

from c2_kit import paths  # noqa: E402
from transfer.T36 import freeze as F  # noqa: E402
from transfer.T36 import redo2 as R  # noqa: E402

IGNORED_ANSWERS: frozenset = frozenset()     # answer task names whose file-access audit failed: none (list given as [])
MODE_T = ("skin", "skin_heldout")
MODE_T_AUTHORED = ("skin", "skin_heldout", "attack", "freeform", "freeform_heldout")
POOLS = F.POOLS


def _record(pool: str, piece, tid: str, psha: str) -> dict:
    """A freeze record, the shape extract.collect() gives an authored Mode T skin."""
    return {"pool": pool, "pid": f"{pool}|{R._sha(piece.text)[:16]}", "text": piece.text, "task_id": tid,
            "prompt_sha": psha, "held_out": bool(piece.held_out), "obj": piece}


def _authored_texts(recs: dict) -> set:
    """Normalised texts of everything authored before the redo rounds (the pre-redo pools, idempotent on re-run)."""
    return {R._norm(r["obj"].text) for pool in MODE_T_AUTHORED for r in recs.get(pool, [])}


def redo_pieces(recs: dict) -> tuple:
    """({pool: [record]} kept by the redo rounds, audit). Round 1 first, then round 2, as redo2.load() orders them."""
    seen = _authored_texts(recs)
    src = R._batches()
    keep = {p: [] for p in MODE_T}
    audit = {"round1": Counter(), "round2": Counter(), "ignored_answers": sorted(IGNORED_ANSWERS), "problems": []}

    # round 1: haiku/redo/answers (one text per item; a redo item that passed round 1 is not in this file)
    for t in R._read_json(R.REDO / "REDO_INDEX.json")["tasks"]:
        pool, _b, c = src[t["source_task_id"]]
        if pool not in MODE_T or t["name"] in IGNORED_ANSWERS:
            audit["round1"]["ignored_or_not_mode_t"] += 1
            continue
        f = Path(t["answer_file"])
        if not f.exists():
            audit["problems"].append(f"{t['name']}: no answer file")
            continue
        its = {it["qid"]: it for it in c["items"]}
        for a in R._read_json(f):
            q = a.get("qid")
            if q not in its:
                audit["problems"].append(f"{t['name']}: unknown qid {q!r}")
                continue
            piece, reasons = R.lint_piece(pool, its[q], a.get("text", ""), t["name"], t["redo_instructions_sha256"])
            if reasons:
                audit["round1"]["lint_drop"] += 1
                continue
            if R._norm(piece.text) in seen:
                audit["round1"]["duplicate_drop"] += 1
                continue
            seen.add(R._norm(piece.text))
            keep[pool].append(_record(pool, piece, t["name"], t["redo_instructions_sha256"]))
            audit["round1"]["kept"] += 1

    # round 2: haiku/redo2/answers (Mode T only here; Mode F waits for its G3-H read)
    for t in R.build():
        if t["pool"] not in MODE_T:
            audit["round2"]["mode_f_waiting_for_g3h"] = audit["round2"].get("mode_f_waiting_for_g3h", 0) + len(t["qids"])
            continue
        if t["name"] in IGNORED_ANSWERS:
            audit["round2"]["ignored_answer_items"] = audit["round2"].get("ignored_answer_items", 0) + len(t["qids"])
            continue
        _pool, _b, c = src[t["source_task_id"]]
        its = {it["qid"]: it for it in c["items"]}
        cands, probs = R.read_candidates(t)
        audit["problems"] += probs
        psha = R._sha(t["text"])
        for q in t["qids"]:
            for j, text in enumerate(cands.get(q, [])):
                piece, reasons = R.lint_piece(t["pool"], its[q], text, t["name"], psha)
                if reasons:
                    audit["round2"]["lint_drop"] += 1
                    continue
                if R._norm(piece.text) in seen:
                    audit["round2"]["duplicate_drop"] += 1
                    continue
                seen.add(R._norm(piece.text))
                keep[t["pool"]].append(_record(t["pool"], piece, t["name"], psha))
                audit["round2"]["kept"] += 1
                break
    return keep, {k: (dict(v) if isinstance(v, Counter) else v) for k, v in audit.items()}


def _j(obj) -> str:
    return json.dumps(obj, ensure_ascii=False, indent=1, sort_keys=True, default=str) + "\n"


def run(write: bool) -> dict:
    """freeze.run with the redo pieces added to the records it rebuilds; the MANIFEST gets an admit block."""
    orig_rebuild = F.rebuild
    state = {}

    def rebuild_with_redo() -> dict:
        st = orig_rebuild()
        keep, audit = redo_pieces(st["recs"])
        for pool, objs in keep.items():
            st["recs"].setdefault(pool, []).extend(objs)
        state.update(keep=keep, audit=audit)
        return st

    F.rebuild = rebuild_with_redo
    try:
        out = F.run(write)
    finally:
        F.rebuild = orig_rebuild

    keep, audit = state["keep"], state["audit"]
    out["admit"] = {"kept_by_pool": {p: len(v) for p, v in keep.items()}, "audit": audit}
    if write:
        man_path = POOLS / "MANIFEST.json"
        man = json.loads(man_path.read_text(encoding="utf-8"))
        man["admit"] = {
            "step": "transfer/T36/admit.py (new; freeze.py unchanged)",
            "sources": ["haiku/redo/answers (round 1, Mode T)", "haiku/redo2/answers (round 2, Mode T)"],
            "kept_by_pool": {p: len(v) for p, v in keep.items()},
            "audit": audit,
            "ignored_answers": sorted(IGNORED_ANSWERS),
            "mode_f": "round 2 Mode F candidates are lint-clean but not admitted: each needs its G3-H read "
                      "(redo2 g3h --write, the read, then redo2 g3h-check) before a document can be frozen",
            "superseded": "freeze.py pending_gates item 3 (the G3-H ruling) is superseded by ruling v2.1 "
                          "(G0_SPEC.md section 7); the open step is the redo2 G3-H read",
        }
        paths.write_files(POOLS, {"MANIFEST.json": _j(man)})
        out["verify"] = F.verify_pools()
    out["written"] = write
    return out


def main(argv: list) -> int:
    res = run("--write" in argv)
    print(json.dumps(res, indent=1, ensure_ascii=False, sort_keys=True, default=str))
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
