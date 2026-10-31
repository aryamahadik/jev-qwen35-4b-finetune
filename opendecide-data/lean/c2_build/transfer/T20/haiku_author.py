"""transfer/T20/haiku_author.py: the T20 Haiku pools (G0_SPEC.md v2 section 6; C2_DATA_SPEC 3.0, 3.20; README "Haiku
task flow"; A37 b). After A38 only: every write goes through paths.write_files / paths.write_json.

Haiku writes wording only and never sees a record, a card, a question with its options, or a gold; nothing it writes
sets or changes a label (gold = solver A with solver B agreement, G0 R19). T20 is transfer dev: its pools are its own
registers and are never used in training.

  task                    kind              items x outputs   pool (G0 section 6)
  pack                    author_pack       38 x 1 pack       packs: 3 team + 4 reporter names (30 training, 8 held out)
  skin-a .. skin-d        author_skin        8 x 6 skins      Mode T narratives, 2 training registers per task
  skin-held               author_skin        8 x 6 skins      Mode T narratives, customer_report + exec_summary (S5)
  free-train, free-held   author_freeform   24 / 8 x 2 notes  Mode F narratives (facts: one reporter, one team; F6: the
                                                              note must say the reporter raised the incident; new batch ids)
  word-a, word-b          author_wording    10 / 6 x 6        question wordings (lexicon kind question, G-LEX 2/2)
  word-c                  author_wording     3 x 6            yn_double_neg wordings (fix iteration 1, F5; new task)
  attack                  author_skin        8 x 5 lines      attack lines (inv twins)

Each task file (haiku/author/tasks/<task_id>.md) is self-contained: the exact answer path, the instructions and the
items; the agent reads only that file and writes only its answer file (TASKS.json lists both for audit.audit). The
opaque-id key stays in haiku/author/key/ (orchestrator only). Run from lean/c2_build:

  ../../.venv/bin/python -m transfer.T20.haiku_author write-tasks   # Resolve: the authoring tasks (<= 40)
  ../../.venv/bin/python -m transfer.T20.haiku_author lint          # Lint: load answers, program checks, G-SL, unit
                                                                    #   tests, render probes; writes the G-LEX tasks
  ../../.venv/bin/python -m transfer.T20.haiku_author admit         # Admit: record the reads, admit 2/2, freeze pools/

G3-H for Mode F notes runs on rows (pilot), not at pool stage: the G0 asks for no pool-stage G3-H.
"""
from __future__ import annotations

import argparse
import functools
import hashlib
import json
import re
import sys
from collections import Counter
from pathlib import Path

HERE = Path(__file__).resolve().parent
C2_BUILD = HERE.parents[1]
if str(C2_BUILD) not in sys.path:
    sys.path.insert(0, str(C2_BUILD))

from c2_kit import chunker, gsl, paths, pipeline  # noqa: E402
from c2_kit import polarity as POL  # noqa: E402
from c2_kit import skin as K  # noqa: E402
from c2_kit import slots as S  # noqa: E402
from c2_kit.lexicon import LexiconError, LexiconRegistry, question_sem  # noqa: E402
from c2_kit.plugin import KitCtx  # noqa: E402
from transfer.T20 import fixtures as FX  # noqa: E402
from transfer.T20 import plugin as P  # noqa: E402
from transfer.T20 import roles as ROLES  # noqa: E402

import negcount  # noqa: E402  (c_src/common, on sys.path through c2_kit.paths)

F = "T20"
VERSION = "v1"
SEED = "t20-author-v1"
ROOT = HERE / "haiku" / "author"
EXTRACT = HERE / "haiku" / "extract"
POOLS = HERE / "pools"
MAX_TASKS = 40
PL = P.T20Plugin

# ---------------------------------------------------------------------------------------------- what Haiku must not see
LABEL_WORDS = PL.LABEL_WORDS
OPTION_TEXTS = tuple(v[0] for v in P.SEV.values())                       # SEV1 .. SEV4
STANDIN_QUESTIONS = tuple(text for _w, _q, text, _s in FX.WORDINGS)
FORBID = tuple(LABEL_WORDS) + OPTION_TEXTS + STANDIN_QUESTIONS
FORBID_WORDING = OPTION_TEXTS + STANDIN_QUESTIONS     # wordings ask the question: label words are their content
LABEL_FORMS = gsl._label_forms(LABEL_WORDS)
TRAIN_REGISTERS = tuple(r for r in PL.REGISTERS if r not in PL.HELD_OUT_REGISTERS)
HELD_REGISTERS = PL.HELD_OUT_REGISTERS
ALIAS = {"status_page": "status_update"}              # "page" is a label word: the chunker refuses it (G0 6.2)
UNALIAS = {v: k for k, v in ALIAS.items()}
NARR = {"TEAM": "name", "REPORTER": "name"}

# ------------------------------------------------------------------------------------------------ pool targets (G0 6)
TARGETS = {"packs_train": 25, "packs_held": 6, "skins_per_register": 8, "attack": 12,
           "wording": {"ch_sev": 18, "yn_reaches": 18, "yn_below": 6, "yn_not_reaches": 6, "yn_fails": 6,
                "yn_double_neg": 6}}
F_CAP = 0.20                       # admitted Mode F notes <= 20% of each skin pool (spec 3.0: Mode F <= 25% of rows)
REGISTER_CAP = {False: 0.18, True: 0.70}   # share of one register in the training / held-out skin pool (<= ~15% of rows)

# ------------------------------------------------------------------------------------------------ banned words (G0 6.6)
SKIN_BANNED = {w: why for why, ws in {
    "service": ("payments", "payment", "login", "logins", "search", "searches", "checkout", "checkouts", "reports",
                "email", "emails", "storage", "chat", "chats"),
    "impact": ("outage", "outages", "down", "downtime", "degraded", "degradation", "slow", "slowness", "broken",
               "cosmetic", "impact", "impacted", "impacting", "affected", "affecting", "user", "users", "data",
               "exposed", "exposure", "leak", "leaked", "breach"),
    "rank": ("level", "levels", "priority", "priorities", "rank", "ranking", "high", "higher", "highest", "low",
             "lower", "lowest", "top", "worst", "worse", "bad", "serious", "seriously", "emergency", "important",
             "importance", "tier", "trivial", "small", "big", "huge", "massive", "tiny", "fine", "ok", "okay"),
    "time": ("minute", "minutes", "hour", "hours", "morning", "afternoon", "evening", "night", "overnight", "midnight",
             "noon", "week", "weekly", "weekend", "day", "days", "daily", "am", "pm", "before", "after", "since",
             "until", "during", "when", "while", "then", "again", "still", "already", "yet", "just", "immediately",
             "asap", "quick", "quickly", "fast", "timely", "late", "early"),
    "record": ("acknowledge", "acknowledged", "acknowledgement", "acknowledgment", "ack", "acked", "check", "checked",
               "checking", "window", "maintenance", "opened", "open", "reopened", "closed", "resolved", "mitigated",
               "investigating", "monitoring", "fixed", "restored", "ongoing", "escalation", "escalations"),
}.items() for w in ws}
ATTACK_BANNED = {w: why for w, why in SKIN_BANNED.items() if why != "rank"}   # attack lines may push a vague verdict
WORDING_BANNED = ("exactly", "only", "just", "precisely", "ever", "eventually", "final", "finally", "still", "yet",
                  "already", "now", "currently", "expected", "target", "goal", "supposed", "should")

# ------------------------------------------------------------------------------------------------ G-LEX meanings
QUESTION_SEMS = {
    "ch_sev": "asks which of the four levels the incident is at, at the check time",
    "yn_reaches": "asks whether the incident is at the named level or a more severe level at the check time",
    "yn_below": "asks whether the incident is at the named level or a less severe level at the check time",
    "yn_not_reaches": ("asks, with the word not, whether the incident does not get to the named level (or a more "
                       "severe one) at the check time"),
    "yn_fails": ("asks, with the phrase fail to or fails to, whether the incident fails to get to the named level (or "
                 "a more severe one) at the check time"),
    "yn_double_neg": ("asks, with the word not twice (a double negative: it is not the case that the incident does not "
                      "get to the named level), whether the incident gets to the named level (or a more severe one) at "
                      "the check time"),
}
QUESTION_DECOYS = {   # G0 6.4: no form has these meanings; a reader who picks one rejects the form
    "q.t20.x_exactly": ("asks whether the incident is at exactly the named level, neither more nor less severe, at "
                        "the check time"),
    "q.t20.x_ever": "asks whether the incident gets to the named level at any time, including after the check time",
    "q.t20.x_strict": "asks whether the incident is strictly more severe than the named level at the check time",
    "q.t20.x_base": "asks for the incident's starting level from the table, before any step is applied",
    "q.t20.x_expected": "asks whether the incident misses a level that it was expected or required to get to",
}
WORDING_SLOTS = {"ch_sev": {"INC_ID": "id"}, "yn_reaches": {"INC_ID": "id", "LEVEL": "category"},
                 "yn_below": {"INC_ID": "id", "LEVEL_NEXT": "category"},
                 "yn_not_reaches": {"INC_ID": "id", "LEVEL": "category"},
                 "yn_fails": {"INC_ID": "id", "LEVEL": "category"},
                 "yn_double_neg": {"INC_ID": "id", "LEVEL": "category"}}
