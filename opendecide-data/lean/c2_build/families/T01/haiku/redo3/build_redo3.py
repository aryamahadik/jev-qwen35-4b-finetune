"""families/T01/haiku/redo3/build_redo3.py: the T01 redo3 Haiku tasks (G0_SPEC.md v3; STAGE_A3_REPORT.json shortfalls).

New tasks only: nothing existing is edited, no answer is written here, and Haiku never sees a gold, an option or a
row. Inputs are the freeze-v2 pools (families/T01/pools_v2/), the authoring plan (haiku_author) and the extraction
prompt (extract.G3H_PROMPT, unchanged). Every write goes through c2_kit.paths.write_files (refuses before A38).

The open G0 shortfalls this round closes (STAGE_A3_REPORT.json, T01; no G0 target is lowered):

  skins        30 short: memo 4, email 2, chat 5, ticket 6, json 3, yaml 1, log 5, transcript 2 (training),
               faq 1, letter 1 (held out). No skin redo task existed. Asked: ceil(1.5 x gap) per register = 48 skins in
               3 tasks, the v1 briefs (register, tone, role, register rules) at the next free index of each register,
               plus the word lists of every G-SL rule the v1 skins were rejected for (bunch, much, one, kept, queued,
               shortly, whenever) and one variation hint per item.
  windows      win.later_anchor 4 short, win.wait_after 3 short. No window redo task existed. Asked 6 + 5 = 11 clauses in
               1 task, the v1 briefs, plus the exact words the family check looks for (v1 losses: "pair" for "dates",
               "day following" for "day after", "right after").
               The 3 + 3 G-LEX reads of the new clauses cannot exist before these answers do (see INGEST).
  documents    2 short: t01r2.free.email.031a and t01r2.free.memo.070a pass check_freeform but have no g3h-r1 read
               (build_redo2 built none): one G3-H read task of the 2 notes (extract.G3H_PROMPT unchanged), and 3 backup
               notes (ceil(1.5 x 2)) from facts-only briefs, in case a read drops a note.

Existing reads without answers: none. Every chunk of haiku/author, haiku/extract and haiku/redo2 has a valid answer file,
and the 12 redo2 wordings that wait for G-LEX reads feed no G0 minimum (asked-count gaps are informational), so no
G-LEX read is built for them here.

Run from lean/c2_build:
  ../.venv/bin/python -B families/T01/haiku/redo3/build_redo3.py            (dry run: counts, writes nothing)
  ../.venv/bin/python -B families/T01/haiku/redo3/build_redo3.py --write    (writes tasks/, chunks/, key/, plan/ ...)
"""
from __future__ import annotations

import sys

sys.dont_write_bytecode = True

import hashlib  # noqa: E402
import importlib.util  # noqa: E402
import json  # noqa: E402
import re  # noqa: E402
from collections import Counter  # noqa: E402
from pathlib import Path  # noqa: E402

ROOT = Path(__file__).resolve().parent                     # families/T01/haiku/redo3
T01_DIR = ROOT.parents[1]                                  # families/T01
C2_BUILD = T01_DIR.parents[1]                              # lean/c2_build
if str(C2_BUILD) not in sys.path:
    sys.path.insert(0, str(C2_BUILD))

from c2_kit import chunker, g3h, gsl, paths  # noqa: E402
from families.T01 import extract as E  # noqa: E402
from families.T01 import haiku_author as A  # noqa: E402
from families.T01 import plugin as P  # noqa: E402

FAMILY = "T01"
VERSION = "redo3-v1"
POOLS_V2 = T01_DIR / "pools_v2"
REDO2 = T01_DIR / "haiku" / "redo2"
A3_REPORT = C2_BUILD / "STAGE_A3_REPORT.json"
CHUNK_SKIN = 16                                            # 48 skins -> 3 tasks of 16

