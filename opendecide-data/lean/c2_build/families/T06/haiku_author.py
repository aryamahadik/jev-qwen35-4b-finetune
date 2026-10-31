"""families/T06/haiku_author.py: the T06 Haiku AUTHORING tasks (G0_SPEC.md section 4) and the loaders that turn their
answers into pool candidates. Written after A38; Haiku never sees a row, a card, a question, an option or a gold:
authors get meaning briefs only (G0 H39).

  build_batches()       {name: (TaskBatch, plan)}: gold-free chunks via c2_kit.chunker.make_batch. Pack, skin, Mode F
                        and attack batches forbid T06Plugin.LABEL_WORDS and every fixture question text; notice and
                        wording batches forbid the fixture question texts (their meaning words are their content)
  write_tasks()         writes prompts / chunks / key / manifest (TaskBatch.files) + plan/<batch>.json (orchestrator
                        side) + one self-contained task file per chunk (tasks/<task_id>.md, naming its exact answer
                        file) + TASKS.json, all through paths.write_files under haiku/author/ (refuses before A38)
  load_answers_for()    chunker.load_answers for one batch from answers/<task_id>.json
  load_packs / load_skins / load_freeform / load_attacks / load_wordings / load_notices
                        answer objects -> pool candidates + per-item problems (T06 shape checks, G-SL lint, the G0 fact
                        word lists, negcount exactness for wordings, lexicon unit tests for notices). G-LEX admission,
                        G3-H and G13 run in the later stages.
  lexicon_registry()    a T06 LexiconRegistry holding loaded notice forms and wordings (pending until G-LEX), with the
                        G0 S9 / section 4 decoy meanings declared so a form read as a decoy is rejected

Task files: a Haiku agent reads ONLY its task file and writes ONLY the answer file it names; audit with
audit.audit_jsonl(transcript, allowed_read={task file}, allowed_write={answer file}) (TASKS.json lists both).

Run (from lean/):  ../.venv/bin/python c2_build/families/T06/haiku_author.py write      (or: plan, to print counts)
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
from families.T06 import fixtures as FX  # noqa: E402  (only the fixture question texts, to forbid them)
from families.T06 import plugin as P  # noqa: E402
import negcount  # noqa: E402  (c_src/common, put on sys.path by c2_kit.paths)

FAMILY = "T06"
ROOT = HERE / "haiku" / "author"
SEED = "t06-author-v1"
LABEL_WORDS = tuple(P.T06Plugin.LABEL_WORDS)
QSTRINGS = tuple(t for _, _, t in FX.WORDINGS + FX.HELD_WORDINGS)
FORBID_ALL = LABEL_WORDS + QSTRINGS
NARR = {"CUSTOMER": "name", "ITEM": "name", "STORE": "name"}

TRAIN_REGISTERS = ("chat", "email", "ticket", "memo", "receipt", "json", "yaml", "form")
HELD_REGISTERS = ("transcript", "letter")                       # P.T06Plugin.HELD_OUT_REGISTERS
N_SKIN_TRAIN, N_SKIN_HELD = 38, 24                             # 304 + 48 = 352 asked (G0: >= 250 admitted)
FREEFORM_TRAIN, FREEFORM_HELD = ("chat", "email", "ticket", "memo"), ("transcript", "letter")
N_FREE_TRAIN, N_FREE_HELD = 50, 20                             # 200 + 40 = 240 asked (Mode F <= 25% of rows)
N_PACKS, N_PACKS_HELD = 44, 8
N_ATTACK, N_ATTACK_HELD = 60, 12
N_NOTICE = {"deontic": 12, "window": 16}                       # per sem (G0: >= 6 admitted per sem)
# (train, held out) wordings per question form (G0 section 4 item 5: each admitted wording <= 2% of the family's rows)
WORDING_PLAN = {"ch_rule": (30, 5), "ch_end_reject": (8, 3), "ch_end_withdraw": (8, 3), "yn_refund": (12, 3),
                "yn_owed": (10, 3), "yn_double": (8, 3), "yn_not_refund": (10, 3), "yn_may_refuse": (12, 3),
                "yn_no_right": (8, 3)}
NEG_EXACT = {"yn_refund": (0, 0), "yn_owed": (0, 0), "yn_may_refuse": (0, 0), "yn_not_refund": (1, 1),
             "yn_no_right": (1, 1), "yn_double": (2, 2)}                         # (k_all, k_syn), G0 S11
BLOCK_HEADS = ("Order record", "Message added to the case")
SAMPLE = {"CUSTOMER": "Dana Okafor", "ITEM": "electric toothbrush", "STORE": "Brightwell Home"}
SAMPLE2 = {"CUSTOMER": "Jonah Pryce", "ITEM": "desk lamp", "STORE": "Fernway Market"}

# ------------------------------------------------------------------------------------------------ word lists (G0 S4)
# T06 fact words a message, attack line or Mode F text must never hold (G-SL covers numbers, dates, time, quantity,
# quantifier, modal, hedge, status, operator, negation and the label words).
FACT_WORDS = {
    "reason / condition": r"wrong|damaged?|damages|cracked|scratched|torn|dented|leak\w*|working|works|stopped|issues?|"
                          r"problems?|quality|mistakes?|changed|mind|fit|fits|size|colou?r|unwanted|disappoint\w*|"
                          r"repair\w*|replace\w*|warranty|guarantee",
    "delivery / parcel": r"deliver\w*|arriv\w*|came|received?|receiving|parcels?|packages?|lockers?|neighbou?rs?|"
                         r"couriers?|shipp\w*|shipment|collect\w*|picked|pickup|doorstep|postman|dispatch\w*",
    "seal / packaging": r"seals?|sealed|unsealed|wrapp\w*|boxe?s?|boxed|packaging|unopened|tags?|untouched|unused",
    "period / time": r"days?|weeks?|months?|years?|periods?|windows?|deadlines?|hours?|time|timely|expir\w*|"
                     r"delay\w*|quick\w*|fast|slow",
    "rules / money": r"rights?|rules?|polic(?:y|ies)|terms|laws?|legal\w*|statut\w*|notices?|signs?|money|cash|paid|"
                     r"reimburs\w*|credit|vouchers?|exchange\w*|compensat\w*|due|deserv\w*|qualif\w*|"
                     r"warrant\w*|promis\w*|owing|claims?",
}
FACT_RE = {cat: re.compile(r"\b(?:" + rx + r")\b", re.I) for cat, rx in FACT_WORDS.items()}
ONLINE_RE = re.compile(r"\b(?:online|website|web site|web shop|webshop|web form|app|site|internet)\b", re.I)
OVERRIDE_RE = re.compile(r"\b(?:ignore|disregard|override|instructions?|prompt|system|assistant|model|ai)\b", re.I)


def fact_hits(text: str, skip: tuple = ()) -> list:
    """[(category, word)] of T06 fact words in `text` (categories in `skip` are allowed)."""
    return [(cat, m.group()) for cat, rx in FACT_RE.items() if cat not in skip for m in rx.finditer(text)]


# ------------------------------------------------------------------------------------------------ prompts
# The chunker refuses any authoring prompt that holds a label word or a fixture question: label words are described,
# never printed (G0 section 4 item 1); G-SL drops any piece that uses one.
COMMON_BANS = """Hard word rules (a program rejects any text that breaks one):
1. No digits, number words or ordinals (one, two, first, second, half, single, double, twice, pair, couple), no dates, \
times, months or weekdays, no currency or percent signs, no e-mail or web addresses, no domain names, no codes that \
mix letters and digits.
2. No time words: today, tonight, tomorrow, yesterday, now, soon, later, earlier, recently, currently, already, yet, \
next, last, past, ago, day, week, month, weekend, morning, evening, night, daily, immediately, quick, quickly, time, \
period, window, deadline.
3. Nothing about why the item goes back and nothing about its condition: no words such as wrong, damaged, cracked, \
scratched, torn, working, stopped, issue, problem, quality, mistake, changed, mind, fit, size, colour, unwanted, \
repair, replace, warranty, guarantee.
4. Nothing about delivery or the parcel: no words such as delivered, delivery, arrived, came, received, parcel, \
package, locker, neighbour, courier, shipping, collected, picked up, doorstep, dispatch.
5. Nothing about packaging or seals: no words such as seal, sealed, wrapper, wrapping, box, packaging, opened, \
unopened, tag, unused.
6. Nothing about money, rights or rules: no words about money coming back, paying, cash, vouchers, credit notes, \
exchanges, compensation, what anyone is due or deserves, rights, rules, policies, terms, laws, notices or signs, \
promises or claims. Never say whether the return will work out, and never speak about lateness or timeliness.
7. No quantity or quantifier words: all, every, each, some, any, none, both, either, neither, only, always, never, \
often, usually, several, few, many, much, more, most, less, least, another, extra, whole, entire, total.
8. No modal words: must, may, might, can, could, should, shall, will, would, need, able, have to, has to, allowed, \
permitted, required, optional (write "I want to send it back", "please help me with the return", "I am writing to \
return ..."). Avoid contractions such as I'd and I'll.
9. No hedges: maybe, perhaps, probably, likely, seems, appears, think, believe, guess, assume, suspect, almost, \
roughly.
10. No status or outcome words: approved, accepted, confirmed, pending, completed, done, processed, open, opened, \
closed, active, valid, settled, ok, okay, cancel, cancelled.
11. No logic words: if, unless, except, otherwise, instead, regardless, provided, excluding.
12. No negation of any kind: not, n't (don't, can't, isn't ...), no, never, nothing, nobody, nowhere, without, \
cannot, lack, fail, hardly.
13. No capital letter except at the start of a sentence, of a line, or right after a colon, and in the placeholders \
or names you are given (write "the help desk", never "the Help Desk"; no acronyms; "I" is fine)."""

SKIN_PROMPT = """You write short customer messages for a puzzle set about online shopping. A program fills in the \
facts later; you never see the puzzle, its question or its outcome. Each item gives a register (the kind of text), \
a tone and a hint. Write ONE message per item.

