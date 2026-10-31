"""a49c.py: PREREG A49 (c) balance checks on the SELECTED rows of a family (mix_c2.py asserts them; c2_select.py reports them
and swaps units where it can). Pure functions over C2 rows + relations; CPU only; no I/O except importing a family's plugin for
its QFORMS (yes_is_bad, complement_kind).

Per family (program families, T37b, T40-T45): yes/no share (spec 3.0: 45-55%, T35 67-73%), yes rate 50 +/- 2 (hard yes/no rows),
yes-is-bad share 50 +/- 5, gold position and gold rank uniform with ONE count per (call_id, option count) cell (A49 b; partner rows
share the draw), longest-option within +/- 2 pp of 1/k, abstain option wrong on >= 50% overall and per option-count cell with
>= 30 rows, spec 3.0 token mean <= 800, spec 4.1 overlay shares (complement >= 20% of yes/no, >= 30% non-syntactic pairs, minimal-
edit twins 20-25%, equiv 5-10%). Blocks (GB, GW, MD, RTW) and carry pools are report-only here: their own A42-D rules bind.
A check that cannot be computed from the rows (gold rank without meta.gold_rank, a family without QFORMS) is "n/a" with the reason.
"""
from __future__ import annotations

import importlib
import math
import random
import re
import sys
from collections import Counter, defaultdict
from pathlib import Path

HERE = Path(__file__).resolve().parent
YN_SHARE = {"T35": (0.67, 0.73)}
YN_SHARE_DEFAULT = (0.45, 0.55)
try:
    from mixer import ABSTAIN  # c_build (pinned); the mixer's own abstain pattern
except ImportError:  # pragma: no cover - c_build not on the path
    ABSTAIN = re.compile(r"not enough information|cannot be determined|none of (these|the above)|no tool|general / other", re.I)
TOKEN_MEAN_MAX = 800
BINDING = "binding"


def _chi2_p(counts):
    from scipy.stats import chisquare
    return None if not counts or sum(counts) == 0 else float(chisquare(counts).pvalue)


def _plugin(fam: str):
    try:
        if str(HERE) not in sys.path:
            sys.path.insert(0, str(HERE))
        return importlib.import_module(f"families.{fam}.plugin")
    except Exception:  # noqa: BLE001 - no plugin: the QFORMS checks are n/a
        return None


def _chk(out, name, value, bar, ok, **extra):
    out[name] = {"value": value, "bar": bar, "verdict": "n/a" if ok is None else "pass" if ok else "fail", **extra}


