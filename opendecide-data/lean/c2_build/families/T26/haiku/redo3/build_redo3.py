"""families/T26/haiku/redo3/build_redo3.py: the T26 redo3 Haiku round (STAGE_A3_REPORT.json, T26 shortfalls).

What is short (STAGE_A3_REPORT, family T26): training yn_fails 0 of 6 admitted and held-out wordings 0 of 24 admitted (3 per
form). Every redo2 candidate is already registered and waits for its two independent G-LEX reads, so the main gap is reads.

  (a) READS. The 4 redo2/extract chunk files have no answers (haiku/redo2/extract/answers is empty). Each is re-wrapped
      here as ONE self-contained text file: the unchanged G-LEX read prompt inline (sha256 2aa999a4..., identical to
      the v1 reads), the answer contract, the items exactly as in the source chunk (same qids, same text, same 12 choices
      in the same order) and the answer path under redo3/answers/. The task id is kept, so the answer file name equals
      the one the redo2/extract key and manifest already know: copying redo3/answers/<task id>.json to
      redo2/extract/answers/<task id>.json is a 1:1 move, and the validators read the same chunk definitions.
      Read 1 (batch dc30ff13) and read 2 (batch 0a9b4c9a) stay in separate files, each for its own fresh agent.
  (b) NEW AUTHORING, only where the 2/2 G-LEX rate says the redo2 candidates may not close the gap. Sizing rule: the
      candidates in flight times the expected 2/2 admission rate of that form must close the floor with probability
      >= 0.95 (binomial) at the plausible rate. Rates come from the first pass (every form except yn_dneg_apply and
      yn_fails admitted 95 of 95; yn_dneg_apply 2 of 8 = 0.25; yn_fails 0 of 11 under the old brief, rate under the R1
      brief not yet observed, taken as 0.5 for the training floor and 0.6 for the held-out floor):
        training yn_fails   floor 6, in flight 16: P(close) 0.90 at 0.5 -> +4 (20): 0.98
        held-out yn_dneg    floor 3, in flight 10: P(close) 0.47-0.62 at 0.25-0.30 -> +10 (20): 0.91-0.97
        held-out yn_fails   floor 3, in flight  6: P(close) 0.82 at 0.6 -> +3 (9): 0.98
        held-out yn_clears  floor 3, in flight  5 (one dropped by dedup): +2 (7) so a 0.8 rate still closes (0.99)
        every other held-out form has 6-8 in flight at an observed rate near 1.0: no top-up.
      Same briefs as redo2 (build_redo2.prompt and _item are used as they are; the held-out task keeps the held-out
      styles, never a training style). Styles go first to the style the form used least in redo2, so new wordings differ
      from the redo2 ones. New internal ids: t26|wording|yn_fails|116-119 and t26|wording_ho|<qform>|100+.

Nothing here sets a label or a read's answer. The script writes only task files (and key/, manifest/, prompts/, TASKS.json)
through c2_kit.paths (A38 guard, never-open guard). Items of the authoring batches come from c2_kit.chunker.make_batch.

Run (from lean/c2_build):
  ../.venv/bin/python families/T26/haiku/redo3/build_redo3.py --dry-run   # build and check, write nothing
  ../.venv/bin/python families/T26/haiku/redo3/build_redo3.py             # write the task files
  ../.venv/bin/python families/T26/haiku/redo3/build_redo3.py --check     # files on disk == the rebuild
"""
from __future__ import annotations

import argparse
import hashlib
import importlib.util
import json
import random
import re
import sys
from collections import Counter
from pathlib import Path

sys.dont_write_bytecode = True
HERE = Path(__file__).resolve().parent                 # .../families/T26/haiku/redo3
C2_BUILD = HERE.parents[3]                              # .../lean/c2_build
if str(C2_BUILD) not in sys.path:
    sys.path.insert(0, str(C2_BUILD))

from c2_kit import chunker, paths  # noqa: E402
from c2_kit.paths import never_open  # noqa: E402
from families.T26 import author_tasks as AT  # noqa: E402
from families.T26 import plugin as P  # noqa: E402

VERSION = "redo3-v1"
REDO2 = HERE.parent / "redo2"
SRC_CHUNKS = REDO2 / "extract" / "chunks"
SRC_PROMPT = REDO2 / "extract" / "prompts" / "2aa999a4fa05aeae.txt"
SRC_KEYS = REDO2 / "extract" / "key"
LEX_PROMPT_SHA = "2aa999a4fa05aeaedcff5edfee07ba4dd94433f3a7cb900a74625718d6a2561a"
ANSWERS = HERE / "answers"

