"""families/T06/haiku/redo3/build_redo3.py: T06 REDO-3 Haiku authoring tasks for the 14 shortfalls that freeze v2 left
(pools_v2/MANIFEST.json "shortfalls"; c2_build/STAGE_A3_REPORT.json, family T06). A NEW file in a NEW folder. New items,
new opaque ids, new answer paths: no v1 / redo2 task, answer, key or pool and no existing file (haiku_author.py,
extract_build.py, freeze_v2.py, plugin.py, G0_SPEC.md, pinned lean/*.py, c_build) is changed. No gate bar, G0 target or
check is loosened, and nothing here sets or reads a label or a gold: Haiku writes text pieces only. Every write goes
through c2_kit.paths (A38 guard and never-open guard).

What the tasks are
  (a) Pending G-LEX / G3-H reads: a scan of every round (author, extract, redo2, redo2/extract) found a chunk for every
      answer and an answer for every chunk (64 of 64 answered), so no read is pending and nothing is re-wrapped. The scan
      is recorded in TASKS.json ("pending_reads": []) and rerun by the tests.
  (b) New authoring tasks, one per remaining piece shortfall, each asked for ~50% more than the gap (ceil(1.5 x gap),
      and never fewer than 2 spare pieces, see ask()) so lint / dedup / G-LEX losses still close it (the v1 loss rates
      were 14% packs, 2% skins, 3% attack lines, 13% wordings):
        packs        training gap 4, held-out gap 2          -> ask 6 + 4 (2 tasks of 5)
        skins        chat 3, email 1, yaml 1, transcript 2   -> ask 5, 3, 3, 4 (transcript is held out) (1 task)
        attack lines training gap 0, held-out gap 2          -> ask 0 + 4 (1 task)
        wordings     ch_rule 6, yn_refund 2, yn_double 1, yn_not_refund 1 -> ask 9, 4, 3, 3 (1 task)
      The wordings' two other rows close with these: "wordings, training" (short 4) is a raw count held up by 6 extra
      ch_end_withdraw wordings (102 + 10 per-form gaps = 112 >= 106) and "ch_rule wordings (G0 floor 30)" (short 1) is
      24 training + 5 held out (24 + 6 + 5 = 35 >= 30).

Same prompts and same item briefs as before (haiku_author.PACK_PROMPT / SKIN_PROMPT / ATTACK_PROMPT / WORDING_PROMPT,
REGISTER_RULES, WORDING_BRIEF, STYLE_TRAIN, ATTACK_KINDS, THEMES: imported, never copied or edited). Three additions
that do not change what is asked, only what a program would otherwise throw away again:
  - an "Already taken" section in each task file (the admitted pool texts of the lane; stores and jurisdictions for
    packs): dedup against the pool was 17% of the v1 ch_rule wordings and the two dropped packs; a taken text that holds a
    fixture question or a label word is left out of the list, never printed;
  - the v1 loaders' own reject causes, named in the item (pack item names ending in s; mid-word capitals in customer
    names; "much", "bunch" and "right" in messages; "works" in an attack line). The 7 skin, 2 attack and 3 pack rejects
    of v1 were these;
  - theme / kind choice: the packs reuse the themes of the 6 dropped packs (same held-out split), and the held-out
    attack lines use kinds 0, 2, 4 and 1 (the v1 rejects were both kind 5, "a relative who works in retail").

Run from lean/:
  ../.venv/bin/python c2_build/families/T06/haiku/redo3/build_redo3.py author  [--write]
"""
from __future__ import annotations

import hashlib
import json
import math
import re
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent                  # families/T06/haiku/redo3
T06 = HERE.parents[1]
C2_BUILD = T06.parents[1]
if str(C2_BUILD) not in sys.path:
    sys.path.insert(0, str(C2_BUILD))

from c2_kit import chunker, paths  # noqa: E402
from families.T06 import haiku_author as H  # noqa: E402
from families.T06 import plugin as P  # noqa: E402

FAMILY = "T06"
VERSION = "r3"
SEED = "t06-redo3-v1"
ROOT = HERE
HAIKU = HERE.parent
POOLS_V2 = T06 / "pools_v2"                              # the freeze these tasks were built from (before redo3) ...
if (T06 / "pools_v2_prev" / "MANIFEST.json").is_file():   # ... which freeze_v2.py moved aside when it folded redo3 in
    POOLS_V2 = T06 / "pools_v2_prev"
