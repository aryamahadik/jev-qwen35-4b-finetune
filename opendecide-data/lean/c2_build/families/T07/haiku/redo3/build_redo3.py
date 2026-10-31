#!/usr/bin/env python3
"""families/T07/haiku/redo3/build_redo3.py: T07 REDO-3, the last two Haiku authoring tasks (a NEW file).

Why: after redo2 the independent verdict (families/T07/merged_pools.py, STAGE_A3_REPORT.json) leaves exactly two G0
target lines short, and every other line, the G-LEX gate and the G3-H bar are met:
  * Question wordings, training, yn_misses: 19 admitted of 20 (short by 1). redo2 showed the cause: every 'forfeit'
    wording was rejected by G-LEX (readers pick yn_fails_to / yn_not_gets), 'lose out on' wordings were admitted at
    11 of 14. Fix: ONE new author_wording task for yn_misses that allows 'lose out on' only (G0 S19's antonym predicate,
    R2). The meaning list of the closed G-LEX choices is unchanged.
  * Packs asked (G0 section 4): 49 kept of 60 (short by 11). 10 of the 11 v1 losses were one spelling rule of
    authoring.lint_pack (a customer name with a hyphen followed by a lower-case letter, or a capital inside a name:
    "Sung-min Park", "Catriona MacLeod"), 1 was check_packs (a store name holding a seed region word). Fix: ONE new
    author_pack task with the v1 fields and checks unchanged, the spelling patterns spelled out, and the taken words
    and store names listed (R3 for packs).

Asks are ~50% over the gap (ask = max(ceil(1.5 x gap), gap + 2); the +2 floor is the smallest spare that keeps a
one-piece gap from depending on one lucky piece): wordings 3 (gap 1), packs 17 (gap 11). No gate bar, G0 target, lint
check, gold or label changes; no pack word or wording is read from or written to any pool here.

(a) Pending reads: every chunk of every T07 round (v1 author / extract, redo2 author / extract) has its answer file, so
there is NO pending G-LEX or G3-H read to re-wrap (checked below and recorded in TASKS.json "pending_reads"). The G-LEX
2/2 reads of the new yn_misses wordings can only be built after their text exists (build_redo2-style extract stage).

Each task file is self-contained: answer path, answer contract with a literal JSON example, the full prompt, the items.
The agent reads only its task file and writes only its answer file. key/ and plan/ are orchestrator only. Every write
goes through c2_kit.paths (A38 guard and never-open guard).

Run from lean/c2_build (set PYTHONDONTWRITEBYTECODE=1 or pass -B):
  .venv/bin/python -B families/T07/haiku/redo3/build_redo3.py author [--write]    # build (and write) the task files
  .venv/bin/python -B families/T07/haiku/redo3/build_redo3.py validate            # strict contract check of answers
"""
from __future__ import annotations

import argparse
import hashlib
import json
import math
import random
import re
import sys
from pathlib import Path

sys.dont_write_bytecode = True
HERE = Path(__file__).resolve().parent                   # families/T07/haiku/redo3
T07 = HERE.parents[1]
C2_BUILD = T07.parents[1]
if str(C2_BUILD) not in sys.path:
    sys.path.insert(0, str(C2_BUILD))

from c2_kit import chunker, paths  # noqa: E402
from families.T07 import authoring as A  # noqa: E402
from families.T07 import merged_pools as MP  # noqa: E402
from families.T07 import plugin as P  # noqa: E402
from families.T07 import validate_answers as VA  # noqa: E402
from families.T07.haiku.redo2 import build_redo2 as R2  # noqa: E402

FAMILY = "T07"
VERSION = "r3"
SEED = "t07-redo3-v1"
ROOT = HERE
HAIKU = T07 / "haiku"
G0_SHA = P.T07Plugin.G0_SHA256_AUTHORED
# The pools redo3 was authored against: v1 + redo2. merged_pools.load() now also merges the redo3 supplement (admit_redo3.py),
# so every pool read in the redo3 builders names the baseline, and the task files stay reproducible after the redo3 freeze.
BASELINE = "redo2"

