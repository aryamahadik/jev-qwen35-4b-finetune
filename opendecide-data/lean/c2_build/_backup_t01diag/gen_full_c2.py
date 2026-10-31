"""gen_full_c2.py: C2 full 1.5x candidate generation + QC task files for ONE program family (C2_DATA_SPEC 6.4 step 7,
6.3 gates, 7.1 mixdev; PREREG A43 a/d/f, A44 a/b, A45 a/g). CPU only; no model, no network, no git.

What `gen_full_c2.py <FAM>` does
  1. Opens the family with the loader patch of its LATEST pilot runner (imported, never run): run_pilot_i3 for T06 T31 T01;
     run_pilot_i2 for T23 T12 T24 T15 T33 T32 T27; run_pilot_i1 for T28 T30 T07 T26 T25 (RUNNER below).
  2. Exclusions are applied to the kit context BEFORE any draw, so an excluded form is never drawn (not drawn-then-dropped):
       - templates quarantined by the binding verdict: g5h/G5H_FINAL.json quarantined_templates and the G3-H report
         (PILOT_REPORT.json gates.G3-H.report.quarantined) of the family's binding pilot folder;
       - the family's forms in zed_orch/a43f_quarantine.json (A43 f);
       - T27 only: T27-wording-60ef1ded0d (3 hits in the pilot rows, found by the final pass).
     A question form whose every wording is excluded ("dead" qform) is redrawn at the SAMPLE level with a deterministic
     seed + j * REDRAW_STRIDE (stride divisible by 32, so seed blocks keep their position), except for T01 / T06 / T31,
     whose plugins fall back to plain forms by design (their pilots equal what this produces).
  3. Seeds (documented, disjoint from each other and from the pilot seed base 900000+ of pilot.SEED_BASE):
       candidates  FULL_SEED_BASE   2,000,000 + k   (k = seed per training sampler, as pilot.build_pilot)
       QC build    QC_SEED_BASE     3,000,000 + k   (G6 / G7 sample, G15 off)
       mixdev S5   MIXDEV_SEED_BASE 4,000,000 + k
       redraws     + j * 50,000,000
     All bases are divisible by 32 (label-first seed blocks stay whole).
  4. Builds ceil(1.5 x c2io.TARGETS[FAM]) candidate rows (whole units; the last unit may overshoot) through
     pilot.build_pilot (G2, G3, G4, G-SL, G-LEX, G-TW, G15, schema, options in c2_kit.pipeline), then G7, G10, overlay,
     spec 3.0, G11 (template shares), G12 (exact duplicates dropped, keep first) on the candidates, and a SEPARATE QC
     build of >= 5,000 rows (default 6,000, G15 off) for G6 (A43 a: unchanged bar chance + 2 pp, every view and model;
     plus a report on the free-form slice) and G7. If the candidates alone are >= 5,000 rows they carry G6.
  5. G10 is recorded as pilot.g10 plus two explicit annotations (nothing is hidden):
       - double_negation_share below 2% is "waived (A44 b / A45 a)" ONLY when the family has A43 (f) forms in
         a43f_quarantine.json (the shortfall comes from A43 f); every other check binds;
       - yes_rate_cells is reported as deferred to crowd selection (difficulty bin unset before the crowd; every
         binding PILOT_VERDICT treats it so; crowd_select enforces wording x bin label quotas).
  6. Writes (unless --dry-run), all through the guarded kit writers (A38 present; never-open paths refused):
       data/c2_parts/<FAM>/out/candidates_c2.jsonl, candidates_c2.relations.jsonl, MANIFEST.json, mixdev_S5.jsonl
       data/c2_parts/<FAM>/qc/QC_REPORT.json                  pass=false, stage "generated" (qc_full_c2.py finalize replaces it)
       data/c2_parts/<FAM>/qc/GEN_REPORT.json                 every gate against its bar, seeds, exclusions, build stats
       data/c2_parts/<FAM>/qc/_generated/*.jsonl              the untouched generated files (finalize always starts here)
       data/c2_parts/<FAM>/qc/g5h/{tasks,answers,key.json,manifest.json}   G5-H: readers A and B on the seeded 300 rows
                                                                (400 for T32), reader FF on every Mode F row; <= 50 items
       data/c2_parts/<FAM>/qc/g3h/{tasks,answers,key.json,manifest.json}   G3-H: one read of every Mode F row
     Task files are self-contained (pilot._task_text): the exact answer path, the instructions, the contract, the items.
     key.json files are orchestrator only: never give them to an agent.

  ../.venv/bin/python -B gen_full_c2.py T30 --dry-run --n 600 --qc-n 1000      (from lean/c2_build; in memory)
  ../.venv/bin/python -B gen_full_c2.py T30                                    (writes the out/ + qc/ layout)
  ../.venv/bin/python -B gen_full_c2.py --counts                               (expected candidate counts, 15 families)
"""
from __future__ import annotations

