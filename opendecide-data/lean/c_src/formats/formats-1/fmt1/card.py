"""Card and instructions renderers: card style + definition style + few-shot overlay + inverted frames.

Card IR:
  {"title": str | None, "blocks": [block, ...]}
  block types:
    {"type": "para", "text": str}
    {"type": "items", "items": [str, ...]} / {"type": "steps", "items": [str, ...]}
    {"type": "table", "columns": [...], "rows": [[...], ...], "caption": str | None}
    {"type": "defs", "variant": "DVxx", "heading": str | None, "columns": [...] (rubric_table only),
     "entries": [{"name": str, "text": str, "examples": [str, ...], "cells": [str, ...]}, ...]}
    {"type": "fewshot", "template": "FTxx", "heading": str | None,
     "examples": [{"case": str, "answer": str, "note": str | None}, ...]}
    {"type": "task", "text": str}            the card-level task line; IP4 / IP5 move it to the head / tail
    {"type": "section", "heading": str, "blocks": [...]}
The family writes every sentence (definitions, rules, reading rules, notices); the card style only lays them out.
Few-shot answers are option text (a label name, code, level text or Yes / No), never an option letter.

What the prompt shows (v1.1, review formats-1). C trains and serves with decoder_io's cygnet style and
schema_branch_mark layout (recipe v4; decoder_io.py sha256 908c08d7..., pinned below). decoder_io prints the whole card
on a yes/no row only. On a choice row it prints NO card text except lines "- {option text}: {definition}"
(decoder_io.card_defs), each appended to the matching option line. So:
  - render_row_text(..., qtype=...) is the only row entry point. On a choice row it writes option definitions with
    render_choice_defs (one "- {option}: {definition}" line per defined option, examples inline, the same for every
    card style) and lays every other card block out in the card style inside `instructions`, in the instruction
    position's order (IP4 / IP5: the task line starts / ends the instructions). render_card alone is the yes/no form.
  - loader_check(row) renders the row with decoder_io.user_msg (cygnet, schema_branch_mark) under a random option
    order and checks that every non-empty card line, definition, example and rule sentence is in the prompt and that
    the gold letter maps back to the gold option. Every family row must pass it (label rules LR04, LR07, LR14, LR15).
"""
from __future__ import annotations

import contextlib
import hashlib
import json
import random
import re
import string
import sys
from functools import lru_cache
from pathlib import Path

from . import pool
from .render import FormatError, text_table, text_value

LEAN = Path(__file__).resolve().parents[4]
DECODER_IO = LEAN / "decoder_io.py"
DECODER_IO_SHA256 = "908c08d752ce8896c2628a06f8a9d3153df8c76b657bf29daae44656f75f2948"  # A16 readout, frozen
TRAIN_DECODER = LEAN / "train_decoder.py"
TRAIN_DECODER_SHA256 = "c2c2d1d623ccd53f64254fb41400f5c952b4e1324d11550a01f170ab25ba04ef"  # A16 trainer (check_rows)
SERVE_STYLE, SERVE_LAYOUT = "cygnet", "schema_branch_mark"  # recipe v4; runs/q35_4b_c_r1.json
QTYPES = ("choice", "noul")  # noul = yes/no (the raw row format's name)
CHOICE_LINE = "- {name}: {text}"
CHOICE_EX = " (e.g. {ex})"
CHOICE_EX_JOIN = "; "

_CARD_KEYS = {"para": {"text"}, "items": {"items"}, "steps": {"items"}, "table": {"columns", "rows", "caption"},
              "defs": {"variant", "heading", "columns", "entries"}, "fewshot": {"template", "heading", "examples"},
              "task": {"text"}, "section": {"heading", "blocks"}}


def _check(blocks, depth=0):
    for b in blocks:
        t = b.get("type")
        if t not in _CARD_KEYS:
            raise FormatError(f"unknown card block {t!r}")
        extra = set(b) - _CARD_KEYS[t] - {"type"}
        if extra:
            raise FormatError(f"unknown keys {sorted(extra)} in card {t} block")
        if t == "section":
            if depth >= 1:
                raise FormatError("card sections nest 1 deep")
            _check(b["blocks"], depth + 1)


