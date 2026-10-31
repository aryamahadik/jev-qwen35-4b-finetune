#!/usr/bin/env python3
"""W7: tool routing with abstain (PREREG_FINAL A40 b). Gold = CONSTRUCTION from Haiku-authored pieces.

Input: author/answers/W7_tNN.json (brief: make_tasks.W7_BRIEF). Per setting Haiku wrote a catalog of 3-7 tools, 2
requests filed under each tool (each with "if_tool_removed": another catalog tool or "no_tool") and 4 requests in
the "no_tool" slot. Rows (choice; options = the catalog's tools in a seeded order, then "no_tool"; card = one
"- tool: description" line per option; state = the request; instructions = the question naming the setting):
  base      options = the full catalog + no_tool; gold = the tool the request is filed under, or no_tool;
  removed   the same request with its tool taken out of the options; gold = its "if_tool_removed" answer (another
            catalog tool or no_tool), recorded as Haiku stated it (A40 c verifies it blind like every row).
Every gold is a slot or a stated answer of the brief; nothing is chosen here. Malformed catalogs (tool names, > 7
tools, unknown tool references) are dropped whole; malformed requests alone. Balance: removed rows are added (seeded)
only while no_tool stays <= NO_TOOL_MAX of the type, and the total is capped at TARGET.

  ../../../../../.venv/bin/python -I builders/w7_tools.py [--dry-run]
"""
from __future__ import annotations

import re
import sys
from collections import Counter
from pathlib import Path

if __package__ in (None, ""):
    sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from builders import common as C  # noqa: E402

T = "W7"
NO_TOOL = "no_tool"
NO_TOOL_DEF = ("none of the listed tools can do what the request needs, so the assistant should reply without "
               "calling a tool (answer, ask a question or decline).")
NAME = re.compile(r"^[a-z][a-z0-9]*(?:_[a-z0-9]+){1,5}$")
MAX_TOOLS = C.MAX_OPTIONS - 1
NO_TOOL_MAX = 0.33
TARGET = 1750
NT_KINDS = ("near_miss", "general_chat_or_knowledge", "out_of_domain")
QUESTIONS = ("An assistant for {setting} can call the tools listed in the options. Which one should it call for the "
             "user request below? Choose no_tool if none of the listed tools can do it.",
             "Tool routing for {setting}: which listed tool should handle the user request below? Choose no_tool if no "
             "listed tool fits.")


def catalog_tools(cat: dict) -> tuple:
    """({name: description}, problem or None)."""
    tools = cat.get("tools")
    if not isinstance(tools, list) or not 3 <= len(tools) <= MAX_TOOLS:
        return None, "tools_count"
    out = {}
    for t in tools:
        if not isinstance(t, dict):
            return None, "tool_not_object"
        name = t.get("name")
        if not isinstance(name, str) or not NAME.match(name) or name == NO_TOOL or name in out:
            return None, "tool_name"
        d, why = C.text_field(t.get("description"), min_w=3, max_w=45, single_line=True)
        if why:
            return None, "tool_description"
        out[name] = d
    return out, None


def make(tid, cid, setting, tools: dict, order: list, text: str, gold: str, *, variant: str, req_key: str,
         removed: str | None, prov: dict, extra: dict) -> dict:
    opts = [t for t in order if t != removed] + [NO_TOOL]
    defs = dict(tools, **{NO_TOOL: NO_TOOL_DEF})
    qi = C.pick_wording(QUESTIONS, T, tid, cid, req_key)
    return C.make_row(
        T, f"{tid}:{cid}:{req_key}:{variant}", f"c2_wave2:W7:{tid}:{cid}", text,
        QUESTIONS[qi].format(setting=setting), qtype="choice", options=opts, gold=gold,
        card=C.card_lines([(o, defs[o]) for o in opts]), gold_method="construction",
        construction={"variant": variant, "removed_tool": removed, "n_tools": len(opts) - 1, "setting": setting,
                      **extra},
        extra_meta={"wording_id": f"W7.q{qi}", "licence": C.LICENCE_AUTHORED, **prov})


