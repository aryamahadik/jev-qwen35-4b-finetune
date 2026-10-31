"""mixdev_c2.py: the writer of the merged C2 mixdev and the predict-job manifests of the C2 dev sets
(C2_DATA_SPEC 7.1, 9.1; PREREG A37 g, A39 h, A53, A62, A68 and the C2 odds analysis lane P5). CPU only; no network; no G13.

What it builds (all STAGED; nothing is written into data/):
  staged/mixdev/c2_mixdev.jsonl              the merged mixdev the gate (split "c2_mixdev"), the snapshot reports and the temperature
                                             fit read: 150 rows per TRAINED family (entered families only; whole units; no refill),
                                             plus the existing S5 mixdev of F5 / F6 / F11 (spec 7.1: "plus F5/F6/F11 existing S5
                                             mixdev"). F4 (a trained carry-over pool) follows the 150 rule. Rows are taken as
                                             generated: no edit, no relabel, no re-order inside a family.
  staged/mixdev/c2_mixdev_report_only.jsonl  report-only reads, never in the learning check (a): T27's mixdev (A62 b: T27 moves
                                             to C3) and the mixdev of every entered block that has one (A39 h: GB 1,650 rows, SB5).
  staged/mixdev/*.sha256                     sha256sum -c lines
  staged/mixdev/MIXDEV_BUILD_REPORT.json     counts, shas, every input with its sha256, the entry decision, problems.
  staged/mixdev/manifests/predict_*.json     predict-job manifests: c2_mixdev, c2_mixdev_report, c2_transfer_dev, c2_t37b_dev (when
                                             staged) and the G-proxy (pab_gproxy), plus predict_jobs_index.json (the one gate job).

Which families count as "trained" (entered): by default the same test mix_c2 uses (mix_c2.admission on the QC record, the files
on disk and the cutoff). The set can be pinned instead: --families T01 T06 ... or --entered-from <mix dry-run JSON holding
entry.entered>. The mix tools decide the final entered set; rerun this builder after that decision if it differs.

A new data/ dev file makes every G13 candidates log stale (g13_c2.py lists the dev files it scanned). This tool refuses an
--out-dir under data/. Installing the staged file into data/ is the orchestrator's step, in the one code-edit window after the
G13 capture batch's inputs are final (then one g13_c2.py refresh-dev). This tool never runs g13_c2.py or decontam_g13.py.

  mixdev_c2.py build [--families ...] [--entered-from J] [--per-family 150] [--out-dir staged/mixdev] [--write]
  mixdev_c2.py manifests [--out-dir staged/mixdev]      (re-derives the manifests from the staged files; run again when
                                                         T37b-dev is staged)
  mixdev_c2.py verify [--out-dir staged/mixdev]         (staged files unchanged; data/ copy, if installed, equal to staged)
Exit 0 = ok; 2 = problems (nothing written by build).

Run from lean/c2_build:  ../../.venv/bin/python -B mixdev_c2.py build --write      (HF_HUB_OFFLINE=1)
"""
from __future__ import annotations

import argparse
import hashlib
import json
import sys
import time
from collections import Counter, defaultdict
from pathlib import Path

sys.dont_write_bytecode = True
HERE = Path(__file__).resolve().parent          # lean/c2_build
LEAN = HERE.parent
for _p in (str(HERE), str(LEAN)):
    if _p not in sys.path:
        sys.path.insert(0, _p)

import c2io  # noqa: E402
import gate_c2 as gc  # noqa: E402  (split names, the C1 / C2 read names, SPLITS9: the gate's own constants)
import mix_c2  # noqa: E402  (admission: the same entry test as the mix)
import snap_monitor_c2 as sm  # noqa: E402  (BASE, REV, LAYOUT, VMS)
from mixio import h64, sha256_file  # noqa: E402

PER_FAMILY = 150                                  # spec 7.1
SEED = c2io.SEED
STAGED = HERE / "staged" / "mixdev"
MAIN, REPORT_ONLY = "c2_mixdev.jsonl", "c2_mixdev_report_only.jsonl"
REPORT_SPLIT = "c2_mixdev_report"                 # split name of the report-only reads (not a gate input)
BUILD_REPORT = "MIXDEV_BUILD_REPORT.json"
GPROXY_SPLIT = "pab_gproxy"
GPROXY_DIR = LEAN / "data" / "c2_gproxy"

TRAINED_PROGRAM = tuple(c2io.PROGRAM)             # the 17 program families of spec 2.1 (T27 leaves by A62; T35 has no data yet)
REPORT_ONLY_FAMILIES = ("T27",)                   # A62 (b): T27's mixdev leaves the C2 mixdev (report-only read)
CARRY_FULL = ("F5", "F6", "F11")                  # spec 7.1: their existing S5 mixdev is taken whole
CARRY_CAPPED = ("F4",)                            # a trained carry-over pool without a spec 7.1 line: the 150 rule applies
REPORT_BLOCKS = tuple(c2io.BLOCK_TARGETS)         # A39 h: a block's own mixdev is report-only and never trained
OWN_DEV_FAMILIES = tuple(c2io.NEW_FAMILIES) + tuple(c2io.POST_FREEZE)   # PREREG 4.4 own dev split: pooled separately (9.3 term 3)
SCOPE = TRAINED_PROGRAM + CARRY_FULL + CARRY_CAPPED + REPORT_BLOCKS
KEEP_KEYS = ("id", "group_id", "call_id", "qtype", "gold", "meta")


