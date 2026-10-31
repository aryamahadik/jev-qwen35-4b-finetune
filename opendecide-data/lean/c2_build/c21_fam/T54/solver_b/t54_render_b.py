"""T54 SOLVER B, RENDER-FIDELITY PARSER (G0-lite 3.3: "a deterministic parser over the RENDERED prompt (regex/slot extraction, no
model) to recover the record fields the rules need"). Standard library only. Input: the rendered text of one row (a string).
Output: a letter, or an abstain code when the text does not carry enough to decide (an abstain is NOT a disagreement).

Written from G0_LITE.md section 3.2 and from the rendered-text shapes only. It never sees a stored label or a record.
Limits (reported, not hidden):
  * the verb equivalence table (add=create, delete=remove, lookup=read=get, search=find, set=update) is the engine's group
    convention as OBSERVED on record `group` ids; the G0-lite says only that groups exist.
  * card and option wording is matched with keyword rules; unrecognised wording -> abstain (a Haiku reword pass will need the
    rules re-checked by the round-trip test).
"""
import re

ACTIONS = ["get", "list", "find", "search for", "search", "count", "read", "check", "create", "add", "update", "set", "rename", "move",
           "copy", "remove", "delete", "cancel", "close", "open", "archive", "restore", "assign", "merge", "send", "schedule",
           "reserve", "release", "approve", "reject", "export", "import", "sync", "lock", "unlock", "tag", "look up", "lookup"]
_ACT_NORM = {"search for": "search", "look up": "lookup"}
_GROUP = {"add": "create", "delete": "remove", "lookup": "get", "read": "get", "search": "find", "set": "update"}
_ACT_RE = "|".join(sorted([re.escape(a) for a in ACTIONS], key=len, reverse=True))
_ORD = {"first": "1", "second": "2", "third": "3", "fourth": "4", "fifth": "5", "sixth": "6", "seventh": "7", "eighth": "8",
        "ninth": "9", "tenth": "10", "eleventh": "11", "twelfth": "12"}


def grp(verb):
    return _GROUP.get(verb, verb)


class Abstain(Exception):
    pass


# ------------------------------------------------------------------------------------------------------------ wording lexicon
# The production wording pool holds >= 50 wordings per form (cards, options, requests, facts), far more than the keyword rules below were
# written for. `set_lexicon` injects the pool ({form id: [templates with {slot} fields]}) as DATA: a sentence is recognised by an exact
# match against the pool's templates (slots captured by pattern); every decision still comes from the facts in the rendered row. Without a
# lexicon only the keyword rules run. Standard library only; the dict is passed in, never read from a file here.
_LEX = {}
_RX = {}
_SLOT_RE = {"entity": r"\w+", "field": r"\w+", "value": r"\S+?", "ref": r"\S+?", "refpart": r"(?: \S+)?", "clauses": r"(?:, .*?)?",
            "action": r"[a-z]+(?: [a-z]+)?", "action_cap": r"[A-Z][a-z]+(?: [a-z]+)?", "pname": r"\w+(?: \w+)?", "steps": r".+"}
_OPT_LABELS = ("CALL", "ASK", "NO_TOOL", "ANSWER", "RESULT_MISSING", "WRITE", "READ_FIRST", "DONE_NO_CALL", "GROUNDED", "UNGROUNDED")


def set_lexicon(pools):
    _LEX.clear()
    _LEX.update(dict((k, list(v)) for k, v in (pools or {}).items()))
    _RX.clear()


def _rx(tpl):
    if tpl not in _RX:
        seen, out = set(), []
        for i, part in enumerate(re.split(r"\{([a-z_]+)\}", tpl)):
            if i % 2 == 0:
                out.append(re.escape(part))
            elif part in seen:
                out.append("(?P=%s)" % part)
            else:
                seen.add(part)
                out.append("(?P<%s>%s)" % (part, _SLOT_RE.get(part, r".+?")))
        _RX[tpl] = re.compile("^" + "".join(out) + "$", re.S)
    return _RX[tpl]


def lex_line(forms, line):
    """-> (form, slots) when the line matches a template of one of `forms`; None when none; Abstain when two different forms match."""
    hits = {}
    for f in forms:
        for tpl in _LEX.get(f, ()):
            m = _rx(tpl).match(line)
            if m:
                hits.setdefault(f, m.groupdict())
                break
    if len(hits) > 1:
        raise Abstain("wording_ambiguous:" + ",".join(sorted(hits)))
    return next(iter(hits.items())) if hits else None


