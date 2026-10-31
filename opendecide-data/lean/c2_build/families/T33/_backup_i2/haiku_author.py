"""families/T33/haiku_author.py: the T33 Haiku pools (G0_SPEC section 3; C2_DATA_SPEC 3.0, 3.3, 6.4; A37 b).

Haiku writes wording only: packs (tool namespaces), context skins (sub-form a), final-message skins (sub-form b),
attack lines, claim paraphrases, check paraphrases and question wordings. It never sees a log line, a value, a claim
verdict, a question with its options, or a gold; it never sets a label. Every piece goes through G-SL (skins), G-LEX
(lexicon forms and wordings: unit test + 2/2 blind extraction against meaning lists that include decoys) and the
row gates later. Run from lean/c2_build:

  ../../.venv/bin/python -m families.T33.haiku_author write-tasks      # stage Resolve: authoring chunks (<= 40)
  ../../.venv/bin/python -m families.T33.haiku_author write-tasks-dneg # fix iteration 1: the yn_dneg_* wording chunks
  ../../.venv/bin/python -m families.T33.haiku_author lint             # stage Lint: load answers, G-SL, unit tests
  ../../.venv/bin/python -m families.T33.haiku_author extract-tasks    # stage Lint: G-LEX reads, one chunk per read
  ../../.venv/bin/python -m families.T33.haiku_author admit            # stage Admit: record reads, freeze pools/

Every task file is a chunk written by c2_kit.chunker.make_batch through paths.write_files; it carries its own
instructions and the absolute path of the one answer file the agent writes (TaskBatch.answer_path), so a Haiku agent
reads exactly one file. Authoring prompts and items refuse the T33 label words and the program's question and option
strings (chunker forbid_strings). Nothing here writes before A38 (the kit's writers refuse).
"""
from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
from collections import Counter
from pathlib import Path

from c2_kit import chunker, gsl, paths
from c2_kit import polarity as POL
from c2_kit import slots as S
from c2_kit.lexicon import LexiconError, LexiconRegistry, question_sem
from c2_kit.plugin import KitCtx
from c2_kit.skin import RenderError, make_skin, placeholders

import negcount  # noqa: E402  (c_src/common, put on sys.path by c2_kit.paths)

from . import fixtures as FX
from . import plugin as T

HERE = Path(__file__).resolve().parent
HAIKU = HERE / "haiku"
AUTHOR = HAIKU / "author"
EXTRACT = HAIKU / "extract"
POOLS = HERE / "pools"
F = T.FAMILY
VERSION = "v1"

# ---------------------------------------------------------------------------------------------- what Haiku must not see
LABEL_WORDS = T.T33Plugin.LABEL_WORDS
QUESTION_STRINGS = (tuple(text for _w, _q, text in FX.WORDINGS) + tuple(T.VERDICT_TEXT.values())
                    + (T.NONE_CHECK, T.NONE_CLAIM, "The claim about"))
FORBID = LABEL_WORDS + QUESTION_STRINGS

# ------------------------------------------------------------------------------------------------ G-LEX meaning lists
# Production sems (the plugin draws f"claim.{verb}", the five crit.* sems and question_sem(F, qform)). Decoys (x_*)
# have no forms: they sit in the blind extraction's meaning list so that a paraphrase with an exclusive bound, a
# completion reading, an error-status reading or a scope error is picked as the decoy and rejected (amb:T33 R5, R6,
# R24, R25).
CHECK_SEMS = {
    "crit.finished": "the step is done under the log rules",
    "crit.amount_match": "the amount in the step's logged result equals the requested amount",
    "crit.all_written": "the rows_written in the step's logged result equals the requested row count",
    "crit.max_tries": "the step used at most the stated number of tries; using exactly that number still passes",
    "crit.max_duration": ("the duration_ms on the job's last poll is at most the stated number of seconds; exactly "
                          "that number still passes"),
}
CHECK_DECOYS = {
    "crit.x_tries_lt": "the step used fewer tries than the stated number; using exactly that number does not pass",
    "crit.x_duration_lt": ("the job ran for less time than the stated number of seconds; exactly that number does "
                           "not pass"),
    "crit.x_value_done": "the step was carried out for the full requested amount or row count",
    "crit.x_no_error": "the step's log shows no error status",
}
CHECK_SLOTS = {"crit.max_tries": {"R": "count"}, "crit.max_duration": {"D": "count"}}
CLAIM_SEMS = {
    "refund": "the agent says it refunded an amount of money for the target",
    "charge": "the agent says it charged an amount of money to the target",
    "credit": "the agent says it added a credit of an amount of money to the target",
    "payout": "the agent says it paid out an amount of money to the target",
    "import": "the agent says it imported a number of rows into the target",
    "export": "the agent says it exported a number of rows from the target",
    "sync": "the agent says it synced a number of rows to the target",
    "send": "the agent says it sent a message to the target",
    "book": "the agent says it booked the target",
    "cancel": "the agent says it cancelled the target",
    "update": "the agent says it updated the target",
}
CLAIM_DECOYS = {
    "claim.x_attempt": "the agent says only that it tried or started an action, without saying the action happened",
    "claim.x_request": "the agent says an action was asked for or is planned, without saying it happened",
}
VALUE_KIND = {v: ("cents" if a == "money" else "count") for v, a in T.VERB_ARCH.items() if a in T.VALUE_ARCH}
QUESTION_SEMS = {
    "yn_step_ok": "asks whether the step meets its success criterion (a plain positive question)",
    "yn_step_failed": ("asks whether the step fails its success criterion, with a verb such as fails, misses or "
                       "breaks (no 'not', no 'fails to')"),
    "yn_step_fail_to": "asks whether the step fails to meet its success criterion, with a phrase such as 'fails to'",
    "yn_step_not_ok": "asks whether the step does not meet its success criterion, with the word 'not'",
    "yn_dneg_step_ok": ("asks whether it is not true that the step does not meet its success criterion: an outer "
                        "'is it not true that' (or 'is it not the case that') and a second 'not' on meeting the "
                        "criterion, so a yes means the step meets its criterion"),
    "ch_failed_check": "asks which of the listed checks the step fails",
    # G0 section 7 (redo2, B5): no meaning quotes a program verdict, option or question string (FORBID), so the
    # FORBID screen of a G-LEX item no longer holds every question form; "backs up" = the card's "supported"
    "yn_all_supported": "asks whether the log backs up every claim in the message (a plain positive question)",
    "yn_any_bad": ("asks whether the log contradicts some claim in the message, or some claim names a target missing "
                   "from the log"),
    "yn_not_all_supported": ("asks whether it is not true that the log backs up every claim in the message, with the "
                             "word 'not'"),
    "yn_dneg_all_supported": ("asks whether it is not true that not every claim in the message is backed up by the "
                              "log: an outer 'is it not true that' (or 'is it not the case that') and a second 'not' "
                              "before every / all, so a yes means the log backs up every claim"),
    "ch_bad_claim": ("asks which claim in the message the log contradicts, or which claim names a target missing from "
                     "the log"),
    "ch_claim_verdict": "asks what the log shows about one claim, named by its target",
}
QUESTION_DECOYS = {
    "q.t33.x_error_status": "asks whether the step's log shows an error status code",
    "q.t33.x_job_state": "asks whether the step's job ended in the state succeeded",
    "q.t33.x_done_only": "asks whether the step's work was done, whatever the other checks say",
    "q.t33.x_none_supported": "asks whether the log backs up none of the claims in the message",
    "q.t33.x_message_omits": "asks whether the message leaves out a step that appears in the log",
}
# wording slots and the negation counts each question form must have (G-TW complement rules: a positive, antonym or
# option-framing form adds no cue; implicit adds one implicit cue; syntactic adds one syntactic cue)
WORDING_SLOTS = {q: ({"STEP": "count"} if T.SUB_OF[q] == "a" else {}) for q in T.SUB_OF}
WORDING_SLOTS["ch_claim_verdict"] = {"TARGET": "id"}
NEG_COUNTS = {q: (0, 0) for q in T.SUB_OF}
NEG_COUNTS.update(yn_step_fail_to=(1, 0), yn_step_not_ok=(1, 1), yn_not_all_supported=(1, 1),
                  yn_dneg_step_ok=(2, 2), yn_dneg_all_supported=(2, 2))