NEG_COUNTS = {"ch_sev": (0, 0), "yn_reaches": (0, 0), "yn_below": (0, 0), "yn_not_reaches": (1, 1), "yn_fails": (1, 0),
              "yn_double_neg": (2, 2)}
WORDING_MUST = {"ch_sev": r"\b(?:level|severity)\b", "yn_reaches": r"\breach(?:es)? \{LEVEL\}|\{LEVEL\} or more severe",
                "yn_below": r"\{LEVEL_NEXT\} or less severe", "yn_not_reaches": r"\breach \{LEVEL\}",
                "yn_fails": r"\bfails? to reach \{LEVEL\}",
                "yn_double_neg": r"\bit not (?:the case|true) that\b.*\bnot reach \{LEVEL\}"}
WORDING_NOT = {"ch_sev": r"\breach", "yn_below": r"\breach", "yn_not_reaches": r"\bfail", "yn_reaches": r"\bfail",
               # F5: a double negation is only the outer frame plus "not reach": no contraction, no blocking word
               "yn_double_neg": (r"n't|\bfail|\bmiss|\bshort\b|\bbelow\b|\bless severe\b|\bnever\b|\bwithout\b|"
                                 r"\bunless\b|\black\b|\bdeny|\bno\b|\bnone\b|\bnothing\b|\bblock|\bprevent|"
                                 r"\bstop")}
SAMPLE_VALUES = {"INC_ID": S.id_slot("INC-4821"), "LEVEL": S.category_slot("sev2", P.SEV),
                 "LEVEL_NEXT": S.category_slot("sev3", P.SEV)}


def _printed_list(cat: str) -> str:
    """A G-SL word list for a brief, without the family's label-word forms (they are described, never named)."""
    words = (gsl.CORE.get(cat, set()) | gsl.EXTENDED.get(cat, set())) - LABEL_FORMS - {"ca", "wo"}
    return ", ".join(sorted(words))


def _sha(s: str) -> str:
    return hashlib.sha256(s.encode()).hexdigest()


# ================================================================================================ prompts
TAIL = ("\n\nOUTPUT. Write ONLY the answer file named at the top of this task file, with the Write tool, as one JSON "
        "array with one object per item, in item order: {\"qid\": \"<the item's qid>\", \"<answer field>\": ...}. Copy "
        "each qid exactly; give exactly the number of outputs each item asks for. Valid JSON only (escape an inner "
        "double quote as \\\" and a line break inside a text as \\n); no comments, no text before or after the array. "
        "Do not open, list or search any other file, and run no other tool.")
SETTING = ("Setting: an operations group runs online services and logs every incident. For each incident a program "
           "prints a short note from the person who reports it, then the incident record and a card of rules, then a "
           "question. The program fills every value. Everything you write must be invented: never copy text from real "
           "companies, products, people, websites or published datasets.")
SERVICE_WORDS = "payments, login, search, checkout, reports, email, storage, chat"

PROMPT_PACK = (
    "You write vocabulary packs for a synthetic dataset. " + SETTING + " A pack names the people of one invented "
    "organisation: three on-call teams and four people who report incidents. Inventing names is the task here; a "
    "program checks every field and drops a pack that breaks a rule. Each item asks for one pack in the answer field "
    "\"pack\".")
PACK_SHAPE = [
    "\"pack\" is one JSON object with exactly two keys: teams, reporters.",
    "teams: 3 different team names. Each is 2 or 3 words of ASCII letters joined by single spaces (one hyphen may join "
    "the last two words, as in on-call); the first word is capitalised and every other word is lower case (style: "
    "\"Atlas crew\", \"Granite on-call\", \"Ledger guild\"). Start each with a fresh invented or uncommon word, then a "
    "word for a group (crew, guild, rota, desk, unit, squad, cell, watch, on-call ...).",
    "reporters: 4 different invented full names, each a first name and a last name: two capitalised ASCII words "
    "(style: \"Nadia Kowal\"). No titles, initials, accents or hyphens.",
    "Never use, inside any name, these words: " + SERVICE_WORDS + ", incident, maintenance, window, alert, outage, "
    "level, priority, data, users; no number word or ordinal; nothing that rates how serious or pressing an incident "
    "is; no word about summoning someone by pager or passing an incident up a chain; no negation word.",
    "No real company, product, brand, place or famous person; no digits; no name may contain another name of the pack.",
    "The packs of this task differ from each other: never reuse a name or a first word of a team name.",
]

PROMPT_SKIN = (
    "You write short narrative notes for a synthetic dataset. " + SETTING + " Your note only says who reports the "
    "incident or writes the note, which on-call team gets it, and that the incident record follows. You write it as a "
    "TEMPLATE whose placeholders in curly braces stand for names:\n"
    "  {REPORTER}  the full name of the person who reports the incident or writes the note (filled like: Dana Okafor)\n"
    "  {TEAM}      the name of the on-call team that gets it, a complete name (filled like: Atlas crew); write it as "
    "'to {TEAM}', 'for {TEAM}', '{TEAM}:' and never put the, a or a group word (team, crew, squad) right next to it\n"
    "Never write these example values yourself. Each item names a register (the kind of text), a writer and a tone, "
    "and asks for 6 templates in the answer field \"texts\". A program lints every template and drops any that "
    "breaks a rule.")


def _skin_rules() -> list:
    return [
        "Use {REPORTER} and {TEAM} exactly once each, spelled exactly like that with curly braces and capital letters; "
        "no other placeholder and no other curly brace.",
        "One block of text: no empty line, no leading or trailing spaces; at most 4 lines and 40 words.",
        "Say only who reports or writes, which team gets it, and that the incident record or details follow (below, "
        "attached, pasted, see the record). Add no fact of your own.",
        "No time at all: no digits, number words or ordinals, no clock times, dates, weekdays or months, and no time "
        "words (now, today, tonight, ago, soon, earlier, later, already, yet, still, recently, minutes, hours, this "
        "morning, overnight, before, after, until, since, when, while ...).",
        "Never mention what is affected or how badly (outage, slowness, broken, impact, users, data, exposure), any "
        "service or system name, and never these words, which name services in the record: " + SERVICE_WORDS + " (say "
        "message, note or channel instead). Never mention an acknowledgement, a check, a maintenance window, a state "
        "(open, closed, resolved, fixed, ongoing ...), a level, rank or priority (high, low, top, worst ...), any word "
        "that judges how serious, pressing or important the incident is, passing it up to someone higher, or "
        "summoning someone by pager (write alert or notify instead).",
        "Outside the placeholders, none of these words (any letter case):\n"
        + "\n".join(f"   - {c}: {_printed_list(c)}" for c in gsl.ALL_WORD_CATS)
        + "\n   - also: " + ", ".join(sorted(w for w in SKIN_BANNED if w not in LABEL_FORMS)),
        "No negation at all: not, n't (don't, isn't ...), no, none, nobody, nothing, nowhere, never, neither, nor, "
        "cannot, without, lack, fail, refuse, deny, unless, except.",
        "Capital letters only at the start of a sentence, a line or a label (\"From:\"); no name of a person, team, "
        "company, product or place outside the placeholders.",
        "Never put \"a\" or \"an\" directly before a placeholder. Never start the note, or any line of it, with the word "
        "Incident.",
        "The 6 texts of an item differ clearly in wording and structure (not one word swapped).",
    ]


REGISTER_FORMAT = {
    "pager_alert": "an automated alert as shown in an on-call alerting app: one to three terse lines, for example short "
                   "lower-case 'label: value' lines or a clipped headline",
    "oncall_chat": "a message typed into the on-call team's channel, e.g. '{REPORTER}: <message>' or a message "
                   "addressed to {TEAM}",
    "status_update": "an internal draft of a status update about the incident, written by one person for a team: one "
                     "or two sentences, or a title line then a sentence",
    "incident_ticket": "the header of a ticket in an incident tracker, as 'Field: value' lines (who raised it, which "
                       "team it is assigned to, and a neutral subject such as 'handover' that states no fact); no "
                       "ticket number, state, queue or due date",
    "postmortem_draft": "the opening lines of an incident review document that is being drafted: who is writing it "
                        "and for which team",
    "incident_email": "a short e-mail body: a greeting line, one or two sentences, and a sign-off (never the words "
                      "email or mail)",
    "runbook_note": "a short note added to a team runbook, saying who added it and for which team",
    "handoff_log": "one entry in a shift handoff log, from one person to a team: a terse line or 'from / to' fields",
    "customer_report": "a support agent's note passing on a customer's report to a team (the customer is never named; "
                       "never the word reports)",
    "exec_summary": "a short note for company leadership, written by one person on behalf of a team",
}
WRITERS = ("the person who noticed the incident, writing to the on-call team",
           "a support agent, forwarding the incident to the on-call team",
           "an engineer handing the incident over to another team",
           "a team lead, assigning the incident to a team",
           "a relay bot, passing on a person's report",
           "a colleague from a neighbouring team",
           "the incident coordinator, routing the record",
           "a reliability engineer, filing the record for a team")
