"""c2_build/families/T12/plugin.py: T12, three-way match with ordered exception precedence (C2_DATA_SPEC 3.15;
frozen G0_SPEC_v2_2.md, fix iteration 1; G0_SPEC.md v2.1 is the spec the pools were authored under).

A vendor invoice is matched against its purchase order (PO) and goods receipt under a stated AP policy of 2-4 checks:
quantity (per line, invoiced quantity <= received quantity), price (per line, invoiced unit price minus PO unit price
within a tolerance that is a percent of the PO unit price or an absolute amount per unit), duplicate (the invoice
number is not in the paid-invoice register) and approval limit (the invoice total against the approver's limit). The
checks run in a stated check order; the first check that fails decides the action (hold for receipt, price-variance
review, reject as a duplicate, route to a senior approver); an invoice that passes every check is released for
payment. Semantics: G0_SPEC_v2_2.md R1-R27 (and G0_SPEC.md resolutions H1-H30; frozen sha below). Fix iteration 1 (v2.2):
the rules of yes/no rows print from row.card (cards.place_rules), a full and a short card style, no line totals and no
dates, one-line headers, 8 cards per sampler with one pack each, stratified gold draws for ch_action / ch_price_line,
the generation-time wording screen (wording_screen.py) and a label-blind register draw.

  solver A   rules.RuleSet (policy first_match over the checks in the stated check order, default release) over a
             rule AST evaluated on decimal.Decimal amounts                                     paradigm rule_engine
  solver B   solver_b.py: its own parser of the rendered row, sqlite tables of the three documents joined by line,
             every check as an integer-cents SQL query, the check order as a ranked table      paradigm sql_sqlite
  samplers   S1 forward; S2 label-first near-miss (boundary values, look-alike register numbers); S3 ERP-export-first
             (CSV / JSON documents first, the policy as a table); S4 vendor-thread-first (narrative and invoice
             first); S5 held out (held-out registers, wordings and tolerance values; mixdev only)
  questions  ch_action (the card's actions, closed set; answer codes on ~12%); ch_price_line (which line fails the
             price check, or none); yn_release + complements yn_not_release (syntactic), yn_payment_stopped
             (antonym), yn_exception_route (option framing); yn_within_tol + yn_over_tol (antonym); yn_price_review
  relations  complement; minimal-edit twin (one received quantity, invoiced unit price, register entry or approval
             limit moved across one check's boundary; the new answer predicted from the flipped check); equiv
             (another skin, on half also another document container); inv (one pressure line); G4 metamorphic
             (rename the vendor, rename the buyer, rename the approver, reverse the line order, reverse the check order)
Construction is label-first: the target action (or the yes / no label) is a seeded draw from the row key and the
card's yes-rate; check truths are set to realise it (checks before the deciding one pass, it fails, later ones fail
only under a label-blind two-failure plan); then the documents are built to realise those truths. Every display choice
(skin, wording, slot forms, option order, answer codes, display order, document container) is a seeded draw that never
reads the gold. Three implementations agree on every spec: the construction side (integer arithmetic: targets, trap
tags, twin predictions, error models), solver A (Decimal rule engine: the gold) and solver B (sqlite on the parsed
text). The built-in packs are Claude-written placeholders (code, not data); the Haiku pack pool replaces them after
A38. Nothing in this module writes a file.
"""
from __future__ import annotations

import functools
import math
import random
from decimal import Decimal
from pathlib import Path

from c2_kit import cards as CARDS
from c2_kit import polarity as POL
from c2_kit import rules as RL
from c2_kit import skin as K
from c2_kit import slots as S
from c2_kit.distractors import build_closed, error_model, register_name, uhash
from c2_kit.plugin import C2Plugin, ContractError, KitCtx, QuestionForm, RelationProposal, Spec, choose_forms
from c2_kit.rows import TextBuilder, assemble_row
from families.T12 import wording_screen as WS

HERE = Path(__file__).resolve().parent
FAMILY = "T12"
# The sha256 of the G0-lite the Haiku task files, the pools (pools/, pools_v2/) and the extraction records were authored
# under: G0_SPEC.md, v2.1, frozen 13 Oct 2026 (kept unchanged). Their manifests record it and the pool-stage tools
# (authoring, extract_*, pool_freeze, freeze_v2, haiku/redo2) check it. The plugin's own G0_SHA256 moved with v2.2
# (G0_SPEC_v2_2.md: card text and placement, documents, length levers; fix iteration 1), which changes no pool and no
# Haiku task.
G0_SHA256_AUTHORED = "daca0538f47d7ebfe0d1442c6826cf1596ca236c98223a5c0948be3fc66b996c"

# ----------------------------------------------------------------------------------------------- closed sets (G0 R1-R3)
UNITS = {sg: (sg, pl) for sg, pl in (
    ("bag", "bags"), ("bottle", "bottles"), ("box", "boxes"), ("carton", "cartons"), ("case", "cases"),
    ("crate", "crates"), ("drum", "drums"), ("kit", "kits"), ("pack", "packs"), ("pallet", "pallets"),
    ("ream", "reams"), ("roll", "rolls"), ("set", "sets"), ("spool", "spools"), ("tube", "tubes"),
    ("unit", "units"))}
CURRENCIES = {"eur": ["EUR"], "gbp": ["GBP"], "usd": ["USD"]}
SYMBOL = {"eur": "€", "gbp": "£", "usd": "$"}
DEPTS = {"facilities": ["facilities"], "field": ["field service"], "it": ["IT support"], "lab": ["laboratory"],
         "marketing": ["marketing"], "warehouse": ["warehouse"]}
U_PCT = ("percent", "percent")

# packs (placeholder): buyer, currency, document prefixes, vendors, items (name, unit, PO unit-price band in cents),
# AP clerks, approvers. Item names hold no digit, comma, semicolon or pipe (G0 R1).
PACKS = (
    {"id": "t12-pk-lab", "org": "Halden Labs", "currency": "usd", "po": "PO", "gr": "GR", "inv": "INV",
     "vendors": ("Corran Supply", "Bellweather Scientific", "Pellham Lab Goods"),
     "items": (("nitrile gloves", "case", 900, 2600), ("pipette tips", "box", 1200, 4800),
               ("lab coats", "unit", 1800, 5200), ("sample vials", "pack", 600, 1900),
               ("bench paper", "roll", 1500, 4200), ("ethanol", "drum", 9000, 26000)),
     "clerks": ("Dana Okafor", "Lena Whitcombe", "Ravi Anand"), "approvers": ("Mira Castell", "Tomas Ferreira")},
    {"id": "t12-pk-clinic", "org": "Brookfield Clinic", "currency": "usd", "po": "PUR", "gr": "GRN", "inv": "SI",
     "vendors": ("Medlow Distribution", "Ashgrove Health Supply", "Tarrant Medical"),
     "items": (("exam table paper", "roll", 700, 2100), ("syringes", "box", 1100, 3900),
               ("gauze pads", "pack", 300, 1200), ("face masks", "case", 2500, 7800),
               ("hand sanitiser", "bottle", 400, 1500), ("scrub sets", "set", 2200, 6400)),
     "clerks": ("Priya Velasco", "Jonah Pike", "Aiko Brandt"), "approvers": ("Ines Moreau", "Kofi Mensah")},
    {"id": "t12-pk-foods", "org": "Marlowe Foods", "currency": "eur", "po": "PO", "gr": "WE", "inv": "RE",
     "vendors": ("Vandermolen Packaging", "Ostler Ingredients", "Brisa Containers"),
     "items": (("shipping cartons", "pallet", 18000, 52000), ("cane sugar", "bag", 2400, 6100),
               ("glass jars", "case", 1500, 4400), ("label rolls", "roll", 900, 2800),
               ("olive oil", "drum", 21000, 64000), ("stretch film", "roll", 1300, 3600)),
     "clerks": ("Hana Sato", "Elias Strand", "Maya Lindqvist"), "approvers": ("Omar Haddad", "Lucia Romano")},
    {"id": "t12-pk-print", "org": "Tessaro Print Works", "currency": "gbp", "po": "PO", "gr": "GR", "inv": "INV",
     "vendors": ("Kingsley Paper Mills", "Ludgate Inks", "Redfern Bindery Supply"),
     "items": (("coated paper", "ream", 450, 1400), ("black ink", "drum", 8000, 24000),
               ("binding wire", "spool", 1900, 5600), ("cover board", "pallet", 30000, 90000),
               ("plate cleaner", "bottle", 600, 1800), ("shrink sleeves", "box", 1400, 3900)),
     "clerks": ("Theo Grant", "Sara Novak", "Felix Huber"), "approvers": ("Amara Diallo", "Ken Watanabe")},
    {"id": "t12-pk-facilities", "org": "Ardent Facilities Group", "currency": "usd", "po": "PO", "gr": "RCV",
     "inv": "INV", "vendors": ("Holloway Janitorial", "Brightmere Lighting", "Castor Hardware"),
     "items": (("floor cleaner", "drum", 6000, 17000), ("light fittings", "carton", 3500, 9800),
               ("door hinges", "box", 900, 2700), ("air filters", "case", 2800, 8400),
               ("paint rollers", "pack", 700, 1900), ("cable ties", "bag", 300, 900)),
     "clerks": ("Rosa Alvarez", "Nikolai Petrov", "Grace Achebe"), "approvers": ("Leo Marchetti", "Dana Okafor")},
    {"id": "t12-pk-field", "org": "Coldwater Field Services", "currency": "eur", "po": "BE", "gr": "WE", "inv": "RG",
     "vendors": ("Hartwig Tools", "Nordmark Safety", "Ferraz Industrial"),
     "items": (("safety helmets", "box", 4500, 12000), ("hi-vis vests", "pack", 1600, 4800),
               ("tool kits", "kit", 9000, 28000), ("work gloves", "pack", 800, 2200),
               ("sealant", "tube", 300, 950), ("drill bits", "set", 1500, 4600)),
     "clerks": ("Ravi Anand", "Mira Castell", "Jonah Pike"), "approvers": ("Felix Huber", "Hana Sato")},
)

QTYS = (2, 3, 4, 5, 6, 8, 10, 12, 15, 16, 20, 24, 25, 30, 36, 40, 48, 50, 60, 72, 75, 80, 96, 100, 120, 144, 150, 180,
        200)
PCTS = (1, 3, 5)                 # training percent tolerances (G0 R5, H6)
PCTS_S5 = (2, 4)                 # held out: sampler S5 only (never a training value)
TOL_ABS = (5, 10, 15, 20, 25, 50, 75, 100, 150, 200, 250, 500)
TOL_ABS_S5 = (30, 40, 60, 120, 300)
LIMITS = (25000, 50000, 100000, 200000, 250000, 500000, 1000000, 2500000, 5000000)

# ------------------------------------------------------------------------------------------------ checks (G0 R4-R11)
CHECKS = ("qty", "price", "dup", "limit")
CHECK_NAME = {"qty": "quantity", "price": "price", "dup": "duplicate", "limit": "approval limit"}
ACTION_OF = {"qty": "hold", "price": "review", "dup": "reject", "limit": "escalate"}
CHECK_OF = {a: c for c, a in ACTION_OF.items()}
VERDICTS = ("release", "hold", "review", "reject", "escalate")
ACTION_PHRASE = {"release": "release for payment", "hold": "hold for receipt", "review": "price-variance review",
                 "reject": "reject as a duplicate", "escalate": "route to a senior approver"}
