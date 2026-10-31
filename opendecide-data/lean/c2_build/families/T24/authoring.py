"""families/T24/authoring.py: the T24 Haiku AUTHORING tasks (G0_SPEC.md section 3; C2_DATA_SPEC 3.0, 3.12; README
"Haiku task flow"), plus the loader and program checks the lint stage uses. After A38 only: every write goes through
paths.write_files.

One make_batch per task (one chunk each, <= 50 items, opaque qids, gold-free). Haiku never sees a policy version, a
case, a question of a row, an option or a gold: it writes reusable pieces only. Forbidden strings (chunker
forbid_strings, checked in the prompt and in every item):
  FORBID          skins, Mode F documents, clause forms: the plugin LABEL_WORDS (materiality words, generic outcome
                  words, every stand-in outcome name) + the stand-in question strings
  FORBID_WORDING  question wordings: outcome words and names + stand-in questions (a wording asks about the outcome
                  differing, so the materiality words are its content; G-LEX admits its meaning)
  FORBID_PACK     packs: materiality words + stand-in questions (a pack defines its own outcome names)

  task                         kind              items x outputs     pool (G0 section 3)
  pack-a, pack-b               author_pack       40 x 1 pack         packs (R2 format; 80 everyday settings)
  lex-win                      author_lexicon     4 x 8 forms        t24.win (window, 3/3)
  lex-special                  author_lexicon     7 x 8 forms        t24.ovc 3 items, t24.ovd 4 items (window, 3/3)
  lex-amount                   author_lexicon    12 x 8 forms        t24.amt.ge / gt / le / lt (comparator, 2/2)
  lex-exc-alt                  author_lexicon     6 x 8 forms        t24.exc, t24.alt (other, 2/2)
  word-ch, word-pos, word-neg  author_wording   8-10 x 8 wordings    question wordings, training (6 forms)
  word-held                    author_wording     6 x 8 wordings     question wordings, held out (S5)
  skin-<register> (9)          author_skin        8 x 5 skins        Mode T narratives, training registers
  skin-transcript, -voicemail  author_skin        6 x 5 skins        Mode T narratives, held-out registers
  free-a, free-b               author_freeform   50 x 1 document     Mode F narratives (training)
  free-held                    author_freeform   24 x 1 document     Mode F narratives (held out)

Each task file (haiku/author/tasks/<task_id>.md) is self-contained: the exact answer path, the prompt and the items.
The agent reads only that file and writes only its answer file (audit.audit with TASKS.json's allowed paths). The
opaque-id key stays in haiku/author/key/ and the item metadata in TASKS.json (orchestrator only).

  ../../.venv/bin/python -m families.T24.authoring          (from lean/c2_build; writes haiku/author/, after A38 only)
"""
from __future__ import annotations

import hashlib
import json
import re
import sys
from dataclasses import dataclass
from pathlib import Path

HERE = Path(__file__).resolve().parent
C2_BUILD = HERE.parents[1]
if str(C2_BUILD) not in sys.path:
    sys.path.insert(0, str(C2_BUILD))

from c2_kit import chunker, gsl, paths  # noqa: E402
from c2_kit import polarity as POL  # noqa: E402
from c2_kit import skin as K  # noqa: E402
from c2_kit.lexicon import LexiconRegistry, question_sem  # noqa: E402
from families.T24 import fixtures as FX  # noqa: E402
from families.T24 import plugin as P  # noqa: E402

import negcount  # noqa: E402  (c_src/common, read-only; on sys.path through c2_kit.paths)

FAMILY = "T24"
ROOT = HERE / "haiku" / "author"
VERSION = "v1"
MAX_TASKS = 40

STANDIN_QUESTIONS = tuple(text for _wid, _qf, text in FX.WORDINGS + FX.HELD_WORDINGS)
OUTCOME_VOCAB = tuple(dict.fromkeys(P.OUTCOME_WORDS + tuple(o for d in P.STANDIN_DOMAINS.values()
                                                            for o in d.outcomes)))
FORBID = tuple(P.AUTHORING_LABEL_WORDS) + STANDIN_QUESTIONS     # the words v1 authoring ran with (frozen task files)
FORBID_WORDING = OUTCOME_VOCAB + STANDIN_QUESTIONS
FORBID_PACK = P.MATERIAL_WORDS + STANDIN_QUESTIONS
TRAIN_REGISTERS = tuple(r for r in P.T24Plugin.REGISTERS if r not in P.T24Plugin.HELD_OUT_REGISTERS)
HELD_REGISTERS = tuple(P.T24Plugin.HELD_OUT_REGISTERS)


def _bad(word: str, forbid: tuple) -> bool:
    return any(re.search(r"(?<![a-z0-9])" + re.escape(f.lower()) + r"(?![a-z0-9])", word.lower()) for f in forbid if f)


def _word_lists(forbid: tuple = FORBID) -> str:
    """The G-SL CORE + EXTENDED word lists (minus any forbidden string), as prompt text."""
    cats = ("number", "relative_time", "quantity", "quantifier", "modal", "hedge", "status", "operator")
    lines = []
    for c in cats:
        words = sorted(gsl.CORE.get(c, set()) | gsl.EXTENDED.get(c, set()))
        words = [w for w in words if not _bad(w, forbid) and w not in ("ca", "wo")]
        lines.append(f"   - {c.replace('_', ' ')}: " + ", ".join(words))
    lines.append("   - phrases: have to, has to, had to, got to, sort of, kind of")
    return "\n".join(lines)


NEGATION_CUES = ("not, n't (don't, isn't, can't, won't ...), no, none, nobody, nothing, nowhere, never, neither, nor, "
                 "cannot, without, lack, deny, hardly, scarcely, barely, few, except, unless, false, other than, "
                 "free of, no longer, fail to, neglect to, omit to, decline to, refuse to, prevent ... from, rule out")

COMMON = """You are writing short pieces of text for a synthetic training dataset about everyday customer-service
policies (returns, repairs, bookings, deposits, fees and the like). Everything you write is either a reusable template
(a program later fills each {SLOT} placeholder with a value) or a set of invented values. Write natural, varied
English. Invent everything: never copy text from real companies, products, people, laws, websites or published
datasets.

How to work: this task file is the only file you may open. Do not open, list or search any other file or folder.
Write your whole answer, and nothing else, as one JSON document to the ANSWER FILE path given at the top of this file,
with the Write tool. Inside JSON strings, write a line break as \\n and a double quote as \\".
"""