TOPUP_TRAIN = {"yn_fails": 4}                                   # ids 116-119 (R1 used 100-115)
TOPUP_HELD = {"yn_dneg_apply": 10, "yn_fails": 3, "yn_clears": 2}  # ids 100+ (R2 used 000-009)
TOPUP_ID_BASE = {("wording", "yn_fails"): 116, ("wording_heldout", "yn_dneg_apply"): 100,
                 ("wording_heldout", "yn_fails"): 100, ("wording_heldout", "yn_clears"): 100}


def load_build_redo2():
    spec = importlib.util.spec_from_file_location("t26_build_redo2", REDO2 / "build_redo2.py")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


# ------------------------------------------------------------------------------------------------ (a) re-wrapped reads

def extract_text(chunk: dict, prompt: str, answer_file: str) -> str:
    """One self-contained G-LEX read task: header, answer path, contract, the unchanged prompt, the items."""
    tid, items = chunk["task_id"], chunk["items"]
    n = len(items)
    lines = [
        f"TASK {tid}  (kind extract_lex, {n} items)",
        "",
        "This one text file is your whole task. Read all of it, then write the answer file, then stop.",
        "Do not open, search or write any other file. Create no other file.",
        "",
        f"answer_file (the exact path you must write, with the Write tool): {answer_file}",
        "",
        "=== ANSWER CONTRACT (exact) ===",
        f"Write ONE JSON array to answer_file, and nothing else in that file. The array has exactly {n} objects, one "
        "per item below, every qid exactly once.",
        "Each object has exactly two keys, \"qid\" and \"meaning\", in this shape (the angle-bracket parts are what you "
        "fill in):",
        "[",
        "  {\"qid\": \"<qid of item 1>\", \"meaning\": \"<one choice of item 1 copied exactly, or NONE>\"},",
        "  {\"qid\": \"<qid of item 2>\", \"meaning\": \"<one choice of item 2 copied exactly, or NONE>\"}",
        "]",
        f"(that sketch shows two objects; your file has {n}.) Copy each qid character for character from its item. "
        "\"meaning\" is a JSON string: exactly one of that item's own choices, copied character for character, or the "
        "single word NONE.",
        "No other keys, no wrapper object, no markdown fence, no comments, no null, no skipped qid, no qid used twice, "
        "and no qid that is not in the items below.",
        "",
        "=== INSTRUCTIONS (complete; the same text every other task in this batch received) ===",
        prompt.rstrip("\n"),
        "",
        f"=== ITEMS ({n}; one JSON object per line; every one needs an answer object with its qid) ===",
    ] + [json.dumps(it, ensure_ascii=False) for it in items]
    return "\n".join(lines) + "\n"


def build_reads() -> tuple:
    """(files {name: text}, task rows) for the 4 pending redo2/extract chunks, in file-name order."""
    prompt = SRC_PROMPT.read_text(encoding="utf-8")
    if hashlib.sha256(prompt.encode("utf-8")).hexdigest() != LEX_PROMPT_SHA:
        raise SystemExit("the G-LEX read prompt on disk is not the unchanged one")
    files, rows = {}, []
    for f in sorted(SRC_CHUNKS.glob("*.json")):
        c = json.loads(f.read_text(encoding="utf-8"))
        if "\n".join(c["instructions"]) != prompt.rstrip("\n") or c["prompt_sha"] != LEX_PROMPT_SHA:
            raise SystemExit(f"{f.name}: the chunk's instructions differ from the unchanged prompt")
        tid = c["task_id"]
        old_answer = Path(c["answer_file"])
        if old_answer.exists():
            continue                                              # answered meanwhile: nothing to redo
        for it in c["items"]:
            chunker.check_item("extract_lex", {k: v for k, v in it.items() if k != "qid"})
        answer = str(ANSWERS / f"{tid}.json")
        tfile = HERE / f"{tid}.txt"
        if never_open(answer) or never_open(tfile):
            raise chunker.ChunkError(f"never-open path for {tid}")
        files[tfile.name] = extract_text(c, prompt, answer)
        rows.append({"task_file": str(tfile), "answer_file": answer, "kind": "read", "task_kind": "extract_lex",
                     "pool": c["pool"], "g0_ref": "G0 section 7 R1/R2 (G-LEX, 2 independent reads)", "held_out": None,
                     "n_items": len(c["items"]), "batch_id": c["task_id"].rsplit("-", 1)[0],
                     "prompt_sha": c["prompt_sha"], "source_chunk": str(f), "old_answer_file": str(old_answer),
                     "key_file": str(SRC_KEYS / f"{c['task_id'].rsplit('-', 1)[0]}.json")})
    return files, rows


