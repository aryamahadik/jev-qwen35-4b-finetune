"""families/T24/redo2.py: T24 supplementary Haiku tasks (redo2) for the Mode F e-mail blocker (G0_SPEC v2.1: section
3.2 and the v2.1 line of section 5; C2_DATA_SPEC 3.0 Mode F, 6.3 G-SL and G3-H). A new file. NEW items, new opaque
ids, new answer paths: no earlier task, answer, key or pool and no pinned file (authoring.py, extract_stage.py,
pool_freeze.py, lean/*.py) changes. No gate bar, G0 target, field or gold semantics changes. After A38 only: every
write goes through c2_kit.paths.

Blocker (G3-H; a re-read cannot fix it). The v1 e-mail format "a short e-mail from the customer (a greeting, the
message, a sign-off)" let 10 of the 20 v1 e-mails (task free-a) put the customer's name only in the greeting ("Hi
<name>,"): the named person is the addressee, the writer is unnamed, and the G3-H field "customer" (the person who raised
the case) is correctly null. The register reads 10/20 < 98%, so the v1 e-mail template is quarantined (all 20 dropped).
That stays so. This file writes a NEW e-mail authoring task whose prompt states the writer rule of G0 3.2: the greeting
names nobody; the name stands alone on the last line below the sign-off, or in a self-introduction in the first
sentence. The new prompt is a new G3-H template (G0 3.2: one register under one authoring prompt sha) and must reach 98%
on its own. The v1 read prompt and field schema are reused unchanged.

Stages (each later stage rebuilds the earlier ones in memory and stops if a file on disk differs):
  author   haiku/redo2/: tasks/<task_id>.md (self-contained: answer path, inline answer contract, prompt, items),
           chunks/, prompts/, key/ (orchestrator only), manifest/, TASKS.json, answers/ (written only by the agent).
  extract  after the author answer exists: answer shape -> the v1 Mode F lint unchanged (authoring.check_freeform =
           G-SL lint_freeform, extract_stage.freeform_rule_problems) + the e-mail writer check (email_role_problems,
           the new prompt's rules 7-10; it only drops) -> dedup inside redo2 and against every v1 Mode F text -> one
           G3-H read (g3h-r2) under haiku/redo2/extract/ (tasks/<task_id>.md self-contained; pieces.json orchestrator
           only).
  admit    after the read answer exists: g3h.compare per document (a mismatch is dropped), g3h.template_report per
           template (>= 98%, else every document of the template is dropped), then the SUPPLEMENT pools/redo2/
           (documents.jsonl, quarantine.jsonl, MANIFEST.json). pools/ (pool_freeze.py output) is not touched; Mode F
           rows draw from pools/documents.jsonl plus pools/redo2/documents.jsonl.

  ../../.venv/bin/python -m families.T24.redo2 author  [--write]     (from lean/c2_build)
  ../../.venv/bin/python -m families.T24.redo2 extract [--write]
  ../../.venv/bin/python -m families.T24.redo2 admit   [--write]
"""
from __future__ import annotations

import hashlib
import json
import re
import sys
from collections import Counter
from dataclasses import dataclass
from pathlib import Path

HERE = Path(__file__).resolve().parent
C2_BUILD = HERE.parents[1]
if str(C2_BUILD) not in sys.path:
    sys.path.insert(0, str(C2_BUILD))

from c2_kit import chunker, g3h, paths  # noqa: E402
from families.T24 import authoring as A  # noqa: E402
from families.T24 import extract_stage as X  # noqa: E402
from families.T24 import plugin as P  # noqa: E402

FAMILY = P.FAMILY
VERSION = "r2"
ROOT = HERE / "haiku" / "redo2"
EX_ROOT = ROOT / "extract"
POOLS = HERE / "pools"
SUPP = POOLS / "redo2"
G3H_READ = "g3h-r2"
REGISTER = "email"
N_EMAIL = 50                     # one chunk (the kit maximum); at >= 50 read documents one G3-H miss still clears 98%
INTRO_SLOTS = (1, 3)             # item i with i % 5 in INTRO_SLOTS: self-introduction (20 of 50); else sign-off (30)
BLOCKER = "BLOCKER 1: Mode F e-mail register, G3-H"
NEED = ("a new e-mail template (new authoring prompt) that reaches G3-H >= 98% on its own; the v1 e-mail template "
        "stays quarantined (10/20: the name only in the greeting)")


