"""C round-1 mixer (C_DATA_SPEC.md v4 section 11 step 9; sections 0, 2.1, 2.4, 3, 4, 5, 6, 7, 8; recipe v4 3; PREREG
A15, A16, A16.1, A16.2, A17). CPU only: no Modal, gcloud or paid call; no git.

Round 1: 150,000 rows = 90,000 replay (C1's golden_train draw, kept rows of the second pass, margin-trimmed per source
quota, E2 re-checked) + 45,250 own (13 families, spec 2.1 crowd selection; + public fallback rows, e.g. Qasper -> F13)
+ 8,750 public (minus the fallback rows) + 6,000 commits. Only the spec's stated fallbacks change a share.

Steps (each counted in the report): input-path log with sha256 (7.4 guard); deny-list (3.H, denylist.py check in its
own process) + licence join; fmt1 refuse_held_out on every shard (held-out styles, S5); decontam drop hooks (G13
orchestrator id lists); relation units (<= 3 rows, long units <= 2, one call_id); C1 anchor targets (spec 5: C1 right
and p_top >= 0.8, or right on a protected unit; never on new rows or rows with their own target); replay option_level
detection + G18 ordinal target lint on the merged targets (100%); E2 replay yes rate per wording; G10 aggregate
checks; token cap (real Qwen3.5 tokenizer on the rendered cygnet / schema_branch_mark prompt, so instructions count
twice: rows >= 2,000 tokens <= 9% of new rows and <= 30% of new-row tokens; every row <= 7,900); train_decoder.check_rows
on every row; config fill values (epochs from the batches() dry run, expect_ord_rows, expect_kd_targets, expect_kd_full).
PREREG A28 (b): the cap is met after the refills by cap_trim (A28_RULE): spec 6's F13 / 3B 6-7.9K units first (only
while long tokens > 30%), then closed-form quotas: the mix's excess long rows (or tokens) apportioned over the blocks
over a cap on their own rows by their own excess, met with whole units (same-cell short swaps first; own blocks then
drop in composite moves over their cells that keep every spec 2.1 / G9 / G10 rule judged against the pre-trim mix,
with no search constants), a stated fallback for any quota a block cannot meet; freed rows are refilled under A26 (b)
(short units of cards already mixed, <= 1.5x target, <= 12% of the realised own rows after each refill; a family
without refill rows may not end above max(12%, its pre-trim share)); attack twins = the inv relation's twins;
a remainder sets replay = floor(1.5 x realised new rows) (60% of the new total); a mix under the cap is unchanged.
Refills: rows lost to G13, deny-list, G18 or 7,900-token drops are refilled with whole unused units (replay: same
source's trimmed-off margin, E2 re-reported; own / commit: unselected units of the same crowd stratum and bin;
public: same source's reserve). Held-out checks: spec 10 S7 (group_id / normalized state / structure_hash vs every
mix-tuning dev part; domain_pack vs the block's own mixdev_S5; F14; commit held-out repos); strict formats-1 style ids
on own and commit rows. Relation files are taken from each MANIFEST and must match its count and sha256. Parents must
be declared by every builder (only declared lists go to denylist.py). G10 yes-rate cells: 50 +/- 2 at >= 50 rows.

  ../.venv/bin/python c_build/mixer.py --dry-run            counts only (any families present; provisional selection)
  ../.venv/bin/python c_build/mixer.py --final --sealed-sha <A15 suite sha> --decontam-drops logs/decontam_counts/*.json
--final refuses unless every included family's QC_REPORT.json says pass=true and records the sha256 of the candidates
and relation files on disk (the same for each public builder's qc/QC_REPORT.json), the crowd score files exist, every
crowd selection file exists, matches its candidates file and target and passes its own checks, and the sealed sha is
A15's; it also refuses on any failed gate or unmet share. --dry-run lists the --final blockers in the report.
"""
from __future__ import annotations

import argparse
import json
import math
import random
import re
import subprocess
import sys
import time
from collections import Counter, defaultdict, deque
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import crowd_select as cs  # noqa: E402
from mixio import (A15_SUITE_SHA, DATA, HERE, LEAN, PY, InputLog, h64, log_line, sha256_file,  # noqa: E402
                   write_json, write_jsonl)

SEED = 20261003
SHARES_R1 = {"replay": 90000, "own": 45250, "public": 8750, "commit": 6000}
TOTAL_R1 = 150000
KD, LS, LS_MNLI = 0.5, 0.05, 0.08                 # recipe 3 (C1's values)
KD_FULL_SRC = ("gd_gen2_probability",)
KD_SKIP_SRC = ("blend50",)
LONG_TOK, MAX_TOK = 2000, 7900
LONG_ROW_SHARE, LONG_TOK_SHARE = 0.09, 0.30
BATCH = 16
REPLAY_SHARDS = DATA / "c_replay_r1_shards"
REPLAY_LABELS = REPLAY_SHARDS / "labels_q35_4b_main500k"
OLD_SLICE = DATA / "c_old_slice_shards"
PG_ANCHOR = HERE / "replay_r1_pg_anchor.json"
REPLAY_WRITE = HERE / "replay_r1_write.json"
REPLAY_VERDICTS = HERE / "replay_denylist_verdicts.json"
GOLDEN_RELS = DATA / "v14_parts/golden_relations.jsonl"
DENYLIST = DATA / "c_parts/denylist.json"
OUT_PARTS = DATA / "c_parts"
WORK = HERE / "mix_r1"
LOG = HERE / "progress_mixer.log"
CONFIG = LEAN / "runs/q35_4b_c_r1.json"
PUBLIC_FILES = ("public-1/out/public1_rows_r1.jsonl", "public-2/out/rows_r1.jsonl", "public-3/out/public3_rows_r1.jsonl")
PUBLIC_RESERVE = ("public-1/out/public1_reserve.jsonl", "public-2/out/reserve_r1.jsonl",
                  "public-3/out/public3_reserve.jsonl")
PROGRAM_LICENCE = "CC0 1.0 (program-generated)"
REPLAY_LICENCE_JOIN = {"judge_prm800k": "MIT (openai/prm800k; as gd_prm800k_steps, LICENCE_REGISTER.md 4)",
                       "judge_mathderiv": PROGRAM_LICENCE + " (build_judge.py, procedural)"}
_LEVEL = re.compile(r"^\s*(\d{1,2})\s*:\s*\S")


def log(msg):
    log_line(LOG, "mixer: " + msg)
    print(msg, flush=True)


def rs_mod():
    """The pinned replay sampler (A16.1 5735ca3e...), imported for its unit, order and E2 helpers only."""
    import replay_sample as rs
    return rs


# ------------------------------------------------------------------ replay (spec 5)

def light(r, rs) -> dict:
    """replay_sample's row form (the fields its unit order and E2 helpers read)."""
    m = r.get("meta") or {}
    w = rs.norm_wording(r["instructions"]) if r["qtype"] == "noul" else ""
    return {"id": r["id"], "source": r["source"], "qtype": r["qtype"], "role": r["role"], "gold": r["gold"],
            "soft": isinstance(m.get("teacher"), dict) and m.get("teacher_src") != "blend50",
            "gold_probs": bool(m.get("gold_probs")), "w": w, "wf": rs.wording_family(r["role"], w) if w else ""}


def load_replay(ilog: InputLog, rep: dict):
    """Kept rows of the second pass (C1 read + p_g rule), whole relation units. Returns rows (full dicts), light rows,
    units, kept unit indices, flags, C1 probs."""
    rs = rs_mod()
    sys.path.insert(0, str(LEAN))
    import shard_golden as sg
    pa = ilog.json(PG_ANCHOR)
    if pa.get("pg_rule", {}).get("amendment") != "A16":
        raise SystemExit(f"replay_r1_pg_anchor.json: unexpected p_g rule {pa.get('pg_rule')}")
    rows = [r for p in sg.shard_files(REPLAY_SHARDS) for r in ilog.jsonl(p)]
    for p in sorted(REPLAY_LABELS.glob("shard_*")):
        ilog.record(p)
    probs, view = sg.load_labels(REPLAY_LABELS, REPLAY_SHARDS, return_view=True)
    if (view or {}).get("settings", {}).get("name") != "q35_4b_main500k" or view["settings"] != pa["read"]:
        raise SystemExit("replay labels are not the C1 A5 read recorded by the second pass")
    flags = pa["flags"]
    miss = [r["id"] for r in rows if r["id"] not in flags or r["id"] not in probs]
    if miss:
        raise SystemExit(f"{len(miss)} replay rows without second-pass flags or C1 labels, e.g. {miss[:3]}")
    ids = {r["id"] for r in rows}
    rels = [x for x in ilog.jsonl(GOLDEN_RELS) if x["a"] in ids and x["b"] in ids]
    lt = [light(r, rs) for r in rows]
    units = rs.build_units(lt, rels)
    kept = [u for u, x in enumerate(units) if not any(flags[lt[i]["id"]]["drop_pg"] for i in x["rows"])]
    rep["replay_read"] = {"rows_read": len(rows), "units": len(units), "relations": len(rels),
                          "rows_dropped_pg": sum(len(units[u]["rows"]) for u in range(len(units))) -
                          sum(len(units[u]["rows"]) for u in kept), "rows_kept": sum(len(units[u]["rows"]) for u in kept),
                          "second_pass_counts": pa.get("counts")}
    return rows, lt, units, kept, rels, flags, probs


def old_slice_clash(ilog, rows, lt, units, kept, rs):
    """Units sharing a group_id or normalized state with the old slice (held out in both rounds) are removed."""
    sys.path.insert(0, str(LEAN))
    import shard_golden as sg
    old = [r for p in sg.shard_files(OLD_SLICE) for r in ilog.jsonl(p)] if OLD_SLICE.exists() else []
    groups, states = {r["group_id"] for r in old}, {rs.norm_state(r.get("state")) for r in old}
    bad = {u for u in kept if any(rows[i]["group_id"] in groups or rs.norm_state(rows[i].get("state")) in states
                                  for i in units[u]["rows"])}
    return [u for u in kept if u not in bad], {"old_slice_rows": len(old), "clash_units_removed": len(bad)}


def trim_replay(ilog, lt, units, kept, rep, total=SHARES_R1["replay"], scale=False):
    """The margin trim (replay_sample second-pass note): per source, the prefix of the sampler's own seeded stratified
    unit order covering the round-1 quota Q1_s; sources short after the p_g drops pass their deficit to sources with
    margin (largest remainder over Q1), so replay stays at exactly `total`; then E2 re-stratification by same-source,
    same-size unit swaps with the trimmed-off margin (replay_sample.restratify)."""
    rs = rs_mod()
    q1 = {s: v["q1"] for s, v in ilog.json(REPLAY_WRITE)["quota_by_source"].items()}
    if scale:                       # PREREG A34 (c): a smaller replay total keeps the per-source Q1 proportions
        q1 = largest_remainder(q1, total)
    by_src = defaultdict(list)
    for u in kept:
        by_src[units[u]["source"]].append(u)
    order = {s: rs.unit_order(lt, units, uis) for s, uis in by_src.items()}
    size = lambda us: sum(len(units[u]["rows"]) for u in us)  # noqa: E731
    take = {s: rs.prefix(order[s], units, q1.get(s, 0)) for s in order}
    deficit = total - sum(size(t) for t in take.values())
    rounds = 0
    while deficit > 0 and rounds < 50:
        donors = {s: q1.get(s, 0) for s in order if len(take[s]) < len(order[s])}
        if not donors:
            break
        extra = largest_remainder(donors, deficit)
        for s, k in extra.items():
            if k > 0:
                take[s] = rs.prefix(order[s], units, size(take[s]) + k)
        deficit = total - sum(size(t) for t in take.values())
        rounds += 1
    take = exact_total(take, q1, units, total)
    sel = [u for s in sorted(take) for u in take[s]]
    chosen = set(sel)
    pool = [u for s in sorted(order) for u in order[s] if u not in chosen]
    short = {s: q1.get(s, 0) - size(take[s]) for s in take if size(take[s]) < q1.get(s, 0)}
    rep["replay_trim"] = {"quota_r1": sum(q1.values()), "sources": len(take), "rows": size(sel), "units": len(sel),
                          "margin_units_left": len(pool), "deficit_rounds": rounds,
                          "sources_short_of_q1": len(short), "rows_short_of_q1": sum(short.values()),
                          "redistributed_to_other_sources": sum(max(0, size(take[s]) - q1.get(s, 0)) for s in take)}
    return sel, pool


def largest_remainder(weights: dict, total: int) -> dict:
    w = sum(weights.values()) or 1
    raw = {k: total * v / w for k, v in weights.items()}
    out = {k: int(math.floor(x)) for k, x in raw.items()}
    for k in sorted(raw, key=lambda k: (-(raw[k] - out[k]), k))[:total - sum(out.values())]:
        out[k] += 1
    return out


def exact_total(take: dict, q1: dict, units, total: int) -> dict:
    """Unit granularity overshoots a prefix by < one unit per source: drop the last single-row units of the sources
    furthest above Q1 until the replay total is exact."""
    size = lambda us: sum(len(units[u]["rows"]) for u in us)  # noqa: E731
    over = sum(size(t) for t in take.values()) - total
    while over > 0:
        cand = [s for s in take if any(len(units[u]["rows"]) == 1 for u in take[s])]
        if not cand:
            break
        s = max(cand, key=lambda s: (size(take[s]) - q1.get(s, 0), s))
        j = max(i for i, u in enumerate(take[s]) if len(units[u]["rows"]) == 1)
        take[s] = take[s][:j] + take[s][j + 1:]
        over -= 1
    return take


def e2_restratify(lt, units, sel, pool, rep):
    """Spec 5 E2 on the trimmed set: cells with >= 50 hard yes/no rows outside 50 +/- 5 are re-stratified by
    same-source, same-size unit swaps with the margin (replay_sample.restratify); before/after reports."""
    rs = rs_mod()
    cell0 = rs.cell_defs(lt, units, sel)
    sticky = {lt[i]["w"] for u in sel for i in units[u]["rows"] if rs.hard_yn(lt[i]) and cell0(lt[i]).startswith("w:")}
    before = rs.e2_report(lt, units, sel)
    sel2, pool2, swaps, stuck, sticky2 = rs.restratify(lt, units, sel, pool)
    after = rs.e2_report(lt, units, sel2, sticky=sticky2)
    rep["e2"] = {"before": before, "after": after, "swaps": swaps if isinstance(swaps, int) else len(swaps),
                 "stuck_cells": stuck if isinstance(stuck, int) else len(stuck), "start_wording_cells": len(sticky)}
    return sorted(sel2), sorted(pool2), sticky2


# ------------------------------------------------------------------ targets: C1 anchor, option_level, G18 (spec 5)

def own_target(m) -> bool:
    return (isinstance(m.get("teacher"), dict) and m.get("teacher_src") not in KD_SKIP_SRC) or bool(m.get("gold_probs"))


def merge_replay_targets(r, flag, probs, cnt: Counter):
    """C1 anchor (spec 5 / recipe 3): meta.teacher = C1's A5 probabilities and teacher_src = the second pass's flag
    ("c1_anchor": C1 right and p_top >= 0.8; "c1_anchor_protected": C1 right on an inv / equiv / complement unit or an
    attacked row / its clean partner). Rows with their own target keep it; a blend50-only teacher is no target and is
    stripped. Plus the licence join (spec 5) for rows without meta.licence."""
    m = dict(r.get("meta") or {})
    a = flag.get("anchor")
    if a and not own_target(m):
        p = probs[r["id"]]
        keys = ["yes", "no"] if r["qtype"] == "noul" else list(r["options"])
        t = {k: float(p.get(k, 0.0)) for k in keys}
        s = sum(t.values())
        if s <= 0:
            raise SystemExit(f"{r['id']}: C1 probabilities have no mass on the row's options")
        m["teacher"], m["teacher_src"] = {k: v / s for k, v in t.items()}, a
        cnt[a] += 1
    elif isinstance(m.get("teacher"), dict) and m.get("teacher_src") in KD_SKIP_SRC:
        m.pop("teacher"), m.pop("teacher_src")
        m["blend50_teacher_stripped"] = True
        cnt["blend50_stripped"] += 1
    if not m.get("licence"):
        s = r["source"]
        if s in REPLAY_LICENCE_JOIN:
            m["licence"] = REPLAY_LICENCE_JOIN[s]
        elif s.startswith("pg_"):
            m["licence"] = PROGRAM_LICENCE + " (build_pg.py)"
        else:
            cnt["licence_missing"] += 1
            return r | {"meta": m}
        cnt["licence_joined"] += 1
    return r | {"meta": m}


def detect_option_level(r) -> dict | None:
    """Replay rows whose options carry level numbers ('<n>: <label>' on every option, n consecutive from 0 or 1;
    spec 2.4 A1): {option text: level index}. Bare numbers (trivia answers, quantities) are not levels."""
    if r["qtype"] != "choice":
        return None
    o = r.get("options") or []
    ms = [_LEVEL.match(str(x)) for x in o]
    if len(o) < 2 or not all(ms) or len(set(o)) != len(o):
        return None
    nums = [int(x.group(1)) for x in ms]
    lo = min(nums)
    if lo not in (0, 1) or sorted(nums) != list(range(lo, lo + len(o))) or r.get("gold") not in o:
        return None
    return {x: n - lo for x, n in zip(o, nums)}


def train_target(r) -> list[float]:
    """The trainer's actual choice target over r['options'] (train_decoder.loss, recipe 3 values): gold_probs ->
    0.97 x normalized + 0.03 / K; else smoothed gold (0.05 / K + 0.95 on gold) mixed 0.5 / 0.5 with a dict teacher."""
    m, o = r.get("meta") or {}, r["options"]
    k = len(o)
    gp = m.get("gold_probs")
    if gp:
        q = [float(gp.get(x, 0.0)) for x in o]
        s = sum(q)
        return [0.97 * v / s + 0.03 / k for v in q]
    q = [LS / k] * k
    q[o.index(r["gold"])] += 1 - LS
    t = m.get("teacher")
    if isinstance(t, dict) and t and m.get("teacher_src") not in KD_SKIP_SRC:
        tq = [float(t.get(x, 0.0)) for x in o]
        s = sum(tq) or 1.0
        q = [(1 - KD) * a + KD * b / s for a, b in zip(q, tq)]
    return q


def g18_ok(r) -> bool:
    ol = r["meta"]["option_level"]
    e = sum(p * ol[x] for p, x in zip(train_target(r), r["options"]))
    return round(e) == ol[r["gold"]]          # Python round(): half to even, as the Score readout


def g18_lint(rows, block: str, cnt: dict) -> tuple[list, set]:
    """G18 on the final merged targets: fall back to smoothed gold (drop the KD / anchor part), else drop the row.
    Returns (rows, dropped ids). cnt[block][source] = [checked, fell_back, dropped]."""
    out, dropped = [], set()
    for r in rows:
        if not isinstance((r.get("meta") or {}).get("option_level"), dict):
            out.append(r)
            continue
        c = cnt.setdefault(block, {}).setdefault(r["source"], [0, 0, 0])
        c[0] += 1
        if g18_ok(r):
            out.append(r)
            continue
        m = {k: v for k, v in r["meta"].items() if k not in ("teacher", "teacher_src", "gold_probs")}
        r2 = r | {"meta": m | {"g18_fallback": "smoothed_gold"}}
        if g18_ok(r2):
            c[1] += 1
            out.append(r2)
        else:
            c[2] += 1
            dropped.add(r["id"])
    return out, dropped


# ------------------------------------------------------------------ new rows: own families, public, commits

def parent_names(par: list) -> list[str]:
    """Declared parents as strings for the deny-list query (B3: F10 / F11 declare dicts). A string stays as is; a dict
    gives its id or path plus every string in its source / parents / dataset fields, so nothing declared is hidden."""
    out = []
    for x in par or []:
        if isinstance(x, str):
            out.append(x)
        elif isinstance(x, dict):
            for k in ("id", "path", "name"):
                if isinstance(x.get(k), str) and x[k]:
                    out.append(x[k])
                    break
            for k in ("source", "parents", "dataset", "datasets"):
                v = x.get(k)
                out += [y for y in (v if isinstance(v, list) else [v]) if isinstance(y, str) and y]
        elif x is not None:
            out.append(json.dumps(x, sort_keys=True))
    return out


def manifest_parents(man: dict, source: str | None = None) -> list | None:
    """Declared parents (3.H.1): family manifests 'parents'; public manifests datasets.<source>.parents or
    parents_declared.<source>. None = not declared (G1 failure)."""
    if source is not None:
        d = (man.get("datasets") or {}).get(source)
        if isinstance(d, dict) and isinstance(d.get("parents"), list):
            return d["parents"]
        pd = man.get("parents_declared") or {}
        if isinstance(pd, dict) and isinstance(pd.get(source), list):
            return pd[source]
        return None
    p = man.get("parents")
    return p if isinstance(p, list) else None


class Pool:
    """A block's unused whole units, for refills after drops (spec 5: replay from the same source's trimmed-off margin;
    2.1 / 4.2: own and commit rows from unselected units of the same crowd stratum and bin; 3: public rows from the
    same source's reserve). unit_of: row id -> unit key (a row id with no unit is its own unit); group_row: row ->
    refill group (source; '' for own / commit);
    cands: {group: [unit keys, seeded order]}; raw_of(u): the unit's source rows (for keys); rows_of(u, tally): its
    training rows (targets merged, _block set; target counts into tally); keys_of(row): row keys for the match tiers
    (fine -> coarse); rels_of(ids): relations inside those rows; tried: units already used or refused."""

    def __init__(self, block, unit_of, group_row, cands, raw_of, rows_of, keys_of, rels_of, sources=()):
        self.block, self.unit_of, self.group_row, self.cands = block, unit_of, group_row, cands
        self.raw_of, self.rows_of, self.keys_of, self.rels_of = raw_of, rows_of, keys_of, rels_of
        self.tried: set = set()
        self.sources = set(sources)


def own_keys(r, b) -> tuple:
    """Refill tiers for own / commit rows: (crowd stratum, label class), crowd stratum, (commit type|view, bin)."""
    s = cs.stratum(r, b)
    return ((s, cs.label_class(r)), s, (cs.commit_group(r), b))


