import sys, os, json, hashlib
sys.path.insert(0, '/Users/aryamahadik/Documents/jev/opendecide-data/lean/c2_build')
import pilot_t37b as P
rep = P.run(write=False, out_name="pilot_i1", log=lambda *_: None)
tasks = [t["task_sha256"] for g in rep["chunks"].values() for t in g]
print(os.environ.get("PYTHONHASHSEED"), rep["files"]["rows_sha256"][:16], rep["files"]["n_rows"],
      hashlib.sha256("|".join(tasks).encode()).hexdigest()[:16], len(tasks),
      round(rep["gates"]["G6"]["yes_no"]["d_meta"]["gbt"], 4), rep["gates"]["G10"]["checks"]["yes_rate"]["value"], flush=True)
