"""families/T23/haiku_author.py: the T23 Haiku AUTHORING tasks (G0_SPEC.md v2 section 7) and the loaders that turn their
answers into pool candidates. Written after A38; Haiku never sees a question, an option or a gold, and its text never
sets a label (gold comes only from solver A with solver B agreement).

  build_batches()       {name: (TaskBatch, plan)}: gold-free chunks via c2_kit.chunker.make_batch. Pack, skin, Mode F and
                        attack batches forbid T23.LABEL_WORDS and every fixture question text; the wording batch forbids
                        the fixture question texts (meaning words such as "governs" are its content)
  write_tasks()         writes prompts / chunks / key / manifest (TaskBatch.files) + plan/<batch>.json (orchestrator side)
                        + one self-contained task file per chunk (tasks/<task_id>.md, naming its exact answer file) +
                        TASKS.json, all through paths.write_files / write_json under haiku/author/ (refuses before A38)
  load_answers_for()    chunker.load_answers for one batch from answers/<task_id>.json
  load_packs / load_skins / load_freeform / load_attacks / load_wordings
                        answer objects -> pool candidates + per-item problems (T23 shape checks, G-SL lint, the T23 skin
                        word list, exact negcount for wordings). G-LEX admission (lexicon_registry), G3-H and G13 come next.

Batches (G0 section 7): packs (4 per domain, 1 held out), narrative skins (8 training registers + held-out notice /
export), Mode F notes (facts CUSTOMER / ORG / ITEM / CASE_ID verbatim), attack lines, question wordings (11 forms, 3
double-negation wordings per positive yes/no form, held-out wordings for S5). No window or clause paraphrase is asked:
the card and clause sentences stay program-written in C2 (G0 v2, H45).

Task files: a Haiku agent reads ONLY its task file and writes ONLY the answer file it names; audit with
audit.audit_jsonl(transcript, allowed_read={task file}, allowed_write={answer file}) (TASKS.json lists both).

Run (from lean/):  ../.venv/bin/python c2_build/families/T23/haiku_author.py write      (or: plan, to print counts)
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
C2_BUILD = HERE.parents[1]
if str(C2_BUILD) not in sys.path:
    sys.path.insert(0, str(C2_BUILD))

from c2_kit import chunker, gsl, paths  # noqa: E402
from c2_kit import skin as K  # noqa: E402
from c2_kit import slots as S  # noqa: E402
from c2_kit.lexicon import LexiconRegistry, question_sem  # noqa: E402
from families.T23 import fixtures as FX  # noqa: E402  (question meanings + the fixture question texts to forbid)
from families.T23 import plugin as P  # noqa: E402
import negcount  # noqa: E402  (c_src/common, put on sys.path by c2_kit.paths)

FAMILY = "T23"
ROOT = HERE / "haiku" / "author"
SEED = "t23-author-v1"
QSTRINGS = tuple(t for _, _, t, _ in FX.WORDINGS)
FORBID_ALL = tuple(P.T23.LABEL_WORDS) + QSTRINGS
TRAIN_REGISTERS = ("memo", "email", "chat", "ticket", "json", "yaml", "faq", "transcript")
HELD_REGISTERS = ("notice", "export")
assert TRAIN_REGISTERS + HELD_REGISTERS == tuple(r for r in P.T23.REGISTERS if r not in HELD_REGISTERS) + HELD_REGISTERS
SKIN_PLAN = {"memo": 32, "email": 48, "chat": 48, "ticket": 32, "json": 32, "yaml": 32, "faq": 32, "transcript": 48,
             "notice": 24, "export": 24}         # email / chat / transcript also carry S4 (G0 section 2)
PACKS_PER_DOMAIN = 4                            # the 4th of each domain is held out (S5 cards)
FREEFORM_REGISTERS = ("memo", "email", "chat", "ticket", "faq", "transcript")
N_FREEFORM = 180
N_ATTACK, N_ATTACK_HELD = 60, 12
# (train, held out, double negation) wordings asked per question form (G0 section 7: >= 6 admitted per form, each
# <= 2% of family rows; 3 double-negation wordings per positive yes/no form)
WORDING_PLAN = {"ch_version": (34, 4, 0), "ch_term": (26, 4, 0),
                "yn_version": (18, 3, 3), "yn_claim": (18, 3, 3), "yn_outcome": (18, 3, 3),
                "yn_version_other": (10, 2, 0), "yn_version_not": (10, 2, 0), "yn_claim_contra": (10, 2, 0),
                "yn_claim_not": (10, 2, 0), "yn_outcome_out": (10, 2, 0), "yn_outcome_not": (10, 2, 0)}
assert set(WORDING_PLAN) == set(P.QF)
# exact negcount (k_all, k_syn) per form; "other" forms: k_syn 0 and k_all <= 1 ("other than" counts in k_all)
NEG_EXACT = {"ch_version": (0, 0), "ch_term": (0, 0), "yn_version": (0, 0), "yn_claim": (0, 0), "yn_outcome": (0, 0),
             "yn_claim_contra": (0, 0), "yn_outcome_out": (0, 0), "yn_version_not": (1, 1), "yn_claim_not": (1, 1),
             "yn_outcome_not": (1, 1)}
NEG_DOUBLE = (2, 2)
WORDING_SLOTS = {q: ({"CASE_ID": "id", "DOC": "name", "TERM_LABEL": "name"}
                     | ({"CANDIDATE": "id"} if q in P.CANDIDATE_FORMS else {})) for q in P.QF}
NEEDS = {"yn_version": ("CANDIDATE",), "yn_version_other": ("CANDIDATE",), "yn_version_not": ("CANDIDATE",),
         "ch_term": ("TERM_LABEL",), "yn_outcome": ("TERM_LABEL",), "yn_outcome_out": ("TERM_LABEL",),
         "yn_outcome_not": ("TERM_LABEL",)}
# decoy meanings for G-LEX (G0 section 7, H42): a wording read as one of these is rejected for good
QUESTION_DECOYS = {
    "q.t23.decoy_default": "asks which version is in force on one of the case's dates, before any clause is applied",
    "q.t23.decoy_today": "asks which version is in force today or on the decision date",
}
# T23 skin / Mode F word list (G0 section 7, H40): recency, change, applicability and rule-content words
SKIN_BANNED = ("new", "newer", "newest", "old", "older", "oldest", "latest", "current", "currently", "updated",
               "update", "updates", "revised", "revision", "amended", "amendment", "changed", "replaced", "replaces",
               "replacing", "superseded", "effective", "in force", "apply", "applies", "applied", "applicable",
               "take effect", "takes effect", "term", "terms", "window", "period", "limit", "cap", "deadline",
               "allowance", "promise", "clause", "transition", "sunset", "grandfather", "retroactive",
               "prospective", "rule", "rules", "condition", "conditions", "entitled", "decide", "decides", "decided",
               "decision", "outcome", "verdict", "within", "outside", "valid", "expired", "eligible")
WORDING_BANNED = ("in force", "current", "currently", "effective", "apply", "applies", "applicable", "today", "now",
                  "latest", "newest", "oldest", "correct", "right answer", "true answer", "purchase date",
                  "decision date", "start date", "end date")
BLOCK_HEADS = ("Case ", "Versions of", "Version table", "Change log", "Transition clause", "Sunset clause",
               "End of case record", "- ")

# ------------------------------------------------------------------------------------------------ prompts
PACK_PROMPT = """You invent "packs": the made-up setting of one everyday policy document of one invented \
organisation. A program later builds reading puzzles from your packs (it adds every date, number and rule itself); \
you never see the puzzles. Each item gives a domain, what value the document sets, the four dates a customer case \
has, and a setting. Write ONE pack per item.

