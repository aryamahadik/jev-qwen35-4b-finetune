"""A50 G6 builds, version b (g6_a50.py plus --plugin-file, --src, --name; a separate file because g6_a50.py was overwritten
by a pull from the VM).  No existing runner, plugin or generator is edited.

  build one 6,000-row in-memory QC build at a seed base (G15 off), pilot.g6 only, every view x model cell saved:
    ../../.venv/bin/python -B zed_orch/g6_a50b.py build FAMILY --seed-base N [--n 6000] --out FILE.json [--plugin-file P]
  average four builds (A50 a) and write the verdict:
    ../../.venv/bin/python -B zed_orch/g6_a50b.py agg FAMILY --dir DIR [--src DIR2] [--name G6_A50.json] [--bases ...]

Each family goes through the SAME build path as its binding 6,000-row G6 run:
  T19, T20      pilot_loaders.open_family (= zed_orch/g6_at_size.py)
  T29           families/T29/run_pilot_i4.py loader patch (pools/dneg supplement + a43f quarantine), imported unchanged
  T35           families/T35/run_pilot_i4.py install_loader (a43f quarantine), imported unchanged
  T36           pilot_loaders.open_family (= transfer/T36/g6_seedbase.py)
Only the seed base differs (pilot.build_pilot's own seed_base argument). --plugin-file loads another plugin.py in memory.
Run from lean/c2_build."""
import argparse, contextlib, importlib, json, sys, time
from pathlib import Path
sys.dont_write_bytecode = True
C2 = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(C2))

BASES = (900000, 11000000, 12000000, 13000000)
FAMDIR = {"T29": "families/T29/pilot_i4", "T35": "families/T35/pilot_i4", "T36": "transfer/T36/pilot_i2",
          "T20": "transfer/T20/pilot_i3", "T19": "transfer/T19/pilot_i2"}


def build(a):
    import pilot, pilot_loaders as PL
    fam = a.family
    if a.plugin_file:   # another plugin.py (e.g. a _backup_*/plugin.py) loaded in memory as families.<F>.plugin
        import types
        importlib.import_module(f"families.{fam}")
        live = C2 / "families" / fam / "plugin.py"          # keep __file__ = the live path so pools/ and G0_SPEC.md resolve
        mod = types.ModuleType(f"families.{fam}.plugin")
        mod.__file__ = str(live)
        mod.__package__ = f"families.{fam}"
        sys.modules[mod.__name__] = mod
        exec(compile(Path(a.plugin_file).read_text(encoding="utf-8"), str(live), "exec"), mod.__dict__)
        setattr(sys.modules[f"families.{fam}"], "plugin", mod)
    if fam == "T29":
        R = importlib.import_module("families.T29.run_pilot_i4")
        orig = PL.open_family

        @contextlib.contextmanager
        def patched(fid):  # identical to run_pilot_i4.main's patched()
            with orig(fid) as kit0:
                kit = R.without_quarantine(R.with_dneg(kit0))
                kit.dir = R._Dir(kit.dir)
                yield kit
        PL.open_family = patched
    elif fam == "T35":
        R = importlib.import_module("families.T35.run_pilot_i4")
        R.install_loader()
    t0 = time.time()
    with PL.open_family(fam) as kit:
        b = pilot.build_pilot(kit, a.n, seed_base=a.seed_base, run_g15=False)
        g6 = pilot.g6(b.infos)
    parts = {}
    for part in ("yes_no", "choice"):
        p = g6.get(part) or {}
        if p.get("n"):
            parts[part] = {"n": p["n"], "chance": p["chance"],
                           "views": {v: {m: p[v][m] for m in ("lr", "gbt")} for v in p
                                     if isinstance(p[v], dict) and "lr" in p[v]}}
    out = {"family": fam, "plugin_file": a.plugin_file or f"live families/{fam}/plugin.py", "seed_base": a.seed_base,
           "n_rows_requested": a.n, "n_rows": len(b.infos), "seconds": round(time.time() - t0), "G15": "off",
           "G6_verdict": g6["verdict"], "G6_fails": g6["fails"], "parts": parts}
    Path(a.out).write_text(json.dumps(out, indent=1, default=str))
    print(json.dumps({k: out[k] for k in ("family", "seed_base", "n_rows", "G6_verdict", "seconds")}))


