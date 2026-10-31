"""families/T01/plugin.py: T01 "rolling windows and anchored deadlines" (C2_DATA_SPEC 2.1 T01, 3.10; G0_SPEC.md
frozen v2 after the Haiku ambiguity pass amb:T01, sha below). Absorbs the T02 rolling sums (S4) and the T16
cutoffs (S6).

Seven card kinds, each with every rule printed on the card (closed world) and every intermediate printed:
  rolling   (S1, S5)  at most N days present in any M-day window; stays inclusive of entry and exit; the window that
                      ends on the reference date is checked, its first day printed; each stay's day count printed
  anchor    (S2, S5)  a filing is due within N days after the LATER of two dated events (later date = day zero); the
                      day counts from each event to the filing are printed
  waiting   (S3)      a waiting period of W days whose first day is the day after its start date (the policy start,
                      or a rider's effective date for the rider's peril); the day counts to the loss are printed
  purchase  (S4)      the new request plus the earlier purchases inside the M-day window ending on the request date,
                      against a comparator clause (more than / or more); the window's first day is printed
  cash      (S4)      per-day deposit and withdrawal totals kept apart (never netted, never mixed across days),
                      against a comparator clause
  addon     (S6)      due N days after the notice, + K days for a notice sent by post, moved forward past listed
                      office closures; the plain N-day date is printed
  cutoff    (S6)      a same-day cutoff stated in the office offset, a response sent from another offset (the same
                      instant in office time printed in brackets) and the day-of-receipt convention

  solver A   day-ordinal integer arithmetic: closed-form interval overlaps, anchor ordinals, integer-cent sums and
             integer office minutes                                                     paradigm integer_arithmetic
  solver B   solver_b.py: its own parser of the rendered row, then day-by-day enumeration (bitmaps of present days,
             per-day ledgers, window lists, closure walks) and epoch minutes             paradigm day_bitmap
  ledger     a third, construction-only view (_ledger_* helpers): it predicts minimal-edit twins and tags traps,
             never the gold
  samplers   S1 rolling; S2 anchor; S3 waiting; S4 sums (purchase / cash); S6 deadlines (addon / cutoff);
             S5 held out (table-first travel log or court notice; other limits; held-out skins; mixdev only)
Error models (every wrong option) are solver A with one rule swapped. Pools below (people, perils, vendors, labels)
are Claude-written stand-ins until the Haiku packs exist (after A38); they live in code and nothing here writes a file.
"""
from __future__ import annotations

import datetime as dt
import random
import sys
from pathlib import Path

_C2_BUILD = Path(__file__).resolve().parents[2]
if str(_C2_BUILD) not in sys.path:
    sys.path.insert(0, str(_C2_BUILD))

from c2_kit import polarity as POL  # noqa: E402
from c2_kit import skin as K  # noqa: E402
from c2_kit import slots as S  # noqa: E402
from c2_kit.distractors import (build_closed, build_options, error_model, ordered_k, register_name,  # noqa: E402
                                uhash)
from c2_kit.lexicon import question_sem  # noqa: E402
from c2_kit.plugin import (C2Plugin, ContractError, KitCtx, QuestionForm, RelationProposal, Spec,  # noqa: E402
                           choose_forms)
from c2_kit.rows import TextBuilder, assemble_row  # noqa: E402

HERE = Path(__file__).resolve().parent
FAMILY = "T01"
DAY = dt.timedelta(days=1)
UNIT_DAY = ("day", "days")
CENT = 100
DATE_LO, DATE_SPAN = dt.date(2025, 3, 2), 1340          # dates 2025-03 .. 2028-11 (crosses 29 Feb 2028)

# ------------------------------------------------------------------------------------------------ pools (stand-ins)
PEOPLE = ("Priya Raman", "Tomas Lindqvist", "Ana Ruiz", "Dana Okafor", "Lena Whitcombe", "Ravi Anand", "Mira Castell",
          "Aiko Brandt", "Jonas Feld", "Nadia Kowal", "Owen Pryce", "Sara Ilves", "Malik Osei", "Ines Duarte",
          "Kofi Mensah", "Hana Sato", "Lucas Brenner", "Eva Marsh", "Theo Kalnins", "Yara Haddad", "Bruno Lacerda",
          "Freya Holm", "Iris Vance", "Omar Saleh", "Clara Weiss", "Felix Ortega", "Maya Lindgren", "Paolo Greco")
RESERVE_PEOPLE = ("Quinn Arbeloa", "Rosa Templeton")                         # G4 renames only
TOPICS = {"rolling": ("visa stay count", "residence day count", "border stay check"),
          "anchor": ("appeal deadline", "claim deadline question", "complaint filing"),
          "waiting": ("insurance claim", "cover question", "loss claim"),
          "purchase": ("purchase request", "supplier order", "buying request"),
          "cash": ("cash ledger check", "branch cash review", "teller ledger review"),
          "addon": ("response deadline", "notice response", "reply deadline"),
          "cutoff": ("response deadline", "notice response", "reply timing question")}
REF_PREFIX = {"rolling": "STAY", "anchor": "CASE", "waiting": "POL", "purchase": "PO", "cash": "LED", "addon": "NTC",
              "cutoff": "NTC"}
ROLL_PAIRS = ((90, 180), (60, 120), (45, 90), (30, 90), (21, 60), (14, 30))
ROLL_PAIRS_S5 = ((75, 150), (40, 100))
ANCHOR_N = (10, 14, 21, 28, 30, 45, 60, 90)
ANCHOR_N_S5 = (20, 35)
ANCHOR_GAPS = (1, 2, 3, 5, 7, 10, 14, 21, 30, 45)
EVENT_PACKS = (("appeal", "decision date", "delivery date"), ("claim", "invoice date", "goods received date"),
               ("complaint", "incident date", "discovery date"), ("dispute", "billing date", "statement date"),
               ("objection", "inspection date", "report date"), ("refund request", "purchase date", "handover date"))
PERILS = ("flood damage", "storm damage", "burst pipe damage", "theft", "fire damage", "subsidence",
          "glass breakage", "power surge damage")
RESERVE_PERIL = "hail damage"
WAIT_DAYS = (7, 10, 14, 15, 21, 30, 45, 60, 90)
VENDORS = ("Brightwell Supply", "Corvane Office", "Halden Tools", "Mirefield Print", "Ostrava Parts", "Quillon Labs",
           "Tessaro Foods", "Vantmoor Electric")
PURCHASE_WINDOWS = (30, 60, 90, 120)
PURCHASE_THRESHOLDS = (300000, 500000, 1000000, 1500000, 2500000)
CASH_THRESHOLDS = (300000, 500000, 1000000, 1500000)
DIRS = {"in": ["deposit"], "out": ["withdrawal"]}
CASH_LABELS = ("in", "out", "both", "neither")
CASH_TEXT = {"in": "Only the deposit total", "out": "Only the withdrawal total", "both": "Both totals",
             "neither": "Neither total"}                    # G0 v2 (H19): the options name the day's totals
ADDON_N = (10, 14, 20, 21, 28, 30)
ADDON_K = (2, 3, 5)
METHODS = {"post": ["post"], "hand": ["hand delivery"], "email": ["email"]}
OFFICE_OFFSETS = (60, 120, 0, -300, 330, 540, -240, 180)                    # minutes east of UTC (fixed; no DST)
SENDER_OFFSETS = (0, 60, 120, 180, -300, -240, -420, 330, 480, 540, 600, -180)
# G0 v4 12.2 (e): the daily cutoff is any clock minute from 12:00 to 22:59 (v3: six fixed clocks, 12:00-23:30). With six
# round clocks the minute digits of a boundary row ("16:59", "17:01") gave the verdict away: the context-only reader
# scored 0.63 on yn_on_time (n = 471, +13 pp, 5 sigma) at the full-generation sample size
CUTOFF_HOURS = (12, 22)
CMP_SEMS = ("cmp.gt", "cmp.ge")

# ------------------------------------------------------------------------------------------------ card text (G0 1.1)
CLOSED_WORLD = "The listed rules and records are complete: no other rule, record or note changes the answer."
RULES = {   # G0 v2 (Haiku pass amb:T01, H1-H41): calendar days, day zero and final days stated on every card
    "rolling": ("Stay rule: the person named in the record may be present on {WIN_CLAUSE}. Day counts are calendar "
                "days, and entry and exit days both count as days present. Only one {M_WIN:adj} window is checked: the "
                "one that ends on the reference date, both ends included; its first day is printed with the record. "
                "The person is over the limit if the number of days present inside that window is more than {N_MAX}, "
                "and within the limit if it is {N_MAX} or fewer. " + CLOSED_WORLD),
    "anchor": ("Filing rule: the {ACTION} must be filed {AN_CLAUSE}: the {EVA_LABEL} and the {EVB_LABEL}. Day zero is "
               "the later of those two dates, and the earlier date plays no part. Day counts are calendar days, and "
               "the final day of the period is {N_DAYS} after day zero. A filing made on any day up to and including "
               "that final day is in time; a filing after it is late. " + CLOSED_WORLD),
    "waiting": ("Cover rule: a loss is covered only after {WAIT_CLAUSE}. That start date is the policy start date or, "
                "for a peril added by a rider, the rider's effective date; the same waiting period applies either way. "
                "Day counts are calendar days. The start date itself is day zero, the waiting period begins on the "
                "next day, and its final day is {W_DAYS} after the start date. A loss that happens after that final "
                "day is covered; a loss on or before it is not. " + CLOSED_WORLD),
    "purchase": ("Purchase rule: every purchase in the log is from the vendor the log names. Add up the new request "
                 "and every earlier purchase made inside the {M_WIN:adj} window that ends on the request date; day "
                 "counts are calendar days, and both ends of the window count. If that total is {CMP}, written quotes "
                 "are required; otherwise the small-purchase path applies. " + CLOSED_WORLD),
    "cash": ("Cash rule: for each day, add up that day's cash deposits and, separately, that day's cash withdrawals; "
             "never net one against the other, and never mix days. A cash report is required for a day if its deposit "
             "total or its withdrawal total is {CMP}, and not otherwise. " + CLOSED_WORLD),
    "addon": ("Response rule: a response is due {N_DAYS} after the notice date, counted in calendar days with the "
              "notice date as day zero. If the notice was sent by post, add {K_DAYS} to that date. The date this gives "
              "is the day reached. If the day reached is a day the office is closed, the due date moves forward to "
              "the next day the office is open; otherwise the day reached is the due date. The office is open on "
              "every day except the listed closures. " + CLOSED_WORLD),
    "cutoff": ("Receipt rule: the office dates every response by office time. Office time is the UTC offset shown "
               "with the office cutoff, and the due date is a date in office time; the record also gives the sending "
               "time in office time, in square brackets. Every response here is sent electronically and arrives at "
               "the instant it is sent. A response that arrives at or before the daily cutoff time counts as received "
               "that day; one that arrives after it counts as received on the next day. The cutoff is the same office "
               "clock time every day. A response is on time if it counts as received on or before the due date, and "
               "late otherwise. " + CLOSED_WORLD),
}

