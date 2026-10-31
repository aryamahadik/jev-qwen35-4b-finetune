"""finalize_md.py: the QC-record writer of the metadata block MD (Ruling A66 (a), 17 Oct 2026). STAGED: NOT run with --write; it needs
the orchestrator's OK after a skeptic review of this code (A66 (a)).

merge_md.py hard-codes pass=false (twins, G13 and the selection were pending when it ran) and no later tool sets MD's pass. This
tool re-derives every binding non-G13 gate from the FILES on disk at the pre-registered, unchanged bars and, only with --write,
records pass=true + passed_utc in data/c2_parts/MD/qc/QC_REPORT.json. Without --write it prints the verdict as JSON (counts and
shas only) and writes nothing.

  cd lean/c2_build && ../../.venv/bin/python -B zed_orch/md_final/finalize_md.py            # dry run (default)
  cd lean/c2_build && ../../.venv/bin/python -B zed_orch/md_final/finalize_md.py --write    # only after the orchestrator says so

Gates re-derived (all must hold, else no write; the QC record is never taken as proof of itself):
  1  bars: the imported bar constants equal the pre-registered ones (no bar can be loosened by editing a module quietly).
  2  files: MANIFEST == candidates / relations on disk (sha256 + rows); hold files == the A60 record (sha256 + rows), disjoint from
     the candidates; c2io.candidate_problems empty; ids unique; relations = twin links inside the rows.
  3  block rules (A42-D 8.2, 7.1): mix_c2.block_rules('MD') with the A51 (c) deviations DERIVED here from the noise-gate re-derivation
     (not read from the record).
  4  noise gate (A42-D 8.4, A51): merge_md.gate_source re-run on the per-source answers on disk for all 11 sources: every answer
     present, every task read, the flagged tasks (>= 2 of the picked rows clearly wrong at confidence >= 0.7) equal dropped_tasks.json
     and the record, and none of them (nor any schema-dropped task) is in the candidates. The answer / key / pick / rows files are
     sha-bound (one digest recorded).
  5  twins (A42-D 7.3): G-TW 100% recomputed; every twin's pattern is in the frozen trained catalogue and none is one of the patterns
     the Sonnet / Opus pooled audit dropped; the "exactly one predicate changed" program check (checks.check_pair), the edit-site and
     A48 (h) guards re-run on every twin; the audit report (sha-bound) names the same twin count as the file.
  6  A60 / spec 3.18: the pooled complement-twin shares recomputed from the GB + MD + RTW candidates on disk (exact fractions), and
     equal to the A60 and pooled-audit records.
  7  sources (A42-D 8.3 / 8.5, A61): kit validate_row on every row (meta.licence excepted); every row carries the licence of its
     part MANIFEST and the record's licence equals the MANIFEST's; mix_c2.gated_membership clean; the A61-barred md_fdc / md_peps
     absent; the deny-list script (meta_src/c1_denylist_check.py) run: CLEAR for every md_* id in the block (the bare platform word
     "github" alone is the documented A16 (a) non-hit); the binding input meta_src/SOURCES_CANDIDATES.json sha-bound.
  8  the new record, built in memory, passes mix_c2.admission and mixer.qc_binding.

Still pending after this (listed in gates_pending, none waived): G13 on the candidates incl. the OHS-AC path, the crowd selection,
the A61 (e 5) final all-block G13 and the A61 (f) single final-mix 8.5 run. fix_iterations stays 0 (a writer fix is not a data fix).

--write order: re-check the verdict -> backup of QC_REPORT.json (verified copy, never overwritten) -> atomic replace of QC_REPORT.json
(the only file written besides the backup) -> re-read: qc_binding and admission must be clean, else the backup is restored.
"""
from __future__ import annotations

import argparse
import copy
import datetime
import hashlib
import importlib.util
import json
import os
import shutil
import subprocess
import sys
from collections import Counter, defaultdict
from fractions import Fraction
from pathlib import Path

HERE = Path(__file__).resolve().parent
BUILD = HERE.parent.parent
LEAN = BUILD.parent
sys.path.insert(0, str(BUILD))
import c2io  # noqa: E402
import mix_c2  # noqa: E402
import mixer as mx  # noqa: E402
from negtwins import a60 as A60  # noqa: E402
from negtwins import checks as K  # noqa: E402
from negtwins import core as C  # noqa: E402
from negtwins import frozen as FZ  # noqa: E402

MD = LEAN / "data" / "c2_parts" / "MD"
PARTS = LEAN / "data" / "c2_md_parts"
BLOCK = "MD"
BARRED_A61 = ("md_fdc", "md_peps")                        # A61 (a): recorded whole-file 8.5 HITs, barred under any id / alias / form
PATH_BAN = ("ohs", "sealed", "preread", "external_quarantine", "longbench", ".claude", "jev_output")
BACKUP_DIR = "_backup_finalize_md"
STAMP = "%Y%m%dT%H%M%SZ"


