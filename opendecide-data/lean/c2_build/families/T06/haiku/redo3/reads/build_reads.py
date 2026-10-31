"""families/T06/haiku/redo3/reads/build_reads.py: the T06 redo3 read tasks (G0_SPEC.md v2, section 4; README.md "Haiku task flow").

Run after the five redo3 answer files returned. It (1) validates every redo3 answer file whole against its contract (the file,
its chunk, its manifest hash, its prompt hash and its task file are checked; a bad file is rejected whole, never edited; the
orchestrator's audit-failed list for this run is []), (2) runs the family's own lint and dedup on every newly AUTHORED piece
(haiku_author.validate_pack / check_skin / check_attack / check_wording, the same functions the v1 loaders and freeze_v2.relint
use, with the dedup set seeded by pools_v2 and by every earlier answer text), and (3) builds read tasks only for the pieces
that need a read.

What needs a read (G0_SPEC sections 1 S9, 4):
  packs, skins, attack lines  none. A pack is gated by validate_pack; a Mode T skin by G-SL + the family check (check_skin);
                              an attack line by G-SL + check_attack. None of them has a G-LEX or G3-H read.
  question wordings           G-LEX, kind question: TWO independent reads (glex-r1, glex-r2; 2/2; there is no precedence or
                              window piece in redo3, which would need 3). Each read is its own batch: its own seed, its own
                              opaque qids, its own chunk file, its own order of the closed meaning list, and its own task file
                              and answer file. The closed list holds every question meaning, the never-generated decoys
                              included (extract_build.glex_prompt, the prompt of v1 and redo2). Wordings are added to the
                              frozen pools_v2 registry first and unit tested (build_redo2.merge_wordings); one that fails
                              its unit test, or breaks the unit test of a frozen form, is dropped here and is not read.
  Mode F documents            none in redo3 (no G3-H read).

Nothing existing is edited, no answer is written here, Haiku never sees a gold, an option, a card or a row, and a Haiku answer
only flags: a pick that is not the form's own meaning rejects the form (lexicon.record_extraction). Every write goes through
c2_kit.paths.write_files (A38 guard, never-open guard).

Run from lean/:
  ../.venv/bin/python -B c2_build/families/T06/haiku/redo3/reads/build_reads.py           (dry run: prints counts, writes nothing)
  ../.venv/bin/python -B c2_build/families/T06/haiku/redo3/reads/build_reads.py --write   (writes once; refuses if TASKS.json exists)
"""
from __future__ import annotations

import sys

sys.dont_write_bytecode = True

import difflib  # noqa: E402
import hashlib  # noqa: E402
import json  # noqa: E402
from collections import Counter  # noqa: E402
from pathlib import Path  # noqa: E402

ROOT = Path(__file__).resolve().parent                       # families/T06/haiku/redo3/reads
REDO3 = ROOT.parent                                          # families/T06/haiku/redo3
HAIKU = REDO3.parent                                         # families/T06/haiku
T06 = HAIKU.parent                                           # families/T06
C2_BUILD = T06.parents[1]                                    # lean/c2_build
if str(C2_BUILD) not in sys.path:
    sys.path.insert(0, str(C2_BUILD))

from c2_kit import chunker, paths  # noqa: E402
from c2_kit import lexicon as LX  # noqa: E402
from families.T06 import extract_build as E  # noqa: E402
from families.T06 import freeze_v2 as FZ  # noqa: E402
from families.T06 import haiku_author as H  # noqa: E402
from families.T06 import plugin as P  # noqa: E402

FAMILY = "T06"
VERSION = "redo3-reads-v1"
POOLS_V2 = T06 / "pools_v2"                              # the freeze these tasks were built from (before redo3) ...
if (T06 / "pools_v2_prev" / "MANIFEST.json").is_file():   # ... which freeze_v2.py moved aside when it folded redo3 in
    POOLS_V2 = T06 / "pools_v2_prev"
READS = ("glex-r1", "glex-r2")                               # 2/2 for question forms (lexicon.LexForm.required)
MAX_TASKS = 8
NEAR_DUP = 0.90                                              # reported, never a drop: the family's dedup is the exact
#                                                              normalised text (check_skin / check_attack / check_wording)


def _jsonl(path: Path) -> list:
    paths.check_path(path)
    return [json.loads(x) for x in Path(path).read_text(encoding="utf-8").splitlines() if x.strip()]