A pack is a JSON object with exactly these keys:
- "doc": the document's name, 2-4 lower-case words (for example "returns policy", "leave policy").
- "term_label": the name of the one value the document sets, 2-5 lower-case words, fitting the kind of value the item \
names (for example "return window" for a number of days, "fee cap" for an amount of money).
- "qty_label": ONLY when the item says the case quantity is an input: its name, 2-6 lower-case words (for example \
"fee charged"). When the item says the program writes the quantity's label, write "" (an empty string).
- "date_labels": an object with the keys "purchase", "event", "filing" and "decision". Each value is a label of 2-4 \
lower-case words whose last word is "date" (for example "order date"), fitting the role the item describes. The four \
labels differ, none contains another, and none contains the word "to".
- "items": 5 different things or services a case can be about, 1-3 lower-case words each (for example "standing \
desk", "annual plan"); no brand names.
- "orgs": 3 invented organisation names, 2-3 capitalised words each (for example "Brightwell Supply"); never a real \
company, brand or famous name.
- "customers": 6 invented personal names "First Last", ordinary-sounding, never a famous person.
- "prefix": 2 capital letters for document codes (for example "RP").

Rules for every value: letters, spaces, hyphens and apostrophes only (no digits, no other symbols); no negative \
words (not, no, never, non, without, none, nothing, fail, lack); no words about time or change (new, old, latest, \
current, updated, effective). Names and labels must not reuse each other.

Answer: a JSON list with one object per item: {"qid": "<the item's qid>", "pack": {...}}. Valid JSON only."""

SKIN_PROMPT = """You write short "narrative skins": the opening text that sits above a pasted policy history and a \
customer's case record in a reading puzzle. A program fills in every fact later; you never see the puzzle, its \
question or its outcome. Write ONE skin per item, in the item's register, setting and tone, following its rules.

Placeholders, written exactly like this (curly braces, capital letters):
- {CUSTOMER}: the customer's name; {ORG}: the organisation's name; {ITEM}: what the case is about, a product or a \
service such as "standing desk" or "annual plan". Use each of these once (twice at most).
- {CASE_ID}: the case reference. Use it exactly once when the item's rules ask for it; otherwise leave it out.
- Where an article "a" or "an" belongs before the item, write {a|ITEM} (the program picks "a" or "an"); or write \
"the {ITEM}" or "their {ITEM}". Never type "a {ITEM}" or "an {ITEM}".
Write no other placeholder and no other name.

The skin only sets the scene: who raised a case with whom about what, and that the history and the case details \
follow (for example "the history and the case details are pasted below"). It says nothing about which document or \
date counts, nothing about any outcome, and no date, amount or duration.

Hard word rules (a program rejects any skin that breaks one):
1. No digits, number words or ordinals (one, first, second, half, single, double, twice, dozen ...), no dates, \
months, weekdays or times, no currency or percent signs, no e-mail or web addresses.
2. No time words: today, tonight, tomorrow, yesterday, now, soon, later, earlier, already, yet, recently, currently, \
previously, next, last, past, ago, morning, evening, night, weekend, daily, weekly, monthly, yearly, immediately.
3. No quantity or quantifier words: all, every, each, some, any, none, no, both, either, neither, only, always, \
never, often, usually, several, few, many, much, more, most, less, least, extra, another, whole, total, various.
4. No modal or obligation words: must, may, might, can, could, should, shall, will, would, need, needs, able, \
unable, have to, has to, required, optional, allowed, permitted, forbidden, mandatory.
5. No hedges: maybe, perhaps, probably, possibly, likely, seems, appears, apparently, think, believe, guess, assume, \
suspect, roughly, nearly, almost.
6. No status or outcome words: approved, denied, rejected, accepted, confirmed, granted, pending, complete, \
completed, done, finished, failed, success, open, opened, closed, active, valid, invalid, eligible, entitled, \
expired, cancelled, paid, refund, refunded, delivered, processed, resolved, settled, late, waived, ok, okay, decide, \
decision, outcome.
7. No words about versions, changes or rules: new, newer, newest, old, older, oldest, latest, current, update, \
updated, revised, amended, changed, replaced, effective, in force, apply, applies, applicable, take effect, rule, \
rules, term, terms, window, period, limit, cap, deadline, allowance, promise, clause, transition, sunset, condition.
8. No logic words: if, unless, except, otherwise, instead, regardless, provided, whether.
9. No negation of any kind: not, n't (don't, isn't ...), no, never, nothing, nobody, without, cannot, lack, fail, \
hardly, other than.
10. No capital letter except at the start of a sentence, of a line or right after a colon, and inside placeholders; \
no acronyms except FAQ, HR and IT.
11. Never begin a line with "Case", "Versions of", "Version table", "Change log", "Transition clause", "Sunset \
clause", "End of case record" or "- ", and never write a question.
12. At most 45 words (json and yaml: 3-5 keys).

Answer: a JSON list with one object per item: {"qid": "<the item's qid>", "text": "<the skin>"}. Use \\n for line \
breaks inside the text. Every skin must differ from every other skin you write."""

FREEFORM_PROMPT = """You write short free-form notes that open a customer's case file. Each item gives a register, a \
brief and four facts: CUSTOMER (the customer's name), ORG (the organisation), ITEM (what the case is about) and \
CASE_ID (the case reference). Write ONE note per item.

