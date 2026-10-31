"""gen_policy_exceptions: applying written policies with rules, exceptions, exceptions to exceptions, defined terms,
k-of-n requirements, overrides ("notwithstanding") and conflicting clauses resolved by an explicit precedence rule.

Domains (golden_src/gen/pe_domains.py): retail returns, ticket refunds, home-insurance claims, HR leave, school
coursework extensions, community grants, travel expenses, pharmacy dispensing, building access control, content
moderation.  Every item is a policy document (title, optional definitions, numbered / lettered / legal / memo /
prose / IF-THEN rule layouts, precedence statement, default outcome, schedules and tables, irrelevant general
notes) plus case notes; the question is either yes/no or a choice of outcome code.

Labels are exact by construction:
  * a policy is a list of clauses, each "condition -> outcome"; a condition is all / any / at-least-k of literals,
    optionally negated (a requirement: "refused unless ..."), with an exception chain
    base AND NOT (U AND NOT (W AND NOT X)) ("unless U", "that exception does not apply if W", ...);
  * defined terms are conditions over facts that clauses refer to (multi-hop);
  * a total priority over clauses is chosen and rendered as ONE of: first matching rule wins, later rule prevails,
    ranking of outcomes, or explicit "Section i prevails over Sections j, k" / "Notwithstanding ..." statements;
    if no two clauses can conflict nothing needs to be said;
  * the primary evaluator uses the priority list; an independent second evaluator compiles each condition to a
    Python expression and resolves conflicts ONLY from what the text states (listing order, stated ranking or
    stated prevail-pairs).  Every emitted row is re-checked with the second evaluator; any disagreement aborts.
  * unknown facts ("the file does not say ...") are resolved by enumerating every value the fact could take; the
    outcome is undetermined exactly when two completions give different outcomes.

Questions (qid): approved / denied (binary policies), est_approved / est_denied ("do the stated facts establish",
unknown -> no), outcome_is / est_outcome (multi-outcome policies), claim (a colleague's recorded conclusion; reported
speech), hypo / hypo_outcome (counterfactual change of one fact), choice_<domain> (pick the outcome code; some rows
add "cannot be determined from the stated facts").  Every base row has a fact-flip twin (meta.twin_of) that changes
ONE fact (or reveals / hides one fact) so that the gold answer changes.  Deterministic (seed 20261129), CPU only.
"""
import collections
import copy
import hashlib
import itertools
import json
import os
import random
import re
import sys
import time
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
sys.path.insert(0, str(HERE.parent / "moral_social_norms"))
from common import EDGE_TAGS, check_rows, edge_tags, norm, summary, write_defs, yesno_share  # noqa: E402
from nd_common import hk, person  # noqa: E402
from pe_atoms import (InPred, NumFact, NumPred, PairPred, RatioPred, TablePred, TimePred, fdate, lit, lkey, neg,  # noqa: E402
                      pick, seed_lits)
from pe_domains import DOMAINS  # noqa: E402

KEY = "gen_policy_exceptions"
SEED = 20261129
N_PAIRS = int(os.environ.get("PE_PAIRS", "12500"))
FAMILY = "nli_logic_reasoning"
UNDET = "cannot be determined from the stated facts"
LEAN = HERE.parent.parent
RAW = LEAN / "data" / "v14_parts" / "raw"
MANIFEST = LEAN / "golden_src" / "MANIFEST.jsonl"
DOM = {D.name: D for D in DOMAINS}


def cap(s):
    return s[:1].upper() + s[1:]


def tidy(s):
    """'Co..' -> 'Co.' (organisation names that end in a full stop)."""
    return re.sub(r"\.\.(?=[\s\"]|$)", ".", s)


def art(w):
    return ("an " if w[:1].lower() in "aeiou" else "a ") + w


# =============================================================================================== evaluation (primary)
def lv(l, T):
    return T[l[0]] if l[1] else not T[l[0]]


def base_holds(c, T):
    vals = [lv(l, T) for l in c["lits"]]
    m = c["mode"]
    b = all(vals) if m == "all" else any(vals) if m == "any" else sum(vals) >= m
    return (not b) if c.get("neg") else b


def exc_active(c, T):
    e = False
    for x in reversed(c.get("exc", [])):
        e = lv(x, T) and not e
    return e


def fire(c, T):
    return base_holds(c, T) and not exc_active(c, T)


def preds_on_fact(D, pol, fid):
    return [pid for pid in pol["pp"] if D.preds[pid].fact == fid]


def fact_values(D, pol, fid):
    return D.facts[fid].values([pol["pp"][p] for p in preds_on_fact(D, pol, fid)])


def truths(D, pol, f):
    T = {}
    pp = pol["pp"]
    for pid in sorted(pp, key=lambda p: D.facts[D.preds[p].fact].req is not None):
        P = D.preds[pid]
        F = D.facts[P.fact]
        if F.req is not None:
            rp, rt = F.req
            assert rp in T, (pid, rp)
            if T[rp] != rt:
                T[pid] = False
                continue
        v = f[P.fact]
        assert v is not None, (pid, P.fact)
        T[pid] = P.truth(v, pp[pid])
    for t in pol["terms"]:
        T[t["id"]] = fire(t["cond"], T)
    return T


def outcome(pol, T):
    fired = [i for i, c in enumerate(pol["clauses"]) if fire(c, T)]
    if not fired:
        return pol["default"], fired
    w = min(fired, key=pol["prio"].index)
    return pol["clauses"][w]["out"], fired


def valid(D, pol, f):
    for a, b in D.mutex:
        if f.get(a) is True and f.get(b) is True:
            return False
    return True


def completions(D, pol, f):
    unk = [fid for fid in pol["facts"] if f.get(fid) is None]
    if not unk:
        yield f
        return
    for combo in itertools.product(*[fact_values(D, pol, fid) for fid in unk]):
        g = dict(f)
        g.update(zip(unk, combo))
        if valid(D, pol, g):
            yield g


def outcomes(D, pol, f):
    return {outcome(pol, truths(D, pol, g))[0] for g in completions(D, pol, f)}


# =============================================================================================== evaluation (second)
def _cl(l):
    return f"A[{l[0]!r}]" if l[1] else f"(not A[{l[0]!r}])"


def compile_cond(c):
    xs = [_cl(l) for l in c["lits"]]
    m = c["mode"]
    if m == "all":
        b = "(" + " and ".join(xs) + ")"
    elif m == "any":
        b = "(" + " or ".join(xs) + ")"
    else:
        b = "((" + " + ".join(f"int({x})" for x in xs) + f") >= {int(m)})"
    if c.get("neg"):
        b = f"(not {b})"
    e = "False"
    for x in reversed(c.get("exc", [])):
        e = f"({_cl(x)} and not {e})"
    return compile(f"({b} and not {e})", "<cond>", "eval")


def outcome2(D, pol, f):
    """Independent re-computation: per-fact truth table loop, compiled conditions, and conflict resolution taken
    only from the precedence data that the renderer wrote into the text."""
    A = {}
    pending = list(pol["pp"])
    while pending:
        pid = pending.pop(0)
        P = D.preds[pid]
        F = D.facts[P.fact]
        if F.req is not None and F.req[0] not in A:
            pending.append(pid)
            continue
        A[pid] = (A[F.req[0]] == F.req[1] and P.truth(f[P.fact], pol["pp"][pid])) if F.req is not None else P.truth(f[P.fact], pol["pp"][pid])
    for t in pol["terms"]:
        A[t["id"]] = eval(compile_cond(t["cond"]), {}, {"A": A})
    cl = pol["clauses"]
    fired = [i for i, c in enumerate(cl) if eval(compile_cond(c), {}, {"A": A})]
    R = pol["R"]
    if not fired:
        return R["default"]
    mode = R["mode"]
    if mode == "first":
        return cl[min(fired, key=R["listing"].index)]["out"]
    if mode == "later":
        return cl[max(fired, key=R["listing"].index)]["out"]
    if mode == "rank":
        return min({cl[i]["out"] for i in fired}, key=R["rank"].index)
    if mode == "explicit":
        beats = set(map(tuple, R["beats"]))
        cands = [i for i in fired if not any((j, i) in beats for j in fired if cl[j]["out"] != cl[i]["out"])]
        outs = {cl[i]["out"] for i in cands}
        assert len(outs) == 1, ("underspecified precedence", outs)
        return outs.pop()
    outs = {cl[i]["out"] for i in fired}
    assert mode == "none" and len(outs) == 1, (mode, outs)
    return outs.pop()


def outcomes2(D, pol, f):
    return {outcome2(D, pol, g) for g in completions(D, pol, f)}


# =============================================================================================== policy builder
LAYOUTS = [("numbered", 0.36), ("legal", 0.17), ("rules", 0.14), ("prose", 0.13), ("memo", 0.2)]


def wchoice(rng, items):
    r = rng.random() * sum(w for _, w in items)
    for x, w in items:
        r -= w
        if r <= 0:
            return x
    return items[-1][0]