def _json(path: Path):
    paths.check_path(path)
    return json.loads(Path(path).read_text(encoding="utf-8"))


def _sha(path: Path) -> str:
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


# ------------------------------------------------------------------------------------------------ 1  the answer files
def load_redo3() -> dict:
    """Every redo3 answer file validated whole. -> {"files": [record per task], "answers": {internal id: answer object},
    "task_of": {internal id: task id}, "plan": {internal id: plan}, "prompt_sha": {internal id: sha}}. A file with any
    problem leaves its items out (rejected whole, never edited); the record lists the problems."""
    index = _json(REDO3 / "TASKS.json")
    out = {"files": [], "answers": {}, "task_of": {}, "plan": {}, "prompt_sha": {}, "index": index}
    for bid in sorted({t["batch_id"] for t in index["tasks"]}):
        key = _json(REDO3 / "key" / f"{bid}.json")["key"]
        out["plan"].update(_json(REDO3 / "plan" / f"{bid}.json")["plan"])
        man = _json(REDO3 / "manifest" / f"{bid}.json")
        pfile = REDO3 / "prompts" / f"{man['prompt_sha'][:16]}.txt"
        for t in index["tasks"]:
            if t["batch_id"] != bid:
                continue
            tid = t["task_id"]
            probs = []
            chunk = _json(REDO3 / "chunks" / f"{tid}.json")
            mt = next((x for x in man["tasks"] if x["task_id"] == tid), None)
            if mt is None or chunker.sha(json.dumps(chunk, sort_keys=True, ensure_ascii=False)) != mt["sha256"]:
                probs.append("chunk differs from its manifest hash")
            if chunk.get("prompt_sha") != man["prompt_sha"] or chunker.sha(pfile.read_text(encoding="utf-8")) \
                    != man["prompt_sha"]:
                probs.append("prompt differs from its manifest hash")
            tfile = Path(t["task_file"])
            if _sha(tfile) != t["task_sha256"]:
                probs.append("task file on disk differs from TASKS.json")
            qids = [it["qid"] for it in chunk["items"]]
            afile = Path(t["answer_file"])
            raw = None
            if not afile.is_file():
                probs.append("no answer file")
            else:
                data = paths.check_path(afile).read_bytes()
                try:
                    raw = json.loads(data.decode("utf-8"))
                except (UnicodeDecodeError, json.JSONDecodeError) as e:
                    probs.append(f"answer is not valid UTF-8 JSON ({str(e)[:60]})")
                else:
                    probs += FZ.answer_problems(t["kind"], raw, qids)
            rec = {"task_id": tid, "batch_id": bid, "kind": t["kind"], "answer_file": str(afile),
                   "sha256": _sha(afile) if afile.is_file() else None,
                   "n_items": len(qids), "n_answered": len(raw) if isinstance(raw, list) else 0,
                   "valid": not probs, "problems": probs[:8]}
            out["files"].append(rec)
            if probs:
                continue
            for a in raw:
                iid = key[a["qid"]]
                out["answers"][iid] = {k: v for k, v in a.items() if k != "qid"}
                out["task_of"][iid] = tid
                out["prompt_sha"][iid] = man["prompt_sha"]
    return out


# ------------------------------------------------------------------------------------------------ 2  family lint / dedup
def _prior_texts() -> set:
    """Normalised text of every earlier authoring answer (v1 author round and redo2), admitted or dropped."""
    seen = set()
    for rnd in ("author", "redo2"):
        for f in sorted((HAIKU / rnd / "answers").glob("*.json")):
            for a in json.loads(f.read_text(encoding="utf-8")):
                if isinstance(a, dict) and isinstance(a.get("text"), str):
                    seen.add(H._norm(a["text"]))
    return seen


def _near(text: str, others: list) -> tuple:
    """(highest similarity ratio, the text) of `text` against `others` (normalised, informational only)."""
    best = (0.0, "")
    for o in others:
        r = difflib.SequenceMatcher(None, H._norm(text), H._norm(o)).ratio()
        if r > best[0]:
            best = (r, o)
    return round(best[0], 3), best[1]


