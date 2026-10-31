"""A50 (a) G6 for FULL GENERATION: three more independent 6,000-row QC builds per family (seed bases 11M, 12M, 13M) through
gen_full_c2.py's own QC path (loader_patch + quarantine exclusions + Redraw + pilot.build_pilot(run_g15=False) + pilot.g6),
averaged with B0 = the family's existing 6,000-row QC build (its GEN_REPORT gates.G6, at the QC base GEN_REPORT names).

  build:  ../.venv/bin/python -B zed_orch/g6_a50_full.py build FAM --seed-base N [--n 6000] [--out FILE]
          (default out: zed_orch/a50/<FAM>_b<N>.json; every view x model cell is saved)
  agg:    ../.venv/bin/python -B zed_orch/g6_a50_full.py agg FAM [--no-write-reports]
          averages B0 + the three builds, writes data/c2_parts/<FAM>/qc/G6_A50.json, and records G6_A50 / pass_a50 in the
          family's GEN_REPORT.json and QC_REPORT.json (the 24K result and the 6k result stay as diagnostics).
Run from lean/c2_build. No generator, plugin or label is touched."""
import argparse, json, sys, time
from pathlib import Path
sys.dont_write_bytecode = True
C2 = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(C2))
import gen_full_c2 as G  # noqa: E402

NEW_BASES = (11_000_000, 12_000_000, 13_000_000)
OUTDIR = C2 / "zed_orch" / "a50"


def build(a):
    fam = a.family
    G.check_family(fam)
    t0 = time.time()
    src = G.quarantine_sources(fam)
    banned = set().union(*map(set, src.values()))
    with G.loader_patch(fam):
        with G.PL.open_family(fam) as kit0:
            kit, xrep = G.apply_exclusions(kit0, banned)
            use_redraw = (not a.no_redraw) and fam not in G.FALLBACK_FAMILIES and bool(xrep["dead_qforms"])
            rd = G.Redraw(kit.plugin, xrep["dead_qforms"]) if use_redraw else None
            try:
                b = G.pilot.build_pilot(kit, a.n, seed_base=a.seed_base, run_g15=False)
            finally:
                if rd:
                    rd.restore()
            g6 = G.pilot.g6(b.infos)
            sm = G.g6_summary(g6)
            rec = {"family": fam, "seed_base": a.seed_base, "n_target": a.n, "n_rows": len(b.infos), "units": len(b.units),
                   "G15": "off", "loader": kit.loader, "skins_removed": xrep["skins_removed"], "dead_qforms": xrep["dead_qforms"],
                   "redraw_on": use_redraw, "redrawn": dict(rd.redrawn) if rd else {},
                   "rows_digest": G.rows_digest([i.row["id"] for i in b.infos]), "qc_build_stats": G._clean(b.stats),
                   "G6_verdict_single_build": sm["verdict"], "max_excess_pp": sm["max_excess_pp"], "max_cell": sm["max_cell"],
                   "cells": sm["cells"], "n_yes_no": sm["n_yes_no"], "n_choice": sm["n_choice"],
                   "seconds": round(time.time() - t0)}
    out = Path(a.out) if a.out else OUTDIR / f"{fam}_b{a.seed_base}.json"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(rec, indent=1, default=str))
    print(json.dumps({k: rec[k] for k in ("family", "seed_base", "n_rows", "units", "G6_verdict_single_build", "max_excess_pp",
                                          "max_cell", "seconds")}))


def b0_from_report(gen: dict) -> dict:
    g6 = gen["gates"]["G6"]
    sm = G.g6_summary(g6)
    return {"seed_base": gen["seeds"]["qc"], "n_rows": gen["qc_build"]["rows_written"], "units": gen["qc_build"]["units_written"],
            "cells": sm["cells"], "source": "GEN_REPORT.gates.G6 (the existing 6,000-row QC build)", "skins_removed":
            gen["exclusions"]["skins_removed"], "max_excess_pp": sm["max_excess_pp"], "max_cell": sm["max_cell"]}


