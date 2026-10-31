"""Tests for the formats-1 pool and renderers. Run from the formats-1 folder:
    ../../../../.venv/bin/python -m pytest -q tests
Checks are written from the data specs (grammars, standard parsers), not from the renderer code.
"""
from __future__ import annotations

import collections
import csv
import datetime as dt
import hashlib
import io
import json
import re
import sys
from decimal import Decimal
from html.parser import HTMLParser
from pathlib import Path

import pytest
import yaml

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(HERE))
sys.path.insert(0, str(ROOT.parents[2]))  # lean/ for c_src.common

from fixtures import NOTE, QUESTION, TS, WORDING, card_for, choice_case, defs_block, doc_for, leaf_strings  # noqa: E402
from fmt1 import card, labels, pool, render  # noqa: E402
from fmt1.render import ABSENT, BLANK, OMIT, Choice, FormatError  # noqa: E402

ALL = pool.styles(held_out=None)
DATA = ROOT / "data"


def _unfence(text: str, st: dict) -> tuple[str | None, str]:
    """Split the outside title and the container body using the fence spec."""
    f = pool.fence(st["fence"])
    title = None
    body = text
    if st["container"] in ("csv", "log_lines", "diff", "key_value") and "\n\n" in text:
        head, rest = text.split("\n\n", 1)
        if "\n" not in head and (f["name"] != "none" or st["container"] != "key_value"):
            title, body = head, rest
    if f["name"] in ("backticks", "backticks_lang"):
        lines = body.split("\n")
        assert lines[0].startswith("```") and lines[-1] == "```", "fence"
        body = "\n".join(lines[1:-1])
    elif f["name"] == "indent4":
        lines = body.split("\n")
        assert all(ln == "" or ln.startswith("    ") for ln in lines), "indent fence"
        body = "\n".join(ln[4:] for ln in lines)
    return title, body


def _norm(v) -> str:
    return repr(v) if isinstance(v, float) else str(v)


def _allowed_values(doc, st) -> set:
    """Everything a container may print as a value or text node: the Doc's own strings and numbers, its titles and
    keys, formatted timestamps, and the skin's fixed vocabulary (column names it must name itself)."""
    al = set(leaf_strings(doc))
    al |= {_norm(float(x)) for x in al if re.fullmatch(r"\d+\.\d+", x)}
    if doc.get("title"):
        al.add(doc["title"])
    for k, v in doc.get("meta") or []:
        al |= {k, str(v)}
    for b in doc.get("blocks", []):
        for k in ("label", "caption"):
            if b.get(k):
                al.add(b[k])
        if b["type"] == "fields":
            al |= {str(v) for _, v in b["pairs"] if isinstance(v, (str, int, Decimal))}
    for t in TS:
        al |= {t.strftime("%Y-%m-%dT%H:%M:%S"), t.strftime("%Y-%m-%d %H:%M")}
    al |= {"3.25"}
    voc = pool.skin(st["skin"]).get("vocab") or {}
    al |= set(voc.values()) | {x.capitalize() for x in voc.values()}
    return al


def _rendered(i, st):
    doc = doc_for(st["skin"])
    out = card.render_row_text(st, doc=doc, question=QUESTION, qtype="noul", card=card_for(i), wording=WORDING,
                               note=NOTE)
    return doc, out


# ----------------------------------------------------------------------------------------------------------------------
# data integrity

def test_counts_and_holdout():
    assert len(ALL) == 400
    ho = [s for s in ALL if s["held_out"]]
    assert len(ho) == 50
    c = collections.Counter(s["container"] for s in ALL if not s["held_out"])
    assert set(c.values()) == {25} and len(c) == 14
    for s in ho:
        assert s["flags"]["uses_never_trained_element"]
    for s in ALL:
        if not s["held_out"]:
            assert not pool.skin(s["skin"])["held_out_only"]
            assert not pool.card_style(s["card_style"])["held_out_only"]
    assert len({(s["skin"], s["card_style"], s["register"], s["instr_position"], s["fence"]) for s in ALL}) == 400
    assert pool.styles() == [s for s in ALL if not s["held_out"]]


def test_every_container_has_f4_dev_styles():
    for cname in ("prose", "memo", "bullet_sop", "markdown_table", "csv", "html_snippet", "json", "yaml"):
        assert len(pool.styles(held_out=True, container=cname)) == 4


def test_ids_unique_and_sha():
    for f in sorted(DATA.glob("*.jsonl")):
        ids = set()
        for line in f.read_text().splitlines():
            o = json.loads(line)
            assert o["id"] not in ids
            ids.add(o["id"])
            body = {k: v for k, v in o.items() if k != "sha256"}
            assert hashlib.sha256(json.dumps(body, sort_keys=True, ensure_ascii=False).encode()).hexdigest() \
                == o["sha256"], (f.name, o["id"])


