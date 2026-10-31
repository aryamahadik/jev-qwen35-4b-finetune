"""families/T25/plugin.py: T25 "source reliability conflict with tie-abstain" (C2_DATA_SPEC 2.1 T25, 3.17;
G0_SPEC.md frozen, sha below).

A bundle of 3-5 sources about one attribute (a fee, a deadline, an allowance ...): each source has a stated tier (three
names ranked on the card), a date, an origin (independent, or copied from another listed source) and the value it
states. Copies are ignored; among the independent sources the most reliable tier wins, then the most recent date; a
top group (same tier, same date) that disagrees makes the attribute "not determinable from reliable sources" (G0 S1-S6).

  solver A   rule engine: the rule "t outranks s" as a kit rule AST (rules.Or / And / Cmp over tier ranks and dates),
             run by rules.evaluate on every ordered pair of independent sources; the top group is the set no source
             outranks, then the agreement step                                                  paradigm rule_engine
  solver B   solver_b.py: its own parser of the rendered row; the independent sources sorted by (tier rank, newest
             date) and grouped with itertools.groupby; the head group decides                   paradigm sort_group
  construct  _top_c: a third, construction-only reading (a plain max over the plan). It steers the samplers, tags the
             traps and lets twins predict their answer from the edit; it never sets a gold, and a guard refuses any
             spec where it and solver A disagree
  samplers   S1 forward (list); S2 near-miss gaps (list); S3 source table first (table); S4 narrative over pasted
             excerpts (excerpt); S5 held out (keyed records, held-out skins and registers; mixdev only)
  questions  ch_value, ch_source (open sets; the abstain option is shown by a label-blind plan, gold on 1 / k of the rows
             that show it); yn_claim (+ wrong / not / other complements), yn_claim_dneg (double negation)
  relations  complement, minimal-edit twin, equiv (another skin; half also another layout), inv, G4 metamorphic
  card       G0 v4 1.1: yes/no rows print the rules once as row.card, choice rows keep them at the head of the instructions
             (c2_kit.cards.place_rules); solver B reads both through cards.split_rules
Pools below (attribute packs, tier schemes, organisations, askers, source names) are Claude-written stand-ins until the
Haiku packs exist (after A38); they live in code and nothing here writes a file.
"""
from __future__ import annotations

import collections
import dataclasses
import datetime as dt
import math
import random
import re
import sys
from dataclasses import dataclass
from pathlib import Path

_C2_BUILD = Path(__file__).resolve().parents[2]
if str(_C2_BUILD) not in sys.path:
    sys.path.insert(0, str(_C2_BUILD))

from c2_kit import cards as KC  # noqa: E402
from c2_kit import choiceplan as CP  # noqa: E402
from c2_kit import polarity as POL  # noqa: E402
from c2_kit import rules as RL  # noqa: E402
from c2_kit import skin as K  # noqa: E402
from c2_kit import slots as S  # noqa: E402
from c2_kit.distractors import build_options, error_model, register_name, uhash  # noqa: E402
from c2_kit.plugin import C2Plugin, ContractError, QuestionForm, RelationProposal, Spec, choose_forms  # noqa: E402
from c2_kit.rows import TextBuilder, assemble_row  # noqa: E402

HERE = Path(__file__).resolve().parent
FAMILY = "T25"
DAY = dt.timedelta(days=1)
MAX_TRIES = 400
FIRST_DAY = dt.date(2024, 1, 1)                 # D* = FIRST_DAY + [TOP_LO, TOP_HI] days
TOP_LO, TOP_HI = 400, 900
DATE_MIN, DATE_MAX = dt.date(2023, 1, 1), dt.date(2027, 12, 31)
VALUE_DATE_FIRST, VALUE_DATE_SPAN = dt.date(2026, 1, 5), 540     # date-valued packs
ABSTAIN = "undetermined"
ABSTAIN_TEXT = "Not determinable from reliable sources"
SOURCE_ABSTAIN_TEXT = "No source: not determinable from reliable sources"
SRC_RE = re.compile(r"S(\d+)_(ID|NAME|TIER|DATE|VALUE)")
FIELDS = ("ID", "NAME", "TIER", "DATE", "VALUE")


# ------------------------------------------------------------------------------------------------ packs (G0 7)
@dataclass(frozen=True)
class Pack:
    attr: str
    kind: str                   # cents | date | count
    unit: tuple | None
    pool: tuple                 # cents / count values (date packs draw dates)


PACKS = {
    "filing_fee": Pack("late filing fee", "cents", None, (1500, 2000, 2500, 3000, 3500, 4000, 4950)),
    "deposit": Pack("booking deposit", "cents", None, (5000, 7500, 10000, 12500, 15000, 17550)),
    "membership": Pack("monthly membership price", "cents", None, (1999, 2499, 2999, 3499, 3999, 4500)),
    "withdrawal": Pack("daily withdrawal limit", "cents", None, (20000, 25000, 30000, 40000, 50000, 60000)),
    "deadline": Pack("application deadline", "date", None, ()),
    "opening": Pack("market opening date", "date", None, ()),
    "entries": Pack("closing date for entries", "date", None, ()),
    "baggage": Pack("checked bag allowance", "count", ("kilogram", "kilograms"), (15, 20, 23, 25, 30, 32)),
    "notice": Pack("cancellation notice period", "count", ("day", "days"), (7, 10, 14, 21, 28, 30)),
    "group": Pack("maximum group size", "count", ("person", "people"), (6, 8, 10, 12, 15, 20)),
    "age": Pack("minimum age for the course", "count", ("year", "years"), (12, 14, 16, 18, 21)),
    "pickup": Pack("parcel pickup window", "count", ("hour", "hours"), (24, 48, 72, 96, 120)),
}
PACK_KEYS = tuple(PACKS)
SCHEMES = {   # G0 S2: rank 1 first
    "official": ("official", "trade", "community"),
    "metal": ("gold", "silver", "bronze"),
    "order": ("primary", "secondary", "tertiary"),
    "level": ("high", "medium", "low"),
    "colour": ("blue", "green", "grey"),
    "greek": ("alpha", "beta", "gamma"),
}
SCHEME_KEYS = tuple(SCHEMES)
TIER_KEYS = ("t1", "t2", "t3")
TIER_RANK = {"t1": 1, "t2": 2, "t3": 3}
ORGS = ("Redfern Council", "Pembroke Travel", "Halvard Bank", "Selkirk Market Trust", "Quayside Gym", "Corran Rail",
        "Mistral Art School", "Upland Water Board", "Tamsin Tours", "Veridia Clinic", "Brightwell Library",
        "Lindenfeld Club")
ASKERS = ("Priya Raman", "Tomas Lindqvist", "Ana Ruiz", "Dana Okafor", "Lena Whitcombe", "Ravi Anand", "Mira Castell",
          "Aiko Brandt", "Jonas Feld", "Nadia Kowal", "Owen Pryce", "Sara Ilves", "Malik Osei", "Ines Duarte",
          "Kofi Mensah", "Hana Sato")
SOURCE_NAMES = ("help page", "newsletter", "price sheet", "reply email", "notice board post", "phone script",
                "printed leaflet", "partner website", "forum thread", "annual report", "press note", "staff handbook",
                "app banner", "info desk note", "social media post", "trade journal item", "radio announcement",
                "welcome pack", "chat transcript", "receipt footer")
RESERVE_ASKERS = ("Quinn Arbeloa", "Rosa Templeton")          # G4 renames only
RESERVE_ORGS = ("Wexford Mutual", "Yarrow Retail")
RESERVE_IDS = ("Z", "S-00")

