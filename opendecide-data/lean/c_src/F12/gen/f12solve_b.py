"""F12 solver B: declarative validator on the PARSED structure (G0 section 5 "Solver B").

Match, value resolution and outcome run as SQL over in-memory sqlite3 tables (NOT EXISTS for scope, a window over
statement order for the value in force, one CASE decision table for SEM-04 and the policies). Acceptance compiles each
parsed tool to a JSON Schema (Draft 2020-12) and validates with `jsonschema`, after the fixed pre-pass (typed parse,
Decimal scaled by 10^places, dates to day ordinals, defaults filled). Written from the spec, not from solver A.
"""
from __future__ import annotations

import datetime as dt
import json
import re
import sqlite3
from decimal import Decimal

import jsonschema

RELW = re.compile(r"^(?:today|tomorrow|yesterday|in (\d+) days?|(\d+) days? ago|in (\d+) weeks?)$")


def day_ord(text, now):
    base = dt.date.fromisoformat(now[:10]).toordinal()
    if re.fullmatch(r"\d{4}-\d{2}-\d{2}", text):
        try:
            return dt.date.fromisoformat(text).toordinal()
        except ValueError:
            return None
    m = RELW.match(text)
    if not m:
        return None
    if text == "today":
        return base
    if text == "tomorrow":
        return base + 1
    if text == "yesterday":
        return base - 1
    if m.group(1):
        return base + int(m.group(1))
    if m.group(2):
        return base - int(m.group(2))
    return base + 7 * int(m.group(3))


def prepass(p, text, now):
    """Typed form of a forward-row value; anything unreadable stays a raw string (-> type / enum error)."""
    t = p["type"]
    if t in ("integer", "decimal"):
        unit = p.get("unit")
        m = re.fullmatch(r"(\d+(?:\.\d+)?)" + (r" " + re.escape(unit) if unit else ""), text)
        if not m:
            return text
        v = Decimal(m.group(1))
        if t == "integer":
            return int(v) if v == v.to_integral_value() and "." not in m.group(1) else float(v)
        sc = v * (10 ** p["places"])
        return int(sc) if sc == sc.to_integral_value() else float(sc)
    if t == "date":
        o = day_ord(text, now)
        return o if o is not None else text
    if t == "enum":
        for x in p["members"]:
            if x.casefold() == text.casefold():
                return x
        return text
    if t == "boolean":
        return text
    return text


def schema_of(tool):
    props, req = {}, []
    for p in tool["params"]:
        t = p["type"]
        s = {}
        if t == "id":
            s = {"type": "string", "pattern": "^(?:" + re.escape(p["prefix"]) + "[A-Z0-9]{%d})$" % p["n"]}
        elif t in ("integer", "decimal"):
            s = {"type": "integer"}
            k = 10 ** p["places"] if t == "decimal" else 1
            if p.get("min"):
                s["minimum" if p["min"][1] else "exclusiveMinimum"] = int(Decimal(str(p["min"][0])) * k)
            if p.get("max"):
                s["maximum" if p["max"][1] else "exclusiveMaximum"] = int(Decimal(str(p["max"][0])) * k)
        elif t == "date":
            s = {"type": "integer"}
            if p.get("min"):
                o = dt.date.fromisoformat(p["min"][0]).toordinal()
                s["minimum" if p["min"][1] else "exclusiveMinimum"] = o
            if p.get("max"):
                o = dt.date.fromisoformat(p["max"][0]).toordinal()
                s["maximum" if p["max"][1] else "exclusiveMaximum"] = o
        elif t == "enum":
            s = {"enum": list(p["members"])}
        elif t == "string":
            s = {"type": "string", "minLength": p["minlen"], "maxLength": p["maxlen"]}
        elif t == "boolean":
            s = {"enum": ["yes", "no"]}
        props[p["name"]] = s
        if p["required"]:
            req.append(p["name"])
    return {"$schema": "https://json-schema.org/draft/2020-12/schema", "type": "object", "properties": props,
            "required": req, "additionalProperties": False}


def form_fits(p, text, now):
    t = p["type"]
    if t == "id":
        return re.fullmatch(re.escape(p["prefix"]) + "[A-Z0-9]{%d}" % p["n"], text) is not None
    if t in ("integer", "decimal"):
        u = p.get("unit")
        rx = (r"\d+" if t == "integer" else r"\d+(?:\.\d+)?") + ((" " + re.escape(u)) if u else "")
        return re.fullmatch(rx, text) is not None
    if t == "date":
        return day_ord(text, now) is not None
    if t == "enum":
        return any(x.casefold() == text.casefold() for x in p["members"])
    return False


