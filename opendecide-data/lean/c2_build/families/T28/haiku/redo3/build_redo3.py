"""families/T28/haiku/redo3/build_redo3.py: builds the T28 REDO-3 Haiku task files (STAGE_A3_REPORT.json, T28 shortfall).

Writes ONLY under haiku/redo3/ (paths.write_files, A38 guard). Edits no pinned lean/*.py, no c_build file, no other T28
file, never pools/ or pools_v2/. Haiku answers only flag: nothing here sets or reads a label or a gold.

  check   rebuild every file in memory and compare it byte for byte with haiku/redo3/ on disk (writes nothing)
  write   write the files (refuses when REDO3_INDEX.json already exists)

Run from lean/:  ../.venv/bin/python -B c2_build/families/T28/haiku/redo3/build_redo3.py check|write

The layout is the redo2 layout (chunks/, key/, manifest/, plan/, prompts/, tasks/, answers/, REDO3_INDEX.json), so
freeze_v2.py picks the round up by itself (freeze_v2.discover_rounds / load_round_n).

What this round asks for:
  1. The one open G0 shortfall: skins email, admitted 74 of 75 (the piece that failed v1, the round-1 redo and redo2;
     the Haiku answer for it is the only thing missing). Gap = 1 piece; three independent authoring attempts for that
     same piece (three agents, three style hints, same brief and same register rule as before; the first attempt that
     passes the loader checks fills it and the others are logged as unused). Each task holds ONE item.
  2. The 9 redo wordings that still wait for their 2 independent G-LEX reads (redo2-a replacements for the rejected
     yn_deny / yn_mustnot wordings and the yn_mustnot_syn retry). Not needed for a G0 minimum; they close the
     "remaining_work" line of the freeze report. Two independent reads (r3read0, r3read1), the v1.1 meaning list, the
     family's unchanged G-LEX prompt. No G3-H read is pending (160 of 160 memos pass), so none is built.
The pending set is computed from haiku/redo/ (round 1) and haiku/redo2/ only, so the build stays reproducible after
the redo3 answers exist.
"""
from __future__ import annotations

import sys

sys.dont_write_bytecode = True        # importing freeze_v2 and the kit must not leave __pycache__ files behind

import hashlib
import json
from collections import Counter
from pathlib import Path

HERE = Path(__file__).resolve().parent
T28 = HERE.parents[1]
C2_BUILD = T28.parents[1]
if str(C2_BUILD) not in sys.path:
    sys.path.insert(0, str(C2_BUILD))

from c2_kit import chunker, paths  # noqa: E402
from c2_kit.lexicon import question_sem  # noqa: E402
from families.T28 import freeze_v2 as FV  # noqa: E402
from families.T28 import haiku_author as A  # noqa: E402
from families.T28 import haiku_extract as HX  # noqa: E402
from families.T28 import plugin as P  # noqa: E402

F = "T28"
R3 = HERE
SEED = "t28-redo3-v1"
OPEN_PIECE = "t28a.skin.email.025"          # the only open G0 shortfall (skins email 74 < 75); orchestrator side only
PRIOR_FAILS = ("v1: G-SL hedge: kind of", "round-1 redo: G-SL hedge: kind of", "redo2: G-SL number: one")

WENT_WRONG = (
    "Earlier texts for this item were turned down by the program's word check. One used the phrase 'kind of' (as in "
    "'the routine kind of job') and another used the number word 'one' (as in 'a routine one'). So never write the "
    "words 'kind', 'sort' or 'one' anywhere, nor 'ones', 'someone', 'anyone' or 'no one'. To point back at the work "
    "say 'it', 'this job' or 'this step'; never sum the work up with a category word (kind, sort, type, one).")
SHAPE = (
    "Shape: the greeting line, a blank line, a body of exactly two short sentences in plain everyday words, a blank "
    "line, and the sign-off line (no name). {USER} and {AGENT} each appear at least once and at most twice in the "
    "whole e-mail, the greeting line included. Self-check before you write the file: read the e-mail word by word "
    "against every list in the REDO NOTE; when a word matches, rewrite that sentence with simpler words.")
# (attempt id, style hint): three independent agents, three different openings and sign-offs
ATTEMPTS = (
    ("a", "Style hint: the greeting line is 'Hi {AGENT},' and the sign-off line is 'Thanks,'."),
    ("b", "Style hint: the greeting line is 'Hello {USER},' and the sign-off line is 'Best wishes,'. Name {AGENT} in "
          "the body."),
    ("c", "Style hint: the greeting line is 'Hello,' and the sign-off line is 'Regards,'. Name {USER} and {AGENT} in "
          "the body."),
)