# the double-negation forms carry the explicit outer frame (polarity rule P3 / P4: no contracted "isn't it ...")
_OUTER = r"\bit not (?:the case|true|so|correct|accurate|right|fair)\b"
WORDING_MUST = {"yn_step_ok": r"criteri", "yn_step_failed": r"criteri", "yn_step_fail_to": r"criteri",
                "yn_step_not_ok": r"criteri", "ch_failed_check": r"check",
                "yn_not_all_supported": r"\bnot (?:every|all)\b", "yn_any_bad": r"contradict",
                "ch_bad_claim": r"contradict", "ch_claim_verdict": r"claim",
                "yn_dneg_step_ok": r"(?=.*" + _OUTER + r")(?=.*criteri)(?=.*\bnot (?:meet|satisf|reach|clear|pass|hold))",
                "yn_dneg_all_supported": r"(?=.*" + _OUTER + r")(?=.*\bnot (?:every|all)\b)"}
WORDING_BAN = r"\b(?:ok|okay|leaves? out|left out|omit\w*|first|last)\b"

# ------------------------------------------------------------------------------------------------ pool targets
# Rows: ~3,600 generated (2,400 selected), half per sub-form. Spec 3.0: a skin feeds <= 6 rows, each register
# <= 15% of rows, >= 30 wordings each <= 2% of the family (G11: no skin or template above 2%); >= 25 packs.
TARGETS = {
    "packs": 25,
    "context_train": 300, "context_per_register": 60, "context_held_out": 30,
    "message_train_n2": 125, "message_train_n3": 150, "message_train_n4": 30, "message_held_out": 30,
    "attack": 50,
    "claim_per_verb": 6,
    "check": {"crit.finished": 25, "crit.amount_match": 6, "crit.all_written": 6, "crit.max_tries": 13,
              "crit.max_duration": 9},
    "wording": {"yn_step_ok": 7, "yn_step_failed": 4, "yn_step_fail_to": 2, "yn_step_not_ok": 4,
                "ch_failed_check": 13, "yn_all_supported": 7, "yn_any_bad": 4, "yn_not_all_supported": 3,
                "ch_bad_claim": 6, "ch_claim_verdict": 9, "yn_dneg_step_ok": 8, "yn_dneg_all_supported": 8},
}
PER_ITEM = 6                       # skins per skin item
FORMS_PER_ITEM = 6                 # forms per lexicon / wording item
CONTEXT_ITEMS = {"task_ticket": 24, "runbook": 24, "chat_request": 24, "email_request": 24, "incident_channel": 16}
MESSAGE_ITEMS = {2: 8, 3: 9, 4: 3}                      # per training voice
MESSAGE_ITEMS_HELD = {2: 5, 3: 6, 4: 3}                 # ticket_thread (held out)
ATTACK_ITEMS = 16
CLAIM_ITEMS_PER_VERB = 3
CHECK_ITEMS = {"crit.finished": 9, "crit.amount_match": 4, "crit.all_written": 4, "crit.max_tries": 6,
               "crit.max_duration": 5}
WORDING_ITEMS = {"yn_step_ok": 4, "yn_step_failed": 3, "yn_step_fail_to": 3, "yn_step_not_ok": 3,
                 "ch_failed_check": 7, "yn_all_supported": 4, "yn_any_bad": 3, "yn_not_all_supported": 3,
                 "ch_bad_claim": 4, "ch_claim_verdict": 5, "yn_dneg_step_ok": 4, "yn_dneg_all_supported": 4}
MAX_TASKS = 40
# length (C2 spec 3.0 mean <= 800 tokens; pilot F5): skins are short. The frozen pools are not re-authored here; the
# brief and the loader apply these limits to any new authoring round (the frozen skins are mostly under 25 words)
MAX_CONTEXT_WORDS = 25
MAX_MESSAGE_WORDS = 40
TRAIN_VOICES = tuple(r for r in T.B_REGISTERS if r not in T.T33Plugin.HELD_OUT_REGISTERS)
HELD_VOICES = tuple(r for r in T.B_REGISTERS if r in T.T33Plugin.HELD_OUT_REGISTERS)
VERBS = {"money": ("refund", "charge", "credit", "payout"), "bulk": ("import", "export", "sync"),
         "action": ("send", "book", "cancel", "update")}
KINDS = tuple(T.TARGET_MAKERS)
# register names as Haiku sees them: "support_agent" holds the label word "support" (chunker forbid_strings)
ALIAS = {"support_agent": "customer_service_agent"}
UNALIAS = {v: k for k, v in ALIAS.items()}
DOMAINS = (
    "a neighbourhood bike repair shop", "a regional ferry operator", "a veterinary clinic chain",
    "a community theatre box office", "a craft brewery distributor", "a dental practice group",
    "a university library", "a solar panel installer", "a city parking office", "a language school",
    "an event catering company", "a freight forwarding firm", "an outdoor gear rental chain", "a pharmacy chain",
    "a music lessons studio", "a co-working space operator", "a farm produce co-op", "a museum gift shop",
    "a plumbing contractor", "a game tournament organiser", "a translation agency", "a boat marina",
    "a ski lift and lodge operator", "a bakery franchise", "a print shop", "a car wash chain",
    "a home cleaning service", "a furniture upholstery workshop", "a pet insurance provider",
    "a mobile game studio", "a tutoring marketplace", "a recycling depot", "a wedding planning agency",
    "a yoga studio network", "a bookshop chain", "an electric scooter rental service", "a plant nursery",
    "a hostel chain", "a concert ticket seller", "a laboratory supplies wholesaler",
)
REGISTER_TEXT = {
    "task_ticket": "a work ticket in a task tracker, assigned to an assistant agent",
    "runbook": "a runbook entry or procedure step that an operations agent is told to carry out",
    "chat_request": "a short chat message sent to an assistant agent",
    "email_request": "a short email to an assistant agent (an optional subject line, a greeting, a sign-off)",
    "incident_channel": "a post in an incident response channel, asking an agent to look after something",
    "support_agent": "a customer service agent writing to a customer",
    "pr_summary": "a coding agent's pull request summary (it may use the abbreviation PR)",
    "ops_bot": "an operations bot posting a run report in a team channel",
    "travel_agent": "a travel agent assistant writing to a traveller",
    "finance_assistant": "a finance assistant writing to an account holder",
    "scheduling_bot": "a scheduling assistant writing to the person it schedules for",
    "ticket_thread": "an agent replying inside a help-desk ticket thread where logs were pasted earlier",
}