# ------------------------------------------------------------------------------------------------ question forms
QUESTION_FORMS_FROZEN = (       # the 26 forms the pools_v2 wordings were authored for (freeze.py / freeze_v2.py / authors)
    QuestionForm("yn_over", "noul", "over_limit", 1, yes_is_bad=True),
    QuestionForm("yn_within", "noul", "over_limit", -1, "antonym", yes_is_bad=False),
    QuestionForm("yn_not_over", "noul", "over_limit", -1, "syntactic", yes_is_bad=False),
    QuestionForm("ch_days", "choice", answer_set="open"),
    QuestionForm("yn_timely", "noul", "filed_in_time", 1, yes_is_bad=False),
    QuestionForm("yn_late", "noul", "filed_in_time", -1, "antonym", yes_is_bad=True),
    QuestionForm("yn_fail_time", "noul", "filed_in_time", -1, "implicit", yes_is_bad=True),
    QuestionForm("yn_not_timely", "noul", "filed_in_time", -1, "syntactic", yes_is_bad=True),
    QuestionForm("ch_deadline", "choice", answer_set="open"),
    QuestionForm("yn_covered", "noul", "loss_covered", 1, yes_is_bad=False),
    QuestionForm("yn_in_waiting", "noul", "loss_covered", -1, "antonym", yes_is_bad=True),
    QuestionForm("yn_not_covered", "noul", "loss_covered", -1, "syntactic", yes_is_bad=True),
    QuestionForm("ch_first_day", "choice", answer_set="open"),
    QuestionForm("yn_quotes", "noul", "quotes_required", 1, yes_is_bad=True),
    QuestionForm("yn_quotes_without", "noul", "quotes_required", -1, "implicit", yes_is_bad=False),
    QuestionForm("yn_no_quotes", "noul", "quotes_required", -1, "syntactic", yes_is_bad=False),
    QuestionForm("ch_total", "choice", answer_set="open"),
    QuestionForm("yn_cash_report", "noul", "cash_report", 1, yes_is_bad=True),
    QuestionForm("yn_cash_without", "noul", "cash_report", -1, "implicit", yes_is_bad=False),
    QuestionForm("yn_cash_no_report", "noul", "cash_report", -1, "syntactic", yes_is_bad=False),
    QuestionForm("ch_cash_which", "choice", answer_set="closed"),
    QuestionForm("ch_due", "choice", answer_set="open"),
    QuestionForm("yn_on_time", "noul", "on_time", 1, yes_is_bad=False),
    QuestionForm("yn_late_cut", "noul", "on_time", -1, "antonym", yes_is_bad=True),
    QuestionForm("yn_not_on_time", "noul", "on_time", -1, "syntactic", yes_is_bad=True),
    QuestionForm("ch_receipt_day", "choice", answer_set="open"),
)
# G0 v4 section 12 (pilot fix F1): double negation, spec 3.0 ">= 2% of yes/no rows". One positive-polarity base form per
# yes/no predicate, asked with two syntactic negations (negcount k_syn = k_all = 2): an explicit outer frame ("is it not
# the case that" / "is it not true that") around a clause that puts a second "not" on the predicate's own positive word.
DNEG_FORMS = {"yn_over": "yn_dneg_over", "yn_timely": "yn_dneg_timely", "yn_covered": "yn_dneg_covered",
              "yn_quotes": "yn_dneg_quotes", "yn_cash_report": "yn_dneg_cash_report", "yn_on_time": "yn_dneg_on_time"}
QUESTION_FORMS_DNEG = (
    QuestionForm("yn_dneg_over", "noul", "over_limit", 1, yes_is_bad=True),
    QuestionForm("yn_dneg_timely", "noul", "filed_in_time", 1, yes_is_bad=False),
    QuestionForm("yn_dneg_covered", "noul", "loss_covered", 1, yes_is_bad=False),
    QuestionForm("yn_dneg_quotes", "noul", "quotes_required", 1, yes_is_bad=True),
    QuestionForm("yn_dneg_cash_report", "noul", "cash_report", 1, yes_is_bad=True),
    QuestionForm("yn_dneg_on_time", "noul", "on_time", 1, yes_is_bad=False),
)
QUESTION_FORMS = QUESTION_FORMS_FROZEN + QUESTION_FORMS_DNEG
KIND_OF = {}
for _k, _qs in (("rolling", ("yn_over", "yn_within", "yn_not_over", "ch_days")),
                ("anchor", ("yn_timely", "yn_late", "yn_fail_time", "yn_not_timely", "ch_deadline")),
                ("waiting", ("yn_covered", "yn_in_waiting", "yn_not_covered", "ch_first_day")),
                ("purchase", ("yn_quotes", "yn_quotes_without", "yn_no_quotes", "ch_total")),
                ("cash", ("yn_cash_report", "yn_cash_without", "yn_cash_no_report", "ch_cash_which")),
                ("addon", ("ch_due",)),
                ("cutoff", ("yn_on_time", "yn_late_cut", "yn_not_on_time", "ch_receipt_day"))):
    for _q in _qs:
        KIND_OF[_q] = _k
for _base, _dq in DNEG_FORMS.items():
    KIND_OF[_dq] = KIND_OF[_base]
POLARITY = {q.qform: q.polarity for q in QUESTION_FORMS}

# ------------------------------------------------------------------------------------------------ shares
SAMPLER_KINDS = {"S1": (("rolling", 1.0),), "S2": (("anchor", 1.0),), "S3": (("waiting", 1.0),),
                 "S4": (("purchase", 0.5), ("cash", 0.5)), "S6": (("addon", 0.4), ("cutoff", 0.6)),
                 "S5": (("rolling", 0.5), ("anchor", 0.5))}
BASE_FORMS = {"rolling": ("yn_over", "ch_days"), "anchor": ("yn_timely", "ch_deadline"),
              "waiting": ("yn_covered", "ch_first_day"), "purchase": ("yn_quotes", "ch_total"),
              "cash": ("yn_cash_report", "ch_cash_which"), "addon": (None, "ch_due"),
              "cutoff": ("yn_on_time", "ch_receipt_day")}
P_YN = {"rolling": 0.43, "anchor": 0.43, "waiting": 0.43, "purchase": 0.43, "cash": 0.43, "addon": 0.0,
        "cutoff": 0.72}
COMPLEMENTS = {"yn_over": (("yn_within", 0.6), ("yn_not_over", 0.4)),
               "yn_timely": (("yn_late", 0.35), ("yn_fail_time", 0.3), ("yn_not_timely", 0.35)),
               "yn_covered": (("yn_in_waiting", 0.6), ("yn_not_covered", 0.4)),
               "yn_quotes": (("yn_quotes_without", 0.6), ("yn_no_quotes", 0.4)),
               "yn_cash_report": (("yn_cash_without", 0.6), ("yn_cash_no_report", 0.4)),
               "yn_on_time": (("yn_late_cut", 0.6), ("yn_not_on_time", 0.4))}
# G-TW (c2_kit.relations): a complement of a double negation (negation cues k_all 2) must differ by exactly one cue, so
# its only complement is the single-negation syntactic form of the same predicate
_QF = {q.qform: q for q in QUESTION_FORMS_FROZEN}
for _b, _dq in DNEG_FORMS.items():
    COMPLEMENTS[_dq] = tuple((f, 1.0) for f, _w in COMPLEMENTS[_b] if _QF[f].complement_kind == "syntactic")
P_DNEG = 0.10                                  # yes/no bases asked as the double-negation form (once a wording is admitted)
CASH_TARGETS = (("in", 0.25), ("out", 0.25), ("both", 0.25), ("neither", 0.25))   # G0 v4: closed label set, uniform
P_EQUIV, P_TWIN, P_BOUNDARY = 0.12, 0.42, 0.45
P_COMPLEMENT = {False: 0.7, True: 0.3}         # by the base form's yes_is_bad: balances yes = bad to about 50%
# G0 v4 section 12 (pilot fix F2): option cues. The answer of these forms is a count or an amount, never a verdict, so
# the "exactly on a boundary" target (present N / N + 1, a total at the threshold) would put the printed limit itself
# among the options as the gold (G7: opt:61 days, opt:000)
NO_BOUNDARY_FORMS = ("ch_days", "ch_total")
# every option of an open set shares the gold's visible cues (printed in the card or record; digit count of a count or
# an amount), so no rule on them can find the gold (G6 options-only, G7 kind:verbatim_in_text / longest / shortest)
CUE_MATCH_FORMS = ("ch_days", "ch_deadline", "ch_first_day", "ch_total", "ch_due")
LENGTH_MATCH_FORMS = ("ch_days", "ch_total")
# ch_receipt_day: the record prints every date near the answer (due date, sending day in two offsets), so equal value
# cues leave no set to build (1.6% of rows); measured, the gold is printed as often as a wrong option (63% / 59%). What
# differs is only the SURFACE (timestamps against a date form), so its options are shown in a date form the record never
# prints, and no option can be a verbatim copy of anything printed
RECEIPT_OPTION_FORMS = ("iso", "dmy", "mdy", "dmy_abbr")
CARDS = 8                                       # per (sampler, kind): the card fixes the pack and the comparator

# ------------------------------------------------------------------------------------------------ error models
register_name("t01_whole_stays", "counts every listed stay in full, ignoring the window's first day")
register_name("t01_straddle_dropped", "drops a stay that began before the window's first day")
register_name("t01_straddle_full", "counts a stay that began before the window's first day in full")
register_name("t01_request_only", "judges the new request alone, without the earlier purchases in the window")
register_name("t01_prior_only", "adds the earlier purchases in the window but leaves out the new request")
register_name("t01_ignore_window", "adds every listed purchase, inside the window or not")
register_name("t01_sum_across_days", "adds transactions from other days into the day's totals")
register_name("t01_skip_addon", "leaves out the postal add-on for a notice sent by post")
register_name("t01_addon_not_post", "adds the postal add-on to a notice that was not sent by post")
register_name("t01_ignore_closure", "keeps a due date that falls on a listed office closure")
register_name("t01_ignore_cutoff", "dates a response by its arrival day and ignores the daily cutoff")
register_name("t01_due_date_read", "gives the due date instead of working out the day of receipt")
register_name("t01_window_one_long", "starts the window one day before its printed first day")
register_name("t01_window_one_short", "leaves the window's printed first day out of the window")
register_name("t01_exit_extra_day", "counts each stay one day longer, through the day after its exit")
register_name("t01_both_ends_early", "counts day zero as day 1 and also leaves out the final day (two days early)")
register_name("t01_both_ends_late", "starts counting the day after day zero and also counts one day past the final "
                                    "day (two days late)")
register_name("t01_business_days", "counts the period in weekdays (Monday to Friday) instead of calendar days")
register_name("t01_double_request", "counts the new request twice: once as a purchase in the window and once as the "
                                    "request")
register_name("t01_always_next_day", "counts every response as received on the day after it arrives, before the "
                                     "cutoff or not")
register_name("t01_sender_date", "dates the response by the sender's own calendar date and ignores the cutoff")
register_name("t01_utc_date", "applies the cutoff to the UTC clock time and date instead of office time")
register_name("t01_early_previous_day", "dates a response that arrives at or before the cutoff to the previous day")
register_name("t01_last_prior_only", "adds only the most recent earlier purchase in the window to the new request")
CHOICE_EM = {
    "ch_days": ("calendar_year", "t01_whole_stays", "t01_straddle_dropped", "t01_straddle_full",
                "drop_inclusive_endpoint", "t01_window_one_long", "t01_window_one_short", "t01_exit_extra_day"),
    "ch_deadline": ("earlier_anchor", "count_day0", "off_by_one_late", "t01_both_ends_early", "t01_both_ends_late",
                    "t01_business_days"),
    "ch_first_day": ("count_day0", "off_by_one_late", "wrong_anchor", "t01_both_ends_early", "t01_both_ends_late",
                     "t01_business_days"),
    "ch_total": ("t01_request_only", "t01_prior_only", "t01_ignore_window", "drop_inclusive_endpoint",
                 "add_exclusive_endpoint", "t01_double_request", "t01_last_prior_only"),
    "ch_cash_which": ("netting", "t01_sum_across_days", "more_than_as_at_least", "at_least_as_more_than"),
    "ch_due": ("t01_skip_addon", "t01_addon_not_post", "t01_ignore_closure", "wrong_roll_direction", "count_day0",
               "off_by_one_late", "t01_both_ends_early", "t01_both_ends_late", "t01_business_days"),
    "ch_receipt_day": ("t01_ignore_cutoff", "skip_offset_conversion", "off_by_one_late", "t01_due_date_read",
                       "drop_inclusive_endpoint", "t01_always_next_day", "t01_sender_date", "t01_utc_date",
                       "t01_early_previous_day"),
}
# Ordered open sets (dates, counts, cents): the gold's sorted rank among the options is label-blind (kit target_rank);
# two partial sums whose total is the gold never share a set (the "sum of two options" cue).
EXCLUSIVE_EM = {"ch_total": (("t01_request_only", "t01_prior_only"),)}
K_DRAW = (3, 4)                                 # label-blind option count before ordered_k sizes it to the error range
ALL_EM = tuple(dict.fromkeys(n for names in CHOICE_EM.values() for n in names))
CHOICE_VALUE = {"ch_days": "present", "ch_deadline": "deadline", "ch_first_day": "first", "ch_total": "total",
                "ch_cash_which": "label", "ch_due": "due", "ch_receipt_day": "receipt"}   # solver A value per form
