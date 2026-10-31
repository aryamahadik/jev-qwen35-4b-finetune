"""Tiny client for the local decision server (stdlib only). Times request -> typed answer for a sample of items.
The clock starts before the body is built, so reading the file, base64 encoding and JSON serialisation are inside the time,
like the bench's run_decisions.py (which times upload + encoding + the HTTP round trip). Excludes internet (localhost).
Sample: the first --n items of every suite, in suite order. --conc N requests in flight (1 = sequential)."""
import argparse
import base64
import http.client
import json
import os
import threading
import time

ap = argparse.ArgumentParser()
ap.add_argument("--port", type=int, required=True)
ap.add_argument("--n", type=int, default=20)
ap.add_argument("--conc", type=int, default=1)
ap.add_argument("--out", required=True)
ap.add_argument("--data", required=True)
a = ap.parse_args()
SUITES = ["img_sst2", "img_ar_sentiment", "img_pets", "img_vqa_yesno", "img_count"]
cases = []
for s in SUITES:
    k = 0
    for line in open(f"{a.data}/{s}/cases.jsonl", encoding="utf-8"):
        cases.append((s, json.loads(line)))
        k += 1
        if k == a.n:
            break
MIME = {"png": "image/png", "jpg": "image/jpeg"}
rows, lock, idx = [], threading.Lock(), [0]


def one(conn, s, c):
    path = f"{a.data}/{s}/images/{os.path.basename(c['state'][0]['image'])}"
    t0 = time.perf_counter()
    raw = open(path, "rb").read()
    body = json.dumps({"state": [{"image": f"data:{MIME[path.rsplit('.', 1)[1]]};base64," + base64.b64encode(raw).decode()}],
                       "questions": c["questions"]}).encode()
    conn.request("POST", "/decisions", body=body, headers={"Content-Type": "application/json"})
    r = conn.getresponse()
    data = json.loads(r.read())
    ms = (time.perf_counter() - t0) * 1000
    rec = {"id": c["id"], "e2e_ms": ms, "status": r.status, "body_bytes": len(body)}
    if r.status == 200:
        rec["server_ms"] = data["server_ms"]
        rec["answers"] = data["answers"]
    else:
        rec["error"] = data.get("error")
    return rec


def worker():
    conn = http.client.HTTPConnection("127.0.0.1", a.port, timeout=300)
    while True:
        with lock:
            i = idx[0]
            idx[0] += 1
        if i >= len(cases):
            return
        s, c = cases[i]
        rec = one(conn, s, c)
        with lock:
            rows.append(rec)


# warm the connection path with one untimed request (the server model is already warm from the eval passes)
w = http.client.HTTPConnection("127.0.0.1", a.port, timeout=300)
one(w, *cases[0])
w.close()
ts = [threading.Thread(target=worker) for _ in range(a.conc)]
t0 = time.perf_counter()
[t.start() for t in ts]
[t.join() for t in ts]
wall = time.perf_counter() - t0
with open(a.out, "w") as f:
    for r in rows:
        f.write(json.dumps(r) + "\n")
print(json.dumps({"conc": a.conc, "n": len(rows), "wall_s": wall, "errors": sum("error" in r for r in rows)}))
