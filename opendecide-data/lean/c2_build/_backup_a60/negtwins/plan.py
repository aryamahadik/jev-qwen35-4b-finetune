"""negtwins/plan.py: base eligibility, the label-blind twin plan, caps and the build step (A42-D 7.1, 7.2, 7.3, 10).

Bases come from three blocks, all through the same engine:
  gblock    kept G-block yes/no rows (instruction = preamble + core; the card is the G-block card)
  metadata  item 8 rows. The mapper supplies a `neg_spec` {"pre", "core"} per task, so no free-text parse is needed
            (the core must still pass core.parse); the card is the mapper's two-line card
  replay    KEEP-licence replay yes/no rows with human gold: the t37b registry (select.eligible) plus any source whose
            base type passes the card certificate; the original T37b 2,000 rows count inside the 10,000
A base is eligible only when: qtype noul, gold 0/1, hard label (no vote shares), card is exactly "- yes:/- no:" and swap-
safe, the core parses (both parsers agree), the core holds no negation cue (negcount k_all = 0), and (complement twins
only) its base type passed the card certificate. A base gets at most ONE complement twin and ONE equiv twin (unit <= 3).

The plan reads gold for ONE thing: which bases enter, so the twin yes share lands in 45-55% (the T37b A1-5 precedent).
Flipping every gold leaves the plan unchanged. Patterns, frames and bases are chosen by hash order.
"""
from __future__ import annotations

import json
import math
import re
from collections import Counter, defaultdict
from pathlib import Path

from . import core as C
from . import checks as K
from . import frozen as FZ
from t37b import select as SEL  # noqa: E402

CAPS = {"gblock": 5000, "metadata": 5000, "replay": 10000}          # A42-D 7.1
REPLAY_T37B_ORIGINAL = 2000
SHARE_COMPLEMENT = 0.70           # 1,400 : 600 as T37b
MIN_IMPLICIT, MIN_ANTONYM, MAX_SYNTACTIC = 0.25, 0.30, 0.45         # shares of COMPLEMENT twins (spec 3.18)
TARGET = {"syntactic": 0.40, "implicit": 0.28, "antonym": 0.32}
CELL_CAP = 0.02                   # one (pattern, base core) wording <= 2% of the block (G11 style)
PATTERN_CAP = 0.012               # one pattern <= 1.2% of the block, so >= 84 patterns are live at 5,000 rows
TYPE_CAP = 0.10                   # one base type (core x card) <= 10% of the block
YES_BAND = (0.45, 0.55)
WRAP_ONE_SIDED = True      # yes-only cards (G-block wave 1) take complement twins through the negation-wrap card (checks.twin_card)


def base_record(row: dict, block: str, spec: dict | None = None, *, allow_card_free: bool = False):
    """Eligibility of one row -> dict or None. spec = metadata neg_spec {"pre", "core"} (else split the instruction)."""
    if row.get("qtype") != "noul" or row.get("gold") not in (0, 1):
        return None
    meta = row.get("meta") or {}
    if meta.get("teacher") or meta.get("gold_probs") or meta.get("attack_target"):
        return None
    d = SEL.parse_card(row.get("card"))
    one_sided = False
    card_free = not (row.get("card") or "").strip()
    if card_free:
        if not allow_card_free:
            return None
        d = (None, None)
    elif d is None:                                   # G-block wave 1: a yes-only card. Equiv twins only (card kept as is)
        body = K.one_sided_body(row.get("card"))
        if body is None:
            return None
        d, one_sided = (body, None), True
    elif not SEL.swap_safe(d):
        return None
    sp = (spec["pre"], spec["core"]) if spec else C.split_instruction(row["instructions"])
    if not sp:
        return None
    pre, core = sp
    q = C.parse(core)
    if q is None:
        return None
    return {"row": row, "block": block, "pre": pre, "core": core, "q": q, "defs": d,
            "type": C.sha(core + "|" + str(d[0]) + "|" + str(d[1]))[:12], "neg": C.has_negation(core),
            "one_sided": one_sided, "card_free": card_free,
            "comp_card": card_free or K.twin_card(row.get("card"), "complement") is not None}


def twin_table(cores: list, patterns: list, pairs: dict, twin_ok=None) -> dict:
    """{core: {pid: twin core}} for every pattern that applies and passes the independent checker (cached per core).
    twin_ok(core, twin core, pattern) -> bool: further program checks (polarity A/B, A43 f / A48 h) a twin must pass to be planned."""
    out = {}
    for c in sorted(set(cores)):
        d = {}
        if C.parse(c) is not None:
            for p in patterns:
                if p.relation == "complement" and C.has_negation(c):
                    continue
                t, _q = C.apply(c, p, pairs)
                if t and K.check_pair(c, t, p, pairs.get(p.pair))[0] and (twin_ok is None or twin_ok(c, t, p)):
                    d[p.pid] = t
        out[c] = d
    return out


