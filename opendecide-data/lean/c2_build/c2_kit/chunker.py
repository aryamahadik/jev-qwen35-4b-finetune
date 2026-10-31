"""c2_kit/chunker.py: Haiku task chunks, TEACH-0 pattern (PREREG A36; C2_DATA_SPEC 6.1, 6.5, 10.2).

Every Haiku task is a gold-free chunk of at most 50 items with opaque ids, plus one prompt. A Haiku agent reads only
its own chunk file and writes only its own answer file (audit.py checks its transcript). The key (opaque id ->
internal id) never leaves the orchestrator.

Task kinds and the only item fields each may carry (anything else, at any depth, refuses the batch):
  author_pack      brief                                  packs (tool namespaces, org contexts, everyday settings)
  author_skin      brief, register, slots, rules          Mode T skins: typed {SLOT}s, label-blind
  author_wording   brief, slots, rules                    question paraphrases (meaning admitted later by G-LEX)
  author_freeform  brief, register, facts, rules          Mode F text from a facts-only brief
  author_lexicon   brief, meaning, slots, rules           operator paraphrases (admitted by G-LEX extraction)
  extract_g3h      text, schema                           G3-H extraction (g3h.extraction_item)
  extract_lex      text, choices                          G-LEX blind meaning pick (lexicon.lexicon_items)
  blind_read       kind, text, question, options, definitions    G5-H dual blind solve; free-form single read
  polarity         question_a, question_b                 T37b polarity judgements
Never anywhere in an item: keys such as gold, answer, label, id, meta, spec, error_model (FORBIDDEN_KEYS); the
internal row ids; a path that is on the never-open list. Authoring kinds also refuse any `forbid_strings` the family
passes (its gold-label words and question texts; required for author_skin and author_freeform, and checked in the
prompt too): Haiku never sees the question, options or gold while writing.

  b = make_batch("blind_read", "T28", items, seed="g5h-a", prompt=PROMPT)    # items: [(internal id, item dict)]
  b.chunks, b.key, b.files()      # files(): {relative path: text}; written only by paths.write_files (after A38)
  answers = load_answers(b, {task_id: raw answer object})                     # -> ({internal id: answer}, problems)
"""
from __future__ import annotations

import hashlib
import hmac
import json
import re
from dataclasses import dataclass, field

from .paths import never_open

MAX_ITEMS = 50
TASK_KINDS = {
    "author_pack": ("brief",),
    "author_skin": ("brief", "register", "slots", "rules"),
    "author_wording": ("brief", "slots", "rules"),
    "author_freeform": ("brief", "register", "facts", "rules"),
    "author_lexicon": ("brief", "meaning", "slots", "rules"),
    "extract_g3h": ("text", "schema"),
    "extract_lex": ("text", "choices"),
    "blind_read": ("kind", "text", "question", "options", "definitions"),
    "polarity": ("question_a", "question_b"),
}
AUTHORING = ("author_pack", "author_skin", "author_wording", "author_freeform", "author_lexicon")
NEEDS_FORBID = ("author_skin", "author_freeform")      # label-blind writing: the family's label words + questions
FORBIDDEN_KEYS = {"gold", "answer", "answers", "label", "labels", "gold_label", "id", "row_id", "rid", "group_id",
                  "call_id", "meta", "spec", "structure", "solver", "solver_a", "solver_b", "error_model", "err",
                  "opt_err", "twin_of", "twin_kind", "difficulty", "difficulty_bin", "crowd_pg", "p_g", "key",
                  "correct", "truth", "expected"}
_PATHISH = re.compile(r"(?:~|\.{1,2})?(?:/[\w.@-]+){2,}")


class ChunkError(ValueError):
    pass


def sha(s: str) -> str:
    return hashlib.sha256(s.encode()).hexdigest()


