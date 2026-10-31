"""T55 SOLVER B, RENDER-FIDELITY / OBSERVABILITY PARSER (G0-lite 3.3 and addendum P-10: "B's parser recovers every fact the label needs
from the rendered row"). Standard library only. Input: the rendered text of ONE row. Output: ('letter', X) or ('abstain', code). It sees
no record, no stored label, and no hidden ledger world. An abstain is "the text does not carry what the rule needs" (counted by the
harness as an observability drop), not a disagreement.

Rules are the G0-lite 3.2 tables with the Opus C1 (B3) and C2 (B6) orders. Where a rule needs a fact the generator keeps in the record,
this parser re-derives it from the text: error class from the status token / code / phrase (all present channels must agree), tool
read/write/idempotent flags from the tool list, the key from the call arguments, equivalent tools from (entity, verb group), the retry
cap and escalation table from the card, the corrected value from the user's own clause, and the invariant context (stated count,
prior ids, reference value, prior / intended arguments) from the earlier outputs and the user turn.
Verb groups (add=create, delete=remove, lookup=read=get, search=find, set=update) are the engine's group convention as observed on
`group` ids; the G0-lite says only that equivalence groups exist.
"""
import re

_GROUP = {"add": "create", "delete": "remove", "lookup": "get", "read": "get", "search": "find", "set": "update"}
_STATUS_GROUP = {"error_temp": "temp", "error_rate": "rate", "error_auth": "auth", "error_arg": "arg", "error_unsup": "unsup",
                 "error_quota": "quota", "error_fatal": "fatal"}
_CODE_GROUP = {"1": "temp", "2": "rate", "3": "auth", "4": "arg", "5": "unsup", "6": "quota", "7": "fatal"}
_PHRASE_GROUP = {"temporarily unavailable": "temp", "dependency timed out": "temp", "backend not ready": "temp",
                 "request rate exceeded": "rate", "too many calls in the window": "rate", "rate cap reached": "rate",
                 "credentials not accepted": "auth", "permission missing for this operation": "auth", "access denied": "auth",
                 "argument rejected": "arg", "request failed validation": "arg", "malformed argument": "arg",
                 "operation not supported": "unsup", "unsupported operation for this object": "unsup",
                 "usage quota exhausted": "quota", "allowance used up": "quota",
                 "target no longer exists": "fatal", "object permanently removed": "fatal", "goal cannot be met": "fatal"}


class Abstain(Exception):
    pass


# ------------------------------------------------------------------------------------------------------------ wording lexicon
# The production wording pool holds >= 50 wordings per form (cards, options, error phrases), far more than the keyword rules below were
# written for. `set_lexicon` injects the pool ({form id: [templates with {slot} fields]}) as DATA: a sentence is recognised by an exact
# match against the pool's templates (slots captured by pattern); every decision still comes from the facts in the rendered row. Without
# a lexicon only the keyword rules run. Standard library only; the dict is passed in, never read from a file here.
_LEX = {}
_RX = {}
_SLOT_RE = {"kc": r"\d+", "kt": r"\d+", "kw": r"\d+", "w": r"\d+", "pcap": r"\d+", "lim": r"\d+",
            "quota": r"(?:ask the user|stop)", "unsupp": r"(?:ask the user|stop)", "nw": r"(?:can|cannot)", "trans": r".+?"}


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


# the two escalation-table forms carry the SAME sentences (the table's values travel in the {quota} / {unsupp} slots, not in the form id)
_SAME_CLASS = {"card.card.t55.escalate_table_ask": "escalate_table", "card.card.t55.escalate_table_stop": "escalate_table"}


def lex_line(forms, line):
    """-> (form, slots) when the line matches a template of one of `forms`; None when none; Abstain when two different forms match
    (forms in _SAME_CLASS count as one)."""
    hits = {}
    for f in forms:
        for tpl in _LEX.get(f, ()):
            m = _rx(tpl).match(line)
            if m:
                hits.setdefault(f, m.groupdict())
                break
    if len(set(_SAME_CLASS.get(f, f) for f in hits)) > 1:
        raise Abstain("wording_ambiguous:" + ",".join(sorted(hits)))
    return next(iter(hits.items())) if hits else None


