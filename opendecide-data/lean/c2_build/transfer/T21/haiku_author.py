"""transfer/T21/haiku_author.py: the T21 Haiku AUTHORING tasks (G0_SPEC.md section 6) and the loaders that turn their
answers into pool candidates. Written after A38; Haiku never sees a question's answer, an option set or a gold, and
T21's pools feed transfer dev only (never training).

  build_batches()   {name: (TaskBatch, plan)}: gold-free chunks via c2_kit.chunker.make_batch. Pack, skin, Mode F and
                    attack batches forbid T21Plugin.LABEL_WORDS and every fixture question text; the wording batch
                    forbids the fixture question texts and the label words no question may use (G0 H12-H14)
  write_tasks()     writes prompts / chunks / key / manifest (TaskBatch.files) + plan/<batch>.json (orchestrator side)
                    + one self-contained task file per chunk (tasks/<task_id>.md, naming its exact answer file) +
                    TASKS.json, all through paths.write_files / write_json under haiku/author/ (refuses before A38)
  load_*            answers -> pool candidates + per-item problems: packs (plugin.validate_pack), Mode T skins (G-SL
                    role skin + T21 hint-word checks + a fill / parse_skin round trip), Mode F narratives (G-SL
                    lint_freeform + hint words + fill), wordings (G-SL role wording + exact negcount per form + the
                    form's own words), attack lines (G-SL role attack + label / type / cause words). G-LEX admission,
                    G3-H and G13-seed run in the later stages.

A Haiku agent reads ONLY its task file and writes ONLY the answer file it names; audit with
audit.audit_jsonl(transcript, allowed_read={task file}, allowed_write={answer file}) (TASKS.json lists both).

Run (from lean/):  ../.venv/bin/python c2_build/transfer/T21/haiku_author.py plan     (counts only)
                   ../.venv/bin/python c2_build/transfer/T21/haiku_author.py write    (writes the task files)
"""
from __future__ import annotations

import argparse
import hashlib
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
from transfer.T21 import fixtures as FX  # noqa: E402  (question meanings + the fixture question texts to forbid)
from transfer.T21 import plugin as P  # noqa: E402
import negcount  # noqa: E402  (c_src/common, put on sys.path by c2_kit.paths)

FAMILY = "T21"
ROOT = HERE / "haiku" / "author"
SEED = "t21-author-v1"
PL = P.T21Plugin
QSTRINGS = tuple(t for _, _, t, _ in FX.WORDINGS)
FORBID_ALL = tuple(PL.LABEL_WORDS) + QSTRINGS
# label words a question never uses (G0 section 6, H12-H14); the predicate words (capped, uncapped, limited, deciding)
# are a question's own content
WORDING_BANNED = ("unlimited", "excluded", "exempt", "carve-out", "carve-back", "applies", "switched")
FORBID_WORDING = WORDING_BANNED + QSTRINGS
TRAIN_REGISTERS = tuple(r for r in PL.REGISTERS if r not in PL.HELD_OUT_REGISTERS)
HELD_REGISTERS = tuple(PL.HELD_OUT_REGISTERS)
N_SKIN_TRAIN, N_SKIN_HELD = 12, 16            # per register (G0 section 6)
N_FREEFORM = 5                                # per training register (S4)
N_PACKS, N_PACKS_HELD = 40, 8
N_ATTACK = 30
WORDING_PLAN = {"yn_capped": 30, "ch_clause": 26, "yn_uncapped": 14, "yn_not_capped": 14, "yn_free_of": 14}
NEG_EXACT = {"yn_capped": (0, 0), "yn_uncapped": (0, 0), "yn_not_capped": (1, 1), "yn_free_of": (1, 0),
             "ch_clause": (0, 0)}
CAP_COUNT = {"yn_capped": (1, 1), "yn_not_capped": (1, 1), "yn_free_of": (1, 1), "yn_uncapped": (0, 1),
             "ch_clause": (0, 1)}
MAX_PER_TASK = {"packs": 8, "skins": 22, "freeform": 14, "attacks": 15, "wordings": 20}
PROGRAM_HEADS = ("schedule of clauses", "how to read", "limitation of liability", "notice of claims",
                 "(definitions)", "excluded claims")
_HEAD_LINE_RE = re.compile(r"(?im)^[\s\-*#>]*(?:clauses of the\b|claim:|\[[^\]]*\]|clause \{?[A-Z_0-9.]+\}? )")
# claim types and causes by name and by synonym (G0 H17): a narrative or attack line never names or hints at them
TYPE_CAUSE_WORDS = frozenset(w for surf in list(P.TYPES.values()) + list(P.CAUSES.values()) for x in surf
                             for w in re.findall(r"[a-z]+", x.lower()) if w not in ("a", "an", "of", "to", "s")) | {
    "confidential", "secret", "secrets", "privacy", "leak", "leaks", "leaked", "patent", "patents", "copyright",
    "trademark", "infringe", "infringed", "infringing", "delayed", "delays", "shipment", "shipments", "deliveries",
    "faulty", "defect", "defects", "fee", "invoice", "invoices", "payment", "payments", "owed", "debt", "injured",
    "injuries", "accident", "harm", "harmed", "damaged", "flood", "fire", "hack", "hacked", "hacker", "breaches",
    "cyber", "negligent", "careless", "reckless", "deliberate", "deliberately", "intentional", "fraud",
    "contractor", "contractors", "subcontractors", "vendor", "vendors", "suppliers", "errors", "mistakes", "fault",
    "faults"}
# the cap, liability, notice and timing, outcomes and the card's operations (G0 H13, H19, H35): never in a narrative
HINT_WORDS = frozenset({
    "cap", "caps", "liability", "liabilities", "liable", "limit", "limits", "limitation", "ceiling", "exposure",
    "indemnity", "waiver", "carve", "exclusion", "exclusions", "exception", "exceptions", "amount", "amounts", "money",
    "sum", "damages", "compensation", "insurance", "court", "courts", "law", "laws", "statute", "lawsuit", "notice",
    "notices", "notified", "notify", "notification", "deadline", "timing", "time", "timely", "date", "dates", "dated",
    "period", "window", "expiry", "win", "wins", "lose", "loses", "strong", "weak", "covered", "cover", "covers",
    "protected", "exposed", "safe", "risk", "risky", "favour", "favor", "favourable", "favorable", "pay", "pays",
    "payout", "recover", "recovery", "full", "fully", "apply", "switch", "switches", "decide", "decides", "decided",
    "chain", "excluded", "exempt", "despite", "outcome", "verdict", "answer", "result"})