class Problem(Exception):
    pass


# ---------------------------------------------------------------------------------------------------------------- layout
def fam_paths(fam: str, lean: Path = LEAN) -> dict:
    """The files of one family. Same layout as c2io.fam_files (a test checks the two agree), with the lean root injectable."""
    d = Path(lean) / "data" / "c2_parts" / fam
    if fam in c2io.CARRY:
        o = Path(lean) / "c_src" / fam / "out"
        return {"mixdev": o / "mixdev_S5.jsonl", "cand": o / "candidates_r1.jsonl", "rel": o / "candidates_r1.relations.jsonl",
                "manifest": o / "MANIFEST.json", "qc": d / "qc" / c2io.QC, "layout": "round-1 (carry-over)"}
    o = d / "out"
    return {"mixdev": o / "mixdev_S5.jsonl", "cand": o / c2io.CAND, "rel": o / c2io.REL, "manifest": o / c2io.MAN,
            "qc": d / "qc" / c2io.QC, "layout": "c2"}


def rel(p, lean: Path = LEAN) -> str:
    p = Path(p)
    try:
        return p.resolve().relative_to(Path(lean).resolve()).as_posix()
    except ValueError:
        return p.as_posix()


# ----------------------------------------------------------------------------------------------------------------- entry
def admission_why(ilog, fam: str, lean: Path = LEAN) -> list[str]:
    """Why `fam` would not enter the mix (mix_c2.admission on the same inputs as mix_c2.admit_blocks; [] = it enters)."""
    f = fam_paths(fam, lean)
    if not f["cand"].exists():
        return ["no candidates on disk"]
    qc = ilog.json(f["qc"]) if f["qc"].exists() else None
    files = {f["cand"].name: f["cand"]} | ({f["rel"].name: f["rel"]} if f["rel"].exists() else {})
    binding = mix_c2.mx.qc_binding(qc, files) if isinstance(qc, dict) else []
    return mix_c2.admission(fam, qc, binding)


def entered_set(ilog, lean: Path = LEAN, families=None, entered_from=None) -> tuple[list[str], dict, dict]:
    """(entered blocks in SCOPE order, {left-out block: [why]}, source record). Priority: --families, --entered-from, admission."""
    if families:
        bad = sorted(set(families) - set(SCOPE) - set(REPORT_ONLY_FAMILIES))
        if bad:
            raise Problem(f"--families: not a C2 mixdev block: {bad}")
        return [b for b in SCOPE if b in families], {}, {"source": "explicit --families", "families": sorted(families)}
    if entered_from:
        p = ilog.check(entered_from)
        d = ilog.json(p)
        ent = (d.get("entry") or {}).get("entered") if isinstance(d, dict) else None
        ent = ent if ent is not None else (d.get("entered") if isinstance(d, dict) else None)
        if not isinstance(ent, list):
            raise Problem(f"--entered-from {p}: no entry.entered list")
        left = (d.get("entry") or {}).get("left_out") or d.get("left_out") or {}
        return ([b for b in SCOPE if b in ent], {b: v for b, v in left.items() if b in SCOPE},
                {"source": "mix report", "file": rel(p, lean), "sha256": sha256_file(p)})
    entered, left = [], {}
    for b in SCOPE:
        why = admission_why(ilog, b, lean)
        (left.__setitem__(b, why) if why else entered.append(b))
    return entered, left, {"source": "mix_c2.admission on the QC records and files on disk now"}


# ----------------------------------------------------------------------------------------------------------- row checks
def row_problems(fam: str, rows: list[dict]) -> list[str]:
    """Hard checks of one family's mixdev rows (the form gate_dev.score and gate_c2.split_rows need, spec 7.1: S5, never trained)."""
    out, seen = [], set()
    kinds = Counter()
    for i, r in enumerate(rows):
        w = f"{fam} row {i} ({r.get('id')!r})"
        if not isinstance(r, dict):
            out.append(f"{w}: not an object")
            continue
        miss = [k for k in ("id", "group_id", "call_id", "qtype", "gold", "meta") if k not in r]
        if miss or not isinstance(r["meta"], dict):
            out.append(f"{w}: missing {miss or ['meta object']}")
            continue
        if r["id"] in seen:
            kinds["duplicate id"] += 1
        seen.add(r["id"])
        priv = [k for k in r if str(k).startswith("_")] + [k for k in r["meta"] if str(k).startswith("_")]
        if priv:
            kinds["private key"] += 1
        m = r["meta"]
        if m.get("family") != fam:
            kinds[f"meta.family is {m.get('family')!r}, not {fam}"] += 1
        if m.get("sampler") != "S5" and not m.get("dev_only"):
            kinds["not an S5 / dev_only row"] += 1
        if r["qtype"] == "noul":
            if not (isinstance(r["gold"], int) and not isinstance(r["gold"], bool) and r["gold"] in (0, 1)):
                kinds["noul gold is not 0 / 1"] += 1
        elif r["qtype"] == "choice":
            o = r.get("options")
            if not (isinstance(o, list) and len(o) >= 2 and all(isinstance(x, str) for x in o) and r["gold"] in o):
                kinds["choice gold is not one of the options"] += 1
        else:
            kinds[f"qtype {r['qtype']!r}"] += 1
    out += [f"{fam}: {n} rows: {k}" for k, n in sorted(kinds.items())]
    return out


