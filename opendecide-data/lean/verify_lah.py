"""Second, independent verifier for LLM-authored items (different model family than the author/first verifier).
Keeps a row only if the second verifier's blind answer equals the stored gold. Rewrites data/lah_train.jsonl
(the unfiltered file is kept as data/lah_train_unverified.jsonl) and logs agreement per family.
  python verify_lah.py [--cap-usd 0.6]
"""
import asyncio
import json
import os
import random
import re
import sys
from collections import Counter
from pathlib import Path

import httpx

HERE = Path(__file__).resolve().parent
for line in (HERE.parent / ".env").read_text().splitlines():
    if "=" in line:
        k, v = line.split("=", 1)
        os.environ.setdefault(k.strip(), v.strip())
MODEL = "openai/gpt-oss-120b"
PRICE_IN, PRICE_OUT = 0.15e-6, 0.75e-6  # conservative upper bounds
PROMPT = """{state}

Question: {question}
Options:
{opts}

Choose the single best option using only the text. Reply with JSON on the last line: {{"answer": "<letter>"}}"""


async def main(cap):
    src = HERE / "data/lah_train.jsonl"
    keep_all = HERE / "data/lah_train_unverified.jsonl"
    if not keep_all.exists():
        keep_all.write_text(src.read_text())
    rows = [json.loads(l) for l in open(keep_all)]
    spent = {"usd": 0.0}
    sem = asyncio.Semaphore(16)
    L = "ABCDEFGH"

    async def one(client, r, rng):
        opts = list(r["options"])
        rng.shuffle(opts)
        desc = dict(l[2:].split(": ", 1) for l in r["card"].splitlines() if ": " in l)
        shown = "\n".join(f"{L[i]}. {o}: {desc.get(o, '')}" for i, o in enumerate(opts))
        if spent["usd"] >= cap:
            return None
        async with sem:
            for attempt in range(3):
                try:
                    res = await client.post("https://openrouter.ai/api/v1/chat/completions", timeout=180, json={
                        "model": MODEL, "max_tokens": 3000, "temperature": 0.0, "reasoning": {"effort": "low"},
                        "provider": {"sort": "price"},
                        "messages": [{"role": "user", "content": PROMPT.format(state=r["state"], question=r["instructions"], opts=shown)}]})
                    d = res.json()
                    u = d.get("usage") or {}
                    spent["usd"] += u.get("prompt_tokens", 0) * PRICE_IN + u.get("completion_tokens", 0) * PRICE_OUT
                    txt = d["choices"][0]["message"]["content"] or ""
                    a = json.loads(re.findall(r"\{[^{}]*\"answer\"[^{}]*\}", txt)[-1])["answer"].strip()[:1]
                    return opts[L.index(a)] if a in L[:len(opts)] else "?"
                except Exception:
                    await asyncio.sleep(2 ** attempt)
        return None

    rng = random.Random(5)
    async with httpx.AsyncClient(headers={"Authorization": f"Bearer {os.environ['OPENROUTER_API_KEY']}"}) as client:
        ans = await asyncio.gather(*[one(client, r, random.Random(rng.random())) for r in rows])
    kept = [r for r, a in zip(rows, ans) if a == r["gold"]]
    fam = Counter(r["meta"]["family"] for r in rows)
    famk = Counter(r["meta"]["family"] for r in kept)
    src.write_text("".join(json.dumps(r) + "\n" for r in kept))
    log = {"verifier": MODEL, "rows": len(rows), "kept": len(kept), "no_answer": sum(a is None for a in ans),
           "est_usd": round(spent["usd"], 3), "agree_by_family": {f: f"{famk[f]}/{n}" for f, n in fam.items()}}
    (HERE / "logs/lah_verify2.json").write_text(json.dumps(log, indent=1))
    print(json.dumps(log, indent=1))


if __name__ == "__main__":
    asyncio.run(main(float(sys.argv[sys.argv.index("--cap-usd") + 1]) if "--cap-usd" in sys.argv else 0.6))