# ---------------------------------------------------------------------------------------------------------------- paths / io
class Paths:
    """Every file the verdict reads (so a test can point them at a copy). Nothing here is written except `qc` (and its backup)."""

    def __init__(self, md=MD, parts=PARTS, gb=None, rtw=None, audit=None, sources_cand=None, denylist=None):
        self.md = Path(md)
        self.parts = Path(parts)
        self.gb = Path(gb) if gb else self.md.parent / "GB"
        self.rtw = Path(rtw) if rtw else self.md.parent / "RTW"
        self.audit = Path(audit) if audit else BUILD / "negtwins" / "stage3" / "POOLED_AUDIT_REPORT.json"
        self.sources_cand = Path(sources_cand) if sources_cand else BUILD / "meta_src" / "SOURCES_CANDIDATES.json"
        self.denylist = Path(denylist) if denylist else BUILD / "meta_src" / "c1_denylist_check.py"
        self.qc = self.md / "qc" / "QC_REPORT.json"
        self.dropped = self.md / "qc" / "dropped_tasks.json"
        self.cand = self.md / "out" / "candidates_c2.jsonl"
        self.rel = self.md / "out" / "candidates_c2.relations.jsonl"
        self.man = self.md / "out" / "MANIFEST.json"
        self.hold = self.md / "out" / "c3_hold_a60.jsonl"
        self.hold_rel = self.md / "out" / "c3_hold_a60.relations.jsonl"


def refuse_path(p) -> str | None:
    s = str(Path(p)).lower()
    for w in PATH_BAN:
        if w in s:
            return f"never-open path ({w}): {p}"
    return c2io.refusal(p)


def rd(p) -> bytes:
    why = refuse_path(p)
    if why:
        raise PermissionError(why)
    return Path(p).read_bytes()


def sha(p) -> str:
    return hashlib.sha256(rd(p)).hexdigest()


def jl(p) -> list:
    """JSONL rows. Lines split on "\\n" ONLY: str.splitlines() also splits on U+2028 / U+2029 / U+0085 / \\x1c-\\x1e / \\f / \\v, which
    JSON allows inside a string, and would cut such a row in two."""
    return [json.loads(x) for x in rd(p).decode("utf-8").split("\n") if x.strip()]


def js(p):
    return json.loads(rd(p).decode("utf-8"))


def load_merge_md():
    """meta_src/merge_md.py loaded under its own name (its directory is not put on sys.path; it only defines functions at import)."""
    spec = importlib.util.spec_from_file_location("merge_md_ro", BUILD / "meta_src" / "merge_md.py")
    mod = importlib.util.module_from_spec(spec)
    sys.modules["merge_md_ro"] = mod
    spec.loader.exec_module(mod)
    return mod


# ---------------------------------------------------------------------------------------------------------------- 1 bars
def bars_problems(mm) -> list:
    """The bars this writer measures against, restated from the pre-registration (A42-D 7.1, 8.2, 8.4; A51). A module whose constant moved
    is a problem: the tool never measures against a loosened bar."""
    want = [(mix_c2.SOURCE_MAX, 0.15, "source share"), (mix_c2.DOMAIN_MAX, 0.20, "domain share"), (mix_c2.META_MIN_ROWS, 8000, "row floor"),
            (tuple(mix_c2.META_TASKS_PER_SOURCE), (40, 80), "tasks per source"), (mix_c2.CARD_FREE_MIN, 0.30, "card-free share"),
            (mix_c2.META_TASK_ROWS_MAX, 200, "rows per task"), (mix_c2.META_DOMAINS_MIN, 8, "domains"), (mix_c2.TWIN_CAP.get(BLOCK), 5000, "twin cap"),
            (mix_c2.BLOCK_CAPS.get(BLOCK), 12000, "block cap"), (mm.CLEAR_CONF, 0.7, "A51 (a) clearly-wrong confidence"),
            (mm.NOISE_MIN_WRONG, 2, "A42-D 8.4 wrong reads that drop a task"), (A60.MIN_IMPLICIT, Fraction(1, 4), "A60 implicit"),
            (A60.MIN_ANTONYM, Fraction(3, 10), "A60 antonym"), (A60.MAX_SYNTACTIC, Fraction(9, 20), "A60 syntactic")]
    return [f"bar changed in code: {name} is {got!r}, pre-registered {exp!r}" for got, exp, name in want if got != exp]


# ---------------------------------------------------------------------------------------------------------------- 2 files
def file_problems(P: Paths, qc: dict, rows: list, rels: list, man: dict) -> tuple[dict, list]:
    p, ids = [], {r["id"] for r in rows}
    got = {c2io.CAND: (sha(P.cand), len(rows)), c2io.REL: (sha(P.rel), len(rels))}
    p += [f"manifest: {x}" for x in c2io.manifest_problems(BLOCK, man, got)]
    p += [f"candidates: {x}" for x in c2io.candidate_problems(BLOCK, rows)]
    if len(ids) != len(rows):
        p.append("duplicate ids")
    tw = {r["id"] for r in rows if (r.get("meta") or {}).get("negtwin")}
    if {x["b"] for x in rels} != tw or len(rels) != len(tw) or any(x["a"] not in ids or x["b"] not in ids for x in rels):
        p.append("relations are not exactly the twin links inside the rows")
    a = qc.get("a60") or {}
    h = a.get("hold") or {}
    hold_rows, hold_rels = jl(P.hold), jl(P.hold_rel)
    for k, f, n in (("rows_sha256", P.hold, len(hold_rows)), ("relations_sha256", P.hold_rel, len(hold_rels))):
        if h.get(k) != sha(f):
            p.append(f"hold file {f.name} differs from its recorded sha")
    if h.get("rows") != len(hold_rows) or h.get("relations") != len(hold_rels):
        p.append(f"hold files hold {len(hold_rows)} rows / {len(hold_rels)} relations, the A60 record says {h.get('rows')} / {h.get('relations')}")
    if {r["id"] for r in hold_rows} & ids:
        p.append("hold rows (never trained in C2) share ids with the candidates")
    if a.get("block_rule_problems") or (a.get("pooled_after") or {}).get("problems"):
        p.append("A60 record carries problems")
    if qc.get("problems"):
        p.append("QC record lists problems")
    shas = {c2io.CAND: {"sha256": got[c2io.CAND][0], "rows": len(rows)}, c2io.REL: {"sha256": got[c2io.REL][0], "rows": len(rels)},
            "MANIFEST.json": {"sha256": sha(P.man)},
            P.hold.name: {"sha256": sha(P.hold), "rows": len(hold_rows)}, P.hold_rel.name: {"sha256": sha(P.hold_rel), "rows": len(hold_rels)}}
    return shas, p


