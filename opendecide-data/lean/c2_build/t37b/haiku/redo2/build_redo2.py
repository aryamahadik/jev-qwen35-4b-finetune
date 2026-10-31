"""t37b/haiku/redo2/build_redo2.py: T37b REDO-2. A NEW Haiku authoring batch for the four equiv-pool entries that
the 13 Oct pool freeze left short (pools/MANIFEST.json "shortfall"): gd_comve/against 0 of 12, gd_multiwoz21_sysacts/
match 0 of 7, gd_nhtsa_complaints/injury 0 of 7, gd_taskmaster1/status 1 of 12 (37 paraphrases short).

Nothing that exists changes. No v1 task, answer, key, candidate, read or pool is reused or edited. The same goes for
author_pool.py, gsl_pool_lint.py, builder.py, G0_LITE_T37B.md (sha 9733b721), the pinned lean/*.py and c_build.
No gate bar, G0 target, check or gold semantics changes either. Every redo2 paraphrase passes the UNCHANGED v1
checks: author_pool.lint_one (placeholders, bans, both polarity programs 'same' on every probe fill), then
gsl_pool_lint.gsl_check (G-SL, role "wording", with empty label words, exceptions and NAME_ALLOW). Then come two
independent Haiku polarity reads (POOL_POLARITY_PROMPT unchanged), and author_pool.admit admits a paraphrase only on
'same' / 'same'. A redo2 text equal to any v1 author text (admitted or dropped) is a duplicate and drops: it gets no
second read. Haiku answers only admit or drop a paraphrase. Nothing here sets or reads a label or a gold.

The cause of each blocker: the v1 brief asked for wording that the unchanged G-SL lint drops. The fix: a new brief
whose rules lead to wording that passes the same lint with the same meaning.
  B1  gd_comve/against (0 of 21 lint-passed survived G-SL: 'name: Statement' 21, 'number: two' 19, 'number: one' 1).
      The program needs a capitalised 'Statement {N}' after the first word (polarity anchors). G-SL reads a
      capitalised word as a name unless it starts a sentence, a line or a label (gsl._sentence_starts: after
      '.', '!', '?', ':', ';' or '|'). Fix: the required shape
      "<short opening phrase about the statements shown>: Statement {N}, <rest in lowercase>?". 'Statement' then
      starts the part after the colon, as a label does. Counting words are never written ('the statements shown',
      'the pair of statements'). No NAME_ALLOW and no exception: the kit's own label-start rule.
  B2  gd_multiwoz21_sysacts/match and gd_nhtsa_complaints/injury (every text dropped 'number: one'). The v1 brief said
      keep 'least' and every condition, so every author copied 'at least one', and 'one' is a CORE number word.
      Fix: write 'at least a single <noun>', which has the same meaning and keeps 'least'. Never write 'one'.
  B3  gd_taskmaster1/status (20 of 21 dropped 'relative_time: last'). The v1 brief's own example was "keep ... 'last
      message'". Fix: write 'final message' or 'latest message', which has the same meaning in a finished
      conversation. Never write 'last' or 'most recent'. The v1 admitted text is listed as taken.
Asked: comve 8 items, match 4, injury 4, taskmaster1 6; 5 questions per item (110 questions in 3 tasks of <= 8 items).

Stages (each later stage rebuilds the earlier ones in memory and stops if a batch on disk differs):
  author   tasks/<task_id>.md (self-contained: answer path, inline answer contract, prompt, items), chunks/,
           prompts/, key/ and plan/ (orchestrator only), manifest/, TASKS.json. answers/ is written only by the agents.
  extract  (every author answer present) lint_one + G-SL + v1 dedup -> lint/candidates.json, lint/report.json,
           lint/gsl_drops.json, and the two independent polarity reads under extract/ (separate seeds, chunks, agents).
  admit    (every read answer present) author_pool.admit -> the SUPPLEMENT pool ../../pools/redo2/
           (t37b_equiv_pool_redo2.json, MANIFEST.json with merged counts against the G0 targets, never lowered;
           QUARANTINE.json). pools/t37b_equiv_pool.json and pools/MANIFEST.json are not touched. The build then uses
           load_merged_pool() (v1 pool + supplement, both verified) in place of author_pool.load_pool().

Run from lean/ (each stage prints its counts and problems; --write writes once):
  ../.venv/bin/python c2_build/t37b/haiku/redo2/build_redo2.py author  [--write]
  ../.venv/bin/python c2_build/t37b/haiku/redo2/build_redo2.py extract [--write]
  ../.venv/bin/python c2_build/t37b/haiku/redo2/build_redo2.py admit   [--write]
"""
from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
from collections import Counter
from pathlib import Path