def lint(r3: dict) -> dict:
    """The family's lint and dedup over every newly authored piece. -> {"packs"|"skins"|"attacks"|"wordings":
    {"kept": [...], "drops": [...]}}; each drop carries the item id and the reasons, nothing is edited."""
    ans, plan, tof, psha = r3["answers"], r3["plan"], r3["task_of"], r3["prompt_sha"]
    out = {k: {"kept": [], "drops": []} for k in ("packs", "skins", "attacks", "wordings")}
    prior = _prior_texts()

    # packs: validate_pack + a store or jurisdiction that no pool pack or earlier kept pack uses (as the v1 loader)
    pool_packs = _jsonl(POOLS_V2 / "packs.jsonl")
    names = {p["store"] for p in pool_packs} | {p["jurisdiction"] for p in pool_packs}
    for iid in sorted(i for i in ans if plan[i]["role"] == "pack"):
        p = ans[iid].get("pack")
        v = H.validate_pack(p)
        if not v and (p["store"] in names or p["jurisdiction"] in names):
            v = ["store or jurisdiction repeats another pack"]
        if v:
            out["packs"]["drops"].append({"item": iid, "task_id": tof[iid], "reasons": v})
        else:
            names |= {p["store"], p["jurisdiction"]}
            out["packs"]["kept"].append({"item": iid, "pid": f"t06pk-{iid.rsplit('.', 1)[1]}",
                                         "held_out": plan[iid]["held_out"], "store": p["store"],
                                         "jurisdiction": p["jurisdiction"], "haiku_task_id": tof[iid]})

    # skins and attack lines: the loaders' own checks, the dedup set = pools_v2 texts + every earlier answer text
    sk_pool = _jsonl(POOLS_V2 / "skins.jsonl")
    at_pool = _jsonl(POOLS_V2 / "attacks.jsonl")
    seen_sk = {H._norm(r["text"]) for r in sk_pool} | prior
    for iid in sorted(i for i in ans if plan[i]["role"] == "skin"):
        meta = plan[iid]
        text = ans[iid]["text"]
        _o, v = H.check_skin(iid, text, {"register": meta["register"], "escape": meta["escape"],
                                         "held_out": meta["held_out"]}, tof[iid], psha[iid], seen_sk)
        rec = {"item": iid, "task_id": tof[iid], "register": meta["register"], "held_out": meta["held_out"],
               "text": text.strip()}
        if v:
            out["skins"]["drops"].append(dict(rec, reasons=v))
        else:
            r, other = _near(text, [x["text"] for x in sk_pool if x["register"] == meta["register"]])
            out["skins"]["kept"].append(dict(rec, near_pool_ratio=r, near_pool_flag=r >= NEAR_DUP))
    seen_at = {H._norm(r["text"]) for r in at_pool} | prior
    for iid in sorted(i for i in ans if plan[i]["role"] == "attack"):
        meta = plan[iid]
        text = ans[iid]["text"]
        _o, v = H.check_attack(iid, text, {"decl": meta["decl"], "held_out": meta["held_out"]}, tof[iid], psha[iid],
                               seen_at)
        rec = {"item": iid, "task_id": tof[iid], "held_out": meta["held_out"], "kind_index": meta["kind_index"],
               "text": text.strip()}
        if v:
            out["attacks"]["drops"].append(dict(rec, reasons=v))
        else:
            r, other = _near(text, [x["text"] for x in at_pool])
            out["attacks"]["kept"].append(dict(rec, near_pool_ratio=r, near_pool_flag=r >= NEAR_DUP))

    # wordings: check_wording (exact negcount, full refund, scope and anchor rules, fixture copy) + dedup
    wd_pool = _jsonl(POOLS_V2 / "wordings.jsonl")
    seen_wd = {H._norm(r["text"]) for r in wd_pool} | prior
    for iid in sorted(i for i in ans if plan[i]["role"] == "wording"):
        meta = plan[iid]
        text = ans[iid]["text"]
        obj, v = H.check_wording(iid, text, {"qform": meta["qform"], "held_out": meta["held_out"]}, tof[iid],
                                 psha[iid], seen_wd)
        rec = {"item": iid, "task_id": tof[iid], "qform": meta["qform"], "held_out": meta["held_out"],
               "text": " ".join(text.split())}
        if v:
            out["wordings"]["drops"].append(dict(rec, reasons=v))
        else:
            r, other = _near(text, [x["text"] for x in wd_pool if x["qform"] == meta["qform"]])
            out["wordings"]["kept"].append(dict(rec, near_pool_ratio=r, near_pool_flag=r >= NEAR_DUP, obj=obj))
    return out