def disjoint_problems(fam: str, rows: list[dict], cand: list[dict]) -> list[str]:
    """No mixdev id, group_id or call_id may also be a candidate's (spec 7.1: never trained)."""
    out = []
    for key in ("id", "group_id", "call_id"):
        a, b = {r[key] for r in rows if key in r}, {r[key] for r in cand if key in r}
        if a & b:
            out.append(f"{fam}: {len(a & b)} {key}(s) are also candidate {key}s, e.g. {sorted(a & b)[:2]}")
    return out


def recorded_sha_problems(fam: str, path: Path, qc: dict | None, manifest: dict | None) -> tuple[list[str], dict]:
    """The mixdev file must equal the sha256 its QC record / MANIFEST give (a stale record after a rebuild is a problem).
    Carry-over pools record it in other shapes: a recorded sha is compared when one is found, else the check says so."""
    disk = sha256_file(path)
    got = {}
    for label, d in (("qc", (qc or {}).get("mixdev")), ("manifest", (manifest or {}).get("mixdev"))):
        s = _find_sha(d)
        if s:
            got[label] = s
    if not got and isinstance(manifest, dict):
        s = _find_sha(manifest, deep=True)
        if s:
            got["manifest"] = s
    probs = [f"{fam}: mixdev file sha256 {disk[:12]} differs from the {k} record {v[:12]} (stale record after a rebuild)"
             for k, v in got.items() if not disk.startswith(v)]
    return probs, {"disk": disk, **{f"{k}_record": v for k, v in got.items()}, "recorded": bool(got)}


def _find_sha(d, deep=False):
    """The sha256 recorded for mixdev_S5.jsonl inside a QC / MANIFEST fragment ({'mixdev_S5.jsonl': {'sha256': ..}} or
    {'sha256': ..}); deep: search the whole object for a key naming mixdev_S5.jsonl without sidecar / relations / pre_ markers."""
    if isinstance(d, dict):
        if isinstance(d.get("mixdev_S5.jsonl"), dict) and isinstance(d["mixdev_S5.jsonl"].get("sha256"), str):
            return d["mixdev_S5.jsonl"]["sha256"]
        if not deep and isinstance(d.get("sha256"), str):
            return d["sha256"]
        if deep:
            for k, v in d.items():
                if isinstance(k, str) and "mixdev_S5.jsonl" in k and not any(x in k for x in ("relations", "sidecar", "qc_side", "pre_")):
                    if isinstance(v, dict) and isinstance(v.get("sha256"), str):
                        return v["sha256"]
                r = _find_sha(v, deep=True) if isinstance(v, (dict, list)) else None
                if r:
                    return r
    elif isinstance(d, list) and deep:
        for v in d:
            r = _find_sha(v, deep=True)
            if r:
                return r
    return None


# --------------------------------------------------------------------------------------------------------------- selection
def components(rows: list[dict]) -> dict[str, list[int]]:
    """Whole-unit components: rows tied by a shared group_id or call_id (a unit is never split). {representative: row indices};
    the representative is the smallest row id, so the key does not depend on file order."""
    parent = list(range(len(rows)))

    def find(x):
        while parent[x] != x:
            parent[x] = parent[parent[x]]
            x = parent[x]
        return x
    first = {}
    for i, r in enumerate(rows):
        for k in (("g", r["group_id"]), ("c", r["call_id"])):
            if k in first:
                parent[find(i)] = find(first[k])
            else:
                first[k] = i
    comp = defaultdict(list)
    for i in range(len(rows)):
        comp[find(i)].append(i)
    return {min(rows[i]["id"] for i in v): v for v in comp.values()}


def pick_units(fam: str, rows: list[dict], n: int, seed: int = SEED) -> tuple[list[dict], dict]:
    """At most n rows in whole units. A file with n rows or fewer is taken whole (a shortfall is reported, never refilled).
    Larger files: units in the order of a seeded hash, a unit that would overshoot n is skipped; source order is kept."""
    if len(rows) <= n:
        return list(rows), {"truncated": False, "units": len(components(rows))}
    comp = components(rows)
    take, size = set(), 0
    for key in sorted(comp, key=lambda k: (h64(seed, fam, k), k)):
        if size + len(comp[key]) <= n:
            take.update(comp[key])
            size += len(comp[key])
        if size == n:
            break
    return [r for i, r in enumerate(rows) if i in take], {"truncated": True, "units": len([k for k in comp if comp[k][0] in take]),
                                                          "rows_in": len(rows)}


