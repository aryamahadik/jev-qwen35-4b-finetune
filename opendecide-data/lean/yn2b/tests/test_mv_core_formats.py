"""mv_core formats (SPEC 4.3): every renderer has a parse-back that recovers what was rendered."""
from __future__ import annotations

import json
import random
import sys
from datetime import datetime, timedelta, timezone
from pathlib import Path

import pytest

LEAN = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(LEAN / "golden_src" / "gen3"))
import mv_core as mv  # noqa: E402

T0 = datetime(2026, 3, 8, 6, 30, tzinfo=timezone.utc)


def test_json_is_jevbench_rendering():
    obj = {"policy": ["1. Refunds within 30 days."], "session": {"user": "Élodie", "n": 3}, "recent_calls": []}
    s = mv.render_json(obj)
    assert s == json.dumps(obj, indent=1, ensure_ascii=False)
    assert mv.is_canonical_json(s) and "Élodie" in s and '"recent_calls": []' in s
    assert not mv.is_canonical_json(json.dumps(obj))


@pytest.mark.parametrize("style", mv.TS_STYLES)
def test_timestamps_round_trip(style):
    for off in (0, 60, -300, 330):
        t = T0.astimezone(timezone(timedelta(minutes=off)))
        s = mv.fmt_ts(t, style)
        assert mv.parse_ts(s) == t and mv.parse_ts(s).utcoffset() == t.utcoffset()
    with pytest.raises(ValueError):
        mv.fmt_ts(T0.replace(tzinfo=None))
    with pytest.raises(ValueError):
        mv.fmt_ts(T0 + timedelta(seconds=5), "space")


def _entries():
    return [mv.Entry(T0 + timedelta(minutes=m), src, txt, ref) for m, src, txt, ref in [
        (5, "billing", "invoice issued for order W3319027", "e1"), (1, "orders", "order W3319027 created", None),
        (9, "billing", "payment posted: 40.00", "e3"), (7, "warehouse", "hold placed on 2 units", None),
        (12, "orders", "resend of e1 received (ignored)", "e5")]]


@pytest.mark.parametrize("order", mv.LOG_ORDERS)
@pytest.mark.parametrize("style", mv.TS_STYLES)
def test_log_orders_round_trip(order, style):
    es = _entries()
    txt = mv.render_log(es, order, rng=random.Random(3), ts_style=style, title="Audit log")
    back = mv.parse_log(txt)
    key = lambda e: (e.ts, e.source, e.text, e.ref)
    assert sorted(map(key, back)) == sorted(map(key, es))
    ts = [e.ts for e in back]
    if order == "chrono":
        assert ts == sorted(ts)
    if order == "newest":
        assert ts == sorted(ts, reverse=True)
    if order == "grouped":
        assert txt.count("== billing ==") == 1 and "[billing]" not in txt


def test_log_rejects_ambiguous_input():
    es = _entries()
    with pytest.raises(ValueError):
        mv.render_log(es + [mv.Entry(es[0].ts, "x", "same time")])
    with pytest.raises(ValueError):
        mv.render_log([mv.Entry(T0, "x", "two\nlines")])
    with pytest.raises(ValueError):
        mv.render_log(es, "shuffled")  # needs an rng


def test_email_and_chat_round_trip():
    msgs = [mv.Msg("Ana Velmor <ana@talvora.example>", "Please refund order 88.\n\nThanks,\nAna",
                   T0, "support@talvora.example", "Refund"),
            mv.Msg("support@talvora.example", "Done - refund 88 issued.", T0 + timedelta(hours=2))]
    for nf in (False, True):
        back = mv.parse_email_thread(mv.render_email_thread(msgs, newest_first=nf))
        assert [(m.sender, m.text, m.ts, m.to, m.subject) for m in (reversed(back) if nf else back)] == \
               [(m.sender, m.text, m.ts, m.to, m.subject) for m in msgs]
    chat = [mv.Msg("User", "move $40 to savings", T0), mv.Msg("Assistant", "Confirm: $40 to savings?", T0)]
    for st in (None, "iso"):
        back = mv.parse_chat(mv.render_chat(chat, ts_style=st))
        assert [(m.sender, m.text) for m in back] == [(m.sender, m.text) for m in chat]
    with pytest.raises(ValueError):
        mv.render_chat([mv.Msg("User", "a\nb")])


def test_kv_and_markdown_round_trip():
    obj = {"policy": ["1. Transfers over 500.00 need approval.", "2. Exception: own accounts."],
           "session": {"user id": "U-771", "role": "teller", "verified": True, "note": None}}
    kv = mv.render_kv(obj)
    p = mv.parse_kv(kv)
    assert p["policy.1"] == obj["policy"][0] and p["session.user id"] == "U-771" and p["session.verified"] == "true"
    assert p["session.note"] == "none"
    assert mv.state_keys(kv, "kv") == ("policy", "session")
    with pytest.raises(ValueError):
        mv.render_kv({"a:b": 1})
    secs = [("Policy", [("R1", "No wildcard deletes."), ("R2", "Staging only.")]), ("Session", {"role": "admin"}),
            ("Notes", ["first", "second"]), ("Summary", "Plain paragraph.\n\nSecond paragraph.")]
    md = mv.render_markdown(secs)
    back = dict(mv.parse_markdown(md))
    assert back["Policy"] == "R1. No wildcard deletes.\nR2. Staging only." and back["Session"] == "- role: admin"
    assert back["Summary"] == "Plain paragraph.\n\nSecond paragraph."
    assert mv.state_keys(md, "markdown") == ("Policy", "Session", "Notes", "Summary")


@pytest.mark.parametrize("layout", mv.TABLE_LAYOUTS)
def test_tables_through_tab_core(layout):
    heads = ["Lead", "Company size", "Budget", "Stage"]
    rows = [["Orvala Labs", "120", "$40,000 per year", "demo booked"], ["Drenmoor Freight", "35", "none", "new"],
            ["Keltaris Media", "1,200", "$3,000 per month", "contacted"]]
    txt = mv.render_grid(heads, rows, layout)
    h, b = mv.parse_grid(txt, layout)
    assert h == heads and b == rows
    with pytest.raises(ValueError):
        mv.render_grid(heads, rows + [rows[0]], layout)  # duplicate row names


def test_len_bins_and_paragraphs():
    assert [mv.len_bin(n) for n in (0, 1499, 1500, 5999, 6000, 12000, 50000)] == [0, 0, 1, 2, 3, 4, 4]
    assert mv.join_paragraphs(["a ", "", " b"]) == "a\n\nb"