def family_checks(fam: str, rows: list, rels: list, ntok: dict | None = None, plugin=None) -> dict:
    """{check: {value, bar, verdict}} for the rows of one family; verdict in pass / fail / n/a."""
    out: dict = {}
    n = len(rows) or 1
    yn = [r for r in rows if r["qtype"] == "noul"]
    ch = [r for r in rows if r["qtype"] == "choice"]
    lo, hi = YN_SHARE.get(fam, YN_SHARE_DEFAULT)
    share = len(yn) / n
    if not yn or not ch:
        _chk(out, "yes_no_share", round(share, 4), f"{lo:.0%}-{hi:.0%} where both forms exist (spec 3.0)", None,
             note="one answer format only by construction")
    else:
        _chk(out, "yes_no_share", round(share, 4), f"{lo:.0%}-{hi:.0%} (spec 3.0)", lo - 1e-9 <= share <= hi + 1e-9)
    yr = sum(int(r["gold"]) for r in yn) / len(yn) if yn else None
    _chk(out, "yes_rate", None if yr is None else round(yr, 4), "50 +/- 2 (spec 3.0)",
         None if yr is None else abs(yr - 0.5) <= 0.02 + 1e-9, n=len(yn))
    pl = plugin if plugin is not None else _plugin(fam)
    qf = getattr(pl, "QFORMS", None) or {}
    bad = [r for r in yn if getattr(qf.get((r.get("meta") or {}).get("qform")), "yes_is_bad", None) is not None]
    if bad:
        s = sum(1 for r in bad if qf[r["meta"]["qform"]].yes_is_bad) / len(bad)
        _chk(out, "yes_is_bad_share", round(s, 4), "50 +/- 5 (spec 3.0)", abs(s - 0.5) <= 0.05 + 1e-9, n=len(bad))
    else:
        _chk(out, "yes_is_bad_share", None, "50 +/- 5 (spec 3.0)", None, note="no question form declares yes_is_bad")
    # gold position / rank: one count per (call_id, k) cell (A49 b)
    cell = {}
    for r in sorted(ch, key=lambda r: r["id"]):
        o = r.get("options") or []
        if r.get("gold") in o:
            cell.setdefault((r.get("call_id") or r["id"], len(o)), (o.index(r["gold"]), (r.get("meta") or {}).get("gold_rank"),
                                                                    len(o)))
    pos, rank = defaultdict(Counter), defaultdict(Counter)
    for (_, k), (p, rk, _) in cell.items():
        pos[k][p] += 1
        if rk is not None:
            rank[k][rk] += 1
    pp = {k: _chi2_p([c[j] for j in range(k)]) for k, c in pos.items() if sum(c.values()) >= 5 * k}
    bp = sorted(k for k, p in pp.items() if p is not None and p <= 0.01)
    _chk(out, "gold_position_cells", {"cells": {str(k): sum(c.values()) for k, c in pos.items()},
                                      "chi2_p": {str(k): None if p is None else round(p, 4) for k, p in pp.items()}},
         "uniform per option count, one count per (call_id, k) cell: chi-square p > 0.01 (A49 b)", None if not pos else not bp,
         failing_k=bp)
    if rank:
        rp = {k: _chi2_p([c[j] for j in range(k)]) for k, c in rank.items() if sum(c.values()) >= 5 * k}
        br = sorted(k for k, p in rp.items() if p is not None and p <= 0.01)
        _chk(out, "gold_rank_cells", {"chi2_p": {str(k): None if p is None else round(p, 4) for k, p in rp.items()}},
             "ordered sets: gold rank uniform per cell (A49 b)", not br, failing_k=br)
    else:
        _chk(out, "gold_rank_cells", None, "gold rank uniform per cell (A49 b)", None,
             note="rows carry no meta.gold_rank (rank is a build-time statistic of ordered option sets): bound at full generation")
    lg = [0.0, 0.0, 0]
    ab: dict = defaultdict(lambda: [0, 0])
    for r in ch:
        o = r.get("options") or []
        if len(o) < 2 or r.get("gold") not in o:
            continue
        lens = [len(str(x)) for x in o]
        top = [j for j, x in enumerate(lens) if x == max(lens)]
        lg[0] += (1 / len(top)) if o.index(r["gold"]) in top else 0.0
        lg[1] += 1 / len(o)
        lg[2] += 1
        if any(ABSTAIN.search(str(x)) for x in o):
            c = ab[len(o)]
            c[0] += 1
            c[1] += bool(ABSTAIN.search(str(r["gold"])))
    d = 100 * (lg[0] - lg[1]) / lg[2] if lg[2] else None
    _chk(out, "longest_option_pp", None if d is None else round(d, 2), "gold-is-longest within +/- 2 pp of 1/k",
         None if d is None else abs(d) <= 2.0, n=lg[2])
    tot, gold = sum(c[0] for c in ab.values()), sum(c[1] for c in ab.values())
    cells_bad = [f"k{k}" for k, (m, g) in ab.items() if m >= 30 and 1 - g / m < 0.5]
    _chk(out, "abstain_wrong_share", None if not tot else round(1 - gold / tot, 4),
         "abstain option wrong on >= 50% of the rows that show it, overall and per option-count cell with >= 30 rows (spec 3.0)",
         None if not tot else (1 - gold / tot >= 0.5 and not cells_bad), rows_showing=tot, failing_cells=cells_bad,
         note="rows showing an option the mixer's ABSTAIN pattern matches")
    if ntok is not None and rows:
        m = sum(ntok.get(r["id"], 0) for r in rows) / len(rows)
        _chk(out, "token_mean", round(m, 1), f"mean <= {TOKEN_MEAN_MAX} real tokens (spec 3.0)", m <= TOKEN_MEAN_MAX)
    else:
        _chk(out, "token_mean", None, f"mean <= {TOKEN_MEAN_MAX} real tokens (spec 3.0)", None, note="no token counts given")
    # spec 4.1 overlay shares
    ids = {r["id"] for r in rows}
    comp = [x for x in rels if x.get("type") == "complement" and x["a"] in ids and x["b"] in ids]
    cids = {x["a"] for x in comp} | {x["b"] for x in comp}
    by_id = {r["id"]: r for r in rows}
    cshare = len(cids & {r["id"] for r in yn}) / len(yn) if yn else None
    _chk(out, "complement_share_of_yes_no", None if cshare is None else round(cshare, 4), ">= 20% of yes/no rows (spec 4.1)",
         None if cshare is None else cshare >= 0.20 - 1e-9)
    if comp and qf:
        def kind(i):
            f = getattr(qf.get((by_id[i].get("meta") or {}).get("qform")), "complement_kind", None)
            return f
        ns = sum(1 for x in comp if kind(x["a"]) not in (None, "syntactic") or kind(x["b"]) not in (None, "syntactic"))
        _chk(out, "non_syntactic_share_of_pairs", round(ns / len(comp), 4), ">= 30% of complement pairs (spec 4.1)",
             ns / len(comp) >= 0.30 - 1e-9)
    else:
        _chk(out, "non_syntactic_share_of_pairs", None, ">= 30% of complement pairs (spec 4.1)", None,
             note="no complement pairs or no QFORMS")
    tw = sum(1 for r in rows if (r.get("meta") or {}).get("twin_kind") == "minimal_edit") / n
    eq = sum(1 for r in rows if (r.get("meta") or {}).get("twin_kind") == "equiv") / n
    _chk(out, "twin_share", round(tw, 4), "minimal-edit twins 20-25% of rows (spec 4.1)", 0.20 - 1e-9 <= tw <= 0.25 + 1e-9)
    _chk(out, "equiv_share", round(eq, 4), "equiv twins 5-10% of rows (spec 4.1)", 0.05 - 1e-9 <= eq <= 0.10 + 1e-9)
    return out


