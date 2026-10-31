"""F12 solver A: the generator's own procedural schema matcher (G0 spec section 3, 5 "Solver A").

Works on the sampled Python structure S (before rendering): tuple equality / set inclusion for match, an ordered walk
over the user's statements for value resolution, hand-written per-constraint accept checks (Decimal, datetime.date),
and an explicit if-chain for the SEM-04 precedence and the card policies.

Structure S (canonical; every key is decisive-relevant and goes into structure_hash):
  pol      {"invalid": "A"|"B", "chain": bool, "tie": bool, "fresh": None|int, "role": bool}
  now      "YYYY-MM-DD HH:MM" (one stated time zone)
  role     user's role (POL-ROLE on) or None
  tools    listed tools in display order (f12lex tool dicts; row copies)
  records  [{"fields": [[key, value], ...]}]   (always about the target entity or a look-alike)
  conv     [{"who": "user", "ts", "st": [statement, ...]} | {"who": "assistant", "ts", "ask": param|None}
            | {"who": "tool", "ts", "tool": name, "fields": [[k, v], ...]}]
  stored   [{"tool": name, "ts", "fields": [[k, v], ...]}]
  call     None | {"tool": name, "args": [[k, v], ...]}   (audit rows)
User statements:
  {"t": "req", "kind": "action"|"info"|"catalog", "cue": "plain"|"polite"|"catalog"|"info", "a", "o",
   "ref": ["id", X] | ["name", N] | None, "field": f | None}
  {"t": "val", "p": param | None (unnamed), "v": text, "alts": [t1, t2] | None (open choice)}
  {"t": "qual", "v": text}            scope qualifier, always stated with the dimension's name
  {"t": "corr"}                       correction cue line (a later value wins anyway, R3-01)
  {"t": "fact", "name": N, "p": key, "v": text}   fact statement about the target entity (earlier turn, R4-02)
  {"t": "cont", "v": text}            continuation answer to the assistant's preceding question
"""
from __future__ import annotations

import datetime as dt
import re
from decimal import Decimal, InvalidOperation

MARK_UNKNOWN = ("not recorded", "unknown")
REL = re.compile(r"^(today|tomorrow|yesterday|in (\d+) days?|(\d+) days? ago|in (\d+) weeks?)$")
NUM = re.compile(r"^(\d+(?:\.\d+)?)(?: ([A-Za-z][A-Za-z/]*))?$")
DATE = re.compile(r"^(\d{4})-(\d{2})-(\d{2})$")


def now_date(now: str) -> dt.date:
    return dt.date.fromisoformat(now[:10])


def rel_date(text: str, now: str):
    m = REL.match(text)
    if not m:
        return None
    d = now_date(now)
    if text == "today":
        return d
    if text == "tomorrow":
        return d + dt.timedelta(days=1)
    if text == "yesterday":
        return d - dt.timedelta(days=1)
    if m.group(2):
        return d + dt.timedelta(days=int(m.group(2)))
    if m.group(3):
        return d - dt.timedelta(days=int(m.group(3)))
    return d + dt.timedelta(days=7 * int(m.group(4)))


def as_date(text: str, now: str):
    m = DATE.match(text)
    if m:
        try:
            return dt.date(int(m.group(1)), int(m.group(2)), int(m.group(3)))
        except ValueError:
            return None
    return rel_date(text, now)


def form_ok(p: dict, text: str, now: str) -> bool:
    """NG-19 'could take by its form' (limits not part of form)."""
    t = p["type"]
    if t == "id":
        return bool(re.fullmatch(re.escape(p["prefix"]) + r"[A-Z0-9]{%d}" % p["n"], text))
    if t in ("integer", "decimal"):
        m = NUM.match(text)
        if not m or (m.group(2) or None) != (p.get("unit") or None):
            return False
        return t == "decimal" or "." not in m.group(1)
    if t == "date":
        return as_date(text, now) is not None
    if t == "enum":
        return text.lower() in [x.lower() for x in p["members"]]
    return False  # strings and yes/no are always named (R4-10, R4-11)


