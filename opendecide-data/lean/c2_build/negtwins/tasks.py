"""negtwins/tasks.py: Haiku / Sonnet task writers for A42-D item 7 (same task-file style as t37b/author_pool.py).

Stages (every writer goes through c2_kit.paths, which refuses before A38; the orchestrator runs the agents):
  draft      (a) lexicon candidates: truth frames, negative frames, lexical complement pairs   -> haiku/draft/
  heldout    (b) surface realisations of the 43 frozen held-out patterns' slots                 -> haiku/heldout/
  glex       two independent polarity rounds on the rewritten probes of every drafted entry     -> haiku/glex_<set>_r1|r2/
  exact      blind exactness: 10 base/twin pairs per pattern, flag only, >= 0.9 per pattern     -> haiku/exact_<set>/
  cardcert   two reads per base type: is the card's "no" the exact complement of its "yes"      -> haiku/cardcert_r1|r2/
  audit      Sonnet audit of 3% of twin rows (seeded, stratified by pattern)                    -> haiku/audit/
Answers are read back with chunker.load_answers; the decision functions below turn them into admit / drop lists.
Haiku never sees a pattern id, a gold, a label or a block name.
"""
from __future__ import annotations

import json
import math
from collections import Counter, defaultdict
from pathlib import Path

from c2_kit import chunker, paths  # noqa: E402
from t37b import builder as BL  # noqa: E402

from . import core as C
from . import heldout as H
from . import lexicon as L
from . import probe_bank as PB

HERE = Path(__file__).resolve().parent
FAMILY = "NEGTW"
CHUNK = 50
PAIRS_PER_ITEM = 2
EXACT_PER_PATTERN = 10
EXACT_MIN = 0.9
AUDIT_FRAC = 0.03
AUDIT_DROP_RATE = 0.03
AUDIT_SMALL = 33
GEN_CARD = "a48h"           # card certificates: items unchanged since the first A48 (h) pass, batch ids kept
GEN = "a48h2"               # task generation tag: A48 (h) superseded the first stage-2 task files (new seeds, new batch ids)

FIELDS = ("permission and prohibition", "requirement and option", "presence and absence", "inclusion and exclusion",
          "mentioning and leaving out", "acceptance and refusal", "availability and unavailability",
          "support and contradiction", "eligibility and ineligibility", "approval and rejection",
          "opening and closing", "allowance and restriction", "disclosure and concealment", "validity and invalidity")
TARGET_VERBS = ("contain", "ask", "say", "name", "send", "require", "use", "involve", "give", "mean", "try", "show",
                "mention", "offer", "support", "cover", "list", "provide", "allow", "include")
TARGET_ADJS = ("given", "limited", "free", "supported", "faithful", "off-topic", "worth", "available", "required",
               "permitted", "covered", "included", "open", "valid", "eligible")
STYLES = ("formal register", "everyday plain words", "short and direct", "as used in notices and rules",
          "as used in reviews and reports", "as used in forms and applications")

# ------------------------------------------------------------------------------------------------ prompts
DRAFT_PROMPT = (
    "You write wording options for a reading test about negation. Each item has a brief, the meaning the wording must "
    "have, and rules. For each item write exactly what its rules ask for and nothing else. Never answer a question, "
    "never add facts. Reply with JSON only: a list with one object per item, {\"qid\": <the item's qid>, \"frames\": "
    "[...]} for a frame item and {\"qid\": <the item's qid>, \"pairs\": [...]} for a pair item, as the item's rules "
    "describe. Every string is plain text on one line.")
HELDOUT_PROMPT = (
    "You write wording options for a reading test about negation. Each item names one slot and gives the meaning the "
    "wording must have, plus rules. Write what the rules ask for. Use unusual but natural wordings; do not reuse the "
    "most common phrase for the meaning. Never answer a question, never add facts. Reply with JSON only: a list with "
    "one object per item, {\"qid\": <the item's qid>, \"frames\": [...]} for a frame slot and {\"qid\": <the item's "
    "qid>, \"pairs\": [...]} for a pair slot. Every string is plain text on one line.")
