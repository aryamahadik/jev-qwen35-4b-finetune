#!/usr/bin/env python3
"""W8: complaint and ticket routing (PREREG_FINAL A40 addendum, W8). Gold = CONSTRUCTION from Haiku-authored text.

Two stages, both deterministic (seed 20261013):

  tasks   writes the Haiku AUTHORING tasks (24 = one per routing card, builders/w8_cards.py) to author/w8/tasks/, the
          key author/w8/tasks_key.json and author/w8/MANIFEST.json. A task holds the routing card, the card's precedence
          sentence and one SLOT per complaint. A slot names the route the complaint must go to (the intended answer),
          a kind (plain / angry / misleading / multi / other_plain / vague) and style fields. The slots are balanced
          across routes by construction and about 60% of them are hard cases (angry tone that does not change the
          route, decoy keywords of another team, two issues where the precedence sentence decides).
  build   reads author/w8/answers/W8_tNN.json and writes candidates/w8_candidates.jsonl (+ _stats.json). Row =
          choice question: state = the complaint, options = the card's routes in a seeded order (general / other
          usually last), card = one "- route: definition" line per option, instructions = the question with the
          card's precedence sentence (one line). Gold = the route of the slot the complaint was written for (recorded,
          never chosen or edited). Malformed items are dropped, never repaired; duplicates and texts with an email,
          phone number, IP address or user path are dropped; routes are balanced within each card (max/min <= 1.2).

Verification (A40 c: blind Haiku, then Opus for the rest, 5% audit, G13) runs on these candidates afterwards. No public
complaint corpus and no CFPB or consumer-finance text is used or shown to the authors.

  ../../../../../.venv/bin/python -I builders/w8_complaint_routing.py tasks [--force] [--dry-run]
  ../../../../../.venv/bin/python -I builders/w8_complaint_routing.py build [--dry-run]
"""
from __future__ import annotations

import json
import sys
from collections import Counter, defaultdict
from pathlib import Path

if __package__ in (None, ""):
    sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from builders import common as C  # noqa: E402
from builders.w8_cards import (ANGRY_STYLES, CARDS, CHANNELS, GENERAL, K_BY_N, LENGTH_WEIGHTS, LENGTHS, PERSONAS,  # noqa: E402
                               TONES, card_problems, route_by_label, route_labels)

T = "W8"
NAME = "complaint_routing"
C.TYPES.setdefault(T, NAME)                       # common.TYPES lists W1-W7; make_row() needs the type registered

GEN_VERSION_W8 = "gblock-wave2 1.1 (14 Oct 2026, W8)"
W8_DIR = C.AUTHOR / "w8"
W8_TASKS = W8_DIR / "tasks"
W8_ANSWERS = W8_DIR / "answers"
W8_KEY = W8_DIR / "tasks_key.json"
W8_MANIFEST = W8_DIR / "MANIFEST.json"
OUT_ROWS = C.CAND_DIR / "w8_candidates.jsonl"
OUT_STATS = C.CAND_DIR / "w8_candidates_stats.json"

MAX_TASKS = 24
TEXT_WORDS = (3, 230)
BALANCE_RATIO = 1.2
TEAM_KINDS = ("plain", "angry", "misleading", "multi", "plain")           # 40% plain, 20% each of the hard kinds
GEN_KINDS = ("other_plain", "angry", "misleading", "vague", "other_plain")
HARD_KINDS = ("angry", "misleading", "multi", "vague")

ORDER_SENTENCES = (
    "If a complaint raises issues for more than one team, send it to the team that comes first in this order: {lst}, "
    "then general / other.",
    "When a complaint touches several teams, the team listed earliest here gets it: {lst}, then general / other.",
)
ASK_SENTENCES = (
    "If a complaint raises issues for more than one team, send it to the team that can fix what the customer most "
    "wants done; problems mentioned in passing do not decide.",
    "A complaint that touches several teams goes to the team that handles the customer's main request, not the one "
    "for a side remark.",
    "When more than one team could be involved, choose the team for the thing the customer is mainly asking to have "
    "put right.",
)
TOP_SENTENCE = ("A complaint that raises {phrase} always goes to {top}, even if it also raises other problems; any "
                "other complaint that touches several teams goes to the team that can fix what the customer most wants "
                "done.")