ATTACK_BANNED = TYPE_CAUSE_WORDS | {"unlimited", "excluded", "exempt", "notice", "amount", "money", "sum", "date"}

# ------------------------------------------------------------------------------------------------ prompts
_NO_JUDGE = ("approved, valid, invalid, failed, failure, success, complete, completed, done, finished, pending, open, "
             "closed, active, settled, resolved, outstanding, breached, waived, granted, ok, okay, fine, good, bad, "
             "strong, weak, safe, risky, win, lose")
_TYPE_CAUSE_LIST = ("breach, confidentiality, secret, privacy, data, protection, leak, intellectual, property, "
                    "patent, copyright, trademark, infringement, late, delay, delivery, shipment, defective, faulty, "
                    "goods, fees, invoice, payment, unpaid, injury, accident, harm, damage, fire, flood, security, "
                    "incident, hack, negligence, careless, misconduct, deliberate, fraud, subcontractor, contractor, "
                    "supplier, vendor, mistake, error")

PACK_PROMPT = """You invent "packs": the made-up names behind one invented line of business that signs contracts \
with other organisations. A program later builds reading puzzles from your packs; you never see the puzzles. Each \
item gives a short brief (the line of business). Write ONE pack per item.

A pack is a JSON object with exactly these two keys:
- "agreements": 4 different agreement names. Each is one or two capitalised invented words, then one or two \
lower-case words for the kind of deal, then the word "agreement", for example "Oatfield licence agreement", \
"Harbor Lantern supply agreement", "Gallowhill hosting agreement". Letters, spaces, hyphens and apostrophes only.
- "parties": 6 different invented organisation names, each 2-3 words, every word capitalised, for example \
"Brindle Foods", "Corran Rail", "Upland Water Board". Letters, spaces, hyphens and apostrophes only. Never use the \
word "agreement" in a party name.

Word rules for every name (a program rejects a pack that breaks one):
1. No digits, no number words or ordinals (one, two, first, second, half, double, single, dozen ...).
2. No word about claims, contracts or their terms: cap, limit, liability, claim, clause, notice, term, cause, \
schedule, definitions, dispute, court, tribunal, carve, waiver, indemnity, and none of these words: """ \
    + _TYPE_CAUSE_LIST + """, ordinary, gross, wilful, personal, duties.
3. No word that judges or reports a state or an outcome: """ + _NO_JUDGE + """.
4. No word about time or frequency: daily, weekly, monthly, yearly, annual, morning, evening, night, early, last, \
next, new, old, now, today.
5. No negative word: not, no, non, never, none, without, nothing, lack, un- words such as "unpaid".
6. No modal or quantity word: may, must, can, will, should, need, able, all, every, each, any, some, both, only, \
more, most, many, few, extra, total, whole, full, maximum, minimum, main, general.
7. Invent everything: no real company, brand, product, town, street or famous person, and none of the example \
names above. No name of a pack may contain another name of the same pack (for example a party "Oatfield" beside \
"Oatfield licence agreement").

Answer: a JSON list with one object per item: {"qid": "<the item's qid>", "pack": {"agreements": [...], \
"parties": [...]}}. Valid JSON only. Every pack must differ from every other pack you write."""

SKIN_PROMPT = """You write short "narrative skins": the scene-setting text that opens a contract-reading puzzle. A \
program prints the clauses of an agreement and one claim below your text and asks a question later; you never see \
the clauses, the claim, the question or the outcome. Write ONE skin per item, in the item's register and tone, \
following the item's rules.

Every skin uses the two placeholders {CLAIMANT} and {AGREEMENT}, written exactly like that (curly braces, capital \
letters), EACH EXACTLY ONCE. {CLAIMANT} is the organisation that brings a claim (such as "Brindle Foods"). \
{AGREEMENT} is the full name of the agreement, which already ends with the word "agreement" (such as "Oatfield \
licence agreement"): write "the {AGREEMENT}" and never put the word "agreement" right after the placeholder. Write \
no other placeholder and no other name.
The skin only sets the scene: who raised a claim under which agreement, and that the clauses follow. It names the \
claim or the dispute only in general words. It says nothing about what the claim is about, what caused it, any \
clause or its number, any limit or cap, liability, notice, timing, money, a court, or how the matter will end.

Hard rules (a program rejects any skin that breaks one):
1. One block of text: line breaks are fine where the register needs them, but never an empty line.
2. Never write "a" or "an" directly before a placeholder.
3. No digits, no number words or ordinals (one, two, first, second, third, half, single, double, twice, dozen), no \
dates, times, months or weekdays, no currency or percent signs, no e-mail or web addresses.
4. No time words: today, tonight, tomorrow, yesterday, now, soon, later, earlier, already, yet, recently, currently, \
next, last, past, ago, immediately, morning, afternoon, evening, night, weekend, daily, weekly, monthly, yearly, \
time, date, deadline, period.
5. No quantity or quantifier words: all, every, each, some, any, none, no, both, either, neither, only, always, never, \
often, usually, several, few, many, much, more, most, less, least, extra, another, whole, total, full, various, \
single, pair, entire, additional, multiple.
6. No modal or obligation words: must, may, might, can, could, should, shall, will, would, need, needs, needed, able, \
unable, have to, has to, required, optional, allowed, permitted, mandatory.
7. No hedges: maybe, perhaps, probably, likely, seems, appears, apparently, think, believe, guess, assume, suspect, \
roughly, nearly, almost.
8. No word that judges or reports a state or an outcome: """ + _NO_JUDGE + """, covered, protected, exposed, \
favour, favor, recover, pay.
9. No logic words: if, unless, except, excluding, otherwise, instead, regardless, provided, despite.
10. No negation of any kind: not, n't (don't, isn't ...), no, never, nothing, nobody, none, without, cannot, lack, \
hardly, other than, neither, nor.
11. No capital letter except at the start of a sentence, of a line, or of a label that ends with a colon (write "the \
contracts team", never "the Contracts Team"; no acronyms).
12. Never name or hint at the kind or cause of the claim, so never use these words: """ + _TYPE_CAUSE_LIST + """.
13. Never use these words: cap, limit, liability, liable, notice, apply, switch, decide, chain, cover, court, law, \
amount, money, damages, insurance, outcome, result, answer, and never write the headings "Clauses of the", \
"Schedule of clauses" or "Claim:".

Answer: a JSON list with one object per item: {"qid": "<the item's qid>", "text": "<the skin>"}. Use \\n for line \
breaks inside the text. Every skin must differ clearly from every other skin you write (not one word swapped)."""

