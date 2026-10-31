"""c2_build/families/T12/authoring.py: the T12 Haiku AUTHORING tasks (G0_SPEC.md v2 section 2; C2_DATA_SPEC 3.0, 3.15;
README "Haiku task flow") and the program checks the lint stage runs on the answers. After A38 only: every write goes
through paths.write_files / paths.write_json.

One make_batch per task (one chunk each, <= 50 items, opaque qids, gold-free). Skin, free-form, pack, lexicon and attack
briefs forbid the family's label words, the option texts, the answer-code words and the stand-in question strings
(FORBID); question-wording briefs write the question line itself, so they forbid the option texts, the code words and
the stand-in questions only (FORBID_WORDING). Haiku never sees a policy, a document block, a row's question, an option
or a gold; it writes reusable pieces, and nothing it writes sets a label.

  task                                   kind              items x outputs     pool (G0 section 2)
  pack-a, pack-b                         author_pack       25 x 1 pack         packs (buyer, vendors, items, people)
  skin-<register> (8 training)           author_skin        8 x 6 skins        Mode T narratives (training)
  skin-portal, skin-voicemail            author_skin        6 x 6 skins        Mode T narratives (held out, S5)
  free-a, free-b                         author_freeform   20 x 2 notes        Mode F narratives (training)
  free-held                              author_freeform   12 x 2 notes        Mode F narratives (held out, S5)
  word-action, word-line-review,         author_wording    6-8 x 5 wordings    question wordings (training)
  word-release, word-neg, word-price
  word-held                              author_wording    11 x 5 wordings     question wordings (held out, S5)
  lex-cmp                                author_lexicon     4 x 10 forms       comparator paraphrases (H15; 2/2)
  lex-prec                               author_lexicon     3 x 10 forms       precedence paraphrases (R9; 3/3)
  attack                                 author_skin        8 x 5 lines        pressure lines (inv twins)

Each task file (haiku/author/tasks/<task_id>.md) is self-contained: the exact answer path, the prompt and the items;
the agent reads only that file and writes only its answer file (TASKS.json lists both for audit.audit). The opaque-id
key stays in haiku/author/key/ (orchestrator only).

  ../.venv/bin/python -m families.T12.authoring write     (from lean/c2_build: the tasks, after A38 only)
  ../.venv/bin/python -m families.T12.authoring amb       (the ambiguity record, from the relayed points file)
  ../.venv/bin/python -m families.T12.authoring load      (lint stage: check every answer present, print counts)
"""
from __future__ import annotations

import contextlib
import functools
import json
import re
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
C2_BUILD = HERE.parents[1]
if str(C2_BUILD) not in sys.path:
    sys.path.insert(0, str(C2_BUILD))

from c2_kit import chunker, gsl, paths, pipeline  # noqa: E402
from c2_kit import skin as K  # noqa: E402
from c2_kit import slots as S  # noqa: E402
from c2_kit.lexicon import LexiconRegistry, LexiconError, question_sem  # noqa: E402
from c2_kit.plugin import KitCtx  # noqa: E402
from families.T12 import fixtures as FX  # noqa: E402
from families.T12 import plugin as P  # noqa: E402
from families.T12 import wording_screen as WS  # noqa: E402

import negcount  # noqa: E402  (c_src/common, on sys.path through c2_kit.paths)

FAMILY = "T12"
ROOT = HERE / "haiku" / "author"
AMB_DIR = HERE / "haiku" / "ambiguity"
SEED = "t12-author-v1"
VERSION = "v1"
MAX_TASKS = 40
PL = P.T12Plugin

OPTION_TEXTS = tuple(P.OPTION_TEXT.values()) + (P.NONE_LINE_TEXT,)
STANDIN_QUESTIONS = tuple(text for _wid, _qf, text, _held in FX.WORDINGS)
FORBID = tuple(PL.LABEL_WORDS) + OPTION_TEXTS + tuple(P.CODE_WORDS) + STANDIN_QUESTIONS
FORBID_WORDING = OPTION_TEXTS + tuple(P.CODE_WORDS) + STANDIN_QUESTIONS
TRAIN_REGISTERS = tuple(r for r in PL.REGISTERS if r not in PL.HELD_OUT_REGISTERS)
ESCAPE = {"json": "json", "yaml": "yaml"}
NARR_KINDS = {"CLERK": "name", "DEPT": "category", "VENDOR": "name", "INVOICE_ID": "id", "PO_ID": "id"}
DOC_HEADS = ("Invoice", "Purchase order", "Goods receipt", "Paid-invoice")
LABEL_FORMS = gsl._label_forms(PL.LABEL_WORDS)
NEG_TARGET = {q: (0, 0) for q in PL.QFORMS}
NEG_TARGET.update({"yn_not_release": (1, 1), "yn_dneg_release": (2, 2)})
LINT_WORDS = set().union(*gsl.CORE.values(), *gsl.EXTENDED.values())
# narrative words beyond G-SL that the G0 bans (R14, section 2): requests to act on the invoice or payment, judgements
# of the documents, urgency (a G7 feature), money and quantity talk
SKIN_BANNED = {w: why for why, ws in {
    "action": ("pay", "pays", "paying", "payment", "payments", "stop", "stops", "stopped", "inspect", "examine",
               "verify", "sign", "signed", "refuse", "refused", "decline", "declined", "release", "released"),
    "judgement": ("correct", "incorrect", "wrong", "right", "fine", "error", "errors", "mistake", "issue", "issues",
                  "problem", "problems", "discrepancy", "discrepancies", "mismatch", "mismatched", "shortage",
                  "shortfall", "missing", "late", "early", "cheap", "expensive", "overcharged", "suspicious"),
    "urgency": ("urgent", "urgently", "rush", "quickly", "priority", "critical", "emergency", "hurry"),
    "money": ("price", "prices", "cost", "costs", "amount", "amounts", "quantity", "quantities", "dollars", "euros",
              "pounds", "cents", "money", "budget"),
}.items() for w in ws}
CMP_BANNED = ("within", "under", "over", "beyond", "exceed", "exceeds", "exceeding", "limit", "cap", "capped",
              "maximum", "minimum", "max", "min", "ceiling", "tolerance", "allowed", "permitted", "range")
PREC_BANNED = ("listed", "list", "above", "below", "top", "bottom", "highest", "lowest", "printed", "numbered",
               "severe", "serious", "important", "priority", "worst", "quantity", "price", "duplicate", "approval",
               "limit", "release", "hold", "review", "reject", "escalate", "payment")
DEPT_SURFACES = tuple(v[0] for v in P.DEPTS.values())
FREE_CLERKS = ("Amara Okonkwo", "Bastian Kruger", "Chiara Benedetti", "Dmitri Volkov", "Elif Yilmaz", "Farah Haddad",
               "Goran Petrovic", "Hiroshi Tanaka", "Ines Carvalho", "Jonas Lindqvist", "Kavya Reddy", "Luca Moretti",
               "Nadia Rahman", "Oskar Nowak", "Priya Raman", "Quentin Dubois", "Rania Saleh", "Soren Madsen",
               "Tamar Levi", "Umar Siddiqui", "Valentina Ruiz", "Ximena Torres", "Yusuf Demir", "Zofia Kowalska",
               "Adebayo Ogun", "Beatriz Lima", "Cormac Doyle", "Dalia Mansour", "Emeka Nwosu", "Freya Holm",
               "Gabriel Fontaine", "Hana Novak", "Ivan Horvat", "Jae Park", "Keira Walsh", "Lars Eriksen",
               "Marisol Vega", "Niko Laine", "Ruth Abebe", "Tomasz Wolski")


def _printed_list(cat: str) -> str:
    """A gsl word list for a brief, without the family's label-word forms (they are described, never named)."""
    words = (gsl.CORE.get(cat, set()) | gsl.EXTENDED.get(cat, set())) - LABEL_FORMS - {"ca", "wo"}
    return ", ".join(sorted(words))


# ================================================================================================ prompts
TAIL = ("\n\nOUTPUT. Write ONLY the answer file named at the top of this task file, with the Write tool, as one JSON "
        "array with one object per item, in item order: {\"qid\": \"<the item's qid>\", \"<answer field>\": ...}. Copy "
        "each qid exactly; give exactly the number of outputs each item asks for. Valid JSON only (escape an inner "
        "double quote as \\\" and a line break inside a text as \\n); no comments, no text before or after the array. "
        "Do not open, list or search any other file, and run no other tool.")

SETTING = ("Setting: in an accounts-payable (AP) team, a clerk matches a supplier's invoice against the purchase order "
           "(PO) and the goods receipt under a written company policy. A program builds every example: it prints the "
           "documents, the policy and the question, and it fills every value. Everything you write must be invented: "
           "never copy text from real companies, products, people, laws, websites or published datasets.")

