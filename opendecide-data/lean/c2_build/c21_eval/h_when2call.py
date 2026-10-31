"""When2Call MCQ, Artificial Analysis (AA) protocol harness (Tier 1 item 1). Eval only.

Source: nvidia/When2Call test/when2call_test_mcq.jsonl (3,652 items; CC-BY-4.0), pinned revision in SOURCES.json.
AA protocol (https://artificialanalysis.ai/evaluations/when2call, fetched 18 Oct 2026): 3,423 tasks, one choice among four
candidate replies (direct, tool call, ask for more information, cannot answer), "We leave out 229 'ask for more
information' tasks where it is ambiguous whether more information is required", replies shuffled per task, accuracy.

ROW-COUNT STATUS (read this before quoting a number):
  * The 3,652 / 4-reply / per-task-shuffle / accuracy parts are reproduced exactly.
  * AA does NOT publish WHICH 229 request_for_info tasks it dropped (not on the AA page, not in the When2Call repo).
    Our row count therefore cannot be 3,423 with the same items. Every score file carries protocol_status =
    "NOT SAME-PROTOCOL: AA's 229 dropped items are unpublished". We report instead, all pre-registered:
      full      accuracy on all 3,652 items (primary);
      per class accuracy for request_for_info (1,062), tool_call (1,295), cannot_answer (1,295);
      bounds    the AA-style 3,423 accuracy for ANY choice of 229 dropped request_for_info items lies between a
                lower bound (the 229 dropped are the ones we got right) and an upper bound (the ones we got wrong);
                see aa_bounds; and
      expected  the value if the 229 were a uniform random subset of request_for_info items.
    "Ahead of Jev 1.14 under the AA protocol" may be claimed only if our LOWER bound (and the paired CI of the full set)
    clears Jev 1.14 read by us on the same rows; otherwise the claim line says "full 3,652 items, not AA-identical".
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path

from . import common as C
from .formats import load_format

SET = "when2call"
SRC = C.QUARANTINE / SET / "test" / "when2call_test_mcq.jsonl"
REPLY_KEYS = ["direct", "tool_call", "request_for_info", "cannot_answer"]
AA_N, AA_DROPPED, FULL_N = 3423, 229, 3652
PROTOCOL_STATUS = "NOT SAME-PROTOCOL: AA's 229 dropped request_for_info items are unpublished (full 3,652 reported)"


def render_tools(tools):
    parts = []
    for t in tools:
        d = json.loads(t) if isinstance(t, str) else t
        parts.append(json.dumps(d, ensure_ascii=False, separators=(",", ":")))
    return "\n".join(f"- {p}" for p in parts)


def build_rows(src=SRC):
    fmt, _, _ = load_format()
    raw = C.read_jsonl(src)
    if len(raw) != FULL_N:
        raise ValueError(f"When2Call MCQ has {len(raw)} rows, expected {FULL_N}")
    rows = []
    for r in raw:
        ans = r["answers"]
        if sorted(ans) != sorted(REPLY_KEYS):
            raise ValueError(f"{r['uuid']}: unexpected reply keys {sorted(ans)}")
        options = [ans[k] for k in REPLY_KEYS]
        state = "Available tools:\n" + render_tools(r["tools"]) + "\n\nUser request:\n" + r["question"].strip()
        rows.append(C.make_row(r["uuid"], state, fmt["when2call_instructions"], options, gold=ans[r["correct_answer"]],
                               meta={"correct_answer": r["correct_answer"], "source": r["source"],
                                     "keys": REPLY_KEYS}))
    return rows


def aa_bounds(correct_by_class: dict, n_dropped=AA_DROPPED):
    """Range of the AA-style accuracy over every possible choice of `n_dropped` dropped request_for_info items.
    correct_by_class[c] = (n_correct, n_total). Dropping wrong RFI items raises accuracy (upper bound); dropping
    right ones lowers it (lower bound)."""
    tot_c = sum(c for c, _ in correct_by_class.values())
    tot_n = sum(n for _, n in correct_by_class.values())
    rc, rn = correct_by_class["request_for_info"]
    if n_dropped > rn:
        raise ValueError("cannot drop more request_for_info items than exist")
    n_after = tot_n - n_dropped
    wrong = rn - rc
    # upper: drop as many wrong RFI items as possible
    up_drop_wrong = min(n_dropped, wrong)
    up_drop_right = n_dropped - up_drop_wrong
    upper = (tot_c - up_drop_right) / n_after
    # lower: drop as many right RFI items as possible
    lo_drop_right = min(n_dropped, rc)
    lower = (tot_c - lo_drop_right) / n_after
    # expected under a uniform random subset of the RFI items
    expected = (tot_c - n_dropped * rc / rn) / n_after
    return {"n_after": n_after, "lower": lower, "expected_random_drop": expected, "upper": upper}


def score(rows, probs_fwd, probs_rev, probs_avg):
    by_id = {r["id"]: r for r in rows}
    if set(probs_avg) != set(by_id):
        raise ValueError("prediction ids do not match the When2Call rows")
    ids = sorted(by_id)
    correct = {}
    per_order = {}
    for name, pr in (("avg", probs_avg), ("fwd", probs_fwd), ("rev", probs_rev)):
        correct[name] = [int(C.argmax_option(pr[i]) == by_id[i]["gold"]) for i in ids]
        per_order[name] = sum(correct[name]) / len(ids)
    cls = {}
    for k in REPLY_KEYS:
        if k == "direct":
            continue
        idx = [j for j, i in enumerate(ids) if by_id[i]["meta"]["correct_answer"] == k]
        cls[k] = (sum(correct["avg"][j] for j in idx), len(idx))
    acc = sum(correct["avg"]) / len(ids)
    k_correct = sum(correct["avg"])
    chosen = {}
    for i in ids:
        a = C.argmax_option(probs_avg[i])
        key = REPLY_KEYS[by_id[i]["options"].index(a)]
        chosen[key] = chosen.get(key, 0) + 1
    lo, hi = C.wilson(k_correct, len(ids))
    return {
        "set": SET, "protocol_status": PROTOCOL_STATUS, "n": len(ids), "aa_published_n": AA_N,
        "accuracy_full": acc, "accuracy_full_wilson95": [lo, hi],
        "accuracy_by_order": per_order,
        "accuracy_by_class": {k: {"correct": c, "n": n, "acc": c / n} for k, (c, n) in cls.items()},
        "chosen_reply_counts": chosen,
        "aa_style_bounds": aa_bounds(cls),
        "per_item_correct_avg": dict(zip(ids, correct["avg"])),
    }


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    sub = ap.add_subparsers(dest="cmd", required=True)
    b = sub.add_parser("build")
    b.add_argument("--out", default=str(C.QUARANTINE / SET / "rows"))
    s = sub.add_parser("score")
    s.add_argument("--rows", default=str(C.QUARANTINE / SET / "rows" / "rows.jsonl"))
    s.add_argument("--fwd", required=True)
    s.add_argument("--rev", required=True)
    s.add_argument("--out", required=True)
    a = ap.parse_args(argv)
    if a.cmd == "build":
        rows = build_rows()
        out = Path(a.out)
        _, status, fsha = load_format()
        man = {"set": SET, "n": len(rows), "rows_sha256": C.write_jsonl(out / "rows.jsonl", rows),
               "views_sha256": C.write_json(out / "views.json", C.make_views(rows)), "view_seed": C.SEED,
               "format_status": status, "format_sha256": fsha, "protocol_status": PROTOCOL_STATUS,
               "source_sha256": C.sha256_file(SRC)}
        C.write_json(out / "manifest.json", man)
        print(json.dumps(man, indent=1))
    else:
        rows = C.read_jsonl(a.rows)
        f, r, avg = C.load_both_orders(a.fwd, a.rev)
        res = score(rows, f, r, avg)
        C.write_json(a.out, res)
        print(json.dumps({k: v for k, v in res.items() if k != "per_item_correct_avg"}, indent=1))


if __name__ == "__main__":
    main()
