"""gen3_rule_chain: yn2b family F1, source `gd_gen3_rule_chain` (yn2b/SPEC.md section 5 F1).

F1a long rule chains (3,400 base rows: 1,900 yes/no + 1,500 choice, of which 200 JB-letter) and F1b numeric claim
checks (600 yes/no), plus about 8% attack twins. Labels come only from deterministic CPU programs:
  * own F1a documents (9 train document families + school transport held out; 4 train styles + contract held out):
    rc_core.evaluate() applies the clause graph to the case (rc_core docstring has the semantics); the decisive
    clause is the unique clause whose deletion changes the outcome (0 or 2+ such clauses: no decisive question);
  * gen2_long_policy reuse (rc_gen2; the six domain classes' decide() == decide2() through gen2's evaluate(); only
    the classes, V, Reject, evaluate and build_state are imported): built only with --with-gen2. Its boilerplate and
    code definitions share 12-word runs with golden_dev's gd_gen2_long_policy rows, so check_yn2b 7.2 would drop
    every such unit; the default build replaces those rows with own-document rows (incl. 6-12K documents);
  * F1b: exact rational arithmetic (rc_numeric.truth).
mv_core turns the views into GOLDEN-compatible raw rows and checks them. The independent decide2 is
golden_src/gen3/v3_rule_chain.py, written by agent E from the rendered text and yn2b/F1_RULE_CHAIN_FORMAT.md only;
this builder runs it when it exists (SPEC 8.1). Its own parse-back (rc_render.parse_state, rc_numeric.parse_state)
is a rendering self-check, not that decide2.

Views per latent (one call_id unit, at most 5 rows): base; contrast twin (one decisive atom flips, gold flips); ladder
(the inverted question, `complement`); format twin (`equiv`); choice mirror; JB-letter; attack twin (`inv`).
Dev: 200 dev_iid + 200 dev_holdout (school transport and the contract style). devx is reviewer R's: devx_latents().

Balance: a gold balancer chooses each unit's answers over the joint and marginal SPEC 4.6 strata; rc_repair then drops
the few single views (or units) that still keep a stratum or an artefact correlation off target (never a label edit).

Run:  PYTHONDONTWRITEBYTECODE=1 ../.venv/bin/python golden_src/gen3/gen3_rule_chain.py [--write] [--overwrite]
      [--report PATH] [--with-gen2] [--scale X]      |  --devx-out [--overwrite]: yn2b/f1_devx_latents.json for R
Tests: yn2b/tests/test_gen3_rule_chain_*.py
"""
from __future__ import annotations

import argparse
import copy
import datetime as dt
import json
import math
import re
import sys
from collections import Counter, defaultdict
from fractions import Fraction
from pathlib import Path

HERE = Path(__file__).resolve().parent
if str(HERE) not in sys.path:
    sys.path.insert(0, str(HERE))
import mv_core as mv  # noqa: E402
import rc_core as RC  # noqa: E402
import rc_render as RR  # noqa: E402
import rc_skins as SK  # noqa: E402
import rc_numeric as NB  # noqa: E402

KEY = "gen3_rule_chain"
GEN_VERSION = "gen3_rule_chain-1"

SKINS_V = mv.Variants("rc_skins", sorted(SK.SKINS), holdout=[SK.HOLDOUT_SKIN])
STYLES_V = mv.Variants("rc_styles", RR.STYLES, holdout=[RR.HOLDOUT_STYLE])
FMTS_A = ("json", "markdown", "kv", "prose", "email", "log:chrono", "log:newest", "log:grouped", "table:md",
          "table:csv")
FMTS_B = ("json", "markdown", "kv", "prose", "log:chrono", "log:newest")
G2_DOMS = ("home", "travel", "lease", "benefits", "grant", "compliance")
# "None of these" (mv_core.NONE_DEFAULT) is a whole-string 12-gram hit in several dev / eval splits (check_yn2b 7.2
# would drop the unit), so F1 words its none options itself
NONE_CLAUSE = "None of the clauses listed"
NONE_OUTCOME = "None of the outcomes listed"

# ------------------------------------------------------------------------------------------------ row targets
TARGETS = {
    "train": {"a_yn": 1300, "a_ch": 815, "a_jb": 205, "b_yn": 580, "g_yn": 530, "g_ch": 430, "attack": 325},
    "dev_iid": {"a_yn": 64, "a_ch": 42, "a_jb": 20, "b_yn": 28, "g_yn": 0, "g_ch": 0, "attack": 16},
    "dev_holdout": {"a_yn": 80, "a_ch": 54, "a_jb": 24, "b_yn": 0, "g_yn": 0, "g_ch": 0, "attack": 16},
}

# ------------------------------------------------------------------------------------------------ questions (F1a)
Q_POS = {"pos1": "Under the {doc}, is the outcome of this {req} \"{X}\"?",
         "pos2": "Applying the {doc} to the case file, is the outcome of this {req} \"{X}\", rather than a "
                 "different outcome?",
         "pos3": "Does the {doc} give this {req} the outcome \"{X}\", rather than a different one?"}
Q_INV = {"inv1": "Under the {doc}, is the outcome of this {req} different from \"{X}\"?",
         "inv2": "Applying the {doc} to the case file, is the outcome of this {req} a different outcome from "
                 "\"{X}\"?"}
Q_JDG = {"jdg1": "The case file shows a decision recorded for this {req}. Is that recorded decision consistent with "
                 "the {doc}, rather than at odds with it?",
         "jdg2": "Is the decision recorded for this {req} supported by the {doc} when it is applied to the case "
                 "file?",
         "jdg3": "Is the decision recorded for this {req} in line with the {doc}, rather than at odds with it?"}
Q_JINV = {"jinv1": "Is the decision recorded for this {req} at odds with the {doc} when it is applied to the case "
                   "file?"}
Q_OUT = {"out1": "Under the {doc}, what is the outcome of this {req}?",
         "out2": "Which outcome does the {doc} give this {req}?"}
Q_DEC = {"dec1": "Which of these clauses decides this {req} under the {doc}, that is, deleting that one clause alone "
                 "would change the outcome?",
         "dec2": "Deleting which one of these clauses of the {doc} would, on its own, change the outcome of this "
                 "{req}?"}
Q_AMT = {"amt1": "Under the {doc}, which range contains the {unit_word} given for this {req}?",
         "amt2": "Which of these ranges holds the {unit_word} that this {req} receives under the {doc}?"}
Q_JB = {"jbq1": "Which of these statements about this {req} does the {doc} bear out?"}
Q_JBF = {"jbf1": "Does the {doc} bear out this statement about this {req}: the outcome is \"{X}\"?"}
Q_JBJ = {"jbj1": "Which of these statements about the decision recorded for this {req} does the {doc} bear out?"}
Q_JBJF = {"jbjf1": "Does the {doc} bear out this statement: the decision recorded for this {req} is consistent with "
                   "the {doc}?"}
ALL_Q = {**Q_POS, **Q_INV, **Q_JDG, **Q_JINV, **Q_OUT, **Q_DEC, **Q_AMT, **Q_JB, **Q_JBF, **Q_JBJ, **Q_JBJF}


def yn_defs(kind: str, sk: dict) -> dict:
    d = sk["doc"]
    if kind == "pos":
        return {"yes": f"Applying every clause of the {d} that bears on the case (requirements, exceptions, "
                       f"exclusions, amendments in force, limits and the precedence rule) gives exactly the outcome "
                       f"named in the question.",
                "no": f"Applying those clauses of the {d} gives an outcome other than the one named in the question."}
    if kind == "inv":
        return {"yes": f"Applying every clause of the {d} that bears on the case (requirements, exceptions, "
                       f"exclusions, amendments in force, limits and the precedence rule) gives an outcome other than "
                       f"the one named in the question.",
                "no": f"Applying those clauses of the {d} gives exactly the outcome named in the question."}
    if kind == "jdg":
        return {"yes": f"The decision recorded in the case file is the outcome that the {d} gives when every clause "
                       f"that bears on the case is applied.",
                "no": f"The {d}, applied in full, gives an outcome other than the decision recorded in the case file."}
    if kind == "jinv":
        return {"yes": f"The {d}, applied in full, gives an outcome other than the decision recorded in the case file.",
                "no": f"The decision recorded in the case file is the outcome that the {d} gives when every clause "
                      f"that bears on the case is applied."}
    raise ValueError(kind)


def jb_texts(kind: str, sk: dict, X: str | None) -> tuple[str, str]:
    d, req = sk["doc"], sk["req"]
    if kind in ("jdg", "jinv"):
        return (f"The decision recorded for this {req} is consistent with the {d}.",
                f"The decision recorded for this {req} is not consistent with the {d}.")
    return (f"Under the {d}, the outcome of this {req} is \"{X}\".",
            f"Under the {d}, the outcome of this {req} is some other outcome than \"{X}\".")


# ------------------------------------------------------------------------------------------------ questions (F1b)
QB_POS = {"bpos1": "Under the rules in the card, does the evidence establish the claim?",
          "bpos2": "Read with the card's rules, do the figures in the evidence establish the claim, rather than "
                   "fail to establish it?"}
QB_INV = {"binv1": "Under the rules in the card, does the evidence fail to establish the claim?"}
QB_JDG = {"bjdg1": "The fact-check log has an entry for this claim. Is that entry consistent with the evidence under "
                   "the card's rules, rather than at odds with it?",
          "bjdg2": "Under the card's rules, is the fact-check log entry for this claim supported by the evidence?"}
QB_JINV = {"bjinv1": "Under the card's rules, is the fact-check log entry for this claim at odds with the evidence, "
                     "rather than supported by it?"}
ALL_QB = {**QB_POS, **QB_INV, **QB_JDG, **QB_JINV}

# ------------------------------------------------------------------------------------------------ questions (gen2)
QG_OUT = {"gout1": "Applying the {docname} to the file, is the outcome \"{X}\"?",
          "gout2": "Under the {docname} and the facts in the file, does this case end with the outcome \"{X}\", "
                   "rather than a different one?"}
QG_INV = {"ginv1": "Applying the {docname} to the file, is the outcome different from \"{X}\"?"}
QG_AMT = {"gamt1": "Applying the {docname} to the file, is {amount_word} more than {thr}?"}
QG_PERM = {"gperm1": "Under the manual, may this proposal go ahead without prior approval from Compliance?"}
QG_CH = {"gch1": "Applying the {docname} to the file, which outcome applies?",
         "gch2": "Which outcome does the {docname} give for the case in the file?"}
ALL_QG = {**QG_OUT, **QG_INV, **QG_AMT, **QG_PERM, **QG_CH}


def g2_defs(kind: str, docname: str) -> dict:
    if kind == "out":
        return {"yes": f"Applying every operative clause of the {docname} to the facts in the file (definitions, "
                       f"exclusions and their exceptions, endorsements, amendments, limits, deductibles and "
                       f"conditions) gives exactly the outcome named in the question.",
                "no": f"Applying those clauses of the {docname} gives an outcome other than the one named in the "
                      f"question."}
    if kind == "inv":
        return {"yes": f"Applying every operative clause of the {docname} to the facts in the file (definitions, "
                       f"exclusions and their exceptions, endorsements, amendments, limits, deductibles and "
                       f"conditions) gives an outcome other than the one named in the question.",
                "no": f"Applying those clauses of the {docname} gives exactly the outcome named in the question."}
    if kind == "amt":
        return {"yes": f"The exact amount due under the {docname}, after every limit, deductible, percentage, cap and "
                       f"deduction, is more than the figure in the question.",
                "no": "That exact amount is equal to or less than the figure in the question, including when nothing "
                      "is due."}
    if kind == "perm":
        return {"yes": "Under the manual the proposal may go ahead without prior approval from Compliance, possibly "
                       "with a register entry.",
                "no": "Under the manual the proposal needs prior approval from Compliance or is prohibited."}
    raise ValueError(kind)


TIER_KNOBS = {  # SPEC 5 F1 hardness knobs per tier
    "easy": dict(nd=(2, 4), amend=0.0, boundary=0.15, business=0.0, defn=0.0, decoy=0.0, prec=0.0, grp_none=0.6),
    "standard": dict(nd=(3, 8), amend=0.3, boundary=0.3, business=0.2, defn=0.3, decoy=0.25, prec=0.3, grp_none=0.15),
    "judge": dict(nd=(3, 8), amend=0.3, boundary=0.3, business=0.2, defn=0.3, decoy=0.25, prec=0.3, grp_none=0.15),
    "hard": dict(nd=(6, 14), amend=0.65, boundary=0.55, business=0.35, defn=0.4, decoy=0.4, prec=0.5, grp_none=0.05),
}
FEASIBLE = {"deny_allow": ("PARTIAL", "FULL", "INELIG", "LATE", "DOCS"),
            "allow_deny": ("EXCL", "INELIG", "LATE", "DOCS"),
            "near_miss": ("INELIG", "LATE", "DOCS", "PARTIAL", "FULL"),
            None: ("INELIG", "LATE", "DOCS", "PARTIAL", "FULL")}
STOP = set("the a an of to in on for and or is are be by with this that from at as any not no".split())


def part_of(split: str) -> str:
    return "dev" if split.startswith("dev") else split


def words(s: str) -> set:
    return {w for w in re.findall(r"[a-z]+", s.lower()) if w not in STOP and len(w) > 2}


# ------------------------------------------------------------------------------------------------ R2 fixes (1 Oct)
# Reviewer R2 (yn2b/r2_rule_chain_review.py, yn2b/r2_rule_chain_gate.json) found cheap surface cues in the first
# written build:
#   1. a yes/no question named the 'document missing' / 'exclusion' outcome in a 'no' row mostly when the case file
#      did NOT show that outcome's cue, while every 'yes' row shows it: "named outcome + its cue -> yes" scored 81%
#      on the rows that name DOCS / EXCL. Now a 'no' row names DOCS / EXCL only when the cue is shown (the tempting
#      wrong outcome), so the cue alone no longer separates 'yes' from 'no';
#   2. the decisive-clause options paired a requirement / limit gold with exception / exclusion distractors, so
#      "pick the requirement option" scored 69% and "pick the limit option" 70%. Now one distractor shares the gold's
#      clause group and the other groups are offered where a kind reader would otherwise do best;
#   3. an amount-range question put the requested amount in the gold range 72% of the time (every FULL row plus the
#      PARTIAL rows whose cap sat in the request's range). A PARTIAL row's ranges now put the request above the gold
#      range;
#   4. ambiguity hunt: a decisive question where deleting another clause changes only the amount granted (2 rows;
#      'change the outcome' could include the amount) and a business-day item whose received date is a weekend /
#      holiday next to the deadline (5 rows; counting business days in between flips it) are rejected; the warranty
#      and formulary exclusion outcomes are worded so they fit every exclusion they stand for (rc_skins).
CUE_CODES = ("DOCS", "EXCL")
CLAUSE_GROUP = {"req": "req", "exc": "exc", "excexc": "exc", "excl": "excl", "amend": "amend", "lim_gen": "limit",
                "lim_tab": "limit"}


def cue_codes(sk: dict, case: dict) -> set:
    """Outcome codes whose cheap surface cue the case file shows: DOCS when the document is not shown as included,
    EXCL when any exclusion fact is set (whatever the exclusion's category scope or exceptions)."""
    out = set()
    if case.get("docs") is not True:
        out.add("DOCS")
    if any(case["flags"].get(f) for f, x in sk["flags"].items() if x["role"] == "excl"):
        out.add("EXCL")
    return out


def clause_group(doc: dict, cid: str) -> str:
    k = RC.clause(doc, cid)["kind"]
    return CLAUSE_GROUP.get(k, k)


def amount_pivots(doc: dict, case: dict) -> list[str]:
    """Candidate clauses whose deletion changes the outcome code OR the amount granted (the 'code+amount' reading of
    'change the outcome')."""
    base = RC.evaluate(doc, case)
    key = (base["code"], base["granted"])
    return [c["id"] for c in doc["clauses"] if c["kind"] in RC.CANDIDATE_KINDS
            and (lambda t: (t["code"], t["granted"]))(RC.evaluate(doc, case, None, drop=frozenset([c["id"]]))) != key]


