"""rc_core: the clause engine of yn2b F1a (gen3_rule_chain), yn2b/SPEC.md section 5 F1.

A document is a list of typed clauses (definitions, entitlement, requirements, exceptions, exceptions to exceptions,
exclusions, amendments with effective dates, a precedence rule, cross references, a limit table, a general limit and
time rules); a case is a dict of typed facts. `evaluate()` applies the clause graph to the case and returns the
outcome plus a trace. It is the only labeller of F1a (no model is called anywhere). `pivotal()` finds the clauses whose
deletion changes the outcome (SPEC: "decisive = the unique clause whose removal changes the outcome"; items with 0
or 2+ such clauses are rejected for that question). The SPEC 5 F1 shortcut solvers are evaluator MODES (ignore
exceptions, any exception applies, ignore amendments, the latest-dated clause wins, every boundary inclusive, the
first matching clause wins); keyword overlap is computed on the rendered text by the builder. Shortcuts are used for
tiers and distractors only, never for labels.

Semantics (every rule is also stated in the rendered document's own "General" clauses, so a reader needs nothing
else):
  * days: calendar or business days (Mon-Fri minus the listed public holidays); "the Nth day after X" is the date
    N (business) days after X; "N days before X" is the date N (business) days before X. "no later than" / "at least"
    are inclusive of that date, "before the Nth day after" / "more than N days before" exclusive.
  * an exception applies only to the clause it names and only when every condition holds and no exception to it
    applies; a period exception replaces the period of the time requirement it names.
  * an amendment replaces the figure it names for requests received on or after its effective date; a withdrawn
    amendment has no effect.
  * if two refusal grounds apply, the ground stated first in the document is the one recorded (true-mode latents
    with two grounds are rejected: SPEC 8.3 "two independent sufficient reasons").
  * a fact not shown in the case file is not established (missing documents = not included).
  * limits: the general limit and the category row of the limit table; when both apply, the document's precedence
    rule picks one (specific category prevails / the later clause prevails / the lower limit / a named clause).
    The benefit covers the amount requested up to the limit; above it, the benefit is cut to the limit.

Atoms reuse golden_src/gen helpers by import: pe_atoms.OPS / NEG_OP (comparators), nd_common.ftrim / ordn (exact
decimal text, ordinals) and nd_time.bdays_after (business-day stepping). F1b's unit factors are stated in its card,
so nd_units has nothing to add here.
"""
from __future__ import annotations

import copy
import datetime as dt
from fractions import Fraction

import mv_core as mv  # noqa: F401  (puts golden_src/gen on sys.path)
from pe_atoms import NEG_OP, OPS  # noqa: E402
from nd_common import ftrim, ordn  # noqa: E402
from nd_time import bdays_after  # noqa: E402
import rc_skins as SK  # noqa: E402

CANDIDATE_KINDS = ("req", "exc", "excexc", "excl", "amend", "lim_gen", "lim_tab")   # "decisive clause" candidates
MODES = ("ignore_exceptions", "any_exception", "ignore_amendments", "latest_dated", "all_inclusive", "first_match")
GATE_CODE = {"elig": "INELIG", "time": "LATE", "docs": "DOCS"}
CODE_GATE = {v: k for k, v in GATE_CODE.items()}
INCL = {"gt": "ge", "lt": "le", "ge": "ge", "le": "le"}
OP_WORDS = {"ge": "at least", "gt": "more than", "le": "at most", "lt": "less than"}


# ================================================================================================ small helpers
def D(s: str) -> dt.date:
    return dt.date.fromisoformat(s)


def iso(d: dt.date) -> str:
    return d.isoformat()


def F(x) -> Fraction:
    return Fraction(str(x)) if not isinstance(x, Fraction) else x


def num_text(x) -> str:
    return ftrim(F(x), 3, commas=True)


def bdays_before(start: dt.date, n: int, hol) -> dt.date:
    """The n-th business day before start (start excluded) - the mirror image of nd_time.bdays_after."""
    d, k = start, 0
    while k < n:
        d -= dt.timedelta(days=1)
        if d.weekday() < 5 and iso(d) not in hol:
            k += 1
    return d


def deadline(doc: dict, case: dict, n: int, direction: str) -> dt.date:
    """after: the date n (business) days after the event; before: the date n (business) days before it."""
    ev = D(case["event"])
    hol = set(doc["holidays"])
    if doc["count"] == "business":
        return D(bdays_after(iso(ev), n, hol)) if direction == "after" else bdays_before(ev, n, hol)
    return ev + dt.timedelta(days=n) if direction == "after" else ev - dt.timedelta(days=n)


def clause(doc: dict, cid: str) -> dict:
    return next(c for c in doc["clauses"] if c["id"] == cid)


def by_kind(doc: dict, *kinds) -> list[dict]:
    return [c for c in doc["clauses"] if c["kind"] in kinds]


def index_of(doc: dict) -> dict:
    return {c["id"]: i for i, c in enumerate(doc["clauses"])}


# ================================================================================================ figures
def base_figures(doc: dict) -> dict:
    """(clause id, field) -> figure as written in the clause text (before amendments)."""
    f = {}
    for c in doc["clauses"]:
        if c["kind"] == "defn" or (c["kind"] == "req" and c["gate"] == "elig" and not c.get("via")):
            f[(c["id"], "value")] = F(c["value"])
        elif c["kind"] == "req" and c["gate"] == "time":
            f[(c["id"], "n")] = int(c["n"])
        elif c["kind"] == "lim_gen":
            f[(c["id"], "limit")] = int(c["limit"])
        elif c["kind"] == "lim_tab":
            for cat, lim in c["rows"]:
                f[(c["id"], "row:" + cat)] = int(lim)
    return f


def _fig_value(field: str, text):
    return int(text) if field in ("n", "limit") or field.startswith("row:") else F(text)


def figures(doc: dict, case: dict, mode: str | None = None) -> tuple[dict, dict]:
    """Effective figures after amendments, and {(clause, field): amendment id applied}."""
    f = base_figures(doc)
    used = {}
    ams = by_kind(doc, "amend")
    if mode == "ignore_amendments":
        return f, used
    req = D(case["request"])
    if mode == "latest_dated":
        live = sorted(ams, key=lambda a: (a["eff"], a["k"]))
    else:
        live = sorted((a for a in ams if not a["withdrawn"] and D(a["eff"]) <= req), key=lambda a: (a["eff"], a["k"]))
    for a in live:
        key = (a["target"], a["field"])
        if key in f:
            f[key] = _fig_value(a["field"], a["new"])
            used[key] = a["id"]
    return f, used


