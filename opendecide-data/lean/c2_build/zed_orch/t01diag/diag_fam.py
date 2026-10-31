"""Family-generic attribution run (in memory). variant runner = the family's loader patch only (what the latest runner builds),
variant tool = gen_full_c2's build (loader patch + apply_exclusions + Redraw). Same pilot.build_pilot call as pilot.run_family."""
from __future__ import annotations
import argparse, json, sys, time
from collections import Counter
from pathlib import Path
sys.dont_write_bytecode = True
HERE = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(HERE))
import pilot, gen_full_c2 as GF, pilot_loaders as PL  # noqa: E402

ap = argparse.ArgumentParser()
ap.add_argument("--family", required=True); ap.add_argument("--variant", choices=("runner", "tool"), required=True)
ap.add_argument("--seed-base", type=int, required=True); ap.add_argument("--n", type=int, required=True)
ap.add_argument("--g15", type=int, default=1); ap.add_argument("--g6", type=int, default=0); ap.add_argument("--out", required=True)
a = ap.parse_args(); fam = a.family; t0 = time.time()
src = GF.quarantine_sources(fam); banned = set().union(*map(set, src.values()))
with GF.loader_patch(fam):
    with PL.open_family(fam) as kit0:
        rd = None; xinfo = None
        if a.variant == "tool":
            kit, x = GF.apply_exclusions(kit0, banned); xinfo = {k: x[k] for k in ("skins_removed", "dead_qforms", "wordings_before", "wordings_after")}
            if x["dead_qforms"] and fam not in GF.FALLBACK_FAMILIES:
                rd = GF.Redraw(kit.plugin, x["dead_qforms"])
        else:
            kit = kit0
        try:
            b = pilot.build_pilot(kit, a.n, seed_base=a.seed_base, run_g15=bool(a.g15))
        finally:
            if rd: rd.restore()
        infos, plugin = b.infos, kit.plugin
        rows = [i.row for i in infos]
        body = "".join(json.dumps(r, ensure_ascii=False) + "\n" for r in rows)
        out = {"family": fam, "variant": a.variant, "seed_base": a.seed_base, "n_rows": len(rows), "rows_sha256": pilot.sha_text(body),
               "exclusion": xinfo, "redrawn": dict(rd.redrawn) if rd else None, "qtype": dict(Counter(r["qtype"] for r in rows)),
               "qform": dict(Counter(r["meta"]["qform"] for r in rows))}
        yn = [r for r in rows if r["qtype"] == "noul"]
        out["yes_no_share"] = round(len(yn) / len(rows), 4); out["yes_rate"] = round(sum(int(r["gold"]) for r in yn) / max(1, len(yn)), 4)
        g10 = pilot.g10(infos, b.units, plugin); chk = g10["checks"]
        out["G10_failing"] = g10.get("failing")
        out["G10"] = {k: {"verdict": v["verdict"], "value": v["value"]} for k, v in chk.items() if v["verdict"] == "fail" or k in ("yes_no_share", "yes_rate", "longest_option_gold_pp", "yes_is_bad_share")}
        g11 = GF.g11_shares(infos, plugin); out["G11"] = {k: g11[k] for k in ("max_template_share", "templates_over_bar", "verdict")}
        ov = pilot.overlay(b.units, plugin); out["overlay_verdict"] = ov.get("verdict"); out["overlay"] = ov.get("report")
        s30 = pilot.spec30(infos, plugin); out["spec30_verdict"] = s30.get("verdict")
        out["spec30_fail"] = {k: v for k, v in (s30.get("checks") or {}).items() if v.get("verdict") == "fail"}
        out["build"] = {k: b.stats[k] for k in ("rows_written", "units_written", "units_attempted", "drops_by_gate")}
        if a.g6:
            g6 = pilot.g6(infos); out["G6_verdict"] = g6["verdict"]
            out["G6_fails"] = [(f["part"], f["view"], f["model"], f["acc"], f["chance"], round(100 * (f["acc"] - f["chance"]), 2)) for f in g6["fails"]]
            out["G6_cells"] = {p: {v: g6[p][v] for v in g6[p] if isinstance(g6[p][v], dict) and "lr" in g6[p][v]} | {"chance": g6[p].get("chance")} for p in ("yes_no", "choice")}
out["seconds"] = round(time.time() - t0)
Path(a.out).write_text(json.dumps(out, indent=1, default=str)); print(a.family, a.variant, a.seed_base, out["rows_sha256"][:12], out["yes_no_share"], out["G10_failing"], out["seconds"])
