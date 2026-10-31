"""a69_faithful.py (A78, wired by A80 b): the drop-only repair of ADOPTED Ruling A69 (d), the guarded swap of (c), and the (f) admission tests,
written to the adopted text (c2_build/zed_orch/c21/A69_SELECTION_RULING.md, sha256 b1ed6d7346ec5261...) and its companion builder spec section 6.
CPU only. Imports the existing tools READ-ONLY (a49c, c2_select, crowd_select, mixer, mix_c2); edits none of them; writes nothing itself
(c2_select.select_family / reselect write the select record, mix_c2 reads it). Rows are only removed, never added, edited or relabelled; no bar,
band or cap is changed. This file is the move of zed_orch/a78/repair_a69_faithful.py (which is now a thin import of it) plus the A80 (b) fixes:
  D1  the combined token_mean entry is built only when BOTH check groups (family_checks' exact mean, cap_checks' 1-decimal mean) were evaluated,
      and its verdict is the stricter of the two, so an exact mean in (800.00, 800.05] can no longer abort the run.
  L1  (f)(ii) checks rows_pre_repair - rows_dropped == rows selected also when rows_dropped == 0, and refuses a record with no repair block.
  L2  (f)(ii) requires the four (f) report.checks entries; (f)(i) refuses a record without the a42d6 / a69 blocks, a scratch record, or tool
      shas other than the pinned A69_TOOL_SHAS (mix_c2 holds the pin; program_record_problem takes it as an argument).
  L3  A34 (e) ("short of its base target ONLY because G13 removed units") is read literally: see g13_counterfactual and READING L3 below.

Wiring: c2_select.select_family and reselect call stage2() (trap_select -> guarded swap (c) -> repair (d)); mix_c2.selection_problem calls
program_selection_problem() for a program family.

What it does (all numbers from the adopted text):
  (d1) 16 checks in a FIXED order, each judged by the function that binds it (a49c.family_checks, mix_c2.cap_checks,
       mixer.g10_checks, crowd_select.selection_report), at its adopted bar.
  (d2) a MOVE drops ONE selected unit u, then crowd_select's own cap pass (hard, then easy: units holding that bin and no medium
       row, walked from the END of the priority order, while the bin is above its cap) sheds companions.
  (d3) candidates = the selected units in reverse (b4) priority, lowest first.
  (d4) a move is admissible only if: removing u alone strictly lowers the failing check's distance AND so does the whole move;
       no check that passes before the move fails after it (every d1 check, the difficulty caps, the 35% type cap, G11); no failing
       check's distance rises; total repair loss (companions included) <= 25% of the pre-repair rows. The FIRST admissible
       candidate is dropped; repeat until the check passes or none is admissible; then the next check; at most 3 passes.
  (d5) it may stop below target; nothing refills (no fill, reflow, swap or re-selection runs after it).
  (d6) every move is recorded.
  (f)(ii) short_record_decision / selection_problem_faithful: a short record is accepted only when total_eq_target is the only
       failed check, rows_pre_repair - rows_dropped == rows selected, rows_dropped <= 25% of rows_pre_repair, and the pre-repair
       selection was at target or A34 (e) (G13 removed units, read literally: L3) / an upper-bound target applies.

READINGS chosen where the text is silent (each is also listed in the A78 / A80 reports):
  R1 distance. The ruling says "distance" without a formula. The distances are the ones of the companion builder spec 6.2: the
     excess outside the bar in the check's own units, with the binding function's tolerance subtracted, so distance == 0 exactly
     when the binding verdict is pass / n/a (asserted on every evaluated state: SystemExit on a mismatch). A multi-part check
     (G10 cells, gold position / rank cells, the chi-squares, abstain cells, rows per card) is the SUM of its parts' excesses;
     p-value parts are in -log10(p) above 2, capped at 300, +1e-6 so a failing part is never 0.
  R2 item 16 ("chi-square label x bin, on both bin maps") is ONE list item: it fails when either map fails and its distance is
     the sum of both maps; the two maps are separate PROTECTED sub-checks (chi2_a42d6, chi2_pg).
  R3 token mean: binds in two functions (mix_c2.cap_checks on the rounded mean, a49c.family_checks on the exact mean); the check
     fails if either fails (the stricter reading, D1); distance max(0, mean - 800). Needs real token counts for every row (SystemExit otherwise).
  R4 "the difficulty caps" = hard <= 30% on the A42-D 6 bins (cap_checks), easy <= 25% on the A42-D 6 bins (cap_checks) and on the
     p_g bins (A69 f v). medium >= 45% (a crowd_select report check that report.pass needs, so (f)(ii) needs it) is a separate
     PROTECTED entry: a move may not take a passing medium share below 45%.
  R5 "priority" = position in the final (b4) race order (the order of the selection that produced the pre-repair set); the cap pass
     walks that order from its end (ruling d2 "from the end of the priority order"), not crowd_select's internal append order.
  R6 loss limit: cumulative rows dropped (u plus companions of every move so far) + this move's rows <= floor(rows_pre / 4), with
     rows_pre = the rows of the selection that ENTERS the repair (after the swap step; the swap keeps row counts).
  R7 trap type cap (protected): over the SELECTED units that kept the trap treatment, no ptype holds more than 35% of them
     (count > 0.35 N + 1e-9 fails, as the (b6) loop reads it); N = 0 passes. The treated set is the final (b6) set; the repair
     never changes it.
  R8 G11: no meta.c2.skin_id and no meta.wording_id above 2% of the selected rows (share > 0.02 fails), counted on the selected rows.
  R9 strictness margin: "strictly lowers" = lowers by more than 1e-12 (float noise guard) or reaches exactly 0 from a positive distance (lowers());
     "rises" = rises by more than 1e-12.
  R10 "n/a" counts as pass; a check whose verdict is fail before AND after a move is judged on its distance only.
  R11 passes: a pass is one walk over the 16 checks; the walk stops early when a whole pass made no move (the state is then
     unchanged, so another pass would repeat it); at most 3 passes.
  R12 (A80, replaces the A78 fallback) (f)(ii) has ONE path for every program record: the four (f) report.checks entries and a repair block
     must be present; rows_pre_repair - rows_dropped must equal the rows selected (also when rows_dropped is 0); rows_dropped <= 25% of
     rows_pre_repair; total_eq_target may be the only failed check; and a record short before the repair needs A34 (e) (L3) or an upper bound.
  R13 the swap guard of (c) ("kept only if no check that passed before it fails after it") is swap_balance_guarded: a49c.swap_balance's
     loop and seeded order, plus the guard; with guard None its output is identical to a49c.swap_balance's.
  R14 cost: every candidate is judged with the real binding functions (no incremental shortcut), so a stuck check on a
     2,400-row family scans every selected unit once per pass; expect minutes per family, not seconds.
  L3 (A34 e, read literally). "An included family that is short of its base target ONLY because G13 removed units enters with its realised rows,
     when every other selection check passes." The loose reading the old mix used (any G13-removed unit at all) admits a family that would have
     been short anyway. Literal reading: the shortfall is caused by the removal alone iff the SAME first-stage selection (A42-D 6 trap weighting,
     same seed, key and settings) run on the pool BEFORE the G13 removal reaches the target exactly; g13_counterfactual computes that, the select
     record stores it (a69.a34e.short_only_because_g13), and (f)(ii) admits a pre-repair shortfall only on that flag (or an upper-bound target).
     A family not short before the repair needs no A34 (e). A record without the field cannot show it: refused.
"""
from __future__ import annotations