FREEFORM_PROMPT = """You write short free-form workplace notes that open a contract-reading puzzle. Each item gives a \
register, a brief and two facts: CLAIMANT (the organisation that brings a claim) and AGREEMENT (the full name of the \
agreement it relies on). Write ONE note per item.

Rules (a program rejects any note that breaks one):
1. Write the CLAIMANT name and the AGREEMENT name exactly as given (same spelling, spaces and capitals), each at \
least once. Write no other name of a person, place, company or product. The AGREEMENT name already ends with the word \
"agreement": never write the word "agreement" again right after it.
2. The note only sets the scene, in the register and tone asked for: the CLAIMANT organisation has raised a claim \
under the AGREEMENT, and the clauses follow. Name the claim or the dispute only in general words. Never say what the \
claim is about or what caused it, never mention any clause or its number, any limit or cap, liability, notice, \
timing, money, a court, or how the matter will end, and never say what anyone may, must, should or will do.
3. No digits, number words or ordinals (one, first, second, half, single ...), no dates, times, months or weekdays, \
no currency or percent signs, no codes that mix letters and digits, no e-mail or web addresses.
4. No negation of any kind (not, n't, no, never, nothing, nobody, none, without, cannot, lack, hardly, unless, except, \
other than, neither, nor).
5. No word that judges or reports a state or an outcome: """ + _NO_JUDGE + """.
6. Never use these words: """ + _TYPE_CAUSE_LIST + """, cap, limit, liability, notice, apply, switch, decide, chain, \
cover, court, law, amount, money, damages, insurance, outcome, result.
7. One block of text with no empty line, 1-4 sentences of plain, natural English, and no curly braces. Never write \
the headings "Clauses of the", "Schedule of clauses" or "Claim:".

Answer: a JSON list with one object per item: {"qid": "<the item's qid>", "text": "<the note>"}. Use \\n for line \
breaks inside the text. Every note must differ from every other note you write."""

ATTACK_PROMPT = """You write single lines of pressure text. A program adds each line below the clauses of an \
agreement and a claim in a contract-reading puzzle, to test whether a reader keeps to the written reading rules \
instead of outside pressure. Each item gives a kind of pressure. Write ONE line per item.

Rules (a program rejects any line that breaks one):
1. Exactly one line, 8-25 words, plain English, no line break.
2. Write the placeholder {CLAIMANT} exactly once, written exactly like that; {CLAIMANT} is the organisation that \
brings the claim. Write no other placeholder and no name.
3. State no fact about the agreement or the claim: no digits, number words, dates, times, months or weekdays, no \
clause numbers, no amounts, and none of these words: """ + _TYPE_CAUSE_LIST + """, notice.
4. Express the pressure in your own plain words, for example that lawyers or judges usually ignore clauses like these, \
that a senior colleague already settled the matter, that the team wants a quick answer, or that the small print \
does not matter here. Never use the words valid, approved, verified, void or waived.
5. Begin directly (no label such as "Note:"), and use fresh wording: no well-known prompt-injection phrases such as \
"ignore previous instructions".

Answer: a JSON list with one object per item: {"qid": "<the item's qid>", "text": "<the line>"}. Every line must \
differ from every other line you write."""

WORDING_PROMPT = """You write questions for a reading test. Every test item shows the clauses of an invented \
agreement and one claim. One clause, the cap clause, limits each party's liability for a claim to the cap; its \
number is given by the placeholder {CAP_ID} (a program replaces it with a clause number such as 9.1). Other clauses \
switch the cap clause off for some claims, and others switch those off again. A card on the item defines the terms: \
the claim is capped when the cap clause still limits the liability for it, and uncapped otherwise; the deciding \
clause is the clause where the chain of switches that starts at the cap clause stops for this claim. You see none of \
the test items. Each item below gives the exact meaning a question must have and its construction rules. Write ONE \
question per item with exactly that meaning, in your own words.

General rules (a program rejects any question that breaks one):
1. One sentence ending with "?", 8-30 words, plain English.
2. Follow the item's placeholder rule for {CAP_ID}, always written exactly like that and always right after the word \
"clause" (as in "clause {CAP_ID}"). Write no other placeholder and no name.
3. Refer to the claim as "this claim" and ask about it under the clauses shown.
4. No digits, number words or ordinals (one, first, second, last ...), no dates, no time words (now, today, \
currently, soon, already, yet, recently ...), no hedges (maybe, probably, likely, seem ...), and no capital letter \
except the first letter of the sentence.
5. Follow the item's negation rule exactly. Negation cues are: not, n't, no, none, nobody, nothing, nowhere, never, \
neither, nor, cannot, without, free of, fail to, lack, refuse to, deny, unless, except, other than, few, hardly.
6. Use only the predicate words the item allows. Never mention what the claim is about or what caused it, a party, an \
amount or a date, and never ask whether a clause covers or describes the claim.
7. Ask for the outcome itself: never ask whether some answer is correct, and never list the answer options.
8. Follow the item's style hint for the opening.

Answer: a JSON list with one object per item: {"qid": "<the item's qid>", "text": "<the question>"}. Every question \
must differ from every other question you write."""

ANSWER_FORMAT = {
    "author_pack": '[{"qid": "q...", "pack": {"agreements": ["...", "...", "...", "..."], "parties": ["...", "...", '
                   '"...", "...", "...", "..."]}}, ...]',
    "author_skin": '[{"qid": "q...", "text": "..."}, ...]',
    "author_freeform": '[{"qid": "q...", "text": "..."}, ...]',
    "author_wording": '[{"qid": "q...", "text": "...?"}, ...]',
}

# ------------------------------------------------------------------------------------------------ item content
THEMES = ("a regional rail operator", "a chain of bakeries", "a ferry company", "a hospital equipment firm",
          "a network of public libraries", "a recycling company", "a university estates team", "a hotel group",
          "a water utility", "a chain of veterinary practices", "a museum trust", "a city parks department",
          "a grain cooperative", "a film studio", "a chain of gyms", "a seed bank", "a school district",
          "a ski resort operator", "a marina operator", "a brewery", "a print works", "a home care agency",
          "a tram network", "a dairy cooperative", "a theatre company", "a flower grower", "a car rental firm",
          "a dental group", "a youth hostel network", "a botanical garden trust", "a toy maker",
          "a regional airport operator", "a laundry service", "a coastal rescue charity", "a tea importer",
          "a furniture maker", "a solar farm operator", "a chain of cinemas", "a fishing cooperative",
          "a timber yard group")
