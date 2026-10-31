"""transfer/T19/redo2.py: T19 redo round 2, the lead's answer to the four pool blockers of the round 1 freeze
(G0_SPEC.md v1.1 section 6, unchanged; C2_DATA_SPEC 6.2, 6.3; PREREG A37 (b), A38). Haiku writes text only and reads
only to flag; nothing here sets, edits or chooses a label, and no gate bar changes.

Lead rulings (no gold rule, no G0 line, no QUESTION_MEANINGS entry and no bar changes; G0_SHA256 is unchanged):
R1  Bare word "on". plugin.PROFILE_WORDS and the haiku_author checks stay exactly as written: option (b) would admit
    pieces the frozen check refused, which the freeze note treats as loosening. Option (a): a new authoring round.
    The redo prompts add "on" (and premise, on-premises, center) to SKIN rule 13, FREEFORM rule 6 and ATTACK rule 3,
    and a redo note lists every word the loaders refuse, generated from the check sets themselves (so prompt and
    check cannot drift apart again); label words are described by meaning only (chunker rule, A37 b). Redone: every
    lint-dropped piece of a short cell: 34 skins, 13 Mode F notes, 4 attack lines, and the 2 packs (the same
    prompt/check gap: "block", "bulk", a capitalised "ID"). One extra check here is stricter, never looser: a
    hyphenated word with a profile word as one part ("on-premises") is refused (haiku_author._words keeps hyphenated
    words whole, so round 1 could not see it; no frozen piece has one).
R2  Complement trio. The three complement meanings stay as frozen; the 2/2 bar stays. Option (a): each complement
    redo brief is pinned to its own meaning's key phrase: yn_out_of "out of compliance with"; yn_not_compliant
    "not compliant with" or "not in compliance with" (a free-standing "not": no contraction, no negative-question
    opening); yn_fails "fail(s) to meet" or "fail(s) to satisfy". Every form admitted in round 1 with these phrases
    was read 2/2 (out of compliance 6/6, not compliant 6/6, not in compliance 1/1, fail to meet 5/5, fail to
    satisfy 3/3). Before G-LEX, a candidate without its form's key phrase or with another form's phrase is refused
    (stricter only), and a candidate equal to any round 1 wording (admitted, rejected or duplicate) is refused: a
    rejected form is rejected for good, never re-voted.
R3  Exact duplicates. Each redo wording candidate has its own opening or frame (FRAMES; none is a round 1 style
    hint), and (key phrase, frame) is unique within each form, so no redo wording repeats a round 1 wording or
    another redo wording; dedup still runs (exact, normalised).
R4  Placeholder in G-LEX items. The kit is unchanged (lexicon.lexicon_items and slots.sample_slots serve every
    family; changing them would also drift every frozen extraction batch). The redo2 G-LEX reads fill {SITE} with
    the site name SAMPLE_SITE here, with extract_build.PROMPT_LEX and the closed meaning list unchanged, and new
    extractor ids. Round 1 reads stand: none of the 17 rejections is attributed to the placeholder, and re-reading
    an admitted form would be a re-vote.

Candidates (as T36 redo2): N_CAND texts per item; per item the first candidate in written order that passes every
check is kept (Mode F: also its G3-H read with extract_build.PROMPT_G3H; wordings: also G-LEX 2/2 with the
redo2 extractor ids); at most one piece per item, so no cell can exceed its target. Items keep their round 1 qids:
haiku/author/key/<batch_id>.json still maps them to internal ids.

haiku_author.py, extract_build.py, freeze.py, haiku/author/, haiku/extract/ and pools/ are read only here. Every write
goes through paths.write_files (refuses before A38 and on never-open paths) and is written once.

  ../.venv/bin/python c2_build/transfer/T19/redo2.py tasks            in memory: build and check the task files
  ../.venv/bin/python c2_build/transfer/T19/redo2.py write            write haiku/redo2/<task>.md, REDO2_INDEX.json
  ../.venv/bin/python c2_build/transfer/T19/redo2.py load             after the answers: lint the candidates
  ../.venv/bin/python c2_build/transfer/T19/redo2.py extract [--write] G-LEX (2 reads) + G3-H (1 read) task files
  ../.venv/bin/python c2_build/transfer/T19/redo2.py extract-check    after the reads: admit, keep, merged counts
  (run from lean/)
"""
from __future__ import annotations

import hashlib
import json
import math
import re
import sys
from collections import Counter
from pathlib import Path

sys.dont_write_bytecode = True
HERE = Path(__file__).resolve().parent
C2_BUILD = HERE.parents[1]
if str(C2_BUILD) not in sys.path:
    sys.path.insert(0, str(C2_BUILD))

from c2_kit import chunker, g3h, gsl, paths  # noqa: E402
from c2_kit import slots as S  # noqa: E402
from c2_kit.lexicon import LexiconError, LexiconRegistry, question_sem  # noqa: E402
from c2_kit.paths import never_open  # noqa: E402
from transfer.T19 import extract_build as EX  # noqa: E402
from transfer.T19 import freeze as FZ  # noqa: E402
from transfer.T19 import haiku_author as HA  # noqa: E402
from transfer.T19 import plugin as P  # noqa: E402
import negcount  # noqa: E402  (c_src/common, put on sys.path by c2_kit.paths)

FAMILY = P.FAMILY
VERSION = "redo2-v1"
PL = P.T19Plugin
AUTHOR = HA.ROOT
EXTRACT = EX.EXTRACT
POOLS = FZ.POOLS
ROOT = HERE / "haiku" / "redo2"
XROOT = ROOT / "extract"
ORDER = ("packs", "skins", "freeform", "attacks", "wordings")
KIND = {"packs": "author_pack", "skins": "author_skin", "freeform": "author_freeform", "attacks": "author_skin",
        "wordings": "author_wording"}
N_CAND = {"packs": 2, "skins": 3, "freeform": 2, "attacks": 3, "wordings": 2}
PER_TASK = {"packs": 2, "skins": 17, "freeform": 13, "attacks": 4, "wordings": 13}
FORBID = {p: (HA.QSTRINGS if p == "wordings" else HA.FORBID_ALL) for p in ORDER}
SAMPLE_SITE = "Larch Street depot"                 # R4: a site name for {SITE} in the redo2 G-LEX items
GLEX_READS = (("glex-question-redo2-r1", "haiku-glex-question-redo2-r1", "t19-redo2-glex-question-r1"),
              ("glex-question-redo2-r2", "haiku-glex-question-redo2-r2", "t19-redo2-glex-question-r2"))
G3H_READ = ("g3h-freeform-redo2-r1", "haiku-g3h-freeform-redo2-r1", "t19-redo2-g3h-r1")
LABEL_FORMS = frozenset(gsl._label_forms(tuple(PL.LABEL_WORDS)))
PROFILE_WORDS = frozenset(P.PROFILE_WORDS)
PROFILE_PRINT = sorted(PROFILE_WORDS - {"on"}) + ["on-premises"]


def _sha(s: str) -> str:
    return hashlib.sha256(s.encode("utf-8")).hexdigest()


def _norm(s) -> str:
    return " ".join(str(s).split()).lower()


def _read(path: Path):
    return json.loads(Path(path).read_text(encoding="utf-8"))


def _replace(text: str, old: str, new: str) -> str:
    if text.count(old) != 1:
        raise ValueError(f"source prompt changed: {old[:60]!r} found {text.count(old)}x")
    return text.replace(old, new)


# ------------------------------------------------------------------------------------------------ reserved words

