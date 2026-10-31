"""families/T40/solver_b.py: T40 solver B (paradigm sql_sqlite), written from G0_SPEC.md, not from plugin.py / resolver.py.

parse(row, ctx) reads the RENDERED state back into the generator's facts with its own regular expressions (registry block,
request line, earlier results, proposed call; or the file / old_str / new_str blocks of head C). solve_b(view) decides:
head A and B by relational queries (an in-memory SQLite database with tables tools, params, args, known values; JSON types
by json_type, ranges by BETWEEN, enums by instr, formats and id patterns by a regexp user function); head C by counting
non-overlapping matches with re and parsing the edited text with compile(..., PyCF_ONLY_AST). Imports nothing of the
solver-A side (no resolver, no schema, no plugin).
"""
from __future__ import annotations

import ast
import re
import sqlite3

CLOSED = "The listing above is complete: no other tool, file, rule or fact applies."
TOOL_RE = re.compile(r"^\[(?P<prov>[^\]]+)\] (?P<name>\S+) - (?P<purpose>.+?) \| menu: (?P<menu>\S+)$")
PARAM_RE = re.compile(r"^(?P<n>[A-Za-z0-9_.-]+)(?P<r>\*)? (?P<t>.+) \((?P<l>[^()]*)\)$")
ARG_RE = re.compile(r'([^,=\s]+)=("[^"]*"|[^,]*)')
EDIT_RE = re.compile(r"File (?P<path>\S+):\n<<<\n(?P<file>.*?)\n>>>\n" + re.escape(CLOSED) +
                     r"\n\nProposed str_replace edit on (?P=path):\nold_str:\n<<<\n(?P<old>.*?)\n>>>\nnew_str:\n<<<\n(?P<new>.*?)\n>>>$",
                     re.S)
HEAD_OF = {"a": "A", "b": "B", "c": "C"}
YES_IF = {  # qform -> (underlying label that is the good outcome, polarity of the question)
    "ya_valid": ("VALID", 1), "ya_dneg": ("VALID", 1), "ya_reject": ("VALID", -1), "ya_notvalid": ("VALID", -1),
    "yb_call": ("CALL", 1), "yb_bdneg": ("CALL", 1), "yb_hold": ("CALL", -1), "yb_notcall": ("CALL", -1),
    "yc_applies": ("APPLIES_ONCE", 1), "yc_cdneg": ("APPLIES_ONCE", 1), "yc_fails": ("APPLIES_ONCE", -1),
    "yc_notapplies": ("APPLIES_ONCE", -1)}


class ParseError(ValueError):
    pass


def _one(rx, text, what):
    ms = list(rx.finditer(text))
    if len(ms) != 1:
        raise ParseError(f"{len(ms)} {what}(s) in the row")
    return ms[0]


def parse(row: dict, ctx) -> dict:
    state = row["state"]
    wording = ctx.skin(row["meta"]["wording_id"])
    qform = wording.qform
    head = HEAD_OF[qform[1]]
    view = {"qform": qform, "head": head}
    if head == "C":
        m = _one(EDIT_RE, state, "edit block")
        view.update(path=m["path"], file=m["file"], old=m["old"], new=m["new"])
    else:
        lines = state.split("\n")
        i0 = next((i for i, x in enumerate(lines) if x.startswith("Registry (")), None)
        if i0 is None:
            raise ParseError("no registry block")
        tools, i = [], i0 + 1
        while i < len(lines) and lines[i] != CLOSED:
            m = TOOL_RE.match(lines[i])
            if not m:
                raise ParseError(f"tool line {lines[i]!r}")
            sig = lines[i + 1]
            if not sig.startswith("  "):
                raise ParseError("signature line")
            params = []
            for part in sig[2:].split("; "):
                pm = PARAM_RE.match(part)
                if not pm:
                    raise ParseError(f"parameter {part!r}")
                params.append([pm["n"], pm["t"], pm["r"] == "*", pm["l"]])
            tools.append({"provider": m["prov"], "name": m["name"], "purpose": m["purpose"], "menu": m["menu"],
                          "params": params})
            i += 2
        if i >= len(lines):
            raise ParseError("registry is not closed")
        rest = lines[i + 1:]
        req_line = [x for x in rest if x.startswith("Request: ")]
        if len(req_line) != 1:
            raise ParseError("request line")
        rm = re.fullmatch(r'Request: "(.*)\."', req_line[0])
        if not rm:
            raise ParseError("request quoting")
        parts = rm.group(1).split(". ")
        clauses, provider = [], None
        for part in parts[1:]:
            lab, sep, val = part.partition(": ")
            if not sep:
                raise ParseError(f"clause {part!r}")
            if lab == "Provider":
                provider = val
            else:
                clauses.append([lab, val])
        results = []
        for x in rest:
            if x.startswith("Earlier result from "):
                tool, _, body = x[len("Earlier result from "):].partition(": ")
                results.append([tool, [kv.split(" = ", 1) for kv in body.split("; ")]])
        view.update(tools=tools, request={"sentence": parts[0], "clauses": clauses, "provider": provider},
                    results=results, call=None)
        call_lines = [x for x in rest if x.startswith("Proposed call: ")]
        if head == "A":
            if len(call_lines) != 1:
                raise ParseError("call line")
            cm = re.fullmatch(r"Proposed call: (\S+?)\((.*)\)", call_lines[0])
            if not cm:
                raise ParseError("call syntax")
            args = []
            for am in ARG_RE.finditer(cm.group(2)):
                v = am.group(2)
                quoted = v.startswith('"')
                args.append([am.group(1), v[1:-1] if quoted else v, not quoted])
            view["call"] = {"callee": cm.group(1), "args": args}
        elif call_lines:
            raise ParseError("a request row shows a call")
    if row["qtype"] == "choice":
        view["options"] = list(row["options"])
    return view