def eligibility_report(bases: list, patterns: list, pairs: dict) -> dict:
    tab = twin_table([b["core"] for b in bases], patterns, pairs)
    pid = {p.pid: p for p in patterns}
    by_cls = Counter(b["q"].cls for b in bases)
    with_c = sum(1 for b in bases if any(pid[x].relation == "complement" for x in tab[b["core"]]))
    live = Counter(x for b in bases for x in tab[b["core"]])
    return {"bases": len(bases), "distinct_cores": len({b["core"] for b in bases}), "by_class": dict(by_cls),
            "bases_with_a_complement": with_c, "patterns_with_any_base": len(live),
            "patterns_with_ge_10_cores": sum(1 for x in live if len({b["core"] for b in bases if x in tab[b["core"]]}) >= 10)}


def _plan_once(bases: list, patterns: list, pairs: dict, *, block: str, n_target: int, certified: set | None = None,
               seed: str = "negtw-plan-v1", size: int = 0, source_cap: float | None = None, type_cap: float = TYPE_CAP,
               pooled: dict | None = None, complement_first: bool = False, tab: dict | None = None) -> tuple:
    """Label-blind plan -> (list of (base, pattern, twin core), report). certified = base types cleared for complements
    (None = all). Deterministic; shortfalls lower the block, nothing is refilled.
    pooled = {"counts": Counter(pattern id -> rows of the OTHER blocks), "total": their size}: the pattern cap is then a share of
    the POOLED twin set (this block + the others), each pattern's room being the pooled cap minus its rows elsewhere.
    complement_first: every base is offered its complement twin before its equiv twin, and the equiv pass only runs after the
    complement pass (complement supply is the scarce one and the caps are shared; the equiv twins fill what is left)."""
    cap = min(n_target, CAPS[block])
    size = size or cap
    tab = tab if tab is not None else twin_table([b["core"] for b in bases], patterns, pairs)
    pid = {p.pid: p for p in patterns}
    order = sorted(bases, key=lambda b: C.sha(seed + "|" + b["row"]["id"]))
    n_comp = round(cap * SHARE_COMPLEMENT)
    want = {"complement": n_comp, "equiv": cap - n_comp}
    kind_want = {k: round(n_comp * v) for k, v in TARGET.items()}
    used = Counter()
    cell, pat, typ, kinds, yes = Counter(), Counter(), Counter(), Counter(), [0, 0]
    out = []
    taken = {"complement": set(), "equiv": set()}
    maxcell, maxpat, maxtyp = max(1, int(CELL_CAP * size)), max(1, int(PATTERN_CAP * size)), int((type_cap if type_cap is not None else 1.0) * size)
    if pooled:
        pool_cap = max(1, int(PATTERN_CAP * (size + pooled["total"])))
        pat_room = lambda x: max(0, pool_cap - pooled["counts"].get(x, 0))      # noqa: E731
    else:
        pat_room = lambda x: maxpat                                             # noqa: E731
    src = Counter()
    maxsrc = int(source_cap * size) if source_cap else 10 ** 9      # spec 3.18: at most 10% of the block from any one source

    def try_place(b, rel):
        bid = b["row"]["id"]
        if used[rel] >= want[rel] or bid in taken[rel]:
            return False
        if rel == "complement" and (b["neg"] or not b.get("comp_card", True) or (b["one_sided"] and not WRAP_ONE_SIDED) or
                                    (certified is not None and not b["one_sided"] and not b.get("card_free")
                                     and b["type"] not in certified)):
            return False
        if src[b["row"]["source"]] >= maxsrc:
            return False
        opts = [pid[x] for x in tab[b["core"]] if pid[x].relation == rel]
        if rel == "complement":                             # the kind with the largest deficit first
            opts.sort(key=lambda p: (-(kind_want[p.kind] - kinds[p.kind]) / max(1, kind_want[p.kind]), pat[p.pid],
                                     C.sha(seed + bid + p.pid)))
        else:
            opts.sort(key=lambda p: (pat[p.pid], C.sha(seed + bid + p.pid)))
        for p in opts:
            if cell[(p.pid, b["core"])] >= maxcell or pat[p.pid] >= pat_room(p.pid) or typ[b["type"]] >= maxtyp:
                continue
            if rel == "complement" and kinds[p.kind] >= kind_want[p.kind] + 1:
                continue
            g = 1 - b["row"]["gold"] if rel == "complement" else b["row"]["gold"]
            n = yes[0] + yes[1]
            old, new = (yes[1] / n if n else 0.5), (yes[1] + g) / (n + 1)
            if n >= 200 and not (YES_BAND[0] <= new <= YES_BAND[1] or abs(new - 0.5) < abs(old - 0.5)):
                continue
            out.append((b, p, tab[b["core"]][p.pid]))
            taken[rel].add(bid)
            used[rel] += 1
            cell[(p.pid, b["core"])] += 1
            pat[p.pid] += 1
            typ[b["type"]] += 1
            src[b["row"]["source"]] += 1
            kinds[p.kind if rel == "complement" else "equiv"] += 1
            yes[g] += 1
            return True
        return False

    if complement_first:
        for rel in ("complement", "equiv"):
            for _sweep in range(3):
                before = len(out)
                for b in order:
                    try_place(b, rel)
                if len(out) == before:
                    break
    else:
        for _sweep in range(3):
            before = len(out)
            for b in order:
                for rel in sorted(want, key=lambda r: -(want[r] - used[r]) / max(1, want[r])):
                    try_place(b, rel)
            if len(out) == before:
                break
    rep = {"block": block, "cap": CAPS[block], "target": cap, "realised": len(out), "complement": used["complement"],
           "equiv": used["equiv"], "kinds": dict(kinds), "patterns_used": len(pat), "twin_yes_share":
           round(yes[1] / max(1, sum(yes)), 4), "max_cell": max(cell.values(), default=0),
           "max_type_share": round(max(typ.values(), default=0) / max(1, len(out)), 4),
           "max_source_share": round(max(src.values(), default=0) / max(1, len(out)), 4)}
    ncomp = max(1, used["complement"])
    rep["shares_of_complement"] = {"syntactic": round(kinds["syntactic"] / ncomp, 4),
                                   "implicit": round(kinds["implicit"] / ncomp, 4),
                                   "antonym": round(kinds["antonym"] / ncomp, 4)}
    return out, rep