HERE = Path(__file__).resolve().parent                  # t37b/haiku/redo2
T37B = HERE.parents[1]
C2_BUILD = T37B.parent
if str(C2_BUILD) not in sys.path:
    sys.path.insert(0, str(C2_BUILD))

from c2_kit import chunker, paths  # noqa: E402
from t37b import author_pool as AP  # noqa: E402
from t37b import builder as BL  # noqa: E402
from t37b import gsl_pool_lint as GL  # noqa: E402
from t37b import sources as SRC  # noqa: E402

FAMILY = "T37b"
VERSION = "r2"
SEED = "t37b-redo2-author-v1"
SEED_POL = "t37b-redo2-polarity-v1"
ROOT = HERE
LINT_DIR = HERE / "lint"
EX_ROOT = HERE / "extract"
SUPP = AP.POOL_DIR / "redo2"
SUPP_POOL = SUPP / "t37b_equiv_pool_redo2.json"
V1_POOL = AP.POOL_FILE
V1_POOL_SHA256 = "69f5f65dcf0cd2787d5e61594b84c16599e073e6d50f2c3c5a19323a0089c579"   # pools/MANIFEST.json (frozen)
CHUNK = 8
PER_ITEM = AP.PER_ITEM
# entry key, authoring items, blocker, the need (v1 pools/MANIFEST.json; G0 targets are author_pool.TARGET_*)
PLAN = (("gd_comve/against", 8, "B1", "G0 target 12, v1 admitted 0"),
        ("gd_multiwoz21_sysacts/match", 4, "B2", "G0 target 7, v1 admitted 0"),
        ("gd_nhtsa_complaints/injury", 4, "B2", "G0 target 7, v1 admitted 0"),
        ("gd_taskmaster1/status", 6, "B3", "G0 target 12, v1 admitted 1"))

REDO2_PROMPT = AP.AUTHOR_POOL_PROMPT + (
    " Some items also give a required shape, or a word to write in place of a word of the item's question: follow "
    "those rules exactly, because a program throws away every question that breaks a rule.")

# ------------------------------------------------------------------------------------------------ rules
SAME_RULE = "Ask exactly the same thing: keep every condition and every person or thing the question names."
DIRECT_RULE = ("Ask the question directly: do not open with a phrase that asks whether a statement holds, do not ask "
               "about an answer or an option, and do not ask for an opinion.")
WORDS_RULE = ("Never write a number word (such as one, two, three, first, second, twice, half or dozen), a time word "
              "(such as last, next, now, today, earlier, later, recently, currently, previously, soon, already, yet "
              "or past) or a hedge word (such as maybe, perhaps, probably, possibly, likely, apparently, seems, "
              "appears, think, believe, guess, almost, nearly or roughly): a program throws away every question that "
              "holds one.")
COMVE_HINTS = (
    "keep the verb 'go against' and ask with 'does it'",
    "use a different verb or phrase with exactly the same meaning as 'go against'",
    "ask with 'is it' followed by a phrase that means exactly 'going against common sense'",
    "open with a phrase that says where the statements are (shown, given, listed or presented)",
    "make it as short as you can while keeping every condition",
    "make it a little more formal",
    "make it a little more conversational, in plain everyday words",
    "put a dash or a semicolon after Statement {N} instead of a comma",
    "refer back to Statement {N} with 'this statement' instead of 'it'",
    "open with a phrase that says the reader is comparing or looking at the statements",
)
COMVE_SHAPE = (
    "Every question must have this shape: a short opening phrase that refers to the statements the reader sees "
    "without counting them (for example 'Of the statements shown' or 'Looking at the pair of statements'), then a "
    "colon, then the words Statement {N} right after the colon, then the rest of the question in lowercase letters, "
    "which refers back to Statement {N} with 'it' or 'this statement' and asks whether it goes against common sense. "
    "Shape example for a different question (never copy it): 'Of the cards on the table: Card {N}, is it red?'")
COMVE_COUNT = ("The item's question says 'these two statements'. Never write 'two', and never any other counting word "
               "(one, both, either, each): call them the statements shown, given or listed, or the pair of "
               "statements.")
COMVE_SLOT = ("{N} stands for the number of the statement being asked about. Write it only as 'Statement {N}' "
              "(capital S), exactly once, right after the colon. Ask about Statement {N} itself, never about the "
              "other statement, and never start the question with the word Statement.")