def solve(P, pol, lex):
    """P = parsed structure (f12parse.parse_state) with P['request'] info filled. Returns dict(outcome, tool,...)."""
    db = sqlite3.connect(":memory:")
    c = db.cursor()
    c.executescript("""
      CREATE TABLE tools(name TEXT PRIMARY KEY, a TEXT, o INTEGER, pre TEXT, restricted INTEGER, cost INTEGER,
                         pref INTEGER, pos INTEGER, provider INTEGER);
      CREATE TABLE scope(tool TEXT, value TEXT);
      CREATE TABLE roles(tool TEXT, role TEXT);
      CREATE TABLE params(tool TEXT, name TEXT, required INTEGER);
      CREATE TABLE returns(tool TEXT, param TEXT);
      CREATE TABLE mentions(seq INTEGER, param TEXT, value TEXT, open INTEGER);
      CREATE TABLE src(sid INTEGER, kind TEXT, ts TEXT, k TEXT, v TEXT);
    """)
    now = P["now"]
    users = [i for i, x in enumerate(P["conv"]) if x["who"] == "user"]
    # current request: last user message plus the messages it continues
    cur = [users[-1]]
    while any(s["t"] == "cont" for s in P["conv"][cur[0]]["st"]):
        cur.insert(0, max(u for u in users if u < cur[0] - 1))
    req = next(s for i in cur for s in P["conv"][i]["st"] if s["t"] == "req")
    a, o = req["a"], req["o"]
    kind = "catalog" if (req["cue"] == "catalog" and req["ref"] is None) else ("info" if a == "look up"
                                                                                  else "action")
    for pos, t in enumerate(P["tools"]):
        oo = lex["owords"].get(t["oword"], -1)
        c.execute("INSERT INTO tools VALUES (?,?,?,?,?,?,?,?,?)",
                  (t["name"], t["a"], oo, t["pre"], 1 if t["scope"] else 0, t["cost"], 1 if t["pref"] else 0,
                   pos, 1 if (t["returns"] and pol["chain"]) else 0))
        for v in t["scope"] or []:
            c.execute("INSERT INTO scope VALUES (?,?)", (t["name"], v))
        for r in t["roles"] or []:
            c.execute("INSERT INTO roles VALUES (?,?)", (t["name"], r))
        for p in t["params"]:
            c.execute("INSERT INTO params VALUES (?,?,?)", (t["name"], p["name"], 1 if p["required"] else 0))
        for r in t["returns"]:
            c.execute("INSERT INTO returns VALUES (?,?)", (t["name"], r))
    byname = {t["name"]: t for t in P["tools"]}
    cand_names = [r[0] for r in c.execute("SELECT name FROM tools WHERE (a=? AND o=? AND provider=0) OR provider=1",
                                          (a, o))]
    pdefs = {}
    for n in cand_names:
        for p in byname[n]["params"]:
            pdefs.setdefault(p["name"], []).append(p)
    # mentions: fact statements about the target (by name), then the current request, in order
    seq = 0
    et_idkey = lex["idkeys"][o] if o is not None and o >= 0 else None
    et_namekey = lex["namekeys"][o] if o is not None and o >= 0 else None
    for i, x in enumerate(P["conv"]):
        if x["who"] != "user":
            continue
        for s in x["st"]:
            seq += 1
            if i not in cur:
                if s["t"] == "fact" and req["ref"] and req["ref"][0] == "name" and s["name"] == req["ref"][1]:
                    c.execute("INSERT INTO mentions VALUES (?,?,?,0)", (seq, s["p"], s["v"]))
                continue
            if s["t"] == "val":
                pn = s["p"]
                val = s["v"] if s["v"] is not None else None
                if pn is None:
                    names = sorted({n for n, ds in pdefs.items() if any(form_fits(d, val, now) for d in ds)})
                    if len(names) != 1:
                        raise ValueError("unnamed value")
                    pn = names[0]
                c.execute("INSERT INTO mentions VALUES (?,?,?,?)", (seq, pn, val, 1 if s.get("alts") else 0))
            elif s["t"] == "cont":
                prev = P["conv"][i - 1]
                c.execute("INSERT INTO mentions VALUES (?,?,?,0)", (seq, prev["ask"], s["v"]))
    if req["ref"] and req["ref"][0] == "id" and et_idkey:
        c.execute("INSERT INTO mentions VALUES (0,?,?,0)", (et_idkey, req["ref"][1]))
    # sources about the target
    sid = 0
    for kind_s, items in (("record", [r["fields"] for r in P["records"]]),
                          ("tool", [x["fields"] for x in P["conv"] if x["who"] == "tool"])):
        for f in items:
            sid += 1
            for k, v in f:
                c.execute("INSERT INTO src VALUES (?,?,?,?,?)", (sid, kind_s, None, k, v))
    for s in P["stored"]:
        sid += 1
        for k, v in s["fields"]:
            c.execute("INSERT INTO src VALUES (?,?,?,?,?)", (sid, "stored", s["ts"], k, v))
    about = []
    unclear_id = False
    if req["ref"] and et_idkey:
        if req["ref"][0] == "id":
            about = [r[0] for r in c.execute("SELECT DISTINCT sid FROM src WHERE k=? AND v=?",
                                             (et_idkey, req["ref"][1]))]
        else:
            rows = list(c.execute("""SELECT s1.sid, s2.v FROM src s1 JOIN src s2 ON s1.sid=s2.sid AND s2.k=?
                                     WHERE s1.k=? AND s1.v=?""", (et_idkey, et_namekey, req["ref"][1])))
            ids = {r[1] for r in rows}
            unclear_id = len(ids) >= 2
            about = [r[0] for r in rows] if not unclear_id else []
    # value in force per param (window over statement order; latest wins)
    vals, unclear = {}, set()
    for pn, val, op in c.execute("""SELECT param, value, open FROM (SELECT param, value, open,
                                    ROW_NUMBER() OVER (PARTITION BY param ORDER BY seq DESC) rn FROM mentions)
                                    WHERE rn=1"""):
        if pn in pdefs:
            if op:
                unclear.add(pn)
            else:
                vals[pn] = val
    if unclear_id and et_idkey and et_idkey not in vals:
        unclear.add(et_idkey)
    if about:
        q = "SELECT k, v FROM src WHERE sid IN (%s)" % ",".join("?" * len(about))
        for k, v in c.execute(q, about):
            if k in pdefs and k not in vals and k not in unclear and v not in ("not recorded", "unknown"):
                vals[k] = v
    # qualifier and status (user statement or a record about the target)
    qual = next((s["v"] for i in cur for s in P["conv"][i]["st"] if s["t"] == "qual"), None)
    rec_ids = [r[0] for r in c.execute("SELECT DISTINCT sid FROM src WHERE kind='record'")]
    rec_about = [x for x in about if x in rec_ids]
    if qual is None and rec_about:
        r = c.execute("SELECT v FROM src WHERE k=? AND sid IN (%s)" % ",".join("?" * len(rec_about)),
                      [lex["dimkey"]] + rec_about).fetchone()
        qual = r[0] if r else None
    status = None
    if rec_about:
        r = c.execute("SELECT v FROM src WHERE k='status' AND sid IN (%s)" % ",".join("?" * len(rec_about)),
                      rec_about).fetchone()
        status = r[0] if r else None
    out = {"kind": kind, "vals": vals, "unclear": sorted(unclear)}
    # ANSWER
    if kind == "catalog":
        out.update(outcome="ANSWER", tool=None)
        return out
    if kind == "info":
        f = req["field"]
        shown = any(s["t"] == "val" and s["p"] == f for i in cur for s in P["conv"][i]["st"])
        shown = shown or c.execute("SELECT 1 FROM mentions WHERE param=? AND seq>0", (f,)).fetchone() is not None
        if not shown and about and not unclear_id:
            for sid_, kd, ts, v in c.execute("SELECT sid, kind, ts, v FROM src WHERE k=? AND sid IN (%s)" % ",".join(
                    "?" * len(about)), [f] + about):
                if v in ("not recorded", "unknown"):
                    continue
                if kd == "stored" and pol["fresh"] is not None:
                    age = (dt.datetime.fromisoformat(now.replace(" ", "T")) -
                           dt.datetime.fromisoformat(ts.replace(" ", "T"))).total_seconds() / 60
                    if age > pol["fresh"]:
                        continue
                shown = True
        if shown:
            out.update(outcome="ANSWER", tool=None)
            return out
    # match (SQL): capability, scope NOT EXISTS, precondition, role
    role = P.get("role")
    c.execute("CREATE TABLE ctx(qual TEXT, status TEXT, role TEXT)")
    c.execute("INSERT INTO ctx VALUES (?,?,?)", (qual, status, role))
    match_sql = """SELECT t.name FROM tools t, ctx WHERE t.a=? AND t.o=? AND t.provider=0
        AND (t.restricted=0 OR ctx.qual IS NULL OR EXISTS (SELECT 1 FROM scope s WHERE s.tool=t.name
             AND s.value=ctx.qual))
        AND (t.pre IS NULL OR t.pre = ctx.status)
        AND (? = 0 OR EXISTS (SELECT 1 FROM roles r WHERE r.tool=t.name AND r.role=ctx.role))"""
    matched = [r[0] for r in c.execute(match_sql, (a, o, 1 if pol["role"] else 0))]
    acc, miss = {}, {}
    for n in matched:
        acc[n], miss[n] = check(byname[n], vals, unclear, now)
    fits = [n for n in matched if pol["invalid"] == "A" or acc[n]]
    comp = [n for n in fits if acc[n] and not miss[n]]
    c.execute("CREATE TABLE st(name TEXT, fit INTEGER, comp INTEGER)")
    for n in matched:
        c.execute("INSERT INTO st VALUES (?,?,?)", (n, 1 if n in fits else 0, 1 if n in comp else 0))
    row = c.execute("""SELECT CASE WHEN (SELECT COUNT(*) FROM st WHERE fit=1)=0 THEN 'UNABLE'
                                   WHEN (SELECT COUNT(*) FROM st WHERE comp=1)>=1 THEN 'CALL'
                                   ELSE 'ASK' END""").fetchone()[0]
    out.update(outcome=row, tool=None, fits=fits, complete=comp, accepts=acc, missing=miss)
    if row == "CALL":
        best = c.execute("""SELECT st.name FROM st JOIN tools t ON t.name=st.name WHERE comp=1
                            ORDER BY t.cost, t.pref DESC LIMIT 2""").fetchall()
        if len(comp) >= 2:
            if not pol["tie"]:
                raise ValueError("tie without POL-TIE")
            key = lambda n: (byname[n]["cost"], not byname[n]["pref"])
            cs = sorted(comp, key=key)
            if key(cs[0]) == key(cs[1]):
                raise ValueError("unbroken tie")
            out["tool"] = cs[0]
        else:
            out["tool"] = best[0][0]
    elif row == "ASK" and pol["chain"] and len(fits) == 1:
        T = fits[0]
        m = miss[T]
        if acc[T] and len(m) == 1 and m[0] not in unclear and m[0] not in [x for x in unclear]:
            provs = [r[0] for r in c.execute("""SELECT t.name FROM tools t JOIN returns r ON r.tool=t.name, ctx
                     WHERE t.provider=1 AND r.param=? AND (t.pre IS NULL OR t.pre=ctx.status)
                     AND (? = 0 OR EXISTS (SELECT 1 FROM roles x WHERE x.tool=t.name AND x.role=ctx.role))
                     AND (t.restricted=0 OR EXISTS (SELECT 1 FROM scope s WHERE s.tool=t.name AND s.value=ctx.qual))""",
                                             (m[0], 1 if pol["role"] else 0))]
            el = [n for n in provs if check(byname[n], vals, unclear, now) == (True, [])]
            if len(el) == 1:
                out.update(outcome="CALL", tool=el[0], chain=True, final=T)
    return out


def check(tool, vals, unclear, now):
    """(accepts, missing needed params) via the compiled JSON Schema."""
    inst = {}
    pmap = {p["name"]: p for p in tool["params"]}
    for n, p in pmap.items():
        if n in vals:
            inst[n] = prepass(p, vals[n], now)
    errs = list(jsonschema.Draft202012Validator(schema_of(tool)).iter_errors(inst))
    bad = [e for e in errs if e.validator != "required"]
    missing = [p["name"] for p in tool["params"] if p["required"] and p["name"] not in inst]
    missing = missing + [n for n in unclear if n in pmap and pmap[n]["required"] and n not in missing]
    return (not bad), missing
