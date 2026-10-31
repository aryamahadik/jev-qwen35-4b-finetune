"""F12 question forms on forward rows (G0 1.2, 8, 8.1): display-then-gold (XF01), functional distractors only.

Each builder returns a row spec R:
  {"S", "res", "nm", "form", "qtype", "opts": [canonical option], "gold": canonical option | 1/0 (yes/no),
   "q": {...question args}, "framing", "info"}
Canonical options: ("out", O) ("call", T) ("ask", p) ("unable",) ("answer",) ("tool", T) ("none",) ("param", p)
  ("nothing",) ("value", text) ("novalue",) ("case", i)
"""
from __future__ import annotations

import collections
import datetime as dt

import f12samp as SM
import f12solve_a as A
from f12samp import Reject

OUTS = ["CALL", "ASK", "UNABLE", "ANSWER"]


# ---- balance controller (repair r1; G10 / G6 / G7): every balance target is met on the rows a card actually makes
# (twins, T-NEG units and rejected draws included), not only in expectation on the draws. Each choice is the category
# with the largest deficit (expected so far + this row's share - realised); nothing visible depends on it.
BUCKETS = {"C-TOOL": {"20-60": (20, 32), "10-19": (10, 19), "5-9": (5, 9), "2-4": (3, 4)},
           "C-ACT": {"10-19": (10, 13), "5-9": (5, 9)},
           "C-PARAM": {"2-4": (2, 4), "5-9": (5, 7)},
           "C-VALUE": {"2-4": (2, 4), "5-9": (5, 6)},
           "C-DEFECT": {"2-4": (3, 4), "5-9": (5, 9)},
           "C-INV": {"2-4": (3, 4), "5-9": (5, 6)}}
# option-count bucket targets per form (2.1: 35 / 35 / 15 / 15 of choice rows; G0 8 plan: 20-60 from C-TOOL, 10-19
# from C-TOOL and C-ACT, the rest from all forms); S2 / S4 catalogs are small (bins 3-12), so their C-TOOL k <= 9
# repair r5 (G10 cand buckets on build 15: 5-9 38.6% > 38, 20-60 10.6% < 12; build 14 20-60 12.9%): the 2-4 cuts
# (C-DEFECT, C-INV) moved rows into 5-9, so C-TOOL big 20-60 .62 -> .70 (5-9 .13 -> .08) and C-ACT 10-19 .65 -> .75
# repair r7 (G10 cand buckets on build 17: 20-60 11.89% < 12; C-TOOL big rows 351 of 2,036 cand choice rows, 69% of them
# 20-60; qc 13.4%): C-TOOL big 20-60 .70 -> .78 (10-19 .22 -> .17, 5-9 .08 -> .05); plan: cand 20-60 ~13.4%, 10-19 ~14.9%
BK_TARGET = {"C-TOOL": {"big": {"20-60": 0.78, "10-19": 0.17, "5-9": 0.05}, "small": {"5-9": 0.7, "2-4": 0.3}},
             "C-ACT": {"10-19": 0.75, "5-9": 0.25}, "C-PARAM": {"2-4": 0.25, "5-9": 0.75},
             "C-VALUE": {"2-4": 0.6, "5-9": 0.4},
             # repair r4 (G10 cand buckets: 2-4 at 38.6%): C-DEFECT k was uniform 3-9 per draw, and large-k draws
             # fail more often ("C-DEFECT distractors"), so the rows made held 42% k 3-4 instead of 2/7; the bucket
             # is now drawn against the card's realised mix like the other forms (k uniform inside the bucket)
             "C-DEFECT": {"2-4": 2 / 7, "5-9": 5 / 7},
             # repair r5 (G10 cand buckets 2-4 38.6% > 38 on build 14): C-INV k was uniform 3-6 (half the rows in
             # 2-4); G0 1.2 allows 3-6, so k is drawn by bucket like the other forms, 2-4 on 30% of C-INV rows
             "C-INV": {"2-4": 0.30, "5-9": 0.70}}


def bkt(k):
    return "2-4" if k <= 4 else "5-9" if k <= 9 else "10-19" if k <= 19 else "20-60"


YES_BOUNDS = (0.205, 0.795)  # repair r4: realised per-card yes share kept inside the G0 20-80% band


# repair r9 (G6 yes/no question view on build 20: LR 0.5353 vs chance 0.5037; tmp/t_ynf.py): label-flip twins ride only
# on one truth side (Y-CALLX / Y-FIT / Y-ASK: CALL bases; Y-VALID: invalid calls; Y-DIRECT: by kind), so a pick of that
# side mostly came out as a balanced pair and left the cell where it was, while a pick of the other side always moved
# it. The per-card (form, framing) controller therefore ended most cards with a surplus of other-side singles (Y-CALLX
# qc: N framing 56% yes, P 43%; singles N 91 yes / 51 no), and the question wording (P / N) predicted the gold. Each
# yes/no unit of a form with label-flip twins is now planned as a PAIR (base on the side that takes the twin, learned
# per card; no twin -> Reject; neutral: one yes and one no row in the same framing cell) or a SINGLE (label from the
# deficit controller; label-flip twins removed, so every single moves the cell). Pair share per (sampler, form) =
# build-20 share (tmp/t_pairshare in HANDOFF_repair9), a little higher on the large ones (G10 flip-set rows 20-25%).
PAIR_SHARE = {"S1": {"Y-ASK": 0.48, "Y-CALLX": 0.53, "Y-DIRECT": 0.52, "Y-FIT": 0.25},
              "S2": {"Y-ASK": 0.07, "Y-CALLX": 0.58, "Y-FIT": 0.05},
              "S3": {"Y-VALID": 0.58},
              "S4": {"Y-ASK": 0.03, "Y-CALLX": 0.30, "Y-DIRECT": 0.10},
              "S6": {"Y-ASK": 0.05, "Y-FIT": 0.30}}
PAIR_FAIL_RUN = 3  # consecutive failed pair attempts of a form before one single attempt
PAIR_GIVE_UP = 8  # pair attempts without any success before the card's form makes singles only