DIRECT_RULE_OPTION = ("Ask the question directly: do not open with a phrase that asks whether a statement holds, do not "
                      "ask whether something is the answer, and do not ask for an opinion.")
LEAST_RULE = ("The item's question says 'at least one'. Keep that meaning, but write it as 'at least a single' "
              "(for example 'at least a single {noun}'): keep the word 'least' exactly once and never write the word "
              "'one' anywhere. Never put 'any', 'some', 'one or more' or a digit in its place: a program throws away "
              "every such question.")
LEAST_NOUN = {"gd_multiwoz21_sysacts/match": "option", "gd_nhtsa_complaints/injury": "person"}
FINAL_RULE = ("The item's question says 'the assistant's last message': the final message the assistant sent in the "
              "conversation. Keep that meaning, but write it as 'the assistant's final message', 'the assistant's "
              "latest message' or 'the final message from the assistant'. Never write the word 'last', and never "
              "'most recent' or 'previous': a program throws away every such question.")


def entry(key: str):
    return SRC.ENTRY_BY_KEY[key]


def v1_admitted() -> list:
    """The frozen v1 pool records (pools/t37b_equiv_pool.json through author_pool.load_pool: frozen, G0, 2/2 reads)."""
    return AP.load_pool(V1_POOL).paraphrases


def taken(key: str) -> list:
    return sorted(r["template"] for r in v1_admitted() if r["sem"] == key)


def _hints(key: str, g: int) -> list:
    if key == "gd_comve/against":
        return [COMVE_HINTS[(g * 3 + i) % len(COMVE_HINTS)] for i in range(PER_ITEM)]
    return [AP.STYLE_HINTS[(g * 4 + i) % len(AP.STYLE_HINTS)] for i in range(PER_ITEM)]


def rules_r2(key: str, g: int) -> list:
    """The closed rules of one redo2 authoring item (the v1 rule kinds, with the B1 / B2 / B3 fixes)."""
    e = entry(key)
    _tpl, slots = SRC.pool_template(e)
    rules = [f"Write {PER_ITEM} questions; question i follows style hint i: "
             + "; ".join(f"({i + 1}) {h}" for i, h in enumerate(_hints(key, g))) + ".", SAME_RULE,
             DIRECT_RULE_OPTION if key == "gd_multiwoz21_sysacts/match" else DIRECT_RULE]
    if key == "gd_comve/against":
        rules += [COMVE_SHAPE, COMVE_COUNT]
    elif key in LEAST_NOUN:
        rules.append(LEAST_RULE.replace("{noun}", LEAST_NOUN[key]))
    elif key == "gd_taskmaster1/status":
        rules.append(FINAL_RULE)
    kw = AP.keep_words(e)
    if kw:
        rules.append("Keep each of these words, exactly as many times as in the question: " + ", ".join(kw) + ".")
    rules.append("Do not use any of these words or phrases: " + ", ".join(AP.banned_words(e)) + "; and do not add "
                 "any other negative word.")
    rules.append(WORDS_RULE)
    if "N" in slots:
        rules.append("Use a capital letter only for the first word of the question and for the word Statement right "
                     "after the colon. Do not use digits.")
    else:
        rules.append("Use a capital letter only for the first word of the question. Do not use digits.")
    if slots:
        rules.append("Use each placeholder exactly once, written exactly as shown, and do not use any other "
                     "placeholder: " + ", ".join("{" + s + "}" for s in sorted(slots)) + ".")
        rules += [COMVE_SLOT if s == "N" else AP.SLOT_TEXT[s] for s in sorted(slots)]
    tk = taken(key)
    if tk:
        rules.append("Already taken (never repeat these): " + " | ".join(tk))
    return rules


def author_items() -> tuple:
    """([(internal id, author_wording item)], plan {internal id: {...}}): new ids, never a v1 id."""
    items, plan = [], {}
    for key, n, blocker, need in PLAN:
        tpl, slots = SRC.pool_template(entry(key))
        for g in range(n):
            iid = f"t37b-r2|{key}|g{g}"
            brief = ("Question template: " if slots else "Question: ") + tpl
            items.append((iid, {"brief": brief, "slots": sorted(slots), "rules": rules_r2(key, g)}))
            plan[iid] = {"entry": key, "group": g, "blocker": blocker, "need": need, "hints": _hints(key, g)}
    return items, plan


def author_batch():
    items, _plan = author_items()
    return chunker.make_batch("author_wording", FAMILY, items, seed=SEED, prompt=REDO2_PROMPT, max_items=CHUNK,
                              forbid_strings=AP.FORBID)


