"""Replay noise screen (A45 b), step 1: Haiku blind-read task files for every replay row of the T37b sources.

  cd lean/c2_build && nice -n 10 ../../.venv/bin/python -B t37b/noise_screen/make_tasks.py [--count-only] [--tier 1|2|all]

Replay rows: the golden_train pool (lean/data/v14_parts/golden_train.jsonl) IS the replay pool (replay_sample.load_rows
reads exactly that file). A row of a screened source is read when it is C1's own hard yes/no question: qtype "noul",
role "aff", no attack_target. Attacked copies, "neg" rows and def-swaps are the same human label in a derived row; they
sit in the aff row's relation unit, so dropping the aff id drops the whole unit (mixer.drop_units), and they are not
read again. Sources: every source of the T37b registry (sources.SOURCES) + gd_ghc_hate (hate speech, not a T37b source:
vote-share rows, screened as the same hate-speech risk). Tier 1 = the three sources behind the pilot_i1_full failure
(hate speech: gd_hatemoji_build_v14, gd_ghc_hate; table fact: gd_semtabfacts_sci); tier 2 = the other T37b sources.

Gold-free items (g5h.read_item: text, question, definitions), opaque qids, <= 50 items per task, two independent reads
(reader A and B: own seeds, orders, qids and chunk splits), the same prompt and answer contract as the G5-H tasks.
Writes (all under noise_screen/):
  tasks/<task_id>.md       one per chunk (Haiku reads only this file and writes only answers/<task_id>.json)
  manifest.json            every task: source, tier, reader, task file, answer file, n_items, sha256
  key.json                 ORCHESTRATOR ONLY: qid -> row id per batch, plus gold and source per row (never in a task)
"""
from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
from collections import Counter
from pathlib import Path

HERE = Path(__file__).resolve().parent
C2 = HERE.parents[1]
if str(C2) not in sys.path:
    sys.path.insert(0, str(C2))

import pilot as PI  # noqa: E402
from c2_kit import chunker, g5h, paths  # noqa: E402
from t37b import sources as SRC  # noqa: E402

GOLDEN = paths.LEAN / "data" / "v14_parts" / "golden_train.jsonl"
POOL_DROPS = paths.LEAN / "logs" / "decontam_counts" / "pool_drops_r1.json"      # always a G13 drop list (mix_c2)
HATE_EXTRA = ("gd_ghc_hate",)
TIER1 = ("gd_hatemoji_build_v14", "gd_ghc_hate", "gd_semtabfacts_sci")
SOURCES = tuple(sorted(set(SRC.SOURCES) | set(HATE_EXTRA)))
SRC_RE = re.compile(r'"source": "([^"]+)"')
SEED = "replay-noise-screen-a45"


def tier_of(source: str) -> int:
    return 1 if source in TIER1 else 2


def load_pool_rows(sources=SOURCES) -> dict:
    """{source: [row, ...]} of the screened replay rows, in file order."""
    want = set(sources)
    drops = set(json.loads(paths.check_path(POOL_DROPS).read_text(encoding="utf-8"))["drop_ids"])
    out = {s: [] for s in sources}
    with open(paths.check_path(GOLDEN), encoding="utf-8") as f:
        for line in f:
            m = SRC_RE.search(line)
            if not m or m.group(1) not in want or '"qtype": "noul"' not in line:
                continue
            r = json.loads(line)
            mt = r.get("meta") or {}
            if r["id"] in drops:                                  # never replayed (G13): not read
                continue
            if r.get("role") != "aff" or r.get("qtype") != "noul" or mt.get("attack_target") or r.get("gold") not in (0, 1):
                continue
            out[r["source"]].append(r)
    return out


def main(argv=None) -> dict:
    ap = argparse.ArgumentParser()
    ap.add_argument("--count-only", action="store_true")
    ap.add_argument("--tier", default="all", choices=["1", "2", "all"])
    a = ap.parse_args(argv)
    pool = load_pool_rows()
    counts, manifest_tasks, key = {}, [], {"family": "replay-noise-screen", "gate": "A45b", "batches": {}, "gold": {},
                                           "source_of": {}, "refused": {},
                                           "note": "orchestrator only: never give this file to a Haiku agent"}
    for s, rows in pool.items():
        if a.tier != "all" and str(tier_of(s)) != a.tier:
            continue
        counts[s] = {"tier": tier_of(s), "rows": len(rows), "tasks_per_reader": -(-len(rows) // chunker.MAX_ITEMS)}
        if a.count_only:
            continue
        ok, refused = [], []
        for r in rows:
            try:
                chunker.check_item("blind_read", g5h.read_item(r))
                ok.append(r)
            except chunker.ChunkError as e:
                refused.append({"row_id": r["id"], "why": str(e)[:160]})
        key["refused"][s] = refused
        counts[s]["refused_by_chunk_check"] = len(refused)
        key["gold"].update({r["id"]: r["gold"] for r in ok})
        key["source_of"].update({r["id"]: s for r in ok})
        ba, bb = g5h.make_reads(ok, "NS-" + s.replace("gd_", ""), seed=f"{SEED}|{s}", prompt=PI.G5H_PROMPT)
        key["batches"][s] = {"A": PI._batch_record(ba), "B": PI._batch_record(bb)}
        for reader, bt in (("A", ba), ("B", bb)):
            for c in bt.chunks:
                tid = c["task_id"]
                tf, af = HERE / "tasks" / f"{tid}.md", HERE / "answers" / f"{tid}.json"
                text = PI._task_text("Replay noise screen blind read", bt.family, tid, af, len(c["items"]),
                                     PI.G5H_PROMPT, PI.G5H_CONTRACT, c["items"])
                paths.write_text(tf, text)
                manifest_tasks.append({"gate": "A45b-replay-noise", "source": s, "tier": tier_of(s), "reader": reader,
                                       "task_id": tid, "task_file": str(tf), "answer_file": str(af),
                                       "n_items": len(c["items"]), "batch_id": bt.batch_id,
                                       "task_sha256": hashlib.sha256(text.encode()).hexdigest(),
                                       "allowed_read": [str(tf)], "allowed_write": [str(af)]})
        counts[s]["rows_read"] = len(ok)
    tot_rows = sum(c["rows"] for c in counts.values())
    summary = {"sources": counts, "rows": tot_rows,
               "reads": 2 * tot_rows, "tasks": sum(2 * c["tasks_per_reader"] for c in counts.values()),
               "tier1_rows": sum(c["rows"] for c in counts.values() if c["tier"] == 1),
               "tier1_reads": 2 * sum(c["rows"] for c in counts.values() if c["tier"] == 1),
               "tier2_rows": sum(c["rows"] for c in counts.values() if c["tier"] == 2),
               "tier2_reads": 2 * sum(c["rows"] for c in counts.values() if c["tier"] == 2)}
    if not a.count_only:
        paths.write_text(HERE / "answers" / "README.txt", "Haiku answer files: one <task_id>.json per task in ../tasks/.\n")
        paths.write_json(HERE / "manifest.json", {"gate": "A45b-replay-noise", "prompt_sha": chunker.sha(PI.G5H_PROMPT),
                                                   "summary": summary, "tasks": manifest_tasks})
        paths.write_json(HERE / "key.json", key)
    print(json.dumps(summary, indent=1))
    return summary


if __name__ == "__main__":
    main()