QUESTIONS = (
    "{Company} routes each complaint from {who} to exactly one team. {rule} Which team should handle the complaint "
    "below? Use general / other only if no other team fits.",
    "Complaint routing at {company} (complaints from {who}): pick the one team that should handle the complaint below. "
    "{rule} Choose general / other only when no other team fits.",
)


# ------------------------------------------------------------------------------------------------------- the card

def rule_sentence(card: dict) -> str:
    rule = card["rule"]
    if rule["type"] == "order":
        i = C.key_hash(C.SEED, T, "ordersentence", card["card_id"]) % len(ORDER_SENTENCES)
        return ORDER_SENTENCES[i].format(lst=", ".join(rule["order"]))
    if rule["type"] == "top":
        return TOP_SENTENCE.format(phrase=rule["phrase"], top=rule["top"])
    if rule.get("sentence"):
        return rule["sentence"]
    return ASK_SENTENCES[C.key_hash(C.SEED, T, "asksentence", card["card_id"]) % len(ASK_SENTENCES)]


def secondary_choices(card: dict, gold: str) -> list:
    """The routes a multi-issue complaint may carry as its second issue when `gold` is the winning route, so that the
    card's precedence rule gives `gold` (never the other way round)."""
    rule, labels = card["rule"], route_labels(card)
    others = [x for x in labels if x != gold]
    if rule["type"] == "order":
        rank = rule["order"]
        return [x for x in others if x == GENERAL or (x in rank and rank.index(x) > rank.index(gold))]
    if rule["type"] == "top" and gold != rule["top"]:
        return [x for x in others if x != rule["top"]]
    return others


def decoy_choices(card: dict, gold: str) -> list:
    """Teams whose keywords a 'misleading' complaint may borrow (never general; never the top team of a 'top' rule
    unless it is the gold, so the decoy words cannot trigger the card's top rule)."""
    rule = card["rule"]
    c = [x for x in route_labels(card) if x not in (gold, GENERAL)]
    if rule["type"] == "top" and gold != rule["top"]:
        c = [x for x in c if x != rule["top"]] or c
    return c


# --------------------------------------------------------------------------------------------------------- slots

def plan_slots(card: dict) -> list:
    """The card's slots, balanced across routes, in a seeded shuffled order with ids s01.. ."""
    labels = route_labels(card)
    k = K_BY_N[len(labels)]
    slots = []
    for label in labels:
        gen = label == GENERAL
        cyc = GEN_KINDS if gen else TEAM_KINDS
        for j in range(k):
            rng = C.rng_for(T, card["card_id"], label, j)
            kind = cyc[j % len(cyc)]
            s = {"route": label, "kind": kind, "decoy": None, "secondary": None, "first": None, "hint": None}
            if kind == "angry":
                s["tone"] = "angry: " + rng.choice(ANGRY_STYLES)
            else:
                s["tone"] = rng.choice(TONES)
            if gen:
                s["hint"] = card["other_hints"][(j + rng.randrange(len(card["other_hints"]))) % len(card["other_hints"])]
            if kind == "misleading":
                s["decoy"] = rng.choice(decoy_choices(card, label))
            if kind == "multi":
                s["secondary"] = rng.choice(secondary_choices(card, label))
                s["first"] = "secondary" if rng.random() < 0.55 else "gold"       # which issue the text mentions first
            pool = [(ln, w) for (ln, w) in zip(LENGTHS, LENGTH_WEIGHTS) if not (kind == "multi" and ln[0] == "very short")]
            lname, lrange = rng.choices([p[0] for p in pool], weights=[p[1] for p in pool])[0]
            s["length"], s["length_words"] = lname, lrange
            s["writer"] = rng.choice(PERSONAS[card["audience"]])
            s["channel"] = rng.choice(CHANNELS)
            s["_j"] = j
            slots.append(s)
    slots.sort(key=lambda s: C.key_hash(C.SEED, T, "slotorder", card["card_id"], s["route"], s["_j"]))
    for i, s in enumerate(slots):
        s["slot_id"] = f"s{i + 1:02d}"
        del s["_j"]
    return slots


def second_issue_phrase(card: dict, sec: str) -> str:
    if sec == GENERAL:
        return "a side remark that fits none of the teams (general / other)"
    return f"a '{sec}' matter (card definition: {route_by_label(card)[sec]['definition'].rstrip('.')})"


