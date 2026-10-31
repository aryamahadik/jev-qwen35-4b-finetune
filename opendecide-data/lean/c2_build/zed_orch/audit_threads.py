"""Audit Zed subagent threads (read-only): for every descendant of ROOT created at/after --since, list the model, the
first prompt line, each tool call (name + path/command) and the final reply. With --reads, check the blind-read
contract: only read_file on the task file and write_file on the answer file named in the prompt."""
import argparse, json, re, sqlite3, zstandard
DB = "/Users/aryamahadik/Library/Application Support/Zed/threads/threads.db"
ap = argparse.ArgumentParser()
ap.add_argument("--root", default="01e71618-d54d-4929-8250-005267193512")
ap.add_argument("--since", default="")
ap.add_argument("--match", default="")
ap.add_argument("--reads", action="store_true")
ap.add_argument("--quiet", action="store_true")
a = ap.parse_args()
con = sqlite3.connect(f"file:{DB}?mode=ro", uri=True)
rows = con.execute("select id, parent_id, created_at, data from threads").fetchall()
kids = {}
for tid, pid, ca, blob in rows:
    kids.setdefault(pid, []).append((tid, ca, blob))
dz = zstandard.ZstdDecompressor()
def walk(t):
    for tid, ca, blob in kids.get(t, []):
        yield tid, ca, blob
        yield from walk(tid)
bad = ok = 0
for tid, ca, blob in sorted(walk(a.root), key=lambda x: x[1] or ""):
    if a.since and (ca or "") < a.since:
        continue
    d = json.loads(dz.decompress(blob, max_output_size=500_000_000))
    msgs = d.get("messages", [])
    first = ""
    if msgs and "User" in msgs[0]:
        first = " ".join(c.get("Text", "") for c in msgs[0]["User"]["content"] if isinstance(c, dict))
    if a.match and a.match not in first:
        continue
    calls, final = [], ""
    for m in msgs:
        if "Agent" in m:
            for c in m["Agent"]["content"]:
                if "ToolUse" in c:
                    v = (c["ToolUse"].get("input") or {}).get("value") or {}
                    calls.append((c["ToolUse"]["name"], v.get("path") or v.get("command") or json.dumps(v)[:120]))
                elif "Text" in c and c["Text"].strip():
                    final = c["Text"].strip()
    model = (d.get("model") or {}).get("model", "?")
    if a.reads:
        task = re.search(r"jev/\S+?(?:tasks|chunks)/\S+?\.(?:md|txt|json)", first)
        ans = re.search(r"jev/\S+?answers/\S+?\.json", first)
        allowed = {("read_file", task.group(0) if task else None), ("write_file", ans.group(0) if ans else None)}
        extra = [c for c in calls if (c[0], c[1]) not in allowed]
        wrote = any(c[0] == "write_file" for c in calls)
        status = "OK" if (not extra and wrote) else "AUDIT_FAIL"
        bad += status != "OK"; ok += status == "OK"
        if not a.quiet or status != "OK":
            print(f"{status} {tid[:8]} {model} task={task.group(0).split('/')[-1] if task else '?'} calls={len(calls)} "
                  f"extra={extra[:3]} reply={final[:60]!r}")
    else:
        print(f"== {tid[:8]} {ca} {model} :: {first[:110]!r}\n   calls={len(calls)} last={calls[-3:]}\n   reply={final[:300]!r}")
if a.reads:
    print(f"reads audited: ok={ok} fail={bad}")