# ----------------------------------------------------------------------------------------------------------------- build
def load_family(ilog, fam: str, lean: Path, per_family: int, full: bool, problems: list[str]) -> tuple[list[dict], dict]:
    f = fam_paths(fam, lean)
    info = {"family": fam, "source": rel(f["mixdev"], lean)}
    if not f["mixdev"].exists():
        problems.append(f"{fam}: no mixdev file {rel(f['mixdev'], lean)} (an entered family needs its S5 mixdev, spec 7.1)")
        info["rows_out"] = 0
        return [], info
    rows = ilog.jsonl(f["mixdev"])
    p = row_problems(fam, rows)
    qc = ilog.json(f["qc"]) if f["qc"].exists() else None
    man = ilog.json(f["manifest"]) if f["manifest"].exists() else None
    sp, shas = recorded_sha_problems(fam, f["mixdev"], qc, man)
    problems += p + sp
    if f["cand"].exists():
        problems += disjoint_problems(fam, rows, ilog.jsonl(f["cand"]))
    out, sel = (list(rows), {"truncated": False, "units": len(components(rows)) if rows else 0}) if full else pick_units(fam, rows, per_family)
    info |= {"rows_in": len(rows), "rows_out": len(out), "shortfall": 0 if full else max(0, per_family - len(out)),
             "rule": "whole existing S5 mixdev" if full else f"<= {per_family} rows, whole units", **sel, "sha256": shas,
             "qtype": dict(Counter(r["qtype"] for r in out)), "role": dict(Counter(r.get("role") for r in out)),
             "groups": len({r["group_id"] for r in out})}
    return out, info


def build(ilog, lean: Path = LEAN, families=None, entered_from=None, per_family: int = PER_FAMILY) -> dict:
    """Pure of writes. Returns {"main": rows, "report_only": rows, "report": dict, "problems": [...]}."""
    problems: list[str] = []
    entered, left, src = entered_set(ilog, lean, families, entered_from)
    trained = [b for b in TRAINED_PROGRAM if b in entered and b not in REPORT_ONLY_FAMILIES] + \
              [b for b in CARRY_FULL + CARRY_CAPPED if b in entered]
    main, per = [], {}
    for fam in trained:
        rows, info = load_family(ilog, fam, lean, per_family, fam in CARRY_FULL, problems)
        main += rows
        per[fam] = info
    rep_rows, rep_per, rep_warn = [], {}, []
    rep_blocks = [b for b in REPORT_ONLY_FAMILIES if fam_paths(b, lean)["mixdev"].exists()] + \
                 [b for b in REPORT_BLOCKS if b in entered and fam_paths(b, lean)["mixdev"].exists()]
    for b in rep_blocks:
        rows, info = load_family(ilog, b, lean, 10 ** 9, True, problems if b in entered else rep_warn)
        rep_rows += rows
        rep_per[b] = info
    # the merged file as a whole
    ids = Counter(r["id"] for r in main + rep_rows)
    dup = [i for i, n in ids.items() if n > 1]
    if dup:
        problems.append(f"{len(dup)} ids occur twice across the staged mixdev files, e.g. {dup[:2]}")
    grp = defaultdict(set)
    for r in main:
        grp[r["group_id"]].add((r.get("meta") or {}).get("family"))
    cross = [g for g, s in grp.items() if len(s) > 1]
    if cross:
        problems.append(f"{len(cross)} group_ids are shared by two families in the merged mixdev (a paired bootstrap would join them)")
    td = lean / "data" / "c2_transfer_dev.jsonl"
    if td.exists():                                        # the two dev sets must not share an id or a group
        trows = ilog.jsonl(td)
        for key in ("id", "group_id"):
            both = {r[key] for r in main + rep_rows} & {r[key] for r in trows}
            if both:
                problems.append(f"mixdev and transfer dev share {len(both)} {key}(s), e.g. {sorted(both)[:2]}")
    own = [b for b in OWN_DEV_FAMILIES if b in entered]
    report = {
        "tool": "c2_build/mixdev_c2.py", "spec": "C2_DATA_SPEC 7.1", "seed": SEED, "per_family": per_family,
        "entry": {"entered": entered, "left_out": left, **src},
        "trained_families": trained, "mixdev_main": per, "main_rows": len(main),
        "main_by_family": {b: v["rows_out"] for b, v in per.items()},
        "shortfalls": {b: v["shortfall"] for b, v in per.items() if v.get("shortfall")},
        "report_only": rep_per, "report_only_rows": len(rep_rows), "report_only_warnings": rep_warn,
        "excluded": {"T27": "A62 (b): moves to C3; its mixdev is a report-only read (c2_mixdev_report_only.jsonl)",
                     "blocks": "A39 h: a block's own mixdev is report-only and never trained",
                     "T35": "no data yet (no candidates on disk)" if "T35" not in entered else "entered",
                     "T37b": "A52 (a): moves to C3, no mixdev",
                     "own_dev_families_entered": own or None,
                     "own_dev_note": "T40-T46 own dev (PREREG 4.4) is pooled separately (9.3 term 3), not in c2_mixdev" if own else None},
        "interpretations": ["F5 / F6 / F11: the whole existing S5 mixdev (spec 7.1 'plus F5/F6/F11 existing S5 mixdev')",
                            "F4 (carry-over, no spec 7.1 line): the 150-per-trained-family rule, whole units, seeded",
                            "a family below 150 rows keeps its rows; nothing is refilled or relabelled (spec 5.3 / A34 c)"],
        "inputs": dict(ilog.entries), "problems": problems,
    }
    return {"main": main, "report_only": rep_rows, "report": report, "problems": problems}


