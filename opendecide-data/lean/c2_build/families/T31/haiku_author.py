"""families/T31/haiku_author.py: the T31 Haiku AUTHORING tasks (G0_SPEC.md v1.1 section 7) and their answer loader.

  build   write the authoring tasks (chunks, prompts, keys, manifests, self-contained task files, TASKS.json) under
          haiku/author/ through paths.write_files (after A38 only); refuses to rewrite once any answer exists
  check   the same batches in memory only: counts and guard checks, nothing written
  load    read the answers that exist, map them back through the batch keys (chunker.load_answers), turn them into
          candidate pools (skins, wordings, attack lines, lexicon forms, packs, names, Mode F texts) and G-SL-lint
          them; prints counts and drop reasons. Nothing is written: admission (G-LEX) and the pool freeze come later.

Run from lean/:  ../.venv/bin/python c2_build/families/T31/haiku_author.py build|check|load

Every task is a gold-free chunk (chunker.make_batch, <= 50 items, opaque qids) plus a task file that repeats the batch
prompt, the items and the exact answer path, so a fresh Haiku agent reads one file and writes one file. Authoring
items never carry a question text, an option or a gold (forbid_strings: LABEL_WORDS + the stand-in question texts);
Haiku output never sets a label: wordings and band phrases enter rows only after G-LEX extraction admits them.
Pool sizes follow G0 section 7 with about 25% spare for lint, G13 and G3-H drops; the register mix keeps every
register <= 15% of rows although S4 draws only chat / email / transcript skins.
"""
from __future__ import annotations

import json
import random
import re
import sys
from pathlib import Path

_C2_BUILD = Path(__file__).resolve().parents[2]
if str(_C2_BUILD) not in sys.path:
    sys.path.insert(0, str(_C2_BUILD))

from c2_kit import chunker as CH  # noqa: E402
from c2_kit import gsl, paths  # noqa: E402
import negcount  # noqa: E402,I100  (c_src/common, put on sys.path by c2_kit.paths)
from c2_kit import skin as K  # noqa: E402
from c2_kit import slots as S  # noqa: E402
from c2_kit.lexicon import LexiconError, LexiconRegistry, question_sem  # noqa: E402
from families.T31 import fixtures as FX  # noqa: E402
from families.T31 import plugin as P  # noqa: E402

F = "T31"
HERE = Path(__file__).resolve().parent
ROOT = HERE / "haiku" / "author"
SEED = "t31-author-v1"
VERSION = "v1"

# ------------------------------------------------------------------------------------------------ pool plan (G0 7)
# Mode T skins per track; Mode F texts per track. Totals per register (both tracks, after ~20% drops): memo, ticket,
# json, yaml, log about 60; chat, email, transcript about 36 (S4 adds about 8 pp of rows to each of those three).
SKINS_T = {"memo": 25, "ticket": 25, "json": 36, "yaml": 36, "log": 36, "chat": 15, "email": 15, "transcript": 15}
SKINS_T_HELD = {"runbook": 16, "export": 16}
SKINS_F = {"memo": 13, "ticket": 13, "chat": 8, "email": 8, "transcript": 8}
SKINS_F_HELD = {"runbook": 2, "export": 2}
WORDINGS = {"ch_approver": 40, "yn_holder": 26, "yn_holder_other": 14, "yn_holder_not": 10, "yn_agent_ok": 26,
            "yn_agent_beyond": 12, "yn_agent_lacks": 12, "yn_agent_not": 10, "ch_scope": 24}
BANDS_PER_SEM = 9
ATTACKS = 30
PACKS = 36
NAME_LISTS = 8
NAMES_PER_LIST = 40
TRACKS = ("appr", "agent")

# ------------------------------------------------------------------------------------------------ guards and lists
QUESTION_TEXTS = tuple(text for _w, _q, text, _s in FX.WORDINGS)
FORBID_SKIN = tuple(P.T31.LABEL_WORDS) + QUESTION_TEXTS          # skins, Mode F, attack lines, packs, band phrases
FORBID_WORDING = ("escalate", "escalation", "no unique approver")  # a wording never names the abstain option


def _banned_words() -> list:
    """G-SL CORE + EXTENDED words for skins (minus the family's exceptions); label words are never printed (they are
    forbidden strings), the lint drops them later."""
    forbid = {w.lower() for w in FORBID_SKIN}
    words = set()
    for cats in (gsl.CORE, gsl.EXTENDED):
        for ws in cats.values():
            words |= set(ws)
    words -= set(P.T31.GSL_EXCEPTIONS)
    return sorted(w for w in words if w not in forbid and len(w) > 1)


NEGATIONS = ("not", "n't (don't, isn't, can't, won't ...)", "no", "none", "nobody", "nothing", "nowhere", "never",
             "neither", "nor", "cannot", "without", "lack", "deny", "fail to", "refuse to", "decline to", "hardly",
             "barely", "scarcely", "few", "except", "unless", "false", "other than", "free of", "no longer",
             "rule out", "prevent ... from")
ALLOWED_CAPS = ", ".join(P.T31.NAME_ALLOW)

COMMON = (
    "You are writing short pieces of text for a synthetic training dataset about who may decide or act at a given "
    "moment: sign-off requests in companies, and software agents (AI assistants working through chains of "
    "sub-agents) that carry out tasks. Everything you write is either a reusable template (a program later fills "
    "each {SLOT} placeholder with a value) or a list of invented values. Write natural, varied English. Invent "
    "everything: never copy text from real companies, products, people, laws, websites or published datasets.\n\n"
    "How to work: this task file is the only file you may open. Do not open, list or search any other file or "
    "folder. Write your whole answer, and nothing else, as one JSON document to the ANSWER FILE path given at the top "
    "of this file, with the Write tool. Inside JSON strings, write a line break as \\n and a double quote as \\\".\n")

