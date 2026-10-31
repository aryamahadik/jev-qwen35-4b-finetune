"""F12 renderer: structure -> fmt1 Doc IR (state), card IR (SEM sentences, G0 section 10), question and option texts.

Every constraint is written in the controlled language of G0 6.2 (SEM-12 limit words, SEM-14 date words, SEM-42 ID
phrases, closed empty-attribute phrases R4-17). Each line of state is one self-contained atom so that the parser
(f12parse.py) reads it in every admitted container. Paraphrase variety lives in request cues, card styles, wordings
and containers, never inside a constraint.
"""
from __future__ import annotations

import json

import f12lex as L

# ------------------------------------------------------------------------------------------------ fixed texts
OUT_NAME_SETS = [
    {"CALL": "Call a tool", "ASK": "Ask the user for more information", "UNABLE": "Say it cannot be done",
     "ANSWER": "Answer directly"},
    {"CALL": "Use one of the listed tools", "ASK": "Ask the user a question first",
     "UNABLE": "Tell the user it cannot be done", "ANSWER": "Reply directly without a tool"},
    {"CALL": "Make a tool call", "ASK": "Request the missing information", "UNABLE": "Explain that it cannot be done",
     "ANSWER": "Give the answer directly"},
]
OUT_DEFS = {"CALL": "call the one fitting tool that has every needed value",
            "ASK": "ask the user for a missing, unclear or unusable value",
            "UNABLE": "say it cannot be done, because no listed tool fits",
            "ANSWER": "answer directly from what is shown (conversation, records, stored results or the tool list)"}
ACT_DEFS = {"call": "call the tool {x} next", "ask": "ask the user for {x}", "unable": "say it cannot be done",
            "answer": "answer directly from what is shown (conversation, records, stored results or the tool list)"}
TXT = {"unable": "Say it cannot be done", "answer": "Answer directly from what is shown",
       "none": "None of the listed tools can do this", "nothing": "Nothing is missing",
       "novalue": "No usable value, so ask the user", "valid": "Nothing, the call is valid"}