import argparse
import contextlib
import dataclasses
import hashlib
import importlib
import json
import math
import os
import sys
import time
from collections import Counter, defaultdict
from pathlib import Path

sys.dont_write_bytecode = True
HERE = Path(__file__).resolve().parent                     # lean/c2_build
if str(HERE) not in sys.path:
    sys.path.insert(0, str(HERE))

import c2io  # noqa: E402
import pilot  # noqa: E402
import pilot_loaders as PL  # noqa: E402
from c2_kit import chunker, g3h, g5h, paths, pipeline  # noqa: E402

GEN_VERSION = "c2 full generation 1.0 (15 Oct 2026)"
FULL_SEED_BASE = 2_000_000
QC_SEED_BASE = 3_000_000
MIXDEV_SEED_BASE = 4_000_000
REDRAW_STRIDE = 50_000_000
QC_N_DEFAULT = 6_000            # A43 a: >= 5,000 QC rows (6,000 is the size every pilot verdict used)
QC_N_MIN = 5_000
MIXDEV_N = 150                  # spec 7.1: 150 per trained family
MIXDEV_N_MIN = 1
CAND_FACTOR = 1.5               # spec 6.4 step 7
FAMILIES_DIR = HERE / "families"
QUAR_A43F = HERE / "zed_orch" / "a43f_quarantine.json"
G11_MAX_SHARE = 0.02            # spec 6.3 G11: no skin or template above 2% of a family
EXTRA_EXCLUDE = {"T27": ["T27-wording-60ef1ded0d"]}
FALLBACK_FAMILIES = ("T01", "T06", "T31")          # plugins fall back to plain forms when a dneg wording is missing

# family -> (latest runner module, its iteration number = QC fix_iterations)
RUNNER = {"T06": ("run_pilot_i3", 3), "T31": ("run_pilot_i3", 3), "T01": ("run_pilot_i3", 3),
          "T23": ("run_pilot_i2", 2), "T12": ("run_pilot_i2", 2), "T24": ("run_pilot_i2", 2),
          "T15": ("run_pilot_i2", 2), "T33": ("run_pilot_i2", 2), "T32": ("run_pilot_i2", 2),
          "T27": ("run_pilot_i2", 2),
          "T28": ("run_pilot_i1", 1), "T30": ("run_pilot_i1", 1), "T07": ("run_pilot_i1", 1),
          "T26": ("run_pilot_i1", 1), "T25": ("run_pilot_i1", 1)}


# ================================================================================================ sizes and seeds

def candidate_target(fam: str) -> int:
    """Spec 6.4 step 7: 1.5 x the spec 2.1 selected target (c2io.TARGETS)."""
    return int(round(CAND_FACTOR * c2io.TARGETS[fam]))


def seed_plan() -> dict:
    return {"candidates": FULL_SEED_BASE, "qc": QC_SEED_BASE, "mixdev": MIXDEV_SEED_BASE,
            "redraw_stride": REDRAW_STRIDE, "pilot_seed_base": pilot.SEED_BASE,
            "note": "bases divisible by 32; pilot (900000+, G6-at-size included) never overlaps"}


def check_family(fam: str) -> None:
    if fam not in RUNNER:
        raise SystemExit(f"{fam}: not one of the 15 full-generation program families {sorted(RUNNER)} "
                         "(T37b has its own builder; T29/T35 are not generated until they pass; transfer dev is "
                         "never trained)")


# ================================================================================================ loader patches

def _import_runner(fam: str):
    mod, _ = RUNNER[fam]
    sys.path.insert(0, str(HERE))
    return importlib.import_module(f"families.{fam}.{mod}")


@contextlib.contextmanager
def loader_patch(fam: str):
    """Install the loader patch of the family's latest pilot runner (the runner module is imported, its main never
    runs; the output-folder redirect is not needed: this tool writes its own layout). Restores PL on exit."""
    check_family(fam)
    saved_open, saved_loaders = PL.open_family, dict(PL.LOADERS)
    try:
        R = _import_runner(fam)
        if fam == "T01":                                        # make_ctx_i3: supplement minus the A43 f forms
            with R._patched():
                yield R
        elif fam == "T33":                                      # dneg_i2 loader (its forms are all A43 f: excluded below)
            with R._patched():
                yield R
        elif fam == "T31":                                      # pools_v2 + dneg supplement minus the 44 A43 f forms
            R.install_loader()
            yield R
        elif fam == "T06":
            RP = R._load_run_pilot()
            orig = RP._t06

            @contextlib.contextmanager
            def t06_i3():
                with orig() as kit:
                    yield dataclasses.replace(kit, ctx=R._drop_quarantined(kit.ctx))
            PL.LOADERS["T06"] = t06_i3
            yield R
        elif fam == "T27":
            R._install_supplement()
            PL.LOADERS["T27"] = R.RP._t27
            yield R
        elif fam == "T26":
            PL.LOADERS["T26"] = R._t26
            yield R
        elif fam == "T32":                                      # real loader + dneg_stage2.apply_supplement (no-op today)
            real = PL.LOADERS["T32"]
            sys.path.insert(0, str(FAMILIES_DIR / "T32"))
            from dneg_stage2 import apply_supplement

            @contextlib.contextmanager
            def t32_i2():
                with real() as kit:
                    apply_supplement(kit)
                    yield kit
            PL.LOADERS["T32"] = t32_i2
            yield R
        else:                                                   # T28 T30 T07 T25 T23 T12 T24 T15: dir redirect only
            yield R
    finally:
        PL.open_family = saved_open
        PL.LOADERS.clear()
        PL.LOADERS.update(saved_loaders)