def failing(checks: dict) -> list[str]:
    return sorted(k for k, v in checks.items() if v["verdict"] == "fail")


def _viol(tot, yn, yes, tw, fam):
    """Distance outside the A49 (c) bands a whole-unit swap can move: yes rate 50 +/- 2, yes/no share, minimal-edit twin share
    20-25% (only when the selection holds both yes/no and choice rows / twins at all). 0 = inside every band."""
    lo, hi = YN_SHARE.get(fam, YN_SHARE_DEFAULT)
    v = 0.0
    if yn:
        v += max(0.0, abs(yes / yn - 0.5) - 0.02)
        if yn < tot:
            v += max(0.0, lo - yn / tot, yn / tot - hi)
    if tw:
        v += max(0.0, 0.20 - tw / tot, tw / tot - 0.25)
    return v


def swap_balance(fam: str, rows: list, units: list, sel: list, bins: dict, seed, max_swaps: int = 600, never_in: set = frozenset(),
                 unit_class: dict | None = None) -> tuple[list, dict]:
    """Where it can: swap selected whole units for unselected ones of the SAME bin and the SAME row count so the selection comes
    inside the A49 (c) bands for the yes rate, the yes/no share and the minimal-edit twin share (greedy, seeded; the swap must
    lower the summed distance outside the bands). Labels are never touched. Returns (new unit-index list, info); a selection
    already inside, or one no swap improves, is returned as it is and info says so."""
    def stat(u):
        rr = [rows[i] for i in units[u]]
        yn = [r for r in rr if r["qtype"] == "noul"]
        return (len(rr), len(yn), sum(int(r["gold"]) for r in yn),
                sum(1 for r in rr if (r.get("meta") or {}).get("twin_kind") == "minimal_edit"))

    def bin_of(u):
        return (bins.get(rows[units[u][0]]["id"]), (unit_class or {}).get(u))      # A69: a trap-treated unit swaps only with one of its own type
    chosen = list(sel)
    st = {u: stat(u) for u in range(len(units))}
    T = [sum(st[u][j] for u in chosen) for j in range(4)]
    f0 = _viol(*T, fam)
    info = {"violation_before": round(f0, 5), "swaps": 0, "totals_before": {"rows": T[0], "yes_no": T[1], "yes": T[2], "twins": T[3]}}
    if f0 <= 1e-12:
        return chosen, info | {"note": "inside the bands; no swap"}
    rng = random.Random(f"{seed}|a49c|swap|{fam}")
    inn = set(chosen)
    out_by = defaultdict(list)
    for u in range(len(units)):
        if u not in inn and units[u] and u not in never_in:       # never_in: units the selection's seeded easy keep thinned out
            out_by[(bin_of(u), st[u][0])].append(u)
    for v in out_by.values():
        rng.shuffle(v)
    for _ in range(3):                                    # a few passes: one swap can unlock another
        for u in sorted(chosen, key=lambda u: rng.random()):
            if info["swaps"] >= max_swaps or _viol(*T, fam) <= 1e-12:
                break
            cur = _viol(*T, fam)
            key = (bin_of(u), st[u][0])
            best, bf = None, cur
            for v in out_by.get(key, [])[:80]:
                T2 = [T[j] - st[u][j] + st[v][j] for j in range(4)]
                f = _viol(*T2, fam)
                if f < bf - 1e-12:
                    best, bf = v, f
            if best is not None:
                T = [T[j] - st[u][j] + st[best][j] for j in range(4)]
                chosen[chosen.index(u)] = best
                out_by[key].remove(best)
                out_by[key].append(u)
                info["swaps"] += 1
    return chosen, info | {"violation_after": round(_viol(*T, fam), 5),
                           "totals_after": {"rows": T[0], "yes_no": T[1], "yes": T[2], "twins": T[3]}}


