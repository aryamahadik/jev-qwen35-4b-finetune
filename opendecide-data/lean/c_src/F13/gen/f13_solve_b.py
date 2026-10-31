"""F13 SOLVER B (G0 section 6; G2). Reads only the parser's output (f13_parse), never the generator model or solver
A. Paradigm: the parsed facts go into sqlite tables; version-in-force, scope filters and life-cycle windows are SQL
queries; conditions are evaluated row-wise; traces are completed by exhaustive critical-point enumeration (value
traces) and label-typed witness facts (part traces). Documented deviation (no z3 in the venv): critical points replace
the SMT search; every predicate is a single-attribute threshold, so the critical points cover every satisfiable class.
"""
from __future__ import annotations

import copy
import itertools
import sqlite3

TRACE = "__TRACE__"
TI_LABELS = ("Contact list", "Staff directory", "Telephone and e-mail list")
CMP = {"ge": ">=", "le": "<=", "gt": ">", "lt": "<"}


# ------------------------------------------------------------------------------------------------ database
class _DB:
    def __init__(self):
        self.cx = sqlite3.connect(":memory:")

    def execute(self, *a):
        return self.cx.execute(*a)

    def executescript(self, *a):
        return self.cx.executescript(*a)


def load(doc: dict):
    db = _DB()
    db.tabs = []
    db.executescript("""
      CREATE TABLE ver (sid TEXT, rid TEXT, vid TEXT, rev INT, scope TEXT, status TEXT, eff TEXT, end_kind TEXT,
                        end_date TEXT, outcome TEXT, ci INT);
      CREATE TABLE reg (vid TEXT, rid TEXT, eff TEXT);
      CREATE TABLE voids (target TEXT);
      CREATE TABLE exc (sid TEXT, eid TEXT, rid TEXT, scope TEXT, status TEXT, eff TEXT, end_kind TEXT, end_date TEXT,
                        ci INT);
      CREATE TABLE cases (sid TEXT, cid TEXT, scope TEXT, gdate TEXT, ai INT);
      CREATE TABLE dec (sid TEXT, scope TEXT, matter TEXT, kind TEXT, date TEXT, outcome TEXT, status TEXT, va INT);
      CREATE TABLE dvoid (scope TEXT, matter TEXT, kind TEXT, date TEXT);
      CREATE TABLE dcorr (scope TEXT, matter TEXT, kind TEXT, date TEXT, new TEXT);
      CREATE TABLE lc (sid TEXT, ft TEXT, noun TEXT, eid TEXT, scope TEXT, start TEXT, stop TEXT);
      CREATE TABLE aev (sid TEXT, scope TEXT, aid TEXT, verb TEXT, who TEXT, date TEXT);
      CREATE TABLE tab (ti INT, sid TEXT, scope TEXT, p1 TEXT, p2 TEXT, name TEXT, part INT, total INT, tmeas TEXT);
      CREATE TABLE cell (ti INT, ri INT, col TEXT, txt TEXT, num INT);
      CREATE TABLE crit (rid TEXT, eff TEXT, outcome TEXT, ci INT);
      CREATE TABLE excl (xid TEXT, scope TEXT, status TEXT, eff TEXT, end_kind TEXT, end_date TEXT);
      CREATE TABLE le (sid TEXT, scope TEXT, ft TEXT, date TEXT, time TEXT, no INT, cfg TEXT, vid TEXT, status TEXT,
                       value INT, noun TEXT, eid TEXT, target INT);
    """)
    conds = []
    attrs = []
    for s in doc["sections"]:
        for f in s["facts"]:
            ft = f["ft"]
            if ft == "rule":
                conds.append((f["conds"], f["join"]))
                db.execute("INSERT INTO ver VALUES (?,?,?,?,?,?,?,?,?,?,?)",
                           (s["sid"], f["rid"], f["vid"], f["rev"], f["scope"], f["status"], f["eff"], f["end"][0],
                            f["end"][1] if len(f["end"]) > 1 else None, f["outcome"], len(conds) - 1))
            elif ft == "effreg":
                db.execute("INSERT INTO reg VALUES (?,?,?)", (f["vid"], f["rid"], f["eff"]))
            elif ft == "void":
                db.execute("INSERT INTO voids VALUES (?)", (f["target"],))
            elif ft == "exc":
                conds.append((f["conds"], f["join"]))
                db.execute("INSERT INTO exc VALUES (?,?,?,?,?,?,?,?,?)",
                           (s["sid"], f["eid"], f["rid"], f["scope"], f["status"], f["eff"], f["end"][0],
                            f["end"][1] if len(f["end"]) > 1 else None, len(conds) - 1))
            elif ft == "dec":
                db.execute("INSERT INTO dec VALUES (?,?,?,?,?,?,?,?)", (s["sid"], s.get("scope"), f["matter"],
                           f["kind"], f["date"], f["outcome"], f["status"], f["votes"][0] if f["votes"] else None))
            elif ft == "dvoid":
                db.execute("INSERT INTO dvoid VALUES (?,?,?,?)", (s.get("scope"), f["matter"], f["kind"], f["date"]))
            elif ft == "dcorr":
                db.execute("INSERT INTO dcorr VALUES (?,?,?,?,?)", (s.get("scope"), f["matter"], f["kind"], f["date"],
                                                                    f["new"]))
            elif ft == "hold":
                db.execute("INSERT INTO lc VALUES (?,?,?,?,?,?,?)", (s["sid"], "hold", f["noun"], f["eid"], f["scope"],
                                                                     f["placed"], f["released"]))
            elif ft == "lcond":
                db.execute("INSERT INTO lc VALUES (?,?,?,?,?,?,?)", (s["sid"], "lcond", f["noun"], f["eid"],
                                                                     f["scope"], f["imposed"],
                                                                     f["end"][1] if f["end"] else None))
            elif ft == "aitem":
                for verb, who, d in f["events"]:
                    db.execute("INSERT INTO aev VALUES (?,?,?,?,?,?)", (s["sid"], s.get("scope"), f["aid"], verb, who,
                                                                        d))
            elif ft == "table":
                ti = len(db.tabs)
                db.tabs.append(f)
                per = s.get("period") or [None, None]
                db.execute("INSERT INTO tab VALUES (?,?,?,?,?,?,?,?,?)", (ti, s["sid"], s.get("scope"), per[0], per[1],
                                                                          f["name"], f["part"], f["total"],
                                                                          f["tmeas"]))
                for ri, row in enumerate(f["rows"]):
                    for col, v in zip(f["cols"], row):
                        db.execute("INSERT INTO cell VALUES (?,?,?,?,?)", (ti, ri, col, None if isinstance(v, int)
                                                                           else str(v), v if isinstance(v, int)
                                                                           else None))
            elif ft == "crit":
                conds.append((f["conds"], f["join"]))
                db.execute("INSERT INTO crit VALUES (?,?,?,?)", (f["rid"], f["eff"], f["outcome"], len(conds) - 1))
            elif ft == "excl":
                db.execute("INSERT INTO excl VALUES (?,?,?,?,?,?)", (f["xid"], f["scope"], f["status"], f["eff"],
                                                                     f["end"][0], f["end"][1] if len(f["end"]) > 1
                                                                     else None))
            elif ft.startswith("le_"):
                db.execute("INSERT INTO le VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?)",
                           (s["sid"], s.get("scope"), ft, f["date"], f["time"], f["no"], f.get("cfg"), f.get("vid"),
                            f.get("status"), f.get("value"), f.get("noun"), f.get("eid"), f.get("target")))
            elif ft == "case":
                attrs.append(f["attrs"])
                db.execute("INSERT INTO cases VALUES (?,?,?,?,?)", (s["sid"], f["cid"], f["scope"], f["gdate"],
                                                                    len(attrs) - 1))
    db.conds = conds
    db.attrs = attrs
    return db


