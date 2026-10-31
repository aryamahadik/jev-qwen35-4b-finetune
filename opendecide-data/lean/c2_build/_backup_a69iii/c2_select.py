"""C2 G9 crowd difficulty + stratified selection (C2_DATA_SPEC 2.1, 3.0, 3.19, 6.3 G9, 6.4 step 9; PREREG A37 e).
CPU only: no Modal, gcloud, GPU or paid call; no git.

Crowd (A37 e: "The crowd becomes C1-only. Bins and selection are unchanged."). One model, C1 = q35_4b_main500k
(adapter 507d1c29...), read once on every candidate row with the A18.2 readout (one view, given option order, no TTA)
on SGLang S1 or the free L4. Crowd p_g = C1's probability on the gold answer (yes/no: P(yes) when gold = 1, else
P(no); choice: P(gold option)). Every candidate row must carry a C1 label (else SystemExit: the read is incomplete),
and the label set must be one view of C1 (shard_golden.one_view; the view's model name must be C1's).

Imported unchanged from c_build/crowd_select.py (never edited): relation units (units_of), the bins (easy p_g > 0.97;
medium 0.30 < p_g <= 0.97; hard p_g <= 0.30), the stratified whole-unit selection (select: a seeded 30% keep of all-easy
units, bin budgets easy <= 25% / hard <= 30% / medium the rest, label-balanced quotas per stratum, A27 c reflow when a
bin's balanced pool is short), the label x bin chi-square (chi2_p, p > 0.01) and the G5 re-read list (g5_reread: every
row with p_g < 0.05 plus a seeded 300 of the selected rows). Seed: A37 (i) 20261013, selection key = the family id
(carry-over pools: '<F>|c2carry'); the mixer's budget trim re-selects with the same seed and key.

Targets (spec 2.1, rows after the crowd step; builders generate about 1.5x): T28 2,400, T35 600, T33 2,400,
T29 2,000, T30 1,400, T27 1,600, T26 1,400, T31 1,000, T32 800, T01 1,600, T23 800, T24 600, T06 900, T15 900,
T12 800, T07 800, T25 600; T37b 2,000. Carry-over pools (spec 3.19): F5 1,500 (complement and equiv units only),
F6 <= 1,000, F11 <= 1,000 (XED / MAMS real-text codebook rows first), F4 <= 500, each drawn from its round-1 SELECTED
rows with C1-only p_g from the round-1 C1 crowd labels (data/c_crowd_r1_shards/<F>/labels_q35_4b_main500k).
A G13 drop list (--exclude-ids, key drop_ids) removes whole units before selection (the A34 b rule).

PREREG Ruling A69 (DRAFT 17 Oct 2026; program fix, nothing loosened): for the 15 program families (TRAP_FAMS) the selection applies
A42-D 6 trap weighting (trap_select: units C1 puts >= 0.25 probability on a tagged trap option go to the hard bin at weight 2 in
the seeded order, trap types favoured by C1 pick rate, no type above 35% of the treated units), through
crowd_select_c2.select (c_build/crowd_select.select copied verbatim with the bins and the unit order injected), and, with
the drop-only repair step (a49c.repair_drop_only: whole units removed, seeded, no cap raised, the target may be missed), ON by
default for a TRAP_FAMS family (select_family repair=None; CLI --no-a69-repair turns it off, --a69-repair is accepted and is the default). Carry pools, blocks, DI blocks and T40-T46 are selected exactly as before.

  ../.venv/bin/python c2_build/c2_select.py tasks [--fam T28 ...] [--write-shards]   the C1-only read plan (+ shards)
  ../.venv/bin/python c2_build/c2_select.py select [--fam T28 ...] [--exclude-ids logs/decontam_counts/x.json ...]
  ../.venv/bin/python c2_build/c2_select.py carry [--fam F5 F6 F11 F4] [--exclude-ids ...]
--exclude-ids (select and carry): a file is a C2 G13 log when its "tool" is c2_build/g13_c2.py (any spelling of the path),
it is named c2_*.json, or it carries a g13_c2 record (inputs_at_start, inputs_at_start_paths or engine, or a set name
c2_*): the same scope as mix_c2. A G13 log is used only when g13_log_problems finds nothing (the check mix_c2 runs:
complete true, incomplete_why empty, inputs_at_start present for a non-seed run, and not stale: the candidates / training
file and every C2 dev file are the ones the run hashed; a dev file that exists now but is not in the log makes it stale);
any problem refuses the whole run (SystemExit, nothing written). EVERY other file keeps the gate it always had: "complete"
must be true (and incomplete_why empty), so a partial round-1 log such as logs/decontam_counts/F6.json is refused, and so
are the plain drop lists that carry no completeness key (replay_screen/REPLAY_DENY_A46.json, REPLAY_UNSCREENED_A46.json,
logs/decontam_counts/pool_drops_r1.json): no file, by path or by name, is exempt. Those lists go to mix_c2
--decontam-drops, which reads every non-G13 list as before. A path is refused when the never-open rule refuses it OR where
its links lead (resolved_refusal): a link with a harmless name into a refused folder is not followed.
Outputs (c2_build/crowd_c2/): select_<FAM>.json, g5_reread_<FAM>.json, crowd_tasks_c2.json; shards under
data/c2_crowd_shards/<FAM>/. Every write needs the OHS-4 freeze (PREREG A38) first (A37 f); before it the tools refuse.
"""
from __future__ import annotations

import argparse
import math
import os
import re
import sys
from collections import Counter
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import c2io  # noqa: E402
from c2io import C1, CARRY, SEED, C2InputLog
from c2io import ALL_TARGETS as TARGETS  # A47 registry: + T40-T45, GB, MD, RTW  # noqa: E402

import a49c  # noqa: E402  (A49 c balance report + yes-rate swaps)
import crowd_select as cs  # noqa: E402  (c_build: imported, never edited)
import crowd_select_c2 as cs2  # noqa: E402  (A69 b5: crowd_select.select + two injected inputs)
from mixio import h64  # noqa: E402
from mixio import log_line, sha256_file  # noqa: E402

OUT = c2io.HERE / "crowd_c2"
SHARDS = c2io.DATA / "c2_crowd_shards"
R1_SHARDS = c2io.DATA / "c_crowd_r1_shards"          # carry-over pools: the round-1 crowd shards and C1 labels
R1_SELECT = c2io.CB / "crowd_r1"                     # carry-over pools: round-1 select_<F>.json (selected ids)
LOG = c2io.HERE / "progress_c2.log"
G13_TOOL = "c2_build/g13_c2.py"                      # the "tool" key of a C2 G13 log (g13_c2._record)
SHARD_ROWS = 5000
READ_ROWS_PER_H = 124000                             # spec 9.2: SGLang S1 about 124K rows/h (C1-only, one view)
CARRY_REL_ONLY = {"F5": {"complement", "equiv"}}     # spec 3.19: F5 complement and equiv units only
CARRY_PREFER = {"F11": ("xed_en", "mams")}           # spec 3.19: prefer F11's XED / MAMS real-text codebook rows
CROWD_RULE = ("A37 (e): C1-only crowd (q35_4b_main500k, A18.2 readout, one view); bins and selection unchanged "
              "(c_build/crowd_select.py)")