def _slug(h: str) -> str:
    s = re.sub(r"[^a-z0-9]+", "_", h.lower()).strip("_")
    if not s or not s[0].isalpha():
        s = "part_" + s
    return s


def _table_form(cs_form: str) -> str:
    return cs_form


# ----------------------------------------------------------------------------------------------------------------------
# definitions

_ENTRY_KEYS = {"one_line": {"name", "text"}, "one_line_examples": {"name", "text", "examples"},
               "rubric_table": {"name", "text", "examples", "cells"}, "decision_list": {"name", "text"},
               "short": {"name", "text"}}


def render_defs(block: dict, cs: dict, item_marker: str) -> str:
    v = pool.defs_variant(block["variant"])
    ents = block["entries"]
    if not ents:
        raise FormatError("empty defs block")
    sty = v["style"]
    lines: list[str] = []
    if sty == "none":
        raise FormatError("DV50 means the card has no defs block; leave the block out")
    for e in ents:  # a key this variant cannot show would be dropped silently: refuse it
        extra = set(e) - _ENTRY_KEYS[sty]
        if extra:
            raise FormatError(f"{v['id']} ({sty}) cannot show entry keys {sorted(extra)}")
    if sty in ("one_line", "one_line_examples"):
        for e in ents:
            name, text = text_value(e["name"]), text_value(e["text"])
            exs = [text_value(x) for x in e.get("examples", [])]
            if sty == "one_line" and exs:
                raise FormatError("one_line defs carry no examples")
            if len(exs) > 2:
                raise FormatError("at most 2 examples per definition")
            layout = v["layout"]
            if layout == "card":
                if cs["def_layout"] == "next_line":
                    head = [cs["def_fmt"].format(name=name, text=text), "    " + text]
                else:
                    head = [cs["def_fmt"].format(name=name, text=text)]
            elif layout == "next_line":
                head = [v["fmt"].format(name=name, text=text), v["indent"] + text]
            else:
                head = [v["fmt"].format(name=name, text=text)]
            if v.get("marker"):
                head[0] = item_marker + head[0]
            if exs:
                if v["ex_mode"] == "inline":
                    head[-1] = head[-1] + v["ex_fmt"].format(ex=v.get("ex_join", "; ").join(exs))
                else:
                    head += [v["ex_fmt"].format(ex=x, i=k + 1) for k, x in enumerate(exs)]
            lines.append("\n".join(head))
        joiner = "\n\n" if any("\n" in x for x in lines) and v["layout"] == "next_line" else "\n"
        return joiner.join(lines)
    if sty == "rubric_table":
        cols = block.get("columns")
        if not cols:
            raise FormatError("rubric_table needs columns")
        rows = []
        for e in ents:
            r = [e["name"], e["text"]] + list(e.get("cells", []))
            if len(r) != len(cols):
                raise FormatError("rubric row length differs from columns")
            rows.append(r)
        form = v["table"]
        if form == "blocks":
            out = []
            for r in rows:
                sub = [text_value(r[0])] + [v["cell_fmt"].format(col=text_value(c), cell=text_value(x))
                                            for c, x in zip(cols[1:], r[1:])]
                out.append("\n".join(sub))
            res = "\n\n".join(out)
        else:
            res = text_table(cols, rows, cs["table"] if form == "card" else form)
        if v.get("ex_mode") == "after_table":
            exl = [v["ex_fmt"].format(name=text_value(e["name"]), ex=text_value(x))
                   for e in ents for x in e.get("examples", [])]
            if exl:
                res += "\n\n" + "\n".join(exl)
        elif any(e.get("examples") for e in ents):
            raise FormatError("this rubric variant shows no examples")
        return res
    if sty == "decision_list":
        for i, e in enumerate(ents, start=1):
            if v.get("named"):
                lines.append(v["num_fmt"].format(name=text_value(e["name"]), text=text_value(e["text"])))
            else:
                if e.get("name"):
                    raise FormatError("this decision-list variant numbers rules; names are not shown")
                lines.append(v["num_fmt"].format(i=i, text=text_value(e["text"])))
        return "\n".join(lines)
    if sty == "short":
        names = [text_value(e["name"]) for e in ents]
        if any(e.get("text") for e in ents):
            raise FormatError("short defs show names only")
        if v["form"] == "list":
            return "\n".join(item_marker + n for n in names)
        sep = v["sep"]
        if any(sep.strip() in n for n in names):
            raise FormatError("a name contains the separator")
        return sep.join(names)
    raise FormatError(f"unknown defs style {sty}")


