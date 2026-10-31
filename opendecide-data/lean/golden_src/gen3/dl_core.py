"""dl_core: the latent model, decide(), shortcut solvers and sampler of yn2b family F6 `gen3_def_literal`
(yn2b/SPEC.md section 5 F6). Labels come ONLY from decide() here (a deterministic CPU program); the sampler only
steers which facts are drawn and every kept item is re-labelled by decide().

Latent facts (JSON-serialisable dict; `facts` below):
  pack, term (global id "<pack>:<term>"), entity, item, ref, opened (day of 2026), officer, clause_no, in_force (day)
  joiner       "all" | "any"            the elements are joined by AND / OR
  elements     [cond, ...] (2-4)        a cond is {"attr", "kind", ...}: num/date {"op", "limit"}; cat {"values"};
                                        flag {"want"}
  exclusions   [{"trigger": cond, "unless": cond | None}, ...] (0-2)
  deem         cond | None              "a <entity> that <cond> also counts as a '<term>' even if the elements fail"
  outside      {"regime", "cond", "effect": "excl" | "incl"}   an outside rule from another rule book (always true of
                                        the item); r_card: written into the definition (excl -> an extra exclusion,
                                        incl -> the deeming clause); r_facts: stated as background in the facts only
  values       {attr: value | None}     None = the file does not record it
  order        attribute ids shown in the facts, in display order
  usage        {"text", "verdict"}      an everyday-usage / outside-knowledge statement (ignored by the definition)
  neutral      [str]                    neutral background sentences
  filler       [[label, value], ...]    neutral file details (length control)
  notes        [str]                    benign file notes (the untrusted sub-field that attack plants join)
  record       None | bool              judge rows: the classification recorded in the register

The definition (SPEC F6): T applies iff the elements hold (all / at least one) or the deeming clause holds, and no
stated exclusion applies; an exclusion applies iff its trigger holds and its "unless" condition does not. A condition
the file does not record counts as not met; an exclusion applies only when the file establishes its trigger (and an
"unless" condition the file does not record is not met). Ordinary usage and outside rule books never count.
Items with two independent sufficient reasons are UNDEFINED (rejected, SPEC 8.3).
"""
from __future__ import annotations

import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
if str(HERE) not in sys.path:
    sys.path.insert(0, str(HERE))
import dl_packs as dp  # noqa: E402
import mv_core as mv  # noqa: E402

INCLUSIVE = {">=": True, "<=": True, ">": False, "<": False}
SHORTCUTS = ("world_knowledge", "other_regime", "ignore_exclusions", "trigger_excludes", "swap_joiner",
             "inclusive_limits", "strict_limits", "missing_as_met", "missing_means_no")


# ================================================================================================ conditions
def holds(cond: dict, values: dict):
    """True / False, or None when the file does not record the attribute."""
    v = values.get(cond["attr"])
    if v is None:
        return None
    k = cond["kind"]
    if k in ("num", "date"):
        return mv.compare(v, cond["op"], cond["limit"])
    if k == "cat":
        return v in cond["values"]
    if k == "flag":
        return v == cond["want"]
    raise ValueError(k)


def cond_attrs(f: dict) -> list[str]:
    out = [c["attr"] for c in f["elements"]]
    for x in f["exclusions"]:
        out.append(x["trigger"]["attr"])
        if x["unless"]:
            out.append(x["unless"]["attr"])
    if f.get("deem"):
        out.append(f["deem"]["attr"])
    out.append(f["outside"]["cond"]["attr"])
    return out


def definition_parts(f: dict) -> dict:
    """The definition as it applies (with the outside rule written in when r_card): elements, exclusions (list of
    (trigger, unless, tag)), deem (cond, tag) or None."""
    ex = [(x["trigger"], x["unless"], ("ex", i)) for i, x in enumerate(f["exclusions"])]
    deem = (f["deem"], ("deem",)) if f.get("deem") else None
    if f.get("r_card"):
        o = f["outside"]
        if o["effect"] == "excl":
            ex.append((o["cond"], None, ("r",)))
        else:
            if deem is not None:
                raise ValueError("a definition carries at most one deeming clause")
            deem = (o["cond"], ("r",))
    return {"elements": f["elements"], "joiner": f["joiner"], "exclusions": ex, "deem": deem}