def slot_brief(card: dict, s: dict) -> str:
    """The slot's one-paragraph instruction (gold-by-construction wording: it names the intended route)."""
    r, kind = s["route"], s["kind"]
    by = route_by_label(card)
    rule = card["rule"]
    if kind == "plain":
        return f"One clear problem that belongs to '{r}'. Give concrete invented details."
    if kind == "other_plain":
        return (f"A matter that none of the teams on the card handles, for example {s['hint']}. It must sit clearly "
                f"outside every team's definition, and the route is 'general / other'.")
    if kind == "vague":
        return ("An unhappy message that names no concrete problem and no request (the customer is fed up, or "
                "disappointed, and says little else), so no team can be picked from it; the route is 'general / other'.")
    if kind == "angry":
        if r == GENERAL:
            return (f"Angry about something no team handles (for example {s['hint']}) or an angry outburst without a "
                    f"concrete problem. No team's definition fits it, so the route is 'general / other'.")
        return (f"Angry. The one concrete problem is a '{r}' matter. Threats to cancel, to post a bad review or to "
                f"call a regulator are only threats: they must not make it look like another team's job.")
    if kind == "misleading":
        d = s["decoy"]
        words = ", ".join(by[d]["words"][:4])
        if r == GENERAL:
            return (f"A matter that fits no team, written with words that sound like the job of '{d}' (such as: "
                    f"{words}). The decoy words must really appear, but it is still something no team handles, so "
                    f"the route is 'general / other'. Example kind of matter: {s['hint']}.")
        return (f"One problem for '{r}', written with words that sound like the job of '{d}' (such as: {words}). The "
                f"decoy words must really appear, but what the customer wants put right is the '{r}' matter.")
    # multi
    sec = s["secondary"]
    sec_p = second_issue_phrase(card, sec)
    first_gold = s["first"] == "gold"
    if rule["type"] == "order":
        order_txt = (f"The card's order puts '{r}' ahead of {('general / other' if sec == GENERAL else repr(sec))}, so "
                     f"'{r}' is the route. ")
        place = ("Mention the '{r}' issue first and the other one second." if first_gold else
                 "Describe the other issue first and at more length, as if it were the customer's main worry, then "
                 "raise the '{r}' issue clearly but more briefly.").format(r=r)
        return f"TWO issues: a '{r}' matter and {sec_p}. {order_txt}{place}"
    if rule["type"] == "top" and r == rule["top"]:
        return (f"TWO issues: {rule['phrase']} (a '{r}' matter), raised clearly but it may be brief, and {sec_p}, "
                f"which takes most of the words and may look like the main request. The card sends anything "
                f"involving {rule['phrase']} to '{r}', so '{r}' is the route.")
    place = ("Mention the main request first and the side remark second." if first_gold else
             "Mention the side remark first, then the main request.")
    extra = f" Neither issue involves {rule['phrase']}." if rule["type"] == "top" else ""
    return (f"TWO issues: the MAIN request is a '{r}' matter, and a side remark of one sentence or less is {sec_p}."
            f"{extra} State the main request in the customer's own words (for example 'what I really want is' "
            f"or 'the main thing is') so that it is clearly the main ask. {place}")


# ---------------------------------------------------------------------------------------------------------- tasks

W8_RULES = """General rules (all of them apply):
1. Everything you write is new and invented by you now. Do not copy or closely paraphrase any real customer complaint
   or any public complaint, support-ticket, intent or banking-and-finance dataset or benchmark, and do not reuse
   well-known example texts.
2. Make it varied and realistic: ordinary people with ordinary problems; different lengths, tones and writers; some
   typos or informal language is good, as the "writer" and "channel" fields suggest.
3. Use made-up names, products and references. No real company or brand names, no real people, and no phone numbers,
   email addresses, web addresses or street addresses.
4. Nothing hateful or sexual, no slurs, no threats of violence and no instructions for causing harm. These are
   complaints about service, money and admin: keep any medical or danger detail to a few plain words (for example "a
   blood test", "a smell of gas"), never graphic.
5. Follow the counts exactly: one complaint per slot, in slot order. The slot IS the intended answer.
6. Output: write ONE JSON object and nothing else (no markdown fence, no comments, no trailing commas; escape any
   double quote inside a string as \\"; use \\n for a line break inside a string) to this exact file path:
   {answer_path}
7. Access rules: read only this task file; write only the answer file named above. Do not open any other file, do
   not run programs, do not use the web."""

