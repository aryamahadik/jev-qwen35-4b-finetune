"""Latency, API against API: send the SAME 515 bundled eval requests Jev received (data/eval_calls.jsonl, same seeded
question order) to our deployed endpoint, from this laptop, and time the client wall-clock exactly like run_jev.py.

  OD_URL=https://...modal.run python bench_api.py      -> preds/q4b_v05_A3_api.jsonl + logs/bench_api.json
"""
import asyncio
import json
import os
import random
import statistics
import time
from pathlib import Path

import httpx

HERE = Path(__file__).resolve().parent
URL = os.environ["OD_URL"]
CONC = int(os.environ.get("OD_CONC", "8"))  # run_jev.py used 8 concurrent calls
rows = {json.loads(l)["id"]: json.loads(l) for l in open(HERE / "data/eval.jsonl")}
calls = [json.loads(l) for l in open(HERE / "data/eval_calls.jsonl")]


def q(r):
    d = {"type": r["qtype"], "instructions": r["instructions"]}
    if r["qtype"] == "choice":
        d["options"] = r["options"]
    return d


async def main():
    out, lat, srv = [], [], []
    async with httpx.AsyncClient(timeout=600) as client:
        for _ in range(3):  # warm the container (cold start is not part of steady-state latency; reported separately)
            t = time.perf_counter()
            await client.post(URL, json={"state": "warm up", "questions": {"q": {"type": "noul", "instructions": "Is this a test?"}}})
            print(f"warm-up call {(time.perf_counter() - t) * 1000:.0f} ms")
        sem = asyncio.Semaphore(CONC)

        async def one(c):
            rid = list(c["row_ids"])
            random.Random(c["call_id"]).shuffle(rid)  # same seeded order as run_jev.py
            qmap = {f"q{i}": r for i, r in enumerate(rid)}
            async with sem:
                t = time.perf_counter()
                res = (await client.post(URL, json={"state": c["state"], "questions": {k: q(rows[v]) for k, v in qmap.items()}})).json()
                ms = (time.perf_counter() - t) * 1000
            lat.append(ms)
            srv.append(res["server_ms"])
            for k, rid_ in qmap.items():
                a = res["answers"][k]
                probs = {"yes": a["noul"], "no": 1 - a["noul"]} if a["type"] == "noul" else a["probabilities"]
                out.append({"id": rid_, "model": "q4b_v05_A3_api", "probs": probs, "latency_ms": ms})

        await asyncio.gather(*(one(c) for c in calls))
    with open(HERE / "preds/q4b_v05_A3_api.jsonl", "w") as f:
        for o in out:
            f.write(json.dumps(o) + "\n")
    s = sorted(lat)
    stats = {"calls": len(lat), "client_median_ms": statistics.median(lat), "client_p95_ms": s[int(0.95 * len(s))],
             "server_median_ms": statistics.median(srv), "concurrency": CONC,
             "note": "client wall-clock from the same laptop/network as the Jev run; includes network + Modal web routing"}
    (HERE / "logs/bench_api.json").write_text(json.dumps(stats, indent=2))
    print(json.dumps(stats, indent=2))


asyncio.run(main())
