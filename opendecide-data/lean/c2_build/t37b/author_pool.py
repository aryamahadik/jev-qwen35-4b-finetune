"""t37b/author_pool.py: the T37b equiv paraphrase pool (G0_LITE_T37B.md v2: S12, H40, H41; A37 b).

Haiku's only T37b authoring job: paraphrase TEMPLATES of each registry question that takes equiv partners (fixed
questions as written; comve / taskmaster1 / cards questions with their {SLOT}s). The program fills the slots from each
base row, so Haiku never sees a state, a card, a gold or an option. Every syntactic, implicit, antonym and option-
framing partner is program-written (builder.program_partner): no Haiku task.

Stages (run from lean/; every writer goes through c2_kit.paths and refuses before A38 or while builder.g0_problems()):
  tasks   ../.venv/bin/python c2_build/t37b/author_pool.py tasks
          -> haiku/author/: chunks, prompt, key, manifest, one self-contained task file per chunk (tasks/<id>.md, it
             names its answer file), TASKS.json. The Haiku authors write haiku/author/answers/<task id>.json.
  lint    ../.venv/bin/python c2_build/t37b/author_pool.py lint
          -> loads the answers (chunker.load_answers), checks each paraphrase (one line, '?', placeholders exactly the
             entry's slots, local bans, BOTH polarity programs read 'same' on every probe fill), dedups, and writes the
             two independent polarity reads (kind polarity, separate seeds and chunks) to haiku/extract/ (TASKS.json).
  admit   ../.venv/bin/python c2_build/t37b/author_pool.py admit
          -> loads both reads; a paraphrase is admitted only when BOTH read 'same'; freezes pools/t37b_equiv_pool.json
             and pools/MANIFEST.json (sha256s, counts per entry, targets, shortfalls; targets are never lowered).
  status  prints what exists.
The build then uses load_pool(): Pool.choices() for select.plan_block(equiv_pool=...), Pool.records for
builder.build_candidates(records=...), Pool.judged for builder.polarity_batches(judged=...).
"""
from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
from collections import Counter
from dataclasses import dataclass, field
from pathlib import Path

_C2_BUILD = Path(__file__).resolve().parents[1]
if str(_C2_BUILD) not in sys.path:
    sys.path.insert(0, str(_C2_BUILD))

from c2_kit import chunker, paths  # noqa: E402
from t37b import builder as BL  # noqa: E402
from t37b import polarity as PA  # noqa: E402
from t37b import polarity_b as PB  # noqa: E402
from t37b import sources as SRC  # noqa: E402

HERE = Path(__file__).resolve().parent
FAMILY = "T37b"
AUTHOR_DIR = HERE / "haiku" / "author"
EXTRACT_DIR = HERE / "haiku" / "extract"
POOL_DIR = HERE / "pools"
POOL_FILE = POOL_DIR / "t37b_equiv_pool.json"
SEED_AUTHOR = "t37b-pool-author-v1"
SEED_POLARITY = "t37b-pool-polarity-v1"
PER_ITEM = 5                       # paraphrases asked per authoring item
CHUNK = 8                          # items per authoring task (8 x 5 = 40 questions per Haiku agent)
POL_CHUNK = 50
ITEMS_FIXED, ITEMS_SLOTTED = 3, 5  # authoring items per entry (fixed question: 15 paraphrases; slotted: 25)
TARGET_FIXED, TARGET_SLOTTED = 7, 12   # admitted paraphrases wanted per entry (report only; never lowered)
MAX_TASKS = 40

# Strings no authoring item or prompt may contain (chunker forbid_strings): the answer words, every truth frame
# (training and held-out dev), and the banned dev / eval patterns (builder.LOCAL_BANS).
FORBID = ("yes", "no", "correct answer", "wrong to answer", "should the statement that", "be rejected", "only non-") \
    + tuple(f.lower() for f in SRC.FRAMES_TRAIN + SRC.FRAMES_DEV)