# ---------------------------------------------------------------------------------------------------------------- 4 noise gate
def _gate_input_digest(d: Path) -> str:
    """One digest over the noise-gate inputs of a source part (its rows, MANIFEST, picks, keys, confirmation and every answer file)."""
    files = [d / "rows.jsonl", d / "MANIFEST.json"]
    for sub in ("noise_gate", "noise_gate_orch"):
        g = d / sub
        files += sorted((g / "answers").glob("*.json")) if (g / "answers").is_dir() else []
        files += sorted((g / "key").glob("MD_*.json")) if (g / "key").is_dir() else []
        files += [g / "SEEDED_PICK.json", g / "confirmed.json"]
    h = hashlib.sha256()
    for f in files:
        if f.is_file():
            h.update(f"{f.relative_to(d)}\x00{sha(f)}\n".encode())
    return h.hexdigest()


def noise_gate_check(mm, P: Paths, qc: dict, cand_rows: list, only=None) -> tuple[dict, list, dict]:
    """A51 / A42-D 8.4 re-derived: returns (report, problems, {block source: {tasks_in, dropped, kept}}) for the A51 (c) deviation derivation.
    `only` limits the source parts (tests)."""
    p, rep, dev_in = [], {"per_source": {}}, {}
    old = mm.PARTS
    mm.PARTS = P.parts
    try:
        if not P.parts.is_dir():
            return rep, [f"no source parts folder {P.parts.name}"], dev_in
        names = [d.name for d in sorted(P.parts.iterdir()) if d.is_dir() and not d.name.startswith("_")
                 and not any(w in d.name.lower() for w in PATH_BAN) and (not only or d.name in only)]
        srcs, load_p = mm.load_sources(set(names))
    finally:
        mm.PARTS = old
    p += [f"load: {x}" for x in load_p]
    dropped_file = js(P.dropped)
    per = ((qc.get("gates_run") or {}).get("A42D_8_4_noise_gate") or {}).get("per_source") or {}
    cand_tasks_by_src = defaultdict(set)
    for r in cand_rows:
        cand_tasks_by_src[r["source"]].add(r["meta"]["task_id"])
    file_gate_ids = {t for t, v in dropped_file.items() if isinstance(v, dict) and not v.get("reason")}
    file_schema_ids = {t for t, v in dropped_file.items() if isinstance(v, dict) and v.get("reason")}
    all_flagged, digests = set(), {}
    for name, s in sorted(srcs.items()):
        drop, g = mm.gate_source(name, s, None, True)
        bsrc = next((r["source"] for r in s["rows"]), None)
        tasks_in = {r["meta"]["task_id"] for r in s["rows"]}
        row = {"block_source": bsrc, "status": g.get("status"), "answers": g.get("answers"), "expected": g.get("expected"),
               "unanswered": g.get("unanswered"), "invalid_answers": g.get("invalid_answers"), "tasks_in": len(tasks_in),
               "tasks_read": g.get("tasks_checked"), "tasks_unchecked": g.get("tasks_unchecked"), "tasks_flagged": len(drop),
               "stale_keys_ignored": len(g.get("stale_keys_ignored") or ())}
        digests[name] = _gate_input_digest(s["dir"])
        rep["per_source"][name] = row
        if g.get("status") != "complete":
            p.append(f"noise gate {name}: status {g.get('status')} ({g.get('answers')} of {g.get('expected')} answers)")
            continue
        if g.get("tasks_unchecked") or g.get("tasks_checked") != len(tasks_in):
            p.append(f"noise gate {name}: {len(tasks_in) - (g.get('tasks_checked') or 0)} of {len(tasks_in)} tasks not read")
        if g.get("tasks_in_block") != len(tasks_in):
            p.append(f"noise gate {name}: task count disagrees")
        rec = per.get(name)
        if not rec:
            p.append(f"noise gate {name}: no entry in the QC record")
        else:
            for ko, kn in (("tasks_in", "tasks_in"), ("tasks_read_by_gate", "tasks_read"), ("tasks_dropped_by_gate", "tasks_flagged")):
                if rec.get(ko) != row[kn]:
                    p.append(f"noise gate {name}: the QC record's {ko} {rec.get(ko)} != {row[kn]} re-derived from the answers")
        mine = {t for t in drop}
        if not mine <= file_gate_ids:
            p.append(f"noise gate {name}: {len(mine - file_gate_ids)} flagged tasks are not in dropped_tasks.json")
        recorded_here = {t for t in file_gate_ids if dropped_file[t].get("source") == name}
        if recorded_here != mine:
            p.append(f"noise gate {name}: dropped_tasks.json has {len(recorded_here)} tasks, the answers flag {len(mine)}")
        for t, v in (g.get("dropped") or {}).items():
            if (dropped_file.get(t) or {}).get("wrong") != v["wrong"] or (dropped_file.get(t) or {}).get("read") != v["read"]:
                p.append(f"noise gate {name}: {t} wrong/read counts differ from dropped_tasks.json")
        all_flagged |= mine
        # merge_md's one other whole-task drop: a task whose rows cannot pass the kit schema (dropped_tasks.json "reason"); re-derived here
        sch = {t for t in file_schema_ids if dropped_file[t].get("source") == bsrc}
        for t in sorted(sch):
            p += [f"noise gate {name}: {x}" for x in schema_drop_problems(mm, s, t, dropped_file[t])]
        row["tasks_schema_dropped"] = len(sch)
        kept = cand_tasks_by_src.get(bsrc, set())
        if kept & (mine | sch):
            p.append(f"noise gate {name}: {len(kept & (mine | sch))} dropped tasks are in the candidates")
        survive = tasks_in - mine - sch
        if not kept <= survive:
            p.append(f"noise gate {name}: {len(kept - survive)} candidate tasks are not source tasks that survive the drops")
        row["tasks_kept_in_candidates"] = len(kept)
        if kept != survive:
            p.append(f"noise gate {name}: {len(survive - kept)} surviving tasks are missing from the candidates (removed outside the gate)")
        dev_in[bsrc] = {"source": name, "tasks_in": len(tasks_in), "dropped": len(mine), "schema_dropped": len(sch), "kept": len(kept)}
    if not only:
        if all_flagged != file_gate_ids:
            p.append(f"dropped_tasks.json holds {len(file_gate_ids - all_flagged)} gate-dropped tasks the answers do not flag")
        if set(per) != set(srcs):
            p.append(f"the QC record's noise-gate sources {sorted(set(per) ^ set(srcs))} differ from the source parts")
        if (qc["gates_run"]["A42D_8_4_noise_gate"].get("tasks_dropped_total")) != len(dropped_file):
            p.append("the QC record's tasks_dropped_total != dropped_tasks.json")
    allcand = set().union(*cand_tasks_by_src.values()) if cand_tasks_by_src else set()
    if allcand & (all_flagged | file_schema_ids):
        p.append(f"{len(allcand & (all_flagged | file_schema_ids))} dropped tasks (gate or schema) are in the candidates")
    rep.update({"tasks_flagged_total": len(all_flagged), "dropped_tasks_json_sha256": sha(P.dropped), "dropped_tasks_json_entries": len(dropped_file),
                "rule": f"drop a task with >= {mm.NOISE_MIN_WRONG} picked rows whose blind answer differs from gold (confidence >= {mm.CLEAR_CONF}); twin rows not counted",
                "inputs_sha256": hashlib.sha256(json.dumps(digests, sort_keys=True).encode()).hexdigest(), "inputs_sha256_by_source": digests})
    return rep, p, dev_in


