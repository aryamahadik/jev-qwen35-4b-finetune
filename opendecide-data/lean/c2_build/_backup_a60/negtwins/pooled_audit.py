"""negtwins/pooled_audit.py: the ONE pooled twin audit (A42-D 7.3) over the twins of GB, MD and RTW.

PREREG A42-D 7.3: a Sonnet reader audits 3% of the twin rows (seeded, stratified by pattern) and every pattern with more than 3%
error is dropped; a pattern with 33 or fewer audited rows is dropped on a single CONFIRMED error. The patterns are one frozen
catalogue shared by the three blocks, so the sample is drawn from the pooled twin set (every pattern gets at least one row).
Labels are never edited: a dropped pattern leaves every block (rows and relation edges), nothing else changes (7.5).

Commands (from c2_build; `PY -B -m negtwins.pooled_audit <cmd>`):
    tasks                      pool the twins, draw the sample, write haiku/audit_pooled/ (Sonnet read: same / opposite / unclear)
    flags                      read haiku/audit_pooled/answers/, list the disagreements with the expected relation (complement =
                               opposite, equiv = same) and write haiku/audit_pooled_opus/ (Opus confirms EVERY flag, blind)
    apply [--ruling TEXT] [--dry-run]
                               read the Opus answers, decide the patterns (tasks.audit_decide), drop them from GB / MD / RTW
                               (backups in c2_build/_backup_pooled_audit/), put the RTW caps (source <= 10%, cell <= 2%, pooled
                               pattern <= 1.2%, yes band) and the GB card yes band back by removal only, update MANIFEST / QC
                               file records, write negtwins/stage3/POOLED_AUDIT_REPORT.json
RTW's QC `pass` becomes true only when its own gates hold AND the audit is applied AND the pooled spec 3.18 shares hold; if they do not,
an orchestrator ruling is passed with --ruling and recorded as a deviation (no bar is changed here).
"""
from __future__ import annotations

import datetime
import hashlib
import json
import shutil
import sys
from collections import Counter, defaultdict
from pathlib import Path

from c2_kit import chunker
from t37b import select as SEL

from . import block_twins as BT
from . import checks as K
from . import core as C
from . import plan as P
from . import rtw
from . import tasks as T

CB = rtw.CB
DATA = rtw.DATA
HAIKU = T.HERE / "haiku"
ROOT = HAIKU / "audit_pooled"
ROOT_OPUS = HAIKU / "audit_pooled_opus"
BACKUP = CB / "_backup_pooled_audit"
REPORT = T.HERE / "stage3" / "POOLED_AUDIT_REPORT.json"
GEN = "pa1"
SEED = "negtw-audit-pooled-" + GEN
BLOCKS = ("GB", "MD", "RTW")
WANT = {"complement": "opposite", "equiv": "same"}


def read_jsonl(p: Path) -> list:
    return [json.loads(l) for l in p.open(encoding="utf-8") if l.strip()]


def file_sha(p: Path) -> str:
    return hashlib.sha256(p.read_bytes()).hexdigest()


def block_file(b: str, parts: Path, name: str = "candidates_c2.jsonl") -> Path:
    return parts / b / "out" / name


# ------------------------------------------------------------------------------------------------ the pooled twin set

def pool(parts: Path = DATA / "c2_parts") -> list:
    """[{block, twin, base}] for every twin row of GB, MD and RTW (the base row is the one the twin names)."""
    out = []
    for b in ("GB", "MD"):
        rows = read_jsonl(block_file(b, parts))
        idx = {r["id"]: r for r in rows}
        for r in rows:
            if (r.get("meta") or {}).get("negtwin"):
                out.append({"block": b, "twin": r, "base": idx[r["meta"]["twin_of"]]})
    rows = read_jsonl(block_file("RTW", parts))
    bases, _ = rtw.load_bases(True, set())
    bidx = {x["row"]["id"]: x["row"] for x in bases}
    for r in rows:
        out.append({"block": "RTW", "twin": r, "base": bidx[r["meta"]["twin_of"]]})
    return out


