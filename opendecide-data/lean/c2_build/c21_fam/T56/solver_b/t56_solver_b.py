"""T56 SOLVER B (independent): a VISIBLE-EVIDENCE-ONLY evaluator. Written from G0_LITE.md sections 2-3 (gold, fault manifest, the fixed
reason precedence, matched-pair rules) and the Opus addendum E1-E6 only, never from solver A code and never from a record's hidden
state. Standard library only.

Input: the RENDERED text of one row (a string). It parses the policy line, task statement (acceptance criteria, optional markers,
declared scope), the trajectory (calls and their outputs), the closing claim, the question and the lettered options, then decides
DONE/CONTINUE (or READY/NOT_READY for the commit question) plus the reason from the text alone.

Evidence conditions (G0-lite section 3.2 / addendum E1-E6), evaluated against the LAST check on the deliverable:
  E1 present   a check/verify call exists                                  -> else unverified
  E3 on target the check's `target` equals the deliverable                 -> else wrong_target
  E4 fresh     snapshot_rev >= last mutation rev of the checked thing      -> else stale_evidence
               (D4 commit question: the last full check follows the last edit of any kind)
  E5/E6 covers every non-optional entity criterion has an item line that passes; `checked` count not below the number of
               required criteria; a required item reported skipped is not covered -> else short_coverage
  unmet        an item/test/summary shows a failure                         -> unmet_criterion
  ledger       every exactly-once criterion matches exactly one ledger effect -> else ledger_mismatch
  reach        the tested symbol is reachable from the entrypoint (imports wired, guards on, calls present) -> else dead_or_demo_only
  scope (D4)   no listed path outside the declared scope                   -> else stray_change
Precedence of the reason: unverified > unmet_criterion > wrong_target > stale_evidence > stray_change > short_coverage >
ledger_mismatch > dead_or_demo_only  (stray_change sits after stale_evidence, G0-lite 3.2).
Reachability uses a depth-first search (the G0-lite P-20 pairs the symbolic gold with an independent graph search).
API: solve_text(text) -> Result(label, reason, letter, reasons_all, flags, abstain)
"""
import re

PRECEDENCE = ["unverified", "unmet_criterion", "wrong_target", "stale_evidence", "stray_change", "short_coverage", "ledger_mismatch",
              "dead_or_demo_only"]
MUTATING = ("create", "add", "update", "set", "remove", "delete", "move", "rename", "send", "export", "sync", "stage", "commit")


class Result(object):
    __slots__ = ("label", "reason", "letter", "reasons_all", "flags", "abstain")

    def __init__(self, label=None, reason=None, letter=None, reasons_all=None, flags=None, abstain=None):
        self.label, self.reason, self.letter = label, reason, letter
        self.reasons_all, self.flags, self.abstain = list(reasons_all or []), list(flags or []), abstain

    def __repr__(self):
        return "Result(%r,%r,%r,all=%r,flags=%r,abstain=%r)" % (self.label, self.reason, self.letter, self.reasons_all, self.flags,
                                                                 self.abstain)


class Abstain(Exception):
    pass


# ------------------------------------------------------------------------------------------------------------ wording lexicon
# The production wording pool holds >= 50 wordings per form, far more than the keyword rules below were written for. `set_lexicon`
# injects the pool ({form id: [templates with {slot} fields]}) as DATA: a wording is then recognised by an exact match of the
# rendered sentence against the pool's templates (slots captured by pattern), and the decision still comes only from the visible
# facts. Without a lexicon (the default) only the keyword rules run. A sentence matching templates of two different forms is
# ambiguous and abstains. Standard library only; the dict is passed in, never read from a file here.
_LEX = {}
_RX = {}
_SLOT_RE = {"item": r"[\w.\-]+", "value": r"[\w.\-]+", "field": r"\w+", "entity": r"\w+", "scope": r"\w+", "criteria": r".+"}


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


def lex_find(forms, text, merge=None):
    """-> (form, slots) when the sentence matches the templates of one of `forms`; None when it matches none. Two forms matching the
    same sentence is ambiguous (Abstain), unless `merge` maps both to the SAME class (forms the evidence rules cannot tell apart,
    e.g. 'X carries status V' as a status or as a field value): the first form in `forms` order then wins."""
    hits = {}
    for f in forms:
        for tpl in _LEX.get(f, ()):
            m = _rx(tpl).match(text)
            if m:
                hits.setdefault(f, m.groupdict())
                break
    if len(set((merge or {}).get(f, f) for f in hits)) > 1:
        raise Abstain("wording_ambiguous:" + ",".join(sorted(hits)))
    for f in forms:
        if f in hits:
            return f, hits[f]
    return None