# ------------------------------------------------------------------------------------------------ task files
CONTRACT = {
    "author_wording": ('"questions"', f"a JSON list of exactly {PER_ITEM} strings: the new questions, each one line "
                                      "ending with a question mark, in the order of the item's style hints",
                       '["<question 1>?", "<question 2>?", "<question 3>?", "<question 4>?", "<question 5>?"]'),
    "polarity": ('"relation"', 'exactly one of the strings "same", "opposite" or "unclear"', '"<same | opposite | '
                 'unclear>"'),
}


def task_text(b, chunk: dict, root: Path, title: str) -> str:
    tid = chunk["task_id"]
    n = len(chunk["items"])
    qids = [it["qid"] for it in chunk["items"]]
    key, what, shape = CONTRACT[b.kind]
    return "\n".join([
        f"# {title} {tid} (family {FAMILY}, kind {b.kind})", "",
        "ANSWER FILE (write your whole answer here, and nowhere else, with the Write tool):",
        str(root / b.answer_path(tid)), "",
        "This file is self-contained: the instructions, the answer contract and the items are all below. Read this "
        "whole file. Do not open, list or search any other file or folder.", "",
        "ANSWER CONTRACT (exact; a program checks it):",
        f"- The answer file holds one JSON array with exactly {n} objects: one per item below, each item answered "
        "once, in any order.",
        f'- Each object has exactly two keys: "qid" and {key}. Nothing else.',
        "- \"qid\": copy the item's qid exactly, character for character (the letter q followed by ten letters or "
        f"digits, 11 characters in all). The qids of this task: {', '.join(qids)}.",
        f"- {key}: {what}.",
        "- Valid JSON only: nothing before or after the array, without markdown code fences or comments. Inside "
        'JSON strings write a double quote as \\".',
        f'Literal example of the shape (the qid shown is the first real one): [{{"qid": "{qids[0]}", {key}: '
        f"{shape}}}, ...]", "",
        f"Task kind: {b.kind}; items: {n}.", "",
        "## Instructions", "", b.prompt.rstrip(), "",
        f"## Items ({n}; answer every item, keyed by its qid)", "", "```json",
        json.dumps(chunk["items"], ensure_ascii=False, indent=1), "```", ""])


def batch_files(b, root: Path, *, title: str, kind_label: str, extra: dict | None = None) -> tuple:
    """({relative path: text}, task rows) for one batch written under root."""
    files, rows = dict(b.files()), []
    for c in b.chunks:
        tid = c["task_id"]
        rel = f"tasks/{tid}.md"
        text = task_text(b, c, root, title)
        files[rel] = text
        ans = str(root / b.answer_path(tid))
        rows.append({"task_id": tid, "kind": kind_label, "task_file": str(root / rel), "answer_file": ans,
                     "batch_id": b.batch_id, "prompt_sha": b.prompt_sha,
                     "task_sha256": hashlib.sha256(text.encode()).hexdigest(), "n_items": len(c["items"]),
                     **({k: v(c) for k, v in (extra or {}).items()}),
                     "allowed_read": sorted({str(root / rel)} | b.allowed(str(root), tid)[0]),
                     "allowed_write": [ans]})
    return files, rows


def author_files(root: Path = ROOT) -> tuple:
    """({relative path: text}, TASKS.json object) of the author stage."""
    b = author_batch()
    _items, plan = author_items()
    files, rows = batch_files(b, root, title="T37b redo2 authoring task", kind_label="author_wording:equiv_pool_r2",
                              extra={"outputs_expected": lambda c: len(c["items"]) * PER_ITEM,
                                     "entries": lambda c: dict(sorted(Counter(plan[b.key[it["qid"]]]["entry"]
                                                                               for it in c["items"]).items()))})
    files[f"plan/{b.batch_id}.json"] = json.dumps({"batch_id": b.batch_id, "plan": plan}, indent=1,
                                                  sort_keys=True) + "\n"
    index = {
        "family": FAMILY, "version": VERSION, "seed": SEED, "stage": "redo2 author (design-level pool blockers B1-B3)",
        "g0_sha256": BL.G0_SHA256, "g0_changed": False, "v1_pool_sha256": V1_POOL_SHA256,
        "batch_id": b.batch_id, "prompt_sha": b.prompt_sha, "n_tasks": len(rows), "n_items": len(b.key),
        "outputs_expected": len(b.key) * PER_ITEM,
        "entries": {k: {"items": n, "questions": n * PER_ITEM, "blocker": bl, "need": need,
                        "target_G0": AP.TARGET_SLOTTED if SRC.pool_template(entry(k))[1] else AP.TARGET_FIXED}
                    for k, n, bl, need in PLAN},
        "notes": [
            "New items, new opaque ids, new answer paths; no v1 task, answer, key, candidate, read or pool is reused "
            "or changed. G0_LITE_T37B.md, author_pool.py, gsl_pool_lint.py and builder.py are unchanged.",
            "Each task file is self-contained (answer path, inline answer contract, prompt, items). The agent reads "
            "only its task file and writes only its answer file; audit each agent with audit.audit_jsonl("
            "allowed_read, allowed_write) before its answers count.",
            "Gates unchanged: author_pool.lint_one, gsl_pool_lint.gsl_check (no NAME_ALLOW, no exception), v1 dedup, "
            "two independent polarity reads, author_pool.admit (2/2 'same').",
            "key/ and plan/ are orchestrator only. Next: build_redo2.py extract --write, then admit --write.",
            "Labels: none. Haiku writes paraphrase templates only; equiv gold = the base's human gold (G0 S5)."],
        "tasks": rows}
    files["TASKS.json"] = json.dumps(index, ensure_ascii=False, indent=1) + "\n"
    files["answers/README.txt"] = ("Haiku answer files: one <task_id>.json per redo2 authoring task (see ../TASKS.json). "
                                   "Written only by the task agents.\n")
    return files, index