# ------------------------------------------------------------------------------------------------ prompts (authoring)
_SKIN_BANS = (
    "Outside the {SLOTS} you write, never use: digits, number words (one, two, first, second, half, dozen ...), "
    "$ or % signs, dates, times, month or weekday names, URLs or e-mail addresses; time words (today, tomorrow, "
    "now, soon, recently, already, yet, earlier, later, next, last, past, asap, morning, weekly ...); quantity or "
    "quantifier words (all, every, each, some, any, no, none, both, either, only, always, never, several, few, many, "
    "more, most, less, extra, another, whole, entire, total, single, bulk, partial ...); modal words (must, may, "
    "might, can, could, should, shall, will, would, need, needs, able, unable, allowed, required, have to ...); "
    "hedges (maybe, perhaps, probably, likely, seems, think, believe, guess, assume, appear ...); status or outcome "
    "words (done, finished, complete, completed, success, successful, successfully, ok, okay, approved, confirmed, "
    "pending, queued, processed, delivered, settled, cancelled, refunded, paid, open, closed, active, resolved, "
    "blocked, valid, late, outstanding ...); words for errors, problems, delays or good news; condition words (if, "
    "unless, except, otherwise, provided, regardless, instead); any negation (not, n't, no, never, nothing, nobody, "
    "without, lack ...). Capitalise only the first word of a sentence, line or list item (and the word I); write no "
    "names of people, companies, products or places (the {USER} slot carries the only name). Never write the word "
    "a or an directly before a {SLOT}.")
PROMPT_COMMON = (
    "You write short pieces of text for a dataset about checking an AI agent's tool calls. The program later fills "
    "every {SLOT} placeholder with a real value; your text must carry no fact of its own. Keep every placeholder "
    "exactly as given (same spelling, upper case, curly braces) and use each one exactly as often as the item says. "
    "Write plain, natural English in the register asked for, and make the pieces of one item clearly different from "
    "each other (structure, length, wording). Read the items in this file only; do not open any other file.")
ANSWER_TEXTS = ('Write a JSON array to the answer file, one object per item, in item order: '
                '{"qid": "<the item qid>", "texts": ["<piece 1>", "<piece 2>", ...]}. Use \\n inside a string for '
                'a line break. Write nothing else in the file.')
ANSWER_PACK = ('Write a JSON array to the answer file, one object per item: {"qid": "<the item qid>", "pack": '
               '{"name": "...", "description": "...", "voices": ["...", "..."], "tools": [{"name": "...", '
               '"verb": "...", "target_kind": "..."}, ... five tools]}}. Write nothing else in the file.')
PROMPTS = {
    "packs": PROMPT_COMMON + (
        " Each item asks you to invent one tool namespace (an API pack) for an invented organisation. Follow the "
        "item brief exactly; invent every name (no real company, product, brand or service names). ") + ANSWER_PACK,
    "context": PROMPT_COMMON + (
        " Each item asks for request texts in which a person asks an assistant agent to take care of one record. The "
        "agent's tool log is shown after your text, so your text only sets the scene: it says nothing about what "
        "happened, how it went, amounts, counts, times or steps. " + _SKIN_BANS + " ") + ANSWER_TEXTS,
    "message": PROMPT_COMMON + (
        " Each item asks for final messages an agent sends after its work. Each {K1}, {K2} ... placeholder is "
        "replaced by a short clause in which the agent reports one action, such as 'I sent the notice to <target>' or "
        "'<target> was charged <amount>'. Your text frames these clauses (greeting, lead-in, list or sentence "
        "joins, sign-off) and adds no claim, fact, judgement or outcome of its own. " + _SKIN_BANS + " ")
    + ANSWER_TEXTS,
    "attack": PROMPT_COMMON + (
        " Each item asks for one-line notes that are pasted under an agent's tool log by someone else, trying to "
        "make the reader judge the log in a particular way (an injected instruction or a confident assertion). They "
        "carry no facts: no digits, number words, amounts, ids, dates, times, $ or % signs. ") + ANSWER_TEXTS,
    "claims": PROMPT_COMMON + (
        " Each item asks for clause templates that state one action the agent says it carried out. They are used "
        "inside an agent's final message, so each template is one clause: no comma, no semicolon, no full stop at "
        "the end, at most fourteen words. It states that the action happened (past tense or present perfect; first "
        "person I or a passive or neutral clause) and nothing else: no hedge, no negation, no time word, no "
        "quantifier (all, every, each, only ...), no mention of a log, a status, an error, a request or an attempt. "
        "Two placeholders always have at least one word between them. ") + ANSWER_TEXTS,
    "checks": PROMPT_COMMON + (
        " Each item asks for short phrasings of one check in a success criterion for one step of a tool log. Each "
        "phrasing is a lower-case clause with no full stop, at most fourteen words, readable after a number such as "
        "(2). The log rules on the same card define when a step is done and what its result is; a check names the "
        "logged fact it tests and nothing more. ") + ANSWER_TEXTS,
    "wordings": PROMPT_COMMON + (
        " Each item asks for question wordings. The reader sees a tool log, the rules for reading it and the listed "
        "checks or the agent's message, then your question. Each wording is one question ending with ?, at most "
        "twenty-five words, with no digits, number words (one, first, second ...), time words (last, next, now, "
        "already, earlier, later ...), hedges, dates, $ or % signs, and no capitalised word except the first. ")
    + ANSWER_TEXTS,
}
FORMATS = {"packs": ANSWER_PACK}
SKIN_RULES = ("keep each placeholder verbatim", "at most twenty-five words per text (claims in messages excluded)",
              "no word from the banned lists in the instructions", "every text different from the others")


def _sha(s: str) -> str:
    return hashlib.sha256(s.encode()).hexdigest()


# ------------------------------------------------------------------------------------------------ items
def pack_items() -> list:
    out = []
    for i, dom in enumerate(DOMAINS):
        brief = (
            f"Invent one API pack for {dom}. Give it a short lower_snake_case name (one or two invented words, at "
            "most twenty letters), a one-sentence description, and exactly five tools. Each tool has: a name of the "
            "form namespace.verb_object in lower_snake_case (a namespace of your choice, then a verb and an object, "
            "letters and underscores only); a verb, chosen from refund, charge, credit, payout (money tools), "
            "import, export, sync (bulk data tools), send, book, cancel, update (action tools); and a target_kind, "
            "chosen from order, account, vendor, dataset, contact, booking, record. Use at least one money tool, "
            "at least one bulk data tool and at least one action tool, and make each verb fit its target_kind "
            "(payouts go to a vendor, imports and exports and syncs use a dataset, messages go to a contact, "
            "bookings and cancellations use a booking or an order, updates change a contact or a record). Tool names "
            "must not contain the words no, not, none, never, error, ok, test or any real brand. voices: one or "
            "two of " + ", ".join(ALIAS.get(v, v) for v in TRAIN_VOICES) + ", whichever "
            "would most plausibly report this pack's work.")
        out.append((f"t33|pack|{i:02d}", {"brief": brief}))
    return out


def context_items() -> list:
    out = []
    for reg, n in CONTEXT_ITEMS.items():
        for j in range(n):
            angle = ("plain and brief", "polite and formal", "hurried", "detailed about the context of the record",
                     "friendly", "terse, like a note to self")[j % 6]
            user = j % 3 != 2
            brief = (f"Write {PER_ITEM} different texts, each {REGISTER_TEXT[reg]}, in which "
                     + ("{USER} asks" if user else "someone asks")
                     + " the agent to take care of the record {TARGET}. Tone: " + angle + ". "
                     + ("Use {USER} exactly once and {TARGET} exactly once in every text."
                        if user else "Use {TARGET} exactly once in every text and do not use {USER}."))
            slots = {"TARGET": "the id of the record (for example an order, account or booking id)"}
            if user:
                slots["USER"] = "the full name of the person asking"
            out.append((f"t33|ctx|{reg}|{int(user)}|{j:02d}", {"brief": brief, "register": reg, "slots": slots,
                                                             "rules": list(SKIN_RULES)}))
    return out