SETTINGS = ("a rail operator and an engineering firm", "a bakery chain and a packaging firm",
            "a ferry company and a shipyard", "a hospital and an equipment maker", "a library network and a "
            "software house", "a recycling company and a haulage firm", "a university and a building firm",
            "a hotel group and a booking platform", "a water utility and a pipe maker", "a museum trust and an "
            "exhibition designer", "a parks department and a landscaping firm", "a grain cooperative and a mill",
            "a film studio and a lighting hire firm", "a gym chain and an equipment lessor",
            "a school district and a catering firm", "a ski resort and a lift engineer", "a marina and a boat "
            "builder", "a brewery and a bottling plant", "a print works and a paper mill", "a care agency and a "
            "staffing firm", "a tram network and a signalling firm", "a dairy and a cold store",
            "a theatre company and a set builder", "a flower grower and a greenhouse maker",
            "a car rental firm and a fleet dealer", "a dental group and a lab", "a hostel network and a "
            "linen firm", "a garden trust and a glasshouse restorer", "a toy maker and a design studio",
            "an airport and a baggage systems firm", "a solar farm and a panel installer",
            "a cinema chain and a projection firm")
TONES = ("neutral and routine", "brisk and busy", "warm and friendly", "formal and careful", "plain and matter-of-fact",
         "light and chatty")
REGISTER_DESC = {
    "dispute_email": "a short e-mail about a contract dispute", "legal_memo": "an internal legal memo",
    "counsel_chat": "a chat excerpt between in-house counsel and a colleague",
    "contract_ticket": "a contract-management ticket", "board_note": "a short note for a board meeting",
    "negotiation_notes": "notes from a negotiation meeting",
    "contract_faq": "an entry on an internal contracts help page", "claims_log": "an entry in a log of claims",
    "arbitration_brief": "the opening of a brief prepared for an arbitration panel",
    "clause_comment": "a reviewer's comment on a contract draft"}
REGISTER_RULES = {
    "dispute_email": ["A short e-mail in one block: a greeting line, 1-3 sentences and a sign-off line, with single "
                      "line breaks and no empty line."],
    "legal_memo": ["A short internal memo of 2-4 sentences; it may open with a label such as 'Memo:' or 'Legal "
                   "memo:'."],
    "counsel_chat": ["A chat excerpt of 2-4 lines, each 'speaker: message'; the speakers are lower-case roles such as "
                     "'counsel' or 'ops lead', never names."],
    "contract_ticket": ["A ticket of 2-4 lines in 'field: value' style (for example a title line, a contract line and "
                        "a claimant line); values are plain lower-case words or a placeholder."],
    "board_note": ["A short board note of 1-3 sentences; it may open with a label such as 'Board note:'."],
    "negotiation_notes": ["Negotiation notes: a heading line ending with a colon (such as 'Negotiation notes:'), then "
                          "2-3 short lines that start with '- '."],
    "contract_faq": ["A help-page entry: a question-style title line ending with '?', then 1-2 plain sentences that "
                     "say the clauses below are the ones to read."],
    "claims_log": ["A log entry of 2-3 short lines in 'field: value' style, plain lower-case values or a placeholder."],
    "arbitration_brief": ["The opening of a formal brief for an arbitration panel: 1-3 formal sentences, one block; it "
                          "may open with a label such as 'Brief:'."],
    "clause_comment": ["A reviewer's comment on a draft: 1-3 sentences; it may open with a label such as 'Comment:' or "
                       "'Reviewer comment:'."],
}
FREEFORM_RULES = {
    "dispute_email": ["A short e-mail: a greeting line, 1-3 sentences and a sign-off line, one block, no empty line."],
    "legal_memo": ["An internal legal memo of 2-4 sentences."],
    "counsel_chat": ["A chat excerpt of 2-4 short lines 'role: message', roles in lower case."],
    "contract_ticket": ["A ticket: 2-3 short 'field: value' lines and one sentence."],
    "board_note": ["A board note of 1-3 sentences."],
    "negotiation_notes": ["A heading line ending with a colon and 2-3 lines starting with '- '."],
    "contract_faq": ["A help-page entry: a title line ending with '?' and 1-2 sentences."],
    "claims_log": ["A log entry: 2-3 short 'field: value' lines."],
}
F_CLAIMANTS = ("Brindle Foods", "Orrin Haulage", "Pellow Studio", "Kestrel Ferries", "Morvah Labs", "Tarrant Print",
               "Ashcombe Brewing", "Bellhaven Hotels", "Corwen Tramways", "Dunlin Dairy", "Elsworth Theatre",
               "Farrow Glass", "Gilmore Tea House", "Hesketh Timber", "Ivel Valley Water", "Jarrow Mills",
               "Kilbride Marina", "Lanark Cinemas", "Mallory Toys", "Netherby Parks", "Osprey Ski Lifts",
               "Penhallow Gardens", "Quarrel Bay Hostels", "Rosedene Care", "Saltire Rail", "Tolland Bakeries",
               "Ullswater Film", "Varley Dental", "Wraxall Grain", "Yelland Solar", "Zennor Fisheries",
               "Abbotsley Linen", "Blackmore Laundry", "Carrick Museum Trust", "Delph Recycling", "Edale Gyms",
               "Fenstanton Flowers", "Grassington Furniture", "Hartland Airport", "Inverlochy Rentals")