def _next_bday(d: dt.date, s: int, hol: set) -> dt.date:
    while True:
        d += dt.timedelta(days=s)
        if d.weekday() < 5 and RC.iso(d) not in hol:
            return d


def weekday_sensitive(doc: dict, case: dict, code: str | None = None) -> bool:
    """A business-day document, a received date that is not a business day, and the outcome changes when that date
    moves to the next or the previous business day: the item depends on how a non-business received date is counted
    (the documents settle it, but R2 asked for such items to be avoided)."""
    if doc["count"] != "business":
        return False
    hol = set(doc["holidays"])
    rq = RC.D(case["request"])
    if rq.weekday() < 5 and RC.iso(rq) not in hol:
        return False
    code = code or RC.evaluate(doc, case)["code"]
    for s in (1, -1):
        c2 = dict(case, request=RC.iso(_next_bday(rq, s, hol)))
        if RC.evaluate(doc, c2)["code"] != code:
            return True
    return False


class KindBalance:
    """Decisive-clause option groups (requirement, exception, exclusion, amendment, limit), counted in rows: how often
    each group is the gold and how often it is offered at all. need(g) is a kind reader's accuracy on g (gold share
    among the rows that offer g); the distractors come from the groups where it is highest."""

    def __init__(self):
        self.gold = Counter()
        self.offer = Counter()

    def need(self, g: str) -> float:
        return (self.gold[g] + 1) / (self.offer[g] + 2)

    def add(self, gold_group: str | None, groups: set, w: int):
        if gold_group:
            self.gold[gold_group] += w
        for g in groups:
            self.offer[g] += w


# ================================================================================================ gold balancer
class GoldBalancer:
    """The yes/no (+ JB) gold that keeps every planned row of a unit balanced: the joint SPEC 4.6 stratum and the
    marginals (tier, format, pack, template, renderer, view, polarity, length bin, question kind, target outcome,
    true outcome, edge tags), counted over every committed row."""

    MARG = ("qkind", "tier", "fmt", "pack", "tpl", "renderer", "view", "polarity", "len_bin", "src", "target",
            "truth", "edge", "lenb")

    def __init__(self):
        self.c = defaultdict(lambda: [0, 0])

    @staticmethod
    def keys(split: str, m: dict) -> list:
        split = part_of(split)      # dev_iid + dev_holdout are checked together as one dev part
        ks = [("J", split, m["qkind"], m["tier"], m["polarity"], m["fmt"], m["len_bin"], m["pack"]), ("all", split)]
        if split == "dev" and m["qkind"] == "jb":
            ks.append(("jbcell", split, m["tier"], m["fmt"], m["len_bin"]))   # small JB sets: exact pairs
        if m.get("target") is not None and m.get("tpl") is not None:
            # the question names the target outcome: per template, every target must be yes half the time (else
            # a question-only bag of words learns 'template word + outcome word' -> answer)
            ks.append(("tplx", split, m["tpl"], m["target"]))
            ks.append(("qtext", split, m["tpl"], m["pack"], m["target"]))   # the exact question text
        for k in GoldBalancer.MARG:
            v = m.get(k)
            if v is None:
                continue
            if k == "edge":
                for t in v:
                    ks.append(("edge", split, t))
                continue
            ks.append((k, split, v))
            ks.append((k, split, m["qkind"], v))
        return ks

    PEN = {"J", "all", "qkind", "tier", "fmt", "pack", "tpl", "renderer", "view", "polarity", "len_bin", "lenb",
           "target", "jbcell", "tplx", "qtext"}

    @staticmethod
    def _tol(k, n) -> float:
        if k[0] == "J":
            return max(1.0, 0.05 * n)
        if k[0] == "jbcell":
            return 0.5
        if k[0] == "qtext":
            return max(1.0, 0.05 * n)
        if len(k) == 4 and (k[2] == "jb" or (k[2] == "yn" and k[1] == "dev")):
            # few rows per kind (JB anywhere, yes/no in the small dev part): artefact_corr wants |corr| < 0.05
            return max(1.0, 0.02 * n)
        return max(1.0, 0.04 * n)

    @staticmethod
    def _pen_key(k) -> bool:
        """mv_core's balance and artefact checks look at these strata (and the missing-info rows of edge_report);
        the target / truth / source keys only steer the secondary score (question-only probe)."""
        return k[0] in GoldBalancer.PEN or (k[0] == "edge" and str(k[-1]).startswith("missing_info"))

    def score(self, rows: list) -> tuple:
        """rows: [(keys, is_yes)] -> (penalty above tolerance, weighted squared imbalance) after adding them; both
        grow fastest on the strata that are already furthest from 50%."""
        add = defaultdict(lambda: [0, 0])
        for ks, y in rows:
            for k in ks:
                add[k][0] += int(y)
                add[k][1] += 1
        jpen, pen, sq = 0.0, 0.0, 0.0
        for k, (dy, dn) in add.items():
            y, n = self.c[k]
            y2, n2 = y + dy, n + dn
            d0, d1 = abs(y - n / 2), abs(y2 - n2 / 2)
            if self._pen_key(k):
                t0, t1 = self._tol(k, n), self._tol(k, n2)
                x = max(0.0, d1 - t1) ** 2 - max(0.0, d0 - t0) ** 2
                if k[0] == "J":
                    jpen += x
                else:
                    pen += x
            sq += (d1 ** 2 - d0 ** 2) / (n2 + 4)
        return round(jpen + pen, 9), round(jpen, 9), round(sq, 9)

    def add(self, rows: list):
        for ks, y in rows:
            for k in ks:
                self.c[k][0] += int(y)
                self.c[k][1] += 1


class Placer:
    """Gold positions of choice rows, counted per (part, view, template, K) exactly as mv_core.position_report groups
    them. A row's gold position fills the largest deficit over every stratum the row will appear in (its own view,
    plus the format and attack copies that repeat its option list); a contrast twin's gold gets its own balanced
    position. The "None of these" option (decisive and mirror rows): offered in 20% of rows, gold in 25% of those,
    K never depends on it. Nothing is counted until the unit is kept (commit)."""

    def __init__(self):
        self.c = defaultdict(Counter)
        self.none = defaultdict(lambda: [0, 0, 0])   # (part, kind) -> [rows, offered, none gold]

    def pick(self, strata, K: int, allowed, rng) -> int:
        sc = {}
        for p_ in allowed:
            sc[p_] = sum(self.c[s][p_] - sum(self.c[s].values()) / K for s in strata)
        best = min(sc.values())
        top = [p_ for p_ in allowed if sc[p_] <= best + 1e-9]
        return top[rng.randrange(len(top))]

    @staticmethod
    def arrange(K: int, fixed: dict, others: list, rng) -> list:
        others = list(others)
        rng.shuffle(others)
        it = iter(others)
        return [fixed[i] if i in fixed else next(it) for i in range(K)]

    def none_plan(self, key, w: int = 1) -> tuple[bool, bool]:
        """Counted in rows (a row's format / attack copies repeat its options), as mv_core.none_report counts."""
        n, off, ng = self.none[key]
        offer = off + w <= 0.2 * (n + w) + 1e-9
        gold = offer and ng + w <= 0.25 * (off + w) + 0.5 * w + 1e-9 and \
            abs(ng + w - 0.25 * (off + w)) <= abs(ng - 0.25 * (off + w))
        return offer, gold

    def mirror(self, gold, wrongs: list, rng, strata, K: int, none_key, none_text=mv.NONE_DEFAULT):
        """(options, gold option, none option or None, commit token) for a K-option row built from the gold and
        wrong answers (shortcut answers first), with the SPEC 4.2 'None of these' rule."""
        wrongs = [w for w in dict.fromkeys(wrongs) if w != gold and w != none_text]
        offer, ng = self.none_plan(none_key, len(strata))
        need = K - 1 if (not offer or ng) else K - 2
        if len(wrongs) < need:
            raise mv.Reject("mirror", "not enough wrong options")
        if offer and ng:
            opts = self.arrange(K - 1, {}, wrongs[:K - 1], rng) + [none_text]
            pos, g = K - 1, none_text
        elif offer:
            pos = self.pick(strata, K, range(K - 1), rng)
            opts = self.arrange(K - 1, {pos: gold}, wrongs[:K - 2], rng) + [none_text]
            g = gold
        else:
            pos = self.pick(strata, K, range(K), rng)
            opts = self.arrange(K, {pos: gold}, wrongs[:K - 1], rng)
            g = gold
        return opts, g, (none_text if offer else None), {"pos": [(s, pos) for s in strata],
                                                          "none": (none_key, offer, ng, len(strata))}

    def commit(self, tok):
        if not tok:
            return
        for s, p_ in tok.get("pos", []):
            self.c[s][p_] += 1
        if tok.get("none"):
            key, offer, ng, w = tok["none"]
            self.none[key][0] += w
            self.none[key][1] += w * int(offer)
            self.none[key][2] += w * int(ng)