def aggregate(fam: str, root: Path | None = None, write_reports: bool = True) -> dict:
    L = G.layout(fam, root)
    gen = json.loads(L["gen"].read_text())
    builds = [b0_from_report(gen)]
    for sb in NEW_BASES:
        builds.append(json.loads((OUTDIR / f"{fam}_b{sb}.json").read_text()))
        assert builds[-1]["family"] == fam and builds[-1]["seed_base"] == sb
    bases = [b["seed_base"] for b in builds]
    assert len(set(bases)) == 4, bases
    cells, parts = {}, {}
    for b in builds:
        for c in b["cells"]:
            cells.setdefault(f'{c["part"]}/{c["view"]}/{c["model"]}', []).append(c)
    for part in ("yes_no", "choice"):
        chs = [c["chance"] for c in cells.get(next((k for k in cells if k.startswith(part + "/")), ""), [])]
        if chs:
            parts[part] = {"n": [c["n"] for c in cells[next(k for k in cells if k.startswith(part + "/"))]], "chance": chs,
                           "mean_chance": round(sum(chs) / len(chs), 4), "bar": round(sum(chs) / len(chs) + 0.02, 4)}
    out_cells = {}
    for k, cs in cells.items():
        assert len(cs) == 4, (k, len(cs))
        exc = [c["acc"] - c["chance"] for c in cs]
        me = sum(exc) / 4
        part = k.split("/")[0]
        out_cells[k] = {"acc": [c["acc"] for c in cs], "chance": [c["chance"] for c in cs],
                        "excess_pp": [round(100 * e, 2) for e in exc], "mean_excess_pp": round(100 * me, 3),
                        "mean_acc": round(sum(c["acc"] for c in cs) / 4, 4), "mean_chance": parts[part]["mean_chance"],
                        "pass": bool(me <= 0.02 + 1e-9)}
    worst = max(out_cells, key=lambda k: out_cells[k]["mean_excess_pp"])
    res = {"ruling": "A50 (a), full generation: mean over four independent 6,000-row QC builds (B0 = the existing build + seed "
                     "bases 11,000,000 / 12,000,000 / 13,000,000) of each view x model cell's excess over chance; bar: every "
                     "cell mean <= chance + 2 pp", "family": fam, "G15": "off", "seed_bases": bases,
           "n_rows_per_build": [b["n_rows"] for b in builds], "units_per_build": [b["units"] for b in builds],
           "b0_source": builds[0]["source"], "parts": parts, "cells": out_cells,
           "worst_cell": {"cell": worst, "mean_excess_pp": out_cells[worst]["mean_excess_pp"],
                          "mean_acc": out_cells[worst]["mean_acc"], "mean_chance": out_cells[worst]["mean_chance"],
                          "bar_acc": parts[worst.split("/")[0]]["bar"]},
           "failing_cells": [k for k, c in out_cells.items() if not c["pass"]],
           "single_build_max_excess_pp": [{"seed_base": b["seed_base"], "max_excess_pp": b["max_excess_pp"], "max_cell": b["max_cell"]}
                                          for b in builds],
           "verdict": "pass" if all(c["pass"] for c in out_cells.values()) else "fail",
           "created_utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())}
    if write_reports:
        (L["qc"] / "G6_A50.json").write_text(json.dumps(res, indent=1))
        gates = gen["gates"]
        gates["G6_A50"] = {"gate": "G6_A50", "verdict": res["verdict"], "bar": "A50 (a): every view x model cell mean excess over "
                           "chance (mean of 4 independent 6,000-row builds) <= 2 pp", "seed_bases": bases,
                           "worst_cell": res["worst_cell"], "failing_cells": res["failing_cells"], "file": "qc/G6_A50.json"}
        probs = gen.get("candidate_problems") or []
        ok49, failing49 = G.program_pass_a49(gates, probs)
        failing50 = sorted(x for x in failing49 if x not in ("G6_24K", "G6_24K_missing"))
        if res["verdict"] == "fail":
            failing50.append("G6_A50")
        ok50 = not failing50
        gen.update({"program_pass_a50": ok50, "program_failing_a50": failing50})
        G.paths.write_json(L["gen"], G._clean(gen))
        q = json.loads(L["qcrep"].read_text())
        q.setdefault("gates", {})["G6_A50"] = res["verdict"]
        q["G6_A50"] = {"verdict": res["verdict"], "worst_cell": res["worst_cell"], "failing_cells": res["failing_cells"],
                       "seed_bases": bases, "file": "G6_A50.json"}
        g5 = q.get("gates", {}).get("G5-H")
        g3 = q.get("gates", {}).get("G3-H")
        q["pass_a50"] = bool(ok50 and g5 == "pass" and g3 in ("pass", "n/a")) if q.get("stage") == "final" else None
        q["program_failing_a50"] = failing50
        q["a50_note"] = ("A50: G6 binds as the mean of four 6,000-row builds (G6_A50); G6_24K and the 6k single build are "
                         "diagnostics; pass_a50 is null until G5-H / G3-H are final")
        G.paths.write_json(L["qcrep"], G._clean(q))
        res["program_pass_a50"] = ok50
        res["program_failing_a50"] = failing50
    return res


def main():
    ap = argparse.ArgumentParser()
    sub = ap.add_subparsers(dest="cmd", required=True)
    b = sub.add_parser("build")
    b.add_argument("family")
    b.add_argument("--seed-base", type=int, required=True)
    b.add_argument("--n", type=int, default=6000)
    b.add_argument("--out", default=None)
    b.add_argument("--no-redraw", action="store_true")
    g = sub.add_parser("agg")
    g.add_argument("family")
    g.add_argument("--no-write-reports", action="store_true")
    a = ap.parse_args()
    if a.cmd == "build":
        build(a)
    else:
        r = aggregate(a.family, write_reports=not a.no_write_reports)
        w = r["worst_cell"]
        print(a.family, r["verdict"], "worst", w["cell"], f'{w["mean_excess_pp"]:+.2f} pp', "failing", r["failing_cells"],
              "pass_a50", r.get("program_pass_a50"), r.get("program_failing_a50"))


if __name__ == "__main__":
    main()
