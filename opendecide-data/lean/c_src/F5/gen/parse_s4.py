"""S4 G3 parser (records tables in JSON / YAML / CSV / markdown / HTML / key-value; keys mapped back from snake and
camel case), solver B (sqlite on the parsed table, the LF compiled to SQL by its own compiler, COALESCE(flag, 0) for
blank yes/no cells on closed cards, the SQL re-run once per SEM-04 test value of each unrecorded cell) and the S4
question forms."""
from __future__ import annotations

import itertools
import json
import re
import sqlite3

import yaml

from . import parse as PZ
from .texts import ATTACK_RE

ATT = re.compile(ATTACK_RE)
ID = r"[A-Z]{1,4}-[A-Z0-9]+(?:-[A-Z0-9]+)?"


def _unkey(k):
    k = str(k)
    if "_" in k:
        return k.replace("_", " ").lower()
    return re.sub(r"(?<=[a-z0-9])([A-Z])", r" \1", k).lower()


def _records_from_obj(obj):
    if isinstance(obj, list) and obj and all(isinstance(x, dict) for x in obj):
        return obj
    if isinstance(obj, dict):
        for v in obj.values():
            r = _records_from_obj(v)
            if r:
                return r
    if isinstance(obj, list):
        for v in obj:
            r = _records_from_obj(v)
            if r:
                return r
    return None


def table(state):
    """(header, rows) of the one records table in the state."""
    body = PZ._strip_fence(state)
    for cand in (body, body.split("\n", 2)[-1]):
        for loader in (json.loads, yaml.safe_load):
            try:
                obj = loader(cand.strip())
            except Exception:
                continue
            recs = _records_from_obj(obj)
            if recs:
                hdr = [_unkey(k) for k in recs[0].keys()]
                rows = [["" if v is None else str(v) if not isinstance(v, bool) else ("yes" if v else "no")
                         for v in r.values()] for r in recs]
                nulls = [[v is None for v in r.values()] for r in recs]
                return hdr, rows, nulls
    lines, rows = PZ.flatten(state)
    if rows and len(rows) >= 2 and len({len(r) for r in rows}) == 1 and re.fullmatch(ID, rows[1][0] or ""):
        return [h.lower() for h in rows[0]], rows[1:], None
    cr = PZ.csv_rows(state)
    if cr and re.fullmatch(ID, cr[1][0] if len(cr) > 1 else ""):
        return [h.lower() for h in cr[0]], cr[1:], None
    raw = [ln.rstrip() for ln in PZ._strip_fence(state).split("\n")]
    # text tables: pipe-separated lines, an '=' rule (aligned), or 2+ space columns (fixed width)
    for i, ln in enumerate(raw):
        if re.fullmatch(r"=+(?:  =+)+", ln.strip()) and i > 0:
            spans = [(m.start(), m.end()) for m in re.finditer(r"=+", ln)]
            off = len(ln) - len(ln.lstrip())
            cut = lambda t: [t[a:(spans[k + 1][0] if k + 1 < len(spans) else None)].strip()  # noqa: E731
                             for k, (a, _) in enumerate(spans)]
            hdr = cut(raw[i - 1])
            body = []
            for t in raw[i + 1:]:
                if not t.strip():
                    break
                body.append(cut(t))
            if body and re.fullmatch(ID, body[0][0]):
                return [h.lower() for h in hdr], body, None
    for splitter in (lambda t: [c.strip() for c in re.split(r"\s*\|\s*", t.strip())] if " | " in t or t.rstrip()
                     .endswith(" |") else [], lambda t: re.split(r"\s{2,}", t.strip())):
        groups, cur = [], []
        for t in raw:
            cells = splitter(t) if t.strip() else []
            if len(cells) >= 3 and (not cur or len(cells) == len(cur[0])):
                cur.append(cells)
            else:
                if cur:
                    groups.append(cur)
                cur = [cells] if len(cells) >= 3 else []
        if cur:
            groups.append(cur)
        for g in groups:
            if len(g) >= 3 and re.fullmatch(ID, g[1][0]):
                return [h.lower() for h in g[0]], g[1:], None
    # key-value groups
    groups, cur = [], []
    for ln in PZ._strip_fence(state).split("\n"):
        s = ln.strip()
        if not s:
            if cur:
                groups.append(cur)
                cur = []
            continue
        if s.startswith(("#", "[")) or s.isupper():
            continue
        m = re.match(r"^(.+?)\s*(?:::|=|:|\.{3,})\s*(.*)$", s)
        if m:
            cur.append((_unkey(m.group(1).strip()), m.group(2).strip()))
    if cur:
        groups.append(cur)
    groups = [g for g in groups if len(g) >= 3]
    if groups:
        hdr = [k for k, _ in groups[0]]
        return hdr, [[v for _, v in g] for g in groups], None
    raise ValueError("no table")


