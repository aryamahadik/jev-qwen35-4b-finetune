"""Item 10 stages 1-3: error slices, Haiku card authoring, lint, G-LEX reads, admission.

  slices     the G-block C1 read -> where C1 is uncertain and wrong -> authoring tasks per domain (counts only, no text)
  author     Haiku authoring task files (3 choice cards per task). Slice A = intent / topic boundary pairs (Haiku-labelled
             later); slice B = emotion and political taxonomies (Opus-labelled only, since Haiku is no better than C1 there)
  lint       collect answers, lint (gcards.lint_card + the I10 extras), dedup among cards and against the 41 GB cards
  extract    two independent Haiku restatement reads (rA, rB) of the surviving cards (A39 c: G-LEX-style 2/2)
  compare    program checks (admit_cards.check_card) and the review sheet for the first pass
  admit      cards/admission/review.json -> cards/admitted.jsonl (any doubt rejects; hard program failures never admit)

Nothing here sets a label. Haiku only writes cards and restates options; the readers' restatements and examples are checked
and never used as labels or training data.
"""
from __future__ import annotations

import hashlib
import hmac
import json
import math
import random
import re
import sys
from collections import Counter, defaultdict
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import i10_lib as L  # noqa: E402
from i10_lib import kp  # noqa: E402

import gcards  # noqa: E402  (gblock/tools: pure lint_card, toks, jacc, PROMPT)
import admit_cards as AC  # noqa: E402  (check_card, Tfidf)
import make_card_tasks as MCT  # noqa: E402  (DOMAINS: the A39 source descriptions)

DOMAINS = MCT.DOMAINS