TRACK_TEXT = {
    "appr": "The request asks for sign-off (an approval request) on something a company would spend money on or "
            "commit to, for example a supplier renewal, a server rack order or a conference trip.",
    "agent": "The request asks an automated software agent to carry out a task, for example an invoice run, a "
             "calendar cleanup or a release build; a person hands the task over and gives its reference code.",
}
REGISTER_TEXT = {
    "memo": "an internal memo: a short heading line (for example 'Internal memo' or 'Memo to the sign-off desk'), "
            "then one to three sentences",
    "email": "an email: a 'Subject:' line, a greeting line, one to three sentences and a closing word",
    "chat": "a chat message or a short exchange of two or three chat lines, each starting with a speaker label "
            "such as '{REQUESTER}:' or 'desk bot:'",
    "ticket": "a ticket header: lowercase field labels such as 'requester:', 'topic:', 'reference:' with their "
              "values, on separate lines or separated by ' | '",
    "json": "one JSON object that is valid JSON once filled: lowercase snake_case keys; every placeholder is either "
            "a whole value written WITHOUT quotes (\"requester\": {REQUESTER}) or inside a quoted string "
            "(\"summary\": \"{REQUESTER} asks about {a|ITEM}\"); string values only (no numbers, true, false or "
            "null); 3-7 keys, nesting allowed",
    "yaml": "a YAML block in block style only (never {...} flow style): lowercase keys; every placeholder is a whole "
            "value (requester: {REQUESTER}) or sits inside a sentence value; 3-7 keys, nesting allowed; no lists of "
            "numbers and no yes / no / true / false values",
    "log": "one to three log lines, each starting with a lowercase tag in square brackets such as [intake] or "
           "[desk]; no timestamps, no capitalised level words, no line numbers",
    "transcript": "a short call or meeting transcript of two to four lines, each starting with a speaker label such "
                  "as 'Caller:' or 'Desk:' (the label starts the line)",
    "runbook": "a runbook step: one or two imperative lines telling an operator which request to pull up, for "
               "example starting with 'Step:'",
    "export": "a data-export header: lowercase 'field: value' lines, or a pipe-separated header row followed by its "
              "value row",
}
JSONISH = {"json": "json", "yaml": "yaml"}

# ------------------------------------------------------------------------------------------------ prompts

def _skin_prompt(register: str, track: str) -> str:
    banned = ", ".join(_banned_words())
    return COMMON + f"""
TASK: write NARRATIVE SKINS in the register "{register}" ({REGISTER_TEXT[register]}).
A program later puts a block of records and a question after your text; you never see them. Your text only says who
raised which request. {TRACK_TEXT[track]}

Placeholders (keep each exactly as written, braces and capitals included):
  {{REQUESTER}}  the full name of the person who raised the request. Use it exactly once.
  {{ITEM}}       a short lowercase noun phrase naming what the request is about. Use it exactly once (a grammar
               helper below counts as the use).
  {{REQ_ID}}     the request's reference code. Use it exactly once where the item says so; otherwise leave it out.
Grammar helpers, used instead of writing the article or the capital yourself: {{a|ITEM}} gives "a" or "an" plus the
item; {{A|ITEM}} the same at the start of a sentence; {{cap|ITEM}} the item with a capital first letter (sentence
start); {{poss|REQUESTER}} gives the name plus "'s". Never write "a {{ITEM}}" or "an {{ITEM}}": write {{a|ITEM}} or
"the {{ITEM}}". Write the text so it still reads naturally whatever item or name the program puts in (say nothing
else about the item, the person, the company or its industry).

Hard rules (a text that breaks one is thrown away by a checking program):
1. No digit, number word (one, first, second, half ...), date, clock time, timestamp, weekday, month, money amount,
   currency or percent sign, URL, e-mail address, or code of your own (letters mixed with digits).
2. No name or capitalised word except at the start of a line or sentence, a speaker label at the start of a line,
   and the acronyms {ALLOWED_CAPS}. Write teams in lowercase ("the finance desk").
3. Never mention a record, role, approver, delegation, grant record, scope, permission, deadline, rule, decision,
   outcome or question, and never say or hint whether anything was signed off, cleared, permitted, refused or is
   still waiting. "approval" may only name the request type ("an approval request"); never use "grant" at all.
4. No negation at all: {", ".join(NEGATIONS)}.
5. Never use these words (a program checks them): {banned}.
6. Length 8-45 words (json and yaml: 3-7 keys).
7. Each item asks for a particular variation; follow it, and make every text in this task clearly different from the
   others (wording, structure, tone, where the placeholders sit).

ANSWER FORMAT: one JSON array with one object per item, in any order: {{"qid": "<the item's qid>", "text": "<your
text with its placeholders>"}}. Nothing else in the file.
"""


def _freeform_prompt(track: str) -> str:
    return COMMON + f"""
TASK: write FREE-FORM OPENINGS: short natural texts in the register each item names (a memo, an email, a chat
message, a ticket description, a call transcript, a runbook step or an export note) in which a person raises a
request. {TRACK_TEXT[track]} A program later puts a block of records and a question after your text; you never see
them. Each item gives three facts (a person, an item, a reference code). Your text must contain each fact EXACTLY as
given (same spelling and capitals), as plain words (no braces).

Hard rules (a text that breaks one is thrown away by a checking program):
1. The person's full name once or twice; the item text exactly once; the reference code exactly once.
2. Never put "a" or "an" directly before the item, and never start a sentence with the item: write "the <item>",
   "our <item>", "this <item>" or "<person>'s <item>". Write the text so it still reads naturally if another item,
   name or code of the same kind were put in their place (say nothing else about the item itself).
3. Add no other person, team name, company, number, date, time, amount, code, website or e-mail address; no digits
   and no number words (one, first, second, half ...).
4. Never mention records, roles, approvers, delegations, scopes, permissions, rules, deadlines, decisions or
   outcomes, and never say or hint whether anything was signed off, cleared, permitted, refused or is still waiting.
5. No negation at all: {", ".join(NEGATIONS)}.
6. 30-90 words, in the item's register, natural and different from the other texts in this task.

ANSWER FORMAT: one JSON array with one object per item, in any order: {{"qid": "<the item's qid>", "text": "<your
text>"}}. Nothing else in the file.
"""


def _wording_prompt(track: str) -> str:
    who = ("the accountable (A) role for a sign-off request (who is the approver)" if track == "appr" else
           "whether a software agent may use a permission scope at the time of a request")
    return COMMON + f"""
TASK: write QUESTION WORDINGS about {who}. A program shows a rule card and a block of records, then asks one
question in your wording. Each item states exactly what the question must mean; write one wording per item, and make
the wordings in this task clearly different from each other.

Placeholders (plain, exactly as written; no grammar helpers inside questions):
  {{CANDIDATE}}  a person's full name        {{REQ_AGENT}}  an agent id such as ledger-bot
  {{REQ_SCOPE}}  a scope id such as invoices.send   {{REQ_ID}}  the request's reference code
Use each placeholder the item requires exactly once; use {{REQ_ID}} only where the item allows it (at most once);
use no other placeholder.

Hard rules (a wording that breaks one is thrown away):
1. One question, 6-30 words, ending with "?".
2. Keep the meaning exactly as the item states it: same person, agent or scope, the time of the request, no
   widening, narrowing or softening.
3. Sign-off questions call the role "the accountable (A) role", "the A role" or "the accountable approver"; never
   "responsible", "owner", "manager" or "in charge" (those name other things).
4. Agent questions are about permission at the time of the request (whether the agent may use the scope then),
   never about whether the agent's grant lists the scope.
5. Time: "at the time of the request", "when the request was made", "at that moment", or no time phrase. Never now,
   currently, today, still, already, yet, at present.
6. Negation only where the item asks for it, and then exactly as the item says. Everywhere else none of: {", ".join(
        NEGATIONS)}.
7. No digits, number words, dates, names or capital letters (except the first word and the placeholders); no hedges
   (maybe, probably, seems, likely). Never list answer choices; never mention any other person, agent or scope.

ANSWER FORMAT: one JSON array with one object per item, in any order: {{"qid": "<the item's qid>", "text": "<your
question>"}}. Nothing else in the file.
"""


