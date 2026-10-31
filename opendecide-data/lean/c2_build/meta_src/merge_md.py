"""merge_md.py: merge the per-source metadata-block parts into the MD block that mix_c2.py reads (A42-D 8; c2io layout).

  data/c2_md_parts/<source>/{rows.jsonl, relations.jsonl, MANIFEST.json, noise_gate/...}     (one mapper per source)
      -> data/c2_parts/MD/out/{candidates_c2.jsonl, candidates_c2.relations.jsonl, MANIFEST.json}
         data/c2_parts/MD/qc/{QC_REPORT.json, MD_MERGE_REPORT.json, dropped_tasks.json}

Steps (in this order; nothing is relabelled, edited or added; only rows and whole tasks are removed):
 1. Load every source part (a source needs rows.jsonl + MANIFEST.json). Rows are normalised to the mix's keys
    (source with the "c2_" prefix negtwins expects, meta.family "MD", meta.domain, meta.task_id, meta.card_id). A row with meta.sampler S5 or meta.dev_only is
    refused (candidates are never dev rows). Self-made twin rows of the mappers (meta.twin_of / twin_kind / role "twin")
    are dropped here (orchestrator ruling 16 Oct: MD negation twins come only from negtwins.block_twins md, the frozen
    item-7 catalogue); they stay readable for the gate because the seeded 13 rows per task were drawn before this step.
 2. Noise gate (A42-D 8.4). Per source, the seeded 13 rows per task were read blind by Haiku (noise_gate/chunks, key/;
    the group-A sources keep SEEDED_PICK.json and key/ in noise_gate_orch/). Answers go to <source>/noise_gate/answers/*.json
    ({qid: {"answer", "confidence"}} or a list with qid). Only key files whose every row id is in rows.jsonl are used (a
    key from an earlier run of a mapper is stale). A row is "clearly wrong" when the normalised answer differs from gold
    at confidence >= 0.7 (A51 a; --min-conf overrides). Picked rows that are mapper twins do not count (A51 b; the task is
    judged on its remaining base picks; --gate-count-twins overrides). A task with 2 or more of its picked rows clearly
    wrong is dropped whole. A source left under 40 tasks keeps them (A51 c): recorded as a deviation, not refilled. Invalid answers are counted apart. A source
    with no answers makes the gate "pending": the merge refuses unless --allow-pending-gate.
 3. Caps (A42-D 8.2, 7.1), by seeded whole-task removal (hash of seed, tag, task id): twins <= 5,000; rows <= 12,000;
    no domain above 20%; no source above 15%. A task is never removed below 40 tasks in its source.
 4. Floors, reported as QC problems: 8,000 rows or more, at least 8 domains, >= 30% card-free rows per source,
    40-80 tasks per source, <= 200 rows per task, twins <= 5,000, unique ids, relations inside the kept rows, plus the
    mixer's own check (mix_c2.block_rules and c2io.candidate_problems) when importable.
 5. Write the C2 block files (c2io writers: A38 guard, lean/ only) with the MANIFEST sha256 / rows contract and a
    QC_REPORT (pass = no problem and the gate complete for every source).

  .venv/bin/python -B meta_src/merge_md.py --dry-run [--allow-pending-gate]
  .venv/bin/python -B meta_src/merge_md.py            # after the Haiku answers (and the confirmation file) exist
"""
from __future__ import annotations

import argparse
import datetime
import hashlib
import json
import math
import sys
from collections import Counter, defaultdict
from pathlib import Path

HERE = Path(__file__).resolve().parent
BUILD = HERE.parent
LEAN = BUILD.parent
sys.path.insert(0, str(BUILD))
PARTS = LEAN / "data" / "c2_md_parts"
SEED = 20261013
SRC_MAX, DOM_MAX, N_MIN, N_MAX, DOM_MIN, TWIN_MAX = 0.15, 0.20, 8000, 12000, 8, 5000
CARD_FREE_MIN, TASK_ROWS_MAX, TASKS_PER_SOURCE = 0.30, 200, (40, 80)
CLEAR_CONF, NOISE_DROP = 0.7, 0.08              # A51 (a): clearly wrong = the blind read disagrees with gold at confidence >= 0.7, all 11 sources
NOISE_MIN_WRONG = 2                              # A42-D 8.4: 2 or more of the 13
# openalex (scholarly_publishing) and ror (research_organisations) share one domain for the 20% cap (16 Oct ruling)
DOMAIN_GROUP = {"scholarly_publishing": "scholarly", "research_organisations": "scholarly"}