# ---------------------------------------------------------------------------------------------------- slices and allocation
A_TASKS_TOTAL = 33          # slice A authoring tasks (3 cards each) over the 11 domains, at least 2 per domain
A_TASKS_MIN = 2
B_TASKS = [                 # slice B (Opus-only labels): (domain, topic). Emotion and political taxonomies on texts that carry them
    ("news", "emotion"), ("news", "political"), ("gov_news", "political"), ("office_help", "emotion"),
    ("museum", "emotion"), ("travel", "emotion"), ("volunteer_posts", "emotion"), ("open_data", "political"),
]
_NEAR = ", where neighbouring answers are easy to confuse"
A_ANGLES = {
    "recipes": [
        "dish type: what kind of dish the recipe makes" + _NEAR,
        "cooking method: the main way the food is cooked or put together" + _NEAR,
        "occasion: the setting or meal the dish is best suited to" + _NEAR,
        "effort: how much work, time or skill the recipe asks of the cook" + _NEAR,
        "dietary fit: who could eat the dish, judged only from the ingredients and steps" + _NEAR,
        "main ingredient role: what the central ingredient of the dish is" + _NEAR,
    ],
    "travel": [
        "section: which section of a travel guide the passage belongs in" + _NEAR,
        "traveller need: which need of a traveller the passage meets" + _NEAR,
        "kind of advice: what sort of information or advice the passage gives" + _NEAR,
        "kind of place: what sort of place or setting the passage describes" + _NEAR,
        "effort or risk: how demanding or risky the thing described is for a visitor" + _NEAR,
        "timing: when in a trip or a year the passage matters to a visitor" + _NEAR,
    ],
    "news": [
        "story type: what kind of event or development the story reports" + _NEAR,
        "subject area: which area of public life the story is mainly about" + _NEAR,
        "reader stake: what a reader of the story stands to gain, lose or need to do" + _NEAR,
        "story stage: where the story stands (first report, new development, result, aftermath)" + _NEAR,
        "news value: why the story is worth printing" + _NEAR,
        "sourcing: what the story mainly rests on (an official statement, a document, an eyewitness, a count of something)" + _NEAR,
    ],
    "learning": [
        "topic: which sub-area of the subject the text is about" + _NEAR,
        "learning purpose: what the text is meant to help a learner do" + _NEAR,
        "material type: what sort of study material this passage is" + _NEAR,
        "level: how much the passage assumes the learner already knows" + _NEAR,
        "learner action: what the passage asks the learner to do next" + _NEAR,
        "course role: what job the passage does inside a course" + _NEAR,
    ],
    "gov_news": [
        "purpose: what the release is trying to get done" + _NEAR,
        "audience: which readers the release is mainly written for" + _NEAR,
        "kind of announcement: what sort of announcement it is" + _NEAR,
        "what changes: what the release says is new, different or ending" + _NEAR,
        "urgency: how soon a reader needs to act or take notice" + _NEAR,
        "money or rule: whether the release is mainly about money, a rule, a service or an event" + _NEAR,
    ],
    "office_help": [
        "request: what the poster wants from a helper" + _NEAR,
        "problem type: what kind of problem the poster describes" + _NEAR,
        "program area: which part of the office software the post is about" + _NEAR,
        "symptom: how the problem shows itself to the poster" + _NEAR,
        "answer needed: what kind of answer would settle the post" + _NEAR,
        "stage: how far the poster has already got (nothing tried, tried some fixes, found a partial answer)" + _NEAR,
    ],
    "sci_abstracts": [
        "kind of study: what sort of study the abstract reports" + _NEAR,
        "subject: what the study is mainly about" + _NEAR,
        "kind of finding: what sort of result the abstract reports" + _NEAR,
        "method: the main way the authors got their result" + _NEAR,
        "claim strength: how firmly the abstract states its result" + _NEAR,
        "use: who could use the result, and for what" + _NEAR,
    ],
    "museum": [
        "kind of object: what sort of object the description is about" + _NEAR,
        "description focus: what the description spends most of its words on (looks, maker, history, use, meaning)" + _NEAR,
        "subject shown: what the object shows or represents" + _NEAR,
        "material or technique: how the object was made" + _NEAR,
        "visitor use: what a visitor would use the description for" + _NEAR,
        "curator task: what job a museum team would give the description (catalogue, label, story, loan file)" + _NEAR,
    ],
    "park_programs": [
        "kind of activity: what sort of activity the listing offers" + _NEAR,
        "fit: which visitors the program suits" + _NEAR,
        "effort: how physically demanding the program is" + _NEAR,
        "visit conditions: what a visitor must arrange or bring before taking part" + _NEAR,
        "setting: where and in what surroundings the program takes place" + _NEAR,
        "purpose: what a visitor is meant to get out of the program" + _NEAR,
    ],
    "volunteer_posts": [
        "kind of work: what sort of work the volunteer would do" + _NEAR,
        "skills: what the volunteer needs to bring" + _NEAR,
        "commitment: how much time and regularity the posting asks for" + _NEAR,
        "setting: where and in what conditions the work happens" + _NEAR,
        "who benefits: whom the volunteer work helps directly" + _NEAR,
        "match: which kind of person the posting suits best" + _NEAR,
    ],
    "open_data": [
        "kind of dataset: what sort of records the dataset holds" + _NEAR,
        "subject area: which area of public life the dataset is about" + _NEAR,
        "intended use: what a person would use the dataset for" + _NEAR,
        "detail level: what one record in the dataset stands for" + _NEAR,
        "freshness: how current, complete or final the data are said to be" + _NEAR,
        "first look: which kind of team should look at the dataset first" + _NEAR,
    ],
}
B_ANGLES = {
    "emotion": [
        "writer's feeling: the feeling the writer shows or describes",
        "reader's feeling: the feeling a typical reader would most likely have after reading the text",
        "overall mood: the mood or tone the text gives off as a whole, apart from any one sentence",
    ],
    "political": [
        "kind of public matter: what sort of public or political matter the text is about",
        "framing: how the text presents a decision, measure or event (for example as a cost, a benefit, a dispute, a routine step)",
        "part of public life: which part of public life or which level of decision-making the matter touches",
    ],
}
FOCUS_A = ("SLICE: boundary pairs. The cards are about intent or topic where neighbouring answers are easy to confuse, like the "
           "hard choices in a help-desk or routing system. Build every card so that its options are near neighbours.")
FOCUS_B = {
    "emotion": ("SLICE: feeling and tone. Invent your own 5 to 8 feeling or mood labels that suit this kind of text. Spell out the "
                "dividing line between similar feelings by what the text says or does. The last option must be a catch-all for "
                "texts with no clear feeling. Do not use any ready-made emotion list (not the usual handful of basic emotions, "
                "not a positive / negative / neutral scale, not a list of dozens of emotions)."),
    "political": ("SLICE: public affairs. The cards are about what kind of public or political matter a text is about, or how the "
                  "text presents a decision or measure. Invent your own labels. Do not use left / right / centre or party "
                  "scales, do not ask about any person's party, beliefs or character, and do not ask whether a named person "
                  "or group is good or bad. The cards are about the text, not about people. A card must be answerable "
                  "without knowing who any person or party is."),
}

