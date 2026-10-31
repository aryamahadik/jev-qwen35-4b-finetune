"""families/T46/haiku_author.py: the T46 Haiku pools (A59 (c) and (d); C2_DATA_SPEC 3.0, 3.3, 6.4; A37 b).

Haiku writes wording only: question wordings (5 forms), class glosses (what a label means), Arabic person names and
Arabic notes (one program-assigned situation class per note). It never sees a label, an option, a row or a gold, and it
never sets a class: every piece goes through the lints below, then G-LEX (the unit test plus >= 2 blind reads that must
pick the program's meaning list entry; one disagreement rejects the piece for good). The label sets, the flag-value
lexicon and the state layouts are program text; their meanings are read blind as well. Steps (from lean/c2_build):

  ../.venv/bin/python -m families.T46.haiku_author write-tasks        # Resolve: authoring chunks (<= 13 items each)
  ../.venv/bin/python -m families.T46.haiku_author lint               # load answers, lints, counts, probe collisions
  ../.venv/bin/python -m families.T46.haiku_author extract-tasks      # G-LEX reads: 2 independent reads of every form
  ../.venv/bin/python -m families.T46.haiku_author admit              # record the reads, freeze pools/

Every task file is a chunk written by c2_kit.chunker.make_batch through paths.write_files; it carries its own
instructions and the absolute path of the one answer file the agent writes. Nothing is written before A38.
"""
from __future__ import annotations

import argparse
import ast
import hashlib
import json
import re
import sys
import unicodedata
from collections import Counter
from pathlib import Path

from c2_kit import chunker, gsl, paths
from c2_kit import polarity as POL
from c2_kit.lexicon import LexiconRegistry, question_sem
from c2_kit.skin import make_skin

import negcount  # noqa: E402  (c_src/common, put on sys.path by c2_kit.paths)

from . import plugin as PLG
from . import tables as T

HERE = Path(__file__).resolve().parent
HAIKU = HERE / "haiku"
AUTHOR = HAIKU / "author"
EXTRACT = HAIKU / "extract"
POOLS = HERE / "pools"
F = T.FAMILY
VERSION = "v1"
MAX_TASKS = 40

# ------------------------------------------------------------------------------------------------ targets (items x texts)
WORD_ITEMS = {"yn_is": 8, "yn_not": 7, "yn_ruledout": 7, "yn_dneg": 6, "ch_disp": 14}      # train items per form
WORD_ITEMS_DEV = 2
WORD_TEXTS = 6
GLOSS_ITEMS, GLOSS_ITEMS_DEV, GLOSS_TEXTS = 8, 2, 6
NAME_ITEMS, NAME_ITEMS_DEV, NAME_TEXTS = 4, 1, 12
NOTE_ITEMS, NOTE_ITEMS_DEV, NOTE_TEXTS = 2, 1, 5            # per (workflow, class)
AR_WF_TRAIN = ("support", "access", "hr")
# floors after admission (the pools freeze reports shortfalls; G11 needs >= 50 wordings for the big forms)
FLOORS = {"wording": {"ch_disp": 50, "yn_is": 30, "yn_not": 24, "yn_ruledout": 24, "yn_dneg": 18},
          "wording_dev": 4, "gloss": 16, "gloss_dev": 4, "names_ar": 24, "names_ar_dev": 6, "note": 8, "note_dev": 2}

PERSON_CTX = {"support": "a customer asks a support desk to put a purchase right",
              "access": "an employee asks for access to a system", "hr": "an employee asks for leave",
              "purchase": "a buyer asks to place a purchase order"}
SITUATION = {"P": "everything about the request is in order and nothing needs a second look",
             "H": "something needed to decide is still missing or unconfirmed, so the decision has to be put off",
             "D": "the request breaks a firm rule or looks fraudulent, so it must be refused",
             "E": "the case is disputed or unusual or beyond the clerk's authority, so a person must decide"}

ALL_LABEL_STRINGS = sorted({t for v in T.VOCABS for c in T.CLASSES for t in T.label_forms(v, c)})
SINGLE_LABEL_WORDS = sorted({t for t in ALL_LABEL_STRINGS if " " not in t})
LABEL_CLASS = T.all_label_texts()


# ------------------------------------------------------------------------------------------------ lints
def _sha(s: str) -> str:
    return hashlib.sha256(s.encode()).hexdigest()


def _words(text: str) -> int:
    return len(re.findall(r"\S+", text))


def has_label_word(text: str, classes=None) -> list:
    """Label strings (any vocabulary) that occur as whole words in `text`; classes: only labels of those classes."""
    low = text.lower()
    out = []
    for t, c in LABEL_CLASS.items():
        if classes is not None and c not in classes:
            continue
        if re.search(r"(?<![a-z0-9_])" + re.escape(t) + r"(?![a-z0-9_])", low):
            out.append(t)
    return out


NEG_PROFILE = {"yn_is": (0, 0), "yn_not": (1, 1), "yn_ruledout": (1, 0), "yn_dneg": (2, 2), "ch_disp": (0, 0)}   # (k_all, k_syn)


def wording_problems(qform: str, text: str) -> list:
    p = []
    if not isinstance(text, str) or text != text.strip() or "\n" in text:
        return ["not one trimmed line"]
    if not text.endswith("?") or text.count("?") != 1:
        p.append("one question ending with ?")
    if not 6 <= _words(text) <= 25:
        p.append(f"{_words(text)} words (6-25)")
    if re.search(r"\d", text):
        p.append("digit")
    if has_label_word(text):
        p.append(f"names an action: {has_label_word(text)[:2]}")
    if qform != "ch_disp" and "proposed action" not in text.lower():
        p.append("yes/no wording must say 'proposed action'")
    if qform == "ch_disp" and ("proposed" in text.lower() or "yes" in text.lower().split()):
        p.append("choice wording must not mention a proposed action")
    if qform == "ch_disp" and not re.search(r"\b(action|actions|option|options|choice)\b", text.lower()):
        p.append("choice wording must say action / option")
    sk = make_skin("lint-w", F, text, {}, kind="wording", register="question", qform=qform)
    for v in gsl.lint_template(sk, label_words=PLG.T46Plugin.LABEL_WORDS, exceptions={}, name_allow=()):
        p.append(f"G-SL {v.rule}: {v.detail}")
    k = negcount.count(text)
    if (k.k_all, k.k_syn) != NEG_PROFILE[qform]:
        p.append(f"negation profile (k_all, k_syn) = {(k.k_all, k.k_syn)}, the form needs {NEG_PROFILE[qform]}")
    if qform != "ch_disp":
        p += [f"polarity: {x}" for x in POL.form_problems(PLG.T46Plugin, qform, text)]
    return p


