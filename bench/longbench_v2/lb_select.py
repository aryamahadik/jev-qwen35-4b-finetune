"""longjev's chunk-scoring + keep-8K procedure with an OpenDecide model as the scorer (functions + a CPU plan mode).

Named lb_select.py, not select.py: a select.py next to these scripts would shadow Python's stdlib `select` module
(subprocess / selectors / asyncio import it), and every script in this folder would break.

Steps (longjev eval/run.py run_item -> judge_at("jev", 8000); see lb_lib.py for the verbatim pieces):
  1. chunk the context: 800 est. tokens (2,400 chars), coarsest separator first, greedy packing, no overlap
  2. score every chunk with ONE yes/no read: "This passage contains information that helps answer the following
     question: <question> Options: A: ..; B: ..; C: ..; D: .."; score = P(yes) (float32, as longjev's arrays)
     (longjev's chunk request also asked the task question and a sufficiency yes/no in the same call; they feed only
     the per-piece vote and the widening diagnostics, not the jev@8000 answer, so they are not read here)
  3. chunk sizes := the scorer's own token counts (longjev: Jev's reported usage per chunk)
  4. budget = max(1000, min(8000, int(32000*0.9) - longest final question estimate))
  5. take chunks best-first (stable order on ties), each costing tokens + 15, until the next one does not fit
  6. put them back in document order, gaps as "\\n[… about N tokens omitted …]\\n"
  7. if the final prompt is too long for the reader, keep the first 85% of the kept chunks in selection order and
     retry, at most 3 times (longjev's judge() on a "too long" error)

  # CPU plan: chunk counts, exact prompt token counts with the adapter's layout, budget checks, compute estimate
  opendecide-data/.venv/bin/python bench/longbench_v2/lb_select.py --plan \\
      --items bench/external_quarantine/longbench_v2/kit/lb_items.jsonl \\
      --model backups/modal_models/q35_4b_main500k --base Qwen/Qwen3.5-4B
"""
from __future__ import annotations

import argparse
import json
import os
import statistics
import sys
import time
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import lb_lib as lb  # noqa: E402

TOO_LONG_RETRIES = 3     # api.LongJev.judge: range(4) attempts
TOO_LONG_KEEP = 0.85     # kept = kept[: max(1, int(len(kept) * 0.85))]
# L4 (od-l4) prefill cost per prompt token, batch 1, eager, from our own v154 JevBench runs (results.jsonl latency vs
# usage.input_tokens, least squares over 231 rows each): 4B C1 0.258 ms/token (+28 ms), 2B arm I 0.082 ms/token (+96 ms)
L4_MS_PER_TOKEN = {"4b": 0.258, "2b": 0.082}


def prepare(item, tok):
    """Chunks (sizes = our token counts) and the relevance rows, one per chunk."""
    chunks = lb.chunk_state(item["context"])
    ids = tok([c.text for c in chunks], add_special_tokens=False)["input_ids"]
    chunks_r = lb.recalibrate(chunks, [len(x) for x in ids])
    rows = [lb.rel_row(item, c) for c in chunks]
    return chunks_r, rows


def keep(item, chunks_r, rel_scores, budget=lb.BUDGET):
    """Selection order of the kept chunks for one item (best first), and the budget used."""
    b = lb.effective_budget(item, budget)
    rel = {"q": np.asarray(rel_scores, dtype=np.float32)}
    return lb.select_round_robin(chunks_r, rel, b), b


def assemble(item, chunks_r, kept, prompt_tokens=None, max_tokens=None):
    """The final row over the kept chunks; with prompt_tokens/max_tokens, longjev's too-long retry. Returns
    (row or None, kept actually used, number of drops)."""
    kept = list(kept)
    for attempt in range(TOO_LONG_RETRIES + 1):
        row = lb.final_row(item, lb.render_state(chunks_r, kept))
        if prompt_tokens is None or prompt_tokens(row) <= max_tokens:
            return row, kept, attempt
        if attempt == TOO_LONG_RETRIES or len(kept) < 2:
            return None, kept, attempt
        kept = kept[: max(1, int(len(kept) * TOO_LONG_KEEP))]
    return None, kept, TOO_LONG_RETRIES


def set_prompt_layout(dio, adapter, base, revision=None):
    """decoder_io LAYOUT/STYLE from the adapter's training cfg, without loading weights (as run_v154 --dry-run)."""
    info = dio.resolve_prompt([str(adapter)], base, None, None, revision)
    dio.LAYOUT = info["layout"] or dio.LAYOUT
    dio.STYLE = info["style"] or dio.STYLE
    return info