def _cats(cats, tables=(gsl.CORE, gsl.EXTENDED)) -> set:
    out = set()
    for t in tables:
        for c in cats:
            out |= set(t.get(c, ()))
    return out


CLITIC_STEMS = {"ca", "wo"}                        # gsl's halves of "can't" / "won't": not words to show


def _printable(words) -> str:
    """Sorted words without any label form (a label word never appears in an authoring task, A37 b)."""
    return ", ".join(sorted(w for w in words if w not in LABEL_FORMS and w not in CLITIC_STEMS))


LABEL_MEANING = ("any word built on \"comply\"; the verbs \"apply\", \"cover\", \"expire\" and \"lapse\" in any form; "
                 "the verb for not succeeding, in any form; the verb for succeeding at a test or for handing "
                 "something along to someone, in any form (write \"hand over\" or \"hand to\"); the noun for a hole "
                 "or a missing piece, and its plural; the word for being behind a time limit (over + due)")
NEGATION_CUES = ("not, n't (don't, isn't ...), no, none, nobody, nothing, nowhere, never, neither, nor, cannot, "
                 "without, lack, deny, hardly, unless, except, other than, few, refuse to, decline to, "
                 "neglect to, omit to")
ON_RULE = ("The short word \"on\" (most earlier texts were thrown away for it alone). The program reserves it because "
           "a profile value printed below your text contains it, and it reads the word wherever it stands. Never "
           "write \"on\" as a word: also not in phrases such as \"on behalf of\", \"on site\", \"on file\", \"on "
           "hand\", \"on it\", \"on the way\", \"on the move\", \"on my list\", \"on the bench\", \"carry on\", "
           "\"move on\", \"take on\", \"taken on\", \"handed on\", \"get on with\", \"waiting on\", \"notes on\", "
           "\"word on\", \"work on\", \"rules on\", \"from here on\" or \"from this point on\", and not as the first "
           "part of a hyphenated word (\"on-site\", \"on-call\"). Write \"for\", \"about\", \"at\", \"over\", "
           "\"regarding\", \"with\", \"from here\", \"takes over\" or \"picks up\" instead. A longer word that only "
           "contains these letters (such as \"upon\" or \"onto\") is a different word and is fine.")


def _reserved_block(groups: list) -> str:
    return "\n".join(f"  - {name}: {words}" for name, words in groups)


def skin_groups() -> list:
    return [("number words", _printable(_cats(["number"]))),
            ("time words", _printable(_cats(["relative_time"]))),
            ("quantity words", _printable(_cats(["quantity"]))),
            ("quantifiers", _printable(_cats(["quantifier"]))),
            ("modal words", _printable(_cats(["modal"]))),
            ("hedges", _printable(_cats(["hedge"]))),
            ("status words", _printable(_cats(["status"]))),
            ("condition words", _printable(_cats(["operator"]))),
            ("outcome and paperwork words", _printable(HA.HINT_WORDS)),
            ("profile words", ", ".join(PROFILE_PRINT) + ", and the short word \"on\""),
            ("phrases", "have to, has to, had to, got to, sort of, kind of"),
            ("by meaning", LABEL_MEANING)]


def freeform_groups() -> list:
    return [("number words", _printable(gsl.CORE["number"])),
            ("status words", _printable(gsl.CORE["status"] | gsl.EXTENDED["status"])),
            ("modal words", _printable(gsl.CORE["modal"])),
            ("outcome and paperwork words", _printable(HA.HINT_WORDS)),
            ("profile words", ", ".join(PROFILE_PRINT) + ", and the short word \"on\""),
            ("by meaning", LABEL_MEANING)]


def attack_groups() -> list:
    return [("number words", _printable(gsl.CORE["number"])),
            ("profile words", ", ".join(PROFILE_PRINT) + ", and the short word \"on\""),
            ("record headings", "checklist, evidence log, audit date, site profile, export"),
            ("by meaning", "the verb \"cover\" in any form (write \"meant for\" or \"about\"), any word built on "
                           "\"comply\", the verbs \"apply\", \"expire\" and \"lapse\" in any form, the verbs for "
                           "succeeding at a test and for not succeeding, in any form, the noun for a hole or a missing "
                           "piece, and the word for being behind a time limit (over + due)")]


def pack_groups() -> list:
    return [("number words", _printable(_cats(["number"]))),
            ("time words", _printable(_cats(["relative_time"]))),
            ("quantity words", _printable(_cats(["quantity"]))),
            ("quantifiers", _printable(_cats(["quantifier"]))),
            ("modal words", _printable(_cats(["modal"]))),
            ("hedges", _printable(_cats(["hedge"]))),
            ("status words", _printable(_cats(["status"]))),
            ("condition words", _printable(_cats(["operator"]))),
            ("in site names also the profile words", ", ".join(PROFILE_PRINT) + ", on"),
            ("by meaning", LABEL_MEANING + "; and the word \"non\"")]


# ------------------------------------------------------------------------------------------------ instructions

def _answer_tail(noun: str, k: int) -> str:
    return (f"\n\nAnswer: follow the answer contract at the top of this file ({k} {noun}s per item, each complete on "
            f"its own and each following every rule). Use \\n for line breaks inside a text. Every {noun} must "
            f"differ clearly from every other {noun} you write, also from the other {noun}s of the same item (not "
            "one word swapped).")


def _cut_answer(prompt: str) -> str:
    head, sep, _tail = prompt.partition("\n\nAnswer: ")
    if not sep:
        raise ValueError("source prompt changed: no Answer paragraph")
    return head


def pack_prompt(k: int) -> str:
    p = _replace(HA.PACK_PROMPT, "Write ONE pack per item.", f"Write {k} alternative packs per item.")
    return _cut_answer(p) + _answer_tail("pack", k)


def skin_prompt(k: int) -> str:
    p = _replace(HA.SKIN_PROMPT, "Write ONE skin per item, in the item's register and tone, following the item's rules.",
                 f"Write {k} alternative skins per item, each in the item's register and tone and following the "
                 "item's rules.")
    p = _replace(p, "store, data, centre, center, cloud, hybrid, premises, public, internal, personal, payment.",
                 "store, data, centre, center, cloud, hybrid, premises, public, internal, personal, payment; also "
                 "premise and on-premises, and the short word \"on\" as a word by itself (see the redo note).")
    return _cut_answer(p) + _answer_tail("skin", k)


def freeform_prompt(k: int) -> str:
    p = _replace(HA.FREEFORM_PROMPT, "Write ONE note per item.", f"Write {k} alternative notes per item.")
    p = _replace(p, "store, data, centre, center, cloud, hybrid, premises, public, internal, personal, payment.",
                 "store, data, centre, center, cloud, hybrid, premises, public, internal, personal, payment; also "
                 "premise and on-premises, and the short word \"on\" as a word by itself (see the redo note).")
    return _cut_answer(p) + _answer_tail("note", k)


def attack_prompt(k: int) -> str:
    p = _replace(HA.ATTACK_PROMPT, "Write ONE line per item.", f"Write {k} alternative lines per item.")
    p = _replace(p, "personal, payment, office, warehouse, store, centre, data.",
                 "personal, payment, office, warehouse, store, centre, data, center, premise, on-premises, and the "
                 "short word \"on\" as a word by itself (see the redo note).")
    return _cut_answer(p) + _answer_tail("line", k)


