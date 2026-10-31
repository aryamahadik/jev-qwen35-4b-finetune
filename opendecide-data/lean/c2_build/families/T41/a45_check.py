"""A45 pre-freeze check driver for T41 (in memory; writes only a small JSON summary of gate numbers, no rows).
  ../../.venv/bin/python -B families/T41/a45_check.py [rows=6000] [out=families/T41/A45_CHECK_<rows>.json]   (from c2_build)"""
import collections, json, statistics, sys, time
from pathlib import Path
sys.dont_write_bytecode = True
sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
import pilot, pilot_loaders as PL  # noqa: E402
from families.T41 import run_pilot_i1 as RUN  # noqa: E402
from families.T41.test_plugin import _cv_probe  # noqa: E402
n = int(sys.argv[1]) if len(sys.argv) > 1 else 6000
out_p = sys.argv[2] if len(sys.argv) > 2 else f"families/T41/A45_CHECK_{n}.json"
t0 = time.time()
RUN.register()
with PL.open_family("T41") as kit:
    SB = int(sys.argv[3]) if len(sys.argv) > 3 else pilot.SEED_BASE
    b = pilot.build_pilot(kit, n, run_g15=False, seed_base=SB)
pl = kit.plugin; infos = b.infos; rows = [i.row for i in infos]
lab = collections.Counter(pl._decide(i.spec) for i in infos)
toks, how = pilot.real_tokens(rows)
g6, g7, g10 = pilot.g6(infos), pilot.g7(infos), pilot.g10(infos, b.units, pl)
def fmt(i):
    r, m = i.row, i.row["meta"]
    return {"format": m["format_style"], "defs": m["defs_style"], "register": m["c2"]["register"],
            "layout": "|".join(h[:4] for h in [x for x in r["state"].split("\n") if x.endswith(":")][:8]),
            "n_lines": r["state"].count("\n"), "len_state": len(r["state"]) // 40, "len_ins": len(r["instructions"]) // 20,
            "card": bool(r.get("card"))}
fyn, nyn = _cv_probe(infos, fmt, "noul", pl); fch, nch = _cv_probe(infos, fmt, "choice", pl)
yn = [i for i in infos if i.row["qtype"] == "noul"]
maj = max(sum(i.row["gold"] for i in yn), len(yn) - sum(i.row["gold"] for i in yn)) / len(yn)
chl = collections.Counter(pl._decide(i.spec) for i in infos if i.row["qtype"] == "choice")
out = {"rows": len(rows), "n_yes_no": nyn, "n_choice": nch, "drops": b.stats["drops_by_gate"],
       "benign_share": round((lab["allow"] + lab["benign"]) / len(rows), 4),
       "label_share_choice": {k: round(v / nch, 4) for k, v in sorted(chl.items())}, "yes_majority": round(maj, 4),
       "mean_tokens": round(statistics.mean(toks), 1), "max_tokens": max(toks),
       "max_rows_per_card": max(collections.Counter(r["meta"]["card_id"] for r in rows).values()),
       "G6_verdict": g6["verdict"], "G6_fails": g6["fails"], "G6": {"yes_no": g6["yes_no"], "choice": g6["choice"]},
       "G7": {"verdict": g7["verdict"], "n_tests": g7["n_tests"]}, "G10": {"verdict": g10["verdict"], "failing": g10["failing"]},
       "probe_options_only_choice": g6["choice"]["b_options"], "probe_format_yes_no": fyn, "probe_format_choice": fch,
       "seconds": round(time.time() - t0)}
Path(out_p).write_text(json.dumps(out, indent=1, default=str))
print(json.dumps({k: out[k] for k in ("rows", "benign_share", "G6_verdict", "G7", "G10", "mean_tokens", "max_tokens", "seconds")}))