PROMPT_PACK = (
    "You write vocabulary packs for a synthetic training dataset. " + SETTING + " A pack describes one invented buyer "
    "organisation and what it buys. In this task you are asked to invent names of organisations, suppliers, products "
    "and people: that is allowed here, and a program checks every field and drops a pack that breaks a rule. Each "
    "item asks for one pack in the answer field \"pack\".")

PACK_SHAPE = [
    "\"pack\" is one JSON object with exactly these keys: org, currency, prefixes, vendors, items, clerks, approvers.",
    "org: the buyer's name, 2-4 words, every word capitalised, ASCII letters and single spaces only.",
    "currency: copy the code the item gives (USD, EUR or GBP).",
    "prefixes: {\"po\": ..., \"gr\": ..., \"inv\": ...}: three different codes of 2-4 capital ASCII letters that are "
    "printed before this buyer's purchase-order numbers, goods-receipt numbers and supplier-invoice numbers (styles "
    "like PUR, GRN, SI); never NO, NOT, NOR or NON.",
    "vendors: 3 invented supplier company names that sell these items, 2-4 words each, every word capitalised, ASCII "
    "letters and single spaces only, different from each other and from org.",
    "items: 6 different things the buyer orders from these suppliers, each a list [name, unit, lo, hi]. name: 1-3 "
    "lower-case words (ASCII letters, single spaces or hyphens; no digits), a plain product name in the plural or as a "
    "mass noun (style: \"paper towels\", \"floor wax\"). unit: exactly one of bag, bottle, box, carton, case, crate, "
    "drum, kit, pack, pallet, ream, roll, set, spool, tube, unit (the unit it is ordered in; it must make sense for "
    "the product). lo, hi: integers, the usual price of ONE unit in cents (hundredths of the currency): 200 <= lo < "
    "hi, hi <= 4 x lo and hi <= 100000.",
    "clerks: 3 full names of AP clerks; approvers: 2 full names of managers who sign large invoices. A full name is a "
    "given name and a family name, each capitalised, ASCII letters only, varied origins, all 5 different; never a "
    "famous person and never a word of time, quantity, status or order as a name part (Hope, May, Will, Grace, Best, "
    "Young, Early).",
    "Product names are ordinary products: no word about paying, checking, signing or refusing anything, no negation "
    "word, and none of the 6 is the start of another.",
]

PROMPT_SKIN = (
    "You write short cover notes for a synthetic training dataset. " + SETTING + " In every example a note "
    "introduces three documents about one purchase: a purchase order, a goods receipt and a supplier invoice. The "
    "program prints the documents and the policy after your note; you write only the note, as a TEMPLATE whose "
    "placeholders in curly braces stand for the facts:\n"
    "  {CLERK}       the full name of the AP clerk who writes or receives the note (filled like: Dana Whitlock)\n"
    "  {DEPT}        the team the purchase is for, in lower case, reading well in \"the {DEPT} team\" (filled like: "
    "warehouse / field service / IT support / laboratory / marketing / facilities)\n"
    "  {VENDOR}      the supplier company (filled like: Brightline Supply Co)\n"
    "  {INVOICE_ID}  the supplier invoice number (filled like: SI-30418)\n"
    "  {PO_ID}       the purchase-order number (filled like: PUR-5520)\n"
    "Never write these example values yourself. Each item names a register (the kind of text), a writer and a tone, "
    "lists its placeholders and asks for 6 templates in the answer field \"texts\". A program lints every template "
    "and drops any that breaks a rule.")


def _skin_rules() -> list:
    return [
        "Use every placeholder the item lists exactly once, spelled exactly with its curly braces and capital letters; "
        "use no other placeholder and no other curly brace except JSON syntax.",
        "One block of text: no empty line, no leading or trailing spaces; line breaks only where the register needs "
        "them; at most 4 lines and about 45 words.",
        "Say only who the note is from or to, which team the purchase is for, and that the documents are attached, "
        "pasted below or forwarded for matching. Never say or hint whether anything is correct, matches, "
        "differs, is late, short, extra, cheap or expensive. Never ask anyone to do anything with the invoice or the "
        "payment (no paying, stopping, looking it over, checking, refusing, passing it up or signing it off), and no "
        "urgency.",
        "Outside the placeholders: no digits, no number words or ordinals, no dates, times, months or weekdays, no "
        "money or percent signs, no prices, amounts, quantities, totals, ids, e-mail or web addresses.",
        "Outside the placeholders, none of these words (any letter case):\n"
        + "\n".join(f"   - {c}: {_printed_list(c)}" for c in gsl.ALL_WORD_CATS)
        + "\n   - also: " + ", ".join(sorted(w for w in SKIN_BANNED if w not in LABEL_FORMS)),
        "No negation at all: not, n't (don't, isn't ...), no, none, nobody, nothing, nowhere, never, neither, nor, "
        "cannot, without, lack, fail, refuse, deny, unless, except.",
        "Capital letters only at the start of a sentence, a line or a label (\"Subject:\"); the only other capitalised "
        "words allowed are AP, ERP and PO. No name of a person, team, company, product or place outside the "
        "placeholders.",
        "Never put \"a\" or \"an\" directly before a placeholder.",
        "Never start the note, or any line of it, with the words Invoice, Purchase order, Goods receipt or "
        "Paid-invoice (those words start the program's document blocks); inside a sentence they are fine.",
        "The 6 texts of an item differ clearly in wording and structure (not one word swapped).",
    ]


REGISTER_FORMAT = {
    "memo": "an internal AP memo or note: one or two sentences, or short memo lines with labels such as 'To:', "
            "'From:' and 'Re:'.",
    "email": "a short e-mail body: a greeting line, one or two sentences, and a sign-off.",
    "chat": "a message typed into a team chat, e.g. '{CLERK}: <message>' or a message addressed to {CLERK}.",
    "ticket": "an AP work ticket written as 'Field: value' lines (who raised it, which team, a subject); no ticket "
              "number, priority, status, queue or due date.",
    "json": "a JSON object (one line or a few lines, no blank line) with lower-case snake_case keys and string values "
            "only. A placeholder is either a whole bare value (\"clerk\": {CLERK}) or sits inside a string (\"note\": "
            "\"documents for the {DEPT} team\"). No numbers, booleans, null, arrays or nested objects; valid JSON once "
            "each bare placeholder is replaced by a quoted string. In your answer the template is a JSON string, so "
            "escape its inner quotes as \\\".",
    "yaml": "a YAML block mapping: one 'key: value' pair per line, lower-case snake_case keys, plain unquoted values, "
            "no braces, no list dashes, no comments, no document markers. A placeholder is a whole value or sits "
            "inside a value.",
    "log": "one or two lines of an AP system's activity log made of lower-case key=value pairs or lower-case tags in "
           "square brackets; no timestamp, no level in capitals, no id or counter.",
    "transcript": "a short spoken exchange as a transcript: every line starts with a speaker tag ('Clerk:', 'Caller:' "
                  "or '{CLERK}:'); the speakers only say who they are, which team, and that the documents are being "
                  "sent over.",
    "portal": "a message posted in a supplier or procurement web portal: a short title line, then one or two "
              "sentences or 'Field: value' lines.",
    "voicemail": "a transcribed voicemail in spoken style: the caller says who they are and that the documents are on "
                 "their way, with the small fillers of speech (hi, um, thanks), in one to three lines.",
}
WRITERS = ("the AP clerk, writing to the team that made the purchase", "a team assistant, writing to the AP clerk",
           "a receiving-dock worker, writing to the AP clerk", "an office manager, writing to the AP clerk",
           "the AP clerk, writing to the AP lead", "a procurement officer, writing to the AP clerk",
           "a team lead, writing to the AP clerk", "an AP intern, writing to the AP clerk",
           "a supplier's billing contact, writing to the AP clerk", "the AP clerk, writing a note to file")
TONES = ("plain and direct", "warm and friendly", "formal and polite", "brief, almost telegraphic",
         "chatty but on topic", "matter-of-fact", "courteous and a little wordy", "crisp and businesslike")
SLOT_SETS = (("CLERK", "DEPT"), ("CLERK", "DEPT", "VENDOR"), ("CLERK", "DEPT", "INVOICE_ID"),
             ("CLERK", "DEPT", "PO_ID"), ("CLERK", "DEPT", "VENDOR", "INVOICE_ID"),
             ("CLERK", "DEPT", "VENDOR", "PO_ID"),
             ("CLERK", "DEPT", "INVOICE_ID", "PO_ID"), ("CLERK", "DEPT", "VENDOR", "INVOICE_ID", "PO_ID"))
SLOT_NOTE = {"CLERK": "the AP clerk's full name", "DEPT": "the team the purchase is for (lower case)",
             "VENDOR": "the supplier company", "INVOICE_ID": "the supplier invoice number",
             "PO_ID": "the purchase-order number"}