def agg(a):
    d = C2 / a.dir
    s = C2 / (a.src or a.dir)
    builds = []
    for sb in a.bases:
        builds.append(json.loads((s / f"G6_A50_b{sb}.json").read_text()))
        assert builds[-1]["seed_base"] == sb and builds[-1]["family"] == a.family, sb
    cells, tables = {}, {}
    for part in ("yes_no", "choice"):
        tables[part] = {"n": [b["parts"][part]["n"] for b in builds], "chance": [b["parts"][part]["chance"] for b in builds]}
        mch = sum(tables[part]["chance"]) / len(builds)
        tables[part]["mean_chance"] = round(mch, 4)
        tables[part]["bar"] = round(mch + 0.02, 4)
        for v in builds[0]["parts"][part]["views"]:
            for m in ("lr", "gbt"):
                acc = [b["parts"][part]["views"][v][m] for b in builds]
                exc = [x - c for x, c in zip(acc, tables[part]["chance"])]
                me = sum(exc) / len(exc)
                cells[f"{part}/{v}/{m}"] = {"acc": acc, "excess": [round(e, 4) for e in exc],
                                            "mean_acc": round(sum(acc) / len(acc), 4), "mean_excess": round(me, 5),
                                            "mean_chance": round(mch, 4), "bar_excess": 0.02,
                                            "pass": bool(me <= 0.02 + 1e-9)}
    worst = max(cells, key=lambda k: cells[k]["mean_excess"])
    wp = worst.split("/")[0]
    res = {"ruling": "A50 (a): mean over four independent 6,000-row QC builds of each view x model cell's excess over chance; "
                     "bar: every cell mean <= chance + 2 pp", "family": a.family, "plugin_file": builds[0].get("plugin_file"),
           "seed_bases": list(a.bases), "G15": "off", "n_rows_per_build": [b["n_rows"] for b in builds],
           "seconds_per_build": [b["seconds"] for b in builds],
           "per_build_G6_verdict_unaveraged": [b["G6_verdict"] for b in builds], "parts": tables, "cells": cells,
           "worst_cell": {"cell": worst, "mean_excess_pp": round(cells[worst]["mean_excess"] * 100, 2),
                          "mean_acc": cells[worst]["mean_acc"], "mean_chance": cells[worst]["mean_chance"],
                          "bar": tables[wp]["bar"]},
           "worst_by_part": {p: max((k for k in cells if k.startswith(p + "/")), key=lambda k: cells[k]["mean_excess"])
                             for p in tables},
           "failing_cells": [k for k in cells if not cells[k]["pass"]],
           "verdict": "pass" if all(c["pass"] for c in cells.values()) else "fail"}
    (d / a.name).write_text(json.dumps(res, indent=1))
    w = res["worst_cell"]
    print(a.family, res["verdict"], "worst", w["cell"], f"{w['mean_excess_pp']:+.2f} pp", "mean_acc", w["mean_acc"],
          "mean_chance", w["mean_chance"], "bar", w["bar"], "failing:", res["failing_cells"], "| plugin:", res["plugin_file"])
    for sb, b in zip(a.bases, builds):
        mx = max(((b["parts"][p]["views"][v][m] - b["parts"][p]["chance"], p, v, m) for p in b["parts"]
                  for v in b["parts"][p]["views"] for m in ("lr", "gbt")))
        print(f"   build {sb}: max single-build excess {mx[0]*100:+.2f} pp ({mx[1]}/{mx[2]}/{mx[3]}), rows {b['n_rows']}")


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    sub = ap.add_subparsers(dest="cmd", required=True)
    b = sub.add_parser("build")
    b.add_argument("family", choices=sorted(FAMDIR))
    b.add_argument("--seed-base", type=int, required=True)
    b.add_argument("--n", type=int, default=6000)
    b.add_argument("--out", required=True)
    b.add_argument("--plugin-file", default=None, help="use this plugin.py instead of the live one (in memory only)")
    g = sub.add_parser("agg")
    g.add_argument("family", choices=sorted(FAMDIR))
    g.add_argument("--dir", required=True, help="folder that receives the result")
    g.add_argument("--src", default=None, help="folder holding G6_A50_b<base>.json (default: --dir)")
    g.add_argument("--name", default="G6_A50.json")
    g.add_argument("--bases", type=int, nargs="+", default=list(BASES))
    args = ap.parse_args()
    {"build": build, "agg": agg}[args.cmd](args)
