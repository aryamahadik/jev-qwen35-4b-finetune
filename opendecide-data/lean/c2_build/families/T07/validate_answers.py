#!/usr/bin/env python3
"""families/T07/validate_answers.py: strict answer-contract validation of every Haiku answer file of T07, all rounds
(v1 author, v1 extract, redo2 author, redo2 extract). A NEW file; read-only: it never writes, converts or edits an
answer (a file that breaks its contract is REJECTED and reported, nothing more).

The contract is the one printed at the top of each task file (and enforced in part by chunker.load_answers, which
checks qid coverage only):
  * the file is UTF-8 JSON: one array, no text around it, no code fence;
  * exactly n_items objects, one per chunk item, each with exactly the two keys "qid" and <answer field>;
  * qid values are exactly the chunk's qids: each once, none missing, none from another chunk;
  * author: "texts" / "wordings" / "forms" are lists of non-empty strings, exactly as many as the item asks for;
    "text" is one non-empty string; "pack" is an object with exactly store, ladder, regions, categories, customers
    (a string and four lists of strings); the per-task sum of outputs equals TASKS.json outputs_expected;
  * extract_lex: "meaning" is a string copied exactly from the item's "choices";
  * extract_g3h: "extraction" is an object with exactly the item's schema field names; an enum field holds one of its
    choices; every other field holds a JSON string or null (a bound as written; never a number).
Also checked per task: the answer path is the one in TASKS.json, the chunk on disk has the TASKS.json task id, kind and
item count, and the task file's sha256 is the one recorded when the tasks were written. Extra files in an answers
folder (README.txt aside) are reported.

A file-access audit failure is the orchestrator's input (`failed_audit` task ids): those answer files are not read at
all and are reported as ignored. This module never looks for a transcript.

  run (from lean/c2_build):
    /Users/aryamahadik/Documents/jev/opendecide-data/.venv/bin/python families/T07/validate_answers.py
"""
from __future__ import annotations

import hashlib
import json
import re
import sys
from pathlib import Path

C2_BUILD = Path(__file__).resolve().parents[2]
if str(C2_BUILD) not in sys.path:
    sys.path.insert(0, str(C2_BUILD))

HERE = Path(__file__).resolve().parent
HAIKU = HERE / "haiku"

# round name -> folder holding TASKS.json, chunks/, tasks/, answers/
ROUNDS = {
    "v1-author": HAIKU / "author",
    "v1-extract": HAIKU / "extract",
    "redo2-author": HAIKU / "redo2",
    "redo2-extract": HAIKU / "redo2" / "extract",
}
ANSWER_FIELD = {"extract_lex": "meaning", "extract_g3h": "extraction"}
PACK_KEYS = {"store": str, "ladder": list, "regions": list, "categories": list, "customers": list}
_WRITE_N = re.compile(r"\bwrite (\d+) (?:different |separate )?[a-z]+", re.I)


def _read_json(p: Path):
    return json.loads(p.read_text(encoding="utf-8"))


def expected_outputs(kind: str, item: dict) -> int:
    """How many outputs one authoring item asks for (its own brief says so)."""
    if kind in ("author_pack", "author_freeform"):
        return 1
    brief = item.get("brief")
    if isinstance(brief, dict) and isinstance(brief.get("how_many"), int):
        return brief["how_many"]
    if isinstance(brief, str):
        m = _WRITE_N.search(brief)
        if m:
            return int(m.group(1))
    raise ValueError(f"item {item.get('qid')}: no output count in its brief")


def _is_text_list(v, n: int) -> list:
    if not isinstance(v, list):
        return [f"not a list ({type(v).__name__})"]
    probs = []
    if len(v) != n:
        probs.append(f"{len(v)} outputs, the item asks for {n}")
    probs += [f"output {j} is not a non-empty string" for j, o in enumerate(v) if not (isinstance(o, str) and o.strip())]
    return probs


