"""Inputs for the B1 H100 benchmark (modal_think.py). Local, CPU, no model, no new items.

  python think/build_bench_inputs.py            # writes think/data/{squad2_parity100,fast_rows_dev200}.jsonl + manifest

squad2_parity100: 100 SQuAD2 items that the free L4 already answered in A17-B0 (bench/think_check/think_preds.jsonl,
  768-token budget, the answers think_run.py reuses for routed squad2 items). Picked by sha256("b1-parity:" + id), the
  first 100 in that order. Each line: our row (od_engine.build_row of think_eval.to_di, exactly as think_eval.py), the
  rendered user message (decoder_io.user_msg, cygnet + schema_branch_mark) and its sha256, the info/letters needed to map
  a letter back, and the L4 result (ok / parsed / think_tokens / capped). Gold stays in a separate file that never goes
  to Modal (scoring is local).
fast_rows_dev200: 200 rows of data/dev.jsonl (a gate_dev.SPLITS dev split), fields needed for a readout only (no gold):
  timing of the C1 fast path. No labels are used on Modal.
od_engine imports the Decision Index harness only for Engine/Unsupported/text; this script stubs those three names (text
= the string as is, JSON compact otherwise, as od_engine's docstring states). The harness itself is never opened.
"""
from __future__ import annotations

import hashlib
import json
import re
import sys
import types
from pathlib import Path

THINK = Path(__file__).resolve().parent
LEAN = THINK.parent
JEV = LEAN.parent.parent
OUT = THINK / "data"
PREDS = JEV / "bench/think_check/think_preds.jsonl"
SQUAD = JEV / "bench/nimble_suite/data/squad2/all.jsonl"
DEV = LEAN / "data/dev.jsonl"
N_PARITY, N_FAST = 100, 200


def _stub_harness():
    """Minimal stand-ins for decision_index.engines.base (Engine, Unsupported, text); nothing is read from the harness."""
    class Unsupported(Exception):
        pass

    def text(x):
        return x if isinstance(x, str) else json.dumps(x, ensure_ascii=False, separators=(",", ":"))

    base = types.ModuleType("decision_index.engines.base")
    base.Engine, base.Unsupported, base.text = object, Unsupported, text
    for name in ("decision_index", "decision_index.engines"):
        sys.modules.setdefault(name, types.ModuleType(name))
    sys.modules["decision_index.engines.base"] = base


def to_di(q):  # copied from bench/think_check/think_eval.py (A17-B0)
    t, c, ins = q["type"], q["criteria"], q.get("instructions") or ""
    if t == "noul":
        return {"type": "choice", "instructions": ins, "criteria": {"true": c["true"], "false": c["false"]}}
    return {"type": "choice", "instructions": ins, "criteria": dict(c)}


def sha(s: str) -> str:
    return hashlib.sha256(s.encode("utf-8")).hexdigest()


def sha_file(p: Path) -> str:
    return hashlib.sha256(p.read_bytes()).hexdigest()


def read(p: Path):
    with open(p, encoding="utf-8") as f:
        return [json.loads(x) for x in f if x.strip()]


def write(p: Path, rows) -> str:
    p.parent.mkdir(parents=True, exist_ok=True)
    with open(p, "w", encoding="utf-8") as f:
        for r in rows:
            f.write(json.dumps(r, ensure_ascii=False) + "\n")
    return sha_file(p)


def main():
    _stub_harness()
    sys.path[:0] = [str(LEAN), str(JEV / "bench/decision_index")]
    import decoder_io as dio
    from od_engine import build_row, state_text
    dio.LAYOUT, dio.STYLE = "schema_branch_mark", "cygnet"  # as think_eval.py / think_run.py
    l4 = {r["id"]: r for r in read(PREDS) if r["sub"] == "squad2"}
    pick = sorted(l4, key=lambda i: sha(f"b1-parity:{i}"))[:N_PARITY]
    want, recs = set(pick), {}
    with open(SQUAD, encoding="utf-8") as f:
        for line in f:
            r = json.loads(line)
            if r["id"] in want:
                recs[r["id"]] = r
    assert len(recs) == N_PARITY, (len(recs), N_PARITY)
    items, local = [], []
    for i in pick:
        r = recs[i]
        q = r["input"]["questions"]["decision"]
        row, info = build_row(state_text(r["input"]["state"]), to_di(q), "q0")
        user = dio.user_msg(row)
        letters = dict(re.findall(r"^([A-Z])\. (.+)$", user, flags=re.M))
        items.append({"id": i, "row": row, "info": info, "letters": letters, "user": user, "user_sha256": sha(user)})
        local.append({"id": i, "kind": q["type"], "gold": r["reference"]["target"], "yes_key": info["keys"][0],
                      "l4": {k: l4[i].get(k) for k in ("ok", "parsed", "think_tokens", "capped", "sec_per_item")},
                      "l4_budget": 768, "l4_source": "bench/think_check/think_preds.jsonl (A17-B0, think_eval.py)"})
    dev = read(DEV)
    dev = sorted(dev, key=lambda r: sha(f"b1-fast:{r['id']}"))[:N_FAST]
    keep = ("id", "call_id", "state", "instructions", "qtype", "options", "card")
    fast = [{k: r[k] for k in keep if k in r} for r in dev]
    man = {"built_by": "think/build_bench_inputs.py", "pick_rule": "sha256('b1-parity:'+id) ascending, first 100 squad2 "
           "ids of think_preds.jsonl; dev rows: sha256('b1-fast:'+id) ascending, first 200",
           "layout": dio.LAYOUT, "style": dio.STYLE,
           "sources": {str(p.relative_to(JEV)): sha_file(p) for p in (PREDS, SQUAD, DEV, LEAN / "decoder_io.py",
                                                                      JEV / "bench/decision_index/od_engine.py")},
           "outputs": {"squad2_parity100.jsonl": write(OUT / "squad2_parity100.jsonl", items),
                       "squad2_parity100_local.jsonl": write(OUT / "squad2_parity100_local.jsonl", local),
                       "fast_rows_dev200.jsonl": write(OUT / "fast_rows_dev200.jsonl", fast)},
           "n": {"parity": len(items), "fast": len(fast), "noul": sum(x["row"]["qtype"] == "noul" for x in items)},
           "l4_acc_on_pick": sum(bool(x["l4"]["ok"]) for x in local) / len(local)}
    (OUT / "inputs_manifest.json").write_text(json.dumps(man, indent=1) + "\n")
    print(json.dumps({k: man[k] for k in ("n", "l4_acc_on_pick", "outputs")}, indent=1))


if __name__ == "__main__":
    main()
