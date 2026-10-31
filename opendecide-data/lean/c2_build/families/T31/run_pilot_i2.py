"""families/T31/run_pilot_i2.py: the T31 fix-iteration-2 pilot (C2_DATA_SPEC 6.4 step 6 then step 5 again) into pilot_i2/.

It is run_pilot_i1.py with output folder pilot_i2/ (pilot/ and pilot_i1/ stay as produced) and with a loader that reads the
double-negation supplement pools_v2_dneg/ (dneg_i2.py) on top of the frozen pools_v2/: the supplement adds two question
sems, the G-LEX 2/2 admitted wordings of yn_holder_dneg / yn_agent_dneg and their wording skins. pilot_loaders.py is not
edited: install_loader() replaces PL.LOADERS["T31"] in this process. Without a supplement folder the loader is the frozen
one and the plugin falls back (0% double negation). Program gates only: no Haiku or model is run; the G5-H / G3-H task
files are written, never answered.

  cd lean/c2_build
  ../.venv/bin/python -B families/T31/run_pilot_i2.py                       # write pilot_i2/ (program gates, task files)
  ../.venv/bin/python -B families/T31/run_pilot_i2.py --dry-run             # in memory, nothing written (prints the shas)
  PYTHONHASHSEED=1 ../.venv/bin/python -B families/T31/run_pilot_i2.py --dry-run   # determinism: compare with seed 2
  ../.venv/bin/python -B families/T31/run_pilot_i2.py --g6 --n 6000         # A43 G6 -> pilot_i2/G6_AT_6000.json
  ../.venv/bin/python -B families/T31/run_pilot_i2.py --score               # after the Haiku G5-H / G3-H answers exist
  options: --supp-dir DIR (default pools_v2_dneg)  --out-dir DIR (default pilot_i2)  --no-g15  --n N
"""
from __future__ import annotations

import argparse
import contextlib
import importlib
import json
import sys
import time
from collections import Counter
from pathlib import Path

sys.dont_write_bytecode = True
HERE = Path(__file__).resolve().parent
C2_BUILD = HERE.parents[1]
if str(C2_BUILD) not in sys.path:
    sys.path.insert(0, str(C2_BUILD))

import pilot as PI  # noqa: E402
import pilot_loaders as PL  # noqa: E402
from c2_kit import cards as CD  # noqa: E402
from c2_kit import chunker, paths  # noqa: E402
from c2_kit import choiceplan as CP  # noqa: E402

FID = "T31"
OUT = HERE / "pilot_i2"
SUPP = HERE / "pools_v2_dneg"
VERSION = PI.PILOT_VERSION + " / T31 fix iteration 2"
DNEG_FORMS = ("yn_holder_dneg", "yn_agent_dneg")
_SUPP = [SUPP]


# ------------------------------------------------------------------------------------------------ loader
@contextlib.contextmanager
def _t31_i2():
    """pilot_loaders._t31 plus the double-negation supplement (dneg_i2.apply_supplement)."""
    P = importlib.import_module("families.T31.plugin")
    FV = importlib.import_module("families.T31.freeze_v2")
    D = importlib.import_module("families.T31.dneg_i2")
    pools = FV.load_pools()
    notes = D.apply_supplement(pools, _SUPP[0])
    yield PL.FamilyKit("T31", PL.family_dir("T31"), P.T31(lexicon=pools["lexicon"]), FV.kit_ctx(pools),
                       "freeze_v2.load_pools() + dneg_i2.apply_supplement() / kit_ctx(); T31(lexicon=pools['lexicon'])",
                       f"pools_v2/ + {_SUPP[0].name}/", notes)


def install_loader(supp=None) -> None:
    if supp is not None:
        _SUPP[0] = Path(supp)
    PL.LOADERS[FID] = _t31_i2