# ----------------------------------------------------------------------------------------------------------------------
# few-shot overlay

def render_fewshot(block: dict, cs: dict) -> tuple[str | None, str]:
    t = pool.fewshot_template(block["template"])
    exs = block["examples"]
    if not 1 <= len(exs) <= 3:
        raise FormatError("few-shot cards carry 1-3 worked examples")
    items = []
    for i, e in enumerate(exs, start=1):
        case = text_value(e["case"], single_line=(t["case"] == "inline"))
        ans = text_value(e["answer"])
        if re.fullmatch(r"[A-Z]{1,2}", ans) and ans not in ("OK",):
            raise FormatError("few-shot answers are option text, never an option letter")
        note = e.get("note")
        if t.get("needs_note") and not note:
            raise FormatError("this template shows a reason; give note")
        if note and not t.get("needs_note"):
            raise FormatError("this template shows no reason; drop note")
        if "json_keys" in t:
            items.append(json.dumps({t["json_keys"][0]: case, t["json_keys"][1]: ans}, ensure_ascii=False))
        else:
            items.append(t["item"].format(i=i, case=case, answer=ans, note=text_value(note) if note else ""))
    body = ("\n" if t["case"] == "inline" else "\n\n").join(items)
    if t.get("table_head"):
        body = t["table_head"] + "\n" + body
    header = block.get("heading") or t["header"]
    return header, body


# ----------------------------------------------------------------------------------------------------------------------
# card

def render_card(card: dict, style) -> str:
    st = pool.style(style) if isinstance(style, str) else style
    cs = pool.card_style(st["card_style"])
    ip = pool.instr_position(st["instr_position"])
    if set(card) - {"title", "blocks"}:
        raise FormatError("unknown card keys")
    blocks = list(card.get("blocks", []))
    _check(blocks)
    tasks = [b for b in blocks if b["type"] == "task"]
    if len(tasks) > 1:
        raise FormatError("one task line per card")
    if tasks and ip["card_task"] in ("head", "tail"):
        blocks.remove(tasks[0])
        blocks = ([tasks[0]] + blocks) if ip["card_task"] == "head" else (blocks + [tasks[0]])
    sec_no = [0]

    def heading(h: str) -> str:
        h = text_value(h)
        sec_no[0] += 1
        s = cs["heading"].format(heading=h, HEADING=h.upper(), n=sec_no[0], tag=_slug(h))
        if cs["underline"]:
            s += "\n" + cs["underline"] * len(h)
        return s

    def wrap(h: str, inner: str) -> str:
        """Heading + content, honoring the xml and indent wrappers."""
        if cs["wrapper"] == "xml":
            tag = _slug(text_value(h))
            return f"<{tag}>\n{inner}\n</{tag}>"
        if cs["wrapper"] == "indent":
            return heading(h) + "\n" + "\n".join(("    " + ln) if ln else "" for ln in inner.split("\n"))
        return heading(h) + "\n" + inner

    def step_fmt(i):
        return cs["step"].format(i=i, n=max(sec_no[0], 1))

    def render_blocks(bl) -> list[str]:
        out = []
        for b in bl:
            t = b["type"]
            if t in ("para", "task"):
                out.append(text_value(b["text"]))
            elif t == "items":
                out.append("\n".join(cs["item"] + text_value(i) for i in b["items"]))
            elif t == "steps":
                out.append("\n".join(step_fmt(k + 1) + text_value(i) for k, i in enumerate(b["items"])))
            elif t == "table":
                tb = text_table(b["columns"], b["rows"], cs["table"])
                out.append(wrap(b["caption"], tb) if b.get("caption") else tb)
            elif t == "defs":
                d = render_defs(b, cs, cs["item"])
                out.append(wrap(b["heading"], d) if b.get("heading") else d)
            elif t == "fewshot":
                h, body = render_fewshot(b, cs)
                out.append(wrap(h, body) if h else body)
            elif t == "section":
                inner = ("\n\n" if cs["blank_between"] else "\n").join(render_blocks(b["blocks"]))
                out.append(wrap(b["heading"], inner))
        return out
    parts = []
    if card.get("title"):
        t = text_value(card["title"])
        tl = cs["title"].format(title=t, TITLE=t.upper())
        if cs["underline"]:
            tl += "\n" + cs["underline"] * len(t)
        parts.append(tl)
    parts += render_blocks(blocks)
    text = ("\n\n" if cs["blank_between"] else "\n").join(parts)
    if cs["wrapper"] == "quote":
        text = "\n".join(("> " + ln) if ln else ">" for ln in text.split("\n"))
    if not text:
        raise FormatError("empty card")
    return text