def default_lean():
    env = os.environ.get("LB_LEAN")
    if env:
        return env
    home = Path.home() / "lean"
    return str(home if (home / "decoder_io.py").exists() else lb.REPO / "opendecide-data/lean")


def plan(items_path, model_dir, base, lean, sets=("all_proxy", "all_own"), limit=0):
    sys.path.insert(0, str(lean))
    import decoder_io as dio
    from transformers import AutoTokenizer
    set_prompt_layout(dio, model_dir, base)
    tok = AutoTokenizer.from_pretrained(str(model_dir))
    ro = dio.Readout(tok)
    items = [it for it in lb.read_jsonl(items_path) if any(lb.in_set(it, s) for s in sets)]
    if limit:
        items = items[:limit]
    ntok = lambda row: len(tok(ro.prompt(row), add_special_tokens=False)["input_ids"])  # noqa: E731
    t0 = time.time()
    per = []
    for it in items:
        chunks_r, rows = prepare(it, tok)
        rel_tok = [ntok(r) for r in rows]
        b = lb.effective_budget(it, lb.BUDGET)
        # final prompt size if the whole budget is used: state <= budget tokens, plus the prompt around it
        empty = ntok(lb.final_row(it, ""))
        readable = [n for n in rel_tok if n <= dio.MAX_LEN]  # longer rows are never read (the chunk scores 0)
        per.append({"n_chunks": len(rows), "rel_tokens": sum(readable), "rel_max": max(rel_tok),
                    "rel_over": len(rel_tok) - len(readable), "budget": b, "final_overhead": empty,
                    "final_est": b + empty if b + empty <= dio.MAX_LEN else 0,
                    "final_over": b + empty > dio.MAX_LEN, "test_proxy": lb.in_set(it, "test_proxy")})
    n = len(per)
    tot_rel = sum(p["rel_tokens"] for p in per)
    tot_final = sum(p["final_est"] for p in per)
    out = {"items": n, "chunks": sum(p["n_chunks"] for p in per),
           "chunks_median": statistics.median(p["n_chunks"] for p in per) if per else None,
           "chunks_max": max((p["n_chunks"] for p in per), default=None),
           "rel_prompt_tokens_total": tot_rel,
           "rel_prompt_tokens_mean": round(tot_rel / max(1, sum(p["n_chunks"] - p["rel_over"] for p in per)), 1),
           "rel_prompt_tokens_max": max((p["rel_max"] for p in per), default=None),
           "rel_rows_over_max_len": sum(p["rel_over"] for p in per),
           "items_with_rel_rows_over_max_len": sum(p["rel_over"] > 0 for p in per),
           "items_budget_below_8000": sum(p["budget"] < lb.BUDGET for p in per),
           "final_overhead_tokens_median": statistics.median(p["final_overhead"] for p in per) if per else None,
           "final_overhead_tokens_max": max((p["final_overhead"] for p in per), default=None),
           "final_prompt_tokens_est_total_1view": tot_final,
           "items_final_est_over_max_len": sum(p["final_over"] for p in per),
           "test_proxy_items": sum(p["test_proxy"] for p in per), "layout": dio.LAYOUT, "style": dio.STYLE,
           "max_len": dio.MAX_LEN, "plan_s": round(time.time() - t0, 1)}
    est = {}
    for k, ms in L4_MS_PER_TOKEN.items():
        sc = tot_rel * ms / 1000 / 3600
        fin = 2 * tot_final * ms / 1000 / 3600  # A5 2-view for choice rows
        est[k] = {"scoring_h": round(sc, 2), "final_2view_h": round(fin, 2), "total_h": round(sc + fin, 2),
                  "basis": f"{ms} ms per prompt token (L4, batch 1, eager; batching may be faster, long prompts slower)"}
    out["l4_estimate"] = est
    return out


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--plan", action="store_true", required=True)
    ap.add_argument("--items", required=True)
    ap.add_argument("--model", required=True, help="adapter dir (tokenizer + train_meta.json for the layout)")
    ap.add_argument("--base", required=True)
    ap.add_argument("--lean", default=default_lean())
    ap.add_argument("--sets", default="all_proxy,all_own")
    ap.add_argument("--limit", type=int, default=0)
    a = ap.parse_args(argv)
    res = plan(a.items, a.model, a.base, a.lean, tuple(a.sets.split(",")), a.limit)
    print(json.dumps({"plan": res}, indent=1))
    return res


if __name__ == "__main__":
    main()