ANSWER = {
    "pack": '[{"qid": "<qid of the item>", "pack": {...the fields listed above...}}, ...]',
    "forms": '[{"qid": "<qid of the item>", "forms": ["<form 1>", "<form 2>", ...]}, ...]',
    "wordings": '[{"qid": "<qid of the item>", "wordings": ["<question 1>", "<question 2>", ...]}, ...]',
    "texts": '[{"qid": "<qid of the item>", "texts": ["<text 1>", "<text 2>", ...]}, ...]',
    "text": '[{"qid": "<qid of the item>", "text": "<the document>"}, ...]',
}


def _answer_block(field: str) -> str:
    return (f"\nAnswer format: one JSON array with one object per item (every item answered once):\n{ANSWER[field]}\n"
            "Copy each qid exactly. Give exactly the number of outputs each item asks for.\n")


# ------------------------------------------------------------------------------------------------ packs (G0 3.4, R2)
PACK_PROMPT = COMMON + """
TASK: invent one policy PACK per item: the vocabulary of one invented everyday customer-service policy. Each item
gives a setting (the kind of business or service); fit every value to it.

Fields of "pack" (all invented; no real company, brand, product, place or person):
- "title": the policy's name: two to four lower-case words ending with the word "policy" (e.g. "lost luggage policy").
- "prefix": exactly three capital letters that start the case numbers (e.g. "LUG").
- "date_fields": exactly two names of dates that every case of this policy has, each two or three lower-case words
  ending with the word "date" (e.g. ["flight date", "report date"]). In a normal case the first date is never later
  than the second. Neither may be "request date".
- "money_field": the name of the money amount of a case, one to three lower-case words (e.g. "claimed value").
- "categories": four or five kinds of items, services or plans the policy covers, lower case, one to three words each
  (e.g. ["suitcases", "backpacks", "sports gear", "instruments"]).
- "conditions": exactly three short states a case can be in, lower case, one to three words each, that read
  naturally after "the condition is" (e.g. ["tagged", "receipt kept", "photo only"]).
- "outcomes": exactly three outcome names, lower case, two or three words each, in this order: the full result the
  customer asks for, a partial or alternative result, and the request turned down (e.g. ["full settlement",
  "partial settlement", "claim declined"]). Each reads naturally after "the outcome is".

Rules for every value (a pack that breaks one is thrown away):
1. Only lower-case letters, spaces, hyphens and apostrophes (the prefix: three capital letters); no digits, commas,
   pipes or braces; never the word "and".
2. No negation word or cue anywhere: """ + NEGATION_CUES + """.
3. All values within a pack are distinct, and no word of the three outcome names appears in the categories,
   conditions, date fields or money field. Categories, conditions, date fields and the money field never use the
   words refund, credit, compensation, voucher, reimbursement, payout or rebate.
4. No word about comparing or revising anywhere (such as alter, revise, update, version, identical, compare).
5. Everyday consumer settings only: nothing medical, legal, about children or about personal safety; plain words.
6. Every pack in your answer has its own title, prefix and categories (no repeats across items).
""" + _answer_block("pack")

PACK_SETTINGS = (
    "a bicycle rental shop", "a dry cleaner", "a pet grooming salon", "a furniture delivery service",
    "a car wash chain", "a meal kit delivery service", "a photo printing shop", "a language learning app",
    "a concert hall cloakroom", "a phone repair kiosk", "a self-service laundromat", "a museum gift shop",
    "a ski equipment rental", "a boat tour operator", "a cooking class school", "a garden centre",
    "an online bookshop", "a bakery taking custom cake orders", "a coworking space", "a parking garage",
    "a home cleaning service", "a removals firm", "a camera rental shop", "a tailoring shop",
    "a flower delivery service", "a music streaming service", "a city bike share scheme", "a bowling alley",
    "a poster printing shop", "a toy library", "a wedding venue", "a campsite", "a dog walking service",
    "a computer repair shop", "a mattress store", "a day spa", "a climbing wall", "an escape room venue",
    "a car parts shop", "a shoe repair shop", "a farm produce box delivery", "a dance studio",
    "a vintage clothing shop", "a board game cafe", "a public swimming pool", "a key cutting kiosk",
    "a piano tuning service", "a car ferry booking desk", "a printer ink shop", "a costume rental shop",
    "a picture framing shop", "a tutoring centre", "a coffee machine supplier", "a window cleaning service",
    "a craft supply store", "a portrait photography studio", "an online plant nursery", "a self-storage facility",
    "a driving school", "a hair salon", "a tool hire shop", "a pottery studio", "a kayak hire base", "a wine club",
    "a stationery shop", "a party equipment hire", "a sports kit shop", "a cinema", "a holiday cottage agency",
    "an electric bike shop", "a carpet cleaning service", "a jewellery repair shop", "a magazine publisher",
    "a language exam centre", "a golf course", "a recording studio", "a chess club", "a cat boarding cattery",
    "a scuba diving school", "a theme park",
)

# ------------------------------------------------------------------------------------------------ clause forms (3.1)
LEX_PROMPT = COMMON + """
TASK: write CLAUSE FORMS: one-line clauses that a program inserts into the versions of an invented customer-service
policy, both as bullet lines ("- <clause>.") and as cells of a table. Each item states the exact meaning, the
placeholders to keep and the edge case that must stay clear; write the number of distinct forms it asks for, all
with exactly that meaning.

How the program fills the placeholders: {N} becomes a number of days with its unit (e.g. "14 days" or "fourteen
days"); {A} the name of one date of the case (e.g. "delivery date"); {M} the name of the money amount (e.g. "price");
{X} an amount of money (e.g. "$1,250.00", "1,250.00 USD" or "$1,250"); {C} a category name (e.g. "suitcases");
{K} a condition name (e.g. "receipt kept"); {O} an outcome name (e.g. "partial settlement"); {S} and {E} dates
(e.g. "5 March 2026").

Hard rules (a form that breaks one is thrown away):
1. One line that starts with a capital letter, never with a placeholder; no period or other punctuation at the end.
2. Keep every listed placeholder exactly once, spelled exactly so with its curly braces; add no other placeholder.
   Two placeholders never touch (always at least one word between them). Never write "a" or "an" right before a
   placeholder, and never add the word "days" after {N} (it already holds the unit).
3. No digits, number words, dates, months, amounts or other values: the program supplies every value.
4. No hedges (about, around, roughly, nearly, almost, approximately, usually) and no double quote characters.
5. The meaning must be unmistakable to any careful reader, including at the edge case the item names. A form adds
   no condition, no exception and no second idea, and never mentions any other clause.
6. All forms in your answer are distinct.
""" + _answer_block("forms")

