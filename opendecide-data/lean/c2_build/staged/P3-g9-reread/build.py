"""P3-g9-reread build: dual blind Haiku read task files for every candidate row with C1 crowd p_g < 0.05 (G9 / g5_reread low set).
Read-only on data/; writes only under staged/P3-g9-reread/. Run from lean/c2_build: ../../.venv/bin/python -B staged/P3-g9-reread/build.py"""
import sys, json, hashlib
from pathlib import Path
sys.dont_write_bytecode = True
HERE = Path(__file__).resolve().parent
CB = HERE.parents[1]
sys.path.insert(0, str(CB))
import c2_select as S, crowd_select as cs, pilot as PI
from c2_kit import chunker, g5h

FAMS = ["T28", "T26", "T29", "T33", "T30", "T31", "T32", "T01", "T23", "T24", "T06", "T15", "T12", "T07", "T25"]
GROUPS = {"T28": ["T28"], "T26": ["T26"], "T29": ["T29"], "T33": ["T33"], "T30": ["T30"],
          "TOTH": [f for f in FAMS if f not in ("T28", "T26", "T29", "T33", "T30")]}
ilog = S.LinkGuardedInputLog()
low_rows, shas, nlow = {}, {}, {}
for fam in FAMS:
    rows, rels, sh = S.family_inputs(ilog, fam)
    sd = S.SHARDS / fam
    pg, view = S.load_c1(ilog, rows, sd / f"labels_{S.C1}", sd)
    lows = sorted((r for r in rows if pg[r["id"]] < cs.G5_PG), key=lambda r: r["id"])
    low_rows[fam] = lows
    shas[fam] = sh["candidates_sha256"]
    nlow[fam] = len(lows)
assert sum(nlow.values()) == 695, nlow
tasks, key = [], {"purpose": "P3 early G9 re-read", "rule": "crowd p_g < 0.05, all candidates (crowd_select.g5_reread low set)",
                  "candidates_sha256": shas, "n_low": nlow, "groups": {}, "note": "orchestrator only: never give to a Haiku agent"}
for gname, fams in GROUPS.items():
    chosen, refused = [], []
    for f in fams:
        for r in low_rows[f]:
            try:
                chunker.check_item("blind_read", g5h.read_item(r))
                chosen.append(r)
            except chunker.ChunkError as e:
                refused.append({"row_id": r["id"], "family": f, "why": str(e)[:160]})
    a, b = g5h.make_reads(chosen, gname, seed=f"P3-g9-{gname}", prompt=PI.G5H_PROMPT)
    rec = {"families": fams, "n_rows": len(chosen), "row_ids": [r["id"] for r in chosen], "refused": refused,
           "readers": {"A": PI._batch_record(a), "B": PI._batch_record(b)},
           "items": {iid: it for bt in (a, b) for iid, it in chunker.item_by_internal(bt).items()}}
    key["groups"][gname] = rec
    for reader, bt in (("A", a), ("B", b)):
        for c in bt.chunks:
            tid = c["task_id"]
            tf = HERE / "tasks" / reader / f"{tid}.md"
            af = HERE / "answers" / reader / f"{tid}.json"
            text = PI._task_text("G9 early re-read, blind read", gname, tid, af, len(c["items"]), PI.G5H_PROMPT,
                                 PI.G5H_CONTRACT, c["items"])
            tf.parent.mkdir(parents=True, exist_ok=True); af.parent.mkdir(parents=True, exist_ok=True)
            tf.write_text(text, encoding="utf-8")
            tasks.append({"reader": reader, "group": gname, "task_id": tid, "task_file": str(tf), "answer_file": str(af),
                          "n_items": len(c["items"]), "sha256": hashlib.sha256(text.encode()).hexdigest()})
(HERE / "key.json").write_text(json.dumps(key, ensure_ascii=False, indent=1))
(HERE / "manifest.json").write_text(json.dumps({"tasks": tasks, "prompt_sha": chunker.sha(PI.G5H_PROMPT)}, indent=1))
print({g: (v["n_rows"], len(v["refused"])) for g, v in key["groups"].items()}, len(tasks))
