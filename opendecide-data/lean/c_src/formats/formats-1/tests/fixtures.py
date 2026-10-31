"""Placeholder Docs and cards for tests and previews. Neutral placeholder tokens only: no domain, no rows."""
from __future__ import annotations

import datetime as dt
from decimal import Decimal

from fmt1 import pool
from fmt1.render import ABSENT, BLANK, OMIT, Choice  # noqa: F401

TS = [dt.datetime(2031, 5, 6, 9, 14), dt.datetime(2031, 5, 6, 9, 20), dt.datetime(2031, 5, 7, 16, 2)]


def _table():
    return {"type": "table", "caption": "Table alpha", "columns": ["Col one", "Col two", "Col three"],
            "rows": [["Cell a1", 17, "Cell c1"], ["Cell a2", Decimal("12.50"), "Cell c2, with comma"]]}


def _events(actor=True, level=True):
    ev = []
    for i, t in enumerate(TS):
        e = {"ts": t, "text": f"Event text {i + 1}"}
        if actor:
            e["actor"] = f"agent{i + 1}"
        if level:
            e["level"] = ["info", "warn", "info"][i]
        ev.append(e)
    return {"type": "events", "events": ev}


def _messages(ts=True, to=True, subject=True, quoted_ok=False):
    ms = []
    for i in range(3):
        m = {"speaker": f"Person {chr(65 + i)}", "text": f"Message body {i + 1}."}
        if ts:
            m["ts"] = TS[i]
        newest = i == 2
        if to and (newest or not quoted_ok):
            m["to"] = f"Person {chr(66 + i)}"
        if subject and (newest or not quoted_ok):
            m["subject"] = "Subject line"
        ms.append(m)
    return {"type": "messages", "messages": ms}


META = [["To", "Person B"], ["From", "Person A"], ["Date", "6 May 2031"], ["Subject", "Subject text"]]
FIELDS = {"type": "fields", "label": "Fields alpha", "pairs": [["Key alpha", "Value 1"], ["Key beta", 42],
                                                               ["Key gamma", "Value 3"]]}
FIELDS_NOLABEL = {"type": "fields", "label": None, "pairs": [["Key alpha", "Value 1"], ["Key beta", 42],
                                                             ["Key gamma", "Value 3"]]}