class Bal:
    def __init__(self, rng):
        self.rng = rng
        self.n = {}
        self.e = {}
        self.pst = {}  # repair r9: form -> [units, pair units, failed pair run, pair attempts]
        self.plab = {}  # repair r9: (form, framing, label) -> (pair attempts, pairs made)

    def yn_intent(self, form, sampler):
        """repair r9: 'pair' / 'single' for a yes/no unit of a form with label-flip twins on this sampler, else None."""
        tgt = PAIR_SHARE.get(sampler, {}).get(form)
        if not tgt:
            return None
        st = self.pst.setdefault(form, [0, 0, 0, 0])
        if st[3] >= PAIR_GIVE_UP and st[1] == 0:
            return "single"
        if st[2] >= PAIR_FAIL_RUN:
            st[2] = 0
            return "single"
        return "pair" if st[1] < tgt * (st[0] + 1) else "single"

    def pair_label(self, form, framing):
        """repair r9: base label of a pair unit: the label whose pair attempts made a twin most often on this card."""
        sc = {}
        for lab in (0, 1):
            t, k = self.plab.get((form, framing, lab), (0, 0))
            sc[lab] = (k + 1) / (t + 2)
        m = max(sc.values())
        return self.rng.choice([lab for lab in (0, 1) if sc[lab] >= m - 1e-9])

    def yn_try(self, form, framing, label, ok):
        t, k = self.plab.get((form, framing, label), (0, 0))
        self.plab[(form, framing, label)] = (t + 1, k + int(ok))
        st = self.pst.setdefault(form, [0, 0, 0, 0])
        st[3] += 1
        st[2] = 0 if ok else st[2] + 1

    def yn_done(self, form, pair):
        st = self.pst.setdefault(form, [0, 0, 0, 0])
        st[0] += 1
        st[1] += int(pair)

    def choose(self, key, w, hold=(), soft=False):
        """hold: categories that label-flip twins also supply (T-KIND gives ANSWER); a base row takes one only when
        it is at least one row short, so the twins can fill it without pushing it over its target.
        soft (repair r2): draw at random with p(c) ~ max(0, w(c) + (e(c) - n(c)) / 2), the deficit damped by half per
        row. The largest-deficit rule under-draws small-weight categories on short streams (a card makes only a few
        C-ACT rows per bucket, so "Say it cannot be done" / "Answer directly" at 1/k were almost never drawn); the
        damped draw is unbiased and still pulls each card toward its target."""
        n, e = self.n.setdefault(key, {}), self.e.setdefault(key, {})
        if soft:
            pw = {c: (max(0.0, x + 0.5 * (e.get(c, 0.0) - n.get(c, 0)))
                      if c not in hold or e.get(c, 0.0) + x - n.get(c, 0) >= 1.0 else 0.0) for c, x in w.items() if x > 0}
            tot = sum(pw.values())
            if tot > 1e-9:
                r = self.rng.random() * tot
                for c in sorted(pw):
                    r -= pw[c]
                    if r <= 0 and pw[c] > 0:
                        return c
                return max(sorted(pw), key=lambda c: pw[c])
        sc = {c: e.get(c, 0.0) + x - n.get(c, 0) for c, x in w.items() if x > 0}
        if any(c not in hold for c in sc):
            sc = {c: v for c, v in sc.items() if c not in hold or v >= 1.0}
        m = max(sc.values())
        return self.rng.choice(sorted(c for c, v in sc.items() if v >= m - 1e-9))

    def add(self, key, w, got):
        n, e = self.n.setdefault(key, {}), self.e.setdefault(key, {})
        for c, x in w.items():
            e[c] = e.get(c, 0.0) + x
        n[got] = n.get(got, 0) + 1

    def over(self, key, w, got, extra=None, tol=0.25):
        """True if adding a row of category `got` (after `extra` = (w, got) of the base row) would put `got` more
        than a quarter row above its expected count."""
        n, e = dict(self.n.get(key, {})), dict(self.e.get(key, {}))
        for ww, g in ([extra] if extra else []) + [(w, got)]:
            for c, x in ww.items():
                e[c] = e.get(c, 0.0) + x
            n[g] = n.get(g, 0) + 1
        return n[got] > e.get(got, 0.0) + tol

    def yes(self, key, target):
        """repair r4 (G10 card yes rate 20-80: F12-S2-c12 drawn 0.797 came out 0.806): the (form, framing) cells
        hold only a few rows per card and their rounding pushed a card past its rate; the label now follows the
        summed deficit of its cell and of the whole card, and a card's realised yes share (all its yes/no rows,
        negated ones included) never goes past YES_BOUNDS."""
        na = self.n.get(("yn_all",), {})
        tot, ny = na.get(0, 0) + na.get(1, 0), na.get(1, 0)
        if tot >= 8:
            if (ny + 1) / (tot + 1) > YES_BOUNDS[1]:
                return False
            if ny / (tot + 1) < YES_BOUNDS[0]:
                return True
        w = {1: target, 0: 1 - target}
        nk, ek = self.n.get(key, {}), self.e.get(key, {})
        nc, ec = self.n.get(("yn_card",), {}), self.e.get(("yn_card",), {})
        sc = {c: (ek.get(c, 0.0) + x - nk.get(c, 0)) + (ec.get(c, 0.0) + x - nc.get(c, 0)) for c, x in w.items()}
        m = max(sc.values())
        return self.rng.choice(sorted(c for c, v in sc.items() if v >= m - 1e-9)) == 1


def bal(ctx):
    b = getattr(ctx, "bal", None)
    if b is None:
        b = ctx.bal = Bal(ctx.rng)
    return b


# repair r4 (G7 qc "opt:<tool word>" over-gold on single cards): a tool that is seldom a near miss of other requests
# was shown on C-TOOL / C-ACT rows mostly as the gold. Per card, a tool's gold count G(t) and expected count E(t) =
# sum of 1/k over the rows showing it are tracked; near-miss distractors are drawn in order of G - E (over-gold tools
# first, then a random order), and a CALL gold that would put G - E above TEXP_SLACK is redrawn.
# repair r5 (G6 choice a/b/c on build 14: GBT on the option-text SVD +51 rows on C-TOOL; in qc_sample the tool shown
# most often on its card was the gold on 18.5% of C-TOOL rows vs mean 1/k 9.0%, tools shown >= 16 times gold 1.55 x
# their 1/k share): see forward_matched (gold drawn by exposure surplus over TEXP_TRIES draws)
TEXP_SLACK = 0.35  # texp_over (other callers)
TEXP_TRIES = 40
TEXP_FAILS = 8
TEXP_ALPHA = 0.1


def texp_prio(ctx):
    b = bal(ctx)
    n, e = b.n.get(("texp",), {}), b.e.get(("texp",), {})
    return {t: n.get(t, 0) - e.get(t, 0.0) for t in set(n) | set(e)}


def texp_over(ctx, t, k):
    return texp_prio(ctx).get(t, 0.0) + 1.0 - 1.0 / k > TEXP_SLACK


def texp_add(ctx, oc, g):
    b = bal(ctx)
    n, e = b.n.setdefault(("texp",), {}), b.e.setdefault(("texp",), {})
    sh = b.n.setdefault(("tshow",), {})
    k = len(oc)
    for o in oc:
        if o[0] in ("tool", "call"):
            e[o[1]] = e.get(o[1], 0.0) + 1.0 / k
            sh[o[1]] = sh.get(o[1], 0) + 1  # repair r5: times shown as an option on the card
            if tuple(o) == tuple(g):
                n[o[1]] = n.get(o[1], 0) + 1


# repair r5 (G6 choice a/b/c: on build 14 a GBT given only "log times the option is shown on its card" + "is None"
# found the C-TOOL gold on 15.7% of rows vs mean 1/k 9.0%; in 20-60 rows tools shown >= 16 times were gold 1.63 x
# their 1/k share): the gold is always shown, so a tool that is often gold is also shown more. Distractor near misses
# (options and the catalog's near-miss slots) are now taken least-shown first, so show counts level out across a
# cluster whoever is gold; the gold side keeps the exposure balance (forward_matched draws it by E - G surplus).
def tshow_prio(ctx):
    """nm_prio for f12samp.choose_catalog (sorted by -prio): least-shown tools first."""
    sh = bal(ctx).n.get(("tshow",), {})
    return collections.defaultdict(float, {t: -float(v) for t, v in sh.items()})


def texp_sorted(ctx, names):
    """names least-shown first (repair r5; was over-gold first); the incoming (shuffled) order breaks ties."""
    sh = bal(ctx).n.get(("tshow",), {})
    return sorted(names, key=lambda t: sh.get(t, 0))


# repair r4 (G7 cand "depth=2 & Answer directly" over-gold): on C-ACT rows the ANSWER gold sat at depth 2 (record /
# stored answers) while the other golds sit mostly at depth 1. The answer source of a C-ACT ANSWER row is now drawn so
# that its depth follows the realised depth mix of the sampler's other C-ACT rows (user statement = depth 1, record or
# stored result = 2, stored result under a freshness limit = 3). Counts per worker (like SHORT_N in f12build).
ACT_DEPTH = collections.Counter()
ACT_D_PRIOR = {1: 0.66, 2: 0.26, 3: 0.08}


def act_answer_src(ctx, rng, no_stored=False):
    smp = ctx.sampler
    st_ok = smp in ("S2", "S4", "S6") and not no_stored
    has3 = st_ok and ctx.pol.get("fresh") is not None
    feas = [1, 2, 3] if has3 else [1, 2]
    non = {d: ACT_DEPTH[(smp, False, d)] for d in range(1, 7)}
    tn = sum(non.values())
    p = {d: (non[d] + 5 * ACT_D_PRIOR[d]) / (tn + 5) for d in (1, 2, 3)}
    p[3] += sum(non[d] for d in range(4, 7)) / (tn + 5)
    if not has3:
        p[2] += p.pop(3)
    na = {d: ACT_DEPTH[(smp, True, d)] for d in range(1, 7)}
    ta = sum(na.values())
    deficit = {d: p[d] * (ta + 1) - na[d] for d in feas}
    d = max(feas, key=lambda x: (deficit[x], rng.random()))
    if d == 1:
        return "user"
    if d == 3:
        return "stored"
    if st_ok and not has3:
        return rng.choice(["record", "record", "stored"])
    return "record"