def _yes_means(row: dict) -> str | None:
    c = (row.get("card") or "").strip()
    if not c:
        return None
    d = SEL.parse_card(c)
    return d[0] if d else c.replace("- yes:", "", 1).strip()


def pair_item(base: dict, twin: dict) -> tuple:
    _, cb = C.split_instruction(base["instructions"])
    _, ct = C.split_instruction(twin["instructions"])
    ya, yb = _yes_means(base), _yes_means(twin)
    qa = cb + (f" (yes means: {ya})" if ya else "")
    qb = ct + (f" (yes means: {yb})" if yb else "")
    return f"audit|{twin['id']}", {"question_a": qa, "question_b": qb}


def draw(entries: list) -> list:
    """The seeded 3% sample stratified by pattern (tasks.audit_sample on the pooled twin rows) -> entries."""
    by_id = {e["twin"]["id"]: e for e in entries}
    return [by_id[r["id"]] for r in T.audit_sample([e["twin"] for e in entries], seed=SEED)]


def make_batch(sample: list):
    return T._batch("polarity", [pair_item(e["base"], e["twin"]) for e in sample], SEED, T.AUDIT_PROMPT)


def files_record(parts: Path) -> dict:
    return {b: {"candidates_c2.jsonl": file_sha(block_file(b, parts))} for b in BLOCKS}


def cmd_tasks(parts: Path = DATA / "c2_parts") -> dict:
    entries = pool(parts)
    sample = draw(entries)
    batch = make_batch(sample)
    if (ROOT / "TASKS.json").exists() and json.loads((ROOT / "TASKS.json").read_text())["batch_id"] != batch.batch_id:
        _supersede(ROOT)
    kinds = Counter(e["block"] for e in sample)
    man = T._write(ROOT, batch, "Sonnet pooled twin audit (GB + MD + RTW)", T.POL_FORMAT, "polarity:negtw_audit_pooled",
                   extra={"reader": "sonnet", "fraction": T.AUDIT_FRAC, "blocks": list(BLOCKS), "n_twin_rows": len(entries),
                          "n_sampled_by_block": dict(kinds), "n_patterns_sampled": len({e["twin"]["meta"]["negtwin"]["pattern"] for e in sample})})
    rec = {"batch_id": batch.batch_id, "seed": SEED, "n_twins": len(entries), "twins_by_block": dict(Counter(e["block"] for e in entries)),
           "files_sha256": files_record(parts), "items": [list(pair_item(e["base"], e["twin"])) for e in sample],
           "sample": [{"twin_id": e["twin"]["id"], "block": e["block"], "pattern": e["twin"]["meta"]["negtwin"]["pattern"],
                       "role": e["twin"]["role"], "kind": e["twin"]["meta"]["negtwin"]["kind"]} for e in sample]}
    (ROOT / "SAMPLE.json").write_text(json.dumps(rec, indent=1) + "\n", encoding="utf-8")
    return {"batch_id": batch.batch_id, "n_tasks": man["n_tasks"], "n_items": man["n_items"], "n_twins": len(entries),
            "twins_by_block": rec["twins_by_block"], "sample_by_block": dict(kinds), "patterns": man["n_patterns_sampled"]}


def _supersede(root: Path) -> None:
    dst = HAIKU / "_superseded_rtw"
    dst.mkdir(exist_ok=True)
    n = len(list(dst.glob(root.name + "*")))
    shutil.move(str(root), str(dst / f"{root.name}_{n}"))


# ------------------------------------------------------------------------------------------------ answers

