"""F7 v2 r6: r5 repaired for the fixer review of 2 Oct 2026 (three findings; the r4 candidate pool is unchanged).

  1. Items 28 ('numeric bounds WITH negation') and 30 (De Morgan: not both / neither-nor / not (A or B)) reached their
     SHOULD train floor (150) only by counting unnegated R0 anchors (r5: 136 and 118 rows with a scoping negation).
     The generator's pair_features and yn2b/f7_precheck.py 3.1 now count a row toward these two items only when its
     scoping depth is >= 1. r6 adds train pairs from the SAME r4 candidate pool (whole twin pairs, the generator's
     Objective decides, already-audited source texts preferred) until every hard limit holds again.
  2. Same-answer links of a train ladder without R0 were 'inv' with a negated row (N2 / N4) as the stop-gradient
     anchor (470 of 2,654 links in r5). The generator's Planner.relations now writes them as 'equiv' (symmetric; the
     checklist's rule 2.2); every train ladder's relations are recomputed with it. Ladders WITH an R0 keep exactly
     r5's relations (checked).
  3. Depth 4 must be at most 3% of the rows of the probe too (checklist item 9, 'at most 3% of rows'; the dev also
     needs >= 40 depth-4 rows, CL:374). r5's probe has 144 depth-4 rows of 2,498 (5.76%). r6 drops the fewest
     depth-4 rows that reach the cap (72), chosen by a deterministic local search (pick_probe_trim) so that the
     dev-side checks of the precheck keep passing (lexeme parity 6.CSb, card style 4.6b, yes share per depth, the
     composition probes 6.C1-C6), every ladder keeps both golds and its rung semantics (9.6), the twin design holds
     (a row is always dropped with the same rung of its twin ladder: same question, opposite gold), and the held-out
     spec stays byte-identical; where removing even-depth rows pushes a lexeme over 60% odd, a few odd-depth iid twin
     rows (never a row of an aff/dneg pair) are dropped with them. Every kept probe line is byte-identical to r5's; relations
     touching a dropped row are dropped. gate/fix2_pairs.json (step 0a) is re-frozen afterwards (no model has read the
     probe).
  4. A train pair the r6 fill adds can push a cross-validated surface probe (check 5) over its bar in one stratum;
     as in r5, single swaps of the NEW pairs in the failing probe's worst stratum repair it.

Steps (CPU only, no model, OHS-3 never opened; PYTHONHASHSEED=0 like r5):
  repair --pool <r4 pool pkl from f7_repair_r5.py dump> [--new-out FILE] [--write --overwrite]
    - checks that the pool rebuilds r5's train files and the probe byte for byte (r5's selection, r5's relations);
    - forbids every candidate extra/build_fix2.py would drop (its current rules, imported);
    - fills: adds the spare pair that leaves the Objective's hard penalty lowest (+ --unread-cost per source row the
      label audit has not read), while the hard penalty falls; then the generator's audit (yn2b/f7_precheck.py as a
      library, full surface probes, the trimmed probe and the devx) must report no failing check;
    - lists every source row of the new pairs that the label audit has not read (--new-out); --write refuses while
      any is unread (read them, add flagged rows to yn2b/f7_fix2_drops.json, run again);
    - --write: backs up r5 once (data/v14_parts/f7_v2_r5_backup/) and writes r6: f7_train / f7_relations / f7_meta
      (rows_of on the new selection with the recomputed relations), the trimmed f7_probe / _relations / _meta, the
      unchanged held-out spec (checked), f7_counts.json ("revision": "r6").

  cd opendecide-data/lean
  PYTHONDONTWRITEBYTECODE=1 ../.venv/bin/python golden_src/gen3/f7_repair_r6.py repair --pool <scratch>/f7_pool_r4.pkl \
      --new-out <scratch>/f7_r6_new_sources.json [--write --overwrite]
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

REVISION = "r6"
V = LEAN / "data/v14_parts"
DROPS = LEAN / "yn2b/f7_fix2_drops.json"
AUDIT = LEAN / "yn2b/f7_source_label_audit.json"
BACKUP = V / "f7_v2_r5_backup"
R5_FILES = ("f7_train.jsonl", "f7_relations.jsonl", "f7_meta.jsonl", "f7_probe.jsonl", "f7_probe_relations.jsonl",
            "f7_probe_meta.jsonl", "f7_counts.json", "f7_holdout_spec.json")
R5_TRAIN_SHA = "018798bce6d804872fd1e6fdbcd400d8f6ac71ffe4d44222de16399f9de45d8f"
R5_PROBE_SHA = "f16c05a1749ce27ffd072dcbbab8697ca509d8e08fd544b85d6efa396fc17d0f"
PART_ABBR = {"train": "tr", "iid": "ii", "holdout": "ho"}
DEPTH4_DEV_CAP = 0.03       # CL:61
DEPTH4_DEV_MIN = 40         # CL:374


def sha(p: Path) -> str:
    return hashlib.sha256(p.read_bytes()).hexdigest()


def log_fn():
    t0 = time.time()
    return lambda s: print(f"[{time.time() - t0:6.0f}s] {s}", flush=True)


def need_hashseed():
    if os.environ.get("PYTHONHASHSEED") != "0":
        os.environ["PYTHONHASHSEED"] = "0"
        os.execv(sys.executable, [sys.executable] + sys.argv)


def as_lad(c):
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
    rows, metas, rels = g.rows_of(SimpleNamespace(ladders=lads))
    dump = lambda xs: [json.dumps(x, ensure_ascii=False) for x in xs]  # noqa: E731
    return dump(rows), dump(rels), dump(g.strip_private(metas))


def relink(g, lad):
    """The ladder with its train relations recomputed by the generator's (r6) Planner.relations."""
    shim = SimpleNamespace(part="train")
    new = {tw: g.Planner.relations(shim, lad["rows"][tw]) for tw in ("A", "B")}
    return {**lad, "rels": new}