W8_BRIEF = """Task {task_id} (W8, complaint routing). A small classifier will see ONE complaint written to {company} by
one of its {who}, together with a routing card: a list of teams (or products), each with a one-sentence definition,
and a rule for a complaint that touches more than one of them. It must pick the single team that should handle the
complaint.

What this file gives you:
- "routing_card": the teams, each with "team", "definition" and "typical_words" (words people often use when writing
  to that team; "general / other" has none).
- "precedence_sentence": the card's rule for a complaint that touches more than one team. The classifier sees this
  sentence too.
- "slots": {n} slots in a fixed order. Each has a "slot_id", the "route" (the team the complaint MUST go to), a "kind",
  a "brief" for that slot, and style fields ("tone", "length_words", "writer", "channel").

Your job: write exactly ONE complaint per slot, in slot order. Under the card's definitions and the precedence
sentence, the finished complaint must clearly belong to the slot's "route" and to no other team. Check each complaint
once against the card before you move on.

Kinds of slot:
- plain: one clear problem that belongs to the route team.
- angry: the writer is angry (insults, capitals, sarcasm, threats to cancel, to post a bad review or to go to a
  regulator). The anger never changes the route: the one concrete problem still belongs only to the route team.
- misleading: one problem for the route team, written with words or phrases that sound like another team's job (the
  brief names that decoy team and gives sample words). The decoy words must really appear in the text, but what the
  customer wants put right is the route team's matter.
- multi: two issues in one complaint. The precedence sentence decides which team wins, and the brief says which issue
  is which and which one comes first in the text. Both issues must be recognisable, and the winning issue must win
  under the precedence sentence exactly as the brief says.
- other_plain and vague (route "general / other" only): other_plain is a matter that none of the teams handles (the
  brief gives an example of the kind of matter); vague is an unhappy message that names no concrete problem and no
  request, so no team can be picked from it.
In every kind the complaint is the customer's own message: do not label it and do not explain the routing.

Style fields: "tone" is the mood; "length_words" is a min-max guide for the number of words (stay close to it);
"writer" is who is writing (use their voice, detail and language skill); "channel" is the form of the message (an email
may have a greeting and a sign-off; a chat or text message is short and informal; a letter is formal; a public post
speaks to everyone; a voicemail transcription has "um" and run-on sentences; a review reads like a review).

Writing rules for this task:
- Never write a team's name as a label or heading, and never say "this is for the X team", "please pass this to ..." or
  "category:". Customers do not know the company's internal teams, but ordinary words such as "my bill" or "your app"
  are fine.
- Invent the facts (names, amounts, dates, products, short references such as "order 48213" or "account ending 4821").
  Do not write phone numbers, email addresses, web addresses or street addresses.
- plain, angry and misleading complaints raise ONLY the route team's issue: do not add a request that belongs to
  another team (for example a refund request in a complaint about a broken item when a refunds team exists), because
  the precedence sentence could then send the complaint somewhere else.
- Every complaint must differ in situation and wording. Do not start more than 3 complaints with the same word, and
  avoid "I am writing to complain". Several slots for the same team need different problems.
- Refer to the company as "you", "your company" or by an invented brand name; never by a real company name.

JSON shape (one entry per slot, same order, slot_id copied):
{{"task_id": "{task_id}",
  "complaints": [
    {{"slot_id": "s01", "text": "...", "note": "a few words naming the issue (and the second issue for a multi slot)"}},
    "... {n} in total"
  ]}}
"note" is for our records only.

""" + W8_RULES


def company_cap(s: str) -> str:
    return s[0].upper() + s[1:]


def card_key_entry(card: dict) -> dict:
    """What the builder needs from the card at build time, frozen in the key (so it always matches the brief)."""
    by = route_by_label(card)
    return {"card_id": card["card_id"], "industry": card["industry"], "company": card["company"], "who": card["who"],
            "audience": card["audience"], "routes": route_labels(card),
            "definitions": {x: by[x]["definition"] for x in by}, "words": {x: by[x]["words"] for x in by},
            "rule_type": card["rule"]["type"], "rule_sentence": rule_sentence(card),
            "top": card["rule"].get("top"), "order": card["rule"].get("order")}