Every message uses exactly three placeholders, each exactly once, written exactly like this: {CUSTOMER} (the \
customer's full name), {STORE} (the online store's name) and the item they bought: write {a|ITEM} where the item \
needs "a" or "an" in front of it (the program picks the right one), or {ITEM} where no article goes in front of it \
(after "the" or "my", or as a field value). Never write "a" or "an" yourself right before a placeholder. Write no \
other placeholder and no other name.

The message only says that the customer wants to send the item back to the store, and that they bought it online \
(on the website, in the app or in the online shop). It says nothing else about the case.

Layout: one block of text with no blank line (single line breaks are fine where the register uses them); at most \
about sixty words. Never start with "Order record" or "Message added to the case", and never list order facts.

""" + COMMON_BANS + """

Answer: a JSON list with one object per item: {"qid": "<the item's qid>", "text": "<the message>"}. Use \\n for line \
breaks inside the text. Every message must differ from every other message you write."""

FREEFORM_PROMPT = """You write short customer messages for a puzzle set about online shopping. Each item gives a \
register, a tone and three facts: CUSTOMER (the customer's full name), ITEM (what they bought) and STORE (the online \
store). Write ONE message per item, in which the customer says they want to send the item back to the store and that \
they bought it online (on the website, in the app or in the online shop). Nothing else about the case.

Fact rules:
A. Write the CUSTOMER, ITEM and STORE values exactly as given (same spelling, same capitals), each at least once. \
Write "the" or "my" right before the item, never "a" or "an". Never describe the item or say what kind of goods it is.
B. No other person's name, company name, brand or product name.
C. One block of text with no blank line (single line breaks are fine where the register uses them); at most about \
seventy words.

""" + COMMON_BANS + """

Answer: a JSON list with one object per item: {"qid": "<the item's qid>", "text": "<the message>"}. Use \\n for line \
breaks inside the text. Every message must differ from every other message you write."""

PACK_PROMPT = """You invent "packs": the made-up setting of one invented online store. A program later builds \
practice puzzles about shopping from your packs; you never see the puzzles. Each item gives a brief (the kind of \
store). Write ONE pack per item.

A pack is a JSON object with exactly these keys:
- "store": the store's name: 2 or 3 words, each starting with a capital letter, letters only (no digits, "&", \
apostrophe or hyphen), an invented name that is not a real company, brand or website, for example "Brightwell Home".
- "goods": an object with exactly these four keys, each a list of different item names the store sells:
  - "standard": 5 ordinary manufactured items (for example "desk lamp", "rain jacket", "board game");
  - "custom": 3 items made to the buyer's own specification: engraved, monogrammed, printed with a chosen name or \
photo, or made to measure (for example "engraved watch", "pair of made-to-measure curtains");
  - "perishable": 3 food or flower items that spoil within days (for example "box of pastries", "fresh flower \
bouquet", "cheese hamper");
  - "hygiene": 3 items sold in a protective hygiene seal (for example "electric toothbrush", "face serum", \
"swimsuit", "wireless earbud set").
  Item names: lower case, 1-5 words, letters, spaces and hyphens only; a plain noun phrase that reads right after "a" \
or "an" and after "the" (write "pair of hiking boots" or "set of mixing bowls", never a bare plural); no brand, no \
digits, no quantity or size words, no colour, and no word about the item's condition or quality.
- "customers": 6 invented customer names, each "First Last" (two capitalised words, letters only), from varied \
backgrounds; no famous people.
- "jurisdiction": the name of an invented country or region: one capitalised word of 5-10 letters, letters only, not \
a real place (for example "Valdoria").

The store's goods fit its brief. No name or item contains the words not, no, none, never or nothing. Never use \
words about an item being damaged, worn, used or spoiled. Every store, item, customer and jurisdiction must differ \
from every other one you write.

Answer: a JSON list with one object per item: {"qid": "<the item's qid>", "pack": {...}}. Valid JSON only."""

ATTACK_PROMPT = """You write single lines of pressure or hearsay. A program adds each line to a customer-service case \
file as "Message added to the case: <your line>", to test whether a reader sticks to the written facts. Each item \
gives a kind of pressure. Write ONE line per item.

Rules:
1. Exactly one line, 8-25 words, plain English, no line break; start with a lower-case word or with the placeholder.
2. If the item's slots include STORE, write the placeholder {STORE} exactly once (the store's name, for example "a \
support worker at {STORE} says ..."); otherwise write no placeholder and no name.
3. Hearsay or pressure only: who says, urges or feels what, about shops or returns in general. Never state a fact \
about this case: nothing about the item, its condition, the reason for the return, any date or time span, delivery, \
packaging, the order, or what the store's sign says. Never report a promise by the store or its staff.
4. No digits, number words, dates, times, months, weekdays, currency or percent signs.
5. No words about money coming back, what anyone is due or deserves, or the item's condition (working, damaged ...).
6. Never address the reader, never give instructions, and never use words such as ignore, disregard, override, \
system, prompt or assistant.

Answer: a JSON list with one object per item: {"qid": "<the item's qid>", "text": "<the line>"}. Every line must \
differ from every other line you write."""

NOTICE_PROMPT = """You write short store notices: the returns sign a made-up online store shows at its checkout and \
on its website. A program prints each notice inside quotation marks. Each item gives the exact meaning; write ONE \
notice per item with exactly that meaning, in your own words, like a real shop sign.

Rules (a program rejects any notice that breaks one):
1. One or two short sentences, 4-30 words, no line break, no quotation marks, no braces except the placeholder.
2. If the item's slots include P, write the placeholder {P} exactly once, written exactly like that. The program \
replaces it with a number of days such as "14 days" or "fourteen days", so never write "day" or "days" right after \
{P} (write "within {P} of ..."). Write no other number, digit, number word, date, weekday or month.
3. Say exactly what the meaning says and nothing more: no condition (receipt, tags, unused, original packaging, proof \
of purchase), no exception, no type of goods unless the meaning names one, no store credit, voucher or exchange \
unless the meaning says so, no store name, no hedge.
4. Where the meaning promises money back, say "full refund", "refund in full" or "refunded in full" explicitly.
5. Where the meaning counts from the purchase, start the count with the word purchase, order, ordered or bought (for \
example "of the purchase date", "from the day you ordered"); where it counts from delivery, use delivery or delivered. \
Never use receive, arrival, collect or get for the start.
6. Every notice must differ from every other notice you write and from the example in the item.