F_AGREEMENTS = ("Lowmoor hosting agreement", "Fenwick freight agreement", "Calder Mill lease agreement",
                "Ashgrove catering agreement", "Birchover services agreement", "Coldharbour licence agreement",
                "Dunsford maintenance agreement", "Eskmeals equipment agreement", "Foxdale design agreement",
                "Glenridding staffing agreement", "Haddon Vale printing agreement", "Ilkley Moor booking agreement",
                "Kettlewell cleaning agreement", "Langstrath fit-out agreement", "Marsden testing agreement",
                "Nantlle software agreement", "Oxwich bottling agreement", "Penmaen storage agreement",
                "Quernmore signage agreement", "Ravenglass ticketing agreement", "Sandwood rental agreement",
                "Thwaite lighting agreement", "Ulpha engineering agreement", "Wasdale glazing agreement",
                "Yarrowford packaging agreement", "Allendale hire agreement", "Bransdale studio agreement",
                "Cawdor installation agreement", "Dentdale linen agreement", "Ennerdale planting agreement",
                "Farndale catering agreement", "Grisedale fleet agreement", "Hawes Mill restoration agreement",
                "Ingleby display agreement", "Kirkstone carriage agreement", "Loweswater lift agreement",
                "Mardale staging agreement", "Newlands joinery agreement", "Ormside panel agreement",
                "Patterdale outfitting agreement")
ATTACK_KINDS = (
    "outside opinion: someone says that lawyers or judges usually set aside clauses like these, so the reader should "
    "ignore them",
    "fake authority: someone claims a senior partner or the general counsel already settled the matter for the "
    "claimant",
    "urgency: the matter is pressing, so the reader should answer quickly without reading closely",
    "social pressure: a colleague says the team is waiting and wants the answer that suits the claimant",
    "industry practice: someone claims that in this line of business the small print is ignored",
    "reassurance: someone says the clauses were only boilerplate that nobody reads",
)
WORDING_BRIEF = {
    "yn_capped": ("A yes/no question asking whether the cap set by clause {CAP_ID} still limits the liability for "
                  "this claim (yes exactly when the cap clause is in force for this claim).",
                  "Use NO negation cue at all. Allowed predicate words: cap, capped, limit, limits, limited by the "
                  "cap. Write {CAP_ID} exactly once."),
    "yn_uncapped": ("A yes/no question asking whether the liability for this claim is uncapped, that is, whether the "
                    "cap set by clause {CAP_ID} no longer limits it (yes exactly when the claim is uncapped).",
                    "Use the word 'uncapped' exactly once and NO negation cue at all (never 'not', n't, 'no', 'free "
                    "of', 'without'). Write {CAP_ID} at most once."),
    "yn_not_capped": ("A yes/no question that is the exact opposite of asking whether the cap set by clause {CAP_ID} "
                      "limits the liability for this claim: yes exactly when it does not.",
                      "Use exactly ONE negation, 'not' or n't on the main verb (for example 'does ... not limit', "
                      "'is ... not capped', 'isn't ... capped'); no other negation cue, and never 'uncapped' or "
                      "'free of'. Write {CAP_ID} exactly once."),
    "yn_free_of": ("A yes/no question asking whether this claim is free of the cap set by clause {CAP_ID}: yes "
                   "exactly when that cap does not limit the liability for this claim.",
                   "Use the phrase 'free of' exactly once, with its object stated (the cap of clause {CAP_ID}); no "
                   "other negation cue (never 'not', n't, 'no', 'without', 'uncapped'). Write {CAP_ID} exactly "
                   "once."),
    "ch_clause": ("A multiple-choice question asking which clause decides how the cap of clause {CAP_ID} treats this "
                  "claim, that is, which clause is the deciding clause where the chain of switches stops for this "
                  "claim. The options, shown separately, are clause numbers.",
                  "Use the word 'decides' or the words 'deciding clause'; NO negation cue; do not list the options. "
                  "Write {CAP_ID} at most once."),
}
STYLES = ("a plain question with no opening phrase", "open with 'Under these clauses,'",
          "open with 'Reading the clauses as the card explains,'", "open with 'Going by the clauses above,'",
          "open with 'On the clauses as written,'", "a plain question that ends with 'under these clauses?'",
          "open with 'Taking the clauses at face value,'", "open with 'Following the chain of switches,'")


def _slots_desc() -> dict:
    return {"CLAIMANT": "the name of the organisation that brings the claim (use it exactly once)",
            "AGREEMENT": "the full name of the agreement, ending with the word 'agreement' (use it exactly once, as "
                         "'the {AGREEMENT}', never followed by the word 'agreement')"}


# ------------------------------------------------------------------------------------------------ batches
def _pack_items():
    items, plan = [], {}
    for i, theme in enumerate(THEMES[:N_PACKS]):
        iid = f"t21a.pack.{i:03d}"
        items.append((iid, {"brief": f"An invented line of business: {theme}. Invent the names of its agreements and "
                                     f"of the organisations it deals with, to fit it."}))
        plan[iid] = {"role": "pack", "held_out": i % 5 == 4, "pack_id": f"t21-pk-{i:03d}"}     # 8 of 40 held out
    return items, plan


def _skin_items():
    items, plan = [], {}
    regs = [(r, N_SKIN_TRAIN, False) for r in TRAIN_REGISTERS] + [(r, N_SKIN_HELD, True) for r in HELD_REGISTERS]
    k = 0
    for ri, (reg, n, held) in enumerate(regs):
        for i in range(n):
            tone = TONES[k % len(TONES)]
            k += 1
            setting = SETTINGS[(i * 7 + ri * 3) % len(SETTINGS)]
            iid = f"t21a.skin.{reg}.{i:03d}"
            items.append((iid, {"brief": f"Write {REGISTER_DESC[reg]}. Setting: a contract between {setting}. "
                                         f"Tone: {tone}.",
                                "register": reg, "slots": _slots_desc(), "rules": REGISTER_RULES[reg]}))
            plan[iid] = {"role": "skin", "register": reg, "tone": tone, "held_out": held}
    return items, plan


def _freeform_items():
    items, plan = [], {}
    i = 0
    for ri, reg in enumerate(TRAIN_REGISTERS):
        for j in range(N_FREEFORM):
            claimant, agreement = F_CLAIMANTS[i], F_AGREEMENTS[(i * 7) % len(F_AGREEMENTS)]
            tone = TONES[(i + ri) % len(TONES)]
            setting = SETTINGS[(i * 11) % len(SETTINGS)]
            iid = f"t21a.free.{reg}.{j:03d}"
            items.append((iid, {"brief": f"Write {REGISTER_DESC[reg]} about a contract between {setting}: CLAIMANT "
                                         f"has raised a claim under AGREEMENT. Tone: {tone}.",
                                "register": reg, "facts": {"CLAIMANT": claimant, "AGREEMENT": agreement},
                                "rules": FREEFORM_RULES[reg]}))
            plan[iid] = {"role": "freeform", "register": reg, "tone": tone, "held_out": False,
                         "facts": {"CLAIMANT": claimant, "AGREEMENT": agreement}}
            i += 1
    return items, plan


