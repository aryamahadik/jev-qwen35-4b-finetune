"""families/T29/validate_answers.py: read-only contract check of EVERY T29 Haiku answer file, all rounds (A37 / A38).

A new file. It reads the task chunks and answer files under haiku/ and writes nothing: an invalid answer is reported
(never edited, never repaired) so that the caller can leave it out. The contract of each file is the one printed in its
own task file and chunk:

  all kinds      the file is UTF-8 JSON, one array; every element an object holding exactly "qid" plus the kind's answer
                 fields; every qid of the chunk answered exactly once; no qid outside the chunk; no duplicate qid; no
                 other file in answers/ except README.txt; the chunk on disk is the same bytes the manifest hashed.
  author_*       "pack" (one object with the six pack fields), "names" / "texts" / "wordings" / "forms" (a list of
                 non-empty strings, exactly as many as the item asks for) or "text" (one non-empty string). The count
                 comes from the item's brief ("how_many", or "write N different ...") or, in the redo2 round, from the
                 task's outputs_per_item; the sum over a file must equal the manifest's outputs_expected.
  extract_lex    "meaning" is one of that item's own choices, copied exactly.
  extract_g3h    "requester" is a non-empty string; "reason" is one of that item's choices or "NONE".

  ../.venv/bin/python -m families.T29.validate_answers            (from lean/c2_build; prints a JSON report; exit 1 if
                                                                   any answer file is invalid)
"""
from __future__ import annotations

import hashlib
import json
import re
import sys
from collections import Counter
from pathlib import Path

HERE = Path(__file__).resolve().parent
HAIKU = HERE / "haiku"
ROUNDS = (("author", HAIKU / "author"), ("extract", HAIKU / "extract"), ("redo2", HAIKU / "redo2"),
          ("redo2/extract", HAIKU / "redo2" / "extract"))
PACK_FIELDS = ("org_name", "org_domain", "lookalike_domains", "partner_domains", "target_prefix", "people")
ANSWER_FIELDS = {"author_pack": None,            # "pack" or "names": from the manifest row
                 "author_skin": ("texts",), "author_wording": ("wordings",), "author_freeform": ("text",),
                 "author_lexicon": ("forms",), "extract_lex": ("meaning",), "extract_g3h": ("requester", "reason")}
NONE_CHOICE = "NONE"


def _sha(b: bytes) -> str:
    return hashlib.sha256(b).hexdigest()


def _nonempty(s) -> bool:
    return isinstance(s, str) and bool(s.strip())


def expected_count(row: dict, item: dict):
    """How many outputs one item asks for: the redo2 manifest's outputs_per_item, else the brief's how_many, else the
    'write N different ...' sentence of the brief; None when the item states no count."""
    if isinstance(row.get("outputs_per_item"), int):
        return row["outputs_per_item"]
    brief = item.get("brief")
    if isinstance(brief, dict) and isinstance(brief.get("how_many"), int):
        return brief["how_many"]
    if isinstance(brief, str):
        m = re.search(r"write (\d+) different", brief)
        if m:
            return int(m.group(1))
    return None


def _n_outputs(row: dict, ans: dict) -> int:
    """Outputs one answer holds: the length of its list, else one (a pack, a document, a pick, an extraction)."""
    for k, v in ans.items():
        if k != "qid" and isinstance(v, list):
            return len(v)
    return 1


def check_pack(pack) -> list:
    if not isinstance(pack, dict) or set(pack) != set(PACK_FIELDS):
        return [f"pack fields {sorted(pack) if isinstance(pack, dict) else type(pack).__name__} != {sorted(PACK_FIELDS)}"]
    p, bad = pack, []
    for k in ("org_name", "org_domain", "target_prefix"):
        if not _nonempty(p[k]):
            bad.append(f"{k} is not a non-empty string")
    for k, n in (("lookalike_domains", 2), ("partner_domains", 2), ("people", 4)):
        v = p[k]
        if not (isinstance(v, list) and len(v) == n and all(_nonempty(x) for x in v) and len(set(v)) == n):
            bad.append(f"{k} is not {n} distinct non-empty strings")
    if _nonempty(p["org_domain"]) and not p["org_domain"].endswith(".example"):
        bad.append("org_domain does not end in .example")
    if _nonempty(p["target_prefix"]) and not re.fullmatch(r"[A-Z]{2,4}", p["target_prefix"]):
        bad.append("target_prefix is not 2-4 capital letters")
    return bad


