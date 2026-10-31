"""negtwins/pooled_audit.py: the ONE pooled twin audit (A42-D 7.3) over the twins of GB, MD and RTW.

PREREG A42-D 7.3: a Sonnet reader audits 3% of the twin rows (seeded, stratified by pattern) and every pattern with more than 3%
error is dropped; a pattern with 33 or fewer audited rows is dropped on a single CONFIRMED error. The patterns are one frozen
catalogue shared by the three blocks, so the sample is drawn from the pooled twin set (every pattern gets at least one row).
Labels are never edited: a dropped pattern leaves every block (rows and relation edges), nothing else changes (7.5).

Commands (from c2_build; `PY -B -m negtwins.pooled_audit <cmd>`):
    tasks                      pool the twins, draw the sample, write haiku/audit_pooled/ (Sonnet read: same / opposite / unclear)
    flags                      read haiku/audit_pooled/answers/, list the disagreements with the expected relation (complement =
                               opposite, equiv = same) and write haiku/audit_pooled_opus/ (Opus confirms EVERY flag, blind)
    apply [--ruling TEXT] [--dry-run] [--select-a60]
                               read the Opus answers, decide the patterns (tasks.audit_decide), drop them from GB / MD / RTW
                               (backups in c2_build/_backup_pooled_audit/), put the RTW caps (source <= 10%, cell <= 2%, pooled
                               pattern <= 1.2%, yes band) and the GB card yes band back by removal only, update MANIFEST / QC
                               file records, write negtwins/stage3/POOLED_AUDIT_REPORT.json
                               --select-a60 (Ruling A60, after the RTW rebuild): keep every antonym complement twin of GB + MD +
                               RTW, N_c = floor(antonym / 0.30), the non-antonym slots split by the pooled implicit : syntactic
                               proportion, hash-earliest per kind (negtwins.a60); every other complement twin moves byte-unchanged
                               (with its relation edges) to <block>/out/c3_hold_a60.jsonl (+ .relations.jsonl) and never trains in
                               C2; the block caps are re-enforced by removal only until nothing changes (negtwins/stage3/
                               A60_SELECT_REPORT.json; backups in c2_build/_backup_a60/). Refuses when a hold file already exists.
RTW's QC `pass` becomes true only when its own gates hold AND the audit is applied AND the pooled spec 3.18 shares hold. A --ruling is
recorded in the QC record (and as a deviation when a share problem remains) but NEVER removes a pooled share problem from
reasons_not_passed: no bar is changed here.
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

from . import a60 as A60
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
BACKUP_A60 = CB / "_backup_a60"
REPORT = T.HERE / "stage3" / "POOLED_AUDIT_REPORT.json"
A60_REPORT = T.HERE / "stage3" / "A60_SELECT_REPORT.json"
HOLD, HOLD_REL = "c3_hold_a60.jsonl", "c3_hold_a60.relations.jsonl"      # <block>/out/: the complement twins that do not enter C2
RTW_CAP_SEED = "negtw-plan-rtw-v1"                                       # rtw.build's cap seed (the same removal order)
A60_MAX_ITER = 200
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

def _backup(parts: Path, root: Path | None = None) -> Path:
    dst = (root or BACKUP) / datetime.datetime.now(datetime.timezone.utc).strftime("%Y%m%dT%H%M%SZ")
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


# ------------------------------------------------------------------------------------------------ A60 selection (pooled complement twins)

def _neg(r: dict):
    return (r.get("meta") or {}).get("negtwin")


def _is_comp(r: dict) -> bool:
    return bool(_neg(r)) and r.get("role") == "complement"


def _kind(r: dict) -> str:
    k = _neg(r).get("kind")
    if k not in A60.KINDS:
        raise ValueError(f"{r.get('id')}: complement twin of kind {k!r} (expected one of {A60.KINDS})")
    return k


def _tkey(r: dict) -> str:
    """plan.trim_pooled's order key: sha256("negtw-trim-v1" + base row id + pattern id)."""
    return A60.trim_key(r["meta"]["twin_of"], _neg(r)["pattern"])


def read_raw(p: Path) -> tuple:
    """(rows, {row id: the exact line}) of a jsonl file; the line is what a hold file copies, so held rows stay byte-unchanged."""
    rows, raw = [], {}
    for line in p.open(encoding="utf-8"):
        if line.strip():
            line = line.rstrip("\n")
            r = json.loads(line)
            rows.append(r)
            raw[r["id"]] = line
    return rows, raw