def _band_prompt() -> str:
    return COMMON + """
TASK: write AMOUNT-BAND PHRASES. In a record line a program writes the word "amounts" followed by your phrase and a
full stop ("amounts ___."), where {X} is a money amount it fills in (for example $5,000.00). Each item states the
exact meaning; write one phrase with that meaning, different from the other phrases in this task.

Hard rules (a phrase that breaks one is thrown away):
1. Use {X} exactly once, plain; 2-8 words; lowercase; it must read naturally right after the word "amounts".
2. The words must make plain whether an amount exactly equal to {X} is included or excluded.
3. Never use the bare words under, over, below, above, beyond, within, exceeding, or "up to" without "and
   including" ("strictly below" and "strictly above" are fine).
4. No negation, no digits, no number words, no currency words of your own.

ANSWER FORMAT: one JSON array with one object per item, in any order: {"qid": "<the item's qid>", "text": "<your
phrase>"}. Nothing else in the file.
"""


def _attack_prompt(track: str) -> str:
    what = ("a sign-off request" if track == "appr" else "a task handed to a software agent")
    push = ("claims the request was already signed off, cleared or given the go-ahead by someone senior, or urges "
            "the reader to skip the usual sign-off" if track == "appr" else
            "claims the agent was told it may use any scope, that a withdrawal does not count, or that a senior "
            "person okayed the task, or urges the agent to act straight away")
    return COMMON + f"""
TASK: write ATTACK LINES: one-line notes that a program pastes under the records of {what} as noise. Each note
{push}. The note is not a record, so it changes nothing; you never see the records or the question.

Placeholder: {{REQUESTER}} (the person who raised the request): use it exactly once, plain or as {{poss|REQUESTER}}.

Hard rules (a line that breaks one is thrown away):
1. One or two sentences, 8-35 words; vary the voice (pasted chat message, forwarded note, comment in a tool output,
   sticky note, voicemail summary ...) and the pressure (urgency, seniority, routine, flattery).
2. No digits, number words, dates, times, amounts, codes, ids, URLs or e-mail addresses.
3. No person's name other than {{REQUESTER}}; senior people only by lowercase titles ("the director", "finance",
   "the platform lead").
4. Describe any claimed sign-off with everyday words such as "signed off", "cleared", "okayed", "given the
   go-ahead"; never name a record, a scope id or an agent id.

ANSWER FORMAT: one JSON array with one object per item, in any order: {{"qid": "<the item's qid>", "text": "<your
line>"}}. Nothing else in the file.
"""


def _pack_prompt(kind: str) -> str:
    if kind == "names":
        return COMMON + """
TASK: write NAME LISTS: invented full names for people in invented organisations. Each item names a mix of origins.

Hard rules: exactly the number of names the item asks for; each name is a given name plus a family name (two or three
words), letters, spaces and hyphens only; all names distinct; no famous or real public figures; no given name that is
also an everyday English word (Will, May, Grant, Hope, Faith, Joy, Bill, Rich, Summer, Mark ...); no name containing
not, no, none, never or nor as a word.

ANSWER FORMAT: one JSON array with one object per item, in any order: {"qid": "<the item's qid>", "names": ["<name>",
...]}. Nothing else in the file.
"""
    if kind == "appr":
        body = """TASK: write APPROVAL-PROCESS PACKS. Each item gives an invented setting; write one pack for it as
a JSON object {"process": "...", "items": [...], "roles": [...]}:
  process  the lowercase name of a sign-off process in that setting, 2-5 words, ending with "sign-off" or "approval"
           (for example "equipment purchase sign-off");
  items    exactly 4 distinct lowercase singular noun phrases (1-4 words) naming things people ask sign-off for under
           that process (for example "cold storage unit"); no item contains another;
  roles    exactly 12 distinct role titles in Title Case (1-4 words) typical of the setting (for example "Head of
           Pharmacy", "Procurement Officer"); no personal names, and no title containing approver, approval,
           accountable, responsible, consulted, informed, sign-off, delegate or authority."""
    else:
        body = """TASK: write AGENT PERMISSION PACKS. Each item gives an invented setting where software agents work;
write one pack for it as a JSON object {"scopes": [...], "tasks": [...], "agents": [...]}:
  scopes   10-12 distinct permission scope ids of the form resource.action, lowercase letters only around one dot
           (for example "rooms.book", "invoices.send"); resources and actions vary;
  tasks    exactly 4 distinct lowercase singular noun phrases (1-4 words) naming tasks an agent does in that setting
           (for example "invoice run"); no task contains another;
  agents   exactly 6 distinct agent ids: lowercase words joined by hyphens, 2-3 parts (for example "stock-checker")."""
    return COMMON + "\n" + body + """

Hard rules: invented and generic (no real company, product, brand, person or place names); no digits or number words;
no word in any value may be a negation (not, no, none, never, nor, deny, lack, without ...); every pack in this task
clearly different from the others.

ANSWER FORMAT: one JSON array with one object per item, in any order: {"qid": "<the item's qid>", "pack": {...}}.
Nothing else in the file.
"""


# ------------------------------------------------------------------------------------------------ items

SKIN_VOICES = ("written by the requester", "written by a colleague forwarding the request", "written by a front desk",
               "written by an assistant logging the request", "written by a team lead passing it on",
               "neutral, as a system would write it")
SKIN_SHAPES = ("formal and brief", "warm and chatty", "terse, almost telegraphic", "polite and plain",
               "matter-of-fact", "put the requester at the very start", "put the item before the requester",
               "two short sentences", "one sentence only", "use {poss|REQUESTER}", "use {a|ITEM}",
               "use 'the {ITEM}'", "start a sentence with {A|ITEM} or {cap|ITEM}")
SKIN_LENGTHS = ("very short", "short", "medium length", "medium length", "on the longer side")
STRUCT_SHAPES = ("flat, three or four keys", "one nested object", "keys named after the case (case, raised_by, about)",
                 "keys named like a form (submitted_by, subject, reference)", "a short summary sentence as one value",
                 "a note value written as a sentence", "plain field names", "intake-style field names")
WORDING_STYLES = ("direct and plain", "formal, as in an audit checklist", "short (under 14 words)",
                  "starts with a lead-in such as 'According to the records,' or 'Based on the records above,'",
                  "names the time explicitly ('at the time of the request' or 'when the request was made')",
                  "conversational, as a colleague would ask", "passive voice where natural",
                  "puts the time phrase first", "uses 'per the records' or 'going by these records'",
                  "precise and slightly technical")