def log(msg):
    try:
        c2io.require_a38()
        log_line(LOG, "c2_select: " + msg)
    except Exception:  # noqa: BLE001 - before A38 nothing is written (A37 f)
        pass
    print(msg, flush=True)


def sel_key(fam: str) -> str:
    """The selection key (crowd_select's seeded orders and easy keep): the family id; carry-over: '<F>|c2carry'."""
    return f"{fam}|c2carry" if fam in CARRY else fam


# ------------------------------------------------------------------ the never-open rule, links included

def resolved_refusal(path) -> str | None:
    """Why `path` may not be listed, stat-ed, hashed or opened (None = allowed): c2io.refusal on the path as given, then on
    where its links lead. c2io.refusal is string logic (plus round-1's list), so a link with a harmless name that points
    into a refused folder (data/c2_parts/<name> -> .../ohs4_x) passes it. The path is also resolved here (links are followed
    with lstat / readlink and pathlib's one stat of the real path, as mixio.refusal always did: nothing is opened, listed or
    read) and the rule is applied to the real path. A path that cannot be resolved (a link loop, an unreadable folder) is
    refused."""
    try:
        why = c2io.refusal(path)                                   # (mixio.refusal inside resolves the path: a loop raises)
        if why:
            return why
        return c2io.refusal(Path(path).resolve())
    except (OSError, RuntimeError) as e:                           # a link loop, an unreadable folder: where it leads is unknown
        return f"path cannot be resolved ({type(e).__name__}), so where its links lead is unknown: refused"


def guard(ilog, path) -> Path:
    """resolved_refusal(path), then ilog.check(path) (the log's own rule): C2Refused before the path is stat-ed, hashed,
    opened or logged. The log classes of the tools (LinkGuardedInputLog) do both in check(); this holds for a plain
    C2InputLog too."""
    why = resolved_refusal(path)
    if why:
        raise c2io.C2Refused(f"input refused: {path}: {why}")
    ilog.check(path)
    return Path(path)


class LinkGuardedInputLog(C2InputLog):
    """C2InputLog whose check() also refuses a path whose links lead to a refused one (resolved_refusal). The tools'
    input logs: every file they read or log (drop lists, candidates, crowd labels, dev files) goes through check()."""

    def check(self, path) -> Path:
        why = resolved_refusal(path)
        if why:
            raise c2io.C2Refused(f"input refused: {path}: {why}")
        return super().check(path)


# ------------------------------------------------------------------ the C1-only crowd (A37 e)

def view_problem(view: dict | None, c1: str = C1) -> str | None:
    """A crowd label set must be ONE view of C1 (shard_golden.one_view already refuses mixed views). Its model name
    may be C1's adapter name or its merged S1 checkpoint ('<C1>_merged'); a TTA view is refused (A18.2: one view)."""
    if not view or not isinstance(view.get("settings"), dict):
        return "label view without settings (cannot tell which model read it)"
    s = view["settings"]
    if s.get("name") not in (c1, f"{c1}_merged"):
        return f"labels were read by {s.get('name')!r}, not C1 ({c1}): the C2 crowd is C1-only (A37 e)"
    if s.get("tta") or s.get("tta_choice") or s.get("tta_noul") or s.get("perm_seed") is not None:
        return "labels are a TTA / permuted view; the crowd read is one view in given option order (A18.2)"
    return None


def c1_pg(rows: list[dict], probs: dict) -> dict:
    """{row id: C1's probability on the gold answer}. Every row must be labelled (else SystemExit)."""
    miss = [r["id"] for r in rows if r["id"] not in probs]
    if miss:
        raise SystemExit(f"C1 crowd read incomplete: {len(miss)} rows without a C1 label, e.g. {miss[:3]}")
    return {r["id"]: cs.p_gold(r, probs[r["id"]]) for r in rows}


def load_c1(ilog: C2InputLog, rows, labels_dir: Path, shards_dir: Path | None, c1: str = C1) -> tuple[dict, dict]:
    """(p_g by id, label view) from a shard_golden label directory (every shard done) or a preds .jsonl."""
    pg, view, _ = load_c1_full(ilog, rows, labels_dir, shards_dir, c1)
    return pg, view


def load_c1_full(ilog: C2InputLog, rows, labels_dir: Path, shards_dir: Path | None, c1: str = C1) -> tuple[dict, dict, dict]:
    """(p_g by id, label view, the label set {row id: {option: probability}}). The label set is the one p_g comes from; A69 reads
    the same one for the trap flag (A49 f: a C1 read used as a selection signal, never as a label or a target)."""
    sys.path.insert(0, str(c2io.LEAN))
    import shard_golden as sg
    p = Path(labels_dir)
    for f in ([p] if p.is_file() else sorted(p.glob("shard_*.jsonl")) + sorted(p.glob("shard_*.meta.json"))):
        ilog.record(f)
    probs, view = sg.load_labels(p, shards_dir, return_view=True) if not p.is_file() else \
        sg.load_labels(p, return_view=True)
    why = view_problem(view, c1) if not p.is_file() else None
    if why:
        raise SystemExit(f"crowd labels refused: {why}")
    return c1_pg(rows, probs), view, probs


# ------------------------------------------------------------------ selection (crowd_select, unchanged)

def drop_excluded(rows, rels, drop_ids: set) -> tuple[list, dict]:
    """A34 (b): every unit holding a G13-dropped id leaves the pool before selection."""
    if not drop_ids:
        return rows, {"units_removed": 0, "rows_removed": 0, "pool_rows_after": len(rows)}
    units = cs.units_of(rows, rels)
    bad = {i for u in units if any(rows[i]["id"] in drop_ids for i in u) for i in u}
    n_u = sum(1 for u in units if bad.intersection(u))
    keep = [r for i, r in enumerate(rows) if i not in bad]
    return keep, {"units_removed": n_u, "rows_removed": len(bad), "pool_rows_after": len(keep)}


# ------------------------------------------------------------------ PREREG Ruling A69 (DRAFT): A42-D 6 trap weighting

TRAP_FAMS = ("T01", "T06", "T07", "T12", "T15", "T23", "T24", "T25", "T26", "T28", "T29", "T30", "T31", "T32", "T33")
TRAP_P = 0.25                                         # A42-D 6.2: C1 probability on a tagged trap option
TRAP_W = 2.0                                          # A42-D 6.3: selection weight against other hard-bin units
TRAP_CAP = 0.35                                       # A42-D 6.4: no trap type above 35% of the treated units
HARD_CAP = 0.30                                       # spec 5.2
_TWO64 = 2 ** 64


def row_trap_tags(r) -> dict:
    """{option text: sorted tag tuple} of the tagged WRONG options a choice row shows (meta.opt_err: option text -> error-model tags;
    an option with an empty tag list, one that is not shown, and the gold option, which is never tagged, are left out)."""
    oe = (r.get("meta") or {}).get("opt_err")
    if r.get("qtype") != "choice" or not isinstance(oe, dict):
        return {}
    opts = r.get("options") or []
    return {o: tuple(sorted(map(str, t))) for o, t in oe.items()
            if o in opts and o != r.get("gold") and isinstance(t, (list, tuple)) and t}


