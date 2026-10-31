"""families/T33/redo2.py: the T33 lead redo2 after the Stage-A lint (G0_SPEC section 7, blockers B1-B6; A37 b).

Nothing here loosens a gate, changes a gold or touches a label; Haiku answers only flag (G-LEX: any other pick
rejects a form for good). The decisions, recorded in G0_SPEC section 7:
  B1-B3  claim and check clauses get the kit's lint role for G-LEX-admitted lexicon text, "wording", plus the
         gold-label words (haiku_extract_run.clause_lint). Clauses the first run dropped and that now pass are read.
  B2     crit.max_duration: every authored form said "last" (CORE relative time): re-authored here ("final poll").
  B4     bulk claims (import, export, sync): "{V} rows" breaks G-SL grammar; re-authored here, naming rows elsewhere.
  B5     question meanings no longer quote verdict strings (haiku_author.QUESTION_SEMS); the FORBID screen is the
         same, so a question form whose own text holds a program string stays held.
  B6     read items show realistic values (read_item), never the kit's sample values ($0.00, "1 day").
The 6 round-1 reads (haiku/extract batches; answers in haiku/redo) stand unchanged; their forms are not re-sent.

Stages (run from lean/c2_build; every write goes through paths.write_files, which refuses before A38):
  ../../.venv/bin/python -m families.T33.redo2 build [--write]        authoring tasks + reads of the released forms
  ../../.venv/bin/python -m families.T33.redo2 extract-new [--write]  after the authoring answers: reads of new forms
  ../../.venv/bin/python -m families.T33.redo2 admit [--write]        record every read, then freeze pools/
Every task file is self-contained (haiku/redo2/tasks/<task_id>.txt): its instructions, items, answer contract and the
one absolute answer path. One fresh agent per task; audit with c2_kit.audit (read: the task file only; write: its
answer file); a failed audit deletes that answer file before the next stage.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import random
import sys
from collections import Counter
from pathlib import Path

from c2_kit import chunker, paths
from c2_kit import slots as S
from c2_kit.lexicon import LexiconError
from c2_kit.skin import RenderError

from . import haiku_author as H
from . import haiku_extract_run as XR
from . import plugin as T

F = H.F
VERSION = "redo2"
R2 = H.HAIKU / "redo2"
AUTH = R2 / "author"
READ = R2 / "read"
READ_NEW = R2 / "read_new"
TASKS_DIR = R2 / "tasks"
LINT = R2 / "lint"
CLAUSE_KINDS = XR.CLAUSE_KINDS
N_READS = 2                      # every T33 form: kinds status, other, question (no precedence or window form)

# ------------------------------------------------------------------------------------------------ authoring (B2, B4)
BULK_VERBS = ("import", "export", "sync")
BULK_ITEMS_PER_VERB = 4          # 24 forms per verb asked (target 6 admitted)
DUR_ITEMS = 5                    # 30 forms asked (target 9 admitted)
AFTER_COUNT = "of, in, into, to, from, for, on, at, by, with, as, and, or"
EXTRA = ("Write no digits, no number words (one, first, second, half ...), no time words (last, next, now, already, "
         "earlier, later ...), no hedges (maybe, probably, roughly, nearly ...) and no $ or % signs. Start with a "
         "lower-case word, a placeholder or the word I, and capitalise nothing else. Never write the word a or an "
         "directly before a {SLOT}. Follow each item's brief exactly.")
PROMPTS = {"claims": H.PROMPTS["claims"] + " " + EXTRA, "checks": H.PROMPTS["checks"] + " " + EXTRA}
BULK_SHAPES = (
    "name the rows with a phrase such as 'a row count of {V}' or 'rows numbering {V}'",
    "end the clause with {V}, after a phrase that names the rows (for example 'the rows ... came to {V}')",
    "start the clause with I and name the rows before {V}",
    "any shape that keeps every rule above, different from the shapes 'a row count of {V}' and '... came to {V}'",
)
DUR_ANGLES = ("start with duration_ms", "start with the job's final poll", "say latest poll instead of final poll",
              "end the phrasing with {D}", "keep each phrasing short (at most eight words)")
DUR_MEANING = ("the duration_ms on the job's final poll is at most the stated number of seconds; exactly that number "
               "still passes")


def author_items() -> dict:
    """{"claims": [(iid, item)], "checks": [(iid, item)]}. Internal ids keep haiku_author's layout, so
    haiku_author._load_one reads them (parts[2] = verb or sem)."""
    claims = []
    for verb in BULK_VERBS:
        meaning = H.CLAIM_SEMS[verb]
        for j in range(BULK_ITEMS_PER_VERB):
            style = ("first person (I ...)", "a passive or neutral clause about the target")[j % 2]
            brief = (f"Write {H.FORMS_PER_ITEM} different clause templates in which the agent states that it did "
                     f"this: {meaning.replace('the agent says it ', '')}. Use {{V}} and {{T}} exactly once each, and "
                     "name the rows with the word rows (or row) once. {V} is a bare row count such as 4,800 that the "
                     f"program writes; the word right after {{V}} may only be one of: {AFTER_COUNT}; or {{V}} ends "
                     "the clause. So never put rows, or any other noun or verb, right after {V}. Shape: "
                     f"{BULK_SHAPES[j]}. Style: {style}. Use the specific verb or noun for this action (this action "
                     f"is the {verb} itself, not any other kind).")
            claims.append((f"t33|claim|{verb}|r2-{j}", {
                "brief": brief, "meaning": meaning,
                "slots": {"T": "the target id, such as a dataset id",
                          "V": "a bare row count such as 4,800 (the program writes it; no unit)"},
                "rules": ["one clause, no comma or semicolon", "at most fourteen words", "no full stop at the end",
                          "the word rows (or row) once, never right after {V}",
                          f"the word right after {{V}} is one of: {AFTER_COUNT}; or {{V}} ends the clause"]}))
    checks = []
    for j in range(DUR_ITEMS):
        brief = (f"Write {H.FORMS_PER_ITEM} different phrasings of this check: the duration_ms on the job's final "
                 "poll is at most {D}. The stated number itself passes, so use an inclusive phrase such as at most, "
                 "no more than, up to or within (never less than, under or below). Name the job's final poll (or "
                 "its latest poll) or that poll's duration_ms, and never use the word last. {D} already includes "
                 "its unit (for example 45 seconds): never write seconds after it; the word right after {D} may only "
                 "be one of: of, in, on, for, at, by, with, from, to, and, or; or {D} ends the phrasing. Use {D} "
                 f"exactly once. Angle: {DUR_ANGLES[j]}.")
        checks.append((f"t33|check|crit.max_duration|r2-{j}", {
            "brief": brief, "meaning": DUR_MEANING, "slots": {"D": "a number of seconds with its unit"},
            "rules": ["lower-case clause, no full stop", "at most fourteen words", "never the word last"]}))
    return {"claims": claims, "checks": checks}


def author_batches() -> list:
    out = []
    for name, items in author_items().items():
        b = chunker.make_batch("author_lexicon", F, items, seed=f"{F}-author-{VERSION}-{name}", prompt=PROMPTS[name],
                               max_items=chunker.MAX_ITEMS, forbid_strings=H.FORBID)
        for c in b.chunks:
            c["instructions"] = PROMPTS[name]
            c["answer_format"] = H.ANSWER_TEXTS
            c["answer_file"] = str(AUTH / b.answer_path(c["task_id"]))
        out.append((name, b))
    return out


# ------------------------------------------------------------------------------------------------ read items (B6)
TARGET_KIND = {"refund": "order", "charge": "account", "credit": "account", "payout": "vendor", "import": "dataset",
               "export": "dataset", "sync": "dataset", "send": "contact", "book": "booking", "cancel": "booking",
               "update": "record"}
MONEY = (4800, 12599, 250000, 7350, 31000)          # G0 S4: $5-$2,500
ROWS = (4800, 1250, 360, 23170, 9940)               # G0 S4: 120-47,990, multiples of 10
TRIES = (2, 3, 4)                                   # G0 S2: R_MAX 1-5
SECONDS = (45, 90, 120, 30)                         # G0 S2: D_MAX 1-265
STEPS = (2, 3, 4)


def _sha(s: str) -> str:
    return hashlib.sha256(s.encode()).hexdigest()


def item_values(f) -> tuple:
    """({slot: Slot}, {slot: form}) with values a T33 row could show (label-blind: seeded by the form id only)."""
    rng = random.Random(int(_sha(f"{F}|{VERSION}|values|{f.form_id}"), 16))
    vals, forms = {}, {}
    for name, kind in f.slots:
        if name == "T":
            vals[name] = S.id_slot(T.TARGET_MAKERS[TARGET_KIND[f.sem_id.split(".", 1)[1]]](rng))
        elif name == "TARGET":
            vals[name] = S.id_slot(T.TARGET_MAKERS[rng.choice(("order", "account", "booking", "dataset"))](rng))
        elif name == "V" and kind == "cents":
            vals[name] = S.cents_slot(rng.choice(MONEY))
            forms[name] = rng.choice(S.free_forms(vals[name]))
        elif name == "V" and kind == "count":
            vals[name], forms[name] = S.count_slot(rng.choice(ROWS)), "digits"
        elif name == "R":
            vals[name], forms[name] = S.count_slot(rng.choice(TRIES), T.TRY_UNIT), "digits"
        elif name == "D":
            vals[name], forms[name] = S.count_slot(rng.choice(SECONDS), T.SECOND_UNIT), "digits"
        elif name == "STEP":
            vals[name], forms[name] = S.count_slot(rng.choice(STEPS)), "digits"
        else:
            raise ValueError(f"{f.form_id}: no realistic value for slot {name} ({kind})")
    return vals, forms


def read_item(reg, fid: str, seed: str) -> dict:
    """The G-LEX item of one form (the kit's lexicon_items layout: text + its kind's meanings in a seeded order), with
    realistic values. Refuses a rendering that does not parse back to the form's own meaning."""
    f = reg.forms[fid]
    vals, forms = item_values(f)
    txt = reg.render(fid, vals, forms)
    sem, _fid, got = reg.parse_exact(txt, {k: v.schema for k, v in vals.items()})
    if sem != f.sem_id or got != {k: v.value for k, v in vals.items()}:
        raise LexiconError(f"{fid}: {txt!r} reads back as {sem} {got}")
    mean = sorted((s.meaning for s in reg.sems.values() if s.kind == f.kind),
                  key=lambda m: _sha(f"{seed}|{fid}|{m}"))
    return {"text": txt, "choices": mean}