# ------------------------------------------------------------------------------------------------ 3  G-LEX read plan
def frozen_registry() -> LX.LexiconRegistry:
    """pools_v2/lexicon.json (the frozen admitted forms, every sem incl. the decoys), re-read and re-tested."""
    reg = LX.LexiconRegistry.from_json(_json(POOLS_V2 / "lexicon.json"))
    bad = [fid for fid in reg.forms if reg.status(fid) != "admitted"]
    if bad:
        raise SystemExit(f"STOP: pools_v2 forms are not admitted after reload: {bad[:3]}")
    return reg


def glex_plan(wordings_kept: list) -> dict:
    """The wordings that survived lint, merged into the frozen registry (unit tested), and the two G-LEX read batches.
    -> {"reg", "new" {form id: (iid, qform, text, held, task id, prompt sha)}, "merge_drops", "batches" [(read, batch)]}"""
    BR = FZ.build_redo2()
    reg = frozen_registry()
    n_frozen = len(reg.forms)
    kept = [(w["item"], w["obj"]) for w in wordings_kept]
    new, merge_drops = BR.merge_wordings(reg, kept)
    if len(reg.forms) != n_frozen + len(new):
        raise SystemExit("STOP: the registry lost a frozen form in the merge")
    new_ids = sorted(new)
    if len(new_ids) > E.GROUP:
        raise SystemExit("STOP: more than one G-LEX group of new wordings")
    meanings = sorted(s.meaning for s in reg.sems.values() if s.kind == "question")
    batches = []
    for r, label in enumerate(READS, start=1):
        seed = f"{FAMILY}-glex-redo3-r{r}-question-00"
        order = sorted(meanings, key=lambda m: hashlib.sha256(f"{seed}|{m}".encode()).hexdigest())
        items = [(fid, {"text": E.glex_text(reg, fid, r - 1)}) for fid in new_ids]
        if not items:
            continue
        b = chunker.make_batch("extract_lex", FAMILY, items, seed=seed, prompt=E.glex_prompt(order), max_items=E.GROUP)
        if len(b.chunks) != 1:
            raise SystemExit(f"STOP: {seed}: one chunk per read")
        batches.append((label, b))
    return {"reg": reg, "new": new, "merge_drops": merge_drops, "batches": batches, "n_frozen": n_frozen}


def task_text(label: str, b, chunk: dict, root: Path = ROOT) -> str:
    """One self-contained read task: answer path, inline answer contract with a literal example, the G-LEX prompt with the
    closed meaning list, the items (a text each, with its qid). The agent opens this file only."""
    tid = chunk["task_id"]
    n = len(chunk["items"])
    qids = [it["qid"] for it in chunk["items"]]
    tfile = root / "tasks" / f"{tid}.md"
    afile = root / b.answer_path(tid)
    return "\n".join([
        f"# T06 redo3 read task {tid}  (family T06, kind extract_lex / question, read {label}, {n} items)", "",
        "This one text file is your whole task. Read all of it, then write the answer file, then stop.",
        "Do not open, list, search or write any other file or folder. Create no other file. Do not put the answer in chat;",
        "when the answer file is written, reply with the single word DONE.", "",
        f"TASK FILE (this file)                 : {tfile}",
        f"ANSWER FILE (write exactly this path) : {afile}",
        "(The folder of that path is created by your write if it does not exist yet.)", "",
        "=== ANSWER CONTRACT (exact; a program checks it) ===",
        "Write ONE JSON array to the ANSWER FILE with the Write tool, and nothing else in that file: no markdown fence, no",
        "comment, no wrapper object, no extra text before or after the array.",
        f"- The array has exactly {n} objects, one for each of the {n} items below, every qid exactly once (any order).",
        '- Each object has exactly these keys and no others: "qid", "meaning".',
        '- "qid": the item\'s qid, copied character for character (the letter q followed by ten letters or digits). It is an',
        "  opaque label; read nothing into it.",
        '- "meaning": ONE line of the CLOSED LIST below, copied character for character (never a new meaning, never',
        "  a paraphrase, never the text itself).",
        '- Inside a JSON string write a double quote as \\" and a line break as \\n. Valid JSON only.',
        '- Not allowed: any other key (such as "note", "reason" or "confidence"); a skipped qid; a qid used twice; a qid that',
        "  is not in the items below.",
        f"The qids of this task: {', '.join(qids)}.",
        'Shape of one object: {"qid": "<the item\'s qid>", "meaning": "<the chosen meaning, copied exactly>"}',
        f"Literal example of the required shape (the qid shown is the first real one; your array has {n} objects):",
        "[",
        f'  {{"qid": "{qids[0]}", "meaning": "<one line of the CLOSED LIST, copied character for character>"}}',
        "]", "",
        "=== INSTRUCTIONS ===",
        b.prompt.rstrip(), "",
        f"=== ITEMS ({n}; one text each; every item needs one answer object carrying its qid) ===",
        "```json", json.dumps(chunk["items"], ensure_ascii=False, indent=1), "```", ""])


