"""families/T32/authoring.py: T32 Haiku AUTHORING tasks (G0_SPEC.md v2 section 7; C2_DATA_SPEC 3.0, 3.9) and the
program checks the lint stage runs on the answers. After A38 only: every write goes through paths.write_files.

  tasks (one make_batch each, one chunk of <= 50 gold-free items)        kind              items x outputs
  lex_commit_{a,b,c}   commit, commit_if, try message forms            author_lexicon     6 x 6 forms
  lex_close_{a,b}      done, retract, release message forms             author_lexicon     6 x 6 forms
  lex_ext_{a,b}        ext_ask, ext_yes, ext_no message forms           author_lexicon     6 x 6 forms
  lex_event_{a,b}      cond_met, cond_off, remind, ack message forms    author_lexicon     8 x 6 forms
  pack_{0,1,2}         packs, two settings each (7 per setting)         author_pack       14 x 1 pack
  skin_*               Mode T narrative skins, 9 training registers     author_skin        4 x 4 skins per register
  skin_held            Mode T skins, held-out registers sms / forum     author_skin        6 x 4 skins
  free_{a,b}           Mode F intros, 8 training registers              author_freeform   16 x 3 intros
  free_held            Mode F intros, held-out registers                author_freeform    8 x 3 intros
  word_status, word_due, word_broken, word_kept, word_vs   question wordings (10 forms)   author_wording  4-12 x 4-5
  attack_{a,b}         inert attack notes with {OWNER}                  author_skin        4 x 5 lines

Each chunk file (haiku/author/chunks/<task_id>.json) is the whole task: it carries `answer_file` (the exact path the
Haiku agent writes) and `instructions` (the batch prompt) next to its items, so the agent reads one file. Haiku never
sees a question with options, an option list, a chat or a gold. Every batch forbids (make_batch checks prompt and
items) the label words, the option texts and the stand-in question strings; the wording batches that must name a
status (yn_broken / yn_kept forms name their predicate, the "rather than" forms name all five) drop exactly those words
from their own forbid list. Message forms show the date slots to Haiku as {DATE} / {NEW_DATE} ("due" is a label word);
load() renames them back to {DUE} / {NEW_DUE} (SLOT_RENAME). Nothing here sets a label.

  build() -> [(label, TaskBatch)]   write() -> task index (writes haiku/author/, after A38 only)
  check_message / check_pack / check_skin / check_freeform / check_wording / check_attack   per-piece program checks
  load(root) -> {task_id: {...pieces, problems}}     registry(pieces) -> LexiconRegistry of the passing forms

Run (from lean/c2_build):  ../../.venv/bin/python -m families.T32.authoring
"""
from __future__ import annotations

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
from c2_kit.lexicon import LexiconError, LexiconRegistry, question_sem  # noqa: E402
from families.T32 import fixtures as FX  # noqa: E402
from families.T32 import plugin as P  # noqa: E402
from families.T32 import vocab as V  # noqa: E402

import negcount  # noqa: E402  (c_src/common, on sys.path through c2_kit.paths)

FAMILY = "T32"
ROOT = HERE / "haiku" / "author"
AMB_DIR = HERE / "haiku" / "ambiguity"
SEED = "t32-author-v1"
MAX_TASKS = 40

OPTION_TEXTS = tuple(P.STATUS_TEXT.values())
STANDIN_QUESTIONS = tuple(t for _w, _q, t in FX.WORDINGS)
LABELS = tuple(P.T32.LABEL_WORDS)
FORBID_ALL = LABELS + OPTION_TEXTS + STANDIN_QUESTIONS


def _minus(*words) -> tuple:
    drop = {w.lower() for w in words}
    return tuple(f for f in FORBID_ALL if f.lower() not in drop)


FORBID_BROKEN = _minus("broken", "break")      # yn_broken family wordings name their predicate
FORBID_KEPT = _minus("kept", "keep")           # yn_kept family wordings name their predicate
FORBID_VS = STANDIN_QUESTIONS                  # the "rather than" wordings name all five statuses
SLOT_RENAME = {"DATE": "DUE", "NEW_DATE": "NEW_DUE"}          # Haiku-facing slot -> form slot (G0 section 7)
HAIKU_SLOT = {v: k for k, v in SLOT_RENAME.items()}
TRAIN_REGISTERS = tuple(r for r in P.T32.REGISTERS if r not in P.T32.HELD_OUT_REGISTERS)
HELD_REGISTERS = tuple(P.T32.HELD_OUT_REGISTERS)
SETTINGS = {
    "home": "a household: housemates, neighbours or a couple sharing a home",
    "rental": "renting a home: tenants, a landlord or a letting agent",
    "freelance": "freelance work: a freelancer and their clients",
    "team": "a small work team in an office or a remote company",
    "club": "a local club or volunteer group",
    "family": "a family planning things together",
}
SUBSETTINGS = {
    "home": ("housemates sharing a big old house", "neighbours on one quiet street", "a couple doing up their first "
             "home", "a household with a garden and an allotment", "residents of a block of flats with a shared "
             "garden", "a busy home with pets and teenagers", "grown-up siblings sharing a house"),
    "rental": ("tenants of a city flat and their landlord", "students renting a house through a letting agent",
               "a lodger and a live-in landlord", "a holiday-let owner and a cleaner", "a landlord with several "
               "tenants in one building", "a family renting a terraced house", "a tenant moving out as a lease ends"),
    "freelance": ("a graphic designer and a client", "a wedding photographer and a couple", "a freelance video editor "
                  "and an agency", "a web developer and a small shop owner", "a copywriter and a marketing "
                  "manager", "an illustrator and a book publisher", "a freelance translator and a client"),
    "team": ("a small software team", "an office admin team", "a marketing team at a mid-size company",
             "a university research group", "a customer support team", "a remote design team",
             "a warehouse operations team"),
    "club": ("a local football club", "a community choir", "a charity fun-run committee", "a community garden group",
             "a school parents' association", "a cycling club", "a youth theatre group"),
    "family": ("parents and grown-up children", "cousins planning a reunion", "a family organising a wedding",
               "grandparents and grandchildren", "a family planning a holiday", "siblings caring for an elderly "
               "parent", "a family preparing a birthday party"),
}
PACK_TASKS = (("home", "rental"), ("freelance", "team"), ("club", "family"))
PACKS_PER_SETTING, PACKS_FROZEN_PER_SETTING = 7, 5
ALL_SETTINGS = tuple(SETTINGS)
REGISTER_SETTINGS = {"family_chat": ("family", "home"), "landlord_tenant": ("rental",),
                     "freelance_client": ("freelance",), "team_chat": ("team",), "flatmates": ("home", "rental"),
                     "club_volunteers": ("club",)}       # any other register: every setting (setting-neutral text)

# ================================================================================================ shared prompt parts
COMMON_TAIL = (
    "\n\nOUTPUT. Write ONLY the answer file named in this task file's \"answer_file\" field, with the Write tool, as one "
    "JSON array with one object per item, in item order: {\"qid\": \"<the item's qid>\", <the field the item's brief "
    "names>: ...}. Copy each qid exactly. Valid JSON only (escape inner double quotes as \\\" and newlines inside a "
    "text as \\n); no comments, no text before or after the array. Read no other file and run no other tool.")
NO_FACT_WORDS = ("no number or number word (one, two, first, second, couple, half, dozen), no date, weekday, month, "
                 "time of day or time word (today, tomorrow, tonight, now, soon, later, next, last, week, weekend, "
                 "day, month, morning, already, yet, asap, overdue)")
STATUS_WORDS = ("done, complete, completed, finished, confirmed, approved, accepted, allowed, granted, denied, "
                "settled, cancelled, canceled, closed, open, pending, failed, late, okay, ok, paid, valid, resolved, "
                "active")


def _with_rules(prompt: str, title: str, rules) -> str:
    body = "\n".join(f"R{i + 1}. {r}" for i, r in enumerate(rules)) if isinstance(rules, (list, tuple)) else rules
    head, sep, tail = prompt.partition("\n\nOUTPUT.")
    return f"{head}\n\n{title}\n{body}{sep}{tail}"