def test_build_is_deterministic(tmp_path):
    import importlib
    before = {f.name: f.read_bytes() for f in DATA.glob("*.jsonl")}
    bp = importlib.import_module("build_pool")
    bp.main()
    after = {f.name: f.read_bytes() for f in DATA.glob("*.jsonl")}
    assert before == after


# ----------------------------------------------------------------------------------------------------------------------
# lints on every chrome string (rendered text that this pool adds)

def _chrome_strings():
    out = []
    for r in pool._load("registers.jsonl"):
        for k in ("memo_title", "form_title_fmt", "email_greeting", "email_greeting_generic", "email_closing",
                  "q_prefix"):
            out.append(r[k])
        out += list(r["headings"].values())
    for s in pool._load("skins.jsonl"):
        for v in s["params"].values():
            if isinstance(v, str):
                out.append(v)
            elif isinstance(v, list):
                out += [x for x in v if isinstance(x, str)]
        if s.get("vocab"):
            out += list(s["vocab"].values())
    for c in pool._load("card_styles.jsonl"):
        out += [c["title"], c["heading"], c["item"], c["step"], c["def_fmt"]]
    out += [card.CHOICE_LINE, card.CHOICE_EX, card.CHOICE_EX_JOIN]
    for o in pool._load("defs_styles.jsonl"):
        out += [o[k] for k in ("fmt", "ex_fmt", "num_fmt", "cell_fmt") if o.get(k)]
    for t in pool._load("fewshot_templates.jsonl"):
        out += [x for x in (t["header"], t["item"], t.get("table_head")) if x]
    for o in pool._load("inverted.jsonl"):
        out.append(o.get("text") or o.get("fmt"))
    out += [m["pattern"] for m in pool._load("label_masks.jsonl")]
    out += [w["word"] for w in pool._load("swap_words.jsonl")]
    out += [n["text"] for n in pool._load("label_notices.jsonl")]
    return [s for s in out if s]


def test_chrome_has_no_negation_cues():
    from c_src.common.negcount import count
    bad = [s for s in _chrome_strings() if count(re.sub(r"\{[^}]*\}", "x", s)).k_all]
    assert not bad, bad


RECORD_WORDS = re.compile(r"\b(record\w*|recorded|unrecorded|log|logs|logged|logging|documented|registered|reported)\b"
                          r"|on file", re.I)


def test_chrome_has_no_record_status_words():
    bad = [s for s in _chrome_strings() if RECORD_WORDS.search(s)]
    assert not bad, bad


def test_chrome_and_words_are_no_markers():
    markers = {"not recorded", "unknown", "none", "no", "yes", "present", "absent", "true", "false", "pending",
               "partial", "maybe", "not listed", "not checked", "n/a", "tbd", "?", "-", "y", "n", "x"}
    for w in pool.swap_words():
        assert w["word"].lower() not in markers
    for s in _chrome_strings():
        if s.endswith(" "):  # a line prefix (bullet "- ", quote "> "), never a value
            continue
        assert s.strip().lower() not in markers, s


def test_swap_words_have_no_negation_or_stem_clash():
    from c_src.common.negcount import count
    words = [w["word"] for w in pool.swap_words()]
    assert all(count(w).k_all == 0 for w in words)
    assert len(words) == len(set(words))


# ----------------------------------------------------------------------------------------------------------------------
# every style renders; standard parsers read the containers back; grammars cover the lines