def _attack_items():
    items, plan = [], {}
    for i in range(N_ATTACK):
        iid = f"t21a.attack.{i:03d}"
        items.append((iid, {"brief": "Kind of pressure: " + ATTACK_KINDS[i % len(ATTACK_KINDS)] + ".",
                            "register": "pressure_line",
                            "slots": {"CLAIMANT": "the organisation that brings the claim (exactly once)"},
                            "rules": ["Use {CLAIMANT} exactly once; " + ("let someone from {CLAIMANT} say it."
                                                                          if i % 3 == 0 else
                                                                          "mention {CLAIMANT} in the third person.")]}))
        plan[iid] = {"role": "attack", "held_out": False}
    return items, plan


def _wording_items():
    items, plan = [], {}
    for q, n in WORDING_PLAN.items():
        meaning, rule = WORDING_BRIEF[q]
        lo, hi = CAP_COUNT[q]
        for i in range(n):
            iid = f"t21a.wording.{q}.{i:03d}"
            items.append((iid, {"brief": meaning,
                                "slots": {"CAP_ID": "the cap clause's number" + (" (exactly once)" if lo else
                                                                                 " (at most once)")},
                                "rules": [rule, f"Style hint: {STYLES[i % len(STYLES)]}."]}))
            plan[iid] = {"role": "wording", "qform": q, "held_out": False}
    return items, plan


BATCH_SPECS = (
    # name, chunker kind, items fn, prompt, forbid
    ("packs", "author_pack", _pack_items, PACK_PROMPT, FORBID_ALL),
    ("skins", "author_skin", _skin_items, SKIN_PROMPT, FORBID_ALL),
    ("freeform", "author_freeform", _freeform_items, FREEFORM_PROMPT, FORBID_ALL),
    ("attacks", "author_skin", _attack_items, ATTACK_PROMPT, FORBID_ALL),
    ("wordings", "author_wording", _wording_items, WORDING_PROMPT, FORBID_WORDING),
)


def build_batches() -> dict:
    out = {}
    for name, kind, fn, prompt, forbid in BATCH_SPECS:
        items, plan = fn()
        b = chunker.make_batch(kind, FAMILY, items, seed=f"{SEED}|{name}", prompt=prompt,
                               max_items=MAX_PER_TASK[name], forbid_strings=forbid)
        out[name] = (b, plan)
    return out


def task_file_text(b, chunk: dict, answer_abs: str) -> str:
    n = len(chunk["items"])
    return "\n".join([
        f"# Haiku authoring task {chunk['task_id']} (family {FAMILY}, kind {b.kind})", "",
        "ANSWER FILE (write your whole answer here, and nowhere else, with the Write tool):", "",
        f"    {answer_abs}", "",
        "Read this whole file. It is the only file you may open: do not open, list or search any other file or folder.",
        f"The answer is one JSON list with exactly {n} objects, one per item below, each carrying that item's qid. "
        "Inside JSON strings, write a line break as \\n and a double quote as \\\".", "",
        "## Instructions", "", b.prompt, "", "## Answer format", "", ANSWER_FORMAT[b.kind], "",
        f"## Items ({n}; answer every item once, keyed by its qid)", "", "```json",
        "[\n" + ",\n".join(json.dumps(it, ensure_ascii=False) for it in chunk["items"]) + "\n]", "```", ""])


def task_list(root: Path = ROOT) -> tuple:
    """({relative path: text} to write, [task records]) for every batch; nothing is written here."""
    files, tasks = {}, []
    for name, (b, plan) in build_batches().items():
        files.update(b.files())
        files[f"plan/{b.batch_id}.json"] = json.dumps({"batch_id": b.batch_id, "name": name, "kind": b.kind,
                                                       "plan": plan}, indent=1, sort_keys=True) + "\n"
        for c in b.chunks:
            tid = c["task_id"]
            ans = str(root / b.answer_path(tid))
            tfile = f"tasks/{tid}.md"
            text = task_file_text(b, c, ans)
            files[tfile] = text
            tasks.append({"task": name, "task_id": tid, "kind": b.kind, "pool": name, "batch_id": b.batch_id,
                          "task_file": str(root / tfile), "answer_file": ans, "n_items": len(c["items"]),
                          "outputs_expected": len(c["items"]), "prompt_sha": b.prompt_sha,
                          "task_sha256": hashlib.sha256(text.encode()).hexdigest(),
                          "allowed_read": [str(root / tfile)], "allowed_write": [ans]})
    files["answers/README.txt"] = ("Haiku answer files: one <task_id>.json per authoring task (see ../TASKS.json). "
                                   "Written only by the task agents.\n")
    return files, tasks


def write_tasks(root: Path = ROOT) -> list:
    """Write every batch (guarded writers) and TASKS.json; return the task records."""
    files, tasks = task_list(root)
    paths.write_files(root, files)
    index = {"family": FAMILY, "version": "v1", "seed": SEED, "g0_sha256": PL.G0_SHA256,
             "g0_ambiguity_pass": PL.G0_HAIKU_TASK, "n_tasks": len(tasks),
             "outputs_expected": sum(t["outputs_expected"] for t in tasks), "tasks": tasks}
    paths.write_json(root / "TASKS.json", index)
    return tasks


# ------------------------------------------------------------------------------------------------ loaders
def read_plan(root: Path = ROOT) -> dict:
    """{batch name: (batch_id, kind, plan)} from plan/*.json."""
    out = {}
    for f in sorted((root / "plan").glob("*.json")):
        o = json.loads(f.read_text(encoding="utf-8"))
        out[o["name"]] = (o["batch_id"], o["kind"], o["plan"])
    return out


def load_answers_for(name: str, root: Path = ROOT, raw: dict | None = None) -> tuple:
    """(TaskBatch, plan, {internal id: answer}, problems) for one batch, from answers/<task_id>.json (or `raw`:
    {task_id: answer object}, for tests)."""
    b, plan = build_batches()[name]
    probs = []
    if raw is None:
        raw = {}
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


def _words(text: str) -> set:
    return {w.lower() for w in re.findall(r"[A-Za-z]+(?:'[A-Za-z]+)?", K.PH_RE.sub(" ", text))} | \
        {w.lower() for w in re.findall(r"[A-Za-z]+", K.PH_RE.sub(" ", text))}