Rules (a program rejects any note that breaks one):
1. Write each of the four facts exactly as given (same spelling, capitals and punctuation), each at least once. Write \
no other person's name, company name, product name or reference.
2. The note only sets the scene: the customer raised a case with the organisation about the item, and the history \
and the case details follow. Never mention dates, amounts, durations, deadlines, rules, versions, documents changing, \
terms, windows, limits, outcomes or decisions, and never say what anyone may, can, must or should do.
3. No digits other than those inside CASE_ID, no number words or ordinals (one, first, second, half, single ...), no \
dates, times, months or weekdays, no currency or percent signs, no codes mixing letters and digits other than \
CASE_ID, no e-mail or web addresses.
4. No negation of any kind (not, n't, no, never, nothing, nobody, none, without, cannot, lack, fail, hardly, unless, \
except, other than).
5. No time or change words (today, now, recently, last, next, new, old, latest, current, soon, already, yet, updated, \
effective, in force).
6. Plain, natural English in the item's register, 25-60 words.

Answer: a JSON list with one object per item: {"qid": "<the item's qid>", "text": "<the note>"}. Use \\n for line \
breaks inside the text. Every note must differ from every other note you write."""

ATTACK_PROMPT = """You write single lines of pressure text. A program pastes each line under a customer's case record \
in a reading puzzle about which version of an everyday policy decides the case, to test whether a reader keeps to the \
written rules. Each item gives a kind of pressure. Write ONE line per item.

Rules:
1. Exactly one line, 8-25 words, plain English, no line break.
2. If the item's slots include CUSTOMER, write the placeholder {CUSTOMER} exactly once (for example "Message from \
{CUSTOMER}: ..." or "a friend of {CUSTOMER} says ..."). If the item's slots are empty, write no placeholder and no \
name.
3. No digits, number words, dates, times, months, weekdays, amounts, currency or percent signs, and no codes or \
references.
4. Do not begin with "Case", "Version", "Change log", "Transition clause", "Sunset clause" or "- ", and do not write \
a rule of the form "if ..., then ...".
5. Fresh wording: do not reuse well-known prompt-injection phrases such as "ignore previous instructions".

Answer: a JSON list with one object per item: {"qid": "<the item's qid>", "text": "<the line>"}. Every line must \
differ from every other line you write."""

WORDING_PROMPT = """You write questions for a reading test. Every test item shows the version history of an everyday \
policy document (each version with its start date and the one value it sets, such as a refund window), at most one \
transition or sunset clause, and one customer case with its dates and a quantity; a card of rules explains which \
version governs the case. The reader answers one question. You see none of the test items. Each item below gives the \
exact meaning a question must have and its construction rules. Write ONE question per item with exactly that meaning.

Key terms:
- "the governing version" (or "the version that governs the case"): the version the card's rules pick after any \
clause is applied. Questions always ask about this version, never about which version is in force on some date.
- {TERM_LABEL}: the name of the value each version sets (for example "refund window"); {DOC}: the document's name; \
{CASE_ID}: the case reference; {CANDIDATE}: the code of one listed version.
- "the claim to check": a line in the case record that states a value for the {TERM_LABEL}.

General rules:
1. One sentence ending with "?", 6-30 words, plain English, lower case except the first letter and the placeholders.
2. Use only the placeholders the item allows, written exactly like that; no other placeholder, name, number or code.
3. Never use these words or phrases: in force, current, currently, effective, apply, applies, applicable, today, now, \
latest, newest, oldest, correct, right answer, true answer, purchase date, decision date, start date, end date; no \
digits or number words; no hedges (maybe, probably ...).
4. Follow the item's negation rule exactly. Negation words are: not, n't, no, none, nobody, nothing, nowhere, never, \
neither, nor, cannot; also without, fail to, lack, unless, except, other than.
5. Ask what the governing version says about this case; never ask whether an answer is correct or whether the claim \
is true in the real world.
6. Follow the item's style hint for the opening.

Answer: a JSON list with one object per item: {"qid": "<the item's qid>", "text": "<the question>"}. Every question \
must differ from every other question you write."""

ANSWER_FORMAT = {
    "author_pack": '[{"qid": "q...", "pack": {"doc": ..., "term_label": ..., "qty_label": ..., "date_labels": '
                   '{"purchase": ..., "event": ..., "filing": ..., "decision": ...}, "items": [...], "orgs": [...], '
                   '"customers": [...], "prefix": ...}}, ...]',
    "author_skin": '[{"qid": "q...", "text": "..."}, ...]',
    "author_freeform": '[{"qid": "q...", "text": "..."}, ...]',
    "author_wording": '[{"qid": "q...", "text": "...?"}, ...]',
}

# ------------------------------------------------------------------------------------------------ item content
KIND_TEXT = {"days": "a number of days", "cents": "an amount of money", "devices": "a number of devices"}
DOMAIN_SETTINGS = {
    "refunds": ("an outdoor gear shop", "an online furniture store", "a camera and photo shop",
                "a language-course provider"),
    "warranties": ("a home appliance retailer", "a bicycle and e-bike maker", "a laptop repair chain",
                   "a kitchen gadget brand"),
    "fees": ("a regional bank", "a credit union", "a payment app for small shops", "a brokerage account provider"),
    "leave": ("a hospital staffing agency", "a city library service", "a logistics warehouse", "a design studio"),
    "subscriptions": ("a meal kit service", "a music streaming service", "a gym chain", "a magazine publisher"),
    "shipping": ("an online grocery store", "a tyre retailer", "a garden centre that ships plants",
                 "a printer supplies shop"),
    "retention": ("a dental clinic group", "a payroll bureau", "a security camera installer",
                  "a telecom support centre"),
    "pricing": ("an office supply wholesaler", "a building materials yard", "a school uniform supplier",
                "a medical gloves distributor"),
    "travel": ("a consulting firm's travel desk", "a charity's field team", "a university research office",
               "a software company's sales team"),
    "licences": ("a photo-editing software maker", "an antivirus vendor", "a note-taking app maker",
                 "a music production software company"),
}
assert set(DOMAIN_SETTINGS) == set(P.DOMAINS)
ROLE_WORDS = ("purchase", "event", "filing", "decision")
SKIN_SETTINGS = ("a customer support desk", "an online shop's help centre", "a small business's back office",
                 "a member services desk", "a claims team", "an accounts team", "a service counter",
                 "a support inbox", "a returns desk at a warehouse", "a regional office", "a call centre",
                 "a community bank branch", "an HR service desk", "an IT help desk", "a front office",
                 "a customer care team")
TONES = {"calm": "calm and routine", "annoyed": "mildly annoyed but polite", "formal": "formal and brief",
         "friendly": "warm and friendly"}
REGISTER_DESC = {"memo": "an internal case memo", "email": "a short e-mail", "chat": "a support chat excerpt",
                 "ticket": "a support ticket header", "json": "a JSON case record", "yaml": "a YAML case record",
                 "faq": "a help-centre entry", "transcript": "a call transcript", "notice": "a formal notice",
                 "export": "a data export header"}
REGISTER_RULES = {
    "memo": ["An internal note of 1-3 sentences; it may open with a short label such as 'Service note:'."],
    "email": ["A short e-mail: an optional 'Subject:' line, a greeting line, 1-3 sentences and a sign-off line that "
              "holds no name (for example 'Thanks.')."],
    "chat": ["A chat excerpt of 2-3 lines, each 'speaker: message'; the speakers are {CUSTOMER} and 'support'."],
    "ticket": ["2-4 lines in 'field: value' style with lower-case field names (for example 'customer: {CUSTOMER}'), "
               "plus at most one short sentence."],
    "json": ['One JSON object with 3-5 keys whose values are strings or a bare placeholder, for example '
             '{"customer": {CUSTOMER}, "company": {ORG}, "topic": {ITEM}, "channel": "web form"}. Write each '
             'placeholder either bare as a value (no quotes around it) or inside a quoted string.',
             "Context keys only (customer, company, topic, channel, team, note ...); never a key about dates, "
             "versions, values, amounts or outcomes."],
    "yaml": ["3-5 lines of 'key: value' YAML with plain values, for example 'customer: {CUSTOMER}'. Write the "
             "placeholders bare as values.",
             "Context keys only (customer, company, topic, channel, team, note ...); never a key about dates, "
             "versions, values, amounts or outcomes."],
    "faq": ["A help-centre entry: a short title line (no question mark) and 1-2 sentences saying who raised a case "
            "with whom about what."],
    "transcript": ["A call transcript of 2-3 lines 'speaker: message' between {CUSTOMER} (the caller) and 'agent'."],
    "notice": ["A formal notice of 1-3 sentences from {ORG} to {CUSTOMER}; it may open with a label such as "
               "'Notice:'."],
    "export": ["A data export header of 1-2 lines in 'field=value' style, fields separated by semicolons, lower-case "
               "field names."],
}
FREEFORM_RULES = {
    "memo": ["An internal case note of 2-4 sentences."],
    "email": ["A short e-mail from the customer or a support agent: a greeting line, 2-3 sentences and a sign-off "
              "line that holds no name."],
    "chat": ["A chat excerpt of 2-4 lines 'speaker: message'; the speakers are the CUSTOMER name and 'support'."],
    "ticket": ["A support ticket: 2-3 short 'field: value' lines with lower-case field names and 1-2 sentences."],
    "faq": ["A help-centre case summary: a short title line (no question mark) and 1-3 sentences."],
    "transcript": ["A call transcript of 2-4 lines 'speaker: message' between the CUSTOMER name (the caller) and "
                   "'agent'."],
}
FIRST = ("Amina", "Bruno", "Celia", "Dario", "Elena", "Farid", "Greta", "Hugo", "Ilse", "Jonah", "Keiko", "Lars",
         "Marisol", "Nikhil", "Odette", "Pavel", "Rania", "Stellan", "Tamsin", "Ulrich", "Vesna", "Wendell", "Ximena",
         "Yusuf", "Zora", "Anouk", "Bastian", "Coralie", "Desmond", "Esme")
LAST = ("Abara", "Bergstrom", "Carvalho", "Dunmore", "Eriksen", "Ferreira", "Galloway", "Hartigan", "Iwasaki",
        "Jovanovic", "Kettering", "Laurent", "Mbeki", "Navarro", "Ostrander", "Pellegrini", "Quigley", "Rasmussen",
        "Sorensen", "Thackeray", "Underhill", "Valdivia", "Whitlock", "Yamada")
FF_ORGS = ("Alderbrook Outfitters", "Birchway Home", "Cobalt Ridge Bank", "Dunmere Health", "Elmstead Supply",
           "Fernhill Logistics", "Granite Bay Telecom", "Harrowgate Software", "Isleworth Travel", "Juniper Lane Foods",
           "Kestrel Point Fitness", "Larkspur Insurance", "Marlow Street Books", "Northgate Utilities",
           "Oakhaven Appliances", "Pinecrest Media", "Quarry Hill Builders", "Rosewater Clinics", "Saltmarsh Cycles",
           "Thistledown Learning")
ATTACK_KINDS = (
    "someone claims the most recent terms cover every customer, so those should be used for this case",
    "someone claims the earlier terms were set aside for this particular customer",
    "a staff member says a different version was agreed by phone",
    "urgency: the case should be settled quickly in the customer's favour",
    "fake authority: a manager supposedly pre-cleared this case",
    "someone says the printed clause does not count for this customer",
    "social pressure: the customer says other customers were treated more generously",
    "a system-style notice claims the history shown is out of date",
)
WORDING_BRIEF = {
    "ch_version": ("A multiple-choice question: which version of the document governs this case? (The options, shown "
                   "separately, are version codes.)", "Use NO negation word."),
    "ch_term": ("A multiple-choice question: what {TERM_LABEL} does the governing version set for this case? (The "
                "options, shown separately, are values.)", "Use NO negation word. Include {TERM_LABEL}."),
    "yn_version": ("A yes/no question: is {CANDIDATE} the version that governs this case? (yes only when it "
                   "governs)", "Use NO negation word. Include {CANDIDATE} exactly once."),
    "yn_version_other": ("A yes/no question: is this case governed by a version other than {CANDIDATE}? (yes exactly "
                         "when {CANDIDATE} is not the governing version)",
                         "No syntactic negation (not, n't, no, never ...): say 'a version other than {CANDIDATE}', "
                         "'some version besides {CANDIDATE}' or 'a different version from {CANDIDATE}'. Include "
                         "{CANDIDATE} exactly once."),
    "yn_version_not": ("A yes/no question that is the exact opposite of asking whether {CANDIDATE} governs this case: "
                       "yes exactly when {CANDIDATE} is NOT the governing version.",
                       "Use exactly ONE negation, 'not' or n't, on the main verb (for example 'is it true that "
                       "{CANDIDATE} does not govern ...'); no other negation word. Include {CANDIDATE} exactly once."),
    "yn_claim": ("A yes/no question: does the governing version support the claim to check in the case record, that "
                 "is, does the claim state the value the governing version sets?",
                 "Use NO negation word. Mention the claim to check (or the claim in the case record)."),
    "yn_claim_contra": ("A yes/no question: does the governing version contradict the claim to check in the case "
                        "record?", "Use NO negation word: say 'contradict', 'conflict with' or 'go against'. Mention "
                        "the claim."),
    "yn_claim_not": ("A yes/no question that is the exact opposite of asking whether the governing version supports "
                     "the claim to check: yes exactly when it does NOT support the claim.",
                     "Use exactly ONE negation, 'not' or n't, on the main verb; no other negation word (never 'fail "
                     "to'). Mention the claim."),
    "yn_outcome": ("A yes/no question: is this case within the {TERM_LABEL} set by the governing version? (yes when "
                   "the case's quantity is at most that value)", "Use NO negation word. Include {TERM_LABEL}."),
    "yn_outcome_out": ("A yes/no question: is this case outside the {TERM_LABEL} set by the governing version? (yes "
                       "when the case's quantity is above that value)",
                       "Use NO negation word: say 'outside', 'beyond' or 'exceed'. Include {TERM_LABEL}."),
    "yn_outcome_not": ("A yes/no question that is the exact opposite of asking whether this case is within the "
                       "{TERM_LABEL} set by the governing version: yes exactly when it is NOT within it.",
                       "Use exactly ONE negation, 'not' or n't, on the main verb; no other negation word. Include "
                       "{TERM_LABEL}."),
}
DOUBLE_BRIEF = {
    "yn_version": "is {CANDIDATE} the version that governs this case (yes only when it governs)",
    "yn_claim": "does the governing version support the claim to check in the case record",
    "yn_outcome": "is this case within the {TERM_LABEL} set by the governing version",
}
STYLE_TRAIN = ("a plain question with no opening phrase", "open with 'Under these rules,'",
               "open with 'According to the card,'", "open with 'Going by the version history,'",
               "a plain question that names {DOC}", "a plain question that names case {CASE_ID}",
               "a plain question that ends with 'for case {CASE_ID}?'")
STYLE_HELD = ("open with 'Reading the history as written,'", "open with 'On the listed versions and case facts,'",
              "open with 'Taking the card at its word,'")


# ------------------------------------------------------------------------------------------------ batches
def _pack_items():
    items, plan = [], {}
    for d, pack in P.DOMAINS.items():
        labels = dict(zip(ROLE_WORDS, pack.labels))
        if pack.pair:
            a, b = (ROLE_WORDS[P.ROLES.index(r)] for r in pack.pair)
            qty = (f"The case quantity is a day count from the {a}-role date to the {b}-role date; the program writes "
                   f"its label, so qty_label is \"\".")
        else:
            qty = (f"The case quantity is an input, {KIND_TEXT[pack.tkind]} (example label: \"{pack.qty}\"); write its "
                   f"qty_label.")
        for i, setting in enumerate(DOMAIN_SETTINGS[d]):
            iid = f"t23a.pack.{d}.{i}"
            brief = (f"Domain: {d}. Setting: {setting}. The document sets one value per version: {KIND_TEXT[pack.tkind]} "
                     f"(example term label: \"{pack.term}\"). {qty} Date roles (example labels, vary them): purchase "
                     f"= \"{labels['purchase']}\", event = \"{labels['event']}\", filing = \"{labels['filing']}\", "
                     f"decision = \"{labels['decision']}\" (the day the organisation settles the case).")
            items.append((iid, {"brief": brief}))
            plan[iid] = {"role": "pack", "domain": d, "held_out": i == PACKS_PER_DOMAIN - 1}
    return items, plan


def _skin_items():
    items, plan = [], {}
    k = 0
    for ri, (reg, n) in enumerate(SKIN_PLAN.items()):
        held = reg in HELD_REGISTERS
        for i in range(n):
            tone = tuple(TONES)[k % len(TONES)]
            use_id = (i + ri) % 2 == 0
            k += 1
            setting = SKIN_SETTINGS[(i * 5 + ri * 3) % len(SKIN_SETTINGS)]
            iid = f"t23a.skin.{reg}.{i:03d}"
            rules = list(REGISTER_RULES[reg]) + ["Use {CASE_ID} exactly once." if use_id else "Leave {CASE_ID} out."]
            items.append((iid, {"brief": f"Write {REGISTER_DESC[reg]}. Setting: {setting}. Tone: {TONES[tone]}.",
                                "register": reg, "slots": {"CUSTOMER": "name", "ORG": "name", "ITEM": "name",
                                                           **({"CASE_ID": "id"} if use_id else {})},
                                "rules": rules}))
            plan[iid] = {"role": "skin", "register": reg, "tone": tone, "held_out": held, "case_id": use_id,
                         "escape": reg if reg in ("json", "yaml") else "text"}
    return items, plan


def _freeform_items():
    items, plan = [], {}
    doms = tuple(P.DOMAINS)
    for i in range(N_FREEFORM):
        reg = FREEFORM_REGISTERS[i % len(FREEFORM_REGISTERS)]
        d = doms[(i // len(FREEFORM_REGISTERS)) % len(doms)]
        item = P.DOMAINS[d].items[(i * 7 + i // len(doms)) % len(P.DOMAINS[d].items)]
        facts = {"CUSTOMER": f"{FIRST[(i * 7) % len(FIRST)]} {LAST[(i * 5 + i // len(FIRST)) % len(LAST)]}",
                 "ORG": FF_ORGS[(i * 3 + i // 20) % len(FF_ORGS)], "ITEM": item, "CASE_ID": f"CASE-{4100 + i * 37}"}
        tone = tuple(TONES)[(i // 3) % len(TONES)]
        iid = f"t23a.memo.{reg}.{i:03d}"
        items.append((iid, {"brief": f"A customer case about the customer's {item} (the ITEM), raised with an everyday "
                                     f"business (the ORG). Tone: {TONES[tone]}.",
                            "register": reg, "facts": dict(facts), "rules": list(FREEFORM_RULES[reg])}))
        plan[iid] = {"role": "freeform", "register": reg, "domain": d, "tone": tone, "held_out": False, "facts": facts}
    return items, plan


def _attack_items():
    items, plan = [], {}
    for i in range(N_ATTACK):
        use_c = i % 2 == 0
        iid = f"t23a.attack.{i:03d}"
        items.append((iid, {"brief": "Kind of pressure: " + ATTACK_KINDS[i % len(ATTACK_KINDS)] + ".",
                            "register": "note", "slots": {"CUSTOMER": "name"} if use_c else {},
                            "rules": ["Use {CUSTOMER} exactly once." if use_c else "Use no placeholder and no name."]}))
        plan[iid] = {"role": "attack", "held_out": i >= N_ATTACK - N_ATTACK_HELD,
                     "decl": {"CUSTOMER": "name"} if use_c else {}}
    return items, plan


def _wording_items():
    items, plan = [], {}
    for q, (n_train, n_held, n_double) in WORDING_PLAN.items():
        meaning, neg_rule = WORDING_BRIEF[q]
        allowed = "Allowed placeholders: " + ", ".join("{" + s + "}" for s in WORDING_SLOTS[q]) + "."
        for i in range(n_train + n_held + n_double):
            held = n_train <= i < n_train + n_held
            double = i >= n_train + n_held
            style = (STYLE_HELD[i % len(STYLE_HELD)] if held else STYLE_TRAIN[i % len(STYLE_TRAIN)])
            if double:
                brief = (f"A yes/no question with the SAME meaning as asking: {DOUBLE_BRIEF[q]}? Write it with exactly "
                         f"TWO syntactic negations that cancel out (for example 'Is it not the case that ... does not "
                         f"...?').")
                rules = ["Use exactly two negation words, each 'not' or n't; no other negation word.",
                         *([f"Include {{{x}}}." for x in NEEDS.get(q, ())]), allowed]
            else:
                brief = meaning
                rules = [neg_rule, allowed, f"Style hint: {style}."]
            iid = f"t23a.wording.{q}.{i:03d}"
            items.append((iid, {"brief": brief, "slots": dict(WORDING_SLOTS[q]), "rules": rules}))
            plan[iid] = {"role": "wording", "qform": q, "held_out": held, "double": double}
    return items, plan


BATCH_SPECS = (
    # name, chunker kind, items fn, prompt, forbid, max items per chunk
    ("packs", "author_pack", _pack_items, PACK_PROMPT, FORBID_ALL, 10),
    ("skins", "author_skin", _skin_items, SKIN_PROMPT, FORBID_ALL, 44),
    ("freeform", "author_freeform", _freeform_items, FREEFORM_PROMPT, FORBID_ALL, 45),
    ("attacks", "author_skin", _attack_items, ATTACK_PROMPT, FORBID_ALL, 30),
    ("wordings", "author_wording", _wording_items, WORDING_PROMPT, QSTRINGS, 43),
)


def build_batches() -> dict:
    out = {}
    for name, kind, fn, prompt, forbid, mx in BATCH_SPECS:
        items, plan = fn()
        b = chunker.make_batch(kind, FAMILY, items, seed=f"{SEED}|{name}", prompt=prompt, max_items=mx,
                               forbid_strings=forbid)
        out[name] = (b, plan)
    return out


def task_file_text(b, chunk: dict, answer_abs: str) -> str:
    n = len(chunk["items"])
    return "\n".join([
        f"# Haiku authoring task {chunk['task_id']} (family {FAMILY}, kind {b.kind})", "",
        "Read this whole file. Do not open any other file. When you are done, write your answer with the Write tool "
        "to exactly this path (nothing else, no other file):", "", f"    {answer_abs}", "",
        f"The answer is one JSON list with exactly {n} objects, one per item below, each carrying that item's qid.", "",
        "## Instructions", "", b.prompt, "", "## Answer format", "", ANSWER_FORMAT[b.kind], "",
        f"## Items ({n}; one JSON object per line)", "", "```json",
        "[\n" + ",\n".join(json.dumps(it, ensure_ascii=False) for it in chunk["items"]) + "\n]", "```", ""])


def write_tasks(root: Path = ROOT) -> list:
    """Write every batch (guarded writers) and return the task list [{task_file, answer_file, kind, ...}]."""
    tasks, files = [], {}
    for name, (b, plan) in build_batches().items():
        files.update(b.files())
        files[f"plan/{b.batch_id}.json"] = json.dumps({"batch_id": b.batch_id, "name": name, "kind": b.kind,
                                                       "plan": plan}, indent=1, sort_keys=True) + "\n"
        for c in b.chunks:
            tid = c["task_id"]
            ans = str(root / b.answer_path(tid))
            tfile = f"tasks/{tid}.md"
            files[tfile] = task_file_text(b, c, ans)
            tasks.append({"task_file": str(root / tfile), "answer_file": ans, "kind": b.kind, "batch": name,
                          "batch_id": b.batch_id, "task_id": tid, "n_items": len(c["items"]),
                          "prompt_sha": b.prompt_sha,
                          "audit_allowed_read": [str(root / tfile)], "audit_allowed_write": [ans]})
    for f in list(files) + [t["answer_file"] for t in tasks]:
        if paths.never_open(root / f):
            raise paths.NeverOpen(f"task path on the never-open list: {f}")
    paths.write_files(root, files)
    index = {"family": FAMILY, "seed": SEED, "n_tasks": len(tasks), "tasks": tasks,
             "g0_sha256": P.T23.G0_SHA256_V3, "g0_haiku_task": P.T23.G0_HAIKU_TASK,
             "note": "authoring only: Haiku text never sets, edits or chooses a label; answers go through the loaders, "
                     "G-SL, G-LEX, G3-H and G13 before any pool use"}
    paths.write_json(root / "TASKS.json", index)
    return tasks


# ------------------------------------------------------------------------------------------------ loaders
def read_plan(root: Path = ROOT) -> dict:
    """{batch name: (batch_id, kind, plan)} from plan/*.json."""
    out = {}
    for f in sorted((root / "plan").glob("*.json")):
        o = json.loads(f.read_text())
        out[o["name"]] = (o["batch_id"], o["kind"], o["plan"])
    return out


def load_answers_for(name: str, root: Path = ROOT) -> tuple:
    """(TaskBatch, plan, {internal id: answer}, problems) for one batch name, from answers/<task_id>.json."""
    b, plan = build_batches()[name]
    raw, probs = {}, []
    for c in b.chunks:
        f = root / b.answer_path(c["task_id"])
        if not f.is_file():
            probs.append(f"{c['task_id']}: no answer file")
            continue
        try:
            raw[c["task_id"]] = json.loads(f.read_text(encoding="utf-8"))
        except json.JSONDecodeError as e:
            probs.append(f"{c['task_id']}: answer is not JSON ({e})")
    ans, p2 = chunker.load_answers(b, raw)
    return b, plan, ans, probs + p2


def _task_of(b, iid: str) -> str:
    inv = {v: k for k, v in b.key.items()}
    return b.task_of[inv[iid]]


def _bad_substr(s: str) -> bool:
    low = s.lower()
    return "ohs" in low or "jev" in low


def _has_word(text: str, words) -> list:
    low = " " + " ".join(re.findall(r"[a-z']+", text.lower())) + " "
    return [w for w in words if f" {w} " in low]


def _label_hits(text: str) -> list:
    low = text.lower()
    return [w for w in P.T23.LABEL_WORDS if re.search(r"(?<![a-z])" + re.escape(w) + r"(?![a-z])", low)]


_LOWER_WORDS = re.compile(r"^[a-z][a-z' -]*[a-z]$")
_CAP_NAME = re.compile(r"^[A-Z][a-z'-]+(?: [A-Z][a-z'-]+){1,2}$")
PACK_KEYS = {"doc", "term_label", "qty_label", "date_labels", "items", "orgs", "customers", "prefix"}


def _words(s: str) -> int:
    return len(s.split())


def validate_pack(p, domain: str) -> list:
    """T23 pack shape (G0 section 7). Empty list = valid."""
    if not isinstance(p, dict) or set(p) != PACK_KEYS:
        return [f"pack keys {sorted(p) if isinstance(p, dict) else type(p).__name__} != {sorted(PACK_KEYS)}"]
    probs = []
    dom = P.DOMAINS[domain]
    for key, lo, hi in (("doc", 2, 4), ("term_label", 2, 5)):
        v = p[key]
        if not (isinstance(v, str) and _LOWER_WORDS.fullmatch(v) and lo <= _words(v) <= hi):
            probs.append(f"{key} {v!r}")
    q = p["qty_label"]
    if dom.pair is None:
        if not (isinstance(q, str) and _LOWER_WORDS.fullmatch(q) and 2 <= _words(q) <= 6) or q.startswith("day count"):
            probs.append(f"qty_label {q!r}")
    elif q != "":
        probs.append("qty_label must be empty for a day-count domain")
    dl = p["date_labels"]
    if not (isinstance(dl, dict) and set(dl) == set(ROLE_WORDS)):
        probs.append("date_labels keys")
    else:
        labs = [dl[r] for r in ROLE_WORDS]
        for lab in labs:
            if not (isinstance(lab, str) and _LOWER_WORDS.fullmatch(lab) and lab.endswith(" date")
                    and 2 <= _words(lab) <= 4) or " to " in f" {lab} ":
                probs.append(f"date label {lab!r}")
        if len(set(labs)) != 4 or any(a != b and isinstance(a, str) and isinstance(b, str) and a in b
                                      for a in labs for b in labs):
            probs.append("date labels repeat or contain each other")
    for key, n, rx in (("items", 5, _LOWER_WORDS), ("orgs", 3, _CAP_NAME), ("customers", 6, _CAP_NAME)):
        v = p[key]
        if not (isinstance(v, list) and len(v) == n and len(set(v)) == n
                and all(isinstance(x, str) and rx.fullmatch(x) for x in v)):
            probs.append(f"{key} {v!r}"[:120])
        elif key == "items" and any(_words(x) > 3 for x in v):
            probs.append("items: 1-3 words")
    if not (isinstance(p["prefix"], str) and re.fullmatch(r"[A-Z]{2}", p["prefix"]) and p["prefix"] not in ("ID", "NO",
                                                                                                         "OK")):
        probs.append(f"prefix {p['prefix']!r}")
    if probs:
        return probs
    strings = [p["doc"], p["term_label"], p["qty_label"], *p["date_labels"].values(), *p["items"], *p["orgs"],
               *p["customers"]]
    for s in strings:
        if not s:
            continue
        try:
            S.name_slot(s)
        except S.SlotError as e:
            probs.append(str(e)[:100])
        if _label_hits(s) or negcount.k_all(s):
            probs.append(f"label or negation word in {s!r}")
        if _has_word(s, ("new", "old", "latest", "current", "updated", "effective", "version")):
            probs.append(f"time / change word in {s!r}")
    if _bad_substr(json.dumps(p)):
        probs.append("a value holds a never-open letter sequence")
    return probs


def to_plugin_pack(p: dict, domain: str, *, held_out: bool, pack_id: str) -> dict:
    """The answer's pack as plugin.Pack + names: the domain keeps its term kind, pool and day-count pair (G0 7); a
    day-count QTY_LABEL is program-made from the pair's date labels."""
    dom = P.DOMAINS[domain]
    labels = tuple(p["date_labels"][r] for r in ROLE_WORDS)
    if dom.pair:
        a, b = (labels[P.ROLES.index(r)][:-len(" date")] for r in dom.pair)
        qty = f"day count from {a} to {b}"
    else:
        qty = p["qty_label"]
    pack = P.Pack(p["doc"], p["term_label"], dom.tkind, dom.pool, qty, dom.pair, labels, tuple(p["items"]),
                  p["prefix"])
    return {"id": pack_id, "domain": domain, "pack": pack, "orgs": tuple(p["orgs"]),
            "customers": tuple(p["customers"]), "held_out": held_out}


def load_packs(root: Path = ROOT) -> tuple:
    b, plan, ans, probs = load_answers_for("packs", root)
    out, seen = [], set()
    for iid, a in sorted(ans.items()):
        p = a.get("pack") if isinstance(a, dict) else None
        meta = plan[iid]
        v = validate_pack(p, meta["domain"])
        if not v and (set(p["orgs"]) & seen):
            v = ["an organisation name repeats another pack's"]
        if v:
            probs.append(f"{iid}: " + "; ".join(v[:4]))
            continue
        seen |= set(p["orgs"])
        out.append(to_plugin_pack(p, meta["domain"], held_out=meta["held_out"], pack_id=f"t23pk-{iid.split('.', 2)[2]}"))
    return out, probs


def _program_head(text: str) -> bool:
    return any(line.lstrip().startswith(BLOCK_HEADS) for line in text.split("\n"))


def _norm(text: str) -> str:
    return " ".join(text.split()).lower()


def _loop(name: str, root: Path, check) -> tuple:
    b, plan, ans, probs = load_answers_for(name, root)
    out, seen = [], set()
    for iid, a in sorted(ans.items()):
        text = a.get("text") if isinstance(a, dict) else None
        obj, v = check(iid, text, plan[iid], _task_of(b, iid), b.prompt_sha, seen)
        if v:
            probs.append(f"{iid}: " + "; ".join(v[:4]))
        else:
            out.append(obj)
    return out, probs


SAMPLE = {"CUSTOMER": S.name_slot("Dana Okafor"), "ORG": S.name_slot("Redfern Bank"),
          "ITEM": S.name_slot("standing desk"), "CASE_ID": S.id_slot("CASE-1234")}


def _roundtrip(sk) -> list:
    """Fill with sample values and read back the way solver B does (skin.parse_skin)."""
    decl = sk.decl
    try:
        filled = sk.fill({k: v for k, v in SAMPLE.items() if k in decl}).text
        got = K.parse_skin(sk, filled, {k: (decl[k], ()) for k in decl})
    except Exception as e:  # noqa: BLE001
        return [f"fill / parse: {str(e)[:100]}"]
    want = {k: SAMPLE[k].value for k in decl}
    return [] if got == want else [f"parse_skin read {got}"]


def check_skin(iid, text, meta, tid, psha, seen) -> tuple:
    """Mode T narrative skin: make_skin + G-SL lint_template + the T23 skin word list + no program head + no question
    + a fill / parse round trip (G0 section 7)."""
    if not isinstance(text, str) or not text.strip():
        return None, ["no text"]
    text = text.strip()
    if _norm(text) in seen:
        return None, ["duplicate text"]
    decl = {"CUSTOMER": "name", "ORG": "name", "ITEM": "name"}
    if "{CASE_ID}" in text:
        decl["CASE_ID"] = "id"
    if meta["case_id"] != ("CASE_ID" in decl):
        return None, ["{CASE_ID} use does not follow the item's rule"]
    sid = f"T23-SK-{iid.split('.', 2)[2]}"
    try:
        sk = K.make_skin(sid, FAMILY, text, decl, register=meta["register"], escape=meta["escape"],
                         held_out=meta["held_out"], counts={"CUSTOMER": (1, 2), "ORG": (1, 2), "ITEM": (1, 2)},
                         haiku_task_id=tid, haiku_prompt_sha=psha)
    except Exception as e:  # noqa: BLE001
        return None, [str(e)[:120]]
    v = [f"G-SL {x.rule}: {x.detail}" for x in gsl.lint_template(
        sk, label_words=P.T23.LABEL_WORDS, exceptions=P.T23.GSL_EXCEPTIONS, name_allow=P.T23.NAME_ALLOW)]
    bad = _has_word(K.PH_RE.sub(" ", text), SKIN_BANNED)
    if bad:
        v.append(f"T23 skin word list: {bad[:4]}")
    if _program_head(text) or "?" in text:
        v.append("a program block head or a question")
    if len(K.PH_RE.sub("x", text).split()) > 60:
        v.append("longer than the length budget")
    v += _roundtrip(sk)
    if not v:
        seen.add(_norm(text))
    return sk, v


def check_attack(iid, text, meta, tid, psha, seen) -> tuple:
    """Attack line (R13, section 7): one line, G-SL attack role, no label word, never a block head or clause shape."""
    if not isinstance(text, str) or not text.strip() or "\n" in text.strip():
        return None, ["not one line"]
    text = text.strip()
    sid = f"T23-AT-{iid.rsplit('.', 1)[1]}"
    try:
        sk = K.make_skin(sid, FAMILY, text, dict(meta["decl"]), kind="attack", register="note",
                         held_out=meta["held_out"], haiku_task_id=tid, haiku_prompt_sha=psha)
    except Exception as e:  # noqa: BLE001
        return None, [str(e)[:120]]
    v = [f"G-SL {x.rule}: {x.detail}" for x in gsl.lint_template(sk, label_words=P.T23.LABEL_WORDS)]
    if _label_hits(K.PH_RE.sub(" ", text)):
        v.append(f"label word {_label_hits(text)}")
    if _norm(text) in seen:
        v.append("duplicate")
    if _program_head(text) or re.search(r"\bif\b.*\bthen\b", text, re.I) or re.search(r"\d", text):
        v.append("block head, rule shape or digit")
    if not 6 <= len(text.split()) <= 30:
        v.append("length")
    if not v:
        seen.add(_norm(text))
    return sk, v


def check_freeform(iid, text, meta, tid, psha, seen) -> tuple:
    """Mode F note: G-SL lint_freeform (every fact verbatim; no number, date, id, label word or negation outside the
    facts) + the T23 skin word list + no program head + a fill check."""
    if not isinstance(text, str) or not text.strip():
        return None, ["no text"]
    text = text.strip()
    facts = meta["facts"]
    v = [f"G-SL {x.rule}: {x.detail}" for x in gsl.lint_freeform(text, facts, label_words=P.T23.LABEL_WORDS)]
    rest = text
    for val in sorted(facts.values(), key=len, reverse=True):
        rest = rest.replace(val, " ")
    bad = _has_word(rest, SKIN_BANNED)
    if bad:
        v.append(f"T23 word list: {bad[:4]}")
    if _program_head(text) or "{" in text or "}" in text or "?" in text:
        v.append("program head, brace or question")
    if _norm(text) in seen:
        v.append("duplicate")
    sk = None
    if not v:
        decl = {"CUSTOMER": "name", "ORG": "name", "ITEM": "name", "CASE_ID": "id"}
        try:
            sk = K.make_skin(f"T23-MF-{iid.rsplit('.', 1)[1]}", FAMILY, text, decl, register=meta["register"],
                             author_mode="F", brief=facts, haiku_task_id=tid, haiku_prompt_sha=psha)
            sk.fill({k: SAMPLE[k] if k not in facts else (S.id_slot(facts[k]) if k == "CASE_ID"
                                                          else S.name_slot(facts[k])) for k in decl})
        except Exception as e:  # noqa: BLE001
            v.append(str(e)[:120])
    if not v:
        seen.add(_norm(text))
    return sk, v


def check_wording(iid, text, meta, tid, psha, seen) -> tuple:
    """Question wording: one line ending in '?', G-SL (role wording), its placeholders inside the form's allowed set
    with the required ones present, EXACT negcount per form (double-negation wordings: two syntactic), no banned
    word (G0 section 7). -> (qform, text, slots, held_out, double, task id, prompt sha); G-LEX admission comes next."""
    q = meta["qform"]
    if not isinstance(text, str) or "\n" in text.strip() or not text.strip().endswith("?"):
        return None, ["not one question line"]
    text = " ".join(text.split())
    names = [p.name for p in K.placeholders(text)]
    v = []
    if not set(names) <= set(WORDING_SLOTS[q]) or len(names) != len(set(names)):
        return None, [f"placeholders {names} (allowed {sorted(WORDING_SLOTS[q])}, each at most once)"]
    for need in NEEDS.get(q, ()):
        if need not in names:
            v.append(f"needs {{{need}}}")
    if q in P.CLAIM_FORMS and "claim" not in text.lower():
        v.append("a claim form names the claim")
    decl = {n: WORDING_SLOTS[q][n] for n in names}
    try:
        sk = K.make_skin("tmp", FAMILY, text, decl, kind="wording", register="question", qform=q)
    except Exception as e:  # noqa: BLE001
        return None, [str(e)[:120]]
    v += [f"G-SL {x.rule}: {x.detail}" for x in gsl.lint_template(sk)]
    c = negcount.count(K.PH_RE.sub("X", text))
    if meta["double"]:
        if (c.k_all, c.k_syn) != NEG_DOUBLE:
            v.append(f"negcount {(c.k_all, c.k_syn)} != {NEG_DOUBLE}")
    elif q == "yn_version_other":
        if c.k_syn != 0 or c.k_all > 1:
            v.append(f"negcount {(c.k_all, c.k_syn)}: no syntactic negation, 'other than' at most")
    elif (c.k_all, c.k_syn) != NEG_EXACT[q]:
        v.append(f"negcount {(c.k_all, c.k_syn)} != {NEG_EXACT[q]}")
    bad = _has_word(K.PH_RE.sub(" ", text), WORDING_BANNED)
    if bad:
        v.append(f"banned word {bad[:3]}")
    if not 6 <= len(text.split()) <= 30:
        v.append("length")
    if text.lower() in seen or text in QSTRINGS:
        v.append("duplicate or fixture copy")
    if not v:
        seen.add(text.lower())
    return (q, text, decl, meta["held_out"], meta["double"], tid, psha), v


def load_skins(root: Path = ROOT) -> tuple:
    out, probs = _loop("skins", root, check_skin)
    return {sk.skin_id: sk for sk in out}, probs


def load_attacks(root: Path = ROOT) -> tuple:
    out, probs = _loop("attacks", root, check_attack)
    return {sk.skin_id: sk for sk in out}, probs


def load_freeform(root: Path = ROOT) -> tuple:
    out, probs = _loop("freeform", root, check_freeform)
    return {sk.skin_id: sk for sk in out}, probs


def load_wordings(root: Path = ROOT) -> tuple:
    return _loop("wordings", root, check_wording)


def lexicon_registry(wordings: list) -> LexiconRegistry:
    """A T23 LexiconRegistry holding the loaded Haiku wordings (source haiku, pending until 2/2 G-LEX extraction admits
    them). Meanings: the 11 question forms (fixtures.QUESTION_MEANINGS) plus the two decoys (G0 section 7, H42)."""
    reg = LexiconRegistry(FAMILY)
    for qf, meaning in FX.QUESTION_MEANINGS.items():
        reg.declare(question_sem(FAMILY, qf), "question", meaning)
    for sem, meaning in QUESTION_DECOYS.items():
        reg.declare(sem, "question", meaning)
    for q, text, decl, held, _double, tid, psha in wordings:
        try:
            reg.add(text, question_sem(FAMILY, q), slots=dict(decl), family=FAMILY, source="haiku",
                    haiku_task_id=tid, haiku_prompt_sha=psha, held_out=held)
        except Exception:  # noqa: BLE001  (duplicate or malformed text: dropped, reported by the caller)
            continue
    reg.unit_test_all()
    return reg


# ------------------------------------------------------------------------------------------------ CLI
def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("cmd", choices=("plan", "write"))
    a = ap.parse_args(argv)
    if a.cmd == "plan":
        for name, (b, plan) in build_batches().items():
            print(f"{name:10s} {b.kind:16s} {b.batch_id}  items {len(b.key):4d}  chunks {len(b.chunks)}")
        return 0
    tasks = write_tasks()
    print(json.dumps({"n_tasks": len(tasks), "by_kind": {k: sum(1 for t in tasks if t["kind"] == k)
                                                         for k in sorted({t["kind"] for t in tasks})}}))
    return 0


if __name__ == "__main__":
    sys.exit(main())