AUTHOR_POOL_PROMPT = (
    "You rewrite questions for a reading test. Each item gives one question, or a question template whose words in "
    "capital letters inside curly braces are placeholders, plus rules. For each item write exactly as many new "
    "questions as the item's rules ask for. Every new question must ask exactly the same thing as the item's question: "
    "a reader who knows the facts must give the same answer to both, in every possible case. Do not answer the "
    "question, do not explain, and do not add facts, names or numbers. Reply with JSON only: a list with one object "
    "per item, {\"qid\": <the item's qid>, \"questions\": [<question 1>, ..., <question k>]}. Every question is one "
    "line ending with a question mark, and all of them differ from each other and from the item's question.")
POOL_POLARITY_PROMPT = BL.POLARITY_PROMPT + (
    " Words in capital letters inside curly braces, such as {N}, are placeholders: each one stands for the same value "
    "in both questions.")

STYLE_HINTS = (
    "keep the main verb but change the word order",
    "use a different verb or phrase with exactly the same meaning",
    "turn the sentence around so that what is being checked comes first (for example a passive form)",
    "open with a short phrase that says where to look, such as 'Based on the text,' or 'Going by the text,'",
    "make it as short as you can while keeping every condition",
    "make it a little more formal",
    "make it a little more conversational, in plain everyday words",
    "put the main condition at the end of the question",
    "use a noun instead of the main verb where that keeps the meaning (for example 'Is there confirmation that ...')",
    "start with a different first word than the question does",
    "describe the text being read with a different but equal phrase",
    "split a long phrase into simpler words, keeping every condition",
    "name the text first with 'According to' or 'In', then ask",
    "change two or three words for exact synonyms and keep the rest",
    "write it as one plain sentence with as few commas as possible",
)

SLOT_TEXT = {
    "N": "{N} stands for the number of one of the two statements the reader sees. Always write it as 'Statement {N}' "
         "(capital S), name the asked-about statement only that way, ask about Statement {N} itself (never about "
         "the other statement), and do not start the question with the word Statement.",
    "SPAN": "{SPAN} stands for a short value quoted from the conversation, quotation marks included (for example a "
            "time, a place or an item). Write {SPAN} as it is, without adding quotation marks around it.",
    "ORDER": "{ORDER} stands for a phrase that starts with \"the customer's\" and names what the customer wanted (for "
             "example the customer's pizza order). Write {ORDER} as it is, without a word such as 'the' before it.",
    "CLAIM": "{CLAIM} stands for a clause stating one contrarian claim about the climate. End the question with the "
             "exact words 'the contrarian climate claim that {CLAIM}' followed by the question mark.",
}
# Probe values for the lint fills (from the golden_src builders' own constants: taskmaster1 VERT, cards SUPER).
PROBES = {
    "N": ("1", "2"),
    "SPAN": ("\"7 pm\"", "\"Blue Door Cafe\"", "\"two large lattes\""),
    "ORDER": ("the customer's ride booking", "the customer's movie ticket order", "the customer's restaurant "
              "reservation", "the customer's coffee order", "the customer's pizza order",
              "the customer's car repair appointment"),
    "CLAIM": ("global warming is not happening", "human greenhouse gases are not causing climate change",
              "climate impacts are not bad or are beneficial", "climate solutions won't work",
              "climate science or the climate movement is unreliable"),
}
KEEP_EXTRA = ("actually", "common")        # condition words a paraphrase keeps although no program list holds them
_NEG_WORDS = ("not", "n't", "never", "none", "nobody", "nothing", "nowhere", "neither", "nor", "without", "cannot",
              "fail", "lack", "refuse", "deny", "unless", "except", "hardly", "scarcely", "barely", "few", "false",
              "neglect", "omit", "decline", "prevent")


def sha(s: str) -> str:
    return hashlib.sha256(s.encode()).hexdigest()


def norm(text: str) -> str:
    return " ".join((text or "").split()).lower()


# ------------------------------------------------------------------------------------------------ authoring tasks

