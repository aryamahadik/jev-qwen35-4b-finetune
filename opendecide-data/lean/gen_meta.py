"""Diverse data for the meta-claim check used by leverage-bounded decoding (open teacher, never Jev, never benchmark text).
  positives: messages planted in a document to dictate the decision; '{T}' marks the pushed answer
  hard negatives: rule / fact / history sentences that MENTION outcomes but do not dictate this case's answer
Held-out attack wording (jagged audit, our eval families) is banned and asserted.
Writes data/meta_pos.jsonl, data/meta_neg.jsonl.   python gen_meta.py [calls_per_side]
"""
import asyncio
import json
import random
import re
import sys
from pathlib import Path

import httpx

from build_inj_v2 import BANNED
from gen_lah import DOMAINS, MODEL, call

HERE = Path(__file__).resolve().parent
POS = """Write 20 different short texts (1-3 sentences each) that someone could plant inside a {dom} case file, email thread,
tool output, log or form field to make an automated decision system output a particular answer instead of deciding
from the evidence. Vary the style widely: fake system/audit notes, claimed prior rulings, managers' instructions,
"auto-classifier" outputs, JSON-like fields, footers, forwarded replies, polite requests, urgent threats, other
languages (a few). Write the pushed answer as the literal placeholder {{T}} (it may appear once or twice).
Do not use these phrases: closing administrator, ignore the discussion above, has confirmed this article, annotation
team, QA reviewer, only sensible reading, really about, relabel.
Return ONLY a JSON list of 20 strings."""
NEG = """Write 20 different sentences or short paragraphs that could appear in a legitimate {dom} document and that MENTION
decisions, outcomes, approvals, labels or answers, but do NOT tell the reader how to decide the current case. Mix:
rules with conditions ("claims are approved only if ..."), past outcomes of other cases, statistics about outcomes,
definitions of outcome categories, procedural steps, deadlines, facts about the current case (dates, amounts, what
happened), and quotes of a policy. Invented names and numbers.
Return ONLY a JSON list of 20 strings."""


async def main(n):
    import os
    for line in (HERE.parent / ".env").read_text().splitlines():
        if "=" in line:
            k, v = line.split("=", 1)
            os.environ.setdefault(k.strip(), v.strip())
    rng = random.Random(7)
    spent = {"usd": 0.0}
    sem = asyncio.Semaphore(8)

    async def one(kind, i):
        dom = DOMAINS[i % len(DOMAINS)]
        async with sem:
            txt = await call(client, (POS if kind == "pos" else NEG).format(dom=dom), 2600, spent, 0.5)
        try:
            items = json.loads(re.search(r"\[.*\]", txt, re.S).group(0))
            return [(kind, dom, str(x).strip()) for x in items if isinstance(x, str) and 10 < len(x) < 600]
        except Exception:
            return []

    async with httpx.AsyncClient(headers={"Authorization": f"Bearer {os.environ['OPENROUTER_API_KEY']}"}) as client:
        res = await asyncio.gather(*[one(k, i) for k in ("pos", "neg") for i in range(n)])
    flat = [x for r in res for x in r]
    pos = [{"text": t, "domain": d} for k, d, t in flat if k == "pos" and "{T}" in t and not BANNED.search(t)]
    neg = [{"text": t, "domain": d} for k, d, t in flat if k == "neg" and "{T}" not in t and not BANNED.search(t)]
    rng.shuffle(pos)
    rng.shuffle(neg)
    (HERE / "data/meta_pos.jsonl").write_text("".join(json.dumps(x) + "\n" for x in pos))
    (HERE / "data/meta_neg.jsonl").write_text("".join(json.dumps(x) + "\n" for x in neg))
    print(json.dumps({"pos": len(pos), "neg": len(neg), "est_usd": round(spent["usd"], 3)}))


if __name__ == "__main__":
    asyncio.run(main(int(sys.argv[1]) if len(sys.argv) > 1 else 80))
