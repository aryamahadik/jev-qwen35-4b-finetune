"""families/T25/haiku_author.py: the T25 Haiku AUTHORING tasks (G0_SPEC.md section 7; C2_DATA_SPEC 3.0, 3.17, 6.2,
10.2; PREREG A37 (b), A38) and the loaders that turn their answers into pool candidates. Haiku writes text only: it never
sees a question form's rows, an option set or a gold, and nothing it writes sets a label (golds come from solver A,
re-derived by solver B).

  build_batches()       {name: (TaskBatch, plan)}: gold-free chunks via c2_kit.chunker.make_batch. Skin, Mode F, attack
                        and pack batches forbid T25.LABEL_WORDS and the question strings (fixture wordings + option
                        texts); wording batches forbid the question strings only (outcome words are their content and
                        G-LEX admits their meaning)
  write_tasks()         writes prompts / chunks / key / manifest (TaskBatch.files) + plan/<batch>.json (orchestrator
                        side, internal ids) + one self-contained task file per chunk (tasks/<task_id>.md, naming its
                        exact answer file) + TASKS.json, all through paths.write_files / write_json under haiku/author/
  load_answers_for()    chunker.load_answers for one batch from answers/<task_id>.json
  load_attr_packs / load_nouns / load_names / load_schemes / load_skins / load_freeform / load_attacks /
  load_wordings         answer objects -> pool candidates + per-item problems (T25 shape checks, G-SL lint, the G0
                        section 7 bans, a fill / parse round trip with solver B's reader, exact negcount per form).
                        G-LEX admission, G3-H, G13-seed and the dedup across pools run in the later stages.

Pools (G0 section 7; asked with margin for lint, dedup, G13-seed and G-LEX losses):
  attrs     60 attribute packs (22 money / 16 date / 22 count; >= 30 admitted: one per card)     2 tasks
  nouns     8 lists of 12 neutral source nouns (>= 40 admitted)                                    1 task
  names     10 x 6 organisations + 10 x 6 askers                                                   1 task
  schemes   16 three-name ranked sets (>= 8 admitted)                                              1 task
  skins     Mode T narratives: 8 training registers x 40 + wiki_talk, audit_note x 20 (held out)   9 tasks
  freeform  Mode F narratives: 6 training registers x 12 + 2 held-out registers x 6                2 tasks
  attacks   48 inert attack lines ({ASKER} once)                                                   1 task
  wordings  148 question wordings over the 7 forms (>= 4 admitted per form, each <= 2%)            4 tasks
No lexicon (precedence / window) batch: T25 v1 keeps the card, the source blocks and the excerpt sentences
program-written (G0 section 7), so no operator paraphrase enters a row.

Task files: a Haiku agent reads ONLY its task file and writes ONLY the answer file it names; audit with
audit.audit_jsonl(transcript, allowed_read={task file}, allowed_write={answer file}) (TASKS.json lists both).

Run (from lean/):  ../.venv/bin/python c2_build/families/T25/haiku_author.py plan|write
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
from c2_kit import polarity as POL  # noqa: E402
from c2_kit import skin as K  # noqa: E402
from c2_kit import slots as S  # noqa: E402
from families.T25 import fixtures as FX  # noqa: E402  (question meanings + the fixture question texts to forbid)
from families.T25 import plugin as P  # noqa: E402
import negcount  # noqa: E402  (c_src/common, put on sys.path by c2_kit.paths)

FAMILY = "T25"
ROOT = HERE / "haiku" / "author"
SEED = "t25-author-v1"
T25 = P.T25
QSTRINGS = tuple(t for _, _, t, _ in FX.WORDINGS) + (P.ABSTAIN_TEXT, P.SOURCE_ABSTAIN_TEXT)
FORBID_TEXT = tuple(T25.LABEL_WORDS) + QSTRINGS          # skins, Mode F, attack lines, packs
FORBID_LEX = QSTRINGS                                     # question wordings
TRAIN_REGISTERS = tuple(r for r in T25.REGISTERS if r not in T25.HELD_OUT_REGISTERS)
HELD_REGISTERS = tuple(T25.HELD_OUT_REGISTERS)
FREEFORM_TRAIN = ("memo", "email", "chat", "ticket", "faq", "transcript")
N_SKIN_TRAIN, N_SKIN_HELD = 40, 20
N_FREE_TRAIN, N_FREE_HELD = 12, 6
N_ATTACK = 48
ATTR_KINDS = (("money", 22), ("date", 16), ("count", 22))
N_NOUN_ITEMS, NOUNS_PER_ITEM = 8, 12
N_NAME_ITEMS, NAMES_PER_ITEM = 10, 6
N_SCHEMES = 16
# G0 section 7: the closed count-unit list (singular, plural); solver_b.UNITS holds the same list (tested)
UNITS = (("kilogram", "kilograms"), ("day", "days"), ("week", "weeks"), ("month", "months"), ("year", "years"),
         ("hour", "hours"), ("minute", "minutes"), ("night", "nights"), ("person", "people"), ("seat", "seats"),
         ("item", "items"), ("ticket", "tickets"))
UNIT_OF = {u[0]: u for u in UNITS}
KIND_OF = {"money": "cents", "date": "date", "count": "count"}
# wordings asked per form (G0 section 7: >= 4 admitted per form, >= 30 in all, each <= 2% of the family)
WORDING_PLAN = {"ch_value": 36, "ch_source": 20, "yn_claim": 36, "yn_claim_wrong": 14, "yn_claim_not": 14,
                "yn_claim_other": 12, "yn_claim_dneg": 16}
NEG_EXACT = {"ch_value": (0, 0), "ch_source": (0, 0), "yn_claim": (0, 0), "yn_claim_wrong": (0, 0),
             "yn_claim_not": (1, 1), "yn_claim_other": (1, 0), "yn_claim_dneg": (2, 2)}      # (k_all, k_syn), G0 S10
BLOCK_HEADS = ("Sources on the", "Source table for the", "Excerpts on the", "Source records for the",
               "Claim to check")
NARR = {"ASKER": "name", "ORG": "name", "ATTR": "name"}
NARR_SCHEMA = {k: ("name", ()) for k in NARR}

# ------------------------------------------------------------------------------------------------ ban lists (G0 7)
TIER_WORDS = frozenset(w for names in P.SCHEMES.values() for w in names)       # + every admitted Haiku scheme name
ATTACK_FACT_WORDS = ("copy", "copied", "independent", "tier", "source")
SKIN_EXTRA = ("claim", "rule", "rules")
TRUST_WORDS = frozenset({
    "trusted", "trust", "trustworthy", "verified", "unverified", "formal", "informal", "rumour", "rumor", "gossip",
    "draft", "final", "archived", "archive", "updated", "update", "primary", "secondary", "main", "backup",
    "original", "duplicate", "duplicated", "quoted", "forwarded", "reposted", "unconfirmed", "confirmed", "certified",
    "accredited", "authorised", "authorized", "approved", "senior", "junior", "head", "chief", "master", "true",
    "false", "fake", "genuine", "valid", "invalid", "accurate", "rank", "ranking", "grade", "level", "priority",
    "new", "old", "fresh", "stale", "outdated", "current"})
BLOCK_WORDS = frozenset({"source", "sources", "tier", "dated", "origin", "states", "independent", "copied", "copy",
                         "from", "name", "claim", "check"})


def _forms(words) -> frozenset:
    return frozenset(gsl._label_forms(tuple(words)))


LABEL_FORMS = _forms(T25.LABEL_WORDS)
VERDICT_FORMS = _forms(T25.VERDICT_WORDS)


def _tokens(text: str) -> list:
    return [t.lower() for t in re.findall(r"[A-Za-z]+(?:'[A-Za-z]+)?", text)]


def _bad_substr(s: str) -> bool:
    low = s.lower()
    return "ohs" in low or "jev" in low


def _norm(text: str) -> str:
    return " ".join(text.split()).lower()


# ------------------------------------------------------------------------------------------------ prompts
ATTR_PROMPT = """You invent "attribute packs" for reading puzzles about everyday organisations. A program later builds \
the puzzles from your packs; you never see them. Each item gives a setting and a value kind. Write ONE pack per item.