# ------------------------------------------------------------------------------------------------ (b) top-up authoring

def _style_of(item: dict) -> str:
    m = re.search(r"Style: (.*)\.$", item["brief"])
    return m.group(1)


def _existing_items(R) -> tuple:
    """redo2's (training yn_fails items, held-out items), rebuilt exactly as redo2.build() does."""
    rng = random.Random(f"T26|author|{R.VERSION}")
    return R.fails_items(rng), R.held_items(rng)


def topup(R, pool: str, qf: str, n: int, existing: list, styles_pool: list) -> list:
    used = Counter(_style_of(it) for iid, it in existing if iid.split("|")[2] == qf)
    order = random.Random(f"T26|author|{VERSION}|{pool}|{qf}").sample(styles_pool, len(styles_pool))
    base = TOPUP_ID_BASE[(pool, qf)]
    tag = "wording" if pool == "wording" else "wording_ho"
    out = []
    for i in range(n):
        style = min(order, key=lambda s: (used[s], order.index(s)))
        used[style] += 1
        out.append((f"t26|{tag}|{qf}|{base + i:03d}", R._item(qf, style)))
    return out


def build_authoring(R) -> tuple:
    """(files, rows, batches): the two top-up authoring tasks."""
    fails_old, held_old = _existing_items(R)
    train = []
    for qf, n in TOPUP_TRAIN.items():
        train += topup(R, "wording", qf, n, fails_old, AT.WORDING_STYLES)
    held = []
    for qf, n in TOPUP_HELD.items():
        held += topup(R, "wording_heldout", qf, n, held_old, R.HELD_STYLES)
    old_ids = {iid for iid, _ in fails_old + held_old}
    assert not old_ids & {iid for iid, _ in train + held}, "a redo3 internal id repeats a redo2 one"
    assert not set(R.HELD_STYLES) & set(AT.WORDING_STYLES)
    plan = [("wording", "R1 top-up", train, R.prompt(False), 16, f"t26-redo3-wording-yn_fails-{VERSION}"),
            ("wording_heldout", "R2 top-up", held, R.prompt(True), 15, f"t26-redo3-wording_heldout-{VERSION}")]
    files, rows, batches = {}, [], {}
    for pool, ref, items, instr, size, seed in plan:
        b = chunker.make_batch("author_wording", P.FAMILY, items, seed=seed, prompt=instr, max_items=size,
                               forbid_strings=R.FORBID)
        batches[pool] = b
        files.update({k: v for k, v in b.files().items() if not k.startswith("chunks/")})
        by_internal = dict(items)
        for c in b.chunks:
            tid = c["task_id"]
            answer = str(ANSWERS / f"{tid}.json")
            tfile = HERE / f"{tid}.txt"
            if never_open(answer) or never_open(tfile):
                raise chunker.ChunkError(f"never-open path for {tid}")
            text = R.task_text(tid, b.kind, instr, c["items"], answer)
            AT._check_text(text, R.FORBID)
            if any(iid in text for iid in b.key.values()):
                raise chunker.ChunkError("a task file names an internal id")
            files[tfile.name] = text
            qforms = Counter()
            for it in c["items"]:
                qforms[b.key[it["qid"]].split("|")[2]] += 1
                assert by_internal[b.key[it["qid"]]]["brief"] == it["brief"]
            rows.append({"task_file": str(tfile), "answer_file": answer, "kind": "author", "task_kind": b.kind,
                         "pool": pool, "g0_ref": f"G0 section 7 {ref}", "held_out": pool == "wording_heldout",
                         "n_items": len(c["items"]), "items_per_qform": dict(sorted(qforms.items())),
                         "batch_id": b.batch_id, "prompt_sha": b.prompt_sha,
                         "key_file": str(HERE / "key" / f"{b.batch_id}.json")})
    return files, rows, batches


# ------------------------------------------------------------------------------------------------ build / main

NOTE = ("redo3: G-LEX reads re-wrapped from haiku/redo2/extract/chunks (unchanged prompt sha 2aa999a4..., same qids and "
        "choices; the task id is kept, so redo3/answers/<task id>.json is the file redo2/extract/answers/<task id>.json "
        "expects) plus two small top-up authoring tasks sized by the 2/2 G-LEX admission rate (see build_redo3.py). One "
        "fresh Haiku agent per task_file; it reads only that file and writes only its answer_file. Read 1 and read 2 of a "
        "form go to different agents. key/ and manifest/ are orchestrator-only. Answers set no label. Authoring answers "
        "go through authoring_ingest.lint_wording (role wording, unchanged), dedup against every earlier wording and "
        "fixture stand-in, the registry (held_out=True for pool wording_heldout), then 2 independent G-LEX reads with "
        "the unchanged LEX_PROMPT and choices (a later read round); only 2/2 is admitted.")