# ------------------------------------------------------------------------------------------------------------------ parsing
_ID = r"[a-z]{3}-\d+"


def parse_task(text):
    m = re.search(r"Task statement:\n(.*?)\n\nTrajectory:", text, re.S)
    if not m:
        raise Abstain("no_task_statement")
    t = m.group(1)
    lx = lex_find(["task.all"], t) if _LEX else None
    if lx is not None:
        entity, crit_text, scope = lx[1]["entity"], lx[1]["criteria"], lx[1]["scope"]
    else:
        me = re.match(r"Task: (?:finish|complete) the (\w+) (?:work|change)\.", t)
        if not me:
            raise Abstain("task_header")
        entity = me.group(1)
        mc = re.search(r"(?:Acceptance criteria|It is done when): (.*?)\. (?:Only files under|Changes are allowed only under) (\w+)", t, re.S)
        if not mc:
            raise Abstain("criteria_block")
        scope, crit_text = mc.group(2), mc.group(1)
    items = re.split(r"(?:^|; )\d+\) ", crit_text)
    items = [i.strip() for i in items if i.strip()]
    crits = []
    for it in items:
        optional = it.endswith("(optional)")
        body = it[: -len("(optional)")].strip() if optional else it
        crits.append(classify_criterion(body, optional))
    return dict(entity=entity, scope=scope, criteria=crits)


_CRIT_FORMS = ["crit." + p for p in ("status_is", "equals", "exists", "absent", "count_eq", "unchanged", "exactly_once", "reachable")]
# the evidence rules read a store criterion only through its item id, so these five are one class for ambiguity purposes
_CRIT_CLASS = dict([("crit." + p, "item") for p in ("status_is", "equals", "exists", "absent", "unchanged")] +
                   [("crit.count_eq", "count"), ("crit.exactly_once", "ledger"), ("crit.reachable", "reach")])


def classify_criterion(body, optional):
    lx = lex_find(_CRIT_FORMS, body, _CRIT_CLASS) if _LEX else None
    if lx is not None:
        pred, sl = lx[0][len("crit."):], lx[1]
        if pred == "exactly_once":
            return dict(kind="ledger", key=sl["item"], optional=optional)
        if pred == "reachable":
            mod, _, sym = sl["value"].partition(".")
            return dict(kind="reach", module=mod, symbol=sym, entry=sl["item"], optional=optional)
        if pred == "status_is" and sl["value"] == "pass" and sl["item"].startswith("tst-"):
            return dict(kind="test", key=sl["item"], optional=optional)
        if pred == "count_eq":
            return dict(kind="item", key="entries", optional=optional)
        return dict(kind="item", key=sl["item"], optional=optional)
    m = re.match(r"^(" + _ID + r") (?:receives the notice exactly once|gets exactly one notice)$", body)
    if m:
        return dict(kind="ledger", key=m.group(1), optional=optional)
    m = re.match(r"^(?:the )?(\w+)\.(\w+) (?:runs when (\w+)\.run is run|is used by the (\w+)\.run entrypoint)$", body)
    if m:
        return dict(kind="reach", module=m.group(1), symbol=m.group(2), entry=(m.group(3) or m.group(4)) + ".run", optional=optional)
    m = re.match(r"^(?:the status of (tst-\d+) is pass|(tst-\d+) has status pass)$", body)
    if m:
        return dict(kind="test", key=m.group(1) or m.group(2), optional=optional)
    if re.match(r"^(?:the \w+ list holds exactly \d+ entries|there are exactly \d+ \w+ entries)$", body):
        return dict(kind="item", key="entries", optional=optional)
    m = re.search(r"(" + _ID + r")", body)
    if m:
        return dict(kind="item", key=m.group(1), optional=optional)
    return dict(kind="unknown", key=body, optional=optional)


