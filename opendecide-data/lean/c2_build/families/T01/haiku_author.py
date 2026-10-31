"""families/T01/haiku_author.py: the T01 Haiku AUTHORING tasks (G0_SPEC.md section 7, v2) and the loaders that turn
their answers into pool candidates. Written after A38; Haiku never sees a question, an option or a gold while it writes
skins, documents or packs, and it never sets a label.

  build_batches()   {name: (TaskBatch, plan)}: gold-free chunks via c2_kit.chunker.make_batch. Pack, skin and Mode F
                    batches forbid T01.LABEL_WORDS and every fixture question text; wording and lexicon batches forbid
                    the fixture question texts (their meaning words are their content)
  write_tasks()     prompts / chunks / key / manifest (TaskBatch.files) + plan/<batch>.json (orchestrator side) + one
                    self-contained task file per chunk (tasks/<task_id>.md, naming its exact answer file) + TASKS.json,
                    all through paths.write_files / write_json under haiku/author/ (refuses before A38)
  load_*            answer objects -> pool candidates + per-item problems: T01 shape checks, G-SL lint, the G0 section 7
                    T01 word lists (H38), exact negcount per wording form, slot round trips. G-LEX admission
                    (2/2; 3/3 for window rules), G3-H and G13 run in the later stages.

A Haiku agent reads ONLY its task file and writes ONLY the answer file it names (TASKS.json lists both for
audit.audit_jsonl). Run (from lean/):  ../.venv/bin/python c2_build/families/T01/haiku_author.py plan | write
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
from families.T01 import fixtures as FX  # noqa: E402  (sem meanings + the fixture question texts to forbid)
from families.T01 import plugin as P  # noqa: E402
import negcount  # noqa: E402  (c_src/common, put on sys.path by c2_kit.paths)

FAMILY = "T01"
ROOT = HERE / "haiku" / "author"
SEED = "t01-author-v1"
QSTRINGS = tuple(t for _, _, t, _ in FX.WORDINGS)
FORBID_ALL = tuple(P.T01.LABEL_WORDS) + QSTRINGS
TRAIN_REGISTERS = ("memo", "email", "chat", "ticket", "json", "yaml", "log", "transcript")
HELD_REGISTERS = tuple(P.T01.HELD_OUT_REGISTERS)                       # faq, letter (S5 / mixdev only)
N_SKIN_TRAIN, N_SKIN_HELD = 56, 28
N_PACKS, N_PACKS_HELD = 80, 16                                         # 56 training cards + 16 S5 cards
N_FREEFORM = 120
FREEFORM_REGISTERS = ("memo", "email", "chat", "ticket", "transcript")
N_WINDOW, N_CMP = 14, 12
NARR = {"PERSON": "name", "REF": "id", "TOPIC": "name"}
SLOT_KIND = {"PERSON": "name", "REF": "id", "REF_DATE": "date", "ACTION": "name", "PERIL": "name", "DAY": "date"}

# ------------------------------------------------------------------------------------------------ question forms
BASE_YN = ("yn_over", "yn_timely", "yn_covered", "yn_quotes", "yn_cash_report", "yn_on_time")
CHOICE = ("ch_days", "ch_deadline", "ch_first_day", "ch_total", "ch_cash_which", "ch_due", "ch_receipt_day")
COMPLEMENT = ("yn_within", "yn_not_over", "yn_late", "yn_fail_time", "yn_not_timely", "yn_in_waiting",
              "yn_not_covered", "yn_quotes_without", "yn_no_quotes", "yn_cash_without", "yn_cash_no_report",
              "yn_late_cut", "yn_not_on_time")
WORDING_N = {**{q: 12 for q in BASE_YN}, **{q: 14 for q in CHOICE}, **{q: 9 for q in COMPLEMENT}}   # 287 items
IMPLICIT = ("yn_fail_time", "yn_quotes_without", "yn_cash_without")
SYNTACTIC = ("yn_not_over", "yn_not_timely", "yn_not_covered", "yn_no_quotes", "yn_cash_no_report", "yn_not_on_time")
NEG_EXACT = {q: ((1, 0) if q in IMPLICIT else (1, 1) if q in SYNTACTIC else (0, 0)) for q in WORDING_N}
KIND_NOUN = {"rolling": "record {REF} or file {REF}", "anchor": "case {REF}", "waiting": "policy {REF}",
             "purchase": "log {REF} or request {REF}", "cash": "ledger {REF}", "addon": "notice {REF}",
             "cutoff": "notice {REF}"}
RULE_NAME = {"rolling": "the stay rule", "anchor": "the filing rule", "waiting": "the cover rule",
             "purchase": "the purchase rule", "cash": "the cash rule", "addon": "the response rule",
             "cutoff": "the receipt rule"}
SLOT_SETS = {"rolling": (("PERSON", "REF_DATE"), ("PERSON",), ("REF",), ("REF", "REF_DATE"), ("PERSON", "REF")),
             "anchor": (("ACTION", "REF"), ("PERSON", "ACTION"), ("ACTION",), ("PERSON", "ACTION", "REF")),
             "waiting": (("PERIL", "REF"), ("PERIL",), ("PERSON", "PERIL"), ("REF",)),
             "purchase": (("REF",), ("PERSON",), ("PERSON", "REF")),
             "cash": (("DAY", "REF"), ("DAY",), ("PERSON", "DAY"), ("REF",)),
             "addon": (("REF",), ("PERSON",), ("PERSON", "REF")),
             "cutoff": (("REF",), ("PERSON",), ("PERSON", "REF"))}
NO_NEG = "Use NO negation word at all."
ONE_NOT = ("Use exactly ONE negation, 'not' or n't on the main verb (for example 'is it true that ... not ...'); no "
           "other negation word.")
# qform -> (meaning brief, [form rules]); the meanings follow G0 v2 section 8 (H8, H11, H20-H22, H32-H37)
WORDING_BRIEF = {
    "yn_over": ("A yes/no question: is the person over the stay limit, that is, are more days present inside the "
                "checked window (the window that ends on the reference date) than the limit? Yes only when over.",
                [NO_NEG]),
    "yn_within": ("A yes/no question: is the person within the stay limit, that is, are the days present inside the "
                  "checked window at most the limit (exactly the limit still counts as within)? Yes when within.",
                  [NO_NEG, "Say 'within the stay limit' or 'inside the stay limit'."]),
    "yn_not_over": ("A yes/no question that is the exact opposite of 'is the person over the stay limit?': yes when "
                    "the person is NOT over the limit.", [ONE_NOT]),
    "ch_days": ("A multiple-choice question (the options, shown separately, are day counts): how many days present "
                "fall inside the checked window, the window that ends on the reference date? Ask for the days present "
                "inside that window, never the days above the limit or the full length of the stays.", [NO_NEG]),
    "yn_timely": ("A yes/no question: was the document filed in time, that is, on or before the final day of the "
                  "filing period? Yes only when in time.", [NO_NEG]),
    "yn_late": ("A yes/no question: was the document filed late, that is, after the final day of the filing period? "
                "Yes only when late.", [NO_NEG, "Use 'late', 'too late' or 'after the deadline'."]),
    "yn_fail_time": ("A yes/no question: did the person fail to file the document in time? The record always shows "
                     "a filing; yes when that filing came after the final day.",
                     ["Use exactly ONE negation: 'fail to' or 'failed to', together with 'in time' or 'by the "
                      "deadline'; no other negation word. Ask about timing, never about whether a filing exists."]),
    "yn_not_timely": ("A yes/no question that is the exact opposite of 'was the document filed in time?': yes when "
                      "it was NOT filed in time.", [ONE_NOT]),
    "ch_deadline": ("A multiple-choice question (the options, shown separately, are dates): what is the last date on "
                    "which the document can still be filed in time? Ask for the last day still in time, never the "
                    "first late day.", [NO_NEG]),
    "yn_covered": ("A yes/no question: is the loss covered under the cover rule? Yes only when covered.", [NO_NEG]),
    "yn_in_waiting": ("A yes/no question: did the loss happen during the waiting period (on or before its final "
                      "day)? Yes when it falls inside the waiting period.",
                      [NO_NEG, "Say 'during', 'within' or 'inside' the waiting period."]),
    "yn_not_covered": ("A yes/no question that is the exact opposite of 'is the loss covered?': yes when the loss is "
                       "NOT covered.", [ONE_NOT]),
    "ch_first_day": ("A multiple-choice question (the options, shown separately, are dates): what is the first date "
                     "on which a loss of this kind would be covered? Ask for the first covered date, never the last "
                     "waiting day or the start date.", [NO_NEG]),
    "yn_quotes": ("A yes/no question: does the purchase request need written quotes under the purchase rule? Yes only "
                  "when quotes are needed.", [NO_NEG]),
    "yn_quotes_without": ("A yes/no question: does the purchase rule let the request go ahead without written quotes? "
                          "Yes when the rule does not call for quotes. Ask what the rule requires, never whether "
                          "quotes were in fact collected.",
                          ["Use exactly ONE negation: the word 'without'; no other negation word."]),
    "yn_no_quotes": ("A yes/no question that is the exact opposite of 'does the request need written quotes?': yes "
                     "when written quotes are NOT needed.", [ONE_NOT]),
    "ch_total": ("A multiple-choice question (the options, shown separately, are amounts): what total does the "
                 "purchase rule compare with its threshold for this request? Make plain that the new request is part "
                 "of that total.", [NO_NEG]),
    "yn_cash_report": ("A yes/no question: is a cash report required for the day under review? Yes only when a "
                       "report is required.", [NO_NEG]),
    "yn_cash_without": ("A yes/no question: does the cash rule let the day under review close without a cash report? "
                        "Yes when the rule calls for no report. Ask what the rule requires, never whether a report "
                        "was in fact filed.",
                        ["Use exactly ONE negation: the word 'without'; no other negation word."]),
    "yn_cash_no_report": ("A yes/no question that is the exact opposite of 'is a cash report required for the day?': "
                          "yes when NO report is required.",
                          ["Use exactly ONE negation, 'no' or 'not' (for example 'is it true that no cash report "
                           "...'); no other negation word."]),
    "ch_cash_which": ("A multiple-choice question (the options, shown separately, name the deposit total, the "
                      "withdrawal total, both totals or neither total): which of the day's totals call for a cash "
                      "report?", [NO_NEG, "Refer to the day's totals."]),
    "ch_due": ("A multiple-choice question (the options, shown separately, are dates): on which date is the response "
               "to the notice due under the response rule? Ask for the due date itself.", [NO_NEG]),
    "yn_on_time": ("A yes/no question: was the response to the notice on time under the receipt rule? Yes only when "
                   "on time.", [NO_NEG]),
    "yn_late_cut": ("A yes/no question: was the response to the notice late under the receipt rule, that is, counted "
                    "as received after the due date? Yes only when late.",
                    [NO_NEG, "Use 'late' or 'after the due date'; never mention a clock time or the cutoff."]),
    "yn_not_on_time": ("A yes/no question that is the exact opposite of 'was the response on time?': yes when it was "
                       "NOT on time.", [ONE_NOT]),
    "ch_receipt_day": ("A multiple-choice question (the options, shown separately, are dates): on which date does the "
                       "office count the response as received under the receipt rule? Ask for that date, never the "
                       "date it was sent.", [NO_NEG]),
}
STYLES = ("a plain question with no opening phrase", "open with 'Under the card's rule,'",
          "open with 'According to the rule card,'", "open with 'Going by the record,'",
          "a plain question that ends with 'under {RULE}?'", "a plain question that names {RULE} in the middle",
          "open with 'Based on the card and the record,'")

# ------------------------------------------------------------------------------------------------ prompts
PACK_PROMPT = """You invent "packs": small sets of made-up names for one everyday setting. A program later builds \
reading puzzles from your packs (stay records, filing cases, insurance policies, purchase logs, cash ledgers and \
replies to official notices); you never see the puzzles. Each item gives a setting and a name style. Write ONE pack \
per item.