def read_raw_rels(p: Path) -> tuple:
    rels, raw = [], {}
    for line in p.open(encoding="utf-8"):
        if line.strip():
            line = line.rstrip("\n")
            x = json.loads(line)
            rels.append(x)
            raw[(x["a"], x["b"], x["type"])] = line
    return rels, raw


def a60_state(rows: dict, rels: dict, kept: dict | None = None, raw: dict | None = None, raw_rels: dict | None = None) -> dict:
    """The A60 working state: per block its rows / relation edges in file order, the RTW plan records ({(base id, pattern id):
    (base record, pattern, twin core)}) that plan.enforce_caps needs, and the twins that left (held = complement twins)."""
    return {"blocks": {b: {"rows": list(rows[b]), "rels": list(rels[b])} for b in BLOCKS},
            "order": {b: {r["id"]: i for i, r in enumerate(rows[b])} for b in BLOCKS},
            "held": {b: {"rows": [], "rels": [], "why": {}} for b in BLOCKS},
            "gone": {b: {"equiv": [], "base": []} for b in BLOCKS},
            "removed": Counter(), "kept": kept or {}, "raw": raw or {}, "raw_rels": raw_rels or {}}


def _remove(st: dict, blk: str, ids, reason: str) -> int:
    """Take rows out of a block (removal only). A complement twin goes to the block's hold list (with its relation edge); an equiv
    twin or a base row is only counted. Returns the number of rows removed."""
    ids = set(ids)
    bl = st["blocks"][blk]
    gone = [r for r in bl["rows"] if r["id"] in ids]
    if not gone:
        return 0
    bl["rows"] = [r for r in bl["rows"] if r["id"] not in ids]
    held_ids = set()
    for r in gone:
        if _is_comp(r):
            st["held"][blk]["rows"].append(r)
            st["held"][blk]["why"][r["id"]] = reason
            held_ids.add(r["id"])
            role = "complement"
        else:
            role = "equiv" if _neg(r) else "base"
            st["gone"][blk][role].append(r["id"])
        st["removed"][(blk, reason, role)] += 1
    keep = []
    for x in bl["rels"]:
        if x["b"] in held_ids:
            st["held"][blk]["rels"].append(x)
        elif x["a"] not in ids and x["b"] not in ids:
            keep.append(x)
    bl["rels"] = keep
    return len(gone)


def comp_counts(st: dict) -> dict:
    """{kind: n} of the complement twins now in the three blocks (the pooled pool the A60 bars bind on)."""
    k = Counter()
    for blk in BLOCKS:
        for r in st["blocks"][blk]["rows"]:
            if _is_comp(r):
                k[_kind(r)] += 1
    return {x: k.get(x, 0) for x in A60.KINDS}


def a60_select_step(st: dict, ratio: tuple) -> tuple:
    """A60 (c)-(e) on the complement twins now in GB + MD + RTW: keep all antonym twins, N_c = floor(antonym / 0.30), the other
    slots by `ratio`, hash-earliest per kind; every other complement twin moves to the hold list. -> (choose info, {block: moved})."""
    ranked = {k: [] for k in A60.KINDS}
    for blk in BLOCKS:
        for r in st["blocks"][blk]["rows"]:
            if _is_comp(r):
                ranked[_kind(r)].append((_tkey(r), r["id"], blk))
    for v in ranked.values():
        v.sort()
    kept, info = A60.choose(ranked, ratio)
    keep_ids = {i for v in kept.values() for (_k, i, _b) in v}
    moved = {}
    for blk in BLOCKS:
        moved[blk] = _remove(st, blk, [r["id"] for r in st["blocks"][blk]["rows"] if _is_comp(r) and r["id"] not in keep_ids], "a60_selection")
    return info, moved


def _fit_block(st: dict, blk: str) -> int:
    """mix_c2.fit_block (twins cap, size cap, domain share, MD source share; whole units / whole MD tasks) on the block's rows."""
    import mix_c2 as M
    bl = st["blocks"][blk]
    out, _rels, _info = M.fit_block(blk, [r | {"_block": blk} for r in bl["rows"]], list(bl["rels"]))
    keep = {r["id"] for r in out}
    return _remove(st, blk, [r["id"] for r in bl["rows"] if r["id"] not in keep], "fit_block")