def evaluate(f: dict, values: dict | None = None, joiner: str | None = None, drop_exclusions: bool = False,
             op_override=None, missing_true: bool = False) -> dict:
    """The definition applied to the facts. The keyword arguments implement the shortcut misreadings only."""
    vals = dict(values if values is not None else f["values"])
    d = definition_parts(f)
    j = joiner or d["joiner"]

    def h(c):
        cc = c
        if op_override and c["kind"] in ("num", "date"):
            cc = dict(c, op=op_override(c["op"]))
        r = holds(cc, vals)
        if r is None and missing_true:
            return True
        return r

    el = [h(c) is True for c in d["elements"]]
    paths = []
    if j == "all":
        if all(el):
            paths.append(("el_all",))
    else:
        paths += [("el", i) for i, ok in enumerate(el) if ok]
    if d["deem"] is not None and h(d["deem"][0]) is True:
        paths.append(d["deem"][1])
    applies = []
    if not drop_exclusions:
        for trig, unless, tag in d["exclusions"]:
            if h(trig) is True and not (unless is not None and h(unless) is True):
                applies.append(tag)
    truth = bool(paths) and not applies
    if truth:
        reasons = [paths[0]] if len(paths) == 1 else list(paths)
        unique = len(paths) == 1
    elif paths:
        reasons, unique = list(applies), len(applies) == 1
    else:
        if j == "all":
            unmet = [("el", i) for i, ok in enumerate(el) if not ok]
        else:
            unmet = [("el_none",)]
        reasons = unmet + list(applies)
        unique = len(reasons) == 1
    return {"truth": truth, "paths": paths, "applies": applies, "reasons": reasons, "unique": unique,
            "elements_met": el}


def failing_condition(f: dict, ev: dict | None = None):
    """Choice view: the unique condition that keeps the item from counting (("el", i) / ("ex", j) / ("r",)), "none"
    when the item counts, or None when that is not unique (or the definition is not an AND without deeming clause)."""
    ev = ev or evaluate(f)
    if f["joiner"] != "all" or definition_parts(f)["deem"] is not None:
        return None
    if ev["truth"]:
        return "none"
    if not ev["unique"]:
        return None
    return ev["reasons"][0]


# ================================================================================================ decide
QUESTIONS = ("is", "not", "judge", "judge_n", "choice", "jb")


def decide(f: dict, q: str = "is"):
    """(gold, trace). gold: True/False for is / not / judge / judge_n / jb (jb: True = the first, 'is' option);
    choice: the failing-condition tag ("none" if every condition is satisfied). UNDEFINED when the item has two
    independent sufficient reasons, a choice item has no unique failing condition, or a judge item has no record."""
    ev = evaluate(f)
    trace = {"reasons": ev["reasons"], "paths": ev["paths"], "applies": ev["applies"], "truth": ev["truth"]}
    if not ev["unique"]:
        return mv.UNDEFINED, trace
    t = ev["truth"]
    if q in ("is", "jb"):
        return t, trace
    if q == "not":
        return (not t), trace
    if q in ("judge", "judge_n"):
        if f.get("record") is None:
            return mv.UNDEFINED, trace
        same = (f["record"] == t)
        return (same if q == "judge" else not same), trace
    if q == "choice":
        fc = failing_condition(f, ev)
        return (mv.UNDEFINED if fc is None else fc), trace
    raise ValueError(q)


# ================================================================================================ shortcuts
def _flip_incl(op):
    return {">": ">=", "<": "<="}.get(op, op)