def round1_sent() -> set:
    """Form ids already in the round-1 read batches (haiku/extract): never re-sent."""
    p = H.EXTRACT / "TASKS.json"
    if not p.exists():
        return set()
    t = json.loads(p.read_text(encoding="utf-8"))
    return {fid for bid in t["batches"].values() for fid in H.batch_from_disk(H.EXTRACT, bid).key.values()}


def release(reg, candidates) -> dict:
    """G-SL (clauses: XR.clause_lint), the FORBID screen on the item Haiku would read, then the forms to send."""
    drops, held, fids = {}, {}, []
    for fid in sorted(candidates):
        f = reg.forms[fid]
        if not f.unit_ok or reg.status(fid) != "pending":
            continue
        if f.kind in CLAUSE_KINDS:
            v = XR.clause_lint(f)
            if v:
                drops[fid] = {"form_id": fid, "sem_id": f.sem_id, "kind": f.kind, "text": f.text, "rules": v}
                continue
        try:
            it = read_item(reg, fid, seed=f"{F}-glex-{VERSION}-screen")
        except (LexiconError, RenderError, S.SlotError) as e:
            drops[fid] = {"form_id": fid, "sem_id": f.sem_id, "kind": f.kind, "text": f.text,
                          "rules": [f"render: {e}"]}
            continue
        hit_text = XR._forbid_in(it["text"])
        hit_choice = sorted({s for m in it["choices"] for s in XR._forbid_in(m)})
        if hit_text or hit_choice:
            held[fid] = {"form_id": fid, "sem_id": f.sem_id, "kind": f.kind, "rendered_text": it["text"],
                         "forbidden_in_text": hit_text, "forbidden_in_choices": hit_choice}
            continue
        fids.append(fid)
    return {"drops": drops, "held": held, "fids": fids}


