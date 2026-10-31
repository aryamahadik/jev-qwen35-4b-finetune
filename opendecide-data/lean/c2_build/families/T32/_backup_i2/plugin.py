"""families/T32/plugin.py: T32 "commitment ledger in chat" (C2_DATA_SPEC 2.1 T32, 3.9; G0_SPEC.md frozen, sha below).

A chat log of 2-4 members. One commitment (the asked one) and 1-5 decoy commitments are made, extended, triggered,
released, taken back or reported done in casual one-line messages; the question asks the status of the asked
commitment at the end of a status date: kept, broken, not yet due, not triggered or waived (or its due date in force).
Every message body is one admitted lexicon form (sem chat.*), so the event stream is read back exactly (G0 R1, R4).

  solver A   event sourcing: the message stream folded through a state machine (none -> waiting / active ->
             retracted -> terminal; the due date passing is a transition), G0 R9                 paradigm event_sourcing
  solver B   solver_b.py: its own parser of the rendered row, the messages loaded into sqlite, each fact one
             aggregate query, the status one SQL CASE; it refuses rows that break the G0 R10 invariants
                                                                                                 paradigm sql_sqlite
  plan       a third, construction-only table (_plan / _plan_status: one closed formula over the asked commitment's
             story lines): it checks the label-first samplers and predicts minimal-edit twins, never the gold
  samplers   S1 forward; S2 near-miss (boundary dates, allowed vs not-allowed movers); S3 export (log style, more
             decoys); S4 transcript-heavy (try / remind / ack lines, after-ASOF lines); S5 held out (2027, both styles)
  questions  ch_status (closed 5), ch_due (open dates), yn_broken (+ complements other_than / not), yn_dneg_broken,
             yn_kept (+ not), yn_kept_vs (+ option-framed unkept_vs)
  relations  complement, minimal-edit twin (ASOF, done date, release / yes sender, AUTH, event line), equiv (other
             container + skin), inv (attack note), G4 metamorphic (rename, shift dates, swap the asked task)
Pools. The 30 frozen Haiku packs (pools_v2/packs.jsonl, read through packs_v2.py) give the task phrases, events and
chat topics (pilot fix F7); the 6 Claude-written stand-in packs of vocab.py serve the unit tests (T32(vocab=
packs_v2.standin())). Nothing here writes a file.

Pilot fixes of 14 Oct 2026 (families/T32/pilot/PILOT_VERDICT.json F1-F8; iteration 1 of at most 2; G0 v3):
  F1  wordings: ctx_for() leaves out the wordings that break the polarity rule (c2_kit.polarity; this removes the six
      yn_other_than_broken wordings without a negation cue that failed G-TW) and the yn_dneg_broken wordings that are not
      a truth-evaluation statement (F8); yn_dneg_broken falls back to yn_broken while no clean wording is admitted
  F2  twins: P(twin | yes/no base) = 1.0 for a no, 0.45 for a yes (both about 44% of bases get one), choice 0.40
  F3  ch_status gold shares 20% each
  F4  ch_due: the status date is redrawn (label-blind, from the seed) so it equals none of the three option dates and
      the gold is the nearest, middle or farthest option 1/3 each (_spread_asof)
  F5  deep: DEEP_DAMP 0.25, a deep spec gets no equiv / attack partner
  F6  length: three card styles (full / compact / short), rules in row.card on yes/no rows (printed once), fewer
      lines (MAX_LINES 7 / 8), fewer decoys in S3, message forms at or under the per-sem median length
"""
from __future__ import annotations

import datetime as dt
import functools
import random
import re
import sys
from dataclasses import dataclass
from pathlib import Path
from types import SimpleNamespace

_C2_BUILD = Path(__file__).resolve().parents[2]
if str(_C2_BUILD) not in sys.path:
    sys.path.insert(0, str(_C2_BUILD))

from c2_kit import cards as CD  # noqa: E402
from c2_kit import gsl  # noqa: E402
from c2_kit import polarity as POL  # noqa: E402
from c2_kit import skin as K  # noqa: E402
from c2_kit import slots as S  # noqa: E402
from c2_kit.distractors import build_closed, build_options, error_model, register_name, uhash  # noqa: E402
from c2_kit.plugin import (C2Plugin, ContractError, KitCtx, QuestionForm, RelationProposal, Spec,  # noqa: E402
                           choose_forms)
from c2_kit.rows import TextBuilder, assemble_row  # noqa: E402
from families.T32 import packs_v2 as PV  # noqa: E402

HERE = Path(__file__).resolve().parent
FAMILY = "T32"
DAY = dt.timedelta(days=1)
MAX_TRIES = 1500                              # a rare (status, depth) story (Not yet due at depth 3) needs ~70 draws on average

# ------------------------------------------------------------------------------------------------ G0 semantics
STATUSES = ("kept", "broken", "not_yet_due", "not_triggered", "waived")
STATUS_TEXT = {"kept": "Kept", "broken": "Broken", "not_yet_due": "Not yet due", "not_triggered": "Not triggered",
               "waived": "Waived"}
TERMINAL = frozenset(("kept", "broken", "waived", "not_triggered"))
COMMIT_SEMS = ("chat.commit", "chat.commit_if")
SIG = {   # G0 R4: the slot signature of every message sem (form slot names)
    "chat.commit": ("DUE", "TASK"), "chat.commit_if": ("COND", "DUE", "TASK"), "chat.try": ("DUE", "TASK"),
    "chat.done": ("TASK",), "chat.ext_ask": ("NEW_DUE", "TASK"), "chat.ext_yes": ("NEW_DUE", "TASK"),
    "chat.ext_no": ("TASK",), "chat.cond_met": ("COND",), "chat.cond_off": ("COND",), "chat.release": ("TASK",),
    "chat.retract": ("TASK",), "chat.remind": ("TASK",), "chat.ack": (),
}
YN = {"yn_broken": lambda s: int(s == "broken"), "yn_dneg_broken": lambda s: int(s == "broken"),
      "yn_not_broken": lambda s: int(s != "broken"), "yn_other_than_broken": lambda s: int(s != "broken"),
      "yn_kept": lambda s: int(s == "kept"), "yn_kept_vs": lambda s: int(s == "kept"),
      "yn_not_kept": lambda s: int(s != "kept"), "yn_unkept_vs": lambda s: int(s != "kept")}

# ------------------------------------------------------------------------------------------------ card text (G0 1.1)
CLOSED_WORLD = "The chat is complete: no other message, agreement or event exists."
# Three phrasings of the same rules (G0 1.1; c2_kit.cards: CardSpec.problems() checks that every variant keeps its
# item's slots, operator words and negation count). full = the v2 wording; compact and short are shorter (pilot fix F6).
CARD_SPEC = CD.CardSpec(
    family=FAMILY,
    heads={"full": "Count only chat lines sent on or before the question's date, in the order listed.",
           "compact": "Count only lines sent on or before the question's date, in listed order.",
           "short": "Count only lines on or before the question's date, in listed order."},
    items=(
        CD.CardItem("commit",
                    "A commitment: the sender says they will do a task by a date (that day included), made to "
                    "<<ADDRESS>>; saying they will try is not one.",
                    "Commitment: the sender says they will do a task by a date (day included) to <<ADDRESS>>; "
                    "trying is not one.",
                    "Commitment: the sender says they will do a task by a date (day included) to <<ADDRESS>>; "
                    "trying is not one."),
        CD.CardItem("due", "Its due date: that date, replaced by a new date once someone allowed says yes to it.",
                    "Due date: that date, replaced by a new date once someone allowed says yes.",
                    "Due date: that date, replaced by a new date once someone allowed says yes."),
        CD.CardItem("order", "Status: the first of these that fits.", "Status: the first that fits.",
                    "Status: the first that fits."),
        CD.CardItem("not_triggered", "Not triggered: it depends on an event that no line says is going ahead.",
                    "Not triggered: it depends on an event no line says is going ahead.",
                    "Not triggered: depends on an event no line says is going ahead."),
        CD.CardItem("waived", "Waived: someone allowed lets the maker off by the due date, before the maker says it "
                              "is done.",
                    "Waived: someone allowed lets the maker off by the due date, before the maker says done.",
                    "Waived: someone allowed lets the maker off by the due date, before the maker says done."),
        CD.CardItem("kept", "Kept: its maker says it is done by the due date.",
                    "Kept: its maker says done by the due date.", "Kept: its maker says done by the due date."),
        CD.CardItem("broken", "Broken: the maker took it back, or its due date is before the question's date.",
                    "Broken: the maker took it back, or the due date is before the question's date.",
                    "Broken: the maker took it back, or the due date is before the question's date."),
        CD.CardItem("not_yet_due", "Not yet due: none of the above.", "Not yet due: none of the above.",
                    "Not yet due: none of the above."),
        CD.CardItem("allowed", "Allowed to say yes to a new date or let the maker off: the person it was made to"
                               "<<AUTH_PART>>, never the maker.",
                    "Allowed to say yes to a new date or let the maker off: the person it was made to<<AUTH_PART>>, "
                    "never the maker.",
                    "Allowed to say yes or let off: the person it was made to<<AUTH_PART>>, never the maker."),
    ),
    tail=CLOSED_WORLD, numbered=False)
CARD_SHARES = {"full": 0.10, "compact": 0.75, "short": 0.15}      # spec 3.0: a short card on about 15% of rows
ADDRESS = {"chat": "the person it @-mentions", "log": "the person in its to column"}
AUTH_PART = ", and {AUTH} (pinned rule)"
HEADER = {"chat": "Chat log (oldest first):", "log": "Chat export (date | from | to | message):"}
STAMP = {"chat": "dmy_abbr", "log": "iso"}          # pinned timestamp forms (dates inside messages stay free)
GROUP = "group"

# ------------------------------------------------------------------------------------------------ pools (stand-ins)
NAMES = ("Ana", "Lee", "Mo", "Priya", "Tomas", "Ines", "Kofi", "Rhea", "Sami", "Yuki", "Dara", "Femi", "Lena",
         "Oskar", "Nadia", "Ravi", "Elif", "Bruno", "Hana", "Jonas", "Zara", "Malik", "Greta", "Arlo", "Wren", "Ivo",
         "Leila", "Omar", "Tess", "Kai")