LEX_SLOTS = {
    "N": "the time limit: a number of days with its unit, e.g. '14 days'",
    "A": "the name of one date of the case, e.g. 'delivery date'",
    "M": "the name of the money amount of the case, e.g. 'price'",
    "X": "an amount of money, e.g. '$1,250.00'",
    "C": "a category name, e.g. 'suitcases'",
    "K": "a condition name, e.g. 'receipt kept'",
    "O": "an outcome name, e.g. 'partial settlement'",
    "S": "the first date of the window, e.g. '5 March 2026'",
    "E": "the last date of the window, e.g. '19 March 2026'",
}
LEX_MEANING = {
    "t24.win": ("the base time limit: a request is on time when it is made at most {N} after the {A}. The {A} itself is "
                "day zero, so a request made exactly {N} after the {A} is still on time, and one day later is late",
                "a request made exactly {N} after the {A} is on time",
                "never use wordings whose edge reading is unclear, such as 'before {N} have passed', 'less than {N}', "
                "'under {N}' or 'by the end of'"),
    "t24.ovc": ("a special time limit for one category: cases in the category {C} have the time limit {N}, which "
                "replaces the usual time limit for them (the days are still counted from the date the usual time "
                "limit names)",
                "the form makes clear that {N} replaces the usual time limit for the {C} category (e.g. with "
                "'instead' or 'in place of the usual time limit')",
                "never name a date and never say what the days are counted from"),
    "t24.ovd": ("a special time limit by date window: cases whose {A} falls inside the window from {S} to {E}, with "
                "BOTH end dates included, have the time limit {N}, which replaces the usual time limit for them",
                "a case whose {A} is exactly {S} or exactly {E} is inside the window",
                "state the inclusivity inside the form ('both dates included', 'inclusive', 'from {S} through {E}', "
                "'on or after {S} and on or before {E}'); never a bare 'from {S} to {E}', 'between {S} and {E}' or "
                "'until {E}'; make clear that {N} replaces the usual time limit"),
    "t24.amt.ge": ("the {M} of a case must be at least {X}: an amount exactly equal to {X} meets the rule, and a "
                   "smaller amount fails it",
                   "an amount exactly equal to {X} meets the rule", "never use 'up to' or 'within'"),
    "t24.amt.gt": ("the {M} of a case must be strictly more than {X}: an amount exactly equal to {X} fails the rule",
                   "an amount exactly equal to {X} fails the rule", "never use 'up to' or 'within'"),
    "t24.amt.le": ("the {M} of a case must be at most {X}: an amount exactly equal to {X} meets the rule, and a larger "
                   "amount fails it",
                   "an amount exactly equal to {X} meets the rule", "never use 'up to' or 'within'"),
    "t24.amt.lt": ("the {M} of a case must be strictly less than {X}: an amount exactly equal to {X} fails the rule",
                   "an amount exactly equal to {X} fails the rule", "never use 'up to' or 'within'"),
    "t24.exc": ("cases in the category {C} are excluded from this policy: it gives them nothing at all",
                "every case in the {C} category is excluded", "never mention any other category"),
    "t24.alt": ("cases whose condition is {K} get the outcome {O}: the clause names the outcome for that condition and "
                "adds no other rule",
                "{K} is the case's condition and {O} is the outcome it gets",
                "never say what happens to cases in other conditions"),
}
LEX_SLOTS_OF = {"t24.win": ("N", "A"), "t24.ovc": ("C", "N"), "t24.ovd": ("A", "S", "E", "N"), "t24.exc": ("C",),
                "t24.alt": ("K", "O"), **{f"t24.amt.{op}": ("M", "X") for op in P.OPS}}
LEX_STYLES = {
    "t24.win": ("a rule about when a request has to be made", "a statement of the time limit itself, naming the date "
                "it is counted from", "phrased around the customer (e.g. 'Customers have ...')",
                "a short policy line"),
    "t24.ovc": ("a short policy line", "phrased around the category ('For the {C} category, ...')",
                "phrased around the time limit ('The time limit for ...')"),
    "t24.ovd": ("a short policy line", "phrased around the cases ('Cases whose {A} ...')",
                "phrased around the time limit ('The time limit is {N} instead for ...')",
                "starting with 'For' or 'When'"),
    "amt.pos": ("stated as a requirement on the {M} (e.g. 'The {M} must ...')",
                "stated as which cases qualify (e.g. 'Only cases whose {M} ... qualify', 'A case qualifies when ...')"),
    "amt.neg": ("stated as which cases do not qualify, naming the failing side (e.g. 'Cases whose {M} ... do not "
                "qualify'); here one negation such as 'do not' is allowed and wanted",),
    "t24.exc": ("a short policy line", "phrased around the category ('The {C} category ...')",
                "phrased around the policy's cover ('This policy ...')"),
    "t24.alt": ("a short policy line", "phrased around the condition ('For cases whose condition is {K}, ...')",
                "phrased around the outcome ('The outcome is {O} for ...')"),
}
LEX_KIND = {"t24.win": "window", "t24.ovc": "window", "t24.ovd": "window", "t24.exc": "other", "t24.alt": "other",
            **{f"t24.amt.{op}": "comparator" for op in P.OPS}}
FORMS_PER_ITEM = 8


def _lex_item(sem: str, style: str) -> dict:
    meaning, edge, avoid = LEX_MEANING[sem]
    slots = LEX_SLOTS_OF[sem]
    return {"brief": {"how_many": FORMS_PER_ITEM, "style": style, "edge_case": edge, "avoid": avoid},
            "meaning": meaning, "slots": {s: LEX_SLOTS[s] for s in slots},
            "rules": [f"{FORMS_PER_ITEM} forms", ", ".join("{" + s + "}" for s in slots) + ": each exactly once",
                      "one line, capital first letter, no period at the end"]}