# ================================================================================================ atoms + checks
def atom_holds(a: dict, case: dict, inclusive: bool = False) -> bool:
    if a["t"] == "flag":
        return case["flags"].get(a["f"]) is True
    if a["t"] == "amt":
        op = INCL[a["op"]] if inclusive else a["op"]
        return OPS[op](F(case["amount"]), F(a["value"]))
    raise ValueError(a)


def atoms_of(x: dict) -> list:
    """The conditions of an exception / exclusion as atoms, the category scope (if any) counted as one atom."""
    out = []
    if x.get("cats"):
        out.append({"t": "cat", "in": list(x["cats"])})
    return out + list(x.get("conds", []))


def atom_true(a: dict, case: dict, inclusive=False) -> bool:
    if a["t"] == "cat":
        return case["cat"] in a["in"]
    return atom_holds(a, case, inclusive)


def conds_hold(x: dict, case: dict, inclusive=False) -> bool:
    return all(atom_true(a, case, inclusive) for a in atoms_of(x))


def elig_ok(doc, case, r, figs, inclusive=False) -> bool:
    src = r["via"] if r.get("via") else r["id"]
    op = clause(doc, src)["op"]
    if inclusive:
        op = INCL[op]
    return OPS[op](F(case["elig"]), figs[(src, "value")])


def time_ok(doc, case, n: int, incl: bool, inclusive=False) -> bool:
    sk = SK.SKINS[doc["skin"]]
    dl = deadline(doc, case, n, sk["time"]["dir"])
    rq = D(case["request"])
    return rq <= dl if (incl or inclusive) else rq < dl


def base_ok(doc, case, r, figs, inclusive=False) -> bool:
    """The requirement's own test, before any exception."""
    if r.get("scope_type") and r["scope_type"] != case["type"]:
        return True
    if r["gate"] == "elig":
        return elig_ok(doc, case, r, figs, inclusive)
    if r["gate"] == "time":
        return time_ok(doc, case, figs[(r["id"], "n")], r["incl"], inclusive)
    if r["gate"] == "docs":
        return case["docs"] is True
    raise ValueError(r["gate"])


# ================================================================================================ evaluation
def evaluate(doc: dict, case: dict, mode: str | None = None, drop: frozenset = frozenset()) -> dict:
    """Apply the clause graph (minus the clause ids in `drop`) to the case. mode: None (the document as written) or
    one of MODES (a shortcut solver). Returns the trace: code, granted amount, requirement / exception / exclusion
    statuses, figures used, the limit chosen, and every refusal ground (in document order)."""
    d2 = doc if not drop else dict(doc, clauses=[c for c in doc["clauses"] if c["id"] not in drop])
    figs, used = figures(d2, case, mode)
    idx = index_of(d2)
    inclusive = mode == "all_inclusive"
    exc_by_target: dict = {}
    for x in by_kind(d2, "exc"):
        exc_by_target.setdefault(x["target"], []).append(x)
    excexc_by_target: dict = {}
    for y in by_kind(d2, "excexc"):
        excexc_by_target.setdefault(y["target"], []).append(y)

    def blocked(x) -> bool:
        return any(conds_hold(y, case, inclusive) for y in excexc_by_target.get(x["id"], []))

    def exc_applies(x, target_idx) -> bool:
        if mode == "ignore_exceptions":
            return False
        if mode == "any_exception":
            return True
        if mode == "first_match" and idx[x["id"]] > target_idx:
            return False          # the first matching clause wins: a later exception is never reached
        return conds_hold(x, case, inclusive) and not blocked(x)

    tr = {"req": {}, "exc": {}, "excl": {}, "figs": {f"{k[0]}|{k[1]}": str(v) for k, v in sorted(figs.items())},
          "amend_used": sorted(set(used.values())), "fails": []}
    for x in by_kind(d2, "exc"):
        tr["exc"][x["id"]] = (conds_hold(x, case, inclusive) and not blocked(x)) if mode is None else None
    for r in by_kind(d2, "req"):
        ok = base_ok(d2, case, r, figs, inclusive)
        via = None
        if not ok:
            for x in exc_by_target.get(r["id"], []):
                if not exc_applies(x, idx[r["id"]]):
                    continue
                if x["mode"] == "waive":
                    ok, via = True, x["id"]
                    break
                if x["mode"] == "period" and r["gate"] == "time":
                    if time_ok(d2, case, int(x["n2"]), r["incl"], inclusive):
                        ok, via = True, x["id"]
                        break
        tr["req"][r["id"]] = [ok, via]
        if not ok:
            tr["fails"].append([idx[r["id"]], r["id"], GATE_CODE[r["gate"]]])
    for e in by_kind(d2, "excl"):
        app = False
        via = None
        if mode != "ignore_exceptions" and conds_hold(e, case, inclusive):
            app = True
            for x in exc_by_target.get(e["id"], []):
                if exc_applies(x, idx[e["id"]]):
                    app, via = False, x["id"]
                    break
        tr["excl"][e["id"]] = [app, via]
        if app:
            tr["fails"].append([idx[e["id"]], e["id"], "EXCL"])
    tr["fails"].sort()
    # ---- limits
    cands = []
    for c in by_kind(d2, "lim_gen"):
        cands.append((idx[c["id"]], c["id"], figs[(c["id"], "limit")]))
    for c in by_kind(d2, "lim_tab"):
        k = (c["id"], "row:" + case["cat"])
        if k in figs:
            cands.append((idx[c["id"]], c["id"], figs[k]))
    lim = None
    if len(cands) == 1:
        lim = cands[0]
    elif len(cands) > 1:
        if mode == "first_match":
            lim = min(cands)
        elif d2["prec"] == "specific":
            lim = next(x for x in cands if clause(d2, x[1])["kind"] == "lim_tab")
        elif d2["prec"] == "later":
            lim = max(cands)
        elif d2["prec"] == "lower":
            lim = min(cands, key=lambda x: (x[2], x[0]))
        elif d2["prec"] == "named":
            pn = by_kind(d2, "prec_named")
            winner = pn[0]["b"] if pn else None
            hit = [x for x in cands if x[1] == winner]
            lim = hit[0] if hit else min(cands, key=lambda x: (x[2], x[0]))
        else:
            raise ValueError(d2["prec"])
    tr["limit"] = [lim[1], lim[2]] if lim else None
    if tr["fails"]:
        tr["code"] = tr["fails"][0][2]
        tr["granted"] = 0
    else:
        amt = int(case["amount"])
        if lim is not None and amt > lim[2]:
            tr["code"], tr["granted"] = "PARTIAL", lim[2]
        else:
            tr["code"], tr["granted"] = "FULL", amt
    tr["n_fails"] = len(tr["fails"])
    return tr