def head_cards(head):
    """{card form id: slots} for every line of the policy block that is a pool card sentence (lexicon mode only)."""
    out = {}
    if not _LEX:
        return out
    forms = [f for f in _LEX if f.startswith("card.")]
    for ln in head.split("\n"):
        lx = lex_line(forms, ln.strip())
        if lx is not None:
            out[lx[0]] = lx[1]
    return out


def grp(v):
    return _GROUP.get(v, v)


def parse(text):
    if "\n\nTools:\n" not in text or "\n\nConversation:\n" not in text or "\n\nQuestion:" not in text:
        raise Abstain("layout")
    head, rest = text.split("\n\nTools:\n", 1)
    tools_block, rest = rest.split("\n\nConversation:\n", 1)
    conv, qa = rest.split("\n\nQuestion:", 1)
    opts = {}
    for ln in qa.split("\n")[1:]:
        m = re.match(r"^([A-Z])\) (.*)$", ln)
        if m:
            opts[m.group(1)] = m.group(2)
    tools = {}
    for ln in tools_block.split("\n"):
        m = re.match(r"^- (\w+)\((.*)\) \[(.*?)\] -- (.*)$", ln)
        if m:
            verb, _, ent = m.group(1).partition("_")
            flags = [f.strip() for f in m.group(3).split(",")]
            tools[m.group(1)] = dict(name=m.group(1), verb=verb, entity=ent, group=grp(verb), rw=flags[0],
                                     idem="idempotent" in flags, params=m.group(2))
    return dict(head=head, tools=tools, conv=conv, opts=opts, text=text)


def parse_calls(conv):
    """[(name, {arg: value}, out-lines list or None)] ; out None = no output block."""
    calls = []
    lines = conv.split("\n")
    i = 0
    while i < len(lines):
        m = re.match(r"^Agent called (\w+)\((.*)\)$", lines[i])
        if m:
            args = [(k, v) for k, v in re.findall(r'(\w+)="((?:[^"\\]|\\.)*)"', m.group(2))]
            out = None
            if i + 1 < len(lines) and lines[i + 1].strip().startswith("-> output:"):
                out = []
                j = i + 2
                while j < len(lines) and lines[j].startswith("     "):
                    k, _, v = lines[j].strip().partition(": ")
                    out.append((k, v))
                    j += 1
                i = j - 1
            calls.append((m.group(1), args, out))
        i += 1
    return calls


def kv(out):
    return dict(out or [])


_FAM_LABELS = {"b1": ("RETRY", "FIX_ARGS", "SWITCH_TOOL", "ASK", "STOP"), "b4": ("RETRY", "FIX_ARGS", "SWITCH_TOOL", "ASK", "STOP"),
               "b3": ("ACCEPT", "RETRY", "FIX_ARGS", "SWITCH_TOOL", "ASK"),
               "b2": ("RETRY_KEYED", "READ_BACK", "RETRY_PLAIN", "ASK", "NO_RETRY"),
               "b5": ("CONTINUE_ALT", "ESCALATE", "RETRY_SAME", "STOP"), "b6": ("KEEP_POLLING", "BREAK_LOOP_ALT", "ESCALATE", "STOP")}