# ------------------------------------------------------------------------------------------------ the gaps
# STAGE_A3_REPORT.json, family T01, "shortfalls" (cross-checked against pools_v2 in check_gaps()).
SKIN_GAP = {"memo": 4, "email": 2, "chat": 5, "ticket": 6, "json": 3, "yaml": 1, "log": 5, "transcript": 2,
            "faq": 1, "letter": 1}
WINDOW_GAP = {"win.later_anchor": 4, "win.wait_after": 3}
DOC_GAP = 2
TRAIN = tuple(A.TRAIN_REGISTERS)
HELD = tuple(A.HELD_REGISTERS)


def ask(gap: int) -> int:
    """About 50% more than the gap, rounded up (lint and G-LEX losses still close it): 4 -> 6, 3 -> 5, 1 -> 2."""
    return (3 * gap + 1) // 2


# ------------------------------------------------------------------------------------------------ small helpers
def _jsonl(path: Path) -> list:
    paths.check_path(path)
    return [json.loads(x) for x in path.read_text(encoding="utf-8").splitlines() if x.strip()]


def _sha(path: Path) -> str:
    paths.check_path(path)
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _load_redo2():
    spec = importlib.util.spec_from_file_location("t01_build_redo2", REDO2 / "build_redo2.py")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def _norm(t: str) -> str:
    return " ".join(str(t).split()).lower()


def check_gaps() -> dict:
    """Recompute every gap from pools_v2 and compare with SKIN_GAP / WINDOW_GAP / DOC_GAP and the A3 report text."""
    skins = _jsonl(POOLS_V2 / "skins.jsonl")
    wins = _jsonl(POOLS_V2 / "windows.jsonl")
    docs = _jsonl(POOLS_V2 / "documents.jsonl")
    pend = _jsonl(POOLS_V2 / "documents_pending_g3h.jsonl")
    tgt = {"train": 56, "held": 28, "win": 14, "docs": 120}
    got_s = Counter(r["register"] for r in skins)
    got = {r: (tgt["held"] if r in HELD else tgt["train"]) - got_s[r] for r in TRAIN + HELD}
    got_w = Counter(r["sem"] for r in wins)
    got_w = {s: tgt["win"] - got_w[s] for s in ("win.later_anchor", "win.wait_after")}
    got_d = tgt["docs"] - len(docs)
    if got != SKIN_GAP or got_w != WINDOW_GAP or got_d != DOC_GAP or len(pend) != DOC_GAP:
        raise SystemExit(f"gaps differ from the builder constants: skins {got}, windows {got_w}, docs {got_d}, "
                         f"pending {len(pend)}; pools_v2 changed since this round was planned")
    rep = [r for r in json.loads(paths.check_path(A3_REPORT).read_text(encoding="utf-8")) if r["id"] == FAMILY][0]
    text = " ".join(rep["shortfalls"])
    for reg, g in SKIN_GAP.items():
        m = re.search(rf"skins {reg} \((?:training|held out)\): \d+ of \d+ \(short {g}\)", text)
        if not m:
            raise SystemExit(f"STAGE_A3_REPORT.json does not list 'skins {reg} short {g}'")
    for s, g in (("later_anchor", WINDOW_GAP["win.later_anchor"]), ("wait_after", WINDOW_GAP["win.wait_after"])):
        if not re.search(rf"window win\.{s}: \d+ of 14 \(short {g}\)", text):
            raise SystemExit(f"STAGE_A3_REPORT.json does not list 'window win.{s} short {g}'")
    if "documents admitted (G3-H): 118 of 120 (short 2)" not in text:
        raise SystemExit("STAGE_A3_REPORT.json does not list 'documents short 2'")
    return {"skins": SKIN_GAP, "windows": WINDOW_GAP, "documents": DOC_GAP,
            "asked": {"skins": {r: ask(g) for r, g in SKIN_GAP.items()},
                      "windows": {s: ask(g) for s, g in WINDOW_GAP.items()}, "documents_backup": ask(DOC_GAP)}}