# Probe inputs of check_author (never an answer file, never admitted): the v1 failure modes must still fail the
# unchanged gate, and the redo2 rules' required forms must pass it.
V1_FAILS = {"gd_comve/against": "Of these two statements, is Statement {N} at odds with common sense?",
            "gd_multiwoz21_sysacts/match": "Did the assistant, in its reply, find at least one option that meets "
                                           "everything the customer asked for?",
            "gd_nhtsa_complaints/injury": "Does this vehicle safety complaint state that at least one person was "
                                          "actually injured?",
            "gd_taskmaster1/status": "Per the assistant's last message, is {SPAN} confirmed for {ORDER}?"}
R2_FORMS = {"gd_comve/against": "Of the statements shown: Statement {N}, does it go against common sense?",
            "gd_multiwoz21_sysacts/match": "In its reply, did the assistant find at least a single option that meets "
                                           "everything the customer asked for?",
            "gd_nhtsa_complaints/injury": "Does this vehicle safety complaint report that at least a single person "
                                          "was actually injured?",
            "gd_taskmaster1/status": "According to the assistant's final message, is {SPAN} confirmed for {ORDER}?"}


def gate(key: str, text: str) -> list:
    """The unchanged v1 gate on one paraphrase: author_pool.lint_one, then gsl_pool_lint.gsl_check."""
    probs = AP.lint_one(entry(key), text)
    if probs:
        return probs
    return [f"G-SL {v.rule}: {v.detail}" for v in GL.gsl_check(AP.record(key, text, "probe", "0" * 64))]


def check_author(files: dict, index: dict, root: Path = ROOT) -> list:
    """Problems with the author tasks (empty = ready): leaks, ids, paths, fields, counts and the three fixes."""
    probs = []
    b = author_batch()
    for c in b.chunks:
        tid = c["task_id"]
        text = files[f"tasks/{tid}.md"]
        low = text.lower()
        for f in AP.FORBID:
            if f and re.search(r"(?<![a-z0-9])" + re.escape(f.lower()) + r"(?![a-z0-9])", low):
                probs.append(f"{tid}: task text holds forbidden string {f!r}")
        if any(i in text for i in b.key.values()):
            probs.append(f"{tid}: internal id in the task text")
        if not 1 <= len(c["items"]) <= min(CHUNK, chunker.MAX_ITEMS):
            probs.append(f"{tid}: {len(c['items'])} items")
        if str(root / b.answer_path(tid)) not in text or "ANSWER CONTRACT" not in text:
            probs.append(f"{tid}: answer path or contract missing")
        for it in c["items"]:
            if set(it) - {"qid"} != set(chunker.TASK_KINDS[b.kind]):
                probs.append(f"{tid}: item fields {sorted(it)}")
        for pth in (root / f"tasks/{tid}.md", root / b.answer_path(tid)):
            if paths.never_open(pth):
                probs.append(f"{tid}: never-open path {pth}")
    for key, _n, _b, _need in PLAN:
        if not gate(key, V1_FAILS[key]):
            probs.append(f"{key}: the v1 failure mode now passes the gate (gate or diagnosis changed)")
        if gate(key, R2_FORMS[key]):
            probs.append(f"{key}: the redo2 required form fails the gate: {gate(key, R2_FORMS[key])}")
    if not gate("gd_comve/against", "Of the statements shown, does Statement {N} go against common sense?"):
        probs.append("comve: a mid-sentence 'Statement' now passes G-SL (gate changed)")
    if index["outputs_expected"] != sum(n for _k, n, _b, _x in PLAN) * PER_ITEM:
        probs.append("output count")
    if hashlib.sha256(V1_POOL.read_bytes()).hexdigest() != V1_POOL_SHA256:
        probs.append("the frozen v1 pool changed")
    if BL.g0_problems():
        probs.append(f"G0: {BL.g0_problems()}")
    return probs