def gloss_problems(cls: str, text: str) -> list:
    p = []
    if not isinstance(text, str) or text != text.strip() or "\n" in text:
        return ["not one trimmed line"]
    if not 4 <= _words(text) <= 16:
        p.append(f"{_words(text)} words (4-16)")
    if not text[0].islower():
        p.append("starts with a lower-case letter")
    if re.search(r"[\d:;|#=\"'`{}\[\]<>@]", text) or text[-1] in ".!?":
        p.append("digit, quote, colon or end punctuation")
    other = [t for t in has_label_word(text) if LABEL_CLASS[t] != cls]
    if other:
        p.append(f"holds a label of another class: {other[:2]}")
    if re.search(r"\b(yes|true|false)\b", text.lower()):
        p.append("yes / true / false")
    return p


AR_LETTERS = re.compile(r"^[ء-يًٰ-ْ ]+$")


def ar_name_problems(text: str) -> list:
    p = []
    if text != unicodedata.normalize("NFC", text) or text != text.strip():
        p.append("not NFC / trimmed")
    if not AR_LETTERS.match(text):
        p.append("Arabic letters and spaces only")
    if not 2 <= len(text.split()) <= 3:
        p.append("2-3 words")
    return p


def ar_note_problems(text: str) -> list:
    p = []
    if text != unicodedata.normalize("NFC", text) or text != text.strip() or "\n" in text:
        p.append("not NFC / one trimmed line")
    body = text[:-1] if text.endswith(".") else text
    if not re.match(r"^[ء-يًٰ-ْ ،]+$", body):
        p.append("Arabic letters, spaces, the Arabic comma and a final period only")
    if not 3 <= _words(text) <= 14:
        p.append(f"{_words(text)} words (3-14)")
    return p


# ------------------------------------------------------------------------------------------------ prompts
COMMON = ("You write short pieces of text for a synthetic dataset about deciding what to do with a request in an "
          "office workflow. Plain, natural writing; every piece of one item clearly different from the others "
          "(structure, length, wording). Read the items in this file only; do not open any other file. ")
ANSWER_TEXTS = ('Write a JSON array to the answer file, one object per item, in item order: '
                '{"qid": "<the item qid>", "texts": ["<piece 1>", "<piece 2>", ...]}. Write nothing else in the file.')
ANSWER_NAMES = ('Write a JSON array to the answer file, one object per item, in item order: '
                '{"qid": "<the item qid>", "texts": ["<name 1>", "<name 2>", ...]}. Write nothing else in the file.')
PROMPTS = {
    "wordings": COMMON + (
        "Each item asks for question wordings. The reader sees a short record, then (for yes/no items) a line "
        "'Proposed action: ...' naming one action, then your question. Write ONE question per piece, ending with a "
        "question mark, 6 to 25 words, a capital letter only at the start, no digits, no number words, no names, no "
        "dates or times, and never name or hint at a particular action. Follow each item's rules about negation "
        "words exactly: they decide what the question means. ") + ANSWER_TEXTS,
    "glosses": COMMON + (
        "Each item gives a meaning and asks for short phrases that spell out that meaning as an instruction about "
        "what to do with a request. A phrase is lower case, starts with a verb, has 4 to 16 words, uses only commas "
        "as punctuation (no period, no colon, no quotes), has no digits, and says nothing about yes or no. The "
        "reader must be able to tell from the phrase alone which meaning it carries, so stay inside the meaning and "
        "do not hint at the other kinds of outcome. ") + ANSWER_TEXTS,
    "names": COMMON + (
        "Each item asks for invented full names of people (first name and family name, two or three words) written "
        "in Modern Standard Arabic script. Use only Arabic letters and spaces: no digits, no Latin letters, no "
        "punctuation, no titles. Real public figures are not allowed; make the names ordinary and varied. ")
    + ANSWER_NAMES,
    "notes": COMMON + (
        "Each item gives a workflow context and a situation, and asks for one-sentence notes in Modern Standard "
        "Arabic that a clerk might type into a request record. Each note states the situation plainly as a fact "
        "(what is the case), not as an instruction and not as a decision. 3 to 14 words, Arabic letters and spaces "
        "only, with at most one Arabic comma and a final period; no digits, no Latin letters, no quotes, no "
        "colon, no names of people. A reader who sees only the note must be able to tell which situation it "
        "describes. ") + ANSWER_TEXTS,
}
WORD_BRIEFS = {
    "yn_is": ("ask whether the proposed action is the right call for the request in the record; yes means the "
              "proposed action is right", ["use the words 'proposed action'", "no negation word of any kind "
              "(not, no, never, n't, without, fail, rule out ...)"]),
    "yn_not": ("ask whether the proposed action is NOT the right call; yes means it is not right",
               ["use the words 'proposed action'", "exactly one negation word: the single word 'not' (never n't), "
                "and no other negation of any kind"]),
    "yn_ruledout": ("ask whether the facts in the record rule the proposed action out; yes means the proposed "
                    "action is the wrong call", ["use the words 'proposed action'", "build the question on 'rule "
                    "out' or 'ruled out'", "no other negation word (not, no, never, n't, without, fail ...)"]),
    "yn_dneg": ("ask with two negations whether the proposed action is the right call; yes means it IS the right "
                "call", ["use the words 'proposed action'", "exactly two negation words, both the single word "
                "'not' (never n't)", "open with 'Is it not the case that', 'Is it not true that', 'Is it not so "
                "that' or 'Is it not correct that', and put the second 'not' inside the that-clause"]),
    "ch_disp": ("ask which one of the actions listed under the record is the right call for the request",
                ["the actions are listed after your question, so say 'action' or 'actions'", "no negation word of "
                 "any kind", "do not mention a proposed action and do not name any action"]),
}
WORD_ANGLES = ("short and direct", "formal office wording", "conversational", "refers to what the record shows",
               "refers to the request and the facts", "uses an auditor's point of view", "plain everyday words",
               "uses a different sentence opening from the usual ones", "mentions the case or the file",
               "reads like a review checklist question", "asks as a manager would", "neutral and impersonal",
               "asks from the requester's side", "asks about what the facts support")