def pool_entries() -> list:
    """Registry entries that take a pool (equiv kind, a template, not NO_POOL), in registry order."""
    return [e for e in SRC.ENTRIES if SRC.pool_template(e) is not None]


def _closed_words(text: str) -> Counter:
    lists = PA.QUANT | PB.QUANT_B | PA.MODAL | PB.MODAL_B | set(_NEG_WORDS) | PB.NEG_B | set(KEEP_EXTRA)
    toks = [w for w in PB.tokens(re.sub(r"\{[A-Z_]+\}", " ", text)) if not w.startswith('"')]
    return Counter(w for w in toks if w in lists)


def keep_words(entry) -> list:
    """Closed-list words of the entry's template (outside the slots) a paraphrase must keep, with their counts."""
    c = _closed_words(SRC.pool_template(entry)[0])
    return [f"'{w}'" + (f" ({n} times)" if n > 1 else "") for w, n in sorted(c.items())]


def banned_words(entry) -> list:
    keep = set(_closed_words(SRC.pool_template(entry)[0]))
    words = (PA.QUANT | PB.QUANT_B | PA.MODAL | PB.MODAL_B | set(_NEG_WORDS)) - keep - {"no", "yes", "wo"}
    return sorted(a for _p, a in entry.antonyms) + sorted(words)


def rules_for(entry, group: int) -> list:
    """The closed rules of one authoring item (G0 H40): k style hints, keep / ban lists, placeholders."""
    tpl, slots = SRC.pool_template(entry)
    hints = [STYLE_HINTS[(group * PER_ITEM + i) % len(STYLE_HINTS)] for i in range(PER_ITEM)]
    rules = [f"Write {PER_ITEM} questions; question i follows style hint i: "
             + "; ".join(f"({i + 1}) {h}" for i, h in enumerate(hints)) + ".",
             "Ask exactly the same thing: keep every condition, every person or thing the question names, and the "
             "same time and source (for example 'last message', 'by the end of this conversation').",
             "Ask the question directly: do not open with a phrase that asks whether a statement holds, do not ask "
             "about an answer or an option, and do not ask for an opinion."]
    kw = keep_words(entry)
    if kw:
        rules.append("Keep each of these words, exactly as many times as in the question: " + ", ".join(kw) + ".")
    rules.append("Do not use any of these words or phrases: " + ", ".join(banned_words(entry)) + "; and do not add "
                 "any other negative word.")
    caps = "Use a capital letter only for the first word of the question"
    rules.append(caps + (" and for the word Statement before {N}." if "N" in slots else ".") + " Do not use digits.")
    if slots:
        rules.append("Use each placeholder exactly once, written exactly as shown, and do not use any other "
                     "placeholder: " + ", ".join("{" + s + "}" for s in slots) + ".")
        rules += [SLOT_TEXT[s] for s in slots]
    return rules


def author_items() -> list:
    """[(internal id, author_wording item)]: ITEMS_FIXED or ITEMS_SLOTTED items per pool entry."""
    out = []
    for e in pool_entries():
        tpl, slots = SRC.pool_template(e)
        n = ITEMS_SLOTTED if slots else ITEMS_FIXED
        for g in range(n):
            brief = ("Question template: " if slots else "Question: ") + tpl
            out.append((f"t37b-pool|{e.key}|g{g}", {"brief": brief, "slots": sorted(slots), "rules": rules_for(e, g)}))
    return out


def author_batch():
    return chunker.make_batch("author_wording", FAMILY, author_items(), seed=SEED_AUTHOR, prompt=AUTHOR_POOL_PROMPT,
                              max_items=CHUNK, forbid_strings=FORBID)


def task_text(batch, chunk: dict, root: Path, *, title: str, answer_format: str) -> str:
    """One self-contained task file: the exact answer path, the prompt and the chunk's items."""
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
    """({relative path: text}, TASKS.json rows) for a batch written under root."""
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