import importlib
import json
import math
import re
import statistics
import sys
from collections import Counter, OrderedDict, defaultdict
from functools import lru_cache
from pathlib import Path

C2B = Path(__file__).resolve().parent                # c2_build
if str(C2B) not in sys.path:
    sys.path.insert(0, str(C2B))
import c2io  # noqa: E402  (puts c_build on sys.path)
import a49c  # noqa: E402
import crowd_select as cs  # noqa: E402
import mixer  # noqa: E402
from mixio import sha256_file  # noqa: E402


class _Lazy:
    """A module looked up on first use. mix_c2 and c2_select import this file, and this file uses their pure functions and constants,
    so neither is imported at load time (no import cycle, whichever of the three is imported first)."""

    def __init__(self, name: str):
        object.__setattr__(self, "_name", name)

    def __getattr__(self, attr):
        return getattr(importlib.import_module(object.__getattribute__(self, "_name")), attr)


mix_c2 = _Lazy("mix_c2")
c2_select = _Lazy("c2_select")

SEED = c2io.SEED                                      # 20261013
EPS = 1e-12                                           # R9
PASSES = 3                                            # (d4)
LOSS_DEN = 4                                          # (d4): total repair loss <= 25% of the pre-repair rows
TYPE_CAP = 0.35                                       # A42-D 6.4
G11_MAX = 0.02                                        # G11 (spec 6.3)
TOKEN_MEAN_MAX = 800

ORDER = ["rows_per_card", "token_mean", "freeform_share", "yes_no_share", "yes_rate", "g10_cells", "yes_is_bad_share",
         "twin_share", "equiv_share", "complement_share_of_yes_no", "non_syntactic_share_of_pairs", "longest_option_pp",
         "abstain_wrong_share", "gold_position_cells", "gold_rank_cells", "chi2_label_x_bin"]        # (d1), 1..16
SUB = {"chi2_label_x_bin": ("chi2_a42d6", "chi2_pg")}                                                # R2
EXTRA_PROTECTED = ["difficulty_caps", "medium_ge_45", "trap_type_cap", "g11_selected"]                # (d4); R4
PROTECTED = [c for c in ORDER if c not in SUB] + ["chi2_a42d6", "chi2_pg"] + EXTRA_PROTECTED
ALL_NAMES = ORDER + ["chi2_a42d6", "chi2_pg"] + EXTRA_PROTECTED
GROUP_OF = {
    "rows_per_card": ("cap",), "token_mean": ("fc", "cap"), "freeform_share": ("cap",), "difficulty_caps": ("cap",),
    "yes_no_share": ("fc",), "yes_rate": ("fc",), "yes_is_bad_share": ("fc",), "twin_share": ("fc",), "equiv_share": ("fc",),
    "complement_share_of_yes_no": ("fc",), "non_syntactic_share_of_pairs": ("fc",), "longest_option_pp": ("fc",),
    "abstain_wrong_share": ("fc",), "gold_position_cells": ("fc",), "gold_rank_cells": ("fc",),
    "g10_cells": ("g10",), "chi2_a42d6": ("sr6",), "medium_ge_45": ("sr6",), "chi2_pg": ("srpg",),
    "chi2_label_x_bin": ("sr6", "srpg"), "trap_type_cap": ("trap",), "g11_selected": ("g11",)}
ALL_GROUPS = ("fc", "cap", "g10", "sr6", "srpg", "trap", "g11")


class _NoPlugin:
    QFORMS: dict = {}


def _logp_excess(p) -> float:
    """R1: a failing p-value part (p <= 0.01) as -log10(p) above 2, capped at 300, +1e-6."""
    if p is None or not p <= cs.CHI_P:
        return 0.0
    return min(300.0, 300.0 if p <= 0 else -math.log10(p)) - 2.0 + 1e-6


@lru_cache(maxsize=None)
def _binom_p(k: int, n: int) -> float:
    from scipy.stats import binomtest
    return float(binomtest(k, n, 0.5).pvalue)


def _negcount():
    p = str(mixer.LEAN / "c_src/common")
    if p not in sys.path:
        sys.path.insert(0, p)
    import negcount
    return negcount


# ================================================================== distances (R1): the binding functions' own formulas