# ------------------------------------------------------------------------------------------------ solving

def _type_cols(t: str):
    """(base, lo, hi, values, pattern) of a printed type."""
    m = re.fullmatch(r"(integer|number) (-?\d+)\.\.(-?\d+)", t)
    if m:
        return m.group(1), float(m.group(2)), float(m.group(3)), "", ""
    m = re.fullmatch(r"enum\((.*)\)", t)
    if m:
        return "enum", 0.0, 0.0, m.group(1), ""
    m = re.fullmatch(r"id\(([a-z]+_)\)", t)
    if m:
        return "id", 0.0, 0.0, "", re.escape(m.group(1)) + r"\d+"
    if t == "email":
        return "email", 0.0, 0.0, "", r"[\w.%+-]+@[\w-]+(?:\.[\w-]+)+"
    if t in ("string", "date", "integer", "number", "boolean"):
        return t, 0.0, 0.0, "", ""
    raise ParseError(f"type {t!r}")


def _db(view: dict) -> sqlite3.Connection:
    con = sqlite3.connect(":memory:")
    con.create_function("rx", 2, lambda pat, s: 1 if re.fullmatch(pat, s) else 0)
    con.executescript("""
        CREATE TABLE tools(id INTEGER PRIMARY KEY, provider TEXT, name TEXT, purpose TEXT, menu TEXT);
        CREATE TABLE params(tool INTEGER, name TEXT, base TEXT, lo REAL, hi REAL, vals TEXT, pat TEXT, req INTEGER, label TEXT);
        CREATE TABLE args(pos INTEGER, name TEXT, lit TEXT, bare INTEGER);
        CREATE TABLE known(value TEXT);
        CREATE TABLE clauses(label TEXT);
        CREATE TABLE rkeys(name TEXT);""")
    for i, t in enumerate(view["tools"]):
        con.execute("INSERT INTO tools VALUES(?,?,?,?,?)", (i, t["provider"], t["name"], t["purpose"], t["menu"]))
        for n, typ, req, lab in t["params"]:
            con.execute("INSERT INTO params VALUES(?,?,?,?,?,?,?,?,?)", (i, n, *_type_cols(typ), int(req), lab))
    rq = view["request"]
    for lab, val in rq["clauses"]:
        con.execute("INSERT INTO clauses VALUES(?)", (lab.lower(),))
        con.execute("INSERT INTO known VALUES(?)", (val,))
    if rq["provider"]:
        con.execute("INSERT INTO known VALUES(?)", (rq["provider"],))
    for _tool, fields in view["results"]:
        for k, v in fields:
            con.execute("INSERT INTO rkeys VALUES(?)", (k,))
            con.execute("INSERT INTO known VALUES(?)", (v,))
    if view["call"]:
        for j, (n, lit, bare) in enumerate(view["call"]["args"]):
            con.execute("INSERT INTO args VALUES(?,?,?,?)", (j, n, lit, int(bare)))
    return con


TYPE_SQL = """
SELECT 1 FROM args a JOIN params p ON p.tool = :t AND p.name = a.name
WHERE CASE p.base
  WHEN 'integer' THEN NOT (json_type(CASE WHEN a.bare = 1 THEN a.lit ELSE json_quote(a.lit) END) = 'integer'
                           AND CAST(a.lit AS REAL) BETWEEN p.lo AND p.hi AND a.bare = 1)
  WHEN 'number' THEN NOT (json_type(CASE WHEN a.bare = 1 THEN a.lit ELSE json_quote(a.lit) END) IN ('integer', 'real')
                          AND CAST(a.lit AS REAL) BETWEEN p.lo AND p.hi AND a.bare = 1)
  WHEN 'string' THEN a.bare = 1
  WHEN 'boolean' THEN NOT (a.bare = 1 AND a.lit IN ('true', 'false'))
  WHEN 'email' THEN NOT (a.bare = 0 AND rx(p.pat, a.lit))
  WHEN 'date' THEN NOT (a.bare = 0 AND rx('\\d{4}-\\d{2}-\\d{2}', a.lit) AND COALESCE(date(a.lit) = a.lit, 0))
  WHEN 'enum' THEN NOT (a.bare = 0 AND instr('|' || p.vals || '|', '|' || a.lit || '|') > 0)
  WHEN 'id' THEN NOT (a.bare = 0 AND rx(p.pat, a.lit))
  ELSE 1 END
LIMIT 1"""


