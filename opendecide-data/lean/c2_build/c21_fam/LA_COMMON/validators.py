"""Round-trip VALIDATORS (parse only; never execute) for rendered strings (G0-lite T50 section 3, K1/K16).

  tree-sitter-bash (MIT)  - Python binding `tree_sitter` + `tree_sitter_bash`; in-process, pure parse.
  mvdan/sh parser (BSD-3) - the Go `shfmt` binary run as `shfmt --to-json` with the rendered text on STDIN.
                            The interpreter package is NOT used. argv is a fixed list (never built from a
                            rendered string), shell=False, so no rendered string can reach a shell.
  sqlglot (MIT)           - parses the SQL statement text embedded in psql/sqlite3/mysql calls.

None of these is a labeller. A row where a validator's command SHAPE disagrees with the expander's shape is
dropped and counted (K1). bashlex and shlex are never imported (bashlex is GPL-3.0 and barred).

Availability: tree_sitter / tree_sitter_bash and shfmt are NOT installed on this Mac (checked 18 Oct 2026); the
adapters below are written against the documented APIs and report `None` ("unavailable") instead of guessing.
They have NOT been run live; the shape-comparison logic is unit-tested on synthetic validator output. sqlglot is
installed and tested live.
"""
import json
import shutil
import subprocess

SHFMT_ARGV = ["shfmt", "--to-json"]            # fixed list; the rendered text goes to stdin only
# Compound constructs. The expander refuses them (opaque control_flow) and emits ONE {"opaque": "control_flow"} marker per
# statement; the validators mirror that (one marker, bodies not descended into), so a control-flow row compares like for like
# (A64 skeptic: before this, every control-flow opaque row disagreed the moment a live validator was installed -> K1 drop).
TS_CONTROL_FLOW = ("for_statement", "c_style_for_statement", "while_statement", "if_statement", "case_statement",
                   "function_definition", "subshell", "compound_statement")
MVDAN_CONTROL_FLOW = ("IfClause", "WhileClause", "ForClause", "CaseClause", "FuncDecl", "Subshell", "Block")
PARSE_ERROR = [{"parse_error": True}]            # never equals an expander shape: a validator syntax error drops the rendering


# ------------------------------------------------------------------------------------------------ availability
def tree_sitter_available():
    try:
        import tree_sitter          # noqa: F401
        import tree_sitter_bash     # noqa: F401
        return True
    except Exception:
        return False


def shfmt_available():
    return shutil.which("shfmt") is not None


def availability():
    return {"tree_sitter_bash": tree_sitter_available(), "mvdan_sh_shfmt": shfmt_available(), "sqlglot": _sqlglot() is not None}


# ------------------------------------------------------------------------------------------------ tree-sitter
def tree_sitter_shape(text):
    """List of {"name","args"} for every simple command as written, source order; None if unavailable."""
    if not tree_sitter_available():
        return None
    import tree_sitter
    import tree_sitter_bash
    lang = tree_sitter.Language(tree_sitter_bash.language())
    parser = tree_sitter.Parser(lang)
    src = text.encode("utf-8")
    tree = parser.parse(src)
    if tree.root_node.has_error:
        return list(PARSE_ERROR)
    out = []

    def seg(node):
        return src[node.start_byte:node.end_byte].decode("utf-8")

    def walk(node):
        if node.type in ("command_substitution", "process_substitution", "string_content"):
            return
        if node.type in TS_CONTROL_FLOW:
            out.append({"opaque": "control_flow"})
            return
        if node.type == "command":
            name = node.child_by_field_name("name")
            args = node.children_by_field_name("argument")
            if name is not None:
                out.append({"name": seg(name), "args": [seg(a) for a in args]})
        for ch in node.children:
            walk(ch)

    walk(tree.root_node)
    return out