def schema_drop_problems(mm, s: dict, task: str, entry: dict) -> list:
    """The schema drop of dropped_tasks.json re-derived: the task's rows, mapped by merge_md.c2_schema on copies, still fail the kit
    validate_row (meta.licence excepted) with exactly the recorded reason; the recorded row count is the task's."""
    from c2_kit import rows as KR
    rr = [copy.deepcopy(r) for r in s["rows"] if r["meta"]["task_id"] == task]
    if not rr:
        return [f"schema-dropped task {task} is not a task of the source"]
    idmap, msgs = {}, set()
    for r in rr:
        mm.c2_schema(r, idmap)
        msgs |= {m for m in KR.validate_row(r) if m != "meta.licence"}
    out = []
    if not msgs:
        out.append(f"schema-dropped task {task} passes the kit schema: it should not have been dropped")
    elif entry.get("reason") != "schema: " + "; ".join(sorted(msgs)):
        out.append(f"schema-dropped task {task}: reason {entry.get('reason')!r} != {'schema: ' + '; '.join(sorted(msgs))!r}")
    if entry.get("rows") != len(rr):
        out.append(f"schema-dropped task {task}: {len(rr)} rows, dropped_tasks.json says {entry.get('rows')}")
    return out


def derived_deviations(dev_in: dict) -> list:
    """A51 (c): the sources under the 40-task floor after the gate, derived from the re-derivation (not from the record)."""
    out = []
    for bsrc, v in sorted(dev_in.items()):
        if v["kept"] < mix_c2.META_TASKS_PER_SOURCE[0] and v["dropped"] > 0 and v["tasks_in"] - v["dropped"] == v["kept"]:
            out.append({"ruling": "A51 (c)", "source": v["source"], "block_source": bsrc, "tasks_in": v["tasks_in"], "tasks_dropped_by_gate": v["dropped"],
                        "tasks_kept": v["kept"], "floor": mix_c2.META_TASKS_PER_SOURCE[0],
                        "note": "keeps its surviving tasks; the shortfall lowers the block total and is not refilled; reported in the training-GO request"})
    return out