IN_FORCE = """status = 'in force' AND {eff} IS NOT NULL AND {eff} <= :on
  AND (end_kind = 'none' OR (end_kind = 'through' AND end_date >= :on) OR (end_kind = 'repealed' AND end_date > :on))"""

V_EFF = ("COALESCE(v.eff, CASE WHEN (SELECT COUNT(*) FROM reg r WHERE r.vid = v.vid) = 1 THEN "
         "(SELECT r.eff FROM reg r WHERE r.vid = v.vid) END)")


def in_force_version(db, rid, on, unit):
    q = (f"SELECT v.vid, v.outcome, v.ci, v.scope, {V_EFF} AS e FROM ver v WHERE v.rid = :rid "
         f"AND v.vid NOT IN (SELECT target FROM voids) AND (v.scope IS NULL OR v.scope = :unit) AND "
         + IN_FORCE.format(eff=V_EFF).replace("status", "v.status").replace("end_kind", "v.end_kind")
         .replace("end_date", "v.end_date") + " ORDER BY e DESC, v.rev DESC LIMIT 1")
    return db.execute(q, {"rid": rid, "on": on, "unit": unit}).fetchone()


def holds(db, ci, attrs):
    conds, join = db.conds[ci]
    if conds is None:
        return True
    vals = []
    for a in conds:
        if a["attr"] not in attrs:
            raise KeyError(a["attr"])
        x = attrs[a["attr"]]
        vals.append({"ge": x >= a["val"], "le": x <= a["val"], "gt": x > a["val"], "lt": x < a["val"]}[a["op"]])
    return all(vals) if join == "all" else any(vals)


def qp(db, case, card):
    on, unit, attrs = case["gdate"], case["scope"], case["attrs"]
    ex = db.execute("SELECT eid, rid, ci FROM exc WHERE eid NOT IN (SELECT target FROM voids) AND (scope IS NULL OR "
                    "scope = :unit) AND " + IN_FORCE.format(eff="eff"), {"on": on, "unit": unit}).fetchall()
    act = [(e, r) for e, r, ci in ex if holds(db, ci, attrs)]
    act_ids = {e for e, _ in act}
    switched = {r for _, r in act if r in act_ids}
    off = {r for e, r in act if e not in switched}
    fired = []
    for (rid,) in db.execute("SELECT DISTINCT rid FROM ver").fetchall():
        if rid in off:
            continue
        v = in_force_version(db, rid, on, unit)
        if v and holds(db, v[2], attrs):
            fired.append(v)
    if not fired:
        return card["default"]
    if card["precedence"] == "specific":
        tier = [v for v in fired if v[3] == unit] or fired
    else:
        top = max(v[4] for v in fired)
        tier = [v for v in fired if v[4] == top]
    outs = {v[1] for v in tier}
    return outs.pop() if len(outs) == 1 else "__CONFLICT__"


def the_case(doc, db, q):
    if q.get("case_ref"):
        r = db.execute("SELECT cid, scope, gdate, ai FROM cases WHERE cid = ?", (q["case_ref"],)).fetchall()
        if len(r) != 1:
            return None
        return {"cid": r[0][0], "scope": r[0][1], "gdate": r[0][2], "attrs": db.attrs[r[0][3]]}
    return q.get("case")


LC_QK = ("qr_decision", "ag2_decision", "ag1_hold", "ag1_cond", "qr_holder", "ag1_items")


def lc_core(db, q, card):
    """SQL answers for S2 / S6 query kinds (SEM-50..53, SEM-30: an entry in an unmarked section applies to all)."""
    p = {"on": q["date"], "u": q.get("unit"), "k": card.get("vote_k") or 0}
    qk = q["qk"]
    if qk in ("qr_decision", "ag2_decision"):
        p["m"] = q["matter"]
        r = db.execute("""SELECT COALESCE((SELECT c.new FROM dcorr c WHERE c.matter = d.matter AND c.kind = d.kind
                            AND c.date = d.date AND c.scope IS d.scope), d.outcome)
                          FROM dec d WHERE d.matter = :m AND (d.scope IS NULL OR d.scope = :u)
                            AND d.status = 'in force' AND (d.va IS NULL OR d.va >= :k) AND d.date <= :on
                            AND NOT EXISTS (SELECT 1 FROM dvoid v WHERE v.matter = d.matter AND v.kind = d.kind
                                            AND v.date = d.date AND v.scope IS d.scope)
                          ORDER BY d.date DESC LIMIT 2""", p).fetchall()
        return r[0][0] if r else "__UNDET__"
    if qk in ("ag1_hold", "ag1_cond"):
        p.update(ft="hold" if qk == "ag1_hold" else "lcond", n=q["noun"], e=q["eid"])
        return db.execute("SELECT COUNT(*) FROM lc WHERE ft = :ft AND noun = :n AND eid = :e AND scope = :u AND "
                          "start <= :on AND (stop IS NULL OR stop > :on)", p).fetchone()[0]
    st = """(SELECT a2.verb FROM aev a2 WHERE a2.aid = a.aid AND a2.scope IS a.scope AND a2.date <= :on
               ORDER BY a2.date DESC LIMIT 1)"""
    hd = """(SELECT a3.who FROM aev a3 WHERE a3.aid = a.aid AND a3.scope IS a.scope AND a3.date <= :on
               AND a3.verb IN ('assigned', 'transferred') ORDER BY a3.date DESC LIMIT 1)"""
    if qk == "qr_holder":
        p["a"] = q["aid"]
        r = db.execute(f"SELECT DISTINCT {st}, {hd} FROM aev a WHERE a.aid = :a AND (a.scope IS NULL OR a.scope = :u)",
                       p).fetchall()
        if len(r) != 1 or r[0][0] in (None, "closed"):
            return "__UNDET__"
        return r[0][1]
    if qk == "ag1_items":
        p["h"] = q["holder"]
        r = db.execute(f"SELECT COUNT(*) FROM (SELECT DISTINCT a.aid, a.scope, {st} AS v, {hd} AS w FROM aev a "
                       f"WHERE a.scope = :u) WHERE v IN ('assigned', 'transferred', 'reopened') AND w = :h",
                       p).fetchone()
        return r[0]
    raise ValueError(qk)