# ================================================================================================ exclusions

def binding_dir(fam: str) -> Path:
    return FAMILIES_DIR / fam / f"pilot_i{RUNNER[fam][1]}"


def _json(p: Path):
    try:
        return PL.safe_json(p)
    except Exception:  # noqa: BLE001  (missing / unreadable: no list from that source)
        return None


def quarantine_sources(fam: str, *, bdir: Path | None = None, a43f_file: Path = QUAR_A43F) -> dict:
    """{source: sorted ids}: the A43 f forms, the binding G5-H and G3-H template quarantines, the family extras."""
    bdir = bdir or binding_dir(fam)
    a43f = (_json(a43f_file) or {}).get(fam) or []
    g5 = (_json(bdir / "g5h" / "G5H_FINAL.json") or {}).get("quarantined_templates") or []
    rep = _json(bdir / "PILOT_REPORT.json") or {}
    g3 = ((rep.get("gates") or {}).get("G3-H") or {}).get("report") or {}
    return {"a43f": sorted(set(a43f)), "g5h": sorted(set(g5)), "g3h": sorted(set(g3.get("quarantined") or [])),
            "extra": sorted(set(EXTRA_EXCLUDE.get(fam, [])))}


def skin_matches(s, banned: set) -> bool:
    return s.skin_id in banned or any(l in banned for l in (s.lexicon_ids or ()))


def apply_exclusions(kit, banned: set):
    """(kit with the banned skins / wordings removed from kit.ctx.skins, report). Removing them is what makes an excluded
    form un-drawable (KitCtx.pick draws from ctx.skins). Held-out skins are filtered by the same rule."""
    skins = kit.ctx.skins
    gone = {k for k, s in skins.items() if skin_matches(s, banned)}
    qf_before = Counter(s.qform for s in skins.values() if s.kind == "wording" and not s.held_out and s.qform)
    kept = {k: s for k, s in skins.items() if k not in gone}
    qf_after = Counter(s.qform for s in kept.values() if s.kind == "wording" and not s.held_out and s.qform)
    dead = sorted(q for q in qf_before if not qf_after.get(q))
    seen = set()
    for k in gone:
        seen.add(k)
        seen.update(l for l in (skins[k].lexicon_ids or ()) if l in banned)
    rep = {"banned_ids": len(banned), "skins_removed": len(gone),
           "removed_by_kind": dict(Counter(skins[k].kind for k in gone)),
           "banned_ids_matching_no_skin": sorted(banned - seen)[:40],
           "n_banned_ids_matching_no_skin": len(banned - seen), "dead_qforms": dead,
           "wordings_before": sum(qf_before.values()), "wordings_after": sum(qf_after.values())}
    new_ctx = dataclasses.replace(kit.ctx, skins=kept)
    return dataclasses.replace(kit, ctx=new_ctx), rep


class Redraw:
    """Shadows plugin.sample on the INSTANCE: a spec whose question form is dead (no wording left after the exclusions)
    is redrawn from seed + j * REDRAW_STRIDE (same position inside its seed block), deterministic, <= MAX tries."""
    MAX = 60

    def __init__(self, plugin, dead):
        self.plugin, self.dead, self.orig = plugin, set(dead), plugin.sample
        self.redrawn = Counter()
        plugin.sample = self

    def __call__(self, seed, sampler):
        spec = self.orig(seed, sampler)
        j = 0
        while spec.qform in self.dead and j < self.MAX:
            j += 1
            self.redrawn[spec.qform] += 1
            spec = self.orig(seed + j * REDRAW_STRIDE, sampler)
        if spec.qform in self.dead:
            raise ValueError(f"no live question form after {self.MAX} redraws (seed {seed})")
        return spec

    def restore(self):
        if self.plugin.__dict__.get("sample") is self:
            del self.plugin.__dict__["sample"]


# ================================================================================================ builds and gates