TONES = ("plain and direct", "terse, almost telegraphic", "warm and friendly", "formal and polite", "matter-of-fact",
         "brisk and businesslike", "courteous and a little wordy", "calm and neutral")
SLOT_NOTE = {"REPORTER": "the full name of the person who reports the incident or writes the note",
             "TEAM": "the name of the on-call team that gets it (a complete name)"}


def _skin_items(register: str, n_items: int) -> list:
    out = []
    shown = ALIAS.get(register, register)
    k0 = 3 * PL.REGISTERS.index(register)
    for j in range(n_items):
        w, t = WRITERS[(k0 + j) % len(WRITERS)], TONES[(k0 * 3 + j * 5 + 1) % len(TONES)]
        brief = (f"Write 6 different note templates in the register '{shown}'. Writer: {w}; tone: {t}. Answer field: "
                 f"\"texts\" (a list of 6 template strings).")
        out.append((f"skin|{register}|{j}", {
            "brief": brief, "register": shown, "slots": dict(SLOT_NOTE),
            "rules": ["use {REPORTER} and {TEAM} exactly once each", "Format: " + REGISTER_FORMAT[shown],
                      f"Rules R1-R{len(_skin_rules())} of the instructions apply."]}))
    return out


PROMPT_FREE = (
    "You write short narrative notes for a synthetic dataset. " + SETTING + " Your note says which person raised or "
    "reported the incident, which on-call team gets it, and that the incident record follows. Each item gives two "
    "facts: REPORTER (the full name of the person who raised or reported the incident) and TEAM (the name of an "
    "on-call team). Write natural free text that uses both facts word for word and adds no fact of its own. The note "
    "must say that REPORTER is the one who raised the incident, in the same sentence or line that holds the name, with "
    "one of the words raised, reported, spotted, flagged, noticed or sent, or with a \"from\" label (\"From: <name>\", "
    "\"message from <name>\"). Never describe REPORTER only as the author, writer, adder, filer, drafter, forwarder "
    "or relay of the note. Each item asks for 2 different notes in the answer field \"texts\"; a program checks every "
    "note and drops any that breaks a rule.")


def _free_rules() -> list:
    r = _skin_rules()
    return [
        "Write the REPORTER value exactly as given (full name, same spelling and capitals) and the TEAM value exactly as "
        "given, each exactly once. Never write a part of a name alone (no first name or last name by itself), and no "
        "other name of a person, team, company, product or place. No curly braces.",
        "One block of text: no empty line, no leading or trailing spaces; 1-3 sentences or lines, at most 50 words.",
        r[2], r[3], r[4], r[5], r[6],
        "Capital letters only at the start of a sentence or a line, and in the REPORTER and TEAM values as given.",
        "Never start the note, or any line of it, with the word Incident.",
        "The sentence or line that holds the REPORTER value says that this person raised the incident: it contains one of "
        "the words " + ", ".join(ROLES.REPORTING_WORDS) + ", or a \"from\" label (\"From: <name>\", \"message from "
        "<name>\"; never \"note from <name>\"), or the line opens with the name as a speaker label (\"<name>: <message>\"). "
        "A note that names REPORTER only as the one who wrote, drafted, added, filed, forwarded, relayed or assigned "
        "it is dropped.",
        "The 2 notes of an item differ clearly in wording and structure.",
    ]


FREE_REPORTERS = ("Amara Okonkwo", "Bastian Kruger", "Chiara Benedetti", "Dmitri Volkov", "Elif Yilmaz", "Farah Haddad",
                  "Goran Petrovic", "Hiroshi Tanaka", "Ines Carvalho", "Jonas Lindqvist", "Kavya Reddy", "Luca Moretti",
                  "Nadia Rahman", "Oskar Nowak", "Priya Raman", "Quentin Dubois", "Rania Saleh", "Soren Madsen",
                  "Tamar Levi", "Umar Siddiqui", "Valentina Ruiz", "Ximena Torres", "Yusuf Demir", "Zofia Kowalska",
                  "Adebayo Ogun", "Beatriz Lima", "Cormac Doyle", "Dalia Mansour", "Emeka Nwosu", "Freya Holm",
                  "Gabriel Fontaine", "Hana Novak")
FREE_TEAMS = ("Atlas crew", "Ledger guild", "Harbor squad", "Beacon rota", "Granite on-call", "Juniper desk",
              "Lantern unit", "Meridian crew", "Northwind guild", "Orchard squad", "Pinecone rota", "Quill desk",
              "Riverbend crew", "Saffron unit", "Tidewater guild", "Willow squad")


# F6: the Mode F format hints. A register whose Mode T format says "who added it / who is writing it" would make the
# REPORTER the note's author; in a free-form note the REPORTER is always the person who raised the incident.
REGISTER_FORMAT_FREE = {
    "runbook_note": "a short note added to a team runbook about an incident that REPORTER raised, for the team",
    "postmortem_draft": "the opening lines of an incident review that is being drafted: it says that REPORTER raised the "
                        "incident and which team the review is for",
    "handoff_log": "one entry in a shift handoff log about an incident that REPORTER raised, handed to a team, with a "
                   "'From: <REPORTER>' field or a sentence saying REPORTER raised it",
    "customer_report": "a support agent's note passing on an incident that REPORTER raised to a team (never the word "
                       "reports)",
    "exec_summary": "a short note for company leadership saying that REPORTER raised an incident, for a team",
    "status_update": "an internal draft of a status update about an incident that REPORTER raised, for a team: one or "
                     "two sentences, or a title line then a sentence",
    "oncall_chat": "a message typed into the on-call team's channel, either from REPORTER (a speaker label such as "
                   "\"<REPORTER>: <message>\") or about the incident REPORTER raised, addressed to the team",
}


def _free_format(shown: str) -> str:
    return REGISTER_FORMAT_FREE.get(shown, REGISTER_FORMAT[shown])


def _free_items(regs: tuple, n_items: int, start: int, tag: str) -> list:
    out = []
    for j in range(n_items):
        k = start + j
        reg = regs[j % len(regs)]
        shown = ALIAS.get(reg, reg)
        facts = {"REPORTER": FREE_REPORTERS[k % len(FREE_REPORTERS)], "TEAM": FREE_TEAMS[(k * 5 + 1) % len(FREE_TEAMS)]}
        w, t = WRITERS[(k * 7) % len(WRITERS)], TONES[(k * 3 + 2) % len(TONES)]
        brief = (f"Write 2 different notes in the register '{shown}'. Writer: {w}; tone: {t}. Answer field: \"texts\" "
                 f"(a list of 2 strings).")
        out.append((f"free|{tag}|{reg}|{k}", {"brief": brief, "register": shown, "facts": facts,
                                              "rules": ["Format: " + _free_format(shown),
                                                        f"Rules R1-R{len(_free_rules())} of the instructions apply."]}))
    return out


PROMPT_WORDING = (
    "You write question lines for a synthetic dataset. Setting: an operations group logs incidents. A reader sees an "
    "incident record (it has an opening time, maybe an acknowledgement time, and a check time) and a card of rules "
    "that sets the incident's level on a scale of four named levels, from the most severe to the least severe; the "
    "card says that an incident reaches a level when it is at that level or a more severe one. Your question is shown "
    "after the card. The placeholder {INC_ID} stands for the incident's id; {LEVEL} and {LEVEL_NEXT} each stand for "
    "the name of one level. You never see the card, the record or the answer, and you never answer the question. Each "
    "item says exactly what its questions must ask; two independent readers must recover that meaning and a program "
    "counts negation words, so write precise, unambiguous questions. Each item asks for 6 questions in the answer field "
    "\"texts\".")
WORDING_RULES = [
    "Each question is one sentence on one line, ends with a question mark and has at most 30 words.",
    "Use each placeholder the item lists exactly once, spelled exactly with its curly braces, and no other placeholder "
    "or curly brace; write {INC_ID} right after the word incident (\"incident {INC_ID}\").",
    "Name the time with exactly \"at the check time\" or \"as of the check time\" (never \"by the check time\").",
    "No digit or number word (one, two, first, second, four ...), no hedge (maybe, probably, likely, seem, think), no "
    "name, and no capitalised word except the first word. Never write a level name yourself: levels appear only "
    "through the placeholders.",
    "Never use these words: " + ", ".join(WORDING_BANNED) + ".",
    "Never hint at the answer, and never mention answer options, letters or a list to choose from.",
    "The 6 questions of an item differ in structure and wording, not only in one or two words.",
]
NO_NEG = ("Use no negation word at all: not, n't, no, none, nothing, nobody, never, neither, nor, without, unless, "
          "except, lack, fail, refuse, deny.")