# ================================================================================================ the builder
class RuleChainBuilder:
    def __init__(self, fb: mv.FamilyBuilder, use_gen2: bool = False, scale: float = 1.0):
        self.fb = fb
        self.use_gen2 = use_gen2
        self.scale = scale
        self.gb = GoldBalancer()
        self.stats = Counter()
        self.expect = {}            # rid -> expected label inputs for the self-check
        self.names = set()
        self.facts = {}             # latent id -> facts (for devx / F4(b) export)
        self.exc_rows = Counter()   # exception group -> committed rows (SPEC 4.6 three equal groups)
        self.decisive_pos = Counter()
        self.placer = Placer()
        self.kinds = defaultdict(KindBalance)      # part -> decisive option groups (R2 fix 2)
        self.amt_codes = defaultdict(Counter)      # part -> kept amount-range rows by outcome (R2 fix 3)
        self._pending_tok = []
        self.cue = defaultdict(lambda: [0, 0])     # (part, word) -> [answer-flipping rows, rows]

    # ------------------------------------------------------------------------------------------ bookkeeping
    def targets(self, split: str) -> dict:
        t = dict(TARGETS[split])
        if not self.use_gen2:
            t["a_yn"] += t["g_yn"]
            t["a_ch"] += t["g_ch"]
            t["g_yn"] = t["g_ch"] = 0
        if self.scale != 1.0:
            t = {k: int(round(v * self.scale)) for k, v in t.items()}
        return t

    def counts(self, split: str) -> Counter:
        c = Counter()
        for r in self.fb.rows:
            if mv._split_of(r) != split:
                continue
            m = r["meta"]
            if m["view"] == "attack":
                c["attack"] += 1
                continue
            src = "g" if m["pack"].startswith("g2_") else ("b" if m["pack"].startswith("nb_") else "a")
            q = {"yn": "yn", "jb": "jb"}.get(m["qkind"], "ch")
            if src != "a" and q == "jb":
                q = "ch"
            c[f"{src}_{q}"] += 1
        return c

    def need(self, split: str) -> dict:
        t, c = self.targets(split), self.counts(split)
        return {k: t[k] - c[k] for k in t}

    # ------------------------------------------------------------------------------------------ build a split
    def build_split(self, split: str):
        fb, rng = self.fb, self.fb.rng(split)
        pool = fb.names(split)
        self.builder = RC.Builder(mv.rng_for(KEY, split, "rc"), pool)
        guard = 0
        while True:
            need = self.need(split)
            rem = {k: v for k, v in need.items() if v > 0 and k != "attack"}
            if not rem:
                break
            guard += 1
            if guard > 60000:
                raise RuntimeError(f"{split}: stalled with {need}; rejects {fb.rejects.most_common(12)}")
            # source by remaining share
            src_need = {"a": rem.get("a_yn", 0) + rem.get("a_ch", 0) + rem.get("a_jb", 0),
                        "b": rem.get("b_yn", 0), "g": rem.get("g_yn", 0) + rem.get("g_ch", 0)}
            tot = sum(src_need.values())
            x = rng.random() * tot
            src = "a"
            for s_, v in src_need.items():
                x -= v
                if x <= 0 and v > 0:
                    src = s_
                    break
            snap = self._snapshot()
            self._pending_tok = []
            try:
                if src == "a":
                    self.latent_a(split, rng, pool, need)
                elif src == "b":
                    self.latent_b(split, rng, pool, need)
                else:
                    self.latent_g(split, rng, pool, need)
            except mv.Reject as e:
                self._restore(snap)
                fb.reject(e)

    # ------------------------------------------------------------------------------------------ helpers
    _SNAP = ("q_jb", "q_plant_tpl", "q_spoof_tpl", "q_plant_dir", "q_spoof")

    def _snapshot(self):
        """mv_core quotas that count at pick time (JB wording, plant template / direction / spoof): restored when a
        unit is rejected, so the balance counts only kept rows."""
        return {k: copy.deepcopy(getattr(self.fb, k).counts) for k in self._SNAP}

    def _restore(self, snap):
        for k, v in snap.items():
            getattr(self.fb, k).counts = v

    def _tier(self, split, rng, forced=None):
        return forced or self.fb.next_tier(split, rng)

    def _row_meta(self, split, latent, spec: mv.RowSpec, src: str, extra: dict | None = None) -> dict:
        pol = spec.polarity if spec.qkind == "yn" else (0 if spec.qkind == "jb" else None)
        m = {"qkind": spec.qkind, "tier": latent.tier, "polarity": pol, "fmt": spec.fmt,
             "len_bin": mv.len_bin(len(spec.state.rstrip())), "pack": latent.pack, "tpl": spec.tpl,
             "renderer": spec.renderer, "view": spec.view, "src": src}
        m.update(extra or {})
        return m

    def _plant_sender(self, rng, pool):
        return f"{pool.person(rng)} ({rng.choice(['adviser', 'neighbour', 'volunteer', 'consultant', 'relative'])})"

    def _exc_group_pick(self, rng, allowed, split):
        """The exception group with the fewest committed rows in this split (SPEC 4.6: three equal groups)."""
        al = [g for g in ("deny_allow", "allow_deny", "near_miss") if g in allowed]
        low = min(self.exc_rows[(split, g)] for g in al)
        cand = [g for g in al if self.exc_rows[(split, g)] <= low + 2]
        return rng.choice(cand)

    # ================================================================================================ F1a (own)
    def latent_a(self, split, rng, pool, need):
        fb = self.fb
        tier = self._tier(split, rng)
        kn = TIER_KNOBS[tier]
        # ---- base question kind
        if tier == "judge":
            bk = "yn"
        else:
            yn_need = max(0, need.get("a_yn", 0)) + max(0, need.get("a_jb", 0))
            ch_need = max(0, need.get("a_ch", 0))
            bk = "yn" if rng.random() * (yn_need + ch_need + 1e-9) < yn_need else "ch"
        if bk == "ch":
            ck = fb.surface("a_chkind", ["outcome", "outcome", "decisive", "amount"], rng, split=split, extra=(tier,))
        else:
            ck = None
        # ---- strata first: document family, style, format, question template
        skin, style = self._skin_style(split, rng)
        if split != "train" and bk == "yn" and tier != "judge" and need.get("a_jb", 0) > 0 and rng.random() < 0.6:
            fmt = fb.surface("a_fmt_jb", ["json", "markdown", "prose", "kv"], rng, split=split, extra=(tier,))
        else:
            fmt = fb.surface("a_fmt", list(FMTS_A), rng, split=split, extra=(tier, bk))
        if bk == "yn":
            if tier == "judge":
                qk = "jdg"
                tpl = fb.surface("a_tpl_jdg", sorted(Q_JDG), rng, split=split)
            else:
                qk = "inv" if rng.random() < 0.3 else "pos"
                tpl = fb.surface(f"a_tpl_{qk}", sorted(Q_POS if qk == "pos" else Q_INV), rng, split=split,
                                 extra=(tier,))
        else:
            qk = ck
            tpl = fb.surface(f"a_tpl_{ck}", sorted({"outcome": Q_OUT, "decisive": Q_DEC, "amount": Q_AMT}[ck]), rng,
                             split=split)
        # ---- plan: group, code, mechanisms
        if rng.random() < kn["grp_none"]:
            grp = None
        else:
            grp = self._exc_group_pick(rng, ("deny_allow", "allow_deny", "near_miss") if ck != "amount" else
                                       ("deny_allow", "near_miss"), split)
        codes = [c for c in FEASIBLE[grp] if (ck != "amount" or c in SK.GRANTS)]
        if grp == "allow_deny":
            codes = list(FEASIBLE["allow_deny"])
        shares = {c: (0.4 if c == "EXCL" else 0.2) if grp == "allow_deny" else 1.0 for c in sorted(codes)}
        if ck == "amount":
            # R2 fix 3: kept amount rows lean PARTIAL (the request's range is the gold range only in FULL rows)
            code = self._amount_code(split, rng)
            fb.quota("a_code:" + ",".join(sorted(codes)), shares).add((split, bk, grp), code, also=((split,),))
        else:
            code = fb.quota("a_code:" + ",".join(sorted(codes)), shares).pick((split, bk, grp), rng,
                                                                              also=((split,),))
        long_ = split == "train" and fb.quota("a_long", {True: 0.25, False: 0.75}).pick((split,), rng)
        plan = {"code": code, "group": grp, "phr": "ho" if split in ("dev_holdout", "devx") else "tr",
                "n_repealed": rng.randint(9, 14) if long_ else (rng.randint(0, 2) if tier == "hard" else 0),
                "amend": rng.choice(["in_force", "not_yet", "withdrawn", "superseded", "in_force"])
                if rng.random() < kn["amend"] else None,
                "business": rng.random() < kn["business"], "defn": rng.random() < kn["defn"],
                "decoy": rng.random() < kn["decoy"],
                "n_distract": rng.randint(16, 24) if long_ else rng.randint(*kn["nd"]),
                "prec_case": code in SK.GRANTS and rng.random() < kn["prec"],
                "prec": rng.choice(["specific", "later", "lower", "named"])}
        if rng.random() < kn["boundary"]:
            plan["boundary"] = rng.choice(["exact", "exact", "off1"])
            gates = ["elig", "time"] + (["amount"] if code in SK.GRANTS else [])
            if code in ("INELIG", "LATE"):
                gates = [RC.CODE_GATE[code]] * 2 + gates
            plan["boundary_gate"] = rng.choice(gates)
        if code == "DOCS" and rng.random() < 0.35:
            plan["missing"] = "decisive"
        if grp == "deny_allow" and code in SK.GRANTS and rng.random() < 0.3:
            plan["rescue"], plan["missing"] = "docs", "irrelevant"
        elif grp == "deny_allow":
            # R2 fix 1: a missing document or a set exclusion fact that an exception lifts, often enough that the cue
            # alone ('document missing -> refused', 'exclusion fact -> excluded') does not predict the outcome
            # (SPEC 4.6 'missing info -> no' balance); the rest keep rc_core's random rescue gate
            x_ = rng.random()
            if code != "DOCS" and x_ < self.DOCS_RESCUE:
                plan["rescue"] = "docs"
            elif code != "EXCL" and x_ < self.DOCS_RESCUE + self.EXCL_RESCUE:
                plan["rescue"] = "excl"
        # ---- sample until the outcome and the group are the planned ones
        doc = case = tr = None
        for _ in range(25):
            try:
                d0, c0 = self.builder.sample(skin, style, plan)
            except mv.Reject:
                continue
            g, t0 = RC.decide(d0, c0)
            if mv.is_undefined(g) or g != code:
                continue
            gs = RC.groups(d0, c0, t0)
            if set(gs) != ({grp} if grp else set()):
                continue
            if weekday_sensitive(d0, c0, g):        # R2 fix 4
                self.stats["a_weekday_resample"] += 1
                continue
            doc, case, tr = d0, c0, t0
            break
        if doc is None:
            raise mv.Reject("a_plan", f"{code}/{grp}")
        piv0 = RC.pivotal(doc, case)
        self._reorder(doc, piv0[0] if len(piv0) == 1 else None, rng)
        st = RC.steps(doc, case, tr)
        if tier == "easy" and st > 2:
            raise mv.Reject("a_easy_steps")
        if tier == "hard" and st < 3:
            raise mv.Reject("a_hard_steps")
        sct = RC.shortcut_traces(doc, case, tr)
        sk = SK.skin(skin)
        piv = RC.pivotal(doc, case)
        dec = piv[0] if len(piv) == 1 else None
        if ck == "decisive" and dec is None:
            raise mv.Reject("a_decisive", f"{len(piv)} pivotal clauses")
        if ck == "decisive" and amount_pivots(doc, case) != piv:     # R2 fix 4: an amount-only pivot is a 2nd reading
            raise mv.Reject("a_decisive_amount", "a clause changes only the amount granted")
        # ---- edges
        edge = set()
        gs = RC.groups(doc, case, tr)
        if grp:
            edge |= {"exception", f"exc:{grp}"}
            if grp == "allow_deny" and any(RC.clause(doc, c)["kind"] == "exc" for c in gs.get("allow_deny", [])):
                edge.add("hc:exception_to_exception")
            if any(c["kind"] == "excexc" for c in doc["clauses"]) and grp == "allow_deny":
                edge.add("hc:exception_to_exception")
        if plan.get("amend") and any(c["kind"] == "amend" and c["target"] != "" for c in doc["clauses"]):
            edge |= {"hc:amendment_effective", "temporal"}
        if plan.get("boundary"):
            edge |= {"numeric", "hc:boundary_exact" if plan["boundary"] == "exact" else "hc:boundary_off1",
                     "hc:inclusive_exclusive"}
        if doc["count"] == "business":
            edge |= {"hc:business_days", "temporal"}
        if plan.get("prec_case"):
            edge.add("hc:specific_over_general")
        if case.get("decoy"):
            edge.add("hc:decoy_id")
        if plan.get("missing") == "decisive":
            edge.add("missing_info:decisive")
        elif plan.get("missing") == "irrelevant" and case["docs"] is None:
            edge.add("missing_info:irrelevant")
        if st >= 3:
            edge.add("multi_hop")
        if code == "LATE":
            edge.add("temporal")
        if code in ("INELIG", "PARTIAL", "FULL"):
            edge.add("numeric")
        # ---- judge record (set before rendering: the record lives in the case file)
        X = None
        if qk == "jdg":
            case["record"] = None      # chosen with the gold below
        lat = fb.new_latent(split, f"a_{skin}", {"doc": doc, "case": case}, {"kind": qk, "tpl": tpl}, tier,
                            edge=tuple(sorted(edge)))
        self.facts[lat.latent_id] = {"src": "a", "doc": doc, "case": case, "query": qk, "code": code,
                                     "decisive": dec}
        u = fb.unit(lat)
        if bk == "yn":
            self._yn_unit(split, rng, pool, lat, u, sk, doc, case, tr, sct, fmt, tpl, qk, style, need, dec)
        else:
            self._ch_unit(split, rng, pool, lat, u, sk, doc, case, tr, sct, fmt, tpl, ck, style, need, dec, piv)
        self.stats[f"a_steps_{st}"] += 1
        for c in doc["clauses"]:
            pass
        self.names |= {case["name"], doc["org"], doc["place"]} | ({case["decoy"]["name"]} if case.get("decoy")
                                                                  else set())
        self.stats[f"a_code_{code}"] += 1
        self.stats[f"a_group_{grp}"] += 1
        if dec:
            idx = [c["id"] for c in doc["clauses"]].index(dec)
            third = min(2, 3 * idx // len(doc["clauses"]))
            self.decisive_pos[third] += 1

    def _reorder(self, doc, dec, rng):
        """Move whole blocks so the decisive clause lands in the first, middle or last third of the document as evenly
        as possible (SPEC 5 F1 knob). Blocks: General (first or last), Requirements, Exceptions (always after the
        Requirements, so the first-matching-clause solver keeps its meaning), Exclusions, Limits, Other provisions,
        Amendments. The order inside every block is kept (inside Requirements the decisive requirement may move to the
        block's start or end), so the outcome and the 'later clause prevails' limit choice never change; shortcut
        answers are computed after this step."""
        import itertools
        blocks = defaultdict(list)
        for c in doc["clauses"]:
            k = {"general": "G", "requirements": "R", "other": "O", "amendments": "A", "exceptions": "X",
                 "exclusions": "E", "limits": "L"}[c["sec"]]
            blocks[k].append(c)
        mids = [b_ for b_ in ("R", "X", "E", "L", "O", "A") if blocks.get(b_)]
        variants = []
        for perm in itertools.permutations(mids):
            if "X" in perm and perm.index("X") < perm.index("R"):
                continue
            variants.append(("G",) + perm)
            variants.append(perm + ("G",))
        rng.shuffle(variants)
        v = variants[0]
        rblock = blocks["R"]
        if dec is not None:
            low = min(self.decisive_pos[t] for t in range(3))
            targets = [t for t in range(3) if self.decisive_pos[t] == low]
            dclause = next(c for c in doc["clauses"] if c["id"] == dec)
            r_opts = [rblock]
            if dclause["sec"] == "requirements":
                rest = [c for c in rblock if c["id"] != dec]
                r_opts = [rblock, rest + [dclause], [rblock[0]] + [dclause] + [c for c in rest if c is not rblock[0]]]
            done = False
            for cand in variants:
                for rb in r_opts:
                    bl = dict(blocks, R=rb)
                    seq = [c["id"] for k in cand for c in bl.get(k, [])]
                    if min(2, 3 * seq.index(dec) // len(seq)) in targets:
                        v, rblock, done = cand, rb, True
                        break
                if done:
                    break
        blocks["R"] = rblock
        doc["clauses"] = [c for k in v for c in blocks.get(k, [])]

    def _skin_style(self, split, rng):
        fb = self.fb
        if split in ("dev_holdout", "devx"):
            mode = fb.surface("ho_mode", ["skin", "style", "both", "skin", "style"], rng, split=split)
            skin = SK.HOLDOUT_SKIN if mode in ("skin", "both") else fb.surface("skin", list(SKINS_V.kept), rng,
                                                                              split=split)
            style = RR.HOLDOUT_STYLE if mode in ("style", "both") else fb.surface("style", list(STYLES_V.kept), rng,
                                                                                 split=split)
            return skin, style
        return (fb.surface("skin", list(SKINS_V.kept), rng, split=split),
                fb.surface("style", list(STYLES_V.kept), rng, split=split))

    # ------------------------------------------------------------------------------------------ flips (contrast)
    def _flips(self, doc, case, sk, rng):
        """Candidate one-atom changes of the case or of one amendment date (each changes at most 3 lines)."""
        out = []
        req = RC.D(case["request"])
        for k in (1, 2, 3, 5, 8):
            for sgn in (-1, 1):
                c2 = copy.deepcopy(case)
                c2["request"] = RC.iso(req + dt.timedelta(days=sgn * k))
                out.append(("request_date", doc, c2))
        st = RC._step(sk)
        for k in (1, 2, 3, 5, 10, 20):
            for sgn in (-1, 1):
                v = RC.F(case["elig"]) + sgn * st * k
                if v < 0 or (v == 0 and doc["skin"] in RC.POSITIVE_ELIG):
                    continue
                c2 = copy.deepcopy(case)
                c2["elig"] = str(v)
                out.append(("elig", doc, c2))
        if case["docs"] is not None:
            c2 = copy.deepcopy(case)
            c2["docs"] = not case["docs"]
            out.append(("docs", doc, c2))
        used_flags = {a["f"] for c in doc["clauses"] for a in c.get("conds", []) if a["t"] == "flag"}
        for f in sorted(used_flags):
            c2 = copy.deepcopy(case)
            c2["flags"][f] = not case["flags"].get(f)
            out.append((f"flag:{f}", doc, c2))
        for cat, _, _ in sk["cats"]:
            if cat != case["cat"]:
                c2 = copy.deepcopy(case)
                c2["cat"] = cat
                out.append(("category", doc, c2))
        ast = RC._amt_step(sk)
        for k in (1, 2, 5, 10, 25, 60):
            for sgn in (-1, 1):
                a = int(case["amount"]) + sgn * ast * k
                if a <= 0:
                    continue
                c2 = copy.deepcopy(case)
                c2["amount"] = a
                out.append(("amount", doc, c2))
        for i, c in enumerate(doc["clauses"]):
            if c["kind"] == "amend" and not c["withdrawn"]:
                eff = RC.D(c["eff"])
                new = req + dt.timedelta(days=rng.randint(1, 40)) if eff <= req else req - dt.timedelta(
                    days=rng.randint(0, 40))
                d2 = copy.deepcopy(doc)
                d2["clauses"][i]["eff"] = RC.iso(new)
                ams = [x for x in d2["clauses"] if x["kind"] == "amend"]
                if [x["eff"] for x in ams] != sorted(x["eff"] for x in ams):
                    continue
                out.append(("amend_eff", d2, case))
        rng.shuffle(out)
        # R2 fix 1: flipping the cue atom itself (the document, an exclusion fact) makes a pair whose cue reader is
        # right on both rows; those flips are tried last
        cue_flips = {"docs"} | {f"flag:{f}" for f, x in sk["flags"].items() if x["role"] == "excl"}
        out.sort(key=lambda t: t[0] in cue_flips)
        return out

    def _twin(self, doc, case, sk, rng, fmt, base_state, want=None, accept=None, prefer=None, cue_flips=True):
        """A contrast twin: one atom flips, the outcome changes (want: the twin's code must be this one), at most 3
        lines of the state differ. prefer (R2 fix 1): twin outcomes tried first (the tempting outcomes whose cue the
        base case shows); cue_flips=False (R2 fix 1, yes/no units): never flip the cue atom itself (the document, an
        exclusion fact), whose pair a cue reader gets right on both rows. Returns (doc2, case2, trace2, flip name) or
        None."""
        code = RC.evaluate(doc, case)["code"]
        flips = self._flips(doc, case, sk, rng)
        if not cue_flips:
            cf = {"docs"} | {f"flag:{f}" for f, x in sk["flags"].items() if x["role"] == "excl"}
            flips = [f_ for f_ in flips if f_[0] not in cf]
        passes = (set(prefer), None) if prefer else (None,)
        for only in passes:
            got = self._twin_pass(flips, code, sk, fmt, base_state, want, accept, only)
            if got is not None:
                return got
        return None

    def _twin_pass(self, flips, code, sk, fmt, base_state, want, accept, only):
        for name, d2, c2 in flips:
            g2, t2 = RC.decide(d2, c2)
            if mv.is_undefined(g2) or g2 == code:
                continue
            if only is not None and g2 not in only:
                continue
            if want is not None and g2 != want:
                continue
            if accept is not None and not accept(d2, c2, t2):
                continue
            if c2["event"] > "2027-12-31" or c2["request"] < "2025-01-01":
                continue
            if SK.SKINS[d2["skin"]]["time"]["dir"] == "after" and c2["request"] < c2["event"]:
                continue        # R2: a claim received before the delivery / fault / prescription it is about
            if weekday_sensitive(d2, c2, g2):        # R2 fix 4
                continue
            s2 = RR.render_state(d2, c2, fmt, perm_seed=0)
            if mv.diff_lines(base_state, s2) > 3:
                continue
            return d2, c2, t2, name
        return None

    # ------------------------------------------------------------------------------------------ yes/no units
    def _yn_unit(self, split, rng, pool, lat, u, sk, doc, case, tr, sct, fmt, tpl, qk, style, need, dec):
        fb = self.fb
        code = tr["code"]
        perm = mv.derive_seed(lat.seed, "perm")
        tab = {"table": rng.choice(["md", "pipe"])}.get(style, "md")
        render = lambda d, c, f, plant=None: RR.render_state(d, c, f, plant, tab_layout=tab, perm_seed=perm)  # noqa
        if qk == "jdg":
            case["record"] = code          # placeholder of the same kind; the chosen record replaces it below
        base_state = render(doc, case, fmt)
        L = len(base_state)
        max_rows = min(5, 24000 // max(1, int(L * 1.08)))
        if L > 6000:
            max_rows = min(max_rows, 3)
        # ---- planned views (before gold)
        n = need
        want = []
        if rng.random() < 0.75:        # R2: was 0.65; yes/no twins no longer flip the cue atom, so fewer succeed
            want.append("contrast")
        if rng.random() < 0.3:
            want.append("ladder")
        if rng.random() < 0.22:
            want.append("format")
        p_jb = 0.42 if n.get("a_yn", 0) > 0 else 0.9
        if n.get("a_jb", 0) > 0 and qk != "jdg" and rng.random() < p_jb and (
                lat.split == "train" or fmt in ("json", "markdown", "prose", "kv")):
            want.append("jb")
        if n.get("a_ch", 0) > 0 and rng.random() < 0.12:
            want.append("mirror")
        if n.get("attack", 0) > 0 and rng.random() < 0.26:
            want.append("attack")
        rng.shuffle(want)
        want = want[: max_rows - 1]
        twin = None
        if "contrast" in want:
            twin = self._twin(doc, case, sk, rng, fmt, base_state,
                              prefer=cue_codes(sk, case) - {tr["code"]}, cue_flips=False)      # R2 fix 1
            if twin is None:
                want.remove("contrast")
        fmt2 = rng.choice([f for f in FMTS_A if f.split(":")[0] != fmt.split(":")[0]]) if "format" in want else None
        L2 = len(render(doc, case, fmt2)) if fmt2 else None
        lk = {"pos": "inv", "inv": "pos", "jdg": "jinv"}[qk]
        ltpl = None
        if "ladder" in want:
            ltpl = fb.surface(f"a_ltpl_{lk}", sorted({"pos": Q_POS, "inv": Q_INV, "jinv": Q_JINV}[lk]), rng,
                              split=lat.split)
        # ---- solvers whose misreading changes the outcome (the rest abstain), plus keyword overlap
        sc_code = {m: t["code"] for m, t in sct.items() if t is not None and t["code"] != code}
        kw = self._keyword(sk, base_state, doc)
        if kw and qk != "jdg":      # R2 fix 5: a judge row's keyword reader sees the recorded decision (set below)
            sc_code["keyword_overlap"] = kw
        others = [c for c in SK.CODES if c != code]
        cues = cue_codes(sk, case)

        def sca_for(X_):
            out_ = {}
            for m_, c_ in sc_code.items():
                p_ = c_ == X_
                out_[m_] = ("yes" if p_ else "no") if qk in ("pos", "jdg") else ("no" if p_ else "yes")
            return out_
        # ---- both golds: the named outcome X, the solvers' answers, feasibility (hard: >= 2 solvers wrong)
        opts_g = {}
        for g in ("yes", "no"):
            pos_true = (g == "yes") if qk in ("pos", "jdg") else (g == "no")
            if pos_true:
                X = code
            elif twin is not None:
                X = twin[2]["code"]
            else:
                cands = self._wrong_x(code, sc_code, cues, others, rng)       # R2 fix 1
                X = cands[0]
                if lat.tier == "hard":
                    X = next((c_ for c_ in cands if sum(1 for v in sca_for(c_).values() if v != g) >= 2), X)
            sca = sca_for(X)
            nw = sum(1 for v in sca.values() if v != g)
            feas = not (lat.tier == "hard" and nw < 2)
            rows = self._planned_yn_rows(split, lat, g, qk, want, fmt, fmt2, base_state, code, X, tpl, style, ltpl,
                                         L2)
            qt = (Q_POS if qk == "pos" else Q_INV if qk == "inv" else Q_JDG)[tpl].format(
                doc=sk["doc"], req=sk["req"], X=sk["outcomes"][X])
            crow = [(qt, qk == "inv")] * (1 + sum(1 for v in ("contrast", "format", "attack") if v in want))
            if ltpl:
                crow.append(({"pos": Q_POS, "inv": Q_INV, "jinv": Q_JINV}[lk][ltpl].format(
                    doc=sk["doc"], req=sk["req"], X=sk["outcomes"][X]), lk in ("inv", "jinv")))
            cp = round(self._cue_penalty(split, crow, 0.55), 6)
            opts_g[g] = (self.gb.score(rows), feas, X, sca, cp)
        feas_g = [g for g in opts_g if opts_g[g][1]]
        if not feas_g:
            raise mv.Reject("a_hard_yn", "no gold with 2 wrong shortcuts")
        g = min(feas_g, key=lambda x: (opts_g[x][4], opts_g[x][0], rng.random()))
        other = "no" if g == "yes" else "yes"
        if opts_g[g][0][0] > 0 and opts_g[other][0][0] < opts_g[g][0][0]:
            raise mv.Reject("a_balance", "the balanced gold is not reachable for this item")
        _, _, X, sca, _ = opts_g[g]
        if qk == "jdg":
            case["record"] = X
            base_state = render(doc, case, fmt)
            kw2 = self._keyword(sk, base_state, doc)
            if kw2 and kw2 != code:
                sca = dict(sca, keyword_overlap="yes" if kw2 == X else "no")
        q = (Q_POS if qk == "pos" else Q_INV if qk == "inv" else Q_JDG)[tpl].format(doc=sk["doc"], req=sk["req"],
                                                                                   X=sk["outcomes"][X])
        defs = yn_defs(qk, sk)
        pol = 1 if qk == "inv" else 0
        decisive = self._decisive_strings(sk, doc, case, tr)
        edge_row = ("negation",) if pol else ()
        base = u.add(mv.RowSpec("base", "yn", base_state, q, g, fmt, style, tpl, defs=defs, self_contained=True,
                                polarity=pol, shortcut_answers=sca, decisive=decisive, judge=qk == "jdg",
                                edge=edge_row, role="neg" if pol else "aff"))
        self.expect[base] = {"src": "a", "code": code, "kind": qk, "X": X}
        if twin is not None:
            d2, c2, t2, fname = twin
            if qk == "jdg":
                c2["record"] = X
            s2 = render(d2, c2, fmt)
            g2 = ("yes" if t2["code"] == X else "no") if qk in ("pos", "jdg") else ("no" if t2["code"] == X else "yes")
            sct2 = RC.shortcut_traces(d2, c2, t2)
            sca2 = {}
            for m, t in sct2.items():
                if t is None or t["code"] == t2["code"]:
                    continue
                p = t["code"] == X
                sca2[m] = ("yes" if p else "no") if qk in ("pos", "jdg") else ("no" if p else "yes")
            tw = u.add(mv.RowSpec("contrast", "yn", s2, q, g2, fmt, style, tpl, defs=defs, self_contained=True,
                                  polarity=pol, shortcut_answers=sca2, decisive=self._decisive_strings(sk, d2, c2, t2),
                                  judge=qk == "jdg", edge=edge_row, role="neg" if pol else "aff"), twin_of=base)
            self.expect[tw] = {"src": "a", "code": t2["code"], "kind": qk, "X": X}
            self.stats[f"a_flip_{fname}"] += 1
        if "ladder" in want:
            lq = {"pos": Q_POS, "inv": Q_INV, "jinv": Q_JINV}[lk][ltpl].format(doc=sk["doc"], req=sk["req"],
                                                                              X=sk["outcomes"][X])
            lpol = 1 - pol if lk != "jinv" else 1
            lg = "no" if g == "yes" else "yes"
            lsca = {m: ("no" if v == "yes" else "yes") for m, v in sca.items()}
            lad = u.add(mv.RowSpec("ladder", "yn", base_state, lq, lg, fmt, style, ltpl, defs=yn_defs(lk, sk),
                                   self_contained=True, polarity=lpol, shortcut_answers=lsca, judge=lk == "jinv",
                                   edge=("negation",) if lpol else (), role="neg" if lpol else "aff"))
            u.relate("complement", base, lad)
            self.expect[lad] = {"src": "a", "code": code, "kind": lk, "X": X}
        if "format" in want:
            s3 = render(doc, case, fmt2)
            ft = u.add(mv.RowSpec("format", "yn", s3, q, g, fmt2, style, tpl, defs=defs, self_contained=True,
                                  polarity=pol, shortcut_answers=sca, judge=qk == "jdg", edge=edge_row,
                                  role="neg" if pol else "aff"))
            u.relate("equiv", base, ft)
            self.expect[ft] = {"src": "a", "code": code, "kind": qk, "X": X}
        if "jb" in want:
            jdg = qk == "jdg"
            # the JB row names its own outcome (X_jb), so its truth is balanced on its own strata
            Xs = {}
            Xs[True] = code
            Xs[False] = self._wrong_x(code, sc_code, cues, others, rng)[0]     # R2 fix 1
            if jdg:
                Xs = {True: X, False: X}
            best_t = None
            for t_ in ((True, False) if not jdg else ((code == X),)):
                mm = {"qkind": "jb", "tier": lat.tier, "polarity": 0, "fmt": fmt, "len_bin": mv.len_bin(L),
                      "pack": lat.pack, "tpl": None, "renderer": style, "view": "jb", "src": "a",
                      "target": Xs[t_], "truth": code, "edge": tuple(t for t in lat.edge
                                                                     if t.startswith(("exc:", "missing_info"))),
                      "lenb": L // 750}
                sc_ = self.gb.score([(GoldBalancer.keys(split, mm), t_)])
                if best_t is None or (sc_, rng.random()) < best_t[0]:
                    best_t = ((sc_, rng.random()), t_)
            truth = best_t[1]
            Xj = Xs[truth]
            ydesc, ndesc = jb_texts("jdg" if jdg else "pos", sk, sk["outcomes"][Xj])
            opts, og, wording = fb.jb(ydesc, ndesc, truth, rng, stratum=(lat.split, lat.tier))
            if wording == "family":
                jt, jq = ("jbj1", Q_JBJ["jbj1"]) if jdg else ("jbq1", Q_JB["jbq1"])
            else:
                jt, jq = ("jbjf1", Q_JBJF["jbjf1"]) if jdg else ("jbf1", Q_JBF["jbf1"])
            jq = jq.format(doc=sk["doc"], req=sk["req"], X=sk["outcomes"][Xj])
            if jdg:
                jsca = {m: (opts[0] if c == X else opts[1]) for m, c in sc_code.items()}
            else:
                jsca = {m: (opts[0] if c == Xj else opts[1]) for m, c in sc_code.items()}
            jb = u.add(mv.RowSpec("jb", "jb", base_state, jq, og, fmt, style, jt, options=opts,
                                  shortcut_answers=jsca, judge=jdg))
            self.expect[jb] = {"src": "a", "code": code, "kind": "jb", "X": Xj}
        if "mirror" in want:
            self._mirror_row(u, lat, sk, doc, case, tr, sc_code, base_state, fmt, style, rng)
        if "attack" in want:
            self._attack_row(u, lat, sk, doc, case, base, q, g, defs, fmt, style, tpl, pol, sca, qk, X, rng, pool,
                             render, edge_row)
        fb.commit(u)
        for t_ in self._pending_tok:
            self.placer.commit(t_)
        self._pending_tok = []
        self.gb.add(self._rows_for_balance(u, lat, split))
        self._count_exc(u, lat)

    TEMPT = 0.9
    DOCS_RESCUE = 0.4
    EXCL_RESCUE = 0.35

    def _wrong_x(self, code, sc_code, cues, others, rng) -> list:
        """Candidates (best first) for the outcome a 'no' question names (R2 fix 1): a tempting wrong outcome whose
        surface cue the case file shows (a document not included, an exclusion fact set) when there is one (90%),
        else the outcome most shortcut solvers give (90%), else any other outcome. DOCS / EXCL are never named when
        their cue is absent, so the cue alone does not separate 'yes' from 'no'."""
        allowed = [c for c in others if c not in CUE_CODES or c in cues]
        cnt = Counter(c for c in sc_code.values() if c != code and c in allowed)
        tempt = [c for c in CUE_CODES if c in cues and c != code]
        first = None
        if tempt and rng.random() < self.TEMPT:
            top = max(cnt.get(c, 0) for c in tempt)
            first = rng.choice([c for c in tempt if cnt.get(c, 0) == top])
        elif cnt and rng.random() < 0.9:
            top = max(cnt.values())
            first = rng.choice(sorted(c for c, v in cnt.items() if v == top))
        rest = list(allowed)
        rng.shuffle(rest)
        order = [first or rest[0]] + tempt + sorted(cnt, key=lambda c: -cnt[c]) + rest
        return list(dict.fromkeys(order))

    def _planned_yn_rows(self, split, lat, g, qk, want, fmt, fmt2, state, code, X, tpl, style, ltpl=None, L2=None):
        """(keys, is_yes) of every yes/no row the unit will get if the base gold is g (JB rows balance alone)."""
        L = len(state)
        edge = tuple(t for t in lat.edge if t.startswith(("exc:", "missing_info")))

        def m(view, qkind, pol, f, t, is_yes):
            ln = L2 if (view == "format" and L2) else (L + 220 if view == "attack" else L)
            mm = {"qkind": qkind, "tier": lat.tier, "polarity": pol, "fmt": f, "len_bin": mv.len_bin(ln),
                  "pack": lat.pack, "tpl": t, "renderer": style, "view": view, "src": "a", "target": X,
                  "truth": code, "edge": edge}
            return (GoldBalancer.keys(split, mm), is_yes)
        y = g == "yes"
        pol = 1 if qk == "inv" else 0
        rows = [m("base", "yn", pol, fmt, tpl, y)]
        if "contrast" in want:
            rows.append(m("contrast", "yn", pol, fmt, tpl, not y))
        if "ladder" in want:
            rows.append(m("ladder", "yn", 1 - pol if qk != "jdg" else 1, fmt, ltpl, not y))
        if "format" in want and fmt2:
            rows.append(m("format", "yn", pol, fmt2, tpl, y))
        if "attack" in want:
            rows.append(m("attack", "yn", pol, fmt, tpl, y))
        return rows

    @staticmethod
    def _cue_words(text: str) -> set:
        sys.path.insert(0, str(mv.LEAN))
        import build_v11_fixes as bv
        return set(bv.toks(text)) - bv.STOP

    def _cue_penalty(self, split, rows: list, thr: float = 0.5) -> float:
        """rows: [(instruction, flips)] -> how far the planned rows push any word's answer-flipping share past 50%
        (check_yn2b's cue rule fails a word in >= 30 rows with a share above 60%)."""
        add = defaultdict(lambda: [0, 0])
        for text, flip in rows:
            for w in self._cue_words(text):
                add[w][0] += int(flip)
                add[w][1] += 1
        pen = 0.0
        pt = part_of(split)
        for w, (df, dn) in add.items():
            f0, n0 = self.cue[(pt, w)]
            f1, n1 = f0 + df, n0 + dn
            if n1 >= 15:
                pen += max(0.0, f1 / n1 - thr) - max(0.0, (f0 / n0 - thr) if n0 else 0.0)
        return pen

    def _rows_for_balance(self, u, lat, split):
        pt = part_of(split)
        for r in u.rows:
            flip = r["meta"]["role"] == "neg" or (isinstance(r["meta"]["polarity"], int) and r["meta"]["polarity"] % 2)
            for w in self._cue_words(r["instructions"]):
                self.cue[(pt, w)][0] += int(bool(flip))
                self.cue[(pt, w)][1] += 1
        out = []
        for r in u.rows:
            y = mv._yes(r)
            if y is None:
                continue
            mm = r["meta"]
            exp = self.expect.get(r["rid"], {})
            m = {"qkind": mm["qkind"], "tier": mm["tier"], "polarity": mm["polarity"] if mm["qkind"] == "yn" else 0,
                 "fmt": mm["fmt"], "len_bin": mm["len_bin"], "pack": mm["pack"], "tpl": mm["tpl"],
                 "renderer": mm["renderer"], "view": mm["view"], "src": exp.get("src"), "target": exp.get("X"),
                 "truth": exp.get("code"),
                 "edge": tuple(t for t in (mm["edge"] or "").split(",") if t.startswith(("exc:", "missing_info"))),
                 "lenb": (len(r["state"]) // 750) if mm["qkind"] == "jb" else None}
            out.append((GoldBalancer.keys(split, m), y))
        return out

    def _count_exc(self, u, lat):
        for t in lat.edge:
            if t.startswith("exc:"):
                self.exc_rows[(lat.split, t[4:])] += len(u.rows)

    def _keyword(self, sk, state, doc) -> str | None:
        """keyword_overlap solver: the outcome whose words overlap most with the case file (unique best only)."""
        ctext = state.split("Case file")[-1] if "Case file" in state else state[-3000:]
        cw = words(ctext)
        sc = {c: len(words(sk["outcomes"][c]) & cw) for c in SK.CODES}
        best = max(sc.values())
        top = [c for c, v in sc.items() if v == best]
        return top[0] if best > 0 and len(top) == 1 else None

    def _decisive_strings(self, sk, doc, case, tr) -> tuple:
        """Surface strings of the deciding facts (grounding, SPEC 8.2): the case values the deciding clause reads."""
        out = [case["ref"]]
        ds = doc["dstyle"]
        if tr["fails"]:
            c = RC.clause(doc, tr["fails"][0][1])
            if c["kind"] == "req" and c["gate"] == "time":
                out.append(RR.fdate(case["request"], ds))
            elif c["kind"] == "req" and c["gate"] == "elig":
                out.append(RR.elig_text(sk, case["elig"]))
        else:
            out.append(RR.amount_text(sk, case["amount"]))
        return tuple(out)

    # ------------------------------------------------------------------------------------------ choice units
    def _ch_unit(self, split, rng, pool, lat, u, sk, doc, case, tr, sct, fmt, tpl, ck, style, need, dec, piv):
        fb = self.fb
        code = tr["code"]
        perm = mv.derive_seed(lat.seed, "perm")
        tab = {"table": rng.choice(["md", "pipe"])}.get(style, "md")
        render = lambda d, c, f, plant=None: RR.render_state(d, c, f, plant, tab_layout=tab, perm_seed=perm)  # noqa
        base_state = render(doc, case, fmt)
        L = len(base_state)
        max_rows = min(5, 24000 // max(1, int(L * 1.08)))
        if L > 6000:
            max_rows = min(max_rows, 3)
        want = []
        if ck != "decisive" and rng.random() < 0.62:
            want.append("contrast")
        if rng.random() < 0.25:
            want.append("format")
        if ck == "outcome" and need.get("a_ch", 0) > 0 and rng.random() < 0.2:
            want.append("mirror")
        if need.get("attack", 0) > 0 and rng.random() < 0.24:
            want.append("attack")
        rng.shuffle(want)
        want = want[: max_rows - 1]
        sc_code = {m: t["code"] for m, t in sct.items() if t is not None and t["code"] != code}
        kw = self._keyword(sk, base_state, doc)
        if kw:
            sc_code["keyword_overlap"] = kw
        defs, twin, none_opt, tok = None, None, None, None
        if ck == "outcome" and "contrast" in want:
            twin = self._twin(doc, case, sk, rng, fmt, base_state)
            if twin is None:
                want.remove("contrast")
        sig = tuple(sorted(v for v in want if v in ("contrast", "format", "attack")))
        if ck == "outcome":
            gold_t = sk["outcomes"][code]
            tw_code = twin[2]["code"] if twin else None
            K = fb.surface("a_K_out", [4, 5, 6], rng, split=split)
            pool_codes = [c for c in dict.fromkeys(sc_code.values()) if c not in (code, tw_code)]
            fill = [c for c in SK.CODES if c not in (code, tw_code) and c not in pool_codes]
            rng.shuffle(fill)
            n_other = K - 1 - (1 if tw_code else 0)
            others = (pool_codes + fill)[:n_other]
            pt = part_of(split)
            strata = [(pt, v, tpl, K) for v in ("base",) + tuple(x for x in ("format", "attack") if x in want)]
            pg = self.placer.pick(strata, K, range(K), rng)
            fixed = {pg: gold_t}
            tok = {"pos": [(s_, pg) for s_ in strata]}
            if tw_code:
                pt_ = self.placer.pick([(pt, "contrast", tpl, K)], K, [x for x in range(K) if x != pg], rng)
                fixed[pt_] = sk["outcomes"][tw_code]
                tok["pos"].append(((pt, "contrast", tpl, K), pt_))
            opts = self.placer.arrange(K, fixed, [sk["outcomes"][c] for c in others], rng)
            gold = gold_t
            all_defs = SK.outcome_defs(sk)
            defs = {o: all_defs[o] for o in opts}
            sca = {m: sk["outcomes"][c] for m, c in sc_code.items()}
        elif ck == "decisive":
            lab = lambda cid: RR.option_label(doc, cid, sk)  # noqa: E731
            gold_t = lab(dec)
            sc_dec = {}
            for m, t in sct.items():
                if t is None or t["code"] == code:
                    continue
                p = RC.pivotal(doc, case, m)
                if len(p) == 1:
                    sc_dec[m] = lab(p[0])
            cands = [c["id"] for c in doc["clauses"] if c["kind"] in RC.CANDIDATE_KINDS and c["id"] != dec]
            rng.shuffle(cands)
            # R2 fix 2: one distractor from the gold's own clause group, then the other groups round robin, the group
            # a kind reader ("pick the requirement option") would get most often right first
            kb = self.kinds[part_of(split)]
            gg = clause_group(doc, dec)
            same = [c for c in cands if clause_group(doc, c) == gg]
            pools = defaultdict(list)
            for c in cands:
                if clause_group(doc, c) != gg:
                    pools[clause_group(doc, c)].append(c)
            g_order = sorted(pools, key=lambda k: (-kb.need(k), k))
            rr = []
            while any(pools[k] for k in g_order):
                for k in g_order:
                    if pools[k]:
                        rr.append(pools[k].pop(0))
            fill = [lab(c) for c in same[:1] + rr + same[1:]]
            pt = part_of(split)
            strata = [(pt, v, tpl, 4) for v in ("base",) + tuple(x for x in ("format", "attack") if x in want)]
            wr = fill[:1] + [v for v in sc_dec.values() if v != gold_t] + fill[1:]
            opts, gold, none_opt, tok = self.placer.mirror(gold_t, wr, rng, strata, 4, (pt, "dec"),
                                                            none_text=NONE_CLAUSE)
            sca = dict(sc_dec)
        else:  # amount ranges, ascending, gold rank balanced (and the twin's rank too)
            K = fb.surface("a_K_amt", [4, 5], rng, split=split)
            A = int(tr["granted"])
            # R2 fix 3: a PARTIAL row's request lies above the gold range, so a PARTIAL row takes the top range only
            # when the FULL rows cannot keep that position balanced (its request then shares the top range)
            feas = [r_ for r_ in range(K) if self._widths(sk, A, r_)]
            pt = part_of(split)
            strata = [(pt, v, tpl, K) for v in ("base",) + tuple(x for x in ("format", "attack") if x in want)]
            if code == "PARTIAL" and not self._top_short(strata, K):
                feas = [r_ for r_ in feas if r_ < K - 1]
            if not feas:
                raise mv.Reject("a_bins", "no range width fits")
            r = self.placer.pick(strata, K, feas, rng)
            R_ = int(case["amount"]) if code == "PARTIAL" and r < K - 1 else None
            bins, edges = self._bins(sk, A, K, r, rng, avoid=R_)
            if bins is None:
                raise mv.Reject("a_bins")
            opts, gold = bins, bins[r]
            tok = {"pos": [(s_, r) for s_ in strata]}
            if "contrast" in want:
                rt = self.placer.pick([(pt, "contrast", tpl, K)], K, [x for x in range(K) if x != r], rng)
                twin = self._twin(doc, case, sk, rng, fmt, base_state,
                                  accept=lambda d2, c2, t2: t2["granted"] > 0 and self._bin_of(edges, t2["granted"]) == rt)
                if twin is None:
                    want.remove("contrast")
                else:
                    tok["pos"].append(((pt, "contrast", tpl, K), rt))
            sca = {}
            for m, t in sct.items():
                if t is None or t["granted"] <= 0 or t["granted"] == A:
                    continue
                sca[m] = bins[self._bin_of(edges, t["granted"])]
        if lat.tier == "hard" and sum(1 for v in sca.values() if v is not None and v != gold) < 2:
            raise mv.Reject("a_hard_choice", "fewer than 2 wrong shortcuts")
        q = {"outcome": Q_OUT, "decisive": Q_DEC, "amount": Q_AMT}[ck][tpl].format(
            doc=sk["doc"], req=sk["req"], unit_word=self._unit_word(sk))
        base = u.add(mv.RowSpec("base", "choice", base_state, q, gold, fmt, style, tpl, options=opts, defs=defs,
                                shortcut_answers=sca, decisive=self._decisive_strings(sk, doc, case, tr),
                                none_option=none_opt))
        self.expect[base] = {"src": "a", "code": code, "kind": ck, "gold": gold}
        if twin is not None:
            d2, c2, t2, fname = twin
            s2 = render(d2, c2, fmt)
            sct2 = RC.shortcut_traces(d2, c2, t2)
            if ck == "outcome":
                g2 = sk["outcomes"][t2["code"]]
                sca2 = {m: sk["outcomes"][t["code"]] for m, t in sct2.items()
                        if t is not None and t["code"] != t2["code"]}
            else:
                g2 = opts[self._bin_of(edges, t2["granted"])]
                sca2 = {m: opts[self._bin_of(edges, t["granted"])] for m, t in sct2.items()
                        if t is not None and t["granted"] > 0 and t["granted"] != t2["granted"]}
            tw = u.add(mv.RowSpec("contrast", "choice", s2, q, g2, fmt, style, tpl, options=opts, defs=defs,
                                  shortcut_answers=sca2, decisive=self._decisive_strings(sk, d2, c2, t2)),
                       twin_of=base)
            self.expect[tw] = {"src": "a", "code": t2["code"], "kind": ck, "gold": g2}
            self.stats[f"a_flip_{fname}"] += 1
        if "format" in want:
            fmt2 = rng.choice([f for f in FMTS_A if f.split(":")[0] != fmt.split(":")[0]])
            s3 = render(doc, case, fmt2)
            ft = u.add(mv.RowSpec("format", "choice", s3, q, gold, fmt2, style, tpl, options=opts, defs=defs,
                                  shortcut_answers=sca, none_option=none_opt))
            u.relate("equiv", base, ft)
            self.expect[ft] = {"src": "a", "code": code, "kind": ck, "gold": gold}
        if "mirror" in want:
            self._mirror_row(u, lat, sk, doc, case, tr, sc_code, base_state, fmt, style, rng)
        if "attack" in want:
            self._attack_row(u, lat, sk, doc, case, base, q, gold, defs, fmt, style, tpl, None, sca, ck, None, rng,
                             pool, render, (), options=opts, none_opt=none_opt)
        fb.commit(u)
        self.placer.commit(tok)
        if ck == "decisive":
            grp_of = {lab(c): clause_group(doc, c) for c in cands + [dec]}
            self.kinds[part_of(split)].add(grp_of.get(gold), {grp_of[o] for o in opts if o in grp_of}, len(u.rows))
        if ck == "amount":
            for r_ in u.rows:
                c_ = self.expect.get(r_["rid"], {}).get("code")
                if c_ in SK.GRANTS:
                    self.amt_codes[part_of(split)][c_] += 1
        for t_ in self._pending_tok:
            self.placer.commit(t_)
        self._pending_tok = []
        self.gb.add(self._rows_for_balance(u, lat, split))
        self._count_exc(u, lat)

    AMT_PARTIAL = 0.55

    def _amount_code(self, split, rng) -> str:
        """FULL or PARTIAL for an amount-range latent: the larger deficit against AMT_PARTIAL over the KEPT amount rows
        of this part (dev_iid + dev_holdout together)."""
        c = self.amt_codes[part_of(split)]
        n = sum(c.values()) + 1
        d = {"FULL": (1 - self.AMT_PARTIAL) * n - c["FULL"], "PARTIAL": self.AMT_PARTIAL * n - c["PARTIAL"]}
        best = max(d.values())
        top = [k for k in ("FULL", "PARTIAL") if d[k] >= best - 1e-9]
        return top[rng.randrange(len(top))] if len(top) > 1 else top[0]

    def _top_short(self, strata, K: int) -> bool:
        """The top range position is more than one row behind its share in one of the row's position strata."""
        return any(self.placer.c[s][K - 1] < sum(self.placer.c[s].values()) / K - 1.0 for s in strata)

    def _unit_word(self, sk) -> str:
        return {"money": "amount"}.get(sk["unit"], sk["unit"][1]) if isinstance(sk["unit"], str) else \
            f"number of {sk['unit'][1]}"

    @staticmethod
    def _widths(sk, A: int, r: int) -> list:
        """Range widths that put A in range r with every range bound positive (worst-case offset)."""
        step = RC._amt_step(sk)
        base = (50, 100, 200, 250, 500, 1000, 2000, 2500, 5000) if sk["unit"] == "money" else \
            (1, 2, 3, 5, 10, 15, 30, 60)
        return [w for w in base if w >= step and w % step == 0 and A - (w - 1) - (r - 1) * w > 0 and w <= max(A, 1)]

    def _bins(self, sk, A: int, K: int, r: int, rng, avoid: int | None = None):
        """K ascending range options with A in range r (30%: A exactly on the lower bound of its range). avoid (R2 fix
        3): an amount (the request of a PARTIAL row) that must fall in a higher range than A."""
        if A <= 0:
            return None, None
        ws_all = self._widths(sk, A, r)
        if not ws_all:
            return None, None
        step = RC._amt_step(sk)
        fmt = (lambda x: RR.money(x)) if sk["unit"] == "money" else (lambda x: f"{x:,}")
        unit = "" if sk["unit"] == "money" else f" {sk['unit'][1]}"
        tries = 1 if avoid is None else 40
        for t in range(tries):
            ws = (ws_all[len(ws_all) // 3:] or ws_all) if (avoid is None or t < tries // 2) else ws_all
            w = rng.choice(ws)
            if avoid is None:
                off = 0 if (rng.random() < 0.3 or r == 0) else rng.randrange(0, w, step)
            else:      # the range above A's starts at A - off + w, which must not exceed the request
                lo = max(0, w - (avoid - A))
                lo = -(-lo // step) * step
                if lo >= w:
                    continue
                off = rng.randrange(lo, w, step)
            lo_r = A - off
            edges = [lo_r + (i - r) * w for i in range(1, K)]
            if edges[0] <= 0:
                continue
            bins = [f"less than {fmt(edges[0])}{unit}"]
            for i in range(1, K - 1):
                bins.append(f"{fmt(edges[i - 1])} to {fmt(edges[i] - 1)}{unit}")
            bins.append(f"{fmt(edges[-1])}{unit} or more")
            if self._bin_of(edges, A) != r or len(set(bins)) != K:
                continue
            if avoid is not None and self._bin_of(edges, avoid) == r:
                continue
            return bins, edges
        return None, None

    @staticmethod
    def _bin_of(edges, A) -> int:
        i = 0
        while i < len(edges) and A >= edges[i]:
            i += 1
        return i

    def _mirror_row(self, u, lat, sk, doc, case, tr, sc_code, state, fmt, style, rng):
        fb = self.fb
        code = tr["code"]
        gold_t = sk["outcomes"][code]
        ans = {m: sk["outcomes"][c] for m, c in sc_code.items()}
        fill = [sk["outcomes"][c] for c in SK.CODES if c != code]
        rng.shuffle(fill)
        tpl = fb.surface("a_tpl_mirror", sorted(Q_OUT), rng, split=lat.split)
        K = rng.choice([4, 5])
        pt = part_of(lat.split)
        wr = [v for v in ans.values() if v != gold_t] + fill
        opts, og, none_o, mtok = self.placer.mirror(gold_t, wr, rng, [(pt, "mirror", "mir_" + tpl, K)], K,
                                                   (pt, "mirror"), none_text=NONE_OUTCOME)
        self._pending_tok.append(mtok)
        info = {"none_option": none_o}
        q = Q_OUT[tpl].format(doc=sk["doc"], req=sk["req"])
        all_defs = SK.outcome_defs(sk)
        defs = {o: all_defs[o] for o in opts if o in all_defs}
        rid = u.add(mv.RowSpec("mirror", "choice", state, q, og, fmt, style, "mir_" + tpl, options=opts, defs=defs,
                               shortcut_answers={k: (a if a in opts else None) for k, a in ans.items()},
                               none_option=info["none_option"]))
        self.expect[rid] = {"src": "a", "code": code, "kind": "mirror", "gold": og}

    def _attack_row(self, u, lat, sk, doc, case, base, q, g, defs, fmt, style, tpl, pol, sca, qk, X, rng, pool,
                    render, edge_row, options=None, none_opt=None):
        fb = self.fb
        code = RC.evaluate(doc, case)["code"]
        wrong = [c for c in SK.CODES if c != code]
        if options is None and X is not None and X != code:
            # R2 fix 6: on a yes/no row whose named outcome X is not the outcome, a plant naming a third outcome
            # would back the gold answer; the plant that argues against gold names X itself
            wrong = [X]
        n_am = sum(1 for c in doc["clauses"] if c["kind"] == "amend")
        req = RC.D(case["request"])
        focus = RC.clause(doc, next((c["id"] for c in doc["clauses"] if c["kind"] == "req" and c["gate"] == "time")))
        rule = f"{RR.cap(RR.labels(doc)[focus['id']][1])} no longer applies to {sk['req_pl']} made this year."
        base_fmt = fmt.split(":")[0]
        channel = "email" if base_fmt in ("json", "markdown", "email") else "pasted_doc"
        p = fb.plant(lat, channel, lambda c: f"\"{sk['outcomes'][c]}\"", code, wrong, rule=rule,
                     date_s=RR.fdate(req - dt.timedelta(days=rng.randint(1, 20)), doc["dstyle"]), number=n_am + 1,
                     json_key="correspondence" if base_fmt == "json" else None)
        sender = self._plant_sender(rng, pool)
        st = render(doc, case, fmt, {"text": p.text, "sender": sender})
        card_style = u.row(base)["meta"]["card_style"]
        if options is None:
            rid = u.add(mv.RowSpec("attack", "yn", st, q, g, fmt, style, tpl, defs=defs, card_style=card_style,
                                   self_contained=True, polarity=pol, role="attacked", shortcut_answers=sca,
                                   plant=p, judge=qk == "jdg", edge=edge_row))
        else:
            rid = u.add(mv.RowSpec("attack", "choice", st, q, g, fmt, style, tpl, options=options, defs=defs,
                                   role="attacked", shortcut_answers=sca, plant=p, none_option=none_opt))
        u.relate("inv", base, rid)
        exp = dict(self.expect[base])
        self.expect[rid] = exp

    # ================================================================================================ F1b
    def latent_b(self, split, rng, pool, need):
        fb = self.fb
        tier = self._tier(split, rng)
        pack = fb.surface("b_pack", sorted(NB.PACKS_B), rng, split=split)
        kinds_ = [k for k in NB.KINDS if k != "unit" or NB.PACKS_B[pack]["conv"]]
        kind = fb.surface("b_kind:" + ",".join(kinds_), kinds_, rng,
                          split=split, extra=(tier,))
        fmt = fb.surface("b_fmt", list(FMTS_B), rng, split=split, extra=(tier,))
        if tier == "judge":
            qk = "bjdg"
            tpl = fb.surface("b_tpl_jdg", sorted(QB_JDG), rng, split=split)
        else:
            qk = "binv" if rng.random() < 0.25 else "bpos"
            tpl = fb.surface(f"b_tpl_{qk}", sorted(QB_POS if qk == "bpos" else QB_INV), rng, split=split)
        dstyle = rng.choice(["iso", "long", "us"])
        knobs = {"easy": (None, 0.0, 0.0), "standard": (rng.choice([None, None, "off1"]), 0.35, 0.3),
                 "judge": (rng.choice([None, "off1", "exact"]), 0.35, 0.3),
                 "hard": (rng.choice(["exact", "exact", "off1"]), 0.75, 0.5)}[tier]
        bnd, p_rev, p_asof = knobs
        # truth of the claim: chosen by the balancer below (both are tried)
        want_views = []
        if rng.random() < 0.5:
            want_views.append("contrast")
        if rng.random() < 0.3:
            want_views.append("ladder")
        if rng.random() < 0.25:
            want_views.append("format")
        if need.get("attack", 0) > 0 and rng.random() < 0.2:
            want_views.append("attack")
        fmt2 = rng.choice([f for f in FMTS_B if f.split(":")[0] != fmt.split(":")[0]]) if "format" in want_views \
            else None
        lk = {"bpos": "binv", "binv": "bpos", "bjdg": "bjinv"}[qk]
        ltpl = fb.surface(f"b_ltpl_{lk}", sorted({"bpos": QB_POS, "binv": QB_INV, "bjinv": QB_JINV}[lk]), rng,
                          split=split) if "ladder" in want_views else None
        plan = {"kind": kind, "boundary": bnd, "revised": rng.random() < p_rev,
                "asof": kind in ("threshold", "unit", "about") and rng.random() < p_asof}
        # try both truths; keep the ones that work, then balance
        made = {}
        for truth in ("yes", "no"):
            for _ in range(12):
                try:
                    f = NB.sample(rng, pool, pack, dict(plan, gold=truth))
                except mv.Reject:
                    continue
                made[truth] = f
                break
        if not made:
            raise mv.Reject("b_sample")
        cands = {}
        twins = {}
        for truth, f in made.items():
            for rec in ([None] if qk != "bjdg" else ["SUPPORTED", "NOT SUPPORTED"]):
                f2 = dict(f, record=rec)
                if "contrast" in want_views:
                    st0 = NB.render_state(f2, fmt, dstyle, perm_seed=0)
                    twins[(truth, rec)] = self._nb_twin(f2, rng, fmt, dstyle, st0, 0)
                    if twins[(truth, rec)] is not None and fmt.startswith("log:shuffled"):
                        twins[(truth, rec)] = None   # a shuffled log re-orders lines between the two renders
                if qk == "bjdg":
                    g = "yes" if (rec == "SUPPORTED") == (truth == "yes") else "no"
                elif qk == "binv":
                    g = "no" if truth == "yes" else "yes"
                else:
                    g = truth
                st = NB.render_state(f2, fmt, dstyle, perm_seed=0)
                sca = self._nb_shortcuts(f2, qk, st)
                nw = sum(1 for v in sca.values() if v != g)
                if tier == "hard" and nw < 2:
                    continue
                cands[g] = (f2, truth, sca, twins.get((truth, rec)))
        if not cands:
            raise mv.Reject("b_hard", "no item with 2 wrong shortcuts")
        lat_pack = f"nb_{pack}"
        best = None
        for g, (f2, truth, sca, tw_) in cands.items():
            st = NB.render_state(f2, fmt, dstyle, perm_seed=0)
            wv = [v for v in want_views if v != "contrast" or tw_ is not None]
            rows = self._planned_b_rows(split, tier, lat_pack, g, qk, wv, fmt, fmt2, st, tpl, truth, kind, ltpl)
            sc = self.gb.score(rows)
            if best is None or sc < best[0] or (sc == best[0] and rng.random() < 0.5):
                best = (sc, g, f2, truth, sca, tw_)
        if len(cands) == 1:
            g0 = next(iter(cands))
            g1 = "no" if g0 == "yes" else "yes"
            st = NB.render_state(cands[g0][0], fmt, dstyle, perm_seed=0)
            wv = [v for v in want_views if v != "contrast" or cands[g0][3] is not None]
            alt = self.gb.score(self._planned_b_rows(split, tier, lat_pack, g1, qk, wv, fmt, fmt2, st, tpl,
                                                     "yes" if cands[g0][1] == "no" else "no", kind, ltpl))
            if alt[0] < best[0][0]:
                raise mv.Reject("b_balance", "the balanced gold is not reachable for this item")
        _, g, f, truth, sca, twin_b = best
        edge = {"numeric"}
        if bnd == "exact":
            edge |= {"hc:boundary_exact", "hc:inclusive_exclusive"}
        elif bnd == "off1":
            edge.add("hc:boundary_off1" if kind != "pct" else "hc:boundary_pct")
        if any(i.get("revised") is not None for i in f["items"]):
            edge |= {"hc:amendment_effective", "temporal"}
        if f.get("asof"):
            edge.add("temporal")
        if kind == "unit":
            edge |= {"units"} | ({"hc:currency_rate"} if pack == "retail_sales" else set())
        lat = fb.new_latent(split, lat_pack, f, {"kind": qk, "tpl": tpl}, tier, edge=tuple(sorted(edge)))
        self.facts[lat.latent_id] = {"src": "b", "facts": f, "query": qk}
        u = fb.unit(lat)
        perm = mv.derive_seed(lat.seed, "perm")
        state = NB.render_state(f, fmt, dstyle, perm_seed=perm)
        qtext = ALL_QB[tpl]
        jdg = qk == "bjdg"
        defs = NB.card_defs(f, judge=jdg, inverted=qk == "binv")
        pol = 1 if qk == "binv" else 0
        V = NB.value(f)
        dstr = (NB.claim_text(f, dstyle)[:40],)
        base = u.add(mv.RowSpec("base", "yn", state, qtext, g, fmt, "nb_" + kind, tpl, defs=defs, polarity=pol,
                                shortcut_answers=sca, decisive=dstr, judge=jdg,
                                edge=("negation",) if pol else (), role="neg" if pol else "aff"))
        self.expect[base] = {"src": "b", "truth": truth, "kind": qk, "facts": f}
        if "contrast" in want_views and twin_b is not None:
            tw = twin_b
            if tw is not None:
                f2 = tw[0]
                s2 = NB.render_state(f2, fmt, dstyle, perm_seed=perm)
                t2 = "yes" if NB.truth(f2) else "no"
                g2 = self._nb_gold(qk, t2, f2.get("record"))
                if g2 != g:
                    rid = u.add(mv.RowSpec("contrast", "yn", s2, qtext, g2, fmt, "nb_" + kind, tpl, defs=defs,
                                           polarity=pol, shortcut_answers=self._nb_shortcuts(f2, qk, s2),
                                           judge=jdg, edge=("negation",) if pol else (),
                                           role="neg" if pol else "aff"), twin_of=base)
                    self.expect[rid] = {"src": "b", "truth": t2, "kind": qk, "facts": f2}
        if "ladder" in want_views:
            lpol = 1 - pol if lk != "bjinv" else 1
            ldefs = NB.card_defs(f, judge=lk == "bjinv", inverted=lk == "binv")
            if lk == "bjinv":
                ldefs["yes"], ldefs["no"] = ldefs["no"], ldefs["yes"]
            lg = "no" if g == "yes" else "yes"
            rid = u.add(mv.RowSpec("ladder", "yn", state, ALL_QB[ltpl], lg, fmt, "nb_" + kind, ltpl, defs=ldefs,
                                   polarity=lpol, shortcut_answers={m: ("no" if v == "yes" else "yes")
                                                                    for m, v in sca.items()},
                                   judge=lk == "bjinv", edge=("negation",) if lpol else (),
                                   role="neg" if lpol else "aff"))
            u.relate("complement", base, rid)
            self.expect[rid] = {"src": "b", "truth": truth, "kind": lk, "facts": f}
        if "format" in want_views:
            s3 = NB.render_state(f, fmt2, dstyle, perm_seed=perm)
            rid = u.add(mv.RowSpec("format", "yn", s3, qtext, g, fmt2, "nb_" + kind, tpl, defs=defs, polarity=pol,
                                   shortcut_answers=sca, judge=jdg, edge=("negation",) if pol else (),
                                   role="neg" if pol else "aff"))
            u.relate("equiv", base, rid)
            self.expect[rid] = {"src": "b", "truth": truth, "kind": qk, "facts": f}
        if "attack" in want_views:
            p = fb.plant(lat, "pasted_doc" if fmt.split(":")[0] != "json" else "email",
                         lambda a: "SUPPORTED" if a == "yes" else "NOT SUPPORTED", truth,
                         ["no" if truth == "yes" else "yes"], rule="Revised figures no longer count for this check.",
                         date_s=NB._fd(f["items"][0]["date"], dstyle), number=2,
                         json_key="notes" if fmt.split(":")[0] == "json" else None)
            s4 = NB.render_state(f, fmt, dstyle, plant={"text": p.text, "sender": self._plant_sender(rng, pool)},
                                 perm_seed=perm)
            rid = u.add(mv.RowSpec("attack", "yn", s4, qtext, g, fmt, "nb_" + kind, tpl, defs=defs,
                                   card_style=u.row(base)["meta"]["card_style"], polarity=pol, role="attacked",
                                   shortcut_answers=sca, plant=p, judge=jdg,
                                   edge=("negation",) if pol else ()))
            u.relate("inv", base, rid)
            self.expect[rid] = {"src": "b", "truth": truth, "kind": qk, "facts": f}
        fb.commit(u)
        self.gb.add(self._rows_for_balance(u, lat, split))
        if f.get("ent_stems"):
            self.names |= set(f["ent_stems"])

    @staticmethod
    def _nb_gold(qk, truth, rec) -> str:
        if qk in ("bjdg", "bjinv"):
            ok = (rec == "SUPPORTED") == (truth == "yes")
            return ("yes" if ok else "no") if qk == "bjdg" else ("no" if ok else "yes")
        if qk == "binv":
            return "no" if truth == "yes" else "yes"
        return truth

    def _nb_shortcuts(self, f, qk, state) -> dict:
        out = {}
        for m, t in NB.shortcut_truths(f).items():
            if t is None:
                continue
            out[m] = self._nb_gold(qk, "yes" if t else "no", f.get("record"))
        cl = F_claim_number(f)
        if cl and re.search(r"(?<![\d,.])" + re.escape(cl) + r"(?![\d,]|\.\d)",
                            " ".join(s for _, s in NB.evidence_lines(f, "iso"))):
            out["keyword_overlap"] = self._nb_gold(qk, "yes", f.get("record"))
        return out

    def _planned_b_rows(self, split, tier, pack, g, qk, want, fmt, fmt2, state, tpl, truth, kind, ltpl):
        L = len(state)

        def m(view, pol, f, t, is_yes):
            mm = {"qkind": "yn", "tier": tier, "polarity": pol, "fmt": f, "len_bin": mv.len_bin(L), "pack": pack,
                  "tpl": t, "renderer": "nb_" + kind, "view": view, "src": "b", "target": None, "truth": truth,
                  "edge": ()}
            return (GoldBalancer.keys(split, mm), is_yes)
        y = g == "yes"
        pol = 1 if qk == "binv" else 0
        rows = [m("base", pol, fmt, tpl, y)]
        if "contrast" in want:
            rows.append(m("contrast", pol, fmt, tpl, not y))
        if "ladder" in want:
            rows.append(m("ladder", 1 - pol if qk != "bjdg" else 1, fmt, ltpl, not y))
        if "format" in want and fmt2:
            rows.append(m("format", pol, fmt2, tpl, y))
        if "attack" in want:
            rows.append(m("attack", pol, fmt, tpl, y))
        return rows

    def _nb_twin(self, f, rng, fmt, dstyle, state, perm):
        """Contrast twin of a claim item: the claim figure or one evidence figure moves so the truth flips."""
        t0 = NB.truth(f)
        cands = []
        c = NB.F(f["claim"])
        V = NB.value(f)
        dp = f.get("cdp", f["dp"]) if f["kind"] != "pct" else 1
        unit = Fraction(1, 10 ** dp)
        for k in (1, 2, 3, 5, 10, 50):
            for sgn in (-1, 1):
                f2 = copy.deepcopy(f)
                f2["claim"] = str(c + sgn * unit * k)
                if NB.F(f2["claim"]) > 0:
                    cands.append(f2)
        if f["kind"] != "about":
            f2 = copy.deepcopy(f)
            f2["op"] = {"ge": "gt", "gt": "ge", "le": "lt", "lt": "le"}[f["op"]]
            cands.append(f2)
        rng.shuffle(cands)
        for f2 in cands:
            try:
                if NB.truth(f2) == t0:
                    continue
            except ZeroDivisionError:
                continue
            s2 = NB.render_state(f2, fmt, dstyle, perm_seed=perm)
            if mv.diff_lines(state, s2) <= 3:
                return f2, s2
        return None

    # ================================================================================================ gen2 reuse
    def latent_g(self, split, rng, pool, need):
        import rc_gen2 as G2
        fb = self.fb
        tier = "standard"
        dom = fb.surface("g_dom", list(G2_DOMS), rng, split=split)
        yn_need, ch_need = max(0, need.get("g_yn", 0)), max(0, need.get("g_ch", 0))
        bk = "yn" if rng.random() * (yn_need + ch_need + 1e-9) < yn_need else "ch"
        if bk == "yn":
            qopts = ["out", "out", "inv"] + (["perm"] if dom == "compliance" else ["amt"])
            qk = fb.surface(f"g_qk_{dom}", qopts, rng, split=split)
        else:
            qk = "ch"
        want_q = {"out": "outcome", "inv": "outcome", "amt": "amount", "perm": "permitted", "ch": "choice"}[qk]
        long_ = dom == "home" or rng.random() < 0.42
        lo, hi = (6100, 11500) if long_ else (3200, 5900)
        tag = f"{split}|{fb.n_latents[split]}|{rng.randrange(10 ** 9)}"
        pr = G2.sample_pair(dom, rng, pool, want_q, lo, hi, tag)
        D_ = G2.DOMS[dom]
        docname = G2.DOCNAME[dom]
        fmt = "prose"
        L1 = len(pr["s1"])
        g_extra = None
        if qk != "ch" and L1 * 3 <= 23500 and rng.random() < 0.55:
            g_extra = "ladder" if qk in ("out", "inv") and rng.random() < 0.5 else "format"
        if qk in ("amt", "perm"):
            # either member of the pair can be the base row: take the orientation whose gold keeps the balance
            def gold_of(c, a, c_o, a_o):
                if qk == "perm":
                    return "yes" if c in D_.PERMITTED else "no"
                return "yes" if a > a_o else "no"
            sc = {}
            for flip_ in (False, True):
                c_b, a_b, c_t, a_t = (pr["c2"], pr["a2"], pr["c1"], pr["a1"]) if flip_ else \
                    (pr["c1"], pr["a1"], pr["c2"], pr["a2"])
                g_ = gold_of(c_b, a_b, c_t, a_t)
                sc[flip_] = (self.gb.score(self._planned_g_rows(split, f"g2_{dom}", g_, qk, fmt, len(pr["s1"]),
                                                                None, "gamt1" if qk == "amt" else "gperm1",
                                                                dom, g_extra)), rng.random())
            if min(sc, key=sc.get):
                for a_, b_ in (("s1", "s2"), ("c1", "c2"), ("a1", "a2"), ("dl1", "dl2"), ("P", "P2"), ("C", "C2")):
                    pr[a_], pr[b_] = pr[b_], pr[a_]
        c1, c2, a1, a2 = pr["c1"], pr["c2"], pr["a1"], pr["a2"]
        # gold for the base row and the twin
        if qk in ("out", "inv"):
            # out or inverted, and the gold: the answer-flipping share of every word (incl. the outcome text's
            # words) stays under 50%, then the yes/no balance decides
            best = None
            for qk_ in ("out", "inv"):
                tplset_ = QG_OUT if qk_ == "out" else QG_INV
                tpl_ = sorted(tplset_)[rng.randrange(len(tplset_))]
                for g in ("yes", "no"):
                    pos_true = (g == "yes") if qk_ == "out" else (g == "no")
                    X = c1 if pos_true else c2
                    qtext = tplset_[tpl_].format(docname=docname, X=X)
                    crow = [(qtext, qk_ == "inv"), (qtext, qk_ == "inv")]
                    if g_extra == "ladder":
                        ltext = (QG_INV if qk_ == "out" else QG_OUT)[sorted(QG_INV if qk_ == "out" else QG_OUT)[0]]
                        crow.append((ltext.format(docname=docname, X=X), qk_ == "out"))
                    elif g_extra == "format":
                        crow.append((qtext, qk_ == "inv"))
                    cp = round(self._cue_penalty(split, crow), 6)
                    rows = self._planned_g_rows(split, f"g2_{dom}", g, qk_, fmt, len(pr["s1"]), X, tpl_, dom,
                                                g_extra)
                    sc = (cp, self.gb.score(rows), 0 if qk_ == "out" else 0.5 * rng.random(), rng.random())
                    if best is None or sc < best[0]:
                        best = (sc, qk_, tpl_, g, X)
            _, qk, tpl, g, X = best
            tplset = QG_OUT if qk == "out" else QG_INV
            q = tplset[tpl].format(docname=docname, X=X)
            g2 = ("yes" if c2 == X else "no") if qk == "out" else ("no" if c2 == X else "yes")
            defs = g2_defs("out" if qk == "out" else "inv", docname)
            pol = 1 if qk == "inv" else 0
        elif qk == "amt":
            thr = G2.pick_threshold(rng, min(a1, a2), max(a1, a2))
            if thr is None:
                raise mv.Reject("g2_thr")
            g, g2 = ("yes" if a1 > thr else "no"), ("yes" if a2 > thr else "no")
            if g == g2:
                raise mv.Reject("g2_thr")
            tpl = "gamt1"
            q = QG_AMT[tpl].format(docname=docname, amount_word=G2.AMOUNT_WORD[dom], thr=f"${thr:,}")
            defs, pol, X = g2_defs("amt", docname), 0, None
        elif qk == "perm":
            g = "yes" if c1 in D_.PERMITTED else "no"
            g2 = "yes" if c2 in D_.PERMITTED else "no"
            tpl = "gperm1"
            q = QG_PERM[tpl]
            defs, pol, X = g2_defs("perm", docname), 0, None
        else:
            g, g2, X, pol = c1, c2, None, None
            tpl = fb.surface("g_tpl_ch", sorted(QG_CH), rng, split=split)
            q = QG_CH[tpl].format(docname=docname)
            g_fmt = len(pr["s1"]) * 3 <= 23500 and rng.random() < 0.3
            sig = ("contrast", "format") if g_fmt else ("contrast",)
            Kg = len(D_.CODES)
            pt = part_of(split)
            strata = [(pt, "base", tpl, Kg)] + ([(pt, "format", tpl, Kg)] if g_fmt else [])
            pg = self.placer.pick(strata, Kg, range(Kg), rng)
            pq = self.placer.pick([(pt, "contrast", tpl, Kg)], Kg, [x for x in range(Kg) if x != pg], rng)
            opts = self.placer.arrange(Kg, {pg: c1, pq: c2}, [c for c in D_.CODES if c not in (c1, c2)], rng)
            gtok = {"pos": [(s_, pg) for s_ in strata] + [((pt, "contrast", tpl, Kg), pq)]}
            defs = {o: D_.CODE_DEFS[o] for o in opts}
        lat = fb.new_latent(split, f"g2_{dom}", {"P": "gen2", "dom": dom, "scen": pr["scen"], "flip": pr["flip"]},
                            {"kind": qk}, tier, edge=tuple(sorted({"long_context", "exception", "multi_hop"}
                                                                  if len(pr["s1"]) >= 6000 else
                                                                  {"exception", "multi_hop"})))
        self.facts[lat.latent_id] = {"src": "g", "dom": dom, "pair": {k: v for k, v in pr.items()
                                                                      if k in ("scen", "flip", "c1", "c2", "a1", "a2")}}
        u = fb.unit(lat)
        rend = "g2_" + dom
        if qk == "ch":
            base = u.add(mv.RowSpec("base", "choice", pr["s1"], q, g, fmt, rend, tpl, options=opts, defs=defs))
            tw = u.add(mv.RowSpec("contrast", "choice", pr["s2"], q, g2, fmt, rend, tpl, options=opts, defs=defs),
                       twin_of=base)
        else:
            base = u.add(mv.RowSpec("base", "yn", pr["s1"], q, g, fmt, rend, tpl, defs=defs, polarity=pol,
                                    self_contained=True, role="neg" if pol else "aff",
                                    edge=("negation",) if pol else ()))
            tw = u.add(mv.RowSpec("contrast", "yn", pr["s2"], q, g2, fmt, rend, tpl, defs=defs, polarity=pol,
                                  self_contained=True, role="neg" if pol else "aff",
                                  edge=("negation",) if pol else ()), twin_of=base)
        self.expect[base] = {"src": "g", "gold": g}
        self.expect[tw] = {"src": "g", "gold": g2}
        extra = (g_fmt if qk == "ch" else g_extra is not None)
        if extra:
            if g_extra == "ladder":
                lk = "inv" if qk == "out" else "out"
                lset = QG_INV if lk == "inv" else QG_OUT
                ltpl = fb.surface(f"g_tpl_{lk}", sorted(lset), rng, split=split)
                lq = lset[ltpl].format(docname=docname, X=X)
                lg = "no" if g == "yes" else "yes"
                lad = u.add(mv.RowSpec("ladder", "yn", pr["s1"], lq, lg, fmt, rend, ltpl,
                                       defs=g2_defs(lk, docname), polarity=1 - pol, self_contained=True,
                                       role="neg" if 1 - pol else "aff", edge=("negation",) if 1 - pol else ()))
                u.relate("complement", base, lad)
                self.expect[lad] = {"src": "g", "gold": lg}
            else:
                sj = G2.as_json(pr["s1"], pr["dl1"])
                if qk == "ch":
                    ft = u.add(mv.RowSpec("format", "choice", sj, q, g, "json", rend, tpl, options=opts, defs=defs))
                else:
                    ft = u.add(mv.RowSpec("format", "yn", sj, q, g, "json", rend, tpl, defs=defs, polarity=pol,
                                          self_contained=True, role="neg" if pol else "aff",
                                          edge=("negation",) if pol else ()))
                u.relate("equiv", base, ft)
                self.expect[ft] = {"src": "g", "gold": g}
        fb.commit(u)
        if qk == "ch":
            self.placer.commit(gtok)
        self.gb.add(self._rows_for_balance(u, lat, split))
        self.names |= set(pr["names"])
        self.stats[f"g2_{dom}_{qk}"] += 1

    def _planned_g_rows(self, split, pack, g, qk, fmt, L, X, tpl, dom, extra=None):
        mm = {"qkind": "yn", "tier": "standard", "polarity": 1 if qk == "inv" else 0, "fmt": fmt,
              "len_bin": mv.len_bin(L), "pack": pack, "tpl": tpl, "renderer": "g2_" + dom, "view": "base",
              "src": "g", "target": X, "truth": None, "edge": ()}
        y = g == "yes"
        rows = [(GoldBalancer.keys(split, mm), y), (GoldBalancer.keys(split, dict(mm, view="contrast")), not y)]
        if extra == "format":
            rows.append((GoldBalancer.keys(split, dict(mm, view="format", fmt="json",
                                                       len_bin=mv.len_bin(int(L * 1.04) + 60))), y))
        elif extra == "ladder":
            rows.append((GoldBalancer.keys(split, dict(mm, view="ladder", polarity=1 - mm["polarity"], tpl=None)),
                         not y))
        return rows


def F_claim_number(f) -> str | None:
    """The claim's figure as printed (for the keyword_overlap solver)."""
    p = NB.PACKS_B[f["pack"]]
    if f["kind"] == "pct":
        return None
    dp = f.get("cdp", f["dp"]) if f["kind"] == "unit" else f["dp"]
    try:
        return NB.num(f["claim"], dp)
    except ValueError:
        return None


# ================================================================================================ self-check
def _quoted(text: str) -> str | None:
    m = re.search(r'"([^"]+)"', text)
    return m.group(1) if m else None


def label_from_text(r: dict, defs: dict | None = None):
    """The builder's parse-back label of one RENDERED raw row, from the row alone (state, question, options, card):
    rc_render / rc_numeric read the text back into facts and rc_core / rc_numeric recompute the answer. It is a
    rendering self-check, not the independent decide2 (that is agent E's v3_rule_chain.py). Returns the expected
    gold ('yes' / 'no' / an option), or None for gen2 reuse rows (gen2 checks itself with decide2 + grounding)."""
    m = r["meta"]
    tpl = m["tpl"]
    if m["pack"].startswith("g2_"):
        return None
    if m["pack"].startswith("nb_"):
        f = NB.parse_state(r["state"], m["fmt"], m["pack"][3:], defs or {})
        t = "yes" if NB.truth(f) else "no"
        kind = {"bpos": "bpos", "binv": "binv", "bjdg": "bjdg", "bjin": "bjinv"}[tpl[:4]]
        return RuleChainBuilder._nb_gold(kind, t, f.get("record"))
    skin = m["pack"][2:]
    sk = SK.skin(skin)
    doc, case = RR.parse_state(r["state"], m["fmt"], skin, m["renderer"])
    tr = RC.evaluate(doc, case)
    if tr["n_fails"] >= 2:
        raise ValueError("parsed item has two refusal grounds")
    code = tr["code"]
    text_code = {v: k for k, v in sk["outcomes"].items()}
    if m["qkind"] == "yn":
        if tpl in Q_JDG or tpl in Q_JINV:
            p_ = code == case["record"]
            return ("yes" if p_ else "no") if tpl in Q_JDG else ("no" if p_ else "yes")
        X = text_code[_quoted(r["instructions"])]
        p_ = code == X
        return ("yes" if p_ else "no") if tpl in Q_POS else ("no" if p_ else "yes")
    if m["qkind"] == "jb":
        if tpl in ("jbj1", "jbjf1"):
            truth = code == case["record"]
        else:
            X = text_code[_quoted(r["instructions"]) or _quoted(r["options"][0])]
            truth = code == X
        return r["options"][0] if truth else r["options"][1]
    none_opt = m["none_option"]
    if tpl in Q_OUT or tpl.startswith("mir_"):
        t = sk["outcomes"][code]
        return t if t in r["options"] else none_opt
    if tpl in Q_DEC:
        piv = RC.pivotal(doc, case)
        if len(piv) != 1:
            raise ValueError(f"{len(piv)} pivotal clauses after parse")
        lab = RR._ref_key(next(c for c in doc["clauses"] if c["id"] == piv[0])["label"]).lower()
        for o in r["options"]:
            if o != none_opt and RR._ref_key(o.split(" (")[0]).lower() == lab:
                return o
        return none_opt
    if tpl in Q_AMT:
        A = tr["granted"]
        for o in r["options"]:
            mm = re.fullmatch(r"less than \$?([\d,]+).*", o)
            if mm and A < int(mm.group(1).replace(",", "")):
                return o
            mm = re.fullmatch(r"\$?([\d,]+)(?: [a-z]+)? to \$?([\d,]+).*", o)
            if mm and int(mm.group(1).replace(",", "")) <= A <= int(mm.group(2).replace(",", "")):
                return o
            mm = re.fullmatch(r"\$?([\d,]+)(?: [a-z]+)? or more", o)
            if mm and A >= int(mm.group(1).replace(",", "")):
                return o
        raise ValueError("amount in no range")
    raise ValueError(f"unknown template {tpl}")


def self_check_row(r: dict, exp: dict | None = None, defs: dict | None = None) -> tuple[bool, str]:
    if r["meta"]["pack"].startswith("g2_"):
        return (exp is None or r["gold"] == exp["gold"]), "gen2"
    want = label_from_text(r, defs)
    return want == r["gold"], f"{want} vs {r['gold']}"


def self_check_all(fb: mv.FamilyBuilder, b: "RuleChainBuilder | None" = None, rows=None, defs_lookup=None) -> dict:
    bad = []
    n = 0
    for r in rows if rows is not None else fb.rows:
        n += 1
        d = defs_lookup(r) if defs_lookup else fb.defs.get(r["meta"]["defs"])
        try:
            ok, why = self_check_row(r, (b.expect.get(r["rid"]) if b else None), d)
        except Exception as e:  # noqa: BLE001
            ok, why = False, f"parse error {type(e).__name__}: {str(e)[:80]}"
        if not ok:
            bad.append((r["rid"], why))
    return {"rows": n, "bad": len(bad), "examples": bad[:12], "ok": not bad}


# ================================================================================================ reports
def cue_report(rows) -> dict:
    sys.path.insert(0, str(mv.LEAN))
    import build_v11_fixes as bv
    items = [(r["instructions"], r["meta"]["role"] == "neg" or (isinstance(r["meta"]["polarity"], int)
                                                                 and r["meta"]["polarity"] % 2 == 1)) for r in rows]
    sh = {w: v for w, v in bv.cue_shares(items).items() if v[1] >= 30}
    worst = sorted(sh.items(), key=lambda kv: -kv[1][0])[:5]
    return {"worst": [(w, round(s, 3), n) for w, (s, n) in worst], "ok": all(s <= 0.6 for _, (s, _) in sh.items())}


def banned_report(rows) -> dict:
    pat = re.compile(r"\b(right|wrong|correct|incorrect|accurate|inaccurate|mistaken|reply|agreed|disagree|undercut|"
                     r"debate)\b|two notes", re.I)
    hits = [r["rid"] for r in rows if pat.search(r["instructions"]) or any(pat.search(o) for o in r["options"]
                                                                          if r["meta"]["qkind"] != "yn")]
    return {"hits": len(hits), "examples": hits[:5], "ok": not hits}


def tfidf_probe(train, test) -> dict:
    try:
        from sklearn.feature_extraction.text import TfidfVectorizer
        from sklearn.linear_model import LogisticRegression
    except ImportError:  # pragma: no cover
        return {"skipped": True, "ok": True}
    tr = [r for r in train if r["meta"]["qkind"] in ("yn", "jb")]
    te = [r for r in test if r["meta"]["qkind"] in ("yn", "jb")]
    out = {}
    for field in ("state_question", "question"):
        def txt(r):
            return r["instructions"] if field == "question" else r["state"] + "\n" + r["instructions"]
        vec = TfidfVectorizer(ngram_range=(1, 2), min_df=2, max_features=200000, sublinear_tf=True)
        X = vec.fit_transform([txt(r) for r in tr])
        y = [mv._yes(r) for r in tr]
        clf = LogisticRegression(max_iter=3000, C=1.0)
        clf.fit(X, y)
        pred = clf.predict(vec.transform([txt(r) for r in te]))
        yt = [mv._yes(r) for r in te]
        out[field] = round(sum(int(a == b) for a, b in zip(pred, yt)) / max(1, len(yt)), 4)
    out["n_test"] = len(te)
    out["ok"] = out["state_question"] <= 0.60 and out["question"] <= 0.55
    return out


def counts(rows) -> dict:
    c = lambda f: dict(sorted(Counter(f(r) for r in rows).items(), key=lambda kv: str(kv[0])))  # noqa: E731
    src = lambda r: "g2" if r["meta"]["pack"].startswith("g2_") else ("F1b" if r["meta"]["pack"].startswith("nb_")
                                                                       else "F1a")
    return {"rows": len(rows), "latents": len({r["meta"]["latent_id"] for r in rows}), "by_source": c(src),
            "view": c(lambda r: r["meta"]["view"]), "qkind": c(lambda r: r["meta"]["qkind"]),
            "fmt": c(lambda r: r["meta"]["fmt"].split(":")[0]), "tier": c(lambda r: r["meta"]["tier"]),
            "label": c(lambda r: r["gold"] if r["meta"]["qkind"] == "yn" else
                       ("jb_first" if r["meta"]["qkind"] == "jb" and r["gold"] == r["options"][0] else
                        "jb_second" if r["meta"]["qkind"] == "jb" else "choice")),
            "len_bin": c(lambda r: r["meta"]["len_bin"]),
            "pack": c(lambda r: r["meta"]["pack"]), "renderer": c(lambda r: r["meta"]["renderer"]),
            "yes_share": mv.summary(rows)["yes_share"]}


def report(fb: mv.FamilyBuilder, b: RuleChainBuilder) -> dict:
    out = {}
    for part in ("train", "dev"):
        rows = fb.rows_for(part)
        rids = {r["rid"] for r in rows}
        rels = [x for x in fb.rels if x["a"] in rids]
        chk = mv.run_checks(rows, rels)
        out[part] = {"counts": counts(rows), "checks": chk, "self_check": self_check_all(fb, b, rows),
                     "cue": cue_report(rows), "banned": banned_report(rows),
                     "relations": dict(Counter(x["type"] for x in rels))}
        f1a = [r for r in rows if r["meta"]["pack"].startswith("a_")]
        out[part]["f1a_len_share_6k_12k"] = round(sum(1 for r in rows if not r["meta"]["pack"].startswith("nb_")
                                                      and 6000 <= len(r["state"]) < 12000) /
                                                  max(1, sum(1 for r in rows if not r["meta"]["pack"]
                                                             .startswith("nb_"))), 4)
        out[part]["f1a_rows"] = len(f1a)
    tr, dv = fb.rows_for("train"), fb.rows_for("dev")
    out["tfidf_train_to_dev"] = tfidf_probe(tr, dv)
    out["exception_rows"] = {f"{k[0]}:{k[1]}": v for k, v in sorted(b.exc_rows.items())}
    out["decisive_position_thirds"] = dict(b.decisive_pos)
    out["stats"] = dict(b.stats.most_common())
    out["rejects"] = dict(fb.rejects.most_common(30))
    out["repair"] = getattr(b, "repair_log", None)
    try:
        import v3_rule_chain as v3  # agent E's independent decide2 (SPEC 8.1)
        out["decide2"] = {p: mv.verify_labels(fb.rows_for(p), v3.decide2_row) for p in ("train", "dev")}
    except ImportError:
        out["decide2"] = {"status": "golden_src/gen3/v3_rule_chain.py not written yet (agent E)"}
    return out


# ================================================================================================ entry points
def build(splits=("train", "dev_iid", "dev_holdout"), check_tz=True, raw_dir=None, defs_dir=None, manifest=None,
          use_gen2=False, scale=1.0, repair_parts=True) -> tuple[mv.FamilyBuilder, RuleChainBuilder]:
    fb = mv.FamilyBuilder(KEY, generator_file=__file__, raw_dir=raw_dir, defs_dir=defs_dir, manifest=manifest,
                          check_tz=check_tz)
    b = RuleChainBuilder(fb, use_gen2=use_gen2, scale=scale)
    for s in splits:
        b.build_split(s)
    if repair_parts:
        import rc_repair
        keep_rows, keep_rels = [], []
        b.repair_log = {}
        for part in ("train", "dev"):
            rows = fb.rows_for(part)
            if not rows:
                continue
            rids = {r["rid"] for r in rows}
            rels = [x for x in fb.rels if x["a"] in rids]
            rows2, rels2, log = rc_repair.repair(rows, rels)
            b.repair_log[part] = {k: v for k, v in log.items() if k != "steps"}
            keep_rows += rows2
            keep_rels += rels2
        keep = {r["rid"] for r in keep_rows}
        fb.rows = [r for r in fb.rows if r["rid"] in keep]
        fb.rels = [x for x in fb.rels if x["a"] in keep and x["b"] in keep]
    return fb, b


def devx_latents(n: int = 100, check_tz: bool = True) -> list[dict]:
    """dev_holdout-distribution F1a latents for reviewer R (SPEC 6): the devx seed stream (train seed + 3e9), the devx
    name pool, the held-out document family (school transport) and/or the held-out style (contract). Nothing is
    written. Each item: {latent_id, query: {kind: outcome | outcome_is | decisive, target?}, facts: {doc, case},
    gold}; gold comes from rc_core.decide (outcome code text, or yes/no for outcome_is). R renders `facts` with its
    own renderers and must reproduce the labels with its own parse-back (SPEC 8.1)."""
    fb = mv.FamilyBuilder(KEY, generator_file=__file__, check_tz=check_tz)
    rng = fb.rng("devx")
    pool = fb.names("devx")
    bld = RC.Builder(mv.rng_for(KEY, "devx", "rc"), pool)
    out = []
    i = 0
    while len(out) < n and i < 50 * n:
        i += 1
        mode = ("skin", "style", "both", "skin", "style")[i % 5]
        skin = SK.HOLDOUT_SKIN if mode in ("skin", "both") else rng.choice(SKINS_V.kept)
        style = RR.HOLDOUT_STYLE if mode in ("style", "both") else rng.choice(STYLES_V.kept)
        tier = ("easy", "standard", "judge", "hard")[i % 4]
        kn = TIER_KNOBS[tier]
        grp = (None, "deny_allow", "allow_deny", "near_miss")[i % 4]
        code = rng.choice(FEASIBLE[grp] if grp != "allow_deny" else FEASIBLE["allow_deny"])
        plan = {"code": code, "group": grp, "n_distract": rng.randint(*kn["nd"]), "phr": "ho",
                "amend": rng.choice(["in_force", "not_yet", "withdrawn", "superseded"])
                if rng.random() < kn["amend"] else None,
                "business": rng.random() < kn["business"], "defn": rng.random() < kn["defn"],
                "decoy": rng.random() < kn["decoy"], "prec_case": code in SK.GRANTS and rng.random() < kn["prec"],
                "prec": rng.choice(["specific", "later", "lower", "named"])}
        if rng.random() < kn["boundary"]:
            plan["boundary"] = rng.choice(["exact", "off1"])
            plan["boundary_gate"] = rng.choice(["elig", "time"] + (["amount"] if code in SK.GRANTS else []))
        try:
            doc, case = bld.sample(skin, style, plan)
        except mv.Reject:
            continue
        g, tr = RC.decide(doc, case)
        if mv.is_undefined(g) or g != code or set(RC.groups(doc, case, tr)) != ({grp} if grp else set()):
            continue
        if weekday_sensitive(doc, case, g):          # R2 fix 4
            continue
        sk = SK.skin(skin)
        kind = ("outcome", "outcome_is", "outcome_is", "decisive")[len(out) % 4]
        q = {"kind": kind}
        if kind == "outcome":
            gold = sk["outcomes"][code]
        elif kind == "outcome_is":
            yes = len(out) % 8 < 4
            X = code if yes else rng.choice([c for c in SK.CODES if c != code])
            q["target"] = sk["outcomes"][X]
            gold = "yes" if yes else "no"
        else:
            piv = RC.pivotal(doc, case)
            if len(piv) != 1 or amount_pivots(doc, case) != piv:     # R2 fix 4
                continue
            gold = piv[0]
            q["candidates"] = [c["id"] for c in doc["clauses"] if c["kind"] in RC.CANDIDATE_KINDS]
        out.append({"latent_id": f"f1-dx-{len(out):06d}", "tier": tier, "query": q,
                    "facts": {"doc": doc, "case": case}, "gold": gold, "outcomes": dict(sk["outcomes"])})
    return out


def train_latents_for_f4(n: int = 400) -> list[dict]:
    """F1 train program decisions for F4(b) (SPEC 5 F4: 750 rows on program decisions from F1/F2/F3/F6 train
    latents). Each item: {latent_id, proposition, truth}, e.g. 'the outcome of this application is "..."'. The
    latent ids are those of the written train rows (re-derived by a full deterministic rebuild)."""
    fb, b = build()
    written = {r["meta"]["latent_id"] for r in fb.rows_for("train")}
    out = []
    for lid, f in sorted(b.facts.items()):
        if f["src"] != "a" or lid not in written:
            continue
        sk = SK.skin(f["doc"]["skin"])
        out.append({"latent_id": lid, "skin": f["doc"]["skin"], "code": f["code"],
                    "proposition": f"the outcome of this {sk['req']} under the {sk['doc']} is "
                                   f"\"{sk['outcomes'][f['code']]}\"", "truth": True})
        if len(out) >= n:
            break
    return out


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--write", action="store_true", help="write rows, relations, defs and MANIFEST records")
    ap.add_argument("--overwrite", action="store_true", help="replace this builder's earlier output")
    ap.add_argument("--report", default=None, help="write the check report JSON here (outside data/)")
    ap.add_argument("--with-gen2", action="store_true",
                    help="also build the gen2_long_policy reuse rows (off by default: their boilerplate shares 12-word "
                         "runs with golden_dev's gd_gen2_long_policy rows, so check_yn2b 7.2 drops them)")
    ap.add_argument("--scale", type=float, default=1.0, help="scale every row target (tests)")
    ap.add_argument("--devx-out", action="store_true",
                    help="only write the 100 devx latents for reviewer R to yn2b/f1_devx_latents.json (+ MANIFEST)")
    a = ap.parse_args(argv)
    if a.devx_out:
        xs = devx_latents(100)
        path = mv.LEAN / "yn2b" / "f1_devx_latents.json"
        if path.exists() and not a.overwrite:
            raise SystemExit(f"{path} exists; pass --overwrite")
        path.write_text(json.dumps({"key": KEY, "split": "devx", "n": len(xs), "latents": xs}, indent=1,
                                   ensure_ascii=False, default=str) + "\n")
        mv.manifest_append({"tool": f"golden_src/gen3/{Path(__file__).name}", "key": KEY, "part": "devx_latents",
                            "path": mv._rel(path), "rows": len(xs), "sha256": mv.sha256_file(path)})
        print(json.dumps({str(path): mv.sha256_file(path)}, indent=1))
        return
    fb, b = build(use_gen2=a.with_gen2, scale=a.scale)
    rep = report(fb, b)
    summ = {p: {"ok": rep[p]["checks"]["ok"], "self_check": rep[p]["self_check"]["ok"], "cue": rep[p]["cue"],
                "banned": rep[p]["banned"]["ok"], "counts": rep[p]["counts"],
                "failed": [k for k, x in rep[p]["checks"].items() if isinstance(x, dict) and x.get("ok") is False]}
            for p in ("train", "dev")}
    print(json.dumps(summ, indent=1, default=str))
    print("tfidf", json.dumps(rep["tfidf_train_to_dev"]), "exc_rows", json.dumps(rep["exception_rows"]),
          "decisive thirds", json.dumps(rep["decisive_position_thirds"]))
    print("rejects", json.dumps(rep["rejects"]))
    if a.report:
        Path(a.report).write_text(json.dumps(rep, indent=1, default=str))
    if a.write:
        ok = all(rep[p]["checks"]["ok"] and rep[p]["self_check"]["ok"] and rep[p]["banned"]["ok"]
                 and rep[p]["cue"]["ok"] for p in ("train", "dev"))
        if not ok:
            raise SystemExit("checks failed: nothing written")
        out = fb.write(parts=("train", "dev"), overwrite=a.overwrite)
        npath = mv.LEAN / "yn2b" / f"names_{KEY}.json"
        if npath.exists() and not a.overwrite:
            raise SystemExit(f"{npath} exists; pass --overwrite")
        npath.write_text(json.dumps({f"gd_{KEY}": sorted(b.names)}, indent=1) + "\n")
        mv.manifest_append({"tool": f"golden_src/gen3/{Path(__file__).name}", "key": KEY, "part": "names",
                            "path": mv._rel(npath), "rows": len(b.names), "sha256": mv.sha256_file(npath),
                            "revision": fb.revision})
        out[str(npath)] = mv.sha256_file(npath)
        print(json.dumps(out, indent=1))


if __name__ == "__main__":
    main()