def parse_calls(text):
    m = re.search(r"Trajectory:\n(.*?)\n\nAgent's closing message:", text, re.S)
    if not m:
        raise Abstain("no_trajectory")
    lines = m.group(1).split("\n")
    calls, cur = [], None
    for ln in lines:
        mc = re.match(r"^Agent called (\w+)\((.*)\)$", ln)
        if mc:
            name = mc.group(1)
            verb, _, ent = name.partition("_")
            cur = dict(name=name, verb=verb, entity=ent, args=mc.group(2), out=[], idx=len(calls))
            calls.append(cur)
        elif ln.startswith("     ") and cur is not None:
            k, _, v = ln.strip().partition(": ")
            cur["out"].append((k, v))
    for c in calls:
        c["kv"] = dict((k, v) for k, v in c["out"])
    return calls


def question_kind(text):
    m = re.search(r"\n\nQuestion: (.*?)\n", text)
    if not m:
        raise Abstain("no_question")
    if _LEX:
        lx = lex_find(["q.ready", "q.done"], m.group(1))
        if lx is not None:
            return "ready" if lx[0] == "q.ready" else "done"
    return "ready" if "commit" in m.group(1).lower() else "done"


def option_label(opt_text, qkind):
    if _LEX:
        lx = lex_find(["opt.READY", "opt.NOT_READY", "opt.DONE", "opt.CONTINUE"], opt_text)
        if lx is not None:
            return lx[0][len("opt."):]
    s = opt_text.lower()
    neg = s.startswith("no") or "do not accept" in s or "must not" in s or "not ready" in s
    if qkind == "ready":
        return "NOT_READY" if neg else "READY"
    return "CONTINUE" if neg else "DONE"


def parse_options(text):
    opts = {}
    for ln in text.split("\n"):
        m = re.match(r"^([A-Z])\) (.*)$", ln)
        if m:
            opts[m.group(1)] = m.group(2)
    return opts


def _int(x):
    try:
        return int(x)
    except (TypeError, ValueError):
        return None


# ---------------------------------------------------------------------------------------------------------- evidence rules
def _reachable(out, entry, module, symbol, flags):
    imports = set()
    flagdef = {}
    edges = []
    ep = None
    for k, v in out:
        if k == "entrypoint":
            ep = v.strip()
        elif k in ("import", "source"):
            m = re.match(r"^(\S+) -> (\S+)$", v.strip())
            if m:
                imports.add((m.group(1).rsplit(".", 1)[0], m.group(2).rsplit(".", 1)[0]))
        elif k == "flag":
            m = re.match(r"^(\w+) default=(on|off)$", v.strip())
            if m:
                flagdef[m.group(1)] = m.group(2) == "on"
        elif k == "call":
            m = re.match(r"^(\S+) -> (\S+) guard=(none|never|flag (\w+))$", v.strip())
            if m:
                edges.append((m.group(1), m.group(2), m.group(3), m.group(4)))
    if ep is None:
        flags.append("no_entrypoint_line")
        return None
    target = module + "." + symbol

    def edge_open(a, b, g, fl):
        if g == "never":
            return False
        if g.startswith("flag") and not flagdef.get(fl, False):
            return False
        ma, mb = a.split(".")[0], b.split(".")[0]
        if ma != mb and (ma, mb) not in imports:
            return False        # the import is not wired
        return True

    seen = set()

    def dfs(node):
        if node == target:
            return True
        seen.add(node)
        for (a, b, g, fl) in edges:
            if a == node and b not in seen and edge_open(a, b, g, fl):
                if dfs(b):
                    return True
        return False

    return dfs(ep)


def _ledger_count(out, who):
    n = 0
    for k, v in out:
        if k.startswith("effect") and re.search(r"=" + re.escape(who) + r"(?:,|$)", v):
            n += 1
    return n


