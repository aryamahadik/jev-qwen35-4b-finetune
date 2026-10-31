"""F6 carry (STAGED, needs an orchestrator ruling before it writes to crowd_r1/): the round-1 selection record select_F6.json for
the v2 candidates with a C1-ONLY crowd (A37 e: "the crowd becomes C1-only; bins and selection unchanged"). Same code as
c_build/crowd_select.py cmd_select (imported, never edited): select_any / g5_reread / load_family on the v2 candidates, target =
TARGET_R1['F6'] (3,600), seed 20261003, key 'F6'. Only the crowd differs: p_g = C1's p_g (the 4B-E and base0 labels of the
round-1 3-model crowd no longer exist and may not be read). No G13 exclusion here (round 1 applied none for F6).
usage: r1_select_c1only.py --out DIR [--install]    DIR defaults to zed_orch/f6_carry/r1_select_scratch (dry run);
--install writes c_build/crowd_r1/select_F6.json + g5_reread_F6.json (the old pair is copied to zed_orch/f6_carry/backup first).
Counts only on stdout."""
import sys, json, shutil, argparse
from pathlib import Path
LEAN = Path("/Users/aryamahadik/Documents/jev/opendecide-data/lean")
sys.path.insert(0, str(LEAN / "c_build")); sys.path.insert(0, str(LEAN))
import crowd_select as cs
from mixio import InputLog, sha256_file, write_json
ap = argparse.ArgumentParser(); ap.add_argument("--out", default=str(LEAN / "c2_build/zed_orch/f6_carry/r1_select_scratch")); ap.add_argument("--install", action="store_true")
a = ap.parse_args()
fam = "F6"
cs.CROWD = {"c1": cs.CROWD["c1"]}                                   # C1 only
ilog = InputLog()
rows, rels = cs.load_family(ilog, fam)
units = cs.units_of(rows, rels)
sd = LEAN / "data/c2_crowd_shards" / fam                            # the v2 shards + C1 one-view labels (see verify_crowd_labels)
pg = cs.load_crowd(ilog, rows, {"c1": sd / "labels_q35_4b_main500k"}, sd)
res = cs.select_any(rows, units, pg, cs.TARGET_R1[fam], key=fam)
g5 = cs.g5_reread(rows, units, res["sel"], pg, fam)
ids = [rows[i]["id"] for u in res["sel"] for i in units[u]]
rec = {"family": fam, "target": cs.TARGET_R1[fam], "seed": cs.SEED, "crowd": {"c1": "q35_4b_main500k"},
       "crowd_note": "C1-only (A37 e); round-1 3-model crowd unavailable for the v2 rebuild",
       "candidates_sha256": sha256_file(cs.fam_files(fam)["cand"]), "report": res["report"], "budget": res["budget"],
       "easy_dropped_units": res["easy_dropped_units"], "reflow": res.get("reflow", []), "selected_ids": ids,
       "crowd_pg": {r["id"]: round(pg[r["id"]], 4) for r in rows}, "difficulty_bin": {r["id"]: res["bins"][r["id"]] for r in rows}}
if a.install:
    for n in ("select_F6.json", "g5_reread_F6.json"):
        shutil.copy2(cs.OUT / n, LEAN / "c2_build/zed_orch/f6_carry/backup" / ("pre_v2_" + n))
    write_json(cs.OUT / "select_F6.json", rec); write_json(cs.OUT / "g5_reread_F6.json", g5); where = str(cs.OUT)
else:
    Path(a.out).mkdir(parents=True, exist_ok=True)
    json.dump(rec, open(Path(a.out) / "select_F6.json", "w")); json.dump(g5, open(Path(a.out) / "g5_reread_F6.json", "w")); where = a.out
print(json.dumps({"rows": len(rows), "selected": len(ids), "bins": res["report"].get("bins"), "pass": res["report"].get("pass"),
                  "g5_low": g5["n_low"], "g5_sample": g5["n_sample"], "cand_sha": rec["candidates_sha256"][:12], "written_to": where}))