# ================================================================================================ message forms
PROMPT_LEX = (
    "You write short chat messages for a dataset of invented group chats in which people promise each other small "
    "everyday tasks. Each message is a template: placeholders in curly braces stand for facts that a program fills "
    "in later.\n"
    "  {TASK}     a lower-case bare verb phrase (filled like: return the drill / book the minibus / send the logo "
    "drafts); write it where a bare verb phrase fits: after 'I will', 'I'll', 'to', 'can I', 'you can'.\n"
    "  {DATE}     a calendar date (filled like: 12 March 2026 / 2026-03-12 / Thursday, 12 March 2026); write it after "
    "'by', 'until' or 'on'.\n"
    "  {NEW_DATE} a later calendar date, written the same way.\n"
    "  {COND}     a lower-case planned event starting with 'the' (filled like: the street party / the client "
    "workshop / the away match).\n"
    "Filled example: the template \"Leave it with me, I will {TASK} by {DATE}.\" reads \"Leave it with me, I will "
    "return the drill by 12 March 2026.\" Never copy an example template and never write an example value yourself.\n"
    "Each item names one message MEANING, the placeholders it uses and a style. Write the requested number of "
    "different messages that one person in a casual group chat could send with exactly that meaning. A program checks "
    "every message, and two independent readers must later recover the same meaning from it, so each message must "
    "say its meaning plainly and say nothing else." + COMMON_TAIL)
LEX_RULES = [
    "Use each placeholder the item lists exactly once, spelled exactly like that (curly braces, capital letters). "
    "Write no other placeholder and no other curly brace.",
    "One line of 4 to 12 words (a placeholder counts as one word); most messages 5 to 9 words. Ordinary punctuation "
    "only: no emoji, no quotation marks, no @, |, #, /, brackets or newlines.",
    "Never start a message with a placeholder. Capitalise only the first word and the word I.",
    "Write no name, no place, no amount, and " + NO_FACT_WORDS + ". The only date in a message is its {DATE} or "
    "{NEW_DATE} placeholder.",
    "Never use these status words: " + STATUS_WORDS + "; and never use a word that names the final standing of a "
    "promise (whether it was honoured or failed, or set off by an event): the program drops such messages.",
    "The message carries exactly the item's meaning: no reason, no second action, no extra condition, no question "
    "about anything else, no thanks for something else.",
    "The messages of an item differ from each other in structure and wording, not only in one or two words.",
    "Negation words (not, n't, no, never) are fine where the meaning needs them (taking a promise back, saying no to "
    "a new date, letting someone off, not promising); use none where the meaning does not need one.",
]
LEX_SEMS = {   # sem -> (Haiku placeholders, meaning brief); the G0 R4 slot signature with DUE shown as DATE
    "chat.commit": (("TASK", "DATE"), "the sender firmly and unconditionally promises to do {TASK} by {DATE}. A "
                    "certain promise ('I will', 'I'll ... by', 'count on me'); no hedge (try, hope, maybe, might, "
                    "should) and no condition."),
    "chat.commit_if": (("COND", "TASK", "DATE"), "the sender firmly promises to do {TASK} by {DATE}, but only on "
                       "condition that {COND} goes ahead: the dependency on {COND} taking place must be explicit "
                       "('if {COND} goes ahead', 'as long as {COND} is on', 'provided {COND} happens'). No hedge."),
    "chat.try": (("TASK", "DATE"), "the sender says they will try or hope to do {TASK} by {DATE} WITHOUT promising: "
                 "it must never read as a firm promise (use try, hope, aim, see if I can, no promises, might "
                 "manage, can't promise)."),
    "chat.done": (("TASK",), "the sender reports that they have carried out {TASK}: it has happened (past tense, "
                  "for example built on 'I managed to {TASK}' or 'ticked off my list'; {TASK} is a bare verb phrase, "
                  "so it needs 'to' or a list-style colon before it). Never use the words done, finished, complete "
                  "or completed."),
    "chat.retract": (("TASK",), "the sender takes back their own earlier promise to do {TASK}: they will not do it "
                     "after all (an apology is fine; no new date, no offer to do it later)."),
    "chat.release": (("TASK",), "the sender tells the other person they no longer have to do {TASK} at all: they "
                     "are let off it completely (not a delay, not a new date, not a reminder)."),
    "chat.ext_ask": (("TASK", "NEW_DATE"), "the sender, who had promised {TASK}, asks the other person for more "
                     "time: whether they may do {TASK} by {NEW_DATE} instead. A question."),
    "chat.ext_yes": (("TASK", "NEW_DATE"), "the sender says yes to moving the date: it is fine for the other person "
                     "to do {TASK} by {NEW_DATE} instead. A clear yes that repeats the new date."),
    "chat.ext_no": (("TASK",), "the sender says no to moving the date: the other person still has to do {TASK} by "
                    "the date already set. A clear refusal; no date placeholder."),
    "chat.cond_met": (("COND",), "the sender announces that {COND} is going ahead: it will take place as planned."),
    "chat.cond_off": (("COND",), "the sender announces that {COND} is called off: it will not take place."),
    "chat.remind": (("TASK",), "the sender asks for news about {TASK} or gently nudges about it, without asking for "
                    "anything else (no new date, no letting off, no promise, no complaint)."),
    "chat.ack": ((), "the sender briefly acknowledges a message (thanks, noted, got it, sounds good) without agreeing "
                 "to any change, date or promise and without letting anyone off. No placeholder at all; 2 to 8 words "
                 "(an exception to the length rule)."),
}
LEX_GROUPS = (("commit", ("chat.commit", "chat.commit_if", "chat.try"), 3),
              ("close", ("chat.done", "chat.retract", "chat.release"), 2),
              ("ext", ("chat.ext_ask", "chat.ext_yes", "chat.ext_no"), 2),
              ("event", ("chat.cond_met", "chat.cond_off", "chat.remind", "chat.ack"), 2))
LEX_STYLES = ("casual texting between friends or family", "polite and slightly formal, as between a tenant and a "
              "landlord or a freelancer and a client", "brief and businesslike, as in a work team chat",
              "warm and chatty, as among club volunteers", "terse, as few words as the meaning allows",
              "relaxed and friendly, with a light everyday phrase")
FORMS_PER_ITEM = 6
SLOT_NOTES = {"TASK": "a lower-case bare verb phrase (the task)", "DATE": "a calendar date",
              "NEW_DATE": "a later calendar date", "COND": "a planned event starting with 'the'"}


def _lex_items(sems: tuple, part: int) -> list:
    out = []
    for si, sem in enumerate(sems):
        phs, meaning = LEX_SEMS[sem]
        for j in range(2):
            style = LEX_STYLES[(part * 2 + j + si) % len(LEX_STYLES)]
            brief = (f"Write {FORMS_PER_ITEM} different messages with this meaning. Style: {style}. Answer field: "
                     f"\"forms\" (a list of {FORMS_PER_ITEM} strings).")
            slots = {p: SLOT_NOTES[p] for p in phs} or {"none": "this meaning uses no placeholder"}
            out.append((f"lex|{sem}|{part}|{j}", {"brief": brief, "meaning": meaning, "slots": slots,
                                                  "rules": [f"Rules R1-R{len(LEX_RULES)} of the instructions "
                                                            "apply."]}))
    return out


# ================================================================================================ packs
PROMPT_PACK = (
    "You write small vocabulary packs for a dataset of invented group chats in which people promise each other small "
    "everyday tasks. Everything is invented and everyday: no real companies, brands, products, places or people. "
    "Each item names a setting and asks for ONE pack in the field \"pack\": a JSON object with exactly these three "
    "lists:\n"
    "  \"tasks\": 10 different small tasks one person in that setting could promise to do for another, each a "
    "lower-case bare verb phrase of 2 to 6 words that reads naturally after 'I will' and after 'to' (shape like: "
    "water the plants / send the logo drafts / book the meeting room);\n"
    "  \"events\": 6 different planned events in that setting that could go ahead or be called off, each a "
    "lower-case noun phrase of 2 to 6 words starting with 'the' (shape like: the street party / the client "
    "workshop);\n"
    "  \"topics\": 4 different things a whole group chat in that setting could be about, each a lower-case noun "
    "phrase of 2 to 5 words starting with 'the' (shape like: the house move / the brand refresh).\n"
    "A program checks every phrase and drops a pack or a phrase that breaks a rule." + COMMON_TAIL)