# ----------------------------------------------------------------------------------------------------------------------
# instructions

def render_instructions(style, *, question: str, wording: str | None = None, note: str | None = None,
                        card_text: str | None = None, task: str | None = None) -> str:
    """Order the family's instruction wording, question and answer note by the style's instruction position.
    Choice rows (render_row_text) also pass the card text moved out of the card field (`card_text`, placed before the
    wording and question) and, under IP4 / IP5, the card's task line (`task`: first / last part of instructions)."""
    st = pool.style(style) if isinstance(style, str) else style
    ip = pool.instr_position(st["instr_position"])
    reg = pool.register(st["register"])
    q = text_value(question, single_line=False)
    if ip["q_prefix"] and reg["q_prefix"]:
        q = reg["q_prefix"] + " " + q
    parts = {"wording": text_value(wording, single_line=False) if wording else None, "question": q,
             "note": text_value(note, single_line=False) if note else None}
    core = ip["joiner"].join(parts[k] for k in ip["order"] if parts[k])
    if card_text is None and task is None:
        return core
    if task is not None and ip["card_task"] not in ("head", "tail"):
        raise FormatError(f"{ip['id']} keeps the task line inside the card text")
    seq = [task] if task is not None and ip["card_task"] == "head" else []
    if card_text:
        seq.append(card_text)
    seq.append(core)
    if task is not None and ip["card_task"] == "tail":
        seq.append(task)
    return "\n\n".join(seq)


# ----------------------------------------------------------------------------------------------------------------------
# rows: the qtype-aware entry point

def _fold(s: str) -> str:
    return " ".join(str(s).split()).casefold()


def render_choice_defs(entries: list[dict], *, options: list[str] | None = None, require_all: bool = False) -> str:
    """The card text of a choice row: exactly one line '- {option text}: {definition}' per defined option, examples
    inline on the same line (' (e.g. ex1; ex2)'). The same for every card style: decoder_io.card_defs reads these
    lines and nothing else on a choice row. `name` must be the exact option text (masked ID, swapped word, level text).
    options: the row's option texts; then every name must be one of them (require_all: every option defined)."""
    if not entries:
        raise FormatError("no option definitions")
    lines, seen = [], set()
    for e in entries:
        extra = set(e) - {"name", "text", "examples"}
        if extra:
            raise FormatError(f"choice definition entries take name, text, examples; not {sorted(extra)}")
        name, text = text_value(e["name"]), text_value(e["text"])
        if name != name.strip() or text != text.strip():
            raise FormatError("leading or trailing space in a choice definition")
        if ": " in name:
            raise FormatError("an option text holding ': ' cannot carry a definition line (decoder_io.card_defs "
                              "splits each line at its first ': ')")
        if name in seen:
            raise FormatError("two definition lines for one option (decoder_io keeps only the last)")
        if options is not None and name not in options:
            near = [o for o in options if _fold(o) == _fold(name)]
            raise FormatError("definition name differs from its option text" + (" only in case or spacing" if near
                              else ": no option has this text, so the line would be hidden on a choice row"))
        seen.add(name)
        exs = [text_value(x) for x in e.get("examples") or []]
        if len(exs) > 2:
            raise FormatError("at most 2 examples per definition")
        line = CHOICE_LINE.format(name=name, text=text)
        if exs:
            line += CHOICE_EX.format(ex=CHOICE_EX_JOIN.join(exs))
        lines.append(line)
    if require_all and options is not None:
        missing = [o for o in options if o not in seen]
        if missing:
            raise FormatError(f"{len(missing)} option(s) without a definition line")
    return "\n".join(lines)