EXACT_PROMPT = BL.POLARITY_PROMPT
GLEX_PROMPT = BL.POLARITY_PROMPT
CARD_PROMPT = (
    "Each item holds two statements written as yes/no questions, question_a and question_b, about the same piece of "
    "text. Reply 'opposite' if for ANY text exactly one of them has the answer yes (never both, never neither); "
    "'same' if a yes to one always goes with a yes to the other; 'unclear' if some texts could make both answers "
    "no, or both yes, or the wording is not clear. Reply with JSON: a list of objects {\"qid\": <qid>, "
    "\"relation\": \"same\" | \"opposite\" | \"unclear\"}.")
AUDIT_PROMPT = (
    "Each item holds two yes/no questions, question_a and question_b, each followed by what a yes means. Both are "
    "asked about the same text. Reply 'same' if a correct yes to question_a always goes with a correct yes to "
    "question_b and a correct no with a correct no; 'opposite' if a correct yes to one always goes with a correct no "
    "to the other; 'unclear' if neither holds for certain, if what yes means does not fit its question, or a "
    "question is ungrammatical. Reply with JSON: a list of objects {\"qid\": <qid>, \"relation\": \"same\" | "
    "\"opposite\" | \"unclear\"}.")
DRAFT_FORMAT = ('[{"qid": "q...", "frames": ["Is it ... that", "..."]}, ...] for frame items; [{"qid": "q...", "pairs": '
                '[{"pos": "verb", "a": {"base": "...", "s3": "...", "past": "...", "pp": "..."}, "b": {...}, '
                '"cores_a": ["Does ...?", ...10], "cores_b": ["Does ...?", ...10]}, ...]}, ...] for pair items; for an '
                'adjective pair: {"pos": "adj", "a": {"base": "allowed", "adj": "allowed"}, "b": {...}, "cores_a": '
                '["Is ... allowed ...?", ...10], "cores_b": [...10]}')
POL_FORMAT = '[{"qid": "q...", "relation": "same" | "opposite" | "unclear"}, ...]'


def task_text(batch, chunk: dict, root: Path, *, title: str, answer_format: str) -> str:
    """One self-contained task file (same layout as t37b/author_pool.task_text): answer path, prompt, format, items."""
    ans = root / batch.answer_path(chunk["task_id"])
    n = len(chunk["items"])
    return "\n".join([
        f"# {title} {chunk['task_id']} (family {FAMILY}, kind {chunk['kind']})", "",
        "Read this whole file. Do not open any other file. When you are done, write your answer with the Write tool "
        "to exactly this path (nothing else, no other file):", "", f"    {ans}", "",
        f"The answer is one JSON list with exactly {n} objects, one per item below, each carrying that item's qid.", "",
        "## Instructions", "", batch.prompt, "", "## Answer format", "", answer_format, "",
        f"## Items ({n}; one JSON object per line)", "", "```json", "[",
        ",\n".join(json.dumps(it, ensure_ascii=False) for it in chunk["items"]), "]", "```", ""])


def task_files(batch, root: Path, *, title: str, answer_format: str, kind_label: str) -> tuple:
    files = dict(batch.files())
    rows = []
    for c in batch.chunks:
        rel = f"tasks/{c['task_id']}.md"
        files[rel] = task_text(batch, c, root, title=title, answer_format=answer_format)
        read, write = batch.allowed(str(root), c["task_id"])
        rows.append({"task_file": str(root / rel), "answer_file": str(root / batch.answer_path(c["task_id"])),
                     "kind": kind_label, "batch_id": batch.batch_id, "task_id": c["task_id"], "n_items": len(c["items"]),
                     "prompt_sha": batch.prompt_sha, "audit_allowed_read": sorted(read | {str(root / rel)}),
                     "audit_allowed_write": sorted(write)})
    return files, rows