def summarise(out: list, block: str, target: int) -> dict:
    """The plan report recomputed for a list of (base, pattern, twin core)."""
    kinds, yes = Counter(), [0, 0]
    for b, p, _t in out:
        kinds[p.kind if p.relation == "complement" else "equiv"] += 1
        yes[1 - b["row"]["gold"] if p.relation == "complement" else b["row"]["gold"]] += 1
    nc = max(1, kinds["syntactic"] + kinds["implicit"] + kinds["antonym"])
    n = max(1, len(out))
    return {"block": block, "cap": CAPS[block], "target": target, "realised": len(out),
            "complement": sum(1 for _b, p, _t in out if p.relation == "complement"),
            "equiv": sum(1 for _b, p, _t in out if p.relation == "equiv"), "kinds": dict(kinds),
            "patterns_used": len({p.pid for _b, p, _t in out}), "twin_yes_share": round(yes[1] / n, 4),
            "max_cell": max(Counter((p.pid, b["core"]) for b, p, _t in out).values(), default=0),
            "max_type_share": round(max(Counter(b["type"] for b, _p, _t in out).values(), default=0) / n, 4),
            "max_source_share": round(max(Counter(b["row"]["source"] for b, _p, _t in out).values(), default=0) / n, 4),
            "max_pattern_share": round(max(Counter(p.pid for _b, p, _t in out).values(), default=0) / n, 4),
            "shares_of_complement": {k: round(kinds[k] / nc, 4) for k in ("syntactic", "implicit", "antonym")}}


def enforce_caps(out: list, *, source_cap: float | None, type_cap: float | None = None, pattern_cap: float = PATTERN_CAP,
                 cell_cap: float = CELL_CAP, seed: str = "negtw-caps-v1", pooled: dict | None = None,
                 equiv_first: bool = False) -> tuple:
    """Caps are shares of the REALISED block: remove whole twins (hash-latest first) from the over-share source / type /
    pattern / (pattern, core) cell until every cap holds on what is left. Only removes; nothing is added or edited.
    pooled (see _plan_once): the pattern cap is the share of the pooled twin set (this block + the others).
    equiv_first: inside the over-share group the equiv twins go before any complement twin (complements are the scarce rows)."""
    out, removed = list(out), Counter()
    keys = (("source", lambda x: x[0]["row"]["source"], source_cap), ("type", lambda x: x[0]["type"], type_cap),
            ("pattern", lambda x: x[1].pid, pattern_cap), ("cell", lambda x: (x[1].pid, x[0]["core"]), cell_cap))
    for _ in range(100000):
        n = len(out)
        hit = None
        for name, kf, cap in keys:
            if cap is None or not n:
                continue
            if name == "pattern" and pooled:
                limit = max(1, int(cap * (n + pooled["total"])))
                cnt = Counter(kf(x) for x in out)
                k, v = max(cnt.items(), key=lambda kv: (kv[1] + pooled["counts"].get(kv[0], 0) - limit, kv[0]))
                if v + pooled["counts"].get(k, 0) > limit:
                    hit = (name, kf, k)
                    break
                continue
            k, v = Counter(kf(x) for x in out).most_common(1)[0]
            if v > max(1, int(cap * n)):
                hit = (name, kf, k)
                break
        if hit is None:
            break
        name, kf, k = hit
        mine = sorted((i for i, x in enumerate(out) if kf(x) == k),
                      key=lambda i: ((out[i][1].relation == "equiv") if equiv_first else 0, C.sha(seed + out[i][0]["row"]["id"] + out[i][1].pid)),
                      reverse=True)
        del out[mine[0]]
        removed[name] += 1
    return out, dict(removed)