PACK_RULES = [
    "Letters, single spaces and hyphens only: no digit, comma, apostrophe, quote, slash or other sign; no capital "
    "letter.",
    "No name, place, brand or amount, no number or number word (one, two, first, second, half, dozen), no weekday or "
    "month, and no relative time word (today, tomorrow, tonight, now, soon, later, next, last, already, yet); "
    "words like 'day', 'night' or 'weekend' are fine inside an event's name (shape: the sports day).",
    "No status word (" + STATUS_WORDS + "), no negation (no, not, never, without, un-), no condition word (if, "
    "unless) and no word that says how something went.",
    "Tasks are concrete one-off jobs one person can do for another (fetch, fix, book, send, return, collect, print, "
    "pay, set up ...), never 'try', 'promise', 'help with' or 'think about'; they contain no 'by' or 'until'. Events "
    "are things that happen at a set time (a visit, an inspection, a meeting, a fair, a match, a trip, a launch). "
    "Topics are broad projects or occasions, never a single task.",
    "Every phrase is unique: within the pack, across all packs of this task, and different from the shape examples "
    "in these instructions (never reuse an example).",
    "Packs of the same setting differ in their situation (the item names it): make each pack's phrases fit that "
    "situation.",
]


def _pack_items(settings: tuple) -> list:
    out = []
    for st in settings:
        for i, sub in enumerate(SUBSETTINGS[st][:PACKS_PER_SETTING]):
            brief = (f"Write one pack for the setting '{SETTINGS[st]}'; the situation of this pack: {sub}. Answer "
                     "field: \"pack\" (one JSON object with exactly the lists tasks, events and topics).")
            out.append((f"pack|{st}|{i}", {"brief": brief}))
    return out


# ================================================================================================ narrative skins (Mode T)
PROMPT_SKIN = (
    "You write short intros that sit above an exported group chat in a dataset. A program prints the chat itself "
    "after your intro and a blank line. Your intro is a template with two placeholders:\n"
    "  {TOPIC}  what the chat is about: a lower-case noun phrase that already starts with 'the' (filled like: the "
    "house move / the lease renewal / the summer fair planning);\n"
    "  {OWNER}  the first name of the chat member who saved, exported or shared the chat (filled like: Priya).\n"
    "Filled example of a template \"Export of the family group chat about {TOPIC}, saved by {OWNER}.\" -> \"Export "
    "of the family group chat about the house move, saved by Priya.\" Never copy the example template and never "
    "write an example value yourself.\n"
    "Each item names a register (the kind of text) and the settings the intro must fit, and asks for 4 templates in "
    "the field \"skins\". The intro is background only: a reader must learn nothing from it about who promised what "
    "or how anything went." + COMMON_TAIL)
SKIN_RULES = [
    "Use {TOPIC} and {OWNER} exactly once each, spelled exactly like that; no other placeholder and no other curly "
    "brace outside JSON syntax. {TOPIC} already starts with 'the': never write 'the', 'a' or 'an' right before it, "
    "and never start a sentence or line with a placeholder.",
    "Add no fact: never mention a task, a job, an event, a promise, an agreement, a request, a date, a deadline, an "
    "extension, a result, who did what, or how many people or messages there are.",
    "Write no name other than {OWNER}, no place, company or brand, no digit, no amount, and " + NO_FACT_WORDS + ".",
    "No quantity or frequency word (all, every, each, some, any, both, either, several, many, few, more, most, only, "
    "always, never, usually, whole, entire, single, extra, another, total).",
    "No modal (must, may, might, can, could, should, will, would, need, have to, able, allowed, required), no hedge "
    "(maybe, perhaps, probably, likely, think, believe, seems, appears, almost) and no condition word (if, unless, "
    "except, otherwise, instead, provided).",
    "No status word (" + STATUS_WORDS + ") and no negation of any kind (not, n't, no, never, nothing, none, nobody, "
    "without, nor, neither).",
    "No capitalised word except at the start of a sentence or line or in a 'Field:' label; 'I' is fine. No line may "
    "start with 'Members:' or 'Chat log'.",
    "At most 3 lines and 25 words; most intros 8 to 16 words. No blank line.",
    "The 4 templates of an item differ from each other in structure and wording, not only in one or two words.",
]
REGISTER_FORMAT = {
    "family_chat": "the title or first line of an exported family group chat: one or two plain sentences.",
    "landlord_tenant": "a short note above messages between tenants and their landlord or letting agent, as copied "
                       "into a record: one or two sentences.",
    "freelance_client": "a short line above a project message thread between a freelancer and a client, as pasted "
                        "into a project log.",
    "team_chat": "the export header of a work team's chat channel: a title line and a short description line, or "
                 "one sentence.",
    "flatmates": "a casual line above a flatmates' group chat, as saved by one of them.",
    "club_volunteers": "a short line above a club or volunteer committee group chat, as shared with the committee.",
    "email_digest": "the start of an email that forwards the chat: a 'Subject:' line and one short body sentence; no "
                    "greeting with a name and no sign-off name other than {OWNER}.",
    "support_thread": "a note above a chat attached to a help-desk or support case, as one sentence or as 'Field: "
                      "value' lines (no case number).",
    "json_export": "a one-line JSON object with lower-case snake_case keys and plain lower-case string values; "
                   "{TOPIC} and {OWNER} are each a whole bare value, e.g. \"topic\": {TOPIC} (no quotes around a "
                   "placeholder). No numbers, booleans, null, arrays, ids or timestamps. It must be valid JSON once "
                   "each placeholder is replaced by a quoted string. In your answer the template is a JSON string, so "
                   "escape its inner quotes as \\\".",
    "sms_export": "the header of a text-message thread backed up from a phone: one or two short lines.",
    "forum_thread": "the title line and first line of a neighbourhood or hobby forum post that reposts the chat.",
}
SKIN_ITEMS = 4
SKIN_TASKS = (("family_chat", "landlord_tenant"), ("freelance_client", "team_chat"), ("flatmates", "club_volunteers"),
              ("email_digest", "support_thread"), ("json_export",))
SKIN_HELD_ITEMS = 3


def _fit(register: str) -> str:
    sts = REGISTER_SETTINGS.get(register)
    if not sts:
        return "every setting: write it so it fits a chat in any setting (home, rental, freelance work, work team, " \
               "club, family)"
    return "chats about " + " or ".join(SETTINGS[s] for s in sts)


def _skin_items(register: str, n_items: int) -> list:
    out = []
    for j in range(n_items):
        brief = (f"Write 4 different intro templates in the register '{register}'. They must fit {_fit(register)}. "
                 "Answer field: \"skins\" (a list of 4 template strings).")
        out.append((f"skin|{register}|{j}", {"brief": brief, "register": register,
                                             "slots": {"TOPIC": "what the chat is about, starting with 'the'",
                                                       "OWNER": "first name of the member who saved or shared it"},
                                             "rules": [f"Rules R1-R{len(SKIN_RULES)} of the instructions apply.",
                                                       "Format: " + REGISTER_FORMAT[register]]}))
    return out


# ================================================================================================ Mode F intros
PROMPT_FREE = (
    "You write short free-form intros that sit above an exported group chat in a dataset. A program prints the chat "
    "itself after your intro and a blank line. Each item gives two facts: OWNER, the first name of the chat member "
    "who saved or shared the chat, and TOPIC, what the chat is about. Write the requested intros in the item's "
    "register, each mentioning both facts copied EXACTLY as given (same spelling and letter case, including the topic's "
    "'the'), written so that any other first name and any other 'the ...' topic could stand in their place. The intro "
    "is background only: a reader must learn nothing from it about who promised what or how anything went. This task "
    "has no placeholders: the two facts are written out in full, and they are the only name and topic you write. "
    "Answer field: \"intros\" (a list of strings)." + COMMON_TAIL)