# ------------------------------------------------------------------------------------------------ wordings (3.3)
WORDING_PROMPT = COMMON + """
TASK: write QUESTION WORDINGS. A program shows two versions of one invented customer-service policy (an original
version and a revised version), the record of one case and the rules for applying a version to a case: each version,
applied on its own, gives the case one outcome. Then it asks one question in your wording. Each item states exactly
what the question must mean; write the number of distinct wordings it asks for, all with that meaning.

Hard rules (a wording that breaks one is thrown away):
1. One question, 8-30 words, ending with "?". No placeholders, no names, no digits or numbers, no dates, no time
   words (today, now, currently, already, yet, soon, later), no hedges (maybe, probably, seems, likely, think).
2. Keep the meaning exactly as the item states it: do not widen, narrow or soften it. The question is about the
   OUTCOME FOR THIS CASE, never about the wording of the policy: use the word "outcome", and "this case" or "the case".
3. Refer to the versions only as "the original version", "the revised version", "both versions", "the two versions"
   or "the revision". Never "new policy", "old policy", "update", "draft" or the like.
4. Never name an outcome and never list answer choices.
5. Negation exactly as the item says. Negation words and cues: not, n't, no, none, nobody, nothing, nowhere, never,
   neither, nor, and also without, fail to, lack, unless, except, false, cannot, hardly. Never start a question with
   "Isn't", "Doesn't", "Don't", "Aren't" or "Wasn't": such leading questions read two ways.
6. Capital letter only on the first word. Vary the structure across your wordings (the case as the subject, the
   revised version as the subject, "Under ...", "Comparing ...", short and long forms).
""" + _answer_block("wordings")

Q_MEANING = {
    "yn_changes": ("yes/no: does this case get a different outcome under the revised version than under the original "
                   "version? Yes exactly when the two outcomes differ. No negation word or cue at all"),
    "yn_same": ("yes/no: does this case get one and the same outcome under both versions? Yes exactly when the two "
                "outcomes are equal. Use a positive word for equality (same, identical, unchanged, alike, equal); no "
                "negation word or cue at all"),
    "yn_not_change": ("yes/no, the negated form of asking whether the revision alters this case's outcome: yes exactly "
                      "when the outcome stays as it was. Put exactly one 'not' or 'n't' on the verb of altering "
                      "(change, alter, give another outcome), inside the question (e.g. 'Is it true that ... does not "
                      "...?' or 'Does ... not ...?'); no other negation word or cue"),
    "yn_fail_change": ("yes/no: asks whether the revision fails to alter this case's outcome: yes exactly when the "
                       "outcome stays as it was. Use 'fail to', 'fails to' or 'failed to' exactly once with a verb of "
                       "altering (change, alter, shift); no other negation word or cue at all (no not, n't, no, never, "
                       "nothing, without)"),
    "yn_dneg": ("yes/no with a double negation whose meaning is positive: it asks whether it is untrue that the "
                "revision leaves this case's outcome as it was, so yes exactly when the two outcomes differ. Use "
                "exactly two negation words from: not, n't, no, never, nothing (e.g. 'Is it not true that ... makes "
                "no difference to the outcome ...?' or 'Is it not the case that ... leaves the outcome with no change "
                "...?'), both in the one sentence, and no other negation cue (no fail to, without, false, unless)"),
    "ch_v2": ("asks which outcome this case gets under the revised version. The reader picks the outcome from a list "
              "shown after the question, so the question names no outcome. No negation word or cue at all"),
}
WORDING_STYLES = ("short and direct", "formal, like a reviewer's checklist", "plain conversational",
                  "the case as the subject", "the revised version as the subject", "careful and precise",
                  "neutral clerk's tone", "brisk workplace tone", "longer, with a short lead-in phrase",
                  "simple words only")
HELD_STYLE = ("phrased as a check made by an auditor who reads both documents side by side; plain words; wordings "
              "unlike common phrasings")
WORDING_TASKS = (("word-ch", (("ch_v2", 10),)), ("word-pos", (("yn_changes", 5), ("yn_same", 3))),
                 ("word-neg", (("yn_not_change", 3), ("yn_fail_change", 3), ("yn_dneg", 3))))
WORDINGS_PER_ITEM = 8

# ------------------------------------------------------------------------------------------------ skins (3.2)
SKIN_SLOTS = {
    "CUSTOMER": "the customer's full name, e.g. 'Jordan Vale'",
    "CASE_ID": "the case number, e.g. 'LUG-48213'",
    "CAT": "the category of the case, a short lower-case label, e.g. 'suitcases'; use it as a label, as in "
           "'category: {CAT}' or 'the {CAT} category'",
    "COND": "the condition noted on the case, a short lower-case label, e.g. 'receipt kept'; use it only as a "
            "labelled value, as in 'condition: {COND}'",
    "AMOUNT": "the money amount of the case, e.g. '$1,250.00'; use it only as a labelled value, as in "
              "'amount: {AMOUNT}'",
    "REQ": "the date the request was sent, e.g. '5 March 2026'; use it only as that date, as in 'sent on {REQ}' or "
           "'request date: {REQ}'",
}
PROSE_SETS = (("CUSTOMER", "CASE_ID"), ("CUSTOMER",), ("CUSTOMER", "CASE_ID", "REQ"), ("CUSTOMER", "CASE_ID"),
              ("CUSTOMER", "CAT"))
FIELD_SETS = (("CUSTOMER", "CASE_ID", "CAT"), ("CUSTOMER", "CASE_ID", "COND"), ("CUSTOMER", "CASE_ID", "AMOUNT"),
              ("CUSTOMER", "CASE_ID", "REQ"), ("CUSTOMER", "CASE_ID"))
