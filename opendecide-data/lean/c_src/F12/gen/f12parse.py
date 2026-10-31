"""F12 independent parser (G0 section 6): rendered row -> parsed structure (same schema as solver A's S).

Written from the spec's controlled language (6.2 grammar families, SEM-12 / SEM-14 / SEM-42 phrases, closed
empty-attribute phrases, the frozen cue classes of 6.4) and the pack lexicon file (action / object words, field keys,
ID formats, units, enum members). Container decoding is per format style container (json / yaml / html / text).
"""
from __future__ import annotations

import html
import json
import re
import textwrap
from decimal import Decimal

import yaml

import f12lex as L

ATOM_PREFIX = re.compile(r"^(Now: |Requester role: |Tool \w+: |\w+ needs \w+: |\w+ optional \w+: |\w+ rule: |\w+ usage: |\w+ <\w+>: |\w+ \[--\w+(?: VALUE)?\]: |Record: |"
                         r"Stored result from |\[\d{4}-\d{2}-\d{2} |Proposed call: |(Case|Scenario|Item|Entry|"
                         r"Situation|Profile|Matter|Request) [A-Z0-9-]+: )")


class ParseError(Exception):
    pass


# ------------------------------------------------------------------------------------------------ containers
def atoms_of(state: str, container: str) -> list[str]:
    if container == "json":
        txt = state.strip()
        if txt.startswith("```"):
            txt = txt.split("\n", 1)[1].rsplit("```", 1)[0]
        return list(_walk(json.loads(txt)))
    if container == "yaml":
        txt = state.strip("\n")
        if txt.strip().startswith("```"):
            txt = txt.strip().split("\n", 1)[1].rsplit("```", 1)[0]
        return list(_walk(yaml.safe_load(textwrap.dedent(txt.strip("\n")))))
    lines = []
    if container == "html_snippet":
        for m in re.finditer(r"<li[^>]*>(.*?)</li>", state, re.S):
            lines.append(html.unescape(re.sub(r"<[^>]+>", "", m.group(1))).strip())
        return [x for x in lines if ATOM_PREFIX.match(x)]
    for ln in state.split("\n"):
        s = ln.strip()
        s = re.sub(r"^(?:[^\w\s\[\"'(<]{1,3}|\d+[.)]|\(\d+\)|[a-zA-Z][.)])\s+", "", s)
        if ATOM_PREFIX.match(s):
            lines.append(s)
    return lines


def _walk(o):
    if isinstance(o, str):
        if ATOM_PREFIX.match(o):
            yield o
    elif isinstance(o, list):
        for x in o:
            yield from _walk(x)
    elif isinstance(o, dict):
        for v in o.values():
            yield from _walk(v)


def split_top(s, sep):
    out, depth, cur, i = [], 0, [], 0
    while i < len(s):
        if s[i] == "(":
            depth += 1
        elif s[i] == ")":
            depth -= 1
        if depth == 0 and s.startswith(sep, i):
            out.append("".join(cur))
            cur = []
            i += len(sep)
            continue
        cur.append(s[i])
        i += 1
    out.append("".join(cur))
    return out


# ------------------------------------------------------------------------------------------------ type phrases
NUMU = r"(\d+(?:\.\d+)?)(?: ([A-Za-z][A-Za-z/]*))?"


def parse_limits(p, txt):
    if not txt:
        return
    m = re.fullmatch(r"between " + NUMU + r" and " + NUMU + r", inclusive", txt)
    if m and p["type"] in ("integer", "decimal"):
        p["min"], p["max"] = (_num(p, m.group(1)), True), (_num(p, m.group(3)), True)
        return
    m = re.fullmatch(r"between (\d{4}-\d{2}-\d{2}) and (\d{4}-\d{2}-\d{2}), inclusive", txt)
    if m:
        p["min"], p["max"] = (m.group(1), True), (m.group(2), True)
        return
    for part in txt.split(" and "):
        m = re.fullmatch(r"(at least|more than|at most|less than) " + NUMU, part)
        if m and p["type"] in ("integer", "decimal"):
            v = _num(p, m.group(2))
            if m.group(1) in ("at least", "more than"):
                p["min"] = (v, m.group(1) == "at least")
            else:
                p["max"] = (v, m.group(1) == "at most")
            continue
        m = re.fullmatch(r"(on or after|after|on or before|before) (\d{4}-\d{2}-\d{2})", part)
        if m and p["type"] == "date":
            if m.group(1).endswith("after"):
                p["min"] = (m.group(2), m.group(1) == "on or after")
            else:
                p["max"] = (m.group(2), m.group(1) == "on or before")
            continue
        raise ParseError(f"limit phrase {part!r}")