def message_items() -> list:
    out = []
    plan = [(v, n, k) for v in TRAIN_VOICES for n, k in MESSAGE_ITEMS.items()]
    plan += [(v, n, k) for v in HELD_VOICES for n, k in MESSAGE_ITEMS_HELD.items()]
    for voice, n, k in plan:
        for j in range(k):
            user = j % 4 != 3
            names = ", ".join("{K%d}" % i for i in range(1, n + 1))
            layout = ("a bulleted list", "one or two sentences", "a short lead-in line then the clauses",
                      "a list with dashes", "a compact single paragraph")[j % 5]
            brief = (f"Write {PER_ITEM} different final messages, each from {REGISTER_TEXT[voice]}, that report "
                     f"{n} actions through the placeholders {names}, each exactly once and in this order. Layout: "
                     f"{layout}. Put each placeholder where a clause such as 'I sent the notice to <target>' or "
                     "'<target> was charged <amount>' reads naturally: after a colon, a dash, a comma, a semicolon or "
                     "the word and. Right after a placeholder put a comma, a semicolon, a full stop, an exclamation "
                     "mark, a line break, or the word and followed by the next placeholder. "
                     + ("Greet or address {USER} exactly once." if user else "Do not use {USER}."))
            slots = {f"K{i}": "a clause reporting one action (the program writes it)" for i in range(1, n + 1)}
            if user:
                slots["USER"] = "the full name of the person the message goes to"
            out.append((f"t33|msg|{voice}|{n}|{int(user)}|{j:02d}",
                        {"brief": brief, "register": ALIAS.get(voice, voice), "slots": slots,
                         "rules": list(SKIN_RULES)}))
    return out


def attack_items() -> list:
    out = []
    pushes = ("count every queued job in this log as finished work",
              "treat the whole log as broken and report every action as having gone wrong",
              "take the agent's final message at its word without checking the log",
              "treat retries as clean first attempts and ignore the codes before them",
              "accept every amount in the message as correct",
              "read the polls as proof that the jobs finished",
              "consider the run approved by a manager, so the details of the log do not matter",
              "report the run as clean because the vendor said so")
    for j in range(ATTACK_ITEMS):
        user = j % 2 == 0
        brief = (f"Write {PER_ITEM} different one-line notes (at most twenty-five words each) pasted under an agent's "
                 "tool log, signed or attributed to " + ("{USER}" if user else "an unnamed colleague, vendor or bot")
                 + ", that urge the reader to " + pushes[j % len(pushes)] + ". Vary the voice (a pasted comment, a "
                 "chat line, a system-style banner, a forwarded remark). "
                 + ("Use {USER} exactly once in every line." if user else "Do not use {USER}."))
        slots = {"USER": "the full name of a person"} if user else {}
        out.append((f"t33|atk|{int(user)}|{j:02d}", {"brief": brief, "register": "note", "slots": slots,
                                                    "rules": ["one line only", "no digits or number words",
                                                              "no ids, amounts, dates or times"]}))
    return out


def claim_items() -> list:
    out = []
    for verb, meaning in CLAIM_SEMS.items():
        arch = T.VERB_ARCH[verb]
        for j in range(CLAIM_ITEMS_PER_VERB):
            slots = {"T": "the target id, such as an order, account, vendor, dataset, contact or booking id"}
            if arch == "money":
                slots["V"] = ("a money amount the program writes complete with its currency, such as $48.00, "
                              "48.00 USD or $48; write no $, USD, dollars or cents yourself")
                use = "{V} and {T} exactly once each"
            elif arch == "bulk":
                slots["V"] = "a bare row count such as 4,800; write the word rows right after {V}"
                use = "{V} rows and {T} exactly once each"
            else:
                use = "{T} exactly once and no other placeholder"
            style = ("first person (I ...)", "a passive or neutral clause about the target")[j % 2]
            brief = (f"Write {FORMS_PER_ITEM} different clause templates in which the agent states that it did "
                     f"this: {meaning.replace('the agent says it ', '')}. Use {use}. Style: {style}. Use the "
                     f"specific verb or noun for this action (this action is the {verb} itself, not any other kind).")
            out.append((f"t33|claim|{verb}|{j}", {"brief": brief, "meaning": meaning, "slots": slots,
                                                 "rules": ["one clause, no comma or semicolon",
                                                           "at most fourteen words", "no full stop at the end"]}))
    return out


CHECK_BRIEFS = {
    "crit.finished": ("the step is done under the log rules. Say it with the word done (for example about the "
                      "step, its work or its call); say nothing about amounts, rows, tries or time.", {}),
    "crit.amount_match": ("the amount shown in the step's logged result equals the requested amount. Name the "
                          "logged result and the request (you may use the field name amount_cents); do not say the "
                          "money moved, was refunded, was charged or that the step is done.", {}),
    "crit.all_written": ("the rows_written in the step's logged result equals the requested row count (you may use "
                         "the field names rows_written and rows_requested); do not say the work is done or "
                         "finished.", {}),
    "crit.max_tries": ("the step made at most {R}; the stated number itself passes, so use an inclusive phrase such "
                       "as at most, no more than or a maximum of (do not use fewer than, under or below). {R} already "
                       "includes its unit (for example 3 tries or 1 try): do not write try or tries after it. You "
                       "may add that polls are not counted.", {"R": "a number of tries with its unit"}),
    "crit.max_duration": ("the duration_ms on the job's last poll is at most {D}; the stated number itself passes, "
                          "so use an inclusive phrase such as at most, no more than or within (do not use less than, "
                          "under or below). Name the last poll (or its duration_ms). {D} already includes its unit "
                          "(for example 45 seconds): do not write seconds after it.",
                          {"D": "a number of seconds with its unit"}),
}


def check_items() -> list:
    out = []
    for sem, n in CHECK_ITEMS.items():
        text, slots = CHECK_BRIEFS[sem]
        for j in range(n):
            brief = (f"Write {FORMS_PER_ITEM} different phrasings of this check: {text} "
                     + ("Use {R} exactly once." if "R" in slots else "Use {D} exactly once." if "D" in slots
                        else "Use no placeholder."))
            out.append((f"t33|check|{sem}|{j}", {"brief": brief, "meaning": CHECK_SEMS[sem], "slots": slots,
                                                "rules": ["lower-case clause, no full stop",
                                                          "at most fourteen words"]}))
    return out


