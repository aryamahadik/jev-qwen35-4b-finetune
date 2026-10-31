"""families/T41/measure.py: the measured numbers of BUILD_NOTES.md (in memory; writes nothing).

  ../../.venv/bin/python -B families/T41/measure.py [rows=5000]      (from lean/c2_build; about 5 minutes)
"""
from __future__ import annotations

import collections
import json
import statistics
import sys
from pathlib import Path

sys.dont_write_bytecode = True
sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
import pilot  # noqa: E402
import pilot_loaders as PL  # noqa: E402
from families.T41 import run_pilot_i1 as RUN  # noqa: E402
from families.T41.test_plugin import _cv_probe  # noqa: E402

n = int(sys.argv[1]) if len(sys.argv) > 1 else 5000
RUN.register()
with PL.open_family("T41") as kit:
    b = pilot.build_pilot(kit, n, run_g15=False)
pl = kit.plugin
infos = b.infos
rows = [i.row for i in infos]
lab = collections.Counter(pl._decide(i.spec) for i in infos)
ch = collections.Counter(pl._decide(i.spec) for i in infos if i.row["qtype"] == "choice")
toks, how = pilot.real_tokens(rows)
g6, g7, g10 = pilot.g6(infos), pilot.g7(infos), pilot.g10(infos, b.units, pl)
ov = pilot.overlay(b.units, pl)


def fmt(i):
    r, m = i.row, i.row["meta"]
    return {"format": m["format_style"], "defs": m["defs_style"], "register": m["c2"]["register"],
            "layout": "|".join(h[:4] for h in [x for x in r["state"].split("\n") if x.endswith(":")][:8]),
            "n_lines": r["state"].count("\n"), "len_state": len(r["state"]) // 40, "len_ins": len(r["instructions"]) // 20,
            "card": bool(r.get("card"))}


fyn, _ = _cv_probe(infos, fmt, "noul", pl)
fch, _ = _cv_probe(infos, fmt, "choice", pl)
out = {"rows": len(rows), "units": len(b.units), "drops": b.stats["drops_by_gate"],
       "label_share_all": {k: round(v / len(rows), 4) for k, v in sorted(lab.items())},
       "benign_share": round((lab["allow"] + lab["benign"]) / len(rows), 4),
       "label_share_choice": {k: round(v / sum(ch.values()), 4) for k, v in sorted(ch.items())},
       "yes_no_share": g10["checks"]["yes_no_share"]["value"], "yes_rate": g10["checks"]["yes_rate"]["value"],
       "mean_tokens": round(statistics.mean(toks), 1), "max_tokens": max(toks), "tokenizer": how,
       "G6": {"verdict": g6["verdict"], "yes_no": {k: g6["yes_no"][k] for k in ("a_question", "c_card_without_question", "d_meta")},
              "choice": {k: g6["choice"][k] for k in ("a_question", "b_options", "c_card_without_question", "d_meta")}},
       "G7": {"verdict": g7["verdict"], "n_tests": g7["n_tests"]},
       "G10": {"verdict": g10["verdict"], "failing": g10["failing"]},
       "overlay": {k: v["value"] for k, v in ov["checks"].items()},
       "probes": {"options_only_choice": g6["choice"]["b_options"], "formatting_only_yes_no": fyn,
                  "formatting_only_choice": fch},
       "cards": len({r["meta"]["card_id"] for r in rows}),
       "max_rows_per_card": max(collections.Counter(r["meta"]["card_id"] for r in rows).values())}
print(json.dumps(out, indent=1))