QUESTIONS = {
    "C-OUT": "What should the assistant do next?",
    "C-ACT": "What is the assistant's exact next action?",
    "C-TOOL": "Which tool should the assistant call next?",
    "C-PARAM": "For the one tool that fits the request, which needed value is missing (not given, unclear, or not "
               "accepted)?",
    "C-VALUE": "Which value should be used for {p} of {T}?",
    "C-DEFECT": "What is wrong with this call?",
    "C-INV": "Which of these requests can {T} handle right away?",
}
YN = {  # form -> framing -> [base, negated, double-negated]
    ("Y-CALLX", "P"): ["Should the assistant call {T} now?",
                       "Is it true that the assistant should not call {T} now?",
                       "Is it not true that the assistant should not call {T} now?"],
    ("Y-CALLX", "N"): ["Should the assistant hold off calling {T} now?",
                       "Is it true that the assistant should not hold off calling {T} now?",
                       "Is it not true that the assistant should not hold off calling {T} now?"],
    ("Y-ASK", "P"): ["Can the assistant act now without asking the user for more information?",
                     "Is it true that the assistant cannot act now without asking the user for more information?",
                     "Is it not true that the assistant cannot act now without asking the user for more "
                     "information?"],
    ("Y-ASK", "N"): ["Must the assistant ask the user for more information first?",
                     "Is it true that the assistant does not need to ask the user for more information first?",
                     "Is it not true that the assistant does not need to ask the user for more information first?"],
    ("Y-FIT", "P"): ["Can some listed tool do what the user asks?",
                     "Is it true that no listed tool can do what the user asks?",
                     "Is it not true that no listed tool can do what the user asks?"],
    ("Y-FIT", "N"): ["Is it beyond every listed tool to do what the user asks?",
                     "Is it true that it is not beyond every listed tool to do what the user asks?",
                     "Is it not true that it is not beyond every listed tool to do what the user asks?"],
    ("Y-DIRECT", "P"): ["Can the assistant answer directly from what is shown, without a tool?",
                        "Is it true that the assistant cannot answer directly from what is shown, without a tool?",
                        "Is it not true that the assistant cannot answer directly from what is shown, without a "
                        "tool?"],
    ("Y-DIRECT", "N"): ["Does the next step need something other than a direct answer from what is shown?",
                        "Is it true that the next step does not need anything other than a direct answer from what "
                        "is shown?",
                        "Is it not true that the next step does not need anything other than a direct answer from "
                        "what is shown?"],
    ("Y-VALID", "P"): ["Is this call valid under the tool's parameter list?",
                       "Is it true that this call is not valid under the tool's parameter list?",
                       "Is it not true that this call is not valid under the tool's parameter list?"],
    ("Y-VALID", "N"): ["Does this call break the tool's parameter list?",
                       "Is it true that this call does not break the tool's parameter list?",
                       "Is it not true that this call does not break the tool's parameter list?"],
    ("Y-CORRECT", "P"): ["Is this call correct for the user's request?",
                         "Is it true that this call is not correct for the user's request?",
                         "Is it not true that this call is not correct for the user's request?"],
    ("Y-CORRECT", "N"): ["Does this call differ from what the user's request needs?",
                         "Is it true that this call does not differ from what the user's request needs?",
                         "Is it not true that this call does not differ from what the user's request needs?"],
}
CUES = {  # request kind cues (6.4): plain, polite (also on info questions), catalog (own ability), info
    "plain": ["Please {a} the {o} {ref}.", "I need you to {a} the {o} {ref}.", "Go ahead and {a} the {o} {ref}."],
    "polite": ["Could you {a} the {o} {ref}?", "Would you {a} the {o} {ref}, please?"],
    "catalog": ["Are you able to {a} the {o} {ref}?", "Is it possible for you to {a} the {o} {ref}?"],
    "catalog_q": ["Are you able to {a} {os}?", "Is it possible for you to {a} {os}?"],
    "info": ["What is the {f} of the {o} {ref}?", "Tell me the {f} of the {o} {ref}."],
    "polite_info": ["Could you look up the {f} of the {o} {ref}?", "Please look up the {f} of the {o} {ref}."],
}
CORR = ["Sorry, a correction.", "Let me correct that.", "Wait, change that."]
UNNAMED = "Use {v}."


def ref_text(ref):
    return ref[1] if ref[0] == "id" else f"called {ref[1]}"


# ------------------------------------------------------------------------------------------------ catalog atoms
def id_phrase(p):
    return f"an ID, {p['prefix']} followed by exactly {p['n']} capital letters or digits"


def lim_num(p):
    u = (" " + p["unit"]) if p.get("unit") else ""
    lo, hi = p.get("min"), p.get("max")
    f = L.fmt_dec
    if lo and hi and lo[1] and hi[1]:
        return f"between {f(lo[0])} and {f(hi[0])}{u}, inclusive"
    parts = []
    if lo:
        parts.append((f"at least {f(lo[0])}{u}" if lo[1] else f"more than {f(lo[0])}{u}"))
    if hi:
        parts.append((f"at most {f(hi[0])}{u}" if hi[1] else f"less than {f(hi[0])}{u}"))
    return " and ".join(parts)


def lim_date(p):
    lo, hi = p.get("min"), p.get("max")
    if lo and hi and lo[1] and hi[1]:
        return f"between {lo[0]} and {hi[0]}, inclusive"
    parts = []
    if lo:
        parts.append(f"on or after {lo[0]}" if lo[1] else f"after {lo[0]}")
    if hi:
        parts.append(f"on or before {hi[0]}" if hi[1] else f"before {hi[0]}")
    return " and ".join(parts)