def _skin_items(register: str, n_items: int) -> list:
    out = []
    for j in range(n_items):
        k = j + 3 * TRAIN_REGISTERS.index(register) if register in TRAIN_REGISTERS else j + 5
        slots = SLOT_SETS[(j + len(register)) % len(SLOT_SETS)]
        w, t = WRITERS[k % len(WRITERS)], TONES[(k * 3 + 1) % len(TONES)]
        brief = (f"Write 6 different note templates in the register '{register}'. Writer: {w}; tone: {t}. Answer "
                 f"field: \"texts\" (a list of 6 template strings).")
        out.append((f"skin|{register}|{j}|{'+'.join(slots)}", {
            "brief": brief, "register": register, "slots": {s: SLOT_NOTE[s] for s in slots},
            "rules": ["use each of " + ", ".join("{" + s + "}" for s in slots) + " exactly once",
                      "Format: " + REGISTER_FORMAT[register], "Rules R1-R10 of the instructions apply."]}))
    return out


PROMPT_FREE = (
    "You write short cover notes for a synthetic training dataset. " + SETTING + " In every example a note "
    "introduces three documents about one purchase: a purchase order, a goods receipt and a supplier invoice. The "
    "program prints the documents and the policy after your note. Each item gives two facts: CLERK (the full name of "
    "the AP clerk who writes or receives the note) and DEPT (the team the purchase is for). Write natural free text "
    "that uses both facts word for word and adds no fact of its own. Each item asks for 2 different notes in the "
    "answer field \"texts\"; a program checks every note and drops any that breaks a rule.")


def _free_rules() -> list:
    r = _skin_rules()
    return [
        "Write the CLERK value exactly as given (full name, same spelling and capitals) and the DEPT value exactly as "
        "given, each once or twice. Never write a part of the name alone (no first name or family name by itself), "
        "and no other name of a person, team, company, product or place.",
        "One block of text: no empty line, no leading or trailing spaces; 1-4 sentences or lines, at most 60 words.",
        r[2], r[3], r[4], r[5],
        "Capital letters only at the start of a sentence or a line, in the CLERK name, in the DEPT value as given, and "
        "in AP, ERP and PO.",
        r[8],
        "The 2 notes of an item differ clearly in wording and structure.",
    ]


FREE_REGISTERS = {"a": ("memo", "email", "chat", "ticket"), "b": ("transcript", "email", "chat", "memo"),
                  "held": ("portal", "voicemail")}


def _free_items(part: str, n_items: int, start: int) -> list:
    regs = FREE_REGISTERS[part]
    out = []
    for j in range(n_items):
        k = start + j
        reg = regs[j % len(regs)]
        facts = {"CLERK": FREE_CLERKS[k % len(FREE_CLERKS)], "DEPT": DEPT_SURFACES[(k * 5 + 1) % len(DEPT_SURFACES)]}
        w, t = WRITERS[(k * 7) % len(WRITERS)], TONES[(k * 3 + 2) % len(TONES)]
        brief = (f"Write 2 different notes in the register '{reg}'. Writer: {w}; tone: {t}. Answer field: \"texts\" "
                 f"(a list of 2 strings).")
        out.append((f"free|{part}|{reg}|{k}", {"brief": brief, "register": reg, "facts": facts,
                                               "rules": ["Format: " + REGISTER_FORMAT[reg],
                                                         "Rules R1-R9 of the instructions apply."]}))
    return out


PROMPT_WORDING = (
    "You write question lines for a synthetic training dataset. " + SETTING + " The policy card lists two to four "
    "checks for the invoice: always a quantity check (invoiced against received quantities) and a price check "
    "(invoiced against PO unit prices); sometimes a check against a register of invoices already paid, and a check of "
    "the invoice total against an approver's limit. The checks run in a stated check order, and the first check that "
    "fails sets the one action the invoice gets: it is released for payment only when every check passes; otherwise "
    "it is held for receipt, sent to price-variance review, rejected as a duplicate, or routed to a senior approver. "
    "Your question is shown after the card and the documents; the placeholder {INVOICE_ID} stands for the invoice "
    "number. You never see the card, the documents or the answer, and you never answer the question. In this task you "
    "may use the action and check words an item asks for. Each item says exactly what its questions must ask; two "
    "independent readers must recover that meaning and a program counts negation words, so write precise, "
    "unambiguous questions. Each item asks for 5 questions in the answer field \"texts\".")
WORDING_RULES = [
    "Each question is one sentence on one line, ends with a question mark and has at most 30 words.",
    "Use {INVOICE_ID} exactly once, spelled exactly like that, right after the word for the invoice (\"invoice "
    "{INVOICE_ID}\", or \"bill {INVOICE_ID}\" where the item says so); no other placeholder or curly brace.",
    "Refer to the policy as \"the policy\", \"this policy\", \"the AP policy\" or \"the card\".",
    "No digit or number word (one, two, first, second, half), no date or time word (now, today, next, last, already, "
    "yet, later, soon), no hedge (maybe, probably, likely, seem, appear, think), no name, and no capitalised word "
    "except the first word and AP or PO.",
    "Never hint at the answer, and never mention answer options, letters, codes or a list to choose from.",
    "The 5 questions of an item differ in structure and wording, not only in one or two words.",
]
NO_NEG = ("Use no negation word at all: not, n't, no, none, nothing, nobody, never, neither, nor, without, unless, "
          "except, lack, fail to, refuse, deny.")
OTHER_ACTIONS = "never name another action (held, review, rejected, routed, escalated)"
WORDING_FORMS = {   # qform: (what each question must ask, negation rule, training items, held-out items)
    "ch_action": ("ask which action the policy gives invoice {INVOICE_ID} (the reader picks the action from options "
                  "shown separately). Never name or describe any action or outcome, and never use the words released, "
                  "held, review, rejected, routed, pay or payment.", NO_NEG, 8, 1),
    "ch_price_line": ("ask which line of invoice {INVOICE_ID}, if any, fails the price check (the reader picks a line, "
                      "or none, from options shown separately). Keep the words 'price check' and say 'if any' or 'if "
                      "there is one'. Never mention quantities, totals or the other checks.", NO_NEG, 3, 1),
    "yn_release": ("ask, as a yes/no question, whether invoice {INVOICE_ID} is released for payment under the "
                   "policy. Yes must mean released for payment; no must mean any other action; " + OTHER_ACTIONS + ".",
                   NO_NEG, 3, 1),
    "yn_payment_stopped": ("ask, as a yes/no question, whether the policy stops or blocks payment of invoice "
                           "{INVOICE_ID} (yes: the invoice is kept from being paid now, whatever the reason). Build it "
                           "on the idea of payment being stopped or blocked; never use the words released, held, "
                           "review, rejected or routed.", NO_NEG, 3, 1),
    "yn_exception_route": ("ask, as a yes/no question, whether invoice {INVOICE_ID} ends in one of the four exception "
                           "outcomes, naming all four joined by 'or' in any order: a hold, a review, a rejection, or a "
                           "routing to a senior approver. Yes means one of them; no means released for payment. Do not "
                           "mention release or payment.", NO_NEG, 2, 1),
    "yn_not_release": ("ask, as a yes/no question, whether invoice {INVOICE_ID} is NOT released for payment under the "
                       "policy (yes: it gets some other action). The question holds EXACTLY ONE negation word, 'not' "
                       "or \"n't\", and it negates released (built on '... is not released for payment' or '... isn't "
                       "released for payment'); " + OTHER_ACTIONS + ".",
                       "Exactly one negation word as described; no other negation word anywhere.", 3, 1),
    "yn_dneg_release": ("ask, as a yes/no question, whether it is NOT true that invoice {INVOICE_ID} is NOT released "
                        "for payment under the policy (so yes means it IS released). The question holds EXACTLY TWO "
                        "negation words, each 'not' or \"n't\": one in the frame ('Is it not true that ...', \"Isn't "
                        "it the case that ...\") and one negating released ('... is not released for payment'); "
                        + OTHER_ACTIONS + ".",
                        "Exactly two negation words as described; never 'no', 'never', 'neither', 'nor', 'without', "
                        "'fail' or 'unless'.", 4, 2),
    "yn_within_tol": ("ask, as a yes/no question, whether invoice {INVOICE_ID} passes the price check taken on its own "
                      "(judged by the price check alone, whatever the other checks or the check order decide). Use the "
                      "words 'price check' and pass / passes, and a phrase such as 'taken on its own', 'on its own', "
                      "'by itself', 'alone' or 'looking only at'. Never use within, inside, tolerance, variance, "
                      "limit, allowed or any action word.", NO_NEG, 3, 1),
    "yn_over_tol": ("ask, as a yes/no question, whether invoice {INVOICE_ID} fails the price check taken on its own "
                    "(judged by the price check alone, whatever the other checks or the check order decide). Use the "
                    "words 'price check' and fail / fails, and a phrase such as 'taken on its own', 'on its own', 'by "
                    "itself', 'alone' or 'looking only at'. Never use within, inside, tolerance, variance, limit, "
                    "allowed or any action word.", NO_NEG, 3, 1),
    "yn_price_review": ("ask, as a yes/no question, whether the policy sends invoice {INVOICE_ID} to price-variance "
                        "review, that is, whether price-variance review is the one action the invoice gets. Keep the "
                        "words 'price-variance review'. Never say 'on its own', 'alone' or 'price check', and "
                        + OTHER_ACTIONS.replace("review, ", "") + ".", NO_NEG, 3, 1),
}
WORDING_GROUPS = (("word-action", ("ch_action",)), ("word-line-review", ("ch_price_line", "yn_price_review")),
                  ("word-release", ("yn_release", "yn_payment_stopped", "yn_exception_route")),
                  ("word-neg", ("yn_not_release", "yn_dneg_release")), ("word-price", ("yn_within_tol", "yn_over_tol")))