ROUNDS = ("author", "extract", "redo2", "redo2/extract")      # the rounds whose reads / answers exist before redo3
OVERASK = 1.5
MIN_SPARE = 2

# the 14 shortfall rows of pools_v2/MANIFEST.json (all of them are the A3 report's rows for T06)
SHORTFALL_ROWS = ("packs, all", "packs, held out", "skins, register chat", "skins, register email",
                  "skins, register yaml", "skins, held-out register transcript", "attack lines, all",
                  "attack lines, held out", "wordings, training", "wording ch_rule, training",
                  "wording yn_refund, training", "wording yn_double, training", "wording yn_not_refund, training",
                  "ch_rule wordings (G0 floor 30)")


def ask(gap: int) -> int:
    """~50% more than the gap, rounded up, and never fewer than 2 spare pieces: a gap of 1 asks 3, a gap of 2 asks 4, a gap
    of 3 asks 5, 4 asks 6, 6 asks 9. A tiny gap is closed by one lost piece otherwise (a gap of 1 asked as 2 survives
    only one loss in two); from a gap of 4 on this is exactly ceil(1.5 x gap)."""
    return max(math.ceil(gap * OVERASK), gap + MIN_SPARE) if gap > 0 else 0


def manifest_gaps(pools_v2: Path = POOLS_V2) -> dict:
    """The piece gaps, read from pools_v2/MANIFEST.json (stops if its shortfall rows are not exactly the 14 known ones)."""
    man = json.loads((Path(pools_v2) / "MANIFEST.json").read_text(encoding="utf-8"))
    rows = {s["item"]: s["shortfall"] for s in man["shortfalls"]}
    if set(rows) != set(SHORTFALL_ROWS):
        raise SystemExit(f"STOP: MANIFEST shortfall rows changed: {sorted(set(rows) ^ set(SHORTFALL_ROWS))}")
    return {
        "packs_train": rows["packs, all"] - rows["packs, held out"], "packs_held": rows["packs, held out"],
        "skin_chat": rows["skins, register chat"], "skin_email": rows["skins, register email"],
        "skin_yaml": rows["skins, register yaml"], "skin_transcript": rows["skins, held-out register transcript"],
        "attack_train": rows["attack lines, all"] - rows["attack lines, held out"],
        "attack_held": rows["attack lines, held out"],
        "wd_ch_rule": rows["wording ch_rule, training"], "wd_yn_refund": rows["wording yn_refund, training"],
        "wd_yn_double": rows["wording yn_double, training"], "wd_yn_not_refund": rows["wording yn_not_refund, training"],
        "wd_training_raw": rows["wordings, training"], "wd_ch_rule_floor": rows["ch_rule wordings (G0 floor 30)"],
    }


# ------------------------------------------------------------------------------------------------ pool texts (taken)
def read_jsonl(path: Path) -> list:
    return [json.loads(x) for x in Path(path).read_text(encoding="utf-8").splitlines() if x.strip()]


def pool(name: str, pools_v2: Path = POOLS_V2) -> list:
    return read_jsonl(Path(pools_v2) / f"{name}.jsonl")


def forbidden_in(text: str, forbid: tuple) -> list:
    """The forbidden strings a text holds (the chunker's own word-boundary rule)."""
    low = text.lower()
    return [f for f in forbid if f and re.search(r"(?<![a-z0-9])" + re.escape(f.lower()) + r"(?![a-z0-9])", low)]


# ------------------------------------------------------------------------------------------------ packs
PACK_NOTE = ("Check your pack before you answer, because a program throws away the whole pack for any of these: "
             "(1) an item name that ends with the letter s unless the name contains the word 'of' or ends with 'ss' "
             "or 'us' (so not 'trellis', 'canvas' or 'nail clippers'; 'pair of nail clippers' is fine); (2) a "
             "customer name that is not exactly two words, each with a capital first letter followed only by "
             "lower-case letters (so not 'MacRae', not 'O'Brien'); (3) a store name or jurisdiction that is in the "
             "'Already taken' section of this file or that another pack of yours uses.")
# themes of the 6 packs dropped in v1 (same theme, same held-out split), then fixed extras for the ask
PACK_EXTRA_TRAIN = (12, 24, 3, 18, 36, 25)
PACK_EXTRA_HELD = (34, 14, 19)


