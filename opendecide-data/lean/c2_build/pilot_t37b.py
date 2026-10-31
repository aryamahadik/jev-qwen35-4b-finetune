"""c2_build/pilot_t37b.py: the spec 6.4 step 5 pilot for T37b (real-text complements and paraphrases on replay yes/no
rows; C2_DATA_SPEC 3.18, 4.2; G0_LITE_T37B.md v2). Called by `pilot.py run t37b`.

T37b is not a C2Plugin family (plugin.FAMILIES: "its own builder"), so its units go through t37b/builder.py instead of
c2_kit.pipeline.build_unit. The pilot follows builder.py's documented flow exactly, at pilot size:
  0. pool   author_pool.load_pool() on the frozen v1 pool + the frozen redo2 supplement (pools/redo2/MANIFEST.json:
            "supplement_of" the v1 file; both 2/2-admitted, same G0 sha), merged as one Pool.
  1. bases  select.eligible(golden_train rows of the registry sources, golden_relations, the round-1 old slice): the
            old slice ids come from c_build/replay_draw.json (old_slice_ids); their groups and normalised states from
            those golden_train rows. Source status = select.default_status() (replay register keep, not an OHS-3 hit
            source, not program-labelled) AND the replay deny-list verdict (c_build/replay_denylist_verdicts.json:
            "drop" and "part" both refuse the source here, fail closed); plus pool_drops_r1.json (spec 5.4) by id.
            Not applied at pilot (needs the C2 replay read, spec 5.4): the human rows with C1 p_g < 0.2.
  2. plan   select.plan_block(n_complement=700, n_equiv=300): the train block's 1,400 : 600 at 1,000 partner rows,
            kinds and wordings never read the gold (it only balances which bases enter, G0 A1-5), floors (implicit
            >= 25%, non-syntactic >= 30% of complements) and caps (source <= 10%,
            wording key <= 2%) on the realised block.
  3. build  builder.build_candidates: every partner written by the program; polarity programs A and B must both
            return the planned relation (the T37b G2 analogue; a disagreement drops the unit).
  4. rows   builder.finalize: partner rows, validate_partner (schema, gold = 1 - base gold for complements, the base's
            gold for equiv, card swap, same state / group / call), G15 loader_check, trim_block (floors and caps).
Written: pilot/rows.jsonl (partner rows, the new rows), pilot/bases.jsonl (their replay bases, so every relation edge
resolves), pilot/relations.jsonl ({a: base, b: partner, type}).
Gates on the partner rows: G6, G7, G10 (pilot.py functions), the S14 floors and caps (select.plan_report), and the
Haiku chunks: G5-H (100 seeded partner rows, two blind reads) and, for the same 100 units, the G0 S13 checks the full
build needs before a unit is kept (two polarity reads per distinct question pair not already read at pool stage, the
blind solver on base and on partner in separate batches). Haiku answers only flag (A37 b): no label is set anywhere.

Fix iteration 1 (14 Oct 2026; G0_LITE_T37B_A1.md): out_name (or the env var T37B_PILOT_DIR) picks the output folder under
t37b/ ("pilot" = the first pilot, kept as the verdict's input; "pilot_i1" = this iteration), so `pilot.py run t37b`
can be re-run without overwriting a pilot a verdict was written on. The program gates of the other families that
need a plugin (G3, G4, G-SL, G-LEX, overlay) are reported n/a with the reason; spec 3.0 length is measured.
"""
from __future__ import annotations

import hashlib
import json
import os
import re
import sys
import time
from collections import Counter
from pathlib import Path

HERE = Path(__file__).resolve().parent
if str(HERE) not in sys.path:
    sys.path.insert(0, str(HERE))

from c2_kit import chunker, g5h, paths  # noqa: E402
from c2_kit import rows as R  # noqa: E402
import pilot as PI  # noqa: E402
import pilot_loaders as PL  # noqa: E402
from t37b import author_pool as AP  # noqa: E402
from t37b import builder as BL  # noqa: E402
from t37b import select as SEL  # noqa: E402
from t37b import sources as SRC  # noqa: E402