A pack is a JSON object with exactly these keys:
- "people": 6 different people's names, each "First Last" (two words, letters only, a capital first letter on each \
word; a hyphen inside a surname is fine), in the item's name style. Plausible but invented; never a famous or real \
public person.
- "topics": an object with exactly the keys "rolling", "anchor", "waiting", "purchase", "cash" and "notice". Each \
value is a short lower-case noun phrase of 2-4 words naming what a file is about, fitting the setting: rolling = a \
count of days someone spent in a place (like "visa stay count"); anchor = a document someone files against a \
deadline (like "appeal deadline"); waiting = an insurance matter (like "storm damage claim"); purchase = a request \
to buy something (like "supplier order"); cash = a review of a cash ledger (like "teller ledger review"); notice = a \
reply to an official notice (like "notice reply"). Do not copy the examples.
- "filing": an object {"action": ..., "event_a": ..., "event_b": ...}. action = a lower-case noun of 1-3 words for a \
document a person files (an appeal, a claim, an objection ...); event_a and event_b = two different lower-case \
labels of 2-4 words for dated events that can start the filing period, each ending with the word "date" (like \
"decision date", "delivery date"). Neither label may contain the other.
- "perils": 3 different lower-case kinds of insured loss, 1-3 words each (like "hail damage", "theft").
- "vendors": 3 different invented supplier names, 2-3 words each, every word capitalised, letters and spaces only \
(like "Brightwell Supply"); never a real company, brand or product.

Word rules for every value (a program rejects a pack that breaks one):
1. No digits, no number words or ordinals, no dates, months or weekdays, no currency or percent signs.
2. No negation of any kind (not, no, non, never, without, or un- / in- words such as "unpaid" or "invalid").
3. No status or outcome words (approved, denied, rejected, pending, paid, refunded, expired, valid, settled, \
granted, waived), and no words about deadlines being met or missed.
4. Values inside one pack are all different, and no value contains another value of the pack.
5. Plain English letters, spaces, hyphens and apostrophes only.

