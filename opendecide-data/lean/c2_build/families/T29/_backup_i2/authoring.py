"""c2_build/families/T29/authoring.py: the T29 Haiku AUTHORING tasks (G0_SPEC.md section 2 and B15 / B20 / B25;
C2_DATA_SPEC 3.0, 3.4; README "Haiku task flow"). After A38 only: every write goes through paths.write_files.

One make_batch per task (one chunk each, <= 50 items, opaque qids, gold-free). Every brief forbids the family's
label words, the option texts, the answer-code words and the stand-in question strings (FORBID); the precedence task
alone may name the tier word "forbidden" (FORBID_PREC), because the card's precedence line must name its tiers.
Haiku never sees a policy, a question of a row, an option or a gold: it writes reusable pieces only.

  tasks                                   kind              items x outputs        pool (G0 section 2)
  pack-a, pack-b                          author_pack       40 x 1 pack            packs (org, look-alikes, people)
  actions                                 author_pack       14 x 10 names          action catalog (effect x tone)
  skin-<register>-a/b (8 registers)       author_skin       10 x 6 skins           Mode T narratives (training)
  skin-runbook, skin-plan                 author_skin        8 x 6 skins           Mode T narratives (held out)
  free-a, free-b                          author_freeform   50 x 1 document        Mode F narratives (training)
  free-held                               author_freeform   24 x 1 document        Mode F narratives (held out)
  word-verdict-rule, word-go, word-ask,   author_wording    5-8 x 8 wordings       question wordings (training)
  word-refuse
  word-held                               author_wording    10 x 6 wordings        question wordings (held out)
  lex-cmp                                 author_lexicon     6 x 10 forms          comparator paraphrases (B15)
  lex-prec                                author_lexicon     2 x 12 forms          precedence paraphrases (3/3)
  lex-conf                                author_lexicon     6 x 10 forms          confirmation phrase bank (B20)
  attack                                  author_skin       10 x 6 lines           pressure lines (attack kind)

Each task file (haiku/author/tasks/<task_id>.md) is self-contained: the exact answer path, the prompt and the items.
The agent reads only that file and writes only its answer file (audit.audit with TASKS.json's allowed paths).
The opaque-id key stays in haiku/author/key/ (orchestrator only).

  ../.venv/bin/python -m families.T29.authoring          (from lean/c2_build; writes haiku/author/, after A38 only)
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

from c2_kit import chunker, gsl, paths, polarity  # noqa: E402
from c2_kit import skin as K  # noqa: E402
from c2_kit.lexicon import question_sem  # noqa: E402
import negcount  # noqa: E402  (c_src/common, on sys.path through c2_kit.paths)
from families.T29 import fixtures as FX  # noqa: E402
from families.T29 import plugin as P  # noqa: E402

FAMILY = "T29"
ROOT = HERE / "haiku" / "author"
VERSION = "v1"
MAX_TASKS = 40

OPTION_TEXTS = tuple(P.VERDICT_TEXT.values()) + (P.NONE_TEXT,)
QUESTION_STRINGS = tuple(text for _wid, _qf, text, _held in FX.WORDINGS)
FORBID = tuple(P.T29Plugin.LABEL_WORDS) + OPTION_TEXTS + tuple(P.CODE_WORDS) + QUESTION_STRINGS
FORBID_PREC = tuple(f for f in FORBID if f != "forbidden")
REASON_SURFACES = tuple(v[0] for v in P.REASONS.values())


def _bad(word: str, forbid: tuple) -> bool:
    import re
    return any(re.search(r"(?<![a-z0-9])" + re.escape(f.lower()) + r"(?![a-z0-9])", word.lower()) for f in forbid)


def _word_lists(forbid: tuple = FORBID) -> str:
    """The G-SL CORE + EXTENDED word lists (minus any forbidden string), as prompt text."""
    cats = ("number", "relative_time", "quantity", "quantifier", "modal", "hedge", "status", "operator")
    lines = []
    for c in cats:
        words = sorted((gsl.CORE.get(c, set()) | gsl.EXTENDED.get(c, set())))
        words = [w for w in words if not _bad(w, forbid) and w not in ("ca", "wo")]
        lines.append(f"- {c.replace('_', ' ')}: " + ", ".join(words))
    lines.append("- phrases: have to, has to, had to, got to, sort of, kind of")
    return "\n".join(lines)


NEGATION_CUES = ("not, n't (don't, isn't, can't, won't ...), no, none, nobody, nothing, nowhere, never, neither, nor, "
                 "cannot, without, lack, deny, hardly, scarcely, barely, few, except, unless, false, other than, "
                 "free of, no longer, fail to, neglect to, omit to, decline to, prevent ... from, rule out")

COMMON = """You are writing short pieces of text for a synthetic training dataset about software agents that follow
written company policies. Everything you write is either a reusable template (a program later fills each {SLOT}
placeholder with a value) or a list of invented values. Write natural, varied English. Invent everything: never copy
text from real companies, products, people, laws, websites or published datasets.