@pytest.mark.parametrize("i_st", list(enumerate(ALL)), ids=[s["id"] for s in ALL])
def test_style_renders_and_parses(i_st):
    i, st = i_st
    doc, out = _rendered(i, st)
    text = out["state"]
    sk = pool.skin(st["skin"])
    g = sk["grammar"]
    title, body = _unfence(text, st)
    # never a banned marker as a whole line or cell, never a YAML ~ null
    for ln in body.split("\n"):
        assert not render.is_banned_marker(ln) or ln.strip() == "" or re.fullmatch(r"[-=+|:\s]+", ln), ln
    leaves = leaf_strings(doc, values_only=g["parser"] in ("json", "jsonl", "yaml_safe_load"))
    if g["parser"] in ("json", "jsonl"):
        objs = [json.loads(x) for x in body.split("\n")] if g["parser"] == "jsonl" else [json.loads(body)]
        vals = []

        def walk(o):
            if isinstance(o, dict):
                for v in o.values():
                    walk(v)
            elif isinstance(o, list):
                for v in o:
                    walk(v)
            else:
                vals.append(o)
        for o in objs:
            walk(o)
        allowed = _allowed_values(doc, st)
        for v in vals:
            assert isinstance(v, bool) or _norm(v) in allowed, ("invented", v, st["id"])
        sv = collections.Counter(str(v) if not isinstance(v, float) else repr(v) for v in vals)
        for leaf in leaves:
            alt = repr(float(leaf)) if re.fullmatch(r"\d+\.\d+", leaf) else leaf
            assert sv[leaf] or sv[alt], (leaf, st["id"])
    elif g["parser"] == "yaml_safe_load":
        assert "~" not in re.findall(r":\s*(\S+)\s*$", body, flags=re.M)
        obj = yaml.safe_load(body)
        allowed = _allowed_values(doc, st)

        def walk_y(o):
            if isinstance(o, dict):
                for v in o.values():
                    walk_y(v)
            elif isinstance(o, list):
                for v in o:
                    walk_y(v)
            else:
                assert isinstance(o, bool) or _norm(o) in allowed, ("invented", o, st["id"])
        walk_y(obj)
        dumped = json.dumps(obj, default=str)
        for leaf in leaves:
            alt = repr(float(leaf)) if re.fullmatch(r"\d+\.\d+", leaf) else leaf
            assert leaf in dumped or alt in dumped, (leaf, st["id"])
    elif g["parser"] == "csv":
        rows = list(csv.reader(io.StringIO(body), delimiter=g["delimiter"]))
        flat = [c for r in rows for c in r]
        for leaf in leaves:
            assert leaf in flat, (leaf, st["id"])
        allowed = _allowed_values(doc, st)
        assert all(c in allowed for c in flat), st["id"]
        assert len({len(r) for r in rows}) == 1
        if g["quoting"] == "all":
            assert all(ln.startswith('"') for ln in body.split("\n"))
    elif g["parser"] == "fixed_width":
        rows = [re.split(g["col_sep"], ln) for ln in body.split("\n")]
        assert len({len(r) for r in rows}) == 1
        flat = [c for r in rows for c in r]
        for leaf in leaves:
            assert leaf in flat, (leaf, st["id"])
    elif g["parser"] == "html":
        class P(HTMLParser):
            def __init__(self):
                super().__init__()
                self.data, self.stack = [], []

            def handle_starttag(self, tag, attrs):
                self.stack.append(tag)

            def handle_endtag(self, tag):
                assert self.stack and self.stack[-1] == tag, (tag, self.stack)
                self.stack.pop()

            def handle_data(self, d):
                if d.strip():
                    self.data.append(d.strip())
        p = P()
        p.feed(body)
        p.close()
        assert not p.stack
        for leaf in leaves:
            assert leaf in p.data, (leaf, st["id"])
        allowed = _allowed_values(doc, st)
        assert all(d in allowed for d in p.data), [d for d in p.data if d not in allowed]
    else:
        low = text.lower()
        for leaf in leaves:
            ok = leaf.lower() in low or render.keyname(leaf, "snake") in low
            assert ok, (leaf, st["id"])
    if g["full_cover"] and g["lines"]:
        pats = [re.compile(x) for x in g["lines"].values()]
        for ln in body.split("\n"):
            if ln.strip():
                assert any(p.match(ln) for p in pats), (st["id"], ln)
    elif g["lines"]:
        # every structural pattern is well-formed and at least one structural line is present
        pats = [re.compile(x, re.M) for x in g["lines"].values()]
        assert any(p.search(body) for p in pats), st["id"]


def test_deterministic_render():
    for i, st in enumerate(ALL[:60]):
        assert _rendered(i, st)[1] == _rendered(i, st)[1]


# ----------------------------------------------------------------------------------------------------------------------
# content rules: never invent, never drop, never write a marker

def _st(skin_id, **kw):
    s = next(x for x in ALL if x["skin"] == skin_id)
    return {**s, **kw}


def test_text_containers_refuse_none_bool_empty_and_markers():
    st = _st("kv.colon", fence="FN-none")
    for bad in (None, True, "", "-", "N/A", "TBD", "?", "—", "--"):
        with pytest.raises(FormatError):
            render.render_state({"blocks": [{"type": "fields", "label": None, "pairs": [["Key", bad]]}]}, st)


def test_json_null_only_when_allowed():
    st = _st("json.pretty2", fence="FN-none")
    d = {"blocks": [{"type": "fields", "label": None, "pairs": [["Key", None], ["Other", 1]]}]}
    with pytest.raises(FormatError):
        render.render_state(d, st)
    assert json.loads(render.render_state(d, st, allow_null=True)) == {"key": None, "other": 1}