TAB_QK = ("tq_count", "tq_argmax", "tq_cmp", "tq_crit", "tq_set", "ag3_sum", "ag3_count", "tp_outcome", "ag1_excl")
SQL_OP = {"ge": ">=", "le": "<=", "gt": ">", "lt": "<"}


def _tab_parts(db, q):
    p = {"n": q["table"], "u": q["unit"], "p1": q["period"][0], "p2": q["period"][1]}
    first = db.execute("SELECT ti, part FROM tab WHERE name = :n AND scope IS :u AND (part IS NULL OR part = 1) AND "
                       "p1 = :p1 AND p2 = :p2", p).fetchall()
    if len(first) != 1:
        return None
    if first[0][1] is None:
        return [first[0][0]]
    if db.execute("SELECT COUNT(*) FROM tab WHERE name = :n AND scope IS :u AND part = 1", p).fetchone()[0] != 1:
        return None
    return [t for (t,) in db.execute("SELECT ti FROM tab WHERE name = :n AND scope IS :u AND part IS NOT NULL "
                                     "ORDER BY part", p).fetchall()]


def tab_core(db, q, card):
    """SQL answers for S4 query kinds: table selection by (name, unit mark, stated period; continued parts), WHERE
    filters, ORDER BY with the card's tie rule, SUM of part totals, criteria on one entity row, active exclusions."""
    qk = q["qk"]
    if qk == "ag1_excl":
        return db.execute("SELECT COUNT(*) FROM excl WHERE scope = :u AND " + IN_FORCE.format(eff="eff"),
                          {"u": q["unit"], "on": q["date"]}).fetchone()[0]
    if qk == "tp_outcome":
        hits = db.execute("SELECT c.ti, c.ri FROM cell c JOIN tab t ON t.ti = c.ti WHERE c.col = 'id' AND c.txt = :e "
                          "AND t.part IS NULL AND t.p1 = :p1 AND t.p2 = :p2",
                          {"e": q["ent"], "p1": q["period"][0], "p2": q["period"][1]}).fetchall()
        if len(hits) != 1:
            return "__UNDET__"
        attrs = {c: (n if n is not None else t) for c, t, n in db.execute(
            "SELECT col, txt, num FROM cell WHERE ti = ? AND ri = ?", hits[0]).fetchall()}
        fired = []
        for rid, eff, out, ci in db.execute("SELECT rid, eff, outcome, ci FROM crit WHERE eff <= ?",
                                            (q["period"][0],)).fetchall():
            try:
                if holds(db, ci, attrs):
                    fired.append((eff, out))
            except KeyError:
                continue
        if not fired:
            return card["default"]
        if card["precedence"] == "later":
            top = max(e for e, _ in fired)
            fired = [x for x in fired if x[0] == top]
        outs = {o for _, o in fired}
        return outs.pop() if len(outs) == 1 else "__CONFLICT__"
    parts = _tab_parts(db, q)
    if not parts:
        return "__UNDET__"
    ph = ",".join(str(t) for t in parts)
    if qk == "ag3_sum":
        r = db.execute(f"SELECT COUNT(*), SUM(total), COUNT(total) FROM tab WHERE ti IN ({ph})").fetchone()
        return r[1] if r[2] == r[0] else "__UNDET__"
    pm = {"m": q["measure"], "thr": q.get("thr")}
    n_m = db.execute(f"SELECT COUNT(*) FROM cell WHERE ti IN ({ph}) AND col = :m", pm).fetchone()[0]
    if n_m == 0:
        return "__UNDET__"
    base = (f"SELECT i.txt, v.num, d.txt FROM cell v JOIN cell i ON i.ti = v.ti AND i.ri = v.ri AND i.col = 'id' "
            f"LEFT JOIN cell d ON d.ti = v.ti AND d.ri = v.ri AND d.col = 'date' WHERE v.ti IN ({ph}) AND v.col = :m")
    if qk in ("tq_count", "ag3_count"):
        return db.execute(f"SELECT COUNT(*) FROM ({base}) x WHERE x.num {SQL_OP[q['op']]} :thr", pm).fetchone()[0]
    if qk == "tq_set":
        return frozenset(e for (e,) in db.execute(f"SELECT x.txt FROM ({base}) x WHERE x.num {SQL_OP[q['op']]} :thr",
                                                  pm).fetchall())
    if qk == "tq_argmax":
        tie = card.get("tie")
        order = "x.num DESC, " + ("x.d ASC" if tie == "date" else "substr(x.e, instr(x.e, '-') + 1) ASC")  # r6 MR5
        rows = db.execute(f"SELECT x.e, x.num, x.d FROM (SELECT i.txt AS e, v.num AS num, d.txt AS d FROM cell v "
                          f"JOIN cell i ON i.ti = v.ti AND i.ri = v.ri AND i.col = 'id' LEFT JOIN cell d ON "
                          f"d.ti = v.ti AND d.ri = v.ri AND d.col = 'date' WHERE v.ti IN ({ph}) AND v.col = :m) x "
                          f"ORDER BY {order} LIMIT 2", pm).fetchall()
        if len(rows) == 2 and rows[0][1] == rows[1][1]:
            if tie is None or (tie == "date" and rows[0][2] == rows[1][2]):
                return "__UNDET__"
        return rows[0][0]
    if qk == "tq_cmp":
        v = dict(db.execute(f"SELECT x.txt, x.num FROM ({base}) x WHERE x.txt IN (:a, :b)",
                            {**pm, "a": q["ent"], "b": q["ent2"]}).fetchall())
        if q["ent"] not in v or q["ent2"] not in v:
            return "__UNDET__"
        return q["ent"] if v[q["ent"]] > v[q["ent2"]] else "__NOT__"
    if qk == "tq_crit":  # repair r6
        hit = db.execute(f"SELECT x.num FROM ({base}) x WHERE x.txt = :a", {**pm, "a": q["ent"]}).fetchall()
        if not hit or any(n is None for (n,) in hit):
            return "__UNDET__"
        okf = {"ge": lambda a, b: a >= b, "le": lambda a, b: a <= b, "gt": lambda a, b: a > b, "lt": lambda a, b: a < b}
        return q["ent"] if okf[q["op"]](hit[0][0], q["thr"]) else "__NOT__"
    raise ValueError(qk)