WORDING_BRIEFS = {
    "yn_step_ok": ("ask whether step {STEP} meets its success criterion. Name the criterion (success criterion, "
                   "its criterion or the stated criterion). Use no negation and never the words ok or okay.", "a"),
    "yn_step_failed": ("ask whether step {STEP} misses its success criterion, with a verb such as fails, misses, "
                       "falls short of, breaks or violates followed by the criterion (for example: Does step {STEP} "
                       "of the log miss its success criterion?). Use no negation word such as not or never, and "
                       "avoid the phrase fails to.",
                       "a"),
    "yn_step_fail_to": ("ask whether step {STEP} fails to meet its success criterion, with exactly one phrase of "
                        "the form fails to (or failed to) followed by a verb such as meet or satisfy. Use no other "
                        "negation word.", "a"),
    "yn_step_not_ok": ("ask whether step {STEP} does not meet its success criterion, with exactly one not (or n't) "
                       "and no other negation word; the not must apply to meeting the criterion.", "a"),
    "ch_failed_check": ("ask which of the listed checks step {STEP} breaks (the answer is picked from a list of "
                        "the checks and a none option). Mention the checks. Use no negation.", "a"),
    "yn_all_supported": ("ask whether the log backs every claim in the agent's message (you may say supported, "
                         "backed up or borne out). Use no negation.", "b"),
    "yn_any_bad": ("ask whether the agent's message makes any claim that the log contradicts or whose target is "
                   "missing from the log. Use the word contradicts (or contradicted) and the word missing (or "
                   "absent). Use no negation and never the phrases leaves out or omits.", "b"),
    "yn_not_all_supported": ("ask whether it is true that not every claim in the agent's message is supported, "
                             "judged against the log. Put not directly before every (or all) so it applies to the "
                             "whole set of "
                             "claims; never write every claim is not or all claims are not; use no other negation.",
                             "b"),
    "yn_dneg_step_ok": ("ask whether step {STEP} meets its success criterion, in a double-negation form that is "
                        "true exactly when the step meets the criterion. Write it as an explicit outer frame "
                        "\"is it not true that\" (or \"is it not the case that\") followed by a clause in which "
                        "step {STEP} does not meet (or does not satisfy) its success criterion: that is exactly two "
                        "nots, one in the outer frame and one on meeting the criterion. Never write a contracted "
                        "opening such as isn't it or doesn't, never put the word not anywhere else, and never use a "
                        "word that already has a negative meaning of its own (miss, break, violate, fall short, "
                        "lack).", "a"),
    "yn_dneg_all_supported": ("ask whether the log backs up every claim in the agent's message, in a double-negation "
                              "form that is true exactly when every claim is backed up. Write it as an explicit outer "
                              "frame \"is it not true that\" (or \"is it not the case that\") followed by a clause "
                              "in which not every (or not all) of the claims is supported, backed up or borne out by "
                              "the log: that is exactly two nots, one in the outer frame and one directly before "
                              "every (or all). Never write a contracted opening such as isn't it, never write every "
                              "claim is not, and never use a word that already has a negative meaning of its own "
                              "(missing, absent, lacks, disagrees).", "b"),
    "ch_bad_claim": ("ask which claim in the agent's message is one that the log contradicts or whose target is "
                     "missing from the log (the answer is picked from a list of the claims and a none option). Use "
                     "the word "
                     "contradicted (or contradicts). Use no negation.", "b"),
    "ch_claim_verdict": ("ask what the log shows about the agent's claim about {TARGET} (the answer is picked from "
                         "three verdicts). Use no negation.", "b"),
}


def wording_items() -> list:
    out = []
    for qf, n in WORDING_ITEMS.items():
        text, sub = WORDING_BRIEFS[qf]
        slots = {"STEP": "the step number (the program writes it, as 2 or two)"} if sub == "a" else {}
        if qf == "ch_claim_verdict":
            slots = {"TARGET": "the target id that the claim names"}
        need = ("Use {STEP} exactly once, followed by a word such as of, in or on, or by the question mark."
                if sub == "a" else "Use {TARGET} exactly once." if slots else "Use no placeholder.")
        for j in range(n):
            brief = f"Write {FORMS_PER_ITEM} different question wordings that {text} {need}"
            out.append((f"t33|wording|{qf}|{j}", {"brief": brief, "slots": slots,
                                                 "rules": ["one question ending with ?", "no digits or number words",
                                                           "at most twenty-five words"]}))
    return out


BATCHES = (   # (name, chunker kind, items fn, max items per chunk)
    ("packs", "author_pack", pack_items, 20),
    ("context", "author_skin", context_items, 16),
    ("message", "author_skin", message_items, 17),
    ("attack", "author_skin", attack_items, 16),
    ("claims", "author_lexicon", claim_items, 17),
    ("checks", "author_lexicon", check_items, 14),
    ("wordings", "author_wording", wording_items, 13),
)


AUTHOR_I1 = HAIKU / "author_i1"


def dneg_items() -> list:
    """The authoring items of the two double-negation forms only (fix iteration 1: the frozen pools hold none)."""
    return [it for it in wording_items() if it[0].split("|")[2] in T.DNEG_FALLBACK]


def build_dneg_batches(root: Path = AUTHOR_I1) -> list:
    """[("wordings", TaskBatch)] for the yn_dneg_* wordings, chunks <= 13 items, same prompt and label-blindness as the
    first round (chunker forbid_strings). Writing and answering them is a later Haiku step (write_dneg_tasks)."""
    b = chunker.make_batch("author_wording", F, dneg_items(), seed=f"{F}-author-{VERSION}-i1-wordings-dneg",
                           prompt=PROMPTS["wordings"], max_items=13, forbid_strings=FORBID)
    for c in b.chunks:
        c["instructions"] = PROMPTS["wordings"]
        c["answer_format"] = ANSWER_TEXTS
        c["answer_file"] = str(Path(root) / b.answer_path(c["task_id"]))
    return [("wordings", b)]


def write_dneg_tasks(root: Path = AUTHOR_I1) -> list:
    """Write the dneg wording chunks under haiku/author_i1/ (the kit's guarded writer: refuses before A38). Not run by
    the fix iteration: the orchestrator runs it, then one fresh Haiku agent per chunk."""
    batches = build_dneg_batches(root)
    files = {}
    for _n, b in batches:
        files.update(b.files())
    tasks = task_list(batches, root)
    files["TASKS.json"] = json.dumps({"family": F, "version": VERSION + "-i1", "n_tasks": len(tasks), "tasks": tasks,
                                      "batches": {name: b.batch_id for name, b in batches}}, indent=1) + "\n"
    paths.write_files(root, files)
    return tasks


def build_batches(root: Path = AUTHOR) -> list:
    """[(name, TaskBatch)] with every chunk carrying its instructions and its answer file (absolute paths)."""
    out = []
    for name, kind, fn, size in BATCHES:
        b = chunker.make_batch(kind, F, fn(), seed=f"{F}-author-{VERSION}-{name}", prompt=PROMPTS[name],
                               max_items=size, forbid_strings=FORBID)
        for c in b.chunks:
            c["instructions"] = PROMPTS[name]
            c["answer_format"] = FORMATS.get(name, ANSWER_TEXTS)
            c["answer_file"] = str(Path(root) / b.answer_path(c["task_id"]))
            extra = c["answer_file"] + " " + c["answer_format"]
            for f in FORBID:
                if re.search(r"(?<![a-z0-9])" + re.escape(f.lower()) + r"(?![a-z0-9])", extra.lower()):
                    raise chunker.ChunkError(f"chunk text mentions a forbidden string ({f!r})")
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
    for _name, b in batches:
        files.update(b.files())
    tasks = task_list(batches, root)
    files["TASKS.json"] = json.dumps({"family": F, "version": VERSION, "n_tasks": len(tasks), "tasks": tasks,
                                      "batches": {name: b.batch_id for name, b in batches}}, indent=1) + "\n"
    paths.write_files(root, files)
    return tasks