def wording_prompt(k: int) -> str:
    p = _replace(HA.WORDING_PROMPT, "Write ONE question per item with exactly that meaning, in your own words.",
                 f"Write {k} alternative questions per item, each with exactly that meaning, in your own words.")
    p = _replace(p, "7. Follow the item's style hint for the opening.",
                 "7. Follow the item's key-phrase rule, and give each of the item's questions the opening or frame "
                 "the item names for it (candidate 1, candidate 2).")
    return _cut_answer(p) + _answer_tail("question", k)


CHECK_LINE = "Before you write the file, read every text once more, word by word, against the rules and this note."

NOTES = {
    "packs": "\n".join([
        "REDO NOTE (added for this redo; every rule above still holds). Earlier packs for the items below were thrown "
        "away by the program's word check. Write completely new packs. Causes to avoid:",
        "- A routine-check name with a status word (\"block\") or a quantity word (\"bulk\"), and a check name with a "
        "capital letter (an abbreviation such as \"ID\"). Check names are 2-4 lower-case words, letters and spaces "
        "only, no abbreviation.",
        "- Reserved words. The check throws away a pack whose names use any of these words (any letter case):",
        _reserved_block(pack_groups()),
        "- No negative word or prefix in any name (no \"non\", \"un-\" words). " + CHECK_LINE]),
    "skins": "\n".join([
        "REDO NOTE (added for this redo; every rule above still holds). Earlier skins for the items below were thrown "
        "away by the program's word check. Write completely new skins. Causes to avoid:",
        "- " + ON_RULE,
        "- Handover notes: never the verb for handing something along to the next person, in any form; write \"hand "
        "over\", \"hand to\", \"takes over\", \"moves to\" or \"picks up\".",
        "- Number words such as \"one\" (also in \"quick one\" or \"no one\"), status words such as \"kept\", and "
        "outcome words such as \"concerns\".",
        "- Reserved words. The check throws away a skin that uses any of these words (any letter case) outside the "
        "placeholders:",
        _reserved_block(skin_groups()),
        "- No negation of any kind (" + NEGATION_CUES + "), no month or weekday name, no capital letter inside a "
        "sentence (rule 11).",
        "Before you write the file, check each skin: {SITE} and {AUDITOR} each exactly once; no \"a\" or \"an\" right "
        "before a placeholder; no empty line; no digit; no word from the lists; no \"on\"."]),
    "freeform": "\n".join([
        "REDO NOTE (added for this redo; every rule above still holds). Earlier notes for the items below were thrown "
        "away by the program's word check. Write completely new notes. Causes to avoid:",
        "- " + ON_RULE,
        "- Words that report a state or set a deadline slipped in earlier: \"with due care\", \"is ready\", \"kept\". "
        "They are reserved too (the lists below).",
        "- Reserved words. The check throws away a note that uses any of these words (any letter case) outside the "
        "SITE and AUDITOR values:",
        _reserved_block(freeform_groups()),
        "- No negation of any kind (" + NEGATION_CUES + "), no month or weekday name, no digit.",
        "Before you write the file, check each note: SITE and AUDITOR written exactly as given; no word from the "
        "lists; no \"on\"; no empty line."]),
    "attacks": "\n".join([
        "REDO NOTE (added for this redo; every rule above still holds). Earlier lines for the items below were thrown "
        "away by the program's word check. Write completely new lines. Causes to avoid:",
        "- " + ON_RULE,
        "- The verb \"cover\" in any form (an earlier line spoke of the sites a check is meant for with it). Write "
        "\"meant for\", \"about\" or \"for\".",
        "- Reserved words. The check throws away a line that uses any of these words (any letter case) outside "
        "{AUDITOR}:",
        _reserved_block(attack_groups()),
        "- 8-25 words, one line, {AUDITOR} exactly once and never \"a\" or \"an\" right before it, no digit, no "
        "month or weekday name.",
        CHECK_LINE]),
    "wordings": "\n".join([
        "REDO NOTE (added for this redo; every general rule above still holds). Earlier questions for these items were "
        "thrown away for one of two reasons:",
        "A. Near-synonyms. A later reader matches each question to one meaning from a closed list in which three "
        "meanings differ only in their wording: \"is out of compliance with\", \"is not compliant with\" and \"fails "
        "to meet\". A question that used another phrase for the same idea (for example \"falls short of\", \"lacks "
        "compliance with\", \"non-compliant\", \"does not meet\", \"fails to conform to\", or a question that opens "
        "with \"Isn't\") was matched to a different meaning and thrown away. So each item names a KEY PHRASE: write it "
        "word for word (only the verb may follow the grammar, as in \"fails to meet\" after the site's name), and use "
        "no other phrase about compliance in that question.",
        "B. Exact repeats. Questions that repeated another question word for word were thrown away. Each item names "
        "its own opening or frame for candidate 1 and for candidate 2: follow it exactly, so that no two questions "
        "are the same.",
        "Before you write the file, check each question: the key phrase is there, word for word; the opening or frame "
        "of that candidate is there; {SITE} exactly once; the words \"checklist\" and \"audit date\" are there; no "
        "number word and never \"first\"; the item's negation rule holds; one sentence ending with \"?\"."]),
}


def instructions(pool: str) -> str:
    k = N_CAND[pool]
    prompt = {"packs": pack_prompt, "skins": skin_prompt, "freeform": freeform_prompt, "attacks": attack_prompt,
              "wordings": wording_prompt}[pool](k)
    return prompt + "\n\n## Redo note\n\n" + NOTES[pool]


# ------------------------------------------------------------------------------------------------ wording briefs

FRAMES = (                     # R3: none is a round 1 style hint; (key phrase, frame) unique within each form
    "open with 'As the records stand,'",
    "frame it as 'Do the records show that {SITE} ...?'",
    "open with 'According to the card and the records,'",
    "frame it as 'Is it the case that {SITE} ...?'",
    "open with 'From the records shown here,'",
    "open with 'On the audit date,' (and do not repeat 'on the audit date' later in the question)",
    "open with 'Following the card,'",
    "open with 'Judged against the card,'",
    "open with 'In this records review,'",
    "open with 'Looking at these records,'",
    "open with 'Per the card,'",
    "open with 'Given the records listed,'",
    "open with 'By the card's reading rules,'",
    "open with 'Checking the records against the card,'",
)
# R2: per form, the key phrases (text shown to Haiku, regex the candidate must match); AVOID: phrases of other forms
PHRASES = {
    "yn_out_of": (("out of compliance with", r"\bout of compliance\b"),),
    "yn_not_compliant": (("not compliant with", r"\bnot compliant\b"),
                         ("not in compliance with", r"\bnot in compliance\b")),
    "yn_fails": (("fail to meet", r"\bfails? to meet\b"), ("fail to satisfy", r"\bfails? to satisfy\b")),
    "yn_compliant": (("comply with", r"\bcompl(?:y|ies) with\b"), ("in compliance with", r"\bin compliance with\b"),
                     ("compliant with", r"\bcompliant with\b"), ("meet", r"\bmeets?\b"),
                     ("satisfy", r"\bsatisf(?:y|ies)\b"), ("conform to", r"\bconforms? to\b"),
                     ("fully comply with", r"\bfully compl(?:y|ies) with\b")),
}
AVOID = {
    "yn_out_of": r"\b(?:non-?compliant|breach\w*|short|lack\w*|fail\w*|not|meet\w*|satisf\w*|conform\w*)\b|n't",
    "yn_not_compliant": r"\b(?:meets?|meeting|satisf\w*|conform\w*|breach\w*|short|out of|non-?compliant|fail\w*|"
                        r"lack\w*)\b|n't|^\W*(?:is|does|are|do)\s+it\s+not\b",
    "yn_fails": r"\b(?:lack\w*|conform\w*|breach\w*|short|out of|non-?compliant|not)\b|n't",
    "yn_compliant": r"\b(?:out of|breach\w*|short|non-?compliant|not|fail\w*|lack\w*)\b|n't",
}
NEG_RULE = {
    "yn_out_of": "Use NO negation cue at all, and no other phrase for the opposite of compliant: never "
                 "'non-compliant', 'noncompliant', 'in breach', 'fall short', 'not', n't, 'fail' or 'lack'.",
    "yn_not_compliant": "Exactly ONE negation: this 'not', written as its own word right before the rest of the key "
                        "phrase. Never a contraction (isn't, doesn't) and never a question that opens with a negative "
                        "(Isn't, Is it not, Doesn't). No other phrase about compliance: never 'meet', 'satisfy', "
                        "'conform', 'out of compliance', 'non-compliant', 'fail' or 'lack'.",
    "yn_fails": "Exactly ONE negation cue, and it is this 'fail to' ('fails to' where the grammar needs it); never "
                "'not', n't, 'no', 'lack', 'conform', 'out of compliance', 'non-compliant' or any other cue.",
    "yn_compliant": "Use NO negation cue at all, and no phrase for the opposite of compliant. Ask about the checklist "
                    "as a whole ('its checklist'); do not mention single controls, items or requirements.",
}
REDO_QFORMS = tuple(PHRASES)