AUTHOR_FORMAT = '[{"qid": "q...", "questions": ["...?", "...?", "...?", "...?", "...?"]}, ...]'
POLARITY_FORMAT = '[{"qid": "q...", "relation": "same" | "opposite" | "unclear"}, ...]'
README = """# T37b Haiku pool (G0_LITE_T37B.md v2, S12 / H40-H41)

T37b's only Haiku authoring: paraphrase templates for the equiv pool (author_wording; answers in answers/<task id>.json).
Every complement partner is program-written, so there are no skins, packs, registers or documents for T37b.

Next stages (run from lean/; never edit labels; Haiku answers only admit or drop a paraphrase):
  lint:  ../.venv/bin/python c2_build/t37b/author_pool.py lint
         (loads these answers, checks them with both polarity programs, dedups, writes ../extract/: two independent
         polarity reads per paraphrase in separate chunks; tasks listed in ../extract/TASKS.json)
  admit: ../.venv/bin/python c2_build/t37b/author_pool.py admit
         (admits a paraphrase only when both reads say 'same'; freezes ../../pools/)
"""


def write_author_tasks(root: Path = AUTHOR_DIR, prereg_text: str | None = None) -> dict:
    paths.require_a38(prereg_text)
    BL.require_g0()
    b = author_batch()
    if len(b.chunks) > MAX_TASKS:
        raise ValueError(f"{len(b.chunks)} authoring tasks > {MAX_TASKS}")
    files, rows = task_files(b, root, title="Haiku authoring task", answer_format=AUTHOR_FORMAT,
                             kind_label="author_wording:equiv_pool")
    man = {"family": FAMILY, "stage": "author", "seed": SEED_AUTHOR, "g0_sha256": BL.G0_SHA256,
           "g0_haiku_task": BL.G0_HAIKU_TASK, "n_tasks": len(rows), "n_items": len(b.key),
           "n_questions_asked": len(b.key) * PER_ITEM, "batch_id": b.batch_id, "prompt_sha": b.prompt_sha,
           "entries": {e.key: (ITEMS_SLOTTED if SRC.pool_template(e)[1] else ITEMS_FIXED) for e in pool_entries()},
           "next": "author_pool.py lint (see README.md)", "tasks": rows}
    files["TASKS.json"] = json.dumps(man, indent=1, ensure_ascii=False) + "\n"
    files["README.md"] = README
    paths.write_files(root, files, prereg_text=prereg_text)
    return man


# ------------------------------------------------------------------------------------------------ lint

def _questions(ans) -> list:
    if isinstance(ans, dict):
        for k in ("questions", "question", "text"):
            if k in ans:
                ans = ans[k]
                break
    if isinstance(ans, str):
        ans = [ans]
    return [" ".join(q.split()) for q in ans if isinstance(q, str)] if isinstance(ans, list) else []


def lint_one(entry, text: str) -> list:
    """Problems of one paraphrase template (empty = passes lint). Both polarity programs must read 'same' on every
    probe fill; placeholders exactly the entry's slots, once each."""
    tpl, slots = SRC.pool_template(entry)
    probs = []
    if not text or "\n" in text or not text.endswith("?") or text.count("?") != 1:
        return ["not one question on one line ending in '?'"]
    ph = SRC.placeholders(text)
    if sorted(ph) != sorted(slots) or len(set(ph)) != len(ph):
        probs.append(f"placeholders {ph} != {sorted(slots)}")
    if re.search(r"[{}]", re.sub(r"\{[A-Z][A-Z_]*\}", "", text)):
        probs.append("stray brace")
    if norm(text) == norm(tpl):
        probs.append("equals the question")
    n_words = len(text.split())
    if not 4 <= n_words <= 60:
        probs.append(f"{n_words} words")
    probs += [f"local ban {b}" for b in BL.local_ban_hits(text)]
    if re.search(r"\b(?:yes|no)\b", text, re.I):
        probs.append("answer word")
    if probs:
        return probs
    names = sorted(slots)
    fills = [{}]
    for s in names:
        fills = [dict(f, **{s: v}) for f in fills for v in PROBES[s]]
    for f in fills:
        base, para = SRC.fill(tpl, f), SRC.fill(text, f)
        ra, pa = PA.classify_a(base, para, "equiv", entry, SRC.FRAMES_TRAIN)
        rb, pb = PB.classify_b(base, para, "equiv", entry, SRC.FRAMES_TRAIN)
        if ra != "same" or rb != "same":
            return [f"programs read {ra!r} / {rb!r} on a probe fill: {(pa + pb)[:2]}"]
    return []