def _split_choice_card(card: dict, st: dict, options: list[str]) -> tuple[list[dict], dict, dict | None]:
    """(option definition entries, the rest of the card IR, the task block moved by IP4 / IP5 or None)."""
    if set(card) - {"title", "blocks"}:
        raise FormatError("unknown card keys")
    blocks = list(card.get("blocks", []))
    _check(blocks)
    opt = set(options)
    folded = {_fold(o) for o in options}
    entries: list[dict] = []

    def walk(bl):
        out = []
        for b in bl:
            t = b["type"]
            if t == "defs":
                v = pool.defs_variant(b["variant"])
                keep = []
                for e in b["entries"]:
                    nm = e.get("name")
                    if isinstance(nm, str) and nm not in opt and _fold(nm) in folded:
                        raise FormatError("a definition name differs from its option text only in case or spacing; "
                                          "use the exact option text")
                    if v["choice_route"] == "option_lines" and isinstance(nm, str) and nm in opt:
                        extra = set(e) - _ENTRY_KEYS[v["style"]]
                        if extra:
                            raise FormatError(f"{v['id']} ({v['style']}) cannot show entry keys {sorted(extra)}")
                        entries.append({k: e[k] for k in ("name", "text", "examples") if e.get(k) is not None})
                    else:
                        keep.append(e)
                if keep:
                    out.append({**b, "entries": keep})
            elif t == "section":
                inner = walk(b["blocks"])
                if inner:
                    out.append({**b, "blocks": inner})
            else:
                out.append(b)
        return out
    rest = walk(blocks)
    task = None
    ip = pool.instr_position(st["instr_position"])
    tasks = [b for b in rest if b["type"] == "task"]
    if len(tasks) > 1:
        raise FormatError("one task line per card")
    if tasks and ip["card_task"] in ("head", "tail"):
        task = tasks[0]
        rest.remove(task)
    rest_card = {"blocks": rest}
    if card.get("title"):
        rest_card["title"] = card["title"]
    return entries, rest_card, task


def render_row_text(style, *, doc: dict, question: str, qtype: str, card: dict | None = None,
                    options: list[str] | None = None, wording: str | None = None, note: str | None = None,
                    allow_null: bool = False, choice_card: str = "move") -> dict:
    """state, card and instructions for one row in one style. The outer prompt layout is untouched.
    qtype "noul" (yes/no): the card is rendered whole (decoder_io prints it under "Definitions:").
    qtype "choice": `options` (the row's option texts) is required. Option definitions become
    '- {option}: {definition}' card lines (render_choice_defs); every other card block (paragraphs, items, steps,
    tables, term definitions, rubric tables, decision lists, few-shot blocks, inverted frames, notices, the task line)
    is laid out in the card style inside instructions, before the wording and question; under IP4 / IP5 the task line
    is the first / last part of instructions. choice_card="refuse" raises instead of moving anything.
    Moved text is printed twice by schema_branch_mark (the question is repeated after the text): count it twice
    against the token cap."""
    from .render import render_state
    if qtype not in QTYPES:
        raise FormatError(f"qtype must be one of {QTYPES} (noul = yes/no), not {qtype!r}")
    st = pool.style(style) if isinstance(style, str) else style
    out = {"state": render_state(doc, st, allow_null=allow_null)}
    if qtype == "noul":
        text = render_card(card, st) if card else None
        if text and any(ln.startswith(("- Yes: ", "- No: ")) for ln in text.split("\n")):
            raise FormatError("a yes/no card line '- Yes: ' or '- No: ' is glued to the option by decoder_io")
        out["instructions"] = render_instructions(st, question=question, wording=wording, note=note)
        out["card"] = text
        return out
    if choice_card not in ("move", "refuse"):
        raise FormatError("choice_card is 'move' or 'refuse'")
    if not options or not all(isinstance(o, str) for o in options):
        raise FormatError("choice rows need options= (the row's option texts) to place the definitions")
    entries, rest, task = _split_choice_card(card, st, list(options)) if card else ([], {"blocks": []}, None)
    if choice_card == "refuse" and (rest["blocks"] or rest.get("title") or task):
        raise FormatError("choice row: only option definitions can stay in the card; other blocks would be hidden")
    moved = render_card(rest, st) if (rest["blocks"] or rest.get("title")) else None
    out["instructions"] = render_instructions(st, question=question, wording=wording, note=note, card_text=moved,
                                              task=text_value(task["text"]) if task else None)
    out["card"] = render_choice_defs(entries, options=list(options)) if entries else None
    return out