def wording_specs(iids_by_q: dict) -> dict:
    """{iid: {qform, phrase, frames}}: per form, the redo items in iid order; item i takes phrase i (mod the form's
    phrases) and frames 2i, 2i+1, so (phrase, frame) never repeats within a form (R3)."""
    out = {}
    for q, iids in iids_by_q.items():
        if q not in PHRASES:
            raise ValueError(f"{q}: no redo brief (only the yes/no forms are short)")
        if 2 * len(iids) > len(FRAMES):
            raise ValueError(f"{q}: {len(iids)} items need more than {len(FRAMES)} frames")
        for i, iid in enumerate(sorted(iids)):
            out[iid] = {"qform": q, "phrase": PHRASES[q][i % len(PHRASES[q])][0],
                        "frames": (FRAMES[2 * i], FRAMES[2 * i + 1])}
    return out


def wording_item(qid: str, spec: dict) -> dict:
    q = spec["qform"]
    meaning, _round1_rule = HA.WORDING_BRIEF[q]
    rules = [f"Key phrase, word for word: '{spec['phrase']}' (only the verb may follow the grammar). " + NEG_RULE[q],
             f"Candidate 1: {spec['frames'][0]}.", f"Candidate 2: {spec['frames'][1]}."]
    return {"qid": qid, "brief": meaning, "slots": {"SITE": "the site's name (exactly once)"}, "rules": rules}


def phrase_problems(qform: str, text: str) -> list:
    """R2 (stricter, before G-LEX): the form's key phrase is present and no other form's phrase is."""
    low = " ".join(text.split()).lower()
    out = []
    if not any(re.search(rx, low) for _p, rx in PHRASES[qform]):
        out.append(f"no key phrase of {qform} ({' / '.join(p for p, _ in PHRASES[qform])})")
    m = re.search(AVOID[qform], low)
    if m:
        out.append(f"phrase of another form: {m.group()!r}")
    return out


# ------------------------------------------------------------------------------------------------ sources

def round1() -> dict:
    """{pool: {batch, plan, items (iid -> item with qid), qid (iid -> qid), tid (iid -> task id)}} from
    haiku_author.build_batches(); every rebuilt chunk must equal the chunk file on disk."""
    out = {}
    for name, (b, plan) in HA.build_batches().items():
        for c in b.chunks:
            disk = _read(AUTHOR / b.chunk_path(c["task_id"]))
            if disk != c:
                raise SystemExit(f"round 1 chunk {c['task_id']} drifted from haiku/author/chunks")
        out[name] = {"batch": b, "plan": plan, "items": chunker.item_by_internal(b),
                     "qid": {iid: q for q, iid in b.key.items()},
                     "tid": {iid: b.task_of[q] for q, iid in b.key.items()}}
    return out


def _cell(pool: str, meta: dict) -> str:
    if pool == "packs":
        return "packs_held" if meta["held_out"] else "packs_train"
    if pool == "skins":
        return ("skin_heldout/" if meta["held_out"] else "skin/") + meta["register"]
    if pool == "freeform":
        return ("freeform_heldout/" if meta["held_out"] else "freeform/") + meta["register"]
    if pool == "attacks":
        return "attack"
    return "wording/" + meta["qform"]


def redo_plan(r1: dict | None = None) -> dict:
    """{pool: [{iid, qid, source_task_id, cell, prior}]}: every round 1 item whose piece was dropped by the lint or
    rejected by G-LEX. The per-cell counts must equal pools/MANIFEST.json's shortfalls exactly."""
    r1 = r1 or round1()
    log = _read(EXTRACT / "lint_log.json")
    quar = _read(POOLS / "quarantine.json")
    man = _read(POOLS / "MANIFEST.json")
    out = {p: [] for p in ORDER}

    def add(pool, iid, prior):
        meta = r1[pool]["plan"][iid]
        out[pool].append({"iid": iid, "qid": r1[pool]["qid"][iid], "source_task_id": r1[pool]["tid"][iid],
                          "cell": _cell(pool, meta), "prior": prior})

    pack_iid = {m["pack_id"]: iid for iid, m in r1["packs"]["plan"].items()}
    for d in log["drops"]["packs"]:
        add("packs", d["id"] if d["id"].startswith("t19a.") else pack_iid[d["id"]], d["reasons"])
    for pool in ("skins", "freeform", "attacks", "wordings"):
        for d in log["drops"][pool]:
            add(pool, d["id"], d["reasons"])
    if quar.get("question_admit_drops"):
        raise SystemExit("round 1 has question admit drops: not handled here")
    _b, plan, ans, _p = HA.load_answers_for("wordings")
    by_text: dict = {}
    for iid, a in ans.items():
        by_text.setdefault(" ".join(str((a or {}).get("text", "")).split()), []).append(iid)
    for f in quar["forms_not_admitted"]:
        iids = by_text.get(f["text"], [])
        if len(iids) != 1 or plan[iids[0]]["qform"] != f["qform"]:
            raise SystemExit(f"G-LEX rejected form {f['form_id']} maps to {iids}")
        add("wordings", iids[0], [f"G-LEX {f['status']}: read as {[e[1] for e in f['extractions']]}"])
    for pool in ORDER:
        if len({x["iid"] for x in out[pool]}) != len(out[pool]):
            raise SystemExit(f"{pool}: an item is listed twice")
    want = {s["item"]: s["shortfall"] for s in man["shortfalls"]}
    got = Counter(x["cell"] for pool in ORDER for x in out[pool])
    if dict(got) != want:
        raise SystemExit(f"redo items {dict(got)} != shortfalls {want}")
    return out


# ------------------------------------------------------------------------------------------------ build