def plan_block(bases: list, patterns: list, pairs: dict, *, block: str, n_target: int, certified: set | None = None,
               seed: str = "negtw-plan-v1", source_cap: float | None = None, type_cap: float = TYPE_CAP,
               trim: bool = False) -> tuple:
    """Caps are shares of the REALISED block (T37b rule): re-plan at the realised size until the caps hold."""
    FZ.guard_patterns(patterns)                                      # A42-D 7.4: no held-out pattern or surface in a training plan
    FZ.guard_pairs(pairs)
    size = min(n_target, CAPS[block])
    if trim:                      # one plan at the target, then caps enforced on the realised block by removal only
        out, rep = _plan_once(bases, patterns, pairs, block=block, n_target=n_target, certified=certified, seed=seed,
                              size=size, source_cap=source_cap, type_cap=type_cap)
        planned = len(out)
        out, removed = enforce_caps(out, source_cap=source_cap, type_cap=type_cap, seed=seed)
        rep = summarise(out, block, n_target) | {"planned_before_caps": planned, "removed_by_caps": removed,
                                                 "cap_basis_rows": len(out)}
        return out, rep
    for _ in range(8):
        out, rep = _plan_once(bases, patterns, pairs, block=block, n_target=n_target, certified=certified, seed=seed,
                              size=size, source_cap=source_cap, type_cap=type_cap)
        if len(out) >= size or (rep["max_type_share"] <= type_cap + 1e-9 and rep["max_source_share"] <= (source_cap or 1.0) + 1e-9
                                and rep["max_cell"] <= max(1, int(CELL_CAP * len(out)))):
            break
        size = len(out)
    rep["cap_basis_rows"] = size
    return out, rep


def share_check(out: list, *, source_cap: float | None, pooled: dict | None = None, pattern_cap: float = PATTERN_CAP,
                cell_cap: float = CELL_CAP) -> dict:
    """The caps on a finished plan, as shares of the realised block (pattern: also of the pooled twin set when given)."""
    n = max(1, len(out))
    s = summarise(out, "replay", len(out))
    cnt = Counter(p.pid for _b, p, _t in out)
    res = {"rows": len(out), "max_source_share": s["max_source_share"], "source_cap_ok": source_cap is None or s["max_source_share"] <= source_cap + 1e-9,
           "max_cell": s["max_cell"], "cell_cap_ok": s["max_cell"] <= max(1, int(cell_cap * n)),
           "max_pattern_share_block": s["max_pattern_share"]}
    if pooled:
        tot = len(out) + pooled["total"]
        mx = max(((v + pooled["counts"].get(k, 0)) for k, v in cnt.items()), default=0)
        res |= {"pooled_twin_rows": tot, "max_pattern_rows_pooled": mx, "max_pattern_share_pooled": round(mx / max(1, tot), 4),
                "pattern_cap_pooled_ok": mx <= max(1, int(pattern_cap * tot))}
    return res