OPTION_TEXT = {"release": "Release for payment", "hold": "Hold for receipt", "review": "Send to price-variance review",
               "reject": "Reject as a duplicate", "escalate": "Route to a senior approver"}
CODE_WORDS = ("Heron", "Kestrel", "Marlin", "Osprey", "Plover")
NONE_LINE = "none"
NONE_LINE_TEXT = "None of the lines"
PREC_SEM = "prec.t12.first_failing"
CMP_SEMS = ("cmp.le", "cmp.lt")
# the family lexicon's meanings (G0 R5, R9, R17-R19; H15, H30): the closed lists G-LEX extractors choose from. The decoys
# (cmp.ge / cmp.gt, last_failing, most_severe, first_listed) are never rendered; a form read as one is rejected.
LEX_SEMS = (
    ("cmp.le", "comparator", "less than or equal to the bound"),
    ("cmp.lt", "comparator", "strictly less than the bound"),
    ("cmp.ge", "comparator", "greater than or equal to the bound"),
    ("cmp.gt", "comparator", "strictly greater than the bound"),
    (PREC_SEM, "precedence", "the first check in the stated check order that fails decides the action"),
    ("prec.t12.last_failing", "precedence", "the last check in the stated check order that fails decides the action"),
    ("prec.t12.most_severe", "precedence", "the most severe failing check decides the action"),
    ("prec.t12.first_listed", "precedence", "the failing check printed highest in the list of checks decides the "
                                            "action, whatever the stated check order"),
)
# The negative / antonym predicates of "the invoice is released for payment" and "the invoice passes the price check"
# (c2_kit.polarity rules P1-P3): a yes/no wording negates a positive predicate syntactically or uses one of these, never
# both, and its polarity must be its form's (yn_payment_stopped: stop / block; yn_over_tol: fail). Pattern list, one
# regex per predicate family.
NEGATIVE_PREDICATES = (
    r"fail(?:s|ed|ing|ure)?", r"stop(?:s|ped|ping)?", r"block(?:s|ed|ing)?", r"halt(?:s|ed|ing)?",
    r"withh(?:o|e)ld(?:s|ing)?", r"bar(?:s|red|ring)?", r"forbid(?:s|den|ding)?|forbade", r"prohibit(?:s|ed|ing)?",
    r"(?:keep|keeps|kept|keeping)\s+(?:\w+\s+){0,3}?(?:from|away|back|out)",
    r"(?:hold|holds|held|holding)\s+(?:\w+\s+){0,3}?back", r"disallow(?:s|ed|ing)?", r"declin(?:e|es|ed|ing)",
    r"refus(?:e|es|ed|ing)", r"den(?:y|ies|ied|ying)", r"reject(?:s|ed|ing)?", r"suspend(?:s|ed|ing)?",
    r"freez(?:e|es|ing)|froze(?:n)?",
)
QUESTION_MEANINGS = {
    "ch_action": "asks which action the policy gives the invoice",
    "ch_price_line": "asks which invoice line fails the price check, if any",
    "yn_release": "asks whether the invoice is released for payment",
    "yn_dneg_release": "asks whether it is not true that the invoice is not released for payment",
    "yn_not_release": "asks whether the invoice is not released for payment",
    "yn_payment_stopped": "asks whether the policy stops payment of the invoice",
    "yn_exception_route": "asks whether the invoice ends in one of the failure actions",
    "yn_within_tol": "asks whether the invoice passes the price check, taken on its own",
    "yn_over_tol": "asks whether the invoice fails the price check, taken on its own",
    "yn_price_review": "asks whether the policy sends the invoice to price-variance review",
}


def declare_lexicon(reg) -> None:
    """Declare the T12 meanings and antonym pairs in a LexiconRegistry (fixtures, and the frozen pool after A38)."""
    from c2_kit.lexicon import question_sem
    for sem, kind, meaning in LEX_SEMS:
        reg.declare(sem, kind, meaning)
    for qf, meaning in QUESTION_MEANINGS.items():
        reg.declare(question_sem(FAMILY, qf), "question", meaning)
    reg.declare_antonym(question_sem(FAMILY, "yn_release"), question_sem(FAMILY, "yn_payment_stopped"))
    reg.declare_antonym(question_sem(FAMILY, "yn_within_tol"), question_sem(FAMILY, "yn_over_tol"))

# ------------------------------------------------------------------------------------------------ card text (G0 R12)
# G0 v2.2 (pilot fix F3, spec 3.0 length): the card is built from CardItems, each a full phrasing (85% of rows) and a
# short one (15%, spec 3.0 "a short or no card on about 15% of rows"); c2_kit.cards.variant_problems keeps every slot,
# number, operator word and the negation count in the short phrasing (test_i1_fixes). Yes/no rows print the card from
# row.card (once), choice rows from the head of the instructions (cards.place_rules).
CI = CARDS.CardItem
CARD_HEADER = CI("header", "AP policy of {ORG}: each invoice gets exactly one action.",
                 short="{ORG} AP policy: each invoice gets exactly one action.")
CARD_TITLE = {
    "qty": CI("title_qty", "Quantity check", short="Quantity"),
    "price": CI("title_price", "Price check", short="Price"),
    "dup": CI("title_dup", "Duplicate check", short="Duplicate"),
    "limit": CI("title_limit", "Approval-limit check", short="Approval limit"),
}
CARD_COND = {
    "qty": CI("cond_qty", "invoiced quantity is at most received quantity on every line",
              short="invoiced quantity at most received quantity on every line"),
    "price_pct": CI("cond_price_pct", "invoiced unit price minus PO unit price is {TOL_CMP} of the PO unit price on "
                                      "every line"),
    "price_abs": CI("cond_price_abs", "invoiced unit price minus PO unit price is {TOL_CMP} on every line"),
    "dup": CI("cond_dup", "the invoice number is not in the paid-invoice register (exact match only)",
              short="invoice number not in the paid-invoice register (exact match only)"),
    "limit": CI("cond_limit", "the invoice total is {LIMIT_CMP} (limit of approver {APPROVER})",
                short="invoice total is {LIMIT_CMP} (limit of approver {APPROVER})"),
}
COND_TPL = {k: it.full for k, it in CARD_COND.items()}   # the full phrasings (the pool-stage tools build the price
#                                                          condition from COND_TPL["price_pct"], unchanged since v2.1)
CARD_RELEASE = CI("release", "If every check passes: release for payment, the only action that pays. Lower invoiced "
                             "prices always pass.",
                  short="If every check passes: release for payment, the only paying action. Lower invoiced prices "
                        "always pass.")
CARD_AMOUNTS = CI("amounts", "Amounts: {CURRENCY}, whole cents.")
CARD_ITEMS = (CARD_HEADER, *CARD_TITLE.values(), *CARD_COND.values(), CARD_RELEASE, CARD_AMOUNTS)
CARD_SHARES = {"full": 0.85, "short": 0.15}            # label-blind draw from the row key (cards.draw_style)
FAIL_TPL = "If it fails: {action}."
RULE_LIST_TPL = "{lead} {title}: {cond}. " + FAIL_TPL
RULE_TABLE_HEAD = ("| check | passes when | if it fails |", "|---|---|---|")
RULE_TABLE_TPL = "| {title} | {cond} | {action} |"
ORDER_TPL = "Check order: {names}."
CODES_TPL = "Answer codes: {pairs}."
CLOSED_WORLD = "Nothing else applies: the policy and the documents shown are complete."

# ------------------------------------------------------------------------------------------------ documents (G0 R14)
# (head, line ("#" = the line number), foot); every value is a slot placeholder. G0 v2.2: no line totals are printed
# (no check reads one; the document totals stay), the receipt and the invoice repeat no vendor or PO number except the
# invoice's PO number (identity holds by construction, R1).
DOC_KV = {
    "po": ("Purchase order {PO_ID} from {VENDOR}",
           "- line #: {ITEM_#}; {PO_Q_#} at {PO_P_#}",
           "- order total: {PO_TOTAL}"),
    "gr": ("Goods receipt {GR_ID}",
           "- line #: received {RCV_Q_#}", None),
    "inv": ("Invoice {INVOICE_ID} for purchase order {PO_ID}",
            "- line #: {ITEM_#}; {INV_Q_#} at {INV_P_#}",
            "- invoice total: {INV_TOTAL}"),
}
DOC_TABLE = {
    "po": ("Purchase order {PO_ID} | vendor {VENDOR}\n"
           "| line | item | quantity | unit price |\n|---|---|---|---|",
           "| # | {ITEM_#} | {PO_Q_#} | {PO_P_#} |", "| total | | | {PO_TOTAL} |"),
    "gr": ("Goods receipt {GR_ID}\n| line | received |\n"
           "|---|---|", "| # | {RCV_Q_#} |", None),
    "inv": ("Invoice {INVOICE_ID} | purchase order {PO_ID}\n"
            "| line | item | quantity | unit price |\n|---|---|---|---|",
            "| # | {ITEM_#} | {INV_Q_#} | {INV_P_#} |", "| total | | | {INV_TOTAL} |"),
}
DOC_CSV = {
    "po": ("Purchase order export, po_number {PO_ID}, vendor {VENDOR}\n"
           "line,item,quantity,unit_price",
           "#,{ITEM_#},{PO_Q_#:plain},{PO_P_#:nocomma}", "total,,,{PO_TOTAL:nocomma}"),
    "gr": ("Goods receipt export, gr_number {GR_ID}\n"
           "line,received", "#,{RCV_Q_#:plain}", None),
    "inv": ("Invoice export, invoice_number {INVOICE_ID}, po_number {PO_ID}\nline,item,quantity,unit_price",
            "#,{ITEM_#},{INV_Q_#:plain},{INV_P_#:nocomma}", "total,,,{INV_TOTAL:nocomma}"),
}
JSON_HEAD = {"po": "Purchase order (JSON):", "gr": "Goods receipt (JSON):", "inv": "Invoice (JSON):",
             "reg": "Paid-invoice register (JSON):"}
JSON_DOC = {   # minified (no space after "," or ":"): valid JSON, about 20% fewer tokens (G0 v2.2 R14)
    "po": '{"po_number":{PO_ID},"vendor":{VENDOR},"lines":[%s],"total_cents":{PO_TOTAL:int_cents}}',
    "gr": '{"gr_number":{GR_ID},"lines":[%s]}',
    "inv": '{"invoice_number":{INVOICE_ID},"po_number":{PO_ID},"lines":[%s],"total_cents":{INV_TOTAL:int_cents}}',
}
JSON_LINE = {
    "po": '{"line":#,"item":{ITEM_#},"quantity":{PO_Q_#:plain},"unit_price_cents":{PO_P_#:int_cents}}',
    "gr": '{"line":#,"received":{RCV_Q_#:plain}}',
    "inv": '{"line":#,"item":{ITEM_#},"quantity":{INV_Q_#:plain},"unit_price_cents":{INV_P_#:int_cents}}',
}
ORDERS = {"narrative_first": ("narrative", "po", "gr", "inv", "reg"),
          "docs_first": ("po", "gr", "inv", "reg", "narrative"),
          "thread_first": ("narrative", "inv", "reg", "po", "gr")}
