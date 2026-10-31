"""GEN solver B, TABLE sub-block (TB-B1 .. TB-B4).

Method (G0-lite section 2, solver B column): an independent AST-to-SQL compiler run on an in-memory stdlib SQLite database, plus a
table-carrier parser that reads the serialised table text back (TBL-PIPE, TBL-CSV, TBL-TSV, TBL-KV, TBL-JSON).
Decimal columns are stored as integer hundredths and averages are formed from an integer SUM and COUNT, then rounded half up with
fractions.Fraction, so no floating point enters an answer.
"""
import json
import re
import sqlite3
from fractions import Fraction

from b_questions import read_question
from bcommon import ParseFail, Reject, statements, pick_unique, norm_text, fnum, numstr, round_half_up, name_list, scene_and_body

INT_RE = re.compile(r"^-?\d+$")
DEC_RE = re.compile(r"^-?\d+\.\d+$")
DATE_RE = re.compile(r"^\d{4}-\d\d-\d\d$")
IDENT = r"[a-z][a-z0-9_]*"
LABEL_RE = re.compile(r"^(?:Table (?:named )?)?(%s):$" % IDENT)
INTRO = ("Consider the data below.", "Table data follows.", "Data:")
JOIN_SENT = [re.compile(r"^The tables are joined where (%s) in the first table equals (%s) in the second$" % (IDENT, IDENT)),
             re.compile(r"^Join the two tables on (%s) = (%s)$" % (IDENT, IDENT))]
ROUND_FILLER = re.compile(r"^(?:Give|Round) the result to (\d+) decimal places, (?:rounding )?half up$")


# ---------------------------------------------------------------------------------------------------------------------
# carrier parsing

class Table(object):
    def __init__(self, label, cols, rows):
        self.label = label
        self.cols = cols          # list of column names
        self.rows = rows          # list of lists of strings
        self.types = None

    def infer_types(self):
        types = []
        for j, c in enumerate(self.cols):
            vals = [r[j] for r in self.rows]
            if vals and all(INT_RE.match(v) for v in vals):
                types.append("int")
            elif vals and all(DEC_RE.match(v) for v in vals):
                types.append("dec")
            elif vals and all(DATE_RE.match(v) for v in vals):
                types.append("date")
            else:
                types.append("name" if j == 0 else "cat")
        self.types = types


def _body(lines, i, carrier):
    """Return (cols, rows, next_index) for the table body starting at lines[i]."""
    n = len(lines)
    if carrier == "TBL-JSON":
        if i >= n:
            raise ParseFail("table_body_missing", "")
        try:
            data = json.loads(lines[i])
        except ValueError:
            raise ParseFail("bad_json_table", "")
        if not isinstance(data, list) or not data or not all(isinstance(d, dict) for d in data):
            raise ParseFail("bad_json_table", "")
        cols = list(data[0].keys())
        rows = []
        for d in data:
            if list(d.keys()) != cols:
                raise ParseFail("json_rows_differ_in_columns", "")
            rows.append([str(d[c]) for c in cols])
        return cols, rows, i + 1
    if carrier == "TBL-KV":
        rows, cols = [], None
        while i < n:
            m = re.match(r"^row \d+: (.+)$", lines[i])
            if not m:
                break
            pairs = [p.split("=", 1) for p in re.split(r";\s*", m.group(1))]
            if any(len(p) != 2 for p in pairs):
                raise ParseFail("bad_kv_row", lines[i])
            c = [p[0] for p in pairs]
            if cols is None:
                cols = c
            elif c != cols:
                raise ParseFail("kv_rows_differ_in_columns", "")
            rows.append([p[1] for p in pairs])
            i += 1
        if not rows:
            raise ParseFail("table_body_missing", "")
        return cols, rows, i
    sep = {"TBL-CSV": ",", "TBL-TSV": "\t", "TBL-PIPE": " | "}.get(carrier)
    if sep is None:
        raise ParseFail("unknown_table_carrier", str(carrier))
    if i >= n or sep not in lines[i]:
        raise ParseFail("table_body_missing", "")
    cols = lines[i].split(sep)
    cols = [c.strip() for c in cols]
    rows = []
    i += 1
    while i < n:
        ln = lines[i]
        if sep not in ln:
            break
        cells = [c.strip() for c in ln.split(sep)]
        if len(cells) != len(cols) or any((" " in c) for c in cells):
            break
        rows.append(cells)
        i += 1
    if not rows:
        raise ParseFail("table_has_no_rows", "")
    return cols, rows, i