AUTHOR_INSTRUCTIONS = """You are helping design decision tasks for a small text classifier.
The {n} example texts below are {desc}.
Write exactly 3 task cards. Every card is a CHOICE question with 4 to 8 options (5 or 6 is best).
{focus}
Card 1 angle: {a1}.
Card 2 angle: {a2}.
Card 3 angle: {a3}.
The three cards must ask three different decisions, not three wordings of one decision.

Rules for all three cards:
1. A careful reader must be able to decide the answer from the text alone, with no outside knowledge.
2. The question must apply to most texts of this kind, not only to these {n} examples.
3. Use plain everyday words. No jargon and no academic terms.
4. Options must not overlap: for any text exactly one option fits best. The last option may be a catch-all (for example
   "something else"), and its definition must say exactly when to pick it.
5. Give every option a one-sentence definition that says exactly when to pick it.
6. Boundary rule, the heart of this task: build the options as near neighbours. At least two pairs of options must be easy to
   confuse for a hurried reader. For every such pair, the two definitions must state the dividing line: what the text must say
   or do to belong to the first option and not to the second.
7. Balance: choose questions where each option is the right answer for a fair share of texts of this kind. No option should
   fit more than half of the texts.
8. Do not copy label names or label sets from public datasets or benchmarks (for example positive/negative/neutral sentiment
   scales, entailment/contradiction, star ratings, standard emotion lists, standard news or topic category lists, or intent
   lists from chatbot or banking datasets). Invent labels that fit the real decision.
9. Do not ask about anyone's identity, health or other personal traits, and do not ask for an opinion about a named person.
10. Do not label, summarise or quote the example texts. Your output holds only the 3 cards.

Labels are short (1 to 5 words), lower case unless a proper noun, and unique within a card. expected_share is your rough guess
for texts of this kind in general, not a count over the examples; the shares of a card sum to 1."""

AUTHOR_CONTRACT = """Write ONE JSON object, and nothing else (no text before or after it), to the answer file named at the top.

{{"task_id": "{task_id}",
  "cards": [
    {{"kind": "choice",
      "who_decides": "one sentence: who makes this decision and why",
      "question": "the question, ending with a question mark",
      "options": [{{"label": "short label", "definition": "one sentence"}}, "... 4 to 8 options in total"],
      "expected_share": {{"<each label>": 0.2}}}},
    "... exactly 3 cards in total"
  ]}}

The items below are read-only context (the example texts). Your answer holds exactly 3 cards."""


def compute_slices() -> dict:
    """Counts of where C1 is uncertain (top < 0.75 or margin < 0.3) and wrong on the labelled G-block rows, per domain and
    kind. Counts only: no row text. Wrong = C1 argmax differs from the kept label (haiku_accepted or opus_kept rows)."""
    cl = L.read_jsonl(L.GB / "route_a42d" / "classes.jsonl")
    pr = {}
    for r in L.read_jsonl(L.LEAN / "preds_gblock_a42d_c1read" / f"{L.C1}.jsonl"):
        pr[r["id"]] = r["probs"]
    by = defaultdict(Counter)
    for r in cl:
        p = sorted(pr[r["id"]].values(), reverse=True)
        unc = p[0] < L.UNC_TOP or (p[0] - p[1]) < L.UNC_MARGIN
        kept = r["status"] in ("haiku_accepted", "opus_kept")
        wrong = kept and r["c1_argmax"] != r["label"]
        for key in (r["domain"], f"{r['domain']}|{r['qtype']}"):
            c = by[key]
            c["rows"] += 1
            c["uncertain"] += unc
            c["labelled"] += kept
            c["c1_wrong"] += wrong
            c["uncertain_and_wrong"] += unc and wrong
    return {k: dict(v) for k, v in by.items()}


def allocate(weights: dict, total: int, minimum: int) -> dict:
    """Largest-remainder split of `total` over the keys by weight, each at least `minimum` (taken from the largest first)."""
    keys = sorted(weights)
    w = {k: max(weights[k], 0) for k in keys}
    s = sum(w.values()) or 1
    raw = {k: total * w[k] / s for k in keys}
    out = {k: max(minimum, int(math.floor(raw[k]))) for k in keys}
    guard = 0
    while sum(out.values()) != total and guard < 10000:
        guard += 1
        if sum(out.values()) < total:
            k = max(keys, key=lambda x: (raw[x] - out[x], x))
            out[k] += 1
        else:
            k = max((x for x in keys if out[x] > minimum), key=lambda x: (out[x] - raw[x], x))
            out[k] -= 1
    return out