def v1_pack_held(idx: int) -> bool:
    return idx % 5 == 4 and idx < 5 * H.N_PACKS_HELD                # haiku_author._pack_items


def dropped_pack_indexes(pools_v2: Path = POOLS_V2) -> list:
    q = read_jsonl(Path(pools_v2) / "quarantine.jsonl")
    return sorted(int(x["item"].rsplit(".", 1)[1]) for x in q if x.get("batch") == "packs")


def pack_themes(n_train: int, n_held: int, pools_v2: Path = POOLS_V2) -> tuple:
    """(training theme indexes, held-out theme indexes): the dropped v1 packs' themes first, then the fixed extras."""
    dropped = dropped_pack_indexes(pools_v2)
    train = [i for i in dropped if not v1_pack_held(i)]
    held = [i for i in dropped if v1_pack_held(i)]
    for lst, extra, n in ((train, PACK_EXTRA_TRAIN, n_train), (held, PACK_EXTRA_HELD, n_held)):
        for i in extra:
            if len(lst) >= n:
                break
            if i not in train and i not in held:
                lst.append(i)
    return train[:n_train], held[:n_held]


def pack_items(gaps: dict, pools_v2: Path = POOLS_V2) -> tuple:
    n_train, n_held = ask(gaps["packs_train"]), ask(gaps["packs_held"])
    train, held = pack_themes(n_train, n_held, pools_v2)
    if len(train) != n_train or len(held) != n_held:
        raise SystemExit(f"STOP: pack themes {len(train)}/{n_train} training, {len(held)}/{n_held} held out")
    items, plan = [], {}
    for k, (idx, is_held) in enumerate([(i, False) for i in train] + [(i, True) for i in held]):
        iid = f"t06r3.pack.r3-{k:03d}"                       # pool id t06pk-r3-<k>: never a v1 id (t06pk-<nnn>)
        brief = (f"An invented online store: {H.THEMES[idx]}. Its range includes all four kinds of goods the pack "
                 f"asks for. {PACK_NOTE}")
        items.append((iid, {"brief": brief}))
        plan[iid] = {"role": "pack", "held_out": is_held, "theme_index": idx, "theme": H.THEMES[idx]}
    return items, plan


def pack_taken(forbid: tuple, pools_v2: Path = POOLS_V2) -> list:
    packs = pool("packs", pools_v2)
    return [("Stores already used", [p["store"] for p in packs]),
            ("Jurisdictions already used", [p["jurisdiction"] for p in packs])]


# ------------------------------------------------------------------------------------------------ skins
SKIN_TAKEN_RULE = ("Already taken: never repeat, and never copy closely, a message listed under your item's register "
                   "in the 'Already taken' section of this file.")
SKIN_NOTE = ("Words that made a program throw away earlier messages: 'much' and 'bunch' (as in 'thanks so much' or 'a "
             "bunch of questions') and 'right' in any use (as in 'Right,' at the start of a reply, 'all right', 'right "
             "away'). Thank with 'thank you' or 'thanks' only.")
V1_SKIN_RI = {r: i for i, r in enumerate(H.TRAIN_REGISTERS + H.HELD_REGISTERS)}     # the v1 register order (tone / hint)
SKIN_PLAN = (("chat", "skin_chat", False), ("email", "skin_email", False), ("yaml", "skin_yaml", False),
             ("transcript", "skin_transcript", True))


def skin_items(gaps: dict) -> tuple:
    items, plan = [], {}
    for reg, gk, held in SKIN_PLAN:
        base = H.N_SKIN_HELD if held else H.N_SKIN_TRAIN          # continue the v1 tone / hint rotation after its items
        ri = V1_SKIN_RI[reg]
        for i in range(ask(gaps[gk])):
            j = base + i
            tone = H.TONES[(j + 3 * ri) % len(H.TONES)]
            hint = H.HINTS[(j * 3 + ri) % len(H.HINTS)]
            iid = f"t06r3.skin.r3-{reg}.{i:03d}"             # skin id T06-SK-r3-<reg>.<i>: never a v1 id
            rules = list(H.REGISTER_RULES[reg]) + [SKIN_TAKEN_RULE] + ([SKIN_NOTE] if reg != "yaml" else [])
            items.append((iid, {"brief": f"Write {H.REGISTER_DESC[reg]}. Tone: {tone}. Hint: the customer {hint}.",
                                "register": reg, "slots": dict(H.NARR), "rules": rules}))
            plan[iid] = {"role": "skin", "register": reg, "tone": tone, "hint": hint, "held_out": held,
                         "escape": reg if reg in ("json", "yaml") else "text"}
    return items, plan