def trap_pick_rates(rows, probs) -> tuple[dict, list]:
    """A69 (b2): per tag, pick rate = (rows whose C1 argmax option carries the tag) / (rows that show an option carrying it), on
    the pool given (the post-G13 pool). Order: rate descending, rows shown descending, tag name. Returns ({tag: [picked, shown,
    rate]}, ordered tag list). The argmax is the first option with the largest C1 probability."""
    shown, picked = Counter(), Counter()
    for r in rows:
        tg = row_trap_tags(r)
        if not tg:
            continue
        p = probs[r["id"]]
        pick = max(r["options"], key=lambda o: p.get(o, 0.0))
        shown.update({t for ts in tg.values() for t in ts})
        picked.update(set(tg.get(pick, ())))
    rate = {t: picked[t] / shown[t] for t in shown}
    order = sorted(shown, key=lambda t: (-rate[t], -shown[t], t))
    return {t: [picked[t], shown[t], round(rate[t], 6)] for t in order}, order


def trap_flags(rows, units, probs, rank_of: dict) -> tuple[dict, Counter]:
    """A69 (b1, b2): ({unit index: trap type}, per-tag unit counts). A unit is flagged when any choice row in it has a tagged
    option on which C1's probability is >= 0.25; its type is the highest-ranked tag among those options (one type per unit).
    The per-tag count counts a unit once per tag it names (reported only)."""
    flagged, per_tag = {}, Counter()
    for u, idx in enumerate(units):
        hit = set()
        for i in idx:
            r = rows[i]
            tg = row_trap_tags(r)
            if tg:
                p = probs[r["id"]]
                for o, ts in tg.items():
                    if p.get(o, 0.0) >= TRAP_P:
                        hit.update(ts)
        if hit:
            flagged[u] = min(hit, key=lambda t: rank_of[t])
            per_tag.update(hit)
    return flagged, per_tag


def trap_order(rows, units, key: str, seed, treated: dict, rank_of: dict, w: float) -> list:
    """A69 (b4): the seeded unit order of crowd_select.select with the trap weight. t = -ln(1 - U) / w, U = (h + 0.5) / 2^64 (an
    exponential race; w = 2 for a treated unit, 1 for any other), h = h64(seed, key, "order", first row id). The untreated
    units keep their exact h order (the merge never reorders them); a treated unit comes before an untreated one with odds
    w : 1. The positions the treated units hold are then refilled with them sorted by (type rank, own t). With nothing
    treated this is exactly crowd_select's order."""
    n = len(units)
    h = [h64(seed, key, "order", rows[units[u][0]]["id"]) for u in range(n)]
    base = sorted(range(n), key=lambda u: h[u])
    if not treated:
        return base

    def t(u, wt):
        return -math.log((2 * (_TWO64 - h[u]) - 1) / (2 * _TWO64)) / wt
    un = [u for u in base if u not in treated]
    tr = sorted(treated, key=lambda u: (t(u, w), h[u]))
    out, i, j = [], 0, 0
    while i < len(un) or j < len(tr):
        if j < len(tr) and (i >= len(un) or t(tr[j], w) < t(un[i], 1.0)):
            out.append(tr[j])
            j += 1
        else:
            out.append(un[i])
            i += 1
    slots = [k for k, u in enumerate(out) if u in treated]
    for k, u in zip(slots, sorted(treated, key=lambda u: (rank_of[treated[u]], t(u, w), h[u]))):
        out[k] = u
    return out


def trap_run(rows, units, pg: dict, target: int, key: str, seed, pg_bins: dict, flagged: dict, rank_of: dict) -> tuple[dict, dict, float, list, list]:
    """A69 (b3-b7): the treated map starts as `flagged` ({unit index: type}); crowd_select.select (cs2.select) runs on the A42-D 6
    bins (treated units hard, the rest `pg_bins`) and the weighted, type-favouring order; the type cap (b6) shrinks the treated
    set until no type holds more than 35% of the selected treated units; the hard-share assert (b7) steps the weight down by 0.1
    (to 1.0) if hard rows exceed 30% of the realised rows. Returns (select result, final treated map, weight, weight steps, cap steps).
    Shared by the first selection (trap_select) and the mixer's trim (reselect), so a trimmed family is selected the same way."""
    w, w_steps = TRAP_W, []
    while True:
        treated, cap_steps = dict(flagged), []
        while True:
            order = trap_order(rows, units, key, seed, treated, rank_of, w)
            bins = dict(pg_bins)
            for u in treated:
                for i in units[u]:
                    bins[rows[i]["id"]] = "hard"
            res = cs2.select(rows, units, pg, target, key=key, seed=seed, bins_in=bins, order_in=order)
            pos = {u: k for k, u in enumerate(order)}
            st = [u for u in res["sel"] if u in treated]
            cnt = Counter(treated[u] for u in st)
            over = [(c, t) for t, c in cnt.items() if c > TRAP_CAP * len(st) + 1e-9]
            if not over:
                break
            c, t = max(over, key=lambda x: (x[0], -rank_of[x[1]]))
            m = max(1, math.ceil((c - TRAP_CAP * len(st)) / (1 - TRAP_CAP) - 1e-9))
            lose = sorted((u for u in st if treated[u] == t), key=lambda u: -pos[u])[:m]
            for u in lose:
                del treated[u]
            cap_steps.append({"type": t, "units_of_type": c, "treated_selected": len(st), "treatment_removed_from": len(lose)})
        hard = res["report"]["bins"].get("hard", 0)
        total = max(1, res["report"]["rows"])
        if hard <= HARD_CAP * total + 1e-9 or w <= 1.0 + 1e-9:
            break
        w_steps.append({"weight": w, "hard_rows": hard, "rows": total})
        w = max(1.0, round(w - 0.1, 10))
    return res, treated, w, w_steps, cap_steps


def trap_select(rows, units, pg: dict, probs: dict, target: int, key: str, seed) -> tuple[dict, dict]:
    """A69 (b): crowd_select.select on the A42-D 6 bins and the weighted, type-favouring order (cs2.select, the verbatim copy with
    those two inputs injected), then the type cap (b6) and the hard-share assert (b7). Returns (select result, a69 record
    with the final treated map under "_treated"). The result's bins are the A42-D 6 bins; the p_g bins are in the record."""
    pg_bins = {r["id"]: cs.bin_of(pg.get(r["id"])) for r in rows}
    rates, rank = trap_pick_rates(rows, probs)
    rank_of = {t: i for i, t in enumerate(rank)}
    flagged, per_tag = trap_flags(rows, units, probs, rank_of)
    res, treated, w, w_steps, cap_steps = trap_run(rows, units, pg, target, key, seed, pg_bins, flagged, rank_of)
    hard = res["report"]["bins"].get("hard", 0)
    total = max(1, res["report"]["rows"])
    sel_flagged = Counter(flagged[u] for u in res["sel"] if u in flagged)
    rec = {"rule": "PREREG Ruling A69 (DRAFT): A42-D 6 trap weighting (6.2 flag, 6.3 hard bin at weight, 6.4 type order and 35% cap)",
           "seed": seed, "key": key, "trap_prob": TRAP_P, "weight": w, "weight_start": TRAP_W, "scaled": w != TRAP_W,
           "weight_steps": w_steps, "pick_rates_post_g13": rates, "type_order": rank,
           "dev_pick_rates": "reported by the orchestrator, not used (A69 b2)",
           "flagged_units": len(flagged), "flagged_rows": sum(len(units[u]) for u in flagged),
           "flagged_units_by_type": dict(Counter(flagged.values())), "flagged_units_per_tag": dict(sorted(per_tag.items())),
           "treated_units_final": len(treated), "treated_rows_final": sum(len(units[u]) for u in treated),
           "treated_selected_units": sum(1 for u in res["sel"] if u in treated),
           "treated_selected_rows": sum(len(units[u]) for u in res["sel"] if u in treated),
           "treated_selected_by_type": dict(Counter(treated[u] for u in res["sel"] if u in treated)),
           "flagged_selected_by_type_reported_only": dict(sel_flagged), "type_cap_steps": cap_steps,
           "hard_rows": hard, "hard_share": round(hard / total, 4), "hard_assert_ok": hard <= HARD_CAP * total + 1e-9,
           "pool_units": len(units), "pool_rows": len(rows), "pg_bin": pg_bins, "_treated": treated}
    return res, rec