swap_yes_balance = None  # replaced by swap_balance (W6): yes rate, yes/no share and twin share


# ================================================================== PREREG Ruling A69 (DRAFT): the drop-only repair step
# SUPERSEDED (Ruling A80 b, 18 Oct 2026): repair_drop_only and its helpers below (unit_stats ... h64_tie) are the DRAFT greedy repair that built the first C2 select records. It is NOT the
# adopted A69 text (Record A78). c2_select.select_family / reselect no longer call repair_drop_only; they call a69_faithful.stage2 (the guarded swap of A69 (c) and the
# faithful repair of A69 (d)). The code is kept unchanged only so the old records stay reproducible and its tests keep running; nothing may import it for a new selection.
# Rows are only REMOVED (whole units, seeded); nothing is added, moved between bins or relabelled; no bar, band or cap is changed.
# It runs after swap_balance on the selected units of a program family, with the A49 (c) checks that are additive over units
# (yes/no share, yes rate, yes-is-bad share, longest option, abstain wrong, token mean, complement / non-syntactic / twin / equiv
# shares), the A42-D 1.5 rows-per-card cap, and two guards: the spec 5.2 bin caps and the A69 (b6) trap-type cap may not get
# worse by a drop. The chi-square checks (gold position / rank) are not additive; they are re-judged on the result.
ROWS_PER_CARD_MAX = 64                                     # A42-D 1.5 / spec 3.0 (mix_c2.ROWS_PER_CARD_MAX)
BIN_CAPS = {"easy": 0.25, "hard": 0.30}                    # spec 5.2; medium >= 0.45 (crowd_select.CAP / MED_MIN)
MED_MIN = 0.45
_SCALE = {"yes_no_share": 0.05, "yes_rate": 0.02, "yes_is_bad_share": 0.05, "longest_option_pp": 2.0, "abstain_wrong": 0.05,
          "token_mean": 8.0, "complement_share": 0.02, "non_syntactic_share": 0.03, "twin_share": 0.025, "equiv_share": 0.025,
          "card_rows": 8.0}   # only orders the greedy search (each check's excess in units of its own tolerance); never a bar