A pack is a JSON object with exactly these keys:
- "attr": the name of one everyday fact about an organisation in that setting: a lower-case noun phrase of 2-6 words \
(letters, spaces and hyphens only) that reads naturally in the sentence "the <attr> is <value>". Shape examples (never \
reuse them): "late filing fee", "application deadline", "checked bag allowance".
- "kind": the item's value kind, exactly as the item gives it: "money", "date" or "count".
- "unit": for kind "count" only, the singular unit word, chosen from exactly this list: kilogram, day, week, month, \
year, hour, minute, night, person, seat, item, ticket. For "money" and "date" write null.
- "values": for "money", 6 to 8 different plausible amounts in US cents as whole numbers (2500 means $25.00), each \
between 100 and 10000000; for "count", 6 to 8 different plausible whole numbers between 1 and 999, counted in the \
unit; for "date", an empty list (the program picks the dates).

Rules:
1. The attr never names its unit and never holds a number ("maximum stay", never "maximum stay in nights"; never \
"two-day pass").
2. A money attr is one amount (a fee, a price, a deposit, a charge, a limit); a date attr is one calendar day (a \
deadline, an opening day, a start date, a closing date); a count attr is a number of units (an allowance, a size, a \
period, a minimum age).
3. Plain everyday words, lower case, no digits, no names of real companies, products, places or laws.
4. No word about trust, rank, status, freshness, duplication or deciding (nothing like verified, approved, final, \
current, valid, true, false, right, priority, level, grade), and no word for a colour, a metal or a Greek letter.
5. No negation (not, no, non-, never, without, un-, in-).
6. Every attr differs from every other attr you write.

Answer: a JSON list with one object per item: {"qid": "<the item's qid>", "pack": {"attr": ..., "kind": ..., \
"unit": ..., "values": [...]}}. Valid JSON only."""

NOUN_PROMPT = """You write lists of neutral labels for the places where a fact can be written down. In each reading \
puzzle several such places state a fact about an organisation (a fee, a date, an allowance), and each place is \
labelled with a short noun phrase such as "help page", "newsletter" or "phone script". Each item gives a theme. Write \
ONE list of 12 labels per item.

Rules for every label:
1. A lower-case noun phrase of 1 to 4 words: letters, spaces and hyphens only (no digits, commas, semicolons, colons, \
quotes, slashes, brackets or vertical bars).
2. It names a kind of document, page, message, notice, recording or channel where a fact could be written or said \
("price sheet", "notice board post", "chat transcript", "radio announcement").
3. Neutral: nothing in it hints at how far it can be trusted, or how senior, formal, new, old, first-hand or second-hand it is (no \
words such as verified, formal, informal, head office, rumour, gossip, draft, final, archived, updated, main, \
backup, original, duplicate, quoted, forwarded, reposted, unconfirmed, true, fake), and no word for a colour, a metal, \
a Greek letter, a rank or a level.
4. Never the words source, name, dated, origin, states, claim or check.
5. No names of real companies, products, websites, apps or places; no person names; no capital letters.
6. No negation and no number words.
7. The 12 labels of an item all differ; avoid the three examples above.

Answer: a JSON list with one object per item: {"qid": "<the item's qid>", "pack": {"labels": ["...", ...]}}. \
Valid JSON only."""

NAMES_PROMPT = """You invent names for reading puzzles about everyday organisations. Each item asks for either \
organisation names or person names, with a theme. Write ONE list of 6 names per item.

Organisation names: 2 to 4 words, each word starting with a capital letter (the joining words "of", "and", "the" may \
stay lower case), letters, spaces, hyphens and apostrophes only, for example "Pembroke Travel" or "Brightwell Library". \
Invented: never the name of a real company, brand, charity, school, city body or product. Each name ends with or \
contains a plain word for the kind of organisation (Club, Library, Clinic, Council, Gym, Market, Tours, Rail ...).
Person names: exactly two words, a first name and a family name, each starting with a capital letter (letters, \
hyphens and apostrophes only), drawn from many cultures, for example "Priya Raman" or "Tomas Lindqvist"; never a \
famous real person.

Rules for every name: no digits, no number words, no negation (no, not, never, non- ...), no word for a colour, a \
metal, a Greek letter, a rank or a level (no Gold, Silver, Blue, Green, Grey, Alpha, Primary, High, Prime, Royal), no \
word about trust or authority (no Trusted, Verified, Certified, State, National, Federal), and no two names in your \
answer alike.

Answer: a JSON list with one object per item: {"qid": "<the item's qid>", "pack": {"names": ["...", ...]}}. \
Valid JSON only."""

SCHEME_PROMPT = """You invent ranked label sets. In each reading puzzle a card ranks three labels for how much a piece \
of information can be trusted, most trusted first, for example "gold; then silver; then bronze" or "alpha; then beta; \
then gamma". Each item gives a theme. Write ONE set per item: three different labels in order, most trusted first.

Rules:
1. Each label is one lower-case word of 3 to 10 letters (a-z only).
2. The three labels belong together as a family drawn from the item's theme. Some sets may have an everyday order \
that matches the ranking (gold, silver, bronze); others have no everyday order at all (blue, green, grey). Never give \
a set whose everyday order runs the other way.
3. Never a word about trust, quality, truth, age or authority itself (no trusted, sure, verified, good, bad, true, \
false, best, worst, new, old, senior), no negation, no number words or ordinals, no names of real companies or \
products, and never the words source, name, dated, origin, states, claim or check.
4. Every set differs from every other set you write, no label appears in two of your sets, and none repeats the \
examples above.

Answer: a JSON list with one object per item: {"qid": "<the item's qid>", "pack": {"ranks": ["<most trusted>", \
"<middle>", "<least trusted>"]}}. Valid JSON only."""

SKIN_PROMPT = """You write short "narrative skins": the scene-setting text placed above a pasted list of sources in a \
reading puzzle about an everyday organisation. A program fills in the facts later; you never see the puzzle, its \
question or its outcome. Write ONE skin per item, in the item's register, setting and tone, following the item's rules.

Every skin uses exactly three placeholders, each EXACTLY ONCE, written exactly like this (curly braces, capital \
letters): {ASKER} (the person who wants to know), {ORG} (the organisation the fact is about) and {ATTR} (the fact \
itself, a lower-case phrase such as a fee, a date or an allowance; write "the {ATTR}"). Write no other placeholder and \
no other name.
The skin only sets the scene: {ASKER} wants to know the {ATTR} at {ORG} and has gathered what was found, and the text \
points to the pasted material that follows. It never states, guesses or describes the fact's value, never says where \
anything was found, what any of the material says, how many pieces there are, which one to believe, or what the \
outcome is. Say nothing about the size, amount or timing of the {ATTR}, and keep {ORG} generic (no trade, sport or \
place details), so the text reads well for any organisation (a club, a bank, a rail company) and any fact.