def check_value(kind: str, field: str, item: dict, value) -> list:
    """Problems with one answer value against its item (empty = valid)."""
    if field in ("texts", "wordings", "forms"):
        return _is_text_list(value, expected_outputs(kind, item))
    if field == "text":
        return [] if isinstance(value, str) and value.strip() else ["not a non-empty string"]
    if field == "pack":
        if not isinstance(value, dict):
            return ["pack is not an object"]
        probs = []
        if set(value) != set(PACK_KEYS):
            probs.append(f"pack keys {sorted(value)} != {sorted(PACK_KEYS)}")
        for k, t in PACK_KEYS.items():
            v = value.get(k)
            if not isinstance(v, t):
                probs.append(f"pack.{k} is not a {t.__name__}")
            elif t is list and not (v and all(isinstance(x, str) and x.strip() for x in v)):
                probs.append(f"pack.{k} is not a list of non-empty strings")
            elif t is str and not v.strip():
                probs.append("pack.store is empty")
        want = item.get("brief", {}).get("ladder_levels")
        if isinstance(value.get("ladder"), list) and isinstance(want, int) and len(value["ladder"]) != want:
            probs.append(f"pack.ladder has {len(value['ladder'])} levels, the item asks for {want}")
        return probs
    if field == "meaning":
        if not isinstance(value, str):
            return ["meaning is not a string"]
        return [] if value in item.get("choices", []) else ["meaning is not copied exactly from the choices"]
    if field == "extraction":
        if not isinstance(value, dict):
            return ["extraction is not an object"]
        sch = {s["field"]: s for s in item.get("schema", [])}
        probs = []
        if set(value) != set(sch):
            miss, extra = sorted(set(sch) - set(value)), sorted(set(value) - set(sch))
            probs.append(f"extraction fields differ from the schema (missing {miss}, extra {extra})")
        for name, spec in sch.items():
            if name not in value:
                continue
            v = value[name]
            if spec.get("type") == "enum":
                if v not in spec.get("choices", []):
                    probs.append(f"{name}: {v!r} is not one of its choices")
            elif not (v is None or isinstance(v, str)):
                probs.append(f"{name}: {type(v).__name__} (a string or null is the contract)")
        return probs
    return [f"unknown answer field {field!r}"]


def check_answer_array(kind: str, field: str, chunk: dict, raw, n_items: int) -> list:
    """Problems with one parsed answer array against its chunk (empty = valid)."""
    if not isinstance(raw, list):
        return [f"the file holds {type(raw).__name__}, not one array"]
    probs = []
    if len(raw) != n_items:
        probs.append(f"{len(raw)} objects, the task has {n_items} items")
    by_q = {it["qid"]: it for it in chunk["items"]}
    seen = set()
    for i, a in enumerate(raw):
        if not isinstance(a, dict):
            probs.append(f"element {i} is not an object")
            continue
        if set(a) != {"qid", field}:
            probs.append(f"element {i}: keys {sorted(a)} != ['qid', {field!r}]")
            continue
        q = a["qid"]
        if not isinstance(q, str) or q not in by_q:
            probs.append(f"element {i}: qid {q!r} is not in this task")
            continue
        if q in seen:
            probs.append(f"element {i}: qid {q} answered twice")
            continue
        seen.add(q)
        probs += [f"{q}: {p}" for p in check_value(kind, field, by_q[q], a[field])]
    miss = sorted(set(by_q) - seen)
    if miss:
        probs.append(f"{len(miss)} qid(s) unanswered, e.g. {miss[:2]}")
    return probs