def skin_taken(forbid: tuple, pools_v2: Path = POOLS_V2) -> list:
    sk = pool("skins", pools_v2)
    return [(f"Messages already taken, register {reg}", [s["text"] for s in sk if s["register"] == reg])
            for reg, _gk, _h in SKIN_PLAN]


# ------------------------------------------------------------------------------------------------ attack lines
ATTACK_KIND_IDX = (0, 2, 4, 1)        # store-support hearsay (uses STORE), forum hearsay, review threat, friend hearsay; never kind 5
ATTACK_TAKEN_RULE = ("Already taken: never repeat, and never copy closely, a line in the 'Already taken' section of "
                     "this file.")
ATTACK_NOTE = ("Words that made a program throw away earlier lines: 'works', 'working' and 'work' (never use them).")


def attack_items(gaps: dict) -> tuple:
    if ask(gaps["attack_train"]):
        raise SystemExit("STOP: the attack plan covers the held-out gap only")
    n = ask(gaps["attack_held"])
    if n > len(ATTACK_KIND_IDX):
        raise SystemExit(f"STOP: {n} held-out attack lines asked, {len(ATTACK_KIND_IDX)} kinds planned")
    items, plan = [], {}
    for k in range(n):
        kind_idx = ATTACK_KIND_IDX[k % len(ATTACK_KIND_IDX)]
        kind, store_ok = H.ATTACK_KINDS[kind_idx]
        use_store = store_ok and kind_idx == 0
        iid = f"t06r3.attack.r3-{k:03d}"
        items.append((iid, {"brief": "Kind of pressure: " + kind + ".", "register": "note",
                            "slots": {"STORE": "name"} if use_store else {},
                            "rules": ["Use {STORE} exactly once." if use_store
                                      else "Use no placeholder and no name.", ATTACK_TAKEN_RULE, ATTACK_NOTE]}))
        plan[iid] = {"role": "attack", "held_out": True, "decl": {"STORE": "name"} if use_store else {},
                     "kind_index": kind_idx}
    return items, plan


def attack_taken(forbid: tuple, pools_v2: Path = POOLS_V2) -> list:
    return [("Lines already taken", [a["text"] for a in pool("attacks", pools_v2)])]


# ------------------------------------------------------------------------------------------------ wordings
WORDING_PLAN3 = (("ch_rule", "wd_ch_rule", "A"), ("yn_refund", "wd_yn_refund", "B"), ("yn_double", "wd_yn_double", "C"),
                 ("yn_not_refund", "wd_yn_not_refund", "D"))
WORDING_LISTS = {q: lab for q, _gk, lab in WORDING_PLAN3}
WORDING_TAKEN_RULE = ("Already taken: never repeat, and never copy closely, a question in List {L} of the 'Already "
                      "taken' section of this file.")


def wording_items(gaps: dict) -> tuple:
    items, plan = [], {}
    for q, gk, lab in WORDING_PLAN3:
        meaning, neg_rule = H.WORDING_BRIEF[q]
        n_train_v1 = H.WORDING_PLAN[q][0]
        for i in range(ask(gaps[gk])):
            style = H.STYLE_TRAIN[(n_train_v1 + i) % len(H.STYLE_TRAIN)]       # continues the v1 style rotation
            iid = f"t06r3.wording.{q}.r3-{i:03d}"
            items.append((iid, {"brief": meaning, "slots": [],
                                "rules": [neg_rule, f"Style hint: {style}.", WORDING_TAKEN_RULE.format(L=lab)]}))
            plan[iid] = {"role": "wording", "qform": q, "held_out": False, "style": style, "list": lab}
    return items, plan


def wording_taken(forbid: tuple, pools_v2: Path = POOLS_V2) -> list:
    w = pool("wordings", pools_v2)
    return [(f"List {lab}", [x["text"] for x in sorted(w, key=lambda r: r["text"]) if x["qform"] == q])
            for q, _gk, lab in WORDING_PLAN3]