class Builder:
    def __init__(self, D, rng, multi, arch):
        self.D, self.rng, self.multi = D, rng, multi
        self.used, self.facts = set(), set()
        lay = wchoice(rng, LAYOUTS) if arch != "table" else rng.choice(["rules", "rules", "numbered", "memo"])
        self.pol = {"dom": D.name, "multi": multi, "arch": arch, "pp": {}, "clauses": [], "terms": [], "layout": lay,
                    "sty": rng.randrange(10 ** 9)}
        self.maxchain = 2 if lay == "prose" else 3
        self.probs = (0.62, 0.45, 0.3)[:self.maxchain]

    # ---------------------------------------------------------------- availability
    def avail(self, l, ctx=()):
        pid = l[0]
        if pid in self.used:
            return False
        if pid.startswith("T_"):
            return True
        P = self.D.preds[pid]
        for a, b in self.D.nocombine:
            if (P.fact == a and b in self.facts) or (P.fact == b and a in self.facts):
                return False
        if P.guard and lkey(P.guard) not in ctx:
            return False
        return True

    def use(self, l):
        pid = l[0]
        self.used.add(pid)
        if pid.startswith("T_"):
            return
        P = self.D.preds[pid]
        self.facts.add(P.fact)
        if pid not in self.pol["pp"]:
            p = P.params(self.rng)
            # two threshold predicates on the same fact must not share a threshold
            for q in preds_on_fact(self.D, self.pol, P.fact):
                if "t" in p and self.pol["pp"][q].get("t") == p["t"]:
                    alts = [t for t in getattr(P, "ts", []) if t != p["t"]]
                    if alts:
                        p["t"] = self.rng.choice(alts)
            self.pol["pp"][pid] = p

    def seed_ok(self, s):
        ls = seed_lits(s)
        ctx = {lkey(l) for l in ls}
        return all(self.avail(l, ctx) for l in ls)

    def chain(self, keys, ctx, p_scale=1.0):
        out = []
        cur = list(keys)
        cctx = set(ctx) | set(keys)
        for p in self.probs:
            if self.rng.random() >= p * p_scale:
                break
            cands = []
            for k in cur:
                cands += self.D.exc.get(k, [])
            cands = [c for c in dict.fromkeys(cands) if self.avail(lit(c), cctx)]
            if not cands:
                break
            c = self.rng.choice(cands)
            self.use(lit(c))
            out.append(lit(c))
            cur, cctx = [c], {c}
        return out

    def out_for(self, codes, binary):
        return binary if not self.multi else self.rng.choice(codes)

    def add(self, lits, mode, out, kind, exc=(), negb=False, key=None):
        self.pol["clauses"].append({"lits": list(lits), "mode": mode, "neg": negb, "exc": list(exc), "out": out,
                                    "kind": kind, "key": key})

    # ---------------------------------------------------------------- clause makers
    def add_prereq(self, force_neg_any=False):
        D, rng = self.D, self.rng
        av = [lit(s) for s in D.prereq if self.avail(lit(s))]
        if not av:
            return False
        k = min(len(av), rng.choice([1, 1, 2, 2, 3]))
        ls = rng.sample(av, k)
        for l in ls:
            self.use(l)
        out = "deny" if not self.multi else D.deny_code
        fkeys = [lkey(neg(l)) for l in ls]
        exc = self.chain(fkeys, fkeys)
        if k == 1 and rng.random() < 0.5:
            self.add([neg(ls[0])], "all", out, "ground", exc, key=fkeys[0])
        else:
            self.add(ls, "all", out, "prereq", exc, negb=True, key="&".join(fkeys))
        return True

    def add_seed(self, pool, kind, binary, p_scale=1.0):
        cands = [(s, codes) for s, codes in pool if self.seed_ok(s)]
        if not cands:
            return False
        s, codes = self.rng.choice(cands)
        ls = seed_lits(s)
        for l in ls:
            self.use(l)
        keys = [s.replace(" ", "")] if len(ls) > 1 else [lkey(ls[0])]
        keys = [s] if s in self.D.exc else keys
        exc = self.chain(keys, {lkey(l) for l in ls}, p_scale)
        self.add(ls, "all", self.out_for(codes, binary), kind, exc, key=s)
        return True

    def add_ground(self, p_scale=1.0):
        return self.add_seed(self.D.grounds, "ground", "deny", p_scale)

    def add_mod(self):
        return self.add_seed(self.D.mods, "mod", None)

    def add_override(self, prefer_yes=True):
        pools = []
        if self.D.ovr_yes:
            pools.append((self.D.ovr_yes, "approve"))
        if self.D.ovr_no and (self.multi or not prefer_yes):
            pools.append((self.D.ovr_no, "deny"))
        self.rng.shuffle(pools)
        for pool, b in pools:
            if self.add_seed(pool, "override", b):
                return True
        return False

    def add_approve_clause(self, kmode=None):
        D, rng = self.D, self.rng
        av = [lit(s) for s in D.prereq if self.avail(lit(s))]
        if len(av) < 2:
            return False
        r = rng.random() if kmode is None else kmode
        if r < 0.55 or len(av) < 3:
            ls = rng.sample(av, min(len(av), rng.choice([2, 2, 3])))
            mode = "all" if (r < 0.55 or rng.random() < 0.5 or len(ls) < 2) else "any"
            if r >= 0.85 and len(ls) == 2:
                mode = "any"
        else:
            n = min(len(av), rng.choice([3, 3, 4]))
            ls = rng.sample(av, n)
            mode = rng.randint(2, n - 1)
        for l in ls:
            self.use(l)
        out = "approve" if not self.multi else D.best
        self.add(ls, mode, out, "approve", [], key="approve")
        return True

    def add_term(self, T):
        """Define a term from its pool; returns the term literal or None."""
        D, rng = self.D, self.rng
        pool = [lit(x) for x in T["pool"] if self.avail(lit(x))]
        if len(pool) < min(2, len(T["pool"])) or T["id"] in self.used:
            return None
        mode = rng.choice(T["modes"])
        if mode == "k2":
            if len(pool) < 3:
                return None
            ls = rng.sample(pool, 3)
            mode = 2
        elif len(pool) == 1:
            ls = pool
            mode = "all"
        else:
            ls = rng.sample(pool, rng.randint(2, min(3, len(pool))))
        for l in ls:
            self.use(l)
        self.used.add(T["id"])
        self.pol["terms"].append({"id": T["id"], "name": T["name"], "cond": {"lits": ls, "mode": mode, "neg": False, "exc": []}})
        return (T["id"], True)


def term_spec(D, tid):
    return next(t for t in D.terms if t["id"] == tid)


def build_policy(D, rng, multi, arch):
    B = Builder(D, rng, multi, arch)
    pol = B.pol
    cl = pol["clauses"]
    if arch == "gate":
        if D.prereq and rng.random() < 0.75:
            B.add_prereq()
        for _ in range(rng.choice([1, 2, 2, 3])):
            B.add_ground()
        if multi:
            if D.mods and rng.random() < 0.55:
                B.add_mod()
            if rng.random() < 0.35:
                B.add_override()
        pol["default"] = "approve" if not multi else D.best
    elif arch == "override":
        if D.prereq and rng.random() < 0.6:
            B.add_prereq()
        for _ in range(rng.choice([1, 2, 2])):
            B.add_ground()
        if not B.add_override(prefer_yes=True):
            return None
        if multi and D.mods and rng.random() < 0.4:
            B.add_mod()
        pol["default"] = "approve" if not multi else D.best
    elif arch == "approve_if":
        if not B.add_approve_clause():
            return None
        for _ in range(rng.choice([1, 1, 2])):
            B.add_ground()
        if multi and D.mods and rng.random() < 0.5:
            B.add_mod()
        pol["default"] = "deny" if not multi else D.deny_code
    elif arch == "kofn":
        if not B.add_approve_clause(kmode=0.99):
            return None
        for _ in range(rng.choice([0, 1, 1, 2])):
            B.add_ground()
        pol["default"] = "deny" if not multi else D.deny_code
    elif arch == "conflict":
        ok = False
        if D.ovr_yes and rng.random() < 0.7:
            ok = B.add_seed(D.ovr_yes, "override", "approve")
        if not ok:
            ok = B.add_approve_clause()
        if not ok:
            return None
        for _ in range(rng.choice([1, 2])):
            B.add_ground()
        if multi and D.mods and rng.random() < 0.5:
            B.add_mod()
        pol["default"] = rng.choice(["approve", "deny"]) if not multi else rng.choice([D.best, D.deny_code])
    elif arch == "table":
        n = rng.randint(3, 5)
        pools = [("g", 5), ("pre", 2 if D.prereq else 0), ("oy", 2 if D.ovr_yes else 0), ("on", 1 if D.ovr_no else 0),
                 ("m", 2 if (multi and D.mods) else 0)]
        pools = [(x, w) for x, w in pools if w]
        B.probs = (0.35, 0.2)
        for _ in range(n * 2):
            if len(cl) >= n:
                break
            kind = wchoice(rng, pools)
            if kind == "g":
                B.add_ground()
            elif kind == "pre":
                av = [lit(s) for s in D.prereq if B.avail(lit(s))]
                if av:
                    l = rng.choice(av)
                    B.use(l)
                    exc = B.chain([lkey(neg(l))], [lkey(neg(l))])
                    B.add([neg(l)], "all", "deny" if not multi else D.deny_code, "ground", exc, key=lkey(neg(l)))
            elif kind == "oy":
                B.add_seed(D.ovr_yes, "override", "approve")
            elif kind == "on":
                B.add_seed(D.ovr_no, "override", "deny")
            else:
                B.add_mod()
        pol["default"] = rng.choice(["approve", "deny"]) if not multi else rng.choice([D.best, D.best, D.deny_code])
    elif arch == "defs":
        terms = list(D.terms)
        rng.shuffle(terms)
        nt = 0
        for T in terms:
            if nt >= 2:
                break
            if T["role"] == "prereq":
                tl = B.add_term(T)
                if tl:
                    fkeys = [lkey(neg(l)) for l in B.pol["terms"][-1]["cond"]["lits"]]
                    exc = B.chain(fkeys, fkeys, 0.6)
                    B.add([tl], "all", "deny" if not multi else D.deny_code, "prereq", exc, negb=True, key="term")
                    nt += 1
            elif T["role"] == "exc":
                seeds = [(s, codes) for s, codes in D.grounds if s in T["for_"] and B.seed_ok(s)]
                if not seeds:
                    continue
                tl = B.add_term(T)
                if not tl:
                    continue
                s, codes = rng.choice(seeds)
                ls = seed_lits(s)
                for l in ls:
                    B.use(l)
                B.add(ls, "all", B.out_for(codes, "deny"), "ground", [tl], key=s)
                nt += 1
            elif T["role"] == "ground":
                tl = B.add_term(T)
                if tl:
                    first = B.pol["terms"][-1]["cond"]["lits"][0]
                    codes = next((c for s, c in D.grounds if s == lkey(first)), [D.deny_code])
                    B.add([tl], "all", B.out_for(codes, "deny"), "ground", [], key="term")
                    nt += 1
        if nt == 0:
            return None
        for _ in range(rng.choice([0, 1, 1, 2])):
            B.add_ground()
        if multi and D.mods and rng.random() < 0.4:
            B.add_mod()
        pol["default"] = "approve" if not multi else D.best
    else:
        raise ValueError(arch)

    # ------------------------------------------------------------------ validity
    if not cl:
        return None
    outs_all = {c["out"] for c in cl} | {pol["default"]}
    if multi and len(outs_all) < 3:
        return None
    if len(outs_all) < 2:
        return None
    interesting = (any(c["exc"] for c in cl) or pol["terms"] or len({c["out"] for c in cl}) >= 2
                   or any(isinstance(c["mode"], int) or c["mode"] == "any" for c in cl))
    if not interesting or (len(cl) < 2 and not any(c["exc"] for c in cl)):
        return None
    # term-level exceptions are single literals (no chains) - nothing else to check
    pol["facts"] = sorted(B.facts, key=lambda fid: D.facts[fid].order)
    assign_priority(D, pol, rng)
    choose_mode(D, pol, rng)
    # distractor facts and evidence rule
    cands = [fid for fid, F in D.facts.items() if F.distract and fid not in B.facts
             and not any((fid == a and b in B.facts) or (fid == b and a in B.facts) for a, b in D.nocombine)]
    pol["distract"] = sorted(rng.sample(cands, min(len(cands), rng.choice([0, 1, 1, 2]))), key=lambda fid: D.facts[fid].order)
    pol["ev"] = None
    evc = [fid for fid in pol["facts"] if D.facts[fid].ev and D.facts[fid].req is None]
    if evc and D.sources and rng.random() < 0.14:
        pol["ev"] = {"fact": rng.choice(evc), "w": rng.randrange(2)}
    pol["cur"] = rng.choice(["$"] * 6 + ["£", "€"])
    return pol