# ------------------------------------------------------------------------------------------------ card text (G0 1.1)
CLOSED_WORLD = "The listed sources are complete: no other source, tier or rule applies."
CARD = (
    "How to settle the {ATTR} from the listed sources:\n"
    "- Tiers, most reliable first: {RANK_1}; then {RANK_2}; then {RANK_3}.\n"
    "- A source marked as copied from another is a copy and is ignored, whatever its tier or date; the rest are "
    "independent.\n"
    "- The most reliable tier present among the independent sources wins, then the most recent 'dated' date within it "
    "(never a date a source states). A less reliable source never wins.\n"
    "- Independent sources with that tier and date decide together: one value (or a lone source) stands; different "
    "values make the {ATTR} not determinable from reliable sources.\n"
    "- Only the listed sources count; surrounding text, notes, the claim to check and outside knowledge do not.\n"
    + CLOSED_WORLD)
CLAIM_TPL = "Claim to check: the {ATTR} is {CANDIDATE}."
HEADS = {"list": "Sources on the {ATTR}:", "table": "Source table for the {ATTR}:",
         "excerpt": "Excerpts on the {ATTR}:", "keyed": "Source records for the {ATTR}:"}
TABLE_HEAD = "source | name | tier | dated | origin | stated value"

# ------------------------------------------------------------------------------------------------ shares (G0 2-4, 6)
BASE_SHARES = (("ch_value", 0.40), ("ch_source", 0.18), ("yn_claim", 0.38), ("yn_claim_dneg", 0.04))
SCEN_SHARES = {"ch_value": (("clear", 0.62), ("tie_agree", 0.16), ("tie_disagree", 0.22)),
               "ch_source": (("clear", 0.78), ("tie_disagree", 0.22)),
               "noul": (("clear", 0.82), ("tie_agree", 0.18))}
TOP_TIER = ((1, 0.50), (2, 0.35), (3, 0.15))
RIVAL_KINDS = (("same_tier_older", 0.35), ("lower_newer", 0.40), ("lower_older", 0.25))
COPY_KINDS = (("outrank", 0.45), ("false_tie", 0.20), ("of_winner", 0.15), ("inert", 0.20))
COPY_COUNT = ((0, 0.25), (1, 0.50), (2, 0.25))
N_SOURCES = {"S1": (3, 4, 5), "S2": (4, 5), "S3": (4, 5), "S4": (3, 4), "S5": (3, 4, 5)}
LAYOUT = {"S1": "list", "S2": "list", "S3": "table", "S4": "excerpt", "S5": "keyed"}
TRAIN_LAYOUTS = ("list", "table", "excerpt")
SAMPLER_INDEX = {"S1": 0, "S2": 1, "S3": 2, "S4": 3, "S5": 4}
S4_REGISTERS = ("email", "chat", "transcript", "memo", "ticket", "faq")   # G0 2: <= 15% per register
CARDS = 7                                       # cards per sampler (G0 v4 section 2: 28 training cards + 7 S5; F3)
P_RIVAL_DIFF, P_TIE3, P_PROMOTE_COPY = 0.75, 0.15, 0.5
COMPLEMENTS = {"yn_claim": (("yn_claim_wrong", 0.4), ("yn_claim_other", 0.2), ("yn_claim_not", 0.4)),
               "yn_claim_dneg": (("yn_claim_not", 1.0),)}
P_COMPLEMENT, P_EQUIV, P_EQUIV_LAYOUT, P_INV, P_TWIN = 0.6, 0.12, 0.5, 0.05, 0.42
SHIFT = DAY * 35

QUESTION_FORMS = (
    QuestionForm("ch_value", "choice", answer_set="open", abstain=True),
    QuestionForm("ch_source", "choice", answer_set="open", abstain=True),
    QuestionForm("yn_claim", "noul", "claim_holds", 1),
    QuestionForm("yn_claim_wrong", "noul", "claim_holds", -1, "antonym"),
    QuestionForm("yn_claim_not", "noul", "claim_holds", -1, "syntactic"),
    QuestionForm("yn_claim_other", "noul", "claim_holds", -1, "implicit"),
    QuestionForm("yn_claim_dneg", "noul", "claim_holds", 1),
)
QF = {q.qform: q for q in QUESTION_FORMS}
POLARITY = {q.qform: q.polarity for q in QUESTION_FORMS}
CHOICE_FORMS = ("ch_value", "ch_source")
VALUE_K, SOURCE_K = (3,), (3, 4)     # option counts (label-blind draws; G0 S7, S8)
# Display plan of a choice row (G0 v4 S7, S8; c2_kit.choiceplan), drawn from the row key BEFORE any structure: k counts the
# abstain option when it is shown; SHOW_RATE is the probability that the abstain option is shown; shown rows have the
# abstain option gold on 1 / k of them (the kit's default share), so SHOW_RATE = a * k puts it gold on a = 22% of all
# choice rows (spec 3.17: 15-25%) whatever k is. The abstain text is the longest option, so a "never take the longest
# option" rule gains nothing: gold-is-longest is 1 / k (pilot F1: it was 22% against 1 / k = 33%).
ABSTAIN_GOLD = 0.22
PLAN_BLOCK = 1024                    # seeds per balancing block (a pure function of the seed: blocks never move)
SHOW_RATE = {(q, k): round(ABSTAIN_GOLD * k, 4) for q, ks in (("ch_value", VALUE_K), ("ch_source", SOURCE_K)) for k in ks}
CLAIM_FORMS = tuple(q.qform for q in QUESTION_FORMS if q.qtype == "noul")

# Negative / antonym predicates of "the claim holds" (c2_kit.polarity rules P1-P3; G0 v4 section 7): the antonyms of
# "correct" and the words that say the claim and the settled value differ. A yes/no wording negates a positive predicate
# syntactically ("does not match") or uses one of these, never both, and its layers must give its form's polarity.
NEGATIVE_PREDICATES = (r"wrong", r"mistaken", r"incorrect", r"inaccurate", r"untrue", r"false", r"invalid", r"erroneous",
                       r"flawed", r"faulty", r"differs?", r"differ(?:ing|ent)", r"disagrees?", r"contradicts?",
                       r"conflicts?", r"mismatch(?:es)?", r"deviates?")

# G5-H template quarantine (spec 6.3: a template whose read rows a reader disputes on > 3% is quarantined). Pilot iteration 0
# read each of these two templates once and one of two readers disagreed (a reader error on a double negation, adjudicated
# gold_ok, PILOT_VERDICT g5h.quarantine_note): the rule fires mechanically and is not loosened. T25.ctx_for leaves them out of
# the pool, so no row of iteration 1 uses them; nothing is relabelled.
QUARANTINED_TEMPLATES = {
    "T25-SK-yaml.021": "G5-H pilot 0: read once, 1 of 2 readers disagreed (adjudicated gold_ok); spec 6.3 > 3% rule",
    "q.t25.yn_claim_dneg#90841882": "G5-H pilot 0: read once, 1 of 2 readers disagreed (adjudicated gold_ok); spec 6.3 > 3% rule",
}

# ------------------------------------------------------------------------------------------------ error models (G0 5)
_EM_TEXT = {
    "t25_newest_first": "lets the most recent independent source win and uses the tier only to break a same-date tie",
    "t25_count_copies": "counts copied sources as independent sources",
    "t25_tier_reversed": "reads the card's tier ranking backwards",
    "t25_oldest_in_tier": "lets the oldest source win inside the most reliable tier",
    "t25_tier_only": "ignores dates, so every independent source of the most reliable tier is in the top group",
    "t25_tie_first_listed": "breaks a disagreeing top group by taking the first listed member",
    "t25_tie_last_listed": "breaks a disagreeing top group by taking the last listed member",
    "t25_majority": "takes the value that the most sources state, copies counted",
    "t25_first_listed": "takes the first listed source",
    "t25_newest_any": "takes the most recent source of any tier or origin",
}
for _n, _d in _EM_TEXT.items():
    register_name(_n, _d)