def fc_distances(fam: str, R: list, rl: list, qf: dict, ntok: dict | None) -> dict:
    """{a49c.family_checks check name: distance}; replicates family_checks' arithmetic (same order of summation) so a distance
    is 0 exactly when the check's verdict is not fail."""
    n = len(R) or 1
    yn = [r for r in R if r["qtype"] == "noul"]
    ch = [r for r in R if r["qtype"] == "choice"]
    lo, hi = a49c.YN_SHARE.get(fam, a49c.YN_SHARE_DEFAULT)
    d: dict = {}
    share = len(yn) / n
    d["yes_no_share"] = 0.0 if (not yn or not ch) else max(0.0, (lo - 1e-9) - share, share - (hi + 1e-9))
    yr = sum(int(r["gold"]) for r in yn) / len(yn) if yn else None
    d["yes_rate"] = 0.0 if yr is None else max(0.0, abs(yr - 0.5) - (0.02 + 1e-9))
    bad = [r for r in yn if getattr(qf.get((r.get("meta") or {}).get("qform")), "yes_is_bad", None) is not None]
    if bad:
        s = sum(1 for r in bad if qf[r["meta"]["qform"]].yes_is_bad) / len(bad)
        d["yes_is_bad_share"] = max(0.0, abs(s - 0.5) - (0.05 + 1e-9))
    else:
        d["yes_is_bad_share"] = 0.0
    cell = {}
    for r in sorted(ch, key=lambda r: r["id"]):
        o = r.get("options") or []
        if r.get("gold") in o:
            cell.setdefault((r.get("call_id") or r["id"], len(o)), (o.index(r["gold"]), (r.get("meta") or {}).get("gold_rank"), len(o)))
    pos, rank = defaultdict(Counter), defaultdict(Counter)
    for (_, k), (p, rk, _) in cell.items():
        pos[k][p] += 1
        if rk is not None:
            rank[k][rk] += 1
    pp = {k: a49c._chi2_p([c[j] for j in range(k)]) for k, c in pos.items() if sum(c.values()) >= 5 * k}
    d["gold_position_cells"] = sum(_logp_excess(p) for p in pp.values())
    if rank:
        rp = {k: a49c._chi2_p([c[j] for j in range(k)]) for k, c in rank.items() if sum(c.values()) >= 5 * k}
        d["gold_rank_cells"] = sum(_logp_excess(p) for p in rp.values())
    else:
        d["gold_rank_cells"] = 0.0
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
        if any(a49c.ABSTAIN.search(str(x)) for x in o):
            c = ab[len(o)]
            c[0] += 1
            c[1] += bool(a49c.ABSTAIN.search(str(r["gold"])))
    dd = 100 * (lg[0] - lg[1]) / lg[2] if lg[2] else None
    d["longest_option_pp"] = 0.0 if dd is None else max(0.0, abs(dd) - 2.0)
    tot, gold = sum(c[0] for c in ab.values()), sum(c[1] for c in ab.values())
    if tot:
        v = max(0.0, 0.5 - (1 - gold / tot))
        for k, (m, g) in ab.items():
            if m >= 30 and 1 - g / m < 0.5:
                v += 0.5 - (1 - g / m) + 1e-6
        d["abstain_wrong_share"] = v
    else:
        d["abstain_wrong_share"] = 0.0
    if ntok is not None and R:
        m = sum(ntok.get(r["id"], 0) for r in R) / len(R)
        d["token_mean@fc"] = max(0.0, m - TOKEN_MEAN_MAX)
    else:
        d["token_mean@fc"] = 0.0                                       # no rows (or no counts): family_checks says n/a; always present, so the D1 combination never lacks a part
    ids = {r["id"] for r in R}
    comp = [x for x in rl if x.get("type") == "complement" and x["a"] in ids and x["b"] in ids]
    cids = {x["a"] for x in comp} | {x["b"] for x in comp}
    by_id = {r["id"]: r for r in R}
    cshare = len(cids & {r["id"] for r in yn}) / len(yn) if yn else None
    d["complement_share_of_yes_no"] = 0.0 if cshare is None else max(0.0, (0.20 - 1e-9) - cshare)
    if comp and qf:
        def kind(i):
            return getattr(qf.get((by_id[i].get("meta") or {}).get("qform")), "complement_kind", None)
        ns = sum(1 for x in comp if kind(x["a"]) not in (None, "syntactic") or kind(x["b"]) not in (None, "syntactic"))
        d["non_syntactic_share_of_pairs"] = max(0.0, (0.30 - 1e-9) - ns / len(comp))
    else:
        d["non_syntactic_share_of_pairs"] = 0.0
    tw = sum(1 for r in R if (r.get("meta") or {}).get("twin_kind") == "minimal_edit") / n
    eq = sum(1 for r in R if (r.get("meta") or {}).get("twin_kind") == "equiv") / n
    d["twin_share"] = max(0.0, (0.20 - 1e-9) - tw, tw - (0.25 + 1e-9))
    d["equiv_share"] = max(0.0, (0.05 - 1e-9) - eq, eq - (0.10 + 1e-9))
    return d


def g10_distance(R: list) -> float:
    """Distance of the three G10 lines the repair judges: aggregate yes rate (50 +/- 2, on the 4-dp rounded rate as mixer),
    cells of >= 50 rows outside 50 +/- 2, cells of < 50 rows with binomial p < 0.01."""
    nc = _negcount()
    hard = [r for r in R if r["qtype"] == "noul" and not mixer.own_target(r.get("meta") or {})]
    fam_rate, cells = defaultdict(list), defaultdict(list)
    for r in hard:
        m = r.get("meta") or {}
        fam_rate[r["_block"]].append(int(r["gold"]))
        cells[(r["_block"], str(m.get("wording_id")), str(m.get("difficulty_bin")), nc.k_all(r["instructions"]))].append(int(r["gold"]))
    v = 0.0
    for b, x in fam_rate.items():
        if b.startswith("c_pub"):
            continue
        agg = round(sum(x) / len(x), 4)
        v += max(0.0, abs(agg - 0.5) - 0.02)
    for x in cells.values():
        if len(x) >= 50:
            v += max(0.0, abs(sum(x) / len(x) - 0.5) - (0.02 + 1e-12))
        else:
            p = _binom_p(sum(x), len(x))
            if p < 0.01:
                v += min(300.0, 300.0 if p <= 0 else -math.log10(p)) - 2.0 + 1e-6
    return v


def _entry(verdict: str, dist: float) -> tuple:
    return (verdict, float(dist))


def rd(x: float) -> float:
    """round(x, 6) for the move log, except that a positive distance which would round to 0.0 keeps 6 significant digits (a float-noise distance such as
    1.7e-17 must not be logged as 0.0 -> 0.0 when the move that clears it is recorded)."""
    r = round(x, 6)
    return r if (r != 0.0 or x == 0.0) else float(f"{x:.6g}")


def lowers(new: float, old: float) -> bool:
    """R9 / A80 skeptic: 'strictly lowers the distance' = lowers by more than EPS (the float-noise guard), OR reaches exactly 0 from a positive
    distance. A check that goes from fail to pass has always strictly lowered its distance, however small the float-noise excess was: the mixer's G10
    aggregate yes rate (no tolerance, 4-dp rounded) fails at exactly 52.00% / 48.00% by 1.7e-17 while A49 (c) yes_rate (1e-9 tolerance) passes, and
    the EPS guard alone would make that one-row fix 'not strictly lower' (an unrepairable check, the family left out)."""
    return new < old - EPS or (new == 0.0 and old > 0.0)


def _consistent(name: str, e: tuple):
    v, dd = e
    if (v == "fail") != (dd > 0.0):
        raise SystemExit(f"A69 repair: distance of '{name}' is {dd!r} but its binding verdict is '{v}' (the distance helper and "
                         f"the binding function disagree)")


# ================================================================== the evaluator