def must_show(card: dict | None = None, *, question: str | None = None, wording: str | None = None,
              note: str | None = None) -> list[str]:
    """The strings loader_check must find in the prompt: every content string of the card IR (definitions, examples,
    rubric cells, rules, paragraphs, items, steps, table cells, few-shot cases / answers / reasons, the task line) plus
    the question, wording and note. Titles and headings are chrome (a card style may re-case or tag them): left out."""
    out: list[str] = []

    def add(v, single=True):
        if v is not None:
            out.append(text_value(v, single_line=single))

    def walk(bl):
        for b in bl:
            t = b["type"]
            if t in ("para", "task"):
                add(b["text"])
            elif t in ("items", "steps"):
                for x in b["items"]:
                    add(x)
            elif t == "table":
                for c in b["columns"]:
                    add(c)
                for r in b["rows"]:
                    for c in r:
                        add(c)
            elif t == "defs":
                for e in b["entries"]:
                    for k in ("name", "text"):
                        add(e.get(k))
                    for x in e.get("examples") or []:
                        add(x)
                    for x in e.get("cells") or []:
                        add(x)
            elif t == "fewshot":
                for e in b["examples"]:
                    add(e["case"], single=False)
                    add(e["answer"])
                    add(e.get("note"))
            elif t == "section":
                walk(b["blocks"])
    if card:
        walk(card.get("blocks", []))
    for x in (question, wording, note):
        if x:
            out.append(text_value(x, single_line=False))
    return out


# ----------------------------------------------------------------------------------------------------------------------
# loader check: the row as decoder_io renders it for training and serving

@lru_cache(maxsize=None)
def _dio():
    """lean/decoder_io.py, the pinned A16 readout (refuses any other version)."""
    got = hashlib.sha256(DECODER_IO.read_bytes()).hexdigest()
    if got != DECODER_IO_SHA256:
        raise FormatError(f"decoder_io.py sha256 {got[:12]} is not the A16 readout {DECODER_IO_SHA256[:12]}")
    mod = sys.modules.get("decoder_io")
    if mod is None:
        if str(LEAN) not in sys.path:
            sys.path.insert(0, str(LEAN))
        import decoder_io as mod
    if Path(mod.__file__).resolve() != DECODER_IO.resolve():
        raise FormatError(f"imported decoder_io is {mod.__file__}, not {DECODER_IO}")
    return mod


@lru_cache(maxsize=None)
def _td():
    """lean/train_decoder.py, the pinned A16 trainer (for check_rows, G15); refuses any other version."""
    got = hashlib.sha256(TRAIN_DECODER.read_bytes()).hexdigest()
    if got != TRAIN_DECODER_SHA256:
        raise FormatError(f"train_decoder.py sha256 {got[:12]} is not the A16 trainer {TRAIN_DECODER_SHA256[:12]}")
    _dio()
    mod = sys.modules.get("train_decoder")
    if mod is None:
        import train_decoder as mod
    if Path(mod.__file__).resolve() != TRAIN_DECODER.resolve():
        raise FormatError(f"imported train_decoder is {mod.__file__}, not {TRAIN_DECODER}")
    return mod