def family_block(ilog, fam, target, final, rep, probs, a34=False):
    """One family's selected rows + relations + refill pool. --final: the crowd selection file (crowd_select.py
    select) must exist, match the current candidates file and target, and pass every selection check (G9, 2.1).
    --dry-run without it: provisional selection (no crowd; counts only). A relation file that does not match the
    MANIFEST is refused (SystemExit in --final; the family is left out with a problem line in --dry-run)."""
    try:
        rows, rels = cs.load_family(ilog, fam)
    except SystemExit as e:
        if final:
            raise
        probs.append(f"{fam} refused: {e}")
        rep.setdefault("own", {})[fam] = {"refused": str(e), "rows": 0, "target": target}
        return [], [], None, None
    units = cs.units_of(rows, rels)
    f = cs.fam_files(fam)
    sf = cs.OUT / f"select_{fam}.json"
    info = {"candidates": len(rows), "target": target, "relation_file": f["rel"].name if f["rel"] else None,
            "relations_loaded": len(rels)}
    s = None
    if sf.exists():
        s = ilog.json(sf)
        if s.get("candidates_sha256") != sha256_file(f["cand"]):
            if final:
                raise SystemExit(f"{fam}: select_{fam}.json was made on another candidates file (re-run the crowd)")
            s = None
            info["selection"] = "stale crowd selection ignored (provisional)"
    if s is None:
        if final:
            raise SystemExit(f"{fam}: no crowd selection file {sf.name} (G9 not run)")
        res = cs.select_any(rows, units, None, target, key=fam)
        chosen = {rows[i]["id"] for u in res["sel"] for i in units[u]}
        info |= {"selection": info.get("selection", "provisional (no crowd yet)"), "report": res["report"]}
        pg, bins = {}, {r["id"]: "na" for r in rows}
    else:
        chosen = set(s["selected_ids"])
        pg, bins = s["crowd_pg"], s["difficulty_bin"]
        info |= {"selection": "crowd", "report": s["report"]}
        sr = s.get("report") or {}
        bad = [k for k, v in (sr.get("checks") or {}).items() if v is not True]
        ex = s.get("exclude_ids")
        if (a34 and bad == ["total_eq_target"] and isinstance(ex, dict) and (ex.get("units_removed") or 0) > 0
                and len(chosen) < target):
            # PREREG A34 (e): short of its base target ONLY because G13 removed units (every other check passes):
            # the family enters with its realised selected rows; the shortfall lowers the total (A34 c)
            info["a34_e"] = {"selected_rows": len(chosen), "target": target, "short": target - len(chosen),
                             "failed_checks": bad, "exclude_ids": {k: v for k, v in ex.items() if k != "files"},
                             "exclude_files": len(ex.get("files") or [])}
        elif sr.get("pass") is not True or bad:
            probs.append(f"{fam}: crowd selection fails its checks (G9 / 2.1): {bad or ['pass is not true']}")
        if s.get("target") != target:
            probs.append(f"{fam}: crowd selection target {s.get('target')} != mixer target {target}")
    out = []
    for r in rows:
        if r["id"] in chosen:
            m = dict(r.get("meta") or {})
            if pg:
                m["crowd_pg"], m["difficulty_bin"] = pg[r["id"]], bins[r["id"]]
            out.append(r | {"meta": m})
    keep_rels = [x for x in rels if x["a"] in chosen and x["b"] in chosen]
    man = ilog.json(f["manifest"]) if f["manifest"].exists() else {}
    parents = manifest_parents(man)
    qc = ilog.json(f["qc"]) if f["qc"].exists() else {}
    info |= {"rows": len(out), "relations": len(keep_rels), "qc_pass": qc.get("pass") is True,
             "parents_declared": parents is not None}
    if parents is None:
        probs.append(f"{fam}: MANIFEST declares no parents (G1, 3.H.1; the deny-list check cannot run on it)")
    rep.setdefault("own", {})[fam] = info
    return out, keep_rels, parents, own_pool(fam, rows, rels, units, chosen, bins, pg)


def rel_index(rels) -> dict:
    by = defaultdict(list)
    for x in rels:
        by[x["a"]].append(x)
    return by


def own_pool(fam, rows, rels, units, chosen, bins, pg) -> Pool:
    """Unselected whole units of an own / commit block: never an all-easy unit thinned out by the seeded 30% keep
    (spec 2.1, the selection's own rule and key), never a unit without a crowd bin; seeded order."""
    uid = {}
    for u, x in enumerate(units):
        for i in x:
            uid[rows[i]["id"]] = u
    used = {uid[i] for i in chosen if i in uid}
    cands = []
    for u, x in enumerate(units):
        if u in used or (pg and any(rows[i]["id"] not in pg for i in x)):
            continue
        key = f"COMMIT|{cs.commit_group(rows[x[0]])}" if fam == "COMMIT" else fam
        if pg and cs.easy_thinned(rows, [x], bins, key):
            continue
        cands.append(u)
    cands.sort(key=lambda u: h64(SEED, fam, "refill", rows[units[u][0]]["id"]))
    ri = rel_index(rels)
    srcs = {r["source"] for r in rows}

    def rows_of(u, tally=None):
        out = []
        for i in units[u]:
            m = dict(rows[i].get("meta") or {})
            if pg:
                m["crowd_pg"], m["difficulty_bin"] = pg[rows[i]["id"]], bins[rows[i]["id"]]
            out.append(rows[i] | {"meta": m, "_block": fam})
        return out
    return Pool(fam, uid, lambda r: "", {"": cands}, lambda u: [rows[i] for i in units[u]], rows_of,
                lambda r: own_keys(r, bins.get(r["id"], "na")),
                lambda ids: [x for a in ids for x in ri.get(a, []) if x["b"] in ids], srcs)


def replay_pool(rows_r, lt, units, pool, rels_r, flags, c1p) -> Pool:
    """The trimmed-off margin after E2 (whole relation units, kept by the second pass, no old-slice clash), per
    source in the sampler's own seeded stratified order (replay_sample.unit_order)."""
    rs = rs_mod()
    uid = {lt[i]["id"]: u for u in range(len(units)) for i in units[u]["rows"]}
    by_src = defaultdict(list)
    for u in pool:
        by_src[units[u]["source"]].append(u)
    cands = {s: rs.unit_order(lt, units, us) for s, us in by_src.items()}
    ri = rel_index(rels_r)

    def rows_of(u, tally):
        out = []
        for i in units[u]["rows"]:
            r = merge_replay_targets(rows_r[i], flags[rows_r[i]["id"]], c1p, tally)
            ol = None if "option_level" in r["meta"] else detect_option_level(r)
            if ol:
                r["meta"]["option_level"] = ol
                tally["option_level:" + r["source"]] += 1
            out.append(r | {"_block": "replay"})
        return out

    def keys_of(r):
        g = r["gold"] if r["qtype"] == "noul" else "-"
        return ((r["qtype"], r["role"], g), (r["qtype"], r["role"]), "*")
    return Pool("replay", uid, lambda r: r["source"], cands, lambda u: [rows_r[i] for i in units[u]["rows"]], rows_of,
                keys_of,
                lambda ids: [x for a in ids for x in ri.get(a, []) if x["b"] in ids])


def public_pool(reserve) -> Pool:
    """Public reserve rows, per source, seeded order (one row = one unit)."""
    by = {r["id"]: r for r in reserve}
    cands = defaultdict(list)
    for r in sorted(reserve, key=lambda r: h64(SEED, "reserve", r["id"])):
        cands[r["source"]].append(r["id"])
    return Pool("public", {}, lambda r: r["source"], dict(cands), lambda u: [by[u]],
                lambda u, tally=None: [by[u] | {"_block": "public"}], lambda r: ((r["qtype"],), "*"), lambda ids: [])


def public_block(ilog, expected: int, rep, probs, builders=None):
    """builders: the public builders named in --include (None = all three; a builder left out is a missing source:
    no rows, no reserve, no manifest)."""
    base = LEAN / "c_src/public"
    rows, reserve, parents = [], [], {}
    inc = (lambda rel: True) if builders is None else (lambda rel: rel.split("/")[0] in builders)
    for rel in PUBLIC_FILES:
        if inc(rel):
            rows += ilog.jsonl(base / rel)
    for rel in PUBLIC_RESERVE:
        if inc(rel) and (base / rel).exists():
            reserve += ilog.jsonl(base / rel)
    srcs = {r["source"] for r in rows} | {r["source"] for r in reserve}
    for m in sorted(base.glob("public-*/manifest_public*.json")) + sorted(base.glob("public-*/out/manifest.json")):
        if not inc(str(m.relative_to(base))):
            continue
        man = ilog.json(m)
        for src in srcs:
            p = manifest_parents(man, src)
            if p is not None:
                parents[src] = p
    missing = sorted(srcs - set(parents))
    rep["public"] = {"rows": len(rows), "expected": expected, "reserve": len(reserve), "builders": sorted(
                     {r.split("/")[0] for r in PUBLIC_FILES if inc(r)}),
                     "by_source": dict(Counter(r["source"] for r in rows)), "sources_without_parents": missing}
    if missing:
        probs.append(f"public sources without declared parents (G1, 3.H.1): {missing}")
    return rows, reserve, parents


def commit_block(ilog, target, final, rep, probs, included=True):
    if not included:
        rep["commit"] = {"rows": 0, "expected": target, "status": "not in --include (left out as a missing source)"}
        return [], [], None, None
    if "COMMIT" not in cs.available(["COMMIT"]):
        rep["commit"] = {"rows": 0, "expected": target, "status": "no c_src/COMMIT/out/candidates_r1.jsonl yet"}
        return [], [], None, None
    rows, rels, parents, pool = family_block(ilog, "COMMIT", target, final, rep, probs)
    rep["commit"] = rep["own"].pop("COMMIT")
    return rows, rels, parents, pool


# ------------------------------------------------------------------ guards: deny-list, licence, held-out styles, G13

ONET_PARENT = "gd_onet_occupation (O*NET occupation titles; persona seeds via packs; role titles only)"


def denylist_query(new_rows, parents: dict) -> dict:
    """One query entry per new-row source (names: source + meta.dataset values; parents: the builder's declared list,
    plus O*NET when the rows carry persona seeds) and one per real-text source dataset (meta.text_source.dataset; a
    leaf, parents []). A source whose builder declared no parents gets NO 'parents' key, so denylist.py's own G1
    refusal ('no parents field') applies to it; `parents` holds declared lists only."""
    q = {}
    for r in new_rows:
        m = r.get("meta") or {}
        e = q.setdefault(r["source"], {"names": {r["source"]}, "datasets": set(), "parents": set(), "emits_rows": True})
        if m.get("dataset"):
            e["names"].add(str(m["dataset"]))
        if m.get("persona_seed"):
            e["parents"].add(ONET_PARENT)
        ts = m.get("text_source")
        if isinstance(ts, dict) and ts.get("dataset"):
            q.setdefault("text:" + str(ts["dataset"]), {"names": {str(ts["dataset"])}, "datasets": set(),
                                                        "parents": set(), "emits_rows": True})
    out = {}
    for k, v in sorted(q.items()):
        e = {"names": sorted(v["names"]), "datasets": sorted(v["datasets"]), "emits_rows": True}
        if k.startswith("text:"):
            e["parents"] = []
        elif isinstance(parents.get(k), list):
            e["parents"] = sorted(v["parents"] | set(parent_names(parents[k])))
        out[k] = e
    return out


def run_denylist(ilog, query: dict, rep, final=False) -> set:
    """denylist.py check in its own process (3.H.2: the mixer refuses a denied source or text_source.dataset).
    Returns the denied query keys (verdict deny or no_new_rows: these rows are new rows). --final sends every entry
    (an undeclared-parents entry makes denylist.py refuse, G1); --dry-run sends only entries with declared parents
    and lists the others as not checked (each is also a problem line from its block)."""
    WORK.mkdir(parents=True, exist_ok=True)
    qp, vp = WORK / "denylist_query_mix_r1.json", WORK / "denylist_verdicts_mix_r1.json"
    vp.unlink(missing_ok=True)
    undeclared = sorted(k for k, v in query.items() if "parents" not in v)
    if not final:
        query = {k: v for k, v in query.items() if "parents" in v}
    write_json(qp, {"purpose": "C round-1 mixer (C_DATA_SPEC.md v4 3.H.2): every new-row source and real-text source",
                    "datasets": query})
    ilog.record(DENYLIST)
    p = subprocess.run([str(PY), str(LEAN / "c_src/common/denylist.py"), "check", "--query", str(qp), "--out", str(vp),
                        "--run", "mixer_r1", "--denylist", str(DENYLIST)], capture_output=True, text=True,
                       cwd=str(LEAN), timeout=600)
    if p.returncode not in (0, 3) or not vp.exists():
        raise SystemExit(f"denylist.py check failed (exit {p.returncode}): {p.stderr[-400:]}")
    ver = ilog.json(vp)["verdicts"]
    denied = {k for k, v in ver.items() if v.get("verdict") in ("deny", "no_new_rows")}
    rep["denylist_new"] = {"checked": len(ver), "denied": sorted(denied),
                           "verdicts": dict(Counter(v.get("verdict") for v in ver.values())),
                           "not_checked_parents_undeclared": undeclared}
    return denied


def replay_denylist_check(ilog, rows, rep):
    ver = ilog.json(REPLAY_VERDICTS)["verdicts"]
    srcs = Counter(r["source"] for r in rows)
    v = {s: (ver.get(s) or {}).get("verdict") for s in srcs}
    bad = sorted(s for s, x in v.items() if x is None or x == "drop")
    rep["denylist_replay"] = {"sources": len(srcs), "verdicts": dict(Counter(v.values())), "refused": bad}
    return bad


def licence_ok(r) -> bool:
    return bool(str((r.get("meta") or {}).get("licence") or "").strip())


def refuse_held_out(ilog, blocks: dict, rep):
    """formats-1 fmt1.pool.refuse_held_out on every training shard (held-out style ids, sampler S5)."""
    sys.path.insert(0, str(LEAN / "c_src/formats/formats-1"))
    from fmt1 import pool
    ilog.record(LEAN / "c_src/formats/formats-1/fmt1/pool.py")
    out = {}
    for name, rows in blocks.items():
        # own and commit rows use formats-1 style ids: strict (an unknown or misspelled id is refused). Replay rows
        # carry no style; public builders use their own style ids (e.g. sq_s1, markdown), which strict would refuse.
        strict = name.startswith("F") or name == "COMMIT"
        try:
            out[name] = pool.refuse_held_out(rows, strict_unknown=strict) | {"strict_unknown": strict}
        except pool.HeldOutStyleError as e:
            out[name] = {"refused": str(e).split("; first ids")[0], "strict_unknown": strict}
        if strict:
            out[name]["rows_without_format_style"] = sum(1 for r in rows if not (r.get("meta") or {}).get("format_style"))
    rep["fmt1_refuse_held_out"] = out
    return [n for n, v in out.items() if "refused" in v or v.get("rows_without_format_style")]


# ------------------------------------------------------------------ spec 10 rules S7: training rows vs the mix-tuning dev

PUBLIC_DEV = ("public-1/out/public1_mtdev.jsonl", "public-2/out/dev_mt_r1.jsonl", "public-3/out/public3_mtdev.jsonl")
DEV_EXTRA = ("probe_hardneg.jsonl",)          # other dev parts in a block's out/ (F5 hard-negation probe)


def dev_items(ilog, blocks) -> dict:
    """{block: [(dev row, pack_check)]}: each own / commit block's mixdev_S5.jsonl (held-out packs: pack_check) and
    other dev parts, the public dev splits, and any F14 hold-out family file (never trained)."""
    out = defaultdict(list)
    for b in blocks:
        d = cs.fam_dir(b) / "out"
        if (d / "mixdev_S5.jsonl").exists():
            out[b] += [(r, True) for r in ilog.jsonl(d / "mixdev_S5.jsonl")]
        for n in DEV_EXTRA:
            if (d / n).exists():
                out[b] += [(r, False) for r in ilog.jsonl(d / n)]
    for rel in PUBLIC_DEV:
        p = LEAN / "c_src/public" / rel
        if p.exists():
            out["public"] += [(r, False) for r in ilog.jsonl(p)]
    f14 = LEAN / "c_src/F14/out"
    for p in sorted(f14.glob("*.jsonl")) if f14.exists() else []:
        out["F14"] += [(r, False) for r in ilog.jsonl(p)]
    return out


class HeldOut:
    """Spec 10 S7 + held-out packs / F14: a training row may not share a group_id, normalized state or structure_hash
    with ANY dev item, nor a domain_pack with its own block's mixdev_S5 (held-out packs are chosen per family; packs
    are shared across families by design), nor be an F14 row. A normalized state shared by >= 2 distinct dev group_ids
    is a template (e.g. public sarcasm's '{"task": "headline review", ...}' header), not an item's text (S7 says
    "normalized text"): it is not matched on, and is reported."""

    def __init__(self, dev: dict, rs):
        self.rs, self.keys, self.packs = rs, {"group_id": {}, "state": {}, "structure_hash": {}}, defaultdict(set)
        self.n = {b: len(v) for b, v in dev.items()}
        groups = defaultdict(set)
        for b, items in dev.items():
            for r, pack_check in items:
                for k, v in self.row_keys(r).items():
                    if v:
                        self.keys[k].setdefault(v, b)
                if self.row_keys(r)["state"]:
                    groups[self.row_keys(r)["state"]].add(r.get("group_id") or r.get("id"))
                if pack_check and (r.get("meta") or {}).get("domain_pack"):
                    self.packs[b].add(r["meta"]["domain_pack"])
        self.template_states = {s for s, g in groups.items() if len(g) >= 2}
        for s in self.template_states:
            self.keys["state"].pop(s, None)

    def row_keys(self, r) -> dict:
        m = r.get("meta") or {}
        st = str(r.get("state") or "")
        return {"group_id": r.get("group_id"), "state": self.rs.norm_state(st) if st.strip() else None,
                "structure_hash": m.get("structure_hash")}

    def clash(self, r) -> list[str]:
        m = r.get("meta") or {}
        out = [k for k, v in self.row_keys(r).items() if v and v in self.keys[k]]
        if m.get("domain_pack") and m["domain_pack"] in self.packs.get(r["_block"], ()):
            out.append("domain_pack")
        if m.get("family") == "F14" or "F14" in str(r.get("source")):
            out.append("F14")
        return out

    def check(self, rows, rep) -> list[str]:
        hits = defaultdict(Counter)
        for r in rows:
            for k in self.clash(r):
                hits[r["_block"]][k] += 1
        tmpl = Counter(r["_block"] for r in rows if self.row_keys(r)["state"] in self.template_states)
        rep["s7_dev_overlap"] = {"dev_items": self.n, "held_out_packs": {b: len(v) for b, v in self.packs.items()},
                                 "training_rows_hit": {b: dict(c) for b, c in hits.items()},
                                 "template_states_not_matched": len(self.template_states),
                                 "training_rows_on_template_states": dict(tmpl)}
        return [f"S7 / held-out: training rows share keys with the mix-tuning dev: { {b: dict(c) for b, c in hits.items()} }"] \
            if hits else []


COMMIT_SIDECARS = (DATA / "c_parts/commit_meta.jsonl",)
_HELD_REPOS = re.compile(r"held.?out.?repo", re.I)


def commit_repo_check(ilog, rows, rep) -> list[str]:
    """Spec 4.2 / 10: no training commit row from the 30 held-out repo groups of the mix-tuning dev. Repo groups come
    from the commit sidecars (G0 1.7: data/c_parts/commit_meta.jsonl, and out/*.sidecar.jsonl), keyed by row id; the
    held-out set = repo groups of the commit dev items plus any MANIFEST list under a 'held-out repo' key."""
    tr = [r for r in rows if r["_block"] == "COMMIT"]
    if not tr:
        return []
    d = cs.fam_dir("COMMIT") / "out"
    repo = {}
    for p in [*COMMIT_SIDECARS, *sorted(d.glob("*.sidecar.jsonl"))]:
        if p.exists():
            for x in ilog.jsonl(p):
                if x.get("id") and x.get("repo_group"):
                    repo[x["id"]] = x["repo_group"]
    held = set()
    if (d / "mixdev_S5.jsonl").exists():
        held |= {repo[r["id"]] for r in ilog.jsonl(d / "mixdev_S5.jsonl") if r["id"] in repo}
    man = ilog.json(d / "MANIFEST.json") if (d / "MANIFEST.json").exists() else {}

    def visit(x):
        if isinstance(x, dict):
            for k, v in x.items():
                if _HELD_REPOS.search(str(k)) and isinstance(v, list):
                    held.update(map(str, v))
                visit(v)
        elif isinstance(x, list):
            for v in x:
                visit(v)
    visit(man)
    unknown = [r["id"] for r in tr if r["id"] not in repo]
    hit = [r["id"] for r in tr if repo.get(r["id"]) in held]
    rep["commit_held_out_repos"] = {"held_out_repo_groups": len(held), "training_rows": len(tr),
                                    "rows_without_repo_group": len(unknown), "rows_in_held_out_repos": len(hit)}
    p = []
    if not held:
        p.append("commit: no held-out repo set found (dev sidecar / MANIFEST); the 30-repo split cannot be checked")
    if unknown:
        p.append(f"commit: {len(unknown)} training rows without a repo_group in the sidecars, e.g. {unknown[:3]}")
    if hit:
        p.append(f"commit: {len(hit)} training rows from held-out repos, e.g. {hit[:3]}")
    return p


# ------------------------------------------------------------------ QC records tied to the files mixed

SHA_HEX = re.compile(r"^[0-9a-f]{12,64}$")
_QC_HISTORY = re.compile(r"previous|archive|history|^r1_0|^v10", re.I)


def qc_recorded_shas(qc: dict, names) -> dict:
    """{file name: [sha256 values (full or >= 12-hex prefixes) the QC record gives for that file]}, from any layout:
    {name: sha}, {name: {sha256 | input_sha256}}, {path | file | input: name, sha256}. History subtrees skipped."""
    names = set(names)
    out = defaultdict(list)

    def add(name, v):
        if isinstance(v, str) and SHA_HEX.match(v):
            out[name].append(v)

    def visit(x, key=""):
        if isinstance(x, list):
            for v in x:
                visit(v, key)
            return
        if not isinstance(x, dict):
            return
        if Path(str(key)).name in names:
            for k in ("sha256", "input_sha256"):
                add(Path(str(key)).name, x.get(k))
        for k in ("path", "file", "input"):
            if isinstance(x.get(k), str) and Path(x[k]).name in names:
                for kk in ("sha256", "input_sha256"):
                    add(Path(x[k]).name, x.get(kk))
        for k, v in x.items():
            if _QC_HISTORY.search(str(k)):
                continue
            if isinstance(v, str) and Path(str(k)).name in names:
                add(Path(str(k)).name, v)
            visit(v, k)
    visit(qc)
    return out