def doc_for(skin_id: str) -> dict:
    sk = pool.skin(skin_id)
    c = sk["container"]
    p = sk["params"]
    if c == "prose":
        return {"title": "Title alpha", "blocks": [
            {"type": "para", "text": "Paragraph one text."},
            {"type": "items", "items": ["Item one.", "Item two."]},
            FIELDS_NOLABEL,
            {"type": "section", "heading": "Section alpha", "blocks": [
                {"type": "para", "text": "Paragraph two text."},
                {"type": "steps", "items": ["Step one.", "Step two."]}]}]}
    if c == "memo":
        return {"title": "Title alpha", "meta": META, "blocks": [
            {"type": "para", "text": "Paragraph one text."},
            {"type": "items", "items": ["Item one", "Item two"]},
            {"type": "steps", "items": ["Step one", "Step two"]},
            FIELDS,
            {"type": "table", "caption": "Table alpha", "columns": ["Col one", "Col two"],
             "rows": [["Cell a1", 17], ["Cell a2", "Cell b2"]]},
            {"type": "section", "heading": "Section alpha", "blocks": [{"type": "para", "text": "Paragraph two."}]}]}
    if c == "email_thread":
        if p["order"] == "single":
            return {"title": None, "meta": META, "blocks": [
                {"type": "para", "text": "Paragraph one text."},
                {"type": "items", "items": ["Item one", "Item two"]}, FIELDS]}
        return {"title": "Thread alpha", "blocks": [_messages(quoted_ok=(p["order"] == "newest_first"))]}
    if c == "chat_log":
        return {"blocks": [_messages(ts=p["needs_ts"], to=False, subject=False)]}
    if c in ("json", "yaml"):
        if p.get("layout") in ("lines", "array"):
            t = _table()
            t["caption"] = None
            return {"blocks": [t]}
        return {"title": "Title alpha", "meta": [["Date", "6 May 2031"], ["Ref", "R7"]], "blocks": [
            {"type": "para", "text": "Paragraph one text."},
            {"type": "items", "items": ["Item one", "Item two"]},
            {"type": "steps", "items": ["Step one", "Step two"]},
            FIELDS, _table(), _events(), _messages(),
            {"type": "section", "heading": "Section alpha", "blocks": [
                {"type": "fields", "label": None, "pairs": [["Key delta", True], ["Key epsilon", Decimal("3.25")]]}]}]}
    if c == "csv":
        t = _table()
        t["caption"] = None
        if p["fixed"]:
            t["rows"][1][2] = "Cell c2 with words"
        return {"title": "Title alpha", "blocks": [t]}
    if c in ("markdown_table", "html_snippet"):
        return {"title": "Title alpha", "meta": [["Date", "6 May 2031"], ["Ref", "R7"]], "blocks": [
            {"type": "para", "text": "Paragraph one text."},
            {"type": "items", "items": ["Item one", "Item two"]},
            {"type": "steps", "items": ["Step one", "Step two"]},
            FIELDS, _table(), _events(),
            {"type": "section", "heading": "Section alpha", "blocks": [
                {"type": "para", "text": "Paragraph two text."}]}]}
    if c == "key_value":
        return {"title": "Title alpha", "meta": [["Date", "6 May 2031"], ["Ref", "R7"]], "blocks": [
            FIELDS, {"type": "table", "caption": "Table alpha", "columns": ["Col one", "Col two"],
                     "rows": [["Cell a1", 17], ["Cell a2", "Cell b2"]]},
            _events(),
            {"type": "section", "heading": "Section alpha", "blocks": [
                {"type": "fields", "label": None, "pairs": [["Key delta", "Value 4"], ["Key omega", OMIT]]}]}]}
    if c == "bullet_sop":
        return {"title": "Title alpha", "meta": [["Date", "6 May 2031"]], "blocks": [
            {"type": "para", "text": "Paragraph one text."},
            {"type": "section", "heading": "Section alpha", "blocks": [
                {"type": "steps", "items": ["Step one", "Step two", "Step three"]},
                {"type": "items", "items": ["Item one", "Item two"]}]},
            {"type": "section", "heading": "Section beta", "blocks": [FIELDS_NOLABEL]}]}
    if c == "log_lines":
        return {"title": "Title alpha", "blocks": [_events()]}
    if c == "diff":
        entries = [{"key": "key_alpha", "value": "Value 1"}, {"key": "key_beta", "old": "Value 2", "new": "Value 2b"},
                   {"key": "key_gamma", "old": 5, "new": 7}]
        if p["form"] != "table":
            entries += [{"key": "key_delta", "old": ABSENT, "new": "Value 4"},
                        {"key": "key_eps", "old": "Value 5", "new": ABSENT}]
        return {"title": "Title alpha", "blocks": [
            {"type": "changes", "target": "conf/alpha.cfg" if p.get("header") == "path" else None,
             "entries": entries}]}
    if c == "form":
        return {"title": "Title alpha", "meta": [["Date", "6 May 2031"], ["Ref", "R7"]], "blocks": [
            {"type": "fields", "label": None, "pairs": [["Key alpha", "Value 1"],
                                                        ["Key choice", Choice("Opt two", ["Opt one", "Opt two"])]]},
            {"type": "section", "heading": "Section alpha", "blocks": [
                {"type": "fields", "label": None, "pairs": [["Key beta", 42], ["Key gamma", "Value 3"]]},
                {"type": "para", "text": "Paragraph one text."}]},
            {"type": "table", "caption": None, "columns": ["Col one", "Col two"],
             "rows": [["Cell a1", 17], ["Cell a2", "Cell b2"]]}]}
    raise KeyError(c)