# ------------------------------------------------------------------------------------------------ skins
_LABEL_FORMS = {w.lower() for w in P.T01.LABEL_WORDS}
_LIST_WORDS = sorted((set().union(*gsl.CORE.values()) | set().union(*gsl.EXTENDED.values())) - _LABEL_FORMS
                     - {"late", "ca", "wo", "mustn", "shouldn"})   # "late" is a gold-label word: the prompt may not
                                                                   # print it; ca / wo / mustn / shouldn are n't stems
_T01_WORDS = ("deadline", "due", "limit", "window", "period", "cutoff", "office", "calendar", "weekday", "week",
              "business day", "working day", "clock", "hour", "minute", "date", "day", "rule", "policy", "quote",
              "report", "threshold", "travel", "trip", "visa", "stay", "insurance", "insurer", "claim", "purchase",
              "order", "vendor", "supplier", "cash", "money", "bank", "teller", "ledger", "notice", "court", "appeal",
              "filing", "loss", "damage", "peril")

SKIN_EXTRA = """

Extra rules for this round (a program rejects a skin that breaks one; these come on top of the rules above):
11. Earlier skins were rejected for these words, so never write them: bunch, much, one (also as a pronoun, as in "a \
routine one"), kept, queued, shortly, whenever. Never write "kind of" or "sort of" either.
12. A program rejects every one of these whole words anywhere outside the placeholders, in any capital letters: \
""" + ", ".join(_LIST_WORDS) + """.
13. It also rejects these whole words and their plural forms, wherever they stand outside the placeholders: \
""" + ", ".join(_T01_WORDS) + """.
14. Write only plain words and the punctuation the item's register needs. Put a capital letter only where rule 10 \
allows it.
15. Before you answer, read every skin word by word against rules 11-13 and rewrite any skin that holds a listed \
word. Each item ends with a variation hint: follow it.""" + ""

NARR_REG = {r: i for i, r in enumerate(TRAIN + HELD)}
VERBS = ("forwards", "submits", "passes along", "shares", "hands in", "routes", "sends over", "brings in")
ORDERS = ("name the sender first", "name the file reference first", "name the topic first")
SENDER_KEYS = ("sent_by", "from", "sender", "submitted_by", "author", "origin", "contact", "owner")
FILE_KEYS = ("file", "file_ref", "ref", "reference", "doc", "item", "ref_code", "file_code")
LOG_TAGS = ("intake", "handoff", "routing", "inbox", "mailroom", "frontline", "triage", "dispatch")


def variation_hint(reg: str, i: int) -> str:
    ri = NARR_REG[reg]
    if reg in ("json", "yaml"):
        return (f"Variation hint: name the key that holds {{PERSON}} '{SENDER_KEYS[(i * 3 + ri) % 8]}' and the key "
                f"that holds {{REF}} '{FILE_KEYS[(i * 5 + ri) % 8]}'.")
    if reg == "log":
        return f"Variation hint: use the word '{LOG_TAGS[(i * 3 + ri) % 8]}' once as a tag or key name, and {ORDERS[i % 3]}."
    return f"Variation hint: if you use a verb for sending, use '{VERBS[(i * 3 + ri) % 8]}'; {ORDERS[i % 3]}."


def skin_batch() -> tuple:
    items, plan = [], {}
    quarantined = {r["pid"] for r in _jsonl(POOLS_V2 / "quarantine.jsonl") if r.get("group") == "skins"}
    for reg in TRAIN + HELD:
        held = reg in HELD
        base = A.N_SKIN_HELD if held else A.N_SKIN_TRAIN          # the next free index of this register
        ri = NARR_REG[reg]
        open_slots = sorted(p for p in quarantined if p.startswith(f"t01a.skin.{reg}."))
        for k in range(ask(SKIN_GAP[reg])):
            i = base + k
            tone = A.TONES[(i + ri) % len(A.TONES)]
            role = A.ROLES[(i * 3 + ri) % len(A.ROLES)]
            iid = f"t01r3.skin.{reg}.{i:03d}"
            items.append((iid, {
                "brief": f"Write {A.REGISTER_DESC[reg]} in which {{PERSON}} sends file {{REF}} about the {{TOPIC}} to "
                         f"{role}. Tone: {tone}.",
                "register": reg, "slots": dict(A.NARR), "rules": list(A.REGISTER_RULES[reg]) + [variation_hint(reg, i)]}))
            plan[iid] = {"role": "skin", "register": reg, "tone": tone, "held_out": held,
                         "escape": reg if reg in ("json", "yaml") else "text", "open_slots": open_slots,
                         "gap": SKIN_GAP[reg]}
    b = chunker.make_batch("author_skin", FAMILY, items, seed=f"t01-{VERSION}|skins", prompt=A.SKIN_PROMPT + SKIN_EXTRA,
                           max_items=CHUNK_SKIN, forbid_strings=A.FORBID_ALL)
    return "skins", b, plan