# ---------------------------------------------------------------------------------------------------------------- 5 twins
def twin_check(rows: list, pats: list, pairs: dict, dropped_patterns: set) -> tuple[dict, list]:
    by = {r["id"]: r for r in rows}
    pm = {x.pid: x for x in pats}
    tw = [r for r in rows if (r.get("meta") or {}).get("negtwin")]
    p, bad = [], Counter()
    pairs_ok = []
    for r in tw:
        n = r["meta"]["negtwin"]
        pat = pm.get(n.get("pattern"))
        b = by.get(n.get("base_id"))
        if pat is None:
            bad["pattern not in the frozen trained catalogue"] += 1
            continue
        if n["pattern"] in dropped_patterns:
            bad["pattern dropped by the pooled Sonnet/Opus audit"] += 1
        if b is None:
            bad["no base row"] += 1
            continue
        pairs_ok.append((b, r))
        if r.get("role") != pat.relation or n.get("op") != pat.op or n.get("kind") != pat.kind:
            bad["role / op / kind differ from the pattern"] += 1
        sb, st = C.split_instruction(b["instructions"]), C.split_instruction(r["instructions"])
        if not sb or not st:
            bad["instruction does not split into preamble + one-question core"] += 1
            continue
        bc, tc = sb[1], st[1]
        ok, probs, _ = K.check_pair(bc, tc, pat, pairs.get(pat.pair) if pat.pair else None)
        if not ok:
            bad["check_pair: " + (probs[0][:60] if probs else "?")] += 1
        if K.bad_edit_site(bc, tc):
            bad["edit site (A48 h iv)"] += 1
        if C.a48h_class(pat):
            bad["A48 h pattern class"] += 1
        if C.MODAL_SPLIT.search(tc) and not C.MODAL_SPLIT.search(bc):
            bad["A48 h modal scope"] += 1
    gtw = K.g_tw(pairs_ok)
    if len(pairs_ok) != len(tw):
        p.append(f"G-TW: {len(pairs_ok)}/{len(tw)} twins with a known pattern and a base")
    if not gtw["pass"]:
        p.append(f"G-TW: {gtw['violations']} violations over {gtw['n_pairs']} pairs")
    p += [f"twin program check: {n} twins: {k}" for k, n in sorted(bad.items())]
    rep = {"twins": len(tw), "g_tw": {k: gtw[k] for k in ("n_pairs", "violations", "pass")}, "program_check_failures": dict(bad),
           "patterns_used": len({r["meta"]["negtwin"].get("pattern") for r in tw}), "audit_dropped_patterns": len(dropped_patterns),
           "by_role": dict(Counter(r["role"] for r in tw))}
    return rep, p


def audit_check(P: Paths, qc: dict, n_twins: int) -> tuple[set, dict, list]:
    p = []
    a = js(P.audit)
    dropped = set(a.get("patterns_dropped") or [])
    if a.get("n_patterns_dropped") != len(dropped):
        p.append("pooled audit report: n_patterns_dropped != the list")
    fin = (a.get("final_twins") or {}).get(BLOCK)
    if fin != n_twins:
        p.append(f"pooled audit report names {fin} MD twins, the file has {n_twins}")
    rec = qc.get("negtwin_audit") or {}
    if rec.get("final_twins") != n_twins:
        p.append(f"QC record negtwin_audit.final_twins {rec.get('final_twins')} != {n_twins}")
    if rec.get("patterns_dropped") != len(dropped):
        p.append(f"QC record negtwin_audit.patterns_dropped {rec.get('patterns_dropped')} != the report's {len(dropped)}")
    if a.get("dry_run") is not False:
        p.append("pooled audit report is a dry run")
    return dropped, {"sha256": sha(P.audit), "patterns_dropped": len(dropped), "final_twins_MD": fin}, p