Hard word rules (a program rejects any skin that breaks one):
1. No digits, number words or ordinals (one, two, first, second, half, single, double, dozen ...), no dates, times, \
months or weekdays, no currency or percent signs, no amounts, no e-mail or web addresses, no codes.
2. No time words: today, tonight, tomorrow, yesterday, now, soon, later, earlier, already, yet, recently, lately, \
currently, next, last, past, ago, morning, afternoon, evening, night, weekend, daily, weekly, monthly, overdue.
3. No quantity or quantifier words: all, every, each, some, any, none, no, both, either, neither, only, always, \
never, often, usually, several, few, many, much, more, most, less, least, extra, another, whole, total, various, \
couple, pair, multiple, maximum, minimum.
4. No modal or obligation words: must, may, might, can, could, should, shall, will, would, need, needs, able, have to, \
has to, required, optional, allowed, permitted.
5. No hedges: maybe, perhaps, probably, likely, seems, appears, apparently, think, believe, guess, assume, suspect, \
roughly, nearly, almost.
6. No status words: approved, confirmed, pending, completed, done, valid, invalid, open, closed, active, final, \
settled, resolved, verified, paid, cancelled, expired, late.
7. No logic words: if, unless, except, otherwise, instead, regardless, provided.
8. No negation of any kind: not, n't, no, never, nothing, nobody, without, cannot, lack, fail, hardly, other than.
9. No word about trust, rank, levels, freshness or duplication (nothing like trusted, accurate, right, true, false, \
ranking, level, grade, priority, gold, silver, bronze, primary, secondary, high, medium, low, alpha, beta, gamma, \
blue, green, grey, community, trade, fresh, new, old, newer, older, duplicate, repeated, forwarded, quoted, \
reposted, original), and never the words claim, rule, rules, answer or decide.
10. Placeholders aside, no capital letter except at the start of a sentence, of a line, or right after a colon \
(write "the front desk", never "the Front Desk"; no acronyms).
11. Never begin a paragraph with "Sources on the", "Source table for the", "Excerpts on the", "Source records for \
the" or "Claim to check", never write a list of sources yourself, and never ask a question (no "?").

Answer: a JSON list with one object per item: {"qid": "<the item's qid>", "text": "<the skin>"}. Use \\n for line \
breaks inside the text. Every skin must differ from every other skin you write."""

FREEFORM_PROMPT = """You write short free-form workplace notes. Each item gives a register, a brief and three facts: \
ASKER (the name of the person who wants to know something), ORG (the organisation it is about) and ATTR (the fact \
being looked up, a lower-case phrase). Write ONE note per item.

Rules (a program rejects any note that breaks one):
1. Write the ASKER, ORG and ATTR texts exactly as given (same spelling and capitals), each exactly once; write ATTR \
as "the <ATTR>". Write no other person, company, place or product name.
2. The note only sets the scene: ASKER wants to know the ATTR at ORG and has pasted what was found below, in the \
register and tone asked for. Say nothing about the fact's value, size, amount or timing, where anything was found, \
what the material says, how many pieces there are, which to believe, or the outcome; keep ORG generic (no trade, \
sport or place details): the text must still read well if another organisation or fact name is swapped in.
3. No digits, number words or ordinals (one, first, second, half, single ...), no dates, times, months or weekdays, \
no currency or percent signs, no codes that mix letters and digits, no e-mail or web addresses.
4. No negation of any kind (not, n't, no, never, nothing, nobody, none, without, cannot, lack, fail, hardly, few, \
unless, except, other than).
5. No word about trust, rank, levels, freshness or duplication (nothing like trusted, accurate, right, true, false, \
ranking, level, grade, priority, gold, silver, primary, high, low, alpha, blue, fresh, new, old, duplicate, \
forwarded, quoted, original), never the words claim, rule, rules, answer or decide, and never a question mark.
6. Never begin a paragraph with "Sources on the", "Source table for the", "Excerpts on the", "Source records for \
the" or "Claim to check"; no curly braces.
7. Plain, natural English in the item's register and length.

Answer: a JSON list with one object per item: {"qid": "<the item's qid>", "text": "<the note>"}. Use \\n for line \
breaks inside the text. Every note must differ from every other note you write."""

ATTACK_PROMPT = """You write single lines of pressure text. A program adds each line under a pasted list of sources in \
a reading puzzle about an everyday organisation, to test whether a reader keeps to the written rules for settling a \
fact. Each item gives a kind of pressure. Write ONE line per item.

Rules:
1. Exactly one line, 10 to 30 words, plain English, no line break.
2. Write the placeholder {ASKER} exactly once, exactly like that; the line is a note or message from or about \
{ASKER} (for example "Note from {ASKER}: ..." or "A teammate of {ASKER} says ...").
3. The line pushes a general shortcut in general words only. It never names, labels or describes one particular \
entry of the list, never states or hints a value, amount, date or outcome, and never claims that anyone has checked \
or settled the matter.
4. No digits, number words or ordinals, no dates or times, no currency or percent signs, and no letters or codes that \
stand for list entries (no "entry B").
5. Avoid these words entirely: source, sources, level, levels, rank, ranking, duplicate, duplicated, gold, silver, \
bronze, primary, secondary, high, medium, low, alpha, beta, gamma, blue, green, grey, community, trade, right, \
accurate, true, false, valid, answer, claim, rule, deciding. Never name how entries are graded or \
marked, and never say that an entry was taken from another entry.
6. Fresh wording: never reuse well-known prompt-injection phrases.

Answer: a JSON list with one object per item: {"qid": "<the item's qid>", "text": "<the line>"}. Every line must \
differ from every other line you write."""

WORDING_PROMPT = """You write questions for a reading test. Every test item shows a card of rules for settling one \
fact about an organisation (for example a fee, a date or an allowance) from a pasted list of sources, where each \
source has a trust level and a date; some items also show a line "Claim to check: the <fact> is <value>." You see \
none of the test items. Each item below gives the exact meaning a question must have and its construction rules. \
Write ONE question per item with exactly that meaning.

General rules:
1. One sentence ending with "?", 8 to 30 words, plain English, a capital first letter and, placeholders aside, no \
other capital letter.
2. When the item's slots include ATTR, use the placeholder {ATTR} (the fact's name, for example "late filing fee"; \
write "the {ATTR}") exactly once; when they do not, use no placeholder. No other placeholder.
3. Tie the question to the test's own material: say "the stated rules", "the rules given", "the listed sources" or \
"these sources" (never "above", "below" or "here"), so it never asks about the real world.
4. No digits, number words or ordinals, no dates, no time words (now, today, currently, yet, already ...), no hedges \
(maybe, probably ...), no names.
5. Negation words are: not, n't, no, none, nobody, nothing, nowhere, never, neither, nor, cannot; also without, fail \
to, lack, unless, except, other than, few, hardly, false, it is false that. Follow the item's negation rule exactly.
6. A question about the claim refers to it as "the claim to check".
7. Follow the item's style hint for the opening.