def core(doc, q, card):
    db = load(doc)
    qk = q["qk"]
    if qk in LC_QK:
        return lc_core(db, q, card)
    if qk in TAB_QK:
        return tab_core(db, q, card)
    if qk in LG_QK:
        return log_core(db, q, card)
    if qk == "qp_outcome":
        c = the_case(doc, db, q)
        return "__UNDET__" if c is None else qp(db, c, card)
    if qk in ("qr_version", "ag2_version"):
        v = in_force_version(db, q["rid"], q["date"], q["unit"])
        return v[0] if v else "__UNDET__"
    if qk == "ag1_exc":
        r = db.execute("SELECT COUNT(*) FROM exc WHERE scope = :unit AND eid NOT IN (SELECT target FROM voids) AND "
                       + IN_FORCE.format(eff="eff"), {"on": q["date"], "unit": q["unit"]}).fetchone()
        return r[0]
    if qk == "qp_inverted":
        res = []
        for c in q["cases"]:
            v = in_force_version(db, q["rid"], c["gdate"], c["scope"])
            res.append(bool(v) and holds(db, v[2], c["attrs"]))
        return tuple(res)
    raise ValueError(qk)


# ------------------------------------------------------------------------------------------------ completions
def _pts(vals):
    s = {0}
    for v in vals:
        s.update(x for x in (v - 1, v, v + 1) if x >= 0)
    s.add(max(vals, default=0) + 100)
    return sorted(s)


def _witness(trace, doc, q, card):
    """Label-typed completions of a part trace: [] (empty) plus witness fact sets of the label's one type and scope."""
    lab, sl = trace["label"], trace["scope_label"]
    if lab in TI_LABELS:
        return [[]]
    kind = card["scope_kind"]
    unit = sl[len(kind) + 1:] if sl.startswith(kind + " ") else sl
    on = q.get("date") or (the_case_static(doc, q) or {}).get("gdate") or "2000-01-01"
    outs = []
    if lab.startswith("Versions of rule "):
        rid = lab.split(" ")[-1]
        for o in card["outcomes"]:
            outs.append([{"ft": "rule", "rid": rid, "vid": f"{rid}.99", "rev": 99, "scope": unit, "status": "in force",
                          "eff": on, "end": ["none"], "conds": None, "join": "all", "outcome": o, "form": "amend",
                          "amends": None}])
    elif lab.startswith("Exceptions to rule "):
        rid = lab.split(" ")[-1]
        outs.append([{"ft": "exc", "eid": "EX-0", "rid": rid, "conds": None, "join": "all", "scope": unit,
                      "status": "in force", "eff": "1900-01-01", "end": ["none"]}])
    elif lab == "Exceptions":
        rids = sorted({f["rid"] for s in doc["sections"] for f in s["facts"] if f["ft"] == "rule"})
        outs.append([{"ft": "exc", "eid": f"EX-{i}", "rid": r, "conds": None, "join": "all", "scope": unit,
                      "status": "in force", "eff": "1900-01-01", "end": ["none"]} for i, r in enumerate(rids)])
    elif lab == "Log entries":
        return [[]] + _log_witness(unit, q, card)
    elif lab in LC_LABELS:
        return [[]] + _lc_witness(lab, sl, unit, doc, q, card, on)
    elif lab.startswith("Table ") or lab.startswith("Part "):
        return [[]] + _tab_witness(lab, unit, doc, q, card)
    else:
        raise ValueError(f"part label {lab!r}")
    return [[]] + outs


LC_LABELS = ("Decision notices", "Motions", "Holds", "Conditions", "Action items")


def _cell_pts(doc, q, col):
    """Critical points of a traced cell (2.4): every stated value of its column and every constant a predicate on
    it compares with, each with its neighbours, plus 0 and one value above all."""
    readers = {q.get("measure")} | {a["attr"] for s in doc["sections"] for f in s["facts"] if f["ft"] == "crit"
                                    for a in f["conds"]}
    if col not in readers:
        return [0]  # no predicate reads the cell: one point covers its whole domain
    vals = [v for s in doc["sections"] for f in s["facts"] if f["ft"] == "table" and col in f["cols"]
            for row in f["rows"] for v in [row[f["cols"].index(col)]] if isinstance(v, int)]
    consts = ([q["thr"]] if q.get("thr") is not None and q.get("measure") == col else []) + [
        a["val"] for s in doc["sections"] for f in s["facts"] if f["ft"] == "crit" for a in f["conds"]
        if a["attr"] == col]
    pts = {0, max(vals + consts + [0]) + 100}
    for v in vals + consts:
        pts.update(x for x in (v - 1, v, v + 1) if x >= 0)
    return sorted(pts)


def _tab_witness(lab, unit, doc, q, card):
    """'Table <T>' / 'Part <k> of table <T>' parts: [] plus one table of that caption for the label's unit and the
    question's period whose rows put the queried measure at 0 and at a high value."""
    import re as _re
    m = _re.fullmatch(r"(?:Part (\d+) of table|Table) ([A-Z])", lab)
    part = int(m.group(1)) if m.group(1) else None
    name = m.group(2)
    cols = ["id", q.get("measure") or "x"]
    per = q.get("period") or [None, None]
    out = []
    for v in (0, 10 ** 6):
        f = {"ft": "table", "name": name, "part": part, "cols": cols, "rows": [[q.get("ent") or "W-0000", v]],
             "total": v if part else None, "tmeas": cols[1] if part else None}
        out.append({"_scope": unit, "_period": per if part in (None, 1) else None, "facts": [f]})
    return out