def read_batches(reg, fids: list, root: Path, tag: str) -> list:
    """N_READS independent reads, each its own batch, so each read of a form sits in its own chunk file."""
    out = []
    for r in range(N_READS):
        items = [(fid, read_item(reg, fid, seed=f"{F}-glex-{VERSION}-{tag}-r{r}")) for fid in sorted(fids)]
        b = chunker.make_batch("extract_lex", F, items, seed=f"{F}-glex-{VERSION}-{tag}-read{r}",
                               prompt=H.EXTRACT_PROMPT, forbid_strings=H.FORBID)
        for c in b.chunks:
            c["instructions"] = H.EXTRACT_PROMPT
            c["answer_file"] = str(root / b.answer_path(c["task_id"]))
        out.append((f"read{r}", b))
    return out


# ------------------------------------------------------------------------------------------------ task files
_HEAD = ("THIS FILE IS SELF-CONTAINED. Read only this file. Do not open, list, search or run anything else. You may "
         "write exactly\none file: the answer file named below.")


def read_task_text(c: dict, read: str) -> str:
    its = c["items"]
    n = len(its)
    return "\n".join([
        "T33 G-LEX BLIND READ: REDO2 FILE",
        f"task: {c['task_id']}   ({read}, {n} items)",
        "",
        _HEAD + " You are one independent reader. You have not seen, and must not look for, any\nother reader's "
        "answers.",
        "",
        "WHAT TO DO",
        "Each item below has three fields: \"qid\", \"text\" and \"choices\". The \"text\" is a short wording; a "
        "program filled in its\nvalues (amounts, row counts, numbers of tries or seconds, ids, step numbers) as "
        "examples, so judge its wording. The\n\"choices\" are a list of meanings. For every item, pick the ONE "
        "meaning in that item's own \"choices\" list that the\ntext expresses exactly. The choices come in a "
        "different shuffled order for each item, so a choice's position tells\nyou nothing. Pick exactly one choice "
        "for every item. If no choice fits perfectly, pick the closest in meaning; never\nskip an item, never answer "
        "an item twice, never write null or \"none\".",
        "",
        "INSTRUCTIONS OF THE READ (kept word for word)",
        c["instructions"],
        "",
        "ANSWER FILE (write exactly this one path, with the Write tool; the folder is created if it is missing)",
        c["answer_file"],
        "",
        "EXACT ANSWER CONTRACT",
        "1. The file holds ONE JSON array and nothing else: no text before or after it, no markdown code fence, no "
        "comments.",
        f"2. The array has exactly {n} objects, one per item, in the same order as the items below.",
        f"   The first object has qid \"{its[0]['qid']}\" and the last has qid \"{its[-1]['qid']}\".",
        "3. Every object has exactly two keys, \"qid\" and \"choice\", both strings, and no other key:",
        "   \"qid\"    the item's qid, copied exactly (the letter q followed by 10 hex characters).",
        "   \"choice\" ONE of that same item's \"choices\" strings, copied character for character: same words, same "
        "case, same\n            punctuation and semicolons. Do not shorten it, reword it, number it, add a letter, "
        "or join two choices.",
        "4. No qid is missing, repeated or invented. A choice taken from another item's list is wrong even if its "
        "words are\n   identical to a choice of this item; copy it from this item's own list.",
        "",
        "LITERAL EXAMPLE (a toy example with made-up content; it is NOT one of your items and none of its words are "
        "answers)",
        "Example item:",
        '{"qid": "q00example01", "text": "the kettle is switched on", "choices": ["the kettle is switched off", '
        '"the kettle is switched on", "the kettle is being repaired"]}',
        "Example answer file (a complete file for a one-item task):",
        "[",
        ' {"qid": "q00example01", "choice": "the kettle is switched on"}',
        "]",
        f"Your answer file has the same shape, with {n} objects instead of 1.",
        "",
        "CHECK BEFORE YOU FINISH",
        f"- The file parses as JSON and is an array of {n} objects with only the keys \"qid\" and \"choice\".",
        "- The qids appear in the same order as in the items below, each once.",
        "- Each \"choice\" string appears, character for character, in the \"choices\" list of the item with the "
        "same qid.",
        "",
        f"ITEMS ({n}, in this order; the JSON array starts on the next line and runs to the end of the file)",
        json.dumps(its, ensure_ascii=False, indent=1),
    ]) + "\n"