SKIN_REGISTERS = {"S3": ("json", "log", "yaml"), "S4": ("chat", "email", "transcript"), "S5": ("portal", "voicemail")}
# S1 / S2 draw their register with these weights (label-blind, from the row key) so that every training register is 12.5%
# of the family (spec 3.0: each register <= 15%): S3 and S4 already give json / log / yaml and chat / email / transcript
# 8.3% each, so memo and ticket, which only S1 / S2 can use, carry 25% of those two samplers and the other six 8.3%.
# Low-discrepancy steps over the seed (Kronecker sequences, a hash phase per coordinate): the golden ratio for the question
# form (shares exact over consecutive seeds, R20) and sqrt(2) - 1 for the skin register (R21). The skin inside its register
# and the question wording are picked round-robin over a block of seeds (_block_members / _pick_rr), not by a step.
WEYL = 0.6180339887498949
REGISTER_STEP = 0.41421356237309503
FREE_REGISTER_W = (("memo", 0.25), ("ticket", 0.25), ("chat", 1 / 12), ("email", 1 / 12), ("transcript", 1 / 12),
                   ("log", 1 / 12), ("yaml", 1 / 12), ("json", 1 / 12))
DOC_FMTS = {"S3": ("csv", "json"), "S4": ("kv",)}
EQUIV_FMT = {"kv": "table", "table": "kv", "csv": "json", "json": "csv"}

# ---------------------------------------------------------------------------------------------- questions (G0 R15-R20)
QFORM_SHARES = (("ch_action", 0.45), ("ch_price_line", 0.10), ("yn_release", 0.115), ("yn_dneg_release", 0.035),
                ("yn_payment_stopped", 0.055), ("yn_not_release", 0.035), ("yn_within_tol", 0.07), ("yn_over_tol", 0.04),
                ("yn_price_review", 0.10))          # G0 v2.2 R20: yes/no 45% of base specs (was 42%): length, spec 3.0
NOT_RELEASE = ("escalate", "hold", "reject", "review")
YES_VERDICTS = {"yn_release": ("release",), "yn_dneg_release": ("release",), "yn_not_release": NOT_RELEASE,
                "yn_payment_stopped": NOT_RELEASE, "yn_exception_route": NOT_RELEASE, "yn_price_review": ("review",)}
PRICE_FORMS = {"yn_within_tol": False, "yn_over_tol": True}       # yes iff (the price check fails) == value
# complement partner of each yes/no base form (same predicate, opposite polarity); syntactic pairs differ by one cue
COMPLEMENTS = {"yn_release": (("yn_not_release", 0.30), ("yn_payment_stopped", 0.35), ("yn_exception_route", 0.35)),
               "yn_dneg_release": (("yn_not_release", 1.0),),
               "yn_payment_stopped": (("yn_release", 1.0),),
               "yn_not_release": (("yn_release", 0.5), ("yn_dneg_release", 0.5)),
               "yn_within_tol": (("yn_over_tol", 1.0),),
               "yn_over_tol": (("yn_within_tol", 1.0),)}
COMPLEMENT_RATE = {"yn_release": 0.65, "yn_dneg_release": 0.65, "yn_payment_stopped": 0.65, "yn_not_release": 0.65,
                   "yn_within_tol": 0.55, "yn_over_tol": 0.55}

N_CARDS = 8                # per training sampler (G0 v2.2; was 16): 32 training cards, one pack each (spec 3.0)
N_CARDS_S5 = 10
TRIES = 200
LINES_W = ((1, 0.30), (2, 0.35), (3, 0.22), (4, 0.13))   # G0 v2.2 R1: PO lines 1-4 (was 16 / 42 / 28 / 14%): length
TRAIN_SAMPLERS = ("S1", "S2", "S3", "S4")
BLOCK = 4096               # seeds per stratification block (G0 v2.2 R15, R16): in any run of consecutive seeds inside a
#                            block, each outcome of a stratum is the gold of ch_action / ch_price_line rows +- 1 times
DUP_P = 0.4                # the duplicate check is on the card (G0 v2.2 R8; was 50%)
LIMIT_P = 0.4              # the approval-limit check is on the card (G0 v2.2 R8; was 50%)
TWO_FAIL_P = 0.52          # label-blind plan: checks after the deciding one may fail too (trap two_fail)
TWO_FAIL_LATER = 0.6
MATCH_P = 0.50             # label-blind plan on >= 2-line rows: the invoice bills the PO quantities, totals equal
SHORTFALL_OK_P = 0.60      # a passing line with a receipt shortfall, billed at what was received
OVERBILL_P = 0.35          # a failing quantity line billed above the ordered (= received) quantity
# ch_price_line (G0 v2.2 R16): the gold is "None of the lines" with probability 1 / (n + 1) for n PO lines (a label-blind
# draw from the row key), else the one line that fails the price check, uniform over the lines: every option of the
# k = n + 1 shown is gold 1 / k of the time, so no option text carries a prior (was 25% none: a "none" whose gold share
# differs from 1 / k is the leak of the Stage B patterns; for one line the item was gold 75% of the time).
TWIN_RATE = 0.50           # G0 v2.2 R24 (was 42%): twin rows 20-25% of the family at the new rows-per-unit
EQUIV_RATE = 0.14          # G0 v2.2 R24 (was 11%): equiv rows 5-10%
INV_RATE = 0.06

ERROR_TEXT = {
    "t12_reverse_order": "takes the last failing check in the stated check order instead of the first",
    "t12_price_first": "reports the price variance whenever the price check fails, whatever the check order",
    "t12_totals_only": "releases the invoice because its total equals the PO total, without checking the lines",
    "t12_ordered_not_received": "compares the invoiced quantity with the ordered quantity, not the received quantity",
    "t12_invoice_price_base": "takes the percentage tolerance of the invoiced unit price instead of the PO unit price",
    "t12_line_total_base": "applies the price tolerance to the line total instead of the unit price",
    "t12_two_sided_tolerance": "treats an invoiced unit price below the PO unit price by more than the tolerance as a "
                               "variance too",
    "t12_near_miss_duplicate": "counts a register number that differs by one digit or one swap as the invoice number",
    "t12_limit_on_po_total": "compares the PO total instead of the invoice total with the approval limit",
    "t12_line_by_line": "scans the invoice line by line and reports the first problem on the earliest line",
}
for _n, _d in ERROR_TEXT.items():
    register_name(_n, _d)
ERROR_NAMES = ("first_failure_only", "drop_inclusive_endpoint", "add_exclusive_endpoint") + tuple(ERROR_TEXT)


def _pct_of(price: Decimal, pct) -> Decimal:
    return price * Decimal(pct) / Decimal(100)


def _line_amount(qty, price: Decimal) -> Decimal:
    return Decimal(qty) * price


for _fn_name, _fn in (("t12_pct_of", _pct_of), ("t12_line_amount", _line_amount)):
    if _fn_name not in RL.FNS:                # idempotent across re-imports
        RL.register_fn(_fn_name, _fn)


@functools.lru_cache(maxsize=None)
def _rate(sampler: str, card_idx: int, n: int) -> float:
    """Per-card gold-yes rate, spread evenly over 20-80% (family mean exactly 50%)."""
    order = sorted(range(n), key=lambda i: uhash(FAMILY, "rate", sampler, i))
    return 0.2 + 0.6 * (order.index(card_idx) + 0.5) / n


def _card_idx_of(seed: int, sampler: str) -> int:
    """The card index of a seed: the first draw of the row's rng (as in T12Plugin.sample), a pure function of the seed."""
    return random.Random(f"{FAMILY}|{sampler}|{seed}").randrange(N_CARDS_S5 if sampler == "S5" else N_CARDS)


@functools.lru_cache(maxsize=16)
def _yes_table(samplers: tuple, b0: int) -> dict:
    """{(seed, sampler): gold yes} of the yes/no base rows of the block [b0, b0 + BLOCK): a label-first draw stratified by
    (question form, card), by deterministic error diffusion over the seeds in (seed, sampler) order (a pure function of
    the seeds, so stateless). A row of card c with rate r (_rate, 20-80%) is yes iff the card's running deficit
    A = r (n_c + 1) - yes_c - o_c plus the form's running deficit B = 0.5 (N + 1) - Y - o_f (N, Y: the rows and
    yes of the form on the sampler so far) is positive; o_c, o_f are seeded offsets in [0, 1). Each card keeps its rate
    (+- 1 per stratum, shifted by at most a few pp by the form term, inside 20-80%) and every question form's yes rate
    on every sampler is 50% to within +- 1 row per consecutive run, whatever the mix of cards the seeds drew, so the
    form carries no prior (G6: a question-only reader learned the form's i.i.d. yes rate, which varied 0.458-0.550).
    Label-blind: only seeds and hashes are read; solver A confirms the gold."""
    out: dict = {}
    card_n: dict = {}
    card_y: dict = {}
    form_n: dict = {}
    form_y: dict = {}
    for s in range(b0, b0 + BLOCK):
        for smp in samplers:
            q = T12Plugin._qform_of(s, smp)
            if q in ("ch_action", "ch_price_line"):
                continue
            n_cards = N_CARDS_S5 if smp == "S5" else N_CARDS
            idx = _card_idx_of(s, smp)
            ck, fk = (q, smp, idx), (q, smp)
            a = (_rate(smp, idx, n_cards) * (card_n.get(ck, 0) + 1) - card_y.get(ck, 0)
                 - uhash(FAMILY, "yes-off", b0, q, smp, idx))
            b = 0.5 * (form_n.get(fk, 0) + 1) - form_y.get(fk, 0) - uhash(FAMILY, "yes-offf", b0, q, smp)
            yes = a + b > 0
            out[(s, smp)] = yes
            card_n[ck] = card_n.get(ck, 0) + 1
            card_y[ck] = card_y.get(ck, 0) + int(yes)
            form_n[fk] = form_n.get(fk, 0) + 1
            form_y[fk] = form_y.get(fk, 0) + int(yes)
    return out


def _near_variants(num: str) -> list:
    """Look-alike invoice numbers (G0 R6): one adjacent swap or one changed digit, same prefix and length."""
    pre, digits = num.rsplit("-", 1)
    out = []
    for i in range(len(digits) - 1):
        if digits[i] != digits[i + 1]:
            d = digits[:i] + digits[i + 1] + digits[i] + digits[i + 2:]
            if d[0] != "0":
                out.append(f"{pre}-{d}")
    for i, ch in enumerate(digits):
        for x in "0123456789":
            if x != ch and not (i == 0 and x == "0"):
                out.append(f"{pre}-{digits[:i]}{x}{digits[i + 1:]}")
    return sorted(set(out))


def _is_near(a: str, b: str) -> bool:
    if a == b or len(a) != len(b):
        return False
    diff = [i for i in range(len(a)) if a[i] != b[i]]
    return len(diff) == 1 or (len(diff) == 2 and diff[1] == diff[0] + 1 and a[diff[0]] == b[diff[1]]
                              and a[diff[1]] == b[diff[0]])


def _verdicts(checks) -> list:
    """The card's actions in canonical order: release + one per check on the card (G0 R10)."""
    return ["release"] + [ACTION_OF[c] for c in CHECKS if c in checks]


def _first_failing(order, truths: dict) -> str:
    return next((ACTION_OF[c] for c in order if truths[c]), "release")


def _answer(qform: str, verdict: str, price_lines: list, items: list):
    if qform == "ch_action":
        return verdict
    if qform == "ch_price_line":
        if len(price_lines) > 1:
            raise ContractError("ch_price_line needs at most one line that fails the price check")
        return items[price_lines[0]] if price_lines else NONE_LINE
    if qform in PRICE_FORMS:
        return int(bool(price_lines) == PRICE_FORMS[qform])
    return int(verdict in YES_VERDICTS[qform])