SWAP_CMP = {"more_than_as_at_least": ("cmp.gt", "cmp.ge"), "at_least_as_more_than": ("cmp.ge", "cmp.gt")}


# ------------------------------------------------------------------------------------------------ helpers

def _draw(u: float, shares: tuple) -> str:
    acc = 0.0
    for key, share in shares:
        acc += share
        if u < acc:
            return key
    return shares[-1][0]


CASH_BLOCK_PAIRS = 128                          # seed pairs per dealing block of the ch_cash_which label (G0 v4 12.7)
_CASH_DEAL: dict = {}


def _cash_which_pair(sampler: str, pair: int) -> bool:
    """True iff seed pair `pair` of `sampler` asks ch_cash_which (the same label-blind draws sample() makes)."""
    kind = _draw(uhash(FAMILY, "kind", sampler, pair), SAMPLER_KINDS[sampler])
    yn_form, ch_form = BASE_FORMS[kind]
    qform = yn_form if yn_form and uhash(FAMILY, "qform", sampler, pair) < P_YN[kind] else ch_form
    return qform == "ch_cash_which"


def _cash_which_label(sampler: str, seed: int) -> str:
    """G0 v4 12.7: the ch_cash_which label is dealt, not drawn. Stateless and seed-deterministic: the seeds of a block of
    CASH_BLOCK_PAIRS seed pairs that ask ch_cash_which are numbered in seed order and take the labels of consecutive
    decks of the four labels (each deck a seeded shuffle), so every label has 25% of a block to within one row. Label
    shares per card follow the G0 rule (25% each); the card is drawn independently of the label."""
    pair = seed // 2
    block = pair // CASH_BLOCK_PAIRS
    key = (sampler, block)
    if key not in _CASH_DEAL:
        seeds = [s for p in range(block * CASH_BLOCK_PAIRS, (block + 1) * CASH_BLOCK_PAIRS)
                 if _cash_which_pair(sampler, p) for s in (2 * p, 2 * p + 1)]
        labels = []
        for d in range((len(seeds) + 3) // 4):
            deck = [k for k, _share in CASH_TARGETS]
            deck.sort(key=lambda k: uhash(FAMILY, "cashdeal", sampler, block, d, k))
            labels += deck
        _CASH_DEAL[key] = {s: labels[i] for i, s in enumerate(seeds)}
    return _CASH_DEAL[key][seed]


def _yes_target(sampler: str, seed: int) -> bool:
    """Label-first target bit: the two seeds of a pair (2k, 2k + 1) share kind and question form and get opposite
    targets, so every yes/no base form is exactly 50% yes over any run of whole seed pairs (G0 section 4)."""
    return (uhash(FAMILY, "yes", sampler, seed // 2) < 0.5) != bool(seed % 2)


def _rand_date(rng: random.Random, margin: int = 0) -> dt.date:
    return DATE_LO + dt.timedelta(days=margin + rng.randrange(DATE_SPAN - 2 * margin))


def _o(d) -> int:
    """Proleptic day ordinal of a date (or of a datetime's local date)."""
    return d.toordinal()


def _iso(ordinal: int) -> str:
    return dt.date.fromordinal(ordinal).isoformat()


def _tz(minutes: int) -> dt.timezone:
    return dt.timezone(dt.timedelta(minutes=minutes))


def _off(t: dt.datetime) -> int:
    off = t.utcoffset()
    return off.days * 1440 + off.seconds // 60


def _utc_min(t: dt.datetime) -> int:
    """Integer UTC minutes on the ordinal scale (solver A's time arithmetic)."""
    return t.toordinal() * 1440 + t.hour * 60 + t.minute - _off(t)


def _cmp(sem: str, total: int, bound: int) -> bool:
    if sem == "cmp.gt":
        return total > bound
    if sem == "cmp.ge":
        return total >= bound
    raise ContractError(f"comparator {sem}")


def _compose(rng: random.Random, total: int, parts: int, minimum: int = 1) -> list:
    """`parts` integers >= minimum that sum to total (a seeded composition)."""
    if parts <= 0:
        return []
    spare = total - parts * minimum
    if spare < 0:
        raise ValueError("composition does not fit")
    cuts = sorted(rng.randrange(spare + 1) for _ in range(parts - 1))
    bounds = [0] + cuts + [spare]
    return [minimum + bounds[i + 1] - bounds[i] for i in range(parts)]


def _weekdays_after(ordinal: int, n: int) -> int:
    """The ordinal reached by counting n weekdays (Monday to Friday) after day `ordinal` (t01_business_days)."""
    d = ordinal
    while n > 0:
        d += 1
        if dt.date.fromordinal(d).weekday() < 5:
            n -= 1
    return d


def _shift(mods) -> int:
    """The day shift of the off-by-one error models (count_day0 -1, off_by_one_late +1, both ends -2 / +2)."""
    return (-("count_day0" in mods) + ("off_by_one_late" in mods) - 2 * ("t01_both_ends_early" in mods)
            + 2 * ("t01_both_ends_late" in mods))


def _dollars(cents: float) -> int:
    return int(cents // CENT) * CENT


def _order_key(answer) -> object:
    """Choice answers are ISO dates, day counts or cents: each sorts in its own natural order."""
    return answer


def _answer(qform: str, verdict: bool) -> int:
    return int(verdict) if POLARITY[qform] == 1 else int(not verdict)


# G0 v4 section 12.4 (pilot fix F3): wordings the family leaves out of its pool although G-LEX admitted them. A label-blind
# screen on the wording text alone (never a row, never a gold). The first two word the cutoff rule by the day the response
# ARRIVES or is SENT, while the card decides on the day the office COUNTS it as received (the two differ for a response
# that arrives on the due date after the daily cutoff). The third asks about the whole ledger, while the rule decides for
# the one day under review (46% of cash records carry a large total on another day). A careful reader answers each the
# other way round for those rows: a wrong gold risk, so they leave the pool and the rows are regenerated.
WORDING_QUARANTINE = {
    "Was notice {REF} answered late, with its response arriving after the due date?":
        "G0 v4 12.4: 'arriving after the due date' reads the arrival day, not the day the office counts as received",
    "Is it true that the response to notice {REF} was not sent on time?":
        "G0 v4 12.4: 'sent on time' reads the sending day, not the day the office counts as received",
    "Must ledger {REF} include a cash report under the cash rule?":
        "G0 v4 12.4: asks about the whole ledger, the rule decides for the day under review",
}
# regexes: the lexical negative (antonym) predicate phrases of the family's antonym forms (c2_kit.polarity P1 / P2): the
# stay limit read as "within", filing "late", a loss "in the waiting period"; none occurs in a positive wording
POLARITY_NEGATIVE_PHRASES = (r"(?:within|inside) the stay limit", r"(?:too )?late",
                             r"after the (?:final day|deadline|due date)(?: of the filing period)?",
                             r"(?:during|within|inside) the waiting period")


class T01(C2Plugin):
    FAMILY = FAMILY
    TIER = "everyday"
    G0_LITE = HERE / "G0_SPEC_v4.md"
    # G3-H topic describe. G0 v4 section 3 (mode F) writes "the" before TOPIC and the generator's topic is the bare phrase, so
    # the schema says to leave the article out (iteration 3, A44 a; iteration 2: all 200 mode-F rows mismatched on "the ").
    # The pool-era G3-H task files carry TOPIC_DESCRIBE_AUTHORED; conftest.py swaps it in for their rebuilds.
    TOPIC_DESCRIBE_AUTHORED = "what the message is about, as written"
    TOPIC_DESCRIBE_I3 = ("what the message is about, as written, WITHOUT the leading word \"the\" (the passage writes "
                         "\"about the ...\"; the topic does not include that \"the\")")
    TOPIC_DESCRIBE = TOPIC_DESCRIBE_I3
    G0_SHA256 = "7f9ab6b636c411830e201452284842bd1b9e0acad14701a5008a413a29a771b3"   # frozen v4 (G0_SPEC_v4.md, section 12; 12.7 added in fix iteration 2c)
    G0_SHA256_AUTHORED = "4dad231680dc6b09d4c7240cac21ef8f382075d4dd0516b79970c888db0fe61c"   # v3 = G0_SPEC.md, the
    # version every pools_v2 task, answer and manifest was authored against (freeze.py, freeze_v2.py, haiku_author.py)
    # the one Haiku G0-lite ambiguity pass this freeze resolves (workflow c2-data-stage-a, Ambiguity phase): it read
    # v1 (sha256 749c85b4...) and raised 41 points, resolved as H1-H41 in G0 section 8
    G0_HAIKU_TASK = "c2-data-stage-a/amb:T01"
    G0_AMBIGUITY_PASS = {"task_id": "c2-data-stage-a/amb:T01", "model": "haiku", "points": 41,
                         "read_g0_sha256": "749c85b408dbfaa87347209cd7c2db09f90fca3d7bc3e6f7af4df006b6e54b66"}
    SAMPLERS = ("S1", "S2", "S3", "S4", "S6", "S5")
    HELD_OUT_SAMPLERS = ("S5",)
    PARADIGM_A = "integer_arithmetic"
    PARADIGM_B = "day_bitmap"
    SOLVER_B_MODULE = "families.T01.solver_b"
    QFORMS = {q.qform: q for q in QUESTION_FORMS}
    FROZEN_QFORMS = {q.qform: q for q in QUESTION_FORMS_FROZEN}
    LABEL_WORDS = ("late", "timely", "covered", "uncovered", "over the limit", "within the limit", "on time",
                   "in time", "written quotes", "small-purchase path", "cash report", "only the deposit total",
                   "only the withdrawal total", "both totals", "neither total")
    CLOSED_WORLD_SENTENCE = CLOSED_WORLD
    REGISTERS = ("memo", "email", "chat", "ticket", "json", "yaml", "log", "transcript", "faq", "letter")
    HELD_OUT_REGISTERS = ("faq", "letter")
    GSL_EXCEPTIONS = {}
    NAME_ALLOW = ("UTC",)
    POLARITY_CHECK = True                       # c2_kit.polarity: every yes/no wording reads with its form's polarity
    POLARITY_NEGATIVES = POLARITY_NEGATIVE_PHRASES
    POLARITY_STRICT_FRAMES = True               # no negative polar question "aux + subject + not" (P4)
    CUE_MATCH = True                            # G0 v4 12.2 (tests of hand-built arithmetic switch it off per instance)

    def __init__(self, lexicon=None):
        super().__init__(lexicon)
        self._ems = None
        self._forms_by_sem = {}
        self._screened: list = []               # [(ctx, screened ctx, {wording skin id: problems})]
        self.dneg_ok = {q: self._clean_forms(q) for q in DNEG_FORMS.values()}

    def _clean_forms(self, qform: str) -> bool:
        """True when the lexicon holds an admitted TRAINING question form of `qform` whose wording passes the polarity
        rule and is not quarantined (label-blind: the pool, not a row). Without a lexicon (contract checks): True."""
        if self.lexicon is None:
            return True
        sem = question_sem(FAMILY, qform)
        return any(f.sem_id == sem and not f.held_out and self.lexicon.status(f.form_id) == "admitted"
                   and f.text not in WORDING_QUARANTINE and not POL.form_problems(self, qform, f.text)
                   for f in self.lexicon.forms.values())

    def ctx_for(self, spec, ctx):
        """The kit context without the wordings that break the polarity rule (c2_kit.polarity) or are quarantined
        (WORDING_QUARANTINE), so neither render() nor the pipeline's complement partner can pick one. Cached."""
        for c, screened, _bad in self._screened:
            if c is ctx or screened is ctx:
                return screened
        screened, bad = POL.screen(ctx, self)
        extra = {sid: [WORDING_QUARANTINE[sk.text]] for sid, sk in screened.skins.items()
                 if sk.kind == "wording" and sk.text in WORDING_QUARANTINE}
        if extra:
            screened = KitCtx(skins={k: v for k, v in screened.skins.items() if k not in extra},
                              lexicon=screened.lexicon)
            bad = {**bad, **extra}
        self._screened.append((ctx, screened, bad))
        return screened

    def quarantined_wordings(self, ctx) -> dict:
        """{wording skin id: problems} for the wordings ctx_for() leaves out of `ctx`."""
        self.ctx_for(None, ctx)
        return next(bad for c, _s, bad in self._screened if c is ctx)

    # ============================================================================================ sampling
    def sample(self, seed: int, sampler: str) -> Spec:
        if sampler not in self.SAMPLERS:
            raise ContractError(f"sampler {sampler}")
        if self.lexicon is None:
            raise ContractError("T01 needs its lexicon registry (T01(lexicon=...))")
        rng = random.Random(f"{FAMILY}|{sampler}|{seed}")
        pair = seed // 2
        kind = _draw(uhash(FAMILY, "kind", sampler, pair), SAMPLER_KINDS[sampler])
        yn_form, ch_form = BASE_FORMS[kind]
        qform = yn_form if yn_form and uhash(FAMILY, "qform", sampler, pair) < P_YN[kind] else ch_form
        if (qform == yn_form and yn_form in DNEG_FORMS and self.dneg_ok[DNEG_FORMS[yn_form]]
                and uhash(FAMILY, "dneg", sampler, pair) < P_DNEG):
            qform = DNEG_FORMS[yn_form]      # only while the pool holds a clean, admitted double-negation wording
        card = rng.randrange(CARDS)
        c = {"seed": seed, "sampler": sampler, "kind": kind, "qform": qform, "card": card,
             "yes": _yes_target(sampler, seed), "boundary": rng.random() < P_BOUNDARY and qform not in NO_BOUNDARY_FORMS,
             "style": "table" if sampler in self.HELD_OUT_SAMPLERS else "list"}
        slots = {"PERSON": S.name_slot(rng.choice(PEOPLE)),
                 "REF": S.id_slot(f"{REF_PREFIX[kind]}-{rng.randrange(1000, 9999)}"),
                 "TOPIC": S.name_slot(TOPICS[kind][card % len(TOPICS[kind])])}
        body, structure, tags = getattr(self, f"_sample_{kind}")(rng, c)
        slots.update(body)
        spec = Spec(FAMILY, sampler, seed, f"{FAMILY}:{sampler}:{kind}:c{card:02d}", qform, slots,
                    structure={"kind": kind, "style": c["style"], **structure}, depth=2, deep=False,
                    tags=tuple(sorted(set(tags))), pack=f"t01-{kind}-p{card % 4}")
        spec = self.derive(spec)
        return spec.replace(tags=tuple(sorted(set(spec.tags) | set(self._tags(spec)))))

    def _clause(self, sem: str, rng: random.Random, bind: dict) -> S.Slot:
        if sem not in self._forms_by_sem:
            self._forms_by_sem[sem] = sorted(f for f, x in self.lexicon.forms.items() if x.sem_id == sem
                                             and x.kind != "question" and self.lexicon.status(f) == "admitted")
        ids = self._forms_by_sem[sem]
        if not ids:
            raise ContractError(f"no admitted lexicon form for {sem}")
        return self.lexicon.clause(rng.choice(ids), bind=bind)

    # -------------------------------------------------------------------------------------------- rolling
    def _sample_rolling(self, rng, c):
        pairs = ROLL_PAIRS_S5 if c["sampler"] == "S5" else ROLL_PAIRS
        n, m = pairs[(c["card"] + rng.randrange(2)) % len(pairs)]
        ref = _rand_date(rng, 200)
        ws = ref - (m - 1) * DAY
        over = c["yes"]
        if c["qform"] == "ch_days":
            # a count answer: any present count in one contiguous range around the limit, N and N + 1 included (G0 v4
            # 12.2: a gap at the limit makes "N + 1 days" an option that is never the gold)
            present = rng.randint(max(1, n - max(3, n // 2)), n + 1 + max(3, n // 4))
        elif c["boundary"]:
            present = n + 1 if over else n
        elif over:
            present = n + 2 + rng.randrange(max(3, n // 4))
        else:
            present = max(1, n - 1 - rng.randrange(max(3, n // 2)))
        n_in = min(rng.choice((1, 2, 2, 3)), present)
        choice = c["qform"] == "ch_days"                 # more straddles and early stays: more error models apply
        straddle = rng.random() < (0.8 if choice else 0.45)
        pre = n_in < 3 and rng.random() < (0.5 if choice else 0.35)
        parts = _compose(rng, present, n_in)
        free = m - present - (n_in - 1)
        if free < 0:
            raise ContractError("rolling: the stays do not fit the window")
        gaps = [0] * (n_in + 1)
        open_gaps = list(range(1 if straddle or rng.random() < 0.25 else 0, n_in + 1))
        for _ in range(free):
            gaps[rng.choice(open_gaps)] += 1
        segs, pos = [], ws + gaps[0] * DAY
        for k, length in enumerate(parts):
            seg_end = pos + (length - 1) * DAY
            segs.append([pos, seg_end])
            pos = seg_end + (2 + gaps[k + 1]) * DAY
        if straddle:
            segs[0][0] = ws - (1 + rng.randrange(30)) * DAY
        stays = [tuple(s) for s in segs]
        if pre:
            edge = not straddle and gaps[0] >= 1 and rng.random() < 0.4
            end = min(ws - DAY, stays[0][0] - 2 * DAY) - (0 if edge else rng.randrange(25)) * DAY
            stays.insert(0, (end - rng.randrange(20) * DAY, end))
        slots = {"N_MAX": S.count_slot(n, UNIT_DAY), "M_WIN": S.count_slot(m, UNIT_DAY), "REF_DATE": S.date_slot(ref),
                 "WIN_CLAUSE": self._clause("win.rolling_cap", rng, {"N": "N_MAX", "M": "M_WIN"})}
        names = []
        for k, (a, b) in enumerate(stays, 1):
            slots[f"SI_{k}"], slots[f"SO_{k}"] = S.date_slot(a), S.date_slot(b)
            names.append([f"SI_{k}", f"SO_{k}"])
        return slots, {"stays": names}, (["boundary"] if present in (n, n + 1) else [])

    # -------------------------------------------------------------------------------------------- anchor
    def _sample_anchor(self, rng, c):
        n = rng.choice(ANCHOR_N_S5 if c["sampler"] == "S5" else ANCHOR_N)
        action, la, lb = EVENT_PACKS[c["card"] % len(EVENT_PACKS)]
        filed = c["qform"] != "ch_deadline"
        gap = rng.choice(ANCHOR_GAPS)
        e, tags = None, []
        if filed:
            timely = c["yes"]
            if c["boundary"]:
                e = n if timely else n + 1
            else:
                e = rng.randrange(n) if timely else n + 2 + rng.randrange(30)
            if timely and e + gap <= n and rng.random() < 0.6:          # the earlier anchor would read late
                gap = n - e + 1 + rng.randrange(10)
        later = _rand_date(rng, 120)
        earlier = later - gap * DAY
        a_later = rng.random() < 0.5
        ev_a, ev_b = (later, earlier) if a_later else (earlier, later)
        slots = {"ACTION": S.name_slot(action), "EVA_LABEL": S.name_slot(la), "EVB_LABEL": S.name_slot(lb),
                 "EVENT_A": S.date_slot(ev_a), "EVENT_B": S.date_slot(ev_b), "N_DAYS": S.count_slot(n, UNIT_DAY),
                 "AN_CLAUSE": self._clause("win.later_anchor", rng, {"N": "N_DAYS"})}
        if filed:
            slots["FILED_DATE"] = S.date_slot(later + e * DAY)
            if e in (n, n + 1):
                tags.append("boundary")
        return slots, {"filed": filed}, tags

    # -------------------------------------------------------------------------------------------- waiting
    def _sample_waiting(self, rng, c):
        w = rng.choice(WAIT_DAYS)
        start = _rand_date(rng, 300)
        rider = rng.random() < 0.5
        anchor = start + (10 + rng.randrange(200)) * DAY if rider else start
        slots = {"PERIL": S.name_slot(PERILS[(c["card"] + rng.randrange(3)) % len(PERILS)]),
                 "START_DATE": S.date_slot(start), "W_DAYS": S.count_slot(w, UNIT_DAY),
                 "WAIT_CLAUSE": self._clause("win.wait_after", rng, {"W": "W_DAYS"})}
        if rider:
            slots["RIDER_DATE"] = S.date_slot(anchor)
        loss = c["qform"] != "ch_first_day"
        tags = []
        if loss:
            covered = c["yes"]
            if c["boundary"]:
                e = w + 1 if covered else w
            else:
                e = w + 2 + rng.randrange(60) if covered else 1 + rng.randrange(w - 1)
            slots["LOSS_DATE"] = S.date_slot(anchor + e * DAY)
            if e in (w, w + 1):
                tags.append("boundary")
        return slots, {"rider": rider, "loss": loss}, tags

    # -------------------------------------------------------------------------------------------- purchase
    def _sample_purchase(self, rng, c):
        m = rng.choice(PURCHASE_WINDOWS)
        thr = rng.choice(PURCHASE_THRESHOLDS)
        sem = CMP_SEMS[1] if c["card"] % 4 == 3 else CMP_SEMS[0]
        req = _rand_date(rng, 200)
        ws = req - (m - 1) * DAY
        yes = c["yes"]
        if c["qform"] == "ch_total":                      # an amount answer: one contiguous range, no gap at the threshold
            total = _dollars(thr * (0.6 + rng.random() * 0.8))
        elif c["boundary"]:
            total = (thr + CENT if yes else thr) if sem == "cmp.gt" else (thr if yes else thr - CENT)
        else:
            frac = 0.05 + rng.random() * 0.35
            total = _dollars(thr * (1 + frac)) if yes else _dollars(thr * (1 - frac))
        n_in = rng.choice((1, 1, 2, 2, 3))
        n_out = rng.choice((0, 1, 1, 2))
        req_amt = max(CENT, _dollars(total * (0.15 + rng.random() * 0.45)))
        rest = total - req_amt
        parts = [p * CENT for p in _compose(rng, rest // CENT, n_in)]
        span = (req - ws).days                                          # in-window prior dates: ws .. req - 1
        dates_in = [ws + rng.randrange(span) * DAY for _ in range(n_in)]
        if rng.random() < 0.35:
            dates_in[0] = ws                                            # a purchase on the window's first day
        dates_out = [ws - (1 + rng.randrange(120)) * DAY for _ in range(n_out)]
        if dates_out and rng.random() < 0.35:
            dates_out[0] = ws - DAY                                     # the day before the window starts
        amts_out = [_dollars(thr * (0.1 + rng.random() * 0.5)) for _ in range(n_out)]
        prior = sorted(list(zip(dates_in, parts)) + list(zip(dates_out, amts_out)),
                       key=lambda x: (x[0], uhash(c["seed"], "ord", x[1])))
        slots = {"VENDOR": S.name_slot(VENDORS[(c["card"] + rng.randrange(2)) % len(VENDORS)]),
                 "M_WIN": S.count_slot(m, UNIT_DAY), "REQ_DATE": S.date_slot(req), "REQ_AMT": S.cents_slot(req_amt),
                 "THRESHOLD": S.cents_slot(thr), "CMP": self._clause(sem, rng, {"X": "THRESHOLD"})}
        names = []
        for k, (d, a) in enumerate(prior, 1):
            slots[f"PD_{k}"], slots[f"PA_{k}"] = S.date_slot(d), S.cents_slot(a)
            names.append([f"PD_{k}", f"PA_{k}"])
        edge = total in (thr - CENT, thr, thr + CENT)
        return slots, {"prior": names}, (["boundary"] if edge else [])

    # -------------------------------------------------------------------------------------------- cash
    def _sample_cash(self, rng, c):
        thr = rng.choice(CASH_THRESHOLDS)
        sem = CMP_SEMS[1] if c["card"] % 4 == 3 else CMP_SEMS[0]
        day = _rand_date(rng, 30)
        if c["qform"] == "ch_cash_which":
            rng.random()                                # keeps the row's draw stream as it was (the label is dealt)
            label = _cash_which_label(c["sampler"], c["seed"])
        else:
            label = rng.choices(("in", "out", "both"), weights=(4, 4, 2))[0] if c["yes"] else "neither"
        over = {"in": label in ("in", "both"), "out": label in ("out", "both")}
        edge_dir = rng.choice(("in", "out")) if c["boundary"] else None
        totals = {}
        for d in ("in", "out"):
            if d == edge_dir:
                if over[d]:
                    totals[d] = thr + CENT if sem == "cmp.gt" else thr
                else:
                    totals[d] = thr if sem == "cmp.gt" else thr - CENT
            elif over[d]:
                totals[d] = _dollars(thr * (1.05 + rng.random() * 0.45))
            else:
                totals[d] = 0 if rng.random() < 0.15 else _dollars(thr * (0.2 + rng.random() * 0.75))
        if totals["in"] == totals["out"] == 0:
            totals[rng.choice(("in", "out"))] = _dollars(thr * (0.2 + rng.random() * 0.5))
        txns = []
        for d in ("in", "out"):
            if totals[d]:
                k = 1 if totals[d] < 2 * CENT else rng.choice((1, 2, 2))
                for amt in _compose(rng, totals[d] // CENT, k):
                    txns.append((day, d, amt * CENT))
        for _ in range(rng.choice((1, 1, 2))):
            other = day + rng.choice((-2, -1, 1, 2)) * DAY
            txns.append((other, rng.choice(("in", "out")), _dollars(thr * (0.2 + rng.random() * 0.6))))
        txns.sort(key=lambda t: (t[0], uhash(c["seed"], "txn", t[1], t[2])))
        slots = {"DAY": S.date_slot(day), "THRESHOLD": S.cents_slot(thr),
                 "CMP": self._clause(sem, rng, {"X": "THRESHOLD"})}
        names = []
        for k, (d, direction, amt) in enumerate(txns, 1):
            slots[f"TD_{k}"], slots[f"TT_{k}"] = S.date_slot(d), S.category_slot(direction, DIRS)
            slots[f"TA_{k}"] = S.cents_slot(amt)
            names.append([f"TD_{k}", f"TT_{k}", f"TA_{k}"])
        return slots, {"txns": names}, (["boundary"] if edge_dir else [])

    # -------------------------------------------------------------------------------------------- addon
    def _sample_addon(self, rng, c):
        n = ADDON_N[(c["card"] + rng.randrange(3)) % len(ADDON_N)]
        k = rng.choice(ADDON_K)
        notice = _rand_date(rng, 30)
        method = rng.choices(("post", "hand", "email"), weights=(2, 1, 1))[0]
        base = notice + n * DAY
        reached = base + (k * DAY if method == "post" else dt.timedelta(0))
        closed = set()
        if rng.random() < 0.5:
            closed.add(reached)
            if rng.random() < 0.35:
                closed.add(reached + DAY)
        if method == "post" and rng.random() < 0.3:
            closed.add(base)
        if method != "post" and rng.random() < 0.3:
            closed.add(base + k * DAY)
        while len(closed) < 3 and rng.random() < 0.4:
            closed.add(notice + (2 + rng.randrange(n + k + 6)) * DAY)
        slots = {"NOTICE_DATE": S.date_slot(notice), "METHOD": S.category_slot(method, METHODS),
                 "N_DAYS": S.count_slot(n, UNIT_DAY), "K_DAYS": S.count_slot(k, UNIT_DAY)}
        names = []
        for i, d in enumerate(sorted(closed), 1):
            slots[f"CL_{i}"] = S.date_slot(d)
            names.append(f"CL_{i}")
        return slots, {"closed": names}, []

    # -------------------------------------------------------------------------------------------- cutoff
    def _sample_cutoff(self, rng, c):
        office = OFFICE_OFFSETS[c["card"] % len(OFFICE_OFFSETS)]
        hh, mm = rng.randint(*CUTOFF_HOURS), rng.randrange(60)
        sender = rng.choice([o for o in SENDER_OFFSETS if o != office])
        due = _rand_date(rng, 30)
        cutoff = dt.datetime(due.year, due.month, due.day, hh, mm, tzinfo=_tz(office))
        if self.QFORMS[c["qform"]].qtype == "noul":
            on_time = c["yes"]
            if c["boundary"]:
                delta = rng.choice((0, -1, -5)) if on_time else rng.choice((1, 5))
            elif on_time:
                delta = -(6 + rng.randrange(36 * 60))
            else:
                delta = 6 + rng.randrange(30 * 60)
        else:                                                   # ch_receipt_day: after the daily cutoff or not
            after, cut = c["yes"], hh * 60 + mm
            if c["boundary"]:
                minute = rng.choice((1, 5)) if after else -rng.choice((0, 1, 5))
            else:
                minute = 6 + rng.randrange(1439 - cut - 5) if after else -(6 + rng.randrange(cut - 5))
            delta = 1440 * rng.randrange(-3, 2) + minute
        sent = (cutoff + dt.timedelta(minutes=delta)).astimezone(_tz(sender))
        slots = {"DUE_DATE": S.date_slot(due), "SENT": S.datetime_slot(sent)}
        return slots, {"office": office, "cut": [hh, mm]}, []

    # ============================================================================================ derive
    def derive(self, spec: Spec) -> Spec:
        st, v = spec.structure, {k: s.value for k, s in spec.slots.items()}
        kind = st["kind"]
        d, deps = {}, {}
        if kind == "rolling":
            for si, so in st["stays"]:
                name = "SD_" + si.split("_", 1)[1]
                d[name] = S.count_slot((v[so] - v[si]).days + 1, UNIT_DAY)
                deps[name] = (si, so)
            d["WIN_START"] = S.date_slot(v["REF_DATE"] - (v["M_WIN"] - 1) * DAY)
            deps["WIN_START"] = ("REF_DATE", "M_WIN")
        elif kind == "anchor" and st["filed"]:
            for ev, name in (("EVENT_A", "ELAPSED_A"), ("EVENT_B", "ELAPSED_B")):
                d[name] = S.count_slot((v["FILED_DATE"] - v[ev]).days, UNIT_DAY)
                deps[name] = (ev, "FILED_DATE")
        elif kind == "waiting" and st["loss"]:
            d["EL_START"] = S.count_slot((v["LOSS_DATE"] - v["START_DATE"]).days, UNIT_DAY)
            deps["EL_START"] = ("START_DATE", "LOSS_DATE")
            if st["rider"]:
                d["EL_RIDER"] = S.count_slot((v["LOSS_DATE"] - v["RIDER_DATE"]).days, UNIT_DAY)
                deps["EL_RIDER"] = ("RIDER_DATE", "LOSS_DATE")
        elif kind == "purchase":
            d["WIN_START"] = S.date_slot(v["REQ_DATE"] - (v["M_WIN"] - 1) * DAY)
            deps["WIN_START"] = ("REQ_DATE", "M_WIN")
        elif kind == "addon":
            d["BASE_DATE"] = S.date_slot(v["NOTICE_DATE"] + v["N_DAYS"] * DAY)
            deps["BASE_DATE"] = ("NOTICE_DATE", "N_DAYS")
        elif kind == "cutoff":
            due, (hh, mm), tz = v["DUE_DATE"], st["cut"], _tz(st["office"])
            d["CUTOFF"] = S.datetime_slot(dt.datetime(due.year, due.month, due.day, hh, mm, tzinfo=tz))
            deps["CUTOFF"] = ("DUE_DATE",)
            d["SENT_OFFICE"] = S.datetime_slot(v["SENT"].astimezone(tz))
            deps["SENT_OFFICE"] = ("SENT",)
        return spec.replace(derived=d, derived_deps=deps)

    # ============================================================================================ solver A
    def _value(self, spec: Spec, mods: frozenset = frozenset()):
        """Solver A (mods empty) and the error models (one rule swapped): the kind's quantity on ordinals."""
        return getattr(self, f"_a_{spec.structure['kind']}")(spec.env(), spec.structure, mods)

    @staticmethod
    def _a_rolling(env, st, mods):
        ref = _o(env["REF_DATE"])
        lo, hi = ref - (env["M_WIN"] - 1), ref
        if "calendar_year" in mods:
            lo = _o(dt.date(env["REF_DATE"].year, 1, 1))
        lo += ("t01_window_one_short" in mods) - ("t01_window_one_long" in mods)
        total, segs = 0, 0
        for si, so in st["stays"]:
            a, b = _o(env[si]), _o(env[so])
            if "t01_whole_stays" in mods:
                total, segs = total + b - a + 1, segs + 1
                continue
            start = lo
            if a < lo <= b:
                if "t01_straddle_dropped" in mods:
                    continue
                if "t01_straddle_full" in mods:
                    start = a
            k = min(b, hi) - max(a, start) + 1
            if k > 0:
                total, segs = total + k, segs + 1
                if "t01_exit_extra_day" in mods and b < hi:
                    total += 1
        if "drop_inclusive_endpoint" in mods:
            total -= segs
        return {"present": total, "verdict": total > env["N_MAX"]}

    @staticmethod
    def _a_anchor(env, st, mods):
        a, b = _o(env["EVENT_A"]), _o(env["EVENT_B"])
        anchor = min(a, b) if "earlier_anchor" in mods else max(a, b)
        if "t01_business_days" in mods:
            last = _weekdays_after(anchor, env["N_DAYS"])
        else:
            last = anchor + env["N_DAYS"] + _shift(mods)
        out = {"deadline": _iso(last)}
        if st["filed"]:
            out["verdict"] = _o(env["FILED_DATE"]) <= last
        return out

    @staticmethod
    def _a_waiting(env, st, mods):
        start = _o(env["START_DATE"])
        anchor = _o(env["RIDER_DATE"]) if st["rider"] and "wrong_anchor" not in mods else start
        if "t01_business_days" in mods:
            first = _weekdays_after(anchor, env["W_DAYS"]) + 1
        else:
            first = anchor + env["W_DAYS"] + 1 + _shift(mods)
        out = {"first": _iso(first)}
        if st["loss"]:
            out["verdict"] = _o(env["LOSS_DATE"]) >= first
        return out

    @staticmethod
    def _a_purchase(env, st, mods):
        req = _o(env["REQ_DATE"])
        lo = req - (env["M_WIN"] - 1) + ("drop_inclusive_endpoint" in mods) - ("add_exclusive_endpoint" in mods)
        inside = [(pd, pa) for pd, pa in st["prior"] if "t01_ignore_window" in mods or lo <= _o(env[pd]) < req]
        if "t01_last_prior_only" in mods:
            inside = sorted(inside, key=lambda x: _o(env[x[0]]))[-1:]
        prior = sum(env[pa] for _pd, pa in inside)
        total = (0 if "t01_prior_only" in mods else env["REQ_AMT"]) + (0 if "t01_request_only" in mods else prior)
        if "t01_double_request" in mods:
            total += env["REQ_AMT"]
        return {"total": total, "verdict": _cmp(env["CMP"], total, env["THRESHOLD"])}

    @staticmethod
    def _a_cash(env, st, mods):
        day = _o(env["DAY"])
        tot = {"in": 0, "out": 0}
        for td, tt, ta in st["txns"]:
            if "t01_sum_across_days" in mods or _o(env[td]) == day:
                tot[env[tt]] += env[ta]
        if "netting" in mods:
            net = tot["in"] - tot["out"]
            tot = {"in": max(net, 0), "out": max(-net, 0)}
        sem = env["CMP"]
        for name, (frm, to) in SWAP_CMP.items():
            if name in mods and sem == frm:
                sem = to
        over_in, over_out = _cmp(sem, tot["in"], env["THRESHOLD"]), _cmp(sem, tot["out"], env["THRESHOLD"])
        label = "both" if over_in and over_out else "in" if over_in else "out" if over_out else "neither"
        return {"label": label, "verdict": label != "neither"}

    @staticmethod
    def _a_addon(env, st, mods):
        post = env["METHOD"] == "post"
        if ("t01_skip_addon" in mods and not post) or ("t01_addon_not_post" in mods and post):
            return {"due": None}                                 # the misreading does not apply to this notice
        add = env["K_DAYS"] if post != ("t01_skip_addon" in mods or "t01_addon_not_post" in mods) else 0
        if "t01_business_days" in mods:
            due = _weekdays_after(_o(env["NOTICE_DATE"]), env["N_DAYS"]) + add
        else:
            due = _o(env["NOTICE_DATE"]) + env["N_DAYS"] + add + _shift(mods)
        closed = {_o(env[x]) for x in st["closed"]}
        if "t01_ignore_closure" not in mods:
            step = -1 if "wrong_roll_direction" in mods else 1
            while due in closed:
                due += step
        return {"due": _iso(due)}

    @staticmethod
    def _a_cutoff(env, st, mods):
        office = st["office"]
        cut = st["cut"][0] * 60 + st["cut"][1]
        sent = env["SENT"]
        if "skip_offset_conversion" in mods or "t01_sender_date" in mods:   # the sender's wall clock as office time
            local = sent.toordinal() * 1440 + sent.hour * 60 + sent.minute
        elif "t01_utc_date" in mods:
            local = _utc_min(sent)
        else:
            local = _utc_min(sent) + office
        day, clock = divmod(local, 1440)
        after = clock > cut or ("drop_inclusive_endpoint" in mods and clock == cut)
        if "t01_always_next_day" in mods:
            after = True
        if "t01_sender_date" in mods:
            after = False
        receipt = day + (after and "t01_ignore_cutoff" not in mods) + ("off_by_one_late" in mods)
        if "t01_early_previous_day" in mods and not after:
            receipt -= 1
        if "t01_due_date_read" in mods:
            receipt = _o(env["DUE_DATE"])
        return {"receipt": _iso(receipt), "verdict": receipt <= _o(env["DUE_DATE"])}

    def solve_a(self, spec: Spec):
        q = spec.qform
        if KIND_OF.get(q) != spec.structure["kind"]:
            raise ContractError(f"question {q} does not belong to a {spec.structure['kind']} card")
        val = self._value(spec)
        if self.QFORMS[q].qtype == "noul":
            return _answer(q, val["verdict"])
        return val[CHOICE_VALUE[q]]

    # ============================================================================================ facts (G3)
    def canonical(self, spec: Spec) -> dict:
        a = spec.all_slots()
        st = spec.structure

        def c(name):
            return S.canonical(a[name]) if name in a else None

        out = {"kind": st["kind"], "style": st["style"], "qform": spec.qform, "person": c("PERSON"), "ref": c("REF"),
               "topic": c("TOPIC")}
        kind = st["kind"]
        if kind == "rolling":
            out.update(rule=c("WIN_CLAUSE"), n_max=c("N_MAX"), m_win=c("M_WIN"), ref_date=c("REF_DATE"),
                       win_start=c("WIN_START"),
                       stays=[[c(si), c(so), c("SD_" + si.split("_", 1)[1])] for si, so in st["stays"]])
        elif kind == "anchor":
            out.update(action=c("ACTION"), rule=c("AN_CLAUSE"), n_days=c("N_DAYS"),
                       labels=[c("EVA_LABEL"), c("EVB_LABEL")], events=[c("EVENT_A"), c("EVENT_B")],
                       filed=c("FILED_DATE"),
                       elapsed=[c("ELAPSED_A"), c("ELAPSED_B")] if st["filed"] else None)
        elif kind == "waiting":
            out.update(peril=c("PERIL"), rule=c("WAIT_CLAUSE"), w_days=c("W_DAYS"), start=c("START_DATE"),
                       rider=c("RIDER_DATE"), loss=c("LOSS_DATE"),
                       elapsed=[c("EL_START"), c("EL_RIDER")] if st["loss"] else None)
        elif kind == "purchase":
            out.update(vendor=c("VENDOR"), cmp=c("CMP"), threshold=c("THRESHOLD"), m_win=c("M_WIN"),
                       req_date=c("REQ_DATE"), req_amt=c("REQ_AMT"), win_start=c("WIN_START"),
                       prior=[[c(pd), c(pa)] for pd, pa in st["prior"]])
        elif kind == "cash":
            out.update(cmp=c("CMP"), threshold=c("THRESHOLD"), day=c("DAY"),
                       txns=[[c(td), c(tt), c(ta)] for td, tt, ta in st["txns"]])
        elif kind == "addon":
            out.update(n_days=c("N_DAYS"), k_days=c("K_DAYS"), notice=c("NOTICE_DATE"), method=c("METHOD"),
                       base=c("BASE_DATE"), closed=[c(x) for x in st["closed"]])
        else:
            out.update(due=c("DUE_DATE"), cutoff=c("CUTOFF"), sent=c("SENT"), sent_office=c("SENT_OFFICE"))
        return out

    def canonical_for(self, spec: Spec, author_mode: str) -> dict:
        c = self.canonical(spec)
        return c if author_mode == "T" else {k: v for k, v in c.items() if k != "topic"}

    def extract_view(self, spec: Spec) -> dict:
        c = self.canonical(spec)
        return {"person": c["person"], "ref": c["ref"], "topic": c["topic"]}

    def extract_fields(self, spec: Spec) -> list:
        from c2_kit.g3h import Field
        return [Field("person", "name", "the person who wrote or is named as the sender, as written"),
                Field("ref", "id", "the file, case or notice reference, as written"),
                Field("topic", "str", T01.TOPIC_DESCRIBE)]

    # ============================================================================================ render
    def _row_key(self, spec: Spec) -> str:
        return f"{spec.family}|{spec.seed}|{spec.sampler}|{spec.qform}"

    def rule_template(self, spec: Spec) -> str:
        return RULES[spec.structure["kind"]]

    def block_template(self, spec: Spec) -> str:
        """The program-written record block as a slot template (G0 1.2)."""
        st = spec.structure
        kind, table = st["kind"], st["style"] == "table"
        if kind == "rolling":
            if table:
                lines = ["Travel log {REF}, traveller {PERSON}:", "| Entry day | Exit day | Whole stay |",
                         "| --- | --- | --- |"]
                lines += [f"| {{{si}}} | {{{so}}} | {{SD_{si.split('_', 1)[1]}}} |" for si, so in st["stays"]]
            else:
                lines = ["Stay record {REF} for {PERSON}:"]
                lines += [f"- entry day {{{si}}}, exit day {{{so}}} (whole stay: {{SD_{si.split('_', 1)[1]}}})"
                          for si, so in st["stays"]]
            lines += ["Reference date: {REF_DATE}", "Window checked: {WIN_START} to {REF_DATE}, both included."]
        elif kind == "anchor":
            if table:
                lines = ["Court notice, case {REF}, party {PERSON}:", "| Date | Event |", "| --- | --- |",
                         "| {EVENT_A} | {EVA_LABEL} |", "| {EVENT_B} | {EVB_LABEL} |"]
                if st["filed"]:
                    lines += ["| {FILED_DATE} | {ACTION} filed |",
                              "Days from the {EVA_LABEL} to the filing: {ELAPSED_A}. Days from the {EVB_LABEL} to the "
                              "filing: {ELAPSED_B}."]
            else:
                lines = ["Case {REF}, party {PERSON}:", "- {EVA_LABEL}: {EVENT_A}", "- {EVB_LABEL}: {EVENT_B}"]
                if st["filed"]:
                    lines += ["- {ACTION} filed on: {FILED_DATE}",
                              "- days from the {EVA_LABEL} to the filing: {ELAPSED_A}",
                              "- days from the {EVB_LABEL} to the filing: {ELAPSED_B}"]
        elif kind == "waiting":
            lines = ["Policy {REF}, holder {PERSON}:", "- policy start date: {START_DATE}",
                     "- {PERIL} cover: added by a rider effective {RIDER_DATE}" if st["rider"]
                     else "- {PERIL} cover: part of the base policy"]
            if st["loss"]:
                lines += ["- {PERIL} loss on: {LOSS_DATE}", "- days from the policy start date to the loss: {EL_START}"]
                if st["rider"]:
                    lines.append("- days from the rider effective date to the loss: {EL_RIDER}")
        elif kind == "purchase":
            lines = ["Purchase log {REF}, kept by {PERSON}, vendor {VENDOR}:"]
            lines += [f"- earlier purchase on {{{pd}}}: {{{pa}}}" for pd, pa in st["prior"]]
            lines += ["- new request on {REQ_DATE}: {REQ_AMT}",
                      "Window checked: {WIN_START} to {REQ_DATE}, both included."]
        elif kind == "cash":
            lines = ["Cash ledger {REF}, teller {PERSON}:"]
            lines += [f"- {{{td}}}: {{{tt}}} of {{{ta}}}" for td, tt, ta in st["txns"]]
            lines.append("Day under review: {DAY}")
        elif kind == "addon":
            lines = ["Notice {REF} to {PERSON}:", "- notice date: {NOTICE_DATE}", "- sent by: {METHOD}",
                     "- {N_DAYS} after the notice date, before any postal add-on or closure: {BASE_DATE}",
                     "Office closures: " + ("; ".join(f"{{{x}}}" for x in st["closed"]) if st["closed"] else "none")
                     + "."]
        else:
            lines = ["Notice {REF} to {PERSON}:", "- response due date: {DUE_DATE}",
                     "- office cutoff on the due date: {CUTOFF}",
                     "- response sent: {SENT} [same instant in office time: {SENT_OFFICE}]"]
        return "\n".join(lines)

    def _option_renderer(self, spec: Spec, forms: dict):
        q = spec.qform
        if q == "ch_days":
            return lambda n: S.render(S.count_slot(n, UNIT_DAY), "digits")
        if q == "ch_total":
            fmt = forms.get("REQ_AMT", "symbol")
            return lambda c: S.render(S.cents_slot(c), fmt if fmt in S.forms(S.cents_slot(c)) else "symbol")
        if q == "ch_cash_which":
            return CASH_TEXT.__getitem__
        if q == "ch_receipt_day":
            due = forms["DUE_DATE"]                    # a weekday form also prints its plain date form
            shown = {due, {"wdmy": "dmy", "wmdy": "mdy"}.get(due, due)} | {
                "dmy" if forms[n] == "text" else "iso" for n in ("SENT", "CUTOFF", "SENT_OFFICE")}
            pool = [f for f in RECEIPT_OPTION_FORMS if f not in shown]
            fmt = pool[int(uhash(self._row_key(spec), "receipt_form") * len(pool))]
            return lambda iso: S.render(S.date_slot(dt.date.fromisoformat(iso)), fmt)
        date_slot = {"ch_deadline": "EVENT_A", "ch_first_day": "START_DATE", "ch_due": "NOTICE_DATE"}[q]
        fmt = forms[date_slot]
        return lambda iso: S.render(S.date_slot(dt.date.fromisoformat(iso)), fmt)

    # -------------------------------------------------------------------------------------------- option cues (G0 v4 12.2)
    @staticmethod
    def _printed_values(spec: Spec) -> set:
        """The values the card and the record print, as canonical keys: ISO dates (a datetime prints its date), counts and
        amounts. An option that equals one of them is "printed" whatever form it is shown in."""
        out = set()
        for sl in spec.all_slots().values():
            if sl.kind == "date":
                out.add(sl.value.isoformat())
            elif sl.kind == "datetime":
                out.add(sl.value.date().isoformat())
            elif sl.kind in ("count", "cents"):
                out.add((sl.kind, int(sl.value)))
        return out

    @staticmethod
    def _cue_sig(qform: str, a, rk, vis: str, printed: set) -> tuple:
        """The visible cues of an option: shown verbatim in the card or record (surface), equal to a printed value
        (canonical) and, for counts and amounts, the length of its text (its digit count)."""
        text = rk(a)
        surface = len(text) > 3 and text.lower() in vis
        if isinstance(a, str):
            canon = a in printed
        else:
            canon = (("count" if qform == "ch_days" else "cents"), a) in printed
        return surface, canon, (len(text) if qform in LENGTH_MATCH_FORMS else 0)

    def _cue_models(self, spec: Spec, gold, rk, vis: str) -> dict:
        """The error models restricted to outputs that share the gold's cues (and, for a count, are possible golds:
        at least one day present). Then every option is printed or none is, and a count or an amount has one length, so
        no content-free rule on them can find the gold (pilot G6 options-only; G7 verbatim / longest / shortest)."""
        printed = self._printed_values(spec)
        want = self._cue_sig(spec.qform, gold, rk, vis, printed)
        out = {}
        for name, m in self.error_models().items():
            def fn(s, base=m.fn):
                a = base(s)
                if a is None or (spec.qform == "ch_days" and a < 1):
                    return None
                return a if self._cue_sig(spec.qform, a, rk, vis, printed) == want else None
            out[name] = error_model(name, fn)
        return out

    def render(self, spec: Spec, ctx, *, skin=None, wording=None, forms=None, attack=None):
        key = self._row_key(spec)
        ctx = self.ctx_for(spec, ctx)                  # never pick a wording that breaks the polarity rule
        held = spec.sampler in self.HELD_OUT_SAMPLERS
        skin = skin or ctx.pick(FAMILY, "skin", key, held_out=held)
        wording = wording or ctx.pick(FAMILY, "wording", key, qform=spec.qform, held_out=held)   # A54 (2): S5 uses held-out wordings
        if wording.qform != spec.qform:
            raise ContractError(f"wording {wording.skin_id} asks {wording.qform}, spec asks {spec.qform}")
        forms = forms or choose_forms(spec, key)
        slots = spec.all_slots()
        tb = TextBuilder()
        tb.add("state", skin.fill(slots, forms), skin_id=skin.skin_id)
        tb.add("state", "\n\n").add("state", K.fill(self.block_template(spec), slots, forms))
        if attack is not None:
            tb.add("state", "\n\n").add("state", attack.fill(slots, forms), skin_id=attack.skin_id)
        tb.add("instructions", K.fill(self.rule_template(spec), slots, forms, field="instructions"))
        tb.add("instructions", "\n\n")
        tb.add("instructions", wording.fill(slots, forms, field="instructions"), skin_id=wording.skin_id)
        ans = self.solve_a(spec)
        os_ = None
        if self.QFORMS[spec.qform].qtype == "choice":
            rk = self._option_renderer(spec, forms)
            if spec.qform == "ch_cash_which":
                os_ = build_closed(spec, ans, list(CASH_LABELS), self.error_models(), row_key=key, render_key=rk)
            else:
                ex = EXCLUSIVE_EM.get(spec.qform, ())
                models = self.error_models()
                vis = ((tb.text("state") or "") + "\n" + (tb.text("instructions") or "")).lower()
                if self.CUE_MATCH and spec.qform in CUE_MATCH_FORMS:   # G0 v4 12.2: the options share the gold's cues
                    models = self._cue_models(spec, ans, rk, vis)
                k = ordered_k(spec, ans, models, k=K_DRAW[int(uhash(key, "k") * len(K_DRAW))],
                              order_key=_order_key, exclusive=ex)
                os_ = None if k is None else build_options(spec, ans, models, k=k, row_key=key,
                                                          render_key=rk, order_key=_order_key, exclusive=ex)
                if os_ is None:                    # dropped, never re-tried with another k (kit distractors.py)
                    raise K.RenderError("the error models leave a side of the gold empty")
                if spec.qform == "ch_receipt_day" and any(len(o.text) > 3 and o.text.lower() in vis
                                                         for o in os_.options):
                    raise K.RenderError("an option copies a printed date")      # G0 v4 12.2 (about 1.6% of rows)
        return assemble_row(self, spec, tb, answer=ans, option_set=os_, skin=skin, wording=wording, forms=forms,
                            attack=attack)

    # ============================================================================================ ledger (construction)
    def _tags(self, spec: Spec) -> tuple:
        """Trap tags from the construction ledger (G0 section 3)."""
        v, st = spec.env(), spec.structure
        kind, tags = st["kind"], set()
        if kind == "rolling":
            ws, rows = self._ledger_rolling(spec)
            if any(r["straddle"] for r in rows):
                tags.add("straddle")
            if any(r["b"] < ws for r in rows):
                tags.add("pre_window_stay")
            if any(r["a"] == ws or r["b"] == ws - DAY for r in rows):
                tags.add("window_edge")
            present = sum(r["inside"] for r in rows)
            cal = sum(max(0, (min(r["b"], v["REF_DATE"]) - max(r["a"], dt.date(v["REF_DATE"].year, 1, 1))).days + 1)
                      for r in rows)
            if (cal > v["N_MAX"]) != (present > v["N_MAX"]):
                tags.add("calendar_trap")
        elif kind == "anchor" and st["filed"]:
            later, earlier = max(v["EVENT_A"], v["EVENT_B"]), min(v["EVENT_A"], v["EVENT_B"])
            if (v["FILED_DATE"] - later).days <= v["N_DAYS"] < (v["FILED_DATE"] - earlier).days:
                tags.add("earlier_trap")
        elif kind == "waiting" and st["loss"] and st["rider"]:
            if (v["LOSS_DATE"] - v["RIDER_DATE"]).days <= v["W_DAYS"] < (v["LOSS_DATE"] - v["START_DATE"]).days:
                tags.add("rider_trap")
        elif kind == "purchase":
            ws, rows = self._ledger_purchase(spec)
            if any(r["d"] in (ws, ws - DAY) for r in rows):
                tags.add("window_edge")
            inside = sum(r["amt"] for r in rows if r["inside"])
            verdict = _cmp(v["CMP"], v["REQ_AMT"] + inside, v["THRESHOLD"])
            if _cmp(v["CMP"], v["REQ_AMT"], v["THRESHOLD"]) != verdict:
                tags.add("request_alone_trap")
            if _cmp(v["CMP"], v["REQ_AMT"] + sum(r["amt"] for r in rows), v["THRESHOLD"]) != verdict:
                tags.add("ignore_window_trap")
        elif kind == "cash":
            day_tot, all_tot = self._ledger_cash(spec)
            label = self._cash_label(v, day_tot)
            net = day_tot["in"] - day_tot["out"]
            if self._cash_label(v, {"in": max(net, 0), "out": max(-net, 0)}) != label:
                tags.add("netting_trap")
            if self._cash_label(v, all_tot) != label:
                tags.add("other_day_trap")
        elif kind == "addon":
            reached, due, walked = self._ledger_addon(spec)
            if walked:
                tags.add("closure_roll")
            if walked >= 2:
                tags.add("double_roll")
            if v["METHOD"] == "post":
                tags.add("post_addon")
        elif kind == "cutoff":
            sent, cutoff = v["SENT"], self._cutoff_instant(spec)
            office_local = sent.astimezone(cutoff.tzinfo)
            daily = office_local.replace(hour=cutoff.hour, minute=cutoff.minute)
            if abs((office_local - daily).total_seconds()) <= 300:
                tags.add("boundary")                            # within 5 minutes of a daily cutoff
            wall = sent.replace(tzinfo=cutoff.tzinfo)
            if (wall <= cutoff) != (sent <= cutoff):
                tags.add("conversion_trap")
            if office_local.date() == cutoff.date() - DAY and office_local.time() > cutoff.time():
                tags.add("evening_before")
            if office_local.date() != sent.date():
                tags.add("date_crosses")
        return tuple(sorted(tags))

    @staticmethod
    def _ledger_rolling(spec: Spec):
        v, st = spec.env(), spec.structure
        ws = v["REF_DATE"] - (v["M_WIN"] - 1) * DAY
        rows = []
        for si, so in st["stays"]:
            a, b = v[si], v[so]
            inside = (b - max(a, ws)).days + 1 if b >= ws else 0
            rows.append({"in": si, "out": so, "a": a, "b": b, "inside": inside, "straddle": a < ws <= b})
        return ws, rows

    @staticmethod
    def _ledger_purchase(spec: Spec):
        v, st = spec.env(), spec.structure
        ws = v["REQ_DATE"] - (v["M_WIN"] - 1) * DAY
        rows = [{"slot": pd, "amt_slot": pa, "d": v[pd], "amt": v[pa], "inside": ws <= v[pd] < v["REQ_DATE"]}
                for pd, pa in st["prior"]]
        return ws, rows

    @staticmethod
    def _ledger_cash(spec: Spec):
        v, st = spec.env(), spec.structure
        day_tot, all_tot = {"in": 0, "out": 0}, {"in": 0, "out": 0}
        for td, tt, ta in st["txns"]:
            all_tot[v[tt]] += v[ta]
            if v[td] == v["DAY"]:
                day_tot[v[tt]] += v[ta]
        return day_tot, all_tot

    @staticmethod
    def _cash_label(v: dict, tot: dict) -> str:
        oi, oo = _cmp(v["CMP"], tot["in"], v["THRESHOLD"]), _cmp(v["CMP"], tot["out"], v["THRESHOLD"])
        return "both" if oi and oo else "in" if oi else "out" if oo else "neither"

    @staticmethod
    def _ledger_addon(spec: Spec, method: str | None = None):
        v, st = spec.env(), spec.structure
        method = method or v["METHOD"]
        reached = v["NOTICE_DATE"] + v["N_DAYS"] * DAY + (v["K_DAYS"] * DAY if method == "post" else dt.timedelta(0))
        closed = {v[x] for x in st["closed"]}
        due, walked = reached, 0
        while due in closed:
            due, walked = due + DAY, walked + 1
        return reached, due, walked

    @staticmethod
    def _cutoff_instant(spec: Spec) -> dt.datetime:
        v, st = spec.env(), spec.structure
        due, (hh, mm) = v["DUE_DATE"], st["cut"]
        return dt.datetime(due.year, due.month, due.day, hh, mm, tzinfo=_tz(st["office"]))

    # ============================================================================================ relations
    def relations(self, spec: Spec) -> list:
        out = []
        key = self._row_key(spec)
        comp = COMPLEMENTS.get(spec.qform)
        if comp and uhash(FAMILY, "comp", key) < P_COMPLEMENT[self.QFORMS[spec.qform].yes_is_bad]:
            out.append(RelationProposal("complement", qform=_draw(uhash(FAMILY, "ckind", key), comp)))
        if uhash(FAMILY, "equiv", key) < P_EQUIV:
            out.append(RelationProposal("equiv"))
        if uhash(FAMILY, "twin", key) < P_TWIN:
            t = self._twin(spec)
            if t is not None:
                out.append(t)
        return out + self._metamorphic(spec)

    def _twin(self, spec: Spec):
        """One input slot moves; the prediction comes from the construction ledger and the move, never solve_a."""
        return getattr(self, f"_twin_{spec.structure['kind']}")(spec)

    def _twin_rolling(self, spec: Spec):
        v = spec.env()
        ws, rows = self._ledger_rolling(spec)
        present = sum(r["inside"] for r in rows)
        n = v["N_MAX"]
        last = rows[-1]
        if spec.qform == "ch_days":
            delta = (1 + int(uhash(FAMILY, "tdelta", spec.seed) * 3)) * (1 if uhash(FAMILY, "tsign", spec.seed) < .5
                                                                          else -1)
            target = present + delta
            expect = target
        else:
            target = n if present > n else n + 1
            delta = target - present
            expect = _answer(spec.qform, target > n)
        new_out = last["b"] + delta * DAY
        if not (max(last["a"], ws) <= new_out <= v["REF_DATE"]) or last["b"] < ws:
            return None
        return RelationProposal("twin", spec=spec.with_slot(last["out"], S.date_slot(new_out)),
                                changed_slot=last["out"], expect=expect, note=f"stay_exit.{delta:+d}")

    def _twin_anchor(self, spec: Spec):
        v = spec.env()
        n = v["N_DAYS"]
        later = max(v["EVENT_A"], v["EVENT_B"])
        if spec.qform == "ch_deadline":
            d = (1 + int(uhash(FAMILY, "tdelta", spec.seed) * 5)) * (1 if uhash(FAMILY, "tsign", spec.seed) < .5
                                                                      else -1)
            if n + d < 1:
                d = -d
            return RelationProposal("twin", spec=spec.with_slot("N_DAYS", S.count_slot(n + d, UNIT_DAY)),
                                    changed_slot="N_DAYS", expect=(later + (n + d) * DAY).isoformat(),
                                    note="n_days")
        e = (v["FILED_DATE"] - later).days
        timely = e <= n
        if uhash(FAMILY, "tslot", spec.seed) < 0.4:
            n2 = e - 1 if timely else e
            if n2 >= 1:
                return RelationProposal("twin", spec=spec.with_slot("N_DAYS", S.count_slot(n2, UNIT_DAY)),
                                        changed_slot="N_DAYS", expect=_answer(spec.qform, e <= n2), note="n_days")
        e2 = n + 1 if timely else n
        return RelationProposal("twin", spec=spec.with_slot("FILED_DATE", S.date_slot(later + e2 * DAY)),
                                changed_slot="FILED_DATE", expect=_answer(spec.qform, e2 <= n), note="filed")

    def _twin_waiting(self, spec: Spec):
        v, st = spec.env(), spec.structure
        w = v["W_DAYS"]
        anchor = v["RIDER_DATE"] if st["rider"] else v["START_DATE"]
        if spec.qform == "ch_first_day":
            d = (1 + int(uhash(FAMILY, "tdelta", spec.seed) * 5)) * (1 if uhash(FAMILY, "tsign", spec.seed) < .5
                                                                      else -1)
            return RelationProposal("twin", spec=spec.with_slot("W_DAYS", S.count_slot(w + d, UNIT_DAY)),
                                    changed_slot="W_DAYS", expect=(anchor + (w + d + 1) * DAY).isoformat(),
                                    note="w_days")
        e = (v["LOSS_DATE"] - anchor).days
        covered = e > w
        if uhash(FAMILY, "tslot", spec.seed) < 0.4:
            w2 = e if covered else e - 1
            if w2 >= 1:
                return RelationProposal("twin", spec=spec.with_slot("W_DAYS", S.count_slot(w2, UNIT_DAY)),
                                        changed_slot="W_DAYS", expect=_answer(spec.qform, e > w2), note="w_days")
        e2 = w if covered else w + 1
        return RelationProposal("twin", spec=spec.with_slot("LOSS_DATE", S.date_slot(anchor + e2 * DAY)),
                                changed_slot="LOSS_DATE", expect=_answer(spec.qform, e2 > w), note="loss")

    def _twin_purchase(self, spec: Spec):
        v = spec.env()
        ws, rows = self._ledger_purchase(spec)
        thr, sem = v["THRESHOLD"], v["CMP"]
        total = v["REQ_AMT"] + sum(r["amt"] for r in rows if r["inside"])
        verdict = _cmp(sem, total, thr)
        if spec.qform != "ch_total" and uhash(FAMILY, "tslot", spec.seed) < 0.4:
            order = sorted(range(len(rows)), key=lambda i: uhash(FAMILY, "trow", spec.seed, rows[i]["slot"]))
            for i in order:                                     # move one earlier purchase across the window edge
                r = rows[i]
                new = ws - DAY if r["inside"] else ws
                t2 = total - r["amt"] if r["inside"] else total + r["amt"]
                if (_cmp(sem, t2, thr) != verdict and (i == 0 or rows[i - 1]["d"] <= new)
                        and (i == len(rows) - 1 or new <= rows[i + 1]["d"])):
                    return RelationProposal("twin", spec=spec.with_slot(r["slot"], S.date_slot(new)),
                                            changed_slot=r["slot"], expect=_answer(spec.qform, _cmp(sem, t2, thr)),
                                            note="window_edge")
        if spec.qform == "ch_total":
            step = (1 + int(uhash(FAMILY, "tdelta", spec.seed) * 20)) * 50 * CENT
            t2 = total + step if uhash(FAMILY, "tsign", spec.seed) < .5 or v["REQ_AMT"] <= step else total - step
            expect = t2
        else:
            if sem == "cmp.gt":
                t2 = thr if verdict else thr + CENT
            else:
                t2 = thr - CENT if verdict else thr
            expect = _answer(spec.qform, _cmp(sem, t2, thr))
        new_req = v["REQ_AMT"] + (t2 - total)
        if new_req < CENT:
            return None
        return RelationProposal("twin", spec=spec.with_slot("REQ_AMT", S.cents_slot(new_req)), changed_slot="REQ_AMT",
                                expect=expect, note="request_amount")

    def _twin_cash(self, spec: Spec):
        v, st = spec.env(), spec.structure
        thr, sem = v["THRESHOLD"], v["CMP"]
        day_tot, _ = self._ledger_cash(spec)
        label = self._cash_label(v, day_tot)
        over = {d: _cmp(sem, day_tot[d], thr) for d in ("in", "out")}
        edge_over = thr + CENT if sem == "cmp.gt" else thr
        edge_under = thr if sem == "cmp.gt" else thr - CENT
        order = sorted(("in", "out"), key=lambda d: uhash(FAMILY, "tdir", spec.seed, d))
        for d in order:
            on_day = [(td, tt, ta) for td, tt, ta in st["txns"] if v[td] == v["DAY"] and v[tt] == d]
            if not on_day:
                continue
            td, tt, ta = max(on_day, key=lambda x: (v[x[2]], x[2]))
            target = edge_under if over[d] else edge_over
            new_amt = v[ta] + (target - day_tot[d])
            if new_amt < CENT:
                continue
            tot2 = dict(day_tot, **{d: target})
            label2 = self._cash_label(v, tot2)
            if label2 == label:
                continue
            expect = label2 if spec.qform == "ch_cash_which" else _answer(spec.qform, label2 != "neither")
            if spec.qform != "ch_cash_which" and (label2 != "neither") == (label != "neither"):
                continue
            return RelationProposal("twin", spec=spec.with_slot(ta, S.cents_slot(new_amt)), changed_slot=ta,
                                    expect=expect, note=f"cash_{d}")
        return None

    def _twin_addon(self, spec: Spec):
        v = spec.env()
        _, due, _ = self._ledger_addon(spec)
        others = [m for m in sorted(METHODS) if m != v["METHOD"]]
        others.sort(key=lambda m: (m != "post") if v["METHOD"] != "post" else uhash(FAMILY, "tm", spec.seed, m))
        for m in others:
            _, due2, _ = self._ledger_addon(spec, m)
            if due2 != due:
                return RelationProposal("twin", spec=spec.with_slot("METHOD", S.category_slot(m, METHODS)),
                                        changed_slot="METHOD", expect=due2.isoformat(), note="method")
        return None

    def _twin_cutoff(self, spec: Spec):
        v = spec.env()
        sent, cutoff = v["SENT"], self._cutoff_instant(spec)
        tz_s = sent.tzinfo
        step = 1 + int(uhash(FAMILY, "tdelta", spec.seed) * 5)
        if spec.qform == "ch_receipt_day":
            local = sent.astimezone(cutoff.tzinfo)
            cut_today = local.replace(hour=cutoff.hour, minute=cutoff.minute)
            after = local > cut_today
            new = cut_today - dt.timedelta(minutes=step - 1) if after else cut_today + dt.timedelta(minutes=step)
            receipt = new.date() + (DAY if new > cut_today else dt.timedelta(0))
            return RelationProposal("twin", spec=spec.with_slot("SENT", S.datetime_slot(new.astimezone(tz_s))),
                                    changed_slot="SENT", expect=receipt.isoformat(), note="sent")
        on_time = sent <= cutoff
        new = cutoff + dt.timedelta(minutes=step) if on_time else cutoff - dt.timedelta(minutes=step - 1)
        return RelationProposal("twin", spec=spec.with_slot("SENT", S.datetime_slot(new.astimezone(tz_s))),
                                changed_slot="SENT", expect=_answer(spec.qform, new <= cutoff), note="sent")

    # -------------------------------------------------------------------------------------------- G4 (metamorphic)
    def _metamorphic(self, spec: Spec) -> list:
        """G4 (checked, never emitted): renames, a common shift of every date and time, and kind-specific inert
        additions leave the answer as predicted."""
        v, st = spec.env(), spec.structure
        kind = st["kind"]
        out = [RelationProposal("metamorphic", spec=spec.with_slot("PERSON", S.name_slot(
            next(p for p in RESERVE_PEOPLE if p != v["PERSON"]))), expect="same", note="rename the person")]
        week = 7 * DAY
        moved = {k: (S.date_slot(s.value + week) if s.kind == "date" else S.datetime_slot(s.value + week))
                 for k, s in spec.slots.items() if s.kind in ("date", "datetime")}
        expect = "same"
        if self.QFORMS[spec.qform].qtype == "choice" and isinstance(self.solve_a(spec), str) \
                and spec.qform != "ch_cash_which":
            expect = (dt.date.fromisoformat(self.solve_a(spec)) + week).isoformat()
        out.append(RelationProposal("metamorphic", spec=spec.replace(slots={**spec.slots, **moved}), expect=expect,
                                    note="shift every date and time by seven days"))
        if kind == "rolling":
            ws, rows = self._ledger_rolling(spec)
            end = min(rows[0]["a"], ws) - 3 * DAY
            add = {"SI_X": S.date_slot(end - 4 * DAY), "SO_X": S.date_slot(end)}
            out.append(RelationProposal("metamorphic", spec=spec.replace(
                slots={**spec.slots, **add}, structure={**st, "stays": [["SI_X", "SO_X"]] + st["stays"]}),
                expect="same", note="add a stay that ends before the window"))
        elif kind == "anchor":
            sw = {"EVA_LABEL": spec.slots["EVB_LABEL"], "EVB_LABEL": spec.slots["EVA_LABEL"],
                  "EVENT_A": spec.slots["EVENT_B"], "EVENT_B": spec.slots["EVENT_A"]}
            out.append(RelationProposal("metamorphic", spec=spec.replace(slots={**spec.slots, **sw}), expect="same",
                                        note="swap the two events"))
        elif kind == "waiting":
            out.append(RelationProposal("metamorphic", spec=spec.with_slot("PERIL", S.name_slot(RESERVE_PERIL)),
                                        expect="same", note="rename the peril"))
        elif kind == "purchase":
            ws, rows = self._ledger_purchase(spec)
            first = min([r["d"] for r in rows] + [ws])
            add = {"PD_X": S.date_slot(first - 9 * DAY), "PA_X": S.cents_slot(v["THRESHOLD"])}
            out.append(RelationProposal("metamorphic", spec=spec.replace(
                slots={**spec.slots, **add}, structure={**st, "prior": [["PD_X", "PA_X"]] + st["prior"]}),
                expect="same", note="add a purchase before the window"))
        elif kind == "cash":
            add = {"TD_X": S.date_slot(v["DAY"] + 5 * DAY), "TT_X": S.category_slot("in", DIRS),
                   "TA_X": S.cents_slot(2 * v["THRESHOLD"])}
            out.append(RelationProposal("metamorphic", spec=spec.replace(
                slots={**spec.slots, **add}, structure={**st, "txns": st["txns"] + [["TD_X", "TT_X", "TA_X"]]}),
                expect="same", note="add a large deposit on another day"))
        elif kind == "addon":
            _, due, _ = self._ledger_addon(spec)
            far = max([due] + [v[x] for x in st["closed"]]) + 4 * DAY
            out.append(RelationProposal("metamorphic", spec=spec.replace(
                slots={**spec.slots, "CL_X": S.date_slot(far)}, structure={**st, "closed": st["closed"] + ["CL_X"]}),
                expect="same", note="list a closure after the due date"))
        else:
            other = next(o for o in SENDER_OFFSETS if o not in (_off(v["SENT"]), st["office"]))
            out.append(RelationProposal("metamorphic", spec=spec.with_slot(
                "SENT", S.datetime_slot(v["SENT"].astimezone(_tz(other)))), expect="same",
                note="write the sending time in another offset"))
        return out

    # ============================================================================================ error models
    def error_models(self) -> dict:
        if self._ems is None:
            ems = {}
            for name in ALL_EM:
                def fn(spec, name=name):
                    if name not in CHOICE_EM.get(spec.qform, ()):
                        return None
                    return self._value(spec, frozenset({name}))[CHOICE_VALUE[spec.qform]]
                ems[name] = error_model(name, fn)
            self._ems = ems
        return self._ems