def sev_map(D, pol):
    if not pol["multi"]:
        return {"deny": 0, "approve": 1}
    n = len(D.codes)
    return {c: n - 1 - i for i, c in enumerate(D.codes)}  # worst outcome first


def assign_priority(D, pol, rng):
    cl = pol["clauses"]
    sev = sev_map(D, pol)

    def nat(i):
        c = cl[i]
        if c["kind"] == "override":
            return 0
        if c["kind"] == "approve":
            return 9
        return 1 + sev[c["out"]]

    prio = sorted(range(len(cl)), key=lambda i: (nat(i), rng.random()))
    arch = pol["arch"]
    if arch == "conflict":
        rng.shuffle(prio)
        appr = [i for i in prio if cl[i]["kind"] == "approve"]
        if appr and rng.random() < 0.5:  # an approve-if clause at the top makes grounds irrelevant; keep it low sometimes
            prio.remove(appr[0])
            prio.append(appr[0])
    elif arch == "table":
        rng.shuffle(prio)
    elif rng.random() < 0.3 and len(prio) >= 2:
        idx = [k for k in range(len(prio) - 1) if cl[prio[k]]["out"] != cl[prio[k + 1]]["out"]
               and cl[prio[k + 1]]["kind"] != "approve"]
        if idx:
            k = rng.choice(idx)
            prio[k], prio[k + 1] = prio[k + 1], prio[k]
    pol["prio"] = prio


def rank_order(pol):
    """Outcome ranking consistent with the clause priority, or None."""
    cl, prio = pol["clauses"], pol["prio"]
    order = []
    for i in prio:
        if cl[i]["out"] not in order:
            order.append(cl[i]["out"])
    for a in range(len(prio)):
        for b in range(a + 1, len(prio)):
            oa, ob = cl[prio[a]]["out"], cl[prio[b]]["out"]
            if oa != ob and order.index(oa) > order.index(ob):
                return None
    return order


def choose_mode(D, pol, rng):
    cl = pol["clauses"]
    conflicts = len({c["out"] for c in cl}) >= 2
    lay = pol["layout"]
    if not conflicts:
        mode = "none"
    elif pol["arch"] == "table":
        mode = "first" if rng.random() < 0.7 else "later"
    else:
        opts = [("first", 0.24), ("later", 0.14)]
        if lay != "prose":
            opts.append(("explicit", 0.38))
        if rank_order(pol):
            opts.append(("rank", 0.28))
        mode = wchoice(rng, opts)
    pol["mode"] = mode
    if mode == "first":
        listing = list(pol["prio"])
    elif mode == "later":
        listing = list(reversed(pol["prio"]))
    else:
        korder = {"prereq": 0, "approve": 1, "ground": 2, "mod": 3, "override": 4}
        listing = sorted(range(len(cl)), key=lambda i: (korder[cl[i]["kind"]], rng.random()))
        if rng.random() < 0.2:
            rng.shuffle(listing)
    pol["listing"] = listing
    pol["rank"] = rank_order(pol) if mode == "rank" else None


# =============================================================================================== rendering: policy
LABELS = [
    dict(fmt="Section {i}.", one="Section {i}", many="Sections {l}", word="section", words="sections"),
    dict(fmt="Rule {i}:", one="Rule {i}", many="Rules {l}", word="rule", words="rules"),
    dict(fmt="Clause {i} -", one="Clause {i}", many="Clauses {l}", word="clause", words="clauses"),
    dict(fmt="{i}.", one="item {i}", many="items {l}", word="item", words="items"),
    dict(fmt="({i})", one="paragraph ({i})", many="paragraphs {l}", word="paragraph", words="paragraphs", paren=True),
    dict(fmt="Article {i}.", one="Article {i}", many="Articles {l}", word="article", words="articles"),
]
LEGAL = dict(fmt="§ {s}.{i}", one="§ {s}.{i}", many="§§ {l}", word="section", words="sections", legal=True)
MEMO = dict(fmt="{i})", one="point {i}", many="points {l}", word="point", words="points")
PROSE = dict(word="rule", words="rules")
RULESL = dict(fmt="Rule {i}:", one="Rule {i}", many="Rules {l}", word="rule", words="rules")


def joinand(xs, conj="and"):
    xs = list(xs)
    if len(xs) == 1:
        return xs[0]
    return ", ".join(xs[:-1]) + f" {conj} " + xs[-1]