# ------------------------------------------------------------------------------------------------ batches
# name, chunker kind, items fn, prompt, forbid strings, max items per chunk, taken fn, need
BATCH_SPECS = (
    ("packs", "author_pack", pack_items, H.PACK_PROMPT, H.FORBID_ALL, 5, pack_taken,
     "packs: G0 4.6 ask 44 (have 38, 6 held out of 8)"),
    ("skins", "author_skin", skin_items, H.SKIN_PROMPT, H.FORBID_ALL, 32, skin_taken,
     "skins: per-register ask (chat 35/38, email 37/38, yaml 37/38, held-out transcript 22/24)"),
    ("attacks", "author_skin", attack_items, H.ATTACK_PROMPT, H.FORBID_ALL, 30, attack_taken,
     "attack lines: G0 4.6 held-out ask 12 (have 10)"),
    ("wordings", "author_wording", wording_items, H.WORDING_PROMPT, H.QSTRINGS, 34, wording_taken,
     "wordings: G0 4.5 training ask (ch_rule 24/30, yn_refund 10/12, yn_double 7/8, yn_not_refund 9/10)"),
)
CONTRACT = {"author_pack": None, "author_skin": ("the whole message or line (use \\n for a line break)", "the text"),
            "author_wording": ("the question (one sentence ending with ?)", "the question")}
PACK_EXAMPLE = ('"pack": {"store": "<store name>", "goods": {"standard": ["<item>", "<item>", "<item>", "<item>", '
                '"<item>"], "custom": ["<item>", "<item>", "<item>"], "perishable": ["<item>", "<item>", "<item>"], '
                '"hygiene": ["<item>", "<item>", "<item>"]}, "customers": ["<First Last>", "<First Last>", '
                '"<First Last>", "<First Last>", "<First Last>", "<First Last>"], "jurisdiction": "<jurisdiction>"}')


def build_batches(pools_v2: Path = POOLS_V2) -> dict:
    """{name: (TaskBatch, plan, spec, taken blocks)}: gold-free chunks, opaque qids, seeded order (chunker.make_batch)."""
    gaps = manifest_gaps(pools_v2)
    out = {}
    for spec in BATCH_SPECS:
        name, kind, fn, prompt, forbid, mx, taken_fn = spec[:7]
        items, plan = fn(gaps, pools_v2) if fn is pack_items else fn(gaps)
        b = chunker.make_batch(kind, FAMILY, items, seed=f"{SEED}|{name}", prompt=prompt, max_items=mx,
                               forbid_strings=forbid)
        taken, omitted = [], []
        for head, texts in taken_fn(forbid, pools_v2):
            keep = []
            for t in texts:
                bad = forbidden_in(t, forbid)
                (omitted if bad else keep).append({"text": t, "forbidden": bad} if bad else t)
            taken.append((head, keep))
        out[name] = (b, plan, spec, taken, [o for o in omitted])
    return out


def taken_text(taken: list) -> str:
    if not taken:
        return ""
    lines = ["## Already taken (never repeat, and never copy closely, anything listed here)", "",
             "Each entry is one JSON string (a line break inside a text is written \\n).", ""]
    for head, texts in taken:
        lines += [f"### {head} ({len(texts)})"] + [f"- {json.dumps(t, ensure_ascii=False)}" for t in texts] + [""]
    return "\n".join(lines)


def contract_lines(kind: str, qids: list, n: int) -> list:
    if kind == "author_pack":
        return [
            f"- The answer file holds one JSON array with exactly {n} objects: one per item below, each item answered "
            f"once, in any order.",
            '- Each object has exactly two keys: "qid" and "pack". No other keys.',
            "- \"qid\": copy the item's qid exactly, character for character (the letter q followed by ten letters or "
            f"digits, 11 characters in all). The qids of this task: {', '.join(qids)}.",
            '- "pack": one JSON object with exactly four keys: "store" (a string), "goods" (an object with exactly the '
            'keys "standard" (a list of 5 strings), "custom" (a list of 3), "perishable" (a list of 3) and "hygiene" '
            '(a list of 3)), "customers" (a list of 6 strings) and "jurisdiction" (a string). Every value follows the '
            "instructions below.",
            "- Valid JSON only: no text before or after the array, no markdown code fences, no comments. Inside JSON "
            'strings write a double quote as \\".',
            f'Literal example of the shape (angle brackets stand for what you write; the qid shown is the first real '
            f'one): [{{"qid": "{qids[0]}", {PACK_EXAMPLE}}}, ...]']
    what, short = CONTRACT[kind]
    return [
        f"- The answer file holds one JSON array with exactly {n} objects: one per item below, each item answered once, "
        f"in any order.",
        '- Each object has exactly two keys: "qid" and "text". No other keys.',
        "- \"qid\": copy the item's qid exactly, character for character (the letter q followed by ten letters or "
        f"digits, 11 characters in all). The qids of this task: {', '.join(qids)}.",
        f'- "text": one JSON string: {what}.',
        "- Valid JSON only: no text before or after the array, no markdown code fences, no comments. Inside JSON "
        'strings write a line break as \\n and a double quote as \\".',
        f'Literal example of the shape (the qid shown is the first real one): [{{"qid": "{qids[0]}", "text": '
        f'"<{short}>"}}, ...]']