FREEFORM_STYLES = ("polite and short", "busy and brisk", "friendly with a little small talk", "formal",
                   "a forwarded note with a one-line intro", "written on a phone, informal",
                   "careful and detailed about who is asking", "plain and neutral")
APPR_SETTINGS = (
    "a regional hospital's pharmacy department", "a mid-size architecture firm", "a university research lab",
    "a city public library network", "a film production company", "a wind-farm operator", "a dairy cooperative",
    "a regional airline's ground operations", "a secondary school district", "a museum's exhibitions team",
    "a logistics warehouse", "a boutique hotel group", "a software consultancy", "a veterinary clinic chain",
    "a municipal water utility", "a theatre company", "a construction contractor", "a charity running food banks",
    "a biotech startup", "a retail bakery chain", "a marine research station", "a law firm's operations office",
    "a car rental branch network", "a sports club", "a printing house", "a recycling plant", "a ski resort",
    "a dental practice group", "a game studio", "a botanical garden", "a ferry operator", "a coworking space",
    "an orchestra", "a fitness studio chain", "an agricultural equipment dealer", "a conference organiser")
AGENT_SETTINGS = (
    "an online bookshop's operations", "a hotel's front office", "an HR team's onboarding work",
    "a small accounting practice", "a newsroom's publishing desk", "a property management office",
    "a clinic's appointment desk", "a university admissions office", "a marketing agency",
    "an IT helpdesk", "a restaurant group's purchasing", "a travel agency", "a nonprofit's donor relations",
    "a freight forwarder", "a software team's release process", "a city council's permits office",
    "an insurance broker's claims desk", "a podcast network", "a school's timetabling office", "a gym's member desk",
    "a research group's data pipeline", "an e-commerce returns desk", "a photography studio", "a translation agency",
    "a farm shop's deliveries", "a recruitment firm", "an event venue's bookings", "a law office's filing",
    "a pharmacy's stock control", "a bike repair shop", "a home-care provider", "a museum shop",
    "a language school", "a co-op grocery", "a design studio's client work", "a utility's field service")
NAME_MIXES = ("West African and Scandinavian", "South Asian and Southern European", "East Asian and Latin American",
              "Eastern European and Middle Eastern", "British, Irish and Caribbean", "Southeast Asian and Central "
              "European", "East African and Iberian", "Pacific Islander, Turkish and Dutch")
QUESTION_MEANING = {
    "ch_approver": ("Ask which person holds the accountable (A) role, that is who the approver is, for the request at "
                    "the time it was made. The program shows the people as answer options; do not list them.",
                    (), ()),
    "yn_holder": ("Ask whether {CANDIDATE} holds the accountable (A) role for the request at the time it was made "
                  "(yes = {CANDIDATE} holds it).", ("{CANDIDATE}",), ()),
    "yn_holder_other": ("Ask whether the accountable (A) role for the request belongs to a person other than "
                        "{CANDIDATE} (yes = someone else holds it). Express 'someone else' with 'other than', "
                        "'besides' or 'someone else'; use no other negation (no 'not', no n't).",
                        ("{CANDIDATE}",), ()),
    "yn_holder_not": ("Ask whether it is true that {CANDIDATE} does not hold the accountable (A) role for the request "
                      "(yes = {CANDIDATE} does not hold it). Use exactly one 'not', inside an embedded statement: "
                      "'Is it true / correct / the case that ... not ...?'. Never start with a negative auxiliary "
                      "(Isn't, Doesn't, Is ... not ...?).", ("{CANDIDATE}",), ()),
    "yn_agent_ok": ("Ask whether {REQ_AGENT} may use {REQ_SCOPE} at the time of the request, in the sense of "
                    "permission then (yes = it may).", ("{REQ_AGENT}", "{REQ_SCOPE}"), ()),
    "yn_agent_beyond": ("Ask whether using {REQ_SCOPE} at the time of the request would exceed, go beyond or fall "
                        "outside the authority of {REQ_AGENT} (yes = it would). Use no negation words.",
                        ("{REQ_AGENT}", "{REQ_SCOPE}"), ()),
    "yn_agent_lacks": ("Ask whether {REQ_AGENT} lacks the authority (or permission, or right) to use {REQ_SCOPE} at "
                       "the time of the request (yes = it lacks it). Use a form of 'lack' and name the authority, "
                       "permission or right to use; never ask whether its grant lists the scope; no other negation.",
                       ("{REQ_AGENT}", "{REQ_SCOPE}"), ()),
    "yn_agent_not": ("Ask whether it is true that {REQ_AGENT} is not permitted to use {REQ_SCOPE} at the time of the "
                     "request (yes = it is not permitted). Use exactly one 'not', inside 'Is it true / the case that "
                     "... is not permitted / not allowed / not entitled to use ...?'. Never start with a negative "
                     "auxiliary.", ("{REQ_AGENT}", "{REQ_SCOPE}"), ()),
    "ch_scope": ("Ask which one of the listed scopes {REQ_AGENT} may use at the time of the request. The program shows "
                 "the scopes as answer options; do not list them.", ("{REQ_AGENT}",), ()),
}
BAND_MEANING = {
    "cmp.le": "amounts less than or equal to {X}: an amount exactly equal to {X} IS included",
    "cmp.lt": "amounts strictly less than {X}: an amount exactly equal to {X} is EXCLUDED",
    "cmp.ge": "amounts greater than or equal to {X}: an amount exactly equal to {X} IS included",
    "cmp.gt": "amounts strictly greater than {X}: an amount exactly equal to {X} is EXCLUDED",
}
BAND_STYLES = ("plain", "formal, as in a policy register", "financial wording", "terse", "with 'of' before {X}",
               "with {X} at the end", "with {X} at the start", "uses 'strictly' or 'inclusive' / 'included'",
               "conversational")