Answer: a JSON list with one object per item: {"qid": "<the item's qid>", "text": "<the notice>"}."""

WORDING_PROMPT = """You write questions for a reading test about online shopping. Every test item shows one returns \
case: a consumer law's rules for returns, the store's posted returns notice, an order record and a customer message. \
The reader answers a question about the case. You see none of the test items. Each item below gives the exact \
meaning a question must have and its construction rules. Write ONE question per item with exactly that meaning.

General rules:
1. One sentence ending with "?", 8-30 words, plain English. Refer to "the customer" and "the store"; no names.
2. No digits, number words or ordinals, no dates, no time words (now, today, yet, already, still, soon, later, last, \
next ...), no hedges (maybe, probably ...), no capital letter except the first letter.
3. Every yes/no question says "full refund" (or "refund in full"); money back that is not a full refund never counts.
4. In yes/no questions never narrow the question to the law: never write "these rules", "the rules", "the law", \
"legally", "lawfully", "by law", "the statute" or "the act". Use "here", "in this case", "on these facts", "for this \
return", or nothing.
5. Follow the item's negation rule exactly. Negation words are: not, n't, no, none, nobody, nothing, nowhere, never, \
neither, nor, cannot, without, "it is not the case that", lack, fail to, unless, except, other than. ("Refuse", \
"decline" and "turn down" are not negation words, but never write "refuse to", "decline to" or "fail to".)
6. Ask about the case; never ask whether some answer is correct, and never mention options by letter.
7. Follow the item's style hint for the opening.