def type_phrase(p):
    t = p["type"]
    if t == "id":
        return id_phrase(p)
    if t == "integer":
        s = "a whole number" + (f" in {p['unit']}" if p.get("unit") else "")
        lim = lim_num(p)
        return s + (", " + lim if lim else "")
    if t == "decimal":
        s = "a number" + (f" in {p['unit']}" if p.get("unit") else "") + \
            f" with at most {p['places']} decimal place" + ("s" if p["places"] > 1 else "")
        lim = lim_num(p)
        return s + (", " + lim if lim else "")
    if t == "date":
        lim = lim_date(p)
        return "a date (YYYY-MM-DD)" + (", " + lim if lim else "")
    if t == "enum":
        return "one of " + ", ".join(p["members"])
    if t == "string":
        return f"text with a length between {p['minlen']} and {p['maxlen']} characters, inclusive"
    if t == "boolean":
        return "yes or no"
    raise AssertionError(t)


def param_atom(tn, p):
    if p["required"]:
        return f"{tn} needs {p['name']}: {type_phrase(p)}."
    d = f"; default {p['default']}" if p["default"] is not None else "; no default"
    return f"{tn} optional {p['name']}: {type_phrase(p)}{d}."


def tool_atoms(t, pk, card, layout):
    """Atoms for one tool. layout full (3-25 bins) or compact (26-60)."""
    n = t["name"]
    a = L.READ[1] if t["a"] == "look up" else L.ACTIONS[t["a"]][1]
    ow = t.get("oword") or pk["etypes"][t["o"]]["word"]
    dimw = card["dimw"]
    pol = card["pol"]
    scope = (f"only for {dimw} " + " or ".join(t["scope"])) if t["scope"] else f"any value of every {dimw}"
    pre = f"works only when status is {t['pre']}" if t["pre"] else "works whatever the record shows"
    roles = ("allowed roles " + ", ".join(t["roles"])) if pol["role"] else None
    tie = (f"cost tier {t['cost']}, " + ("preferred" if t["pref"] else "not preferred")) if pol["tie"] else None
    ret = None
    if pol["chain"]:
        ret = ("can return " + ", ".join(t["returns"])) if t["returns"] else "gives no value to other tools"
    if t.get("borrowed"):
        dimw2 = t.get("dimw", dimw)
        scope = f"any value of every {dimw2}"
    if layout == "compact":
        assert not t.get("cons"), "rules only in full layout"
        req = [p for p in t["params"] if p["required"]]
        opt = [p for p in t["params"] if not p["required"]]
        bits = [f"Tool {n}: {a} {ow}", scope, pre]
        for x in (roles, tie, ret):
            if x:
                bits.append(x)
        bits.append("needs " + ", ".join(f"{p['name']} ({type_phrase(p)})" for p in req))
        bits.append(("optional " + ", ".join(f"{p['name']} ({type_phrase(p)}"
                                             + (f"; default {p['default']}" if p["default"] is not None else
                                                "; no default") + ")" for p in opt)) if opt else
                    "no optional inputs")
        return ["; ".join(bits) + "."]
    head = [f"Tool {n}: {a} {ow}", scope, pre] + [x for x in (roles, tie, ret) if x]
    if all(p["required"] for p in t["params"]):
        head.append("no optional inputs")
    out = ["; ".join(head) + "."]
    if card.get("syntax") == "cli":
        return out + cli_atoms(t)
    for p in t["params"]:
        out.append(param_atom(n, p))
    for c in t.get("cons") or []:
        out.append(cons_atom(n, c))
    return out