def read_files(plan: dict, root: Path = ROOT) -> tuple:
    """({relative path: text}, [task rows]) for paths.write_files."""
    files, rows = {}, []
    for label, b in plan["batches"]:
        files.update(b.files())
        for c in b.chunks:
            tid = c["task_id"]
            tfile = f"tasks/{tid}.md"
            text = task_text(label, b, c, root)
            files[tfile] = text
            rows.append({"read": label, "kind": "question", "group": 0, "batch_id": b.batch_id, "task_id": tid,
                         "task_file": str(root / tfile), "answer_file": str(root / b.answer_path(tid)),
                         "n_items": len(c["items"]), "outputs_expected": len(c["items"]), "prompt_sha": b.prompt_sha,
                         "task_sha256": hashlib.sha256(text.encode()).hexdigest(),
                         "allowed_read": [str(root / tfile)], "allowed_write": [str(root / b.answer_path(tid))]})
    return files, rows


# ------------------------------------------------------------------------------------------------ arithmetic and report
def closing(lint_out: dict, kept_wordings_after_merge: dict) -> list:
    """The piece gaps of pools_v2 against the pieces that survived lint (wordings: before G-LEX, which can still drop one)."""
    import importlib.util
    spec = importlib.util.spec_from_file_location("t06_build_redo3", REDO3 / "build_redo3.py")
    b3 = importlib.util.module_from_spec(spec)
    sys.modules["t06_build_redo3"] = b3
    spec.loader.exec_module(b3)
    gaps = b3.manifest_gaps()
    L = lint_out
    pk = L["packs"]["kept"]
    sk = Counter(x["register"] for x in L["skins"]["kept"])
    at_held = sum(1 for x in L["attacks"]["kept"] if x["held_out"])
    wd = Counter(kept_wordings_after_merge.values())
    rows = [
        ("packs, training", gaps["packs_train"], sum(1 for x in pk if not x["held_out"])),
        ("packs, held out", gaps["packs_held"], sum(1 for x in pk if x["held_out"])),
        ("skins, chat", gaps["skin_chat"], sk["chat"]), ("skins, email", gaps["skin_email"], sk["email"]),
        ("skins, yaml", gaps["skin_yaml"], sk["yaml"]), ("skins, held-out transcript", gaps["skin_transcript"],
                                                          sk["transcript"]),
        ("attack lines, held out", gaps["attack_held"], at_held),
        ("wordings ch_rule, training", gaps["wd_ch_rule"], wd["ch_rule"]),
        ("wordings yn_refund, training", gaps["wd_yn_refund"], wd["yn_refund"]),
        ("wordings yn_double, training", gaps["wd_yn_double"], wd["yn_double"]),
        ("wordings yn_not_refund, training", gaps["wd_yn_not_refund"], wd["yn_not_refund"])]
    return [{"piece": n, "gap": g, "kept_after_lint": k, "closes_gap": k >= g,
             "note": "wordings still need 2/2 G-LEX" if n.startswith("wordings") else "no read needed"}
            for n, g, k in rows]