def test_yaml_quotes_coercible_words_and_never_tilde():
    st = _st("yaml.block", fence="FN-none")
    d = {"blocks": [{"type": "fields", "label": None,
                     "pairs": [["A", "yes"], ["B", "no"], ["C", "on"], ["D", "2031-05-06"], ["E", "12"],
                               ["F", "null"], ["G", "a: b"], ["H", "#x"], ["I", None]]}]}
    out = render.render_state(d, st, allow_null=True)
    back = yaml.safe_load(out)
    assert back == {"a": "yes", "b": "no", "c": "on", "d": "2031-05-06", "e": "12", "f": "null", "g": "a: b",
                    "h": "#x", "i": None}
    assert "~" not in out


def test_blank_and_omit_are_explicit():
    st = _st("kv.colon", fence="FN-none")
    out = render.render_state({"blocks": [{"type": "fields", "label": None,
                                           "pairs": [["Key one", BLANK], ["Key two", OMIT], ["Key three", 3]]}]}, st)
    assert out.split("\n") == ["Key one:", "Key three: 3"]
    st2 = _st("json.pretty2", fence="FN-none")
    with pytest.raises(FormatError):
        render.render_state({"blocks": [{"type": "fields", "label": None, "pairs": [["K", BLANK]]}]}, st2)


def test_no_silent_drop():
    with pytest.raises(FormatError):  # chat skin without times, doc with times
        render.render_state({"blocks": [{"type": "messages", "messages": [
            {"speaker": "Person A", "ts": TS[0], "text": "Hi there."}]}]}, _st("chat.plain"))
    with pytest.raises(FormatError):  # seconds on a minute format
        render.render_state({"blocks": [{"type": "messages", "messages": [
            {"speaker": "Person A", "ts": dt.datetime(2031, 1, 2, 3, 4, 5), "text": "Hi."}]}]},
            _st("chat.bracket_time"))
    with pytest.raises(FormatError):  # diff path on a skin that shows no path
        render.render_state({"blocks": [{"type": "changes", "target": "a.cfg",
                                         "entries": [{"key": "k", "old": 1, "new": 2}]}]}, _st("diff.word"))
    with pytest.raises(FormatError):  # container cannot show the block type
        render.render_state({"blocks": [{"type": "table", "caption": None, "columns": ["a"], "rows": [["b"]]}]},
                            _st("chat.plain"))


def test_numbers_are_never_reformatted():
    st = _st("csv.comma", fence="FN-none")
    out = render.render_state({"blocks": [{"type": "table", "caption": None, "columns": ["n"],
                                           "rows": [[1234567], [Decimal("1234.50")], ["0012"]]}]}, st)
    assert out.split("\n") == ["n", "1234567", "1234.50", "0012"]


def test_form_checkbox_and_plain_choice():
    d = {"blocks": [{"type": "fields", "label": None, "pairs": [["Pick", Choice("Two", ["One", "Two"])]]}]}
    assert render.render_state(d, _st("form.checkbox")) == "Pick: [ ] One  [x] Two"
    assert render.render_state(d, _st("form.colon")) == "Pick: Two"


# ----------------------------------------------------------------------------------------------------------------------
# cards, definitions, few-shot, inverted, instructions

def test_every_defs_variant_in_every_card_style():
    for cs in pool._load("card_styles.jsonl"):
        st = {**ALL[0], "card_style": cs["id"], "instr_position": "IP1"}
        for v in [o for o in pool._load("defs_styles.jsonl") if o.get("kind") == "defs_variant"]:
            if v["style"] == "none":
                continue
            ents = [{"name": "Label one", "text": "text one"}, {"name": "Label two", "text": "text two"}]
            blk = {"type": "defs", "variant": v["id"], "heading": "Definitions", "entries": ents}
            if v["style"] == "one_line_examples" or v.get("ex_mode") == "after_table":
                ents[0]["examples"] = ["example one", "example two"]
            if v["style"] == "rubric_table":
                blk["columns"] = ["Label", "Meaning", "Note"]
                for e in ents:
                    e["cells"] = ["note cell"]
            if v["style"] == "decision_list" and not v.get("named"):
                for e in ents:
                    e.pop("name")
            if v["style"] == "short":
                for e in ents:
                    e.pop("text")
            text = card.render_card({"title": "Card", "blocks": [blk]}, st)
            for e in ents:
                for k in ("name", "text"):
                    if e.get(k):
                        assert e[k] in text, (cs["id"], v["id"])
                for x in e.get("examples", []):
                    assert x in text