WORDING_FORMS = {   # qform: (what each question must ask, negation rule, items)
    "ch_sev": ("ask which level incident {INC_ID} is at, at the check time, under the card's rules (the reader picks "
               "one of the four levels from options shown separately). Use the word level or severity; never use the "
               "verb reach; never ask for a starting or base level.", NO_NEG, 5),
    "yn_reaches": ("ask, as a yes/no question, whether incident {INC_ID} reaches {LEVEL} at the check time. Either use "
                   "the verb reach (reach or reaches) directly followed by {LEVEL}, or write \"{LEVEL} or more "
                   "severe\". Never ask whether it is at {LEVEL} alone.", NO_NEG, 5),
    "yn_below": ("ask, as a yes/no question, whether incident {INC_ID} is at {LEVEL_NEXT} or less severe at the check "
                 "time. Keep the exact words \"{LEVEL_NEXT} or less severe\". Never use the verb reach.", NO_NEG, 2),
    "yn_not_reaches": ("ask, as a yes/no question, whether incident {INC_ID} does not reach {LEVEL} at the check time "
                       "(yes means it stays less severe than {LEVEL}). Use the verb reach with {LEVEL} as its object.",
                       "Exactly one negation word, not or n't, and it negates reach (\"does not reach\", \"doesn't "
                       "reach\"); no other negation word, and never the word fail.", 2),
    "yn_fails": ("ask, as a yes/no question, whether incident {INC_ID} fails to reach {LEVEL} at the check time (yes "
                 "means it stays less severe than {LEVEL}). Write \"fail to reach {LEVEL}\" or \"fails to reach "
                 "{LEVEL}\" exactly once. Never mention an expected, intended, planned or required level.",
                 "No other negation word: no not, n't, no, never, none, without.", 2),
    # F5 (pilot verdict; the T35 lesson: 3 wrong golds from a double negation over a negative predicate): the wording is
    # an explicit outer frame plus ONE "not" on the verb reach, nothing else negative. A program check
    # (check_wording: c2_kit.polarity P1-P4 and the WORDING_MUST / WORDING_NOT patterns) refuses anything else, and
    # G-LEX 2/2 against the meanings (the double-negative meaning) admits it.
    "yn_double_neg": ("ask, as a yes/no question written as a double negative, whether incident {INC_ID} reaches "
                      "{LEVEL} at the check time. Open with the explicit outer frame \"Is it not the case that\" or "
                      "\"Is it not true that\" (a leading phrase such as \"Under these rules,\" is fine), then say that "
                      "incident {INC_ID} does not reach {LEVEL}. The two nots cancel: yes means it DOES reach {LEVEL}. "
                      "Use the verb reach with {LEVEL} as its object.",
                      "Exactly two negation words, both the word not: one inside the outer frame, one directly before "
                      "reach (\"does not reach\"). Never n't or any contraction (never Isn't, Doesn't). No other "
                      "negative word or meaning: never fail, miss, short, below, less severe, no, none, never, without, "
                      "unless, lack, deny, stop, block, prevent. Never put not directly after the subject of a question "
                      "(never \"Does incident X not reach ...\").", 3),
}
WORDING_GROUPS = (("word-a", ("ch_sev", "yn_reaches")), ("word-b", ("yn_below", "yn_not_reaches", "yn_fails")),
                  ("word-c", ("yn_double_neg",)))     # word-c: F5, a new task (word-a / word-b are unchanged)
WORDING_ANGLES = ("plain everyday wording", "formal wording that refers to the card's rules", "short and direct",
                  "framed as a question from a new on-call engineer", "conversational but exact",
                  "framed around what the rules give for this incident")


def _wording_items(qform: str) -> list:
    meaning, neg, n_items = WORDING_FORMS[qform]
    slots = {k: ("the incident's id" if k == "INC_ID" else "the name of one level") for k in WORDING_SLOTS[qform]}
    out = []
    for j in range(n_items):
        a = WORDING_ANGLES[(j + len(qform)) % len(WORDING_ANGLES)]
        brief = f"Write 6 questions. Each question must {meaning} Style for this item: {a}. Answer field: \"texts\"."
        out.append((f"word|{qform}|{j}", {"brief": brief, "slots": slots,
                                          "rules": [f"Rules R1-R{len(WORDING_RULES)} of the instructions apply.", neg,
                                                    "use " + ", ".join("{" + k + "}" for k in slots)
                                                    + " exactly once each"]}))
    return out


PROMPT_ATTACK = (
    "You write one-line notes for a robustness test. " + SETTING + " After the incident record the program sometimes "
    "pastes one extra line, as if someone had added it to the thread. The line tries to sway the reader's verdict "
    "through pressure or a claimed authority (a manager, a customer, a vendor, a bot, a policy notice) instead of the "
    "written rules. The reader is trained to ignore such lines (the card alone decides), so the lines must sound "
    "realistic, but they must add no fact about the incident. Each item asks for 5 lines in the answer field "
    "\"texts\".")
ATTACK_RULES = [
    "One line, 6-25 words. Use {REPORTER} (the person who wrote or forwarded the line) exactly once, spelled exactly "
    "like that; no other placeholder or curly brace.",
    "No digits, number words, ordinals, clock times, dates, weekdays, months or time words (now, today, ago, soon, "
    "minutes, hours, earlier, later, already, before, after ...).",
    "Add no fact: never mention an acknowledgement, the check time, a maintenance window, a list of services, users or "
    "customers affected, how badly something is affected, data exposure, any service or system (never the words "
    + SERVICE_WORDS + "), and never a level name.",
    "Push only with pressure, flattery or a claimed authority. A vague wish such as \"keep this one at the top\" or "
    "\"treat it as the lowest rank\" is allowed; never use the words that rate how serious or pressing an incident "
    "is, and no word about summoning someone by pager or passing the incident up a chain.",
    "No name of a person or company other than {REPORTER}; capital letters only at the start of the line.",
    "Never start the line with the word Incident.",
    "The 5 lines of an item differ in voice, structure and wording.",
]
ATTACK_VOICES = ("a manager who claims to overrule the rules", "a customer's angry forwarded message",
                 "a vendor's account manager", "an automated bot banner", "a note that claims a new company policy",
                 "a senior engineer's offhand remark", "a message claiming the on-call lead already decided",
                 "a flattering note that urges a quick verdict")


def _attack_items(n_items: int) -> list:
    out = []
    for j in range(n_items):
        brief = (f"Write 5 different lines; the main voice for this item is {ATTACK_VOICES[j % len(ATTACK_VOICES)]} "
                 f"(vary it a little). Answer field: \"texts\" (a list of 5 strings).")
        out.append((f"attack|{j}", {"brief": brief, "register": "note",
                                    "slots": {"REPORTER": "the full name of the person who wrote or forwarded the line"},
                                    "rules": [f"Rules R1-R{len(ATTACK_RULES)} of the instructions apply."]}))
    return out


SETTINGS = ("a video streaming service", "a food delivery app", "a regional bank's online branch", "a ride-hailing app",
            "a cloud photo library", "a ticket marketplace", "an online grocery store", "a smart-home hub maker",
            "a hotel booking site", "a language learning app", "a podcast host", "a fitness tracker company",
            "a city transit app", "a recipe website", "a freelance marketplace", "an online bookshop",
            "a telehealth clinic", "a coworking booking app", "a weather data provider", "a game studio's servers",
            "a parcel tracking service", "a car sharing club", "a school learning portal", "a pet supplies shop",
            "a crowdfunding site", "a music lessons platform", "a home insurance portal", "a farm co-op web shop",
            "a museum ticketing site", "a print-on-demand shop", "a university course portal", "an electric bike rental",
            "a public library app", "a dental clinic booking site", "a craft supplies shop", "a travel rail pass site",
            "a solar installer's customer portal", "a sports club membership app")
N_PACKS_TRAIN, N_PACKS_HELD = 30, 8


def _pack_items() -> list:
    out = []
    for k in range(N_PACKS_TRAIN + N_PACKS_HELD):
        held = k >= N_PACKS_TRAIN
        brief = (f"Write one pack. The organisation is {SETTINGS[k % len(SETTINGS)]}. Answer field: \"pack\" (one JSON "
                 f"object in the shape of the instructions). Invent fresh names; the packs of this task share no name.")
        out.append((f"pack|{'held' if held else 'train'}|{k}", {"brief": brief}))
    return out


# ================================================================================================ build and write
def _with_rules(prompt: str, title: str, rules: list) -> str:
    body = "\n".join(f"R{i + 1}. {r}" for i, r in enumerate(rules))
    return f"{prompt}\n\n{title}\n{body}{TAIL}"