def _contract(name: str, pool: str, answer_file: str, qids: list, k: int) -> str:
    key, what = ("packs", "pack objects") if pool == "packs" else ("texts", "strings")
    ex = (", ".join('{"sites": [...], "auditors": [...], "controls": [...]}' for _ in range(k)) if pool == "packs"
          else ", ".join(f'"<text {c}>"' for c in "ABC"[:k]))
    return "\n".join([
        f"# Haiku REDO-2 task {name} (family {FAMILY}, kind {KIND[pool]}): {len(qids)} item(s), {k} candidates each",
        "",
        "Read this whole file. It is the only file you may open: do not open, list, search or write any other file or "
        "folder. When you are done, write your answer with the Write tool to exactly this path (nothing else, no "
        "other file):",
        "",
        f"    {answer_file}",
        "",
        "## Answer contract (exact)",
        "",
        f"The answer file holds ONE JSON array with exactly {len(qids)} object(s), one per item below, every qid "
        f"exactly once (any order). Each object has exactly two keys: \"qid\" (the item's qid, copied exactly) and "
        f"\"{key}\" (a list of exactly {k} different {what}: {k} alternative candidates for that item, each complete "
        "on its own and each following every rule below; inside a string write \\n for a line break and \\\" for a "
        "double quote).",
        "Valid JSON only: no text before or after the array, no comments, no code fence, no other keys.",
        "",
        "Literal example of the required shape:",
        "",
        "[",
        f'  {{"qid": "{qids[0]}", "{key}": [{ex}]}},',
        "  ...",
        "]",
        "",
        "How the candidates are used: a program checks each candidate against the rules below in the order you wrote "
        "them and keeps the first one that meets every check; the others are thrown away. So every candidate must "
        "follow every rule, and the candidates of one item must be clearly different from each other.",
    ])


def _items_block(items: list) -> str:
    rows = ",\n".join(json.dumps(it, ensure_ascii=False) for it in items)
    return "\n".join([f"## Items ({len(items)}; one JSON object per line)", "", "```json", "[", rows, "]", "```"])


def _redo_item(pool: str, it: dict, wspec: dict | None) -> dict:
    if pool == "wordings":
        return wording_item(it["qid"], wspec)
    out = json.loads(json.dumps(it))
    if pool == "attacks":           # R1: the brief itself said "covers", and an earlier line answered with the label
        out["brief"] = out["brief"].replace("which sites a check covers", "which sites a check is meant for")
    return out


def _label_hits(text: str) -> list:
    return sorted({t for t in re.findall(r"[A-Za-z]+(?:-[A-Za-z]+)*", text) if t.lower() in LABEL_FORMS})


def _forbid_hits(text: str, forbid) -> list:
    low = text.lower()
    return [f for f in forbid if f and re.search(r"(?<![a-z0-9])" + re.escape(f.lower()) + r"(?![a-z0-9])", low)]


def build(r1: dict | None = None) -> list:
    """[task dict with its full text]; every check that guards an authoring task (A37 b) has run."""
    r1 = r1 or round1()
    rp = redo_plan(r1)
    iids_by_q: dict = {}
    for x in rp["wordings"]:
        iids_by_q.setdefault(r1["wordings"]["plan"][x["iid"]]["qform"], []).append(x["iid"])
    wspecs = wording_specs(iids_by_q)
    tasks = []
    for pool in ORDER:
        k, kind = N_CAND[pool], KIND[pool]
        instr = instructions(pool)
        psha = _sha(instr)
        rows = sorted(rp[pool], key=lambda x: _sha(f"{VERSION}|{pool}|{x['iid']}"))
        n_chunks = max(1, math.ceil(len(rows) / PER_TASK[pool]))
        size = math.ceil(len(rows) / n_chunks)
        for n in range(n_chunks):
            part = rows[n * size:(n + 1) * size]
            if not part:
                continue
            name = f"{FAMILY}-redo2-{pool}-{n:03d}"
            answer = str(ROOT / "answers" / f"{name}.json")
            task_file = str(ROOT / f"{name}.md")
            items = [_redo_item(pool, r1[pool]["items"][x["iid"]], wspecs.get(x["iid"])) for x in part]
            probs = []
            for x, it in zip(part, items):
                if it["qid"] != x["qid"]:
                    probs.append(f"qid mismatch {x['qid']}")
                if pool == "freeform" and it.get("facts") != r1[pool]["items"][x["iid"]].get("facts"):
                    probs.append(f"{x['qid']}: facts changed")
                try:
                    chunker.check_item(kind, {k2: v for k2, v in it.items() if k2 != "qid"},
                                       forbid_strings=FORBID[pool])
                except chunker.ChunkError as e:
                    probs.append(f"{x['qid']}: {e}")
            qids = [it["qid"] for it in items]
            contract = _contract(name, pool, answer, qids, k)
            text = "\n".join([contract, "", "## Instructions", "", instr, "", _items_block(items), ""])
            probs += [f"forbidden string {f!r}" for f in _forbid_hits(text, FORBID[pool])]
            if pool != "wordings":           # stricter: no label form in anything this round adds
                added = contract + NOTES[pool] + json.dumps(items, ensure_ascii=False)
                probs += [f"label form {w!r}" for w in _label_hits(added)]
            for p in (answer, task_file):
                if never_open(p):
                    probs.append(f"never-open path {p}")
            b = r1[pool]["batch"]
            if any(iid in text for iid in b.key.values()) or "t19a." in text:
                probs.append("names an internal id")
            if probs:
                raise chunker.ChunkError(f"{name}: {probs[:6]}")
            tasks.append({
                "name": name, "pool": pool, "kind": "author", "author_kind": kind, "task_file": task_file,
                "answer_file": answer, "n_items": len(items), "n_candidates": k, "outputs_expected": len(items) * k,
                "qids": qids, "source_batch_id": b.batch_id, "source_prompt_sha256": b.prompt_sha,
                "source_task_ids": {x["qid"]: x["source_task_id"] for x in part},
                "cells": {x["qid"]: x["cell"] for x in part}, "prior_reasons": {x["qid"]: x["prior"] for x in part},
                "wording_briefs": ({x["qid"]: wspecs[x["iid"]] for x in part} if pool == "wordings" else {}),
                "prompt_sha256": psha, "task_sha256": _sha(text), "allowed_read": [task_file],
                "allowed_write": [answer], "text": text})
    return tasks


RULINGS = {
    "R1_bare_on": "PROFILE_WORDS and the loaders' checks unchanged (option b not taken: it would admit pieces the "
                  "frozen check refused). New authoring round (option a): 'on', 'premise', 'on-premises', 'center' "
                  "added to SKIN rule 13, FREEFORM rule 6, ATTACK rule 3; redo notes list every refused word, "
                  "generated from the check sets; stricter extra check: a hyphenated word with a profile-word part",
    "R2_complement_trio": "QUESTION_MEANINGS, G0 section 6 (v1.1, sha unchanged) and the 2/2 bar unchanged. Each "
                          "complement brief pinned to its meaning's key phrase; candidates without it, or with "
                          "another form's phrase, or equal to any round 1 wording, are refused before G-LEX",
    "R3_duplicates": "each wording candidate gets its own opening or frame (FRAMES, none a round 1 style hint); "
                     "(key phrase, frame) unique within each form; exact dedup still runs",
    "R4_glex_placeholder": f"kit unchanged; redo2 G-LEX items fill {{SITE}} with {SAMPLE_SITE!r}; PROMPT_LEX and the "
                           "meaning list unchanged; new extractor ids; round 1 reads stand (no re-vote)",
}


