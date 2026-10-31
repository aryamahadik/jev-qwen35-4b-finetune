"""A80 (b) G9 read of the rows that entered an ENTERING family's selection or seeded read set after the A80 re-selection (T01 T06 T15 T23 T25 T26 T28 T29 T30 T31;
any family). Multi-family generalisation of a76/g9_t33_a76.py and a74/g9_new_rows.py (same readers, prompts, contracts and bars; make_tasks.py / g9_score.py
reused unchanged). Rows to read for FAM = selected rows (select_FAM.json, the A80 re-selection) not in ANY earlier G9 read set of FAM
(every crowd_c2/g9_reread*/key/FAM.json row_ids except this step's own folder) that are
  (a) not in the earlier selection (--prev FAM:<select json>; the A80 backup crowd_c2 records in c2_build/_backup_a80/), OR
  (b) in the current seeded read set (g5_reread_FAM.json reread_ids) but never read.   (union; the A74 rule, stricter than either alone)
Output: crowd_c2/g9_reread_a80/{tasks,answers,key,fam/FAM,manifest.json}; seed "<FAM>|g9-reread|A80-new". CPU only; counts and ids only on stdout.
  g9_new_rows_a80.py count FAM... --prev FAM:P ...            counts only (no files)
  g9_new_rows_a80.py list FAM... --prev FAM:P ...             writes zed_orch/a80/newly_selected_rows.json (ids; counts on stdout)
  g9_new_rows_a80.py make FAM... --prev FAM:P ...             builds dual blind Haiku task files (reader A, reader B); checks the ids against newly_selected_rows.json
  g9_new_rows_a80.py check | score | adjudicate | confirm-amb | final FAM [--skip ...]   g9_score.py commands with OUT = crowd_c2/g9_reread_a80/
Run from lean/:  ../.venv/bin/python -B c2_build/zed_orch/a80/g9_new_rows_a80.py <cmd> ..."""
import sys, json, hashlib, glob
from pathlib import Path
HERE = Path(__file__).resolve().parent
CB = HERE.parent.parent
sys.path.insert(0, str(CB)); sys.path.insert(0, str(HERE.parent / "g9_reread"))
sys.dont_write_bytecode = True
import c2_select as S
from c2_kit import g5h, chunker
import pilot
import g9_score as G

OUT = CB / "crowd_c2" / "g9_reread_a80"
NEWLY = HERE / "newly_selected_rows.json"
CHAR_BUDGET = 90000


def earlier_read(fam):
    """Union of row_ids of every earlier G9 read set of FAM (all crowd_c2/g9_reread*/key/FAM.json except this step's own folder)."""
    read, srcs = set(), []
    for k in sorted(glob.glob(str(CB / "crowd_c2" / "g9_reread*" / "key" / f"{fam}.json"))):
        if Path(k).resolve().parent.parent == OUT.resolve():
            continue
        ids = set(json.load(open(k))["row_ids"])
        read |= ids
        srcs.append([Path(k).parent.parent.name, len(ids)])
    return read, srcs


def to_read(fam, prevs):
    prevs = [p for f, p in prevs if f == fam]
    assert prevs, f"no --prev for {fam}"
    sel = set(json.load(open(CB / "crowd_c2" / f"select_{fam}.json"))["selected_ids"])
    read, srcs = earlier_read(fam)
    g = json.load(open(CB / "crowd_c2" / f"g5_reread_{fam}.json"))
    newly = set()   # new against ANY listed earlier selection (union of the differences)
    for p in prevs:
        newly |= sel - set(json.load(open(p))["selected_ids"])
    in_set_unread = (set(g["reread_ids"]) & sel) - read
    new = sorted((newly | in_set_unread) - read)
    return new, {"selected": len(sel), "earlier_read_sets": srcs, "earlier_g9_read": len(read), "selected_and_read": len(sel & read),
                 "newly_selected_vs_prev": len(newly), "newly_selected_unread": len(newly - read), "seeded_set_unread": len(in_set_unread),
                 "overlap": len((newly - read) & in_set_unread), "to_read": len(new)}, g