def trim_ladder(lad, drop_ids):
    rows = {tw: [x for x in lad["rows"][tw] if x[0]["id"] not in drop_ids] for tw in ("A", "B")}
    rels = {tw: [x for x in lad["rels"][tw] if x["a"] not in drop_ids and x["b"] not in drop_ids] for tw in ("A", "B")}
    return {**lad, "rows": rows, "rels": rels}


def diagnose(g, obj, T, words):
    """Which hard terms are left: the instruction-word parity rule (with the base), lexeme parity, the rest."""
    import copy
    h = obj.hard(T)
    o2 = copy.copy(obj)
    o2.words = set()
    h_nowords = o2.hard(T)
    bad_words = []
    for w in sorted(words):
        r = T[("w_r", w)] + obj.base[("w_r", w)]
        if r >= 26:
            over = T[("w_o", w)] + obj.base[("w_o", w)] - 0.59 * r
            if over > 0:
                bad_words.append((w, r, T[("w_o", w)] + obj.base[("w_o", w)], round(over, 3),
                                  round((T[("w_o", w)] + obj.base[("w_o", w)]) / r, 4)))
    print(f"DIAGNOSE hard {h:.4f}; without the word rule {h_nowords:.4f}; words over 59% odd {bad_words}", flush=True)
    ok = h_nowords <= 1e-12 and all(o / r <= 0.60 + 1e-12 for _, r, o, _, _ in bad_words if r >= 30)
    return ok, [{"word": w, "rows": r, "odd_rows": o, "odd_share": sh} for w, r, o, _, sh in bad_words]