def parse_tables(stem, carrier):
    _dom, rest_text = scene_and_body(stem)
    body = rest_text.split("\n")
    lines = [ln.rstrip() for ln in body]
    lines = [ln for ln in lines if ln.strip()]
    tables, other = [], []
    i = 0
    while i < len(lines):
        ln = lines[i].strip() if carrier != "TBL-TSV" else lines[i]
        m = LABEL_RE.match(lines[i].strip())
        if m:
            cols, rows, j = _body(lines, i + 1, carrier)
            width = len(cols)
            if any(len(r) != width for r in rows):
                raise ParseFail("ragged_table", m.group(1))
            if len(set(cols)) != len(cols):
                raise ParseFail("duplicate_column", m.group(1))
            if not all(re.match("^%s$" % IDENT, c) for c in cols):
                raise ParseFail("column_name_not_identifier", m.group(1))     # names go into SQL text: only plain identifiers are accepted
            t = Table(m.group(1), cols, rows)
            t.infer_types()
            tables.append(t)
            i = j
        else:
            other.append(lines[i].strip())
            i += 1
    return tables, other


# ---------------------------------------------------------------------------------------------------------------------
# conditions and queries

OPS = [("at least", ">="), ("at most", "<="), ("more than", ">"), ("less than", "<"), ("on or before", "<="), ("on or after", ">="),
       ("before", "<"), ("after", ">")]
COND_ATOM = re.compile(r"^(%s) is (?:(at least|at most|more than|less than|on or before|on or after|before|after) )?(\S+)$" % IDENT)


def parse_cond(text):
    text = text.strip().replace("on or before", "on_or_before").replace("on or after", "on_or_after")
    has_and = " and " in text
    has_or = " or " in text
    if has_and and has_or:
        raise ParseFail("mixed_and_or", text)
    conj = "or" if has_or else "and"
    parts = [p.replace("on_or_before", "on or before").replace("on_or_after", "on or after") for p in re.split(r"\s+(?:and|or)\s+", text)]
    out = []
    for p in parts:
        m = COND_ATOM.match(p.strip())
        if not m:
            raise ParseFail("condition_atom", p)
        word = m.group(2)
        op = "=" if word is None else dict(OPS)[word]
        out.append({"col": m.group(1), "op": op, "val": m.group(3)})
    return conj, out


AGG_WORD = {"total": "sum", "minimum": "min", "maximum": "max", "average": "avg", "number": "count"}


class Q(object):
    """Query AST: tables list, agg (fn, col), where (conj, atoms), group col, join keys."""

    def __init__(self):
        self.agg_fn = None
        self.agg_col = None
        self.conj = "and"
        self.where = []
        self.group = None
        self.highest = None
        self.rank_rows = False


def _resolve(tables, col):
    hits = [(k, t) for k, t in enumerate(tables) if col in t.cols]
    if len(hits) != 1:
        raise ParseFail("column_not_found_or_ambiguous", col)
    return hits[0]


# ---------------------------------------------------------------------------------------------------------------------
# SQLite evaluation

def _scaled(tbl, j, text):
    """Stored integer for a cell: dec -> hundredths, int -> itself, others -> text."""
    ty = tbl.types[j]
    if ty == "int":
        return int(text)
    if ty == "dec":
        f = Fraction(text) * 100
        if f.denominator != 1:
            raise ParseFail("decimal_with_more_than_two_places", text)
        return int(f)
    return text