def _num(p, s):
    return int(s) if p["type"] == "integer" else Decimal(s)


def parse_type(name, phrase, required, default):
    p = {"name": name, "required": required, "default": default}
    m = re.fullmatch(r"an ID, (\S+) followed by exactly (\d+) capital letters or digits", phrase)
    if m:
        p.update(type="id", prefix=m.group(1), n=int(m.group(2)))
        return p
    m = re.fullmatch(r"a whole number(?: in ([A-Za-z][A-Za-z/]*))?(?:, (.+))?", phrase)
    if m:
        p.update(type="integer", unit=m.group(1), min=None, max=None)
        parse_limits(p, m.group(2))
        return p
    m = re.fullmatch(r"a number(?: in ([A-Za-z][A-Za-z/]*))? with at most (\d+) decimal places?(?:, (.+))?", phrase)
    if m:
        p.update(type="decimal", unit=m.group(1), places=int(m.group(2)), min=None, max=None)
        parse_limits(p, m.group(3))
        return p
    m = re.fullmatch(r"a date \(YYYY-MM-DD\)(?:, (.+))?", phrase)
    if m:
        p.update(type="date", min=None, max=None)
        parse_limits(p, m.group(1))
        return p
    m = re.fullmatch(r"one of (.+)", phrase)
    if m:
        p.update(type="enum", members=m.group(1).split(", "))
        return p
    m = re.fullmatch(r"text with a length between (\d+) and (\d+) characters, inclusive", phrase)
    if m:
        p.update(type="string", minlen=int(m.group(1)), maxlen=int(m.group(2)))
        return p
    if phrase == "yes or no":
        p.update(type="boolean")
        return p
    raise ParseError(f"type phrase {phrase!r}")


# ------------------------------------------------------------------------------------------------ catalog
def parse_tool_head(body, lex, tools):
    parts = split_top(body, "; ")
    m = re.fullmatch(r"(\w+): (.+)", parts[0])
    if not m:
        raise ParseError("tool head")
    name, cap = m.group(1), m.group(2)
    a, oword = lex_cap(cap, lex)
    t = {"name": name, "a": a, "oword": oword, "scope": None, "pre": None, "roles": None, "cost": None,
         "pref": None, "returns": [], "params": [], "cons": []}
    for x in parts[1:]:
        if x.startswith("only for "):
            rest = x[len("only for "):]
            dimw = next((d for d in lex["dims"] if rest.startswith(d + " ")), None)
            if dimw is None:
                raise ParseError("scope dimension")
            t["scope"] = rest[len(dimw) + 1:].split(" or ")
            t["dimw"] = dimw
        elif x.startswith("any value of every "):
            t["dimw"] = x[len("any value of every "):]
        elif x.startswith("works only when status is "):
            t["pre"] = x[len("works only when status is "):]
        elif x == "works whatever the record shows":
            pass
        elif x.startswith("allowed roles "):
            t["roles"] = x[len("allowed roles "):].split(", ")
        elif x.startswith("cost tier "):
            m2 = re.fullmatch(r"cost tier (\d), (preferred|not preferred)", x)
            t["cost"], t["pref"] = int(m2.group(1)), m2.group(2) == "preferred"
        elif x.startswith("can return "):
            t["returns"] = x[len("can return "):].split(", ")
        elif x == "gives no value to other tools" or x == "no optional inputs":
            pass
        elif x.startswith("needs "):
            for item in split_top(x[len("needs "):], ", "):
                m2 = re.fullmatch(r"(\w+) \((.+)\)", item)
                t["params"].append(parse_type(m2.group(1), m2.group(2), True, None))
        elif x.startswith("optional "):
            for item in split_top(x[len("optional "):], ", "):
                m2 = re.fullmatch(r"(\w+) \((.+)\)", item)
                ph, d = split_top(m2.group(2), "; ")[0], split_top(m2.group(2), "; ")[1]
                t["params"].append(parse_type(m2.group(1), ph, False, None if d == "no default" else
                                              d[len("default "):]))
        else:
            raise ParseError(f"tool attribute {x!r}")
    tools[name] = t