# the two shortfall lines this round closes (merged_pools.verdict item names)
LINE_WORD = "wordings training yn_misses"
LINE_PACKS = "packs asked (G0 section 4)"
# rounds whose chunks must all have answers (a chunk without one is a pending read)
ROUNDS = {"v1-author": HAIKU / "author", "v1-extract": HAIKU / "extract", "redo2-author": HAIKU / "redo2",
          "redo2-extract": HAIKU / "redo2" / "extract"}


def ask(gap: int) -> int:
    """Pieces asked for a gap: ~50% over it, at least 2 spare."""
    return 0 if gap <= 0 else max(math.ceil(1.5 * gap), gap + 2)


# ------------------------------------------------------------------------------------------------ the gaps
def gaps() -> dict:
    """{line: short_by} from the independent verdict over the merged v1 + redo2 pools. Stops if any other line is short:
    this round only writes the two tasks below."""
    v = MP.verdict(MP.load(through=BASELINE))
    short = {s["item"]: s["short_by"] for s in v["shortfalls"]}
    extra = sorted(set(short) - {LINE_WORD, LINE_PACKS})
    if extra:
        raise SystemExit(f"STOP: shortfalls beyond the two redo3 lines: {extra}")
    return {"wording": short.get(LINE_WORD, 0), "packs": short.get(LINE_PACKS, 0)}


def pending_reads() -> dict:
    """{round: {"tasks", "answers", "pending": [task ids with a chunk but no answer file]}}: (a) of the brief."""
    out = {}
    for name, root in ROUNDS.items():
        chunks = sorted(p.stem for p in (root / "chunks").glob("*.json"))
        have = {p.stem for p in (root / "answers").glob("*.json")}
        out[name] = {"chunks": len(chunks), "answers": len(have & set(chunks)),
                     "pending": [c for c in chunks if c not in have]}
    return out


# ------------------------------------------------------------------------------------------------ wording task
# R2 verbs: v1 'go short of' / 'be shut out of' read as yn_fails_to; redo2 'forfeit' read as yn_fails_to / yn_not_gets
# (13 of 13 rejected); 'lose out on' was admitted 11 of 14. Redo3 allows 'lose out on' only.
YN_MISSES_R3 = ("yes/no: does order {ORDER_ID} from {CUSTOMER} lose out on {ASKED} under the advertised terms? For the "
                "outcome use exactly this verb phrase, in any tense: 'lose out on' (loses out on, lost out on). No "
                "other verb for the outcome, and NO negation word at all (not 'without', not 'denied', not 'fail')")
# redo2 openings already in the pool (training, same style): a repeat is dropped as a duplicate, so ask for other frames
USED_OPENINGS = ("Under the advertisement and its fine print, does ...", "Given the advertisement and its fine print, will ...",
                 "Measured against the advertisement and its fine print, does ...",
                 "Taking the advertisement and its fine print into account, has ...",
                 "Does order ... lose out on ... according to the advertisement and its fine print?")
WORD_STYLE = A.WORD_STYLES[1]            # "refer to 'the advertisement and its fine print'": 5 of 5 admitted in redo2
SLOT_TEXT = {"CUSTOMER": "the customer's full name", "ORDER_ID": "the order's code",
             "ASKED": "the name of one advertised benefit"}


def wording_items(n: int) -> tuple:
    iid = "t07r3.word.yn_misses.training.00"
    rules = [f"{n} wordings with exactly this meaning", "each listed placeholder exactly once",
             "the outcome verb phrase is 'lose out on' in every wording",
             "open each wording differently from the others and from these already used openings: "
             + "; ".join(f"'{o}'" for o in USED_OPENINGS)]
    item = {"brief": {"meaning": YN_MISSES_R3, "style": WORD_STYLE, "how_many": n},
            "slots": {k: SLOT_TEXT[k] for k in A.wording_slots("yn_misses")}, "rules": rules}
    plan = {"piece": "wording", "qform": "yn_misses", "held_out": False, "outputs": n, "style": WORD_STYLE,
            "line": LINE_WORD}
    return [(iid, item)], {iid: plan}