class PolicyText:
    """Renders a policy.  All surface choices are keyed hashes of pol['sty'] (deterministic, twin-stable)."""

    def __init__(self, D, pol):
        self.D, self.pol = D, pol
        self.s = pol["sty"]
        lay = pol["layout"]
        if lay == "numbered":
            self.L = LABELS[hk(self.s, "lab") % len(LABELS)]
        elif lay == "legal":
            self.L = LEGAL
        elif lay == "memo":
            self.L = MEMO
        elif lay == "rules":
            self.L = RULESL
        else:
            self.L = PROSE
        self.sec = 2 + hk(self.s, "secno") % 7
        self.ctx = {"org": pol["org"], "cur": pol["cur"], "_clock": hk(self.s, "clock") % 2}
        self.flags = collections.defaultdict(set)   # clause index -> {"neg", "dneg", "quant", "list"}
        self.num = {ci: k + 1 for k, ci in enumerate(pol["listing"])}

    def k(self, seq, *key):
        return pick(seq, self.s, *key)

    # ---------------------------------------------------------------- references
    def numtxt(self, ci):
        i = self.num[ci]
        if self.L.get("legal"):
            return f"{self.sec}.{i}"
        if self.L.get("paren"):
            return f"({i})"
        return str(i)

    def ref(self, ci):
        return self.L["one"].format(i=self.num[ci], s=self.sec) if "one" in self.L else None

    def refs(self, cis):
        cis = sorted(cis, key=lambda c: self.num[c])
        if len(cis) == 1:
            return self.ref(cis[0])
        return self.L["many"].format(l=joinand([self.numtxt(c) for c in cis]))

    def label(self, ci):
        return self.L["fmt"].format(i=self.num[ci], s=self.sec)

    # ---------------------------------------------------------------- phrases
    def lp(self, l, ci=None):
        pid, pos = l
        if pid.startswith("T_"):
            T = term_spec(self.D, pid)
            return self.k(T["pos"] if pos else T["neg"], "term", pid, pos).format(name=T["name"])
        P = self.D.preds[pid]
        if not pos and ci is not None:
            self.flags[ci].add("neg")
        return P.phrase(self.pol["pp"][pid], pos, (self.s,), self.ctx)

    def oc(self, out, *key):
        D = self.D
        if not self.pol["multi"]:
            seq = D.appr["clause"] if out == "approve" else D.deny["clause"]
        else:
            seq = D.code_clause[out]
        return self.k(seq, "oc", out, *key)

    def itemize(self, xs, conj, ci, roman=False):
        marks = ["i", "ii", "iii", "iv"] if (roman or hk(self.s, "mk", ci) % 2) else ["a", "b", "c", "d"]
        parts = [f"({marks[j]}) {x}" for j, x in enumerate(xs)]
        if conj:
            return "; ".join(parts[:-1]) + f"; {conj} " + parts[-1]
        return "; ".join(parts)

    def cond(self, lits, mode, ci, roman=False, allow_list=True):
        """Returns (text, form) with form in single / inline / list."""
        n = len(lits)
        if n == 1:
            return self.lp(lits[0], ci), "single"
        if mode == "all":
            if all(not l[1] for l in lits) and hk(self.s, "none", ci) % 3 == 0 and allow_list:
                self.flags[ci] |= {"quant", "dneg"}
                pos = [self.lp(neg(l)) for l in lits]
                return "none of the following is true: " + self.itemize(pos, "", ci, roman), "list"
            ph = [self.lp(l, ci) for l in lits]
            if n == 2 and (hk(self.s, "l2", ci) % 3 or not allow_list):
                return self.k([f"{ph[0]} and {ph[1]}", f"both {ph[0]} and {ph[1]}"], "and2", ci), "inline"
            if not allow_list:
                return joinand(ph), "inline"
            self.flags[ci].add("quant")
            return "all of the following are true: " + self.itemize(ph, "and", ci, roman), "list"
        ph = [self.lp(l, ci) for l in lits]
        self.flags[ci].add("quant")
        if mode == "any":
            if n == 2 and (hk(self.s, "o2", ci) % 3 or not allow_list):
                return self.k([f"{ph[0]} or {ph[1]}", f"either {ph[0]} or {ph[1]}"], "or2", ci), "inline"
            if not allow_list:
                return joinand(ph, "or"), "inline"
            return "at least one of the following is true: " + self.itemize(ph, "or", ci, roman), "list"
        kk = int(mode)
        return f"at least {['zero', 'one', 'two', 'three', 'four'][kk]} of the following are true: " + self.itemize(ph, "", ci, roman), "list"

    # ---------------------------------------------------------------- clause
    def clause(self, ci, pre_note=None):
        """Returns a list of lines (the first is the main sentence; lettered sub-paragraphs follow)."""
        pol, D = self.pol, self.D
        c = pol["clauses"][ci]
        exc = c["exc"]
        lettered = len(exc) >= 3 or (exc and pol["layout"] == "legal" and hk(self.s, "let", ci) % 2 == 0) or \
            (exc and pol["layout"] in ("numbered", "memo", "rules") and hk(self.s, "let", ci) % 5 == 0)
        mode = pol["mode"]
        O = self.oc(c["out"], ci)
        is_rules = pol["layout"] == "rules"
        done_first = False
        # requirement clauses
        if c["neg"]:
            if mode in ("first", "later") or is_rules:
                lits = [neg(l) for l in c["lits"]]
                C, form = self.cond(lits, "any" if len(lits) > 1 else "all", ci, roman=lettered)
                main = self.main_sentence(ci, C, form, O, inline_exc=None, is_rules=is_rules)
                exc_word = "rule"
            else:
                C, form = self.cond(c["lits"], "all", ci, roman=lettered)
                opts = [f"{cap(O)} unless {C}."]
                if form == "list" and C.startswith("all of the following"):
                    opts = [f"{cap(O)} unless {C}.", f"Every {D.req} must meet all of these requirements: " +
                            C.split(": ", 1)[1] + f". If any of them is not met, {O}."]
                elif form != "list" and not pol["multi"] and mode == "none":
                    opts += [f"{cap(D.subj_pl)} are {D.appr['pas']} only if {C}; otherwise, {self.oc('deny', ci, 'o')}.",
                             f"No {D.req} is {D.appr['pas']} unless {C}."]
                main = self.k(opts, "pre", ci)
                if main.startswith("No ") or " unless none of" in main:
                    self.flags[ci].add("dneg")
                exc_word = "requirement"
        else:
            C, form = self.cond(c["lits"], c["mode"], ci, roman=lettered)
            inline = None
            if len(exc) == 1 and form == "single" and not lettered and hk(self.s, "inl", ci) % 2 == 0:
                inline = self.lp(exc[0], ci)
            main = self.main_sentence(ci, C, form, O, inline_exc=inline, is_rules=is_rules)
            exc_word = "rule"
            if inline is not None:
                self.flags[ci].add("inline")
                done_first = True
        if pre_note:
            main = pre_note + main[0].lower() + main[1:] if not main.startswith(("IF", "No ")) else pre_note + main
        if any(not x[1] for x in c["exc"]):
            self.flags[ci].add("dneg")
        lines = [main]
        if not c["exc"]:
            return lines
        if lettered:
            lines = ["(a) " + main]
            letters = "abcd"
            for j, x in enumerate(c["exc"]):
                lines.append(f"({letters[j + 1]}) Paragraph ({letters[j]}) does not apply if {self.lp(x, ci)}.")
            return lines
        seq = list(c["exc"])
        start = 0
        if not c["neg"] and done_first:
            start = 1
        sent = []
        for j in range(start, len(seq)):
            x = seq[j]
            if j == 0:
                if exc_word == "requirement":
                    t = self.k(["This requirement does not apply if {u}.", "The requirement is waived where {u}.",
                                "Exception: the requirement does not apply when {u}."], "e1r", ci)
                else:
                    t = self.k(["This does not apply if {u}.", "However, this rule does not apply where {u}.",
                                "Exception: this rule does not apply when {u}.", "The rule in the previous sentence does not apply if {u}."],
                               "e1", ci)
                sent.append(t.format(u=self.lp(x, ci)))
            elif j == 1:
                t = self.k(["However, that exception does not apply if {w}.", "That exception applies only if {wn}.",
                            "But the exception is lost where {w}.", "The exception itself does not apply when {w}."], "e2", ci)
                sent.append(t.format(w=self.lp(x, ci), wn=self.lp(neg(x), ci)))
            else:
                sent.append(f"The limit on the exception in the previous sentence does not apply if {self.lp(x, ci)}.")
        lines[0] = lines[0] + " " + " ".join(sent) if sent else lines[0]
        return lines

    def main_sentence(self, ci, C, form, O, inline_exc=None, is_rules=False):
        if is_rules:
            code = O
            if self.pol["multi"]:
                code = self.pol["clauses"][ci]["out"].upper()
            s = f"IF {C} THEN {code}" if self.pol["multi"] else f"If {C}, {O}"
            if inline_exc:
                s += f", unless {inline_exc}"
            return s + "."
        if form == "list":
            return self.k([f"{cap(O)} if {C}.", f"{cap(O)} where {C}."], "ml", ci)
        if inline_exc is not None:
            return self.k([f"{cap(O)} if {C}, unless {inline_exc}.", f"If {C}, {O} unless {inline_exc}.",
                           f"{cap(O)} if {C}, except where {inline_exc}.", f"{cap(O)} if {C}, except when {inline_exc}."], "mi", ci)
        return self.k([f"If {C}, {O}.", f"{cap(O)} if {C}.", f"Where {C}, {O}.", f"{cap(O)} whenever {C}.", f"When {C}, {O}."], "ms", ci)

    # ---------------------------------------------------------------- precedence and default
    def precedence(self):
        pol, D = self.pol, self.D
        cl, mode = pol["clauses"], pol["mode"]
        L = self.L
        R = {"mode": mode, "listing": list(pol["listing"]), "rank": None, "beats": [], "default": pol["default"]}
        lines, inline_notes = [], {}
        if mode == "first":
            lines.append(self.k([f"Apply the {L['words']} in the order listed: the first {L['word']} that fits the case decides the outcome, and later {L['words']} are ignored.",
                                 f"Go through the {L['words']} from the top; only the first {L['word']} whose conditions are met counts.",
                                 f"The first {L['word']} that matches the case wins; do not read further."], "pf"))
        elif mode == "later":
            lines.append(self.k([f"If two or more {L['words']} apply and lead to different outcomes, the one that appears later in this policy prevails.",
                                 f"Where {L['words']} conflict, the later {L['word']} controls.",
                                 f"When several {L['words']} apply, follow the last of them in the list."], "pl"))
        elif mode == "rank":
            rk = pol["rank"]
            R["rank"] = list(rk)
            if not pol["multi"]:
                a = D.appr["noun"] if rk[0] == "approve" else D.deny["noun"]
                b = D.deny["noun"] if rk[0] == "approve" else D.appr["noun"]
                lines.append(self.k([f"Whenever {L['words']} point to different outcomes, {a} takes precedence over {b}.",
                                     f"If one {L['word']} leads to {a} and another to {b}, {a} wins."], "pr2"))
            else:
                q = [f'"{x}"' for x in rk]
                lines.append(self.k([f"If more than one {L['word']} applies and they lead to different outcomes, the outcome that comes first in this list prevails: {'; '.join(q)}.",
                                     f"Order of precedence between outcomes, highest first: {'; '.join(q)}.",
                                     f"When {L['words']} conflict, apply whichever outcome ranks higher in this order: {', then '.join(q)}."], "prm"))
        elif mode == "explicit":
            prio = pol["prio"]
            stm = []
            for a, i in enumerate(prio):
                losers = [j for j in prio[a + 1:] if cl[j]["out"] != cl[i]["out"]]
                if not losers:
                    continue
                for j in losers:
                    R["beats"].append((i, j))
                use_inline = hk(self.s, "nw", i) % 100 < (50 if cl[i]["kind"] == "override" else 30)
                if use_inline:
                    inline_notes[i] = f"Notwithstanding {self.refs(losers)}, "
                else:
                    stm.append(self.k([f"{cap(self.ref(i))} prevails over {self.refs(losers)}.",
                                       f"{cap(self.ref(i))} takes precedence over {self.refs(losers)}.",
                                       f"In case of conflict, {self.ref(i)} overrides {self.refs(losers)}."], "px", i))
            lines += stm
        return lines, inline_notes, R

    def default_line(self):
        L = self.L
        O = self.oc(self.pol["default"], "def")
        if self.pol["mode"] == "first":
            return self.k([f"If no {L['word']} fits, {O}.", f"If none of the {L['words']} above matches, {O}."], "df")
        return self.k([f"If none of the {L['words']} above applies, {O}.", f"In all other cases, {O}.", f"Otherwise, {O}.",
                       f"{cap(O)} in every other case."], "dd")

    # ---------------------------------------------------------------- whole document
    def render(self):
        pol, D = self.pol, self.D
        s = self.s
        title = self.k(D.titles, "title").format(org=pol["org"], num=100 + hk(s, "num") % 900)
        prec_lines, inline_notes, R = self.precedence()
        cls = []
        for ci in pol["listing"]:
            cls.append((ci, self.clause(ci, inline_notes.get(ci))))
        defline = self.default_line()
        out = [title]
        lay = pol["layout"]
        if lay == "memo":
            out = ["To: All staff", f"From: {self.k(['Operations Manager', 'Head of Policy', 'Compliance Lead', 'Service Director'], 'from')}",
                   f"Subject: {title}", "", self.k(["Please apply the following rules to every case.",
                                                   "From today, decide every case using these rules."], "memo")]
        elif hk(s, "intro") % 2 == 0:
            out.append(self.k([f"This policy explains how {D.req_pl} are decided.", "Staff must apply the rules below exactly as written.",
                               f"The rules below decide every {D.req}.", "Read all of the rules before deciding a case."], "intro"))
        # definitions
        if pol["terms"]:
            dl = []
            for t in pol["terms"]:
                T = term_spec(D, t["id"])
                C, form = self.cond(t["cond"]["lits"], t["cond"]["mode"], "T" + t["id"], roman=True)
                dl.append(self.k(T["defs"], "tdef", t["id"]).format(name=T["name"], cond=C))
            if lay == "prose":
                out.append(" ".join(dl))
            else:
                out.append(self.k(["Definitions", "Terms used in this policy", "Definitions:"], "defh"))
                out += [f"- {x}" for x in dl]
        prec_before = prec_lines and hk(s, "pbefore") % 3 == 0
        if prec_before:
            out.append(" ".join(prec_lines))
        if lay == "prose":
            conn = ["", "Also, ", "In addition, ", "Separately, ", "Furthermore, "]
            para = []
            for j, (ci, lines) in enumerate(cls):
                t = " ".join(lines)
                if j and hk(s, "conn", j) % 2 == 0 and not t.startswith(("IF", "(")):
                    t = conn[1 + hk(s, "cw", j) % 4] + t[0].lower() + t[1:] if not t.startswith(("Notwithstanding",)) else t
                para.append(t)
            para.append(defline)
            out.append(" ".join(para))
        else:
            if lay != "memo" and hk(s, "rh") % 2 == 0:
                out.append(self.k(["Rules", "Decision rules", "How cases are decided"], "rhh"))
            for ci, lines in cls:
                out.append(f"{self.label(ci)} {lines[0]}")
                for x in lines[1:]:
                    out.append(f"    {x}")
            out.append(defline)
        if prec_lines and not prec_before:
            if lay == "prose" or len(prec_lines) == 1:
                out.append(" ".join(prec_lines))
            else:
                out.append(self.k(["Order of precedence:", "Conflicts between rules:", "Precedence:"], "ph"))
                out += [f"- {x}" for x in prec_lines]
        if pol["ev"]:
            a, b = D.sources
            w = (a, b)[pol["ev"]["w"]]
            out.append(self.k([f"Where {a} and {b} disagree about a fact, go by {w}.",
                               f"If {a} and {b} give different accounts of a fact, rely on {w}."], "ev"))
        for pid in pol["pp"]:
            sch = D.preds[pid].schedule(pol["pp"][pid], (s,), self.ctx)
            if sch:
                out.append(sch)
        if pol.get("noise"):
            out.append(self.k(["General notes:", "Other information:", "Notes:"], "nh"))
            out += [f"- {x}" for x in pol["noise"]]
        R["flags"] = {k: sorted(v) for k, v in self.flags.items()}
        return "\n".join(out), R