def sha_text(s: str) -> str:
    return hashlib.sha256(s.encode("utf-8")).hexdigest()


def sha_file(p: Path) -> str:
    return hashlib.sha256(Path(p).read_bytes()).hexdigest()


# ------------------------------------------------------------------------------------------------ the e-mail prompt
EMAIL_FORMAT = ("a short e-mail that the customer writes to the support team about their own case (a greeting line, "
                "the message, a sign-off)")
GREETING_RULE = ("the greeting line is written to the support team and names nobody (such as 'Hello,' or 'Dear support "
                 "team,')")
PLACE = {
    "signoff": ("the customer signs the e-mail: a sign-off line (such as 'Kind regards,') and then the customer's name "
                "alone on the last line"),
    "intro": ("the customer introduces themself in the first sentence of the message (such as 'This is ..., writing "
              "about my case.' or 'My name is ... and I am writing about my request.'); the sign-off line is the last "
              "line and holds no name"),
}
EMAIL_RULES = """
E-mail rules (every item of this task is an e-mail written BY the customer; an e-mail that breaks one is thrown away):
7. The CUSTOMER is the person who raised the case and the WRITER of the e-mail. The e-mail goes from the customer to
   the support team: never write it to the customer, and never greet the customer.
8. Three parts on separate lines (single line breaks, never an empty line): a greeting line, the message (two or three
   sentences), and the sign-off.
9. The greeting line names nobody: it greets the support team, as in "Hello,", "Hi there,", "Good day," or "Dear
   support team,". The customer's name never appears in the greeting line.
10. Put the customer's name where the item's rules say, and nowhere else: EITHER alone on the very last line, directly
   below a sign-off line such as "Kind regards," or "Thanks,"; OR in a self-introduction in the first sentence of the
   message, as in "This is ..., writing about my case." or "My name is ... and I am writing about my request." (then
   the sign-off line is the last line and holds no name).
"""
_ANSWER = A._answer_block("text")
assert A.FREEFORM_PROMPT.endswith(_ANSWER)
# The v1 Mode F prompt (task text and hard rules 1-6) unchanged, plus the e-mail rules 7-10 before the answer format.
EMAIL_PROMPT = A.FREEFORM_PROMPT[: -len(_ANSWER)] + EMAIL_RULES + _ANSWER
EMAIL_SITUATIONS = tuple(s for s in A.CUSTOMER_SITUATIONS if "person second" not in s)   # the name may come first


def email_items() -> tuple:
    """([(internal id, item)], {internal id: meta}): 50 e-mails, every T24 customer name, 30 sign-off + 20 intro."""
    items, meta = [], {}
    for i in range(N_EMAIL):
        place = "intro" if i % 5 in INTRO_SLOTS else "signoff"
        name = P.CUSTOMERS[(i * 3) % len(P.CUSTOMERS)]
        sit = EMAIL_SITUATIONS[(i * 7 + 2) % len(EMAIL_SITUATIONS)]
        iid = f"t24-{VERSION}-free-email-{i:02d}"
        items.append((iid, {"brief": f"{sit}; {EMAIL_FORMAT}", "register": REGISTER, "facts": {"CUSTOMER": name},
                            "rules": ["exactly one document", "the name exactly once, verbatim", GREETING_RULE,
                                      PLACE[place]]}))
        meta[iid] = {"register": REGISTER, "customer": name, "held_out": False, "placement": place}
    return items, meta