@functools.lru_cache(maxsize=16)
def _block_members(samplers: tuple, b0: int) -> dict:
    """{stratum: {(seed, sampler): rank}} over the block [b0, b0 + BLOCK) of the given samplers jointly, ranks in
    (seed, sampler) order. Strata: ("ch_action", check set), ("ch_price_line", line count) for the stratified golds
    (T12Plugin._outcome), ("reg", register) for the round-robin skin and ("qform", question form) for the round-robin
    wording (T12Plugin._pick_rr). A pure function of the seeds."""
    lists: dict = {}
    for s in range(b0, b0 + BLOCK):
        for smp in samplers:
            q = T12Plugin._qform_of(s, smp)

            if q == "ch_action":
                lists.setdefault((q, T12Plugin._extras_of(s, smp)), []).append((s, smp))
            elif q == "ch_price_line":
                lists.setdefault((q, T12Plugin._lines_of(s, smp)), []).append((s, smp))
            lists.setdefault(("qform", q), []).append((s, smp))
            lists.setdefault(("reg", T12Plugin._register_of(s, smp)), []).append((s, smp))
    return {k: {pair: i for i, pair in enumerate(v)} for k, v in lists.items()}


class T12Plugin(C2Plugin):
    FAMILY = FAMILY
    TIER = "everyday"
    G0_LITE = HERE / "G0_SPEC_v2_2.md"
    G0_SHA256 = "65892dd9a9561c20ca8c418353eb4f3f01094160c527e942fdfeff16f6e482c6"   # frozen v2.2 (re-frozen in fix iteration 2: R20 yes draw; was da876f58...); v2.1 = G0_SPEC.md (G0_SHA256_AUTHORED)
    G0_HAIKU_TASK = "c2-data-stage-a/amb:T12"     # the one Haiku ambiguity pass (30 points; G0 section 5)
    SAMPLERS = ("S1", "S2", "S3", "S4", "S5")
    HELD_OUT_SAMPLERS = ("S5",)
    PARADIGM_A = "rule_engine"
    PARADIGM_B = "sql_sqlite"
    SOLVER_B_MODULE = "families.T12.solver_b"
    QFORMS = {q.qform: q for q in (
        QuestionForm("ch_action", "choice", answer_set="closed"),
        QuestionForm("ch_price_line", "choice", answer_set="closed"),
        QuestionForm("yn_release", "noul", "released", 1, yes_is_bad=False),
        QuestionForm("yn_dneg_release", "noul", "released", 1, yes_is_bad=False),
        QuestionForm("yn_not_release", "noul", "released", -1, "syntactic", yes_is_bad=True),
        QuestionForm("yn_payment_stopped", "noul", "released", -1, "antonym", yes_is_bad=True),
        QuestionForm("yn_exception_route", "noul", "released", -1, "option_framing", yes_is_bad=True),
        QuestionForm("yn_within_tol", "noul", "price_ok", 1, yes_is_bad=False),
        QuestionForm("yn_over_tol", "noul", "price_ok", -1, "antonym", yes_is_bad=True),
        QuestionForm("yn_price_review", "noul", "price_review", 1, yes_is_bad=True),
    )}
    LABEL_WORDS = ("release", "hold", "review", "reject", "duplicate", "escalate", "variance", "approve", "approval",
                   "tolerance", "senior approver", "price-variance review")
    CLOSED_WORLD_SENTENCE = CLOSED_WORLD
    REGISTERS = ("memo", "email", "chat", "ticket", "json", "log", "transcript", "yaml", "portal", "voicemail")
    HELD_OUT_REGISTERS = ("portal", "voicemail")
    GSL_EXCEPTIONS: dict = {}
    NAME_ALLOW = ("AP", "ERP", "PO")
    POLARITY_CHECK = True                 # c2_kit.polarity P1-P3 on every yes/no wording (screened in ctx_for)
    POLARITY_NEGATIVES = NEGATIVE_PREDICATES

    def __init__(self, lexicon=None):
        super().__init__(lexicon)
        self._forms_cache: dict = {}
        self._screened: list = []                  # [(ctx, screened ctx, {wording skin id: problems})]

    # ------------------------------------------------------------------------------------------- lexicon draws
    def _form_ids(self, sem: str, kind: str | None = None) -> list:
        if self.lexicon is None:
            raise ContractError("T12 needs its lexicon registry (T12Plugin(lexicon=...))")
        key = (sem, kind)
        if key not in self._forms_cache:
            self._forms_cache[key] = sorted(
                fid for fid, f in self.lexicon.forms.items() if f.sem_id == sem and self.lexicon.status(fid) ==
                "admitted" and (kind is None or dict(f.slots).get("X") == kind))
        ids = self._forms_cache[key]
        if not ids:
            raise ContractError(f"no admitted lexicon form for {sem} ({kind})")
        return ids

    # ------------------------------------------------------------------------------------------- spec accessors
    @staticmethod
    def _n(spec: Spec) -> int:
        return spec.structure["n"]

    def _items(self, spec: Spec) -> list:
        return [spec.slots[f"ITEM_{i}"].value for i in range(1, self._n(spec) + 1)]

    @staticmethod
    def _regs(spec: Spec) -> list:
        return [spec.slots[f"REG_{j}"].value for j in range(1, 5) if f"REG_{j}" in spec.slots]

    @staticmethod
    def _money(spec: Spec) -> tuple:
        s = spec.slots["PO_P_1"]
        return s.param("currency"), s.param("symbol")

    def _lines(self, spec: Spec) -> list:
        v = spec.env()
        return [{"po_q": v[f"PO_Q_{i}"], "po_p": v[f"PO_P_{i}"], "rcv": v[f"RCV_Q_{i}"], "inv_q": v[f"INV_Q_{i}"],
                 "inv_p": v[f"INV_P_{i}"]} for i in range(1, self._n(spec) + 1)]

    def _tols(self, spec: Spec) -> list:
        """Per-line tolerance in cents (percent cards: whole cents by construction, G0 R5)."""
        v = spec.env()
        if spec.structure["tol_kind"] == "pct":
            return [x["po_p"] * v["TOL_PCT"] // 100 for x in self._lines(spec)]
        return [v["TOL_AMT"]] * self._n(spec)

    # ------------------------------------------------------------------------------------------- sampling
    def sample(self, seed: int, sampler: str) -> Spec:
        if sampler not in self.SAMPLERS:
            raise ContractError(f"sampler {sampler}")
        rng = random.Random(f"{FAMILY}|{sampler}|{seed}")
        qform = self._qform_of(seed, sampler)
        n_cards = N_CARDS_S5 if sampler == "S5" else N_CARDS
        idx = rng.randrange(n_cards)
        card = self._draw_card(sampler, idx, n_cards)
        h = lambda name: uhash(FAMILY, name, sampler, seed)   # noqa: E731
        has_dup, has_limit = self._extras_of(seed, sampler)
        checks = ["qty", "price"] + (["dup"] if has_dup else []) + (["limit"] if has_limit else [])
        order = rng.sample(checks, len(checks))
        aligned = h("display") < (0.4 if sampler == "S2" else 0.6)
        display = list(order) if aligned else rng.sample(checks, len(checks))
        style = "table" if card["rule_fmt"] == "table" else ("numbered" if aligned else "bulleted")
        codes = None
        if qform == "ch_action" and h("masked") < 0.12:
            codes = sorted(CODE_WORDS, key=lambda w: uhash(FAMILY, "code", sampler, seed, w))[:len(checks) + 1]
        n = self._lines_of(seed, sampler)
        sems = {"tol": rng.choice(CMP_SEMS), "limit": rng.choice(CMP_SEMS)}
        pct = rng.choice(PCTS_S5 if sampler == "S5" else PCTS) if card["tol_kind"] == "pct" else None
        plan = self._plan(seed, sampler, n)
        strat = self._outcome(seed, sampler, qform, checks, n)          # ch_action / ch_price_line: balanced in a block
        target, forced = self._target(seed, qform, sampler, idx, n_cards, checks, order, strat)
        st = {"n": n, "checks": order, "display": display, "style": style, "doc_fmt": card["doc_fmt"],
              "blocks": card["blocks"], "tol_kind": card["tol_kind"], "codes": codes,
              "card_style": CARDS.draw_style(f"{FAMILY}|{sampler}|{seed}", CARD_SHARES)}
        for _ in range(TRIES):
            truths = self._truths(rng, order, target, forced, plan)
            vals = self._values(rng, sampler, card, n, pct, sems, checks, truths, plan, qform,
                                strat if qform == "ch_price_line" and strat != NONE_LINE else None)
            if vals is None:
                continue
            spec = self._assemble(seed, sampler, qform, card, st, vals, pct, sems, rng)
            verdict, pf, t = self._judge(spec)
            if {c: t[c] for c in checks} != truths or verdict != target:
                continue
            if qform == "ch_price_line" and len(pf) > 1:
                continue
            want = _answer(qform, verdict, pf, self._items(spec))
            got = self.solve_a(spec)
            if got != want:
                raise ContractError(f"construction gives {want!r} but solver A gives {got!r} (seed {seed})")
            return spec
        raise ContractError(f"no {target} construction (seed {seed}, {sampler}, {qform})")

    # ------------------------------------------------------------------------------------------- seed-level draws
    @staticmethod
    def _qform_of(seed: int, sampler: str) -> str:
        """The question form of a seed: a low-discrepancy step (shares exact over consecutive seeds)."""
        u = ((seed + 1) * WEYL + uhash(FAMILY, "qform", sampler)) % 1.0
        acc = 0.0
        for q, share in QFORM_SHARES:
            acc += share
            if u < acc:
                return q
        return QFORM_SHARES[-1][0]

    @staticmethod
    def _extras_of(seed: int, sampler: str) -> tuple:
        """(duplicate check on the card, approval-limit check on the card): independent seeded draws (G0 R8)."""
        return (uhash(FAMILY, "dup", sampler, seed) < DUP_P, uhash(FAMILY, "limit", sampler, seed) < LIMIT_P)

    @staticmethod
    def _lines_of(seed: int, sampler: str) -> int:
        """The number of PO lines of a seed (G0 R1 weights), a seeded draw."""
        u, acc = uhash(FAMILY, "nlines", sampler, seed), 0.0
        for k, w in LINES_W:
            acc += w
            if u < acc:
                return k
        return LINES_W[-1][0]

    def _outcome(self, seed: int, sampler: str, qform: str, checks: list, n: int):
        """ch_action: the gold action; ch_price_line: NONE_LINE or the index of the one failing line; else None. A
        label-first draw from the seed, balanced exactly (+- 1) within the block of BLOCK consecutive seeds of the sampler
        for every stratum (ch_action: the card's check set, so each action is gold 1 / k; ch_price_line: the line count,
        so none and every line are gold 1 / (n + 1)): the sample of a pilot is then not unbalanced by chance, which an
        options-only reader would learn (Stage B patterns; G6). Label-blind: only seeds and hashes are read, and the
        outcome is the gold by construction (solver A confirms it)."""
        if qform == "ch_action":
            g, outcomes = self._extras_of(seed, sampler), sorted(_verdicts(checks))
        elif qform == "ch_price_line":
            g, outcomes = n, [NONE_LINE] + list(range(n))
        else:
            return None
        b0 = seed - seed % BLOCK
        group = TRAIN_SAMPLERS if sampler in TRAIN_SAMPLERS else (sampler,)   # the training samplers share one sequence
        rank = _block_members(group, b0)[(qform, g)][(seed, sampler)]
        perm = sorted(outcomes, key=lambda o: uhash(FAMILY, "stratum", b0, qform, repr(g), repr(o)))
        return perm[rank % len(perm)]

    @staticmethod
    def _yes_of(seed: int, sampler: str, qform: str, idx: int, n_cards: int) -> bool:
        """The gold yes of a yes/no base row (see _yes_table): label-first, stratified by (question form, card)."""
        b0 = seed - seed % BLOCK
        group = TRAIN_SAMPLERS if sampler in TRAIN_SAMPLERS else (sampler,)
        return _yes_table(group, b0)[(seed, sampler)]

    def _draw_card(self, sampler: str, idx: int, n_cards: int) -> dict:
        si = "S12345".index(sampler[1])
        rank = sorted(range(n_cards), key=lambda i: uhash(FAMILY, "tolkind", sampler, i)).index(idx)
        fmts = DOC_FMTS.get(sampler, ("kv", "table"))
        # one pack per card (spec 3.0; pilot F2): the global card number si * N_CARDS + idx (S5: 32..41, disjoint from
        # the 32 training cards) indexes the pack list, so 32 training cards use 32 distinct packs
        return {"id": f"{FAMILY}:{sampler}:c{idx:02d}", "idx": idx,
                "pack": PACKS[((si - 1) * N_CARDS + idx) % len(PACKS)],
                "tol_kind": "pct" if rank < n_cards // 2 else "abs", "doc_fmt": fmts[idx % len(fmts)],
                "rule_fmt": "table" if sampler == "S3" else "list",
                "blocks": {"S3": "docs_first", "S4": "thread_first"}.get(sampler, "narrative_first")}

    @staticmethod
    def _plan(seed: int, sampler: str, n: int) -> dict:
        """Label-blind construction plans (seeded from the row key, never from the target)."""
        h = lambda name: uhash(FAMILY, "plan", name, sampler, seed)   # noqa: E731
        s2 = sampler == "S2"
        return {"boundary": h("bnd") < (0.65 if s2 else 0.22), "at_tol": h("attol") < (0.5 if s2 else 0.28),
                "two_fail": h("two") < TWO_FAIL_P, "match": n >= 2 and h("match") < MATCH_P,
                "near_dup": h("near") < (0.7 if s2 else 0.35)}

    def _target(self, seed, qform, sampler, idx, n_cards, checks, order, strat) -> tuple:
        """(target action, forced check truths): ch_action uniform over the card's actions; yes / no from the card's
        yes-rate; yn_within_tol and ch_price_line draw the price check's own truth (G0 R20)."""
        verdicts = _verdicts(checks)
        u = uhash(FAMILY, "target", sampler, seed)

        def pick(pool):
            pool = sorted(pool)
            return pool[min(len(pool) - 1, int(u * len(pool)))]

        if qform == "ch_action":
            return strat, {}
        if qform == "ch_price_line":
            yes = strat == NONE_LINE                                          # "yes" = the price check passes: none
        else:
            yes = self._yes_of(seed, sampler, qform, idx, n_cards)
        if qform in YES_VERDICTS and qform != "yn_price_review":          # predicate "released" (any polarity)
            released = yes == ("release" in YES_VERDICTS[qform])
            return ("release" if released else pick(v for v in verdicts if v != "release")), {}
        if qform == "yn_price_review":
            return ("review" if yes else pick(v for v in verdicts if v != "review")), {}
        if qform in PRICE_FORMS and PRICE_FORMS[qform]:                 # yn_over_tol: "yes" = the check fails
            yes = not yes
        if yes:
            return pick(v for v in verdicts if v != "review"), {"price": False}
        before = order[:order.index("price")]
        return pick(["review"] + [ACTION_OF[c] for c in before]), {"price": True}

    @staticmethod
    def _truths(rng, order, target, forced, plan) -> dict:
        """Check truths (True = fails) that realise the target under first-failing precedence (G0 R9)."""
        pos = len(order) if target == "release" else order.index(CHECK_OF[target])
        t = {}
        for k, c in enumerate(order):
            if k < pos:
                t[c] = False
            elif k == pos:
                t[c] = True
            elif c in forced:
                t[c] = forced[c]
            else:
                t[c] = plan["two_fail"] and rng.random() < TWO_FAIL_LATER
        if any(t[c] != x for c, x in forced.items()):
            raise ContractError("a forced check truth contradicts the target")
        return t

    # ------------------------------------------------------------------------------------------- values
    def _values(self, rng, sampler, card, n, pct, sems, checks, truths, plan, qform, pline=None):
        pack = card["pack"]
        items = rng.sample(pack["items"], n)
        step = 100 // math.gcd(pct, 100) if pct else 1
        po_q, po_p = [], []
        for _name, _unit, lo, hi in items:
            po_q.append(rng.choice(QTYS) if rng.random() < 0.7 else rng.randint(2, 200))
            p = rng.randint(lo, hi)
            po_p.append(max(step, p - p % step))
        if pct:
            tol, tols = pct, [p * pct // 100 for p in po_p]
        else:
            table = TOL_ABS_S5 if sampler == "S5" else TOL_ABS
            lo_p = min(po_p)
            cands = [t for t in table if 0.008 * lo_p <= t <= 0.04 * lo_p] or [
                min(table, key=lambda t: abs(t - 0.02 * lo_p))]
            tol = rng.choice(cands)
            tols = [tol] * n
        le = sems["tol"] == "cmp.le"
        max_pass = [t if le else t - 1 for t in tols]
        first_fail = [t + 1 if le else t for t in tols]
        cap = [max(1, p * 5 // 100) for p in po_p]
        match = plan["match"]
        # quantities (G0 R4): a failing line bills more than was received; passing lines bill at most the receipt
        f_q = set()
        if truths["qty"]:
            f_q = set(rng.sample(range(n), 2 if n >= 2 and rng.random() < 0.2 else 1))
        rcv_q, inv_q = [], []
        for i, q in enumerate(po_q):
            if i in f_q and not match and rng.random() < OVERBILL_P:
                r, inv = q, q + (1 if plan["boundary"] else rng.randint(1, 3))     # billed above the PO quantity
            elif i in f_q:
                r = q - min(q - 1, rng.choice((1, 1, 2, 3)))
                inv = r + 1 if (plan["boundary"] and not match and rng.random() < 0.6) else q
            elif match:
                r, inv = q, q
            elif rng.random() < SHORTFALL_OK_P:
                r = q - min(q - 1, rng.choice((1, 2, 3)))
                inv = r if rng.random() < 0.85 else max(1, r - rng.randint(1, 2))
            else:
                r = q
                inv = q if rng.random() < 0.9 else q - rng.randint(1, min(3, q - 1))
            rcv_q.append(r)
            inv_q.append(inv)
        # unit prices (G0 R5): failing lines above the tolerance, passing lines at, below or within it
        f_p = set()
        if truths["price"]:
            two = n >= 2 and not match and qform != "ch_price_line" and rng.random() < 0.15
            f_p = {pline} if pline is not None else set(rng.sample(range(n), 2 if two else 1))
        if match:
            delta = self._match_deltas(rng, po_q, po_p, f_p, max_pass, first_fail, tols, cap, plan, le)
            if delta is None:
                return None
        else:
            delta = [0] * n
            exact = None
            if plan["at_tol"]:
                cand = [i for i in range(n) if (i in f_p) != le]     # le: an exact line passes; lt: it fails
                exact = rng.choice(cand) if cand else None
            for i in range(n):
                if i == exact:
                    delta[i] = tols[i]
                elif i in f_p:
                    delta[i] = (first_fail[i] if plan["boundary"]
                                else rng.randint(first_fail[i], max(first_fail[i], cap[i])))
                else:
                    u = rng.random()
                    if u < 0.25 or (u >= 0.5 and max_pass[i] < 1):
                        d = 0
                    elif u < 0.5:
                        d = -rng.randint(1, cap[i])
                    else:
                        d = max_pass[i] if plan["boundary"] else rng.randint(1, max_pass[i])
                    delta[i] = d
        inv_p = [p + d for p, d in zip(po_p, delta)]
        if min(inv_p) < 1:
            return None
        # duplicate (G0 R6): register entries of the same vendor, look-alikes by a label-blind plan
        inv_no = f"{pack['inv']}-{rng.randrange(10000, 100000)}"
        reg = None
        if "dup" in checks:
            m = rng.choice((2, 3, 4))
            reg = []
            while len(reg) < m:
                x = f"{pack['inv']}-{rng.randrange(10000, 100000)}"
                if x != inv_no and not _is_near(x, inv_no) and x not in reg:
                    reg.append(x)
            free = list(range(m))
            if truths["dup"]:
                j = rng.randrange(m)
                reg[j] = inv_no
                free.remove(j)
            if plan["near_dup"]:
                alt = [x for x in _near_variants(inv_no) if x not in reg]
                reg[rng.choice(free)] = rng.choice(alt)
        # approval limit (G0 R7) on the invoice total
        total = sum(q * p for q, p in zip(inv_q, inv_p))
        limit = None
        if "limit" in checks:
            le_l, ok = sems["limit"] == "cmp.le", not truths["limit"]
            if plan["boundary"]:
                limit = total if le_l == ok else (total + 1 if ok else total - 1)
            else:
                pool = [x for x in LIMITS if x > total][:3] if ok else [x for x in LIMITS if x < total][-3:]
                if pool and rng.random() >= 0.35:
                    limit = rng.choice(pool)
                else:
                    gap = rng.randint(1, max(1, total // 3))
                    limit = total + gap if ok else total - gap
            if limit < 1:
                return None
        return {"items": [(nm, un) for nm, un, _, _ in items], "po_q": po_q, "po_p": po_p, "rcv_q": rcv_q,
                "inv_q": inv_q, "inv_p": inv_p, "tol": tol, "inv_no": inv_no, "reg": reg, "limit": limit,
                "vendor": rng.choice(pack["vendors"]),
                "approver": rng.choice(pack["approvers"]), "clerk": rng.choice(pack["clerks"]),
                "dept": rng.choice(sorted(DEPTS)), "po_no": f"{pack['po']}-{rng.randrange(1000, 10000)}",
                "gr_no": f"{pack['gr']}-{rng.randrange(1000, 10000)}"}

    @staticmethod
    def _match_deltas(rng, po_q, po_p, f_p, max_pass, first_fail, tols, cap, plan, le):
        """Totals-match plan (every line bills its PO quantity): at most one moved line a and one compensating line
        c with po_q[a] * delta[a] + po_q[c] * delta[c] = 0, so the invoice total equals the PO total although a line
        differs. c gets a lower price (it always passes)."""
        n = len(po_q)
        delta = [0] * n
        if f_p:
            a = min(f_p)
        elif rng.random() < 0.6:
            a = rng.randrange(n)
        else:
            return delta
        c = rng.choice([i for i in range(n) if i != a])
        unit = po_q[c] // math.gcd(po_q[a], po_q[c])
        if f_p:
            lo = first_fail[a]
            want = tols[a] if (plan["at_tol"] and not le) else (
                lo if plan["boundary"] else rng.randint(lo, max(lo, cap[a])))
            da = -(-want // unit) * unit                                  # the next multiple of unit
        else:
            want = max_pass[a] if (plan["boundary"] or plan["at_tol"]) else rng.randint(1, max(1, max_pass[a]))
            da = (min(want, max_pass[a]) // unit) * unit
            if da <= 0:
                return delta
        dc = -(po_q[a] * da) // po_q[c]
        if po_q[a] * da + po_q[c] * dc != 0 or da > 2 * max(cap[a], first_fail[a]) or -dc > 2 * cap[c] \
                or po_p[c] + dc < 1:
            return None
        delta[a], delta[c] = da, dc
        return delta

    def _assemble(self, seed, sampler, qform, card, st, vals, pct, sems, rng) -> Spec:
        pack = card["pack"]
        code, sym = CURRENCIES[pack["currency"]][0], SYMBOL[pack["currency"]]

        def cents(x):
            return S.cents_slot(x, code, sym)

        slots = {"ORG": S.name_slot(pack["org"]), "VENDOR": S.name_slot(vals["vendor"]),
                 "CURRENCY": S.category_slot(pack["currency"], CURRENCIES), "PO_ID": S.id_slot(vals["po_no"]),
                 "GR_ID": S.id_slot(vals["gr_no"]), "INVOICE_ID": S.id_slot(vals["inv_no"]),
                 "CLERK": S.name_slot(vals["clerk"]), "DEPT": S.category_slot(vals["dept"], DEPTS)}
        for i, (name, unit) in enumerate(vals["items"], 1):
            un = UNITS[unit]
            slots[f"ITEM_{i}"] = S.name_slot(name)
            slots[f"PO_Q_{i}"] = S.count_slot(vals["po_q"][i - 1], un)
            slots[f"PO_P_{i}"] = cents(vals["po_p"][i - 1])
            slots[f"RCV_Q_{i}"] = S.count_slot(vals["rcv_q"][i - 1], un)
            slots[f"INV_Q_{i}"] = S.count_slot(vals["inv_q"][i - 1], un)
            slots[f"INV_P_{i}"] = cents(vals["inv_p"][i - 1])
        if pct:
            slots["TOL_PCT"] = S.count_slot(pct, U_PCT)
            tol_slot, tol_kind = "TOL_PCT", "count"
        else:
            slots["TOL_AMT"] = cents(vals["tol"])
            tol_slot, tol_kind = "TOL_AMT", "cents"
        slots["TOL_CMP"] = self.lexicon.clause(rng.choice(self._form_ids(sems["tol"], tol_kind)), bind={"X": tol_slot})
        if vals["limit"] is not None:
            slots["LIMIT"] = cents(vals["limit"])
            slots["LIMIT_CMP"] = self.lexicon.clause(rng.choice(self._form_ids(sems["limit"], "cents")),
                                                     bind={"X": "LIMIT"})
            slots["APPROVER"] = S.name_slot(vals["approver"])
        for j, r in enumerate(vals["reg"] or (), 1):
            slots[f"REG_{j}"] = S.id_slot(r)
        slots["PREC"] = self.lexicon.clause(rng.choice(self._form_ids(PREC_SEM)), bind={})
        spec = Spec(FAMILY, sampler, seed, card["id"], qform, slots, structure=dict(st), depth=1 + int(bool(pct)),
                    deep=False, pack=pack["id"])
        return self.derive(spec)

    def derive(self, spec: Spec) -> Spec:
        """Printed intermediates (G0 R2): the document totals (no line total is printed, G0 v2.2); then the trap tags
        (G0 R22)."""
        n, v = self._n(spec), {k: s.value for k, s in spec.slots.items()}
        code, sym = self._money(spec)
        d, deps = {}, {}
        po_keys, inv_keys = [], []
        for i in range(1, n + 1):
            po_keys += [f"PO_Q_{i}", f"PO_P_{i}"]
            inv_keys += [f"INV_Q_{i}", f"INV_P_{i}"]
        d["PO_TOTAL"] = S.cents_slot(sum(v[f"PO_Q_{i}"] * v[f"PO_P_{i}"] for i in range(1, n + 1)), code, sym)
        deps["PO_TOTAL"] = tuple(po_keys)
        d["INV_TOTAL"] = S.cents_slot(sum(v[f"INV_Q_{i}"] * v[f"INV_P_{i}"] for i in range(1, n + 1)), code, sym)
        deps["INV_TOTAL"] = tuple(inv_keys)
        out = spec.replace(derived=d, derived_deps=deps)
        return out.replace(tags=self._tags(out))

    # ------------------------------------------------------------------------------------------- construction side
    # (direct integer truths: used to hit targets, tag traps, predict twins and run error models; never the gold)
    def _judge(self, spec: Spec, mistake: str | None = None):
        """(action, failing price lines, check truths) by integer arithmetic with at most one named mistake
        (None: the card as stated). Returns None when the mistake does not apply to the spec."""
        st, v = spec.structure, spec.env()
        lines = self._lines(spec)
        pct = st["tol_kind"] == "pct"
        tsem, lsem = v["TOL_CMP"], v.get("LIMIT_CMP")
        if mistake == "drop_inclusive_endpoint":
            if "cmp.le" not in (tsem, lsem):
                return None
            tsem, lsem = ("cmp.lt" if s == "cmp.le" else s for s in (tsem, lsem))
        elif mistake == "add_exclusive_endpoint":
            if "cmp.lt" not in (tsem, lsem):
                return None
            tsem, lsem = ("cmp.le" if s == "cmp.lt" else s for s in (tsem, lsem))
        elif mistake == "t12_invoice_price_base" and not pct:
            return None
        elif mistake == "t12_near_miss_duplicate" and "dup" not in st["checks"]:
            return None
        elif mistake == "t12_limit_on_po_total" and "limit" not in st["checks"]:
            return None
        elif mistake == "first_failure_only" and st["display"] == st["checks"]:
            return None

        def price_fails(x) -> bool:
            d = x["inv_p"] - x["po_p"]
            if mistake == "t12_two_sided_tolerance":
                d = abs(d)
            if pct:
                p = v["TOL_PCT"]
                if mistake == "t12_line_total_base":
                    lhs, rhs = 100 * x["inv_q"] * d, p * x["po_q"] * x["po_p"]
                else:
                    lhs, rhs = 100 * d, p * (x["inv_p"] if mistake == "t12_invoice_price_base" else x["po_p"])
            else:
                lhs, rhs = (x["inv_q"] * d if mistake == "t12_line_total_base" else d), v["TOL_AMT"]
            return lhs > rhs if tsem == "cmp.le" else lhs >= rhs

        pf = [i for i, x in enumerate(lines) if price_fails(x)]
        ref = "po_q" if mistake == "t12_ordered_not_received" else "rcv"
        t = {"qty": any(x["inv_q"] > x[ref] for x in lines), "price": bool(pf)}
        if "dup" in st["checks"]:
            inv, regs = v["INVOICE_ID"], self._regs(spec)
            t["dup"] = inv in regs or (mistake == "t12_near_miss_duplicate" and any(_is_near(r, inv) for r in regs))
        if "limit" in st["checks"]:
            total = v["PO_TOTAL"] if mistake == "t12_limit_on_po_total" else v["INV_TOTAL"]
            t["limit"] = total > v["LIMIT"] if lsem == "cmp.le" else total >= v["LIMIT"]
        order = list(st["checks"])
        if mistake == "first_failure_only":
            order = list(st["display"])
        elif mistake == "t12_reverse_order":
            order.reverse()
        verdict = _first_failing(order, t)
        if mistake == "t12_price_first" and t["price"]:
            verdict = "review"
        elif mistake == "t12_totals_only":
            verdict = "release" if v["INV_TOTAL"] == v["PO_TOTAL"] else None
        elif mistake == "t12_line_by_line":
            verdict = self._line_by_line(st, lines, pf, t)
        return verdict, pf, t

    @staticmethod
    def _line_by_line(st, lines, pf, t) -> str:
        line_checks = [c for c in st["checks"] if c in ("qty", "price")]
        for i, x in enumerate(lines):
            for c in line_checks:
                if (c == "qty" and x["inv_q"] > x["rcv"]) or (c == "price" and i in pf):
                    return ACTION_OF[c]
        return next((ACTION_OF[c] for c in st["checks"] if c in ("dup", "limit") and t[c]), "release")

    def _tags(self, spec: Spec) -> tuple:
        st, v = spec.structure, spec.env()
        verdict, pf, t = self._judge(spec)
        lines, tols = self._lines(spec), self._tols(spec)
        tags = set()
        if sum(t[c] for c in st["checks"]) >= 2:
            tags.add("two_fail")
        same = all(x["inv_q"] == x["po_q"] == x["rcv"] and x["inv_p"] == x["po_p"] for x in lines)
        if v["INV_TOTAL"] == v["PO_TOTAL"] and not same:
            tags.add("totals_match_lines_differ")
        if any(x["inv_p"] - x["po_p"] == tl for x, tl in zip(lines, tols)):
            tags.add("at_tolerance")
        if any(x["rcv"] < x["po_q"] and x["inv_q"] <= x["rcv"] for x in lines):
            tags.add("shortfall_billed_ok")
        if any(x["inv_q"] == x["rcv"] + 1 for x in lines):
            tags.add("qty_boundary")
        if any(x["inv_p"] < x["po_p"] for x in lines):
            tags.add("price_below_po")
        if any(_is_near(r, v["INVOICE_ID"]) for r in self._regs(spec)):
            tags.add("near_miss_duplicate")
        if "limit" in st["checks"] and v["LIMIT"] == v["INV_TOTAL"]:
            tags.add("limit_at_boundary")
        for name, tag in (("t12_invoice_price_base", "wrong_base_trap"), ("t12_line_total_base", "wrong_base_trap"),
                          ("first_failure_only", "display_order_trap"), ("t12_line_by_line", "line_by_line_trap"),
                          ("t12_totals_only", "totals_trap"), ("t12_price_first", "salience_trap")):
            r = self._judge(spec, name)
            if r is not None and r[0] is not None and (r[0], r[1]) != (verdict, pf):
                tags.add(tag)
        return tuple(sorted(tags))

    # ------------------------------------------------------------------------------------------- solver A
    def _env_a(self, spec: Spec) -> dict:
        v = spec.env()
        env = {"INVNO": v["INVOICE_ID"]}
        for i in range(1, self._n(spec) + 1):
            env[f"QI{i}"], env[f"QR{i}"] = v[f"INV_Q_{i}"], v[f"RCV_Q_{i}"]
            env[f"PP{i}"] = Decimal(v[f"PO_P_{i}"]) / 100
            env[f"PI{i}"] = Decimal(v[f"INV_P_{i}"]) / 100
        env["TOL"] = Decimal(v["TOL_PCT"]) if spec.structure["tol_kind"] == "pct" else Decimal(v["TOL_AMT"]) / 100
        if "LIMIT" in v:
            env["LIMIT"] = Decimal(v["LIMIT"]) / 100
        for j, r in enumerate(self._regs(spec), 1):
            env[f"REG{j}"] = r
        return env

    def _price_nodes(self, spec: Spec) -> list:
        """One node per line: the line fails the price check (difference above the allowed variance)."""
        st, v = spec.structure, spec.env()
        op = ">" if v["TOL_CMP"] == "cmp.le" else ">="
        out = []
        for i in range(1, st["n"] + 1):
            allowed = (RL.Fn("t12_pct_of", (RL.Ref(f"PP{i}"), RL.Ref("TOL"))) if st["tol_kind"] == "pct"
                       else RL.Ref("TOL"))
            out.append(RL.Cmp(op, RL.Fn("sub", (RL.Ref(f"PI{i}"), RL.Ref(f"PP{i}"))), allowed))
        return out

    def _fail_node(self, spec: Spec, check: str):
        n, v = self._n(spec), spec.env()
        if check == "qty":
            return RL.Or(tuple(RL.Cmp(">", RL.Ref(f"QI{i}"), RL.Ref(f"QR{i}")) for i in range(1, n + 1)))
        if check == "price":
            return RL.Or(tuple(self._price_nodes(spec)))
        if check == "dup":
            return RL.In(RL.Ref("INVNO"), tuple(RL.Ref(f"REG{j}") for j in range(1, len(self._regs(spec)) + 1)))
        total = RL.Fn("t12_line_amount", (RL.Ref("QI1"), RL.Ref("PI1")))
        for i in range(2, n + 1):
            total = RL.Fn("add", (total, RL.Fn("t12_line_amount", (RL.Ref(f"QI{i}"), RL.Ref(f"PI{i}")))))
        return RL.Cmp(">" if v["LIMIT_CMP"] == "cmp.le" else ">=", total, RL.Ref("LIMIT"))

    def _solve(self, spec: Spec) -> tuple:
        env = self._env_a(spec)
        rs = RL.RuleSet(tuple(RL.Rule(c, ACTION_OF[c], self._fail_node(spec, c)) for c in spec.structure["checks"]),
                        "first_match", "release")
        verdict = RL.resolve(rs, env).effect
        pf = [i for i, node in enumerate(self._price_nodes(spec)) if RL.evaluate(node, env)]
        return verdict, pf

    def solve_a(self, spec: Spec):
        verdict, pf = self._solve(spec)
        return _answer(spec.qform, verdict, pf, self._items(spec))

    # ------------------------------------------------------------------------------------------- canonical facts (G3)
    def canonical(self, spec: Spec) -> dict:
        st, a, v = spec.structure, spec.all_slots(), spec.env()

        def c(k):
            return S.canonical(a[k]) if k in a else None

        lines = [{"item": c(f"ITEM_{i}"), "unit": a[f"PO_Q_{i}"].param("unit")[0], "po_qty": c(f"PO_Q_{i}"),
                  "po_price": c(f"PO_P_{i}"), "received": c(f"RCV_Q_{i}"), "inv_qty": c(f"INV_Q_{i}"),
                  "inv_price": c(f"INV_P_{i}")} for i in range(1, st["n"] + 1)]
        pct = st["tol_kind"] == "pct"
        return {"qform": spec.qform, "org": c("ORG"), "vendor": c("VENDOR"), "currency": c("CURRENCY"),
                "po_id": c("PO_ID"), "gr_id": c("GR_ID"), "invoice_id": c("INVOICE_ID"),
                "lines": lines, "po_total": c("PO_TOTAL"),
                "inv_total": c("INV_TOTAL"), "register": self._regs(spec) or None, "checks": list(st["checks"]),
                "display": list(st["display"]), "style": st["style"], "card_style": st["card_style"],
                "tol_kind": st["tol_kind"],
                "tol": c("TOL_PCT") if pct else c("TOL_AMT"), "tol_cmp": v["TOL_CMP"], "limit": c("LIMIT"),
                "limit_cmp": v.get("LIMIT_CMP"), "approver": c("APPROVER"), "precedence": v["PREC"],
                "codes": dict(zip(st["codes"], _verdicts(st["checks"]))) if st["codes"] else None,
                "clerk": c("CLERK"), "dept": c("DEPT")}

    def canonical_for(self, spec: Spec, author_mode: str) -> dict:
        c = self.canonical(spec)
        return c if author_mode == "T" else {k: x for k, x in c.items() if k not in ("clerk", "dept")}

    def extract_view(self, spec: Spec) -> dict:
        c = self.canonical(spec)
        return {"clerk": c["clerk"], "dept": c["dept"]}

    def extract_fields(self, spec: Spec) -> list:
        from c2_kit.g3h import Field
        return [Field("clerk", "name", "the accounts payable person the note is from or to, as written"),
                Field("dept", "category", "the team the purchase is for", spec.slots["DEPT"].params)]

    # ------------------------------------------------------------------------------------------- render
    @staticmethod
    def _register_of(seed: int, sampler: str) -> str:
        """The skin register of a seed: a low-discrepancy draw over the seed (label-blind: seed and sampler only). S3, S4
        and S5 draw uniformly from their own registers; S1 and S2 with the FREE_REGISTER_W weights (G0 v2.2 R21)."""
        u = ((seed + 1) * REGISTER_STEP + uhash(FAMILY, "regphase", sampler)) % 1.0
        regs = SKIN_REGISTERS.get(sampler)
        if regs:
            return regs[min(len(regs) - 1, int(u * len(regs)))]
        acc = 0.0
        for reg, w in FREE_REGISTER_W:
            acc += w
            if u < acc:
                return reg
        return FREE_REGISTER_W[-1][0]

    def _pick_skin(self, ctx, spec, key, held):
        reg = self._register_of(spec.seed, spec.sampler)
        try:
            return self._pick_rr(ctx, "skin", spec, held, register=reg)
        except (LookupError, KeyError):
            return ctx.pick(FAMILY, "skin", key, held_out=held)

    @staticmethod
    def _pick_rr(ctx, kind: str, spec, held: bool, *, register=None, qform=None):
        """A skin of a register / a wording of a question form, round-robin over the block: the rows of the stratum (the
        training samplers' rows of that register or question form, in (seed, sampler) order) take the candidates in a
        seeded permutation, so every candidate is used once before any is used twice (spec 3.0: each skin <= 6 rows, each
        wording <= 2%). Label-blind: seeds and candidate ids only. KeyError: the row is not a row of that stratum (a
        complement partner's wording): the caller falls back to the kit's hash pick."""
        c = sorted((x for x in ctx.skins.values() if x.family == FAMILY and x.kind == kind and x.held_out == held
                    and (register is None or x.register == register) and (qform is None or x.qform == qform)),
                   key=lambda x: x.skin_id)
        if not c:
            raise LookupError(f"no {kind} for {FAMILY} (register={register}, qform={qform}, held_out={held})")
        b0 = spec.seed - spec.seed % BLOCK
        group = TRAIN_SAMPLERS if spec.sampler in TRAIN_SAMPLERS else (spec.sampler,)
        key = ("reg", register) if kind == "skin" else ("qform", qform)
        rank = _block_members(group, b0)[key][(spec.seed, spec.sampler)]
        perm = sorted(c, key=lambda x: uhash(FAMILY, "rr", kind, b0, repr(key), held, x.skin_id))
        return perm[rank % len(perm)]

    def _pick_wording(self, ctx, spec, key, held):
        for h in ((True, False) if held else (False,)):
            try:
                return self._pick_rr(ctx, "wording", spec, h, qform=spec.qform)
            except KeyError:
                break
            except LookupError:
                continue
        return ctx.pick(FAMILY, "wording", key, qform=spec.qform, held_out=False)

    def _doc(self, spec: Spec, kind: str, slots: dict, forms: dict) -> list:
        st = spec.structure
        n, fmt = st["n"], st["doc_fmt"]
        if kind == "reg":
            ids = ["{REG_%d}" % j for j in range(1, len(self._regs(spec)) + 1)]
            if fmt == "json":
                body = '{"vendor":{VENDOR},"paid_invoice_numbers":[%s]}' % ",".join(ids)
                return [JSON_HEAD["reg"] + "\n", K.fill(body, slots, forms, escape="json")]
            text = {"kv": "Paid-invoice register for {VENDOR}: " + ", ".join(ids),
                    "table": "Paid-invoice register | vendor {VENDOR}\n| invoice number |\n|---|\n"
                             + "\n".join("| %s |" % x for x in ids),
                    "csv": "Paid-invoice register export, vendor {VENDOR}\ninvoice_number\n" + "\n".join(ids)}[fmt]
            return [K.fill(text, slots, forms)]
        if fmt == "json":
            body = JSON_DOC[kind] % ",".join(JSON_LINE[kind].replace("#", str(i)) for i in range(1, n + 1))
            return [JSON_HEAD[kind] + "\n", K.fill(body, slots, forms, escape="json")]
        head, line, foot = {"kv": DOC_KV, "table": DOC_TABLE, "csv": DOC_CSV}[fmt][kind]
        parts = [head] + [line.replace("#", str(i)) for i in range(1, n + 1)] + ([foot] if foot else [])
        return [K.fill("\n".join(parts), slots, forms)]

    @staticmethod
    def card_template(spec: Spec) -> str:
        """The policy card as one template (slots in braces; G0 v2.2 R12): the style's phrasing of every CardItem, the
        checks in the display order, the check order, {PREC}, the release line, the amounts line, the answer codes
        (ch_action rows, 12%) and the closed-world sentence."""
        st = spec.structure
        sty = st["card_style"]
        lines = [CARD_HEADER.text(sty)]
        if st["style"] == "table":
            lines += list(RULE_TABLE_HEAD)
        for k, c in enumerate(st["display"], 1):
            cond = CARD_COND["price_" + st["tol_kind"]] if c == "price" else CARD_COND[c]
            title, action = CARD_TITLE[c].text(sty), ACTION_PHRASE[ACTION_OF[c]]
            if st["style"] == "table":
                lines.append(RULE_TABLE_TPL.format(title=title, cond=cond.text(sty), action=action))
            else:
                lines.append(RULE_LIST_TPL.format(lead=f"{k}." if st["style"] == "numbered" else "-", title=title,
                                                  cond=cond.text(sty), action=action))
        lines.append(ORDER_TPL.format(names=", then ".join(CHECK_NAME[c] for c in st["checks"])))
        lines.append("{PREC}")
        lines.append(CARD_RELEASE.text(sty))
        lines.append(CARD_AMOUNTS.text(sty))
        if st["codes"]:
            pairs = ", ".join(f"{w} = {ACTION_PHRASE[x]}" for w, x in zip(st["codes"], _verdicts(st["checks"])))
            lines.append(CODES_TPL.format(pairs=pairs))
        lines.append(CLOSED_WORLD)
        return "\n".join(lines)

    # ------------------------------------------------------------------------------------------- wording screen
    def ctx_for(self, spec, ctx):
        """The kit context without the wordings that break the premise or polarity rule (wording_screen; pilot fixes
        F1 and c2_kit.polarity), so neither render() nor the pipeline's complement partner can pick one. Label-blind
        (the wording text and its form only); cached per context object."""
        for c, screened, _bad in self._screened:
            if c is ctx:
                return screened
        bad = {}
        for sid, sk in ctx.skins.items():
            if sk.kind == "wording" and sk.qform:
                p = WS.problems(sk.text, sk.qform, self)
                if p:
                    bad[sid] = p
        screened = KitCtx(skins={k: v for k, v in ctx.skins.items() if k not in bad}, lexicon=ctx.lexicon) if bad \
            else ctx
        self._screened.append((ctx, screened, bad))
        return screened

    def quarantined_wordings(self, ctx) -> dict:
        """{wording skin id: problems} for the wordings ctx_for() leaves out of `ctx`."""
        self.ctx_for(None, ctx)
        return next(bad for c, _s, bad in self._screened if c is ctx)

    def render(self, spec: Spec, ctx, *, skin=None, wording=None, forms=None, attack=None):
        ctx = self.ctx_for(spec, ctx)                  # never pick a wording that breaks the premise / polarity rule
        key = f"{spec.family}|{spec.seed}|{spec.sampler}|{spec.qform}"
        held = spec.sampler in self.HELD_OUT_SAMPLERS
        st = spec.structure
        skin = skin or self._pick_skin(ctx, spec, key, held)
        wording = wording or self._pick_wording(ctx, spec, key, held)
        if wording.qform != spec.qform:
            raise ContractError(f"wording {wording.skin_id} asks {wording.qform}, spec asks {spec.qform}")
        forms = forms or choose_forms(spec, key)
        slots = spec.all_slots()
        narrative = skin.fill(slots, forms)
        if "\n\n" in narrative.text or narrative.text != narrative.text.strip():
            raise K.RenderError(f"skin {skin.skin_id}: a narrative is one block (no blank line, no outer space)")
        blocks = {"narrative": [narrative]}
        for kind in ("po", "gr", "inv"):
            blocks[kind] = self._doc(spec, kind, slots, forms)
        if self._regs(spec):
            blocks["reg"] = self._doc(spec, "reg", slots, forms)
        tb = TextBuilder()
        for k, name in enumerate(b for b in ORDERS[st["blocks"]] if b in blocks):
            if k:
                tb.add("state", "\n\n")
            for piece in blocks[name]:
                tb.add("state", piece, skin_id=skin.skin_id if name == "narrative" else None)
        if attack is not None:
            tb.add("state", "\n\n").add("state", attack.fill(slots, forms), skin_id=attack.skin_id)
        # the rules: yes/no rows print row.card once, choice rows the head of the instructions (cards.place_rules)
        placed = CARDS.place_rules(tb, K.fill(self.card_template(spec), slots, forms), self.QFORMS[spec.qform].qtype)
        tb.add("instructions", wording.fill(slots, forms), skin_id=wording.skin_id)
        ans = self.solve_a(spec)
        os_ = None
        if spec.qform == "ch_action":
            vs, codes = _verdicts(st["checks"]), st["codes"]
            text = (lambda k: codes[vs.index(k)]) if codes else OPTION_TEXT.__getitem__
            os_ = build_closed(spec, ans, vs, self.error_models(), row_key=key, render_key=text)
        elif spec.qform == "ch_price_line":
            os_ = build_closed(spec, ans, self._items(spec) + [NONE_LINE], self.error_models(), row_key=key,
                               render_key=lambda k: NONE_LINE_TEXT if k == NONE_LINE else k)
        return assemble_row(self, spec, tb, answer=ans, option_set=os_, skin=skin, wording=wording, forms=forms,
                            attack=attack, defs_style=CARDS.defs_style(placed, st["card_style"]))

    # ------------------------------------------------------------------------------------------- relations
    def relations(self, spec: Spec) -> list:
        out = []
        seed, q = spec.seed, spec.qform
        if q in COMPLEMENTS and uhash(FAMILY, "comp", spec.sampler, seed) < COMPLEMENT_RATE[q]:
            u, acc, q2 = uhash(FAMILY, "ckind", spec.sampler, seed), 0.0, COMPLEMENTS[q][-1][0]
            for cand, w in COMPLEMENTS[q]:
                acc += w
                if u < acc:
                    q2 = cand
                    break
            out.append(RelationProposal("complement", qform=q2))
        u = uhash(FAMILY, "extra", spec.sampler, seed)
        if u < EQUIV_RATE:
            if uhash(FAMILY, "equivfmt", spec.sampler, seed) < 0.5:
                st = spec.structure
                out.append(RelationProposal("equiv", spec=spec.replace(
                    structure={**st, "doc_fmt": EQUIV_FMT[st["doc_fmt"]]}), note="another document container"))
            else:
                out.append(RelationProposal("equiv", note="another register"))
        elif u < EQUIV_RATE + INV_RATE:
            out.append(RelationProposal("inv"))
        # no twin for ch_price_line (G0 v2.2 R24): the twin of a "none" row is an item row and the other way round, so
        # twins inverted the 1 / k gold share of R16 (none was gold 7 pp too often over base and twin rows)
        if q != "ch_price_line" and uhash(FAMILY, "twin", spec.sampler, seed) < TWIN_RATE:
            t = self._twin(spec)
            if t is not None:
                out.append(t)
        return out + self._metamorphic(spec)

    def _twin(self, spec: Spec):
        """One input slot moved across one check's boundary (G0 R24). The new answer is predicted from the base
        check truths with that one check flipped; the twin's own construction truths must confirm the flip."""
        st, v = spec.structure, spec.env()
        verdict, pf, t = self._judge(spec)
        lines, tols = self._lines(spec), self._tols(spec)
        le = v["TOL_CMP"] == "cmp.le"
        code, sym = self._money(spec)
        cands = []                                   # (slot, new slot, check, predicted failing price lines)
        qf = [i for i, x in enumerate(lines) if x["inv_q"] > x["rcv"]]
        if len(qf) == 1:
            i, x = qf[0], lines[qf[0]]
            unit = spec.slots[f"RCV_Q_{i + 1}"].param("unit")
            if x["inv_q"] <= x["po_q"]:                  # the rest of the order arrives
                cands.append((f"RCV_Q_{i + 1}", S.count_slot(x["inv_q"], unit), "qty", pf))
            else:                                        # an over-billed line is billed at what was received
                cands.append((f"INV_Q_{i + 1}", S.count_slot(x["rcv"], unit), "qty", pf))
        elif not qf:
            for i, x in enumerate(lines):
                r = x["inv_q"] - 1
                if r >= 1 and x["po_q"] - r <= 3:
                    cands.append((f"RCV_Q_{i + 1}", S.count_slot(r, spec.slots[f"RCV_Q_{i + 1}"].param("unit")),
                                  "qty", pf))
        if len(pf) == 1:
            i = pf[0]
            new_p = lines[i]["po_p"] + (tols[i] if le else tols[i] - 1)
            if new_p >= 1:
                cands.append((f"INV_P_{i + 1}", S.cents_slot(new_p, code, sym), "price", []))
        elif not pf:
            for i, x in enumerate(lines):
                new_p = x["po_p"] + (tols[i] + 1 if le else tols[i])
                cands.append((f"INV_P_{i + 1}", S.cents_slot(new_p, code, sym), "price", [i]))
        if "dup" in st["checks"]:
            regs, inv = self._regs(spec), v["INVOICE_ID"]
            if t["dup"]:
                alt = [x for x in _near_variants(inv) if x not in regs]
                pick = alt[int(uhash(FAMILY, "twinreg", spec.sampler, spec.seed) * len(alt))]
                cands.append((f"REG_{regs.index(inv) + 1}", S.id_slot(pick), "dup", pf))
            else:
                j = int(uhash(FAMILY, "twinreg", spec.sampler, spec.seed) * len(regs))
                cands.append((f"REG_{j + 1}", S.id_slot(inv), "dup", pf))
        if "limit" in st["checks"]:
            total, le_l = v["INV_TOTAL"], v["LIMIT_CMP"] == "cmp.le"
            new = (total if le_l else total + 1) if t["limit"] else (total - 1 if le_l else total)
            if new >= 1:
                cands.append(("LIMIT", S.cents_slot(new, code, sym), "limit", pf))
        items = self._items(spec)
        base = _answer(spec.qform, verdict, pf, items)
        keep = []
        for slot, new_slot, check, new_pf in cands:
            want = dict(t)
            want[check] = not t[check]
            new_v = _first_failing(st["checks"], want)
            expect = _answer(spec.qform, new_v, new_pf, items)
            if expect == base:
                continue                                 # the question's answer must flip, not only a check
            twin = self.derive(spec.with_slot(slot, new_slot))
            got_v, got_pf, got_t = self._judge(twin)
            if {c: got_t[c] for c in st["checks"]} != {c: want[c] for c in st["checks"]} or got_pf != new_pf:
                continue                                 # the edit moved another check too: not a minimal twin
            keep.append((slot, new_slot, expect, f"{slot} across the {CHECK_NAME[check]} boundary: "
                                                 f"{verdict} -> {new_v}"))
        if not keep:
            return None
        # the twin's new answer is drawn first, uniformly over the answers the candidates can reach (a line count n makes
        # n price and n quantity candidates but one duplicate and one limit candidate, so a uniform draw over candidates
        # over-weighted the hold / review golds: the longest option text of a ch_action row was gold 8 pp too often on
        # twins, a visible-length cue); then a candidate that reaches it, uniformly. Both draws come from the row key.
        answers = sorted({repr(k[2]) for k in keep})
        want = answers[int(uhash(FAMILY, "twinans", spec.sampler, spec.seed) * len(answers))]
        pool = [k for k in keep if repr(k[2]) == want]
        slot, new_slot, expect, note = pool[int(uhash(FAMILY, "twinpick", spec.sampler, spec.seed) * len(pool))]
        return RelationProposal("twin", spec=spec.with_slot(slot, new_slot), changed_slot=slot, expect=expect,
                                note=note)

    def _metamorphic(self, spec: Spec) -> list:
        st, v = spec.structure, spec.env()
        pack = next(p for p in PACKS if p["id"] == spec.pack)
        out = []
        other = next(x for x in pack["vendors"] if x != v["VENDOR"])
        out.append(RelationProposal("metamorphic", spec=spec.with_slot("VENDOR", S.name_slot(other)), expect="same",
                                    note="rename the vendor"))
        org = next(p["org"] for p in PACKS if p["org"] != v["ORG"])
        out.append(RelationProposal("metamorphic", spec=spec.with_slot("ORG", S.name_slot(org)), expect="same",
                                    note="rename the buyer"))
        n = st["n"]
        if n >= 2:
            sl = dict(spec.slots)
            for i in range(1, n + 1):
                for pre in ("ITEM", "PO_Q", "PO_P", "RCV_Q", "INV_Q", "INV_P"):
                    sl[f"{pre}_{i}"] = spec.slots[f"{pre}_{n + 1 - i}"]
            out.append(RelationProposal("metamorphic", spec=spec.replace(slots=sl), expect="same",
                                        note="reverse the line order"))
        if "APPROVER" in spec.slots:                     # the approver's name is narrative (G0 R7): rename it
            other = next(x for x in pack["approvers"] if x != v["APPROVER"])
            out.append(RelationProposal("metamorphic", spec=spec.with_slot("APPROVER", S.name_slot(other)),
                                        expect="same", note="rename the approver"))
        rev = list(reversed(st["checks"]))
        st2 = {**st, "checks": rev, "display": rev if st["style"] == "numbered" else list(st["display"])}
        verdict, pf, t = self._judge(spec)
        expect = _answer(spec.qform, _first_failing(rev, t), pf, self._items(spec))
        out.append(RelationProposal("metamorphic", spec=spec.replace(structure=st2), expect=expect,
                                    note="reverse the check order"))
        return out

    # ------------------------------------------------------------------------------------------- error models
    def error_models(self) -> dict:
        def make(name):
            def fn(spec):
                if spec.qform not in ("ch_action", "ch_price_line"):
                    return None
                r = self._judge(spec, name)
                if r is None or r[0] is None:
                    return None
                verdict, pf, _ = r
                if spec.qform == "ch_action":
                    return verdict
                if len(pf) > 1:
                    return None
                return self._items(spec)[pf[0]] if pf else NONE_LINE
            return fn

        return {name: error_model(name, make(name)) for name in ERROR_NAMES}