# repair r4 (G7 "depth=3 / deep x None" over-gold, "deep x tool option" under-gold): the None gold of C-TOOL (an
# UNABLE row) and "Say it cannot be done" of C-ACT came out deeper than the rows whose gold is a call (several failing
# layers, plus the role layer). The forward structure of such a row is redrawn (same outcome, same options plan) while
# its depth cell would sit more than DEPTH_SLACK rows above the depth mix of the form's other rows; after DEPTH_TRIES
# the least-over draw is kept, so the gold share (drawn first) never changes. Counts per worker, depth 4+ pooled.
DEPTH_FN = None  # f12build.depth_of (set by f12build)
DEPTH_N = collections.Counter()  # (form, cls, depth) -> realised rows
DEPTH_SLACK = 0.5  # repair r6: was 1.0, i.e. one free row per cell per worker; a worker (1 of 16 shards) makes only a
# few abstain-type rows, so nearly every row was free and the redraw never acted (build 16 G7 cand deep x tool option
# under-gold: C-ACT ASK depth 3-4 30% vs CALL 9%, C-TOOL None gold 7 of 23 at depth 4 vs CALL 8 of 455)
DEPTH_TRIES = 24


def depth_cls(form, g):
    if form == "C-TOOL":
        return "abstain" if g[0] == "none" else "other"
    if form == "C-ACT":
        return g[0] if g[0] in ("unable", "answer", "ask") else "other"  # repair r6: + ask (redrawn like unable)
    return None


def depth_over(form, cls, d):
    """rows by which a new (form, cls) row at depth d would exceed the depth mix of the form's 'other' rows"""
    ds = range(1, 5)
    oth = {x: DEPTH_N[(form, "other", x)] for x in ds}
    no = sum(oth.values())
    prior = {1: 0.5, 2: 0.35, 3: 0.11, 4: 0.04}
    p = (oth[d] + 4 * prior[d]) / (no + 4)
    nc = sum(DEPTH_N[(form, cls, x)] for x in ds)
    return DEPTH_N[(form, cls, d)] + 1 - (p * (nc + 1) + DEPTH_SLACK)


def depth_update(form, g, depth):
    c = depth_cls(form, g)
    if c is not None:
        DEPTH_N[(form, c, min(int(depth), 4))] += 1


# repair r7 (build 17 G6 choice d_metadata GBT .2121 / d_literal .2003 vs .1956; G7 qc "request cue info x Answer
# directly" 14 / 2.6, cand "depth 2 x param named in the conversation" 45 / 24.0): the gold class of C-OUT, C-ACT and
# C-PARAM rows followed the visible row structure (C-OUT qc: a stated value on 6 of 132 ANSWER rows vs 63.3 at the
# form's pooled rate, catalog cue 76 vs 41.6, no record 76 vs 41.3, qualifier on 60 ASK rows vs 35.6; C-ACT: info cue
# on 24 of 52 ANSWER rows vs 24 of 339 others; C-PARAM: a stated value on Nothing-gold rows). As depth_over does for
# depth, the forward structure of such a row is now drawn up to MM_TRIES times (same gold class, same option plan)
# and the draw whose structure cells (mm_feats: the G0 8 G6 metadata the structure fixes) sit least above the form's
# pooled mix over all gold classes is kept; the gold share (drawn first) never changes. Counts per worker.
MM_N = collections.Counter()  # (form, feat, cls) / (form, feat, "*") / (form, cls) / (form, "*") -> realised rows
MM_TRIES = 6
MM_SLACK = 0.5
MM_W = 0.3  # C-ACT CALL: texp weight x MM_W ** mm_over
MM_TYPES = ("val", "qual", "corr", "cont", "fact")
MM_FORMS = ("C-OUT", "C-ACT", "C-PARAM")


def mm_cls(form, g):
    """gold class of a row for the structure match (g = gold_canon)."""
    if form == "C-OUT":
        return g[1]
    return g[0]


def mm_feats(S, res, depth=None):
    """visible structure cells of a row (chk_lib.meta_feats names: request cue, statement types, number of stated
    values, records, stored results, shown call, user turns, depth)."""
    conv = S.get("conv") or []
    sts = [st for t in conv for st in (t.get("st") or []) if isinstance(st, dict)]
    types = collections.Counter(st.get("t") for st in sts)
    if depth is None:
        depth = DEPTH_FN({"S": S, "res": res}) if DEPTH_FN is not None else 1
    f = {"cue=" + "+".join(sorted({str(st.get("cue")) for st in sts if st.get("t") == "req"})),
         "nval=%d" % min(types["val"], 3), "rec=%d" % min(len(S.get("records") or []), 2),
         "sto=%d" % min(len(S.get("stored") or []), 1), "call=%d" % (S.get("call") is not None),
         "users=%d" % min(sum(t.get("who") == "user" for t in conv), 3), "depth=%d" % min(int(depth), 4)}
    f |= {"st_%s=%d" % (t, types[t] > 0) for t in MM_TYPES}
    return f


def mm_over(form, cls, feats):
    """rows by which a new (form, cls) row with these cells would exceed the form's pooled cell mix (summed)."""
    tot = MM_N[(form, "*")]
    nc = MM_N[(form, cls)]
    ov = 0.0
    for f in feats:
        p = (MM_N[(form, f, "*")] + 0.5) / (tot + 1.0)
        ov += max(0.0, MM_N[(form, f, cls)] + 1 - (p * (nc + 1) + MM_SLACK))
    return ov


def mm_update(form, g, S, depth):
    if form not in MM_FORMS or not g:
        return
    cls = mm_cls(form, g)
    MM_N[(form, cls)] += 1
    MM_N[(form, "*")] += 1
    for f in mm_feats(S, None, depth):
        MM_N[(form, f, cls)] += 1
        MM_N[(form, f, "*")] += 1


def mm_forward(ctx, form, cls, outcome, w):
    """_forward drawn up to MM_TRIES times; the first draw at or under the pooled structure mix is kept, else the
    least-over one. A failed redraw keeps the draws made (only the first draw's reject is the form's own)."""
    if DEPTH_FN is None:
        return _forward(ctx, outcome, w)
    if outcome == "CALL" and "chain" not in w:  # the chain share of _forward is drawn once, not selected on
        if ctx.pol["chain"] and not w.get("no_chain") and ctx.rng.random() < 0.4:
            w = dict(w, chain=True, kind="action", one_fit=False)
        else:
            w = dict(w, chain=False)
    best = None
    for _t in range(MM_TRIES):
        try:
            d = _forward(ctx, outcome, w)
        except Reject:
            if best is None:
                raise
            break
        ov = mm_over(form, cls, mm_feats(d[0], d[1]))
        if ov <= 0:
            return d
        if best is None or ov < best[0]:
            best = (ov, d)
    return best[1]