def hx(*p) -> int:
    return int(hashlib.sha256("|".join(map(str, p)).encode()).hexdigest()[:15], 16)


def sha256_bytes(b: bytes) -> str:
    return hashlib.sha256(b).hexdigest()


def read_jsonl(p: Path) -> list:
    return [json.loads(l) for l in open(p, encoding="utf-8") if l.strip()]


def card_free(r) -> bool:
    return not str(r.get("card") or "").strip()


def is_twin(r) -> bool:
    return bool((r.get("meta") or {}).get("twin_of"))


def self_twin(r) -> bool:
    """A twin made by a mapper (not by negtwins): meta.twin_of / twin_kind / c2.twin_of or role 'twin'."""
    m = r.get("meta") or {}
    return bool(m.get("twin_of") or m.get("twin_kind") or (m.get("c2") or {}).get("twin_of") or r.get("role") == "twin")


def dom(r) -> str:
    d = r["meta"]["domain"]
    return DOMAIN_GROUP.get(d, d)


# ---- 1. load -------------------------------------------------------------------------------------------------------
def load_sources(only=None):
    srcs, problems = {}, []
    for d in sorted(PARTS.iterdir()):
        if not d.is_dir() or d.name.startswith("_") or "ohs" in d.name.lower() or (only and d.name not in only):
            continue
        if not (d / "rows.jsonl").is_file() or not (d / "MANIFEST.json").is_file():
            problems.append(f"{d.name}: no rows.jsonl + MANIFEST.json, skipped")
            continue
        rows = read_jsonl(d / "rows.jsonl")
        schema_before = dict(schema_problems(rows))
        rels = read_jsonl(d / "relations.jsonl") if (d / "relations.jsonl").is_file() else []
        man = json.loads((d / "MANIFEST.json").read_text())
        kept, all_rows, prefixed = [], [], 0
        for r in rows:
            m = r.setdefault("meta", {})
            if m.get("sampler") == "S5" or m.get("dev_only"):
                problems.append(f"{d.name}: dev row {r.get('id')} refused")
                continue
            m["family"] = "MD"
            r["source"] = r.get("source") or m.get("source") or d.name
            if not str(r["source"]).startswith("c2_"):
                # negtwins.block_twins md gives every twin the source "c2_<source>" and says the merged block already carries
                # c2_ sources; without the prefix the twins of the group-A / group-C sources would form 7 extra "sources".
                # Only this field changes (ids, text, gold, meta are untouched).
                r["source"] = "c2_" + str(r["source"])
                prefixed += 1
            m["source"] = r["source"]
            m["domain"] = m.get("domain") or r.get("domain") or man.get("domain") or "na"
            if r.get("card") and not m.get("card_id"):
                m["card_id"] = r.get("card_id") or f"{m.get('task_id')}:card"
            if not m.get("task_id"):
                problems.append(f"{d.name}: row {r.get('id')} has no meta.task_id")
                continue
            all_rows.append(r)
            if not self_twin(r):
                kept.append(r)
        srcs[d.name] = {"rows": kept, "all_rows": all_rows, "twins_removed": len(all_rows) - len(kept), "source_prefixed": prefixed, "schema_before": schema_before, "rels": rels, "man": man, "dir": d}
    return srcs, problems


# ---- 1b. schema (kit validate_row, meta.licence excepted) ------------------------------------------------------------------
def schema_problems(rows):
    """Counter of validate_row messages over rows, meta.licence excepted (real-text rows carry the upstream licence)."""
    from c2_kit import rows as K
    c = Counter()
    for r in rows:
        for m in K.validate_row(r):
            if m != "meta.licence":
                c[m] += 1
    return c


