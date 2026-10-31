"""Real-tokenizer lengths (Qwen/Qwen3.5-4B, the C base; local files only). G0 s1 / A16.1 (g): fields-based count =
state + card + 2 x instructions + options; the full cygnet / schema_branch_mark prompt is also reported."""
from __future__ import annotations

from functools import lru_cache


@lru_cache(maxsize=1)
def tok():
    from transformers import AutoTokenizer
    return AutoTokenizer.from_pretrained("Qwen/Qwen3.5-4B", local_files_only=True)


def n(text: str) -> int:
    return len(tok().encode(text or "", add_special_tokens=False))


def row_len(row: dict) -> int:
    opts = row.get("options") or ["Yes", "No"]
    return n(row["state"]) + n(row.get("card") or "") + 2 * n(row["instructions"]) + sum(n(o) for o in opts)


def prompt_len(row: dict) -> int:
    import sys
    from fmt1 import card as fcard
    dio = fcard._dio()
    with fcard._serving(dio, len(row.get("options") or [1, 2])):
        p = dio.user_msg(row, None)
    return n(p)