# ----------------------------------------------------------------------------------------------------------------- writers
class PlainWriter:
    """Unguarded writer for tests (temp folders)."""

    def jsonl(self, p, rows):
        from mixio import write_jsonl
        return write_jsonl(p, rows)

    def json(self, p, obj):
        from mixio import write_json
        return write_json(p, obj)

    def text(self, p, s):
        Path(p).parent.mkdir(parents=True, exist_ok=True)
        Path(p).write_text(s, encoding="utf-8")


class GuardedWriter(PlainWriter):
    """c2io writers: A38 first, never-open refused, lean/ only."""

    def jsonl(self, p, rows):
        return c2io.write_jsonl(p, rows)

    def json(self, p, obj):
        return c2io.write_json(p, obj)

    def text(self, p, s):
        c2io.require_a38()
        super().text(c2io._out(p), s)


def check_out_dir(out_dir: Path, lean: Path = LEAN) -> Path:
    """Staging only: never under data/ (a new dev file there makes every G13 log stale)."""
    o = Path(out_dir).resolve()
    if (Path(lean).resolve() / "data") == o or (Path(lean).resolve() / "data") in o.parents:
        raise Problem(f"--out-dir {out_dir} is under data/: stage under c2_build/staged/<lane>/ (a new data/ dev file makes every G13 log stale)")
    return o


def write_rows(w, out_dir: Path, name: str, rows: list[dict]) -> dict:
    sha = w.jsonl(out_dir / name, rows)
    w.text(out_dir / f"{name}.sha256", f"{sha}  {name}\n")
    return {"file": name, "rows": len(rows), "sha256": sha}


