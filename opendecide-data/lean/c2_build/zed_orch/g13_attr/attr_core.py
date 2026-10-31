"""attr_core.py: shared loaders and the c2_mixdev attribution scan for the G13 attribution analysis (16 Oct 2026).

Analysis only. CPU, no network, nothing G13-official is written. It imports the engine (c_build/decontam_g13.py) and the
C2 wrapper (c2_build/g13_c2.py) READ-ONLY and re-uses their classes and functions unchanged: g.words, g.TrainIndex,
g.Scan (exact_full / exact_seg / substring / ngram10 / tulu8 / minhash on the training side of the c2_mixdev target),
g.sub_units (A25 c: state + option only), X.row_units / X.engine_units, X.A53State-style waiver (X.a53_apply) and
X.A53Context (program-literal tiling). Method 5 (embed) is NOT recomputed (it needs the sentence encoder): the logs show
embed == exact_full unit counts for every T block, so it adds no unit there.

The dev set is rebuilt EXACTLY as the batch-4 candidates run (16 Oct 2026, 19:15) saw it: the files in each log's
inputs_at_start (sha256-verified); T27 had no mixdev then, and T33's mixdev has since been superseded (its batch-4
version is found by sha256 under data/c2_parts/T33/qc/_superseded_r2).

Only C2-side files are read: data/c2_parts/*/out/{candidates_c2,mixdev_S5}.jsonl, c2_build/families/<B>/** code and pools,
logs/decontam_counts/c2_cand_<B>.json. No path with "ohs", no sealed folder, no Jev output is opened by this module.
"""
from __future__ import annotations

import hashlib
import json
import os
import re
import sys
from collections import Counter, defaultdict
from pathlib import Path

HERE = Path(__file__).resolve().parent
LEAN = HERE.parents[2]
for _p in (str(LEAN / "c2_build"), str(LEAN / "c_build")):
    if _p not in sys.path:
        sys.path.insert(0, _p)
sys.dont_write_bytecode = True

import c2io  # noqa: E402
import decontam_g13 as g  # noqa: E402  (read-only)
import g13_c2 as X  # noqa: E402  (read-only)

BLOCKS = ["T01", "T06", "T07", "T12", "T15", "T23", "T24", "T25", "T26", "T28", "T29", "T30", "T31", "GB", "GW", "MD"]
LOGS = LEAN / "logs" / "decontam_counts"
ILOG = X.LinkGuardedInputLog()


def log_of(block: str) -> dict:
    return json.loads((LOGS / f"c2_cand_{block}.json").read_text(encoding="utf-8"))


def sha_file(p: Path) -> str:
    return hashlib.sha256(Path(p).read_bytes()).hexdigest()


def read_jsonl(p: Path) -> list[dict]:
    return ILOG.jsonl(Path(p))


# ---- the batch-4 dev set -------------------------------------------------------------------------------------------
def batch4_dev_files(ref_block: str = "T25") -> tuple[dict, dict]:
    """{mixdev family label: Path} of the c2_mixdev files the batch-4 run read (sha256 equal to the log's), and a record
    of where each came from. A file whose current sha256 differs is looked for by sha256 in the family's own folder."""
    ias = log_of(ref_block)["inputs_at_start"]
    paths = log_of(ref_block)["inputs_at_start_paths"]
    out, rec = {}, {}
    for key, sha in sorted(ias.items()):
        rel = paths.get(key) or key
        if not rel.endswith("mixdev_S5.jsonl"):
            continue
        fam = rel.split("/")[2]                                   # data/c2_parts/<FAM>/out/mixdev_S5.jsonl
        cur = LEAN / rel
        if X.resolved_refusal(cur):
            raise SystemExit(f"refused: {rel}")
        if cur.is_file() and sha_file(cur) == sha:
            out[fam], rec[fam] = cur, {"source": rel, "sha256": sha, "status": "current file == batch-4 file"}
            continue
        found = None
        for dp, dn, fn in os.walk(LEAN / "data" / "c2_parts" / fam):
            dn[:] = [d for d in dn if not X.resolved_refusal(Path(dp) / d)]
            for f in fn:
                if f.endswith("mixdev_S5.jsonl"):
                    q = Path(dp) / f
                    if sha_file(q) == sha:
                        found = q
                        break
            if found:
                break
        if not found:
            raise SystemExit(f"batch-4 dev file for {fam} (sha {sha[:12]}) not found")
        out[fam] = found
        rec[fam] = {"source": str(found.relative_to(LEAN)), "sha256": sha,
                    "status": "SUPERSEDED version found by sha256 (the current file differs)"}
    return out, rec