FIELD_REGISTERS = ("ticket", "json", "yaml", "log", "form")
ESCAPE = {"json": "json", "yaml": "yaml"}
REGISTER_FORMAT = {
    "memo": ("an internal case note or memo: one to three sentences of prose, optionally starting with a short "
             "heading such as 'Case note:'",
             "Case note: {CUSTOMER} contacted the service desk about case {CASE_ID} and asked to have the request "
             "looked at."),
    "email": ("a short e-mail from the customer: a greeting line, one to three sentences and a sign-off line, on "
              "separate lines (single line breaks only, never an empty line)",
              "Hello,\nI am writing about case {CASE_ID}. Please look at my request.\nKind regards,\n{CUSTOMER}"),
    "chat": ("a chat message: starts with '{CUSTOMER}: ' and then one or two casual lines of what they type",
             "{CUSTOMER}: hi, this is about case {CASE_ID}. where do I stand with my request?"),
    "ticket": ("a support ticket: two to four short lines with labelled fields (such as 'Ticket:', 'Requester:', "
               "'Topic:') or fields separated by ' | '",
               "Ticket {CASE_ID}\nRequester: {CUSTOMER}\nTopic: request under the policy"),
    "json": ("a JSON object (one or several lines) with three to five snake_case keys; each placeholder is a bare JSON "
             "value with no quotes around it, e.g. \"customer\": {CUSTOMER}; at most one extra key whose value is a "
             "plain neutral word or short phrase in quotes (such as \"topic\": \"request\")",
             '{"case": {CASE_ID}, "customer": {CUSTOMER}, "topic": "request under the policy"}'),
    "yaml": ("a block-style YAML mapping with three to five lowercase keys (two-space indentation for nested keys; "
             "never inline {key: value} mappings); each placeholder is a plain value",
             "case: {CASE_ID}\ncustomer: {CUSTOMER}\ntopic: request under the policy"),
    "letter": ("a short formal letter: a salutation line, two to four sentences and a closing line, on separate lines "
               "(single line breaks only, never an empty line)",
               "Dear support team,\nmy name is {CUSTOMER} and I write about case {CASE_ID}. Please give my request "
               "your attention.\nThank you."),
    "log": ("one or two machine log lines made of key=value pairs or bracketed fields (no timestamps, no numbers)",
            "[support inbox] message from {CUSTOMER} about case {CASE_ID}: asks for a review of the request"),
    "form": ("a filled-in web form: a title line and two to four 'Label: value' lines",
             "Request form\nSubmitted by: {CUSTOMER}\nCase number: {CASE_ID}\nCategory: {CAT}"),
    "transcript": ("a transcript of two to four short spoken turns between a support agent and the customer, each "
                   "line starting with 'Agent: ' or 'Caller: '",
                   "Agent: thanks for calling, who am I speaking with?\nCaller: {CUSTOMER}, about case {CASE_ID}."),
    "voicemail": ("a voicemail transcript: one to three spoken sentences from the customer, starting with a label "
                  "such as 'Voicemail from {CUSTOMER}:' or with a greeting",
                  "Voicemail from {CUSTOMER}: hello, I am calling about case {CASE_ID} and my request under your "
                  "policy."),
}
SITUATIONS = ("a polite first message", "a short, plain note", "a message written in a hurry",
              "a formal request to have the case looked at", "a friendly note with a thank-you",
              "a note written by a support agent after a call", "a terse note", "a message with a short greeting",
              "a structured note with labelled parts", "a note that names the case first and the person second",
              "a calm, neutral message", "a message from someone who writes in short sentences")
CUSTOMER_SITUATIONS = tuple(x for x in SITUATIONS if "support agent" not in x and "labelled parts" not in x)
CUSTOMER_VOICED = ("email", "chat", "letter", "voicemail")       # the customer writes or speaks: no agent situations
SKINS_PER_ITEM = 5


def _skin_prompt(register: str) -> str:
    fmt, example = REGISTER_FORMAT[register]
    return COMMON + f"""
TASK: write NARRATIVE TEMPLATES in the register "{register}": {fmt}.
A narrative is a short message or note from or about the customer who raised a case under an invented
customer-service policy. Elsewhere on the page a program prints the policy and the case record; your text adds no
fact of its own and never hints at how the case will be decided.

Placeholders: each item lists the placeholders ("slots") to use and what the program puts in them. Use every listed
placeholder EXACTLY ONCE, spelled exactly as given with its curly braces (e.g. {{CUSTOMER}}); never use any other
placeholder and never write a real value in its place.

Hard rules (a text that breaks one is thrown away):
1. One block of text: no empty line, no leading or trailing spaces; line breaks only where the register needs them.
2. Never put "a" or "an" directly before a placeholder.
3. Outside the placeholders: no digits, number words or ordinals; no dates, times, months or weekdays; no currency
   or percent signs; no web or e-mail addresses; no codes or ids.
4. Outside the placeholders, none of these words (any letter case):
{_word_lists()}
5. No negation at all: {NEGATION_CUES}.
6. Capital letters only at the start of a sentence, a line, a list item or a label; no names of people, companies,
   products, places or teams (the only name is the {{CUSTOMER}} placeholder).
7. Refer to the subject only as the case, the request, my case or my request. Say nothing about what was bought,
   used, booked or damaged; about dates, deadlines, amounts, categories or conditions (except through the
   placeholders); about the policy's rules or versions (never new, old, revised or updated rules); or about any
   result, any money paid back or what the customer hopes to get (asking to have the case looked at is fine).
8. Use each placeholder only in the role its description gives.
9. The texts of one item vary clearly in wording and structure (not one word swapped), and none copies the example.

Example of the register (for format only):
  {json.dumps(example)}
""" + _answer_block("texts")


# ------------------------------------------------------------------------------------------------ Mode F (3.2)
FREEFORM_PROMPT = COMMON + """
TASK: write one short FREE-FORM DOCUMENT per item, in the item's register, from the facts given. The document is the
narrative part of a page: a message or note from or about the customer who raised a case under an invented
customer-service policy. A program prints the policy and the case record elsewhere, so the document adds no fact of
its own and never hints at how the case will be decided.

Hard rules (a document that breaks one is thrown away):
1. Two to four sentences, 25-80 words, one block of text (single line breaks allowed, never an empty line).
2. Write the CUSTOMER's full name exactly as given, letter for letter with its capitals, exactly once, and no other
   personal names, initials or nicknames. No gendered pronouns (he, she, his, her): after the name, use "they" or no
   pronoun.
3. No digits, number words or ordinals; no dates, times, months or weekdays; no words such as today, tomorrow, now,
   soon, later, earlier, yesterday, recently; no codes, case numbers or ids; no web or e-mail addresses; no currency
   or percent signs.
4. No negation at all: """ + NEGATION_CUES + """.
5. Refer to the subject only as the case, the request, my case or my request. Say nothing about what was bought, used,
   booked or damaged; about dates, deadlines, amounts, categories or conditions; about the policy's rules or versions
   (never new, old, revised or updated rules); or about any result, any money paid back or what the customer hopes to
   get (asking to have the case looked at is fine).
6. Capital letters only at the start of a sentence or a line, plus the customer's name.
""" + _answer_block("text")

FREE_REGISTER_FORMAT = {
    "email": "a short e-mail from the customer (a greeting, the message, a sign-off)",
    "letter": "a short formal letter from the customer",
    "chat": "a chat message the customer types to a support agent",
    "memo": "an internal note a support agent writes about the customer's contact",
    "ticket": "the free-text description of a support ticket, written by a support agent",
    "transcript": "a short transcript of a phone call, with lines starting 'Agent:' and 'Caller:'",
    "voicemail": "a voicemail the customer leaves, as spoken",
}
FREE_TRAIN = ("email", "letter", "chat", "memo", "ticket")
FREE_HELD = ("transcript", "voicemail")