Answer: a JSON list with one object per item: {"qid": "<the item's qid>", "pack": {...}}. Valid JSON only. Every \
pack must differ from every other pack you write: no repeated names, topics, labels, perils or vendors."""

SKIN_PROMPT = """You write short "narrative skins": the scene-setting text placed above a record in a reading \
puzzle. The record may be a stay record, a filing case, an insurance policy, a purchase log, a cash ledger or an \
official notice. A program fills in the facts later; you never see the record, the puzzle, its question or its \
outcome. Write ONE skin per item, in the item's register and tone, following the item's rules.

Every skin uses the three placeholders {PERSON}, {REF} and {TOPIC}, written exactly like that (curly braces, capital \
letters), each EXACTLY ONCE:
- {PERSON} is the person the file is about, who also sent it in (a full name, filled in later);
- {REF} is the file's reference code (a short code, filled in later);
- {TOPIC} is what the file is about (a short lower-case phrase, filled in later). Write it as "the {TOPIC}", or as \
{a|TOPIC} where the program puts "a" or "an"; never write "a {TOPIC}" or "an {TOPIC}".
Write no other placeholder and no name of any person, company or place.

The skin only says who sent which file about what, to whom: use plain roles such as "the desk", "the clerk" or "the \
review team". It must fit ANY of the six kinds of record, so never mention travel, stays, insurance, claims, \
purchases, orders, money, cash, ledgers, notices, courts, filings, losses or offices, and say nothing about rules, \
policies, limits, periods, deadlines, dates, days, clocks, reports, quotes or any outcome.

Hard word rules (a program rejects any skin that breaks one):
1. No digits, no number words or ordinals (one, two, first, second, half, single, double, twice, dozen ...), no \
dates, times, months or weekdays, no currency or percent signs, no e-mail or web addresses.
2. No time words: today, tonight, tomorrow, yesterday, now, soon, already, yet, recently, currently, next, last, past, \
earlier, later, immediately, morning, afternoon, evening, night, week, weekend, weekday, daily, weekly, monthly, \
overdue, due, deadline, period, window, cutoff, calendar, business day, working day.
3. No quantity or quantifier words: all, every, each, some, any, none, no, both, either, neither, only, always, \
never, often, usually, several, few, many, much, more, most, less, least, extra, another, whole, total, various, \
limit.
4. No modal or obligation words: must, may, might, can, could, should, shall, will, would, need, needs, needed, able, \
have to, has to, required, optional, allowed, permitted.
5. No hedges: maybe, perhaps, probably, likely, seems, appears, apparently, think, believe, guess, assume, roughly, \
nearly, almost.
6. No status or outcome words: approved, denied, rejected, accepted, confirmed, granted, pending, completed, done, \
finished, failed, paid, valid, invalid, ok, okay, open, closed, settled, received, reported, eligible, entitled, \
expired, missed, met.
7. No logic words: if, unless, except, otherwise, instead, regardless, provided.
8. No negation of any kind: not, n't (don't, isn't ...), no, never, nothing, nobody, without, cannot, lack, fail, \
hardly.
9. No question and no question mark.
10. No capital letter except at the start of a sentence, of a line, of a list item or right after a colon (write "the \
review desk", never "the Review Desk"; no acronyms).

Answer: a JSON list with one object per item: {"qid": "<the item's qid>", "text": "<the skin>"}. Use \\n for line \
breaks inside the text. Every skin must differ from every other skin you write."""

FREEFORM_PROMPT = """You write short free-form notes that sit above a record in a reading puzzle (the record may be a \
stay record, a filing case, an insurance policy, a purchase log, a cash ledger or an official notice). Each item \
gives a register, a brief and three facts: PERSON (a full name), REF (a file reference code) and TOPIC (what the file \
is about). Write ONE note per item.