def accept(p: dict, text: str, now: str):
    """(True, canonical) or (False, reason) for a forward-row value (SEM-12..18, 29, 30, 42, 44)."""
    t = p["type"]
    if t == "id":
        return (True, text) if form_ok(p, text, now) else (False, "format")
    if t in ("integer", "decimal"):
        m = NUM.match(text)
        if not m:
            return False, "type"
        if (m.group(2) or None) != (p.get("unit") or None):
            return False, "unit"
        v = Decimal(m.group(1))
        if t == "integer" and v != v.to_integral_value():
            return False, "type"
        if t == "decimal":
            exp = -v.normalize().as_tuple().exponent if "." in m.group(1) else 0
            if exp > p["places"]:
                return False, "places"
        if p.get("min") and (v < Decimal(str(p["min"][0])) or (v == Decimal(str(p["min"][0])) and not p["min"][1])):
            return False, "limit"
        if p.get("max") and (v > Decimal(str(p["max"][0])) or (v == Decimal(str(p["max"][0])) and not p["max"][1])):
            return False, "limit"
        return True, (int(v) if t == "integer" else v)
    if t == "date":
        d = as_date(text, now)
        if d is None:
            return False, "type"
        if p.get("min"):
            lo = dt.date.fromisoformat(p["min"][0])
            if d < lo or (d == lo and not p["min"][1]):
                return False, "limit"
        if p.get("max"):
            hi = dt.date.fromisoformat(p["max"][0])
            if d > hi or (d == hi and not p["max"][1]):
                return False, "limit"
        return True, d.isoformat()
    if t == "enum":
        for x in p["members"]:
            if x.lower() == text.lower():
                return True, x
        return False, "choice"
    if t == "string":
        if not (p["minlen"] <= len(text) <= p["maxlen"]):
            return False, "length"
        return True, text
    if t == "boolean":
        return (True, text) if text in ("yes", "no") else (False, "type")
    return False, "type"


# ------------------------------------------------------------------------------------------------ request
def current_request(S):
    """Step 0: the last user message, plus the messages it continues (continuation chain back to the request)."""
    conv = S["conv"]
    users = [i for i, c in enumerate(conv) if c["who"] == "user"]
    last = users[-1]
    cur = [last]
    i = last
    while any(st["t"] == "cont" for st in conv[i]["st"]):
        j = i - 1
        assert conv[j]["who"] == "assistant" and conv[j].get("ask"), "continuation without a question"
        k = max(u for u in users if u < j)
        cur.insert(0, k)
        i = k
    return cur


def request_of(S):
    cur = current_request(S)
    for i in cur:
        for st in S["conv"][i]["st"]:
            if st["t"] == "req":
                return st, cur
    raise AssertionError("no request statement")


def kind_of(req) -> str:
    """Ordered kind test (section 3 step 0, R1-06, R2-04)."""
    if req["cue"] == "catalog" and req["ref"] is None:
        return "catalog"
    if req["a"] == "look up":
        return "info"
    return "action"


def target_info(S, pk):
    req, cur = request_of(S)
    et = pk["etypes"][req["o"]] if req["ref"] else None
    return req, cur, et


def _sources_about(S, et, req):
    """Records and tool outputs about the target entity (SEM-43). Returns (list of field dicts, unclear_id)."""
    srcs = [("record", r["fields"]) for r in S["records"]]
    srcs += [("tool", c["fields"]) for c in S["conv"] if c["who"] == "tool"]
    srcs += [("stored", s["fields"], s) for s in S["stored"]]
    ref = req["ref"]
    out, ids = [], set()
    for s in srcs:
        f = dict(s[1])
        if et["idkey"] not in f:
            continue
        if ref[0] == "id" and f[et["idkey"]] == ref[1]:
            out.append(s)
        elif ref[0] == "name" and f.get(et["namekey"]) == ref[1]:
            out.append(s)
            ids.add(f[et["idkey"]])
    unclear = ref[0] == "name" and len(ids) >= 2
    return out, unclear


