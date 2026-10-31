"""Own SQL splitter / classifier for the migration files: strips `--` comments, splits on `;` outside quotes, normalises whitespace and keywords, and
classifies each statement into a small tag set. Statements are never run or planned; only their words are read."""
import re

from . import textview as V


def statements(text):
    out, cur, q = [], [], None
    lines = []
    for ln in text.split("\n"):
        if ln.lstrip().startswith("--"):
            continue
        lines.append(ln)
    s = "\n".join(lines)
    for ch in s:
        if q:
            cur.append(ch)
            if ch == q:
                q = None
        elif ch in ("'", '"'):
            q = ch
            cur.append(ch)
        elif ch == ";":
            out.append("".join(cur))
            cur = []
        else:
            cur.append(ch)
    if "".join(cur).strip():
        out.append("".join(cur))
    return [" ".join(x.split()) for x in out if x.strip()]


def _bare(table):
    t = table.strip('"')
    return t.split(".", 1)[1] if "." in t else t


_VOLATILE_FN = r"^[A-Za-z_][A-Za-z0-9_]*\s*\("


def classify(stmt):
    """-> dict(tag=..., table=..., ...) for one statement."""
    s = stmt.strip()
    low = s.lower()
    m = re.match(r"^create\s+table\s+(?:if\s+not\s+exists\s+)?(\S+)", low)
    if m:
        return dict(tag="create_table", table=_bare(m.group(1)))
    m = re.match(r"^create\s+(?:unique\s+)?index\s+(concurrently\s+)?(?:if\s+not\s+exists\s+)?(\S+)\s+on\s+(?:only\s+)?(\S+)", low)
    if m:
        return dict(tag="create_index_concurrently" if m.group(1) else "create_index", table=_bare(m.group(3)))
    m = re.match(r"^alter\s+table\s+(?:only\s+)?(?:if\s+exists\s+)?(\S+)\s+(.*)$", s, re.I)
    if m:
        table, rest = _bare(m.group(1)), m.group(2)
        mm = re.match(r"^add\s+column\s+(?:if\s+not\s+exists\s+)?(\S+)\s+(.*)$", rest, re.I)
        if mm:
            tail = mm.group(2)
            dm = re.search(r"\bdefault\s+(.*)$", tail, re.I)
            if not dm:
                return dict(tag="add_column", table=table, column=mm.group(1), default=None)
            dv = dm.group(1).strip()
            kind = "volatile" if re.match(_VOLATILE_FN, dv) or dv.lower() in ("current_timestamp", "current_date", "current_time", "localtimestamp") else "constant"
            return dict(tag="add_column", table=table, column=mm.group(1), default=kind)
        mm = re.match(r"^add\s+constraint\s+(\S+)\s+(foreign\s+key|check)\b(.*)$", rest, re.I)
        if mm:
            body = mm.group(3)
            not_valid = re.search(r"\bnot\s+valid\s*$", body, re.I) is not None
            if mm.group(2).lower().startswith("foreign"):
                return dict(tag="add_fk", table=table, name=mm.group(1), not_valid=not_valid)
            cm = re.search(r"\(\s*(\S+)\s+is\s+not\s+null\s*\)", body, re.I)
            return dict(tag="add_check", table=table, name=mm.group(1), not_valid=not_valid, column=cm.group(1) if cm else None, notnull_check=cm is not None)
        mm = re.match(r"^validate\s+constraint\s+(\S+)\s*$", rest, re.I)
        if mm:
            return dict(tag="validate", table=table, name=mm.group(1))
        mm = re.match(r"^alter\s+column\s+(\S+)\s+set\s+not\s+null\s*$", rest, re.I)
        if mm:
            return dict(tag="set_not_null", table=table, column=mm.group(1))
        mm = re.match(r"^alter\s+column\s+(\S+)\s+(?:set\s+data\s+)?type\s+(.*)$", rest, re.I)
        if mm:
            return dict(tag="alter_type", table=table, column=mm.group(1))
        mm = re.match(r"^drop\s+column\s+(?:if\s+exists\s+)?(\S+)", rest, re.I)
        if mm:
            return dict(tag="drop_column", table=table, column=mm.group(1))
        mm = re.match(r"^rename\s+(?:column\s+)?(\S+)\s+to\s+(\S+)\s*$", rest, re.I)
        if mm:
            return dict(tag="rename", table=table)
        return dict(tag="alter_other", table=table)
    m = re.match(r"^drop\s+table\s+(?:if\s+exists\s+)?(\S+)", low)
    if m:
        return dict(tag="drop_table", table=_bare(m.group(1)))
    m = re.match(r"^truncate\s+(?:table\s+)?(\S+)", low)
    if m:
        return dict(tag="truncate", table=_bare(m.group(1)))
    m = re.match(r"^delete\s+from\s+(\S+)(.*)$", low)
    if m:
        return dict(tag="delete", table=_bare(m.group(1)), predicate=bool(re.search(r"\bwhere\b", m.group(2))))
    m = re.match(r"^update\s+(\S+)\s+set\b(.*)$", low)
    if m:
        return dict(tag="update", table=_bare(m.group(1)), predicate=bool(re.search(r"\bwhere\b", m.group(2))))
    m = re.match(r"^(?:insert\s+(?:or\s+\w+\s+)?into|replace\s+into)\s+(\S+)", low)
    if m:
        upsert = re.match(r"^replace\s+into", low) or re.match(r"^insert\s+or\s+", low) or re.search(r"\bon\s+conflict\b.*\bdo\s+update\b", low) \
            or re.search(r"\bon\s+duplicate\s+key\s+update\b", low)
        return dict(tag="insert_upsert" if upsert else "insert", table=_bare(m.group(1)))
    m = re.match(r"^grant\s+.*?\bon\s+(?:table\s+)?(\S+)\s+to\b", low)
    if m:
        return dict(tag="grant", table=_bare(m.group(1)))
    raise V.Unparsable("sql statement")