def lex_cap(cap, lex):
    for a, forms in list(L.ACTIONS.items()) + [("look up", L.READ)]:
        if cap.startswith(forms[1] + " "):
            return a, cap[len(forms[1]) + 1:]
    raise ParseError(f"capability {cap!r}")


# ------------------------------------------------------------------------------------------------ user text
CUE_RES = [
    ("plain", r"(?:Please|I need you to|Go ahead and) (?P<v>[a-z]+(?: up)?) the (?P<o>.+?) (?P<r>called .+|\S+)\."),
    ("polite", r"(?:Could you|Would you) (?P<v>[a-z]+(?: up)?) the (?P<o>.+?) (?P<r>called .+?|\S+)(?:, please)?\?"),
    ("catalog", r"(?:Are you able to|Is it possible for you to) (?P<v>[a-z]+(?: up)?) the (?P<o>.+?) "
                r"(?P<r>called .+|\S+)\?"),
]
CATQ = r"(?:Are you able to|Is it possible for you to) (?P<v>[a-z]+(?: up)?) (?P<os>.+)\?"
INFO_RES = [("info", r"(?:What is|Tell me) the (?P<f>.+?) of the (?P<o>.+?) (?P<r>called .+?|\S+)[?.]"),
            ("polite", r"(?:Could you|Please) look up the (?P<f>.+?) of the (?P<o>.+?) (?P<r>called .+?|\S+)[?.]")]
CORR = {"Sorry, a correction.", "Let me correct that.", "Wait, change that."}


def parse_user_line(ln, lex, pending_ask):
    for cue, rx in INFO_RES:
        m = re.fullmatch(rx, ln)
        if m and m.group("o") in lex["owords"]:
            f = m.group("f").replace(" ", "_")
            return {"t": "req", "kind": "info", "cue": cue, "a": "look up", "o": lex["owords"][m.group("o")],
                    "ref": _ref(m.group("r")), "field": f}
    for cue, rx in CUE_RES:
        m = re.fullmatch(rx, ln)
        if m and m.group("o") in lex["owords"]:
            a = lex["verbs"].get(m.group("v"))
            if a is None:
                raise ParseError("verb")
            kind = "info" if a == "look up" else "action"
            return {"t": "req", "kind": kind, "cue": cue, "a": a, "o": lex["owords"][m.group("o")],
                    "ref": _ref(m.group("r")), "field": None}
    m = re.fullmatch(CATQ, ln)
    if m and m.group("os") in lex["oplurals"]:
        return {"t": "req", "kind": "catalog", "cue": "catalog", "a": lex["verbs"][m.group("v")],
                "o": lex["oplurals"][m.group("os")], "ref": None, "field": None}
    if ln in CORR:
        return {"t": "corr"}
    m = re.fullmatch(r"Use (.+)\.", ln)
    if m:
        return {"t": "val", "p": None, "v": m.group(1), "alts": None}
    m = re.fullmatch(r"(.+)'s ([a-z0-9 ]+) is (.+)\.", ln)
    if m and m.group(2).replace(" ", "_") in lex["fields"]:
        return {"t": "fact", "name": m.group(1), "p": m.group(2).replace(" ", "_"), "v": m.group(3)}
    m = re.fullmatch(r"([a-z0-9 ]+): (.+)", ln)
    if m:
        key, v = m.group(1), m.group(2)
        if key == lex["dimw"]:
            return {"t": "qual", "v": v}
        p = key.replace(" ", "_")
        if p in lex["fields"]:
            ptype = lex["ptypes"].get(p)
            if " or " in v and ptype not in ("string", "boolean", None):
                a1, a2 = v.split(" or ", 1)
                return {"t": "val", "p": p, "v": None, "alts": [a1, a2]}
            return {"t": "val", "p": p, "v": v, "alts": None}
    if pending_ask:
        return {"t": "cont", "v": ln}
    raise ParseError(f"user line {ln!r}")


def _ref(r):
    return ["name", r[len("called "):]] if r.startswith("called ") else ["id", r]