def load_dev(files: dict) -> tuple[dict, dict]:
    """({family label: rows}, {row id: family label})"""
    rows, fam_of = {}, {}
    for fam, p in files.items():
        rs = read_jsonl(p)
        rows[fam] = rs
        for r in rs:
            if r["id"] in fam_of and fam_of[r["id"]] != fam:
                raise SystemExit(f"dev row id {r['id']} occurs in two mixdev files")
            fam_of[r["id"]] = fam
    return rows, fam_of


def load_block(block: str) -> list[dict]:
    f = c2io.fam_files(block)["cand"]
    return read_jsonl(f)


# ---- the scan (engine classes, per eval text) -----------------------------------------------------------------------
SUB = ("state", "option")                                       # g.MIXDEV_TRAIN_FIELDS


def scan_block(block: str, rows: list[dict], dev_rows: dict) -> dict:
    """The engine's c2_mixdev scan of one block's candidates, attributed per eval text.
    Returns {"units", "hits": {unit key: [ (dev fam, dev row id, 'S'|'O<j>', method, training field, training text id) ]},
    "idx", "eu"}."""
    units = X.row_units(rows)
    eu = g.sub_units(X.engine_units(units), SUB)
    idx = g.TrainIndex(eu)
    sc = g.Scan(idx, None, None, defer=False)
    lab_info = {}
    for fam, rs in dev_rows.items():
        for r in rs:
            st = r.get("state")
            if isinstance(st, str) and st.strip():
                lab = ("S", r["id"])
                lab_info[lab] = (fam, r["id"], "S")
                sc.add_item((lab,), [(st, True)], "all", False)
            for j, o in enumerate(r.get("options") or []):
                if isinstance(o, str) and o.strip():
                    lab = (f"O{j}", r["id"])
                    lab_info[lab] = (fam, r["id"], f"O{j}")
                    sc.add_item((lab,), [(o, False)], "all", False)
    sc.flush()
    hits = defaultdict(list)
    for lab, ms in sc.hits.items():
        fam, rid, ek = lab_info[lab]
        for m, us in ms.items():
            for u in us:
                for ui, f in idx.occ[u]:
                    if m == "exact_short" and f == "option":
                        continue
                    hits[eu[ui]["key"]].append((fam, rid, ek, m, f, u))
    return {"units": units, "hits": dict(hits), "idx": idx, "eu": eu}


# ---- A53 on top of the scan (the wrapper's own function) --------------------------------------------------------------
def a53_state(dev_rows: dict):
    """An X.A53State for the batch-4 dev set (the class's own constructor reads the CURRENT files, so it is filled by
    hand with the batch-4 rows; everything else is the wrapper's code)."""
    allrows = [r for rs in dev_rows.values() for r in rs]
    st = X.A53State.__new__(X.A53State)
    st.ilog, st.ctx, st.refused = ILOG, {}, {}
    st.dev = {"c2_mixdev": allrows}
    st.items = {"c2_mixdev": set().union(*[X.a53_row_items(r, False) for r in allrows])}
    return st


def hits_for_a53(unit_hits: dict) -> dict:
    """{method: {unit key: set(training fields)}} from the scan."""
    by = defaultdict(lambda: defaultdict(set))
    for k, hs in unit_hits.items():
        for fam, rid, ek, m, f, u in hs:
            by[m][k].add(f)
    return by


def apply_a53(block: str, units: list[dict], unit_hits: dict, st) -> tuple[dict, dict]:
    """(binding hits {method: {unit key: fields}}, a53 record). Calls the wrapper's a53_apply unchanged."""
    by = hits_for_a53(unit_hits)
    hits = {"c2_mixdev": {m: {k: set(v) for k, v in d.items()} for m, d in by.items()}}
    s = {"units": units, "block": block}
    rec = X.a53_apply("candidates", s, hits, st)
    return {m: dict(d) for m, d in hits.get("c2_mixdev", {}).items()}, rec