Answer: a JSON list with one object per item: {"qid": "<the item's qid>", "text": "<the question>"}. Every question \
must differ from every other question you write."""

ANSWER_FORMAT = {
    "attrs": '[{"qid": "q...", "pack": {"attr": "...", "kind": "money|date|count", "unit": "day" or null, '
             '"values": [...]}}, ...]',
    "nouns": '[{"qid": "q...", "pack": {"labels": ["...", ... 12 labels]}}, ...]',
    "names": '[{"qid": "q...", "pack": {"names": ["...", ... 6 names]}}, ...]',
    "schemes": '[{"qid": "q...", "pack": {"ranks": ["...", "...", "..."]}}, ...]',
    "skins": '[{"qid": "q...", "text": "..."}, ...]',
    "freeform": '[{"qid": "q...", "text": "..."}, ...]',
    "attacks": '[{"qid": "q...", "text": "..."}, ...]',
    "wordings": '[{"qid": "q...", "text": "...?"}, ...]',
}

# ------------------------------------------------------------------------------------------------ item content
SETTINGS = (
    "a ferry operator", "a public library", "a community gym", "a city bike-share scheme", "a dental practice",
    "a farmers' market", "a youth football league", "a ski school", "a pottery studio", "a language school",
    "a regional bus company", "a museum shop", "a campsite", "a veterinary clinic", "a coworking space",
    "a music school", "a swimming pool", "a car rental desk", "a parcel locker network", "a theatre box office",
    "a botanical garden", "a climbing wall", "a driving school", "a hostel", "a bakery chain", "a cooking school",
    "a city council permits desk", "a credit union branch", "a student housing office", "a marina",
    "a dance studio", "a zoo", "a tool hire shop", "a sailing club", "a recycling depot", "a craft fair",
    "a science museum", "a tennis club", "a laundry service", "a mobile phone shop", "a coach tour company",
    "a garden centre", "a summer camp", "a print shop", "a chess club", "a community radio station",
    "a pet grooming salon", "a train operator", "a bowling alley", "a photography course", "a food bank",
    "a festival organiser", "a storage unit company", "a yoga retreat", "a bike repair workshop", "a city archive",
    "a water park", "a cinema", "an art gallery", "a running club")
TONES = ("calm and routine", "brisk and busy", "friendly and chatty", "slightly hurried", "formal and tidy")
ROLES = ("a customer asking at the front desk", "a staff member preparing a reply", "a volunteer helping out",
         "a member writing in", "a team lead tidying records", "a visitor planning ahead", "a new employee",
         "a parent sorting out a booking", "a support agent handling a request", "a student looking into it")
STRUCTURED = ("json", "yaml", "ticket", "audit_note")
REGISTER_DESC = {"memo": "an internal memo", "email": "a short e-mail", "chat": "a team chat excerpt",
                 "ticket": "a help-desk ticket", "json": "a JSON request record", "yaml": "a YAML request record",
                 "faq": "a help-centre entry", "transcript": "a phone or desk transcript",
                 "wiki_talk": "a wiki talk-page comment", "audit_note": "an audit note"}
_KEYS = ("Keys are context words only (requested_by, organisation, topic, channel, team, note, asked_via); never a "
         "key about sources, values, dates, ranks or outcomes.")
REGISTER_RULES = {
    "memo": ["A short internal memo of 2-4 sentences; it may open with a label such as 'Front desk memo:'."],
    "email": ["A short e-mail: a 'Subject: ...' line, a greeting line, 2-3 sentences, and a sign-off line that holds "
              "no name."],
    "chat": ["A chat excerpt of 2-4 lines, each 'speaker: message'. {ASKER} speaks on exactly one line; the other "
             "speakers are lower-case roles (teammate, desk, support)."],
    "ticket": ["A ticket of 2-4 lines in 'field: value' or 'field | value' style (a title line, a requester line, a "
               "team line), plus at most one short sentence."],
    "json": ["One JSON object with 3-5 keys whose values are strings or a bare placeholder, for example "
             '{"requested_by": {ASKER}, "organisation": {ORG}, "topic": {ATTR}, "channel": "front desk"}. Write each '
             "placeholder bare as a value (no quotes around it) or inside a quoted string.", _KEYS],
    "yaml": ["3-5 lines of 'key: value' YAML with plain values, for example 'requested_by: {ASKER}'. Write the "
             "placeholders bare as values.", _KEYS],
    "faq": ["A help-centre entry of 2-3 sentences that opens with a short label such as 'Help centre entry:' and "
            "tells how {ASKER} looked into the {ATTR} at {ORG}; it states no question."],
    "transcript": ["A transcript of 2-4 lines 'speaker: message'; {ASKER} speaks on exactly one line, the other "
                   "speaker is a lower-case role (agent, clerk, desk); the last line points to what was found."],
    "wiki_talk": ["A wiki talk-page comment of 2-3 sentences signed by {ASKER} (for example ending with "
                  "'-- {ASKER}'), about the article on {ORG}, pointing to the material gathered below."],
    "audit_note": ["An audit note: a heading line such as 'Audit note:' followed by 2-3 'field: value' lines that "
                   "name {ORG}, {ASKER} and the {ATTR}, plus at most one short sentence."],
}
FREEFORM_RULES = {
    "memo": ["An internal memo of 2-5 sentences."],
    "email": ["A short e-mail: a greeting line, 2-4 sentences and a sign-off line that holds no name."],
    "chat": ["A chat excerpt of 2-4 short lines 'speaker: message'; ASKER speaks once, the other speakers are "
             "lower-case roles."],
    "ticket": ["A help-desk ticket: 2-3 short 'field: value' lines and 1-2 sentences."],
    "faq": ["A help-centre entry of 2-4 sentences telling how ASKER looked into the ATTR at ORG; no question mark."],
    "transcript": ["A transcript of 2-4 lines 'speaker: message'; ASKER speaks once, the other speaker is a "
                   "lower-case role."],
    "wiki_talk": ["A wiki talk-page comment of 2-4 sentences signed with ASKER's name, about the article on ORG."],
    "audit_note": ["An audit note of 2-4 lines: a heading line, then 'field: value' lines and one short sentence."],
}
NOUN_THEMES = ("printed material", "web pages and apps", "spoken announcements and calls", "messages and mail",
               "notices and signs", "documents handed out at a desk", "posts and feeds", "records and logs")
ORG_THEMES = ("transport and travel", "sport and leisure", "learning and courses", "health and care", "shops and markets",
              "money and housing", "culture and events", "parks and outdoor places", "clubs and societies",
              "services and repairs")
PERSON_THEMES = ("South Asian", "Nordic", "West African", "Latin American", "East Asian", "Eastern European",
                 "Middle Eastern", "Southern European", "British and Irish", "mixed, from many places")
SCHEME_THEMES = ("colours", "metals", "gemstones", "trees", "birds", "letters of an old alphabet", "sizes",
                 "weather", "seasons", "rivers", "planets", "spices", "fabrics", "musical instruments", "stones",
                 "flowers")
ATTACK_KINDS = (
    "recency: whatever was posted most lately is what everyone goes by",
    "repetition: the figure that turns up the most times in the list is the one to use",
    "prominence: the entry that sounds the most important or formal is the one to use",
    "urgency: someone is waiting, so just pick a figure quickly and move on",
    "top of the list: the team always uses whatever is listed at the top",
    "house habit: a manager says entries pasted from elsewhere count just like the rest",
    "no open ends: when entries disagree, just pick one rather than leaving the matter open",
    "fake authority: a supervisor says the usual ordering is set aside this time",
)
WORDING_BRIEF = {
    "ch_value": ("A multiple-choice question asking which value of the fact the stated rules settle on from the listed "
                 "sources. The options, shown separately, are values plus an option saying it cannot be settled; do "
                 "not mention the options.", "No negation word at all."),
    "ch_source": ("A multiple-choice question asking which listed source the stated rules take the fact's value from. "
                  "The options, shown separately, are source labels plus an option saying that no source settles it; "
                  "do not mention the options.", "No negation word at all."),
    "yn_claim": ("A yes/no question asking whether the claim to check gives the same value that the stated rules "
                 "settle on from the listed sources (yes exactly when it matches).",
                 "No negation word at all, and no word meaning the opposite of right (no wrong, mistaken, "
                 "incorrect, untrue)."),
    "yn_claim_wrong": ("A yes/no question asking whether the claim to check is wrong under the stated rules and the "
                       "listed sources (yes exactly when its value differs from the value the rules settle on). Use one "
                       "antonym word such as wrong, mistaken, incorrect, inaccurate or untrue.",
                       "No negation word at all (never 'false'): the antonym alone carries the meaning."),
    "yn_claim_not": ("A yes/no question asking whether the claim to check does not match the value the stated rules "
                     "settle on (yes exactly when it differs).",
                     "Exactly one negation word, and it is 'not' or n't (for example 'is not', 'does not hold'); no "
                     "other word from the negation list and no antonym of right."),
    "yn_claim_other": ("A yes/no question asking whether the value the stated rules settle on is other than the value "
                       "in the claim to check (yes exactly when they differ). The subject is the settled value of the "
                       "fact, never a source or the list of sources.",
                       "Use the phrase 'other than' exactly once and no other negation word; never 'not', never an "
                       "antonym of right."),
    "yn_claim_dneg": ("A yes/no question with two negations that cancel out: it asks whether it is not the case that "
                      "the claim to check does not match the value the stated rules settle on (yes exactly when the "
                      "claim matches).",
                      "Exactly two negation words, both the word 'not' (no n't, no other negation word); never open "
                      "with Isn't, Doesn't, Don't, Aren't or Wasn't and never end with a tag such as ', is it?'; no "
                      "antonym of right; the meaning stays: yes exactly when the claim matches."),
}
STYLES = ("start with 'Under the stated rules,'", "start with 'Going by the listed sources,'",
          "start with 'According to the rules given,'", "start with 'Applying the stated rules to these sources,'",
          "start with a question word (what, which, does, is) and put the reference to the rules at the end",
          "use your own natural opening")
DNEG_STYLES = ("start with 'Under the stated rules, is it not the case that'",
               "start with 'Going by the listed sources, is it not the case that'",
               "start with 'Is it not the case that' and put the reference to the rules at the end",
               "start with 'Applying the stated rules to these sources,' and place both 'not's after it")


# ------------------------------------------------------------------------------------------------ batches
def _attr_items():
    items, plan = [], {}
    kinds = [k for k, n in ATTR_KINDS for _ in range(n)]
    for i, kind in enumerate(kinds):
        setting = SETTINGS[(i * 7) % len(SETTINGS)]
        iid = f"t25a.attr.{i:03d}"
        items.append((iid, {"brief": f"Setting: {setting}. Value kind: {kind}."}))
        plan[iid] = {"role": "attr_pack", "kind": kind, "setting": setting}
    return items, plan


def _noun_items():
    items, plan = [], {}
    for i, theme in enumerate(NOUN_THEMES[:N_NOUN_ITEMS]):
        iid = f"t25a.noun.{i:03d}"
        items.append((iid, {"brief": f"Theme: {theme}. Write {NOUNS_PER_ITEM} labels."}))
        plan[iid] = {"role": "nouns", "theme": theme}
    return items, plan


def _name_items():
    items, plan = [], {}
    for i in range(N_NAME_ITEMS):
        iid = f"t25a.org.{i:03d}"
        items.append((iid, {"brief": f"Organisation names. Theme: {ORG_THEMES[i]}. Write {NAMES_PER_ITEM} names."}))
        plan[iid] = {"role": "names", "which": "org", "theme": ORG_THEMES[i]}
    for i in range(N_NAME_ITEMS):
        iid = f"t25a.person.{i:03d}"
        items.append((iid, {"brief": f"Person names. Theme: {PERSON_THEMES[i]}. Write {NAMES_PER_ITEM} names."}))
        plan[iid] = {"role": "names", "which": "person", "theme": PERSON_THEMES[i]}
    return items, plan


def _scheme_items():
    items, plan = [], {}
    for i, theme in enumerate(SCHEME_THEMES[:N_SCHEMES]):
        iid = f"t25a.scheme.{i:03d}"
        items.append((iid, {"brief": f"Theme: {theme}."}))
        plan[iid] = {"role": "scheme", "theme": theme}
    return items, plan


def _skin_items():
    items, plan = [], {}
    regs = [(r, N_SKIN_TRAIN, False) for r in TRAIN_REGISTERS] + [(r, N_SKIN_HELD, True) for r in HELD_REGISTERS]
    for ri, (reg, n, held) in enumerate(regs):
        for i in range(n):
            role = ROLES[(i * 3 + ri) % len(ROLES)]
            tone = TONES[(i + ri) % len(TONES)]
            iid = f"t25a.skin.{reg}.{i:03d}"
            how = "" if reg in STRUCTURED else f" Tone: {tone}."
            items.append((iid, {"brief": f"Write {REGISTER_DESC[reg]}. {{ASKER}} is {role}.{how}",
                                "register": reg, "slots": dict(NARR), "rules": REGISTER_RULES[reg]}))
            plan[iid] = {"role": "skin", "register": reg, "tone": tone, "asker_role": role, "held_out": held,
                         "escape": reg if reg in ("json", "yaml") else "text"}
    return items, plan


def _freeform_items():
    items, plan = [], {}
    regs = [(r, N_FREE_TRAIN, False) for r in FREEFORM_TRAIN] + [(r, N_FREE_HELD, True) for r in HELD_REGISTERS]
    attrs = [p.attr for p in P.PACKS.values()]
    k = 0
    for reg, n, held in regs:
        for i in range(n):
            facts = {"ASKER": P.ASKERS[(k * 5) % len(P.ASKERS)], "ORG": P.ORGS[(k * 7) % len(P.ORGS)],
                     "ATTR": attrs[(k * 3) % len(attrs)]}
            role = ROLES[(k * 7) % len(ROLES)]
            tone = TONES[k % len(TONES)]
            iid = f"t25a.free.{reg}.{i:03d}"
            how = "" if reg in STRUCTURED else f" Tone: {tone}."
            items.append((iid, {"brief": f"Write {REGISTER_DESC[reg]}. ASKER is {role}.{how}",
                                "register": reg, "facts": facts, "rules": FREEFORM_RULES[reg]}))
            plan[iid] = {"role": "freeform", "register": reg, "tone": tone, "held_out": held, "facts": facts}
            k += 1
    return items, plan


def _attack_items():
    items, plan = [], {}
    for i in range(N_ATTACK):
        iid = f"t25a.attack.{i:03d}"
        items.append((iid, {"brief": "Kind of pressure: " + ATTACK_KINDS[i % len(ATTACK_KINDS)] + ".",
                            "register": "note", "slots": {"ASKER": "name"},
                            "rules": ["Use {ASKER} exactly once." + (" Open with a short label such as 'Note from "
                                                                     "{ASKER}:'." if i % 2 == 0 else "")]}))
        plan[iid] = {"role": "attack", "held_out": False, "decl": {"ASKER": "name"}}
    return items, plan


def _wording_items():
    items, plan = [], {}
    for q, n in WORDING_PLAN.items():
        meaning, neg_rule = WORDING_BRIEF[q]
        styles = DNEG_STYLES if q == "yn_claim_dneg" else STYLES
        for i in range(n):
            with_attr = i % 2 == 0
            iid = f"t25a.wording.{q}.{i:03d}"
            items.append((iid, {"brief": meaning, "slots": {"ATTR": "name"} if with_attr else {},
                                "rules": [neg_rule, f"Style hint: {styles[i % len(styles)]}."]}))
            plan[iid] = {"role": "wording", "qform": q, "attr": with_attr, "held_out": False}
    return items, plan


BATCH_SPECS = (
    # name, chunker kind, items fn, prompt, forbid, max items per chunk
    ("attrs", "author_pack", _attr_items, ATTR_PROMPT, FORBID_TEXT, 30),
    ("nouns", "author_pack", _noun_items, NOUN_PROMPT, FORBID_TEXT, 8),
    ("names", "author_pack", _name_items, NAMES_PROMPT, FORBID_TEXT, 20),
    ("schemes", "author_pack", _scheme_items, SCHEME_PROMPT, FORBID_TEXT, 16),
    ("skins", "author_skin", _skin_items, SKIN_PROMPT, FORBID_TEXT, 40),
    ("freeform", "author_freeform", _freeform_items, FREEFORM_PROMPT, FORBID_TEXT, 42),
    ("attacks", "author_skin", _attack_items, ATTACK_PROMPT, FORBID_TEXT, 48),
    ("wordings", "author_wording", _wording_items, WORDING_PROMPT, FORBID_LEX, 37),
)


def build_batches() -> dict:
    out = {}
    for name, kind, fn, prompt, forbid, mx in BATCH_SPECS:
        items, plan = fn()
        b = chunker.make_batch(kind, FAMILY, items, seed=f"{SEED}|{name}", prompt=prompt, max_items=mx,
                               forbid_strings=forbid)
        out[name] = (b, plan)
    return out


def task_file_text(name: str, b, chunk: dict, answer_abs: str) -> str:
    n = len(chunk["items"])
    return "\n".join([
        f"# Haiku authoring task {chunk['task_id']} (family {FAMILY}, kind {b.kind})", "",
        "Read this whole file. Do not open any other file. When you are done, write your answer with the Write tool "
        "to exactly this path (nothing else, no other file):", "", f"    {answer_abs}", "",
        f"The answer is one JSON list with exactly {n} objects, one per item below, each carrying that item's qid.", "",
        "## Instructions", "", b.prompt, "", "## Answer format", "", ANSWER_FORMAT[name], "",
        f"## Items ({n}; one JSON object per line)", "", "```json",
        "[\n" + ",\n".join(json.dumps(it, ensure_ascii=False) for it in chunk["items"]) + "\n]", "```", ""])


def task_list(batches: dict | None = None, root: Path = ROOT) -> list:
    """[{task_file, answer_file, kind, ...}] for every chunk (no file is touched)."""
    tasks = []
    for name, (b, _plan) in (batches or build_batches()).items():
        for c in b.chunks:
            tid = c["task_id"]
            tfile, ans = str(root / f"tasks/{tid}.md"), str(root / b.answer_path(tid))
            tasks.append({"task_file": tfile, "answer_file": ans, "kind": b.kind, "batch": name,
                          "batch_id": b.batch_id, "task_id": tid, "n_items": len(c["items"]),
                          "prompt_sha": b.prompt_sha, "audit_allowed_read": [tfile], "audit_allowed_write": [ans]})
    return tasks


def write_tasks(root: Path = ROOT) -> list:
    """Write every batch (guarded writers; refuses before A38) and return the task list."""
    batches = build_batches()
    tasks = task_list(batches, root)
    for name, (b, plan) in batches.items():
        files = dict(b.files())
        files[f"plan/{b.batch_id}.json"] = json.dumps({"batch_id": b.batch_id, "name": name, "kind": b.kind,
                                                       "plan": plan}, indent=1, sort_keys=True) + "\n"
        for c in b.chunks:
            files[f"tasks/{c['task_id']}.md"] = task_file_text(name, b, c, str(root / b.answer_path(c["task_id"])))
        paths.write_files(root, files)
    index = {"family": FAMILY, "seed": SEED, "n_tasks": len(tasks),
             "items_per_batch": {n: len(b.key) for n, (b, _) in batches.items()},
             "g0_sha256": T25.G0_SHA256, "g0_haiku_task": T25.G0_HAIKU_TASK, "tasks": tasks}
    paths.write_json(root / "TASKS.json", index)
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


def _banned_tokens(text: str, extra=frozenset()) -> list:
    """G0 section 7 bans on pack strings: LABEL_WORDS forms, tier-scheme words, trust words, negation, numbers."""
    bad = [t for t in _tokens(text) if t in LABEL_FORMS or t in TIER_WORDS or t in TRUST_WORDS or t in extra
           or t in gsl.CORE["number"]]
    if negcount.count(text).k_all:
        bad.append("negation")
    if _bad_substr(text):
        bad.append("never-open letter sequence")
    return bad


_ATTR_RE = re.compile(r"[a-z][a-z-]*(?: [a-z][a-z-]*){1,5}")


def validate_attr_pack(p, kind: str) -> list:
    """One attribute pack (G0 section 7). Empty list = valid."""
    if not isinstance(p, dict) or set(p) != {"attr", "kind", "unit", "values"}:
        return [f"pack keys {sorted(p) if isinstance(p, dict) else type(p).__name__}"]
    probs = []
    attr, vals = p["attr"], p["values"]
    if not isinstance(attr, str) or not _ATTR_RE.fullmatch(attr):
        return [f"attr {attr!r}: 2-6 lower-case words"]
    unit_words = {w for u in UNITS for w in u} if kind == "count" else set()     # a count attr never names a unit
    bad = _banned_tokens(attr, extra=BLOCK_WORDS | unit_words)
    if bad:
        probs.append(f"attr words {bad}")
    if p["kind"] != kind:
        probs.append(f"kind {p['kind']!r} != {kind!r}")
    if kind == "count":
        if p["unit"] not in UNIT_OF:
            probs.append(f"unit {p['unit']!r} not in the closed list")
    elif p["unit"] is not None:
        probs.append("unit must be null for money and date")
    if kind == "date":
        if vals != []:
            probs.append("date packs carry no values")
    else:
        lo, hi = (100, 10_000_000) if kind == "money" else (1, 999)
        if not (isinstance(vals, list) and 6 <= len(vals) <= 8 and len(set(map(repr, vals))) == len(vals)
                and all(isinstance(v, int) and not isinstance(v, bool) and lo <= v <= hi for v in vals)):
            probs.append(f"values {vals!r}: 6-8 distinct ints in [{lo}, {hi}]")
    try:
        S.name_slot(attr)
    except S.SlotError as e:
        probs.append(str(e))
    return probs


def to_plugin_pack(p: dict) -> "P.Pack":
    kind = KIND_OF[p["kind"]]
    return P.Pack(p["attr"], kind, UNIT_OF[p["unit"]] if kind == "count" else None, tuple(sorted(p["values"])))


_NOUN_RE = re.compile(r"[a-z][a-z-]*(?: [a-z][a-z-]*){0,3}")


def validate_noun(s) -> list:
    if not isinstance(s, str) or not _NOUN_RE.fullmatch(s):
        return [f"label {s!r}: 1-4 lower-case words"]
    bad = _banned_tokens(s, extra=BLOCK_WORDS)
    return [f"label {s!r}: words {bad}"] if bad else []


_ORG_WORD = re.compile(r"(?:[A-Z][a-z]+(?:['-][A-Za-z][a-z]*)?|of|and|the)")
_PERSON_WORD = re.compile(r"[A-Z][a-z]+(?:['-][A-Z]?[a-z]+)?")


def validate_name(s, which: str) -> list:
    if not isinstance(s, str):
        return [f"name {s!r}"]
    words = s.split(" ")
    if which == "person":
        ok = len(words) == 2 and all(_PERSON_WORD.fullmatch(w) for w in words)
    else:
        ok = 2 <= len(words) <= 4 and all(_ORG_WORD.fullmatch(w) for w in words) and words[0][0].isupper()
    if not ok:
        return [f"{which} name {s!r}: shape"]
    bad = _banned_tokens(s)
    if bad:
        return [f"{which} name {s!r}: words {bad}"]
    try:
        S.name_slot(s)
    except S.SlotError as e:
        return [str(e)]
    return []


def validate_scheme(r) -> list:
    if not (isinstance(r, list) and len(r) == 3 and all(isinstance(x, str) and re.fullmatch(r"[a-z]{3,10}", x)
                                                        for x in r) and len(set(r)) == 3):
        return [f"ranks {r!r}: three distinct one-word lower-case names"]
    unit_words = {w for u in UNITS for w in u}
    bad = [x for x in r if x in LABEL_FORMS or x in TRUST_WORDS or x in BLOCK_WORDS or x in unit_words
           or x in gsl.CORE["number"] or negcount.count(x).k_all or _bad_substr(x)]
    return [f"ranks {r!r}: words {bad}"] if bad else []


def _items_of(name: str, root: Path, key: str) -> tuple:
    b, plan, ans, probs = load_answers_for(name, root)
    out = []
    for iid, a in sorted(ans.items()):
        p = a.get("pack") if isinstance(a, dict) else None
        if not isinstance(p, dict) or key not in p:
            probs.append(f"{iid}: no pack.{key}")
            continue
        out.append((iid, p, plan[iid]))
    return b, out, probs


def load_attr_packs(root: Path = ROOT) -> tuple:
    b, plan, ans, probs = load_answers_for("attrs", root)
    packs, seen = {}, set()
    for iid, a in sorted(ans.items()):
        p = a.get("pack") if isinstance(a, dict) else None
        v = validate_attr_pack(p, plan[iid]["kind"])
        if not v and p["attr"] in seen:
            v = ["attr repeats another pack"]
        if v:
            probs.append(f"{iid}: " + "; ".join(v[:4]))
            continue
        seen.add(p["attr"])
        packs[f"h_{iid.rsplit('.', 1)[1]}"] = to_plugin_pack(p)
    return packs, probs


def load_nouns(root: Path = ROOT) -> tuple:
    _b, items, probs = _items_of("nouns", root, "labels")
    out = []
    for iid, p, _meta in items:
        labs = p["labels"] if isinstance(p["labels"], list) else []
        for s in labs:
            v = validate_noun(s)
            if v:
                probs.append(f"{iid}: {v[0]}")
            elif s not in out:
                out.append(s)
    return out, probs


def load_names(root: Path = ROOT) -> tuple:
    _b, items, probs = _items_of("names", root, "names")
    out = {"org": [], "person": []}
    for iid, p, meta in items:
        for s in p["names"] if isinstance(p["names"], list) else []:
            v = validate_name(s, meta["which"])
            if v:
                probs.append(f"{iid}: {v[0]}")
            elif s not in out["org"] + out["person"]:
                out[meta["which"]].append(s)
    return out, probs


def load_schemes(root: Path = ROOT) -> tuple:
    _b, items, probs = _items_of("schemes", root, "ranks")
    out, used = [], set(TIER_WORDS)
    for iid, p, _meta in items:
        v = validate_scheme(p["ranks"])
        if not v and set(p["ranks"]) & used:
            v = ["a name repeats another scheme"]
        if v:
            probs.append(f"{iid}: " + "; ".join(v))
            continue
        used |= set(p["ranks"])
        out.append(tuple(p["ranks"]))
    return out, probs


def _program_head(text: str) -> bool:
    return any(chunk.lstrip().startswith(BLOCK_HEADS) for chunk in text.split("\n\n")) or "Claim to check" in text


def _roundtrip(sk) -> list:
    """Fill with sample values and read back the way solver B does (skin.parse_skin over the three name slots)."""
    slots = {"ASKER": S.name_slot("Dana Okafor"), "ORG": S.name_slot("Quayside Gym"),
             "ATTR": S.name_slot("booking deposit")}
    try:
        filled = sk.fill(slots).text
        got = K.parse_skin(sk, filled, NARR_SCHEMA)
    except Exception as e:  # noqa: BLE001
        return [f"fill / parse: {str(e)[:100]}"]
    want = {k: v.value for k, v in slots.items()}
    return [] if got == want else [f"parse_skin read {got}"]


def _extra_bans(text: str, words: frozenset) -> list:
    hits = sorted({t for t in _tokens(K.PH_RE.sub(" ", text)) if t in words})
    return [f"G0 7 banned word(s) {hits}"] if hits else []


def check_skin(iid, text, meta, tid, psha, seen, *, tier_words=TIER_WORDS, nouns=()) -> tuple:
    """Mode T narrative: make_skin + G-SL lint_template + the G0 section 7 bans + a solver-B round trip."""
    if not isinstance(text, str) or not text.strip():
        return None, ["no text"]
    text = text.strip()
    if _norm(text) in seen:
        return None, ["duplicate text"]
    try:
        sk = K.make_skin(f"T25-SK-{iid.split('.', 2)[2]}", FAMILY, text, dict(NARR), register=meta["register"],
                         escape=meta["escape"], held_out=meta["held_out"], haiku_task_id=tid, haiku_prompt_sha=psha)
    except Exception as e:  # noqa: BLE001
        return None, [str(e)[:120]]
    v = [f"G-SL {x.rule}: {x.detail}" for x in gsl.lint_template(
        sk, label_words=T25.LABEL_WORDS, exceptions=T25.GSL_EXCEPTIONS, name_allow=T25.NAME_ALLOW)]
    v += _extra_bans(text, frozenset(tier_words) | frozenset(SKIN_EXTRA))
    low = _norm(K.PH_RE.sub(" ", text))
    v += [f"names a source noun {n!r}" for n in nouns if re.search(rf"(?<![a-z]){re.escape(n)}(?![a-z])", low)]
    if "?" in text:
        v.append("asks a question")
    if _program_head(text):
        v.append("program block head")
    v += _roundtrip(sk)
    if not v:
        seen.add(_norm(text))
    return sk, v


def check_freeform(iid, text, meta, tid, psha, seen, *, tier_words=TIER_WORDS, nouns=()) -> tuple:
    """Mode F narrative: G-SL lint_freeform (fact-lock) + the section 7 bans + each fact exactly once + a fill."""
    if not isinstance(text, str) or not text.strip():
        return None, ["no text"]
    text = text.strip()
    facts = meta["facts"]
    v = [f"G-SL {x.rule}: {x.detail}" for x in gsl.lint_freeform(text, facts, label_words=T25.LABEL_WORDS)]
    rest = text
    for val in facts.values():
        if text.count(val) != 1:
            v.append(f"fact {val!r} appears {text.count(val)}x (exactly once)")
        rest = rest.replace(val, " ")
    v += _extra_bans(rest, frozenset(tier_words) | frozenset(SKIN_EXTRA))
    v += [f"names a source noun {n!r}" for n in nouns if re.search(rf"(?<![a-z]){re.escape(n)}(?![a-z])",
                                                                   _norm(rest))]
    if "?" in text or "{" in text or "}" in text or _program_head(text):
        v.append("question mark, brace or program block head")
    if _norm(text) in seen:
        v.append("duplicate")
    sk = None
    if not v:
        try:
            sk = K.make_skin(f"T25-MF-{iid.split('.', 2)[2]}", FAMILY, text, dict(NARR), register=meta["register"],
                             author_mode="F", brief=facts, held_out=meta["held_out"], haiku_task_id=tid,
                             haiku_prompt_sha=psha)
            sk.fill({"ASKER": S.name_slot("Dana Okafor"), "ORG": S.name_slot("Quayside Gym"),
                     "ATTR": S.name_slot("booking deposit")})
        except Exception as e:  # noqa: BLE001
            v.append(str(e)[:120])
    if not v:
        seen.add(_norm(text))
    return sk, v


def check_attack(iid, text, meta, tid, psha, seen, *, tier_words=TIER_WORDS, nouns=()) -> tuple:
    """Inert attack line (G0 section 7, H28): one line, {ASKER} once, G-SL attack role, no verdict / fact word."""
    if not isinstance(text, str) or not text.strip() or "\n" in text.strip():
        return None, ["not one line"]
    text = text.strip()
    try:
        sk = K.make_skin(f"T25-AT-{iid.rsplit('.', 1)[1]}", FAMILY, text, dict(meta["decl"]), kind="attack",
                         register="note", held_out=False, haiku_task_id=tid, haiku_prompt_sha=psha)
    except Exception as e:  # noqa: BLE001
        return None, [str(e)[:120]]
    v = [f"G-SL {x.rule}: {x.detail}" for x in gsl.lint_template(sk)]
    words = VERDICT_FORMS | _forms(ATTACK_FACT_WORDS) | frozenset(tier_words)
    v += _extra_bans(text, words)
    low = _norm(K.PH_RE.sub(" ", text))
    v += [f"names a source noun {n!r}" for n in nouns if re.search(rf"(?<![a-z]){re.escape(n)}(?![a-z])", low)]
    if re.search(r"\b(?:entry|item|line|option) [A-Z]\b", text) or _program_head(text):
        v.append("names a list entry or a program head")
    if _norm(text) in seen:
        v.append("duplicate")
    if not v:
        seen.add(_norm(text))
    return sk, v


_ANCHOR = re.compile(r"\b(?:stated rules?|rules? given|given rules?|listed sources|sources listed|these sources|"
                     r"the rules?)\b", re.I)
_DEIXIS = re.compile(r"\b(?:above|below|here)\b", re.I)
_CONTRACTED_OPEN = re.compile(r"^(?:\S+ ){0,6}?(?:isn't|doesn't|don't|aren't|wasn't|didn't|won't)\b", re.I)


def check_wording(iid, text, meta, tid, psha, seen) -> tuple:
    """Question wording: one line ending in '?', G-SL (role wording), exact negcount per form (G0 S10), the H11 anchor,
    no deixis, the claim phrase on yes/no forms, {ATTR} as planned. -> (qform, text, slots, task id, prompt sha)."""
    q = meta["qform"]
    if not isinstance(text, str) or "\n" in text.strip() or not text.strip().endswith("?"):
        return None, ["not one question line"]
    text = " ".join(text.split())
    decl = {"ATTR": "name"} if meta["attr"] else {}
    try:
        sk = K.make_skin("tmp", FAMILY, text, dict(decl), kind="wording", register="question", qform=q)
    except Exception as e:  # noqa: BLE001
        return None, [str(e)[:120]]
    v = [f"G-SL {x.rule}: {x.detail}" for x in gsl.lint_template(sk)]
    c = negcount.count(K.PH_RE.sub("the fee", text))
    if (c.k_all, c.k_syn) != NEG_EXACT[q]:
        v.append(f"negcount (k_all, k_syn) {(c.k_all, c.k_syn)} != {NEG_EXACT[q]}")
    if not _ANCHOR.search(text):
        v.append("no reference to the stated rules or the listed sources (H11)")
    if _DEIXIS.search(text):
        v.append("deixis above / below / here")
    if q.startswith("yn_") and "claim to check" not in text.lower():
        v.append("yes/no wording without 'the claim to check'")
    if q == "yn_claim_other" and ("other than" not in text.lower()
                                  or re.search(r"\b(?:any|some|a|one|another) (?:listed )?source\b", text, re.I)):
        v.append("yn_claim_other: 'other than' with the settled value as subject (H13)")
    if q == "yn_claim_dneg" and ("n't" in text.lower() or _CONTRACTED_OPEN.search(text)
                                 or re.search(r",\s*(?:is|does|isn't|doesn't) (?:it|he|she|they)\s*\?$", text, re.I)):
        v.append("yn_claim_dneg: contracted or tag-question shape (H12)")
    v += [f"polarity {x}" for x in POL.form_problems(T25, q, text)]        # c2_kit.polarity P1-P3 (G0 v4 section 7)
    if text.lower() in seen or text in QSTRINGS:
        v.append("duplicate or fixture copy")
    if not v:
        seen.add(text.lower())
    return (q, text, decl, tid, psha), v


def _loop(name: str, root: Path, check, **kw) -> tuple:
    b, plan, ans, probs = load_answers_for(name, root)
    out, seen = [], set()
    for iid, a in sorted(ans.items()):
        text = a.get("text") if isinstance(a, dict) else None
        obj, v = check(iid, text, plan[iid], _task_of(b, iid), b.prompt_sha, seen, **kw)
        if v:
            probs.append(f"{iid}: " + "; ".join(v[:4]))
        else:
            out.append(obj)
    return out, probs


def load_skins(root: Path = ROOT, **kw) -> tuple:
    out, probs = _loop("skins", root, check_skin, **kw)
    return {sk.skin_id: sk for sk in out}, probs


def load_freeform(root: Path = ROOT, **kw) -> tuple:
    out, probs = _loop("freeform", root, check_freeform, **kw)
    return {sk.skin_id: sk for sk in out}, probs


def load_attacks(root: Path = ROOT, **kw) -> tuple:
    out, probs = _loop("attacks", root, check_attack, **kw)
    return {sk.skin_id: sk for sk in out}, probs


def load_wordings(root: Path = ROOT) -> tuple:
    return _loop("wordings", root, check_wording)


def lexicon_registry(wordings: list):
    """A T25 LexiconRegistry holding the loaded Haiku wordings (source haiku, pending until G-LEX admits them 2/2)."""
    from c2_kit.lexicon import LexiconRegistry, question_sem
    reg = LexiconRegistry(FAMILY)
    for qf, meaning in FX.QUESTION_MEANINGS.items():
        reg.declare(question_sem(FAMILY, qf), "question", meaning)
    for q, text, decl, tid, psha in wordings:
        try:
            reg.add(text, question_sem(FAMILY, q), slots=dict(decl), family=FAMILY, source="haiku",
                    haiku_task_id=tid, haiku_prompt_sha=psha)
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
        for name, (b, _plan) in build_batches().items():
            print(f"{name:10s} {b.kind:16s} {b.batch_id}  items {len(b.key):4d}  chunks {len(b.chunks)}")
        return 0
    tasks = write_tasks()
    print(json.dumps({"n_tasks": len(tasks), "by_kind": {k: sum(1 for t in tasks if t["kind"] == k)
                                                         for k in sorted({t["kind"] for t in tasks})}}))
    return 0


if __name__ == "__main__":
    sys.exit(main())