# ---------------------------------------------------------------------------------------------------------------- 6 pooled shares
def pooled_check(P: Paths, qc: dict, md_rows: list, audit: dict, gb_rows=None, rtw_rows=None) -> tuple[dict, list]:
    gb = jl(P.gb / "out" / "candidates_c2.jsonl") if gb_rows is None else gb_rows
    rtw = jl(P.rtw / "out" / "candidates_c2.jsonl") if (rtw_rows is None and (P.rtw / "out" / "candidates_c2.jsonl").is_file()) else (rtw_rows or [])
    by_block, p = {}, []
    for name, rows in (("GB", gb), ("MD", md_rows), ("RTW", rtw)):
        c = Counter()
        for r in rows:
            n = (r.get("meta") or {}).get("negtwin")
            if isinstance(n, dict) and r.get("role") == "complement":
                c[str(n.get("kind"))] += 1
        by_block[name] = c
    pooled = Counter()
    for c in by_block.values():
        pooled.update(c)
    unknown = {k: v for k, v in pooled.items() if k not in A60.KINDS}
    if unknown:
        p.append(f"A60: complement twins without a known kind {unknown}")
    rep = A60.report({k: pooled.get(k, 0) for k in A60.KINDS}, vacuous_ok=True)
    p += [f"A60 pooled spec 3.18 shares: {x}" for x in rep["problems"]]
    a60 = qc.get("a60") or {}
    for label, got, want in (("QC record a60.pooled_after.by_kind", (a60.get("pooled_after") or {}).get("by_kind"), rep["by_kind"]),
                             ("pooled audit report pooled_spec_3_18_shares.by_kind", (audit.get("pooled_spec_3_18_shares") or {}).get("by_kind"), rep["by_kind"]),
                             ("QC record a60.block.complement_after_by_kind", (a60.get("block") or {}).get("complement_after_by_kind"),
                              {k: v for k, v in dict(by_block["MD"]).items()})):
        if got is None or {k: int(v) for k, v in got.items()} != {k: int(v) for k, v in want.items()}:
            p.append(f"{label} {got} != {want} recomputed from the files")
    rep["by_block"] = {b: dict(c) for b, c in by_block.items()}
    rep["inputs_sha256"] = {"GB": sha(P.gb / "out" / "candidates_c2.jsonl"), "MD": sha(P.cand)}
    if (P.rtw / "out" / "candidates_c2.jsonl").is_file():
        rep["inputs_sha256"]["RTW"] = sha(P.rtw / "out" / "candidates_c2.jsonl")
    return rep, p


# ---------------------------------------------------------------------------------------------------------------- 7 sources
def lic_name(x) -> str:
    return str(x.get("name") if isinstance(x, dict) else x)


def sources_check(mm, P: Paths, qc: dict, rows: list, denylist_out: str | None = None, only=None) -> tuple[dict, list]:
    p, rep = [], {}
    rows_b = [dict(r, _block=BLOCK) for r in rows]
    gm, gp = mix_c2.gated_membership(rows_b)
    p += [f"8.5 membership: {x}" for x in gp]
    gated = set(gm.get("sources", ()))
    rep["gated_sources"] = len(gated)
    bar = sorted(set(BARRED_A61) & gated)
    if bar:
        p.append(f"A61-barred sources in the block: {bar}")
    src_all = {r["source"] for r in rows}
    if any(b.split("_", 1)[1] in s for s in src_all for b in BARRED_A61):
        p.append("a row source names an A61-barred source")
    want_sha = mix_c2.BINDING_INPUTS["md"][0][1]                   # A61 (a): the closed list of binding inputs, each with its logged sha256
    got_sha = sha(P.sources_cand)
    if got_sha != want_sha:
        p.append("8.5 binding input SOURCES_CANDIDATES.json differs from the ruling's sha256")
    rep["binding_input_sha256"] = {"SOURCES_CANDIDATES.json": got_sha}
    # licence: the part MANIFEST is the source of truth; rows and the record must carry it
    qlic = ((qc.get("gates_run") or {}).get("A42D_8_3_licence_and_name_checks_recorded_by_the_mappers") or {}).get("licence") or {}
    by_src = defaultdict(list)
    for r in rows:
        by_src[r["source"]].append(r)
    lic = {}
    for d in sorted(P.parts.iterdir()) if P.parts.is_dir() else ():
        if not d.is_dir() or d.name.startswith("_") or any(w in d.name.lower() for w in PATH_BAN) or (only and d.name not in only):
            continue
        m = js(d / "MANIFEST.json")
        lic[d.name] = m.get("licence")
        if qlic.get(d.name) != m.get("licence"):
            p.append(f"licence of {d.name}: the QC record's differs from the part MANIFEST's")
        bs = next((s for s in by_src if s in (f"c2_{d.name}", f"c2_md_{d.name}")), None)
        if bs is None:
            p.append(f"source part {d.name} has no rows in the block")
            continue
        want = lic_name(m.get("licence"))
        bad = sum(1 for r in by_src[bs] if not str((r.get("meta") or {}).get("licence") or "").startswith(want))
        if not want or want == "None" or bad:
            p.append(f"licence: {bad} rows of {bs} do not carry the part MANIFEST licence {want!r}")
    if not only and set(by_src) != {next((s for s in by_src if s in (f"c2_{d}", f"c2_md_{d}")), None) for d in lic}:
        p.append("the block's sources are not exactly the 11 source parts")
    # kit schema on every row, meta.licence excepted (as merge_md's own check)
    from c2_kit import rows as KR
    sc = Counter()
    for r in rows:
        for x in KR.validate_row(r):
            if x != "meta.licence":
                sc[x] += 1
    rep["validate_row_failures"] = dict(sc)
    if sc:
        p.append(f"kit validate_row: {sum(sc.values())} problems, e.g. {sorted(sc)[:3]}")
    # deny-list / C1 name script (clear text; it reads nothing sealed)
    out = denylist_out if denylist_out is not None else run_denylist(P)
    seen = {}
    for line in str(out).splitlines():
        a = line.split(None, 2)
        if len(a) >= 2:
            seen[a[0]] = (a[1], a[2] if len(a) > 2 else "")
    dl = {}
    for g in sorted(gated):
        v = seen.get(g)
        if v is None:
            p.append(f"deny-list script has no line for {g}")
        elif v[0] == "CLEAR":
            dl[g] = "CLEAR"
        elif v[0] == "OVERLAP" and {x.strip() for x in v[1].split(";")} == {"c1:github"}:
            dl[g] = "OVERLAP c1:github only (platform word in the licence-page host; A16 a: never a hit alone)"
        else:
            dl[g] = f"OVERLAP {v[1]}"
            p.append(f"deny-list script: {g} {v[0]} {v[1]}")
    rep["denylist"] = dl
    rep["licence_by_part"] = lic
    return rep, p