def classify_option(t, family):
    if _LEX:
        hit = [lab for lab in _FAM_LABELS.get(family, ()) if t in _LEX.get("opt." + lab, ())]
        if len(hit) == 1:
            return hit[0]
    s = t.lower()
    if family in ("b1", "b4", "b3"):
        if re.search(r"identical call again|same call", s):
            return "RETRY"
        if re.search(r"corrected arguments|correct the argument", s):
            return "FIX_ARGS"
        if re.search(r"different listed tool|equivalent listed tool", s):
            return "SWITCH_TOOL"
        if re.search(r"\bask\b", s):
            return "ASK"
        if re.search(r"give up|report", s):
            return "STOP"
        if re.search(r"use the result as it is|accept the result", s):
            return "ACCEPT"
    if family == "b2":
        if re.search(r"same idempotency key|same write again, same key", s):
            return "RETRY_KEYED"
        if re.search(r"read the state back|took effect", s):
            return "READ_BACK"
        if re.search(r"new attempt|fresh call", s):
            return "RETRY_PLAIN"
        if re.search(r"do not repeat|leave it", s):
            return "NO_RETRY"
        if re.search(r"\bask\b", s):
            return "ASK"
    if family == "b5":
        if re.search(r"another permitted path|different permitted route", s):
            return "CONTINUE_ALT"
        if re.search(r"denied action", s):
            return "RETRY_SAME"
        if re.search(r"escalate|human decision", s):
            return "ESCALATE"
        if re.search(r"give up|report", s):
            return "STOP"
    if family == "b6":
        if re.search(r"keep polling|poll again", s):
            return "KEEP_POLLING"
        if re.search(r"break the loop|another approach", s):
            return "BREAK_LOOP_ALT"
        if re.search(r"escalate|human decision", s):
            return "ESCALATE"
        if re.search(r"give up|report", s):
            return "STOP"
    return None


def letter(P, family, label):
    hits = [l for l, t in P["opts"].items() if classify_option(t, family) == label]
    if len(hits) != 1:
        raise Abstain("option_wording:" + label)
    return hits[0]


def family_of(P):
    t = P["text"]
    if "Denials:" in t and "denied" in t:
        return "b5"
    if "Calls used on this poll" in t:
        return "b6"
    last = parse_calls(P["conv"])
    if any(o and (kv(o).get("status") == "timeout" or kv(o).get("committed") in ("yes", "no")) for (_, _, o) in last):
        return "b2"
    if "Attempts of this call so far" not in t:
        raise Abstain("unknown_family")
    if last and last[-1][2] and str(kv(last[-1][2]).get("status", "")).startswith("error"):
        return "b1"
    if last and last[-1][2] and kv(last[-1][2]).get("status") == "ok":
        return "b3"
    raise Abstain("unknown_family")


def attempts(P):
    m = re.search(r"Attempts of this call so far \(including this one\): (\d+)\.", P["text"])
    if not m:
        raise Abstain("attempts_missing")
    return int(m.group(1))


def cap_of(P):
    cards = head_cards(P["head"])
    for f, cap in (("card.card.t55.retry_cap2", 2), ("card.card.t55.retry_cap3", 3)):
        if f in cards:
            if not re.search(r"(?<!\d)%d(?!\d)" % cap, P["head"]):
                raise Abstain("cap_not_in_text")           # the form says a cap the sentence does not carry
            return cap
    m = re.search(r"fewer than (\d+) attempts", P["head"])
    if not m:
        raise Abstain("cap_missing")
    return int(m.group(1))


def escalation(P):
    cards = head_cards(P["head"])
    for f in ("card.card.t55.escalate_table_ask", "card.card.t55.escalate_table_stop"):
        if f in cards:
            sl = cards[f]
            fx = lambda s: "ASK" if "ask" in s.lower() else ("STOP" if "stop" in s.lower() else None)       # noqa: E731
            return {"quota_exhausted": fx(sl["quota"]), "unsupported_op": fx(sl["unsupp"])}
    m = re.search(r"Escalation table: quota exhausted -> ([^;]+); unsupported operation -> ([^;]+); target destroyed", P["head"])
    if not m:
        return {}
    f = lambda s: "ASK" if "ask" in s.lower() else ("STOP" if "stop" in s.lower() else None)
    return {"quota_exhausted": f(m.group(1)), "unsupported_op": f(m.group(2))}


def user_lines(conv):
    return [ln[len("User: "):] for ln in conv.split("\n") if ln.startswith("User: ")]


def equivalent_listed(P, tool):
    return any(t["entity"] == tool["entity"] and t["group"] == tool["group"] and t["name"] != tool["name"] for t in P["tools"].values())