class Family:
    """One family's pool + the state the repair needs. Units are indices into `units` (lists of indices into `rows`)."""

    def __init__(self, fam, rows, rels, units, bins6, pgbins, pg, ntok, order, treated, ptype=None, target=0, plugin=None):
        self.fam, self.rows, self.units, self.target = fam, rows, units, target
        self.bins6, self.pgbins, self.pg = bins6, pgbins, pg
        if ntok is None or any(r["id"] not in ntok for r in rows):
            raise SystemExit(f"{fam}: A69 (d1) item 2 binds on real tokens; every pool row needs a token count (R3)")
        self.ntok = ntok
        self.order = list(order)
        if sorted(self.order) != list(range(len(units))):
            raise SystemExit(f"{fam}: the priority order is not a permutation of the units")
        self.treated = dict(treated or {})                  # {unit index: trap type}: the final (b6) treated set
        self.ptype = dict(ptype) if ptype is not None else dict(self.treated)
        pl = plugin if plugin is not None else a49c._plugin(fam)
        self.plugin = pl if pl is not None else _NoPlugin()
        self.qf = getattr(self.plugin, "QFORMS", None) or {}
        self.prow = []
        for r in rows:
            m = dict(r.get("meta") or {})
            m["difficulty_bin"], m["pg_bin"], m["crowd_pg"] = bins6[r["id"]], pgbins[r["id"]], pg.get(r["id"])
            self.prow.append(r | {"meta": m, "_block": fam})
        at = {rows[i]["id"]: u for u, x in enumerate(units) for i in x}
        self.rels_u = defaultdict(list)
        for x in rels:
            if x.get("a") in at and x.get("b") in at:
                self.rels_u[at[x["a"]]].append(x)
        self.ubins = [Counter(bins6[rows[i]["id"]] for i in x) for x in units]
        self.nrows = [len(x) for x in units]
        self.first_id = [rows[x[0]]["id"] for x in units]
        self._memo: OrderedDict = OrderedDict()
        self._card_applicable = (fam in mix_c2.PROGRAM or fam in mix_c2.NEW_FAMILIES or fam in mix_c2.POST_FREEZE
                                 or fam in mix_c2.DI_BLOCKS)

    # ---- state helpers
    def rows_of(self, S) -> list:
        return [self.prow[i] for i in sorted(i for u in S for i in self.units[u])]

    def n_rows(self, S) -> int:
        return sum(self.nrows[u] for u in S)

    # ---- groups
    def _groups(self, S: frozenset, groups) -> dict:
        out: dict = {}
        for g in groups:
            key = (S, g)
            if key not in self._memo:
                if len(self._memo) > 96:
                    self._memo.popitem(last=False)
                self._memo[key] = getattr(self, "_g_" + g)(S)
            out.update(self._memo[key])
        return out

    def _g_fc(self, S):
        R = self.rows_of(S)
        rl = [x for u in sorted(S) for x in self.rels_u.get(u, [])]
        fc = a49c.family_checks(self.fam, R, rl, self.ntok, plugin=self.plugin)
        dist = fc_distances(self.fam, R, rl, self.qf, self.ntok)
        out = {}
        for nm, dd in dist.items():
            if nm == "token_mean@fc":
                out[nm] = _entry(fc["token_mean"]["verdict"], dd)
            else:
                out[nm] = _entry(fc[nm]["verdict"], dd)
        return out

    def _g_cap(self, S):
        R = self.rows_of(S)
        n = len(R)
        rep, probs = mix_c2.cap_checks(R, self.ntok, True)
        mine = [p for p in probs if p.startswith(f"{self.fam}: ")]
        has = lambda s: any(s in p for p in mine)  # noqa: E731
        out = {}
        cards = Counter(mix_c2.card_of(r) for r in R if mix_c2.card_of(r))
        d_cards = sum(max(0, c - mix_c2.ROWS_PER_CARD_MAX) for c in cards.values()) if self._card_applicable else 0
        out["rows_per_card"] = _entry("fail" if has("a card holds") else "pass", d_cards)
        mean = sum(self.ntok.get(r["id"], 0) for r in R) / max(1, n)
        out["token_mean@cap"] = _entry("fail" if has("tokens per row >") else "pass", max(0.0, mean - TOKEN_MEAN_MAX))
        ff = sum(1 for r in R if ((r.get("meta") or {}).get("c2") or {}).get("author_mode") == "F")
        cap = mix_c2.FREEFORM_MAX_FAM.get(self.fam, mix_c2.FREEFORM_MAX)
        d_ff = 0.0 if self.fam in mix_c2.BLOCK_TARGETS else max(0.0, ff / max(1, n) - (cap + 1e-12))
        out["freeform_share"] = _entry("fail" if has("free-form rows") else "pass", d_ff)
        b6 = Counter((r["meta"]).get("difficulty_bin") or "na" for r in R)
        easy_pg = sum(1 for r in R if r["meta"].get("pg_bin") == "easy") / max(1, n)
        E, H = mix_c2.EASY_MAX, mix_c2.HARD_MAX
        d_caps = (max(0.0, b6["hard"] / max(1, n) - (H + 1e-9)) + max(0.0, b6["easy"] / max(1, n) - (E + 1e-9))
                  + max(0.0, easy_pg - (E + 1e-9)))
        fail = has("difficulty easy") or easy_pg > E + 1e-9
        out["difficulty_caps"] = _entry("fail" if fail else "pass", d_caps)
        return out

    def _g_g10(self, S):
        R = self.rows_of(S)
        probs = mixer.g10_checks(R, {}, True, side={})
        fail = any(p.startswith(("G10 yes-rate cell outside", "G10 aggregate yes rate")) or re.match(r"G10 \d+ small yes-rate cells", p)
                   for p in probs)
        return {"g10_cells": _entry("fail" if fail else "pass", g10_distance(R))}

    def _sr(self, S, bins):
        return cs.selection_report(self.rows, self.units, sorted(S), bins, self.target, True, self.pg)

    @staticmethod
    def _chi_distance(rep) -> float:
        ps = [rep["chi2_label_x_bin"]["yes_no"], *rep["chi2_label_x_bin"]["choice_by_k"].values()]
        return sum(_logp_excess(p) for p in ps if p is not None)

    def _g_sr6(self, S):
        rep = self._sr(S, self.bins6)
        ok = rep["checks"]["chi2_p_gt_0.01"]
        med = rep["shares"].get("medium", 0)
        return {"chi2_a42d6": _entry("pass" if ok else "fail", self._chi_distance(rep)),
                "medium_ge_45": _entry("pass" if rep["checks"]["medium_ge_45"] else "fail", max(0.0, (cs.MED_MIN - 1e-9) - med))}

    def _g_srpg(self, S):
        rep = self._sr(S, self.pgbins)
        return {"chi2_pg": _entry("pass" if rep["checks"]["chi2_p_gt_0.01"] else "fail", self._chi_distance(rep))}

    def _g_trap(self, S):
        t = Counter(self.ptype[u] for u in S if u in self.treated)
        N = sum(t.values())
        fail = any(c > TYPE_CAP * N + 1e-9 for c in t.values())
        d = sum(max(0.0, c - (TYPE_CAP * N + 1e-9)) / N for c in t.values()) if N else 0.0
        return {"trap_type_cap": _entry("fail" if fail else "pass", d)}

    def _g_g11(self, S):
        R = self.rows_of(S)
        n = len(R) or 1
        skins = Counter(((r.get("meta") or {}).get("c2") or {}).get("skin_id") for r in R)
        words = Counter((r.get("meta") or {}).get("wording_id") for r in R)
        skins.pop(None, None)
        words.pop(None, None)
        shares = [v / n for v in [*skins.values(), *words.values()]]
        fail = any(s > G11_MAX for s in shares)
        return {"g11_selected": _entry("fail" if fail else "pass", sum(max(0.0, s - G11_MAX) for s in shares))}

    # ---- evaluation
    def _finalize(self, out: dict) -> dict:
        if "token_mean@fc" in out and "token_mean@cap" in out:
            # D1 (A80): the combined entry exists only when BOTH groups were evaluated. family_checks judges the exact mean and cap_checks the
            # mean rounded to 1 decimal, so an exact mean in (800.00, 800.05] passes one and fails the other; built from one group alone
            # it would be (pass, distance > 0) and _consistent would abort. Here the verdict is the stricter reading: fail when either part
            # fails or when the exact-mean distance is above 0 (the same thing for the fc part), so verdict and distance always agree.
            parts = [out["token_mean@fc"], out["token_mean@cap"]]
            dist = max(p[1] for p in parts)
            out["token_mean"] = _entry("fail" if (any(p[0] == "fail" for p in parts) or dist > 0.0) else "pass", dist)
        if "chi2_a42d6" in out and "chi2_pg" in out:
            a, b = out["chi2_a42d6"], out["chi2_pg"]
            out["chi2_label_x_bin"] = _entry("fail" if "fail" in (a[0], b[0]) else "pass", a[1] + b[1])
        for k, e in out.items():
            if "@" not in k:
                _consistent(k, e)
        return out

    def some(self, S, names) -> dict:
        S = frozenset(S)
        gs = []
        for nm in names:
            for g in GROUP_OF[nm]:
                if g not in gs:
                    gs.append(g)
        out = self._finalize(self._groups(S, gs))
        return {nm: out[nm] for nm in names}

    def all(self, S) -> dict:
        S = frozenset(S)
        out = self._finalize(self._groups(S, ALL_GROUPS))
        return {nm: out[nm] for nm in ALL_NAMES}

    # ---- (d2) a move
    def move(self, S: frozenset, u: int) -> tuple:
        """S - {u}, then crowd_select's cap pass (verbatim rule) walking the priority order from its end. Returns (new set,
        companion units in the order they were shed)."""
        S1 = set(S)
        S1.discard(u)
        used = Counter()
        for v in S1:
            used.update(self.ubins[v])
        comps = []
        for b in ("hard", "easy"):
            for v in [x for x in reversed(self.order) if x in S1]:
                tot = sum(used.values())
                if used[b] <= cs.CAP[b] * tot + 1e-9:
                    break
                bs = self.ubins[v]
                if bs[b] and not bs["medium"]:
                    S1.discard(v)
                    used.subtract(bs)
                    comps.append(v)
        return frozenset(S1), comps

    # ---- (d4) the protected-check rule
    @staticmethod
    def protected_ok(before: dict, after: dict) -> bool:
        for p in PROTECTED:
            vb, db = before[p]
            va, da = after[p]
            if vb != "fail" and va == "fail":
                return False                                  # a passing check fails after the move
            if vb == "fail" and da > db + EPS:
                return False                                  # a failing check's distance rises
        return True

    def guard(self, old, new) -> bool:
        """(c): a swap is kept only if no PROTECTED check that passed before it fails after it."""
        B, A = self.all(old), self.all(new)
        return not any(B[p][0] != "fail" and A[p][0] == "fail" for p in PROTECTED)

    # ---- (d) the repair
    def repair(self, sel) -> tuple:
        S = frozenset(sel)
        rows_pre, units_pre = self.n_rows(S), len(S)
        loss_max = rows_pre // LOSS_DEN                      # floor(25% of the pre-repair rows)
        base = self.all(S)
        failing_before = [c for c in ORDER if base[c][0] == "fail"]
        moves, dropped, stop, loss_hit, passes_run = [], 0, {}, False, 0
        for _ in range(PASSES):
            passes_run += 1
            progress = False
            for c in ORDER:
                while base[c][0] == "fail":
                    found, loss_blocked = None, False
                    for u in [x for x in reversed(self.order) if x in S]:
                        d0 = base[c][1]
                        if not lowers(self.some(S - {u}, [c])[c][1], d0):
                            continue                           # removing u alone must strictly lower the distance
                        M, comps = self.move(S, u)
                        if comps and not lowers(self.some(M, [c])[c][1], d0):
                            continue                           # ... and so must the whole move
                        A = self.all(M)
                        if not lowers(A[c][1], d0) or not self.protected_ok(base, A):
                            continue
                        lost = self.n_rows(S) - self.n_rows(M)
                        if dropped + lost > loss_max:
                            loss_blocked = True
                            continue
                        found = (u, comps, M, A, lost)
                        break                                  # the FIRST admissible candidate
                    if found is None:
                        stop[c] = "loss limit" if loss_blocked else "no admissible unit"
                        loss_hit = loss_hit or loss_blocked
                        break
                    u, comps, M, A, lost = found
                    changed = {nm: [rd(base[nm][1]), rd(A[nm][1])] for nm in ALL_NAMES
                               if abs(A[nm][1] - base[nm][1]) > EPS or A[nm][0] != base[nm][0]}
                    moves.append({
                        "check": c, "unit_first_id": self.first_id[u], "unit_rows": self.nrows[u],
                        "rows_by_bin6": dict(self.ubins[u]), "treated": u in self.treated, "ptype": self.ptype.get(u),
                        "companions": [[self.first_id[v], self.nrows[v]] for v in comps],
                        "distance_before": rd(base[c][1]), "distance_after": rd(A[c][1]), "changed_distances": changed})
                    S, base, dropped, progress = M, A, dropped + lost, True
            if not progress:
                break
        for c in ORDER:
            stop[c] = "passed" if base[c][0] != "fail" else stop.get(c, "not reached")
        rec = {
            "rule": "A69 (d) drop-only repair, faithful (a78)", "seed": SEED, "key": self.fam,
            "checks_order": ORDER, "protected": PROTECTED, "rows_pre_repair": rows_pre, "units_pre_repair": units_pre,
            "loss_max_rows": loss_max, "moves": moves,
            "units_dropped": units_pre - len(S), "rows_dropped": rows_pre - self.n_rows(S), "rows_after": self.n_rows(S),
            "passes_run": passes_run, "loss_limit_hit": loss_hit, "failing_before": failing_before,
            "failing_after": [c for c in ORDER if base[c][0] == "fail"], "stop_reason_by_check": stop,
            "checks_final": {nm: {"verdict": base[nm][0], "distance": rd(base[nm][1])} for nm in ALL_NAMES},
            "report_checks_additions": self._additions(base, S),
            "spec_3_0_report_only": self._report_3_0(S)}
        if rec["rows_dropped"] != dropped:
            raise SystemExit("A69 repair: the move log and the selection disagree on the rows dropped")
        return sorted(S), rec

    def _additions(self, base: dict, S) -> dict:
        """The four (f) report.checks entries (A69 f): every (d1) check passes (with the difficulty caps), the chi-square on the pg bins,
        easy <= 25% on the pg bins, the type cap <= 35%. `base` = self.all(S)."""
        return {"a49c_and_caps_pass": all(base[c][0] != "fail" for c in ORDER) and base["difficulty_caps"][0] != "fail",
                "chi2_p_gt_0.01_pg_bins": base["chi2_pg"][0] != "fail",
                "easy_le_25_pg_bins": self._easy_pg_ok(S), "trap_type_cap_le_35": base["trap_type_cap"][0] != "fail"}

    def report_additions(self, S) -> dict:
        """The same four entries for any selection (the record of a family whose repair did not run)."""
        S = frozenset(S)
        return self._additions(self.all(S), S)

    def _easy_pg_ok(self, S) -> bool:
        R = self.rows_of(S)
        return sum(1 for r in R if r["meta"].get("pg_bin") == "easy") <= cs.CAP["easy"] * max(1, len(R)) + 1e-9

    def _report_3_0(self, S) -> dict:
        R = self.rows_of(S)
        n = len(R) or 1
        cards = Counter(mix_c2.card_of(r) for r in R if mix_c2.card_of(r))
        skins = Counter(((r.get("meta") or {}).get("c2") or {}).get("skin_id") for r in R)
        skins.pop(None, None)
        regs = Counter(((r.get("meta") or {}).get("c2") or {}).get("register") for r in R)
        regs.pop(None, None)
        return {"cards": len(cards), "cards_needed_max_20_rows_div_45": max(20, math.ceil(len(R) / 45)),
                "median_rows_per_card": statistics.median(cards.values()) if cards else None,
                "max_skin_rows": max(skins.values(), default=0), "max_register_share": round(max(regs.values()) / n, 4) if regs else None,
                "note": "report only"}