# =============================================================================================== rendering: case
def make_ctx(D, pol, rng):
    name, sub, obj, pos = person(rng)
    refl = {"she": "herself", "he": "himself", "they": "themselves"}[sub]
    ctx = {"n": name, "sub": sub, "obj": obj, "pos": pos, "refl": refl, "Sub": cap(sub), "Pos": cap(pos),
           "org": pol["org"], "cur": pol["cur"]}
    for k, vs in D.extra_ctx.items():
        ctx[k] = rng.choice(vs)
    if "g" in ctx:
        ctx["G"] = cap(ctx["g"])
    if "subj" in ctx:
        ctx["a_subjtask"] = art(f"{ctx['subj']} {ctx['task']}")
    return ctx


def bind_ctx(D, ctx, f):
    c = dict(ctx)
    for fid, F in D.facts.items():
        if F.binds and fid in f and f[fid] is not None:
            c[F.binds] = F.bind(f[fid])
    if "item" in c:
        c["a_item"] = art(c["item"])
    return c


def fact_shown(D, pol, f, fid, T):
    F = D.facts[fid]
    if F.req is None:
        return True
    return T.get(F.req[0]) == F.req[1]


def ev_sentence(D, pol, f, ctx, ckey):
    fid = pol["ev"]["fact"]
    F = D.facts[fid]
    a, b = D.sources
    gov, other = f[fid], f["__ev"]
    va, vb = (gov, other) if pol["ev"]["w"] == 0 else (other, gov)
    pa = (F.ev[0] if va else F.ev[1]).format(**ctx)
    pb = (F.ev[0] if vb else F.ev[1]).format(**ctx)
    if va == vb:
        return f"Both {a} and {b} say that {pa}."
    return pick([f"{cap(a)} says that {pa}, but according to {b}, {pb}.", f"According to {a}, {pa}; according to {b}, {pb}."],
                ckey, "evs").format()


def render_case(D, pol, f, ctx0, ckey, extra_line=None):
    ctx = bind_ctx(D, ctx0, f)
    T = None
    try:
        T = truths(D, pol, next(completions(D, pol, f)))
    except StopIteration:
        T = {}
    sents = [pick(D.intro, ckey, "intro").format(**ctx)]
    shown = {}
    for fid in sorted(set(pol["facts"]) | set(pol["distract"]), key=lambda x: D.facts[x].order):
        F = D.facts[fid]
        if not fact_shown(D, pol, f, fid, T):
            continue
        if f.get(fid) is None:
            s = F.unknown(ctx, (ckey,))
        elif pol["ev"] and pol["ev"]["fact"] == fid:
            s = ev_sentence(D, pol, f, ctx, ckey)
        else:
            s = F.render(f[fid], ctx, (ckey,))
        if s:
            s = cap(s)
            sents.append(s)
            shown[fid] = s
    if extra_line:
        sents.append(extra_line)
    head = pick(["Case:", "Situation:", "Case notes:", "Facts of the case:", "Request details:"], ckey, "head")
    if hk(ckey, "bul") % 10 < 3:
        body = "\n".join(f"- {x}" for x in sents)
        return f"{head}\n{body}", shown, ctx
    return f"{head} " + " ".join(sents), shown, ctx


# =============================================================================================== questions
QG = {
    "approved": ["Under the policy above, is {wr} {pas}?", "Applying every rule, exception and precedence statement above, is {wr} {pas}?",
                 "According to the policy, should {wr} be {pas}?"],
    "denied": ["Under the policy above, is {wr} {dpas}?", "Applying the policy exactly as written, must {wr} be {dpas}?",
               "According to the policy, should {wr} be {dpas}?"],
    "est_approved": ["Do the stated facts establish that {wr} is {pas} under the policy?",
                     "Based only on the facts given, can it be concluded that {wr} is {pas} under the policy?"],
    "est_denied": ["Do the stated facts establish that {wr} is {dpas} under the policy?",
                   "Based only on the facts given, can it be concluded that {wr} is {dpas} under the policy?"],
    "outcome_is": ['Under the policy, is the outcome for {wr} "{code}"?', 'Is "{code}" the correct outcome for {wr} under the policy above?',
                   'Applying the policy, should {wr} be decided as "{code}"?'],
    "est_outcome": ['Do the stated facts establish that the outcome for {wr} is "{code}"?',
                    'Based only on the facts given, is it certain that the outcome for {wr} is "{code}"?'],
    "claim": ["Is {rev}'s conclusion correct under the policy?", "Did {rev} apply the policy correctly?",
              "Is the conclusion reached by {rev} right under the policy above?"],
    "hypo": ['Suppose the case notes had said instead: "{h}" Everything else stays the same. Would {wr} then be {pas} under the policy?',
             'If the following were true instead: "{h}" (with every other fact unchanged), would {wr} be {pas} under the policy?'],
    "hypo_outcome": ['Suppose the case notes had said instead: "{h}" Everything else stays the same. Would the outcome for {wr} then be "{code}"?',
                     'If the following were true instead: "{h}" (with every other fact unchanged), would the outcome for {wr} be "{code}"?'],
    "choice": ["Which outcome does the policy require for {wr}?", "Under the policy above, how should {wr} be decided?",
               "Which decision applies to {wr} under this policy?",
               "Applying the policy's exceptions and order of precedence, what is the outcome for {wr}?"],
}
REVIEWERS = ["the duty manager", "a colleague", "the first reviewer", "the assistant on the desk", "the previous case handler", "a trainee"]

DEFS = {
    "approved": {"yes": "Applying every rule, exception (and exception to an exception), definition and the stated precedence to the facts, the policy's outcome is approval (accepted, paid, granted, dispensed, allowed, and so on).",
                 "no": "Applying the policy exactly as written, the outcome is refusal: a requirement fails or a refusal rule prevails, and no exception or higher-priority rule saves the request."},
    "denied": {"yes": "Applying the policy exactly as written, the outcome is refusal: a requirement fails or a refusal rule prevails, and no exception or higher-priority rule saves the request.",
               "no": "Applying every rule, exception, definition and the stated precedence to the facts, the policy's outcome is approval, not refusal."},
    "est_approved": {"yes": "The stated facts are enough to show approval: every value that an unknown fact could take still leads to approval under the policy.",
                     "no": "Either the policy leads to refusal, or a fact marked as unknown could change the outcome, so approval is not established."},
    "est_denied": {"yes": "The stated facts are enough to show refusal: every value that an unknown fact could take still leads to refusal under the policy.",
                   "no": "Either the policy leads to approval, or a fact marked as unknown could change the outcome, so refusal is not established."},
    "outcome_is": {"yes": "The outcome named in the question is exactly the one the policy gives after applying its conditions, exceptions, definitions and its explicit order of precedence.",
                   "no": "The policy gives a different outcome from the one named, for example because an exception applies or a higher-priority rule prevails."},
    "est_outcome": {"yes": "The stated facts are enough to show that the named outcome applies: every value an unknown fact could take leads to that outcome.",
                    "no": "The policy gives another outcome, or a fact marked as unknown could change the outcome, so the named outcome is not established."},
    "claim": {"yes": "The conclusion recorded in the case (someone else's decision) matches the outcome the policy actually gives for the stated facts.",
              "no": "The recorded conclusion differs from the outcome the policy gives, even if the person relied on a rule that does apply but is overridden."},
    "hypo": {"yes": "With only the supposed change made and every other fact kept, applying the policy would give approval.",
             "no": "With only the supposed change made and every other fact kept, applying the policy would not give approval."},
    "hypo_outcome": {"yes": "With only the supposed change made and every other fact kept, the policy would give exactly the named outcome.",
                     "no": "With only the supposed change made and every other fact kept, the policy would give a different outcome."},
}
UNDET_DEF = ("A fact marked as unknown matters: some values it could take lead to one outcome and other values to another, "
             "so the policy's outcome cannot be fixed from the stated facts.")