# ------------------------------------------------------------------------------------------------ author stage
@dataclass
class R2Task:
    name: str
    kind: str
    field: str
    batch: chunker.TaskBatch
    pool: str
    meta: dict

    @property
    def chunk(self) -> dict:
        assert len(self.batch.chunks) == 1
        return self.batch.chunks[0]

    @property
    def task_id(self) -> str:
        return self.chunk["task_id"]

    @property
    def template_id(self) -> str:
        return template_id(REGISTER, self.batch.prompt_sha)

    def task_file(self, root: Path = ROOT) -> Path:
        return Path(root) / "tasks" / f"{self.task_id}.md"

    def answer_file(self, root: Path = ROOT) -> Path:
        return Path(root) / self.batch.answer_path(self.task_id)

    def text(self, root: Path = ROOT) -> str:
        c = self.chunk
        n = len(c["items"])
        qids = [it["qid"] for it in c["items"]]
        items = json.dumps(c["items"], ensure_ascii=False, indent=1)
        return (f"# T24 redo2 authoring task {self.task_id}\n\n"
                f"ANSWER FILE (write your whole answer here, and nowhere else, with the Write tool):\n"
                f"{self.answer_file(root)}\n\n"
                "This file is self-contained: the instructions, the answer contract and the items are all below. It "
                "is the only file you may open.\n\n"
                "ANSWER CONTRACT (exact; a program checks it):\n"
                f"- The answer file holds one JSON array with exactly {n} objects: one per item below, each item "
                "answered once, in any order.\n"
                '- Each object has exactly two keys: "qid" and "text". No other keys.\n'
                '- "qid": copy the item\'s qid exactly, character for character (the letter q followed by ten letters '
                f"or digits, 11 characters in all). The qids of this task: {', '.join(qids)}.\n"
                '- "text": one JSON string (the whole e-mail, its line breaks written as \\n).\n'
                "- Valid JSON only: no object around the array, no text before or after it, no markdown code fences, "
                'no comments. Inside JSON strings write a line break as \\n and a double quote as \\".\n'
                "Literal example of the shape (the qid shown is the first real one; replace the angle brackets with "
                f'your own text):\n[{{"qid": "{qids[0]}", "text": "<the e-mail>"}}, ...]\n\n'
                f"Task kind: {self.kind}; items: {n}; outputs expected: {n}.\n\n"
                f"{self.batch.prompt.rstrip()}\n\n"
                f"ITEMS (JSON; answer every item, keyed by its qid):\n{items}\n")


def template_id(register: str, prompt_sha: str) -> str:
    """G0 3.2 (v2.1): a G3-H template is one register under one authoring prompt."""
    return f"{register}|{prompt_sha[:16]}"


def build_tasks() -> list:
    items, meta = email_items()
    b = chunker.make_batch("author_freeform", FAMILY, items, seed=f"t24-author-{VERSION}-free-email",
                           prompt=EMAIL_PROMPT, forbid_strings=A.FORBID)
    if len(b.chunks) != 1:
        raise chunker.ChunkError("free-email-r2: one chunk")
    return [R2Task("free-email-r2", "author_freeform", "text", b, "freeform", meta)]


def _forbidden_hits(text: str) -> list:
    low = text.lower()
    return [f for f in A.FORBID if f and re.search(r"(?<![a-z0-9])" + re.escape(f.lower()) + r"(?![a-z0-9])", low)]


def check_author(tasks: list, root: Path = ROOT) -> list:
    """Problems: a forbidden string, an internal id or a never-open path in a task file; > 50 items; no answer path;
    an item field the chunker does not allow."""
    probs = []
    for t in tasks:
        text = t.text(root)
        probs += [f"{t.task_id}: task text holds forbidden string {f!r}" for f in _forbidden_hits(text)]
        if any(iid in text for iid in t.batch.key.values()):
            probs.append(f"{t.task_id}: internal id in task text")
        if not 1 <= len(t.chunk["items"]) <= chunker.MAX_ITEMS:
            probs.append(f"{t.task_id}: {len(t.chunk['items'])} items")
        if str(t.answer_file(root)) not in text:
            probs.append(f"{t.task_id}: answer path missing")
        for it in t.chunk["items"]:
            extra = set(it) - {"qid"} - set(chunker.TASK_KINDS[t.kind])
            if extra:
                probs.append(f"{t.task_id}: item fields {sorted(extra)}")
        for p in (t.task_file(root), t.answer_file(root)):
            if paths.never_open(p):
                probs.append(f"{t.task_id}: never-open path {p}")
    return probs