def write_build(res: dict, out_dir: Path, w=None, lean: Path = LEAN) -> dict:
    w = w or GuardedWriter()
    out_dir = check_out_dir(out_dir, lean)
    main = write_rows(w, out_dir, MAIN, res["main"])
    rep = write_rows(w, out_dir, REPORT_ONLY, res["report_only"])
    report = res["report"] | {"staged": {"main": main, "report_only": rep, "dir": rel(out_dir, lean)},
                              "built_utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())}
    w.json(out_dir / BUILD_REPORT, report)
    man = write_manifests(out_dir, w, lean)
    return {"main": main, "report_only": rep, "manifests": man}


# --------------------------------------------------------------------------------------------------------------- manifests
def jl(p) -> list[dict]:
    return [json.loads(x) for x in Path(p).read_text(encoding="utf-8").splitlines() if x.strip()]


def file_info(p: Path, lean: Path = LEAN) -> dict:
    """Counts of a dev jsonl file (counts, ids, shas only)."""
    rows = jl(p)
    return {"file": rel(p, lean), "rows": len(rows), "bytes": Path(p).stat().st_size, "sha256": sha256_file(p),
            "groups": len({r["group_id"] for r in rows}), "calls": len({r["call_id"] for r in rows}),
            "qtype": dict(Counter(r["qtype"] for r in rows)),
            "families": dict(Counter((r.get("meta") or {}).get("family") for r in rows))}


def predict_cmd(adapter: str, splits, tag: str = "") -> str:
    """The HF-path read the gate requires (gate_dev.pipeline_check: od_gcp.py predict, TTA off, pinned revision)."""
    return (f"python -B od_gcp.py predict --name {adapter} --base {sm.BASE} --splits {','.join(splits)} --layout {sm.LAYOUT} "
            f"--revision {sm.REV}" + (f" --tag {tag}" if tag else ""))


GATE_MODELS = [
    {"model": gc.CAND, "adapter": gc.CAND, "tag": "", "role": "candidate (final-step adapter; spec 7.3 / A42-D 9)"},
    {"model": gc.REF, "adapter": gc.STORED_C1, "tag": "_c2", "role": "REF = a fresh C1 read in the same job (gate_c2 REF)"},
]
GATE_RULES = [
    "C1 and C2 are read in the SAME od_gcp.py predict job as the 9 gate dev splits (gate_dev.pipeline_check: one base, host, GPU, torch, "
    "CUDA, revision and chat template; TTA off; no forced override; no .meta.json without a load record)",
    "the data file sha256 below must equal the file on the VM at read time (sha256sum -c) and is frozen: any rebuild gives a new sha and "
    "makes every read of the old file stale",
    "CANDIDATE_C2.json (the candidate adapter sha256) is written before the candidate's first read (gate_c2.check_candidate)",
    "a passing refparity look for the REF read (gate_dev --mode refparity) precedes the pre-gate",
    "never read at the 25 / 50 / 75% snapshots (spec 9.1): only c2_mixdev is a report-only snapshot read",
]
VM_DATA = "~/lean/data"


def _vm(name: str, staged_rel: str, sha: str | None) -> dict:
    return {"vm": sm.VMS[0][0], "zone": sm.VMS[0][1], "lean_dir": "~/lean",
            "push": f"reads/vm_scripts/vm.sh scp {staged_rel} {sm.VMS[0][0]}:{VM_DATA}/{name}.jsonl",
            "verify": f"cd {VM_DATA} && echo '{sha}  {name}.jsonl' | sha256sum -c"}


def set_manifest(split: str, info: dict | None, *, staged_rel: str | None, final_rel: str, role: str, gate_bound: bool,
                 status: str, notes=(), extra: dict | None = None, models=None, snapshot: bool = False) -> dict:
    models = models if models is not None else GATE_MODELS
    m = {"manifest": "c2_predict_job", "version": 1, "set": split, "status": status, "role": role,
         "gate_input": gate_bound, "report_only": not gate_bound,
         "data": {"staged": staged_rel, "install_to": final_rel, **(info or {})},
         "install": ("orchestrator, in the one code-edit window: copy the staged file to the install path, register it with g13_c2 "
                     "(c2_mixdev: path already in C2_DEV; a new data/ dev file makes every G13 log stale -> one g13_c2.py refresh-dev); "
                     "never before the capture batch's inputs are final") if staged_rel else "already in data/ (frozen)",
         "vm": _vm(split, staged_rel or final_rel, (info or {}).get("sha256")), "models": models,
         "reads": [{"model": x["model"], "command": predict_cmd(x["adapter"], [split], x["tag"]),
                    "preds": f"preds_{split}/{x['model']}.jsonl"} for x in models],
         "rules": list(GATE_RULES if gate_bound else [GATE_RULES[1]] + ["report-only: no ship rule, no gate decision, no candidate choice reads this set"]),
         "notes": list(notes)}
    if snapshot:
        m["snapshot_reads_report_only"] = {
            "when": "25 / 50 / 75% snapshots of the C2 run (spec 9.1), on od-l4b, free",
            "adapter": "q35_4b_c2/snaps/<snapshot>",
            "preds_name": "q35_4b_c2__snaps__<snapshot>  ('/' becomes '__' in od_gcp.out_name)",
            "command": predict_cmd("q35_4b_c2/snaps/<snapshot>", [split]),
            "rule": "report-only; never a candidate, never a stop-rule input (snap_monitor_c2 reads only the old slice)"}
    if extra:
        m |= extra
    return m


def mixdev_manifests(out_dir: Path, lean: Path = LEAN) -> dict:
    """{file name: manifest dict} for everything that can be derived now."""
    out = {}
    srel = lambda n: rel(out_dir / n, lean)           # noqa: E731
    main_p, rep_p = out_dir / MAIN, out_dir / REPORT_ONLY
    rpt = json.loads((out_dir / BUILD_REPORT).read_text()) if (out_dir / BUILD_REPORT).exists() else {}
    if main_p.exists():
        info = file_info(main_p, lean)
        out["predict_c2_mixdev.json"] = set_manifest(
            gc.MIXDEV, info, staged_rel=srel(MAIN), final_rel="data/c2_mixdev.jsonl", gate_bound=True, status="staged",
            role="pre-gate (a) learning (C2 - C1 >= +8.0 pp, paired LB > 0), the temperature fit, the R term of S (PREREG 9.3), "
                 "report-only per-family reads",
            snapshot=True, extra={"build_report": srel(BUILD_REPORT), "families_entered": rpt.get("trained_families")},
            notes=["150 per trained family; F5 / F6 / F11 whole; T27 and block mixdevs are NOT here (A62 b, A39 h)",
                   "rows are gate_dev form: qtype noul (gold 0/1) or choice (gold in options); meta.family keys the per-family report"])
    if rep_p.exists():
        info = file_info(rep_p, lean)
        out["predict_c2_mixdev_report.json"] = set_manifest(
            REPORT_SPLIT, info, staged_rel=srel(REPORT_ONLY), final_rel=f"data/{REPORT_SPLIT}.jsonl", gate_bound=False, status="staged",
            role="report-only: T27 (A62 b, 'family not trained in C2') and the entered blocks' own mixdev (A39 h)",
            notes=["not a gate_c2 input; reading it never changes a decision",
                   "if installed under data/, it is a new data/ file: do it in the same code-edit window as c2_mixdev, or not at all"])
    tr = lean / "data" / "c2_transfer_dev.jsonl"
    if tr.exists():
        info = file_info(tr, lean)
        out["predict_c2_transfer_dev.json"] = set_manifest(
            gc.TRANSFER, info, staged_rel=None, final_rel="data/c2_transfer_dev.jsonl", gate_bound=True, status="frozen in data/",
            role="pre-gate (b) transfer (C2 - C1 >= +3.0 pp, paired LB > 0); never trained",
            notes=["T19 and T21 only (T36, T20 out: A45 c / A52); built by zed_orch/build_transfer_dev.py",
                   "the dev job must also include the G13 'c2_transfer_dev' target as scanned: no change to this file after the capture batch"])
    out["predict_c2_t37b_dev.json"] = t37b_manifest(lean)
    out["predict_pab_gproxy.json"] = gproxy_manifest(lean)
    out["predict_jobs_index.json"] = index_manifest(out, lean)
    return out


def t37b_manifest(lean: Path = LEAN) -> dict:
    """T37b-dev (spec 3.18; gate_c2 check (d)): staged by lane P4 as c2_t37b_dev.jsonl + c2_t37b_dev_relations.jsonl. Pending until a
    staged or installed pair is found."""
    cands = sorted((Path(lean) / "c2_build" / "staged").glob("*/c2_t37b_dev.jsonl")) + [Path(lean) / "data" / "c2_t37b_dev.jsonl"]
    found = next((c for c in cands if c.exists()), None)
    base = {"set": gc.T37B_DEV, "gate_input": True, "report_only": False,
            "role": "pre-gate (d): complement violation C2 < C1 on 300 complement pairs of gate-dev yes/no rows (spec 3.18, 7.2)",
            "expected": {"pairs": 300, "rows": 600, "relation_type": "complement", "relations_file": "c2_t37b_dev_relations.jsonl",
                         "split": gc.T37B_DEV, "frames": "held out of the trained 379-pattern catalogue (A42-D 10.3)"}}
    if found is None:
        return {"manifest": "c2_predict_job", "version": 1, "status": "pending: T37b-dev is not staged yet (lane P4)", **base,
                "models": GATE_MODELS, "rules": GATE_RULES,
                "reads": [{"model": x["model"], "command": predict_cmd(x["adapter"], [gc.T37B_DEV], x["tag"]),
                           "preds": f"preds_{gc.T37B_DEV}/{x['model']}.jsonl"} for x in GATE_MODELS],
                "notes": ["rerun `mixdev_c2.py manifests` after the pair of files is staged; gate_c2.pregate refuses without them"]}
    relp = found.with_name("c2_t37b_dev_relations.jsonl")
    rows = jl(found)
    probs = []
    rels = jl(relp) if relp.exists() else []
    if not relp.exists():
        probs.append("c2_t37b_dev_relations.jsonl missing next to the rows (gate_c2.relations refuses)")
    by = {r["id"]: r for r in rows}
    comp = [x for x in rels if x.get("type") == "complement"]
    bad = [x for x in comp if not (x.get("a") in by and x.get("b") in by and by[x["a"]]["qtype"] == "noul" == by[x["b"]]["qtype"])]
    if bad:
        probs.append(f"{len(bad)} complement relations point at missing or non-yes/no rows")
    comp = [x for x in comp if x not in bad]
    if len(comp) != 300:
        probs.append(f"{len(comp)} valid complement pairs, spec 3.18 says 300 (report the shortfall; never refill after a read)")
    staged = Path(lean) / "data" in found.parents
    m = set_manifest(gc.T37B_DEV, file_info(found, lean), staged_rel=None if staged else rel(found, lean),
                     final_rel="data/c2_t37b_dev.jsonl", gate_bound=True, status="staged" if not probs else "staged with problems",
                     role=base["role"], notes=["relations file: " + rel(relp, lean) + (f" sha256 {sha256_file(relp)}" if relp.exists() else "")]
                     + probs, extra={"expected": base["expected"], "relations": {"file": rel(relp, lean), "pairs": len(comp),
                                                                                  "sha256": sha256_file(relp) if relp.exists() else None}})
    m["vm"]["push_relations"] = f"reads/vm_scripts/vm.sh scp {rel(relp, lean)} {sm.VMS[0][0]}:{VM_DATA}/{gc.T37B_DEV}_relations.jsonl"
    return m


def gproxy_manifest(lean: Path = LEAN) -> dict:
    """The G-proxy (PREREG item 12; A42-D 12.2 unmet label, A61 f). C1's read exists; the pins come from GPROXY_HASH.json."""
    g = Path(lean) / "data" / "c2_gproxy"
    pin = json.loads((g / "GPROXY_HASH.json").read_text()) if (g / "GPROXY_HASH.json").exists() else {}
    want = (pin.get("sha256") or {}).get("pab_gproxy.jsonl")
    have = sha256_file(g / "pab_gproxy.jsonl") if (g / "pab_gproxy.jsonl").exists() else None
    c1 = g / "c1_read" / "preds_pab_gproxy" / "q35_4b_main500k_pab.jsonl"
    probs = [] if want and want == have else [f"pab_gproxy.jsonl sha256 {str(have)[:12]} is not the pinned {str(want)[:12]}"]
    m = {"manifest": "c2_predict_job", "version": 1, "set": GPROXY_SPLIT, "status": "frozen in data/c2_gproxy" if not probs else "PIN MISMATCH",
         "role": "G-proxy: the G term of S (PREREG 9.3), the item 4.3 / 10 probes; NOT a ship rule (item 12.5). A42-D 12.2 is UNMET "
                 "(A61 f): every result carries that label",
         "gate_input": False, "report_only": False,
         "data": {"file": "data/c2_gproxy/pab_gproxy.jsonl", "sha256": have, "pinned_sha256": want, "rows": 3267,
                  "relations": "data/c2_gproxy/pab_gproxy_relations.jsonl", "relations_sha256": (pin.get("sha256") or {}).get("pab_gproxy_relations.jsonl"),
                  "hash_record": "data/c2_gproxy/GPROXY_HASH.json"},
         "vm": {"vm": sm.VMS[0][0], "push": "meta_src/gproxy/c1_read.sh push (pab_gproxy.jsonl -> ~/lean/data/, sha256 -c on the VM)"},
         "c1_read": {"exists": c1.exists(), "file": "data/c2_gproxy/c1_read/preds_pab_gproxy/q35_4b_main500k_pab.jsonl",
                     "sha256": sha256_file(c1) if c1.exists() else None, "settings": "fast path (SGLang S1), A18.2 readout, choice rows 2 views, yes/no 1 read"},
         "reads": [{"model": f"{gc.CAND}_pab", "engine": "fast_read.py predict (same settings as C1's G-proxy read; needs the merged C2 served)",
                    "command": f"~/od/bin/python -B fast_read.py predict --name {gc.CAND} --splits {GPROXY_SPLIT} --tag _pab --workers 12 --chunk 8",
                    "preds": f"preds_{GPROXY_SPLIT}/{gc.CAND}_pab.jsonl"}],
         "rules": ["C2 is read with the SAME engine, readout and tag as C1's recorded read (a different engine would add parity noise to the paired change)",
                   "the file hash in GPROXY_HASH.json is checked before any read (meta_src/gproxy/finalize.py verify); the file is never edited",
                   "paired CI clustered by source document, 10,000 resamples, seed 0 (item 12.6); a complement pair is one cluster",
                   "Jev never reads a selection signal; G-proxy sources are disjoint from training sources"],
         "notes": probs}
    return m


def index_manifest(ms: dict, lean: Path = LEAN) -> dict:
    """The one gate job: the splits the pre-gate reads for C1 and C2 together, and where each set stands."""
    splits = list(gc.SPLITS9) + ["eval_jagged", "eval_opi", gc.MIXDEV, gc.TRANSFER, gc.T37B_DEV]
    return {"manifest": "c2_predict_job_index", "version": 1,
            "gate_job": {"splits": splits, "models": GATE_MODELS,
                         "commands": [predict_cmd(x["adapter"], splits, x["tag"]) for x in GATE_MODELS],
                         "note": "one od_gcp.py predict job per model on the same VM (gate_dev.pipeline_check); the _perm reads (perm seed 1) "
                                 "are the retention lane's; the 18-candidate grid reads the same sets with its own names (lane P6)"},
            "sets": {f: {"set": m.get("set"), "status": m.get("status"), "gate_input": m.get("gate_input"),
                         "report_only": m.get("report_only"), "sha256": (m.get("data") or {}).get("sha256"),
                         "rows": (m.get("data") or {}).get("rows")} for f, m in sorted(ms.items()) if f != "predict_jobs_index.json"},
            "not_in_the_gate_job": [GPROXY_SPLIT + " (fast path, tag _pab; see predict_pab_gproxy.json)", REPORT_SPLIT + " (report-only)"],
            "snapshot_reads": "25 / 50 / 75%: c2_mixdev only, report-only (spec 9.1); never transfer dev, T37b-dev, the gate dev splits or the G-proxy"}


def write_manifests(out_dir: Path, w=None, lean: Path = LEAN) -> dict:
    w = w or GuardedWriter()
    out_dir = check_out_dir(out_dir, lean)
    ms = mixdev_manifests(out_dir, lean)
    res = {}
    for name, m in ms.items():
        res[name] = w.json(out_dir / "manifests" / name, m)
    return res


# ---------------------------------------------------------------------------------------------------------------- verify
def verify(out_dir: Path, lean: Path = LEAN) -> list[str]:
    out_dir = Path(out_dir)
    probs = []
    rpt = out_dir / BUILD_REPORT
    if not rpt.exists():
        return [f"{BUILD_REPORT} missing in {out_dir}"]
    r = json.loads(rpt.read_text())
    for key, name in (("main", MAIN), ("report_only", REPORT_ONLY)):
        want = r["staged"][key]
        p = out_dir / name
        if not p.exists() or sha256_file(p) != want["sha256"]:
            probs.append(f"{name}: staged file differs from the build report (rebuilt or edited after the build)")
    inst = Path(lean) / "data" / MAIN
    if inst.exists() and inst.exists() and (out_dir / MAIN).exists() and sha256_file(inst) != sha256_file(out_dir / MAIN):
        probs.append("data/c2_mixdev.jsonl exists and differs from the staged file")
    return probs


# ------------------------------------------------------------------------------------------------------------------- CLI
def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    sub = ap.add_subparsers(dest="cmd", required=True)
    b = sub.add_parser("build")
    b.add_argument("--families", nargs="*", default=None)
    b.add_argument("--entered-from", default=None)
    b.add_argument("--per-family", type=int, default=PER_FAMILY)
    b.add_argument("--out-dir", default=str(STAGED))
    b.add_argument("--write", action="store_true")
    for n in ("manifests", "verify"):
        s = sub.add_parser(n)
        s.add_argument("--out-dir", default=str(STAGED))
    a = ap.parse_args(argv)
    try:
        if a.cmd == "build":
            check_out_dir(a.out_dir)
            ilog = c2io.C2InputLog()
            res = build(ilog, LEAN, a.families, a.entered_from, a.per_family)
            r = res["report"]
            print(json.dumps({"entered": r["entry"]["entered"], "trained": r["trained_families"], "main_rows": r["main_rows"],
                              "by_family": r["main_by_family"], "shortfalls": r["shortfalls"], "report_only_rows": r["report_only_rows"],
                              "problems": res["problems"]}, indent=1))
            if res["problems"]:
                print("REFUSED: problems above; nothing written", file=sys.stderr)
                return 2
            if a.write:
                print(json.dumps(write_build(res, Path(a.out_dir)), indent=1))
            return 0
        if a.cmd == "manifests":
            print(json.dumps(write_manifests(Path(a.out_dir)), indent=1))
            return 0
        probs = verify(Path(a.out_dir))
        print(json.dumps({"ok": not probs, "problems": probs}, indent=1))
        return 0 if not probs else 2
    except (Problem, c2io.C2Refused) as e:
        print(f"REFUSED: {e}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    sys.exit(main())
