"""LongBench v2 in longjev's protocol, with an OpenDecide model as the chunk scorer and the final reader (shared code).

Mirrors github.com/avshalomd/longjev at commit 9d317786820c69f8346687e94453bf3e801e8de5 (MIT licence, (c) Avshalom
Dayan). The pieces marked VERBATIM below are copies of longjev's own functions (chunker.py, questions.py, assembler.py,
api.py, eval/longbench.py, eval/report.py); tests/test_lb.py imports the quarantined longjev checkout and checks every
one of them against the original on synthetic inputs.

Protocol (the headline "jev selector, keep 8K tokens" arm of longjev's LongBench v2 eval):
  data      LongBench v2 data.json (503 four-option questions), split by sha256(_id): first 100 = dev, rest = test
  items     contexts with ceil(chars / 3.0) <= CAP_TOKENS ("chosen"); only items that do NOT fit Jev's window whole
            (context tokens + 600 > 28,000) are compressed and counted ("long" items)
  chunks    800 estimated tokens (= 2,400 characters at 3.0 chars/token), cut at the coarsest of "\\n\\n", "\\n", ". ", " ",
            packed greedily, no overlap; joining the chunks gives the context back exactly
  scoring   one yes/no per chunk: "This passage contains information that helps answer the following question:
            <question> Options: A: ...; B: ...; C: ...; D: ..."; the chunk's score is P(yes)
  sizes     chunk sizes in tokens as the SCORER counts them (longjev: Jev's reported usage; here: our tokenizer)
  keep      budget = max(1000, min(8000, int(32000 * 0.9) - longest final question)); chunks are taken best-first,
            each costing its tokens + 15, until the next best does not fit; then put back in document order and every
            gap becomes "\\n[… about N tokens omitted …]\\n"
  answer    the four-option question over the kept text; correct if the chosen letter equals the gold letter

BLIND: nothing in this module prints item text, questions, options or gold labels.
"""
from __future__ import annotations

import hashlib
import json
import math
from dataclasses import dataclass, replace
from pathlib import Path
from typing import Any, Mapping

import numpy as np

HERE = Path(__file__).resolve().parent
BENCH = HERE.parent
REPO = BENCH.parent
QUARANTINE = BENCH / "external_quarantine" / "longbench_v2"

LONGJEV_REPO = "https://github.com/avshalomd/longjev"
LONGJEV_COMMIT = "9d317786820c69f8346687e94453bf3e801e8de5"
DATA_REPO = "zai-org/LongBench-v2"  # THUDM/LongBench-v2 redirects here
DATA_REVISION = "2b48e494f2c7a2f0af81aae178e05c7e1dde0fe9"  # HEAD since 2024-12-20; data.json unchanged since ac35867b
DATA_SHA256 = "15d61c22d92c96900b3c4948b6aeea218d3214b676a65df48e7b8555604c7fe2"
DATA_N = 503

# ---- longjev constants (file: constant)
DEV_SIZE = 100                 # eval/longbench.py
LETTERS = ("A", "B", "C", "D")  # eval/longbench.py
CHARS_PER_TOKEN = 3.0          # eval/run.py CHARS_PER_TOKEN (TokenEstimator for chunking and the item filter)
CHUNK_TOKENS = 800             # LongJev(chunk_tokens=800), the default; eval/run.py does not change it
BUDGET = 8_000                 # the "jev @ 8000" result (BUDGETS[0], frozen on dev by the tie-break to the smaller)
MAX_BUDGET = 28_000            # LongJev(max_budget_tokens=28_000); fits = context_tokens + 600 <= this
FIT_MARGIN = 600               # eval/run.py: fits = record["context_tokens"] + 600 <= lj.max_budget_tokens
SINGLE_LIMIT_TOKENS = 32_000   # api.py
MARGIN = 0.9                   # api.py
GAP_TOKENS = 15                # assembler.py
REL, SUFF = "rel__", "suff__"  # questions.py