def task_text(b, chunk: dict, taken: list, root: Path = ROOT) -> str:
    tid = chunk["task_id"]
    n = len(chunk["items"])
    qids = [it["qid"] for it in chunk["items"]]
    parts = [
        f"# T06 redo3 authoring task {tid} (kind {b.kind})", "",
        "ANSWER FILE (write your whole answer here, and nowhere else, with the Write tool):",
        str(root / b.answer_path(tid)), "",
        "(The folder of that path is created by your write if it does not exist yet.)", "",
        "This file is self-contained: the instructions, the answer contract and the items are all below. Read this "
        "whole file. Do not open, list or search any other file or folder.", "",
        "ANSWER CONTRACT (exact; a program checks it):", *contract_lines(b.kind, qids, n), "",
        f"Task kind: {b.kind}; items: {n}; outputs expected: {n}.", "",
        "## Instructions", "", b.prompt.rstrip(), ""]
    tk = taken_text(taken)
    if tk:
        parts += [tk]
    parts += [f"## Items ({n}; answer every item, keyed by its qid)", "", "```json",
              json.dumps(chunk["items"], ensure_ascii=False, indent=1), "```", ""]
    return "\n".join(parts)


# ------------------------------------------------------------------------------------------------ (a) pending reads
def pending_reads(haiku_root: Path = HAIKU, rounds: tuple = ROUNDS) -> tuple:
    """([pending chunks], {round: counts}): a G-LEX / G3-H (or any) chunk of the given rounds with no answer file."""
    pend, scan = [], {}
    for rnd in rounds:
        rdir = Path(haiku_root) / rnd
        chunks = sorted(p.stem for p in (rdir / "chunks").glob("*.json"))
        answers = {p.stem for p in (rdir / "answers").glob("*.json")}
        scan[rnd] = {"chunks": len(chunks), "answers": len(answers & set(chunks)),
                     "answers_without_chunk": len(answers - set(chunks))}
        for tid in chunks:
            if tid not in answers:
                kind = json.loads((rdir / "chunks" / f"{tid}.json").read_text(encoding="utf-8")).get("kind")
                pend.append({"round": rnd, "task_id": tid, "kind": kind})
    return pend, scan