def qc_binding(qc: dict, files: dict) -> list[str]:
    """Problems unless the QC record gives a full sha256 for every mixed file ({name: path}) and every sha it records
    for those files (full or prefix) equals the file on disk (a stale pass after a regeneration is refused)."""
    rec = qc_recorded_shas(qc, files)
    p = []
    for name, path in files.items():
        disk = sha256_file(path)
        got = rec.get(name, [])
        if not any(len(x) == 64 for x in got):
            p.append(f"no full sha256 recorded for {name}")
        if any(not disk.startswith(x) for x in got):
            p.append(f"recorded sha256 of {name} differs from the file on disk (stale QC)")
    return p


def decontam_drop_ids(ilog, files) -> tuple[set, list]:
    """G13 hook: the orchestrator's counts-only decontamination logs (logs/decontam_counts/*.json) list training ids
    to drop (keys 'drop_ids' / 'training_ids_to_drop' / 'ids'); the mixer drops their whole units."""
    ids, used = set(), []
    for f in files or []:
        d = ilog.json(f)
        got = next((d[k] for k in ("drop_ids", "training_ids_to_drop", "ids") if isinstance(d.get(k), list)), None)
        if got is None:
            raise SystemExit(f"{f}: no drop id list (drop_ids / training_ids_to_drop / ids)")
        ids |= set(map(str, got))
        used.append({"file": str(f), "ids": len(got)})
    return ids, used


# ------------------------------------------------------------------ G15: units, tokens, loader rows

TOKENIZER = Path.home() / ".cache/huggingface/hub/models--Qwen--Qwen3.5-4B/snapshots" / \
    "851bf6e806efd8d0a36b00ddf55e13ccb7b8cd0a/tokenizer.json"
TOKENIZER_SHA = "5f9e4d4901a92b997e463c1f46055088b6cca5ca61a6522d1b9f64c4bb81cb42"


_TOK: dict = {}


def token_counts(ilog, rows, chunk=2000) -> list[int]:
    """Real Qwen3.5 tokenizer on the rendered training prompt (cygnet system + schema_branch_mark user message, given
    option order). The layout repeats the instructions, so they count twice (A16.1 g)."""
    from tokenizers import Tokenizer
    import decoder_io as dio
    ilog.record(TOKENIZER)
    if "tok" not in _TOK:
        if sha256_file(TOKENIZER) != TOKENIZER_SHA:
            raise SystemExit("tokenizer.json is not the pinned Qwen3.5-4B snapshot")
        tok = Tokenizer.from_file(str(TOKENIZER))
        U = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"   # decoder_io.Readout's wide labels: single-token two-letter strings
        _TOK["tok"] = tok
        _TOK["wide"] = [w for w in (a + b for a in U for b in U) if len(tok.encode(w, add_special_tokens=False).ids) == 1]
    tok, wide = _TOK["tok"], _TOK["wide"]
    saved = (dio.STYLE, dio.LAYOUT, dio.WIDE)
    dio.WIDE = list(dio.LETTERS) + wide[: dio.MAX_OPTIONS - 26]
    dio.STYLE, dio.LAYOUT = "cygnet", "schema_branch_mark"
    try:
        out = []
        for i in range(0, len(rows), chunk):
            texts = [dio.CYGNET_SYSTEM + "\n" + dio.user_msg(r) for r in rows[i:i + chunk]]
            out += [len(e.ids) for e in tok.encode_batch(texts)]
        return out
    finally:
        dio.STYLE, dio.LAYOUT, dio.WIDE = saved


def unit_check(rows, rels, ntok: dict, rep) -> list[str]:
    """G15 relation units: every relation pair shares one call_id; a call_id unit has <= 3 rows, <= 2 when any row has
    >= 2,000 tokens; no call_id spans two blocks."""
    cid = {r["id"]: r["call_id"] for r in rows}
    by = defaultdict(list)
    for r in rows:
        by[r["call_id"]].append(r)
    split = [x for x in rels if cid.get(x["a"]) != cid.get(x["b"])]
    dangling = [x for x in rels if x["a"] not in cid or x["b"] not in cid]
    big = [c for c, u in by.items() if len(u) > 3]
    long2 = [c for c, u in by.items() if len(u) > 2 and any(ntok.get(r["id"], 0) >= LONG_TOK for r in u)]
    span = [c for c, u in by.items() if len({r["_block"] for r in u}) > 1]
    rep["g15_units"] = {"units": len(by), "size_hist": dict(sorted(Counter(len(u) for u in by.values()).items())),
                        "relations": dict(Counter(x["type"] for x in rels)), "relation_pairs_split_call_id": len(split),
                        "dangling_relations": len(dangling), "units_over_3": len(big), "long_units_over_2": len(long2),
                        "call_id_spans_blocks": len(span),
                        "units_over_3_by_block": dict(Counter(by[c][0]["_block"] for c in big)),
                        "long_units_over_2_by_block": dict(Counter(by[c][0]["_block"] for c in long2))}
    probs = []
    for k in ("relation_pairs_split_call_id", "dangling_relations", "units_over_3", "long_units_over_2",
              "call_id_spans_blocks"):
        if rep["g15_units"][k]:
            probs.append(f"G15 {k} {rep['g15_units'][k]}")
    return probs


def split_replay_call_ids(rows, rels, ntok, rep):
    """Spec 2.1 / G15 on replay rows: C1's golden_train groups some rows under one call_id that are NOT joined by a
    relation (e.g. a complement pair + an inv pair of the same item: 4-8 rows). A group over the cap (> 3 rows, > 2
    with a >= 2,000-token row) is split into its relation components (complement / equiv / inv edges), each with its
    own call_id '<call_id>~<k>', so every relation pair keeps one call_id ("contrast twins with no relation term get
    their own call_id"). Nothing else changes. Relation components never exceed 3 rows in the round-1 draw."""
    by = defaultdict(list)
    for i, r in enumerate(rows):
        if r["_block"] == "replay":
            by[r["call_id"]].append(i)
    adj = defaultdict(set)
    for x in rels:
        adj[x["a"]].add(x["b"])
        adj[x["b"]].add(x["a"])
    groups = units = 0
    for c, idx in by.items():
        cap = 2 if any(ntok[rows[i]["id"]] >= LONG_TOK for i in idx) else 3
        if len(idx) <= cap:
            continue
        pos = {rows[i]["id"]: i for i in idx}
        seen, comps = set(), []
        for rid in pos:
            if rid in seen:
                continue
            stack, comp = [rid], []
            while stack:
                x = stack.pop()
                if x in seen:
                    continue
                seen.add(x)
                comp.append(x)
                stack += [y for y in adj[x] if y in pos and y not in seen]
            comps.append(comp)
        for k, comp in enumerate(comps):
            for rid in comp:
                rows[pos[rid]] = rows[pos[rid]] | {"call_id": f"{c}~{k}"}
        groups += 1
        units += len(comps)
    rels, long_split = split_long_components(rows, rels, ntok)
    rep["replay_call_id_split"] = {"groups_split": groups, "units_after": units} | long_split
    return rels


REL_PRIORITY = {"inv": 0, "complement": 1, "equiv": 2}


def split_long_components(rows, rels, ntok):
    """A replay relation unit of 3 rows with a >= 2,000-token row breaks the long-unit cap (<= 2 rows, spec 6 / G15).
    Keep its highest-priority pair (inv > complement > equiv; security first, as the protected-skill order) under the
    call_id, give the third row its own call_id, and drop that row's relation edges inside the unit (the F5 3+1 split
    pattern). New-row units are never changed here (builders must comply; unit_check reports them)."""
    by = defaultdict(list)
    for i, r in enumerate(rows):
        if r["_block"] == "replay":
            by[r["call_id"]].append(i)
    drop, n = set(), 0
    for c, idx in by.items():
        if len(idx) <= 2 or not any(ntok[rows[i]["id"]] >= LONG_TOK for i in idx):
            continue
        ids = {rows[i]["id"]: i for i in idx}
        inner = sorted((x for x in rels if x["a"] in ids and x["b"] in ids),
                       key=lambda x: (REL_PRIORITY.get(x["type"], 9), x["a"], x["b"]))
        keep = {inner[0]["a"], inner[0]["b"]} if inner else set(list(ids)[:2])
        for k, rid in enumerate(r for r in ids if r not in keep):
            rows[ids[rid]] = rows[ids[rid]] | {"call_id": f"{c}~L{k}"}
            drop |= {(x["a"], x["b"], x["type"]) for x in inner if rid in (x["a"], x["b"])}
        n += 1
    kept = [x for x in rels if (x["a"], x["b"], x["type"]) not in drop]
    return kept, {"long_units_split": n, "relations_dropped_long_split": len(rels) - len(kept)}


def spec6_bin(r, ntok) -> bool:
    """Spec 6's first drop: an F13 or 3B (long public) row in the 6-7.9K bin."""
    return P1_LO <= ntok[r["id"]] <= MAX_TOK and (r["_block"] == "F13" or
                                                   (r.get("meta") or {}).get("block") in ("3B",) or
                                                   r["source"] == "c_pub_quality")


def token_cap(rows, ntok, rep, spec6=True) -> tuple[set, list]:
    """Spec 6 token cap on new rows: >= 2,000-token rows <= 9% of new rows and <= 30% of new-row tokens (a problem line
    when not met); rows over 7,900 tokens are returned for dropping (G15). spec6=True applies spec 6's own sentence on
    the rows given ('if the real count passes 30%, the mixer drops F13 and 3B rows from the 6-7.9K bin first'): whole
    call_id units holding such a row, seeded hash order, only while long tokens > 30%. finish() calls it with
    spec6=False (measure only): there the rule runs inside cap_trim() after the refills (PREREG A28 b: phase p1, whole
    units, every guard kept, freed rows refilled under A26 b), followed by the closed-form A28 trim."""
    new = [r for r in rows if r["_block"] != "replay"]
    over = [r["id"] for r in rows if ntok[r["id"]] > MAX_TOK]
    drop = set()
    def shares(rs_):  # noqa: E306
        t = sum(ntok[r["id"]] for r in rs_ if r["id"] not in drop)
        n = sum(1 for r in rs_ if r["id"] not in drop)
        lt = sum(ntok[r["id"]] for r in rs_ if r["id"] not in drop and ntok[r["id"]] >= LONG_TOK)
        ln = sum(1 for r in rs_ if r["id"] not in drop and ntok[r["id"]] >= LONG_TOK)
        return ln / max(1, n), lt / max(1, t), ln, n
    before = shares(new)
    if spec6 and before[1] > LONG_TOK_SHARE:
        units = defaultdict(list)
        for r in new:
            units[(r["_block"], r.get("call_id") or r["id"])].append(r["id"])
        cand = {(r["_block"], r.get("call_id") or r["id"]) for r in new if spec6_bin(r, ntok)}
        for u in sorted(cand, key=lambda u: h64(SEED, "tokcap", *u)):
            if shares(new)[1] <= LONG_TOK_SHARE:
                break
            drop.update(units[u])
    after = shares(new)
    rep["token_cap"] = {"new_rows": after[3], "long_rows": after[2], "long_row_share": round(after[0], 4),
                        "long_token_share": round(after[1], 4), "before": [round(before[0], 4), round(before[1], 4)],
                        "dropped_for_cap": len(drop), "rows_over_7900": len(over),
                        "max_tokens": max(ntok.values()) if ntok else 0,
                        "new_tokens_total": sum(ntok[r["id"]] for r in new if r["id"] not in drop)}
    probs = []
    if after[0] > LONG_ROW_SHARE:
        probs.append(f"token cap: long rows {after[0]:.3f} > 9% of new rows")
    if after[1] > LONG_TOK_SHARE:
        probs.append(f"token cap: long tokens {after[1]:.3f} > 30% of new-row tokens")
    if over:
        probs.append(f"G15: {len(over)} rows over {MAX_TOK} tokens")
    return drop | set(over), probs


# ------------------------------------------------------------------ PREREG A28 (b): meeting the spec 6 token cap

A34_REPLAY_X = 1.5      # PREREG A34 (c): replay = floor(1.5 x new rows), i.e. 60% of the total
A26_ROOM = 1.5          # A26 (b): a passed family holds at most 1.5x its own target
OWN_MAX = 0.12          # spec 2.1: max share of own rows per family, judged on the realised own rows
P1_LO = 6000            # spec 6: "the 6-7.9K bin"
G10_TOL = 0.02          # G10: yes rate 50 +/- 2 per family and per cell of >= 50 rows; longest-is-gold 1/k +/- 2 pp
CARD_MAX, CARD_WORDINGS, DEF_STYLES = 128, 5, 3     # spec 2.1: rows per card, wordings per card, styles per family
FIXED = ("public", "COMMIT")    # A26 (b) "public rows stay as specced"; spec 3.2 / 4.2 per-dataset / per-type counts
A28_TRACE = None        # tests: a list -> every committed trim / refill move is appended (phase, block, kind, units)
COST = {"blk": 0, "bins": 1, "cell": 2, "card": 3, "cardw": 4, "defs": 5, "ord": 6, "g10": 7, "pos": 8, "g9": 9}
# Spec 2.1 quota shares of an own block. (lo, hi): a band, each edge its own rule (an edge the pre-trim mix met must
# hold; an edge it missed may not be missed by more). (p, p): a point value with no stated band ("about 5%" attack
# twins and swapped names, F10's 40% / 30%): none is assumed; the share may not end further from p than it was before
# the trim. Kept unchanged from the pre-r4 guard (not part of this fix): option buckets 35/35/15/15 +/- 3 pp and short
# or no card 10-20% (the family checkers' readings). yes_no_share applies only where the block's pre-trim rows hold
# both yes/no and other rows.
# twin_set_rows: rows that sit in a minimal-pair (label-flip) twin set = a row whose meta.twin_of names a row of the
# same block in the mix with a different gold, plus that base row (judged on the rows in the mix at each step).
# masked / swapped (of choice rows), yes = bad outcome (of yes/no rows), few-shot / inverted cards: the families'
# quota fields (sidecar_flags); a family that carries none of them has no such share (reported as not carried).
COMP = {"yes_no_share": (0.45, 0.55), "opt_2-4": (0.32, 0.38), "opt_5-9": (0.32, 0.38), "opt_10-19": (0.12, 0.18),
        "opt_20-60": (0.12, 0.18), "neg_ge1_of_yes_no": (0.10, 1.0), "neg_ge2_of_yes_no": (0.02, 1.0),
        "deep": (0.0, 0.10), "short_or_no_card": (0.10, 0.20), "twin_set_rows": (0.20, 0.25),
        "attack_rows": (0.05, 0.05), "masked_of_choice": (0.10, 0.15), "swapped_of_choice": (0.05, 0.05),
        "yes_bad_of_yes_no": (0.45, 0.55)}
COMP_F10 = {"masked_of_choice": (0.40, 0.40), "swapped_of_choice": (0.30, 0.30)}      # spec 2.1 "(F10: 40%)", "(F10: 30%)"
CARD_QUOTAS = {"fewshot_cards": (0.05, 0.10), "inverted_cards": (0.10, 0.15)}           # spec 2.1, shares of cards
REPORT_ONLY = ("twin_kind_or_role_twin_rows",)   # the pre-r4 row-flag proxy of the twin quota, reported only
SIDE_FILE_QUOTAS = (
    "Spec 2.1 quotas carried in the families' own fields are guarded where a family carries them: masked / swapped "
    "label names (of choice rows) and 'yes = bad outcome' polarity (of yes/no rows) per row, few-shot and inverted "
    "cards per card. They are read by sidecar_flags() from c_src/<F>/out/candidates_r1.sidecar.jsonl (else row meta) "
    "with the builders' field names: label_form (F1, F4; F7 in row meta), vocab (F3), mode (F10: neutral IDs = masked, "
    "swapped), yes_bad (F1, F4, F10), polarity bad / not bad (F3), fewshot_card (F10), inverted_card (F3, F10), "
    "inverted (F4). A family without such a field (today: F2, F5, F6, F8, F9, F11, F12, F13 for the label-name and "
    "polarity fields) has no share to guard; the report lists them as not carried. Card quotas: no card is added or "
    "emptied by the trim (card rule), so the card shares cannot move; they are recomputed in the audit. Attack twins "
    "and short or no card rows are counted by ATTACK_RULE (the relation file's inv twins, the sidecar's attack / short "
    "fields and the row markers), so F7's / F12's attack twins and F10's / F12's short or no cards are guarded too.")
A28_RULE = (
    "spec 6: 'if the real count passes 30%, the mixer drops F13 and 3B rows from the 6-7.9K bin first' (phase p1, only"
    ' while the long-token share is > 30%). Spec 6 is silent on the 9% row cap, on what follows that bin and on '
    'refills, so PREREG A28 (b) applies (phase p2). Quotas are closed form. p1: the long tokens to remove = (long '
    'tokens - 0.30 x new tokens) / 0.70 (the amount that meets the token cap with no refill credit), apportioned by '
    'largest remainder over F13 and public by their 6-7.9K tokens; each move starts with a unit holding a 6-7.9K F13 /'
    ' 3B row. p2 (each round, while a cap fails): the excess E = long rows - floor(9% x new rows) (the rows in the mix'
    " at the start of the round, after the previous round's refills; if only the token cap fails: long tokens to "
    'remove = (long tokens - 0.30 x new tokens) / 0.70) is apportioned by largest remainder over the blocks over a cap'
    " on their own rows, by each block's own excess e_b = its long rows - floor(9% x its rows) (tokens: long tokens - "
    '30% x tokens), each quota <= e_b; since blocks under their own cap have e_b <= 0, sum e_b >= E, so the quotas '
    'always fit and no block is taken below its own 9% / 30%. A block meets its quota with whole units: first swaps (a'
    " long unit replaced by an unused short unit of the same block's pool with the same refill group and selection "
    'cell, finest tier first: same row quota flags and cards, then same flags, then the cell; public: same source '
    "only; commit: same type x view), then, in own blocks only, drops. Drops are composite moves over the block's "
    'cells (selection cell plus the gold position of choice rows; inside a cell the seeded hash order, quota units '
    'first): the first unit is a quota unit from the first cell in apportionment order (the cell furthest above its '
    'pre-trim share) whose drop leaves the rules kept, else the one leaving them least broken; while a rule is broken,'
    ' the next unit (any unit of the block, quota units first in each cell) is the one that leaves the rules least '
    'broken, taken only if it lowers how far they are broken; when no unit does, the move is rolled back and its first'
    ' unit stays in the mix for good. No step counts or search constants: each failed move removes one candidate, so '
    "the procedure ends. A block's dropped rows never exceed the rows of a proportional slice with the long rows it "
    'removed (ceil(long rows removed x its pre-trim rows / its pre-trim long rows)). Fallback rule: the quota a block '
    'cannot meet (no unit left, the slice bound, or public / commit without a swap) is apportioned again, the same '
    'way, over the other blocks of that phase that still have own excess left, until it is met or no block is left. '
    'Freed rows are refilled under A26 (b) after each round by the same composite moves (sign +1): always into the '
    'passed family with the lowest rows / target, from its unused pool units of cells and cards already in its mix, '
    'every row < 2,000 tokens, each family <= 1.5 x target and, after the move, <= 12% of the realised own rows '
    '(spec 2.1). Share limit m: 12% for a family that holds refill rows, else max(12%, its pre-trim share) (no '
    'worse). A family above m later (the own rows fell) gives back its latest refill moves while the state before '
    'each still passes, then drops whole units (composite moves, every rule kept) of at least ceil((rows - m x own '
    'rows) / (1 - m)) rows. Any remainder lowers the round-1 total: replay = floor(1.5 x the realised new '
    'rows) (60% of the new total), cut by per-source prefixes of the sampler order. Rules, judged against the pre-trim'
    " mix (a rule it met must hold; a rule it missed may not get worse): selection cell balance (crowd_select's "
    'tolerance, max(2, 2%) per stratum, ordinal 1), label x bin chi-square p > 0.01, crowd-bin caps, G10 yes rate per '
    'block and per cell (50 +/- 2 at >= 50 rows, else binomial p >= 0.01), gold position chi-square, longest-is-gold, '
    "abstain wrong >= 50%, ordinal levels; in own blocks the spec 2.1 quota shares (COMP: the spec's bands; point "
    "values with no stated band, 'about 5%' attack twins (ATTACK_RULE: the inv relation's twins) and swapped names "
    "and F10's 40% / 30%, not moved further from the value; option buckets +/- 3 pp and short or no card 10-20% "
    '(ATTACK_RULE) as in the pre-r4 guard), twin-set rows 20-25% (true sets via meta.twin_of), the quota fields the '
    'families carry (side_file_quotas); no card added or emptied, rows per card <= 128, wordings per card (5) and '
    'definition styles (3) kept; families <= m of the realised own rows. A mix under the cap is unchanged.')


def bin_excess(c) -> float:
    """Rows by which a block's crowd bins break spec 2.1's caps (easy <= 25%, hard <= 30%, medium >= 45%); 0 for a
    block without crowd bins (provisional 'na')."""
    tot = sum(c.values())
    if not tot or not any(c.get(b, 0) for b in ("easy", "medium", "hard")):
        return 0.0
    return (max(0.0, c.get("easy", 0) - cs.CAP["easy"] * tot) + max(0.0, c.get("hard", 0) - cs.CAP["hard"] * tot) +
            max(0.0, cs.MED_MIN * tot - c.get("medium", 0)))


def comp_bands(blk) -> dict:
    return COMP | COMP_F10 if blk == "F10" else COMP


def band_excess(v0, v1, band) -> float:
    """How far v1 is past what the rule allows, given the pre-trim v0 (0: kept). (lo, hi): each edge its own rule;
    (p, p): |v1 - p| <= |v0 - p|."""
    lo, hi = band
    if lo == hi:
        return max(0.0, abs(v1 - lo) - abs(v0 - lo) - 1e-12)
    out = 0.0
    for o0, o1 in ((lo - v0, lo - v1), (v0 - hi, v1 - hi)):
        if o1 > 1e-12 and (o0 <= 1e-12 or o1 > o0 + 1e-12):
            out += o1 - max(0.0, o0)
    return out


def comp_shares(c: Counter) -> dict:
    """Spec 2.1 quota shares of one block from its counts (None where the denominator is 0 or the field is not
    carried)."""
    n, yn, ch = c["n"], c["yn"], c["ch"]
    d = {"yes_no_share": yn / n if n else None}
    for b in ("2-4", "5-9", "10-19", "20-60"):
        d["opt_" + b] = c["opt:" + b] / ch if ch else None
    d["neg_ge1_of_yes_no"] = c["neg1"] / yn if yn else None
    d["neg_ge2_of_yes_no"] = c["neg2"] / yn if yn else None
    for k in ("deep", "short_or_no_card", "attack_rows"):
        d[k] = c[k] / n if n else None
    d["twin_set_rows"] = c["tset"] / n if n else None
    d["masked_of_choice"] = c["mask"] / c["lfn"] if c["lfn"] else None
    d["swapped_of_choice"] = c["swap"] / c["lfn"] if c["lfn"] else None
    d["yes_bad_of_yes_no"] = c["ybad"] / c["ybn"] if c["ybn"] else None
    d["twin_kind_or_role_twin_rows"] = c["twin_rows"] / n if n else None
    return d