def author_task_text(c: dict) -> str:
    its = c["items"]
    n, k = len(its), H.FORMS_PER_ITEM
    return "\n".join([
        "T33 AUTHORING: REDO2 FILE",
        f"task: {c['task_id']}   ({n} items, {k} texts each)",
        "",
        _HEAD,
        "",
        "INSTRUCTIONS (kept word for word)",
        c["instructions"],
        "",
        "ANSWER FORMAT (kept word for word)",
        c["answer_format"],
        "",
        "ANSWER FILE (write exactly this one path, with the Write tool; the folder is created if it is missing)",
        c["answer_file"],
        "",
        "EXACT ANSWER CONTRACT",
        "1. The file holds ONE JSON array and nothing else: no text before or after it, no markdown code fence, no "
        "comments.",
        f"2. The array has exactly {n} objects, one per item, in the same order as the items below.",
        f"   The first object has qid \"{its[0]['qid']}\" and the last has qid \"{its[-1]['qid']}\".",
        "3. Every object has exactly two keys, \"qid\" and \"texts\", and no other key:",
        "   \"qid\"    the item's qid, copied exactly (the letter q followed by 10 hex characters).",
        f"   \"texts\"  an array of exactly {k} different strings, each one template written as that item's brief "
        "and rules ask,\n            with every placeholder spelled exactly as given (curly braces, upper case).",
        "4. No qid is missing, repeated or invented.",
        "",
        "LITERAL EXAMPLE (a toy example with made-up content; it is NOT one of your items)",
        "Example item:",
        '{"qid": "q00example01", "brief": "Write 2 different clause templates in which the agent states that it '
        'watered the plant {P}. Use {P} exactly once.", "meaning": "the agent says it watered the plant", "slots": '
        '{"P": "the plant id"}, "rules": ["one clause, no comma"]}',
        "Example answer file (a complete file for a one-item task asking for 2 texts):",
        "[",
        ' {"qid": "q00example01", "texts": ["I watered {P}", "{P} was watered"]}',
        "]",
        f"Your answer file has the same shape, with {n} objects of {k} texts each.",
        "",
        "CHECK BEFORE YOU FINISH",
        f"- The file parses as JSON and is an array of {n} objects with only the keys \"qid\" and \"texts\".",
        f"- Each \"texts\" holds {k} different strings that keep their placeholders verbatim and follow the item's "
        "brief and rules.",
        "",
        f"ITEMS ({n}, in this order; the JSON array starts on the next line and runs to the end of the file)",
        json.dumps(its, ensure_ascii=False, indent=1),
    ]) + "\n"


