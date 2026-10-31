"""transfer/T19/redo2_merge.py: stage the read-free redo2 pieces as a freeze CANDIDATE, and run the redo2 read path.

The redo2 packs, skins and attack lines are admitted by their loaders' own checks (redo2.lint_candidate), with no
Haiku read needed. Wordings (G-LEX 2/2) and Mode F documents (G3-H) need their reads first (redo2.py extract, then
extract-check), so they are NOT merged here.

freeze.py and redo2.py are not edited. This wrapper:
  - patches only the in-memory freeze.rebuild() so freeze.run counts and writes the merged lint;
  - writes the candidate to haiku/redo2/merge_candidate/ (never to pools/);
  - keeps pools/ at the ROUND 1 freeze. redo2.py's shortfall guard (redo_plan) and its seen-text checks read
    pools/, and the family's own test suite asserts the round 1 shortfalls, so a live merged freeze would break
    the read path before the reads exist. The round 1 freeze is backed up in haiku/redo2/pools_round1/, which is
    the baseline the read path runs against (RD.POOLS below).

Targets come from freeze.TARGETS and are never lowered. Promotion of the candidate to pools/ is the final freeze,
after the redo2 reads are merged too (not built yet).

  cd lean && ../.venv/bin/python c2_build/transfer/T19/redo2_merge.py                  (dry run: counts, writes nothing)
  cd lean && ../.venv/bin/python c2_build/transfer/T19/redo2_merge.py --write          (writes the candidate and verifies it)
  cd lean && ../.venv/bin/python c2_build/transfer/T19/redo2_merge.py tasks|load|extract [--write]|extract-check
      (the redo2 read path, run against the round 1 baseline)
"""
from __future__ import annotations

import hashlib
import json
import sys
from pathlib import Path

sys.dont_write_bytecode = True
HERE = Path(__file__).resolve().parent
C2_BUILD = HERE.parents[1]
if str(C2_BUILD) not in sys.path:
    sys.path.insert(0, str(C2_BUILD))

from c2_kit import paths  # noqa: E402
from transfer.T19 import freeze as FZ  # noqa: E402
from transfer.T19 import plugin as P  # noqa: E402
from transfer.T19 import redo2 as RD  # noqa: E402

READ_FREE = ("packs", "skins", "attacks")
BASELINE = HERE / "haiku" / "redo2" / "pools_round1"      # the round 1 freeze, backed up before any merge
CANDIDATE = HERE / "haiku" / "redo2" / "merge_candidate"  # the merged freeze, staged (not promoted)
REDO_CMDS = ("tasks", "write", "load", "extract", "extract-check")


def _sha(s: str) -> str:
    return hashlib.sha256(s.encode("utf-8")).hexdigest()


def read_free_pieces(loaded: dict) -> tuple:
    """({pool: [piece]}, [record]) for every item whose first lint-clean candidate is kept without a read."""
    pieces = {p: [] for p in READ_FREE}
    records = []
    for row in loaded["selection"]["items"]:
        if row["pool"] not in READ_FREE or row["kept"] is None:
            continue
        cand = next(c for c in row["candidates"] if c["j"] == row["kept"] and c["ok"])
        obj = cand["obj"]
        pieces[row["pool"]].append(obj)
        pid = obj["pack_id"] if row["pool"] == "packs" else obj.skin_id
        records.append({"pool": row["pool"], "piece_id": pid, "cell": row["cell"], "qid": row["qid"],
                        "task": row["task"], "candidate": row["kept"]})
    return pieces, records


def merge_into(res: dict, pieces: dict) -> dict:
    """Add the pieces to freeze's lint dict (packs: list of dicts; skins and attacks: dicts by skin_id)."""
    lint = res["lint"]
    have_packs = {p["pack_id"] for p in lint["packs"]}
    for pk in pieces["packs"]:
        if pk["pack_id"] in have_packs:
            raise SystemExit(f"pack id collides with a frozen pack: {pk['pack_id']}")
        lint["packs"].append(pk)
    for pool in ("skins", "attacks"):
        for sk in pieces[pool]:
            if sk.skin_id in lint[pool] or sk.skin_id in lint["free"]:
                raise SystemExit(f"skin id collides with a frozen piece: {sk.skin_id}")
            lint[pool][sk.skin_id] = sk
    return {p: len(pieces[p]) for p in READ_FREE}


