"""families/T26/haiku/redo3/build_reads.py: load the redo3 answers and issue the G-LEX reads of the NEW redo3 wordings.

Inputs (read only): haiku/redo3/answers/ (4 G-LEX reads of the redo2 wordings, 2 top-up authoring answers) and the whole
T26 state that freeze_v2.build() rebuilds in memory.

What a run does (A38 only; every write goes through the kit's guarded writers; nothing outside haiku/redo3/reads/ is written):
  1. Validates EVERY redo3 answer file against its task contract (freeze_v2.validate_round: file level rejects the whole file,
     item level rejects one item). The answers are never edited; a rejected answer counts as unanswered, never as a vote.
  2. Rebuilds the T26 state with the redo3 G-LEX reads as the redo2 reads (freeze_v2.build(raw_override=...), in memory), so the
     registry knows which redo2 wordings are now admitted / rejected / still pending.
  3. Ingests the NEW authored wordings (the 4 training yn_fails and the 15 held-out wordings): the unchanged wording lint
     (authoring_ingest.lint_wording), dedup against every registry form (first pass, redo2, any status), every fixture
     stand-in and each other, then registry add (held_out=True for pool wording_heldout) and unit test.
  4. Writes the G-LEX reads of the survivors: TWO independent reads (question wordings need 2/2), each its own self-contained
     task file for its own fresh agent (own seed, qids, item order and choice order), the unchanged LEX_PROMPT and meaning
     choices (decoys included). Answer paths: haiku/redo3/reads/answers/<task id>.json. No label and no read is invented here.

  ../.venv/bin/python families/T26/haiku/redo3/build_reads.py --dry-run   (from lean/c2_build; build and check, write nothing)
  ../.venv/bin/python families/T26/haiku/redo3/build_reads.py             (write haiku/redo3/reads/)
  ../.venv/bin/python families/T26/haiku/redo3/build_reads.py --check     (files on disk == the rebuild)
"""
from __future__ import annotations

import argparse
import hashlib
import importlib.util
import json
import sys
from collections import Counter, defaultdict
from pathlib import Path

sys.dont_write_bytecode = True
HERE = Path(__file__).resolve().parent                 # .../families/T26/haiku/redo3
C2_BUILD = HERE.parents[3]                              # .../lean/c2_build
if str(C2_BUILD) not in sys.path:
    sys.path.insert(0, str(C2_BUILD))

from c2_kit import chunker, paths  # noqa: E402
from c2_kit.paths import never_open  # noqa: E402
from families.T26 import authoring_ingest as AI  # noqa: E402
from families.T26 import freeze_v2 as FV  # noqa: E402
from families.T26 import plugin as P  # noqa: E402

VERSION = "redo3-reads-v1"
READS = HERE / "reads"
ANSWERS = HERE / "answers"
READ_ANSWERS = READS / "answers"
LEX_PROMPT_SHA = "2aa999a4fa05aeaedcff5edfee07ba4dd94433f3a7cb900a74625718d6a2561a"
R3_READS = (("glex-question-r3read1", "t26-glex-question-r3read1-v1"),
            ("glex-question-r3read2", "t26-glex-question-r3read2-v1"))