def trap_carry(rows, units, treated: dict, rank: list) -> dict:
    """What a selection record carries so the mixer's trim can re-run A69 on the selected rows: {"trap": {row id: type} for every row
    of a treated unit, "trap_rank": the type order}. Stored inside the record's parts (c2_select.reselect reads it back)."""
    return {"trap": {rows[i]["id"]: t for u, t in sorted(treated.items()) for i in units[u]}, "trap_rank": list(rank)}


def select_family(fam: str, rows, rels, pg: dict, target: int, seed: int = SEED, drop_ids: set | None = None,
                  key: str | None = None, probs: dict | None = None, repair: bool | None = None, ntok: dict | None = None) -> dict:
    """One family's C2 selection: candidate checks, G13 exclusion, crowd_select.select (bins, budgets, balanced quotas,
    reflow, chi-square) and the G5 re-read list. Returns the select record (no file written). probs (C1 option probabilities,
    the label set p_g comes from) switches on A69 trap weighting for a TRAP_FAMS family and, with it, the A69 drop-only repair
    (repair=None means ON whenever A69 is on; repair=False turns it off; needs ntok for the token-mean bar, else that bar is not
    repaired and the record says has_ntok false). Without probs the selection is exactly what it was before A69."""
    probs_chk = c2io.candidate_problems(fam, rows)
    if probs_chk:
        raise SystemExit("candidates refused: " + "; ".join(probs_chk))
    rows, excl = drop_excluded(rows, rels, set(drop_ids or ()))
    ids = {r["id"] for r in rows}
    rels = [x for x in rels if x.get("a") in ids and x.get("b") in ids]
    units = cs.units_of(rows, rels)
    k = key or sel_key(fam)
    a69, treated = None, {}
    if probs is not None and fam in TRAP_FAMS and pg:
        miss = [r["id"] for r in rows if r["qtype"] == "choice" and r["id"] not in probs]
        if miss:
            raise SystemExit(f"A69: {len(miss)} choice rows without C1 option probabilities, e.g. {miss[:3]}")
        res, a69 = trap_select(rows, units, pg, probs, target, k, seed)
        treated = a69.pop("_treated")
    else:
        res = cs.select(rows, units, pg, target, key=k, seed=seed)
    swap, rep_info = None, None
    if fam not in c2io.BLOCK_TARGETS and fam not in CARRY and pg:      # A49 c: bring the yes rate, yes/no share and twin share inside their bands by whole-unit swaps (same bin, same size)
        sel2, swap = a49c.swap_balance(fam, rows, units, res["sel"], res["bins"], seed,
                                       never_in=set(cs.easy_thinned(rows, units, res["bins"], k, seed)), unit_class=treated or None)
        if swap.get("swaps"):
            res["sel"] = sel2
    if repair is None:
        repair = a69 is not None
    if repair and a69 is not None and fam in TRAP_FAMS and pg:
        sel3, rep_info = a49c.repair_drop_only(fam, rows, rels, units, res["sel"], res["bins"], ntok, seed, unit_type=treated,
                                               type_cap=TRAP_CAP)
        res["sel"] = sel3
    if (swap and swap.get("swaps")) or (rep_info and rep_info["units_dropped"]):
        res["report"] = cs.selection_report(rows, units, sorted(res["sel"]), res["bins"], target, True, {r["id"]: pg[r["id"]] for r in rows})
    g5 = cs.g5_reread(rows, units, res["sel"], pg, fam)
    chosen = [rows[i]["id"] for u in res["sel"] for i in units[u]]
    rep = res["report"]
    rep["crowd_rule"] = CROWD_RULE
    rep["unit_sizes"] = dict(sorted(Counter(len(units[u]) for u in res["sel"]).items()))
    chosen_set = set(chosen)
    srows = [r for r in rows if r["id"] in chosen_set]
    sck = a49c.family_checks(fam, srows, [x for x in rels if x["a"] in chosen_set and x["b"] in chosen_set], ntok)
    rep["a49c"] = {"failing": a49c.failing(sck), "balance_swap": swap, "checks": sck, "card_max": a49c.card_max(srows),
                   "note": "A49 c is asserted on the mixed rows (mix_c2.a49c_assert); here it is reported, with whole-unit "
                           "swaps for the yes rate, yes/no share and twin share; what selection cannot fix is listed in 'failing'"}
    if a69 is not None:
        a69["treated_selected_units"] = sum(1 for u in res["sel"] if u in treated)
        a69["treated_selected_by_type"] = dict(Counter(treated[u] for u in res["sel"] if u in treated))
        a69["repair"] = rep_info if rep_info is not None else "not run (repair=False)"
        hard_f, total_f = rep["bins"].get("hard", 0), max(1, rep["rows"])      # the REALISED hard share, after the swaps and the repair
        a69["hard_rows_at_trap_select"], a69["hard_share_at_trap_select"] = a69["hard_rows"], a69["hard_share"]
        a69["hard_rows"], a69["hard_share"] = hard_f, round(hard_f / total_f, 4)
        a69["hard_assert_ok"] = hard_f <= HARD_CAP * total_f + 1e-9
        rep["a69"] = a69
    rec = {"family": fam, "target": target, "seed": seed, "key": k, "crowd": {"c1": C1}, "crowd_rule": CROWD_RULE,
           "report": rep, "budget": res["budget"], "easy_dropped_units": res["easy_dropped_units"],
           "reflow": res.get("reflow", []), "selected_ids": chosen, "parts": [{"key": k, "ids": chosen}],
           "exclude_ids": excl, "crowd_pg": {r["id"]: round(pg[r["id"]], 4) for r in rows},
           "difficulty_bin": {r["id"]: res["bins"][r["id"]] for r in rows}, "g5": g5}
    if a69 is not None:
        rec["pg_bin"] = a69.pop("pg_bin")
        rec["a69"] = a69
        rec["parts"][0] |= trap_carry(rows, units, treated, a69["type_order"])     # the trim (reselect) re-runs A69 from this
    return rec


