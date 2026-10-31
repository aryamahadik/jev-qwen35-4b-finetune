"""Package DI-KR into lean/data/c2_parts/DI-KR/{out,hold_owndev,qc} (like SB5). Usage: python -I -B kr_package.py <candidates.jsonl> <owndev.jsonl> <stage note> [<qc json>]
Writes out/candidates_c2.jsonl, out/candidates_c2.relations.jsonl (empty: no twins from DI rows in C2), hold_owndev/mixdev_S5.jsonl (own dev: NOT out/, so no G13 log goes stale;
the orchestrator moves it at the G13 re-run), out/MANIFEST.json, qc/QC_REPORT.json."""
import json, sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
from kr_lib import *
import c2io
cand, dev, note = sys.argv[1:4]
qc = json.load(open(sys.argv[4])) if len(sys.argv) > 4 else {"pass": None, "stage": note}
out = LEAN / "data/c2_parts/DI-KR/out"; out.mkdir(parents=True, exist_ok=True); (out.parent / "qc").mkdir(exist_ok=True)
rows = [json.loads(l) for l in open(cand, encoding="utf-8")]
drows = [json.loads(l) for l in open(dev, encoding="utf-8")]
hold = out.parent / "hold_owndev"; hold.mkdir(exist_ok=True)
files = {}
for name, rs in ((c2io.CAND, rows), (c2io.REL, []), ("mixdev_S5.jsonl", drows)):
    d = hold if name == "mixdev_S5.jsonl" else out
    c2io.write_jsonl(d / name, rs)
    b = (d / name).read_bytes()
    files[name] = {"sha256": sha(b), "rows": len(rs)}
G1 = json.load(open(KR / "G1_RECORD.json"))
man = {"family": "DI-KR", "stage": note,
       "parents": [{"dataset": "GSM8K (openai/grade-school-math), main train split only", "source_licence": "MIT (repo LICENSE at the pinned commit; V)",
                    "pinned_commit": G1["pinned_commit"], "train_jsonl_sha256": G1["files"]["train.jsonl"]["sha256"], "licence_sha256": G1["files"]["LICENSE"]["sha256"],
                    "labels": "human-written solutions; gold re-derived by a pure-arithmetic AST evaluator; distractor options program-made (seed 20261013)"}],
       "ruling": "A61 (draft) DI-KR; head: choice; options = gold + 3 numerically distinct distractors in one number format",
       "inputs": {"pool.json": sha((WORK / "pool.json").read_bytes()), "build": "zed_orch/di_train/DI-KR/tools/kr_prep.py + kr_rows.py + kr_cand.py"},
       "files": {k: v for k, v in files.items() if k != "mixdev_S5.jsonl"}, "own_dev": {"mixdev_S5.jsonl": files["mixdev_S5.jsonl"]}}
(out / c2io.MAN).write_text(json.dumps(man, indent=1, ensure_ascii=False) + "\n")
(out.parent / "qc" / c2io.QC).write_text(json.dumps(qc, indent=1, ensure_ascii=False) + "\n")
print(json.dumps({"files": files, "problems": c2io.candidate_problems("DI-KR", rows)}))