LEAN = paths.LEAN
GOLDEN = LEAN / "data" / "v14_parts" / "golden_train.jsonl"
GOLDEN_RELS = LEAN / "data" / "v14_parts" / "golden_relations.jsonl"
REPLAY_DRAW = LEAN / "c_build" / "replay_draw.json"
DENY = LEAN / "c_build" / "replay_denylist_verdicts.json"
POOL_DROPS = LEAN / "logs" / "decontam_counts" / "pool_drops_r1.json"
POOL_V1 = HERE / "t37b" / "pools" / "t37b_equiv_pool.json"
POOL_R2 = HERE / "t37b" / "pools" / "redo2" / "t37b_equiv_pool_redo2.json"
N_COMPLEMENT, N_EQUIV = 700, 300            # 1,400 : 600 at a 1,000-row pilot
PLAN_SEED = "t37b-pilot-1"
ID_RE = re.compile(r'^\{"id": "([^"]+)"')
SRC_RE = re.compile(r'"source": "([^"]+)"')
POLARITY_CONTRACT = (
    "Write ONLY the answer file named at the top of this task file, with the Write tool, as one JSON array with one "
    "object per item: {\"qid\": \"<the item's qid>\", \"relation\": \"same\" | \"opposite\" | \"unclear\"}. Exactly the "
    "keys qid and relation. Valid JSON only; no text before or after the array.")
BLIND_CONTRACT = (
    "Write ONLY the answer file named at the top of this task file, with the Write tool, as one JSON array with one "
    "object per item: {\"qid\": \"<the item's qid>\", \"answer\": \"yes\" | \"no\"}. Exactly the keys qid and answer. "
    "Valid JSON only; no text before or after the array.")


class _Kit:
    """The pilot.py view of the family (no C2Plugin: G10 reads FAMILY / TIER / QFORMS / YES_NO_ONLY)."""
    FAMILY = "T37b"
    TIER = "real_text"
    QFORMS: dict = {}
    YES_NO_ONLY = True
    G0_SHA256 = BL.G0_SHA256


def load_pool() -> AP.Pool:
    man = PL.safe_json(POOL_R2.parent / "MANIFEST.json")
    if man["supplement_of"]["sha256"] != PL.sha_file(POOL_V1) or man["sha256"] != PL.sha_file(POOL_R2):
        raise PL.LoaderError("T37b pool files differ from pools/redo2/MANIFEST.json")
    v1, r2 = AP.load_pool(POOL_V1), AP.load_pool(POOL_R2)
    ids = [c["template_id"] for c in v1.paraphrases + r2.paraphrases]
    if len(set(ids)) != len(ids):
        raise PL.LoaderError("T37b pool v1 and redo2 share a template id")
    return AP.Pool(v1.paraphrases + r2.paraphrases)


def load_inputs(log=print) -> dict:
    """Golden_train rows of the registry sources (yes/no only), golden_relations, the old slice (ids, groups,
    normalised states), the pool drops and the deny-list verdicts."""
    import replay_sample as RS                       # c_build (put on sys.path by t37b.select); read-only
    t0 = time.time()
    old_ids = set(PL.safe_json(REPLAY_DRAW)["old_slice_ids"])
    drops = set(PL.safe_json(POOL_DROPS)["drop_ids"])
    deny = PL.safe_json(DENY)["verdicts"]
    sources = set(SRC.SOURCES)
    rows, old_groups, old_states, n_lines, n_drop = [], set(), set(), 0, 0
    with open(paths.check_path(GOLDEN), encoding="utf-8") as f:
        for line in f:
            n_lines += 1
            m = ID_RE.match(line)
            rid = m.group(1) if m else None
            if rid in old_ids:
                r = json.loads(line)
                old_groups.add(r["group_id"])
                old_states.add(RS.norm_state(r.get("state")))
            s = SRC_RE.search(line)
            if not s or s.group(1) not in sources or '"qtype": "noul"' not in line:
                continue
            r = json.loads(line)
            if r["id"] in drops:
                n_drop += 1
                continue
            rows.append(r)
    rels = PL.safe_jsonl(GOLDEN_RELS)
    log(f"T37b: {n_lines} golden_train lines, {len(rows)} registry yes/no rows, {n_drop} pool_drops_r1 drops, "
        f"{len(old_ids)} old-slice ids ({len(old_groups)} groups), {len(rels)} relations, {time.time() - t0:.0f}s")
    return {"rows": rows, "rels": rels, "old_ids": old_ids, "old_groups": old_groups, "old_states": old_states,
            "deny": deny, "n_lines": n_lines, "n_pool_drops": n_drop}