# ------------------------------------------------------------------------------------------------ run
def run(out: Path = OUT, n_rows: int = PI.N_ROWS, *, write: bool = True, run_g15: bool = True, supp=None,
        log=print) -> dict:
    install_loader(supp)
    with PL.open_family(FID) as kit:
        plugin = kit.plugin
        pdir = Path(out)
        log(f"{FID}: loader {kit.loader}; output {pdir}; {kit.notes}")
        b = PI.build_pilot(kit, n_rows, run_g15=run_g15, log=log)
        log(f"{FID}: built {b.stats['rows_written']} rows in {b.stats['units_written']} units "
            f"({b.stats['units_attempted']} attempted, {b.stats['seconds']}s)")
        infos = b.infos
        gates = {"pilot_size": {"value": b.stats["rows_written"], "bar": f">= {n_rows} rows of passing units "
                                "(spec 6.4 step 5)", "verdict": "pass" if b.stats["reached_target"] else "fail",
                                "units_attempted": b.stats["units_attempted"]}}
        gates.update(PI.program_gates(b))
        gates["G6"] = PI.g6(infos)
        gates["G7"] = PI.g7(infos)
        gates["G10"] = PI.g10(infos, b.units, plugin)
        gates["overlay"] = PI.overlay(b.units, plugin)
        gates["spec_3_0"] = PI.spec30(infos, plugin)
        files, tasks5, key5 = PI.g5h_chunks(infos, FID, pdir)
        files3, tasks3, key3 = PI.g3h_chunks(infos, plugin, FID, pdir)
        files.update(files3)
        n_ff = sum(1 for i in infos if i.row["meta"]["c2"]["author_mode"] == "F")
        gates["G3-H"] = {"verdict": "pending" if tasks3 else "n/a", "bar": ">= 98% per template, else quarantine; "
                         "mismatched rows always dropped (spec 6.3)", "mode_f_rows": n_ff,
                         "items": key3["n_rows"] if key3 else 0, "tasks": len(tasks3),
                         "note": ("Haiku answers pending; run `run_pilot_i2.py --score` after they exist" if tasks3 else
                                  "no Mode F row in the pilot")}
        gates["G5-H"] = {"verdict": "pending", "bar": "0 confirmed wrong golds; ambiguous <= 1%; a template with > 3% "
                         "disagreement is quarantined (spec 6.3; pilot reads 100 rows)", "rows": key5["n_rows"],
                         "readers": 2, "tasks": len(tasks5),
                         "note": "two blind reads pending; then Claude adjudication of the queue + 30 controls"}
        rows = [i.row for i in infos]
        extra = iteration_report(b, plugin, kit)
        if write:
            paths.write_jsonl(pdir / "rows.jsonl", rows)
            paths.write_jsonl(pdir / "relations.jsonl", b.rels)
            for rel, text in files.items():
                paths.write_text(pdir / rel, text)
            paths.write_text(pdir / "g5h" / "answers" / "README.txt",
                             "Haiku G5-H answer files: one <task_id>.json per task file in ../tasks/.\n")
            paths.write_json(pdir / "g5h" / "key.json", key5)
            paths.write_json(pdir / "g5h" / "manifest.json", {"family": FID, "gate": "G5-H", "tasks": tasks5,
                                                               "prompt_sha": chunker.sha(PI.G5H_PROMPT)})
            if tasks3:
                paths.write_text(pdir / "g3h" / "answers" / "README.txt",
                                 "Haiku G3-H answer files: one <task_id>.json per task file in ../tasks/.\n")
                paths.write_json(pdir / "g3h" / "key.json", key3)
                paths.write_json(pdir / "g3h" / "manifest.json", {"family": FID, "gate": "G3-H", "tasks": tasks3,
                                                                   "prompt_sha": chunker.sha(PI.G3H_PROMPT)})
        body_rows = "".join(json.dumps(r, ensure_ascii=False) + "\n" for r in rows)
        body_rels = "".join(json.dumps(r, ensure_ascii=False) + "\n" for r in b.rels)
        report = {"family": FID, "version": VERSION, "created_utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
                  "spec": "C2_DATA_SPEC 6.4 step 5 (bars 6.3; overlay 4.1; balance 3.0); PREREG A37 / A38; "
                          "fix iteration 2 (the last; A43 c)",
                  "tier": plugin.TIER, "plugin": type(plugin).__name__, "g0_sha256": plugin.G0_SHA256,
                  "loader": kit.loader, "pools": kit.pools, "loader_notes": kit.notes, "build": b.stats,
                  "files": {"rows": str(pdir / "rows.jsonl"), "rows_sha256": PI.sha_text(body_rows),
                            "relations": str(pdir / "relations.jsonl"), "relations_sha256": PI.sha_text(body_rels),
                            "n_rows": len(rows), "n_relations": len(b.rels),
                            "relation_types": dict(Counter(x["type"] for x in b.rels)),
                            "qtype": dict(Counter(r["qtype"] for r in rows)),
                            "roles": dict(Counter(r["role"] for r in rows))},
                  "gates": gates, "chunks": {"G5-H": tasks5, "G3-H": tasks3}, "iteration": extra, "written": write}
        report["summary"] = PI.summarize(gates)
        report["gate_lines"] = PI.gate_lines(gates).split("\n")
        fix = fix_report(report, rows)
        if write:
            paths.write_json(pdir / "PILOT_REPORT.json", report)
            paths.write_json(pdir / "FIX_I2.json", fix)
        report["fix_i2"] = fix
        return report