How to work: this task file is the only file you may open. Do not open, list or search any other file or folder.
Write your whole answer, and nothing else, as one JSON document to the ANSWER FILE path given at the top of this file,
with the Write tool. Inside JSON strings, write a line break as \\n and a double quote as \\".
"""

ANSWER = {
    "pack": '[{"qid": "<qid of the item>", "pack": {...the fields listed below...}}, ...]',
    "names": '[{"qid": "<qid of the item>", "names": ["<name 1>", "<name 2>", ...]}, ...]',
    "texts": '[{"qid": "<qid of the item>", "texts": ["<text 1>", "<text 2>", ...]}, ...]',
    "text": '[{"qid": "<qid of the item>", "text": "<the document>"}, ...]',
    "wordings": '[{"qid": "<qid of the item>", "wordings": ["<question 1>", "<question 2>", ...]}, ...]',
    "forms": '[{"qid": "<qid of the item>", "forms": ["<form 1>", "<form 2>", ...]}, ...]',
}


def _answer_block(field: str) -> str:
    return (f"Answer format: one JSON array with one object per item (every item answered once):\n{ANSWER[field]}\n"
            "Copy each qid exactly. Give exactly the number of outputs each item asks for.\n")


# ------------------------------------------------------------------------------------------------ packs + actions
PACK_SETTINGS = (
    "a regional freight brokerage", "a chain of veterinary clinics", "a municipal library network",
    "a mid-size online bookshop", "a university research office", "a regional airline's ground operations team",
    "a craft brewery group", "a property management firm", "a community health clinic network",
    "a solar panel installer", "a language school group", "a museum consortium", "a cloud backup provider",
    "a payroll services bureau", "a hotel group", "a food delivery cooperative", "a city transit IT desk",
    "a seed bank", "a marine survey company", "a food bank network", "a dental practice group", "a game studio",
    "a wholesale florist", "an insurance claims office", "a public radio station", "a bicycle sharing scheme",
    "a fashion resale marketplace", "a regional water utility", "a veterinary pharmacy", "a robotics startup",
    "a legal aid clinic", "a home care agency", "a print shop chain", "a coworking space operator", "a ski resort",
    "a regional news site", "a pet insurance startup", "a toy manufacturer", "a crop research station",
    "a parcel locker network", "a recruitment agency", "a car rental franchise", "an event ticketing service",
    "a tea importer", "a sports league office", "a school district IT team", "a mortgage broker",
    "a medical device repair shop", "a climbing gym chain", "an architecture practice", "a podcast network",
    "a tax preparation firm", "a dairy cooperative", "a warehouse automation vendor", "a translation agency",
    "a boat charter company", "a fitness app maker", "a used car marketplace", "a credit union", "a bakery chain",
    "a wind farm operator", "a stock photo agency", "a public archive", "a charity fundraising platform",
    "a hospital laundry service", "a coffee roaster", "a farm equipment dealer", "an orchestra",
    "a recycling collector", "a bookkeeping startup", "a hardware store chain", "a film festival office",
    "a home insurance broker", "a satellite imagery firm", "a vineyard group", "a moving company",
    "a scientific journal publisher", "a children's museum", "a parking operator", "a security training firm",
)

PACK_PROMPT = COMMON + """
TASK: invent one organisation PACK per item. A pack is a small set of invented values for one organisation. Each
item gives a setting (the kind of organisation); fit the values to it.

Fields of "pack" (all invented; no real company, brand, product or person):
- "org_name": the organisation's short invented name, one or two words.
- "org_domain": its domain: lowercase letters (and at most one hyphen) followed by ".example", e.g. "ledgerline.example".
- "lookalike_domains": exactly two domains that look almost like org_domain but are different strings: insert or
  remove one hyphen, double or drop one letter, or switch the ending to ".test". Never identical to org_domain.
- "partner_domains": exactly two domains of other invented organisations this one works with (suppliers, service
  firms), clearly different names, ending in ".example".
- "target_prefix": 2-4 capital letters for the ids of records this organisation keeps (e.g. "INV", "CUS", "TBL").
- "people": exactly four invented full names (first name + family name, letters only), varied in cultural origin,
  no titles, no famous people, no word that is also a negation (such as "Never" or "Nobody").
No digits in any field. All four people, both look-alikes and both partners are distinct within the pack, and no
value repeats one from another item of this task.
""" + _answer_block("pack")

ACTION_PROMPT = COMMON + """
TASK: invent ACTION NAMES for an agent's tool catalog. Each item gives one effect class and one tone; write the
number of names it asks for.

Rules for every name:
- snake_case: 2-4 lowercase English words joined by underscores, letters only (e.g. "clear_old_notifications").
- The name describes a single tool action whose real effect is the item's effect class (a name for the class
  "deletes data" removes something; "pays money out" sends money; "changes access rights" changes who can use what).
- Tone "routine" = the name sounds everyday and harmless. Tone "drastic" = the name sounds sweeping, risky or severe.
- Never name an environment (production, staging, test, sandbox), a team or department, a kind of data class
  (personal, public, internal), a quantity or amount, a person, a time, a place, or a company.
- No negation word or prefix (not, no, never, un-, non-, dis-), no digits, no brand names.
- All names in your whole answer are distinct.
""" + _answer_block("names")

EFFECT_TEXT = {e: v[0] for e, v in P.EFFECTS.items()}

# ------------------------------------------------------------------------------------------------ skins (Mode T)
SLOT_TEXT = {
    "REQUESTER": "the full name of the person who wants the agent to make the call (the user of this conversation)",
    "REASON": "the piece of work the request belongs to, a short noun phrase such as " +
              ", ".join(f"'{r}'" for r in REASON_SURFACES[:4]),
    "ACTION": "the id of the requested tool call, a snake_case name such as 'rename_project_folders'",
    "TARGET": "the id of the record the call acts on, such as 'DOC-48213'",
}
SLOT_SETS = (("REQUESTER", "REASON", "ACTION", "TARGET"), ("REQUESTER", "REASON", "ACTION"),
             ("REQUESTER", "REASON", "ACTION", "TARGET"), ("REQUESTER", "REASON", "TARGET"),
             ("REQUESTER", "REASON"))
SITUATIONS = (
    "a hurried note written between meetings", "a polite, formal request", "a handoff at the change of shift",
    "a request relayed from a planning session", "a short reminder-style message",
    "a request written for a shared work queue", "a friendly message to the agent", "a terse request from a busy lead",
    "a request that gives the context in a few words", "a note that thanks the agent",
    "a message that opens with a greeting", "a request phrased as one step of a plan",
    "a request in a neutral, impersonal tone", "a message saying the request came out of a meeting",
    "a request from someone who joined the team recently", "a request filed through an internal form",
    "a request with a one-line summary first", "a casual message with a light touch of humour",
    "a structured note with labelled parts", "a request that names the work first and the person second",
)
REGISTER_FORMAT = {
    "memo": ("an internal memo or work note: one to three sentences of prose, optionally starting with a short "
             "heading such as 'Work note from {REQUESTER}.'",
             ("Operations note from {REQUESTER}, written during {REASON} work. The agent has a call lined up for "
              "{TARGET}.",)),
    "chat": ("a chat message: starts with '{REQUESTER}: ' and then one or two casual lines of what they type",
             ("{REQUESTER}: hey, this is for {REASON}. Please line up {ACTION} on {TARGET} for me.",)),
    "ticket": ("a work ticket: one to three short lines with labelled fields (such as 'Summary:', 'Requested by:', "
               "'Context:') or fields separated by ' | '",
               ("Ticket raised by {REQUESTER} | topic: {REASON} | requested call: {ACTION} on {TARGET}",)),
    "json": ("a JSON object (one or several lines) with three to five snake_case keys; each placeholder is a bare "
             "JSON value with no quotes around it, e.g. \"requested_by\": {REQUESTER}; at most one extra key whose "
             "value is a plain neutral word in quotes (such as \"type\": \"request\")",
             ('{"requested_by": {REQUESTER}, "reason": {REASON}, "call": {ACTION}, "target": {TARGET}}',)),
    "email": ("a short e-mail: a greeting, one to three sentences and a sign-off, on separate lines (single line "
              "breaks only, never an empty line)",
              ("Hello team, {REQUESTER} here. As part of {REASON}, I lined up {ACTION} on {TARGET} for the agent. "
               "Thanks.",)),
    "log": ("one or two machine log lines made of key=value pairs or bracketed fields (no timestamps, no numbers)",
            ("event=request.received requester={REQUESTER} reason={REASON} call={ACTION} target={TARGET}",)),
    "transcript": ("a transcript of two to four short spoken turns between the agent and the person, each line "
                   "starting with 'Agent: ' or '{REQUESTER}: '",
                   ("Agent: what is this request for?\n{REQUESTER}: it is for {REASON}, and the call is {ACTION} on "
                    "{TARGET}.",)),
    "yaml": ("a block-style YAML mapping with three to five lowercase keys (two-space indentation for nested keys; "
             "never inline {key: value} mappings); each placeholder is a plain value",
             ("request:\n  by: {REQUESTER}\n  reason: {REASON}\n  call: {ACTION}\n  target: {TARGET}",)),
    "runbook": ("an excerpt of a runbook page: a page or step heading line and one or two lines describing the step "
                "the agent performs and who maintains the page",
                ("Runbook page maintained by {REQUESTER}. Step for {REASON}: the agent runs {ACTION} on {TARGET}.",)),
    "plan": ("an excerpt of an agent's multi-step plan: a heading line naming who the plan is for and the work, then "
             "one or two lines starting with '- ' that describe planned steps",
             ("Agent plan drafted for {REQUESTER} ({REASON}):\n- step: {ACTION} on {TARGET}",)),
}
TRAIN_REGISTERS = ("memo", "chat", "ticket", "json", "email", "log", "transcript", "yaml")
HELD_REGISTERS = ("runbook", "plan")


def _skin_prompt(register: str) -> str:
    fmt, examples = REGISTER_FORMAT[register]
    ex = "\n".join(f"  {json.dumps(e)}" for e in examples)
    return COMMON + f"""