@contextlib.contextmanager
def _serving(dio, n: int):
    saved = (dio.STYLE, dio.LAYOUT, dio.WIDE)
    try:
        dio.STYLE, dio.LAYOUT = SERVE_STYLE, SERVE_LAYOUT
        if n > len(dio.WIDE):  # placeholder two-letter labels; a Readout fills the tokenizer's real set
            U = string.ascii_uppercase
            dio.WIDE = list(U) + [a + b for a in U for b in U]
        yield
    finally:
        dio.STYLE, dio.LAYOUT, dio.WIDE = saved


def _norm(s: str) -> str:
    return " ".join(s.split())


def loader_check(row: dict, *, must_show: list[str] | tuple = (), seed: str = "fmt1-loader", perm: list | None = None,
                 raise_on_fail: bool = False, check_rows: bool = True) -> dict:
    """Render `row` (raw format: qtype, state, instructions, options, gold, card) with decoder_io.user_msg in the
    trained and served prompt (cygnet, schema_branch_mark) under a random option order (seeded by seed and row id;
    or `perm`) and check:
      - the option block is exactly decoder_io's (one line per option, label, text, its definition if any);
      - every non-empty card line is in the prompt: yes/no rows print the card whole; on choice rows every card line
        must be a '- {option}: {definition}' line of a shown option (other lines are hidden), one per option;
      - no yes/no card line '- Yes: ' / '- No: ' (glued to the option);
      - every line of every `must_show` string (card.must_show) is in the prompt (whitespace-normalised);
      - the gold letter maps back: the option line under gold's letter shows the gold option;
      - check_rows: train_decoder.check_rows([row]) accepts it (pinned A16 trainer). With the above this is G15's
        per-row part (relation-unit and real-tokenizer length checks stay with the family and the mixer).
    Returns {"ok", "problems", "gold_letter", "perm", "n_options", "prompt_sha256"}; raise_on_fail raises FormatError."""
    dio = _dio()
    probs: list[str] = []
    qt = row.get("qtype")
    card_text = row.get("card")
    if qt not in QTYPES:
        probs.append(f"qtype {qt!r} is not one of {QTYPES}")
        res = {"ok": False, "problems": probs, "gold_letter": None, "perm": None, "n_options": 0,
               "prompt_sha256": None}
        if raise_on_fail:
            raise FormatError("; ".join(probs))
        return res
    if qt == "noul":
        opts = ["Yes", "No"]
        g = row.get("gold")
        gold = None if g is None else ("Yes" if g == 1 else "No")  # decoder_io.as_letter_row
    else:
        opts = list(row.get("options") or [])
        gold = row.get("gold")
        if len(opts) < 2:
            probs.append("a choice row needs at least 2 options")
        if not all(isinstance(o, str) and o for o in opts):
            probs.append("every option is a non-empty string")
        if any(isinstance(o, str) and ("\n" in o or "\r" in o) for o in opts):
            probs.append("an option text holds a line break (it would split its option line)")
        if len(set(opts)) != len(opts):
            probs.append("duplicate option texts")
    n = len(opts)
    if perm is None:
        rng = random.Random(int.from_bytes(hashlib.sha256(f"{seed}:{row.get('id')}".encode()).digest()[:8], "big"))
        perm = list(range(n))
        rng.shuffle(perm)
    elif sorted(perm) != list(range(n)):
        probs.append("perm is not a permutation of the options")
        perm = list(range(n))
    with _serving(dio, n):
        prompt = dio.user_msg(row, perm)
        labs = [dio.label(i) for i in range(n)]
        defs = dio.card_defs(card_text)
    head = (f"Definitions:\n{card_text}\n\n" if qt == "noul" and card_text else "") \
        + str(row.get("instructions") or "").rstrip() + "\n\nOptions:\n"
    shown: list[str] = []
    if not prompt.startswith(head):
        probs.append("prompt does not start with the expected definitions / instructions / options block")
    else:
        shown = prompt[len(head):].split("\n")[:n]
        for j in range(n):
            o = opts[perm[j]]
            want = f"{labs[j]}. {o}" + (f": {defs[o]}" if o in defs else "")
            if j >= len(shown) or shown[j] != want:
                probs.append(f"option line {j + 1} is not decoder_io's form")
    if card_text:
        lines = card_text.split("\n")
        if qt == "noul":
            if f"Definitions:\n{card_text}" not in prompt:
                probs.append("yes/no card not printed whole")
            if any(k in ("Yes", "No") for k in defs):
                probs.append("yes/no card has a '- Yes: ' / '- No: ' line (glued to the option)")
        else:
            keys = []
            for i, ln in enumerate(lines):
                if not ln.strip():
                    continue
                if not (ln.startswith("- ") and ": " in ln):
                    probs.append(f"card line {i + 1} is hidden on a choice row (not '- {{option}}: {{definition}}')")
                    continue
                k = ln[2:].split(": ", 1)[0]
                if k not in opts:
                    probs.append(f"card line {i + 1} names no option text (hidden on a choice row)")
                    continue
                keys.append(k)
            if len(keys) != len(set(keys)):
                probs.append("two card lines for one option (decoder_io keeps only the last)")
    np_ = _norm(prompt)
    for idx, s in enumerate(must_show):
        for ln in str(s).split("\n"):
            t = _norm(ln)
            if t and t not in np_ and _norm(json.dumps(ln, ensure_ascii=False)[1:-1]) not in np_:
                probs.append(f"must_show item {idx} not in the prompt: {t[:48]!r}")
                break
    if check_rows:
        try:
            _td().check_rows([row])
        except (ValueError, KeyError, TypeError) as e:
            probs.append(f"train_decoder.check_rows refuses the row: {str(e)[:160]}")
    letter = None
    if gold is None or gold not in opts:
        probs.append("gold is not one of the options")
    elif shown and len(shown) == n:
        j = perm.index(opts.index(gold))
        letter = labs[j]
        line = shown[j]
        back = line[len(letter) + 2:] if line.startswith(f"{letter}. ") else None
        if back is None or not (back == gold or back.startswith(gold + ": ")):
            probs.append("gold letter does not map back to the gold option")
        branch = [x for x in prompt.split("\n") if x.startswith("Options: ")]
        if not branch or f"{letter}. {gold}" not in branch[-1]:
            probs.append("gold letter missing from the repeated options line")
    res = {"ok": not probs, "problems": probs, "gold_letter": letter, "perm": perm, "n_options": n,
           "prompt_sha256": hashlib.sha256(prompt.encode()).hexdigest()}
    if raise_on_fail and probs:
        raise FormatError("loader_check: " + "; ".join(probs))
    return res