def load_relations(root: Path, batch) -> dict:
    files = sorted((root / "answers").glob("*.json")) if (root / "answers").exists() else []
    if not files:
        raise SystemExit(f"{root.name}: no answers yet")
    raw = {p.stem: json.loads(p.read_text(encoding="utf-8")) for p in files}
    ans, probs = chunker.load_answers(batch, raw)
    if probs:
        raise SystemExit(f"{root.name}: answer problems {probs[:5]}")
    bad = {k: v for k, v in T.relations(ans).items() if v not in ("same", "opposite", "unclear")}
    if bad:
        raise SystemExit(f"{root.name}: {len(bad)} answers are not same / opposite / unclear")
    return T.relations(ans)


def load_sample() -> dict:
    return json.loads((ROOT / "SAMPLE.json").read_text())


def batch_of(rec: dict):
    """The audit batch rebuilt from the items stored at draw time (independent of the live block files)."""
    batch = T._batch("polarity", [(i, it) for i, it in rec["items"]], rec["seed"], T.AUDIT_PROMPT)
    if batch.batch_id != rec["batch_id"]:
        raise SystemExit("the rebuilt batch does not match SAMPLE.json")
    return batch


def cmd_flags(parts: Path = DATA / "c2_parts") -> dict:
    rec = load_sample()
    rel = load_relations(ROOT, batch_of(rec))
    flags = []
    for s_ in rec["sample"]:
        got = rel[f"audit|{s_['twin_id']}"]
        if got != WANT[s_["role"]]:
            flags.append({**s_, "expected": WANT[s_["role"]], "sonnet": got})
    out = {"batch_id": rec["batch_id"], "sampled": len(rec["sample"]), "flags": len(flags),
           "by_block": dict(Counter(f["block"] for f in flags)), "by_answer": dict(Counter(f["sonnet"] for f in flags)), "flagged": flags}
    (ROOT / "FLAGS.json").write_text(json.dumps(out, indent=1) + "\n", encoding="utf-8")
    if flags:
        ids = {f"audit|{f['twin_id']}" for f in flags}
        ob = T._batch("polarity", [(i, it) for i, it in rec["items"] if i in ids], rec["seed"] + "-opus", T.AUDIT_PROMPT)
        if (ROOT_OPUS / "TASKS.json").exists() and json.loads((ROOT_OPUS / "TASKS.json").read_text())["batch_id"] != ob.batch_id:
            _supersede(ROOT_OPUS)
        man = T._write(ROOT_OPUS, ob, "Opus confirmation of pooled twin audit flags", T.POL_FORMAT, "polarity:negtw_audit_pooled_opus",
                       extra={"reader": "opus", "flags": len(flags)})
        out["opus_tasks"] = {"batch_id": ob.batch_id, "n_tasks": man["n_tasks"], "n_items": man["n_items"],
                             "task_files": [t["task_file"] for t in man["tasks"]], "answer_files": [t["answer_file"] for t in man["tasks"]]}
    return {k: v for k, v in out.items() if k != "flagged"}


# ------------------------------------------------------------------------------------------------ apply

