"""fastcore.readout: API v1 requests -> decoder_io rows -> per-(question, view) work items -> API v1 answers (SPEED-1).

C1's A5 readout, rebuilt around PRE-TOKENIZED work items so that prompt building and tokenization can run outside the
GPU worker (hosting/SPEED1_DESIGN.md, "Shared HTTP API" and "Answers must stay C1's"):
  - parse_v1(req) -> [(name, row)]: row = {"state", "instructions", "qtype", "options", "card"}, the fields
    decoder_io's prompt reads (cygnet_msg / as_letter_row read state, instructions, qtype, options and card; prompt_texts
    also reads "_prompt", which a request can never set). Errors raise RequestError (a ValueError: HTTP 400).
  - build_items(ro, named) -> [WorkItem]: one item per (question, view). View 0 = the given order (perm None, exactly as
    decoder_io.predict reads it); view 1 = the exact reversal list(range(n))[::-1], for choice questions only. The text
    is decoder_io.prompt_texts(ro, [row], [perm])[0] = ro.prompt(row, perm) byte for byte; candidate id groups are
    ro.cand(row) (the full Readout, so two-letter labels after Z are the ones decoder_io uses).
  - tokenize_items(tok, items): tok(texts, add_special_tokens=False) capped like decoder_io's eager path
    (truncation=True, max_length=decoder_io.MAX_LEN, on the tokenizer's truncation side).
  - combine(named, items, logits) -> (answers, usage): per-view fp32 candidate logits -> probabilities with
    decoder_io.to_probs, then the prob-space average of the two views per option, exactly as
    decoder_io.predict(tta_choice=True) does (decoder_io.py:688-695); noul = the single read; T = 1.0 / 1.0.

No GPU, no network, no Modal: everything here is pure CPU and is unit-tested in hosting/tests/test_fastcore_readout.py.
decoder_io is imported read-only from lean/ (or /root/lean in a container); nothing pinned is edited.
"""
from __future__ import annotations

import sys
from dataclasses import dataclass, field
from pathlib import Path

API_VERSION = "v1"
MAX_QUESTIONS = 16
MIN_OPTIONS = 2
MAX_OPTIONS = 255  # decoder_io.MAX_OPTIONS; the served limit is min(255, len(decoder_io.WIDE)) once a Readout is built
TEMPS = {"noul": 1.0, "choice": 1.0}  # prep89/t_fit_q35_4b_main500k.json "ship": T_noul = T_choice = 1.0
REQUEST_KEYS = {"id", "state", "questions", "return_views"}
QUESTION_KEYS = {"type", "instructions", "options", "card"}
REMOTE_LEAN = "/root/lean"


def lean_import():
    """decoder_io from /root/lean in a container, else from lean/ (two levels above this package). Read-only."""
    here = Path(__file__).resolve().parents[2]
    p = REMOTE_LEAN if Path(REMOTE_LEAN, "decoder_io.py").exists() else str(here)
    if p not in sys.path:
        sys.path.insert(0, p)
    import decoder_io
    return decoder_io


dio = lean_import()


class RequestError(ValueError):
    """A malformed API v1 request (the host answers HTTP 400 with str(error))."""
    status = 400


def max_options() -> int:
    """Options a choice may have in THIS process: 255, or fewer if no full decoder_io.Readout has been built yet (the
    two-letter labels after Z come from Readout's vocabulary scan, which fills decoder_io.WIDE)."""
    return min(MAX_OPTIONS, len(dio.WIDE))