def c2_schema(r, idmap):
    """Make a mapper row pass the kit's validate_row (meta.licence excepted) without touching text, options or gold:
    id / group_id / call_id get the source prefix (group B already has it); missing meta keys get honest values
    (not tracked = None; derived = a hash of the task id)."""
    src = r["source"]
    bare = src[3:] if src.startswith("c2_") else src
    pre = src + ":"
    if not str(r["id"]).startswith(pre):
        new = pre + str(r["id"]).rsplit(":", 1)[-1]
        idmap[r["id"]] = new
        r["id"] = new
        for k in ("group_id", "call_id"):
            v = str(r.get(k) or "")
            if v and not v.startswith(pre):
                r[k] = (pre + "g:" if ":g:" in v else pre) + v.rsplit(":", 1)[-1]
    m = r["meta"]
    qform = m.get("qform") or str(m["task_id"]).split(":", 1)[-1]
    ds = m.get("dataset_url") or ""
    host = ds.split("/")[2] if ds.count("/") >= 2 else None
    defaults = {"spec_id": f"MD.{bare}.v1", "domain_pack": f"md.{bare}", "sampler": None, "git_sha": "uncommitted",
                "structure_hash": hashlib.sha256(str(m["task_id"]).encode()).hexdigest()[:16], "difficulty_bin": None, "crowd_pg": None,
                "depth": 0, "deep": False, "format_style": "record", "wording_id": None,
                "defs_style": "none" if card_free(r) else "rules_in_card", "twin_of": None, "twin_kind": None,
                "text_source": host, "edge": [], "qform": qform, "dev_only": False, "gen_version": None, "seed": SEED}
    for k, v in defaults.items():
        m.setdefault(k, v)
    c2 = m.setdefault("c2", {})
    for k, v in {"author_mode": "T", "skin_id": f"MD-{bare}-{qform}", "register": "metadata", "lexicon_ids": [], "haiku_task_id": None,
                 "haiku_prompt_sha": None, "twin_kind": m["twin_kind"], "twin_of": m["twin_of"], "closed_world": False}.items():
        c2.setdefault(k, v)
    return r