def _ignored_audit_answers() -> list:
    """Answers whose file-access audit failed. No audit record exists on disk for the redo2 agents (their transcripts
    are outside this run's allowed paths), so the list is the harness's value, recorded as given."""
    return []


def _redo2_record(loaded: dict, records: list, merged: dict) -> dict:
    answers = {}
    for t in loaded["tasks"]:
        f = Path(t["answer_file"])
        probs = [p for p in loaded["selection"]["problems"] if t["name"] in p]
        answers[t["name"]] = {"sha256": _sha(f.read_text(encoding="utf-8")) if f.exists() else None,
                              "answer_problems": probs, "structurally_valid": not probs}
    waiting = [r for r in loaded["selection"]["items"] if r["pool"] in ("freeform", "wordings") and r["kept"] is None]
    by_cell: dict = {}
    for r in waiting:
        by_cell[r["cell"]] = by_cell.get(r["cell"], 0) + 1
    return {
        "version": RD.VERSION,
        "status": "CANDIDATE: staged in haiku/redo2/merge_candidate/, not promoted to pools/. pools/ stays at the "
                  "round 1 freeze until the redo2 reads are merged (redo2.py guards read pools/MANIFEST.json).",
        "g0_sha256": P.T19Plugin.G0_SHA256_AUTHORED,
        "g0_sha256_expected": json.loads((RD.ROOT / "REDO2_INDEX.json").read_text(encoding="utf-8"))["g0_sha256"],
        "answers": answers,
        "ignored_answers_audit_failed": _ignored_audit_answers(),
        "merged_without_read": {"pieces": merged, "records": records},
        "awaiting_read": {"items": len(waiting), "by_cell": dict(sorted(by_cell.items())),
                          "reads": ["G-LEX 2/2 on each lint-clean wording candidate (redo2.py extract, then "
                                    "extract-check)", "G3-H 1 read on each lint-clean Mode F candidate"]},
        "pending": ["file-access audit of the 7 redo2 authoring transcripts (c2_kit/audit.py): no record on disk",
                    "redo2 read answers (extract) and extract-check",
                    "merge of kept redo2 wordings and Mode F documents (needs the reads first)",
                    "promotion of this candidate to pools/ (final freeze, after the reads)",
                    "G13-seed decontamination on every pool before any row"],
    }


def run(write: bool) -> dict:
    RD.POOLS = BASELINE                            # the read path reads the round 1 freeze, never the candidate
    loaded = RD.load()
    pieces, records = read_free_pieces(loaded)
    merged_counts: dict = {}
    orig_rebuild, orig_pools = FZ.rebuild, FZ.POOLS

    def rebuild_with_redo2() -> dict:
        res = orig_rebuild()                       # round 1 batches, drift-checked exactly as freeze.py does
        merged_counts.update(merge_into(res, pieces))
        return res

    FZ.rebuild = rebuild_with_redo2
    if write:
        FZ.POOLS = CANDIDATE
    try:
        out = FZ.run(write)
    finally:
        FZ.rebuild, FZ.POOLS = orig_rebuild, orig_pools
    record = _redo2_record(loaded, records, merged_counts)
    out["redo2"] = {"merged_without_read": merged_counts, "awaiting_read": record["awaiting_read"],
                    "answers": {k: {"structurally_valid": v["structurally_valid"]}
                                for k, v in record["answers"].items()}}
    if write:
        man = json.loads((CANDIDATE / "MANIFEST.json").read_text(encoding="utf-8"))
        man["redo2"] = record
        paths.write_files(CANDIDATE, {"MANIFEST.json": json.dumps(man, ensure_ascii=False, indent=1,
                                                                  sort_keys=True, default=str) + "\n"})
        out["verify"] = FZ.verify_pools(CANDIDATE)
        out["written"] = str(CANDIDATE)
    return out


def main(argv: list) -> int:
    if argv and argv[0] in REDO_CMDS:              # the redo2 read path, against the round 1 baseline
        RD.POOLS = BASELINE
        return RD.main(argv)
    res = run("--write" in argv)
    print(json.dumps(res, indent=1, ensure_ascii=False, sort_keys=True, default=str))
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