# ------------------------------------------------------------------------------------------------ windows
WINDOW_EXTRA = """

Extra rules for this round (a program rejects a clause that breaks one; these come on top of the rules above):
6. A program checks each clause by looking for exact words. The last rules of each item name the exact words that \
item's clause must contain: use those exact words (not a synonym) inside your own sentence.
7. Each item lists clauses that already exist for its meaning. Write a NEW clause: never copy one of them, and never \
repeat a clause you write for another item. Change the words around the required ones, never the meaning.
8. A program rejects a clause that holds any of these whole words: calendar, business, working, week, weeks, month, \
months, year, years. Write no digit."""

WINDOW_MUST = {
    "win.later_anchor": "Exact words this clause must contain: 'later' (as in 'the later of') and 'dates' (as in 'these "
                        "two dates' or 'the dates below'). Never write 'pair', 'earlier', 'first' or 'either'. Begin "
                        "with a lower-case word that reads right after 'must be filed' (such as 'within' or 'inside').",
    "win.wait_after": "Exact words this clause must contain: 'waiting period' and 'the day after' (never 'the day "
                      "following', 'right after', 'comes after' or 'next day'). The clause must END with the exact words "
                      "'its start date', with no word after them. Use {W} exactly once.",
}


def window_batch() -> tuple:
    wins = _jsonl(POOLS_V2 / "windows.jsonl")
    items, plan = [], {}
    for sem in ("win.later_anchor", "win.wait_after"):
        meaning, example, sentence, slots, rules = A.WINDOW_MEANING[sem]
        exist = sorted(r["text"] for r in wins if r["sem"] == sem)
        for k in range(ask(WINDOW_GAP[sem])):
            i = A.N_WINDOW + k                                   # the next free index of this sem
            vary = ("keep it short", "use a different verb or preposition", "use your own sentence shape")[i % 3]
            iid = f"t01r3.window.{sem}.{i:03d}"
            items.append((iid, {
                "brief": f"Write a clause with this meaning. It goes into: \"{sentence}\" Example of the shape (do not "
                         f"copy it): \"{example}\".",
                "meaning": meaning, "slots": dict(slots),
                "rules": list(rules) + [f"Vary the wording: {vary}.", WINDOW_MUST[sem],
                                        "Clauses that already exist for this meaning (write a NEW one, never copy "
                                        "one): " + " | ".join(exist)]}))
            plan[iid] = {"role": "lexicon", "kind": "window", "sem": sem, "slots": dict(slots),
                         "gap": WINDOW_GAP[sem]}
    b = chunker.make_batch("author_lexicon", FAMILY, items, seed=f"t01-{VERSION}|windows",
                           prompt=A.WINDOW_PROMPT + WINDOW_EXTRA, max_items=len(items), forbid_strings=A.QSTRINGS)
    return "windows", b, plan


# ------------------------------------------------------------------------------------------------ backup notes
CLEAN_TOPICS = tuple(t for t in A.FF_TOPICS if not A.SKIN_BANNED.search(t))         # no banned word inside the TOPIC
BACKUP_START = A.N_FREEFORM                                                         # the next free index: 120