# ------------------------------------------------------------------------------------------------------------------ B1 / B4
def solve_b1(P, fam):
    calls = parse_calls(P["conv"])
    name, args, out = calls[-1]
    tool = P["tools"].get(name)
    if tool is None:
        raise Abstain("call_tool_not_listed")
    o = kv(out)
    groups = set()
    if o.get("status") in _STATUS_GROUP:
        groups.add(_STATUS_GROUP[o["status"]])
    if o.get("code"):
        c = _CODE_GROUP.get(o["code"][1:2])
        if c:
            groups.add(c)
    if o.get("detail") in _PHRASE_GROUP:
        groups.add(_PHRASE_GROUP[o["detail"]])
    elif _LEX and o.get("detail"):
        hit = [f[len("phrase."):] for f in _LEX if f.startswith("phrase.") and o["detail"] in _LEX[f]]
        if len(hit) == 1:
            groups.add(hit[0])
    if "retry_after" in o and not groups:
        groups.add("rate")
    if len(groups) != 1:
        raise Abstain("error_class_not_unique:%d" % len(groups))
    g = groups.pop()
    a, cap = attempts(P), cap_of(P)
    eq = equivalent_listed(P, tool)
    keyed = any(k == "idempotency_key" for k, _ in args)
    safe = tool["rw"] == "read" or tool["idem"] or keyed
    esc = escalation(P)
    if g in ("temp", "rate"):
        if not safe:
            raise Abstain("non_idempotent_write_without_key_is_b2")
        if a < cap:
            return letter(P, fam, "RETRY")
        return letter(P, fam, "SWITCH_TOOL" if eq else "ASK")
    if g == "arg":
        field = o.get("field")
        if field:
            pw = field.replace("_", " ")
            cur = dict(args).get(field)
            have = []
            for ln in user_lines(P["conv"]):
                # a value runs to the next space, comma or question mark ('.' belongs to it only inside a number): the pool's request
                # wordings continue after the clauses ('... with name abc-12 for me?'), so a terminator-only pattern missed them
                for m in re.finditer(r"\bwith " + re.escape(pw) + r" ((?:[^\s,?.]|\.(?=\d))+)", ln):
                    have.append(m.group(1))
            ok = [v for v in have if v != cur]
            return letter(P, fam, "FIX_ARGS" if ok else "ASK")
        return letter(P, fam, "SWITCH_TOOL" if eq else "ASK")
    if g == "auth":
        return letter(P, fam, "ASK")
    if g == "unsup":
        if eq:
            return letter(P, fam, "SWITCH_TOOL")
        if esc.get("unsupported_op") is None:
            raise Abstain("escalation_table")
        return letter(P, fam, esc["unsupported_op"])
    if g == "quota":
        if eq:
            return letter(P, fam, "SWITCH_TOOL")
        if esc.get("quota_exhausted") is None:
            raise Abstain("escalation_table")
        return letter(P, fam, esc["quota_exhausted"])
    if g == "fatal":
        return letter(P, fam, "STOP")
    raise Abstain("class")


# --------------------------------------------------------------------------------------------------------------------- B2
def solve_b2(P, fam):
    calls = parse_calls(P["conv"])
    wr = [c for c in calls if c[2] is not None and kv(c[2]).get("status") == "timeout"]
    if not wr:
        raise Abstain("no_timeout_write")
    name, args, _ = wr[-1]
    tool = P["tools"].get(name)
    if tool is None:
        raise Abstain("call_tool_not_listed")
    rb = [c for c in calls if c[2] is not None and kv(c[2]).get("committed") in ("yes", "no")]
    if rb:
        return letter(P, fam, "NO_RETRY" if kv(rb[-1][2])["committed"] == "yes" else "RETRY_PLAIN")
    keyed = any(k == "idempotency_key" for k, _ in args) or tool["idem"]
    if keyed:
        return letter(P, fam, "RETRY_KEYED")
    rp = any(t["rw"] == "read" and t["entity"] == tool["entity"] for t in P["tools"].values())
    return letter(P, fam, "READ_BACK" if rp else "ASK")