def author_files(tasks: list, root: Path = ROOT) -> tuple:
    """({relative path: text}, manifest) for paths.write_files."""
    out, rows = {}, []
    for t in tasks:
        out.update(t.batch.files())
        text = t.text(root)
        out[str(t.task_file(root).relative_to(root))] = text
        rows.append({"task": t.name, "task_id": t.task_id, "kind": t.kind, "pool": t.pool, "held_out": False,
                     "register": REGISTER, "blocker": BLOCKER, "need": NEED, "answer_field": t.field,
                     "template": t.template_id, "task_file": str(t.task_file(root)),
                     "answer_file": str(t.answer_file(root)), "batch_id": t.batch.batch_id,
                     "prompt_sha": t.batch.prompt_sha, "task_sha256": sha_text(text),
                     "n_items": len(t.chunk["items"]), "outputs_expected": len(t.chunk["items"]),
                     "placements": dict(Counter(m["placement"] for m in t.meta.values())),
                     "answer_contract": '[{"qid": "<qid>", "text": "<the e-mail>"}, ...] (a bare JSON array)',
                     "allowed_read": [str(t.task_file(root))], "allowed_write": [str(t.answer_file(root))],
                     "items": t.meta})
    manifest = {
        "family": FAMILY, "version": VERSION, "stage": "author (redo2: new Mode F e-mail template)",
        "g0_sha256": P.G0_SHA256_AUTHORED, "n_tasks": len(rows),
        "outputs_expected": sum(r["outputs_expected"] for r in rows),
        "notes": [
            "New items with new opaque ids and new answer paths; no v1 task, answer, key or pool is reused or changed.",
            "The task file is self-contained (answer path, inline answer contract, prompt, items). The agent reads only "
            "its task file and writes only its answer file (audit with allowed_read / allowed_write).",
            "key/ maps opaque qids to internal ids and TASKS.json 'items' holds the customer of each item (both "
            "orchestrator only). Ingest: families.T24.redo2 extract (lint + one G3-H read), then admit.",
            "Labels: none. Haiku writes text pieces only; G3-H only drops; every gold still comes from solver A = "
            "solver B.",
        ],
        "tasks": rows}
    out["TASKS.json"] = json.dumps(manifest, ensure_ascii=False, indent=1) + "\n"
    out["answers/README.txt"] = ("Haiku answer files: one <task_id>.json per redo2 authoring task (see ../TASKS.json), "
                                 "one bare JSON array each. Written only by the task agents.\n")
    return out, manifest


def check_on_disk(root: Path, files: dict) -> list:
    return [rel for rel, text in sorted(files.items())
            if not (Path(root) / rel).is_file() or (Path(root) / rel).read_text(encoding="utf-8") != text]


# ------------------------------------------------------------------------------------------------ extract stage
_INTRO_RE = r"(?i:\b(?:this is|my name is|i am|i'm|it's|it is))"


def email_role_problems(text: str, customer: str) -> list:
    """The new prompt's rules 7-10 (a drop-only check before the read): the greeting names nobody, and the name is
    alone on the last line below a sign-off line, or in a self-introduction in the first message line."""
    lines = text.split("\n")
    if len(lines) < 3:
        return ["e-mail: a greeting line, the message and a sign-off on separate lines (rule 8)"]
    probs = []
    if customer in lines[0]:
        probs.append("e-mail: the customer's name is in the greeting line, so it reads as the addressee (rule 9)")
    signed = len(lines) >= 4 and lines[-1].strip() == customer
    intro = bool(re.search(_INTRO_RE + r",?\s+" + re.escape(customer) + r"(?![A-Za-z])", lines[1])
                 or re.search(re.escape(customer) + r",?\s+here\b", lines[1]))
    if not (signed or intro):
        probs.append("e-mail: the name is neither alone on the last line below a sign-off nor in a self-introduction "
                     "in the first message line (rule 10)")
    return probs


def v1_freeform_texts() -> dict:
    """{normalised text: v1 piece id} over every v1 Mode F document (kept or dropped)."""
    pools, probs = A.load(A.ROOT)
    if probs:
        raise SystemExit(f"STOP: v1 authoring answers are incomplete: {probs[:5]}")
    return {X.norm(p["text"]): p["iid"] for p in pools.get("freeform", []) if isinstance(p.get("text"), str)}