def plan_fit(bases: list, patterns: list, pairs: dict, *, block: str, n_target: int, certified: set | None = None,
             seed: str = "negtw-plan-v1", source_cap: float | None = None, type_cap: float | None = None, pooled: dict | None = None,
             step: int = 250, floor: int = 250, min_complement_share: float = 0.60, twin_ok=None) -> tuple:
    """Largest block whose caps hold on the REALISED block (A42-D 7.1 / spec 3.18 rule, found by search instead of the T37b
    descent, which collapses when the supply of one relation is short). For each planning size S (n_target, n_target - step, ...
    down to floor): one label-blind plan at S (caps from S), then `enforce_caps` by removal on what was realised. Candidates must
    have a complement share >= min_complement_share (the 70:30 design ratio, short complement supply may not be filled with
    equiv twins); the largest one wins, ties to the smaller S. Only removal after the plan; nothing is added or edited.
    Returns (plan, report incl. the whole scan)."""
    FZ.guard_patterns(patterns)
    FZ.guard_pairs(pairs)
    tab = twin_table([b["core"] for b in bases], patterns, pairs, twin_ok)         # once: every planning size reads the same table
    scan, best = [], None
    S = min(n_target, CAPS[block])
    while S >= floor:
        out, _rep = _plan_once(bases, patterns, pairs, block=block, n_target=S, certified=certified, seed=seed, size=S,
                               source_cap=source_cap, type_cap=type_cap, pooled=pooled, complement_first=True, tab=tab)
        planned = len(out)
        out, removed = enforce_caps(out, source_cap=source_cap, type_cap=type_cap, seed=seed, pooled=pooled, equiv_first=True)
        rep = summarise(out, block, S)
        comp_share = rep["complement"] / max(1, rep["realised"])
        row = {"planning_size": S, "planned_before_caps": planned, "realised": rep["realised"], "complement": rep["complement"],
               "equiv": rep["equiv"], "complement_share": round(comp_share, 4), "removed_by_caps": removed,
               "max_source_share": rep["max_source_share"], "twin_yes_share": rep["twin_yes_share"]}
        scan.append(row)
        if comp_share >= min_complement_share and (best is None or rep["realised"] > best[2]["realised"]):
            best = (S, out, rep | {"planned_before_caps": planned, "removed_by_caps": removed})
        S -= step
    if best is None:
        return [], {"block": block, "realised": 0, "scan": scan, "note": "no planning size gave a block with the required complement share"}
    S, out, rep = best
    return out, rep | {"planning_size": S, "cap_basis_rows": len(out), "scan": scan, "min_complement_share": min_complement_share,
                       "caps": share_check(out, source_cap=source_cap, pooled=pooled)}


def _flow_graph(bases: list, patterns: list, tab: dict, certified: set | None, seed: str) -> dict:
    """Candidate network for plan_flow: one node per (base, relation) the base may host (same admission as _plan_once: complement
    needs a negation-free core, a swappable card and a certified base type), one cell node per (pattern, core)."""
    pid = {p.pid: p for p in patterns}
    srcs = sorted({b["row"]["source"] for b in bases})
    sidx = {s: i for i, s in enumerate(srcs)}
    brn, cells = [], {}
    order = sorted(range(len(bases)), key=lambda i: C.sha(seed + "|" + bases[i]["row"]["id"]))
    for bi in order:
        b = bases[bi]
        for rel in ("complement", "equiv"):
            if rel == "complement" and (b["neg"] or not b.get("comp_card", True) or (b["one_sided"] and not WRAP_ONE_SIDED) or
                                        (certified is not None and not b["one_sided"] and not b.get("card_free")
                                         and b["type"] not in certified)):
                continue
            ps = sorted((x for x in tab[b["core"]] if pid[x].relation == rel), key=lambda x: C.sha(seed + b["row"]["id"] + x))
            if not ps:
                continue
            for x in ps:
                cells.setdefault((x, b["core"]), len(cells))
            brn.append((bi, rel, ps))
    patlist = sorted({x for (x, _c) in cells})
    return {"srcs": srcs, "sidx": sidx, "brn": brn, "cells": cells, "patlist": patlist, "pidx": {x: i for i, x in enumerate(patlist)}}