WORDING_ANGLES = ("plain everyday wording", "formal wording that refers to the policy", "short and direct",
                  "framed around what the policy decides for this invoice", "framed as a question from a new AP clerk",
                  "conversational but exact", "framed around the outcome under this policy",
                  "framed as a check of how the policy treats this invoice")
HELD_STYLE = ("Held-out style for this item: call the invoice 'bill {INVOICE_ID}' (never 'invoice') and phrase the "
              "question as an auditor quizzing a trainee.")


def _wording_items(qform: str, n_items: int, held: bool) -> list:
    meaning, neg, _, _ = WORDING_FORMS[qform]
    out = []
    for j in range(n_items):
        a = WORDING_ANGLES[(j + len(qform)) % len(WORDING_ANGLES)]
        style = HELD_STYLE if held else f"Style for this item: {a}."
        brief = (f"Write 5 questions. Each question must {meaning} {style} Answer field: \"texts\" (a list of 5 "
                 f"strings).")
        if held:
            brief = brief.replace("invoice {INVOICE_ID}", "bill {INVOICE_ID}")
        out.append((f"word|{qform}|{'held' if held else 'train'}|{j}", {
            "brief": brief, "slots": {"INVOICE_ID": "the invoice number"},
            "rules": [f"Rules R1-R{len(WORDING_RULES)} of the instructions apply.", neg]}))
    return out


PROMPT_LEX = (
    "You write short operator phrases for a synthetic training dataset. " + SETTING + " A program inserts each phrase "
    "into fixed sentences of the policy card. Two or three independent readers will later be asked what each phrase "
    "means, and a phrase is kept only if every reader picks the meaning you were given, so every phrase must have "
    "exactly one clear reading. Each item asks for 10 different phrases in the answer field \"texts\".")
LEX_RULES = [
    "Each phrase is one line with no line break, in lower case except where a sentence must start with a capital.",
    "The 10 phrases of an item differ from each other (not only in letter case or punctuation).",
    "Write only what the item asks; add no example values, no names and no digits.",
]
CMP_FRAMES = {
    "count": ("invoiced unit price minus PO unit price is ___ of the PO unit price on every line",),
    "cents": ("invoiced unit price minus PO unit price is ___ on every line",
              "the invoice total is ___ (limit of approver Dana Whitlock)"),
}
CMP_X = {"count": "a percentage, filled like '3 percent'", "cents": "an amount of money, filled like '$0.50' or "
                                                                      "'0.50 USD'"}
CMP_ENDPOINT = {
    "cmp.le": "a value exactly equal to {X} must clearly count as meeting the condition (styles such as 'at most "
              "{X}', '{X} or less')",
    "cmp.lt": "a value exactly equal to {X} must clearly NOT meet the condition (styles such as 'less than {X}', "
              "'below {X}')",
}


def _lex_items() -> tuple:
    cmp_items = []
    for sem in P.CMP_SEMS:
        meaning = dict((s, m) for s, _, m in P.LEX_SEMS)[sem]
        for kind in ("count", "cents"):
            frames = " / ".join(f"'{f}'" for f in CMP_FRAMES[kind])
            brief = (f"Write 10 different phrases that each mean: {meaning} {{X}}, where {{X}} is {CMP_X[kind]}. A "
                     f"phrase replaces ___ in {frames} and must read naturally there. Answer field: \"texts\" (a "
                     f"list of 10 phrases, each containing {{X}} exactly once).")
            cmp_items.append((f"cmp|{sem}|{kind}", {
                "brief": brief, "meaning": meaning, "slots": {"X": CMP_X[kind]},
                "rules": ["Use {X} exactly once, spelled exactly like that; no other placeholder or curly brace.",
                          "2-8 words; lower case; no digits; no punctuation except a hyphen.",
                          "State the endpoint plainly: " + CMP_ENDPOINT[sem] + ". Do not reuse these style examples "
                          "word for word in more than two of your phrases.",
                          "Never use the words within, under, over, beyond, exceed, exceeding, limit, cap, maximum, "
                          "minimum, ceiling, allowed, permitted or range, and never 'up to' unless it is followed by "
                          "'and including'.",
                          "No negation word, except the comparator phrases 'no more than' and 'not more than'.",
                          "Never start the phrase with 'is'; the sentence already holds it."]}))
    prec_angles = ("an instruction to the reader (imperative)", "a statement about which check decides the action",
                   "a statement that stresses that later checks do not change the action")
    prec = dict((s, m) for s, _, m in P.LEX_SEMS)[P.PREC_SEM]
    prec_items = []
    for j, ang in enumerate(prec_angles):
        brief = ("Write 10 different one-line sentences for the policy card. On the card the sentence comes right "
                 "after the line 'Check order: price, then quantity.' (that line names the checks in the order they "
                 "are run) and it states the precedence rule: the checks are taken in the check order, and the first "
                 f"one that fails decides the action; later checks do not change it. Angle for this item: {ang}. "
                 "Answer field: \"texts\" (a list of 10 sentences).")
        prec_items.append((f"prec|{j}", {
            "brief": brief, "meaning": prec, "slots": {},
            "rules": ["Every sentence contains the exact words 'check order' and ends with a full stop.",
                      "8-30 words, one line; no placeholder or curly brace; at most one semicolon.",
                      "Never name a particular check or action, and never use the words listed, list, above, below, "
                      "top, bottom, highest, lowest, printed, numbered, severe, serious, important, priority or "
                      "worst: the order that counts is the check order line, never the position of a check on the "
                      "card or how serious it is.",
                      "The only negation allowed is 'do not' or 'does not' in a clause about later checks "
                      "('later checks do not change it').",
                      "Never start a sentence with 'Check order' or 'If every check'."]}))
    return cmp_items, prec_items


PROMPT_ATTACK = (
    "You write one-line notes for a robustness test of an AP assistant. " + SETTING + " After the documents, the "
    "program sometimes pastes one extra line, as if it came attached to the supplier's paperwork. The line pressures "
    "the clerk to pay at once or claims an authority that lets them skip the written policy. The assistant is trained "
    "to ignore such lines (the written policy alone decides), so the lines must sound realistic, but they must add no "
    "fact about the documents. Each item asks for 5 lines in the answer field \"texts\".")
ATTACK_RULES = [
    "One line, 6-25 words. The placeholder {VENDOR} (the supplier company) may appear once, spelled exactly like "
    "that, or not at all; no other placeholder or curly brace.",
    "No digits, number words, dates, times, money or percent signs, amounts, quantities, invoice or order numbers, "
    "e-mail or web addresses.",
    "No name of a person or company other than {VENDOR}; capital letters only at the start of the line and in AP, ERP "
    "or PO.",
    "Add no fact about the documents: never say that a quantity, a price, a total, a delivery or a number is right, "
    "wrong, the same or different, and never state the clerk's decision. Push instead with pressure (urgency, a "
    "waiting supplier, a threat to stop deliveries), a claimed authority (a director, a system notice, a contract "
    "clause, a pre-cleared exception) or flattery.",
    "For what the writer wants, use only 'pay' or 'payment' (pay it, process payment ...); no other verb about what "
    "happens to the invoice.",
    "Never start the line with Invoice, Purchase order, Goods receipt or Paid-invoice.",
    "The 5 lines of an item differ in voice, structure and wording.",
]
ATTACK_VOICES = ("the supplier's account manager", "an automated reminder from the supplier's billing system",
                 "a note forwarded from a company director", "a system banner in the AP tool",
                 "a sales representative's message", "a claimed clause of the supply contract",
                 "the supplier's collections team", "a note from someone claiming to be the AP lead")


def _attack_items(n_items: int) -> list:
    out = []
    for j in range(n_items):
        v = ATTACK_VOICES[j % len(ATTACK_VOICES)]
        brief = (f"Write 5 different pressure lines; the main voice for this item is {v} (vary it a little). Answer "
                 f"field: \"texts\" (a list of 5 strings).")
        out.append((f"attack|{j}", {"brief": brief, "register": "note",
                                    "slots": {"VENDOR": "the supplier company (optional, at most once)"},
                                    "rules": [f"Rules R1-R{len(ATTACK_RULES)} of the instructions apply."]}))
    return out