def _g0_check() -> str:
    g0 = (T28 / "G0_SPEC.v1_1.md").read_bytes()          # the G0 these task files are authored under (v1.1; G0 v1.2 moved the pin)
    sha = hashlib.sha256(g0).hexdigest()
    if sha != P.T28Plugin.G0_SHA256_AUTHORED:
        raise SystemExit("G0_SPEC.v1_1.md does not match the plugin's authored pin")
    return sha


def _skin_prompt3(br) -> str:
    """The v1 skin prompt + the redo2 word-list note (third-redo wording). The note's lists are built from the same
    gsl tables the loader uses."""
    note = br.SKIN_NOTE
    a = "REDO NOTE (second redo;"
    b = "Each item carries one extra rule naming what went wrong before: follow it exactly."
    if a not in note or b not in note:
        raise SystemExit("redo2 SKIN_NOTE changed shape")
    note = note.replace(a, "REDO NOTE (third redo;").replace(
        b, "Each item carries extra rules naming what went wrong before, and a style hint: follow them exactly.")
    return A.SKIN_PROMPT + note


# ------------------------------------------------------------------------------------------------ state before redo3
def pre_redo3_state() -> dict:
    """Everything redo3 needs, from v1 + round 1 + redo2 only (never from redo3 itself)."""
    batches = A.build_batches()
    st1 = FV.PF.admit()
    m11, br = FV.meanings_v11()
    reg2, _changed = FV.build_registry_v2(st1["reg"], m11)
    table11 = FV.meaning_table(reg2)
    problems: list = []
    v1_rej = FV.v1_rejected_ids(st1)
    a1, _recs1, _info = FV.load_round1(batches, v1_rej, set(), problems)
    r2 = FV.HAIKU / "redo2"
    au2, rds2, _recs2 = FV.load_round_n(2, r2, r2 / "REDO2_INDEX.json", batches, v1_rej, table11, set(), problems)
    mg = FV.merge_author_items(st1, batches, a1 + au2, problems)
    acc = mg["accepted"]
    new = []
    for iid in sorted(acc["wordings"]):
        q, text, held, tid, psha = acc["wordings"][iid]
        f = reg2.add(text, question_sem(F, q), family=F, source="haiku", haiku_task_id=tid, haiku_prompt_sha=psha,
                     held_out=held)
        new.append((iid, f.form_id, q))
    reg2.unit_test_all()
    for rb in rds2:
        if rb.kind == "extract_lex":
            FV.record_lex_votes(reg2, rb, problems)
    pending = [(iid, fid, q) for iid, fid, q in new if reg2.status(fid) == "pending"]
    return {"batches": batches, "reg": reg2, "m11": m11, "br": br, "pending": pending, "problems": problems,
            "skin_open": [(i, a) for (p, i), a in mg["attempts"].items() if p == "skins"],
            "skins_accepted": set(acc["skins"])}


# ------------------------------------------------------------------------------------------------ task text
def author_task(b, c, ans: str) -> str:
    n = len(c["items"])
    ex = json.dumps({"qid": c["items"][0]["qid"], "text": "<greeting line>\n\n<body sentences>\n\n<sign-off line>"},
                    ensure_ascii=False)
    return "\n".join([
        f"# Haiku REDO-3 authoring task {c['task_id']} (family {F}, kind {b.kind})", "",
        "Read this whole file. Do not open, list or search any other file, and run no other tool. When you are done, "
        "write your answer with the Write tool to exactly this path (nothing else, no other file):", "", f"    {ans}", "",
        "## Answer contract (exact)", "",
        f"The answer file holds ONE JSON list with exactly {n} object{'s' if n != 1 else ''}, one per item below. "
        "Each object has exactly two keys: \"qid\" (the item's qid, copied exactly) and \"text\" (a string; write \\n "
        "for each line break inside it, so a blank line is \\n\\n). Valid JSON only: no text before or after the "
        "list, no comments, no code fence. Every item answered once.", "",
        "Literal example of the required shape (replace the angle-bracket parts with your own words):", "",
        "[", "  " + ex, "]", "",
        "## Instructions", "", b.prompt, "", f"## Items ({n}; one JSON object per line)", "", "```json",
        "[\n" + ",\n".join(json.dumps(it, ensure_ascii=False) for it in c["items"]) + "\n]", "```", ""])