def parse(artifact):
    return [classify(s) for s in statements(artifact)]


def group_forms(stmts):
    """Group the classified statements into the migration units a lock table talks about.
    -> list of dict(form=<int MG-S number> | None, tag=<M01 tag for non-form units>, table, predicate)."""
    units = []
    i, n = 0, len(stmts)
    validated_checks = set()
    while i < n:
        s = stmts[i]
        tag = s["tag"]
        if tag == "create_table":
            units.append(dict(form=1, tag=tag, table=s["table"]))
        elif tag == "add_column":
            f = 2 if s["default"] is None else (3 if s["default"] == "constant" else 4)
            units.append(dict(form=f, tag=tag, table=s["table"]))
        elif tag == "create_index":
            units.append(dict(form=5, tag=tag, table=s["table"]))
        elif tag == "create_index_concurrently":
            units.append(dict(form=6, tag=tag, table=s["table"]))
        elif tag == "add_fk":
            if s["not_valid"]:
                j = i + 1
                if j < n and stmts[j]["tag"] == "validate" and stmts[j]["name"] == s["name"]:
                    i = j
                units.append(dict(form=8, tag=tag, table=s["table"]))
            else:
                units.append(dict(form=7, tag=tag, table=s["table"]))
        elif tag == "add_check":
            j = i + 1
            if j < n and stmts[j]["tag"] == "validate" and stmts[j]["name"] == s["name"]:
                i = j
                if s.get("notnull_check"):
                    validated_checks.add((s["table"], s["column"]))
                    if i + 1 < n and stmts[i + 1]["tag"] == "set_not_null" and stmts[i + 1]["column"] == s["column"]:
                        i += 1
            units.append(dict(form=11 if s.get("notnull_check") else None, tag=tag if s.get("notnull_check") else "alter_other", table=s["table"]))
        elif tag == "set_not_null":
            units.append(dict(form=11 if (s["table"], s["column"]) in validated_checks else 10, tag=tag, table=s["table"]))
        elif tag == "alter_type":
            units.append(dict(form=9, tag=tag, table=s["table"]))
        elif tag == "rename":
            units.append(dict(form=15, tag=tag, table=s["table"]))
        elif tag == "validate":
            units.append(dict(form=None, tag="alter_other", table=s["table"]))
        elif tag == "drop_column":
            units.append(dict(form=12, tag=tag, table=s["table"]))
        elif tag in ("drop_table", "truncate"):
            units.append(dict(form=13, tag=tag, table=s["table"]))
        elif tag in ("delete", "update"):
            units.append(dict(form=None, tag=tag, table=s["table"], predicate=s.get("predicate", False)))
        else:
            units.append(dict(form=None, tag=tag, table=s["table"]))
        i += 1
    return units