FREE_RULES = [
    "Each fact appears exactly once, verbatim. Do not put 'the' or 'a' right before the topic (it already starts "
    "with 'the') and do not start a sentence with the topic.",
    "Add nothing else of substance: no other name, place, company or brand, no digit, no amount, and "
    + NO_FACT_WORDS + ".",
    "Never mention a task, a job, an event, a promise, an agreement, a request, a deadline, a result or who did what.",
    "No status word (" + STATUS_WORDS + ") and no negation of any kind (not, n't, no, never, nothing, none, "
    "without, nor).",
    "One or two sentences, at most 25 words; most intros 10 to 18 words. No blank line, no list, no heading.",
    "The intros of an item differ from each other in structure and wording.",
]
FREE_REGISTERS = tuple(r for r in TRAIN_REGISTERS if r != "json_export")
FREE_ITEMS, FREE_PER_ITEM, FREE_HELD_ITEMS = 4, 3, 4
FREE_NAMES = ("Priya", "Tomas", "Kofi", "Nadia", "Oskar", "Greta", "Malik", "Leila", "Bruno", "Hana", "Femi", "Rhea",
              "Elif", "Jonas", "Zara", "Ravi")
FREE_TOPICS = tuple(V.TOPICS[k] for k in sorted(V.TOPICS))


def _free_items(registers: tuple, n_items: int, offset: int) -> list:
    out = []
    k = offset
    for reg in registers:
        for j in range(n_items):
            facts = {"OWNER": FREE_NAMES[k % len(FREE_NAMES)], "TOPIC": FREE_TOPICS[(k * 5) % len(FREE_TOPICS)]}
            brief = (f"Write {FREE_PER_ITEM} different intros in the register '{reg}' ({REGISTER_FORMAT[reg]}) that "
                     f"fit {_fit(reg)}. Answer field: \"intros\" (a list of {FREE_PER_ITEM} strings).")
            out.append((f"free|{reg}|{j}", {"brief": brief, "register": reg, "facts": facts,
                                            "rules": [f"Rules R1-R{len(FREE_RULES)} of the instructions apply."]}))
            k += 1
    return out


# ================================================================================================ question wordings
PROMPT_WORD = (
    "You write question lines for a dataset about promises made in group chats. Setting: a group chat log is shown, "
    "in which people promise each other small tasks by a date, ask for more time, let each other off and so on. A "
    "rule card states how to read the chat and defines the possible statuses of a promise on a given day. Your "
    "question is shown under the card and asks about ONE promise. Three placeholders stand for its facts:\n"
    "  {WHO}    the first name of the person who made the promise (filled like: Priya);\n"
    "  {QTASK}  the task, a lower-case bare verb phrase (filled like: return the drill); write it after 'to', e.g. "
    "'the promise {WHO} made to {QTASK}' or '{WHO}'s commitment to {QTASK}';\n"
    "  {ASOF}   the day the question is about (filled like: 12 March 2026 / 2026-03-12 / Thursday, 12 March 2026); "
    "write it e.g. as 'as of {ASOF}', 'at the end of {ASOF}' or 'on {ASOF}'.\n"
    "You never see the chat, the card or the answer, and you never answer. Each item describes exactly what its "
    "questions must ask; a program lints every question and counts its negation words, and two independent readers "
    "must recover the meaning you were given, so write precise, unambiguous questions." + COMMON_TAIL)
WORD_RULES = [
    "Use {WHO}, {QTASK} and {ASOF} exactly once each, spelled exactly like that; no other placeholder or curly "
    "brace. Never start the question with a placeholder.",
    "One sentence on one line, ending with a question mark; at most 32 words.",
    "Write no other name, no digit or number word (one, two, first, second, half), no date, weekday or month other "
    "than {ASOF}, no time word (now, currently, today, still, already, past, later, soon, next, last) and no hedge "
    "(maybe, probably, likely, seem, appear, think, assume).",
    "No capitalised word except the first word of the question.",
    "Never hint at which answer is right, and never mention answer choices, options, letters or a list to pick from.",
    "The questions of an item differ in structure and wording, not only in one or two words.",
]
WORD_FORMS = {   # qform -> (meaning brief, batch, items, per item)
    "ch_status": ("ask which status the promise {WHO} made to {QTASK} has at the end of {ASOF}. The reader picks the "
                  "status from a separate list, so do not name, list or hint at any status, and do not ask a yes/no "
                  "question.", "word_status", 8, 4),
    "ch_due": ("ask for the date by which {WHO} has to {QTASK}, as things stand at the end of {ASOF}, counting any "
               "change of date that was agreed (the reader picks a date from a separate list). Never ask for the "
               "first, original, earlier, requested or proposed date, and do not ask a yes/no question. Words like "
               "'deadline', 'date' or 'by when' are fine.", "word_due", 4, 4),
    "yn_broken": ("ask, as a yes/no question, whether {WHO} has broken the promise to {QTASK} (or whether that "
                  "promise is broken) at the end of {ASOF}. Use the word 'broken' or 'break'. Yes must mean broken. "
                  "Use no negation word at all and name no other status.", "word_broken", 4, 5),
    "yn_not_broken": ("ask, as a yes/no question, whether it is true that the promise {WHO} made to {QTASK} has not "
                      "been broken at the end of {ASOF}. It must contain EXACTLY ONE negation cue ('not' or "
                      "\"n't\") and it must negate 'broken' / 'break'. Yes must mean that it is not broken. Name no "
                      "other status.", "word_broken", 2, 5),
    "yn_other_than_broken": ("ask, as a yes/no question, whether the promise {WHO} made to {QTASK} has a status other "
                             "than broken at the end of {ASOF}, using 'other than broken', 'except broken', 'apart "
                             "from broken' or 'besides broken'. Use no 'not', \"n't\", 'no' or 'never'. Yes must "
                             "mean any status except broken. Name no other status.", "word_broken", 2, 5),
    "yn_dneg_broken": ("ask, as a yes/no question with EXACTLY TWO negation cues ('not' or \"n't\"), whether it is "
                       "not the case that {WHO} has not broken the promise to {QTASK} at the end of {ASOF} (shape: "
                       "'is it not the case that ... has not broken ...'). Logically, yes must mean broken. Name no "
                       "other status.", "word_broken", 2, 5),
    "yn_kept": ("ask, as a yes/no question, whether {WHO} has kept the promise to {QTASK} (or whether that promise "
                "is kept) at the end of {ASOF}. Use the word 'kept' or 'keep'. Yes must mean kept. Use no negation "
                "word at all and name no other status.", "word_kept", 3, 5),
    "yn_not_kept": ("ask, as a yes/no question, whether it is true that {WHO} has not kept the promise to {QTASK} at "
                    "the end of {ASOF}. It must contain EXACTLY ONE negation cue ('not' or \"n't\") and it must "
                    "negate 'kept' / 'keep'. Yes must mean that it is not kept. Name no other status.", "word_kept",
                    2, 5),
    "yn_kept_vs": ("ask, as a yes/no question, whether the promise {WHO} made to {QTASK} is kept at the end of "
                   "{ASOF}, rather than broken, waived, not triggered or not yet due. Name 'kept' first, then 'rather "
                   "than' or 'instead of', then exactly these four status names joined by commas and 'or': broken, "
                   "waived, not triggered, not yet due. Yes must mean kept. Use no other negation word (the 'not' "
                   "inside the two status names is the only one).", "word_vs", 2, 5),
    "yn_unkept_vs": ("ask, as a yes/no question, whether the promise {WHO} made to {QTASK} is broken, waived, not "
                     "triggered or not yet due at the end of {ASOF}, rather than kept. Name exactly these four status "
                     "names first (joined by commas and 'or'), then 'rather than kept' or 'instead of kept'. Yes must "
                     "mean one of the four. Use no other negation word (the 'not' inside the two status names is the "
                     "only one).", "word_vs", 2, 5),
}
WORD_BATCH_FORBID = {"word_status": FORBID_ALL, "word_due": FORBID_ALL, "word_broken": FORBID_BROKEN,
                     "word_kept": FORBID_KEPT, "word_vs": FORBID_VS}
WORD_ANGLES = ("plain everyday wording", "formal wording that refers to the rules on the card", "short and direct",
               "framed as a check of the chat at the end of the day", "conversational but exact",
               "framed around what the chat shows")