@dataclass
class TaskBatch:
    kind: str
    family: str
    batch_id: str
    prompt: str
    prompt_sha: str
    seed: str
    chunks: list = field(default_factory=list)      # [{"task_id", "kind", "prompt_sha", "items"}]
    key: dict = field(default_factory=dict)         # qid -> internal id (orchestrator only)
    task_of: dict = field(default_factory=dict)     # qid -> task id

    def chunk_path(self, task_id: str) -> str:
        return f"chunks/{task_id}.json"

    def answer_path(self, task_id: str) -> str:
        return f"answers/{task_id}.json"

    def prompt_path(self) -> str:
        return f"prompts/{self.prompt_sha[:16]}.txt"

    def files(self) -> dict:
        """{relative path: text}: prompt, chunks, manifest and the key (the key in key/, never sent to Haiku)."""
        out = {self.prompt_path(): self.prompt}
        for c in self.chunks:
            out[self.chunk_path(c["task_id"])] = json.dumps(c, ensure_ascii=False, indent=1) + "\n"
        out[f"key/{self.batch_id}.json"] = json.dumps({"batch_id": self.batch_id, "key": self.key}, indent=1) + "\n"
        out[f"manifest/{self.batch_id}.json"] = json.dumps(self.manifest(), indent=1) + "\n"
        return out

    def manifest(self) -> dict:
        return {"batch_id": self.batch_id, "kind": self.kind, "family": self.family, "seed": self.seed,
                "prompt_sha": self.prompt_sha, "n_items": len(self.key),
                "tasks": [{"task_id": c["task_id"], "n": len(c["items"]),
                           "sha256": sha(json.dumps(c, sort_keys=True, ensure_ascii=False))} for c in self.chunks]}

    def allowed(self, root: str, task_id: str) -> tuple:
        """(paths the agent may read, paths it may write) for audit.audit()."""
        r = str(root).rstrip("/")
        return ({f"{r}/{self.chunk_path(task_id)}", f"{r}/{self.prompt_path()}"}, {f"{r}/{self.answer_path(task_id)}"})


def _walk_keys(o, where="item"):
    if isinstance(o, dict):
        for k, v in o.items():
            if str(k).lower() in FORBIDDEN_KEYS:
                raise ChunkError(f"{where}: forbidden key {k!r}")
            _walk_keys(v, f"{where}.{k}")
    elif isinstance(o, list):
        for i, v in enumerate(o):
            _walk_keys(v, f"{where}[{i}]")


def _strings(o):
    if isinstance(o, str):
        yield o
    elif isinstance(o, dict):
        for k, v in o.items():
            yield str(k)
            yield from _strings(v)
    elif isinstance(o, list):
        for v in o:
            yield from _strings(v)


def check_item(kind: str, item: dict, *, forbid_strings: tuple = ()) -> None:
    if kind not in TASK_KINDS:
        raise ChunkError(f"task kind {kind!r}")
    if not isinstance(item, dict) or not item:
        raise ChunkError("an item is a non-empty object")
    extra = set(item) - set(TASK_KINDS[kind])
    if extra:
        raise ChunkError(f"{kind}: fields {sorted(extra)} not allowed (allowed: {TASK_KINDS[kind]})")
    _walk_keys(item)
    if kind == "blind_read":
        if item.get("kind") not in ("yes/no", "choice"):
            raise ChunkError("blind_read kind is 'yes/no' or 'choice'")
        if item["kind"] == "choice" and not (isinstance(item.get("options"), list) and len(item["options"]) >= 2):
            raise ChunkError("a choice item lists its options")
        if item["kind"] == "yes/no" and "options" in item:
            raise ChunkError("a yes/no item has no options")
    for s in _strings(item):
        for m in _PATHISH.finditer(s):
            if never_open(m.group()):
                raise ChunkError(f"item text names a never-open path ({m.group()[:40]})")
        if kind in AUTHORING:
            low = s.lower()
            for f in forbid_strings:
                if f and re.search(r"(?<![a-z0-9])" + re.escape(f.lower()) + r"(?![a-z0-9])", low):
                    raise ChunkError(f"authoring item mentions a forbidden string ({f!r}): question / label leak")