def wording_items() -> list:
    out = []
    for qf, n in WORD_ITEMS.items():
        meaning, rules = WORD_BRIEFS[qf]
        for i in range(n):
            out.append((f"wording|{qf}|train|{i}", {"brief": f"Question wordings that {meaning}. Angle: "
                                                    f"{WORD_ANGLES[i % len(WORD_ANGLES)]}. Write {WORD_TEXTS} different questions.",
                                                    "slots": {}, "rules": rules}))
        for i in range(WORD_ITEMS_DEV):
            out.append((f"wording|{qf}|dev|{i}", {"brief": f"Question wordings that {meaning}. Angle: "
                                                  f"{WORD_ANGLES[(i * 5 + 3) % len(WORD_ANGLES)]}. Write 5 different questions.",
                                                  "slots": {}, "rules": rules}))
    return out


def gloss_items() -> list:
    out = []
    for c in T.CLASSES:
        for part, n, k in (("train", GLOSS_ITEMS, GLOSS_TEXTS), ("dev", GLOSS_ITEMS_DEV, 5)):
            for i in range(n):
                out.append((f"gloss|{c}|{part}|{i}", {
                    "brief": f"Instruction phrases for this meaning: {T.MEANING[c]}. Style {i + 1}: "
                             f"{('very short', 'full clause', 'passive voice', 'plain verb phrase', 'formal', 'casual', 'starts with a different verb', 'about the outcome for the requester')[i % 8]}. "
                             f"Write {k} different phrases.",
                    "meaning": T.MEANING[c], "slots": {},
                    "rules": ["lower case, starts with a verb", "4 to 16 words", "no period, no colon, no quotes"]}))
    return out


def name_items() -> list:
    out = []
    for part, n, k in (("train", NAME_ITEMS, NAME_TEXTS), ("dev", NAME_ITEMS_DEV, 8)):
        for i in range(n):
            out.append((f"names|{part}|{i}", {"brief": f"Invented full names of people in Modern Standard Arabic script "
                                                    f"(set {i + 1}): {k} different names, mixing men and "
                                                    "women, ordinary family names from different regions."}))
    return out


def note_items() -> list:
    out = []
    for wf in AR_WF_TRAIN + ("purchase",):
        for c in T.CLASSES:
            parts = (("dev", 4, 5),) if wf == "purchase" else (("train", NOTE_ITEMS, NOTE_TEXTS), ("dev", NOTE_ITEMS_DEV, 4))
            for part, n, k in parts:
                for i in range(n):
                    out.append((f"note|{wf}|{c}|{part}|{i}", {
                        "brief": f"Context: {PERSON_CTX[wf]}. Situation: {SITUATION[c]}. Write {k} different "
                                 "one-sentence Arabic notes that state this situation as a fact.",
                        "slots": {},
                        "rules": ["Arabic letters and spaces only, one optional Arabic comma, final period", "3 to 14 words",
                                  "state a fact; no instruction, no decision, no names"]}))
    return out


TOPUP_ITEMS = 12            # round 3: yn_dneg train wordings fell below the floor after the polarity lint; one extra authoring task
TOPUP_JSON = "TOPUP.json"
TOPUP_RULES = ["use the words 'proposed action'", "exactly two negation words, both the single word 'not' (never n't), and no "
               "other negation of any kind",
               "open with 'Is it not the case that', 'Is it not true that', 'Is it not so that' or 'Is it not correct that', "
               "and put the second 'not' inside the that-clause",
               "end the that-clause with a POSITIVE word about the action such as right, correct, sound, fitting or the "
               "proper call; never end it with wrong, mistake, error, bad, incorrect or any other negative word",
               "no hedge (really, quite, probably, I think), no number word, no time word"]


def topup_items() -> list:
    meaning, _rules = WORD_BRIEFS["yn_dneg"]
    out = []
    for i in range(TOPUP_ITEMS):
        out.append((f"wording|yn_dneg|train|T{i}", {"brief": f"Question wordings that {meaning}. Angle: "
                                                   f"{WORD_ANGLES[(i * 3 + 1) % len(WORD_ANGLES)]}. Write {WORD_TEXTS} different questions.",
                                                   "slots": {}, "rules": TOPUP_RULES}))
    return out


def write_topup(root: Path = AUTHOR) -> list:
    b = chunker.make_batch("author_wording", F, topup_items(), seed=f"{F}-author-{VERSION}-wordings-topup",
                           prompt=PROMPTS["wordings"], max_items=13, forbid_strings=FORBID)
    for c in b.chunks:
        c["instructions"] = PROMPTS["wordings"]
        c["answer_format"] = ANSWER_TEXTS
        c["answer_file"] = str(Path(root) / b.answer_path(c["task_id"]))
    files = dict(b.files())
    tasks = task_list([("wordings_topup", b)], root)
    files[TOPUP_JSON] = json.dumps({"family": F, "version": VERSION, "n_tasks": len(tasks), "tasks": tasks,
                                    "batches": {"wordings_topup": b.batch_id}}, indent=1) + "\n"
    paths.write_files(root, files)
    return tasks