def _forbid_blob(text: str) -> list:
    return XR._forbid_in(text)


# ------------------------------------------------------------------------------------------------ stage: build
def build(pieces: dict | None = None) -> dict:
    pieces = pieces or H.load_pieces()
    reg = pieces["registry"]
    sent1 = round1_sent()
    rel = release(reg, [fid for fid in reg.forms if fid not in sent1])
    reads = read_batches(reg, rel["fids"], READ, "rel")
    auth = author_batches()
    texts, tasks, hits = {}, [], []
    for name, b in auth:
        for c in b.chunks:
            t = author_task_text(c)
            hits += [(c["task_id"], s) for s in _forbid_blob(t)]
            texts[c["task_id"]] = t
            tasks.append({"task_file": str(TASKS_DIR / f"{c['task_id']}.txt"), "answer_file": c["answer_file"],
                          "kind": f"author_lexicon:{name}", "n_items": len(c["items"])})
    for name, b in reads:
        for c in b.chunks:
            t = read_task_text(c, name)
            hits += [(c["task_id"], s) for s in _forbid_blob(json.dumps(c["items"], ensure_ascii=False))]
            texts[c["task_id"]] = t
            tasks.append({"task_file": str(TASKS_DIR / f"{c['task_id']}.txt"), "answer_file": c["answer_file"],
                          "kind": f"extract_lex:{name}", "n_items": len(c["items"])})
    return {"pieces": pieces, "sent_round1": sent1, "release": rel, "reads": reads, "author": auth, "texts": texts,
            "tasks": tasks, "hits": hits}