def build_mixdev(kit, n: int = MIXDEV_N, seed_base: int = MIXDEV_SEED_BASE, log=None) -> tuple:
    """Spec 7.1 mixdev: whole S5 units (held-out sampler, held-out registers / skins / wordings via the plugin), trimmed to
    n rows, G2 ... G15 through pipeline.build_unit. Never trained (meta.dev_only)."""
    plugin, ctx = kit.plugin, kit.ctx
    held = tuple(plugin.HELD_OUT_SAMPLERS)
    if not held:
        return [], {"note": "no held-out sampler"}
    rows, drops, k = [], Counter(), 0
    while len(rows) < n and k < 40 * n:
        seed, sampler = seed_base + k // len(held), held[k % len(held)]
        k += 1
        try:
            res = pipeline.build_unit(plugin, plugin.sample(seed, sampler), ctx, run_g15=True)
        except Exception as e:  # noqa: BLE001
            drops[type(e).__name__] += 1
            continue
        if not res.ok:
            for g in {g for g, _ in res.problems}:
                drops[g] += 1
            continue
        rows += res.rows
    rows = rows[:n]
    not_dev = sum(1 for r in rows if not (r["meta"].get("dev_only") or r["meta"].get("sampler") in held))
    return rows, {"rows": len(rows), "attempts": k, "drops": dict(drops), "not_dev_only": not_dev,
                  "seed_base": seed_base, "held_out_samplers": list(held)}


def dedup_exact(b) -> dict:
    """G12 exact: drop later rows whose (card, state, instructions) repeats an earlier one (keep first); relations of a
    dropped row are removed. Rows are never edited."""
    seen, drop = {}, set()
    for i in b.infos:
        r = i.row
        key = hashlib.sha256(json.dumps([r.get("card"), r["state"], r["instructions"], r.get("options")],
                                        ensure_ascii=False).encode()).hexdigest()
        if key in seen:
            drop.add(r["id"])
        else:
            seen[key] = r["id"]
    if drop:
        b.infos = [i for i in b.infos if i.row["id"] not in drop]
        b.rels = [x for x in b.rels if x["a"] not in drop and x["b"] not in drop]
    return {"gate": "G12", "exact_duplicates_dropped": len(drop), "rows_after": len(b.infos),
            "bar": "exact duplicates 0 after the keep-first drop (MinHash near-dup: batch step, not run here)",
            "verdict": "pass"}


def g11_shares(infos, plugin) -> dict:
    rows = [i.row for i in infos]
    n = len(rows) or 1
    skins = Counter(r["meta"]["c2"]["skin_id"] for r in rows)
    words = Counter(r["meta"]["wording_id"] for r in rows if r["meta"].get("wording_id"))
    regs = Counter(r["meta"]["c2"]["register"] for r in rows)
    over = {k: round(v / n, 4) for k, v in {**skins, **words}.items() if v / n > G11_MAX_SHARE}
    return {"gate": "G11", "bar": f"no skin or wording above {G11_MAX_SHARE:.0%} of the family (spec 6.3)",
            "n_rows": n, "max_template_share": round(max(list((skins | words).values()) or [0]) / n, 4),
            "templates_over_bar": over, "verdict": "pass" if not over else "fail",
            "report_3_0": {"max_skin_rows": max(skins.values()) if skins else 0,
                           "skins_over_6_rows": sum(1 for v in skins.values() if v > 6),
                           "max_register_share": round(max(regs.values()) / n, 4) if regs else None,
                           "registers_over_15pct": sorted(k for k, v in regs.items() if v / n > 0.15),
                           "bar": "spec 3.0: each skin <= 6 rows, each register <= 15% of new rows (report; the crowd "
                                  "selection trims to the 1.0x target)"},
            "deferred": "Self-BLEU / Vendi vs the golden_train slice: not run by this tool"}


def annotate_g10(g10: dict, fam: str, a43f_ids: int, removed: int) -> dict:
    """A45 (a): the double-negation floor is waived ONLY when the shortfall comes from A43 f (the family has A43 f forms
    listed). yes_rate_cells is deferred to selection (precedent of every binding PILOT_VERDICT). Everything else binds."""
    g = json.loads(json.dumps(g10, default=str))
    chk = g["checks"]
    waivers, deferred = [], {}
    dn = chk.get("double_negation_share")
    if dn and dn["verdict"] == "fail":
        if a43f_ids > 0:
            dn["verdict"] = "waived"
            dn["waiver"] = "waived (A44 b / A45 a)"
            dn["why"] = (f"shortfall from A43 (f): {a43f_ids} banned forms listed for {fam} in a43f_quarantine.json "
                         f"({removed} more skins removed by this tool's exclusion step)")
            waivers.append({"check": "double_negation_share", "record": "waived (A44 b / A45 a)"})
        else:
            dn["waiver"] = "NOT waived: the family has no A43 (f) forms, so the shortfall is not from A43 (f)"
    yr = chk.get("yes_rate_cells")
    if yr and yr["verdict"] == "fail":
        deferred["yes_rate_cells"] = ("deferred to crowd selection (difficulty bin unset before the crowd; every binding "
                                      "PILOT_VERDICT treats it as report-only; crowd_select enforces wording x bin quotas)")
    binding = sorted(k for k, v in chk.items() if v["verdict"] == "fail" and k not in deferred)
    g.update({"waivers": waivers, "deferred": deferred, "failing_raw": g.get("failing"), "failing_binding": binding,
              "verdict": "pass" if not binding else "fail"})
    return g