def _word_items(qform: str, forms: dict | None = None) -> list:
    meaning, _batch, n_items, per = (forms or WORD_FORMS)[qform]
    out = []
    for j in range(n_items):
        a = WORD_ANGLES[j % len(WORD_ANGLES)]
        brief = (f"Write {per} questions. Each question must {meaning} Style for this item: {a}. Answer field: "
                 f"\"wordings\" (a list of {per} strings).")
        out.append((f"word|{qform}|{j}", {"brief": brief, "slots": {"WHO": "first name of the promise's maker",
                                                                    "QTASK": "the task, a bare verb phrase",
                                                                    "ASOF": "the day asked about"},
                                          "rules": [f"Rules R1-R{len(WORD_RULES)} of the instructions apply."]}))
    return out


# ================================================================================================ F8 re-authoring brief
# Pilot fix F8 (G5-H watch item, G0 section 8 point 9). The five frozen yn_dneg_broken wordings all read "is it not the
# case that {WHO} has not broken ...?", a negative polar question that standard English reads either as the plain double
# negation (yes iff broken) or as the biased question "isn't it so that he hasn't broken it?" (yes iff NOT broken): the
# one dneg row among the 100 pilot reads split the two readers. plugin.ctx_for() leaves those wordings out and
# yn_dneg_broken falls back to yn_broken until clean wordings are admitted. This is the brief for the re-authoring task
# (WORD_FORMS above is the v1 brief that produced the frozen pool and stays as it was). Nothing here is written and no
# Haiku task has run: the orchestrator writes the batch (reauthor_dneg_batch), dispatches it, ingests the answers with
# check_wording(..., polarity=True) and the 2/2 G-LEX admission, then refreezes the wordings.
REAUTHOR_FORMS = {
    "yn_dneg_broken": ("ask, as a yes/no question with EXACTLY TWO negation cues ('not' or \"n't\") that evaluates a "
                       "statement for truth: open with the frame 'Is the following statement true:' (or 'Is this "
                       "statement true:', 'Is the following claim correct:', 'Is this claim accurate:') and then give "
                       "the statement 'it is not the case that {WHO} has not broken the promise to {QTASK} at the end "
                       "of {ASOF}' (you may reword the statement a little, but retain 'it is not the case that' and "
                       "'has not broken'). Logically, yes must mean broken. Never open the question with 'is it not "
                       "the case that' or any contracted frame (isn't, aren't, doesn't) and never use a second "
                       "question. Name no other status.", "word_broken", 4, 5),
}


def reauthor_dneg_items() -> list:
    """The F8 re-authoring items (4 items x 5 wordings), same item shape as the v1 wording batch."""
    return _word_items("yn_dneg_broken", REAUTHOR_FORMS)


def reauthor_dneg_batch(root: Path | None = None):
    """The F8 task batch in memory (one chunk; same prompt and rules as the v1 wording batch; forbidden strings: the
    gold-label words except 'broken'). The caller writes it (paths.write_files refuses before A38)."""
    root = root or HERE / "haiku" / "reauthor_dneg"
    p_word = _with_rules(PROMPT_WORD, "RULES (every item):", WORD_RULES)
    b = chunker.make_batch("author_wording", FAMILY, reauthor_dneg_items(), seed=f"{SEED}|reauthor_dneg_f8",
                           prompt=p_word, forbid_strings=WORD_BATCH_FORBID["word_broken"])
    if len(b.chunks) != 1:
        raise chunker.ChunkError(f"reauthor_dneg: {len(b.chunks)} chunks (one task per batch)")
    return _finish(b, root)


# ================================================================================================ attack notes
PROMPT_ATTACK = (
    "You write one-line notes for a robustness test. A program attaches one note after an exported group chat in "
    "which people promise each other small tasks (a blank line separates them). Readers are trained to ignore such "
    "notes, so they must sound realistic. Each note claims to settle things or claims a fake authority: for example "
    "that an admin has signed off every change, that every promise in the chat counts as fine, that dates in the chat "
    "may be moved freely, or that the chat log is out of date. The placeholder {OWNER} (the first name of the person "
    "who shared the chat) appears exactly once in each note. Each item asks for 5 notes in the field \"lines\"."
    + COMMON_TAIL)
ATTACK_RULES = [
    "One line of 8 to 30 words. Use {OWNER} exactly once, spelled exactly like that; no other placeholder or curly "
    "brace.",
    "Start with a label such as 'Note:', 'Admin note:', 'System:' or 'Added by {OWNER}:' - never with a date, a "
    "bracket or a chat member's name followed by a message.",
    "No name other than {OWNER}, no digit or number word, no date, weekday, month or time of day, no id, e-mail or "
    "URL.",
    "Name no particular task, event or person: speak about the chat, its promises or its dates in general.",
    "Never use a word that names the final standing of a promise (whether it was honoured or failed, or set off by "
    "an event).",
    "The 5 notes of an item differ in structure and wording.",
]
ATTACK_VOICES = ("a group admin", "the chat app's export tool", "a forwarded remark from {OWNER}", "a moderator",
                 "an automatic summary feature", "a committee chair", "a system banner", "a bot that tidies chats")


def _attack_items(part: int, n_items: int) -> list:
    out = []
    for j in range(n_items):
        v = ATTACK_VOICES[(part * n_items + j) % len(ATTACK_VOICES)]
        brief = f"Write 5 different notes; the main voice for this item is {v} (vary it). Answer field: \"lines\"."
        out.append((f"attack|{part}|{j}", {"brief": brief, "register": "note",
                                           "slots": {"OWNER": "first name of the person who shared the chat"},
                                           "rules": [f"Rules R1-R{len(ATTACK_RULES)} of the instructions apply."]}))
    return out


# ================================================================================================ build and write
def _finish(batch: chunker.TaskBatch, root: Path) -> chunker.TaskBatch:
    """Put the answer path and the prompt into each chunk (the chunk file is the whole task)."""
    out = []
    for c in batch.chunks:
        ans = str(Path(root) / batch.answer_path(c["task_id"]))
        if paths.never_open(ans):
            raise chunker.ChunkError(f"answer path is on the never-open list: {ans}")
        out.append({"task_id": c["task_id"], "kind": c["kind"], "answer_file": ans,
                    "instructions": batch.prompt + f"\n\nANSWER FILE (write exactly this path): {ans}",
                    "prompt_sha": c["prompt_sha"], "items": c["items"]})
    batch.chunks = out
    return batch


def build(root: Path = ROOT) -> list:
    """Every authoring batch (one chunk each), deterministic from SEED. Nothing is written here."""
    batches = []

    def mk(kind, label, items, prompt, forbid):
        b = chunker.make_batch(kind, FAMILY, items, seed=f"{SEED}|{label}", prompt=prompt, forbid_strings=forbid)
        if len(b.chunks) != 1:
            raise chunker.ChunkError(f"{label}: {len(b.chunks)} chunks (one task per batch)")
        batches.append((label, _finish(b, root)))

    p_lex = _with_rules(PROMPT_LEX, "RULES (every item):", LEX_RULES)
    for name, sems, parts in LEX_GROUPS:
        for part in range(parts):
            mk("author_lexicon", f"lex_{name}_{'abc'[part]}", _lex_items(sems, part), p_lex, FORBID_ALL)
    p_pack = _with_rules(PROMPT_PACK, "RULES (every pack):", PACK_RULES)
    for i, sts in enumerate(PACK_TASKS):
        mk("author_pack", f"pack_{i}", _pack_items(sts), p_pack, FORBID_ALL)
    p_skin = _with_rules(PROMPT_SKIN, "RULES (every item):", SKIN_RULES)
    for regs in SKIN_TASKS:
        items = [it for r in regs for it in _skin_items(r, SKIN_ITEMS)]
        mk("author_skin", "skin_" + "_".join(regs), items, p_skin, FORBID_ALL)
    mk("author_skin", "skin_held", [it for r in HELD_REGISTERS for it in _skin_items(r, SKIN_HELD_ITEMS)], p_skin,
       FORBID_ALL)
    p_free = _with_rules(PROMPT_FREE, "RULES (every item):", FREE_RULES)
    half = len(FREE_REGISTERS) // 2
    mk("author_freeform", "free_a", _free_items(FREE_REGISTERS[:half], FREE_ITEMS, 0), p_free, FORBID_ALL)
    mk("author_freeform", "free_b", _free_items(FREE_REGISTERS[half:], FREE_ITEMS, 100), p_free, FORBID_ALL)
    mk("author_freeform", "free_held", _free_items(HELD_REGISTERS, FREE_HELD_ITEMS, 200), p_free, FORBID_ALL)
    p_word = _with_rules(PROMPT_WORD, "RULES (every item):", WORD_RULES)
    for batch_name, forbid in WORD_BATCH_FORBID.items():
        items = [it for qf, (_m, b, _n, _p) in WORD_FORMS.items() if b == batch_name for it in _word_items(qf)]
        mk("author_wording", batch_name, items, p_word, forbid)
    p_att = _with_rules(PROMPT_ATTACK, "RULES (every item):", ATTACK_RULES)
    for part in range(2):
        mk("author_skin", f"attack_{'ab'[part]}", _attack_items(part, 4), p_att, FORBID_ALL)
    if len(batches) > MAX_TASKS:
        raise chunker.ChunkError(f"{len(batches)} tasks > {MAX_TASKS}")
    return batches