def make_batch(kind: str, family: str, items: list, *, seed: str, prompt: str, max_items: int = MAX_ITEMS,
               forbid_strings: tuple = ()) -> TaskBatch:
    """items: [(internal id, item dict)]. Shuffled by seed, opaque qids, chunks of <= max_items (<= 50)."""
    if not 1 <= max_items <= MAX_ITEMS:
        raise ChunkError(f"chunks hold 1-{MAX_ITEMS} items")
    if not prompt.strip():
        raise ChunkError("a batch has a prompt")
    if kind in NEEDS_FORBID and not any(f and f.strip() for f in forbid_strings):
        raise ChunkError(f"{kind} batches pass forbid_strings (the family's label words and question texts)")
    low_prompt = prompt.lower()
    for f in forbid_strings if kind in AUTHORING else ():
        if f and re.search(r"(?<![a-z0-9])" + re.escape(f.lower()) + r"(?![a-z0-9])", low_prompt):
            raise ChunkError(f"the authoring prompt mentions a forbidden string ({f!r})")
    ids = [i for i, _ in items]
    if len(set(ids)) != len(ids):
        raise ChunkError("duplicate internal ids")
    for _, it in items:
        check_item(kind, it, forbid_strings=forbid_strings)
    psha = sha(prompt)
    if any(i and i in prompt for i in ids):
        raise ChunkError("the prompt names an internal id")
    secret = sha(f"{family}|{kind}|{seed}|{psha}").encode()
    order = sorted(items, key=lambda x: sha(f"{seed}|order|{x[0]}"))
    batch_id = f"{family}-{kind}-{sha(seed + psha + '|'.join(sorted(ids)))[:8]}"
    b = TaskBatch(kind, family, batch_id, prompt, psha, seed)
    for c in range(0, len(order), max_items):
        tid = f"{batch_id}-{c // max_items:03d}"
        its = []
        for iid, it in order[c:c + max_items]:
            qid = "q" + hmac.new(secret, iid.encode(), hashlib.sha256).hexdigest()[:10]
            if qid in b.key:
                raise ChunkError("opaque id collision")
            b.key[qid] = iid
            b.task_of[qid] = tid
            its.append({"qid": qid, **it})
        chunk = {"task_id": tid, "kind": kind, "prompt_sha": psha, "items": its}
        blob = json.dumps(chunk, ensure_ascii=False)
        leaked = [i for i in ids if i and i in blob]
        if leaked:
            raise ChunkError(f"chunk text contains internal id(s) {leaked[:2]}")
        b.chunks.append(chunk)
    return b


def load_answers(batch: TaskBatch, raw: dict) -> tuple:
    """raw: {task_id: [{"qid", ...}, ...] or {qid: answer}}. Returns ({internal id: answer object}, problems).
    An answer for a qid outside its own chunk, a duplicate or an unknown qid is a problem (and is not used)."""
    out, probs = {}, []
    for tid, ans in raw.items():
        if isinstance(ans, list):
            pairs = []
            for a in ans:
                if not isinstance(a, dict) or "qid" not in a:
                    probs.append(f"{tid}: an answer without qid")
                    continue
                pairs.append((a["qid"], {k: v for k, v in a.items() if k != "qid"}))
        elif isinstance(ans, dict):
            pairs = list(ans.items())
        else:
            probs.append(f"{tid}: answers are a list or an object")
            continue
        for qid, a in pairs:
            if qid not in batch.key:
                probs.append(f"{tid}: unknown qid {qid}")
            elif batch.task_of[qid] != tid:
                probs.append(f"{tid}: qid {qid} belongs to {batch.task_of[qid]}")
            elif batch.key[qid] in out:
                probs.append(f"{tid}: qid {qid} answered twice")
            else:
                out[batch.key[qid]] = a
    missing = sorted(set(batch.key.values()) - set(out))
    if missing:
        probs.append(f"{len(missing)} item(s) unanswered")
    return out, probs


def item_by_internal(batch: TaskBatch) -> dict:
    """{internal id: the item as Haiku saw it} (orchestrator side; used to map letters back to options)."""
    inv = {}
    for c in batch.chunks:
        for it in c["items"]:
            inv[batch.key[it["qid"]]] = it
    return inv