def _batch(kind, items, seed, prompt, max_items=CHUNK):
    return chunker.make_batch(kind, FAMILY, items, seed=seed, prompt=prompt, max_items=max_items)


def _write(root: Path, batch, title: str, answer_format: str, kind_label: str, extra: dict | None = None,
           prereg_text=None) -> dict:
    files, rows = task_files(batch, root, title=title, answer_format=answer_format, kind_label=kind_label)
    man = {"family": FAMILY, "stage": kind_label, "batch_id": batch.batch_id, "prompt_sha": batch.prompt_sha,
           "seed": batch.seed, "n_tasks": len(rows), "n_items": len(batch.key), "tasks": rows, **(extra or {})}
    files["TASKS.json"] = json.dumps(man, indent=1, ensure_ascii=False) + "\n"
    paths.write_files(root, files, prereg_text=prereg_text)
    return man


# ------------------------------------------------------------------------------------------------ (a) draft

def draft_items() -> list:
    """Frame items (4 frames each) and pair items (2 pairs each). Targets: 24 pos-frame, 16 neg-frame candidates and 100
    pair candidates for >= 10 / 6 / 60 admitted."""
    out = []
    for i, st in enumerate(STYLES):
        out.append((f"draft|pos|{i}", {
            "brief": "Write 4 question openers, each ending with the word 'that', that ask whether the clause which "
                     "will follow is TRUE. Style: " + st + ".",
            "meaning": "asks whether what follows is true, and nothing else",
            "slots": [],
            "rules": ["start with Is, Would, Does, Could or Can", "3 to 8 words, one line, no comma, no question mark",
                      "no negative word of any kind (no not, n't, no, never, false, untrue, wrong ...)",
                      "the 4 openers must differ in their words, not only in one word",
                      "do not use 'Is it true that', 'Is it correct that' or 'Is it the case that'"]}))
    for i, st in enumerate(STYLES[:4]):
        out.append((f"draft|neg|{i}", {
            "brief": "Write 4 question openers, each ending with the word 'that', that ask whether the clause which "
                     "will follow is FALSE. Style: " + st + ".",
            "meaning": "asks whether what follows is false (not true), and nothing else",
            "slots": [],
            "rules": ["start with Is, Would, Does, Could or Can", "3 to 8 words, one line, no comma, no question mark",
                      "carry exactly one negative idea, in a word such as false, untrue, incorrect, wrong, mistaken, "
                      "inaccurate, or the words 'not the case'",
                      "never use a contraction such as isn't",
                      "do not use 'Is it false that' or 'Is it not the case that'"]}))
    n_pair_items = 30
    for i in range(n_pair_items):
        fld = FIELDS[i % len(FIELDS)]
        kind = "verb" if i % 2 == 0 else "adj"
        out.append((f"draft|pair|{i}", {
            "brief": f"Write {PAIRS_PER_ITEM} {'verb' if kind == 'verb' else 'adjective or participle'} pairs in the "
                     f"field '{fld}' (item {i}). In each pair, word b must be the EXACT complement of word a.",
            "meaning": "for any rule, notice, report or record, exactly one of 'X <a>' and 'X <b>' is true: never both, "
                       "never neither, no middle case",
            "slots": ["a", "b"] if kind == "verb" else ["a", "b"],
            "rules": (["each pair is {\"pos\": \"verb\", \"a\": {base, s3, past, pp}, \"b\": {base, s3, past, pp}, "
                       "\"cores_a\": [10 questions], \"cores_b\": [10 questions]}",
                       "a and b are single lower-case verbs; give base, third person singular (s3), past and past participle (pp)",
                       "cores_a: 10 different yes/no questions of the form 'Does <the thing> <a base> <something>?'",
                       "cores_b: 10 different questions of the same form that use b's base verb",
                       "each question starts with Does, one line, ends with ?, contains no negative word, and names a "
                       "different thing (notice, report, label, form, page, policy, contract, ...)"]
                      if kind == "verb" else
                      ["each pair is {\"pos\": \"adj\", \"a\": {base, adj}, \"b\": {base, adj}, \"cores_a\": [10 "
                       "questions], \"cores_b\": [10 questions]}",
                       "a and b are single lower-case words (adjectives or participles); base and adj are the same word",
                       "cores_a: 10 different yes/no questions of the form 'Is <the thing> <a> <rest>?' where the word a "
                       "is the first word after the thing",
                       "cores_b: 10 different questions of the same form with word b in that place",
                       "each question starts with Is or Are, one line, ends with ?, contains no negative word and no "
                       "word like every, some or all"]) +
                     [f"give exactly {PAIRS_PER_ITEM} pairs in the item's 'pairs' list", "the two pairs must not share a word"]}))
    for j, w in enumerate(TARGET_VERBS):                  # targeted: the predicate words of the live pools (G-block cores)
        out.append((f"draft|tpair|{j}", {
            "brief": f"Write 1 verb pair in which word a is exactly '{w}' and word b is its EXACT complement.",
            "meaning": "for any rule, notice, report or record, exactly one of 'X <a>' and 'X <b>' is true: never both, "
                       "never neither, no middle case",
            "slots": ["a", "b"],
            "rules": ["pair = {\"pos\": \"verb\", \"a\": {base, s3, past, pp}, \"b\": {base, s3, past, pp}, "
                      "\"cores_a\": [10 questions], \"cores_b\": [10 questions]}",
                      "single lower-case verbs; cores: 'Does <the thing> <base verb> <something>?', one line, no negative word",
                      "if no exact complement verb exists for a, write the closest one whose complement is exact for "
                      "records and notices, and make cores_a use a",
                      "give exactly 1 pair in the item's 'pairs' list"]}))
    for j, w in enumerate(TARGET_ADJS):
        out.append((f"draft|tpair|{len(TARGET_VERBS) + j}", {
            "brief": f"Write 1 adjective or participle pair in which word a is exactly '{w}' and word b is its EXACT complement.",
            "meaning": "for any rule, notice, report or record, exactly one of 'X is <a>' and 'X is <b>' is true: never both, "
                       "never neither, no middle case",
            "slots": ["a", "b"],
            "rules": ["pair = {\"pos\": \"adj\", \"a\": {base, adj}, \"b\": {base, adj}, \"cores_a\": [10 "
                      "questions], \"cores_b\": [10 questions]}",
                      "single lower-case words; cores: 'Is <the thing> <a> <rest>?' with the word right after the thing, "
                      "one line, no negative word, no every / some / all",
                      "give exactly 1 pair in the item's 'pairs' list"]}))
    return out