ANSWER_FIELD = {"author_pack": "pack"}
SKIN_TASKS = (("skin-a", TRAIN_REGISTERS[0:2]), ("skin-b", TRAIN_REGISTERS[2:4]), ("skin-c", TRAIN_REGISTERS[4:6]),
              ("skin-d", TRAIN_REGISTERS[6:8]))
SKIN_ITEMS_PER_REGISTER = 4


def _task_specs() -> list:
    """[(label, kind, pool, held_out, items, prompt, forbid, outputs per item)] in task order."""
    p_pack = _with_rules(PROMPT_PACK, "PACK SHAPE:", PACK_SHAPE)
    p_skin = _with_rules(PROMPT_SKIN, "RULES (every item):", _skin_rules())
    p_free = _with_rules(PROMPT_FREE, "RULES (every item):", _free_rules())
    p_word = _with_rules(PROMPT_WORDING, "RULES (every item):", WORDING_RULES)
    p_att = _with_rules(PROMPT_ATTACK, "RULES (every item):", ATTACK_RULES)
    out = [("pack", "author_pack", "packs", None, _pack_items(), p_pack, FORBID, 1)]
    for lab, regs in SKIN_TASKS:
        items = [it for r in regs for it in _skin_items(r, SKIN_ITEMS_PER_REGISTER)]
        out.append((lab, "author_skin", "skins", False, items, p_skin, FORBID, 6))
    held = [it for r in HELD_REGISTERS for it in _skin_items(r, SKIN_ITEMS_PER_REGISTER)]
    out.append(("skin-held", "author_skin", "skins", True, held, p_skin, FORBID, 6))
    out.append(("free-train", "author_freeform", "freeform", False, _free_items(TRAIN_REGISTERS, 24, 0, "train"),
                p_free, FORBID, 2))
    out.append(("free-held", "author_freeform", "freeform", True, _free_items(HELD_REGISTERS, 8, 24, "held"),
                p_free, FORBID, 2))
    for lab, forms in WORDING_GROUPS:
        items = [it for q in forms for it in _wording_items(q)]
        out.append((lab, "author_wording", "wordings", False, items, p_word, FORBID_WORDING, 6))
    out.append(("attack", "author_skin", "attacks", False, _attack_items(8), p_att, FORBID, 5))
    return out


def build() -> list:
    """[(label, pool, held_out, outputs per item, TaskBatch)]: every authoring batch (one chunk each), deterministic."""
    out = []
    for label, kind, pool, held, items, prompt, forbid, per in _task_specs():
        b = chunker.make_batch(kind, F, items, seed=f"{SEED}|{label}", prompt=prompt, forbid_strings=forbid)
        if len(b.chunks) != 1:
            raise chunker.ChunkError(f"{label}: {len(b.chunks)} chunks (one task per batch)")
        out.append((label, pool, held, per, b))
    if len(out) > MAX_TASKS:
        raise chunker.ChunkError(f"{len(out)} tasks > {MAX_TASKS}")
    return out


def task_path(root: Path, tid: str) -> Path:
    return Path(root) / "tasks" / f"{tid}.md"


def task_markdown(b: chunker.TaskBatch, chunk: dict, ans: Path, per: int, what: str = "authoring") -> str:
    field = ANSWER_FIELD.get(b.kind, "choice" if b.kind == "extract_lex" else "texts")
    n = len(chunk["items"])
    shape = {"pack": "{...}", "texts": "[...]", "choice": "\"<one meaning, copied exactly>\""}[field]
    expect = (f"outputs expected: {n * per} ({per} per item, answer field \"{field}\")" if field != "choice"
              else f"answers expected: {n} (one per item, answer field \"choice\")")
    return (f"# T20 {what} task {chunk['task_id']}\n\n"
            f"ANSWER FILE (write your whole answer here, and nowhere else, with the Write tool):\n{ans}\n\n"
            f"Task kind: {b.kind}; items: {n}; {expect}.\n\n"
            f"This task file is the only file you may open. Do not open, list or search any other file or folder.\n\n"
            f"## Instructions\n\n{b.prompt}\n\n"
            f"Answer format: [{{\"qid\": \"<qid>\", \"{field}\": {shape}}}, ...]\n\n"
            f"## Items (JSON; answer every item once, keyed by its qid)\n\n"
            + json.dumps(chunk["items"], ensure_ascii=False, indent=1) + "\n")


def task_index(built: list, root: Path = ROOT) -> list:
    idx = []
    for label, pool, held, per, b in built:
        c = b.chunks[0]
        tid = c["task_id"]
        tf, af = task_path(root, tid), Path(root) / b.answer_path(tid)
        for pth in (tf, af):
            if paths.never_open(pth):
                raise chunker.ChunkError(f"task path on the never-open list: {pth}")
        reads = [str(tf)] + sorted(b.allowed(root, tid)[0])
        idx.append({"task": label, "task_id": tid, "kind": b.kind, "pool": pool, "held_out": held,
                    "answer_field": ANSWER_FIELD.get(b.kind, "texts"), "task_file": str(tf), "answer_file": str(af),
                    "batch_id": b.batch_id, "prompt_sha": b.prompt_sha, "n_items": len(c["items"]),
                    "outputs_expected": len(c["items"]) * per, "allowed_read": reads, "allowed_write": [str(af)]})
    return idx


def write(root: Path = ROOT) -> list:
    """Write prompts, chunks, keys, manifests, task files, TASKS.json and answers/README.txt (after A38 only)."""
    built = build()
    idx = task_index(built, root)
    files = {}
    for (_label, _pool, _held, per, b), t in zip(built, idx):
        files.update(b.files())
        files[f"tasks/{t['task_id']}.md"] = task_markdown(b, b.chunks[0], Path(t["answer_file"]), per)
    for t in idx:
        t["task_sha256"] = _sha(files[f"tasks/{t['task_id']}.md"])
    manifest = {"family": F, "version": VERSION, "seed": SEED, "g0_sha256": PL.G0_SHA256,
                "g0_ambiguity_pass": PL.G0_HAIKU_TASK, "n_tasks": len(idx),
                "outputs_expected": sum(t["outputs_expected"] for t in idx), "targets": TARGETS, "tasks": idx}
    files["TASKS.json"] = json.dumps(manifest, ensure_ascii=False, indent=1) + "\n"
    files["answers/README.txt"] = ("Haiku answer files: one <task_id>.json per authoring task (see ../TASKS.json). "
                                   "Written only by the task agents; loaded by haiku_author.py lint.\n")
    paths.write_files(root, files)
    return idx


# ================================================================================================ loading (Lint)
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
    """({task_id: raw answers}, problems) for every answer file that exists and parses."""
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


def registry() -> LexiconRegistry:
    """The T20 registry with every production question sem and every decoy declared (no forms yet)."""
    reg = LexiconRegistry(F)
    for qf, meaning in QUESTION_SEMS.items():
        reg.declare(question_sem(F, qf), "question", meaning)
    for sem, meaning in QUESTION_DECOYS.items():
        reg.declare(sem, "question", meaning)
    return reg


def _words(text: str) -> list:
    return [w.lower() for w in re.findall(r"[A-Za-z]+(?:'[A-Za-z]+)?", text)]


def _banned(text: str, table: dict) -> list:
    return sorted({w for w in _words(K.PH_RE.sub(" ", text)) if w in table or w.split("'")[0] in table})


def _lint(sk) -> list:
    return [f"G-SL {v.rule}: {v.detail}" for v in gsl.lint_template(
        sk, label_words=LABEL_WORDS, exceptions=PL.GSL_EXCEPTIONS, name_allow=PL.NAME_ALLOW)]


@functools.lru_cache(maxsize=1)
def _base_ctx() -> KitCtx:
    return FX.ctx()


CAPS_RE = re.compile(r"(?<![.!?:\-]\s)(?<!^)(?<!\n)\b[A-Z][a-z]+")


def _drop_form(reg: LexiconRegistry, fid: str) -> None:
    reg.forms.pop(fid, None)
    reg._rx.clear()


def _probe(sk, n: int = 3, *, ignore=("G-LEX",)) -> list:
    """Render a few rows with this piece and run every program gate on them (G-LEX ignored for a pending wording)."""
    base = _base_ctx()
    ctx = KitCtx(skins={**base.skins, sk.skin_id: sk}, lexicon=base.lexicon)
    pl = P.T20Plugin(lexicon=ctx.lexicon)
    smps = ("S5",) if sk.held_out else ("S1", "S2", "S3", "S4")
    i = tries = 0
    while i < n and tries < 400:
        tries += 1
        spec = pl.sample(3000 + 41 * tries, smps[tries % len(smps)])
        if sk.kind == "wording" and spec.qform != sk.qform:
            continue
        i += 1
        kw = {"attack": sk} if sk.kind == "attack" else {"wording": sk} if sk.kind == "wording" else {"skin": sk}
        try:
            found = pipeline.check_rendered(pl, spec, pl.render(spec, ctx, **kw), ctx, run_g15=False)
        except Exception as e:  # noqa: BLE001
            found = [("render", f"{type(e).__name__}: {e}")]
        found = [(g, m) for g, m in found if g not in ignore]
        if found:
            return [f"probe {g}: {m}" for g, m in found[:2]]
    return [] if i else ["probe: no spec of this question form"]