# ---- 2. noise gate -------------------------------------------------------------------------------------------------
def gate_source(name, s, min_conf=None, nontwin_only=True):
    """Returns (dropped task ids, report). Needs c2_kit.g5h.normalize_answer / read_item.
    The gate reads every picked row (twins included: they were drawn into the seeded 13 before they were removed from the
    block); the report also gives the variants (non-twin rows only; confidence >= 0.7) for the orchestrator."""
    from c2_kit import g5h
    min_conf = CLEAR_CONF if min_conf is None else min_conf
    ng = s["dir"] / "noise_gate"
    og = s["dir"] / "noise_gate_orch"
    rep = {"status": "pending", "answers": 0, "tasks_checked": 0, "dropped": {}}
    afiles = sorted((ng / "answers").glob("*.json")) if (ng / "answers").is_dir() else []
    keyf = sorted((ng / "key").glob("MD_*.json")) + (sorted((og / "key").glob("MD_*.json")) if (og / "key").is_dir() else [])
    if not afiles or not keyf:
        return set(), rep
    byid = {r["id"]: r for r in s.get("all_rows", s["rows"])}
    key, stale = {}, []
    for k in keyf:
        j = json.loads(k.read_text())
        if isinstance(j, dict) and isinstance(j.get("key"), dict):
            if all(v in byid for v in j["key"].values()):
                key.update(j["key"])
            else:
                stale.append(k.name)             # a key of an earlier mapper run: some row ids no longer exist
    ans = {}

    def walk(o):
        if isinstance(o, dict):
            for k, v in o.items():
                if k in key:
                    ans[k] = v if isinstance(v, dict) else {"answer": v}
                else:
                    walk(v)
        elif isinstance(o, list):
            for x in o:
                if isinstance(x, dict) and x.get("qid") in key:
                    ans[x["qid"]] = {k: y for k, y in x.items() if k != "qid"}
                else:
                    walk(x)
    for a in afiles:
        walk(json.loads(a.read_text()))
    conf = None
    cf = ng / "confirmed.json"
    if cf.is_file():
        conf = set(json.loads(cf.read_text()).get("confirmed_wrong", []))
    pickf = ng / "SEEDED_PICK.json" if (ng / "SEEDED_PICK.json").is_file() else og / "SEEDED_PICK.json"
    pick = json.loads(pickf.read_text()) if pickf.is_file() else {}
    wrong, per_task_n, invalid, unanswered = defaultdict(list), Counter(), 0, 0
    combos = {(c, t): defaultdict(int) for c in (0.0, 0.7) for t in (False, True)}   # variants: (min conf, twin rows counted)
    for qid, rid in key.items():
        r = byid.get(rid)
        if r is None:
            continue
        istw = self_twin(r)
        if nontwin_only and istw:
            continue
        if qid not in ans:
            unanswered += 1
            continue
        t = r["meta"]["task_id"]
        per_task_n[t] += 1
        a = ans[qid]
        norm = g5h.normalize_answer(g5h.read_item(r), a)
        if norm is None:
            invalid += 1
            continue
        c = a.get("confidence") if isinstance(a, dict) else None
        try:
            c = 1.0 if c is None else float(c)
        except (TypeError, ValueError):
            c = 1.0
        if norm != r["gold"]:
            if c >= min_conf and (conf is None or rid in conf):
                wrong[t].append(rid)
            for (mc, ct), dd in combos.items():
                if c >= mc and (ct or not istw):
                    dd[t] += 1
    drop = set()
    for t, n in per_task_n.items():
        if len(wrong.get(t, [])) >= NOISE_MIN_WRONG:
            drop.add(t)
            rep["dropped"][t] = {"wrong": len(wrong[t]), "read": n}
    expected = sum(len(v) for v in pick.values()) if pick else len(key)
    kept_tasks = {r["meta"]["task_id"] for r in s["rows"]}
    rep.update({"status": "complete" if len(ans) >= expected and not unanswered else "partial", "answers": len(ans), "expected": expected,
                "unanswered": unanswered, "invalid_answers": invalid, "stale_keys_ignored": stale,
                "tasks_checked": len(per_task_n), "tasks_in_block": len(kept_tasks), "tasks_unchecked": len(kept_tasks - set(per_task_n)),
                "rule": f"drop a task with >= {NOISE_MIN_WRONG} picked rows whose blind answer differs from gold (confidence >= {min_conf})" + ("; twin rows not counted" if nontwin_only else "; every picked row counts, mapper twins included"),
                "confirmation_file": conf is not None, "clearly_wrong_rows": sum(len(v) for v in wrong.values()),
                "twin_rows_among_picked": sum(1 for rid in key.values() if self_twin(byid[rid])),
                "variants_tasks_dropped": {f"conf>={mc}, twin picks {'counted' if ct else 'not counted'}": sum(1 for v in dd.values() if v >= NOISE_MIN_WRONG)
                                           for (mc, ct), dd in combos.items()},
                "per_task_wrong": {t: len(v) for t, v in sorted(wrong.items())}})
    return drop, rep


# ---- 3. caps ---------------------------------------------------------------------------------------------------------
def fit(rows, rels, steps):
    """Whole-task removal in seeded order until the caps hold. Returns rows, rels."""
    def tasks_of(rr):
        d = defaultdict(list)
        for r in rr:
            d[r["meta"]["task_id"]].append(r)
        return d

    def remove(rr, pred, need, tag):
        # a task that holds a pred row; removed in seeded order; never below 40 tasks in its source
        tk = tasks_of(rr)
        per_src = Counter(r["source"] for r in rr)
        ntasks = Counter()
        for t, v in tk.items():
            ntasks[v[0]["source"]] += 1
        cand = sorted((t for t, v in tk.items() if any(pred(x) for x in v)), key=lambda t: hx(SEED, "fit", tag, t))
        got, gone = 0, set()
        for t in cand:
            if got >= need:
                break
            s = tk[t][0]["source"]
            if ntasks[s] <= TASKS_PER_SOURCE[0]:
                continue
            ntasks[s] -= 1
            gone.add(t)
            got += sum(1 for x in tk[t] if pred(x))
        return [r for r in rr if r["meta"]["task_id"] not in gone], got
    for _ in range(300):
        n = len(rows)
        tw = sum(1 for r in rows if is_twin(r))
        act = None
        if tw > TWIN_MAX:
            act = ("twins", is_twin, tw - TWIN_MAX)
        elif n > N_MAX:
            act = ("size", lambda r: True, n - N_MAX)
        else:
            for lim, keyf, tg in ((DOM_MAX, dom, "domain"), (SRC_MAX, lambda r: r["source"], "source")):
                c = Counter(keyf(r) for r in rows)
                if c:
                    v, k = max(c.items(), key=lambda x: (x[1], str(x[0])))
                    if k > lim * n + 1e-9:
                        act = (f"{tg}:{v}", lambda r, v=v, keyf=keyf: keyf(r) == v, math.ceil((k - lim * n) / (1 - lim)))
                        break
        if act is None:
            break
        rows, got = remove(rows, act[1], act[2], act[0])
        steps.append({"rule": act[0], "need": act[2], "removed_rows_of_rule": got})
        if got == 0:
            steps[-1]["unfixable"] = True
            break
    ids = {r["id"] for r in rows}
    return rows, [x for x in rels if x["a"] in ids and x["b"] in ids]