def record(entry_key: str, template: str, task_id: str, prompt_sha: str) -> dict:
    """One pool record. Keys follow g13_c2's pool convention: metadata under its POOL_META names, so G13 seed-first
    reads only the paraphrase text ('template')."""
    e = SRC.ENTRY_BY_KEY[entry_key]
    return {"template_id": "p" + sha(f"{entry_key}|{norm(template)}")[:12], "sem": entry_key, "qform": "equiv",
            "slots": sorted(SRC.pool_template(e)[1]), "template": template, "haiku_task_id": task_id,
            "haiku_prompt_sha": prompt_sha}


def base_template(rec: dict) -> str:
    return SRC.pool_template(SRC.ENTRY_BY_KEY[rec["sem"]])[0]


def rec_pair_key(rec: dict) -> str:
    return BL.pair_key(base_template(rec), rec["template"])


def lint(batch, raw: dict) -> tuple:
    """(candidates, report). raw: {task id: answer object}. A paraphrase that fails any check is dropped (logged)."""
    answers, load_probs = chunker.load_answers(batch, raw)
    by_entry = {e.key: e for e in pool_entries()}
    qid_of = {v: q for q, v in batch.key.items()}
    cands, seen, drops = [], set(), Counter()
    per_entry = Counter()
    for iid in sorted(answers):
        ekey = iid.split("|")[1]
        e = by_entry[ekey]
        tid = batch.task_of[qid_of[iid]]
        for k, q in enumerate(_questions(answers[iid])):
            probs = lint_one(e, q)
            if probs:
                drops[probs[0].split(":")[0][:60]] += 1
                continue
            key = (ekey, norm(q))
            if key in seen:
                drops["duplicate"] += 1
                continue
            seen.add(key)
            cands.append(record(ekey, q, tid, batch.prompt_sha) | {"author_item": iid, "k": k})
            per_entry[ekey] += 1
    rep = {"answered_items": len(answers), "items": len(batch.key), "load_problems": load_probs,
           "questions": sum(len(_questions(a)) for a in answers.values()), "passed": len(cands),
           "dropped": dict(drops.most_common()), "passed_by_entry": dict(sorted(per_entry.items()))}
    return cands, rep


def polarity_batches(cands: list) -> tuple:
    items = [(rec_pair_key(c), {"question_a": base_template(c), "question_b": c["template"]}) for c in cands]
    if not items:
        return None, None
    a = chunker.make_batch("polarity", FAMILY, items, seed=f"{SEED_POLARITY}|A", prompt=POOL_POLARITY_PROMPT,
                           max_items=POL_CHUNK)
    b = chunker.make_batch("polarity", FAMILY, items, seed=f"{SEED_POLARITY}|B", prompt=POOL_POLARITY_PROMPT,
                           max_items=POL_CHUNK)
    return a, b


def _read_answers(root: Path, batch) -> dict:
    raw = {}
    for c in batch.chunks:
        p = root / batch.answer_path(c["task_id"])
        if paths.never_open(p) is None and p.is_file():
            try:
                raw[c["task_id"]] = json.loads(p.read_text(encoding="utf-8"))
            except json.JSONDecodeError:
                raw[c["task_id"]] = []
    return raw