def pick_probe_trim(g, pmeta, spec_now, frozen_pairs, log):
    """The probe rows r6 drops (finding 3). Exactly the fewest depth-4 rows that bring depth 4 to <= 3% of the probe
    (CL:61) with >= 40 left (CL:374), chosen so that the dev-side checks of yn2b/f7_precheck.py keep passing:
      6.CSb  odd-parity share 40-60% for every lexeme with >= 30 dev yes/no rows (removing even rows raises it);
      4.6b   card style share within +- 2 points per depth and per gold; 4.x yes share per depth;
      6.C1-C6 composition probes on the dev (2 points of margin);
    rows are dropped in TWIN units (a row and the same rung of its twin ladder: same question, opposite gold), so the
    twin design (no surface feature predicts the gold) holds for every kept row; every ladder keeps both golds and its
    rung semantics (9.6: a D row keeps its twin, an AR row its odd sibling), and the held-out spec is unchanged.
    Deterministic local search: start from every iid depth-4 twin unit plus the held-out ones needed, swap one dropped
    unit for a kept one while the penalty falls; if a lexeme is still out of band, also drop odd-depth iid twin units
    (never a row of a frozen aff/dneg pair: those are R0 / even-depth rows)."""
    import f7_precheck as fp
    from collections import defaultdict
    rows = {k: v[3] for k, v in pmeta.items()}
    metas = {k: v[4] for k, v in pmeta.items()}
    strip = {k: g.strip_private([m])[0] for k, m in metas.items()}
    ctx = fp.Ctx({"probe": list(rows.values())}, list(strip.values()), {"probe": []},
                 fp.Opts(fast=True, unseen=False), log=lambda s_: None)
    comp = {R["row"]["id"]: (fp.comp_preds(R), R["row"]["gold"], R["an"]["depth"]) for R in ctx.dev if R["an"]["yn"]}
    info = {k: dict(par=m["depth"] % 2, d=m["depth"], lex={c["lexeme"].lower() for c in m["cues"]},
                    st=m["card_style"], g=int(rows[k]["gold"]), kind=m["dev_kind"])
            for k, m in metas.items() if rows[k]["qtype"] == "noul"}
    lad_rows = defaultdict(list)
    for k, m in metas.items():
        lad_rows[m["ladder_id"]].append(k)
    n_all = len(rows)
    d4 = sorted(k for k, v in info.items() if v["d"] == 4)
    k_drop = 0
    while (len(d4) - k_drop) / (n_all - k_drop) > DEPTH4_DEV_CAP + 1e-12:
        k_drop += 1
    k_drop += k_drop % 2
    in_pair = {x for a_, b_, _ in frozen_pairs for x in (a_, b_)}

    def spec_ok(drop):
        hm = [strip[k] for k in metas if metas[k]["dev_kind"] == "holdout" and k not in drop]
        return g.holdout_spec_json(hm) == spec_now

    def rung_ok(drop):
        for ids0 in lad_rows.values():
            ids = [k for k in ids0 if k not in drop]
            gold = {k: str(rows[k]["gold"]) for k in ids}
            for k in ids:
                m = metas[k]
                if m["rung"] == "D" and not any(
                        j != k and metas[j]["n_distractor"] < m["n_distractor"] and metas[j]["depth"] == m["depth"]
                        and rows[j]["qtype"] == rows[k]["qtype"] and gold[j] == gold[k] for j in ids):
                    return False
                if m["rung"] == "AR" and not any(j != k and metas[j]["depth"] % 2 == 1 and metas[j]["rung"] != "AR"
                                                 and gold[j] == gold[k] for j in ids):
                    return False
            if any(k in info for k in ids0) and len({info[k]["g"] for k in ids if k in info}) < 2:
                return False
        return True

    def penalty(drop, detail=False):
        keep = [k for k in info if k not in drop]
        pen, bad = 0.0, {}
        par = defaultdict(lambda: [0, 0])
        for k in keep:
            for x in info[k]["lex"]:
                par[x][0] += info[k]["par"]
                par[x][1] += 1
        for x, (o, n) in par.items():
            if n >= 30 and abs(o - n * 0.5) - max(n * 0.1, 1) > 1e-9:
                pen += abs(o - n * 0.5) - max(n * 0.1, 1)
                bad[f"CS:{x}"] = (o, n)
        N = len(keep)
        sty = Counter(info[k]["st"] for k in keep)
        for key in ("d", "g"):
            grp = defaultdict(list)
            for k in keep:
                grp[info[k][key]].append(k)
            for gv, ks in grp.items():
                for st, c in sty.items():
                    kk = sum(1 for k in ks if info[k]["st"] == st)
                    over = abs(kk - len(ks) * c / N) - max(len(ks) * 0.02, 1)
                    if over > 1e-9:
                        pen += over
                        bad[f"style:{st}:{key}={gv}"] = (kk, len(ks))
        grp = defaultdict(list)
        for k in keep:
            grp[info[k]["d"]].append(k)
        for gv, ks in grp.items():
            y = sum(info[k]["g"] for k in ks)
            over = abs(y - len(ks) * 0.5) - max(len(ks) * 0.02, 1)
            if over > 1e-9:
                pen += over
                bad[f"yes:d={gv}"] = (y, len(ks))
        ks = [k for k in keep if k in comp]
        n = len(ks)
        acc, c2d = Counter(), defaultdict(lambda: [0, 0])
        for k in ks:
            pr, gg, d = comp[k]
            for nm, v in pr.items():
                acc[nm] += int(v == gg)
            c2d[d][0] += int(pr["C2 count all cues"] == gg)
            c2d[d][1] += 1
        bars = {"C2 count all cues": 0.698, "C3 count syntactic cues": 0.648, "C4 outer cue only": 0.598,
                "C5 inner cue only": 0.598, "C6 counter ignoring affixal": 0.598, "C6 counter ignoring lexical": 0.598,
                "C6 counter ignoring cross-sentence": 0.598}
        for nm, bar in bars.items():
            if acc[nm] - bar * n > 1e-9:
                pen += acc[nm] - bar * n
                bad[f"comp:{nm}"] = round(acc[nm] / n, 4)
        c1 = acc["C1 ignore negation"] / n
        if not 0.452 <= c1 <= 0.548:
            pen += n * (max(0.0, 0.452 - c1) + max(0.0, c1 - 0.548))
            bad["comp:C1"] = round(c1, 4)
        for d, (c, nn) in c2d.items():
            if c > 0.748 * nn:
                pen += c - 0.748 * nn
                bad[f"comp:C2:d={d}"] = round(c / nn, 4)
        return (pen, bad) if detail else pen

    def valid(drop):
        return rung_ok(drop) and spec_ok(drop)

    # twin units: a ladder pair's twins have the same rung plan and opposite golds (the generator's twin design and
    # yn2b/tests/test_gen3_nested_negation.py's invariant), so a row is dropped only together with its twin row
    import re as _re

    def twin(k):
        m_ = _re.match(r"^(.*_\d{5})([ab])(_\d+)$", k)
        return m_.group(1) + ("b" if m_.group(2) == "a" else "a") + m_.group(3)

    def unit_of(k):
        t = twin(k)
        if t not in metas or metas[t]["rung"] != metas[k]["rung"] or metas[t]["depth"] != metas[k]["depth"] \
                or str(rows[t]["gold"]) == str(rows[k]["gold"]):
            raise SystemExit(f"probe trim: {k} has no proper twin row {t}")
        return tuple(sorted((k, t)))
    u4 = sorted({unit_of(k) for k in d4})
    rows_of = lambda units: {x for u in units for x in u}  # noqa: E731
    # start: every iid depth-4 twin unit, then held-out depth-4 units until the cap holds
    drop_u = {u for u in u4 if info[u[0]]["kind"] == "iid"}
    hold_u = [u for u in u4 if info[u[0]]["kind"] == "holdout"]
    while 2 * len(drop_u) < k_drop:
        nxt = next((u for u in hold_u if u not in drop_u and valid(rows_of(drop_u | {u}))), None)
        if nxt is None:
            raise SystemExit("probe trim: cannot reach the depth-4 cap with valid drops")
        drop_u.add(nxt)
    drop = rows_of(drop_u)
    if len(drop) != k_drop or sum(info[k]["g"] for k in drop) * 2 != k_drop:
        raise SystemExit(f"probe trim start: {len(drop)} rows, {sum(info[k]['g'] for k in drop)} yes")
    cur = penalty(drop)
    log(f"probe trim: start {k_drop} depth-4 rows ({len(drop_u)} twin units), penalty {cur:.3f} "
        f"{penalty(drop, True)[1]}")
    while cur > 1e-9:
        cands_sw = []
        for out in sorted(drop_u):
            for inn in u4:
                if inn in drop_u:
                    continue
                p_ = penalty(rows_of((drop_u - {out}) | {inn}))
                if p_ < cur - 1e-9:
                    cands_sw.append((p_, out, inn))
        cands_sw.sort()
        step = next(((p_, o, i_) for p_, o, i_ in cands_sw if valid(rows_of((drop_u - {o}) | {i_}))), None)
        if step is None:
            break
        cur, o, i_ = step
        drop_u = (drop_u - {o}) | {i_}
        log(f"  trim swap {o[0]} (+ twin) -> {i_[0]} (+ twin): penalty {cur:.3f}")
    drop = rows_of(drop_u)
    extra_u = set()
    while cur > 1e-9:
        bad_lex = {k.split(":", 1)[1] for k in penalty(drop | rows_of(extra_u), True)[1] if k.startswith("CS:")}
        odd_u = sorted({unit_of(k) for k, v in info.items() if v["par"] == 1 and v["kind"] == "iid"
                        and (not bad_lex or v["lex"] & bad_lex)})
        odd_u = [u for u in odd_u if u not in extra_u and not (set(u) & in_pair)]
        best = None
        for u in odd_u:
            nd = drop | rows_of(extra_u | {u})
            p_ = penalty(nd)
            if p_ < cur - 1e-9 and (best is None or p_ < best[0]) and valid(nd):
                best = (p_, u)
        if best is None:
            raise SystemExit(f"probe trim: penalty {cur:.3f} left {penalty(drop | rows_of(extra_u), True)[1]}: stop")
        cur = best[0]
        extra_u.add(best[1])
        log(f"  trim + odd twin rows {best[1]}: penalty {cur:.3f}")
    extra = rows_of(extra_u)
    allx = drop | extra
    left4 = len(d4) - len(drop)
    if not (left4 >= DEPTH4_DEV_MIN and left4 / (n_all - len(allx)) <= DEPTH4_DEV_CAP + 1e-12 and valid(allx)):
        raise SystemExit("probe trim: the final set breaks a constraint")
    rep = {"depth4_iid": sum(1 for k in drop if info[k]["kind"] == "iid"),
           "depth4_holdout": sum(1 for k in drop if info[k]["kind"] == "holdout"), "odd_rows": len(extra),
           "odd_rows_ids": sorted(extra), "frozen_pairs_touched": sum(1 for a_, b_, _ in frozen_pairs
                                                                      if a_ in allx or b_ in allx),
           "rule": "fewest depth-4 rows to reach <= 3% (CL:61, >= 40 left CL:374); chosen by a deterministic local "
                   "search that keeps precheck 6.CSb, 4.6b, the per-depth yes share and 6.C1-C6 on the dev passing; "
                   "odd-depth iid rows (never in an aff/dneg pair) added only to rebalance a lexeme's parity; rows "
                   "always dropped with their twin row (same rung of the twin ladder, opposite gold)"}
    return allx, rep

