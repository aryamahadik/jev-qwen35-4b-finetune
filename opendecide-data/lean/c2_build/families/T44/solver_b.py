"""families/T44/solver_b.py: T44 solver B, written from G0_SPEC.md (not from plugin.py or world.py).

parse(row, ctx) reads the RENDERED row back to the facts: the tool-block layout of the row's register is undone by this
module's own inverse (labels found as tokens, items by pattern), then objects, start facts, goal literals and the plan
or the calls so far. Option texts are read back to keys (a verdict label, or a call).

solve_b(view) is a different paradigm from solver A (forward state simulation + BFS): BACKWARD REGRESSION.
  verdict    step k is inapplicable iff the start state does not satisfy the regression of step k's needs through
             steps k-1 ... 1 (or the regression is contradictory); the goal is reached iff the start state satisfies the
             goal regressed through the whole plan. No state is ever simulated forward past the start.
  next call  regression levels L_0 = {goal}, L_j+1 = regress(L_j, relevant calls); d = first level the current state
             satisfies; an option is a shortest-route call iff it is applicable now and the state after it satisfies a
             condition of a level below d.
Imports no solver-A code (plugin.check_independence).
"""
from __future__ import annotations

import itertools
import re

from . import texts as TX


class ParseError(ValueError):
    pass


LIT = re.compile(r"(not )?(\w+)\(([^)]*)\)")
CALL = re.compile(r"(\w+)\((.*)\)")


def _args(s: str) -> list:
    return [a.strip() for a in s.split(",")] if s.strip() else []


# ------------------------------------------------------------------------------------------------ parse
def _tools(lines: list, reg: str) -> list:
    R = TX.REGISTERS[reg]
    pre = re.escape(R["prefix"]).replace(re.escape("{i}"), r"\d+")
    entries, cur = [], None
    for ln in lines:
        if ln.startswith(" ") and cur is not None:
            cur.append(ln)
        else:
            cur = [ln]
            entries.append(cur)
    labs = list(R["labels"])
    lab_re = re.compile("|".join(r"(?<![\w])" + re.escape(x) + r"(?![\w])" for x in labs))
    out = []
    for ent in entries:
        text = "\n".join(ent)
        m = re.match(pre + r"(\w+)\(([^)]*)\)", text)
        if not m:
            raise ParseError(f"tool entry {text[:40]!r}")
        params = []
        for a in _args(m.group(2)):
            v, _, ty = a.partition(":")
            params.append([v.strip(), ty.strip()])
        rest = text[m.end():]
        hits = list(lab_re.finditer(rest))
        seg = {lab: "" for lab in labs}
        for i, h in enumerate(hits):
            seg[h.group(0)] = rest[h.end(): hits[i + 1].start() if i + 1 < len(hits) else len(rest)]
        needs = [[bool(x.group(1)), x.group(2), _args(x.group(3))] for x in LIT.finditer(seg[labs[0]])]
        adds = [[x.group(2), _args(x.group(3))] for x in LIT.finditer(seg[labs[1]])]
        dels = [[x.group(2), _args(x.group(3))] for x in LIT.finditer(seg[labs[2]])]
        out.append([m.group(1), params, needs, adds, dels])
    return out


def _option_key(qform: str, text: str) -> str:
    if qform == TX.HEAD_VERDICT:
        if text in TX.VERDICT_BASE or TX.STEP_RE.fullmatch(text):
            return text
        raise ParseError(f"unknown verdict option {text!r}")
    if not CALL.fullmatch(text):
        raise ParseError(f"option {text!r} is not a call")
    return text


def parse(row: dict, ctx) -> dict:
    wording = ctx.skin(row["meta"]["wording_id"])
    qform = wording.qform
    reg = ctx.skin(row["meta"]["c2"]["skin_id"]).register
    rules, sep, question = row["instructions"].partition("\n\n")
    if not sep or rules != TX.RULES[qform] or question != wording.text or question not in TX.WORDINGS[qform]:
        raise ParseError("rules / question text does not match the G0 wording")
    lines = row["state"].split("\n")
    if lines[0] != TX.H_TOOLS:
        raise ParseError("no tools header")
    i = 1
    while not lines[i].startswith(TX.H_OBJECTS):
        i += 1
    tools = _tools(lines[1:i], reg)
    objs = {}
    for part in lines[i][len(TX.H_OBJECTS):].strip().split("; "):
        m = re.fullmatch(r"(.+) \((\w+)\)", part)
        if not m:
            raise ParseError(f"objects {part!r}")
        objs[m.group(2)] = [x.strip() for x in m.group(1).split(",")]
    if not lines[i + 1].startswith(TX.H_START) or not lines[i + 2].startswith(TX.H_GOAL):
        raise ParseError("start / goal lines")
    st = lines[i + 1][len(TX.H_START):].strip()
    start = [] if st == TX.NOTHING else [[x.group(2), _args(x.group(3))] for x in LIT.finditer(st)]
    goal = [[bool(x.group(1)), x.group(2), _args(x.group(3))] for x in LIT.finditer(lines[i + 2][len(TX.H_GOAL):])]
    head = lines[i + 3]
    want = TX.H_PLAN if qform == TX.HEAD_VERDICT else TX.H_CALLS
    if head != want:
        raise ParseError("plan header")
    seq = []
    for ln in lines[i + 4:]:
        if ln == TX.NONE_YET:
            continue
        m = re.fullmatch(r"\d+\. (\w+)\((.*)\)", ln)
        if not m:
            raise ParseError(f"call line {ln!r}")
        seq.append([m.group(1), _args(m.group(2))])
    view = {"qform": qform, "tools": tools, "objects": objs, "start": start, "goal": goal,
            "plan" if qform == TX.HEAD_VERDICT else "prefix": seq}
    view["options"] = [_option_key(qform, t) for t in row["options"]]
    return view