# ------------------------------------------------------------------------------------------------ pack task
def taken_stores() -> list:
    return sorted(set(P.STORES) | set(P.STORES_HELD) | {p["store"] for p in R2.kept_packs()})


TAKEN_WORDS = R2.A.SURFACE_WORDS | R2.PACK_WORDS
_PH = re.compile(r"\{[A-Za-z0-9_|]+\}")
_FUNCTION_WORDS = frozenset("""a an and are as at be but by for from has have he her his i if in is it its me my no not of
on or our she so than that the their them then there these they this to up us was we were what when which who will with
you your""".split())
EXAMPLE_PACK = {"store": "Wrenfield Emporium", "ladder": ["Cog", "Crown", "Pendulum"],
                "regions": ["Tolverra", "Mistlecombe", "Harrowdene", "Pellimar"],
                "categories": ["pocket watches", "watch straps", "clock movements"],
                "customers": ["Imogen Fairweather", "Kwame Boateng", "Anika Rao", "Tomas Lindqvist"]}


def pool_words(pools: dict | None = None) -> frozenset:
    """Every word of the admitted pool texts: skins, Mode F bodies (store name and fine-print run removed), attack
    lines, wordings and condition sentences (placeholders removed)."""
    pools = pools or MP.load(through=BASELINE)
    words = set()
    for k in ("skins", "attacks", "wordings"):
        for x in pools[k]:
            words |= set(A._words(_PH.sub(" ", x["text"])))
    for d in pools["documents"]:
        body = d["text"].replace(d["run"], " ").replace(d["store"], " ")
        words |= set(A._words(_PH.sub(" ", body)))
    for f in pools["lexicon"]:
        if f["status"] == "admitted":
            words |= set(A._words(_PH.sub(" ", f["text"])))
    return frozenset(words)


def pool_vocab(pools: dict | None = None) -> frozenset:
    """pool_words that are not already taken words or plain function words. A level, region or category word equal to
    one of them would put a surface word into an already admitted piece (G0 section 4: pieces hold no SURFACE_WORDS
    word), so the pack prompt lists them."""
    return frozenset(pool_words(pools) - TAKEN_WORDS - _FUNCTION_WORDS)


def pack_pool_collisions(pack: dict, pools: dict | None = None) -> list:
    """The level, region and category words of a pack that already appear in an admitted pool text (empty = the pack
    can join the frozen packs without putting a surface word into an admitted piece). For the admit stage."""
    words = pool_words(pools)
    return sorted({w for f in ("ladder", "regions", "categories") for v in pack[f] for w in A._words(v)} & words)