COMP_DEN = {"opt": "ch", "neg": "yn", "mas": "lfn", "swa": "lfn", "yes_bad": "ybn"}


def sel_tol(s, n) -> float:
    """crowd_select.select's balance tolerance for one stratum (ordinal 1; else max(2, 2% of the stratum's rows))."""
    return 1 if s[0] == "ord" else max(2, 0.02 * n)


SIDE_KEYS = ("label_form", "vocab", "mode", "yes_bad", "polarity", "polarity_tag", "fewshot_card", "inverted_card",
             "inverted", "attack", "short")
INV_TWIN = "inv_twin"   # sidecar_flags(): the row is the twin end (b) of an `inv` relation (its relation file)
SHORT_STYLES = ("short", "none", "no_card")      # meta.defs_style values of a short or no card (F12 writes no_card)
ATTACK_RULE = (
    "Spec 2.1 attack twins ('about 5% of own rows, `inv` relation'): a row counts when it is the twin end (b) of an "
    "`inv` relation in its family's relation file (the families' convention: b.twin_of = a, or F1's role 'attacked'), "
    "or when it carries an attack marker: meta.attack_target, role attacked / attack, a twin_kind naming attack "
    "(attack, F12's T-ATTACK) or inv (F7), or the sidecar's attack field (F1, F3, F10). Short or no card (spec 2.1 "
    "'about 15% of rows'): meta.defs_style short / none / no_card (F12), or the sidecar's short field (F1, F4, F10).")


def inv_twin_ids(ilog, fams) -> set:
    """Ids of the twin end (b) of every `inv` relation in each own family's relation file (crowd_select.fam_files: the
    file family_block loads and checks against the MANIFEST)."""
    out = set()
    for fam in fams:
        p = cs.fam_files(fam)["rel"] if fam in cs.FAMS else None
        if p is None or not p.exists():
            continue
        out |= {x["b"] for x in ilog.jsonl(p) if x.get("type") == "inv" and "b" in x}
    return out


def sidecar_flags(ilog, fams) -> dict:
    """{row id: the spec 2.1 quota fields of that row} from each family's out/candidates_r1.sidecar.jsonl (where the
    file exists; only SIDE_KEYS are kept), plus INV_TWIN for the twin end of every `inv` relation (inv_twin_ids). Row
    meta is read by quota_flags() / is_attack() / short_card() as well (F7 keeps label_form there)."""
    out = {}
    for fam in fams:
        p = cs.fam_dir(fam) / "out" / "candidates_r1.sidecar.jsonl"
        if fam not in cs.FAMS or not p.exists():
            continue
        for d in ilog.jsonl(p):
            if "id" in d:
                out[d["id"]] = {k: d[k] for k in SIDE_KEYS if k in d}
    for i in inv_twin_ids(ilog, fams):
        out.setdefault(i, {})[INV_TWIN] = True
    return out


def is_attack(r, sd=None) -> bool:
    """Spec 2.1 attack twin (ATTACK_RULE): the twin end of an `inv` relation, or an attack marker."""
    m = r.get("meta") or {}
    sd = sd or {}
    tk = str(m.get("twin_kind") or "").lower()
    return bool(sd.get(INV_TWIN) or sd.get("attack") or m.get("attack_target")) or \
        r.get("role") in ("attacked", "attack") or "attack" in tk or tk == "inv"


def short_card(r, sd=None) -> bool:
    """Spec 2.1 'short or no card' row (ATTACK_RULE): defs_style short / none / no_card, or the sidecar's short."""
    return (r.get("meta") or {}).get("defs_style") in SHORT_STYLES or (sd or {}).get("short") is True


def quota_flags(r, sd, blk=None) -> tuple:
    """(label form 'masked' / 'swapped' / 'plain' or None, yes = bad outcome True / False / None, few-shot card,
    inverted card) of one own row: its sidecar fields (sd), else its meta."""
    m = r.get("meta") or {}
    sd = sd or {}
    lf = sd.get("label_form") or sd.get("vocab") or m.get("label_form")
    if lf is None and (blk or r.get("_block")) == "F10" and "mode" in sd:
        lf = {"neutral": "masked", "swapped": "swapped"}.get(sd["mode"], "plain")
    yb = sd.get("yes_bad")
    if not isinstance(yb, bool):
        yb = {"bad": True, "not bad": False}.get(sd.get("polarity") or sd.get("polarity_tag"))
    fs = sd.get("fewshot_card")
    inv = sd.get("inverted_card", sd.get("inverted"))
    return (lf if lf in ("masked", "swapped", "plain") else None, yb, fs if isinstance(fs, bool) else None,
            inv if isinstance(inv, bool) else None)


def row_flags(r, sd=None, blk=None) -> tuple:
    """Row-level 2.1 quota fields of a row (the first replacement tiers also match these)."""
    m = r.get("meta") or {}
    q = quota_flags(r, sd, blk)
    return (bool(m.get("deep")), short_card(r, sd), m.get("twin_kind"), r.get("role"), is_attack(r, sd), q[0], q[1])


_E = Counter()          # a shared empty count table (read only)


