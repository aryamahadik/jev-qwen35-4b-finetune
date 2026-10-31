"""Exploratory-only OHS-3 evaluation of the Round-1 adapter with adaptive thinking.

This is deliberately separate from the pre-registered OHS-3 pass.  It must never
be presented as the one-shot score.  The policy is fixed before reading any OHS-3
gold labels:

* run the Round-1 adapter's normal A5 2-view readout on every row;
* send the lowest-confidence 20 percent of rows to a 1,024-token Qwen thinking
  pass, one request at a time on an L4;
* replace a routed fast answer only when the thinking answer parses; otherwise
  keep the fast probabilities.

The script never reads or prints gold labels.  Scoring happens separately on the
Mac after predictions are complete.  All partial artifacts are resumable.

Run only with an explicit owner GO, on the L4:
  ~/od/bin/python prep89/ohs3_r1_think_exploratory.py --go
"""
from __future__ import annotations

import argparse
import hashlib
import json
import math
import re
import statistics
import time
from pathlib import Path

import torch

HERE = Path(__file__).resolve().parent
LEAN = HERE.parent
import sys

if str(LEAN) not in sys.path:
    sys.path.insert(0, str(LEAN))
import decoder_io as dio  # noqa: E402
import ohs3_lib as L  # noqa: E402


NAME = "q35_4b_c_r1_think_exploratory"
ADAPTER_NAME = "q35_4b_c_r1"
ADAPTER_SHA256 = "144e1a8489013d96c4f93baa98fb2d32cd4ea0b48b8cfedd3222ebe3262ced5f"
BASE = "Qwen/Qwen3.5-4B"
REVISION = "851bf6e806efd8d0a36b00ddf55e13ccb7b8cd0a"
LAYOUT, STYLE = "schema_branch_mark", "cygnet"
ROUTE_SHARE = 0.20
THINK_BUDGET = 1024
PSEUDO_CONFIDENCE = 0.90
LATENCY_SAMPLE = 160


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for b in iter(lambda: f.read(1 << 20), b""):
            h.update(b)
    return h.hexdigest()


def write_json(path: Path, obj) -> None:
    tmp = path.with_suffix(path.suffix + ".tmp")
    tmp.write_text(json.dumps(obj, indent=2, sort_keys=True) + "\n")
    tmp.replace(path)


def read_jsonl(path: Path) -> list[dict]:
    if not path.exists():
        return []
    with open(path) as f:
        return [json.loads(line) for line in f if line.strip()]


def append_jsonl(path: Path, records: list[dict]) -> None:
    if not records:
        return
    with open(path, "a") as f:
        for r in records:
            f.write(json.dumps(r, separators=(",", ":")) + "\n")
        f.flush()


def percentile(values: list[float], p: float) -> float | None:
    if not values:
        return None
    return round(float(__import__("numpy").percentile(values, p)), 4)


def mixture_percentile(fast: list[float], think: list[float], routed_share: float, p: float) -> float | None:
    """Quantile of the adaptive system, not of an unweighted test-artifact mix."""
    if not fast or not think:
        return None
    weighted = [(v, (1.0 - routed_share) / len(fast)) for v in fast]
    weighted += [(v, routed_share / len(think)) for v in think]
    total, target = 0.0, p / 100.0
    for value, weight in sorted(weighted):
        total += weight
        if total >= target:
            return round(value, 4)
    return round(max(v for v, _ in weighted), 4)


def row_confidence(row: dict, probs: dict) -> float:
    if row["qtype"] == "noul":
        p = float(probs.get("yes", 0.5))
        return max(p, 1.0 - p)
    vals = [float(probs.get(o, 0.0)) for o in row["options"]]
    total = sum(vals)
    return max(vals) / total if total > 0 else 0.0


def select_routed(rows: list[dict], fast: dict[str, dict]) -> set[str]:
    n = max(1, math.ceil(len(rows) * ROUTE_SHARE))
    ordered = sorted(
        rows,
        key=lambda r: (row_confidence(r, fast[r["id"]]), hashlib.sha256(r["id"].encode()).hexdigest()),
    )
    return {r["id"] for r in ordered[:n]}


def think_prompt(tok, row: dict) -> tuple[str, list[tuple[str, str]]]:
    user = dio.user_msg(row)
    labels = [(dio.label(i), option) for i, option in enumerate((dio.as_letter_row(row))["options"])]
    prompt = tok.apply_chat_template(
        [{"role": "system", "content": dio.SYSTEM}, {"role": "user", "content": user}],
        tokenize=False,
        add_generation_prompt=True,
        enable_thinking=True,
    )
    return prompt, labels


def parse_letter(text: str, labels: list[tuple[str, str]]) -> str | None:
    # Prefer the final answer line, but accept any exact option label as the old
    # thinking harness does.  Long labels must be tested before their prefixes.
    for label, option in sorted(labels, key=lambda x: -len(x[0])):
        if re.search(rf"(?<![A-Z]){re.escape(label)}(?![A-Z])", text):
            return option
    return None