def build_tasks() -> tuple:
    """({task_id: task dict}, {task_id: key entry}). Deterministic."""
    assert len(CARDS) <= MAX_TASKS, len(CARDS)
    tasks, key = {}, {}
    tmpl_sha = C.sha256_text(W8_BRIEF)
    for i, card in enumerate(CARDS):
        probs = card_problems(card)
        assert not probs, probs
        tid = f"W8_t{i + 1:02d}"
        tpath, apath = W8_TASKS / f"{tid}.json", W8_ANSWERS / f"{tid}.json"
        slots = plan_slots(card)
        by = route_by_label(card)
        n = len(slots)
        task = {
            "task_id": tid, "type": T, "task_name": NAME, "kind": "wave2_authoring_w8",
            "binding": "PREREG_FINAL.md Ruling A40 addendum (W8) with A40 (b)-(c): Haiku 5.5 writes the wording; the "
                       "route of each complaint is the slot this brief names, recorded by the builder as the "
                       "constructed gold and verified blind (A40 c); Haiku never edits or chooses a gold afterwards",
            "answer_path": str(apath), "allowed_read": [str(tpath)], "allowed_write": [str(apath)],
            "instructions": W8_BRIEF.format(task_id=tid, n=n, answer_path=apath, company=card["company"],
                                            who=card["who"]),
            "instructions_template_sha256": tmpl_sha,
            "industry": card["industry"], "company": card["company"],
            "routing_card": [{"team": x["label"], "definition": x["definition"], "typical_words": x["words"]}
                             for x in card["routes"]],
            "precedence_sentence": rule_sentence(card),
            "slots": [{"slot_id": s["slot_id"], "route": s["route"], "kind": s["kind"], "brief": slot_brief(card, s),
                       "tone": s["tone"], "length_words": s["length_words"], "writer": s["writer"],
                       "channel": s["channel"]} for s in slots]}
        kk = {"type": T, "task_file": str(tpath), "answer_file": str(apath), "template_sha256": tmpl_sha,
              "card": card_key_entry(card),
              "slots": {s["slot_id"]: {k: s[k] for k in ("route", "kind", "decoy", "secondary", "first", "hint", "tone",
                                                          "length", "length_words", "writer", "channel")}
                        for s in slots}}
        del by
        tasks[tid], key[tid] = task, kk
    return tasks, key


def task_text(task: dict) -> str:
    return json.dumps(task, ensure_ascii=False, indent=1) + "\n"


def plan_counts(tasks: dict, key: dict) -> dict:
    routes = Counter()
    kinds = Counter()
    for tid, kk in key.items():
        for s in kk["slots"].values():
            routes[(kk["card"]["card_id"], s["route"])] += 1
            kinds[s["kind"]] += 1
    n = sum(kinds.values())
    per_card = {kk["card"]["card_id"]: len(kk["slots"]) for kk in key.values()}
    return {"tasks": len(tasks), "slots": n, "cards": len(per_card), "per_card": per_card,
            "industries": sorted({kk["card"]["industry"] for kk in key.values()}),
            "routes_per_card": dict(Counter(len(kk["card"]["routes"]) for kk in key.values())),
            "rules": dict(Counter(kk["card"]["rule_type"] for kk in key.values())),
            "kinds": dict(kinds), "hard_share": round(sum(kinds[k] for k in HARD_KINDS) / n, 4),
            "route_count_min_max": [min(routes.values()), max(routes.values())]}


def write_tasks(argv: list) -> dict:
    force, dry = "--force" in argv, "--dry-run" in argv
    tasks, key = build_tasks()
    blocked = []
    for tid, task in tasks.items():
        tpath, apath = Path(key[tid]["task_file"]), Path(key[tid]["answer_file"])
        if apath.exists() and tpath.exists() and C.kp.check_path(tpath).read_text(encoding="utf-8") != task_text(task):
            blocked.append(tid)
    if blocked and not force:
        raise SystemExit(f"answers exist for tasks that would change: {blocked} (rerun with --force only if those "
                         f"answers are discarded)")
    counts = plan_counts(tasks, key)
    if not dry:
        W8_ANSWERS.mkdir(parents=True, exist_ok=True)
        C.kp.check_path(W8_ANSWERS)
        for tid, task in tasks.items():
            C.kp.write_text(key[tid]["task_file"], task_text(task))
            key[tid]["task_sha256"] = C.sha256_file(key[tid]["task_file"])
        C.kp.write_json(W8_KEY, {"seed": C.SEED, "ruling": "PREREG_FINAL A40 addendum (W8)", "expected": counts,
                                 "tasks": key})
        C.kp.write_json(W8_MANIFEST, {
            "what": "G-block wave-2 W8 (complaint routing) Haiku authoring tasks", "n_tasks": len(tasks),
            "expected": counts,
            "tasks": {tid: {"task_sha256": key[tid]["task_sha256"], "answer_file": key[tid]["answer_file"],
                            "card_id": key[tid]["card"]["card_id"], "n_slots": len(key[tid]["slots"])}
                      for tid in tasks},
            "template_sha256": C.sha256_text(W8_BRIEF)})
    print(json.dumps(counts))
    return counts