# ---- shared items and the A53 verdict per item (the wrapper's own A53Context / a53_row_items) ----------------------------
def shared_items(block: str, rows: list[dict], units: list[dict], st) -> dict:
    """Per-item A53 status for the block against the batch-4 dev set (target c2_mixdev, own-family precondition applied
    by the caller). Items are the wrapper's: ('ng', 10-gram) / ('seg', segment) in states, ('seg', ...) and ('opt', whole
    option) in options. Returns {"ctx", "items": {item: {...}}, "unit_items": {unit key: set(items)}, "row_items"}."""
    ctx = st.context(block, rows)
    ev = st.items["c2_mixdev"]
    iv = defaultdict(lambda: defaultdict(set))
    row_items, item_rows = {}, defaultdict(set)
    for r in rows:
        its = X.a53_row_items(r, False) & ev
        row_items[r["id"]] = its
        a = X.a53_assets(r)
        for it in its:
            item_rows[it].add(r["id"])
            for d in X.A53_DIMS:
                iv[it][d].add(a[d])
    unit_items = {u["key"]: set().union(*[row_items.get(r["id"], set()) for r in u["rows_src"]]) for u in units}
    items = {}
    for it, rs in item_rows.items():
        indep = bool(ctx and ctx.has_assets and all(ctx.ndist[d] < 2 or len(iv[it][d] - {None}) >=
                                                     min(X.A53_MIN_DISTINCT, ctx.ndist[d]) for d in X.A53_DIMS))
        tiled = bool(ctx and ctx.tiled(it[1]))
        items[it] = {"rows": len(rs), "dims": {d: len(iv[it][d] - {None}) for d in X.A53_DIMS}, "indep": indep,
                     "tiled": tiled}
    return {"ctx": ctx, "items": items, "unit_items": unit_items, "row_items": row_items, "item_rows": item_rows}


# ---- helpers for the attribution report ------------------------------------------------------------------------------
LINE_BULLET = re.compile(r"^(-|\*|•)\s")
LINE_LABEL = re.compile(r"^[^:|]{1,48}:\s")


def line_type(line: str) -> str:
    s = line.strip()
    if not s:
        return "blank"
    if s.startswith("|"):
        return "table_row"
    if LINE_BULLET.match(s):
        return "bullet_line"
    if s.endswith(":"):
        return "heading_line"
    if LINE_LABEL.match(s):
        return "label_value_line"
    return "prose_line"


def state_lines_of(state: str, item: tuple) -> set:
    """Line types of the state lines an item ('ng' / 'seg') sits in (a 10-gram may span several lines)."""
    kind, text = item
    tw = text.split()
    lines = state.split("\n")
    toks, owner = [], []
    for i, ln in enumerate(lines):
        w = X.words(ln)
        toks += w
        owner += [i] * len(w)
    n, out = len(tw), set()
    for p in range(len(toks) - n + 1):
        if toks[p:p + n] == tw:
            out |= {line_type(lines[owner[q]]) for q in range(p, p + n)}
    return out


def item_fields(r: dict, item: tuple) -> set:
    """{'state', 'option'}: where in row r the A53 item occurs."""
    out = set()
    if isinstance(r.get("state"), str) and item in X._a53_text_items(r["state"], True, True, False):
        out.add("state")
    for o in r.get("options") or []:
        if isinstance(o, str) and item in X._a53_text_items(o, False, True, True):
            out.add("option")
            break
    return out


def norm_state(r: dict) -> str:
    return " ".join(X.words(r.get("state") or ""))


def norm_opts(r: dict) -> tuple:
    return tuple(sorted(" ".join(X.words(o)) for o in (r.get("options") or []) if isinstance(o, str)))


def dev_item_index(dev_rows: dict) -> dict:
    """{A53 item: set((dev file family, row id))} over the whole batch-4 dev set."""
    inv = defaultdict(set)
    for fam, rs in dev_rows.items():
        for r in rs:
            for it in X.a53_row_items(r, False):
                inv[it].add((fam, r["id"]))
    return inv