# ------------------------------------------------------------------------------------------------------------- text parsing
def parse(text):
    if "\n\nTools:\n" not in text or "\n\nConversation:\n" not in text:
        raise Abstain("layout")
    head, rest = text.split("\n\nTools:\n", 1)
    tools_block, rest = rest.split("\n\nConversation:\n", 1)
    if "\n\nQuestion:" in rest:
        conv, qa = rest.split("\n\nQuestion:", 1)
    else:
        raise Abstain("no_question")
    qlines = qa.split("\n")
    opts = {}
    for ln in qlines[1:]:
        m = re.match(r"^([A-Z])\) (.*)$", ln)
        if m:
            opts[m.group(1)] = m.group(2)
    tools = {}
    for ln in tools_block.split("\n"):
        m = re.match(r"^- (\w+)\((.*)\) \[(.*?)\] -- (.*)$", ln)
        if not m:
            continue
        name = m.group(1)
        verb, _, ent = name.partition("_")
        params = []
        for p in split_top(m.group(2)):
            pm = re.match(r"^(\w+): (\w+)(\?)?(?: = (.*))?$", p.strip())
            if not pm:
                raise Abstain("tool_param_syntax")
            params.append(dict(name=pm.group(1), type=pm.group(2), required=not pm.group(3), default=pm.group(4)))
        flags = [f.strip() for f in m.group(3).split(",")]
        tools[name] = dict(name=name, verb=verb, entity=ent, group=grp(verb), params=params, rw=flags[0],
                           idempotent="idempotent" in flags)
    return dict(head=head, tools=tools, conv=conv, opts=opts)


def split_top(s):
    out, cur, depth, q = [], "", 0, False
    for ch in s:
        if ch == '"':
            q = not q
        if ch == "," and not q and depth == 0:
            out.append(cur)
            cur = ""
            continue
        cur += ch
    if cur.strip():
        out.append(cur)
    return out


def card_flags(head):
    if _LEX:
        found = set()
        for ln in head.split("\n"):
            lx = lex_line(["card.card.t54.strict_ask", "card.card.t54.defaults_ok"], ln.strip())
            if lx is not None:
                found.add(lx[0])
        if len(found) == 1:
            return found.pop() == "card.card.t54.defaults_ok"
    h = head.lower()
    defaults_ok = bool(re.search(r"use the default|may stand in", h))
    strict = bool(re.search(r"never fill|defaults are not used", h))
    if defaults_ok == strict:
        # neither (or both) recognised: only an error when the rule needs the card
        return None
    return defaults_ok


def user_lines(conv):
    return [ln[len("User: "):] for ln in conv.split("\n") if ln.startswith("User: ")]


def agent_calls(conv):
    """[(tool, {arg: value}, {outkey: value} or None for 'no output recorded')]"""
    calls = []
    lines = conv.split("\n")
    i = 0
    while i < len(lines):
        m = re.match(r"^Agent called (\w+)\((.*)\)$", lines[i])
        if m:
            args = dict((k, v) for k, v in re.findall(r'(\w+)="((?:[^"\\]|\\.)*)"', m.group(2)))
            out = None
            if i + 1 < len(lines) and lines[i + 1].strip().startswith("-> output:"):
                out = {}
                j = i + 2
                while j < len(lines) and lines[j].startswith("     "):
                    k, _, v = lines[j].strip().partition(": ")
                    out[k] = v
                    j += 1
                i = j - 1
            elif i + 1 < len(lines) and "no output" in lines[i + 1]:
                out = None
                i += 1
            calls.append((m.group(1), args, out))
        i += 1
    return calls


def classify_option(t):
    if _LEX:
        hit = [lab for lab in _OPT_LABELS if t in _LEX.get("opt." + lab, ())]
        if len(hit) == 1:
            return hit[0]
    s = t.lower()
    if re.search(r"earlier result|never arrived|result is missing", s):
        return "RESULT_MISSING"
    if re.search(r"at least one value|some supplied value|has no grounding|has no source", s):
        return "UNGROUNDED"
    if re.search(r"every value|all supplied values|all values in|come from the conversation", s) and "tool call now" not in s:
        return "GROUNDED"
    if re.search(r"\bask\b", s):
        return "ASK"
    if re.search(r"no listed tool|cannot do this|listed tools cannot", s):
        return "NO_TOOL"
    if re.search(r"answer directly|reply from what|without a tool", s):
        return "ANSWER"
    if re.search(r"no call|already|do nothing", s) and "write call" not in s:
        return "DONE_NO_CALL"
    if re.search(r"read", s) and re.search(r"first|state", s) and "listed tool" not in s:
        return "READ_FIRST"
    if re.search(r"write call", s):
        return "WRITE"
    if re.search(r"call the listed tool|tool call now|make the tool call", s):
        return "CALL"
    return None


