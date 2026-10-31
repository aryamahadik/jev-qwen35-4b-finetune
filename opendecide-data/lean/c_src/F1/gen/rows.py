"""F1 row builder: one selection set (group) = a base row + its relation-unit rows + its contrast twins.

Questions (G0 F1 v7 1.1): Q1 outcome choice, Q2 outcome + basis choice, Q3 yes/no (aff / neg / dneg), Q4 inverted
choice. Balance (section 8) is reached by rejection inside the sampler (quotas below), never by relabelling.
Relation units (section 7): U-neg {aff, neg (complement), dneg (equiv)}, U-inert {base, M4 / M5 variant (equiv)},
U-attack {clean, attacked (inv)}; contrast twins (own call_id): boundary flip, M6 repeal, M7 effective date move,
open-world reveal; a twin is kept only if the row gold flips.
"""
from __future__ import annotations

import copy
import math
import random
from collections import Counter, defaultdict
from decimal import Decimal

import balance as BAL
import lexicon as L
import r2bal as R2
import samplers as SM
import solver_a as A
from model import Attr, Case, Inert, Item, Lit, Notice, Rule, Struct
from solver_a import CBD, Reject

DEPTH_TARGET = {1: 0.22, 2: 0.33, 3: 0.28, 4: 0.17}
# r3 pass C2 (G10 depth, qc pool 25.1 / 36.1 / 25.2 / 13.5% at depth 1-4, cand 14.5% depth 4): the deep-capable Q2
# cards (ceiling >= 4; 8 of 17) take a deeper table, since the other 9 Q2 cards cannot pass depth 2-3 and the family
# share of depth 4 runs ~3 pp under G0 8's 17%; realized shares sit under the table (pass B: ~75% of the depth-4 plan)
DEPTH_Q2_DEEP = {4: {1: 0.10, 2: 0.22, 3: 0.33, 4: 0.35}, 5: {1: 0.08, 2: 0.18, 3: 0.34, 4: 0.40}}
# r3 pass C2 v4 (agent 5; G10 depth in the qc pool only: pass B 25.1% depth 1 (max 25) / 13.5% depth 4 (min 14),
# cand 23.2 / 14.5% passes): the qc set scales every card to 5200/8100 of its rows (min 30), so the non-Q2 cards'
# per-card quota slack (1.5 rows per level) weighs ~1.6x more and settles in depth 1. The qc set's deep-capable Q2
# cards carry the difference (cand C2 v3 chain: realized depth 4 ~8 pp under this table, depth 1 ~10 pp over it).
DEPTH_Q2_DEEP_QC = {4: {1: 0.05, 2: 0.15, 3: 0.30, 4: 0.50}, 5: {1: 0.04, 2: 0.12, 3: 0.29, 4: 0.55}}
Q2_BAND_BUDGET = 40   # r3 pass C2: Q2 band refusals in a row per (card, band key) before the soft factor applies
# r3 pass C2 v5 (agent 5): sources whose longest-gold band re-arms after an escape and whose non-Q2 pool deviation
# seeds the chains (G10 src cells with the least slack: cand T n ~400 / CBD ~280, qc T ~235 / CBD ~170 rows, so
# 2 pp = 3-8 hits); ONE (n ~2,000) and D keep the C2 v3 rule (smoke: seeding / re-arming ONE capped F1-C041 at
# 29 of 40 rows in 600 s, 34k band refusals)
Q2_REARM_SRC = ("T", "CBD")
# r3 pass C2 v7 (agent 8; G7 option n-grams, check round 4: cand 'opt:97' = rule id 97 gold 27 vs 10.7 exp over 15 Q2
# cards, base rows 21 of 56; qc 'code jxb' = one card's special code gold 23 vs 10.0): per-basis bands on the Q2 keep
# step. ("g7rid", id): gold basis is rule id minus that id's shown option share, carried along the chain (ids are drawn
# per row, so the chain total is the pool-level n-gram count); ("g7code", card, letter): the same for each special code
# (card-fixed text) over the card. Same refusal budget / escape rule as the G10 aggregate bands, wider dead bands.
Q2_G7_BAND = {"g7rid": 1.5, "g7code": 1.0}
# r3 pass C2 v8 (agent 10; G10 twins_units, cand contrast-set share 0.187 < 0.20): the C2 v3-v7 hard bands also sat in
# the Q2 twin keep step (twin_gold_ok -> q2_keepf). A twin gets one keep draw where a base row gets dozens, so the bands
# refused most Q2 twins (cand Q2 cards: contrast rows 94 of 1,247 = 7.5%; pass B ~25%). A Q2 twin now takes the
# composition-first prior and the soft class factor only (no band refusal, no band counters touched); its booked
# deviations are pulled back by the later base rows of the chain (bands unchanged). The qc set keeps its C2 v7 Q2
# shards (qc contrast share passes), so the rule is per set (seed_key '<set>|<card>').
Q2_TWIN_SOFT_SETS = ("cand",)
# r3 pass D (agent 10; G10 depth, qc pool only: non-deep shares 25.1 / 36.0 / 24.8 / 14.1% vs 22 / 33 / 28 / 17, tol 3 pp;
# cand 23.5 / 35.4 / 26.3 / 14.8 passes). The per-card soft depth quota lets each level run 1.5 rows over its share
# (SoftQuota slack); the easy shallow levels sit at that edge on every card. qc cards are built at 5200/8100 of their
# cand size (min 30), so the same 1.5 rows weigh ~1.6x more in qc shares (agent 5's diagnosis). The qc set's non-Q2
# cards now scale the depth slack by the same factor (1.5 x 5200/8100 = 0.96 rows), so qc settles where cand does.
# Q2 cards keep 1.5 (their qc shards stay C2 v7); top-up sets ('topup', 'vqctop') are unchanged.
DEPTH_SLACK_QC = 1.5 * 5200 / 8100


class Quota:
    """Deficit acceptor: accept a category while its count stays within target share * (n+1) + slack."""

    def __init__(self, targets: dict, slack=1.5):
        self.t = dict(targets)
        self.c = Counter()
        self.n = 0
        self.slack = slack

    def ok(self, cat):
        if cat not in self.t:
            return True
        return self.c[cat] + 1 <= self.t[cat] * (self.n + 1) + self.slack

    def add(self, cat):
        self.c[cat] += 1
        self.n += 1


class Trackers:
    """Generation-time steering across one build (per sampler where the spec checks per sampler)."""

    def __init__(self):
        self.depth = defaultdict(lambda: Quota(DEPTH_TARGET, slack=3))
        self.boundary = defaultdict(lambda: Quota({"at": 0.31, "below": 0.345, "above": 0.345}, slack=2))
        self.position = defaultdict(lambda: defaultdict(Counter))
        self.s6_A = Counter()
        self.yesbad = Counter()
        self.role_yes = defaultdict(Counter)
        self.amend = Counter()

    @staticmethod
    def _ter(n, pos):
        return min(2, int(3 * (pos - 1) / max(1, n)))

    def pos_ok(self, sampler, n, pos):
        c = self.position[sampler]["ter"]
        t = self._ter(n, pos)
        return c[t] <= min(c[0], c[1], c[2]) + 2

    def pos_add(self, sampler, n, pos):
        self.position[sampler]["ter"][self._ter(n, pos)] += 1


# ---------------------------------------------------------------- literal helpers

def satisfy_lit(lit: Lit, a: Attr, want: bool, rng):
    """A value of a's field that gives the literal the wanted truth value (None if impossible)."""
    op, args = lit.op, lit.args
    if a.type == "bool":
        return args[0] if want else (not args[0])
    if a.type == "cat":
        inside = [v for v in a.values if v in args]
        outside = [v for v in a.values if v not in args]
        pool = (inside if op == "in" else outside) if want else (outside if op == "in" else inside)
        return rng.choice(pool) if pool else None
    step = a.step if a.type == "num" else 1
    lo, hi = a.lo, a.hi
    c = lit.canon({lit.attr: a})
    cop, cargs = c[1], c[2]
    if cop == "ge":
        rng_ = (cargs[0], hi) if want else (lo, cargs[0] - step)
    elif cop == "le":
        rng_ = (lo, cargs[0]) if want else (cargs[0] + step, hi)
    elif cop == "between":
        if want:
            rng_ = (cargs[0], cargs[1])
        else:
            rng_ = (lo, cargs[0] - step) if rng.random() < 0.5 else (cargs[1] + step, hi)
    else:
        return None
    x0, x1 = rng_
    if x1 < x0:
        return None
    n = int((x1 - x0) / step)
    if rng.random() < 0.5:
        k = rng.choice([0, n]) if n > 0 else 0
    else:
        k = rng.randint(0, n)
    return x0 + step * k


def satisfy_item(it: Item, S: Struct, vals: dict, want: bool, rng, fixed: set):
    """Assign field values so the item gets the wanted truth value; returns False if a fixed field conflicts."""
    def setv(m, w):
        a = S.attrs[m.attr]
        if m.attr in fixed:
            return A.lit_val(m, S.attrs, vals) == w
        v = satisfy_lit(m, a, w, rng)
        if v is None:
            return False
        vals[m.attr] = v
        fixed.add(m.attr)
        return True
    k = it.kind
    if k == "lit":
        return setv(it.mem[0], want)
    if k == "not":
        return setv(it.mem[0], not want)
    mem = list(it.mem)
    if k == "all":
        if want:
            return all(setv(m, True) for m in mem)
        i = rng.randrange(len(mem))
        return setv(mem[i], False)
    if k in ("any", "or"):
        if want:
            i = rng.randrange(len(mem))
            return setv(mem[i], True)
        return all(setv(m, False) for m in mem)
    if k == "xor":
        if want:
            i = rng.randrange(2)
            return setv(mem[i], True) and setv(mem[1 - i], False)
        w = rng.random() < 0.5
        return setv(mem[0], w) and setv(mem[1], w)
    if k == "kofn":
        order = list(range(len(mem)))
        rng.shuffle(order)
        t = it.k if want else it.k - 1
        ok = True
        for j, i in enumerate(order):
            ok = ok and setv(mem[i], j < t)
        return ok
    return False


def all_lit_occurrences(S: Struct, rules: dict | None = None):
    """(rule, item, literal) occurrences of the rules (in force when rules is given, else base + notice rules)."""
    out = []
    src = [r for r, d, s in rules.values()] if rules is not None else \
        list(S.rules) + [n.rule for n in S.notices if n.rule is not None]
    for r in src:
        for it in r.all_items():
            for m in it.mem:
                out.append((r, it, m))
    return out


def decisive_literals(S: Struct, vals: dict, notrec=frozenset()):
    """Numeric / date literal occurrences whose truth value, flipped alone, changes the final outcome (F1R1-A16)."""
    base = A.solve_closed(S, vals, notrec)
    if base["src"] == "M":
        return [], base
    out = []
    for r, it, m in all_lit_occurrences(S, base["rules"]):
        a = S.attrs[m.attr]
        if a.type not in ("num", "date"):
            continue
        cur = A.lit_val(m, S.attrs, vals)
        A.set_override({id(m): not cur})
        try:
            alt = A.solve_closed(S, vals, notrec)
        except Reject:
            alt = None
        finally:
            A.set_override(None)
        if alt is not None and alt["final"] != base["final"]:
            out.append(m)
    return out, base


def threshold_of(m: Lit, v):
    if m.op in ("between", "fromto"):
        a, b = m.args
        return a if abs(v - a) <= abs(v - b) else b
    return m.args[0]


