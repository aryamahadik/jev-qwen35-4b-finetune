#!/usr/bin/env python3
"""Write wave2/ROUTE.md from route/route_stats.json (produced by route/route_haiku.py). Numbers only come from that file."""
from __future__ import annotations

import sys
from pathlib import Path

WAVE2 = Path("/Users/aryamahadik/Documents/jev/opendecide-data/lean/c2_build/gblock/wave2")
if str(WAVE2) not in sys.path:
    sys.path.insert(0, str(WAVE2))
from builders import common as C  # noqa: E402

TASKS = {"W1": "injection", "W2": "pii", "W3": "rag_faithfulness", "W4": "off_topic", "W5": "search_relevance",
         "W6": "commit_type", "W7": "tool_routing"}


def pct(x) -> str:
    return "n/a" if x is None else f"{100 * x:.1f}%"


def main() -> None:
    st = C.read_json(WAVE2 / "route" / "route_stats.json")
    man = C.read_json(WAVE2 / "verify" / "manifest.json")
    om = C.read_json(WAVE2 / "opus_queue" / "manifest.json")
    pt, tot = st["per_type"], st["total"]
    L = []
    L.append("# G-block wave 2: Haiku keep/queue route")
    L.append("")
    L.append("PREREG_FINAL Ruling A40 (c), steps 1 and 3 sampling. Generated from `route/route_stats.json`; gold never edited.")
    L.append("Opus reads have NOT been run. They wait for the Mon 19 Oct reset (A39 g, A41 a).")
    L.append("")
    L.append("## Rules applied")
    L.append("")
    L.append("- **Keep** (A40 c.1): Haiku's answer equals the program gold AND Haiku confidence >= 0.80.")
    L.append("- **Queue** for the blind Opus read (A40 c.2), one reason per item, first match wins:")
    L.append("  - `missing`: no usable Haiku verdict (qid not answered, or chunk has no Haiku output).")
    L.append("  - `invalid`: answer not an allowed label, confidence not a number in [0, 1], or a duplicate qid.")
    L.append("  - `disagree`: valid answer != gold (any confidence).")
    L.append("  - `low_confidence`: valid answer == gold, confidence < 0.80.")
    L.append("- **Audit** (A40 c.3): per type, round(5% x kept) of kept items, chosen by seeded hash (seed 20261013),"
             " sent to Opus as role `audit`. The per-domain 6% re-read rule is applied after the Opus audit reads.")
    L.append("- **chunk_129**: the orchestrator marks its audit as failed and it has no Haiku output. Its Haiku answers"
             " are not used, so its 50 items are treated as `missing` and queued. They are not dropped and not kept.")
    L.append("- **Agreement rate** = valid Haiku answers equal to gold / valid Haiku answers. The second rate restricts"
             " to confidence >= 0.80.")
    L.append("")
    L.append("## Counts per type")
    L.append("")
    L.append("| Type | Task | Candidates | Valid answers | Agreement | Agreement (conf >= 0.80) | Kept | Keep rate |"
             " Queued: missing | invalid | disagree | low_conf | Queued total | Audit (of kept) | Opus items |")
    L.append("|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|")
    for T in ("W1", "W2", "W3", "W4", "W5", "W6", "W7"):
        r = pt[T]
        q = r["queued_by_reason"]
        L.append(f"| {T} | {TASKS[T]} | {r['candidates']} | {r['valid_haiku_answers']} | {pct(r['agreement_rate'])} |"
                 f" {pct(r['agreement_rate_conf_ge_0.80'])} | {r['kept']} | {pct(r['keep_rate'])} |"
                 f" {q['missing']} | {q['invalid']} | {q['disagree']} | {q['low_confidence']} |"
                 f" {r['queued_total']} | {r['audit_of_kept']} | {r['opus_items']} |")
    q = tot["queued_by_reason"]
    L.append(f"| **all** | | **{tot['candidates']}** | **{tot['valid_haiku_answers']}** | **{pct(tot['agreement_rate'])}** |"
             f" **{pct(tot['agreement_rate_conf_ge_0.80'])}** | **{tot['kept']}** | **{pct(tot['keep_rate'])}** |"
             f" **{q['missing']}** | **{q['invalid']}** | **{q['disagree']}** | **{q['low_confidence']}** |"
             f" **{tot['queued_total']}** | **{tot['audit_of_kept']}** | **{tot['opus_items']}** |")
    L.append("")
    L.append("Counts of raw Haiku answers equal to gold (valid answers only):")
    L.append("")
    for T in ("W1", "W2", "W3", "W4", "W5", "W6", "W7"):
        L.append(f"- {T}: {pt[T]['agree_with_gold']} of {pt[T]['valid_haiku_answers']}")
    L.append(f"- all: {tot['agree_with_gold']} of {tot['valid_haiku_answers']}")
    L.append("")
    L.append("## Integrity")
    L.append("")
    L.append(f"- Candidates: {tot['candidates']}; verify chunks: {man['n_chunks']}; chunk sizes 50 (last 32)."
             " `candidates.jsonl` and `key.json` match the verify manifest hashes.")
    L.append(f"- Kept {tot['kept']} + queued {tot['queued_total']} = {tot['candidates']} (asserted in the script).")
    L.append(f"- Haiku entries: malformed {sum(st['malformed_entries'].values())}, foreign or misplaced qids"
             f" {st['foreign_or_misplaced_entries']} (ignored; the real item is counted as `missing`)."
             f" Haiku chunk status not ok: {st['haiku_chunk_status']}.")
    L.append(f"- Opus queue: {om['n_items']} items = {om['n_queued']} queued + {om['n_audit']} audit, in"
             f" {om['n_chunks']} gold-free TEACH-0 chunks (last chunk {om['chunk_sizes'][-1]} items).")
    L.append("- Audit by type (kept, 5% stratified): "
             + ", ".join(f"{T} {st['audit_n_per_type'][T]}" for T in ("W1", "W2", "W3", "W4", "W5", "W6", "W7")) + ".")
    L.append("")
    L.append("## Files")
    L.append("")
    L.append("- `kept_haiku.jsonl`: the kept candidate rows, unchanged from `candidates/candidates.jsonl`.")
    L.append("- `kept_haiku_provenance.jsonl`: per kept row, the Haiku answer and confidence, the gold label, and"
             " whether it is in the Opus audit.")
    L.append("- `opus_queue/chunk_NNN.json`: gold-free TEACH-0 chunks (qid, kind, text, question, options, definitions)."
             " `opus_queue/key.json` maps each new qid to its row id, type and gold (scoring only). `opus_queue/roles.json`"
             " gives role (queued / audit), reason and the Haiku verdict. `opus_queue/manifest.json` holds the hashes.")
    L.append("- `route/decisions.jsonl`: one decision per candidate. `route/route_stats.json`: the counts above.")
    L.append("")
    C.kp.write_text(WAVE2 / "ROUTE.md", "\n".join(L) + "\n")
    print("wrote", WAVE2 / "ROUTE.md")


if __name__ == "__main__":
    main()