def collect(t: R2Task) -> tuple:
    """([piece], shape drops). Stops when the answer file is missing, is not a bare JSON array or does not map to its
    items (the task is run again); an answer object with other keys or a non-string text is a shape drop."""
    p = t.answer_file()
    if not p.is_file():
        raise SystemExit(f"STOP: redo2 author answer missing: {p}")
    try:
        raw = json.loads(p.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, UnicodeDecodeError) as e:
        raise SystemExit(f"STOP: redo2 author answer is not JSON: {p}: {e}")
    if not isinstance(raw, list):
        raise SystemExit(f"STOP: redo2 author answer is a {type(raw).__name__}, the contract wants a bare JSON array: {p}")
    got, probs = chunker.load_answers(t.batch, {t.task_id: raw})
    if probs:
        raise SystemExit(f"STOP: redo2 author answers do not map to their items: {probs[:3]}")
    pieces, drops = [], []
    for iid in sorted(got):
        a, m = got[iid], t.meta[iid]
        base = {"iid": iid, "task_id": t.task_id, "prompt_sha": t.batch.prompt_sha, "template": t.template_id,
                "held_out": False, "register": m["register"], "customer": m["customer"], "placement": m["placement"]}
        if not isinstance(a, dict) or set(a) != {"text"} or not isinstance(a["text"], str):
            drops.append({**base, "stage": "shape", "reason": "answer object must be exactly {qid, text: string}"})
            continue
        pieces.append({**base, "text": a["text"]})
    return pieces, drops


def lint(pieces: list, v1_texts: dict) -> tuple:
    """(kept, drops): the v1 Mode F lint unchanged + the e-mail writer check, then dedup (redo2 and v1)."""
    kept, drops, seen = [], [], {}
    for p in pieces:
        probs = (A.check_freeform(p["text"], p["customer"]) + X.freeform_rule_problems(p["text"], p["customer"])
                 + email_role_problems(p["text"], p["customer"]))
        if probs:
            drops.append({**{k: v for k, v in p.items() if k != "text"}, "stage": "lint", "reason": "; ".join(probs),
                          "text": p["text"]})
            continue
        key = X.norm(p["text"])
        hit = v1_texts.get(key) or seen.get(key)
        if hit:
            drops.append({**{k: v for k, v in p.items() if k != "text"}, "stage": "dedup",
                          "reason": f"duplicate of {hit}", "text": p["text"]})
            continue
        seen[key] = p["iid"]
        kept.append(p)
    return kept, drops


def read_batch(pieces: list) -> chunker.TaskBatch:
    """One G3-H read of the kept e-mails: the plugin's field schema and the v1 read prompt, both unchanged."""
    fields = P.T24Plugin().extract_fields(None)
    items = [(p["iid"], g3h.extraction_item(p["text"], fields)) for p in pieces]
    return chunker.make_batch("extract_g3h", FAMILY, items, seed=f"t24-g3h-{VERSION}-email", prompt=X.G3H_PROMPT)


G3H_RULES = X.G3H_PROMPT.split("\n3. This task file")[0].rstrip()


def read_text(b: chunker.TaskBatch, c: dict, root: Path = EX_ROOT) -> str:
    tid, n = c["task_id"], len(c["items"])
    lines = ",\n".join(json.dumps(it, ensure_ascii=False) for it in c["items"])
    return (f"# T24 redo2 read task {tid}\n"
            f"Family T24, G3-H name extraction, {G3H_READ}, {n} items. Run by one fresh agent.\n\n"
            "READ THIS WHOLE FILE FIRST. This file is the only file you may open. Do not open, list or search any "
            "other file or\nfolder, and use no tool except one Write call.\n\n"
            "ANSWER FILE (write your whole answer here, and nowhere else, with the Write tool):\n"
            f"{Path(root) / b.answer_path(tid)}\n\n"
            "## 1. Instructions\n\n"
            f"{G3H_RULES}\n"
            "3. Answer every item exactly once, using the item's qid copied exactly. Judge each document only by what "
            "it says.\n\n"
            "## 2. Exact answer contract\n\n"
            "THE ANSWER FILE HOLDS ONE JSON ARRAY AND NOTHING ELSE: no object around it, no text before or after it, "
            "no code fence.\n"
            f"The array has exactly {n} objects, one per item in section 3, in any order. Every object has exactly "
            'these two keys,\nspelled exactly like this: "qid" and "customer".\n\n'
            "Literal example of the required shape (the values here are placeholders; yours are read from the "
            "documents):\n\n"
            '[\n{"qid": "q0123456789", "customer": "Firstname Lastname"},\n{"qid": "qabcdef0123", "customer": null}\n'
            "]\n\n"
            "Values:\n"
            f'- "qid": the item\'s qid, copied exactly. Each of the {n} qids appears exactly once.\n'
            '- "customer": the person\'s full name as a JSON string, copied character for character from that '
            "item's document, or the\n  JSON value null (written without quotes) when the document names no person "
            "who raised the case.\n\n"
            "These shapes are REJECTED and the whole task is run again:\n"
            '- an object around the array, e.g. {"task_id": "...", "answers": [ ... ]} (the file must START with [ '
            "and END with ]);\n"
            '- the name nested in another key, e.g. {"qid": "...", "fields": {"customer": "..."}}, or any key other '
            'than "qid" and\n  "customer";\n'
            '- the text "null" in quotes, an explanation, a note or a guess added to a value;\n'
            "- a missing qid, a repeated qid, a qid from another task.\n\n"
            f"Before you write: count that the array has {n} objects.\n\n"
            f"## 3. Items ({n}; one JSON object per line, inside one JSON array; copy each qid exactly)\n\n"
            f"```json\n[\n{lines}\n]\n```\n")


