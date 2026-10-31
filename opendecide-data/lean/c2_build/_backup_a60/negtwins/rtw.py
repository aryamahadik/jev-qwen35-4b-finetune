"""negtwins/rtw.py: the replay yes/no twin block RTW (A42-D 7.1 / 7.2), built from the FROZEN trained catalogue only.

Bases: replay yes/no rows (qtype noul) that A46 marked agreed (replay_screen/reads/SCORE.json 'agreed': both blind reads equal
the human gold) and that are in neither REPLAY_DENY_A46.json nor REPLAY_UNSCREENED_A46.json, whose core parses (both parsers),
whose card is a swap-safe two-line card or a yes-only card, and whose source is NOT a T37b registry source (T37b is being
rebuilt on those sources and a unit is at most base + 1 complement + 1 equiv twin). A complement twin on a two-line card needs
the base type's card certificate (2 Haiku reads 'opposite'): cardcert_replay_r1/r2. Without the answers the block holds equiv
twins only and its QC record says pass = false.

Commands (from c2_build):
    python -B -m negtwins.rtw cardtasks          # write the replay card-certificate tasks (Haiku, 2 rounds)
    python -B -m negtwins.rtw build [--target N] [--exclude-t37b-sources] [--exclude-ids FILE] [--preview]
                                    [--strict-pattern-cap | --greedy] [--step N] [--floor N]
        plan -> twins -> program checks (check_pair, polarity A/B, A43 f / A48 h) -> G-TW -> lean/data/c2_parts/RTW/.
        Gold: complement = 1 - base gold, equiv = base gold, never edited. The ONE Sonnet 3% audit is pooled over GB + MD + RTW
        (`python -B -m negtwins.pooled_audit`), so build writes no RTW-only audit tasks.
        Caps (shares of the REALISED block): source <= 10% (spec 3.18), (pattern, core) cell <= 2%, pattern <= 1.2%. The pattern
        cap is measured on the POOLED twin set (GB + MD + RTW, DESIGN section 5: the spec 3.18 shares are pooled) and the
        planner is `plan.plan_flow` (the largest block the caps allow, by max-flow: complement twins first, then equiv twins;
        the yes share is brought into 45-55% by removal). `--greedy` is plan_fit (a scan over greedy plans, about 40% below the
        flow bound); `--strict-pattern-cap` is the old per-block rule (plan_block trim): with 12 of 24 base types certified it
        collapses to about 33 rows (infeasible: the max-flow bound is about 64 rows).
"""
from __future__ import annotations

import datetime
import gzip
import json
import shutil
import sys
from collections import Counter
from pathlib import Path

from c2_kit import chunker, rows as R
from t37b import sources as SRC

from . import checks as K
from . import core as C
from . import frozen as FZ
from . import plan as P
from . import stage2_admit as A
from . import tasks as T

CB = Path(__file__).resolve().parents[1]
DATA = CB.parent / "data"
GOLDEN = DATA / "v14_parts" / "golden_train.jsonl"        # the pool replay_screen/draw.py drew from (rows with call_id and meta)
SCREEN = CB / "replay_screen"
OUT = DATA / "c2_parts" / "RTW"
HAIKU = T.HERE / "haiku"
TARGET = 9000                       # RTW + the rebuilt T37b (about 1,000) <= 10,000 (A42-D 7.1)
GEN = "rtw1"
BLOCK = "replay"                    # plan.CAPS key (10,000)
SOURCE = "c2_rtw"
T37B_SOURCES = frozenset(e.source for e in SRC.ENTRIES)
POOL_BLOCKS = ("GB", "MD")           # the other blocks whose twins make up the pooled twin set (their out/candidates_c2.jsonl)
KIND_SHARE_PROBLEMS = ("implicit share", "antonym share", "syntactic share")      # pooled over GB + MD + RTW, not per block


# ------------------------------------------------------------------------------------------------ pooled context