def draft_batch():
    return _batch("author_lexicon", draft_items(), "negtw-draft-v1", DRAFT_PROMPT, max_items=8)


def write_draft_tasks(root: Path = HERE / "haiku" / "draft", prereg_text=None) -> dict:
    return _write(root, draft_batch(), "Haiku lexicon drafting task", DRAFT_FORMAT, "author_lexicon:negtw_draft",
                  prereg_text=prereg_text)


def parse_draft(batch, raw: dict) -> tuple:
    """Raw answers -> ({'pos_frames', 'neg_frames', 'pairs'} after lint, problems). Nothing is admitted here (G-LEX next)."""
    ans, probs = chunker.load_answers(batch, raw)
    taken, out = L.seed_taken(), {"pos_frames": [], "neg_frames": [], "pairs": []}
    for iid, a in sorted(ans.items()):
        _, kind, _i = iid.split("|")
        if kind in ("pos", "neg"):
            key = "pos_frames" if kind == "pos" else "neg_frames"
            for f in (a.get("frames") if isinstance(a, dict) else None) or []:
                pr = L.lint_frame(f, "pos_frame" if kind == "pos" else "neg_frame", taken)
                if pr:
                    probs.append(f"{iid}: {f!r}: {pr[0]}")
                else:
                    taken.add(L.norm_frame(f))
                    out[key].append(f)
        else:
            for j, pr in enumerate((a.get("pairs") if isinstance(a, dict) else None) or []):
                pr = {**pr, "pair_id": f"P{kind[0]}{iid.split('|')[2]}_{j}"}
                if pr.get("pos") == "adj":
                    for s in ("a", "b"):
                        if isinstance(pr.get(s), dict):
                            pr[s]["adj"] = pr[s].get("adj") or pr[s].get("base")
                bad = L.lint_pair(pr)
                if bad:
                    probs.append(f"{iid}/{j}: {bad[0]}")
                else:
                    out["pairs"].append(pr)
    return out, probs