class DB(object):
    def __init__(self, tables, join):
        self.tables = tables
        self.join = join
        self.con = sqlite3.connect(":memory:")
        cur = self.con.cursor()
        for k, t in enumerate(tables):
            cdefs = []
            for j, c in enumerate(t.cols):
                cdefs.append('"%s" %s' % (c, "INTEGER" if t.types[j] in ("int", "dec") else "TEXT"))
            cur.execute('CREATE TABLE "t%d" (%s)' % (k, ", ".join(cdefs)))
            for r in t.rows:
                cur.execute('INSERT INTO "t%d" VALUES (%s)' % (k, ", ".join("?" * len(t.cols))), [_scaled(t, j, v) for j, v in enumerate(r)])
        self.con.commit()

    def from_clause(self):
        if self.join is None:
            return '"t0"'
        li, rj = self.join
        return '"t0" JOIN "t1" ON "t0"."%s" = "t1"."%s"' % (self.tables[0].cols[li], self.tables[1].cols[rj])

    def where_sql(self, conj, atoms):
        if not atoms:
            return "", []
        parts, args = [], []
        for a in atoms:
            k, t = a["tbl"]
            j = t.cols.index(a["col"])
            ty = t.types[j]
            qcol = '"t%d"."%s"' % (k, a["col"])
            val = a["val"]
            if ty in ("int", "dec"):
                if not (INT_RE.match(val) or DEC_RE.match(val)):
                    raise ParseFail("non_numeric_literal_for_numeric_column", val)
                f = Fraction(val) * (100 if ty == "dec" else 1)
                lit = int(f) if f.denominator == 1 else float(f)
            else:
                if a["op"] != "=" and ty != "date":
                    raise ParseFail("ordering_on_text_column", a["col"])
                lit = val
            parts.append("%s %s ?" % (qcol, a["op"]))
            args.append(lit)
        return " WHERE " + (" AND " if conj == "and" else " OR ").join(parts), args

    def _col_ref(self, tbl_idx, col):
        return '"t%d"."%s"' % (tbl_idx, col)

    def aggregate(self, fn, col_ref, scale, conj, atoms, places=2):
        w, args = self.where_sql(conj, atoms)
        cur = self.con.cursor()
        if fn == "count":
            cur.execute("SELECT COUNT(*) FROM " + self.from_clause() + w, args)
            return Fraction(cur.fetchone()[0])
        if fn in ("sum", "min", "max"):
            cur.execute("SELECT %s(%s) FROM %s%s" % (fn.upper(), col_ref, self.from_clause(), w), args)
            v = cur.fetchone()[0]
            if v is None:
                raise Reject("empty_selection", fn)
            return Fraction(v, scale)
        if fn == "avg":
            cur.execute("SELECT SUM(%s), COUNT(*) FROM %s%s" % (col_ref, self.from_clause(), w), args)
            s, n = cur.fetchone()
            if not n:
                raise Reject("empty_selection", fn)
            return Fraction(s, scale * n)
        raise ParseFail("unknown_aggregate", fn)

    def groups(self, fn, col_ref, scale, gcol_ref, conj, atoms):
        w, args = self.where_sql(conj, atoms)
        cur = self.con.cursor()
        if fn == "avg":
            cur.execute("SELECT %s, SUM(%s), COUNT(*) FROM %s%s GROUP BY %s" % (gcol_ref, col_ref, self.from_clause(), w, gcol_ref), args)
            return dict((g, Fraction(s, scale * n)) for g, s, n in cur.fetchall())
        cur.execute("SELECT %s, %s(%s) FROM %s%s GROUP BY %s" % (gcol_ref, fn.upper(), col_ref, self.from_clause(), w, gcol_ref), args)
        return dict((g, Fraction(v, scale)) for g, v in cur.fetchall())

    def extreme_row(self, col_ref, highest, name_ref, conj, atoms):
        w, args = self.where_sql(conj, atoms)
        cur = self.con.cursor()
        cur.execute("SELECT %s, %s FROM %s%s ORDER BY %s %s" % (name_ref, col_ref, self.from_clause(), w, col_ref, "DESC" if highest else "ASC"), args)
        rows = cur.fetchall()
        if not rows:
            raise Reject("empty_selection", "extreme")
        if len(rows) > 1 and rows[0][1] == rows[1][1]:
            raise Reject("tie_for_extreme", "")
        return rows[0][0]


# ---------------------------------------------------------------------------------------------------------------------
# question frames