def card_for(i: int) -> dict:
    """A placeholder card that cycles through the definition styles and overlays."""
    dvs = [v["id"] for v in pool.defs_variants("one_line") + pool.defs_variants("one_line_examples")]
    dv = dvs[i % len(dvs)]
    ex = pool.defs_variant(dv)["style"] == "one_line_examples"
    blocks = [{"type": "task", "text": "Task line for this card."},
              {"type": "para", "text": "Card intro sentence."},
              {"type": "defs", "variant": dv, "heading": "Definitions",
               "entries": [{"name": "Label one", "text": "definition text one",
                            **({"examples": ["example one"]} if ex else {})},
                           {"name": "Label two", "text": "definition text two"}]},
              {"type": "section", "heading": "Rules", "blocks": [
                  {"type": "items", "items": ["Rule sentence one.", "Rule sentence two."]}]}]
    if i % 9 == 0:
        fts = [t for t in (f"FT{k:02d}" for k in range(1, 19)) if not pool.fewshot_template(t).get("needs_note")]
        blocks.append({"type": "fewshot", "template": fts[(i // 9) % len(fts)], "heading": None,
                       "examples": [{"case": "Case text one", "answer": "Label one"}]})
    return {"title": "Card alpha", "blocks": blocks}


def leaf_strings(doc: dict, values_only: bool = False) -> list[str]:
    """Every content string or number of a Doc, as text (for presence checks). values_only drops keys, column
    names and headings (JSON / YAML keys are rewritten by key case)."""
    out = []

    def key(k):
        if not values_only:
            val(k)

    def val(v):
        if v in (BLANK, OMIT, ABSENT) or v is None:
            return
        if isinstance(v, Choice):
            out.append(str(v.selected))
            return
        if isinstance(v, bool):
            return
        if isinstance(v, Decimal):
            out.append(format(v, "f"))
            return
        out.append(str(v))

    def blocks(bl):
        for b in bl:
            t = b["type"]
            if t == "para":
                val(b["text"])
            elif t in ("items", "steps"):
                for x in b["items"]:
                    val(x)
            elif t == "fields":
                for k, v in b["pairs"]:
                    if v is not OMIT:
                        key(k)
                        val(v)
            elif t == "table":
                for c in b["columns"]:
                    key(c)
                for r in b["rows"]:
                    for c in r:
                        val(c)
            elif t == "events":
                for e in b["events"]:
                    val(e["text"])
                    for k in ("actor", "level"):
                        if e.get(k):
                            val(e[k])
            elif t == "messages":
                for m in b["messages"]:
                    val(m["text"])
                    val(m["speaker"])
                    for k in ("to", "subject"):
                        if m.get(k):
                            val(m[k])
            elif t == "changes":
                for e in b["entries"]:
                    val(e["key"])
                    for k in ("value", "old", "new"):
                        if k in e:
                            val(e[k])
            elif t == "section":
                key(b["heading"])
                blocks(b["blocks"])
    for k, v in doc.get("meta") or []:
        val(v)
    blocks(doc.get("blocks", []))
    return out


# ----------------------------------------------------------------------------------------------------------------------
# v1.1: choice-row cards (review formats-1). Every definition variant, label form (plain / masked / swapped), term
# definitions, tables, notices, inverted frames and few-shot blocks meet every style on a choice row.

QUESTION, WORDING, NOTE = "Which label fits the case?", "Use the card.", "Answer with one option."
_NUM = ["one", "two", "three", "four"]


def _defs_variants():
    return [v for v in pool._load("defs_styles.jsonl") if v.get("kind") == "defs_variant" and v["style"] != "none"]


def defs_block(vid: str, names: list[str], *, examples: bool = True) -> dict:
    """A defs block of variant vid over the option names (placeholder sentences only)."""
    v = pool.defs_variant(vid)
    sty = v["style"]
    ents = []
    for k, n in enumerate(names):
        e = {"name": n, "text": f"definition text {_NUM[k % 4]} for slot {k + 1}"}
        if sty == "one_line_examples" and examples and k < 2:
            e["examples"] = [f"example {_NUM[k % 4]}"] + (["example extra"] if k == 0 else [])
        if sty == "rubric_table":
            e["cells"] = [f"note cell {k + 1}"]
            if v.get("ex_mode") == "after_table" and k == 0:
                e["examples"] = ["example one"]
        if sty == "decision_list":
            e["text"] = f"If condition {k + 1} holds, pick {n}."
            if not v.get("named"):
                e.pop("name")
        if sty == "short":
            e.pop("text")
        ents.append(e)
    blk = {"type": "defs", "variant": vid, "heading": "Definitions", "entries": ents}
    if sty == "rubric_table":
        blk["columns"] = ["Label", "Meaning", "Note"]
    return blk


def choice_case(i: int) -> dict:
    """A placeholder choice row: card IR, options, gold, question, wording, note."""
    from fmt1 import card as _card, labels as _labels
    dvs = _defs_variants()
    v = dvs[i % len(dvs)]
    form = ("plain", "masked", "swapped")[(i // len(dvs) + i) % 3]
    n = 3 + i % 3
    if form == "masked":
        names = _labels.masked_ids(f"MS{i % 20 + 1:02d}", n, f"fx{i}")
    elif form == "swapped":
        names = _labels.swapped_names("group" if i % 2 else "mixed", n, f"fx{i}",
                                      exclude=["Label", "Term", "Case", "Rule", "Note", "Slot"])
    else:
        names = [f"Label {_NUM[k]}" for k in range(n)] if n <= 4 else [f"Label {k + 1}" for k in range(n)]
    blocks = [{"type": "task", "text": "Task line for this card."},
              {"type": "para", "text": "Card intro sentence."}]
    if form != "plain" or i % 4 == 0:
        blocks.append({"type": "para", "text": pool.label_notices()[i % 8]["text"]})
    if i % 7 == 0:
        blocks.append({"type": "para", "text": _card.inverted_frame(f"IVC{i % 10 + 1:02d}")})
    blocks.append(defs_block(v["id"], names))
    if i % 3 == 0:
        blocks.append({"type": "defs", "variant": "DV01", "heading": "Terms",
                       "entries": [{"name": "Term alpha", "text": "term definition text"}]})
    if i % 5 == 0:
        blocks.append({"type": "table", "caption": "Reference table", "columns": ["Col one", "Col two"],
                       "rows": [["Cell a1", 17], ["Cell a2", "Cell b2"]]})
    blocks.append({"type": "section", "heading": "Rules", "blocks": [
        {"type": "items", "items": ["Rule sentence one.", "Rule sentence two."]}]})
    if i % 9 == 0:
        fts = [t for t in (f"FT{k:02d}" for k in range(1, 19)) if not pool.fewshot_template(t).get("needs_note")]
        blocks.append({"type": "fewshot", "template": fts[(i // 9) % len(fts)], "heading": None,
                       "examples": [{"case": "Case text one", "answer": names[0]}]})
    return {"card": {"title": "Card alpha", "blocks": blocks}, "options": list(names), "gold": names[i % n],
            "form": form, "variant": v["id"], "question": QUESTION, "wording": WORDING, "note": NOTE}