def qvars(D, ctx):
    return {"wr": D.wr.format(**ctx), "pas": D.appr["pas"], "dpas": D.deny["pas"], "n": ctx["n"]}


def question(D, qid, ctx, qkey, code=None, rev=None, h=None):
    v = qvars(D, ctx)
    if qid in ("approved", "denied") and hk(qkey, "dq") % 2 == 0:
        seq = D.q_appr if qid == "approved" else D.q_deny
        return pick(seq, qkey, "dqq").format(**ctx)
    return pick(QG[qid], qkey, "q", qid).format(code=code, rev=rev, h=h, **v)


def gold_of(qid, outs, target=None):
    """outs: set of possible outcomes (singleton when determined)."""
    det = len(outs) == 1
    o = next(iter(outs)) if det else None
    if qid == "approved":
        assert det
        return "yes" if o == "approve" else "no"
    if qid == "denied":
        assert det
        return "yes" if o == "deny" else "no"
    if qid == "est_approved":
        return "yes" if outs == {"approve"} else "no"
    if qid == "est_denied":
        return "yes" if outs == {"deny"} else "no"
    if qid in ("outcome_is", "claim", "hypo_outcome"):
        assert det
        return "yes" if o == target else "no"
    if qid == "hypo":
        assert det
        return "yes" if o == "approve" else "no"
    if qid == "est_outcome":
        return "yes" if outs == {target} else "no"
    if qid == "choice":
        return o if det else UNDET
    raise ValueError(qid)


# =============================================================================================== sampling
def typical_pp(D, fid, pol):
    """Parameters of the domain's predicates on a fact that the policy does not use (for distractor values);
    fixed per policy so twins agree."""
    r = random.Random(hk(pol["sty"], "typ", fid))
    return [P.params(r) for P in D.preds.values() if P.fact == fid and not isinstance(P, InPred)]


def sample_facts(D, pol, rng):
    f = {}
    for fid in pol["facts"]:
        pp = [pol["pp"][p] for p in preds_on_fact(D, pol, fid)]
        f[fid] = D.facts[fid].sample(rng, pp)
    for fid in pol["distract"]:
        f[fid] = D.facts[fid].sample(rng, typical_pp(D, fid, pol))
    for fid, F in D.facts.items():
        if F.binds and fid not in f:
            f[fid] = F.sample(rng, [])
    if pol["ev"]:
        fid = pol["ev"]["fact"]
        f["__ev"] = (not f[fid]) if rng.random() < 0.85 else f[fid]
    return f


def score_case(D, pol, f):
    T = truths(D, pol, f)
    out, fired = outcome(pol, T)
    sc = 0.0
    for c in pol["clauses"]:
        if c["exc"] and base_holds(c, T):
            sc += 1.5
            if lv(c["exc"][0], T):
                sc += 1.0
                if len(c["exc"]) > 1:
                    sc += 0.8
    if len({pol["clauses"][i]["out"] for i in fired}) >= 2:
        sc += 2.0
    for pid, p in pol["pp"].items():
        P = D.preds[pid]
        v = f[P.fact]
        if v is not None and P.boundary(v, p):
            sc += 0.7
    for t in pol["terms"]:
        if T[t["id"]]:
            sc += 0.5
    return sc, out


def hideable(D, pol, f, fid):
    F = D.facts[fid]
    if not F.hide or F.binds or (pol["ev"] and pol["ev"]["fact"] == fid):
        return False
    # a parent of a stated child fact cannot be unknown
    for gid in pol["facts"]:
        G = D.facts[gid]
        if G.req and D.preds[G.req[0]].fact == fid:
            return False
    if F.req is not None:
        T = truths(D, pol, next(completions(D, pol, f)))
        if T.get(F.req[0]) != F.req[1]:
            return False
    return True


class Balancer:
    def __init__(self):
        self.c = collections.Counter()

    def weight(self, key):
        return 1.0 / (1.0 + self.c[key])

    def add(self, key):
        self.c[key] += 1


def pick_case(D, pol, rng, bal, balkey, k=14):
    best = []
    for _ in range(k):
        f = sample_facts(D, pol, rng)
        if not valid(D, pol, f):
            continue
        sc, out = score_case(D, pol, f)
        w = (0.6 + sc) * bal.weight((balkey, out)) ** 1.5
        best.append((w, f, out))
    if not best:
        return None, None
    tot = sum(w for w, _, _ in best)
    r = rng.random() * tot
    for w, f, out in best:
        r -= w
        if r <= 0:
            return f, out
    return best[-1][1], best[-1][2]


def exc_facts(D, pol):
    s = set()
    for c in pol["clauses"]:
        for x in c["exc"]:
            if not x[0].startswith("T_"):
                s.add(D.preds[x[0]].fact)
            else:
                t = next(t for t in pol["terms"] if t["id"] == x[0])
                s |= {D.preds[l[0]].fact for l in t["cond"]["lits"]}
    return s


def flip_candidates(D, pol, f, keep_hidden=True):
    """All single-fact changes of the policy facts (values from the fact's candidate list)."""
    out = []
    qtext = " ".join([D.wr] + list(D.q_appr) + list(D.q_deny))
    for fid in pol["facts"]:
        cur = f.get(fid)
        if cur is None:
            continue
        F = D.facts[fid]
        for v in fact_values(D, pol, fid):
            if v == cur:
                continue
            if F.binds and "{" + F.binds + "}" in qtext and F.bind(v) != F.bind(cur):
                continue  # keep the question text identical between a row and its twin
            g = dict(f)
            g[fid] = v
            if not valid(D, pol, g):
                continue
            out.append((fid, v, g))
    return out


def weight_flip(D, pol, fid, v, g, ex):
    w = 1.0
    if fid in ex:
        w *= 3.0
    for pid in preds_on_fact(D, pol, fid):
        if D.preds[pid].boundary(v, pol["pp"][pid]):
            w *= 2.0
    return w


def wpick(rng, items):
    tot = sum(w for w, _ in items)
    r = rng.random() * tot
    for w, x in items:
        r -= w
        if r <= 0:
            return x
    return items[-1][1]


# =============================================================================================== edge tags
def row_edges(D, pol, R, f, qid, state, flip_fid=None):
    tags = set()
    comp = next(completions(D, pol, f))
    T = truths(D, pol, comp)
    cl = pol["clauses"]
    flags = {int(k) if str(k).isdigit() else k: set(v) for k, v in R["flags"].items()}
    ex = exc_facts(D, pol)
    relevant = set()
    for i, c in enumerate(cl):
        if base_holds(c, T) or fire(c, T):
            relevant.add(i)
        if c["exc"] and base_holds(c, T):
            tags.add("exception")
            if len(c["exc"]) >= 2 and lv(c["exc"][0], T):
                tags.add("double_negation")
    if flip_fid is not None and flip_fid in ex:
        tags.add("exception")
    for i in relevant:
        fl = flags.get(i, set())
        if "neg" in fl or cl[i].get("neg"):
            tags.add("negation")
        if "dneg" in fl:
            tags.add("double_negation")
        if "quant" in fl:
            tags.add("quantifier")
    if qid in ("denied", "est_denied"):
        tags.add("negation")
    for t in pol["terms"]:
        tags.add("multi_hop")
        if isinstance(t["cond"]["mode"], int) or t["cond"]["mode"] == "any":
            tags.add("quantifier")
    out, fired = outcome(pol, T)
    if len({cl[i]["out"] for i in fired}) >= 2:
        tags.add("multi_hop")
    for pid, p in pol["pp"].items():
        P = D.preds[pid]
        v = comp[P.fact]
        F = D.facts[P.fact]
        if isinstance(P, (NumPred, TablePred, RatioPred, PairPred, TimePred)) and f.get(P.fact) is not None and P.boundary(v, p):
            tags.add("numeric")
        for tg in P.tags:
            if tg in ("table", "units", "implicit", "temporal", "multi_hop", "numeric"):
                if tg == "multi_hop" and not p.get("sched"):
                    continue
                tags.add(tg)
        if isinstance(P, InPred) and p.get("sched"):
            tags |= {"multi_hop", "table"}
        if isinstance(F, NumFact) and f.get(P.fact) is not None and F.uses_dates(f[P.fact], (pol["_ckey"],)):
            tags.add("temporal")
        if isinstance(P, NumPred) and P.hours:
            if F.uses_days(comp[P.fact], (pol["_ckey"],)) != bool(p.get("days")):
                tags.add("units")
    if flip_fid is not None:
        for pid in preds_on_fact(D, pol, flip_fid):
            if isinstance(D.preds[pid], (NumPred, TablePred, RatioPred, PairPred, TimePred)):
                tags.add("numeric")
    if any(f.get(fid) is None for fid in pol["facts"]):
        tags.add("missing_info")
    if pol["ev"] and f["__ev"] != f[pol["ev"]["fact"]]:
        tags.add("conflicting_evidence")
    if qid == "claim":
        tags.add("reported_speech")
    if qid in ("hypo", "hypo_outcome"):
        tags.add("hypothetical")
    if len(state) > 2200:
        tags.add("long_context")
    tags = [t for t in ["negation", "double_negation", "exception", "missing_info", "conflicting_evidence", "temporal", "numeric",
                        "units", "quantifier", "hypothetical", "reported_speech", "implicit", "long_context", "table", "multi_hop"] if t in tags]
    for t in tags:
        assert t in EDGE_TAGS
    return ",".join(tags) if tags else None