def run_denylist(P: Paths) -> str:
    r = subprocess.run([sys.executable, "-B", str(P.denylist)], cwd=str(BUILD), capture_output=True, text=True, timeout=300)
    if r.returncode != 0:
        raise RuntimeError(f"deny-list script exit {r.returncode}")
    return r.stdout


# ---------------------------------------------------------------------------------------------------------------- verdict
def live_caps(rows: list, rep: dict) -> dict:
    n = len(rows)
    sc, dc = Counter(r["source"] for r in rows), Counter(mix_c2.dom_of(r) for r in rows)
    free = {s: round(sum(1 for r in rows if r["source"] == s and not str(r.get("card") or "").strip()) / c, 4) for s, c in sc.items()}
    return {"source_max": mix_c2.SOURCE_MAX, "domain_max": mix_c2.DOMAIN_MAX, "block_rows": n, "twins": rep.get("twins"),
            "source_shares": {s: round(c / n, 4) for s, c in sorted(sc.items())}, "domain_shares": {d: round(c / n, 4) for d, c in sorted(dc.items())},
            "n_domains": len(dc), "card_free": dict(sorted(free.items())), "tasks_per_source": rep.get("tasks_per_source"),
            "note": "recomputed from the candidates on disk by finalize_md.py; the merge-time block moved to superseded_at_finalize"}


def verdict(P: Paths | None = None, denylist_out: str | None = None, only=None, now=None) -> tuple[dict, list]:
    P = P or Paths()
    mm = load_merge_md()
    qc = js(P.qc)
    rows, rels, man = jl(P.cand), jl(P.rel), js(P.man)
    out = {"qc_sha256_read": sha(P.qc), "rows": len(rows), "relations": len(rels)}
    p = bars_problems(mm)
    shas, fp = file_problems(P, qc, rows, rels, man)
    p += fp
    out["files"] = shas
    ng, np_, dev_in = noise_gate_check(mm, P, qc, rows, only=only)
    out["noise_gate"], p = ng, p + np_
    devs = derived_deviations(dev_in)
    out["deviations"] = devs
    old = [{k: d.get(k) for k in ("ruling", "block_source", "tasks_in", "tasks_dropped_by_gate", "tasks_kept")} for d in (qc.get("deviations") or [])]
    new = [{k: d.get(k) for k in ("ruling", "block_source", "tasks_in", "tasks_dropped_by_gate", "tasks_kept")} for d in devs]
    if not only and old != new:
        p.append("the QC record's A51 (c) deviations differ from those derived from the answers")
    rep, bp = mix_c2.block_rules(BLOCK, rows, loaded=True, deviations=devs)
    p += bp
    out["block_rules"] = rep
    pats, pairs = FZ.load_trained()
    dropped_pat, arep, ap = audit_check(P, qc, sum(1 for r in rows if (r.get("meta") or {}).get("negtwin")))
    p += ap
    out["pooled_audit"] = arep
    tw, tp = twin_check(rows, pats, pairs, dropped_pat)
    out["twins"], p = tw, p + tp
    audit = js(P.audit)
    pl, pp = pooled_check(P, qc, rows, audit)
    out["pooled_A60"], p = pl, p + pp
    sr, sp = sources_check(mm, P, qc, rows, denylist_out, only=only)
    out["sources"], p = sr, p + sp
    out["live_caps"] = live_caps(rows, rep)
    out["problems"] = p
    out["would_pass"] = not p
    if not p:                                                    # 8: the new record, in memory, against the mixer's own admission
        rec = build_record(qc, out, now or utc_now())
        files = {c2io.CAND: P.cand, c2io.REL: P.rel}
        bind = mx.qc_binding(rec, files)
        adm = mix_c2.admission(BLOCK, rec, bind)
        out["admission_simulated"] = adm
        if adm:
            p += [f"simulated admission: {x}" for x in adm]
            out["would_pass"] = False
    return out, p


# ---------------------------------------------------------------------------------------------------------------- record
PENDING = [
    "G13 decontamination on the candidates (A42-D 8.6; `g13_c2.py candidates --block MD`, orchestrator batch), INCLUDING the OHS-AC path "
    "(A64 g: ohsac_hash, ohsac_rows, ohsac_gtpl, 0 hits after drops; the run executes it with no switch): drops are whole units",
    "C1 crowd selection for MD (c2_select.py select --fam MD --exclude-ids <complete G13 log>; target 12,000, short is allowed)",
    "A61 (e 5): the final all-block G13 (g13_c2.py final) for every block incl. MD, against di03_public and di_src_splits (0 hits after drops)",
    "A61 (f) / A42-D 8.5: the single final-mix source-name check, orchestrator only, once (source_name_check.py --exports all on the membership "
    "list's binding inputs, meta_src/SOURCES_CANDIDATES.json for the 11 md_* ids); every md_* id in the mix needs a PASS line, a HIT or an "
    "incomplete check is followed by mix_c2.py --remove-sources (drops only); preflight_c2.py's a61_85 check enforces it",
]


