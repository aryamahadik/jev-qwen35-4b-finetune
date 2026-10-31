"""STEP 4 (G9 re-read): build the dual blind Haiku task files for every family's g5_reread_<FAM>.json reread_ids
(crowd p_g < 0.05 rows + the seeded 300 sample). Reuses c2_kit.g5h / chunker and the pilot G5-H prompt+contract verbatim.
Outputs under c2_build/crowd_c2/g9_reread/: tasks/<tid>.md, answers/ (empty dir), key/<FAM>.json (orchestrator only: qid->row id,
items as read, reader batch ids). Counts only on stdout. T32 is skipped (A71: T32 out). Usage: make_tasks.py [FAM ...]"""
import sys, json, glob, os, hashlib
from pathlib import Path
HERE = Path(__file__).resolve().parent
CB = HERE.parent.parent
sys.path.insert(0, str(CB))
import c2_select as S
from c2_kit import g5h, chunker
import pilot
OUT = CB / "crowd_c2" / "g9_reread"
SKIP = {"T32": "A71: T32 out (mixer A49c assertion removes it)"}
CHAR_BUDGET = 90000


def main(fams):
    ilog = S.LinkGuardedInputLog()
    for d in ("tasks", "answers", "key"):
        (OUT / d).mkdir(parents=True, exist_ok=True)
    summary, manifest = {}, []
    for fam in fams:
        if fam in SKIP:
            summary[fam] = {"skipped": SKIP[fam]}
            continue
        rows, _, _ = S.family_inputs(ilog, fam)
        by = {r["id"]: r for r in rows}
        g = json.load(open(CB / "crowd_c2" / f"g5_reread_{fam}.json"))
        ids = g["reread_ids"]
        sample, refused = [], []
        for i in ids:
            r = by[i]
            try:
                chunker.check_item("blind_read", g5h.read_item(r))
            except chunker.ChunkError as e:
                refused.append({"row_id": i, "why": str(e)[:160]})
                continue
            sample.append(r)
        mean = sum(len(json.dumps(g5h.read_item(r), ensure_ascii=False)) for r in sample) / max(1, len(sample))
        mx = max(10, min(50, int(CHAR_BUDGET // max(mean, 1))))
        seed = f"{fam}|g9-reread|A68"
        items = [(r["id"], g5h.read_item(r)) for r in sample]
        a = chunker.make_batch("blind_read", fam, items, seed=f"{seed}|reader-A", prompt=pilot.G5H_PROMPT, max_items=mx)
        b = chunker.make_batch("blind_read", fam, items, seed=f"{seed}|reader-B", prompt=pilot.G5H_PROMPT, max_items=mx)
        ntask = 0
        for reader, bt in (("A", a), ("B", b)):
            for n, c in enumerate(bt.chunks):
                chunk_tid = c["task_id"]
                tid = f"{fam}-{reader}{n:02d}"                 # short file id; chunk_task_id keeps the chunker's id for load_answers
                ans = OUT / "answers" / f"{tid}.json"
                tf = OUT / "tasks" / f"{tid}.md"
                text = pilot._task_text("G9 re-read (G5-H blind read)", fam, tid, ans, len(c["items"]), pilot.G5H_PROMPT,
                                        pilot.G5H_CONTRACT, c["items"])
                tf.write_text(text)
                manifest.append({"family": fam, "reader": reader, "task_id": tid, "chunk_task_id": chunk_tid, "task_file": str(tf), "answer_file": str(ans),
                                 "n_items": len(c["items"]), "sha256": hashlib.sha256(text.encode()).hexdigest()})
                ntask += 1
        key = {"family": fam, "gate": "G9-reread", "seed": seed, "n_rows": len(sample), "row_ids": [r["id"] for r in sample],
               "low_ids": g["low_ids"], "sample_ids": g["sample_ids"], "refused_by_chunk_check": refused, "max_items": mx,
               "readers": {"A": pilot._batch_record(a), "B": pilot._batch_record(b)},
               "items": {iid: it for bt in (a, b) for iid, it in chunker.item_by_internal(bt).items()},
               "note": "orchestrator only: never give this file to a Haiku agent"}
        json.dump(key, open(OUT / "key" / f"{fam}.json", "w"), ensure_ascii=False, indent=1)
        summary[fam] = {"rows": len(sample), "refused": len(refused), "max_items": mx, "task_files": ntask}
    json.dump(manifest, open(OUT / "manifest.json", "w"), indent=1)
    print(json.dumps(summary))
    print("task files", len(manifest))


if __name__ == "__main__":
    fams = sys.argv[1:] or sorted(os.path.basename(f)[10:-5] for f in glob.glob(str(CB / "crowd_c2" / "g5_reread_*.json")))
    main(fams)