def pack_prompt(vocab: frozenset | None = None) -> str:
    vocab = pool_vocab() if vocab is None else vocab
    return A.COMMON + f"""
TASK: invent one STORE PACK per item: the invented values a fictional shop of the item's kind uses in its adverts and
order records. Fit every value to the item's shop kind.

A program checks the spelling of every value, and a pack that breaks one rule is thrown away whole. Write plain
English letters only (a-z and A-Z): no accents, hyphens, apostrophes, ampersands, digits or other marks anywhere.

Fields of "pack" (all invented: no real company, brand, product line, person or place):
- "store": the shop's name, two or three words (such as "Wrenfield Emporium"). Each word is one capital letter
  followed by lowercase letters only. It must not contain a word that names a product category, a delivery region, a
  membership level or a price status, and it must not contain a taken word (list below).
- "ladder": the shop's membership levels, lowest first, exactly as many as the item asks (3 or 4). Each level is ONE
  word: one capital letter followed by lowercase letters only. The order from lowest to highest must be easy to follow
  (metals, gems, sizes, trees by height, stars by brightness ...). Avoid the common ladders Bronze/Silver/Gold/Platinum,
  Basic/Plus/Premier/Elite and Green/Blue/Black.
- "regions": exactly four invented delivery-region names, ONE word each (one capital letter followed by lowercase
  letters only), sounding like places but not real ones (such as "Tolverra").
- "categories": exactly three product categories the shop sells: lowercase letters only, one or two words separated by
  one space (never a hyphen), plural or mass nouns (such as "pocket watches"). Never a price word or a status such as
  clearance, sale, refurbished or open box.
- "customers": exactly four invented customers' full names. Each name is exactly two words, a given name and a family
  name, and each word is one capital letter followed by lowercase letters only. No hyphen, no apostrophe, no accent, no
  capital letter inside a word, no initial and no third word. Right: "Marisol Vega", "Oluwaseun Adeyemi". Wrong:
  "Sung-min Park", "Catriona MacLeod", "Zoe O'Neil", "Maria de la Cruz". Vary the cultural origin; no famous people.
No digits anywhere. No value may contain a negation word (such as no, not, never, none, nobody). All values within a
pack differ, and no value repeats a value of another item in this task or of the example.

Taken words. Each word below is already a region, a membership level or a product category word in other shops' packs
or in the seed lists. None of them may appear anywhere in your packs: not as a level, a region or a category word, and
not inside a store name or a customer's name (a pack holding one is thrown away):
{R2._list(TAKEN_WORDS)}

Words in use. Each word below already appears in the dataset's advertisement copy, notes, questions or small-print
sentences. No level, no region name and no category word may be one of them (a pack holding one is thrown away); store
names and customers' names may use them:
{R2._list(vocab)}

Taken store names (never reuse or imitate one): {", ".join(taken_stores())}.

{R2.CHECK.replace("every word of every text", "every word of every value")}
"""


def pack_items(n: int) -> tuple:
    """n pack items: the dropped v1 shop kinds first (the 'same briefs'), then spare kinds of kept packs; ladder sizes
    chosen to even out the kept 3-level / 4-level counts (label-blind: no gold exists on a pack)."""
    kept = R2.kept_packs()
    used = sorted(int(p["internal_id"][-2:]) for p in kept)
    dropped = sorted(set(range(len(A.PACK_SETTINGS))) - set(used))
    idx = dropped[:n]
    if len(idx) < n:
        rng = random.Random(f"{SEED}|extra-kinds")
        idx += sorted(rng.sample(used, n - len(idx)))
    n3 = sum(len(p["ladder"]) == 3 for p in kept)
    n4 = len(kept) - n3
    order = sorted(range(len(idx)), key=lambda i: hashlib.sha256(f"{SEED}|ladder|{idx[i]}".encode()).hexdigest())
    size = {}
    for i in order:
        size[i] = 3 if n3 <= n4 else 4
        n3, n4 = n3 + (size[i] == 3), n4 + (size[i] == 4)
    items, plan = [], {}
    for i, k in enumerate(idx):
        iid = f"t07r3.pack.{i:02d}"
        items.append((iid, {"brief": {"shop_kind": A.PACK_SETTINGS[k], "ladder_levels": size[i]}}))
        plan[iid] = {"piece": "pack", "ladder_levels": size[i], "held_out": False, "v1_setting_index": k,
                     "v1_dropped": k in dropped, "line": LINE_PACKS}
    return items, plan


# ------------------------------------------------------------------------------------------------ task files
CONTRACT = {
    "wordings": ('"wordings": a JSON list of strings, exactly as many as the item asks for',
                 '{"qid": "%s", "wordings": ["<question 1>", "<question 2>", "<question 3>"]}',
                 'The angle-bracket strings are stand-ins for your own question texts.'),
    "pack": ('"pack": one JSON object with exactly these five keys: "store" (a string), "ladder" (a list of strings, '
             'as many as the item\'s ladder_levels), "regions" (a list of exactly 4 strings), "categories" (a list of '
             'exactly 3 strings) and "customers" (a list of exactly 4 strings)',
             '{"qid": "%s", "pack": ' + json.dumps(EXAMPLE_PACK, ensure_ascii=False) + '}',
             "The example values are for the format only (its ladder has 3 levels; yours has the item's ladder_levels): "
             "invent your own values and never copy the example's."),
}