# ------------------------------------------------------------------------------------------------ row
def lexicon(pk):
    acts = {a: L.ACTIONS[a] for a in pk["actions"]}
    verbs = {f[0]: a for a, f in acts.items()}
    verbs["look up"] = "look up"
    ptypes = {k: s["type"] for k, s in pk["params"].items()}
    return {"actions": acts, "verbs": verbs, "owords": {e["word"]: i for i, e in enumerate(pk["etypes"])},
            "oplurals": {e["plural"]: i for i, e in enumerate(pk["etypes"])}, "dimw": pk["dim"]["words"],
            "dims": [pk["dim"]["words"]], "fields": set(pk["params"]), "ptypes": ptypes}


def parse_state(state, container, pk, extra_dims=()):
    lex = lexicon(pk)
    lex["dims"] = [pk["dim"]["words"]] + list(extra_dims)
    S = {"now": None, "role": None, "tools": [], "records": [], "conv": [], "stored": [], "call": None}
    tools = {}
    order = []
    cases = {}
    pending_ask = False
    for at in atoms_of(state, container):
        if at.startswith("Now: "):
            S["now"] = re.fullmatch(r"Now: (\d{4}-\d{2}-\d{2} \d{2}:\d{2}) UTC\.", at).group(1)
        elif at.startswith("Requester role: "):
            S["role"] = at[len("Requester role: "):-1]
        elif at.startswith("Tool "):
            parse_tool_head(at[len("Tool "):-1], lex, tools)
            order.append(at[len("Tool "):].split(":")[0])
        elif re.match(r"^\w+ (needs|optional) \w+: ", at):
            m = re.fullmatch(r"(\w+) needs (\w+): (.+)\.", at)
            if m:
                tools[m.group(1)]["params"].append(parse_type(m.group(2), m.group(3), True, None))
                continue
            m = re.fullmatch(r"(\w+) optional (\w+): (.+); (?:default (.+)|no default)\.", at)
            tools[m.group(1)]["params"].append(parse_type(m.group(2), m.group(3), False, m.group(4)))
        elif re.match(r"^\w+ usage: ", at):
            pass
        elif re.match(r"^\w+ <\w+>: ", at):
            m = re.fullmatch(r"(\w+) <(\w+)>: (.+)\.", at)
            tools[m.group(1)]["params"].append(parse_type(m.group(2), m.group(3), True, None))
        elif re.match(r"^\w+ \[--\w+\]: ", at):
            m = re.fullmatch(r"(\w+) \[--(\w+)\]: a flag; present means yes, absent means no \(the default\)\.", at)
            tools[m.group(1)]["params"].append(parse_type(m.group(2), "yes or no", False, "no"))
        elif re.match(r"^\w+ \[--\w+ VALUE\]: ", at):
            m = re.fullmatch(r"(\w+) \[--(\w+) VALUE\]: (.+); (?:default (.+)|no default)\.", at)
            tools[m.group(1)]["params"].append(parse_type(m.group(2), m.group(3), False, m.group(4)))
        elif re.match(r"^\w+ rule: --\w+ and --\w+ are mutually exclusive", at):
            m = re.fullmatch(r"(\w+) rule: --(\w+) and --(\w+) are mutually exclusive, so give at most one of "
                             r"(\w+) or (\w+)\.", at)
            tools[m.group(1)]["cons"].append({"k": "AT_MOST_ONE", "p": m.group(2), "q": m.group(3)})
        elif re.match(r"^\w+ rule: ", at):
            tn, c = parse_rule(at)
            tools[tn]["cons"].append(c)
        elif at.startswith("Record: "):
            S["records"].append({"fields": _fields(at[len("Record: "):-1])})
        elif at.startswith("Stored result from "):
            m = re.fullmatch(r"Stored result from (\w+) at (\d{4}-\d{2}-\d{2} \d{2}:\d{2}): (.+)\.", at)
            S["stored"].append({"tool": m.group(1), "ts": m.group(2), "fields": _fields(m.group(3))})
        elif at.startswith("["):
            m = re.fullmatch(r"\[(\d{4}-\d{2}-\d{2}) (\d{2}:\d{2})\] (User|Assistant): (.*)", at)
            if m:
                who, ts, txt = m.group(3).lower(), m.group(2), m.group(4)
                if who == "assistant":
                    m2 = re.fullmatch(r"What is the ([a-z0-9 ]+)\?", txt)
                    S["conv"].append({"who": "assistant", "ts": ts, "ask": m2.group(1).replace(" ", "_")
                                      if m2 else None})
                    pending_ask = bool(m2)
                    continue
                st = parse_user_line(txt, lex, pending_ask and not (S["conv"] and S["conv"][-1]["who"] == "user"
                                                                    and S["conv"][-1]["ts"] == ts))
                if S["conv"] and S["conv"][-1]["who"] == "user" and S["conv"][-1]["ts"] == ts:
                    S["conv"][-1]["st"].append(st)
                else:
                    S["conv"].append({"who": "user", "ts": ts, "st": [st]})
                pending_ask = False
                continue
            m = re.fullmatch(r"\[(\d{4}-\d{2}-\d{2} \d{2}:\d{2})\] Tool result from (\w+): (.+)\.", at)
            if not m:
                raise ParseError("conversation line")
            S["conv"].append({"who": "tool", "ts": m.group(1), "tool": m.group(2), "fields": _fields(m.group(3))})
            pending_ask = False
        elif at.startswith("Proposed call: "):
            S["call"] = parse_call(at[len("Proposed call: "):])
        else:
            m = re.fullmatch(r"((?:Case|Scenario|Item|Entry|Situation|Profile|Matter|Request) [A-Z0-9-]+): (.*)", at)
            if m:
                cases.setdefault(m.group(1), []).append(parse_user_line(m.group(2), lex, False))
    S["tools"] = [tools[n] for n in order]
    S["cases"] = cases or None
    return S