def letter_for(opts, label):
    hits = [l for l, t in opts.items() if classify_option(t) == label]
    if len(hits) != 1:
        raise Abstain("option_wording_unrecognised_or_duplicate:" + label)
    return hits[0]


def pwords(p):
    return p.replace("_", " ")


def stated(userlines, param, entity=None):
    """The request states a value for `param`: a clause 'with <param words> <value>', or, for the entity's own id parameter, the
    reference written right after the entity noun ('the <entity> <id>')."""
    if any(re.search(r"\bwith " + re.escape(pwords(param)) + r"(?= )", ln) for ln in userlines):
        return True
    if entity and param == entity + "_id" and userlines:
        return bool(re.search(r"\bthe " + re.escape(entity) + r" [a-z]{3}-\d+", userlines[-1]))
    return False


# ----------------------------------------------------------------------------------------------------------- request forms
def request_of(userlines):
    if not userlines:
        raise Abstain("no_user_line")
    return userlines[-1]


_FETCH = [r"What is the (\w+) of the (?:same )?(\w+)", r"Which (\w+) does the (?:same )?(\w+)"]
_INFO = [r"Which (\w+) did I give for that (\w+)", r"What (\w+) did I say that (\w+) has"]
_INFO_CARD = [r"What is the default (\w+) for the (\w+)", r"Which default (\w+) applies to the (\w+)"]


_REQ_FORMS = ["req." + k for k in ("act", "fetch", "fetch_ref", "info", "info_card", "reference", "plan", "state_write")]


def req_kind(req):
    if _LEX:
        lx = lex_line(_REQ_FORMS, req)
        if lx is not None:
            k, sl = lx[0][len("req."):], lx[1]
            if k in ("act", "reference"):
                v = sl["action"].lower()
                return k, dict(verb=_ACT_NORM.get(v, v), entity=sl["entity"])
            if k in ("fetch", "fetch_ref", "info", "info_card"):
                return k, dict(field=sl["field"], entity=sl["entity"])
            if k == "plan":
                return "plan", {}
    for pat in _INFO_CARD:
        m = re.search(pat, req)
        if m:
            return "info_card", dict(field=m.group(1), entity=m.group(2))
    for pat in _INFO:
        m = re.search(pat, req)
        if m:
            return "info", dict(field=m.group(1), entity=m.group(2))
    for pat in _FETCH:
        m = re.search(pat, req)
        if m:
            same = "same " in m.group(0)
            return ("fetch_ref" if same else "fetch"), dict(field=m.group(1), entity=m.group(2))
    m = re.search(r"\b(" + _ACT_RE + r")\s+the\s+([a-z]+)", req, re.I)
    if m:
        v = m.group(1).lower()
        v = _ACT_NORM.get(v, v)
        if re.search(r"using the same \w+ as before|with the same \w+ as last time", req):
            return "reference", dict(verb=v, entity=m.group(2))
        return "act", dict(verb=v, entity=m.group(2))
    if re.search(r"Do the following|Carry out these steps", req):
        return "plan", {}
    raise Abstain("request_form_unrecognised")


def find_fact(head, ulines, field, entity, ref=None):
    if _LEX:
        for ln in ulines:
            lx = lex_line(["fact.text"], ln)
            if lx is not None and lx[1]["entity"] == entity and lx[1]["field"] == field and (ref is None or lx[1]["ref"] == ref):
                return True
        for ln in head.split("\n"):
            lx = lex_line(["card.note"], ln.strip())
            if lx is not None and lx[1]["entity"] == entity and lx[1]["field"] == field:
                return True
    for ln in ulines:
        for m in re.finditer(r"(?:For the record|Note that),? the (\w+) (\S+?) (?:has|carries) (\w+) (\S+?)\.(?:\s|$)", ln):
            if m.group(1) == entity and m.group(3) == field and (ref is None or m.group(2) == ref):
                return True
    for m in re.finditer(r"(?:the default (\w+) for a (\w+) is (\S+?)\.|Default: (\w+) of a (\w+) is (\S+?)\.)", head):
        f, e = (m.group(1), m.group(2)) if m.group(1) else (m.group(4), m.group(5))
        if f == field and e == entity:
            return True
    return False


