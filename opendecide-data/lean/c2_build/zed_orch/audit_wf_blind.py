#!/usr/bin/env python3
"""A57 step-3 read audit for workflow blind() readers (prompt: "Your ONLY task file is: <t> ... to exactly: <a>").

Usage: audit_wf_blind.py --task-prefix <abs path prefix> [--root <workflows dir>] [--out result.json]

Scans every agent-*.jsonl under every workflow run in --root. A reader whose task OR answer file starts with --task-prefix passes
only if every tool call is Read of its task file, Write/Edit of its answer file, or StructuredOutput, and it wrote the
answer file. Readers still running (no write yet) are listed as NO-WRITE. Prints basenames and tool names only, never
item content. Agents may run this script; they never open the transcripts themselves.
"""
import argparse, glob, json, os, re

ROOT = "/Users/aryamahadik/.claude/projects/-Users-aryamahadik-Documents-jev/adbc4a3b-e366-431b-b0e2-96c55904b928/subagents/workflows"
TF = re.compile(r"Your ONLY task file is:\s*\n\s*(\S+)")
AF = re.compile(r"to exactly:\s*\n\s*(\S+)")


def scan(path):
    prompt, calls = None, []
    for line in open(path, encoding="utf-8"):
        try:
            rec = json.loads(line)
        except json.JSONDecodeError:
            continue
        c = (rec.get("message") or {}).get("content")
        if rec.get("type") == "user" and prompt is None:
            txt = c if isinstance(c, str) else " ".join(b.get("text", "") for b in (c or []) if isinstance(b, dict) and b.get("type") == "text")
            if TF.search(txt or ""):
                prompt = txt
        if rec.get("type") == "assistant" and isinstance(c, list):
            for b in c:
                if isinstance(b, dict) and b.get("type") == "tool_use":
                    calls.append((b.get("name"), (b.get("input") or {}).get("file_path")))
    return prompt, calls


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--task-prefix", required=True)
    ap.add_argument("--root", default=ROOT)
    ap.add_argument("--out")
    a = ap.parse_args()
    res = {"task_prefix": a.task_prefix, "ok": 0, "bad": [], "no_write": [], "readers": 0}
    for p in sorted(glob.glob(os.path.join(a.root, "*", "agent-*.jsonl"))):
        prompt, calls = scan(p)
        if not prompt:
            continue
        t, m = TF.search(prompt).group(1), AF.search(prompt)
        if not m:
            continue
        ans = m.group(1)
        if not (t.startswith(a.task_prefix) or ans.startswith(a.task_prefix)):
            continue
        res["readers"] += 1
        v = [f"{n}:{os.path.basename(fp or '-')}" for n, fp in calls
             if not ((n == "Read" and fp == t) or (n in ("Write", "Edit") and fp == ans) or n == "StructuredOutput")]
        wrote = any(n in ("Write", "Edit") and fp == ans for n, fp in calls)
        tag = {"task": os.path.basename(t), "run": os.path.basename(os.path.dirname(p)), "violations": v[:8]}
        if v:
            res["bad"].append(tag)
        elif not wrote:
            res["no_write"].append(tag)
        else:
            res["ok"] += 1
    for b in res["bad"]:
        print("BAD", b["task"], b["violations"])
    for b in res["no_write"]:
        print("NO-WRITE", b["task"])
    print(json.dumps({"readers": res["readers"], "ok": res["ok"], "bad": len(res["bad"]), "no_write": len(res["no_write"])}))
    if a.out:
        json.dump(res, open(a.out, "w"), indent=1)


if __name__ == "__main__":
    main()