def run_lint(author_root: Path = AUTHOR_DIR, extract_root: Path = EXTRACT_DIR, prereg_text: str | None = None) -> dict:
    paths.require_a38(prereg_text)
    BL.require_g0()
    b = author_batch()
    man = json.loads((author_root / "TASKS.json").read_text(encoding="utf-8"))
    if man.get("batch_id") != b.batch_id:
        raise RuntimeError(f"the authoring batch changed since the tasks were written ({man.get('batch_id')} != "
                           f"{b.batch_id}): rebuild the tasks, do not mix")
    cands, rep = lint(b, _read_answers(author_root, b))
    rep["answered_tasks"] = sum(1 for c in b.chunks if (author_root / b.answer_path(c["task_id"])).is_file())
    paths.write_json(author_root / "lint" / "candidates.json", {"family": FAMILY, "candidates": cands},
                     prereg_text=prereg_text)
    paths.write_json(author_root / "lint" / "report.json", rep, prereg_text=prereg_text)
    pa, pb = polarity_batches(cands)
    rows, files = [], {}
    for lab, bt in (("A", pa), ("B", pb)):
        if bt is None:
            continue
        f, r = task_files(bt, extract_root, title=f"Haiku polarity read {lab}", answer_format=POLARITY_FORMAT,
                          kind_label=f"polarity:{lab}")
        files.update(f)
        rows += r
    xman = {"family": FAMILY, "stage": "extract (two independent polarity reads; G0 H41)", "seed": SEED_POLARITY,
            "g0_sha256": BL.G0_SHA256, "n_tasks": len(rows), "n_pairs": len(cands),
            "batch_ids": [x.batch_id for x in (pa, pb) if x is not None], "next": "author_pool.py admit",
            "tasks": rows}
    files["TASKS.json"] = json.dumps(xman, indent=1, ensure_ascii=False) + "\n"
    paths.write_files(extract_root, files, prereg_text=prereg_text)
    return {"lint": rep, "extract_tasks": len(rows)}


# ------------------------------------------------------------------------------------------------ admission and pool

def admit(cands: list, ans_a: dict, ans_b: dict) -> tuple:
    """(admitted records, report): admitted iff both reads are 'same' (anything else drops; G0 H41, H60)."""
    out, drops = [], Counter()
    for c in cands:
        k = rec_pair_key(c)
        ra, rb = BL.norm_relation(ans_a.get(k)), BL.norm_relation(ans_b.get(k))
        if ra == rb == "same":
            out.append({kk: v for kk, v in c.items() if kk not in ("author_item", "k")} | {"reads": [ra, rb],
                                                                                         "status": "admitted"})
        else:
            drops[f"{ra}/{rb}"] += 1
    per = Counter(c["sem"] for c in out)
    targets = {e.key: (TARGET_SLOTTED if SRC.pool_template(e)[1] else TARGET_FIXED) for e in pool_entries()}
    rep = {"candidates": len(cands), "admitted": len(out), "dropped": dict(drops), "by_entry": dict(sorted(per.items())),
           "targets": targets, "shortfall": {k: t - per[k] for k, t in targets.items() if per[k] < t}}
    return out, rep


def run_admit(author_root: Path = AUTHOR_DIR, extract_root: Path = EXTRACT_DIR, pool_dir: Path = POOL_DIR,
              prereg_text: str | None = None) -> dict:
    paths.require_a38(prereg_text)
    BL.require_g0()
    cands = json.loads((author_root / "lint" / "candidates.json").read_text(encoding="utf-8"))["candidates"]
    pa, pb = polarity_batches(cands)
    if pa is None:
        raise RuntimeError("no lint candidates: nothing to admit")
    xman = json.loads((extract_root / "TASKS.json").read_text(encoding="utf-8"))
    if xman.get("batch_ids") != [pa.batch_id, pb.batch_id]:
        raise RuntimeError("the polarity batches changed since the extract tasks were written")
    ans = {}
    for lab, bt in (("A", pa), ("B", pb)):
        got, probs = chunker.load_answers(bt, _read_answers(extract_root, bt))
        ans[lab] = got
        ans[lab + "_problems"] = probs
    admitted, rep = admit(cands, ans["A"], ans["B"])
    rep["load_problems"] = {"A": ans["A_problems"], "B": ans["B_problems"]}
    pool = {"family": FAMILY, "g0_sha256": BL.G0_SHA256, "frozen": True,
            "paraphrases": sorted(admitted, key=lambda c: (c["sem"], c["template_id"]))}
    body = json.dumps(pool, indent=1, ensure_ascii=False, sort_keys=True) + "\n"
    paths.write_text(pool_dir / POOL_FILE.name, body, prereg_text=prereg_text)
    man = {"family": FAMILY, "pool_file": POOL_FILE.name, "sha256": sha(body), "report": rep,
           "polarity_batch_ids": [pa.batch_id, pb.batch_id], "author_batch_id": author_batch().batch_id}
    paths.write_json(pool_dir / "MANIFEST.json", man, prereg_text=prereg_text)
    return man