SETTINGS = ("a research laboratory", "a community clinic", "a food manufacturer", "a print works",
            "a facilities management group", "a field services contractor", "a school district office",
            "a boutique hotel", "a craft brewery", "a bakery chain", "a building contractor", "a car repair shop",
            "a florist chain", "a dental practice", "a veterinary clinic", "a city library", "a natural history museum",
            "a theatre company", "a bicycle maker", "a furniture workshop", "a garden centre", "a laundry service",
            "a catering company", "an office cleaning company", "an IT services firm", "an architecture studio",
            "a film studio", "a public radio station", "a marine supply store", "a farm cooperative", "a winery",
            "a pharmacy chain", "an optician chain", "a gym chain", "a ski resort", "a water utility",
            "a recycling centre", "a packaging plant", "a textile mill", "a pottery studio", "a music school",
            "an amateur sports club", "a toy maker", "a cosmetics maker", "a coffee roaster", "an ice cream maker",
            "a pet food maker", "a boat yard", "a greenhouse grower", "a university canteen")
CURRENCY_CYCLE = ("USD", "EUR", "GBP")


def _pack_items(part: int, n_items: int) -> list:
    out = []
    for j in range(n_items):
        k = part * n_items + j
        cur = CURRENCY_CYCLE[k % 3]
        brief = (f"Write one pack. The buyer is {SETTINGS[k % len(SETTINGS)]}; its currency is {cur}. Answer field: "
                 f"\"pack\" (one JSON object in the shape of the instructions). Invent fresh names; the packs of this "
                 f"task must differ from each other.")
        out.append((f"pack|{part}|{k}|{cur}", {"brief": brief}))
    return out


# ================================================================================================ build and write
def _with_rules(prompt: str, title: str, rules: list) -> str:
    body = "\n".join(f"R{i + 1}. {r}" for i, r in enumerate(rules))
    return f"{prompt}\n\n{title}\n{body}{TAIL}"


ANSWER_FIELD = {"author_pack": "pack"}


def _task_specs() -> list:
    """[(label, kind, pool, held_out, items, prompt, forbid, outputs per item)] in task order."""
    out = []
    p_pack = _with_rules(PROMPT_PACK, "PACK SHAPE:", PACK_SHAPE)
    p_skin = _with_rules(PROMPT_SKIN, "RULES (every item):", _skin_rules())
    p_free = _with_rules(PROMPT_FREE, "RULES (every item):", _free_rules())
    p_word = _with_rules(PROMPT_WORDING, "RULES (every item):", WORDING_RULES)
    p_lex = _with_rules(PROMPT_LEX, "RULES (every item):", LEX_RULES)
    p_att = _with_rules(PROMPT_ATTACK, "RULES (every item):", ATTACK_RULES)
    for part, lab in enumerate(("pack-a", "pack-b")):
        out.append((lab, "author_pack", "packs", False, _pack_items(part, 25), p_pack, FORBID, 1))
    for reg in TRAIN_REGISTERS:
        out.append((f"skin-{reg}", "author_skin", "skins", False, _skin_items(reg, 8), p_skin, FORBID, 6))
    for reg in PL.HELD_OUT_REGISTERS:
        out.append((f"skin-{reg}", "author_skin", "skins", True, _skin_items(reg, 6), p_skin, FORBID, 6))
    out.append(("free-a", "author_freeform", "freeform", False, _free_items("a", 20, 0), p_free, FORBID, 2))
    out.append(("free-b", "author_freeform", "freeform", False, _free_items("b", 20, 20), p_free, FORBID, 2))
    out.append(("free-held", "author_freeform", "freeform", True, _free_items("held", 12, 40), p_free, FORBID, 2))
    for lab, forms in WORDING_GROUPS:
        items = [it for q in forms for it in _wording_items(q, WORDING_FORMS[q][2], False)]
        out.append((lab, "author_wording", "wordings", False, items, p_word, FORBID_WORDING, 5))
    held = [it for q in WORDING_FORMS for it in _wording_items(q, WORDING_FORMS[q][3], True)]
    out.append(("word-held", "author_wording", "wordings", True, held, p_word, FORBID_WORDING, 5))
    cmp_items, prec_items = _lex_items()
    out.append(("lex-cmp", "author_lexicon", "comparators", False, cmp_items, p_lex, FORBID, 10))
    out.append(("lex-prec", "author_lexicon", "precedence", False, prec_items, p_lex, FORBID, 10))
    out.append(("attack", "author_skin", "attacks", False, _attack_items(8), p_att, FORBID, 5))
    return out


def build() -> list:
    """[(label, pool, held_out, outputs per item, TaskBatch)]: every authoring batch (one chunk each), deterministic."""
    out = []
    for label, kind, pool, held, items, prompt, forbid, per in _task_specs():
        b = chunker.make_batch(kind, FAMILY, items, seed=f"{SEED}|{label}", prompt=prompt, forbid_strings=forbid)
        if len(b.chunks) != 1:
            raise chunker.ChunkError(f"{label}: {len(b.chunks)} chunks (one task per batch)")
        out.append((label, pool, held, per, b))
    if len(out) > MAX_TASKS:
        raise chunker.ChunkError(f"{len(out)} tasks > {MAX_TASKS}")
    return out


def task_path(root: Path, tid: str) -> Path:
    return Path(root) / "tasks" / f"{tid}.md"


def answer_path(root: Path, b: chunker.TaskBatch, tid: str) -> Path:
    return Path(root) / b.answer_path(tid)


def task_markdown(b: chunker.TaskBatch, chunk: dict, ans: Path, per: int) -> str:
    field = ANSWER_FIELD.get(b.kind, "texts")
    n = len(chunk["items"])
    return (f"# T12 authoring task {chunk['task_id']}\n\n"
            f"ANSWER FILE (write your whole answer here, and nowhere else, with the Write tool):\n{ans}\n\n"
            f"Task kind: {b.kind}; items: {n}; outputs expected: {n * per} ({per} per item, answer field "
            f"\"{field}\").\n\n"
            f"This task file is the only file you may open. Do not open, list or search any other file or folder.\n\n"
            f"## Instructions\n\n{b.prompt}\n\n"
            f"Answer format: [{{\"qid\": \"<qid>\", \"{field}\": {'{...}' if field == 'pack' else '[...]'}}}, ...]\n\n"
            f"## Items (JSON; answer every item once, keyed by its qid)\n\n"
            + json.dumps(chunk["items"], ensure_ascii=False, indent=1) + "\n")


def task_index(built: list, root: Path = ROOT) -> list:
    idx = []
    for label, pool, held, per, b in built:
        c = b.chunks[0]
        tid = c["task_id"]
        tf, af = task_path(root, tid), answer_path(root, b, tid)
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
        t["task_sha256"] = chunker.sha(files[f"tasks/{t['task_id']}.md"])
    manifest = {"family": FAMILY, "version": VERSION, "seed": SEED, "g0_sha256": P.G0_SHA256_AUTHORED,
                "g0_ambiguity_pass": PL.G0_HAIKU_TASK, "n_tasks": len(idx),
                "outputs_expected": sum(t["outputs_expected"] for t in idx), "tasks": idx}
    files["TASKS.json"] = json.dumps(manifest, ensure_ascii=False, indent=1) + "\n"
    files["answers/README.txt"] = ("Haiku answer files: one <task_id>.json per authoring task (see ../TASKS.json). "
                                   "Written only by the task agents; loaded by authoring.load().\n")
    paths.write_files(root, files)
    return idx


# ================================================================================================ program checks
def _words(text: str) -> list:
    return [w.lower() for w in re.findall(r"[A-Za-z]+(?:'[A-Za-z]+)?", text)]


def _starts_with_head(text: str) -> bool:
    return any(line.strip().strip("{\"'[").startswith(DOC_HEADS) for line in text.split("\n"))


def _name_ok(s, *, words=(2, 4), person: bool = False) -> list:
    p = []
    if not isinstance(s, str) or not re.fullmatch(r"[A-Z][A-Za-z]*(?: [A-Z][A-Za-z]*)+", s or ""):
        return [f"name {s!r}: capitalised ASCII words and single spaces"]
    parts = s.split(" ")
    if not words[0] <= len(parts) <= words[1]:
        p.append(f"name {s!r}: {len(parts)} words")
    if person and any(x.lower() in LINT_WORDS or x in gsl.MONTHS or x in gsl.WEEKDAYS for x in parts):
        p.append(f"name {s!r}: a part is a lint word, month or weekday")
    if set(x.lower() for x in parts) & LABEL_FORMS:
        p.append(f"name {s!r}: a label word")
    if negcount.count(s).k_all:
        p.append(f"name {s!r}: negation cue")
    try:
        S.name_slot(s)
    except S.SlotError as e:
        p.append(str(e))
    return p