Q_B2_PHRASE = re.compile(r"^(?P<hl>highest|lowest) (?:(?P<agg>total|minimum|average|maximum) )?(?P<col>%s)(?: per (?P<grp>%s))?(?:, counting only rows where (?P<cond>.+))?$" % (IDENT, IDENT))
CL_VALUE = re.compile(r"^the (?P<agg>total|minimum|average|maximum) of (?P<col>%s) over rows where (?P<rest>.+) is (?P<val>-?\d+(?:\.\d+)?)$" % IDENT)
CL_COUNT = re.compile(r"^exactly (?P<n>-?\d+(?:\.\d+)?) rows satisfy: (?P<cond>.+)$")
CL_ROW = re.compile(r"^the row with the (?P<hl>lowest|highest) (?P<col>%s)(?: among rows where (?P<cond>.+))? is (?P<name>\S+)$" % IDENT)


def _atoms(tables, conj_atoms):
    conj, atoms = conj_atoms
    out = []
    for a in atoms:
        k, t = _resolve(tables, a["col"])
        out.append({"col": a["col"], "op": a["op"], "val": a["val"], "tbl": (k, t)})
    return conj, out


def _find_join(tables):
    if len(tables) != 2:
        raise ParseFail("join_needs_two_tables", str(len(tables)))
    L, R = tables
    cands = []
    for i, ci in enumerate(L.cols):
        if L.types[i] != "name":
            continue
        lv = set(r[i] for r in L.rows)
        for j, cj in enumerate(R.cols):
            if R.types[j] not in ("name", "cat"):
                continue
            rv = set(r[j] for r in R.rows)
            if rv and rv <= lv:
                cands.append((i, j))
    if not cands:
        raise ParseFail("no_join_key", "")
    if (0, 0) in cands:
        return (0, 0)
    if len(cands) != 1:
        raise ParseFail("ambiguous_join_key", str(cands))
    return cands[0]


def _col_info(tables, col):
    k, t = _resolve(tables, col)
    j = t.cols.index(col)
    ty = t.types[j]
    return k, t, j, ty


def _opt_numbers(options):
    out = []
    for o in options:
        s = o.strip()
        if not re.match(r"^-?\d+(?:\.\d+)?$", s):
            raise ParseFail("option_not_a_number", o)
        out.append(Fraction(s))
    return out


def _canon_where(tables, conj, atoms):
    return [{"col": a["col"], "op": a["op"], "t": a["tbl"][0], "val": a["val"]} for a in atoms]


def _tables_canon(tables):
    rows_out = []
    out = []
    for t in tables:
        rr = []
        for r in t.rows:
            rr.append([int(v) if t.types[j] == "int" else v for j, v in enumerate(r)])
        out.append({"label": t.label, "columns": [[c, t.types[j]] for j, c in enumerate(t.cols)], "rows": rr})
    return out


def _cmp_fraction(x):
    return numstr(x)


def solve(form, stem, options, carrier=None):
    if carrier is None:
        raise ParseFail("carrier_missing", "")
    key, qs, remainder = read_question("q." + form, stem)
    tables, other = parse_tables(remainder, carrier)
    if not tables:
        raise ParseFail("no_table", "")
    if form == "TB-B3" and len(tables) != 2:
        raise ParseFail("join_needs_two_tables", "")
    if form != "TB-B3" and len(tables) != 1:
        raise ParseFail("one_table_expected", str(len(tables)))
    # the lines that are not table data: intro words and the rounding sentence (nothing else may be there)
    places = 2
    stated_join = None
    for ln in other:
        if ln in INTRO:
            continue
        for s in statements(ln, scene=False):
            m = ROUND_FILLER.match(s)
            if m:
                places = int(m.group(1))
                continue
            jm = next((r.match(s) for r in JOIN_SENT if r.match(s)), None)
            if jm:
                if stated_join is not None:
                    raise ParseFail("join_stated_twice", s)
                stated_join = (jm.group(1), jm.group(2))
                continue
            raise ParseFail("unread_sentences", s)
    join = None
    if form == "TB-B3":
        if stated_join is None:
            raise ParseFail("join_key_not_stated", "")
        L, R = tables
        if stated_join[0] not in L.cols or stated_join[1] not in R.cols:
            raise ParseFail("join_key_unknown_column", str(stated_join))
        join = (L.cols.index(stated_join[0]), R.cols.index(stated_join[1]))
    elif stated_join is not None:
        raise ParseFail("join_stated_for_a_single_table", "")
    db = DB(tables, join)
    if form == "TB-B1":
        return _b1(db, tables, qs, options, places, form)
    if form == "TB-B3":
        return _b3(db, tables, qs, options, places, join)
    if form == "TB-B2":
        return _b2(db, tables, qs, options)
    if form == "TB-B4":
        return _b4(db, tables, qs, options, places)
    raise ParseFail("not_a_table_form", form)


