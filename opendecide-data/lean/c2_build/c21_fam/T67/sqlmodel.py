"""T67 migration model: statement forms MG-S1..MG-S15, the Opus lock table (T67-LOCK-TABLE, hashed; a DRAFT fixture exists for tests only), table
size classes, and the SQL surface of each form (rendering + parse-back). Nothing here executes SQL.

Lock classes (T67-M5): LC0 (none / brief metadata lock), LC1 (blocks writes for a time proportional to table size), LC2 (blocks reads and writes,
time proportional to table size). MG-S12 (drop column), MG-S13 (drop table / truncate) and MG-S14 (backfill update) carry NO lock class: they are M01
forms on every card. The lock table covers only the M02 forms (S1-S11, S15) and is written by a SEPARATE fresh Opus session (T67-B7); the draft below is
the G0-lite's own UNVERIFIED assignment, flagged `draft` and refused for row builds by `LockTable.require_real()`.
"""
import json
import re

from LP_COMMON import util

from . import config as C

M02_FORMS = ("MG-S1", "MG-S2", "MG-S3", "MG-S4", "MG-S5", "MG-S6", "MG-S7", "MG-S8", "MG-S9", "MG-S10", "MG-S11", "MG-S15")
M01_ONLY_FORMS = ("MG-S12", "MG-S13", "MG-S14")
CREATE_FORMS = ("MG-S1", "MG-S5", "MG-S6")            # T50 does not express CREATE: never on clause-OFF cards, never in production rows
DRAFT_LOCKS = {"MG-S1": "LC0", "MG-S2": "LC0", "MG-S3": "LC0", "MG-S4": "LC2", "MG-S5": "LC1", "MG-S6": "LC0", "MG-S7": "LC1", "MG-S8": "LC0",
               "MG-S9": "LC2", "MG-S10": "LC2", "MG-S11": "LC0", "MG-S15": "LC0"}

# statement kind (M01 class) per form
KIND_OF_FORM = {"MG-S1": "create", "MG-S2": "alter", "MG-S3": "alter", "MG-S4": "alter", "MG-S5": "create", "MG-S6": "create", "MG-S7": "alter",
                "MG-S8": "alter", "MG-S9": "alter", "MG-S10": "alter", "MG-S11": "alter", "MG-S12": "alter", "MG-S13": "drop", "MG-S14": "update",
                "MG-S15": "alter"}


class LockTable(object):
    def __init__(self, data):
        self.data = data
        self.draft = bool(data.get("draft", False))
        self.locks = dict(data["locks"])
        self.sha = util.sha_obj({"locks": self.locks})
        if data.get("sha256") and data["sha256"] != self.sha:
            raise ValueError("lock table sha does not match its content")
        if set(self.locks) != set(M02_FORMS) or any(v not in C.LOCK_CLASSES for v in self.locks.values()):
            raise ValueError("lock table must cover exactly S1-S11 and S15 with LC0..LC2")

    @classmethod
    def load(cls, path):
        with open(path, "r", encoding="utf-8") as f:
            return cls(json.load(f))

    def require_real(self):
        if self.draft:
            raise ValueError("the DRAFT lock assignment cannot build rows: the Opus-written lock table (T67-B7) is required")
        return self

    def lock(self, form):
        return self.locks[form]


def draft_lock_table():
    return LockTable({"draft": True, "locks": dict(DRAFT_LOCKS)})


def size_class(rows):
    for sc, (lo, hi) in C.SIZE_RANGES.items():
        if lo <= rows <= hi:
            return sc
    raise ValueError("row count outside every size class")


def near_boundary(rows):
    """M-SIZE HIGH: within 10% of a class boundary."""
    for sc, (lo, hi) in C.SIZE_RANGES.items():
        for b in (lo, hi):
            if b > 100 and abs(rows - b) <= 0.1 * b:
                return True
    return False


# ---- SQL surface -------------------------------------------------------------------------------------------------------------------------
def render_statements(form, table, col, col2, idx, fk_tbl, style):
    """SQL text lines for a form. style: dict(upper: bool, qualified: schema|None, comment: bool). Returns a list of statements (each one string)."""
    kw = (lambda s: s.upper()) if style.get("upper") else (lambda s: s.lower())
    t = ("%s.%s" % (style["qualified"], table)) if style.get("qualified") else table
    c, c2 = col, col2
    if form == "MG-S1":
        return [kw("create table ") + t + " (" + "id bigint primary key, " + c + " text)"]
    if form == "MG-S2":
        return [kw("alter table ") + t + kw(" add column ") + c + " text"]
    if form == "MG-S3":
        return [kw("alter table ") + t + kw(" add column ") + c + kw(" integer default ") + "0"]
    if form == "MG-S4":
        return [kw("alter table ") + t + kw(" add column ") + c + kw(" timestamp default ") + "now()"]
    if form == "MG-S5":
        return [kw("create index ") + idx + kw(" on ") + t + " (" + c + ")"]
    if form == "MG-S6":
        return [kw("create index concurrently ") + idx + kw(" on ") + t + " (" + c + ")"]
    if form == "MG-S7":
        return [kw("alter table ") + t + kw(" add constraint ") + idx + kw(" foreign key ") + "(" + c + ")" + kw(" references ") + fk_tbl + " (id)"]
    if form == "MG-S8":
        return [kw("alter table ") + t + kw(" add constraint ") + idx + kw(" foreign key ") + "(" + c + ")" + kw(" references ") + fk_tbl + " (id)" + kw(" not valid"),
                kw("alter table ") + t + kw(" validate constraint ") + idx]
    if form == "MG-S9":
        return [kw("alter table ") + t + kw(" alter column ") + c + kw(" type ") + "bigint"]
    if form == "MG-S10":
        return [kw("alter table ") + t + kw(" alter column ") + c + kw(" set not null")]
    if form == "MG-S11":
        return [kw("alter table ") + t + kw(" add constraint ") + idx + kw(" check ") + "(" + c + kw(" is not null") + ")" + kw(" not valid"),
                kw("alter table ") + t + kw(" validate constraint ") + idx,
                kw("alter table ") + t + kw(" alter column ") + c + kw(" set not null")]
    if form == "MG-S12":
        return [kw("alter table ") + t + kw(" drop column ") + c]
    if form == "MG-S13":
        return [kw("drop table ") + t] if style.get("drop", True) else [kw("truncate table ") + t]
    if form == "MG-S14":
        return [kw("update ") + t + kw(" set ") + c + " = " + c2 + kw(" where ") + "id between 1 and 5000"]
    if form == "MG-S15":
        return [kw("alter table ") + t + kw(" rename column ") + c + kw(" to ") + c2]
    raise ValueError(form)