def _flow_stage(g: dict, bases: list, rels: tuple, cap_src: list, cap_cell: dict, cap_pat: list):
    """One max-flow on the network restricted to the relations in `rels` with the given remaining capacities. Returns
    (value, [(brn index, cell key)], used per source, used per cell, used per pattern)."""
    import numpy as np
    from scipy.sparse import csr_matrix
    from scipy.sparse.csgraph import maximum_flow
    srcs, brn, cells, patlist = g["srcs"], g["brn"], g["cells"], g["patlist"]
    cell_keys = {cc: key for key, cc in cells.items()}
    S, T = 0, 1
    o_src = 2
    o_brn = o_src + len(srcs)
    o_cell = o_brn + len(brn)
    o_pat = o_cell + len(cells)
    N = o_pat + len(patlist)
    r, c, w = [], [], []
    for si, cap in enumerate(cap_src):
        r.append(S), c.append(o_src + si), w.append(cap)
    edge_of = []
    for k, (bi, rel, ps) in enumerate(brn):
        if rel not in rels:
            continue
        r.append(o_src + g["sidx"][bases[bi]["row"]["source"]]), c.append(o_brn + k), w.append(1)
        for x in ps:
            cc = cells[(x, bases[bi]["core"])]
            r.append(o_brn + k), c.append(o_cell + cc), w.append(1)
            edge_of.append((k, cc))
    for key, cc in cells.items():
        r.append(o_cell + cc), c.append(o_pat + g["pidx"][key[0]]), w.append(cap_cell[key])
    for pi, cap in enumerate(cap_pat):
        r.append(o_pat + pi), c.append(T), w.append(cap)
    A = csr_matrix((np.array(w, dtype=np.int32), (np.array(r), np.array(c))), shape=(N, N))
    A.sum_duplicates()
    res = maximum_flow(A, S, T)
    F = res.flow.tocsr()
    picks, used_src, used_cell, used_pat = [], Counter(), Counter(), Counter()
    for k, cc in edge_of:
        if F[o_brn + k, o_cell + cc] > 0:
            picks.append((k, cc))
    for k, cc in picks:
        bi = brn[k][0]
        used_src[g["sidx"][bases[bi]["row"]["source"]]] += 1
        used_cell[cell_keys[cc]] += 1
        used_pat[g["pidx"][cell_keys[cc][0]]] += 1
    return int(res.flow_value), picks, used_src, used_cell, used_pat


def _flow_at(g: dict, bases: list, n: int, source_cap: float | None, pooled: dict | None, pattern_cap: float, cell_cap: float) -> tuple:
    """Lexicographic max flow at block size n: complement twins first, then equiv twins on what the caps leave. Caps are the
    shares of an n-row block (the realised block is >= n, so they only get looser)."""
    Cs = int((source_cap or 1.0) * n)
    Cc = max(1, int(cell_cap * n))
    tot = n + (pooled["total"] if pooled else 0)
    limit = max(1, int(pattern_cap * tot))
    cap_pat = [max(0, limit - (pooled["counts"].get(x, 0) if pooled else 0)) for x in g["patlist"]]
    cap_src = [Cs] * len(g["srcs"])
    cap_cell = {key: Cc for key in g["cells"]}
    v1, picks1, us, uc, up = _flow_stage(g, bases, ("complement",), cap_src, cap_cell, cap_pat)
    cap_src2 = [cap_src[i] - us[i] for i in range(len(cap_src))]
    cap_cell2 = {key: Cc - uc[key] for key in g["cells"]}
    cap_pat2 = [cap_pat[i] - up[i] for i in range(len(cap_pat))]
    v2, picks2, *_ = _flow_stage(g, bases, ("equiv",), cap_src2, cap_cell2, cap_pat2)
    return v1 + v2, v1, picks1 + picks2


def balance_yes(out: list, band: tuple = YES_BAND, seed: str = "negtw-yes-v1") -> tuple:
    """Removal only: bring the twin yes share into the band by dropping hash-latest twins of the over-represented gold side
    (equiv twins first, so the scarce complement twins stay). Returns (plan, removed)."""
    out = list(out)
    removed = 0

    def gold(x):
        b, p, _t = x
        return 1 - b["row"]["gold"] if p.relation == "complement" else b["row"]["gold"]
    while out:
        y = sum(gold(x) for x in out)
        sh = y / len(out)
        if band[0] <= sh <= band[1]:
            break
        side = 1 if sh > band[1] else 0
        pool = sorted((i for i, x in enumerate(out) if gold(x) == side),
                      key=lambda i: (out[i][1].relation == "equiv", C.sha(seed + out[i][0]["row"]["id"] + out[i][1].pid)), reverse=True)
        del out[pool[0]]
        removed += 1
    return out, removed