def think_one(model, tok, row: dict) -> dict:
    prompt, labels = think_prompt(tok, row)
    pad = tok.pad_token_id if tok.pad_token_id is not None else tok.eos_token_id
    enc = tok(prompt, return_tensors="pt").to("cuda")
    t0 = time.perf_counter()
    with torch.no_grad():
        generated = model.generate(
            **enc,
            max_new_tokens=THINK_BUDGET,
            do_sample=True,
            temperature=0.6,
            top_p=0.95,
            top_k=20,
            pad_token_id=pad,
        )
    thought = tok.decode(generated[0, enc["input_ids"].shape[1]:], skip_special_tokens=False)
    thought = thought.split("<|im_end|>")[0].replace(tok.pad_token or "\x00", "")
    capped = "</think>" not in thought
    closed = thought.split("</think>")[0] + "</think>\n\n" if not capped else thought + "\n</think>\n\n"
    enc2 = tok(prompt + closed, return_tensors="pt").to("cuda")
    with torch.no_grad():
        answer = model.generate(**enc2, max_new_tokens=8, do_sample=False, pad_token_id=pad)
    answer_text = tok.decode(answer[0, enc2["input_ids"].shape[1]:], skip_special_tokens=True)
    return {
        "pred_key": parse_letter(answer_text, labels),
        "think_tokens": len(tok(thought, add_special_tokens=False)["input_ids"]),
        "capped": capped,
        "wall_s": round(time.perf_counter() - t0, 4),
    }


def load_model(models_dir: Path):
    adapter = models_dir / ADAPTER_NAME
    weights = adapter / "adapter_model.safetensors"
    if not weights.exists() or sha256_file(weights) != ADAPTER_SHA256:
        raise SystemExit(f"adapter missing or sha mismatch: {weights}")
    dio.LAYOUT, dio.STYLE = LAYOUT, STYLE
    model, tok, info = dio.load(BASE, "cuda", adapter=str(adapter), revision=REVISION,
                                layout=LAYOUT, style=STYLE, force=False, return_info=True)
    if (dio.LAYOUT, dio.STYLE) != (LAYOUT, STYLE):
        raise SystemExit("adapter prompt layout/style differs from the experimental protocol")
    model = model.merge_and_unload().eval()
    return model, tok, {"adapter_sha256": ADAPTER_SHA256, "load": info,
                        "gpu": torch.cuda.get_device_name(0)}


def base_reads(model, tok, rows: list[dict], fast_path: Path) -> dict[str, dict]:
    existing = {r["id"]: r["probs"] for r in read_jsonl(fast_path)}
    ro = dio.Readout(tok)

    def read_safely(todo: list[dict]) -> list[dict]:
        """Keep the exploratory run alive on a 24 GB L4 for unusually long prompts."""
        try:
            _, probs = L.a5_read(dio, model, ro, todo, "cuda", "2view", batch_size=4, token_budget=6000)
            return probs
        except torch.OutOfMemoryError:
            torch.cuda.empty_cache()
            if len(todo) == 1:
                raise
            mid = len(todo) // 2
            print(json.dumps({"phase": "fast", "oom_recovery": True, "split": [len(todo[:mid]), len(todo[mid:])]}),
                  flush=True)
            return read_safely(todo[:mid]) + read_safely(todo[mid:])

    for batch in L.predict_batches(rows):
        todo = [rows[i] for i in batch if rows[i]["id"] not in existing]
        if not todo:
            continue
        probs = read_safely(todo)
        recs = [{"id": r["id"], "probs": p} for r, p in zip(todo, probs)]
        append_jsonl(fast_path, recs)
        existing.update({r["id"]: r["probs"] for r in recs})
        torch.cuda.empty_cache()
        print(json.dumps({"phase": "fast", "done": len(existing), "total": len(rows)}), flush=True)
    if len(existing) != len(rows):
        raise SystemExit("fast reads incomplete")
    return existing