def _gb_card_band(st: dict) -> int:
    """A42-D 5.5: every GB yes/no card inside 40-60% yes (BT.rebalance_cards: twin rows only, removal only)."""
    rows = st["blocks"]["GB"]["rows"]
    base, tw = [r for r in rows if not _neg(r)], [r for r in rows if _neg(r)]
    kept, _bal = BT.rebalance_cards(base, tw)
    return _remove(st, "GB", {r["id"] for r in tw} - {r["id"] for r in kept}, "gb_card_band")


def _rtw_items(st: dict) -> list:
    plan = st["kept"]
    return [plan[(r["meta"]["twin_of"], _neg(r)["pattern"])] for r in st["blocks"]["RTW"]["rows"]]


def _rtw_caps(st: dict) -> int:
    """RTW source <= 10%, (pattern, core) cell <= 2%, pooled pattern <= 1.2% (plan.enforce_caps, equiv twins first) and the twin yes
    share in 45-55% (plan.balance_yes), again until neither removes anything. Removal only."""
    rows = st["blocks"]["RTW"]["rows"]
    if not rows:
        return 0
    pooled = _pool_ctx({b: st["blocks"][b]["rows"] for b in ("GB", "MD")})
    items = _rtw_items(st)
    owner = {id(x): r["id"] for x, r in zip(items, rows)}
    cur = list(items)
    detail = st.setdefault("cap_detail", Counter())
    while True:
        n0 = len(cur)
        cur, rm = P.enforce_caps(cur, source_cap=0.10, type_cap=None, seed=RTW_CAP_SEED, pooled=pooled, equiv_first=True)
        for k, v in rm.items():
            detail[f"RTW_{k}_cap"] += v
        cur, y = P.balance_yes(cur)
        detail["RTW_yes_band"] += y
        if len(cur) == n0:
            break
    left = {owner[id(x)] for x in cur}
    return _remove(st, "RTW", [r["id"] for r in rows if r["id"] not in left], "rtw_caps")


def _rtw_cap_probe(st: dict) -> dict:
    """Diagnostic only (nothing is removed or applied): what each RTW cap does ALONE to the rows that stand now, and all of them
    together (the rule that is applied). Shows which cap empties the block."""
    rows = st["blocks"]["RTW"]["rows"]
    items = _rtw_items(st)
    pooled = _pool_ctx({b: st["blocks"][b]["rows"] for b in ("GB", "MD")})
    none = dict(source_cap=None, type_cap=None, pattern_cap=None, cell_cap=None)

    def left(**kw) -> int:
        return len(P.enforce_caps(list(items), seed=RTW_CAP_SEED, equiv_first=True, **{**none, **kw})[0])
    src = sorted(Counter(b["row"]["source"] for b, _p, _t in items).values(), reverse=True)
    return {"rows": len(rows), "by_role": dict(Counter(p.relation for _b, p, _t in items)), "sources": len(src), "rows_per_source": src,
            "pooled_twin_rows_other_blocks": pooled["total"],
            "rows_left_if_only": {"source<=10%": left(source_cap=0.10), "cell<=2%": left(cell_cap=P.CELL_CAP),
                                  "pooled_pattern<=1.2%": left(pattern_cap=P.PATTERN_CAP, pooled=pooled),
                                  "all_three": left(source_cap=0.10, cell_cap=P.CELL_CAP, pattern_cap=P.PATTERN_CAP, pooled=pooled)},
            "note": "diagnostic only; the applied rule is 'all_three' then the yes band, repeated"}


def a60_caps(st: dict) -> dict:
    """The block caps again on what is left, by removal only: GB card yes band and mix_c2.fit_block, MD mix_c2.fit_block (A42-D 8.2),
    RTW caps and yes band. -> {rule: rows removed}."""
    out = {"GB_card_band": _gb_card_band(st), "GB_fit_block": _fit_block(st, "GB"), "MD_fit_block": _fit_block(st, "MD"),
           "RTW_caps": _rtw_caps(st)}
    return out