TOPUP2_JSON = "TOPUP2.json"
TOPUP2_DNEG_ITEMS = 24      # round 5: after G-LEX only 12 yn_dneg train wordings were admitted (floor 18); notes support D/E, hr D short
TOPUP2_RULES = ["use the words 'proposed action'", "exactly two negation words, both the single word 'not' (never n't), and no "
                "other negation of any kind",
                "open with 'Is it not the case that', 'Is it not true that', 'Is it not so that' or 'Is it not correct that', "
                "and put the second 'not' inside the that-clause",
                "after the second 'not' put a short phrase for a bad or unfitting outcome of the action (for example "
                "mistaken, a poor choice, off base, a mismatch for the facts, out of step with the request); the whole question "
                "asks, in a roundabout way, whether the action is fine for this request",
                "no hedge (really, quite, probably, I think), no number word, no time word"]
TOPUP2_NOTES = (("support", "D", 2), ("support", "E", 2), ("hr", "D", 2), ("access", "D", 1), ("access", "E", 1), ("hr", "E", 1))


def topup2_wording_items() -> list:
    meaning, _rules = WORD_BRIEFS["yn_dneg"]
    return [(f"wording|yn_dneg|train|U{i}", {"brief": f"Question wordings that {meaning}. Angle: "
                                             f"{WORD_ANGLES[(i * 5 + 2) % len(WORD_ANGLES)]}. Write {WORD_TEXTS} different questions.",
                                             "slots": {}, "rules": TOPUP2_RULES}) for i in range(TOPUP2_DNEG_ITEMS)]


def topup2_note_items() -> list:
    out = []
    for wf, c, n in TOPUP2_NOTES:
        for i in range(n):
            out.append((f"note|{wf}|{c}|train|U{i}", {
                "brief": f"Context: {PERSON_CTX[wf]}. Situation: {SITUATION[c]}. Write {NOTE_TEXTS + 2} different "
                         "one-sentence Arabic notes that state this situation as a fact, each with a different sentence shape.",
                "slots": {},
                "rules": ["Arabic letters and spaces only, one optional Arabic comma, final period", "3 to 14 words",
                          "state a fact; no instruction, no decision, no names"]}))
    return out


def write_topup2(root: Path = AUTHOR) -> list:
    bs = []
    for name, fn, pk, kind in (("wordings_topup2", topup2_wording_items, "wordings", "author_wording"),
                               ("notes_topup2", topup2_note_items, "notes", "author_lexicon")):
        b = chunker.make_batch(kind, F, fn(), seed=f"{F}-author-{VERSION}-{name}", prompt=PROMPTS[pk], max_items=13,
                               forbid_strings=FORBID)
        for c in b.chunks:
            c["instructions"] = PROMPTS[pk]
            c["answer_format"] = ANSWER_TEXTS
            c["answer_file"] = str(Path(root) / b.answer_path(c["task_id"]))
        bs.append((name, b))
    files = {}
    for _n, b in bs:
        files.update(b.files())
    tasks = task_list(bs, root)
    files[TOPUP2_JSON] = json.dumps({"family": F, "version": VERSION, "n_tasks": len(tasks), "tasks": tasks,
                                     "batches": {n: b.batch_id for n, b in bs}}, indent=1) + "\n"
    paths.write_files(root, files)
    return tasks


def topup_batches(root: Path = AUTHOR) -> dict:
    out = {}
    for fn in (TOPUP_JSON, TOPUP2_JSON):
        p = Path(root) / fn
        if p.is_file():
            out.update({n: batch_from_disk(root, bid) for n, bid in json.loads(p.read_text(encoding="utf-8"))["batches"].items()})
    return out


BATCHES = (   # (name, chunker kind, items fn, max items per chunk)
    ("wordings", "author_wording", wording_items, 13),
    ("glosses", "author_lexicon", gloss_items, 14),
    ("names", "author_pack", name_items, 10),
    ("notes", "author_lexicon", note_items, 14),
)
FORBID = tuple(ALL_LABEL_STRINGS)


def build_batches(root: Path = AUTHOR) -> list:
    out = []
    for name, kind, fn, size in BATCHES:
        b = chunker.make_batch(kind, F, fn(), seed=f"{F}-author-{VERSION}-{name}", prompt=PROMPTS[name],
                               max_items=size, forbid_strings=FORBID if name in ("wordings", "notes", "names") else ())
        for c in b.chunks:
            c["instructions"] = PROMPTS[name]
            c["answer_format"] = ANSWER_NAMES if name == "names" else ANSWER_TEXTS
            c["answer_file"] = str(Path(root) / b.answer_path(c["task_id"]))
        out.append((name, b))
    n = sum(len(b.chunks) for _, b in out)
    if n > MAX_TASKS:
        raise chunker.ChunkError(f"{n} authoring tasks > {MAX_TASKS}")
    return out


def task_list(batches: list, root: Path = AUTHOR) -> list:
    return [{"task_file": str(Path(root) / b.chunk_path(c["task_id"])), "answer_file": c["answer_file"],
             "kind": f"{b.kind}:{name}"} for name, b in batches for c in b.chunks]


def write_tasks(root: Path = AUTHOR) -> list:
    batches = build_batches(root)
    files = {}
    for _n, b in batches:
        files.update(b.files())
    tasks = task_list(batches, root)
    files["TASKS.json"] = json.dumps({"family": F, "version": VERSION, "n_tasks": len(tasks), "tasks": tasks,
                                      "batches": {n: b.batch_id for n, b in batches}}, indent=1) + "\n"
    paths.write_files(root, files)
    return tasks


# ------------------------------------------------------------------------------------------------ loading answers
def batch_from_disk(root: Path, batch_id: str) -> chunker.TaskBatch:
    root = Path(root)
    man = json.loads((root / "manifest" / f"{batch_id}.json").read_text(encoding="utf-8"))
    key = json.loads((root / "key" / f"{batch_id}.json").read_text(encoding="utf-8"))["key"]
    prompt = (root / "prompts" / f"{man['prompt_sha'][:16]}.txt").read_text(encoding="utf-8")
    b = chunker.TaskBatch(man["kind"], man["family"], batch_id, prompt, man["prompt_sha"], man["seed"])
    for t in man["tasks"]:
        c = json.loads((root / b.chunk_path(t["task_id"])).read_text(encoding="utf-8"))
        b.chunks.append(c)
        for it in c["items"]:
            b.task_of[it["qid"]] = t["task_id"]
    b.key = dict(key)
    return b