def reselect(rows, rels, pg: dict, parts: list[dict], target: int, seed: int = SEED) -> dict:
    """A smaller selection of already-selected rows (the mixer's budget trim and agent-tier cap, spec 5.2 / 5.5):
    crowd_select.select again on each part's rows with the SAME seed and key, so no unit that passed the seeded 30%
    easy keep is thinned twice, at a target split over the parts by largest remainder. Bins, budgets, balanced quotas
    and whole units hold exactly as in the first selection. A part that carries A69 trap data ("trap": {row id: type}, written by
    select_family for a TRAP_FAMS family) is re-selected the A69 way: its treated units stay hard-binned at weight 2 in the type
    order, the 35% type cap and the hard-share assert are run again on the trimmed rows (trap_run), so the A42-D 6 bin in
    meta.difficulty_bin and the spec 3.0 / 5.2 hard cap hold after a trim. Returns {"selected_ids", "parts", "reports", "a69", "bins" (the A42-D 6 bin of each kept row of an A69 part)}."""
    from mixer import largest_remainder
    have = {r["id"] for r in rows}
    sizes = {i: sum(1 for x in p["ids"] if x in have) for i, p in enumerate(parts)}
    want = largest_remainder(sizes, min(target, sum(sizes.values())))
    out, new_parts, reps, a69s, nbins = [], [], [], [], {}
    for i, p in enumerate(parts):
        ids = set(p["ids"]) & have
        sub = [r for r in rows if r["id"] in ids]
        srel = [x for x in rels if x.get("a") in ids and x.get("b") in ids]
        units = cs.units_of(sub, srel)
        ppg = {r["id"]: pg[r["id"]] for r in sub}
        trap = p.get("trap")
        if trap and sub:
            rank = list(p.get("trap_rank") or [])
            rank_of = {t: k for k, t in enumerate(rank)}
            flagged = {}
            for u, idx in enumerate(units):
                tt = next((trap[sub[j]["id"]] for j in idx if sub[j]["id"] in trap), None)
                if tt is not None:
                    flagged[u] = tt
            pg_bins = {r["id"]: cs.bin_of(ppg.get(r["id"])) for r in sub}
            res, treated, w, w_steps, cap_steps = trap_run(sub, units, ppg, want[i], p["key"], seed, pg_bins, flagged, rank_of)
            hard = res["report"]["bins"].get("hard", 0)
            a69s.append({"key": p["key"], "weight": w, "weight_steps": w_steps, "type_cap_steps": cap_steps,
                         "treated_in": len(flagged), "treated_selected": sum(1 for u in res["sel"] if u in treated),
                         "hard_rows": hard, "rows": res["report"]["rows"]})
            keep_trap = dict(trap)                           # the whole map rides on: a unit refilled into this part later is still treated
            drop = {sub[j]["id"] for u in flagged if u not in treated for j in units[u]}
            extra = {"trap": {k: v for k, v in keep_trap.items() if k not in drop}, "trap_rank": rank}
            nbins |= {sub[j]["id"]: res["bins"][sub[j]["id"]] for u in res["sel"] for j in units[u]}
        else:
            res = cs.select(sub, units, ppg, want[i], key=p["key"], seed=seed)
            extra = {}
        got = [sub[j]["id"] for u in res["sel"] for j in units[u]]
        out += got
        new_parts.append({"key": p["key"], "ids": got} | extra)
        reps.append(res["report"])
    return {"selected_ids": out, "parts": new_parts, "reports": reps, "a69": a69s, "bins": nbins}


def rel_kinds_by_unit(rows, rels, units) -> list[set]:
    at = {rows[i]["id"]: u for u, x in enumerate(units) for i in x}
    out = [set() for _ in units]
    for x in rels:
        if x.get("a") in at:
            out[at[x["a"]]].add(x.get("type"))
    return out


def carry_pool(fam: str, rows, rels, r1_selected: set) -> tuple[list, list, dict]:
    """A carry-over pool: the whole units of the round-1 SELECTED rows (a unit only partly selected is left out);
    F5: only units whose relations are all complement / equiv (at least one). Returns (rows, rels, info)."""
    units = cs.units_of(rows, rels)
    kinds = rel_kinds_by_unit(rows, rels, units)
    only = CARRY_REL_ONLY.get(fam)
    keep, why = set(), Counter()
    for u, x in enumerate(units):
        if not all(rows[i]["id"] in r1_selected for i in x):
            why["not_round1_selected"] += 1
            continue
        if only is not None and not (kinds[u] and kinds[u] <= only):
            why["relation_kinds_not_" + "_".join(sorted(only))] += 1
            continue
        keep.update(x)
    out = [r for i, r in enumerate(rows) if i in keep]
    ids = {r["id"] for r in out}
    return out, [x for x in rels if x.get("a") in ids and x.get("b") in ids], \
        {"pool_rows": len(out), "units_left_out": dict(why)}


def preferred(fam: str, r) -> bool:
    ds = CARRY_PREFER.get(fam)
    ts = (r.get("meta") or {}).get("text_source")
    return bool(ds) and isinstance(ts, dict) and str(ts.get("dataset")) in ds


def select_carry(fam: str, rows, rels, pg: dict, target: int, r1_selected: set, seed: int = SEED,
                 drop_ids: set | None = None) -> dict:
    """A carry-over pool's C2 selection (spec 3.19). F11: the XED / MAMS units are selected first (to the target);
    the rest of the pool fills only what they leave short, in a second selection on the remaining units."""
    pool, prel, info = carry_pool(fam, rows, rels, r1_selected)
    if fam not in CARRY_PREFER:
        rec = select_family(fam, pool, prel, pg, target, seed, drop_ids)
        rec["carry_pool"] = info
        return rec
    units = cs.units_of(pool, prel)
    pref_ids = {pool[i]["id"] for x in units if all(preferred(fam, pool[i]) for i in x) for i in x}
    a_rows = [r for r in pool if r["id"] in pref_ids]
    b_rows = [r for r in pool if r["id"] not in pref_ids]
    ka, kb = sel_key(fam) + "|pref", sel_key(fam) + "|rest"
    ra = select_family(fam, a_rows, prel, pg, target, seed, drop_ids, key=ka)
    out = dict(ra)
    out["carry_pool"] = info | {"preferred_rows": len(a_rows), "preferred_selected": len(ra["selected_ids"])}
    short = target - len(ra["selected_ids"])
    if short > 0 and b_rows:
        rb = select_family(fam, b_rows, prel, pg, short, seed, drop_ids, key=kb)
        chosen = ra["selected_ids"] + rb["selected_ids"]
        out["selected_ids"] = chosen
        out["parts"] = [{"key": ka, "ids": ra["selected_ids"]}, {"key": kb, "ids": rb["selected_ids"]}]
        out["part_reports"] = {"preferred": ra["report"], "rest": rb["report"]}
        out["report"] = union_report(pool, prel, chosen, pg, target)
        pu = cs.units_of(pool, prel)
        ch = set(chosen)
        out["g5"] = cs.g5_reread(pool, pu, [u for u, x in enumerate(pu) if pool[x[0]]["id"] in ch], pg, fam)
        out["exclude_ids"] = {"preferred": ra["exclude_ids"], "rest": rb["exclude_ids"]}
        out["easy_dropped_units"] = ra["easy_dropped_units"] + rb["easy_dropped_units"]
        out["budget"] = {"preferred": ra["budget"], "rest": rb["budget"]}
        out["reflow"] = {"preferred": ra["reflow"], "rest": rb["reflow"]}
        out["crowd_pg"] = {**ra["crowd_pg"], **rb["crowd_pg"]}
        out["difficulty_bin"] = {**ra["difficulty_bin"], **rb["difficulty_bin"]}
    out["target"] = target
    out["key"] = sel_key(fam)
    return out