# ------------------------------------------------------------------------------------------------ mvdan/sh
def mvdan_shape(text):
    """Same shape from `shfmt --to-json`; None if shfmt is unavailable. Parse only."""
    if not shfmt_available():
        return None
    p = subprocess.run(SHFMT_ARGV, input=text.encode("utf-8"), capture_output=True, shell=False, timeout=20)
    if p.returncode != 0:
        return []
    ast = json.loads(p.stdout.decode("utf-8"))
    src = text.encode("utf-8")
    out = []

    def word_src(w):
        a, b = w["Pos"]["Offset"], w["End"]["Offset"]
        return src[a:b].decode("utf-8")

    def walk(node):
        if isinstance(node, dict):
            if node.get("Type") in ("CmdSubst", "ProcSubst"):
                return
            if node.get("Type") in MVDAN_CONTROL_FLOW:
                out.append({"opaque": "control_flow"})
                return
            if node.get("Type") == "CallExpr" and node.get("Args"):
                ws = [word_src(w) for w in node["Args"]]
                out.append({"name": ws[0], "args": ws[1:]})
            for v in node.values():
                walk(v)
        elif isinstance(node, list):
            for v in node:
                walk(v)

    walk(ast)
    return out


# ------------------------------------------------------------------------------------------------ shape compare
def shapes_agree(expander_shape, validator_shape):
    """expander_shape: expander.shape(text); validator_shape: list of {"name","args"} (and {"opaque": "control_flow"} markers,
    which the validator adapters emit for compound constructs exactly as the expander does). Compared statement by
    statement in source order. Other opaque markers on the expander side are ignored, as before. A validator parse error
    never agrees."""
    if validator_shape is None:
        return None
    mine = [{"name": s["name"], "args": s["args"]} if "name" in s else {"opaque": "control_flow"}
            for s in expander_shape if "name" in s or s.get("opaque") == "control_flow"]
    theirs = [{"name": v["name"], "args": v["args"]} if "name" in v else v for v in validator_shape]
    return mine == theirs


# ------------------------------------------------------------------------------------------------ sqlglot
def _sqlglot():
    try:
        import sqlglot          # noqa: F401
        return sqlglot
    except Exception:
        return None


def sql_info(text):
    """-> {"kind","table","has_predicate"} read by sqlglot, or None if sqlglot is missing / cannot parse."""
    sg = _sqlglot()
    if sg is None:
        return None
    from sqlglot import expressions as exp
    try:
        node = sg.parse_one(text)
    except Exception:
        return None
    kinds = [(exp.Select, "select"), (exp.Insert, "insert"), (exp.Update, "update"), (exp.Delete, "delete"),
             (exp.Drop, "drop"), (exp.Alter, "alter"), (exp.Create, "ctas")]
    kind = None
    for cls, nm in kinds:
        if isinstance(node, cls):
            kind = nm
            break
    if kind is None:
        tn = type(node).__name__.lower()
        if "truncate" in tn:
            kind = "truncate"
        elif "grant" in tn:
            kind = "grant"
        elif tn == "command":
            up = text.strip().upper()
            kind = "truncate" if up.startswith("TRUNCATE") else ("grant" if up.startswith("GRANT") else None)
    table = None
    t = node.find(exp.Table)
    if kind == "ctas":
        tbl = node.this.find(exp.Table) if hasattr(node, "this") and node.this is not None else None
        table = tbl.name if tbl is not None else None
    elif t is not None:
        table = t.name
    elif kind in ("truncate", "grant"):
        import re
        m = re.search(r"(?:TRUNCATE\s+TABLE|GRANT\s+\w+\s+ON)\s+([A-Za-z0-9_]+)", text, re.I)
        table = m.group(1) if m else None
    return {"kind": kind, "table": table, "has_predicate": node.args.get("where") is not None}


def sql_matches(stmt, text_info):
    """Does the sqlglot reading agree with the spec's SqlStmt?"""
    if text_info is None:
        return None
    want_table = "%s_%s" % (stmt.table, stmt.column) if stmt.kind == "ctas" else stmt.table
    ok = text_info["kind"] == stmt.kind and text_info["table"] == want_table
    if stmt.kind in ("update", "delete", "select"):
        ok = ok and text_info["has_predicate"] == stmt.has_predicate
    return ok
