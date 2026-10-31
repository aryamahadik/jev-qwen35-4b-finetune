"""Re-fetch the public G13 reference sources deleted by the 11 Oct cleanup (HF dataset snapshots + TabFact repo).
Program-only: nothing here prints or reads item text. Used by c_build/decontam_g13.py through c2_build/g13_c2.py."""
import subprocess, sys, time
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "c_build"))
import decontam_g13 as g  # read-only: source list and paths
from huggingface_hub import snapshot_download

repos = [r for r in g.OHS_SRC_HF if r != g.BIGPAT] + ["btzsc/btzsc"]
for r in repos:
    for k in range(4):
        try:
            t = time.time(); snapshot_download(r, repo_type="dataset", max_workers=4)
            print(f"ok {r} {time.time()-t:.0f}s", flush=True); break
        except Exception as e:  # noqa: BLE001
            print(f"retry {r} {k}: {type(e).__name__}", flush=True); time.sleep(20)
gh = g.GH / "wenhuchen--Table-Fact-Checking"
if not gh.exists():
    gh.parent.mkdir(parents=True, exist_ok=True)
    subprocess.run(["git", "clone", "--depth", "1", "https://github.com/wenhuchen/Table-Fact-Checking", str(gh)], check=False)
print("bigpat:", g.fetch_bigpat(), flush=True)