def _lc_witness(lab, sl, unit, doc, q, card, on):
    """Typed completions of an S2 / S6 part (G0 2.4): facts of the label's one type for its scope, dated on the
    question's date; each is placed in the trace section, whose mark is the scope label's unit (S6 committees)."""
    out = []
    if lab in ("Decision notices", "Motions"):
        matter = sl if lab == "Decision notices" else q.get("matter") or "x"
        for o in card["outcomes"]:
            out.append({"_scope": None if lab == "Decision notices" else unit,
                        "facts": [{"ft": "dec", "matter": matter, "kind": "revision", "date": on, "outcome": o,
                                   "status": "in force", "votes": None}]})
    elif lab in ("Holds", "Conditions"):
        ft = "hold" if lab == "Holds" else "lcond"
        f = {"ft": ft, "noun": q.get("noun") or "x", "eid": q.get("eid") or "x", "scope": unit}
        f.update({"hid": "HD-W", "placed": "1900-01-01", "released": None} if ft == "hold" else
                 {"cnd": "CN-W", "imposed": "1900-01-01", "end": None})
        out.append({"_scope": None, "facts": [f]})
    else:
        people = sorted({p for s in doc["sections"] for f in s["facts"] if f["ft"] == "aitem"
                         for _, p, _ in f["events"] if p} | ({q["holder"]} if q.get("holder") else set()))
        if q.get("holder"):
            out.append({"_scope": unit, "facts": [{"ft": "aitem", "aid": "AC-W", "events": [
                ["assigned", q["holder"], "1900-01-01"]]}]})
        if q.get("aid"):
            for p in people + ["W"]:
                out.append({"_scope": unit, "facts": [{"ft": "aitem", "aid": q["aid"], "events": [
                    ["assigned", p, "1900-01-01"]]}]})
    return out


def the_case_static(doc, q):
    if q.get("case_ref"):
        for s in doc["sections"]:
            for f in s["facts"]:
                if f["ft"] == "case" and f["cid"] == q["case_ref"]:
                    return f
        return None
    return q.get("case")


def answers(doc, q, card) -> set:
    out = set()
    for d2 in completions(doc, q, card):
        try:
            out.add(core(d2, q, card))
        except KeyError:
            out.add("__CONFLICT__")
    return out


def tab_argmax_top(doc, q, card):
    """tq_argmax: records left at the top after the card's tie rule; None when the selection has no answer (G2 fix r1,
    SEM-04 / SEM-22)."""
    db = load(doc)
    parts = _tab_parts(db, q)
    if not parts:
        return None
    ph = ",".join(str(t) for t in parts)
    rows = db.execute(f"SELECT i.txt, v.num, d.txt FROM cell v JOIN cell i ON i.ti = v.ti AND i.ri = v.ri AND "
                      f"i.col = 'id' LEFT JOIN cell d ON d.ti = v.ti AND d.ri = v.ri AND d.col = 'date' "
                      f"WHERE v.ti IN ({ph}) AND v.col = :m", {"m": q["measure"]}).fetchall()
    if not rows:
        return None
    best = max(r[1] for r in rows)
    top = [r for r in rows if r[1] == best]
    tie = card.get("tie")
    if len(top) > 1 and tie is not None:
        # repair r5b (SEM-22): 'the lower <record number>' compares the number after the register prefix
        key = (lambda r: r[2]) if tie == "date" else (lambda r: str(r[0]).split("-", 1)[-1])
        k0 = min(key(r) for r in top)
        top = [r for r in top if key(r) == k0]
    return frozenset(r[0] for r in top)


def claim_truths(doc, q, card) -> set:
    """Per-completion inner-claim truth on tq_argmax rows (G2 fix r1): answer == claim; an unsplittable tie gives False
    when the claimed record is not among the tied top records, else None."""
    cv = q["claim"]["value"]
    out = set()
    for d2 in completions(doc, q, card):
        try:
            a = core(d2, q, card)
        except KeyError:
            a = "__CONFLICT__"
        if a not in ("__CONFLICT__", "__UNDET__"):
            out.add(a == cv)
        else:
            top = tab_argmax_top(d2, q, card)
            out.add(False if top is not None and cv not in top else None)
    return out


def completions(doc, q, card):
    slots = []
    preds = {}
    for s in doc["sections"]:
        for f in s["facts"]:
            if f["ft"] in ("rule", "exc") and f["conds"]:
                for a in f["conds"]:
                    preds.setdefault(a["attr"], []).append(a["val"])
    for si, s in enumerate(doc["sections"]):
        for fi, f in enumerate(s["facts"]):
            if f["ft"] == "case":
                for k, v in f["attrs"].items():
                    if v == TRACE:
                        slots.append(("attr", si, fi, k, _pts(preds.get(k, []))))
        if s.get("trace"):
            slots.append(("part", si, None, None, _witness(s["trace"], doc, q, card)))
        for fi, f in enumerate(s["facts"]):
            if f["ft"] == "table":
                for ri, row in enumerate(f["rows"]):
                    for ci, v in enumerate(row):
                        if v == TRACE:
                            slots.append(("cell", si, fi, (ri, ci), _cell_pts(doc, q, f["cols"][ci])))
    for combo in itertools.product(*[sl[4] for sl in slots]) if slots else [()]:
        d2 = copy.deepcopy(doc) if slots else doc
        for sl, val in zip(slots, combo):
            if sl[0] == "attr":
                d2["sections"][sl[1]]["facts"][sl[2]]["attrs"][sl[3]] = val
            elif sl[0] == "cell":
                d2["sections"][sl[1]]["facts"][sl[2]]["rows"][sl[3][0]][sl[3][1]] = val
            elif isinstance(val, dict):
                d2["sections"][sl[1]]["facts"] = val["facts"]
                d2["sections"][sl[1]]["scope"] = val["_scope"]
                if val.get("_period"):
                    d2["sections"][sl[1]]["period"] = val["_period"]
            else:
                d2["sections"][sl[1]]["facts"] = val
        yield d2