# ---- reconstructed, NOT published (see PREREG_longbench_v2.md section 2): the item set behind longjev's 163/42/93
CAP_TOKENS = 170_000   # --max-context-tokens; the eval/run.py default 120,000 gives only 239 chosen items, not 298-301
JEV_PROXY_CPT = 3.8    # chars per Jev token for the "fits" test; with CAP_TOKENS this gives exactly 42 dev / 163 test
EXPECT_PROXY = {"chosen": 301, "long_dev": 42, "long_test": 163, "fit": 96}  # published: 42 / 163 long, 93 fit

REL_TEMPLATE = "This passage contains information that helps answer the following question: {}"
SUFF_CHUNK_TEMPLATE = "The following question can be answered from this passage alone: {}"
SUFF_FINAL_TEMPLATE = "The text contains enough information to answer: {}"


# ===================================================================== token estimate (VERBATIM tokens.py, fixed ratio)

def estimate(value: Any, chars_per_token: float = CHARS_PER_TOKEN) -> int:
    text = value if isinstance(value, str) else json.dumps(value, ensure_ascii=False)
    return math.ceil(len(text) / chars_per_token)


def chars_for(tokens: int, chars_per_token: float = CHARS_PER_TOKEN) -> int:
    return int(tokens * chars_per_token)


# ===================================================================== chunker (VERBATIM chunker.py, str states)

SEPARATORS = ("\n\n", "\n", ". ", " ")


@dataclass(frozen=True)
class Chunk:
    id: int
    label: str
    start: int
    end: int
    text: str
    est_tokens: int


def _pieces(text: str, limit: int, seps: tuple = SEPARATORS) -> list:
    if len(text) <= limit:
        return [text]
    for i, sep in enumerate(seps):
        if sep in text:
            parts = text.split(sep)
            parts = [p + sep for p in parts[:-1]] + [parts[-1]]
            out: list = []
            for part in parts:
                if part:
                    out.extend(_pieces(part, limit, seps[i + 1:]))
            return out
    return [text[i: i + limit] for i in range(0, len(text), limit)]


def _pack(pieces: list, limit: int) -> list:
    out: list = []
    current: list = []
    size = 0
    for piece in pieces:
        if current and size + len(piece) > limit:
            out.append("".join(current))
            current, size = [], 0
        current.append(piece)
        size += len(piece)
    if current:
        out.append("".join(current))
    return out


def _chunk_text(text: str, path: str, limit: int) -> list:
    out = []
    offset = 0
    for i, body in enumerate(_pack(_pieces(text, limit), limit)):
        out.append((f"{path}#c{i}", offset, offset + len(body), body))
        offset += len(body)
    return out


def chunk_state(state: str, chunk_tokens: int = CHUNK_TOKENS) -> list:
    """chunker.chunk_state for a str state (LongBench contexts are strings)."""
    if not isinstance(state, str):
        raise TypeError("LongBench contexts are strings")
    limit = max(1, chars_for(chunk_tokens))
    raw = [r for r in _chunk_text(state, "$", limit) if r[3]]
    return [Chunk(i, label, start, end, text, estimate(text)) for i, (label, start, end, text) in enumerate(raw)]


# ===================================================================== questions (VERBATIM questions.py / longbench.py)

def choice_json(item: Mapping) -> dict:
    """eval/longbench.question(item)["q"].to_json(): Choice(question.strip(), {L: choice_L.strip()})."""
    return {"type": "choice", "instructions": item["question"].strip(),
            "criteria": {L: item[f"choice_{L}"].strip() for L in LETTERS}}


def render(q: Mapping) -> str:
    instructions = q["instructions"]
    text = instructions if isinstance(instructions, str) else str(instructions)
    criteria = q.get("criteria")
    if q["type"] == "choice" and criteria:
        options = "; ".join(f"{k}: {v}" if v else str(k) for k, v in criteria.items())
        return f"{text} Options: {options}"
    if q["type"] == "score" and criteria:
        return f"{text} Levels: {'; '.join(criteria)}"
    return text


