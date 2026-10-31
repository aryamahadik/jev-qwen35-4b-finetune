"""Condense a Claude Code subagent transcript (.jsonl) into a short resume log: every assistant note, every tool call
(description + first 300 chars of the command) and the last N tool results (first 700 chars each)."""
import json, sys
src, dst, last_n = sys.argv[1], sys.argv[2], int(sys.argv[3]) if len(sys.argv) > 3 else 30
ev = []
for line in open(src):
    try:
        o = json.loads(line)
    except Exception:
        continue
    c = (o.get("message") or {}).get("content")
    if not isinstance(c, list):
        continue
    for b in c:
        t = b.get("type")
        if o.get("type") == "assistant" and t == "text" and b.get("text", "").strip():
            ev.append(("note", b["text"].strip()[:1200]))
        elif o.get("type") == "assistant" and t == "tool_use":
            i = b.get("input") or {}
            cmd = (i.get("command") or i.get("file_path") or json.dumps(i))[:300].replace("\n", " \\n ")
            ev.append(("call", f"{i.get('description', b.get('name'))} :: {cmd}"))
        elif o.get("type") == "user" and t == "tool_result":
            cc = b.get("content")
            s = " ".join(x.get("text", "") for x in cc if isinstance(x, dict)) if isinstance(cc, list) else str(cc)
            ev.append(("result", s.strip()[:700].replace("\n", " \\n ")))
res_idx = [k for k, (t, _) in enumerate(ev) if t == "result"]
keep = set(res_idx[-last_n:])
with open(dst, "w") as f:
    for k, (t, s) in enumerate(ev):
        if t == "result" and k not in keep:
            continue
        f.write({"note": "NOTE: ", "call": "  CALL: ", "result": "    RESULT: "}[t] + s + "\n")