def iteration_report(b, plugin, kit) -> dict:
    """Report only (the gates are in PILOT_REPORT.gates): what the dneg wordings did on the pilot rows."""
    rows = [i.row for i in b.infos]
    sets = [rr.option_set for u in b.units for rr in u.rendered if rr.option_set is not None]
    c = Counter((r["role"], r["meta"]["qform"]) for r in rows)
    twins = Counter(r["meta"]["qform"] for r in rows if r["role"] == "twin")
    base = [r for r in rows if r["role"] == "base"]
    tags = Counter(t for r in base for t in r["meta"]["edge"])
    skins = Counter(r["meta"]["c2"]["skin_id"] for r in rows)
    toks = CD.token_report(rows)
    qf = Counter(r["meta"]["qform"] for r in rows)
    yn = [r for r in rows if r["qtype"] == "noul"]
    n_dneg = sum(qf[q] for q in DNEG_FORMS)
    return {
        "double_negation": {"forms_available": plugin.dneg_ok, "rows_by_form": {q: qf[q] for q in DNEG_FORMS},
                            "rows": n_dneg, "yes_no_rows": len(yn),
                            "share_of_yes_no": round(n_dneg / max(1, len(yn)), 4)},
        "supplement_notes": kit.notes,
        "plan_report": CP.plan_report(sets),
        "token_report": {k: toks[k] for k in ("mean", "max", "yes_no_share", "field_means", "rules_mean")},
        "card_styles": CD.style_report(rows),
        "base_forms": dict(Counter(r["meta"]["qform"] for r in base)),
        "twin_forms": dict(twins),
        "trap_shares_of_base_rows": {k: round(v / max(1, len(base)), 3) for k, v in sorted(tags.items())},
        "skin_rows": {"max": max(skins.values()), "n_skins": len(skins), "cap": plugin.skin_row_cap,
                      "cap_overflow": plugin.cap_overflow},
        "packs": {"distinct": len({r["meta"]["domain_pack"] for r in rows}),
                  "cards": len({r["meta"]["card_id"] for r in rows})},
        "double_negation_forms_available": plugin.dneg_ok,
        "quarantined_pieces": {k: v for k, v in sorted(plugin.quarantined(kit.ctx).items())},
        "relations_by_form": {f"{r}|{q}": n for (r, q), n in sorted(c.items())},
    }


def fix_report(report: dict, rows: list) -> dict:
    """pilot_i2/FIX_I2.json: the one open fix (F07) with the pilot number that shows it, and the program gates after."""
    g, it = report["gates"], report["iteration"]
    d = g["G10"]["checks"]["double_negation_share"]
    return {
        "family": FID, "stage": "fix iteration 2 (the last; A43 c)", "version": VERSION,
        "g0_sha256": report["g0_sha256"], "rows_sha256": report["files"]["rows_sha256"],
        "no_label_set": True, "no_haiku_or_model_run_here": True,
        "fixes": {"F07": {
            "status": "fixed" if d["verdict"] == "pass" else "NOT fixed (G10 double_negation_share fails)",
            "how": "Haiku-authored yn_holder_dneg / yn_agent_dneg wordings (dneg_i2.py: authoring, wording_problems, G-LEX "
                   "2/2, regression check) loaded from the pools_v2_dneg/ supplement by this runner's loader",
            "evidence": {"double_negation_share": d["value"], "bar": d["bar"], "verdict": d["verdict"],
                         **it["double_negation"]},
            "open": ["G13-seed on the new wordings (pilot_i2/G13_PENDING.txt: batch run)",
                     "G5-H re-read: the pilot's 100-row sample needs double-negation rows"]}},
        "program_gates_after": [line for line in report["gate_lines"] if not line.startswith(("G3-H", "G5-H"))],
        "not_done_here": ["no Haiku or model run (G5-H, G3-H pending)", "no label set or edited", "no paid compute, no commit",
                          "no gate bar loosened, no G0 target lowered"],
    }