Answer: a JSON list with one object per item: {"qid": "<the item's qid>", "text": "<the question>"}. Every \
question must differ from every other question you write."""

ANSWER_FORMAT = {
    "author_pack": '[{"qid": "q...", "pack": {"store": "...", "goods": {"standard": [5 names], "custom": [3], '
                   '"perishable": [3], "hygiene": [3]}, "customers": [6 names], "jurisdiction": "..."}}, ...]',
    "author_skin": '[{"qid": "q...", "text": "..."}, ...]',
    "author_freeform": '[{"qid": "q...", "text": "..."}, ...]',
    "author_wording": '[{"qid": "q...", "text": "...?"}, ...]',
    "author_lexicon": '[{"qid": "q...", "text": "..."}, ...]',
}

# ------------------------------------------------------------------------------------------------ item content
THEMES = ("a home and gift store", "a department store", "a kitchen and pantry store", "a party and celebration store",
          "a beauty and wellness store", "a baby and nursery store", "a sports and outdoor store", "a garden centre",
          "a bakery with a homeware corner", "a travel goods store", "a student essentials store",
          "a health and pharmacy-style store", "a seaside holiday store", "an art and craft store", "a camping store",
          "a jewellery and gift store", "a pet and home store", "a tea and kitchen store", "a farm shop",
          "a festival goods store", "an audio and gadget store with a snack bar", "a stationery and gift store",
          "a bath and home linen store", "a fitness and nutrition store", "a wedding gift store",
          "a florist with a gift corner", "a cheese and deli store with gifts", "a hiking and trail store",
          "a swimwear and beach store", "a hair and grooming store", "a cookware and chocolate store",
          "a children's toys and treats store", "a picnic and outdoor dining store", "a men's grooming and gift store",
          "a holiday market store", "a cosy home and candle store", "a cycling store with a cafe counter",
          "a music lovers' gift store", "a mountain lodge store", "a city convenience store",
          "a college town store", "a lakeside resort store", "a vintage-style home store", "a family general store")
TONES = ("polite and brief", "friendly and chatty", "formal", "short and to the point", "slightly impatient",
         "apologetic", "cheerful", "businesslike")
HINTS = ("asks how to send the item back", "asks for a return label", "asks where to send the item",
         "simply states the wish to send the item back", "thanks the store and asks for help with the return",
         "asks the store to start the return", "says they bought it online and want to return it")
REGISTER_RULES = {
    "chat": ["A chat message from the customer, or a chat excerpt of 2-3 lines 'speaker: message' where the customer "
             "line starts with '{CUSTOMER}:' and any other speaker is written 'support:' (lower case)."],
    "email": ["A short e-mail on single lines (no blank line): a greeting line to the {STORE} team, 1-3 sentences, a "
              "sign-off word line and {CUSTOMER} on the last line."],
    "ticket": ["A support ticket: 2-4 lines in 'field: value' style (for example a subject line, a 'from' line and a "
               "'store' line) and at most one short sentence."],
    "memo": ["An internal note of 1-3 sentences written by a member of the store's service desk about {CUSTOMER}'s "
             "message (it may open with a label such as 'Service desk note:')."],
    "receipt": ["A short receipt-style block from {STORE}: 3-5 lines 'Label: value' naming the store, the customer "
                "and the item (use {ITEM} with no article as a value), plus one line saying the customer wants to send "
                "it back. No prices, amounts or order numbers."],
    "json": ['One JSON object with 3-5 keys whose values are strings or a bare placeholder, for example {"customer": '
             '{CUSTOMER}, "shop": {STORE}, "item": {ITEM}, "channel": "website", "topic": "return"}. Write the '
             'placeholders bare as values (no quotes around them) and use {ITEM}, never {a|ITEM}.',
             "Context keys only (customer, shop, item, channel, topic, request, note); never a key about dates, a "
             "reason, the condition, delivery, packaging, a policy or a status."],
    "yaml": ["3-5 lines of block-style 'key: value' YAML with lower-case keys and plain values, for example "
             "'customer: {CUSTOMER}'. Write the placeholders bare as values and use {ITEM}, never {a|ITEM}.",
             "Context keys only (customer, shop, item, channel, topic, request, note); never a key about dates, a "
             "reason, the condition, delivery, packaging, a policy or a status."],
    "form": ["A filled web form: a title line and 3-4 'Label: value' lines (for example name, shop, product, "
             "request); use {ITEM} with no article as a value."],
    "transcript": ["A phone-call transcript of 2-4 lines 'Agent: ...' / 'Caller: ...'; the caller gives the name "
                   "{CUSTOMER} once; the agent speaks for {STORE}."],
    "letter": ["A short formal letter on single lines (no blank line): 'Dear {STORE},' as the first line, 1-2 "
               "sentences, a closing line such as 'Kind regards,' and {CUSTOMER} on the last line."],
}
REGISTER_DESC = {"chat": "a chat message", "email": "a short e-mail", "ticket": "a support ticket",
                 "memo": "a service-desk note", "receipt": "a receipt-style block", "json": "a JSON contact record",
                 "yaml": "a YAML contact record", "form": "a filled web form", "transcript": "a phone-call transcript",
                 "letter": "a short formal letter"}
FREEFORM_RULES = {
    "chat": ["A chat message thread of 1-3 short lines 'speaker: message'; the customer speaks under the CUSTOMER "
             "name; any other speaker is 'support'."],
    "email": ["A short e-mail on single lines: a greeting line, 1-3 sentences and a sign-off line with the CUSTOMER "
              "name."],
    "ticket": ["A support ticket: 2-3 short 'field: value' lines and 1-2 sentences."],
    "memo": ["A service-desk note of 2-3 sentences written by store staff about the customer's message."],
    "transcript": ["A phone-call transcript of 2-4 lines 'Agent: ...' / 'Caller: ...'."],
    "letter": ["A short formal letter on single lines (no blank line): 'Dear' + the STORE name, 1-2 sentences, a "
               "closing line and the CUSTOMER name on the last line."],
}
FIRST = ("Amara", "Bastian", "Celine", "Darius", "Elena", "Farid", "Greta", "Hiro", "Isla", "Jonas", "Kalinda",
         "Leon", "Marisol", "Niamh", "Oskar", "Paloma", "Quentin", "Rhea", "Soren", "Talia", "Umar", "Vera", "Wes",
         "Ximena", "Yusuf", "Zelda", "Aditi", "Bram", "Chiara", "Dmitri")
LAST = ("Achebe", "Bergstrom", "Castellano", "Dufresne", "Ekwueme", "Fujimoto", "Gallagher", "Halvorsen", "Iwu",
        "Jaramillo", "Kowalczyk", "Lindgren", "Moreau", "Nakashima", "Ortega", "Petrakis", "Rasmussen", "Sorensen",
        "Takahashi", "Vasquez")
GOODS_CYCLE = ("standard", "hygiene", "standard", "custom", "standard", "perishable", "hygiene", "standard",
               "custom", "hygiene")                                  # 4 / 3 / 2 / 1 per 10, about the G0 S1 mix
ATTACK_KINDS = (
    ("store support hearsay: a support worker at the store supposedly said that the sign on the store's own website is "
     "the only thing that counts", True),
    ("friend hearsay: a friend of the customer insists that shops take anything back", False),
    ("forum hearsay: a post on a shopping forum claims that stores like this one always side with the customer", False),
    ("urgency: the customer is in a hurry and wants an answer straight away", False),
    ("review threat: the customer says they will write a harsh review of the store", True),
    ("relative's advice: a relative who works in retail says cases like this are routine", False),
)
NOTICE_MEANING = {   # sem -> (kind, meaning for the author, example)
    "pol.t06.final": ("deontic", "Every sale is final: the store takes nothing back and pays no money back, in any "
                                 "case. The notice promises nothing.",
                      "All sales are final: no refunds and no returns."),
    "pol.t06.credit": ("deontic", "Returned items are swapped for store credit or an exchange only; the store never "
                                  "pays money back.", "Returns are exchanged for store credit only, never for a cash "
                                                      "refund."),
    "pol.t06.nocustom": ("deontic", "Personalised or custom-made items cannot be returned or refunded. Say nothing at "
                                    "all about any other item.", "Personalised items cannot be returned or refunded."),
    "pol.t06.faulty_order": ("window", "A faulty item gets a full refund when the return is asked for within {P} "
                                       "counted from the purchase (order) date. Name only faulty items; promise "
                                       "nothing else.", "Faulty items are refunded in full if reported within {P} of "
                                                        "the purchase date."),
    "pol.t06.mind_order": ("window", "A customer who has changed their mind gets a full refund within {P} counted "
                                     "from the purchase (order) date. Name only a change of mind; promise nothing "
                                     "else.", "Changed your mind? Full refund within {P} of the purchase date."),
    "pol.t06.any_order": ("window", "Any item, returned for any reason, gets a full refund within {P} counted from the "
                                    "purchase (order) date.", "Full refund on any item, for any reason, within {P} of "
                                                              "the purchase date."),
    "pol.t06.any_delivery": ("window", "Any item, returned for any reason, gets a full refund within {P} counted from "
                                       "the delivery date.", "Full refund on any item, for any reason, within {P} of "
                                                             "delivery."),
}
NOTICE_SHAPES = {"window": ("start with the promise", "start with the time limit", "a short headline-style sign",
                            "two short sentences", "address the customer as 'you'",
                            "write it in the store's voice ('we')"),
                 "deontic": ("a short headline-style sign", "two short sentences", "address the customer as 'you'",
                             "write it in the store's voice ('we')", "one plain sentence", "start with the items it "
                                                                                          "covers")}
WORDING_BRIEF = {
    "yn_refund": ("A yes/no question asked from the customer's side: does the customer have a right to a full refund "
                  "in this case? (yes when a full refund is due)",
                  "Use NO negation word. Make the customer the subject (for example is entitled to, has a right to, "
                  "can get, qualifies for)."),
    "yn_owed": ("A yes/no question asked from the store's side: does the store have to give the customer a full "
                "refund in this case? (yes when a full refund is due)",
                "Use NO negation word. Make the store the subject (for example owes, has to give, is bound to give)."),
    "yn_double": ("A yes/no question with exactly two negations that asks whether it is false that the customer has "
                  "no right to a full refund (yes when a full refund is due).",
                  "Use exactly TWO negations: 'is it not the case that' (or 'it is not the case that') plus 'no' or "
                  "'not' once more; no other negation word."),
    "yn_not_refund": ("A yes/no question that is the exact opposite of asking whether the customer is entitled to a "
                      "full refund: yes when the customer is NOT entitled to a full refund in this case.",
                      "Use exactly ONE negation: 'not' or n't on the verb (for example 'is the customer not entitled "
                      "to', 'is it true that the customer does not have a right to'); never 'no', 'cannot' or any "
                      "other negation word. Make the customer the subject."),
    "yn_no_right": ("A yes/no question: is it true that the customer has no right to a full refund, or that no full "
                    "refund is due, in this case? (yes when no full refund is due)",
                    "Use exactly ONE negation: the word 'no' in front of a noun ('no right', 'no full refund'); never "
                    "'not', n't or any other negation word."),
    "yn_may_refuse": ("A yes/no question from the store's side: may the store refuse (turn down, decline) the "
                      "customer a full refund in this case? (yes when no full refund is due)",
                      "Use NO negation word. Use refuse, decline or turn down with a noun ('refuse the customer a "
                      "full refund', 'turn down a full refund'), never 'refuse to' or 'decline to'. Never start the "
                      "question with 'May' (a program reads a capital May as the month): write 'In this case, may "
                      "the store ...', 'Can the store ...' or 'Is the store free to ...'."),
    "ch_rule": ("A multiple-choice question: which of the listed rules gives the customer a full refund, if any? (The "
                "options, shown separately, are the law's rules for returns, the store's posted notice and 'none of "
                "them'.)", "Allow for 'none': include 'if any' or a similar phrase. No other negation is needed."),
    "ch_end_reject": ("A multiple-choice question whose options are dates: on which date does the period of the "
                      "customer's legal right to reject faulty goods end (its final day)?",
                      "Name that legal right (the right the law gives to reject faulty goods) and say 'legal' or "
                      "'law'; never mention the store's notice or promise, and never say from which date the period "
                      "is counted. Say 'end', 'run out' or 'final day', never 'last'. No negation."),
    "ch_end_withdraw": ("A multiple-choice question whose options are dates: on which date does the period of the "
                        "customer's legal right to withdraw from (cancel) the purchase for any reason end (its final "
                        "day)?",
                        "Name that legal right (the right the law gives to withdraw or cancel for any reason) and say "
                        "'legal' or 'law'; never mention the store's notice or promise, and never say from which date "
                        "the period is counted. Say 'end', 'run out' or 'final day', never 'last'. No negation."),
}
STYLE_TRAIN = ("a plain question with no opening phrase", "open with 'In this case,'", "open with 'On these facts,'",
               "a plain question that ends with 'here?'", "a plain question that ends with 'in this case?'",
               "open with 'For this return,'", "a plain question that names 'this order' in the middle")
STYLE_HELD = ("open with 'Looking at this order,'", "open with 'Taking the facts as given,'",
              "a plain question that ends with 'for this order?'", "open with 'On the case as written,'")
# Extraction meanings (G-LEX lists) incl. never-generated decoys (G0 S9, section 4 item 5): a form read as a decoy is
# rejected. Same kinds as the plugin's sems; the plugin itself only uses the sem ids.
LEX_MEANINGS = {
    "pol.t06.final": ("deontic", "the store refuses every return and every refund: all sales are final"),
    "pol.t06.credit": ("deontic", "the store takes returns only for store credit or an exchange and never pays money "
                                  "back"),
    "pol.t06.nocustom": ("deontic", "the store refuses returns and refunds of personalised or custom-made items and "
                                    "says nothing about other items"),
    "pol.t06.x_some": ("deontic", "the store promises a full refund on some returns"),
    "pol.t06.faulty_order": ("window", "the store promises a full refund for faulty items asked for within the stated "
                                       "days of the purchase (order) date"),
    "pol.t06.mind_order": ("window", "the store promises a full refund to a customer who changed their mind, within "
                                     "the stated days of the purchase (order) date"),
    "pol.t06.any_order": ("window", "the store promises a full refund for any reason within the stated days of the "
                                    "purchase (order) date"),
    "pol.t06.any_delivery": ("window", "the store promises a full refund for any reason within the stated days of the "
                                       "delivery date"),
    "pol.t06.x_credit": ("window", "the store gives store credit or an exchange, not money back, for returns within "
                                   "the stated days"),
    "pol.t06.x_unstated": ("window", "the store accepts returns within the stated days but does not say what the "
                                     "customer gets back"),
    "pol.t06.x_received": ("window", "the store promises a full refund within the stated days of the day the "
                                     "customer received or collected the goods"),
}
QUESTION_MEANINGS = {
    "yn_refund": "asks, with the customer as the subject and no negation, whether the customer has a right to a full "
                 "refund (yes = a full refund is due)",
    "yn_owed": "asks, with the store as the subject and no negation, whether the store has to give the customer a full "
               "refund (yes = a full refund is due)",
    "yn_double": "asks, using two negations, whether it is false that the customer has no right to a full refund "
                 "(yes = a full refund is due)",
    "yn_not_refund": "asks, with 'not' or n't on the verb, whether the customer is not entitled to a full refund "
                     "(yes = no full refund is due)",
    "yn_no_right": "asks, with 'no' in front of a noun, whether the customer has no right to a full refund or no full "
                   "refund is due (yes = no full refund is due)",
    "yn_may_refuse": "asks, with no negation word, whether the store may refuse or turn down a full refund (yes = no "
                     "full refund is due)",
    "ch_rule": "asks which listed rule, if any, gives the customer a full refund",
    "ch_end_reject": "asks on which date the period of the customer's legal right to reject faulty goods ends",
    "ch_end_withdraw": "asks on which date the period of the customer's legal right to withdraw from or cancel the "
                       "purchase ends",
}
QUESTION_DECOYS = {
    "q.t06.x_notice_end": "asks on which date the period of the store's own notice or promise ends",
    "q.t06.x_any_remedy": "asks whether the customer gets any money back, store credit or an exchange",
}


# ------------------------------------------------------------------------------------------------ batches
def _pack_items():
    items, plan = [], {}
    for i, theme in enumerate(THEMES[:N_PACKS]):
        iid = f"t06a.pack.{i:03d}"
        items.append((iid, {"brief": f"An invented online store: {theme}. Its range includes all four kinds of goods "
                                     f"the pack asks for."}))
        plan[iid] = {"role": "pack", "held_out": i % 5 == 4 and i < 5 * N_PACKS_HELD}      # 8 of 44
    return items, plan


def _skin_items():
    items, plan = [], {}
    regs = [(r, N_SKIN_TRAIN, False) for r in TRAIN_REGISTERS] + [(r, N_SKIN_HELD, True) for r in HELD_REGISTERS]
    for ri, (reg, n, held) in enumerate(regs):
        for i in range(n):
            tone = TONES[(i + 3 * ri) % len(TONES)]
            hint = HINTS[(i * 3 + ri) % len(HINTS)]
            iid = f"t06a.skin.{reg}.{i:03d}"
            items.append((iid, {"brief": f"Write {REGISTER_DESC[reg]}. Tone: {tone}. Hint: the customer {hint}.",
                                "register": reg, "slots": dict(NARR), "rules": REGISTER_RULES[reg]}))
            plan[iid] = {"role": "skin", "register": reg, "tone": tone, "held_out": held,
                         "escape": reg if reg in ("json", "yaml") else "text"}
    return items, plan


def _freeform_facts(i: int) -> tuple:
    goods = GOODS_CYCLE[i % len(GOODS_CYCLE)]
    pool = P.ITEMS[goods]
    item = pool[(i * 7 + i // len(GOODS_CYCLE)) % len(pool)]
    store = P.STORES[(i * 5 + i // 12) % len(P.STORES)]
    customer = f"{FIRST[(i * 7) % len(FIRST)]} {LAST[(i * 3 + i // len(FIRST)) % len(LAST)]}"
    return goods, {"CUSTOMER": customer, "ITEM": item, "STORE": store}


def _freeform_items():
    items, plan = [], {}
    regs = [(r, N_FREE_TRAIN, False) for r in FREEFORM_TRAIN] + [(r, N_FREE_HELD, True) for r in FREEFORM_HELD]
    k = 0
    for ri, (reg, n, held) in enumerate(regs):
        for i in range(n):
            goods, facts = _freeform_facts(k)
            k += 1
            tone = TONES[(i * 3 + ri) % len(TONES)]
            iid = f"t06a.free.{reg}.{i:03d}"
            items.append((iid, {"brief": f"Write {REGISTER_DESC[reg]} in which the customer wants to send the item "
                                         f"back. Tone: {tone}.",
                                "register": reg, "facts": dict(facts), "rules": FREEFORM_RULES[reg]}))
            plan[iid] = {"role": "freeform", "register": reg, "tone": tone, "held_out": held, "facts": facts,
                         "goods": goods}
    return items, plan


def _attack_items():
    items, plan = [], {}
    for i in range(N_ATTACK):
        kind, store_ok = ATTACK_KINDS[i % len(ATTACK_KINDS)]
        use_store = store_ok and (i // len(ATTACK_KINDS)) % 2 == 0
        iid = f"t06a.attack.{i:03d}"
        items.append((iid, {"brief": "Kind of pressure: " + kind + ".", "register": "note",
                            "slots": {"STORE": "name"} if use_store else {},
                            "rules": ["Use {STORE} exactly once." if use_store
                                      else "Use no placeholder and no name."]}))
        plan[iid] = {"role": "attack", "held_out": i >= N_ATTACK - N_ATTACK_HELD,
                     "decl": {"STORE": "name"} if use_store else {}}
    return items, plan


def _notice_items():
    items, plan = [], {}
    for sem, (kind, meaning, example) in NOTICE_MEANING.items():
        slots = {"P": "count"} if kind == "window" else {}
        for i in range(N_NOTICE[kind]):
            iid = f"t06a.notice.{sem}.{i:03d}"
            items.append((iid, {"brief": f"Write a returns notice with this meaning. Example of the shape (do not copy "
                                         f"it): \"{example}\"", "meaning": meaning, "slots": slots,
                                "rules": [f"Shape hint: {NOTICE_SHAPES[kind][i % len(NOTICE_SHAPES[kind])]}."]}))
            plan[iid] = {"role": "notice", "kind": kind, "sem": sem, "slots": slots}
    return items, plan


def _wording_items():
    items, plan = [], {}
    for q, (n_train, n_held) in WORDING_PLAN.items():
        meaning, neg_rule = WORDING_BRIEF[q]
        for i in range(n_train + n_held):
            held = i >= n_train
            style = STYLE_HELD[i % len(STYLE_HELD)] if held else STYLE_TRAIN[i % len(STYLE_TRAIN)]
            iid = f"t06a.wording.{q}.{i:03d}"
            items.append((iid, {"brief": meaning, "slots": [], "rules": [neg_rule, f"Style hint: {style}."]}))
            plan[iid] = {"role": "wording", "qform": q, "held_out": held}
    return items, plan


BATCH_SPECS = (
    # name, chunker kind, items fn, prompt, forbid, max items per chunk  (37 tasks in all; G0 section 4)
    ("packs", "author_pack", _pack_items, PACK_PROMPT, FORBID_ALL, 6),
    ("skins", "author_skin", _skin_items, SKIN_PROMPT, FORBID_ALL, 32),
    ("freeform", "author_freeform", _freeform_items, FREEFORM_PROMPT, FORBID_ALL, 30),
    ("attacks", "author_skin", _attack_items, ATTACK_PROMPT, FORBID_ALL, 30),
    ("notices", "author_lexicon", _notice_items, NOTICE_PROMPT, QSTRINGS, 25),
    ("wordings", "author_wording", _wording_items, WORDING_PROMPT, QSTRINGS, 34),
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


def task_list(root: Path = ROOT) -> tuple:
    """([task dicts], {relative path: text}) for every batch, in memory (write_tasks writes them)."""
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
    return tasks, files


def write_tasks(root: Path = ROOT) -> list:
    """Write every batch (guarded writers) and return the task list [{task_file, answer_file, kind, ...}]."""
    tasks, files = task_list(root)
    paths.write_files(root, files)
    index = {"family": FAMILY, "seed": SEED, "n_tasks": len(tasks), "tasks": tasks,
             "g0_sha256": P.T06Plugin.G0_SHA256_AUTHORED, "g0_haiku_task": P.T06Plugin.G0_HAIKU_TASK,
             "loaders": "families/T06/haiku_author.py (load_packs / load_skins / load_freeform / load_attacks / "
                        "load_notices / load_wordings; lexicon_registry declares the G-LEX meanings incl. decoys)"}
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


def _norm(text: str) -> str:
    return " ".join(text.split()).lower()


def _bad_substr(s: str) -> bool:
    return "ohs" in s.lower() or "jev" in s.lower()


def _label_hits(text: str) -> list:
    forms = gsl._label_forms(LABEL_WORDS)
    hits = [w for w in re.findall(r"[A-Za-z]+(?:'[A-Za-z]+)?", text) if w.lower() in forms]
    return hits + [p for p in LABEL_WORDS if " " in p and re.search(r"(?<![a-z])" + re.escape(p) + r"(?![a-z])",
                                                                   text.lower())]


_STORE = re.compile(r"^[A-Z][a-z]+(?: [A-Z][a-z]+){1,2}$")
_ITEM = re.compile(r"^[a-z][a-z-]*(?: [a-z][a-z-]*){0,4}$")
_PERSON = re.compile(r"^[A-Z][a-z]+(?:-[A-Z][a-z]+)? [A-Z][a-z]+(?:-[A-Z][a-z]+)?$")
_JURIS = re.compile(r"^[A-Z][a-z]{4,9}$")
REAL_PLACES = {"france", "spain", "italy", "germany", "wales", "scotland", "ireland", "england", "norway", "sweden",
               "denmark", "finland", "poland", "austria", "greece", "portugal", "canada", "mexico", "brazil", "chile",
               "peru", "japan", "china", "india", "kenya", "ghana", "egypt", "nepal", "bhutan", "texas", "ohio",
               "florida", "bavaria", "tuscany", "provence", "valencia", "andalusia", "brittany", "flanders",
               "holland", "belgium", "croatia", "serbia", "latvia", "estonia", "iceland", "cyprus", "malta",
               "morocco", "tunisia", "jordan", "oman", "qatar", "yemen", "panama", "cuba", "jamaica", "samoa", "tonga"}
GOODS_N = {"standard": 5, "custom": 3, "perishable": 3, "hygiene": 3}


def validate_pack(p) -> list:
    """T06 pack shape (G0 section 4 item 6). Empty list = valid."""
    keys = {"store", "goods", "customers", "jurisdiction"}
    if not isinstance(p, dict) or set(p) != keys:
        return [f"pack keys {sorted(p) if isinstance(p, dict) else type(p).__name__} != {sorted(keys)}"]
    probs = []
    st = p["store"]
    if not (isinstance(st, str) and _STORE.fullmatch(st)):
        probs.append(f"store {st!r}")
    goods = p["goods"]
    items = []
    if not (isinstance(goods, dict) and set(goods) == set(GOODS_N)):
        probs.append("goods: exactly standard / custom / perishable / hygiene")
    else:
        for g, n in GOODS_N.items():
            lst = goods[g]
            if not (isinstance(lst, list) and len(lst) == n and all(isinstance(x, str) and _ITEM.fullmatch(x)
                                                                    for x in lst)):
                probs.append(f"goods {g}: {n} lower-case names")
                continue
            items += lst
        if len(set(items)) != len(items):
            probs.append("an item repeats")
        for it in items:
            if it.split()[0] in ("a", "an", "the", "some", "my") or it.endswith("s") and " of " not in it \
                    and not it.endswith(("ss", "us")):
                probs.append(f"item {it!r}: article or bare plural")
            if fact_hits(it, skip=("delivery / parcel", "seal / packaging", "period / time", "rules / money")) \
                    or _label_hits(it):
                probs.append(f"item {it!r}: condition or label word")
    cust = p["customers"]
    if not (isinstance(cust, list) and len(cust) == 6 and len(set(cust)) == 6
            and all(isinstance(x, str) and _PERSON.fullmatch(x) for x in cust)):
        probs.append(f"customers {cust}")
    j = p["jurisdiction"]
    if not (isinstance(j, str) and _JURIS.fullmatch(j)) or (isinstance(j, str) and j.lower() in REAL_PLACES):
        probs.append(f"jurisdiction {j!r}")
    if probs:
        return probs
    values = [st, j] + items + cust
    for v in values:
        try:
            sl = S.name_slot(v)
        except Exception as e:  # noqa: BLE001
            probs.append(f"{v!r}: {str(e)[:60]}")
            continue
        if gsl.lint_values({"X": sl}):
            probs.append(f"{v!r}: slot value lint")
        if negcount.k_all(v):
            probs.append(f"{v!r}: negation cue")
        if _bad_substr(v):
            probs.append(f"{v!r}: never-open letter sequence")
        if _label_hits(v):
            probs.append(f"{v!r}: label word")
    others = [st, j] + cust                    # values that can share a row with an item (Mode F fill_freeform)
    for a in values:
        for b in (others if a in items else values):
            if a != b and re.search(r"(?<!\w)" + re.escape(a) + r"(?!\w)", b):
                probs.append(f"{a!r} occurs inside {b!r}")
    return probs


def load_packs(root: Path = ROOT) -> tuple:
    b, plan, ans, probs = load_answers_for("packs", root)
    packs, seen = [], set()
    for iid, a in sorted(ans.items()):
        p = a.get("pack") if isinstance(a, dict) else None
        v = validate_pack(p)
        if not v and (p["store"] in seen or p["jurisdiction"] in seen):
            v = ["store or jurisdiction repeats another pack"]
        if v:
            probs.append(f"{iid}: " + "; ".join(v[:4]))
            continue
        seen |= {p["store"], p["jurisdiction"]}
        packs.append({"id": f"t06pk-{iid.rsplit('.', 1)[1]}", "store": p["store"], "items": p["goods"],
                      "customers": p["customers"], "jurisdiction": p["jurisdiction"],
                      "held_out": plan[iid]["held_out"], "haiku_task_id": _task_of(b, iid),
                      "haiku_prompt_sha": b.prompt_sha})
    return packs, probs


def _program_head(text: str) -> bool:
    return (any(chunk.lstrip().startswith(BLOCK_HEADS) for chunk in text.split("\n"))
            or "posted this notice" in text)


def _roundtrip(sk) -> list:
    """Fill with two sample value sets (a / an items) and read back the way solver B does (skin.parse_skin)."""
    for vals in (SAMPLE, SAMPLE2):
        slots = {k: S.name_slot(v) for k, v in vals.items() if k in sk.decl}
        try:
            filled = sk.fill(slots).text
            got = K.parse_skin(sk, filled, {k: ("name", ()) for k in sk.decl})
        except Exception as e:  # noqa: BLE001
            return [f"fill / parse: {str(e)[:100]}"]
        if got != {k: s.value for k, s in slots.items()}:
            return [f"parse_skin read {got}"]
        if sk.escape == "json":
            try:
                if not isinstance(json.loads(filled), dict):
                    return ["JSON skin is not one object"]
            except json.JSONDecodeError as e:
                return [f"JSON skin does not parse ({e})"]
    return []


def check_skin(iid, text, meta, tid, psha, seen) -> tuple:
    """Mode T message skin: make_skin + G-SL lint_template + the G0 fact words + online + one block + round trip."""
    if not isinstance(text, str) or not text.strip():
        return None, ["no text"]
    text = text.strip()
    if _norm(text) in seen:
        return None, ["duplicate text"]
    sid = f"T06-SK-{iid.split('.', 2)[2]}"
    try:
        sk = K.make_skin(sid, FAMILY, text, dict(NARR), register=meta["register"], escape=meta["escape"],
                         held_out=meta["held_out"], haiku_task_id=tid, haiku_prompt_sha=psha)
    except Exception as e:  # noqa: BLE001
        return None, [str(e)[:120]]
    v = [f"G-SL {x.rule}: {x.detail}" for x in gsl.lint_template(
        sk, label_words=LABEL_WORDS, exceptions=P.T06Plugin.GSL_EXCEPTIONS, name_allow=P.T06Plugin.NAME_ALLOW)]
    lit = K.PH_RE.sub(" ", text)
    v += [f"fact word ({c}): {w}" for c, w in fact_hits(lit)]
    if "\n\n" in text:
        v.append("blank line (the state is blocks separated by one blank line)")
    if not ONLINE_RE.search(lit):
        v.append("does not say the order was online")
    if _program_head(text):
        v.append("program block head")
    if len(text) > 420:
        v.append("longer than about sixty words")
    v += _roundtrip(sk)
    if not v:
        seen.add(_norm(text))
    return sk, v


def check_attack(iid, text, meta, tid, psha, seen) -> tuple:
    """Attack line (G0 section 4 item 6): one line, G-SL attack role, no label or fact word, no override phrasing."""
    if not isinstance(text, str) or not text.strip() or "\n" in text.strip():
        return None, ["not one line"]
    text = text.strip()
    sid = f"T06-AT-{iid.rsplit('.', 1)[1]}"
    try:
        sk = K.make_skin(sid, FAMILY, text, dict(meta["decl"]), kind="attack", register="note",
                         held_out=meta["held_out"], haiku_task_id=tid, haiku_prompt_sha=psha)
    except Exception as e:  # noqa: BLE001
        return None, [str(e)[:120]]
    v = [f"G-SL {x.rule}: {x.detail}" for x in gsl.lint_template(sk, label_words=LABEL_WORDS)]
    lit = K.PH_RE.sub(" ", text)
    v += [f"label word {w!r}" for w in _label_hits(lit)]
    v += [f"fact word ({c}): {w}" for c, w in fact_hits(lit, skip=("rules / money", "period / time"))]
    if re.search(r"\b(?:days?|weeks?|months?|years?|hours?|periods?|windows?|deadlines?)\b", lit, re.I):
        v.append("time span word")
    if re.search(r"\b(?:promis\w*|money|paid|pay|credit|voucher|exchange\w*)\b", lit, re.I):
        v.append("store promise or money word")
    if OVERRIDE_RE.search(lit):
        v.append("override or instruction phrasing")
    if not 8 <= len(text.split()) <= 25:
        v.append("8-25 words")
    if _norm(text) in seen:
        v.append("duplicate")
    if _program_head(text) or re.match(r"^\s*[A-Za-z ]{1,20}:", text):
        v.append("carries a label or a program head")
    if not v:
        seen.add(_norm(text))
    return sk, v


def check_freeform(iid, text, meta, tid, psha, seen) -> tuple:
    """Mode F message: G-SL lint_freeform + item 1's rules (the text as a template with the facts as placeholders,
    linted like a Mode T skin) + the G0 fact words + online + no article before ITEM + a fill check."""
    if not isinstance(text, str) or not text.strip():
        return None, ["no text"]
    text = text.strip()
    facts = meta["facts"]
    v = [f"G-SL {x.rule}: {x.detail}" for x in gsl.lint_freeform(text, facts, label_words=LABEL_WORDS)]
    if "{" in text or "}" in text:
        v.append("brace")
    tpl, occ = text, {}
    for name, val in sorted(facts.items(), key=lambda kv: -len(kv[1])):
        occ[name] = len(re.findall(r"(?<!\w)" + re.escape(val) + r"(?!\w)", tpl))
        tpl = re.sub(r"(?<!\w)" + re.escape(val) + r"(?!\w)", "{" + name + "}", tpl)
    if not v:
        try:
            probe = K.make_skin("probe", FAMILY, tpl, dict(NARR),
                                counts={k: (1, max(1, occ[k])) for k in NARR})
            v += [f"item 1 rule {x.rule}: {x.detail}" for x in gsl.lint_template(probe, label_words=LABEL_WORDS)]
        except Exception as e:  # noqa: BLE001
            v.append(str(e)[:120])
    lit = K.PH_RE.sub(" ", tpl)
    v += [f"fact word ({c}): {w}" for c, w in fact_hits(lit)]
    if re.search(r"\b(?:a|an)\s+\{ITEM\}", tpl, re.I):
        v.append("article a / an before ITEM")
    if "\n\n" in text:
        v.append("blank line")
    if not ONLINE_RE.search(lit):
        v.append("does not say the order was online")
    if _program_head(text):
        v.append("program block head")
    if _norm(text) in seen:
        v.append("duplicate")
    sk = None
    if not v:
        try:
            sk = K.make_skin(f"T06-MF-{iid.split('.', 2)[2]}", FAMILY, text, dict(NARR), register=meta["register"],
                             author_mode="F", brief=facts, held_out=meta["held_out"], haiku_task_id=tid,
                             haiku_prompt_sha=psha)
            sk.fill({k: S.name_slot(x) for k, x in SAMPLE.items()})
        except Exception as e:  # noqa: BLE001
            v.append(str(e)[:120])
    if not v:
        seen.add(_norm(text))
    return sk, v


_FULL = re.compile(r"\bfull refund\b|\brefund(?:ed|s)? in full\b", re.I)
_ORDER_W = re.compile(r"\b(?:purchase|purchased|order|ordered|ordering|bought|buy|buying)\b", re.I)
_DELIV_W = re.compile(r"\bdeliver(?:y|ed|ies)?\b", re.I)
_RECV_W = re.compile(r"\b(?:receiv\w*|arriv\w*|collect\w*|pick(?:ed)? up)\b", re.I)
_FAULT_W = re.compile(r"\b(?:faulty|defective|defects?|faults?|damaged|broken|malfunction\w*)\b", re.I)
_MIND_W = re.compile(r"\bchang\w* (?:your|their|of|one's) minds?\b|\bchange of heart\b", re.I)
_ANY_W = re.compile(r"\bany reason\b|\bwhatever the reason\b|\bno reason needed\b|\bno questions asked\b|"
                    r"\bno matter why\b", re.I)
_COND_W = re.compile(r"\b(?:receipts?|unused|unworn|original packaging|tags?|proof|conditions?|unopened|sealed|"
                     r"labels?|except|unless|provided|only if)\b", re.I)
_GOODS_W = re.compile(r"\b(?:personali[sz]ed|custom\w*|bespoke|engraved|made[- ]to[- ](?:order|measure)|"
                      r"perishables?|food|flowers?|hygiene|cosmetics?)\b", re.I)
_CREDIT_W = re.compile(r"\b(?:store credit|credit|vouchers?|exchanges?|exchanged|swap\w*|gift cards?)\b", re.I)


def notice_problems(sem: str, text: str) -> list:
    """G0 S9 / section 4 item 3 shape rules for one notice form (meaning itself: G-LEX extraction)."""
    v = []
    if '"' in text or "“" in text or "”" in text or "\n" in text:
        v.append("quotation mark or line break")
    phs = K.placeholders(text)
    window = sem in P.WINDOWED
    if window:
        if [p.name for p in phs] != ["P"] or text.count("{") != 1:
            v.append("{P} exactly once and no other placeholder")
        if re.search(r"\{P\}\s+days?\b", text, re.I):
            v.append("'day(s)' after {P} (the slot prints its unit)")
    elif phs or "{" in text:
        v.append("a no-promise notice holds no placeholder")
    lit = K.PH_RE.sub(" ", text)
    if re.search(r"\d", lit) or any(w.lower() in gsl.CORE["number"] for w in re.findall(r"[A-Za-z]+", lit)):
        v.append("number outside {P}")
    if any(w in gsl.MONTHS or w in gsl.WEEKDAYS for w in re.findall(r"[A-Za-z]+", lit)):
        v.append("month or weekday")
    if not 4 <= len(text.split()) <= 30:
        v.append("4-30 words")
    if window:
        if not _FULL.search(lit):
            v.append("a promise says full refund / refund(ed) in full")
        if _COND_W.search(lit) or _GOODS_W.search(lit) or _CREDIT_W.search(lit):
            v.append("condition, type of goods or credit in a promise")
        if _RECV_W.search(lit):
            v.append("receive / arrival / collect / get as the start")
        anchor = P.NOTICE_SCOPE[sem][1]
        if anchor == "ordered" and (not _ORDER_W.search(lit) or _DELIV_W.search(lit)):
            v.append("order-dated promise names purchase / order / bought and never delivery")
        if anchor == "delivered" and (not _DELIV_W.search(lit) or _ORDER_W.search(lit)):
            v.append("delivery-dated promise names delivery and never purchase / order")
        reason = P.NOTICE_SCOPE[sem][0]
        if reason == "faulty" and (not _FAULT_W.search(lit) or _ANY_W.search(lit) or _MIND_W.search(lit)):
            v.append("faulty-only promise")
        if reason == "mind" and (not _MIND_W.search(lit) or _ANY_W.search(lit) or _FAULT_W.search(lit)):
            v.append("change-of-mind-only promise")
        if reason == "any" and (_FAULT_W.search(lit) or _MIND_W.search(lit)):
            v.append("any-reason promise names one reason")
    elif sem == "pol.t06.credit" and not _CREDIT_W.search(lit):
        v.append("credit notice names credit or an exchange")
    elif sem == "pol.t06.nocustom" and not _GOODS_W.search(lit):
        v.append("nocustom notice names personalised or custom-made items")
    elif sem == "pol.t06.final" and (_GOODS_W.search(lit) or _CREDIT_W.search(lit)):
        v.append("final notice names a type of goods or credit")
    if not window and _FULL.search(lit) and not negcount.k_all(lit):
        v.append("a no-promise notice states a full refund without negating it")
    return v


def check_notice(iid, text, meta, tid, psha, seen) -> tuple:
    if not isinstance(text, str) or not text.strip():
        return None, ["no text"]
    text = " ".join(text.split())
    v = notice_problems(meta["sem"], text)
    if _norm(text) in seen:
        v.append("duplicate")
    if not v:
        seen.add(_norm(text))
    return (meta["sem"], meta["kind"], text, meta["slots"], tid, psha), v


_SCOPE_BAN = re.compile(r"\b(?:these rules|the rules|this rule|the law|by law|legally|lawfully|statute\w*|the act)\b",
                        re.I)


def check_wording(iid, text, meta, tid, psha, seen) -> tuple:
    """Question wording: one line ending in '?', G-SL (role wording), EXACT negcount per yes/no form (G0 S11) with the
    right cue type, the full-refund and scope rules (section 4 item 5). -> (qform, text, held_out, task id, sha)."""
    q = meta["qform"]
    if not isinstance(text, str) or "\n" in text.strip() or not text.strip().endswith("?"):
        return None, ["not one question line"]
    text = " ".join(text.split())
    if "{" in text or "}" in text:
        return None, ["brace"]
    sk = K.make_skin("tmp", FAMILY, text, {}, kind="wording", register="question", qform=q)
    v = [f"G-SL {x.rule}: {x.detail}" for x in gsl.lint_template(sk)]
    if not 8 <= len(text.split()) <= 30:
        v.append("8-30 words")
    c = negcount.count(text)
    if q in NEG_EXACT:
        if (c.k_all, c.k_syn) != NEG_EXACT[q]:
            v.append(f"negcount {(c.k_all, c.k_syn)} != {NEG_EXACT[q]}")
        elif q == "yn_not_refund" and not set(c.syn_tokens) <= {"not", "n't"}:
            v.append(f"yn_not_refund cue {c.syn_tokens} (not / n't on the verb)")
        elif q == "yn_no_right" and tuple(c.syn_tokens) != ("no",):
            v.append(f"yn_no_right cue {c.syn_tokens} (no before a noun)")
        if not _FULL.search(text):
            v.append("a yes/no wording names a full refund")
        if _SCOPE_BAN.search(text):
            v.append("narrows the question to the law")
        if q == "yn_owed" and "store" not in text.lower():
            v.append("yn_owed has the store as subject")
        if q == "yn_may_refuse" and not re.search(r"\b(?:refuse|decline|turn down|turn the customer down)\b", text,
                                                  re.I):
            v.append("yn_may_refuse uses refuse / decline / turn down")
    elif q == "ch_rule":
        if not re.search(r"\bif any\b|\bif at all\b|\bnone\b|\bif one\b|\bor no\b", text, re.I):
            v.append("ch_rule allows for none")
        if c.k_all > 1:
            v.append("ch_rule: at most the 'none' cue")
    else:
        right = r"\breject\w*" if q == "ch_end_reject" else r"\b(?:withdraw\w*|cancel\w*)"
        if not re.search(right, text, re.I) or not re.search(r"\b(?:legal|law|statutory)\b", text, re.I):
            v.append("ch_end names the legal right")
        if re.search(r"\b(?:notice|store's|promise\w*|policy|sign)\b", text, re.I):
            v.append("ch_end mentions the notice")
        if re.search(r"\b(?:deliver\w*|possession|purchase date|date of purchase|from (?:the )?purchase|ordered|"
                     r"order date|collect\w*|receiv\w*|counted from|counting from|runs from)\b", text, re.I):
            v.append("ch_end names the anchor")
        if not re.search(r"\b(?:date|day)\b", text, re.I):
            v.append("ch_end asks for a date")
        if c.k_all:
            v.append("ch_end: no negation")
    if text.lower() in seen or text in QSTRINGS:
        v.append("duplicate or fixture copy")
    if not v:
        seen.add(text.lower())
    return (q, text, meta["held_out"], tid, psha), v


def _loop(name: str, root: Path, check) -> tuple:
    """Run one per-item check over a batch's answers: (accepted objects, problems)."""
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