def union_report(rows, rels, chosen_ids, pg, target) -> dict:
    """crowd_select.selection_report on the union of a two-part carry selection: every check (total, caps, label x
    bin chi-square) is judged on all of it."""
    ch = set(chosen_ids)
    sub = [r for r in rows if r["id"] in ch]
    units = cs.units_of(sub, [x for x in rels if x["a"] in ch and x["b"] in ch])
    bins = {r["id"]: cs.bin_of(pg.get(r["id"])) for r in sub}
    rep = cs.selection_report(sub, units, list(range(len(units))), bins, target, True,
                              {r["id"]: pg[r["id"]] for r in sub})
    rep["crowd_rule"] = CROWD_RULE
    return rep


# ------------------------------------------------------------------ CLI

def family_inputs(ilog: C2InputLog, fam: str) -> tuple[list, list, dict]:
    """Candidates + relations of a C2 family / T37b, checked against its MANIFEST (count and sha256 of both files)."""
    f = c2io.fam_files(fam)
    if fam in CARRY:
        rows, rels = cs.load_family(ilog, fam)
        return rows, rels, {"candidates_sha256": sha256_file(f["cand"]),
                            "relations_sha256": sha256_file(f["rel"]) if f["rel"] else None}
    rows = ilog.jsonl(f["cand"])
    rels = ilog.jsonl(f["rel"]) if f["rel"].exists() else []
    man = ilog.json(f["manifest"]) if f["manifest"].exists() else {}
    got = {c2io.CAND: (sha256_file(f["cand"]), len(rows))}
    if f["rel"].exists():
        got[c2io.REL] = (sha256_file(f["rel"]), len(rels))
    bad = c2io.manifest_problems(fam, man, got)
    if bad:
        raise SystemExit("family refused: " + "; ".join(bad))
    return rows, rels, {"candidates_sha256": got[c2io.CAND][0], "relations_sha256": got.get(c2io.REL, (None,))[0]}


def available(fams=None) -> list[str]:
    names = fams or [f for f in TARGETS if f not in CARRY]
    for f in names:
        c2io.check_name(f, "family")
        if f not in TARGETS:
            raise SystemExit(f"{f}: not a C2 family (spec 2.1 / 3.19): {sorted(TARGETS)}")
    return [f for f in names if c2io.fam_files(f)["cand"].exists()]


# ------------------------------------------------------------------ the G13 log check (shared with mix_c2)

_RUN_OF_PREFIX = (("c2_seed_", "seed"), ("c2_cand_", "candidates"), ("c2_carry_", "carry"), ("c2_final", "final"))
DEV_BASENAMES = ("c2_mixdev.jsonl", "c2_transfer_dev.jsonl", "mixdev_S5.jsonl")   # the C2 dev files (g13_c2.C2_DEV)


def lean_rel(p) -> str:
    """lean/-relative posix path (absolute outside lean/, e.g. test folders); the same keys as g13_c2.lean_rel."""
    try:
        return Path(p).resolve().relative_to(c2io.LEAN.resolve()).as_posix()
    except ValueError:
        return Path(p).as_posix()


def current_dev_files() -> list[Path]:
    """The C2 dev files that exist now, the set g13_c2 hashes at the start of a non-seed run (its C2_DEV targets):
    data/c2_mixdev.jsonl, data/c2_parts/*/out/mixdev_S5.jsonl and data/c2_transfer_dev.jsonl. The never-open rule is
    applied before any stat (resolved_refusal: the path and where its links lead): the c2_parts folder is listed by name
    only (no glob: a glob would stat <child>/out of a refused child first), and a child or its dev file that is refused,
    or is a link into a refused folder, is neither stat-ed nor scanned nor returned."""
    out, seen, root = set(), set(), c2io.C2_PARTS
    for p in (c2io.DATA / "c2_mixdev.jsonl", c2io.DATA / "c2_transfer_dev.jsonl"):
        if not resolved_refusal(p) and p.is_file():
            out.add(p)
    if not resolved_refusal(root) and root.is_dir():
        for name in sorted(os.listdir(root)):                     # names only; one file per resolved path (as g13_c2.dev_files)
            child = root / name
            if resolved_refusal(child):                           # a refused family folder: not stat-ed, not scanned
                continue
            p = child / "out" / "mixdev_S5.jsonl"
            if not resolved_refusal(p) and p.is_file() and p.resolve() not in seen:
                seen.add(p.resolve())
                out.add(p)
    return sorted(out)


G13_RECORD_KEYS = ("inputs_at_start", "inputs_at_start_paths", "engine")          # keys only a g13_c2 record carries


def is_g13_log(d, path, tool: str = G13_TOOL) -> bool:
    """A C2 G13 log: a JSON object whose "tool" is g13_c2.py (any spelling of the path: a variant is then refused as "not
    a g13_c2.py record"), whose file is named c2_*.json, or that carries a g13_c2 record (inputs_at_start,
    inputs_at_start_paths or engine, or a set name c2_*: a log with its tool key removed or its file renamed is still
    checked). Any other drop list (REPLAY_DENY_A46.json, pool_drops_r1.json ...) is not one."""
    return isinstance(d, dict) and (d.get("tool") == tool or Path(str(d.get("tool"))).name == Path(tool).name
                                    or re.fullmatch(r"c2_.*\.json", Path(path).name) is not None
                                    or any(k in d for k in G13_RECORD_KEYS)
                                    or str(d.get("set") or "").startswith("c2_"))


def log_run(d: dict, name: str) -> str | None:
    """The run a log came from: its "run" key, else the set-name prefix (c2_cand_<block> ...)."""
    return d.get("run") or next((r for pre, r in _RUN_OF_PREFIX if name.startswith(pre)), None)


def log_block(d: dict, name: str, run: str | None) -> str | None:
    if isinstance(d.get("block"), str) and d["block"]:
        return d["block"]
    for pre, r in _RUN_OF_PREFIX:
        if r in ("candidates", "carry") and name.startswith(pre):
            return name[len(pre):] or None
    return "final" if run == "final" else None


def train_file_of(run: str, block: str) -> Path:
    """The training file a g13_c2 run reads (g13_c2.build_sets): a block's candidates (candidates / carry runs) or the
    final mix. check_name refuses a block name that holds 'ohs' or 'jev' before a path is built."""
    if run == "final":
        return c2io.C2_PARTS / "c2_train.jsonl"
    c2io.check_name(block, "block")
    return c2io.fam_files(block)["cand"]


def _recorded(d: dict) -> tuple[dict, dict, dict]:
    """(by_rel, by_name, train) of a log: {lean-relative path: sha256} of inputs_at_start entries that name their path
    (inputs_at_start_paths, or a key that is itself a path), {file name: sha256} of those that do not, and the engine's
    own {path: sha256} of the training file(s) (engine.inputs_sha256.train)."""
    ias = d.get("inputs_at_start") if isinstance(d.get("inputs_at_start"), dict) else {}
    paths = d.get("inputs_at_start_paths") if isinstance(d.get("inputs_at_start_paths"), dict) else {}
    by_rel, by_name = {}, {}
    for key, sha in ias.items():
        rel = paths.get(key) if isinstance(paths.get(key), str) and paths.get(key) else (key if "/" in str(key) else None)
        (by_rel.__setitem__(rel, sha) if rel is not None else by_name.__setitem__(str(key), sha))
    eng = (d.get("engine") or {}).get("inputs_sha256") if isinstance(d.get("engine"), dict) else None
    train = eng.get("train") if isinstance(eng, dict) and isinstance(eng.get("train"), dict) else {}
    return by_rel, by_name, train


