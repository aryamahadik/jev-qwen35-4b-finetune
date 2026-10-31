"""G3 parsers, solver B, canonical forms and trigger re-computation for S2-S5 (S1 lives in parse.py / gates.py).

Solver B per sampler (a different paradigm from solver A):
  S2  backward version-graph resolver: for a query it walks the parsed log backwards from the asked day and follows
      CORRECTION / VOID pointers from each candidate entry (an entry counts iff no counting VOID names it; its value is
      the one of the counting CORRECTION that names it), with its own LF evaluator.
"""
from __future__ import annotations

import datetime as dt
import re

from . import parse as PZ
from .common import DATE_PAT, MONTHS
from .texts import ATTACK_RE

ATT = re.compile(ATTACK_RE)
ID = r"[A-Z]{1,4}-[A-Z0-9]+(?:-[A-Z0-9]+)?"
PERSON = r"[A-Z][a-z]+ [A-Z][A-Za-z'-]+"


def _dd(s, n):
    return (dt.date.fromisoformat(s) + dt.timedelta(days=n)).isoformat()


# ---------------------------------------------------------------------------------------------------------------------
# S2: log grammar

ENTRY = re.compile(r"(E\d+)\. (.+)\.")


def s2_entries(state):
    """[(date, eid, body)] from any container: a date token followed (in reading order) by an entry 'E<n>. ...'."""
    lines, rows = PZ.flatten(state)
    if not rows:
        rows = PZ.csv_rows(state)
        if rows:
            lines = []
    cells = {c for r in rows for c in r}
    stream = [c for r in rows for c in r] + [ln for ln in lines if ln not in cells]
    out = []
    last_date = None
    seen = set()
    for item in stream:
        s = PZ.clean_line(item).strip().strip('"').strip()
        m = re.search(r"\bE\d+\. ", s)
        head = s[: m.start()] if m else s
        for d in re.findall(DATE_PAT, head):
            last_date = d
        if not m:
            continue
        txt = s[m.start():].rstrip(' |"')
        mm = ENTRY.fullmatch(txt)
        if not mm:
            raise ValueError(f"entry text {txt!r}")
        if mm.group(1) in seen:
            continue
        seen.add(mm.group(1))
        out.append((last_date, mm.group(1), mm.group(2)))
    return out, lines, rows


def _item(txt):
    m = re.fullmatch(rf"(.+?) ({ID})", txt)
    if not m:
        raise ValueError(f"item {txt!r}")
    return m.group(1).lower(), m.group(2)


def _vp(v, rest):
    """renew <item> | report a <risk> for <item> | file the <doc> for <item> -> (kind, item_noun, item_id)."""
    if v in ("renew", "renewed", "renewing"):
        n, i = _item(rest)
        return "renew", n, i
    if v in ("report", "reported", "reporting"):
        m = re.fullmatch(rf"a (.+?) for (.+ {ID})", rest)
        n, i = _item(m.group(2))
        return "report:" + m.group(1), n, i
    if v in ("file", "filed", "filing"):
        m = re.fullmatch(rf"the (.+?) for (.+ {ID})", rest)
        n, i = _item(m.group(2))
        return "file:" + m.group(1), n, i
    raise ValueError(v)