def a60_run(st: dict, ratio: tuple | None = None, caps=None, max_iter: int = A60_MAX_ITER) -> dict:
    """Ruling A60 to a fixed point: select (c)-(e), re-enforce the block caps by removal only, and repeat (N_c is recomputed from the
    antonym twins that are left) until the caps remove nothing. `ratio` = the pooled implicit : syntactic counts at entry."""
    caps = caps or a60_caps
    ratio = ratio or A60.ratio_of(comp_counts(st))
    its = []
    for i in range(1, max_iter + 1):
        info, moved = a60_select_step(st, ratio)
        planned = {"kinds": comp_counts(st), "by_block_kind": _block_kinds(st)}
        probe = _rtw_cap_probe(st) if i == 1 and st["kept"] else None
        d0 = Counter(st.get("cap_detail", ()))
        cap = caps(st)
        its.append({"iteration": i, "choose": info, "moved_to_hold": moved, "planned_after_selection": planned, "cap_removals": cap,
                    "cap_detail": {k: v - d0.get(k, 0) for k, v in st.get("cap_detail", Counter()).items() if v - d0.get(k, 0)},
                    "complement_after_caps": comp_counts(st), "by_block_kind_after_caps": _block_kinds(st)}
                   | ({"rtw_cap_probe": probe} if probe else {}))
        if not any(cap.values()):
            break
    else:
        raise RuntimeError(f"A60: no fixed point after {max_iter} iterations")
    return {"ratio_implicit_syntactic": list(ratio), "iterations": its}


def _block_kinds(st: dict) -> dict:
    return {b: dict(Counter(_kind(r) for r in st["blocks"][b]["rows"] if _is_comp(r))) for b in BLOCKS}


def _ids_sha(ids) -> str:
    return C.sha("\n".join(sorted(ids)))


def hold_texts(st: dict, blk: str) -> dict:
    """The hold files of a block as text (rows in file order, copied byte-for-byte from the source lines when known) + their sha256."""
    h, order = st["held"][blk], st["order"][blk]
    rows = sorted(h["rows"], key=lambda r: order[r["id"]])
    raw, ident, lines = st["raw"].get(blk, {}), 0, []
    for r in rows:
        line = json.dumps(r, ensure_ascii=False)
        if r["id"] in raw:
            ident += raw[r["id"]] == line
            line = raw[r["id"]]
        lines.append(line)
    rels = sorted(h["rels"], key=lambda x: order.get(x["b"], 10 ** 9))
    rraw, rl, ridp = st["raw_rels"].get(blk, {}), [], 0
    for x in rels:
        line = json.dumps(x)
        k = (x["a"], x["b"], x["type"])
        if k in rraw:
            ridp += rraw[k] == line
            line = rraw[k]
        rl.append(line)
    rt, lt = "".join(x + "\n" for x in rl), "".join(x + "\n" for x in lines)
    return {"rows_text": lt, "rels_text": rt, "rows": len(rows), "relations": len(rels), "rows_sha256": C.sha(lt), "relations_sha256": C.sha(rt),
            "ids_sha256": _ids_sha(r["id"] for r in rows), "rows_with_source_line": sum(1 for r in rows if r["id"] in raw),
            "rows_roundtrip_identical": ident, "relations_roundtrip_identical": ridp,
            "by_kind": dict(Counter(_kind(r) for r in rows)), "by_reason": dict(Counter(h["why"].values()))}


def a60_summary(st: dict, before: dict, run: dict) -> dict:
    """Planned / realised counts per block and kind, the pooled shares, the holds (sha256), and the block rules on what is left."""
    blk = {}
    for b in BLOCKS:
        rows = st["blocks"][b]["rows"]
        tw = [r for r in rows if _neg(r)]
        held = st["held"][b]["rows"]
        blk[b] = {"rows_before": before["rows"][b], "rows_after": len(rows), "base_rows_after": len(rows) - len(tw),
                  "twins_before": before["twins"][b], "twins_after": len(tw),
                  "complement_before_by_kind": before["complement_by_kind"][b],
                  "complement_after_by_kind": dict(Counter(_kind(r) for r in tw if _is_comp(r))),
                  "complement_held_by_kind": dict(Counter(_kind(r) for r in held)), "complement_held": len(held),
                  "equiv_before": before["equiv"][b], "equiv_after": sum(1 for r in tw if not _is_comp(r)),
                  "removed_by_rule": {f"{k[1]}/{k[2]}": v for k, v in sorted(st["removed"].items()) if k[0] == b}}
    after = comp_counts(st)
    n_eq = sum(v["equiv_after"] for v in blk.values())
    n_cp = sum(after.values())
    pooled = A60.report(after, vacuous_ok=True)
    first = run["iterations"][0]
    return {"ratio_implicit_syntactic": run["ratio_implicit_syntactic"], "iterations": len(run["iterations"]),
            "planned_by_the_selection": first["planned_after_selection"] | {"N_c": first["choose"].get("N_c"),
                                                                            "pooled": A60.report(first["planned_after_selection"]["kinds"])},
            "last_choose": run["iterations"][-1]["choose"], "cap_removals_by_iteration": [i["cap_removals"] for i in run["iterations"]],
            "cap_detail_by_iteration": [i["cap_detail"] for i in run["iterations"]], "rtw_cap_probe": first.get("rtw_cap_probe"),
            "blocks": blk, "pooled_before": A60.report(before["pooled_kinds"]), "pooled_after": pooled,
            "complement_twins_entering": n_cp, "equiv_twins_entering": n_eq,
            "complement_to_equiv_ratio": {"complement": n_cp, "equiv": n_eq, "complement_share": round(n_cp / max(1, n_cp + n_eq), 4),
                                          "target": "70:30 (A42-D 7.1) is a target here, reported, not met"},
            "held_complement_twins": sum(len(st["held"][b]["rows"]) for b in BLOCKS)}