def cmd_slices() -> dict:
    sl = compute_slices()
    doms = sorted(d for d in sl if "|" not in d)
    weights = {d: sl[d]["uncertain_and_wrong"] for d in doms}
    alloc = allocate(weights, A_TASKS_TOTAL, A_TASKS_MIN)
    rec = {"source": "gblock/route_a42d/classes.jsonl + preds_gblock_a42d_c1read (C1 output is a routing signal only)",
           "rule": (f"uncertain = top probability < {L.UNC_TOP} or margin < {L.UNC_MARGIN}; wrong = C1 argmax != kept label; "
                    f"slice A tasks per domain = largest remainder of {A_TASKS_TOTAL} by (uncertain and wrong) rows, at least {A_TASKS_MIN}"),
           "counts": sl, "weights_uncertain_and_wrong": weights, "slice_a_tasks_per_domain": alloc,
           "slice_b_tasks": [list(x) for x in B_TASKS],
           "kind_note": "choice rows are 2-3x more often uncertain than yes/no rows, so every I10 card is a choice card"}
    L.write_json(L.SLICES, rec)
    L.set_state("slices", slice_a_tasks=sum(alloc.values()), slice_b_tasks=len(B_TASKS))
    return rec


# ---------------------------------------------------------------------------------------------------- authoring tasks
def task_catalog(alloc: dict) -> list:
    cat = []
    for d in sorted(alloc):
        for k in range(1, alloc[d] + 1):
            la = A_ANGLES[d]
            ang = [la[(k - 1 + 2 * j) % len(la)] for j in range(3)]
            cat.append({"task_id": f"i10a_{d}_{k}", "slice": "A", "domain": d, "topic": "boundary", "angles": ang})
    seen = Counter()
    for d, topic in B_TASKS:
        seen[(d, topic)] += 1
        cat.append({"task_id": f"i10b_{d}_{topic}_{seen[(d, topic)]}", "slice": "B", "domain": d, "topic": topic,
                    "angles": list(B_ANGLES[topic])})
    return cat


def author_task_text(t: dict, samples: list, answer_path: str) -> str:
    focus = FOCUS_A if t["slice"] == "A" else FOCUS_B[t["topic"]]
    ins = AUTHOR_INSTRUCTIONS.format(n=len(samples), desc=DOMAINS[t["domain"]], focus=focus, a1=t["angles"][0],
                                     a2=t["angles"][1], a3=t["angles"][2])
    return L.task_md("Item 10 card authoring", t["task_id"], answer_path, ins,
                     AUTHOR_CONTRACT.format(task_id=t["task_id"]), samples, 3, items_label="Example texts",
                     n_items=len(samples), items_note="JSON; read-only context, not items to answer")


def cmd_author() -> list:
    rec = L.read_json(L.SLICES)
    cat = task_catalog(rec["slice_a_tasks_per_domain"])
    # 12 sample texts per task, seeded, distinct inside a domain until the domain runs out; the texts the A39 authors saw are
    # not reused (they are the same pool, but a card is never tested on the texts it was written from, see cands)
    used = defaultdict(set)
    out, key = [], {}
    for t in cat:
        d = t["domain"]
        texts = L.read_jsonl(L.GB / "texts" / d / "texts.jsonl")
        rng = random.Random(f"{L.SEED}|i10|author|{t['task_id']}")
        pool = [x for x in texts if x["text_id"] not in used[d]]
        if len(pool) < L.SAMPLES_PER_TASK:
            used[d] = set()
            pool = list(texts)
        pick = rng.sample(pool, L.SAMPLES_PER_TASK)
        used[d] |= {x["text_id"] for x in pick}
        samples = [{"sid": f"s{i + 1:02d}", "text": x["text"]} for i, x in enumerate(pick)]
        tf, af = L.AUTH_T / f"{t['task_id']}.md", L.AUTH_A / f"{t['task_id']}.json"
        L.write_text(tf, author_task_text(t, samples, str(af)))
        key[t["task_id"]] = {**t, "sample_text_ids": [x["text_id"] for x in pick]}
        out.append(L.task_record(tf, af, "haiku"))
    L.AUTH_A.mkdir(parents=True, exist_ok=True)
    L.write_json(L.CARDS / "author_tasks_manifest.json",
                 {"n_tasks": len(out), "tasks": [{**o, "sha256": L.sha_file(o["task_file"])} for o in out]})
    tmpl = L.sha_text(AUTHOR_INSTRUCTIONS)
    L.write_json(L.CARDS / "author_key.json", {"seed": L.SEED, "instructions_template_sha256": tmpl, "tasks": key})
    L.set_state("author", n_tasks=len(out), author_instructions_sha256=tmpl)
    return out