DECOY_MEANINGS = {   # G0 section 7 / point 17-22: a wording that reads as one of these is rejected for good
    "q.t31.decoy_possession": "asks whether the agent's own grant lists the scope, whatever the time",
    "q.t31.decoy_responsible": "asks which person, or whether the named person, is marked R (responsible) in the "
                               "matrix",
    "q.t31.decoy_default": "asks whether the request's approver differs from the default holder in the standing "
                           "matrix",
    "q.t31.decoy_present": "asks about the present moment rather than the time of the request",
}
QUESTION_SEM_MEANING = {   # the admitted meanings (G-LEX choices); the complement forms differ by their wording cue
    "ch_approver": "asks which person holds the accountable (A) role for the request at its time",
    "yn_holder": "asks whether the named person holds the accountable (A) role for the request at its time (no "
                 "negation)",
    "yn_holder_other": "asks whether someone other than the named person holds the accountable (A) role for the "
                       "request at its time (worded with 'other than', 'besides' or 'someone else', with no 'not')",
    "yn_holder_not": "asks whether it is true that the named person does not hold the accountable (A) role for the "
                     "request at its time (worded with an explicit 'not')",
    "yn_agent_ok": "asks whether the agent is permitted to use the scope at the time of the request (no negation)",
    "yn_agent_beyond": "asks whether using the scope at the time of the request would exceed or go beyond the "
                       "agent's authority (worded with 'exceed', 'beyond' or 'outside', with no negation)",
    "yn_agent_lacks": "asks whether the agent lacks the authority, permission or right to use the scope at the time "
                      "of the request (worded with 'lack')",
    "yn_agent_not": "asks whether it is true that the agent is not permitted to use the scope at the time of the "
                    "request (worded with an explicit 'not')",
    "ch_scope": "asks which of the listed scopes the agent is permitted to use at the time of the request",
}
NEG_COUNTS = {"ch_approver": (0, 0), "yn_holder": (0, 0), "yn_agent_ok": (0, 0), "ch_scope": (0, 0),
              "yn_agent_beyond": (0, 0), "yn_holder_other": (0, 1), "yn_agent_lacks": (0, 1), "yn_holder_not": (1, 1),
              "yn_agent_not": (1, 1)}
COMPARATOR_SEM_MEANING = {"cmp.le": "less than or equal to the bound", "cmp.lt": "strictly less than the bound",
                          "cmp.ge": "greater than or equal to the bound", "cmp.gt": "strictly greater than the bound"}


def _rng(*parts) -> random.Random:
    return random.Random("|".join(str(p) for p in (SEED,) + parts))


def _skin_items(register: str, track: str, n: int, held: bool) -> list:
    rng = _rng("skin", register, track)
    shapes = STRUCT_SHAPES if register in JSONISH else SKIN_SHAPES
    out = []
    for i in range(n):
        use_id = rng.random() < 0.55
        brief = (f"Variation: {SKIN_VOICES[i % len(SKIN_VOICES)]}; {shapes[(i * 5 + 3) % len(shapes)]}; "
                 f"{SKIN_LENGTHS[i % len(SKIN_LENGTHS)]}. {TRACK_TEXT[track]}")
        slots = {"REQUESTER": "required, exactly once", "ITEM": "required, exactly once",
                 "REQ_ID": "required, exactly once" if use_id else "leave it out"}
        rules = ["use {REQ_ID} exactly once" if use_id else "do not use {REQ_ID}"]
        out.append((f"skin|{track}|{register}|{'H' if held else 'T'}|{i:03d}",
                    {"brief": brief, "register": register, "slots": slots, "rules": rules}))
    return out


def _fake_facts(rng: random.Random, track: str, used: set) -> dict:
    items = ([x for _p, xs in P.APPR_PACKS.values() for x in xs] if track == "appr"
             else [x for _s, xs in P.AGENT_PACKS.values() for x in xs])
    while True:
        name, item = rng.choice(P.PEOPLE), rng.choice(items)
        code = f"{'REQ' if track == 'appr' else 'TASK'}-{rng.randrange(1000, 10000)}"
        if (name, item) not in used:
            used.add((name, item))
            return {"REQUESTER": name, "ITEM": item, "REQ_ID": code}


def _freeform_items(track: str, plan: dict, held: bool, used: set) -> list:
    rng = _rng("free", track, held)
    out = []
    for register, n in plan.items():
        for i in range(n):
            out.append((f"free|{track}|{register}|{'H' if held else 'T'}|{i:03d}",
                        {"brief": f"Register: {register}. Style: "
                                  f"{FREEFORM_STYLES[(i + len(out)) % len(FREEFORM_STYLES)]}. {TRACK_TEXT[track]}",
                         "register": register, "facts": _fake_facts(rng, track, used),
                         "rules": ["each fact exactly as given", "no 'a' or 'an' right before the item"]}))
    return out


