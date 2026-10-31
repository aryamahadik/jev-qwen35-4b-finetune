#!/usr/bin/env python3
"""Blind-read file-access audit for Claude Code workflow readers (the Claude Code twin of audit_threads.py --reads).

Usage: audit_cc_reads.py <workflow transcript dir> [--out result.json]

Each reader agent's prompt names exactly one task file (.md) and one answer file (.json). The reader passes only if
every tool call it made is Read of its own task file or Write/Edit of its own answer file. Any other tool, path or a
missing answer write is a violation. Only paths and tool names are printed, never item content.
"""
import glob
import json
import os
import re
import sys

TASK_RE = re.compile(r"(/\S+?/tasks/[^\s/]+\.md)")
ANS_RE = re.compile(r"(/\S+?/answers/[^\s/]+\.json)")


def _blocks(rec):
    msg = rec.get("message") or {}
    content = msg.get("content")
    return content if isinstance(content, list) else []


def audit_agent(path):
    task = ans = None
    calls = []
    with open(path, encoding="utf-8") as f:
        for line in f:
            try:
                rec = json.loads(line)
            except json.JSONDecodeError:
                continue
            if rec.get("type") == "user" and task is None:
                text = json.dumps(rec.get("message", {}))
                m1, m2 = TASK_RE.search(text), ANS_RE.search(text)
                if m1 and m2:
                    task, ans = m1.group(1), m2.group(1)
                elif m1:   # answer path named only in the task header: tasks/<id>.md -> answers/<id>.json
                    task = m1.group(1)
                    ans = task.replace("/tasks/", "/answers/")[:-3] + ".json"
            for b in _blocks(rec):
                if isinstance(b, dict) and b.get("type") == "tool_use":
                    calls.append((b.get("name"), b.get("input") or {}))
    if task is None:
        return None
    bad, wrote = [], False
    for name, inp in calls:
        p = inp.get("file_path") or inp.get("path") or ""
        if name == "Read" and p in (task, ans):   # re-reading its own answer file is harmless
            continue
        if name in ("Write", "Edit") and p == ans:
            wrote = wrote or name == "Write"
            continue
        if name == "StructuredOutput":
            continue
        bad.append(f"{name}:{os.path.basename(p) if p else '-'}")
    return {"task": os.path.basename(task), "ok": not bad and wrote, "wrote": wrote, "violations": bad}


def main():
    d = sys.argv[1]
    rows = [r for r in (audit_agent(p) for p in sorted(glob.glob(os.path.join(d, "agent-*.jsonl")))) if r]
    res = {"readers": len(rows), "ok": sum(r["ok"] for r in rows),
           "violations": [r for r in rows if r["violations"]], "no_write": [r["task"] for r in rows if not r["wrote"]]}
    if "--out" in sys.argv:
        json.dump(res, open(sys.argv[sys.argv.index("--out") + 1], "w"), indent=1)
    print(json.dumps({k: (v if k in ("readers", "ok") else len(v)) for k, v in res.items()}))
    for r in res["violations"][:20]:
        print("VIOLATION", r["task"], r["violations"][:5])


if __name__ == "__main__":
    main()