def pooled_context(blocks: tuple = POOL_BLOCKS) -> dict:
    """Twin rows already in the other blocks' out/candidates_c2.jsonl: {"counts": {pattern id: rows}, "total": rows, "kinds":
    {complement kind: rows}, "by_block": {block: rows}} (the pooled twin set the pattern cap and the spec 3.18 shares are on)."""
    counts, kinds, by_block = Counter(), Counter(), {}
    for b in blocks:
        f = DATA / "c2_parts" / b / "out" / "candidates_c2.jsonl"
        n = 0
        if f.exists():
            with f.open(encoding="utf-8") as fh:
                for line in fh:
                    if '"negtwin"' not in line:
                        continue
                    ng = (json.loads(line).get("meta") or {}).get("negtwin")
                    if ng:
                        counts[ng["pattern"]] += 1
                        n += 1
                        if ng["kind"] in ("syntactic", "implicit", "antonym"):
                            kinds[ng["kind"]] += 1
        by_block[b] = n
    return {"counts": counts, "total": sum(counts.values()), "kinds": dict(kinds), "by_block": by_block}


def pooled_shares(rows: list, pooled: dict) -> dict:
    """Spec 3.18 shares of the pooled COMPLEMENT twins (the other blocks + these rows) and the problems against the floors."""
    k = Counter(pooled.get("kinds") or {})
    for r in rows:
        n = r["meta"]["negtwin"]
        if r["role"] == "complement":
            k[n["kind"]] += 1
    rep = P.pooled_report([{"kinds": {x: k.get(x, 0) for x in ("syntactic", "implicit", "antonym")}}])
    rep["by_kind"] = {x: k.get(x, 0) for x in ("syntactic", "implicit", "antonym")}
    return rep


# ------------------------------------------------------------------------------------------------ bases

def t37b_base_ids(extra: str | None = None) -> set:
    """Base ids T37b already uses (its relation edges 'a'), so a unit never holds T37b and RTW twins of one base. T37b is being
    rebuilt: when its relations file is not on disk yet the set is empty and the build records the overlap check as deferred."""
    ids = set()
    for f in [DATA / "c2_parts" / "T37b" / "out" / "candidates_c2.relations.jsonl"] + ([Path(extra)] if extra else []):
        if f.exists():
            if f.suffix == ".json":
                ids |= set(json.loads(f.read_text()).get("drop_ids") or json.loads(f.read_text()).get("ids") or [])
            else:
                ids |= {json.loads(l)["a"] for l in f.open(encoding="utf-8") if l.strip()}
    return ids


def load_bases(include_t37b_sources: bool = True, exclude_ids: set = frozenset()) -> tuple:
    ag = set(json.loads((SCREEN / "reads" / "SCORE.json").read_text())["agreed"])
    deny = set(json.loads((SCREEN / "REPLAY_DENY_A46.json").read_text())["drop_ids"])
    unscreened = set(json.loads((SCREEN / "REPLAY_UNSCREENED_A46.json").read_text())["drop_ids"])
    want = set()
    with gzip.open(SCREEN / "pool" / "population.jsonl.gz", "rt", encoding="utf-8") as fh:
        for line in fh:
            r = json.loads(line)
            if r["qtype"] == "noul" and r["id"] in ag and r["id"] not in deny and r["id"] not in unscreened \
                    and r.get("soft") != "True" and r.get("attacked") != "True":
                want.add(r["id"])
    bases, rep = [], Counter()
    with GOLDEN.open(encoding="utf-8") as fh:
        for line in fh:
            if '"qtype": "noul"' not in line:
                continue
            rid = line[8:line.index('"', 8)]
            if rid not in want:
                continue
            if rid in exclude_ids:
                rep["excluded: base already used by T37b"] += 1
                continue
            r = json.loads(line)
            rep["agreed_yesno_rows"] += 1
            try:
                r["gold"] = int(r["gold"])
            except (TypeError, ValueError):
                rep["gold_not_01"] += 1
                continue
            r["options"] = None
            r["meta"] = r.get("meta") or {}
            b = P.base_record(r, "replay")
            if b is None:
                rep["not_a_base (core / card / meta)"] += 1
            elif r["source"] in T37B_SOURCES and not include_t37b_sources:
                rep["excluded: T37b registry source"] += 1
            else:
                bases.append(b)
    rep["bases"] = len(bases)
    rep["by_source"] = dict(Counter(b["row"]["source"] for b in bases))
    rep["types"] = len({b["type"] for b in bases})
    return bases, dict(rep)