def g6_freeform(infos) -> dict:
    ff = [i for i in infos if i.row["meta"]["c2"]["author_mode"] == "F"]
    if len(ff) < 300:
        return {"verdict": "report", "n": len(ff), "note": "fewer than 300 Mode F rows: G6 not fit on the free-form slice"}
    try:
        out = pilot.g6(ff)
        out["note"] = "separate report on the free-form slice (spec 6.3); the binding G6 is the all-rows part"
        return out
    except Exception as e:  # noqa: BLE001
        return {"verdict": "report", "n": len(ff), "error": f"{type(e).__name__}: {e}"[:300]}


def full_gates(b, qb, plugin, fam: str, rep_excl: dict, sources: dict) -> dict:
    gates = {}
    gates["full_size"] = {"value": b.stats["rows_written"], "bar": f">= {b.stats['target_rows']} rows of passing units "
                          "(1.5 x spec 2.1 target)", "verdict": "pass" if b.stats["reached_target"] else "fail",
                          "units_attempted": b.stats["units_attempted"]}
    gates.update(pilot.program_gates(b))
    gates["G7_candidates"] = pilot.g7(b.infos)
    gates["G10"] = annotate_g10(pilot.g10(b.infos, b.units, plugin), fam, len(sources["a43f"]), rep_excl["skins_removed"])
    gates["overlay"] = pilot.overlay(b.units, plugin)
    gates["spec_3_0"] = pilot.spec30(b.infos, plugin)
    gates["G11"] = g11_shares(b.infos, plugin)
    qsrc = qb if qb is not None else b
    gates["G6"] = pilot.g6(qsrc.infos)
    gates["G6"]["qc_rows"] = len(qsrc.infos)
    gates["G6"]["qc_build"] = "separate (G15 off), seed base %d" % QC_SEED_BASE if qb is not None else "the candidates"
    gates["G6"]["bar_note"] = "A43 (a): <= chance + 2 pp on >= 5,000 QC rows, every view and model"
    gates["G6_freeform_slice"] = g6_freeform(qsrc.infos)
    gates["G7"] = pilot.g7(qsrc.infos)
    gates["G7"]["qc_rows"] = len(qsrc.infos)
    return gates


def program_pass(gates: dict) -> tuple:
    """(pass, failing gate names): every binding program gate. G12 / G11 included; reports excluded."""
    bad = []
    for g, d in gates.items():
        if g in ("overlay", "spec_3_0", "G10", "G6", "G7", "G7_candidates", "G11", "G12", "full_size") or \
                g in pilot.PROGRAM_GATES:
            if d.get("verdict") == "fail":
                bad.append(g)
    if gates.get("G10", {}).get("verdict") == "fail" and "G10" not in bad:
        bad.append("G10")
    return not bad, sorted(set(bad))


# ================================================================================================ Haiku task files