def load_attacks(root: Path = ROOT) -> tuple:
    out, probs = _loop("attacks", root, check_attack)
    return {sk.skin_id: sk for sk in out}, probs


def load_freeform(root: Path = ROOT) -> tuple:
    out, probs = _loop("freeform", root, check_freeform)
    return {sk.skin_id: sk for sk in out}, probs


def load_wordings(root: Path = ROOT) -> tuple:
    return _loop("wordings", root, check_wording)


def load_notices(root: Path = ROOT) -> tuple:
    return _loop("notices", root, check_notice)


def lexicon_registry(wordings: list, notices: list) -> "LexiconRegistry":
    """A T06 LexiconRegistry holding the loaded Haiku forms (source haiku, pending until G-LEX extraction admits them),
    with LEX_MEANINGS / QUESTION_MEANINGS and the never-generated decoys declared (G0 S9, section 4 item 5). Forms whose
    unit test fails stay in the registry with unit_ok False and are never admitted."""
    from c2_kit.lexicon import LexiconRegistry, question_sem
    reg = LexiconRegistry(FAMILY)
    for sem, (kind, meaning) in LEX_MEANINGS.items():
        reg.declare(sem, kind, meaning)
    for qf, meaning in QUESTION_MEANINGS.items():
        reg.declare(question_sem(FAMILY, qf), "question", meaning)
    for sem, meaning in QUESTION_DECOYS.items():
        reg.declare(sem, "question", meaning)
    for sem, _kind, text, slots, tid, psha in notices:
        try:
            reg.add(text, sem, slots=slots, source="haiku", family=FAMILY, haiku_task_id=tid, haiku_prompt_sha=psha)
        except Exception:  # noqa: BLE001  (duplicate or malformed text: dropped, reported by the caller)
            continue
    for q, text, held, tid, psha in wordings:
        try:
            reg.add(text, question_sem(FAMILY, q), family=FAMILY, source="haiku", haiku_task_id=tid,
                    haiku_prompt_sha=psha, held_out=held)
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
            print(f"{name:10s} {b.kind:16s} {b.batch_id}  items {len(b.key):4d}  chunks {len(b.chunks)}")
        return 0
    tasks = write_tasks()
    print(json.dumps({"n_tasks": len(tasks), "by_kind": {k: sum(1 for t in tasks if t["kind"] == k)
                                                         for k in sorted({t["kind"] for t in tasks})}}))
    return 0


if __name__ == "__main__":
    sys.exit(main())