# ------------------------------------------------------------------------------------------------ tasks
@dataclass
class Task:
    name: str
    kind: str
    field: str
    batch: chunker.TaskBatch
    outputs: int
    held_out: bool
    pool: str
    meta: dict                      # internal id -> item metadata (orchestrator only; never in the task file)

    @property
    def chunk(self) -> dict:
        assert len(self.batch.chunks) == 1
        return self.batch.chunks[0]

    @property
    def task_id(self) -> str:
        return self.chunk["task_id"]

    def task_file(self, root: Path = ROOT) -> Path:
        return Path(root) / "tasks" / f"{self.task_id}.md"

    def answer_file(self, root: Path = ROOT) -> Path:
        return Path(root) / self.batch.answer_path(self.task_id)

    def text(self, root: Path = ROOT) -> str:
        items = json.dumps(self.chunk["items"], ensure_ascii=False, indent=1)
        return (f"# T24 authoring task {self.task_id}\n\n"
                f"ANSWER FILE (write your whole answer here, and nowhere else, with the Write tool):\n"
                f"{self.answer_file(root)}\n\n"
                f"Task kind: {self.kind}; items: {len(self.chunk['items'])}; outputs expected: {self.outputs}.\n\n"
                f"{self.batch.prompt.rstrip()}\n\n"
                f"ITEMS (JSON; answer every item, keyed by its qid):\n{items}\n")


def _batch(kind: str, name: str, items: list, prompt: str, forbid: tuple) -> chunker.TaskBatch:
    b = chunker.make_batch(kind, FAMILY, items, seed=f"t24-author-{VERSION}-{name}", prompt=prompt,
                           forbid_strings=forbid)
    if len(b.chunks) != 1:
        raise chunker.ChunkError(f"{name}: one chunk per task")
    return b


def build_tasks() -> list:
    tasks = []

    def add(name, kind, field, items, prompt, outputs, held, pool, forbid, meta):
        tasks.append(Task(name, kind, field, _batch(kind, name, items, prompt, forbid), outputs, held, pool, meta))

    # packs: 2 x 40 settings
    for part, settings in (("a", PACK_SETTINGS[:40]), ("b", PACK_SETTINGS[40:80])):
        items, meta = [], {}
        for i, s in enumerate(settings):
            iid = f"t24-{VERSION}-pack-{part}-{i:02d}"
            items.append((iid, {"brief": {"setting": s}}))
            meta[iid] = {"setting": s}
        add(f"pack-{part}", "author_pack", "pack", items, PACK_PROMPT, len(items), False, "packs", FORBID_PACK, meta)
    # clause forms
    lex_plan = (("lex-win", (("t24.win", LEX_STYLES["t24.win"]),)),
                ("lex-special", (("t24.ovc", LEX_STYLES["t24.ovc"]), ("t24.ovd", LEX_STYLES["t24.ovd"]))),
                ("lex-amount", tuple((f"t24.amt.{op}", LEX_STYLES["amt.pos"] + LEX_STYLES["amt.neg"])
                                     for op in P.OPS)),
                ("lex-exc-alt", (("t24.exc", LEX_STYLES["t24.exc"]), ("t24.alt", LEX_STYLES["t24.alt"]))))
    for name, plan in lex_plan:
        items, meta = [], {}
        for sem, styles in plan:
            for i, style in enumerate(styles):
                iid = f"t24-{VERSION}-lex-{sem}-{i}"
                items.append((iid, _lex_item(sem, style)))
                meta[iid] = {"sem": sem, "lex_kind": LEX_KIND[sem], "slots": list(LEX_SLOTS_OF[sem]),
                             "surface": "negative" if "do not qualify" in style else "plain"}
        add(name, "author_lexicon", "forms", items, LEX_PROMPT, FORMS_PER_ITEM * len(items), False,
            "lexicon:" + ("window" if name in ("lex-win", "lex-special") else
                          "comparator" if name == "lex-amount" else "other"), FORBID, meta)
    # question wordings (training) and the held-out set for S5
    for name, plan in WORDING_TASKS:
        items, meta, n = [], {}, 0
        for qf, k in plan:
            for i in range(k):
                iid = f"t24-{VERSION}-word-{qf}-{i:02d}"
                items.append((iid, {"brief": {"meaning": Q_MEANING[qf],
                                              "style": WORDING_STYLES[(i + n) % len(WORDING_STYLES)],
                                              "how_many": WORDINGS_PER_ITEM},
                                    "rules": [f"{WORDINGS_PER_ITEM} wordings with exactly this meaning",
                                              "no placeholders"]}))
                meta[iid] = {"qform": qf, "held_out": False}
            n += k
        add(name, "author_wording", "wordings", items, WORDING_PROMPT, WORDINGS_PER_ITEM * len(items), False,
            "wordings", FORBID_WORDING, meta)
    items, meta = [], {}
    for qf in P.T24Plugin.QFORMS:
        iid = f"t24-{VERSION}-wordheld-{qf}"
        items.append((iid, {"brief": {"meaning": Q_MEANING[qf], "style": HELD_STYLE, "how_many": WORDINGS_PER_ITEM},
                            "rules": [f"{WORDINGS_PER_ITEM} wordings with exactly this meaning", "no placeholders"]}))
        meta[iid] = {"qform": qf, "held_out": True}
    add("word-held", "author_wording", "wordings", items, WORDING_PROMPT, WORDINGS_PER_ITEM * len(items), True,
        "wordings", FORBID_WORDING, meta)
    # Mode T skins: 9 training registers x 8 items, 2 held-out registers x 6 items; 5 skins per item
    for r_i, reg in enumerate(TRAIN_REGISTERS + HELD_REGISTERS):
        held = reg in HELD_REGISTERS
        sets = FIELD_SETS if reg in FIELD_REGISTERS else PROSE_SETS
        sits = CUSTOMER_SITUATIONS if reg in CUSTOMER_VOICED else SITUATIONS
        items, meta = [], {}
        for i in range(6 if held else 8):
            slots = sets[i % len(sets)]
            iid = f"t24-{VERSION}-skin-{reg}-{i:02d}"
            items.append((iid, {
                "brief": f"{sits[(i + 3 * r_i) % len(sits)]}; write {SKINS_PER_ITEM} texts",
                "register": reg, "slots": {s: SKIN_SLOTS[s] for s in slots},
                "rules": ["use each of " + ", ".join("{" + s + "}" for s in slots) + " exactly once",
                          f"{SKINS_PER_ITEM} texts, each clearly distinct from the others"]}))
            meta[iid] = {"register": reg, "slots": list(slots), "held_out": held, "escape": ESCAPE.get(reg, "text")}
        add(f"skin-{reg}", "author_skin", "texts", items, _skin_prompt(reg), SKINS_PER_ITEM * len(items), held,
            "skins", FORBID, meta)
    # Mode F documents
    def free(tag, n, registers, offset, held):
        items, meta = [], {}
        for i in range(n):
            k = offset + i
            reg = registers[k % len(registers)]
            name = P.CUSTOMERS[(k * 7) % len(P.CUSTOMERS)]
            iid = f"t24-{VERSION}-free-{tag}-{i:02d}"
            items.append((iid, {"brief": f"{CUSTOMER_SITUATIONS[(k * 5) % len(CUSTOMER_SITUATIONS)]}; "
                                         f"{FREE_REGISTER_FORMAT[reg]}",
                                "register": reg, "facts": {"CUSTOMER": name},
                                "rules": ["exactly one document", "the name exactly once, verbatim"]}))
            meta[iid] = {"register": reg, "customer": name, "held_out": held}
        add(f"free-{tag}", "author_freeform", "text", items, FREEFORM_PROMPT, n, held, "freeform", FORBID, meta)
    free("a", 50, FREE_TRAIN, 0, False)
    free("b", 50, FREE_TRAIN, 50, False)
    free("held", 24, FREE_HELD, 100, True)
    if len(tasks) > MAX_TASKS:
        raise chunker.ChunkError(f"{len(tasks)} tasks (at most {MAX_TASKS})")
    return tasks