def _backup(parts: Path) -> Path:
    dst = BACKUP / datetime.datetime.now(datetime.timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    for b in BLOCKS:
        for sub, names in (("out", ("candidates_c2.jsonl", "candidates_c2.relations.jsonl", "MANIFEST.json")), ("qc", ("QC_REPORT.json",))):
            for n in names:
                src = parts / b / sub / n
                if src.exists():
                    (dst / b / sub).mkdir(parents=True, exist_ok=True)
                    shutil.copy2(src, dst / b / sub / n)
    return dst


def _write_block(b: str, parts: Path, rows: list, rels: list) -> dict:
    ct = "".join(json.dumps(r, ensure_ascii=False) + "\n" for r in rows)
    rt = "".join(json.dumps(x) + "\n" for x in rels)
    block_file(b, parts).write_text(ct, encoding="utf-8")
    block_file(b, parts, "candidates_c2.relations.jsonl").write_text(rt, encoding="utf-8")
    files = {"candidates_c2.jsonl": {"sha256": C.sha(ct), "rows": len(rows)},
             "candidates_c2.relations.jsonl": {"sha256": C.sha(rt), "rows": len(rels)}}
    for f in (parts / b / "out" / "MANIFEST.json", parts / b / "qc" / "QC_REPORT.json"):
        if f.exists():
            m = json.loads(f.read_text())
            m["files"] = {**(m.get("files") or {}), **files}
            f.write_text(json.dumps(m, indent=1) + "\n", encoding="utf-8")
    return files


def _pool_ctx(new_rows: dict) -> dict:
    """The twin context of GB and MD after the drops (what the RTW pattern cap is pooled with)."""
    oc, kinds, by_block = Counter(), Counter(), {}
    for b in ("GB", "MD"):
        n = 0
        for r in new_rows[b]:
            ng = (r.get("meta") or {}).get("negtwin")
            if ng:
                oc[ng["pattern"]] += 1
                n += 1
                if r["role"] == "complement":
                    kinds[ng["kind"]] += 1
        by_block[b] = n
    return {"counts": oc, "total": sum(oc.values()), "kinds": dict(kinds), "by_block": by_block}


def cmd_apply(parts: Path = DATA / "c2_parts", ruling: str | None = None, dry_run: bool = False) -> dict:
    """Drop the audited-out patterns. GB and MD (already built): their twin rows of a dropped pattern leave, and GB's cards stay inside
    the 40-60% yes band (twin rows only). RTW: removal from a block planned exactly at its caps collapses (every removal tightens
    every share), so it is planned again from the surviving catalogue (the dropped patterns excluded; the same planner, caps and
    checks), which keeps the audit's meaning: no pattern with a confirmed error is in any block."""
    rec = load_sample()
    son = load_relations(ROOT, batch_of(rec))
    flags = json.loads((ROOT / "FLAGS.json").read_text())
    opus_rel = {}
    if flags["flags"]:
        ids = {f"audit|{f['twin_id']}" for f in flags["flagged"]}
        ob = T._batch("polarity", [(i, it) for i, it in rec["items"] if i in ids], rec["seed"] + "-opus", T.AUDIT_PROMPT)
        opus_rel = load_relations(ROOT_OPUS, ob)
    role_of = {s_["twin_id"]: s_["role"] for s_ in rec["sample"]}
    sample = [{"id": s_["twin_id"], "role": s_["role"], "meta": {"negtwin": {"pattern": s_["pattern"]}}} for s_ in rec["sample"]]

    def confirm(tid: str) -> bool:                 # the flag stands only when Opus (blind) also does not give the expected relation
        return opus_rel[f"audit|{tid}"] != WANT[role_of[tid]]

    dec = T.audit_decide(sample, son, confirm)
    drop_pat = {pid for pid, d in dec.items() if d["drop"]}
    confirmed = [t for d in dec.values() for t in d["error_ids"]]
    block_of = {s_["twin_id"]: s_["block"] for s_ in rec["sample"]}
    rep = {"batch_id": rec["batch_id"], "sampled": len(sample), "patterns_audited": len(dec), "sonnet_flags": flags["flags"],
           "opus_confirmed_errors": len(confirmed), "opus_overturned": flags["flags"] - len(confirmed),
           "patterns_dropped": sorted(drop_pat), "n_patterns_dropped": len(drop_pat),
           "confirmed_error_by_block": dict(Counter(block_of[t] for t in confirmed)),
           "rule": "A42-D 7.3: > 3% error, or <= 33 audited rows and one confirmed error"}
    new_rows, new_rels, removed = {}, {}, {}
    for b in ("GB", "MD"):
        rows = read_jsonl(block_file(b, parts))
        rels = read_jsonl(block_file(b, parts, "candidates_c2.relations.jsonl"))
        gone = {r["id"] for r in rows if (r.get("meta") or {}).get("negtwin") and r["meta"]["negtwin"]["pattern"] in drop_pat}
        idx = {r["id"]: r for r in rows}

        def bad_site(r: dict) -> bool:             # the audit's edit-site finding as a program refusal (checks.bad_edit_site)
            if not (r.get("meta") or {}).get("negtwin"):
                return False
            cb, ct = C.split_instruction(idx[r["meta"]["twin_of"]]["instructions"]), C.split_instruction(r["instructions"])
            return bool(cb and ct and K.bad_edit_site(cb[1], ct[1]))
        site = {r["id"] for r in rows if r["id"] not in gone and bad_site(r)}
        new_rows[b] = [r for r in rows if r["id"] not in gone and r["id"] not in site]
        new_rels[b] = [x for x in rels if x["b"] not in gone and x["b"] not in site]
        removed[b] = {"pattern_drop": len(gone), "edit_site": len(site)}
    gb_base = [r for r in new_rows["GB"] if not (r.get("meta") or {}).get("negtwin")]
    gb_tw = [r for r in new_rows["GB"] if (r.get("meta") or {}).get("negtwin")]
    kept, bal = BT.rebalance_cards(gb_base, gb_tw)
    gone_gb = {r["id"] for r in gb_tw} - {r["id"] for r in kept}
    new_rows["GB"] = gb_base + kept
    new_rels["GB"] = [x for x in new_rels["GB"] if x["b"] not in gone_gb]
    removed["GB"]["card_band"] = len(gone_gb)
    rep["gb_card_band"] = {"twins_removed": len(gone_gb), "cards_unfixable": bal.get("cards_unfixable")}
    pooled = _pool_ctx(new_rows)
    old_rtw = read_jsonl(block_file("RTW", parts))
    removed["RTW"] = {"pattern_drop": sum(1 for r in old_rtw if r["meta"]["negtwin"]["pattern"] in drop_pat), "rows_before": len(old_rtw)}
    rep["removed"] = removed
    now = datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    rep["dry_run"] = dry_run
    if dry_run:
        rb = rtw.build(10000, exclude_patterns=frozenset(drop_pat), pooled_override=pooled, write=False)
        rep["rtw_rebuild"] = {"rows": rb["report"]["rows"], "by_role": rb["report"]["by_role"], "patterns_used": rb["report"]["patterns_used"],
                              "planning_size": rb["plan"].get("planning_size"), "caps": rb["plan"].get("caps"), "dropped": rb["dropped"]}
        rep["pooled_spec_3_18_shares"] = rb["pooled_spec_3_18_shares"]
        return rep
    bk = _backup(parts)
    rep["backup"] = str(bk.relative_to(CB)) if CB in bk.parents else str(bk)
    try:
        for b in ("GB", "MD"):
            _write_block(b, parts, new_rows[b], new_rels[b])
        rb = rtw.build(10000, exclude_patterns=frozenset(drop_pat), pooled_override=pooled, write=True)
    except BaseException:                      # a half-applied audit is worse than none: put the three blocks back, then raise
        for src in bk.rglob("*"):
            if src.is_file():
                dst = parts / src.relative_to(bk)
                shutil.copy2(src, dst)
        raise
    final = {b: read_jsonl(block_file(b, parts)) for b in BLOCKS}
    rep["final_rows"] = {b: len(final[b]) for b in BLOCKS}
    rep["final_twins"] = {b: sum(1 for r in final[b] if (r.get("meta") or {}).get("negtwin")) for b in BLOCKS}
    removed["RTW"]["rows_after_rebuild"] = rep["final_twins"]["RTW"]
    assert not any(r["meta"]["negtwin"]["pattern"] in drop_pat for b in BLOCKS for r in final[b] if (r.get("meta") or {}).get("negtwin"))
    kinds = Counter()
    for b in BLOCKS:
        for r in final[b]:
            n = (r.get("meta") or {}).get("negtwin")
            if n and r["role"] == "complement":
                kinds[n["kind"]] += 1
    pr = P.pooled_report([{"kinds": {x: kinds.get(x, 0) for x in ("syntactic", "implicit", "antonym")}}])
    pr["by_kind"] = {x: kinds.get(x, 0) for x in ("syntactic", "implicit", "antonym")}
    rep["pooled_spec_3_18_shares"] = pr
    audit_rec = {"tool": "negtwins.pooled_audit " + GEN, "batch_id": rec["batch_id"], "sampled": len(sample), "sonnet_flags": flags["flags"],
                 "opus_confirmed_errors": len(confirmed), "patterns_dropped": len(drop_pat), "twins_removed": removed, "utc": now,
                 "report": "negtwins/stage3/POOLED_AUDIT_REPORT.json"}
    for b in ("GB", "MD"):                                        # the base QC verdict is untouched; the audit is added to it
        f = parts / b / "qc" / "QC_REPORT.json"
        if f.exists():
            q = json.loads(f.read_text())
            q["negtwin_audit"] = audit_rec | {"final_twins": rep["final_twins"][b]}
            f.write_text(json.dumps(q, indent=1) + "\n", encoding="utf-8")
    fq = parts / "RTW" / "qc" / "QC_REPORT.json"
    q = json.loads(fq.read_text())
    rt = final["RTW"]
    caps_ok = bool(q["gates"]["caps"].get("source_cap_ok") and q["gates"]["caps"].get("cell_cap_ok")
                   and (q["gates"]["caps"].get("pattern_cap") or {}).get("pattern_cap_pooled_ok", True))
    q["negtwin_audit"] = audit_rec | {"final_twins": rep["final_twins"]["RTW"]}
    q["gates"]["pooled_audit"] = {"patterns_dropped": len(drop_pat), "rebuilt_from_surviving_catalogue": True, "rows_before": len(old_rtw),
                                  "rows_after": len(rt), "applied_utc": now}
    q["gates"]["pooled_spec_3_18_shares"] = pr
    reasons = [x for x in q.get("reasons_not_passed", []) if "pooled Sonnet 3% twin audit" not in x and "pooled spec 3.18" not in x]
    if pr["problems"]:
        if ruling:
            q["deviations"] = [{"gate": "pooled spec 3.18 shares", "ruling": ruling, "problems": pr["problems"], "shares": pr["shares"], "utc": now}]
        else:
            reasons.append("pooled spec 3.18 shares over GB + MD + RTW: " + "; ".join(pr["problems"]) +
                           " (RTW cannot carry them alone; orchestrator ruling needed; no bar changed)")
    q["reasons_not_passed"] = reasons
    q["block_gates_ok"] = bool(q.get("block_gates_ok") and caps_ok)
    q["pass"] = bool(q["block_gates_ok"] and not reasons)
    q["passed_utc"] = now if q["pass"] else None
    fq.write_text(json.dumps(q, indent=1) + "\n", encoding="utf-8")
    rep["rtw_qc_pass"] = q["pass"]
    rep["rtw_reasons_not_passed"] = reasons
    rep["rtw_rebuild"] = {"rows": len(rt), "by_role": dict(Counter(r["role"] for r in rt)), "caps": q["gates"]["caps"],
                          "yes_share": round(sum(r["gold"] for r in rt) / max(1, len(rt)), 4)}
    REPORT.parent.mkdir(exist_ok=True)
    REPORT.write_text(json.dumps(rep, indent=1) + "\n", encoding="utf-8")
    return rep


def main(argv=None) -> int:
    a = list(sys.argv[1:] if argv is None else argv)
    cmd = a[0] if a else "tasks"
    parts = Path(a[a.index("--parts") + 1]) if "--parts" in a else DATA / "c2_parts"
    if cmd == "tasks":
        out = cmd_tasks(parts)
    elif cmd == "flags":
        out = cmd_flags(parts)
    elif cmd == "apply":
        out = cmd_apply(parts, a[a.index("--ruling") + 1] if "--ruling" in a else None, "--dry-run" in a)
    else:
        raise SystemExit(__doc__)
    print(json.dumps(out, indent=1)[:4000])
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