# --------------------------------------------------------------------------------------------------------------------- B3
def _num(x):
    try:
        return float(x)
    except (TypeError, ValueError):
        return None


def _detail_args(v):
    return dict(re.findall(r"(\w+)=(\S+)", v))


def solve_b3(P, fam):
    calls = parse_calls(P["conv"])
    name, args, out = calls[-1]
    tool = P["tools"].get(name)
    if tool is None:
        raise Abstain("call_tool_not_listed")
    prior_outs = [kv(o) for (_, _, o) in calls[:-1] if o]
    fin = out or []
    fkv = kv(fin)
    items = None
    if "items" in fkv:
        items = [] if fkv["items"].strip() == "(none)" else [x.strip() for x in fkv["items"].split(",")]
    cargs = dict(args)
    fired, arg_induced = [], False
    # empty when a count was stated
    stated = [_num(p.get("count")) for p in prior_outs if "count" in p]
    if items == [] and any(n is not None and n > 0 for n in stated):
        fired.append("empty")
    # negative value in any plain field
    for k, v in fin:
        if k not in ("status", "count", "items", "total", "detail") and _num(v) is not None and _num(v) < 0:
            fired.append("negative")
    # ids outside the prior list
    prior_ids = None
    for p in prior_outs:
        if "items" in p:
            prior_ids = [x.strip() for x in p["items"].split(",")]
    if items and prior_ids is not None and any(i not in prior_ids for i in items):
        fired.append("id_not_in_prior")
        if any(v not in prior_ids for v in cargs.values()):
            arg_induced = True
    # parts / total
    if items and "total" in fkv:
        nums = [_num(i) for i in items]
        if all(n is not None for n in nums) and abs(sum(nums) - _num(fkv["total"])) > 1e-9:
            fired.append("parts_total")
    # scale mismatch against the same field in an earlier output
    for k, v in fin:
        if k in ("status", "count", "items", "total", "detail") or _num(v) is None:
            continue
        for p in prior_outs:
            if k in p and _num(p[k]) not in (None, 0) and _num(v) != _num(p[k]):
                ratio = _num(v) / _num(p[k])
                if any(abs(ratio - m) < 1e-9 or abs(ratio - 1.0 / m) < 1e-9 for m in (10, 100, 1000, 10000)):
                    fired.append("scale")
                    if k in cargs and _num(cargs[k]) != _num(p[k]):
                        arg_induced = True
    # stale echo
    if "detail" in fkv and "=" in fkv["detail"]:
        echo = _detail_args(fkv["detail"])
        prior_echo = None
        for p in prior_outs:
            if "detail" in p and "=" in p["detail"]:
                prior_echo = _detail_args(p["detail"])
        ul = " ".join(user_lines(P["conv"]))
        mi = re.search(r"I want (.*)$", ul)
        intended = None
        if mi:
            intended = dict(re.findall(r"(\w+) (\S+?)(?: and |$)", mi.group(1).strip().rstrip(".")))
        if prior_echo is not None and echo == prior_echo and intended is not None and echo != intended:
            fired.append("stale")
            if cargs != intended:
                arg_induced = True
    if not fired:
        return letter(P, fam, "ACCEPT")
    if arg_induced:
        return letter(P, fam, "FIX_ARGS")
    a = attempts(P)
    if tool["rw"] == "write":
        return letter(P, fam, "ASK")
    if a == 1:
        return letter(P, fam, "RETRY")
    return letter(P, fam, "SWITCH_TOOL" if equivalent_listed(P, tool) else "ASK")