def test_fewshot_templates():
    st = ALL[0]
    for t in pool._load("fewshot_templates.jsonl"):
        ex = [{"case": "Case text one", "answer": "Label one"}, {"case": "Case text two", "answer": "Label two"}]
        if t.get("needs_note"):
            for e in ex:
                e["note"] = "Reason text."
        text = card.render_card({"title": None, "blocks": [{"type": "fewshot", "template": t["id"], "heading": None,
                                                           "examples": ex}]}, st)
        for e in ex:
            assert e["case"] in text and e["answer"] in text
    with pytest.raises(FormatError):
        card.render_card({"blocks": [{"type": "fewshot", "template": "FT01", "heading": None,
                                      "examples": [{"case": "c", "answer": "B"}]}]}, st)


def test_task_line_position():
    blocks = [{"type": "para", "text": "First."}, {"type": "task", "text": "Task line."},
              {"type": "para", "text": "Last."}]
    base = {**ALL[0], "card_style": "CS01"}
    head = card.render_card({"blocks": blocks}, {**base, "instr_position": "IP4"})
    tail = card.render_card({"blocks": blocks}, {**base, "instr_position": "IP5"})
    keep = card.render_card({"blocks": blocks}, {**base, "instr_position": "IP1"})
    assert head.startswith("Task line.") and tail.endswith("Task line.") and keep.split("\n\n")[1] == "Task line."


def test_instruction_positions():
    base = {**ALL[0], "register": "terse"}
    a = card.render_instructions({**base, "instr_position": "IP1"}, question="Q?", wording="W.", note="N.")
    b = card.render_instructions({**base, "instr_position": "IP3"}, question="Q?", wording="W.", note="N.")
    c = card.render_instructions({**base, "instr_position": "IP2"}, question="Q?", wording="W.", note="N.")
    assert a == "W.\n\nQ: Q?\n\nN." and b == "Q: Q?\n\nW.\n\nN." and c == "W. Q? N."


def test_inverted_helpers():
    qs = pool.inverted_all("inverted_question")
    assert len(qs) == 24 and all("{target}" in q["text"] for q in qs)
    assert card.inverted_question("IVQ01", "rule 4") == "Which case meets rule 4?"
    refs = card.case_refs("IVN01", 5, "seed")
    assert len(set(refs)) == 5 and all(r.startswith("Case ") for r in refs)
    assert refs != sorted(refs)


# ----------------------------------------------------------------------------------------------------------------------
# masked / swapped labels

def test_label_form_rates_and_independence():
    c = collections.Counter(labels.label_form("F1", f"card{i % 97}", f"row{i}") for i in range(60000))
    assert abs(c["masked"] / 60000 - 0.12) < 0.01 and abs(c["swapped"] / 60000 - 0.05) < 0.006
    c10 = collections.Counter(labels.label_form("F10", "c", f"r{i}", labels.F10_RATES) for i in range(20000))
    assert abs(c10["masked"] / 20000 - 0.40) < 0.02 and abs(c10["swapped"] / 20000 - 0.30) < 0.02


def test_masked_ids_rules():
    for m in pool._load("label_masks.jsonl"):
        for n in (2, 3, 7, 12):
            ids = labels.masked_ids(m["id"], n, f"k{n}")
            assert len(set(ids)) == n
            assert all(re.search(r"[2-9]", x) for x in ids)
            assert not any(re.search(r"[IO01]", re.sub(r"^[A-Za-z ]+ ", "", x)) for x in ids)
            if n >= 3:
                assert ids != sorted(ids) and ids != sorted(ids, reverse=True)
            assert ids == labels.masked_ids(m["id"], n, f"k{n}")
    big = labels.masked_ids("MS02", 60, "big")
    assert len(set(big)) == 60


def test_swapped_names_rules():
    nat = ["Low", "Medium", "High", "Severe"]
    for k in range(50):
        perm = labels.swapped_names("perm", 4, f"s{k}", natural_names=nat)
        assert sorted(perm) == sorted(nat) and all(a != b for a, b in zip(perm, nat))
        g = labels.swapped_names("group", 4, f"s{k}", order=[0, 1, 2, 3], exclude=["Level", "Case"])
        assert len(set(g)) == 4
        ws = {w["word"]: w for w in pool.swap_words()}
        ranks = [ws[x.lower()]["rank"] for x in g]
        if ws[g[0].lower()]["ordered"]:
            assert labels.monotone_ok(ranks, [0, 1, 2, 3])
        mx = labels.swapped_names("mixed", 6, f"s{k}")
        assert len({ws[x.lower()]["group"] for x in mx}) >= 2
        for i, a in enumerate(mx):
            for b in mx[i + 1:]:
                assert a.lower()[:4] != b.lower()[:4]


def test_rules_and_notices_present():
    assert [r["id"] for r in pool.label_rules()] == [f"LR{i:02d}" for i in range(1, 16)]
    assert len(pool.label_notices()) == 8
    rules = {r["id"]: r["rule"] for r in pool.label_rules()}
    for rid in ("LR04", "LR07", "LR14", "LR15"):
        assert "loader_check" in rules[rid], rid