def cli_atoms(t):
    """S5 command-line usage (G0 4 S5): <ARG> needed; [--p VALUE] optional with its default; [--p] a yes/no flag
    (always optional, default no); rules in controlled words, mutually exclusive glossed as at most one of."""
    n = t["name"]
    req = [p for p in t["params"] if p["required"]]
    opt = [p for p in t["params"] if not p["required"]]
    usage = " ".join([n] + [f"<{p['name']}>" for p in req] + [f"[--{p['name']}]" if p["type"] == "boolean" else
                                                           f"[--{p['name']} VALUE]" for p in opt])
    out = [f"{n} usage: {usage}."]
    for p in req:
        assert p["type"] != "boolean"
        out.append(f"{n} <{p['name']}>: {type_phrase(p)}.")
    for p in opt:
        if p["type"] == "boolean":
            assert p["default"] == "no"
            out.append(f"{n} [--{p['name']}]: a flag; present means yes, absent means no (the default).")
        else:
            d = f"default {p['default']}" if p["default"] is not None else "no default"
            out.append(f"{n} [--{p['name']} VALUE]: {type_phrase(p)}; {d}.")
    for c in t.get("cons") or []:
        if c["k"] == "AT_MOST_ONE":
            out.append(f"{n} rule: --{c['p']} and --{c['q']} are mutually exclusive, so give at most one of "
                       f"{c['p']} or {c['q']}.")
        else:
            out.append(cons_atom(n, c))
    return out


def cons_atom(tn, c):
    """Cross-param rule in controlled words (A26, SEM-10, SEM-13, SEM-40)."""
    k = c["k"]
    if k == "ONLY_IF":
        return f"{tn} rule: give {c['p']} only if {c['q']} is also given."
    if k == "UNLESS":
        return f"{tn} rule: {c['p']} is needed unless {c['q']} is {c['v']}."
    w = {"EXACTLY_ONE": "exactly one", "AT_LEAST_ONE": "at least one", "AT_MOST_ONE": "at most one"}[k]
    return f"{tn} rule: give {w} of {c['p']} or {c['q']}."


# ------------------------------------------------------------------------------------------------ state doc
def fields_text(fields):
    return "; ".join(f"{k}: {v}" for k, v in fields)


def user_lines(st, pk):
    out = []
    for s in st:
        t = s["t"]
        if t == "req":
            out.append(s["_text"])
        elif t == "val":
            if s.get("alts"):
                out.append(f"{L.words(s['p'])}: {s['alts'][0]} or {s['alts'][1]}")
            elif s["p"] is None:
                out.append(UNNAMED.format(v=s["v"]))
            else:
                out.append(f"{L.words(s['p'])}: {s['v']}")
        elif t == "qual":
            out.append(f"{pk['dim']['words']}: {s['v']}")
        elif t == "corr":
            out.append(s.get("_text") or CORR[0])
        elif t == "fact":
            out.append(f"{s['name']}'s {L.words(s['p'])} is {s['v']}.")
        elif t == "cont":
            out.append(s["v"])
    return out


def request_text(req, pk, rng):
    a, o = req["a"], pk["etypes"][req["o"]]
    ab = L.READ[0] if a == "look up" else L.ACTIONS[a][0]
    if req["kind"] == "catalog":
        return rng.choice(CUES["catalog_q"]).format(a=ab, os=o["plural"])
    if req["kind"] == "info":
        key = "info" if req["cue"] == "info" else "polite_info"
        return rng.choice(CUES[key]).format(f=L.words(req["field"]), o=o["word"], ref=ref_text(req["ref"]))
    return rng.choice(CUES[req["cue"]]).format(a=ab, o=o["word"], ref=ref_text(req["ref"]))