def stamp_age(now: str, ts: str) -> int:
    a = dt.datetime.fromisoformat(now.replace(" ", "T"))
    b = dt.datetime.fromisoformat(ts.replace(" ", "T"))
    return int((a - b).total_seconds() // 60)


# ------------------------------------------------------------------------------------------------ solve
def solve(S, pk, checks_only=False):
    """Full section-3 procedure. Returns a result dict (outcome, called tool, per-tool checks, resolved values, ...)."""
    req, cur, et = target_info(S, pk)
    kind = kind_of(req)
    res = {"kind": kind, "a": req["a"], "o": req["o"], "ref": req["ref"]}
    tools = S["tools"]
    cand = [t for t in tools if t["a"] == req["a"] and t["o"] == req["o"]]
    prov = [t for t in tools if t["returns"]] if S["pol"]["chain"] else []
    # step 1: value resolution over params of candidate tools and providers
    pdefs = {}
    for t in cand + prov:
        for p in t["params"]:
            pdefs.setdefault(p["name"], []).append(p)
    vals, unclear, src = {}, set(), {}
    stmts = []
    for i in cur:
        for st in S["conv"][i]["st"]:
            stmts.append((i, st))
    # earlier fact statements about e (reference params needed on their own, R5-11) come first in walk order
    facts = []
    if req["ref"] and req["ref"][0] == "name":
        for i, c in enumerate(S["conv"]):
            if c["who"] == "user" and i not in cur:
                for st in c["st"]:
                    if st["t"] == "fact" and st["name"] == req["ref"][1]:
                        facts.append((i, st))
    asked_user = None
    for i, st in sorted(facts + stmts, key=lambda x: x[0]):
        if st["t"] == "fact":
            if st["p"] in pdefs:
                vals[st["p"]] = st["v"]
                src[st["p"]] = "earlier"
                unclear.discard(st["p"])
            if req.get("field") and st["p"] == req["field"]:
                asked_user = st["v"]
        elif st["t"] == "val":
            p = st["p"]
            if p is None:  # unnamed: the one param name every form-able param shares (NG-19)
                names = {n for n, ds in pdefs.items() if any(form_ok(d, st["v"], S["now"]) for d in ds)}
                assert len(names) == 1, f"unnamed value not attributable {st['v']} {names}"
                p = names.pop()
            if p in pdefs:
                if st.get("alts"):
                    unclear.add(p)
                    vals.pop(p, None)
                else:
                    vals[p] = st["v"]
                    unclear.discard(p)
                src[p] = "stated" if i == cur[-1] or len(cur) == 1 else "current"
                if REL.match(st["v"] or ""):
                    src[p] = "reldate"
        elif st["t"] == "cont":
            j = i - 1
            p = S["conv"][j]["ask"]
            if p in pdefs:
                vals[p] = st["v"]
                unclear.discard(p)
                src[p] = "continuation"
    # target id from the request itself
    if et is not None and req["ref"] and req["ref"][0] == "id":
        if et["idkey"] in pdefs:
            vals.setdefault(et["idkey"], req["ref"][1])
            src.setdefault(et["idkey"], "stated")
    about, unclear_id = (_sources_about(S, et, req) if et is not None else ([], False))
    if et is not None and unclear_id and et["idkey"] not in vals:
        unclear.add(et["idkey"])
    elif et is not None:
        for s in about:
            f = dict(s[1])
            for k, v in f.items():
                if k in pdefs and k not in vals and k not in unclear and v not in MARK_UNKNOWN:
                    vals[k] = v
                    src[k] = s[0]
    qual = None
    for i in cur:
        for st in S["conv"][i]["st"]:
            if st["t"] == "qual":
                qual = st["v"]
    rec_about = [s for s in about if s[0] == "record"]
    if qual is None:
        for s in rec_about:
            f = dict(s[1])
            if pk["dim"]["key"] in f:
                qual = f[pk["dim"]["key"]]
    status = None
    for s in rec_about:
        f = dict(s[1])
        if "status" in f:
            status = f["status"]
    res.update(vals=dict(vals), unclear=sorted(unclear), src=dict(src), qual=qual, status=status)
    # ANSWER check (step 4)
    if kind == "catalog":
        res.update(outcome="ANSWER", tool=None, answer="catalog")
        res["checks"] = {t["name"]: check_tool(t, req, qual, status, S, vals, unclear) for t in tools}
        return res
    if kind == "info":
        f = req["field"]
        shown = None
        if asked_user is not None:
            shown = "user"
        for i in cur:
            for st in S["conv"][i]["st"]:
                if st["t"] == "val" and st["p"] == f:
                    shown = "user"
        if shown is None and not unclear_id:
            for s in about:
                fd = dict(s[1])
                if f in fd and fd[f] not in MARK_UNKNOWN:
                    if s[0] == "stored" and S["pol"]["fresh"] is not None and \
                            stamp_age(S["now"], s[2]["ts"]) > S["pol"]["fresh"]:
                        continue
                    shown = s[0]
                    break
        if shown:
            res.update(outcome="ANSWER", tool=None, answer=shown)
            res["checks"] = {t["name"]: check_tool(t, req, qual, status, S, vals, unclear) for t in tools}
            return res
    checks = {t["name"]: check_tool(t, req, qual, status, S, vals, unclear) for t in tools}
    res["checks"] = checks
    if checks_only:
        res["outcome"] = None
        return res
    fitting = [t for t in cand if checks[t["name"]]["fit"]]
    if not fitting:
        res.update(outcome="UNABLE", tool=None)
        return res
    complete = [t for t in fitting if checks[t["name"]]["complete"]]
    if len(complete) == 1:
        res.update(outcome="CALL", tool=complete[0]["name"], chain=False)
        return res
    if len(complete) >= 2:
        assert S["pol"]["tie"], "tie without POL-TIE (NG-06)"
        best = min(t["cost"] for t in complete)
        c2 = [t for t in complete if t["cost"] == best]
        if len(c2) > 1:
            c3 = [t for t in c2 if t["pref"]]
            assert len(c3) == 1, "tie left after the preferred check (NG-06)"
            c2 = c3
        res.update(outcome="CALL", tool=c2[0]["name"], chain=False, tie=[t["name"] for t in complete])
        return res
    # step 7 chain
    if S["pol"]["chain"] and len(fitting) == 1:
        T = fitting[0]
        ck = checks[T["name"]]
        if ck["accepts"] and len(ck["missing"]) == 1 and not ck["unclear"]:
            p = ck["missing"][0]
            el = []
            for P in prov:
                if p not in P["returns"]:
                    continue
                pc = check_tool(P, req, qual, status, S, vals, unclear, as_provider=True)
                if pc["provider_ok"]:
                    el.append(P)
            assert len(el) <= 1, "two eligible providers (NG-02)"
            if el:
                res.update(outcome="CALL", tool=el[0]["name"], chain=True, final=T["name"], chain_param=p)
                return res
    res.update(outcome="ASK", tool=None)
    return res


def check_tool(t, req, qual, status, S, vals, unclear, as_provider=False):
    """Per-tool checks in the fixed order (A58): capability, scope, precondition, role, accept, completeness."""
    out = {"cap": t["a"] == req["a"] and t["o"] == req["o"], "scope": True, "pre": True, "role": True}
    if t["scope"] is not None and qual is not None:
        out["scope"] = qual in t["scope"]
    if t["scope"] is not None and qual is None:
        out["scope"] = False if as_provider else True  # NG-11: generator never leaves a restricted dim unset
    if t["pre"] is not None:
        out["pre"] = status == t["pre"]
    if S["pol"]["role"]:
        out["role"] = S["role"] in t["roles"]
    rej, missing, unc = [], [], []
    for p in t["params"]:
        n = p["name"]
        if n in vals:
            ok, why = accept(p, vals[n], S["now"])
            if not ok:
                rej.append((n, why))
        elif n in unclear:
            if p["required"]:
                unc.append(n)
        elif p["required"]:
            missing.append(n)
    out["rejects"] = rej
    out["accepts"] = not rej
    out["missing"] = missing
    out["unclear"] = unc
    out["match"] = out["cap"] and out["scope"] and out["pre"] and out["role"]
    out["fit"] = out["match"] and (out["accepts"] or S["pol"]["invalid"] == "A")
    out["complete"] = out["fit"] and out["accepts"] and not missing and not unc
    if as_provider:
        out["provider_ok"] = out["scope"] and out["pre"] and out["role"] and out["accepts"] and not missing \
                             and not unc
    # failing components, in check order (near-miss = exactly one)
    fails = []
    if not out["cap"]:
        fails.append("action" if t["o"] == req["o"] else ("object" if t["a"] == req["a"] else "capability"))
    if not out["scope"]:
        fails.append("scope")
    if not out["pre"]:
        fails.append("precondition")
    if not out["role"]:
        fails.append("role")
    if S["pol"]["invalid"] == "B" and rej:
        fails.extend(["value"] * len(rej))
    out["fails"] = fails
    return out


def near_misses(S, res):
    """Sorted (tool name, component) pairs (section 2, R2-13). CALL rows add fitting tools with exactly one
    parameter problem (needed value missing while the request gives a value N lacks, or one non-accepted value)."""
    out = []
    called = {res.get("tool"), res.get("final")}
    stated = set(res["vals"])
    for t in S["tools"]:
        if t["name"] in called or t.get("borrowed"):
            continue
        ck = res["checks"][t["name"]]
        f = ck["fails"]
        if len(f) == 1 and f[0] != "capability":
            out.append((t["name"], f[0]))
        elif not f and res["outcome"] == "CALL" and ck["match"]:
            names = {p["name"] for p in t["params"]}
            if len(ck["missing"]) == 1 and not ck["unclear"] and not ck["rejects"] and (stated - names):
                out.append((t["name"], "needed parameter"))
            elif S["pol"]["invalid"] == "A" and len(ck["rejects"]) == 1 and not ck["missing"] and not ck["unclear"]:
                out.append((t["name"], "non-accepted value"))
    return sorted(out)