def rel_instruction(item: Mapping) -> str:
    return REL_TEMPLATE.format(render(choice_json(item)))


def final_questions(item: Mapping) -> dict:
    """questions.final_questions({"q": Choice(...)}): the task question plus the sufficiency yes/no."""
    q = choice_json(item)
    return {"q": q, SUFF + "q": {"type": "noul", "instructions": SUFF_FINAL_TEMPLATE.format(render(q))}}


def effective_budget(item: Mapping, budget_tokens: int = BUDGET) -> int:
    """api.LongJev.effective_budget (estimates at 3.0 chars/token, as LongJev's TokenEstimator in eval/run.py)."""
    longest = max(estimate(q) for q in final_questions(item).values())
    return max(1_000, min(budget_tokens, int(SINGLE_LIMIT_TOKENS * MARGIN) - longest))


# ===================================================================== selection and rendering (VERBATIM assembler.py)

def select_round_robin(chunks: list, rel: Mapping[str, np.ndarray], budget_tokens: int) -> list:
    orders = {k: list(np.argsort(-scores, kind="stable")) for k, scores in rel.items()}
    position = {k: 0 for k in orders}
    chosen: list = []
    taken: set = set()
    used = 0
    active = list(orders)
    while active:
        for key in list(active):
            order = orders[key]
            while position[key] < len(order) and int(order[position[key]]) in taken:
                position[key] += 1
            if position[key] >= len(order):
                active.remove(key)
                continue
            cid = int(order[position[key]])
            cost = chunks[cid].est_tokens + GAP_TOKENS
            if used + cost > budget_tokens:
                active.remove(key)
                continue
            chosen.append(cid)
            taken.add(cid)
            used += cost
    if not chosen and orders:
        first = next(iter(orders.values()))
        if len(first):
            chosen.append(int(first[0]))
    return chosen


def _path(label: str) -> str:
    return label.split("#c")[0]


def render_state(chunks: list, kept: list) -> str:
    ids = sorted(set(kept))
    parts: list = []
    previous = -1
    for cid in ids:
        if cid != previous + 1:
            omitted = sum(c.est_tokens for c in chunks[previous + 1: cid])
            parts.append(f"\n[… about {omitted} tokens omitted …]\n")
        elif parts and _path(chunks[cid].label) != _path(chunks[previous].label):
            parts.append("\n")
        parts.append(chunks[cid].text)
        previous = cid
    if ids and ids[-1] != len(chunks) - 1:
        omitted = sum(c.est_tokens for c in chunks[ids[-1] + 1:])
        parts.append(f"\n[… about {omitted} tokens omitted …]\n")
    return "".join(parts)


def recalibrate(chunks: list, scorer_tokens: list) -> list:
    """api.LongJev.recalibrate's role: chunk sizes in tokens as the scorer counted them (longjev: Jev's usage per
    chunk; here: our tokenizer's count of the chunk text, so every chunk is measured and no ratio fallback is needed)."""
    if len(scorer_tokens) != len(chunks):
        raise ValueError("one token count per chunk")
    return [replace(c, est_tokens=max(1, int(n))) for c, n in zip(chunks, scorer_tokens)]


# ===================================================================== split and item sets

def dev_ids(items: list) -> set:
    """eval/longbench.load: items sorted by sha256(_id); the first DEV_SIZE are dev."""
    order = sorted(items, key=lambda x: hashlib.sha256(x["_id"].encode()).hexdigest())
    return {x["_id"] for x in order[:DEV_SIZE]}


