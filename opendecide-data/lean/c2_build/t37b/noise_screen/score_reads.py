"""Replay noise screen (A45 b), step 2: turn the two blind Haiku reads of every replay row into a drop list.

  cd lean/c2_build && ../../.venv/bin/python -B t37b/noise_screen/score_reads.py [--tier 1|2|all]

Reads noise_screen/manifest.json + key.json (make_tasks.py) and the answer files in noise_screen/answers/. Per row:
  clean    both reads equal the human gold
  drop     both reads disagree with the human gold, or one disagrees and the other abstains (invalid / missing answer)
  split    one read agrees, one disagrees: kept in the replay (a single disagreement is not enough to drop)
  abstain  no read disagrees but at least one abstains: kept in the replay
  unread   a task of the row has no answer file yet: kept (never dropped on missing evidence)
A row is never relabelled: the output only lists ids to remove.

Writes (in noise_screen/):
  replay_noise_deny.json     {"drop_ids": [...], ...}: the drop file `mix_c2.py --decontam-drops <file>` consumes (mixer.
                             decontam_drop_ids reads the key 'drop_ids' and mixer.drop_units removes the whole relation unit
                             of each id, so the attacked / neg / def-swap rows of a dropped base leave with it).
                             Copy or point to it as logs/decontam_counts/c2_replay_noise.json for the final mix.
  replay_noise_scores.json   per-source counts and rates, the clean ids (the only rows T37b may use as bases:
                             run_pilot_i2.py --screen) and the drop ids; `sources` carries not_clean / n_read, the
                             rate noise.sources_over_bar tests against the 3% bar (A45 b).
"""
from __future__ import annotations

import argparse
import json
import sys
from collections import Counter
from pathlib import Path

HERE = Path(__file__).resolve().parent
C2 = HERE.parents[1]
if str(C2) not in sys.path:
    sys.path.insert(0, str(C2))

import pilot as PI  # noqa: E402
from c2_kit import chunker, g5h, paths  # noqa: E402
from t37b import noise as NZ  # noqa: E402

YESNO_ITEM = {"kind": "yes/no"}


def load_reads(manifest: dict, key: dict, only_tier: str = "all") -> tuple:
    """({source: {reader: {row id: normalised 1 / 0 / None}}}, problems). A row of a task that has an answer file but no
    (or an invalid) answer for it reads None (abstains); a row of a task with no answer file is absent (unread)."""
    raw = PI._read_answers(manifest["tasks"])
    reads, probs = {}, []
    for s, recs in key["batches"].items():
        for rd in ("A", "B"):
            tids = {t["task_id"] for t in manifest["tasks"] if t["source"] == s and t["reader"] == rd
                    and only_tier in ("all", str(t["tier"]))}
            got_raw = {t: a for t, a in raw.items() if t in tids and a is not None}
            if not got_raw:
                continue
            got, pr = chunker.load_answers(PI._KeyBatch(recs[rd]), got_raw)
            probs += [f"{s}/{rd}: {p}" for p in pr if "unanswered" not in p]
            rd_reads = {i: g5h.normalize_answer(YESNO_ITEM, a) for i, a in got.items()}
            for qid, iid in recs[rd]["key"].items():              # answered task, no answer for this item: abstains
                if recs[rd]["task_of"][qid] in got_raw and iid not in rd_reads:
                    rd_reads[iid] = None
            reads.setdefault(s, {})[rd] = rd_reads
    return reads, probs


def score(manifest: dict, key: dict, only_tier: str = "all") -> dict:
    reads, probs = load_reads(manifest, key, only_tier)
    gold, src_of = key["gold"], key["source_of"]
    per_src, drop_ids, clean_ids, status = {}, [], [], {}
    for rid, s in src_of.items():
        if only_tier != "all" and str(manifest_tier(manifest, s)) != only_tier:
            continue
        ra, rb = reads.get(s, {}).get("A", {}), reads.get(s, {}).get("B", {})
        pair = [ra[rid] if rid in ra else "unread", rb[rid] if rid in rb else "unread"]
        sc = NZ.score_row(gold[rid], pair)
        status[rid] = sc["status"]
        d = per_src.setdefault(s, Counter())
        d[sc["status"]] += 1
        if sc["drop"]:
            drop_ids.append(rid)
        if sc["clean"]:
            clean_ids.append(rid)
    sources = {}
    for s, c in sorted(per_src.items()):
        n_read = sum(v for k, v in c.items() if k != "unread")
        sources[s] = {"n_rows": sum(c.values()), "n_read": n_read, "clean": c["clean"], "drop": c["drop"],
                      "split": c["split"], "abstain": c["abstain"], "unread": c["unread"],
                      "not_clean": n_read - c["clean"],
                      "rate_not_clean": round((n_read - c["clean"]) / n_read, 4) if n_read else None,
                      "rate_drop": round(c["drop"] / n_read, 4) if n_read else None,
                      "refused_by_chunk_check": len(key.get("refused", {}).get(s, []))}
    return {"gate": "A45b-replay-noise", "bar": NZ.BAR, "problems": probs, "sources": sources,
            "sources_over_bar": NZ.sources_over_bar(sources), "n_drop": len(drop_ids), "n_clean": len(clean_ids),
            "drop_ids": sorted(drop_ids), "clean_ids": sorted(clean_ids)}


def manifest_tier(manifest: dict, source: str) -> int:
    return next(t["tier"] for t in manifest["tasks"] if t["source"] == source)


def main(argv=None) -> dict:
    ap = argparse.ArgumentParser()
    ap.add_argument("--tier", default="all", choices=["1", "2", "all"])
    a = ap.parse_args(argv)
    manifest = json.loads((HERE / "manifest.json").read_text(encoding="utf-8"))
    key = json.loads((HERE / "key.json").read_text(encoding="utf-8"))
    res = score(manifest, key, a.tier)
    paths.write_json(HERE / "replay_noise_scores.json", res)
    paths.write_json(HERE / "replay_noise_deny.json", {
        "set": "replay noise screen (Ruling A45 b): human-gold rows both blind Haiku reads dispute",
        "drop_ids": res["drop_ids"], "n": res["n_drop"],
        "rule": "both reads disagree with the human gold, or one disagrees and the other abstains; never relabelled",
        "sources": {s: d["drop"] for s, d in res["sources"].items()},
        "use": "mix_c2.py --decontam-drops <this file> (mixer.decontam_drop_ids, key drop_ids; whole units drop)"})
    print(json.dumps({k: res[k] for k in ("problems", "sources_over_bar", "n_drop", "n_clean")}, indent=1)[:3000])
    for s, d in res["sources"].items():
        print(s, {k: d[k] for k in ("n_read", "clean", "drop", "split", "abstain", "unread", "rate_not_clean")})
    return res


if __name__ == "__main__":
    main()