# ------------------------------------------------------------------------------------------------ repair
def stage_repair(a, log):
    import gen3_nested_negation as g
    import nn_lexicon as lx
    with open(a.pool, "rb") as f:
        pool = pickle.load(f)
    if pool["revision_of_pool"] != "r4" or pool["seed"] != g.SEED or pool["hashseed"] != "0":
        raise SystemExit(f"pool {a.pool} is not the r4 pool")
    src_dir = BACKUP if BACKUP.exists() else V
    if sha(src_dir / "f7_train.jsonl") != R5_TRAIN_SHA or sha(src_dir / "f7_probe.jsonl") != R5_PROBE_SHA:
        raise SystemExit(f"{src_dir} does not hold r5's files (sha256 of f7_train / f7_probe)")
    cands = {p: [as_lad(c) for c in pool["parts"][p]["cands"]] for p in ("train", "iid", "holdout")}
    idx_of = {p: {pair_id(l): i for i, l in enumerate(cands[p])} for p in cands}
    prev = {p: set() for p in cands}
    for fn in ("f7_train.jsonl", "f7_probe.jsonl"):
        for line in file_lines(src_dir / fn):
            lid = json.loads(line)["meta"]["latent_id"][:-1]
            part = {v: k for k, v in PART_ABBR.items()}[lid.split("-")[1]]
            if lid not in idx_of[part]:
                raise SystemExit(f"r5 pair {lid} is not in the pool")
            prev[part].add(idx_of[part][lid])
    prev = {p: sorted(v) for p, v in prev.items()}
    tr = selection_lines(g, [cands["train"][i] for i in prev["train"]])
    pr = [x + y for x, y in zip(selection_lines(g, [cands["iid"][i] for i in prev["iid"]]),
                                selection_lines(g, [cands["holdout"][i] for i in prev["holdout"]]))]
    for name, lines in (("f7_train.jsonl", tr[0]), ("f7_relations.jsonl", tr[1]), ("f7_meta.jsonl", tr[2]),
                        ("f7_probe.jsonl", pr[0]), ("f7_probe_relations.jsonl", pr[1]),
                        ("f7_probe_meta.jsonl", pr[2])):
        if lines != file_lines(src_dir / name):
            raise SystemExit(f"the pool does not rebuild r5's {name} byte for byte: stop")
    log(f"pool reproduces r5 byte for byte (train {len(prev['train'])} pairs, iid {len(prev['iid'])}, holdout "
        f"{len(prev['holdout'])}); train candidates {len(cands['train'])}")

    # ---- finding 2: recompute every train candidate's relations with the r6 writer; ladders with an R0 must keep r5's
    rel_change = Counter()
    for i, lad in enumerate(cands["train"]):
        new = relink(g, lad)
        for tw in ("A", "B"):
            old_r, new_r = lad["rels"][tw], new["rels"][tw]
            has_r0 = any(m["rung"] == "R0" for _, m, _ in lad["rows"][tw])
            if has_r0 and old_r != new_r:
                raise SystemExit(f"{pair_id(lad)}{tw}: a ladder with R0 changed its relations")
            if [(x["a"], x["b"]) for x in old_r] != [(x["a"], x["b"]) for x in new_r]:
                raise SystemExit(f"{pair_id(lad)}{tw}: the relation ends changed")
            for x, y in zip(old_r, new_r):
                if x["type"] != y["type"]:
                    if (x["type"], y["type"]) != ("inv", "equiv"):
                        raise SystemExit(f"{pair_id(lad)}{tw}: unexpected relation change {x} -> {y}")
                    if i in set(prev["train"]):
                        rel_change["r5 links inv->equiv"] += 1
        cands["train"][i] = new

    # ---- finding 3: trim the probe's depth-4 rows to <= 3% (the dev-side balance checks keep passing)
    pmeta = {}
    for p in ("iid", "holdout"):
        for i in prev[p]:
            for tw in ("A", "B"):
                for row, m, rd in cands[p][i]["rows"][tw]:
                    pmeta[row["id"]] = (p, i, tw, row, m, rd)
    spec_now = json.loads((src_dir / "f7_holdout_spec.json").read_text())
    frozen_pairs = json.loads((LEAN / "gate/fix2_pairs.json").read_text())["splits"]["f7_probe"]["list"] \
        if (LEAN / "gate/fix2_pairs.json").exists() else []
    cache = Path(a.trim_cache) if a.trim_cache else None
    key = {"r5_probe_sha256": R5_PROBE_SHA, "tool_sha256": sha(Path(__file__)),
           "pairs_sha256": sha(LEAN / "gate/fix2_pairs.json") if (LEAN / "gate/fix2_pairs.json").exists() else None}
    cached = json.loads(cache.read_text()) if cache and cache.exists() else None
    if cached and cached.get("key") == key:
        drop_probe, trim_rep = set(cached["drop"]), cached["rep"]
        log(f"probe trim: loaded from {cache} (same r5 probe, same tool, same pair file)")
    else:
        drop_probe, trim_rep = pick_probe_trim(g, pmeta, spec_now, frozen_pairs, log)
        if cache:
            cache.write_text(json.dumps({"key": key, "drop": sorted(drop_probe), "rep": trim_rep}, indent=1))
    n_probe = len(pmeta)
    d4_total = sum(1 for v in pmeta.values() if v[4]["depth"] == 4)
    left4 = d4_total - sum(1 for k in drop_probe if pmeta[k][4]["depth"] == 4)
    trimmed = {p: [trim_ladder(cands[p][i], drop_probe) for i in prev[p]] for p in ("iid", "holdout")}
    log(f"probe trim: {len(drop_probe)} rows ({trim_rep['depth4_iid']} iid + {trim_rep['depth4_holdout']} held-out "
        f"depth-4 rows, {trim_rep['odd_rows']} odd-depth iid rows); depth 4 {d4_total}/{n_probe} -> "
        f"{left4}/{n_probe - len(drop_probe)} = {left4 / (n_probe - len(drop_probe)):.4f}")

    # ---- what fix2 would drop (extra/build_fix2.py's own F7 rules, imported)
    import build_fix2 as bf2
    drops = json.loads(DROPS.read_text())
    drop_pairs, drop_src = set(drops["f7_pairs"]), set(drops["source_row_ids"])
    bad_ids = set(json.loads((LEAN / "yn2b/label_audit_known_bad_ids.json").read_text())["all_ids"]) | drop_src | set(drops.get("probe_source_row_ids") or {})
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
                    why |= set(w)
        if why:
            forbid[i] = sorted(why)
    lost = [i for i in prev["train"] if i in forbid]
    log(f"forbidden train candidates {len(forbid)} ({Counter(r for v in forbid.values() for r in v)}); r5 pairs "
        f"lost {len(lost)} {[pair_id(cands['train'][i]) for i in lost][:8]}")

    # ---- the train objective (r6 pair_features: items 28 / 30 count depth >= 1 rows only)
    base = g.devx_word_base()
    for p in ("iid", "holdout"):
        for lad in trimmed[p]:
            f_ = g.pair_features(lad, None)
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
    log(f"r5 minus forbidden: {len(sel)} pairs; items 28 / 30 (depth >= 1) {T[('item', 28)]} / {T[('item', 30)]}; "
        f"hard {obj.hard(T):.4f}, penalty {obj.penalty(T):.3f}")
    audited = set(json.loads(AUDIT.read_text()).get("rows_read_ids", []))
    unread = [len(lad_sources(c) - audited) for c in cands["train"]]
    n_min = g.N_PAIRS["train"]
    added = []
    # refill to r5's size first (pairs lost to the current fix2 rules), then add while the hard penalty falls
    while len(sel) < n_min or obj.hard(T) > 1e-12:
        h0 = obj.hard(T)
        best = None
        for j in spare:
            T.update(feats[j])
            key = (round(obj.hard(T), 9) + a.unread_cost * unread[j], obj.penalty(T), j)
            h1 = obj.hard(T)
            T.subtract(feats[j])
            if len(sel) >= n_min and h1 >= h0 - 1e-12:
                continue
            if best is None or key < best:
                best = key
        if best is None:
            log(f"  hard {h0:.4f}: no spare pair lowers it by adding; swap phase next")
            break
        j = best[2]
        T.update(feats[j])
        sel.append(j)
        spare.remove(j)
        added.append(j)
        log(f"  + {pair_id(cands['train'][j])} (unread source rows {unread[j]}): hard {obj.hard(T):.4f}, items 28 / 30 "
            f"{T[('item', 28)]} / {T[('item', 30)]}")
        if len(added) > a.max_add:
            raise SystemExit(f"more than {a.max_add} pairs added: stop")
    # swap phase (as r5): swap one ADDED pair (r5's own pairs stay) for a spare while the hard penalty strictly falls;
    # among the improving swaps the lowest (hard + unread cost, penalty) wins
    swaps, margin_note = [], []
    while obj.hard(T) > 1e-12:
        h0 = obj.hard(T)
        best = None
        for i in list(added):
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
            ok_margin, why = diagnose(g, obj, T, words)
            if ok_margin:
                # the only term left is the generator's own 1-point margin on the SPEC 7.3 word rule (0.59); every word
                # is still within the rule itself (<= 60% odd at >= 30 rows), which precheck 8.9 checks below
                log(f"  residual hard {h0:.4f} is the generator's 0.59 word margin only ({why}); SPEC 7.3's 60% holds")
                margin_note.append(why)
                break
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
    log(f"train: {len(sel)} pairs ({len(added)} added, {len(swaps)} swaps), hard {obj.hard(T):.4f}, penalty "
        f"{obj.penalty(T):.3f}, items 28 / 30 {T[('item', 28)]} / {T[('item', 30)]}")

    # ---- the generator's audit on the new selection (trimmed probe, devx), as f7_repair_r5 runs it
    import f7_precheck as fp

    def run_audit(sel_train, quick):
        rows, metas, rels, hold_m = {}, [], {}, []
        parts = (("train", [cands["train"][i] for i in sel_train]), ("iid", trimmed["iid"]),
                 ("holdout", trimmed["holdout"]))
        for p, lads in parts:
            r_, m_, rl = g.rows_of(SimpleNamespace(ladders=lads))
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
    log(f"generator audit: failing checks {sorted(fails)} {json.dumps(fails, default=str)[:600]}")
    # check 5 (cross-validated surface probes; the Objective does not model them): as in r5, swap ONE new pair at a
    # time, chosen in the failing probe's worst train stratum, for a spare that does not raise the hard penalty
    # (spares whose source rows are audited or that have none first); keep the swap only when the failing probes
    # pass and no other check-5 item starts to fail
    import random as _random
    rng = _random.Random(g.SEED + 66)
    guided = []
    for rnd in range(1, 31):
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
        h_now = obj.hard(T)
        hit = None
        for pool_j in (clean[:40], other[:15]):
            for t in targets[:10]:
                for j in pool_j:
                    T2 = Counter(T)
                    T2.subtract(feats[t])
                    T2.update(feats[j])
                    if obj.hard(T2) > h_now + 1e-12:
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
            log(f"  check-5 repair round {rnd}: no single swap fixes {tid} (stratum {strat})")
            break
        t, j, T, sel = hit
        spare.remove(j)
        spare.append(t)
        if t in added:
            added[added.index(t)] = j
        guided.append((t, j))
        log(f"  check-5 repair round {rnd}: {pair_id(cands['train'][t])} -> {pair_id(cands['train'][j])} "
            f"(stratum {strat}); hard {obj.hard(T):.4f}")
        fails = run_audit(sel, quick=False)
        log(f"  generator audit: failing checks {sorted(fails)} {json.dumps(fails, default=str)[:400]}")
    swaps += guided
    new = sorted(set(sel) - set(prev["train"]))
    new_src = {}
    for i in new:
        for s_ in sorted(lad_sources(cands["train"][i]) - audited):
            new_src.setdefault(s_, []).append(pair_id(cands["train"][i]))
    rep = {"revision": REVISION, "r5_pairs_lost": [pair_id(cands["train"][i]) for i in lost],
           "lost_reasons": {pair_id(cands["train"][i]): forbid[i] for i in lost},
           "added_pairs": [pair_id(cands["train"][i]) for i in added],
           "swaps": [[pair_id(cands["train"][i]), pair_id(cands["train"][j])] for i, j in swaps],
           "new_pairs": [pair_id(cands["train"][i]) for i in new], "forbidden_candidates": len(forbid),
           "hard": round(obj.hard(T), 6), "penalty": round(obj.penalty(T), 4), "audit_fails": sorted(fails),
           "hard_residual_note": (f"the residual is the generator's 0.59 instruction-word margin only: {margin_note[0]}; "
                                  "every word stays within SPEC 7.3's 60% (precheck 8.9)") if margin_note else None,
           "items_depth1": {"28": T[("item", 28)], "30": T[("item", 30)]},
           "relations_inv_to_equiv_in_r5_ladders": rel_change["r5 links inv->equiv"],
           "probe_trim": {"dropped_rows": sorted(drop_probe), **trim_rep,
                          "depth4_before": [d4_total, n_probe], "depth4_after": [left4, n_probe - len(drop_probe)]},
           "new_unaudited_source_rows": new_src}
    if a.new_out:
        Path(a.new_out).write_text(json.dumps(rep, indent=1) + "\n")
        log(f"wrote {a.new_out}: {len(new_src)} unaudited source rows in {len(new)} new pairs")
    if fails:
        raise SystemExit(f"the generator audit fails {sorted(fails)}: not written")
    if not a.write:
        return
    if new_src:
        raise SystemExit(f"{len(new_src)} source rows of the new pairs are not audited yet: audit them first")

    # ---- write r6
    if not BACKUP.exists():
        BACKUP.mkdir(parents=True)
        for fn in R5_FILES:
            shutil.copy2(V / fn, BACKUP / fn)
        log(f"backed up r5 to {BACKUP}")
    import train_decoder as td
    import yn2b_common as yc
    pl_train = SimpleNamespace(ladders=[cands["train"][i] for i in sorted(sel)])
    t_rows, t_metas, t_rels = g.rows_of(pl_train)
    td.check_rows(t_rows, 0.5)
    dump = lambda xs: [json.dumps(x, ensure_ascii=False) for x in xs]  # noqa: E731
    outs = {k: yc.guard_out(V / k, inputs=[], overwrite=a.overwrite)
            for k in ("f7_train.jsonl", "f7_relations.jsonl", "f7_meta.jsonl", "f7_probe.jsonl",
                      "f7_probe_relations.jsonl", "f7_probe_meta.jsonl", "f7_counts.json")}
    yc.write_lines_atomic(outs["f7_train.jsonl"], dump(t_rows))
    yc.write_lines_atomic(outs["f7_relations.jsonl"], dump(t_rels))
    yc.write_lines_atomic(outs["f7_meta.jsonl"], dump(g.strip_private(t_metas)))
    # the probe: r5's lines minus the dropped rows (byte copies of every kept line)
    keep = lambda line: json.loads(line)["id"] not in drop_probe  # noqa: E731
    keep_rel = lambda line: not ({json.loads(line)["a"], json.loads(line)["b"]} & drop_probe)  # noqa: E731
    yc.write_lines_atomic(outs["f7_probe.jsonl"], [x for x in file_lines(src_dir / "f7_probe.jsonl") if keep(x)])
    yc.write_lines_atomic(outs["f7_probe_relations.jsonl"],
                          [x for x in file_lines(src_dir / "f7_probe_relations.jsonl") if keep_rel(x)])
    yc.write_lines_atomic(outs["f7_probe_meta.jsonl"], [x for x in file_lines(src_dir / "f7_probe_meta.jsonl") if keep(x)])
    p_rows, _, p_rels = g.rows_of(SimpleNamespace(ladders=trimmed["iid"] + trimmed["holdout"]))
    if [r["id"] for r in p_rows] != [json.loads(x)["id"] for x in file_lines(V / "f7_probe.jsonl")]:
        raise SystemExit("the trimmed probe file differs from the trimmed ladders")
    if len(p_rels) != len(file_lines(V / "f7_probe_relations.jsonl")):
        raise SystemExit("the trimmed probe relations differ from the trimmed ladders")
    if g.holdout_spec_json(g.strip_private([m for lad in trimmed["holdout"] for tw in ("A", "B")
                                            for _, m, _ in lad["rows"][tw]])) != spec_now:
        raise SystemExit("held-out spec changed")
    r5_counts = json.loads((BACKUP / "f7_counts.json").read_text())
    counts = {"generator": g.GENERATOR, "version": g.VERSION, "revision": REVISION, "seed": g.SEED,
              "golden_train_sha256": g.GOLD_TRAIN_SHA,
              "repair": {"tool": "golden_src/gen3/f7_repair_r6.py", "from_revision": "r5",
                         "r5_train_sha256": R5_TRAIN_SHA, "r5_probe_sha256": R5_PROBE_SHA, "drops_sha256": sha(DROPS),
                         **{k: v for k, v in rep.items() if k != "revision"}},
              "r5_repair": r5_counts.get("repair"),
              "parts": {"train": g.summarize(SimpleNamespace(ladders=pl_train.ladders, rejects=Counter(
                  r5_counts["parts"]["train"].get("rejects") or {}), selection={"pool_pairs": len(cands["train"]),
                                                                            "kept_pairs": len(sel), "repair": REVISION,
                                                                            "hard": rep["hard"]})),
                        **{p: g.summarize(SimpleNamespace(ladders=trimmed[p], rejects=Counter(
                            r5_counts["parts"][p].get("rejects") or {}),
                            selection={"pool_pairs": len(cands[p]), "kept_pairs": len(prev[p]),
                                       "repair": "kept r5 (= r4) minus the depth-4 trim"}))
                           for p in ("iid", "holdout")}}}
    counts["files"] = {f"v14_parts/{k}": sha(V / k) for k in ("f7_train.jsonl", "f7_relations.jsonl", "f7_meta.jsonl",
                                                              "f7_probe.jsonl", "f7_probe_relations.jsonl",
                                                              "f7_probe_meta.jsonl", "f7_defs.json", "f7_lexicon.json",
                                                              "f7_holdout_spec.json")}
    yc.write_json(outs["f7_counts.json"], counts)
    log(f"r6 written: train {len(t_rows)} rows / {len(sel)} pairs, relations {dict(Counter(x['type'] for x in t_rels))}; "
        f"probe {len(p_rows)} rows; sha256 train {counts['files']['v14_parts/f7_train.jsonl']}, probe "
        f"{counts['files']['v14_parts/f7_probe.jsonl']}")


def main():
    need_hashseed()
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    sub = ap.add_subparsers(dest="cmd", required=True)
    r = sub.add_parser("repair")
    r.add_argument("--pool", required=True)
    r.add_argument("--new-out", default=None)
    r.add_argument("--write", action="store_true")
    r.add_argument("--overwrite", action="store_true")
    r.add_argument("--unread-cost", type=float, default=1.0)
    r.add_argument("--max-add", type=int, default=40)
    r.add_argument("--trim-cache", default=None, help="cache file for the probe trim (recomputed when inputs change)")
    a = ap.parse_args()
    stage_repair(a, log_fn())


if __name__ == "__main__":
    main()