_FORM_PATTERNS = [
    ("MG-S1", re.compile(r"^create table (\S+) \(", re.I)),
    ("MG-S6", re.compile(r"^create index concurrently (\S+) on (\S+) \((\S+)\)$", re.I)),
    ("MG-S5", re.compile(r"^create index (\S+) on (\S+) \((\S+)\)$", re.I)),
    ("MG-S2", re.compile(r"^alter table (\S+) add column (\S+) text$", re.I)),
    ("MG-S3", re.compile(r"^alter table (\S+) add column (\S+) integer default 0$", re.I)),
    ("MG-S4", re.compile(r"^alter table (\S+) add column (\S+) timestamp default now\(\)$", re.I)),
    ("FK", re.compile(r"^alter table (\S+) add constraint (\S+) foreign key \((\S+)\) references (\S+) \(id\)( not valid)?$", re.I)),
    ("VALIDATE", re.compile(r"^alter table (\S+) validate constraint (\S+)$", re.I)),
    ("CHECK", re.compile(r"^alter table (\S+) add constraint (\S+) check \((\S+) is not null\) not valid$", re.I)),
    ("MG-S9", re.compile(r"^alter table (\S+) alter column (\S+) type bigint$", re.I)),
    ("NOTNULL", re.compile(r"^alter table (\S+) alter column (\S+) set not null$", re.I)),
    ("MG-S12", re.compile(r"^alter table (\S+) drop column (\S+)$", re.I)),
    ("DROP", re.compile(r"^drop table (\S+)$", re.I)),
    ("TRUNC", re.compile(r"^truncate table (\S+)$", re.I)),
    ("MG-S14", re.compile(r"^update (\S+) set (\S+) = (\S+) where id between 1 and 5000$", re.I)),
    ("MG-S15", re.compile(r"^alter table (\S+) rename column (\S+) to (\S+)$", re.I)),
    ("DML-DEL", re.compile(r"^delete from (\S+)( where .+)?$", re.I)),
    ("DML-UPD", re.compile(r"^update (\S+) set (.+?)( where .+)?$", re.I)),
    ("DML-INS", re.compile(r"^insert into (\S+) .+$", re.I)),
    ("GRANT", re.compile(r"^grant (\S+) on (\S+) to (\S+)$", re.I)),
]


def split_statements(sql):
    """Statements of a rendered SQL file (strip comments, split on ';')."""
    out = []
    for part in re.sub(r"--[^\n]*", "", sql).split(";"):
        s = " ".join(part.split())
        if s:
            out.append(s)
    return out


def parse_statement(stmt):
    """-> (pattern id, match) for one SQL statement or (None, None)."""
    for pid, rx in _FORM_PATTERNS:
        m = rx.match(stmt)
        if m:
            return pid, m
    return None, None


def parse_forms(sql):
    """Recover the ordered list of (form id | kind, table) from rendered SQL; multi-statement forms (S7/S8, S11) are folded back into one form."""
    stmts = split_statements(sql)
    out, i = [], 0
    while i < len(stmts):
        pid, m = parse_statement(stmts[i])
        if pid is None:
            raise ValueError("unparsed statement: %r" % stmts[i][:40])
        if pid == "FK":
            tbl = m.group(1)
            if m.group(5):                                              # not valid ... validate
                nxt = parse_statement(stmts[i + 1]) if i + 1 < len(stmts) else (None, None)
                if nxt[0] == "VALIDATE" and nxt[1].group(2) == m.group(2):
                    out.append(("MG-S8", tbl))
                    i += 2
                    continue
                raise ValueError("NOT VALID foreign key without its VALIDATE")
            out.append(("MG-S7", tbl))
        elif pid == "CHECK":
            tbl = m.group(1)
            v = parse_statement(stmts[i + 1]) if i + 1 < len(stmts) else (None, None)
            n = parse_statement(stmts[i + 2]) if i + 2 < len(stmts) else (None, None)
            if v[0] == "VALIDATE" and n[0] == "NOTNULL" and n[1].group(1) == tbl:
                out.append(("MG-S11", tbl))
                i += 3
                continue
            raise ValueError("incomplete check / validate / set not null chain")
        elif pid == "NOTNULL":
            out.append(("MG-S10", m.group(1)))
        elif pid in ("DROP", "TRUNC"):
            out.append(("MG-S13", m.group(1)))
        elif pid in ("MG-S5", "MG-S6"):
            out.append((pid, m.group(2)))
        elif pid in ("VALIDATE",):
            raise ValueError("stray VALIDATE")
        elif pid.startswith("DML-"):
            out.append((pid, m.group(1)))
        elif pid == "GRANT":
            out.append(("GRANT", m.group(2)))
        else:
            out.append((pid, m.group(1)))
        i += 1
    return out