def _agg_value(db, tables, fn, col, conj, atoms, places):
    k, t, j, ty = _col_info(tables, col)
    if ty not in ("int", "dec"):
        raise ParseFail("aggregate_on_non_numeric_column", col)
    scale = 100 if ty == "dec" else 1
    v = db.aggregate(fn, db._col_ref(k, col), scale, conj, atoms)
    if fn == "avg":
        v = round_half_up(v, places)
    return v


def _pick_number(options, value, what):
    nums = _opt_numbers(options)
    return pick_unique([i for i, x in enumerate(nums) if x == value], "%s=%s" % (what, value))


def _b1(db, tables, qs, options, places, form):
    if qs["agg"] not in AGG_WORD or not re.match("^%s$" % IDENT, qs["col"]):
        raise ParseFail("aggregate_phrase", qs["agg"])
    fn = AGG_WORD[qs["agg"]]
    col = qs["col"]
    conj, atoms = _atoms(tables, parse_cond(qs["cond"]))
    v = _agg_value(db, tables, fn, col, conj, atoms, places)
    idx = _pick_number(options, v, fn)
    k = _col_info(tables, col)[0]
    q = {"table": 0, "join": None, "where": _canon_where(tables, conj, atoms), "conj": conj, "agg": {"fn": fn, "t": k, "col": col}, "group": None}
    return {"answer_index": idx, "answer_text": numstr(v), "parse": {"form": form, "query": q, "tables": _tables_canon(tables)}, "info": {}}


def _b3(db, tables, qs, options, places, join):
    if qs["agg"] not in AGG_WORD:
        raise ParseFail("aggregate_phrase", qs["agg"])
    fn = AGG_WORD[qs["agg"]]
    col = qs["col"]
    conj, atoms = _atoms(tables, parse_cond(qs["cond"]))
    if fn == "count":
        if col != "rows":
            raise ParseFail("count_of_a_column", col)
        v = db.aggregate("count", None, 1, conj, atoms)
        agg = {"fn": "count"}
    else:
        v = _agg_value(db, tables, fn, col, conj, atoms, places)
        agg = {"fn": fn, "t": _col_info(tables, col)[0], "col": col}
    idx = _pick_number(options, v, fn)
    q = {"table": 0, "join": {"left_key": tables[0].cols[join[0]], "right_key": tables[1].cols[join[1]]},
         "where": _canon_where(tables, conj, atoms), "conj": conj, "agg": agg, "group": None}
    return {"answer_index": idx, "answer_text": numstr(v), "parse": {"form": "TB-B3", "query": q, "tables": _tables_canon(tables)}, "info": {}}