def check_answer(row: dict, item: dict, ans: dict) -> list:
    """Problems of one answer object (qid already matched) against its item and the manifest row."""
    kind, bad = row["kind"], []
    fields = ANSWER_FIELDS[kind] or (row.get("answer_field"),)
    if set(ans) != {"qid", *fields}:
        return [f"keys {sorted(ans)} != {sorted({'qid', *fields})}"]
    if kind == "author_pack" and fields == ("pack",):
        return check_pack(ans["pack"])
    if kind == "extract_lex":
        m = ans["meaning"]
        if not (isinstance(m, str) and m in item["choices"]):
            bad.append(f"meaning is not one of the item's choices: {str(m)[:90]!r}")
        return bad
    if kind == "extract_g3h":
        if not _nonempty(ans["requester"]):
            bad.append("requester is not a non-empty string")
        choices = next((s.get("choices") for s in item["schema"] if s["field"] == "reason"), None) or []
        if not (isinstance(ans["reason"], str) and (ans["reason"] in choices or ans["reason"] == NONE_CHOICE)):
            bad.append(f"reason is not one of the item's choices or NONE: {str(ans['reason'])[:60]!r}")
        return bad
    f = fields[0]
    v = ans[f]
    if f == "text":
        if not _nonempty(v):
            bad.append("text is not a non-empty string")
        return bad
    if not (isinstance(v, list) and v and all(_nonempty(x) for x in v)):
        return [f"{f} is not a non-empty list of non-empty strings"]
    n = expected_count(row, item)
    if n is not None and len(v) != n:
        bad.append(f"{f} holds {len(v)} outputs, the item asks for {n}")
    return bad


def check_task(root: Path, row: dict) -> dict:
    """Validate one task's answer file. Returns {"task_id", "ok", "problems", "outputs"}."""
    tid, probs = row["task_id"], []
    chunk_p, ans_p = root / "chunks" / f"{tid}.json", root / "answers" / f"{tid}.json"
    if Path(row["answer_file"]).resolve() != ans_p.resolve():
        probs.append(f"manifest answer path {row['answer_file']} is not {ans_p}")
    if not chunk_p.is_file():
        return {"task_id": tid, "ok": False, "problems": probs + ["chunk file missing"], "outputs": 0}
    chunk = json.loads(chunk_p.read_text(encoding="utf-8"))
    bm = json.loads((root / "manifest" / f"{row['batch_id']}.json").read_text(encoding="utf-8"))
    want_sha = next((t["sha256"] for t in bm["tasks"] if t["task_id"] == tid), None)
    if want_sha != _sha(json.dumps(chunk, sort_keys=True, ensure_ascii=False).encode()):
        probs.append("chunk on disk differs from the manifest hash")
    if len(chunk["items"]) != row["n_items"]:
        probs.append(f"chunk holds {len(chunk['items'])} items, manifest says {row['n_items']}")
    if not ans_p.is_file():
        return {"task_id": tid, "ok": False, "problems": probs + ["answer file missing"], "outputs": 0}
    try:
        data = json.loads(ans_p.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, UnicodeDecodeError) as e:
        return {"task_id": tid, "ok": False, "problems": probs + [f"answer is not JSON: {e}"], "outputs": 0}
    if not isinstance(data, list) or not all(isinstance(a, dict) for a in data):
        return {"task_id": tid, "ok": False, "problems": probs + ["answer is not one array of objects"], "outputs": 0}
    items = {it["qid"]: it for it in chunk["items"]}
    seen = Counter(a.get("qid") for a in data)
    probs += [f"qid {q} answered {n} times" for q, n in sorted(seen.items(), key=str) if n > 1]
    probs += [f"qid {q!r} is not in the chunk" for q in sorted(map(str, seen)) if q not in items]
    probs += [f"qid {q} unanswered" for q in sorted(set(items) - set(seen))]
    outputs = 0
    for a in data:
        it = items.get(a.get("qid"))
        if it is None:
            continue
        for p in check_answer(row, it, a):
            probs.append(f"{a['qid']}: {p}")
        outputs += _n_outputs(row, a)
    if "outputs_expected" in row and outputs != row["outputs_expected"] and not probs:
        probs.append(f"{outputs} outputs, manifest expects {row['outputs_expected']}")
    return {"task_id": tid, "ok": not probs, "problems": probs, "outputs": outputs}


