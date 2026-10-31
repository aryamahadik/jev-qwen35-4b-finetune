"""c2_kit/audit.py: the file-access auditor for Haiku task agents (TEACH-0 pattern; C2_DATA_SPEC 6.5).

A Haiku agent may read only its own chunk file and the batch prompt, and write only its own answer file. The auditor
walks the agent's transcript (any JSON / JSONL whose records contain tool-use blocks {"type": "tool_use", "name",
"input"}) and reports every tool call that steps outside that:
  critical   a path on the never-open list (paths.never_open), anywhere in a call's input
  violation  a read or write of any other path; a tool other than the allowed ones (by default Read and Write);
             Bash, Glob, Grep, web and agent-spawning tools (they can reach other chunks or the network)
  note       an allowed read path that was never read (the agent may have answered blind)
The report passes only with zero critical and zero violation entries. A failed audit discards that agent's answers
(the task is re-run with a fresh agent). The orchestrator passes the transcript; this module never looks for one.

  rep = audit(events, allowed_read={chunk, prompt}, allowed_write={answer})   # events: parsed JSON records
  rep = audit_jsonl(path, ...)                                                # reads a transcript file it is given
"""
from __future__ import annotations

import json
import os
import re
import shlex
from dataclasses import dataclass, field

from .paths import never_open

PATH_KEYS = ("file_path", "path", "notebook_path", "pattern", "glob", "url", "command", "cwd", "directory")
READ_TOOLS = {"Read": "file_path", "NotebookRead": "notebook_path"}
WRITE_TOOLS = {"Write": "file_path", "Edit": "file_path", "MultiEdit": "file_path", "NotebookEdit": "notebook_path"}
ALWAYS_BAD = ("Bash", "Glob", "Grep", "LS", "WebFetch", "WebSearch", "Task", "Agent", "Skill")


@dataclass(frozen=True)
class ToolCall:
    name: str
    input: dict


@dataclass
class AuditReport:
    ok: bool = True
    n_calls: int = 0
    reads: list = field(default_factory=list)
    writes: list = field(default_factory=list)
    entries: list = field(default_factory=list)      # (severity, tool, detail)

    def add(self, severity, tool, detail):
        self.entries.append((severity, tool, detail))
        if severity in ("critical", "violation"):
            self.ok = False

    def as_dict(self) -> dict:
        return {"ok": self.ok, "n_calls": self.n_calls, "reads": self.reads, "writes": self.writes,
                "critical": [e for e in self.entries if e[0] == "critical"],
                "violations": [e for e in self.entries if e[0] == "violation"],
                "notes": [e for e in self.entries if e[0] == "note"]}


def tool_calls(events) -> list:
    """Every tool-use block in a transcript (records nested at any depth)."""
    out = []

    def walk(o):
        if isinstance(o, dict):
            if o.get("type") == "tool_use" and isinstance(o.get("name"), str):
                out.append(ToolCall(o["name"], o.get("input") or {}))
                return
            for v in o.values():
                walk(v)
        elif isinstance(o, list):
            for v in o:
                walk(v)

    walk(events)
    return out


def _norm(p: str) -> str:
    return os.path.normpath(os.path.expanduser(str(p)))


def _path_strings(inp: dict) -> list:
    out = []
    for k, v in inp.items():
        if not isinstance(v, str):
            continue
        if k == "command":
            try:
                toks = shlex.split(v)
            except ValueError:
                toks = v.split()
            out += [t for t in toks if "/" in t or t.startswith("~")]
        elif k in PATH_KEYS:
            out.append(v)
    return out


def audit(events, *, allowed_read, allowed_write, allow_tools=("Read", "Write")) -> AuditReport:
    rep = AuditReport()
    ar = {_norm(p) for p in allowed_read}
    aw = {_norm(p) for p in allowed_write}
    calls = tool_calls(events)
    rep.n_calls = len(calls)
    read_seen = set()
    for c in calls:
        for s in _path_strings(c.input):
            for m in re.finditer(r"[~/][^\s'\"`;|&<>]*", s) if c.name == "Bash" else [re.match(r".*", s)]:
                why = never_open(m.group())
                if why:
                    rep.add("critical", c.name, f"never-open path ({why}): {m.group()[:80]}")
        if c.name not in allow_tools or c.name in ALWAYS_BAD:
            rep.add("violation", c.name, "tool not allowed for Haiku task agents")
            continue
        if c.name in READ_TOOLS:
            p = _norm(c.input.get(READ_TOOLS[c.name], ""))
            rep.reads.append(p)
            if p in ar:
                read_seen.add(p)
            else:
                rep.add("violation", c.name, f"read outside the task: {p}")
        elif c.name in WRITE_TOOLS:
            p = _norm(c.input.get(WRITE_TOOLS[c.name], ""))
            rep.writes.append(p)
            if p not in aw:
                rep.add("violation", c.name, f"write outside the task: {p}")
        else:
            rep.add("violation", c.name, "allowed tool with no audit rule")
    for p in sorted(ar - read_seen):
        rep.add("note", "Read", f"allowed path never read: {p}")
    return rep


def audit_jsonl(path, **kw) -> AuditReport:
    """Audit a transcript file the orchestrator names (JSONL, or one JSON document)."""
    text = open(path, encoding="utf-8").read()
    try:
        events = [json.loads(line) for line in text.splitlines() if line.strip()]
    except ValueError:
        events = json.loads(text)
    return audit(events, **kw)