def parse_v1(req, max_opts: int | None = None) -> list:
    """An API v1 request -> [(question name, decoder_io row)] in request order. Raises RequestError.
    {"id"?: str, "state": str, "return_views"?: bool,
     "questions": {name: {"type": "noul"|"choice", "instructions": str, "options"?: [str], "card"?: str}}}"""
    mo = max_options() if max_opts is None else max_opts
    if not isinstance(req, dict):
        raise RequestError("the request must be a JSON object")
    extra = set(req) - REQUEST_KEYS
    if extra:
        raise RequestError(f"unknown request field(s): {sorted(extra)} (API v1 takes {sorted(REQUEST_KEYS)})")
    if "id" in req and req["id"] is not None and not isinstance(req["id"], str):
        raise RequestError('"id" must be a string')
    if not isinstance(req.get("state"), str):
        raise RequestError('"state" must be a string')
    if "return_views" in req and not isinstance(req["return_views"], bool):
        raise RequestError('"return_views" must be true or false')
    qs = req.get("questions")
    if not isinstance(qs, dict) or not qs:
        raise RequestError('"questions" must be a non-empty object')
    if len(qs) > MAX_QUESTIONS:
        raise RequestError(f"at most {MAX_QUESTIONS} questions per request (got {len(qs)})")
    out = []
    for name, q in qs.items():
        if not isinstance(q, dict):
            raise RequestError(f"{name}: a question must be an object")
        extra = set(q) - QUESTION_KEYS
        if extra:
            hint = ' (send "options" and the definitions "card"; "criteria" is not API v1)' if "criteria" in extra else ""
            raise RequestError(f"{name}: unknown field(s) {sorted(extra)}{hint}")
        qtype = q.get("type")
        if qtype not in ("noul", "choice"):
            raise RequestError(f'{name}: "type" must be "noul" or "choice"')
        ins = q.get("instructions")
        if not isinstance(ins, str) or not ins.strip():
            raise RequestError(f'{name}: "instructions" must be a non-empty string')
        card = q.get("card")
        if card is not None and not isinstance(card, str):
            raise RequestError(f'{name}: "card" must be a string')
        opts = q.get("options")
        if qtype == "noul":
            if opts is not None:
                raise RequestError(f'{name}: a noul question takes no "options"')
        else:
            if not isinstance(opts, list) or not all(isinstance(o, str) and o.strip() for o in opts):
                raise RequestError(f'{name}: a choice needs "options", a list of non-empty strings')
            if not MIN_OPTIONS <= len(opts) <= mo:
                raise RequestError(f"{name}: {MIN_OPTIONS} to {mo} options (got {len(opts)})")
            if len(set(opts)) != len(opts):
                raise RequestError(f"{name}: duplicate options")
            opts = list(opts)
        out.append((name, {"state": req["state"], "instructions": ins, "qtype": qtype, "options": opts, "card": card}))
    return out


def request_from_row(row, name: str = "q0") -> dict:
    """The API v1 request (one question) for a decoder_io / dev row: what the bench sends for parity set P."""
    q = {"type": row["qtype"], "instructions": row["instructions"]}
    if row["qtype"] == "choice":
        q["options"] = list(row["options"])
    if row.get("card") is not None:
        q["card"] = row["card"]
    return {"id": row.get("id"), "state": row["state"], "questions": {name: q}}


@dataclass(eq=False)
class WorkItem:
    """One sequence to read: question q of a request, in view 0 (given order) or view 1 (exact reversal)."""
    q: int
    view: int
    perm: list | None
    text: str | None  # the exact prompt string (None until render_items: legacy renders inside the GPU worker)
    groups: list  # ro.cand(row): one list of token ids per displayed answer letter
    ids: list | None = None  # capped token ids (None until tokenize_items)
    n_tokens: int = 0  # len(ids) after the MAX_LEN cap (= usage input tokens of this read)
    n_raw: int = 0  # before the cap
    flat: list = field(default_factory=list)  # [t for g in groups for t in g]
    sizes: list = field(default_factory=list)  # [len(g) for g in groups]
    row: dict | None = None  # the decoder_io row (for render_items)


def views_for(row, choice_views: int = 2) -> list:
    """The perms one question is read with: [None] (noul, or choice_views=1) or [None, reversal] (choice, A5 2view)."""
    if row["qtype"] == "choice" and choice_views == 2:
        return [None, list(range(len(row["options"])))[::-1]]
    if choice_views not in (1, 2):
        raise ValueError(f"choice_views must be 1 or 2, not {choice_views!r}")
    return [None]


def build_items(ro, named, choice_views: int = 2, render: bool = True) -> list:
    """Work items for parsed questions: candidate groups, and (render=True) the prompt text. Tokens are filled by
    tokenize_items; render=False leaves the text to render_items (A0 builds prompts inside the GPU worker)."""
    items = []
    for qi, (_, row) in enumerate(named):
        groups = ro.cand(row)
        flat = [t for g in groups for t in g]
        sizes = [len(g) for g in groups]
        for vi, perm in enumerate(views_for(row, choice_views)):
            items.append(WorkItem(q=qi, view=vi, perm=perm, text=None, groups=groups, flat=flat, sizes=sizes, row=row))
    if render:
        render_items(ro, items)
    return items