def check_on_disk(root: Path, files: dict) -> list:
    return [rel for rel, text in sorted(files.items())
            if not (root / rel).is_file() or (root / rel).read_text(encoding="utf-8") != text]


# ------------------------------------------------------------------------------------------------ extract stage
def _read_json(p: Path, what: str):
    if paths.never_open(p):
        raise SystemExit(f"STOP: never-open path {p}")
    if not p.is_file():
        raise SystemExit(f"STOP: {what} missing: {p}")
    try:
        return json.loads(p.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, UnicodeDecodeError) as e:
        raise SystemExit(f"STOP: {what} is not JSON: {p}: {e}")


def load_batch_answers(b, root: Path, what: str) -> tuple:
    """({internal id: answer}, load problems) for one batch; stops if an answer file is missing."""
    raw = {c["task_id"]: _read_json(root / b.answer_path(c["task_id"]), what) for c in b.chunks}
    return chunker.load_answers(b, raw)


def v1_seen() -> dict:
    """{entry key: normalised texts}: every v1 author text (admitted, dropped or duplicate) and the v1 pool."""
    out: dict = {}
    vb = AP.author_batch()
    ans, _p = chunker.load_answers(vb, AP._read_answers(AP.AUTHOR_DIR, vb))
    for iid, a in ans.items():
        out.setdefault(iid.split("|")[1], set()).update(AP.norm(q) for q in AP._questions(a))
    for r in v1_admitted():
        out.setdefault(r["sem"], set()).add(AP.norm(r["template"]))
    return out


def lint_r2(b, plan: dict, answers: dict, seen_v1: dict) -> tuple:
    """(candidates, gsl drops, report): the unchanged v1 gate on every redo2 question, then dedup (v1 and redo2)."""
    qid_of = {v: q for q, v in b.key.items()}
    cands, gdrops, drops = [], [], Counter()
    seen, pairs, per = set(), set(), Counter()
    n_q = 0
    for iid in sorted(answers):
        key = plan[iid]["entry"]
        tid = b.task_of[qid_of[iid]]
        qs = AP._questions(answers[iid])
        n_q += len(qs)
        for k, q in enumerate(qs):
            probs = AP.lint_one(entry(key), q)
            if probs:
                drops[probs[0].split(":")[0][:60]] += 1
                continue
            nq = AP.norm(q)
            if nq in seen_v1.get(key, set()):
                drops["duplicate of a v1 text"] += 1
                continue
            if (key, nq) in seen:
                drops["duplicate"] += 1
                continue
            seen.add((key, nq))
            rec = AP.record(key, q, tid, b.prompt_sha) | {"author_item": iid, "k": k}
            viol = GL.gsl_check(rec)
            if viol:
                drops["G-SL"] += 1
                gdrops.append({"sem": key, "template": q, "author_item": iid, "haiku_task_id": tid,
                               "gsl": sorted({f"{x.rule}: {x.detail}" for x in viol})})
                continue
            pk = AP.rec_pair_key(rec)
            if pk in pairs:
                drops["duplicate pair key"] += 1
                continue
            pairs.add(pk)
            cands.append(rec)
            per[key] += 1
    rep = {"answered_items": len(answers), "items": len(b.key), "questions": n_q, "passed": len(cands),
           "dropped": dict(drops.most_common()), "passed_by_entry": dict(sorted(per.items())),
           "gsl_dropped_by_rule": dict(Counter(g.split(":")[0] for d in gdrops for g in d["gsl"]).most_common())}
    return cands, gdrops, rep


def polarity_batches(cands: list) -> tuple:
    """Two independent reads of each (base template, paraphrase) pair: own seeds, orders, ids and chunks (G0 H41)."""
    items = [(AP.rec_pair_key(c), {"question_a": AP.base_template(c), "question_b": c["template"]}) for c in cands]
    if not items:
        return None, None
    return tuple(chunker.make_batch("polarity", FAMILY, items, seed=f"{SEED_POL}|{lab}", prompt=AP.POOL_POLARITY_PROMPT,
                                    max_items=AP.POL_CHUNK) for lab in ("A", "B"))