# ------------------------------------------------------------------------------------------------ card certificates (replay types)

def base_types(bases: list) -> dict:
    """{type: (yes definition, no definition)} for the two-line-card base types (yes-only cards use the wrap, no certificate)."""
    out = {}
    for b in bases:
        if not b["one_sided"]:
            out.setdefault(b["type"], (b["defs"][0], b["defs"][1]))
    return out


def _card_batch(types: dict, r: int):
    return T._batch("polarity", T.card_items(types), f"negtw-cardcert-replay-r{r}-{GEN}", T.CARD_PROMPT)


def write_card_tasks(bases: list) -> dict:
    types = base_types(bases)
    out = {}
    for r in (1, 2):
        b = _card_batch(types, r)
        root = HAIKU / f"cardcert_replay_r{r}"
        if (root / "TASKS.json").exists() and json.loads((root / "TASKS.json").read_text())["batch_id"] != b.batch_id:
            _supersede(root)
        out[r] = T._write(root, b, "Haiku card-complement read (replay base types)", T.POL_FORMAT, "polarity:negtw_cardcert_replay",
                          extra={"n_types": len(types)})
    return out


def certified(bases: list):
    """Set of base types whose card passed 2/2, or None when the answers are not there yet."""
    types = base_types(bases)
    reads = []
    for r in (1, 2):
        b = _card_batch(types, r)
        root = HAIKU / f"cardcert_replay_r{r}"
        files = sorted((root / "answers").glob("*.json")) if (root / "answers").exists() else []
        if not files or not (root / "TASKS.json").exists():
            return None
        if json.loads((root / "TASKS.json").read_text())["batch_id"] != b.batch_id:
            raise RuntimeError(f"{root.name}: the task files do not match the current base types; rewrite them (cardtasks)")
        raw = {p.stem: json.loads(p.read_text(encoding="utf-8")) for p in files}
        ans, probs = chunker.load_answers(b, raw)
        if probs:
            raise RuntimeError(f"{root.name}: {probs[:3]}")
        reads.append(T.relations(ans))
    dec = T.card_decide(reads[0], reads[1])
    return {k for k, v in dec.items() if v}


def _supersede(root: Path) -> None:
    dst = HAIKU / "_superseded_rtw"
    dst.mkdir(exist_ok=True)
    n = len(list(dst.glob(root.name + "*")))
    shutil.move(str(root), str(dst / f"{root.name}_{n}"))


# ------------------------------------------------------------------------------------------------ rows

def c2_row(twin: dict, base: dict, p: C.Pattern, seed: int = 20261013, *, source: str = SOURCE, family: str = "RTW") -> dict:
    """The K.twin_row output in the C2 candidate schema (the T37b partner_row layout)."""
    bm = base.get("meta") or {}
    rel = twin["role"]
    tid = source + ":" + C.sha(base["id"] + "|" + p.pid + "|" + twin["instructions"])[:16]
    neg = dict(twin["meta"]["negtwin"])
    neg["block"] = family
    meta = {"family": family, "spec_id": "A42-D.7+A48(h)", "card_id": (base.get("meta") or {}).get("card_id") or f"{family}:{base['source']}", "domain_pack": None,
            "sampler": family, "gen_version": R.GEN_VERSION, "git_sha": "uncommitted", "seed": seed,
            "structure_hash": C.sha(base["id"] + "|" + p.pid)[:16], "difficulty_bin": None, "crowd_pg": None, "depth": 0,
            "deep": False, "format_style": f"replay/{base['source']}", "wording_id": p.pid, "defs_style": "swap" if rel == "complement" else "same",
            "twin_of": base["id"], "twin_kind": rel, "text_source": base["source"],
            "licence": f"{bm.get('licence') or 'the base row licence'} (text and definitions of {base['source']}); "
                       f"question wording: {R.LICENCE}",
            "edge": [], "qform": p.op, "dev_only": False,
            "c2": {"author_mode": "T", "skin_id": None, "register": "replay", "lexicon_ids": [], "haiku_task_id": None,
                   "haiku_prompt_sha": None, "twin_kind": rel, "twin_of": base["id"], "closed_world": False},
            "negtwin": neg}
    return {"id": tid, "group_id": base["group_id"], "call_id": base.get("call_id") or base["id"], "source": source, "state": base["state"],
            "qtype": "noul", "instructions": twin["instructions"], "options": None, "gold": twin["gold"], "role": rel,
            "card": twin["card"], "meta": meta}