def ceilings(reg, fids_sent: set) -> dict:
    """Forms per production sem that can still be admitted (sent in some read and not rejected)."""
    c = Counter(reg.forms[f].sem_id for f in fids_sent if reg.status(f) in ("pending", "admitted"))
    out = {}
    for verb in H.CLAIM_SEMS:
        out[f"claim.{verb}"] = c[f"claim.{verb}"]
    for sem in H.TARGETS["check"]:
        out[sem] = c[sem]
    for qf in H.TARGETS["wording"]:
        out[f"wording:{qf}"] = c[H.question_sem(F, qf)]
    return out


def targets() -> dict:
    out = {f"claim.{v}": H.TARGETS["claim_per_verb"] for v in H.CLAIM_SEMS}
    out.update(H.TARGETS["check"])
    out.update({f"wording:{q}": n for q, n in H.TARGETS["wording"].items()})
    return out


def summarise_build(res: dict) -> dict:
    reg = res["pieces"]["registry"]
    rel = res["release"]
    sent = set(res["sent_round1"]) | set(rel["fids"])
    ceil = ceilings(reg, sent)
    want = targets()
    return {
        "family": F, "version": VERSION,
        "forms_in_registry": len(reg.forms),
        "round1_forms_in_haiku_extract": len(res["sent_round1"]),
        "released_forms_sent_now": len(rel["fids"]),
        "released_by_kind": dict(Counter(reg.forms[f].kind for f in rel["fids"])),
        "released_by_sem": dict(sorted(Counter(reg.forms[f].sem_id for f in rel["fids"]).items())),
        "clause_lint_drops": len(rel["drops"]),
        "clause_lint_drops_by_sem": dict(sorted(Counter(d["sem_id"] for d in rel["drops"].values()).items())),
        "forbid_held": len(rel["held"]),
        "forbid_held_by_sem": dict(sorted(Counter(d["sem_id"] for d in rel["held"].values()).items())),
        "forbid_held_in_choices": sum(1 for d in rel["held"].values() if d["forbidden_in_choices"]),
        "read_batches": {n: {"batch_id": b.batch_id, "chunks": len(b.chunks), "items": len(b.key)}
                         for n, b in res["reads"]},
        "author_batches": {n: {"batch_id": b.batch_id, "chunks": len(b.chunks), "items": len(b.key)}
                           for n, b in res["author"]},
        "tasks": len(res["tasks"]),
        "ceiling_before_glex": ceil,
        "still_short_before_reauthoring": {k: f"{ceil[k]} < {want[k]}" for k in want if ceil[k] < want[k]},
        "forbid_hits_in_task_files": res["hits"],
    }


def write_build(res: dict) -> dict:
    if any((d / "answers").exists() and any((d / "answers").iterdir()) for d in (AUTH, READ)):
        raise RuntimeError("redo2 answers exist: the redo2 tasks are not rewritten")
    for root, bs in ((AUTH, res["author"]), (READ, res["reads"])):
        files = {}
        for _n, b in bs:
            files.update(b.files())
        paths.write_files(root, files)
    paths.write_files(TASKS_DIR, {f"{tid}.txt": t for tid, t in res["texts"].items()})
    reg = res["pieces"]["registry"]
    rel = res["release"]
    paths.write_files(LINT, {
        "CLAUSE_LINT_V2.json": json.dumps({
            "family": F, "version": VERSION, "gate": "G-SL role wording + gold-label words (G0 section 7 B1)",
            "scope": "every unit-tested form not in the round-1 reads (haiku/extract)",
            "n_dropped": len(rel["drops"]), "forms": [rel["drops"][k] for k in sorted(rel["drops"])]},
            ensure_ascii=False, indent=1) + "\n",
        "FORBIDDEN_HELD_V2.json": json.dumps({
            "family": F, "version": VERSION,
            "rule": "no read item may carry LABEL_WORDS or a question / option string (haiku_author.FORBID); "
                    "meanings reworded (G0 section 7 B5), screen unchanged",
            "n_held": len(rel["held"]), "forms": [rel["held"][k] for k in sorted(rel["held"])]},
            ensure_ascii=False, indent=1) + "\n"})
    doc = {
        "family": F, "version": VERSION,
        "why": "lead redo2 of the Stage-A blockers B1-B6 (G0_SPEC.md section 7)",
        "n_tasks": len(res["tasks"]), "tasks": res["tasks"],
        "author_batches": {n: b.batch_id for n, b in res["author"]},
        "read_batches": {n: b.batch_id for n, b in res["reads"]},
        "released_forms": len(rel["fids"]),
        "ceiling_before_glex": ceilings(reg, set(res["sent_round1"]) | set(rel["fids"])),
        "one_fresh_agent_per_task": True,
        "audit": "c2_kit.audit: read only task_file, write only answer_file; a failed audit deletes that answer file",
        "next": [
            "after both author_lexicon answers: python -m families.T33.redo2 extract-new --write "
            "(loads, lints and unit-tests the new forms, writes their reads and haiku/redo2/TASKS_NEW.json)",
            "after every read: copy the 6 haiku/redo answers to haiku/extract/answers/ (haiku/redo/TASKS.json), then "
            "python -m families.T33.redo2 admit --write (records every read, freezes pools/)"],
    }
    paths.write_files(R2, {"TASKS.json": json.dumps(doc, ensure_ascii=False, indent=1) + "\n"})
    return doc