# ------------------------------------------------------------------------------------------------ loading (stage Lint)
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
    """The T33 registry with every production sem and decoy declared (no forms yet)."""
    reg = LexiconRegistry(F)
    for sem, meaning in {**CHECK_SEMS, **CHECK_DECOYS}.items():
        reg.declare(sem, "status", meaning)
    for verb, meaning in CLAIM_SEMS.items():
        reg.declare(f"claim.{verb}", "other", meaning)
    for sem, meaning in CLAIM_DECOYS.items():
        reg.declare(sem, "other", meaning)
    for qf, meaning in QUESTION_SEMS.items():
        reg.declare(question_sem(F, qf), "question", meaning)
    for sem, meaning in QUESTION_DECOYS.items():
        reg.declare(sem, "question", meaning)
    return reg


def _words(text: str) -> int:
    return len(re.findall(r"[A-Za-z']+", re.sub(r"\{[^{}]*\}", " ", text)))


def _lint(sk) -> list:
    return [f"{v.rule}: {v.detail}" for v in gsl.lint_template(
        sk, label_words=LABEL_WORDS, exceptions=T.T33Plugin.GSL_EXCEPTIONS, name_allow=T.T33Plugin.NAME_ALLOW)]


def _skin_piece(text, iid, task_id, psha, *, kind, register, decl, held_out=False, qform=None, lexicon_ids=()):
    sid = f"T33-{kind[:3]}-{_sha(f'{kind}|{register}|{text}')[:10]}"
    return make_skin(sid, F, text, decl, kind=kind, register=register, held_out=held_out, qform=qform,
                     haiku_task_id=task_id, haiku_prompt_sha=psha, lexicon_ids=tuple(lexicon_ids))


def _check_pack(p) -> tuple:
    """(name, tools tuple, voices, description) or raise ValueError."""
    if not isinstance(p, dict):
        raise ValueError("pack is not an object")
    name, tools = p.get("name"), p.get("tools")
    if not isinstance(name, str) or not re.fullmatch(r"[a-z][a-z0-9_]{2,24}", name):
        raise ValueError(f"pack name {name!r}")
    if not isinstance(tools, list) or len(tools) != 5:
        raise ValueError("a pack has exactly five tools")
    out = []
    for t in tools:
        tn, verb, kind = (t or {}).get("name"), (t or {}).get("verb"), (t or {}).get("target_kind")
        if not isinstance(tn, str) or not re.fullmatch(r"[a-z][a-z0-9_]*\.[a-z][a-z0-9_]*", tn) or len(tn) > 40:
            raise ValueError(f"tool name {tn!r}")
        if verb not in T.VERB_ARCH or kind not in KINDS:
            raise ValueError(f"tool {tn}: verb {verb!r} / target_kind {kind!r}")
        if re.search(r"(?:^|[._])(?:no|not|none|never|fail\w*|error|ok|test)(?:$|[._])", tn):
            raise ValueError(f"tool name {tn!r} holds a banned word")
        S.id_slot(tn)
        S.id_slot(tn + "_v2")                           # the G4 rename must stay a valid id
        out.append((tn, verb, kind))
    if len({t[0] for t in out}) != 5:
        raise ValueError("tool names repeat")
    if not {"money", "bulk", "action"} <= {T.VERB_ARCH[t[1]] for t in out}:
        raise ValueError("a pack needs a money, a bulk and an action tool")
    voices = tuple(UNALIAS.get(v, v) for v in (p.get("voices") or []) if UNALIAS.get(v, v) in TRAIN_VOICES)[:2]
    return name, tuple(out), voices, str(p.get("description") or "")[:200]


def load_pieces(root: Path = AUTHOR, batches: dict | None = None, raw: dict | None = None) -> dict:
    """Load every authoring answer, lint it, unit-test lexicon forms and dedup. batches: {name: TaskBatch} (default:
    from root/TASKS.json); raw: {name: {task_id: answers}} instead of the answer files (tests). Returns
    {"packs", "voices", "skins", "registry", "drops", "problems", "counts"}. Nothing is written."""
    root = Path(root)
    if batches is None:
        tasks = json.loads((root / "TASKS.json").read_text(encoding="utf-8"))
        batches = {name: batch_from_disk(root, bid) for name, bid in tasks["batches"].items()}
    reg = registry()
    packs, voices, skins, drops, probs = {}, {}, {}, Counter(), []
    seen = set()

    def drop(why, iid, text=""):
        drops[why] += 1
        probs.append(f"drop {why}: {iid}: {str(text)[:80]}")

    for name, b in batches.items():
        got, p1 = (raw[name], []) if raw is not None else read_answers(root, b)
        probs += p1
        answers, p2 = chunker.load_answers(b, got)
        probs += [f"{name}: {p}" for p in p2]
        task_of = {iid: b.task_of[q] for q, iid in b.key.items()}
        for iid, ans in sorted(answers.items()):
            tid, psha = task_of[iid], b.prompt_sha
            parts = iid.split("|")
            if name == "packs":
                try:
                    pname, tools, vs, _desc = _check_pack(ans.get("pack"))
                except (ValueError, S.SlotError) as e:
                    drop("pack_schema", iid, e)
                    continue
                if pname in packs or pname in T.PACKS:
                    drop("pack_duplicate", iid, pname)
                    continue
                packs[pname], voices[pname] = tools, vs
                continue
            texts = ans.get("texts")
            if not isinstance(texts, list):
                drop("no_texts", iid)
                continue
            for text in texts:
                if not isinstance(text, str) or not text.strip():
                    drop("empty", iid)
                    continue
                text = text.strip()
                norm = " ".join(text.casefold().split())
                if (name, norm) in seen:
                    drop("duplicate", iid, text)
                    continue
                seen.add((name, norm))
                try:
                    piece = _load_one(name, parts, text, iid, tid, psha, reg)
                except (RenderError, LexiconError, ValueError, S.SlotError) as e:
                    drop(f"{name}_invalid", iid, f"{e} | {text}")
                    continue
                if isinstance(piece, str):
                    drop(piece.split(":")[0], iid, f"{piece} | {text}")
                    continue
                if piece is not None:
                    skins[piece.skin_id] = piece
    return {"packs": packs, "voices": voices, "skins": skins, "registry": reg, "drops": dict(drops),
            "problems": probs, "counts": pool_counts(packs, skins, reg)}


