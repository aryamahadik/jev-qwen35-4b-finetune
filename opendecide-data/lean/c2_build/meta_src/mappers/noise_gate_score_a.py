"""noise_gate_score_a.py <source>: score the A42-D 8.4 noise gate once Haiku has written noise_gate/answers/<chunk>.json.

Answer file: {"<qid>": {"answer": "yes"|"no"|<option text>}} (or a list of {"qid", "answer"}), as chunker.load_answers reads.
A row disagrees when the normalized Haiku answer differs from gold or is invalid. A task with >= 2 disagreeing rows of its 13
goes to review: Sonnet first pass, Opus confirms (A43 d); the task is dropped only if >= 2 of the 13 are confirmed clearly
wrong. Rows are never edited. CPU only.
"""
import json
import sys
from collections import defaultdict
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import _common_a  # noqa: E402,F401  (puts c2_build on sys.path)
from c2_kit import g5h  # noqa: E402

LEAN = HERE.parents[2]


def main(src):
    base = LEAN / "data" / "c2_md_parts" / src
    rows = {json.loads(l)["id"]: json.loads(l) for l in open(base / "rows.jsonl")}
    key = {}
    for f in (base / "noise_gate_orch" / "key").glob("*.json"):
        key.update(json.loads(f.read_text())["key"])
    ans = {}
    for f in (base / "noise_gate" / "answers").glob("*.json"):
        raw = json.loads(f.read_text())
        pairs = [(a["qid"], a) for a in raw] if isinstance(raw, list) else list(raw.items())
        for q, a in pairs:
            if q in key:
                ans[key[q]] = a
    per, miss = defaultdict(lambda: [0, 0, []]), 0
    pick = json.loads((base / "noise_gate_orch" / "SEEDED_PICK.json").read_text())
    for tid, ids in pick.items():
        for rid in ids:
            r = rows[rid]
            it = g5h.read_item(r)
            got = g5h.normalize_answer(it, ans.get(rid))
            per[tid][0] += 1
            if rid not in ans:
                miss += 1
            if got is None or got != r["gold"]:
                per[tid][1] += 1
                per[tid][2].append(rid)
    review = {t: v[2] for t, v in per.items() if v[1] >= 2}
    out = {"source": src, "tasks": len(per), "rows_read": sum(v[0] for v in per.values()), "unanswered": miss,
           "tasks_to_review": review, "n_review": len(review), "per_task_disagree": {t: v[1] for t, v in sorted(per.items())}}
    (base / "noise_gate_orch" / "SCORE.json").write_text(json.dumps(out, indent=1))
    print(json.dumps({k: out[k] for k in ("tasks", "rows_read", "unanswered", "n_review")}))


main(sys.argv[1])