def s2_parse_entry(date, eid, body):
    e = {"eid": eid, "date": date}
    m = re.fullmatch(rf"(.+?) ({ID}) was created for ({PERSON})", body)
    if m:
        return {**e, "type": "create", "item": m.group(2), "noun": m.group(1).lower(), "holder": m.group(3)}
    m = re.fullmatch(rf"({PERSON}) transferred (.+?) ({ID}) to ({PERSON})", body)
    if m:
        return {**e, "type": "transfer", "actor": m.group(1), "item": m.group(3), "noun": m.group(2), "to": m.group(4)}
    m = re.fullmatch(rf"({PERSON}) renewed (.+?) ({ID}) for (\d+) days", body)
    if m:
        return {**e, "type": "renew", "actor": m.group(1), "item": m.group(3), "noun": m.group(2),
                "days": int(m.group(4))}
    m = re.fullmatch(rf"The status of (.+?) ({ID}) was set to (.+)", body)
    if m:
        return {**e, "type": "status", "item": m.group(2), "noun": m.group(1), "status": m.group(3)}
    m = re.fullmatch(rf"({PERSON}) filed the (.+?) for (.+?) ({ID})", body)
    if m:
        return {**e, "type": "file", "actor": m.group(1), "doc": m.group(2), "item": m.group(4), "noun": m.group(3)}
    m = re.fullmatch(rf"({PERSON}) reported a (.+?) for (.+?) ({ID})", body)
    if m:
        return {**e, "type": "report", "actor": m.group(1), "risk": m.group(2), "item": m.group(4),
                "noun": m.group(3)}
    m = re.fullmatch(r"CORRECTION of (E\d+): (the number of days is|the new holder is|the holder is|the status is) (.+)",
                     body)
    if m:
        f = {"the number of days is": "days", "the new holder is": "to", "the holder is": "holder",
             "the status is": "status"}[m.group(2)]
        v = int(m.group(3)) if f == "days" else m.group(3)
        return {**e, "type": "correction", "target": m.group(1), "field": f, "value": v}
    m = re.fullmatch(r"VOID of (E\d+)", body)
    if m:
        return {**e, "type": "void", "target": m.group(1)}
    m = re.fullmatch(rf"({PERSON}) (failed to|neglected to|omitted to|did not manage to|refused to|declined to|was "
                     rf"prevented from) (renew|renewing|file|filing|report|reporting) (.+)", body)
    if m:
        kind, n, i = _vp(m.group(3), m.group(4))
        return {**e, "type": "fail", "actor": m.group(1), "cue": m.group(2), "kind": kind, "item": i}
    m = re.fullmatch(rf"As of ({DATE_PAT}), (.+?) ({ID}) is (not )?valid", body)
    if m:
        return {**e, "type": "asof", "item": m.group(3), "state": "valid", "day": m.group(1),
                "value": not m.group(4)}
    m = re.fullmatch(rf"As of ({DATE_PAT}), the status of (.+?) ({ID}) is (.+)", body)
    if m:
        return {**e, "type": "asof", "item": m.group(3), "state": "status", "day": m.group(1), "value": m.group(4)}
    m = re.fullmatch(rf"No (renewal|report of a (.+?)|filing of the (.+?)) (?:of|for) (.+?) ({ID}) by ({PERSON}) took "
                     rf"place from ({DATE_PAT}) to ({DATE_PAT})", body)
    if m:
        kind = "renew" if m.group(1) == "renewal" else ("report:" + m.group(2) if m.group(2) else "file:" + m.group(3))
        return {**e, "type": "noev", "kind": kind, "item": m.group(5), "actor": m.group(6), "lo": m.group(7),
                "hi": m.group(8)}
    m = re.fullmatch(rf"({PERSON}) (stated|denied) that ({PERSON}) (.+)", body)
    if m:
        kind, item, rng_txt = _split_vp(m.group(4), True)
        claim = {"actor": m.group(3), "kind": kind, "item": item.rsplit(" ", 1)[1]}
        if rng_txt:
            claim["range"] = rng_txt
        return {**e, "type": "notice", "party": m.group(1), "verb": m.group(2), "claim": claim, "item": None}
    raise ValueError(f"S2 entry: {body!r}")


def s2_parse(rs, consts):
    r = next((x for x in rs if x["role"] != "attack"), rs[0])
    ents, lines, rows = s2_entries(r["state"])
    entries = [s2_parse_entry(d, e, b) for d, e, b in ents]
    for x in rs:
        if x["role"] == "attack":
            ents2, l2, r2 = s2_entries(x["state"])
            if [(d, e, b) for d, e, b in ents2] != ents:
                raise ValueError("attack twin log differs")
            if not any(ATT.search(PZ.clean_line(t)) for t in l2 + [c for rr in r2 for c in rr]):
                raise ValueError("attack twin has no attack span")
    return {"entries": entries, "period": consts["period"], "world": consts["world"], "S": consts.get("S"),
            "statuses": consts["value_sets"].get("status")}


# solver B (backward resolver) ----------------------------------------------------------------------------------------

def _counts(S, eid, memo=None):
    """An entry counts iff no counting VOID names it (pointer chase)."""
    memo = {} if memo is None else memo
    if eid in memo:
        return memo[eid]
    memo[eid] = True
    for e in S["entries"]:
        if e["type"] == "void" and e["target"] == eid and _counts(S, e["eid"], memo):
            memo[eid] = False
            break
    return memo[eid]


def _value(S, e, field):
    for c in S["entries"]:
        if c["type"] == "correction" and c["target"] == e["eid"] and c["field"] == field and _counts(S, c["eid"]):
            return c["value"]
    return e.get(field)