def g5h_full_chunks(rows: list, fam: str, qdir: Path) -> tuple:
    """(files {rel path under qc/: text}, tasks, key) for readers A and B on the seeded sample (300; 400 for T32) and
    reader FF on every Mode F row. Same task-file style as pilot.g5h_chunks (exact answer paths, <= 50 items)."""
    n = g5h.n_read(fam)
    seed = f"{fam}|full-g5h|{GEN_VERSION}"
    sample, refused = [], []
    for r in g5h.sample_rows(rows, len(rows), seed):
        if len(sample) >= n:
            break
        try:
            chunker.check_item("blind_read", g5h.read_item(r))
        except chunker.ChunkError as e:
            refused.append({"row_id": r["id"], "why": str(e)[:200]})
            continue
        sample.append(r)
    ff_ok, ff_refused = [], []
    for r in rows:
        if r["meta"]["c2"]["author_mode"] != "F":
            continue
        try:
            chunker.check_item("blind_read", g5h.read_item(r))
            ff_ok.append(r)
        except chunker.ChunkError as e:
            ff_refused.append({"row_id": r["id"], "why": str(e)[:200]})
    a, b = g5h.make_reads(sample, fam, seed=f"{fam}-full-g5h", prompt=pilot.G5H_PROMPT)
    batches = [("A", a), ("B", b)]
    if ff_ok:
        batches.append(("FF", g5h.make_freeform_read(ff_ok, fam, seed=f"{fam}-full-g5h", prompt=pilot.G5H_PROMPT)))
    files, tasks = {}, []
    for reader, bt in batches:
        for c in bt.chunks:
            tid = c["task_id"]
            ans, tf = qdir / "g5h" / "answers" / f"{tid}.json", qdir / "g5h" / "tasks" / f"{tid}.md"
            title = "G5-H blind read" + (" (all free-form rows)" if reader == "FF" else "")
            text = pilot._task_text(title, fam, tid, ans, len(c["items"]), pilot.G5H_PROMPT, pilot.G5H_CONTRACT,
                                    c["items"])
            files[f"g5h/tasks/{tid}.md"] = text
            tasks.append({"gate": "G5-H", "reader": reader, "task_id": tid, "task_file": str(tf), "answer_file": str(ans),
                          "n_items": len(c["items"]), "batch_id": bt.batch_id,
                          "task_sha256": hashlib.sha256(text.encode()).hexdigest(),
                          "allowed_read": [str(tf)], "allowed_write": [str(ans)]})
    key = {"family": fam, "gate": "G5-H", "version": GEN_VERSION, "n_rows": len(sample), "sample_seed": seed,
           "row_ids": [r["id"] for r in sample], "refused_by_chunk_check": refused,
           "freeform_row_ids": [r["id"] for r in ff_ok], "freeform_refused_by_chunk_check": ff_refused,
           "readers": {rd: pilot._batch_record(bt) for rd, bt in batches},
           "note": "orchestrator only: never give this file to a Haiku agent"}
    return files, tasks, key


def g3h_full_chunks(infos, plugin, fam: str, qdir: Path) -> tuple:
    """pilot.g3h_chunks with the full-generation seed and the qc/ folder: one extraction read of every Mode F row."""
    items, exp, missing = [], {}, []
    for i in infos:
        if i.row["meta"]["c2"]["author_mode"] != "F":
            continue
        if not i.ff_text:
            missing.append(i.row["id"])
            continue
        fields = plugin.extract_fields(i.spec)
        it = g3h.extraction_item(i.ff_text, fields)
        try:
            chunker.check_item("extract_g3h", it)
        except chunker.ChunkError as e:
            missing.append(f"{i.row['id']}: {str(e)[:160]}")
            continue
        items.append((i.row["id"], it))
        exp[i.row["id"]] = {"template": i.row["meta"]["c2"]["skin_id"], "register": i.row["meta"]["c2"]["register"],
                            "expected": plugin.extract_view(i.spec), "fields": [pilot._field_json(f) for f in fields]}
    if not items:
        return {}, [], None
    bt = chunker.make_batch("extract_g3h", fam, items, seed=f"{fam}-full-g3h", prompt=pilot.G3H_PROMPT)
    files, tasks = {}, []
    for c in bt.chunks:
        tid = c["task_id"]
        ans, tf = qdir / "g3h" / "answers" / f"{tid}.json", qdir / "g3h" / "tasks" / f"{tid}.md"
        contract = pilot._g3h_contract([[s["field"] for s in it["schema"]] for it in c["items"]])
        text = pilot._task_text("G3-H extraction", fam, tid, ans, len(c["items"]), pilot.G3H_PROMPT, contract, c["items"])
        files[f"g3h/tasks/{tid}.md"] = text
        tasks.append({"gate": "G3-H", "task_id": tid, "task_file": str(tf), "answer_file": str(ans),
                      "n_items": len(c["items"]), "batch_id": bt.batch_id,
                      "task_sha256": hashlib.sha256(text.encode()).hexdigest(),
                      "allowed_read": [str(tf)], "allowed_write": [str(ans)]})
    key = {"family": fam, "gate": "G3-H", "version": GEN_VERSION, "n_rows": len(items), "batch": pilot._batch_record(bt),
           "rows": exp, "mode_f_rows_without_region": missing,
           "note": "orchestrator only: never give this file to a Haiku agent"}
    return files, tasks, key


# ================================================================================================ run

def _clean(obj):
    return json.loads(json.dumps(obj, default=str))


def sha_file(p) -> str:
    return c2io.mixio.sha256_file(p)


def layout(fam: str, root: Path | None = None) -> dict:
    d = (root or c2io.C2_PARTS) / fam
    return {"out": d / "out", "qc": d / "qc", "cand": d / "out" / c2io.CAND, "rel": d / "out" / c2io.REL,
            "man": d / "out" / c2io.MAN, "mixdev": d / "out" / "mixdev_S5.jsonl", "qcrep": d / "qc" / c2io.QC,
            "gen": d / "qc" / "GEN_REPORT.json", "gendir": d / "qc" / "_generated"}