# ----------------------------------------------------------------------------------------------------------------------
# v1.1 (review formats-1): what decoder_io shows. Choice rows print only "- {option}: {definition}" card lines; every
# other card block must reach the prompt through instructions. Checked with decoder_io itself (cygnet,
# schema_branch_mark) under a random option order, for every style x {choice, yes/no} and every card style x variant.

def _choice_row(i, st, **kw):
    c = choice_case(i)
    f = card.render_row_text(st, doc=doc_for(st["skin"]), question=c["question"], qtype="choice", card=c["card"],
                             options=c["options"], wording=c["wording"], note=c["note"], **kw)
    row = {"id": f"t-{st['id']}-{i}", "qtype": "choice", "options": c["options"], "gold": c["gold"], **f}
    ms = card.must_show(c["card"], question=c["question"], wording=c["wording"], note=c["note"])
    return c, row, ms


def test_decoder_io_is_the_pinned_readout():
    assert hashlib.sha256(card.DECODER_IO.read_bytes()).hexdigest() == card.DECODER_IO_SHA256
    assert hashlib.sha256(card.TRAIN_DECODER.read_bytes()).hexdigest() == card.TRAIN_DECODER_SHA256
    dio = card._dio()
    before = (dio.STYLE, dio.LAYOUT, list(dio.WIDE))
    c, row, ms = _choice_row(0, pool.styles()[0])
    card.loader_check(row, must_show=ms)
    assert (dio.STYLE, dio.LAYOUT, list(dio.WIDE)) == before  # the check restores decoder_io's globals


@pytest.mark.parametrize("i_st", list(enumerate(ALL)), ids=[s["id"] for s in ALL])
def test_every_style_choice_row_is_visible(i_st):
    i, st = i_st
    c, row, ms = _choice_row(i, st)
    res = card.loader_check(row, must_show=ms)
    assert res["ok"], (st["id"], c["variant"], c["form"], res["problems"])
    for ln in row["card"].split("\n") if row["card"] else []:  # the card field holds only option lines
        assert ln.startswith("- ") and ln[2:].split(": ", 1)[0] in c["options"], (st["id"], ln)
    route = pool.defs_variant(c["variant"])["choice_route"]
    assert (row["card"] is not None) == (route == "option_lines"), (st["id"], c["variant"])
    ip = pool.instr_position(st["instr_position"])
    if ip["card_task"] == "head":
        assert row["instructions"].startswith("Task line for this card.")
    if ip["card_task"] == "tail":
        assert row["instructions"].endswith("Task line for this card.")


@pytest.mark.parametrize("i_st", list(enumerate(ALL)), ids=[s["id"] for s in ALL])
def test_every_style_yesno_row_is_visible(i_st):
    i, st = i_st
    _, out = _rendered(i, st)
    row = {"id": f"t-{st['id']}-n", "qtype": "noul", "options": None, "gold": i % 2, **out}
    res = card.loader_check(row, must_show=card.must_show(card_for(i), question=QUESTION, wording=WORDING,
                                                           note=NOTE))
    assert res["ok"], (st["id"], res["problems"])


def test_every_card_style_x_variant_on_both_qtypes():
    base = pool.styles()[0]
    names = ["Label one", "Label two", "Label three"]
    n_ok = 0
    for cs in pool._load("card_styles.jsonl"):
        for k, v in enumerate(_ for _ in pool._load("defs_styles.jsonl") if _.get("kind") == "defs_variant"):
            if v["style"] == "none":
                continue
            st = {**base, "card_style": cs["id"], "instr_position": f"IP{k % 5 + 1}"}
            cd = {"title": "Card", "blocks": [{"type": "task", "text": "Task line."},
                                              {"type": "para", "text": "Rule paragraph sentence."},
                                              defs_block(v["id"], names)]}
            for qt in ("choice", "noul"):
                f = card.render_row_text(st, doc=doc_for(st["skin"]), question=QUESTION, qtype=qt, card=cd,
                                         options=names if qt == "choice" else None)
                row = {"id": f"p-{cs['id']}-{v['id']}-{qt}", "qtype": qt, "options": names if qt == "choice" else None,
                       "gold": "Label two" if qt == "choice" else 1, **f}
                res = card.loader_check(row, must_show=card.must_show(cd, question=QUESTION))
                assert res["ok"], (cs["id"], v["id"], qt, res["problems"])
                n_ok += 1
    assert n_ok == 12 * 26 * 2