def evaluate(text):
    flags = []
    task = parse_task(text)
    calls = parse_calls(text)
    qk = question_kind(text)
    ent = task["entity"]
    reasons = set()
    checks = [c for c in calls if c["verb"] in ("check", "verify")]
    muts = [(c, _int(c["kv"].get("rev"))) for c in calls if c["verb"] in MUTATING]
    ledgers = [c for c in calls if c["verb"] == "ledger"]
    runs = [c for c in calls if c["verb"] == "run"]
    inspects = [c for c in calls if c["verb"] == "inspect"]
    statuses = [c for c in calls if c["verb"] == "status"]

    # E1
    if not checks:
        reasons.add("unverified")
    else:
        last = checks[-1]
        kv = last["kv"]
        # E3
        if kv.get("target") != ent:
            reasons.add("wrong_target")
        # E4
        snap = _int(kv.get("snapshot_rev"))
        if qk == "ready":
            rel = [r for (c, r) in muts if r is not None]
        else:
            rel = [r for (c, r) in muts if r is not None and c["entity"] == ent]
        if snap is None:
            flags.append("snapshot_missing")
        elif rel and snap < max(rel):
            reasons.add("stale_evidence")
        # E5 / E6 and unmet
        items = {}
        for k, v in last["out"]:
            mi = re.match(r"^item\[\d+\]$", k)
            if mi:
                mm = re.match(r"^(\S+) (pass|fail|skipped)(?: \(optional\))?$", v.strip())
                if mm:
                    items[mm.group(1)] = mm.group(2)
                else:
                    flags.append("item_line_unparsed")
        required = [c for c in task["criteria"] if c["kind"] == "item" and not c["optional"]]
        for c in required:
            st = items.get(c["key"])
            if st is None or st == "skipped":
                reasons.add("short_coverage")
            elif st == "fail":
                reasons.add("unmet_criterion")
        if any(st == "fail" for st in items.values()):
            reasons.add("unmet_criterion")
        chk = _int(kv.get("checked"))
        if chk is not None and chk < len(required):
            reasons.add("short_coverage")
        if _int(kv.get("failed")) not in (None, 0):
            reasons.add("unmet_criterion")

    # tests
    for c in [x for x in task["criteria"] if x["kind"] == "test"]:
        if not runs:
            reasons.add("unverified")
            continue
        kvr = runs[-1]["kv"]
        failed = _int(kvr.get("fail", kvr.get("failed")))
        passed = _int(kvr.get("pass", kvr.get("passed")))
        ex = _int(kvr.get("exit_status"))
        res_word = kvr.get("result")
        if (failed not in (None, 0)) or (ex not in (None, 0)) or (res_word is not None and res_word.strip().lower() != "ok"):
            reasons.add("unmet_criterion")
        elif passed is None and ex is None and res_word is None:
            flags.append("run_output_unparsed")

    # ledger
    for c in [x for x in task["criteria"] if x["kind"] == "ledger"]:
        if not ledgers:
            reasons.add("unverified")
            continue
        if _ledger_count(ledgers[-1]["out"], c["key"]) != 1:
            reasons.add("ledger_mismatch")

    # reachability
    for c in [x for x in task["criteria"] if x["kind"] == "reach"]:
        if not inspects:
            reasons.add("unverified")
            continue
        r = _reachable(inspects[-1]["out"], c["entry"], c["module"], c["symbol"], flags)
        if r is False:
            reasons.add("dead_or_demo_only")
        elif r is None:
            flags.append("reach_unevaluable")

    # declared scope (commit question)
    if statuses:
        for k, v in statuses[-1]["out"]:
            if k.startswith("path["):
                mm = re.match(r"^(\S+) (modified|untracked|staged|deleted)$", v.strip())
                if mm and not (mm.group(1).startswith(task["scope"] + "/") or mm.group(1) == task["scope"]):
                    reasons.add("stray_change")
    elif qk == "ready":
        flags.append("ready_question_without_status_call")

    return task, qk, reasons, flags


def solve_text(text):
    try:
        task, qk, reasons, flags = evaluate(text)
        opts = parse_options(text)
    except Abstain as e:
        return Result(abstain=str(e))
    if not reasons:
        label, reason = ("READY" if qk == "ready" else "DONE"), "none"
    else:
        label = "NOT_READY" if qk == "ready" else "CONTINUE"
        reason = [r for r in PRECEDENCE if r in reasons][0]
    letters = [l for l, t in opts.items() if option_label(t, qk) == label]
    letter = letters[0] if len(letters) == 1 else None
    return Result(label=label, reason=reason, letter=letter, reasons_all=[r for r in PRECEDENCE if r in reasons], flags=flags)


def solve(record):
    """Convenience: reads ONLY record['rendered']['text'] (no stored label, no hidden state)."""
    return solve_text(record["rendered"]["text"])
