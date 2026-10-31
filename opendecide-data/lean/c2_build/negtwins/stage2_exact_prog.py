"""negtwins stage 2, step 1: score the 24 exact_prog answer files (A42-D 7.3: exactness >= 0.9 per pattern).
Run from c2_build: ../../.venv/bin/python -B -m negtwins.stage2_exact_prog
Writes negtwins/stage2/EXACT_PROG_SCORES.json (per-pattern) and negtwins/stage2/PROG_CATALOGUE.json (survivors)."""
import json
from collections import Counter
from pathlib import Path

from negtwins import core as C, tasks as T

ROOT = T.HERE / "haiku" / "exact_prog"
OUT = T.HERE / "stage2"


def load_raw(root: Path) -> dict:
    return {p.stem: json.loads(p.read_text(encoding="utf-8")) for p in sorted((root / "answers").glob("*.json"))}


def main() -> int:
    OUT.mkdir(exist_ok=True)
    cat = C.build_catalogue(a48h=False)          # the 116 patterns the batch was written for (before Ruling A48 h)
    items, short = T.exact_items(cat, {})
    batch = T._batch("polarity", items, "negtw-exact-prog", T.EXACT_PROMPT)
    man = json.loads((ROOT / "TASKS.json").read_text())
    assert batch.batch_id == man["batch_id"], (batch.batch_id, man["batch_id"])
    raw = load_raw(ROOT)
    ans, probs = T.chunker.load_answers(batch, raw)
    rel = T.relations(ans)
    res = T.exactness_decide(cat, rel)
    by = {p.pid: p for p in cat}
    rows = []
    for pid, r in res.items():
        p = by[pid]
        reads = [rel.get(f"exact|{pid}|{i}") for i in range(T.EXACT_PER_PATTERN)]
        rows.append({"pid": pid, "op": p.op, "cls": p.cls, "contr": p.contr, "frame": p.frame, "verb": p.verb,
                     "relation": p.relation, "good": r["good"], "n": r["n"], "rate": r["rate"], "pass": r["pass"],
                     "reads": dict(Counter(reads))})
    dropped = [r for r in rows if not r["pass"]]
    kept = [r for r in rows if r["pass"]]
    rep = {"batch_id": batch.batch_id, "n_patterns": len(cat), "n_items": len(items), "problems": probs,
           "short_patterns": short, "n_pass": len(kept), "n_drop": len(dropped),
           "mean_rate": sum(r["rate"] for r in rows) / len(rows),
           "drop_by_op": dict(Counter((r["op"], r["cls"], r["contr"]) .__repr__() for r in dropped)),
           "rows": rows}
    (OUT / "EXACT_PROG_SCORES.json").write_text(json.dumps(rep, indent=1, ensure_ascii=False) + "\n", encoding="utf-8")
    cut = {p.pid: C.a48h_class(p) for p in cat if C.a48h_class(p)}          # Ruling A48 (h): dropped whatever the score
    final = sorted(r["pid"] for r in kept if r["pid"] not in cut)
    rep["a48h_cut"] = {"by_class": dict(Counter(cut.values())), "n_cut": len(cut), "n_final": len(final),
                       "cut_at_0.9": sum(1 for r in rows if r["pid"] in cut and r["rate"] == 0.9),
                       "kept_at_0.9": sum(1 for r in rows if r["pid"] not in cut and r["rate"] == 0.9)}
    (OUT / "EXACT_PROG_SCORES.json").write_text(json.dumps(rep, indent=1, ensure_ascii=False) + "\n", encoding="utf-8")
    (OUT / "PROG_CATALOGUE.json").write_text(json.dumps(final, indent=1) + "\n", encoding="utf-8")
    print(json.dumps(rep["a48h_cut"]))
    print(json.dumps({k: rep[k] for k in ("batch_id", "n_patterns", "n_items", "problems", "short_patterns", "n_pass", "n_drop", "mean_rate")}, indent=1))
    for r in sorted(rows, key=lambda r: (r["rate"], r["pid"])):
        if r["rate"] < 1.0:
            print(f'{r["rate"]:.1f} {r["op"]:9s} {r["cls"]:5s} {r["contr"] or "-":4s} verb={r["verb"] or "-":8s} frame={r["frame"][:28]!r:32s} {r["reads"]}')
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