def components(tr: dict) -> tuple:
    """What a shortcut can change (SPEC: a solver abstains when its misapplication changes nothing)."""
    return (tuple(sorted((k, tuple(v)) for k, v in tr["req"].items())),
            tuple(sorted((k, tuple(v)) for k, v in tr["excl"].items())),
            tuple(tr["limit"] or ()), tr["code"], tr["granted"])


def decide(doc: dict, case: dict) -> tuple:
    """(code, trace) for the document as written; UNDEFINED when two refusal grounds apply (SPEC 8.3)."""
    tr = evaluate(doc, case)
    if tr["n_fails"] >= 2:
        return mv.UNDEFINED, tr
    return tr["code"], tr


def shortcut_traces(doc: dict, case: dict, true_tr: dict | None = None) -> dict:
    """{mode: trace or None}. A solver abstains (None) when its misreading does not change the result of the item
    (the outcome code and the amount granted); otherwise it answers from its own trace. Callers that ask about the
    outcome only treat a solver whose code equals the true code as abstaining too."""
    true_tr = true_tr or evaluate(doc, case)
    out = {}
    for m in MODES:
        t = evaluate(doc, case, m)
        out[m] = None if (t["code"], t["granted"]) == (true_tr["code"], true_tr["granted"]) else t
    return out


def pivotal(doc: dict, case: dict, mode: str | None = None) -> list[str]:
    """Candidate clauses whose deletion changes the outcome code (the rest of the document applied as written)."""
    code = evaluate(doc, case, mode)["code"]
    return [c["id"] for c in doc["clauses"] if c["kind"] in CANDIDATE_KINDS
            and evaluate(doc, case, mode, drop=frozenset([c["id"]]))["code"] != code]


# ================================================================================================ classification
def _near(x: dict, case: dict) -> bool:
    """A near miss: two or more atoms and exactly one false, or a single amount atom one step off its figure."""
    ats = atoms_of(x)
    vals = [atom_true(a, case) for a in ats]
    if len(ats) >= 2:
        return sum(1 for v in vals if not v) == 1
    if len(ats) == 1 and ats[0]["t"] == "amt" and not vals[0]:
        return atom_true(ats[0], case, inclusive=True) or abs(F(case["amount"]) - F(ats[0]["value"])) <= 1
    return False


def groups(doc: dict, case: dict, tr: dict | None = None) -> dict:
    """Exception groups present (SPEC 4.6): deny_allow (the default denies, an exception allows), allow_deny (the
    default allows, an exclusion or an exception-to-exception denies), near_miss (an exception or exclusion that
    nearly applies). Returns {group: [clause ids]}."""
    tr = tr or evaluate(doc, case)
    figs, _ = figures(doc, case)
    out = {"deny_allow": [], "allow_deny": [], "near_miss": []}
    excexc_t = {}
    for y in by_kind(doc, "excexc"):
        excexc_t.setdefault(y["target"], []).append(y)
    for r in by_kind(doc, "req"):
        if base_ok(doc, case, r, figs):
            continue
        for x in by_kind(doc, "exc"):
            if x["target"] != r["id"]:
                continue
            if conds_hold(x, case):
                if any(conds_hold(y, case) for y in excexc_t.get(x["id"], [])):
                    out["allow_deny"].append(x["id"])
                elif x["mode"] == "waive" or time_ok(doc, case, int(x["n2"]), r["incl"]):
                    out["deny_allow"].append(x["id"])
                else:
                    out["near_miss"].append(x["id"])   # a period exception that applies but does not save the case
            elif _near(x, case):
                out["near_miss"].append(x["id"])
    for e in by_kind(doc, "excl"):
        if conds_hold(e, case):
            ex = [x for x in by_kind(doc, "exc") if x["target"] == e["id"]]
            if any(conds_hold(x, case) and not any(conds_hold(y, case) for y in excexc_t.get(x["id"], []))
                   for x in ex):
                out["deny_allow"].append(e["id"])
            else:
                out["allow_deny"].append(e["id"])
                out["near_miss"] += [x["id"] for x in ex if _near(x, case)]
        elif _near(e, case):
            out["near_miss"].append(e["id"])
    return {k: v for k, v in out.items() if v}


def primary_group(gs: dict) -> str | None:
    for g in ("deny_allow", "allow_deny", "near_miss"):
        if g in gs:
            return g
    return None


def steps(doc: dict, case: dict, tr: dict) -> int:
    """Reasoning steps on the deciding path (SPEC knob 1-5): the deciding clause, a definition hop, amendments in
    force on a deciding figure, exceptions / exclusions / exceptions-to-exceptions in play, a precedence choice and
    business-day counting."""
    n = 1
    gs = groups(doc, case, tr)
    n += min(2, sum(len(v) for v in gs.values()))
    if any(by_kind(doc, "excexc")) and "allow_deny" in gs and any(clause(doc, c)["kind"] == "exc"
                                                                   for c in gs["allow_deny"]):
        n += 1
    if tr["amend_used"]:
        n += 1
    if tr["fails"]:
        r = clause(doc, tr["fails"][0][1])
        if r["kind"] == "req" and r.get("via"):
            n += 1
        if r["kind"] == "req" and r["gate"] == "time" and doc["count"] == "business":
            n += 1
    elif tr["limit"] and len(by_kind(doc, "lim_gen") + [c for c in by_kind(doc, "lim_tab")
                                                         if any(k == case["cat"] for k, _ in c["rows"])]) > 1:
        n += 1
    return max(1, min(5, n))


# ================================================================================================ sampler
class Plan(dict):
    """The target of one latent: code, group, mechanisms and size (see sample_doc)."""


def _rng_choice_w(rng, items: list, weights: list):
    t = rng.random() * sum(weights)
    for x, w in zip(items, weights):
        t -= w
        if t <= 0:
            return x
    return items[-1]