def target_present(P, kind, info):
    """Is a listed tool present that does the intent? Returns (tool_or_None, ambiguous)."""
    tools = P["tools"].values()
    ent = info["entity"]
    if kind in ("act", "reference"):
        c = [t for t in tools if t["entity"] == ent and t["group"] == grp(info["verb"])]
        return (c[0] if c else None), len(c) > 1
    # fetch-type ("what is the <field> of the <entity>"): the request does not show the verb. Candidates are the read tools of this
    # entity in the get and check groups (list / find / count do not fetch a named record's field). Several candidates -> the
    # intended one cannot be told from the text -> abstain; one -> taken as the target (it may be a sibling of a deleted target:
    # that is the reported fetch-sibling class); none -> not present.
    c = [t for t in tools if t["entity"] == ent and t["rw"] == "read" and t["group"] in ("get", "check")]
    if len(c) > 1:
        raise Abstain("fetch_target_verb_not_visible")
    if len(c) == 1:
        return c[0], False
    return None, False


def required_unsourced(P, tool, ulines, dok, prior_param=None, prior_ok=True):
    miss, rmiss = [], []
    for p in tool["params"]:
        if not p["required"]:
            continue
        if stated(ulines, p["name"], tool["entity"]):
            continue
        if prior_param == p["name"]:
            (rmiss if not prior_ok else []).append(p["name"])
            continue
        if p["default"] is not None and dok:
            continue
        miss.append(p["name"])
    return miss, rmiss


# --------------------------------------------------------------------------------------------------------- sub-block rules
def solve_s1(P, text):
    dok = card_flags(P["head"])
    ulines = user_lines(P["conv"])
    req = request_of(ulines)
    kind, info = req_kind(req)
    if kind in ("info", "info_card"):
        if find_fact(P["head"], ulines, info["field"], info["entity"]):
            return letter_for(P["opts"], "ANSWER")
        raise Abstain("info_form_without_fact")
    if kind == "fetch":
        ref = None
        m = re.search(r"the " + re.escape(info["entity"]) + r" ([a-z]{3}-\d+)(?![\w-])", req)
        if m:
            ref = m.group(1)
        if find_fact(P["head"], ulines, info["field"], info["entity"], ref):
            return letter_for(P["opts"], "ANSWER")
    if kind == "plan":
        raise Abstain("plan_form")
    if dok is None:
        raise Abstain("card_unrecognised")
    tool, amb = target_present(P, kind, info)
    if tool is None:
        return letter_for(P["opts"], "NO_TOOL")
    if amb:
        raise Abstain("several_candidate_tools")
    ent = info["entity"]
    if kind == "fetch_ref":
        # the id comes from an earlier mention "the <entity> <id>"
        earlier = [ln for ln in ulines[:-1] if re.search(r"\bthe " + re.escape(ent) + r" [a-z]{3}-\d+", ln)]
        miss = []
        for p in tool["params"]:
            if not p["required"]:
                continue
            if p["name"] == ent + "_id" and earlier:
                continue
            if stated(ulines, p["name"], ent):
                continue
            if p["default"] is not None and dok:
                continue
            miss.append(p["name"])
        return letter_for(P["opts"], "ASK" if miss else "CALL")
    if kind == "reference":
        raise Abstain("reference_form")
    miss, _ = required_unsourced(P, tool, ulines, dok)
    return letter_for(P["opts"], "ASK" if miss else "CALL")


def solve_s3(P, text):
    dok = card_flags(P["head"])
    if dok is None:
        raise Abstain("card_unrecognised")
    ulines = user_lines(P["conv"])
    req = request_of(ulines)
    kind, info = req_kind(req)
    if kind not in ("act",):
        raise Abstain("s3_request_form")
    tool, amb = target_present(P, kind, info)
    if tool is None:
        return letter_for(P["opts"], "NO_TOOL")
    if amb:
        raise Abstain("several_candidate_tools")
    pm = re.search(r"\(the ([\w ]+?) from the earlier lookup\)", req)
    prior_param = pm.group(1).replace(" ", "_") if pm else None
    calls = agent_calls(P["conv"])
    prior_ok = any(out and prior_param in out for (_, _, out) in calls) if prior_param else True
    miss, rmiss = required_unsourced(P, tool, ulines, dok, prior_param, prior_ok)
    if rmiss:
        return letter_for(P["opts"], "RESULT_MISSING")
    return letter_for(P["opts"], "ASK" if miss else "CALL")


