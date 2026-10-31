"""families/T31/run_pilot_i1.py: the T31 fix-iteration-1 pilot (C2_DATA_SPEC 6.4 step 6 then step 5 again) into pilot_i1/.

It is pilot.run_family (c2 pilot 1.0) with one change: the output folder is families/T31/pilot_i1/ instead of pilot/,
so the first pilot (pilot/: PILOT_REPORT.json, PILOT_VERDICT.json, the Haiku answers) stays as produced. Everything else
is pilot.py's own code: build_pilot (seed base 900000, the pilot seeds are unchanged), program_gates, G6, G7, G10, the
overlay, spec 3.0, the G5-H / G3-H task files. Program gates only: no Haiku or model is run; the task files are written,
never answered.

  cd lean/c2_build
  ../../.venv/bin/python -B families/T31/run_pilot_i1.py run                  # write pilot_i1/
  ../../.venv/bin/python -B families/T31/run_pilot_i1.py run --dry-run        # in memory, nothing written
  PYTHONHASHSEED=1 ../../.venv/bin/python -B families/T31/run_pilot_i1.py run --out-dir /somewhere/else   # determinism
  ../../.venv/bin/python -B families/T31/run_pilot_i1.py score                # after the Haiku answers exist

The fixes applied are listed in pilot_i1/FIX_I1.json (written by `run`).
"""
from __future__ import annotations

import argparse
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
OUT = HERE / "pilot_i1"
VERSION = PI.PILOT_VERSION + " / T31 fix iteration 1"