RESERVE_NAMES = ("Quinn", "Rosa", "Ugo", "Vera")                     # G4 renames only

# ------------------------------------------------------------------------------------------------ shares (G0 2-4)
# F1/F2: with the six G-TW drops gone, a complement for every yes/no base and no yes/no twins, the yes/no rows are 49% of
# the rows (bar 45-55%) with ch_status 40% of the bases; every yes/no pair holds one "yes = bad" form and one good one
# (yes-is-bad 50%, bar 50 +- 5). Fitted on 3,200 units.
BASE_SHARES = (("ch_status", 0.40), ("ch_due", 0.13), ("yn_broken", 0.12), ("yn_kept", 0.205), ("yn_kept_vs", 0.105),
               ("yn_dneg_broken", 0.04))
# F3: the EMITTED ch_status golds (base + twin + equiv / attack rows) are 20% each. The closed label "Not triggered" is
# the unique longest of the five, so any other gold share moves gold-is-longest (G10 +/- 2 pp) and lets a status prior
# predict the gold (G6 / G7 choice). The verdict's flat 20% base shares do not give that: most minimal edits land on
# Broken / Not yet due (measured on 4,000 ch_status specs: 25% / 25% emitted with flat shares, Kept 17%, Waived 17%,
# Not triggered 15%). The base shares below (each inside the G0 band 12-30%) and STATUS_TWIN_KEEP / P_SECOND_TWIN (the
# twin thinning, below) were fitted on 9,000 ch_status specs (G0 section 4); they are re-fitted whenever the twin supply
# moves (story budget, twin rates).
STATUS_SHARES = (("kept", 0.255), ("broken", 0.125), ("not_yet_due", 0.19), ("not_triggered", 0.275), ("waived", 0.155))
NOT_BROKEN = (("kept", 0.28), ("not_yet_due", 0.32), ("not_triggered", 0.18), ("waived", 0.22))
NOT_KEPT = (("broken", 0.40), ("not_yet_due", 0.25), ("not_triggered", 0.15), ("waived", 0.20))
DUE_STATUS = (("kept", 0.35), ("broken", 0.30), ("not_yet_due", 0.35))
BROKEN_KIND = (("late", 0.35), ("time", 0.40), ("retract", 0.25))
COND_KIND = (("off", 0.45), ("open", 0.30), ("open_late", 0.25))
COMPLEMENTS = {"yn_broken": (("yn_other_than_broken", 0.65), ("yn_not_broken", 0.35)),
               "yn_kept": (("yn_not_kept", 1.0),), "yn_kept_vs": (("yn_unkept_vs", 1.0),)}
# Complement on EVERY base that has one (was 0.6): with the question forms about two of the five statuses (broken, kept),
# a yes/no row's status predicts its gold when it has no complement (Not triggered / Not yet due / Waived are 'no' for
# every positive form): P(yes | status) was .60 broken, .63 kept, .27 not triggered, .26 not yet due, .26 waived, so a
# reader of the chat alone (no question) got 65% and the bag-of-words LR of G6 (c) got +2.9 pp on 1,500 yes/no rows
# (p .015). A complement shares the base's chat and flips the gold: every pair is balanced per status. Yes/no twins (their
# status moves with the flip) are cut to 10% of the yes/no bases for the same reason (P_TWIN_PAIR 0.25): oracle 58% -> 55%.
# Equiv 0.10 -> 0.14: ~5.4% of the rows was on the 5% bar (3 of 6 independent 1,000-row draws were under it).
P_COMPLEMENT, P_EQUIV, P_INV = 1.0, 0.14, 0.08
# F2: a minimal-edit twin exists for 97.6% of yes bases but only 43.9% of no bases, so a flat 0.5 made the twins 67%
# "no" and the family's yes rate 45.6% (bar 48-52). The verdict's fix (1.0 / 0.45) balanced the yes rate but gave a
# yes/no twin to 44% of the bases; a yes/no twin changes the status with the gold, which is what lets the chat alone
# predict the gold (P_COMPLEMENT note above). A yes/no seed pair now asks for its twins together (both bases have one
# and a pair-level draw < P_TWIN_PAIR 0.25: ~10% of the yes/no bases; one yes twin and one no twin, so the yes rate does not
# drift), and the bulk of the twins (spec 4.1: 20-25% of the rows) are choice twins: every ch_status / ch_due base that has
# an edit gets one, and a second with probability P_SECOND_TWIN (pick_choice_twins). A ch_status edit is accepted with
# probability STATUS_TWIN_KEEP[the status it lands on]: most edits land on Broken / Not yet due, so without the thinning
# the emitted golds were 23% Broken, 23% Not yet due, 17% Not triggered (fitted with the base shares, 9,000 specs).
P_TWIN_PAIR, P_SECOND_TWIN, P_SECOND_TWIN_DUE = 0.25, 0.75, 1.0
STATUS_TWIN_KEEP = {"kept": 1.0, "broken": 0.58, "not_yet_due": 0.35, "not_triggered": 0.82, "waived": 0.89}
P_TWIN_ASOF = 0.3                             # status-date twins only this often when another edit exists
CARDS = 6                                     # per sampler; cards 0-3 pin an AUTH, card % 6 picks the pack
SAMPLER_STYLE = {"S1": "chat", "S2": "chat", "S3": "log", "S4": "chat"}
N_MEMBERS = {"S1": (2, 4), "S2": (3, 4), "S3": (3, 4), "S4": (3, 4), "S5": (2, 4)}
N_DECOYS = {"S1": (1, 2), "S2": (1, 2), "S3": (1, 2), "S4": (1, 2), "S5": (1, 2)}      # F6: S3 (2, 3) -> (1, 2)
MAX_LINES = {"S1": 6, "S2": 6, "S3": 7, "S4": 7, "S5": 6}                                # F6: 9 / 9 / 10 / 10 / 9
P_BOUND = {"S1": 0.3, "S2": 0.8, "S3": 0.3, "S4": 0.3, "S5": 0.4}
P_UNALLOWED = {"S1": 0.25, "S2": 0.5, "S3": 0.25, "S4": 0.3, "S5": 0.25}
P_TRY = {"S1": 0.2, "S2": 0.15, "S3": 0.15, "S4": 0.45, "S5": 0.25}
P_AFTER = {"S1": 0.4, "S2": 0.4, "S3": 0.4, "S4": 0.5, "S5": 0.4}       # 0.3 / 0.3 / 0.3 / 0.45 / 0.3: the depth plan cost after_asof 3 pp
P_COND = {"S1": 0.28, "S2": 0.25, "S3": 0.28, "S4": 0.3, "S5": 0.28}
P_EXT = {"S1": 0.3, "S2": 0.4, "S3": 0.3, "S4": 0.3, "S5": 0.3}
P_REMIND = {"S1": 0.2, "S2": 0.15, "S3": 0.2, "S4": 0.45, "S5": 0.2}
P_ACK, P_RETRACT_WAIVED, P_AUTH_THIRD = 0.25, 0.3, 0.7
DEEP_DAMP = 1.0                               # F5 (0.5 -> 0.25 in the verdict): replaced by the depth plan below (no damping)
# Depth plan (G6 d_meta, found when the pilot is rerun at 1,500-3,000 rows: the chat's depth, the number of counted
# decisive lines, predicted the status: Kept 1.5, Waived 1.8, Not triggered 0.7, Not yet due 0.95 on average, so a
# gradient-boosted reader of (depth, qform) beat chance by +3 pp on yes/no rows and +7 pp on choice rows, and by 0 once
# depth was removed). The target depth of a spec (not ch_due) is drawn from the seed, independent of the status, and the
# story is drawn again until it has exactly that depth: every status then shows the same depth mix. Depth 0 does not
# occur (a status needs a decisive line); Not triggered has no depth-3 story (a called-off event leaves no room for a
# third), so its depth-3 draws are depth 2.
DEPTH_PLAN = ((1, 0.52), (2, 0.42), (3, 0.06))
DECOY_KINDS = ("plain", "done", "release", "retract", "cond_met", "cond_off", "ext_yes", "ext_no", "try")
# ch_due options (G0 section 5, rank fix): k = 3 on every row = the gold, the asked commitment's other date (the
# original or the requested one) and the neighbouring commitment's due date. The decoy commitments' due dates all fall
# before, all between or all after the asked commitment's two dates, 1/3 each (one label-blind draw per spec: sampler
# and seed only; one draw for all decoys, so the nearest one, which t32_wrong_commitment reads, is not skewed by its
# place in the chat), so the gold's sorted rank is uniform over 0..2 (extended golds sit above the original date,
# original golds below the requested one, 50/50 by seed pairs). The try date stays a trap in the text but is never a
# ch_due option: it exists for original golds only and would make k (or the rank) carry the answer.
DUE_K = 3
DUE_OPTION_MODELS = ("t32_ignore_extension", "t32_unaccepted_extension", "t32_anyone_may_agree",
                     "t32_ignore_status_date", "drop_inclusive_endpoint", "t32_wrong_commitment")
DUE_DECOY_SPREAD = 5                          # days before the first / after the second asked date
CHEAP_DATE_FORMS, DEAR_DATE_FORMS, P_CHEAP_DATES = ("dmy", "dmy_abbr"), ("iso", "mdy", "wdmy", "wmdy"), 0.6
ASOF_REACH = 14                               # F4: a ch_due status date may lie up to this many days after the last line

QUESTION_FORMS = (
    QuestionForm("ch_status", "choice", answer_set="closed"),
    QuestionForm("ch_due", "choice", answer_set="open"),
    QuestionForm("yn_broken", "noul", "broken", 1, yes_is_bad=True),
    QuestionForm("yn_not_broken", "noul", "broken", -1, "syntactic", yes_is_bad=False),
    QuestionForm("yn_other_than_broken", "noul", "broken", -1, "implicit", yes_is_bad=False),
    QuestionForm("yn_dneg_broken", "noul", "broken", 1, yes_is_bad=True),
    QuestionForm("yn_kept", "noul", "kept", 1, yes_is_bad=False),
    QuestionForm("yn_not_kept", "noul", "kept", -1, "syntactic", yes_is_bad=True),
    QuestionForm("yn_kept_vs", "noul", "kept", 1, yes_is_bad=False),
    QuestionForm("yn_unkept_vs", "noul", "kept", -1, "option_framing", yes_is_bad=True),
)