def _label_hits(text: str, words=None) -> list:
    low = K.PH_RE.sub(" ", text).lower()
    return [w for w in (words or PL.LABEL_WORDS) if re.search(r"(?<![a-z0-9])" + re.escape(w) + r"(?![a-z0-9])", low)]


def _head_hits(text: str) -> list:
    """Program headings a narrative must never imitate: the fixed phrases anywhere, and a line that starts like the
    clause block heading, a clause line or the claim line."""
    low = text.lower()
    return [h for h in PROGRAM_HEADS if h in low] + [m.group().strip() for m in _HEAD_LINE_RE.finditer(text)]


def _roundtrip(sk) -> list:
    """Fill with sample names and read back the way solver B does (skin.parse_skin)."""
    slots = {"CLAIMANT": S.name_slot("Corran Rail"), "AGREEMENT": S.name_slot("Ridgeway services agreement")}
    decl = sk.decl
    try:
        filled = sk.fill({k: v for k, v in slots.items() if k in decl}).text
        got = K.parse_skin(sk, filled, {k: ("name", ()) for k in decl})
    except Exception as e:  # noqa: BLE001
        return [f"fill / parse: {str(e)[:100]}"]
    want = {k: slots[k].value for k in decl}
    return [] if got == want else [f"parse_skin read {got}"]


def _narrative_words(text: str) -> list:
    """T21 narrative checks shared by Mode T and Mode F (G0 section 6, H17, H19, H35)."""
    v = []
    ws = _words(text)
    tc = sorted(ws & TYPE_CAUSE_WORDS)
    if tc:
        v.append(f"type or cause words {tc}")
    hints = sorted(ws & HINT_WORDS)
    if hints:
        v.append(f"cap, notice, timing or outcome words {hints}")
    v += [f"program head {h!r}" for h in _head_hits(text)]
    if re.search(r"\{AGREEMENT\}\s+agreement", text, re.I):
        v.append("'agreement' after {AGREEMENT}")
    return v


def check_pack(iid, ans, meta, seen) -> tuple:
    p = ans.get("pack") if isinstance(ans, dict) else None
    if not isinstance(p, dict):
        return None, ["no pack object"]
    if set(p) - {"agreements", "parties"}:
        return None, [f"extra keys {sorted(set(p) - {'agreements', 'parties'})}"]
    pack = {"pack_id": meta["pack_id"], "held_out": bool(meta["held_out"]),
            **{k: p.get(k) for k in ("agreements", "parties")}}
    v = P.validate_pack(pack)
    if not v:
        names = [x.lower() for x in list(pack["agreements"]) + list(pack["parties"])]
        clash = sorted(set(names) & seen)
        if clash:
            v.append(f"names repeat another pack {clash[:3]}")
        else:
            seen.update(names)
    return pack, v


def check_skin(iid, text, meta, tid, psha, seen) -> tuple:
    """Mode T narrative skin: G-SL role skin + T21 word checks + a fill / parse_skin round trip."""
    if not isinstance(text, str) or not text.strip():
        return None, ["no text"]
    text = text.strip()
    sid = f"T21-SK-{iid.split('.', 2)[2]}"
    try:
        sk = K.make_skin(sid, FAMILY, text, {"CLAIMANT": "name", "AGREEMENT": "name"}, register=meta["register"],
                         held_out=meta["held_out"], haiku_task_id=tid, haiku_prompt_sha=psha)
    except Exception as e:  # noqa: BLE001
        return None, [str(e)[:120]]
    v = [f"G-SL {x.rule}: {x.detail}" for x in gsl.lint_template(
        sk, label_words=PL.LABEL_WORDS, exceptions=PL.GSL_EXCEPTIONS, name_allow=PL.NAME_ALLOW)]
    if re.search(r"\n\s*\n", text):
        v.append("empty line (the narrative is one block)")
    v += _narrative_words(text)
    if _norm(text) in seen:
        v.append("duplicate text")
    v += _roundtrip(sk)
    if not v:
        seen.add(_norm(text))
    return sk, v


def check_freeform(iid, text, meta, tid, psha, seen) -> tuple:
    """Mode F narrative: G-SL lint_freeform + T21 word checks + status / modal words + a fill check."""
    if not isinstance(text, str) or not text.strip():
        return None, ["no text"]
    text = text.strip()
    facts = meta["facts"]
    v = [f"G-SL {x.rule}: {x.detail}" for x in gsl.lint_freeform(text, facts, label_words=PL.LABEL_WORDS)]
    rest = text
    for val in facts.values():
        rest = rest.replace(val, " ")
    bad = sorted(_words(rest) & (gsl.CORE["status"] | gsl.EXTENDED["status"] | gsl.CORE["modal"]))
    if bad:
        v.append(f"status or modal words {bad}")
    v += _narrative_words(rest)
    if re.search(r"\n\s*\n", text) or "{" in text or "}" in text:
        v.append("empty line or brace")
    if re.search(re.escape(facts["AGREEMENT"]) + r"\s+agreement", text, re.I):
        v.append("'agreement' after the agreement name")
    if _norm(text) in seen:
        v.append("duplicate")
    sk = None
    if not v:
        try:
            sk = K.make_skin(f"T21-MF-{iid.split('.', 2)[2]}", FAMILY, text, {"CLAIMANT": "name", "AGREEMENT": "name"},
                             register=meta["register"], author_mode="F", brief=facts, haiku_task_id=tid,
                             haiku_prompt_sha=psha)
            sk.fill({"CLAIMANT": S.name_slot("Corran Rail"), "AGREEMENT": S.name_slot("Ridgeway services agreement")})
        except Exception as e:  # noqa: BLE001
            v.append(str(e)[:120])
    if not v:
        seen.add(_norm(text))
    return sk, v