def _fields(txt):
    out = []
    for part in txt.split("; "):
        k, v = part.split(": ", 1)
        out.append([k, v])
    return out


def parse_call(txt):
    txt = txt.strip()
    if txt.startswith("{"):
        o = json.loads(txt, parse_float=Decimal)
        return {"tool": o["tool"], "args": [[k, v] for k, v in o["arguments"].items()], "syntax": "json"}
    m = re.fullmatch(r"([A-Za-z0-9_]+)\((.*)\)", txt)
    if not m:
        raise ParseError("call")
    args = []
    for part in split_args(m.group(2)):
        k, v = part.split("=", 1)
        args.append([k, json.loads(v, parse_float=Decimal)])
    return {"tool": m.group(1), "args": args, "syntax": "func"}


def split_args(s):
    out, cur, depth, q = [], [], 0, False
    i = 0
    while i < len(s):
        c = s[i]
        if c == '"' and (i == 0 or s[i - 1] != "\\"):
            q = not q
        if not q:
            if c == "[":
                depth += 1
            elif c == "]":
                depth -= 1
            elif c == "," and depth == 0 and s[i:i + 2] == ", ":
                out.append("".join(cur))
                cur = []
                i += 2
                continue
        cur.append(c)
        i += 1
    if cur:
        out.append("".join(cur))
    return out


def parse_policies(text):
    """Card policy settings from the card text (card field on yes/no rows, instructions on choice rows)."""
    t = " ".join((text or "").split())
    pol = {"invalid": "B" if "does not fit; if no tool fits for that reason" in t else "A",
           "tie": "lowest cost tier" in t, "role": "allowed for the requester's stated role" in t,
           "chain": "Call another tool first only when" in t, "fresh": None}
    m = re.search(r"only if it is at most (\d+) minutes old", t)
    if m:
        pol["fresh"] = int(m.group(1))
    return pol


RULES = [("ONLY_IF", r"(\w+) rule: give (\w+) only if (\w+) is also given\."),
         ("UNLESS", r"(\w+) rule: (\w+) is needed unless (\w+) is (.+)\."),
         ("EXACTLY_ONE", r"(\w+) rule: give exactly one of (\w+) or (\w+)\."),
         ("AT_LEAST_ONE", r"(\w+) rule: give at least one of (\w+) or (\w+)\."),
         ("AT_MOST_ONE", r"(\w+) rule: give at most one of (\w+) or (\w+)\.")]


def parse_rule(at):
    for k, rx in RULES:
        m = re.fullmatch(rx, at)
        if m:
            c = {"k": k, "p": m.group(2), "q": m.group(3)}
            if k == "UNLESS":
                c["v"] = m.group(4)
            return m.group(1), c
    raise ParseError(f"rule {at!r}")