def extract_task(b, c, ans: str) -> str:
    n = len(c["items"])
    ex = [json.dumps({"qid": it["qid"], "choice": "<one choice copied character for character from THAT item's own "
                                                   "choices list>"}, ensure_ascii=False) for it in c["items"][:2]]
    shape = ["["] + ["  " + e + "," for e in ex] + (["  ..."] if n > 2 else []) + ["]"]
    if n <= 2:
        shape = ["["] + ["  " + e + ("," if i < len(ex) - 1 else "") for i, e in enumerate(ex)] + ["]"]
    return "\n".join([
        f"# Haiku REDO-3 G-LEX extraction task {c['task_id']} (family {F}, kind {b.kind})", "",
        "Read this whole file. Do not open, list or search any other file, and run no other tool. When you are done, "
        "write your answer with the Write tool to exactly this path (nothing else, no other file):", "", f"    {ans}", "",
        "## Answer contract (exact)", "",
        f"The answer file holds ONE JSON list with exactly {n} objects, one per item below (any order). Each object has "
        "exactly two keys: \"qid\" (the item's qid, copied exactly) and \"choice\" (a string: exactly one of THAT "
        "item's own choices, copied character for character). Valid JSON only: no text before or after the list, no "
        "comments, no code fence, no explanation. Every item answered once.", "",
        "Literal example of the required shape (the choice is yours to pick from each item's list):", "", *shape, "",
        "## Instructions", "", b.prompt, "", f"## Items ({n}; one JSON object per line)", "", "```json",
        "[\n" + ",\n".join(json.dumps(it, ensure_ascii=False) for it in c["items"]) + "\n]", "```", ""])