def build() -> tuple:
    R = load_build_redo2()
    f_reads, r_reads = build_reads()
    f_auth, r_auth, batches = build_authoring(R)
    files = {**f_reads, **f_auth}
    rows = r_reads + r_auth
    files["TASKS.json"] = json.dumps({
        "family": P.FAMILY, "version": VERSION, "g0_sha256": P.T26Plugin.G0_SHA256_AUTHORED, "n_tasks": len(rows),
        "note": NOTE,
        "counts": {"reads": len(r_reads), "authoring": len(r_auth)},
        "sizing": {"training_yn_fails": {"floor": 6, "in_flight": 16, "ask": TOPUP_TRAIN["yn_fails"]},
                   "heldout": {qf: {"floor": 3, "ask": n} for qf, n in TOPUP_HELD.items()}},
        "tasks": rows}, ensure_ascii=False, indent=1) + "\n"
    return files, rows, batches


def check_contract(rows: list, files: dict) -> list:
    """In-memory checks of every task file against its source; returns the problems (empty = fine)."""
    from families.T26 import freeze_v2 as FV
    probs = []
    for r in rows:
        name = Path(r["task_file"]).name
        text = files[name]
        cd = FV.def_from_task_text(_TextPath(text, name), r["pool"])
        if cd.answer_file != r["answer_file"]:
            probs.append(f"{name}: answer path {cd.answer_file}")
        if not cd.answer_file.startswith(str(ANSWERS) + "/"):
            probs.append(f"{name}: answer path not under redo3/answers")
        if len(cd.qids) != r["n_items"] or len(set(cd.qids)) != len(cd.qids):
            probs.append(f"{name}: qid count")
        if r["kind"] == "read":
            src = json.loads(Path(r["source_chunk"]).read_text(encoding="utf-8"))
            lines = text.split("\n")
            start = next(i for i, ln in enumerate(lines) if ln.startswith("=== ITEMS"))
            items = [json.loads(ln) for ln in lines[start + 1:] if ln.strip()]
            if items != src["items"]:
                probs.append(f"{name}: items differ from the source chunk")
            if "\n".join(src["instructions"]) not in text:
                probs.append(f"{name}: the unchanged prompt is not inline")
            ch = {i["qid"]: list(i["choices"]) for i in items}
            fake = json.dumps([{"qid": q, "meaning": ch[q][0]} for q in ch]).encode()
            rep = FV.validate_answer_bytes(fake, FV.ChunkDef(cd.task_id, "extract_lex", r["pool"], cd.qids,
                                                             cd.answer_file, False, ch))
            if not rep["ok"] or rep["n_valid_items"] != len(ch):
                probs.append(f"{name}: a well-formed answer does not validate: {rep['file_problems'][:2]}")
        else:
            fake = json.dumps([{"qid": q, "text": "x"} for q in cd.qids]).encode()
            rep = FV.validate_answer_bytes(fake, cd)
            if not rep["ok"]:
                probs.append(f"{name}: a well-formed answer does not validate: {rep['file_problems'][:2]}")
    return probs


class _TextPath:
    """A stand-in for a Path whose read_text() returns the in-memory text (check_contract reads nothing from disk)."""
    def __init__(self, text: str, name: str):
        self._t, self.name = text, name

    def read_text(self, encoding="utf-8"):
        return self._t


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    g = ap.add_mutually_exclusive_group()
    g.add_argument("--dry-run", action="store_true", help="build and check every task, write nothing")
    g.add_argument("--check", action="store_true", help="compare the files on disk with the rebuild, write nothing")
    a = ap.parse_args(argv)
    files, rows, _ = build()
    probs = check_contract(rows, files)
    if probs:
        print(json.dumps({"problems": probs}, indent=1))
        return 2
    if a.check:
        diffs = [rel for rel, text in sorted(files.items())
                 if not (HERE / rel).exists() or (HERE / rel).read_text(encoding="utf-8") != text]
        print(json.dumps({"files": len(files), "diffs": diffs}, indent=1))
        return 1 if diffs else 0
    if not a.dry_run:
        paths.write_files(HERE, files)
        paths.require_a38()
        paths.check_path(ANSWERS).mkdir(exist_ok=True)
    print(json.dumps({"written": not a.dry_run, "n_tasks": len(rows),
                      "tasks": [{k: r.get(k) for k in ("task_file", "answer_file", "kind", "pool", "n_items",
                                                       "items_per_qform")} for r in rows]}, indent=1))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