# ------------------------------------------------------------------------------------------------ error models (G0 5)
FLAG_MODELS = {   # name -> (solver-A flag, description)
    "t32_try_as_commitment": ("try_commit", "takes the date of an earlier 'I'll try' message as the due date"),
    "t32_ignore_condition": ("ignore_cond", "treats a commitment that depends on an event as unconditional"),
    "t32_anyone_may_agree": ("anyone", "accepts a release or a new date from any member of the chat"),
    "t32_ignore_extension": ("ignore_ext", "ignores an agreed new due date"),
    "t32_unaccepted_extension": ("any_ext", "applies a requested new due date whatever the reply"),
    "t32_ignore_status_date": ("ignore_asof", "counts messages sent after the status date"),
    "t32_late_done_counts": ("late_ok", "counts a task reported done after the due date as kept"),
    "t32_retraction_releases": ("retract_releases", "treats taking a commitment back as being let off"),
    "drop_inclusive_endpoint": ("exclusive", None),
}
OTHER_MODELS = {
    "t32_latest_message": "reads the status off the last counted message about the task",
    "t32_wrong_commitment": "answers for the commitment listed next to the asked one",
}
for _n, (_f, _d) in FLAG_MODELS.items():
    if _d:
        register_name(_n, _d)
for _n, _d in OTHER_MODELS.items():
    register_name(_n, _d)

LABEL_STEMS = ("kept", "keep", "keeps", "keeping", "broken", "break", "breaks", "waive", "waived", "waives", "due",
               "trigger", "triggered", "triggers")
# v2 (Haiku pass H9, H10): a message carries no date of its own outside {DUE} / {NEW_DUE}: no relative-time word, no
# day / week / month word and no number word (the dates in a message are the slots, in an absolute kit date form)
TIME_WORDS = frozenset(gsl.CORE["relative_time"] | gsl.EXTENDED["relative_time"] | gsl.CORE["number"]) | frozenset((
    "day", "days", "week", "weeks", "weekend", "weekends", "fortnight", "month", "months", "year", "years", "eod",
    "eow", "tmrw", "tmr", "tonite"))


# F8 (G5-H watch item, G0 section 8 point 9): "is it not the case that X has not broken ...?" reads either as the plain
# double negation (yes iff broken, the G0 reading) or as the biased question "isn't it so that he hasn't broken it?"
# (yes iff NOT broken): the one dneg row in the pilot's 100 reads split the two readers. A yn_dneg_broken wording must
# therefore put the double negation inside a truth evaluation: "Is the following statement true: it is not the case
# that X has not broken ...?" (yes iff the statement is true iff broken).
DNEG_FRAME = re.compile(r"\bis\s+(?:the\s+following|this)\s+(?:statement|claim|sentence)\s+(?:true|correct|accurate|"
                        r"right)\b", re.I)


def wording_problems(qform: str, text: str) -> list:
    """Why a question wording may not be used by T32 (empty = usable): the polarity rule for yes/no forms (c2_kit.polarity;
    F1) and, for yn_dneg_broken, the truth-evaluation frame (F8). Label-blind: reads the wording, never a row."""
    out = POL.form_problems(T32, qform, text)
    if qform == "yn_dneg_broken" and not DNEG_FRAME.search(text or ""):
        out.append("F8 the double negation is not asked as a truth evaluation ('is the following statement true: it is "
                   "not the case that ... has not broken ...?')")
    return out


class _Retry(Exception):
    """A drawn story does not fit its date ranges: draw again (label-blind, same goal)."""


@dataclass(frozen=True)
class Ev:
    i: int                  # line index in the chat
    role: str               # commit, try, cond, ext_ask, ext_reply, done, release, retract, remind, ack
    c: int | None           # commitment index (0 = the asked one), None for chatter
    sem: str
    date: dt.date
    spk: str
    to: str | None
    args: dict              # form slot -> python value (date or category key)


@functools.lru_cache(maxsize=4096)
def _strata(key: tuple, block: int, size: int) -> tuple:
    return tuple(sorted(range(size), key=lambda i: uhash(FAMILY, "strat", *key, block, i)))


def _strat(*key, idx: int, size: int) -> float:
    """A label-blind STRATIFIED uniform draw: idx runs through blocks of `size`; inside a block the `size` strata of
    [0, 1) are visited in a seeded order, so every block holds each stratum once (plus a seeded jitter). The shares of the
    question forms, status goals and target depths then hold inside each block, not only on average: a pilot of 1,000
    rows is about two blocks, and its yes/no share (bar 45-55%) and status mix no longer ride on the luck of 600 coin
    flips (the pair-level qform draw alone gave 54-55% yes/no in the pilot's leading seeds, 49% over 10,000 units)."""
    block, pos = divmod(idx, size)
    return (_strata(key, block, size)[pos] + uhash(FAMILY, "stratj", *key, idx)) / size


def pick_choice_twins(key: tuple, pool: list, qform: str, keep: dict, p_second: float) -> list:
    """The twins of a choice base: its edits (kind, name, twin spec, predicted answer, new value) in a seeded order, kinds
    first, a ch_status edit accepted with probability keep[the status it lands on]; the first accepted one, and a second
    with probability p_second. Label-blind apart from that thinning, which only decides which twin rows exist."""
    order = sorted(pool, key=lambda c: (uhash(FAMILY, "twinkind", *key, c[0]), uhash(FAMILY, "twinord", *key, c[1],
                                                                                      str(c[4]))))
    out = []
    for c in order:
        if qform == "ch_status" and uhash(FAMILY, "twinkeep", *key, c[0], c[1], str(c[4])) >= keep[c[3]]:
            continue
        out.append(c)
        if len(out) == 2 or uhash(FAMILY, "twin2", *key) >= p_second:
            break
    return out


def _draw(shares, u: float):
    acc = 0.0
    for k, w in shares:
        acc += w
        if u < acc:
            return k
    return shares[-1][0]


def _between(rng: random.Random, lo: dt.date, hi: dt.date) -> dt.date:
    if hi < lo:
        raise _Retry(f"empty date range {lo} .. {hi}")
    return lo + DAY * rng.randint(0, (hi - lo).days)


def _due_decoy_date(rng: random.Random, due0: dt.date, due2, u: float) -> dt.date:
    """A ch_due decoy commitment's due date: before the asked commitment's original date, strictly between it and the
    requested date, or after the requested date, 1/3 each by the label-blind draw u (never equal to either)."""
    if due2 is None or (due2 - due0).days < 2:
        raise ContractError("ch_due needs a requested date at least 2 days after the original one")
    if u < 1 / 3:
        return due0 - DAY * rng.randint(1, DUE_DECOY_SPREAD)
    if u < 2 / 3:
        return due0 + DAY * rng.randint(1, (due2 - due0).days - 1)
    return due2 + DAY * rng.randint(1, DUE_DECOY_SPREAD)


def lint_message_form(text: str) -> list:
    """Family G-SL extra for message forms (G0 R4, section 7): no digit, month, weekday, name, status word, label
    word, relative-time / day-week-month word or number word outside the slots (the forms are lexicon clauses, so the
    skin lint does not read them)."""
    lit = K.PH_RE.sub(" ", text)
    bad = []
    if re.search(r"\d", lit):
        bad.append("digit")
    starts = {m.end() for m in re.finditer(r"(?:^|[.!?:;,]\s+)", lit)}
    for m in re.finditer(r"[A-Za-z]+(?:'[A-Za-z]+)?", lit):
        w, low = m.group(), m.group().lower()
        base = low.split("'")[0]
        if base in gsl.CORE["status"] or base in gsl.EXTENDED["status"]:
            bad.append(f"status word {w}")
        if base in LABEL_STEMS:
            bad.append(f"label word {w}")
        if base in TIME_WORDS or low in TIME_WORDS:
            bad.append(f"time or number word {w}")
        if w in S.MONTHS or w in S.WEEKDAYS:
            bad.append(f"date word {w}")
        if w[0].isupper() and m.start() not in starts and base != "i":
            bad.append(f"capitalised word {w}")
    return bad