# ------------------------------------------------------------------------------------------------ (b) held-out

def heldout_items() -> list:
    out = []
    for slot, kind in H.SLOTS.items():
        if kind == "pos_frame":
            it = {"brief": f"Slot {slot}: write 4 question openers ending with the word 'that' that ask whether the "
                           "clause which follows is TRUE.",
                  "meaning": "asks whether what follows is true, and nothing else", "slots": [slot],
                  "rules": ["start with Is, Would, Does, Could or Can", "3 to 8 words, no comma, no question mark",
                            "no negative word of any kind", "not 'Is it true that', 'Is it correct that', 'Is it the "
                            "case that', 'Is it so that', 'Is it accurate that'"]}
        elif kind == "neg_frame":
            it = {"brief": f"Slot {slot}: write 4 question openers ending with the word 'that' that ask whether the "
                           "clause which follows is FALSE.",
                  "meaning": "asks whether what follows is false (not true), and nothing else", "slots": [slot],
                  "rules": ["start with Is, Would, Does, Could or Can", "3 to 8 words, no comma, no question mark",
                            "exactly one negative idea (false, untrue, incorrect, wrong, mistaken, inaccurate, or 'not "
                            "the case')", "no contraction", "not 'Is it false that' or 'Is it not the case that'"]}
        else:
            verb = kind == "verb_pair"
            it = {"brief": f"Slot {slot}: write 4 {'verb' if verb else 'adjective or participle'} pairs; in each, word "
                           "b is the EXACT complement of word a.",
                  "meaning": "for any rule, notice or record exactly one of 'X <a>' and 'X <b>' is true: never both, "
                             "never neither", "slots": ["a", "b"],
                  "rules": (["pair = {\"pos\": \"verb\", \"a\": {base, s3, past, pp}, \"b\": {base, s3, past, pp}, "
                             "\"cores_a\": [10 questions 'Does <thing> <a base> <something>?'], \"cores_b\": [10 same "
                             "form with b]}"] if verb else
                            ["pair = {\"pos\": \"adj\", \"a\": {base, adj}, \"b\": {base, adj}, \"cores_a\": [10 "
                             "questions 'Is <thing> <a> <rest>?'], \"cores_b\": [10 same form with b]}"]) +
                           ["single lower-case words", "questions: one line, no negative word, no every / some / all",
                            "choose rare or specialised words rather than the most common pair"]}
        out.append((f"heldout|{slot}", it))
    return out


def heldout_batch():
    return _batch("author_lexicon", heldout_items(), "negtw-heldout-v1", HELDOUT_PROMPT, max_items=8)


def write_heldout_tasks(root: Path = HERE / "haiku" / "heldout", prereg_text=None) -> dict:
    if not H.verify_frozen():
        raise RuntimeError("the held-out specs are not frozen (heldout.freeze) or were edited")
    freeze = json.loads(H.FREEZE_FILE.read_text())
    return _write(root, heldout_batch(), "Haiku held-out realisation task", DRAFT_FORMAT, "author_lexicon:negtw_heldout",
                  extra={"heldout_specs_sha256": freeze["sha256"], "n_slots": len(H.SLOTS)}, prereg_text=prereg_text)