# ------------------------------------------------------------------------------------------------ stage: extract-new
def load_new(reg) -> dict:
    """Add the redo2 authoring answers to reg through haiku_author._load_one (same rules as round 1, G0 as amended).
    Returns {"fids", "drops", "problems"}."""
    tasks = json.loads((R2 / "TASKS.json").read_text(encoding="utf-8"))
    fids, drops, probs = [], Counter(), []
    for name, bid in tasks["author_batches"].items():
        b = H.batch_from_disk(AUTH, bid)
        got, p1 = H.read_answers(AUTH, b)
        answers, p2 = chunker.load_answers(b, got)
        probs += p1 + [f"{name}: {p}" for p in p2]
        task_of = {iid: b.task_of[q] for q, iid in b.key.items()}
        for iid, ans in sorted(answers.items()):
            texts = ans.get("texts")
            if not isinstance(texts, list):
                drops["no_texts"] += 1
                continue
            for text in texts:
                if not isinstance(text, str) or not text.strip():
                    drops["empty"] += 1
                    continue
                text = text.strip()
                before = set(reg.forms)
                try:
                    piece = H._load_one(name, iid.split("|"), text, iid, task_of[iid], b.prompt_sha, reg)
                except (RenderError, LexiconError, ValueError, S.SlotError) as e:
                    drops["duplicate" if "duplicate" in str(e) else f"{name}_invalid"] += 1
                    probs.append(f"drop {iid}: {str(e)[:80]} | {text}")
                    continue
                if isinstance(piece, str):
                    drops[piece.split(":")[0]] += 1
                    probs.append(f"drop {iid}: {piece[:80]} | {text}")
                fids += sorted(set(reg.forms) - before)
    return {"fids": fids, "drops": dict(drops), "problems": probs}


def extract_new(write: bool) -> dict:
    pieces = H.load_pieces()
    reg = pieces["registry"]
    new = load_new(reg)
    rel = release(reg, [f for f in new["fids"] if reg.forms[f].unit_ok])
    out = {"family": F, "version": VERSION, "stage": "extract-new", "new_forms": len(new["fids"]),
           "new_by_sem": dict(sorted(Counter(reg.forms[f].sem_id for f in new["fids"]).items())),
           "loader_drops": new["drops"], "unit_fail": sum(1 for f in new["fids"] if not reg.forms[f].unit_ok),
           "clause_lint_drops": len(rel["drops"]),
           "clause_lint_rules": dict(Counter(r.split(":")[0] for d in rel["drops"].values() for r in d["rules"])),
           "forbid_held": len(rel["held"]), "released": len(rel["fids"]),
           "released_by_sem": dict(sorted(Counter(reg.forms[f].sem_id for f in rel["fids"]).items())),
           "problems": new["problems"][:40]}
    if not rel["fids"]:
        return out
    reads = read_batches(reg, rel["fids"], READ_NEW, "new")
    texts, tasks, hits = {}, [], []
    for name, b in reads:
        for c in b.chunks:
            texts[c["task_id"]] = read_task_text(c, name)
            hits += [(c["task_id"], s) for s in _forbid_blob(json.dumps(c["items"], ensure_ascii=False))]
            tasks.append({"task_file": str(TASKS_DIR / f"{c['task_id']}.txt"), "answer_file": c["answer_file"],
                          "kind": f"extract_lex:new_{name}", "n_items": len(c["items"])})
    out.update(tasks=tasks, forbid_hits=hits)
    if hits or not write:
        return out
    if (READ_NEW / "answers").exists() and any((READ_NEW / "answers").iterdir()):
        raise RuntimeError("read_new answers exist: not rewritten")
    files = {}
    for _n, b in reads:
        files.update(b.files())
    paths.write_files(READ_NEW, files)
    paths.write_files(TASKS_DIR, texts)
    doc = {"family": F, "version": VERSION, "stage": "extract-new", "n_tasks": len(tasks), "tasks": tasks,
           "read_batches": {n: b.batch_id for n, b in reads}, "new_forms": out["new_by_sem"],
           "released_by_sem": out["released_by_sem"], "one_fresh_agent_per_task": True,
           "lint_drops": [rel["drops"][k] for k in sorted(rel["drops"])],
           "forbid_held": [rel["held"][k] for k in sorted(rel["held"])]}
    paths.write_files(R2, {"TASKS_NEW.json": json.dumps(doc, ensure_ascii=False, indent=1) + "\n"})
    return out