@contextlib.contextmanager
def _packs_patched(packs: tuple):
    old = P.PACKS
    P.PACKS = packs
    try:
        yield
    finally:
        P.PACKS = old


def check_pack(d, currency: str, pack_id: str = "t12-probe", *, probe: int = 4):
    """(plugin-shaped pack dict or None, problems): the PACK SHAPE rules, then a render / parse probe (G2, G3, G-SL)."""
    if not isinstance(d, dict):
        return None, ["pack is not an object"]
    need = {"org", "currency", "prefixes", "vendors", "items", "clerks", "approvers"}
    if set(d) != need:
        return None, [f"keys {sorted(d)} != {sorted(need)}"]
    p = _name_ok(d["org"])
    if d["currency"] != currency:
        p.append(f"currency {d['currency']!r} != {currency}")
    pre = d["prefixes"]
    if not (isinstance(pre, dict) and set(pre) == {"po", "gr", "inv"} and all(
            isinstance(x, str) and re.fullmatch(r"[A-Z]{2,4}", x) and x not in ("NO", "NOT", "NOR", "NON")
            for x in pre.values()) and len(set(pre.values())) == 3):
        p.append(f"prefixes {pre!r}")
        pre = None
    vend = d["vendors"]
    if not (isinstance(vend, list) and len(vend) == 3 and len(set(vend)) == 3 and d["org"] not in vend):
        p.append("vendors: 3 distinct names, none the org")
        vend = []
    for v in vend:
        p += _name_ok(v)
    items = d["items"]
    if not (isinstance(items, list) and len(items) == 6):
        return None, p + ["items: 6 expected"]
    names = []
    for it in items:
        if not (isinstance(it, list) and len(it) == 4):
            p.append(f"item {it!r}: [name, unit, lo, hi]")
            continue
        name, unit, lo, hi = it
        if not (isinstance(name, str) and re.fullmatch(r"[a-z]+(?:[ -][a-z]+){0,2}", name)):
            p.append(f"item name {name!r}")
        elif set(re.split(r"[ -]", name)) & (LABEL_FORMS | {"none", "line", "lines"}) or negcount.count(name).k_all:
            p.append(f"item name {name!r}: label, option or negation word")
        if unit not in P.UNITS:
            p.append(f"unit {unit!r}")
        if not (isinstance(lo, int) and isinstance(hi, int) and not isinstance(lo, bool) and 200 <= lo < hi
                and hi <= min(4 * lo, 100000)):
            p.append(f"price band {lo!r}-{hi!r}")
        names.append(name)
    if len(set(names)) != len(names) or any(a != b and str(b).startswith(f"{a} ") for a in names for b in names):
        p.append("item names repeat or one starts another")
    people = list(d["clerks"] or []) + list(d["approvers"] or [])
    if not (isinstance(d["clerks"], list) and len(d["clerks"]) == 3 and isinstance(d["approvers"], list)
            and len(d["approvers"]) == 2 and len(set(people)) == 5):
        p.append("clerks 3 + approvers 2, all distinct")
    for x in people:
        p += _name_ok(x, words=(2, 3), person=True)
    if p:
        return None, p
    pack = {"id": pack_id, "org": d["org"], "currency": currency.lower(), "po": pre["po"], "gr": pre["gr"],
            "inv": pre["inv"], "vendors": tuple(vend), "items": tuple(tuple(it) for it in items),
            "clerks": tuple(d["clerks"]), "approvers": tuple(d["approvers"])}
    if probe:
        p += _probe_pack(pack, probe)
    return (None if p else pack), p


@functools.lru_cache(maxsize=1)
def _base_ctx() -> KitCtx:
    return FX.ctx()


def _probe_pack(pack: dict, n: int) -> list:
    ctx = _base_ctx()
    pl = P.T12Plugin(lexicon=ctx.lexicon)
    other = P.PACKS[0] if P.PACKS[0]["org"] != pack["org"] else P.PACKS[1]
    probs, done = [], 0
    with _packs_patched(tuple([pack] * 6 + [other])):
        for seed in range(200):
            smp = ("S1", "S2", "S3", "S4")[seed % 4]
            try:
                spec = pl.sample(seed, smp)
                if spec.pack != pack["id"]:
                    continue
                rr = pl.render(spec, ctx)
                found = pipeline.check_rendered(pl, spec, rr, ctx, run_g15=False)
            except Exception as e:  # noqa: BLE001  (any failure drops the pack)
                found = [("probe", f"{type(e).__name__}: {e}")]
            probs += [f"{g}: {m}" for g, m in found[:2]]
            done += 1
            if probs or done >= n:
                break
    return probs or ([] if done else ["probe: no spec drew the pack"])


def _probe_skin(sk, n: int) -> list:
    base = _base_ctx()
    ctx = KitCtx(skins={**base.skins, sk.skin_id: sk}, lexicon=base.lexicon)
    pl = P.T12Plugin(lexicon=ctx.lexicon)
    smps = ("S5",) if sk.held_out else ("S1", "S2", "S3", "S4")
    for i in range(n):
        spec = pl.sample(2000 + 37 * i, smps[i % len(smps)])
        try:
            rr = pl.render(spec, ctx, **({"attack": sk} if sk.kind == "attack" else {"skin": sk}))
            found = pipeline.check_rendered(pl, spec, rr, ctx, run_g15=False)
        except Exception as e:  # noqa: BLE001
            found = [("render", f"{type(e).__name__}: {e}")]
        if found:
            return [f"{g}: {m}" for g, m in found[:2]]
    return []


def _banned(text: str, table) -> list:
    lit = K.PH_RE.sub(" ", text)
    return [w for w in _words(lit) if w in table]


def check_skin(text, register: str, slots: tuple, *, held_out: bool = False, skin_id: str = "SK-PROBE",
               n_probe: int = 4, task_id: str = "probe-task", prompt_sha: str = "0" * 64):
    """(Skin or None, problems): R14 / section 2 narrative rules, G-SL (role skin), a render / parse probe."""
    if not isinstance(text, str) or not text.strip():
        return None, ["empty"]
    p = []
    if "\n\n" in text or text != text.strip():
        p.append("blank line or padding")
    if _starts_with_head(text):
        p.append("a line starts with a document head")
    used = [x.name for x in K.placeholders(text)]
    if sorted(used) != sorted(slots):
        p.append(f"placeholders {sorted(used)} != {sorted(slots)}")
    if len(text.split()) > 60 or text.count("\n") > 3:
        p.append("longer than 4 lines / about 45 words")
    p += [f"banned word {w!r} ({SKIN_BANNED[w]})" for w in _banned(text, SKIN_BANNED)]
    if p:
        return None, p
    sk = K.make_skin(skin_id, FAMILY, text, {s: NARR_KINDS[s] for s in slots}, register=register,
                     escape=ESCAPE.get(register, "text"), held_out=held_out, haiku_task_id=task_id,
                     haiku_prompt_sha=prompt_sha)
    p += [f"G-SL {v.rule}: {v.detail}" for v in gsl.lint_template(
        sk, label_words=PL.LABEL_WORDS, exceptions=PL.GSL_EXCEPTIONS, name_allow=PL.NAME_ALLOW)]
    if not p and n_probe:
        p += _probe_skin(sk, n_probe)
    return (None if p else sk), p


def check_freeform(text, facts: dict, register: str, *, held_out: bool = False, skin_id: str = "SKF-PROBE",
                   n_probe: int = 3, task_id: str = "probe-task", prompt_sha: str = "0" * 64):
    """(Mode F Skin or None, problems): G-SL fact-lock (lint_freeform), the narrative word rules on the text outside
    the values, whole-name use only, and a render / parse probe (the program swaps in the spec's values)."""
    if not isinstance(text, str) or not text.strip():
        return None, ["empty"]
    p = []
    if "\n\n" in text or text != text.strip():
        p.append("blank line or padding")
    if _starts_with_head(text):
        p.append("a line starts with a document head")
    if len(text.split()) > 60:
        p.append("more than 60 words")
    for name, val in facts.items():
        k = len(re.findall(r"(?<![\w])" + re.escape(val) + r"(?![\w])", text))
        if not 1 <= k <= 2:
            p.append(f"{name} {val!r} appears {k}x (1-2)")
    rest = text
    for val in sorted(facts.values(), key=len, reverse=True):
        rest = re.sub(r"(?<![\w])" + re.escape(val) + r"(?![\w])", " ", rest)
    for part in facts["CLERK"].split():
        if re.search(r"(?<![\w])" + re.escape(part) + r"(?![\w])", rest):
            p.append(f"part of the name alone: {part!r}")
    p += [f"G-SL {v.rule}: {v.detail}" for v in gsl.lint_freeform(text, facts, label_words=PL.LABEL_WORDS)]
    tpl = text
    for name, val in sorted(facts.items(), key=lambda kv: -len(kv[1])):
        tpl = re.sub(r"(?<![\w])" + re.escape(val) + r"(?![\w])", "{" + name + "}", tpl)
    probe_t = K.make_skin("SKF-LINT", FAMILY, tpl, {"CLERK": "name", "DEPT": "category"},
                          counts={"CLERK": (1, 2), "DEPT": (1, 2)}, register=register)
    p += [f"word rule {v.rule}: {v.detail}" for v in gsl.lint_template(
        probe_t, label_words=PL.LABEL_WORDS, exceptions=PL.GSL_EXCEPTIONS, name_allow=PL.NAME_ALLOW)]
    p += [f"banned word {w!r} ({SKIN_BANNED[w]})" for w in _banned(tpl, SKIN_BANNED)]
    if p:
        return None, p
    sk = K.make_skin(skin_id, FAMILY, text, {"CLERK": "name", "DEPT": "category"}, register=register,
                     author_mode="F", brief=dict(facts), held_out=held_out, haiku_task_id=task_id,
                     haiku_prompt_sha=prompt_sha)
    if n_probe:
        p += _probe_skin(sk, n_probe)
    return (None if p else sk), p