def freeform_batch() -> tuple:
    docs = _jsonl(POOLS_V2 / "documents.jsonl") + _jsonl(POOLS_V2 / "documents_pending_g3h.jsonl")
    used = {(d["facts"]["PERSON"], d["facts"]["REF"]) for d in docs}
    r2 = _load_redo2()
    items, plan = [], {}
    for k in range(ask(DOC_GAP)):
        i = BACKUP_START + k
        reg = A.FREEFORM_REGISTERS[i % len(A.FREEFORM_REGISTERS)]
        facts = {"PERSON": A.FF_PEOPLE[(i * 7) % len(A.FF_PEOPLE)],
                 "REF": f"{A.FF_PREFIX[i % len(A.FF_PREFIX)]}-{1000 + (i * 7919) % 9000}",
                 "TOPIC": CLEAN_TOPICS[i % len(CLEAN_TOPICS)]}
        if (facts["PERSON"], facts["REF"]) in used:
            raise SystemExit(f"backup facts repeat an existing note: {facts}")
        tone = A.TONES[(i // len(A.FREEFORM_REGISTERS)) % len(A.TONES)]
        role = A.ROLES[(i * 7) % len(A.ROLES)]
        iid = f"t01r3.free.{reg}.{i:03d}"
        items.append((iid, {"brief": f"PERSON sends file REF about the TOPIC to {role}. Tone: {tone}.",
                            "register": reg, "facts": facts, "rules": list(A.FREEFORM_RULES[reg])}))
        plan[iid] = {"role": "freeform", "register": reg, "tone": tone, "held_out": False, "facts": facts,
                     "backup_for": ["t01r2.free.email.031a", "t01r2.free.memo.070a"]}
    b = chunker.make_batch("author_freeform", FAMILY, items, seed=f"t01-{VERSION}|freeform",
                           prompt=A.FREEFORM_PROMPT + r2.FREEFORM_EXTRA, max_items=len(items),
                           forbid_strings=A.FORBID_ALL)
    return "freeform_backup", b, plan


# ------------------------------------------------------------------------------------------------ G3-H read
def g3h_batch() -> tuple:
    pend = _jsonl(POOLS_V2 / "documents_pending_g3h.jsonl")
    fields = E._g3h_fields()
    items = [(p["pid"], g3h.extraction_item(p["text"], fields)) for p in pend]
    plan = {p["pid"]: {"role": "g3h_read", "read": "g3h-r1", "register": p["register"], "g3h_expect": p["g3h_expect"],
                       "text_sha256": hashlib.sha256(p["text"].encode()).hexdigest(), "slot": p.get("slot")}
            for p in pend}
    b = chunker.make_batch("extract_g3h", FAMILY, items, seed=f"t01-{VERSION}|g3h-r1", prompt=E.G3H_PROMPT,
                           max_items=chunker.MAX_ITEMS)
    return "g3h_pending", b, plan


# ------------------------------------------------------------------------------------------------ task files
SKIN_EXAMPLE = [
    {"qid": "qEXAMPLE0001", "text": "Desk memo: {PERSON} forwards file {REF} about the {TOPIC} to the review team."},
    {"qid": "qEXAMPLE0002", "text": "sent_by: {PERSON}\nfile_ref: {REF}\nsubject: {TOPIC}\nchannel: intake"}]
WINDOW_EXAMPLE = [
    {"qid": "qEXAMPLE0001", "text": "by the end of {N} after the later of the two dates below"},
    {"qid": "qEXAMPLE0002", "text": "a waiting period of {W} that starts on the day after its start date"}]
FREEFORM_EXAMPLE = [
    {"qid": "qEXAMPLE0001", "text": "Dear desk,\n\nLena Hartmann forwards file ZZ-0000 about the garden fence repair to "
                                    "the review team. Thank you for your help.\nKind regards,"},
    {"qid": "qEXAMPLE0002", "text": "Lena Hartmann: sending file ZZ-0000 about the garden fence repair.\ndesk: got it, "
                                    "thanks."}]
CONTRACT = {
    "author_skin": ("'qid', 'text'", '{"qid": "<the item\'s qid>", "text": "<the skin; \\n for a line break>"}',
                    SKIN_EXAMPLE),
    "author_lexicon": ("'qid', 'text'", '{"qid": "<the item\'s qid>", "text": "<the clause>"}', WINDOW_EXAMPLE),
    "author_freeform": ("'qid', 'text'", '{"qid": "<the item\'s qid>", "text": "<the note; \\n for a line break>"}',
                        FREEFORM_EXAMPLE),
}


def _example(rows: list) -> str:
    return "[\n  " + ",\n  ".join(json.dumps(r, ensure_ascii=False) for r in rows) + "\n]"


def task_text(b, chunk: dict, label: str, task_file: Path, answer_file: Path) -> str:
    n = len(chunk["items"])
    keys, shape, example = CONTRACT[b.kind]
    items = "\n".join(json.dumps(it, ensure_ascii=False) for it in chunk["items"])
    return "\n".join([
        f"REDO3 TASK {chunk['task_id']}  (family {FAMILY}, kind {b.kind}, {label}, {n} items)", "",
        "This one text file is your whole task. Read all of it, then write the answer file, then stop.",
        "Do not open, list, search or write any other file or folder. Create no other file. Do not put the answer in "
        "chat;", "when the answer file is written, reply with the single word DONE.", "",
        f"TASK FILE (this file)                 : {task_file}",
        f"ANSWER FILE (write exactly this path) : {answer_file}", "",
        "=== ANSWER CONTRACT (exact) ===",
        "Write ONE JSON array to the ANSWER FILE with the Write tool, and nothing else in that file: no markdown fence, "
        "no", "comment, no wrapper object, no extra text before or after the array.",
        f"- The array has exactly {n} objects, one for each of the {n} items below, every qid exactly once (any order).",
        f"- Each object has exactly these keys and no others: {keys}.",
        "- \"qid\": the item's qid, copied character for character. It is an opaque label; read nothing into it.",
        "- Inside a JSON string write a double quote as \\\" and a line break as \\n. Valid JSON only.",
        "- Not allowed: any other key (such as \"note\", \"reason\" or \"confidence\"); a skipped qid; a qid used "
        "twice; a qid", "  that is not in the items below.",
        f"Shape of one object: {shape}",
        f"Literal example of the required shape (EXAMPLE ONLY: these two objects are not items and their texts are not to "
        f"be copied; your array has {n} objects):", _example(example), "",
        "=== INSTRUCTIONS ===", b.prompt.rstrip(), "",
        f"=== ITEMS ({n}; one JSON object per line; every item needs one answer object carrying its qid) ===", items,
        ""])


G3H_FIELDS = """=== WHAT EACH FIELD HOLDS (exact) ===
Copy the characters as they are written in that item's TEXT, with the same capital letters, hyphens and digits.
- "person": the full name (first name and surname) of the person who wrote the note or is named in it as the sender.
  Leave out any colon, comma or period that follows the name, for example the colon after a speaker label in a chat
  or transcript line.
- "ref": the reference code of the file, case or notice (letters, a hyphen and digits), written exactly as in the TEXT.
  Leave out any punctuation that follows it.
- "topic": the short phrase that says what the note is about, written exactly as in the TEXT, without the word "the"
  in front of it. The phrase is only the words that name the subject. It stops before a comma, period or colon, and
  before the words that start the next part of the sentence (such as to, for, with, from, is, as, and). Never include
  a trailing comma, period or colon.
- Do not correct spelling, do not infer anything and do not take a value from another item. Judge each item on its
  own TEXT alone.
"""


def g3h_task_text(b, chunk: dict, label: str, task_file: Path, answer_file: Path) -> str:
    """The haiku/redo (round 1) G3-H wrapper: exact contract with a literal example and the field boundary rules, around
    the family's unchanged G3H_PROMPT (inline, in full)."""
    n = len(chunk["items"])
    items = "\n".join(json.dumps(it, ensure_ascii=False) for it in chunk["items"])
    return "\n".join([
        f"REDO3 TASK {chunk['task_id']}  (family {FAMILY}, kind {b.kind}, read g3h-r1, {n} items)", "",
        "This one text file is your whole task. Read all of it, then write the answer file, then stop.",
        "Do not open, list, search or write any other file or folder. Create no other file. Do not put the answer in "
        "chat;", "when the answer file is written, reply with the single word DONE.", "",
        f"TASK FILE (this file)                 : {task_file}",
        f"ANSWER FILE (write exactly this path) : {answer_file}", "",
        "=== ANSWER CONTRACT (exact) ===",
        "Write ONE JSON array to the ANSWER FILE with the Write tool, and nothing else in that file: no markdown fence, "
        "no", "comment, no wrapper object, no extra text before or after the array.",
        f"- The array has exactly {n} objects, one for each of the {n} items below, every qid exactly once (any order).",
        "- Each object has exactly these four keys and no others: \"qid\", \"person\", \"ref\", \"topic\".",
        "- \"qid\": the item's qid, copied character for character. It is an opaque label; read nothing into it.",
        "- \"person\", \"ref\", \"topic\": each ONE JSON string (never null, a number, a list or an object). Inside a "
        "JSON string", "  write a double quote as \\\" and a line break as \\n. If a field is truly not in the TEXT, the "
        "string is NONE.",
        "- Not allowed: a key such as \"text\", \"schema\", \"note\", \"confidence\" or \"reason\"; a skipped qid; a qid "
        "used twice;", "  a qid that is not in the items below.",
        f"Literal example of the required shape (EXAMPLE ONLY, these two objects are not items; your array has {n} "
        f"objects):", "[",
        '  {"qid": "qEXAMPLE0001", "person": "Lena Hartmann", "ref": "ZZ-0000", "topic": "garden fence repair"},',
        '  {"qid": "qEXAMPLE0002", "person": "Jonas Weller", "ref": "QX-9999", "topic": "boat shed lease"}', "]", "",
        G3H_FIELDS.rstrip(), "",
        "=== INSTRUCTIONS (the family's G3-H read prompt, unchanged) ===", b.prompt.rstrip(), "",
        f"=== ITEMS ({n}; one JSON object per line; every item needs one answer object carrying its qid) ===", items,
        ""])


INGEST = {   # orchestrator side (needs an ingestion step; nothing here admits anything)
    "audit": "audit.audit_jsonl per agent transcript with the task's audit_allowed_read / audit_allowed_write; a failed "
             "audit discards that agent's answers. Map answers with chunker.load_answers(batch, {task_id: answer}) "
             "using key/<batch_id>.json; plan/<batch_id>.json holds the per-item meta.",
    "skins": "haiku_author.check_skin(iid, text, plan meta, task_id, prompt_sha, seen) with 'seen' seeded with the normalised "
             "text of every admitted skin of pools_v2; per register, take the passing skins in sorted id order until the "
             "register reaches its G0 target (training 56, held out 28); unused passing skins are not kept. Skin ids "
             "T01-SK-<register>.<index> continue each register's v1 numbering (56 / 28 up); plan 'open_slots' lists the v1 "
             "slots that stayed open.",
    "windows": "haiku_author.check_lexicon with 'seen' seeded with the admitted window texts. A kept clause is new to "
               "the registry and has NO reads: it needs three independent G-LEX reads (3/3; glex-r1/-r2/-r3 style, "
               "extract.glex_items) and then the three confirmation reads glex-r1b/-r2b/-r3b (H45, "
               "redo2/build_redo2.realistic_values) before it is used. Those read tasks can only be built after these "
               "answers return.",
    "freeform_backup": "haiku_author.check_freeform with the plan facts; a passing note needs one g3h-r1 read and "
                       "g3h.compare against plan facts. Only needed if a note of g3h_pending fails to match.",
    "g3h_pending": "extract G3-H read g3h-r1 (unchanged prompt, prompt_sha = extract.G3H_PROMPT's): record the answer "
                   "with g3h.compare(plan g3h_expect, answer, fields); a match admits the note into documents "
                   "(documents_pending_g3h -> documents), a mismatch drops it (H47).",
    "freeze": "freeze_v2.py ingests author, extract, redo and redo2 only; a redo3 loader is still to be added before the "
              "next freeze (this builder's file layout is the redo2 layout: tasks/, chunks/, key/, plan/, manifest/, "
              "prompts/, answers/, TASKS.json).",
}


def build() -> dict:
    gaps = check_gaps()
    groups = [skin_batch(), window_batch(), freeform_batch(), g3h_batch()]
    files, tasks = {}, []
    for label, b, plan in groups:
        files.update(b.files())
        files[f"plan/{b.batch_id}.json"] = json.dumps({"batch_id": b.batch_id, "label": label, "kind": b.kind,
                                                       "plan": plan}, indent=1, sort_keys=True,
                                                      ensure_ascii=False) + "\n"
        for c in b.chunks:
            tid = c["task_id"]
            tf, af = ROOT / "tasks" / f"{tid}.txt", ROOT / b.answer_path(tid)
            files[f"tasks/{tid}.txt"] = (g3h_task_text if b.kind == "extract_g3h" else task_text)(b, c, label, tf, af)
            tasks.append({"task_file": str(tf), "answer_file": str(af), "kind": b.kind,
                          "stage": "extract" if b.kind == "extract_g3h" else "author", "label": label,
                          "batch_id": b.batch_id, "task_id": tid, "n_items": len(c["items"]),
                          "outputs_expected": len(c["items"]), "prompt_sha": b.prompt_sha,
                          "audit_allowed_read": [str(tf)], "audit_allowed_write": [str(af)]})
    for t in tasks:
        for p in (t["task_file"], t["answer_file"]):
            if paths.never_open(p):
                raise SystemExit(f"never-open path in the task list: {p}")
    if len(tasks) > 12:
        raise SystemExit(f"{len(tasks)} tasks; at most 12 are allowed")
    return {"files": files, "tasks": tasks, "groups": groups, "gaps": gaps}


def main(argv: list) -> int:
    res = build()
    counts = Counter((t["label"], t["kind"]) for t in res["tasks"])
    items = Counter()
    for t in res["tasks"]:
        items[t["label"]] += t["n_items"]
    summary = {"tasks": len(res["tasks"]), "tasks_by_label": {f"{a}|{k}": n for (a, k), n in sorted(counts.items())},
               "items_by_label": dict(sorted(items.items())), "files": len(res["files"]), "gaps": res["gaps"]}
    print(json.dumps(summary, indent=1))
    if "--write" in argv:
        inputs = {f: _sha(POOLS_V2 / f) for f in ("skins.jsonl", "windows.jsonl", "documents.jsonl",
                                                  "documents_pending_g3h.jsonl", "quarantine.jsonl")}
        inputs["STAGE_A3_REPORT.json"] = _sha(A3_REPORT)
        man = {"family": FAMILY, "version": VERSION, "g0_sha256": P.T01.G0_SHA256, "n_tasks": len(res["tasks"]),
               "outputs_expected": sum(t["outputs_expected"] for t in res["tasks"]),
               "builder": str(Path(__file__).resolve()),
               "builder_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
               "inputs_sha256": inputs, "gaps": res["gaps"],
               "note": "Rebuilding is valid only against the input shas above (pools_v2 is read for the gaps, the "
                       "existing window clauses and the pending notes).",
               "ingest": INGEST, "tasks": res["tasks"]}
        res["files"]["TASKS.json"] = json.dumps(man, indent=1, ensure_ascii=False) + "\n"
        res["files"]["answers/README.txt"] = ("Haiku answer files: one <task_id>.json per redo3 task (see ../TASKS.json). "
                                              "Written only by the task agents.\n")
        paths.write_files(ROOT, res["files"])
        print(f"written under {ROOT}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
