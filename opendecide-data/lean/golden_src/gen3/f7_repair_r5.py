"""F7 v2 r5: the r4 TRAIN selection repaired after the source-label audit (yn2b/F7_BLIND_READ_3.md section 5).

Why. Blind read 3 found 4 wrong golds, all of them human labels of the source texts, and the audit of every real-text
source row behind the train part then flagged 95 rows (yn2b/f7_source_label_audit.json). extra/build_fix2.py drops
every pair built from a flagged row, but dropping 103 pairs left the F7 part of fix2 below six checklist bars (item
floors 24 / 28 / 30 / 32, the card share, two lexeme parity / distractor shares and one instruction word's parity).
r5 refills those pairs from the SAME candidate pool, with the least change to r4:

  1. dump: run gen3_nested_negation.build() exactly as r4 does (same seed, PYTHONHASHSEED=0, same pools), stop it
     right before the selection and save every candidate pair of every part (plain data) to a pickle. The candidates
     are byte-identical to r4's: step 2 rebuilds r4's train and probe files from them and compares every byte.
  2. repair:
     - the probe (iid + holdout) keeps r4's selection: its files are rewritten byte for byte;
     - train: start from r4's selection; drop every pair that extra/build_fix2.py would drop (a derived source row in
       yn2b/f7_fix2_drops.json, a listed pair, or any hard fix2 row rule such as the probe 12-gram rule); forbid the
       same for every spare candidate; then fill the vacancies one pair at a time, each time adding the spare pair
       that leaves the generator's own Objective lowest (hard first, then penalty; a source row the label audit has
       not read yet costs --unread-cost of hard penalty, so already-audited texts are preferred); then, only if a hard
       limit is still crossed, swap pairs while the hard penalty strictly falls;
     - the generator's audit (yn2b/f7_precheck.py as a library, with the full surface probes and the devx rows) must
       report no failing check. A failing cross-validated surface probe (check 5, which the Objective does not
       model) is repaired by single swaps of new pairs in the probe's worst stratum, each kept only when the failing
       probes pass and nothing else in check 5 starts to fail;
     - every new pair's real-text source rows that the audit has not read are listed (--new-out) for the
       source-label audit; a flagged row goes into yn2b/f7_fix2_drops.json and the repair is run again.
  3. --write: back up r4's files once (data/v14_parts/f7_v2_r4_backup/), then write r5 with the generator's own
     write_all (same files, same formats; f7_counts.json records "revision": "r5" and the repair).

Labels are program-made (the candidates are r4's). No model is called. CPU only. OHS-3 is never opened.

  cd opendecide-data/lean
  PYTHONDONTWRITEBYTECODE=1 ../.venv/bin/python golden_src/gen3/f7_repair_r5.py dump --pool <scratch>/f7_pool_r4.pkl
  PYTHONDONTWRITEBYTECODE=1 ../.venv/bin/python golden_src/gen3/f7_repair_r5.py repair --pool <scratch>/f7_pool_r4.pkl \
      --new-out <scratch>/f7_r5_new_sources.json [--write --overwrite]
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import pickle
import shutil
import sys
import time
from collections import Counter
from pathlib import Path
from types import SimpleNamespace

HERE = Path(__file__).resolve().parent
LEAN = HERE.parents[1]
for _p in (HERE, LEAN, LEAN / "yn2b", LEAN / "extra"):
    if str(_p) not in sys.path:
        sys.path.insert(0, str(_p))

REVISION = "r5"
DROPS = LEAN / "yn2b/f7_fix2_drops.json"
AUDIT = LEAN / "yn2b/f7_source_label_audit.json"
BACKUP = LEAN / "data/v14_parts/f7_v2_r4_backup"
R4_FILES = ("f7_train.jsonl", "f7_relations.jsonl", "f7_meta.jsonl", "f7_probe.jsonl", "f7_probe_relations.jsonl",
            "f7_probe_meta.jsonl", "f7_defs.json", "f7_counts.json", "f7_lexicon.json", "f7_holdout_spec.json")
R4_TRAIN_SHA = "6e560988104c1e12aa4b8b52f1ebab7d68691f407908b1c951b34da6971c536e"   # build_fix2 INPUT_SHA (r4)
R4_PROBE_SHA = "f16c05a1749ce27ffd072dcbbab8697ca509d8e08fd544b85d6efa396fc17d0f"
PART_ABBR = {"train": "tr", "iid": "ii", "holdout": "ho"}


class _Stop(Exception):
    pass


def sha(p: Path) -> str:
    return hashlib.sha256(p.read_bytes()).hexdigest()


def log_fn():
    t0 = time.time()
    return lambda s: print(f"[{time.time() - t0:6.0f}s] {s}", flush=True)


def need_hashseed():
    if os.environ.get("PYTHONHASHSEED") != "0":
        os.environ["PYTHONHASHSEED"] = "0"
        os.execv(sys.executable, [sys.executable] + sys.argv)


# ------------------------------------------------------------------------------------------------ stage 1: dump
def stage_dump(a, log):
    import gen3_nested_negation as g
    if g.REVISION != "r4":
        raise SystemExit(f"the generator is {g.REVISION}, not r4: r5 repairs the r4 selection")
    got = {}

    def capture(parts, n_pairs, seed, log_, prev=None, round_=0):
        got["parts"] = parts
        raise _Stop()

    g.select_all = capture
    try:
        g.build(seed=g.SEED, log=log, audit=False)
    except _Stop:
        pass
    out = {"generator": g.GENERATOR, "version": g.VERSION, "revision_of_pool": g.REVISION, "seed": g.SEED,
           "hashseed": os.environ.get("PYTHONHASHSEED"), "parts": {}}
    for part, P in got["parts"].items():
        cands = []
        for lad in P["cands"]:
            rows = {tw: [(row, m, {"qtype": rd.qtype}) for row, m, rd in lad["rows"][tw]] for tw in ("A", "B")}
            s = lad["subj"]
            cands.append({"rows": rows, "rels": lad["rels"], "dev_kind": lad["dev_kind"],
                          "subj": {"kind": s.kind, "ptype": s.ptype, "source": s.source}})
        out["parts"][part] = {"cands": cands, "s": P["s"], "wc": dict(P["wc"])}
        log(f"dump {part}: {len(cands)} candidate pairs")
    Path(a.pool).parent.mkdir(parents=True, exist_ok=True)
    with open(a.pool, "wb") as f:
        pickle.dump(out, f, protocol=4)
    log(f"wrote {a.pool} ({os.path.getsize(a.pool):,} bytes)")


# ------------------------------------------------------------------------------------------------ helpers
def as_lad(c):
    """A candidate in the shape the generator's functions read (lad['rows'][tw] = (row, m, rd); lad['subj'])."""
    return {"rows": {tw: [(row, m, SimpleNamespace(**rd)) for row, m, rd in c["rows"][tw]] for tw in ("A", "B")},
            "rels": c["rels"], "dev_kind": c["dev_kind"], "subj": SimpleNamespace(**c["subj"])}