def extract_files(b: chunker.TaskBatch, kept: list, drops: list, counts: dict, root: Path = EX_ROOT) -> tuple:
    files = dict(b.files())
    rows = []
    for c in b.chunks:
        tid = c["task_id"]
        text = read_text(b, c, root)
        tf = Path(root) / "tasks" / f"{tid}.md"
        if paths.never_open(tf) or paths.never_open(Path(root) / b.answer_path(tid)):
            raise SystemExit(f"STOP: never-open path for {tid}")
        files[str(tf.relative_to(root))] = text
        rows.append({"task_id": tid, "kind": b.kind, "read": G3H_READ, "n_items": len(c["items"]),
                     "task_file": str(tf), "answer_file": str(Path(root) / b.answer_path(tid)),
                     "batch_id": b.batch_id, "seed": b.seed, "prompt_sha": b.prompt_sha,
                     "task_sha256": sha_text(text),
                     "answer_contract": '[{"qid": "<qid>", "customer": "<name as written>" or null}, ...]',
                     "allowed_read": [str(tf)], "allowed_write": [str(Path(root) / b.answer_path(tid))]})
    manifest = {"family": FAMILY, "version": VERSION, "stage": "extract (redo2: one G3-H read of the new e-mails)",
                "g0_sha256": P.G0_SHA256_AUTHORED, "counts": counts, "n_tasks": len(rows), "tasks": rows}
    files["TASKS.json"] = json.dumps(manifest, ensure_ascii=False, indent=1) + "\n"
    files["LINT_LOG.json"] = json.dumps({"dropped": drops}, ensure_ascii=False, indent=1) + "\n"
    files["pieces.json"] = json.dumps({"survivors": kept}, ensure_ascii=False, indent=1) + "\n"
    files["answers/README.txt"] = ("Read answer files: one <task_id>.json per task in TASKS.json, one bare JSON array "
                                   "each. Written only by the read agents; G3-H only drops documents.\n")
    return files, manifest


def stage_extract() -> dict:
    tasks = build_tasks()
    probs = check_author(tasks)
    if probs:
        raise SystemExit("STOP: redo2 author check failed: " + "; ".join(probs[:5]))
    files, _m = author_files(tasks)
    bad = check_on_disk(ROOT, files)
    if bad:
        raise SystemExit(f"STOP: redo2 author files on disk differ from the rebuild: {bad[:5]}")
    (t,) = tasks
    pieces, shape_drops = collect(t)
    kept, lint_drops = lint(pieces, v1_freeform_texts())
    if not kept:
        raise SystemExit("STOP: no redo2 e-mail survived the lint; nothing to read")
    b = read_batch(kept)
    drops = shape_drops + lint_drops
    counts = {"authored": len(pieces) + len(shape_drops), "shape_dropped": len(shape_drops),
              "lint_dropped": sum(1 for d in lint_drops if d["stage"] == "lint"),
              "dedup_dropped": sum(1 for d in lint_drops if d["stage"] == "dedup"), "kept_for_read": len(kept),
              "kept_by_placement": dict(Counter(p["placement"] for p in kept)),
              "lint_reasons": dict(Counter(r.split(":")[0] for d in lint_drops for r in d["reason"].split("; "))),
              "template": t.template_id}
    ex_files, manifest = extract_files(b, kept, drops, counts)
    return {"task": t, "kept": kept, "drops": drops, "batch": b, "files": ex_files, "manifest": manifest,
            "counts": counts}