def status_fn(deny: dict):
    keep = SEL.default_status()

    def st(source: str, verified=frozenset()) -> bool:
        v = (deny.get(source) or {}).get("verdict")
        return keep(source, verified) and v not in ("drop", "part")
    return st


def _info(row: dict) -> PI.RowInfo:
    ctx = "\n".join(x for x in (row.get("card") or "", row.get("state") or "") if x.strip())
    return PI.RowInfo(row, None, None, -1, row["instructions"], ctx, None)


def _task_files(kind_title: str, bt, sub: str, pdir: Path, prompt: str, contract: str, gate: str, extra: dict):
    files, tasks = {}, []
    for c in bt.chunks:
        tid = c["task_id"]
        ans = pdir / sub / "answers" / f"{tid}.json"
        tf = pdir / sub / "tasks" / f"{tid}.md"
        text = PI._task_text(kind_title, "T37b", tid, ans, len(c["items"]), prompt, contract, c["items"])
        files[f"{sub}/tasks/{tid}.md"] = text
        tasks.append({"gate": gate, **extra, "task_id": tid, "task_file": str(tf), "answer_file": str(ans),
                      "n_items": len(c["items"]), "batch_id": bt.batch_id,
                      "task_sha256": hashlib.sha256(text.encode()).hexdigest(), "allowed_read": [str(tf)],
                      "allowed_write": [str(ans)]})
    return files, tasks