def heldout_candidates(batch, raw: dict) -> tuple:
    """Raw held-out answers -> ({slot: [candidate frames | pair dicts]} after lint, problems). G-LEX comes next."""
    ans, probs = chunker.load_answers(batch, raw)
    out = {}
    for iid, a in sorted(ans.items()):
        slot = iid.split("|", 1)[1]
        kind = H.SLOTS[slot]
        if kind in ("pos_frame", "neg_frame"):
            taken = L.seed_taken() | {L.norm_frame(f) for f in []}
            good = []
            for f in (a.get("frames") or []):
                pr = L.lint_frame(f, kind, taken)
                if pr:
                    probs.append(f"{slot}: {f!r}: {pr[0]}")
                else:
                    taken.add(L.norm_frame(f))
                    good.append(f)
            out[slot] = good
        else:
            good = []
            for j, pr in enumerate(a.get("pairs") or []):
                pr = {**pr, "pair_id": f"{slot}_{j}"}
                if pr.get("pos") == "adj":
                    for sd in ("a", "b"):
                        if isinstance(pr.get(sd), dict):
                            pr[sd]["adj"] = pr[sd].get("adj") or pr[sd].get("base")
                bad = L.lint_pair(pr)
                if bad:
                    probs.append(f"{slot}/{j}: {bad[0]}")
                else:
                    good.append(pr)
            out[slot] = good
    return out, probs


def heldout_as_lexicon(cands: dict) -> dict:
    """The candidates as one lexicon dict, so write_glex_tasks(..., tag='heldout') probes them like any entry."""
    lex = {"pos_frames": [], "neg_frames": [], "pairs": []}
    for slot, lst in cands.items():
        key = {"pos_frame": "pos_frames", "neg_frame": "neg_frames"}.get(H.SLOTS[slot], "pairs")
        lex[key] += lst
    return lex


def choose_heldout(cands: dict, admitted: dict) -> dict:
    """{slot: the first G-LEX-admitted candidate in hash order}: the realisation H.freeze_realised logs. A slot with no
    admitted candidate stays out (its patterns are reported missing, never replaced)."""
    adm_f = set(admitted["pos_frames"]) | set(admitted["neg_frames"])
    adm_p = {p["pair_id"]: p for p in admitted["pairs"]}
    out = {}
    for slot, lst in cands.items():
        ok = [c for c in lst if (c in adm_f if isinstance(c, str) else c["pair_id"] in adm_p)]
        if ok:
            out[slot] = sorted(ok, key=lambda c: C.sha(slot + (c if isinstance(c, str) else c["pair_id"])))[0]
    return out


# ------------------------------------------------------------------------------------------------ G-LEX reads

def glex_batches(cands: dict, round_no: int, tag: str = "train") -> list:
    """[(batch, kind label)]: the two rounds use different seeds (separate chunks, separate agents)."""
    seed = f"negtw-glex-{tag}-r{round_no}-{GEN}"
    items = (L.frame_probe_items(cands.get("pos_frames", []), "pos_frame") +
             L.frame_probe_items(cands.get("neg_frames", []), "neg_frame") + L.pair_probe_items(cands.get("pairs", [])))
    return _batch("polarity", items, seed, GLEX_PROMPT) if items else None


def write_glex_tasks(cands: dict, round_no: int, tag: str = "train", prereg_text=None) -> dict:
    root = HERE / "haiku" / f"glex_{tag}_r{round_no}"
    b = glex_batches(cands, round_no, tag)
    return _write(root, b, "Haiku G-LEX read", POL_FORMAT, "polarity:negtw_glex", prereg_text=prereg_text)


# ------------------------------------------------------------------------------------------------ exactness

def exact_probe_cores(p: C.Pattern, pairs: dict, extra_cores: list = (), k: int = EXACT_PER_PATTERN) -> list:
    """k (base core, twin core) pairs for pattern p: bank cores first (diverse, hash order), then the live pool cores."""
    pool = list(PB.BANK.get(p.cls, [])) + list(extra_cores)
    pr = pairs.get(p.pair) if p.pair else None
    if pr:
        pool = list(pr["cores_a" if p.direction in ("a>b", "") else "cores_b"])
    out = []
    for c in sorted(set(pool), key=lambda c: C.sha(p.pid + "|" + c)):
        t, _q = C.apply(c, p, pairs)
        if t:
            out.append((c, t))
        if len(out) == k:
            break
    return out