def validate_task(root: Path, row: dict, *, ignored: bool = False) -> dict:
    """One task of one round: {task_id, file, status 'valid'|'invalid'|'missing'|'ignored', problems}."""
    tid, kind = row["task_id"], row["kind"]
    field = row.get("answer_field") or ANSWER_FIELD[kind]
    out = {"task_id": tid, "kind": kind, "field": field, "file": row["answer_file"], "problems": []}
    if ignored:
        return dict(out, status="ignored", problems=["file-access audit failed: answers discarded unread"])
    probs = out["problems"]
    ans = Path(row["answer_file"])
    if ans.parent != root / "answers" or ans.name != f"{tid}.json":
        probs.append("answer path is not <round>/answers/<task_id>.json")
    chunk_p = root / "chunks" / f"{tid}.json"
    task_p = Path(row["task_file"])
    if not chunk_p.is_file():
        return dict(out, status="invalid", problems=probs + ["chunk file missing"])
    chunk = _read_json(chunk_p)
    if chunk.get("task_id") != tid or chunk.get("kind") != kind or len(chunk["items"]) != row["n_items"]:
        probs.append("chunk task id, kind or item count differs from TASKS.json")
    if task_p.is_file():
        if hashlib.sha256(task_p.read_bytes()).hexdigest() != row["task_sha256"]:
            probs.append("task file sha256 differs from TASKS.json (the task changed after it was written)")
    else:
        probs.append("task file missing")
    if kind.startswith("author") and field in ("texts", "wordings", "forms"):
        total = sum(expected_outputs(kind, it) for it in chunk["items"])
        if total != row["outputs_expected"]:
            probs.append(f"items ask for {total} outputs, TASKS.json says {row['outputs_expected']}")
    if not ans.is_file():
        return dict(out, status="missing", problems=probs + ["no answer file"])
    try:
        text = ans.read_bytes().decode("utf-8")
        raw = json.loads(text)
    except (ValueError, UnicodeDecodeError) as e:
        return dict(out, status="invalid", problems=probs + [f"not valid UTF-8 JSON ({e})"])
    if text.lstrip().startswith("```"):
        probs.append("markdown code fence")
    probs += check_answer_array(kind, field, chunk, raw, row["n_items"])
    return dict(out, status="invalid" if probs else "valid", sha256=hashlib.sha256(ans.read_bytes()).hexdigest())


def validate_round(name: str, root: Path, failed_audit=()) -> dict:
    failed = set(failed_audit)
    index = _read_json(root / "TASKS.json")
    results = [validate_task(root, r, ignored=r["task_id"] in failed) for r in index["tasks"]]
    listed = {Path(r["answer_file"]).name for r in index["tasks"]}
    ans_dir = root / "answers"
    extra = sorted(p.name for p in ans_dir.iterdir()
                   if p.is_file() and p.name not in listed and p.name != "README.txt") if ans_dir.is_dir() else []
    return {"round": name, "tasks": len(results),
            "valid": sum(r["status"] == "valid" for r in results),
            "invalid": [r for r in results if r["status"] == "invalid"],
            "missing": [r["task_id"] for r in results if r["status"] == "missing"],
            "ignored": [r["task_id"] for r in results if r["status"] == "ignored"],
            "extra_files": extra, "results": results}


def validate_all(failed_audit=(), rounds: dict | None = None) -> dict:
    reps = [validate_round(n, root, failed_audit) for n, root in (rounds or ROUNDS).items() if (root / "TASKS.json").is_file()]
    ok = all(not r["invalid"] and not r["missing"] and not r["extra_files"] for r in reps)
    return {"ok": ok, "rounds": reps,
            "invalid_task_ids": sorted(x["task_id"] for r in reps for x in r["invalid"]),
            "valid_task_ids": sorted(x["task_id"] for r in reps for x in r["results"] if x["status"] == "valid")}


def main() -> int:
    rep = validate_all()
    for r in rep["rounds"]:
        print(f"{r['round']}: {r['valid']}/{r['tasks']} valid; invalid {len(r['invalid'])}; missing {len(r['missing'])}; "
              f"ignored {len(r['ignored'])}; extra files {r['extra_files']}")
        for x in r["invalid"]:
            print("  INVALID", x["task_id"], x["problems"][:5])
    print("ALL VALID" if rep["ok"] else "SOME FILES REJECTED")
    return 0 if rep["ok"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