def make(fams, prevs):
    for d in ("tasks", "answers", "key"):
        (OUT / d).mkdir(parents=True, exist_ok=True)
    chk = json.load(open(NEWLY))
    ilog = S.LinkGuardedInputLog()
    mpath = OUT / "manifest.json"
    manifest = json.load(open(mpath)) if mpath.is_file() else []
    manifest = [m for m in manifest if m["family"] not in fams]
    summary = {}
    for fam in fams:
        new, cnt, g = to_read(fam, prevs)
        assert set(new) == set(chk["families"][fam]["ids"]), f"{fam}: ids disagree with newly_selected_rows.json"
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
        seed = f"{fam}|g9-reread|A80-new"
        items = [(r["id"], g5h.read_item(r)) for r in sample]
        a = chunker.make_batch("blind_read", fam, items, seed=f"{seed}|reader-A", prompt=pilot.G5H_PROMPT, max_items=mx)
        b = chunker.make_batch("blind_read", fam, items, seed=f"{seed}|reader-B", prompt=pilot.G5H_PROMPT, max_items=mx)
        for reader, bt in (("A", a), ("B", b)):
            for n, c in enumerate(bt.chunks):
                tid = f"{fam}Y-{reader}{n:02d}"
                ans, tf = OUT / "answers" / f"{tid}.json", OUT / "tasks" / f"{tid}.md"
                text = pilot._task_text("G9 re-read (G5-H blind read)", fam, tid, ans, len(c["items"]), pilot.G5H_PROMPT, pilot.G5H_CONTRACT, c["items"])
                tf.write_text(text)
                manifest.append({"family": fam, "reader": reader, "task_id": tid, "chunk_task_id": c["task_id"], "task_file": str(tf),
                                 "answer_file": str(ans), "n_items": len(c["items"]), "sha256": hashlib.sha256(text.encode()).hexdigest()})
        ns = set(new)
        key = {"family": fam, "gate": "G9-reread", "seed": seed, "n_rows": len(sample), "row_ids": [r["id"] for r in sample],
               "low_ids": [i for i in g["low_ids"] if i in ns], "sample_ids": [i for i in g["sample_ids"] if i in ns],
               "refused_by_chunk_check": refused, "max_items": mx, "counts": cnt,
               "readers": {"A": pilot._batch_record(a), "B": pilot._batch_record(b)},
               "items": {iid: it for bt in (a, b) for iid, it in chunker.item_by_internal(bt).items()},
               "note": "orchestrator only: never give this file to a Haiku agent"}
        json.dump(key, open(OUT / "key" / f"{fam}.json", "w"), ensure_ascii=False, indent=1)
        summary[fam] = {**{k: v for k, v in cnt.items() if k != "earlier_read_sets"}, "rows_in_tasks": len(sample), "refused": len(refused), "max_items": mx,
                        "task_files": [m["task_file"] for m in manifest if m["family"] == fam]}
    json.dump(manifest, open(mpath, "w"), indent=1)
    print(json.dumps(summary))


def main():
    cmd = sys.argv[1]
    G.OUT = OUT
    if cmd in ("make", "count", "list"):
        args = sys.argv[2:]
        prevs = []
        if "--prev" in args:
            i = args.index("--prev")
            prevs = [(x.split(":", 1)[0], str(Path(x.split(":", 1)[1]).resolve())) for x in args[i + 1:]]   # FAM:path
            args = args[:i]
        if cmd == "count":
            print(json.dumps({f: to_read(f, prevs)[1] for f in args}))
        elif cmd == "list":
            out = {"basis": "A80 (b) / A72 step 4 / A74: ids of select_FAM.json (A80 re-selection) not in any earlier G9 read set of FAM (crowd_c2/g9_reread*/key/FAM.json "
                            "row_ids) that are newly selected against the pre-A80 record (_backup_a80) or in the current seeded read set (g5_reread_FAM reread_ids)",
                   "families": {}}
            for f in args:
                new, cnt, _ = to_read(f, prevs)
                out["families"][f] = {"counts": cnt, "ids": new}
            NEWLY.write_text(json.dumps(out, indent=1))
            print(json.dumps({f: v["counts"] for f, v in out["families"].items()}))
        else:
            make(args, prevs)
        return
    sys.argv = ["g9_score.py", cmd] + sys.argv[2:]
    G.main()


if __name__ == "__main__":
    main()
