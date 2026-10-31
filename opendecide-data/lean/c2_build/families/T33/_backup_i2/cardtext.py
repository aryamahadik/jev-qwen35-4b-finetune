"""families/T33/cardtext.py: the T33 rules block in two styles, with need-to-know items (G0_SPEC.md section 2 and
amendment 3 in section 8; C2_DATA_SPEC 3.0 "Definition styles" and "Length"; c2_kit.cards).

The block holds every rule the row needs and nothing else:
  log rules   a bullet list (head + bullets). A bullet appears only when the row needs it: the result bullet when a
              value is checked or claimed (and only the field it names), the unit bullets when a money value or a
              duration is involved, the table bullet when the log is a table that shows values.
  (a)         the success criterion head (its two optional clauses only when a listed check needs them), the numbered
              checks "(n) {CHKn}", and for ch_failed_check the tie line
  (b)         the claim rules (the value clause only when a claim states a value), and for ch_bad_claim the tie line
  closed      the closed-world sentence, on every row (G-TW)
Placement (cards.place_rules): yes/no rows carry the block in row.card (the served prompt prints it once, as the
definitions block), choice rows at the head of the instructions (the only place a choice row prints rules, twice).
Styles: "full" (the frozen G0 phrasing) and "short" (the terse phrasing spec 3.0 allows on about 15% of rows; every
rule stays, checked by cards.variant_problems in test_cardtext.py). The style is drawn from the seed (label-blind) and
is the same for every question form of one spec (a complement pair shares its card).

This is the generator side. Solver B (solver_b.py) holds its own copy of the texts, written from G0_SPEC.md.
"""
from __future__ import annotations

from dataclasses import dataclass

from c2_kit import cards as CD
from c2_kit.cards import CardItem, CardSpec

STYLE_SHARES = {"full": 0.85, "short": 0.15}          # spec 3.0: a short card on about 15% of rows
MONEY_VERBS = ("refund", "charge", "credit", "payout")
BULK_VERBS = ("import", "export", "sync")

LOG_HEAD = "Log rules (lines in time order):"
CLOSED_WORLD = "The log is complete and the only evidence: no other call, retry or poll took place."
SEPARATE_TIE = {"ch_failed_check", "ch_bad_claim"}


@dataclass(frozen=True)
class Needs:
    """What the row's rules must say, from the VISIBLE inputs (the listed checks or the claims; never the gold)."""
    money: bool = False       # an amount (amount_cents) is checked or claimed
    rows: bool = False        # a row count (rows_written) is checked or claimed
    dur: bool = False         # a max_duration check is listed
    tries: bool = False       # a max_tries check is listed
    value_dep: bool = False   # a listed check depends on a value the log may not show (value check, max_duration)
    table: bool = False       # the log is a csv / markdown table

    @property
    def value(self) -> bool:
        return self.money or self.rows


def needs_of(spec) -> Needs:
    """Needs of a spec: (a) from its listed checks, (b) from its claims' verbs."""
    st = spec.structure
    env = spec.env()
    table = st["fmt"] in ("csv", "md")
    if st["sub"] == "a":
        sems = [env[f"CHK{c}"] for c in range(1, len(st["checks"]) + 1)]
        money, rows = "crit.amount_match" in sems, "crit.all_written" in sems
        dur, tries = "crit.max_duration" in sems, "crit.max_tries" in sems
        return Needs(money, rows, dur, tries, money or rows or dur, table)
    verbs = [env[f"K{j}"].split(".", 1)[1] for j in range(1, len(st["claims"]) + 1)]
    return Needs(money=any(v in MONEY_VERBS for v in verbs), rows=any(v in BULK_VERBS for v in verbs), table=table)


def _result_field(n: Needs) -> str:
    return "amount_cents or rows_written" if n.money and n.rows else ("amount_cents" if n.money else "rows_written")