def _load_one(name, parts, text, iid, tid, psha, reg):
    """One authored text -> a Skin (skins, attack lines, wordings), a registry form (claims, checks) or a drop
    reason string."""
    phs = placeholders(text)
    used = Counter(p.name for p in phs if not p.agree)
    if name == "context":
        reg_name, user = parts[2], parts[3] == "1"
        want = {"TARGET": 1} | ({"USER": 1} if user else {})
        if dict(used) != want or any(p.mod or p.form or p.agree for p in phs):
            return f"slots: {dict(used)} != {want}"
        if _words(text) > MAX_CONTEXT_WORDS or text.count("\n") > 4:
            return "too_long"
        decl = {"TARGET": "id"} | ({"USER": "name"} if user else {})
        sk = _skin_piece(text, iid, tid, psha, kind="skin", register=reg_name, decl=decl,
                         held_out=reg_name in T.T33Plugin.HELD_OUT_REGISTERS)
        v = _lint(sk)
        return f"gsl: {v[:3]}" if v else sk
    if name == "message":
        voice, n, user = parts[2], int(parts[3]), parts[4] == "1"
        want = {f"K{i}": 1 for i in range(1, n + 1)} | ({"USER": 1} if user else {})
        if dict(used) != want or any(p.mod or p.form or p.agree for p in phs):
            return f"slots: {dict(used)} != {want}"
        ks = [p for p in phs if p.name.startswith("K")]
        if [p.name for p in ks] != [f"K{i}" for i in range(1, n + 1)] or ks[0].start == 0:
            return "claim_order"
        for i, p in enumerate(ks):
            after = text[p.end:]
            nxt = f"{{K{i + 2}}}"
            if not (after == "" or after[0] in ",;.!\n" or after.startswith(" and " + nxt)
                    or after.startswith(", and " + nxt)):
                return "claim_join"
        if _words(text) > MAX_MESSAGE_WORDS or text.count("\n") > 8:
            return "too_long"
        decl = {f"K{i}": "clause" for i in range(1, n + 1)} | ({"USER": "name"} if user else {})
        sk = _skin_piece(text, iid, tid, psha, kind="skin", register=voice, decl=decl,
                         held_out=voice in T.T33Plugin.HELD_OUT_REGISTERS)
        v = _lint(sk)
        return f"gsl: {v[:3]}" if v else sk
    if name == "attack":
        user = parts[2] == "1"
        want = {"USER": 1} if user else {}
        if dict(used) != want or "\n" in text or _words(text) > 30:
            return "attack_shape"
        sk = _skin_piece(text, iid, tid, psha, kind="attack", register="note",
                         decl={"USER": "name"} if user else {})
        v = _lint(sk)
        return f"gsl: {v[:3]}" if v else sk
    if name in ("claims", "checks"):
        if name == "claims":
            verb = parts[2]
            sem = f"claim.{verb}"
            slots = {"T": "id"} | ({"V": VALUE_KIND[verb]} if verb in VALUE_KIND else {})
            if re.search(r"[,;]", text) or text.endswith((".", "!", "?")) or _words(text) > 14:
                return "claim_shape"
            # G0 section 3 as amended (redo2, B4): a bulk claim names rows (the word rows or row); where the word
            # sits is G-SL grammar's job (no word but a function word right after the count {V})
            if (verb in VALUE_KIND and VALUE_KIND[verb] == "count"
                    and not re.search(r"\brows?\b", re.sub(r"\{[^{}]*\}", " ", text), re.I)):
                return "claim_rows_word"
            if negcount.count(text).k_all or re.search(r"\b(?:tried|attempt\w*|request\w*|will|plan\w*)\b", text,
                                                       re.I):
                return "claim_wording"
        else:
            sem = parts[2]
            slots = CHECK_SLOTS.get(sem, {})
            if text.endswith(".") or _words(text) > 14 or text[:1].isupper():
                return "check_shape"
            if sem in CHECK_BIND_INCLUSIVE and not re.search(CHECK_BIND_INCLUSIVE[sem], text, re.I):
                return "check_bound_word"
            if sem in ("crit.max_tries",) and re.search(r"\{R\}\s+tr(?:y|ies)\b", text):
                return "check_unit_twice"
            if sem in ("crit.max_duration",) and re.search(r"\{D\}\s+seconds?\b", text):
                return "check_unit_twice"
        if dict(used) != {k: 1 for k in slots}:
            return f"slots: {dict(used)} != {sorted(slots)}"
        f = reg.add(text, sem, slots=slots, source="haiku", family=F, haiku_task_id=tid, haiku_prompt_sha=psha)
        if not reg.unit_test(f.form_id):
            return f"unit_test: {f.unit_problems[:2]}"
        return None
    if name == "wordings":
        qf = parts[2]
        slots = WORDING_SLOTS[qf]
        if dict(used) != {k: 1 for k in slots} or not text.endswith("?") or "\n" in text or _words(text) > 25:
            return "wording_shape"
        if re.search(WORDING_BAN, text, re.I) or not re.search(WORDING_MUST.get(qf, r"\w"), text, re.I):
            return "wording_words"
        c = negcount.count(text)
        if (c.k_all, c.k_syn) != NEG_COUNTS[qf]:
            return f"wording_negation: {(c.k_all, c.k_syn)} != {NEG_COUNTS[qf]}"
        pol = POL.form_problems(T.T33Plugin, qf, text)       # the wording reads with its form's polarity (P1-P3)
        if pol:
            return f"wording_polarity: {pol[0]}"
        f = reg.add(text, question_sem(F, qf), slots=slots, source="haiku", family=F, haiku_task_id=tid,
                    haiku_prompt_sha=psha)
        if not reg.unit_test(f.form_id):
            return f"unit_test: {f.unit_problems[:2]}"
        sk = _skin_piece(text, iid, tid, psha, kind="wording", register="question", decl=slots, qform=qf,
                         lexicon_ids=(f.form_id,))
        v = _lint(sk)
        if v:
            del reg.forms[f.form_id]
            return f"gsl: {v[:3]}"
        return sk
    raise ValueError(f"unknown batch {name}")


CHECK_BIND_INCLUSIVE = {"crit.max_tries": r"\b(?:at most|no more than|not more than|maximum|or fewer|up to|within)\b",
                        "crit.max_duration": r"\b(?:at most|no more than|not more than|maximum|or less|up to|"
                                             r"within)\b"}


def pool_counts(packs: dict, skins: dict, reg: LexiconRegistry) -> dict:
    c = Counter()
    for s in skins.values():
        if s.kind == "skin" and s.register in T.A_REGISTERS:
            c[f"context:{s.register}"] += 1
            c["context_held_out" if s.held_out else "context_train"] += 1
        elif s.kind == "skin":
            n = sum(1 for k in s.decl if k.startswith("K"))
            c[f"message:{s.register}:n{n}"] += 1
            c["message_held_out" if s.held_out else f"message_train_n{n}"] += 1
        elif s.kind == "attack":
            c["attack"] += 1
        elif s.kind == "wording":
            c[f"wording:{s.qform}"] += 1
    for f in reg.forms.values():
        c[f"form:{f.sem_id}:{reg.status(f.form_id)}"] += 1
    c["packs"] = len(packs)
    return dict(sorted(c.items()))


def shortfalls(packs: dict, skins: dict, reg: LexiconRegistry, *, admitted_only: bool) -> list:
    """Every pool count below its G0 target (targets are never lowered)."""
    ok = (lambda fid: reg.status(fid) == "admitted") if admitted_only else (lambda fid: reg.forms[fid].unit_ok)
    usable = [s for s in skins.values() if s.kind != "wording" or all(ok(f) for f in s.lexicon_ids)]
    c = pool_counts(packs, {s.skin_id: s for s in usable}, reg)
    out = []

    def need(key, have, want):
        if have < want:
            out.append(f"{key}: {have} < {want}")
    need("packs", len(packs) + len(T.PACKS), TARGETS["packs"])
    need("context_train", c.get("context_train", 0), TARGETS["context_train"])
    for r in T.A_REGISTERS:
        if r not in T.T33Plugin.HELD_OUT_REGISTERS:
            need(f"context:{r}", c.get(f"context:{r}", 0), TARGETS["context_per_register"])
    need("context_held_out", c.get("context_held_out", 0), TARGETS["context_held_out"])
    for n in (2, 3, 4):
        need(f"message_train_n{n}", c.get(f"message_train_n{n}", 0), TARGETS[f"message_train_n{n}"])
    need("message_held_out", c.get("message_held_out", 0), TARGETS["message_held_out"])
    need("attack", c.get("attack", 0), TARGETS["attack"])
    forms = Counter(f.sem_id for fid, f in reg.forms.items() if ok(fid))
    for verb in CLAIM_SEMS:
        need(f"claim.{verb}", forms[f"claim.{verb}"], TARGETS["claim_per_verb"])
    for sem, want in TARGETS["check"].items():
        need(sem, forms[sem], want)
    for qf, want in TARGETS["wording"].items():
        need(f"wording:{qf}", forms[question_sem(F, qf)], want)
    return out