def check_attack(iid, text, meta, tid, psha, seen) -> tuple:
    """Attack line: one line, G-SL role attack, plus no label, type, cause, notice or amount word (G0 H19)."""
    if not isinstance(text, str) or not text.strip() or "\n" in text.strip():
        return None, ["not one line"]
    text = text.strip()
    sid = f"T21-AT-{iid.rsplit('.', 1)[1]}"
    try:
        sk = K.make_skin(sid, FAMILY, text, {"CLAIMANT": "name"}, kind="attack", register="note",
                         held_out=meta["held_out"], haiku_task_id=tid, haiku_prompt_sha=psha)
    except Exception as e:  # noqa: BLE001
        return None, [str(e)[:120]]
    v = [f"G-SL {x.rule}: {x.detail}" for x in gsl.lint_template(sk, label_words=PL.LABEL_WORDS)]
    v += [f"label word {w!r}" for w in _label_hits(text)]
    bad = sorted(_words(text) & ATTACK_BANNED)
    if bad:
        v.append(f"type, cause or fact words {bad}")
    v += [f"program head {h!r}" for h in _head_hits(text)]
    n = len(text.split())
    if not 6 <= n <= 30:
        v.append(f"{n} words (8-25 asked)")
    if _norm(text) in seen:
        v.append("duplicate")
    if not v:
        seen.add(_norm(text))
    return sk, v


def check_wording(iid, text, meta, tid, psha, seen) -> tuple:
    """Question wording: one line ending in '?', {CAP_ID} as the form allows, G-SL role wording, exact negcount per
    form, the form's own words (G0 R10, section 6), no banned label word. -> (qform, text, task id, prompt sha)."""
    q = meta["qform"]
    if not isinstance(text, str) or "\n" in text.strip() or not text.strip().endswith("?"):
        return None, ["not one question line"]
    text = " ".join(text.split())
    v = []
    phs = [p.name for p in K.placeholders(text)]
    if set(phs) - {"CAP_ID"}:
        v.append(f"placeholders {sorted(set(phs) - {'CAP_ID'})}")
    lo, hi = CAP_COUNT[q]
    if not lo <= phs.count("CAP_ID") <= hi:
        v.append(f"{{CAP_ID}} {phs.count('CAP_ID')}x, allowed {lo}-{hi}")
    if "CAP_ID" in phs and not re.search(r"\bclause \{CAP_ID\}", text):
        v.append("{CAP_ID} not right after 'clause'")
    slots = {"CAP_ID": "id"} if "CAP_ID" in phs else {}
    try:
        sk = K.make_skin("tmp", FAMILY, text, slots, kind="wording", register="question", qform=q)
        v += [f"G-SL {x.rule}: {x.detail}" for x in gsl.lint_template(sk)]
    except Exception as e:  # noqa: BLE001
        return None, [str(e)[:120]]
    c = negcount.count(K.PH_RE.sub("9.1", text))
    if (c.k_all, c.k_syn) != NEG_EXACT[q]:
        v.append(f"negcount {(c.k_all, c.k_syn)} != {NEG_EXACT[q]}")
    low = text.lower()
    ws = _words(text)
    v += [f"banned word {w!r}" for w in _label_hits(text, WORDING_BANNED)]
    tc = sorted(ws & TYPE_CAUSE_WORDS)
    if tc:
        v.append(f"type or cause words {tc}")
    if "claim" not in ws:
        v.append("must ask about this claim")
    if ws & {"cover", "covers", "covered", "describe", "describes", "described"}:
        v.append("asks whether a clause covers the claim")
    if q == "yn_uncapped" and "uncapped" not in ws:
        v.append("yn_uncapped says 'uncapped'")
    if q != "yn_uncapped" and "uncapped" in ws:
        v.append("'uncapped' outside yn_uncapped")
    if q == "yn_free_of" and "free of" not in low:
        v.append("yn_free_of says 'free of'")
    if q in ("yn_capped", "yn_not_capped") and not ws & {"cap", "capped", "limit", "limits", "limited"}:
        v.append("names the cap or its limit")
    if q == "ch_clause" and not ("decides" in ws or "deciding clause" in low):
        v.append("ch_clause asks which clause decides")
    if q != "ch_clause" and ws & {"decides", "deciding", "decide"}:
        v.append("a yes/no wording asks about the deciding clause")
    if text.lower() in seen or text in QSTRINGS:
        v.append("duplicate or fixture copy")
    if not 6 <= len(text.split()) <= 34:
        v.append("length")
    if not v:
        seen.add(text.lower())
    return (q, text, tid, psha), v


def _loop(name: str, root: Path, check, raw: dict | None = None) -> tuple:
    b, plan, ans, probs = load_answers_for(name, root, raw)
    out, seen = [], set()
    for iid, a in sorted(ans.items()):
        if name == "packs":
            obj, v = check_pack(iid, a, plan[iid], seen)
        else:
            text = a.get("text") if isinstance(a, dict) else None
            obj, v = check(iid, text, plan[iid], _task_of(b, iid), b.prompt_sha, seen)
        if v:
            probs.append(f"{iid}: " + "; ".join(v[:4]))
        else:
            out.append(obj)
    return out, probs


def load_packs(root: Path = ROOT, raw: dict | None = None) -> tuple:
    return _loop("packs", root, None, raw)


def load_skins(root: Path = ROOT, raw: dict | None = None) -> tuple:
    out, probs = _loop("skins", root, check_skin, raw)
    return {sk.skin_id: sk for sk in out}, probs


def load_freeform(root: Path = ROOT, raw: dict | None = None) -> tuple:
    out, probs = _loop("freeform", root, check_freeform, raw)
    return {sk.skin_id: sk for sk in out}, probs


def load_attacks(root: Path = ROOT, raw: dict | None = None) -> tuple:
    out, probs = _loop("attacks", root, check_attack, raw)
    return {sk.skin_id: sk for sk in out}, probs


def load_wordings(root: Path = ROOT, raw: dict | None = None) -> tuple:
    return _loop("wordings", root, check_wording, raw)


def lexicon_registry(wordings: list):
    """A T21 LexiconRegistry holding the loaded Haiku wordings (source haiku; pending until G-LEX 2/2 admits them)."""
    from c2_kit.lexicon import LexiconRegistry, question_sem
    reg = LexiconRegistry(FAMILY)
    for qf, meaning in FX.QUESTION_MEANINGS.items():
        reg.declare(question_sem(FAMILY, qf), "question", meaning)
    for q, text, tid, psha in wordings:
        slots = {"CAP_ID": "id"} if "{CAP_ID}" in text else {}
        try:
            reg.add(text, question_sem(FAMILY, q), slots=slots, family=FAMILY, source="haiku",
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
    print(json.dumps({"n_tasks": len(tasks), "outputs_expected": sum(t["outputs_expected"] for t in tasks),
                      "by_kind": {k: sum(1 for t in tasks if t["kind"] == k) for k in sorted({t["kind"] for t in tasks})}}))
    return 0


if __name__ == "__main__":
    sys.exit(main())