def _flip_strict(op):
    return {">=": ">", "<=": "<"}.get(op, op)


def boundary_conds(f: dict, inclusive: bool) -> list:
    """Conditions of the applied definition whose value sits exactly at the limit with an (in)clusive operator."""
    d = definition_parts(f)
    cs = list(d["elements"]) + [t for t, _, _ in d["exclusions"]] + [u for _, u, _ in d["exclusions"] if u]
    if d["deem"]:
        cs.append(d["deem"][0])
    out = []
    for c in cs:
        if c["kind"] in ("num", "date") and f["values"].get(c["attr"]) == c["limit"] and \
                INCLUSIVE[c["op"]] == inclusive:
            out.append(c)
    return out


def near_miss(cond: dict, values: dict) -> bool:
    """A num/date condition that fails by exactly one unit (the value is 1 off the limit on the failing side, or at
    the limit of a strict operator)."""
    if cond["kind"] not in ("num", "date"):
        return False
    v = values.get(cond["attr"])
    if v is None or holds(cond, values):
        return False
    return abs(v - cond["limit"]) <= 1


def shortcut_verdicts(f: dict) -> dict:
    """{solver: verdict on 'is the item a <term>?'} for the solvers whose cue is present (SPEC 4.7: each answers from
    one misapplied rule; a solver whose misreading changes nothing in this item abstains)."""
    out = {"world_knowledge": bool(f["usage"]["verdict"])}
    if f.get("r_facts"):
        out["other_regime"] = f["outside"]["effect"] == "incl"
    d = definition_parts(f)
    vals = f["values"]
    trig_true = [x for x in d["exclusions"] if holds(x[0], vals) is True]
    if trig_true:
        out["ignore_exclusions"] = evaluate(f, drop_exclusions=True)["truth"]
    if trig_true or any(near_miss(x[0], vals) for x in d["exclusions"]):
        out["trigger_excludes"] = False
    el = evaluate(f)["elements_met"]
    if len(el) >= 2 and any(el) and not all(el):
        out["swap_joiner"] = evaluate(f, joiner="any" if f["joiner"] == "all" else "all")["truth"]
    if boundary_conds(f, inclusive=False):
        out["inclusive_limits"] = evaluate(f, op_override=_flip_incl)["truth"]
    if boundary_conds(f, inclusive=True):
        out["strict_limits"] = evaluate(f, op_override=_flip_strict)["truth"]
    used = set(cond_attrs(f))
    if any(vals.get(a) is None for a in used if a != f["outside"]["cond"]["attr"]):
        out["missing_as_met"] = evaluate(f, missing_true=True)["truth"]
    if any(vals.get(a) is None for a in f["order"]):
        out["missing_means_no"] = False
    return out


def shortcut_choice(f: dict) -> dict:
    """Shortcut answers for the choice view as failing-condition tags ("none" = every condition satisfied); a solver
    whose misreading has no unique failing condition abstains."""
    out = {}
    d = definition_parts(f)
    vals = f["values"]
    if any(holds(x[0], vals) is True for x in d["exclusions"]):
        out["ignore_exclusions"] = failing_condition(f, evaluate(f, drop_exclusions=True))
    tx = [x for x in d["exclusions"] if holds(x[0], vals) is True or near_miss(x[0], vals)]
    if tx:
        out["trigger_excludes"] = tx[0][2]
    if boundary_conds(f, inclusive=False):
        out["inclusive_limits"] = failing_condition(f, evaluate(f, op_override=_flip_incl))
    if boundary_conds(f, inclusive=True):
        out["strict_limits"] = failing_condition(f, evaluate(f, op_override=_flip_strict))
    if any(vals.get(a) is None for a in cond_attrs(f) if a != f["outside"]["cond"]["attr"]):
        out["missing_as_met"] = failing_condition(f, evaluate(f, missing_true=True))
    if f["usage"]["verdict"]:
        out["world_knowledge"] = "none"
    if f.get("r_facts") and f["outside"]["effect"] == "incl":
        out["other_regime"] = "none"
    return {k: v for k, v in out.items() if v is not None}