def pair_id(lad):
    return lad["rows"]["A"][0][0]["meta"]["latent_id"][:-1]


def derived_rows(row):
    d = (row.get("meta") or {}).get("derived_from")
    if not d:
        return set()
    return set(d) if isinstance(d, list) else set(str(d).split("|"))


def lad_sources(lad):
    out = set()
    for tw in ("A", "B"):
        for row, _, _ in lad["rows"][tw]:
            out |= derived_rows(row)
    return out


def file_lines(p):
    return [x for x in p.read_text(encoding="utf-8").splitlines() if x.strip()]


def selection_lines(g, lads):
    pl = SimpleNamespace(ladders=lads)
    rows, metas, rels = g.rows_of(pl)
    dump = lambda xs: [json.dumps(x, ensure_ascii=False) for x in xs]  # noqa: E731
    return dump(rows), dump(rels), dump(g.strip_private(metas))


# ------------------------------------------------------------------------------------------------ stage 2: repair
def stage_repair(a, log):
    import gen3_nested_negation as g
    import nn_lexicon as lx
    with open(a.pool, "rb") as f:
        pool = pickle.load(f)
    if pool["revision_of_pool"] != "r4" or pool["seed"] != g.SEED or pool["hashseed"] != "0":
        raise SystemExit(f"pool {a.pool} is not the r4 pool: {pool['revision_of_pool']} {pool['seed']} {pool['hashseed']}")
    src_dir = BACKUP if BACKUP.exists() else LEAN / "data/v14_parts"
    if sha(src_dir / "f7_train.jsonl") != R4_TRAIN_SHA or sha(src_dir / "f7_probe.jsonl") != R4_PROBE_SHA:
        raise SystemExit(f"{src_dir} does not hold r4's files (sha256 of f7_train / f7_probe)")
    cands = {p: [as_lad(c) for c in pool["parts"][p]["cands"]] for p in ("train", "iid", "holdout")}
    idx_of = {p: {pair_id(l): i for i, l in enumerate(cands[p])} for p in cands}
    # r4's selection, read off r4's files
    prev = {p: set() for p in cands}
    for fn in ("f7_train.jsonl", "f7_probe.jsonl"):
        for line in file_lines(src_dir / fn):
            lid = json.loads(line)["meta"]["latent_id"][:-1]
            part = {v: k for k, v in PART_ABBR.items()}[lid.split("-")[1]]
            if lid not in idx_of[part]:
                raise SystemExit(f"r4 pair {lid} is not in the regenerated pool: the pool differs from r4's")
            prev[part].add(idx_of[part][lid])
    prev = {p: sorted(v) for p, v in prev.items()}
    # byte check: r4's six data files rebuilt from the pool
    tr = selection_lines(g, [cands["train"][i] for i in prev["train"]])
    pr = [a_ + b_ for a_, b_ in zip(selection_lines(g, [cands["iid"][i] for i in prev["iid"]]),
                                     selection_lines(g, [cands["holdout"][i] for i in prev["holdout"]]))]
    for (name, lines) in (("f7_train.jsonl", tr[0]), ("f7_relations.jsonl", tr[1]), ("f7_meta.jsonl", tr[2]),
                          ("f7_probe.jsonl", pr[0]), ("f7_probe_relations.jsonl", pr[1]),
                          ("f7_probe_meta.jsonl", pr[2])):
        if lines != file_lines(src_dir / name):
            raise SystemExit(f"the pool does not rebuild r4's {name} byte for byte: stop")
    log(f"pool reproduces r4 byte for byte (train {len(prev['train'])} pairs, iid {len(prev['iid'])}, holdout "
        f"{len(prev['holdout'])}); candidates train {len(cands['train'])}")

    # ---- what fix2 would drop (extra/build_fix2.py's own F7 rules, imported, not copied)
    import build_fix2 as bf2
    drops = json.loads(DROPS.read_text())
    drop_pairs, drop_src = set(drops["f7_pairs"]), set(drops["source_row_ids"])
    bad_ids = set(json.loads((LEAN / "yn2b/label_audit_known_bad_ids.json").read_text())["all_ids"]) | drop_src
    R = bf2.load_all_refs(log)
    P = bf2.probe_refs(log)
    forbid = {}
    for i, lad in enumerate(cands["train"]):
        why = set()
        if pair_id(lad) in drop_pairs:
            why.add("drop_list_pair")
        if lad_sources(lad) & bad_ids:
            why.add("derived_from_bad_source_row")
        for tw in ("A", "B"):
            for row, _, _ in lad["rows"][tw]:
                w = bf2.hard(bf2.row_reasons(row, R, P, "f7"))
                if w:
                    why |= set([w] if isinstance(w, str) else w)
        if why:
            forbid[i] = sorted(why)
    lost = [i for i in prev["train"] if i in forbid]
    log(f"forbidden train candidates {len(forbid)} ({Counter(r for v in forbid.values() for r in v)}); "
        f"r4 pairs lost {len(lost)}")

    # ---- the train objective as select_all builds it, except that the word rule's base also holds the kept probe
    #      pairs' instruction words (select_all selects train first, so its base is the devx alone; here the probe is
    #      already fixed, and precheck 8.9 reads train + probe + devx together)
    n = g.N_PAIRS["train"]
    base = g.devx_word_base()
    for p in ("iid", "holdout"):
        for i in prev[p]:
            f_ = g.pair_features(cands[p][i], None)
            base.update({k: v for k, v in f_.items() if isinstance(k, tuple) and k[0] in ("w_r", "w_o")})
    words = {w for w, c in pool["parts"]["train"]["wc"].items() if c >= 20}
    feats = [g.pair_features(c, words) for c in cands["train"]]
    frames = sorted({m["frame_id"] for lad in cands["train"] for tw in ("A", "B") for _, m, _ in lad["rows"][tw]})
    obj = g.Objective("train", sorted(lx.LEXICON), words, frames, base=Counter(base), lbase=None)
    sel = [i for i in prev["train"] if i not in forbid]
    spare = [i for i in range(len(cands["train"])) if i not in forbid and i not in set(prev["train"])]
    T = Counter()
    for i in sel:
        T.update(feats[i])
    log(f"after the drops: {len(sel)} pairs, hard {obj.hard(T):.4f}, penalty {obj.penalty(T):.3f}")
    # the real-text source rows the source-label audit has already read
    audited = set(json.loads(AUDIT.read_text()).get("rows_read_ids", [])) if AUDIT.exists() else set()
    if not audited:
        for line in file_lines(src_dir / "f7_train.jsonl"):
            audited |= derived_rows(json.loads(line))
    unread = [len(lad_sources(c) - audited) for c in cands["train"]]
    # fill: lowest hard penalty first; a source row the audit has not read costs UNREAD_COST of hard penalty, so the
    # fill prefers pairs whose texts were already audited (or that have none) when that costs little
    added = []
    while len(sel) < n:
        best = None
        for j in spare:
            T.update(feats[j])
            key = (round(obj.hard(T), 9) + a.unread_cost * unread[j], obj.penalty(T), j)
            T.subtract(feats[j])
            if best is None or key < best:
                best = key
        j = best[2]
        T.update(feats[j])
        sel.append(j)
        spare.remove(j)
        added.append(j)
    log(f"filled {len(added)} vacancies: hard {obj.hard(T):.4f}, penalty {obj.penalty(T):.3f}")
    # hard repair: swap one of the pairs added above (r4's own pairs stay) for a spare while the hard penalty
    # strictly falls; among the improving swaps, the lowest (hard + unread cost, penalty) wins
    swaps = []
    while obj.hard(T) > 1e-12:
        h0 = obj.hard(T)
        best = None
        for i in [x for x in sel if x in set(added)]:
            T.subtract(feats[i])
            for j in spare:
                T.update(feats[j])
                h = obj.hard(T)
                if h < h0 - 1e-12:
                    key = (round(h, 9) + a.unread_cost * unread[j], obj.penalty(T), i, j)
                    if best is None or key < best:
                        best = key
                T.subtract(feats[j])
            T.update(feats[i])
        if best is None:
            raise SystemExit(f"hard {h0:.4f} > 0 and no swap of an added pair lowers it: stop")
        _, _, i, j = best
        T.subtract(feats[i])
        T.update(feats[j])
        sel[sel.index(i)] = j
        spare.remove(j)
        spare.append(i)
        added[added.index(i)] = j
        swaps.append((i, j))
        log(f"  swap {pair_id(cands['train'][i])} -> {pair_id(cands['train'][j])}: hard {obj.hard(T):.4f}")
    sel = sorted(sel)
    new = sorted(set(sel) - set(prev["train"]))
    log(f"train: {len(sel)} pairs, {len(new)} not in r4, hard {obj.hard(T):.4f}, penalty {obj.penalty(T):.3f}")

    # ---- the generator's audit on the repaired selection (probe = r4's, devx included), as
    #      gen3_nested_negation.audit_selection runs it; quick = check 5 only, fast mode
    import f7_precheck as fp

    def run_audit(sel_train, quick):
        rows, metas, rels, hold_m = {}, [], {}, []
        for p, idx in (("train", sel_train), ("iid", prev["iid"]), ("holdout", prev["holdout"])):
            r_, m_, rl = g.rows_of(SimpleNamespace(ladders=[cands[p][i] for i in idx]))
            key = "train" if p == "train" else "probe"
            rows.setdefault(key, []).extend(r_)
            rels.setdefault(key, []).extend(rl)
            metas.extend(g.strip_private(m_))
            if p == "holdout":
                hold_m = g.strip_private(m_)
        rows["devx"], rels["devx"] = g._jsonl(g.DEVX_ROWS), g._jsonl(g.DEVX_REL)
        metas.extend(g._jsonl(g.DEVX_META))
        opts = fp.Opts(fast=True, lexicon=g.lexicon_json(), holdout_spec=g.holdout_spec_json(hold_m), unseen=False,
                       neg_manifest="(not read by the generator)", generator_code=[], decide2_code=[])
        ctx = fp.Ctx(rows, metas, rels, opts, log=lambda s_: None)
        if quick:
            res = fp.run_checks(ctx, only={"5"})
        else:
            res = fp.run_checks(ctx)
            ctx.opts.fast = False
            res.update(fp.run_checks(ctx, only={"5"}))
        return {sb.id: sb.value for r in res.values() for sb in r["subs"] if sb.status == "FAIL"}

    fails = run_audit(sel, quick=False)
    log(f"generator audit: failing checks {sorted(fails)} {json.dumps(fails, default=str)[:400]}")
    # A cross-validated surface probe (check 5) is not modelled by the Objective (the generator handles it with
    # refinement rounds that walk away from the selection). Here: swap ONE new pair at a time, chosen in the failing
    # probe's worst stratum, for a spare that keeps hard = 0 (spares whose source rows are audited or that have none
    # first), and keep the swap only when the failing probes pass and no other check-5 item starts to fail.
    rng = __import__("random").Random(g.SEED + 55)
    guided = []
    for rnd in range(1, 21):
        tid = [k for k in fails if k.startswith("5.")]
        if not fails or not tid or set(fails) - set(tid):
            break
        strat = next((v["worst_stratum_train"][0] for k, v in fails.items()
                      if k in tid and isinstance(v, dict) and v.get("worst_stratum_train")), None)

        def in_stratum(i):
            if not strat:
                return True
            key, val = strat.split("=", 1)
            return any(key in m and str(m[key]) == val for tw in ("A", "B") for _, m, _ in cands["train"][i]["rows"][tw])
        newp = [i for i in sel if i not in set(prev["train"])]
        targets = [i for i in newp if in_stratum(i)] or newp
        rng.shuffle(targets)
        clean = [j for j in spare if not (lad_sources(cands["train"][j]) - audited)]
        other = [j for j in spare if j not in set(clean)]
        rng.shuffle(clean)
        rng.shuffle(other)
        hit = None
        # first every target with spares whose texts are audited (or that have none), then the others
        for pool_j in (clean[:40], other[:10]):
            for t in targets[:10]:
                for j in pool_j:
                    T2 = Counter(T)
                    T2.subtract(feats[t])
                    T2.update(feats[j])
                    if obj.hard(T2) > 1e-12:
                        continue
                    trial = sorted([x for x in sel if x != t] + [j])
                    f2 = run_audit(trial, quick=True)
                    if not any(k in f2 for k in tid) and not (set(f2) - set(fails)):
                        hit = (t, j, T2, trial)
                        break
                if hit:
                    break
            if hit:
                break
        if not hit:
            log(f"  probe repair round {rnd}: no single swap fixes {tid} (stratum {strat})")
            break
        t, j, T, sel = hit
        spare.remove(j)
        spare.append(t)
        guided.append((t, j))
        log(f"  probe repair round {rnd}: {pair_id(cands['train'][t])} -> {pair_id(cands['train'][j])} "
            f"(stratum {strat}); hard {obj.hard(T):.4f}")
        fails = run_audit(sel, quick=False)
        log(f"  generator audit: failing checks {sorted(fails)}")
    swaps += guided
    new = sorted(set(sel) - set(prev["train"]))
    fails = sorted(fails)
    new_src = {}
    for i in new:
        lad = cands["train"][i]
        for s in sorted(lad_sources(lad) - audited):
            new_src.setdefault(s, []).append(pair_id(lad))
    rep = {"revision": REVISION, "r4_pairs_lost": [pair_id(cands["train"][i]) for i in lost],
           "lost_reasons": {pair_id(cands["train"][i]): forbid[i] for i in lost},
           "added_pairs": [pair_id(cands["train"][i]) for i in added],
           "swaps": [[pair_id(cands["train"][i]), pair_id(cands["train"][j])] for i, j in swaps],
           "new_pairs": [pair_id(cands["train"][i]) for i in new], "forbidden_candidates": len(forbid),
           "hard": round(obj.hard(T), 6), "penalty": round(obj.penalty(T), 4), "audit_fails": fails,
           "new_unaudited_source_rows": new_src}
    if a.new_out:
        Path(a.new_out).write_text(json.dumps(rep, indent=1) + "\n")
        log(f"wrote {a.new_out}: {len(new_src)} unaudited source rows in {len(new)} new pairs")
    if fails:
        raise SystemExit(f"the generator audit fails {fails}: not written")
    if not a.write:
        return
    if new_src and not a.allow_unaudited:
        raise SystemExit(f"{len(new_src)} source rows of the new pairs are not audited yet: audit them first")

    # ---- write r5 with the generator's own writer
    if not BACKUP.exists():
        BACKUP.mkdir(parents=True)
        for fn in R4_FILES:
            shutil.copy2(LEAN / "data/v14_parts" / fn, BACKUP / fn)
        log(f"backed up r4 to {BACKUP}")
    out_parts = {}
    r4_counts = json.loads((BACKUP / "f7_counts.json").read_text())
    for p, idx in (("train", sel), ("iid", prev["iid"]), ("holdout", prev["holdout"])):
        pl = SimpleNamespace(ladders=[cands[p][i] for i in idx])
        # the planner's reject tally belongs to the pool, which is r4's (summarize() reports it)
        pl.rejects = Counter(r4_counts["parts"][p].get("rejects") or {})
        pl.selection = {"pool_pairs": len(cands[p]), "kept_pairs": len(idx), "repair": REVISION if p == "train" else
                        "kept r4", "hard": rep["hard"] if p == "train" else None}
        out_parts[p] = pl
    import train_decoder as td
    for p, pl in out_parts.items():
        td.check_rows(g.rows_of(pl)[0], 0.5)
    allids = [r["id"] for pl in out_parts.values() for r in g.rows_of(pl)[0]]
    if len(allids) != len(set(allids)):
        raise SystemExit("duplicate row ids")
    counts = {"generator": g.GENERATOR, "version": g.VERSION, "revision": REVISION, "seed": g.SEED,
              "golden_train_sha256": g.GOLD_TRAIN_SHA,
              "repair": {"tool": "golden_src/gen3/f7_repair_r5.py", "from_revision": "r4",
                         "r4_train_sha256": R4_TRAIN_SHA, "drops_sha256": sha(DROPS),
                         **{k: v for k, v in rep.items() if k != "revision"}},
              "parts": {k: g.summarize(pl) for k, pl in out_parts.items()}}
    g.write_all(out_parts, counts, overwrite=a.overwrite, log=log)
    for p in ("probe", "probe_rel", "probe_meta"):
        if sha(LEAN / "data" / g.OUT[p]) != sha(BACKUP / Path(g.OUT[p]).name):
            raise SystemExit(f"{g.OUT[p]} changed: r5 must keep r4's probe byte for byte")
    log("r5 written; the probe files are byte-identical to r4's")


def main():
    need_hashseed()
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    sub = ap.add_subparsers(dest="cmd", required=True)
    d = sub.add_parser("dump")
    d.add_argument("--pool", required=True)
    r = sub.add_parser("repair")
    r.add_argument("--pool", required=True)
    r.add_argument("--new-out", default=None)
    r.add_argument("--write", action="store_true")
    r.add_argument("--overwrite", action="store_true")
    r.add_argument("--allow-unaudited", action="store_true", help="write although new source rows are unaudited")
    r.add_argument("--unread-cost", type=float, default=1.0,
                   help="hard-penalty cost of one source row the label audit has not read (fill preference)")
    a = ap.parse_args()
    log = log_fn()
    (stage_dump if a.cmd == "dump" else stage_repair)(a, log)


if __name__ == "__main__":
    main()