def forward_matched(ctx, form, outcome, w, k):
    """_forward with the repair r4 redraws: a CALL whose gold tool is over-exposed on the card (texp) or an
    abstain-type gold row over its depth cell (depth_over) is redrawn with the same outcome; the first clean draw is
    kept, else the least-bad one. Never rejects on these grounds: a reject would redraw the outcome too, and rejecting
    only CALL draws raised the None / UNABLE gold share (build 13 G10 abstain 10-19 tool_none 17.6% vs 7.3%)."""
    cls = {"C-TOOL": {"UNABLE": "abstain"}, "C-ACT": {"UNABLE": "unable", "ASK": "ask"}}.get(form, {}).get(outcome)
    mmc = {"CALL": "call", "ASK": "ask", "UNABLE": "unable", "ANSWER": "answer"}[outcome] if form == "C-ACT" else None
    if outcome != "CALL" and (cls is None or DEPTH_FN is None):
        if mmc is not None:  # repair r7: C-ACT ANSWER rows matched on structure (mm_forward)
            return mm_forward(ctx, form, mmc, outcome, w)
        return _forward(ctx, outcome, w)
    if outcome == "CALL":
        # repair r5: TEXP_TRIES draws, one kept per gold tool, and the gold tool drawn with weight
        # max(0, TEXP_ALPHA + E - G) (exposure surplus; an argmax made the most-shown tool the gold); a failed redraw
        # is skipped (up to TEXP_FAILS), never a reject once one draw stands. In build 14
        # the first draw under the slack was kept, so the gold followed the sampler's own skew (on an S1 card two
        # tools took 97 of 300 CALL draws) and 1,053 of 1,513 shown tools were never gold (qc_sample): tools shown
        # often were the golds (G6 GBT on the option-text SVD). Drawing by surplus spreads the golds over the tools
        # the card shows as distractors.
        # the chain / no-chain draw of _forward is made once here, so selecting among the draws keeps its 40% share
        if ctx.pol["chain"] and not w.get("no_chain") and "chain" not in w and ctx.rng.random() < 0.4:
            w = dict(w, chain=True, kind="action", one_fit=False)
        elif "chain" not in w:
            w = dict(w, chain=False)
        cands, fails, nd = [], 0, 0
        while nd < TEXP_TRIES and fails <= TEXP_FAILS:
            try:
                d = _forward(ctx, outcome, w)
            except Reject:
                if not cands:  # the first draw failing is the form's own reject (as before r5)
                    raise
                fails += 1
                continue
            nd += 1
            if all(c[1]["tool"] != d[1]["tool"] for c in cands):  # one draw per gold tool (removes the skew)
                cands.append(d)
        pr = texp_prio(ctx)
        wt = [max(0.0, TEXP_ALPHA - pr.get(c[1]["tool"], 0.0)) for c in cands]
        if mmc is not None:  # repair r7: C-ACT CALL draws weighted down by their structure surplus (mm_over)
            wt = [v * MM_W ** mm_over(form, mmc, mm_feats(c[0], c[1])) for v, c in zip(wt, cands)]
        if sum(wt) <= 1e-9:
            return min(cands, key=lambda c: pr.get(c[1]["tool"], 0.0))
        x = ctx.rng.random() * sum(wt)
        for c, v in zip(cands, wt):
            x -= v
            if x <= 0 and v > 0:
                return c
        return cands[max(range(len(cands)), key=lambda i: wt[i])]
    best = None
    for _t in range(DEPTH_TRIES):
        if best is None:
            S, res, nm, info = _forward(ctx, outcome, w)
        else:
            try:  # a failed redraw falls back to the kept draw (no extra rejects for this outcome)
                S, res, nm, info = _forward(ctx, outcome, w)
            except Reject:
                break
        if outcome == "CALL":
            ov = texp_prio(ctx).get(res["tool"], 0.0) + 1.0 - 1.0 / k - TEXP_SLACK
        else:
            ov = depth_over(form, cls, min(int(DEPTH_FN({"S": S, "res": res})), 4))
        # repair r7: C-ACT ASK / UNABLE rows also matched on structure (mm_over), checked over the first MM_TRIES draws;
        # the depth cell keeps priority (kept draw = least depth surplus, then least structure surplus)
        om = mm_over(form, mmc, mm_feats(S, res)) if mmc is not None else 0.0
        if ov <= 0 and (om <= 0 or _t + 1 >= MM_TRIES):
            return S, res, nm, info
        key = (max(ov, 0.0), om)
        if best is None or key < best[0]:
            best = (key, (S, res, nm, info))
    return best[1]


def _bucket_k(rng, form, ctx=None):
    """Option counts (2.1 buckets; section 8 plan): bucket by the card's deficit, then k uniform in the bucket."""
    if form not in BUCKETS:
        return 4
    tg = BK_TARGET[form]
    if form == "C-TOOL":
        tg = tg["small"] if ctx is not None and ctx.sampler in ("S2", "S4") else tg["big"]
    b = bal(ctx).choose(("bk", form), tg) if ctx is not None else rng.choice(sorted(tg))
    lo, hi = BUCKETS[form][b]
    return rng.randint(lo, hi)


def bk_weights(ctx, form):
    tg = BK_TARGET[form]
    if form == "C-TOOL":
        tg = tg["small"] if ctx.sampler in ("S2", "S4") else tg["big"]
    return tg


def _forward(ctx, outcome, want, tries=60):
    last = None
    if ctx.pol["chain"] and outcome == "CALL" and not want.get("no_chain") and "chain" not in want \
            and ctx.rng.random() < 0.4:
        want = dict(want, chain=True, kind="action", one_fit=False)
    for _ in range(tries):
        try:
            S, res0, info = SM.build_forward(ctx, outcome, want)
            listed, gold, nm_chosen = SM.choose_catalog(ctx, S, res0, info, outcome, want)
            S2, res, nm = SM.finalize(ctx, S, listed)
            if res["outcome"] != outcome:
                raise Reject(f"solver A gave {res['outcome']} for {outcome}")
            if SM.ng29_bad(S2, res, ctx.pk):
                raise Reject("NG-29")
            if SM.ng55_bad(S2, ctx.pk):
                raise Reject("NG-55")
            if want.get("one_fit"):
                fit = [t for t in S2["tools"] if res["checks"][t["name"]]["fit"]]
                if len(fit) != 1:
                    raise Reject("one_fit")
            if outcome == "ASK" and want.get("unique_ask"):
                fit = [t for t in S2["tools"] if res["checks"][t["name"]]["fit"]]
                ck = res["checks"][fit[0]["name"]]
                probs = ck["missing"] + ck["unclear"] + [r[0] for r in ck["rejects"]]
                if len(probs) != 1:
                    raise Reject("ask target not unique")
            if outcome == "CALL" and res.get("tie") and not want.get("tie"):
                raise Reject("unplanned tie")
            if res.get("chain") and not want.get("chain"):
                raise Reject("unplanned chain")
            if len(nm) < want.get("need_nm", 1) and info["kind"] != "catalog":
                raise Reject("near-miss count")
            return S2, res, nm, info
        except Reject as e:
            last = e
        except AssertionError as e:
            last = e
    raise Reject(f"forward failed: {last}")


def fitting(S, res):
    return [t for t in S["tools"] if res["checks"][t["name"]]["fit"]]


# ------------------------------------------------------------------------------------------------ choice forms
def c_out(ctx, rng, want):
    outcome = want.get("outcome") or bal(ctx).choose(("out",), {o: 0.25 for o in OUTS}, hold=_hold(ctx, "ANSWER"))
    S, res, nm, info = mm_forward(ctx, "C-OUT", outcome, outcome, want)  # repair r7: structure-matched draw
    opts = [("out", o) for o in OUTS]
    rng.shuffle(opts)
    return {"S": S, "res": res, "nm": nm, "form": "C-OUT", "qtype": "choice", "opts": opts,
            "gold": ("out", outcome), "q": {}, "info": info}


def _hold(ctx, ans):
    return (ans,) if ctx.sampler in ("S1", "S2") else ()  # samplers whose twins include T-KIND (G0 section 4)


ACT_PEND_MAX = 6  # repair r7: tries kept for a failed C-ACT class (c_act)


def act_pend_clear(ctx, k):
    pend = ctx.__dict__.get("_act_pend")
    if pend:
        pend.pop(bkt(k), None)


def act_weights(n_call, n_ask, k):
    return {"call": n_call / k, "ask": n_ask / k, "unable": 1 / k, "answer": 1 / k}