# ---- 4. checks ---------------------------------------------------------------------------------------------------------
def problems_of(rows, rels, accepted=()):
    """accepted: sources whose task count fell under 40 in the gate and keep their tasks (A51 c): reported, not a problem."""
    p, rep = [], {}
    n = len(rows)
    rep["rows"] = n
    if len({r["id"] for r in rows}) != n:
        p.append("duplicate row ids")
    tw = sum(1 for r in rows if is_twin(r))
    rep["twins"] = tw
    if n < N_MIN:
        p.append(f"{n:,} rows < {N_MIN:,}")
    if n > N_MAX:
        p.append(f"{n:,} rows > {N_MAX:,}")
    if tw > TWIN_MAX:
        p.append(f"{tw:,} twins > {TWIN_MAX:,}")
    dc, src = Counter(dom(r) for r in rows), Counter(r["source"] for r in rows)
    rep.update({"domains": dict(dc), "domain_shares": {d: round(c / max(1, n), 4) for d, c in sorted(dc.items())},
                "source_shares": {s: round(c / max(1, n), 4) for s, c in sorted(src.items())},
                "domain_groups": DOMAIN_GROUP, "sources": dict(src), "n_domains": len(dc)})
    if len(dc) < DOM_MIN:
        p.append(f"{len(dc)} domains < {DOM_MIN}")
    for d, c in dc.items():
        if c > DOM_MAX * n + 1e-9:
            p.append(f"domain {d} holds {c / n:.3f} > {DOM_MAX}")
    for s, c in src.items():
        if c > SRC_MAX * n + 1e-9:
            p.append(f"source {s} holds {c / n:.3f} > {SRC_MAX}")
    tasks = defaultdict(list)
    for r in rows:
        tasks[r["meta"]["task_id"]].append(r)
    tps = Counter(v[0]["source"] for v in tasks.values())
    rep["tasks_per_source"] = dict(tps)
    for s, c in tps.items():
        if not TASKS_PER_SOURCE[0] <= c <= TASKS_PER_SOURCE[1] and s not in accepted:
            p.append(f"{s}: {c} tasks outside {TASKS_PER_SOURCE}")
    rep["task_floor_accepted_A51c"] = {s: tps[s] for s in accepted if s in tps}
    sch = schema_problems(rows)
    rep["schema_after"] = dict(sch)
    if sch:
        p.append(f"kit validate_row (meta.licence excepted): {dict(sch)}")
    big = {t: len(v) for t, v in tasks.items() if len(v) > TASK_ROWS_MAX}
    if big:
        p.append(f"{len(big)} tasks above {TASK_ROWS_MAX} rows")
    free = {s: sum(1 for r in rows if r["source"] == s and card_free(r)) / c for s, c in src.items()}
    rep["card_free"] = {s: round(v, 3) for s, v in free.items()}
    for s, v in free.items():
        if v < CARD_FREE_MIN - 1e-9:
            p.append(f"{s}: card-free share {v:.3f} < {CARD_FREE_MIN}")
    ids = {r["id"] for r in rows}
    if any(x["a"] not in ids or x["b"] not in ids for x in rels):
        p.append("a relation points outside the kept rows")
    yn = [r for r in rows if r["qtype"] == "noul"]
    rep["yes_share_yn"] = round(sum(r["gold"] for r in yn) / max(1, len(yn)), 4)
    for r in rows:
        if r["qtype"] == "choice" and r["gold"] not in (r["options"] or []):
            p.append(f"choice gold outside options: {r['id']}")
            break
    try:
        import c2io
        p += c2io.candidate_problems("MD", rows)
    except Exception as e:  # noqa: BLE001
        rep["c2io_candidate_problems"] = f"not run: {e}"
    try:
        import mix_c2
        r2, p2 = mix_c2.block_rules("MD", [dict(r, _block="MD") for r in rows], loaded=True)
        rep["mix_c2_block_rules"] = r2
        viol = {s for s, c in tps.items() if not TASKS_PER_SOURCE[0] <= c <= TASKS_PER_SOURCE[1]}
        p += [f"mix_c2.block_rules: {x}" for x in p2 if not ("tasks per source outside" in x and viol <= set(accepted))]
        if len(p2) != sum(1 for x in p2 if not ("tasks per source outside" in x and viol <= set(accepted))):
            rep["mix_c2_task_floor_note"] = "mix_c2.block_rules(loaded=True) flags the A51 (c) shortfall; accepted here, the mixer's rule (mix_c2.py ~line 934) still flags it"
    except Exception as e:  # noqa: BLE001
        rep["mix_c2_block_rules"] = f"not run: {type(e).__name__}: {str(e)[:120]}"
    return p, rep