class A28State:
    """Counts on the new rows for the A28 trim: the cap totals, per-block cap counts and, per table key, the counts
    every guarded rule reads ('blk' block totals and 2.1 quota counts, 'bins' crowd bins, 'cell' the selection's
    label classes per crowd_select.stratum, 'g9' label x bin tables, 'g10' yes/no cells, 'pos' gold positions per k,
    'ord' ordinal levels, 'card' rows per card, 'cardw' wordings per card, 'defs' definition styles). The twin-set
    count ('tset' in 'blk') follows the rows in the mix: a row counts while a label-flip partner (meta.twin_of, other
    gold, same block) is in the mix too. c0 is the pre-trim snapshot; every rule is judged against it (a rule c0 met
    must hold, a rule c0 missed may not be worse), so the verdict depends only on the current counts. Moves are
    tentative (journal) until commit(); rollback() undoes them; passes() judges the table keys touched since the last
    commit (every other key still has the verdict it had there)."""

    def __init__(self, rows, ntok, side=None):
        self.ntok, self._f, self.side = ntok, {}, side or {}
        self.n = self.t = self.ln = self.lt = 0
        self.blk = Counter()
        self.bc = defaultdict(lambda: [0, 0, 0, 0])       # block -> rows, tokens, long rows, long tokens
        self.c = defaultdict(Counter)
        self._p, self._r0, self.dirty, self.journal = {}, {}, set(), []
        self.info, self.kids, self.pres, self.mem = {}, defaultdict(set), set(), set()
        self.cardflag = defaultdict(lambda: [False, False])   # (block, card) -> few-shot, inverted (any row)
        self.cardcarry = defaultdict(lambda: [False, False])  # block -> the family carries the field
        self._apply([r for r in rows if r["_block"] != "replay"], +1)
        self.c0 = {k: Counter(v) for k, v in self.c.items()}
        self.blk0 = Counter(self.blk)
        self.commit()

    def feat(self, r):
        """The row's (table key, item, weight) increments; cached per row id."""
        f = self._f.get(r["id"])
        if f is not None:
            return f
        m = r.get("meta") or {}
        blk = r["_block"]
        b = m.get("difficulty_bin") or "na"
        s = cs.stratum(r, b)
        cls = cs.label_class(r)
        yn = r["qtype"] == "noul"
        o = r.get("options") or []
        ol = m.get("option_level")
        own = blk in cs.FAMS
        f = [(("blk", blk), "n", 1), (("bins", blk), b, 1), (("cell", blk, s), cls, 1),
             (("g9", blk) + (("yn",) if yn else s[:2]), (b, cls), 1)]
        if own:
            nc = cs.neg_count(r.get("instructions") or "") if yn else 0
            f += [(("blk", blk), "yn", 1)] if yn else []
            f += [(("blk", blk), "ch", 1), (("blk", blk), "opt:" + cs.opt_bucket(len(o)), 1)] \
                if r["qtype"] == "choice" and o else []
            f += [(("blk", blk), "neg1", 1)] if yn and nc >= 1 else []
            f += [(("blk", blk), "neg2", 1)] if yn and nc >= 2 else []
            f += [(("blk", blk), "deep", 1)] if m.get("deep") else []
            f += [(("blk", blk), "short_or_no_card", 1)] if short_card(r, self.side.get(r["id"])) else []
            f += [(("blk", blk), "twin_rows", 1)] if m.get("twin_kind") is not None or r.get("role") == "twin" else []
            if m.get("card_id") is not None:
                f += [(("card", blk, m["card_id"]), "n", 1), (("cardw", blk, m["card_id"]), m.get("wording_id"), 1)]
            if m.get("defs_style") is not None:
                f += [(("defs", blk), m["defs_style"], 1)]
            lf, yb, fs, inv = quota_flags(r, self.side.get(r["id"]))
            if r["qtype"] == "choice" and lf is not None:
                f += [(("blk", blk), "lfn", 1)] + ([(("blk", blk), "mask", 1)] if lf == "masked" else []) + \
                     ([(("blk", blk), "swap", 1)] if lf == "swapped" else [])
            if yn and yb is not None:
                f += [(("blk", blk), "ybn", 1)] + ([(("blk", blk), "ybad", 1)] if yb else [])
            if m.get("card_id") is not None:
                cf, cc = self.cardflag[(blk, m["card_id"])], self.cardcarry[blk]
                cf[0], cf[1] = cf[0] or bool(fs), cf[1] or bool(inv)
                cc[0], cc[1] = cc[0] or fs is not None, cc[1] or inv is not None
        f += [(("blk", blk), "attack_rows", 1)] if own and is_attack(r, self.side.get(r["id"])) else []
        if yn and not own_target(m):              # g10_checks' cells and family aggregate
            g = int(r["gold"])
            f += [(("blk", blk), "hyn", 1), (("blk", blk), "hyes", g),
                  (("g10", blk, str(m.get("wording_id")), str(m.get("difficulty_bin")),
                    cs.neg_count(r.get("instructions") or "")), g, 1)]
        if r["qtype"] == "choice" and r.get("gold") in o:
            k = len(o)
            if not isinstance(ol, dict):
                f += [(("pos", blk, k), o.index(r["gold"]), 1)]
            if k >= 2:
                lens = [len(str(x)) for x in o]
                top = [i for i, x in enumerate(lens) if x == max(lens)]
                f += [(("blk", blk), "lngc", (1 / len(top)) if o.index(r["gold"]) in top else 0.0),
                      (("blk", blk), "lngk", 1 / k), (("blk", blk), "lngn", 1)]
            if any(ABSTAIN.search(str(x)) for x in o):
                f += [(("blk", blk), "abst", 1), (("blk", blk), "abstg", int(bool(ABSTAIN.search(str(r["gold"])))))]
        if isinstance(ol, dict) and r.get("gold") in ol:
            if blk == "F7":
                f += [(("ord", blk, "f7", m.get("sampler"), len(ol)), ol[r["gold"]], 1)]
            elif blk == "COMMIT":
                f += [(("ord", blk, "cs", m.get("card_id"), len(ol)), ol[r["gold"]], 1)]
        self._f[r["id"]] = f
        if own and r["id"] not in self.info:
            to = m.get("twin_of")
            self.info[r["id"]] = (blk, to, str(r.get("gold")))
            if to is not None:
                self.kids[to].add(r["id"])
        return f

    def _member(self, x) -> bool:
        if x not in self.pres:
            return False
        blk, to, g = self.info[x]
        if to in self.pres and self.info[to][0] == blk and self.info[to][2] != g:
            return True
        return any(k in self.pres and self.info[k][0] == blk and self.info[k][2] != g for k in self.kids.get(x, ()))

    def _twin(self, r, sign):
        """Keep the twin-set count of r's block right after r enters (sign +1) or leaves (-1) the mix."""
        x = r["id"]
        if x not in self.info:
            return
        (self.pres.add if sign > 0 else self.pres.discard)(x)
        to = self.info[x][1]
        for a in [x] + ([to] if to in self.info else []) + [k for k in self.kids.get(x, ()) if k in self.info]:
            now = self._member(a)
            if now != (a in self.mem):
                (self.mem.add if now else self.mem.discard)(a)
                key = ("blk", self.info[a][0])
                self.c[key]["tset"] += 1 if now else -1
                self.dirty.add(key)

    def _apply(self, rr, sign):
        for r in rr:
            k = self.ntok[r["id"]]
            a = self.bc[r["_block"]]
            self.n += sign
            self.t += sign * k
            a[0] += sign
            a[1] += sign * k
            if k >= LONG_TOK:
                self.ln += sign
                self.lt += sign * k
                a[2] += sign
                a[3] += sign * k
            self.blk[r["_block"]] += sign
            for key, item, w in self.feat(r):
                self.c[key][item] += sign * w
                self.dirty.add(key)
            self._twin(r, sign)

    def move(self, out=(), add=()):
        """Tentative: remove `out`, add `add` (rows)."""
        out, add = list(out), list(add)
        self._apply(out, -1)
        self._apply(add, +1)
        self.journal.append((out, add))

    def rollback(self):
        for out, add in reversed(self.journal):
            self._apply(add, -1)
            self._apply(out, +1)
        self.journal, self.dirty = [], set()

    def commit(self):
        self.journal, self.dirty = [], set()

    def undo_last(self):
        """Undo the last tentative move (a probe); its keys stay marked as touched."""
        out, add = self.journal.pop()
        self._apply(add, -1)
        self._apply(out, +1)

    def shares(self):
        return self.ln / max(1, self.n), self.lt / max(1, self.t)

    def ok(self, row=True) -> bool:
        """The cap test of token_cap(): long tokens <= 30% (and, with row, long rows <= 9%)."""
        rs_, ts = self.shares()
        return ts <= LONG_TOK_SHARE and (not row or rs_ <= LONG_ROW_SHARE)

    def own_shares(self, b):
        a = self.bc[b]
        return a[2] / max(1, a[0]), a[3] / max(1, a[1])

    def over_own_cap(self, b) -> bool:
        """The block's own rows break a cap (A28 b: 'each over-cap family's selection')."""
        rs_, ts = self.own_shares(b)
        return rs_ > LONG_ROW_SHARE or ts > LONG_TOK_SHARE

    def passes(self) -> bool:
        return not self.broken(self.dirty, first=True)

    # ---- rule tests (cached p values; every test compares the current counts with the snapshot c0)
    def _cached(self, key, fn):
        if key not in self._p:
            self._p[key] = fn()
        return self._p[key]

    def _chi2(self, c: Counter, key):
        bins = sorted({b for (b, _), v in c.items() if v})
        k = 2 if key[2] == "yn" else max(cs.n_classes((key[2], key[3], b)) for b in bins) if bins else 1
        tab = tuple(tuple(c[(b, j)] for j in range(k)) for b in bins)
        return self._cached(("g9", tab), lambda: cs.chi2_p([list(x) for x in tab]))

    def _pos_p(self, c: Counter, k):
        tab = tuple(c[j] for j in range(k))
        if sum(tab) < 5 * k:
            return None
        from scipy.stats import chisquare
        return self._cached(("pos", tab), lambda: float(chisquare(list(tab)).pvalue))

    def _g10(self, c: Counter):
        """(passes, badness): >= 50 rows: |yes - 0.5| <= 2 pp; fewer: binomial p >= 0.01 (g10_checks)."""
        n = c[0] + c[1]
        if not n:
            return True, ("n", 0.0)
        if n >= 50:
            d = abs(c[1] / n - 0.5)
            return d <= G10_TOL + 1e-12, ("big", d)
        from scipy.stats import binomtest
        p = self._cached(("bin", c[1], n), lambda: float(binomtest(c[1], n, 0.5).pvalue))
        return p >= 0.01, ("small", -p)

    @staticmethod
    def _ord(key, c: Counter):
        """(passes, badness) of ordinal_balance's rule on one F7 sampler x K or commit rubric x K cell."""
        k, n = key[4], sum(c.values())
        if not n:
            return True, 0.0
        if key[2] == "f7":
            d = max(abs(c[j] / n - 1 / k) for j in range(k))
            return not (d > 0.02 and max(c[j] for j in range(k)) - min(c[j] for j in range(k)) > 1), d
        d = max(1 / k - 0.05 - c[j] / n for j in range(k))
        return d <= 0, d

    @staticmethod
    def _cell(key, c: Counter):
        """(passes, imbalance) of the selection's balance rule on one stratum (crowd_select.select's tolerance)."""
        s = key[2]
        k = cs.n_classes(s)
        if k < 2 or not sum(c.values()):
            return True, 0
        imb = max(c[j] for j in range(k)) - min(c[j] for j in range(k))
        return imb <= sel_tol(s, sum(c.values())), imb

    def _block_tests(self, blk, c: Counter) -> dict:
        """name -> (passes, badness) for the block-level G10 tests."""
        out = {}
        if c["hyn"]:
            d = abs(c["hyes"] / c["hyn"] - 0.5)
            out["g10_yes_rate"] = (d <= G10_TOL + 1e-12, d)
        if c["lngn"]:
            d = abs(100 * (c["lngc"] - c["lngk"]) / c["lngn"])
            out["longest_is_gold_pp"] = (d <= 2.0 + 1e-9, d)
        if c["abst"]:
            s = c["abstg"] / c["abst"]
            out["abstain_gold_share"] = (s <= 0.5 + 1e-12, s)
        return out

    def _ref(self, key, fn):
        """Snapshot-side values of one key's rule (c0 never changes, so they are computed once)."""
        if key not in self._r0:
            self._r0[key] = fn()
        return self._r0[key]

    def _rule(self, key, cur: Counter, ref: Counter) -> list:
        """The broken rules on one table key, current counts vs the snapshot: [(message, size)], size > 0 = how far
        past what the rule allows (about rows; used only to steer composite moves, never to pass a rule)."""
        bad, kind = [], key[0]
        if kind == "blk":
            blk = key[1]
            t0, t1 = self._ref(("t0",) + key, lambda: self._block_tests(blk, ref)), self._block_tests(blk, cur)
            scale = {"g10_yes_rate": cur["hyn"], "longest_is_gold_pp": cur["lngn"] / 100,
                     "abstain_gold_share": cur["abst"]}
            for name, (ok1, d1) in t1.items():
                ok0, d0 = t0.get(name, (True, 0.0))
                if not ok1 and (ok0 or d1 > d0 + 1e-12):
                    lim = d0 if not ok0 else (G10_TOL if name == "g10_yes_rate" else 2.0 if name.startswith("long")
                                              else 0.5)
                    bad.append((f"{blk} {name} {d1:.4f}", (d1 - lim) * scale[name] + 1e-3))
            if blk in cs.FAMS:
                s0, s1 = self._ref(("s0",) + key, lambda: comp_shares(ref)), comp_shares(cur)
                for name, band in comp_bands(blk).items():
                    v0, v1 = s0[name], s1[name]
                    if v0 is None or v1 is None or (name == "yes_no_share" and not 0 < v0 < 1):
                        continue
                    ex = band_excess(v0, v1, band)
                    if ex > 0:
                        d = cur[next((v for k, v in COMP_DEN.items() if name.startswith(k)), "n")]
                        bad.append((f"{blk} {name} {v0:.4f} -> {v1:.4f} (spec 2.1 {band})", ex * d + 1e-3))
        elif kind == "bins":
            ex0, ex1 = self._ref(key, lambda: bin_excess(ref)), bin_excess(cur)
            if ex1 > 1e-9 and ex1 > ex0 + 1e-9:
                bad.append((f"{key[1]} crowd-bin caps (+{ex1:.1f} rows)", ex1 - ex0))
        elif kind == "cell":
            (ok0, i0), (ok1, i1) = self._ref(key, lambda: self._cell(key, ref)), self._cell(key, cur)
            if not ok1 and (ok0 or i1 > i0):
                lim = i0 if not ok0 else sel_tol(key[2], sum(cur.values()))
                bad.append((f"{key[1]} cell {key[2]} imbalance {i0} -> {i1}", i1 - lim))
        elif kind == "g9":
            p0, p1 = self._ref(key, lambda: self._chi2(ref, key)), self._chi2(cur, key)
            if p1 is not None and p1 <= cs.CHI_P and (p0 is None or p0 > cs.CHI_P or p1 < p0):
                lim = p0 if p0 is not None and p0 <= cs.CHI_P else cs.CHI_P
                bad.append((f"{key[1]} G9 label x bin {key[2:]} p {p1:.4f}", 100 * (lim - p1) + 1e-3))
        elif kind == "g10":
            (ok0, d0), (ok1, d1) = self._ref(key, lambda: self._g10(ref)), self._g10(cur)
            if not ok1 and (ok0 or d0[0] != d1[0] or d1[1] > d0[1] + 1e-12):
                n = cur[0] + cur[1]
                lim = d0[1] if not ok0 and d0[0] == d1[0] else (G10_TOL if d1[0] == "big" else -0.01)
                bad.append((f"G10 cell {'|'.join(map(str, key[1:]))} {d1}",
                            (d1[1] - lim) * (n if d1[0] == "big" else 100) + 1e-3))
        elif kind == "pos":
            p0, p1 = self._ref(key, lambda: self._pos_p(ref, key[2])), self._pos_p(cur, key[2])
            if p1 is not None and p1 <= 0.01 and (p0 is None or p0 > 0.01 or p1 < p0):
                lim = p0 if p0 is not None and p0 <= 0.01 else 0.01
                bad.append((f"G10 gold position {key[1]}|k{key[2]} p {p1:.4f}", 100 * (lim - p1) + 1e-3))
        elif kind == "ord":
            (ok0, d0), (ok1, d1) = self._ref(key, lambda: self._ord(key, ref)), self._ord(key, cur)
            if not ok1 and (ok0 or d1 > d0 + 1e-12):
                bad.append((f"G10 ordinal {'|'.join(map(str, key[1:]))}",
                            (d1 - (d0 if not ok0 else 0.0)) * sum(cur.values()) + 1e-3))
        elif kind == "card":                    # one key per card: rows of that card
            cid, n0, n1 = key[2], ref["n"], cur["n"]
            if n0 <= 0 < n1:
                bad.append((f"{key[1]} card {cid} not in the block's pre-trim mix", 10.0))
            elif n0 > 0 >= n1:
                bad.append((f"{key[1]} card {cid} emptied", 10.0))
            elif n1 > max(CARD_MAX, n0):
                bad.append((f"{key[1]} card {cid} rows {n1} > {CARD_MAX}", n1 - max(CARD_MAX, n0)))
        elif kind in ("cardw", "defs"):
            n0, n1 = sum(1 for v in ref.values() if v > 0), sum(1 for v in cur.values() if v > 0)
            lim = CARD_WORDINGS if kind == "cardw" else DEF_STYLES
            if n1 < min(lim, n0) and sum(cur.values()) > 0:
                bad.append((f"{'|'.join(map(str, key[1:]))} {kind} {n0} -> {n1}", 10.0 * (min(lim, n0) - n1)))
        return bad

    def broken(self, keys, first=False) -> list[str]:
        bad = []
        for key in sorted(keys, key=lambda k: (COST.get(k[0], 9), repr(k))):
            bad += [m for m, _ in self._rule(key, self.c.get(key, _E), self.c0.get(key, _E))]
            if bad and first:
                return bad
        return bad

    def violation(self, keys=None) -> float:
        """How far the state is past the rules on `keys` (default: the keys touched since the last commit; 0: they
        pass). Used only to steer composite moves; a commit still needs passes()."""
        keys = self.dirty if keys is None else keys
        return math.fsum(v for key in keys for _, v in self._rule(key, self.c.get(key, _E),
                                                                  self.c0.get(key, _E)))

    def keys_for(self, rr) -> set:
        return {key for r in rr for key, _, _ in self.feat(r)}

    def mono_delta(self, out, add) -> float:
        """delta() on the move's card keys only: rows per card, wordings per card, definition styles. A drop that
        empties a card or loses a card's wording or a style below its floor, or an add of a new card or past 128
        rows per card, cannot be mended by more moves of the same kind."""
        ks = {k for k in self.keys_for(list(out) + list(add)) if k[0] in ("card", "cardw", "defs")}
        if not ks:
            return 0.0
        v0 = self.violation(ks)
        self.move(out, add)
        v1 = self.violation(ks)
        self.undo_last()
        return v1 - v0

    def delta(self, out, add) -> float:
        """Change of violation() if `out` / `add` were moved (only their keys can change; the state is restored)."""
        ks = self.keys_for(list(out) + list(add))
        v0 = self.violation(ks)
        self.move(out, add)
        v1 = self.violation(ks)
        self.undo_last()
        return v1 - v0

    def card_shares(self, c, blk) -> dict:
        """Spec 2.1 card quotas of one block: few-shot / inverted cards among its cards in the mix (None when the
        family carries no such field)."""
        cards = [k[2] for k, v in c.items() if k[0] == "card" and k[1] == blk and v["n"] > 0]
        out = {}
        for i, name in enumerate(CARD_QUOTAS):
            carried = self.cardcarry[blk][i]
            out[name] = (sum(1 for x in cards if self.cardflag[(blk, x)][i]) / len(cards)) if cards and carried \
                else None
        return out

    def audit(self) -> list[str]:
        """Every guarded rule on every table key, current counts vs the snapshot (the end-of-trim check), plus the
        card quotas."""
        bad = self.broken(set(self.c) | set(self.c0))
        for blk in sorted({k[1] for k in self.c0 if k[0] == "blk" and k[1] in cs.FAMS}):
            s0, s1 = self.card_shares(self.c0, blk), self.card_shares(self.c, blk)
            for name, band in CARD_QUOTAS.items():
                if s0[name] is not None and s1[name] is not None and band_excess(s0[name], s1[name], band) > 0:
                    bad.append(f"{blk} {name} {s0[name]:.4f} -> {s1[name]:.4f} (spec 2.1 {band})")
        return bad

    @staticmethod
    def cards(c, blk) -> Counter:
        """Rows per card of one block (from the per-card keys)."""
        return Counter({k[2]: v["n"] for k, v in c.items() if k[0] == "card" and k[1] == blk})

    def report(self, blk) -> dict:
        """Spec 2.1 quota shares (incl. twin sets and the families' quota fields), card quotas, the G10 block tests,
        card counts and card_tv of one block: pre-trim vs now."""
        out = {}
        for tag, c in (("before", self.c0), ("after", self.c)):
            b = c.get(("blk", blk), _E)
            cards = self.cards(c, blk)
            sz = sorted(v for v in cards.values() if v > 0)
            out[tag] = {"rows": b["n"],
                        **({k: (round(v, 4) if v is not None else None) for k, v in comp_shares(b).items()}
                           if blk in cs.FAMS else {}),
                        **({k: (round(v, 4) if v is not None else None) for k, v in self.card_shares(c, blk).items()}
                           if blk in cs.FAMS else {}),
                        **{k: round(v[1], 4) for k, v in self._block_tests(blk, b).items()},
                        "cards": len(sz), "max_rows_per_card": sz[-1] if sz else 0,
                        "median_rows_per_card": sz[len(sz) // 2] if sz else 0}
        if blk in cs.FAMS:
            out["bands"] = {k: list(v) for k, v in (comp_bands(blk) | CARD_QUOTAS).items()}
            out["not_carried"] = sorted(k for k in list(comp_bands(blk)) + list(CARD_QUOTAS)
                                        if out["before"].get(k) is None)
        out["card_tv"] = round(card_tv(self.cards(self.c0, blk), self.cards(self.c, blk)), 4)
        return out


def card_tv(c0: Counter, c1: Counter) -> float:
    """Total variation distance between two rows-per-card distributions (0 when either is empty)."""
    n0, n1 = sum(c0.values()), sum(c1.values())
    if not n0 or not n1:
        return 0.0
    return 0.5 * sum(abs(c0[k] / n0 - c1[k] / n1) for k in set(c0) | set(c1))


class Cells:
    """Whole units of one block over its cells, for composite moves that keep the block's pre-trim mix: weights = its
    pre-trim rows per cell, cur = its current rows per cell (shared by the block's drop and refill Cells and updated
    by every take), total() = its current rows. Drops (sign -1) prefer the cell furthest above its pre-trim share,
    refills (sign +1) the cell furthest below it (ties: seeded cell hash); inside a cell, units come in their given
    (seeded) order, quota units first. usable(u) False removes a unit for good. state() / restore() undo takes."""

    def __init__(self, weights: dict, queues: dict, size, cur: Counter, total, sign, usable=lambda u: True, tag="",
                 quota=lambda u: True):
        tot = sum(weights.values()) or 1
        self.w = {c: v / tot for c, v in weights.items()}
        self.q = {c: list(us) for c, us in queues.items() if us and self.w.get(c, 0) > 0}
        self.h = {c: h64(SEED, "a28", "cell", tag, c) for c in self.q}
        self.pos, self.cur, self.total, self.sign = {c: 0 for c in self.q}, cur, total, sign
        self.size, self.usable, self.quota, self.dead, self.kept = size, usable, quota, set(), set()

    def _next(self, c):
        q, i = self.q[c], self.pos[c]
        while i < len(q) and (q[i] in self.dead or not self.usable(q[i])):
            self.dead.add(q[i])
            i += 1
        self.pos[c] = i
        return q[i] if i < len(q) else None

    def order(self, quota_only=False, limit=None) -> list:
        """Cells with a usable head unit (a quota unit if asked; at most `limit` rows), the one whose take best
        restores the pre-trim mix first."""
        n = self.total()
        live = []
        for c in self.q:
            u = self._next(c)
            if u is None or (quota_only and not self.quota(u)) or (limit is not None and self.size(u) > limit):
                continue
            live.append(c)
        return sorted(live, key=lambda c: (self.sign * (self.cur[c] - self.w[c] * n), self.h[c]))

    def pick(self, probe, quota_only=False, limit=None):
        """(unit, its probe value): the cells are tried in apportionment order; the first head giving 0 is taken,
        else the head giving the least (earliest cell on ties). None when no cell has a usable head."""
        best = bv = None
        for c in self.order(quota_only, limit):
            u = self.q[c][self.pos[c]]
            v = probe(u)
            if bv is None or v < bv - 1e-12:
                best, bv = c, v
            if v <= 1e-9:
                break
        if best is None:
            return None, None
        return best, bv

    def take(self, c):
        u = self.q[c][self.pos[c]]
        self.pos[c] += 1
        self.cur[c] += self.sign * self.size(u)
        return u

    def drop(self, u):
        """A unit left out for good (the first unit of a rolled-back composite move)."""
        self.dead.add(u)
        self.kept.add(u)

    def state(self):
        return dict(self.pos), Counter(self.cur)

    def restore(self, s):
        self.pos = dict(s[0])
        self.cur.clear()
        self.cur.update(s[1])


def composite(st: A28State, cells: Cells, move_of, max_rows=None, first_quota=True, final_ok=None):
    """One composite move with no step limit: the first unit (a quota unit when first_quota) comes from the first
    cell in apportionment order whose head keeps the rules, else the head leaving them least broken; while the rules
    are broken, the next unit (any head) is the one leaving them least broken, taken only if it lowers how far they are
    broken. Passing -> commit, (units, rows moved, 'ok'). No such unit -> everything rolled back, the first unit is
    left out for good (Cells.drop): (units, None, 'stuck'); no first unit at all: ([], None, 'spent'). max_rows bounds
    the rows moved (refills). final_ok(units) False on a passing state: rolled back, (units, None, 'bound')."""
    s0, taken, moved = cells.state(), [], 0

    def probe(u):
        return v + st.delta(*move_of(u))
    v = 0.0
    c, _ = cells.pick(probe, quota_only=first_quota, limit=max_rows)
    if c is None:
        return [], None, "spent"
    while True:
        u = cells.take(c)
        out, add = move_of(u)
        v += st.delta(out, add)
        st.move(out, add)
        moved += len(out) + len(add)
        taken.append(u)
        if st.passes():
            if final_ok is not None and not final_ok(taken):
                st.rollback()
                cells.restore(s0)
                return taken, None, "bound"
            st.commit()
            return taken, moved, "ok"
        cur = v
        c, nv = cells.pick(probe, limit=None if max_rows is None else max_rows - moved)
        if c is None or nv >= cur - 1e-9:
            break
    st.rollback()
    cells.restore(s0)
    cells.drop(taken[0])
    return taken, None, "stuck"


def label_bin_p(rows_f) -> list:
    """Spec 2.1 / G9 label x bin chi-square p values of one block's rows (crowd_select.selection_report's tables)."""
    yn, ch, bins = defaultdict(Counter), defaultdict(lambda: defaultdict(Counter)), set()
    for r in rows_f:
        b = (r.get("meta") or {}).get("difficulty_bin") or "na"
        bins.add(b)
        if r["qtype"] == "noul":
            yn[b][int(r["gold"])] += 1
        else:
            s = cs.stratum(r, b)
            ch[(s[0], s[1])][b][cs.label_class(r)] += 1
    bl = sorted(bins)
    ps = [cs.chi2_p([[yn[b][0], yn[b][1]] for b in bl])]
    ps += [cs.chi2_p([[d[b][j] for j in range(cs.n_classes((*k, b)))] for b in bl]) for k, d in ch.items()]
    return [p for p in ps if p is not None]


def shrink_replay(rows, rels, pools, ctx, cut: int, info: dict) -> tuple[list, list]:
    """A26 (b) remainder: replay = 1.5 x new rows, so `cut` replay rows leave. Per source, quotas by largest remainder
    over the replay rows each source holds now; each source keeps the prefix of the sampler's own seeded stratified
    unit order (replay_sample.unit_order) covering its quota; the overshoot is removed from the last single-row units
    of the sources furthest above quota (the exact_total rule). Whole units; relations inside kept units stay."""
    rs = rs_mod()
    rp, units, lt = pools["replay"], ctx["units"], ctx["lt"]
    by_u = defaultdict(list)
    for r in rows:
        if r["_block"] == "replay":
            by_u[rp.unit_of[r["id"]]].append(r["id"])
    by_src = defaultdict(list)
    for u in by_u:
        by_src[units[u]["source"]].append(u)
    cnt = {s: sum(len(by_u[u]) for u in us) for s, us in by_src.items()}
    total = sum(cnt.values()) - cut
    quota = largest_remainder(cnt, max(0, total))
    take = {}
    for s in sorted(by_src):
        out, n = [], 0
        for u in rs.unit_order(lt, units, by_src[s]):
            if n >= quota[s]:
                break
            out.append(u)
            n += len(by_u[u])
        take[s] = out
    size = lambda us: sum(len(by_u[u]) for u in us)  # noqa: E731
    over = sum(size(t) for t in take.values()) - total
    while over > 0:
        cand = [s for s in take if any(len(by_u[u]) == 1 for u in take[s])]
        if not cand:
            break
        s = max(cand, key=lambda s: (size(take[s]) - quota[s], s))
        j = max(i for i, u in enumerate(take[s]) if len(by_u[u]) == 1)
        take[s] = take[s][:j] + take[s][j + 1:]
        over -= 1
    keep = {i for us in take.values() for u in us for i in by_u[u]}
    gone = {i for u in by_u for i in by_u[u]} - keep
    info["replay_shrink"] = {"cut_asked": cut, "replay_rows_before": sum(cnt.values()), "replay_rows_after": len(keep),
                             "sources": len(cnt), "overshoot_left": max(0, over)}
    return drop_rows(rows, rels, gone)


def _csig(pool, rr) -> tuple:
    """A unit's apportionment cell: its rows' tier-0 refill keys plus, on choice rows, the gold position (spec 2.1:
    gold letters uniform; G10 checks positions per k, which crowd_select's label class leaves out for k >= 5)."""
    return tuple(sorted(repr((pool.keys_of(r)[0], (r.get("options") or []).index(r["gold"])
                              if r["qtype"] == "choice" and r.get("gold") in (r.get("options") or []) else None))
                        for r in rr))


def _usig(keys) -> tuple:
    """A unit's selection cell: its rows' tier-0 refill keys (own / commit: stratum x label class; public: qtype)."""
    return tuple(sorted(repr(k) for k in keys))


TRIM_KEYS = ("swapped_out_rows", "swapped_units", "dropped_rows", "dropped_units", "drop_long_rows", "long_rows_removed",
             "long_tokens_removed", "composite_moves", "stuck_moves", "share12_rows")


def cap_trim(rows, rels, ntok, pools, ctx, targets, ever, handled, accept, rep) -> tuple[list, list, list]:
    """PREREG A28 (b) / spec 6: meet the token cap (see A28_RULE). A mix already under the cap is returned unchanged.
    accept(pool, unit, tally) is the refill gate of finish() (ever / deny-list / G13 / held-out / G18 / <= 7,900).
    ctx['sidecar'] (sidecar_flags) holds the families' quota fields. Returns (rows, rels, problems); rep['a28_cap']
    holds the rule, the cap numbers before / after, the closed-form plan (quota, delivered and fallback per phase,
    round and block), the trims by block, the refills, the remainder and replay, the realised rows by block, the 2.1
    quota shares, G10 block tests and card_tv before / after for every touched block, the end-of-trim audit and the
    share deltas the gates expect."""
    side = (ctx or {}).get("sidecar") or {}
    st = A28State(rows, ntok, side)
    b0 = st.shares()
    pub0 = Counter(r["source"] for r in rows if r["_block"] == "public")
    com0 = Counter(cs.commit_group(r) for r in rows if r["_block"] == "COMMIT")
    info = rep["a28_cap"] = {
        "rule": A28_RULE, "applied": False,
        "caps": {"long_tokens_ge": LONG_TOK, "long_row_share_max": LONG_ROW_SHARE,
                 "long_token_share_max": LONG_TOK_SHARE, "family_max_x_target": A26_ROOM},
        "before": {"new_rows": st.n, "long_rows": st.ln, "new_tokens": st.t, "long_tokens": st.lt,
                   "long_row_share": round(b0[0], 4), "long_token_share": round(b0[1], 4)}}
    if st.ok():
        info["after"] = info["before"]
        return rows, rels, []
    info["applied"] = True
    own0 = sum(st.blk0[f] for f in cs.FAMS)
    info["guard"] = {"composition_bands": {k: list(v) for k, v in COMP.items()},
                     "f10_bands": {k: list(v) for k, v in COMP_F10.items()},
                     "card_quotas": {k: list(v) for k, v in CARD_QUOTAS.items()},
                     "point_value_rule": "(p, p): the share may not end further from p than before the trim",
                     "g10_tol": G10_TOL, "own_max_share_of_realised_own": OWN_MAX, "own_rows_before": own0,
                     "rows_per_card_max": CARD_MAX, "wordings_per_card_min": CARD_WORDINGS,
                     "definition_styles_min": DEF_STYLES, "fixed_blocks_same_group_swaps_only": list(FIXED),
                     "side_file_quotas": SIDE_FILE_QUOTAS, "sidecar_rows_read": len(side),
                     "attack_and_short_card_rule": ATTACK_RULE, "report_only": list(REPORT_ONLY)}
    att0 = defaultdict(Counter)                 # pre-trim attack twins per own block: by inv relation / by marker
    for r in rows:
        if r["_block"] in cs.FAMS:
            sd = side.get(r["id"]) or {}
            a = att0[r["_block"]]
            a["rows"] += 1
            a["inv_relation"] += bool(sd.get(INV_TWIN))
            a["marker"] += is_attack(r, {k: v for k, v in sd.items() if k != INV_TWIN})
            a["counted"] += is_attack(r, sd)
            a["short_or_no_card"] += short_card(r, sd)
    info["guard"]["attack_twins_before"] = {b: dict(c) for b, c in sorted(att0.items())}
    units = defaultdict(list)                                   # (block, call_id) -> rows (whole units)
    for r in rows:
        if r["_block"] != "replay":
            units[(r["_block"], r["call_id"])].append(r)
    units0 = {u: list(rr) for u, rr in units.items()}
    is_long = lambda u: any(ntok[r["id"]] >= LONG_TOK for r in units[u])                  # noqa: E731
    lrows = lambda u: sum(1 for r in units[u] if ntok[r["id"]] >= LONG_TOK)               # noqa: E731
    ltoks = lambda u: sum(ntok[r["id"]] for r in units[u] if ntok[r["id"]] >= LONG_TOK)   # noqa: E731
    in6 = lambda u: any(spec6_bin(r, ntok) for r in units[u])                              # noqa: E731
    blocks0 = {b: {"rows": a[0], "long_rows": a[2], "long_row_share": round(a[2] / max(1, a[0]), 4),
                   "long_token_share": round(a[3] / max(1, a[1]), 4)} for b, a in sorted(st.bc.items())}
    n0 = {b: a[0] for b, a in st.bc.items()}
    long0 = {b: a[2] for b, a in st.bc.items()}
    info["over_cap_blocks_before"] = sorted(b for b in st.bc if st.over_own_cap(b))
    fams = [f for f in cs.FAMS if f in pools and targets.get(f, 0) > 0 and st.blk0[f] > 0]
    share0 = {f: st.blk0[f] / max(1, own0) for f in cs.FAMS if st.blk0[f]}
    mshare = {f: max(OWN_MAX, s) for f, s in share0.items()}     # spec 2.1 12%, or no worse than before the trim
    cap15 = {f: math.floor(A26_ROOM * targets[f]) for f in fams}

    def own_rows():
        return sum(st.blk[f] for f in cs.FAMS)

    def lim12(f) -> float:
        """Spec 2.1's 12% of the realised own rows for a family that holds A26 (b) refill rows (a refill never takes
        a family past it); a family without refill rows may not end above max(12%, its pre-trim share) (no worse)."""
        return OWN_MAX if refilled[f] > 0 else mshare[f]

    def over12(f, own=None) -> bool:
        return f in mshare and st.blk[f] > lim12(f) * (own_rows() if own is None else own) + 1e-9
    got, tally = {}, Counter()

    def sig_of(b, rr):
        pool = pools.get(b)
        return _usig(pool.keys_of(r)[0] for r in rr) if pool else None

    def flags_of(rr, b):
        return tuple(sorted(repr(row_flags(r, side.get(r["id"]), b)) for r in rr))

    def fetch(b, v):
        """accept() once per pool unit: its rows, or None (refused, or a row >= 2,000 tokens: never a replacement)."""
        if (b, v) not in got:
            pools[b].tried.add(v)
            rr = accept(pools[b], v, tally)
            got[(b, v)] = None if rr is None or any(ntok[r["id"]] >= LONG_TOK for r in rr) else rr
        return got[(b, v)]

    # replacement index per block, tiers: (group, cell, flags, cards), (group, cell, flags), (group, cell) -> unused
    # pool units in pool seeded order
    rindex = {}

    def cards_of(rr):
        return tuple(sorted(str((r.get("meta") or {}).get("card_id")) for r in rr))

    def rpool(b):
        if b not in rindex:
            pool, tiers = pools.get(b), (defaultdict(list), defaultdict(list), defaultdict(list))
            if pool is not None:
                for g in sorted(pool.cands):
                    for v in pool.cands[g]:
                        if v in pool.tried:
                            continue
                        raw = pool.raw_of(v)
                        s = _usig(pool.keys_of(r)[0] for r in raw)
                        fl = flags_of(raw, b)
                        tiers[0][(g, s, fl, cards_of(raw))].append(v)
                        tiers[1][(g, s, fl)].append(v)
                        tiers[2][(g, s)].append(v)
            rindex[b] = tiers
        return rindex[b]

    used = set()                                                # (block, pool unit) swapped or refilled in
    gone, added, added_rels = set(), [], []
    trims = defaultdict(Counter)                                # block -> counts of its trim
    plan, last, pre_move = [], {}, {}
    refilled, refill_moves, given_back, swapped_in = Counter(), Counter(), Counter(), Counter()
    refill_log = defaultdict(list)                              # family -> [(units, rows)] of the current round
    cur_cells = defaultdict(Counter)                            # block -> its current rows per cell (Cells)
    for (b, _), rr in units.items():
        if b in pools:
            cur_cells[b][_csig(pools[b], rr)] += len(rr)
    deficit = 0

    def trace(ph, b, kind, us):
        if A28_TRACE is not None:
            A28_TRACE.append({"phase": ph, "block": b, "kind": kind, "units": list(us), **pre_move})

    def mark(b):
        pre_move.update(cap_before=st.shares(), own_before=st.own_shares(b))

    def swap(b, u) -> bool:
        """Replace unit u of block b with a short same-group, same-cell unit of b's pool (fine tier first)."""
        pool, rr = pools.get(b), units[u]
        if pool is None:
            return False
        groups = {pool.group_row(r) for r in rr}
        if len(groups) != 1:
            return False
        g = groups.pop()
        s = sig_of(b, rr)
        fl = flags_of(rr, b)
        t = rpool(b)
        seen = set()
        for q in (t[0].get((g, s, fl, cards_of(rr)), []), t[1].get((g, s, fl), []), t[2].get((g, s), [])):
            for v in q:
                if (b, v) in used or v in seen:
                    continue
                seen.add(v)
                new = fetch(b, v)
                if new is None:
                    continue
                st.move(out=rr, add=new)
                if st.passes():
                    st.commit()
                    used.add((b, v))
                    swapped_in[b] += len(new)
                    cur_cells[b][_csig(pool, rr)] -= len(rr)
                    cur_cells[b][_csig(pool, new)] += len(new)
                    gone.update(r["id"] for r in rr)
                    added.extend(new)
                    added_rels.extend(pool.rels_of({r["id"] for r in new}))
                    ever.update({r["id"]: (b, r) for r in new})
                    return True
                st.rollback()
        return False

    dcells, swap_tried = {}, set()

    def drop_cells(ph, b):
        """The block's units in the mix over its cells (weights: its pre-trim rows per cell); inside a cell the seeded
        hash order, the phase's quota units first."""
        if (ph, b) not in dcells:
            quota = in6 if ph == "p1" else is_long
            w = Counter()
            for (bb, _), rr in units0.items():
                if bb == b:
                    w[_csig(pools[b], rr)] += len(rr)
            q = defaultdict(list)
            for u in sorted((u for u in units if u[0] == b and not any(r["id"] in gone for r in units[u])),
                            key=lambda u: (not quota(u), h64(SEED, "a28", ph, *u))):
                q[_csig(pools[b], units[u])].append(u)
            dcells[(ph, b)] = Cells(w, q, lambda u: len(units[u]), cur_cells[b], lambda b=b: st.blk[b], -1,
                                    usable=lambda u: not any(r["id"] in gone for r in units[u]), tag=ph + b,
                                    quota=quota)
        return dcells[(ph, b)]

    def bound(b, extra_rows, extra_long) -> int:
        """The rows a proportional slice with the long rows this block's drops removed would take."""
        return math.ceil((trims[b]["drop_long_rows"] + extra_long) * n0[b] / max(1, long0[b]))

    def deliver(ph, rnd, b, quota, measure) -> tuple[int, str]:
        """Meet `quota` (long rows or long tokens) in block b: swaps, then (own blocks) composite drops."""
        nonlocal deficit
        val = lrows if measure == "rows" else ltoks
        isq = in6 if ph == "p1" else is_long
        done = 0
        for u in sorted((u for u in units if u[0] == b and isq(u)), key=lambda u: h64(SEED, "a28", ph, *u)):
            if done >= quota:
                return done, "met"
            if (ph, u) in swap_tried or any(r["id"] in gone for r in units[u]):
                continue
            swap_tried.add((ph, u))
            k, kl, kt = val(u), lrows(u), ltoks(u)
            mark(b)
            if swap(b, u):
                trace(ph, b, "swap", [u])
                trims[b]["swapped_out_rows"] += len(units[u])
                trims[b]["swapped_units"] += 1
                trims[b]["long_rows_removed"] += kl
                trims[b]["long_tokens_removed"] += kt
                done += k
        if done >= quota:
            return done, "met"
        if b in FIXED or b not in pools:
            return done, "no swap left (public / commit: same-group swaps only)"
        cells = drop_cells(ph, b)

        def within(taken):
            n = sum(len(units[u]) for u in taken)
            return trims[b]["dropped_rows"] + n <= bound(b, n, sum(lrows(u) for u in taken))
        while done < quota:
            mark(b)
            taken, n, why = composite(st, cells, lambda u: (units[u], ()), final_ok=within)
            if n is None:
                if why == "stuck":
                    trims[b]["stuck_moves"] += 1
                    continue
                return done, {"spent": "no quota unit left", "bound": "proportional-slice bound"}[why]
            trace(ph, b, "drop", taken)
            for u in taken:
                gone.update(r["id"] for r in units[u])
                trims[b]["drop_long_rows"] += lrows(u)
                trims[b]["long_rows_removed"] += lrows(u)
                trims[b]["long_tokens_removed"] += ltoks(u)
                done += val(u)
            trims[b]["dropped_rows"] += n
            trims[b]["dropped_units"] += len(taken)
            trims[b]["composite_moves"] += 1
            deficit += n
        return done, "met"

    def run_phase(ph, rnd, measure, need, weights):
        """Closed-form quotas (largest remainder by weight, each <= its weight), then the fallback rule."""
        ent = {"phase": ph, "round": rnd, "measure": measure, "need": need, "weights": dict(weights),
               "quotas": {}, "delivered": Counter(), "why": {}, "fallback": []}
        left = {b: w for b, w in weights.items() if w > 0}
        pend = {b: q for b, q in largest_remainder(left, min(need, sum(left.values()))).items() if q > 0}
        ent["quotas"] = dict(pend)
        if need > sum(left.values()):
            ent["need_over_capacity"] = need - sum(left.values())
        failed = set()
        while pend:
            short = 0
            for b in sorted(pend, key=lambda b: (-pend[b], b)):
                d, why = deliver(ph, rnd, b, pend[b], measure)
                ent["delivered"][b] += d
                ent["why"][b] = why
                left[b] -= d
                if d < pend[b]:
                    failed.add(b)
                    short += pend[b] - d
            if short <= 0:
                break
            cand = {b: w for b, w in left.items() if b not in failed and w > 0}
            if not cand:
                ent["unmet"] = short
                break
            pend = {b: q for b, q in largest_remainder(cand, min(short, sum(cand.values()))).items() if q > 0}
            ent["fallback"].append({"short": short, "to": dict(pend)})
        ent["delivered"] = dict(ent["delivered"])
        plan.append(ent)
        return sum(ent["delivered"].values())

    # ---- A26 (b) refill of freed rows: composite moves into the passed family with the lowest rows / target
    rcells, rspent = {}, set()

    def refill_cells(f):
        if f not in rcells:
            pool = pools[f]
            w = Counter()
            for (b, _), rr in units0.items():
                if b == f:
                    w[_csig(pool, rr)] += len(rr)
            cards = {(r.get("meta") or {}).get("card_id") for (b, _), rr in units0.items() if b == f for r in rr}
            q = defaultdict(list)
            for g in sorted(pool.cands):
                for v in pool.cands[g]:
                    if v not in pool.tried and all((r.get("meta") or {}).get("card_id") in cards
                                                   for r in pool.raw_of(v)):
                        q[_csig(pool, pool.raw_of(v))].append(v)
            rcells[f] = Cells(w, q, lambda v, p=pool: len(p.raw_of(v)), cur_cells[f], lambda f=f: st.blk[f], +1,
                              usable=lambda v, f=f: (f, v) not in used and fetch(f, v) is not None, tag="refill" + f)
        return rcells[f]

    def refill(rnd):
        """Refill the freed rows, always into the passed family with the lowest rows / target that has room (<= 1.5x
        target; its rows / the realised own rows <= 12% after the move, spec 2.1) and a usable unit."""
        nonlocal deficit
        while deficit > 0:
            own = own_rows()
            room = {f: min(deficit, cap15[f] - st.blk[f],
                           math.floor((OWN_MAX * own - st.blk[f]) / (1 - OWN_MAX) + 1e-9) if OWN_MAX < 1
                           else deficit) for f in fams if f not in rspent}
            cand = sorted((f for f, k in room.items() if k > 0),
                          key=lambda f: (st.blk[f] / targets[f], cs.FAMS.index(f)))
            if not cand:
                break
            f = cand[0]
            mark(f)
            taken, n, why = composite(st, refill_cells(f), lambda v, f=f: ((), got[(f, v)]), max_rows=room[f],
                                      first_quota=False)
            if n is None:
                if why == "spent":
                    rspent.add(f)
                continue
            trace(f"refill{rnd}", f, "refill", taken)
            new = [r for v in taken for r in got[(f, v)]]
            for v in taken:
                used.add((f, v))
            refill_log[f].append((taken, new))
            added.extend(new)
            added_rels.extend(pools[f].rels_of({r["id"] for r in new}))
            ever.update({r["id"]: (f, r) for r in new})
            refilled[f] += n
            refill_moves[f] += 1
            deficit -= n

    def give_back() -> int:
        """A family above lim12 of the realised own rows (12% while it holds refill rows; fewer own rows after a
        remainder) gives back its refill moves, the latest first, while the state before that move still passes."""
        nonlocal deficit
        back = 0
        while True:
            own = own_rows()
            over = [f for f in fams if refill_log[f] and over12(f, own)]
            if not over:
                return back
            f = max(over, key=lambda f: (st.blk[f] - lim12(f) * own, -cs.FAMS.index(f)))
            taken, new = refill_log[f][-1]
            st.move(out=new)
            if not st.passes():
                st.rollback()
                refill_log[f].clear()                  # an earlier state that no longer passes: kept, see shrink
                continue
            st.commit()
            refill_log[f].pop()
            ids = {r["id"] for r in new}
            added[:] = [r for r in added if r["id"] not in ids]
            added_rels[:] = [x for x in added_rels if x["a"] not in ids and x["b"] not in ids]
            for v in taken:
                used.discard((f, v))
                rcells[f].drop(v)
                cur_cells[f][_csig(pools[f], pools[f].raw_of(v))] -= len(got[(f, v)])
            for i in ids:
                ever.pop(i, None)
            refilled[f] -= len(new)
            given_back[f] += len(new)
            deficit += len(new)
            back += len(new)

    def shrink12(rnd) -> int:
        """A family still above m = lim12(f) of the realised own rows (its share rose because the own rows fell)
        drops whole units, composite moves over its cells with every rule kept, at least the closed-form
        x = ceil((rows - m x own) / (1 - m)) rows; they join the remainder."""
        nonlocal deficit
        moved = 0
        for f in sorted(mshare, key=cs.FAMS.index):
            if not over12(f) or f not in pools:
                continue
            m, own = lim12(f), own_rows()
            x = math.ceil((st.blk[f] - m * own) / (1 - m) - 1e-9)
            cells = drop_cells(f"s12_{rnd}", f)
            cells.quota = lambda u: True
            done = 0
            while done < x and over12(f):
                mark(f)
                taken, n, why = composite(st, cells, lambda u: (units[u], ()))
                if n is None:
                    if why == "stuck":
                        trims[f]["stuck_moves"] += 1
                        continue
                    break
                trace(f"s12_{rnd}", f, "drop", taken)
                for u in taken:
                    gone.update(r["id"] for r in units[u])
                    trims[f]["long_rows_removed"] += lrows(u)
                    trims[f]["long_tokens_removed"] += ltoks(u)
                trims[f]["dropped_rows"] += n
                trims[f]["dropped_units"] += len(taken)
                trims[f]["share12_rows"] += n
                trims[f]["composite_moves"] += 1
                deficit += n
                done += n
            moved += done
        return moved

    # ---- the trim: p1 (spec 6's bin, while long tokens > 30%), then p2 rounds while a cap fails
    if not st.ok(row=False):
        need = math.ceil((st.lt - LONG_TOK_SHARE * st.t) / (1 - LONG_TOK_SHARE))
        w6 = Counter()
        for u in units:
            if in6(u):
                w6[u[0]] += ltoks(u)
        if w6:
            run_phase("p1", 0, "tokens", need, w6)
            refill(0)
            give_back()
    rnd = 0
    while True:
        moved = 0
        if not st.ok():
            rnd += 1
            if st.shares()[0] > LONG_ROW_SHARE:
                measure, need = "rows", st.ln - math.floor(LONG_ROW_SHARE * st.n)
                w = {b: a[2] - math.floor(LONG_ROW_SHARE * a[0]) for b, a in st.bc.items() if st.over_own_cap(b)}
            else:
                measure, need = "tokens", math.ceil((st.lt - LONG_TOK_SHARE * st.t) / (1 - LONG_TOK_SHARE))
                w = {b: math.floor(a[3] - LONG_TOK_SHARE * a[1]) for b, a in st.bc.items() if st.over_own_cap(b)}
            moved = run_phase("p2", rnd, measure, need, w)
            refill(rnd)
        give_back()
        shrunk = shrink12(rnd)
        if shrunk:
            refill(rnd)
            give_back()
        if (st.ok() and not any(over12(f) for f in mshare)) or not (moved or shrunk):
            break
    last = {"rounds": rnd, "cap_after": [round(x, 6) for x in st.shares()]}
    handled |= gone
    rows = [r for r in rows if r["id"] not in gone] + added
    kid = {r["id"] for r in rows}
    rels = [x for x in rels if x["a"] in kid and x["b"] in kid] + added_rels
    n_rep = sum(1 for r in rows if r["_block"] == "replay")
    cut = max(0, n_rep - math.floor(1.5 * st.n)) if deficit else 0
    if cut:
        rows, rels = shrink_replay(rows, rels, pools, ctx, cut, info)
    n_rep1 = sum(1 for r in rows if r["_block"] == "replay")
    a1 = st.shares()
    delta = Counter()
    for b, t in trims.items():
        delta[b] -= t["dropped_rows"]
    delta.update(refilled)
    touched = sorted({b for b, t in trims.items() if t["swapped_out_rows"] or t["dropped_rows"]} | set(refilled))
    by_blk = defaultdict(list)
    for r in rows:
        if r["_block"] in touched:
            by_blk[r["_block"]].append(r)
    fin = A28State(rows, ntok, side)                    # end-of-trim audit: recounted from the final rows
    fin.c0, fin.blk0, fin.cardflag, fin.cardcarry = st.c0, st.blk0, st.cardflag, st.cardcarry
    audit = fin.audit()
    own1 = sum(st.blk[f] for f in cs.FAMS)
    pub1 = Counter(r["source"] for r in rows if r["_block"] == "public")
    com1 = Counter(cs.commit_group(r) for r in rows if r["_block"] == "COMMIT")
    info.update({
        "plan": plan, "last_move": last,
        "trims_by_block": {b: {k: t[k] for k in TRIM_KEYS} | {"rows_before": n0[b], "long_rows_before": long0[b],
                                         "rows_lost_pct": round(100 * t["dropped_rows"] / max(1, n0[b]), 1),
                                         "drop_bound_rows": bound(b, 0, 0)}
                           for b, t in sorted(trims.items())},
        "swapped_in_rows_by_block": dict(swapped_in),
        "public_rows_by_source_changed": {k: [pub0[k], pub1[k]] for k in sorted(set(pub0) | set(pub1))
                                          if pub0[k] != pub1[k]},
        "commit_rows_by_type_view_changed": {k: [com0[k], com1[k]] for k in sorted(set(com0) | set(com1))
                                             if com0[k] != com1[k]},
        "refill_families": fams, "refilled_rows_by_family": dict(refilled), "refill_moves": dict(refill_moves),
        "refill_given_back_12pct": dict(given_back), "refill_spent_families": sorted(rspent),
        "refill_targets": dict(tally), "remainder_rows": deficit, "replay_cut": cut,
        "replay_after": {"rows": n_rep1, "new_rows": st.n,
                         "replay_share": round(n_rep1 / max(1, n_rep1 + st.n), 4),
                         "rule": "a remainder sets replay = floor(1.5 x realised new rows); else replay is untouched"},
        "after": {"new_rows": st.n, "long_rows": st.ln, "new_tokens": st.t, "long_tokens": st.lt,
                  "long_row_share": round(a1[0], 4), "long_token_share": round(a1[1], 4), "cap_met": st.ok()},
        "blocks": {b: {"before": blocks0.get(b), "after": {
            "rows": a[0], "long_rows": a[2], "long_row_share": round(a[2] / max(1, a[0]), 4),
            "long_token_share": round(a[3] / max(1, a[1]), 4)}} for b, a in sorted(st.bc.items())},
        "over_cap_blocks_after": sorted(b for b in st.bc if st.over_own_cap(b)),
        "rows_by_block": {b: st.blk[b] for b in sorted(st.blk)},
        "family_rows_target_limit": {f: [st.blk[f], targets[f], cap15[f],
                                         round(st.blk[f] / max(1, own1), 4), round(share0[f], 4)] for f in fams},
        "family_share_limit": {f: round(lim12(f), 4) for f in sorted(mshare, key=cs.FAMS.index)},
        "own_rows": [own0, own1],
        "bin_shares_touched": {b: {k: round(v / max(1, st.blk[b]), 4) for k, v in sorted(st.c[("bins", b)].items())
                                   if v} for b in touched},
        "label_x_bin_min_p_touched": {b: (round(min(p), 4) if p else None)
                                      for b, p in ((b, label_bin_p(by_blk[b])) for b in touched)},
        "composition_touched": {b: fin.report(b) for b in touched},
        "guard_audit_breaks": audit[:30], "guard_audit_break_count": len(audit),
        "expected": {"family_delta": {f: delta[f] for f in cs.FAMS if delta[f]},
                     "own_delta": sum(delta[f] for f in cs.FAMS), "public_delta": delta["public"],
                     "commit_delta": delta["COMMIT"], "replay_delta": -cut,
                     "total_delta": sum(delta.values()) - cut}})
    probs = []
    if not st.ok():
        probs.append(f"A28 token cap not met after the trim (quotas could not be met): long rows {a1[0]:.4f}, long "
                     f"tokens {a1[1]:.4f}")
    big = {f: st.blk[f] for f in mshare if over12(f, own1) or (f in cap15 and st.blk[f] > cap15[f])}
    if big:
        probs.append(f"A26 (b) / spec 2.1: families above 1.5x target or their share limit (12% with refill rows, "
                     f"else max(12%, pre-trim share)) of the realised own rows {big}")
    if delta["public"] or delta["COMMIT"] or info["public_rows_by_source_changed"] or \
            info["commit_rows_by_type_view_changed"]:
        probs.append("A28 trim changed public / commit rows; they stay as specced (A26 b, spec 3.2 / 4.2)")
    if audit:
        probs.append(f"A28 trim: {len(audit)} spec 2.1 / G9 / G10 rules broken or worse after the trim: {audit[:6]}")
    log(f"A28 cap trim: long rows {b0[0]:.4f} -> {a1[0]:.4f}, long tokens {b0[1]:.4f} -> {a1[1]:.4f}; swapped "
        f"{sum(t['swapped_out_rows'] for t in trims.values())} rows, dropped "
        f"{sum(t['dropped_rows'] for t in trims.values())}, refilled {sum(refilled.values())}, remainder {deficit}, "
        f"replay cut {cut}, audit breaks {len(audit)}")
    return rows, rels, probs


# ------------------------------------------------------------------ G10 aggregate checks (new rows)

ABSTAIN = re.compile(r"not enough information|cannot be determined|can't be determined|none of (these|the above)|"
                     r"insufficient (information|evidence)|unknown from the|not stated", re.I)


G10_SIDE: dict = {}     # finish() sets it to ctx['sidecar'] (the families' quota fields + inv twins) for g10_checks


def g10_checks(rows, rep, final, side=None) -> list[str]:
    from scipy.stats import binomtest, chisquare, chi2_contingency
    sys.path.insert(0, str(LEAN / "c_src/common"))
    import negcount
    new = [r for r in rows if r["_block"] != "replay"]
    out, probs, side = {}, [], G10_SIDE if side is None else side
    hard = [r for r in new if r["qtype"] == "noul" and not own_target(r.get("meta") or {})]
    fam_rate, cells = defaultdict(list), defaultdict(list)
    for r in hard:
        m = r.get("meta") or {}
        fam_rate[r["_block"]].append(int(r["gold"]))
        cells[(r["_block"], str(m.get("wording_id")), str(m.get("difficulty_bin")),
               negcount.k_all(r["instructions"]))].append(int(r["gold"]))
    agg = {b: round(sum(v) / len(v), 4) for b, v in fam_rate.items()}
    # spec G10: 50 +/- 2 per family x wording x bin x negation-count cell. Cells with >= 50 rows: the band itself;
    # smaller cells: a binomial test (p < 0.01), since +/- 2 pp is below one row there.
    lit = sorted((k for k, v in cells.items() if len(v) >= 50 and abs(sum(v) / len(v) - 0.5) > 0.02 + 1e-12),
                 key=lambda k: -abs(sum(cells[k]) / len(cells[k]) - 0.5))
    sig = [k for k, v in cells.items() if len(v) < 50 and binomtest(sum(v), len(v), 0.5).pvalue < 0.01]
    show = lambda k: "|".join(map(str, k)) + f" n={len(cells[k])} yes={sum(cells[k]) / len(cells[k]):.3f}"  # noqa: E731
    out["yes_rate"] = {"aggregate_by_block": agg, "cells": len(cells), "cells_n_ge_50": sum(len(v) >= 50 for v in
                                                                                        cells.values()),
                       "cells_n_ge_50_outside_2pp": len(lit), "cells_n_lt_50_binom_p_lt_0.01": len(sig),
                       "outside_2pp": [show(k) for k in lit[:20]], "small_binom": [show(k) for k in sig[:20]]}
    bad_agg = [b for b, x in agg.items() if abs(x - 0.5) > 0.02 and not b.startswith("c_pub")]
    if bad_agg:
        probs.append(f"G10 aggregate yes rate outside 50 +/- 2: {bad_agg}")
    for k in lit:
        probs.append(f"G10 yes-rate cell outside 50 +/- 2 (family|wording|bin|negation): {show(k)}")
    if sig:
        probs.append(f"G10 {len(sig)} small yes-rate cells (< 50 rows) with binomial p < 0.01: "
                     f"{[show(k) for k in sig[:6]]}")
    pos, lng = defaultdict(Counter), defaultdict(lambda: [0.0, 0.0, 0])
    abst_n, abst_gold, att = 0, 0, defaultdict(Counter)
    for r in new:
        m = r.get("meta") or {}
        if r["qtype"] == "choice" and r.get("gold") in (r.get("options") or []):
            o = r["options"]
            k = len(o)
            if not isinstance(m.get("option_level"), dict):
                pos[(r["_block"], k)][o.index(r["gold"])] += 1
            if k >= 2:                      # "longest option is gold": 1/m credit when m options tie for longest
                lens = [len(str(x)) for x in o]
                top = [i for i, x in enumerate(lens) if x == max(lens)]
                c = lng[r["_block"]]
                c[0] += (1 / len(top)) if o.index(r["gold"]) in top else 0.0
                c[1] += 1 / k
                c[2] += 1
            if any(ABSTAIN.search(str(x)) for x in o):
                abst_n += 1
                abst_gold += bool(ABSTAIN.search(str(r["gold"])))
        if r["qtype"] == "noul" and not own_target(m):
            a = is_attack(r, side.get(r["id"]) if r["_block"] in cs.FAMS else None)      # ATTACK_RULE (own rows)
            att[a][int(r["gold"])] += 1
    pos_p = {f"{b}|k{k}": round(chisquare([c[j] for j in range(k)]).pvalue, 4)
             for (b, k), c in pos.items() if sum(c.values()) >= 5 * k}
    bad_pos = sorted(x for x, p in pos_p.items() if p <= 0.01)
    lgb = {b: round(100 * (v[0] - v[1]) / v[2], 2) for b, v in lng.items() if v[2]}
    bad_lg = sorted(b for b, x in lgb.items() if abs(x) > 2.0)
    lg = sum(v[0] - v[1] for v in lng.values()) / max(1, sum(v[2] for v in lng.values()))
    att_p = chi2_contingency([[att[False][0], att[False][1]], [att[True][0], att[True][1]]])[1] \
        if att[True] and att[False] and min(sum(att[True].values()), sum(att[False].values())) > 0 else None
    out |= {"gold_position_chi2_p": pos_p, "gold_position_fail": bad_pos,
            "longest_option_gold_minus_1_over_k_pp": round(100 * lg, 2), "longest_by_block_pp": lgb,
            "abstain_rows": abst_n, "abstain_gold_share": round(abst_gold / max(1, abst_n), 4),
            "attack_x_label_p": att_p}
    if bad_pos:
        probs.append(f"G10 gold position not uniform (chi2 p <= 0.01): {bad_pos[:6]}")
    if bad_lg:
        probs.append(f"G10 longest-option-is-gold off 1/k by > 2 pp in {bad_lg} ({ {b: lgb[b] for b in bad_lg} })")
    if abst_n and abst_gold / abst_n > 0.5:
        probs.append("G10 abstain option is gold on > 50% of rows that show one")
    if att_p is not None and att_p <= 0.01:
        probs.append("G10 attack presence correlates with the label")
    probs += ordinal_balance(new, out)
    rep["g10"] = out | {"problems": probs}
    return probs


def ordinal_balance(new, out) -> list[str]:
    """F7: each level 1/K +/- 2 pp per sampler x K; commit score: each level >= 1/K - 5 pp per rubric (card)."""
    f7, sc = defaultdict(Counter), defaultdict(Counter)
    for r in new:
        ol = (r.get("meta") or {}).get("option_level")
        if not isinstance(ol, dict):
            continue
        k = len(ol)
        if r["_block"] == "F7":
            f7[(r["meta"].get("sampler"), k)][ol[r["gold"]]] += 1
        elif r["_block"] == "COMMIT":
            sc[(r["meta"].get("card_id"), k)][ol[r["gold"]]] += 1
    bad7 = [f"{s}|K{k}" for (s, k), c in f7.items()          # a cell within one row of uniform passes (discreteness)
            if any(abs(c[j] / sum(c.values()) - 1 / k) > 0.02 for j in range(k))
            and max(c[j] for j in range(k)) - min(c[j] for j in range(k)) > 1]
    badc = [f"{s}|K{k}" for (s, k), c in sc.items() if any(c[j] / sum(c.values()) < 1 / k - 0.05 for j in range(k))]
    out["ordinal_levels"] = {"f7_cells": len(f7), "f7_cells_off_2pp": bad7[:20], "commit_rubrics": len(sc),
                             "commit_rubrics_level_short": badc[:20]}
    return ([f"G10 F7 level shares off 1/K +/- 2 pp in {len(bad7)} sampler x K cells"] if bad7 else []) + \
        ([f"G10 commit score level floor missed in {len(badc)} rubrics"] if badc else [])


def commit_counts(rows, rep, target=SHARES_R1["commit"]) -> list[str]:
    """G10 / spec 4.2 on the final commit rows: exactly target / 5 rows per type (route, triage, score, gate, match)
    and 30% message-only rows of route, triage and gate (r1 360 each; none for score or match)."""
    want = cs.commit_subtargets(target)
    got = Counter(cs.commit_group(r) for r in rows if r["_block"] == "COMMIT")
    by_type = Counter()
    for g, n in got.items():
        by_type[g.split("|")[0]] += n
    rep["commit_4_2"] = {"groups": {g: [got.get(g, 0), want.get(g, 0)] for g in sorted(set(want) | set(got))},
                         "by_type": dict(by_type)}
    if not got:
        return []                                  # no commit block yet: the share check reports it
    bad = [f"{g} {got.get(g, 0)} vs {want.get(g, 0)}" for g in sorted(set(want) | set(got)) if got.get(g, 0) !=
           want.get(g, 0)]
    return [f"G10 commit type / message-only counts differ from spec 4.2: {bad}"] if bad else []


# ------------------------------------------------------------------ config fill (recipe 2 / A16)

def config_fill(rows, rels) -> dict:
    """epochs = 16 / measured rows per step (a CPU dry run of train_decoder.batches() on the final rows, seeded as the
    run); expect_ord_rows, expect_kd_targets (kd_skip_src applied), expect_kd_full (kd_full_src yes/no rows)."""
    sys.path.insert(0, str(LEAN))
    import train_decoder as td
    clean = [{k: v for k, v in r.items() if k != "_block"} for r in rows]
    if len(clean) < 2 * BATCH:
        raise ValueError(f"config_fill: {len(clean)} rows; batches() never yields a step below {BATCH} rows")
    units, merged = td.make_units(clean, rels)
    st = random.getstate()
    try:
        random.seed(SEED)
        gen = td._BATCHES(list(units), BATCH)
        n_steps = math.ceil(len(clean) / BATCH)
        drawn = sum(len(next(gen)) for _ in range(n_steps))
    finally:
        random.setstate(st)
    per_step = drawn / max(1, n_steps)
    kd_rows = [r for r in clean if td.kd_target(r) is not None and (r.get("meta") or {}).get("teacher_src")
               not in KD_SKIP_SRC]
    return {"epochs": round(BATCH / per_step, 4), "measured_rows_per_step": round(per_step, 4),
            "dry_run_steps": n_steps, "units": len(units), "inv_merged": merged,
            "expect_ord_rows": sum(1 for r in clean if td.is_ordinal(r)),
            "expect_kd_targets": len(kd_rows),
            "expect_kd_full": sum(1 for r in kd_rows if r["source"] in KD_FULL_SRC and r["qtype"] == "noul"),
            "seed": SEED}


def check_rows(rows, rep) -> list[str]:
    sys.path.insert(0, str(LEAN))
    import train_decoder as td
    try:
        td.check_rows([{k: v for k, v in r.items() if k != "_block"} for r in rows], KD)
        rep["check_rows"] = {"rows": len(rows), "ok": True}
        return []
    except ValueError as e:
        rep["check_rows"] = {"rows": len(rows), "ok": False, "error": str(e)[:600]}
        return [f"train_decoder.check_rows: {str(e)[:200]}"]


def drop_units(rows, rels, ids: set) -> tuple[list, list, int]:
    """Drop the whole call_id units of `ids` (decontam and deny-list drops: the training unit)."""
    cids = {r["call_id"] for r in rows if r["id"] in ids}
    keep = [r for r in rows if r["call_id"] not in cids]
    kid = {r["id"] for r in keep}
    return keep, [x for x in rels if x["a"] in kid and x["b"] in kid], len(rows) - len(keep)


def drop_rows(rows, rels, ids: set) -> tuple[list, list]:
    keep = [r for r in rows if r["id"] not in ids]
    kid = {r["id"] for r in keep}
    return keep, [x for x in rels if x["a"] in kid and x["b"] in kid]


REFILL_ROUNDS = 6


def _sig(keys) -> tuple:
    return tuple(sorted(repr(k) for k in keys))


def match_units(pieces, cands, pool, accept, tally):
    """Fill each lost piece (a list of row keys, one per lost row of one unit) with one whole unused unit of the same
    refill group, tier by tier: same fine-key multiset, then same mid-key multiset, then same coarse-key multiset (so
    the same row count). Candidates are taken in the pool's seeded order; accept() runs every per-row gate on the
    unit and returns its rows, or None (the unit is then never tried again). Returns ([(unit, rows)], tiers, left)."""
    got, tiers = [], Counter()
    nlev = len(pieces[0][0]) if pieces else 0
    for t in range(nlev):
        if not pieces:
            break
        index = defaultdict(deque)
        for u in cands:
            if u not in pool.tried:
                index[_sig(pool.keys_of(r)[t] for r in pool.raw_of(u))].append(u)
        left = []
        for p in pieces:
            q, rows = index.get(_sig(k[t] for k in p)), None
            while q:
                u = q.popleft()
                if u in pool.tried:
                    continue
                pool.tried.add(u)
                rows = accept(pool, u, tally)
                if rows is not None:
                    break
            if rows is None:
                left.append(p)
            else:
                got.append((u, rows))
                tiers[f"tier{t + 1}"] += 1
        pieces = left
    return got, tiers, pieces


def refill(pools: dict, rows, ever: dict, handled: set, accept, rep_refill) -> tuple[list, list]:
    """Refill every row that entered the mix (assembled or refilled) and is gone now, block by block and group by
    group (replay / public: the row's source; own / commit: one group, tiers carry stratum and bin). Rows lost from a
    block without a pool stay unfilled (counted). Returns (new rows, their relations)."""
    cur = {r["id"] for r in rows}
    lost = defaultdict(lambda: defaultdict(lambda: defaultdict(list)))
    for i, (blk, r) in ever.items():
        if i in cur or i in handled:
            continue
        handled.add(i)
        st = rep_refill.setdefault(blk, {"lost_rows": 0, "refilled_rows": 0, "refilled_units": 0, "tiers": Counter(),
                                         "unfilled_rows": 0, "targets": Counter()})
        st["lost_rows"] += 1
        pool = pools.get(blk)
        if pool is None:
            st["unfilled_rows"] += 1
            continue
        lost[blk][pool.group_row(r)][pool.unit_of.get(i, i)].append(pool.keys_of(r))
    add, add_rels = [], []
    for blk, groups in lost.items():
        pool, st = pools[blk], rep_refill[blk]
        for g, pieces in sorted(groups.items()):
            got, tiers, left = match_units(list(pieces.values()), pool.cands.get(g, []), pool, accept, st["targets"])
            for u, rr in got:
                add += rr
                add_rels += pool.rels_of({r["id"] for r in rr})
                st["refilled_rows"] += len(rr)
                st["refilled_units"] += 1
            st["tiers"].update(tiers)
            st["unfilled_rows"] += sum(len(p) for p in left)
    return add, add_rels


def e2_final(ctx, rows, rep) -> list[str]:
    """Spec 5 E2 re-run on the final replay rows (after drops and refills): wording cells with >= 50 hard yes/no
    rows must sit inside 50 +/- 5."""
    rs = rs_mod()
    cur = {r["id"] for r in rows if r["_block"] == "replay"}
    sub = defaultdict(lambda: {"rows": []})
    for u, x in enumerate(ctx["units"]):
        for i in x["rows"]:
            if ctx["lt"][i]["id"] in cur:
                sub[u]["rows"].append(i)
    fin = rs.e2_report(ctx["lt"], sub, sorted(sub), sticky=ctx["sticky"])
    rep["e2"]["final"] = fin
    return [f"E2: {fin['cells_out_of_band']} replay wording cells (>= 50 hard yes/no rows) outside 50 +/- 5 after "
            f"drops and refills"] if fin["cells_out_of_band"] else []


PUBLIC_QC = "qc/QC_REPORT.json"           # per public builder, the same convention as the families


def final_blockers(ilog, fams, builders=None) -> list[str]:
    """What --final refuses before reading anything else: a family / commit QC_REPORT.json that is missing, not
    pass=true, or not tied (full sha256) to the candidates and relation files on disk; the same for each public
    builder's QC record (its rows and reserve files); missing crowd score files. --dry-run lists them."""
    out = []
    for fam in fams:
        f = cs.fam_files(fam)
        if not f["qc"].exists():
            out.append(f"{fam}: no QC_REPORT.json")
            continue
        qc = ilog.json(f["qc"])
        if qc.get("pass") is not True:
            out.append(f"{fam}: QC_REPORT.json pass is not true")
        files = {f["cand"].name: f["cand"]} | ({f["rel"].name: f["rel"]} if f["rel"] else {})
        out += [f"{fam}: QC_REPORT.json {p}" for p in qc_binding(qc, files)]
    base = LEAN / "c_src/public"
    for rows_rel, res_rel in zip(PUBLIC_FILES, PUBLIC_RESERVE):
        b = rows_rel.split("/")[0]
        if builders is not None and b not in builders:
            continue
        qp = base / b / PUBLIC_QC
        if not qp.exists():
            out.append(f"{b}: no QC record ({b}/{PUBLIC_QC}; spec 8: public rows pass G1/G5/G6/G7/G10/G12/G13/G15)")
            continue
        qc = ilog.json(qp)
        if qc.get("pass") is not True:
            out.append(f"{b}: {PUBLIC_QC} pass is not true")
        files = {Path(x).name: base / x for x in (rows_rel, res_rel) if (base / x).exists()}
        out += [f"{b}: {PUBLIC_QC} {p}" for p in qc_binding(qc, files)]
    out += [p for fam in fams for p in cs.crowd_complete(fam)]
    return out


PUBLIC_BUILDERS = [r.split("/")[0] for r in PUBLIC_FILES]


def include_sets(names):
    """--include: the sources that enter the mix (families F*, COMMIT, public builders public-N). None = all."""
    if names is None:
        return None
    bad = sorted(set(names) - set(cs.FAMS + ["COMMIT"] + PUBLIC_BUILDERS))
    if bad:
        raise SystemExit(f"--include: unknown source names {bad} (use F1..F13, COMMIT, public-1/2/3)")
    return {"names": set(names), "public": [b for b in PUBLIC_BUILDERS if b in names]}


def fallback_rows_incl(ilog, builders) -> dict:
    """cs.fallback_rows restricted to the included public builders (a left-out builder moves no rows)."""
    out = Counter()
    for b in builders:
        for m in sorted((LEAN / "c_src/public" / b).glob("**/manifest*.json")):
            if "tmp" in m.parts:
                continue
            c = (ilog.json(m) or {}).get("counts") or {}
            for k, v in c.items():
                mm = re.fullmatch(r"(f\d+)_fallback_rows_r1", k)
                if mm and isinstance(v, int):
                    out[mm.group(1).upper()] += v
    return dict(out)


# ------------------------------------------------------------------ build

def build(a) -> dict:
    t0 = time.time()
    ilog, rep, probs = InputLog(), {"mode": "final" if a.final else "dry-run", "seed": SEED, "shares_r1": SHARES_R1}, []
    rs = rs_mod()
    if a.final:
        why = rs.sealed_sha_problem(a.sealed_sha or "") or (None if a.sealed_sha == A15_SUITE_SHA else "not A15's")
        if why:
            raise SystemExit(f"--final: sealed sha refused ({why})")
    incl = include_sets(a.include)
    if incl is None:
        fb = cs.fallback_rows(ilog)
        targets = cs.family_targets(ilog)
    else:
        fb = fallback_rows_incl(ilog, incl["public"])
        targets = {f: t + fb.get(f, 0) for f, t in cs.TARGET_R1.items()}
    fams = cs.available(cs.FAMS)
    commit_in = incl is None or "COMMIT" in incl["names"]
    a34 = incl is not None                  # PREREG A34: --include = the round-1 scope ruling (c) / (e)
    if incl is not None:
        fams = [f for f in fams if f in incl["names"]]
        rep["include"] = {"requested": a.include, "families_entered": fams, "commit_entered": commit_in,
                          "public_entered": incl["public"],
                          "left_out": [n for n in cs.FAMS + ["COMMIT"] + PUBLIC_BUILDERS if n not in incl["names"]],
                          "rule": "PREREG A34 (round 1 = the included sources); a source not in --include is a "
                                  "missing source (no rows, no pool, no QC / crowd guard); its share lowers the total "
                                  "(A34 c: no A26 (b) refill from extras). Every guard applies to every included "
                                  "source (A34 d)."}
    rep["fallbacks"] = {"rows_moved_public_to_own": fb, "rule": "spec 3.2 (named fallback; 3B -> F13)"}
    blockers = final_blockers(ilog, fams + (cs.available(["COMMIT"]) if commit_in else []),
                              None if incl is None else incl["public"])
    rep["final_blockers"] = blockers
    if a.final and blockers:
        raise SystemExit("--final refused:\n  " + "\n  ".join(blockers))
    # own families, public, commits (assembled before the replay: PREREG A34 (c) sizes the replay trim from them)
    fblk = []
    for fam in fams:
        fr, frel, par, fpool = family_block(ilog, fam, targets[fam], a.final, rep, probs, a34)
        if a34:
            targets[fam] = len(fr)          # A34 (c) / (e): own expectation = the family's realised selected rows
        fblk.append((fam, fr, frel, par, fpool))
    exp_pub = SHARES_R1["public"] - sum(fb.values())
    pub, reserve, ppar = public_block(ilog, exp_pub, rep, probs, None if incl is None else incl["public"])
    cr, crel, cpar, cpool = commit_block(ilog, SHARES_R1["commit"], a.final, rep, probs, commit_in)
    replay_total = SHARES_R1["replay"]
    if a34:
        exp_pub = len(pub)                  # A34 (c): public = the included public builders' rows
        exp_com = SHARES_R1["commit"] if commit_in else 0
        new0 = sum(targets[f] for f in fams) + exp_pub + exp_com
        rep_x = math.floor(A34_REPLAY_X * new0)
        rep["a34"] = {"applied": True, "include": list(a.include),
                      "rule": "PREREG A34 (c) / (e): own = the included families' realised selected rows (a family "
                              "short of its target only because G13 removed units enters as-is); public = the "
                              "included public builders' rows; commit = 0 unless included; replay = floor(1.5 x new "
                              "rows) (the replay is trimmed to it, shrink_replay); total = new + replay; no A26 (b) "
                              "refill from extras; every other gate unchanged (A34 d)",
                      "a34_e_families": {f: rep["own"][f]["a34_e"] for f in fams if "a34_e" in rep["own"].get(f, {})},
                      "a26b_refill_applied": False,
                      "expected": {"own": sum(targets[f] for f in fams), "own_by_family": {f: targets[f] for f in fams},
                                   "public": exp_pub, "commit": exp_com, "new": new0, "replay": rep_x,
                                   "total": new0 + rep_x}}
        replay_total = rep_x
    # replay
    rows_r, lt, units, kept, rels_r, flags, c1p = load_replay(ilog, rep)
    kept, rep["old_slice"] = old_slice_clash(ilog, rows_r, lt, units, kept, rs)
    sel, pool = trim_replay(ilog, lt, units, kept, rep, total=replay_total, scale=a34)
    sel, pool, sticky = e2_restratify(lt, units, sel, pool, rep)
    log(f"replay: {sum(len(units[u]['rows']) for u in sel):,} rows after trim + E2 ({time.time() - t0:.0f}s)")
    rpool = replay_pool(rows_r, lt, units, pool, rels_r, flags, c1p)
    cnt = Counter()
    pos = {lt[i]["id"]: i for u in sel for i in units[u]["rows"]}
    replay = sorted((r for u in sel for r in rpool.rows_of(u, cnt)), key=lambda r: pos[r["id"]])
    rpool.tried |= set(sel)
    rid = {r["id"] for r in replay}
    rels = [x for x in rels_r if x["a"] in rid and x["b"] in rid]
    rep["replay_targets"] = {k: v for k, v in cnt.items() if not k.startswith("option_level:")} | \
        {"option_level_detected": {k.split(":", 1)[1]: v for k, v in cnt.items() if k.startswith("option_level:")}}
    ctx = {"lt": lt, "units": units, "sticky": sticky, "sidecar": sidecar_flags(ilog, fams)}
    rows, parents, pools = list(replay), {}, {"replay": rpool}
    for fam, fr, frel, par, fpool in fblk:
        rows += [r | {"_block": fam} for r in fr]
        rels += frel
        if fpool is not None:
            pools[fam] = fpool
        if par is not None:
            for s in {r["source"] for r in fr} | fpool.sources:
                parents[s] = par
    rows += [r | {"_block": "public"} for r in pub]
    parents |= ppar
    pools["public"] = public_pool(reserve)
    rows += [r | {"_block": "COMMIT"} for r in cr]
    rels += crel
    if cpool is not None:
        pools["COMMIT"] = cpool
        if cpar is not None:
            for s in {r["source"] for r in cr} | cpool.sources:
                parents[s] = cpar
    dup = [k for k, v in Counter(r["id"] for r in rows).items() if v > 1]
    if dup:
        probs.append(f"{len(dup)} duplicate row ids across blocks, e.g. {dup[:3]}")
    log(f"assembled {len(rows):,} rows ({time.time() - t0:.0f}s)")
    return finish(a, ilog, rep, probs, rows, rels, parents, pools, ctx, exp_pub, targets, fams, fb, t0)


def _a34f_e2_cells(rows, ctx):
    """PREREG A34 (f) (ii): the E2 wording cells of the replay rows now in the mix, scored exactly as e2_final does
    (replay_sample.cell_defs on the current units). Returns (cell -> [(unit, gold)], unit -> its current row ids)."""
    rs, lt = rs_mod(), ctx["lt"]
    cur = {r["id"] for r in rows if r["_block"] == "replay"}
    sub = defaultdict(lambda: {"rows": []})
    for u, x in enumerate(ctx["units"]):
        for i in x["rows"]:
            if lt[i]["id"] in cur:
                sub[u]["rows"].append(i)
    cell_of = rs.cell_defs(lt, sub, sorted(sub))
    cells, ids = defaultdict(list), {u: {lt[i]["id"] for i in v["rows"]} for u, v in sub.items()}
    for u in sorted(sub):
        for i in sub[u]["rows"]:
            if rs.hard_yn(lt[i]):
                cells[cell_of(lt[i])].append((u, int(lt[i]["gold"])))
    return cells, ids


def _a34f_e2_ok(n, y):
    rs = rs_mod()
    return n < rs.MIN_CELL or rs.BAND[0] <= y / n <= rs.BAND[1]


def _a34f_g10_cells(rows):
    """PREREG A34 (f) (ii): the G10 yes-rate cells (family|wording|bin|negation) exactly as g10_checks keys them;
    the unit is the call_id training unit (drop_units)."""
    sys.path.insert(0, str(LEAN / "c_src/common"))
    import negcount
    cells, ids = defaultdict(list), defaultdict(set)
    for r in rows:
        if r["_block"] == "replay" or r["qtype"] != "noul" or own_target(r.get("meta") or {}):
            continue
        m = r.get("meta") or {}
        k = (r["_block"], str(m.get("wording_id")), str(m.get("difficulty_bin")), negcount.k_all(r["instructions"]))
        cells[k].append((r["call_id"], int(r["gold"])))
        ids[r["call_id"]].add(r["id"])
    return cells, ids


def _a34f_g10_ok(n, y):
    from scipy.stats import binomtest
    if n >= 50:
        return abs(y / n - 0.5) <= 0.02 + 1e-12
    return n == 0 or binomtest(y, n, 0.5).pvalue >= 0.01


def _a34f_balance(rows, rels, tag, cells_fn, ok, targets, log, rounds=200):
    """PREREG A34 (f) (ii): a cell outside its band is fixed by seeded down-sampling of its majority label inside that
    cell: whole units holding only majority rows of the cell, smallest first (seeded order within a size), removed
    until the cell is inside the band; then every cell is re-scored. Rows are only removed; a cell the majority-only
    units cannot fix is left untouched for the gate to report."""
    skip = set()
    for _ in range(rounds):
        cells, ids = cells_fn(rows)
        rate = {k: sum(g for _, g in v) / len(v) for k, v in cells.items() if v}
        bad = sorted((k for k, v in cells.items() if v and str(k) not in skip and not ok(len(v), sum(g for _, g in v))),
                     key=lambda k: (-abs(rate[k] - 0.5), str(k)))
        if not bad:
            break
        k = bad[0]
        n, y = len(cells[k]), sum(g for _, g in cells[k])
        maj = int(2 * y > n)
        per = defaultdict(lambda: [0, 0])
        for u, g in cells[k]:
            per[u][0 if g == maj else 1] += 1
        cand = sorted((u for u, (a, b) in per.items() if b == 0), key=str)
        random.Random(f"{SEED}|A34f|{tag}|{k}").shuffle(cand)
        cand.sort(key=lambda u: len(ids[u]))
        drop = set()
        for u in cand:
            if ok(n, y):
                break
            drop |= ids[u]
            n -= per[u][0]
            y -= per[u][0] * maj
        if not drop or not ok(n, y):
            skip.add(str(k))
            log["unfixed"].append(str(k))
            continue
        before = Counter(r["_block"] for r in rows)
        rows, rels, _ = drop_units(rows, rels, drop)
        after = Counter(r["_block"] for r in rows)
        for b in before:
            d = before[b] - after.get(b, 0)
            if d:
                log["rows_dropped"][b] += d
                if b in targets:            # own rows: the family's realised selected rows follow (A34 f i)
                    targets[b] -= d
        log["cells_fixed"] += 1
    return rows, rels


def a34f_settle(rows, rels, pools, ctx, x, targets, fams):
    """PREREG A34 (f): (ii) G10 / E2 wording cells outside their bands are down-sampled on the majority label;
    (i) expected shares follow the realised clean rows: own = the included families' realised selected rows,
    public / commit = their realised rows when included (else 0), replay = floor(1.5 x new) (replay is down-sampled
    to it when above, keeping E2; a replay already below it enters with its realised rows, the remainder lowering the
    total), total = new + replay. Every band and gate is unchanged."""
    inc = set(x.get("include") or [])
    log = {t: {"cells_fixed": 0, "rows_dropped": Counter(), "unfixed": []} for t in ("g10", "e2")}
    log["replay_cut"] = 0
    use_pub = any(b in inc for b in PUBLIC_BUILDERS)
    for _ in range(6):
        rows, rels = _a34f_balance(rows, rels, "g10", _a34f_g10_cells, _a34f_g10_ok, targets, log["g10"])
        rows, rels = _a34f_balance(rows, rels, "e2", lambda rr: _a34f_e2_cells(rr, ctx), _a34f_e2_ok, targets,
                                   log["e2"])
        by = Counter(r["_block"] for r in rows)
        new = (sum(by[f] for f in fams) + (by["public"] if use_pub else 0) + (by["COMMIT"] if "COMMIT" in inc else 0))
        cut = by["replay"] - math.floor(1.5 * new)
        if cut <= 0:
            break
        rows, rels = shrink_replay(rows, rels, pools, ctx, cut, x)
        log["replay_cut"] += cut
    by = Counter(r["_block"] for r in rows)
    own = sum(targets[f] for f in fams)
    pub = by["public"] if use_pub else 0
    com = by["COMMIT"] if "COMMIT" in inc else 0
    new_real = sum(by[f] for f in fams) + pub + com
    cap = math.floor(1.5 * new_real)
    rp = min(by["replay"], cap)
    x["expected"].update({"own": own, "own_by_family": {f: targets[f] for f in fams}, "public": pub, "commit": com,
                          "new": own + pub + com, "replay": rp, "total": own + pub + com + rp})
    x["a34_f"] = log | {"replay_cap_floor_1p5_new": cap, "replay_realised": by["replay"],
                        "replay_short_of_cap": cap - rp, "rule": "PREREG A34 (f) (i)/(ii)"}
    print(f"A34 (f): G10 cells fixed {log['g10']['cells_fixed']} (rows {sum(log['g10']['rows_dropped'].values()):,}), "
          f"E2 cells fixed {log['e2']['cells_fixed']} (rows {sum(log['e2']['rows_dropped'].values()):,}), unfixed "
          f"{len(log['g10']['unfixed']) + len(log['e2']['unfixed'])}; replay {by['replay']:,} (cap floor(1.5 x "
          f"{new_real:,}) = {cap:,}, cut {log['replay_cut']:,}); expected own {own:,} public {pub:,} commit {com:,} "
          f"total {own + pub + com + rp:,}", flush=True)
    return rows, rels


def finish(a, ilog, rep, probs, rows, rels, parents, pools, ctx, exp_pub, targets, fams, fb, t0) -> dict:
    """Drops (G13 decontam and deny-list: whole units; G18 and token limits: rows), then refills from each block's
    pool until no row is short (or the pools run out), then the gates on the final rows."""
    rs = rs_mod()
    blocks0 = sorted({r["_block"] for r in rows})
    ho = HeldOut(dev_items(ilog, cs.FAMS + ["COMMIT"]), rs)       # every dev part on disk, mixed family or not
    # G13 decontam hook + deny-list over every row that can enter the mix (the pools included)
    dids, rep["g13_decontam_inputs"] = decontam_drop_ids(ilog, a.decontam_drops)
    pool_rows = [r for p in pools.values() if p.block != "replay" for c in p.cands.values() for u in c
                 for r in p.raw_of(u)]
    new = [r for r in rows if r["_block"] != "replay"]
    denied = run_denylist(ilog, denylist_query(new + pool_rows, parents), rep, a.final)

    def bad_row(r) -> bool:
        if r["id"] in dids:
            return True
        if r["_block"] == "replay":
            return False
        ts = (r.get("meta") or {}).get("text_source") or {}
        return r["source"] in denied or "text:" + str(ts.get("dataset")) in denied
    ever = {r["id"]: (r["_block"], r) for r in rows}
    rows, rels, n = drop_units(rows, rels, dids)
    rep["g13_rows_dropped"] = n
    rows, rels, n = drop_units(rows, rels, {r["id"] for r in rows if bad_row(r)})
    rep["denylist_rows_dropped"] = n
    if n:
        probs.append(f"deny-list: {n} new rows from denied sources {rep['denylist_new']['denied']} (refilled below)")
    rb = replay_denylist_check(ilog, [r for r in rows if r["_block"] == "replay"], rep)
    if rb:
        probs.append(f"replay sources without a keep verdict: {rb}")
    # G18 on the merged targets (rows)
    g18 = {}
    out, gone = [], set()
    for b in blocks0:
        kept, d = g18_lint([r for r in rows if r["_block"] == b], b, g18)
        out += kept
        gone |= d
    order = {r["id"]: i for i, r in enumerate(rows)}
    rows = sorted(out, key=lambda r: order[r["id"]])
    rows, rels = drop_rows(rows, rels, gone)
    # tokens and the token cap (rows)
    log(f"tokenizing {len(rows):,} rendered prompts ({time.time() - t0:.0f}s)")
    ntok = dict(zip((r["id"] for r in rows), token_counts(ilog, rows)))
    capdrop, cap_probs = token_cap(rows, ntok, rep, spec6=False)
    rows, rels = drop_rows(rows, rels, capdrop)
    rep["drops_before_refill"] = {"g13": rep["g13_rows_dropped"], "denylist": rep["denylist_rows_dropped"],
                                  "g18": len(gone), "token_cap_or_over_7900": len(capdrop)}
    # refills (spec 5 replay; 2.1 / 4.2 own and commit; 3 public)
    g18r = {}

    def accept(pool, u, tally):
        rr = pool.rows_of(u, tally)
        if any(r["id"] in ever or bad_row(r) or ho.clash(r) for r in rr):
            return None
        rr, d = g18_lint(rr, pool.block, g18r)
        if d:
            return None
        tk = token_counts(ilog, rr)
        if any(t > MAX_TOK for t in tk):
            return None
        ntok.update(zip((r["id"] for r in rr), tk))
        return rr
    handled, rep["refill"] = set(), {}
    for rnd in range(REFILL_ROUNDS):
        add, arels = refill(pools, rows, ever, handled, accept, rep["refill"])
        if not add:
            break
        rows += add
        rels += arels
        ever.update({r["id"]: (r["_block"], r) for r in add})
        capdrop, cap_probs = token_cap(rows, ntok, rep, spec6=False)
        rows, rels = drop_rows(rows, rels, capdrop)
    rep["refill_rounds"] = rnd + 1 if rep["refill"] else 0
    # PREREG A28 (b): the spec 6 token cap (a mix under the cap is unchanged)
    rows, rels, a28_probs = cap_trim(rows, rels, ntok, pools, ctx, targets, ever, handled, accept, rep)
    if rep["a28_cap"]["applied"]:
        capdrop, cap_probs = token_cap(rows, ntok, rep, spec6=False)          # the cap measured again on the trimmed mix
        rows, rels = drop_rows(rows, rels, capdrop)
        tc, ac = rep["token_cap"], rep["a28_cap"]                # before = the pre-trim mix; the trim's own counts
        tc["before"] = [ac["before"]["long_row_share"], ac["before"]["long_token_share"]]
        tc["dropped_for_cap"] = sum(t["dropped_rows"] for t in ac["trims_by_block"].values())
        tc["a28_trim"] = {"units_trimmed": sum(t["swapped_units"] + t["dropped_units"]
                                               for t in ac["trims_by_block"].values()),
                          "rows_refilled": sum(ac["refilled_rows_by_family"].values()),
                          "rows_swapped_in": sum(ac["swapped_in_rows_by_block"].values()),
                          "remainder_rows": ac["remainder_rows"], "replay_cut": ac["replay_cut"],
                          "detail": "rep a28_cap"}
    probs += cap_probs + a28_probs
    if rep.get("a34"):
        x = rep["a34"]
        if rep["a28_cap"]["applied"]:
            probs.append("A34 (c): the token cap needed the A28 (b) trim, whose A26 (b) refill is not applied in this "
                         "round (no tested balance-keeping refill)")
        cut = sum(1 for r in rows if r["_block"] == "replay") - x["expected"]["replay"]
        if cut > 0:                         # A34 (c): replay trimmed to floor(1.5 x new rows), whole units, seeded
            rows, rels = shrink_replay(rows, rels, pools, ctx, cut, x)
        rows, rels = a34f_settle(rows, rels, pools, ctx, x, targets, fams)   # PREREG A34 (f)
    probs += e2_final(ctx, rows, rep)
    rep["g18"] = {"by_block_source": g18, "rows_checked": sum(c[0] for v in g18.values() for c in v.values()),
                  "fell_back": sum(c[1] for v in g18.values() for c in v.values()), "dropped": len(gone),
                  "refill_candidates_checked": g18r,
                  "pass_after_fix": all(g18_ok(r) for r in rows if isinstance(r["meta"].get("option_level"), dict))}
    if not rep["g18"]["pass_after_fix"]:
        probs.append("G18 ordinal target lint is not 100% on the final targets")
    global G10_SIDE
    G10_SIDE = (ctx or {}).get("sidecar") or {}           # g10_checks' attack rule (ATTACK_RULE) on own rows
    return gates(a, ilog, rep, probs, rows, rels, ntok, ho, exp_pub, targets, fams, fb, t0)


def share_checks(by: Counter, own: int, exp_own: int, exp_pub: int, targets: dict, fams: list, a28: dict,
                 a34: dict | None = None):
    """Realised vs expected rows per share. Expected = spec, plus (only after a PREREG A28 b trim) its replay / own /
    total / per-family deltas (A26 b refill and remainder). Public and commit rows always stay as specced (A26 b;
    spec 3.2 / 4.2), so their expectation never takes an A28 delta. Returns (shares, problem lines)."""
    fd = a28.get("family_delta", {})
    spec = {"replay": SHARES_R1["replay"], "own": exp_own, "public": exp_pub, "commit": SHARES_R1["commit"],
            "total": TOTAL_R1}
    if a34:                                 # PREREG A34 (c): the left-out sources' shares lower the total
        spec = {k: a34[k] for k in spec}
    lab = "A34 (c) expected" if a34 else "spec"
    exp = {"replay": spec["replay"] + a28.get("replay_delta", 0), "own": exp_own + a28.get("own_delta", 0),
           "public": exp_pub, "commit": spec["commit"], "total": spec["total"] + a28.get("total_delta", 0)}
    got = {"replay": by["replay"], "own": own, "public": by["public"], "commit": by["COMMIT"],
           "total": sum(by.values())}
    shares = {k: [got[k], exp[k]] for k in spec}
    shares |= {"own_by_family": {f: [by.get(f, 0), targets[f] + fd.get(f, 0)] for f in cs.FAMS},
               "families_present": fams, "families_missing": [f for f in cs.FAMS if f not in fams]}
    if a28:
        shares["spec_before_a28"] = spec | {"own_by_family": {f: targets[f] for f in cs.FAMS}}
    probs = []
    for k in ("replay", "own", "public", "commit", "total"):
        if got[k] != exp[k]:
            if exp[k] == spec[k]:
                probs.append(f"share {k}: {got[k]:,} rows vs {lab} {exp[k]:,}")
            else:
                probs.append(f"share {k}: {got[k]:,} rows vs {exp[k]:,} expected after the A28 (b) trim / A26 (b) "
                             f"refill (spec {spec[k]:,}, delta {exp[k] - spec[k]:+,})")
    short = {f: v for f, v in shares["own_by_family"].items() if f in fams and v[0] != v[1]}
    if short:
        probs.append(f"own family rows differ from targets{' (+ A28 b deltas)' if fd else ''}: {short}")
    return shares, probs


def gates(a, ilog, rep, probs, rows, rels, ntok, ho, exp_pub, targets, fams, fb, t0) -> dict:
    nolic = Counter(r["_block"] for r in rows if not licence_ok(r))
    rep["licence_missing_by_block"] = dict(nolic)
    if nolic:
        probs.append(f"licence join: rows without meta.licence {dict(nolic)}")
    blocks = defaultdict(list)
    for r in rows:
        blocks[r["_block"]].append(r)
    refused = refuse_held_out(ilog, blocks, rep)
    if refused:
        probs.append(f"fmt1 refuse_held_out (strict on own / commit rows; format_style required) refused blocks "
                     f"{refused}")
    probs += ho.check(rows, rep)
    probs += commit_repo_check(ilog, rows, rep)
    rels = split_replay_call_ids(rows, rels, ntok, rep)
    probs += unit_check(rows, rels, ntok, rep)
    probs += check_rows(rows, rep)
    probs += g10_checks(rows, rep, a.final)
    probs += commit_counts(rows, rep)
    # shares
    by = Counter(r["_block"] for r in rows)
    own = sum(v for b, v in by.items() if b.startswith("F"))
    exp_own = SHARES_R1["own"] + sum(fb.values())
    a34 = (rep.get("a34") or {}).get("expected")
    if a34:
        exp_own = a34["own"]
    a28 = (rep.get("a28_cap") or {}).get("expected") or {}     # PREREG A28 (b) trim + A26 (b) refill: realised plan
    shares, msgs = share_checks(by, own, exp_own, exp_pub, targets, fams, a28, a34)
    rep["shares"] = shares
    if a34:
        x, tot = rep["a34"], max(1, sum(by.values()))
        x["realised"] = {k: shares[k][0] for k in ("replay", "own", "public", "commit", "total")} | {
            "own_by_family": {f: by.get(f, 0) for f in fams},
            "share_of_total": {k: round(shares[k][0] / tot, 4) for k in ("replay", "own", "public", "commit")}}
        sc = {}
        for f in fams:                      # A33: counts-only short-or-no-card share per family (vs its own QC band)
            rr = [r for r in rows if r["_block"] == f]
            k = sum(short_card(r, G10_SIDE.get(r["id"])) for r in rr)
            sc[f] = {"rows": len(rr), "short_or_no_card": k, "share": round(k / max(1, len(rr)), 4)}
        x["short_card_share"] = sc
    import hashlib
    ids = sorted(str(r["id"]) for r in rows)
    n = max(1, len(ids))
    rep["selection_digest"] = {"rows": len(ids), "ids_sha256": hashlib.sha256("\n".join(ids).encode()).hexdigest(),
                               "relations": len(rels), "rows_by_block": dict(sorted(by.items())),
                               "realised_share": {b: round(v / n, 4) for b, v in sorted(by.items())}}
    probs += msgs
    if a.final and any(not v.get("qc_pass") for v in rep.get("own", {}).values()):
        probs.append("a family QC_REPORT.json is not pass=true")
    rep["config_fill"] = config_fill(rows, rels)
    rep["problems"] = probs
    rep["inputs"] = ilog.entries
    rep["seconds"] = round(time.time() - t0, 1)
    return write_outputs(a, rep, rows, rels) if a.final else dry_report(rep)


# ------------------------------------------------------------------ outputs

def sealed_check(path: Path) -> dict:
    """RUN (never open) sealed_nd/qc/sealed_check.py on the staged file, in its own process; read its summary."""
    chk = LEAN / "sealed_nd/qc/sealed_check.py"
    out, summ = WORK / f"{path.stem}.sealedqc.jsonl", WORK / f"{path.stem}.sealedqc.summary.json"
    # --structure-fields: without it the part-P structure check (spec 7.2 method 6) has no fields to hash
    p = subprocess.run([str(PY), str(chk), str(path), "--id-field", "id", "--structure-fields",
                        "state,card,instructions,options", "--out", str(out), "--summary", str(summ)],
                       capture_output=True, text=True, cwd=str(LEAN), timeout=7200)
    s = json.loads(summ.read_text()) if summ.exists() else {}
    return {"exit": p.returncode, "rows": s.get("rows"), "rows_hit": s.get("rows_hit"),
            "suite_sha256": s.get("suite_sha256"), "checker": "sealed_nd/qc/sealed_check.py (run only)"}


def write_outputs(a, rep, rows, rels) -> dict:
    clean = [{k: v for k, v in r.items() if k != "_block"} for r in rows]
    rel_out = [{"a": x["a"], "b": x["b"], "type": x["type"]} for x in rels]
    WORK.mkdir(parents=True, exist_ok=True)
    stage = WORK / "stage_c_train_r1.jsonl"
    write_jsonl(stage, clean)
    sc = sealed_check(stage)
    rep["sealed_check"] = sc
    if sc["exit"] != 0 or sc["rows_hit"] != 0 or sc["suite_sha256"] not in (None, A15_SUITE_SHA):
        rep["problems"].append(f"sealed_check on the staged mix: {sc}")
    if rep["problems"]:
        write_json(WORK / "final_refused_r1.json", rep)
        stage.unlink(missing_ok=True)
        raise SystemExit("--final refused (no training file written):\n  " + "\n  ".join(rep["problems"]))
    tr, rl = OUT_PARTS / "c_train_r1.jsonl", OUT_PARTS / "c_rel_r1.jsonl"
    sha_t = write_jsonl(tr, clean)
    sha_r = write_jsonl(rl, rel_out)
    stage.unlink(missing_ok=True)
    fill = rep["config_fill"]
    write_json(WORK / "config_fill_r1.json", {"config": str(CONFIG.relative_to(LEAN)), **fill,
                                              "train_file_sha256": sha_t, "rel_file_sha256": sha_r})
    man = {"what": "C round-1 training mix (C_DATA_SPEC.md v4 step 9)", "written_utc": time.strftime(
        "%Y-%m-%dT%H:%M:%SZ", time.gmtime()), "sealed_suite_sha256_A15": A15_SUITE_SHA,
        "files": {"c_train_r1.jsonl": {"sha256": sha_t, "rows": len(clean)},
                  "c_rel_r1.jsonl": {"sha256": sha_r, "rows": len(rel_out)}},
        "counts": {"by_block": dict(Counter(r["_block"] for r in rows)), "by_source": dict(Counter(
            r["source"] for r in rows)), "relations": dict(Counter(x["type"] for x in rel_out))},
        "config_fill": fill, "mixer_sha256": sha256_file(Path(__file__)),
        "crowd_select_sha256": sha256_file(HERE / "crowd_select.py"), "report": "c_build/mix_r1/mix_report_r1.json"}
    write_json(OUT_PARTS / "c_mix_r1_manifest.json", man)
    write_json(WORK / "mix_report_r1.json", rep)
    log(f"FINAL written: {len(clean):,} rows sha {sha_t[:12]}, {len(rel_out):,} relations; fill {fill}")
    return rep


def dry_report(rep) -> dict:
    write_json(WORK / "dryrun_r1.json", rep)
    sh = rep["shares"]
    log("DRY RUN (counts only; no training file written): " + json.dumps(
        {k: sh[k] for k in ("replay", "own", "public", "commit", "total")}) + f"; problems {len(rep['problems'])}")
    return rep


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    g = ap.add_mutually_exclusive_group(required=True)
    g.add_argument("--dry-run", dest="dry_run", action="store_true")
    g.add_argument("--final", action="store_true")
    ap.add_argument("--sealed-sha", dest="sealed_sha", default=None)
    ap.add_argument("--decontam-drops", dest="decontam_drops", nargs="*", default=[])
    ap.add_argument("--include", nargs="+", default=None,
                    help="sources that enter the mix (F1..F13, COMMIT, public-1/2/3); others are left out as missing")
    a = ap.parse_args(argv)
    if a.final and not a.decontam_drops:
        raise SystemExit("--final needs the G13 counts-only decontamination drop lists (--decontam-drops)")
    rep = build(a)
    print(json.dumps({"shares": {k: rep["shares"][k] for k in ("replay", "own", "public", "commit", "total")},
                      "own_by_family": rep["shares"]["own_by_family"], "config_fill": rep["config_fill"],
                      "include": rep.get("include"), "selection_digest": rep.get("selection_digest"),
                      "problems": rep["problems"]}, indent=1))


if __name__ == "__main__":
    main()
