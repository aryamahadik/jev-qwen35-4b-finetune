"""Query AST helpers (G0 1.2): normal form (G3 equality), columns read (T4), depth (1.2), subtype (6), and the ONE
structure_hash canonicalizer (1.1) that both the generator side and the parsed side call.

Predicate nodes (dicts, key "k"):
  cmp {col, op, lit, unit?}        between {col, lo, hi, unit?}       in {col, vals}       win {col, lo, hi, li, hi_i, form}
  contains {col, s}                term {name}                        quant {q: any|every|no, cond}   (S4 list, T14)
  lift {a}                         (S6 request condition, T41: EXISTS a line of the request meeting a)
  line {level?, lvl_op?, comp?}    (S6 line atom)
  and {args}  or {args}  not {arg}
Operator nodes (key "op"): see f9solve_a.OPS. Literals are canonical: numbers as decimal strings, dates as day
ordinals, date-times as epoch seconds, categories / ids as raw strings.
"""
from __future__ import annotations

import copy
import hashlib
import json
from fractions import Fraction

from f9fmt import to_frac

UNK = None


# ------------------------------------------------------------------------------------------------ normal form
def _canon_lit(v):
    if isinstance(v, Fraction):
        return ("n", str(v.numerator) + "/" + str(v.denominator))
    if isinstance(v, bool):
        return ("b", v)
    if isinstance(v, int):
        return ("i", v)
    if isinstance(v, str):
        try:
            f = to_frac(v)
            return ("n", f"{f.numerator}/{f.denominator}")
        except Exception:
            return ("s", v.strip().casefold())
    if isinstance(v, (list, tuple)):
        return tuple(_canon_lit(x) for x in v)
    return ("o", repr(v))


def norm_pred(p):
    """1.2 AST normal form: comparator phrases already mapped to ops; NOT pushed through AND / OR by De Morgan,
    double NOT removed, quantified nodes / lifts are atoms; AND / OR flattened; operands sorted."""
    if p is None:
        return None
    k = p["k"]
    if k == "not":
        a = p["arg"]
        if a["k"] == "not":
            return norm_pred(a["arg"])
        if a["k"] == "and":
            return norm_pred({"k": "or", "args": [{"k": "not", "arg": x} for x in a["args"]]})
        if a["k"] == "or":
            return norm_pred({"k": "and", "args": [{"k": "not", "arg": x} for x in a["args"]]})
        return {"k": "not", "arg": norm_pred(a)}
    if k in ("and", "or"):
        out = []
        for x in p["args"]:
            nx = norm_pred(x)
            if nx["k"] == k:
                out.extend(nx["args"])
            else:
                out.append(nx)
        out.sort(key=lambda x: json.dumps(x, sort_keys=True, default=str))
        return {"k": k, "args": out}
    q = {}
    for key, v in p.items():
        if key.startswith("_") or v is None:
            continue
        if key in ("cond", "a", "fe"):
            q[key] = norm_pred(v)
        elif key == "vals":
            q[key] = sorted(_canon_lit(x) for x in v)
        elif key in ("lit", "lo", "hi", "s"):
            q[key] = _canon_lit(v)
        else:
            q[key] = v
    return q


def norm_q(q):
    out = {}
    for key, v in q.items():
        if key.startswith("_") or v is None:
            continue
        if isinstance(v, dict) and "k" in v:
            out[key] = norm_pred(v)
        elif isinstance(v, dict) and "op" in v:
            out[key] = norm_q(v)
        elif key in ("lit", "id", "key", "val"):
            out[key] = _canon_lit(v)
        elif isinstance(v, list):
            out[key] = [norm_pred(x) if isinstance(x, dict) and "k" in x else _canon_lit(x) for x in v]
        else:
            out[key] = v
    return out


def q_equal(a, b) -> bool:
    return json.dumps(norm_q(a), sort_keys=True, default=str) == json.dumps(norm_q(b), sort_keys=True, default=str)


# ------------------------------------------------------------------------------------------------ walkers
def atoms(p):
    if p is None:
        return []
    k = p["k"]
    if k in ("and", "or"):
        return [a for x in p["args"] for a in atoms(x)]
    if k == "not":
        return atoms(p["arg"])
    return [p]