def run(fam: str, *, n: int | None = None, dry: bool = False, qc_n: int = QC_N_DEFAULT, no_qc: bool = False,
        redraw: bool = True, root: Path | None = None, log=print) -> dict:
    check_family(fam)
    t0 = time.time()
    n_cand = n or candidate_target(fam)
    if qc_n < QC_N_MIN and n is None and not dry:
        raise SystemExit(f"--qc-n {qc_n} < {QC_N_MIN}: A43 (a) needs >= 5,000 QC rows for the binding G6")
    src = quarantine_sources(fam)
    banned = set().union(*map(set, src.values()))
    L = layout(fam, root)
    with loader_patch(fam):
        with PL.open_family(fam) as kit0:
            kit, xrep = apply_exclusions(kit0, banned)
            plugin = kit.plugin
            use_redraw = redraw and fam not in FALLBACK_FAMILIES and bool(xrep["dead_qforms"])
            rd = Redraw(plugin, xrep["dead_qforms"]) if use_redraw else None
            try:
                log(f"{fam}: loader {kit.loader}; excluded {xrep['skins_removed']} skins "
                    f"({xrep['n_banned_ids_matching_no_skin']} ids matched none); dead qforms {xrep['dead_qforms']}")
                b = pilot.build_pilot(kit, n_cand, seed_base=FULL_SEED_BASE, run_g15=True, log=log)
                g12 = dedup_exact(b)
                log(f"{fam}: {len(b.infos)} candidate rows, {len(b.units)} units, {b.stats['units_attempted']} "
                    f"attempted, {b.stats['seconds']}s")
                need_qc = (not no_qc) and len(b.infos) < QC_N_MIN
                qb = pilot.build_pilot(kit, qc_n, seed_base=QC_SEED_BASE, run_g15=False, log=log) if need_qc else None
                mix_rows, mix_rep = build_mixdev(kit, MIXDEV_N, log=log)
            finally:
                if rd:
                    rd.restore()
            if no_qc:
                gates = {"full_size": {"value": b.stats["rows_written"], "verdict": "pass" if b.stats["reached_target"]
                                       else "fail"}, **pilot.program_gates(b)}
                gates["G10"] = annotate_g10(pilot.g10(b.infos, b.units, plugin), fam, len(src["a43f"]),
                                            xrep["skins_removed"])
                gates["G12"] = g12
            else:
                gates = full_gates(b, qb, plugin, fam, xrep, src)
                gates["G12"] = g12
            infos, rels = b.infos, b.rels
            rows = [i.row for i in infos]
            probs = c2io.candidate_problems(fam, rows)
            ok, failing = program_pass(gates)
            tdir = L["qc"]
            files5, tasks5, key5 = g5h_full_chunks(rows, fam, tdir)
            files3, tasks3, key3 = g3h_full_chunks(infos, plugin, fam, tdir)
            n_ff = sum(1 for r in rows if r["meta"]["c2"]["author_mode"] == "F")
            report = {
                "family": fam, "version": GEN_VERSION, "created_utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
                "spec": "C2_DATA_SPEC 6.4 step 7, 6.3, 7.1; PREREG A43 a/d/f, A44 a/b, A45 a/g",
                "fix_iterations": RUNNER[fam][1], "runner": RUNNER[fam][0], "loader": kit.loader, "pools": kit.pools,
                "loader_notes": kit.notes, "seeds": seed_plan(), "target_selected": c2io.TARGETS[fam],
                "candidate_target": n_cand, "n_candidates": len(rows), "n_relations": len(rels),
                "relation_types": dict(Counter(x["type"] for x in rels)), "qtype": dict(Counter(r["qtype"] for r in rows)),
                "mode_f_rows": n_ff, "build": b.stats, "qc_build": qb.stats if qb is not None else None,
                "mixdev": mix_rep, "exclusions": {"sources": {k: len(v) for k, v in src.items()}, **xrep,
                                                  "redrawn": dict(rd.redrawn) if rd else {},
                                                  "redraw_on": use_redraw},
                "candidate_problems": probs, "gates": gates, "program_pass": ok and not probs,
                "program_failing": failing + (["candidate_problems"] if probs else []),
                "haiku_tasks": {"G5-H": {"sample_rows": key5["n_rows"], "n_read_bar": g5h.n_read(fam),
                                         "tasks": len(tasks5), "freeform_rows": len(key5["freeform_row_ids"]),
                                         "refused_by_chunk_check": len(key5["refused_by_chunk_check"])
                                         + len(key5["freeform_refused_by_chunk_check"])},
                                "G3-H": {"mode_f_rows": n_ff, "tasks": len(tasks3)}},
                "seconds": round(time.time() - t0, 1), "written": not dry}
            if not dry:
                write_layout(fam, L, rows, rels, mix_rows, report, files5, files3, tasks5, tasks3, key5, key3)
            report["gate_lines"] = pilot.gate_lines({k: v for k, v in gates.items() if isinstance(v, dict)
                                                     and "verdict" in v}).split("\n")
            return report


