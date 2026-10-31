"""Real-tokenizer row length = the SERVED prompt (G0 s2 'Length', G15, A16.1 (g)): decoder_io.user_msg under
STYLE 'cygnet' + LAYOUT 'schema_branch_mark' (prints `instructions` and the option texts twice), rendered as a chat with
decoder_io.CYGNET_SYSTEM through decoder_io.render_chat, Qwen/Qwen3.5-4B tokenizer (the C base; local files only).
Same count as F10 qc/gates.served_tokens. decoder_io is imported read-only (pinned by sha); its module globals are
restored after every call.

row_len(row)          -> served tokens of one row (cached on the row's served text)
served_lens(rows)     -> [served tokens], batched
fields_len(row)       -> the old field sum (state + card + 2 x instructions + options), kept for reports only"""
from __future__ import annotations

import os
from functools import lru_cache

os.environ.setdefault("RAYON_NUM_THREADS", "2")
os.environ.setdefault("TOKENIZERS_PARALLELISM", "true")

MAX_SERVED = 7900          # A22 / task: every row <= 7,900 served tokens
_U = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"


@lru_cache(maxsize=1)
def tok():
    from transformers import AutoTokenizer
    return AutoTokenizer.from_pretrained("Qwen/Qwen3.5-4B", local_files_only=True)


@lru_cache(maxsize=1)
def _dio():
    import decoder_io
    return decoder_io


def served_text(row: dict) -> str:
    dio = _dio()
    saved = (dio.STYLE, dio.LAYOUT, dio.WIDE)
    try:
        dio.STYLE, dio.LAYOUT = "cygnet", "schema_branch_mark"
        if row.get("options") and len(row["options"]) > len(dio.WIDE):
            dio.WIDE = list(_U) + [a + b for a in _U for b in _U]
        return dio.render_chat(tok(), dio.CYGNET_SYSTEM, dio.user_msg(dict(row), None))
    finally:
        dio.STYLE, dio.LAYOUT, dio.WIDE = saved


@lru_cache(maxsize=200000)
def _n(text: str) -> int:
    return len(tok()(text, add_special_tokens=False)["input_ids"])


def row_len(row: dict) -> int:
    return _n(served_text(row))


def served_lens(rows) -> list:
    texts = [served_text(r) for r in rows]
    out = []
    for i in range(0, len(texts), 128):
        out += [len(e) for e in tok()(texts[i:i + 128], add_special_tokens=False)["input_ids"]]
    return out


@lru_cache(maxsize=200000)
def n(text: str) -> int:
    return len(tok().encode(text or "", add_special_tokens=False))


def fields_len(row: dict) -> int:
    opts = row.get("options") or ["Yes", "No"]
    return n(row["state"] or "") + n(row.get("card") or "") + 2 * n(row["instructions"] or "") + sum(n(o) for o in opts)