def test_card_alone_is_hidden_on_choice_rows():
    """The v1.0 path (render_card text in a choice row's card field) hides card text; the check must catch it."""
    caught = 0
    for i, st in enumerate(ALL):
        c = choice_case(i)
        f = card.render_row_text(st, doc=doc_for(st["skin"]), question=QUESTION, qtype="noul", card=c["card"])
        row = {"id": f"old-{i}", "qtype": "choice", "options": c["options"], "gold": c["gold"], **f}
        res = card.loader_check(row, must_show=card.must_show(c["card"], question=QUESTION))
        caught += not res["ok"]
    assert caught == len(ALL)


def test_masked_and_swapped_choice_rows_every_scheme():
    st = pool.styles()[3]
    for m in pool._load("label_masks.jsonl"):
        for n in (2, 5, 12):
            ids = labels.masked_ids(m["id"], n, f"lc{n}")
            cd = {"blocks": [defs_block("DV12", ids), {"type": "para", "text": pool.label_notices()[0]["text"]}]}
            f, res = card.render_and_check(st, doc=doc_for(st["skin"]), question=QUESTION, qtype="choice",
                                           card=cd, options=ids, gold=ids[n - 1], row_id=f"m-{m['id']}-{n}")
            assert res["ok"] and f["card"].count("\n") == n - 1
    for k in range(30):
        ws = labels.swapped_names("mixed" if k % 2 else "group", 4, f"sw{k}", exclude=["Label", "Slot"])
        cd = {"blocks": [defs_block("DV01", ws)]}
        f, res = card.render_and_check(st, doc=doc_for(st["skin"]), question=QUESTION, qtype="choice", card=cd,
                                       options=ws, gold=ws[k % 4], row_id=f"s-{k}")
        for w in ws:  # each swapped word carries its own definition on its option line
            assert f"- {w}: definition text" in f["card"]


def test_wide_option_sets_map_back():
    st = pool.styles()[5]
    ids = labels.masked_ids("MS02", 60, "wide")
    cd = {"blocks": [defs_block("DV01", ids)]}
    dio = card._dio()
    before = list(dio.WIDE)
    f, res = card.render_and_check(st, doc=doc_for(st["skin"]), question=QUESTION, qtype="choice", card=cd,
                                   options=ids, gold=ids[47], row_id="wide")
    assert res["ok"] and res["n_options"] == 60 and list(dio.WIDE) == before


def test_render_choice_defs_form_and_refusals():
    t = card.render_choice_defs([{"name": "Category K7", "text": "def one", "examples": ["ex one", "ex two"]},
                                 {"name": "Tiny", "text": "def two"}], options=["Category K7", "Tiny", "Other"])
    assert t == "- Category K7: def one (e.g. ex one; ex two)\n- Tiny: def two"
    bad = [([{"name": "A: b", "text": "t"}], None),                          # ': ' in the name
           ([{"name": "X", "text": "t"}, {"name": "X", "text": "u"}], None),  # two lines for one option
           ([{"name": "Label one", "text": "t"}], ["Label two"]),             # names no option
           ([{"name": "label one", "text": "t"}], ["Label one"]),             # case differs
           ([{"name": "X", "text": "t", "examples": ["a", "b", "c"]}], None),
           ([{"name": "X", "text": "line\nbreak"}], None),
           ([{"name": "X", "text": "t", "cells": ["c"]}], None)]
    for ents, opts in bad:
        with pytest.raises(FormatError):
            card.render_choice_defs(ents, options=opts)
    with pytest.raises(FormatError):
        card.render_choice_defs([{"name": "X", "text": "t"}], options=["X", "Y"], require_all=True)


def test_row_entry_point_needs_qtype_and_options():
    st, doc = pool.styles()[0], doc_for(pool.styles()[0]["skin"])
    with pytest.raises(TypeError):
        card.render_row_text(st, doc=doc, question=QUESTION)  # qtype is required
    with pytest.raises(FormatError):
        card.render_row_text(st, doc=doc, question=QUESTION, qtype="yesno")
    with pytest.raises(FormatError):
        card.render_row_text(st, doc=doc, question=QUESTION, qtype="choice", card=card_for(1))
    names = ["Label one", "Label two"]
    near = {"blocks": [{"type": "defs", "variant": "DV01", "heading": None,
                        "entries": [{"name": "label one", "text": "t"}]}]}
    with pytest.raises(FormatError):
        card.render_row_text(st, doc=doc, question=QUESTION, qtype="choice", card=near, options=names)
    only_defs = {"blocks": [defs_block("DV03", names)]}
    f = card.render_row_text(st, doc=doc, question=QUESTION, qtype="choice", card=only_defs, options=names,
                             choice_card="refuse")
    assert f["card"].startswith("- Label one: ")
    with pytest.raises(FormatError):
        card.render_row_text(st, doc=doc, question=QUESTION, qtype="choice", card=card_for(1), options=names,
                             choice_card="refuse")