def run(out: Path = OUT, n_rows: int = PI.N_ROWS, *, write: bool = True, run_g15: bool = True, log=print) -> dict:
    with PL.open_family(FID) as kit:
        plugin = kit.plugin
        pdir = Path(out)
        log(f"{FID}: loader {kit.loader}; output {pdir}")
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
                         "note": ("Haiku answers pending; run `run_pilot_i1.py score` after they exist" if tasks3 else
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
                          "fix iteration 1 of at most 2 (6.4 step 6)",
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
            paths.write_json(pdir / "FIX_I1.json", fix)
        report["fix_i1"] = fix
        return report


# Measured in the fix session (14 Oct 2026) on in-memory builds with seed bases 1,000,000 .. 1,400,000 (NOT the pilot seeds);
# recorded here, not recomputed by this script: what the G6 d_meta ablation found and why the pilot-size verdict is mostly noise.
G6_NOISE = {
    "found_and_fixed": {
        "what": "ch_approver rows that show the escalate option: a gradient-boosted model on row-level counts (n_numbers, "
                "len_state, ...) plus option kinds picked the gold at +16.1 pp over chance on those rows (+12.6 .. +23.1 "
                "over 6 builds of 1,000 rows; +3.1 pp on all choice rows, the whole d_meta excess); rows without escalate "
                "-0.4 pp, ch_scope -2.3 pp. Cause: an escalate gold needs two competing records, a decoy did not.",
        "fix": "every row that shows escalate has the escalate-like shape whatever its gold (A: two delegations in their window "
               "+ one notice, B: one delegation + two overrides; per seed, 30% B); escalate gold, gold position and gold "
               "length rank are stratified per sampler over blocks of 1,024 seeds",
        "after": "pooled 593 shown rows: +12.9 pp (two delegations only) -> -1.4 pp (shapes A + B); d_meta GBT mean over the "
                 "6 builds +3.1 -> -1.5 pp"},
    "pilot_size_noise_floor": {
        "what": "12 random 1,000-row (unit-grouped) subsamples of an independent 5,000-row build, max excess over chance "
                "across the 8 choice comparisons (4 views x LR / GBT)",
        "true labels": "exceed +2 pp in 10 of 12 (range +0.9 to +8.3 pp); yes/no 7 of 12",
        "permuted labels (gold replaced by a random option per unit)": "exceed +2 pp in 9 of 12 (range +1.0 to +11.1 pp); "
                                                                     "yes/no 10 of 12",
        "6 builds after the fixes": "choice max excess +2.8, -1.1, +4.8, +4.5, +1.2, +2.8 pp (2 of 6 pass), yes/no -0.5, +3.1, "
                                    "+2.3, +2.4, +0.5, +0.6 pp (3 of 6 pass); the b_options / a_question GBT views, which "
                                    "cannot see structure, swing by +-5 pp",
        "5,000-row build (before the fixes)": "G7 0 failing features of 5,136 tests (Bonferroni p 1.9e-6); choice LR views "
                                              "+2.2 .. +3.3 pp against a unit-clustered permutation SD of 1.1-1.6 pp"},
    "reading": "At pilot size the G6 bars sit inside the noise floor of a label-free control, so a pass or a fail there "
               "cannot tell a leak from chance; the structural cue that the ablation could find is fixed. The bar was "
               "applied unchanged and is reported as measured. G7 at 5,000 rows, the G10 balance checks and the feature "
               "tables are clean."}


def fix_report(report: dict, rows: list) -> dict:
    """pilot_i1/FIX_I1.json: every PILOT_VERDICT fix (F01-F10, P1-P5) with its status and the pilot number that shows it."""
    g, it = report["gates"], report["iteration"]
    chk = lambda gate: g[gate]["checks"]  # noqa: E731
    yn = [r for r in rows if r["qtype"] == "noul"]
    tw = [r for r in yn if r["role"] == "twin"]
    ch = it["escalate_gold"]
    cells = {k: (v["abstain_gold"], v["rows"], v["expected"]) for k, v in it["plan_report"]["abstain_cells"].items()}
    mean = g["spec_3_0"]["checks"]["mean_tokens"]["value"]
    return {
        "family": FID, "stage": "fix iteration 1 of at most 2 (C2_DATA_SPEC 6.4 step 6)", "version": VERSION,
        "g0_sha256": report["g0_sha256"], "rows_sha256": report["files"]["rows_sha256"],
        "verdict_in": "pilot/PILOT_VERDICT.json (FIX)", "no_label_set": True, "no_haiku_or_model_run": True,
        "fixes": {
            "F01": {"status": "fixed", "how": "the 20 {cap|ITEM} skins are quarantined in plugin.ctx_for (I1_QUARANTINED_SKINS); "
                    "the kit's skin parser is untouched", "evidence": f"G3 units failed {g['G3']['units_failed']} / "
                    f"{g['G3']['units_attempted']}; quarantined pieces {len(it['quarantined_pieces'])}"},
            "F02": {"status": "fixed in the task text; G3-H re-read pending", "how": "extract_fields item = the noun phrase "
                    "without a leading article (g3h.compare is unchanged)", "evidence": f"{g['G3-H']['tasks']} G3-H task files "
                    f"for {g['G3-H']['items']} Mode F rows, not answered"},
            "F03": {"status": "fixed (screen); G3-H re-read pending", "how": "the 12 listed documents plus plugin.freeform_leaks "
                    "(a REQUESTER name word outside the value, a gendered pronoun, a claim phrase) screen 14 of 116 documents; "
                    "render refuses a leaking document", "evidence": f"Mode F share {g['spec_3_0']['checks']['mode_f_share']['value']}"},
            "F04": {"status": "fixed (+ a structure cue found by the G6 ablation and fixed)", "how": "choiceplan: escalate shown on "
                    "40%, gold 1/k of those; gold, position and length rank stratified per sampler over blocks of 1,024 seeds; "
                    "no twin where escalate is shown; every row that shows escalate has the escalate-like shape (G6_noise_floor)",
                    "evidence": {
                        "G7": f"choice fails {g['G7']['n_choice_fails']}", "escalate_gold": ch,
                        "cells (abstain gold, rows, expected)": cells,
                        "longest_option_gold_pp": chk("G10")["longest_option_gold_pp"]["value"],
                        "abstain_wrong_share": chk("G10")["abstain_wrong_share"]["verdict"],
                        "G6 choice (chance, best view)": [g["G6"]["choice"]["chance"], _g6_best(g["G6"]["choice"])]}},
            "F05": {"status": "fixed", "how": "a yes/no base has a one-slot flip with probability 0.90 (either answer); "
                    "twin proposals 60% yes/no, 100% of ch_approver rows that do not show escalate",
                    "evidence": {"twin yes rate": round(sum(r["gold"] for r in tw) / max(1, len(tw)), 3), "twins": len(tw),
                                 "yes rate": chk("G10")["yes_rate"]["value"], "twin_share": chk("overlay")["twin_share"]["value"]}},
            "F06": {"status": "fixed", "how": "the agent yes/no base form is drawn from all four forms; each negative base has "
                    "yn_agent_ok as its one complement", "evidence": f"yes_is_bad_share {chk('G10')['yes_is_bad_share']['value']}"},
            "F07": {"status": "PARTIAL: forms, fallback, polarity rule and authoring brief done; Haiku wordings OPEN",
                    "how": "yn_holder_dneg / yn_agent_dneg (4% of base specs each) are drawn only while a polarity-clean "
                    "wording is admitted (none is: they fall back); dneg_authoring.py holds the brief and the admission check",
                    "evidence": f"double_negation_share {chk('G10')['double_negation_share']['value']} (bar >= 0.02): G10 still fails",
                    "open": "Haiku authors the wordings from the brief, G-LEX 2/2, G13-seed, pool re-freeze, re-pilot"},
            "F08": {"status": "fixed", "how": "P_EQUIV 0.11 -> 0.15", "evidence": f"equiv_share {chk('overlay')['equiv_share']['value']}"},
            "F09": {"status": "fixed (A + B + C + D)", "how": "rules in row.card on yes/no rows (A); no heading line (B); compact and "
                    "short card styles (C); record counts and matrix sizes lowered, track split 55/45 (D)",
                    "evidence": f"mean tokens {mean} (bar 800), max {g['spec_3_0']['checks']['max_tokens']['value']} (bar 2000); "
                    f"card styles {it['card_styles']['defs_styles']}", "open": "the Haiku ambiguity re-pass of the v1.2 card text"},
            "F10": {"status": "fixed", "how": "pools_v2 packs and names wired, one pack per card (24 + 6 per track)",
                    "evidence": f"{it['packs']['distinct']} distinct packs over {it['packs']['cards']} cards; {it['names']} names",
                    "open": "G13-seed on the pools_v2 pieces (not run)"},
        },
        "before_full_generation": {
            "P1": {"status": "fixed", "evidence": f"register_max_share {g['spec_3_0']['checks']['register_max_share']['value']}"},
            "P2": {"status": "fixed", "how": "T31Ctx counts rows per skin (unit_rows_bound); the generator keeps one plugin "
                   "instance per run", "evidence": it["skin_rows"]},
            "P3": {"status": "kept", "evidence": f"mode_f_share {g['spec_3_0']['checks']['mode_f_share']['value']} (cap 0.25)"},
            "P4": {"status": "kept", "evidence": f"twin_share {chk('overlay')['twin_share']['value']} (20-25%)"},
            "P5": {"status": "OPEN", "what": "G13-seed on the wired pools_v2 packs / names and on the new dneg wordings once authored"}},
        "G6_noise_floor": G6_NOISE,
        "program_gates_after": [line for line in report["gate_lines"] if not line.startswith(("G3-H", "G5-H"))],
        "not_done_here": ["no Haiku or model run (G3-H, G5-H and the G0 ambiguity re-pass are pending)", "no label set or edited",
                          "no paid compute, no commit", "no gate bar loosened, no G0 target lowered"],
    }


def _g6_best(part: dict) -> str:
    best = max((part[v][m], v, m) for v in part if isinstance(part[v], dict) and "lr" in part[v] for m in ("lr", "gbt"))
    return f"{best[1]}/{best[2]} {best[0]}"


def iteration_report(b, plugin, kit) -> dict:
    """What the fixes did, measured on the pilot rows (report only; the gates are in PILOT_REPORT.gates)."""
    rows = [i.row for i in b.infos]
    sets = [rr.option_set for u in b.units for rr in u.rendered if rr.option_set is not None]
    c = Counter((r["role"], r["meta"]["qform"]) for r in rows)
    twins = Counter(r["meta"]["qform"] for r in rows if r["role"] == "twin")
    base = [r for r in rows if r["role"] == "base"]
    tags = Counter(t for r in base for t in r["meta"]["edge"])
    skins = Counter(r["meta"]["c2"]["skin_id"] for r in rows)
    ch = [r for r in rows if r["meta"]["qform"] == "ch_approver"]
    esc = sum(1 for r in ch if r["gold"].startswith("Escalate"))
    rep = CP.plan_report(sets)
    toks = CD.token_report(rows)
    return {
        "plan_report": rep,
        "escalate_gold": {"rows": len(ch), "gold_escalate": esc, "share": round(esc / max(1, len(ch)), 4)},
        "token_report": {k: toks[k] for k in ("mean", "max", "yes_no_share", "field_means", "rules_mean")},
        "card_styles": CD.style_report(rows),
        "base_forms": dict(Counter(r["meta"]["qform"] for r in base)),
        "twin_forms": dict(twins),
        "trap_shares_of_base_rows": {k: round(v / max(1, len(base)), 3) for k, v in sorted(tags.items())},
        "skin_rows": {"max": max(skins.values()), "n_skins": len(skins), "cap": plugin.skin_row_cap,
                      "cap_overflow": plugin.cap_overflow},
        "packs": {"distinct": len({r["meta"]["domain_pack"] for r in rows}),
                  "cards": len({r["meta"]["card_id"] for r in rows})},
        "names": len({s.value for i in b.infos for s in i.spec.all_slots().values()
                      if s.kind == "name" and s.value in set(plugin.names)}),
        "double_negation_forms_available": plugin.dneg_ok,
        "quarantined_pieces": {k: v for k, v in sorted(plugin.quarantined(kit.ctx).items())},
        "relations_by_form": {f"{r}|{q}": n for (r, q), n in sorted(c.items())},
    }


class _IterDir(type(Path())):
    """pilot.score_family reads PL.family_dir(fid) / "pilot"; here that is pilot_i1/."""

    def __truediv__(self, key):
        return Path(str(OUT)) if key == "pilot" else super().__truediv__(key)


def score(*, write: bool = True, audit_failed: tuple = ()) -> dict:
    """pilot.score_family over pilot_i1/ (after the Haiku answers exist): G3-H (g3h.compare, 98% per template) and the
    G5-H adjudication queue + 30 controls."""
    orig = PL.family_dir
    PL.family_dir = lambda fid: _IterDir(orig(fid))
    try:
        return PI.score_family(FID, write=write, audit_failed=audit_failed)
    finally:
        PL.family_dir = orig


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("cmd", choices=("run", "score"))
    ap.add_argument("--n", type=int, default=PI.N_ROWS)
    ap.add_argument("--out-dir", default=str(OUT))
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("--no-g15", action="store_true")
    ap.add_argument("--audit-failed", nargs="*", default=[])
    a = ap.parse_args(argv)
    if a.cmd == "run":
        rep = run(Path(a.out_dir), a.n, write=not a.dry_run, run_g15=not a.no_g15,
                  log=lambda m: print(m, file=sys.stderr, flush=True))
        print(json.dumps({"summary": rep["summary"], "gate_lines": rep["gate_lines"],
                          "rows_sha256": rep["files"]["rows_sha256"],
                          "relations_sha256": rep["files"]["relations_sha256"]}, indent=1, ensure_ascii=False))
        return 0
    print(json.dumps(score(write=not a.dry_run, audit_failed=tuple(a.audit_failed)), indent=1, ensure_ascii=False,
                     default=str)[:20000])
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
