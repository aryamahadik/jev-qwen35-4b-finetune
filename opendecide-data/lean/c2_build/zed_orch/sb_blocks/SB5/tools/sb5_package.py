"""Package SB5 into lean/data/c2_parts/SB5/{out,qc}. Usage: python -B sb5_package.py <candidates.jsonl> <owndev.jsonl> <stage note> [<qc json>]
Writes out/candidates_c2.jsonl, out/candidates_c2.relations.jsonl (empty: no twins), out/mixdev_S5.jsonl (own dev), out/MANIFEST.json, qc/QC_REPORT.json."""
import json, sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
from sb5_lib import *
import c2io
cand, dev, note = sys.argv[1:4]
qc = json.load(open(sys.argv[4])) if len(sys.argv) > 4 else {"pass": None, "stage": note}
out = LEAN / "data/c2_parts/SB5/out"; out.mkdir(parents=True, exist_ok=True); (out.parent / "qc").mkdir(exist_ok=True)
rows = [json.loads(l) for l in open(cand, encoding="utf-8")]
drows = [json.loads(l) for l in open(dev, encoding="utf-8")]
files = {}
hold = out.parent / "hold_owndev"; hold.mkdir(exist_ok=True)   # NOT out/: a new out/mixdev_S5.jsonl makes every G13 log stale (c2_select.stale_problems); the orchestrator moves it at the G13 re-run
for name, rs in ((c2io.CAND, rows), (c2io.REL, []), ("mixdev_S5.jsonl", drows)):
    d = hold if name == "mixdev_S5.jsonl" else out
    c2io.write_jsonl(d / name, rs)
    b = (d / name).read_bytes()
    files[name] = {"sha256": sha(b), "rows": len(rs)}
G1 = json.load(open(SB5 / "G1_RECORD.json"))
man = {"family": "SB5", "stage": note,
       "parents": [{"dataset": "UCI Machine Learning Repository dataset 293, Twitter Data set for Arabic Sentiment Analysis (Abdulla and Mahyoub, 2013)",
                    "doi": "10.24432/C5F31B", "source_licence": "CC BY 4.0 (UCI dataset page, official record)",
                    "zip_sha256": G1["sha256"].get("zip") if isinstance(G1.get("sha256"), dict) and "zip" in G1["sha256"] else "a29250a60a18e1f02daf4ae4c4425113734d7cb79f353330815621c4ea4cd347",
                    "labels": "two native-speaker experts, a third breaks ties (UCI page, quoted in G1_RECORD.json)"}],
       "ruling": "A58 (draft) SB5; heads: yes/no (qtype noul); no neutral class in the source (reported)",
       "inputs": {"pool.json": sha((WORK / "pool.json").read_bytes()), "build": "zed_orch/sb_blocks/SB5/tools/sb5_prep.py + sb5_rows.py"},
       "files": {k: v for k, v in files.items() if k != "mixdev_S5.jsonl"}, "own_dev": {"mixdev_S5.jsonl": files["mixdev_S5.jsonl"]}}
(out / c2io.MAN).write_text(json.dumps(man, indent=1, ensure_ascii=False) + "\n")
(out.parent / "qc" / c2io.QC).write_text(json.dumps(qc, indent=1, ensure_ascii=False) + "\n")
print(json.dumps({"files": files, "problems": c2io.candidate_problems("SB5", rows)}))