# ---------------------------------------------------------------------------------------------------------- build

def option_order(labels: list, tid: str, sid: str) -> list:
    """Seeded option order for one row: the teams shuffled; general / other last in 3 of 4 rows, else anywhere."""
    teams = sorted((x for x in labels if x != GENERAL), key=lambda x: C.key_hash(C.SEED, T, "opts", tid, sid, x))
    if GENERAL in labels:
        if C.key_hash(C.SEED, T, "genpos", tid, sid) % 4 == 0:
            teams.insert(C.key_hash(C.SEED, T, "genat", tid, sid) % (len(teams) + 1), GENERAL)
        else:
            teams.append(GENERAL)
    return teams


def make_row(tid: str, kk: dict, sid: str, text: str, note, prov: dict) -> dict:
    card, sl = kk["card"], kk["slots"][sid]
    labels = card["routes"]
    opts = option_order(labels, tid, sid)
    qi = C.pick_wording(QUESTIONS, T, tid, sid)
    question = QUESTIONS[qi].format(Company=company_cap(card["company"]), company=card["company"], who=card["who"],
                                    rule=card["rule_sentence"])
    gold = sl["route"]
    low = text.lower()
    decoy_hit = None
    if sl["kind"] == "misleading":
        decoy_hit = any(w.lower() in low for w in card["words"][sl["decoy"]])
    construction = {
        "slot": gold, "slot_id": sid, "kind": sl["kind"], "card_id": card["card_id"], "industry": card["industry"],
        "company": card["company"], "n_routes": len(labels), "rule_type": card["rule_type"], "decoy": sl["decoy"],
        "decoy_hit": decoy_hit, "secondary": sl["secondary"], "first_issue": sl["first"], "tone": sl["tone"],
        "length": sl["length"], "writer": sl["writer"], "channel": sl["channel"],
        "label_in_text": bool(gold != GENERAL and gold.lower() in low),
        "note": note[:200] if isinstance(note, str) else None}
    return C.make_row(
        T, f"{tid}:{sid}", f"c2_wave2:W8:{card['card_id']}", text, question, qtype="choice", options=opts, gold=gold,
        card=C.card_lines([(o, card["definitions"][o]) for o in opts]), gold_method="construction",
        construction=construction,
        extra_meta={"wording_id": f"W8.q{qi}", "licence": C.LICENCE_AUTHORED, "gen_version": GEN_VERSION_W8, **prov})


def load_key() -> dict:
    return C.read_json(W8_KEY)


def build(key: dict | None = None, answers: dict | None = None, checker=None) -> tuple:
    key = key if key is not None else load_key()
    rows, drops, tasks_seen, dd = [], Counter(), {}, C.Dedup()
    for tid, kk, obj, probs, prov in C.iter_answers(T, key, answers):
        tasks_seen[tid] = {"answered": obj is not None, "problems": list(probs), "card_id": kk["card"]["card_id"]}
        if obj is None:
            continue
        items = obj.get("complaints")
        if not isinstance(items, list):
            tasks_seen[tid]["problems"].append("complaints is not a list")
            continue
        if len(items) != len(kk["slots"]):
            drops[f"count_{len(items)}_not_{len(kk['slots'])}"] += 1       # recorded; the valid items are still used
        seen = set()
        for it in items:
            sid = it.get("slot_id") if isinstance(it, dict) else None
            if sid not in kk["slots"] or sid in seen:
                drops["unknown_or_repeated_slot_id"] += 1
                continue
            seen.add(sid)
            text, why = C.text_field(it.get("text"), min_w=TEXT_WORDS[0], max_w=TEXT_WORDS[1])
            if why:
                drops["text_" + why.split(" ")[0]] += 1
                continue
            if C.pii_reason(text):
                drops["pii"] += 1
                continue
            if not dd.new(text):
                drops["duplicate_complaint"] += 1
                continue
            rows.append(make_row(tid, kk, sid, text, it.get("note"), prov))
    kept, rdrops, toks = C.check_all(rows, checker)
    by_card = defaultdict(list)
    for r in kept:
        by_card[r["meta"]["construction"]["card_id"]].append(r)
    bal = []
    for cid in sorted(by_card):
        bal += C.balance(by_card[cid], seed_tag=f"W8.balance.{cid}", cap_ratio=BALANCE_RATIO)
    bal.sort(key=lambda r: r["id"])
    stats = stats_for(key["tasks"], tasks_seen, drops, rows, kept, bal, rdrops, toks)
    return bal, stats