def validate(row: dict, base: dict) -> list:
    probs = [x for x in R.validate_row(row, training=True) if x != "meta.licence"]
    m = row["meta"]
    if not str(m.get("licence", "")).endswith(f"question wording: {R.LICENCE}"):
        probs.append("licence must name the base licence and the question-wording licence")
    for k in ("state", "group_id", "call_id"):
        if row.get(k) != base.get(k):
            probs.append(f"{k} differs from the base row")
    want = 1 - base["gold"] if row["role"] == "complement" else base["gold"]
    if row["gold"] != want:
        probs.append("gold is not 1 - base gold (complement) / base gold (equiv)")
    return probs


def twin_checks(base_core: str, twin_core: str, p: C.Pattern, pairs: dict) -> list:
    """Program checks of one planned twin: checker, polarity A and B, A43 (f) and A48 (h) (same functions as stage 2)."""
    pr = pairs.get(p.pair) if p.pair else None
    ok, probs, _rep = K.check_pair(base_core, twin_core, p, pr)
    out = [f"K: {x}" for x in probs] if not ok else []
    if C.MODAL_SPLIT.search(twin_core) and not C.MODAL_SPLIT.search(base_core):
        out.append("A48h (ii) modal scope")
    if C.a48h_class(p):
        out.append("A48h (i) pattern")
    if K.bad_edit_site(base_core, twin_core):
        out.append("A48h (iv) edit site: inserted word right after a function word or 'being' (pooled audit, 16 Oct)")
    out += (A.pol_a(base_core, twin_core, p) + A.pol_b(base_core, twin_core, p)) if p.op in A.DECLARED_LAYERS \
        else A.pair_pol(base_core, twin_core, p, pr)
    return out


def report_of(rows: list, pats: dict) -> dict:
    kinds = Counter()
    for r in rows:
        n = r["meta"]["negtwin"]
        kinds[n["kind"] if r["role"] == "complement" else "equiv"] += 1
    nc = max(1, sum(v for k, v in kinds.items() if k != "equiv"))
    g = Counter((r["role"], r["gold"]) for r in rows)
    return {"rows": len(rows), "by_role": dict(Counter(r["role"] for r in rows)), "by_kind": dict(kinds),
            "by_op": dict(Counter(r["meta"]["negtwin"]["op"] for r in rows)),
            "by_predicate_class": dict(Counter(r["meta"]["negtwin"]["cls"] for r in rows)),
            "by_text_source": dict(Counter(r["meta"]["text_source"] for r in rows)),
            "gold": {"yes": sum(v for (rl, gd), v in g.items() if gd == 1), "no": sum(v for (rl, gd), v in g.items() if gd == 0),
                     "yes_share": round(sum(v for (rl, gd), v in g.items() if gd == 1) / max(1, len(rows)), 4),
                     "complement_yes": g[("complement", 1)], "complement_no": g[("complement", 0)],
                     "equiv_yes": g[("equiv", 1)], "equiv_no": g[("equiv", 0)]},
            "shares_of_complement": {k: round(kinds[k] / nc, 4) for k in ("syntactic", "implicit", "antonym")},
            "patterns_used": len({r["meta"]["negtwin"]["pattern"] for r in rows}),
            "max_pattern_share": round(max(Counter(r["meta"]["negtwin"]["pattern"] for r in rows).values(), default=0) / max(1, len(rows)), 4)}