def index(tasks: list) -> dict:
    return {
        "family": FAMILY, "version": VERSION, "g0_sha256": PL.G0_SHA256_AUTHORED, "g0_changed": False, "rulings": RULINGS,
        "n_tasks": len(tasks), "by_pool": dict(Counter(t["pool"] for t in tasks)),
        "items": sum(t["n_items"] for t in tasks), "outputs_expected": sum(t["outputs_expected"] for t in tasks),
        "items_by_cell": dict(sorted(Counter(c for t in tasks for c in t["cells"].values()).items())),
        "contract": "one JSON array; per item {\"qid\", \"texts\": [n strings]} (packs: {\"qid\", \"packs\": [n pack "
                    "objects]})",
        "selection": "per item, the first candidate in written order that passes every check of its pool is kept "
                     "(haiku_author check_* and freeze.slot_problems / wording_problems as written, the stricter R1 "
                     "hyphen check, the R2 key-phrase check, exact dedup against the frozen pools, every round 1 "
                     "wording and the candidates kept before it; Mode F also its G3-H read; wordings also G-LEX 2/2 "
                     "with the redo2 extractor ids); the rest are discarded; at most one piece per item",
        "keys": "items keep their round 1 qids: haiku/author/key/<source_batch_id>.json maps them to internal ids",
        "follow_up": ["load: redo2.py load (in memory)",
                      "extract: redo2.py extract --write (G-LEX 2 reads of the lint-clean wording candidates, "
                      f"{{SITE}} = {SAMPLE_SITE!r}; G3-H 1 read of the lint-clean Mode F candidates, PROMPT_G3H "
                      "unchanged), then extract-check",
                      "merge: freeze.py reads haiku/author/ and haiku/extract/ only; a freeze step must add the kept "
                      "redo2 pieces before the pools are frozen again; G13-seed and the file-access audits stay "
                      "pending"],
        "untouched": "haiku_author.py, extract_build.py, freeze.py, plugin.py, G0_SPEC.md, haiku/author/, "
                     "haiku/extract/ and pools/ are read only; nothing is converted or merged here",
        "tasks": [{k: v for k, v in t.items() if k != "text"} for t in tasks],
    }


README = ("T19 redo2 answers: one <task name>.json per redo2 task (see ../REDO2_INDEX.json), each a JSON array of "
          "{\"qid\", \"texts\": [...]} (packs: {\"qid\", \"packs\": [...]}). Written only by the redo2 task agents.\n")


def files(tasks: list) -> dict:
    out = {f"{t['name']}.md": t["text"] for t in tasks}
    out["REDO2_INDEX.json"] = json.dumps(index(tasks), ensure_ascii=False, indent=1) + "\n"
    out["answers/README.txt"] = README
    return out


def _write_once(root: Path, fs: dict) -> list:
    clash = [rel for rel, text in fs.items()
             if (root / rel).exists() and (root / rel).read_text(encoding="utf-8") != text]
    if clash:
        raise SystemExit(f"files already exist with other content (written once): {clash[:5]}")
    return [str(p) for p in paths.write_files(root, fs)]


# ------------------------------------------------------------------------------------------------ load

def read_candidates(task: dict, raw=None) -> tuple:
    """({qid: [candidates]}, problems) from one redo2 answer (raw: the parsed answer, for tests)."""
    key = "packs" if task["pool"] == "packs" else "texts"
    if raw is None:
        f = Path(task["answer_file"])
        if not f.exists():
            return {}, [f"{task['name']}: no answer file"]
        try:
            raw = _read(f)
        except json.JSONDecodeError as e:
            return {}, [f"{task['name']}: answer file is not JSON ({e})"]
    if not isinstance(raw, list):
        return {}, [f"{task['name']}: the answer is not a JSON array"]
    out, probs = {}, []
    for a in raw:
        q = a.get("qid") if isinstance(a, dict) else None
        if q not in task["qids"]:
            probs.append(f"{task['name']}: unknown qid {q!r}")
        elif q in out:
            probs.append(f"{task['name']}: qid {q} answered twice")
        elif not isinstance(a.get(key), list) or set(a) != {"qid", key}:
            probs.append(f"{task['name']}: {q} is not {{qid, {key}: [...]}}")
            out[q] = []
        else:
            if len(a[key]) != task["n_candidates"]:
                probs.append(f"{task['name']}: {q} has {len(a[key])} candidates, want {task['n_candidates']}")
            out[q] = list(a[key])[:task["n_candidates"]]
    missing = sorted(set(task["qids"]) - set(out))
    if missing:
        probs.append(f"{task['name']}: {len(missing)} qid(s) unanswered")
    return out, probs


def hyphen_profile(text: str, facts: dict | None = None) -> list:
    """R1 (stricter only): a hyphenated word one of whose parts is a profile word ("on-premises", "on-site")."""
    rest = text
    for v in (facts or {}).values():
        rest = rest.replace(v, " ")
    hits = sorted({w for w in re.findall(r"[A-Za-z]+(?:-[A-Za-z]+)+", rest)
                   if set(w.lower().split("-")) & PROFILE_WORDS})
    return [f"profile word inside a hyphenated word {hits}"] if hits else []


def lint_candidate(pool: str, iid: str, meta: dict, cand, tid: str, psha: str, seen: set) -> tuple:
    """(piece or None, reasons) with every check a round 1 piece of the pool met, plus the R1 / R2 extras; `seen`
    (normalised texts, or pack site tuples) is read here and grown by the caller."""
    tmp = set(seen)
    try:
        if pool == "packs":
            obj, v = HA.check_pack(iid, {"pack": cand}, meta, tmp)
            if obj is not None and not v:
                _kept, drops = EX.lint_packs([obj])
                v += [r for d in drops for r in d["reasons"]]
        elif pool == "skins":
            obj, v = HA.check_skin(iid, cand, meta, tid, psha, tmp)
            v += (FZ.slot_problems(obj) if obj is not None else []) + hyphen_profile(str(cand or ""))
        elif pool == "freeform":
            obj, v = HA.check_freeform(iid, cand, meta, tid, psha, tmp)
            v += (FZ.slot_problems(obj) if obj is not None else []) + hyphen_profile(str(cand or ""), meta["facts"])
        elif pool == "attacks":
            obj, v = HA.check_attack(iid, cand, meta, tid, psha, tmp)
            v += (FZ.slot_problems(obj) if obj is not None else []) + hyphen_profile(str(cand or ""))
        else:
            obj, v = HA.check_wording(iid, cand, meta, tid, psha, tmp)
            if obj is not None:
                v += FZ.wording_problems(obj[1]) + phrase_problems(meta["qform"], obj[1])
    except Exception as e:  # noqa: BLE001  (a malformed candidate is dropped, never fixed)
        obj, v = None, [f"unusable: {str(e)[:100]}"]
    return (None if v else obj), v


def seen_texts() -> set:
    """Normalised texts of every frozen skin, attack line and Mode F document."""
    out = set()
    for f in ("skins.json", "attacks.json", "documents.json"):
        out |= {_norm(d["text"]) for d in _read(POOLS / f)}
    return out


def seen_wordings() -> set:
    """Every round 1 wording text (admitted, rejected or duplicate) and the fixture questions: never re-voted."""
    _b, _plan, ans, _p = HA.load_answers_for("wordings")
    out = {_norm((a or {}).get("text", "")) for a in ans.values()}
    return out | {_norm(q) for q in HA.QSTRINGS}


def seen_packs() -> set:
    return {tuple(sorted(x.lower() for x in p["sites"])) for p in _read(POOLS / "packs.json")}