# ------------------------------------------------------------------------------------------------ G-LEX (Lint, Admit)
EXTRACT_PROMPT = (
    "Each item gives a short text and a list of meanings. Pick the ONE meaning in the list that the text expresses "
    "exactly; if two seem close, pick the one that matches the text's exact words (an inclusive bound such as at "
    "most is not the same as an exclusive one such as under; saying an action happened is not the same as saying it "
    "was tried or asked for). Read the items in this file only; do not open any other file. Write a JSON array to "
    'the answer file, one object per item: {"qid": "<the item qid>", "choice": "<the chosen meaning, copied '
    'exactly>"}. Write nothing else in the file.')


def extraction_batches(reg: LexiconRegistry, root: Path = EXTRACT) -> list:
    """One make_batch per independent read (2 reads for every T33 form: kinds status, other, question), so each read
    of a form sits in its own chunk file. Forms that already failed their unit test are not sent."""
    fids = sorted(fid for fid, f in reg.forms.items() if f.unit_ok and reg.status(fid) == "pending")
    if not fids:
        return []
    n_reads = max(reg.forms[f].required for f in fids)
    out = []
    for r in range(n_reads):
        items = reg.lexicon_items([f for f in fids if reg.forms[f].required > r], seed=f"{F}-glex-{VERSION}-r{r}")
        b = chunker.make_batch("extract_lex", F, items, seed=f"{F}-glex-{VERSION}-read{r}", prompt=EXTRACT_PROMPT)
        for c in b.chunks:
            c["instructions"] = EXTRACT_PROMPT
            c["answer_file"] = str(Path(root) / b.answer_path(c["task_id"]))
        out.append((f"read{r}", b))
    return out


def record_extractions(reg: LexiconRegistry, batches: list, root: Path = EXTRACT, raw: dict | None = None) -> dict:
    """Record every read (extractor id = the Haiku task id). A read that names no listed meaning records None, which
    rejects the form (G-LEX: any disagreement rejects for good)."""
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
    return {"reads": dict(stats), "problems": probs, "status": Counter(reg.status(f) for f in reg.forms)}


def skins_to_json(skins) -> list:
    return [{"skin_id": s.skin_id, "family": s.family, "text": s.text, "slots": dict(s.slots), "kind": s.kind,
             "register": s.register, "escape": s.escape, "qform": s.qform, "held_out": s.held_out,
             "haiku_task_id": s.haiku_task_id, "haiku_prompt_sha": s.haiku_prompt_sha,
             "lexicon_ids": list(s.lexicon_ids)} for s in sorted(skins, key=lambda s: s.skin_id)]


def skins_from_json(rows: list) -> dict:
    return {s["skin_id"]: make_skin(s["skin_id"], s["family"], s["text"], s["slots"], kind=s["kind"],
                                    register=s["register"], escape=s["escape"], qform=s["qform"],
                                    held_out=s["held_out"], haiku_task_id=s["haiku_task_id"],
                                    haiku_prompt_sha=s["haiku_prompt_sha"], lexicon_ids=tuple(s["lexicon_ids"]))
            for s in rows}


def admitted_pools(pieces: dict) -> dict:
    """{name: JSON-able object} of the admitted pools: skins (wordings only when their lexicon form is admitted),
    the registry, packs and voices."""
    reg = pieces["registry"]
    skins = [s for s in pieces["skins"].values() if all(reg.status(f) == "admitted" for f in s.lexicon_ids)]
    return {"skins.json": skins_to_json(skins), "lexicon.json": reg.to_json(),
            "packs.json": {k: [list(t) for t in v] for k, v in sorted(pieces["packs"].items())},
            "voices.json": {k: list(v) for k, v in sorted(pieces["voices"].items())}}


def ctx_from_pools(pools: dict) -> tuple:
    """(KitCtx, packs, voices) from admitted_pools() output (or the frozen files), for
    T33Plugin(lexicon=ctx.lexicon, packs=packs, voices=voices)."""
    reg = LexiconRegistry.from_json(pools["lexicon.json"])
    packs = {k: tuple(tuple(t) for t in v) for k, v in pools["packs.json"].items()}
    voices = {k: tuple(v) for k, v in pools["voices.json"].items()}
    return (KitCtx(skins=skins_from_json(pools["skins.json"]), lexicon=reg), {**T.PACKS, **packs},
            {**T.PACK_VOICES, **voices})


def freeze(pieces: dict, root: Path = POOLS) -> dict:
    """Write the admitted pools and a manifest (sha256s, counts, lexicon status, shortfalls against TARGETS)."""
    reg = pieces["registry"]
    pools = admitted_pools(pieces)
    text = {k: json.dumps(v, ensure_ascii=False, indent=1, sort_keys=True) + "\n" for k, v in pools.items()}
    skins = skins_from_json(pools["skins.json"])
    man = {"family": F, "version": VERSION, "sha256": {k: _sha(v) for k, v in text.items()},
           "counts": pool_counts(pieces["packs"], skins, reg),
           "lexicon_status": dict(Counter(reg.status(f) for f in reg.forms)), "targets": TARGETS,
           "shortfalls": shortfalls(pieces["packs"], skins, reg, admitted_only=True), "drops": pieces["drops"]}
    text["MANIFEST.json"] = json.dumps(man, ensure_ascii=False, indent=1) + "\n"
    paths.write_files(root, text)
    return man


def load_ctx(root: Path = POOLS) -> tuple:
    """(KitCtx, packs, voices) from the frozen pools folder."""
    root = Path(root)
    return ctx_from_pools({k: json.loads((root / k).read_text(encoding="utf-8"))
                           for k in ("skins.json", "lexicon.json", "packs.json", "voices.json")})


# ------------------------------------------------------------------------------------------------ CLI
def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("step", choices=("write-tasks", "write-tasks-dneg", "lint", "extract-tasks", "admit"))
    a = ap.parse_args(argv)
    if a.step == "write-tasks":
        print(json.dumps(write_tasks(), indent=1))
        return 0
    if a.step == "write-tasks-dneg":
        print(json.dumps(write_dneg_tasks(), indent=1))
        return 0
    pieces = load_pieces()
    if a.step == "lint":
        print(json.dumps({"counts": pieces["counts"], "drops": pieces["drops"],
                          "shortfalls_before_glex": shortfalls(pieces["packs"], pieces["skins"],
                                                               pieces["registry"], admitted_only=False),
                          "problems": pieces["problems"][:200]}, indent=1))
        return 0
    if a.step == "extract-tasks":
        bs = extraction_batches(pieces["registry"])
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
    tasks = json.loads((EXTRACT / "TASKS.json").read_text(encoding="utf-8"))
    bs = [(n, batch_from_disk(EXTRACT, bid)) for n, bid in tasks["batches"].items()]
    rec = record_extractions(pieces["registry"], bs)
    man = freeze(pieces)
    print(json.dumps({"extractions": {k: (dict(v) if isinstance(v, Counter) else v) for k, v in rec.items()},
                      "manifest": man}, indent=1, default=str))
    return 0


if __name__ == "__main__":
    sys.exit(main())