# ------------------------------------------------------------------------------------------------ log rules
LOG_ITEMS = (
    CardItem("done",
             "A step is done if a try got 200, 201 or 204, a retry with the same idempotency key got 409, or a try "
             "got 202 and the job's last poll says succeeded.",
             short="A step is done if a try got 200, 201 or 204, a retry with the same key got 409, or a try got 202 "
                   "and the job's last poll says succeeded."),
    CardItem("other", "Any other try status does nothing. A poll's status 200 means nothing; its state counts."),
    CardItem("res_amt",
             "Result: amount_cents on the try that got 200 or 201, else on the job's last poll.",
             short="Result: amount_cents on the 200 or 201 try, else on the job's last poll.",
             when=lambda sp: (lambda n: n.money and not n.rows)(needs_of(sp))),
    CardItem("res_rows",
             "Result: rows_written on the try that got 200 or 201, else on the job's last poll.",
             short="Result: rows_written on the 200 or 201 try, else on the job's last poll.",
             when=lambda sp: (lambda n: n.rows and not n.money)(needs_of(sp))),
    CardItem("res_both",
             "Result: amount_cents or rows_written on the try that got 200 or 201, else on the job's last poll.",
             short="Result: amount_cents or rows_written on the 200 or 201 try, else on the job's last poll.",
             when=lambda sp: (lambda n: n.money and n.rows)(needs_of(sp))),
    CardItem("u_cents", "amount_cents is cents (100 = $1).", short="amount_cents: cents (100 = $1).",
             when=lambda sp: (lambda n: n.money and not n.dur)(needs_of(sp))),
    CardItem("u_ms", "duration_ms is milliseconds.", short="duration_ms: milliseconds.",
             when=lambda sp: (lambda n: n.dur and not n.money)(needs_of(sp))),
    CardItem("u_both", "amount_cents is cents (100 = $1); duration_ms is milliseconds.",
             short="amount_cents: cents (100 = $1); duration_ms: milliseconds.",
             when=lambda sp: (lambda n: n.dur and n.money)(needs_of(sp))),
    CardItem("table", "Table: requested and result are in the unit named by field.",
             short="Table: requested and result use the unit named by field.",
             when=lambda sp: (lambda n: n.table and n.value)(needs_of(sp))),
)
LOG_CARD = CardSpec("T33", LOG_ITEMS, heads={"full": LOG_HEAD, "short": LOG_HEAD}, numbered=False)


# ------------------------------------------------------------------------------------------------ criterion (a)
CRIT = {
    "full": ("Success criterion for step {STEP}: every check must hold", "; a check on a value the log does not show "
             "fails", "; polls are not tries", "."),
    "short": ("Success criterion for step {STEP}: every check must hold", "; a check on a value the log lacks fails",
              "; polls are not tries", "."),
}
TIE_CHECK = {"full": "If several checks fail, answer the lowest-numbered one; if none fails, answer None.",
             "short": "Answer the lowest-numbered failing check; if none fails, answer None."}


def crit_head(style: str, n: Needs) -> str:
    head, dep, tries, end = CRIT[style]
    return head + (dep if n.value_dep else "") + (tries if n.tries else "") + end


# ------------------------------------------------------------------------------------------------ claims (b)
def _differs(n: Needs) -> str:
    what = "amount or row count" if n.money and n.rows else ("amount" if n.money else "row count")
    return f", or the claim's {what} differs from its result"


def claim_rules(style: str, n: Needs) -> str:
    cond = _differs(n) if n.value else ""
    if style == "full":
        return ("Claim rules: a claim is about the step whose target it names.\n"
                "- No step in the log has that target: not shown in the log.\n"
                f"- That step is not done{cond}: contradicted.\n"
                "- Otherwise: supported.")
    return ("Claim rules: a claim is about the step whose target it names. No step in the log has that target: not "
            f"shown in the log. That step is not done{cond}: contradicted. Otherwise: supported.")


TIE_CLAIM = {"full": "If several claims are contradicted or not shown, answer the one first in the message; if none, "
                     "answer None.",
             "short": "Answer the first claim in the message that is contradicted or not shown, or None if none is."}


# ------------------------------------------------------------------------------------------------ the block
def draw_style(seed: int, sampler: str) -> str:
    """The card style of a spec: the seed alone (label-blind), the same for every question form of the spec."""
    return CD.draw_style(f"T33|{seed}|{sampler}|card", STYLE_SHARES)


def block_template(spec, style: str) -> str:
    """The rules block of a spec as a template ({STEP}, {CHKn} placeholders)."""
    if style not in STYLE_SHARES:
        raise CD.CardError(f"T33 card style {style!r}")
    n = needs_of(spec)
    st = spec.structure
    parts = [LOG_CARD.template(style, spec)]
    if st["sub"] == "a":
        parts.append(crit_head(style, n))
        parts += [f"({c}) {{CHK{c}}}" for c in range(1, len(st["checks"]) + 1)]
        if spec.qform == "ch_failed_check":
            parts.append(TIE_CHECK[style])
    else:
        parts.append(claim_rules(style, n))
        if spec.qform == "ch_bad_claim":
            parts.append(TIE_CLAIM[style])
    parts.append(CLOSED_WORLD)
    return "\n".join(parts)


def variant_problems() -> list:
    """Every short phrasing keeps its full phrasing's slots, numbers, operator words and negation count."""
    out = list(LOG_CARD.problems())
    for style in ("short",):
        for key in (0, 1, 2, 3):
            n = Needs(value_dep=bool(key & 1), tries=bool(key & 2))
            out += [f"crit {style} {key}: {p}" for p in CD.variant_problems(crit_head("full", n), crit_head(style, n))]
        for n in (Needs(money=True), Needs(rows=True), Needs(money=True, rows=True), Needs()):
            out += [f"claims {style} {n}: {p}" for p in CD.variant_problems(claim_rules("full", n),
                                                                           claim_rules(style, n))]
    out += [f"tie_check: {p}" for p in CD.variant_problems(TIE_CHECK["full"], TIE_CHECK["short"])]
    out += [f"tie_claim: {p}" for p in CD.variant_problems(TIE_CLAIM["full"], TIE_CLAIM["short"])]
    return out
