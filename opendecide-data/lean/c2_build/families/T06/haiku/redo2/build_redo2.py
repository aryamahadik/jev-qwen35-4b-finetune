"""families/T06/haiku/redo2/build_redo2.py: T06 REDO-2 Haiku tasks for the two design-level pool blockers of the 13 Oct
pool freeze (pools/manifest.json "shortfalls"). A NEW file. New items, new opaque ids, new answer paths: no v1 task,
answer, key or pool and no existing file (haiku_author.py, extract_build.py, pool_freeze.py, plugin.py, G0_SPEC.md,
pinned lean/*.py, c_build) is changed. No gate bar, G0 target, check or gold semantics changes: every redo2 piece is
admitted by the v1 loaders' own checks (haiku_author.check_wording / check_freeform), G-LEX 2/2 and G3-H at 98% per
register. Haiku answers only flag; nothing here sets or reads a label or a gold. Every write goes through c2_kit.paths
(A38 guard and never-open guard).

Blockers and their fix (C2_DATA_SPEC 3.0, 6.3; G0_SPEC.md section 4 items 2 and 5, unchanged):
  B1  ch_end_withdraw wordings: 2 of 8 training admitted (4 of 11 with held out); the 2% per-wording cap needs >= 4
      training. Cause: v1 WORDING_BRIEF named the right "withdraw from (cancel) the purchase" and check_wording's anchor
      rule ('from (the )?purchase') drops "withdraw from the purchase" (7 of 7 drops; all 4 admitted say "cancel").
      Fix: a new brief that bans the word "from" outright, so the right is named "cancel the purchase / withdraw for any
      reason" (G0 4.5: name the legal right, never the notice or the anchor); the 4 admitted texts are listed as taken.
      12 training + 4 held out asked (G0 ask 8 + 3; deficit 6 + 1).
  B2  Mode F documents: 202 of 240 kept. 18 of the 38 drops carry an ITEM fact with a container word (pair of hiking
      boots, pair of custom-fit insoles, pair of made-to-measure curtains, box of pastries, fresh fruit box) that the
      author shortened ("the hiking boots"), so the G-SL fact-lock found 0 verbatim ITEMs (0 of the 212 other messages
      failed so). The v1 brief itself bans "pair" (rule 1) and "box" (rule 5) and never says the bans skip the values.
      Fix: (a) redo2 facts use only plain item names of plugin.ITEMS (no "<word> of ..." head, no "... box");
      (b) the brief says the word rules cover the author's own words only and the three values are copied whole;
      (c) it names the other v1 drop causes too (first name alone 9, "much" / "bunch" 10, "good afternoon" 2).
      The authoring facts only shape the text: at render time kit skin.fill_freeform replaces each brief value with the
      row's own slot, so no gold, slot pool, G3-H field or G0 fact changes. Asked per register: max(1.5 x deficit,
      deficit + 3).

Stages (each later stage rebuilds the earlier ones in memory and stops if a file on disk differs):
  author   (now) tasks/<task_id>.md (self-contained: answer path, inline answer contract, prompt, items), chunks/,
           prompts/, key/ (orchestrator only), manifest/, plan/, TASKS.json. answers/ is written only by the agents.
  extract  (after every author answer exists) the v1 checks with dedup against every v1 text; new wordings added to
           the frozen registry (pools/lexicon.json) and unit tested (a form that breaks a v1 form's unit test is
           dropped); G-LEX reads glex-r1 and glex-r2 (2/2, kind question, the full v1 meaning list incl. decoys) and
           the G3-H read g3h-r1 of the new documents, under extract/ (extract_build's prompts and task-file format).
  admit    (after every extraction answer exists) record the reads (a meaning outside the list rejects, as in v1),
           admit by lexicon.status, G3-H compare + 98% per register; write the SUPPLEMENT pools/redo2/ (new admitted
           wordings, new documents, quarantine, logs, merged lexicon) and its manifest.json with merged counts against
           the G0 asks (never lowered). pools/*.jsonl and pools/manifest.json are not touched.

Run from lean/ (each stage prints its counts; --write writes once):
  ../.venv/bin/python c2_build/families/T06/haiku/redo2/build_redo2.py author  [--write]
  ../.venv/bin/python c2_build/families/T06/haiku/redo2/build_redo2.py extract [--write]
  ../.venv/bin/python c2_build/families/T06/haiku/redo2/build_redo2.py admit   [--write]
"""
from __future__ import annotations

import hashlib
import json
import re
import sys
from collections import Counter
from pathlib import Path

HERE = Path(__file__).resolve().parent                  # families/T06/haiku/redo2
T06 = HERE.parents[1]
C2_BUILD = T06.parents[1]
if str(C2_BUILD) not in sys.path:
    sys.path.insert(0, str(C2_BUILD))

from c2_kit import chunker, g3h, paths  # noqa: E402
from c2_kit import lexicon as LX  # noqa: E402
from families.T06 import extract_build as E  # noqa: E402
from families.T06 import haiku_author as H  # noqa: E402
from families.T06 import plugin as P  # noqa: E402

FAMILY = "T06"
VERSION = "r2"
SEED = "t06-redo2-v1"
ROOT = HERE
EX_ROOT = HERE / "extract"
POOLS = T06 / "pools"
SUPP = POOLS / "redo2"
QF = "ch_end_withdraw"
N_WD_TRAIN, N_WD_HELD = 12, 4                            # G0 ask 8 + 3 (H.WORDING_PLAN); v1 admitted 2 + 2
WD_FLOOR = 4                                             # G0 4.5: each ch_end >= 4 (2% cap per wording)
FREE_PLAN = (("chat", 20, False), ("email", 9, False), ("ticket", 12, False), ("memo", 8, False),
             ("transcript", 7, True), ("letter", 5, True))   # deficits 13 / 6 / 8 / 5 / 4 / 2 (pools/manifest.json)
FREE_CHUNK = 31
LEX_READS = ("glex-r1", "glex-r2")
G3H_READ = "g3h-r1"