def _kind_of(e):
    if e["type"] == "renew":
        return "renew"
    if e["type"] == "report":
        return "report:" + e["risk"]
    if e["type"] == "file":
        return "file:" + e["doc"]
    return None


def _ev(S, kind, actor, iid, lo, hi):
    ps, pe = S["period"]
    lo2, hi2 = lo or ps, hi or pe
    for e in sorted(S["entries"], key=lambda x: x["date"], reverse=True):
        if e.get("item") == iid and _kind_of(e) == kind and e.get("actor") == actor and lo2 <= e["date"] <= hi2 \
                and _counts(S, e["eid"]):
            return True
    if S["world"] == "closed":
        return False
    for e in S["entries"]:
        if e["type"] == "noev" and e["kind"] == kind and e["actor"] == actor and e.get("item") == iid and \
                e["lo"] <= lo2 and e["hi"] >= hi2 and _counts(S, e["eid"]):
            return False
    raise PZ.QParseError("open card: event undetermined")


def _valid(S, iid, day):
    if S["world"] != "closed":
        for e in S["entries"]:
            if e["type"] == "asof" and e.get("item") == iid and e["state"] == "valid" and e["day"] == day and \
                    _counts(S, e["eid"]):
                return e["value"]
        raise PZ.QParseError("open card: state undetermined")
    for e in sorted(S["entries"], key=lambda x: x["date"], reverse=True):     # backward from the asked day
        if e["type"] == "renew" and e.get("item") == iid and e["date"] <= day and _counts(S, e["eid"]):
            last = _dd(e["date"], int(_value(S, e, "days")))
            return day <= last
    return False


def _status(S, iid, s, day):
    if S["world"] != "closed":
        for e in S["entries"]:
            if e["type"] == "asof" and e.get("item") == iid and e["state"] == "status" and e["day"] == day:
                return e["value"] == s
        raise PZ.QParseError("open card: status undetermined")
    for e in sorted(S["entries"], key=lambda x: x["date"], reverse=True):
        if e["type"] == "status" and e.get("item") == iid and e["date"] <= day and _counts(S, e["eid"]):
            return _value(S, e, "status") == s
    raise PZ.QParseError("no status before the asked day")


def s2_eval(lf, S):
    op = lf[0]
    if op == "not":
        return not s2_eval(lf[1], S)
    if op == "and":
        return all(s2_eval(x, S) for x in lf[1:])
    if op == "ev":
        return _ev(S, lf[1], lf[2], lf[3].rsplit(" ", 1)[1], lf[4], lf[5])
    if op == "valid":
        return _valid(S, lf[1].rsplit(" ", 1)[1], lf[2])
    if op == "still":
        iid, day = lf[1].rsplit(" ", 1)[1], lf[2]
        n = (dt.date.fromisoformat(day) - dt.date.fromisoformat(S["period"][0])).days
        return _valid(S, iid, day) and any(_valid(S, iid, _dd(S["period"][0], i)) for i in range(n))
    if op == "status":
        return _status(S, lf[1].rsplit(" ", 1)[1], lf[2], lf[3])
    raise ValueError(op)


# question grammar for S2 ---------------------------------------------------------------------------------------------

RANGE_P = [("on or before", "obf"), ("on or after", "oaf"), ("no later than", "nlt"), ("no earlier than", "net"),
           ("not before", "nbf"), ("not after", "naf"), ("by", "by"), ("before", "bef"), ("after", "aft"), ("on", "on")]


def parse_range(s):
    """' <range>' suffix -> (lo, hi, k, families) with lo / hi ISO or None."""
    s = s.strip()
    if not s:
        return None, None, 0, []
    m = re.fullmatch(rf"between ({DATE_PAT}) and ({DATE_PAT})", s)
    if m:
        return m.group(1), m.group(2), 0, []
    m = re.fullmatch(rf"from ({DATE_PAT}) to ({DATE_PAT})", s)
    if m:
        return m.group(1), m.group(2), 0, []
    m = re.fullmatch(rf"({DATE_PAT}) through ({DATE_PAT})", s)
    if m:
        return m.group(1), m.group(2), 0, []
    m = re.fullmatch(rf"within (\d+) days after ({DATE_PAT})", s)
    if m:
        return _dd(m.group(2), 1), _dd(m.group(2), int(m.group(1))), 0, []
    m = re.fullmatch(r"in (" + "|".join(MONTHS) + r") (\d{4})", s)
    if m:
        y, mo = int(m.group(2)), MONTHS.index(m.group(1)) + 1
        lo = dt.date(y, mo, 1)
        hi = (lo + dt.timedelta(days=32)).replace(day=1) - dt.timedelta(days=1)
        return lo.isoformat(), hi.isoformat(), 0, []
    for ph, tag in RANGE_P:
        m = re.fullmatch(rf"{ph} ({DATE_PAT})", s)
        if m:
            d = m.group(1)
            if tag in ("obf", "by"):
                return None, d, 0, []
            if tag == "nlt" or tag == "naf":
                return None, d, 1, ["C10"]
            if tag == "oaf":
                return d, None, 0, []
            if tag in ("net", "nbf"):
                return d, None, 1, ["C10"]
            if tag == "bef":
                return None, _dd(d, -1), 0, []
            if tag == "aft":
                return _dd(d, 1), None, 0, []
            if tag == "on":
                return d, d, 0, []
    raise PZ.QParseError(f"range {s!r}")