def card_of_row(r):
    return (r.get("meta") or {}).get("card_id") or r.get("card_id")


def unit_stats(fam: str, rows: list, rels: list, units: list, ntok: dict | None, plugin=None) -> list:
    """Per unit, the counts the A49 (c) checks add up (same row logic as family_checks)."""
    pl = plugin if plugin is not None else _plugin(fam)
    qf = getattr(pl, "QFORMS", None) or {}
    at = {rows[i]["id"]: u for u, x in enumerate(units) for i in x}
    comp_by_unit = defaultdict(list)
    for x in rels:
        if x.get("type") == "complement" and x.get("a") in at and x.get("b") in at and at[x["a"]] == at[x["b"]]:
            comp_by_unit[at[x["a"]]].append(x)
    by_id = {r["id"]: r for r in rows}
    out = []
    for u, idx in enumerate(units):
        s = Counter()
        cards = Counter()
        for i in idx:
            r = rows[i]
            m = r.get("meta") or {}
            s["n"] += 1
            s["tok"] += (ntok or {}).get(r["id"], 0)
            c = card_of_row(r)
            if c:
                cards[c] += 1
            if m.get("twin_kind") == "minimal_edit":
                s["twin"] += 1
            if m.get("twin_kind") == "equiv":
                s["equiv"] += 1
            if r["qtype"] == "noul":
                s["yn"] += 1
                s["yes"] += int(r["gold"])
                yb = getattr(qf.get(m.get("qform")), "yes_is_bad", None)
                if yb is not None:
                    s["bad_n"] += 1
                    s["bad_yes"] += bool(yb)
            else:
                s["ch"] += 1
                o = r.get("options") or []
                if len(o) >= 2 and r.get("gold") in o:
                    lens = [len(str(x)) for x in o]
                    top = [j for j, x in enumerate(lens) if x == max(lens)]
                    s["lg0"] += (1 / len(top)) if o.index(r["gold"]) in top else 0.0
                    s["lg1"] += 1 / len(o)
                    s["lg2"] += 1
                    if any(ABSTAIN.search(str(x)) for x in o):
                        s[f"ab_m{len(o)}"] += 1
                        s[f"ab_g{len(o)}"] += bool(ABSTAIN.search(str(r["gold"])))
        cids = set()
        for x in comp_by_unit.get(u, []):
            cids |= {x["a"], x["b"]}
            s["comp_pairs"] += 1
            if qf:
                def kind(i):
                    return getattr(qf.get((by_id[i].get("meta") or {}).get("qform")), "complement_kind", None)
                s["ns_pairs"] += int(kind(x["a"]) not in (None, "syntactic") or kind(x["b"]) not in (None, "syntactic"))
        s["comp_yn"] = sum(1 for i in idx if rows[i]["id"] in cids and rows[i]["qtype"] == "noul")
        s["_cards"] = cards                                  # a Counter inside a Counter value: summed separately
        out.append(s)
    return out


def _sum_stats(stats, units_in) -> tuple:
    tot, cards = Counter(), Counter()
    for u in units_in:
        s = stats[u]
        for k, v in s.items():
            if k != "_cards":
                tot[k] += v
        cards.update(s["_cards"])
    return tot, cards