# ------------------------------------------------------------------------------------------------ admit stage
def _jsonl(rows: list) -> str:
    return "".join(json.dumps(r, ensure_ascii=False) + "\n" for r in rows)


def _js(o) -> str:
    return json.dumps(o, ensure_ascii=False, indent=1) + "\n"


def load_read(b: chunker.TaskBatch) -> dict:
    raw = {}
    for c in b.chunks:
        p = EX_ROOT / b.answer_path(c["task_id"])
        if not p.is_file():
            raise SystemExit(f"STOP: redo2 read answer missing: {p}")
        try:
            a = json.loads(p.read_text(encoding="utf-8"))
        except (json.JSONDecodeError, UnicodeDecodeError) as e:
            raise SystemExit(f"STOP: redo2 read answer is not JSON: {p}: {e}")
        if not isinstance(a, list):
            raise SystemExit(f"STOP: redo2 read answer is a {type(a).__name__}, the contract wants a bare JSON array "
                             f"(run the task again): {p}")
        raw[c["task_id"]] = a
    got, probs = chunker.load_answers(b, raw)
    if probs:
        raise SystemExit(f"STOP: redo2 read answers do not map to their items (run the task again): {probs[:5]}")
    return got


def v1_pool_report() -> dict:
    """Report only: the v1 freeze (pool_freeze.py) as far as it exists on disk."""
    m = POOLS / "MANIFEST.json"
    if not m.is_file():
        return {"present": False}
    man = json.loads(m.read_text(encoding="utf-8"))
    c = man.get("counts", {})
    return {"present": True, "manifest_sha256": sha_file(m),
            "documents_frozen_by_register": c.get("documents_frozen_by_register"),
            "g3h_registers_quarantined": c.get("g3h_registers_quarantined")}