def write_layout(fam, L, rows, rels, mix_rows, report, files5, files3, tasks5, tasks3, key5, key3):
    if probs := report["candidate_problems"]:
        raise SystemExit("candidate rows refused, nothing written: " + "; ".join(probs))
    paths.write_jsonl(L["cand"], rows)
    paths.write_jsonl(L["rel"], rels)
    paths.write_jsonl(L["mixdev"], mix_rows)
    for name, data in (("candidates_c2.jsonl", rows), ("candidates_c2.relations.jsonl", rels), ("mixdev_S5.jsonl", mix_rows)):
        paths.write_jsonl(L["gendir"] / name, data)
    man = {"family": fam, "parents": [], "parents_note": "program-generated rows: no public parent dataset",
           "generator": GEN_VERSION, "stage": "generated (before G5-H / G3-H drops)",
           "files": {c2io.CAND: {"sha256": sha_file(L["cand"]), "rows": len(rows)},
                     c2io.REL: {"sha256": sha_file(L["rel"]), "rows": len(rels)}},
           "mixdev": {"mixdev_S5.jsonl": {"sha256": sha_file(L["mixdev"]), "rows": len(mix_rows)}}}
    paths.write_json(L["man"], man)
    for rel, text in {**files5, **files3}.items():
        paths.write_text(L["qc"] / rel, text)
    for g, tasks, key, fdir in (("g5h", tasks5, key5, "g5h"), ("g3h", tasks3, key3, "g3h")):
        if not tasks:
            continue
        paths.write_text(L["qc"] / fdir / "answers" / "README.txt",
                         f"Haiku {g.upper()} answer files: one <task_id>.json per task file in ../tasks/.\n")
        paths.write_json(L["qc"] / fdir / "key.json", key)
        paths.write_json(L["qc"] / fdir / "manifest.json", {
            "family": fam, "gate": "G5-H" if g == "g5h" else "G3-H", "tasks": tasks,
            "prompt_sha": chunker.sha(pilot.G5H_PROMPT if g == "g5h" else pilot.G3H_PROMPT)})
    paths.write_json(L["gen"], _clean(report))
    paths.write_json(L["qcrep"], {
        "pass": False, "stage": "generated", "family": fam, "fix_iterations": report["fix_iterations"],
        "passed_utc": None, "note": "G5-H / G3-H pending: run qc_full_c2.py score | adjudicate | finalize",
        "program_pass": report["program_pass"],
        "files": {c2io.CAND: {"sha256": sha_file(L["cand"])}, c2io.REL: {"sha256": sha_file(L["rel"])}}})


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("family", nargs="?")
    ap.add_argument("--dry-run", action="store_true", help="in memory: write nothing")
    ap.add_argument("--n", type=int, default=None, help="candidate rows (default 1.5 x the spec 2.1 target)")
    ap.add_argument("--qc-n", type=int, default=QC_N_DEFAULT, help=f"QC build rows for G6 (>= {QC_N_MIN} for a real run)")
    ap.add_argument("--no-qc", action="store_true", help="skip the QC build (G6 not run; never for a real run)")
    ap.add_argument("--no-redraw", action="store_true")
    ap.add_argument("--counts", action="store_true", help="print the expected candidate counts and exit")
    ap.add_argument("--report", default=None, help="dry-run: also write the report JSON to this file")
    a = ap.parse_args(argv)
    if a.counts or not a.family:
        tot = 0
        for f in sorted(RUNNER):
            print(f"{f}: target {c2io.TARGETS[f]} -> candidates {candidate_target(f)} (runner {RUNNER[f][0]})")
            tot += candidate_target(f)
        print(f"total candidates {tot}")
        return 0
    rep = run(a.family, n=a.n, dry=a.dry_run, qc_n=a.qc_n, no_qc=a.no_qc, redraw=not a.no_redraw,
              log=lambda m: print(m, file=sys.stderr, flush=True))
    if a.report:
        Path(a.report).write_text(json.dumps(_clean(rep), indent=1))
    print(json.dumps({"family": rep["family"], "n_candidates": rep["n_candidates"], "qc_rows": (rep["qc_build"] or {}).get(
        "rows_written"), "program_pass": rep["program_pass"], "failing": rep["program_failing"],
        "mixdev_rows": rep["mixdev"].get("rows"), "excluded": rep["exclusions"], "haiku_tasks": rep["haiku_tasks"],
        "seconds": rep["seconds"], "written": rep["written"], "gate_lines": rep["gate_lines"]},
        indent=1, ensure_ascii=False, default=str))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