def render_and_check(style, *, doc: dict, question: str, qtype: str, gold, card: dict | None = None,
                     options: list[str] | None = None, wording: str | None = None, note: str | None = None,
                     allow_null: bool = False, choice_card: str = "move", row_id: str | None = None,
                     seed: str = "fmt1-loader") -> tuple[dict, dict]:
    """render_row_text + loader_check in one call: (row fields, check result). Raises FormatError on a failed check."""
    f = render_row_text(style, doc=doc, question=question, qtype=qtype, card=card, options=options, wording=wording,
                        note=note, allow_null=allow_null, choice_card=choice_card)
    row = {"id": row_id, "qtype": qtype, "options": list(options) if qtype == "choice" else None, "gold": gold, **f}
    res = loader_check(row, must_show=must_show(card, question=question, wording=wording, note=note), seed=seed,
                       raise_on_fail=True)
    return f, res


# ----------------------------------------------------------------------------------------------------------------------
# inverted cards

def inverted_question(qid: str, target: str) -> str:
    q = pool.inverted(qid)
    if q["kind"] != "inverted_question":
        raise FormatError("not an inverted question id")
    return q["text"].format(target=text_value(target))


def inverted_frame(fid: str) -> str:
    f = pool.inverted(fid)
    if f["kind"] != "inverted_card_frame":
        raise FormatError("not an inverted card frame id")
    return f["text"]


def case_refs(ref_id: str, n: int, seed_key: str, scheme: str = "MS10") -> list[str]:
    """n case references like 'Case K7' with unordered random IDs (see labels.masked_ids)."""
    from .labels import masked_ids
    r = pool.inverted(ref_id)
    if r["kind"] != "inverted_case_ref":
        raise FormatError("not a case reference scheme id")
    return [r["fmt"].format(id=x) for x in masked_ids(scheme, n, seed_key)]