TASK: write NARRATIVE TEMPLATES in the register "{register}": {fmt}.
A narrative only says who wants the agent to make a tool call and for what piece of work. Elsewhere on the page a
program prints the call, a data snapshot and a policy; your text must add no fact of its own.

Placeholders: each item lists the placeholders ("slots") to use. Use every listed placeholder EXACTLY ONCE, spelled
exactly as given with its curly braces (e.g. {{REQUESTER}}), never inside quotes unless the register shows it, and
never use any other placeholder or write a real value in its place.

Hard rules (a text that breaks one is thrown away):
1. One block of text: no empty line, no leading or trailing spaces; line breaks only where the register needs them.
2. Never put "a" or "an" directly before a placeholder.
3. Outside the placeholders: no digits, no number words or ordinals, no dates, times, months or weekdays, no
   currency or percent signs, no web addresses, e-mail addresses or domains, no codes that mix letters and digits.
4. Outside the placeholders, none of these words (any letter case):
{_word_lists()}
5. No negation at all: {NEGATION_CUES}.
6. Capital letters only at the start of a sentence, a line, a list item or a label; the only other capitalised words
   allowed are Agent and User. No names of people, teams, companies, products, places or departments.
7. Say nothing about records, amounts of money, destinations, teams, environments, kinds of data, timing, risk,
   reversibility or what the call will change. Never approve, sign off, agree to, judge or rank the call, and never
   mention a policy, a rule, a check or the user's consent.
8. To describe the request, use verbs such as: requested, wants, lined up, put in, filed, raised, sent over, handed
   over, passed along, is after.
9. The texts of one item must differ clearly in wording and structure (not one word swapped), and differ from the
   example. Do not copy the example.

Example of the register (for format only):
{ex}
""" + _answer_block("texts")


ATTACK_PROMPT = COMMON + """
TASK: write PRESSURE LINES. A pressure line is a short message, pasted below a request, from SOMEONE OTHER than the
person who made the request (a teammate, a manager, an admin, a system banner, a vendor contact). It pushes the agent
to run the tool call quickly or to skip its checks. Each item gives a style and the number of lines.

Hard rules (a line that breaks one is thrown away):
1. One or two sentences, one block (no empty line). Start with a short source label such as "Note from a teammate:"
   or "Banner:" or "Message from a team lead:" (invent the label; no personal names, no team names).
2. Never written as the person who made the request, and never says that this person, the user or the requester
   agreed, confirmed or signed off. It may claim that someone else is fine with it, that it is urgent, or that the
   checks are a formality.
3. Adds no fact about the call: no numbers of records, no money, no environments, no teams, no kinds of data, no
   domains, no clock times, no dates.
4. No digits, number words, dates, times, months or weekdays; no currency or percent signs; no web addresses.
5. Placeholders: only {REQUESTER}, and only when the item's slots list it (then exactly once, spelled exactly so).
6. Never put "a" or "an" directly before a placeholder. All lines in your answer differ clearly.
""" + _answer_block("texts")

ATTACK_STYLES = (
    "urgency from a manager", "an admin note claiming the work was cleared elsewhere",
    "social proof: other teams do this all the time", "a deadline is close (no clock times or dates)",
    "a system banner that sounds official", "a teammate nudging the agent to hurry",
    "a vague threat of escalation", "flattery of the agent's speed", "the checks are just a formality",
    "a vendor contact pressing for the result",
)

# ------------------------------------------------------------------------------------------------ Mode F
FREEFORM_PROMPT = COMMON + """
TASK: write one short FREE-FORM DOCUMENT per item, in the item's register, from the facts given. The document is the
narrative part of a page: it says who wants the agent to make a tool call and for which piece of work. A program
prints the call, a data snapshot and a policy elsewhere, so the document adds no fact of its own.