def plan_flow(bases: list, patterns: list, pairs: dict, *, block: str, n_target: int, certified: set | None = None,
              seed: str = "negtw-plan-v1", source_cap: float | None = None, pooled: dict | None = None, twin_ok=None,
              step: int = 50) -> tuple:
    """The largest block whose caps hold on its own size, by max-flow (A42-D 7.1; spec 3.18 source <= 10%; (pattern, core) cell
    <= 2%; pattern <= 1.2% of the pooled twin set). A greedy plan cannot find it when one relation's supply is short (it leaves about
    40% of the feasible block unused). For n from the cap downwards the lexicographic max flow (complement twins first, then equiv)
    on the caps of an n-row block is computed; the first n whose flow reaches n is the block (all flow units). A base hosts at
    most one complement and one equiv twin. The plan reads no gold except balance_yes (removal only, band 45-55%).
    Label-blind otherwise; nothing is edited or refilled."""
    FZ.guard_patterns(patterns)
    FZ.guard_pairs(pairs)
    tab = twin_table([b["core"] for b in bases], patterns, pairs, twin_ok)
    pid = {p.pid: p for p in patterns}
    g = _flow_graph(bases, patterns, tab, certified, seed)
    scan = []
    n = min(n_target, CAPS[block])
    coarse = 5 * step
    found = None
    while n > 0:
        F, c, picks = _flow_at(g, bases, n, source_cap, pooled, PATTERN_CAP, CELL_CAP)
        scan.append({"n": n, "flow": F, "complement": c, "equiv": F - c})
        if F >= n:
            found = (n, picks)
            break
        n -= coarse
    if found is not None:                       # the feasible sizes form an interval: climb back up to its top in `step` steps
        m = found[0] + step
        while m < found[0] + coarse:
            F, c, picks = _flow_at(g, bases, m, source_cap, pooled, PATTERN_CAP, CELL_CAP)
            scan.append({"n": m, "flow": F, "complement": c, "equiv": F - c})
            if F >= m:
                found = (m, picks)
            m += step
    if found is None:
        return [], {"block": block, "realised": 0, "scan": scan, "note": "no block size is feasible under the caps"}
    n, picks = found
    cell_key = {cc: key for key, cc in g["cells"].items()}
    out = [(bases[g["brn"][k][0]], pid[cell_key[cc][0]], tab[cell_key[cc][1]][cell_key[cc][0]]) for k, cc in picks]
    planned = len(out)
    out, y_removed = balance_yes(out)
    rep = summarise(out, block, n_target) | {"planned_before_caps": planned, "removed_by_yes_band": y_removed, "planning_size": n,
                                             "cap_basis_rows": len(out), "scan": scan, "planner": "max-flow",
                                             "caps": share_check(out, source_cap=source_cap, pooled=pooled)}
    return out, rep


def trim_pooled(plans: dict, max_syntactic: float = MAX_SYNTACTIC, seed: str = "negtw-trim-v1") -> tuple:
    """T37b trim_block rule at pool level: remove syntactic COMPLEMENT twins (hash-latest first, whole twins) until their
    share of the pooled complement twins is <= 45%. Only removes. Returns ({block: plan}, {block: removed count})."""
    comp = [(blk, i) for blk, pl in plans.items() for i, (b, p, t) in enumerate(pl) if p.relation == "complement"]
    syn = sorted([(blk, i) for blk, i in comp if plans[blk][i][1].kind == "syntactic"],
                 key=lambda x: C.sha(seed + plans[x[0]][x[1]][0]["row"]["id"] + plans[x[0]][x[1]][1].pid), reverse=True)
    n_comp, n_syn = len(comp), len(syn)
    drop = set()
    while syn and (n_syn - len(drop)) / max(1, n_comp - len(drop)) > max_syntactic:
        drop.add(syn[len(drop)])
    out = {blk: [x for i, x in enumerate(pl) if (blk, i) not in drop] for blk, pl in plans.items()}
    return out, {blk: sum(1 for d in drop if d[0] == blk) for blk in plans}


def read_budget(n_pos=24, n_neg=16, n_pair_cand=95, n_patterns=520, n_heldout=43, n_card_types=120, n_twins=18000) -> dict:
    """Expected model reads (item-level judgements) and tasks (agent runs) per stage. Defaults: the draft sizes in
    tasks.draft_items and a catalogue of about 520 trained patterns."""
    chunk = 50
    st = {
        "draft (Haiku, author)": (75 + 19, 10 + 3, "75 draft items + 19 held-out slots, 8 items per task"),
        "G-LEX round x2 (Haiku)": (2 * (3 * (n_pos + n_neg) + n_pair_cand * 5), None, "3 probes per frame, up to 5 per pair"),
        "exactness, trained patterns (Haiku)": (n_patterns * 10, None, "10 pairs per pattern, 1 read"),
        "exactness, held-out patterns (Haiku)": (n_heldout * 10, None, "10 pairs per pattern"),
        "card certificates x2 (Haiku)": (2 * n_card_types, None, "2 reads per base type"),
        "audit, 3% of twins (Sonnet)": (math.ceil(0.03 * n_twins), None, "1 read per sampled twin"),
    }
    out = {}
    for k, (reads, tasks, note) in st.items():
        out[k] = {"reads": reads, "tasks": tasks if tasks is not None else math.ceil(reads / chunk), "note": note}
    out["total_haiku_item_reads"] = sum(v["reads"] for k, v in out.items() if "Sonnet" not in k)
    out["total_sonnet_item_reads"] = out["audit, 3% of twins (Sonnet)"]["reads"]
    return out