def build(root: Path = ROOT) -> dict:
    r3 = load_redo3()
    L = lint(r3)
    plan = glex_plan(L["wordings"]["kept"])
    files, rows = read_files(plan, root)
    if len(rows) > MAX_TASKS:
        raise SystemExit(f"STOP: {len(rows)} read tasks (at most {MAX_TASKS})")
    new = plan["new"]
    wd_after_merge = {fid: v[1] for fid, v in new.items()}
    new_forms = [{"form_id": fid, "item": v[0], "qform": v[1], "text": v[2], "held_out": bool(v[3]),
                  "haiku_task_id": v[4], "haiku_prompt_sha": v[5]} for fid, v in sorted(new.items())]
    clos = closing(L, wd_after_merge)
    lint_report = {k: {"kept": [{x: y for x, y in d.items() if x != "obj"} for d in v["kept"]], "drops": v["drops"]}
                   for k, v in L.items()}
    counts = {
        "answer_files": len(r3["files"]), "answer_files_valid": sum(1 for f in r3["files"] if f["valid"]),
        "authored": dict(Counter(r3["plan"][i]["role"] for i in r3["answers"])),
        "kept_after_lint": {k: len(v["kept"]) for k, v in L.items()},
        "dropped_by_lint": {k: len(v["drops"]) for k, v in L.items()},
        "wordings_unit_ok_new": len(new), "wordings_merge_drops": plan["merge_drops"],
        "registry_forms_before": plan["n_frozen"], "registry_forms_after_merge": len(plan["reg"].forms),
        "glex_items_per_read": {lab: sum(len(c["items"]) for c in b.chunks) for lab, b in plan["batches"]},
        "read_tasks": len(rows), "g3h_reads": 0,
        "near_duplicate_flags (ratio >= %.2f vs the pool, informational)" % NEAR_DUP:
            sum(1 for k in ("skins", "attacks", "wordings") for d in L[k]["kept"] if d["near_pool_flag"])}
    index = {
        "family": FAMILY, "version": VERSION, "stage": "redo3 reads (new question wordings: G-LEX 2/2)",
        "gate": "G-LEX 2/2 (kind question); packs, skins and attack lines have no read; no Mode F document in redo3",
        "g0_sha256": P.T06Plugin.G0_SHA256, "builder": str(ROOT / "build_reads.py"),
        "source_answers_sha256": {f["task_id"]: f["sha256"] for f in r3["files"]},
        "counts": counts, "closing_arithmetic": clos, "n_tasks": len(rows),
        "outputs_expected": sum(r["outputs_expected"] for r in rows),
        "notes": [
            "Audit each agent with audit.audit_jsonl(allowed_read, allowed_write) before its answers count; an audit-failed "
            "answer is ignored whole. The G-LEX reads are independent: own seed, own opaque qids, own chunk, own order of the "
            "closed meaning list, own task and answer file.",
            "Next freeze: add 'redo3' (author round: packs, skins, attacks, wordings) and 'redo3/reads' (extraction round, "
            "kind question) to freeze_v2.ROUNDS; the redo3 pieces enter the pools through the lint verdicts in LINT.json "
            "(a dropped piece never enters) and the wordings through record_extraction of these reads (extractor ids "
            "haiku-r3-glex-r1 / haiku-r3-glex-r2).",
            "Labels: none. Haiku writes text pieces and picks meanings only; every gold still comes from solver A = solver B."],
        "tasks": rows}
    lint_json = {"family": FAMILY, "version": VERSION, "validation": r3["files"], "lint": lint_report,
                 "new_wording_forms": new_forms, "closing_arithmetic": clos, "counts": counts}
    files["TASKS.json"] = json.dumps(index, ensure_ascii=False, indent=1) + "\n"
    files["LINT.json"] = json.dumps(lint_json, ensure_ascii=False, indent=1) + "\n"
    return {"files": files, "index": index, "lint": lint_json, "plan": plan, "r3": r3}


def check_on_disk(root: Path, files: dict) -> list:
    return [rel for rel, text in sorted(files.items())
            if not (Path(root) / rel).is_file() or (Path(root) / rel).read_text(encoding="utf-8") != text]


def main(argv: list) -> int:
    write = "--write" in argv
    res = build()
    index = res["index"]
    bad = [f for f in res["r3"]["files"] if not f["valid"]]
    if bad:
        print("REJECTED answer files (whole):", json.dumps(bad, indent=1))
    if write:
        if (ROOT / "TASKS.json").exists():
            raise FileExistsError(f"{ROOT}/TASKS.json exists: the redo3 read tasks are written once")
        paths.write_files(ROOT, res["files"])
    else:
        on_disk = check_on_disk(ROOT, res["files"]) if (ROOT / "TASKS.json").exists() else None
        print(f"on disk differs: {on_disk}" if on_disk else "on disk: same bytes" if on_disk == [] else
              "on disk: not written")
    print(json.dumps(index["counts"], indent=1, ensure_ascii=False))
    print(json.dumps(index["closing_arithmetic"], indent=1, ensure_ascii=False))
    for r in index["tasks"]:
        print(f"{r['read']:8s} {r['kind']:9s} items {r['n_items']:3d} {r['task_file']} -> {r['answer_file']}")
    print(f"{index['n_tasks']} tasks, {index['outputs_expected']} outputs expected; written: {write}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