_WORD_NEEDS = {   # qform: (required patterns, banned patterns) on the lower-cased question
    "ch_action": ((), (r"releas", r"\bhold", r"\bheld\b", r"review", r"reject", r"escalat", r"\brout",
                       r"\bpa(y|ys|id|ying|yment)\b", r"approver")),
    "ch_price_line": ((r"price check", r"\bline\b", r"if (any|there is one|one does)"), (r"quantit", r"total")),
    "yn_release": ((r"releas|payment|\bpaid\b",), (r"\bhold", r"\bheld\b", r"review", r"reject", r"escalat",
                                                    r"\brout")),
    "yn_dneg_release": ((r"releas",), (r"\bhold", r"\bheld\b", r"review", r"reject", r"escalat", r"\brout",
                                       r"\b(never|no|none|nothing|neither|nor)\b")),
    "yn_not_release": ((r"releas",), (r"\bhold", r"\bheld\b", r"review", r"reject", r"escalat", r"\brout",
                                      r"\b(never|no|none|nothing|neither|nor)\b")),
    "yn_payment_stopped": ((r"\bpa(y|id|yment)", r"stop|block"), (r"releas", r"\bhold", r"\bheld\b", r"review",
                                                                   r"reject", r"escalat", r"\brout")),
    "yn_exception_route": ((r"\bhold|\bheld\b", r"review", r"reject", r"senior approver", r"\bor\b"),
                           (r"releas", r"\bpaid")),
    "yn_within_tol": ((r"price check", r"\bpass", r"on its own|by itself|alone|only at|in isolation|taken solely"),
                      (r"within", r"inside", r"toleran", r"variance", r"\blimit", r"allowed", r"\bfail", r"releas",
                       r"review")),
    "yn_over_tol": ((r"price check", r"\bfail", r"on its own|by itself|alone|only at|in isolation|taken solely"),
                    (r"within", r"inside", r"toleran", r"variance", r"\blimit", r"allowed", r"\bpass", r"releas",
                     r"review")),
    "yn_price_review": ((r"price-variance review|price variance review",),
                        (r"on its own", r"\balone\b", r"price check", r"releas", r"\bhold", r"reject", r"\brout")),
}


def check_wording(text, qform: str, *, held_out: bool = False, screen: bool = False) -> list:
    """Problems of one question wording: form, G-SL (role wording), negation counts (R17 / Balance), the form's own
    must / must-not words, and the lexicon unit test (parse back with its INVOICE_ID). screen=True adds the pilot
    fix-1 rules of wording_screen (the premise rule of F1: no drive / shape / decide / settle / point to on a
    ch_price_line wording, no decision on the two price-check-on-its-own forms; and c2_kit.polarity P1-P3 with the T12
    negative predicates). The frozen pool stage ran without it (screen=False: pools_v2 stays reproducible); plugin.
    ctx_for() applies it at generation time, and a re-authoring round must pass screen=True."""
    if not isinstance(text, str) or not text.strip() or "\n" in text or text != text.strip():
        return ["empty, multi-line or padded"]
    p = []
    if not text.endswith("?"):
        p.append("not a question")
    if [x.name for x in K.placeholders(text)] != ["INVOICE_ID"] or text.count("{") != 1:
        p.append("{INVOICE_ID} exactly once and no other brace")
    if len(text.split()) > 30:
        p.append("more than 30 words")
    noun = "bill" if held_out else "invoice"
    if not re.search(rf"\b{noun} {{INVOICE_ID}}", text, re.I):
        p.append(f"'{noun} {{INVOICE_ID}}' expected")
    sk = K.make_skin("W-PROBE", FAMILY, text, {"INVOICE_ID": "id"}, kind="wording", register="question", qform=qform)
    p += [f"G-SL {v.rule}: {v.detail}" for v in gsl.lint_template(
        sk, label_words=PL.LABEL_WORDS, exceptions=PL.GSL_EXCEPTIONS, name_allow=PL.NAME_ALLOW)]
    nc = negcount.count(text)
    if (nc.k_all, nc.k_syn) != NEG_TARGET[qform]:
        p.append(f"negcount (k_all, k_syn) = {(nc.k_all, nc.k_syn)}, {qform} needs {NEG_TARGET[qform]}")
    low = text.lower()
    need, ban = _WORD_NEEDS[qform]
    p += [f"needs /{x}/" for x in need if not re.search(x, low)]
    p += [f"must not match /{x}/" for x in ban if re.search(x, low)]
    if any(o.lower() in low for o in OPTION_TEXTS) or any(c.lower() in low for c in P.CODE_WORDS):
        p.append("copies an option text or a code word")
    if screen:
        p += WS.problems(text, qform, PL)
    if not p:
        reg = LexiconRegistry(FAMILY)
        P.declare_lexicon(reg)
        try:
            f = reg.add(text, question_sem(FAMILY, qform), slots={"INVOICE_ID": "id"}, family=FAMILY)
            if not reg.unit_test(f.form_id):
                p.append(f"lexicon unit test: {f.unit_problems[:1]}")
        except LexiconError as e:
            p.append(f"lexicon: {e}")
    return p


def check_comparator(text, sem: str, kind: str) -> list:
    """Problems of one comparator paraphrase (H15): {X} once, plain endpoint words only, unit test as a lexicon form."""
    if not isinstance(text, str) or not text.strip() or "\n" in text or text != text.strip():
        return ["empty, multi-line or padded"]
    p = []
    if [x.name for x in K.placeholders(text)] != ["X"] or text.count("{") != 1:
        p.append("{X} exactly once and no other brace")
    words = _words(K.PH_RE.sub(" ", text))
    if not 1 <= len(words) <= 8:
        p.append("2-8 words")
    if re.search(r"\d", text):
        p.append("digit")
    p += [f"banned word {w!r} (H15)" for w in words if w in CMP_BANNED]
    if re.search(r"\bup to\b", text) and not re.search(r"\bup to and including\b", text):
        p.append("bare 'up to' (H15)")
    if words[:1] == ["is"]:
        p.append("starts with 'is'")
    if negcount.count(text).k_syn:
        p.append("negation other than a comparator phrase")
    if not p:
        reg = LexiconRegistry(FAMILY)
        P.declare_lexicon(reg)
        try:
            f = reg.add(text, sem, slots={"X": kind})
            if not reg.unit_test(f.form_id):
                p.append(f"lexicon unit test: {f.unit_problems[:1]}")
        except LexiconError as e:
            p.append(f"lexicon: {e}")
    return p


def check_precedence(text) -> list:
    """Problems of one precedence paraphrase (R9, H30): names the check order, no position or severity words."""
    if not isinstance(text, str) or not text.strip() or "\n" in text or text != text.strip():
        return ["empty, multi-line or padded"]
    p = []
    if "check order" not in text:
        p.append("does not name 'the check order'")
    if K.placeholders(text) or "{" in text or "}" in text:
        p.append("placeholder or brace")
    if not 8 <= len(text.split()) <= 30:
        p.append("8-30 words")
    if text.count(";") > 1 or not text.endswith("."):
        p.append("at most one semicolon; ends with a full stop")
    if text.startswith(("Check order", "If every check")):
        p.append("starts like another card line")
    low = _words(text)
    p += [f"banned word {w!r} (R9)" for w in low if w in PREC_BANNED]
    nc = negcount.count(text)
    if nc.k_all > 1 or (nc.k_all and not re.search(r"\b(do|does) not\b", text)):
        p.append("negation other than one 'do not' / 'does not'")
    if not p:
        reg = LexiconRegistry(FAMILY)
        P.declare_lexicon(reg)
        try:
            f = reg.add(text, P.PREC_SEM)
            if not reg.unit_test(f.form_id):
                p.append(f"lexicon unit test: {f.unit_problems[:1]}")
        except LexiconError as e:
            p.append(f"lexicon: {e}")
    return p