def utc_now() -> str:
    return datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def build_record(qc: dict, v: dict, now: str) -> dict:
    rec = copy.deepcopy(qc)
    gr = rec.setdefault("gates_run", {})
    sup = {"why": "merge-time blocks that no longer describe the file: the record now says pass=true on the current candidates (10,491 rows), so "
                  "the old counts are kept here, unchanged, and replaced above by the live re-derivation",
           "stage": rec.get("stage"), "note": rec.get("note"), "gates_run.A42D_8_2_caps": gr.get("A42D_8_2_caps"),
           "negtwin_gates": rec.pop("negtwin_gates", None)}
    rec["superseded_at_finalize"] = sup
    gr["A42D_8_2_caps"] = v["live_caps"]
    gr["A51_noise_gate_rederived"] = v["noise_gate"]
    gr["twin_program_checks_rederived"] = v["twins"] | {"pooled_audit": v["pooled_audit"]}
    gr["A60_pooled_spec_3_18_rederived"] = v["pooled_A60"]
    gr["A42D_8_3_8_5_rederived"] = {k: v["sources"][k] for k in ("gated_sources", "binding_input_sha256", "denylist", "licence_by_part", "validate_row_failures")}
    gr["block_rules_rederived"] = v["block_rules"]
    rec["negtwin_gates"] = {"tool": "finalize_md.py (recomputed on the current file)", "twins": v["twins"]["twins"], "g_tw": v["twins"]["g_tw"], "utc": now,
                            "superseded_merge_time_record": "superseded_at_finalize.negtwin_gates"}
    rec["deviations"] = v["deviations"]
    rec["pass"], rec["passed_utc"], rec["fix_iterations"] = True, now, 0
    rec["problems"] = []
    rec["stage"] = "final non-G13 gates passed (finalize_md.py, Ruling A66 a); G13 incl. OHS-AC, crowd selection and the A61 final-mix checks still pending"
    rec["note"] = ("pass=true records the gates in gates_run, negtwin_gates, negtwin_audit and a60, every one re-derived from the files on disk by "
                   "finalize_md.py (A66 a); none is waived and no bar moved. G13, the crowd selection and the final-mix 8.5 run are in gates_pending.")
    rec["gates_pending"] = list(PENDING)
    rec["finalize"] = {"tool": "zed_orch/md_final/finalize_md.py", "ruling": "A66 (a)", "utc": now,
                       "verdict": {k: v[k] for k in ("rows", "relations", "files")} | {"twins": v["twins"]["twins"], "g_tw": v["twins"]["g_tw"]}}
    rec["files"] = copy.deepcopy(v["files"])
    return rec


def atomic_write(path: Path, rec: dict) -> None:
    tmp = path.with_name(path.name + ".tmp")
    tmp.write_text(json.dumps(rec, indent=1) + "\n", encoding="utf-8")
    os.replace(tmp, path)


def backup(P: Paths, stamp: str | None = None) -> Path:
    """A verified copy of QC_REPORT.json in qc/_backup_finalize_md/<UTC>/ (never overwrites a backup)."""
    d = P.qc.parent / BACKUP_DIR / (stamp or datetime.datetime.now(datetime.timezone.utc).strftime(STAMP))
    d.mkdir(parents=True, exist_ok=False)
    dst = d / P.qc.name
    shutil.copy2(P.qc, dst)
    if sha(dst) != sha(P.qc):
        raise RuntimeError("backup differs from the record")
    return dst


def write(P: Paths, v: dict, now: str | None = None) -> Path:
    """Backup first, then replace the record; the only writes are <qc>/_backup_finalize_md/<UTC>/QC_REPORT.json and QC_REPORT.json."""
    if sha(P.qc) != v["qc_sha256_read"]:
        raise RuntimeError("QC_REPORT.json changed since the verdict was computed")
    qc = js(P.qc)
    if qc.get("pass") is True:
        raise RuntimeError("QC_REPORT.json already has pass=true")
    bk = backup(P)
    rec = build_record(qc, v, now or utc_now())
    atomic_write(P.qc, rec)
    after = js(P.qc)
    files = {c2io.CAND: P.cand, c2io.REL: P.rel}
    bad = mx.qc_binding(after, files) + mix_c2.admission(BLOCK, after, mx.qc_binding(after, files))
    if bad:
        shutil.copy2(bk, P.qc)
        raise RuntimeError(f"written record fails admission, backup restored: {bad[:3]}")
    return bk


def main(argv=None, P: Paths | None = None, denylist_out: str | None = None):
    ap = argparse.ArgumentParser()
    ap.add_argument("--write", action="store_true")
    a = ap.parse_args(argv)
    P = P or Paths()
    v, p = verdict(P, denylist_out=denylist_out)
    print(json.dumps(v, indent=1))
    if not a.write:
        return 0 if not p else 1
    if p:
        print("REFUSED: problems above")
        return 2
    bk = write(P, v)
    print("written", P.qc, "backup", bk)
    return 0


if __name__ == "__main__":
    sys.exit(main())