# ================================================================== (c) the swap step with its guard (R13)

def swap_balance_guarded(fam, rows, units, sel, bins, seed, guard=None, max_swaps: int = 600, never_in=frozenset(),
                         unit_class: dict | None = None) -> tuple:
    """a49c.swap_balance with A69 (c)'s new rule: a swap is kept only if guard(old_selection, new_selection) is True (no check that
    passed before it fails after it). When the best partner fails the guard the next-best of the same key (f ascending, then the
    existing seeded order, inside the existing 80-partner window) is tried. guard=None gives exactly a49c.swap_balance's output."""
    import random

    def stat(u):
        rr = [rows[i] for i in units[u]]
        yn = [r for r in rr if r["qtype"] == "noul"]
        return (len(rr), len(yn), sum(int(r["gold"]) for r in yn),
                sum(1 for r in rr if (r.get("meta") or {}).get("twin_kind") == "minimal_edit"))

    def bin_of(u):
        return (bins.get(rows[units[u][0]]["id"]), (unit_class or {}).get(u))
    chosen = list(sel)
    st = {u: stat(u) for u in range(len(units))}
    T = [sum(st[u][j] for u in chosen) for j in range(4)]
    f0 = a49c._viol(*T, fam)
    info = {"violation_before": round(f0, 5), "swaps": 0, "guard_rejections": 0,
            "totals_before": {"rows": T[0], "yes_no": T[1], "yes": T[2], "twins": T[3]}}
    if f0 <= 1e-12:
        return chosen, info | {"note": "inside the bands; no swap"}
    rng = random.Random(f"{seed}|a49c|swap|{fam}")
    inn = set(chosen)
    out_by = defaultdict(list)
    for u in range(len(units)):
        if u not in inn and units[u] and u not in never_in:
            out_by[(bin_of(u), st[u][0])].append(u)
    for v in out_by.values():
        rng.shuffle(v)
    for _ in range(3):
        for u in sorted(chosen, key=lambda u: rng.random()):
            if info["swaps"] >= max_swaps or a49c._viol(*T, fam) <= 1e-12:
                break
            cur = a49c._viol(*T, fam)
            key = (bin_of(u), st[u][0])
            window = out_by.get(key, [])[:80]
            best, bf = None, cur
            scored = []
            for pos, v in enumerate(window):
                T2 = [T[j] - st[u][j] + st[v][j] for j in range(4)]
                f = a49c._viol(*T2, fam)
                if f < cur - 1e-12:
                    scored.append((f, pos, v))
                if f < bf - 1e-12:
                    best, bf = v, f
            pick = best
            if guard is not None and best is not None:
                def ok(v):
                    new = list(chosen)
                    new[new.index(u)] = v
                    return guard(list(chosen), new)
                if not ok(best):
                    info["guard_rejections"] += 1
                    pick = None
                    for _, _, v in sorted(scored):
                        if v == best:
                            continue
                        if ok(v):
                            pick = v
                            break
                        info["guard_rejections"] += 1
            if pick is not None:
                T = [T[j] - st[u][j] + st[pick][j] for j in range(4)]
                chosen[chosen.index(u)] = pick
                out_by[key].remove(pick)
                out_by[key].append(u)
                info["swaps"] += 1
    return chosen, info | {"violation_after": round(a49c._viol(*T, fam), 5),
                           "totals_after": {"rows": T[0], "yes_no": T[1], "yes": T[2], "twins": T[3]}}