def parse(rs, consts):
    r = next((x for x in rs if x["role"] != "attack"), rs[0])
    hdr, rows, nulls = table(r["state"])
    vs = consts["value_sets"]
    cat_name = next(h for h in hdr if h in vs)
    recs = []
    qty_name = unit = None
    flags = []
    FLAGV = ("yes", "no", "", "not recorded")
    roles = {}
    for j, h in enumerate(hdr):
        col = [row[j] for row in rows]
        isn = [bool(nulls and nulls[i][j]) for i in range(len(rows))]
        if j == 0:
            roles[j] = "id"
        elif h == cat_name:
            roles[j] = "cat"
        elif any(re.fullmatch(r"\d+ .+", v) for v in col):
            roles[j] = "qty"
            qty_name = h
        elif all(v in FLAGV or n for v, n in zip(col, isn)):
            roles[j] = "flag"
            flags.append(h)
        else:
            raise ValueError(f"column {h!r}")
    for i, row in enumerate(rows):
        rec = {"flags": {}, "blank": {}}
        for j, (h, v) in enumerate(zip(hdr, row)):
            isnull = bool(nulls and nulls[i][j])
            role = roles[j]
            if role == "id":
                if not re.fullmatch(ID, v):
                    raise ValueError(f"id cell {v!r}")
                rec["id"] = v
            elif role == "cat":
                rec["cat"] = "NR" if (v == "not recorded" or isnull) else v
            elif role == "flag":
                rec["flags"][h] = "NR" if (v == "not recorded" or isnull) else (v == "yes")
                rec["blank"][h] = v == "" and not isnull
            else:
                if v == "not recorded" or isnull:
                    rec["qty"] = "NR"
                    continue
                m = re.fullmatch(r"(\d+) (.+)", v)
                if not m:
                    raise ValueError(f"cell {v!r}")
                unit = m.group(2)
                rec["qty"] = int(m.group(1))
        recs.append(rec)
    for x in rs:
        if x["role"] == "attack":
            h2, r2, n2 = table(x["state"])
            if r2 != rows:
                raise ValueError("attack twin table differs")
            if not ATT.search(x["state"]):
                raise ValueError("attack twin has no attack span")
    decoys = []
    for m in re.finditer(rf"Note: (.+?) ({ID}) is not only ([a-z]+) but also ([a-z]+)\.", r["state"]):
        rec = next((x for x in recs if x["id"] == m.group(2)), None)
        if rec is None or rec["flags"].get(m.group(3)) is not True or rec["flags"].get(m.group(4)) is not True:
            raise ValueError("decoy note contradicts the table")
        decoys.append([m.group(2), m.group(3), m.group(4)])
    return {"world": consts["world"], "noun": hdr[0], "cat": cat_name, "values": vs[cat_name], "qty": qty_name,
            "unit": unit, "flags": flags, "recs": recs, "q_graded": int(consts["q"]) if consts.get("q") else None,
            "decoys": decoys}


def canon_gen(M):
    return sorted(json.dumps({"id": r["id"], "cat": r["cat"], "qty": r["qty"],
                              "flags": {w: v for w, v in r["flags"].items()}}, sort_keys=True) for r in M["recs"]) + \
        [json.dumps(M.get("decoy_text"))]


def canon_parsed(S):
    return sorted(json.dumps({"id": r["id"], "cat": r["cat"], "qty": r["qty"], "flags": r["flags"]}, sort_keys=True)
                  for r in S["recs"]) + [json.dumps(S["decoys"][0] if S["decoys"] else None)]


# solver B: sqlite --------------------------------------------------------------------------------------------------

def _sql_group(S, group, exc):
    conds = []
    args = []
    for f in group[1]:
        if f[0] == "cat":
            conds.append("cat = ?")
            args.append(f[2])
        elif f[0] == "num":
            conds.append(f"qty {f[2]} ?")
            args.append(f[3])
    if exc:
        conds.append("id <> ?")
        args.append(exc)
    return " AND ".join(conds) or "1", args