# ------------------------------------------------------------------------------------------------ build
def build() -> tuple:
    g0_sha = _g0_check()
    st = pre_redo3_state()
    br, batches, reg = st["br"], st["batches"], st["reg"]
    skin_plan_v1 = batches["skins"][1]
    skin_items_v1 = dict(A._skin_items()[0])
    if OPEN_PIECE not in skin_plan_v1 or OPEN_PIECE in st["skins_accepted"]:
        raise SystemExit("the open piece is not an open v1-rejected skin any more")
    if st["problems"]:
        raise SystemExit(f"load notes while rebuilding the pre-redo3 state: {st['problems'][:2]}")
    prompt = _skin_prompt3(br)

    # ---- authoring: three independent attempts at the open email skin (one item per task)
    base = json.loads(json.dumps(skin_items_v1[OPEN_PIECE]))
    skin_batches = []
    for att, hint in ATTEMPTS:
        it = json.loads(json.dumps(base))
        it["rules"] = list(it["rules"]) + [WENT_WRONG, SHAPE, hint]
        b = chunker.make_batch("author_skin", F, [(OPEN_PIECE, it)], seed=f"{SEED}|skin-{att}", prompt=prompt,
                               max_items=50, forbid_strings=A.FORBID_ALL)
        skin_batches.append((att, b))

    # ---- G-LEX: two independent reads of the pending redo wordings (v1.1 meaning list)
    fids = sorted(fid for _iid, fid, _q in st["pending"])
    if not fids:
        raise SystemExit("no pending redo wording")
    lex = []
    for r in range(2):
        items = reg.lexicon_items(fids, seed=f"{SEED}|glex-r{r}")
        lex.append((f"r3read{r}", chunker.make_batch("extract_lex", F, items, seed=f"{SEED}|glex-read{r}",
                                                     prompt=HX.LEX_PROMPT + HX.LEX_TAIL, max_items=HX.LEX_MAX)))

    files, tasks = {}, []
    plans = {}
    for att, b in skin_batches:
        files.update(b.files())
        plans[f"plan/{b.batch_id}.json"] = {
            "batch_id": b.batch_id, "name": "skins", "kind": "author_skin",
            "plan": {OPEN_PIECE: dict(skin_plan_v1[OPEN_PIECE], redo3_attempt=att, prior_failures=list(PRIOR_FAILS),
                                      note="same piece in every redo3 skin task: the first attempt that passes the "
                                           "loader checks fills it, later ones are logged as unused")}}
        for c in b.chunks:
            tid = c["task_id"]
            ans = str(R3 / b.answer_path(tid))
            tf = f"tasks/{tid}.md"
            files[tf] = author_task(b, c, ans)
            tasks.append({"task_file": str(R3 / tf), "answer_file": ans, "kind": b.kind, "name": f"skin_{att}",
                          "batch_id": b.batch_id, "task_id": tid, "n_items": len(c["items"]),
                          "prompt_sha": b.prompt_sha, "stage": "redo3",
                          "audit_allowed_read": [str(R3 / tf)], "audit_allowed_write": [ans]})
    forms = {}
    for iid, fid, q in st["pending"]:
        f = reg.forms[fid]
        forms[fid] = {"item": iid, "qform": q, "sem_id": question_sem(F, q), "text": f.text, "held_out": f.held_out,
                      "haiku_task_id": f.haiku_task_id, "haiku_prompt_sha": f.haiku_prompt_sha,
                      "unit_ok": bool(f.unit_ok)}
    for name, b in lex:
        files.update(b.files())
        for c in b.chunks:
            tid = c["task_id"]
            ans = str(R3 / b.answer_path(tid))
            tf = f"tasks/{tid}.md"
            files[tf] = extract_task(b, c, ans)
            tasks.append({"task_file": str(R3 / tf), "answer_file": ans, "kind": b.kind, "name": name,
                          "batch_id": b.batch_id, "task_id": tid, "n_items": len(c["items"]),
                          "prompt_sha": b.prompt_sha, "stage": "redo3",
                          "audit_allowed_read": [str(R3 / tf)], "audit_allowed_write": [ans]})
    plans["plan/glex_meanings_v1_1.json"] = {
        "g0": "G0_SPEC.md v1.1 section 3, R1", "g0_sha256": g0_sha,
        "note": "choice text -> sem id for every redo3 G-LEX read (same v1.1 list as redo2). A read admits nothing "
                "alone: 2/2 independent picks of the declared sem (any other pick rejects).",
        "meaning_to_sem": {m: question_sem(F, q) for q, m in st["m11"].items()},
        "reads": {n: b.batch_id for n, b in lex}, "forms": forms}
    for k, v in plans.items():
        files[k] = json.dumps(v, ensure_ascii=False, indent=1, sort_keys=True) + "\n"
    summary = {
        "family": F, "seed": SEED, "stage": "redo3", "g0_sha256": g0_sha, "g0_version": "v1.1 (R1)",
        "n_tasks": len(tasks), "by_kind": dict(Counter(t["kind"] for t in tasks)),
        "items": {t["name"]: t["n_items"] for t in tasks},
        "closes": {
            "shortfall": "skins email: admitted 74 < 75 (s7 ask, held_out=False)",
            "how": "3 independent authoring attempts at the one open email skin (gap 1, ~50% more asked, rounded up, "
                   "plus one spare because the piece failed three times); the first passing attempt fills it",
            "remaining_work": f"{len(fids)} redo wording(s) wait for 2 independent G-LEX reads (r3read0, r3read1)"},
        "notes": [
            "Haiku answers only flag. No label or gold is set or read here; freeze-v1 (pools/) and pools_v2/ are untouched.",
            "Each task: one fresh Haiku agent that reads only its task_file and writes only its answer_file; audit with "
            "audit.audit_jsonl(transcript, allowed_read=audit_allowed_read, allowed_write=audit_allowed_write).",
            "r3read0 and r3read1 are independent reads (two different agents); extractor ids for G-LEX are the read "
            "names (distinct from read0-2 and r2read0-1). Choices map to sem ids by plan/glex_meanings_v1_1.json.",
            "The three skin tasks answer the SAME piece: the loader accepts the first attempt that passes; an agent "
            "must not see the other attempts.",
            "After the answers exist: run freeze_v2.py check (a redoN round with this layout is picked up by itself); a "
            "v2 re-freeze needs pools_v2/ moved aside first (freeze_v2.py refuses to overwrite pools_v2/MANIFEST.json).",
        ],
        "tasks": tasks,
    }
    files["REDO3_INDEX.json"] = json.dumps(summary, ensure_ascii=False, indent=1) + "\n"
    return files, summary


def main(argv: list) -> int:
    cmd = argv[1] if len(argv) > 1 else "check"
    files, summary = build()
    if cmd == "write":
        if (R3 / "REDO3_INDEX.json").exists():
            raise SystemExit("haiku/redo3/REDO3_INDEX.json already exists: refusing to overwrite")
        paths.write_files(R3, files)
        (R3 / "answers").mkdir(exist_ok=True)
        print(json.dumps({k: v for k, v in summary.items() if k != "tasks"}, indent=1))
        return 0
    if cmd != "check":
        print(__doc__)
        return 2
    diffs = [rel for rel, text in sorted(files.items())
             if not (R3 / rel).is_file() or (R3 / rel).read_text(encoding="utf-8") != text]
    extra = sorted(str(p.relative_to(R3)) for p in R3.rglob("*") if p.is_file()
                   and p.parent.name != "answers" and p.name != "build_redo3.py" and "__pycache__" not in p.parts
                   and str(p.relative_to(R3)) not in files)
    print(json.dumps({"files": len(files), "n_tasks": len(summary["tasks"]), "differ_or_missing": diffs,
                      "extra_on_disk": extra}, indent=1))
    return 0 if not diffs and not extra else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv))
