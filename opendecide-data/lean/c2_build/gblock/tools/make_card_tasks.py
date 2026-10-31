"""Haiku AUTHORING tasks for G-block task cards (PREREG_FINAL A39 c). Per domain 3 tasks; each shows 12 sample texts
(opaque ids, no labels, no source ids) and asks for 2 task cards. Samples are drawn without replacement, seeded.
Writes cards/tasks/<domain>_<k>.json and cards/tasks_key.json (task -> text_ids; never shown to the agent).
Usage: python -I make_card_tasks.py"""
import hashlib
import json
import random
from pathlib import Path

G = Path("/Users/aryamahadik/Documents/jev/opendecide-data/lean/c2_build/gblock")
TASKS, ANSWERS = G / "cards" / "tasks", G / "cards" / "answers"
SEED, N_TASKS, N_SAMPLES = 20261013, 3, 12

DOMAINS = {
    "recipes": "home-cooking recipes from a community cookbook: a short description, an ingredient list and "
               "preparation steps",
    "travel": "passages from a community travel guide about places: what a place is like, how to get there and "
              "around, what to see and do, and how to stay safe",
    "news": "short news articles from a community news website, on all kinds of topics",
    "learning": "passages from community-written learning resources and course notes on many subjects",
    "gov_news": "news releases from a provincial government: announcements, programmes, funding, advisories and "
                "events",
    "office_help": "questions that people posted on a help forum for an office software suite (documents, "
                   "spreadsheets, presentations, databases)",
    "sci_abstracts": "abstracts of biology research preprints",
    "museum": "descriptions of artworks and objects, written for an art museum's collection website",
    "park_programs": "listings of programmes and activities offered at state parks (tours, classes, events)",
    "volunteer_posts": "volunteer opportunity postings from a county volunteer centre",
    "open_data": "descriptions of datasets published on government open-data portals",
}

ANGLES = {
    1: "handling: how someone would route, prioritise or act on a text like this",
    2: "fit: who or what a text like this is suitable for, or whether it meets a particular need",
    3: "content: what kind of thing the text describes, or what it asks of the reader (time, cost, effort, "
       "conditions)",
}

INSTRUCTIONS = """You are helping design decision tasks for a small text classifier.
The 12 example texts below are {desc}.
Write exactly 2 task cards: decisions that a business, an organisation or an ordinary person would really make about texts of this kind.
Angle for this task: {angle}.

Card 1 must be a yes/no question. Card 2 must be a choice question with 2 to 8 options (3 to 6 is best).

Rules for both cards:
1. A careful reader must be able to decide the answer from the text alone, with no outside knowledge.
2. The question must apply to most texts of this kind, not only to these 12 examples.
3. Use plain everyday words. No jargon and no academic terms.
4. Options must not overlap: for any text exactly one option fits best. If you need one, the last option may be a
   catch-all (for example "something else"), and its definition must say exactly when to pick it.
5. Give every option a one-sentence definition that says exactly when to pick it. For the yes/no card, define both
   "yes" and "no".
6. Balance: choose questions where each option is the right answer for a fair share of texts of this kind. For the
   yes/no card aim for roughly as many "yes" as "no". No option should fit nearly every text.
7. Do not copy label names or label sets from public datasets or benchmarks (for example positive/negative/neutral
   sentiment scales, entailment/contradiction, star ratings, standard emotion lists, standard news or topic category
   lists, or intent lists from chatbot datasets). Invent labels that fit the real decision.
8. Do not ask about anyone's identity, health or other personal traits, and do not ask for an opinion about a named
   person.
9. Do not label, summarise or quote the 12 example texts. Your output holds only the 2 cards.

Write ONE JSON object, and nothing else, to this exact file path:
{answer_path}

JSON shape:
{{"task_id": "{task_id}",
  "cards": [
    {{"kind": "yes/no",
      "who_decides": "one sentence: who makes this decision and why",
      "question": "the question, ending with a question mark",
      "options": [{{"label": "yes", "definition": "one sentence"}}, {{"label": "no", "definition": "one sentence"}}],
      "expected_share": {{"yes": 0.5, "no": 0.5}}}},
    {{"kind": "choice",
      "who_decides": "one sentence",
      "question": "the question, ending with a question mark",
      "options": [{{"label": "short label", "definition": "one sentence"}}, "... 2 to 8 options in total"],
      "expected_share": {{"<each label>": "your rough guess of the share of texts of this kind; shares sum to 1"}}}}
  ]}}

Labels are short (1 to 5 words), lower case unless a proper noun, and unique within a card. expected_share is your
rough guess for texts of this kind in general, not a count over these 12 examples.

Access rules: read only this task file; write only the answer file named above. Do not open any other file, do not
run programs, do not use the web."""


def main():
    TASKS.mkdir(parents=True, exist_ok=True)
    ANSWERS.mkdir(parents=True, exist_ok=True)
    key, made = {}, []
    tmpl_sha = hashlib.sha256(INSTRUCTIONS.encode()).hexdigest()
    for dom, desc in DOMAINS.items():
        f = G / "texts" / dom / "texts.jsonl"
        rows = [json.loads(l) for l in open(f) if l.strip()]
        rng = random.Random(f"{SEED}:{dom}")
        pick = rng.sample(rows, N_TASKS * N_SAMPLES)
        for k in range(1, N_TASKS + 1):
            tid = f"{dom}_{k}"
            sam = pick[(k - 1) * N_SAMPLES:k * N_SAMPLES]
            task_path = TASKS / f"{tid}.json"
            ans_path = ANSWERS / f"{tid}.json"
            task = {
                "task_id": tid,
                "kind": "gblock_card_authoring",
                "binding": "PREREG_FINAL.md Ruling A39 (c): Haiku 5.5 authors task cards only; it never sets a label",
                "answer_path": str(ans_path),
                "allowed_read": [str(task_path)],
                "allowed_write": [str(ans_path)],
                "domain": dom,
                "instructions": INSTRUCTIONS.format(desc=desc, angle=ANGLES[k], answer_path=ans_path, task_id=tid),
                "instructions_template_sha256": tmpl_sha,
                "samples": [{"sid": f"s{i + 1:02d}", "text": r["text"]} for i, r in enumerate(sam)],
            }
            task_path.write_text(json.dumps(task, ensure_ascii=False, indent=1))
            key[tid] = {"domain": dom, "angle": k, "sample_text_ids": [r["text_id"] for r in sam]}
            made.append({"task_file": str(task_path), "answer_file": str(ans_path), "domain": dom})
    (G / "cards" / "tasks_key.json").write_text(json.dumps({"seed": SEED, "instructions_template_sha256": tmpl_sha,
                                                            "tasks": key}, indent=1))
    print(json.dumps(made))


if __name__ == "__main__":
    main()