# ------------------------------------------------------------------------------------------------ stage: admit
def admit(write: bool) -> dict:
    """Record the round-1 reads (haiku/extract/answers: the audited copies of the haiku/redo answers), the redo2 reads
    and the read_new reads, then freeze pools/ (haiku_author.freeze). A missing read leaves its form pending."""
    pieces = H.load_pieces()
    reg = pieces["registry"]
    new = load_new(reg) if (R2 / "TASKS.json").exists() else {"fids": [], "problems": []}
    rec = {}
    t1 = json.loads((H.EXTRACT / "TASKS.json").read_text(encoding="utf-8"))
    rec["round1"] = H.record_extractions(reg, [(n, H.batch_from_disk(H.EXTRACT, bid))
                                               for n, bid in t1["batches"].items()], root=H.EXTRACT)
    for tag, root, fname in (("redo2", READ, "TASKS.json"), ("redo2_new", READ_NEW, "TASKS_NEW.json")):
        p = R2 / fname
        if p.exists():
            bids = json.loads(p.read_text(encoding="utf-8"))["read_batches"]
            rec[tag] = H.record_extractions(reg, [(n, H.batch_from_disk(root, bid)) for n, bid in bids.items()],
                                            root=root)
    status = Counter(reg.status(f) for f in reg.forms)
    adm = Counter(reg.forms[f].sem_id for f in reg.forms if reg.status(f) == "admitted")
    want = targets()
    have = {k: adm[k if not k.startswith("wording:") else H.question_sem(F, k.split(":", 1)[1])] for k in want}
    out = {"family": F, "version": VERSION, "stage": "admit", "new_forms": len(new["fids"]),
           "reads": {k: {"reads": v["reads"], "problems": v["problems"][:10]} for k, v in rec.items()},
           "status": dict(status), "admitted_vs_target": {k: f"{have[k]} / {want[k]}" for k in want},
           "shortfalls": H.shortfalls(pieces["packs"], pieces["skins"], reg, admitted_only=True)}
    if write:
        out["manifest_sha256"] = H.freeze(pieces)["sha256"]
    return out


# ------------------------------------------------------------------------------------------------ CLI
def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("step", choices=("build", "extract-new", "admit"))
    ap.add_argument("--write", action="store_true")
    a = ap.parse_args(argv)
    if a.step == "build":
        res = build()
        out = summarise_build(res)
        if res["hits"]:
            print(json.dumps(out, indent=1, ensure_ascii=False))
            print("STOP: a task file carries a forbidden string; nothing written", file=sys.stderr)
            return 2
        if a.write:
            write_build(res)
            out["mode"] = "written"
            out["task_list"] = res["tasks"]
        else:
            out["mode"] = "dry run (nothing written)"
        print(json.dumps(out, indent=1, ensure_ascii=False))
        return 0
    if a.step == "extract-new":
        out = extract_new(a.write)
        print(json.dumps(out, indent=1, ensure_ascii=False))
        return 2 if out.get("forbid_hits") else 0
    print(json.dumps(admit(a.write), indent=1, ensure_ascii=False, default=str))
    return 0


if __name__ == "__main__":
    sys.exit(main())