# --------------------------------------------------------------------------------------------------------------------- B5
def solve_b5(P, fam):
    t = P["text"]
    m = re.search(r"Denials: (\d+) consecutive, (\d+) in total(?:, (\d+) among the last (\d+) calls)?\.", t)
    if not m:
        raise Abstain("denial_counters")
    nc, nt = int(m.group(1)), int(m.group(2))
    nw = int(m.group(3)) if m.group(3) else None
    alt = re.search(r"An alternative permitted path exists: (yes|no)\.", t)
    blk = re.search(r"A fixed rule blocks the goal itself: (yes|no)\.", t)
    if not alt or not blk:
        raise Abstain("denial_state")
    cards = head_cards(P["head"])
    if "card.card.t55.denial_consec_total" in cards:
        sl = cards["card.card.t55.denial_consec_total"]
        kc, kt, kw = int(sl["kc"]), int(sl["kt"]), None
    elif "card.card.t55.denial_window" in cards:
        sl = cards["card.card.t55.denial_window"]
        kc, kt, kw = int(sl["kc"]), None, int(sl["kw"])
    else:
        mk = re.search(r"after (\d+) consecutive denials or (?:(\d+) denials in total|(\d+) denials among the last (\d+) calls)", P["head"])
        if not mk:
            raise Abstain("denial_card")
        kc = int(mk.group(1))
        kt = int(mk.group(2)) if mk.group(2) else None
        kw = int(mk.group(3)) if mk.group(3) else None
    if nc >= kc or (kt is not None and nt >= kt) or (kw is not None and nw is not None and nw >= kw):
        return letter(P, fam, "ESCALATE")
    if blk.group(1) == "yes":
        return letter(P, fam, "STOP")
    if alt.group(1) == "yes":
        return letter(P, fam, "CONTINUE_ALT")
    return letter(P, fam, "ESCALATE")


# --------------------------------------------------------------------------------------------------------------------- B6
def solve_b6(P, fam):
    t = P["text"]
    calls = parse_calls(P["conv"])
    obs = []
    for (_, _, out) in calls:
        d = kv(out)
        obs.append(dict(progress=_num(d.get("progress")), counter=_num(d.get("count")), status=d.get("status")))
    mu = re.search(r"Calls used on this poll: (\d+)\.", t)
    ma = re.search(r"An alternative approach is available: (yes|no)\.", t)
    mp = re.search(r"Polling budget: (\d+) calls\. Loop limit: (\d+) calls in a row without advance\. Declared transitions: (.*?)\. "
                   r"This goal (can|cannot) wait", P["head"])
    cards = head_cards(P["head"])
    if "card.b6" in cards:
        sl = cards["card.b6"]
        pc, lm, tr_, nw_ = sl["pcap"], sl["lim"], sl["trans"], sl["nw"]
    elif mp:
        pc, lm, tr_, nw_ = mp.group(1), mp.group(2), mp.group(3), mp.group(4)
    else:
        pc = None
    if not (mu and ma and pc is not None):
        raise Abstain("poll_state")
    used, alt = int(mu.group(1)), ma.group(1) == "yes"
    pcap, lim = int(pc), int(lm)
    trans = [tuple(x.strip().split("->")) for x in tr_.split(",") if "->" in x]
    nonwait = nw_ == "cannot"

    def adv(a, b):
        if a["progress"] is not None and b["progress"] is not None and b["progress"] > a["progress"]:
            return True
        if a["counter"] is not None and b["counter"] is not None and b["counter"] > a["counter"]:
            return True
        if a["status"] is not None and b["status"] is not None and (a["status"], b["status"]) in trans:
            return True
        return False

    changed = len(obs) >= 2 and adv(obs[-2], obs[-1])
    if changed:
        return letter(P, fam, "KEEP_POLLING" if used < pcap else "ESCALATE")
    k = 0
    for i in range(len(obs) - 1, 0, -1):
        if adv(obs[i - 1], obs[i]):
            break
        k += 1
    if k < lim:
        return letter(P, fam, "KEEP_POLLING")
    if alt:
        return letter(P, fam, "BREAK_LOOP_ALT")
    if nonwait:
        return letter(P, fam, "STOP")
    return letter(P, fam, "ESCALATE")


def solve_text(text):
    try:
        P = parse(text)
        fam = family_of(P)
        fn = {"b1": solve_b1, "b2": solve_b2, "b3": solve_b3, "b5": solve_b5, "b6": solve_b6}[fam]
        return ("letter", fn(P, fam), fam)
    except Abstain as e:
        return ("abstain", str(e), None)