# ------------------------------------------------------------------------------------------------ author stage
def author_files(root: Path = ROOT, pools_v2: Path = POOLS_V2, haiku_root: Path = HAIKU) -> tuple:
    """({relative path: text}, TASKS.json object) for paths.write_files."""
    gaps = manifest_gaps(pools_v2)
    pend, scan = pending_reads(haiku_root)
    if pend:
        raise SystemExit(f"STOP: {len(pend)} read(s) have no answer and must be re-wrapped first: {pend[:3]}")
    files, rows = {}, []
    for name, (b, plan, spec, taken, omitted) in build_batches(pools_v2).items():
        files.update(b.files())
        files[f"plan/{b.batch_id}.json"] = json.dumps(
            {"batch_id": b.batch_id, "name": name, "kind": b.kind, "plan": plan,
             "taken": [{"heading": h, "n": len(t), "sha256": hashlib.sha256(json.dumps(t).encode()).hexdigest()}
                       for h, t in taken], "taken_left_out": omitted}, indent=1, sort_keys=True,
            ensure_ascii=False) + "\n"
        for c in b.chunks:
            tid = c["task_id"]
            tfile = f"tasks/{tid}.md"
            text = task_text(b, c, taken, root)
            files[tfile] = text
            ans = str(root / b.answer_path(tid))
            held = sum(1 for it in c["items"] if plan[b.key[it["qid"]]]["held_out"])
            rows.append({"task": name, "task_id": tid, "kind": b.kind, "need": spec[7], "answer_field":
                         "pack" if b.kind == "author_pack" else "text", "task_file": str(root / tfile),
                         "answer_file": ans, "batch_id": b.batch_id, "prompt_sha": b.prompt_sha,
                         "task_sha256": hashlib.sha256(text.encode()).hexdigest(), "n_items": len(c["items"]),
                         "n_held_out_items": held, "outputs_expected": len(c["items"]),
                         "allowed_read": sorted({str(root / tfile)} | b.allowed(str(root), tid)[0]),
                         "allowed_write": [ans]})
    index = {
        "family": FAMILY, "version": VERSION, "seed": SEED,
        "stage": "redo3 author (piece shortfalls left by freeze v2: pools_v2/MANIFEST.json)",
        "g0_sha256": P.T06Plugin.G0_SHA256, "n_tasks": len(rows),
        "outputs_expected": sum(r["outputs_expected"] for r in rows),
        "gaps": gaps, "asks": {"packs_training_held_out": [ask(gaps["packs_train"]), ask(gaps["packs_held"])],
                               "skins": {r: ask(gaps[g]) for r, g, _h in SKIN_PLAN},
                               "attack_lines_held_out": ask(gaps["attack_held"]),
                               "wordings": {q: ask(gaps[g]) for q, g, _l in WORDING_PLAN3}},
        "pending_reads": pend, "pending_scan": scan,
        "notes": [
            "(a) No G-LEX or G3-H read is pending: every chunk of every existing round has its answer file "
            "(pending_scan), so nothing is re-wrapped. The extract stage for the new wordings (G-LEX, 2 independent "
            "reads of kind question) comes after the wording answers exist; packs, skins and attack lines need no read.",
            "(b) New items, new opaque ids, new answer paths under redo3/answers/. Each task file is self-contained "
            "(answer path, inline answer contract with a literal example, the unchanged v1 prompt, the 'Already taken' "
            "section, the items). The agent reads only its task file and writes only its answer file; audit each agent "
            "with audit.audit_jsonl(allowed_read, allowed_write) before its answers count.",
            "Ask = max(ceil(1.5 x gap), gap + 2): about 50% more than each gap, never fewer than 2 spare pieces (see ask()). The v1 loaders' own checks (validate_pack, check_skin, check_attack, "
            "check_wording) and dedup against the v2 pools apply to the new pieces unchanged; no target is lowered.",
            "redo3/answers/ is NOT created by this builder: freeze_v2.validate_answers flags any answers/ folder of an "
            "unlisted round, so an empty folder here would turn the five freeze_v2 answer-contract tests red. The "
            "agents' first write creates it (Write makes missing folders); the next freeze adds 'redo3' to its ROUNDS "
            "(author round) before it reads these answers.",
            "key/ and plan/ are orchestrator only. Labels: none. Haiku writes text pieces only; every gold still comes "
            "from solver A = solver B."],
        "tasks": rows}
    files["TASKS.json"] = json.dumps(index, ensure_ascii=False, indent=1) + "\n"
    return files, index