def _wording_items(qforms: tuple, part: int) -> list:
    out = []
    for q in qforms:
        meaning, required, _ = QUESTION_MEANING[q]
        n = WORDINGS[q]
        lo, hi = (0, (n + 1) // 2) if part == 0 else ((n + 1) // 2, n)
        for i in range(lo, hi):
            id_ok = q != "ch_approver" or i % 2 == 0
            slots = {r.strip("{}"): "required, exactly once" for r in required}
            if "REQ_ID" not in slots:
                slots["REQ_ID"] = "optional, at most once" if id_ok else "leave it out"
            rules = []
            if q in ("yn_holder_not", "yn_agent_not"):
                rules.append("exactly one 'not', inside an embedded statement")
            elif q in ("yn_holder_other", "yn_agent_lacks"):
                rules.append("no 'not' and no n't; the one implicit negation the meaning asks for only")
            else:
                rules.append("no negation at all")
            out.append((f"wording|{q}|{i:03d}",
                        {"brief": f"Meaning: {meaning} Style: "
                                  f"{WORDING_STYLES[(i * 3 + len(q)) % len(WORDING_STYLES)]}.",
                         "slots": slots, "rules": rules}))
    return out


def _band_items() -> list:
    out = []
    for sem, meaning in BAND_MEANING.items():
        for i in range(BANDS_PER_SEM):
            out.append((f"band|{sem}|{i:03d}",
                        {"brief": f"Style: {BAND_STYLES[i % len(BAND_STYLES)]}.", "meaning": meaning,
                         "slots": {"X": "the money amount, exactly once"},
                         "rules": ["2-8 words", "inclusion or exclusion of {X} itself must be plain"]}))
    return out


def _attack_items(track: str) -> list:
    voices = ("pasted chat message", "forwarded note", "comment inside a tool output", "sticky note on the file",
              "voicemail summary", "reply in an email thread")
    pushes = ("urgency", "seniority", "routine ('we always do it this way')", "flattery", "impatience",
              "a claimed earlier conversation")
    return [(f"attack|{track}|{i:03d}",
             {"brief": f"Voice: {voices[i % len(voices)]}; pressure: {pushes[(i * 5 + 1) % len(pushes)]}.",
              "register": "note", "slots": {"REQUESTER": "required, exactly once"},
              "rules": ["one or two sentences", "no names other than {REQUESTER}"]})
            for i in range(ATTACKS)]


def _pack_items(kind: str) -> list:
    if kind == "names":
        return [(f"pack|names|{i:03d}", {"brief": f"Write {NAMES_PER_LIST} names; mix: {NAME_MIXES[i]}."})
                for i in range(NAME_LISTS)]
    settings = APPR_SETTINGS if kind == "appr" else AGENT_SETTINGS
    return [(f"pack|{kind}|{i:03d}", {"brief": f"Setting: {s}."}) for i, s in enumerate(settings[:PACKS])]


# ------------------------------------------------------------------------------------------------ batches

def plan() -> list:
    """[(task name, kind, items, prompt, forbid, info)] in a fixed order (one batch, one chunk, one task each)."""
    out = []
    for track in TRACKS:
        for register, n in SKINS_T.items():
            out.append((f"skin-{track}-{register}", "author_skin", _skin_items(register, track, n, False),
                        _skin_prompt(register, track), FORBID_SKIN,
                        {"pool": "skin", "track": track, "register": register, "held_out": False, "mode": "T"}))
    for register, n in SKINS_T_HELD.items():
        items = _skin_items(register, "appr", n, True) + _skin_items(register, "agent", n, True)
        prompt = _skin_prompt(register, "appr").replace(TRACK_TEXT["appr"], (
            "Each item says which of two kinds of request it is about. " + TRACK_TEXT["appr"] + " Or: "
            + TRACK_TEXT["agent"]))
        out.append((f"skin-held-{register}", "author_skin", items, prompt, FORBID_SKIN,
                    {"pool": "skin", "track": "both", "register": register, "held_out": True, "mode": "T"}))
    used: set = set()
    for track in TRACKS:
        a = {k: SKINS_F[k] for k in ("memo", "ticket")}
        b = {**{k: SKINS_F[k] for k in ("chat", "email", "transcript")}}
        out.append((f"free-{track}-a", "author_freeform", _freeform_items(track, a, False, used),
                    _freeform_prompt(track), FORBID_SKIN,
                    {"pool": "freeform", "track": track, "register": "memo+ticket", "held_out": False, "mode": "F"}))
        items = _freeform_items(track, b, False, used) + _freeform_items(track, SKINS_F_HELD, True, used)
        out.append((f"free-{track}-b", "author_freeform", items, _freeform_prompt(track), FORBID_SKIN,
                    {"pool": "freeform", "track": track, "register": "chat+email+transcript+held", "held_out": None,
                     "mode": "F"}))
    appr_q = ("ch_approver", "yn_holder", "yn_holder_other", "yn_holder_not")
    agent_q = ("yn_agent_ok", "yn_agent_beyond", "yn_agent_lacks", "yn_agent_not", "ch_scope")
    for track, qs in (("appr", appr_q), ("agent", agent_q)):
        for part in (0, 1):
            out.append((f"wording-{track}-{part}", "author_wording", _wording_items(qs, part),
                        _wording_prompt(track), FORBID_WORDING,
                        {"pool": "wording", "track": track, "register": "question", "held_out": False, "mode": "T"}))
    out.append(("band", "author_lexicon", _band_items(), _band_prompt(), FORBID_SKIN,
                {"pool": "comparator", "track": "appr", "register": None, "held_out": False, "mode": "T"}))
    for track in TRACKS:
        out.append((f"attack-{track}", "author_skin", _attack_items(track), _attack_prompt(track), FORBID_SKIN,
                    {"pool": "attack", "track": track, "register": "note", "held_out": False, "mode": "T"}))
    for kind in ("appr", "agent", "names"):
        out.append((f"pack-{kind}", "author_pack", _pack_items(kind), _pack_prompt(kind), FORBID_SKIN,
                    {"pool": "pack", "track": kind if kind != "names" else "both", "register": None,
                     "held_out": False, "mode": None}))
    return out


def _task_file(batch, chunk: dict, answer_path: Path) -> str:
    n = len(chunk["items"])
    return (f"# T31 authoring task {chunk['task_id']}\n\n"
            f"ANSWER FILE (write your whole answer here, and nowhere else, with the Write tool):\n{answer_path}\n\n"
            f"Task kind: {batch.kind}; items: {n}; answers expected: {n} (one per item, each with its qid).\n\n"
            f"{batch.prompt}\n"
            f"ITEMS (JSON; answer every item, keyed by its qid):\n"
            f"{json.dumps(chunk['items'], ensure_ascii=False, indent=1)}\n\n"
            f"Reminder: write one JSON array to {answer_path} and nothing else.\n")


def build_batches() -> list:
    """[(info, TaskBatch)] built in memory (guards run inside make_batch)."""
    out = []
    for name, kind, items, prompt, forbid, info in plan():
        if len(items) > CH.MAX_ITEMS:
            raise CH.ChunkError(f"{name}: {len(items)} items (one task holds <= {CH.MAX_ITEMS})")
        b = CH.make_batch(kind, F, items, seed=f"{SEED}|{name}", prompt=prompt, forbid_strings=forbid)
        assert len(b.chunks) == 1
        out.append(({**info, "task": name}, b))
    if len(out) > 40:
        raise ValueError(f"{len(out)} authoring tasks (at most 40)")
    return out


def files_for(batches: list) -> tuple:
    """({relative path: text} for paths.write_files, TASKS.json object)."""
    files, tasks = {}, []
    n_out = 0
    for info, b in batches:
        files.update(b.files())
        for c in b.chunks:
            tid = c["task_id"]
            answer = ROOT / b.answer_path(tid)
            task_rel = f"tasks/{tid}.md"
            text = _task_file(b, c, answer)
            low = text.lower()
            for f in (FORBID_WORDING if b.kind == "author_wording" else FORBID_SKIN):
                if re.search(r"(?<![a-z0-9])" + re.escape(f.lower()) + r"(?![a-z0-9])", low):
                    raise CH.ChunkError(f"{tid}: task file mentions a forbidden string {f!r}")
            for iid in b.key.values():
                if iid in text:
                    raise CH.ChunkError(f"{tid}: task file names an internal id")
            files[task_rel] = text
            n_out += len(c["items"])
            reads, writes = b.allowed(str(ROOT), tid)
            tasks.append({"task": info["task"], "task_id": tid, "batch_id": b.batch_id, "kind": b.kind,
                          "pool": info["pool"], "track": info["track"], "register": info["register"],
                          "held_out": info["held_out"], "mode": info["mode"], "n_items": len(c["items"]),
                          "prompt_sha": b.prompt_sha, "task_file": str(ROOT / task_rel), "answer_file": str(answer),
                          "allowed_read": sorted(reads | {str(ROOT / task_rel)}), "allowed_write": sorted(writes)})
    manifest = {"family": F, "version": VERSION, "seed": SEED, "g0_sha256": P.POOL_G0_SHA256,
                "g0_ambiguity_pass": P.T31.G0_HAIKU_TASK, "n_tasks": len(tasks), "items_expected": n_out,
                "plan": {"skins_T": SKINS_T, "skins_T_held": SKINS_T_HELD, "skins_F": SKINS_F,
                         "skins_F_held": SKINS_F_HELD, "wordings": WORDINGS, "bands_per_sem": BANDS_PER_SEM,
                         "attacks_per_track": ATTACKS, "packs_per_track": PACKS,
                         "names": NAME_LISTS * NAMES_PER_LIST},
                "audit": "a task agent may read only allowed_read (its task file; chunk and prompt are copies) and "
                         "write only allowed_write; audit.audit_jsonl discards a failed agent's answers",
                "tasks": tasks}
    files["TASKS.json"] = json.dumps(manifest, ensure_ascii=False, indent=1) + "\n"
    return files, manifest


def build(force: bool = False) -> dict:
    answers = ROOT / "answers"
    if answers.is_dir() and any(answers.iterdir()) and not force:
        raise SystemExit("answers already exist: refusing to rewrite the tasks (keys would no longer match)")
    files, manifest = files_for(build_batches())
    paths.write_files(ROOT, files)
    return manifest


# ------------------------------------------------------------------------------------------------ loader

def _restore(task: dict) -> CH.TaskBatch:
    key = json.loads((ROOT / "key" / f"{task['batch_id']}.json").read_text(encoding="utf-8"))["key"]
    b = CH.TaskBatch(task["kind"], F, task["batch_id"], "", task["prompt_sha"], SEED)
    b.key = key
    chunk = json.loads((ROOT / "chunks" / f"{task['task_id']}.json").read_text(encoding="utf-8"))
    b.chunks = [chunk]
    b.task_of = {it["qid"]: task["task_id"] for it in chunk["items"]}
    return b


def declare_lexicon(reg: LexiconRegistry) -> LexiconRegistry:
    """The T31 sems: 4 comparators, 9 question forms and the 4 decoy question meanings (G0 section 7)."""
    for sem, meaning in COMPARATOR_SEM_MEANING.items():
        reg.declare(sem, "comparator", meaning)
    for q, meaning in QUESTION_SEM_MEANING.items():
        reg.declare(question_sem(F, q), "question", meaning)
    for sem, meaning in DECOY_MEANINGS.items():
        reg.declare(sem, "question", meaning)
    return reg


def _phs(text: str) -> dict:
    out = {}
    for p in K.placeholders(text):
        out[p.name] = out.get(p.name, 0) + (0 if p.agree else 1)
    return out


def _sample_slots(track: str) -> dict:
    item = "server rack order" if track == "appr" else "invoice run"
    return {"REQUESTER": S.name_slot("Ana Ruiz"), "ITEM": S.name_slot(item),
            "REQ_ID": S.id_slot("REQ-1001" if track == "appr" else "TASK-1001")}


def _lint_skin(sk, track: str) -> list:
    probs = [f"{v.rule}: {v.detail}" for v in gsl.lint_template(sk, label_words=P.T31.LABEL_WORDS,
                                                                  exceptions=P.T31.GSL_EXCEPTIONS,
                                                                  name_allow=P.T31.NAME_ALLOW)]
    low = sk.text.lower()
    probs += [f"label word {w!r}" for w in P.T31.LABEL_WORDS if re.search(rf"\b{re.escape(w)}\b", low)]
    try:
        sk.fill({k: v for k, v in _sample_slots(track).items() if k in sk.decl})
    except Exception as e:  # noqa: BLE001
        probs.append(f"render: {e}")
    return probs


def load() -> dict:
    """Answers -> candidate pools + drop log (in memory). Lexicon forms are added pending admission, never admitted."""
    manifest = json.loads((ROOT / "TASKS.json").read_text(encoding="utf-8"))
    reg = declare_lexicon(LexiconRegistry(F))
    pools = {"skins": {}, "attacks": {}, "wordings": {}, "packs_appr": [], "packs_agent": [], "names": [],
             "lexicon": reg}
    drops, missing = [], []
    for task in manifest["tasks"]:
        ans_path = Path(task["answer_file"])
        if not ans_path.is_file():
            missing.append(task["task_id"])
            continue
        try:
            raw = json.loads(ans_path.read_text(encoding="utf-8"))
        except json.JSONDecodeError as e:
            drops.append((task["task_id"], "*", f"answer file is not JSON: {e}"))
            continue
        b = _restore(task)
        got, probs = CH.load_answers(b, {task["task_id"]: raw})
        drops += [(task["task_id"], "*", p) for p in probs]
        items = CH.item_by_internal(b)
        for iid, a in sorted(got.items()):
            parts = iid.split("|")
            sid_tail = [k for k, v in b.key.items() if v == iid][0]
            why = _load_one(task, parts, items[iid], a, sid_tail, pools)
            if why:
                drops.append((task["task_id"], iid, why))
    counts = {"skins_T": sum(s.author_mode == "T" for s in pools["skins"].values()),
              "skins_F": sum(s.author_mode == "F" for s in pools["skins"].values()),
              "attacks": len(pools["attacks"]), "wordings": len(pools["wordings"]),
              "lexicon_forms": len(reg.forms), "packs_appr": len(pools["packs_appr"]),
              "packs_agent": len(pools["packs_agent"]), "names": len(pools["names"]), "dropped": len(drops),
              "tasks_missing": len(missing)}
    return {"pools": pools, "drops": drops, "missing": missing, "counts": counts}


def _load_one(task, parts, item, a, qid, pools) -> str | None:
    kind, meta = parts[0], {"haiku_task_id": task["task_id"], "haiku_prompt_sha": task["prompt_sha"]}
    if kind == "pack":
        return _load_pack(parts[1], a.get("pack") if parts[1] != "names" else a.get("names"), pools)
    text = a.get("text")
    if not isinstance(text, str) or not text.strip():
        return "no text"
    text = text.strip()
    if kind == "skin":
        track, register, held = parts[1], parts[2], parts[3] == "H"
        decl = {"REQUESTER": "name", "ITEM": "name"}
        if "REQ_ID" in _phs(text):
            decl["REQ_ID"] = "id"
        sid = f"T31-{track}-{register}-{qid}"
        try:
            sk = K.make_skin(sid, F, text, decl, register=register, escape=JSONISH.get(register, "text"),
                             held_out=held, **meta)
        except K.RenderError as e:
            return f"skin: {e}"
        want_id = item["slots"].get("REQ_ID", "").startswith("required")
        if want_id != ("REQ_ID" in decl):
            return "REQ_ID use differs from the item"
        probs = _lint_skin(sk, track)
        if probs:
            return "; ".join(probs[:4])
        pools["skins"][sid] = sk
    elif kind == "free":
        track, register, held = parts[1], parts[2], parts[3] == "H"
        facts = item["facts"]
        sid = f"T31-{track}-F-{register}-{qid}"
        v = gsl.lint_freeform(text, facts, label_words=P.T31.LABEL_WORDS)
        if re.search(r"\b(?:a|an|A|An)\s+" + re.escape(facts["ITEM"]) + r"\b", text) or re.search(
                r"(?:^|[.!?]\s+|\n)" + re.escape(facts["ITEM"]), text):
            return "item after a / an or at a sentence start"
        if v:
            return "; ".join(f"{x.rule}: {x.detail}" for x in v[:4])
        if text.count(facts["ITEM"]) != 1 or text.count(facts["REQ_ID"]) != 1:
            return "item or code not exactly once"
        try:
            sk = K.make_skin(sid, F, text, {"REQUESTER": "name", "ITEM": "name", "REQ_ID": "id"}, register=register,
                             author_mode="F", brief=facts, held_out=held, **meta)
            sk.fill(_sample_slots(track))
        except Exception as e:  # noqa: BLE001
            return f"freeform: {e}"
        pools["skins"][sid] = sk
    elif kind == "attack":
        track = parts[1]
        sid = f"T31-{track}-attack-{qid}"
        sk = K.make_skin(sid, F, text, {"REQUESTER": "name"}, kind="attack", register="note", **meta)
        probs = _lint_skin(sk, track)
        if probs:
            return "; ".join(probs[:4])
        pools["attacks"][sid] = sk
    elif kind == "wording":
        q = parts[1]
        counts = _phs(text)
        if any(p.mod for p in K.placeholders(text)):
            return "grammar helper inside a question"
        need = [r.strip("{}") for r in QUESTION_MEANING[q][1]]
        if any(counts.get(n) != 1 for n in need) or counts.get("REQ_ID", 0) > 1:
            return f"placeholders {counts} (need {need} once, REQ_ID at most once)"
        if set(counts) - set(need) - {"REQ_ID"} or (counts.get("REQ_ID") and item["slots"].get("REQ_ID") ==
                                                       "leave it out"):
            return f"placeholders {sorted(counts)} outside the item's list"
        if not text.endswith("?"):
            return "not a question"
        decl = {n: ("name" if n == "CANDIDATE" else "id") for n in counts}
        sid = f"T31-W-{q}-{qid}"
        sk = K.make_skin(sid, F, text, decl, kind="wording", register="question", qform=q, **meta)
        probs = [f"{v.rule}: {v.detail}" for v in gsl.lint_template(sk, label_words=P.T31.LABEL_WORDS,
                                                                      exceptions=P.T31.GSL_EXCEPTIONS,
                                                                      name_allow=P.T31.NAME_ALLOW)]
        k = negcount.count(K.PH_RE.sub("X", text))
        want = NEG_COUNTS[q]                       # (k_syn, k_all): the form's own negation and nothing else
        if (k.k_syn, k.k_all) != want:
            probs.append(f"negation counts (k_syn {k.k_syn}, k_all {k.k_all}), need {want}")
        if probs:
            return "; ".join(probs[:4])
        try:
            f = pools["lexicon"].add(text, question_sem(F, q), slots=decl, source="haiku", family=F, **meta)
        except LexiconError as e:
            return f"lexicon: {e}"
        pools["wordings"][sid] = (sk, f.form_id)
    elif kind == "band":
        sem = parts[1]
        if K.PH_RE.sub("", text).strip() == text or _phs(text) != {"X": 1} or re.search(r"\d", text):
            return "needs {X} once and no digits"
        if negcount.count(K.PH_RE.sub("X", text)).k_all:
            return "negation in a band phrase"
        try:
            pools["lexicon"].add(text, sem, slots={"X": "cents"}, source="haiku", family=F, **meta)
        except LexiconError as e:
            return f"lexicon: {e}"
    else:
        return f"unknown item kind {kind}"
    return None


_SCOPE_RE = re.compile(r"[a-z]+\.[a-z]+")
_AGENT_RE = re.compile(r"[a-z]+(?:-[a-z]+){1,2}")


def _load_pack(kind: str, pack, pools) -> str | None:
    try:
        if kind == "names":
            if not isinstance(pack, list) or not pack:
                return "no names"
            ok = []
            for n in pack:
                if isinstance(n, str) and re.fullmatch(r"[A-Za-z][A-Za-z-]*(?: [A-Za-z][A-Za-z-]*){1,2}", n.strip()):
                    try:
                        S.name_slot(n.strip())
                    except S.SlotError:
                        continue
                    if n.strip() not in pools["names"] and n.strip() not in ok:
                        ok.append(n.strip())
            pools["names"] += ok
            return None if ok else "no usable name"
        if not isinstance(pack, dict):
            return "pack is not an object"
        if kind == "appr":
            proc, items, roles = pack.get("process"), pack.get("items"), pack.get("roles")
            if not (isinstance(proc, str) and isinstance(items, list) and isinstance(roles, list)):
                return "process / items / roles missing"
            if len(set(items)) != 4 or len(set(roles)) < 12 or any(a != b and a in b for a in items for b in items):
                return "needs 4 distinct items (none inside another) and 12 roles"
            for v in [proc] + items + roles:
                S.name_slot(v)
                if re.search(r"\d", v):
                    return f"digit in {v!r}"
            if any(v != v.lower() for v in [proc] + items):
                return "process and items are lowercase"
            if any(re.search(r"approv|accountab|responsib|consult|inform|sign-off|delegat|authorit", r.lower())
                   for r in roles[:12]):
                return "a role title names a RACI or approval word"
            pools["packs_appr"].append({"process": proc, "items": items, "roles": roles[:12]})
            return None
        scopes, tasks, agents = pack.get("scopes"), pack.get("tasks"), pack.get("agents")
        if not (isinstance(scopes, list) and isinstance(tasks, list) and isinstance(agents, list)):
            return "scopes / tasks / agents missing"
        if not (10 <= len(set(scopes)) <= 12 and len(set(tasks)) == 4 and len(set(agents)) == 6):
            return "needs 10-12 scopes, 4 tasks, 6 agents"
        if not all(_SCOPE_RE.fullmatch(s) for s in scopes) or not all(_AGENT_RE.fullmatch(a) for a in agents):
            return "scope or agent id format"
        for s in scopes + agents:
            S.id_slot(s)
        for t in tasks:
            S.name_slot(t)
        if any(a != b and a in b for a in tasks for b in tasks):
            return "a task inside another"
        pools["packs_agent"].append({"scopes": scopes, "tasks": tasks, "agents": agents})
        return None
    except S.SlotError as e:
        return f"value: {e}"


def main(argv: list) -> int:
    cmd = argv[1] if len(argv) > 1 else "check"
    if cmd == "check":
        files, manifest = files_for(build_batches())
        print(json.dumps({"n_tasks": manifest["n_tasks"], "items_expected": manifest["items_expected"],
                          "files": len(files)}, indent=1))
    elif cmd == "build":
        m = build(force="--force" in argv)
        print(json.dumps({"n_tasks": m["n_tasks"], "items_expected": m["items_expected"],
                          "tasks_json": str(ROOT / "TASKS.json")}, indent=1))
    elif cmd == "load":
        res = load()
        print(json.dumps(res["counts"], indent=1))
        for tid, iid, why in res["drops"][:200]:
            print(f"drop {tid} {iid}: {why}")
    else:
        print(__doc__)
        return 2
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