def read_answers(root: Path, b: chunker.TaskBatch) -> tuple:
    raw, probs = {}, []
    for c in b.chunks:
        p = Path(root) / b.answer_path(c["task_id"])
        if not p.is_file():
            probs.append(f"{c['task_id']}: no answer file")
            continue
        try:
            raw[c["task_id"]] = json.loads(p.read_text(encoding="utf-8"))
        except json.JSONDecodeError as e:
            probs.append(f"{c['task_id']}: answer file is not JSON ({e})")
    return raw, probs


def load_pieces(root: Path = AUTHOR, batches: dict | None = None, raw: dict | None = None, topup: bool = True) -> dict:
    """Load every authoring answer, lint it, dedup. Returns {"pools", "drops", "problems", "counts", "tasks"} where
    pools has the plugin's pool shape (wordings, glosses, names_ar, notes_ar, each {train, dev}). Nothing is written."""
    root = Path(root)
    if batches is None:
        tasks = json.loads((root / "TASKS.json").read_text(encoding="utf-8"))
        batches = {name: batch_from_disk(root, bid) for name, bid in tasks["batches"].items()}
        if topup:
            batches.update(topup_batches(root))
    pools = {"wordings": {qf: {"train": [], "dev": []} for qf in T.QFORM_MEANING},
             "glosses": {c: {"train": [], "dev": []} for c in T.CLASSES},
             "names_ar": {"train": [], "dev": []},
             "notes_ar": {wf: {c: {"train": [], "dev": []} for c in T.CLASSES} for wf in AR_WF_TRAIN + ("purchase",)}}
    drops, probs, seen = Counter(), [], {}
    meta = {}                                                  # text -> (task id, prompt sha)

    def add(bucket: list, text: str, why: list, iid: str, tid: str, psha: str, scope: str):
        norm = " ".join(text.split()).casefold()
        if why:
            drops[why[0].split(":")[0]] += 1
            probs.append(f"drop {iid}: {'; '.join(why)[:140]}: {text[:60]}")
            return
        if norm in seen:
            drops["duplicate"] += 1
            probs.append(f"drop {iid}: duplicate of {seen[norm]}")
            return
        seen[norm] = iid
        bucket.append(text)
        meta[text] = (tid, psha)

    for name, b in batches.items():
        got, p1 = (raw[name], []) if raw is not None else read_answers(root, b)
        probs += p1
        answers, p2 = chunker.load_answers(b, got)
        probs += [f"{name}: {p}" for p in p2]
        task_of = {iid: b.task_of[q] for q, iid in b.key.items()}
        for iid, ans in sorted(answers.items()):
            texts = (ans or {}).get("texts")
            if not isinstance(texts, list) or not all(isinstance(t, str) for t in texts):
                probs.append(f"{iid}: texts is not a list of strings")
                drops["bad_answer"] += 1
                continue
            parts = iid.split("|")
            tid, psha = task_of[iid], b.prompt_sha
            for t in texts:
                t = " ".join(t.split()) if name != "notes" else t.strip()
                if name.startswith("wordings"):
                    qf, part = parts[1], parts[2]
                    add(pools["wordings"][qf][part], t, wording_problems(qf, t), iid, tid, psha, part)
                elif name == "glosses":
                    c, part = parts[1], parts[2]
                    add(pools["glosses"][c][part], t, gloss_problems(c, t), iid, tid, psha, part)
                elif name == "names":
                    add(pools["names_ar"][parts[1]], t, ar_name_problems(t), iid, tid, psha, parts[1])
                else:                                          # notes, notes_topup2
                    wf, c, part = parts[1], parts[2], parts[3]
                    add(pools["notes_ar"][wf][c][part], t, ar_note_problems(t), iid, tid, psha, part)
    # a dev text never equals a train text (dedup above is global); counts
    counts = {"wordings": {qf: {p: len(v[p]) for p in v} for qf, v in pools["wordings"].items()},
              "glosses": {c: {p: len(v[p]) for p in v} for c, v in pools["glosses"].items()},
              "names_ar": {p: len(v) for p, v in pools["names_ar"].items()},
              "notes_ar": {wf: {c: {p: len(v[p]) for p in v} for c, v in byc.items()}
                           for wf, byc in pools["notes_ar"].items()}}
    return {"pools": pools, "drops": dict(drops), "problems": probs, "counts": counts, "meta": meta}


# ------------------------------------------------------------------------------------------------ probe collision (A59 (d))
def arabic_literals(path: Path) -> set:
    """Every Arabic-script string literal of a python file (a superset of its `to_ar` tables). Returns the set; callers
    report counts only."""
    out = set()
    tree = ast.parse(Path(path).read_text(encoding="utf-8"))
    for n in ast.walk(tree):
        if isinstance(n, ast.Constant) and isinstance(n.value, str) and re.search(r"[؀-ۿ]", n.value):
            out.add(unicodedata.normalize("NFC", n.value.strip()))
    return out


def probe_collisions(pools: dict, probe_py: Path) -> dict:
    """Count of pool strings that equal an Arabic literal of the probe generator (required: 0). No string is printed."""
    lits = arabic_literals(probe_py)
    mine = list(pools["names_ar"]["train"]) + list(pools["names_ar"]["dev"])
    for byc in pools["notes_ar"].values():
        for parts in byc.values():
            mine += parts["train"] + parts["dev"]
    hit = sorted({m for m in mine if unicodedata.normalize("NFC", m.strip()) in lits})
    return {"probe_arabic_literals": len(lits), "pool_arabic_items": len(mine), "collisions": len(hit)}


# ------------------------------------------------------------------------------------------------ the registry for G-LEX
def registry_for(pools: dict) -> LexiconRegistry:
    """Every form of the family: labels, flag values, glosses, notes, wordings (pending until two reads agree)."""
    return PLG.build_registry(pools, standin=False)