def a60_before(st: dict) -> dict:
    out = {"rows": {}, "twins": {}, "equiv": {}, "complement_by_kind": {}}
    for b in BLOCKS:
        rows = st["blocks"][b]["rows"]
        out["rows"][b] = len(rows)
        out["twins"][b] = sum(1 for r in rows if _neg(r))
        out["equiv"][b] = sum(1 for r in rows if _neg(r) and not _is_comp(r))
        out["complement_by_kind"][b] = dict(Counter(_kind(r) for r in rows if _is_comp(r)))
    out["pooled_kinds"] = comp_counts(st)
    return out


def a60_checks(st: dict) -> dict:
    """The block rules on the rows that are left: GB / MD mix_c2.block_rules (A42-D 5.5 / 7.1 / 8.2) and the RTW caps, yes share and
    G-TW. Nothing is waived: a miss is listed in "problems"."""
    import mix_c2 as M
    out, probs = {}, []
    for b in ("GB", "MD"):
        rep, p = M.block_rules(b, st["blocks"][b]["rows"], loaded=True)
        out[b] = {"rules": rep, "problems": p}
        probs += p
    rows = st["blocks"]["RTW"]["rows"]
    items = _rtw_items(st) if rows else []
    pooled = _pool_ctx({b: st["blocks"][b]["rows"] for b in ("GB", "MD")})
    caps = P.share_check(items, source_cap=0.10, pooled=pooled)
    rep = rtw.report_of(rows, {})
    gtw = K.g_tw([(x[0]["row"], r) for x, r in zip(items, rows)])
    pb = [x for x in P.share_problems({"cap": P.CAPS[rtw.BLOCK], "realised": len(rows), "complement": rep["by_role"].get("complement", 0),
                                       "shares_of_complement": rep["shares_of_complement"], "twin_yes_share": rep["gold"]["yes_share"]})
          if not x.startswith(rtw.KIND_SHARE_PROBLEMS)]
    for k, ok in (("source_cap_ok", "source share > 10%"), ("cell_cap_ok", "(pattern, core) cell > 2%"),
                  ("pattern_cap_pooled_ok", "pooled pattern share > 1.2%")):
        if caps.get(k) is False:
            pb.append("RTW: " + ok)
    if not gtw["pass"]:
        pb.append("RTW: G-TW violations after the selection")
    if not rows:
        pb.append("RTW holds no row after the A60 selection and its caps: the block does not enter C2")
    out["RTW"] = {"caps": caps, "report": rep, "g_tw": {k: gtw[k] for k in ("n_pairs", "violations", "pass")}, "problems": pb}
    probs += pb
    allp = Counter()
    for b in BLOCKS:
        for r in st["blocks"][b]["rows"]:
            if _neg(r):
                allp[_neg(r)["pattern"]] += 1
    tw_n, mx_p = sum(allp.values()), max(allp.values(), default=0)
    out["pooled_pattern_info"] = {"twin_rows": tw_n, "patterns": len(allp), "max_pattern_rows": mx_p,
                                  "max_pattern_share": round(mx_p / max(1, tw_n), 4), "cap_rows_at_1.2%": max(1, int(P.PATTERN_CAP * tw_n)),
                                  "patterns_over_cap": sum(1 for v in allp.values() if v > max(1, int(P.PATTERN_CAP * tw_n))),
                                  "note": "information: GB and MD are held to their own block rules, only the RTW rows are cut by this cap"}
    out["pooled"] = A60.report(comp_counts(st), vacuous_ok=True)
    probs += out["pooled"]["problems"]
    out["problems"] = probs
    return out