def state_doc(R, pk, card, rng, layout):
    S = R["S"]
    blocks = []
    blocks.append({"type": "section", "heading": "Current time",
                   "blocks": [{"type": "items", "items": [f"Now: {S['now']} UTC."]}]})
    if card["pol"]["role"] and S.get("role"):
        blocks.append({"type": "section", "heading": "Requester",
                       "blocks": [{"type": "items", "items": [f"Requester role: {S['role']}."]}]})
    atoms = []
    for t in S["tools"]:
        atoms += tool_atoms(t, pk, card, layout)
    blocks.append({"type": "section", "heading": "Tools", "blocks": [{"type": "items", "items": atoms}]})
    if S["records"]:
        blocks.append({"type": "section", "heading": "Records", "blocks": [
            {"type": "items", "items": ["Record: " + fields_text(r["fields"]) + "." for r in S["records"]]}]})
    if S["stored"]:
        blocks.append({"type": "section", "heading": "Stored results", "blocks": [
            {"type": "items", "items": [f"Stored result from {s['tool']} at {s['ts']}: " + fields_text(s["fields"])
                                        + "." for s in S["stored"]]}]})
    if R.get("cases"):
        items = []
        for ref, st in R["cases"]:
            for ln in user_lines(st, pk):
                items.append(f"{ref}: {ln}")
        blocks.append({"type": "section", "heading": "Requests", "blocks": [{"type": "items", "items": items}]})
    else:
        lines = []
        date = S["now"][:10]
        for c in S["conv"]:
            if c["who"] == "user":
                for ln in user_lines(c["st"], pk):
                    lines.append(f"[{date} {c['ts']}] User: {ln}")
            elif c["who"] == "assistant":
                txt = (f"What is the {L.words(c['ask'])}?" if c.get("ask") else "Noted, thank you.")
                lines.append(f"[{date} {c['ts']}] Assistant: {txt}")
            else:
                lines.append(f"[{c['ts']}] Tool result from {c['tool']}: " + fields_text(c["fields"]) + ".")
        blocks.append({"type": "section", "heading": "Conversation", "blocks": [{"type": "items",
                                                                                 "items": lines}]})
    if S.get("call"):
        blocks.append({"type": "section", "heading": "Proposed call", "blocks": [
            {"type": "items", "items": ["Proposed call: " + call_text(S["call"])]}]})
    return {"title": None, "meta": [], "blocks": blocks}


def jv(v):
    """JSON / function-call value text of an audit argument (typed: str, int, Decimal-as-str-number, bool, list)."""
    if isinstance(v, dict) and "num" in v:
        return v["num"]
    if isinstance(v, bool):
        return "true" if v else "false"
    if isinstance(v, list):
        return "[" + ", ".join(jv(x) for x in v) + "]"
    if isinstance(v, int):
        return str(v)
    return json.dumps(v)


def call_text(call):
    if call["syntax"] == "json":
        return "{\"tool\": " + json.dumps(call["tool"]) + ", \"arguments\": {" + ", ".join(
            json.dumps(k) + ": " + jv(v) for k, v in call["args"]) + "}}"
    if call["syntax"] == "func":
        return call["tool"] + "(" + ", ".join(f"{k}={jv(v)}" for k, v in call["args"]) + ")"
    raise AssertionError(call["syntax"])


# ------------------------------------------------------------------------------------------------ options
def opt_text(o, R, card):
    k = o[0]
    scheme = card.get("names")
    if k == "out":
        if scheme:
            return scheme["map"][o[1]]
        return OUT_NAME_SETS[card["out_set"]][o[1]]
    if k in ("call", "ask") and scheme:
        return f"{scheme['map']['CALL' if k == 'call' else 'ASK']} {o[1]}"
    if k in ("unable", "answer") and scheme:
        return scheme["map"]["UNABLE" if k == "unable" else "ANSWER"]
    if k == "call":
        return f"Call {o[1]}"
    if k == "ask":
        return f"Ask for {o[1]}"
    if k in ("tool", "param", "value", "case"):
        return str(o[1])
    if k == "defect":
        return o[1]
    return TXT[k]


def option_defs(R, card, texts):
    """Definition lines for masked / swapped C-OUT and C-ACT rows (8.1): one per option."""
    if not card.get("names") or R["form"] not in ("C-OUT", "C-ACT"):
        return None
    ents = []
    for o, tx in zip(R["opts"], texts):
        if o[0] == "out":
            d = OUT_DEFS[o[1]]
        elif o[0] in ("call", "ask"):
            d = ACT_DEFS[o[0]].format(x=o[1])
        else:
            d = ACT_DEFS[o[0]]
        ents.append({"name": tx, "text": d})
    return ents