def item_flags(item: Mapping, dev: set, own_context_tokens: int | None = None) -> dict:
    """Set membership for one item (no text). proxy = the pre-registered reconstruction of longjev's item set
    (CAP_TOKENS, JEV_PROXY_CPT); own = the same rule with our tokenizer's count for 'fits' (secondary)."""
    n = len(item["context"])
    chosen = estimate(item["context"]) <= CAP_TOKENS
    proxy_tokens = math.ceil(n / JEV_PROXY_CPT)
    f = {"split": "dev" if item["_id"] in dev else "test", "n_chars": n, "est3": estimate(item["context"]),
         "chosen": chosen, "proxy_tokens": proxy_tokens,
         "long_proxy": chosen and proxy_tokens + FIT_MARGIN > MAX_BUDGET,
         "fit_proxy": chosen and proxy_tokens + FIT_MARGIN <= MAX_BUDGET}
    if own_context_tokens is not None or not chosen:
        f["own_tokens"] = None if own_context_tokens is None else int(own_context_tokens)
        f["long_own"] = chosen and own_context_tokens + FIT_MARGIN > MAX_BUDGET
        f["fit_own"] = chosen and own_context_tokens + FIT_MARGIN <= MAX_BUDGET
    return f


SETS = {  # name -> (flag, split or None); the primary comparison set is "test_proxy"
    "test_proxy": ("long_proxy", "test"), "dev_proxy": ("long_proxy", "dev"), "all_proxy": ("long_proxy", None),
    "test_own": ("long_own", "test"), "dev_own": ("long_own", "dev"), "all_own": ("long_own", None),
    "control_proxy": ("fit_proxy", None), "control_test_proxy": ("fit_proxy", "test"),
}


def in_set(meta: Mapping, name: str) -> bool:
    flag, split = SETS[name]
    return bool(meta.get(flag)) and (split is None or meta["split"] == split)


# ===================================================================== our row format

def item_id(item: Mapping) -> str:
    """LongBench's "_id" (data.json) or the kit's "id" (lb_items.jsonl)."""
    return item["_id"] if "_id" in item else item["id"]


def final_row(item: Mapping, state: str) -> dict:
    """decoder_io row: the selected text as state, the question, the four options in A-D order (letters A-D)."""
    return {"id": item_id(item), "qtype": "choice", "state": state, "instructions": item["question"].strip(),
            "options": [item[f"choice_{L}"].strip() for L in LETTERS]}


def rel_row(item: Mapping, chunk: Chunk) -> dict:
    """decoder_io yes/no row for longjev's relevance question on one chunk (the chunk text is the state)."""
    return {"id": f"{item_id(item)}#c{chunk.id}", "qtype": "noul", "state": chunk.text,
            "instructions": rel_instruction(item), "options": None}


# ===================================================================== readout (decoder_io; index-keyed for choice rows)

def read_rows(dio, model, ro, rows: list, dev, choice_readout: str, batch_size: int = 16, token_budget: int = 12000,
              batches_fn=None) -> list:
    """A5 readout with probabilities keyed by option INDEX (decoder_io.to_probs keys by option text, which merges
    duplicate option texts; one LongBench item has two identical options). Numbers are those of
    ohs3_lib.a5_read / decoder_io.predict(tta_choice=...): same batches (decoder_io.predict's order and token budget),
    same cand_logits calls, softmax(logits / 1.0), 2-view = (identity + exact reversal) / 2 in probability space.
    Returns per row: yes/no -> {"p_yes"}; choice -> {"p1": identity view, "p": readout} (lists in A-D order)."""
    import torch
    if choice_readout not in ("2view", "single"):
        raise ValueError(choice_readout)
    if batches_fn is None:
        batches_fn = predict_batches
    out = [None] * len(rows)
    with torch.no_grad():
        for idx in batches_fn(rows, batch_size, token_budget):
            batch = [rows[i] for i in idx]
            lg = dio.cand_logits(model, ro, batch, dev)
            for j, i in enumerate(idx):
                r = rows[i]
                if r["qtype"] == "noul":
                    out[i] = {"p_yes": float(dio.to_probs(r, lg[j])["yes"])}
                else:
                    p1 = torch.softmax(lg[j] / 1.0, dim=-1).tolist()
                    out[i] = {"p1": p1, "p": p1}
            ch = [i for i in idx if rows[i]["qtype"] == "choice" and choice_readout == "2view"]
            if ch:
                rev = [list(range(len(rows[i]["options"])))[::-1] for i in ch]
                lg2 = dio.cand_logits(model, ro, [rows[i] for i in ch], dev, perms=rev)
                for i, p, l2 in zip(ch, rev, lg2):
                    shown = torch.softmax(l2 / 1.0, dim=-1).tolist()
                    p2 = [0.0] * len(p)
                    for k, o in enumerate(p):
                        p2[o] = shown[k]
                    p1 = out[i]["p1"]
                    out[i] = {"p1": p1, "p": [(a + b) / 2 for a, b in zip(p1, p2)]}
    return out


