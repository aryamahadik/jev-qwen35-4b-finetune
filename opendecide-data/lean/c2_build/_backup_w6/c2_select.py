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

  ../.venv/bin/python c2_build/c2_select.py tasks [--fam T28 ...] [--write-shards]   the C1-only read plan (+ shards)
  ../.venv/bin/python c2_build/c2_select.py select [--fam T28 ...] [--exclude-ids logs/decontam_counts/x.json ...]
  ../.venv/bin/python c2_build/c2_select.py carry [--fam F5 F6 F11 F4] [--exclude-ids ...]
Outputs (c2_build/crowd_c2/): select_<FAM>.json, g5_reread_<FAM>.json, crowd_tasks_c2.json; shards under
data/c2_crowd_shards/<FAM>/. Every write needs the OHS-4 freeze (PREREG A38) first (A37 f); before it the tools refuse.
"""
from __future__ import annotations

import argparse
import sys
from collections import Counter
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import c2io  # noqa: E402
from c2io import C1, CARRY, SEED, C2InputLog
from c2io import ALL_TARGETS as TARGETS  # A47 registry: + T40-T45, GB, MD, RTW  # noqa: E402

import crowd_select as cs  # noqa: E402  (c_build: imported, never edited)
from mixio import log_line, sha256_file  # noqa: E402

OUT = c2io.HERE / "crowd_c2"
SHARDS = c2io.DATA / "c2_crowd_shards"
R1_SHARDS = c2io.DATA / "c_crowd_r1_shards"          # carry-over pools: the round-1 crowd shards and C1 labels
R1_SELECT = c2io.CB / "crowd_r1"                     # carry-over pools: round-1 select_<F>.json (selected ids)
LOG = c2io.HERE / "progress_c2.log"
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
    return c1_pg(rows, probs), view


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


def select_family(fam: str, rows, rels, pg: dict, target: int, seed: int = SEED, drop_ids: set | None = None,
                  key: str | None = None) -> dict:
    """One family's C2 selection: candidate checks, G13 exclusion, crowd_select.select (bins, budgets, balanced quotas,
    reflow, chi-square) and the G5 re-read list. Returns the select record (no file written)."""
    probs = c2io.candidate_problems(fam, rows)
    if probs:
        raise SystemExit("candidates refused: " + "; ".join(probs))
    rows, excl = drop_excluded(rows, rels, set(drop_ids or ()))
    ids = {r["id"] for r in rows}
    rels = [x for x in rels if x.get("a") in ids and x.get("b") in ids]
    units = cs.units_of(rows, rels)
    k = key or sel_key(fam)
    res = cs.select(rows, units, pg, target, key=k, seed=seed)
    g5 = cs.g5_reread(rows, units, res["sel"], pg, fam)
    chosen = [rows[i]["id"] for u in res["sel"] for i in units[u]]
    rep = res["report"]
    rep["crowd_rule"] = CROWD_RULE
    rep["unit_sizes"] = dict(sorted(Counter(len(units[u]) for u in res["sel"]).items()))
    return {"family": fam, "target": target, "seed": seed, "key": k, "crowd": {"c1": C1}, "crowd_rule": CROWD_RULE,
            "report": rep, "budget": res["budget"], "easy_dropped_units": res["easy_dropped_units"],
            "reflow": res.get("reflow", []), "selected_ids": chosen, "parts": [{"key": k, "ids": chosen}],
            "exclude_ids": excl, "crowd_pg": {r["id"]: round(pg[r["id"]], 4) for r in rows},
            "difficulty_bin": {r["id"]: res["bins"][r["id"]] for r in rows}, "g5": g5}


def reselect(rows, rels, pg: dict, parts: list[dict], target: int, seed: int = SEED) -> dict:
    """A smaller selection of already-selected rows (the mixer's budget trim and agent-tier cap, spec 5.2 / 5.5):
    crowd_select.select again on each part's rows with the SAME seed and key, so no unit that passed the seeded 30%
    easy keep is thinned twice, at a target split over the parts by largest remainder. Bins, budgets, balanced quotas
    and whole units hold exactly as in the first selection. Returns {"selected_ids", "parts", "reports"}."""
    from mixer import largest_remainder
    have = {r["id"] for r in rows}
    sizes = {i: sum(1 for x in p["ids"] if x in have) for i, p in enumerate(parts)}
    want = largest_remainder(sizes, min(target, sum(sizes.values())))
    out, new_parts, reps = [], [], []
    for i, p in enumerate(parts):
        ids = set(p["ids"]) & have
        sub = [r for r in rows if r["id"] in ids]
        srel = [x for x in rels if x.get("a") in ids and x.get("b") in ids]
        units = cs.units_of(sub, srel)
        res = cs.select(sub, units, {r["id"]: pg[r["id"]] for r in sub}, want[i], key=p["key"], seed=seed)
        got = [sub[j]["id"] for u in res["sel"] for j in units[u]]
        out += got
        new_parts.append({"key": p["key"], "ids": got})
        reps.append(res["report"])
    return {"selected_ids": out, "parts": new_parts, "reports": reps}


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


def drop_ids_of(ilog, files) -> set:
    out = set()
    for p in files or []:
        d = ilog.json(p)
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
    ilog = C2InputLog()
    drop = drop_ids_of(ilog, a.exclude_ids)
    for fam in available(a.fam):
        if fam in CARRY:
            raise SystemExit(f"{fam}: carry-over pools use the 'carry' command")
        rows, rels, shas = family_inputs(ilog, fam)
        sd = SHARDS / fam
        pg, view = load_c1(ilog, rows, sd / f"labels_{C1}", sd)
        rec = select_family(fam, rows, rels, pg, TARGETS[fam], SEED, drop)
        write_select(fam, rec, {**shas, "c1_view": view, "exclude_files": [str(p) for p in a.exclude_ids or []]})
    c2io.write_json(OUT / "select_inputs.json", {"inputs": ilog.entries})


def cmd_carry(a):
    c2io.require_a38()
    ilog = C2InputLog()
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
    ilog = C2InputLog()
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
            if c2io.refusal(sd):
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
    a = ap.parse_args(argv)
    {"tasks": cmd_tasks, "select": cmd_select, "carry": cmd_carry}[a.cmd](a)


if __name__ == "__main__":
    main()