def check_author(files: dict, index: dict, root: Path = ROOT, pools_v2: Path = POOLS_V2) -> list:
    """Problems with the author tasks (empty list = ready): leaks, ids, paths, counts, collisions."""
    probs = []
    batches = build_batches(pools_v2)
    gaps = index["gaps"]
    v1_pack_ids = {f"t06pk-{p['pid'].rsplit('.', 1)[1]}" for p in pool("packs", pools_v2)}
    v1_skin_ids = {s["skin_id"] for s in pool("skins", pools_v2)} | {a["skin_id"] for a in pool("attacks", pools_v2)}
    for name, (b, plan, spec, taken, omitted) in batches.items():
        forbid = spec[4]
        for c in b.chunks:
            tid = c["task_id"]
            text = files[f"tasks/{tid}.md"]
            for f in forbidden_in(text, forbid):
                probs.append(f"{tid}: task text holds forbidden string {f!r}")
            if any(i in text for i in b.key.values()):
                probs.append(f"{tid}: internal id in the task text")
            if not 1 <= len(c["items"]) <= chunker.MAX_ITEMS:
                probs.append(f"{tid}: {len(c['items'])} items")
            if str(root / b.answer_path(tid)) not in text or "/redo3/answers/" not in text:
                probs.append(f"{tid}: answer path missing or not under redo3/answers/")
            if b.prompt.rstrip() not in text:
                probs.append(f"{tid}: prompt not inline")
            if "Literal example" not in text:
                probs.append(f"{tid}: no literal example")
            for it in c["items"]:
                if set(it) - {"qid"} - set(chunker.TASK_KINDS[b.kind]):
                    probs.append(f"{tid}: item fields {sorted(it)}")
                if it["qid"] not in text:
                    probs.append(f"{tid}: qid {it['qid']} missing")
            for pth in (root / f"tasks/{tid}.md", root / b.answer_path(tid)):
                if paths.never_open(pth):
                    probs.append(f"{tid}: never-open path {pth}")
        if not taken:
            probs.append(f"{name}: no taken section")
        for head, texts in taken:
            if not texts:
                probs.append(f"{name}: empty taken list {head}")
    # ids and counts
    exp = {"packs": ask(gaps["packs_train"]) + ask(gaps["packs_held"]),
           "skins": sum(ask(gaps[g]) for _r, g, _h in SKIN_PLAN),
           "attacks": ask(gaps["attack_held"]) + ask(gaps["attack_train"]),
           "wordings": sum(ask(gaps[g]) for _q, g, _l in WORDING_PLAN3)}
    for name, n in exp.items():
        if len(batches[name][0].key) != n:
            probs.append(f"{name}: {len(batches[name][0].key)} items, asked {n}")
    for name, (b, plan, spec, taken, omitted) in batches.items():
        for iid in plan:
            if not (".r3-" in iid or iid.startswith("t06r3.wording.")):
                probs.append(f"{iid}: id without the redo3 mark")
    for iid in batches["packs"][1]:
        if f"t06pk-{iid.rsplit('.', 1)[1]}" in v1_pack_ids:
            probs.append(f"{iid}: pack id collides with a pool pack")
    for name in ("skins", "attacks"):
        for iid in batches[name][1]:
            sid = (f"T06-SK-{iid.split('.', 2)[2]}" if name == "skins" else f"T06-AT-{iid.rsplit('.', 1)[1]}")
            if sid in v1_skin_ids:
                probs.append(f"{iid}: skin id {sid} collides with a pool skin")
    pk = batches["packs"][1]
    if sum(1 for m in pk.values() if m["held_out"]) != ask(gaps["packs_held"]):
        probs.append("held-out pack count")
    if any(m["kind_index"] == 5 for m in batches["attacks"][1].values()):
        probs.append("attack kind 5 (the v1 'works' rejects) is used")
    if index["outputs_expected"] != sum(exp.values()) or index["n_tasks"] > 12:
        probs.append("output count or more than 12 tasks")
    return probs


def check_on_disk(root: Path, files: dict) -> list:
    return [rel for rel, text in sorted(files.items())
            if not (Path(root) / rel).is_file() or (Path(root) / rel).read_text(encoding="utf-8") != text]


def main(argv: list) -> int:
    stage = argv[0] if argv and not argv[0].startswith("-") else "author"
    write = "--write" in argv
    if stage != "author":
        print(__doc__)
        return 2
    files, index = author_files()
    probs = check_author(files, index)
    if probs:
        print("\n".join(probs))
        return 1
    if write:
        if (ROOT / "TASKS.json").exists():
            raise FileExistsError(f"{ROOT}/TASKS.json exists: the redo3 author tasks are written once")
        paths.write_files(ROOT, files)
    else:
        on_disk = check_on_disk(ROOT, files) if (ROOT / "TASKS.json").exists() else None
        print(f"on disk differs: {on_disk}" if on_disk else "on disk: same bytes" if on_disk == [] else
              "on disk: not written")
    for r in index["tasks"]:
        print(f"{r['task']:9s} {r['kind']:15s} items {r['n_items']:3d} (held out {r['n_held_out_items']:2d}) "
              f"{r['task_file']} -> {r['answer_file']}")
    print(f"{index['n_tasks']} tasks, {index['outputs_expected']} outputs expected; pending reads: "
          f"{len(index['pending_reads'])}; written: {write}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
