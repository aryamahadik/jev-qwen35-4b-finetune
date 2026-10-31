"""T63 NEAR head: relation registry NM-T1..NM-T8, snapshot spec builder and SOLVER A (the forward label function over the spec).

Gold (G0-lite section 2.1, as amended by Opus T63-M1 and T63-B7):
  LOOKALIKE (YES) iff there is an ESTABLISHED entry Q of the same registry as the query (Q != P) with rel(P, Q) in NM-T1..NM-T7
  AND publisher(P) != publisher(Q) AND no fork_of / same-org edge links P and Q AND age(P) < age(Q) in STRICT class order
  (the same class is NOT newer; B7: the shown age CLASSES decide, no date field).
  NM-T8 is its own first-match clause: a T8-shaped query is YES iff (i) P is listed in the card's reserved_internal_namespaces,
  (ii) the query registry is not the internal registry the card reserves the name for, (iii) a bare install resolves to the query
  registry under the card's resolve_order (first registry of the order whose snapshot lists the name) or the install names the
  registry explicitly, (iv) publisher(P) is not the project's own org handle. T8 shape = P is on the card's reserved list.
  Established = age class >= A2 AND downloads class D2.
ASSUMPTION (flagged in README): "an established entry Q" for NM-T1..T7 ranges over the entries of the QUERY's registry.

`near_relations(p, q)` -> the set of NM-T1..NM-T7 ids with "p can be obtained from q by that single operation". The union is
symmetric (T1 <-> T2, T3, T4, T5, T6, T7 are their own inverses), so a pair (a, b) can be queried from either side.
"""
from . import config as C

AGE_ORDER = {a: i for i, a in enumerate(C.AGE)}
SEPS = "-_."
_ROWS = ("qwertyuiop", "asdfghjkl", "zxcvbnm")


def _kb():
    pos = {ch: (r, c) for r, row in enumerate(_ROWS) for c, ch in enumerate(row)}
    nb = {}
    for ch, (r, c) in pos.items():
        cand = [(r, c - 1), (r, c + 1), (r - 1, c), (r - 1, c + 1), (r + 1, c - 1), (r + 1, c)]
        nb[ch] = {_ROWS[rr][cc] for rr, cc in cand if 0 <= rr < 3 and 0 <= cc < len(_ROWS[rr])}
    return nb


KEYBOARD = _kb()
LOOKALIKES = (("rn", "m"), ("m", "rn"), ("l", "1"), ("1", "l"), ("o", "0"), ("0", "o"))


def strip_seps(s):
    return "".join(ch for ch in s if ch not in SEPS)


def _deletions(q):
    return {q[:i] + q[i + 1:] for i in range(len(q))}


def near_relations(p, q):
    """Set of NM-T1..NM-T7 ids with p = op(q)."""
    out = set()
    if p == q or not p or not q:
        return out
    if len(p) == len(q) - 1 and p in _deletions(q):
        out.add("NM-T1")
    if len(p) == len(q) + 1 and q in _deletions(p):
        out.add("NM-T2")
    if len(p) == len(q):
        diff = [i for i in range(len(p)) if p[i] != q[i]]
        if len(diff) == 1:
            i = diff[0]
            if q[i] in KEYBOARD and p[i] in KEYBOARD[q[i]]:
                out.add("NM-T3")
        elif len(diff) == 2 and diff[1] == diff[0] + 1:
            i = diff[0]
            if p[i] == q[i + 1] and p[i + 1] == q[i]:
                out.add("NM-T4")
    if strip_seps(p) == strip_seps(q) and "/" not in p and "/" not in q:
        out.add("NM-T5")
    for a, b in LOOKALIKES:                        # replace one occurrence of a in q by b
        start = 0
        while True:
            k = q.find(a, start)
            if k < 0:
                break
            if q[:k] + b + q[k + len(a):] == p:
                out.add("NM-T6")
            start = k + 1
    if p.count("/") + q.count("/") == 1:
        scoped, bare = (p, q) if "/" in p else (q, p)
        sc, _, nm = scoped.partition("/")
        if sc and nm == bare:
            out.add("NM-T7")
    return out


def established(entry):
    return entry["age"] in C.ESTABLISHED and entry["dl"] == "D2"


def newer(a, b):
    return AGE_ORDER[a["age"]] < AGE_ORDER[b["age"]]


def linked(p, q):
    """fork_of edge in either direction between the two entries, or the same publisher (same-org edge)."""
    return p["publisher"] == q["publisher"] or p.get("fork_of") == q["name"] or q.get("fork_of") == p["name"]


def resolves_to(card, entries, name, registry, explicit):
    """T8 (iii): explicit install names the registry; a bare install resolves to the first registry of resolve_order whose snapshot
    lists the name."""
    if explicit:
        return True
    for rid in card["resolve_order"]:
        if any(e["name"] == name and e["registry"] == rid for e in entries):
            return rid == registry
    return False


def t8_shaped(spec):
    return spec["query"]["name"] in spec["card"]["reserved"]


def t8_label(spec):
    q, card = spec["query"], spec["card"]
    p = next(e for e in spec["entries"] if e["name"] == q["name"] and e["registry"] == q["registry"])
    return bool(q["name"] in card["reserved"] and q["registry"] != card["internal_registry"]
                and resolves_to(card, spec["entries"], q["name"], q["registry"], q["explicit"])
                and p["publisher"] != card["own_org"])


def lookalike_label(spec):
    q = spec["query"]
    p = next(e for e in spec["entries"] if e["name"] == q["name"] and e["registry"] == q["registry"])
    for e in spec["entries"]:
        if e is p or e["registry"] != q["registry"] or not established(e):
            continue
        if (near_relations(p["name"], e["name"]) and p["publisher"] != e["publisher"] and not linked(p, e) and newer(p, e)):
            return True
    return False


def gold_label(spec):
    """SOLVER A for NEAR: T8 first-match clause, then the T1..T7 rule."""
    if t8_shaped(spec):
        return "YES" if t8_label(spec) else "NO"
    return "YES" if lookalike_label(spec) else "NO"


def relations_present(spec):
    """Diagnostics: ids of NM-T1..T7 relations between the queried entry and ANY other entry of its registry (K5 feature)."""
    q = spec["query"]
    out = set()
    for e in spec["entries"]:
        if e["name"] == q["name"] and e["registry"] == q["registry"]:
            continue
        if e["registry"] == q["registry"]:
            out |= near_relations(q["name"], e["name"])
    return out