# ------------------------------------------------------------------------------------------------ option level
def answer(doc, q, card, shown=None):
    A = answers(doc, q, card)
    det = len(A) == 1 and not ({"__CONFLICT__", "__UNDET__"} & A)
    v = next(iter(A)) if det else None
    form = q["form"]
    abst = "NEI" if card["world"] == "open" else "NONE"
    if form == "inverted":
        n = len(q["cases"])
        per = [{a[i] for a in A if isinstance(a, tuple)} for i in range(n)]
        if any(not isinstance(a, tuple) for a in A):
            return ("bad",)
        yes = [i for i, p in enumerate(per) if p == {True}]
        if det:
            if len(yes) == 1:
                return ("val", yes[0])
            return ("abstain",) if (not yes and abst == "NONE") else ("bad",)
        if len(yes) == 1:
            return ("val", yes[0])
        return ("abstain",) if not yes and abst == "NEI" else ("bad",)
    if form == "choice":
        if not det:
            return ("abstain",) if abst == "NEI" else ("bad",)
        if v in shown:
            return ("val", v)
        return ("abstain",) if abst == "NONE" else ("bad",)
    truth = None if not det else (v == q["claim"]["value"])
    if not det and A and not ({"__CONFLICT__", "__UNDET__"} & A):
        # G2 fix (SEM-04, F13R2-13): claim truth over the completions; one truth value in every completion of an
        # undetermined answer is unproven (unusable row) except "establish" on a claim false in all of them
        ts = {a == q["claim"]["value"] for a in A}
        if len(ts) == 1 and not (form == "establish" and not q["inner_neg"] and ts == {False}):
            return ("bad",)
    if not det and A and ({"__CONFLICT__", "__UNDET__"} & A) and q["qk"] == "tq_argmax":
        # G2 fix r1 (SEM-04, SEM-22): an unsplittable tie among other records leaves the answer open, not the claim;
        # one truth value in every completion -> same rule as above
        ts = claim_truths(doc, q, card)
        if None not in ts and len(ts) == 1 and not (form == "establish" and not q["inner_neg"] and ts == {False}):
            return ("bad",)
    if form == "yn":
        if truth is None:
            return ("bad",)
        return ("yes",) if (truth if q["neg"] % 2 == 0 else not truth) else ("no",)
    if form == "establish":
        t = truth if not q["inner_neg"] or truth is None else (not truth)
        est = t is True
        return ("yes",) if (est if q["neg"] % 2 == 0 else not est) else ("no",)
    if form == "settle":
        return ("claim", truth)
    raise ValueError(form)


def gold_of(a, q):
    if a[0] == "claim":
        st = a[1] is not None
        return ("yes",) if (st if q["neg"] % 2 == 0 else not st) else ("no",)
    return a


# ------------------------------------------------------------------------------------------------ roles
def _without(doc, sids):
    d2 = dict(doc)
    d2["sections"] = [s for s in doc["sections"] if s["sid"] not in sids]
    return d2


def decisive(doc, q, card, shown):
    base = answer(doc, q, card, shown)
    D = []
    for s in doc["sections"]:
        if q.get("case_ref") and any(f["ft"] == "case" and f["cid"] == q["case_ref"] for f in s["facts"]):
            D.append(s["sid"])
            continue
        if not s.get("trace") and all(f["ft"] == "inert" for f in s["facts"]):
            continue
        a = answer(_without(doc, {s["sid"]}), q, card, shown)
        if a != base or a[0] == "bad":
            D.append(s["sid"])
    return D


def sufficient(doc, q, card, shown, D):
    keep = set(D)
    return answer(_without(doc, {s["sid"] for s in doc["sections"] if s["sid"] not in keep}), q, card, shown) == \
        answer(doc, q, card, shown)


def _q_unit(doc, q):
    c = the_case_static(doc, q)
    return c["scope"] if c else q.get("unit")


def near_misses(doc, q, card, shown, D):
    """Sections outside D that one activation operator turns into a different, shown answer: V (a version or
    exception of the section put in force on the question's date, or its void removed), R (the question's / case's
    scope unit set to the section's other unit), I (the question pointed at the section's look-alike record)."""
    if q["qk"] in LC_QK:
        return lc_near_misses(doc, q, card, shown, D)
    if q["qk"] in TAB_QK:
        return tab_near_misses(doc, q, card, shown, D)
    if q["qk"] in LG_QK:
        return log_near_misses(doc, q, card, shown, D)
    base = answer(doc, q, card, shown)
    unit = _q_unit(doc, q)
    on = q.get("date") or (the_case_static(doc, q) or {}).get("gdate")
    out = []
    for si, s in enumerate(doc["sections"]):
        if s["sid"] in D or s.get("trace") or all(f["ft"] == "inert" for f in s["facts"]):
            continue
        cands = []
        voided = {f["target"] for x in doc["sections"] for f in x["facts"] if f["ft"] == "void"}
        for fi, f in enumerate(s["facts"]):
            if f["ft"] in ("rule", "exc") and (f.get("vid") or f.get("eid")) in voided:
                tgt = f.get("vid") or f.get("eid")
                d2 = copy.deepcopy(doc)
                for x in d2["sections"]:
                    x["facts"] = [g for g in x["facts"] if not (g["ft"] == "void" and g["target"] == tgt)]
                cands.append((d2, q))
            if f["ft"] in ("rule", "exc"):
                if f["status"] != "in force" or (f.get("eff") and on and f["eff"] > on):
                    d2 = copy.deepcopy(doc)
                    g = d2["sections"][si]["facts"][fi]
                    g["status"] = "in force"
                    if g.get("eff") and on and g["eff"] > on:
                        g["eff"] = on
                    cands.append((d2, q))
                if f.get("scope") and f["scope"] != unit:
                    q2 = copy.deepcopy(q)
                    if q2.get("case_ref") or q2.get("case"):
                        d2 = copy.deepcopy(doc)
                        c = the_case_static(d2, q2)
                        c["scope"] = f["scope"]
                        cands.append((d2, q2))
                    else:
                        q2["unit"] = f["scope"]
                        cands.append((doc, q2))
            if f["ft"] == "case" and q.get("case_ref") and f["cid"] != q["case_ref"]:
                q2 = dict(q, case_ref=f["cid"])
                cands.append((doc, q2))
        for d2, q2 in cands:
            a = answer(d2, q2, card, shown)
            if a != base and a[0] != "bad" and answer(_without(d2, {s["sid"]}), q2, card, shown) != a:
                out.append(s["sid"])
                break
    return out


def _none_act(q, card):
    """r7: on closed-card choice rows an activation whose new answer is unshown gives "None of the listed answers", a
    different shown option (G0 2.3 MR4, F13R4-SC2)."""
    return q.get("form") == "choice" and card.get("world") == "closed"


def _dl1(a, b):
    """Look-alike test (SEM-31): same length, one substitution or one adjacent transposition."""
    if len(a) != len(b) or a == b:
        return False
    d = [i for i in range(len(a)) if a[i] != b[i]]
    return len(d) == 1 or (len(d) == 2 and d[1] == d[0] + 1 and a[d[0]] == b[d[1]] and a[d[1]] == b[d[0]])