# ------------------------------------------------------------------------------------------------ regression core
def _bind(tool, args):
    b = dict(zip([p[0] for p in tool[1]], args))
    pos = frozenset((p, tuple(b[v] for v in a)) for n, p, a in tool[2] if not n)
    neg = frozenset((p, tuple(b[v] for v in a)) for n, p, a in tool[2] if n)
    adds = frozenset((p, tuple(b[v] for v in a)) for p, a in tool[3])
    dels = frozenset((p, tuple(b[v] for v in a)) for p, a in tool[4])
    return pos, neg, adds, dels


def _regress(cond, eff):
    """Weakest precondition of `cond` (a frozenset of (negated, pred, args)) through a call; None if contradictory."""
    pos, neg, adds, dels = eff
    out = set()
    for ng, p, ar in cond:
        f = (p, ar)
        if not ng:
            if f in adds:
                continue
            if f in dels:
                return None
        else:
            if f in dels:
                continue
            if f in adds:
                return None
        out.add((ng, p, ar))
    out |= {(False, p, ar) for p, ar in pos}
    out |= {(True, p, ar) for p, ar in neg}
    if any((not ng, p, ar) in out for ng, p, ar in out):
        return None
    return frozenset(out)


def _sat(state, cond):
    return all(((p, ar) in state) != ng for ng, p, ar in cond)


def _well_formed(tools, objs, step):
    t = tools.get(step[0])
    return t is not None and len(step[1]) == len(t[1]) and all(a in objs.get(p[1], ()) for a, p in zip(step[1], t[1]))


def _verdict(view) -> str:
    tools = {t[0]: t for t in view["tools"]}
    objs = view["objects"]
    plan = view["plan"]
    if not all(_well_formed(tools, objs, s) for s in plan):
        return TX.V_INVALID
    start = frozenset((p, tuple(a)) for p, a in view["start"])
    effs = [_bind(tools[nm], tuple(a)) for nm, a in plan]
    for k in range(len(plan)):
        cond = frozenset([(False, p, ar) for p, ar in effs[k][0]] + [(True, p, ar) for p, ar in effs[k][1]])
        for i in range(k - 1, -1, -1):
            cond = _regress(cond, effs[i])
            if cond is None:
                break
        if cond is None or not _sat(start, cond):
            return TX.V_STEP.format(k=k + 1)
    cond = frozenset((n, p, tuple(a)) for n, p, a in view["goal"])
    for e in reversed(effs):
        cond = _regress(cond, e)
        if cond is None:
            return TX.V_GOAL
    return TX.V_VALID if _sat(start, cond) else TX.V_GOAL


def _next(view) -> str:
    tools = {t[0]: t for t in view["tools"]}
    objs = view["objects"]
    state = set((p, tuple(a)) for p, a in view["start"])
    for nm, a in view["prefix"]:
        pos, neg, adds, dels = _bind(tools[nm], tuple(a))
        if not (pos <= state and not (neg & state)):
            raise ValueError("a prefix call is not applicable")
        state = (state - dels) | adds
    state = frozenset(state)
    acts = []
    for t in view["tools"]:
        for combo in itertools.product(*[objs.get(p[1], []) for p in t[1]]):
            acts.append((t[0], combo, _bind(t, combo)))
    goal = frozenset((n, p, tuple(a)) for n, p, a in view["goal"])
    levels, seen = [[goal]], {goal}
    d = None
    for j in range(0, 12):
        if any(_sat(state, c) for c in levels[j]):
            d = j
            break
        nxt = []
        for c in levels[j]:
            for nm, combo, eff in acts:
                pos, neg, adds, dels = eff
                if not any((not ng and (p, ar) in adds) or (ng and (p, ar) in dels) for ng, p, ar in c):
                    continue
                r = _regress(c, eff)
                if r is not None and r not in seen:
                    seen.add(r)
                    nxt.append(r)
                if len(seen) > 60000:
                    raise ValueError("regression space too large")
        if not nxt:
            break
        levels.append(nxt)
    if not d:
        raise ValueError("goal holds already or is unreachable")
    near = [c for lv in levels[:d] for c in lv]
    ok = []
    for o in view["options"]:
        nm, args = CALL.fullmatch(o).groups()
        args = tuple(_args(args))
        t = tools.get(nm)
        if t is None or len(args) != len(t[1]):
            continue
        pos, neg, adds, dels = _bind(t, args)
        if not (pos <= state and not (neg & state)):
            continue
        s2 = (state - dels) | adds
        if any(_sat(s2, c) for c in near):
            ok.append(o)
    if len(ok) != 1:
        raise ValueError(f"{len(ok)} shortest-route options")
    return ok[0]


def solve_b(view: dict):
    return _verdict(view) if view["qform"] == TX.HEAD_VERDICT else _next(view)