def stats_for(task_keys, tasks_seen, drops, rows, kept, bal, rdrops, toks) -> dict:
    expected = Counter()
    for kk in task_keys.values():
        for s in kk["slots"].values():
            expected[(kk["card"]["card_id"], s["route"])] += 1
    cons = [r["meta"]["construction"] for r in bal]
    per_route = defaultdict(Counter)
    for r in bal:
        per_route[r["meta"]["construction"]["card_id"]][r["gold"]] += 1
    ratios = {cid: round(max(c.values()) / min(c.values()), 3) for cid, c in per_route.items() if c}
    mis = [c for c in cons if c["kind"] == "misleading"]
    st = C.authored_stats(T, tasks_seen, drops, rows, kept, rdrops, toks, {
        "task_name": NAME, "kept_after_balance": len(bal), "balance_ratio_cap": BALANCE_RATIO,
        "before_balance": C.label_stats(kept) | {"n_routes": len({r["gold"] for r in kept})},
        "n_cards_used": len(per_route), "industries": dict(Counter(c["industry"] for c in cons)),
        "kinds": dict(Counter(c["kind"] for c in cons)),
        "hard_share": round(sum(c["kind"] in HARD_KINDS for c in cons) / max(1, len(cons)), 4),
        "rule_types": dict(Counter(c["rule_type"] for c in cons)),
        "per_card_max_to_min_route_ratio": ratios,
        "routes_with_no_rows": sorted(f"{a}/{b}" for (a, b), n in expected.items() if not per_route[a][b]),
        "decoy_words_present_share": round(sum(bool(c["decoy_hit"]) for c in mis) / max(1, len(mis)), 4),
        "label_in_text_share": round(sum(c["label_in_text"] for c in cons) / max(1, len(cons)), 4),
        "options_per_row": dict(Counter(len(r["options"]) for r in bal)),
        "gold_position": dict(Counter(r["options"].index(r["gold"]) for r in bal)),
        "general_share": round(sum(r["gold"] == GENERAL for r in bal) / max(1, len(bal)), 4),
        "planned_slots": sum(expected.values()), "tokens_note": "CYGNET_SYSTEM + user message, Qwen3.5-4B tokenizer"})
    st["labels"] = {"n": len(bal), "labels": dict(Counter(r["gold"] for r in bal)),
                    "note": "route labels are card-specific; see per_card_max_to_min_route_ratio"}
    return st


def write_outputs(rows: list, stats: dict) -> dict:
    C.kp.write_jsonl(OUT_ROWS, rows)
    stats = dict(stats, output=str(OUT_ROWS), output_sha256=C.sha256_file(OUT_ROWS), n_rows=len(rows))
    C.kp.write_json(OUT_STATS, stats)
    return stats


def main(argv=None):
    argv = sys.argv[1:] if argv is None else argv
    if not argv or argv[0] not in ("tasks", "build"):
        raise SystemExit("usage: w8_complaint_routing.py tasks [--force] [--dry-run] | build [--dry-run]")
    if argv[0] == "tasks":
        return write_tasks(argv[1:])
    rows, stats = build()
    print(f"{T} rows {len(rows)} (before balance {stats['before_balance']['n']}) tasks answered "
          f"{sum(1 for v in stats['tasks'].values() if v.get('answered'))}/{len(stats['tasks'])} "
          f"tokens {stats.get('tokens_min_med_max_mean')} render drops {stats.get('n_render_drops')} "
          f"hard share {stats.get('hard_share')}")
    if "--dry-run" not in argv and rows:
        write_outputs(rows, stats)
    elif not rows:
        print(f"{T}: no rows (no usable answers yet); nothing written")
    return rows, stats


if __name__ == "__main__":
    main()