def _done_like(verb, w):
    """True: the shown state word is the wanted state of `verb`; False: it is not; None: the text alone cannot tell (the engine's
    wanted-state word is a convention, e.g. a restore ends in a generic word, a send in 'sent')."""
    w = w.lower()
    v = verb.lower()
    if v in ("delete", "remove"):
        return {"absent": True, "present": False}.get(w)
    if v in ("create", "add"):
        return {"present": True, "absent": False}.get(w)
    if w in ("absent", "present"):
        return None
    if v in ("restore", "send", "copy", "sync", "import", "export"):
        return True if w.startswith(v[:4]) and v not in ("send",) else None
    for stem in (v, grp(v)):
        cp = 0
        for a, b in zip(w, stem):
            if a != b:
                break
            cp += 1
        if cp >= min(3, len(stem)):
            return True
    return False


def solve_s4(P, text):
    dok = card_flags(P["head"])
    if dok is None:
        raise Abstain("card_unrecognised")
    ulines = user_lines(P["conv"])
    req = request_of(ulines)
    kind, info = req_kind(req)
    if kind != "act":
        raise Abstain("s4_request_form")
    ent, verb = info["entity"], info["verb"]
    W = [t for t in P["tools"].values() if t["entity"] == ent and t["group"] == grp(verb) and t["rw"] == "write"]
    if len(W) != 1:
        raise Abstain("write_tool_not_unique_or_absent")
    W = W[0]
    miss, _ = required_unsourced(P, W, ulines, dok)
    m = re.search(r"with " + re.escape(ent) + r" id (\S+?)(?:,|\.|\?| please|$)", req)
    ref = m.group(1) if m else None
    state = "unobserved"
    for (tname, args, out) in agent_calls(P["conv"]):
        t = P["tools"].get(tname)
        if t and t["entity"] == ent and t["rw"] == "read" and out and "state" in out and (ref is None or ref in args.values()):
            dl = _done_like(verb, out["state"])
            if dl is None:
                raise Abstain("state_word_vs_action_unknown")
            state = "observed_true" if dl else "observed_false"
    if state == "observed_true":
        return letter_for(P["opts"], "DONE_NO_CALL")
    if state == "observed_false":
        return letter_for(P["opts"], "ASK" if miss else "WRITE")
    if W["idempotent"]:
        return letter_for(P["opts"], "WRITE")
    readers = [t for t in P["tools"].values() if t["rw"] == "read" and t["entity"] == ent]
    return letter_for(P["opts"], "READ_FIRST" if readers else "ASK")


def solve_s2(P, text):
    ulines = user_lines(P["conv"])
    req = request_of(ulines)
    kind, info = req_kind(req)
    if kind != "act":
        raise Abstain("s2_request_form")
    hits = []
    for l, t in P["opts"].items():
        m = re.match(r"^(\w+)\(", t)
        tool = P["tools"].get(m.group(1)) if m else None
        if tool is None:
            raise Abstain("option_tool_not_listed")
        if tool["entity"] == info["entity"] and tool["group"] == grp(info["verb"]):
            # parameter-schema coverage: every required parameter is stated in the request (or lists a default)
            if all((not q["required"]) or q["default"] is not None or stated(ulines, q["name"], tool["entity"])
                   for q in tool["params"]):
                hits.append(l)
    if len(hits) != 1:
        raise Abstain("s2_options_ambiguous")
    return hits[0]