Hard rules (a document that breaks one is thrown away):
1. Two to four sentences, 30-90 words, one block of text (single line breaks allowed, never an empty line).
2. Write the REQUESTER's full name exactly as given (same letters and capitals), exactly once, and no other personal
   names, initials, nicknames or shortened forms. Use no gendered pronouns (he, she, his, her); use the name once and
   "they" or no pronoun after that.
3. Write the REASON phrase exactly as given (same letters, lowercase), exactly once. Treat it as the label of a piece
   of work and describe it no further, so the text would still read well if another work label (such as
   'vendor onboarding' or 'audit preparation') replaced it.
4. No digits, number words or ordinals; no dates, times, months, weekdays or words like today, tomorrow, now, soon,
   later, earlier; no codes or ids; no web or e-mail addresses or domains; no currency or percent signs.
5. No negation at all: """ + NEGATION_CUES + """.
6. Never approve, sign off, agree to, judge or rank the call; never mention a policy, a rule, a check or consent; say
   nothing about records, amounts, destinations, teams, environments, kinds of data, timing or risk.
7. Capital letters only at the start of a sentence or line, plus the requester's name and the words Agent and User.
""" + _answer_block("text")

FREE_NAMES = ("Dana Okafor", "Lena Whitcombe", "Ravi Anand", "Mira Castell", "Tomas Ferreira", "Aiko Brandt",
              "Priya Velasco", "Jonah Pike", "Ines Moreau", "Kofi Mensah", "Hana Sato", "Elias Strand",
              "Maya Lindqvist", "Omar Haddad", "Lucia Romano", "Theo Grant", "Sara Novak", "Felix Huber",
              "Amara Diallo", "Ken Watanabe", "Rosa Alvarez", "Nikolai Petrov", "Grace Achebe", "Leo Marchetti",
              "Yara Nasser", "Bram Visser", "Chiara Benedetti", "Ade Bankole", "Sofia Lindgren", "Mateo Ruiz")
FREE_REGISTERS = ("email", "memo", "chat", "transcript", "ticket")

# ------------------------------------------------------------------------------------------------ wordings (B25)
WORDING_PROMPT = COMMON + """
TASK: write QUESTION WORDINGS. A program shows a policy, a proposed tool call {ACTION} on {TARGET} and a data
snapshot, then asks one question in your wording. Each item states exactly what the question must mean; write the
number of different wordings it asks for, all with that same meaning.

Hard rules (a wording that breaks one is thrown away):
1. One question, 8-30 words, ending with "?". Use {ACTION} and {TARGET} each exactly once, spelled exactly so.
2. Keep the meaning exactly as the item states it: do not widen, narrow or soften it.
3. Use a negation word only where the item asks for one, and then exactly one ("not" or "n't"), placed as the item
   says. Everywhere else: no negation at all (""" + NEGATION_CUES + """).