def lc_near_misses(doc, q, card, shown, D):
    """S2 / S6 activation operators (F13R3-09): V (a voided entry's void removed; an entry dated after the question
    date moved to it; a proposal put in force), R (the question's unit set to the section's mark or its item marks),
    I (the question's ID set to a look-alike ID the section names)."""
    base = answer(doc, q, card, shown)
    on = q["date"]
    out = []
    voids = [(x.get("scope"), f["matter"], f["kind"], f["date"]) for x in doc["sections"] for f in x["facts"]
             if f["ft"] == "dvoid"]
    for si, s in enumerate(doc["sections"]):
        if s["sid"] in D or s.get("trace") or all(f["ft"] == "inert" for f in s["facts"]):
            continue
        cands = []
        for fi, f in enumerate(s["facts"]):
            ft = f["ft"]
            if ft == "dec":
                key = (s.get("scope"), f["matter"], f["kind"], f["date"])
                if key in voids:
                    d2 = copy.deepcopy(doc)
                    for x in d2["sections"]:
                        x["facts"] = [g for g in x["facts"] if not (g["ft"] == "dvoid" and (
                            x.get("scope"), g["matter"], g["kind"], g["date"]) == key)]
                    cands.append((d2, q))
                if f["date"] and f["date"] > on:
                    d2 = copy.deepcopy(doc)
                    d2["sections"][si]["facts"][fi]["date"] = on
                    if d2["sections"][si].get("mdate"):
                        d2["sections"][si]["mdate"] = on
                    cands.append((d2, q))
                if f["status"] == "proposed":
                    d2 = copy.deepcopy(doc)
                    d2["sections"][si]["facts"][fi]["status"] = "in force"
                    cands.append((d2, q))
                if q.get("matter") and _dl1(f["matter"], q["matter"]):
                    cands.append((doc, dict(q, matter=f["matter"])))
            if ft in ("hold", "lcond"):
                if f["scope"] != q.get("unit"):
                    cands.append((doc, dict(q, unit=f["scope"])))
                if q.get("eid") and _dl1(f["eid"], q["eid"]):
                    cands.append((doc, dict(q, eid=f["eid"])))
            if ft == "aitem" and q.get("aid") and _dl1(f["aid"], q["aid"]):
                cands.append((doc, dict(q, aid=f["aid"])))
            if ft in ("dec", "aitem") and s.get("scope") and s["scope"] != q.get("unit"):
                cands.append((doc, dict(q, unit=s["scope"])))
        for d2, q2 in cands:
            a = answer(d2, q2, card, shown)
            if a != base and a[0] != "bad" and (a[0] != "abstain" or _none_act(q2, card)) and \
                    answer(_without(d2, {s["sid"]}), q2, card, shown) != a:
                out.append(s["sid"])
                break
    return out


def tab_near_misses(doc, q, card, shown, D):
    """S4 operators (2.3): NM-V prior-period table (question period := the table's period) or an exclusion put in
    force; NM-R (question unit := the table's / exclusion's unit); NM-I (question entity := a look-alike row ID)."""
    base = answer(doc, q, card, shown)
    out = []
    for s in doc["sections"]:
        if s["sid"] in D or s.get("trace") or all(f["ft"] == "inert" for f in s["facts"]):
            continue
        cands = []
        for fi, f in enumerate(s["facts"]):
            if f["ft"] == "table" and q.get("period"):
                if s.get("period") and s["period"] != q["period"] and (q.get("table") is None or (
                        f["name"] == q["table"] and s.get("scope") == q.get("unit"))):
                    cands.append((doc, dict(q, period=s["period"])))
                if q.get("table") and f["name"] == q["table"] and s.get("scope") != q.get("unit"):
                    cands.append((doc, dict(q, unit=s.get("scope"))))
                if q.get("ent"):
                    for row in f["rows"]:
                        if _dl1(row[0], q["ent"]):
                            cands.append((doc, dict(q, ent=row[0])))
            if f["ft"] == "excl" and q["qk"] == "ag1_excl":
                if f["status"] != "in force" or f["eff"] > q["date"]:
                    d2 = copy.deepcopy(doc)
                    g = d2["sections"][[x["sid"] for x in doc["sections"]].index(s["sid"])]["facts"][fi]
                    g["status"] = "in force"
                    g["eff"] = min(g["eff"], q["date"])
                    cands.append((d2, q))
                if f["scope"] != q["unit"]:
                    cands.append((doc, dict(q, unit=f["scope"])))
        for d2, q2 in cands:
            a = answer(d2, q2, card, shown)
            if a != base and a[0] != "bad" and (a[0] != "abstain" or _none_act(q2, card)) and \
                    answer(_without(d2, {s["sid"]}), q2, card, shown) != a:
                out.append(s["sid"])
                break
    return out


def solve(parsed: dict, q: dict, card: dict, shown) -> dict:
    a = answer(parsed, q, card, shown)
    g = gold_of(a, q)
    if q["form"] == "choice" and card["world"] == "closed" and a == ("abstain",):
        A = answers(parsed, q, card)
        if len(A) == 1:
            shown = list(shown) + [next(iter(A))]  # answerable base (F13R1-23)
    D = decisive(parsed, q, card, shown)
    return {"answer": a, "gold": g, "D": D, "sufficient": sufficient(parsed, q, card, shown, D),
            "NM": near_misses(parsed, q, card, shown, D)}


def _unused(parsed, q, card, shown):
    a = answer(parsed, q, card, shown)
    D = decisive(parsed, q, card, shown)
    return {"answer": a, "gold": gold_of(a, q), "D": D, "sufficient": sufficient(parsed, q, card, shown, D),
            "NM": near_misses(parsed, q, card, shown, D)}


# ------------------------------------------------------------------------------------------------ S3 logs
LG_QK = ("lg_version", "ag2_config", "lg_status", "lg_count", "ag3_lcount")
_AFTER = "({x}.date < {y}.date OR ({x}.date = {y}.date AND ({x}.time < {y}.time OR ({x}.time = {y}.time AND " \
         "{x}.no < {y}.no))))"