def _sha_if_file(ilog, p: Path, cache: dict) -> str | None:
    """sha256 of an existing file as it is now (None: gone). The never-open rule (guard: the path and where its links lead)
    runs before any stat or open; ilog.record then logs the file as an input of the run (path and sha256, like every other
    input)."""
    key = str(p)
    if key not in cache:
        guard(ilog, p)
        ilog.record(p)
        cache[key] = sha256_file(p) if p.is_file() else None
    return cache[key]


def stale_problems(ilog, d: dict, name: str, run: str | None, cache: dict | None = None, dev_now=None) -> list[str]:
    """A guarded candidates / carry / final G13 log is tied to the files that are used now. Its recorded training sha256
    (inputs_at_start, and the engine's inputs_sha256.train) must equal the current candidates_c2.jsonl of its block (the
    final mix: data/c2_parts/c2_train.jsonl); every recorded C2 dev file must equal the file now (a file gone is a
    change) and every dev file that exists now must be in the log. One message per file:
    "<log>: stale G13 log (<file> changed after the run): re-run G13 for <block>". A seed log is not tied to these files."""
    if run == "seed":
        return []
    cache = {} if cache is None else cache
    block = log_block(d, name, run)
    if block is None:
        return [f"{name}: stale G13 log (cannot tell which block it covers): re-run G13"]
    by_rel, by_name, train = _recorded(d)
    out = []

    def stale(fname: str, why: str = "changed after the run"):
        out.append(f"{name}: stale G13 log ({fname} {why}): re-run G13 for {block}")

    try:
        tp = train_file_of(run or "candidates", block)
        cur = _sha_if_file(ilog, tp, cache)
    except SystemExit as e:                                   # the never-open rule refused the block name / path
        return [f"{name}: stale G13 log (training file refused: {e}): re-run G13 for {block}"]
    rel = lean_rel(tp)
    got = [x for x in (train.get(rel), by_rel.get(rel)) if x is not None]
    if not got and tp.name in by_name:
        got = [by_name[tp.name]]                               # an older record: names only
    if not got:
        stale(tp.name, "not recorded in the log")
    elif cur is None or any(x != cur for x in got):
        stale(tp.name)
    dev = dev_now() if dev_now is not None else current_dev_files()
    dev = [Path(p) for p in dev]
    count = Counter(p.name for p in dev)

    def shown(p: Path) -> str:                                 # the file name; the path when two dev files share it
        return lean_rel(p) if count[p.name] > 1 else p.name
    try:
        for p in dev:
            guard(ilog, p)                                     # the never-open rule before lean_rel (resolve) stats the path
            sha = by_rel.get(lean_rel(p))
            if sha is None and count[p.name] == 1:
                sha = by_name.get(p.name)
            if sha is None or sha != _sha_if_file(ilog, p, cache):
                stale(shown(p))                                # changed, or a dev file that appeared after the run
    except SystemExit as e:
        return out + [f"{name}: stale G13 log (dev file refused: {e}): re-run G13 for {block}"]
    now = {lean_rel(p) for p in dev}
    for r in sorted(by_rel):                                   # a recorded dev file that is gone now
        if Path(r).name in DEV_BASENAMES and r not in now:
            stale(Path(r).name, "changed after the run (gone)")
    names_now = set(count)
    for n in sorted(by_name):                                  # ... also when the record names it by its file name only
        if n in DEV_BASENAMES and n not in names_now:
            stale(n, "changed after the run (gone)")
    return out


def g13_log_problems(ilog, files, tool: str = G13_TOOL, exempt=(), cache: dict | None = None, dev_now=None) -> list[str]:
    """Why a C2 G13 log among the drop lists may not be used (empty = fine). A file is a C2 G13 log when its "tool" is
    g13_c2.py, it is named c2_*.json or it carries a g13_c2 record; `exempt` paths (mix_c2 passes pool_drops_r1.json, the
    round-1 list; matched by RESOLVED PATH, never by name or substring) and every other list are not checked (read as
    before). A C2 G13 log must be complete (complete true, incomplete_why empty: a changed input, a missing dev set or a
    method that did not run makes it incomplete, and its drop_ids then cannot be trusted), unless it is a seed run's carry
    an inputs_at_start record (a log from before the run-input guard has none: re-run), and, unless it is a seed run's, not
    be stale (stale_problems). mix_c2 and c2_select --exclude-ids both call this one function (--exclude-ids passes no
    exempt path)."""
    out, cache = [], {} if cache is None else cache
    skip = set()
    for e in exempt or ():
        guard(ilog, e)
        skip.add(str(Path(e).resolve()))
    for f in files or []:
        guard(ilog, f)                                         # the never-open rule before the first stat of the path
        if str(Path(f).resolve()) in skip:
            continue
        d = ilog.json(f)
        if not is_g13_log(d, f, tool):
            continue
        name = d.get("set") or Path(f).stem
        why = d.get("incomplete_why")
        if d.get("tool") != tool:
            out.append(f"{name}: not a g13_c2.py record (tool {d.get('tool')!r})")
        if d.get("complete") is not True or (isinstance(why, list) and why) or not isinstance(why, list):
            out.append(f"{name}: incomplete G13 log (complete {d.get('complete')!r}, "
                       f"{len(why) if isinstance(why, list) else 'no'} reasons): re-run before the mix")
        run = log_run(d, name)
        ias = d.get("inputs_at_start")
        if run != "seed" and not (isinstance(ias, dict) and ias):
            out.append(f"{name}: pre-guard G13 log (no inputs_at_start): re-run before the mix")
        else:
            out += stale_problems(ilog, d, name, run, cache, dev_now)
    return out


def plain_list_problems(ilog, files) -> list[str]:
    """Why a --exclude-ids file that is NOT a C2 G13 log may not be used (empty = fine): the gate c2_select always had for
    it, with no exemption for any file (not by path, not by name). It must be a JSON object with "complete" true and no
    incomplete_why (a partial round-1 log such as F6.json, a plain drop list with no completeness key such as
    REPLAY_DENY_A46.json / pool_drops_r1.json, or a g13 record whose tool key was removed would let leaked rows into
    selection: A34 b). A C2 G13 log is not judged here (g13_log_problems does)."""
    out = []
    for f in files or []:
        guard(ilog, f)                                         # the never-open rule before the first stat of the path
        d = ilog.json(f)
        if is_g13_log(d, f):
            continue
        why = d.get("incomplete_why") if isinstance(d, dict) else None
        if not isinstance(d, dict) or d.get("complete") is not True or why:
            have = d.get("complete", "<no complete key>") if isinstance(d, dict) else "<not a JSON object>"
            out.append(f"G13 log is not complete (complete = {have!r}"
                       + (f", {len(why) if isinstance(why, list) else 'some'} incomplete_why reasons" if why else "")
                       + "); a partial drop list is refused (A34 b): rerun G13 to completion first")
    return out