def a60_write(st: dict, parts: Path) -> dict:
    """Write the three blocks as they are left and each block's hold files; returns {block: hold info}. Rows are only removed."""
    holds = {}
    for b in BLOCKS:
        _write_block(b, parts, st["blocks"][b]["rows"], st["blocks"][b]["rels"])
        h = hold_texts(st, b)
        block_file(b, parts, HOLD).write_text(h["rows_text"], encoding="utf-8")
        block_file(b, parts, HOLD_REL).write_text(h["rels_text"], encoding="utf-8")
        holds[b] = {k: v for k, v in h.items() if k not in ("rows_text", "rels_text")}
    return holds


def _a60_qc_record(a: dict, blk: str, now: str) -> dict:
    """What a block's QC record keeps of the A60 selection (the hold files are named by basename only; their sha256 are the holds')."""
    b = a["blocks"][blk]
    return {"ruling": a.get("ruling"), "utc": now, "tool": "negtwins.pooled_audit --select-a60", "report": "negtwins/stage3/A60_SELECT_REPORT.json",
            "pooled_after": a["pooled_after"], "n_c": a["last_choose"].get("N_c"), "block": {k: b[k] for k in (
                "rows_before", "rows_after", "twins_before", "twins_after", "complement_after_by_kind", "complement_held_by_kind",
                "complement_held", "equiv_after", "removed_by_rule")},
            "hold": {"rows_file": HOLD, "relations_file": HOLD_REL, **{k: v for k, v in a["holds"][blk].items() if k in (
                "rows", "relations", "rows_sha256", "relations_sha256", "ids_sha256")}},
            "block_rule_problems": a["checks"][blk]["problems"] if blk in ("GB", "MD") else a["checks"]["RTW"]["problems"],
            "note": "the complement twins in the hold file never train in C2 (never relabelled, never refilled); C3 may use them"}


def a60_hold_preview(st: dict) -> dict:
    return {b: {k: v for k, v in hold_texts(st, b).items() if k not in ("rows_text", "rels_text")} for b in BLOCKS}


def a60_existing_holds(parts: Path) -> list:
    return [str(block_file(b, parts, n)) for b in BLOCKS for n in (HOLD, HOLD_REL) if block_file(b, parts, n).exists()]


def pooled_share_reasons(reasons: list, pr: dict, ruling: str | None, now: str) -> tuple:
    """RTW's reasons_not_passed after the audit: the stale audit / pooled-share reasons go, and a pooled spec 3.18 problem that stands
    is listed again. A --ruling is RECORDED (a deviation record) but never removes the problem from the list: no bar is changed
    here (A60). Returns (reasons, deviations or None)."""
    out = [x for x in reasons if "pooled Sonnet 3% twin audit" not in x and "pooled spec 3.18" not in x]
    if not pr["problems"]:
        return out, None
    out.append("pooled spec 3.18 shares over GB + MD + RTW: " + "; ".join(pr["problems"]) +
               (" (ruling recorded, the problem stands; no bar changed)" if ruling else
                " (RTW cannot carry them alone; orchestrator ruling needed; no bar changed)"))
    if not ruling:
        return out, None
    return out, [{"gate": "pooled spec 3.18 shares", "ruling": ruling, "problems": pr["problems"], "shares": pr["shares"],
                  "effect": "recorded only: the problem stays in reasons_not_passed", "utc": now}]


def _a60_load(parts: Path, kept: dict) -> dict:
    """The A60 state from the three block files on disk (raw lines kept, so a held row is copied byte-for-byte)."""
    rows, rels, raw, raw_rels = {}, {}, {}, {}
    for b in BLOCKS:
        rows[b], raw[b] = read_raw(block_file(b, parts))
        rels[b], raw_rels[b] = read_raw_rels(block_file(b, parts, "candidates_c2.relations.jsonl"))
    return a60_state(rows, rels, kept=kept, raw=raw, raw_rels=raw_rels)


def a60_report(st: dict, ruling: str | None = None) -> dict:
    """Run Ruling A60 on the state (in place) and report: planned counts per block and kind, shares, caps, holds (sha256 preview)."""
    before = a60_before(st)
    run = a60_run(st)
    out = a60_summary(st, before, run)
    chk = a60_checks(st)
    out |= {"checks": chk, "problems": chk["problems"], "hold_preview": a60_hold_preview(st), "ruling": ruling,
            "removed_not_held": {b: {k: {"n": len(v), "ids_sha256": _ids_sha(v)} for k, v in st["gone"][b].items()} for b in BLOCKS}}
    return out