def build(target: int = TARGET, include_t37b_sources: bool = True, exclude_file: str | None = None, preview: bool = False,
          strict: bool = False, greedy: bool = False, step: int = 1000, floor: int = 1000,
          exclude_patterns: frozenset = frozenset(), pooled_override: dict | None = None, write: bool = True) -> dict:
    """exclude_patterns: pattern ids the pooled audit dropped (the block is planned from the surviving catalogue);
    pooled_override: the other blocks' twin context when their files are not on disk yet (audit dry run); write=False: report only."""
    pats, pairs = FZ.load_trained()                     # verifies the frozen sha256 and the held-out guard
    pats = [p for p in pats if p.pid not in exclude_patterns]
    t37b_ids = t37b_base_ids(exclude_file)
    bases, brep = load_bases(include_t37b_sources, t37b_ids)
    brep["t37b_base_ids_known"] = len(t37b_ids)
    cert = certified(bases)
    if cert is None and not preview:
        raise SystemExit("RTW: the card certificates of the replay base types are not read yet (no complement twin on a two-line "
                         "card is allowed without them). Run Haiku on haiku/cardcert_replay_r1 and _r2, then rerun this command. "
                         "`--preview` shows what the block would be if every type passed (writes only negtwins/stage3/).")
    if preview:
        cert = {b["type"] for b in bases if not b["one_sided"]}
    pooled = None if strict else (pooled_override or pooled_context())
    twin_ok = lambda c, t, p: not twin_checks(c, t, p, pairs)           # noqa: E731
    byp = {p.pid: p for p in pats}
    # A block planned exactly at its caps collapses when rows leave it afterwards (every removal tightens every share). The schema check
    # (row length > 2000 tokens) needs the whole row, so it cannot sit in twin_ok; instead a base whose twin fails the schema is left out
    # and the block is planned again from the remaining bases (removal only; nothing is edited), until a plan passes whole.
    sch_excl: set = set()
    for _round in range(8):
        bases_use = [b for b in bases if b["row"]["id"] not in sch_excl]
        if strict:
            plan, prep = P.plan_block(bases_use, pats, pairs, block=BLOCK, n_target=target, certified=cert if cert is not None else set(),
                                      seed="negtw-plan-rtw-v1", source_cap=0.10, type_cap=None, trim=True)
        elif greedy:
            plan, prep = P.plan_fit(bases_use, pats, pairs, block=BLOCK, n_target=target, certified=cert if cert is not None else set(),
                                    seed="negtw-plan-rtw-v1", source_cap=0.10, type_cap=None, pooled=pooled, step=step, floor=floor,
                                    min_complement_share=0.0, twin_ok=twin_ok)
        else:
            plan, prep = P.plan_flow(bases_use, pats, pairs, block=BLOCK, n_target=target, certified=cert if cert is not None else set(),
                                     seed="negtw-plan-rtw-v1", source_cap=0.10, pooled=pooled, twin_ok=twin_ok)
        rows, base_rows, dropped, kept = [], {}, Counter(), []
        bad_bases: set = set()
        for b, p, t in plan:
            bad = twin_checks(b["core"], t, p, pairs)
            if bad:
                dropped["program check"] += 1
                bad_bases.add(b["row"]["id"])
                continue
            tw = K.twin_row(b["row"], b["pre"], t, p, block="rtw")
            r = c2_row(tw, b["row"], p)
            v = validate(r, b["row"])
            if v:
                dropped["schema: " + v[0]] += 1
                bad_bases.add(b["row"]["id"])
                continue
            rows.append(r)
            kept.append((b, p, t))
            base_rows[r["id"]] = b["row"]
        if not bad_bases or not plan:
            break
        sch_excl |= bad_bases
    prep["schema_excluded_bases"] = len(sch_excl)
    prep["replan_rounds"] = _round + 1
    if len(kept) < len(plan):          # rows left the plan after its caps were set: restore the caps on what is left (removal only)
        kept2, removed2 = P.enforce_caps(kept, source_cap=0.10, type_cap=None, seed="negtw-plan-rtw-v1", pooled=pooled, equiv_first=True)
        keep_ix = {id(x) for x in kept2}
        dropped["caps re-enforced after the schema check"] = sum(removed2.values())
        rows = [r for x, r in zip(kept, rows) if id(x) in keep_ix]
        base_rows = {r["id"]: base_rows[r["id"]] for r in rows}
    pairs_gtw = [(base_rows[r["id"]], {**r, "meta": {**r["meta"]}}) for r in rows]
    gtw = K.g_tw(pairs_gtw)
    rows.sort(key=lambda r: r["id"])
    rel = [{"a": r["meta"]["twin_of"], "b": r["id"], "type": r["role"]} for r in rows]
    rep = report_of(rows, byp)
    rep_src = round(max(Counter(r["meta"]["text_source"] for r in rows).values(), default=0) / max(1, len(rows)), 4)
    allprobs = P.share_problems({**prep, "shares_of_complement": rep["shares_of_complement"], "realised": len(rows),
                                 "twin_yes_share": rep["gold"]["yes_share"]})
    probs = [x for x in allprobs if not x.startswith(KIND_SHARE_PROBLEMS)]            # per-block problems (caps, yes band)
    pool_rep = pooled_shares(rows, pooled or pooled_override or pooled_context())      # spec 3.18 kind shares: pooled
    if preview:
        smp = T.audit_sample(rows)
        full = {"preview": True, "audit_expected": {"items": len(smp), "tasks": -(-len(smp) // 50), "patterns": len({r["meta"]["negtwin"]["pattern"] for r in smp})}, "note": "every two-line base type assumed certified; nothing written under data/, no audit tasks",
                "bases": brep, "plan": prep, "report": rep, "dropped": dict(dropped), "share_problems": allprobs,
                "g_tw": {k: gtw[k] for k in ("n_pairs", "violations", "pass")}}
        (T.HERE / "stage3").mkdir(exist_ok=True)
        (T.HERE / "stage3" / "RTW_PREVIEW_REPORT.json").write_text(json.dumps(full, indent=1, ensure_ascii=False) + "\n", encoding="utf-8")
        return full
    ncap = len(rows)
    if not write:
        return {"bases": brep, "plan": {k: v for k, v in prep.items() if k != "scan"}, "report": rep, "dropped": dict(dropped), "share_problems": allprobs,
                "g_tw": {k: gtw[k] for k in ("n_pairs", "violations", "pass")}, "pooled_spec_3_18_shares": pool_rep, "written": False}
    caps = {"max_source_share": rep_src, "source_cap_ok": rep_src <= 0.10 + 1e-9, "rows_le_cap": len(rows) <= P.CAPS[BLOCK], "rows_le_target": len(rows) <= target,
            "t37b_plus_rtw_le_10000_if_t37b_le": 10000 - len(rows),
            "max_cell": prep.get("max_cell"), "cell_cap_ok": prep.get("max_cell", 0) <= max(1, int(P.CELL_CAP * max(1, ncap))),
            "pattern_cap": prep.get("caps") or {"rule": "per-block 1.2% (strict)"}}
    OUT.joinpath("out").mkdir(parents=True, exist_ok=True)
    OUT.joinpath("qc").mkdir(parents=True, exist_ok=True)
    cand = "\n".join(json.dumps(r, ensure_ascii=False) for r in rows) + "\n"
    relt = "\n".join(json.dumps(x) for x in rel) + "\n"
    (OUT / "out" / "candidates_c2.jsonl").write_text(cand, encoding="utf-8")
    (OUT / "out" / "candidates_c2.relations.jsonl").write_text(relt, encoding="utf-8")
    files = {"candidates_c2.jsonl": {"sha256": C.sha(cand), "rows": len(rows)},
             "candidates_c2.relations.jsonl": {"sha256": C.sha(relt), "rows": len(rel)}}
    parents = sorted({r["meta"]["text_source"] for r in rows})
    frozen_rec = json.loads(FZ.FREEZE_FILE.read_text())
    man = {"family": "RTW", "parents": parents, "parents_note": "replay yes/no bases (A46 agreed); text and definitions are the base rows'",
           "generator": "negtwins.rtw " + GEN, "stage": "final" if cert is not None else "PROVISIONAL (equiv twins only: card certificates pending)",
           "trained_catalogue_sha256": frozen_rec["trained_catalogue_sha256"], "files": files}
    (OUT / "out" / "MANIFEST.json").write_text(json.dumps(man, indent=1) + "\n", encoding="utf-8")
    block_ok = bool(gtw["pass"] and not dropped.get("schema", 0) and cert is not None and not probs and caps["source_cap_ok"] and caps["cell_cap_ok"])
    reasons = ([] if cert is not None else ["card certificates for the replay base types are not read yet: "
                                            "no complement twin on a two-line card is allowed"]) + probs
    reasons.append("the pooled Sonnet 3% twin audit (GB + MD + RTW) is not applied yet (`python -B -m negtwins.pooled_audit apply`)")
    if pool_rep["problems"]:
        reasons.append("pooled spec 3.18 shares over GB + MD + RTW: " + "; ".join(pool_rep["problems"]) +
                       " (RTW cannot carry them alone; orchestrator ruling needed; no bar changed)")
    qc = {"pass": False, "passed_utc": None, "stage": "final" if cert is not None else "provisional", "family": "RTW", "fix_iterations": 0,
          "files": files, "block_gates_ok": block_ok, "reasons_not_passed": reasons,
          "gates": {"G-TW": {"pairs": gtw["n_pairs"], "violations": gtw["violations"], "pass": gtw["pass"]},
                    "program_checks_dropped": dict(dropped), "caps": caps,
                    "planner": {"tool": ("negtwins.plan.plan_block(trim)" if strict else "negtwins.plan.plan_fit" if greedy else "negtwins.plan.plan_flow"), "planning_size": prep.get("planning_size"),
                                "excluded_patterns": sorted(exclude_patterns),
                                "scan": prep.get("scan"), "complement_share": round(rep["by_role"].get("complement", 0) / max(1, len(rows)), 4),
                                "note": "the 70:30 complement:equiv ratio is not reachable: complement twins need a certified base type (12 of 24) and the "
                                        "source cap (10%) limits the 6 sources that hold them"},
                    "pooled_twin_set": {"other_blocks": pooled["by_block"] if pooled else None, "other_twin_rows": pooled["total"] if pooled else None},
                    "pooled_spec_3_18_shares": pool_rep},
          "deferred": ([] if t37b_ids else ["T37b base list not on disk: T37b went to C3 (A52), so no base is excluded and the unit rule base + 1 complement + 1 equiv holds without it"]) +
                      ["G13 on the template strings and the twin rows (one final all-block run)", "G10/G11 on the loaded block (mixer)"]}
    (OUT / "qc" / "QC_REPORT.json").write_text(json.dumps(qc, indent=1) + "\n", encoding="utf-8")
    old = HAIKU / "audit_rtw"                                  # the RTW-only audit of the first design: superseded by the pooled audit
    if (old / "TASKS.json").exists():
        _supersede(old)
    full = {"bases": brep, "plan": {k: v for k, v in prep.items() if k != "scan"}, "scan": prep.get("scan"),
            "certified_types": None if cert is None else len(cert), "report": rep, "dropped": dict(dropped),
            "g_tw": {k: gtw[k] for k in ("n_pairs", "violations", "pass")}, "share_problems": allprobs, "block_gates_ok": block_ok,
            "pooled_spec_3_18_shares": pool_rep, "qc_pass": qc["pass"]}
    (OUT / "qc" / "RTW_BUILD_REPORT.json").write_text(json.dumps(full, indent=1, ensure_ascii=False) + "\n", encoding="utf-8")
    return full


def main(argv=None) -> int:
    argv = list(sys.argv[1:] if argv is None else argv)
    cmd = argv[0] if argv else "build"
    inc = "--exclude-t37b-sources" not in argv
    exf = argv[argv.index("--exclude-ids") + 1] if "--exclude-ids" in argv else None
    if cmd == "cardtasks":
        bases, brep = load_bases(inc)
        man = write_card_tasks(bases)
        print(json.dumps({r: {k: m[k] for k in ("batch_id", "n_tasks", "n_items")} for r, m in man.items()}), brep["bases"])
        return 0
    tgt = int(argv[argv.index("--target") + 1]) if "--target" in argv else TARGET
    stp = int(argv[argv.index("--step") + 1]) if "--step" in argv else 1000
    flr = int(argv[argv.index("--floor") + 1]) if "--floor" in argv else 1000
    full = build(tgt, inc, exf, preview="--preview" in argv, strict="--strict-pattern-cap" in argv, greedy="--greedy" in argv, step=stp, floor=flr)
    keys = ("bases", "plan", "dropped", "g_tw", "share_problems") + (() if full.get("preview") else ("certified_types", "block_gates_ok", "pooled_spec_3_18_shares", "qc_pass"))
    print(json.dumps({k: full[k] for k in keys}, indent=1)[:3500])
    print(json.dumps(full["report"], indent=1)[:2500])
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