def drop_ids_of(ilog, files) -> set:
    """The ids of the drop lists given to --exclude-ids. A C2 G13 log (is_g13_log) goes through g13_log_problems, the
    check the mixer runs: any problem (incomplete, pre-guard, stale) refuses the whole run, a partial or stale drop list
    would let leaked rows into selection (A34 b). Every other file keeps the gate it had before the guard: complete true
    (plain_list_problems); no file is exempt from either check (the mixer's pool_drops_r1.json exemption is the mixer's
    own: here that path is judged like any other)."""
    files, cache = list(files or []), {}
    bad = [f"{p}: {why}" for p in files
           for why in g13_log_problems(ilog, [p], cache=cache) + plain_list_problems(ilog, [p])]
    if bad:
        raise SystemExit("--exclude-ids refused (G13 logs must be complete, guarded and current; a partial or stale drop "
                         "list is refused, A34 b):\n  " + "\n  ".join(bad))
    out = set()
    for p in files:
        d = ilog.json(p)
        if not isinstance(d, dict):
            raise SystemExit(f"{p}: not a JSON object with a drop id list")
        got = next((d[k] for k in ("drop_ids", "training_ids_to_drop", "ids") if isinstance(d.get(k), list)), None)
        if got is None:
            raise SystemExit(f"{p}: no drop id list (drop_ids / training_ids_to_drop / ids)")
        out |= set(map(str, got))
    return out


def write_select(fam, rec, extra: dict):
    g5 = rec.pop("g5")
    sha = c2io.write_json(OUT / f"select_{fam}.json", {**rec, **extra})
    c2io.write_json(OUT / f"g5_reread_{fam}.json", g5)
    rep = rec["report"]
    log(f"select {fam}: {rep['rows']} rows (target {rec['target']}), bins {rep['bins']}, pass {rep['pass']}, "
        f"G5 low-p_g rows {g5['n_low']} + sample {g5['n_sample']}; sha {sha[:12]}")


def cmd_select(a):
    c2io.require_a38()
    ilog = LinkGuardedInputLog()
    drop = drop_ids_of(ilog, a.exclude_ids)
    for fam in available(a.fam):
        if fam in CARRY:
            raise SystemExit(f"{fam}: carry-over pools use the 'carry' command")
        rows, rels, shas = family_inputs(ilog, fam)
        sd = SHARDS / fam
        pg, view, probs = load_c1_full(ilog, rows, sd / f"labels_{C1}", sd)
        ntok = None
        if a.a69_repair and fam in TRAP_FAMS:                     # the token-mean bar needs real token counts (as mix_c2 counts them)
            import mixer as mx
            ntok = dict(zip((r["id"] for r in rows), mx.token_counts(ilog, rows)))
        rec = select_family(fam, rows, rels, pg, TARGETS[fam], SEED, drop, probs=probs, repair=bool(a.a69_repair), ntok=ntok)
        write_select(fam, rec, {**shas, "c1_view": view, "exclude_files": [str(p) for p in a.exclude_ids or []]})
    c2io.write_json(OUT / "select_inputs.json", {"inputs": ilog.entries})


def cmd_carry(a):
    c2io.require_a38()
    ilog = LinkGuardedInputLog()
    drop = drop_ids_of(ilog, a.exclude_ids)
    for fam in a.fam or list(CARRY):
        if fam not in CARRY:
            raise SystemExit(f"{fam}: not a carry-over pool {sorted(CARRY)}")
        rows, rels, shas = family_inputs(ilog, fam)
        r1 = ilog.json(R1_SELECT / f"select_{fam}.json")
        if r1.get("candidates_sha256") != shas["candidates_sha256"]:
            raise SystemExit(f"{fam}: round-1 select_{fam}.json was made on another candidates file")
        sd = R1_SHARDS / fam
        pg, view = load_c1(ilog, rows, sd / f"labels_{C1}", sd)
        rec = select_carry(fam, rows, rels, pg, TARGETS[fam], set(r1["selected_ids"]), SEED, drop)
        write_select(fam, rec, {**shas, "c1_view": view, "round1_select_sha256": sha256_file(R1_SELECT /
                                                                                                f"select_{fam}.json")})
    c2io.write_json(OUT / "carry_inputs.json", {"inputs": ilog.entries})


def cmd_tasks(a):
    """The C1-only crowd read plan (no read here): rows per family; --write-shards writes the shard sets the read
    labels (data/c2_crowd_shards/<FAM>/, shard_golden format)."""
    c2io.require_a38()
    sys.path.insert(0, str(c2io.LEAN))
    import shard_golden as sg
    ilog = LinkGuardedInputLog()
    fams = [f for f in available(a.fam) if f not in CARRY]
    tasks = {"purpose": "C2 G9 crowd read (A37 e: C1 only, one view, given option order, A18.2 readout; SGLang S1 "
                        "or the free L4; no GO needed under A37 l)", "model": C1, "seed": SEED, "families": {}}
    n = 0
    for fam in fams:
        rows, _, shas = family_inputs(ilog, fam)
        bad = c2io.candidate_problems(fam, rows)
        if bad:
            raise SystemExit("candidates refused: " + "; ".join(bad))
        sd = SHARDS / fam
        man = None
        if a.write_shards:
            if resolved_refusal(sd):
                raise SystemExit(f"shard dir refused: {sd}")
            man = sg.write_shards(rows, sd, SHARD_ROWS, {"purpose": f"C2 crowd read {fam}", "seed": SEED,
                                                         "candidates_sha256": shas["candidates_sha256"]})
        tasks["families"][fam] = {"rows": len(rows), "target": TARGETS[fam], **shas,
                                  "shards_dir": str(sd.relative_to(c2io.LEAN)), "shards_written": man is not None,
                                  "labels_dir": str((sd / f"labels_{C1}").relative_to(c2io.LEAN))}
        n += len(rows)
    tasks["estimate"] = {"reads": n, "hours_at_S1": round(n / READ_ROWS_PER_H, 2),
                         "basis": f"spec 9.2: SGLang S1 about {READ_ROWS_PER_H:,} rows/h"}
    c2io.write_json(OUT / "crowd_tasks_c2.json", tasks)
    log(f"tasks: {len(fams)} families, {n:,} reads; shards {'written' if a.write_shards else 'not written'}")


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    sub = ap.add_subparsers(dest="cmd", required=True)
    t = sub.add_parser("tasks")
    t.add_argument("--fam", nargs="*", default=None)
    t.add_argument("--write-shards", dest="write_shards", action="store_true")
    for name in ("select", "carry"):
        s = sub.add_parser(name)
        s.add_argument("--fam", nargs="*", default=None)
        s.add_argument("--exclude-ids", dest="exclude_ids", nargs="+", default=None,
                       help="G13 decontam logs (key drop_ids); units holding a listed id leave the pool first")
        if name == "select":
            s.add_argument("--a69-repair", dest="a69_repair", action="store_true", default=True,
                           help="PREREG A69 (DRAFT): the drop-only repair step after the trap-weighted selection (program families); the default")
            s.add_argument("--no-a69-repair", dest="a69_repair", action="store_false",
                           help="switch the A69 repair step off (the pre-repair A69 selection)")
    a = ap.parse_args(argv)
    {"tasks": cmd_tasks, "select": cmd_select, "carry": cmd_carry}[a.cmd](a)


if __name__ == "__main__":
    main()