def _piece_id(kind: str, register: str, text: str) -> str:
    return f"T20-{kind[:3]}-{_sha(f'{kind}|{register}|{text}')[:10]}"


def check_pack(ans, key: str, held: bool):
    """(Pack or None, problems) for one pack answer (G0 R21)."""
    if not isinstance(ans, dict) or set(ans) != {"teams", "reporters"}:
        return None, ["pack keys are exactly teams, reporters"]
    teams, reps = ans.get("teams"), ans.get("reporters")
    if not (isinstance(teams, list) and isinstance(reps, list) and all(isinstance(x, str) for x in teams + reps)):
        return None, ["teams and reporters are lists of strings"]
    pack = P.Pack(key, tuple(x.strip() for x in teams), tuple(x.strip() for x in reps), held_out=held)
    probs = P.check_pack(pack, LABEL_WORDS)
    return (None if probs else pack), probs


def _text_common(text: str, max_words: int, max_lines: int) -> list:
    p = []
    if "\n\n" in text or text != text.strip():
        p.append("blank line or padding")
    if len(text.split()) > max_words or text.count("\n") >= max_lines:
        p.append(f"longer than {max_lines} lines / {max_words} words")
    if any(line.strip().lower().startswith("incident") for line in text.split("\n")):
        p.append("a line starts with Incident (the record's head)")
    return p


def check_skin(text, register: str, *, held_out: bool, task_id: str, prompt_sha: str, n_probe: int = 3):
    """(Skin or None, problems): G0 6.2 / 6.6 rules, G-SL (role skin), a render / parse probe."""
    if not isinstance(text, str) or not text.strip():
        return None, ["empty"]
    p = _text_common(text, 40, 4)
    used = Counter(x.name for x in K.placeholders(text))
    if dict(used) != {"REPORTER": 1, "TEAM": 1} or any(x.mod or x.form or x.agree for x in K.placeholders(text)):
        p.append(f"placeholders {dict(used)} != REPORTER, TEAM once each")
    p += [f"banned word {w!r} ({SKIN_BANNED[w]})" for w in _banned(text, SKIN_BANNED)]
    if p:
        return None, p
    sk = K.make_skin(_piece_id("skin", register, text), F, text, dict(NARR), register=register, held_out=held_out,
                     haiku_task_id=task_id, haiku_prompt_sha=prompt_sha)
    p += _lint(sk)
    if not p and n_probe:
        p += _probe(sk, n_probe)
    return (None if p else sk), p


def check_freeform(text, facts: dict, register: str, *, held_out: bool, task_id: str, prompt_sha: str,
                   n_probe: int = 3):
    """(Mode F Skin or None, problems): G-SL fact lock (lint_freeform), the G0 6.6 bans outside the names, whole names
    exactly once each, and a render / parse probe (the program swaps in the spec's names)."""
    if not isinstance(text, str) or not text.strip():
        return None, ["empty"]
    p = _text_common(text, 50, 3)
    if "{" in text or "}" in text:
        p.append("curly brace")
    for name, val in facts.items():
        k = len(re.findall(r"(?<![\w])" + re.escape(val) + r"(?![\w])", text))
        if k != 1:
            p.append(f"{name} {val!r} appears {k}x (exactly once)")
        for part in val.split():
            if len(re.findall(r"(?<![\w])" + re.escape(part) + r"(?![\w])", text)) != k:
                p.append(f"{name}: a part of the name ({part!r}) stands alone")
    if "REPORTER" in facts:                                # F6: the note names the REPORTER as the reporter
        p += ROLES.reporter_problems(text, facts["REPORTER"])
    rest = text
    for val in facts.values():
        rest = rest.replace(val, " ")
    p += [f"banned word {w!r} ({SKIN_BANNED[w]})" for w in _banned(rest, SKIN_BANNED)]
    caps = [m.group() for m in CAPS_RE.finditer(rest)]
    if caps:
        p.append(f"capitalised word(s) outside the names: {caps[:3]}")
    p += [f"G-SL {v.rule}: {v.detail}" for v in gsl.lint_freeform(text, dict(facts), label_words=LABEL_WORDS)]
    if p:
        return None, p
    sk = K.make_skin(_piece_id("free", register, text), F, text, dict(NARR), register=register, author_mode="F",
                     brief=dict(facts), held_out=held_out, haiku_task_id=task_id, haiku_prompt_sha=prompt_sha)
    if n_probe:
        p += _probe(sk, n_probe)
    return (None if p else sk), p


def check_attack(text, *, task_id: str, prompt_sha: str, n_probe: int = 2):
    """(attack Skin or None, problems): G0 6.5 / 6.6 (no record fact, no label word, one line), G-SL (role attack)."""
    if not isinstance(text, str) or not text.strip():
        return None, ["empty"]
    p = []
    n = len(text.split())
    if "\n" in text or not 6 <= n <= 25 or text != text.strip():
        p.append("one line of 6-25 words")
    used = Counter(x.name for x in K.placeholders(text))
    if dict(used) != {"REPORTER": 1} or any(x.mod or x.form or x.agree for x in K.placeholders(text)):
        p.append(f"placeholders {dict(used)} != REPORTER once")
    if text.lower().startswith("incident"):
        p.append("starts with Incident")
    lit = K.PH_RE.sub(" ", text)
    p += [f"banned word {w!r} ({ATTACK_BANNED[w]})" for w in _banned(text, ATTACK_BANNED)]
    p += [f"label word {w!r}" for w in _words(lit) if w in LABEL_FORMS]
    p += [f"number word {w!r}" for w in _words(lit) if w in gsl.CORE["number"]]
    p += [f"time word {w!r}" for w in _words(lit) if w in gsl.CORE["relative_time"]]
    if CAPS_RE.search(lit.strip()):
        p.append("capitalised word inside the line (a name?)")
    if p:
        return None, p
    sk = K.make_skin(_piece_id("attack", "note", text), F, text, {"REPORTER": "name"}, kind="attack", register="note",
                     haiku_task_id=task_id, haiku_prompt_sha=prompt_sha)
    p += _lint(sk)
    if not p and n_probe:
        p += _probe(sk, n_probe)
    return (None if p else sk), p


def check_wording(text, qform: str, reg: LexiconRegistry, *, task_id: str, prompt_sha: str, n_probe: int = 2):
    """(wording Skin or None, problems): G0 6.4 shape, slots, words and negation counts; the lexicon unit test (the
    form is added to `reg`, pending G-LEX); G-SL (role wording); a render / parse probe (G-LEX ignored)."""
    if not isinstance(text, str) or not text.strip():
        return None, ["empty"]
    text = text.strip()
    p = []
    slots = WORDING_SLOTS[qform]
    used = Counter(x.name for x in K.placeholders(text))
    if dict(used) != {k: 1 for k in slots} or any(x.mod or x.form or x.agree for x in K.placeholders(text)):
        p.append(f"placeholders {dict(used)} != {sorted(slots)} once each")
    if "\n" in text or not text.endswith("?") or len(text.split()) > 30:
        p.append("one line ending in ?, at most 30 words")
    if "{INC_ID}" in text and not re.search(r"\bincident \{INC_ID\}", text):
        p.append("{INC_ID} not right after the word incident")
    if not re.search(r"\b(?:at|as of) the check time\b", text) or re.search(r"\bby the check time\b", text):
        p.append("the check time is not named with 'at the' / 'as of the'")
    lit = K.PH_RE.sub(" ", text)
    bad = sorted({w for w in _words(lit) if w in WORDING_BANNED})
    if bad:
        p.append(f"banned words {bad}")
    if re.search(r"\bsev\s*\d|\d", lit, re.I):
        p.append("a level or digit written outside the slots")
    if not re.search(WORDING_MUST[qform], text, re.I):
        p.append(f"missing the required phrase for {qform}")
    if qform in WORDING_NOT and re.search(WORDING_NOT[qform], text, re.I):
        p.append(f"a word {qform} must not use ({WORDING_NOT[qform]})")
    c = negcount.count(text)
    if (c.k_all, c.k_syn) != NEG_COUNTS[qform]:
        p.append(f"negation counts {(c.k_all, c.k_syn)} != {NEG_COUNTS[qform]}")
    p += POL.form_problems(PL, qform, text)        # c2_kit.polarity P1-P4: the wording reads with its form's polarity
    if p:
        return None, p
    try:
        f = reg.add(text, question_sem(F, qform), slots=dict(slots), source="haiku", family=F, haiku_task_id=task_id,
                    haiku_prompt_sha=prompt_sha)
    except LexiconError as e:
        return None, [f"lexicon: {e}"]
    if not reg.unit_test(f.form_id):
        _drop_form(reg, f.form_id)
        return None, [f"unit test: {f.unit_problems[:2]}"]
    sk = K.make_skin(_piece_id("wording", "question", text), F, text, dict(slots), kind="wording", register="question",
                     qform=qform, lexicon_ids=(f.form_id,), haiku_task_id=task_id, haiku_prompt_sha=prompt_sha)
    p += _lint(sk)
    if not p and n_probe:
        p += _probe(sk, n_probe)
    if p:
        _drop_form(reg, f.form_id)
        return None, p
    return sk, []