def names_registry(pools: dict) -> LexiconRegistry:
    reg = LexiconRegistry(F + "-names")
    reg.declare("name.person", "other", "an invented full name of a person")
    reg.declare("x.company", "other", "the name of a company or an organisation")
    reg.declare("x.place", "other", "the name of a city, a country or a place")
    reg.declare("x.phrase", "other", "an ordinary phrase or sentence that is not a name")
    seen = set()
    for part, held in (("train", False), ("dev", True)):
        for t in pools["names_ar"][part]:
            if t not in seen:
                seen.add(t)
                reg.add(t, "name.person", family=F, held_out=held)
    return reg


EXTRACT_PROMPT = (
    "Each item gives a short text (a word, a phrase, a record line, a note in Arabic, or a question) and a list of "
    "meanings. Pick the ONE meaning in the list that the text expresses best, judging from the text alone: for a "
    "record line such as 'name: value', the line tells what should happen to the request; for a question, say what "
    "a yes answer would mean. If two seem close, pick the one that matches the exact words. Read the items in this "
    "file only; do not open any other file. Write a JSON array to the answer file, one object per item: "
    '{"qid": "<the item qid>", "choice": "<the chosen meaning, copied exactly>"}. Write nothing else in the file.')


def extraction_batches(reg: LexiconRegistry, root: Path = EXTRACT, tag: str = "main", only: set | None = None) -> list:
    fids = sorted(fid for fid, f in reg.forms.items() if f.unit_ok and reg.status(fid) == "pending"
                  and (only is None or fid in only))
    if not fids:
        return []
    n_reads = max(reg.forms[f].required for f in fids)
    out = []
    for r in range(n_reads):
        items = reg.lexicon_items([f for f in fids if reg.forms[f].required > r], seed=f"{F}-glex-{VERSION}-{tag}-r{r}")
        b = chunker.make_batch("extract_lex", F, items, seed=f"{F}-glex-{VERSION}-{tag}-read{r}", prompt=EXTRACT_PROMPT)
        for c in b.chunks:
            c["instructions"] = EXTRACT_PROMPT
            c["answer_file"] = str(Path(root) / b.answer_path(c["task_id"]))
        out.append((f"{tag}-read{r}", b))
    return out


def record_extractions(reg: LexiconRegistry, batches: list, root: Path = EXTRACT, raw: dict | None = None) -> dict:
    stats, probs = Counter(), []
    for name, b in batches:
        got, p1 = (raw[name], []) if raw is not None else read_answers(root, b)
        probs += p1
        answers, p2 = chunker.load_answers(b, got)
        probs += p2
        task_of = {iid: b.task_of[q] for q, iid in b.key.items()}
        for fid, ans in answers.items():
            f = reg.forms[fid]
            choice = " ".join(str((ans or {}).get("choice", "")).split())
            sem = next((s.sem_id for s in reg.sems.values() if s.kind == f.kind
                        and " ".join(s.meaning.split()).casefold() == choice.casefold()), None)
            reg.record_extraction(fid, f"haiku:{task_of[fid]}", sem)
            stats["agree" if sem == f.sem_id else "disagree"] += 1
    return {"reads": dict(stats), "problems": probs, "status": dict(Counter(reg.status(f) for f in reg.forms))}


# ------------------------------------------------------------------------------------------------ freeze / load
def admitted_pools(pools: dict, reg: LexiconRegistry, names_reg: LexiconRegistry) -> dict:
    """The pools restricted to admitted pieces (wordings, glosses, notes by registry status; names by names registry)."""
    ok = {_n(f.text) for i, f in reg.forms.items() if reg.status(i) == "admitted"}
    nok = {_n(f.text) for i, f in names_reg.forms.items() if names_reg.status(i) == "admitted"}
    keep = lambda lst, s: [t for t in lst if _n(t) in s]  # noqa: E731
    return {"wordings": {qf: {p: keep(v[p], ok) for p in v} for qf, v in pools["wordings"].items()},
            "glosses": {c: {p: keep(v[p], ok) for p in v} for c, v in pools["glosses"].items()},
            "names_ar": {p: keep(v, nok) for p, v in pools["names_ar"].items()},
            "notes_ar": {wf: {c: {p: keep(v[p], ok) for p in v} for c, v in byc.items()}
                         for wf, byc in pools["notes_ar"].items()}}


def _n(t: str) -> str:
    return " ".join(str(t).casefold().split())


def shortfalls(ad: dict) -> list:
    out = []
    for qf, want in FLOORS["wording"].items():
        have = len(ad["wordings"][qf]["train"])
        if have < want:
            out.append(f"wording {qf}: {have} < {want}")
    for qf, v in ad["wordings"].items():
        if len(v["dev"]) < FLOORS["wording_dev"]:
            out.append(f"wording dev {qf}: {len(v['dev'])} < {FLOORS['wording_dev']}")
    for c, v in ad["glosses"].items():
        if len(v["train"]) < FLOORS["gloss"]:
            out.append(f"gloss {c}: {len(v['train'])} < {FLOORS['gloss']}")
        if len(v["dev"]) < FLOORS["gloss_dev"]:
            out.append(f"gloss dev {c}: {len(v['dev'])} < {FLOORS['gloss_dev']}")
    for p, want in (("train", FLOORS["names_ar"]), ("dev", FLOORS["names_ar_dev"])):
        if len(ad["names_ar"][p]) < want:
            out.append(f"names_ar {p}: {len(ad['names_ar'][p])} < {want}")
    for wf, byc in ad["notes_ar"].items():
        for c, v in byc.items():
            for p, want in (("train", FLOORS["note"]), ("dev", FLOORS["note_dev"])):
                if wf == "purchase" and p == "train":
                    continue
                if len(v[p]) < want:
                    out.append(f"notes {wf}/{c}/{p}: {len(v[p])} < {want}")
    return out


POOL_FILES = ("wordings.jsonl", "glosses.jsonl", "notes_ar.jsonl", "names_ar.jsonl")


