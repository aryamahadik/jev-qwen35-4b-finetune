"""Jev on the high-cardinality slice (eval_hc). Jev's API rejects more than 255 choices (HTTP 400), so a user
has to wrap it. Two wrappers, both favourable to Jev:

  JEV_HC_MODE=tournament  N <= 255: one call. N > 255: split the non-abstain options into chunks of <= 254, one
                          parallel Jev call per chunk, keep each chunk's top 3, then one final call on the winners
                          plus the abstain option. Latency = slowest chunk call + final call.
  JEV_HC_MODE=shortlist   the same embedding shortlist our model uses, widened to Jev's 255-option maximum
                          (data/<split>_shortlist_255.json, written on Modal by modal_od.py::hc_shortlist).

Writes preds_<split>/jev_<mode>.jsonl (+ _raw). Resumable. Never trains on Jev outputs.
"""
import asyncio
import json
import os
import sys
import time
from pathlib import Path

HERE = Path(__file__).resolve().parent
for envf in (HERE.parent / ".env", HERE / ".env"):
    if envf.exists():
        for line in envf.read_text().splitlines():
            if "=" in line and not line.strip().startswith("#"):
                k, v = line.split("=", 1)
                os.environ.setdefault(k.strip(), v.strip().strip('"').strip("'"))
if not os.environ.get("OPENROUTER_API_KEY"):
    sys.exit("NO_KEY: OPENROUTER_API_KEY")
from typesafe_sdk import AsyncTypeSafeClient, Choice  # noqa: E402

SPLIT = os.environ.get("JEV_SPLIT", "eval_hc")
MODE = os.environ.get("JEV_HC_MODE", "tournament")
LIMIT = int(os.environ.get("JEV_LIMIT", "0"))
MAXC, KEEP = 255, 3
PD = HERE / f"preds_{SPLIT}"
PD.mkdir(exist_ok=True)
rows = [json.loads(l) for l in open(HERE / f"data/{SPLIT}.jsonl")]
raw_path = PD / f"jev_{MODE}_raw.jsonl"
done = {json.loads(l)["id"] for l in open(raw_path) if json.loads(l).get("probs")} if raw_path.exists() else set()
todo = [r for r in rows if r["id"] not in done][: LIMIT or None]
short = json.loads((HERE / f"data/{SPLIT}_shortlist_255.json").read_text()) if MODE == "shortlist" else None


def is_none(o):
    return o.startswith("none of")


async def main():
    client = AsyncTypeSafeClient(api_key=os.environ["OPENROUTER_API_KEY"], base_url="https://openrouter.ai/api")
    sem = asyncio.Semaphore(8)
    lock = asyncio.Lock()

    async def ask(r, opts):
        async with sem:
            for attempt in range(4):
                t = time.perf_counter()
                try:
                    res = await client.system_one(state=r["state"], model="jev-1.13", timeout=180, questions={
                        "q": Choice(instructions=r["instructions"], criteria={o: None for o in opts})})
                    ms = (time.perf_counter() - t) * 1000
                    pr = {k: float(v) for k, v in res.answers["q"].model_dump()["probabilities"].items()}
                    return pr, ms, None
                except Exception as e:  # noqa: BLE001
                    err = repr(e)[:300]
                    await asyncio.sleep(2 ** attempt)
        return None, None, err

    async def one(r):
        none = [o for o in r["options"] if is_none(o)]
        pool = [o for o in r["options"] if not is_none(o)]
        if MODE == "shortlist" and len(r["options"]) > MAXC:
            pool = short[r["id"]][: MAXC - len(none)]
        calls, lat, err = 0, 0.0, None
        if len(pool) + len(none) > MAXC:
            chunks = [pool[i:i + MAXC - 1] for i in range(0, len(pool), MAXC - 1)]
            res = await asyncio.gather(*(ask(r, c) for c in chunks))
            calls += len(chunks)
            if any(p is None for p, _, _ in res):
                err = next(e for p, _, e in res if p is None)
                pool = None
            else:
                lat += max(ms for _, ms, _ in res)
                pool = [o for p, _, _ in res for o, _ in sorted(p.items(), key=lambda x: -x[1])[:KEEP]]
        probs = None
        if pool is not None:
            p, ms, err = await ask(r, pool + none)
            calls += 1
            if p is not None:
                lat += ms
                s = sum(p.values()) or 1.0
                probs = {o: v / s for o, v in p.items()}
        rec = {"id": r["id"], "model": f"jev_{MODE}", "probs": probs, "latency_ms": lat if probs else None,
               "jev_calls": calls, "error": None if probs else err}
        async with lock:
            with open(raw_path, "a") as f:
                f.write(json.dumps(rec) + "\n")

    await asyncio.gather(*(one(r) for r in todo))


print(f"{SPLIT} mode={MODE}: todo {len(todo)} (done {len(done)})")
asyncio.run(main())
best = {}
for l in open(raw_path):
    rec = json.loads(l)
    if rec.get("probs"):
        best[rec["id"]] = rec
with open(PD / f"jev_{MODE}.jsonl", "w") as f:
    for rec in best.values():
        f.write(json.dumps(rec) + "\n")
print(f"jev_{MODE}: {len(best)}/{len(rows)} rows answered")