def _split_vp(rest, past):
    """'renewed licence X-1 <range>' -> (kind, item text, range text)."""
    v = r"(renewed|reported|filed)" if past else r"(renew|report|file)"
    m = re.fullmatch(rf"{v} (.+? {ID})(?: (.*))?", rest)
    if not m:
        raise PZ.QParseError(f"vp {rest!r}")
    verb, obj, rng = m.group(1), m.group(2), m.group(3) or ""
    if verb.startswith("renew"):
        return "renew", obj, rng
    mm = re.fullmatch(rf"(?:a|the) (.+?) for (.+ {ID})", obj)
    if not mm:
        raise PZ.QParseError(f"object {obj!r}")
    kind = ("report:" if verb.startswith("report") else "file:") + mm.group(1)
    return kind, mm.group(2), rng


def s2_decl(c, st, ctx):
    m = re.fullmatch(rf"(.+? {ID}) is (still |not )?valid as of ({DATE_PAT})", c)
    if m:
        if m.group(2) == "still ":
            st.fams.append("C15")          # "still": a C15 cue with k = 0 (fires SEM-26 / SEM-27)
            return ["still", m.group(1), m.group(3)]
        a = ["valid", m.group(1), m.group(3)]
        if m.group(2):
            st.add("C1")
            return ["not", a]
        return a
    m = re.fullmatch(rf"(.+? {ID}) was renewed by ({PERSON})(?: (.*))?", c)
    if m:
        lo, hi, kk, ff = parse_range(m.group(3) or "")
        for f in ff:
            st.add(f)
        return ["ev", "renew", m.group(2), m.group(1), lo, hi]
    m = re.fullmatch(rf"({PERSON}) (.+)", c)
    if not m:
        return None
    actor, rest = m.groups()
    mm = re.fullmatch(r"never (.+)", rest)
    if mm:
        st.add("C15")
        kind, item, rng = _split_vp(mm.group(1), True)
        if rng:
            raise PZ.QParseError("never with a range")
        return ["not", ["ev", kind, actor, item, None, None]]
    mm = re.fullmatch(r"not only (.+?) but also (.+)", rest)
    if mm:
        st.fams.append("C16")
        k1, i1, r1 = _split_vp(mm.group(1), True)
        lo, hi, kk, ff = parse_range(r1)
        k2, i2, r2 = _split_vp(mm.group(2), True)
        return ["and", ["ev", k1, actor, i1, lo, hi], ["ev", k2, actor, i2, None, None]]
    mm = re.fullmatch(rf"did not fail to (.+) by ({DATE_PAT})", rest)
    if mm:
        st.add("C1")
        st.add("C3")
        kind, item, rng = _split_vp(mm.group(1), False)
        return ["not", ["not", ["ev", kind, actor, item, None, mm.group(2)]]]
    mm = re.fullmatch(rf"(failed to|neglected to|omitted to|did not manage to) (.+) by ({DATE_PAT})", rest)
    if mm:
        st.add("C3")
        kind, item, rng = _split_vp(mm.group(2), False)
        return ["not", ["ev", kind, actor, item, None, mm.group(3)]]
    mm = re.fullmatch(r"did not (.+)", rest)
    if mm:
        st.add("C1")
        kind, item, rng = _split_vp(mm.group(1), False)
        lo, hi, kk, ff = parse_range(rng)
        for f in ff:
            st.add(f)
        return ["not", ["ev", kind, actor, item, lo, hi]]
    kind, item, rng = _split_vp(rest, True)
    lo, hi, kk, ff = parse_range(rng)
    for f in ff:
        st.add(f)
    return ["ev", kind, actor, item, lo, hi]