# =============================================================================================== pair construction
BIN_Q = [("approved", 0.29), ("denied", 0.21), ("est_approved", 0.12), ("est_denied", 0.09), ("claim", 0.17), ("hypo", 0.12)]
MUL_Q = [("choice", 0.52), ("outcome_is", 0.22), ("est_outcome", 0.07), ("claim", 0.11), ("hypo_outcome", 0.08)]
BIN_ARCH = [("gate", 0.22), ("override", 0.17), ("approve_if", 0.12), ("kofn", 0.06), ("conflict", 0.17), ("table", 0.12), ("defs", 0.14)]
MUL_ARCH = [("gate", 0.34), ("override", 0.18), ("approve_if", 0.1), ("conflict", 0.1), ("table", 0.14), ("defs", 0.14)]


def tempting(D, pol, f, true_out):
    """Outcomes a careless reader might pick: lower-priority fired clauses, clauses blocked only by an exception,
    or the default."""
    T = truths(D, pol, f)
    cand = []
    for i, c in enumerate(pol["clauses"]):
        if base_holds(c, T) and c["out"] != true_out:
            cand.append(c["out"])
    if pol["default"] != true_out:
        cand.append(pol["default"])
    return cand


def policy_outs(D, pol):
    outs = {c["out"] for c in pol["clauses"]} | {pol["default"]}
    return [c for c in D.codes if c in outs] if pol["multi"] else ["approve", "deny"]


def make_pair(D, rng, multi, qid, bal, idx):
    arch = wchoice(rng, MUL_ARCH if multi else BIN_ARCH)
    if D.name == "content" and arch in ("approve_if", "kofn"):
        arch = "gate"
    pol = build_policy(D, rng, multi, arch)
    if pol is None:
        return None
    pol["org"] = rng.choice(D.orgs)
    pol["noise"] = rng.sample(D.noise, rng.choice([0, 0, 1, 1, 2])) if D.noise else []
    PT = PolicyText(D, pol)
    ptext, R = PT.render()
    pol["R"] = R
    balkey = (D.name, multi, qid)
    f, out = pick_case(D, pol, rng, bal, balkey)
    if f is None:
        return None
    ckey = rng.randrange(10 ** 9)
    pol["_ckey"] = ckey
    ctx0 = make_ctx(D, pol, rng)
    qkey = rng.randrange(10 ** 9)
    ex = exc_facts(D, pol)
    target, rev, h, hyp = None, None, None, None
    base_f, twin_f, flip_fid = f, None, None
    undet_opt = False

    def outs_of(g):
        o1 = outcomes(D, pol, g)
        o2 = outcomes2(D, pol, g)
        assert o1 == o2, ("evaluator disagreement", D.name, o1, o2)
        return o1

    hidden_kind = None
    if qid in ("est_approved", "est_denied", "est_outcome") or (qid == "choice" and rng.random() < 0.3):
        undet_opt = qid == "choice"
        r = rng.random()
        hid = [fid for fid in pol["facts"] if hideable(D, pol, f, fid)]
        if r < (0.5 if qid != "choice" else 0.45) and hid:
            # hide a decisive fact (undetermined base) and reveal it in the twin
            rng.shuffle(hid)
            for fid in hid:
                g = dict(f)
                g[fid] = None
                if len(outs_of(g)) >= 2:
                    base_f, flip_fid, hidden_kind = g, fid, "decisive"
                    break
        elif r < 0.75 and hid:
            rng.shuffle(hid)
            for fid in hid:
                g = dict(f)
                g[fid] = None
                if len(outs_of(g)) == 1:
                    base_f, hidden_kind = g, "irrelevant"
                    break
    elif qid in ("approved", "denied", "outcome_is", "claim", "choice") and rng.random() < 0.12:
        hid = [fid for fid in pol["facts"] if hideable(D, pol, f, fid)]
        rng.shuffle(hid)
        for fid in hid:
            g = dict(f)
            g[fid] = None
            if len(outs_of(g)) == 1:
                base_f, hidden_kind = g, "irrelevant"
                break

    bo = outs_of(base_f)
    codes = policy_outs(D, pol)
    if qid in ("approved", "denied", "outcome_is", "claim", "hypo", "hypo_outcome") and len(bo) != 1:
        return None
    if qid in ("outcome_is", "est_outcome", "claim"):
        o = next(iter(bo)) if len(bo) == 1 else rng.choice(sorted(bo))
        tm = tempting(D, pol, {k: (v if v is not None else f[k]) for k, v in base_f.items()}, o)
        if rng.random() < 0.5:
            target = o
        elif tm:
            target = rng.choice(tm)
        else:
            target = rng.choice([c for c in codes if c != o])
    if qid == "claim":
        rev = rng.choice(REVIEWERS)
    if qid in ("hypo", "hypo_outcome"):
        cands = []
        Tb = truths(D, pol, next(completions(D, pol, base_f)))
        for fid, v, g in flip_candidates(D, pol, base_f):
            if pol["ev"] and fid == pol["ev"]["fact"]:
                continue
            if not fact_shown(D, pol, base_f, fid, Tb):
                continue
            if any(D.facts[x].req and D.preds[D.facts[x].req[0]].fact == fid for x in pol["facts"]):
                continue
            cands.append((weight_flip(D, pol, fid, v, g, ex), (fid, v)))
        if not cands:
            return None
        hyp = wpick(rng, cands)
        if qid == "hypo_outcome":
            ho = outs_of({**base_f, hyp[0]: hyp[1]})
            o = next(iter(ho))
            tm = tempting(D, pol, {**base_f, hyp[0]: hyp[1]}, o)
            target = o if rng.random() < 0.5 else (rng.choice(tm) if tm else rng.choice([c for c in codes if c != o]))

    def gold_for(g):
        if qid in ("hypo", "hypo_outcome"):
            return gold_of(qid, outs_of({**g, hyp[0]: hyp[1]}), target)
        return gold_of(qid, outs_of(g), target)

    gb = gold_for(base_f)
    # ---------------------------------------------------------------- twin
    if hidden_kind == "decisive":
        cands = []
        for v in fact_values(D, pol, flip_fid):
            g = dict(base_f)
            g[flip_fid] = v
            if not valid(D, pol, g):
                continue
            if len(outs_of(g)) != 1:
                continue
            gt = gold_for(g)
            if gt != gb:
                cands.append((weight_flip(D, pol, flip_fid, v, g, ex), g))
        if not cands:
            return None
        twin_f = wpick(rng, cands)
    else:
        cands = []
        for fid, v, g in flip_candidates(D, pol, base_f):
            if hyp is not None and fid == hyp[0]:
                continue
            os_ = outs_of(g) if qid not in ("hypo", "hypo_outcome") else outs_of({**g, hyp[0]: hyp[1]})
            if len(os_) != 1 and qid not in ("est_approved", "est_denied", "est_outcome") and not undet_opt:
                continue
            gt = gold_for(g)
            if gt != gb:
                cands.append((weight_flip(D, pol, fid, v, g, ex), (fid, g)))
        if qid in ("est_approved", "est_denied", "est_outcome") and gb == "yes" and rng.random() < 0.5:
            hc = []
            for fid in pol["facts"]:
                if base_f.get(fid) is None or not hideable(D, pol, base_f, fid):
                    continue
                g = dict(base_f)
                g[fid] = None
                if gold_for(g) != gb:
                    hc.append((2.0, (fid, g)))
            if hc:
                cands = hc
        if not cands:
            return None
        flip_fid, twin_f = wpick(rng, cands)
    gt = gold_for(twin_f)
    assert gt != gb
    diff = [k for k in set(base_f) | set(twin_f) if base_f.get(k) != twin_f.get(k)]
    assert len(diff) == 1 and diff[0] in pol["facts"], diff  # a twin changes (or reveals / hides) exactly one policy fact
    # ---------------------------------------------------------------- render both
    rows = []
    for which, g, gold in (("base", base_f, gb), ("twin", twin_f, gt)):
        extra = None
        if qid == "claim":
            if pol["multi"]:
                concl = pick(D.code_clause[target], ckey, "cc")
            else:
                concl = pick((D.appr if target == "approve" else D.deny)["clause"], ckey, "cc")
            extra = pick(["{R} reviewed the case and concluded that {c}.", "{R} has already looked at the case and decided that {c}.",
                          "A note in the file from {r} says that {c}."], ckey, "rv").format(R=cap(rev), r=rev, c=concl)
        case, shown, ctx = render_case(D, pol, g, ctx0, ckey, extra)
        if qid in ("hypo", "hypo_outcome"):
            hctx = bind_ctx(D, ctx0, {**g, hyp[0]: hyp[1]})
            h = cap(D.facts[hyp[0]].render(hyp[1], hctx, (ckey,)))
            if not h or h in case:
                return None
        code_txt = None
        if target is not None:
            code_txt = target if pol["multi"] else None
        if qid == "choice":
            q = question(D, "choice", ctx, qkey)
        elif qid in ("outcome_is", "est_outcome", "hypo_outcome"):
            q = question(D, qid, ctx, qkey, code=target)
        elif qid == "claim":
            q = question(D, qid, ctx, qkey, rev=rev)
        elif qid == "hypo":
            q = question(D, qid, ctx, qkey, h=h)
        else:
            q = question(D, qid, ctx, qkey)
        if qid == "hypo_outcome":
            q = question(D, qid, ctx, qkey, code=target, h=h)
        state = tidy(ptext + "\n\n" + case)
        q = tidy(q)
        if qid == "choice":
            opts = list(codes) + ([UNDET] if undet_opt else [])
            assert gold in opts, (gold, opts)
        else:
            opts = ["yes", "no"]
        os_ = outs_of(g) if qid not in ("hypo", "hypo_outcome") else outs_of({**g, hyp[0]: hyp[1]})
        comp_f = next(completions(D, pol, g))
        _, fired = outcome(pol, truths(D, pol, comp_f))
        orig = {"outcome": (next(iter(os_)) if len(os_) == 1 else "undetermined"), "possible": sorted(os_),
                "fired": [PT.ref(i) or f"rule {PT.num[i]}" for i in fired], "qid": qid,
                "facts": {k: v for k, v in g.items() if k in pol["facts"] or k == "__ev"}}
        if target is not None:
            orig["target"] = target
        if hyp is not None:
            orig["hypothetical"] = {"fact": hyp[0], "value": hyp[1]}
        edge = row_edges(D, pol, R, g, qid, state, flip_fid if which == "twin" else None)
        rid = f"{KEY}-{D.name}-{idx:05d}" + ("-twin" if which == "twin" else "")
        defs_id = f"choice_{D.name}" if qid == "choice" else qid
        meta = {"dataset": f"program generator golden_src/gen/{KEY}.py", "config": f"{D.name}:{pol['arch']}:{'multi' if multi else 'binary'}:{pol['mode']}",
                "revision": "gen-v1", "licence": "Generated by Claude-written program in this repo (no third-party text)", "split": "train",
                "orig_label": orig, "family": FAMILY, "edge": edge, "defs": defs_id}
        if which == "twin":
            meta["twin_of"] = f"{KEY}-{D.name}-{idx:05d}"
        rows.append({"key": KEY, "rid": rid, "state": state, "instructions": q, "options": opts, "gold": gold, "soft": None, "meta": meta})
        # keep what the self-check needs (dropped before writing)
        rows[-1]["_chk"] = (D.name, pol, g, qid, target, hyp, shown)
    if rows[0]["state"] == rows[1]["state"] and rows[0]["instructions"] == rows[1]["instructions"]:
        return None
    bal.add((balkey, next(iter(bo)) if len(bo) == 1 else "undet"))
    return rows