def log_core(db, q, card):
    """SQL replay of a log (SEM-19, 29, 35, 49, 27): rows of the unit's segments (and unmarked ones), VOID targets
    removed, timestamp date on or before the question's date, latest by (date, time, entry number)."""
    p = {"on": q["date"], "u": q["unit"]}
    U = "(scope IS NULL OR scope = :u)"
    VD = f"(SELECT target FROM le WHERE ft = 'le_void' AND {U})"
    qk = q["qk"]
    if qk in ("lg_version", "ag2_config"):
        p["c"] = q["cfg"]
        sql = f"""WITH ver AS (SELECT * FROM le WHERE ft = 'le_ver' AND cfg = :c AND {U} AND no NOT IN {VD}),
          ev AS (SELECT date, time, no, vid FROM ver WHERE status = 'in force'
            UNION ALL SELECT a.date, a.time, a.no, a.vid FROM le a JOIN ver x ON x.vid = a.vid
              WHERE a.ft = 'le_app' AND (a.scope IS NULL OR a.scope = :u) AND x.status = 'proposed'
                AND a.no NOT IN {VD} AND {_AFTER.format(x="x", y="a")}
            UNION ALL SELECT b.date, b.time, b.no, b.vid FROM le b JOIN ver x ON x.vid = b.vid
              WHERE b.ft = 'le_rb' AND b.cfg = :c AND (b.scope IS NULL OR b.scope = :u) AND x.status = 'in force'
                AND b.no NOT IN {VD} AND {_AFTER.format(x="x", y="b")})
          SELECT ev.vid, (SELECT value FROM ver WHERE ver.vid = ev.vid LIMIT 1) FROM ev WHERE ev.date <= :on
          ORDER BY ev.date DESC, ev.time DESC, ev.no DESC LIMIT 1"""
        r = db.execute(sql, p).fetchone()
        if not r:
            return "__UNDET__"
        return r[0] if qk == "lg_version" else r[1]
    if qk == "lg_status":
        p.update(n=q["noun"], e=q["eid"])
        r = db.execute(f"SELECT status FROM le WHERE ft = 'le_stat' AND noun = :n AND eid = :e AND {U} AND "
                       f"date <= :on AND no NOT IN {VD} ORDER BY date DESC, time DESC, no DESC LIMIT 1", p).fetchone()
        return r[0] if r else "__UNDET__"
    if qk in ("lg_count", "ag3_lcount"):
        p.update(n=q["noun"], s=q["filt"])
        return db.execute(f"SELECT COUNT(*) FROM le WHERE ft = 'le_stat' AND noun = :n AND status = :s AND {U} AND "
                          f"date <= :on AND no NOT IN {VD}", p).fetchone()[0]
    raise ValueError(qk)


def _log_witness(unit, q, card):
    """'Log entries' parts: entries of the question's kind for the label's unit, on the question's date."""
    on = q["date"]
    base = {"date": on, "time": "00:00", "actor": "W"}
    if q["qk"] in ("lg_version", "ag2_config"):
        return [{"_scope": unit, "facts": [{"ft": "le_ver", **base, "no": i, "cfg": q["cfg"], "vid": f"W-0.{i + 1}",
                                            "status": "in force", "value": v}]}
                for i, v in enumerate((0, 10 ** 6))]
    if q["qk"] == "lg_status":
        return [{"_scope": unit, "facts": [{"ft": "le_stat", **base, "no": i, "noun": q["noun"], "eid": q["eid"],
                                            "status": o}]} for i, o in enumerate(card["outcomes"])]
    return [{"_scope": unit, "facts": [{"ft": "le_stat", **base, "no": 0, "noun": q["noun"], "eid": "W-0000",
                                        "status": q["filt"]}]}]


def log_near_misses(doc, q, card, shown, D):
    """S3 operators (2.3): V (an entry dated after the question's date moved to it; a draft / proposed version marked
    in force; the VOID entry naming an entry removed; a later rollback that undoes an in-force version removed),
    R (the question's unit set to the segment's mark), I (the question's record ID set to a look-alike ID)."""
    base = answer(doc, q, card, shown)
    on = q["date"]
    out = []
    LE = ("le_ver", "le_app", "le_rb", "le_void", "le_stat", "le_noop")
    voids = [(x.get("scope"), f["target"]) for x in doc["sections"] for f in x["facts"] if f["ft"] == "le_void"]
    rbs = [(x.get("scope"), f) for x in doc["sections"] for f in x["facts"] if f["ft"] == "le_rb"]
    key = lambda f: (f["date"], f["time"], f["no"])  # noqa: E731

    def drop(pred):
        d2 = copy.deepcopy(doc)
        for x in d2["sections"]:
            x["facts"] = [g for g in x["facts"] if not pred(x, g)]
        return d2
    for si, s in enumerate(doc["sections"]):
        if s["sid"] in D or s.get("trace") or all(f["ft"] == "inert" for f in s["facts"]):
            continue
        cands = []
        sc = s.get("scope")
        for fi, f in enumerate(s["facts"]):
            ft = f["ft"]
            if ft not in ("le_ver", "le_stat"):
                continue
            if (sc, f["no"]) in voids or (None, f["no"]) in voids:
                no = f["no"]
                cands.append((drop(lambda x, g: g["ft"] == "le_void" and g["target"] == no and
                                   x.get("scope") in (None, sc)), q))
            if f["date"] > on:
                d2 = copy.deepcopy(doc)
                d2["sections"][si]["facts"][fi]["date"] = on
                cands.append((d2, q))
            if ft == "le_ver" and f["status"] in ("proposed", "draft"):
                d2 = copy.deepcopy(doc)
                d2["sections"][si]["facts"][fi]["status"] = "in force"
                cands.append((d2, q))
            if ft == "le_ver" and f["status"] == "in force":
                for rsc, rb in rbs:
                    if rb["cfg"] == f["cfg"] and rsc in (None, sc) and key(rb) > key(f) and rb["date"] <= on:
                        rno = rb["no"]
                        cands.append((drop(lambda x, g: g["ft"] == "le_rb" and g["no"] == rno), q))
            if ft == "le_stat" and q.get("eid") and _dl1(f["eid"], q["eid"]):
                cands.append((doc, dict(q, eid=f["eid"])))
        if sc and sc != q.get("unit") and any(f["ft"] in LE for f in s["facts"]):
            cands.append((doc, dict(q, unit=sc)))
        for d2, q2 in cands:
            a = answer(d2, q2, card, shown)
            if a != base and a[0] != "bad" and (a[0] != "abstain" or _none_act(q2, card)) and \
                    answer(_without(d2, {s["sid"]}), q2, card, shown) != a:
                out.append(s["sid"])
                break
    return out
