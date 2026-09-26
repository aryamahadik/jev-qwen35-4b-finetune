"""LLM-authored hard decision items (open teacher, verified by a blind re-solve; never Jev, never JevBench text).

Author: qwen/qwen3-235b-a22b-2507 writes a self-contained hard decision item (state + question + options with
descriptions + intended answer), from a FAMILY DESCRIPTION and a DOMAIN only. Verifier: the same model solves the item
blind (brief reasoning, then JSON answer). Only items where both agree are kept. Hard spending cap via token counting.
Writes data/lah_train.jsonl (rows in the project schema) and logs/lah_log.json.
  python gen_lah.py N [--cap-usd 2.0]
"""
import asyncio
import json
import os
import random
import re
import sys
from pathlib import Path

import httpx

HERE = Path(__file__).resolve().parent
for line in (HERE.parent / ".env").read_text().splitlines():
    if "=" in line:
        k, v = line.split("=", 1)
        os.environ.setdefault(k.strip(), v.strip())
MODEL = "qwen/qwen3-235b-a22b-2507"
PRICE_IN, PRICE_OUT = 0.35e-6, 1.0e-6  # conservative upper bounds per token (list prices vary by provider)
FAMILIES = {
    "long_policy": "a long policy/contract/benefit document with numbered sections, definitions of similar terms, exclusions, exceptions to exceptions, and an amendment/endorsement with an effective date that changes the outcome only for some cases; plus a case file; the question asks for the single authorized outcome",
    "multi_hop": "several records/documents/tables that must be chained through IDs, aliases and version history (only the current version controls, some records are superseded); near-identical distractor IDs; the question asks for the operative outcome for one entity",
    "temporal_numeric": "a decision that requires exact date/time/duration or arithmetic reasoning (inclusive/exclusive deadlines, business days with holidays, time zones, corrections before comparing to a threshold, caps, pro-rata amounts, units); options are bands or amounts, wrong ones come from specific mistakes",
    "trap": "a case where a prominent surface cue, a junior colleague's note, or an outdated instruction points to a wrong answer, but careful reading of the controlling rule gives a different one",
    "adversarial": "a case file that contains an embedded message or note from an unauthorized party trying to steer the decision (e.g. claiming it was already decided or telling the reader what to answer); the correct answer follows the actual rules and evidence",
    "ambiguous": "a case where the stated rules and facts do NOT determine the outcome (a required fact is missing or two rules conflict without a precedence rule); one option says the outcome cannot be determined from the information given and it is correct; other options look plausible",
    "routing": "a request plus a catalog of tools/teams/APIs with capabilities and constraints (permissions, data residency, business hours, cost limits, deprecations); exactly one option satisfies every constraint, each distractor violates exactly one",
    "tradeoff": "choosing between 3-4 alternatives under explicit weighted criteria or hard constraints stated in the state; the best alternative is determined by applying the stated rule exactly",
    "rubric": "an ordinal scoring question: a rubric with levels (e.g. 0-3 or 0-4) defined by criteria and a rule like 'use the highest level fully supported'; facts support some criteria; options are the levels",
    "evidence": "a forecast question (will X happen / most likely cause) where stated base rates and evidence reliabilities make one outcome clearly most likely, but a vivid anecdote in the state points elsewhere",
}
DOMAINS = ["property insurance claims", "employee leave and benefits", "consumer lending and payment relief", "cross-border shipping and customs",
           "hospital medication scheduling", "SaaS incident management", "university admissions and appeals", "corporate travel expenses",
           "retail returns and warranties", "data privacy requests", "manufacturing quality control", "public housing benefits",
           "airline disruptions and rebooking", "telecom billing disputes", "grant funding compliance", "clinical trial eligibility",
           "municipal permits", "bank card disputes and chargebacks", "freight carrier contracts", "cybersecurity alert triage"]
AUTHOR = """Write ONE hard test item for a fast decision model (it must answer from the text alone, without step-by-step writing).
Family: {fam}
Domain: {dom}
Requirements:
- A self-contained "state" of {words} words (sections, records, emails or notes as fits the domain; invented names, IDs, dates, amounts).
- One question and {k} options. Each option has a short snake_case id and a one-sentence description.
- Exactly ONE option is correct, unambiguously, for a careful reader. Every wrong option matches a specific plausible mistake.
- The difficulty must come from careful reading/applying rules, not from trivia or outside knowledge.
Return ONLY JSON: {{"state": "...", "question": "...", "options": {{"id": "description", ...}}, "answer": "id", "mistakes": {{"wrong_id": "mistake name"}}}}"""
VERIFY = """{state}

Question: {question}
Options:
{opts}

Think briefly (at most 150 words), then give your final answer on the last line as JSON: {{"answer": "<option id>"}}"""


