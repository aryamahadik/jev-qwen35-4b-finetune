"""Generic set-level gate helpers shared by the L-P families (CPU, data only; no model). Each family's gates.py composes these with its own
probes. Bars are the G0-lite bars (fixed before any pilot); nothing here is tuned.

Every function returns {"ok": bool, ...numbers...}; a family gate list turns them into {"id", "ok", ...}.
"""
import collections
import math

from . import tokens

LADDER_TARGET = {"L1": 0.20, "L2": 0.30, "L3": 0.30, "L4": 0.20}
LADDER_TOL = 0.05


def share_in(counter_or_pairs, lo, hi, name=None):
    c = collections.Counter(counter_or_pairs) if not isinstance(counter_or_pairs, collections.Counter) else counter_or_pairs
    n = sum(c.values())
    out = {k: (v / n if n else 0.0) for k, v in c.items()}
    return {"ok": bool(n and all(lo <= s <= hi for s in out.values())), "shares": out, "n": n, "name": name}


def label_share(rows, label, lo, hi, key=lambda r: r["gold"]):
    n = len(rows)
    s = sum(1 for r in rows if key(r) == label) / n if n else 0.0
    return {"ok": bool(n and lo <= s <= hi), "share": s, "n": n}


def ladder_composition(rows, level_of=lambda r: r["meta"].get("ladder"), group_of=None, l34_floor=0.25, tol=LADDER_TOL):
    """L1 20 / L2 30 / L3 30 / L4 20 (+- 5 pp); L3-L4 >= 25% overall and per group (block / head)."""
    c = collections.Counter(level_of(r) for r in rows)
    n = sum(c.values())
    sh = {k: c.get(k, 0) / n if n else 0.0 for k in LADDER_TARGET}
    ok = bool(n) and all(abs(sh[k] - LADDER_TARGET[k]) <= tol for k in LADDER_TARGET)
    l34 = sh["L3"] + sh["L4"]
    per = {}
    if group_of is not None:
        by = collections.defaultdict(list)
        for r in rows:
            by[group_of(r)].append(r)
        for g, rs in by.items():
            cc = collections.Counter(level_of(r) for r in rs)
            per[g] = (cc.get("L3", 0) + cc.get("L4", 0)) / len(rs)
    ok = ok and l34 >= l34_floor and all(v >= l34_floor for v in per.values())
    return {"ok": ok, "shares": sh, "l34": l34, "per_group_l34": per, "n": n}


def twin_share(rows, is_hard=lambda r: r["meta"].get("ladder") in ("L3", "L4"), twin_of=lambda r: r["meta"].get("twin_of"), floor=0.50):
    """Every L3/L4 row has an easy-looking twin with the opposite label; twins cover >= 50% of L3-L4 rows."""
    hard = [r for r in rows if is_hard(r)]
    n = len(hard)
    tw = sum(1 for r in hard if twin_of(r))
    return {"ok": bool(n == 0 or tw / n >= floor), "share": (tw / n if n else 1.0), "n": n}


def matched_pair_share(rows, pair_of=lambda r: r["meta"].get("pair_id"), floor=0.30):
    """Share of rows that belong to a pair/quad (a pair id shared by >= 2 kept rows)."""
    c = collections.Counter(pair_of(r) for r in rows if pair_of(r))
    paired = sum(v for v in c.values() if v >= 2)
    n = len(rows)
    s = paired / n if n else 0.0
    return {"ok": bool(n and s >= floor), "share": s, "n": n}


def wording_variety(rows, min_wordings=50, max_share=0.02, form_of=lambda r: r.get("question_form"), wid_of=lambda r: r["meta"].get("wording_id")):
    by = collections.defaultdict(collections.Counter)
    for r in rows:
        by[form_of(r)][wid_of(r)] += 1
    out = {}
    ok = True
    for form, c in by.items():
        n = sum(c.values())
        top = max(c.values()) / n if n else 0.0
        # with W wordings the least-used-first picker keeps the top share at ceil(n/W)/n; the bar is 2% only when n >= 50 / 0.02
        bar = max(max_share, math.ceil(n / max(1, min_wordings)) / n) if n else max_share
        out[form] = {"wordings_used": len(c), "top_share": top, "bar": bar, "ok": bool(top <= bar + 1e-9)}
        ok = ok and out[form]["ok"]
    return {"ok": ok, "forms": out}


def token_report(rows):
    return tokens.token_gate([r["meta"].get("tokens") or tokens.count(r["rendered"]["text"]) for r in rows])


def split_hygiene(rows, group_of=lambda r: r["group_id"], split_of=lambda r: r["meta"].get("split")):
    """No group is in both dev and train."""
    seen = collections.defaultdict(set)
    for r in rows:
        seen[group_of(r)].add(split_of(r))
    bad = [g for g, s in seen.items() if len(s) > 1]
    return {"ok": not bad, "violations": len(bad)}


def hook_fields_complete(rows, fields=("template_id", "wording_id", "construction_id")):
    bad = sum(1 for r in rows if any(not r["meta"].get(f) for f in fields))
    return {"ok": bad == 0, "violations": bad}


def stamp_complete(rows):
    bad = sum(1 for r in rows if not r.get("stamp") or r["stamp"].get("verdict") != "clean")
    return {"ok": bad == 0, "unstamped": bad}


def no_permission_option(rows, words=("ALLOW", "ASK", "BLOCK")):
    """Fact-label families (T63, T66, T65, T62): no ALLOW / ASK / BLOCK option in any form."""
    bad = 0
    for r in rows:
        txt = " ".join(o["text"] for o in r.get("options", [])) + " " + r["rendered"].get("question", "")
        if any(w in txt.split() or w in txt for w in words):
            bad += 1
    return {"ok": bad == 0, "violations": bad}


def run_gate_list(gates, rows, **kw):
    out = []
    for gid, fn in gates:
        try:
            res = fn(rows, **kw)
        except TypeError:
            res = fn(rows)
        res = dict(res)
        res["id"] = gid
        out.append(res)
    return out