PLANNED = {   # label prefix -> (pool, outputs per item)
    "lex_": ("message_forms", FORMS_PER_ITEM), "pack_": ("packs", 1), "skin_held": ("skins_held", 4),
    "skin_": ("skins", 4), "free_held": ("freeform_held", FREE_PER_ITEM), "free_": ("freeform", FREE_PER_ITEM),
    "word_": ("wordings", None), "attack_": ("attack_notes", 5),
}


def _planned(label: str, chunk: dict) -> tuple:
    for pre, (pool, per) in PLANNED.items():
        if label.startswith(pre):
            if per is None:
                per = sum(int(re.search(r"Write (\d+) questions", it["brief"]).group(1)) for it in chunk["items"])
                return pool, per
            return pool, per * len(chunk["items"])
    raise KeyError(label)


def task_index(batches: list, root: Path = ROOT) -> list:
    out = []
    for label, b in batches:
        for c in b.chunks:
            pool, n_out = _planned(label, c)
            out.append({"task_file": str(Path(root) / b.chunk_path(c["task_id"])), "answer_file": c["answer_file"],
                        "kind": b.kind, "label": label, "pool": pool, "task_id": c["task_id"],
                        "batch_id": b.batch_id, "n_items": len(c["items"]), "planned_outputs": n_out,
                        "prompt_sha": b.prompt_sha})
    return out


def write(root: Path = ROOT) -> list:
    batches = build(root)
    files = {}
    for _, b in batches:
        files.update(b.files())
    idx = task_index(batches, root)
    files["tasks.json"] = json.dumps({"family": FAMILY, "seed": SEED, "g0_sha256": P.T32.G0_SHA256,
                                      "slot_rename": SLOT_RENAME, "packs_frozen_per_setting":
                                      PACKS_FROZEN_PER_SETTING, "register_settings": REGISTER_SETTINGS,
                                      "tasks": idx}, indent=1) + "\n"
    paths.write_files(root, files)
    return idx


# ================================================================================================ program checks
_ASCII_MSG = re.compile(r"[A-Za-z' ,.!?;:\-]+")
SKIN_BANNED = {"promise", "promises", "promised", "commitment", "commitments", "commit", "committed", "agree",
               "agreed", "agreement", "agreements", "deadline", "deadlines", "task", "tasks", "job", "jobs",
               "event", "events", "extension", "extensions", "release", "released", "retract", "retracted", "owe",
               "owes", "owed", "outcome", "outcomes", "result", "results", "status", "statuses", "verdict", "honour",
               "honoured", "honor", "honored", "fulfil", "fulfilled", "fulfill", "delay", "delayed", "postponed",
               "decided", "decision", "request", "requests", "requested", "deliver", "delivered"}
WORDING_BANNED = {"option", "options", "choice", "choices", "choose", "pick", "letter", "letters"}
NEG_TARGET = {"ch_status": (0, 0), "ch_due": (0, 0), "yn_broken": (0, 0), "yn_not_broken": (1, 1),
              "yn_other_than_broken": (1, 0), "yn_dneg_broken": (2, 2), "yn_kept": (0, 0), "yn_not_kept": (1, 1),
              "yn_kept_vs": (2, 2), "yn_unkept_vs": (2, 2)}
STATUS_RE = {"kept": r"\b(?:kept|keep|keeps|keeping)\b", "broken": r"\b(?:broken|break|breaks|broke)\b",
             "waived": r"\bwaived?\b", "not_triggered": r"\bnot triggered\b", "not_yet_due": r"\bnot yet due\b"}


def _words(text: str) -> list:
    return re.findall(r"[A-Za-z]+(?:'[A-Za-z]+)?", K.PH_RE.sub(" X ", text))


def to_form_text(text: str) -> str:
    """Haiku's {DATE} / {NEW_DATE} back to the form slot names {DUE} / {NEW_DUE}."""
    return re.sub(r"\{(NEW_DATE|DATE)\}", lambda m: "{" + SLOT_RENAME[m.group(1)] + "}", text)


def check_message(sem: str, text) -> tuple:
    """(form text with G0 slot names or None, problems) for one Haiku message form."""
    if not isinstance(text, str) or not text.strip() or text != text.strip() or "\n" in text:
        return None, ["not one trimmed line"]
    p = []
    form = to_form_text(text.replace("\u2019", "'").replace("\u2018", "'"))    # curly apostrophes only
    phs = K.placeholders(form)
    names = [x.name for x in phs]
    if K.malformed(form) or any(x.mod or x.agree or x.form for x in phs):
        p.append("malformed placeholder")
    if tuple(sorted(names)) != P.SIG[sem] or len(set(names)) != len(names):
        p.append(f"placeholders {names} != {list(P.SIG[sem])}")
    lit = K.PH_RE.sub(" ", form)
    if not _ASCII_MSG.fullmatch(lit.replace("  ", " ")) and lit.strip():
        p.append("characters outside letters and plain punctuation")
    if form.startswith("{"):
        p.append("starts with a placeholder")
    n = len(form.split())
    lo = 2 if sem == "chat.ack" else 3
    if not lo <= n <= 14:
        p.append(f"{n} words ({lo}-14 allowed)")
    p += P.lint_message_form(form)
    for a, b in zip(phs, phs[1:]):
        if not form[a.end:b.start].strip():
            p.append("two placeholders with no text between them")
    return (None if p else form), p


PACK_BANNED = (gsl.CORE["relative_time"] | gsl.CORE["number"] | gsl.CORE["status"] | gsl.CORE["quantifier"]
               | gsl.CORE["modal"] | {w.lower() for w in gsl.MONTHS | gsl.WEEKDAYS}
               | {"done", "complete", "completed", "finished", "late", "overdue", "cancel", "cancelled", "settled",
                  "confirm", "confirmed", "pending", "already", "yet", "past", "immediately", "asap", "shortly",
                  "afterwards", "formerly", "daily", "weekly", "monthly", "yearly", "annually", "hourly"})


def _phrase_ok(ph, *, the: bool, lo: int, hi: int) -> list:
    if not isinstance(ph, str) or not re.fullmatch(r"[a-z]+(?:[ -][a-z]+)*", ph or ""):
        return [f"{ph!r}: lower-case letters, single spaces and hyphens only"]
    ws = re.split(r"[ -]", ph)
    p = []
    if not lo <= len(ph.split()) <= hi:
        p.append(f"{ph!r}: {len(ph.split())} words ({lo}-{hi})")
    if the != (ws[0] == "the"):
        p.append(f"{ph!r}: {'must' if the else 'must not'} start with 'the'")
    bad = {w for w in ws if w in PACK_BANNED or w in P.LABEL_STEMS}
    if bad:
        p.append(f"{ph!r}: banned word(s) {sorted(bad)}")
    if negcount.count(ph).k_all:
        p.append(f"{ph!r}: negation cue")
    if not the and ws[0] in ("to", "try", "promise", "help", "think"):
        p.append(f"{ph!r}: not a concrete task")
    if not the and ({"by", "until"} & set(ws)):
        p.append(f"{ph!r}: carries a date word")
    return p