# R2 (1 Oct): document families whose eligibility quantity cannot be 0 (a consignment of 0 kg, an event for 0 people,
# a walk of 0 miles); the sampler and the contrast flips keep it at one step or more
POSITIVE_ELIG = frozenset({"shipping_tariff", "municipal_fee", "school_transport"})


def _step(sk) -> Fraction:
    return F(sk["elig"]["step"])


def _round_to(x: Fraction, step: Fraction) -> Fraction:
    return (x / step).__floor__() * step


def _elig_value(rng, sk, op: str, thr: Fraction, want_pass: bool, boundary: str | None) -> Fraction:
    st = _step(sk)
    lo, hi = F(sk["elig"]["rng"][0]), F(sk["elig"]["rng"][1])
    mx = sk["elig"]["dir"] == "max"
    if boundary == "exact":
        return thr
    if boundary == "off1":
        if mx:
            return thr - st if want_pass else thr + st
        return thr + st if want_pass else thr - st
    span = max(st * 3, (hi - lo) / 3)
    k = _round_to(F(rng.uniform(0.15, 1.0)) * span, st) + st * 2
    if mx:
        v = thr - k if want_pass else thr + k
    else:
        v = thr + k if want_pass else thr - k
    return max(st if sk.get("key") in POSITIVE_ELIG else F(0), v)