def exact_items(patterns: list, pairs: dict, extra_cores: list = ()) -> tuple:
    items, short = [], []
    for p in patterns:
        pr = exact_probe_cores(p, pairs, extra_cores)
        if len(pr) < EXACT_PER_PATTERN:
            short.append(p.pid)
        for i, (a, b) in enumerate(pr):
            items.append((f"exact|{p.pid}|{i}", {"question_a": a, "question_b": b}))
    return items, short


def exact_seed(tag: str, gen: str = GEN) -> str:
    return f"negtw-exact-{tag}" + (f"-{gen}" if gen else "")


def write_exact_tasks(patterns: list, pairs: dict, tag: str, extra_cores: list = (), prereg_text=None, gen: str = GEN) -> dict:
    items, short = exact_items(patterns, pairs, extra_cores)
    b = _batch("polarity", items, exact_seed(tag, gen), EXACT_PROMPT)
    return _write(HERE / "haiku" / f"exact_{tag}", b, "Haiku exactness read", POL_FORMAT, "polarity:negtw_exact",
                  extra={"patterns": len(patterns), "pairs_per_pattern": EXACT_PER_PATTERN, "short_patterns": short},
                  prereg_text=prereg_text)


def exactness_decide(patterns: list, answers: dict) -> dict:
    """answers: {internal id: relation}. A pattern passes when the share of reads equal to its declared relation is
    >= 0.9 over its EXACT_PER_PATTERN pairs (an unclear or missing read counts as wrong). Haiku flags only: a failing
    pattern is dropped from the catalogue, nothing is edited or relabelled."""
    want = {"complement": "opposite", "equiv": "same"}
    res = {}
    for p in patterns:
        reads = [answers.get(f"exact|{p.pid}|{i}") for i in range(EXACT_PER_PATTERN)]
        good = sum(1 for r in reads if r == want[p.relation])
        res[p.pid] = {"good": good, "n": EXACT_PER_PATTERN, "rate": good / EXACT_PER_PATTERN,
                      "pass": good / EXACT_PER_PATTERN >= EXACT_MIN}
    return res


# ------------------------------------------------------------------------------------------------ card certificates

def card_items(types: dict) -> list:
    """types = {type key: (yes definition, no definition)} -> polarity items; the two definitions as statements."""
    def stmt(d: str) -> str:
        return "Is it the case that " + d.strip().rstrip(".;") + "?"
    return [(f"cardcert|{k}", {"question_a": stmt(y), "question_b": stmt(n)}) for k, (y, n) in sorted(types.items())]


def write_card_tasks(types: dict, round_no: int, prereg_text=None) -> dict:
    b = _batch("polarity", card_items(types), f"negtw-cardcert-r{round_no}-{GEN_CARD}", CARD_PROMPT)
    return _write(HERE / "haiku" / f"cardcert_r{round_no}", b, "Haiku card-complement read", POL_FORMAT,
                  "polarity:negtw_cardcert", prereg_text=prereg_text)


def card_decide(reads_1: dict, reads_2: dict) -> dict:
    """A base type may take complement twins only when BOTH reads say 'opposite' (2/2; anything else drops the type)."""
    return {i[len("cardcert|"):]: (reads_1.get(i) == reads_2.get(i) == "opposite") for i in reads_1}


# ------------------------------------------------------------------------------------------------ Sonnet audit