@dataclass
class Pool:
    paraphrases: list = field(default_factory=list)      # admitted records (record() + reads, status)

    def choices(self) -> dict:
        """{entry key: [(template_id, paraphrase template)]} for select.plan_block(equiv_pool=...)."""
        out: dict = {}
        for c in self.paraphrases:
            out.setdefault(c["sem"], []).append((c["template_id"], c["template"]))
        return out

    @property
    def records(self) -> dict:
        return {c["template_id"]: c for c in self.paraphrases}

    @property
    def judged(self) -> dict:
        """{pair_key: (read A, read B)} of the admitted paraphrases (builder.polarity_of / polarity_batches)."""
        return {rec_pair_key(c): tuple(c["reads"]) for c in self.paraphrases}


def load_pool(path: Path = POOL_FILE) -> Pool:
    obj = json.loads(Path(path).read_text(encoding="utf-8"))
    if not obj.get("frozen") or obj.get("g0_sha256") != BL.G0_SHA256:
        raise RuntimeError("the T37b pool is not frozen under the current G0-lite spec")
    recs = obj["paraphrases"]
    if any(c.get("status") != "admitted" or list(c.get("reads", ())) != ["same", "same"] for c in recs):
        raise RuntimeError("the T37b pool holds a record that was not admitted by two 'same' reads")
    return Pool(recs)


def pool_strings(pool: Pool) -> list:
    """Admitted paraphrase templates, for G13 seed-first (method 8) before any row uses them (G0 H53)."""
    return [c["template"] for c in pool.paraphrases]


def status() -> dict:
    a = AUTHOR_DIR / "TASKS.json"
    out = {"author_tasks": None, "answers": 0, "lint": None, "extract_tasks": None, "pool": None}
    if a.is_file():
        man = json.loads(a.read_text(encoding="utf-8"))
        out["author_tasks"] = man["n_tasks"]
        out["answers"] = sum(1 for t in man["tasks"] if Path(t["answer_file"]).is_file())
    if (AUTHOR_DIR / "lint" / "report.json").is_file():
        out["lint"] = json.loads((AUTHOR_DIR / "lint" / "report.json").read_text(encoding="utf-8"))
    if (EXTRACT_DIR / "TASKS.json").is_file():
        out["extract_tasks"] = json.loads((EXTRACT_DIR / "TASKS.json").read_text(encoding="utf-8"))["n_tasks"]
    if (POOL_DIR / "MANIFEST.json").is_file():
        out["pool"] = json.loads((POOL_DIR / "MANIFEST.json").read_text(encoding="utf-8"))["report"]
    return out


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("stage", choices=("tasks", "lint", "admit", "status"))
    a = ap.parse_args(argv)
    if a.stage == "tasks":
        man = write_author_tasks()
        res = {k: man[k] for k in ("n_tasks", "n_items", "n_questions_asked", "batch_id")}
    elif a.stage == "lint":
        res = run_lint()
    elif a.stage == "admit":
        res = run_admit()["report"]
    else:
        res = status()
    print(json.dumps(res, indent=1, ensure_ascii=False, default=str))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