def c_act(ctx, rng, want):
    k = _bucket_k(rng, "C-ACT", ctx)
    n_ask = rng.randint(1, 3)
    n_call = k - 2 - n_ask
    if n_call > 8:
        n_ask = min(3, k - 2 - 8)
        n_call = k - 2 - n_ask
    if n_call < 2:
        raise Reject("C-ACT k")
    # display-then-gold (R3-SC2): the option set is drawn first; the gold kind follows the card's deficit against
    # 1/k per shown option, so every option (Say it cannot be done, Answer directly) is gold at 1/k on the rows made
    kind = bal(ctx).choose(("act", bkt(k)), act_weights(n_call, n_ask, k), soft=True)  # r2: no hold, soft draw
    # repair r7 (build 17 base C-ACT rows qc: Answer directly gold 50 vs 36.6 expected, call 193 vs 210.3; cand 37 vs
    # 31.9, 166 vs 180.4): a drawn class whose row then failed (CALL rows with many near misses fail most) was redrawn
    # from scratch, so the realised mix followed the success rates. A failed class is now kept for the card's next
    # C-ACT row in the bucket (at most ACT_PEND_MAX tries), so the realised mix follows the draw.
    pend = ctx.__dict__.setdefault("_act_pend", {})
    pk_ = bkt(k)
    if pk_ in pend and pend[pk_][1] < ACT_PEND_MAX and (pend[pk_][0] != "ask" or n_ask > 0):
        kind = pend[pk_][0]
        pend[pk_] = (kind, pend[pk_][1] + 1)
    else:
        pend[pk_] = (kind, 1)
    outcome = {"call": "CALL", "ask": "ASK", "unable": "UNABLE", "answer": "ANSWER"}[kind]
    w = dict(want)
    need_call_d = n_call - (1 if outcome in ("CALL", "ASK") else 0)
    w.update(need_nm=need_call_d, one_fit=outcome == "ASK", unique_ask=True, cluster=need_call_d >= 4)
    if outcome == "ANSWER":
        w.update(need_nm=need_call_d)
        if not w.get("answer_src"):
            w["answer_src"] = act_answer_src(ctx, rng, bool(w.get("no_stored")))  # repair r4: depth-matched answer source
    w["nm_prio"] = tshow_prio(ctx)  # repair r5: least-shown near misses first (was r4 over-gold first)
    S, res, nm, info = forward_matched(ctx, "C-ACT", outcome, w, k)
    by = {t["name"]: t for t in S["tools"]}
    nm_tools = [n for n, _ in nm]
    rng.shuffle(nm_tools)
    nm_tools = texp_sorted(ctx, nm_tools)
    calls = []
    if outcome == "CALL":
        calls.append(res["tool"])
    elif outcome == "ASK":
        calls.append(fitting(S, res)[0]["name"])
    calls += nm_tools[: n_call - len(calls)]
    if len(calls) < n_call:
        raise Reject("C-ACT call distractors")
    # ask options
    asks = []
    gold = None
    if outcome == "ASK":
        T = fitting(S, res)[0]
        ck = res["checks"][T["name"]]
        p = (ck["missing"] + ck["unclear"] + [r[0] for r in ck["rejects"]])[0]
        asks.append(p)
        gold = ("ask", p)
    pool = []
    if outcome in ("CALL", "ASK"):
        T = by[res["tool"]] if outcome == "CALL" else fitting(S, res)[0]
        tn = {p["name"] for p in T["params"]}
        pool += [p["name"] for p in T["params"] if p["name"] in res["vals"]]
        for n in nm_tools:
            for p in by[n]["params"]:
                if p["required"] and p["name"] not in tn:
                    pool.append(p["name"])
    else:
        for t in S["tools"]:
            if not t.get("borrowed"):
                pool += [p["name"] for p in t["params"]]
    pool = [p for p in dict.fromkeys(pool) if p not in asks]
    rng.shuffle(pool)
    # repair r3 (G7 opt:id): ask distractors follow the realised (named, ID) mix of the ask golds
    pc = param_cat(S, conv_named(S))
    asks += pick_matched(ctx, "cask", pool, n_ask - len(asks), pc, pc(asks[0]) if asks else None)
    if len(asks) < n_ask:
        raise Reject("C-ACT ask distractors")
    opts = [("call", c) for c in calls] + [("ask", p) for p in asks] + [("unable",), ("answer",)]
    if outcome == "CALL":
        gold = ("call", res["tool"])
    elif outcome == "UNABLE":
        gold = ("unable",)
    elif outcome == "ANSWER":
        gold = ("answer",)
    rng.shuffle(opts)
    return {"S": S, "res": res, "nm": nm, "form": "C-ACT", "qtype": "choice", "opts": opts, "gold": gold,
            "q": {}, "info": info}


def c_tool(ctx, rng, want):
    k = _bucket_k(rng, "C-TOOL", ctx)
    show_none = k >= 3 and rng.random() < 0.5
    # repair r9: the None-of-these gold is drawn by the card balance controller (as Nothing on C-PARAM): qc build 20
    # None gold 18 / 305 rows vs sum 1/k 23.5 (UNABLE attempts rejected more often than CALL ones)
    unable = show_none and bal(ctx).choose(("nn", bkt(k)), {"nn": 1 / k, "c": 1 - 1 / k}, soft=True) == "nn"
    outcome = "UNABLE" if unable else "CALL"
    need = k - 1 - (1 if show_none and outcome == "CALL" else 0)
    if outcome == "UNABLE":
        need = k - 1
    w = dict(want)
    big = need >= 9
    w.update(need_nm=need, cluster=need >= 4, kind="action" if big else None, info_ok=not big,
             bin=(max(need + 1, 26), 60) if need >= 19 else ((max(need + 1, 13), 25) if need >= 9 else None))
    if w["bin"] is None:
        w.pop("bin")
    w["nm_prio"] = tshow_prio(ctx)  # repair r5: least-shown near misses first (was r4 over-gold first)
    S, res, nm, info = forward_matched(ctx, "C-TOOL", outcome, w, k)
    nm_tools = [n for n, _ in nm]
    rng.shuffle(nm_tools)
    nm_tools = texp_sorted(ctx, nm_tools)
    opts = [("tool", n) for n in nm_tools[:need]]
    if len(opts) < need:
        raise Reject("C-TOOL distractors")
    gold = ("tool", res["tool"]) if outcome == "CALL" else ("none",)
    if outcome == "CALL":
        opts.append(gold)
    if show_none:
        opts.append(("none",))
    rng.shuffle(opts)
    return {"S": S, "res": res, "nm": nm, "form": "C-TOOL", "qtype": "choice", "opts": opts, "gold": gold,
            "q": {}, "info": info}


def conv_named(S):
    """Params a user or fact statement names in the conversation (the G7 feature "param named in the text")."""
    return {st.get("p") for c in S.get("conv") or [] for st in c.get("st") or [] if st.get("p")}


GOLD_CAT = collections.defaultdict(collections.Counter)  # repair r6: (key) -> gold categories realised on this worker


def pick_matched(ctx, key, cands, n, cat, gold_cat):
    """repair r3 (G7 opt:id under-gold, G6 b/d): like pick_named_matched but over a categorical option feature (here
    "param named in the conversation" x "param is an ID"): the n distractors' category shares follow the realised
    category shares of the golds on this card (soft balance draw); gold_cat None for an abstain gold (not counted)."""
    b = bal(ctx)
    cats = ("yi", "yv", "ni", "nv")
    if gold_cat is not None:
        b.add((key, "g"), {c: 1.0 for c in cats}, gold_cat)
        GOLD_CAT[key][gold_cat] += 1
    ng = b.n.get((key, "g"), {})
    tot = sum(ng.get(c, 0) for c in cats)
    # repair r6 (G7 / G6 "param named in the conversation" under-gold on C-PARAM 5 / 13.7 cand, 12 / 18.0 qc, and
    # C-DEFECT): the one pseudo-row was spread evenly (0.25 per category), so on a card with few golds about half a
    # distractor in ten was named against ~3% of golds; the pseudo-row now follows the worker's gold category mix
    gt = sum(GOLD_CAT[key].values())
    pi = {c: (ng.get(c, 0) + (GOLD_CAT[key][c] + 0.25) / (gt + 1.0)) / (tot + 1.0) for c in cats}
    pools = {c: [x for x in cands if cat(x) == c] for c in cats}
    out = []
    for _ in range(n):
        live = [c for c in cats if pools[c]]
        if not live:
            break
        c = b.choose((key, "d"), pi, soft=True)
        if not pools[c]:
            c = max(live, key=lambda x: (pi[x], -cats.index(x)))
        out.append(pools[c].pop(0))
        b.add((key, "d"), pi, c)
    return out


# repair r8 (G6 choice d_metadata LR .1999 > .1967 on build 18; ablation tmp/t_dabl.log: dropping "param named in
# the conversation" cut the C-DEFECT excess 18.9 -> 3.9 and C-PARAM 13.8 -> 4.8): the category match above keeps the
# pooled named share, but not the per-row structure. The gold was the odd one out (C-DEFECT rows with exactly one named
# param option: gold named 32 / 60 qc, exp 21.0; 36 / 63 cand, exp 17.6; rows with more named options: gold named
# 61 / 165, exp 82.4; tmp/t_pnc2.py). The number of named distractors on a param-gold row is now chosen so that the
# two "pick the named / pick the unnamed options" scores stay at chance on this worker: NB[key] = [S+, S-], where a row
# with m named of k options adds (hit / m - 1 / k, (1 - hit) / (k - m) - 1 / k). Distractors stay category-matched
# (pick_matched) inside the named / unnamed sub-pools.
NB = collections.defaultdict(lambda: [0.0, 0.0])
NB_SLACK = 1.0  # a row that would leave |S+| + |S-| above this and above its current value is redrawn