def run(n_rows: int = PI.N_ROWS, *, write: bool = True, run_g15: bool = True, log=print,
        out_name: str | None = None) -> dict:
    fdir = PL.family_dir("t37b")
    out_name = out_name or os.environ.get("T37B_PILOT_DIR") or "pilot"
    if not re.fullmatch(r"pilot[A-Za-z0-9_]*", out_name):
        raise ValueError(f"T37b pilot folder {out_name!r}: must be pilot or pilot_<tag>")
    pdir = fdir / out_name
    if write and (pdir / "PILOT_VERDICT.json").exists():
        raise RuntimeError(f"{pdir} holds a PILOT_VERDICT.json: a verdict's inputs are never overwritten; pass another "
                           "out_name (T37B_PILOT_DIR)")
    if BL.g0_problems():
        raise RuntimeError(f"T37b G0 check failed: {BL.g0_problems()}")
    t0 = time.time()
    pool = load_pool()
    inp = load_inputs(log)
    n_comp = round(n_rows * 0.7)
    n_eq = n_rows - n_comp
    bases, sel_rep = SEL.eligible(inp["rows"], inp["rels"], old_ids=inp["old_ids"], old_groups=inp["old_groups"],
                                  old_states=inp["old_states"], status=status_fn(inp["deny"]))
    log(f"T37b: {len(bases)} eligible bases")
    plan, plan_rep = SEL.plan_block(bases, n_complement=n_comp, n_equiv=n_eq, seed=PLAN_SEED,
                                    equiv_pool=pool.choices())
    diagnosis = None
    if len(plan) < n_rows:              # report-only probe: one _plan_once at the target basis, caps from the target
        import math
        from c2_kit.distractors import uhash
        order = sorted(bases, key=lambda b_: uhash(PLAN_SEED, "t37b-order", b_.row["id"]))
        probe = SEL._plan_once(order, SRC.FRAMES_TRAIN, n_comp, n_eq, PLAN_SEED, "train",
                               max(1, math.floor(SEL.SOURCE_CAP * n_rows)), max(1, math.floor(SEL.TEMPLATE_CAP * n_rows)),
                               pool.choices(), True)
        tpl = SEL._template_counts(probe)
        diagnosis = {"plan_rows": len(plan), "one_pass_at_target_basis": len(probe), "distinct_wording_keys": len(tpl),
                     "max_key_count": max(tpl.values()) if tpl else 0,
                     "template_cap_at_that_size": max(1, math.floor(SEL.TEMPLATE_CAP * len(probe))),
                     "kinds": dict(Counter(i.kind for i in probe)),
                     "note": "select.plan_block re-plans on the realised size whenever a cap computed on that size "
                             "is exceeded (basis = len(plan)); every pass shrinks the caps with the plan, so the loop "
                             "only stops where every cap is its floor of 1. A generator fix (spec 6.4 step 6), not a "
                             "pilot setting"}
        log(f"T37b: plan collapsed to {len(plan)} rows (one pass at the target basis: {len(probe)})")
    cands = BL.build_candidates(plan, records=pool.records)
    ok = [c for c in cands if c.ok]
    prog_drops = Counter()
    examples = []
    for c in cands:
        if not c.ok:
            prog_drops[c.item.kind] += 1
            if len(examples) < 8:
                examples.append(f"{c.item.kind} {c.item.base.entry.key}: {c.problems[:2]}"[:300])
    rows, rels, fin = BL.finalize(ok, n_complement=n_comp, n_equiv=n_eq, run_g15=run_g15,
                                  token_fn=lambda rs: PI.real_tokens(rs)[0])
    base_of = {c.item.base.row["id"]: c.item.base.row for c in ok}
    bases_out = [base_of[e["a"]] for e in rels]
    log(f"T37b: plan {len(plan)}, candidates ok {len(ok)}/{len(cands)}, rows {len(rows)} ({time.time() - t0:.0f}s)")
    # ---- re-verify every written row (the program gates of T37b)
    bad_rows = []
    for r in rows:
        p = BL.validate_partner(r, base_of[r["meta"]["t37b"]["base_id"]])
        t = r["meta"]["t37b"]
        if t["polarity_a"] != t["polarity_b"] or t["polarity_a"] != BL.relation_of(t["kind"]):
            p.append("polarity programs")
        if BL.local_ban_hits(r["instructions"]):
            p.append("local ban")
        if p:
            bad_rows.append((r["id"], p))
    fin_drops = fin.get("dropped_at_finalize", [])
    g15_drops = [d for d in fin_drops if any(str(x).startswith("G15") for x in d[1])]
    len_drops = [d for d in fin_drops if any(str(x).startswith("length:") for x in d[1])]
    tw_drops = [d for d in fin_drops if d not in g15_drops and d not in len_drops]
    gates = {
        "pilot_size": {"value": len(rows), "bar": f">= {n_rows} partner rows of passing units (spec 6.4 step 5)",
                       "verdict": "pass" if len(rows) >= n_rows else "fail", "units_attempted": len(plan)},
        "G2": {"bar": "polarity programs A and B both return the planned relation (G0 S9, S10, S13; a disagreement "
                      "drops the unit)", "units_attempted": len(cands), "units_failed": len(cands) - len(ok),
               "failed_by_kind": dict(prog_drops), "examples": examples,
               "written_rows_pass": 1.0 if not bad_rows else round(1 - len(bad_rows) / max(1, len(rows)), 4),
               "verdict": "pass" if not bad_rows else "fail",
               "note": "the T37b G2 analogue drops failing units by design (S13); written rows re-verified"},
        "G-TW": {"bar": "complement gold = 1 - base gold, equiv gold = base gold, swapped / own / kept card, same "
                        "state, group and call (validate_partner; G0 S3, S5, S11)", "units_attempted": len(ok),
                 "units_failed": len(tw_drops),
                 "examples": [f"{a}: {b[:2]}"[:300] for a, b in tw_drops[:6]],
                 "verdict": "pass" if not bad_rows else "fail"},
        "G15": {"bar": "100% loader round trip; a failure drops the whole unit (G0 H51)",
                "units_attempted": len(ok), "units_failed": len(g15_drops),
                "verdict": "pass" if not bad_rows else "fail", "run": run_g15},
    }
    s14 = {"bar": "implicit >= 25% and antonym + option framing >= 30% of complements; source <= 10%; wording key "
                  "<= 2% (G0 S14, select.plan_report)", "report": fin, "verdict": "pass" if fin.get("pass") else
           "fail"}
    gates["S14_floors_caps"] = s14
    infos = [_info(r) for r in rows]
    gates["G6"] = PI.g6(infos)
    gates["G7"] = PI.g7(infos)
    gates["G10"] = PI.g10(infos, [], _Kit())
    gates["spec_3_0"] = PI.spec30(infos, _Kit())
    gates["spec_3_0"]["length_dropped_units"] = {"n": len(len_drops), "units": [a for a, _b in len_drops],
                                                 "note": "A1-6: a partner row over 2,000 rendered tokens drops its "
                                                         "unit at finalize (pinned tokenizer, instructions twice)"}
    na = {"G3": "T37b has no template skin to parse back: its partners are program-written strings from the base "
                "question, certified by polarity programs A and B (the G2 analogue above)",
          "G4": "the metamorphic relations are the unit itself (complement / equiv; G-TW above); T37b has no samplers",
          "G-SL": "no slot-template text: state, card and base question are replay text; the partner question is a "
                  "closed program string or a frozen pool template (G-SL linted at pool stage)",
          "G-LEX": "no plugin lexicon: the only Haiku-written wording is the frozen equiv pool, admitted 2/2 "
                   "(answers_gate.py READY)",
          "overlay": "the spec 4.1 overlay shares are plugin-family rules; T37b's own shares are S14 above"}
    gates["not_applicable"] = {"verdict": "n/a", "applies_to": sorted(na),
                               "note": "; ".join(f"{g}: {why}" for g, why in na.items()), "reasons": na}
    # ---- Haiku chunks: G5-H (100 seeded partner rows, two reads) + G0 S13 for the same units
    files, tasks5, key5 = PI.g5h_chunks(infos, "T37b", pdir)
    cand_of = {BL.partner_row(c)["id"]: c for c in ok}
    s13 = [cand_of[i] for i in key5["row_ids"] if i in cand_of]
    pa, pb = BL.polarity_batches(s13, seed=f"{PLAN_SEED}|s13", judged=pool.judged)
    ba, bb = BL.blind_batches(s13, seed=f"{PLAN_SEED}|s13")
    tasks13 = []
    if pa is not None:
        for reader, bt in (("A", pa), ("B", pb)):
            f, t = _task_files("T37b polarity judgement", bt, "s13", pdir, BL.POLARITY_PROMPT, POLARITY_CONTRACT,
                               "S13-polarity", {"reader": reader})
            files.update(f)
            tasks13 += t
    if ba is not None:
        for side, bt in (("base", ba), ("partner", bb)):
            f, t = _task_files("T37b blind solver", bt, "s13", pdir, BL.BLIND_PROMPT, BLIND_CONTRACT, "S13-blind",
                               {"side": side})
            files.update(f)
            tasks13 += t
    key13 = {"family": "T37b", "gate": "S13", "units": [c.item.pid for c in s13],
             "partner_row_of_unit": {c.item.pid: BL.partner_row(c)["id"] for c in s13},
             "polarity": {r: PI._batch_record(bt) for r, bt in (("A", pa), ("B", pb)) if bt is not None},
             "blind": {s: PI._batch_record(bt) for s, bt in (("base", ba), ("partner", bb)) if bt is not None},
             "judged_at_pool": sorted(k for c in s13 if c.pair for k in [BL.pair_key(*c.pair)] if k in pool.judged),
             "note": "orchestrator only; builder.decide(c, pol_a, pol_b, blind_base, blind_partner) keeps / drops / "
                     "sends to Claude review"}
    gates["G3-H"] = {"verdict": "n/a", "note": "T37b has no free-form text (G0 S12: Haiku writes only the equiv "
                                               "paraphrase pool, admitted 2/2 at pool stage)"}
    gates["G5-H"] = {"verdict": "pending", "bar": "0 confirmed wrong golds; ambiguous <= 1%; > 3% template "
                     "disagreement quarantines (spec 6.3; pilot reads 100 rows)", "rows": key5["n_rows"], "readers": 2,
                     "tasks": len(tasks5), "note": "two blind reads pending; then Claude adjudication"}
    gates["S13"] = {"verdict": "pending", "bar": "keep iff programs A = B = planned relation, both polarity reads = "
                    "that relation and the blind solver is consistent (opposite for complement, equal for equiv); "
                    "an inconsistent solver goes to Claude review; any other failure drops (G0 S13)",
                    "units": len(s13), "tasks": len(tasks13),
                    "note": "pilot sample = the 100 G5-H units; the full build reads every unit"}
    rows_body = "".join(json.dumps(r, ensure_ascii=False) + "\n" for r in rows)
    if write:
        paths.write_jsonl(pdir / "rows.jsonl", rows)
        paths.write_jsonl(pdir / "bases.jsonl", bases_out)
        paths.write_jsonl(pdir / "relations.jsonl", rels)
        for rel, text in files.items():
            paths.write_text(pdir / rel, text)
        paths.write_text(pdir / "g5h" / "answers" / "README.txt",
                         "Haiku G5-H answer files: one <task_id>.json per task file in ../tasks/.\n")
        paths.write_json(pdir / "g5h" / "key.json", key5)
        paths.write_json(pdir / "g5h" / "manifest.json", {"family": "T37b", "gate": "G5-H", "tasks": tasks5,
                                                           "prompt_sha": chunker.sha(PI.G5H_PROMPT)})
        if tasks13:
            paths.write_text(pdir / "s13" / "answers" / "README.txt",
                             "Haiku S13 answer files (polarity reads, blind solver): one <task_id>.json per task.\n")
            paths.write_json(pdir / "s13" / "key.json", key13)
            paths.write_json(pdir / "s13" / "manifest.json", {"family": "T37b", "gate": "S13", "tasks": tasks13})
    report = {"family": "T37b", "version": PI.PILOT_VERSION, "created_utc": time.strftime("%Y-%m-%dT%H:%M:%SZ",
                                                                                          time.gmtime()),
              "spec": "C2_DATA_SPEC 6.4 step 5; 3.18; 4.2; G0_LITE_T37B.md v2 + G0_LITE_T37B_A1.md (G0 v3); PREREG A37 / A38",
              "fix_iteration": out_name, "g0_amendment1_sha256": BL.G0_AMENDMENT_SHA256,
              "tier": "real_text", "g0_sha256": BL.G0_SHA256,
              "loader": "t37b/builder.py flow: author_pool.load_pool (v1 + redo2 supplement), select.eligible, "
                        "select.plan_block, builder.build_candidates, builder.finalize",
              "pools": "pools/t37b_equiv_pool.json + pools/redo2/t37b_equiv_pool_redo2.json",
              "loader_notes": ["human rows with C1 p_g < 0.2 are not removed at pilot (needs the C2 replay read, "
                               "spec 5.4); deny-list 'part' verdicts refuse the whole source (fail closed)"],
              "build": {"target_rows": n_rows, "plan": {"n_complement": n_comp, "n_equiv": n_eq, "seed": PLAN_SEED},
                        "inputs": {"golden_train_lines": inp["n_lines"], "registry_yes_no_rows": len(inp["rows"]),
                                   "pool_drops_r1_removed": inp["n_pool_drops"], "old_slice_ids": len(inp["old_ids"]),
                                   "relations": len(inp["rels"])},
                        "selection": sel_rep, "plan_report": plan_rep, "plan_diagnosis": diagnosis,
                        "candidates": len(cands),
                        "candidates_ok": len(ok), "rows_written": len(rows), "units_written": len(rows),
                        "pool_paraphrases": len(pool.paraphrases), "seconds": round(time.time() - t0, 1),
                        "reached_target": len(rows) >= n_rows},
              "files": {"rows": str(pdir / "rows.jsonl"), "rows_sha256": PI.sha_text(rows_body),
                        "bases": str(pdir / "bases.jsonl"), "relations": str(pdir / "relations.jsonl"),
                        "n_rows": len(rows), "n_relations": len(rels),
                        "relation_types": dict(Counter(x["type"] for x in rels)),
                        "kinds": dict(Counter(r["meta"]["t37b"]["kind"] for r in rows)),
                        "yes_rate": round(sum(r["gold"] for r in rows) / max(1, len(rows)), 4)},
              "gates": gates, "chunks": {"G5-H": tasks5, "S13": tasks13}, "written": write}
    report["summary"] = PI.summarize(gates)
    report["gate_lines"] = PI.gate_lines(gates).split("\n")
    if write:
        paths.write_json(pdir / "PILOT_REPORT.json", report)
    return report