# =============================================================================================== self-check
def recheck(row):
    """Recompute the gold label from scratch with the second evaluator and check the rendered facts."""
    dname, pol, g, qid, target, hyp, shown = row["_chk"]
    D = DOM[dname]
    gg = {**g, hyp[0]: hyp[1]} if hyp is not None else g
    os2 = outcomes2(D, pol, gg)
    if qid == "choice":
        want = next(iter(os2)) if len(os2) == 1 else UNDET
    elif qid == "approved":
        want = "yes" if os2 == {"approve"} else "no"
        assert len(os2) == 1
    elif qid == "denied":
        want = "yes" if os2 == {"deny"} else "no"
        assert len(os2) == 1
    elif qid == "est_approved":
        want = "yes" if os2 == {"approve"} else "no"
    elif qid == "est_denied":
        want = "yes" if os2 == {"deny"} else "no"
    elif qid in ("outcome_is", "claim", "hypo_outcome"):
        assert len(os2) == 1
        want = "yes" if os2 == {target} else "no"
    elif qid == "est_outcome":
        want = "yes" if os2 == {target} else "no"
    elif qid == "hypo":
        assert len(os2) == 1
        want = "yes" if os2 == {"approve"} else "no"
    else:
        raise ValueError(qid)
    assert want == row["gold"], (row["rid"], want, row["gold"])
    for fid, s in shown.items():
        assert tidy(s) in row["state"], (row["rid"], fid)
    # every policy fact that a clause reads is stated (known, unknown or conflicting sources) unless its
    # presupposition fails
    T = truths(D, pol, next(completions(D, pol, g)))
    for fid in pol["facts"]:
        F = D.facts[fid]
        if F.binds:
            continue
        if F.req is None or T.get(F.req[0]) == F.req[1]:
            assert fid in shown, (row["rid"], fid)
    return True


# =============================================================================================== main
def append_manifest(rec):
    import time as _t
    line = json.dumps(rec, ensure_ascii=False)
    for _ in range(20):
        text = MANIFEST.read_text() if MANIFEST.exists() else ""
        lines = text.splitlines()
        mine = [i for i, ln in enumerate(lines) if ln.strip() and json.loads(ln).get("key") == rec["key"]]
        if not mine:
            with open(MANIFEST, "a") as fh:
                fh.write(line + "\n")
            return
        if len(mine) == 1 and lines[mine[0]] == line:
            return
        for i in mine:
            assert json.loads(lines[i]).get("family") == FAMILY
        new = [ln for i, ln in enumerate(lines) if i not in set(mine)] + [line]
        tmp = MANIFEST.with_suffix(".jsonl.tmp_pe")
        tmp.write_text("\n".join(new) + "\n")
        if (MANIFEST.read_text() if MANIFEST.exists() else "") == text:
            os.replace(tmp, MANIFEST)
            return
        tmp.unlink()
        _t.sleep(0.2)
    raise RuntimeError("manifest kept changing")


def main():
    t0 = time.time()
    rng = random.Random(SEED)
    bal = Balancer()
    rows, seen = [], set()
    per_dom = N_PAIRS // len(DOMAINS)
    extra = N_PAIRS - per_dom * len(DOMAINS)
    stats = collections.Counter()
    fails = collections.Counter()
    idx = 0
    for di, D in enumerate(DOMAINS):
        quota = per_dom + (1 if di < extra else 0)
        made = 0
        tries = 0
        while made < quota:
            tries += 1
            assert tries < quota * 60, (D.name, made, fails)
            multi = rng.random() < 0.45
            qid = wchoice(rng, MUL_Q if multi else BIN_Q)
            try:
                pr = make_pair(D, rng, multi, qid, bal, idx)
            except AssertionError:
                raise
            if pr is None:
                fails[(D.name, qid)] += 1
                continue
            k0 = norm(pr[0]["state"]) + "||" + norm(pr[0]["instructions"])
            k1 = norm(pr[1]["state"]) + "||" + norm(pr[1]["instructions"])
            if k0 in seen or k1 in seen or k0 == k1:
                fails[("dup", D.name)] += 1
                continue
            seen.update({k0, k1})
            rows += pr
            made += 1
            idx += 1
            stats[(D.name, "multi" if multi else "binary", qid)] += 1
        print(f"{D.name}: {made} pairs ({tries} tries) {time.time() - t0:.0f}s", flush=True)
    # ------------------------------------------------------------ self-check every row
    for r in rows:
        recheck(r)
    for r in rows:
        del r["_chk"]
    src = Path(__file__).resolve()
    h = hashlib.sha256()
    for p in sorted(HERE.glob("pe_*.py")) + [src]:
        h.update(p.read_bytes())
    rev = "gen-v1+sha256:" + h.hexdigest()[:16]
    for r in rows:
        r["meta"]["revision"] = rev
    check_rows(rows)
    dry = os.environ.get("PE_OUT")
    RAW.mkdir(parents=True, exist_ok=True)
    out = Path(dry) if dry else RAW / f"{KEY}.jsonl"
    with open(out, "w") as fh:
        for r in rows:
            fh.write(json.dumps(r, ensure_ascii=False) + "\n")
    # re-read the written file: same rows, twins alternate gold
    back = [json.loads(x) for x in open(out)]
    assert back == rows
    by = {r["rid"]: r for r in back}
    for r in back:
        if "twin_of" in r["meta"]:
            b = by[r["meta"]["twin_of"]]
            assert b["gold"] != r["gold"] and b["instructions"] == r["instructions"] or b["meta"]["defs"].startswith("hypo")
    if dry:
        summary(rows)
        print("fails:", fails.most_common(12))
        print(f"DRY RUN wrote {out} ({len(rows)} rows) in {time.time() - t0:.0f}s")
        return
    # ------------------------------------------------------------ defs
    for qid, d in DEFS.items():
        write_defs(f"{KEY}__{qid}", d)
    for D in DOMAINS:
        d = {c: D.code_def[c] for c in D.codes}
        d[UNDET] = UNDET_DEF
        write_defs(f"{KEY}__choice_{D.name}", d)
    summary(rows)
    print("pairs by (domain, type, qid):", len(stats))
    print("fails:", fails.most_common(12))
    yn = [r for r in rows if r["options"] == ["yes", "no"]]
    ch = [r for r in rows if r["options"] != ["yes", "no"]]
    notes = (f"Program-generated policy application over 10 domains (returns, ticket refunds, home insurance, HR leave, school "
             f"extensions, grants, travel expenses, pharmacy, access control, content moderation): rules with 'unless'/'except'/"
             f"'only if' exceptions and exceptions to exceptions (up to 3 levels), defined terms, k-of-n requirements, tables and "
             f"schedules, 'notwithstanding' overrides and conflicting clauses resolved by an explicit precedence statement "
             f"(first-match, later-prevails, outcome ranking or explicit prevail pairs). {len(yn)} yes/no rows (approved, denied, "
             f"do-the-facts-establish, outcome-is, a colleague's conclusion, hypothetical change) + {len(ch)} outcome-code choice "
             f"rows (some with 'cannot be determined'). Every base row has a fact-flip twin (meta.twin_of) with the opposite/"
             f"changed gold. Labels recomputed by an independent evaluator that reads precedence only from the rendered text.")
    append_manifest({"key": KEY, "family": FAMILY, "dataset": f"{KEY} (program generator, golden_src/gen/{KEY}.py)",
                     "licence": "n/a (program-generated; Claude-written templates and rules, labels by construction)",
                     "rows": len(rows), "qtype": "yesno+choice", "yesno_share": yesno_share(rows),
                     "edge_tags": edge_tags(rows), "notes": notes})
    print(f"wrote {out} ({len(rows)} rows) in {time.time() - t0:.0f}s")


if __name__ == "__main__":
    main()