def named_inc(gin, m, k):
    """(pick-a-named-option excess, pick-an-unnamed-option excess) of one row: m named of k options (abstain options
    count as unnamed), gin = the gold is named; uniform pick inside the set, minus the 1 / k chance."""
    a = ((1.0 / m if gin else 0.0) - 1.0 / k) if m >= 1 else 0.0
    b = ((0.0 if gin else 1.0 / (k - m)) - 1.0 / k) if k - m >= 1 else 0.0
    return a, b


def named_note(key, gin, m, k):
    """Record a row whose named count was not chosen here (abstain-gold rows)."""
    a, b = named_inc(gin, m, k)
    NB[key][0] += a
    NB[key][1] += b


def named_choose(key, gy, k, feas, rng, pref=None):
    """Pick the number of named distractors md from feas for a param gold of named status gy on a row of k options:
    least |S+| + |S-| after the row, ties to the md closest to pref (the category-matched count), then random.
    Updates NB[key]."""
    st = NB[key]
    best = []
    for md in feas:
        a, b = named_inc(gy, md + (1 if gy else 0), k)
        sc = round(abs(st[0] + a) + abs(st[1] + b), 9)
        best.append((sc, abs(md - pref) if pref is not None else 0, rng.random(), md, a, b))
    best.sort()
    sc, _, _, md, a, b = best[0]
    if sc > max(abs(st[0]) + abs(st[1]), NB_SLACK) + 1e-9:
        raise Reject(f"{key} named balance")  # no distractor mix keeps the balance: redraw the row
    st[0] += a
    st[1] += b
    return md


def named_pref(key, n):
    """The category-matched number of named distractors: n x the named share of the golds on this worker."""
    g = GOLD_CAT[key]
    tot = sum(g.values())
    sh = (g["yi"] + g["yv"] + 0.25) / (tot + 1.0)
    return n * sh


def cat_pos(S, x):
    """(index of the first listed tool whose schema has param x, index in that schema): the order in which the card
    first shows the param names (the catalog is rendered in S["tools"] order; agrees with the text order on 226 of
    228 build-16 qc C-PARAM rows)."""
    for i, t in enumerate(S["tools"]):
        for j, p in enumerate(t["params"]):
            if p["name"] == x:
                return (i, j)
    return (len(S["tools"]), 0)


def cpar_rank_pick(ctx, S, pool, gold, n_par, pc, key="cpar2", k_row=None):
    """repair r6 (G6 b_options LR on build 16, POSK "first / last in text" on C-PARAM): the gold (the first missing
    param of the target) came before the other shown params (first 67 of 228 qc rows vs 58.6 at a uniform rank,
    last 42; a target distractor followed the gold in its schema on 56 of 66 rows vs 32.5), since required params are
    listed before optional ones and the gold's name is often on several listed tools. The gold's rank among the
    shown params (catalog order) is now drawn first (first / middle / last, soft balance per card against a uniform
    rank) and the distractors are picked before / after the gold to match (category matched as before)."""
    m = n_par
    g = cat_pos(S, gold)
    before = [x for x in pool if cat_pos(S, x) < g]
    after = [x for x in pool if cat_pos(S, x) > g]
    b = bal(ctx)
    w = {"first": 1.0 / m, "last": 1.0 / m, "mid": (m - 2.0) / m} if m >= 3 else {"first": 0.5, "last": 0.5}
    if m < 2:
        return []
    c = b.choose(("cpar_rank",), w, soft=True)
    t = 0 if c == "first" else (m - 1 if c == "last" else ctx.rng.randint(1, m - 2))
    nb = min(t, len(before))
    na = min(m - 1 - nb, len(after))
    nb = min(len(before), m - 1 - na)
    got = "first" if nb == 0 else ("last" if nb == m - 1 else "mid")
    b.add(("cpar_rank",), w, got)
    # repair r8 (G6 d LR: C-PARAM "param named in the conversation" x metadata, NB above): the number of named
    # distractors is chosen by the worker's named balance, split over the before / after sides
    isy = lambda x: pc(x)[0] == "y"  # noqa: E731
    by_, bn_ = [x for x in before if isy(x)], [x for x in before if not isy(x)]
    ay_, an_ = [x for x in after if isy(x)], [x for x in after if not isy(x)]
    rb = range(max(0, nb - len(bn_)), min(nb, len(by_)) + 1)
    ra = range(max(0, na - len(an_)), min(na, len(ay_)) + 1)
    feas = sorted({u + v for u in rb for v in ra})
    md = named_choose("C-PARAM", isy(gold), k_row, feas, ctx.rng, named_pref(key, nb + na))
    splits = [u for u in rb if md - u in ra]
    mb = ctx.rng.choice(splits)
    out = pick_matched(ctx, key, by_, mb, pc, pc(gold)) + pick_matched(ctx, key, bn_, nb - mb, pc, None)
    out += pick_matched(ctx, key, ay_, md - mb, pc, None) + pick_matched(ctx, key, an_, na - (md - mb), pc, None)
    return out


def param_cat(S, cn):
    """Category of a param option: named in the conversation (y/n) x ID type (i/v)."""
    ids = {p["name"] for t in S["tools"] for p in t["params"] if p["type"] == "id"}
    return lambda x: ("y" if x in cn else "n") + ("i" if x in ids else "v")


def pick_named_matched(ctx, key, cands, n, named, gold_named):
    """repair r2 (G6 b/d, G7 "param named in the conversation"): pick n distractor options so that the share of
    distractors whose param the conversation names follows the realised share of golds whose param it names on this
    card (soft balance draw), instead of whatever share the candidate pool happens to have. gold_named: True / False
    for a param gold, None for an abstain gold (not counted)."""
    b = bal(ctx)
    if gold_named is not None:
        b.add((key, "g"), {"y": 1.0}, "y" if gold_named else "n")
    ng = b.n.get((key, "g"), {})
    pi = (ng.get("y", 0) + 0.25) / (ng.get("y", 0) + ng.get("n", 0) + 1.0)
    ys = [c for c in cands if named(c)]
    ns = [c for c in cands if not named(c)]
    out = []
    for _ in range(n):
        if not ys and not ns:
            break
        w = {"y": pi, "n": 1.0 - pi}
        c = b.choose((key, "d"), w, soft=True)
        if c == "y" and not ys:
            c = "n"
        elif c == "n" and not ns:
            c = "y"
        out.append((ys if c == "y" else ns).pop(0))
        b.add((key, "d"), w, c)
    return out