def fast_latency(model, tok, rows: list[dict], latency_path: Path) -> list[dict]:
    want = {r["id"] for r in sorted(rows, key=lambda x: hashlib.sha256(x["id"].encode()).hexdigest())[:LATENCY_SAMPLE]}
    existing = {r["id"]: r for r in read_jsonl(latency_path)}
    ro = dio.Readout(tok)
    for row in rows:
        if row["id"] not in want or row["id"] in existing:
            continue
        t0 = time.perf_counter()
        L.a5_read(dio, model, ro, [row], "cuda", "2view", batch_size=1, token_budget=12000)
        rec = {"id": row["id"], "wall_s": round(time.perf_counter() - t0, 4)}
        append_jsonl(latency_path, [rec])
        existing[row["id"]] = rec
        print(json.dumps({"phase": "fast_latency", "done": len(existing), "total": len(want)}), flush=True)
    return list(existing.values())


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--go", action="store_true", help="required owner authorization for a real OHS-3 exploratory read")
    ap.add_argument("--root", default=str(LEAN))
    ap.add_argument("--models-dir", default=str(LEAN / "models"))
    ap.add_argument("--run-dir", default=str(LEAN / "logs" / "ohs3" / "r1_think_exploratory"))
    args = ap.parse_args()
    if not args.go:
        raise SystemExit("REAL OHS-3 exploratory run requires explicit --go")
    if not torch.cuda.is_available():
        raise SystemExit("this run requires the L4 CUDA host")

    root, run_dir = Path(args.root).resolve(), Path(args.run_dir).resolve()
    run_dir.mkdir(parents=True, exist_ok=True)
    rows = L.read_jsonl(root / "data" / "ohs3.jsonl")
    for row in rows:  # gold never enters inference or output artifacts
        row.pop("gold", None)
    if len(rows) != L.OHS3_CALLS:
        raise SystemExit(f"unexpected OHS-3 row count {len(rows)}")
    model, tok, model_info = load_model(Path(args.models_dir))
    torch.manual_seed(0)
    fast = base_reads(model, tok, rows, run_dir / "fast.jsonl")
    routed = select_routed(rows, fast)
    write_json(run_dir / "policy.json", {
        "experimental_only": True, "name": NAME, "route_share_target": ROUTE_SHARE,
        "routed_rows": len(routed), "route_rule": "lowest A5 2-view confidence; deterministic ID tie break",
        "think_budget": THINK_BUDGET, "sampling": {"temperature": 0.6, "top_p": 0.95, "top_k": 20, "seed": 0},
        "fallback": "fast probabilities when the generated answer is unparsed", "pseudo_confidence": PSEUDO_CONFIDENCE,
        "model": model_info,
    })
    nonrouted_rows = [r for r in rows if r["id"] not in routed]
    fast_samples = fast_latency(model, tok, nonrouted_rows, run_dir / "fast_latency.jsonl")
    thought_path = run_dir / "thinking.jsonl"
    thoughts = {r["id"]: r for r in read_jsonl(thought_path)}
    for row in rows:
        if row["id"] not in routed or row["id"] in thoughts:
            continue
        rec = {"id": row["id"], **think_one(model, tok, row)}
        append_jsonl(thought_path, [rec])
        thoughts[row["id"]] = rec
        print(json.dumps({"phase": "thinking", "done": len(thoughts), "total": len(routed)}), flush=True)
    if len(thoughts) != len(routed):
        raise SystemExit("thinking pass incomplete")

    pred_dir = root / "preds_ohs3"
    pred_dir.mkdir(parents=True, exist_ok=True)
    out = pred_dir / f"{NAME}.jsonl"
    recs, used = [], 0
    for row in rows:
        probs = dict(fast[row["id"]])
        th = thoughts.get(row["id"])
        if th and th.get("pred_key") in probs:
            key = th["pred_key"]
            rest = (1.0 - PSEUDO_CONFIDENCE) / max(1, len(probs) - 1)
            probs = {k: (PSEUDO_CONFIDENCE if k == key else rest) for k in probs}
            used += 1
        recs.append({"id": row["id"], "model": NAME, "probs": probs})
    L.write_jsonl_atomic(out, recs)
    fast_walls = [float(r["wall_s"]) for r in fast_samples]
    think_walls = [float(r["wall_s"]) for r in thoughts.values()]
    # The system p50 is estimated from deterministic individual-call fast samples
    # and actual routed thinking calls, weighted by their observed routed share.
    routed_share = len(routed) / len(rows)
    summary = {
        "experimental_only": True, "name": NAME, "rows": len(rows), "routed_rows": len(routed),
        "thinking_answers_used": used, "thinking_parse_rate": round(used / len(routed), 4),
        "fast_latency_sample_n": len(fast_walls), "fast_latency_s": {"p50": percentile(fast_walls, 50), "p95": percentile(fast_walls, 95)},
        "routed_thinking_s": {"p50": percentile(think_walls, 50), "p95": percentile(think_walls, 95),
                                "mean": round(statistics.mean(think_walls), 4) if think_walls else None},
        "combined_observed_s": {"p50": mixture_percentile(fast_walls, think_walls, routed_share, 50),
                                "p95": mixture_percentile(fast_walls, think_walls, routed_share, 95),
                                "note": "weighted mixture of sampled fast calls and all routed thinking calls"},
        "think_tokens": {"median": percentile([float(r["think_tokens"]) for r in thoughts.values()], 50),
                          "mean": round(statistics.mean(float(r["think_tokens"]) for r in thoughts.values()), 2),
                          "capped_share": round(sum(bool(r["capped"]) for r in thoughts.values()) / len(thoughts), 4)},
        "model": model_info, "predictions": str(out),
    }
    write_json(run_dir / "summary.json", summary)
    (pred_dir / f"{NAME}.meta.json").write_text(json.dumps(summary, indent=2) + "\n")
    print(json.dumps({"complete": True, "predictions": str(out), **summary["combined_observed_s"]}), flush=True)


if __name__ == "__main__":
    main()