def boundary_class(S: Struct, vals: dict, decisive, order_key=None):
    if not decisive:
        return None
    best = None
    for m in decisive:
        a = S.attrs[m.attr]
        v = vals[m.attr]
        T = threshold_of(m, v)
        step = a.step if a.type == "num" else 1
        d = abs(v - T) / step
        if d == 0:
            return "at"
        if best is None or d < best[0]:
            best = (d, m, v, T)
    d, m, v, T = best
    if d == 1:
        return "below" if v < T else "above"
    return "far"


# ---------------------------------------------------------------- core draws

class RowBuilder:
    def __init__(self, card, pack, tr: Trackers, seed_key, held_out=False):
        self.seed_key = seed_key   # r3 pass C2 v4: '<set>|<card id>' (set-specific Q2 depth table)
        self.card = card
        self.pack = pack
        self.tr = tr
        self.held_out = held_out
        self.rng = random.Random(hash(seed_key) & 0xFFFFFFFF)
        import common
        self.rng = common.rng_for("rows", seed_key)
        self.sampler = card["sampler"] if not held_out else card.get("dev_sampler", card["sampler"])
        self.q1_counts = Counter()
        # r3 (A28 longest option per gold source): per-card (gold source, gold-is-longest) row quotas from
        # cardfix_r3_plan.json, set by gen_card for the set being built; None = no quota
        self.srcq = None
        self.srcq_cnt = Counter()
        # r3 pass B (G10 role rate / Q2 code share / longest per source on Q2): per-card running deviations on emitted
        # Q2 rows, (bucket, option class) gold minus m_c / k and (bucket, gold source) longest-gold minus 1 / k; the
        # composition-first keep step is scaled by a factor of these card-history deviations only (never the row's own
        # composition), which removes the smoothing bias of the draw-level class prior (pass A: escalate and code
        # classes under-gold by 2-7 pp)
        self.q2dev = Counter()
        self.q2_out = Counter()
        self.q2_basis = Counter()
        self.q2_exp = Counter()
        self.q4_counts = Counter()
        self.yes = 0
        self.q3n = 0
        self.qbal = BAL.Q3Balance(card)
        self.twin_ans = Counter()
        self.rbal = BAL.RoleBalance()
        # r2: Q2 option-class balance, soft depth / amendment quotas on emitted rows, Q2 option-count plan
        # r2 pass B: the class balance is kept per option-count bucket (10-19 / 20-60): the role-rate rule is checked
        # per (question type x k) cell, and 20-60 rows carry more never-gold options than 10-19 rows (pass A: default
        # gold +6.7 pp on 20-60 Q2 rows, escalate -3.4 pp on 10-19 rows, balanced per card overall)
        self.q2prior = R2.Q2ClassBalance()
        self.q2fprior = Counter()   # r2 pass C: draw-level gold counts by fine option class
        # r3 pass C2: the same counts per option-count bucket (20-23 option rows draw larger structures since C2, so
        # their gold class rates differ; one pooled rate under-kept code-basis gold, pass B q2_code_share -2.5 pp)
        self.q2fprior_b = {"big": Counter(), "small": Counter()}
        self._band_rej = Counter()   # r3 pass C2: per-card band refusal runs (q2_keepf)
        self._band_moved = set()     # r3 pass C2 v6: (long, source, side) band keys this card has moved back inward
        self.q2cb = {"big": R2.Q2ClassBalance(self.q2prior), "small": R2.Q2ClassBalance(self.q2prior)}
        self._late = False
        self.kplan = Counter()
        self.defer_account = False
        self.case_refs_used = set()
        self.stats = Counter()

    # -------- case placement per sampler
    def place_boundary(self, S: Struct, case: Case, rng):
        """Put one numeric or date literal's field value at T, T - s or T + s (S1 A31: place, solve, accept)."""
        occ = [(r, it, m) for r, it, m in all_lit_occurrences(S) if S.attrs[m.attr].type in ("num", "date")
               and m.attr in case.vals and S.attrs[m.attr].role == "normal"]
        if not occ:
            return None
        r, it, m = rng.choice(occ)
        a = S.attrs[m.attr]
        step = a.step if a.type == "num" else 1
        T = m.args[rng.randrange(len(m.args))]
        cls = rng.choices(["at", "below", "above"], weights=[0.34, 0.33, 0.33])[0]
        v = T if cls == "at" else (T - step if cls == "below" else T + step)
        if not (a.lo <= v <= a.hi):
            return None
        case.vals[m.attr] = v
        return cls

    def place_g(self, S: Struct, case: Case, rng):
        """S6: g placed uniformly before, on and after each effective date (each change point equally likely)."""
        if not S.notices:
            return
        n = rng.choice(S.notices)
        mode = rng.choice(["before", "on", "after"])
        g = n.edate + (-rng.randint(1, 20) if mode == "before" else 0 if mode == "on" else rng.randint(1, 20))
        g = max(g, S.policy.B)
        case.vals[S.policy.gov] = g

    def label_first(self, S: Struct, case: Case, rng):
        """S2: pick a winning rule, make its chain fire, and add a near-miss rule failing on exactly one item."""
        res0 = A.solve_closed(S, case.vals, case.notrec)
        rules = res0["rules"]
        outs = [rid for rid, (r, d, s) in rules.items() if r.kind in ("gen", "oexc")]
        if not outs:
            return None
        for tries in range(6):
            got = self._label_first_once(S, case, rng, rules, outs)
            if got is not None:
                return got
        return None

    def _label_first_once(self, S, case, rng, rules, outs):
        W = rng.choice(outs)
        vals = dict(case.vals)
        fixed = {S.policy.gov}
        chain = []
        x = W
        while x is not None and x in rules:
            chain.append(rules[x][0])
            r = rules[x][0]
            x = r.target if r.kind in ("pexc", "oexc") else None
        for r in chain:
            for it in r.all_items():
                if not satisfy_item(it, S, vals, True, rng, fixed):
                    return None
        # near-miss: another outcome-carrying general rule with a different outcome, all items true but one
        others = [rid for rid, (r, d, s) in rules.items() if r.kind == "gen" and rid != W
                  and r.out != rules[W][0].out]
        if not others:
            return None
        NM = rng.choice(others)
        its = list(rules[NM][0].all_items())
        bad = rng.randrange(len(its))
        for i, it in enumerate(its):
            if not satisfy_item(it, S, vals, i != bad, rng, fixed):
                return None
        for k in case.unknown | case.notrec:
            vals.pop(k, None)
        case.vals.clear()
        case.vals.update(vals)
        SM.fix_presup(S, case)
        return (W, NM, bad)

    # -------- one solved base structure
    def size_caps(self):
        """Structure size caps from the card's fit (section 1 length: rows stay < 2,000 tokens)."""
        ft = self.card.get("fit_tokens") or 1200
        if ft >= 1650:
            mr, mf = 4, 5
        elif ft >= 1500:
            mr, mf = 5, 6
        elif ft >= 1350:
            mr, mf = 7, 7
        elif ft >= 1200:
            mr, mf = 9, 8
        else:
            mr, mf = 12, 9
        if self.card["qtype"] == "Q2":
            # r3 (A22, Q2 rows <= 7,900 tokens; tmp/repair/INFEASIBLE_length.md): the ordinary Q2 draw keeps the
            # length-based size (trim lever: rows stay as short as before when nothing needs more); a depth-3/4 need
            # or a 20-23 option grid may raise the structure to 7 rules / 7 fields (size of a 1,350-1,500 token card)
            self._base_caps = (min(mr, 6), min(mf, 6))
            mr, mf = 7, 7
        if self.card["qtype"] == "Q4":
            mr, mf = min(mr, 5 if ft < 1500 else 4), min(mf, 5)
        return mr, mf

    def draw_solved(self, deep=False, closed_only=False, attempts=None):
        """A drawn and solved structure (no depth yet; callers check depth after their cheap checks)."""
        card, rng = self.card, self.rng
        mr, mf = self.size_caps()
        small = getattr(self, "_small", None)
        for attempt in range(attempts or (60 if deep else 300)):
            try:
                rmin = getattr(self, "_rmin", None)
                if small is not None:
                    n_rules, n_fields = small
                elif deep:
                    n_rules, n_fields = rng.randint(max(3, mr - 3), max(3, mr)), rng.randint(4, mf)
                else:
                    mrb, mfb = getattr(self, "_base_caps", None) or (mr, mf)
                    n_rules = rng.choice([x for x in (3, 3, 4, 4, 5, 5, 6, 6, 7, 8, 9, 10, 11, 12) if x <= mrb])
                    n_fields = rng.randint(4, mfb)
                    if rmin:
                        n_rules = max(n_rules, min(mr, rmin))   # r3: Q2 20-23 option rows need >= r_big rules
                # r2: the operative-notice count follows the card's amendment quota (G0 8 shares) on most draws
                n_not = None
                aq = self.amend_quota()
                if aq is not None and not deep and getattr(self, "target_depth", None) is None and \
                        rng.random() < 0.8:
                    n_not = aq.need(rng)
                # r2 pass B: the depth level the card needs is drawn first; a deep level (3-4) gets a structure with
                # room for it (>= 5 / 6 rules and, on cards with notices, >= 1 / 2 operative notices), since the pass A
                # boosts reached depth 4 on too few draws (rows 28 / 41 / 23 / 9% at depth 1-4)
                need = None
                n_rules0, n_fields0 = n_rules, n_fields
                if not deep and small is None and getattr(self, "target_depth", None) is None:
                    need = self.depth_quota().need(rng, allowed={x for x in (1, 2, 3, 4) if x <= self.dmax()})
                    # the larger structure only while the card's rows stay under the length cap (gen_card books length
                    # rejections; smoke: a long Q1 card lost almost every row to the cap with it)
                    roomy = self.kplan["len_fail"] <= 6 + 0.1 * self.depth_quota().n
                    if need >= 3 and roomy:
                        n_rules = max(n_rules, min(mr, 5 if need == 3 else 6))
                        n_fields = max(n_fields, min(mf, n_fields + 1))
                        if aq is not None and need == 4:
                            # one operative notice at least (a decisive amendment is one of the depth terms); the
                            # amendment quota still sets the count above that (smoke: forcing 2 notices on depth-4
                            # draws put 58% of rows at 2 notices against the 20% target)
                            n_not = min(3, max(n_not or 0, 1))
                if small is not None and n_not is not None:
                    n_not = min(n_not, 1)   # r2: Q2 20-60 option rows stay short (length cap)
                try:
                    S = SM.draw_struct(card, self.pack, rng, sampler=self.sampler if self.sampler != "S5" else "S1",
                                       n_rules=n_rules, n_fields=n_fields, n_not=n_not)
                except (ValueError, KeyError, IndexError):
                    if (n_rules, n_fields) == (n_rules0, n_fields0):
                        raise
                    # a card whose literal pool cannot fill the larger structure keeps its own drawn size
                    self.stats["deep_size_fallback"] += 1
                    S = SM.draw_struct(card, self.pack, rng, sampler=self.sampler if self.sampler != "S5" else "S1",
                                       n_rules=n_rules0, n_fields=n_fields0, n_not=n_not)
                case = SM.draw_case(S, card, rng, ref=self.new_ref())
                if closed_only and case.unknown:
                    continue
                if self.sampler == "S6":
                    self.place_g(S, case, rng)
                nm = None
                # r1.1 pass 5: on a missing-field case the missing-field rule decides first, so there is no winning
                # rule chain to build; label_first returned None on every such case and S2 missing-field cards never
                # had M gold (role-rate rule broken, X_role M never final on their Q3 rows)
                if self.sampler == "S2" and not case.notrec:
                    nm = self.label_first(S, case, rng)
                    if nm is None:
                        self.stats["rej_s2_chain"] += 1
                        continue
                td = getattr(self, "target_depth", None)
                if td is None and case.notrec and not deep:
                    # r2: a not-recorded case is decided by the missing-field rule (depth 1); when the card needs a
                    # deep level it is redrawn as often as a missed boost (else missing-field cards fill with depth 1)
                    nd = need if need is not None else 1
                    if nd >= 3 and rng.random() < (0.9 if nd == 4 else 0.7):
                        self.stats["notrec_redraw"] += 1
                        continue
                if td is None and not case.notrec:
                    # r2: every sampler moves its draw towards the depth level its card most needs (G0 8 depth
                    # shares; the r1.1 rows were 43 / 44 / 12 / 1.4% at depth 1-4 against 22 / 33 / 28 / 17).
                    # S2 keeps its label-first chain and builds it to that depth; closed cases are boosted directly,
                    # open-world cases through one completion (the row's depth is the maximum over completions).
                    # Best effort: solver A's depth is what the row records and the quota accepts or redraws.
                    if deep:
                        td_c = rng.choice([5, 6])
                    elif need is not None and (rng.random() < 0.9 or self.sampler == "S2"):
                        td_c = need
                    else:
                        td_c = None
                    if td_c is not None and td_c > 1:
                        tries = (15 if td_c == 2 else 40) if td_c <= 4 else 120
                        okb = chain_boost(S, case, td_c, rng, tries=tries) if not case.unknown else \
                            open_boost(S, case, td_c, rng, tries=tries)
                        if not okb:
                            self.stats["boost_short"] += 1
                            # r2: a draw that misses a needed deep level is usually redrawn (depth 3-4 were 12% and
                            # 1.4% of r1.1 rows; one boost reaches depth 4 on about a fifth of the draws)
                            if td_c >= 3 and rng.random() < (0.9 if td_c == 4 else 0.7):
                                self.stats["boost_redraw"] += 1
                                continue
                elif td is not None and not case.unknown:
                    chain_boost(S, case, td, rng, tries=40 if td <= 4 else getattr(self, "deep_tries", 150))
                if rng.random() < 0.6:
                    self.place_boundary(S, case, rng)
                SM.fix_presup(S, case)
                res = A.solve(S, case)
                if card["short"] and any(c["src"] == "T" for c in res["comps"]):
                    self.stats["rej_short_tie"] += 1
                    continue
                return S, case, res, None, None, nm
            except (Reject, SM.DrawFail, KeyError, IndexError, ValueError) as e:
                self.stats["rej_" + type(e).__name__] += 1
                continue
        raise Reject("no draw")

    def depth_of(self, S, case, deep):
        """(depth, A) or None if the depth does not fit the deep / non-deep path (or the sweep level)."""
        d, Adec = A.depth(S, case)
        if d > 6:
            self.stats["rej_depth7"] += 1
            return None
        td = getattr(self, "target_depth", None)
        if td is not None:
            if d != td:
                self.stats["rej_target_depth"] += 1
                return None
            return d, Adec
        if deep and d < 5:
            self.stats["rej_deep_shallow"] += 1
            return None
        if not deep and d > 4:
            self.stats["rej_deep_unplanned"] += 1
            return None
        return d, Adec

    def new_ref(self):
        ids = self.pack["subject"].get("ids") or []
        rng = self.rng
        for _ in range(50):
            if ids and rng.random() < 0.8:
                r = rng.choice(ids)
            else:
                pre = "".join(w[0] for w in self.card["subj"].split()[:3]).upper() or "CS"
                r = f"{pre}-{rng.randint(1000, 9999)}"
            if r not in self.case_refs_used:
                self.case_refs_used.add(r)
                return r
        return f"CX-{rng.randint(10000, 99999)}"