def c_param(ctx, rng, want):
    k = _bucket_k(rng, "C-PARAM", ctx)
    show_nothing = k >= 3 and rng.random() < 0.5
    # repair r9 (G6 choice b / d on build 20: qc "Nothing is missing" gold 40 / 117 rows vs sum 1/k 23.3): the Nothing
    # gold was a 1/k draw, and param-gold attempts are rejected more often (named balance, rank balance), so Nothing
    # came out over its share. It is now drawn by the card balance controller (damped deficit, as C-ACT), which
    # re-draws the short class after rejections; counted in f12build.bal_update ("np", bucket).
    nothing = show_nothing and bal(ctx).choose(("np", bkt(k)), {"np": 1 / k, "p": 1 - 1 / k}, soft=True) == "np"
    outcome = "CALL" if nothing else "ASK"
    w = dict(want)
    w.update(one_fit=True, unique_ask=True, kind="action", need_nm=1, no_chain=True, no_id_problem=True)
    # repair r2 (G6 / G7 "param named in the conversation"): a named problem (unclear, not accepted) made the gold the
    # only named option on most rows; the missing value is now mostly wholly absent, and accepted values are named
    # more often (G0 8: >= 50% unnamed holds on CALL rows; C-PARAM rows are ASK rows apart from Nothing-gold rows)
    if outcome == "ASK":
        x = rng.random()
        if x < 0.7:
            w["ask_kind"] = "absent"
        elif x < 0.85:
            w["ask_kind"] = "unclear"
    w["p_unnamed"] = 0.2
    S, res, nm, info = mm_forward(ctx, "C-PARAM", "param" if outcome == "ASK" else "nothing", outcome, w)  # repair r7
    T = fitting(S, res)[0]
    ck = res["checks"][T["name"]]
    by = {t["name"]: t for t in S["tools"]}
    gold = ("nothing",)
    params = []
    cn = conv_named(S)
    if outcome == "ASK":
        p = (ck["missing"] + ck["unclear"] + [r[0] for r in ck["rejects"]])[0]
        gold = ("param", p)
        params.append(p)
    # repair r2: the target's own ID param (given by the request's reference) is never the missing value on these
    # rows, so it is not offered either (it was a never-gold option, listed first in every schema)
    tid = {q["name"] for q in T["params"] if q["type"] == "id" and res["vals"].get(q["name"]) == info.get("eid")}
    tn = {p["name"] for p in T["params"]}
    pool = [p["name"] for p in T["params"] if p["name"] in res["vals"] and p["name"] not in tid]
    for n, _c in nm:
        for p in by[n]["params"]:
            if p["required"] and p["name"] not in tn and p["name"] not in tid:
                pool.append(p["name"])
    pool = [p for p in dict.fromkeys(pool) if p not in params]
    rng.shuffle(pool)
    n_par = k - (1 if show_nothing else 0)
    pc = param_cat(S, cn)
    # repair r7 (build 17 G7 cand "depth 2 x param named in the conversation" 45 / 24.0, depth 1 under): the named /
    # ID category match is kept per depth (1 / 2 / 3+); a problem value (depth 2) is named, an absent one is not
    pkey = ("cpar2", min(int(DEPTH_FN({"S": S, "res": res})), 3)) if DEPTH_FN is not None else "cpar2"
    if params:
        params += cpar_rank_pick(ctx, S, pool, params[0], n_par, pc, pkey, k_row=k)
    else:
        params += pick_matched(ctx, pkey, pool, n_par - len(params), pc, None)
        named_note("C-PARAM", False, sum(pc(x)[0] == "y" for x in params), k)  # repair r8
    if len(params) < n_par:
        raise Reject("C-PARAM distractors")
    opts = [("param", p) for p in params] + ([("nothing",)] if show_nothing else [])
    rng.shuffle(opts)
    # repair r8: unshown distractors and the named class of every param option, for the text-rank balance at render
    # time (f12build.rank_fix)
    alt = [("param", p) for p in pool if p not in params]
    acat = {p: pc(p)[0] for p in list(pool) + params}
    return {"S": S, "res": res, "nm": nm, "form": "C-PARAM", "qtype": "choice", "opts": opts, "gold": gold,
            "q": {"tool": T["name"]}, "info": info, "alt": alt, "alt_cat": acat}


def c_value(ctx, rng, want):
    """S4: which value should be used for <p> of <T>? (gold = full step-1 value, or No usable value).
    repair r2 (G6 b/d, G7 "option in text"): the value options of a row all come from one source class: every one is
    written in the row (records, stored results, tool turns, user statements, T's listed members), or none is (derived
    values: relative dates, one-error neighbours, guesses). So "this value is written in the text" carries no
    information about the gold; on rows that show "No usable value" the class mix is kept equal on value-gold and
    No-usable-value-gold rows by the card balance controller."""
    k = _bucket_k(rng, "C-VALUE", ctx)
    show_nv = k >= 3 and rng.random() < 0.5
    novalue = show_nv and bal(ctx).choose(("nv", bkt(k)), {"nv": 1 / k, "v": 1 - 1 / k}) == "nv"
    n_val = k - (1 if show_nv else 0) - (0 if novalue else 1)
    last = None
    for _ in range(10):
        w = dict(want)
        w.update(one_fit=True, kind="action", need_nm=1, no_chain=True, corr_v=True)
        if n_val <= 1 or rng.random() < 0.5:
            w.update(p_look=1.0, look_rec=True)  # a look-alike record: an in-text one-error ID (SEM-09, NG-32)
        outcome = "ASK" if novalue else rng.choice(["CALL", "ASK"])
        if novalue:
            w.update(unique_ask=True, ask_kind=rng.choice(["absent", "unclear"]))
        try:
            S, res, nm, info = _forward(ctx, outcome, w)
            T = fitting(S, res)[0]
            ck = res["checks"][T["name"]]
            now = S["now"]
            if novalue:
                probs = ck["missing"] + ck["unclear"]
                if not probs or ck["rejects"]:
                    raise Reject("novalue problem")
                p = next(q for q in T["params"] if q["name"] == probs[0])
                if p["default"] is not None:
                    raise Reject("default")
                gold = ("novalue",)
                cin, cout = _split_shown(S, p, _wrong_values(S, res, p, None, rng))
                ok = [c for c, xs in (("in", cin), ("out", cout)) if len(xs) >= n_val]
                if not ok:
                    raise Reject(f"C-VALUE nv distractors {p['type']} k={k}")
                vw = _vcls_w(ctx)
                cls = ok[0] if len(ok) == 1 else bal(ctx).choose(("vcls", "nv"), vw)
                bal(ctx).add(("vcls", "nv"), vw, cls)
                cands = cin if cls == "in" else cout
            else:
                good = [q for q in T["params"] if q["name"] in res["vals"] and A.accept(q, res["vals"][q["name"]], now)[0]
                        and (q["required"] or q["default"] is not None)]
                good = [q for q in good if q["type"] in ("date", "id", "integer", "decimal", "enum")]
                feas = []
                for q in good:
                    gv = _canon(q, res["vals"][q["name"]], now)
                    cin, cout = _split_shown(S, q, [c for c in _wrong_values(S, res, q, gv, rng) if c != gv])
                    g_in = gv in _shown_for(S, q)
                    xs = cin if g_in else cout
                    if len(xs) >= n_val:
                        feas.append((q, gv, xs, g_in))
                if not feas:
                    raise Reject(f"C-VALUE no matched-class param k={k}")
                p, gv, cands, g_in = rng.choice(feas)
                gold = ("value", gv)
                if show_nv:
                    bal(ctx).add(("vcls", "v"), {"in": 1.0}, "in" if g_in else "out")
            break
        except Reject as e:
            last = e
    else:
        raise Reject(f"C-VALUE: {last}")
    cands = [c for c in dict.fromkeys(cands) if gold != ("value", c)]
    if len(cands) < n_val:
        raise Reject(f"C-VALUE distractors {p['type']} nv={novalue} k={k} have={len(cands)}")
    opts = [("value", c) for c in cands[:n_val]]
    if not novalue:
        opts.append(gold)
    if show_nv:
        opts.append(("novalue",))
    rng.shuffle(opts)
    # repair r8: unshown same-class distractors, for the text-rank balance at render time (f12build.rank_fix)
    return {"S": S, "res": res, "nm": nm, "form": "C-VALUE", "qtype": "choice", "opts": opts, "gold": gold,
            "q": {"tool": T["name"], "param": p["name"]}, "info": info, "alt": [("value", c) for c in cands[n_val:]],
            "alt_cat": None}


def _leaves(x, out):
    if isinstance(x, str):
        out.add(x)
        if len(x) >= 16 and x[4:5] == "-" and x[10:11] in (" ", "T"):
            out.add(x[:10])  # date part of a date-time stamp
    elif isinstance(x, dict):
        for v in x.values():
            _leaves(v, out)
    elif isinstance(x, (list, tuple)):
        for v in x:
            _leaves(v, out)
    return out


def _shown_for(S, p):
    """Strings that may be written in the row for p's options (a superset guess; the rendered row is checked in
    f12build): every string of the structure (statements, references, records, stored results, tool turns, the
    current date, the catalog), T's listed members of p, and p's own limits and default in T's form."""
    xs = _shown_strings(S) | _leaves([S.get("conv"), S.get("records"), S.get("stored"), S.get("now"),
                                      S.get("tools"), S.get("call")], set()) | set(p.get("members") or [])
    u = (" " + p["unit"]) if p.get("unit") else ""
    for lim in (p.get("min"), p.get("max")):
        if lim:
            xs.add(str(lim[0]))
            try:
                xs.add(SM.L.fmt_dec(SM.L.Decimal(str(lim[0]))) + u)
            except Exception:
                pass
    if p.get("default") is not None:
        xs.add(str(p["default"]))
    return xs


def _split_shown(S, p, cands):
    sh = _shown_for(S, p)
    cands = list(dict.fromkeys(cands))
    return [c for c in cands if c in sh], [c for c in cands if c not in sh]