# ------------------------------------------------------------------------------------------------ B2 facts
# A container head ("pair of ...", "box of ...") or tail ("... box"): the v1 authors dropped the container word.
CONTAINER = re.compile(r"^[a-z-]+ of |(?:^| )box$")
PLAIN_ITEMS = {g: tuple(x for x in items if not CONTAINER.search(x)) for g, items in P.ITEMS.items()}
CONTAINER_ITEMS = tuple(x for items in P.ITEMS.values() for x in items if CONTAINER.search(x))


def free_facts(k: int) -> tuple:
    """(goods, facts) for the k-th redo2 Mode F item: plain item names only, the v1 goods cycle, new name pairs."""
    goods = H.GOODS_CYCLE[k % len(H.GOODS_CYCLE)]
    pool = PLAIN_ITEMS[goods]
    item = pool[(k * 7 + k // len(H.GOODS_CYCLE) + 3) % len(pool)]
    store = P.STORES[(k * 5 + k // 12 + 7) % len(P.STORES)]
    customer = f"{H.FIRST[(k * 11 + 5) % len(H.FIRST)]} {H.LAST[(k * 7 + k // len(H.LAST) + 2) % len(H.LAST)]}"
    return goods, {"CUSTOMER": customer, "ITEM": item, "STORE": store}


# ------------------------------------------------------------------------------------------------ prompts
WD_PROMPT = """You write questions for a reading test about online shopping. Every test item shows one returns case: \
a consumer law's rules for returns, the store's posted returns notice, an order record and a customer message. The \
reader answers a question about the case. You see none of the test items. Every item below asks for ONE question with \
the meaning given in the item: on which date the period of the customer's legal right to cancel the purchase for any \
reason ends (the final day of that period). The options, shown separately, are dates. The same law gives a second \
right, about faulty goods; that is a different question and is never named here.

Hard rules (a program throws away any question that breaks one):
1. One sentence ending with "?", 8-30 words, plain English. Refer to "the customer"; no names. A capital letter only \
on the first word.
2. Name the right with the verb "cancel" or "withdraw" together with the words "for any reason", and say "legal", \
"law" or "statutory". Ways to name it: "the customer's legal right to cancel the purchase for any reason", "the right \
the law gives the customer to withdraw for any reason", "the customer's statutory right to cancel for any reason".
3. Never write the word "from" anywhere in the question. So never "withdraw from the purchase", "counted from" or \
"runs from": with "withdraw", write "withdraw for any reason"; with "cancel", write "cancel the purchase" or "cancel \
this order".
4. Never say when the period starts or what it is counted by: none of the words delivery, delivered, possession, \
received, collected, ordered, "order date", "purchase date", "date of purchase", counted, counting, start, starts, \
begins.
5. Never mention the store's notice, sign, policy or promise, and never write "store's". Never mention faulty goods or \
rejecting.
6. Ask for the date or day the period ends: use the word "date" or "day", and "end", "run out" or "final day". Never \
write last, next, now, today, still, yet, already, soon or later.
7. No negation of any kind: not, n't, no, none, nobody, nothing, nowhere, never, neither, nor, cannot, without, \
except, unless, "other than", lack, fail.
8. No digits, number words or ordinals, no dates or month names, no hedges (maybe, perhaps, probably, likely). Never \
start the question with "May".
9. Ask about the case; never ask whether some answer is correct, and never mention options by letter.
10. Follow the item's style hint for the opening. Never repeat a question that the item lists as already taken, and \
make every question you write differ from every other one."""

WD_BRIEF = ("A multiple-choice question whose options are dates: on which date does the period of the customer's legal "
            "right to cancel the purchase for any reason end (its final day)? The law also calls this the right to "
            "withdraw for any reason.")
WD_RULE = ("Name that legal right with cancel or withdraw plus 'for any reason', and say 'legal', 'law' or "
           "'statutory'. Never write the word 'from'. Never mention the store's notice or promise, faulty goods, or "
           "the day the period is counted by. Say 'end', 'run out' or 'final day', never 'last'. No negation.")
WD_NAMES = ("the customer's legal right to cancel the purchase for any reason",
            "the right the law gives the customer to withdraw for any reason",
            "the customer's statutory right to cancel for any reason")         # the prompt's rule 2 phrasings

FREE_PROMPT = """You write short customer messages for a puzzle set about online shopping. Each item gives a \
register, a tone and three facts: CUSTOMER (the customer's full name), ITEM (what they bought) and STORE (the online \
store). Write ONE message per item, in which the customer says they want to send the item back to the store and that \
they bought it online (on the website, in the app or in the online shop). Nothing else about the case.

Fact rules (a program copies the three values out of your message letter by letter, and throws away any message in \
which a value is changed):
A. Write the CUSTOMER, ITEM and STORE values exactly as given, each at least once: every word of the value, in the \
same order, with the same spelling and the same capitals. Never shorten a value, never leave out a word of it, never \
make it plural and never put another word in its place: if ITEM is "electric toothbrush", write "the electric \
toothbrush", never "the toothbrush" or "the brush". Write "the" or "my" right before the item, never "a" or "an"; \
after its first mention, call the item "it". Never describe the item or say what kind of goods it is.
B. The customer's name appears only as the whole CUSTOMER value (first and last name together). Never write the first \
name alone or the last name alone, anywhere: also not in a greeting and also not in a reply from the support side \
(write "Hello" or "Hello there", never "Hello" followed by a first name). No other person's name, company name, brand \
or product name.
C. One block of text with no blank line (single line breaks are fine where the register uses them); at most about \
seventy words.
D. The word rules below apply to YOUR OWN words only. They never apply to the three values, which you always copy \
whole, whatever words they contain.
E. Thanks and greetings: use only "thank you", "thanks", "hello", "hi" or "dear". Never write "so much", "very much", \
"a bunch", "a lot", "good morning", "good afternoon" or "good evening".

""" + H.COMMON_BANS + """

Answer: a JSON list with one object per item: {"qid": "<the item's qid>", "text": "<the message>"}. Use \\n for line \
breaks inside the text. Every message must differ from every other message you write."""

FREE_RULE = ("Copy CUSTOMER, ITEM and STORE whole, letter for letter (every word of each value); name the customer "
             "only by the whole CUSTOMER value; after the first mention, call the item 'it'.")

CONTRACT = {"author_wording": ("the question (one sentence ending with ?)", "the question"),
            "author_freeform": ("the whole message (use \\n for a line break)", "the message")}


# ------------------------------------------------------------------------------------------------ author stage
def taken_wordings() -> list:
    """The admitted v1 ch_end_withdraw texts (pools/wordings.jsonl), sorted: the 'already taken' list of the brief."""
    rows = [json.loads(x) for x in (POOLS / "wordings.jsonl").read_text(encoding="utf-8").splitlines() if x.strip()]
    return sorted(r["text"] for r in rows if r["qform"] == QF)


def wording_items() -> tuple:
    taken = taken_wordings()
    items, plan = [], {}
    for i in range(N_WD_TRAIN + N_WD_HELD):
        held = i >= N_WD_TRAIN
        style = (H.STYLE_HELD[(i - N_WD_TRAIN) % len(H.STYLE_HELD)] if held
                 else H.STYLE_TRAIN[i % len(H.STYLE_TRAIN)])
        iid = f"t06r2.wording.{QF}.{i:03d}"
        items.append((iid, {"brief": WD_BRIEF, "slots": [],
                            "rules": [WD_RULE, f"Style hint: {style}.",
                                      "Already taken (never repeat these): " + " | ".join(taken)]}))
        plan[iid] = {"role": "wording", "qform": QF, "held_out": held, "style": style}
    return items, plan


def free_items() -> tuple:
    items, plan, k = [], {}, 0
    for ri, (reg, n, held) in enumerate(FREE_PLAN):
        for i in range(n):
            goods, facts = free_facts(k)
            k += 1
            tone = H.TONES[(i * 3 + ri + 1) % len(H.TONES)]
            iid = f"t06r2.free.r2-{reg}.{i:03d}"            # skin id T06-MF-r2-<reg>.<i>: never a v1 id
            items.append((iid, {"brief": f"Write {H.REGISTER_DESC[reg]} in which the customer wants to send the item "
                                         f"back. Tone: {tone}.",
                                "register": reg, "facts": dict(facts), "rules": H.FREEFORM_RULES[reg] + [FREE_RULE]}))
            plan[iid] = {"role": "freeform", "register": reg, "tone": tone, "held_out": held, "facts": facts,
                         "goods": goods}
    return items, plan


# name, chunker kind, items fn, prompt, forbid strings, max items, blocker, need
BATCH_SPECS = (
    ("wordings", "author_wording", wording_items, WD_PROMPT, H.QSTRINGS, 34, "B1",
     "ch_end_withdraw wordings: training admitted >= 4 (2% cap), G0 ask 8 training + 3 held out (have 2 + 2)"),
    ("freeform", "author_freeform", free_items, FREE_PROMPT, H.FORBID_ALL, FREE_CHUNK, "B2",
     "Mode F documents: G0 ask 50 per training register + 20 per held-out register (have chat 37, email 44, ticket 42, "
     "memo 45, transcript 16, letter 18)"),
)


def build_batches() -> dict:
    """{name: (TaskBatch, plan, spec)}: gold-free chunks, opaque qids, seeded order (chunker.make_batch)."""
    out = {}
    for spec in BATCH_SPECS:
        name, kind, fn, prompt, forbid, mx = spec[:6]
        items, plan = fn()
        b = chunker.make_batch(kind, FAMILY, items, seed=f"{SEED}|{name}", prompt=prompt, max_items=mx,
                               forbid_strings=forbid)
        out[name] = (b, plan, spec)
    return out


def task_text(b, chunk: dict, root: Path = ROOT) -> str:
    tid = chunk["task_id"]
    n = len(chunk["items"])
    qids = [it["qid"] for it in chunk["items"]]
    what, short = CONTRACT[b.kind]
    return "\n".join([
        f"# T06 redo2 authoring task {tid} (kind {b.kind})", "",
        "ANSWER FILE (write your whole answer here, and nowhere else, with the Write tool):", str(root / b.answer_path(tid)),
        "", "This file is self-contained: the instructions, the answer contract and the items are all below. Read this "
            "whole file. Do not open, list or search any other file or folder.", "",
        "ANSWER CONTRACT (exact; a program checks it):",
        f"- The answer file holds one JSON array with exactly {n} objects: one per item below, each item answered once, "
        f"in any order.",
        '- Each object has exactly two keys: "qid" and "text". No other keys.',
        "- \"qid\": copy the item's qid exactly, character for character (the letter q followed by ten letters or "
        f"digits, 11 characters in all). The qids of this task: {', '.join(qids)}.",
        f'- "text": one JSON string: {what}.',
        "- Valid JSON only: no text before or after the array, no markdown code fences, no comments. Inside JSON "
        'strings write a line break as \\n and a double quote as \\".',
        f'Literal example of the shape (the qid shown is the first real one): [{{"qid": "{qids[0]}", "text": '
        f'"<{short}>"}}, ...]', "",
        f"Task kind: {b.kind}; items: {n}; outputs expected: {n}.", "",
        "## Instructions", "", b.prompt.rstrip(), "",
        f"## Items ({n}; answer every item, keyed by its qid)", "", "```json",
        json.dumps(chunk["items"], ensure_ascii=False, indent=1), "```", ""])


def author_files(root: Path = ROOT) -> tuple:
    """({relative path: text}, TASKS.json object) for paths.write_files."""
    files, rows = {}, []
    for name, (b, plan, spec) in build_batches().items():
        files.update(b.files())
        files[f"plan/{b.batch_id}.json"] = json.dumps({"batch_id": b.batch_id, "name": name, "kind": b.kind,
                                                       "plan": plan}, indent=1, sort_keys=True) + "\n"
        for c in b.chunks:
            tid = c["task_id"]
            tfile = f"tasks/{tid}.md"
            text = task_text(b, c, root)
            files[tfile] = text
            ans = str(root / b.answer_path(tid))
            held = sum(1 for it in c["items"] if plan[b.key[it["qid"]]]["held_out"])
            rows.append({"task": name, "task_id": tid, "kind": b.kind, "blocker": spec[6], "need": spec[7],
                         "answer_field": "text", "task_file": str(root / tfile), "answer_file": ans,
                         "batch_id": b.batch_id, "prompt_sha": b.prompt_sha,
                         "task_sha256": hashlib.sha256(text.encode()).hexdigest(), "n_items": len(c["items"]),
                         "n_held_out_items": held, "outputs_expected": len(c["items"]),
                         "allowed_read": sorted({str(root / tfile)} | b.allowed(str(root), tid)[0]),
                         "allowed_write": [ans]})
    index = {
        "family": FAMILY, "version": VERSION, "seed": SEED, "stage": "redo2 author (design-level pool blockers B1, B2)",
        "g0_sha256": P.T06Plugin.G0_SHA256, "n_tasks": len(rows),
        "outputs_expected": sum(r["outputs_expected"] for r in rows),
        "notes": [
            "New items with new opaque ids and new answer paths; no v1 task, answer, key or pool is reused or changed.",
            "Each task file is self-contained (answer path, inline answer contract, prompt, items). The agent reads only "
            "its task file and writes only its answer file; audit each agent with audit.audit_jsonl(allowed_read, "
            "allowed_write) before its answers count.",
            "key/ and plan/ are orchestrator only. Next: build_redo2.py extract --write (G-LEX x2, G3-H x1), then admit.",
            "Labels: none. Haiku writes text pieces only; every gold still comes from solver A = solver B.",
        ],
        "tasks": rows}
    files["TASKS.json"] = json.dumps(index, ensure_ascii=False, indent=1) + "\n"
    files["answers/README.txt"] = ("Haiku answer files: one <task_id>.json per redo2 authoring task (see ../TASKS.json). "
                                   "Written only by the task agents.\n")
    return files, index


def check_author(files: dict, index: dict, root: Path = ROOT) -> list:
    """Problems with the author tasks (empty list = ready): leaks, ids, paths, fields, and the two fixes themselves."""
    probs = []
    batches = build_batches()
    for name, (b, plan, spec) in batches.items():
        forbid = spec[4]
        for c in b.chunks:
            tid = c["task_id"]
            text = files[f"tasks/{tid}.md"]
            low = text.lower()
            for f in forbid:
                if f and re.search(r"(?<![a-z0-9])" + re.escape(f.lower()) + r"(?![a-z0-9])", low):
                    probs.append(f"{tid}: task text holds forbidden string {f!r}")
            if any(i in text for i in b.key.values()):
                probs.append(f"{tid}: internal id in the task text")
            if not 1 <= len(c["items"]) <= chunker.MAX_ITEMS:
                probs.append(f"{tid}: {len(c['items'])} items")
            if str(root / b.answer_path(tid)) not in text:
                probs.append(f"{tid}: answer path missing")
            for it in c["items"]:
                if set(it) - {"qid"} - set(chunker.TASK_KINDS[b.kind]):
                    probs.append(f"{tid}: item fields {sorted(it)}")
            for pth in (root / f"tasks/{tid}.md", root / b.answer_path(tid)):
                if paths.never_open(pth):
                    probs.append(f"{tid}: never-open path {pth}")
    # B1: the brief's own phrasings pass the v1 check; the v1 failure mode still fails it (the gate is unchanged)
    meta = {"qform": QF, "held_out": False}
    for nm in WD_NAMES:
        q = f"On which date does {nm} end?"
        v = H.check_wording("probe", q, meta, "probe", "0" * 64, set())[1]
        if v:
            probs.append(f"B1 brief phrasing fails check_wording: {q!r} {v}")
    if not H.check_wording("probe", "On which date does the customer's legal right to withdraw from the purchase for "
                           "any reason end?", meta, "probe", "0" * 64, set())[1]:
        probs.append("B1: check_wording no longer drops 'from the purchase' (diagnosis or gate changed)")
    if not re.search(r'Never write the word "from"', WD_PROMPT):
        probs.append("B1: the brief does not ban 'from'")
    # B2: plain items only, values never inside each other, skin ids new
    v1_docs = [json.loads(x) for x in (POOLS / "documents.jsonl").read_text(encoding="utf-8").splitlines() if x]
    v1_skin_ids = {d["skin_id"] for d in v1_docs}
    _b, plan, _s = batches["freeform"]
    for iid, m in plan.items():
        f = m["facts"]
        if CONTAINER.search(f["ITEM"]) or f["ITEM"] not in PLAIN_ITEMS[m["goods"]]:
            probs.append(f"B2 {iid}: ITEM {f['ITEM']!r} is not a plain item of its goods type")
        for a in f.values():
            for b2 in f.values():
                if a != b2 and re.search(r"(?<!\w)" + re.escape(a) + r"(?!\w)", b2):
                    probs.append(f"B2 {iid}: {a!r} occurs inside {b2!r}")
        if f"T06-MF-{iid.split('.', 2)[2]}" in v1_skin_ids:
            probs.append(f"B2 {iid}: skin id collides with a v1 document")
    if set(CONTAINER_ITEMS) != {"pair of hiking boots", "pair of custom-fit insoles", "pair of made-to-measure curtains",
                                "box of pastries", "fresh fruit box"}:
        probs.append(f"B2: container items {CONTAINER_ITEMS} differ from the diagnosed five")
    if index["outputs_expected"] != N_WD_TRAIN + N_WD_HELD + sum(n for _r, n, _h in FREE_PLAN):
        probs.append("output count")
    return probs


def check_on_disk(root: Path, files: dict) -> list:
    return [rel for rel, text in sorted(files.items())
            if not (root / rel).is_file() or (root / rel).read_text(encoding="utf-8") != text]


# ================================================================================================ extract stage
def _load_author(b) -> dict:
    """{internal id: answer object} for one author batch. Stops if a file is missing or does not map to its items."""
    raw = {}
    for c in b.chunks:
        p = ROOT / b.answer_path(c["task_id"])
        if not p.is_file():
            raise SystemExit(f"STOP: redo2 author answer missing: {p}")
        try:
            raw[c["task_id"]] = json.loads(p.read_text(encoding="utf-8"))
        except (json.JSONDecodeError, UnicodeDecodeError) as e:
            raise SystemExit(f"STOP: redo2 author answer is not JSON: {p}: {e}")
    ans, probs = chunker.load_answers(b, raw)
    if probs:
        raise SystemExit(f"STOP: {b.batch_id}: answers do not map to their items: {probs[:3]}")
    return ans


def v1_seen() -> tuple:
    """(wording texts, document texts) of v1, normalised the way check_wording / check_freeform compare them: every
    v1 author answer (admitted or dropped) plus the frozen pool texts. A redo2 piece equal to one is a duplicate."""
    wd, ff = set(), set()
    for name, store, norm in (("wordings", wd, lambda t: " ".join(t.split()).lower()),
                              ("freeform", ff, lambda t: H._norm(t.strip()))):
        _b, _plan, ans, _p = H.load_answers_for(name)
        for a in ans.values():
            t = a.get("text") if isinstance(a, dict) else None
            if isinstance(t, str) and t.strip():
                store.add(norm(t))
    for line in (POOLS / "wordings.jsonl").read_text(encoding="utf-8").splitlines():
        if line.strip():
            wd.add(" ".join(json.loads(line)["text"].split()).lower())
    for line in (POOLS / "documents.jsonl").read_text(encoding="utf-8").splitlines():
        if line.strip():
            ff.add(H._norm(json.loads(line)["text"].strip()))
    return wd, ff


def run_checks(name: str, b, plan: dict, ans: dict, check, seen: set) -> tuple:
    """The v1 per-item check over one redo2 batch: (kept [(iid, obj)], drops)."""
    keep, drops = [], []
    tid_of = {b.key[q]: b.task_of[q] for q in b.key}
    for iid, a in sorted(ans.items()):
        text = a.get("text") if isinstance(a, dict) else None
        obj, v = check(iid, text, plan[iid], tid_of[iid], b.prompt_sha, seen)
        if v:
            drops.append({"stage": "author", "batch": name, "item": iid, "task_id": tid_of[iid],
                          "class": E._drop_class(v), "reasons": v})
        else:
            keep.append((iid, obj))
    return keep, drops


def frozen_registry() -> LX.LexiconRegistry:
    """The frozen v1 registry (pools/lexicon.json: admitted forms, every sem incl. the decoys), re-read and re-tested."""
    reg = LX.LexiconRegistry.from_json(json.loads((POOLS / "lexicon.json").read_text(encoding="utf-8")))
    bad = [fid for fid in reg.forms if reg.status(fid) != "admitted"]
    if bad:
        raise SystemExit(f"STOP: frozen v1 forms are not admitted after reload: {bad[:3]}")
    return reg


def merge_wordings(reg, kept: list) -> tuple:
    """Add the new wordings to the frozen registry. (new {form id: (iid, qform, text, held, tid, psha)}, drops). A
    duplicate text, a unit-test failure, or a form that makes a v1 form fail its unit test is dropped (v1 kept)."""
    old = set(reg.forms)
    new, drops = {}, []
    for iid, (q, text, held, tid, psha) in kept:
        try:
            f = reg.add(text, LX.question_sem(FAMILY, q), family=FAMILY, source="haiku", haiku_task_id=tid,
                        haiku_prompt_sha=psha, held_out=held)
            new[f.form_id] = (iid, q, text, held, tid, psha)
        except LX.LexiconError as e:
            drops.append({"stage": "lexicon", "batch": "wordings", "item": iid, "task_id": tid,
                          "class": "dedup" if "duplicate" in str(e) else "form", "reasons": [f"lexicon: {e}"]})

    def remove(fid: str, why: str) -> None:
        iid, _q, _t, _h, tid, _ps = new.pop(fid)
        del reg.forms[fid]
        reg._rx.clear()
        drops.append({"stage": "lexicon", "batch": "wordings", "item": iid, "task_id": tid, "class": "form",
                      "reasons": [why]})

    for _ in range(10):
        reg.unit_test_all()
        broken = [fid for fid in old if not reg.forms[fid].unit_ok]
        if not broken:
            break
        culprits = set()
        for ofid in broken:
            for vals in reg._samples(reg.forms[ofid]):
                sentence = f"Note: {reg.render(ofid, vals)}. Thanks."
                pbk = LX._params_by_kind({k: v.schema for k, v in vals.items()})
                culprits |= {n for n in new if reg._regex(reg.forms[n], pbk, False).search(sentence)}
        if not culprits:
            raise SystemExit(f"STOP: v1 forms fail their unit test with no redo2 culprit: {broken[:3]}")
        for n in sorted(culprits):
            remove(n, "breaks the unit test of a frozen v1 form (ambiguous span)")
    failing = [(fid, "; ".join(reg.forms[fid].unit_problems)[:200]) for fid in sorted(new)
               if not reg.forms[fid].unit_ok]
    for fid, why in failing:
        remove(fid, f"unit test: {why}")
    if failing:
        reg.unit_test_all()
    still = [fid for fid in list(old) + list(new) if not reg.forms[fid].unit_ok]
    if still:
        raise SystemExit(f"STOP: forms fail their unit test after the redo2 merge: {still[:3]}")
    return new, drops


def glex_batches(reg, new_ids: list) -> list:
    """[(read, kind, group, batch)]: glex-r1 and glex-r2 over the new wordings (kind question; 2/2). Same prompt and
    item shape as extract_build.glex_batches: the closed list of every question meaning (incl. the decoys), own seed
    and meaning order per read."""
    if len(new_ids) > E.GROUP:
        raise SystemExit("STOP: more than one G-LEX group of new wordings (redo2 asks at most 16)")
    meanings = sorted(s.meaning for s in reg.sems.values() if s.kind == "question")
    out = []
    for r, label in enumerate(LEX_READS, start=1):
        seed = f"{FAMILY}-glex-{VERSION}-r{r}-question-00"
        order = sorted(meanings, key=lambda m: hashlib.sha256(f"{seed}|{m}".encode()).hexdigest())
        items = [(fid, {"text": E.glex_text(reg, fid, r - 1)}) for fid in sorted(new_ids)]
        if not items:
            continue
        b = chunker.make_batch("extract_lex", FAMILY, items, seed=seed, prompt=E.glex_prompt(order), max_items=E.GROUP)
        out.append((label, "question", 0, b))
    return out


def g3h_batch(docs: list) -> tuple:
    """(batch or None, expected by iid): one independent G3-H read of every new document (extract_build's prompt)."""
    items, expected = [], {}
    for iid, sk, facts in docs:
        items.append((iid, g3h.extraction_item(sk.text, list(E.G3H_FIELDS))))
        expected[iid] = {"customer": facts["CUSTOMER"], "item": facts["ITEM"], "store": facts["STORE"]}
    if not items:
        return None, expected
    b = chunker.make_batch("extract_g3h", FAMILY, items, seed=f"{FAMILY}-g3h-{VERSION}-r1",
                           prompt=E.AGENT_RULES + E.G3H_TASK, max_items=E.G3H_MAX)
    return b, expected


def stage_extract() -> dict:
    files, index = author_files()
    probs = check_author(files, index)
    if probs:
        raise SystemExit("STOP: redo2 author check failed: " + "; ".join(probs[:5]))
    bad = check_on_disk(ROOT, files)
    if bad:
        raise SystemExit(f"STOP: redo2 author files on disk differ from the rebuild: {bad[:5]}")
    batches = build_batches()
    wd_seen, ff_seen = v1_seen()
    b, plan, _s = batches["wordings"]
    wd_keep, wd_drops = run_checks("wordings", b, plan, _load_author(b), H.check_wording, wd_seen)
    b, plan, _s = batches["freeform"]
    ff_keep, ff_drops = run_checks("freeform", b, plan, _load_author(b), H.check_freeform, ff_seen)
    docs = [(iid, sk, plan[iid]["facts"]) for iid, sk in ff_keep]
    reg = frozen_registry()
    new, lex_drops = merge_wordings(reg, wd_keep)
    glex = glex_batches(reg, sorted(new))
    g3b, g3_expected = g3h_batch(docs)
    ex_batches = glex + ([(G3H_READ, "extract_g3h", 0, g3b)] if g3b else [])
    ex_files, rows = E._task_rows(EX_ROOT, ex_batches)
    st = {"batches": batches, "wd_keep": wd_keep, "docs": docs, "reg": reg, "new": new, "glex": glex, "g3": g3b,
          "g3_expected": g3_expected, "drops": wd_drops + ff_drops + lex_drops, "ex_batches": ex_batches}
    counts = extract_counts(st)
    ex_files["answers/README.txt"] = ("Haiku answer files: one <task_id>.json per redo2 extraction task (see "
                                      "../TASKS.json). Written only by the task agents.\n")
    ex_files["TASKS.json"] = json.dumps({
        "family": FAMILY, "version": VERSION, "stage": "redo2 extract (new wordings: G-LEX 2/2; new Mode F: G3-H)",
        "gate": "G-LEX 2/2 (question); G3-H single read, 98% per register", "counts": counts,
        "n_tasks": len(rows), "tasks": rows}, ensure_ascii=False, indent=1) + "\n"
    ex_files["lint_log.json"] = json.dumps({"counts": counts, "drops": st["drops"]}, ensure_ascii=False,
                                           indent=1) + "\n"
    ex_files["pool/wordings.jsonl"] = "".join(json.dumps(
        {"form_id": fid, "item": iid, "qform": q, "text": t, "held_out": h, "haiku_task_id": tid,
         "haiku_prompt_sha": ps}, ensure_ascii=False) + "\n" for fid, (iid, q, t, h, tid, ps) in sorted(new.items()))
    ex_files["pool/documents.jsonl"] = "".join(json.dumps(
        {"pid": iid, "skin_id": sk.skin_id, "text": sk.text, "register": sk.register, "facts": dict(facts),
         "held_out": bool(sk.held_out), "haiku_task_id": sk.haiku_task_id, "haiku_prompt_sha": sk.haiku_prompt_sha},
        ensure_ascii=False) + "\n" for iid, sk, facts in docs)
    ex_files["pool/g3h_expected.json"] = json.dumps(g3_expected, ensure_ascii=False, indent=1, sort_keys=True) + "\n"
    st["files"], st["rows"], st["counts"] = ex_files, rows, counts
    return st


def extract_counts(st: dict) -> dict:
    _b, wplan, _s = st["batches"]["wordings"]
    new = st["new"]
    return {
        "author_items": {n: len(b.key) for n, (b, _p, _s) in st["batches"].items()},
        "drops_by_batch_and_class": dict(Counter(f"{d['batch']}/{d['class']}" for d in st["drops"])),
        "wordings_unit_ok_new": len(new),
        "wordings_new_training": sum(1 for v in new.values() if not v[3]),
        "wordings_new_held_out": sum(1 for v in new.values() if v[3]),
        "documents_kept_by_register": dict(Counter(sk.register for _i, sk, _f in st["docs"])),
        "glex_items_per_read": {lab: sum(len(c["items"]) for c in b.chunks) for lab, _k, _g, b in st["glex"]},
        "g3h_items": len(st["g3_expected"]),
        "extraction_tasks": sum(len(b.chunks) for _l, _k, _g, b in st["ex_batches"]),
    }


# ================================================================================================ admit stage
def _load_reads(ex_batches: list) -> tuple:
    """{read: (batch, {internal id: answer})}, problems. A missing answer FILE stops; an unanswered item is a problem
    that is recorded (G-LEX: fewer reads, never admitted; G3-H: 'no answer', dropped), as in pool_freeze v1."""
    reads, probs = {}, []
    for label, _kind, _gi, b in ex_batches:
        raw = {}
        for c in b.chunks:
            p = EX_ROOT / b.answer_path(c["task_id"])
            if not p.is_file():
                raise SystemExit(f"STOP: redo2 extraction answer missing: {p}")
            try:
                raw[c["task_id"]] = json.loads(p.read_text(encoding="utf-8"))
            except (json.JSONDecodeError, UnicodeDecodeError) as e:
                raise SystemExit(f"STOP: redo2 extraction answer is not JSON: {p}: {e}")
        ans, pr = chunker.load_answers(b, raw)
        probs += [f"{label} {b.batch_id}: {x}" for x in pr]
        reads[label] = (b, ans)
    return reads, probs


def _rows(path: Path) -> list:
    return [json.loads(x) for x in path.read_text(encoding="utf-8").splitlines() if x.strip()]


def merged_targets(new_wordings: list, new_docs: list) -> list:
    """The G0 asks (never lowered) over v1 pools + the redo2 supplement, for the two blockers and their totals."""
    wds = _rows(POOLS / "wordings.jsonl") + new_wordings
    docs = _rows(POOLS / "documents.jsonl") + new_docs
    out = []

    def add(item, target, n, source):
        out.append({"item": item, "target": target, "admitted": n, "shortfall": max(0, target - n), "source": source})

    tr, ho = H.WORDING_PLAN[QF]
    add(f"wording {QF}, training", tr, sum(1 for x in wds if x["qform"] == QF and not x["held_out"]),
        f"G0 4.5 ask ({tr} training)")
    add(f"wording {QF}, held out", ho, sum(1 for x in wds if x["qform"] == QF and x["held_out"]),
        f"G0 4.5 ask ({ho} held out)")
    add(f"wording {QF}, training floor (2% cap per wording)", WD_FLOOR,
        sum(1 for x in wds if x["qform"] == QF and not x["held_out"]), "G0 4.5: each ch_end >= 4")
    add("wordings, training", sum(t for t, _h in H.WORDING_PLAN.values()), sum(1 for x in wds if not x["held_out"]),
        "G0 4.5: 106 training")
    add("wordings, held out", sum(h for _t, h in H.WORDING_PLAN.values()), sum(1 for x in wds if x["held_out"]),
        "G0 4.5: 29 held out")
    add("documents (Mode F), all", 240, len(docs), "G0 4.2: 240 asked")
    add("documents (Mode F), held out", 40, sum(1 for x in docs if x["held_out"]), "G0 4.2: 40 asked held out")
    for r in H.FREEFORM_TRAIN:
        add(f"documents, register {r}", H.N_FREE_TRAIN, sum(1 for x in docs if x["register"] == r and not x["held_out"]),
            "per-register ask (50 each, G0 4.2)")
    for r in H.FREEFORM_HELD:
        add(f"documents, held-out register {r}", H.N_FREE_HELD,
            sum(1 for x in docs if x["register"] == r and x["held_out"]), "per-register ask (20 each, G0 4.2)")
    return out


def stage_admit(write: bool) -> dict:
    paths.require_a38()
    st = stage_extract()
    bad = check_on_disk(EX_ROOT, st["files"])
    if bad:
        raise SystemExit(f"STOP: redo2 extraction files on disk differ from the rebuild: {bad[:5]}")
    reads, probs = _load_reads(st["ex_batches"])
    reg, new = st["reg"], st["new"]
    glex_log = []
    for label, _kind, _gi, _b in st["glex"]:
        b, ans = reads[label]
        qid_of = {internal: qid for qid, internal in b.key.items()}
        for fid in sorted(ans):
            meaning = ans[fid].get("meaning") if isinstance(ans[fid], dict) else None
            sem = reg.meaning_to_sem("question", meaning) if isinstance(meaning, str) else None
            reg.record_extraction(fid, f"haiku-{VERSION}-{label}", sem)
            glex_log.append({"form_id": fid, "kind": "question", "read": label, "task_id": b.task_of[qid_of[fid]],
                             "meaning": meaning, "sem_id": sem, "agrees": sem == reg.forms[fid].sem_id})
    status = {fid: reg.status(fid) for fid in new}
    adm_new = sorted(fid for fid, s in status.items() if s == "admitted")

    fields = list(E.G3H_FIELDS)
    reg_of = {iid: sk.register for iid, sk, _f in st["docs"]}
    g3_ans = reads[G3H_READ][1] if G3H_READ in reads else {}
    results, g3log = [], []
    for iid in sorted(st["g3_expected"]):
        if iid not in g3_ans:
            ok, diffs = False, ["no answer"]
        else:
            ok, diffs = g3h.compare(st["g3_expected"][iid], g3_ans[iid], fields)
        results.append((reg_of[iid], iid, ok))
        g3log.append({"item": iid, "register": reg_of[iid], "ok": ok, "diffs": diffs})
    rep = g3h.template_report(results)
    drop = set(rep["drop_rows"])
    v1_g3 = json.loads((POOLS / "manifest.json").read_text(encoding="utf-8"))["summary"]["g3h"]["per_register"]
    combined = {}
    for r in sorted(set(v1_g3) | set(rep["templates"])):
        a, c = v1_g3.get(r, {"n": 0, "ok": 0}), rep["templates"].get(r, {"n": 0, "ok": 0})
        n, ok = a["n"] + c["n"], a["ok"] + c["ok"]
        combined[r] = {"n": n, "ok": ok, "rate": round(ok / n, 4) if n else 1.0,
                       "below_bar": bool(n) and ok / n < g3h.PASS_RATE}

    wordings = [{"form_id": fid, "qform": new[fid][1], "text": new[fid][2], "held_out": bool(new[fid][3]),
                 "haiku_task_id": new[fid][4], "haiku_prompt_sha": new[fid][5],
                 "reads": [list(e) for e in reg.forms[fid].extractions]} for fid in adm_new]
    documents = [{"pid": iid, "skin_id": sk.skin_id, "text": sk.text, "register": sk.register, "facts": dict(facts),
                  "held_out": bool(sk.held_out), "haiku_task_id": sk.haiku_task_id,
                  "haiku_prompt_sha": sk.haiku_prompt_sha} for iid, sk, facts in st["docs"] if iid not in drop]
    for fid in [f for f in new if status[f] != "admitted"]:
        reg.forms.pop(fid)
    reg._rx.clear()
    merged = reg.to_json()
    merged["forms"] = [f for f in merged["forms"] if f["status"] == "admitted"]
    merged["note"] = ("T06 lexicon after redo2: the frozen v1 admitted forms plus the redo2 admitted wordings (G-LEX). "
                      "Every sem is kept: the closed meaning lists and the never-generated decoys.")
    back = LX.LexiconRegistry.from_json(merged)
    if [k for k in back.forms if back.status(k) != "admitted"]:
        raise SystemExit("STOP: merged lexicon round trip: a form is not admitted after reload")
    new_obj = dict(merged, forms=[f for f in merged["forms"] if f["form_id"] in set(adm_new)],
                   note="T06 redo2: the newly admitted forms only (also inside lexicon_merged.json).")

    quar = [dict(d) for d in st["drops"]]
    for fid, s in sorted(status.items()):
        if s != "admitted":
            quar.append({"stage": "glex", "form_id": fid, "item": new[fid][0], "class": s, "text": new[fid][2],
                         "held_out": bool(new[fid][3]),
                         "reads": [e for e in glex_log if e["form_id"] == fid]})
    quar += [{"stage": "g3h", "item": x["item"], "register": x["register"], "class": "mismatch",
              "reasons": x["diffs"]} for x in g3log if not x["ok"]]
    quar += [{"stage": "g3h-template", "register": t, "class": "under 98% pass", "rate": rep["templates"][t]["rate"]}
             for t in rep["quarantined"]]
    tg = merged_targets(wordings, documents)
    summary = {
        "write": write, "read_problems": probs, "new_wording_status": dict(Counter(status.values())),
        "new_wordings_admitted": {"training": sum(1 for w in wordings if not w["held_out"]),
                                  "held_out": sum(1 for w in wordings if w["held_out"])},
        "new_documents_kept_by_register": dict(Counter(d["register"] for d in documents)),
        "g3h_redo2": {t: {k: d[k] for k in ("n", "ok", "rate", "quarantined")} for t, d in rep["templates"].items()},
        "g3h_combined_with_v1": combined, "quarantine_entries": len(quar),
        "targets": tg, "shortfalls": [t for t in tg if t["shortfall"] > 0],
        "ch_end_withdraw_thinning_needed": next(t for t in tg if "floor" in t["item"])["shortfall"] > 0,
    }
    if not write:
        return summary
    if SUPP.exists():
        raise FileExistsError(f"{SUPP} exists: the T06 redo2 supplement is frozen once")
    files = {"wordings.jsonl": wordings, "documents.jsonl": documents, "quarantine.jsonl": quar,
             "extraction_log.jsonl": glex_log, "g3h_log.jsonl": g3log}
    shas = {}
    for name, rows in files.items():
        paths.write_jsonl(SUPP / name, rows)
        shas[name] = {"sha256": hashlib.sha256((SUPP / name).read_bytes()).hexdigest(), "rows": len(rows)}
    for name, obj in (("lexicon_merged.json", merged), ("lexicon_new.json", new_obj)):
        paths.write_json(SUPP / name, obj)
        shas[name] = {"sha256": hashlib.sha256((SUPP / name).read_bytes()).hexdigest(), "forms": len(obj["forms"])}

    def sha(p: Path) -> str:
        return hashlib.sha256(p.read_bytes()).hexdigest()

    manifest = {
        "family": FAMILY, "supplement": "redo2", "a38_frozen": paths.a38_frozen(),
        "base_manifest_sha256": sha(POOLS / "manifest.json"),
        "g0_sha256": sha(T06 / "G0_SPEC.md"), "matches_plugin_G0_SHA256": sha(T06 / "G0_SPEC.md") == P.T06Plugin.G0_SHA256,
        "inputs": {"author_tasks": str(ROOT / "TASKS.json"), "author_tasks_sha256": sha(ROOT / "TASKS.json"),
                   "extract_tasks": str(EX_ROOT / "TASKS.json"), "extract_tasks_sha256": sha(EX_ROOT / "TASKS.json")},
        "code": {str(p.relative_to(T06)): sha(p) for p in (HERE / "build_redo2.py", T06 / "haiku_author.py",
                                                          T06 / "extract_build.py", T06 / "pool_freeze.py",
                                                          T06 / "plugin.py")},
        "pool_files": shas, "summary": summary,
        "decisions": [
            "Supplement only: pools/*.jsonl and pools/manifest.json (v1) are unchanged. The generator reads the v1 pools "
            "plus pools/redo2/ (lexicon_merged.json replaces pools/lexicon.json as the registry; wordings and documents "
            "are v1 rows plus the redo2 rows).",
            "Admission = the v1 rules: check_wording / check_freeform, G-LEX every read agrees (2 for question), G3-H "
            "mismatches dropped and 98% per register on the redo2 documents. g3h_combined_with_v1 is reported; a "
            "register below 98% there is an OPEN DECISION for the lead, never silently passed.",
            "If the ch_end_withdraw training floor (>= 4) is still short, ch_end_withdraw rows must be thinned so no "
            "wording exceeds 2% of the family (G0 section 3 share change + new G0 sha): ch_end_withdraw_thinning_needed.",
            "Access audit (audit.audit_jsonl with each task's allowed_read / allowed_write) must pass for every redo2 "
            "author and extraction agent before these answers count.",
        ]}
    paths.write_json(SUPP / "manifest.json", manifest)
    return summary


# ================================================================================================ main
def main(argv: list) -> int:
    stage = argv[0] if argv and not argv[0].startswith("-") else "author"
    write = "--write" in argv
    if stage == "author":
        files, index = author_files()
        probs = check_author(files, index)
        if probs:
            print("\n".join(probs))
            return 1
        if write:
            if (ROOT / "TASKS.json").exists():
                raise FileExistsError(f"{ROOT}/TASKS.json exists: the redo2 author tasks are written once")
            paths.write_files(ROOT, files)
        else:
            on_disk = check_on_disk(ROOT, files) if (ROOT / "TASKS.json").exists() else None
            print(f"on disk differs: {on_disk}" if on_disk else "on disk: same bytes" if on_disk == [] else
                  "on disk: not written")
        for r in index["tasks"]:
            print(f"{r['blocker']} {r['kind']:16s} items {r['n_items']:3d} (held out {r['n_held_out_items']:2d}) "
                  f"{r['task_file']} -> {r['answer_file']}")
        print(f"{index['n_tasks']} tasks, {index['outputs_expected']} outputs expected; written: {write}")
        return 0
    if stage == "extract":
        st = stage_extract()
        if write:
            if (EX_ROOT / "TASKS.json").exists():
                raise FileExistsError(f"{EX_ROOT}/TASKS.json exists: the redo2 extraction tasks are written once")
            paths.write_files(EX_ROOT, st["files"])
        print(json.dumps(st["counts"], indent=1, ensure_ascii=False))
        for r in st["rows"]:
            print(f"{r['read']:8s} {r['kind']:9s} items {r['n_items']:3d} {r['task_file']} -> {r['answer_file']}")
        print(f"written: {write}")
        return 0
    if stage == "admit":
        print(json.dumps(stage_admit(write), indent=1, ensure_ascii=False, default=str))
        return 0
    print(__doc__)
    return 2


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