# ================================================================== the wired steps (c) and (d) on a trap_select / trap_run result

def stage2(fam, rows, rels, units, res, treated, type_order, weight, pg, pgbins, ntok, target, key, seed, repair: bool = True,
           plugin=None) -> dict:
    """A69 (c) the guarded swap, then (d) the faithful repair, on the result of c2_select.trap_select / trap_run (`res` = the select result
    with the A42-D 6 bins, `treated` = {unit: trap type}, `type_order`, `weight` = the (b4) race weight). Used by c2_select.select_family and
    c2_select.reselect, so a trimmed family is selected the same way. ntok must hold a real token count for every pool row (SystemExit
    otherwise). repair=False runs the swap and leaves the repair out (the record then has no repair block and the mixer refuses it).
    Returns {"family", "order", "pre_repair_sel", "sel" (selection order kept), "swap", "repair" (the (d6) record or None), "additions"}."""
    rank_of = {t: i for i, t in enumerate(type_order)}
    order = c2_select.trap_order(rows, units, key, seed, treated, rank_of, weight)
    bins6 = res["bins"]
    fm = Family(fam, rows, rels, units, bins6, pgbins, {r["id"]: pg[r["id"]] for r in rows}, ntok, order, treated, target=target,
                plugin=plugin)
    sel, swap = swap_balance_guarded(fam, rows, units, res["sel"], bins6, seed, guard=fm.guard,
                                     never_in=set(cs.easy_thinned(rows, units, bins6, key, seed)), unit_class=treated or None)
    if repair:
        kept, rec = fm.repair(sel)
        keep = set(kept)
        final, add = [u for u in sel if u in keep], rec["report_checks_additions"]
    else:
        final, rec, add = list(sel), None, fm.report_additions(sel)
    return {"family": fm, "order": order, "pre_repair_sel": list(sel), "sel": final, "swap": swap, "repair": rec, "additions": add}