def stage_admit(write: bool) -> dict:
    """G3-H on the redo2 e-mails; (write=True) the pools/redo2/ supplement and its manifest."""
    paths.require_a38()
    st = stage_extract()
    bad = check_on_disk(EX_ROOT, st["files"])
    if bad:
        raise SystemExit(f"STOP: redo2 extraction files on disk differ from the rebuild: {bad[:5]}")
    b, t = st["batch"], st["task"]
    got = load_read(b)
    fields = P.T24Plugin().extract_fields(None)
    results, diffs_of = [], {}
    for p in st["kept"]:
        ans = got.get(p["iid"])
        ok, diffs = g3h.compare({"customer": p["customer"]}, ans if isinstance(ans, dict) else {}, fields)
        diffs_of[p["iid"]] = diffs
        results.append((p["template"], p["iid"], ok))
    rep = g3h.template_report(results)
    drop = set(rep["drop_rows"])
    quar = [{"stage": d["stage"], "iid": d["iid"], "task_id": d["task_id"], "reason": d["reason"][:240]}
            for d in st["drops"]]
    docs = []
    for p in st["kept"]:
        if p["iid"] in drop:
            why = list(diffs_of[p["iid"]])
            if p["template"] in rep["quarantined"]:
                d = rep["templates"][p["template"]]
                why.append(f"template {p['template']} below {int(g3h.PASS_RATE * 100)}% G3-H ({d['ok']}/{d['n']})")
            quar.append({"stage": "g3h", "iid": p["iid"], "task_id": p["task_id"], "reason": "; ".join(why)})
            continue
        docs.append({"doc_id": f"DOC-T24-{p['register'].upper()}-{sha_text(p['text'])[:8]}", "pool_id": p["iid"],
                     "register": p["register"], "held_out": False, "customer": p["customer"],
                     "task_id": p["task_id"], "g3h": "match", "template": p["template"],
                     "author_prompt_sha": p["prompt_sha"], "supplement": "redo2", "text_sha256": sha_text(p["text"]),
                     "text": p["text"]})
    dup = [k for k, v in Counter(d["doc_id"] for d in docs).items() if v > 1]
    if (POOLS / "documents.jsonl").is_file():
        v1_ids = {json.loads(x)["doc_id"] for x in (POOLS / "documents.jsonl").read_text(encoding="utf-8").splitlines()
                  if x.strip()}
        dup += sorted(v1_ids & {d["doc_id"] for d in docs})
    if dup:
        raise SystemExit(f"STOP: document ids collide: {dup[:3]}")
    summary = {"stage": "admit", "write": write, "extract_counts": st["counts"],
               "g3h_templates": rep["templates"], "g3h_quarantined": rep["quarantined"],
               "documents_kept": len(docs), "documents_kept_by_placement": dict(Counter(
                   p["placement"] for p in st["kept"] if p["iid"] not in drop)),
               "quarantine_rows": len(quar), "v1_pool": v1_pool_report()}
    if not write:
        return summary
    files = {"documents.jsonl": _jsonl(docs), "quarantine.jsonl": _jsonl(quar)}
    shas = {}
    for rel, text in sorted(files.items()):
        paths.write_text(SUPP / rel, text)
        shas[rel] = sha_text(text)
    manifest = {
        "family": FAMILY, "supplement": "redo2", "a38_present": paths.a38_frozen(),
        "g0_spec_sha256": sha_file(HERE / "G0_SPEC.md"),
        "matches_plugin_G0_SHA256": sha_file(HERE / "G0_SPEC.md") == P.T24Plugin.G0_SHA256,
        "summary": summary,
        "inputs": {"author_tasks": str(ROOT / "TASKS.json"), "extract_tasks": str(EX_ROOT / "TASKS.json"),
                   "author_answer_sha256": sha_file(t.answer_file()),
                   "read_answers_sha256": {c["task_id"]: sha_file(EX_ROOT / b.answer_path(c["task_id"]))
                                           for c in b.chunks}},
        "code": {f"families/T24/{n}": sha_file(HERE / n) for n in ("redo2.py", "authoring.py", "extract_stage.py",
                                                                    "plugin.py")},
        "pool_files": {rel: {"sha256": shas[rel]} for rel in sorted(shas)},
        "decisions": [
            "Supplement only: pools/ (pool_freeze.py, v1) is unchanged. Mode F rows draw from pools/documents.jsonl "
            "plus pools/redo2/documents.jsonl; the v1 e-mail template stays quarantined there.",
            "G3-H template = one register under one authoring prompt (G0 3.2, v2.1). The redo2 e-mail prompt is its own "
            "template and meets 98% on its own or is quarantined whole. Mismatches are always dropped.",
            "Unchanged: the G3-H field and its text, the read prompt (sha of extract_stage.G3H_PROMPT), "
            "g3h.PASS_RATE, the v1 Mode F lint. The e-mail writer check only drops (before the read).",
        ]}
    paths.write_text(SUPP / "MANIFEST.json", _js(manifest))
    return summary


# ------------------------------------------------------------------------------------------------ main
def main(argv: list) -> int:
    stage = argv[0] if argv and not argv[0].startswith("-") else "author"
    write = "--write" in argv
    if stage == "author":
        tasks = build_tasks()
        probs = check_author(tasks)
        if probs:
            print("\n".join(probs))
            return 1
        files, manifest = author_files(tasks)
        if write:
            answered = [t for t in tasks if t.answer_file().exists()]
            if answered and check_on_disk(ROOT, files):
                raise SystemExit("STOP: an answer exists and the task files would change; refusing to rewrite")
            paths.write_files(ROOT, files)
        for r in manifest["tasks"]:
            print(f"{r['kind']:16s} {r['task']:14s} items {r['n_items']:3d} outputs {r['outputs_expected']:3d} "
                  f"template {r['template']} placements {r['placements']}\n  task   {r['task_file']}\n"
                  f"  answer {r['answer_file']}")
        print(f"{manifest['n_tasks']} task(s), {manifest['outputs_expected']} outputs expected; written: {write}")
        return 0
    if stage == "extract":
        st = stage_extract()
        if write:
            paths.write_files(EX_ROOT, st["files"])
        print(json.dumps(st["counts"], indent=1, ensure_ascii=False))
        for r in st["manifest"]["tasks"]:
            print(f"{r['read']} items {r['n_items']:3d}\n  task   {r['task_file']}\n  answer {r['answer_file']}")
        print(f"written: {write}")
        return 0
    if stage == "admit":
        print(json.dumps(stage_admit(write), indent=1, ensure_ascii=False, default=str))
        return 0
    print(__doc__)
    return 2


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
