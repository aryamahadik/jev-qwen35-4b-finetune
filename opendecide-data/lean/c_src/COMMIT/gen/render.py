"""COMMIT renderer (G0 1.3, 1.12): style pick, state assembly, row fields via fmt1, loader_check, counted length.

State layout. fmt1 containers refuse line breaks inside values, but a real message and a real diff are multi-line
and must never be edited (1.9). So the message is laid out by the row's container as one paragraph per message line
(blank lines dropped, order and words unchanged), and the diff part (route: hunks with neutral separators; other
diff views: headers + hunks + cut markers; score and count rules: numstat + total line) is appended verbatim after
the container text in a fenced block. Inverted rows put each case under its case reference the same way.
Training rows take styles only through fmt1 pool.training_style; S5 dev rows only through pool.dev_style.
"""
from __future__ import annotations

import string
import sys
from functools import lru_cache
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import common as C  # noqa: E402

sys.path.insert(0, str(C.CSRC / "formats" / "formats-1"))
sys.path.insert(0, str(C.CSRC / "common"))
from fmt1 import card as fcard  # noqa: E402
from fmt1 import pool as fpool  # noqa: E402
from fmt1.render import FormatError  # noqa: E402

CAP = 1999            # counted length cap of every commit row (1.3, A16.1 g)
ROUTE_SEP = "~~~~~~~~"  # neutral separator between files on route rows (carries no name)


@lru_cache(maxsize=4)
def style_ids(view_kind: str, heldout: bool) -> tuple:
    """view_kind: 'restricted' (route rows and message-only rows: containers with no path and no stats, A59) or
    'full'. Returns style ids sorted (the pick is label-independent)."""
    kw = {"held_out": heldout}
    if view_kind == "restricted":
        kw["compat"] = "COMMIT_route_or_message_only"
    return tuple(sorted(s["id"] for s in fpool.styles(**kw) if s["container"] != "diff"))


def message_doc(msg: str, heading: str = "Commit message") -> dict:
    lines = [ln for ln in msg.split("\n") if ln.strip()]
    return {"title": None, "meta": [],
            "blocks": [{"type": "section", "heading": heading, "blocks": [{"type": "para", "text": ln}
                                                                          for ln in lines]}]}


def get_style(sid: str, heldout: bool) -> dict:
    return fpool.dev_style(sid) if heldout else fpool.training_style(sid)


def pick_style(view_kind: str, heldout: bool, *key, doc: dict | None = None, allow=None) -> dict:
    """First style (in a fixed hash order over ids) that can render `doc`; never reads the label. `allow`: optional
    style predicate (match rows: styles whose chrome adds no code-shaped word)."""
    ids = sorted(style_ids(view_kind, heldout), key=lambda s: fpool.unit_hash("COMMIT-style", *key, s))
    from fmt1.render import render_state
    for sid in ids:
        st = get_style(sid, heldout)
        if allow is not None and not allow(st):
            continue
        if doc is None:
            return st
        try:
            render_state(doc, st)
            return st
        except FormatError:
            continue
    raise FormatError("no style renders this doc")


def fence(body: str, tag: str = "diff") -> str:
    return f"```{tag}\n{body}\n```"


def assemble(style: dict, *, msg: str, extra: str | None, question: str, qtype: str, card: dict | None,
             options: list[str] | None, wording: str | None, gold, row_id: str, heading: str = "Commit message",
             state_first: str | None = None, doc: dict | None = None):
    """Row fields + loader_check (raises FormatError on a failed check: a generator bug, never a dropped row)."""
    doc = doc or message_doc(msg, heading)
    f = fcard.render_row_text(style, doc=doc, question=question, qtype=qtype, card=card, options=options,
                              wording=wording, choice_card="move")
    if extra:
        f["state"] = f["state"] + "\n\n" + extra
    if state_first:
        f["state"] = state_first + "\n\n" + f["state"]
    row = {"id": row_id, "qtype": qtype, "options": list(options) if qtype == "choice" else None, "gold": gold, **f}
    res = fcard.loader_check(row, must_show=fcard.must_show(card, question=question, wording=wording),
                             seed="COMMIT-loader", raise_on_fail=True)
    return f, res


class Tok:
    """Counted length of the full served prompt (cygnet, schema_branch_mark, chat template; instructions twice)."""

    def __init__(self):
        from transformers import AutoTokenizer
        self.tok = AutoTokenizer.from_pretrained("Qwen/Qwen3.5-4B", local_files_only=True)
        self.dio = fcard._dio()

    def user_msg(self, raw: dict, perm: list) -> str:
        dio = self.dio
        saved = (dio.STYLE, dio.LAYOUT, dio.WIDE)
        try:
            dio.STYLE, dio.LAYOUT = "cygnet", "schema_branch_mark"
            if len(perm) > len(dio.WIDE):
                U = string.ascii_uppercase
                dio.WIDE = list(U) + [a + b for a in U for b in U]
            return dio.user_msg(raw, perm)
        finally:
            dio.STYLE, dio.LAYOUT, dio.WIDE = saved

    def count(self, raw: dict, perm: list | None = None) -> int:
        n = len(raw["options"]) if raw.get("qtype") == "choice" else 2
        perm = perm if perm is not None else list(range(n))
        s = self.dio.render_chat(self.tok, self.dio.CYGNET_SYSTEM, self.user_msg(raw, perm))
        return len(self.tok(s, add_special_tokens=False)["input_ids"])

    def text_len(self, s: str) -> int:
        return len(self.tok(s, add_special_tokens=False)["input_ids"])
