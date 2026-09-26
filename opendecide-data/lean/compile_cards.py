"""Decision compiler: turn a label set into a TASK CARD once, with a big open model, so a small model can use it
at every request (big-model knowledge is paid per task, not per question).

Input to the compiler is ONLY the task description (input kind + instruction) and the label names: no dataset items,
no gold labels. Output per label: a one-sentence definition that separates it from the others + 2 short made-up
examples. Cards are cached in assets/cards/<task_key>.json and rendered by card_text().

  python compile_cards.py SPLIT [SPLIT ...]      # compiles every choice label set with >= MIN_N questions
"""
from __future__ import annotations

import hashlib
import json
import os
import re
import sys
from collections import defaultdict
from pathlib import Path

HERE = Path(__file__).resolve().parent
CARDS = HERE.parent / "assets/cards"
MODEL = "qwen/qwen3-235b-a22b-2507"
MIN_N = 20


def task_key(kind: str, labels: list[str]) -> str:
    return hashlib.sha1((kind + "|" + "|".join(sorted(labels))).encode()).hexdigest()[:12]


def input_kind(state: str) -> str:
    head = state.split("\n", 1)[0].strip()
    return head[:-1] if head.endswith(":") and len(head) < 40 else "text"


def card_text(card: dict) -> str:
    lines = []
    for lab in card["labels"]:
        e = card["cards"][lab]
        ex = " | ".join(f'"{x}"' for x in e["examples"][:2])
        lines.append(f"- {lab}: {e['definition']} Examples: {ex}")
    return "\n".join(lines)


def compile_card(kind: str, instruction: str, labels: list[str]) -> dict:
    import httpx
    key = task_key(kind, labels)
    path = CARDS / f"{key}.json"
    if path.exists():
        return json.loads(path.read_text())
    prompt = (f"You are compiling a decision task for a small, fast classifier.\n"
              f"Input kind: {kind}\nQuestion asked about each input: {instruction}\nLabels: {json.dumps(labels)}\n\n"
              "For EVERY label write (1) a one-sentence definition that makes clear how it differs from the other labels, "
              "including the typical borderline cases, and (2) two short, realistic, varied example inputs of this kind "
              "that clearly belong to that label. Answer with JSON only: "
              '{"<label>": {"definition": "...", "examples": ["...", "..."]}, ...} using the labels exactly as given.')
    for attempt in range(4):
        r = httpx.post("https://openrouter.ai/api/v1/chat/completions", timeout=120,
                       headers={"Authorization": f"Bearer {os.environ['OPENROUTER_API_KEY']}"},
                       json={"model": MODEL, "temperature": 0.2, "max_tokens": 2500,
                             "messages": [{"role": "user", "content": prompt}]})
        txt = r.json()["choices"][0]["message"]["content"]
        m = re.search(r"\{.*\}", txt, re.S)
        try:
            d = json.loads(m.group(0))
            if all(l in d and d[l].get("definition") and len(d[l].get("examples", [])) >= 2 for l in labels):
                card = {"key": key, "kind": kind, "instruction": instruction, "labels": labels, "model": MODEL,
                        "cards": {l: {"definition": d[l]["definition"].strip(), "examples": [x.strip() for x in d[l]["examples"][:2]]}
                                  for l in labels}}
                CARDS.mkdir(parents=True, exist_ok=True)
                path.write_text(json.dumps(card, indent=1))
                return card
        except Exception:  # noqa: BLE001
            pass
    raise RuntimeError(f"could not compile card for {kind} {labels}")


def tasks_in(rows):
    """Label sets that recur (>= MIN_N choice questions): kind + sorted labels -> (instruction, labels, sources)."""
    by = defaultdict(list)
    for r in rows:
        if r["qtype"] == "choice":
            by[(input_kind(r["state"]), tuple(sorted(r["options"])))].append(r)
    return {k: v for k, v in by.items() if len(v) >= MIN_N}


def attach(rows):
    """Add row['card'] (rendered text) to every row whose source has a compiled recurring label set."""
    src_card = {}
    for (kind, labs), rs in tasks_in(rows).items():
        card = compile_card(kind, rs[0]["instructions"], [o for o in rs[0]["options"]])
        for r in rs:
            src_card[r["source"]] = card_text(card)
    out = []
    for r in rows:
        out.append({**r, "card": src_card[r["source"]]} if r["source"] in src_card else r)
    return out, len(src_card)


if __name__ == "__main__":
    for envf in (HERE.parent / ".env",):
        for line in envf.read_text().splitlines():
            if "=" in line:
                k, v = line.split("=", 1)
                os.environ.setdefault(k.strip(), v.strip())
    for split in sys.argv[1:]:
        rows = [json.loads(l) for l in open(HERE / f"data/{split}.jsonl")]
        out, n = attach(rows)
        with open(HERE / f"data/{split}_card.jsonl", "w") as f:
            for r in out:
                f.write(json.dumps(r) + "\n")
        rel = HERE / f"data/{split}_relations.jsonl"
        if rel.exists():
            (HERE / f"data/{split}_card_relations.jsonl").write_text(rel.read_text())
        print(f"{split}: {n} sources carded, {sum('card' in r for r in out)}/{len(out)} rows")