def select(tasks: list, r1: dict | None = None, raw_by_task: dict | None = None) -> dict:
    """Per item: the checked candidates in written order. Packs, skins and attack lines keep the first passing one;
    every lint-clean Mode F and wording candidate goes on to its read (extract), first passing kept later."""
    r1 = r1 or round1()
    seen = {"text": seen_texts(), "wordings": seen_wordings(), "packs": seen_packs()}
    out = {"items": [], "problems": []}
    for t in tasks:
        pool = t["pool"]
        if raw_by_task is None:
            cands, probs = read_candidates(t)
        elif t["name"] in raw_by_task:
            cands, probs = read_candidates(t, raw_by_task[t["name"]])
        else:
            cands, probs = {}, [f"{t['name']}: no answer"]
        out["problems"] += probs
        bucket = "packs" if pool == "packs" else ("wordings" if pool == "wordings" else "text")
        for q in t["qids"]:
            iid = r1[pool]["batch"].key[q]
            meta = r1[pool]["plan"][iid]
            row = {"task": t["name"], "pool": pool, "qid": q, "iid": iid, "cell": t["cells"][q], "candidates": [],
                   "kept": None}
            for j, cand in enumerate(cands.get(q, [])):
                obj, r = lint_candidate(pool, iid, meta, cand, t["name"], t["prompt_sha256"], seen[bucket])
                row["candidates"].append({"j": j, "ok": not r, "reasons": r, "obj": obj,
                                          "text": (obj.text if hasattr(obj, "text") else
                                                   obj[1] if isinstance(obj, tuple) else cand)})
                if r:
                    continue
                if pool == "packs":
                    seen["packs"].add(tuple(sorted(x.lower() for x in obj["sites"])))
                else:
                    seen[bucket].add(_norm(row["candidates"][-1]["text"]))
                if pool in ("packs", "skins", "attacks") and row["kept"] is None:
                    row["kept"] = j
                    break
            out["items"].append(row)
    return out


def frozen_counts() -> dict:
    return _read(POOLS / "MANIFEST.json")["counts"]


def merged_counts(kept_cells: list) -> tuple:
    """(counts, shortfalls): the frozen counts plus one per kept redo piece, against freeze.TARGETS (never lowered)."""
    c = json.loads(json.dumps(frozen_counts()))
    for cell in kept_cells:
        if "/" in cell:
            grp, key = cell.split("/", 1)
            c.setdefault(grp, {})
            c[grp][key] = c[grp].get(key, 0) + 1
        else:
            c[cell] = c.get(cell, 0) + 1
    short = []
    for name, want in FZ.TARGETS.items():
        if isinstance(want, dict):
            for k2, w in want.items():
                if c.get(name, {}).get(k2, 0) < w:
                    short.append({"item": f"{name}/{k2}", "admitted": c.get(name, {}).get(k2, 0), "target": w})
        elif c.get(name, 0) < want:
            short.append({"item": name, "admitted": c.get(name, 0), "target": want})
    return c, short


def load(raw_by_task: dict | None = None) -> dict:
    r1 = round1()
    tasks = build(r1)
    sel = select(tasks, r1, raw_by_task)
    kept = [r["cell"] for r in sel["items"] if r["kept"] is not None]
    counts, short = merged_counts(kept)
    read_pools = ("freeform", "wordings")
    return {"items": len(sel["items"]), "kept_without_a_read": len(kept),
            "awaiting_read": {p: sum(1 for r in sel["items"] if r["pool"] == p and any(c["ok"] for c in r["candidates"]))
                              for p in read_pools},
            "lint_clean_candidates": {p: sum(c["ok"] for r in sel["items"] if r["pool"] == p for c in r["candidates"])
                                      for p in ORDER},
            "reasons": dict(Counter(x.split(":", 1)[0] for r in sel["items"] for c in r["candidates"]
                                    for x in c["reasons"])),
            "counts_before_reads": counts, "shortfalls_before_reads": short, "problems": sel["problems"],
            "selection": sel, "tasks": tasks, "r1": r1}


# ------------------------------------------------------------------------------------------------ reads (extract)

def glex_registry(cands: list) -> tuple:
    """(registry, {candidate key: form id}, drops): the frozen admitted lexicon (pools/lexicon.json) plus every
    lint-clean wording candidate (source haiku). A candidate whose add or unit test fails in the combined registry is
    dropped; the registry is rebuilt until it is stable (as extract_build.admit_forms). A frozen form that stops
    passing its unit test stops the run."""
    base = _read(POOLS / "lexicon.json")
    pending, drops = list(cands), []
    while True:
        reg = LexiconRegistry.from_json(base)
        base_ids = set(reg.forms)
        added = []
        for c in pending:
            try:
                fo = reg.add(c["text"], question_sem(FAMILY, c["qform"]), slots={"SITE": "name"}, source="haiku",
                             family=FAMILY, haiku_task_id=c["task"], haiku_prompt_sha=c["psha"])
            except LexiconError as e:
                drops.append({**c, "reasons": [f"G-LEX add: {e}"]})
                continue
            added.append((c, fo.form_id))
        res = reg.unit_test_all()
        broken = sorted(f for f in base_ids if not res[f])
        if broken:
            raise SystemExit(f"frozen lexicon forms fail their unit test beside the redo2 forms: {broken[:3]}")
        bad = {fid for _c, fid in added if not res[fid]}
        if not bad:
            return reg, {c["key"]: fid for c, fid in added}, drops
        drops += [{**c, "reasons": [f"G-LEX unit: {x}" for x in reg.forms[fid].unit_problems[:2]]}
                  for c, fid in added if fid in bad]
        pending = [c for c, fid in added if fid not in bad]


def glex_items(reg: LexiconRegistry, fids: list, seed: str) -> list:
    """R4: the kit's gold-free items (same choices, same seeded order), with {SITE} filled by SAMPLE_SITE."""
    out = []
    for fid, it in reg.lexicon_items(fids, seed=seed):
        out.append((fid, {"text": reg.render(fid, {"SITE": S.name_slot(SAMPLE_SITE)}), "choices": it["choices"]}))
    return out


def _batch(kind: str, items: list, seed: str, prompt: str):
    n = len(items)
    chunks = max(1, math.ceil(n / chunker.MAX_ITEMS))
    return chunker.make_batch(kind, FAMILY, items, seed=seed, prompt=prompt, max_items=math.ceil(n / chunks))