def check_round(name: str, root: Path) -> dict:
    manifest = json.loads((root / "TASKS.json").read_text(encoding="utf-8"))
    rows = manifest["tasks"]
    results = [check_task(root, r) for r in rows]
    known = {f"{r['task_id']}.json" for r in rows} | {"README.txt"}
    stray = sorted(p.name for p in (root / "answers").iterdir() if p.name not in known)
    return {"round": name, "tasks": len(rows), "answer_files": sum(1 for p in (root / "answers").glob("*.json")),
            "valid": [r["task_id"] for r in results if r["ok"]],
            "invalid": {r["task_id"]: r["problems"][:12] for r in results if not r["ok"]},
            "sha256": {r["task_id"]: _sha((root / "answers" / f"{r['task_id']}.json").read_bytes())
                       for r in results if (root / "answers" / f"{r['task_id']}.json").is_file()},
            "stray_files": stray, "outputs_valid": sum(r["outputs"] for r in results if r["ok"])}


def check_all(rounds=ROUNDS) -> dict:
    out = [check_round(n, r) for n, r in rounds]
    return {"rounds": out, "answer_files_valid": sum(len(r["valid"]) for r in out),
            "answer_files_invalid": sum(len(r["invalid"]) for r in out),
            "stray_files": {r["round"]: r["stray_files"] for r in out if r["stray_files"]},
            "all_valid": all(not r["invalid"] and not r["stray_files"] and len(r["valid"]) == r["tasks"] for r in out)}


# ------------------------------------------------------------------------------------------------ redo2 cross-check
def crosscheck_redo2_extract(root: Path = HAIKU / "redo2" / "extract") -> dict:
    """An independent recount of the redo2 extraction reads, without redo2.py or the kit: G-LEX votes per new form (each
    read's pick mapped to its sem through the frozen lexicon's own meaning table and compared with the sem the form was
    written for, from pool/lexicon.jsonl; the form id is sem + sha256(text)[:8]) and the G3-H comparison of every new Mode F document (requester as written,
    reason as written). Counts only; the gates themselves are in redo2.py."""
    meaning = {}
    for s in json.loads((HERE / "pools" / "lexicon.json").read_text(encoding="utf-8"))["sems"]:
        meaning.setdefault((s["kind"], s["meaning"]), s["sem_id"])
    kinds = {}
    intended = {}
    for line in (root / "pool" / "lexicon.jsonl").read_text(encoding="utf-8").splitlines():
        r = json.loads(line)
        fid = f"{r['sem']}#{_sha(r['text'].encode())[:8]}"       # lexicon.add: sem id + sha256(text)[:8]
        intended[fid] = r["sem"]
        kinds[fid] = r["lexkind"]
    docs = {}
    for line in (root / "pool" / "freeform.jsonl").read_text(encoding="utf-8").splitlines():
        r = json.loads(line)
        docs[r["pid"]] = r
    manifest = json.loads((root / "TASKS.json").read_text(encoding="utf-8"))
    votes, g3 = {}, {"n": 0, "ok": 0, "by_register": {}}
    for row in manifest["tasks"]:
        key = json.loads((root / "key" / f"{row['batch_id']}.json").read_text(encoding="utf-8"))["key"]
        answers = json.loads((root / "answers" / f"{row['task_id']}.json").read_text(encoding="utf-8"))
        for a in answers:
            iid = key[a["qid"]]
            if row["kind"] == "extract_g3h":
                d = docs[iid]
                ok = a["requester"] == d["facts"]["REQUESTER"] and a["reason"] == d["facts"]["REASON"]
                reg = g3["by_register"].setdefault(d["register"], {"n": 0, "ok": 0})
                reg["n"] += 1
                reg["ok"] += ok
                g3["n"] += 1
                g3["ok"] += ok
            else:
                votes.setdefault(iid, {})[row["task_id"]] = meaning.get((kinds[iid], a["meaning"]))
    agree = {iid: sum(1 for v in vs.values() if v == intended[iid]) for iid, vs in votes.items()}
    return {"forms_voted": len(votes), "forms_in_pool": len(intended),
            "forms_two_reads_both_agree": sum(1 for iid, n in agree.items() if n == 2 and len(votes[iid]) == 2),
            "forms_any_disagreement": sorted(iid for iid, vs in votes.items() if any(v != intended[iid] for v in vs.values())),
            "forms_not_read_twice": sorted(iid for iid in intended if len(votes.get(iid, {})) != 2),
            "g3h": g3}


def main(argv: list) -> int:
    rep = check_all()
    print(json.dumps(rep, indent=1, ensure_ascii=False))
    return 0 if rep["all_valid"] else 1


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