def s2_matrix(body, st, ctx):
    m = re.fullmatch(rf"Was (.+? {ID}) renewed by ({PERSON})(?: (.*))?", body)
    if m:
        lo, hi, kk, ff = parse_range(m.group(3) or "")
        for f in ff:
            st.add(f)
        return ["ev", "renew", m.group(2), m.group(1), lo, hi]
    m = re.fullmatch(rf"Is (.+? {ID}) (still )?valid as of ({DATE_PAT})", body)
    if m:
        if m.group(2):
            st.fams.append("C15")
            return ["still", m.group(1), m.group(3)]
        return ["valid", m.group(1), m.group(3)]
    m = re.fullmatch(rf"Did ({PERSON}) (fail|neglect|omit) to (.+) by ({DATE_PAT})", body)
    if m:
        st.add("C3")
        kind, item, rng = _split_vp(m.group(3), False)
        return ["not", ["ev", kind, m.group(1), item, None, m.group(4)]]
    m = re.fullmatch(rf"Did ({PERSON}) (.+)", body)
    if m:
        kind, item, rng = _split_vp(m.group(2), False)
        lo, hi, kk, ff = parse_range(rng)
        for f in ff:
            st.add(f)
        return ["ev", kind, m.group(1), item, lo, hi]
    return None


def s2_canon_gen(M):
    out = []
    for e in M["entries"]:
        x = {k: v for k, v in e.items() if k not in ("noun",)}
        if x["type"] == "notice":
            x["claim"] = dict(x["claim"])
        out.append(x)
    return sorted((json_key(x) for x in out))


def s2_canon_parsed(S):
    out = []
    for e in S["entries"]:
        x = {k: v for k, v in e.items() if k not in ("noun",)}
        out.append(x)
    return sorted((json_key(x) for x in out))


def json_key(x):
    import json
    return json.dumps(x, sort_keys=True, default=str)


def s2_triggers(S):
    keys = {"SEM-01", "SEM-02" if S["world"] == "closed" else "SEM-03", "SEM-16", "SEM-20", "SEM-33", "SEM-27",
            "SEM-11", "SEM-12", "SEM-14"}
    if any(e["type"] == "status" or (e["type"] == "correction" and e["field"] == "status") or
           (e["type"] == "asof" and e["state"] == "status") for e in S["entries"]):
        keys.add("SEM-17")
    if any(e["type"] == "fail" for e in S["entries"]):
        keys.add("SEM-19")
    return keys


# ---------------------------------------------------------------------------------------------------------------------
# dispatch

def parse_structure(sampler, rs, consts):
    if sampler == "S2":
        return s2_parse(rs, consts)
    if sampler == "S3":
        from . import parse_s3
        return parse_s3.parse(rs, consts)
    if sampler == "S4":
        from . import parse_s4
        return parse_s4.parse(rs, consts)
    if sampler == "S5":
        from . import parse_s5
        return parse_s5.parse(rs, consts)
    if sampler == "INV":
        from . import parse_inv
        return parse_inv.parse(rs, consts)
    raise ValueError(sampler)


def canon_gen(sampler, M):
    if sampler == "S2":
        return s2_canon_gen(M)
    mod = __import__(f"{__package__}.parse_{sampler.lower()}", fromlist=["x"])
    return mod.canon_gen(M)


def canon_parsed(sampler, S):
    if sampler == "S2":
        return s2_canon_parsed(S)
    mod = __import__(f"{__package__}.parse_{sampler.lower()}", fromlist=["x"])
    return mod.canon_parsed(S)


def solve_b(sampler, S, lfs):
    if sampler == "S2":
        return [s2_eval(lf, S) for lf in lfs]
    mod = __import__(f"{__package__}.parse_{sampler.lower()}", fromlist=["x"])
    return mod.solve_b(S, lfs)


def triggers(sampler, S, qf):
    if sampler == "S2":
        return s2_triggers(S)
    mod = __import__(f"{__package__}.parse_{sampler.lower()}", fromlist=["x"])
    return mod.triggers(S)


def decl_parsers(sampler):
    if sampler == "S2":
        return [s2_decl], [s2_matrix]
    if sampler == "S1":
        return [], []
    mod = __import__(f"{__package__}.parse_{sampler.lower()}", fromlist=["x"])
    return mod.decl_parsers()