BATCH_SPECS = (
    # name, chunker kind, answer field, prompt, line
    ("wordings", "author_wording", "wordings", R2.WORDING_PROMPT, LINE_WORD),
    ("packs", "author_pack", "pack", None, LINE_PACKS),            # prompt: pack_prompt() (pool vocabulary)
)


def build_batches(g: dict) -> dict:
    """{name: (TaskBatch, plan, spec)}: gold-free chunks, opaque qids, seeded order (chunker.make_batch)."""
    out = {}
    n_word, n_pack = ask(g["wording"]), ask(g["packs"])
    for spec in BATCH_SPECS:
        name, kind, _field, prompt, _line = spec
        prompt = prompt or pack_prompt()
        items, plan = wording_items(n_word) if name == "wordings" else pack_items(n_pack)
        b = chunker.make_batch(kind, FAMILY, items, seed=f"{SEED}|{name}", prompt=prompt, forbid_strings=A.FORBID)
        out[name] = (b, plan, spec)
    return out


def outputs_of(plan: dict, iid: str) -> int:
    return plan[iid].get("outputs", 1)


def task_text(b, chunk: dict, field: str, plan: dict, root: Path = ROOT) -> str:
    tid = chunk["task_id"]
    n = len(chunk["items"])
    qids = [it["qid"] for it in chunk["items"]]
    what, shape, note = CONTRACT[field]
    outs = sum(outputs_of(plan, b.key[q]) for q in qids)
    per = sorted({outputs_of(plan, b.key[q]) for q in qids})
    return "\n".join([
        f"# T07 redo3 authoring task {tid} (kind {b.kind})", "",
        "ANSWER FILE (write your whole answer here, and nowhere else, with the Write tool):",
        str(root / b.answer_path(tid)), "",
        "This file is self-contained: the instructions, the answer contract and the items are all below. Read this "
        "whole file. Do not open, list or search any other file or folder.", "",
        "ANSWER CONTRACT (exact; a program checks it):",
        f"- The answer file holds one JSON array with exactly {n} object{'s' if n != 1 else ''}: one per item below, "
        "each item answered once.",
        f'- Each object has exactly two keys: "qid" and "{field}". No other keys.',
        "- \"qid\": copy the item's qid exactly, character for character (the letter q followed by ten letters or "
        f"digits). The qids of this task: {', '.join(qids)}.",
        f"- {what}." + (f" Outputs per item: {per[0]}." if field == "wordings" and len(per) == 1 else ""),
        "- Valid JSON only: no text before or after the array, no markdown code fences, no comments. Inside JSON "
        'strings write a line break as \\n and a double quote as \\".',
        "Literal JSON example (valid JSON; the qid is the first real one of this task"
        + (f"; it shows the first item only, your file holds {n} such objects, one per item" if n > 1 else "")
        + "): [" + shape % qids[0] + "]",
        note, "",
        f"Task kind: {b.kind}; items: {n}; outputs expected: {outs}.", "",
        "## Instructions", "", b.prompt.rstrip(), "",
        f"## Items ({n}; answer every item, keyed by its qid)", "", "```json",
        json.dumps(chunk["items"], ensure_ascii=False, indent=1), "```", ""])