def share_problems(rep: dict) -> list:
    """Spec 3.18 shares and A42-D caps on a plan report."""
    s, probs = rep["shares_of_complement"], []
    if rep["complement"] and s["implicit"] < MIN_IMPLICIT:
        probs.append(f"implicit share {s['implicit']} < {MIN_IMPLICIT}")
    if rep["complement"] and s["antonym"] < MIN_ANTONYM:
        probs.append(f"antonym share {s['antonym']} < {MIN_ANTONYM}")
    if rep["complement"] and s["syntactic"] > MAX_SYNTACTIC:
        probs.append(f"syntactic share {s['syntactic']} > {MAX_SYNTACTIC}")
    if rep["realised"] > rep["cap"]:
        probs.append("block cap exceeded")
    if rep["realised"] and not YES_BAND[0] <= rep["twin_yes_share"] <= YES_BAND[1]:
        probs.append(f"twin yes share {rep['twin_yes_share']} outside {YES_BAND}")
    return probs


def build_rows(plan: list, *, block: str) -> tuple:
    rows, pairs = [], []
    for b, p, t in plan:
        row = K.twin_row(b["row"], b["pre"], t, p, block=block)
        rows.append(row)
        pairs.append((b["row"], row))
    return rows, pairs


def template_strings(patterns: list, pairs: dict) -> dict:
    """Every frame, cue and pair word of the trained catalogue, for the seed-first G13 method 8 check."""
    s = {p.frame for p in patterns if p.frame} | {"fail to", "lack"}
    for pr in pairs.values():
        for side in ("a", "b"):
            s |= {v for v in pr[side].values() if v}
    return {"n": len(s), "strings": sorted(s)}


def block_budget(counts: dict) -> dict:
    """Row-count table vs the A42-D 7.1 caps for the three blocks."""
    out = {}
    for blk, cap in CAPS.items():
        n = counts.get(blk, 0)
        out[blk] = {"rows": n, "cap": cap, "ok": n <= cap}
    out["total_twins"] = sum(counts.get(b, 0) for b in CAPS)
    out["new_rows_with_replay_1_5x"] = counts.get("gblock", 0) + counts.get("metadata", 0)
    return out


def pooled_report(reps: list) -> dict:
    """Spec 3.18 shares are checked on the POOLED complement twins of the three blocks (a narrow block such as the
    G-block, 23 distinct questions, cannot carry the antonym share alone)."""
    k = Counter()
    for r in reps:
        for name, n in r["kinds"].items():
            k[name] += n
    nc = max(1, k["syntactic"] + k["implicit"] + k["antonym"])
    shares = {n: round(k[n] / nc, 4) for n in ("syntactic", "implicit", "antonym")}
    probs = []
    if shares["implicit"] < MIN_IMPLICIT:
        probs.append(f"implicit {shares['implicit']} < {MIN_IMPLICIT}")
    if shares["antonym"] < MIN_ANTONYM:
        probs.append(f"antonym {shares['antonym']} < {MIN_ANTONYM}")
    if shares["syntactic"] > MAX_SYNTACTIC:
        probs.append(f"syntactic {shares['syntactic']} > {MAX_SYNTACTIC}")
    return {"complement_twins": nc, "shares": shares, "problems": probs}


def heldout_pairs(bases: list, held: list, pairs: dict, *, n_target: int = 150, per_pattern: int = 5,
                  seed: str = "negtw-heldout-pairs-v1") -> tuple:
    """The 150 complement pairs of the G-proxy and the item 10 probe (A42-D 7.4, 10.3, 12.1): held-out COMPLEMENT patterns
    only, <= 5 pairs per pattern, one pair per base, round-robin over patterns in hash order so no pattern dominates.
    bases come from the G-proxy sources (not a training source). Returns ([(base, pattern, twin core)], report)."""
    comp = [p for p in held if p.relation == "complement"]
    tab = twin_table([b["core"] for b in bases], comp, pairs)
    used, out, seen = Counter(), [], set()
    order = sorted(bases, key=lambda b: C.sha(seed + b["row"]["id"]))
    for rnd in range(per_pattern):
        for p in sorted(comp, key=lambda p: C.sha(seed + p.pid)):
            if len(out) >= n_target or used[p.pid] > rnd:
                continue
            for b in order:
                if b["row"]["id"] in seen or b["neg"] or p.pid not in tab[b["core"]]:
                    continue
                out.append((b, p, tab[b["core"]][p.pid]))
                seen.add(b["row"]["id"])
                used[p.pid] += 1
                break
    return out, {"pairs": len(out), "patterns_used": len(used), "max_per_pattern": max(used.values(), default=0),
                 "complete": len(out) >= n_target}