def forbid_of(t: Task) -> tuple:
    return {"author_wording": FORBID_WORDING, "author_pack": FORBID_PACK}.get(t.kind, FORBID)


def check(tasks: list, root: Path = ROOT) -> list:
    """Problems: a forbidden string, an internal id or a never-open path in a task file; > 50 items; no answer path."""
    probs = []
    for t in tasks:
        text = t.text(root)
        low = text.lower()
        for f in forbid_of(t):
            if f and re.search(r"(?<![a-z0-9])" + re.escape(f.lower()) + r"(?![a-z0-9])", low):
                probs.append(f"{t.name}: task text holds forbidden string {f!r}")
        if any(iid in text for iid in t.batch.key.values()):
            probs.append(f"{t.name}: internal id in task text")
        if not 1 <= len(t.chunk["items"]) <= chunker.MAX_ITEMS:
            probs.append(f"{t.name}: {len(t.chunk['items'])} items")
        if str(t.answer_file(root)) not in text:
            probs.append(f"{t.name}: answer path missing")
        for p in (t.task_file(root), t.answer_file(root)):
            if paths.never_open(p):
                probs.append(f"{t.name}: never-open path {p}")
    return probs


def files(tasks: list, root: Path = ROOT) -> tuple:
    """({relative path: text}, manifest) for paths.write_files."""
    out, rows = {}, []
    for t in tasks:
        out.update(t.batch.files())
        text = t.text(root)
        out[str(t.task_file(root).relative_to(root))] = text
        read = {str(t.task_file(root))} | t.batch.allowed(str(root), t.task_id)[0]
        rows.append({"task": t.name, "task_id": t.task_id, "kind": t.kind, "pool": t.pool, "held_out": t.held_out,
                     "answer_field": t.field, "task_file": str(t.task_file(root)),
                     "answer_file": str(t.answer_file(root)), "batch_id": t.batch.batch_id,
                     "prompt_sha": t.batch.prompt_sha, "task_sha256": hashlib.sha256(text.encode()).hexdigest(),
                     "n_items": len(t.chunk["items"]), "outputs_expected": t.outputs,
                     "allowed_read": sorted(read), "allowed_write": [str(t.answer_file(root))], "items": t.meta})
    manifest = {"family": FAMILY, "version": VERSION, "g0_sha256": P.G0_SHA256_AUTHORED,
                "g0_ambiguity_pass": P.T24Plugin.G0_AMBIGUITY_PASS["task_id"], "n_tasks": len(tasks),
                "outputs_expected": sum(t.outputs for t in tasks), "tasks": rows}
    out["TASKS.json"] = json.dumps(manifest, ensure_ascii=False, indent=1) + "\n"
    out["answers/README.txt"] = ("Haiku answer files: one <task_id>.json per authoring task (see ../TASKS.json). "
                                 "Written only by the task agents.\n")
    return out, manifest


# ------------------------------------------------------------------------------------------------ lint-stage helpers
def load(root: Path = ROOT) -> tuple:
    """Read TASKS.json, the keys and every answer file present. Returns ({pool: [piece]}, problems); a piece is
    {"iid", "task_id", "text" (or "pack"), **item metadata}. Haiku answers only flag: nothing here sets a label."""
    root = Path(root)
    manifest = json.loads((root / "TASKS.json").read_text(encoding="utf-8"))
    pools: dict = {}
    probs = []
    for row in manifest["tasks"]:
        ans_path = Path(row["answer_file"])
        if not ans_path.exists():
            probs.append(f"{row['task_id']}: no answer file")
            continue
        key = json.loads((root / "key" / f"{row['batch_id']}.json").read_text(encoding="utf-8"))["key"]
        try:
            raw = json.loads(ans_path.read_text(encoding="utf-8"))
        except ValueError as e:
            probs.append(f"{row['task_id']}: answer is not JSON ({e})")
            continue
        if not isinstance(raw, list):
            probs.append(f"{row['task_id']}: answer is not a JSON array")
            continue
        seen = set()
        for a in raw:
            qid = a.get("qid") if isinstance(a, dict) else None
            if qid not in key or qid in seen:
                probs.append(f"{row['task_id']}: unknown or repeated qid {qid!r}")
                continue
            seen.add(qid)
            iid = key[qid]
            meta = dict(row["items"][iid])
            val = a.get(row["answer_field"])
            outs = [val] if row["answer_field"] in ("pack", "text") else (val if isinstance(val, list) else [])
            for j, v in enumerate(outs):
                piece = {"iid": f"{iid}#{j}", "task_id": row["task_id"], "prompt_sha": row["prompt_sha"],
                         "held_out": row["held_out"], **meta}
                piece["pack" if row["answer_field"] == "pack" else "text"] = v
                pools.setdefault(row["pool"], []).append(piece)
        missing = set(key) - seen
        if missing:
            probs.append(f"{row['task_id']}: {len(missing)} item(s) unanswered")
    return pools, probs