def _vcls_w(ctx):
    """Class weights for a No-usable-value-gold row: the realised in-text share of this card's value-gold rows that
    show No usable value (0.5 before any)."""
    n = bal(ctx).n.get(("vcls", "v"), {})
    tot = n.get("in", 0) + n.get("out", 0)
    pin = (n.get("in", 0) + 0.5) / (tot + 1.0)
    return {"in": pin, "out": 1 - pin}


def _canon(p, text, now):
    ok, v = A.accept(p, text, now)
    assert ok
    if p["type"] in ("integer", "decimal"):
        return SM.L.fmt_dec(v) + (" " + p["unit"] if p.get("unit") else "")
    return str(v)


def _shown_strings(S):
    xs = set()
    for r in S.get("records") or []:
        xs.update(str(v) for _, v in r["fields"])
    for r in S.get("stored") or []:
        xs.update(str(v) for _, v in r["fields"])
    for c in S.get("conv") or []:
        for f in c.get("fields") or []:
            xs.add(str(f[1]))
        for st in c.get("st") or []:
            if st.get("v") is not None:
                xs.add(str(st["v"]))
    return xs


def _wrong_values(S, res, p, gv, rng):
    """One-error values in T's own form (SEM-46): off by one day, superseded, look-alike, neighbouring value."""
    now = S["now"]
    out = []
    if p["type"] == "date" and gv:
        d = dt.date.fromisoformat(gv)
        out += [(d + dt.timedelta(days=x)).isoformat() for x in (1, -1, 7, -7)]
    if p["type"] == "id":
        for r in S["records"]:
            f = dict(r["fields"])
            if p["name"] in f and f[p["name"]] != gv:
                out.append(f[p["name"]])
        if gv and gv.startswith(p["prefix"]):
            # look-alike IDs in T's form: two neighbouring characters swapped, or one character changed
            pre, suf = p["prefix"], gv[len(p["prefix"]):]
            LOOK = {"0": "8", "8": "0", "1": "7", "7": "1", "5": "6", "6": "5", "3": "8", "O": "Q", "Q": "O",
                    "B": "8", "S": "5", "E": "F", "F": "E", "M": "N", "N": "M"}
            for i in range(len(suf) - 1):
                if suf[i] != suf[i + 1]:
                    out.append(pre + suf[:i] + suf[i + 1] + suf[i] + suf[i + 2:])
            for i, ch in enumerate(suf):
                alt = LOOK.get(ch) or (str((int(ch) + 1) % 10) if ch.isdigit() else None)
                if alt:
                    out.append(pre + suf[:i] + alt + suf[i + 1:])
            out = [o for o in out if A.form_ok(p, o, now)]
    # superseded user values (in-message or earlier-turn statements replaced later)
    for c in S["conv"]:
        if c["who"] == "user":
            for st in c["st"]:
                if st["t"] == "val" and st["p"] == p["name"] and st["v"]:
                    ok, v = A.accept(p, st["v"], now)
                    if ok:
                        cv = _canon(p, st["v"], now)
                        if cv != gv:
                            out.append(cv)
    if p["type"] == "enum":
        out += [m for m in p["members"] if m != gv]
    if p["type"] in ("integer", "decimal") and gv:
        u = (" " + p["unit"]) if p.get("unit") else ""
        base = SM.L.Decimal(gv.split(" ")[0])
        step = 1 if p["type"] == "integer" else SM.L.Decimal(1).scaleb(-p["places"])
        out += [SM.L.fmt_dec(base + step) + u, SM.L.fmt_dec(max(base - step, SM.L.Decimal(0))) + u,
                SM.L.fmt_dec(base + 2 * step) + u, SM.L.fmt_dec(base * 10) + u]
    rng.shuffle(out)
    # repair r1 (G7 / G6 "option in text"): wrong values that are written somewhere in the row (records, stored results,
    # tool turns, user statements) come first, so the gold is not the only option found in the text
    shown = _shown_strings(S)
    out = [o for o in out if o in shown] + [o for o in out if o not in shown]
    # fill: other values T accepts for p (a guess; on "No usable value" rows these are the guesses SEM-02 forbids)
    fill = []
    if p["type"] in ("date", "integer", "decimal"):
        for _ in range(8):
            try:
                txt = SM.good_value(p, rng, now)
            except (SM.Reject, AssertionError):
                break
            if A.accept(p, txt, now)[0]:
                fill.append(_canon(p, txt, now))
    seen = set()
    return [o for o in out + fill if o != gv and not (o in seen or seen.add(o))]


# ------------------------------------------------------------------------------------------------ yes/no forms
def yes_no(ctx, rng, form, want):
    """Y-CALLX, Y-ASK, Y-FIT, Y-DIRECT (framing P / N drawn 50/50; label from the card's yes rate)."""
    framing = rng.choice(["P", "N"])
    intent = bal(ctx).yn_intent(form, ctx.sampler)  # repair r9 (see PAIR_SHARE)
    if intent == "pair":
        yes = bal(ctx).pair_label(form, framing) == 1
    else:
        yes = bal(ctx).yes(("yn", form, framing), ctx.card["yes_rate"])
    if form == "Y-ASK":
        o = ("CALL" if yes else "ASK") if framing == "P" else ("ASK" if yes else "CALL")
    elif form == "Y-FIT":
        if framing == "P":
            o = rng.choice(["CALL", "ASK"]) if yes else "UNABLE"
        else:
            o = "UNABLE" if yes else rng.choice(["CALL", "ASK"])
    elif form == "Y-DIRECT":
        if framing == "P":
            o = "ANSWER" if yes else rng.choice(["CALL", "ASK", "UNABLE"])
        else:
            o = rng.choice(["CALL", "ASK", "UNABLE"]) if yes else "ANSWER"
    else:  # Y-CALLX
        callx = yes if framing == "P" else not yes
        o = "CALL" if callx else rng.choice(OUTS)
    w = dict(want)
    if intent == "pair" and o == "CALL" and form in ("Y-ASK", "Y-CALLX") and ctx.sampler == "S1":
        w["min_vals"] = 2  # gen:F12 after build 22: T-REMOVE-VALUE twin keeps a value statement (f12build.YS)
    S, res, nm, info = _forward(ctx, o, w)
    q = {}
    if form == "Y-CALLX":
        callx = yes if framing == "P" else not yes
        if callx:
            q["tool"] = res["tool"]
        else:
            pool = []
            x = rng.random()
            nmn = [n for n, _ in nm]
            fit_inc = [t["name"] for t in fitting(S, res) if not res["checks"][t["name"]]["complete"]]
            if x < 0.4 and nmn:
                pool = nmn
            elif x < 0.65 and fit_inc:
                pool = fit_inc
            elif x < 0.75 and (res.get("tie") or res.get("final")):
                pool = [t for t in (res.get("tie") or []) if t != res.get("tool")] + ([res["final"]]
                                                                                      if res.get("final") else [])
            if not pool:
                pool = [t["name"] for t in S["tools"] if t["name"] != res.get("tool") and not t.get("borrowed")] \
                    or nmn
            if not pool:
                raise Reject("Y-CALLX no T")
            q["tool"] = rng.choice(pool)
    base = _base_truth(form, res, q)
    label = base if framing == "P" else (not base if form in ("Y-CALLX", "Y-DIRECT", "Y-VALID", "Y-CORRECT")
                                         else _n_truth(form, res))
    if bool(label) != yes:
        raise Reject("yes/no label mismatch")
    return {"S": S, "res": res, "nm": nm, "form": form, "qtype": "noul", "opts": None, "gold": 1 if yes else 0,
            "q": q, "framing": framing, "info": info, "yn_intent": intent}


def _base_truth(form, res, q):
    o = res["outcome"]
    if form == "Y-CALLX":
        return o == "CALL" and res["tool"] == q["tool"]
    if form == "Y-ASK":
        return o == "CALL"
    if form == "Y-FIT":
        return o in ("CALL", "ASK")
    if form == "Y-DIRECT":
        return o == "ANSWER"
    raise AssertionError(form)


def _n_truth(form, res):
    o = res["outcome"]
    if form == "Y-ASK":
        return o == "ASK"
    if form == "Y-FIT":
        return o == "UNABLE"
    raise AssertionError(form)


BUILDERS = {"C-OUT": c_out, "C-ACT": c_act, "C-TOOL": c_tool, "C-PARAM": c_param, "C-VALUE": c_value}