def predict_batches(rows, batch_size=16, token_budget=12000):
    """decoder_io.predict's order and token-budget batching, verbatim (= ohs3_lib.predict_batches)."""
    order = sorted(range(len(rows)), key=lambda i: len(rows[i]["state"]) + 20 * len(rows[i]["options"] or []))
    est = lambda i: (len(rows[i]["state"]) + len(rows[i].get("card") or "") + 400) / 3.2  # noqa: E731
    batches, cur = [], []
    for i in order:
        if cur and (len(cur) >= batch_size or (len(cur) + 1) * est(i) > token_budget):
            batches.append(cur)
            cur = []
        cur.append(i)
    if cur:
        batches.append(cur)
    return batches


def argmax_letter(p: list) -> str:
    """First maximum in A-D order (a tie goes to the earlier letter)."""
    best = max(range(len(p)), key=lambda k: (p[k], -k))
    return LETTERS[best]


# ===================================================================== statistics (wilson VERBATIM eval/report.py)

def wilson(k: int, n: int, z: float = 1.96) -> tuple:
    if n == 0:
        return (0.0, 0.0)
    p = k / n
    centre = (p + z * z / (2 * n)) / (1 + z * z / n)
    half = z * math.sqrt(p * (1 - p) / n + z * z / (4 * n * n)) / (1 + z * z / n)
    return (max(0.0, centre - half), min(1.0, centre + half))


def newcombe_diff(k1: int, n1: int, k2: int, n2: int, z: float = 1.96) -> tuple:
    """Newcombe (1998) method 10: CI for p1 - p2 of two INDEPENDENT proportions from their Wilson intervals."""
    p1, p2 = k1 / n1, k2 / n2
    l1, u1 = wilson(k1, n1, z)
    l2, u2 = wilson(k2, n2, z)
    d = p1 - p2
    lo = d - math.sqrt((p1 - l1) ** 2 + (u2 - p2) ** 2)
    hi = d + math.sqrt((u1 - p1) ** 2 + (p2 - l2) ** 2)
    return d, lo, hi


def mcnemar(b: int, c: int) -> float:
    """VERBATIM eval/report.py: exact two-sided p from the discordant pairs."""
    n = b + c
    if n == 0:
        return 1.0
    tail = sum(math.comb(n, i) for i in range(0, min(b, c) + 1)) / 2 ** n
    return min(1.0, 2 * tail)


def sha256_file(p) -> str:
    h = hashlib.sha256()
    with open(p, "rb") as f:
        for blk in iter(lambda: f.read(1 << 20), b""):
            h.update(blk)
    return h.hexdigest()


def sha256_text(s: str) -> str:
    return hashlib.sha256(s.encode("utf-8")).hexdigest()


def read_jsonl(p) -> list:
    with open(p, encoding="utf-8") as f:
        return [json.loads(l) for l in f if l.strip()]