# ---------------------------------------------------------------- row records

def row_meta_struct(S: Struct, case: Case, res: dict, d: int, Adec: int, card, decisive_cls=None):
    src, winner = A.gold_source(res)
    n_amend = len(S.notices)
    pos = None
    n_el = len(S.order)
    if src == "ONE" and res["det"]:
        c0 = res["comps"][0]
        el = c0["rules"][winner][2]
        idx = [i for i, x in enumerate(S.order) if x == el]
        pos = idx[0] + 1 if idx else None
    return {"gold_source": src, "winner": winner, "depth": d, "A": Adec, "n_amend": n_amend, "position": pos,
            "n_elements": n_el, "boundary": decisive_cls, "world": S.policy.world,
            "policy": S.policy.prim + ("+" + S.policy.sec if S.policy.sec else ""),
            "n_rules": len(S.rules)}


def opposite_sides(S: Struct, g: int) -> bool:
    for n in S.notices:
        if (n.ndate <= g) != (n.edate <= g):
            return True
    return False


class GroupBuilder(RowBuilder):
    """Builds one selection set (base + units + twins) for the card's question type."""

    def plan_answer(self):
        """Q3: the answer that keeps the card at round(y x rows) yes answers."""
        y = self.card["yes_rate"]
        want = y * (self.q3n + 1)
        return 1 if self.yes + 1 <= want + 0.5 else 0

    def dmax(self):
        cs = self.card["constructs"]
        X = 2 if "exc2" in cs else 1 if ("exc" in cs or "pexc_short" in cs) else 0
        Am = 3 if "notices" in cs else 0
        return 1 + X + Am + 1 + (1 if "onlyif" in cs else 0)

    def depth_quota(self):
        """r2: soft per-card quota over the non-deep depth levels of emitted rows (targets by the card's ceiling,
        r2bal.DEPTH_BY_DMAX; G0 8 family shares 22 / 33 / 28 / 17)."""
        q = getattr(self, "_dq", None)
        if q is None:
            dm = max(2, min(5, self.dmax()))
            tab = R2.DEPTH_BY_DMAX   # r3 (A22): Q2 cards take the same depth table (DEPTH_Q2 was the length lever)
            if self.card["qtype"] == "Q2" and dm >= 4:
                tab = DEPTH_Q2_DEEP   # r3 pass C2
                if str(getattr(self, "seed_key", "")).startswith("qc|"):
                    tab = DEPTH_Q2_DEEP_QC   # r3 pass C2 v4
            sl = 1.5
            if self.card["qtype"] != "Q2" and str(getattr(self, "seed_key", "")).startswith("qc|"):
                sl = DEPTH_SLACK_QC   # r3 pass D (qc depth)
            q = self._dq = R2.SoftQuota(tab[dm], slack=sl, p_rej=0.95)
        return q

    def amend_quota(self):
        """r2: soft per-card quota over the operative-notice count of emitted rows (cards with notices only)."""
        if "notices" not in self.card["constructs"]:
            return None
        q = getattr(self, "_aq", None)
        if q is None:
            t = R2.AMEND_S6 if self.sampler == "S6" else R2.AMEND_NOTICE_CARD
            q = self._aq = R2.SoftQuota(t, slack=2.0, p_rej=0.8)
        return q

    def quota_ok(self, d, n_amend, deep):
        """r2 acceptance on the depth and amendment quotas (relaxed on the last attempts of a row)."""
        if deep or getattr(self, "target_depth", None) is not None or getattr(self, "_relaxed", False):
            return True
        if self._late:
            # r2 pass B: the depth quota still applies, at half strength, on a row's last attempts
            if d <= 4 and self.depth_quota().over(d) and self.rng.random() < 0.5:
                self.stats["rej_depth_q_late"] += 1
                return False
            return True
        if d <= 4 and not self.depth_quota().ok(d, self.rng):
            self.stats["rej_depth_q"] += 1
            return False
        aq = self.amend_quota()
        if aq is not None and not aq.ok(n_amend, self.rng):
            self.stats["rej_amend_q"] += 1
            return False
        return True

    def depth_ok(self, d, deep):
        if getattr(self, "target_depth", None) is not None:
            return d == self.target_depth
        if deep:
            return d in (5, 6)
        return True

    def base_checks(self, S, case, res, d, deep, nm=None):
        """Sampler checks on a closed case: boundary class (S1-S6), decisive position (ONE rows)."""
        rng = self.rng
        info = {}
        if not self.depth_ok(d, deep):
            self.stats["rej_depth_quota"] += 1
            return None
        if not self.quota_ok(d, len(S.notices), deep):
            return None
        closed = not case.unknown
        bcls = None
        if closed:
            dec, base = decisive_literals(S, case.vals, case.notrec)
            bcls = boundary_class(S, case.vals, dec)
            # S6 decisive notice at the boundary: g on its effective date
            if self.sampler == "S6" and S.notices:
                g = case.vals[S.policy.gov]
                dn = self.decisive_notices(S, case)
                if any(n.edate == g for n in S.notices if n.num in dn):
                    bcls = "at"
                elif bcls is None and dn:
                    bcls = "far"
            if bcls is not None:
                q = self.tr.boundary[self.sampler]
                if bcls == "far":
                    self.stats["rej_boundary_far"] += 1
                    return None
                elif not q.ok(bcls):
                    self.stats["rej_boundary_quota"] += 1
                    return None
        info["boundary"] = bcls
        # decisive position uniform over 1..n (ONE rows only; operative elements; section 8)
        src, w = A.gold_source(res)
        if src == "ONE" and res["det"]:
            el = res["comps"][0]["rules"][w][2]
            idx = [i for i, x in enumerate(S.order) if x == el]
            if idx:
                pos, n = idx[0] + 1, len(S.order)
                if not self.tr.pos_ok(self.sampler, n, pos):
                    self.stats["rej_position"] += 1
                    return None
                info["position"] = (n, pos)
        return info

    def decisive_notices(self, S, case):
        out = set()
        P = S.policy
        base = A.solve_closed(S, case.vals, case.notrec)
        nums = [n.num for n in S.notices]
        import itertools
        changes = {}
        for r in range(1, len(nums) + 1):
            for T in itertools.combinations(nums, r):
                T = frozenset(T)
                alt = A.solve_closed(S, case.vals, case.notrec, removed=A.removal_closure(S, T))
                changes[T] = alt["final"] != base["final"]
        for T, ch in changes.items():
            if ch and not any(changes.get(U) for U in changes if U < T):
                out |= T
        g = case.vals[P.gov]
        return {n for n in out if next(x for x in S.notices if x.num == n).edate <= g}

    def commit_base(self, S, case, res, d, info):
        # r2: the depth quota books emitted rows (account_row), not committed bases
        if info.get("position"):
            self.tr.pos_add(self.sampler, *info["position"])
        if info.get("boundary") in ("at", "below", "above"):
            self.tr.boundary[self.sampler].add(info["boundary"])

    # ---------------------------------------------------------------- Q3
    def flip_outcomes(self, S, case):
        if case.unknown:
            return set()
        dec, base = decisive_literals(S, case.vals, case.notrec)
        out = set()
        for m in dec:
            cur = A.lit_val(m, S.attrs, case.vals)
            A.set_override({id(m): not cur})
            try:
                out.add(A.solve_closed(S, case.vals, case.notrec)["final"])
            except Reject:
                pass
            finally:
                A.set_override(None)
        return out

    def _yb(self, X, pol):
        bad = self.card["valence"][X] == "bad"
        return (pol in ("aff", "dneg") and bad) or (pol == "neg" and not bad)

    def build_q3(self, deep=False, pol=None, unit_kind=None, want_twin=False):
        """Q3 base row. r1.1 repair: X is matched between yes and no rows (balance.Q3Balance): the free side picks X
        to follow the forced side's X distribution per card x polarity class, and row structure features (notice
        count, depth, rule count) are kept equally distributed over yes and no rows by rejection. The last third of
        the attempts relaxes the balance rejections (the matching choice of X on the free side always applies)."""
        card, rng = self.card, self.rng
        qb = self.qbal
        a = self.plan_answer()
        if pol is None:
            if card["short"]:
                pol = "aff"
            else:
                # r1.1: more singly negated questions; with X matched over yes and no rows the yes = bad share is
                # 0.5 + (P(X bad) - 0.5)(1 - 2 P(neg)), so negation is the main lever left (G0 8: 50 +/- 5).
                # The polarity is planned per answer by deficit (failed draws are retried with the same plan), so
                # P(polarity | answer) stays equal for yes and no rows (polarity is visible in the question)
                pol = qb.plan_pol(a, rng)
        if unit_kind == "neg":
            pol = "aff"
        pc = BAL.pclass(pol)
        forced = BAL.is_forced(pol, a)
        n_att = 12 if deep else 60
        for attempt in range(n_att):
            late = attempt >= (2 * n_att) // 3
            self._late = late
            S, case, res, d, Adec, nm = self.draw_solved(deep=deep)
            # r2 pass B: the row's depth is known before X is chosen, so X is matched inside the depth bin
            dd = self.depth_of(S, case, deep)
            if dd is None:
                continue
            d, Adec = dd
            db = qb.dbin(d)
            if res["det"]:
                qb.see_final(res["final"], db)
            cands = [X for X in card["outcomes"] if A.q3_answer(res, X, pol) == a]
            if not cands:
                self.stats["rej_q3_answer"] += 1
                continue
            if forced:
                X = cands[0]
                if not late:
                    if qb.forced_excess(pc, X) > 0.12 or qb.forced_excess_d(pc, db, X) > 0.2:
                        self.stats["rej_q3_xmatch"] += 1
                        continue
                    yb = self._yb(X, pol)
                    sh = qb.yb_share_after(yb)
                    if abs(sh - 0.5) > 0.03 and (sh - 0.5) * (1 if yb else -1) > 0 and rng.random() < 0.85:
                        self.stats["rej_q3_yesbad"] += 1
                        continue
            else:
                # the outcome the free side most needs; if this draw cannot ask about it (it is the final), redraw
                need = max(card["outcomes"], key=lambda Y: qb.free_deficit_d(pc, db, Y) + 0.5 * qb.free_deficit(pc, Y))
                if not late and need not in cands and qb.free_deficit_d(pc, db, need) >= 0.5:
                    self.stats["rej_q3_xneed"] += 1
                    continue
                fo = set()
                if want_twin and pol in ("aff", "dneg"):
                    fo = self.flip_outcomes(S, case) & set(cands)

                def score(X):
                    s = qb.free_deficit_d(pc, db, X) + 0.5 * qb.free_deficit(pc, X)
                    if X in fo:
                        s += 0.3
                    s -= 0.5 * abs(qb.yb_share_after(self._yb(X, pol)) - 0.5)
                    return s + rng.random() * 0.05
                X = max(cands, key=score)
            if not late:
                bf = qb.feat_bad(a, qb.feats(S, d))
                if bf:
                    self.stats["rej_q3_feat_" + bf] += 1
                    continue
            info = self.base_checks(S, case, res, d, deep)
            if info is None:
                continue
            # trap: at least one error model flips the answer on most rows (reported; mild steering)
            eo = A.error_outputs(S, case, res)
            flips = [E for E, o in eo.items() if A.q3_from_finals(o["finals"], X, pol) not in (None, a)]
            if not flips and rng.random() < 0.8:
                self.stats["rej_q3_noflip"] += 1
                continue
            self.commit_base(S, case, res, d, info)
            q = {"qtype": "Q3", "X": X, "pol": pol, "frame": rng.randrange(3), "ref_text": f"{card['subj']} {case.ref}"}
            row = {"S": S, "cases": [case], "q": q, "gold": a, "res": res, "depth": d, "A": Adec, "info": info,
                   "eo": eo, "flips": flips, "deep": deep}
            return row
        raise Reject("q3 attempts")

    def account_q3(self, row):
        a = row["gold"]
        self.yes += a
        self.q3n += 1
        q = row["q"]
        card = self.card
        bad = card["valence"][q["X"]] == "bad"
        yb = (q["pol"] in ("aff", "dneg") and bad) or (q["pol"] == "neg" and not bad)
        self.tr.yesbad["n"] += 1
        self.tr.yesbad["yb"] += int(yb)
        self.tr.role_yes[card["roles"][q["X"]]][a] += 1
        self.qbal.account(q["X"], q["pol"], a, row["S"], row["depth"], yb)

    # ---------------------------------------------------------------- r1.1: role bookkeeping on emitted rows
    def role_of(self, o):
        if o == CBD:
            return "cbd"
        if o == "__NONE__":
            return "none"
        return self.card["roles"].get(o, "case")

    def shown_roles(self, opts):
        """{role: m/k} of a choice row's options (Q2 options are (outcome, basis) pairs)."""
        k = len(opts)
        c = Counter(self.role_of(o[0] if isinstance(o, tuple) else o) for o in opts)
        return {ro: m / k for ro, m in c.items()}

    def gold_role(self, row):
        g = row["gold"]
        return self.role_of(g[0] if isinstance(g, tuple) else g)

    def account_row(self, row):
        """Book one emitted row (base, unit row or twin) into the card's balance counters."""
        qt = row["q"]["qtype"]
        # r2: depth and amendment quotas count every emitted non-deep row (G0 8 counts rows)
        if not row.get("deep") and row.get("depth") is not None and row["depth"] <= 4:
            self.depth_quota().add(row["depth"])
            aq = self.amend_quota()
            if aq is not None:
                aq.add(len(row["S"].notices))
        if qt == "Q3":
            self.account_q3(row)
            if row.get("role") == "twin":
                self.twin_ans[row["gold"]] += 1
            return
        if qt == "Q4" and row["gold"] != "__NONE__":
            gr = "case"
        else:
            gr = self.gold_role(row)
        bkey = None
        if qt == "Q2":
            # r2: option-class balance and the option-count plan book every emitted Q2 row
            k2 = len(row["options"])
            cs = Counter(self.q2_class(p) for p in row["options"])
            self.q2cb["big" if k2 >= 20 else "small"].account(self.q2_class(row["gold"]),
                                                              {c: m / k2 for c, m in cs.items()})
            self.kplan["big" if k2 >= 20 else "small"] += 1
            self.q2_book(row["options"], row["gold"], row.get("res"))
            g = row["gold"]
            bkey = gr + "|" + ("cbd" if g[0] == CBD else ("code" if isinstance(g[1], str) else "rule"))
        self.rbal.account(gr, self.shown_roles(row["options"]), row.get("depth") if qt in ("Q1", "Q2") else None,
                          len(row["S"].rules), key=bkey)
        if qt == "Q1":
            self.q1_counts[row["gold"]] += 1
            if self.srcq is not None:
                self.srcq_cnt[self.q1_srcq_key(row["options"], row["gold"], row.get("res"))] += 1
            self.kplan["q1_rows"] += 1
            if row.get("res") is not None and A.gold_source(row["res"])[0] == "T":
                self.kplan["t_src"] += 1
        elif qt == "Q2":
            opts = row["options"]
            if row["gold"][0] != CBD:
                self.q2_basis["code" if isinstance(row["gold"][1], str) else "rule"] += 1
                self.q2_exp["code"] += sum(1 for p in opts if isinstance(p[1], str)) / len(opts)
                # r1.1 pass 5: per-code supply and gold, for the per-code filler steer in build_q2
                for p in opts:
                    if isinstance(p[1], str):
                        self.q2_exp["c:" + p[1]] += 1 / len(opts)
                if isinstance(row["gold"][1], str):
                    self.q2_basis["c:" + row["gold"][1]] += 1

    # ---------------------------------------------------------------- Q1
    def q1_options(self):
        card = self.card
        opts = list(card["outcomes"])
        if card["world"] == "open":
            opts.append(CBD)
        return opts

    @staticmethod
    def _devf(dev):
        if dev > 0.5:
            return max(0.2, 1.0 - 0.6 * (dev - 0.5))
        if dev < -0.5:
            return min(2.5, 1.0 + 0.6 * (-dev - 0.5))
        return 1.0

    def q2_opt_text(self, p):
        import emit as EM   # the rendered option text (the G10 longest-option check measures it)
        return EM.q2_option_text(self.card, p)

    def q2_long_credit(self, opts, gold):
        L = [len(self.q2_opt_text(p)) for p in opts]
        m = max(L)
        T = [i for i, x in enumerate(L) if x == m]
        gi = opts.index(gold)
        return (1.0 / len(T)) if gi in T else 0.0

    def q2_keepf(self, opts, gold, res):
        """r3: keep-step factor from the card's running Q2 deviations (gold option class; longest per source)."""
        bk = "big" if len(opts) >= 20 else "small"
        gcls = self.q2_class(gold)
        f = self._devf(self.q2dev[(bk, gcls)])
        # r3 pass C2 v3 (G10 role_rate per (role, Q2, bucket) and q2_code_share): the running deviations of exactly
        # those quantities (q2_aggs: gold role minus shown share for each role but other / case, gold code basis
        # minus code-option share; never-gold decoy options included, as G10 counts them) are held in [-0.5, +0.5]
        # per bucket: a draw that moves one of them further out is refused, unless the card has made Q2_BAND_BUDGET
        # such refusals in a row on that key with no allowed draw moving it back (a stuck card: soft factor only).
        # (v2 banded the option classes: never-gold decoy classes, e.g. other|code, drift down by construction, so
        # every gold-capable class sat at the band and the code share still ran -2 pp.)
        bad, moved = False, []
        for key, d in self.q2_aggs(opts, gold).items():
            v = self.q2dev[key]
            new = v + d
            bw = Q2_G7_BAND.get(key[0], 0.5)   # r3 pass C2 v7
            if (new > bw and new > v) or (new < -bw and new < v):
                self._band_rej[key] += 1
                if self._band_rej[key] <= Q2_BAND_BUDGET:
                    bad = True
                else:
                    self.stats["q2_aggband_escape"] += 1
            elif abs(v) > bw and abs(new) < abs(v):
                moved.append(key)
        if bad:
            self.stats["rej_q2_aggband"] += 1
            return 0.0
        src = A.gold_source(res)[0] if res is not None else "CBD"
        h = self.q2_long_credit(opts, gold)
        dl = self.q2dev[("long", src)]
        if True:   # r3 pass C2 v5: CBD-gold rows take the band too (see below)
            # r3 pass C (G10 longest per source): the soft factor below let the running deviation of a source whose
            # natural longest-gold rate is under 1/k settle past its -0.5 edge (pass B: Q2 T-source -9.9 / -6.2 hits
            # over 17 cards). Hard band instead: a draw is kept only if the (chain-carried, build.gen_card) longest-gold
            # minus 1/k of its gold source stays in [-0.5, +0.5] or moves toward 0; for any k exactly one of
            # (longest gold, other gold) is open at each state, so the steer never stalls. CBD-gold Q2 rows (the CBD
            # label is nearly always the longest option, 12 rows per pool) keep the soft factor: a hard band would
            # remove them and tilt the Q2 option-class mix.
            # r3 pass C2: the band holds unless the card has made Q2_BAND_BUDGET refusals for (source, direction) in a
            # row with no allowed draw moving that source back toward 0; then the soft factor applies (smoke:
            # F1-C006 under the plain hard band kept 18 of 40 rows in 110 s, every build_q2 call failing on a source
            # whose longest-gold state the card cannot move; the chain carry lets the next cards pull it back)
            # r3 pass C2 v5 (agent 5): CBD-gold rows are banded too (v4 chain: 16 cand CBD-gold Q2 rows gave +8.0 hits,
            # G10 src:CBD +2.1 pp on the shard pool; Q2 rows showing CBD stay < 200 per bucket, so G10 role_rate checks
            # no cbd|Q2 cell, and CBD-gold draws where CBD is not the longest option (~35%) remain open), and each chain
            # starts from its share of the set's non-Q2 longest-gold deviation per source (q2chain_r3.py seed), so the
            # Q2 rows hold the pool total, not only their own.
            new = dl + h - 1.0 / len(opts)
            if (new > 0.5 and new > dl) or (new < -0.5 and new < dl):
                key = ("long", src, "up" if new > dl else "down")
                self._band_rej[key] += 1
                if self._band_rej[key] <= Q2_BAND_BUDGET:
                    self.stats["rej_q2_longband"] += 1
                    return 0.0
                self.stats["q2_longband_escape"] += 1
                # r3 pass C2 v5: an escape admits this one draw and re-arms the band at half budget (v4 and earlier:
                # the run count kept growing, so after the first escape the band stayed off for the rest of the card;
                # cand chain 1 drifted T -5.4 hits over 9 cards, G10 src:T -2.0 pp on the shard pool)
                # r3 pass C2 v6 (agent 6): re-arm only if this card has already moved the source back inward from
                # that side (a card whose draws cannot, e.g. F1-C041 never makes CBD the longest option, or F1-C011
                # nearly always does, keeps the v3 rule: off after the first escape; v5 smoke: C041 stalled 555 s /
                # 40 rows on ~17k CBD band refusals; v6 with a side-free rule: C011 12 of 40 rows in 600 s)
                if src in Q2_REARM_SRC and key in self._band_moved:
                    self._band_rej[key] = Q2_BAND_BUDGET // 2
                f *= (self._devf(dl) if h > 1.0 / len(opts) else 1.0 / self._devf(dl))
            elif abs(dl) > 0.5 and abs(new) < abs(dl):
                self._band_rej[("long", src, "up" if dl > 0 else "down")] = 0
                self._band_moved.add(("long", src, "up" if dl > 0 else "down"))
            for key in moved:
                self._band_rej[key] = 0
            return f
        if h > 1.0 / len(opts):
            f *= self._devf(dl)          # longest-gold draw: damped when the source runs ahead, boosted when behind
        elif dl < -0.5:
            f /= self._devf(dl)          # other draw while the source's longest-gold count runs behind: damped
        for key in moved:
            self._band_rej[key] = 0
        return f

    def q2_keepf_twin(self, opts, gold):
        """r3 pass C2 v8: keep factor of a Q2 twin = the soft class factor of q2_keepf, without the hard bands."""
        bk = "big" if len(opts) >= 20 else "small"
        return self._devf(self.q2dev[(bk, self.q2_class(gold))])

    def q2_aggs(self, opts, gold):
        """r3 pass C2 v3: per-row change of the G10 Q2 aggregates in the row's bucket: ("agg", bucket, "role:R") =
        gold role is R minus R's shown share (roles other / case are not checked by G10), and ("agg", bucket, "code")
        = gold basis is a special code minus the code-option share (rows with a rule / code gold only)."""
        k = len(opts)
        bk = "big" if k >= 20 else "small"
        rs = Counter(self.role_of(p[0]) for p in opts)
        gr = self.role_of(gold[0])
        out = {}
        for r, m in rs.items():
            if r in ("other", "case"):
                continue
            out[("agg", bk, "role:" + r)] = (1.0 if r == gr else 0.0) - m / k
        if gold[0] != CBD:
            mc = sum(1 for p in opts if isinstance(p[1], str))
            out[("agg", bk, "code")] = (1.0 if isinstance(gold[1], str) else 0.0) - mc / k
        # r3 pass C2 v7: per-basis G7 keys on every Q2 row (CBD-gold rows too: G7 counts them as gold lacking the basis)
        gb = gold[1] if gold[0] != CBD else None
        for b, m in Counter(p[1] for p in opts if p[0] != CBD).items():
            key = ("g7code", self.card["card_id"], b) if isinstance(b, str) else ("g7rid", b)
            out[key] = (1.0 if b == gb else 0.0) - m / k
        return out

    def q2_book(self, opts, gold, res):
        k = len(opts)
        bk = "big" if k >= 20 else "small"
        cs = Counter(self.q2_class(p) for p in opts)
        gc = self.q2_class(gold)
        for c, m in cs.items():
            self.q2dev[(bk, c)] += (1.0 if c == gc else 0.0) - m / k
        src = A.gold_source(res)[0] if res is not None else "CBD"
        self.q2dev[("long", src)] += self.q2_long_credit(opts, gold) - 1.0 / k
        for key, d in self.q2_aggs(opts, gold).items():   # r3 pass C2 v3
            self.q2dev[key] += d

    def q1_srcq_key(self, opts, gold, res):
        """r3: quota cell of a Q1 row = gold source | L (gold is a longest rendered option; ties count as L) or N."""
        card = self.card
        src = A.gold_source(res)[0] if res is not None else "CBD"
        L = {o: len(card["cbd_label"] if o == CBD else str(card["display"][o])) for o in opts}
        return src + "|" + ("L" if L.get(gold, -1) == max(L.values()) else "N")

    def srcq_ok(self, opts, gold, res):
        if self.srcq is None:
            return True
        return self.srcq_cnt[self.q1_srcq_key(opts, gold, res)] < self.srcq.get(self.q1_srcq_key(opts, gold, res), 0)

    def q1_gold_ok(self, gold, opts, late=False):
        """Per-outcome slot balance (uniform gold over the card's options) plus the role-rate rule (G0 8), counted
        on every emitted row of the card (base, unit rows and twins; r1.1)."""
        if getattr(self, "_relax_gold", False):
            return True   # r3 (G11): a card with < 8 rows after 10 x target attempts (F1-C029) drops the gold steers
        k = len(opts)
        tot = sum(self.q1_counts.values())
        if self.q1_counts[gold] + 1 > (tot + 1) / k + 1.5:
            self.stats["rej_q1_slot"] += 1
            return False
        ro = self.role_of(gold)
        shown = self.shown_roles(opts)
        if self.rbal.over(ro, shown.get(ro, 0)):
            self.stats["rej_q1_role"] += 1
            return False
        if not late and self.rbal.starving(ro, shown) and self.rng.random() < 0.85:
            self.stats["rej_q1_starve"] += 1
            return False
        return True

    def build_q1(self, deep=False):
        card, rng = self.card, self.rng
        opts = self.q1_options()
        k = len(opts)
        n_att = 12 if deep else 80
        for attempt in range(n_att):
            self._late = attempt >= (2 * n_att) // 3
            S, case, res, d, Adec, nm = self.draw_solved(deep=deep)
            gold = res["final"] if res["det"] else CBD
            if gold not in opts:
                continue
            # r2: T-source cap on the cards cardfix_r2 marks (longest option per gold source, G0 8 A28)
            if card.get("t_src_cap") is not None and A.gold_source(res)[0] == "T" and \
                    self.kplan["t_src"] + 1 > card["t_src_cap"] * (self.kplan["q1_rows"] + 1) + 0.5:
                self.stats["rej_q1_tcap"] += 1
                continue
            if not self.q1_gold_ok(gold, opts, late=attempt >= (2 * n_att) // 3):
                continue
            if not self.srcq_ok(opts, gold, res):
                self.stats["rej_q1_srcq"] += 1
                continue
            eo = A.error_outputs(S, case, res)
            wrong = {o["q1"] for o in eo.values() if o["q1"] in opts and o["q1"] != gold}
            if len(wrong) < 2:
                self.stats["rej_q1_traps"] += 1
                continue
            dd = self.depth_of(S, case, deep)
            if dd is None:
                continue
            d, Adec = dd
            if attempt < (2 * n_att) // 3 and self.rbal.depth_bad(self.role_of(gold), d, len(S.rules)):
                self.stats["rej_q1_depthbal"] += 1
                continue
            info = self.base_checks(S, case, res, d, deep)
            if info is None:
                continue
            self.commit_base(S, case, res, d, info)
            q = {"qtype": "Q1", "ref_text": f"{card['subj']} {case.ref}"}
            return {"S": S, "cases": [case], "q": q, "options": opts, "gold": gold, "res": res, "depth": d,
                    "A": Adec, "info": info, "eo": eo, "traps": sorted(wrong, key=str), "deep": deep}
        raise Reject("q1 attempts")

    # ---------------------------------------------------------------- Q2
    def q2_class(self, p):
        """r2: option class of a Q2 option = (outcome role, basis kind); the CBD option is its own class."""
        o, b = p
        if o == CBD:
            return "cbd"
        return self.role_of(o) + "|" + ("code" if isinstance(b, str) else "rule")

    def q2_capable(self):
        """Classes a case of this card can make gold (the flat part of the class prior): a rule basis with any outcome
        but M; code D with the default, F with the fallback, M with outcome M; T with the escalate outcome on 'esc'
        tie cards, with any outcome but the least strict on 'strict' tie cards."""
        card = self.card
        cap = {self.role_of(o) + "|rule" for o in card["outcomes"] if o != card.get("M")}
        cd = card["codes_defined"]
        if "D" in cd:
            cap.add("default|code")
        if "F" in cd and card.get("fallback"):
            cap.add("fallback|code")
        if "M" in cd and card.get("M"):
            cap.add("M|code")
        if "T" in cd:
            if card.get("tie") == "esc":
                cap.add("escalate|code")
            elif card.get("tie") == "strict":
                least = card["strict"][-1] if card.get("strict") else None
                cap |= {self.role_of(o) + "|code" for o in card["outcomes"] if o != least and o != card.get("M")}
        if card["world"] == "open":
            cap.add("cbd")
        return cap

    def q2_fclass(self, p):
        """r2 pass C: planning class = outcome role x basis kind (rule / special code), the features a reader can see
        without solving (the role-rate rule counts roles, the code-share rule basis kinds; G6 (d) reads both). Code
        pairs that a case cannot make gold sit inside their role's code class (only the code word tells them apart)."""
        return self.q2_class(p)

    def q2_fcapable(self):
        """Fine classes a case of this card can make gold: a rule with any outcome but M; code D with the default, F
        with the fallback, M with outcome M; T with the escalate outcome on 'esc' tie cards, with any outcome but the
        least strict on 'strict' tie cards; the CBD option on open-world cards."""
        card = self.card
        return self.q2_capable()

    def q2_plan(self, k, capable, n_rules_est):
        """Class counts of a row of k options, fixed before any structure is drawn (so never a function of the row's
        gold): each gold-capable class gets about k x its draw-level gold rate (largest remainder, capped by a
        conservative capacity); the CBD option is 1 on open-world cards; what is left are never-gold decoy slots."""
        card, rng = self.card, self.rng
        role_n = Counter(self.role_of(o) for o in card["outcomes"])
        P = self.q2fprior_b["big" if k >= 20 else "small"]   # r3 pass C2: rate of the row's bucket
        n = sum(P.values())
        pr = {c: (P[c] + 4.0 / len(capable)) / (n + 4.0) for c in capable}

        def capc(c):
            if c == "cbd":
                return 1
            role, kind = c.split("|")
            return role_n[role] * (n_rules_est if kind == "rule" else len(card["codes_defined"]))
        m = Counter()
        if "cbd" in capable:
            m["cbd"] = 1
        rest = sorted(c for c in capable if c != "cbd")
        left = k - sum(m.values())
        tot = sum(pr[c] for c in rest) or 1.0
        raw = {c: left * pr[c] / tot for c in rest}
        for c in rest:
            m[c] = min(capc(c), int(raw[c]))
        while sum(m.values()) < k:
            cand = [c for c in rest if m[c] < capc(c)]
            if not cand:
                break
            c = max(cand, key=lambda x: raw[x] - m[x] + 0.01 * rng.random())
            m[c] += 1
        m["decoy"] = k - sum(m.values())
        lam = max([(m[c] / k) / pr[c] for c in m if c != "decoy" and m[c] > 0] or [1.0])
        return m, pr, lam

    def build_q2(self, deep=False):
        """r2 pass C: composition first. The row's option count k and its class counts are fixed before the draw;
        a drawn structure whose gold falls in class c is kept with probability proportional to (m_c / k) / p_c (p_c
        = the class's draw-level gold rate), so on every row P(gold in class c) = m_c / k: each option is gold at
        1/k whatever its class or how many siblings share its outcome or basis (G0 8 role-rate rule at option level;
        pass B's deficit test on the row's own class share left Q2 G6 (d) at 21% vs chance 7%)."""
        card, rng = self.card, self.rng
        big_ok = True   # r3 (A22): Q2 rows <= 7,900 tokens, no length feedback on the 20-60 plan
        sh = card.get("q2_big_share", 0.5)
        big = big_ok and self.kplan["big"] + 1 <= sh * (self.kplan["big"] + self.kplan["small"] + 1) + 0.5 and not deep
        n_o = len(card["outcomes"])
        n_m = 1 if card.get("M") is not None else 0
        free = 20 - n_o * len(card["codes_defined"]) - (1 if card["world"] == "open" else 0)
        r_big = max(3, min(6, -(-free // max(1, n_o - n_m)) if free > 0 else 3))
        # r3 pass C2 (G10 option_count_buckets): r_big only made the grid (outcomes x bases) reach 20 pairs, so a
        # 21-23 option draw had no room (C012: 5 outcomes x (3 rules + 1 code) = 20 pairs) and most big plans fell back
        # to 10-19 options after 180 attempts (pass B: Q2 rows 36% big against the 50% plan). The rule minimum now
        # follows the drawn k: grid >= k + 2 pairs (class-fill room), at most 7 rules (size_caps Q2 ceiling).
        n_fix = n_o * len(card["codes_defined"]) + (1 if card["world"] == "open" else 0)

        def r_for(kk):
            return max(r_big, min(7, -(-(kk + 2 - n_fix) // max(1, n_o - n_m))))
        capable = self.q2_fcapable()
        plan = None
        try:
            for attempt in range(12 if deep else 240):
                late = attempt >= 170
                self._late = late
                if big and attempt >= 180:
                    big, plan = False, None
                if plan is None:
                    k = rng.randint(20, 23) if big else rng.randint(10, 19)
                    m, pr, lam = self.q2_plan(k, capable, r_for(k) if big else 4)
                    plan = (k, m, pr, lam)
                k, m, pr, lam = plan
                self._small = None
                self._rmin = r_for(k) if big else None   # r3 (A22): ordinary structures with >= r_big rules (C2: r_for(k))
                S, case, res, d, Adec, nm = self.draw_solved(deep=deep)
                gp = A.q2_pair(res)
                if gp is None:
                    self.stats["rej_q2_nopair"] += 1
                    continue
                gf = self.q2_fclass(gp)
                if m.get(gf, 0) <= 0 or gf not in pr:
                    self.stats["rej_q2_noslot"] += 1
                    continue
                dd = self.depth_of(S, case, deep)
                if dd is None:
                    continue
                d, Adec = dd
                eo = A.error_outputs(S, case, res)
                errp = set()
                for o in eo.values():
                    p = o["q2"]
                    if p is not None and p != gp:
                        errp.add(p)
                rule_ids = sorted({r.rid for r in S.rules} | {n.rule.rid for n in S.notices if n.ntype == "insert"})
                bases = list(rule_ids) + list(card["codes_defined"])
                outs = [o for o in card["outcomes"]]
                grid = [(o, b) for o in outs for b in bases]
                errp = {p for p in errp if p == (CBD, None) or (p[0] in outs and p[1] in bases)}
                fixed = {gp} | errp
                grid = [p for p in grid if not (card.get("M") is not None and p[0] == card["M"]
                                                and not isinstance(p[1], str))]
                if card["world"] == "open":
                    fixed.add((CBD, None))
                # fill the planned classes; error-model pairs are always shown (they take decoy slots first, then
                # slots of the largest class other than the gold's)
                need = Counter({c: v for c, v in m.items() if c != "decoy"})
                dec = m["decoy"]
                for p in fixed:
                    c = self.q2_fclass(p)
                    if c in need and need[c] > 0:
                        need[c] -= 1
                    elif dec > 0:
                        dec -= 1
                    else:
                        cs = [x for x in need if need[x] > 0 and x != gf]
                        if not cs:
                            dec = -1
                            break
                        need[max(cs, key=lambda x: need[x])] -= 1
                if dec < 0:
                    self.stats["rej_q2_fill"] += 1
                    continue
                byc = defaultdict(list)
                for p in grid:
                    if p not in fixed:
                        byc[self.q2_fclass(p)].append(p)
                opts = list(fixed)
                ok = True
                for c, v in need.items():
                    if v <= 0:
                        continue
                    lst = byc.get(c, [])
                    if len(lst) < v:
                        ok = False
                        break
                    rng.shuffle(lst)
                    opts += lst[:v]
                if ok and dec > 0:
                    pool = [p for c, lst in byc.items() if c not in capable for p in lst]
                    if len(pool) < dec:
                        ok = False
                    else:
                        rng.shuffle(pool)
                        opts += pool[:dec]
                if not ok or len(opts) != k or len(set(opts)) != k:
                    self.stats["rej_q2_fill"] += 1
                    continue
                rng.shuffle(opts)
                g_kind = "cbd" if gp[0] == CBD else ("code" if isinstance(gp[1], str) else "rule")
                ro = self.role_of(gp[0])
                if not late and self.rbal.depth_bad(ro + "|" + g_kind, d, len(S.rules)):
                    self.stats["rej_q2_depthbal"] += 1
                    continue
                info = self.base_checks(S, case, res, d, deep)
                if info is None:
                    continue
                # the composition-first keep step comes last, after every other check, and the class rates it uses
                # are counted on the draws that reached it (so later checks cannot tilt the gold class mix)
                self.q2fprior[gf] += 1
                self.q2fprior_b["big" if k >= 20 else "small"][gf] += 1
                if rng.random() > min(1.0, (m[gf] / k) / (lam * pr[gf]) * self.q2_keepf(opts, gp, res)):
                    self.stats["rej_q2_comp"] += 1
                    continue
                self.commit_base(S, case, res, d, info)
                q = {"qtype": "Q2", "ref_text": f"{card['subj']} {case.ref}"}
                return {"S": S, "cases": [case], "q": q, "options": opts, "gold": gp, "res": res, "depth": d,
                        "A": Adec, "info": info, "eo": eo, "errpairs": sorted(errp, key=str), "deep": deep}
            raise Reject("q2 attempts")
        finally:
            self._small = None
            self._rmin = None

    # ---------------------------------------------------------------- Q4
    def build_q4(self, deep=False):
        card, rng = self.card, self.rng
        none_card = card["none_card"]
        # r1.1: the case count and the "none" plan are drawn once per row and kept over the attempts (re-drawing them
        # per attempt let "none" rows, which need no qualifying case, win the rejection race); "none" gold follows
        # the role-rate rule (1/k) by a per-card deficit
        x = rng.random()
        n_cases = 3 if x < 0.6 else 4 if x < 0.85 else 5
        k = n_cases + (1 if none_card else 0)
        gold_none = False
        if none_card:
            cnt, exp = self.rbal.cnt["none"], self.rbal.exp["none"] + 1.0 / k
            if cnt + 1 > exp + 0.5:
                gold_none = False
            elif cnt < exp - 1.0:
                gold_none = True
            else:
                gold_none = rng.random() < 1.0 / k
        for attempt in range(60):
            try:
                mr, mf = self.size_caps()
                aq = self.amend_quota()
                n_not = aq.need(rng) if (aq is not None and not deep and rng.random() < 0.8) else None
                S = SM.draw_struct(card, self.pack, rng, sampler=self.sampler, n_rules=rng.randint(3, max(3, mr)),
                                   n_fields=rng.randint(4, max(4, mf)), n_not=n_not)
            except (SM.DrawFail, Reject, KeyError, ValueError, IndexError):
                continue
            X = rng.choice(card["outcomes"])
            quals, traps = [], []
            for t in range(140):
                if len(traps) >= n_cases and (gold_none or quals):
                    break
                try:
                    c = SM.draw_case(S, card, rng, ref="")
                    if c.unknown or c.notrec:
                        continue
                    if rng.random() < 0.5:
                        self.place_boundary(S, c, rng)
                    SM.fix_presup(S, c)
                    r = A.solve(S, c)
                except (Reject, KeyError, ValueError):
                    continue
                if r["final"] == X:
                    if not gold_none and len(quals) < 1:
                        quals.append((c, r))
                    continue
                eo = A.error_outputs(S, c, r)
                hits = [E for E, o in eo.items() if o["q1"] == X]
                if len(hits) == 1 and len(traps) < n_cases:
                    traps.append((c, r, hits[0]))
            need_traps = n_cases if gold_none else n_cases - 1
            if len(traps) < need_traps or (not gold_none and not quals):
                self.stats["rej_q4_cases"] += 1
                continue
            listed = traps[:need_traps]
            lst = [(c, r, E) for c, r, E in listed]
            if not gold_none:
                pos = rng.randrange(n_cases)
                qc, qr = quals[0]
                lst.insert(pos, (qc, qr, None))
            depths = []
            try:
                for c, r, E in lst:
                    depths.append(A.depth(S, c)[0])
            except Reject:
                continue
            d = max(depths)
            if d > 6 or (not deep and d > 4) or (deep and d < 5):
                self.stats["rej_q4_depth"] += 1
                continue
            if not self.depth_ok(d, deep):
                continue
            self._late = attempt >= 40
            if not self.quota_ok(d, len(S.notices), deep):
                continue
            # gold slot balance
            refs = self.case_refs(len(lst))
            gold = "__NONE__" if gold_none else refs[[i for i, x in enumerate(lst) if x[2] is None][0]]
            slot = "none" if gold_none else str([i for i, x in enumerate(lst) if x[2] is None][0])
            for (c, r, E), ref in zip(lst, refs):
                c.ref = ref
            q = {"qtype": "Q4", "X": X}
            opts = list(refs) + (["__NONE__"] if none_card else [])
            qual = next(((c, r) for c, r, E in lst if E is None), None)
            Adec = A.depth(S, qual[0])[1] if qual else None
            return {"S": S, "cases": [c for c, r, E in lst], "q": q, "options": opts, "gold": gold,
                    "res": qual[1] if qual else None, "depth": d, "A": Adec, "info": {"boundary": None},
                    "eo": None, "trap_models": [E for c, r, E in lst], "deep": deep, "q4_refs": refs}
        raise Reject("q4 attempts")

    def case_refs(self, n):
        from fmt1 import card as fcard
        rid, sch = self.card["case_ref_scheme"]
        key = f"F1|{self.card['card_id']}|{self.rng.random()}"
        return fcard.case_refs(rid, n, key, scheme=sch)

    # ---------------------------------------------------------------- relation units
    def unit_neg(self, row):
        out = []
        for pol, rel in (("neg", "complement"), ("dneg", "equiv")):
            q = dict(row["q"])
            q["pol"] = pol
            q["frame"] = self.rng.randrange(2)
            a = A.q3_answer(row["res"], q["X"], pol)
            if a is None:
                return []
            r2 = dict(row)
            r2.update({"q": q, "gold": a, "role": "variant", "rel": rel, "unit_kind": "U-neg"})
            out.append(r2)
        return out

    def unit_attack(self, row):
        r2 = dict(row)
        r2.update({"attack": self.rng.choice(L.INJECTIONS), "role": "attacked", "rel": "inv",
                   "unit_kind": "U-attack"})
        return [r2]

    def regold(self, row, S, cases):
        """Row gold of `row`'s question on a mutated structure / case(s) (solver A), or None."""
        q = row["q"]
        try:
            if q["qtype"] == "Q4":
                X = q["X"]
                res_list = [A.solve(S, c) for c in cases]
                quals = [i for i, r in enumerate(res_list) if r["final"] == X]
                if len(quals) > 1:
                    return None
                return ("none" if not quals else quals[0]), res_list
            res = A.solve(S, cases[0])
            if q["qtype"] == "Q3":
                return A.q3_answer(res, q["X"], q["pol"]), res
            if q["qtype"] == "Q1":
                return (res["final"] if res["det"] else CBD), res
            if q["qtype"] == "Q2":
                return A.q2_pair(res), res
        except (Reject, KeyError):
            return None
        return None

    def base_gold_key(self, row):
        q = row["q"]
        if q["qtype"] == "Q4":
            if row["gold"] == "__NONE__":
                return "none"
            return row["q4_refs"].index(row["gold"])
        return row["gold"]

    def q4_still_valid(self, S, cases, X, row):
        for c in cases:
            pass
        res_list = []
        for i, c in enumerate(cases):
            r = A.solve(S, c)
            res_list.append(r)
            is_q = r["final"] == X
            if is_q:
                continue
            eo = A.error_outputs(S, c, r)
            hits = [E for E, o in eo.items() if o["q1"] == X]
            if len(hits) != 1:
                return False
        return True

    def unit_inert(self, row):
        """M4 (non-firing or beaten general rule) or M5 (inert sentence / distractor date change); gold unchanged."""
        rng = self.rng
        q = row["q"]
        S0, cases0 = row["S"], row["cases"]
        for attempt in range(12):
            S = S0.copy()
            cases = [c.copy(vals=dict(c.vals)) for c in cases0]
            kind = rng.choice(["M4", "M5d", "M5i"])
            if kind == "M5i" and ("inert" not in self.card["constructs"] or self.card["short"]):
                kind = "M5d"
            try:
                if kind == "M5d":
                    ds = [k for k, a in S.attrs.items() if a.role == "distractor"]
                    if not ds:
                        continue
                    k = rng.choice(ds)
                    a = S.attrs[k]
                    for c in cases:
                        c.vals[k] = rng.randint(a.lo, a.hi)
                elif kind == "M5i":
                    lm = SM.LitMaker(S.attrs, self.card, rng)
                    new = SM.draw_inert(S.rules, S.notices, lm, self.card, self.pack, rng, n=1)
                    if not new:
                        continue
                    S.inert = list(S.inert) + new
                else:
                    if q["qtype"] == "Q2":
                        continue
                    src = A.gold_source(row["res"])[0] if row.get("res") else None
                    if q["qtype"] != "Q4" and src not in ("ONE", "MANY"):
                        continue
                    lm = SM.LitMaker(S.attrs, self.card, rng)
                    known = [k for k in lm.usable() if all(k in c.vals for c in cases)]
                    if not known:
                        continue
                    k = rng.choice(known)
                    a = S.attrs[k]
                    # a literal false on every listed case -> the rule never fires (M4 first branch)
                    lit = None
                    for t in range(20):
                        cand = lm.lit(k)
                        if all(A.lit_val(cand, S.attrs, c.vals) is False for c in cases):
                            lit = cand
                            break
                    if lit is None:
                        continue
                    used = {r.rid for r in S.rules} | {n.rule.rid for n in S.notices if n.rule is not None} | \
                           {n.num for n in S.notices}
                    nid = rng.choice([x for x in range(10, 100) if x not in used])
                    extra_items = []
                    if rng.random() < 0.5:
                        try:
                            extra_items = [Item("lit", (lm.lit(avoid=(k,)),))]
                        except SM.DrawFail:
                            extra_items = []
                    o = rng.choice([x for x in self.card["outcomes"] if x != self.card["M"]])
                    nr = Rule(nid, "gen", tuple([Item("lit", (lit,))] + extra_items), None, o)
                    if "PRIORITY" in (self.card["prim"], self.card["sec"]):
                        nr.tier = rng.randrange(len(self.card["tiers"]))
                    if "LATER" in (self.card["prim"], self.card["sec"]):
                        nr.date = S.policy.B - rng.choice([0, 30, 90])
                    pos = rng.randint(0, len(S.rules))
                    S.rules = S.rules[:pos] + [nr] + S.rules[pos:]
                    if S.s3_rows is not None:
                        S.s3_rows = list(S.s3_rows)
                        S.s3_rows.insert(pos, nid)
                    SM.recompute_order(S)
                    if len(S.rules) + len(S.notices) > 12 + 3:
                        continue
                g2 = self.regold(row, S, cases)
                if g2 is None or g2[0] != self.base_gold_key(row):
                    self.stats["inert_dropped"] += 1
                    continue
                if q["qtype"] == "Q4" and not self.q4_still_valid(S, cases, q["X"], row):
                    continue
                if q["qtype"] == "Q1":
                    eo = A.error_outputs(S, cases[0], g2[1])
                    wrong = {o["q1"] for o in eo.values() if o["q1"] in row["options"] and o["q1"] != row["gold"]}
                    if len(wrong) < 2:
                        continue
                d = max(A.depth(S, c)[0] for c in cases)
                if d > 6 or (not row["deep"] and d > 4):
                    continue
                r2 = dict(row)
                r2.update({"S": S, "cases": cases, "role": "variant", "rel": "equiv", "unit_kind": "U-inert",
                           "mr": kind, "depth": d})
                if q["qtype"] != "Q4":
                    r2["res"] = g2[1]
                return [r2]
            except (Reject, SM.DrawFail, KeyError, ValueError, IndexError):
                continue
        return []

    # ---------------------------------------------------------------- contrast twins
    def twin(self, row):
        rng = self.rng
        q = row["q"]
        if q["qtype"] == "Q4":
            return None
        kinds = ["boundary"] * 4 + ["m6", "m6", "m7", "m7"]
        if row["cases"][0].unknown and q["qtype"] in ("Q1", "Q2"):
            kinds += ["reveal"] * 4
        # r1.1: twins also pass the balance checks now, so each kind gets three tries; pass 5: six on Q2 rows, whose
        # twins pass the role|basis-kind depth balance less often (Q2 twin rate fell from 9.9% to 7.8% in pass 4)
        # r2: five tries per kind (eight on Q2): contrast sets were 19.9% of rows in r1.1 (G0 8: 20-25%)
        kinds = kinds * (8 if q["qtype"] == "Q2" else 5)
        rng.shuffle(kinds)
        for kind in kinds:
            S = row["S"].copy()
            case = row["cases"][0].copy(vals=dict(row["cases"][0].vals))
            try:
                if kind == "boundary":
                    if case.unknown:
                        continue
                    dec, base = decisive_literals(S, case.vals, case.notrec)
                    if not dec:
                        continue
                    m = rng.choice(dec)
                    a = S.attrs[m.attr]
                    cur = A.lit_val(m, S.attrs, case.vals)
                    v = satisfy_lit(m, a, not cur, rng)
                    if v is None:
                        continue
                    # nearest value across the threshold (a one-attribute flip at the boundary)
                    T = threshold_of(m, case.vals[m.attr])
                    step = a.step if a.type == "num" else 1
                    for cand in (T, T - step, T + step):
                        if a.lo <= cand <= a.hi:
                            vv = dict(case.vals)
                            vv[m.attr] = cand
                            if A.lit_val(m, S.attrs, vv) != cur:
                                v = cand
                                break
                    case.vals[m.attr] = v
                elif kind == "m6":
                    src, W = A.gold_source(row["res"]) if row.get("res") else (None, None)
                    if src != "ONE" or len(S.rules) < 4:
                        continue
                    rmap = {r.rid: r for r in S.rules}
                    if W not in rmap or rmap[W].kind != "gen":
                        continue
                    if any(n.target == W or (n.pos and n.pos[0] == "after" and n.pos[1] == W) or
                           (n.rule is not None and n.rule.kind in ("pexc", "oexc") and n.rule.target == W)
                           for n in S.notices):
                        continue
                    if any(r.kind in ("pexc", "oexc") and r.target == W for r in S.rules):
                        continue
                    S.rules = [r for r in S.rules if r.rid != W]
                    S.order = [x for x in S.order if x != ("r", W)]
                    if S.s3_rows is not None:
                        S.s3_rows = [x for x in S.s3_rows if x != W]
                elif kind == "m7":
                    g = case.vals[S.policy.gov]
                    cand = [n for n in S.notices if n.edate <= g and A.removal_closure(S, frozenset([n.num])) ==
                            frozenset([n.num])]
                    if not cand:
                        continue
                    n = rng.choice(cand)
                    newd = g + rng.randint(1, 30)
                    S.notices = [x.copy(edate=newd) if x.num == n.num else x for x in S.notices]
                    if not self.r3_ok(S):
                        continue
                elif kind == "reveal":
                    k = rng.choice(sorted(case.unknown))
                    case.vals[k] = SM._rand_val(S.attrs[k], rng)
                    case.unknown = frozenset(case.unknown - {k})
                    SM.fix_presup(S, case)
                g2 = self.regold(row, S, [case])
                if g2 is None or g2[0] is None or g2[0] == row["gold"]:
                    continue
                if q["qtype"] in ("Q1", "Q2") and not self.twin_gold_ok(row, g2[0], g2[1]):
                    self.stats["rej_twin_role"] += 1
                    continue
                res2 = g2[1]
                d, Adec = A.depth(S, case)
                if d > 6 or (not row["deep"] and d > 4):
                    continue
                # r2: twins count in the depth shares too (mild: a twin over the card's depth quota is redrawn half
                # the time, so the contrast-set share does not fall)
                if not row["deep"] and self.depth_quota().over(d) and self.rng.random() < 0.5:
                    self.stats["rej_twin_depth_q"] += 1
                    continue
                if q["qtype"] in ("Q1", "Q2"):
                    if isinstance(g2[0], tuple):
                        tk = self.role_of(g2[0][0]) + "|" + ("cbd" if g2[0][0] == CBD else
                                                           ("code" if isinstance(g2[0][1], str) else "rule"))
                    else:
                        tk = self.role_of(g2[0])
                    if self.rbal.depth_bad(tk, d, len(S.rules)):
                        self.stats["rej_twin_depthbal"] += 1
                        continue
                r2 = dict(row)
                r2.update({"S": S, "cases": [case], "gold": g2[0], "res": res2, "depth": d, "A": Adec,
                           "role": "twin", "twin_kind": kind, "rel": None})
                if q["qtype"] == "Q1":
                    eo = A.error_outputs(S, case, res2)
                    wrong = {o["q1"] for o in eo.values() if o["q1"] in row["options"] and o["q1"] != g2[0]}
                    if g2[0] not in row["options"] or len(wrong) < 2:
                        continue
                    r2["eo"] = eo
                if q["qtype"] == "Q2":
                    eo = A.error_outputs(S, case, res2)
                    errp = {o["q2"] for o in eo.values() if o["q2"] is not None and o["q2"] != g2[0]}
                    opts = set(row["options"])
                    if g2[0] not in opts or not errp <= opts:
                        continue
                    r2["eo"] = eo
                if q["qtype"] == "Q3":
                    r2["eo"] = A.error_outputs(S, case, res2)
                return r2
            except (Reject, SM.DrawFail, KeyError, ValueError, IndexError):
                continue
        return None

    def twin_gold_ok(self, row, g, res=None):
        """r1.1: a choice twin's new gold must keep the card's role-rate and slot balance (twins were 50% default
        gold in r1.0: M6 deletes the winning rule and the default takes over). The base row is booked only when the
        group is emitted, so it is counted here."""
        opts = row["options"]
        ro = self.role_of(g[0] if isinstance(g, tuple) else g)
        shown = self.shown_roles(opts)
        extra = 1 if self.gold_role(row) == ro else 0
        if ro in BAL.SPECIAL and self.rbal.cnt[ro] + extra + 1 > self.rbal.exp[ro] + 2 * shown.get(ro, 0) + \
                BAL.RoleBalance.SLACK_HI:
            return False
        if row["q"]["qtype"] == "Q2":
            # r2 pass C: a Q2 twin's gold class is kept with the same composition-first probability as a base row's
            # ((m_c / k) / p_c, normalized on the row), so twins keep each option at 1/k too
            P = self.q2fprior_b["big" if len(opts) >= 20 else "small"]   # r3 pass C2
            n = sum(P.values())
            caps = self.q2_fcapable()
            gf = self.q2_fclass(g)
            if gf not in caps:
                return False
            cnt = Counter(self.q2_fclass(p) for p in opts)
            pr = {c: (P[c] + 4.0 / len(caps)) / (n + 4.0) for c in caps}
            lam = max([(cnt[c] / len(opts)) / pr[c] for c in caps if cnt[c] > 0] or [1.0])
            soft = str(getattr(self, "seed_key", "")).split("|")[0] in Q2_TWIN_SOFT_SETS   # r3 pass C2 v8
            kf = self.q2_keepf_twin(opts, g) if soft else self.q2_keepf(opts, g, res)
            if self.rng.random() > min(1.0, (cnt[gf] / len(opts)) / (lam * pr[gf]) * kf):
                return False
        if row["q"]["qtype"] == "Q1" and res is not None and self.srcq is not None:
            kq = self.q1_srcq_key(opts, g, res)
            if self.srcq_cnt[kq] + (1 if kq == self.q1_srcq_key(opts, row["gold"], row.get("res")) else 0) >= \
                    self.srcq.get(kq, 0):
                return False   # r3: the twin's (source, longest) cell is full (the base is booked at emission)
        if row["q"]["qtype"] == "Q1":
            tot = sum(self.q1_counts.values()) + 1
            if self.q1_counts[g] + (1 if row["gold"] == g else 0) + 1 > (tot + 1) / len(opts) + 1.5:
                return False
        return True

    def r3_ok(self, S):
        """Notice constraints after a date move (R3)."""
        B = S.policy.B
        for n in S.notices:
            if n.edate <= B or n.ndate < B:
                return False
        # targets in force on the effective date (replay without the in-force re-check is solver work; here: no
        # notice may act on a rule before the rule exists or after it is repealed)
        st = {r.rid: r for r in S.rules}
        for n in sorted(S.notices, key=lambda n: (n.edate, n.num)):
            live = {rid: r for rid, r in st.items() if r.last is None or r.last >= n.edate}
            if n.ntype in ("replace", "repeal") and n.target not in live:
                return False
            if n.ntype == "insert" and n.rule.kind in ("pexc", "oexc") and n.rule.target not in live:
                return False
            if n.pos and n.pos[0] == "after" and n.pos[1] not in live:
                return False
            if n.ntype == "replace":
                st[n.target] = n.rule
            elif n.ntype == "repeal":
                st.pop(n.target, None)
            else:
                st[n.rule.rid] = n.rule
        dates = Counter(n.edate for n in S.notices)
        for d, c in dates.items():
            if c > 1:
                return False
        return True

    # ---------------------------------------------------------------- one selection set
    def build_group(self, deep=False):
        card, rng = self.card, self.rng
        qt = card["qtype"]
        unit = None
        u = rng.random()
        if qt == "Q3" and not card["short"]:
            unit = "neg" if u < 0.14 else "attack" if u < 0.22 else "inert" if u < 0.27 else None
        elif qt == "Q3":
            unit = "inert" if u < 0.05 else None
        elif qt == "Q2":
            unit = "attack" if (u < 0.09 and not card["short"]) else None
        else:
            unit = "attack" if (u < 0.09 and not card["short"]) else "inert" if u < 0.14 else None
        want_twin = qt != "Q4"   # r1.1: 0.45 -> every non-Q4 group tries a twin (contrast sets 20-25%)
        if qt == "Q2" and self.rng.random() >= 0.7:
            want_twin = False    # r3 pass B: Q2 twins at 0.7 (A22 Q2 structures made twins easier: qc contrast 25.6%)
        if qt == "Q3":
            base = self.build_q3(deep=deep, unit_kind=unit, want_twin=want_twin)
        elif qt == "Q1":
            base = self.build_q1(deep=deep)
        elif qt == "Q2":
            base = self.build_q2(deep=deep)
        else:
            base = self.build_q4(deep=deep)
        base["role"] = "base"
        base["rel"] = None
        rows = [base]
        if unit == "neg" and base["q"]["pol"] == "aff":
            rows += self.unit_neg(base)
        elif unit == "attack":
            rows += self.unit_attack(base)
        elif unit == "inert":
            rows += self.unit_inert(base)
        if want_twin:
            t = self.twin(base)
            if t is not None and qt == "Q3" and self.twin_ans[t["gold"]] + 1 > self.twin_ans[1 - t["gold"]] + 3:
                # r1.1: twin rows keep yes = no per card (twins of forced bases are easier to make; the row's
                # role "twin" must not carry the answer)
                self.stats["rej_twin_ans"] += 1
                t = None
            if t is not None:
                rows.append(t)
        if not self.defer_account:
            for x in rows:
                self.account_row(x)
        return rows


# ---------------------------------------------------------------- S2 decisive chains of a target depth

def _satisfy_rule_chain(S, rules, rid, vals, fixed, rng):
    x = rid
    while x is not None and x in rules:
        r = rules[x][0]
        for it in r.all_items():
            if not satisfy_item(it, S, vals, True, rng, fixed):
                return False
        x = r.target if r.kind in ("pexc", "oexc") else None
    return True


def chain_boost(S, case, target, rng, tries=40):
    """S2 label-first: move a drawn structure and case towards a decisive chain of exact section-1 depth `target`
    (1 + exception levels + decisive notices + conflict + only-if fallback) by satisfying chains, adding a conflict,
    putting notices in effect and pointing an only-if rule at the reached outcome. Depth is recomputed exactly by
    solver A after each move; moves that overshoot are undone. Returns True when the depth equals the target."""
    import copy as _c
    P = S.policy
    if case.unknown:
        return False
    for t in range(tries):
        try:
            d, Adec = A.depth(S, case)
        except Reject:
            return False
        if d == target:
            return True
        saved_vals = dict(case.vals)
        saved_rules = [r.copy() for r in S.rules]
        saved_notices = [n.copy() for n in S.notices]
        g = case.vals[P.gov]
        base = A.solve_closed(S, case.vals, case.notrec)
        rules = base["rules"]
        fixed = {P.gov}
        vals = dict(case.vals)
        op = rng.choice(["P", "X", "X", "A", "Ains", "Ains", "O"]) if d < target else rng.choice(["unA"])
        ok = False
        if op == "P":
            outs = [rid for rid, (r, dd, s) in rules.items() if r.kind in ("gen", "oexc")]
            if len(outs) >= 2:
                a, b = rng.sample(outs, 2)
                if rules[a][0].out != rules[b][0].out:
                    ok = _satisfy_rule_chain(S, rules, a, vals, fixed, rng) and \
                        _satisfy_rule_chain(S, rules, b, vals, fixed, rng)
        elif op == "X":
            ex = [rid for rid, (r, dd, s) in rules.items() if r.kind in ("pexc", "oexc")]
            if ex:
                ok = _satisfy_rule_chain(S, rules, rng.choice(ex), vals, fixed, rng)
        elif op == "A":
            later = [n for n in S.notices if n.edate > g]
            if later:
                n = rng.choice(later)
                vals[P.gov] = n.edate + rng.choice([0, 0, 1, 3, 10])
                ok = True
        elif op == "Ains":
            ins = [n for n in S.notices if n.ntype in ("insert", "replace") and n.rule is not None
                   and n.rule.kind in ("gen", "oexc")]
            if ins:
                n = rng.choice(ins)
                vals[P.gov] = max(vals[P.gov], n.edate + rng.choice([0, 1, 5]))
                fixed.add(P.gov)
                r2 = A.solve_closed(S, vals, case.notrec)
                rid = n.rule.rid if n.ntype == "insert" else n.target
                if rid in r2["rules"]:
                    ok = _satisfy_rule_chain(S, r2["rules"], rid, vals, fixed, rng)
        elif op == "O":
            oi = [r for r in S.rules if r.kind == "onlyif"]
            o = base["final"]
            if oi and o not in (P.fallback, P.M, None):
                r = rng.choice(oi)
                r.out = o
                for n in S.notices:
                    if n.ntype == "replace" and n.target == r.rid and n.rule is not None:
                        n.rule = n.rule.copy(out=o)
                for it in r.all_items():
                    if not satisfy_item(it, S, vals, False, rng, fixed):
                        break
                ok = True
        elif op == "unP":
            ok = False
        elif op == "unA":
            inn = [n for n in S.notices if n.edate <= g]
            if inn:
                vals[P.gov] = max(P.B, min(n.edate for n in inn) - rng.randint(1, 10))
                ok = True
        elif op == "unX":
            ok = False
        if not ok:
            case.vals.clear()
            case.vals.update(saved_vals)
            S.rules = saved_rules
            S.notices = saved_notices
            continue
        for k in case.unknown | case.notrec:
            vals.pop(k, None)
        case.vals.clear()
        case.vals.update(vals)
        SM.fix_presup(S, case)
        try:
            d2, _ = A.depth(S, case)
            A.solve(S, case)
        except Reject:
            d2 = 99
        if d2 > target:
            case.vals.clear()
            case.vals.update(saved_vals)
            S.rules = saved_rules
            S.notices = saved_notices
    try:
        return A.depth(S, case)[0] == target
    except Reject:
        return False


def open_boost(S, case, target, rng, tries=40):
    """r2: depth boost for an open-world case. One completion (the stated facts plus drawn values for the unknown
    fields) is moved towards `target` by chain_boost; the same fields are then hidden again. The row's depth is the
    maximum over completions (G0 1), so it is at least the boosted completion's depth; solver A recomputes it."""
    if case.notrec or not case.unknown:
        return False
    unk = case.unknown
    vals = dict(case.vals)
    for k in unk:
        vals[k] = SM._rand_val(S.attrs[k], rng)
    cc = case.copy(vals=vals, unknown=frozenset())
    ok = chain_boost(S, cc, target, rng, tries=tries)
    nv = dict(cc.vals)
    for k in unk:
        nv.pop(k, None)
    case.vals.clear()
    case.vals.update(nv)
    SM.fix_presup(S, case)
    return ok