def _b2(db, tables, qs, options):
    m = Q_B2_PHRASE.match(qs["rank_phrase"].strip())
    if not m:
        raise ParseFail("rank_phrase_shape", qs["rank_phrase"])
    highest = m.group("hl") == "highest"
    col = m.group("col")
    k, t, j, ty = _col_info(tables, col)
    if ty not in ("int", "dec"):
        raise ParseFail("rank_on_non_numeric_column", col)
    scale = 100 if ty == "dec" else 1
    if m.group("cond"):
        conj, atoms = _atoms(tables, parse_cond(m.group("cond")))
    else:
        conj, atoms = "and", []
    if m.group("grp"):
        fn = AGG_WORD[m.group("agg")] if m.group("agg") else None
        if fn is None or fn == "count":
            raise ParseFail("group_rank_needs_aggregate", "")
        gk, gt, gj, gty = _col_info(tables, m.group("grp"))
        res = db.groups(fn, db._col_ref(k, col), scale, db._col_ref(gk, m.group("grp")), conj, atoms)
        items = sorted(res.items(), key=lambda kv: kv[1], reverse=highest)
        if len(items) < 2 or items[0][1] == items[1][1]:
            raise Reject("tie_for_first_place", "")
        winner = items[0][0]
        agg = {"fn": fn, "t": k, "col": col}
        group = {"col": m.group("grp"), "t": gk}
    else:
        if m.group("agg"):
            raise ParseFail("aggregate_without_group", "")
        winner = db.extreme_row(db._col_ref(k, col), highest, db._col_ref(0, tables[0].cols[0]), conj, atoms)
        # entity ranking is a group-by on the entry (first) column, one row per entry; the aggregate is then unobservable in the text and
        # is written "max" in both directions (the direction is carried by `highest`)
        agg = {"fn": "max", "t": k, "col": col}
        group = {"col": tables[0].cols[0], "t": 0}
    idx = pick_unique([i for i, o in enumerate(options) if o.strip() == winner], winner)
    q = {"table": 0, "join": None, "where": _canon_where(tables, conj, atoms), "conj": conj, "agg": agg, "group": group, "highest": highest}
    return {"answer_index": idx, "answer_text": winner, "parse": {"form": "TB-B2", "query": q, "tables": _tables_canon(tables)}, "info": {}}


def _b4(db, tables, qs, options, places):
    claim = qs["claim"].strip()
    if claim.startswith('"'):
        if not claim.endswith('"') or claim.count('"') != 2:
            raise ParseFail("claim_quotes", claim)
        claim = claim[1:-1].strip()
    if claim.endswith("."):
        claim = claim[:-1].rstrip()
    truth = None
    cm = CL_VALUE.match(claim)
    if cm:
        fn = AGG_WORD[cm.group("agg")]
        col = cm.group("col")
        conj, atoms = _atoms(tables, parse_cond(cm.group("rest")))
        v = _agg_value(db, tables, fn, col, conj, atoms, places)
        truth = (v == Fraction(cm.group("val")))
        q = {"table": 0, "join": None, "where": _canon_where(tables, conj, atoms), "conj": conj,
             "agg": {"fn": fn, "t": _col_info(tables, col)[0], "col": col}, "group": None}
        ck = {"kind": "value", "value": cm.group("val")}
    else:
        cm = CL_COUNT.match(claim)
        if cm:
            conj, atoms = _atoms(tables, parse_cond(cm.group("cond")))
            v = db.aggregate("count", None, 1, conj, atoms)
            truth = (v == Fraction(cm.group("n")))
            q = {"table": 0, "join": None, "where": _canon_where(tables, conj, atoms), "conj": conj, "agg": {"fn": "count"}, "group": None}
            ck = {"kind": "count", "value": cm.group("n")}
        else:
            cm = CL_ROW.match(claim)
            if not cm:
                raise ParseFail("claim_shape", claim)
            highest = cm.group("hl") == "highest"
            col = cm.group("col")
            k, t, j, ty = _col_info(tables, col)
            if ty not in ("int", "dec"):
                raise ParseFail("rank_on_non_numeric_column", col)
            if cm.group("cond"):
                conj, atoms = _atoms(tables, parse_cond(cm.group("cond")))
            else:
                conj, atoms = "and", []
            winner = db.extreme_row(db._col_ref(k, col), highest, db._col_ref(0, tables[0].cols[0]), conj, atoms)
            truth = (winner == cm.group("name"))
            q = {"table": 0, "join": None, "where": _canon_where(tables, conj, atoms), "conj": conj,
                 "agg": {"fn": "max" if highest else "min", "t": k, "col": col}, "group": None, "highest": highest}
            ck = {"kind": "extreme", "value": cm.group("name")}
    want = "true" if truth else "false"
    idx = pick_unique([i for i, o in enumerate(options) if norm_text(o) == want], want)
    return {"answer_index": idx, "answer_text": "True" if truth else "False",
            "parse": {"form": "TB-B4", "query": q, "tables": _tables_canon(tables), "claim": ck}, "info": {}}