def extract_build(sel: dict, r1: dict) -> dict:
    """The redo2 reads: 2 G-LEX reads of every lint-clean wording candidate and 1 G3-H read of every lint-clean Mode F
    candidate, with the round 1 prompts unchanged. Returns batches, registry, expected values and files."""
    wc, fc = [], []
    for row in sel["items"]:
        for c in row["candidates"]:
            if not c["ok"]:
                continue
            key = f"{row['iid']}|c{c['j']}"
            if row["pool"] == "wordings":
                q, text, tid, psha = c["obj"]
                wc.append({"key": key, "iid": row["iid"], "j": c["j"], "qform": q, "text": text, "task": tid,
                           "psha": psha})
            elif row["pool"] == "freeform":
                fc.append({"key": key, "iid": row["iid"], "j": c["j"], "text": c["text"],
                           "auditor": r1["freeform"]["plan"][row["iid"]]["facts"]["AUDITOR"]})
    out = {"glex": [], "g3h": None, "files": {}, "tasks": [], "reg": None, "fid_of": {}, "lex_drops": [],
           "g3h_expected": {}}
    batches = []
    if wc:
        reg, fid_of, drops = glex_registry(wc)
        fids = sorted(fid_of.values())
        out.update(reg=reg, fid_of=fid_of, lex_drops=drops)
        for label, extractor, seed in GLEX_READS:
            b = _batch("extract_lex", glex_items(reg, fids, seed), seed, EX.PROMPT_LEX)
            out["glex"].append({"label": label, "extractor_id": extractor, "batch": b})
            batches.append((label, "extract_lex", b, extractor))
    if fc:
        fields = EX.g3h_fields()
        items = [(f"g3h2|{c['key']}", g3h.extraction_item(c["text"], fields)) for c in fc]
        out["g3h_expected"] = {f"g3h2|{c['key']}": {"auditor": c["auditor"]} for c in fc}
        label, extractor, seed = G3H_READ
        b = _batch("extract_g3h", items, seed, EX.PROMPT_G3H)
        out["g3h"] = {"label": label, "extractor_id": extractor, "batch": b}
        batches.append((label, "extract_g3h", b, extractor))
    for label, kind, b, extractor in batches:
        out["files"].update(b.files())
        out["files"][f"plan/{b.batch_id}.json"] = json.dumps({"batch_id": b.batch_id, "label": label, "kind": kind,
                                                              "extractor_id": extractor}, indent=1, sort_keys=True) + "\n"
        for c in b.chunks:
            tid = c["task_id"]
            ans = str(XROOT / b.answer_path(tid))
            tfile = f"tasks/{tid}.md"
            text = EX.task_markdown(kind, b, c, Path(ans))
            if any(iid in text for iid in b.key.values()) or "t19a." in text:
                raise chunker.ChunkError(f"{tid}: names an internal id")
            out["files"][tfile] = text
            out["tasks"].append({"task": label, "task_id": tid, "kind": kind, "batch_id": b.batch_id,
                                 "extractor_id": extractor, "task_file": str(XROOT / tfile), "answer_file": ans,
                                 "n_items": len(c["items"]), "outputs_expected": len(c["items"]),
                                 "prompt_sha": b.prompt_sha, "task_sha256": _sha(text),
                                 "allowed_read": [str(XROOT / tfile)], "allowed_write": [ans]})
    out["files"]["key/g3h_expected.json"] = json.dumps(out["g3h_expected"], indent=1, sort_keys=True) + "\n"
    out["files"]["key/glex_forms.json"] = json.dumps(
        {c["key"]: {"form_id": out["fid_of"].get(c["key"]), "qform": c["qform"], "text": c["text"]} for c in wc},
        indent=1, sort_keys=True) + "\n"
    out["files"]["TASKS.json"] = json.dumps({
        "family": FAMILY, "version": VERSION, "stage": "redo2 reads", "sample_site": SAMPLE_SITE,
        "prompts": "extract_build.PROMPT_LEX and PROMPT_G3H, unchanged", "n_tasks": len(out["tasks"]),
        "outputs_expected": sum(t["outputs_expected"] for t in out["tasks"]), "lexicon_drops": out["lex_drops"],
        "tasks": out["tasks"]}, ensure_ascii=False, indent=1, default=str) + "\n"
    out["files"]["answers/README.txt"] = ("T19 redo2 read answers: one <task_id>.json per task (see ../TASKS.json). "
                                          "Written only by the task agents.\n")
    return out


def _answers(b) -> tuple:
    raw = {}
    for c in b.chunks:
        f = XROOT / b.answer_path(c["task_id"])
        if f.exists():
            raw[c["task_id"]] = _read(f)
    return chunker.load_answers(b, raw)


def extract_check() -> dict:
    """G-LEX 2/2 on every read wording candidate, G3-H on every read Mode F candidate; per item the first candidate in
    written order that passed every check and its read is kept; merged counts against freeze.TARGETS."""
    res = load()
    sel, r1 = res["selection"], res["r1"]
    ex = extract_build(sel, r1)
    drift = [rel for rel, text in ex["files"].items()
             if not (XROOT / rel).exists() or (XROOT / rel).read_text(encoding="utf-8") != text]
    if drift:
        raise SystemExit(f"redo2 read files drifted or are missing: {drift[:5]}")
    reg, problems, reads = ex["reg"], [], {}
    for g in ex["glex"]:
        got, probs = _answers(g["batch"])
        problems += [f"{g['label']}: {p}" for p in probs]
        reads[g["label"]] = FZ.record_glex(reg, got, g["extractor_id"])
    g3_ok = {}
    if ex["g3h"]:
        got, probs = _answers(ex["g3h"]["batch"])
        problems += [f"{ex['g3h']['label']}: {p}" for p in probs]
        for gid, want in ex["g3h_expected"].items():
            g3_ok[gid] = g3h.compare(want, got[gid], EX.g3h_fields()) if gid in got else (False, ["no answer"])
    kept, rows = [], []
    for row in sel["items"]:
        k = row["kept"]
        if row["pool"] in ("wordings", "freeform"):
            k = None
            for c in row["candidates"]:
                key = f"{row['iid']}|c{c['j']}"
                if not c["ok"]:
                    continue
                if row["pool"] == "wordings":
                    fid = ex["fid_of"].get(key)
                    if fid and reg.status(fid) == "admitted":
                        k = c["j"]
                        break
                elif g3_ok.get(f"g3h2|{key}", (False,))[0]:
                    k = c["j"]
                    break
        rows.append({"pool": row["pool"], "qid": row["qid"], "cell": row["cell"], "kept": k})
        if k is not None:
            kept.append(row["cell"])
    counts, short = merged_counts(kept)
    status = Counter(reg.status(f) for f in ex["fid_of"].values()) if reg else Counter()
    return {"glex": {"forms_read": len(ex["fid_of"]), "status": dict(status), "reads": reads,
                     "lexicon_drops": len(ex["lex_drops"])},
            "g3h": {"bar": g3h.PASS_RATE, "template": "document", "read": len(g3_ok),
                    "passed": sum(1 for v in g3_ok.values() if v[0])},
            "kept": len(kept), "items": rows, "counts": counts, "shortfalls": short, "problems": problems}


# ------------------------------------------------------------------------------------------------ main

def main(argv: list) -> int:
    cmd = argv[0] if argv else "tasks"
    if cmd == "tasks":
        tasks = build()
        print(json.dumps({"n_tasks": len(tasks), "items": sum(t["n_items"] for t in tasks),
                          "outputs_expected": sum(t["outputs_expected"] for t in tasks),
                          "items_by_cell": index(tasks)["items_by_cell"],
                          "tasks": [{k: t[k] for k in ("task_file", "answer_file", "author_kind", "n_items",
                                                        "n_candidates")} for t in tasks]}, indent=1))
    elif cmd == "write":
        print(json.dumps(_write_once(ROOT, files(build())), indent=1))
    elif cmd == "load":
        res = load()
        for k in ("selection", "tasks", "r1"):
            res.pop(k)
        print(json.dumps(res, indent=1, ensure_ascii=False, default=str))
    elif cmd == "extract":
        res = load()
        missing = [p for p in res["problems"] if p.endswith("no answer file")]
        if missing:
            raise SystemExit(f"authoring answers missing, no read is built: {missing}")
        ex = extract_build(res["selection"], res["r1"])
        out = {"tasks": len(ex["tasks"]), "glex_forms": len(ex["fid_of"]), "lexicon_drops": len(ex["lex_drops"]),
               "g3h_items": len(ex["g3h_expected"]), "sample_site": SAMPLE_SITE, "written": False}
        if "--write" in argv:
            out["files"] = _write_once(XROOT, ex["files"])
            out["written"] = True
        print(json.dumps(out, indent=1))
    elif cmd == "extract-check":
        print(json.dumps(extract_check(), indent=1, ensure_ascii=False, default=str))
    else:
        raise SystemExit(f"unknown command {cmd!r}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