# ---- main ----------------------------------------------------------------------------------------------------------------
PENDING = [
    "negation twins: `python -B -m negtwins.block_twins md cardtasks`, Haiku card-certificate reads, then `md --apply` (A42-D 7; twins <= 5,000, base + twins <= 12,000; G-TW 100%; Sonnet 3% audit of the twin rows, 7.3)",
    "caps re-check after the twins are applied: no source above 15%, no domain above 20% (openalex + ror counted as one scholarly domain), 8,000-12,000 rows, >= 30% card-free per source",
    "G13 decontamination on the candidates (A42-D 8.6; g13_c2.py, OHS-4 sealed-side checkers): drops are whole units",
    "C1 crowd selection for MD (c2_select.py select; mix_c2 reads crowd_c2/select_MD.json, target 12,000, short is allowed)",
    "second source-name check on the final mix (A42-D 8.5, sealed side)",
]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("--allow-pending-gate", action="store_true")
    ap.add_argument("--min-conf", type=float, default=CLEAR_CONF, help="a disagreement counts as clearly wrong at this confidence or higher (A51 a: 0.7)")
    ap.add_argument("--gate-count-twins", action="store_true", help="also count the picked rows that are mapper twins (A51 b says they do not count)")
    ap.add_argument("--sources", nargs="*")
    a = ap.parse_args()
    srcs, probs = load_sources(set(a.sources) if a.sources else None)
    report = {"seed": SEED, "min_conf": a.min_conf, "gate_nontwin_only": not a.gate_count_twins, "sources": {}, "load_problems": probs, "cap_steps": []}
    rows, rels, dropped, pending, owner = [], [], {}, [], {}
    for name, s in srcs.items():
        drop, g = gate_source(name, s, a.min_conf, not a.gate_count_twins)
        if g["status"] != "complete":
            pending.append(name)
        kept_rows = [r for r in s["rows"] if r["meta"]["task_id"] not in drop]
        tasks_in = len({r["meta"]["task_id"] for r in s["rows"]})
        owner.update({r["meta"]["task_id"]: name for r in s["rows"]})
        report["sources"][name] = {"rows_in_file": len(s["all_rows"]), "self_made_twins_removed": s["twins_removed"], "rows_in": len(s["rows"]),
                                   "source_prefixed_rows": s["source_prefixed"], "schema_before": s["schema_before"], "block_source": next((r["source"] for r in s["rows"]), None),
                                   "tasks_in": tasks_in, "tasks_read_by_gate": g.get("tasks_checked", 0), "tasks_dropped_by_gate": len(drop),
                                   "rows_dropped_by_gate": len(s["rows"]) - len(kept_rows), "rows_after_gate": len(kept_rows),
                                   "tasks_after_gate": tasks_in - len(drop), "gate": g, "licence": s["man"].get("licence")}
        dropped.update({t: {"source": name, **v} for t, v in g["dropped"].items()})
        rows += kept_rows
        rels += s["rels"]
    if pending and not a.allow_pending_gate:
        print(json.dumps({"refused": "noise gate not complete", "pending_or_partial": pending}, indent=1))
        sys.exit(2)
    idmap = {}
    for r in rows:
        c2_schema(r, idmap)                            # ids get the source prefix after the gate (the gate keys name the original ids)
    rels = [dict(x, a=idmap.get(x["a"], x["a"]), b=idmap.get(x["b"], x["b"])) for x in rels]
    from c2_kit import rows as K
    bad = defaultdict(set)
    for r in rows:
        for m in K.validate_row(r):
            if m != "meta.licence":
                bad[r["meta"]["task_id"]].add(m)
    if bad:                                            # a task whose rows cannot pass the schema is dropped whole (rows are never edited)
        for t, ms in bad.items():
            dropped[t] = {"source": next(r["source"] for r in rows if r["meta"]["task_id"] == t), "reason": "schema: " + "; ".join(sorted(ms)),
                          "rows": sum(1 for r in rows if r["meta"]["task_id"] == t)}
        rows = [r for r in rows if r["meta"]["task_id"] not in bad]
    report["schema_dropped_tasks"] = {t: dropped[t] for t in bad}
    ids = {r["id"] for r in rows}
    rels = [x for x in rels if x["a"] in ids and x["b"] in ids]
    report["after_gate"] = {"rows": len(rows), "dropped_tasks": len(dropped)}
    rows, rels = fit(rows, rels, report["cap_steps"])
    kept_by_src, tasks_by_src = Counter(owner[r["meta"]["task_id"]] for r in rows), defaultdict(set)
    for r in rows:
        tasks_by_src[owner[r["meta"]["task_id"]]].add(r["meta"]["task_id"])
    for n, v in report["sources"].items():
        v["rows_kept_final"], v["tasks_kept_final"] = kept_by_src.get(n, 0), len(tasks_by_src.get(n, ()))
    accepted = sorted({r["source"] for n, v in report["sources"].items() if v["tasks_dropped_by_gate"] and v["tasks_kept_final"] < TASKS_PER_SOURCE[0]
                       for r in srcs[n]["rows"][:1]})
    report["deviations"] = [{"ruling": "A51 (c)", "source": srcs_name, "block_source": v["block_source"], "tasks_in": v["tasks_in"], "tasks_dropped_by_gate": v["tasks_dropped_by_gate"],
                             "tasks_kept": v["tasks_kept_final"], "rows_kept": v["rows_kept_final"], "floor": TASKS_PER_SOURCE[0],
                             "note": "keeps its surviving tasks; the shortfall lowers the block total and is not refilled; reported in the training-GO request"}
                            for srcs_name, v in report["sources"].items() if v["tasks_dropped_by_gate"] and v["tasks_kept_final"] < TASKS_PER_SOURCE[0]]
    report["schema"] = {"before": {n: v["schema_before"] for n, v in report["sources"].items()}, "ids_rewritten": len(idmap),
                        "note": "meta.licence excepted; text, options and gold untouched"}
    probs2, rep = problems_of(rows, rels, accepted)
    report["check"] = rep
    report["problems"] = probs2
    report["gate_pending"] = pending
    report["gates_pending"] = PENDING
    qc_pass = False                                   # twins, G13 and the crowd selection are still to run (PENDING)
    report["qc_pass"] = qc_pass
    print(json.dumps({"rows": len(rows), "problems": probs2, "deviations": report["deviations"], "schema_dropped_tasks": report["schema_dropped_tasks"], "pending_gate": pending, "dropped_tasks": len(dropped),
                      "cap_steps": report["cap_steps"], "n_domains": rep["n_domains"], "domain_shares": rep["domain_shares"],
                      "source_shares": rep["source_shares"], "card_free": rep["card_free"], "tasks_per_source": rep["tasks_per_source"],
                      "per_source": {n: {k: v[k] for k in ("rows_in_file", "self_made_twins_removed", "tasks_in", "tasks_read_by_gate", "tasks_dropped_by_gate",
                                                           "rows_after_gate", "rows_kept_final", "tasks_kept_final")} for n, v in report["sources"].items()}},
                     indent=1)[:6000])
    if a.dry_run:
        return
    import c2io
    out = c2io.C2_PARTS / "MD" / "out"
    qc = c2io.C2_PARTS / "MD" / "qc"
    rows.sort(key=lambda r: (r["source"], r["meta"]["task_id"], r["id"]))
    cand, rel = out / c2io.CAND, out / c2io.REL
    h1 = c2io.write_jsonl(cand, rows)
    h2 = c2io.write_jsonl(rel, rels)
    sha = lambda p: hashlib.sha256(Path(p).read_bytes()).hexdigest()
    man = {"family": "MD", "block": "metadata (A42-D 8)", "generator": "meta_src/merge_md.py", "seed": SEED,
           "parents": [{"source": n, "rows_in": v["rows_in"], "licence": (v["licence"] or {}).get("name") if isinstance(v["licence"], dict) else v["licence"]}
                       for n, v in report["sources"].items()],
           "files": {c2io.CAND: {"sha256": sha(cand), "rows": len(rows)}, c2io.REL: {"sha256": sha(rel), "rows": len(rels)}}}
    got = {c2io.CAND: (sha(cand), len(rows)), c2io.REL: (sha(rel), len(rels))}
    assert not c2io.manifest_problems("MD", man, got)
    c2io.write_json(out / c2io.MAN, man)
    c2io.write_json(qc / "MD_MERGE_REPORT.json", report)
    c2io.write_json(qc / "dropped_tasks.json", dropped)
    c2io.write_json(qc / c2io.QC, {
        "pass": qc_pass, "stage": "merged base block (no negation twins yet); not admitted until the pending gates below run", "family": "MD",
        "fix_iterations": 0, "passed_utc": None,
        "note": "pass is false on purpose: the negation twins (negtwins.block_twins md), G13 and the crowd selection have not run. The gates in 'gates_run' did run; none is waived.",
        "gates_run": {
            "A42D_8_4_noise_gate": {
                "rule": report["sources"][next(iter(report["sources"]))]["gate"]["rule"],
                "per_source": {n: {k: v[k] for k in ("tasks_in", "tasks_read_by_gate", "tasks_dropped_by_gate", "rows_after_gate")} for n, v in report["sources"].items()},
                "tasks_dropped_total": len(dropped), "record": "qc/dropped_tasks.json; qc/MD_MERGE_REPORT.json"},
            "A42D_8_2_caps": {"source_max": SRC_MAX, "domain_max": DOM_MAX, "domain_groups": DOMAIN_GROUP, "cap_steps": report["cap_steps"],
                              "block_rows": len(rows), "source_shares": rep["source_shares"], "domain_shares": rep["domain_shares"],
                              "n_domains": rep["n_domains"], "card_free": rep["card_free"], "tasks_per_source": rep["tasks_per_source"]},
            "self_made_twins_removed": {n: v["self_made_twins_removed"] for n, v in report["sources"].items()},
            "A42D_8_3_licence_and_name_checks_recorded_by_the_mappers": {
                "licence": {n: v["licence"] for n, v in report["sources"].items()},
                "name_check": "source_name_check.py: PASS for all 11 on the OHS-4 export and the OHS-AC preliminary file (meta_src/name_check_ohs4_result.txt; GROUP_A_SUMMARY._name_check; GROUP_B_SUMMARY._note); c1_denylist_check.py clear (NOTES.md)",
                "meta.licence": "kept on the rows: real-text rows carry the upstream licence (as for GB)"},
            "schema": {"kit validate_row (meta.licence excepted)": {"before_by_source": report["schema"]["before"], "after": rep.get("schema_after"),
                                                                    "ids_rewritten": len(idmap), "note": "id / group_id / call_id source prefix; missing meta keys filled with honest values; text, options and gold untouched"},
                       "c2io.candidate_problems + mix_c2.block_rules": "see MD_MERGE_REPORT.check"}},
        "deviations": report["deviations"],
        "problems": probs2, "gates_pending": PENDING,
        "files": {c2io.CAND: {"sha256": sha(cand), "rows": len(rows)}, c2io.REL: {"sha256": sha(rel), "rows": len(rels)}}})
    print("written", out, qc)


if __name__ == "__main__":
    main()