def g6_at_size(n: int = 6000, out: Path = OUT, supp=None, log=print) -> dict:
    """A43 G6 at >= 5,000 rows: the same build, pilot.g6 / g7 / g10, as zed_orch/g6_at_size.py, with this loader."""
    install_loader(supp)
    t0 = time.time()
    with PL.open_family(FID) as kit:
        b = PI.build_pilot(kit, n, run_g15=False)
        g6, g7, g10 = PI.g6(b.infos), PI.g7(b.infos), PI.g10(b.infos, b.units, kit.plugin)
    cells = {}
    for part in ("yes_no", "choice"):
        p = g6.get(part) or {}
        if p.get("n"):
            cells[part] = {"n": p["n"], "chance": p["chance"],
                           "max": max((p[v][m], v, m) for v in p if isinstance(p[v], dict) and "lr" in p[v]
                                      for m in ("lr", "gbt"))}
    res = {"family": FID, "n_rows": len(b.infos), "seconds": round(time.time() - t0), "seed_base": PI.SEED_BASE,
           "G6_verdict": g6["verdict"], "G6_fails": g6["fails"], "G6_cells_max": cells,
           "G7_verdict": g7.get("verdict"), "G10_verdict": g10.get("verdict"),
           "G10_double_negation_share": (g10.get("checks") or {}).get("double_negation_share"),
           "G10_fails": {k: v for k, v in (g10.get("checks") or {}).items() if v.get("verdict") == "fail"}}
    paths.write_json(Path(out) / f"G6_AT_{n}.json", res)
    return res


class _IterDir(type(Path())):
    """pilot.score_family reads PL.family_dir(fid) / "pilot"; here that is pilot_i2/."""

    def __truediv__(self, key):
        return Path(str(OUT)) if key == "pilot" else super().__truediv__(key)


def score(*, write: bool = True, audit_failed: tuple = ()) -> dict:
    orig = PL.family_dir
    PL.family_dir = lambda fid: _IterDir(orig(fid))
    try:
        return PI.score_family(FID, write=write, audit_failed=audit_failed)
    finally:
        PL.family_dir = orig


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--n", type=int, default=None)
    ap.add_argument("--out-dir", default=str(OUT))
    ap.add_argument("--supp-dir", default=str(SUPP))
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("--no-g15", action="store_true")
    ap.add_argument("--g6", action="store_true", help="A43 G6 at --n rows (default 6000) -> <out-dir>/G6_AT_<n>.json")
    ap.add_argument("--score", action="store_true")
    ap.add_argument("--audit-failed", nargs="*", default=[])
    a = ap.parse_args(argv)
    log = lambda m: print(m, file=sys.stderr, flush=True)  # noqa: E731
    if a.score:
        install_loader(a.supp_dir)
        print(json.dumps(score(write=not a.dry_run, audit_failed=tuple(a.audit_failed)), indent=1, ensure_ascii=False,
                         default=str)[:20000])
        return 0
    if a.g6:
        res = g6_at_size(a.n or 6000, Path(a.out_dir), a.supp_dir, log)
        print(json.dumps({k: res[k] for k in ("family", "n_rows", "G6_verdict", "G7_verdict", "G10_verdict", "seconds")}))
        return 0 if res["G6_verdict"] == "pass" else 3
    rep = run(Path(a.out_dir), a.n or PI.N_ROWS, write=not a.dry_run, run_g15=not a.no_g15, supp=a.supp_dir, log=log)
    print(json.dumps({"summary": rep["summary"], "gate_lines": rep["gate_lines"], "rows_sha256": rep["files"]["rows_sha256"],
                      "relations_sha256": rep["files"]["relations_sha256"]}, indent=1, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