def _load(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    sys.modules[name] = mod
    spec.loader.exec_module(mod)
    return mod


# ------------------------------------------------------------------------------------------------ 1. validate redo3 answers

def redo3_defs(tasks: dict) -> tuple:
    """({task_id: ChunkDef}, {task_id: task row}) of the six redo3 tasks, as the agents saw them."""
    defs, rows = {}, {}
    r2x = FV.defs_from_chunks(FV.R2X / "chunks")
    for t in tasks["tasks"]:
        f = Path(t["task_file"])
        tid = f.stem
        rows[tid] = t
        if t["kind"] == "author":
            cd = FV.def_from_task_text(f, t["pool"])
        else:
            cd = r2x[tid]                                    # qids + choices of the source chunk (identical items)
            tcd = FV.def_from_task_text(f, t["pool"])
            if tcd.qids != cd.qids or tcd.kind != cd.kind:
                raise SystemExit(f"{tid}: the redo3 task file differs from its redo2 source chunk")
            cd.answer_file = tcd.answer_file
        if cd.answer_file != t["answer_file"] or cd.answer_file != str(ANSWERS / f"{tid}.json"):
            raise SystemExit(f"{tid}: answer path {cd.answer_file}")
        defs[tid] = cd
    return defs, rows


# ------------------------------------------------------------------------------------------------ 2. state + new pieces

def build(redo3_tasks: dict) -> object:
    from types import SimpleNamespace
    s = SimpleNamespace()
    defs, rows = redo3_defs(redo3_tasks)
    s.rep = FV.validate_round("redo3", defs, ANSWERS)
    acc = FV.accepted(s.rep)
    s.accepted = acc
    ext_ids = [t for t in defs if defs[t].kind == "extract_lex"]
    aut_ids = [t for t in defs if defs[t].kind == "author_wording"]
    # 2. the whole T26 state with the redo3 reads standing in for the (still empty) redo2/extract/answers
    # redo3=False: this script DERIVES the redo3 read tasks, so it must see the state before the redo3 fold (freeze_v2
    # folds redo3 by default and would otherwise register the new wordings a second time)
    base = FV.build(redo3=False)
    s.base_pending = list(base.pending)
    s.st = FV.build(raw_override={"r2extract": {t: acc[t] for t in ext_ids if t in acc}}, redo3=False)
    reg = s.st.reg
    s.reg = reg
    # 3. the new authored wordings
    B3 = _load("t26_build_redo3", HERE / "build_redo3.py")
    R = B3.load_build_redo2()
    _, _, batches = B3.build_authoring(R)
    p3, cov3 = FV.r2_pieces(batches, {t: acc[t] for t in aut_ids if t in acc})
    taken = {AI._norm(f.text) for f in reg.forms.values()}          # every form of every earlier round, any status
    FV.r2_lint_dedup(p3, taken)
    s.p3, s.cov3 = p3, cov3
    s.need = FV.r2_register(reg, p3)
    s.B3 = B3
    # 4. the reads
    s.batches = []
    for name, seed in R3_READS:
        items = reg.lexicon_items(sorted(s.need), seed=seed)
        b = chunker.make_batch("extract_lex", P.FAMILY, items, seed=seed, prompt=AI.LEX_PROMPT, max_items=50)
        if b.prompt_sha != LEX_PROMPT_SHA:
            raise SystemExit("LEX_PROMPT is not the unchanged G-LEX read prompt")
        s.batches.append((name, FV._finalize(b, name, AI.LEX_PROMPT, READS)))
    s.files, s.rows = reads_files(s, B3)
    return s


def reads_files(s, B3) -> tuple:
    files, rows = {}, []
    for name, b in s.batches:
        files.update(b.files())
        for c in b.chunks:
            tid = c["task_id"]
            tfile = READS / f"{tid}.txt"
            if never_open(c["answer_file"]) or never_open(tfile):
                raise chunker.ChunkError(f"never-open path for {tid}")
            files[tfile.name] = B3.extract_text(c, AI.LEX_PROMPT, c["answer_file"])
            rows.append({"task_file": str(tfile), "answer_file": c["answer_file"], "kind": "read",
                         "task_kind": "extract_lex", "pool": name,
                         "g0_ref": "G0 section 7 R1/R2 (G-LEX, 2 independent reads)", "held_out": None,
                         "n_items": len(c["items"]), "batch_id": b.batch_id, "prompt_sha": b.prompt_sha,
                         "chunk_file": str(READS / b.chunk_path(tid)), "key_file": str(READS / "key" / f"{b.batch_id}.json")})
    per_form = Counter(s.reg.forms[f].sem_id for f in s.need)
    files["TASKS.json"] = json.dumps({
        "family": P.FAMILY, "version": VERSION, "g0_sha256": P.T26Plugin.G0_SHA256_AUTHORED, "n_tasks": len(rows),
        "n_forms": len(s.need), "forms_per_sem": dict(sorted(per_form.items())),
        "note": ("G-LEX reads of the NEW redo3 wordings (4 training yn_fails + the held-out top-up that survived the "
                 "wording lint and dedup; G0 section 7 R1/R2): TWO independent reads, each form once per read, each read "
                 "its own task file for its own fresh agent (own seed, qids, item and choice order); the unchanged "
                 "LEX_PROMPT (sha 2aa999a4...) and meaning choices, decoys included. A task file is self-contained: the "
                 "agent reads only it and writes only its answer_file. chunks/ (same items, orchestrator side), key/ and "
                 "manifest/ are orchestrator-only. A read only flags: it never sets a label. Only 2/2 admits a form; one "
                 "disagreeing read rejects it for good. Record with freeze_v2.record_reads(reg, batches, accepted) under "
                 "the extractor ids " + ", ".join(n for n, _ in s.batches) + "."),
        "tasks": rows}, ensure_ascii=False, indent=1) + "\n"
    return files, rows


# ------------------------------------------------------------------------------------------------ checks

class _TextPath:
    def __init__(self, text: str, name: str):
        self._t, self.name = text, name

    def read_text(self, encoding="utf-8"):
        return self._t


def check_contract(s) -> list:
    """In-memory checks of every read task file against its chunk; returns the problems (empty = fine)."""
    probs = []
    chunk_of = {c["task_id"]: c for _, b in s.batches for c in b.chunks}
    batch_of = {c["task_id"]: b for _, b in s.batches for c in b.chunks}
    qids_by_read = []
    for name, b in s.batches:
        qids_by_read.append({q for c in b.chunks for q in (i["qid"] for i in c["items"])})
        forms = set(b.key.values())
        if forms != set(s.need):
            probs.append(f"{name}: forms differ from the registered survivors")
    if len(s.batches) != 2 or qids_by_read[0] & qids_by_read[1]:
        probs.append("the two reads share a qid")
    for r in s.rows:
        name = Path(r["task_file"]).name
        text = s.files[name]
        tid = Path(r["task_file"]).stem
        c = chunk_of[tid]
        cd = FV.def_from_task_text(_TextPath(text, name), r["pool"])
        if cd.answer_file != r["answer_file"] or not cd.answer_file.startswith(str(READ_ANSWERS) + "/"):
            probs.append(f"{name}: answer path {cd.answer_file}")
        if cd.qids != [i["qid"] for i in c["items"]] or len(set(cd.qids)) != len(cd.qids):
            probs.append(f"{name}: qids")
        lines = text.split("\n")
        start = next(i for i, ln in enumerate(lines) if ln.startswith("=== ITEMS"))
        items = [json.loads(ln) for ln in lines[start + 1:] if ln.strip()]
        if items != c["items"]:
            probs.append(f"{name}: items differ from the chunk")
        if AI.LEX_PROMPT.rstrip("\n") not in text:
            probs.append(f"{name}: the unchanged prompt is not inline")
        if hashlib.sha256(AI.LEX_PROMPT.encode("utf-8")).hexdigest() != LEX_PROMPT_SHA:
            probs.append("prompt sha")
        ch = {i["qid"]: list(i["choices"]) for i in items}
        if any(len(v) != 12 for v in ch.values()):
            probs.append(f"{name}: an item does not carry the 12 question meanings (decoys included)")
        fake = json.dumps([{"qid": q, "meaning": ch[q][0]} for q in ch]).encode()
        rep = FV.validate_answer_bytes(fake, FV.ChunkDef(cd.task_id, "extract_lex", r["pool"], cd.qids, cd.answer_file,
                                                         False, ch))
        if not rep["ok"] or rep["n_valid_items"] != len(ch):
            probs.append(f"{name}: a well-formed answer does not validate: {rep['file_problems'][:2]}")
        # gold-free: no form id, internal id, sem id or label word in the task text
        blob = text.lower()
        for iid in batch_of[tid].key.values():
            if iid.lower() in blob:
                probs.append(f"{name}: names an internal/form id")
                break
        if "q.t26." in blob or "t26|" in blob:
            probs.append(f"{name}: names a sem or internal id")
        # any path-like string in the text must be this task's answer_file
        if never_open(str(READS / name)):
            probs.append(f"{name}: never-open")
    # read 1 and read 2 of a form are in different files: no form twice in one file
    for tid, c in chunk_of.items():
        forms = [batch_of[tid].key[i["qid"]] for i in c["items"]]
        if len(set(forms)) != len(forms):
            probs.append(f"{tid}: a form twice")
    return probs


def summary(s) -> dict:
    reg = s.reg
    st = {fid: reg.status(fid) for fid in reg.forms}
    r2 = {}
    for p in s.st.p2:
        if p.get("form_id"):
            r2.setdefault((p["pool"], p["meta"]["qform"]), Counter())[st[p["form_id"]]] += 1
    train = Counter(); ho = Counter()
    for fid, f in reg.forms.items():
        if f.kind != "question" or f.source != "haiku" or st[fid] != "admitted":
            continue
        qf = f.sem_id.split(".")[-1]
        (ho if f.held_out else train)[qf] += 1
    need_by = defaultdict(Counter)
    for fid in s.need:
        f = reg.forms[fid]
        need_by["held_out" if f.held_out else "training"][f.sem_id.split(".")[-1]] += 1
    new_status = [{"internal_id": p["internal_id"], "pool": p["pool"], "qform": p["meta"]["qform"],
                   "text": AI._value(p).strip() if isinstance(AI._value(p), str) else AI._value(p),
                   "problems": p["problems"], "registered": bool(p.get("form_id")),
                   "to_read": p.get("form_id") in s.need} for p in sorted(s.p3, key=lambda x: x["internal_id"])]
    validation = {"tasks": s.rep["tasks"], "accepted_files": sum(1 for r in s.rep["files"].values() if r["ok"]),
                  "rejected": s.rep["rejected"], "item_rejects": s.rep["item_rejects"], "missing": s.rep["missing"],
                  "stray": s.rep["stray"], "files": {t: {k: v for k, v in r.items() if k != "items"}
                                                      for t, r in s.rep["files"].items()}}
    return {"version": VERSION, "validation": validation,
            "redo2_reads_recorded": s.st.r2_reads,
            "redo2_wordings_by_status": {f"{pool}|{qf}": dict(c) for (pool, qf), c in sorted(r2.items())},
            "admitted_now_by_qform": {"training": dict(sorted(train.items())), "held_out": dict(sorted(ho.items()))},
            "new_pieces": new_status, "new_pieces_dropped": sum(1 for p in s.p3 if p["problems"]),
            "new_forms_to_read": dict((k, dict(v)) for k, v in need_by.items()),
            "reads": [{"task_file": r["task_file"], "answer_file": r["answer_file"], "n_items": r["n_items"],
                       "pool": r["pool"]} for r in s.rows]}


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    g = ap.add_mutually_exclusive_group()
    g.add_argument("--dry-run", action="store_true", help="build and check, write nothing")
    g.add_argument("--check", action="store_true", help="compare the files on disk with the rebuild, write nothing")
    a = ap.parse_args(argv)
    tasks = json.loads((HERE / "TASKS.json").read_text(encoding="utf-8"))
    s = build(tasks)
    probs = check_contract(s)
    out = summary(s)
    if probs:
        print(json.dumps({"problems": probs, **out}, indent=1, ensure_ascii=False))
        return 2
    if a.check:
        diffs = [rel for rel, text in sorted(s.files.items())
                 if not (READS / rel).exists() or (READS / rel).read_text(encoding="utf-8") != text]
        print(json.dumps({"files": len(s.files), "diffs": diffs}, indent=1))
        return 1 if diffs else 0
    if not a.dry_run:
        paths.require_a38()
        paths.write_files(READS, s.files)
        paths.check_path(READ_ANSWERS).mkdir(exist_ok=True)
    out["written"] = not a.dry_run
    print(json.dumps(out, indent=1, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