def extract_files() -> tuple:
    """(lint files {path: text}, extract files {rel: text}, report). Stops unless every author answer is there."""
    files, _index = author_files()
    bad = check_on_disk(ROOT, {k: v for k, v in files.items() if not k.startswith("answers/")})
    if bad:
        raise SystemExit(f"STOP: author files on disk differ from the rebuild: {bad[:3]}")
    b = author_batch()
    _items, plan = author_items()
    answers, load_probs = load_batch_answers(b, ROOT, "redo2 author answer")
    cands, gdrops, rep = lint_r2(b, plan, answers, v1_seen())
    rep["load_problems"] = load_probs
    pa, pb = polarity_batches(cands)
    if pa is None:
        raise SystemExit(f"STOP: no redo2 paraphrase passed the gate: {rep}")
    xfiles, rows = {}, []
    for lab, bt in (("A", pa), ("B", pb)):
        f, r = batch_files(bt, EX_ROOT, title=f"T37b redo2 polarity read {lab}", kind_label=f"polarity:{lab}")
        xfiles.update(f)
        rows += r
    xman = {"family": FAMILY, "version": VERSION, "stage": "redo2 extract (two independent polarity reads; G0 H41)",
            "seed": SEED_POL, "g0_sha256": BL.G0_SHA256, "author_batch_id": b.batch_id, "n_tasks": len(rows),
            "n_pairs": len(cands), "batch_ids": [pa.batch_id, pb.batch_id], "next": "build_redo2.py admit --write",
            "tasks": rows}
    xfiles["TASKS.json"] = json.dumps(xman, indent=1, ensure_ascii=False) + "\n"
    xfiles["answers/README.txt"] = "Polarity read answers: one <task_id>.json per task (see ../TASKS.json).\n"
    lfiles = {"candidates.json": json.dumps({"family": FAMILY, "version": VERSION, "candidates": cands},
                                            ensure_ascii=False, indent=1) + "\n",
              "report.json": json.dumps(rep, ensure_ascii=False, indent=1) + "\n",
              "gsl_drops.json": json.dumps({"family": FAMILY, "g0_sha256": BL.G0_SHA256, "drops": gdrops},
                                           ensure_ascii=False, indent=1) + "\n"}
    return lfiles, xfiles, rep | {"polarity_tasks": len(rows), "polarity_batch_ids": [pa.batch_id, pb.batch_id]}


# ------------------------------------------------------------------------------------------------ admit stage
def admit_files() -> tuple:
    """({path: text} of the supplement pool, manifest). Stops unless the extract files match and every read is in."""
    lfiles, xfiles, _rep = extract_files()
    bad = check_on_disk(LINT_DIR, lfiles) + check_on_disk(EX_ROOT, {k: v for k, v in xfiles.items()
                                                                    if not k.startswith("answers/")})
    if bad:
        raise SystemExit(f"STOP: extract files on disk differ from the rebuild: {bad[:3]}")
    cands = json.loads(lfiles["candidates.json"])["candidates"]
    pa, pb = polarity_batches(cands)
    got_a, probs_a = load_batch_answers(pa, EX_ROOT, "polarity read A answer")
    got_b, probs_b = load_batch_answers(pb, EX_ROOT, "polarity read B answer")
    admitted, rep = AP.admit(cands, got_a, got_b)
    v1 = Counter(r["sem"] for r in v1_admitted())
    r2 = Counter(r["sem"] for r in admitted)
    targets = rep["targets"]
    merged = {k: v1[k] + r2[k] for k in targets}
    quarantine = [{"reason": "reads not both 'same'", "sem": c["sem"], "template": c["template"],
                   "haiku_task_id": c["haiku_task_id"], "author_item": c["author_item"],
                   "pair_key": AP.rec_pair_key(c),
                   "reads": [BL.norm_relation(got_a.get(AP.rec_pair_key(c))),
                             BL.norm_relation(got_b.get(AP.rec_pair_key(c)))]}
                  for c in cands if c["template_id"] not in {a["template_id"] for a in admitted}]
    pool = {"family": FAMILY, "version": VERSION, "g0_sha256": BL.G0_SHA256, "frozen": True,
            "supplement_of": V1_POOL_SHA256, "paraphrases": sorted(admitted, key=lambda c: (c["sem"],
                                                                                            c["template_id"]))}
    body = json.dumps(pool, indent=1, ensure_ascii=False, sort_keys=True) + "\n"
    man = {"family": FAMILY, "version": VERSION, "pool_file": SUPP_POOL.name, "sha256": hashlib.sha256(
        body.encode()).hexdigest(), "supplement_of": {"file": V1_POOL.name, "sha256": V1_POOL_SHA256},
        "g0_sha256": BL.G0_SHA256, "author_batch_id": author_batch().batch_id,
        "polarity_batch_ids": [pa.batch_id, pb.batch_id], "admission_rule": "both independent reads 'same' (2/2)",
        "report": {"candidates": rep["candidates"], "admitted": rep["admitted"], "dropped": rep["dropped"],
                   "load_problems": {"A": probs_a, "B": probs_b}, "redo2_by_entry": dict(sorted(r2.items())),
                   "v1_by_entry": dict(sorted(v1.items())), "merged_by_entry": dict(sorted(merged.items())),
                   "targets": targets, "merged_shortfall": {k: t - merged[k] for k, t in targets.items()
                                                            if merged[k] < t},
                   "note": "targets are never lowered; a shortfall lowers the equiv block (S14), never refilled"},
        "loader": "build_redo2.load_merged_pool() (v1 pool + this supplement, both verified)"}
    files = {SUPP_POOL.name: body, "MANIFEST.json": json.dumps(man, indent=1, ensure_ascii=False) + "\n",
             "QUARANTINE.json": json.dumps({"family": FAMILY, "version": VERSION, "admit_drops": quarantine},
                                           indent=1, ensure_ascii=False) + "\n"}
    return files, man