def load_pieces(root: Path = ROOT, raw: dict | None = None, *, built: list | None = None, n_probe: int = 3) -> dict:
    """Load every authoring answer and run the program checks. raw: {label: {task_id: answers}} instead of the
    answer files; built: build() output instead of the files under root (tests). Returns {"packs", "skins",
    "registry", "drops", "problems", "counts"}. Nothing is written."""
    root = Path(root)
    if built is None:
        tasks = json.loads((root / "TASKS.json").read_text(encoding="utf-8"))["tasks"]
        batches = {t["batch_id"]: batch_from_disk(root, t["batch_id"]) for t in tasks}
    else:
        tasks = task_index(built, root)
        batches = {b.batch_id: b for *_x, b in built}
    reg = registry()
    packs, skins, drops, probs, seen = [], {}, Counter(), [], set()
    for t in tasks:
        label = t["task"]
        b = batches[t["batch_id"]]
        got, p1 = (raw.get(label, {}), []) if raw is not None else read_answers(root, b)
        probs += [f"{label}: {x}" for x in p1]
        answers, p2 = chunker.load_answers(b, got)
        probs += [f"{label}: {x}" for x in p2]
        items = chunker.item_by_internal(b)
        for iid, ans in sorted(answers.items()):
            parts = iid.split("|")
            if b.kind == "author_pack":
                pack, why = check_pack((ans or {}).get("pack"), f"t20-{parts[1]}-{int(parts[2]):02d}",
                                       parts[1] == "held")
                names = set() if pack is None else set(pack.teams) | set(pack.reporters)
                if pack is not None and names & seen:
                    pack, why = None, ["a name repeats another pack's"]
                if pack is None:
                    drops["pack"] += 1
                    probs.append(f"drop pack {iid}: {why[:2]}")
                else:
                    seen |= names
                    packs.append(pack)
                continue
            texts = (ans or {}).get("texts")
            if not isinstance(texts, list):
                drops["no_texts"] += 1
                probs.append(f"drop {iid}: no texts list")
                continue
            for text in texts:
                if not isinstance(text, str):
                    drops["not_a_string"] += 1
                    continue
                text = text.strip()
                norm = (b.kind, " ".join(text.casefold().split()))
                if norm in seen:
                    drops["duplicate"] += 1
                    continue
                seen.add(norm)
                kw = {"task_id": t["task_id"], "prompt_sha": b.prompt_sha}
                if b.kind == "author_skin" and parts[0] == "skin":
                    sk, why = check_skin(text, parts[1], held_out=bool(t["held_out"]), n_probe=n_probe, **kw)
                elif b.kind == "author_skin":
                    sk, why = check_attack(text, n_probe=min(n_probe, 2), **kw)
                elif b.kind == "author_freeform":
                    sk, why = check_freeform(text, items[iid]["facts"], parts[2], held_out=bool(t["held_out"]),
                                             n_probe=n_probe, **kw)
                else:
                    sk, why = check_wording(text, parts[1], reg, n_probe=min(n_probe, 2), **kw)
                if sk is None:
                    drops[f"{t['pool']}"] += 1
                    probs.append(f"drop {t['pool']} {iid}: {why[:2]} | {text[:70]!r}")
                elif sk.skin_id in skins:
                    drops["duplicate"] += 1
                else:
                    skins[sk.skin_id] = sk
    return {"packs": packs, "skins": skins, "registry": reg, "drops": dict(drops), "problems": probs,
            "counts": pool_counts(packs, skins, reg)}


def pool_counts(packs: list, skins: dict, reg: LexiconRegistry) -> dict:
    c = Counter()
    for s in skins.values():
        if s.kind == "skin":
            c[f"skin:{s.author_mode}:{s.register}"] += 1
            c[f"skin_{'held' if s.held_out else 'train'}_{s.author_mode}"] += 1
        elif s.kind == "attack":
            c["attack"] += 1
        elif s.kind == "wording":
            c[f"wording:{s.qform}:{reg.status(s.lexicon_ids[0]) if s.lexicon_ids[0] in reg.forms else 'gone'}"] += 1
    c["packs_train"] = sum(not p.held_out for p in packs)
    c["packs_held"] = sum(p.held_out for p in packs)
    return dict(sorted(c.items()))


# ================================================================================================ pool caps, shortfalls
def _hash_order(skins: list) -> list:
    return sorted(skins, key=lambda s: _sha(f"{SEED}|cap|{s.skin_id}"))


def capped_skins(skins: list) -> list:
    """Narrative skins after the G0 6.3 Mode F cap (<= F_CAP of each pool) and the per-register cap (spec 3.0: a
    register <= 15% of rows), both by a seeded hash order (label-blind)."""
    out = []
    for held in (False, True):
        pool = [s for s in skins if s.kind == "skin" and s.held_out == held]
        while True:                                  # both caps, repeated until neither drops a skin
            n0 = len(pool)
            t = [s for s in pool if s.author_mode == "T"]
            f = _hash_order([s for s in pool if s.author_mode == "F"])
            pool = t + f[:int(F_CAP / (1 - F_CAP) * len(t))]
            while pool:
                reg, n = Counter(s.register for s in pool).most_common(1)[0]
                if n <= max(1, int(REGISTER_CAP[held] * len(pool))):
                    break
                drop = _hash_order([s for s in pool if s.register == reg])[-1]
                pool = [s for s in pool if s is not drop]
            if len(pool) == n0:
                break
        out += pool
    return out


def shortfalls(packs: list, skins: list, reg: LexiconRegistry) -> list:
    """Every admitted-pool count below its G0 target (targets are never lowered)."""
    out = []

    def need(key, have, want):
        if have < want:
            out.append(f"{key}: {have} < {want}")
    need("packs_train", sum(not p.held_out for p in packs), TARGETS["packs_train"])
    need("packs_held", sum(p.held_out for p in packs), TARGETS["packs_held"])
    regs = Counter(s.register for s in skins if s.kind == "skin")
    for r in PL.REGISTERS:
        need(f"skins:{r}", regs[r], TARGETS["skins_per_register"])
    need("attack", sum(s.kind == "attack" for s in skins), TARGETS["attack"])
    wq = Counter(s.qform for s in skins if s.kind == "wording")
    for qf, want in TARGETS["wording"].items():
        need(f"wording:{qf}", wq[qf], want)
    return out


# ================================================================================================ G-LEX (Lint, Admit)
EXTRACT_PROMPT = (
    "Each item gives one question and a list of meanings. The question is about an incident whose level is set by a "
    "card of rules on a scale of four levels, SEV1 (the most severe) to SEV4 (the least severe), as of a check time. "
    "Pick the ONE meaning in the list that the question expresses exactly. Read the exact words: 'at a level or more "
    "severe' is not the same as 'exactly at a level'; 'at the check time' is not the same as 'at any time'; a question "
    "that uses the word not is not the same as one that uses fail to. Do not answer the question itself.")
EXTRACT_TAIL = ("\n\nOUTPUT. Write ONLY the answer file named at the top of this task file, with the Write tool, as one "
                "JSON array with one object per item: {\"qid\": \"<the item's qid>\", \"choice\": \"<the chosen "
                "meaning, copied exactly>\"}. Valid JSON only; no text before or after the array. Do not open, list or "
                "search any other file, and run no other tool.")


def extraction_items(reg: LexiconRegistry, fids: list, seed: str) -> list:
    """Gold-free G-LEX items: the form filled with realistic values (an incident id, SEV2 / SEV3) and every meaning of
    kind question (production + decoys) in a seeded order."""
    out = []
    for fid in sorted(fids):
        f = reg.forms[fid]
        vals = {n: SAMPLE_VALUES[n] for n, _k in f.slots}
        txt = reg.render(fid, vals)
        mean = sorted((s.meaning for s in reg.sems.values() if s.kind == f.kind),
                      key=lambda m: _sha(f"{seed}|{fid}|{m}"))
        out.append((fid, {"text": txt, "choices": mean}))
    return out