def call_label(view: dict) -> str:
    con = _db(view)
    callee = view["call"]["callee"]
    if "::" in callee:
        prov, name = callee.split("::", 1)
        rows = con.execute("SELECT id FROM tools WHERE provider = ? AND name = ?", (prov, name)).fetchall()
    else:
        rows = con.execute("SELECT id FROM tools WHERE name = ?", (callee,)).fetchall()
    if not rows:
        return "NONEXISTENT_TOOL"
    if len(rows) > 1:
        return "AMBIGUOUS_PROVIDER"
    t = rows[0][0]
    if con.execute("SELECT menu FROM tools WHERE id = ?", (t,)).fetchone()[0] != "yes":
        return "OFF_MENU"
    n_args = con.execute("SELECT COUNT(*) FROM args").fetchone()[0]
    n_own = con.execute("SELECT COUNT(*) FROM args a WHERE EXISTS (SELECT 1 FROM params p WHERE p.tool = ? AND p.name = a.name)",
                        (t,)).fetchone()[0]
    if n_args and not n_own and con.execute(
            "SELECT 1 FROM tools y WHERE y.id != ? AND NOT EXISTS (SELECT 1 FROM args a WHERE NOT EXISTS "
            "(SELECT 1 FROM params p WHERE p.tool = y.id AND p.name = a.name)) LIMIT 1", (t,)).fetchone():
        return "BORROWED_SIGNATURE"
    dup = con.execute("SELECT 1 FROM args GROUP BY name HAVING COUNT(*) > 1").fetchone()
    missing = con.execute("SELECT 1 FROM params p WHERE p.tool = ? AND p.req = 1 AND NOT EXISTS "
                          "(SELECT 1 FROM args a WHERE a.name = p.name) LIMIT 1", (t,)).fetchone()
    unknown = con.execute("SELECT 1 FROM args a WHERE NOT EXISTS (SELECT 1 FROM params p WHERE p.tool = ? AND p.name = a.name) "
                          "LIMIT 1", (t,)).fetchone()
    if dup or missing or unknown:
        return "BAD_ARGS"
    try:
        bad_type = con.execute(TYPE_SQL, {"t": t}).fetchone()
    except sqlite3.OperationalError:
        bad_type = (1,)
    if bad_type:
        return "TYPE_VIOLATION"
    if con.execute("SELECT 1 FROM args WHERE lit NOT IN (SELECT value FROM known) LIMIT 1").fetchone():
        return "UNGROUNDED_VALUE"
    return "VALID"


def action_label(view: dict) -> str:
    con = _db(view)
    rq = view["request"]
    q = "SELECT id, provider FROM tools WHERE menu = 'yes' AND instr(lower(?), lower(purpose)) > 0"
    args = [rq["sentence"]]
    if rq["provider"]:
        q += " AND provider = ?"
        args.append(rq["provider"])
    rows = con.execute(q, args).fetchall()
    if not rows:
        return "CANNOT_ANSWER"
    if len({p for _, p in rows}) > 1:
        return "ASK_FOLLOWUP"
    gap = con.execute("SELECT 1 FROM params p WHERE p.tool = ? AND p.req = 1 AND lower(p.label) NOT IN (SELECT label FROM clauses) "
                      "AND p.name NOT IN (SELECT name FROM rkeys) LIMIT 1", (rows[0][0],)).fetchone()
    return "ASK_FOLLOWUP" if gap else "CALL"


def edit_label(view: dict) -> str:
    text, old, new = view["file"], view["old"], view["new"]
    spans = [m.start() for m in re.finditer(re.escape(old), text)] if old else []
    if not spans:
        return "NO_MATCH"
    if len(spans) > 1:
        return "MULTIPLE"
    edited = text[:spans[0]] + new + text[spans[0] + len(old):]
    try:
        compile(edited, "<edit>", "exec", flags=ast.PyCF_ONLY_AST)
    except (SyntaxError, ValueError):
        return "BREAKS_SYNTAX"
    return "APPLIES_ONCE"


def solve_b(view: dict):
    head = view["head"]
    lab = {"A": call_label, "B": action_label, "C": edit_label}[head](view)
    qf = view["qform"]
    if qf in YES_IF:
        good, pol = YES_IF[qf]
        yes = lab == good
        return int(yes if pol == 1 else not yes)
    return lab