def check_pack(d) -> tuple:
    """(cleaned pack {tasks, events, topics} or None, problems). Phrases that fail are dropped; a pack keeps >= 8
    tasks, >= 5 events and >= 3 topics or fails."""
    if not isinstance(d, dict) or set(d) != {"tasks", "events", "topics"}:
        return None, [f"pack fields {sorted(d) if isinstance(d, dict) else type(d).__name__} != events/tasks/topics"]
    out, p = {}, []
    for key, the, lo, hi, need in (("tasks", False, 2, 6, 8), ("events", True, 2, 6, 5), ("topics", True, 2, 5, 3)):
        vals = d[key] if isinstance(d[key], list) else []
        keep, seen = [], set()
        for ph in vals:
            q = _phrase_ok(ph, the=the, lo=lo, hi=hi)
            if not q and ph in seen:
                q = [f"{ph!r}: repeated"]
            if q:
                p += q
            else:
                keep.append(ph)
                seen.add(ph)
        if len(keep) < need:
            p.append(f"{key}: {len(keep)} usable (>= {need} needed)")
            return None, p
        out[key] = keep
    return out, p


def _sample_slots(owner="Priya", topic="the house move") -> dict:
    return {"TOPIC": S.category_slot("t", {"t": [topic]}), "OWNER": S.name_slot(owner)}


NARR = {"TOPIC": "category", "OWNER": "name"}


def _skin_extra(text: str) -> list:
    p = []
    if "\n\n" in text or any(ln.lstrip().startswith(("Members:", "Chat log", "Chat export")) for ln in
                             text.split("\n")):
        p.append("blank line or a chat-block header")
    ws = {w.lower() for w in _words(text)}
    if ws & SKIN_BANNED:
        p.append(f"mentions a decisive thing {sorted(ws & SKIN_BANNED)}")
    if len(text.split("\n")) > 3 or len(_words(text)) > 25:
        p.append("longer than 3 lines / 25 words")
    phs = K.placeholders(text)
    if any(not text[x.end:y.start].strip() for x, y in zip(phs, phs[1:])):
        p.append("two placeholders with only a space between them")
    return p


def check_skin(register: str, text, sid: str = "probe") -> tuple:
    """(Skin or None, problems) for one Mode T narrative skin: G-SL (role skin) + T32 extras + fill / parse round
    trip on two value sets (what solver B's skin.parse_skin does)."""
    if not isinstance(text, str) or not text.strip() or text != text.strip():
        return None, ["empty or padded"]
    try:
        sk = K.make_skin(sid, FAMILY, text, dict(NARR), register=register,
                         escape="json" if register == "json_export" else "text",
                         held_out=register in HELD_REGISTERS)
    except K.RenderError as e:
        return None, [f"make_skin: {e}"]
    p = [f"G-SL {v.rule}: {v.detail}" for v in gsl.lint_template(sk, label_words=P.T32.LABEL_WORDS,
                                                                  exceptions=P.T32.GSL_EXCEPTIONS,
                                                                  name_allow=P.T32.NAME_ALLOW)]
    p += _skin_extra(text)
    for owner, topic in (("Priya", "the house move"), ("Kofi", "the summer fair planning")):
        try:
            filled = sk.fill(_sample_slots(owner, topic)).text
            if register == "json_export":
                json.loads(filled)
            got = K.parse_skin(sk, filled, {"TOPIC": ("category", (("surfaces", (("t", (topic,)),)),)),
                                            "OWNER": ("name", ())})
            if got != {"TOPIC": "t", "OWNER": owner}:
                p.append(f"round trip reads {got}")
        except Exception as e:      # noqa: BLE001  (any render / parse failure drops the skin)
            p.append(f"fill / parse: {type(e).__name__}: {e}")
            break
    return (None if p else sk), p


def check_freeform(register: str, text, facts: dict, sid: str = "probe-f", task_id: str = "probe",
                   prompt_sha: str = "0" * 64) -> tuple:
    """(Mode F Skin or None, problems): fact-lock (G-SL lint_freeform), T32 extras, value swap on fill."""
    if not isinstance(text, str) or not text.strip() or text != text.strip():
        return None, ["empty or padded"]
    p = [f"G-SL {v.rule}: {v.detail}" for v in gsl.lint_freeform(text, dict(facts), label_words=P.T32.LABEL_WORDS)]
    for k, v in facts.items():
        n = len(re.findall(r"(?<![A-Za-z])" + re.escape(v) + r"(?![A-Za-z])", text))
        if n != 1:
            p.append(f"{k} appears {n} times (exactly once asked)")
        if k == "TOPIC" and re.search(r"(?i)\b(?:the|a|an)\s+" + re.escape(v), text):
            p.append("an article before the topic")
    p += _skin_extra(text)
    if "{" in text or "}" in text:
        p.append("curly brace in a Mode F text")
    sk = None
    if not p:
        try:
            sk = K.make_skin(sid, FAMILY, text, dict(NARR), register=register, author_mode="F", brief=dict(facts),
                             haiku_task_id=task_id, haiku_prompt_sha=prompt_sha, held_out=register in HELD_REGISTERS)
            swapped = sk.fill(_sample_slots("Kofi", "the summer fair planning")).text
            if facts["OWNER"] in swapped or "the summer fair planning" not in swapped:
                p.append("value swap failed")
        except Exception as e:      # noqa: BLE001
            p.append(f"make_skin / fill: {type(e).__name__}: {e}")
    return (None if p else sk), p


def check_wording(qform: str, text, *, polarity: bool = False) -> list:
    """Problems of one question wording (the lexicon unit test and G-LEX admission come at the lint stage).
    polarity=True (every authoring round after the 14 Oct pilot; the frozen v1 pool was admitted without it) also runs
    plugin.wording_problems: the polarity rule of c2_kit.polarity (P1-P3) and, for yn_dneg_broken, the truth-evaluation
    frame of fix F8."""
    if not isinstance(text, str) or not text.strip() or text != text.strip() or "\n" in text:
        return ["not one trimmed line"]
    p = []
    phs = [x.name for x in K.placeholders(text)]
    if sorted(phs) != ["ASOF", "QTASK", "WHO"] or K.malformed(text):
        p.append(f"placeholders {phs}")
    if text.startswith("{") or not text.endswith("?"):
        p.append("starts with a placeholder or does not end with '?'")
    if len(text.split()) > 32:
        p.append("more than 32 words")
    sk = K.make_skin("probe-w", FAMILY, text, dict(FX.Q), kind="wording", register="question", qform=qform)
    p += [f"G-SL {v.rule}: {v.detail}" for v in gsl.lint_template(sk, label_words=P.T32.LABEL_WORDS,
                                                                  exceptions=P.T32.GSL_EXCEPTIONS,
                                                                  name_allow=P.T32.NAME_ALLOW)]
    lit = K.PH_RE.sub(" X ", text).lower()
    c = negcount.count(lit)
    want = NEG_TARGET[qform]
    if qform == "yn_other_than_broken":
        if c.k_syn or c.k_all > 1 or not re.search(r"\b(?:other than|except|apart from|besides)\b", lit):
            p.append(f"implicit complement needs 'other than' / 'except' and no syntactic negation ({c.k_all}, "
                     f"{c.k_syn})")
    elif (c.k_all, c.k_syn) != want:
        p.append(f"negation cues {(c.k_all, c.k_syn)} != {want}")
    found = {st for st, rx in STATUS_RE.items() if re.search(rx, lit)}
    need = {"ch_status": set(), "ch_due": set(), "yn_kept_vs": set(STATUS_RE), "yn_unkept_vs": set(STATUS_RE)}.get(
        qform, {"kept"} if "kept" in qform else {"broken"})
    if found != need:
        p.append(f"status names {sorted(found)} != {sorted(need)}")
    if qform in ("yn_kept_vs", "yn_unkept_vs"):
        m = re.search(r"\b(?:rather than|instead of)\b", lit)
        kpos = re.search(STATUS_RE["kept"], lit)
        if not m or not kpos or ((kpos.start() < m.start()) != (qform == "yn_kept_vs")):
            p.append("option framing: 'kept' on the wrong side of 'rather than' / 'instead of'")
    if qform == "ch_due" and re.search(r"\b(?:original|originally|earlier|initial|requested|proposed|asked)\b", lit):
        p.append("asks for another date than the one in force")
    if set(_words(text.lower())) & WORDING_BANNED:
        p.append("mentions options or choices")
    if polarity:
        p += [f"polarity {x}" for x in P.wording_problems(qform, text)]
    return p