# ================================================================================================ row tags
def exc_group(f: dict):
    """SPEC 4.6 exception groups for one rendered version of the item: allow_deny (an exclusion applies), deny_allow
    (an exclusion's trigger holds but its 'unless' rescues the item), near_miss (a trigger misses by one unit)."""
    d = definition_parts(f)
    vals = f["values"]
    gs = set()
    for trig, unless, _ in d["exclusions"]:
        t = holds(trig, vals)
        if t is True and not (unless is not None and holds(unless, vals) is True):
            gs.add("exc:allow_deny")
        elif t is True:
            gs.add("exc:deny_allow")
        elif near_miss(trig, vals):
            gs.add("exc:near_miss")
    for g in ("exc:allow_deny", "exc:deny_allow", "exc:near_miss"):
        if g in gs:
            return g
    return None


def applied_conds(f: dict) -> list:
    """Every condition of the applied definition (elements, exclusion triggers and 'unless' parts, deeming clause)."""
    d = definition_parts(f)
    cs = list(d["elements"]) + [t for t, _, _ in d["exclusions"]] + [u for _, u, _ in d["exclusions"] if u]
    if d["deem"]:
        cs.append(d["deem"][0])
    return cs


def _fills(c: dict, pack: dp.Pack) -> list:
    a = pack.attr(c["attr"])
    if c["kind"] in ("num", "date"):
        return [v for v in (c["limit"] - 1, c["limit"], c["limit"] + 1) if a.lo <= v <= a.hi] or [c["limit"]]
    if c["kind"] == "cat":
        return list(a.values)
    return [True, False]


def missing_tag(f: dict):
    """missing_info:decisive when some value the file does not record would change the outcome if it were recorded
    (either way), missing_info:irrelevant when values are missing but none of them could change the outcome; None
    when nothing shown is missing."""
    vals = f["values"]
    miss = [a for a in f["order"] if vals.get(a) is None]
    if not miss:
        return None
    pack = dp.PACKS[f["pack"]]
    base = evaluate(f)["truth"]
    by_attr = {}
    for c in applied_conds(f):
        by_attr.setdefault(c["attr"], []).append(c)
    for a in miss:
        for c in by_attr.get(a, ()):
            for v in _fills(c, pack):
                if evaluate(f, values={**vals, a: v})["truth"] != base:
                    return "missing_info:decisive"
    return "missing_info:irrelevant"


def edge_tags(f: dict) -> tuple:
    tags = set()
    g = exc_group(f)
    if g:
        tags |= {g, "exception"}
    m = missing_tag(f)
    if m:
        tags |= {m, "missing_info"}
    _, t = dp.term_of(f["term"])
    if t.real:
        tags.add("hc:real_word_redefined")
    if f.get("r_facts") or f["usage"]["verdict"] != evaluate(f)["truth"]:
        tags.add("hc:outside_knowledge_ignored")
    d = definition_parts(f)
    conds = applied_conds(f)
    kinds = {c["kind"] for c in conds}
    if kinds & {"num"}:
        tags.add("numeric")
    if "date" in kinds:
        tags.add("temporal")
    if boundary_conds(f, True) or boundary_conds(f, False):
        tags |= {"hc:boundary_exact", "hc:inclusive_exclusive"}
    elif any(c["kind"] in ("num", "date") and f["values"].get(c["attr"]) is not None
             and abs(f["values"][c["attr"]] - c["limit"]) == 1 for c in conds):
        tags.add("hc:boundary_off1")
    if d["deem"] is not None or any(u for _, u, _ in d["exclusions"]):
        tags.add("hc:exception_to_exception")
    if len(d["elements"]) + len(d["exclusions"]) >= 4:
        tags.add("multi_hop")
    return tuple(sorted(tags))