def _band(v, lo, hi, scale):
    return max(0.0, lo - v, v - hi) / scale


def violation(fam: str, T: Counter, cards: Counter, has_qf: bool) -> float:
    """Summed excess (each check in units of its own tolerance) of the totals T outside the A49 (c) bands. 0 = inside all."""
    n = T["n"]
    if not n:
        return 0.0
    lo, hi = YN_SHARE.get(fam, YN_SHARE_DEFAULT)
    v = 0.0
    yn = T["yn"]
    if yn and T["ch"]:
        v += _band(yn / n, lo, hi, _SCALE["yes_no_share"])
    if yn:
        v += _band(T["yes"] / yn, 0.48, 0.52, _SCALE["yes_rate"])
        v += _band(T["comp_yn"] / yn, 0.20, 9.0, _SCALE["complement_share"])
    if T["bad_n"]:
        v += _band(T["bad_yes"] / T["bad_n"], 0.45, 0.55, _SCALE["yes_is_bad_share"])
    if T["lg2"]:
        v += _band(100 * (T["lg0"] - T["lg1"]) / T["lg2"], -2.0, 2.0, _SCALE["longest_option_pp"])
    ks = {k[4:] for k in T if k.startswith("ab_m")}
    tm = sum(T[f"ab_m{k}"] for k in ks)
    if tm:
        v += _band(1 - sum(T[f"ab_g{k}"] for k in ks) / tm, 0.5, 9.0, _SCALE["abstain_wrong"])
        for k in ks:
            if T[f"ab_m{k}"] >= 30:
                v += _band(1 - T[f"ab_g{k}"] / T[f"ab_m{k}"], 0.5, 9.0, _SCALE["abstain_wrong"])
    if T["tok"]:
        v += _band(T["tok"] / n, -1.0, TOKEN_MEAN_MAX, _SCALE["token_mean"])
    if has_qf and T["comp_pairs"]:
        v += _band(T["ns_pairs"] / T["comp_pairs"], 0.30, 9.0, _SCALE["non_syntactic_share"])
    v += _band(T["twin"] / n, 0.20, 0.25, _SCALE["twin_share"])
    v += _band(T["equiv"] / n, 0.05, 0.10, _SCALE["equiv_share"])
    v += sum(max(0, c - ROWS_PER_CARD_MAX) for c in cards.values()) / _SCALE["card_rows"]
    return v


def _cap_excess(bin_rows: Counter) -> float:
    tot = sum(bin_rows.values())
    if not tot:
        return 0.0
    return (max(0.0, bin_rows["hard"] / tot - BIN_CAPS["hard"]) + max(0.0, bin_rows["easy"] / tot - BIN_CAPS["easy"])
            + max(0.0, MED_MIN - bin_rows["medium"] / tot))


def _type_excess(type_units: Counter, cap: float) -> float:
    n = sum(type_units.values())
    return max(0.0, max((c / n - cap for c in type_units.values()), default=0.0)) if n else 0.0     # 0 inside the cap, as _cap_excess


