"""A45 pre-freeze gate driver for T44 (in memory; writes only a small JSON summary of gate numbers, no rows).
  ../../.venv/bin/python -B families/T44/t44_prefreeze.py [rows=6000] [out=families/T44/A45_CHECK_<rows>.json]   (from c2_build)
Covers: program gates (G2 G3 G4 G-SL G-LEX G-TW G15 schema options; G15 on a 400-row slice), G6 pooled + per head, G7, G10,
the options-only and formatting-only probes, tokens, cards, label / position / length shares, algebra count, the 3% reseed audit."""
import collections, hashlib, json, os, statistics, sys, time
from pathlib import Path
sys.dont_write_bytecode = True
sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
import pilot, pilot_loaders as PL  # noqa: E402
from c2_kit.distractors import uhash  # noqa: E402
from families.T44 import probes as PR  # noqa: E402
from families.T44 import run_pilot_i1 as RUN  # noqa: E402

n = int(sys.argv[1]) if len(sys.argv) > 1 else 6000
out_p = sys.argv[2] if len(sys.argv) > 2 else f"families/T44/A45_CHECK_{n}.json"
t0 = time.time()
PL.LOADERS["T44"] = RUN._t44
RUN.install_patches()
with PL.LOADERS["T44"]() as kit:
    b = pilot.build_pilot(kit, n, run_g15=False, log=lambda m: print(m, file=sys.stderr, flush=True))
    pl, ctx = kit.plugin, kit.ctx
    infos = b.infos
    rows = [i.row for i in infos]
    gates = pilot.program_gates(b)
    g6, g7, g10 = pilot.g6(infos), pilot.g7(infos), pilot.g10(infos, b.units, pl)
    per_head = {}
    for h in PR.HEADS:
        part = [i for i in infos if i.row["meta"]["qform"] == h]
        if len(part) < 20:
            continue
        g = pilot.g6_choice(part)
        views = {v: g[v] for v in ("a_question", "b_options", "c_card_without_question", "d_meta") if v in g}
        fails = [(v, m, a) for v, d in views.items() for m, a in d.items() if a > g["chance"] + 0.02 + 1e-12]
        per_head[h] = {"n": len(part), "chance": g["chance"], "views": views, "fails": fails}
    probe_o, probe_f = PR.options_only(infos), PR.formatting_only(infos)
    toks, how = pilot.real_tokens(rows)
    cards = collections.Counter(r["meta"]["card_id"] for r in rows)
    lab = collections.Counter(r["gold"].split("_")[0] if r["meta"]["qform"] == "ch_verdict" else "call" for r in rows)
    algs = {i.spec.structure["alg"]["id"] for i in infos}
    algs_struct = {hashlib.sha256(json.dumps(i.spec.structure["alg"]["tools"], sort_keys=True).encode()).hexdigest() for i in infos}
    # G15 on a slice (the loader round trip is per row; a 500-row slice keeps the run short)
    from c2_kit import rows as KR
    g15_bad = sum(not KR.g15_check(r)["ok"] for r in rows[:500])
    # 3% reseed audit: the same row cell re-drawn from an independent random stream
    aud = [i for i in infos if uhash(i.row["id"], "reseed") < 0.03]
    flips = disagree = orig_b = 0
    for i in aud:
        sp = i.spec
        sp2 = pl.sample(sp.seed, sp.sampler, reseed="audit")
        a2 = pl.solve_a(sp2)
        b2 = pl.solve_b(pl.parse(pl.render(sp2, ctx).row, ctx))
        disagree += a2 != b2
        if sp.qform == "ch_verdict":
            flips += a2 != i.row["gold"]
        orig_b += pl.solve_b(pl.parse(i.row, ctx)) != i.row["gold"]
    res = {"rows": len(rows), "units": len(b.units), "attempted": b.stats["units_attempted"], "drops": b.stats["drops_by_gate"],
           "per_sampler": b.stats["per_sampler"],
           "program_gates_failed_units": {k: v["units_failed"] for k, v in gates.items() if k in pilot.PROGRAM_GATES},
           "G15_slice_500_failed": g15_bad,
           "G6": {"verdict": g6["verdict"], "fails": g6["fails"], "choice": g6["choice"], "per_head": per_head},
           "G7": {"verdict": g7["verdict"], "n_tests": g7["n_tests"], "choice_fails": g7["choice_fails"][:8]},
           "G10": {"verdict": g10["verdict"], "failing": g10["failing"]},
           "probe_options_only": probe_o, "probe_formatting_only": probe_f,
           "tokens": {"mean": round(statistics.mean(toks), 1), "max": max(toks), "by": how},
           "cards": {"n": len(cards), "max_rows": max(cards.values()), "min_rows": min(cards.values())},
           "label_share": {k: round(v / len(rows), 4) for k, v in sorted(lab.items())},
           "head_share": {h: round(sum(r["meta"]["qform"] == h for r in rows) / len(rows), 4) for h in PR.HEADS},
           "algebras": {"distinct_ids": len(algs), "distinct_tool_structures": len(algs_struct)},
           "reseed": {"audited": len(aud), "verdict_label_flips": flips, "A_vs_B_disagreements": disagree,
                      "B_vs_original_gold": orig_b},
           "seconds": round(time.time() - t0)}
Path(out_p).write_text(json.dumps(res, indent=1, default=str))
print(json.dumps({k: res[k] for k in ("rows", "attempted", "program_gates_failed_units", "tokens", "cards", "reseed", "seconds")}, default=str))
print("G6", g6["verdict"], g6["fails"][:4], "| G7", g7["verdict"], "| G10", g10["verdict"], g10["failing"])
print("per head fails", {h: v["fails"] for h, v in per_head.items()})
print("options", probe_o["pass"], "formatting", probe_f["pass"])