Rules (a program rejects any note that breaks one):
1. Write PERSON, REF and TOPIC exactly as given (same spelling, capitals, hyphens and digits), each exactly once. \
Write TOPIC right after the word "the" (for example "about the <TOPIC>"). Write no other name of a person, company, \
product or place.
2. The note only says who sent which file about what, to whom (plain roles: the desk, the clerk, the review team). \
Keep it neutral so that it fits any of the six kinds of record: beyond the TOPIC words, never mention travel, stays, \
insurance, claims, purchases, money, cash, ledgers, courts, notices, filings or offices.
3. Say nothing about rules, policies, limits, periods, deadlines, due dates, cutoffs, days, dates, clocks, amounts, \
reports, quotes or any outcome; never say what anyone may, can, must, should or will do.
4. Outside the three facts: no digits, number words or ordinals, no dates, times, months or weekdays, no currency or \
percent signs, no codes that mix letters and digits, no e-mail or web addresses.
5. No negation of any kind (not, n't, no, never, nothing, nobody, none, without, cannot, lack, fail, hardly, few, \
unless, except, other than). No question and no question mark.
6. Plain, natural English in the item's register and length.

Answer: a JSON list with one object per item: {"qid": "<the item's qid>", "text": "<the note>"}. Use \\n for line \
breaks inside the text. Every note must differ from every other note you write."""

WORDING_PROMPT = """You write questions for a reading test. Every test item shows a short rule card and a record (a \
stay record, a filing case, an insurance policy, a purchase log, a cash ledger or an official notice), then asks ONE \
question about them. You see none of the test items. Each item below gives the exact meaning a question must have, \
the placeholders it must use and its construction rules. Write ONE question per item with exactly that meaning.

General rules:
1. One sentence ending with "?", 7-28 words, plain English.
2. Use exactly the placeholders the item lists, each exactly once, written exactly like that (curly braces, capital \
letters), and no other placeholder. {PERSON} is the person named in the record; {REF} is the record's reference code; \
{REF_DATE} is the reference date of a stay record; {ACTION} is the kind of document filed, a lower-case noun such as \
"appeal" (write "the {ACTION}"); {PERIL} is the kind of loss, a lower-case phrase such as "storm damage" (write "the \
{PERIL} loss" or "this {PERIL} loss"); {DAY} is the day under review in a cash ledger. {PERSON}, {REF}, {REF_DATE} \
and {DAY} take no article.
3. No digits, number words or ordinals, no dates, no names, no capital letter except the first letter.
4. No time words (today, now, currently, recently, this week, soon, yet, already) and no day-type words (weekday, \
weekend, working day, business day).
5. Follow the item's negation rule exactly. Negation words are: not, n't, no, none, nobody, nothing, nowhere, never, \
neither, nor, cannot; also without, fail to, lack, unless, except, other than, few, hardly, deny, refuse.
6. Ask about the record under the card's rule; never ask whether some answer or option is correct, and never list \
options.
7. Follow the item's style hint for the opening.

Answer: a JSON list with one object per item: {"qid": "<the item's qid>", "text": "<the question>"}. Every \
question must differ from every other question you write."""

WINDOW_PROMPT = """You write paraphrases of one clause of a rule card. A program prints each clause inside a fixed \
sentence (the item shows it, with <clause> where your text goes) and fills each placeholder with a number of days. \
Each item gives the exact meaning. Write ONE clause per item with exactly that meaning, in your own words.

Rules:
1. One clause, lower-case first letter, no final period, no line break, 4-22 words.
2. Use exactly the placeholders the item lists, each exactly once, written exactly as shown (for example {N} or \
{M:adj}); no digits, number words or other numbers.
3. No negation word (not, no, never, none, nothing, without, unless, except, cannot), no "business", "working", \
"week" or "calendar" words, no hedges.
4. Add no condition, exception or example of your own; say exactly the meaning given.
5. The clause must read as correct English inside the item's sentence.

Answer: a JSON list with one object per item: {"qid": "<the item's qid>", "text": "<the clause>"}. Every clause \
must differ from every other clause you write and from the example in the item."""

CMP_PROMPT = """You write short comparison phrases about a sum of money. A program prints each phrase on a card as \
"If that total is <your phrase>, ..." or "if its deposit total or its withdrawal total is <your phrase>", with {X} \
replaced by an amount such as $5,000.00. Each item gives the exact meaning. Write ONE phrase per item, in your own \
words.

Rules:
1. Contains the placeholder {X} exactly once, written exactly like that; no other number, amount or placeholder.
2. Reads as correct English right after "is ", lower case (unless it starts with {X}), no final period, 1-7 words \
besides {X}.
3. Makes it plain whether an amount exactly equal to {X} counts: for "strictly greater" say "more than" or "greater \
than" (strictly may be added); for "greater or equal" say it with "at least", "or more", "or above", "or greater" or \
"equal to or more than".
4. Never use the words over, exceeds, exceeding, excess, beyond, under, below, within, up to, between, and, not, no; \
"above" only inside "or above".

Answer: a JSON list with one object per item: {"qid": "<the item's qid>", "text": "<the phrase>"}. Every phrase \
must differ from every other phrase you write and from the example in the item."""

ANSWER_FORMAT = {
    "author_pack": '[{"qid": "q...", "pack": {"people": [...6], "topics": {"rolling": ..., "anchor": ..., "waiting": '
                   '..., "purchase": ..., "cash": ..., "notice": ...}, "filing": {"action": ..., "event_a": ..., '
                   '"event_b": ...}, "perils": [...3], "vendors": [...3]}}, ...]',
    "author_skin": '[{"qid": "q...", "text": "..."}, ...]',
    "author_freeform": '[{"qid": "q...", "text": "..."}, ...]',
    "author_wording": '[{"qid": "q...", "text": "...?"}, ...]',
    "author_lexicon": '[{"qid": "q...", "text": "..."}, ...]',
}

# ------------------------------------------------------------------------------------------------ item content
SETTINGS = ("a mountain village with seasonal workers", "a university exchange office", "a coastal fishing town",
            "a regional bus company", "a city housing department", "a family-run vineyard", "a hospital volunteer "
            "programme", "a small-town library", "a ferry port", "a farmers' market association", "a ski resort",
            "a music festival", "a research station", "a community garden network", "a city bike repair co-op",
            "a theatre touring company", "a dental clinic group", "a youth football league", "a craft brewery",
            "a seaside hotel", "an island tourist board", "a translation bureau", "a bakery chain", "a print shop",
            "a veterinary practice", "a regional orchestra", "a construction cooperative", "a language school",
            "a film archive", "an organic dairy", "a marina", "a ceramics studio", "a cycling club",
            "a city zoo", "a charity shop network", "a railway museum", "a plant nursery", "a science fair",
            "a riverside campsite", "a winter market")
NAME_STYLES = ("a broad international mix", "Nordic and Baltic names", "West African and French names",
               "South Asian and British names", "Latin American and Iberian names", "East Asian and Pacific names",
               "Central European and Balkan names", "Middle Eastern and North African names")
TONES = ("neutral and routine", "brisk and busy", "polite and formal", "friendly and chatty")
ROLES = ("the desk", "the review team", "the duty clerk", "the help desk", "the intake team", "the admin team",
         "the records clerk", "the front desk", "the case team", "the service desk")
REGISTER_RULES = {
    "memo": ["A short internal memo of 2-4 sentences; it may open with a label such as 'Desk memo:'."],
    "email": ["A short e-mail: a 'Subject:' line, a greeting line, 1-3 sentences and a sign-off line that holds no "
              "name."],
    "chat": ["A chat excerpt of 2-4 lines, each 'speaker: message'. The speakers are lower-case roles such as 'desk' "
             "or 'clerk', or {PERSON}; {PERSON} still appears exactly once in the whole skin."],
    "ticket": ["A ticket of 2-4 lines in 'field: value' or 'field | value' style (such as a title line and a "
               "requester line), plus at most one short sentence."],
    "json": ['One JSON object with 3-5 keys whose values are strings or a bare placeholder, for example {"file": '
             '{REF}, "sent_by": {PERSON}, "subject": {TOPIC}, "channel": "intake"}. Write each placeholder bare as a '
             'value (no quotes around it) or inside a quoted string.',
             "Context keys only (file, sent_by, subject, channel, team, note ...); never keys about rules, dates, "
             "amounts, limits or outcomes."],
    "yaml": ["3-5 lines of 'key: value' YAML with plain values, for example 'sent_by: {PERSON}'. Write the "
             "placeholders bare as values.",
             "Context keys only (file, sent_by, subject, channel, team, note ...); never keys about rules, dates, "
             "amounts, limits or outcomes."],
    "log": ["1-3 log lines in key=value style or '[tag] message' style; words joined by underscores are fine; no "
            "digits and no timestamps."],
    "transcript": ["A call or desk transcript of 2-4 lines 'speaker: message' between {PERSON} and a lower-case role "
                   "('desk', 'clerk', 'agent'); {PERSON} appears exactly once, as a speaker label or in a line."],
    "faq": ["An FAQ-page entry: a short title line, then 1-2 sentences saying who sent in which file about what. Write "
            "no question and no question mark."],
    "letter": ["A short formal letter: a greeting line to a lower-case role (such as 'Dear desk,'), 1-3 sentences, a "
               "closing line, and {PERSON} as the signature line."],
}
REGISTER_DESC = {"memo": "an internal memo", "email": "a short e-mail", "chat": "a team chat excerpt",
                 "ticket": "a help-desk ticket", "json": "a JSON intake record", "yaml": "a YAML intake record",
                 "log": "an intake log excerpt", "transcript": "a desk transcript", "faq": "an FAQ-page entry",
                 "letter": "a short formal letter"}
FREEFORM_RULES = {
    "memo": ["An internal memo of 2-5 sentences."],
    "email": ["A short e-mail: a greeting line, 2-4 sentences and a sign-off line that holds no name."],
    "chat": ["A chat thread of 2-4 short lines 'speaker: message'; the speakers are lower-case roles or PERSON."],
    "ticket": ["A ticket: 2-3 short 'field: value' lines and 1-2 sentences."],
    "transcript": ["A desk transcript of 2-4 lines 'speaker: message' between PERSON and a lower-case role."],
}
FF_PEOPLE = ("Ines Moreau", "Marek Kowalski", "Yara Haddad", "Tobias Lindqvist", "Leila Okoro", "Oskar Brennan",
             "Priya Castillo", "Joaquin Varga", "Hana Nakamura", "Felix Achterberg", "Amara Fontaine",
             "Dmitri Mensah", "Sofia Petrov", "Kwame Quintero", "Elif Sandoval", "Rowan Takeda", "Mei Whitfield",
             "Anders Yilmaz", "Zainab Abernathy", "Lucas Delacroix", "Ingrid Moreau", "Tariq Kowalski",
             "Camila Haddad", "Henrik Okoro")
FF_TOPICS = tuple(t for kind in ("rolling", "anchor", "waiting", "purchase", "cash", "addon") for t in P.TOPICS[kind])
FF_PREFIX = ("STAY", "CASE", "POL", "PO", "LED", "NTC")
WINDOW_MEANING = {
    "win.rolling_cap": ("A cap on days present in every rolling period: in any stretch of {M:adj} consecutive days the "
                        "person may be present on at most {N} of them (a moving period, never a calendar year or "
                        "month).", "at most {N} in any {M:adj} period",
                        "Stay rule: the person named in the record may be present on <clause>.",
                        {"N": "count", "M": "count"},
                        ["Start with words that read after 'may be present on' and state the cap with 'at most', "
                         "'a maximum of' or 'up to'.",
                         "Write {M:adj} right before a noun such as 'period', 'window' or 'stretch' (it renders like "
                         "'180-day'); {N} renders like '90 days'."]),
    "win.later_anchor": ("A filing period that runs for {N} after the LATER of the two dates named right after the "
                         "clause (the earlier date plays no part).",
                         "within {N} after the later of these two dates",
                         "Filing rule: the appeal must be filed <clause>: the decision date and the delivery date.",
                         {"N": "count"},
                         ["Name the later of the two dates explicitly (for example 'the later of', 'whichever ... is "
                          "later', 'the later one').",
                          "End with words that introduce the two dates listed after the colon, such as 'of these two "
                          "dates' or 'of the two dates below'. {N} renders like '30 days'."]),
    "win.wait_after": ("A waiting period of {W} whose first day is the day after its start date (the start date itself "
                       "is not a waiting day).",
                       "a waiting period of {W} whose first day is the day after its start date",
                       "Cover rule: a loss is covered only after <clause>. That start date is the policy start date "
                       "...", {"W": "count"},
                       ["Say 'waiting period' and say that it begins on the day after its start date.",
                        "End with the words 'its start date', so that the next sentence ('That start date is ...') "
                        "follows. {W} renders like '30 days'."]),
}
CMP_MEANING = {
    "cmp.gt": ("the total is strictly greater than {X}: a total exactly equal to {X} does not count", "more than {X}"),
    "cmp.ge": ("the total is greater than or equal to {X}: a total exactly equal to {X} counts", "at least {X}"),
}
_KIND_OF_Q = dict(P.KIND_OF)


def _pack_items():
    items, plan = [], {}
    for i in range(N_PACKS):
        iid = f"t01a.pack.{i:03d}"
        items.append((iid, {"brief": f"Setting: {SETTINGS[i % len(SETTINGS)]}. Name style: "
                                     f"{NAME_STYLES[(i * 3) % len(NAME_STYLES)]}."}))
        plan[iid] = {"role": "pack", "held_out": i % 5 == 4}                                  # 16 of 80
    return items, plan


def _skin_items():
    items, plan = [], {}
    regs = [(r, N_SKIN_TRAIN, False) for r in TRAIN_REGISTERS] + [(r, N_SKIN_HELD, True) for r in HELD_REGISTERS]
    for ri, (reg, n, held) in enumerate(regs):
        for i in range(n):
            tone = TONES[(i + ri) % len(TONES)]
            role = ROLES[(i * 3 + ri) % len(ROLES)]
            iid = f"t01a.skin.{reg}.{i:03d}"
            items.append((iid, {"brief": f"Write {REGISTER_DESC[reg]} in which {{PERSON}} sends file {{REF}} about the "
                                         f"{{TOPIC}} to {role}. Tone: {tone}.",
                                "register": reg, "slots": dict(NARR), "rules": REGISTER_RULES[reg]}))
            plan[iid] = {"role": "skin", "register": reg, "tone": tone, "held_out": held,
                         "escape": reg if reg in ("json", "yaml") else "text"}
    return items, plan


def _freeform_items():
    items, plan = [], {}
    for i in range(N_FREEFORM):
        reg = FREEFORM_REGISTERS[i % len(FREEFORM_REGISTERS)]
        facts = {"PERSON": FF_PEOPLE[(i * 7) % len(FF_PEOPLE)],
                 "REF": f"{FF_PREFIX[i % len(FF_PREFIX)]}-{1000 + (i * 7919) % 9000}",
                 "TOPIC": FF_TOPICS[(i * 5) % len(FF_TOPICS)]}
        tone = TONES[(i // len(FREEFORM_REGISTERS)) % len(TONES)]
        role = ROLES[(i * 7) % len(ROLES)]
        iid = f"t01a.free.{reg}.{i:03d}"
        items.append((iid, {"brief": f"PERSON sends file REF about the TOPIC to {role}. Tone: {tone}.",
                            "register": reg, "facts": facts, "rules": FREEFORM_RULES[reg]}))
        plan[iid] = {"role": "freeform", "register": reg, "tone": tone, "held_out": False, "facts": facts}
    return items, plan


def _wording_items():
    items, plan = [], {}
    for q, n in WORDING_N.items():
        kind = _KIND_OF_Q[q]
        meaning, rules = WORDING_BRIEF[q]
        for i in range(n):
            slots = SLOT_SETS[kind][i % len(SLOT_SETS[kind])]
            style = STYLES[i % len(STYLES)].replace("{RULE}", RULE_NAME[kind])
            iid = f"t01a.wording.{q}.{i:03d}"
            items.append((iid, {"brief": meaning, "slots": list(slots),
                                "rules": rules + [f"Placeholders: exactly {', '.join('{' + s + '}' for s in slots)}, "
                                                  f"each once. Refer to the record as {KIND_NOUN[kind]} when you "
                                                  f"use {{REF}}." if "REF" in slots else
                                                  f"Placeholders: exactly {', '.join('{' + s + '}' for s in slots)}, "
                                                  f"each once.",
                                                  f"Style hint: {style}."]}))
            plan[iid] = {"role": "wording", "qform": q, "kind": kind, "slots": list(slots), "held_out": False}
    return items, plan


def _window_items():
    items, plan = [], {}
    for sem, (meaning, example, sentence, slots, rules) in WINDOW_MEANING.items():
        for i in range(N_WINDOW):
            iid = f"t01a.window.{sem}.{i:03d}"
            items.append((iid, {"brief": f"Write a clause with this meaning. It goes into: \"{sentence}\" Example of "
                                         f"the shape (do not copy it): \"{example}\".",
                                "meaning": meaning, "slots": dict(slots),
                                "rules": rules + [("Vary the wording: " + ("keep it short" if i % 3 == 0 else
                                                                           "use a different verb or preposition"
                                                                           if i % 3 == 1 else
                                                                           "use your own sentence shape") + ".")]}))
            plan[iid] = {"role": "lexicon", "kind": "window", "sem": sem, "slots": dict(slots)}
    return items, plan


def _cmp_items():
    items, plan = [], {}
    for sem, (meaning, example) in CMP_MEANING.items():
        for i in range(N_CMP):
            iid = f"t01a.cmp.{sem}.{i:03d}"
            items.append((iid, {"brief": f"Write a phrase with this meaning. Example (do not copy it): \"{example}\".",
                                "meaning": meaning, "slots": {"X": "cents"},
                                "rules": [("Put {X} at the end." if i % 2 == 0 else "Put {X} at the start.")
                                          if i < 6 else "Place {X} wherever it reads best."]}))
            plan[iid] = {"role": "lexicon", "kind": "comparator", "sem": sem, "slots": {"X": "cents"}}
    return items, plan


BATCH_SPECS = (
    # name, chunker kind, items fn, prompt, forbid strings, max items per chunk
    ("packs", "author_pack", _pack_items, PACK_PROMPT, FORBID_ALL, 16),
    ("skins", "author_skin", _skin_items, SKIN_PROMPT, FORBID_ALL, 46),
    ("freeform", "author_freeform", _freeform_items, FREEFORM_PROMPT, FORBID_ALL, 40),
    ("wordings", "author_wording", _wording_items, WORDING_PROMPT, QSTRINGS, 48),
    ("windows", "author_lexicon", _window_items, WINDOW_PROMPT, QSTRINGS, 42),
    ("comparators", "author_lexicon", _cmp_items, CMP_PROMPT, QSTRINGS, 24),
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
    tasks = []
    for name, (b, plan) in build_batches().items():
        files = dict(b.files())
        files[f"plan/{b.batch_id}.json"] = json.dumps({"batch_id": b.batch_id, "name": name, "kind": b.kind,
                                                       "plan": plan}, indent=1, sort_keys=True) + "\n"
        for c in b.chunks:
            tid = c["task_id"]
            ans = str(root / b.answer_path(tid))
            tfile = f"tasks/{tid}.md"
            files[tfile] = task_file_text(b, c, ans)
            tasks.append({"task_file": str(root / tfile), "answer_file": ans, "kind": b.kind, "batch": name,
                          "batch_id": b.batch_id, "task_id": tid, "n_items": len(c["items"]),
                          "prompt_sha": b.prompt_sha, "audit_allowed_read": [str(root / tfile)],
                          "audit_allowed_write": [ans]})
        paths.write_files(root, files)
    paths.write_json(root / "TASKS.json", {"family": FAMILY, "seed": SEED, "n_tasks": len(tasks), "tasks": tasks,
                                           "g0_sha256": P.T01.G0_SHA256_AUTHORED, "g0_haiku_task": P.T01.G0_HAIKU_TASK})
    return tasks


# ------------------------------------------------------------------------------------------------ loaders
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


def _norm(text: str) -> str:
    return " ".join(text.split()).lower()


def _never_open_letters(s: str) -> bool:
    return "ohs" in s.lower() or "jev" in s.lower()


_LABEL_RX = re.compile(r"(?<![a-z])(?:" + "|".join(re.escape(w) for w in P.T01.LABEL_WORDS) + r")(?![a-z])", re.I)
# G0 v2 section 7 / H38: rule, outcome, date and day-type words, and kind-specific words a neutral skin never needs
SKIN_BANNED = re.compile(
    r"\b(?:deadlines?|due|limits?|windows?|periods?|cut-?offs?|offices?|calendars?|weekdays?|weeks?|business days?|"
    r"working days?|clocks?|hours?|minutes?|dates?|days?|rules?|polic(?:y|ies)|quotes?|reports?|thresholds?|"
    r"travel|trips?|visas?|stays?|insurance|insurers?|claims?|purchases?|orders?|vendors?|suppliers?|cash|money|"
    r"banks?|tellers?|ledgers?|notices?|courts?|appeals?|filings?|losses|loss|damages?|perils?)\b", re.I)
WORDING_BANNED = re.compile(r"\b(?:today|tonight|now|currently|recently|soon|yet|already|this week|weekdays?|"
                            r"weekends?|working days?|business days?)\b", re.I)
LABEL_CHECK = re.compile(r"\b(?:correct|right|true) (?:answer|option|choice)\b|\boptions?\b|\banswer\b", re.I)
_NAME_RX = re.compile(r"^[A-Z][a-z]+(?:['-][A-Za-z][a-z]*)? [A-Z][a-z]+(?:['-][A-Z]?[a-z]+)*$")
_PHRASE_RX = re.compile(r"^[a-z][a-z' -]*[a-z]$")
_VENDOR_RX = re.compile(r"^[A-Z][a-z]+(?: [A-Z][a-z]+){1,2}$")
TOPIC_KEYS = ("rolling", "anchor", "waiting", "purchase", "cash", "notice")


def _value_problems(v: str, what: str) -> list:
    probs = []
    if not isinstance(v, str) or not v.strip() or v != v.strip():
        return [f"{what}: not a trimmed string"]
    if re.search(r"\d", v) or _LABEL_RX.search(v) or _never_open_letters(v):
        probs.append(f"{what} {v!r}: digit, label word or never-open letters")
    if negcount.count(v).k_all:
        probs.append(f"{what} {v!r}: negation cue")
    words = {w.lower() for w in re.findall(r"[A-Za-z]+", v)}
    if words & (gsl.CORE["status"] | gsl.EXTENDED["status"]):
        probs.append(f"{what} {v!r}: status or outcome word")
    lit = gsl.lint_freeform(v, {}, label_words=P.T01.LABEL_WORDS)
    if lit:
        probs.append(f"{what} {v!r}: G-SL {lit[0].rule}")
    try:
        S.name_slot(v)
    except Exception as e:  # noqa: BLE001
        probs.append(f"{what} {v!r}: {str(e)[:60]}")
    return probs


def validate_pack(p) -> list:
    """T01 pack shape (G0 section 7). Empty list = valid."""
    keys = {"people", "topics", "filing", "perils", "vendors"}
    if not isinstance(p, dict) or set(p) != keys:
        return [f"pack keys {sorted(p) if isinstance(p, dict) else type(p).__name__} != {sorted(keys)}"]
    probs = []
    people, topics, filing, perils, vendors = (p[k] for k in ("people", "topics", "filing", "perils", "vendors"))
    if not (isinstance(people, list) and len(people) == 6 and all(isinstance(x, str) and _NAME_RX.fullmatch(x)
                                                                  for x in people)):
        probs.append(f"people {people}")
    if not (isinstance(topics, dict) and set(topics) == set(TOPIC_KEYS)
            and all(isinstance(x, str) and _PHRASE_RX.fullmatch(x) and 2 <= len(x.split()) <= 4
                    for x in topics.values())):
        probs.append(f"topics {topics}")
    if not (isinstance(filing, dict) and set(filing) == {"action", "event_a", "event_b"}
            and all(isinstance(x, str) and _PHRASE_RX.fullmatch(x) for x in filing.values())):
        probs.append(f"filing {filing}")
    else:
        a, b = filing["event_a"], filing["event_b"]
        if not (a.endswith(" date") and b.endswith(" date") and a != b and a not in b and b not in a
                and 1 <= len(filing["action"].split()) <= 3 and 2 <= len(a.split()) <= 4 and 2 <= len(b.split()) <= 4):
            probs.append(f"filing labels {filing}")
    if not (isinstance(perils, list) and len(perils) == 3 and all(isinstance(x, str) and _PHRASE_RX.fullmatch(x)
                                                                  and len(x.split()) <= 3 for x in perils)):
        probs.append(f"perils {perils}")
    if not (isinstance(vendors, list) and len(vendors) == 3 and all(isinstance(x, str) and _VENDOR_RX.fullmatch(x)
                                                                    for x in vendors)):
        probs.append(f"vendors {vendors}")
    if probs:
        return probs
    values = people + list(topics.values()) + list(filing.values()) + perils + vendors
    if len({v.lower() for v in values}) != len(values):
        probs.append("a value repeats")
    groups = (people, list(topics.values()), [filing["event_a"], filing["event_b"]], perils, vendors)
    if any(a != b and a.lower() in b.lower() for g in groups for a in g for b in g):
        probs.append("a value occurs inside another value of its list")
    if any(n.lower() in v.lower() for n in people for v in values if v != n):
        probs.append("a person's name occurs inside another value")
    for v in values:
        probs += _value_problems(v, "value")
    return probs


def load_packs(root: Path = ROOT) -> tuple:
    b, plan, ans, probs = load_answers_for("packs", root)
    packs, seen = [], set()
    for iid, a in sorted(ans.items()):
        p = a.get("pack") if isinstance(a, dict) else None
        v = validate_pack(p)
        if not v and seen & {x.lower() for x in p["people"] + p["vendors"]}:
            v = ["a name or vendor repeats another pack"]
        if v:
            probs.append(f"{iid}: " + "; ".join(v[:4]))
            continue
        seen |= {x.lower() for x in p["people"] + p["vendors"]}
        packs.append({"id": f"t01-pk-{iid.rsplit('.', 1)[1]}", "held_out": plan[iid]["held_out"],
                      "haiku_task_id": _task_of(b, iid), "haiku_prompt_sha": b.prompt_sha, **p})
    return packs, probs


def _roundtrip(sk) -> list:
    """Fill with sample values (vowel and consonant topics) and read back the way solver B does (skin.parse_skin)."""
    out = []
    for topic in ("insurance claim", "visa stay count"):
        vals = {"PERSON": S.name_slot("Dana Okafor"), "REF": S.id_slot("STAY-4821"), "TOPIC": S.name_slot(topic)}
        try:
            filled = sk.fill(vals).text
            got = K.parse_skin(sk, filled, {k: (kind, ()) for k, kind in NARR.items()})
        except Exception as e:  # noqa: BLE001
            return [f"fill / parse: {str(e)[:100]}"]
        if got != {k: v.value for k, v in vals.items()}:
            out.append(f"parse_skin read {got}")
        if re.search(r"\b(?:a|an) (?:insurance|visa)\b", filled.replace("an insurance", "").replace("a visa", "")):
            out.append("article before TOPIC")
    return out


def check_skin(iid, text, meta, tid, psha, seen) -> tuple:
    """Mode T narrative skin: make_skin + G-SL lint_template + T01 word list + no question + fill / parse round trip."""
    if not isinstance(text, str) or not text.strip():
        return None, ["no text"]
    text = text.strip()
    if _norm(text) in seen:
        return None, ["duplicate text"]
    sid = f"T01-SK-{iid.split('.', 2)[2]}"
    try:
        sk = K.make_skin(sid, FAMILY, text, dict(NARR), register=meta["register"], escape=meta["escape"],
                         held_out=meta["held_out"], haiku_task_id=tid, haiku_prompt_sha=psha)
    except Exception as e:  # noqa: BLE001
        return None, [str(e)[:120]]
    v = [f"G-SL {x.rule}: {x.detail}" for x in gsl.lint_template(
        sk, label_words=P.T01.LABEL_WORDS, exceptions=P.T01.GSL_EXCEPTIONS, name_allow=P.T01.NAME_ALLOW)]
    lit = K.PH_RE.sub(" ", text)
    m = SKIN_BANNED.search(lit)
    if m:
        v.append(f"T01 word {m.group()!r} (G0 section 7)")
    if "?" in lit:
        v.append("question mark")
    v += _roundtrip(sk)
    if not v:
        seen.add(_norm(text))
    return sk, v


def check_freeform(iid, text, meta, tid, psha, seen) -> tuple:
    """Mode F note: G-SL lint_freeform + T01 word list (outside the facts) + no question + a fill swap check."""
    if not isinstance(text, str) or not text.strip():
        return None, ["no text"]
    text = text.strip()
    facts = meta["facts"]
    v = [f"G-SL {x.rule}: {x.detail}" for x in gsl.lint_freeform(text, facts, label_words=P.T01.LABEL_WORDS)]
    rest = text
    for val in sorted(facts.values(), key=len, reverse=True):
        if text.count(val) != 1:
            v.append(f"fact {val!r} appears {text.count(val)} times")
        rest = rest.replace(val, " ")
    m = SKIN_BANNED.search(rest)
    if m:
        v.append(f"T01 word {m.group()!r} (G0 section 7)")
    if not re.search(r"\bthe " + re.escape(facts["TOPIC"]), text, re.I):
        v.append("TOPIC not written after 'the'")
    if "?" in text or "{" in text or "}" in text:
        v.append("question mark or brace")
    if _norm(text) in seen:
        v.append("duplicate")
    sk = None
    if not v:
        try:
            sk = K.make_skin(f"T01-MF-{iid.rsplit('.', 1)[1]}", FAMILY, text, dict(NARR), register=meta["register"],
                             author_mode="F", brief=facts, haiku_task_id=tid, haiku_prompt_sha=psha)
            sk.fill({"PERSON": S.name_slot("Dana Okafor"), "REF": S.id_slot("POL-2217"),
                     "TOPIC": S.name_slot("teller ledger review")})
        except Exception as e:  # noqa: BLE001
            v.append(str(e)[:120])
    if not v:
        seen.add(_norm(text))
    return sk, v


def check_wording(iid, text, meta, tid, psha, seen) -> tuple:
    """Question wording: one line ending in '?', its declared slots exactly once, G-SL (role wording), EXACT negcount
    per form, the H38 word list, no label-check form. -> (qform, text, slots, task id, prompt sha)."""
    q = meta["qform"]
    if not isinstance(text, str) or "\n" in text.strip() or not text.strip().endswith("?"):
        return None, ["not one question line"]
    text = " ".join(text.split())
    names = [p.name for p in K.placeholders(text)]
    v = []
    if sorted(names) != sorted(meta["slots"]) or K.malformed(text):
        v.append(f"placeholders {names} != {meta['slots']}")
    slots = {s: SLOT_KIND[s] for s in meta["slots"]}
    try:
        sk = K.make_skin("tmp", FAMILY, text, slots, kind="wording", register="question", qform=q)
        v += [f"G-SL {x.rule}: {x.detail}" for x in gsl.lint_template(sk)]
    except Exception as e:  # noqa: BLE001
        v.append(str(e)[:120])
    c = negcount.count(text)
    if (c.k_all, c.k_syn) != NEG_EXACT[q]:
        v.append(f"negcount {(c.k_all, c.k_syn)} != {NEG_EXACT[q]}")
    lit = K.PH_RE.sub(" ", text)
    m = WORDING_BANNED.search(lit)
    if m:
        v.append(f"time or day-type word {m.group()!r} (H38)")
    if re.search(r"\boffices?\b", lit, re.I) and meta["kind"] not in ("addon", "cutoff"):
        v.append("'office' outside addon / cutoff forms (H38)")
    if LABEL_CHECK.search(lit):
        v.append("label-check form")
    if text.count("?") != 1 or text.lower() in seen or text in QSTRINGS:
        v.append("duplicate, fixture copy or two questions")
    if not v:
        seen.add(text.lower())
    return (q, text, slots, tid, psha), v


_CMP_BANNED = re.compile(r"\b(?:over|exceeds?|exceeding|excess|beyond|under|below|within|up to|between|and|not|no)\b"
                         r"|(?<!or )\babove\b", re.I)
_CMP_GT = re.compile(r"\b(?:more|greater) than\b", re.I)
_CMP_GE = re.compile(r"\bat least\b|\bor (?:more|above|greater|higher)\b|\bequal to or (?:more|greater) than\b", re.I)


def check_lexicon(iid, text, meta, tid, psha, seen) -> tuple:
    """Window clause / comparator phrase shape (G0 section 7, H9, H18). -> (sem, kind, text, slots, tid, psha)."""
    if not isinstance(text, str) or "\n" in text.strip() or not text.strip():
        return None, ["not one line"]
    text = " ".join(text.split()).rstrip(".")
    sem, v = meta["sem"], []
    names = sorted(p.name for p in K.placeholders(text))
    if names != sorted(meta["slots"]) or K.malformed(text) or re.search(r"\d", text):
        v.append(f"placeholders {names} != {sorted(meta['slots'])} (or a digit)")
    if negcount.count(text).k_all:
        v.append("negation cue")
    if meta["kind"] == "comparator":
        if _CMP_BANNED.search(text) or not (text[:1].islower() or text.startswith("{X}")):
            v.append("comparator shape (banned word or capital)")
        elif sem == "cmp.gt" and not (_CMP_GT.search(text) and not _CMP_GE.search(text)):
            v.append("cmp.gt must say 'more / greater than' and nothing inclusive")
        elif sem == "cmp.ge" and not _CMP_GE.search(text):
            v.append("cmp.ge must say 'at least', 'or more', 'or above', 'or greater' or 'equal to or more than'")
    else:
        low = text.lower()
        if not text[:1].islower() or re.search(r"\b(?:business|working|week|weeks|calendar|year|month)\b", low):
            v.append("window clause shape (lower-case start; no day-type or calendar word)")
        elif sem == "win.rolling_cap" and not (re.search(r"\b(?:at most|a maximum of|up to)\b", low)
                                               and re.search(r"\{M(?::adj)?\}", text)):
            v.append("rolling cap must say 'at most' / 'a maximum of' / 'up to' and use {M}")
        elif sem == "win.rolling_cap" and "{M:adj}" in text and not re.search(r"\{M:adj\} [a-z]", text):
            v.append("{M:adj} must stand right before a noun")
        elif sem == "win.later_anchor" and not ("later" in low and re.search(r"\btwo dates\b|\bdates\b", low)
                                                and not re.search(r"\b(?:earlier|first|either)\b", low)):
            v.append("later anchor must name the later date and introduce the two dates (H9)")
        elif sem == "win.wait_after" and not ("waiting period" in low and low.endswith("its start date")
                                              and re.search(r"\b(?:day after|next day|following day)\b", low)):
            v.append("waiting clause must say the waiting period starts the day after and end 'its start date'")
    if text.lower() in seen:
        v.append("duplicate")
    if not v:
        seen.add(text.lower())
    return (sem, meta["kind"], text, dict(meta["slots"]), tid, psha), v


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


def load_skins(root: Path = ROOT) -> tuple:
    out, probs = _loop("skins", root, check_skin)
    return {sk.skin_id: sk for sk in out}, probs


def load_freeform(root: Path = ROOT) -> tuple:
    out, probs = _loop("freeform", root, check_freeform)
    return {sk.skin_id: sk for sk in out}, probs


def load_wordings(root: Path = ROOT) -> tuple:
    return _loop("wordings", root, check_wording)


def load_lexicon(root: Path = ROOT) -> tuple:
    out, probs = [], []
    for name in ("windows", "comparators"):
        o, p = _loop(name, root, check_lexicon)
        out += o
        probs += p
    return out, probs


def lexicon_registry(wordings: list, forms: list):
    """A T01 LexiconRegistry holding the loaded Haiku forms (source haiku, pending until G-LEX extraction admits them:
    2/2, 3/3 for kind window). Sem meanings are the family's declarations in fixtures.py (incl. the window decoys)."""
    from c2_kit.lexicon import LexiconRegistry, question_sem
    reg = LexiconRegistry(FAMILY)
    reg.declare("cmp.gt", "comparator", "strictly greater than the bound")
    reg.declare("cmp.ge", "comparator", "greater than or equal to the bound")
    reg.declare("cmp.lt", "comparator", "strictly less than the bound")
    reg.declare("cmp.le", "comparator", "less than or equal to the bound")
    for sem, meaning in FX.WINDOW_SEMS:
        reg.declare(sem, "window", meaning)
    for qf, meaning in FX.QUESTION_MEANINGS.items():
        reg.declare(question_sem(FAMILY, qf), "question", meaning)
    for sem, _kind, text, slots, tid, psha in forms:
        try:
            reg.add(text, sem, slots=slots, source="haiku", family=FAMILY, haiku_task_id=tid, haiku_prompt_sha=psha)
        except Exception:  # noqa: BLE001  (duplicate or malformed text: dropped, reported by the caller)
            continue
    for q, text, slots, tid, psha in wordings:
        try:
            reg.add(text, question_sem(FAMILY, q), slots=slots, family=FAMILY, source="haiku", haiku_task_id=tid,
                    haiku_prompt_sha=psha)
        except Exception:  # noqa: BLE001
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
            print(f"{name:12s} {b.kind:16s} {b.batch_id}  items {len(b.key):4d}  chunks {len(b.chunks)}")
        return 0
    tasks = write_tasks()
    print(json.dumps({"n_tasks": len(tasks), "by_kind": {k: sum(1 for t in tasks if t["kind"] == k)
                                                         for k in sorted({t["kind"] for t in tasks})},
                      "n_items": sum(t["n_items"] for t in tasks)}))
    return 0


if __name__ == "__main__":
    sys.exit(main())