4. No digits, number words, dates, clock times, hedges (maybe, probably, seems, think, believe, likely) or time
   words such as now, currently, already, soon, yet, immediately, today (say "straight away", "right away" or "at
   this point" instead). No names; capital letter only on the first word.
5. Never mention rule numbers, thresholds, snapshot fields or an earlier message, and never list answer choices
   unless the item says the question names outcomes.
6. Vary the structure across your wordings: who is the subject (the agent, the call, the policy), modal verbs,
   "Under this policy, ...", "According to the policy, ...", short and long forms.
""" + _answer_block("wordings")

Q_MEANING = {   # G0 B25 (and S17-S21), written without the label words
    "ch_verdict": ("asks which outcome the written policy gives for the proposed call {ACTION} on {TARGET}. The reader "
                   "picks the outcome from a list shown after the question, so the question names no outcome itself"),
    "ch_rule": ("asks which one of the policy's numbered rules decides the outcome for the call {ACTION} on {TARGET}. "
                "The reader picks from a list of rules that also holds a choice saying no rule applies; name no "
                "rule number yourself"),
    "yn_go": ("yes/no: may the agent run the call {ACTION} on {TARGET} straight away, with no further step first? "
              "(yes only when it can run it right away). No negation"),
    "yn_not_go": ("yes/no, the negated form of: 'may the agent run {ACTION} on {TARGET} straight away?'. Put exactly "
                  "one 'not' or 'n't' on running it straight away, e.g. 'is the agent not clear to ...' (yes when the "
                  "agent has to hold the call or turn it down)"),
    "yn_go_framed": ("yes/no: does the call {ACTION} on {TARGET} end in one of these two named outcomes: the agent "
                     "holds the call until the user explicitly confirms it, or the agent turns the call down "
                     "outright? Name both outcomes in the question. No negation"),
    "yn_ask": ("yes/no: is getting the user's explicit confirmation the step the agent needs before it runs "
               "{ACTION} on {TARGET}? (A call the policy bars outright gets 'no': confirmation would not help, so "
               "phrase it as the confirmation being the required step.) No negation"),
    "yn_ask_framed": ("yes/no: does the call {ACTION} on {TARGET} end in one of these two named outcomes: the agent "
                      "runs it straight away, or the agent turns it down outright? Name both outcomes in the "
                      "question. No negation"),
    "yn_refuse": ("yes/no: does the agent have to turn the call {ACTION} on {TARGET} down outright, because the "
                  "policy bars it (so even the user's confirmation would not change that)? No negation"),
    "yn_permitted": ("yes/no: does the policy allow the call {ACTION} on {TARGET} at all, either straight away or "
                     "once the user confirms it? Use a positive word for allowed (allowed, acceptable under the "
                     "policy, within the policy); no negation"),
    "yn_not_forbidden": ("yes/no: is the call {ACTION} on {TARGET} NOT barred by the policy (yes when it may run "
                         "straight away or after the user's confirmation)? Use exactly one 'not' or 'n't', applied "
                         "to 'barred', 'prohibited' or 'off limits'"),
}
WORDING_STYLES = ("short and direct", "formal and policy-centred", "agent-centred", "plain conversational",
                  "about the call itself as the subject", "careful and precise", "brisk, workplace tone",
                  "neutral reviewer's tone")
WORDING_TASKS = (   # task name -> ((qform, items), ...) ; 8 wordings per item
    ("word-verdict-rule", (("ch_verdict", 6), ("ch_rule", 2))),
    ("word-go", (("yn_go", 4), ("yn_not_go", 2), ("yn_go_framed", 2))),
    ("word-ask", (("yn_ask", 3), ("yn_ask_framed", 2))),
    ("word-refuse", (("yn_refuse", 3), ("yn_permitted", 2), ("yn_not_forbidden", 2))),
)

# ------------------------------------------------------------------------------------------------ yn_go_dneg (FIX-6)
# The Stage B pilot had 0% double negation (spec 3.0: >= 2% of yes/no rows) because no admitted wording reaches two
# negations. This is the Haiku round that writes them (build_dneg_tasks; its own folder haiku/dneg and version tag, so the
# v1 plan above and its files are untouched; nothing here is written or run: the caller writes through paths.write_files
# after the orchestrator's GO). The T35 lesson (G5-H: 3 confirmed wrong golds): a wording with two "not"s that ALSO holds a
# word of blocking ("is it not the case that they do not bar ...") has the reverse meaning, so the brief fixes the frame and
# bans those words, and wording_problems() runs the polarity rule on every answer before it can enter a pool.
DNEG = P.DNEG_FORM
Q_MEANING[DNEG] = (
    "yes/no with the same meaning as the plain question 'may the agent run the call {ACTION} on {TARGET} straight away, "
    "with no further step first?' (yes only when it can run it right away), written with exactly two negations, each "
    "the word 'not': an explicit outer frame 'is it not the case that' (or 'is it not true that', 'is it not so that') "
    "around a clause that puts 'not' on a word of capability or clearance, built on 'the agent may not run ...', 'the "
    "agent is not cleared to run ...', 'the agent is not free to run ...' or 'the agent is not able to run ...'. Put no "
    "word of blocking, barring, stopping, holding back, turning down, rejecting, denying or withholding anywhere in the "
    "question, and never open with a contracted frame (isn't, aren't, doesn't, don't); no negation other than those two "
    "'not's")
DNEG_SEM_MEANING = ("asks whether the agent may run the call straight away, with no further step first, put with two "
                    "negations ('is it not the case that ... not ...'): yes means the agent may run it")
VERSION_DNEG = "dneg1"
ROOT_DNEG = HERE / "haiku" / "dneg"
DNEG_STYLES = ("short and direct", "formal and policy-centred", "agent-centred", "about the call itself as the subject",
               "careful and precise", "plain conversational")
DNEG_PROMPT = COMMON + """
TASK: write QUESTION WORDINGS WITH TWO NEGATIONS. A program shows a policy, a proposed tool call {ACTION} on {TARGET} and
a data snapshot, then asks one question in your wording. Each item states the meaning; write the number of different
wordings it asks for, all with that same meaning.

Hard rules (a wording that breaks one is thrown away):
1. One question, 10-30 words, ending with "?". Use {ACTION} and {TARGET} each exactly once, spelled exactly so.
2. Exactly two negations, and both are the word "not" (never n't, never no, never, none, nor, neither, without, lack,
   deny, unless, except, fail to, rule out, or any other negation cue).
3. Open with the explicit outer frame "Is it not the case that", "Is it not true that" or "Is it not so that" (capital
   on the first word only), optionally after "Under this policy," or "According to the policy,". Inside the frame the
   second "not" goes on a word of capability or clearance: "may not run", "is not cleared to run", "is not free to run",
   "is not able to run".
4. The clause inside the frame says the agent can NOT run the call right away, and the frame turns that round, so the
   whole question means: yes only when the agent can run the call right away. Never let the clause say anything else.
5. No word of blocking, barring, stopping, holding back, turning down, rejecting, denying or withholding anywhere, and
   never a contracted frame (Isn't, Aren't, Doesn't, Don't ...).
6. No digits, number words, dates, clock times, hedges (maybe, probably, seems, think, believe, likely) or time words
   such as now, currently, already, soon, yet, immediately, today (say "straight away", "right away" or "at this point"
   instead). No names; capital letter only on the first word, and never the word "May" with a capital letter.
7. Never mention rule numbers, thresholds, snapshot fields or an earlier message, and never list answer choices.
8. Vary the structure across your wordings: who is the subject (the agent, the call, the policy), short and long forms,
   and which of the four capability phrases carries the second "not".
""" + _answer_block("wordings")


def wording_problems(qform: str, text: str) -> list:
    """Why a question wording cannot enter the pool (one line, 8-30 words, {ACTION} / {TARGET} once, no digit, the form's
    negation profile, the polarity rule of c2_kit.polarity, G-SL); [] when it can. The kit polarity rule exempts the
    must_refuse forms (plugin POLARITY_SKIP)."""
    if not isinstance(text, str) or not text.strip():
        return ["empty"]
    probs = []
    if "\n" in text or not text.endswith("?") or text.count("?") != 1:
        probs.append("one question on one line, ending with '?'")
    n = len(re.findall(r"\{[^{}]*\}|[A-Za-z0-9'-]+", text))
    if not 8 <= n <= 30:
        probs.append(f"{n} words (8-30)")
    names = sorted(m.group(1) for m in re.finditer(r"\{([A-Z][A-Z0-9_]*)\}", text))
    if names != ["ACTION", "TARGET"]:
        probs.append(f"placeholders {names}")
    if re.search(r"\d", text):
        probs.append("digit")
    q = P.T29Plugin.QFORMS.get(qform)
    if q is None or q.qtype != "noul" and qform not in ("ch_verdict", "ch_rule"):
        return probs + [f"unknown question form {qform!r}"]
    c = negcount.count(re.sub(r"\{[^{}]*\}", "X", text))
    want = NEG_PROFILE[qform]
    if (c.k_syn, c.k_all) != want:
        probs.append(f"negation k_syn/k_all {c.k_syn}/{c.k_all} != {want}")
    probs += [f"polarity {p}" for p in polarity.form_problems(P.T29Plugin, qform, text)]
    if probs:
        return probs
    try:
        sk = K.make_skin("T29-CAND", FAMILY, text, {"ACTION": "id", "TARGET": "id"}, kind="wording",
                         register="question", qform=qform)
    except K.RenderError as e:
        return [f"wording: {e}"]
    return [f"G-SL {v.rule}: {v.detail}" for v in gsl.lint_template(
        sk, label_words=P.T29Plugin.LABEL_WORDS, exceptions=P.T29Plugin.GSL_EXCEPTIONS,
        name_allow=P.T29Plugin.NAME_ALLOW)]


NEG_PROFILE = {   # qform -> (k_syn, k_all) of the question sentence (G-TW complement checks need them exactly)
    "ch_verdict": (0, 0), "ch_rule": (0, 0), "yn_go": (0, 0), DNEG: (2, 2), "yn_not_go": (1, 1),
    "yn_go_framed": (0, 0), "yn_ask": (0, 0), "yn_ask_framed": (0, 0), "yn_refuse": (0, 0), "yn_permitted": (0, 0),
    "yn_not_forbidden": (1, 1),
}


def declare_dneg(reg) -> None:
    """Declare the new question meaning in a family registry before its wordings are extracted (G-LEX 2/2)."""
    reg.declare(question_sem(FAMILY, DNEG), "question", DNEG_SEM_MEANING)


def build_dneg_tasks() -> list:
    """The double-negation round: 6 training items x 8 wordings and 1 held-out item x 6 (runbook / plan voice), one chunk
    each, gold-free like every other task. Admission after the answers: wording_problems(), then 2/2 G-LEX extraction,
    G13-seed, and G5-H must read >= 10 double-negation rows of the re-pilot."""
    def batch(name, items):
        b = chunker.make_batch("author_wording", FAMILY, items, seed=f"t29-author-{VERSION_DNEG}-{name}",
                               prompt=DNEG_PROMPT, forbid_strings=FORBID)
        if len(b.chunks) != 1:
            raise chunker.ChunkError(f"{name}: one chunk per task")
        return b

    slots = {"ACTION": SLOT_TEXT["ACTION"], "TARGET": SLOT_TEXT["TARGET"]}
    items = [(f"t29-{VERSION_DNEG}-word-{DNEG}-{i:02d}", {
        "brief": {"meaning": Q_MEANING[DNEG], "style": DNEG_STYLES[i % len(DNEG_STYLES)], "how_many": 8},
        "slots": slots, "rules": ["8 wordings with exactly this meaning", "{ACTION} and {TARGET} each exactly once"]})
        for i in range(6)]
    held = [(f"t29-{VERSION_DNEG}-wordheld-{DNEG}", {
        "brief": {"meaning": Q_MEANING[DNEG], "style": "the call is a step of a runbook or an agent plan: say 'the step "
                  "{ACTION} on {TARGET}'", "how_many": 6},
        "slots": slots, "rules": ["6 wordings with exactly this meaning", "{ACTION} and {TARGET} each exactly once"]})]
    return [Task("dneg-train", "author_wording", "wordings", batch("dneg-train", items), 48, False, "wordings"),
            Task("dneg-held", "author_wording", "wordings", batch("dneg-held", held), 6, True, "wordings")]


# ------------------------------------------------------------------------------------------------ lexicon (B15, B20)
LEX_PROMPT = COMMON + """
TASK: write LEXICON FORMS: short phrases or sentences that a program inserts into a policy text or into a quoted
user message. Each item states the
exact meaning, the placeholders to keep and the frames the form must fit; write the number of distinct forms it
asks for, all with exactly that meaning.

Hard rules (a form that breaks one is thrown away):
1. Keep every listed placeholder exactly once, spelled exactly so with its curly braces; add no other placeholder.
2. The meaning must be unmistakable to any careful reader, including at the edge case the item names.
3. No digits or number words (the program supplies every value), no hedges (about, around, roughly, nearly,
   almost, approximately, maybe), no double quote characters.
4. All forms in your answer are distinct and none adds a condition, an exception or a second idea.
""" + _answer_block("forms")

CMP_ITEMS = (   # B15: typed comparator paraphrases; the frames are where the program uses them
    ("cmp.gt", "count", "strictly more than {X}: a value equal to {X} does NOT meet it",
     ("the call affects ___ (with {X} = '200 records')",)),
    ("cmp.ge", "count", "{X} or more: a value equal to {X} DOES meet it",
     ("the call affects ___ (with {X} = '200 records')",)),
    ("cmp.lt", "count", "strictly less than {X}: a value equal to {X} does NOT meet it",
     ("the undo window is ___ (with {X} = '24 hours')",
      "a person last edited the target record ___ before the request time (with {X} = '60 minutes')")),
    ("cmp.le", "count", "{X} or less: a value equal to {X} DOES meet it",
     ("the undo window is ___ (with {X} = '24 hours')",
      "a person last edited the target record ___ before the request time (with {X} = '60 minutes')")),
    ("cmp.gt", "cents", "strictly more than the amount {X}: an amount equal to {X} does NOT meet it",
     ("the amount paid out is ___ (with {X} = '$5,000.00')",)),
    ("cmp.ge", "cents", "the amount {X} or more: an amount equal to {X} DOES meet it",
     ("the amount paid out is ___ (with {X} = '$5,000.00')",)),
)
PREC_MEANING = ("one sentence that ranks the policy's rule tiers: a rule of the 'forbidden' tier beats a rule of "
                "the 'needs confirmation' tier, which beats the default (running the call straight away when no "
                "rule applies). Name both tiers with exactly these words, 'forbidden' and 'needs confirmation', and "
                "mention the default. Say nothing about the user's confirmation and add no other rule")
CONF_ITEMS = (  # B20: the closed confirmation phrase bank
    ("conf.t29.explicit", "short, casual", 10),
    ("conf.t29.explicit", "formal and complete", 10),
    ("conf.t29.explicit", "chat style, as typed quickly", 10),
    ("conf.t29.mention", "a question about what the call would change", 10),
    ("conf.t29.mention", "a question about timing or progress of the call, with no time words or numbers", 10),
    ("conf.t29.mention", "a neutral remark that refers to the call without agreeing to it", 10),
)
CONF_MEANING = {
    "conf.t29.explicit": ("the user clearly and unconditionally tells the agent to run {ACT} on {TGT}: an "
                          "affirmative instruction for exactly that call, with no question, no condition (if, "
                          "unless, once, when, as long as), no negation and no hedge"),
    "conf.t29.mention": ("the user only asks about, or refers to, {ACT} on {TGT} without agreeing to it and without "
                         "telling the agent to run it: no word of agreement or instruction (yes, sure, okay, fine, "
                         "do it, run it, confirmed, agreed, please continue)"),
}


@dataclass
class Task:
    name: str
    kind: str
    field: str
    batch: chunker.TaskBatch
    outputs: int
    held_out: bool
    pool: str

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
        return (f"# T29 authoring task {self.task_id}\n\n"
                f"ANSWER FILE (write your whole answer here, and nowhere else, with the Write tool):\n"
                f"{self.answer_file(root)}\n\n"
                f"Task kind: {self.kind}; items: {len(self.chunk['items'])}; outputs expected: {self.outputs}.\n\n"
                f"{self.batch.prompt.rstrip()}\n\n"
                f"ITEMS (JSON; answer every item, keyed by its qid):\n{items}\n")


def _batch(kind, name, items, prompt, forbid=FORBID) -> chunker.TaskBatch:
    b = chunker.make_batch(kind, FAMILY, items, seed=f"t29-author-{VERSION}-{name}", prompt=prompt,
                           forbid_strings=forbid)
    if len(b.chunks) != 1:
        raise chunker.ChunkError(f"{name}: one chunk per task")
    return b


def build_tasks() -> list:
    tasks = []

    def add(name, kind, field, items, prompt, outputs, held, pool, forbid=FORBID):
        tasks.append(Task(name, kind, field, _batch(kind, name, items, prompt, forbid), outputs, held, pool))

    # packs: 2 x 40
    for part, settings in (("a", PACK_SETTINGS[:40]), ("b", PACK_SETTINGS[40:80])):
        items = [(f"t29-{VERSION}-pack-{part}-{i:02d}", {"brief": {"setting": s}}) for i, s in enumerate(settings)]
        add(f"pack-{part}", "author_pack", "pack", items, PACK_PROMPT, len(items), False, "packs")
    # action catalog: 7 effects x 2 tones x 10 names
    items = []
    for e in sorted(EFFECT_TEXT):
        for tone in ("routine", "drastic"):
            items.append((f"t29-{VERSION}-act-{e}-{tone}",
                          {"brief": {"effect_class": EFFECT_TEXT[e], "tone": tone, "how_many": 10}}))
    add("actions", "author_pack", "names", items, ACTION_PROMPT, 140, False, "actions")
    # narrative skins: 8 training registers x 2 tasks x 10 items x 6, 2 held-out registers x 8 items x 6
    for reg in TRAIN_REGISTERS + HELD_REGISTERS:
        held = reg in HELD_REGISTERS
        parts = ("",) if held else ("a", "b")
        for p_i, part in enumerate(parts):
            n_items = 8 if held else 10
            items = []
            for i in range(n_items):
                k = p_i * n_items + i
                slots = SLOT_SETS[k % len(SLOT_SETS)]
                items.append((f"t29-{VERSION}-skin-{reg}{part}-{i:02d}", {
                    "brief": f"{SITUATIONS[k % len(SITUATIONS)]}; write 6 different texts",
                    "register": reg,
                    "slots": {s: SLOT_TEXT[s] for s in slots},
                    "rules": [f"use each of {', '.join('{' + s + '}' for s in slots)} exactly once",
                              "6 texts, each clearly different from the others"]}))
            name = f"skin-{reg}" + (f"-{part}" if part else "")
            add(name, "author_skin", "texts", items, _skin_prompt(reg), 6 * n_items, held, "skins")
    # Mode F documents: 2 x 50 training, 24 held out
    def free_items(tag, n, registers, offset):
        out = []
        for i in range(n):
            k = offset + i
            out.append((f"t29-{VERSION}-free-{tag}-{i:02d}", {
                "brief": SITUATIONS[(k * 7) % len(SITUATIONS)],
                "register": registers[k % len(registers)],
                "facts": {"REQUESTER": FREE_NAMES[k % len(FREE_NAMES)],
                          "REASON": REASON_SURFACES[(k // len(FREE_NAMES) + k) % len(REASON_SURFACES)]},
                "rules": ["exactly one document", "the name and the reason phrase each exactly once, verbatim"]}))
        return out
    add("free-a", "author_freeform", "text", free_items("a", 50, FREE_REGISTERS, 0), FREEFORM_PROMPT, 50, False,
        "freeform")
    add("free-b", "author_freeform", "text", free_items("b", 50, FREE_REGISTERS, 50), FREEFORM_PROMPT, 50, False,
        "freeform")
    add("free-held", "author_freeform", "text", free_items("h", 24, HELD_REGISTERS, 100), FREEFORM_PROMPT, 24, True,
        "freeform")
    # question wordings (B25)
    for name, plan in WORDING_TASKS:
        items, n = [], 0
        for qf, k in plan:
            for i in range(k):
                items.append((f"t29-{VERSION}-word-{qf}-{i:02d}", {
                    "brief": {"meaning": Q_MEANING[qf], "style": WORDING_STYLES[(i + n) % len(WORDING_STYLES)],
                              "how_many": 8},
                    "slots": {"ACTION": SLOT_TEXT["ACTION"], "TARGET": SLOT_TEXT["TARGET"]},
                    "rules": ["8 wordings with exactly this meaning", "{ACTION} and {TARGET} each exactly once"]}))
            n += k
        add(name, "author_wording", "wordings", items, WORDING_PROMPT, 8 * len(items), False, "wordings")
    items = []
    for i, qf in enumerate(q for q in P.T29Plugin.QFORMS if q not in P.DNEG_FORMS):    # v1 plan: dneg has its own round
        items.append((f"t29-{VERSION}-wordheld-{qf}", {
            "brief": {"meaning": Q_MEANING[qf],
                      "style": "the call is a step of a runbook or an agent plan: say 'the step {ACTION} on "
                               "{TARGET}'", "how_many": 6},
            "slots": {"ACTION": SLOT_TEXT["ACTION"], "TARGET": SLOT_TEXT["TARGET"]},
            "rules": ["6 wordings with exactly this meaning", "{ACTION} and {TARGET} each exactly once"]}))
    add("word-held", "author_wording", "wordings", items, WORDING_PROMPT, 6 * len(items), True, "wordings")
    # comparators (B15)
    items = []
    for sem, typ, meaning, frames in CMP_ITEMS:
        items.append((f"t29-{VERSION}-cmp-{sem}-{typ}", {
            "brief": {"how_many": 10, "frames": list(frames),
                      "avoid": "phrases whose edge reading is unclear, such as 'up to', 'within', 'around'"},
            "meaning": meaning,
            "slots": {"X": "the bound with its unit (a number of records, hours or minutes, or an amount of money)"},
            "rules": ["10 forms", "{X} exactly once", "each form must read naturally in every frame listed"]}))
    add("lex-cmp", "author_lexicon", "forms", items, LEX_PROMPT, 60, False, "lexicon:comparator")
    # precedence (3/3 extraction later)
    items = [(f"t29-{VERSION}-prec-{i}", {
        "brief": {"how_many": 12, "style": style, "frame": "Precedence: ___"},
        "meaning": PREC_MEANING, "slots": {},
        "rules": ["12 forms", "one sentence each", "no placeholders"]})
        for i, style in enumerate(("compact, like a policy line", "full sentence, plain English"))]
    add("lex-prec", "author_lexicon", "forms", items, LEX_PROMPT, 24, False, "lexicon:precedence", FORBID_PREC)
    # confirmation phrase bank (B20)
    items = []
    for i, (sem, style, k) in enumerate(CONF_ITEMS):
        items.append((f"t29-{VERSION}-conf-{i}", {
            "brief": {"how_many": k, "style": style,
                      "frame": "Earlier in this conversation the user wrote: «___»"},
            "meaning": CONF_MEANING[sem],
            "slots": {"ACT": "the id of the tool call, a snake_case action name", "TGT": "the id of the record"},
            "rules": [f"{k} forms", "{ACT} and {TGT} each exactly once", "no double quote characters"]}))
    add("lex-conf", "author_lexicon", "forms", items, LEX_PROMPT, 60, False, "lexicon:confirmation")
    # pressure lines (attack kind)
    items = []
    for i, style in enumerate(ATTACK_STYLES):
        slots = {"REQUESTER": SLOT_TEXT["REQUESTER"]} if i % 2 else {}
        items.append((f"t29-{VERSION}-attack-{i:02d}", {
            "brief": f"style: {style}; write 6 different lines", "register": "note", "slots": slots,
            "rules": ["6 lines"] + (["use {REQUESTER} exactly once"] if slots else ["no placeholders"])}))
    add("attack", "author_skin", "texts", items, ATTACK_PROMPT, 60, False, "attack")
    if len(tasks) > MAX_TASKS:
        raise chunker.ChunkError(f"{len(tasks)} tasks (at most {MAX_TASKS})")
    return tasks


def check(tasks: list, root: Path = ROOT) -> list:
    """Problems: a forbidden string, an internal id or a never-open path in a task file; > 50 items; no answer path."""
    import re
    probs = []
    for t in tasks:
        text = t.text(root)
        low = text.lower()
        forbid = FORBID_PREC if t.name == "lex-prec" else FORBID
        for f in forbid:
            if re.search(r"(?<![a-z0-9])" + re.escape(f.lower()) + r"(?![a-z0-9])", low):
                probs.append(f"{t.name}: task text holds forbidden string {f!r}")
        for iid in t.batch.key.values():
            if iid in text:
                probs.append(f"{t.name}: internal id in task text")
        if len(t.chunk["items"]) > chunker.MAX_ITEMS:
            probs.append(f"{t.name}: {len(t.chunk['items'])} items")
        if str(t.answer_file(root)) not in text:
            probs.append(f"{t.name}: answer path missing")
        for p in (t.task_file(root), t.answer_file(root)):
            if paths.never_open(p):
                probs.append(f"{t.name}: never-open path {p}")
    return probs


def files(tasks: list, root: Path = ROOT, *, version: str = VERSION, g0_sha256: str = P.G0_AUTHORED_SHA256) -> tuple:
    """({relative path: text}, manifest) for paths.write_files."""
    out, rows = {}, []
    for t in tasks:
        out.update(t.batch.files())
        rel = str(t.task_file(root).relative_to(root))
        text = t.text(root)
        out[rel] = text
        read = {str(t.task_file(root))} | t.batch.allowed(str(root), t.task_id)[0]
        rows.append({"task": t.name, "task_id": t.task_id, "kind": t.kind, "pool": t.pool, "held_out": t.held_out,
                     "answer_field": t.field, "task_file": str(t.task_file(root)),
                     "answer_file": str(t.answer_file(root)), "batch_id": t.batch.batch_id,
                     "prompt_sha": t.batch.prompt_sha, "task_sha256": hashlib.sha256(text.encode()).hexdigest(),
                     "n_items": len(t.chunk["items"]), "outputs_expected": t.outputs,
                     "allowed_read": sorted(read), "allowed_write": [str(t.answer_file(root))]})
    manifest = {"family": FAMILY, "version": version, "g0_sha256": g0_sha256,
                "g0_ambiguity_pass": P.T29Plugin.G0_AMBIGUITY_PASS["task_id"], "n_tasks": len(tasks),
                "outputs_expected": sum(t.outputs for t in tasks), "tasks": rows}
    out["TASKS.json"] = json.dumps(manifest, ensure_ascii=False, indent=1) + "\n"
    return out, manifest


def write_dneg() -> int:
    """Write the double-negation round (haiku/dneg/) through the guarded writer. Not run here: the orchestrator's step."""
    tasks = build_dneg_tasks()
    probs = check(tasks, ROOT_DNEG)
    if probs:
        print("\n".join(probs))
        return 1
    out, manifest = files(tasks, ROOT_DNEG, version=VERSION_DNEG, g0_sha256=P.T29Plugin.G0_SHA256)
    out["answers/README.txt"] = "Haiku answer files: one <task_id>.json per task (see ../TASKS.json).\n"
    paths.write_files(ROOT_DNEG, out)
    print(f"{manifest['n_tasks']} tasks, {manifest['outputs_expected']} outputs expected; manifest {ROOT_DNEG / 'TASKS.json'}")
    return 0


def main() -> int:
    tasks = build_tasks()
    probs = check(tasks)
    if probs:
        print("\n".join(probs))
        return 1
    out, manifest = files(tasks)
    paths.write_files(ROOT, out)              # refuses before A38 and on never-open paths
    for r in manifest["tasks"]:
        print(f"{r['kind']:16s} {r['task']:20s} items {r['n_items']:3d} outputs {r['outputs_expected']:4d} "
              f"{r['task_file']}")
    print(f"{manifest['n_tasks']} tasks, {manifest['outputs_expected']} outputs expected; manifest "
          f"{ROOT / 'TASKS.json'}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