def solve_s5(P, text):
    dok = card_flags(P["head"])
    if dok is None:
        raise Abstain("card_unrecognised")
    m = re.search(r"\n\nProposed call: (\w+)\((.*)\)\s*$", P["conv"] + "\n\nQuestion:" and text.split("\n\nQuestion:")[0], re.S) \
        or re.search(r"Proposed call: (\w+)\((.*)\)", text)
    if not m:
        raise Abstain("no_proposed_call")
    tname = m.group(1)
    args = re.findall(r'(\w+)="((?:[^"\\]|\\.)*)"', m.group(2))
    tool = P["tools"].get(tname)
    if tool is None:
        raise Abstain("proposed_tool_not_listed")
    conv_main = P["conv"].split("\n\nProposed call:")[0]
    ulines = user_lines(conv_main)
    calls = agent_calls(conv_main)
    conv_decl = re.findall(r"Declared conversion: (\w+) to (\w+), multiply by (\d+)", P["head"])
    unit_pairs = [(a, b, int(f)) for (a, b, f) in conv_decl]

    def user_values(param):
        vals = []
        for ln in ulines:
            for mm in re.finditer(r"\buses " + re.escape(pwords(param)) + r" (.*?)\.(?=\s|$)", ln):
                vals.append(mm.group(1))
            for mm in re.finditer(r'\bwith ' + re.escape(pwords(param)) + r' ("[^"]*"|[^,?]*?)(?=,|\?|\.\s|$)', ln):
                vals.append(mm.group(1))
        return [v.strip('"') if v.startswith('"') else v for v in vals]

    def out_values(param):
        return [out[param] for (_, _, out) in calls if out and param in out]

    def norm(v):
        return v.strip().lower()

    for (param, val) in args:
        sources = user_values(param) + out_values(param)
        ok = any(val == s for s in sources)
        if not ok:
            p = [q for q in tool["params"] if q["name"] == param]
            if p and p[0]["default"] is not None and p[0]["default"] == val and dok:
                ok = True
        if not ok:
            for s in sources:
                if norm(s) == norm(val):          # case / whitespace transform
                    ok = True
                    break
                parts = s.split()
                if len(parts) == 2 and re.match(r"^-?\d+(\.\d+)?$", parts[0]):
                    for (a, b, f) in unit_pairs:
                        # the unit words in the card are full words, the user text uses the same word
                        if parts[1].lower().startswith(a[:3].lower()) and float(parts[0]) * f == float(val):
                            ok = True
                if norm(s) in _ORD and _ORD[norm(s)] == norm(val):
                    ok = True
                if norm(val) in _ORD and _ORD[norm(val)] == norm(s):
                    ok = True
        if not ok:
            return letter_for(P["opts"], "UNGROUNDED")
    return letter_for(P["opts"], "GROUNDED")


def _split_and(s):
    out, cur, q = [], "", False
    i = 0
    while i < len(s):
        ch = s[i]
        if ch == '"':
            q = not q
        if not q and s.startswith(" and ", i):
            out.append(cur)
            cur = ""
            i += 5
            continue
        cur += ch
        i += 1
    out.append(cur)
    return out


def solve_s6(P, text):
    conv = P["conv"]
    done_m = re.search(r"Steps already done:\n(.*?)(?=Steps still to run:)", conv, re.S)
    todo_m = re.search(r"Steps still to run:\n(.*)$", conv, re.S)
    if not todo_m:
        raise Abstain("no_todo_steps")
    done_steps = {}
    if done_m:
        for mm in re.finditer(r"^Step (\d+): (\w+)\(", done_m.group(1), re.M):
            done_steps[int(mm.group(1))] = mm.group(2)
    todo = {}
    for mm in re.finditer(r"^Step (\d+): (\w+)\((.*?)\)(?: \[also available as \w+\])?\s*$", todo_m.group(1), re.M):
        todo[int(mm.group(1))] = (mm.group(2), [int(x) for x in re.findall(r"<result of step (\d+)>", mm.group(3))])
    memo = {}

    def depth(s):
        if s not in memo:
            deps = [d for d in todo[s][1] if d in todo]
            memo[s] = 0 if not deps else 1 + max(depth(d) for d in deps)
        return memo[s]

    ready = [s for s in todo if depth(s) == 0]

    def gkey(tname):
        t = P["tools"].get(tname)
        if t is None:
            raise Abstain("step_tool_not_listed")
        return (t["group"], t["entity"])

    want = sorted(set(gkey(todo[s][0]) for s in ready))
    hits = []
    for l, t in P["opts"].items():
        names = []
        for part in _split_and(t):
            mm = re.match(r"^\s*(\w+)\(", part)
            if not mm:
                raise Abstain("s6_option_syntax")
            names.append(mm.group(1))
        if sorted(set(gkey(n) for n in names)) == want:
            hits.append(l)
    if len(hits) != 1:
        raise Abstain("s6_options_ambiguous")
    return hits[0]


_SB = {"s1_need4": solve_s1, "s2_pick": solve_s2, "s3_limit": solve_s3, "s4_precond": solve_s4, "s5_argground": solve_s5,
       "s6_parseq": solve_s6}


def solve_text(sub_block, text):
    """Returns ('letter', X) or ('abstain', code)."""
    try:
        P = parse(text)
        return ("letter", _SB[sub_block](P, text))
    except Abstain as e:
        return ("abstain", str(e))