def audit_sample(twins: list, *, frac: float = AUDIT_FRAC, seed: str = "negtw-audit-v1") -> list:
    """Seeded 3% of twin rows, stratified by pattern: every pattern gets at least one row (so a pattern can be dropped
    on a confirmed error), the rest proportional to the pattern's size, hash order. twins: rows with meta.negtwin."""
    by = defaultdict(list)
    for r in twins:
        by[r["meta"]["negtwin"]["pattern"]].append(r)
    total = max(len(by), math.ceil(frac * len(twins)))
    quota = {pid: 1 for pid in by}
    extra = total - len(by)
    if extra > 0:
        w = {pid: len(v) for pid, v in by.items()}
        s = sum(w.values())
        floor = {pid: min(len(by[pid]) - 1, int(extra * w[pid] / s)) for pid in by}
        for pid, n in floor.items():
            quota[pid] += n
        rest = total - sum(quota.values())
        for pid in sorted(by, key=lambda p: (-(extra * w[p] / s - floor[p]), C.sha(seed + p))):
            if rest <= 0:
                break
            if quota[pid] < len(by[pid]):
                quota[pid] += 1
                rest -= 1
    out = []
    for pid, rows in by.items():
        rows = sorted(rows, key=lambda r: C.sha(seed + "|" + r["id"]))
        out += rows[:quota[pid]]
    return sorted(out, key=lambda r: r["id"])


def audit_items(pairs: list) -> list:
    """pairs: [(base_row, twin_row)] -> Sonnet polarity items with the 'yes means' definitions after each question."""
    from t37b import select as SEL
    items = []
    for b, t in pairs:
        _, cb = C.split_instruction(b["instructions"])
        _, ct = C.split_instruction(t["instructions"])
        yes = lambda c: (SEL.parse_card(c) or (c.replace("- yes: ", "", 1).strip(),))[0]      # noqa: E731
        items.append((f"audit|{t['id']}", {"question_a": f"{cb} (yes means: {yes(b['card'])})",
                                          "question_b": f"{ct} (yes means: {yes(t['card'])})"}))
    return items


def write_audit_tasks(pairs: list, prereg_text=None) -> dict:
    b = _batch("polarity", audit_items(pairs), "negtw-audit-v1", AUDIT_PROMPT)
    return _write(HERE / "haiku" / "audit", b, "Sonnet twin audit", POL_FORMAT, "polarity:negtw_audit",
                  extra={"reader": "sonnet", "fraction": AUDIT_FRAC}, prereg_text=prereg_text)


def audit_decide(sample: list, answers: dict, confirm=lambda tid: True) -> dict:
    """Drop rule (A42-D 7.3): a pattern with more than 3% error is dropped; a pattern with <= 33 audited rows is dropped
    on a single confirmed error. `confirm(twin id)` is the second look at a Sonnet disagreement (default: confirmed)."""
    want = {"complement": "opposite", "equiv": "same"}
    per = defaultdict(lambda: [0, 0, []])
    for r in sample:
        pid = r["meta"]["negtwin"]["pattern"]
        rel = answers.get(f"audit|{r['id']}")
        bad = rel != want[r["role"]] and confirm(r["id"])
        per[pid][0] += 1
        per[pid][1] += int(bad)
        if bad:
            per[pid][2].append(r["id"])
    res = {}
    for pid, (n, e, ids) in per.items():
        drop = e >= 1 if n <= AUDIT_SMALL else e / n > AUDIT_DROP_RATE
        res[pid] = {"audited": n, "errors": e, "drop": drop, "error_ids": ids}
    return res


def relations(answers: dict) -> dict:
    """chunker.load_answers output ({internal id: {"relation": ...}}) -> {internal id: relation string}."""
    return {k: (v.get("relation") if isinstance(v, dict) else v) for k, v in answers.items()}


def main(argv=None) -> int:
    import argparse
    ap = argparse.ArgumentParser(description="negtwins task writers (the orchestrator runs the agents)")
    ap.add_argument("stage", choices=["draft", "heldout", "exact_prog"])
    a = ap.parse_args(argv)
    if a.stage == "draft":
        man = write_draft_tasks()
    elif a.stage == "heldout":
        man = write_heldout_tasks()
    else:
        man = write_exact_tasks(C.build_catalogue(a48h=False), {}, "prog", gen="")
    print(json.dumps({k: man[k] for k in ("stage", "n_tasks", "n_items")}))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