def _sql_pred(S, pred):
    if pred[0] == "flag":
        i = S["flags"].index(pred[1])
        return f"COALESCE(f{i}, 0) = 1", []
    return f"qty {pred[2]} ?", [pred[3]]


def _run(con, S, lf):
    op = lf[0]
    if op == "not":
        return not _run(con, S, lf[1])
    if op == "and":
        return all(_run(con, S, x) for x in lf[1:])
    _, Q, q, group, pred, exc = lf
    g, ga = _sql_group(S, group, exc)
    p, pa = _sql_pred(S, pred)
    n_all = con.execute(f"SELECT COUNT(*) FROM t WHERE {g}", ga).fetchone()[0]
    n = con.execute(f"SELECT COUNT(*) FROM t WHERE {g} AND {p}", ga + pa).fetchone()[0]
    if n_all == 0:
        raise ValueError("empty group")
    return {"every": n == n_all, "some": n >= 1, "atleast": n >= (q or 0), "atmost": n <= (q or 0),
            "lt": n < (q or 0), "gt": n > (q or 0), "morehalf": 2 * n > n_all}[Q]


def solve_b(S, lfs):
    ths, named = set(), set()

    def walk(x):
        if isinstance(x, list) and x:
            if x[0] == "q":
                for f in x[3][1]:
                    if f[0] == "num":
                        ths.add(f[3])
                    if f[0] == "cat":
                        named.add(f[2])
                if x[4][0] == "num":
                    ths.add(x[4][3])
            for y in x[1:]:
                walk(y)
    for lf in lfs:
        walk(lf)
    slots = []
    for r in S["recs"]:
        if r["cat"] == "NR":
            slots.append((r, "cat", sorted(set(S["values"]) | named | {x["cat"] for x in S["recs"] if x["cat"] != "NR"})
                          + ["Other value"]))
        if r["qty"] == "NR":
            base = ths | {x["qty"] for x in S["recs"] if x["qty"] != "NR"}
            slots.append((r, "qty", sorted({v + d for v in base for d in (-1, 0, 1) if v + d >= 0})))
        for w, v in r["flags"].items():
            if v == "NR":
                slots.append((r, "flag:" + w, [0, 1]))
    results = None
    for combo in itertools.product(*[s[2] for s in slots]) if slots else [()]:
        con = sqlite3.connect(":memory:")
        cols = ", ".join(f"f{i} INTEGER" for i in range(len(S["flags"])))
        con.execute(f"CREATE TABLE t (id TEXT, cat TEXT, qty INTEGER{', ' + cols if cols else ''})")
        sub = {(id(s[0]), s[1]): v for s, v in zip(slots, combo)}
        for r in S["recs"]:
            cat = sub.get((id(r), "cat"), r["cat"])
            qty = sub.get((id(r), "qty"), r["qty"])
            fl = []
            for w in S["flags"]:
                v = r["flags"].get(w)
                v = sub.get((id(r), "flag:" + w), v)
                fl.append(None if (v is False and r["blank"].get(w)) else int(bool(v)))
            con.execute(f"INSERT INTO t VALUES ({', '.join(['?'] * (3 + len(fl)))})", [r["id"], cat, qty] + fl)
        out = [_run(con, S, lf) for lf in lfs]
        con.close()
        if results is None:
            results = out
        elif results != out:
            raise ValueError("unrecorded cell is decisive")
    return results


def triggers(S):
    keys = {"SEM-01", "SEM-02", "SEM-17", "SEM-12", "SEM-14"}
    if S.get("decoys"):
        keys.add("SEM-28")
    if any(r["cat"] == "NR" or r["qty"] == "NR" or "NR" in r["flags"].values() or any(r["blank"].values())
           for r in S["recs"]):
        keys.add("SEM-04")
    return keys


def lf_triggers(lf):
    keys = set()
    if isinstance(lf, list) and lf:
        if lf[0] == "q":
            Q = lf[1]
            keys |= {"every": {"SEM-22"}, "some": {"SEM-22"}, "atleast": {"SEM-08", "SEM-12"},
                     "atmost": {"SEM-08", "SEM-12"}, "lt": {"SEM-08", "SEM-12"}, "gt": {"SEM-08", "SEM-12"},
                     "morehalf": {"SEM-09"}}[Q]
            if any(f[0] == "num" for f in lf[3][1]):
                keys |= {"SEM-08", "SEM-12", "SEM-14"}
        for x in lf[1:]:
            keys |= lf_triggers(x)
    return keys