def load_merged_pool(v1_path: Path = V1_POOL, supp_path: Path = SUPP_POOL) -> AP.Pool:
    """The v1 pool plus the redo2 supplement (when frozen): both under the current G0, every record 2/2 'same', the
    supplement tied to the exact v1 pool bytes, no template id or (entry, text) twice. Without a supplement: v1."""
    v1 = AP.load_pool(v1_path)
    if not Path(supp_path).is_file():
        return v1
    if hashlib.sha256(Path(v1_path).read_bytes()).hexdigest() != V1_POOL_SHA256:
        raise RuntimeError("the v1 pool is not the one the redo2 supplement was built on")
    supp = AP.load_pool(supp_path)
    obj = json.loads(Path(supp_path).read_text(encoding="utf-8"))
    if obj.get("supplement_of") != V1_POOL_SHA256:
        raise RuntimeError("the redo2 supplement does not name the frozen v1 pool")
    ids = [c["template_id"] for c in v1.paraphrases + supp.paraphrases]
    texts = [(c["sem"], AP.norm(c["template"])) for c in v1.paraphrases + supp.paraphrases]
    if len(set(ids)) != len(ids) or len(set(texts)) != len(texts):
        raise RuntimeError("the redo2 supplement repeats a v1 paraphrase")
    return AP.Pool(v1.paraphrases + supp.paraphrases)


def template_strings_r2() -> dict:
    """Claude-written redo2 strings for the G13 seed-first method-8 check (as builder.template_strings)."""
    items, _plan = author_items()
    return {"prompts": [REDO2_PROMPT], "rules": sorted({r for _i, it in items for r in it["rules"]})}


# ------------------------------------------------------------------------------------------------ main
def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("stage", choices=("author", "extract", "admit"))
    ap.add_argument("--write", action="store_true")
    a = ap.parse_args(argv)
    paths.require_a38()
    BL.require_g0()
    if a.stage == "author":
        files, index = author_files()
        probs = check_author(files, index)
        out = {"problems": probs, "batch_id": index["batch_id"], "n_tasks": index["n_tasks"],
               "n_items": index["n_items"], "outputs_expected": index["outputs_expected"],
               "tasks": [{k: r[k] for k in ("task_file", "answer_file", "n_items", "outputs_expected")}
                         for r in index["tasks"]]}
        if a.write and not probs:
            paths.write_files(ROOT, files)
            out["written"] = len(files)
    elif a.stage == "extract":
        lfiles, xfiles, out = extract_files()
        if a.write:
            paths.write_files(LINT_DIR, lfiles)
            paths.write_files(EX_ROOT, xfiles)
            out["written"] = len(lfiles) + len(xfiles)
    else:
        files, man = admit_files()
        out = man["report"] | {"sha256": man["sha256"]}
        if a.write:
            paths.write_files(SUPP, files)
            out["written"] = sorted(files)
    print(json.dumps(out, indent=1, ensure_ascii=False, default=str))
    return 1 if out.get("problems") else 0


if __name__ == "__main__":
    raise SystemExit(main())
