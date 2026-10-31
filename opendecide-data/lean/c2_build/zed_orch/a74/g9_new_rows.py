"""A74 G9 read of the rows that entered a family's selection or seeded read set after its G9 read (SB5, MD; any family/block).
Generalises a72/g9_t33_new.py (same readers, prompts, contracts and bars; make_tasks.py / g9_score.py reused unchanged).
Rows to read for FAM = selected rows (select_FAM.json) with NO row in the earlier G9 read (crowd_c2/g9_reread/key/FAM.json row_ids) that are
  (a) not in at least one earlier selection (--prev FAM:<select json> ...; union of the differences, the strictest base), OR
  (b) in the current seeded read set (g5_reread_FAM.json reread_ids) but never read.  (union; stricter than either alone)
Output: crowd_c2/g9_reread_a74/{tasks,answers,key,fam/FAM,manifest.json}. CPU only; counts and ids only on stdout.
  g9_new_rows.py count FAM --prev FAM:P [FAM:P ...]       counts only (no files)
  g9_new_rows.py make FAM [FAM ...] --prev FAM:P ...  build dual blind Haiku task files (reader A, reader B); manifest covers all FAM in one call
  g9_new_rows.py score|adjudicate|confirm-amb|final FAM [--skip ...]   g9_score.py commands with OUT = crowd_c2/g9_reread_a74/
  g9_new_rows.py check
Run from lean/:  ../.venv/bin/python -B c2_build/zed_orch/a74/g9_new_rows.py <cmd> ..."""
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

OUT = CB / "crowd_c2" / "g9_reread_a74"
OLD = CB / "crowd_c2" / "g9_reread"
CHAR_BUDGET = 90000


def to_read(fam, prevs):
    prevs = [p for f, p in prevs if f == fam]
    assert prevs, f"no --prev for {fam}"
    sel = set(json.load(open(CB / "crowd_c2" / f"select_{fam}.json"))["selected_ids"])
    read = set(json.load(open(OLD / "key" / f"{fam}.json"))["row_ids"])
    g = json.load(open(CB / "crowd_c2" / f"g5_reread_{fam}.json"))
    newly = set()   # stricter: new against ANY listed earlier selection (union of the differences)
    for p in prevs:
        newly |= sel - set(json.load(open(p))["selected_ids"])
    in_set_unread = (set(g["reread_ids"]) & sel) - read
    new = sorted((newly | in_set_unread) - read)
    return new, {"selected": len(sel), "earlier_g9_read": len(read), "selected_and_read": len(sel & read), "newly_selected_vs_prev": len(newly),
                 "newly_selected_unread": len(newly - read), "seeded_set_unread": len(in_set_unread), "overlap": len((newly - read) & in_set_unread),
                 "to_read": len(new)}, g


def make(fams, prevs):
    for d in ("tasks", "answers", "key"):
        (OUT / d).mkdir(parents=True, exist_ok=True)
    ilog = S.LinkGuardedInputLog()
    mpath = OUT / "manifest.json"
    manifest = json.load(open(mpath)) if mpath.is_file() else []
    manifest = [m for m in manifest if m["family"] not in fams]
    summary = {}
    for fam in fams:
        new, cnt, g = to_read(fam, prevs)
        rows, _, _ = S.family_inputs(ilog, fam)
        by = {r["id"]: r for r in rows}
        sample, refused = [], []
        for i in new:
            try:
                chunker.check_item("blind_read", g5h.read_item(by[i]))
            except chunker.ChunkError as e:
                refused.append({"row_id": i, "why": str(e)[:160]})
                continue
            sample.append(by[i])
        mean = sum(len(json.dumps(g5h.read_item(r), ensure_ascii=False)) for r in sample) / max(1, len(sample))
        mx = max(10, min(50, int(CHAR_BUDGET // max(mean, 1))))
        seed = f"{fam}|g9-reread|A74-new"
        items = [(r["id"], g5h.read_item(r)) for r in sample]
        a = chunker.make_batch("blind_read", fam, items, seed=f"{seed}|reader-A", prompt=pilot.G5H_PROMPT, max_items=mx)
        b = chunker.make_batch("blind_read", fam, items, seed=f"{seed}|reader-B", prompt=pilot.G5H_PROMPT, max_items=mx)
        for reader, bt in (("A", a), ("B", b)):
            for n, c in enumerate(bt.chunks):
                tid = f"{fam}X-{reader}{n:02d}"
                ans, tf = OUT / "answers" / f"{tid}.json", OUT / "tasks" / f"{tid}.md"
                text = pilot._task_text("G9 re-read (G5-H blind read)", fam, tid, ans, len(c["items"]), pilot.G5H_PROMPT, pilot.G5H_CONTRACT, c["items"])
                tf.write_text(text)
                manifest.append({"family": fam, "reader": reader, "task_id": tid, "chunk_task_id": c["task_id"], "task_file": str(tf),
                                 "answer_file": str(ans), "n_items": len(c["items"]), "sha256": hashlib.sha256(text.encode()).hexdigest()})
        key = {"family": fam, "gate": "G9-reread", "seed": seed, "n_rows": len(sample), "row_ids": [r["id"] for r in sample],
               "low_ids": [i for i in g["low_ids"] if i in set(new)], "sample_ids": [i for i in g["sample_ids"] if i in set(new)],
               "refused_by_chunk_check": refused, "max_items": mx, "counts": cnt,
               "readers": {"A": pilot._batch_record(a), "B": pilot._batch_record(b)},
               "items": {iid: it for bt in (a, b) for iid, it in chunker.item_by_internal(bt).items()},
               "note": "orchestrator only: never give this file to a Haiku agent"}
        json.dump(key, open(OUT / "key" / f"{fam}.json", "w"), ensure_ascii=False, indent=1)
        summary[fam] = {**cnt, "rows_in_tasks": len(sample), "refused": len(refused), "max_items": mx,
                        "task_files": [m["task_file"] for m in manifest if m["family"] == fam]}
    json.dump(manifest, open(mpath, "w"), indent=1)
    print(json.dumps(summary))


def main():
    cmd = sys.argv[1]
    G.OUT = OUT
    if cmd in ("make", "count"):
        args = sys.argv[2:]
        prevs = []
        if "--prev" in args:
            i = args.index("--prev")
            prevs = [(x.split(":", 1)[0], str(Path(x.split(":", 1)[1]).resolve())) for x in args[i + 1:]]   # FAM:path
            args = args[:i]
        if cmd == "count":
            print(json.dumps({f: to_read(f, prevs)[1] for f in args}))
        else:
            make(args, prevs)
        return
    sys.argv = ["g9_score.py", cmd] + sys.argv[2:]
    G.main()


if __name__ == "__main__":
    main()