# question forms ------------------------------------------------------------------------------------------------------

HEADS = [("no fewer than (\\d+) of the", "atleast", "C9"), ("no more than (\\d+) of the", "atmost", "C9"),
         ("at least (\\d+) of the", "atleast", None), ("at most (\\d+) of the", "atmost", None),
         ("fewer than (\\d+) of the", "lt", None), ("more than half of the", "morehalf", None),
         ("more than (\\d+) of the", "gt", None), ("none of the", "none", "C8"), ("hardly any", "hardly", "C14"),
         ("scarcely any", "hardly", "C14"), ("few", "hardly", "C14")]
FILT = r"with (.+?)"


def _group(noun, fd, ctx):
    filters = []
    for part in fd.split(" and "):
        m = re.fullmatch(r"a (.+?) of (at least|more than|at most|less than) (\d+) (.+)", part)
        if m:
            filters.append(["num", m.group(1), {"at least": ">=", "more than": ">", "at most": "<=",
                                                 "less than": "<"}[m.group(2)], int(m.group(3))])
            continue
        for cname, vals in ctx["value_sets"].items():
            if part.startswith(cname + " ") and part[len(cname) + 1:] in vals:
                filters.append(["cat", cname, part[len(cname) + 1:]])
                break
        else:
            raise PZ.QParseError(f"filter {part!r}")
    return [noun, filters]


def _tail(rest):
    """'<filters>[ other than <noun> <ID>] is|are <w>' -> (fd, exc, w)."""
    m = re.fullmatch(rf"with (.+?)(?: other than .+? ({ID}))? (?:is|are) ([a-z-]+)", rest)
    if not m:
        m = re.fullmatch(rf"with (.+?)(?: other than .+? ({ID}))? ([a-z-]+)", rest)
    if not m:
        raise PZ.QParseError(f"S4 tail {rest!r}")
    return m.group(1), m.group(2), m.group(3)


def decl(c, st, ctx):
    for pat, Q, fam in HEADS:
        m = re.fullmatch(rf"{pat} (.+?) (with .+)", c)
        if m:
            q = int(m.group(1)) if "(\\d+)" in pat else None
            rest = m.group(m.lastindex)
            fd, exc, w = _tail(rest)
            g = _group(ctx.get("noun"), fd, ctx)
            if fam:
                st.add(fam)
            if exc:
                st.add("C11")
            pred = ["flag", w]
            if Q == "none":
                return ["not", ["q", "some", None, g, pred, exc]]
            if Q == "hardly":
                return ["q", "lt", ctx["q_graded"], g, pred, exc]
            return ["q", Q, q, g, pred, exc]
    m = re.fullmatch(r"(not all|all) (.+?) (with .+)", c)
    if m:
        q, plural, rest = m.groups()
        fd, exc, w = _tail(rest)
        g = _group(ctx.get("noun"), fd, ctx)
        if q == "not all":
            st.add("C8")
            return ["not", ["q", "every", None, g, ["flag", w], exc]]
        return ["q", "every", None, g, ["flag", w], exc]
    m = re.fullmatch(r"(not every|every|some|no) (.+?) (with .+)", c)
    if m:
        q, noun, rest = m.groups()
        fd, exc, w = _tail(rest)
        g = _group(noun, fd, ctx)
        if exc:
            st.add("C11")
        pred = ["flag", w]
        if q == "not every":
            st.add("C8")
            return ["not", ["q", "every", None, g, pred, exc]]
        if q == "no":
            st.add("C8")
            return ["not", ["q", "some", None, g, pred, exc]]
        return ["q", q, None, g, pred, exc]
    return None


def matrix(body, st, ctx):
    m = re.fullmatch(r"Is (every|any) (.+?) (with .+)", body)
    if m:
        q, noun, rest = m.groups()
        fd, exc, w = _tail(rest)
        if exc:
            st.add("C11")
        return ["q", "every" if q == "every" else "some", None, _group(noun, fd, ctx), ["flag", w], exc]
    m = re.fullmatch(r"Are (.+)", body)
    if m:
        r = decl(m.group(1), st, ctx)
        if r is not None:
            return r
    return None


def decl_parsers():
    return [decl], [matrix]