def pools_to_records(ad: dict) -> dict:
    """{file: [record]}: one record per piece with a stable id (g13_c2 reads each record of pools/ as a template, so a
    G-TPL hit quarantines one piece); load_pools() is the inverse."""
    def rid(kind, text):
        return f"T46-{kind}-{_sha(text)[:10]}"
    out = {"wordings.jsonl": [], "glosses.jsonl": [], "notes_ar.jsonl": [], "names_ar.jsonl": []}
    for qf, v in sorted(ad["wordings"].items()):
        for part in ("train", "dev"):
            out["wordings.jsonl"] += [{"wording_id": rid("W", t), "qform": qf, "part": part, "text": t} for t in v[part]]
    for c, v in sorted(ad["glosses"].items()):
        for part in ("train", "dev"):
            out["glosses.jsonl"] += [{"id": rid("G", t), "cls": c, "part": part, "text": t} for t in v[part]]
    for wf, byc in sorted(ad["notes_ar"].items()):
        for c, v in sorted(byc.items()):
            for part in ("train", "dev"):
                out["notes_ar.jsonl"] += [{"id": rid("N", t), "wf": wf, "cls": c, "part": part, "text": t} for t in v[part]]
    for part in ("train", "dev"):
        out["names_ar.jsonl"] += [{"id": rid("A", t), "part": part, "text": t} for t in ad["names_ar"][part]]
    return out


def records_to_pools(recs: dict, drop_ids: set = frozenset()) -> dict:
    """The plugin's pool dict from the record files; a record whose id is in `drop_ids` (a G13-seed quarantine) is left out."""
    ad = {"wordings": {qf: {"train": [], "dev": []} for qf in T.QFORM_MEANING},
          "glosses": {c: {"train": [], "dev": []} for c in T.CLASSES}, "names_ar": {"train": [], "dev": []},
          "notes_ar": {wf: {c: {"train": [], "dev": []} for c in T.CLASSES} for wf in AR_WF_TRAIN + ("purchase",)}}
    for r in recs["wordings.jsonl"]:
        if r["wording_id"] not in drop_ids:
            ad["wordings"][r["qform"]][r["part"]].append(r["text"])
    for r in recs["glosses.jsonl"]:
        if r["id"] not in drop_ids:
            ad["glosses"][r["cls"]][r["part"]].append(r["text"])
    for r in recs["notes_ar.jsonl"]:
        if r["id"] not in drop_ids:
            ad["notes_ar"][r["wf"]][r["cls"]][r["part"]].append(r["text"])
    for r in recs["names_ar.jsonl"]:
        if r["id"] not in drop_ids:
            ad["names_ar"][r["part"]].append(r["text"])
    return ad


def _jsonl(rows: list) -> str:
    return "".join(json.dumps(r, ensure_ascii=False, sort_keys=True) + "\n" for r in rows)


def freeze(pieces: dict, reg: LexiconRegistry, names_reg: LexiconRegistry, root: Path = POOLS,
           probe_py: Path | None = None) -> dict:
    ad = admitted_pools(pieces["pools"], reg, names_reg)
    recs = pools_to_records(ad)
    files = {k: _jsonl(v) for k, v in recs.items()}
    files["lexicon.json"] = json.dumps(reg.to_json(), ensure_ascii=False, indent=1, sort_keys=True) + "\n"
    files["names_lexicon.json"] = json.dumps(names_reg.to_json(), ensure_ascii=False, indent=1, sort_keys=True) + "\n"
    man = {"family": F, "version": VERSION, "sha256": {k: _sha(v) for k, v in files.items()},
           "counts": {k: len(v) for k, v in recs.items()},
           "lexicon_status": dict(Counter(reg.status(f) for f in reg.forms)),
           "names_status": dict(Counter(names_reg.status(f) for f in names_reg.forms)),
           "shortfalls": shortfalls(ad), "drops": pieces["drops"],
           "probe_collisions": probe_collisions(ad, probe_py) if probe_py else "not run"}
    files["MANIFEST.json"] = json.dumps(man, ensure_ascii=False, indent=1) + "\n"
    paths.write_files(root, files)
    return man


def frozen_pools_exist(root: Path = POOLS) -> bool:
    return all((Path(root) / n).is_file() for n in POOL_FILES + ("lexicon.json", "MANIFEST.json"))


def pools_manifest_sha(root: Path = POOLS) -> str:
    return _sha((Path(root) / "MANIFEST.json").read_text(encoding="utf-8"))


G13_QUARANTINE = HERE.parent.parent / "zed_orch" / "g13_seed" / "T46.quarantine.json"


def g13_quarantined_ids(path: Path = G13_QUARANTINE) -> set:
    """Pool record ids a G13-seed run quarantined (the TEMPLATE only, A37 e / A38): zed_orch/g13_seed/T46.quarantine.json,
    {"quarantine": [{"template_id": ...}]}; none when the file does not exist."""
    p = Path(path)
    if not p.is_file():
        return set()
    return {q["template_id"] for q in json.loads(p.read_text(encoding="utf-8")).get("quarantine", [])}


def load_pools(root: Path = POOLS, quarantine: set | None = None) -> tuple:
    """(pools, registry) from the frozen folder; refuses a file whose sha256 differs from the manifest. Quarantined pieces are
    left out of the pools (the registry keeps their forms, but no row can draw them)."""
    root = Path(root)
    man = json.loads((root / "MANIFEST.json").read_text(encoding="utf-8"))
    for n, want in man["sha256"].items():
        got = _sha((root / n).read_text(encoding="utf-8"))
        if got != want:
            raise RuntimeError(f"{root / n}: sha256 {got[:12]} != manifest {want[:12]} (frozen pool changed)")
    recs = {n: [json.loads(x) for x in (root / n).read_text(encoding="utf-8").splitlines() if x.strip()] for n in POOL_FILES}
    pools = records_to_pools(recs, g13_quarantined_ids() if quarantine is None else set(quarantine))
    reg = LexiconRegistry.from_json(json.loads((root / "lexicon.json").read_text(encoding="utf-8")))
    return pools, reg