def author_files(root: Path = ROOT, g: dict | None = None) -> tuple:
    """({relative path: text}, TASKS.json object) for paths.write_files."""
    g = g or gaps()
    pend = pending_reads()
    stuck = {k: v["pending"] for k, v in pend.items() if v["pending"]}
    if stuck:
        raise SystemExit(f"STOP: pending reads exist, wrap their chunks first: {stuck}")
    files, rows = {}, []
    for name, (b, plan, spec) in build_batches(g).items():
        field = spec[2]
        files.update(b.files())
        files[f"plan/{b.batch_id}.json"] = json.dumps(
            {"batch_id": b.batch_id, "name": name, "kind": b.kind, "field": field, "line": spec[4], "plan": plan},
            ensure_ascii=False, indent=1, sort_keys=True) + "\n"
        for c in b.chunks:
            tid = c["task_id"]
            tfile = f"tasks/{tid}.md"
            text = task_text(b, c, field, plan, root)
            files[tfile] = text
            ans = str(root / b.answer_path(tid))
            iids = [b.key[it["qid"]] for it in c["items"]]
            rows.append({"task": name, "task_id": tid, "kind": b.kind, "closes": spec[4],
                         "answer_field": field, "task_file": str(root / tfile), "answer_file": ans,
                         "batch_id": b.batch_id, "prompt_sha": b.prompt_sha,
                         "task_sha256": hashlib.sha256(text.encode()).hexdigest(), "n_items": len(c["items"]),
                         "n_held_out_items": sum(1 for i in iids if plan[i]["held_out"]),
                         "outputs_expected": sum(outputs_of(plan, i) for i in iids),
                         "allowed_read": [str(root / tfile)], "allowed_write": [ans]})
    index = {
        "family": FAMILY, "version": VERSION, "seed": SEED, "g0_sha256": G0_SHA,
        "stage": "redo3 author (the two remaining T07 shortfall lines, STAGE_A3_REPORT.json)",
        "gaps": {LINE_WORD: g["wording"], LINE_PACKS: g["packs"]},
        "asked": {LINE_WORD: ask(g["wording"]), LINE_PACKS: ask(g["packs"])},
        "ask_rule": "max(ceil(1.5 x gap), gap + 2)",
        "pending_reads": {"rule": "a chunk of a T07 round without an answer file", "result": pend,
                          "none_pending": not stuck},
        "n_tasks": len(rows), "outputs_expected": sum(r["outputs_expected"] for r in rows),
        "notes": [
            "New items, new opaque ids, new answer paths under redo3/answers/; no earlier task, answer, key, plan or "
            "pool is reused or changed.",
            "Each task file is self-contained (answer path, answer contract with a literal JSON example, the full "
            "prompt, the items). The agent reads only its task file (allowed_read) and writes only its answer file "
            "(allowed_write); audit each agent (c2_kit.audit) before its answers count.",
            "key/ and plan/ are orchestrator only. Next: build_redo3.py validate; then lint (authoring.lint_wording / "
            "lint_pack + check_packs over kept v1 packs first, then drop a pack whose level / region / category word is "
            "returned by build_redo3.pack_pool_collisions), dedup against every earlier text, G-LEX 2/2 reads of the "
            "new yn_misses wordings (v1 meaning list), then merged_pools.verdict.",
            "Labels: none. Haiku writes text pieces only; every gold still comes from solver A = solver B."],
        "tasks": rows}
    files["TASKS.json"] = json.dumps(index, ensure_ascii=False, indent=1) + "\n"
    files["answers/README.txt"] = ("Haiku answer files: one <task_id>.json per redo3 authoring task (see ../TASKS.json). "
                                   "Written only by the task agents.\n")
    return files, index