def g13_counterfactual(rows_all, rels_all, pg, probs, target, key, seed) -> dict:
    """L3 (A34 e read literally): the first-stage A69 selection (c2_select.trap_select: same seed, key, settings, weighting and type cap)
    run on the pool BEFORE the G13 removal. If it reaches the target exactly, the family was short only because G13 removed units.
    `pg` / `probs` must cover rows_all. Returns counts only."""
    units = cs.units_of(rows_all, rels_all)
    res, _ = c2_select.trap_select(rows_all, units, pg, probs, target, key, seed)
    n = int(res["report"]["rows"])
    return {"pre_g13_pool_rows": len(rows_all), "pre_g13_first_stage_rows": n, "pre_g13_first_stage_at_target": n == target}


A69_TOOL_FILES = (("c2_select.py", C2B / "c2_select.py"), ("a49c.py", C2B / "a49c.py"), ("a69_faithful.py", C2B / "a69_faithful.py"),
                  ("crowd_select_c2.py", C2B / "crowd_select_c2.py"), ("crowd_select.py", c2io.CB / "crowd_select.py"),
                  ("mixer.py", c2io.CB / "mixer.py"))


def tool_shas() -> dict:
    """{tool file: sha256} of the code that makes a program-family select record (A69 f i: mix_c2 compares it with A69_TOOL_SHAS)."""
    return {name: sha256_file(path) for name, path in A69_TOOL_FILES}


# ================================================================== end to end on in-memory pools (no file written)

def run_family(fam, rows, rels, pg, probs, target, ntok, seed: int = SEED, key: str | None = None, plugin=None, drop_ids=None,
               do_swap: bool = True) -> dict:
    """The A69 selection for one program family in memory: G13 drop, trap selection (c2_select.trap_select), guarded swap, faithful repair.
    Returns {"sel", "units", "rows", "family", "pre_repair_sel", "swap", "repair", "treated", "order", ...}. Reads only what the caller passes;
    writes nothing. do_swap=False skips the swap (a diagnostic; select_family always swaps)."""
    key = key or c2_select.sel_key(fam)
    rows, excl = c2_select.drop_excluded(rows, rels, set(drop_ids or ()))
    ids = {r["id"] for r in rows}
    rels = [x for x in rels if x.get("a") in ids and x.get("b") in ids]
    units = cs.units_of(rows, rels)
    res, a42 = c2_select.trap_select(rows, units, pg, probs, target, key, seed)
    treated = a42.pop("_treated")
    pgbins = a42["pg_bin"]
    if do_swap:
        st = stage2(fam, rows, rels, units, res, treated, a42["type_order"], a42["weight"], pg, pgbins, ntok, target, key, seed,
                    repair=True, plugin=plugin)
        fm, order, sel, swap, rep, final = st["family"], st["order"], st["pre_repair_sel"], st["swap"], st["repair"], st["sel"]
    else:
        rank_of = {t: i for i, t in enumerate(a42["type_order"])}
        order = c2_select.trap_order(rows, units, key, seed, treated, rank_of, a42["weight"])
        fm = Family(fam, rows, rels, units, res["bins"], pgbins, {r["id"]: pg[r["id"]] for r in rows}, ntok, order, treated,
                    target=target, plugin=plugin)
        sel, swap = res["sel"], None
        final, rep = fm.repair(sel)
    return {"family": fm, "units": units, "rows": rows, "pre_repair_sel": sorted(sel), "sel": final, "swap": swap, "repair": rep,
            "treated": treated, "order": order, "a42d6": a42, "g13_exclusion": excl,
            "selected_ids": [rows[i]["id"] for u in final for i in units[u]]}


# ================================================================== (f)(i) / (f)(ii) admission

F_CHECKS = ("a49c_and_caps_pass", "chi2_p_gt_0.01_pg_bins", "easy_le_25_pg_bins", "trap_type_cap_le_35")   # the four report.checks entries of A69 (f)


def repair_numbers(s: dict) -> dict | None:
    """{"rows_pre_repair", "rows_dropped"} from a select record: the A78 layout (rec["a69"]["repair"]) or the layout the
    draft a49c.repair_drop_only wrote (rec["report"]["a69"]["repair"], rows_pre_repair = totals_before.rows). None = no repair
    block (or 'not run')."""
    for rp in ((s.get("a69") or {}).get("repair"), ((s.get("report") or {}).get("a69") or {}).get("repair")):
        if isinstance(rp, dict):
            pre = rp.get("rows_pre_repair", (rp.get("totals_before") or {}).get("rows"))
            if pre is not None and "rows_dropped" in rp:
                return {"rows_pre_repair": int(pre), "rows_dropped": int(rp["rows_dropped"])}
    return None


def a34e_flag(s: dict) -> bool | None:
    """L3: the record's literal A34 (e) flag (a69.a34e.short_only_because_g13): True / False, or None when the record does not carry it."""
    a = ((s.get("a69") or {}).get("a34e") or {}) if isinstance(s.get("a69"), dict) else {}
    v = a.get("short_only_because_g13")
    return v if isinstance(v, bool) else None