def load_plugin(root: Path = POOLS) -> tuple:
    pools, reg = load_pools(root)
    ctx = PLG.make_ctx(pools, registry=reg)
    return PLG.T46Plugin(lexicon=reg, pools=pools), ctx


# ------------------------------------------------------------------------------------------------ CLI
def all_extraction_batches() -> list:
    """Every G-LEX read batch on disk: TASKS.json (main + names) and every TASKS_*.json (top-ups, pending rounds), in file order."""
    bs = []
    for fn in ["TASKS.json"] + sorted(p.name for p in EXTRACT.glob("TASKS_*.json")):
        p = EXTRACT / fn
        if p.is_file():
            bs += [(n, batch_from_disk(EXTRACT, bid)) for n, bid in json.loads(p.read_text(encoding="utf-8"))["batches"].items()]
    return bs


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("step", choices=("write-tasks", "write-topup", "write-topup2", "lint", "extract-tasks", "extract-topup",
                                     "extract-topup2", "extract-pending", "admit"))
    ap.add_argument("--probe-py", default=None, help="path of the probe generator (Arabic literal collision check)")
    a = ap.parse_args(argv)
    if a.step == "write-tasks":
        print(json.dumps(write_tasks(), indent=1))
        return 0
    if a.step == "write-topup":
        print(json.dumps(write_topup(), indent=1))
        return 0
    if a.step == "write-topup2":
        print(json.dumps(write_topup2(), indent=1))
        return 0
    pieces = load_pieces(topup=a.step != "extract-tasks")      # the main reads stay valid: they never include the top-up pieces
    if a.step == "lint":
        print(json.dumps({"counts": pieces["counts"], "drops": pieces["drops"], "problems": pieces["problems"][:200]},
                         indent=1, ensure_ascii=False))
        return 0
    reg, nreg = registry_for(pieces["pools"]), names_registry(pieces["pools"])
    reg.unit_test_all()
    nreg.unit_test_all()
    if a.step == "extract-pending":
        # every form that still has no recorded read (new flag candidates, new top-up pieces) after replaying all answered reads
        tag = "p%d" % (max([int(x.stem[7:]) for x in EXTRACT.glob("TASKS_P*.json")] or [0]) + 1)
        done = [(n, b) for n, b in all_extraction_batches() if n.startswith(("main", "topup", "flags", "p"))]
        scratch = registry_for(pieces["pools"])
        scratch.unit_test_all()
        record_extractions(scratch, done)
        pend = {f for f in scratch.forms if scratch.status(f) == "pending" and not scratch.forms[f].extractions}
        bs = extraction_batches(reg, tag=tag, only=pend)
        files = {}
        for _n, b in bs:
            files.update(b.files())
        tasks = [{"task_file": str(EXTRACT / b.chunk_path(c["task_id"])), "answer_file": c["answer_file"],
                  "kind": f"extract_lex:{n}"} for n, b in bs for c in b.chunks]
        files[f"TASKS_{tag.upper()}.json"] = json.dumps({"family": F, "n_tasks": len(tasks), "tasks": tasks, "n_forms": len(pend),
                                                         "batches": {n: b.batch_id for n, b in bs}}, indent=1) + "\n"
        paths.write_files(EXTRACT, files)
        print(json.dumps({"tag": tag, "forms": len(pend), "tasks": tasks}, indent=1))
        return 0
    if a.step in ("extract-topup", "extract-topup2"):
        r2 = a.step == "extract-topup2"
        if r2:                                              # forms already read (main + round-1 top-up) are excluded
            tb = {n: b for n, b in topup_batches().items() if not n.endswith("topup2")}
            mt = json.loads((AUTHOR / "TASKS.json").read_text(encoding="utf-8"))["batches"]
            base = load_pieces(batches={**{n: batch_from_disk(AUTHOR, bid) for n, bid in mt.items()}, **tb})
        else:
            base = load_pieces(topup=False)
        main_f = set(registry_for(base["pools"]).forms)
        bs = extraction_batches(reg, tag="topup2" if r2 else "topup", only=set(reg.forms) - main_f)
        files = {}
        for _n, b in bs:
            files.update(b.files())
        tasks = [{"task_file": str(EXTRACT / b.chunk_path(c["task_id"])), "answer_file": c["answer_file"],
                  "kind": f"extract_lex:{n}"} for n, b in bs for c in b.chunks]
        files["TASKS_TOPUP2.json" if r2 else "TASKS_TOPUP.json"] = json.dumps({"family": F, "n_tasks": len(tasks), "tasks": tasks,
                                                "batches": {n: b.batch_id for n, b in bs}}, indent=1) + "\n"
        paths.write_files(EXTRACT, files)
        print(json.dumps(tasks, indent=1))
        return 0
    if a.step == "extract-tasks":
        bs = extraction_batches(reg, tag="main") + extraction_batches(nreg, tag="names")
        files = {}
        for _n, b in bs:
            files.update(b.files())
        tasks = [{"task_file": str(EXTRACT / b.chunk_path(c["task_id"])), "answer_file": c["answer_file"],
                  "kind": f"extract_lex:{n}"} for n, b in bs for c in b.chunks]
        files["TASKS.json"] = json.dumps({"family": F, "n_tasks": len(tasks), "tasks": tasks,
                                          "batches": {n: b.batch_id for n, b in bs}}, indent=1) + "\n"
        paths.write_files(EXTRACT, files)
        print(json.dumps(tasks, indent=1))
        return 0
    bs = all_extraction_batches()
    main_b = [(n, b) for n, b in bs if n.startswith(("main", "topup", "p"))]
    name_b = [(n, b) for n, b in bs if n.startswith("names")]
    rec = record_extractions(reg, main_b)
    rec_n = record_extractions(nreg, name_b)
    man = freeze(pieces, reg, nreg, probe_py=Path(a.probe_py) if a.probe_py else None)
    print(json.dumps({"extractions": rec, "name_extractions": rec_n, "manifest": man}, indent=1, default=str))
    return 0


if __name__ == "__main__":
    sys.exit(main())