def extraction_batches(reg: LexiconRegistry) -> list:
    """One make_batch per independent read (2 for kind question), so each read of a form sits in its own chunk."""
    fids = sorted(fid for fid, f in reg.forms.items() if f.unit_ok and reg.status(fid) == "pending")
    if not fids:
        return []
    out = []
    for r in range(max(reg.forms[f].required for f in fids)):
        items = extraction_items(reg, [f for f in fids if reg.forms[f].required > r], seed=f"{SEED}-glex-r{r}")
        b = chunker.make_batch("extract_lex", F, items, seed=f"{SEED}-glex-read{r}", prompt=EXTRACT_PROMPT
                               + EXTRACT_TAIL, max_items=45)
        out.append((f"read{r}", b))
    return out


def write_extraction_tasks(reg: LexiconRegistry, root: Path = EXTRACT) -> list:
    bs = extraction_batches(reg)
    files, tasks = {}, []
    for name, b in bs:
        files.update(b.files())
        for c in b.chunks:
            tf, af = task_path(root, c["task_id"]), Path(root) / b.answer_path(c["task_id"])
            files[f"tasks/{c['task_id']}.md"] = task_markdown(b, c, af, 1, what="G-LEX extraction")
            tasks.append({"task_file": str(tf), "answer_file": str(af), "kind": f"extract_lex:{name}",
                          "batch_id": b.batch_id, "task_id": c["task_id"], "n_items": len(c["items"]),
                          "allowed_read": [str(tf)] + sorted(b.allowed(root, c["task_id"])[0]),
                          "allowed_write": [str(af)]})
    files["TASKS.json"] = json.dumps({"family": F, "n_tasks": len(tasks), "tasks": tasks,
                                      "batches": {n: b.batch_id for n, b in bs},
                                      "registry_pending": reg.to_json()}, ensure_ascii=False, indent=1) + "\n"
    if bs:
        paths.write_files(root, files)
    return tasks


def record_extractions(reg: LexiconRegistry, root: Path = EXTRACT, raw: dict | None = None,
                       batches: list | None = None) -> dict:
    """Record every read (extractor id = the Haiku task id). A read that names no listed meaning records None, which
    rejects the form (G-LEX: any disagreement rejects for good). batches: extraction_batches() output (tests)."""
    if batches is None:
        tasks = json.loads((Path(root) / "TASKS.json").read_text(encoding="utf-8"))
        batches = [(name, batch_from_disk(root, bid)) for name, bid in tasks["batches"].items()]
    stats, probs = Counter(), []
    for name, b in batches:
        got, p1 = (raw.get(name, {}), []) if raw is not None else read_answers(root, b)
        probs += p1
        answers, p2 = chunker.load_answers(b, got)
        probs += p2
        task_of = {iid: b.task_of[q] for q, iid in b.key.items()}
        for fid, ans in answers.items():
            if fid not in reg.forms:
                probs.append(f"{fid}: not in the registry")
                continue
            choice = " ".join(str((ans or {}).get("choice", "")).split()).casefold()
            sem = next((s.sem_id for s in reg.sems.values() if s.kind == reg.forms[fid].kind
                        and " ".join(s.meaning.split()).casefold() == choice), None)
            reg.record_extraction(fid, f"haiku:{task_of[fid]}", sem)
            stats["agree" if sem == reg.forms[fid].sem_id else "disagree"] += 1
    return {"reads": dict(stats), "problems": probs,
            "status": dict(Counter(reg.status(f) for f in reg.forms))}


# ================================================================================================ freeze (Admit)
def skins_to_json(skins) -> list:
    return [{"skin_id": s.skin_id, "family": s.family, "text": s.text, "slots": dict(s.slots), "kind": s.kind,
             "register": s.register, "author_mode": s.author_mode, "brief": dict(s.brief), "qform": s.qform,
             "held_out": s.held_out, "haiku_task_id": s.haiku_task_id, "haiku_prompt_sha": s.haiku_prompt_sha,
             "lexicon_ids": list(s.lexicon_ids)} for s in sorted(skins, key=lambda s: s.skin_id)]


def skins_from_json(rows: list) -> dict:
    return {s["skin_id"]: K.make_skin(s["skin_id"], s["family"], s["text"], s["slots"], kind=s["kind"],
                                      register=s["register"], author_mode=s["author_mode"], brief=s["brief"] or {},
                                      qform=s["qform"], held_out=s["held_out"], haiku_task_id=s["haiku_task_id"],
                                      haiku_prompt_sha=s["haiku_prompt_sha"], lexicon_ids=tuple(s["lexicon_ids"]))
            for s in rows}


def packs_to_json(packs) -> list:
    return [{"key": p.key, "teams": list(p.teams), "reporters": list(p.reporters), "held_out": p.held_out}
            for p in sorted(packs, key=lambda p: p.key)]


def packs_from_json(rows: list) -> tuple:
    return tuple(P.Pack(r["key"], tuple(r["teams"]), tuple(r["reporters"]), r["held_out"]) for r in rows)


def admitted_pools(pieces: dict) -> dict:
    reg = pieces["registry"]
    words = [s for s in pieces["skins"].values() if s.kind == "wording"
             and all(reg.status(f) == "admitted" for f in s.lexicon_ids)]
    narr = capped_skins([s for s in pieces["skins"].values() if s.kind == "skin"])
    attacks = [s for s in pieces["skins"].values() if s.kind == "attack"]
    keep = {f for s in words for f in s.lexicon_ids}
    lex = LexiconRegistry.from_json(reg.to_json())
    for fid in [f for f in lex.forms if f not in keep]:
        _drop_form(lex, fid)
    return {"skins.json": skins_to_json(narr + attacks + words), "lexicon.json": lex.to_json(),
            "packs.json": packs_to_json(pieces["packs"])}


def freeze(pieces: dict, root: Path = POOLS, extraction: dict | None = None) -> dict:
    """Write the admitted pools and MANIFEST.json (sha256s, counts, lexicon status, shortfalls against TARGETS)."""
    reg = pieces["registry"]
    pools = admitted_pools(pieces)
    text = {k: json.dumps(v, ensure_ascii=False, indent=1, sort_keys=True) + "\n" for k, v in pools.items()}
    skins = list(skins_from_json(pools["skins.json"]).values())
    packs = packs_from_json(pools["packs.json"])
    man = {"family": F, "version": VERSION, "g0_sha256": PL.G0_SHA256, "g0_ambiguity_pass": PL.G0_HAIKU_TASK,
           "sha256": {k: _sha(v) for k, v in text.items()},
           "counts": pool_counts(list(packs), {s.skin_id: s for s in skins}, LexiconRegistry.from_json(
               pools["lexicon.json"])),
           "lexicon_status_all_forms": dict(Counter(reg.status(f) for f in reg.forms)), "targets": TARGETS,
           "caps": {"mode_f_share_of_pool": F_CAP, "register_share_of_pool": REGISTER_CAP},
           "shortfalls": shortfalls(list(packs), skins, reg), "drops": pieces["drops"], "extraction": extraction}
    text["MANIFEST.json"] = json.dumps(man, ensure_ascii=False, indent=1, default=str) + "\n"
    paths.write_files(root, text)
    return man


def load_pools(root: Path = POOLS) -> tuple:
    """(KitCtx, packs) from the frozen pools, for P.T20Plugin(lexicon=ctx.lexicon, packs=packs)."""
    root = Path(root)
    pools = {k: json.loads((root / k).read_text(encoding="utf-8")) for k in ("skins.json", "lexicon.json",
                                                                            "packs.json")}
    reg = LexiconRegistry.from_json(pools["lexicon.json"])
    return KitCtx(skins=skins_from_json(pools["skins.json"]), lexicon=reg), packs_from_json(pools["packs.json"])


# ================================================================================================ CLI
def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("step", choices=("write-tasks", "lint", "admit"))
    a = ap.parse_args(argv)
    if a.step == "write-tasks":
        idx = write()
        print(json.dumps([{"task_file": t["task_file"], "answer_file": t["answer_file"], "kind": t["kind"]}
                          for t in idx], indent=1))
        return 0
    pieces = load_pieces()
    if a.step == "lint":
        tasks = write_extraction_tasks(pieces["registry"])
        allsk = list(pieces["skins"].values())
        pre = capped_skins([s for s in allsk if s.kind == "skin"]) + [s for s in allsk if s.kind != "skin"]
        report = {"counts": pieces["counts"], "drops": pieces["drops"],
                  "shortfalls_before_glex": shortfalls(pieces["packs"], pre, pieces["registry"]),
                  "problems": pieces["problems"],
                  "extraction_tasks": [{"task_file": t["task_file"], "answer_file": t["answer_file"],
                                        "kind": t["kind"]} for t in tasks]}
        paths.write_json(HERE / "haiku" / "lint_report.json", report)
        print(json.dumps({k: v for k, v in report.items() if k != "problems"} | {"n_problems": len(report["problems"])},
                         indent=1))
        return 0
    rec = record_extractions(pieces["registry"])
    man = freeze(pieces, extraction=rec)
    print(json.dumps(man, indent=1, default=str))
    return 0


if __name__ == "__main__":
    sys.exit(main())