def build(key: dict | None = None, answers: dict | None = None, checker=None, target: int = TARGET) -> tuple:
    base, twins, drops, tasks_seen, dd = [], [], Counter(), {}, C.Dedup()
    for tid, kk, obj, probs, prov in C.iter_answers(T, key, answers):
        tasks_seen[tid] = {"answered": obj is not None, "problems": probs}
        if obj is None:
            continue
        want = kk["settings"]
        cats = obj.get("catalogs")
        if not isinstance(cats, list):
            tasks_seen[tid]["problems"].append("catalogs is not a list")
            continue
        seen = set()
        for cat in cats:
            cid = cat.get("c_id") if isinstance(cat, dict) else None
            if cid not in want or cid in seen:
                drops["unknown_or_repeated_c_id"] += 1
                continue
            seen.add(cid)
            tools, why = catalog_tools(cat)
            if why:
                drops[f"catalog_{why}"] += 1
                continue
            setting = C.one_line(want[cid]["setting"])
            order = sorted(tools, key=lambda n: C.key_hash(C.SEED, T, "order", tid, cid, n))
            treq = cat.get("tool_requests")
            if not isinstance(treq, list):
                drops["tool_requests_not_a_list"] += 1
                treq = []
            per_tool = Counter()
            for j, rq in enumerate(treq):
                if not isinstance(rq, dict) or rq.get("tool") not in tools:
                    drops["request_unknown_tool"] += 1
                    continue
                text, why = C.text_field(rq.get("text"), min_w=1, max_w=90)
                if why:
                    drops[f"request_{why.split(' ')[0]}"] += 1
                    continue
                if not dd.new(cid + tid, text):
                    drops["duplicate_request"] += 1
                    continue
                tool = rq["tool"]
                per_tool[tool] += 1
                rk = f"r{j + 1:02d}"
                base.append(make(tid, cid, setting, tools, order, text, tool, variant="base", req_key=rk,
                                 removed=None, prov=prov, extra={"slot": tool}))
                alt = rq.get("if_tool_removed")
                if alt == NO_TOOL or (alt in tools and alt != tool):
                    twins.append(make(tid, cid, setting, tools, order, text, alt, variant="removed", req_key=rk,
                                      removed=tool, prov=prov, extra={"slot": tool, "if_tool_removed": alt}))
                else:
                    drops["if_tool_removed_invalid"] += 1
            if set(per_tool) != set(tools) or any(v != 2 for v in per_tool.values()):
                drops["catalog_request_counts_off"] += 1          # recorded; the valid requests are still used
            nreq = cat.get("no_tool_requests")
            for j, rq in enumerate(nreq if isinstance(nreq, list) else []):
                if not isinstance(rq, dict):
                    drops["item_not_object"] += 1
                    continue
                text, why = C.text_field(rq.get("text"), min_w=1, max_w=90)
                if why:
                    drops[f"no_tool_request_{why.split(' ')[0]}"] += 1
                    continue
                if not dd.new(cid + tid, text):
                    drops["duplicate_request"] += 1
                    continue
                kind = rq.get("kind") if rq.get("kind") in NT_KINDS else "other"
                base.append(make(tid, cid, setting, tools, order, text, NO_TOOL, variant="base", req_key=f"n{j + 1:02d}",
                                 removed=None, prov=prov, extra={"slot": NO_TOOL, "kind": kind}))
    kept_b, rd_b, tok_b = C.check_all(base, checker)
    kept_t, rd_t, tok_t = C.check_all(twins, checker)
    # balance: all base rows (capped at target), then removed rows while no_tool <= NO_TOOL_MAX and total <= target
    kept_b.sort(key=lambda r: C.key_hash(C.SEED, T, "base", r["id"]))
    out = kept_b[:target]
    nt = sum(r["gold"] == NO_TOOL for r in out)
    for r in sorted(kept_t, key=lambda r: C.key_hash(C.SEED, T, "twin", r["id"])):
        if len(out) >= target:
            break
        if r["gold"] == NO_TOOL and (nt + 1) / (len(out) + 1) > NO_TOOL_MAX:
            continue
        out.append(r)
        nt += r["gold"] == NO_TOOL
    out.sort(key=lambda r: r["id"])
    gl = Counter("no_tool" if r["gold"] == NO_TOOL else "tool" for r in out)
    stats = C.authored_stats(T, tasks_seen, drops, base + twins, out, rd_b + rd_t, tok_b + tok_t, {
        "labels": {"n": len(out), "labels": dict(gl)}, "base_rows": len(kept_b), "removed_rows_available": len(kept_t),
        "removed_rows_used": sum(r["meta"]["construction"]["variant"] == "removed" for r in out),
        "no_tool_share": round(gl["no_tool"] / max(1, len(out)), 4), "target": target,
        "options_per_row": dict(Counter(len(r["options"]) for r in out)),
        "gold_position": dict(Counter(r["options"].index(r["gold"]) for r in out))})
    return out, stats


def main(argv=None):
    argv = sys.argv[1:] if argv is None else argv
    rows, stats = build()
    return C.finish_authored(T, rows, stats, argv)


if __name__ == "__main__":
    main()