VALUE_EM = tuple(_EM_TEXT)
if "t25_rank" not in RL.FNS:
    RL.register_fn("t25_rank", lambda key: TIER_RANK[key])


# ------------------------------------------------------------------------------------------------ helpers

def _draw(u: float, shares: tuple):
    acc = 0.0
    for key, share in shares:
        acc += share
        if u < acc:
            return key
    return shares[-1][0]


def _draw_norm(u: float, shares: tuple):
    """_draw over shares that need not sum to 1 (the abstain scenario is taken out of a choice form's list)."""
    tot = sum(s for _, s in shares)
    return _draw(u, tuple((k, s / tot) for k, s in shares))


def _yes_target(sampler: str, seed: int) -> bool:
    """Seeds 2k and 2k + 1 share the question form and get opposite targets (exact 50% over seed pairs; G0 4)."""
    return (uhash(FAMILY, "yes", sampler, seed // 2) < 0.5) != bool(seed % 2)


def _card(sampler: str, card: int) -> tuple:
    """(pack, tier scheme, id style) fixed by the card (G0 2)."""
    si = SAMPLER_INDEX[sampler]
    return (PACK_KEYS[(si * CARDS + card) % len(PACK_KEYS)], SCHEME_KEYS[(card + 2 * si) % len(SCHEME_KEYS)],
            ("letters", "codes")[(card + si) % 2])


def _tier_slot(scheme: str, rank: int) -> S.Slot:
    names = SCHEMES[scheme]
    return S.category_slot(TIER_KEYS[rank - 1], {k: [nm] for k, nm in zip(TIER_KEYS, names)})


def _value_slot(pack: Pack, v) -> S.Slot:
    if pack.kind == "cents":
        return S.cents_slot(v)
    if pack.kind == "count":
        return S.count_slot(v, pack.unit)
    return S.date_slot(v)


def _from_canon(pack: Pack, key):
    return dt.date.fromisoformat(key) if pack.kind == "date" else key


def _gap(rng: random.Random, near: bool, zero_ok: bool) -> int:
    """Days between a rival or copy and D* (G0 2: same day, one day, one week, months, one year; S2 near misses)."""
    r = rng.random()
    if near:
        if zero_ok and r < 0.35:
            return 0
        return 1 if r < 0.85 else rng.randint(2, 7)
    if zero_ok and r < 0.30:
        return 0
    if r < 0.40:
        return 1
    if r < 0.55:
        return 7
    if r < 0.88:
        return rng.randint(2, 120)
    return 365


class T25(C2Plugin):
    FAMILY = FAMILY
    TIER = "everyday"
    G0_LITE = HERE / "G0_SPEC.md"
    G0_SHA256 = "a0013d64285ce1f19f7c7160cbaeb0f115d67613d87aea6e918fb3f98a64004a"   # frozen v4 (14 Oct; v3 8de68753..., v2 aabd110d...)
    G0_HAIKU_TASK = "c2-data-stage-a/amb:T25"     # the one Haiku ambiguity pass (39 points H1-H39; G0 section 9)
    SAMPLERS = ("S1", "S2", "S3", "S4", "S5")
    HELD_OUT_SAMPLERS = ("S5",)
    PARADIGM_A = "rule_engine"
    PARADIGM_B = "sort_group"
    SOLVER_B_MODULE = "families.T25.solver_b"
    QFORMS = QF
    VERDICT_WORDS = ("determinable", "undetermined", "indeterminable", "undeterminable", "decides", "decisive",
                     "wins", "winner", "outranks", "overrides", "ignore", "correct", "wrong", "mistaken", "reliable",
                     "unreliable", "trustworthy", "authoritative")
    FACT_WORDS = ("official", "newest", "latest", "recent", "copy", "copied", "independent", "tier")
    LABEL_WORDS = VERDICT_WORDS + FACT_WORDS   # never in a skin; record blocks state facts, never a verdict (G0 7)
    CLOSED_WORLD_SENTENCE = CLOSED_WORLD
    REGISTERS = ("memo", "email", "chat", "ticket", "json", "yaml", "faq", "transcript", "wiki_talk", "audit_note")
    HELD_OUT_REGISTERS = ("wiki_talk", "audit_note")
    GSL_EXCEPTIONS: dict = {}
    NAME_ALLOW: tuple = ()
    POLARITY_CHECK = True                 # c2_kit.polarity: yes/no wordings must read with their form's polarity (G0 v4 7)
    POLARITY_NEGATIVES = NEGATIVE_PREDICATES

    def __init__(self, lexicon=None):
        super().__init__(lexicon)
        self._ems = None
        self._screened: list = []                  # [(ctx, screened ctx, {wording id: problems})]
        self._plans: dict = {}                     # (sampler, block) -> {(seed, qform): ChoicePlan} (pure functions)

    def ctx_for(self, spec: Spec, ctx):
        """The kit context without the wordings that break the polarity rule and without the G5-H-quarantined templates
        (QUARANTINED_TEMPLATES), so neither render() nor the pipeline's complement or equiv partner can pick one (a template
        is quarantined, never a row relabelled). Cached per context object; the frozen pool loses no wording to the polarity
        rule (tests)."""
        for c, screened, _bad in self._screened:
            if c is ctx:
                return screened
        screened, bad = POL.screen(ctx, self)
        gone = [k for k in screened.skins if k in QUARANTINED_TEMPLATES]
        if gone:
            screened = dataclasses.replace(screened, skins={k: v for k, v in screened.skins.items() if k not in gone})
        self._screened.append((ctx, screened, bad))
        return screened

    def quarantined_wordings(self, ctx) -> dict:
        """{wording skin id: polarity problems} for the wordings ctx_for() leaves out of `ctx`."""
        self.ctx_for(None, ctx)
        return next(bad for c, _s, bad in self._screened if c is ctx)

    # ============================================================================================ sampling
    def sample(self, seed: int, sampler: str) -> Spec:
        if sampler not in self.SAMPLERS:
            raise ContractError(f"sampler {sampler}")
        rng = random.Random(f"{FAMILY}|{sampler}|{seed}")
        qform = _draw(uhash(FAMILY, "qform", sampler, seed // 2), BASE_SHARES)    # seed pairs share the form
        card = rng.randrange(CARDS)
        pack, scheme, ids = _card(sampler, card)
        group = "noul" if QF[qform].qtype == "noul" else qform
        # a choice row's display plan (k, abstain shown, abstain gold, position) comes from the row key before any
        # structure; the scenario then follows the plan: an abstain gold is a disagreeing tie, every other gold a
        # determinable bundle (clear, or an agreeing tie on ch_value). Yes/no rows keep the G0 section 4 draw.
        plan = self._plan(sampler, seed, qform) if group != "noul" else None
        scen = _draw(uhash(FAMILY, "scen", sampler, seed), SCEN_SHARES[group]) if plan is None else (
            "tie_disagree" if plan.gold_abstain else _draw_norm(
                uhash(FAMILY, "scen", sampler, seed), tuple((s, w) for s, w in SCEN_SHARES[group]
                                                           if s != "tie_disagree")))
        ctx = {"seed": seed, "sampler": sampler, "qform": qform, "card": card, "pack": pack, "scheme": scheme,
               "ids": ids, "scen": scen, "layout": LAYOUT[sampler],
               "yes": _yes_target(sampler, seed) if group == "noul" else None}
        if plan is not None:
            try:                     # structure is redrawn under the fixed plan (never the plan, never a label)
                return CP.realize(plan, lambda _i: self._attempt(rng, ctx), solve=self.solve_a, abstain_key=ABSTAIN,
                                  fits=lambda s, g: self._options_ok(s, strict=True), tries=MAX_TRIES)[0]
            except CP.PlanMismatch as e:
                raise ContractError(f"T25 {sampler} seed {seed}: no {scen} spec fills the plan ({e})") from None
        for _ in range(MAX_TRIES):
            spec = self._attempt(rng, ctx)
            if spec is not None:
                return spec
        raise ContractError(f"T25 {sampler} seed {seed}: no {scen} spec in {MAX_TRIES} draws")

    @staticmethod
    def _values(rng: random.Random, pack: Pack, k: int) -> list:
        if pack.kind == "date":
            offs = rng.sample(range(VALUE_DATE_SPAN), k)
            return [VALUE_DATE_FIRST + DAY * o for o in offs]
        return rng.sample(list(pack.pool), k)

    def _attempt(self, rng: random.Random, ctx: dict):
        """Plan G first (tier T*, date D*), then rivals and copies around it (G0 2), then a seeded listing order."""
        sampler, scen = ctx["sampler"], ctx["scen"]
        pack = PACKS[ctx["pack"]]
        near = sampler == "S2"
        n = rng.choice(N_SOURCES[sampler])
        c = min(_draw(rng.random(), COPY_COUNT), n - 2)
        m = n - c
        top = _draw(rng.random(), TOP_TIER)
        g = 1 if scen == "clear" else (3 if m >= 4 and rng.random() < P_TIE3 else 2)
        if g > m or (scen != "tie_disagree" and m == g):
            return None
        D = FIRST_DAY + DAY * rng.randint(TOP_LO, TOP_HI)
        vals = self._values(rng, pack, 4)
        x = vals[0]
        if scen == "tie_disagree":
            gv = [x, vals[1]] + ([rng.choice((x, vals[2]))] if g == 3 else [])
        else:
            gv = [x] * g
        ind = [{"tier": top, "date": D, "value": v, "role": "top"} for v in gv]
        for _ in range(m - g):
            kind = "same_tier_older" if top == 3 else _draw(rng.random(), RIVAL_KINDS)
            if kind == "same_tier_older":
                tier, date = top, D - DAY * max(1, _gap(rng, near, False))
            elif kind == "lower_newer":
                tier, date = rng.randint(top + 1, 3), D + DAY * max(1, _gap(rng, near, False))
            else:
                tier, date = rng.randint(top + 1, 3), D - DAY * _gap(rng, near, True)
            value = rng.choice(vals[1:]) if rng.random() < P_RIVAL_DIFF else x
            ind.append({"tier": tier, "date": date, "value": value, "role": kind})
        if len({s["value"] for s in ind}) < 2:                  # G0 S3: >= 2 distinct independent values
            next(s for s in ind if s["role"] != "top")["value"] = vals[1]
        copies = []
        for _ in range(c):
            cp = self._copy(rng, ind, top, D, x, scen, near)
            if cp is None:
                return None
            copies.append(cp)
        srcs = ind + copies
        order = list(range(len(srcs)))
        rng.shuffle(order)
        pos = {o: p for p, o in enumerate(order, start=1)}
        spec = self._build(rng, ctx, pack, srcs, order, pos)
        if spec is None:
            return None
        plan_top = sorted(pos[i] for i, s in enumerate(ind) if s["role"] == "top")
        return self._finish(spec, ctx, plan_top, x if scen != "tie_disagree" else None)

    def _copy(self, rng, ind, top, D, x, scen, near):
        """One copy of an independent source; the kind is a weighted draw, the others are seeded fallbacks."""
        first = _draw(rng.random(), COPY_KINDS)
        for kind in [first] + [k for k, _ in COPY_KINDS if k != first]:
            got = self._copy_of_kind(rng, kind, ind, top, D, x, scen, near)
            if got is not None:
                return got
        return None

    @staticmethod
    def _copy_of_kind(rng, kind, ind, top, D, x, scen, near):
        tops = [i for i, s in enumerate(ind) if s["role"] == "top"]
        other = (list(range(len(ind))) if scen == "tie_disagree"
                 else [i for i, s in enumerate(ind) if s["value"] != x])
        if kind == "of_winner":
            o = rng.choice(tops)
            return {"of": o, "tier": rng.randint(1, 3), "date": ind[o]["date"] + DAY * _gap(rng, near, True),
                    "role": kind}
        if kind == "outrank":                                    # it would decide if copies counted
            if not other:
                return None
            o = rng.choice(other)
            if top > 1 and rng.random() < P_PROMOTE_COPY:
                tier, date = rng.randint(1, top - 1), ind[o]["date"] + DAY * _gap(rng, near, True)
            else:
                tier, date = top, max(D + DAY * max(1, _gap(rng, near, False)), ind[o]["date"])
            return {"of": o, "tier": tier, "date": date, "role": kind}
        if kind == "false_tie":                                  # it would join G with another value
            cand = [i for i in other if ind[i]["date"] <= D] if scen != "tie_disagree" else []
            if not cand:
                return None
            return {"of": rng.choice(cand), "tier": top, "date": D, "role": kind}
        o = rng.randrange(len(ind))                              # inert: it could never decide
        if top < 3:
            return {"of": o, "tier": rng.randint(top + 1, 3), "date": ind[o]["date"] + DAY * _gap(rng, near, True),
                    "role": kind}
        if ind[o]["date"] > D - DAY:
            return None
        return {"of": o, "tier": 3, "date": ind[o]["date"] + DAY * rng.randint(0, (D - DAY - ind[o]["date"]).days),
                "role": kind}

    def _build(self, rng, ctx, pack, srcs, order, pos):
        n = len(srcs)
        scheme = ctx["scheme"]
        if ctx["ids"] == "letters":
            ids = [chr(ord("A") + k) for k in range(n)]
        else:
            ids = [f"S-{x}" for x in rng.sample(range(10, 100), n)]
        names = rng.sample(SOURCE_NAMES, n)
        slots = {"ASKER": S.name_slot(rng.choice(ASKERS)), "ORG": S.name_slot(rng.choice(ORGS)),
                 "ATTR": S.name_slot(pack.attr)}
        for r in (1, 2, 3):
            slots[f"RANK_{r}"] = _tier_slot(scheme, r)
        copy_of = []
        for p, o in enumerate(order, start=1):
            s = srcs[o]
            slots[f"S{p}_ID"] = S.id_slot(ids[p - 1])
            slots[f"S{p}_NAME"] = S.name_slot(names[p - 1])
            slots[f"S{p}_TIER"] = _tier_slot(scheme, s["tier"])
            slots[f"S{p}_DATE"] = S.date_slot(s["date"])
            if "of" in s:
                copy_of.append(pos[s["of"]])
            else:
                copy_of.append(None)
                slots[f"S{p}_VALUE"] = _value_slot(pack, s["value"])
        structure = {"pack": ctx["pack"], "kind": pack.kind, "scheme": scheme, "layout": ctx["layout"], "n": n,
                     "copy_of": copy_of}
        spec = Spec(FAMILY, ctx["sampler"], ctx["seed"], f"{FAMILY}:{ctx['sampler']}:c{ctx['card']:02d}",
                    ctx["qform"], slots, structure=structure, pack=f"t25:{ctx['pack']}")
        spec = self.derive(spec)
        return spec if self._valid(spec) else None

    def _finish(self, spec: Spec, ctx: dict, plan_top: list, x):
        """CANDIDATE (yes/no), the construction-vs-solver-A guard, depth and tags."""
        if self._top_c(spec)[2] != plan_top:
            raise ContractError(f"T25 seed {spec.seed}: the plan and the construction reading disagree")
        out = self._outcome(spec)
        want = ("undetermined", None) if x is None else ("value", S.canonical(_value_slot(PACKS[spec.structure["pack"]],
                                                                                          x)))
        if out is None or out[:2] != want or out[2] != plan_top:
            raise ContractError(f"T25 seed {spec.seed}: construction and solver A disagree ({out} vs {want})")
        if ctx["yes"] is not None:
            cand = out[1] if ctx["yes"] else self._wrong_value(spec, out[1])
            if cand is None:
                return None
            pack = PACKS[spec.structure["pack"]]
            spec = spec.replace(slots={**spec.slots, "CANDIDATE": _value_slot(pack, _from_canon(pack, cand))})
        st = spec.structure
        deep = st["n"] == 5 and sum(c is not None for c in st["copy_of"]) == 2 and len(plan_top) >= 2
        spec = spec.replace(depth=2, deep=deep)
        spec = spec.replace(tags=self._tags(spec, ctx["scen"]))
        if self.solve_a(spec) is None:
            raise ContractError("T25: solver A gives no answer (never generated)")
        return spec

    def _wrong_value(self, spec: Spec, gold):
        """yes/no 'no' rows: the value of the first error model (seeded order) that gives another value (G0 S11)."""
        for name in sorted(VALUE_EM, key=lambda m: uhash(FAMILY, "cand", spec.sampler, spec.seed, m)):
            out = self._outcome(spec, frozenset({name}))
            if out is not None and out[0] == "value" and out[1] != gold:
                return out[1]
        return None

    def _tags(self, spec: Spec, scen: str) -> tuple:
        st, v = spec.structure, spec.env()
        T, D, G = self._top_c(spec)
        gold = self._outcome(spec)[:2]
        tags = {scen, f"top_t{T}"}

        def err(m):
            o = self._outcome(spec, frozenset({m}))
            return None if o is None else o[:2]
        if err("t25_newest_first") not in (None, gold):
            tags.add("newest_loses")
        cc = err("t25_count_copies")
        if cc != gold:
            tags.add("copy_trap")
            if gold[0] == "value" and cc == ("undetermined", None):
                tags.add("false_tie")
        if err("t25_majority") not in (None, gold):
            tags.add("majority_wrong")
        if err("t25_first_listed") != gold:
            tags.add("first_listed_wrong")
        if gold[0] == "value" and err("t25_tier_only") == ("undetermined", None):
            tags.add("date_separates")
        co = st["copy_of"]
        ind = [i for i in range(1, st["n"] + 1) if co[i - 1] is None]
        rank = {i: TIER_RANK[v[f"S{i}_TIER"]] for i in range(1, st["n"] + 1)}
        if any(rank[i] > T and v[f"S{i}_DATE"] == D for i in ind):
            tags.add("same_day_tiers")
        if (any(rank[i] == T and v[f"S{i}_DATE"] == D - DAY for i in ind)
                or any(rank[i] > T and v[f"S{i}_DATE"] == D + DAY for i in ind)
                or any(co[i - 1] is not None and v[f"S{i}_DATE"] in (D, D + DAY) for i in range(1, st["n"] + 1))):
            tags.add("near_miss")
        if spec.deep:
            tags.add("deep")
        return tuple(sorted(tags))

    # ============================================================================================ derive / validity
    def derive(self, spec: Spec) -> Spec:
        """A copy states its original's value (G0 S3): its value slot is derived from the original's."""
        derived, deps = {}, {}
        for i, j in enumerate(spec.structure["copy_of"], start=1):
            if j is not None:
                derived[f"S{i}_VALUE"] = spec.slots[f"S{j}_VALUE"]
                deps[f"S{i}_VALUE"] = (f"S{j}_VALUE",)
        return spec.replace(derived=derived, derived_deps=deps)

    def _valid(self, spec: Spec) -> bool:
        """The bundle invariants of G0 S3 and S11 (samplers, twins and G4 transforms keep them)."""
        st = spec.structure
        n, co = st["n"], st["copy_of"]
        a = {**spec.slots, **self.derive(spec).derived}
        ids = [a[f"S{i}_ID"].value for i in range(1, n + 1)]
        names = [a[f"S{i}_NAME"].value for i in range(1, n + 1)]
        if len(set(ids)) != n or len(set(names)) != n:
            return False
        dates = {i: a[f"S{i}_DATE"].value for i in range(1, n + 1)}
        if any(not DATE_MIN <= d <= DATE_MAX for d in dates.values()):
            return False
        ind = [i for i in range(1, n + 1) if co[i - 1] is None]
        for i, j in enumerate(co, start=1):
            if j is not None and (co[j - 1] is not None or dates[i] < dates[j]):
                return False
        stated = {S.canonical(a[f"S{i}_VALUE"]) for i in range(1, n + 1)}
        if "CANDIDATE" in a and S.canonical(a["CANDIDATE"]) not in stated:
            return False                                         # G0 S11: the claim names a stated value
        return len(ind) >= 2 and len({S.canonical(a[f"S{i}_VALUE"]) for i in ind}) >= 2

    # ============================================================================================ solver A
    def _outranks(self, t: int, s: int, mods: frozenset):
        """Rule AST "source t outranks source s" (G0 S4, S12); an error model swaps one rule."""
        rt, rs = RL.Fn("t25_rank", (RL.Ref(f"S{t}_TIER"),)), RL.Fn("t25_rank", (RL.Ref(f"S{s}_TIER"),))
        tier_better = RL.Cmp(">" if "t25_tier_reversed" in mods else "<", rt, rs)
        dt_, ds = RL.Ref(f"S{t}_DATE"), RL.Ref(f"S{s}_DATE")
        if "t25_tier_only" in mods:
            return tier_better
        if "t25_newest_first" in mods:
            return RL.Or((RL.Cmp(">", dt_, ds), RL.And((RL.Cmp("==", dt_, ds), tier_better))))
        newer = RL.Cmp("<" if "t25_oldest_in_tier" in mods else ">", dt_, ds)
        return RL.Or((tier_better, RL.And((RL.Cmp("==", rt, rs), newer))))

    def _outcome(self, spec: Spec, mods: frozenset = frozenset()):
        """Solver A (mods empty) and the error models: ("value", canonical value, top positions),
        ("undetermined", None, top positions), or None when the reading gives no single answer."""
        st, env, a = spec.structure, spec.env(), spec.all_slots()
        n = st["n"]
        val = {i: S.canonical(a[f"S{i}_VALUE"]) for i in range(1, n + 1)}
        if "t25_first_listed" in mods:
            return ("value", val[1], [1])
        if "t25_majority" in mods:
            counts = collections.Counter(val.values())
            best = max(counts.values())
            top_vals = [x for x, k in counts.items() if k == best]
            if len(top_vals) != 1:
                return None
            return ("value", top_vals[0], [i for i in range(1, n + 1) if val[i] == top_vals[0]])
        if "t25_newest_any" in mods:
            last = max(env[f"S{i}_DATE"] for i in range(1, n + 1))
            top = [i for i in range(1, n + 1) if env[f"S{i}_DATE"] == last]
            vs = {val[i] for i in top}
            return ("value", val[top[0]], top) if len(vs) == 1 else None
        elig = [i for i in range(1, n + 1) if "t25_count_copies" in mods or st["copy_of"][i - 1] is None]
        top = [s for s in elig
               if RL.evaluate(RL.Not(RL.Or(tuple(self._outranks(t, s, mods) for t in elig if t != s))), env)]
        if not top:
            raise ContractError("T25: the outranks rule left no top source")
        if len({val[i] for i in top}) > 1:
            if "t25_tie_first_listed" in mods:
                top = [min(top)]
            elif "t25_tie_last_listed" in mods:
                top = [max(top)]
            else:
                return ("undetermined", None, top)
        return ("value", val[top[0]], top)

    def _answer(self, spec: Spec, qform: str, mods: frozenset = frozenset()):
        out = self._outcome(spec, mods)
        if out is None:
            return None
        kind, v, top = out
        if qform == "ch_value":
            return ABSTAIN if kind == "undetermined" else v
        if qform == "ch_source":
            if kind == "undetermined":
                return ABSTAIN
            return spec.env()[f"S{top[0]}_ID"] if len(top) == 1 else None
        if kind == "undetermined":
            return None
        ok = RL.evaluate(RL.Cmp("==", RL.Lit(v), RL.Lit(S.canonical(spec.slots["CANDIDATE"]))), {})
        return int(ok if POLARITY[qform] == 1 else not ok)

    def solve_a(self, spec: Spec):
        ans = self._answer(spec, spec.qform)
        if ans is None:
            raise ContractError(f"T25: {spec.qform} has no answer on this bundle (never generated)")
        return ans

    # ============================================================================================ construction
    def _top_c(self, spec: Spec) -> tuple:
        """Construction-only reading (T*, D*, G positions): a plain max over the independent sources. It tags traps and
        lets twins predict the answer of an edit; it never sets a gold."""
        v, st = spec.env(), spec.structure
        ind = [i for i in range(1, st["n"] + 1) if st["copy_of"][i - 1] is None]
        T = min(TIER_RANK[v[f"S{i}_TIER"]] for i in ind)
        D = max(v[f"S{i}_DATE"] for i in ind if TIER_RANK[v[f"S{i}_TIER"]] == T)
        return T, D, [i for i in ind if TIER_RANK[v[f"S{i}_TIER"]] == T and v[f"S{i}_DATE"] == D]

    def _group_answer(self, spec: Spec, grp: list):
        """The answer of a known top group G' (G0 S4, S7-S10), read from the slots of `spec` (twin predictions)."""
        a = spec.all_slots()
        vals = []
        for i in grp:
            cv = S.canonical(a[f"S{i}_VALUE"])
            if cv not in vals:
                vals.append(cv)
        q = spec.qform
        if q == "ch_value":
            return vals[0] if len(vals) == 1 else ABSTAIN
        if q == "ch_source":
            if len(grp) == 1:
                return a[f"S{grp[0]}_ID"].value
            return ABSTAIN if len(vals) > 1 else None
        if len(vals) != 1:
            return None
        same = vals[0] == S.canonical(a["CANDIDATE"])
        return int(same if POLARITY[q] == 1 else not same)

    # ============================================================================================ facts (G3)
    def canonical(self, spec: Spec) -> dict:
        a, st = spec.all_slots(), spec.structure
        co = st["copy_of"]
        sources = [{"id": a[f"S{i}_ID"].value, "name": a[f"S{i}_NAME"].value, "tier": TIER_RANK[a[f"S{i}_TIER"].value],
                    "date": S.canonical(a[f"S{i}_DATE"]),
                    "copy_of": a[f"S{co[i - 1]}_ID"].value if co[i - 1] is not None else None,
                    "value": S.canonical(a[f"S{i}_VALUE"])} for i in range(1, st["n"] + 1)]
        return {"qform": spec.qform, "attr": a["ATTR"].value, "tiers": [S.render(a[f"RANK_{r}"]) for r in (1, 2, 3)],
                "sources": sources, "claim": S.canonical(a["CANDIDATE"]) if "CANDIDATE" in a else None,
                "asker": a["ASKER"].value, "org": a["ORG"].value}

    def canonical_for(self, spec: Spec, author_mode: str) -> dict:
        c = self.canonical(spec)
        return c if author_mode == "T" else {k: v for k, v in c.items() if k not in ("asker", "org")}

    def extract_view(self, spec: Spec) -> dict:
        c = self.canonical(spec)
        return {"asker": c["asker"], "org": c["org"], "attr": c["attr"]}

    def extract_fields(self, spec: Spec) -> list:
        from c2_kit.g3h import Field
        return [Field("asker", "name", "the person asking, as written"),
                Field("org", "name", "the organisation the question is about, as written"),
                Field("attr", "str", "the attribute being looked up, as written")]

    # ============================================================================================ render
    def _row_key(self, spec: Spec) -> str:
        return f"{spec.family}|{spec.seed}|{spec.sampler}|{spec.qform}"

    def block_template(self, spec: Spec) -> str:
        """The program-written source block as a slot template (G0 1.2)."""
        st = spec.structure
        n, lay, co = st["n"], st["layout"], st["copy_of"]
        lines = [HEADS[lay]]
        if lay == "table":
            lines.append(TABLE_HEAD)
        for i in range(1, n + 1):
            j = co[i - 1]
            if lay == "list":
                origin = "independent" if j is None else f"copied from Source {{S{j}_ID}}"
                lines.append(f"- Source {{S{i}_ID}}: {{S{i}_NAME}}; tier {{S{i}_TIER}}; dated {{S{i}_DATE}}; {origin}. "
                             f"It states the {{ATTR}} is {{S{i}_VALUE}}.")
                continue
            origin = "independent" if j is None else f"copied from {{S{j}_ID}}"
            if lay == "table":
                lines.append(f"{{S{i}_ID}} | {{S{i}_NAME}} | {{S{i}_TIER}} | {{S{i}_DATE}} | {origin} | {{S{i}_VALUE}}")
            elif lay == "excerpt":
                lines.append(f"[{{S{i}_ID}}] {{S{i}_NAME}}, tier {{S{i}_TIER}}, dated {{S{i}_DATE}}, {origin}: "
                             f"\"The {{ATTR}} is {{S{i}_VALUE}}.\"")
            else:
                lines += [f"source {{S{i}_ID}}", f"  name: {{S{i}_NAME}}", f"  tier: {{S{i}_TIER}}",
                          f"  dated: {{S{i}_DATE}}", f"  origin: {origin}", f"  states: {{S{i}_VALUE}}"]
        return "\n".join(lines)

    @staticmethod
    def _uniform_forms(spec: Spec, forms: dict) -> dict:
        """One number form per kind in a row (every value and the claim read alike): every count / cents slot takes
        the form of the first such slot by name, words -> digits and whole -> symbol (valid for every value). A
        function of the incoming forms only, so partners and twins that reuse a row's forms keep them."""
        out = dict(forms)
        for kind, swap in (("count", {"words": "digits"}), ("cents", {"whole": "symbol"})):
            names = sorted(k for k, s in spec.all_slots().items() if s.kind == kind and k in out)
            if names:
                f = swap.get(out[names[0]], out[names[0]])
                out.update({k: f for k in names})
        return out

    def _pick_skin(self, ctx, spec: Spec, key: str, held: bool):
        if spec.sampler == "S4":
            reg = S4_REGISTERS[int(uhash(key, "register") * len(S4_REGISTERS))]
            try:
                return ctx.pick(FAMILY, "skin", key, register=reg, held_out=held)
            except LookupError:
                pass
        return ctx.pick(FAMILY, "skin", key, held_out=held)

    def _value_text(self, spec: Spec, forms: dict):
        pack = PACKS[spec.structure["pack"]]
        form = forms["S1_VALUE"]

        def text(key):
            return S.render(_value_slot(pack, _from_canon(pack, key)), form)
        return text

    @staticmethod
    def _source_text(key) -> str:
        return f"Source {key}"

    def render(self, spec: Spec, ctx, *, skin=None, wording=None, forms=None, attack=None):
        key = self._row_key(spec)
        held = spec.sampler in self.HELD_OUT_SAMPLERS
        ctx = self.ctx_for(spec, ctx)                  # never pick a wording that breaks the polarity rule
        skin = skin or self._pick_skin(ctx, spec, key, held)
        wording = wording or ctx.pick(FAMILY, "wording", key, qform=spec.qform)
        if wording.qform != spec.qform:
            raise ContractError(f"wording {wording.skin_id} asks {wording.qform}, spec asks {spec.qform}")
        forms = self._uniform_forms(spec, forms or choose_forms(spec, key))
        slots = spec.all_slots()
        tb = TextBuilder()
        tb.add("state", skin.fill(slots, forms), skin_id=skin.skin_id)
        tb.add("state", "\n\n").add("state", K.fill(self.block_template(spec), slots, forms))
        if "CANDIDATE" in slots:
            tb.add("state", "\n\n").add("state", K.fill(CLAIM_TPL, slots, forms))
        if attack is not None:
            tb.add("state", "\n\n").add("state", attack.fill(slots, forms), skin_id=attack.skin_id)
        # the rules print once as the card on yes/no rows and at the head of the instructions on choice rows, the only
        # place a choice row prints them (c2_kit.cards.place_rules; G0 v4 1.1)
        placed = KC.place_rules(tb, K.fill(CARD, slots, forms), self.QFORMS[spec.qform].qtype)
        tb.add("instructions", wording.fill(slots, forms), skin_id=wording.skin_id)
        ans = self.solve_a(spec)
        os_ = None
        if spec.qform in CHOICE_FORMS:
            os_ = self._option_set(spec, forms, ans)
            if os_ is None:
                raise K.RenderError("too few distinct error-model answers for the planned option count")
        return assemble_row(self, spec, tb, answer=ans, option_set=os_, skin=skin, wording=wording, forms=forms,
                            attack=attack, defs_style=KC.defs_style(placed, "full"))

    @staticmethod
    def _qform_of(sampler: str, seed: int) -> str:
        return _draw(uhash(FAMILY, "qform", sampler, seed // 2), BASE_SHARES)

    @staticmethod
    def _plan_raw(sampler: str, seed: int, qform: str):
        """The kit's hash plan of one choice row: k (the abstain option counted when shown), whether it is shown, whether
        it is the gold (1 / k of the shown rows) and the gold position, all functions of the row key alone."""
        key = f"{FAMILY}|{seed}|{sampler}|{qform}"
        ks = VALUE_K if qform == "ch_value" else SOURCE_K
        k = ks[min(len(ks) - 1, int(uhash(key, "k") * len(ks)))]
        return CP.plan_choice(key, ks=(k,), abstain=True, show_rate=SHOW_RATE[(qform, k)])

    def _plan(self, sampler: str, seed: int, qform: str):
        """The display plan of a choice row (c2_kit.choiceplan), drawn before any structure and label-blind: k, whether
        the abstain option is shown, whether it is the gold, and the gold position. The kit's hash draws fix k and the
        display. The abstain gold (1 / k of every (k, shown) cell) and the gold position (uniform per k) are balanced
        along the seeds of each PLAN_BLOCK block that share the sampler and the question form: the cell's members, in
        seed order, are cut into consecutive groups of k, and every group holds exactly one abstain gold and every
        position once, in an order drawn from hashes. Every run of consecutive seeds (a pilot) is then balanced to
        within one row per cell, not only in expectation, so a 1,000-row pilot does not fail G10 by luck.
        Nothing here reads a structure or a gold."""
        blk = seed // PLAN_BLOCK
        hit = self._plans.get((sampler, blk))
        if hit is None:
            hit = {}
            seeds = {}
            for s in range(blk * PLAN_BLOCK, (blk + 1) * PLAN_BLOCK):
                q = self._qform_of(sampler, s)
                if q in CHOICE_FORMS:
                    seeds.setdefault(q, []).append(s)
            for q, ss in seeds.items():
                raw = {s: self._plan_raw(sampler, s, q) for s in ss}
                n_abs, n_pos = collections.Counter(), collections.Counter()
                for s in ss:                                  # seed order
                    r = raw[s]
                    a = False
                    if r.show_abstain:
                        m = n_abs[r.k]
                        n_abs[r.k] += 1
                        a = m % r.k == min(r.k - 1, int(uhash(FAMILY, "abs_slot", sampler, q, r.k, blk, m // r.k) * r.k))
                    m = n_pos[r.k]
                    n_pos[r.k] += 1
                    perm = sorted(range(r.k), key=lambda i, g=m // r.k, k=r.k: (
                        uhash(FAMILY, "pos_perm", sampler, q, k, blk, g, i), i))
                    hit[(s, q)] = dataclasses.replace(r, gold_abstain=a, pos=perm[m % r.k],
                                                      rank=None if a else r.rank)
            if len(self._plans) > 512:
                self._plans.clear()
            self._plans[(sampler, blk)] = hit
        got = hit.get((seed, qform))
        return got if got is not None else self._plan_raw(sampler, seed, qform)   # a hand-built spec off the sampler's draw

    def _option_set(self, spec: Spec, forms: dict, ans, strict: bool = False):
        """The planned option set. k, the abstain display and the gold position come from the plan; partner rows (twins,
        G4 variants) adapt the plan to their own gold (strict False: choiceplan.for_gold), a base row must agree with
        it (strict True: PlanMismatch). None when the error models cannot fill the plan: the spec is resampled
        (sample) or the twin is not proposed (relations), never re-tried with a smaller k (a tie leaves more distinct
        wrong values than a clear winner, so a k lowered on failure carried the label)."""
        key = self._row_key(spec)
        if spec.qform == "ch_value":
            show, ab = self._value_text(spec, forms), (ABSTAIN, ABSTAIN_TEXT)
        else:
            show, ab = self._source_text, (ABSTAIN, SOURCE_ABSTAIN_TEXT)
        return build_options(spec, ans, self.error_models(), row_key=key, render_key=show, abstain=ab,
                             plan=self._plan(spec.sampler, spec.seed, spec.qform), strict_plan=strict)

    def _options_ok(self, spec: Spec, strict: bool = False) -> bool:
        if spec.qform not in CHOICE_FORMS:
            return True
        forms = self._uniform_forms(spec, choose_forms(spec, self._row_key(spec)))
        try:
            return self._option_set(spec, forms, self.solve_a(spec), strict) is not None
        except CP.PlanMismatch:
            return False

    # ============================================================================================ relations
    def relations(self, spec: Spec) -> list:
        out = []
        key = self._row_key(spec)
        comp = COMPLEMENTS.get(spec.qform)
        if comp and uhash(FAMILY, "comp", key) < P_COMPLEMENT:
            out.append(RelationProposal("complement", qform=_draw(uhash(FAMILY, "ckind", key), comp)))
        u = uhash(FAMILY, "extra", key)
        if u < P_EQUIV:
            lay = spec.structure["layout"]
            if uhash(FAMILY, "eqlayout", key) < P_EQUIV_LAYOUT:
                others = [x for x in TRAIN_LAYOUTS if x != lay]
                new = others[int(uhash(FAMILY, "eqwhich", key) * len(others))]
                out.append(RelationProposal("equiv", spec=spec.replace(structure={**spec.structure, "layout": new}),
                                            note=f"layout {lay} -> {new}"))
            else:
                out.append(RelationProposal("equiv"))
        elif u < P_EQUIV + P_INV:
            out.append(RelationProposal("inv"))
        if uhash(FAMILY, "twin", key) < P_TWIN:
            t = self._twin(spec)
            if t is not None and self._options_ok(self.derive(t.spec)):
                out.append(t)                                    # a twin adapts the plan to its own gold (for_gold)
        return out + [m for m in self._metamorphic(spec) if self._options_ok(self.derive(m.spec))]

    def _member_values(self, spec: Spec, i: int) -> list:
        """Other values a member of G may state in a member_value twin: bundle values, the claim, pack values."""
        a, st = spec.all_slots(), spec.structure
        pack = PACKS[st["pack"]]
        cur = S.canonical(a[f"S{i}_VALUE"])
        seen = [S.canonical(a[f"S{k}_VALUE"]) for k in range(1, st["n"] + 1)]
        if "CANDIDATE" in a:
            seen.append(S.canonical(a["CANDIDATE"]))
        extra = ([x.isoformat() for x in (VALUE_DATE_FIRST, VALUE_DATE_FIRST + DAY * 200)] if pack.kind == "date"
                 else list(pack.pool[:2]))
        out = []
        for x in seen + extra:
            if x != cur and x not in out:
                out.append(x)
        return [_value_slot(pack, _from_canon(pack, x)) for x in out]

    def _twin(self, spec: Spec):
        """One input slot moves; the answer of the edited bundle is read from the group the edit designs (G0 6), never
        from solver A; the twin is kept only when the answer flips and the bundle keeps G0 S3."""
        T, D, G = self._top_c(spec)
        v, st = spec.env(), spec.structure
        co, scheme = st["copy_of"], st["scheme"]
        base = self._group_answer(spec, G)
        ind = [i for i in range(1, st["n"] + 1) if co[i - 1] is None]
        cands = []
        for r in ind:
            if r in G:
                continue
            rank, rd = TIER_RANK[v[f"S{r}_TIER"]], v[f"S{r}_DATE"]
            if rank == T:
                cands.append(("rival_newer", f"S{r}_DATE", S.date_slot(D + DAY), [r]))
                cands.append(("rival_tie", f"S{r}_DATE", S.date_slot(D), G + [r]))
            elif rd > D:
                cands.append(("rival_promote", f"S{r}_TIER", _tier_slot(scheme, T), [r]))
            elif rd == D:
                cands.append(("rival_tie_promote", f"S{r}_TIER", _tier_slot(scheme, T), G + [r]))
        if len(G) >= 2:
            for g in G:
                rest = [x for x in G if x != g]
                cands.append(("member_back", f"S{g}_DATE", S.date_slot(D - DAY), rest))
                cands.append(("member_forward", f"S{g}_DATE", S.date_slot(D + DAY), [g]))
                if T < 3:
                    cands.append(("member_demote", f"S{g}_TIER", _tier_slot(scheme, T + 1), rest))
        for g in G:
            cands += [("member_value", f"S{g}_VALUE", y, list(G)) for y in self._member_values(spec, g)]
        cands.sort(key=lambda c: uhash(FAMILY, "twinop", spec.sampler, spec.seed, c[0], c[1], S.canonical(c[2])))
        if "CANDIDATE" in spec.slots:                            # last resort: the claim names another value
            pack = PACKS[st["pack"]]
            vals = sorted({S.canonical(spec.all_slots()[f"S{i}_VALUE"]) for i in ind}, key=repr)
            cands += [("claim", "CANDIDATE", _value_slot(pack, _from_canon(pack, x)), list(G)) for x in vals]
        for note, slot, new, grp in cands:
            if S.canonical(new) == S.canonical(spec.slots[slot]):
                continue
            twin = spec.with_slot(slot, new)
            if not self._valid(twin):
                continue
            twin = self.derive(twin)
            exp = self._group_answer(twin, sorted(grp))
            if exp is None or exp == base:
                continue
            return RelationProposal("twin", spec=twin, changed_slot=slot, expect=exp, note=note)
        return None

    def _reindex(self, spec: Spec, keep: list) -> Spec:
        """The same bundle with the sources at old positions `keep`, in that order (G4: reverse, drop a copy)."""
        st = spec.structure
        pos = {o: k for k, o in enumerate(keep, start=1)}
        slots = {k: s for k, s in spec.slots.items() if not SRC_RE.fullmatch(k)}
        for o in keep:
            for f in FIELDS:
                if f"S{o}_{f}" in spec.slots:
                    slots[f"S{pos[o]}_{f}"] = spec.slots[f"S{o}_{f}"]
        co = [pos[st["copy_of"][o - 1]] if st["copy_of"][o - 1] is not None else None for o in keep]
        return self.derive(spec.replace(slots=slots, structure={**st, "n": len(keep), "copy_of": co}))

    def _metamorphic(self, spec: Spec) -> list:
        """G4 (checked, never emitted): renames, a common date shift, another tier scheme, another listing order,
        a dropped copy and a renamed deciding source leave the answer as predicted."""
        v, st = spec.env(), spec.structure
        n, co = st["n"], st["copy_of"]
        out = []
        who = next(x for x in RESERVE_ASKERS if x != v["ASKER"])
        out.append(RelationProposal("metamorphic", spec=spec.with_slot("ASKER", S.name_slot(who)), expect="same",
                                    note="rename the asker"))
        org = next(x for x in RESERVE_ORGS if x != v["ORG"])
        out.append(RelationProposal("metamorphic", spec=spec.with_slot("ORG", S.name_slot(org)), expect="same",
                                    note="rename the organisation"))
        moved = {f"S{i}_DATE": S.date_slot(v[f"S{i}_DATE"] + SHIFT) for i in range(1, n + 1)}
        shifted = spec.replace(slots={**spec.slots, **moved})
        if self._valid(shifted):
            out.append(RelationProposal("metamorphic", spec=shifted, expect="same",
                                        note="shift every source date by 35 days"))
        other = SCHEME_KEYS[(SCHEME_KEYS.index(st["scheme"]) + 1) % len(SCHEME_KEYS)]
        tiers = {f"S{i}_TIER": _tier_slot(other, TIER_RANK[v[f"S{i}_TIER"]]) for i in range(1, n + 1)}
        tiers.update({f"RANK_{r}": _tier_slot(other, r) for r in (1, 2, 3)})
        out.append(RelationProposal("metamorphic", spec=spec.replace(slots={**spec.slots, **tiers},
                                                                     structure={**st, "scheme": other}),
                                    expect="same", note="another tier scheme, same order"))
        out.append(RelationProposal("metamorphic", spec=self._reindex(spec, list(range(n, 0, -1))), expect="same",
                                    note="reverse the listing order"))
        drop = [i for i in range(1, n + 1) if co[i - 1] is not None]
        if drop:
            keep = [i for i in range(1, n + 1) if i != drop[0]]
            out.append(RelationProposal("metamorphic", spec=self._reindex(spec, keep), expect="same",
                                        note="drop a copy"))
        _, _, G = self._top_c(spec)
        if len(G) == 1:
            ids = {v[f"S{i}_ID"] for i in range(1, n + 1)}
            new = next(x for x in RESERVE_IDS if x not in ids)
            out.append(RelationProposal("metamorphic", spec=spec.with_slot(f"S{G[0]}_ID", S.id_slot(new)),
                                        expect=new if spec.qform == "ch_source" else "same",
                                        note="rename the deciding source"))
        return out

    # ============================================================================================ error models
    def error_models(self) -> dict:
        if self._ems is None:
            ems = {}
            for name in VALUE_EM:
                def fn(spec, name=name):
                    if spec.qform not in CHOICE_FORMS:
                        return None
                    return self._answer(spec, spec.qform, frozenset({name}))
                ems[name] = error_model(name, fn)
            self._ems = ems
        return self._ems