def check_pack(d) -> tuple:
    """(Domain or None, problems) for one Haiku pack object (R2; plugin.check_domain)."""
    need = ("title", "prefix", "date_fields", "money_field", "categories", "conditions", "outcomes")
    if not isinstance(d, dict) or set(d) != set(need):
        return None, [f"pack fields must be exactly {need}"]
    try:
        dom = P.Domain(key=d["prefix"].lower(), title=d["title"], prefix=d["prefix"], dates=tuple(d["date_fields"]),
                       amount=d["money_field"], cats=tuple(d["categories"]), conds=tuple(d["conditions"]),
                       outcomes=tuple(d["outcomes"]))
    except (TypeError, AttributeError) as e:
        return None, [f"pack shape: {e}"]
    probs = P.check_domain(dom)
    return (None if probs else dom), probs


def check_skin(text: str, register: str, slots: list, *, held_out: bool = False, skin_id: str = "SK-PROBE") -> list:
    """G-SL lint_template (role skin) plus the T24 skin rules (no blank line, CUSTOMER present, declared slots only)."""
    if not isinstance(text, str) or not text.strip():
        return ["empty text"]
    if "\n\n" in text or text != text.strip():
        return ["blank line or outer whitespace"]
    try:
        sk = K.make_skin(skin_id, FAMILY, text, {s: P_SLOT_KIND[s] for s in slots}, register=register,
                         escape=ESCAPE.get(register, "text"), held_out=held_out)
    except Exception as e:   # noqa: BLE001  (a malformed template is a lint failure, not a crash)
        return [f"make_skin: {e}"]
    v = gsl.lint_template(sk, label_words=P.T24Plugin.LABEL_WORDS, exceptions=P.T24Plugin.GSL_EXCEPTIONS,
                          name_allow=P.T24Plugin.NAME_ALLOW)
    return [f"{x.rule}: {x.detail}" for x in v]


P_SLOT_KIND = {"CUSTOMER": "name", "CASE_ID": "id", "CAT": "category", "COND": "category", "AMOUNT": "cents",
               "D1": "date", "D2": "date", "REQ": "date"}


def check_freeform(text: str, customer: str) -> list:
    """G-SL lint_freeform for one Mode F document (the customer name is the only fact)."""
    if not isinstance(text, str) or not text.strip() or "\n\n" in text:
        return ["empty text or blank line"]
    return [f"{x.rule}: {x.detail}" for x in gsl.lint_freeform(text, {"CUSTOMER": customer},
                                                                label_words=P.T24Plugin.LABEL_WORDS)]


NEG_TARGET = {"yn_changes": (0, 0), "yn_same": (0, 0), "ch_v2": (0, 0), "yn_not_change": (1, 1),
              "yn_fail_change": (1, 0), "yn_dneg": (2, 2)}


def check_wording(text: str, qform: str) -> list:
    """R16 negation counts, the question shape, the wording-role G-SL lint and the polarity rule P1-P3 (c2_kit.polarity;
    a wording must read with its form's declared polarity)."""
    if not isinstance(text, str) or not text.endswith("?") or "\n" in text or K.placeholders(text):
        return ["one line, ends with '?', no placeholder"]
    probs = []
    c = negcount.count(text)
    if (c.k_all, c.k_syn) != NEG_TARGET[qform]:
        probs.append(f"negcount (k_all, k_syn) = {(c.k_all, c.k_syn)}, want {NEG_TARGET[qform]}")
    if re.match(r"(?i)(isn't|doesn't|don't|aren't|wasn't)\b", text):
        probs.append("leading negative question")
    if "outcome" not in text.lower():
        probs.append("does not name the outcome (H20)")
    if _bad(text, OUTCOME_VOCAB):
        probs.append("names an outcome word")
    sk = K.make_skin("W-PROBE", FAMILY, text, {}, kind="wording", register="question", qform=qform)
    probs += [f"{x.rule}: {x.detail}" for x in gsl.lint_template(sk, label_words=P.T24Plugin.LABEL_WORDS)]
    probs += [f"polarity {x}" for x in POL.form_problems(P.T24Plugin, qform, text)]     # kit item 3: P1-P3
    if text in P.QUARANTINED_WORDINGS:
        probs.append(f"quarantined wording: {P.QUARANTINED_WORDINGS[text]}")
    return probs


def check_form(text: str, sem: str) -> list:
    """Clause-form shape (G0 3.1) and the lexicon unit test against the stand-in forms of every T24 meaning."""
    if not isinstance(text, str) or text != text.strip() or "\n" in text or not text[:1].isupper():
        return ["one trimmed line starting with a capital letter"]
    if text.endswith((".", ";", ":", ",")) or text.startswith("{"):
        return ["no end punctuation; never starts with a slot"]
    want = set(LEX_SLOTS_OF[sem])
    got = [p.name for p in K.placeholders(text)]
    if sorted(got) != sorted(want):
        return [f"slots {sorted(got)}, want {sorted(want)} each once"]
    if re.search(r"\d", K.PH_RE.sub(" ", text)) or _bad(text, FORBID):
        return ["digit or label word outside the slots"]
    reg = FX.lexicon(admit=False)
    same = [f for f in reg.forms.values() if f.text == text]
    if same:                                   # one of the stand-in forms: already unit-tested
        return [] if same[0].sem_id == sem else [f"text is a stand-in form of {same[0].sem_id}"]
    slots = FX.AMT_SLOTS if sem.startswith("t24.amt.") else FX.SLOT_KINDS[sem]
    try:
        f = reg.add(text, sem, slots=slots, family=FAMILY)
    except Exception as e:   # noqa: BLE001  (a malformed form is a lint failure, not a crash)
        return [f"lexicon.add: {e}"]
    ok = reg.unit_test(f.form_id)
    return [] if ok else ([f"unit test: {x}" for x in f.unit_problems] or ["unit test failed"])


def main() -> int:
    tasks = build_tasks()
    probs = check(tasks)
    if probs:
        print("\n".join(probs))
        return 1
    out, manifest = files(tasks)
    paths.write_files(ROOT, out)              # refuses before A38 and on never-open paths
    for r in manifest["tasks"]:
        print(f"{r['kind']:16s} {r['task']:18s} items {r['n_items']:3d} outputs {r['outputs_expected']:4d} "
              f"{r['task_file']}")
    print(f"{manifest['n_tasks']} tasks, {manifest['outputs_expected']} outputs expected; manifest "
          f"{ROOT / 'TASKS.json'}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