def pred_cols(p, terms=None):
    """Columns a predicate reads (T4: a term's columns are its general columns, every override's columns and the
    override key column, F9-R3-04)."""
    out = []
    for a in atoms(p):
        if a["k"] in ("cmp", "between", "in", "win", "contains"):
            out.append(a["col"])
        elif a["k"] == "term" and terms is not None:
            out.extend(term_cols(terms[a["name"]], terms))
        elif a["k"] == "quant":
            out.append(a["list"])
        elif a["k"] == "has":
            out.extend(pred_cols(a["fe"], terms))
        elif a["k"] == "lift":
            out.extend(pred_cols(a["a"], terms))
    return list(dict.fromkeys(out))


def term_cols(t, terms=None):
    cols = []
    for key in ("A", "B", "C"):
        if t.get(key):
            cols += pred_cols(t[key])
    for x in t.get("list") or []:
        cols += pred_cols(x)
    for o in t.get("overrides") or []:
        cols.append(o["col"])
        cols += pred_cols(o["cond"])
    return list(dict.fromkeys(cols))


def n_atoms(p, terms=None):
    n = 0
    for a in atoms(p):
        if a["k"] == "term" and terms:
            t = terms[a["name"]]
            n += len(atoms(t.get("A"))) + len(atoms(t.get("B"))) + len(atoms(t.get("C"))) + \
                sum(len(atoms(x)) for x in t.get("list") or [])
        elif a["k"] == "quant":
            n += len(atoms(a["cond"]))
        elif a["k"] == "lift":
            n += len(atoms(a["a"]))
        elif a["k"] == "win":
            n += 1  # a window counts once, as a time window
        else:
            n += 1
    return n


SUBTYPE = {"count": "f9_count", "cdist": "f9_count", "count_lines": "f9_count", "g_count": "f9_count",
           "sum": "f9_sum", "ent_sum": "f9_sum", "mean": "f9_mean", "min": "f9_extreme", "max": "f9_extreme",
           "argmax": "f9_extreme", "argmin": "f9_extreme", "g_argmax": "f9_extreme", "comp_argmax": "f9_extreme",
           "lookup": "f9_lookup", "lookup_p": "f9_lookup", "presence": "f9_lookup", "ent_any": "f9_lookup",
           "req_any": "f9_lookup", "quant_lookup": "f9_lookup", "ent_attr": "f9_lookup", "exists": "f9_exists",
           "forall": "f9_exists", "exists_lines": "f9_exists", "compare": "f9_compare", "select": "f9_select",
           "cpick": "f9_select", "first": "f9_time", "last": "f9_time", "cell": "f9_lookup",
           "row_total": "f9_sum", "row_top": "f9_extreme", "col_count": "f9_count"}


def base_op(q):
    while q["op"] in ("thr", "not"):
        q = q["inner"]
    return q


def subtype(q):
    return SUBTYPE[base_op(q)["op"]]


def depth(q, terms=None, tie_decides=False):
    b = base_op(q)
    d = 0
    for key in ("f", "a", "b", "fe", "fd"):
        if isinstance(b.get(key), dict):
            d += n_atoms(b[key], terms)
    if b["op"] in ("g_count", "g_argmax", "ent_any", "ent_sum"):
        d += 1  # join
    w = 2 if b["op"] == "compare" else 1
    return d + w + (1 if tie_decides else 0)


# ------------------------------------------------------------------------------------------------ canonicalizer
TYPE_RANK = {"id": 0, "fk": 1, "cat": 2, "num": 3, "date": 4, "dt": 5, "bool": 6, "text": 7, "lvl": 8, "comp": 9,
             "req": 10, "list": 11}


def _h(x) -> str:
    return hashlib.sha256(json.dumps(x, sort_keys=True, default=str).encode()).hexdigest()


def _val(v):
    if v is None:
        return ["UNK"]
    if isinstance(v, Fraction):
        return ["n", f"{v.numerator}/{v.denominator}"]
    if isinstance(v, bool):
        return ["b", v]
    if isinstance(v, int):
        return ["i", v]
    if isinstance(v, list):
        return ["L", [[_val(x) for x in r] for r in v]]
    return ["s", str(v)]