def _thr(rng, sk) -> Fraction:
    lo, hi = F(sk["elig"]["rng"][0]), F(sk["elig"]["rng"][1])
    st = _step(sk)
    steps_n = int((hi - lo) / st)
    x = lo + st * rng.randint(0, steps_n)
    if st == 1 and x >= 50:
        x = F(int(x) // 10 * 10)
    return x


def _amt_step(sk) -> int:
    return int(sk["amount"][2])


def _rand_amount(rng, sk) -> int:
    lo, hi, st = sk["amount"]
    return rng.randrange(lo, hi + 1, st)


def _rand_limit(rng, sk) -> int:
    lo, hi, st = sk["limit"]
    return rng.randrange(lo, hi + 1, st)


def _date_in(rng, lo: str, hi: str) -> dt.date:
    a, b = D(lo), D(hi)
    return a + dt.timedelta(days=rng.randint(0, (b - a).days))


def _flag_names(sk, role) -> list[str]:
    return [k for k, v in sk["flags"].items() if v["role"] == role]


class Builder:
    """Builds (doc, case) proposals for plans. The caller evaluates every proposal and keeps it only when the outcome
    code and the exception group are the planned ones (classification is re-derived, never assumed).

    plan keys: code (CODES), group (None | deny_allow | allow_deny | near_miss), rescue (gate an exception saves, for
    deny_allow), amend (None | in_force | not_yet | withdrawn | superseded), boundary (None | exact | off1) and
    boundary_gate (elig | time | amount), business (bool), defn (bool), prec_case (bool: both limits apply), prec
    (specific | later | lower | named), missing (None | decisive | irrelevant), n_distract (int), decoy (bool)."""

    def __init__(self, rng, pool: mv.NamePool):
        self.rng, self.pool = rng, pool
        self.n = 0

    def cid(self) -> str:
        self.n += 1
        return f"k{self.n:02d}"

    def sample(self, skin_key: str, style: str, plan: dict) -> tuple[dict, dict]:
        rng, pool = self.rng, self.pool
        self.n = 0
        sk = SK.skin(skin_key)
        code, grp = plan["code"], plan.get("group")
        focus = CODE_GATE.get(code)
        cats = [c[0] for c in sk["cats"]]
        place, org = pool.stem(rng), pool.org(rng)
        doc = {"skin": skin_key, "style": style, "place": place, "org": org,
               "count": "business" if plan.get("business") else "calendar", "holidays": [],
               "prec": plan.get("prec") or rng.choice(["specific", "later", "lower"]),
               "dstyle": plan.get("dstyle") or rng.choice(["iso", "long", "us"]), "clauses": [], "version": None,
               "phr": plan.get("phr") or "tr"}
        name = pool.person(rng)
        case = {"ref": pool.ident(rng, rng.choice("WRAKT"), 7), "name": name, "cat": rng.choice(cats),
                "type": sk["types"][0], "elig": None, "event": None, "request": None, "docs": True,
                "flags": {f: False for f in sk["flags"]}, "amount": _rand_amount(rng, sk), "record": None,
                "decoy": None}
        # ---------------------------------------------------------------- which gates fail before exceptions
        fail_base = {focus} if focus else set()
        rescue = None
        if grp == "deny_allow":
            rescue = plan.get("rescue") or rng.choice(
                ["elig", "time", "docs", "excl"] if code in SK.GRANTS else
                [g for g in ("elig", "time", "docs", "excl") if g != focus])
            if rescue != "excl":
                fail_base.add(rescue)
        bnd, bgate = plan.get("boundary"), plan.get("boundary_gate")
        # ---------------------------------------------------------------- elig gate (effective figure first)
        mx = sk["elig"]["dir"] == "max"
        thr = _thr(rng, sk)
        el_pass = "elig" not in fail_base
        op_incl = rng.random() < 0.5
        if bnd == "exact" and bgate == "elig":
            op_incl = el_pass
        el_op = ("le" if op_incl else "lt") if mx else ("ge" if op_incl else "gt")
        case["elig"] = str(_elig_value(rng, sk, el_op, thr, el_pass, bnd if bgate == "elig" else None))
        # ---------------------------------------------------------------- time gate
        n = rng.randint(*sk["time"]["rng"])
        incl = rng.random() < 0.5
        tm_pass = "time" not in fail_base
        if bnd == "exact" and bgate == "time":
            incl = tm_pass
        ev = _date_in(rng, "2026-01-20", "2026-11-20")
        case["event"] = iso(ev)
        if doc["count"] == "business":
            doc["holidays"] = self._holidays(rng, ev, n, sk["time"]["dir"])
        case["request"] = iso(self._request_date(doc, case, sk, n, incl, tm_pass, bnd if bgate == "time" else None))
        # ---------------------------------------------------------------- docs gate
        dc_pass = "docs" not in fail_base
        if plan.get("missing") and not dc_pass:
            case["docs"] = None
        else:
            case["docs"] = bool(dc_pass)
        # ---------------------------------------------------------------- clauses: general part
        G = [{"id": self.cid(), "kind": "i_days"}]
        if doc["count"] == "business":
            G.append({"id": self.cid(), "kind": "i_hol"})
        G += [{"id": self.cid(), "kind": k} for k in ("i_exc", "i_amend", "i_order", "i_missing")]
        if doc["prec"] != "named":
            G.append({"id": self.cid(), "kind": "i_prec"})
        R = [{"id": self.cid(), "kind": "entitle"}]
        dfn = None
        if plan.get("defn"):
            dfn = {"id": self.cid(), "kind": "defn", "gate": "elig", "op": el_op, "value": str(thr)}
            r_el = {"id": self.cid(), "kind": "req", "gate": "elig", "via": dfn["id"]}
        else:
            r_el = {"id": self.cid(), "kind": "req", "gate": "elig", "op": el_op, "value": str(thr), "via": None}
        r_tm = {"id": self.cid(), "kind": "req", "gate": "time", "n": n, "incl": incl}
        r_dc = {"id": self.cid(), "kind": "req", "gate": "docs"}
        reqs = [r_el, r_tm, r_dc]
        rng.shuffle(reqs)
        R += reqs
        gate_req = {"elig": r_el, "time": r_tm, "docs": r_dc}
        # ---------------------------------------------------------------- limits
        want_prec = bool(plan.get("prec_case"))
        has_gen = want_prec or rng.random() < 0.7
        has_tab = want_prec or not has_gen or rng.random() < 0.75
        lim_gen = {"id": self.cid(), "kind": "lim_gen", "limit": _rand_limit(rng, sk)} if has_gen else None
        lim_tab = None
        if has_tab:
            order_c = list(cats)
            rng.shuffle(order_c)
            chosen = order_c[:rng.randint(2, len(cats))]
            if want_prec and case["cat"] not in chosen:
                chosen[0] = case["cat"]
            elif not want_prec and case["cat"] in chosen and len(chosen) > 2 and rng.random() < 0.3:
                chosen.remove(case["cat"])
            lim_tab = {"id": self.cid(), "kind": "lim_tab", "rows": [[c, _rand_limit(rng, sk)] for c in cats
                                                                      if c in chosen]}
        if want_prec and lim_gen and lim_tab:
            row = next(r for r in lim_tab["rows"] if r[0] == case["cat"])
            while abs(row[1] - lim_gen["limit"]) < 2 * _amt_step(sk):
                row[1] = _rand_limit(rng, sk)
        grant = {"id": self.cid(), "kind": "grant"}
        prec_named = None
        if doc["prec"] == "named":
            if lim_gen and lim_tab:
                a, b = (lim_gen, lim_tab) if rng.random() < 0.5 else (lim_tab, lim_gen)
                prec_named = {"id": self.cid(), "kind": "prec_named", "a": a["id"], "b": b["id"]}
            else:
                doc["prec"] = rng.choice(["specific", "later", "lower"])
                G.append({"id": self.cid(), "kind": "i_prec"})
        L = [x for x in (lim_gen, lim_tab) if x]
        rng.shuffle(L)
        L += [grant] + ([prec_named] if prec_named else [])
        doc["clauses"] = G + ([dfn] if dfn else []) + R + L     # provisional order (needed by evaluate)
        # ---------------------------------------------------------------- amendments of the deciding figure
        amends = self._gate_amendments(rng, doc, case, sk, plan, gate_req, focus)
        doc["clauses"] += amends
        # ---------------------------------------------------------------- grant amount against the effective limit
        if code in SK.GRANTS:
            self._fit_amount(rng, doc, case, sk, plan)
            amends2 = self._limit_amendments(rng, doc, case, sk, plan, lim_gen, lim_tab, len(amends))
            doc["clauses"] += amends2
            amends += amends2
        # ---------------------------------------------------------------- exceptions, exclusions
        exc_flags = _flag_names(sk, "exc")
        ee_flag = _flag_names(sk, "excexc")[0]
        excl_flags = _flag_names(sk, "excl")
        rng.shuffle(excl_flags)
        used = set()
        E, X = [], []          # exclusions, exceptions (+ exceptions to exceptions)
        e1 = {"id": self.cid(), "kind": "excl", "cats": [], "conds": [{"t": "flag", "f": excl_flags[0]}]}
        E.append(e1)
        if rng.random() < 0.5:
            E.append({"id": self.cid(), "kind": "excl", "cats": [], "conds": [{"t": "flag", "f": excl_flags[1]}]})
        if rescue in ("elig", "time", "docs"):
            r = gate_req[rescue]
            mode = "period" if rescue == "time" and rng.random() < 0.5 else "waive"
            x = self._exc(sk, case, cats, r, exc_flags, used, "true", gate=rescue, mode=mode)
            if mode == "period":
                x["n2"] = self._period_n2(doc, case, sk, r)
                if x["n2"] is None:
                    x["mode"] = "waive"
                    x.pop("n2")
            X.append(x)
        if rescue == "excl":
            case["flags"][excl_flags[0]] = True
            X.append(self._exc(sk, case, cats, e1, exc_flags, used, "true"))
        if code == "EXCL":
            case["flags"][excl_flags[0]] = True
            if rng.random() < 0.4:
                x = self._exc(sk, case, cats, e1, exc_flags, used, "true")
                X.append(x)
                case["flags"][ee_flag] = True
                X.append({"id": self.cid(), "kind": "excexc", "target": x["id"], "cats": [],
                          "conds": [{"t": "flag", "f": ee_flag}]})
        if focus and grp == "near_miss":
            r = gate_req[focus]
            mode = "period" if focus == "time" and rng.random() < 0.4 else "waive"
            x = self._exc(sk, case, cats, r, exc_flags, used, "near", gate=focus, mode=mode)
            if mode == "period":
                n2 = self._period_n2(doc, case, sk, r)
                if n2 is None:
                    x["mode"] = "waive"
                else:
                    x["n2"] = n2
            X.append(x)
        if focus and grp == "allow_deny":
            r = gate_req[focus]
            x = self._exc(sk, case, cats, r, exc_flags, used, "true", gate=focus)
            X.append(x)
            case["flags"][ee_flag] = True
            X.append({"id": self.cid(), "kind": "excexc", "target": x["id"], "cats": [],
                      "conds": [{"t": "flag", "f": ee_flag}]})
        if code in SK.GRANTS and grp == "near_miss":
            fl = e1["conds"][0]["f"]
            others = [c for c in cats if c != case["cat"]]
            if rng.random() < 0.5:
                case["flags"][fl] = True
                e1["cats"] = sorted(rng.sample(others, rng.randint(1, 2)))
            else:
                e1["cats"] = sorted({case["cat"]} | set(rng.sample(others, 1)))
        # ---------------------------------------------------------------- distractors
        D_ = self._distractors(rng, sk, case, cats, gate_req, exc_flags, ee_flag, fail_base,
                               int(plan.get("n_distract", 4)), {a["f"] for e in E for a in e["conds"]},
                               ho=doc["phr"] == "ho")
        D_ += self._repealed(rng, sk, case, cats, int(plan.get("n_repealed", 0)), r_el, r_tm, lim_gen,
                             {a["f"] for e in E for a in e["conds"]})
        # ---------------------------------------------------------------- final order
        sec_x = X + [d for d in D_ if d["kind"] in ("exc", "excexc")]
        rng.shuffle(sec_x)
        # an exception to an exception comes after the exception it names
        pos = {c["id"]: i for i, c in enumerate(sec_x)}
        sec_x.sort(key=lambda c: (pos[c["target"]] + 0.5) if c["kind"] == "excexc" and c["target"] in pos
                   else pos[c["id"]])
        sec_e = E + [d for d in D_ if d["kind"] == "excl"]
        rng.shuffle(sec_e)
        procs = [d for d in D_ if d["kind"] in ("proc", "udef", "scoped", "repealed") or
                 (d["kind"] == "req" and d.get("scope_type"))]
        rng.shuffle(procs)
        k_early = rng.randint(0, len(procs))
        early, late = procs[:k_early], procs[k_early:]
        body = {"x": sec_x, "e": sec_e, "l": L}
        order = rng.choice([("x", "e", "l"), ("e", "x", "l"), ("x", "l", "e")])
        secname = {"x": "exceptions", "e": "exclusions", "l": "limits"}
        early_g = [d for d in early if d["kind"] == "udef"]
        early_r = [d for d in early if d["kind"] != "udef"]
        for c in G + early_g + ([dfn] if dfn else []):
            c["sec"] = "general"
        for c in R + early_r:
            c["sec"] = "requirements"
        clauses = G + early_g + ([dfn] if dfn else []) + R + early_r
        for o in order:
            for c in body[o]:
                c["sec"] = secname[o]
            clauses += body[o]
        for c in late:
            c["sec"] = "other"
        # amendments: numbered in the order they come into force
        amends.sort(key=lambda a: (a["eff"], a["k"]))
        for i, a in enumerate(amends, 1):
            a["k"] = i
            a["sec"] = "amendments"
        clauses += late + amends
        doc["clauses"] = clauses
        doc["n_early"] = len(early)
        # ---------------------------------------------------------------- decoy file, dates of the document
        if plan.get("decoy"):
            other = [c for c in cats if c != case["cat"]]
            v2 = _elig_value(rng, sk, el_op, thr, not el_pass, None)
            case["decoy"] = {"ref": mv.decoy_id(case["ref"], rng), "name": f"{pool.first_name(rng)} "
                             f"{name.split()[-1]}", "cat": rng.choice(other), "elig": str(v2)}
        case["proc"] = iso(max(D(case["event"]), D(case["request"])) + dt.timedelta(days=rng.randint(20, 40)))
        first_eff = min([D(a["eff"]) for a in amends] + [D(case["request"])])
        doc["version"] = iso(first_eff - dt.timedelta(days=rng.randint(30, 200)))
        doc["title"] = sk["title"].format(place=place, org=org)
        doc["issuer"] = sk["issuer"].format(place=place, org=org)
        return doc, case

    # ------------------------------------------------------------------------------------------ dates
    def _holidays(self, rng, ev: dt.date, n: int, direction: str) -> list[str]:
        span = int(n * 1.6) + 6
        out = set()
        for _ in range(rng.randint(2, 4)):
            off = rng.randint(1, span)
            d = ev + dt.timedelta(days=off if direction == "after" else -off)
            while d.weekday() >= 5:
                d += dt.timedelta(days=1)
            out.add(iso(d))
        return sorted(out)

    def _request_date(self, doc, case, sk, n, incl, want_pass, boundary) -> dt.date:
        rng = self.rng
        dl = deadline(doc, case, n, sk["time"]["dir"])
        if boundary == "exact":
            return dl
        if boundary == "off1":
            return dl - dt.timedelta(days=1) if want_pass else dl + dt.timedelta(days=1)
        k = rng.randint(2, max(2, min(12, n - 1)))
        return dl - dt.timedelta(days=k) if want_pass else dl + dt.timedelta(days=k)

    def _period_n2(self, doc, case, sk, r):
        """A replacement period that saves the time requirement r for this case (None if none is found)."""
        rng = self.rng
        for _ in range(40):
            if sk["time"]["dir"] == "after":
                n2 = r["n"] + rng.randint(2, 25)
            else:
                n2 = r["n"] - rng.randint(1, max(1, r["n"] - 1))
            if n2 >= 1 and n2 != r["n"] and time_ok(doc, case, n2, r["incl"]):
                return n2
        return None

    # ------------------------------------------------------------------------------------------ exceptions
    def _exc(self, sk, case, cats, target, exc_flags, used, how: str, gate=None, mode="waive") -> dict:
        """An exception to `target` whose atoms all hold (how=true) or with exactly one atom false (how=near)."""
        rng = self.rng
        free = [f for f in exc_flags if f not in used] or list(exc_flags)
        fl = rng.choice(free)
        used.add(fl)
        shapes = ["cat_flag", "flag", "cat_flag", "flag_flag"] + (["flag_amt", "cat_amt"] if gate == "docs" else [])
        shape = rng.choice(shapes)
        if how == "near" and shape == "flag":
            shape = "cat_flag"
        atoms = (["cat"] if shape.startswith("cat") else []) + \
            ([("flag", fl)] if "flag" in shape else []) + (["amt"] if shape.endswith("amt") else [])
        if shape == "flag_flag":
            free2 = [f for f in exc_flags if f not in used]
            if free2:
                f2 = rng.choice(free2)
                used.add(f2)
                atoms.append(("flag", f2))
            else:
                atoms = ["cat", ("flag", fl)]
        false_at = rng.randrange(len(atoms)) if how == "near" else None
        x = {"id": self.cid(), "kind": "exc", "target": target["id"], "cats": [], "conds": [], "mode": mode}
        st = _amt_step(sk)
        for i, a in enumerate(atoms):
            want = i != false_at
            others = [c for c in cats if c != case["cat"]]
            if a == "cat":
                x["cats"] = sorted({case["cat"]} | set(rng.sample(others, rng.randint(0, 1)))) if want else \
                    sorted(rng.sample(others, rng.randint(1, 2)))
            elif a == "amt":
                amt = int(case["amount"])
                if want:
                    val = amt + st * rng.randint(0, 25)
                    op = "le" if val == amt else rng.choice(["le", "lt"])
                else:
                    val = amt - st * (1 if rng.random() < 0.5 else rng.randint(2, 25))
                    if val <= 0:
                        val, op = amt, "lt"
                    else:
                        op = rng.choice(["le", "lt"])
                x["conds"].append({"t": "amt", "op": op, "value": int(val)})
            else:
                case["flags"][a[1]] = want
                x["conds"].append({"t": "flag", "f": a[1]})
        return x

    def _repealed(self, rng, sk, case, cats, k, r_el, r_tm, lim_gen, excl_used) -> list:
        """Superseded provisions kept for reference (SPEC 5 F1 distractors): a former requirement, limit or exclusion
        with another figure or condition, repealed before the request was received. They never apply."""
        out = []
        req = D(case["request"])
        kinds = ["elig", "time", "lim", "excl"]
        rng.shuffle(kinds)
        excl_free = [f for f in _flag_names(sk, "excl") if f not in excl_used]
        for i in range(k):
            kd = kinds[i % len(kinds)]
            date = iso(req - dt.timedelta(days=rng.randint(30, 400)))
            if kd == "elig":
                v = _thr(rng, sk)
                op = rng.choice(["le", "lt"] if sk["elig"]["dir"] == "max" else ["ge", "gt"])
                inner = {"id": "x", "kind": "req", "gate": "elig", "op": op, "value": str(v), "via": None}
            elif kd == "time":
                inner = {"id": "x", "kind": "req", "gate": "time", "n": rng.randint(*sk["time"]["rng"]),
                         "incl": rng.random() < 0.5}
            elif kd == "lim":
                inner = {"id": "x", "kind": "lim_gen", "limit": _rand_limit(rng, sk)}
            else:
                if not excl_free:
                    continue
                inner = {"id": "x", "kind": "excl", "cats": [], "conds": [{"t": "flag", "f": excl_free.pop()}]}
            out.append({"id": self.cid(), "kind": "repealed", "date": date, "inner": inner})
        return out

    def _distractors(self, rng, sk, case, cats, gate_req, exc_flags, ee_flag, fail_base, k, excl_used=(),
                     ho=False) -> list:
        """Clauses that never decide: procedure sentences, unused definitions, a requirement scoped to another
        request type, exceptions to requirements the case passes anyway, exclusions whose conditions are all false,
        an exception to a distractor exception."""
        out = []
        procs = list(SK.HO_TEXT[sk["key"]]["proc"] if ho else sk["proc"])
        rng.shuffle(procs)
        udefs = list(SK.HO_TEXT[sk["key"]]["udefs"] if ho else sk["unused_defs"])
        rng.shuffle(udefs)
        excl_flags = [f for f in _flag_names(sk, "excl") if not case["flags"].get(f) and f not in excl_used]
        kinds = ["proc", "proc", "udef", "scoped", "exc_pass", "exc_pass", "excl_false", "excexc_d"]
        scoped = False
        tries = 0
        while len(out) < k and tries < 6 * k + 10:
            tries += 1
            kd = rng.choice(kinds)
            if kd == "proc" and procs:
                out.append({"id": self.cid(), "kind": "proc", "text": procs.pop()})
            elif kd == "udef" and udefs:
                t, x = udefs.pop()
                out.append({"id": self.cid(), "kind": "udef", "term": t, "text": x})
            elif kd == "scoped" and not scoped:
                scoped = True
                out.append({"id": self.cid(), "kind": "req", "gate": "docs", "scope_type": sk["types"][1],
                            "docs2": sk["docs2"]})
            elif kd == "exc_pass":
                passing = [g for g in ("elig", "time", "docs") if g not in fail_base]
                if not passing:
                    continue
                r = gate_req[rng.choice(passing)]
                x = {"id": self.cid(), "kind": "exc", "target": r["id"], "mode": "waive", "cats": [],
                     "conds": [{"t": "flag", "f": rng.choice(exc_flags)}]}
                if rng.random() < 0.5:
                    x["cats"] = sorted(rng.sample(cats, rng.randint(1, 2)))
                out.append(x)
            elif kd == "excl_false" and excl_flags:
                fl = excl_flags.pop()
                e = {"id": self.cid(), "kind": "excl", "cats": [], "conds": [{"t": "flag", "f": fl}]}
                if rng.random() < 0.4:
                    e["cats"] = sorted(rng.sample([c for c in cats if c != case["cat"]], 1))
                out.append(e)
            elif kd == "excexc_d":
                tg = [x for x in out if x["kind"] == "exc"]
                if tg and not any(x["kind"] == "excexc" for x in out):
                    out.append({"id": self.cid(), "kind": "excexc", "target": rng.choice(tg)["id"], "cats": [],
                                "conds": [{"t": "flag", "f": ee_flag}]})
        return out

    # ------------------------------------------------------------------------------------------ amendments
    def _flip_figure(self, doc, case, sk, r, g, eff_value):
        """A figure for gate g's clause that gives the opposite result to eff_value for this case (candidates near
        the case's own value, so the change reads like a real revision)."""
        rng = self.rng
        figs = base_figures(doc)
        if g == "elig":
            src = r["via"] or r["id"]
            st = _step(sk)
            v = F(case["elig"])
            f2 = dict(figs)
            f2[(src, "value")] = F(eff_value)
            want = not elig_ok(doc, case, r, f2)
            cands = []
            for j in range(-15, 16):
                alt = v + st * j
                if alt <= 0 or alt == F(eff_value):
                    continue
                f2[(src, "value")] = alt
                if elig_ok(doc, case, r, f2) == want:
                    cands.append(alt)
            if st == 1:
                round_c = [a for a in cands if a % 5 == 0]
                cands = round_c or cands
            return rng.choice(cands) if cands else None
        want = not time_ok(doc, case, int(eff_value), r["incl"])
        cands = [n2 for n2 in range(1, int(eff_value) + 46) if n2 != int(eff_value)
                 and time_ok(doc, case, n2, r["incl"]) == want]
        return rng.choice(cands[:12] if want else cands[-12:]) if cands else None

    def _gate_amendments(self, rng, doc, case, sk, plan, gate_req, focus) -> list:
        """Planned amendment of a requirement figure: in_force / superseded (the written figure would give the other
        result; the amendment in force gives the planned one), not_yet / withdrawn (the written figure decides; the
        amendment would flip it). For grant codes the limit is amended later (_limit_amendments)."""
        am = plan.get("amend")
        out = []
        if not am or plan["code"] in SK.GRANTS:
            return out
        g = focus if focus in ("elig", "time") else rng.choice(["elig", "time"])
        r = gate_req[g]
        src = doc_clause = (next(c for c in doc["clauses"] if c["id"] == r["via"]) if g == "elig" and r.get("via")
                            else r)
        field = "value" if g == "elig" else "n"
        eff_v = F(src["value"]) if g == "elig" else int(src["n"])
        alt = self._flip_figure(doc, case, sk, r, g, eff_v)
        if alt is None:
            raise mv.Reject("amend", "no figure flips the gate")
        req = D(case["request"])
        if am in ("in_force", "superseded"):
            doc_clause[field] = str(alt) if g == "elig" else int(alt)
            eff = req - dt.timedelta(days=0 if rng.random() < 0.2 else rng.randint(1, 150))
            out.append({"id": self.cid(), "kind": "amend", "k": 1, "target": src["id"], "field": field,
                        "old": str(alt), "new": str(eff_v), "eff": iso(eff), "withdrawn": False})
            if am == "superseded":
                alt2 = self._flip_figure(doc, case, sk, r, g, eff_v)
                if alt2 is None or str(alt2) == str(alt):
                    raise mv.Reject("amend", "no second figure")
                out.append({"id": self.cid(), "kind": "amend", "k": 2, "target": src["id"], "field": field,
                            "old": str(eff_v), "new": str(alt2),
                            "eff": iso(req + dt.timedelta(days=rng.randint(1, 60))), "withdrawn": False})
        else:
            eff = req + dt.timedelta(days=rng.randint(1, 90)) if am == "not_yet" else \
                req - dt.timedelta(days=rng.randint(-30, 90))
            out.append({"id": self.cid(), "kind": "amend", "k": 1, "target": src["id"], "field": field,
                        "old": str(eff_v), "new": str(alt), "eff": iso(eff), "withdrawn": am == "withdrawn"})
        return out

    def _fit_amount(self, rng, doc, case, sk, plan):
        """Grant codes: the requested amount against the limit that applies (boundary: exactly at the limit, or one
        step over it)."""
        st = _amt_step(sk)
        tr = evaluate(doc, case)
        lim = tr["limit"]
        bnd = plan.get("boundary") == "exact" and plan.get("boundary_gate") == "amount"
        off1 = plan.get("boundary") == "off1" and plan.get("boundary_gate") == "amount"
        if lim is None:
            if plan["code"] == "PARTIAL":
                raise mv.Reject("no_limit", "PARTIAL needs a limit")
            return
        L = int(lim[1])
        if plan["code"] == "PARTIAL":
            case["amount"] = L + st if (bnd or off1) else L + st * rng.randint(2, 40)
        else:
            case["amount"] = L if bnd else (L - st if off1 else max(st, L - st * rng.randint(2, 40)))

    def _limit_amendments(self, rng, doc, case, sk, plan, lim_gen, lim_tab, k0) -> list:
        am = plan.get("amend")
        out = []
        tr = evaluate(doc, case)
        if am and tr["limit"]:
            cid, L = tr["limit"]
            c = clause(doc, cid)
            field = "limit" if c["kind"] == "lim_gen" else "row:" + case["cat"]
            amt = int(case["amount"])
            lo, hi, st = sk["limit"]
            # a figure on the other side of the requested amount (so the amendment decides PARTIAL vs FULL)
            pool_alt = [v for v in range(lo, hi + 1, st) if (amt > v) != (amt > L) and v != L]
            if not pool_alt:
                raise mv.Reject("amend", "no limit figure flips the outcome")
            alt = rng.choice(pool_alt)
            req = D(case["request"])

            def set_written(v):
                if field == "limit":
                    c["limit"] = int(v)
                else:
                    for row in c["rows"]:
                        if row[0] == case["cat"]:
                            row[1] = int(v)
            if am in ("in_force", "superseded"):
                set_written(alt)
                out.append({"id": self.cid(), "kind": "amend", "k": k0 + 1, "target": cid, "field": field,
                            "old": str(alt), "new": str(L),
                            "eff": iso(req - dt.timedelta(days=0 if rng.random() < 0.2 else rng.randint(1, 150))),
                            "withdrawn": False})
                if am == "superseded":
                    alt2 = rng.choice([v for v in pool_alt if v != alt] or pool_alt)
                    out.append({"id": self.cid(), "kind": "amend", "k": k0 + 2, "target": cid, "field": field,
                                "old": str(L), "new": str(alt2),
                                "eff": iso(req + dt.timedelta(days=rng.randint(1, 60))), "withdrawn": False})
            else:
                out.append({"id": self.cid(), "kind": "amend", "k": k0 + 1, "target": cid, "field": field,
                            "old": str(L), "new": str(alt),
                            "eff": iso(req + dt.timedelta(days=rng.randint(1, 90)) if am == "not_yet" else
                                       req - dt.timedelta(days=rng.randint(-30, 90))),
                            "withdrawn": am == "withdrawn"})
        # distractor: an amendment of another category's row (in force), 30%
        if lim_tab and rng.random() < 0.3:
            others = [(c_, v) for c_, v in lim_tab["rows"] if c_ != case["cat"]]
            if others:
                c_, v = rng.choice(others)
                lo, hi, st = sk["limit"]
                new = rng.choice([x for x in range(lo, hi + 1, st) if x != v])
                out.append({"id": self.cid(), "kind": "amend", "k": k0 + len(out) + 1, "target": lim_tab["id"],
                            "field": "row:" + c_, "old": str(v), "new": str(new),
                            "eff": iso(D(case["request"]) - dt.timedelta(days=rng.randint(5, 200))),
                            "withdrawn": False})
        return out