# ---------------------------------------------------------------------------------------------------- lint
DENY_EMOTION = {"joy", "joyful", "sadness", "sad", "anger", "angry", "fear", "afraid", "surprise", "surprised", "disgust",
                "disgusted", "love", "happy", "happiness", "trust", "anticipation", "neutral", "positive", "negative",
                "optimism", "pessimism", "admiration", "amusement", "annoyance", "approval", "caring", "confusion",
                "curiosity", "desire", "disappointment", "disapproval", "embarrassment", "excitement", "gratitude", "grief",
                "nervousness", "pride", "realization", "relief", "remorse"}
DENY_POLITICAL = {"left", "right", "centre", "center", "liberal", "conservative", "libertarian", "progressive", "left wing",
                  "right wing", "far left", "far right", "democrat", "republican", "socialist", "populist"}
SHARE_SUM_TOL, SHARE_MAX = 0.10, 0.60


def lint_i10(card: dict) -> tuple:
    """(reasons, details): gcards.lint_card plus the I10 rules. An empty reasons list passes."""
    fails, det = gcards.lint_card(card)
    fails = list(fails)
    if card.get("kind") != "choice":
        fails.append("kind_not_choice")
    opts = card.get("options") if isinstance(card.get("options"), list) else []
    if not 4 <= len(opts) <= 8:
        fails.append("option_count_not_4_to_8")
    labels = [(o.get("label") or "").strip().lower() for o in opts if isinstance(o, dict)]
    raw = [(o.get("label") or "") for o in opts if isinstance(o, dict)]
    if any(": " in x or ":" in x or x.lstrip().startswith("-") or "\n" in x for x in raw):
        fails.append("label_format")
    if any("\n" in (o.get("definition") or "") for o in opts if isinstance(o, dict)) or "\n" in (card.get("question") or ""):
        fails.append("multiline_text")
    if len([x for x in labels if x in DENY_EMOTION]) >= 3 or sum(1 for x in labels if x in DENY_EMOTION) >= max(2, len(labels) // 2):
        fails.append("standard_emotion_list")
    if any(x in DENY_POLITICAL for x in labels):
        fails.append("standard_political_scale")
    sh = card.get("expected_share")
    if not isinstance(sh, dict) or not sh:
        fails.append("expected_share_missing")
    else:
        try:
            vals = [float(v) for v in sh.values()]
            if abs(sum(vals) - 1.0) > SHARE_SUM_TOL:
                fails.append("expected_share_not_sum_1")
            if max(vals) > SHARE_MAX:
                fails.append("expected_share_one_option_dominates")
            if {str(k).strip().lower() for k in sh} != set(labels):
                fails.append("expected_share_keys")
        except (TypeError, ValueError):
            fails.append("expected_share_not_numbers")
    return fails, det


def gb_admitted_cards() -> list:
    return L.read_jsonl(L.GB / "cards" / "admitted.jsonl")


def load_authored(key: dict) -> tuple:
    cards, problems = [], []
    for tid, t in sorted(key["tasks"].items()):
        p = L.AUTH_A / f"{tid}.json"
        if not p.exists():
            problems.append(f"{tid}: no answer file")
            continue
        try:
            d = json.loads(p.read_text(encoding="utf-8"))
        except Exception as e:  # noqa: BLE001 - reported
            problems.append(f"{tid}: unreadable ({e})")
            continue
        cl = d.get("cards") if isinstance(d, dict) else None
        if not isinstance(d, dict) or d.get("task_id") != tid:
            problems.append(f"{tid}: task_id {d.get('task_id') if isinstance(d, dict) else None!r}")
        if not isinstance(cl, list) or len(cl) != L.CARDS_PER_TASK:
            problems.append(f"{tid}: expected {L.CARDS_PER_TASK} cards, found {len(cl) if isinstance(cl, list) else 'none'}")
            cl = cl if isinstance(cl, list) else []
        for i, c in enumerate(cl):
            if isinstance(c, dict):
                cards.append({"src": f"{tid}#{i}", "task_id": tid, "domain": t["domain"], "slice": t["slice"],
                              "topic": t["topic"], "card": c})
    return cards, problems


def cmd_lint() -> dict:
    key = L.read_json(L.CARDS / "author_key.json")
    cards, problems = load_authored(key)
    gb = gb_admitted_cards()
    report, passing, reason_ct = [], [], Counter()
    for s in cards:
        reasons, det = lint_i10(s["card"])
        for r in reasons:
            reason_ct[r] += 1
        report.append({"src": s["src"], "domain": s["domain"], "slice": s["slice"], "status": "lint_fail" if reasons else "lint_pass",
                       "reasons": reasons, "details": det})
        if not reasons:
            passing.append(s)
    by_src = {r["src"]: r for r in report}
    kept, dedup = [], Counter()
    gbq = [(g["domain"], set(gcards.toks(g["question"])), g["kind"]) for g in gb]
    for s in passing:
        qs = set(gcards.toks(s["card"]["question"]))
        near = None
        for d, gq, gk in gbq:
            if d == s["domain"] and gcards.jacc(qs, gq) >= gcards.NEAR_DUP:
                near = f"GB card question (same domain)"
                break
        if near is None:
            for k in kept:
                if k["domain"] == s["domain"] and gcards.jacc(qs, set(gcards.toks(k["card"]["question"]))) >= gcards.NEAR_DUP:
                    near = f"near duplicate of {k['src']}"
                    break
        if near:
            by_src[s["src"]].update(status="dedup_drop", reasons=[near])
            dedup["near_duplicate_question"] += 1
            continue
        kept.append(s)
    survivors = [{"src": s["src"], "domain": s["domain"], "slice": s["slice"], "topic": s["topic"], "task_id": s["task_id"],
                  "card": s["card"]} for s in kept]
    summ = {"answer_files": len(list(L.AUTH_A.glob("*.json"))) if L.AUTH_A.exists() else 0, "problems": problems,
            "cards_loaded": len(cards), "lint_pass": len(passing), "lint_fail": len(cards) - len(passing),
            "lint_fail_reasons": dict(reason_ct), "dedup_drops": dict(dedup), "survivors": len(survivors),
            "survivors_by_domain": dict(Counter(s["domain"] for s in survivors)),
            "survivors_by_slice": dict(Counter(s["slice"] for s in survivors))}
    L.write_json(L.CARDS / "lint_report.json", {"summary": summ, "cards": list(by_src.values())})
    L.write_json(L.CARDS / "survivors.json", survivors)
    L.set_state("lint", survivors=len(survivors))
    return summ


# ---------------------------------------------------------------------------------------------------- G-LEX reads
EXTRACT_CHUNK = 25
EXTRACT_INSTRUCTIONS = gcards.PROMPT.split("Write ONE JSON object")[0].strip()
EXTRACT_CONTRACT = """Write ONE JSON object, and nothing else (no text before or after it), to the answer file named at the top. task_id must be "{task_id}".
{{"task_id": "{task_id}",
 "answers": [
   {{"qid": "<the qid of a card>",
    "options": [
      {{"name": "<option name exactly as given>", "meaning": "one line", "example": "one short example text"}}
    ]}}
 ]}}

Give one entry in "answers" for every card in the items, and one entry in "options" for every option of that card. Copy each qid and
each option name exactly as given."""


def _opt_key(seed, src, name):
    return hashlib.sha256(f"{seed}|opt|{src}|{name}".encode()).hexdigest()


def build_extract(read: str, survivors: list) -> list:
    seed = f"item10-g-lex-A47|{read}"
    secret = hashlib.sha256(seed.encode()).digest()
    order = sorted(survivors, key=lambda s: hashlib.sha256(f"{seed}|order|{s['src']}".encode()).hexdigest())
    tasks = []
    for k in range(0, len(order), EXTRACT_CHUNK):
        tid = f"I10-ext-{read}-{k // EXTRACT_CHUNK + 1:03d}"
        cards_out, keys_here = [], {}
        for s in order[k:k + EXTRACT_CHUNK]:
            c = s["card"]
            qid = "q" + hmac.new(secret, s["src"].encode(), hashlib.sha256).hexdigest()[:10]
            if qid in keys_here:
                raise SystemExit(f"qid collision in {tid}")
            keys_here[qid] = s["src"]
            opts = [{"name": o["label"].strip(), "definition": o["definition"].strip()} for o in c["options"]]
            opts.sort(key=lambda o: _opt_key(seed, s["src"], o["name"]))
            cards_out.append({"qid": qid, "kind": c["kind"], "who_decides": c["who_decides"].strip(),
                              "question": c["question"].strip(), "options": opts})
        ans = str(L.EXT_A / f"{tid}.json")
        text = L.task_md("Item 10 card G-LEX read", tid, ans, EXTRACT_INSTRUCTIONS, EXTRACT_CONTRACT.format(task_id=tid),
                         cards_out, len(cards_out), items_label="Cards")
        blob = json.dumps(cards_out, ensure_ascii=False)
        leaked = [src for src in keys_here.values() if src in blob]
        if leaked:
            raise SystemExit(f"internal id leaked into {tid}: {leaked[:2]}")
        tasks.append({"task_id": tid, "read": read, "text": text, "keys": keys_here, "answer_path": ans})
    return tasks


def cmd_extract() -> list:
    survivors = L.read_json(L.CARDS / "survivors.json")
    if not survivors:
        raise SystemExit("no survivors")
    reads = {r: build_extract(r, survivors) for r in ("rA", "rB")}
    qa = {q for t in reads["rA"] for q in t["keys"]}
    qb = {q for t in reads["rB"] for q in t["keys"]}
    if qa & qb:
        raise SystemExit("qids overlap across the two reads")
    man, keys, out = {"n_survivor_cards": len(survivors), "chunk_size": EXTRACT_CHUNK, "tasks": []}, {}, []
    for r, tasks in reads.items():
        for t in tasks:
            tf = L.EXT_T / f"{t['task_id']}.md"
            L.write_text(tf, t["text"])
            man["tasks"].append({"task_id": t["task_id"], "read": r, "n_cards": len(t["keys"]), "task_file": str(tf),
                                 "answer_file": t["answer_path"], "sha256": L.sha_file(tf)})
            keys[t["task_id"]] = t["keys"]
            out.append(L.task_record(tf, t["answer_path"], "haiku"))
    L.EXT_A.mkdir(parents=True, exist_ok=True)
    L.write_json(L.EXT_K / "keys.json", keys)
    L.write_json(L.EXT_K / "manifest.json", man)
    L.set_state("extract", n_tasks=len(out), survivors=len(survivors))
    return out


# ---------------------------------------------------------------------------------------------------- compare / admit
def load_reads() -> tuple:
    man = L.read_json(L.EXT_K / "manifest.json")
    keys = L.read_json(L.EXT_K / "keys.json")
    survivors = {s["src"]: s for s in L.read_json(L.CARDS / "survivors.json")}
    problems, reads = [], {"rA": {}, "rB": {}}
    for t in man["tasks"]:
        tf = Path(t["task_file"])
        if L.sha_file(tf) != t["sha256"]:
            problems.append(f"{t['task_id']}: task file sha256 changed since the manifest")
        ap = Path(t["answer_file"])
        if not ap.exists():
            problems.append(f"{t['task_id']}: no answer file")
            continue
        try:
            ans = json.loads(ap.read_text(encoding="utf-8"))
        except Exception as e:  # noqa: BLE001
            problems.append(f"{t['task_id']}: unreadable answer ({e})")
            continue
        if not isinstance(ans, dict) or ans.get("task_id") != t["task_id"]:
            problems.append(f"{t['task_id']}: answer task_id mismatch")
            continue
        seen = Counter()
        for a in ans.get("answers", []):
            q = a.get("qid")
            seen[q] += 1
            if q not in keys[t["task_id"]]:
                problems.append(f"{t['task_id']}: unknown qid {q!r}")
                continue
            reads[t["read"]][keys[t["task_id"]][q]] = {"task_id": t["task_id"], "qid": q, "options": a.get("options", [])}
        for q in keys[t["task_id"]]:
            if seen[q] != 1:
                problems.append(f"{t['task_id']}: qid {q} answered {seen[q]} times")
    return survivors, reads, problems


def same_decision_pairs(survivors: dict, thr: float = 0.45) -> list:
    """Pairs of cards of one domain whose question + option-name words overlap strongly: they may ask the same decision."""
    sig = {}
    for s in survivors.values():
        c = s["card"]
        sig[s["src"]] = set(gcards.toks(c["question"])) | {t for o in c["options"] for t in gcards.toks(o["label"])}
    out = []
    srcs = sorted(sig)
    for i, a in enumerate(srcs):
        for b in srcs[i + 1:]:
            if survivors[a]["domain"] == survivors[b]["domain"]:
                v = gcards.jacc(sig[a], sig[b])
                if v >= thr:
                    out.append({"a": a, "b": b, "jaccard": round(v, 3)})
    return out


HARD_FLAG = re.compile(r"^r[AB]:(missing_card$|option_names_differ |.*:(missing_option|empty_field)$)")


def is_hard_flag(flag: str) -> bool:
    """A structural failure of a read (card or option absent, names differ, empty field), not a lexical aid flag."""
    return bool(HARD_FLAG.match(flag))


def cmd_compare(only: str | None = None) -> dict:
    survivors, reads, problems = load_reads()
    docs = []
    for s in survivors.values():
        docs += [o["definition"] for o in s["card"]["options"]]
    for r in ("rA", "rB"):
        for v in reads[r].values():
            for o in v["options"]:
                docs += [o.get("meaning", ""), o.get("example", "")]
    tf = AC.Tfidf(docs)
    res = []
    for s in sorted(survivors.values(), key=lambda s: s["src"]):
        x = AC.check_card(tf, s, reads)
        # the shared checker marks a flag hard when it merely contains the word "missing"; an option label such as
        # "missing feature or add-on" then fails a sound card.  Recompute from the flag structure (rA/rB:missing_card,
        # rA/rB:<label>:missing_option, option_names_differ, empty_field), keeping the shared checker untouched.
        x["hard_fail"] = [f for f in x["flags"] if is_hard_flag(f)]
        x["slice"], x["topic"] = s["slice"], s["topic"]
        res.append(x)
    flag_types = Counter(re.sub(r"^r[AB]:(.*?:)?", "", f).split("=")[0].split("(")[0] for x in res for f in x["flags"])
    summ = {"problems": problems, "cards": len(res), "answered": {r: len(reads[r]) for r in reads},
            "cards_with_any_flag": sum(1 for x in res if x["flags"]), "hard_fail": sum(1 for x in res if x["hard_fail"]),
            "flag_types": dict(flag_types), "same_decision_pairs": same_decision_pairs(survivors)}
    L.write_json(L.ADMIT / "compare.json", {"summary": summ, "cards": res})
    L.set_state("compare", cards=len(res), hard_fail=summ["hard_fail"])
    return summ


def review_sheet(only: str | None = None, flagged_only: bool = False) -> str:
    cmp_ = L.read_json(L.ADMIT / "compare.json")
    lines = []
    for x in cmp_["cards"]:
        if only and x["domain"] != only:
            continue
        if flagged_only and not x["flags"]:
            continue
        lines.append("=" * 90)
        lines.append(f"{x['src']} [{x['slice']}/{x['topic']}] {x['question']}")
        lines.append(f"  who: {x['who_decides']}")
        for o in x["options"]:
            lab = o["label"]
            lines.append(f"  * {lab}: {o['definition']}")
            for r in ("rA", "rB"):
                rec = x["reads"].get(r, {}).get(lab)
                if rec:
                    lines.append(f"     {r} M: {rec['meaning']}")
                    lines.append(f"     {r} E: {rec['example']}")
        lines.append(f"  FLAGS: {x['flags']}")
    return "\n".join(lines)


def cmd_admit() -> dict:
    cmp_ = L.read_json(L.ADMIT / "compare.json")
    rev = L.read_json(L.ADMIT / "review.json")
    verdicts = rev["verdicts"]
    missing = [x["src"] for x in cmp_["cards"] if x["src"] not in verdicts]
    if missing:
        raise SystemExit(f"no verdict for {missing}")
    if cmp_["summary"]["problems"]:
        raise SystemExit(f"program problems: {cmp_['summary']['problems'][:3]}")
    admitted, rejected = [], []
    for x in cmp_["cards"]:
        v = verdicts[x["src"]]
        if v["admit"] and x["hard_fail"]:
            raise SystemExit(f"{x['src']}: admitted with a hard program failure {x['hard_fail']}")
        (admitted if v["admit"] else rejected).append((x, v.get("reason", "")))
    counters = Counter()
    rows = []
    for x, _ in sorted(admitted, key=lambda t: t[0]["src"]):
        tid, j = x["src"].split("#")
        cid = "i10_" + re.sub(r"^i10[ab]_", "", tid) + f"_c{j}"
        counters[x["domain"]] += 1
        rows.append({"card_id": cid, "src": x["src"], "domain": x["domain"], "slice": x["slice"], "topic": x["topic"],
                     "kind": x["kind"], "question": x["question"], "options": [o["label"] for o in x["options"]],
                     "definitions": {o["label"]: o["definition"] for o in x["options"]}})
    ids = [r["card_id"] for r in rows]
    if len(set(ids)) != len(ids):
        raise SystemExit("duplicate card ids")
    L.write_jsonl(L.CARDS / "admitted.jsonl", rows)
    summ = {"admitted": len(rows), "rejected": len(rejected), "by_domain": dict(counters),
            "by_slice": dict(Counter(r["slice"] for r in rows)),
            "same_decision_pairs": rev.get("same_decision_pairs", []),
            "reject_reasons": [{"src": x["src"], "reason": why} for x, why in rejected]}
    L.write_json(L.ADMIT / "admission_summary.json", summ)
    L.set_state("admit", admitted=len(rows), rejected=len(rejected))
    return summ