class T32(C2Plugin):
    FAMILY = FAMILY
    TIER = "agent"
    G0_LITE = HERE / "G0_SPEC.md"
    G0_SHA256 = "1521a061fb3e6d43571d503d0589d1024dc05c923538b1d036fd3f39077ffaf0"   # frozen v3 (v2.1 + pilot fixes F1-F8)
    G0_AMBIGUITY_PASS = ("c2-data-stage-a amb:T32 (Haiku 5.5, 13 Oct 2026; 45 points H1-H45; "
                         "haiku/ambiguity/amb_T32.json)")
    SAMPLERS = ("S1", "S2", "S3", "S4", "S5")
    HELD_OUT_SAMPLERS = ("S5",)
    PARADIGM_A = "event_sourcing"
    PARADIGM_B = "sql_sqlite"
    SOLVER_B_MODULE = "families.T32.solver_b"
    QFORMS = {q.qform: q for q in QUESTION_FORMS}
    LABEL_WORDS = ("kept", "keep", "broken", "break", "waived", "waive", "due", "triggered", "trigger",
                   "not yet due", "not triggered")
    CLOSED_WORLD_SENTENCE = CLOSED_WORLD
    REGISTERS = ("family_chat", "landlord_tenant", "freelance_client", "team_chat", "flatmates", "club_volunteers",
                 "email_digest", "support_thread", "json_export", "sms_export", "forum_thread")
    HELD_OUT_REGISTERS = ("sms_export", "forum_thread")
    GSL_EXCEPTIONS = {"yet": "the status name 'not yet due' inside the yn_kept_vs / yn_unkept_vs wordings (G0 9)"}
    NAME_ALLOW = ()
    # c2_kit.polarity (F1): a yes/no wording must read with its form's polarity. This leaves out the yn_other_than_broken
    # wordings built on "apart from" / "besides" (no negation cue, so the pair has no implicit cue: G-TW).
    POLARITY_CHECK = True
    POLARITY_NEGATIVES = ()

    def __init__(self, lexicon=None, vocab=None):
        """vocab None: the 30 frozen packs (packs_v2.frozen(), sha checked); packs_v2.standin() for the unit tests."""
        super().__init__(lexicon)
        self.vocab = vocab if vocab is not None else PV.frozen()
        self._form_cache: dict = {}
        self._pool_cache: dict = {}
        self._pair_cache: dict = {}
        self._screened: list = []                  # [(ctx, wording-screened ctx, {wording id: problems})]
        self._by_setting: dict = {}                # (id(ctx), setting) -> (ctx, ctx narrowed to the setting)
        self._settings = PV.skin_settings() if self.vocab.frozen else {}
        self._register_weight = PV.register_weights() if self.vocab.frozen else {}
        self.dneg_ok = self._clean_wordings("yn_dneg_broken")

    # ------------------------------------------------------------------------------------------- wordings (F1, F8)
    def _clean_wordings(self, qform: str) -> bool:
        """True when the lexicon holds an admitted question form of `qform` that passes wording_problems. Label-blind:
        the pool, not a row. Without a lexicon (contract checks) True."""
        if self.lexicon is None:
            return True
        from c2_kit.lexicon import question_sem
        sem = question_sem(FAMILY, qform)
        return any(f.sem_id == sem and self.lexicon.status(f.form_id) == "admitted"
                   and not wording_problems(qform, f.text) for f in self.lexicon.forms.values())

    def _screen(self, ctx):
        """(ctx without the wordings that fail wording_problems, {wording skin id: problems}); cached per context."""
        for c, screened, bad in self._screened:
            if c is ctx:
                return screened, bad
        bad = {sid: p for sid, sk in ctx.skins.items() if sk.kind == "wording" and sk.qform
               and (p := wording_problems(sk.qform, sk.text))}
        screened = KitCtx(skins={k: v for k, v in ctx.skins.items() if k not in bad}, lexicon=ctx.lexicon)
        self._screened.append((ctx, screened, bad))
        return screened, bad

    def ctx_for(self, spec, ctx):
        """The kit context a row of `spec` may draw from (pipeline.build_unit and render() both call it): no wording that
        fails wording_problems, and, with the frozen packs, only the narrative skins and Mode F intros tagged with the
        setting of the card's pack (G0 section 2: a card's pack and its skin agree). Cached."""
        screened, _bad = self._screen(ctx)
        setting = None
        if spec is not None and spec.pack and self._settings:
            setting = self.vocab.setting_of(spec.pack.split(":", 1)[1])
        if setting is None:
            return screened
        hit = self._by_setting.get((id(ctx), setting))
        if hit is not None and hit[0] is ctx:
            return hit[1]
        keep = {k: v for k, v in screened.skins.items() if setting in self._settings.get(k, (setting,))}
        out = KitCtx(skins=keep, lexicon=ctx.lexicon)
        self._by_setting[(id(ctx), setting)] = (ctx, out)
        return out

    def _pick_skin(self, ctx, key: str, held: bool):
        """The narrative skin / Mode F intro of a row: the register first (a label-blind weighted draw from the row key;
        packs_v2.register_weights keeps every register under 15% of the rows), then a skin of that register. Without the
        frozen pools (unit tests) every register weighs 1."""
        regs = sorted({s.register for s in ctx.skins.values() if s.kind == "skin" and s.held_out == held})
        if not regs:
            return ctx.pick(FAMILY, "skin", key, held_out=held)
        w = [self._register_weight.get(r, 1.0) for r in regs]
        u, acc = uhash(key, "register") * sum(w), 0.0
        reg = regs[-1]
        for r, x in zip(regs, w):
            acc += x
            if u < acc:
                reg = r
                break
        return ctx.pick(FAMILY, "skin", key, register=reg, held_out=held)

    def quarantined_wordings(self, ctx) -> dict:
        """{wording skin id: problems} for the wordings ctx_for() leaves out of `ctx`."""
        return dict(self._screen(ctx)[1])

    # ------------------------------------------------------------------------------------------- lexicon forms
    def _forms_of(self, sem: str) -> list:
        """Admitted forms of a message sem with exactly its G0 slot signature and a clean family lint."""
        if sem in self._form_cache:
            return self._form_cache[sem]
        if self.lexicon is None:
            raise ContractError("T32 needs its lexicon registry (T32(lexicon=...))")
        ids = sorted(fid for fid, f in self.lexicon.forms.items()
                     if f.sem_id == sem and self.lexicon.status(fid) == "admitted"
                     and tuple(sorted(n for n, _ in f.slots)) == SIG[sem]
                     and all(k == ("date" if n in ("DUE", "NEW_DUE") else "category") for n, k in f.slots)
                     and not lint_message_form(f.text))
        if not ids:
            raise ContractError(f"no admitted message form for {sem}")
        self._form_cache[sem] = ids
        return ids

    def _short_forms(self, sem: str) -> list:
        """F6: the usable forms of a sem whose literal text (outside the slots) is at or under the sem's median length
        (characters; the pinned tokenizer is not needed and the choice is the same on every machine). A message line is
        printed on every row, so the shorter half costs fewer tokens per row; the pick among them stays a seeded,
        label-blind draw. At least 3 forms are kept (all of them when the sem has fewer)."""
        if sem not in self._pool_cache:
            ids = self._forms_of(sem)
            lens = {f: len(K.PH_RE.sub("", self.lexicon.forms[f].text)) for f in ids}
            med = sorted(lens.values())[(len(ids) - 1) // 2]
            short = [f for f in ids if lens[f] <= med]
            self._pool_cache[sem] = short if len(short) >= 3 else list(ids)
        return self._pool_cache[sem]

    def _pick_form(self, sem: str, sampler: str, seed: int, i: int) -> str:
        return min(self._short_forms(sem), key=lambda f: uhash(FAMILY, "form", sampler, seed, i, f))

    # ------------------------------------------------------------------------------------------- sampling
    def sample(self, seed: int, sampler: str) -> Spec:
        if sampler not in self.SAMPLERS:
            raise ContractError(f"sampler {sampler}")
        pair = seed // 2
        qform = _draw(BASE_SHARES, _strat("qform", sampler, idx=pair, size=50))
        if qform == "yn_dneg_broken" and not self.dneg_ok:      # F8: no clean wording admitted yet: ask yn_broken
            qform = "yn_broken"
        card = min(CARDS - 1, int(uhash(FAMILY, "card", sampler, pair) * CARDS))
        goal = self._goal(qform, seed, sampler)
        rng = random.Random(f"{FAMILY}|{sampler}|{seed}")
        for _ in range(MAX_TRIES):
            try:
                return self._build(rng, seed, sampler, qform, card, goal)
            except _Retry:
                continue
        raise ContractError(f"no story for {goal} after {MAX_TRIES} draws ({sampler}, seed {seed})")

    @staticmethod
    def _goal(qform: str, seed: int, sampler: str) -> dict:
        """Label-first target (seed pairs share qform and card; the yes bit alternates within a pair)."""
        yes = (seed % 2 == 0) != (uhash(FAMILY, "flip", sampler, seed // 2) < 0.5)
        u = _strat("status", sampler, idx=seed, size=100)
        if qform == "ch_status":
            return {"status": _draw(STATUS_SHARES, u), "ext": None}
        if qform == "ch_due":
            return {"status": _draw(DUE_STATUS, u), "ext": "extended" if yes else "original"}
        if qform in ("yn_broken", "yn_dneg_broken"):
            return {"status": "broken" if yes else _draw(NOT_BROKEN, u), "ext": None}
        return {"status": "kept" if yes else _draw(NOT_KEPT, u), "ext": None}

    def _build(self, rng, seed, sampler, qform, card, goal) -> Spec:
        year0 = dt.date(2027 if sampler == "S5" else 2026, 1, 4)
        pack = self.vocab.pack_for(sampler, card)          # F7: the card's own pack (30 frozen packs, one per card)
        style = SAMPLER_STYLE.get(sampler) or ("log" if card % 2 else "chat")
        members = rng.sample(NAMES, rng.randint(*N_MEMBERS[sampler]))
        auth = rng.choice(members) if card < 4 else None
        tasks = self.vocab.pack_tasks(pack)
        conds = self.vocab.pack_conds(pack)
        task_table = self.vocab.table("tasks", tasks)
        cond_table = self.vocab.table("conds", conds)
        rng.shuffle(tasks)
        rng.shuffle(conds)
        base = year0 + DAY * rng.randrange(0, 300)
        maker, promisee = rng.sample(members, 2)
        allowed = {promisee, auth} - {None, maker}
        thirds = [m for m in members if m not in allowed and m != maker]
        auth_third = auth if auth is not None and auth not in (maker, promisee) else None
        others = [m for m in members if m != maker]
        sl: dict = {}
        evs: list = []
        status, budget = goal["status"], MAX_LINES[sampler]

        def add(story, role, sem, date, spk, to, c, bind):
            evs.append(SimpleNamespace(story=story, seq=len(evs), role=role, sem=sem, date=date, spk=spk, to=to,
                                       c=c, bind=dict(bind)))

        def cat(key, table):
            return S.category_slot(key, table)

        # ---- the asked commitment (index 0), G0 R9 story plans
        c0 = base + DAY * rng.randint(2, 5)
        due = c0 + DAY * rng.randint(3, 8)
        sl["TASK0"], sl["DUE0"] = cat(tasks[0], task_table), S.date_slot(due)
        td0 = {"TASK": "TASK0"}
        cond_kind = None
        if status == "not_triggered":
            cond_kind = _draw(COND_KIND, rng.random())
        elif rng.random() < P_COND[sampler] * (DEEP_DAMP if goal["ext"] else 1.0):
            cond_kind = "met"
        if cond_kind:
            sl["COND0"] = cat(conds[0], cond_table)
        if rng.random() < P_TRY[sampler]:
            try_due = _between(rng, c0 + DAY, due + 4 * DAY)
            if try_due == due:
                try_due = due + DAY
            sl["TRY0"] = S.date_slot(try_due)
            add(0, "try", "chat.try", c0 - DAY * rng.randint(1, 2), maker,
                rng.choice(others) if rng.random() < 0.5 else None, 0, {"TASK": "TASK0", "DUE": "TRY0"})
        bind = {"TASK": "TASK0", "DUE": "DUE0", **({"COND": "COND0"} if cond_kind else {})}
        add(0, "commit", "chat.commit_if" if cond_kind else "chat.commit", c0, maker, promisee, 0, bind)
        if rng.random() < P_ACK:
            add(0, "ack", "chat.ack", c0, promisee, None, None, {})
        e0, cond_date = c0, None
        if cond_kind in ("met", "off"):
            cond_date = _between(rng, c0, due - DAY)
            add(0, "cond", "chat.cond_met" if cond_kind == "met" else "chat.cond_off", cond_date, rng.choice(members),
                None, 0, {"COND": "COND0"})
            e0 = cond_date
        ext = None
        if goal["ext"] == "extended":
            ext = "yes_auth"
        elif goal["ext"] == "original":
            ext = rng.choice(("no", "ask_only") + (("yes_unauth",) if thirds else ()))
        elif rng.random() < P_EXT[sampler] * (DEEP_DAMP if cond_kind else 1.0):          # also a not-triggered story (depth plan)
            ext = rng.choice(("yes_auth", "no", "ask_only") + (("yes_unauth",) if thirds else ()))
        due2 = None
        if ext:
            ask = _between(rng, e0, due)
            due2 = due + DAY * rng.randint(2, 6)
            sl["NEWDUE0"] = S.date_slot(due2)
            add(0, "ext_ask", "chat.ext_ask", ask, maker, promisee, 0, {"TASK": "TASK0", "NEW_DUE": "NEWDUE0"})
            e0 = ask
            if ext != "ask_only":
                reply = _between(rng, ask, due)
                if ext == "yes_auth":
                    who = auth_third if auth_third and rng.random() < P_AUTH_THIRD else promisee
                    add(0, "ext_reply", "chat.ext_yes", reply, who, maker, 0, {"TASK": "TASK0", "NEW_DUE": "NEWDUE0"})
                elif ext == "yes_unauth":
                    add(0, "ext_reply", "chat.ext_yes", reply, rng.choice(thirds), maker, 0,
                        {"TASK": "TASK0", "NEW_DUE": "NEWDUE0"})
                else:
                    add(0, "ext_reply", "chat.ext_no", reply, promisee, maker, 0, td0)
                e0 = reply
        due_eff = due2 if ext == "yes_auth" else due
        bound = rng.random() < P_BOUND[sampler]
        after = rng.random() < P_AFTER[sampler]
        unallowed = bool(thirds) and rng.random() < P_UNALLOWED[sampler]

        def release(date, who):
            add(0, "release", "chat.release", date, who, maker, 0, td0)

        def done(date):
            add(0, "done", "chat.done", date, maker, promisee, 0, td0)

        if status == "kept":
            if ext == "yes_auth" and rng.random() < 0.6:
                t = _between(rng, max(e0, due + DAY), due2)
            elif bound:
                t = due_eff
            else:
                t = _between(rng, e0, due_eff)
            if unallowed:
                release(_between(rng, e0, t), rng.choice(thirds))
            done(t)
            asof = t if bound and rng.random() < 0.4 else t + DAY * rng.randint(0, 6)
        elif status == "broken":
            kind = _draw(BROKEN_KIND, rng.random())
            if kind == "late":
                if ext in ("no", "ask_only", "yes_unauth") and rng.random() < 0.6:
                    t = _between(rng, due + DAY, due2)
                else:
                    t = due_eff + DAY * (1 if bound else rng.randint(1, 3))
                if unallowed:
                    release(_between(rng, e0, due_eff), rng.choice(thirds))
                done(t)
                if after and (t - due_eff).days >= 2:
                    asof = _between(rng, due_eff + DAY, t - DAY)
                else:
                    asof = t + DAY * rng.randint(0, 4)
            elif kind == "time":
                if unallowed:
                    release(_between(rng, e0, due_eff), rng.choice(thirds))
                asof = due_eff + DAY * (1 if bound else rng.randint(1, 5))
                if after:
                    done(asof + DAY * rng.randint(1, 3))
            else:
                r0 = _between(rng, e0, due_eff)
                add(0, "retract", "chat.retract", r0, maker, promisee, 0, td0)
                last = r0
                if unallowed:
                    last = _between(rng, r0, due_eff)
                    release(last, rng.choice(thirds))
                asof = last + DAY * rng.randint(0, 5)
        elif status == "not_yet_due":
            if ext == "yes_auth" and rng.random() < 0.6:
                asof = _between(rng, max(e0, due + DAY), due2)
            elif bound:
                asof = due_eff
            else:
                asof = _between(rng, e0, due_eff)
            if unallowed:
                release(_between(rng, e0, asof), rng.choice(thirds))
            if after:
                if not unallowed and asof < due_eff and rng.random() < 0.4:
                    release(_between(rng, asof + DAY, due_eff), promisee)
                else:
                    done(asof + DAY * rng.randint(1, 3))
        elif status == "not_triggered":
            if cond_kind == "off":
                asof = cond_date + DAY * rng.randint(0, (due - cond_date).days + 4)
            elif cond_kind == "open":
                asof = c0 + DAY * rng.randint(0, (due - c0).days + 4)
            else:
                asof = _between(rng, c0, due - 2 * DAY)
                met = _between(rng, asof + DAY, due - DAY)
                add(0, "cond", "chat.cond_met", met, rng.choice(members), None, 0, {"COND": "COND0"})
                if after:
                    done(_between(rng, met, due))
        else:   # waived
            who = auth_third if auth_third and rng.random() < P_AUTH_THIRD else promisee
            if rng.random() < P_RETRACT_WAIVED:
                r0 = _between(rng, e0, due_eff)
                add(0, "retract", "chat.retract", r0, maker, promisee, 0, td0)
                w = _between(rng, r0, due_eff)
            else:
                w = due_eff if bound else _between(rng, e0, due_eff)
            release(w, who)
            asof = w + DAY * rng.randint(0, 5)
        if rng.random() < P_REMIND[sampler]:
            add(1, "remind", "chat.remind", _between(rng, c0 + DAY, asof + 2 * DAY), rng.choice(others), None, 0,
                td0)
        if len(evs) > budget:
            raise _Retry("asked story longer than the line budget")

        # ---- decoy commitments (stories 2..), each a different task, event and due date
        n_dec = rng.randint(*N_DECOYS[sampler])
        avoid = {due} | ({due2} if due2 else set())
        cond_i = 1 if cond_kind else 0
        for k in range(1, n_dec + 1):
            kind = rng.choice(DECOY_KINDS if k > 1 or qform != "ch_due" else DECOY_KINDS[:-1])
            if kind.startswith("cond") and cond_i >= len(conds):
                kind = "plain"
            size = {"plain": 1, "try": 1, "ext_yes": 3, "ext_no": 3}.get(kind, 2)
            if len(evs) + size > budget:
                if k == 1 and qform == "ch_due":
                    raise _Retry("the due-date question needs a neighbouring commitment (t32_wrong_commitment)")
                break
            pk, qk = rng.sample(members, 2)
            if qform == "ch_due":
                dk = _due_decoy_date(rng, due, due2, uhash(FAMILY, "due_region", sampler, seed))
                ck = dk - DAY * rng.randint(2, 9)
            else:
                ck = base + DAY * rng.randint(0, 8)
                dk = ck + DAY * rng.randint(2, 9)
                while dk in avoid:
                    dk += DAY
            sl[f"TASK{k}"], sl[f"DUE{k}"] = cat(tasks[k], task_table), S.date_slot(dk)
            tk = {"TASK": f"TASK{k}"}
            story = 1 + k
            if kind == "try":
                add(story, "try", "chat.try", ck, pk, qk if rng.random() < 0.5 else None, None,
                    {"TASK": f"TASK{k}", "DUE": f"DUE{k}"})
                continue
            if kind.startswith("cond"):
                sl[f"COND{k}"] = cat(conds[cond_i], cond_table)
                cond_i += 1
                add(story, "commit", "chat.commit_if", ck, pk, qk, k,
                    {"TASK": f"TASK{k}", "DUE": f"DUE{k}", "COND": f"COND{k}"})
                add(story, "cond", "chat." + kind, _between(rng, ck, dk - DAY), rng.choice(members), None, k,
                    {"COND": f"COND{k}"})
                continue
            add(story, "commit", "chat.commit", ck, pk, qk, k, {"TASK": f"TASK{k}", "DUE": f"DUE{k}"})
            if kind == "done":
                add(story, "done", "chat.done", _between(rng, ck, dk + 2 * DAY), pk, qk, k, tk)
            elif kind == "release":
                add(story, "release", "chat.release", _between(rng, ck, dk), rng.choice([m for m in members
                                                                                         if m != pk]), pk, k, tk)
            elif kind == "retract":
                add(story, "retract", "chat.retract", _between(rng, ck, dk), pk, qk, k, tk)
            elif kind in ("ext_yes", "ext_no"):
                a = _between(rng, ck, dk)
                sl[f"NEWDUE{k}"] = S.date_slot(dk + DAY * rng.randint(2, 5))
                add(story, "ext_ask", "chat.ext_ask", a, pk, qk, k, {"TASK": f"TASK{k}", "NEW_DUE": f"NEWDUE{k}"})
                if kind == "ext_yes":
                    add(story, "ext_reply", "chat.ext_yes", _between(rng, a, dk), qk, pk, k,
                        {"TASK": f"TASK{k}", "NEW_DUE": f"NEWDUE{k}"})
                else:
                    add(story, "ext_reply", "chat.ext_no", _between(rng, a, dk), qk, pk, k, tk)

        # ---- the chat in sending order (a story keeps its own order on a shared day)
        order = sorted(evs, key=lambda e: (e.date, uhash(FAMILY, "ord", sampler, seed, e.story), e.seq))
        order = self._story_order(order)
        msgs = []
        for i, e in enumerate(order):
            sl[f"T{i}"], sl[f"S{i}"] = S.date_slot(e.date), S.name_slot(e.spk)
            if e.to is not None:
                sl[f"A{i}"] = S.name_slot(e.to)
            sl[f"M{i}"] = self.lexicon.clause(self._pick_form(e.sem, sampler, seed, i), bind=e.bind)
            msgs.append({"role": e.role, "c": e.c, "to": e.to is not None, "bind": dict(sorted(e.bind.items()))})
        for j, m in enumerate(members):
            sl[f"P{j}"] = S.name_slot(m)
        if auth is not None:
            sl["AUTH"] = S.name_slot(auth)
        sl["WHO"], sl["QTASK"], sl["ASOF"] = S.name_slot(maker), cat(tasks[0], task_table), S.date_slot(asof)
        topics = self.vocab.pack_topics(pack)
        sl["TOPIC"] = cat(rng.choice(topics), self.vocab.table("topics", topics))
        sl["OWNER"] = S.name_slot(rng.choice(members))
        structure = {"style": style, "auth": auth is not None, "n_members": len(members), "msgs": msgs}
        spec = Spec(FAMILY, sampler, seed, f"{FAMILY}:{sampler}:c{card:02d}", qform, sl, structure=structure,
                    pack=f"t32:{pack}")
        if goal["ext"]:                                      # F4: the ch_due status date carries no option cue
            spec = self._spread_asof(spec, goal, sampler, seed)
        pl = self._plan(spec)
        if not self._plan_ok(pl):
            raise _Retry("story breaks a G0 R10 invariant")
        got = self._plan_status(pl)
        if (got != status and not goal["ext"]) or self._fold(spec)[0] != got:      # a ch_due status date may leave the goal
            raise ContractError(f"generator bug: goal {status}, plan {got}, solver A {self._fold(spec)[0]} "
                                f"({sampler}, seed {seed})")
        if goal["ext"] and (pl.due_eff == pl.due0) != (goal["ext"] == "original"):
            raise ContractError(f"generator bug: ch_due goal {goal['ext']} ({sampler}, seed {seed})")
        depth = sum(1 for e in (pl.cond, pl.ext_reply, pl.done, pl.retract, pl.release) if pl.counted(e))
        if not goal["ext"]:
            want = _draw(DEPTH_PLAN, _strat("depth", sampler, idx=seed, size=100))
            if status == "not_triggered":
                want = min(want, 2)
            if depth != want:
                raise _Retry(f"depth {depth}, target {want}")
        return spec.replace(depth=depth, deep=depth >= 3, tags=tuple(sorted(self._tags(spec, pl))))

    @staticmethod
    def _story_order(order: list) -> list:
        """Keep each story's own line order (the sort key already does on distinct days; this is a guard)."""
        seen: dict = {}
        for e in order:
            if e.story in seen and e.seq < seen[e.story]:
                raise _Retry("a story's lines left their order")
            seen[e.story] = e.seq
        return order

    def _spread_asof(self, spec: Spec, goal: dict, sampler: str, seed: int) -> Spec:
        """F4 (pilot G6 a_question leak on ch_due): the story anchored the status date on the answer, so the question's
        date equalled one of the three option dates in 41.8% of ch_due specs (that option was the gold 71.7% of the time)
        and the gold was the option nearest to the status date in 61%. A due-date row asks for the due date in force, not
        the status, so its status date is free to move wherever that date stays the same. Redraw it, label-blind:
          (i)  it equals none of the three option dates (the gold, the other asked date, the neighbouring due date);
          (ii) the gold's distance rank among the three (0 = nearest) is drawn from the seed, 1/3 each, among the ranks
               some valid date gives;
        keeping the gold (the due date in force), every R10 invariant (construction table and solver A agree) and an
        option set the named models can still build (a date before the request silences the "applies the requested
        date" models). The story's own date stays when it already meets (i) and (ii)."""
        pl = self._plan(spec)
        near = self._neighbours(spec)
        if not near:
            raise _Retry("the due-date question needs a neighbouring commitment")
        gold = pl.due_eff
        other = pl.newdue if gold == pl.due0 else pl.due0
        nb = near[0].args["DUE"]
        opts = {gold, other, nb}
        if len(opts) < 3:
            raise _Retry("two options are the same date")

        def klass(d):
            dg = abs((d - gold).days)
            others = [abs((d - o).days) for o in (other, nb)]
            return None if dg in others else sum(1 for x in others if x < dg)

        def valid(d):
            if d in opts or klass(d) is None:
                return False
            s2 = spec.with_slot("ASOF", S.date_slot(d))
            p2 = self._plan(s2)
            if not self._plan_ok(p2) or p2.due_eff != gold:
                return False
            if self._fold(s2)[1] != gold:
                return False
            outs = {m.fn(s2) for n, m in models.items() if n in DUE_OPTION_MODELS}
            return {other.isoformat(), nb.isoformat()} <= outs

        models = self.error_models()
        lo, hi = pl.commit.date, max(e.date for e in pl.evs) + ASOF_REACH * DAY
        days = {d: klass(d) for d in (lo + DAY * i for i in range((hi - lo).days + 1)) if valid(d)}
        if not days:
            raise _Retry("no status date clears the option dates and keeps the option set buildable")
        allowed = sorted(set(days.values()))
        want = min(2, int(uhash(FAMILY, "due_prox", sampler, seed) * 3))
        if want not in allowed:
            want = allowed[min(len(allowed) - 1, int(uhash(FAMILY, "due_prox2", sampler, seed) * len(allowed)))]
        cur = spec.slots["ASOF"].value
        if days.get(cur) == want:
            return spec
        cands = [d for d, c in days.items() if c == want]
        pick = min(cands, key=lambda d: uhash(FAMILY, "asof_pick", sampler, seed, d.toordinal()))
        return spec.with_slot("ASOF", S.date_slot(pick))

    # ------------------------------------------------------------------------------------------- reading the spec
    def _events(self, spec: Spec) -> list:
        sl = spec.all_slots()
        out = []
        for i, m in enumerate(spec.structure["msgs"]):
            clause = sl[f"M{i}"]
            args = {fs: sl[ss].value for fs, ss in m["bind"].items()}
            out.append(Ev(i, m["role"], m["c"], clause.value[0], sl[f"T{i}"].value, sl[f"S{i}"].value,
                          sl[f"A{i}"].value if m["to"] else None, args))
        return out

    def _members(self, spec: Spec) -> list:
        return [spec.slots[f"P{j}"].value for j in range(spec.structure["n_members"])]

    # ------------------------------------------------------------------------------------------- solver A
    def _fold(self, spec: Spec, *, who=None, task=None, f=frozenset()) -> tuple:
        """Event sourcing (G0 R9): fold the counted messages through the state machine; returns (status, due).
        `f` swaps one rule (error models only)."""
        env = spec.env()
        who = who or env["WHO"]
        task = task or env["QTASK"]
        asof = env["ASOF"]
        auth = env.get("AUTH")
        evs = self._events(spec)
        if "ignore_asof" in f:
            asof = max([asof] + [e.date for e in evs])

        def passed(day, due):
            return day >= due if "exclusive" in f else day > due

        st, due, to, cond, try_due = None, None, None, None, None
        for e in evs:
            if e.date > asof:
                continue
            a = e.args
            if st is None:
                if e.sem in COMMIT_SEMS and e.spk == who and a["TASK"] == task:
                    due, to, cond = a["DUE"], e.to, a.get("COND")
                    if "try_commit" in f and try_due is not None:
                        due = try_due
                    st = "waiting" if cond is not None and "ignore_cond" not in f else "active"
                elif e.sem == "chat.try" and e.spk == who and a["TASK"] == task:
                    try_due = a["DUE"]
                continue
            if st in ("active", "retracted") and "late_ok" not in f and passed(e.date, due):
                st = "broken"
            if st in TERMINAL:
                continue
            if e.sem in ("chat.cond_met", "chat.cond_off"):
                if st == "waiting" and a["COND"] == cond:
                    st = "active" if e.sem == "chat.cond_met" else "not_triggered"
                continue
            if a.get("TASK") != task:
                continue
            allowed = (set(self._members(spec)) - {who}) if "anyone" in f else ({to, auth} - {None, who})
            if e.sem == "chat.ext_ask" and e.spk == who and "any_ext" in f and st in ("waiting", "active"):
                due = a["NEW_DUE"]
            elif e.sem == "chat.ext_yes" and e.spk in allowed and "ignore_ext" not in f and st in ("waiting",
                                                                                                 "active"):
                due = a["NEW_DUE"]
            elif e.sem == "chat.done" and e.spk == who and st == "active":
                st = "kept" if ("late_ok" in f or not passed(e.date, due)) else "broken"
            elif e.sem == "chat.release" and e.spk in allowed and st in ("active", "retracted"):
                st = "waived"
            elif e.sem == "chat.retract" and e.spk == who and st == "active":
                st = "waived" if "retract_releases" in f else "retracted"
        if st is None:
            raise ContractError(f"no commitment by {who} to {task} on or before the status date")
        if st == "waiting":
            st = "not_triggered"
        elif st == "retracted":
            st = "broken"
        elif st == "active":
            st = "broken" if passed(asof, due) else "not_yet_due"
        return st, due

    def _answer_of(self, qform: str, status: str, due: dt.date):
        if qform == "ch_status":
            return status
        if qform == "ch_due":
            return due.isoformat()
        return YN[qform](status)

    def solve_a(self, spec: Spec):
        status, due = self._fold(spec)
        return self._answer_of(spec.qform, status, due)

    # ------------------------------------------------------------------------------------------- construction table
    def _plan(self, spec: Spec) -> SimpleNamespace:
        """The asked commitment's story lines and the facts the construction table reads (never the gold)."""
        env = spec.env()
        evs = self._events(spec)
        mine = [e for e in evs if e.c == 0]
        pick = {r: next((e for e in mine if e.role == r), None)
                for r in ("commit", "cond", "ext_ask", "ext_reply", "done", "release", "retract")}
        pick["try_line"] = next((e for e in mine if e.role == "try"), None)
        pl = SimpleNamespace(**pick, evs=evs, mine=mine, asof=env["ASOF"], maker=env["WHO"], auth=env.get("AUTH"),
                             members=self._members(spec), due0=env["DUE0"], newdue=env.get("NEWDUE0"))
        pl.promisee = pl.commit.to
        pl.allowed = {pl.promisee, pl.auth} - {None, pl.maker}
        pl.conditional = pl.commit.sem == "chat.commit_if"
        pl.counted = lambda e: e is not None and e.date <= pl.asof
        yes = pl.ext_reply is not None and pl.ext_reply.sem == "chat.ext_yes" and pl.ext_reply.spk in pl.allowed
        pl.yes_ok = yes
        pl.due_eff = pl.newdue if yes and pl.counted(pl.ext_reply) else pl.due0
        return pl

    @staticmethod
    def _plan_status(pl) -> str:
        """G0 R9 as one closed formula over the story lines (valid under the R10 invariants)."""
        c = pl.counted
        if pl.conditional and not (c(pl.cond) and pl.cond.sem == "chat.cond_met"):
            return "not_triggered"
        if c(pl.release) and pl.release.spk in pl.allowed and pl.release.date <= pl.due_eff:
            return "waived"
        if c(pl.done):
            return "kept" if pl.done.date <= pl.due_eff else "broken"
        if c(pl.retract) or pl.asof > pl.due_eff:
            return "broken"
        return "not_yet_due"

    @staticmethod
    def _plan_ok(pl) -> bool:
        """The G0 R10 invariants an edit could break (solver B refuses such rows)."""
        if pl.commit.date > pl.asof or pl.release is not None and pl.release.spk == pl.maker:
            return False
        due_then = pl.newdue if pl.yes_ok else pl.due0
        if pl.release is not None:
            before_yes = pl.ext_reply is None or pl.release.i < pl.ext_reply.i
            if pl.release.date > (pl.due0 if before_yes else due_then):
                return False
        if pl.conditional and pl.cond is not None and pl.cond.sem == "chat.cond_off" and any(
                e is not None for e in (pl.done, pl.release, pl.retract)):
            return False
        dates = [e.date for e in pl.evs]
        return all(a <= b for a, b in zip(dates, dates[1:]))

    def _tags(self, spec: Spec, pl) -> set:
        tags = set()
        if pl.conditional:
            tags.add("conditional")
        if pl.ext_ask is not None:
            tags.add("extension")
        movers = [e for e in (pl.release, pl.ext_reply) if e is not None and e.sem != "chat.ext_no"]
        if any(e.spk not in pl.allowed for e in movers):
            tags.add("unallowed_move")
        if any(e.spk == pl.auth and pl.auth not in (pl.promisee, pl.maker) for e in movers):
            tags.add("auth_third")
        if pl.retract is not None:
            tags.add("retract")
        if pl.try_line is not None:
            tags.add("try_decoy")
        if any(e is not None and e.date > pl.asof for e in (pl.done, pl.release, pl.cond, pl.ext_reply)):
            tags.add("after_asof")
        if (pl.done is not None and pl.done.date in (pl.due_eff, pl.due_eff + DAY)) or pl.asof in (
                pl.due_eff, pl.due_eff + DAY):
            tags.add("boundary")
        if pl.counted(pl.done) and pl.done.date > pl.due_eff:
            tags.add("late_done")
        if self._latest_status(spec) != self._plan_status(pl):
            tags.add("latest_misleads")
        return tags

    # ------------------------------------------------------------------------------------------- facts (G3)
    def canonical(self, spec: Spec) -> dict:
        env = spec.env()
        msgs = [{"date": e.date.isoformat(), "from": e.spk, "to": e.to, "sem": e.sem,
                 "args": {k: (v.isoformat() if isinstance(v, dt.date) else v) for k, v in sorted(e.args.items())}}
                for e in self._events(spec)]
        return {"members": self._members(spec), "auth": env.get("AUTH"), "topic": env["TOPIC"],
                "owner": env["OWNER"], "messages": msgs, "who": env["WHO"], "task": env["QTASK"],
                "asof": env["ASOF"].isoformat(), "qform": spec.qform}

    def canonical_for(self, spec: Spec, author_mode: str) -> dict:
        c = self.canonical(spec)
        return c if author_mode == "T" else {k: v for k, v in c.items() if k not in ("topic", "owner")}

    def extract_view(self, spec: Spec) -> dict:
        c = self.canonical(spec)
        return {"topic": c["topic"], "owner": c["owner"]}

    def extract_fields(self, spec: Spec) -> list:
        from c2_kit.g3h import Field
        return [Field("topic", "category", "what the chat is about, as written", spec.slots["TOPIC"].params),
                Field("owner", "name", "the person who saved or shared the chat")]

    # ------------------------------------------------------------------------------------------- render
    def card_template(self, spec: Spec, style: str = "full") -> str:
        """The rule card of a card style (CARD_SPEC; G0 1.1): `<<ADDRESS>>` and `<<AUTH_PART>>` filled from the chat style
        and the pinned authority; `{AUTH}` stays a slot."""
        st = spec.structure
        text = CARD_SPEC.template(style, spec).replace("<<ADDRESS>>", ADDRESS[st["style"]])
        return text.replace("<<AUTH_PART>>", AUTH_PART if st["auth"] else "")

    @staticmethod
    def _cheap_dates(spec: Spec, forms: dict) -> dict:
        """F6: a date costs 7-8 tokens as '17 July 2026' / '17 Jul 2026' and 10-12 as ISO, 'July 17, 2026' or with the
        weekday, and a row prints about six of them. On 60% of the rows that drew a dearer form every free date is written
        the day-month-year way instead (the choice depends on the sampler and the seed alone, so a row and every partner
        of its unit agree: G-TW compares the state of complements and the unchanged slots of twins)."""
        key = f"{FAMILY}|{spec.sampler}|{spec.seed}"
        if uhash(key, "cheapdate") >= P_CHEAP_DATES:
            return forms
        cheap = CHEAP_DATE_FORMS[int(uhash(key, "cheapform") * len(CHEAP_DATE_FORMS))]
        slots = spec.all_slots()
        return {k: (cheap if slots[k].kind == "date" and v in DEAR_DATE_FORMS and cheap in S.forms(slots[k]) else v)
                for k, v in forms.items()}

    @staticmethod
    def card_style(spec: Spec) -> str:
        """The card style of a row (full / compact / short, CARD_SHARES): a label-blind draw from the sampler and the seed
        alone, so a row and every partner of its unit (complement, twin, equiv, attack) print the same card."""
        return CD.draw_style(f"{FAMILY}|{spec.sampler}|{spec.seed}", CARD_SHARES)

    def chat_template(self, spec: Spec) -> str:
        st = spec.structure
        lines = ["Members: " + ", ".join(f"{{P{j}}}" for j in range(st["n_members"])), HEADER[st["style"]]]
        for i, m in enumerate(st["msgs"]):
            if st["style"] == "chat":
                lines.append(f"[{{T{i}:{STAMP['chat']}}}] {{S{i}}}: " + (f"@{{A{i}}} " if m["to"] else "")
                             + f"{{M{i}}}")
            else:
                lines.append(f"{{T{i}:{STAMP['log']}}} | {{S{i}}} | " + (f"{{A{i}}}" if m["to"] else GROUP)
                             + f" | {{M{i}}}")
        return "\n".join(lines)

    def render(self, spec: Spec, ctx, *, skin=None, wording=None, forms=None, attack=None):
        key = f"{spec.family}|{spec.seed}|{spec.sampler}|{spec.qform}"
        held = spec.sampler in self.HELD_OUT_SAMPLERS
        ctx = self.ctx_for(spec, ctx)                       # F1 / F7: usable wordings, the card's setting
        skin = skin or self._pick_skin(ctx, key, held)
        wording = wording or ctx.pick(FAMILY, "wording", key, qform=spec.qform)
        if wording.qform != spec.qform:
            raise ContractError(f"wording {wording.skin_id} asks {wording.qform}, spec asks {spec.qform}")
        forms = self._cheap_dates(spec, forms or choose_forms(spec, key))
        slots = spec.all_slots()
        tb = TextBuilder()
        tb.add("state", skin.fill(slots, forms), skin_id=skin.skin_id)
        tb.add("state", "\n\n").add("state", K.fill(self.chat_template(spec), slots, forms))
        if attack is not None:
            tb.add("state", "\n\n").add("state", attack.fill(slots, forms), skin_id=attack.skin_id)
        # F6: the served prompt prints row.card once (yes/no rows) and row.instructions twice: yes/no rows carry the rules
        # in the card, choice rows keep them at the head of the instructions (cards.place_rules)
        style = self.card_style(spec)
        field = CD.place_rules(tb, K.fill(self.card_template(spec, style), slots, forms), self.QFORMS[spec.qform].qtype)
        tb.add("instructions", wording.fill(slots, forms), skin_id=wording.skin_id)
        ans = self.solve_a(spec)
        os_ = None
        if spec.qform == "ch_status":
            os_ = build_closed(spec, ans, list(STATUSES), self.error_models(), row_key=key,
                               render_key=STATUS_TEXT.__getitem__)
        elif spec.qform == "ch_due":
            fmt = forms["ASOF"]

            def as_text(iso):
                return S.render(S.date_slot(dt.date.fromisoformat(iso)), fmt)

            # k = 3 on every row, never lowered after a failed build (kit distractors.py); the gold's sorted rank is
            # uniform by construction (DUE_K note). A spec that cannot fill it is dropped.
            ems = self.error_models()
            # the row key carries the story's hash: a base, its (up to two) twins and its equiv partner are one cluster
            # of rows with the same dates, and one shared gold position would count the cluster's position 3-4 times in
            # G10's chi-square (3 options: p 0.003 on 119 rows); an attack partner is the same spec, so the same options
            os_ = build_options(spec, ans, {n: ems[n] for n in DUE_OPTION_MODELS}, k=DUE_K,
                                row_key=f"{key}|{spec.structure_hash()[:12]}", render_key=as_text)
            if os_ is None:
                raise K.RenderError("the due-date question needs the other asked date and a neighbouring due date")
        return assemble_row(self, spec, tb, answer=ans, option_set=os_, skin=skin, wording=wording, forms=forms,
                            attack=attack, defs_style=CD.defs_style(field, style))

    # ------------------------------------------------------------------------------------------- relations
    def relations(self, spec: Spec) -> list:
        out = []
        seed, smp = spec.seed, spec.sampler
        if spec.qform in COMPLEMENTS and uhash(FAMILY, "comp", smp, seed) < P_COMPLEMENT:
            out.append(RelationProposal("complement", qform=_draw(COMPLEMENTS[spec.qform],
                                                                  uhash(FAMILY, "ckind", smp, seed))))
        pair = self._pair(spec)
        u = uhash(FAMILY, "extra", smp, seed // 2 if pair is not None else seed)    # a yes/no seed pair decides together
        if spec.deep or (pair is not None and pair.deep):   # F5: a deep spec gets no equiv / attack partner
            pass
        elif u < P_EQUIV:
            other = "log" if spec.structure["style"] == "chat" else "chat"
            out.append(RelationProposal("equiv", spec=spec.replace(structure={**spec.structure, "style": other}),
                                        note="other container and skin"))
        elif u < P_EQUIV + P_INV:
            out.append(RelationProposal("inv"))
        if pair is None:                                 # choice rows: one or two minimal-edit twins
            for kind, name, twin, pred, _v in pick_choice_twins(
                    (spec.sampler, spec.seed), self._twin_pool(spec), spec.qform, STATUS_TWIN_KEEP,
                    P_SECOND_TWIN if spec.qform == "ch_status" else P_SECOND_TWIN_DUE):
                out.append(RelationProposal("twin", spec=twin, changed_slot=name, expect=pred, note=f"twin.{kind}"))
        elif self._asks_twin(spec, pair):
            t = self._twin(spec)
            if t is not None:
                out.append(t)
        out += self._metamorphic(spec)
        return out

    def _pair(self, spec: Spec):
        """A yes/no spec's seed-pair partner (the other yes bit of the same qform and card), else None."""
        if self.QFORMS[spec.qform].qtype != "noul":
            return None
        key = (spec.sampler, spec.seed ^ 1)
        if key not in self._pair_cache:
            if len(self._pair_cache) > 4096:
                self._pair_cache.clear()
            try:
                self._pair_cache[key] = self.sample(spec.seed ^ 1, spec.sampler)
            except ContractError:
                self._pair_cache[key] = None
        return self._pair_cache[key]

    def _asks_twin(self, spec: Spec, pair) -> bool:
        """F2: does a yes/no base ask for its minimal-edit twin? (the twin is a separate row and never changes the base)"""
        return (uhash(FAMILY, "twin", spec.sampler, spec.seed // 2) < P_TWIN_PAIR and self._twin(spec) is not None
                and self._twin(pair) is not None)

    def _twin_candidates(self, spec: Spec, pl) -> list:
        """(kind, slot, new slot) edits of ONE input slot of the asked commitment's story."""
        out = []
        ds = {pl.due_eff, pl.due_eff + DAY} | {e.date - DAY for e in (pl.done, pl.release, pl.retract, pl.cond,
                                                                     pl.ext_reply) if e is not None}
        for d in sorted(ds):                # F4: never for ch_due, whose status date must stay clear of its options
            if d != pl.asof and d >= pl.commit.date and spec.qform != "ch_due":
                out.append(("asof", "ASOF", S.date_slot(d)))
        if pl.done is not None:
            for d in (pl.due_eff, pl.due_eff + DAY):
                if d != pl.done.date:
                    out.append(("done_date", f"T{pl.done.i}", S.date_slot(d)))
        for e, kind in ((pl.release, "release_by"), (pl.ext_reply, "yes_by")):
            if e is None or e.sem == "chat.ext_no":
                continue
            for m in pl.members:
                if m not in (e.spk, pl.maker):
                    out.append((kind, f"S{e.i}", S.name_slot(m)))
        if spec.structure["auth"]:
            for m in pl.members:
                if m != pl.auth:
                    out.append(("auth", "AUTH", S.name_slot(m)))
        if pl.cond is not None and all(e is None for e in (pl.done, pl.release, pl.retract)):
            sem = "chat.cond_off" if pl.cond.sem == "chat.cond_met" else "chat.cond_met"
            fid = self._pick_form(sem, spec.sampler, spec.seed, pl.cond.i)
            out.append(("cond_flip", f"M{pl.cond.i}", self.lexicon.clause(fid, bind={"COND": "COND0"})))
        return out

    def _twin_pool(self, spec: Spec) -> list:
        """Every (kind, changed slot, twin spec, predicted answer, new value) minimal edit whose answer changes (the
        prediction comes from the construction table); the status-date kind is thinned (P_TWIN_ASOF)."""
        pl = self._plan(spec)
        cur = self._answer_of(spec.qform, self._plan_status(pl), pl.due_eff)
        pool = []
        for kind, name, slot in self._twin_candidates(spec, pl):
            twin = spec.with_slot(name, slot)
            pl2 = self._plan(twin)
            if not self._plan_ok(pl2):
                continue
            pred = self._answer_of(spec.qform, self._plan_status(pl2), pl2.due_eff)
            if pred != cur:
                pool.append((kind, name, twin, pred, S.canonical(slot)))
        kinds = {c[0] for c in pool}
        if len(kinds) > 1 and uhash(FAMILY, "twinasof", spec.sampler, spec.seed) >= P_TWIN_ASOF:
            pool = [c for c in pool if c[0] != "asof"]
        return pool

    def _twin(self, spec: Spec):
        """A yes/no minimal-edit twin (kind first, then an edit of that kind; the prediction comes from the construction
        table). Not used with P_TWIN_PAIR 0; choice twins come from pick_choice_twins."""
        pool = self._twin_pool(spec)
        if not pool:
            return None
        kinds = sorted({c[0] for c in pool})
        kind = min(kinds, key=lambda k: uhash(FAMILY, "twinkind", spec.sampler, spec.seed, k))
        kind, name, twin, pred, _v = min((c for c in pool if c[0] == kind),
                                         key=lambda c: uhash(FAMILY, "twinpick", spec.seed, c[1], str(c[4])))
        return RelationProposal("twin", spec=twin, changed_slot=name, expect=pred, note=f"twin.{kind}")

    def _metamorphic(self, spec: Spec) -> list:
        out = []
        members = self._members(spec)
        old = members[-1]
        new = next(n for n in RESERVE_NAMES if n not in members)
        renamed = {k: (S.name_slot(new) if v.kind == "name" and v.value == old else v) for k, v in spec.slots.items()}
        out.append(RelationProposal("metamorphic", spec=spec.replace(slots=renamed), expect="same",
                                    note="rename a member everywhere"))
        week = 7 * DAY
        shifted = {k: (S.date_slot(v.value + week) if v.kind == "date" else v) for k, v in spec.slots.items()}
        exp = "same"
        if spec.qform == "ch_due":
            exp = (self._fold(spec)[1] + week).isoformat()
        out.append(RelationProposal("metamorphic", spec=spec.replace(slots=shifted), expect=exp,
                                    note="shift every date by 7 days"))
        pack = spec.pack.split(":", 1)[1]
        used = {v.value for k, v in spec.slots.items() if re.fullmatch(r"TASK\d+", k)}
        pack_tasks = self.vocab.pack_tasks(pack)
        spare = [t for t in pack_tasks if t not in used]
        if spare:
            t = S.category_slot(spare[0], self.vocab.table("tasks", pack_tasks))
            out.append(RelationProposal("metamorphic", spec=spec.replace(slots={**spec.slots, "TASK0": t, "QTASK": t}),
                                        expect="same", note="swap the asked task for an unused one"))
        return out

    # ------------------------------------------------------------------------------------------- error models
    def _latest_status(self, spec: Spec):
        """t32_latest_message: the status the last counted line on the asked task suggests by itself."""
        env = spec.env()
        pl = self._plan(spec)
        lines = [e for e in pl.evs if e.date <= env["ASOF"] and e.i >= pl.commit.i
                 and (e.args.get("TASK") == env["QTASK"] or (pl.conditional and e.args.get("COND") ==
                                                             pl.commit.args.get("COND")))]
        last = lines[-1]
        if last.sem == "chat.done":
            return "kept"
        if last.sem == "chat.release":
            return "waived"
        if last.sem == "chat.retract":
            return "broken"
        if last.sem == "chat.cond_off":
            return "not_triggered"
        due = last.args.get("NEW_DUE") or pl.due0
        return "broken" if env["ASOF"] > due else "not_yet_due"

    def _neighbours(self, spec: Spec) -> list:
        """t32_wrong_commitment: the other commitment lines, nearest to the asked one first (the later one on a tie)."""
        evs = self._events(spec)
        i0 = next(e.i for e in evs if e.c == 0 and e.role == "commit")
        cands = [e for e in evs if e.role == "commit" and e.c not in (0, None)]
        return sorted(cands, key=lambda e: (abs(e.i - i0), e.i < i0))

    def error_models(self) -> dict:
        def by_flag(flag):
            def fn(spec):
                if spec.qform not in ("ch_status", "ch_due"):
                    return None
                status, due = self._fold(spec, f=frozenset((flag,)))
                return status if spec.qform == "ch_status" else due.isoformat()
            return fn

        def latest(spec):
            return self._latest_status(spec) if spec.qform == "ch_status" else None

        def wrong(spec):
            near = self._neighbours(spec) if spec.qform in ("ch_status", "ch_due") else []
            if not near:
                return None
            if spec.qform == "ch_due":                      # the date the neighbouring commitment states
                return near[0].args["DUE"].isoformat()
            for e in near:                                  # its status (first one made by the status date)
                try:
                    return self._fold(spec, who=e.spk, task=e.args["TASK"])[0]
                except ContractError:
                    continue
            return None

        out = {n: error_model(n, by_flag(fl)) for n, (fl, _d) in FLAG_MODELS.items()}
        out["t32_latest_message"] = error_model("t32_latest_message", latest)
        out["t32_wrong_commitment"] = error_model("t32_wrong_commitment", wrong)
        return out