def test_yesno_card_never_glues_to_the_option():
    st, doc = {**pool.styles()[0], "card_style": "CS01"}, doc_for(pool.styles()[0]["skin"])
    cd = {"blocks": [defs_block("DV03", ["Yes", "No"])]}
    with pytest.raises(FormatError):
        card.render_row_text(st, doc=doc, question=QUESTION, qtype="noul", card=cd)
    row = {"id": "g", "qtype": "noul", "gold": 1, "state": "S.", "instructions": "Q?", "card": "- Yes: means met"}
    assert not card.loader_check(row)["ok"]


def test_loader_check_catches_bad_rows():
    base = {"id": "b", "qtype": "choice", "state": "S.", "instructions": "Q?", "card": None,
            "options": ["One", "Two", "Three"], "gold": "Two"}
    assert card.loader_check(base)["ok"]
    for change in ({"gold": "Four"}, {"options": ["One", "Two", "Two"]}, {"options": ["One", "Tw\no", "Two"]},
                   {"card": "Definitions:\n- One: x"}, {"card": "- Four: x"}, {"card": "- One: x\n- One: y"},
                   {"qtype": "yesno"}):
        assert not card.loader_check({**base, **change})["ok"], change
    assert not card.loader_check(base, must_show=["text that is nowhere"])["ok"]
    yn = {"id": "y", "qtype": "noul", "state": "S.", "instructions": "Q?", "card": None}
    assert card.loader_check({**yn, "gold": 1})["ok"] and card.loader_check({**yn, "gold": 0.25})["ok"]
    assert not card.loader_check({**yn, "gold": 2})["ok"]  # train_decoder.check_rows: noul gold in [0, 1]
    with pytest.raises(FormatError):
        card.loader_check({**base, "gold": "Four"}, raise_on_fail=True)
    for p in ([0, 1, 2], [2, 0, 1], [1, 2, 0]):
        r = card.loader_check(base, perm=p)
        assert r["ok"] and r["gold_letter"] == "ABC"[p.index(1)]


def test_choice_flags_on_every_card_style_and_variant():
    for c in pool._load("card_styles.jsonl"):
        assert c["choice_visible"] is True and c["on_choice_rows"]
    for v in pool._load("defs_styles.jsonl"):
        if v.get("kind") == "defs_variant":
            assert v["choice_visible"] is True
            assert v["choice_route"] in ("option_lines", "instructions", "none")
            assert (v["choice_route"] == "option_lines") == (v["style"] in ("one_line", "one_line_examples"))
    for f in pool.inverted_all("inverted_card_frame"):
        assert f["row_qtype"] == "choice"
    assert any(d["name"] == "none" for d in pool._load("defs_styles.jsonl") if d.get("kind") == "defs_style")


def test_held_out_guard():
    ho = pool.held_out_style_ids()
    assert len(ho) == 50
    for sid in ho:
        with pytest.raises(pool.HeldOutStyleError):
            pool.training_style(sid)
        assert pool.dev_style(sid)["held_out"]
    for s in pool.styles():
        assert pool.training_style(s["id"]) is s or pool.training_style(s["id"]) == s
        with pytest.raises(ValueError):
            pool.dev_style(s["id"])
    tr = pool.styles()[0]["id"]
    ok = [{"id": "r1", "meta": {"format_style": tr}}, {"id": "r2", "meta": {}}, {"id": "r3"}]
    assert pool.refuse_held_out(ok)["rows"] == 3
    with pytest.raises(pool.HeldOutStyleError):
        pool.refuse_held_out(ok + [{"id": "r4", "meta": {"format_style": sorted(ho)[0]}}])
    with pytest.raises(pool.HeldOutStyleError):
        pool.refuse_held_out([{"id": "r5", "meta": {"format_style": tr, "sampler": "S5"}}])
    with pytest.raises(pool.HeldOutStyleError):
        pool.refuse_held_out([{"id": "r6", "meta": {"format_style": "FS-9999"}}], strict_unknown=True)


def test_guard_cli_exit_codes():
    from fmt1 import guard
    tmpd = ROOT / "tmp"
    tmpd.mkdir(exist_ok=True)
    good, bad = tmpd / "_guard_ok.jsonl", tmpd / "_guard_bad.jsonl"
    good.write_text(json.dumps({"id": "a", "meta": {"format_style": pool.styles()[0]["id"]}}) + "\n")
    bad.write_text(json.dumps({"id": "b", "meta": {"format_style": sorted(pool.held_out_style_ids())[0]}}) + "\n")
    try:
        assert guard.main([str(good)]) == 0
        assert guard.main([str(good), str(bad)]) == 1
        assert guard.main([]) == 2
    finally:
        good.unlink()
        bad.unlink()