def repair_drop_only(fam: str, rows: list, rels: list, units: list, sel: list, bins: dict, ntok: dict | None, seed,
                     unit_type: dict | None = None, type_cap: float = 0.35, plugin=None) -> tuple[list, dict]:
    """PREREG A69 (DRAFT) drop-only repair: from the selected whole units, greedily remove the unit whose removal lowers the summed
    violation of the additive A49 (c) checks (+ the 64-rows-per-card cap) the most (seeded tie-break), until every one is inside
    its bar or no single removal helps. A removal is refused when it would make the spec 5.2 bin caps (easy <= 25%, hard <= 30%,
    medium >= 45% of the realised rows) or the trap-type cap (A69 b6: `unit_type` = {unit: type} of the treated units) worse, so
    no cap is raised. Rows are only removed; the target may then be missed (spec 5.3: missing shares lower the total)."""
    pl = plugin if plugin is not None else _plugin(fam)
    has_qf = bool(getattr(pl, "QFORMS", None))
    stats = unit_stats(fam, rows, rels, units, ntok, pl)
    unit_type = unit_type or {}
    chosen = list(sel)
    T, cards = _sum_stats(stats, chosen)
    binrows = Counter()
    for u in chosen:
        for i in units[u]:
            binrows[bins[rows[i]["id"]]] += 1
    types = Counter(unit_type[u] for u in chosen if u in unit_type)
    v0 = violation(fam, T, cards, has_qf)
    info = {"violation_before": round(v0, 5), "units_dropped": 0, "rows_dropped": 0,
            "totals_before": {"rows": T["n"], "yes_no": T["yn"], "yes": T["yes"], "twins": T["twin"], "equiv": T["equiv"]},
            "has_ntok": bool(ntok), "has_qforms": has_qf}
    tie = {u: h64_tie(seed, fam, rows[units[u][0]]["id"]) for u in chosen}
    cur = v0

    def after(us):
        """(violation, ok) with the units `us` removed; ok = no bin cap and no trap-type cap gets worse by it."""
        T2, c2, b2, t2 = T.copy(), cards.copy(), binrows.copy(), types.copy()
        for u in us:
            s = stats[u]
            for k, x in s.items():
                if k != "_cards":
                    T2[k] -= x
            c2.subtract(s["_cards"])
            for i in units[u]:
                b2[bins[rows[i]["id"]]] -= 1
            if u in unit_type:
                t2[unit_type[u]] -= 1
        ok = _cap_excess(b2) <= _cap_excess(binrows) + 1e-12 and _type_excess(+t2, type_cap) <= _type_excess(types, type_cap) + 1e-12
        return violation(fam, T2, c2, has_qf), ok

    info["pair_steps"] = 0
    while cur > 1e-12 and chosen:
        best, bv, single = None, cur - 1e-12, []
        for u in chosen:
            v, ok = after((u,))
            single.append((v, tie[u], u))
            if ok and (v < bv - 1e-12 or (best is not None and abs(v - bv) <= 1e-12 and tie[u] < tie[best])):
                best, bv = u, v
        drop = (best,) if best is not None else ()
        if best is None:                    # no single removal helps: try the best PAIRS of the 40 most promising removals
            top = [u for _, _, u in sorted(single)[:40]]
            pv = cur - 1e-12
            for x in range(len(top)):
                for y in range(x + 1, len(top)):
                    v, ok = after((top[x], top[y]))
                    if ok and (v < pv - 1e-12 or (drop and abs(v - pv) <= 1e-12 and tie[top[x]] + tie[top[y]] < sum(tie[q] for q in drop))):
                        drop, pv = (top[x], top[y]), v
            if drop:
                bv = pv
                info["pair_steps"] += 1
        if not drop:
            break
        for u in drop:
            s = stats[u]
            for k, x in s.items():
                if k != "_cards":
                    T[k] -= x
            cards.subtract(s["_cards"])
            for i in units[u]:
                binrows[bins[rows[i]["id"]]] -= 1
            if u in unit_type:
                types[unit_type[u]] -= 1
            chosen.remove(u)
            info["units_dropped"] += 1
            info["rows_dropped"] += s["n"]
        cur = bv
    info |= {"violation_after": round(cur, 5), "totals_after": {"rows": T["n"], "yes_no": T["yn"], "yes": T["yes"],
                                                                   "twins": T["twin"], "equiv": T["equiv"]},
             "stopped": "inside every additive band" if cur <= 1e-12 else "no single removal lowers the violation"}
    return chosen, info


def h64_tie(seed, fam, first_id) -> int:
    from mixio import h64
    return h64(seed, fam, "a69|repair", first_id)


def card_max(rows) -> int:
    return max(Counter(card_of_row(r) for r in rows if card_of_row(r)).values(), default=0)