def structure_hash(tables, sem_stated: dict, q, extra=None) -> str:
    """tables: [{"role", "cols": [{name, type, dp?, unit?, group?}], "rows": [[v...]]}] in any row / column order.
    Column names are dropped (c0..cn by signature order), records sorted by ID number, IDs and categories tokenised.
    Returns sha256 hex. Both sides call this on their own reading of the row."""
    canon_tables = []
    id_tok, cat_tok = {}, {}
    rename = {}
    for t in sorted(tables, key=lambda t: t["role"]):
        cols = t["cols"]
        sigs = []
        for j, c in enumerate(cols):
            vals = [r[j] for r in t["rows"]]
            if c["type"] in ("id", "comp", "req", "fk"):
                prof = sorted(_h(_val(v)) for v in vals)
                prof = sorted({p: prof.count(p) for p in prof}.values())
            elif c["type"] in ("cat", "lvl", "bool"):
                cnt = {}
                for v in vals:
                    cnt[str(v)] = cnt.get(str(v), 0) + 1
                prof = sorted(cnt.values())
            elif c["type"] == "text":
                prof = sorted(_h(str(v).strip().casefold()) for v in vals)
            else:
                prof = sorted((_val(v) for v in vals), key=lambda x: json.dumps(x))
            sig = [c["type"], c.get("dp"), c.get("unit"), c.get("group", "top"), prof]
            raw = sorted(json.dumps(_val(v)) for v in vals)
            sigs.append((TYPE_RANK.get(c["type"], 99), _h(sig), _h(raw), j))
        order = [s[3] for s in sorted(sigs)]
        names = {cols[j]["name"]: f"{t['role']}.c{i}" for i, j in enumerate(order)}
        rename.update(names)
        idj = next((j for j in order if cols[j]["type"] == "id"), None)
        rows = [[r[j] for j in order] for r in t["rows"]]
        if idj is not None:
            pos = order.index(idj)

            def rk(r):
                v = r[pos]
                import re
                m = re.match(r"^(.*?)(\d+)$", str(v))
                return (m.group(1), int(m.group(2))) if m else (str(v), -1)
            rows.sort(key=lambda r: (rk(r), json.dumps([_val(x) for x in r])))
        else:
            rows.sort(key=lambda r: json.dumps([_val(x) for x in r]))
        ocols = [cols[j] for j in order]
        for c, j in zip(ocols, range(len(ocols))):
            if c["type"] in ("id", "comp", "req", "fk"):
                for r in rows:
                    v = r[j]
                    if v is not None and v != "":
                        id_tok.setdefault(("id", str(v)), None)
        canon_tables.append({"role": t["role"], "cols": [[c["type"], c.get("dp"), c.get("unit"), c.get("group", "top")]
                                                         for c in ocols], "rows": rows, "ocols": ocols})
    # ID tokens in sorted ID order (one per distinct id value, every id kind in one series per kind)
    import re

    def idsort(s):
        m = re.match(r"^(.*?)(\d+)$", s)
        return (m.group(1), int(m.group(2))) if m else (s, -1)
    ids = sorted({k[1] for k in id_tok}, key=idsort)
    idmap = {v: f"i{n}" for n, v in enumerate(ids)}
    out_tables = []
    for t in canon_tables:
        rows = []
        for r in t["rows"]:
            rr = []
            for c, v in zip(t["ocols"], r):
                if v is None:
                    rr.append(["UNK"])
                elif c["type"] in ("id", "comp", "req", "fk"):
                    rr.append(["I", idmap.get(str(v), str(v))] if v != "" else ["I", ""])
                elif c["type"] in ("cat", "lvl"):
                    key = (c["name"], str(v))
                    if key not in cat_tok:
                        cat_tok[key] = f"k{sum(1 for x in cat_tok if x[0] == c['name'])}"
                    rr.append(["K", cat_tok[key]])
                else:
                    rr.append(_val(v))
            rows.append(rr)
        out_tables.append({"role": t["role"], "cols": t["cols"], "rows": rows})

    def tok_q(x):
        if isinstance(x, dict):
            y = {}
            for k, v in x.items():
                if k in ("col", "list") and isinstance(v, str):
                    y[k] = rename.get(v, v)
                else:
                    y[k] = tok_q(v)
            return y
        if isinstance(x, list):
            return [tok_q(v) for v in x]
        if isinstance(x, str) and x in idmap:
            return idmap[x]
        return x
    payload = {"tables": out_tables, "sem": {k: sem_stated[k] for k in sorted(sem_stated)},
               "q": tok_q(norm_q(q)), "extra": extra}
    return _h(payload)


def deep_copy(x):
    return copy.deepcopy(x)