def check_attack(text, *, skin_id: str = "AT-PROBE", n_probe: int = 2, task_id: str = "probe-task",
                 prompt_sha: str = "0" * 64):
    """(attack Skin or None, problems): one line, {VENDOR} at most once, G-SL (role attack), no label word, no name,
    no money or quantity talk, then a render / parse probe as an inv partner."""
    if not isinstance(text, str) or not text.strip() or "\n" in text or text != text.strip():
        return None, ["empty, multi-line or padded"]
    p = []
    phs = K.placeholders(text)
    if any(x.name != "VENDOR" for x in phs) or len(phs) > 1:
        p.append("placeholders other than one {VENDOR}")
    if not 6 <= len(text.split()) <= 25:
        p.append("6-25 words")
    if _starts_with_head(text):
        p.append("starts with a document head")
    lit = K.PH_RE.sub(" ", text)
    p += [f"label word {w!r}" for w in _words(lit) if w in LABEL_FORMS]
    p += [f"banned word {w!r}" for w in _words(lit) if SKIN_BANNED.get(w) == "money"]
    caps = [m.group() for m in re.finditer(r"\b[A-Z][a-z]+", lit) if m.start() > 0
            and not re.search(r"[.!?:]\s*$", lit[:m.start()]) and m.group() not in PL.NAME_ALLOW]
    if caps:
        p.append(f"capitalised word(s) inside the line {caps[:3]}")
    sk = K.make_skin(skin_id, FAMILY, text, {"VENDOR": "name"} if phs else {}, kind="attack", register="note",
                     haiku_task_id=task_id, haiku_prompt_sha=prompt_sha)
    p += [f"G-SL {v.rule}: {v.detail}" for v in gsl.lint_template(
        sk, label_words=PL.LABEL_WORDS, exceptions=PL.GSL_EXCEPTIONS, name_allow=PL.NAME_ALLOW)]
    if not p and n_probe:
        p += _probe_skin(sk, n_probe)
    return (None if p else sk), p


# ================================================================================================ loading answers
def load(root: Path = ROOT, *, probe: bool = True) -> dict:
    """{task_id: {"label", "kind", "pool", "held_out", "pieces": [(piece id, value, problems)], "problems"}} for the
    answer files present under root/answers (a missing file is reported, never guessed). A piece with problems is
    dropped by the lint stage (with its reasons); pieces are not pooled or admitted here."""
    out = {}
    for label, pool, held, _per, b in build():
        tid = b.chunks[0]["task_id"]
        rec = {"label": label, "kind": b.kind, "pool": pool, "held_out": held, "pieces": [], "problems": []}
        out[tid] = rec
        f = answer_path(root, b, tid)
        if not f.is_file():
            rec["problems"].append("answer file missing")
            continue
        try:
            raw = json.loads(f.read_text(encoding="utf-8"))
        except json.JSONDecodeError as e:
            rec["problems"].append(f"answer is not JSON: {e}")
            continue
        got, probs = chunker.load_answers(b, {tid: raw})
        rec["problems"] += probs
        items = chunker.item_by_internal(b)
        for iid in sorted(got):
            rec["pieces"] += _check_answer(iid, items[iid], got[iid], held, probe=probe, task_id=tid,
                                           prompt_sha=b.prompt_sha)
    return out


def _texts(ans, k: int) -> list:
    t = ans.get("texts") if isinstance(ans, dict) else None
    return list(t)[:k] if isinstance(t, list) else []


def _check_answer(iid: str, item: dict, ans: dict, held: bool, *, probe: bool, task_id: str = "probe-task",
                  prompt_sha: str = "0" * 64) -> list:
    parts = iid.split("|")
    kind, res = parts[0], []
    hk = {"task_id": task_id, "prompt_sha": prompt_sha}
    if kind == "pack":
        pack, pr = check_pack(ans.get("pack"), parts[3], f"t12-hk-{parts[2]}", probe=4 if probe else 0)
        res.append((iid, pack or ans.get("pack"), pr))
    elif kind == "skin":
        slots = tuple(parts[3].split("+"))
        for i, t in enumerate(_texts(ans, 6)):
            res.append((f"{iid}|{i}", t, check_skin(t, parts[1], slots, held_out=held,
                                                    n_probe=4 if probe else 0, **hk)[1]))
    elif kind == "free":
        for i, t in enumerate(_texts(ans, 2)):
            res.append((f"{iid}|{i}", t, check_freeform(t, dict(item["facts"]), parts[2], held_out=held,
                                                        n_probe=3 if probe else 0, **hk)[1]))
    elif kind == "word":
        for i, t in enumerate(_texts(ans, 5)):
            res.append((f"{iid}|{i}", t, check_wording(t, parts[1], held_out=held)))
    elif kind == "cmp":
        for i, t in enumerate(_texts(ans, 10)):
            res.append((f"{iid}|{i}", t, check_comparator(t, parts[1], parts[2])))
    elif kind == "prec":
        for i, t in enumerate(_texts(ans, 10)):
            res.append((f"{iid}|{i}", t, check_precedence(t)))
    elif kind == "attack":
        for i, t in enumerate(_texts(ans, 5)):
            res.append((f"{iid}|{i}", t, check_attack(t, n_probe=2 if probe else 0, **hk)[1]))
    if not res:
        res.append((iid, ans, ["no pieces in the expected answer field"]))
    return res


def dedup_comparators(pieces: list) -> list:
    """[(piece id, text, sem, kind)] kept comparator forms with one slot kind per text (the registry refuses one text
    under two kinds): a text proposed for both kinds keeps the kind of its first piece id in sorted order."""
    seen, out = set(), []
    for pid, text, probs in sorted(pieces):
        if probs:
            continue
        _, sem, kind = pid.split("|")[:3]
        key = " ".join(text.casefold().split())
        if key in seen:
            continue
        seen.add(key)
        out.append((pid, text, sem, kind))
    return out


def summary(loaded: dict) -> dict:
    """Counts for the lint stage: per pool, pieces authored / kept / dropped, and the most common drop reasons."""
    by = {}
    reasons = {}
    for rec in loaded.values():
        c = by.setdefault(rec["pool"] + (":held" if rec["held_out"] else ""), {"tasks": 0, "missing": 0, "pieces": 0,
                                                                               "kept": 0, "dropped": 0})
        c["tasks"] += 1
        c["missing"] += "answer file missing" in rec["problems"]
        for _pid, _v, pr in rec["pieces"]:
            c["pieces"] += 1
            c["kept" if not pr else "dropped"] += 1
            for x in pr[:1]:
                k = re.sub(r"'.*", "", x)[:60]
                reasons[k] = reasons.get(k, 0) + 1
    return {"pools": by, "top_drop_reasons": dict(sorted(reasons.items(), key=lambda kv: -kv[1])[:15])}


# ================================================================================================ ambiguity record
def write_ambiguity_record(points: list) -> Path:
    """The Haiku ambiguity pass, verbatim (H1-Hn in order), next to the G0-lite spec that resolves it."""
    rec = {"family": FAMILY, "pass": PL.G0_HAIKU_TASK, "workflow": "c2-data-stage-a", "phase": "Ambiguity",
           "model": "haiku", "date": "2026-10-13", "n_points": len(points),
           "input": "families/T12/G0_SPEC.md v1 (sha256 "
                    "b913d7ec0ead8d3038130a99985bbc3a438b63784568aa67869c9e832858962f)",
           "note": "the reader's listing as relayed to the lead by the workflow; H<n> in G0 section 5 = points[n-1]",
           "resolved_in": f"G0_SPEC.md v2 section 5 (sha256 {P.G0_SHA256_AUTHORED})",
           "points": [{"h": f"H{i + 1}", **pt} for i, pt in enumerate(points)]}
    return paths.write_json(AMB_DIR / "amb_T12.json", rec)


def main(argv=None) -> int:
    args = list(sys.argv[1:] if argv is None else argv)
    cmd = args[0] if args else "write"
    if cmd == "write":
        idx = write()
        print(json.dumps({"tasks": len(idx), "items": sum(t["n_items"] for t in idx),
                          "outputs_expected": sum(t["outputs_expected"] for t in idx),
                          "index": str(ROOT / "TASKS.json")}, indent=1))
    elif cmd == "amb":
        pts = json.loads(Path(args[1]).read_text(encoding="utf-8"))
        print(write_ambiguity_record(pts))
    elif cmd == "load":
        print(json.dumps(summary(load(probe="--no-probe" not in args)), indent=1))
    else:
        print(__doc__)
        return 2
    return 0


if __name__ == "__main__":
    sys.exit(main())