def render_items(ro, items) -> None:
    """Fill the prompt text of every item that has none: decoder_io.prompt_texts(ro, [row], [perm])[0]."""
    for it in items:
        if it.text is None:
            it.text = dio.prompt_texts(ro, [it.row], [it.perm])[0]


def prepare_items(ro, tok, items) -> None:
    """render_items + tokenize_items (what the GPU worker runs for legacy requests)."""
    render_items(ro, items)
    tokenize_items(tok, items)


def cap_ids(ids: list, tok, max_len: int | None = None) -> list:
    """decoder_io's eager cap: tok(..., truncation=True, max_length=MAX_LEN) keeps the first MAX_LEN tokens (right
    truncation side, the default) or the last ones (left)."""
    m = dio.MAX_LEN if max_len is None else max_len
    if len(ids) <= m:
        return ids
    return ids[-m:] if getattr(tok, "truncation_side", "right") == "left" else ids[:m]


def tokenize_items(tok, items) -> None:
    """Fill ids / n_tokens / n_raw of every item: one batched tok(texts, add_special_tokens=False) call."""
    todo = [it for it in items if it.ids is None]
    if not todo:
        return
    if any(it.text is None for it in todo):
        raise ValueError("tokenize_items: render the prompt text first (render_items / prepare_items)")
    enc = tok([it.text for it in todo], add_special_tokens=False)["input_ids"]
    for it, ids in zip(todo, enc):
        it.n_raw = len(ids)
        it.ids = cap_ids(list(ids), tok)
        it.n_tokens = len(it.ids)


def _as_logits(x):
    import torch
    if isinstance(x, torch.Tensor):
        return x.detach().to("cpu", torch.float32)
    return torch.tensor(list(x), dtype=torch.float32)


def combine(named, items, logits, temps=None, return_views: bool = False):
    """Per-item candidate logits (fp32 tensors or float lists, in `items` order) -> ({name: answer}, request usage).
    choice: decoder_io.to_probs per view, then {o: (p_given[o] + p_reversed[o]) / 2 for o in options} (predict's
    tta_choice formula); noul: decoder_io.to_probs of the single read. Answer dicts are API v1."""
    T = dict(TEMPS if temps is None else temps)
    if len(logits) != len(items):
        raise ValueError(f"combine: {len(logits)} logits for {len(items)} items")
    by_q = {}
    for it, lg in zip(items, logits):
        lg = _as_logits(lg)
        if lg.shape != (len(it.groups),):
            raise ValueError(f"combine: question {it.q} view {it.view}: {tuple(lg.shape)} logits for {len(it.groups)} candidates")
        by_q.setdefault(it.q, []).append((it, lg))
    answers, total = {}, 0
    for qi, (name, row) in enumerate(named):
        reads = sorted(by_q.get(qi, []), key=lambda x: x[0].view)
        if not reads:
            raise ValueError(f"combine: no read for question {name!r}")
        t = T["noul" if row["qtype"] == "noul" else "choice"]
        probs = [dio.to_probs(row, lg, it.perm, temp=t) for it, lg in reads]
        usage = {"input_tokens": sum(it.n_tokens for it, _ in reads), "input_tokens_first_view": reads[0][0].n_tokens,
                 "views": len(reads)}
        total += usage["input_tokens"]
        if row["qtype"] == "noul":
            p = probs[0]
            ans = {"type": "noul", "noul": p["yes"], "probabilities": {"yes": p["yes"], "no": p["no"]}}
        else:
            if len(probs) == 2:
                p = {o: (probs[0][o] + probs[1][o]) / 2 for o in row["options"]}
            else:
                p = {o: probs[0][o] for o in row["options"]}
            best = max(p, key=p.get)
            ans = {"type": "choice", "choice": best, "confidence": p[best], "probabilities": p}
            if return_views:
                ans["view_probabilities"] = [{o: v[o] for o in row["options"]} for v in probs]
        ans["usage"] = usage
        answers[name] = ans
    return answers, {"input_tokens": total, "routed_rows": 0}


def readout_info(ro=None) -> dict:
    """The readout block of /health."""
    return {"api": API_VERSION, "layout": dio.LAYOUT, "style": dio.STYLE, "choice": "2view_prob_avg (given + exact reversal)",
            "noul": "single read", "temps": dict(TEMPS), "logits": "fp32 logsumexp over Readout.cand(row), last real token",
            "max_questions": MAX_QUESTIONS, "max_options": max_options(), "max_len": dio.MAX_LEN}