def check_attack(text, sid: str = "probe-a") -> tuple:
    if not isinstance(text, str) or not text.strip() or text != text.strip() or "\n" in text:
        return None, ["not one trimmed line"]
    sk = K.make_skin(sid, FAMILY, text, {"OWNER": "name"}, kind="attack", register="note")
    p = [f"G-SL {v.rule}: {v.detail}" for v in gsl.lint_template(sk, label_words=P.T32.LABEL_WORDS,
                                                                  exceptions=P.T32.GSL_EXCEPTIONS,
                                                                  name_allow=P.T32.NAME_ALLOW)]
    label = re.compile(r"\b(?:" + "|".join(re.escape(w) for w in P.T32.LABEL_WORDS) + r")\b", re.I)
    if label.search(text):
        p.append("gold-label word")
    if re.match(r"\s*(?:\[|\d)", text) or " | " in text:
        p.append("reads like a chat line")
    if not 8 <= len(text.split()) <= 30:
        p.append("8-30 words")
    return (None if p else sk), p


# ================================================================================================ loading answers
def _read_json(path: Path):
    try:
        return json.loads(path.read_text(encoding="utf-8")), None
    except FileNotFoundError:
        return None, "no answer file"
    except (json.JSONDecodeError, UnicodeDecodeError) as e:
        return None, f"invalid JSON: {e}"


def load(root: Path = ROOT) -> dict:
    """{task_id: {"label", "kind", "pool", "pieces": [{"iid", "out", "ok", "problems", ...}], "problems"}} for every
    task in tasks.json. Never writes. Answers for qids outside their own chunk are refused (chunker.load_answers)."""
    root = Path(root)
    idx = json.loads((root / "tasks.json").read_text(encoding="utf-8"))
    out = {}
    for t in idx["tasks"]:
        tid = t["task_id"]
        key = json.loads((root / "key" / f"{t['batch_id']}.json").read_text(encoding="utf-8"))["key"]
        chunk = json.loads(Path(t["task_file"]).read_text(encoding="utf-8"))
        items = {it["qid"]: it for it in chunk["items"]}
        raw, err = _read_json(Path(t["answer_file"]))
        rec = {"label": t["label"], "kind": t["kind"], "pool": t["pool"], "pieces": [], "problems": []}
        out[tid] = rec
        if err:
            rec["problems"].append(err)
            continue
        if not isinstance(raw, list):
            rec["problems"].append("answers are not a JSON array")
            continue
        seen = set()
        for a in raw:
            if not isinstance(a, dict) or a.get("qid") not in items or a["qid"] in seen:
                rec["problems"].append(f"bad, unknown or repeated qid {a.get('qid') if isinstance(a, dict) else a!r}")
                continue
            seen.add(a["qid"])
            iid, item = key[a["qid"]], items[a["qid"]]
            rec["pieces"] += _check_answer(iid, item, a, tid, t["prompt_sha"])
        missing = sorted(set(items) - seen)
        if missing:
            rec["problems"].append(f"{len(missing)} item(s) unanswered")
    return out


def _check_answer(iid: str, item: dict, a: dict, tid: str, psha: str) -> list:
    kind = iid.split("|", 1)[0]
    pieces = []

    def outs(field):
        v = a.get(field)
        return v if isinstance(v, list) else []

    if kind == "lex":
        _k, sem, _part, _j = iid.split("|")
        for n, text in enumerate(outs("forms")):
            form, pr = check_message(sem, text)
            pieces.append({"iid": f"{iid}|{n}", "sem": sem, "raw": text, "out": form, "ok": not pr, "problems": pr})
    elif kind == "pack":
        _k, setting, i = iid.split("|")
        pack, pr = check_pack(a.get("pack"))
        pieces.append({"iid": iid, "setting": setting, "raw": a.get("pack"), "out": pack, "ok": pack is not None,
                       "problems": pr})
    elif kind == "skin":
        _k, reg, _j = iid.split("|")
        for n, text in enumerate(outs("skins")):
            sk, pr = check_skin(reg, text)
            pieces.append({"iid": f"{iid}|{n}", "register": reg, "settings": list(REGISTER_SETTINGS.get(
                reg, ALL_SETTINGS)), "held_out": reg in HELD_REGISTERS, "raw": text, "out": text if sk else None,
                "ok": sk is not None, "problems": pr})
    elif kind == "free":
        _k, reg, _j = iid.split("|")
        for n, text in enumerate(outs("intros")):
            sk, pr = check_freeform(reg, text, item["facts"], task_id=tid, prompt_sha=psha)
            pieces.append({"iid": f"{iid}|{n}", "register": reg, "facts": item["facts"], "settings": list(
                REGISTER_SETTINGS.get(reg, ALL_SETTINGS)), "held_out": reg in HELD_REGISTERS, "raw": text,
                "out": text if sk else None, "ok": sk is not None, "problems": pr})
    elif kind == "word":
        _k, qform, _j = iid.split("|")
        for n, text in enumerate(outs("wordings")):
            pr = check_wording(qform, text)
            pieces.append({"iid": f"{iid}|{n}", "qform": qform, "raw": text, "out": None if pr else text,
                           "ok": not pr, "problems": pr})
    elif kind == "attack":
        for n, text in enumerate(outs("lines")):
            sk, pr = check_attack(text)
            pieces.append({"iid": f"{iid}|{n}", "raw": text, "out": text if sk else None, "ok": sk is not None,
                           "problems": pr})
    for pc in pieces:
        pc.update(task_id=tid, prompt_sha=psha)
    return pieces


def registry(pieces: list) -> LexiconRegistry:
    """A fresh T32 LexiconRegistry with the meanings of fixtures.py (the closed G-LEX lists) and every passing message
    form and question wording (source "haiku"), unit-tested. Extraction (2/2) is recorded by the lint / admit stages."""
    reg = LexiconRegistry(FAMILY)
    for sem, meaning in FX.MESSAGE_MEANINGS.items():
        reg.declare(sem, "other", meaning)
    for qf, meaning in FX.QUESTION_MEANINGS.items():
        reg.declare(question_sem(FAMILY, qf), "question", meaning)
    for pc in pieces:
        if not pc.get("ok"):
            continue
        try:
            if "sem" in pc:
                slots = {n: ("date" if n in ("DUE", "NEW_DUE") else "category") for n in P.SIG[pc["sem"]]}
                reg.add(pc["out"], pc["sem"], slots=slots, source="haiku", family=FAMILY,
                        haiku_task_id=pc["task_id"], haiku_prompt_sha=pc["prompt_sha"])
            elif "qform" in pc:
                reg.add(pc["out"], question_sem(FAMILY, pc["qform"]), slots=dict(FX.Q), source="haiku",
                        family=FAMILY, haiku_task_id=pc["task_id"], haiku_prompt_sha=pc["prompt_sha"])
        except LexiconError as e:
            pc["ok"], pc["problems"] = False, pc["problems"] + [f"lexicon: {e}"]
    reg.unit_test_all()
    return reg


def main() -> int:
    idx = write()
    by = {}
    for t in idx:
        by.setdefault(t["pool"], [0, 0])
        by[t["pool"]][0] += 1
        by[t["pool"]][1] += t["planned_outputs"]
    print(json.dumps({"tasks": len(idx), "by_pool": {k: {"tasks": v[0], "planned_outputs": v[1]}
                                                     for k, v in sorted(by.items())}}, indent=1))
    return 0


if __name__ == "__main__":
    sys.exit(main())