def short_record_decision(checks: dict, n_selected: int, repair: dict | None, target: int, g13_units_removed: int = 0,
                          at_most: bool = False, short_only_g13: bool | None = None) -> tuple:
    """A69 (f)(ii) (and A34 e), one path for every program record: (accepted, [reasons it was not]). `checks` = report.checks of the record.
    Refused when: an (f) entry is missing (L2); there is no repair block (L1); rows_pre_repair - rows_dropped != rows selected (also when nothing was
    dropped, L1); rows_dropped is above 25% of rows_pre_repair; a check other than total_eq_target failed; or the record is short and neither
    pre == target, nor A34 (e) read literally (G13 removed units AND the shortfall exists only because of that: short_only_g13 is True; L3),
    nor an upper-bound target (at_most) applies."""
    why = []
    miss = [k for k in F_CHECKS if k not in checks]
    if miss:
        why.append(f"report.checks lacks the A69 (f) entries {miss}")
    if not repair or "rows_pre_repair" not in repair or "rows_dropped" not in repair:
        why.append("the record has no repair block (A69 d did not run, or the record is not an A69 record)")
        return False, why
    pre, rd = repair["rows_pre_repair"], repair["rows_dropped"]
    if pre - rd != n_selected:
        why.append(f"rows_pre_repair - rows_dropped = {pre - rd} != rows selected {n_selected}")
    if LOSS_DEN * rd > pre:
        why.append(f"rows_dropped {rd} is {100 * rd / max(1, pre):.1f}% of rows_pre_repair {pre} (limit 25%)")
    bad = [k for k, v in checks.items() if v is not True]
    if bad and bad != ["total_eq_target"]:
        why.append(f"total_eq_target must be the ONLY failed check, failed: {bad}")
    elif bad:
        a34e = g13_units_removed > 0 and short_only_g13 is True
        if not (pre == target or a34e or at_most):
            why.append(f"pre-repair selection {pre} is short of target {target}; A34 (e) read literally needs G13-removed units AND the "
                       f"shortfall only because of them (units removed {g13_units_removed}, literal flag {short_only_g13}), and no upper-bound target applies")
    return not why, why


def program_record_problem(s: dict | None, pinned: dict | None) -> str | None:
    """A69 (f)(i): None = the record may be considered. Refused: not a dict, a scratch record, no a42d6 / a69 block or no pg_bin map, an empty
    pin, or tool shas other than the pinned A69_TOOL_SHAS (exact equality of the dict)."""
    if not isinstance(s, dict):
        return "no select record"
    if s.get("scratch") is True:
        return "a scratch selection record (A69 f i)"
    miss = [k for k in ("a42d6", "a69") if not isinstance(s.get(k), dict)]
    if not isinstance(s.get("pg_bin"), dict) or not s.get("pg_bin"):
        miss.append("pg_bin")
    if miss:
        return f"the select record lacks {miss} (A69 f i): re-select with the A69 code"
    if not pinned:
        return "A69_TOOL_SHAS is empty: the A69 tool shas are not pinned (A69 f i)"
    ts = s.get("tool_sha256")
    if not isinstance(ts, dict) or dict(ts) != dict(pinned):
        diff = sorted(k for k in set(pinned) | set(ts or {}) if (ts or {}).get(k) != pinned.get(k)) if isinstance(ts, dict) else ["tool_sha256"]
        return f"the record was made by other tools than the pinned A69_TOOL_SHAS (differs: {diff}; A69 f i)"
    return None


def selection_problem_faithful(s: dict | None, cand_sha: str, target: int, at_most: bool = False) -> str | None:
    """mix_c2.selection_problem for a program record with (f)(ii) (not (f)(i): see program_selection_problem): None = the record may be mixed."""
    if s is None:
        return "no C2 crowd selection file (G9 not run)"
    if s.get("candidates_sha256") != cand_sha:
        return "the crowd selection was made on another candidates file (re-run the crowd)"
    if s.get("target") != target:
        return f"crowd selection target {s.get('target')} != spec target {target}"
    rep = s.get("report") or {}
    checks = rep.get("checks") or {}
    if s.get("scratch") is True:
        return "a scratch selection record (A69 f i)"
    ok, why = short_record_decision(checks, len(s.get("selected_ids") or []), repair_numbers(s), target,
                                    mix_c2.units_removed(s.get("exclude_ids")), at_most, a34e_flag(s))
    if ok and (not [k for k, v in checks.items() if v is not True]) and rep.get("pass") is not True:
        return "crowd selection fails its checks (G9 / spec 2.1): ['pass is not true']"
    if not ok:
        return f"crowd selection fails its checks (G9 / spec 2.1, A69 f ii): {why}"
    return None


def program_selection_problem(s: dict | None, cand_sha: str, target: int, pinned: dict | None, at_most: bool = False) -> str | None:
    """A69 (f) for a program-family record: the plain refusals (no record, other candidates, other target), then (f)(i), then (f)(ii).
    None = the record may be mixed."""
    if s is None:
        return "no C2 crowd selection file (G9 not run)"
    if s.get("candidates_sha256") != cand_sha:
        return "the crowd selection was made on another candidates file (re-run the crowd)"
    if s.get("target") != target:
        return f"crowd selection target {s.get('target')} != spec target {target}"
    why = program_record_problem(s, pinned)
    if why:
        return why
    return selection_problem_faithful(s, cand_sha, target, at_most)


def accept_table(select_dir: Path | None = None) -> list:
    """Counts only, read-only: for each crowd_c2/select_T*.json, (f)(ii)'s arithmetic on the numbers it records."""
    d = Path(select_dir) if select_dir else C2B / "crowd_c2"
    out = []
    for f in sorted(d.glob("select_T*.json")):
        s = json.loads(f.read_text())
        rp = repair_numbers(s)
        checks = (s.get("report") or {}).get("checks") or {}
        ok, why = short_record_decision(checks, len(s.get("selected_ids") or []), rp, s.get("target"),
                                        mix_c2.units_removed(s.get("exclude_ids")), False, a34e_flag(s))
        out.append({"family": s.get("family"), "target": s.get("target"), "selected": len(s.get("selected_ids") or []),
                    "rows_pre_repair": (rp or {}).get("rows_pre_repair"), "rows_dropped": (rp or {}).get("rows_dropped"),
                    "pct_dropped": None if not rp or not rp["rows_pre_repair"] else round(100 * rp["rows_dropped"] / rp["rows_pre_repair"], 1),
                    "accepted_f_ii": ok, "why_not": why})
    return out


if __name__ == "__main__":
    if sys.argv[1:] == ["accept-table"]:
        for row in accept_table():
            print(json.dumps(row))
    else:
        print("usage: a69_faithful.py accept-table   (read-only; counts only)")