def check_author(files: dict, g: dict, root: Path = ROOT) -> list:
    """Problems with the tasks (empty = ready): leaks, ids, paths, asks, prompts and the examples themselves."""
    probs = []
    batches = build_batches(g)
    for name, (b, plan, spec) in batches.items():
        for c in b.chunks:
            tid = c["task_id"]
            text = files[f"tasks/{tid}.md"]
            low = text.lower()
            for f in A.FORBID:
                if f and re.search(r"(?<![a-z0-9])" + re.escape(f.lower()) + r"(?![a-z0-9])", low):
                    probs.append(f"{tid}: task text holds forbidden string {f!r}")
            if any(i in text for i in b.key.values()):
                probs.append(f"{tid}: internal id in the task text")
            if not 1 <= len(c["items"]) <= chunker.MAX_ITEMS:
                probs.append(f"{tid}: {len(c['items'])} items")
            if str(root / b.answer_path(tid)) not in text.split("\n")[3]:
                probs.append(f"{tid}: answer path missing from the top")
            for pth in (root / f"tasks/{tid}.md", root / b.answer_path(tid)):
                if paths.never_open(pth):
                    probs.append(f"{tid}: never-open path {pth}")
            if "Literal JSON example" not in text:
                probs.append(f"{tid}: no literal JSON example")
        words = set(A._words(b.prompt))
        missing = sorted(w for w in R2.PACK_WORDS if not A._bad(w) and w not in words)
        if missing and name == "packs":
            probs.append(f"{name}: prompt lacks taken words {missing[:5]}")
    # asks: ~50% over each gap
    got = {LINE_WORD: 0, LINE_PACKS: 0}
    for name, (b, plan, spec) in batches.items():
        got[spec[4]] += sum(outputs_of(plan, i) for i in plan)
    for line, gap in ((LINE_WORD, g["wording"]), (LINE_PACKS, g["packs"])):
        if got[line] < math.ceil(1.5 * gap) or got[line] < gap + 2:
            probs.append(f"ask {line}: {got[line]} for a gap of {gap}")
    # the wording brief allows 'lose out on' only
    if re.search(r"go short|shut out|forfeit", YN_MISSES_R3) or "lose out on" not in YN_MISSES_R3:
        probs.append("yn_misses brief verbs")
    # the pack example is lint-clean, new and free of taken words; the pack settings are the family's
    if A.lint_pack(EXAMPLE_PACK, len(EXAMPLE_PACK["ladder"])):
        probs.append(f"example pack fails lint_pack: {A.lint_pack(EXAMPLE_PACK, 3)}")
    kept, dropped = A.check_packs(R2.kept_packs() + [EXAMPLE_PACK])
    if dropped:
        probs.append("example pack fails check_packs against the kept packs")
    for v in (EXAMPLE_PACK["store"], *EXAMPLE_PACK["ladder"], *EXAMPLE_PACK["regions"], *EXAMPLE_PACK["categories"],
              *EXAMPLE_PACK["customers"]):
        if set(A._words(v)) & TAKEN_WORDS:
            probs.append(f"example value {v!r} holds a taken word")
    b, plan, _s = batches["packs"]
    for it in (x for c in b.chunks for x in c["items"]):
        if it["brief"]["shop_kind"] not in A.PACK_SETTINGS or it["brief"]["ladder_levels"] not in (3, 4):
            probs.append(f"{it['qid']}: pack brief outside the family's settings")
    return probs


def check_on_disk(root: Path, files: dict, skip=("answers/README.txt",)) -> list:
    return [rel for rel, text in sorted(files.items())
            if rel not in skip and (not (root / rel).is_file() or (root / rel).read_text(encoding="utf-8") != text)]


def validate() -> int:
    rep = VA.validate_all(rounds={"redo3-author": ROOT})
    for r in rep["rounds"]:
        print(f"{r['round']}: {r['valid']}/{r['tasks']} valid; invalid {len(r['invalid'])}; missing {len(r['missing'])}; "
              f"extra files {r['extra_files']}")
        for x in r["invalid"]:
            print("  INVALID", x["task_id"], x["problems"][:6])
    return 0 if rep["ok"] else 1


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("stage", choices=("author", "validate"))
    ap.add_argument("--write", action="store_true")
    args = ap.parse_args()
    if args.stage == "validate":
        return validate()
    g = gaps()
    files, index = author_files(g=g)
    probs = check_author(files, g)
    if probs:
        print("\n".join(probs))
        return 1
    if args.write:
        paths.write_files(ROOT, files)
    print(json.dumps({"gaps": index["gaps"], "asked": index["asked"],
                      "tasks": [(r["task"], r["task_id"], r["n_items"], r["outputs_expected"]) for r in index["tasks"]],
                      "n_tasks": index["n_tasks"], "outputs_expected": index["outputs_expected"],
                      "none_pending": index["pending_reads"]["none_pending"], "written": bool(args.write)}, indent=1))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