def parse_json(txt):
    m = re.search(r"\{.*\}", txt, re.S)
    return json.loads(m.group(0)) if m else None


async def call(client, prompt, max_tokens, spent, cap):
    if spent["usd"] >= cap:
        return None
    for attempt in range(3):
        try:
            r = await client.post("https://openrouter.ai/api/v1/chat/completions", timeout=180,
                                  json={"model": MODEL, "temperature": 0.7 if "ONE hard" in prompt else 0.0, "max_tokens": max_tokens,
                                        "provider": {"sort": "price"}, "messages": [{"role": "user", "content": prompt}]})
            d = r.json()
            u = d.get("usage") or {}
            spent["usd"] += u.get("prompt_tokens", 0) * PRICE_IN + u.get("completion_tokens", 0) * PRICE_OUT
            return d["choices"][0]["message"]["content"]
        except Exception:
            await asyncio.sleep(2 ** attempt)
    return None


async def one(client, i, sem, spent, cap, rng):
    fam = list(FAMILIES)[i % len(FAMILIES)]
    dom, words, k = rng.choice(DOMAINS), rng.choice([250, 450, 700, 1000]), rng.choice([2, 3, 4, 4, 5])
    if fam == "rubric":
        k = rng.choice([4, 5])
    async with sem:
        a = await call(client, AUTHOR.format(fam=FAMILIES[fam], dom=dom, words=words, k=k), 2600, spent, cap)
        try:
            item = parse_json(a)
            opts = item["options"]
            assert isinstance(opts, dict) and item["answer"] in opts and 2 <= len(opts) <= 6 and len(item["state"]) > 300
        except Exception:
            return None
        letters = "ABCDEF"
        keys = list(opts)
        rng.shuffle(keys)
        shown = "\n".join(f"{letters[j]}. {kk}: {opts[kk]}" for j, kk in enumerate(keys))
        v = await call(client, VERIFY.format(state=item["state"], question=item["question"], opts=shown), 700, spent, cap)
        try:
            vans = json.loads(re.findall(r"\{[^{}]*\"answer\"[^{}]*\}", v)[-1])["answer"].strip()
            vans = keys[letters.index(vans)] if vans in letters[:len(keys)] else vans
        except Exception:
            return {"_disagree": True}
        if vans != item["answer"]:
            return {"_disagree": True}
    return {"id": f"r_lah_{i}", "group_id": f"g:lah:{i}", "call_id": f"c_lah_{i}", "split": "train", "track": "LAH", "source": f"lah_{fam}",
            "state": item["state"], "qtype": "choice", "instructions": item["question"], "options": keys, "gold": item["answer"],
            "role": "choice", "card": "\n".join(f"- {kk}: {opts[kk]}" for kk in keys),
            "meta": {"family": fam, "domain": dom, "mistakes": item.get("mistakes"), "anchor": False, "teacher": MODEL}}


async def main(n, cap):
    rng = random.Random(20260926)
    spent = {"usd": 0.0}
    sem = asyncio.Semaphore(16)
    async with httpx.AsyncClient(headers={"Authorization": f"Bearer {os.environ['OPENROUTER_API_KEY']}"}) as client:
        res = await asyncio.gather(*(one(client, i, sem, spent, cap, random.Random(rng.random())) for i in range(n)))
    kept = [r for r in res if r and not r.get("_disagree")]
    dis = sum(1 for r in res if r and r.get("_disagree"))
    (HERE / "data/lah_train.jsonl").write_text("".join(json.dumps(r) + "\n" for r in kept))
    log = {"requested": n, "kept": len(kept), "verifier_disagreed": dis, "failed": n - len(kept) - dis, "est_usd": round(spent["usd"], 3)}
    (HERE / "logs/lah_log.json").write_text(json.dumps(log, indent=1))
    print(json.dumps(log))


if __name__ == "__main__":
    cap = float(sys.argv[sys.argv.index("--cap-usd") + 1]) if "--cap-usd" in sys.argv else 2.0
    asyncio.run(main(int(sys.argv[1]), cap))
