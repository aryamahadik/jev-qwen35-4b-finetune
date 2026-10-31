"""A72 step 4 G9 read of the rows NEWLY selected for T33 after its A72 re-selection (rows not in the earlier 144-row G9 read set, key/T33.json).
Same readers, prompts, contracts and bars as make_tasks.py / g9_score.py (both reused unchanged); output goes to its own folder
crowd_c2/g9_reread_a72/ so the earlier T33 reads are untouched. CPU only; counts and ids only on stdout.
  g9_t33_new.py make                      build dual blind Haiku task files (reader A, reader B) for the newly selected rows
  g9_t33_new.py score|adjudicate|confirm-amb|final T33 [--skip ...]   g9_score.py commands with OUT = crowd_c2/g9_reread_a72/
  g9_t33_new.py check                     task sha / answer presence
Run from lean/:  ../.venv/bin/python -B c2_build/zed_orch/a72/g9_t33_new.py <cmd>"""
import sys, json, hashlib
from pathlib import Path
HERE = Path(__file__).resolve().parent
CB = HERE.parent.parent
sys.path.insert(0, str(CB)); sys.path.insert(0, str(HERE.parent / "g9_reread"))
sys.dont_write_bytecode = True
import c2_select as S
from c2_kit import g5h, chunker
import pilot
import g9_score as G

OUT = CB / "crowd_c2" / "g9_reread_a72"
OLD = CB / "crowd_c2" / "g9_reread"
FAM = "T33"
CHAR_BUDGET = 90000


def make():
    for d in ("tasks", "answers", "key"):
        (OUT / d).mkdir(parents=True, exist_ok=True)
    sel = json.load(open(CB / "crowd_c2" / "select_T33.json"))["selected_ids"]
    old = set(json.load(open(OLD / "key" / "T33.json"))["row_ids"])
    new = sorted(set(sel) - old)
    chk = set(json.load(open(HERE / "newly_selected_rows.json"))["T33"]["newly_selected_ids"])
    assert set(new) == chk, "newly selected ids disagree with newly_selected_rows.json"
    g = json.load(open(CB / "crowd_c2" / "g5_reread_T33.json"))
    rows, _, _ = S.family_inputs(S.LinkGuardedInputLog(), FAM)
    by = {r["id"]: r for r in rows}
    sample, refused = [], []
    for i in new:
        try:
            chunker.check_item("blind_read", g5h.read_item(by[i]))
        except chunker.ChunkError as e:
            refused.append({"row_id": i, "why": str(e)[:160]})
            continue
        sample.append(by[i])
    seed = "T33|g9-reread|A72-new"
    items = [(r["id"], g5h.read_item(r)) for r in sample]
    a = chunker.make_batch("blind_read", FAM, items, seed=f"{seed}|reader-A", prompt=pilot.G5H_PROMPT, max_items=50)
    b = chunker.make_batch("blind_read", FAM, items, seed=f"{seed}|reader-B", prompt=pilot.G5H_PROMPT, max_items=50)
    manifest = []
    for reader, bt in (("A", a), ("B", b)):
        for n, c in enumerate(bt.chunks):
            tid = f"{FAM}N-{reader}{n:02d}"
            ans, tf = OUT / "answers" / f"{tid}.json", OUT / "tasks" / f"{tid}.md"
            text = pilot._task_text("G9 re-read (G5-H blind read)", FAM, tid, ans, len(c["items"]), pilot.G5H_PROMPT, pilot.G5H_CONTRACT, c["items"])
            tf.write_text(text)
            manifest.append({"family": FAM, "reader": reader, "task_id": tid, "chunk_task_id": c["task_id"], "task_file": str(tf),
                             "answer_file": str(ans), "n_items": len(c["items"]), "sha256": hashlib.sha256(text.encode()).hexdigest()})
    key = {"family": FAM, "gate": "G9-reread", "seed": seed, "n_rows": len(sample), "row_ids": [r["id"] for r in sample],
           "low_ids": [i for i in g["low_ids"] if i in new], "sample_ids": [i for i in g["sample_ids"] if i in new],
           "refused_by_chunk_check": refused, "max_items": 50,
           "readers": {"A": pilot._batch_record(a), "B": pilot._batch_record(b)},
           "items": {iid: it for bt in (a, b) for iid, it in chunker.item_by_internal(bt).items()},
           "note": "orchestrator only: never give this file to a Haiku agent"}
    json.dump(key, open(OUT / "key" / "T33.json", "w"), ensure_ascii=False, indent=1)
    json.dump(manifest, open(OUT / "manifest.json", "w"), indent=1)
    print(json.dumps({"selected": len(sel), "already_read": len(set(sel) & old), "new": len(new), "rows_in_tasks": len(sample), "refused": len(refused),
                      "task_files": [m["task_file"] for m in manifest]}))


def main():
    cmd = sys.argv[1]
    G.OUT = OUT
    if cmd == "make":
        make()
        return
    rest = sys.argv[2:]
    sys.argv = ["g9_score.py", cmd] + rest
    G.main()


if __name__ == "__main__":
    main()