def cmd_apply(parts: Path = DATA / "c2_parts", ruling: str | None = None, dry_run: bool = False, select_a60: bool = False) -> dict:
    """Drop the audited-out patterns. GB and MD (already built): their twin rows of a dropped pattern leave, and GB's cards stay inside
    the 40-60% yes band (twin rows only). RTW: removal from a block planned exactly at its caps collapses (every removal tightens
    every share), so it is planned again from the surviving catalogue (the dropped patterns excluded; the same planner, caps and
    checks), which keeps the audit's meaning: no pattern with a confirmed error is in any block.
    select_a60 (Ruling A60): after the RTW rebuild, apply the pooled complement-twin selection (a60_run): only the antonym, the
    hash-earliest implicit and the hash-earliest syntactic complement twins that the bars allow stay in GB / MD / RTW; every other
    complement twin moves byte-unchanged to the block's out/c3_hold_a60.jsonl; the block caps are re-enforced by removal only."""
    held_files = a60_existing_holds(parts) if select_a60 else []
    if held_files and not dry_run:
        raise SystemExit("A60 is already applied (hold files exist: " + ", ".join(held_files) + "); a rerun would overwrite the held "
                         "twins. Restore the blocks from c2_build/_backup_a60/ first.")
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
        rb = rtw.build(10000, exclude_patterns=frozenset(drop_pat), pooled_override=pooled, write=False, keep_plan=select_a60)
        rep["rtw_rebuild"] = {"rows": rb["report"]["rows"], "by_role": rb["report"]["by_role"], "patterns_used": rb["report"]["patterns_used"],
                              "planning_size": rb["plan"].get("planning_size"), "caps": rb["plan"].get("caps"), "dropped": rb["dropped"]}
        rep["pooled_spec_3_18_shares"] = rb["pooled_spec_3_18_shares"]
        if select_a60:
            rep["a60"] = a60_report(a60_state({**new_rows, "RTW": rb["_rows"]}, {**new_rels, "RTW": rb["_relations"]}, kept=rb["_kept"]), ruling)
            if held_files:
                rep["a60"]["warning"] = "hold files already exist: this state is already A60-selected, the plan below is not meaningful"
        return rep
    bk = _backup(parts)
    bk60 = _backup(parts, BACKUP_A60) if select_a60 else None
    rep["backup"] = str(bk.relative_to(CB)) if CB in bk.parents else str(bk)
    if bk60 is not None:
        rep["backup_a60"] = str(bk60.relative_to(CB)) if CB in bk60.parents else str(bk60)
        if REPORT.exists():
            shutil.copy2(REPORT, bk60 / REPORT.name)
    holds = None
    try:
        for b in ("GB", "MD"):
            _write_block(b, parts, new_rows[b], new_rels[b])
        rb = rtw.build(10000, exclude_patterns=frozenset(drop_pat), pooled_override=pooled, write=True, keep_plan=select_a60)
        if select_a60:
            st = _a60_load(parts, rb["_kept"])
            rep["a60"] = a60_report(st, ruling)
            holds = a60_write(st, parts)
            rep["a60"]["holds"] = holds
    except BaseException:                      # a half-applied audit is worse than none: put the three blocks back, then raise
        for src in bk.rglob("*"):
            if src.is_file():
                dst = parts / src.relative_to(bk)
                shutil.copy2(src, dst)
        for b in BLOCKS:
            for n in (HOLD, HOLD_REL):
                block_file(b, parts, n).unlink(missing_ok=True)
        raise
    final = {b: read_jsonl(block_file(b, parts)) for b in BLOCKS}
    rep["final_rows"] = {b: len(final[b]) for b in BLOCKS}
    rep["final_twins"] = {b: sum(1 for r in final[b] if (r.get("meta") or {}).get("negtwin")) for b in BLOCKS}
    removed["RTW"]["rows_after_rebuild"] = len(rb["_rows"]) if select_a60 else rep["final_twins"]["RTW"]
    if select_a60:
        removed["RTW"]["rows_after_a60"] = rep["final_twins"]["RTW"]
    assert not any(r["meta"]["negtwin"]["pattern"] in drop_pat for b in BLOCKS for r in final[b] if (r.get("meta") or {}).get("negtwin"))
    kinds = Counter()
    for b in BLOCKS:
        for r in final[b]:
            n = (r.get("meta") or {}).get("negtwin")
            if n and r["role"] == "complement":
                kinds[n["kind"]] += 1
    pr = P.pooled_report([{"kinds": {x: kinds.get(x, 0) for x in ("syntactic", "implicit", "antonym")}}], vacuous_ok=select_a60)
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
            if select_a60:
                q["a60"] = _a60_qc_record(rep["a60"], b, now)
            f.write_text(json.dumps(q, indent=1) + "\n", encoding="utf-8")
    fq = parts / "RTW" / "qc" / "QC_REPORT.json"
    q = json.loads(fq.read_text())
    rt = final["RTW"]
    if select_a60:                                               # the caps / G-TW of the rows that are left (removal only since the build)
        c, g = rep["a60"]["checks"]["RTW"]["caps"], rep["a60"]["checks"]["RTW"]["g_tw"]
        q["gates"]["caps"] = {**q["gates"]["caps"], "max_source_share": c["max_source_share"], "source_cap_ok": c["source_cap_ok"],
                              "rows_le_cap": len(rt) <= P.CAPS[rtw.BLOCK], "t37b_plus_rtw_le_10000_if_t37b_le": P.CAPS[rtw.BLOCK] - len(rt),
                              "max_cell": c["max_cell"], "cell_cap_ok": c["cell_cap_ok"], "pattern_cap": c, "after_a60": True}
        q["gates"]["G-TW"] = {"pairs": g["n_pairs"], "violations": g["violations"], "pass": g["pass"], "after_a60": True}
        q["gates"]["pooled_twin_set"] = {"other_blocks": {b: rep["final_twins"][b] for b in ("GB", "MD")},
                                         "other_twin_rows": rep["final_twins"]["GB"] + rep["final_twins"]["MD"], "after_a60": True}
    caps_ok = bool(q["gates"]["caps"].get("source_cap_ok") and q["gates"]["caps"].get("cell_cap_ok")
                   and (q["gates"]["caps"].get("pattern_cap") or {}).get("pattern_cap_pooled_ok", True))
    q["negtwin_audit"] = audit_rec | {"final_twins": rep["final_twins"]["RTW"]}
    q["gates"]["pooled_audit"] = {"patterns_dropped": len(drop_pat), "rebuilt_from_surviving_catalogue": True, "rows_before": len(old_rtw),
                                  "rows_after": len(rt), "applied_utc": now}
    q["gates"]["pooled_spec_3_18_shares"] = pr
    reasons, deviations = pooled_share_reasons(q.get("reasons_not_passed", []), pr, ruling, now)
    if deviations:
        q["deviations"] = deviations
    a60_probs = rep["a60"]["checks"]["RTW"]["problems"] if select_a60 else []
    reasons += [f"after the A60 selection: {x}" for x in a60_probs]
    if select_a60:
        q["a60"] = _a60_qc_record(rep["a60"], "RTW", now)
    q["reasons_not_passed"] = reasons
    q["block_gates_ok"] = bool(q.get("block_gates_ok") and caps_ok and not a60_probs)
    q["pass"] = bool(q["block_gates_ok"] and not reasons)
    q["passed_utc"] = now if q["pass"] else None
    fq.write_text(json.dumps(q, indent=1) + "\n", encoding="utf-8")
    rep["rtw_qc_pass"] = q["pass"]
    rep["rtw_reasons_not_passed"] = reasons
    rep["rtw_rebuild"] = {"rows": len(rt), "by_role": dict(Counter(r["role"] for r in rt)), "caps": q["gates"]["caps"],
                          "yes_share": round(sum(r["gold"] for r in rt) / max(1, len(rt)), 4)}
    REPORT.parent.mkdir(exist_ok=True)
    REPORT.write_text(json.dumps(rep, indent=1) + "\n", encoding="utf-8")
    if select_a60:
        A60_REPORT.write_text(json.dumps(rep["a60"], indent=1) + "\n", encoding="utf-8")
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
        out = cmd_apply(parts, a[a.index("--ruling") + 1] if "--ruling" in a else None, "--dry-run" in a, "--select-a60" in a)
    else:
        raise SystemExit(__doc__)
    print(json.dumps(out, indent=1)[:(40000 if "--select-a60" in a else 4000)])
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
