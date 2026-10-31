"""Tests for c2_kit.paths (never-open, A38 guard, writers) and c2_kit.slots (typed slots). In memory only."""
from __future__ import annotations

import datetime as dt
import random
import zoneinfo

import pytest

from c2_kit import paths as P
from c2_kit import slots as S

NO_A38 = "# PREREG\n> **Ruling A37 (13 Oct 2026): C2 ...**\n"
WITH_A38 = NO_A38 + "\n> **Ruling A38 (14 Oct 2026): OHS-4 frozen.**\n"


# ------------------------------------------------------------------------------------------------ never-open

@pytest.mark.parametrize("p,why", [
    (P.LEAN / "ohs4_sealed" / "suite.jsonl", "ohs"),
    (P.LEAN / "data" / "ohs3_parts" / "x.jsonl", "ohs"),
    (P.LEAN / "data" / "OHS3.jsonl", "ohs"),
    (P.LEAN / "sealed_nd" / "a.json", "sealed_nd"),
    (P.LEAN / "c_spec" / "sealed_brief" / "b.md", "sealed_brief"),
    (P.LEAN / "c_build" / "preread" / "x", "preread"),
    (P.DATA_ROOT / "bench" / "external_quarantine" / "x", "external_quarantine"),
    (P.DATA_ROOT / "bench" / "longbench_v2" / "x", "longbench_v2"),
    (P.DATA_ROOT / "bench" / "decision_index" / "x", "decision_index"),
    (P.LEAN / "teach0" / "jev_U" / "a.json", "jev"),
    (P.LEAN / "speed" / "jev_latency.json", "jev"),
    ("~/.claude/projects/foo/bar.jsonl", "claude_projects"),
    ("/private/tmp/claude-501/x/y", "claude_session_tmp"),
    ("/tmp/claude-501/x", "claude_session_tmp"),
])
def test_never_open_refuses(p, why):
    assert P.never_open(p) == why
    with pytest.raises(P.NeverOpen):
        P.check_path(p)


@pytest.mark.parametrize("p", [P.LEAN / "c2_build" / "c2_kit" / "slots.py", P.REPO_ROOT, P.LEAN / "PREREG_FINAL.md",
                               P.LEAN / "c_src" / "common" / "negcount.py", "/data/prod/reports"])
def test_never_open_allows(p):
    assert P.never_open(p) is None


def test_a38_guard_reads_the_freeze_block():
    assert not P.a38_frozen(NO_A38)
    assert P.a38_frozen(WITH_A38)
    with pytest.raises(P.DataBeforeFreeze):
        P.require_a38(NO_A38)
    P.require_a38(WITH_A38)
    assert isinstance(P.a38_frozen(), bool)          # the real PREREG_FINAL.md is readable


def test_writers_refuse_before_a38_and_write_nothing():
    target = P.LEAN / "data" / "c2_parts" / "never_written.jsonl"
    with pytest.raises(P.DataBeforeFreeze):
        P.write_jsonl(target, [{"id": "x"}], prereg_text=NO_A38)
    with pytest.raises(P.DataBeforeFreeze):
        P.write_files(P.LEAN / "data" / "c2_parts", {"a.json": "{}"}, prereg_text=NO_A38)
    assert not target.exists()


def test_writers_refuse_never_open_and_outside_lean_even_after_a38():
    with pytest.raises(P.NeverOpen):
        P.write_text(P.LEAN / "ohs4_sealed" / "x.txt", "x", prereg_text=WITH_A38)
    with pytest.raises(PermissionError):
        P.write_text("/usr/local/x.txt", "x", prereg_text=WITH_A38)
    with pytest.raises(ValueError):
        P.write_jsonl(P.LEAN / "data" / "c2_parts" / "x.jsonl", [{"id": "a", "_spans": []}], prereg_text=WITH_A38)
    with pytest.raises(PermissionError):
        P.write_files(P.LEAN / "data" / "c2_parts", {"../escape.json": "{}"}, prereg_text=WITH_A38)


def test_no_c2_data_exists_before_a38():
    if not P.a38_frozen():
        assert not P.C2_PARTS.exists()


# ------------------------------------------------------------------------------------------------ slots

def _rand_slots(rng):
    out = []
    for _ in range(40):
        d = dt.date(2024, 1, 1) + dt.timedelta(days=rng.randrange(0, 1500))
        out.append(S.date_slot(d))
        off = rng.randrange(-48, 57) * 15
        tz = dt.timezone(dt.timedelta(minutes=off))
        t = dt.datetime(2026, rng.randrange(1, 13), rng.randrange(1, 29), rng.randrange(24), rng.randrange(60),
                        rng.choice((0, 0, rng.randrange(60))), tzinfo=tz)
        out.append(S.datetime_slot(t))
        out.append(S.cents_slot(rng.choice((0, 1, 99, 100, 1000, 123456, 99999999, -2550, rng.randrange(10 ** 7)))))
        out.append(S.cents_slot(rng.randrange(10 ** 6), currency="EUR", symbol="€"))
        out.append(S.count_slot(rng.randrange(0, 2000), rng.choice((None, ("day", "days"), ("record", "records")))))
        out.append(S.count_slot(rng.randrange(0, 25), ("hour", "hours")))
    out += [S.category_slot("prod", {"prod": ["production", "prod"], "stage": "staging"}),
            S.id_slot("INV-20419"), S.id_slot("a"), S.glob_slot("ns.*"), S.url_slot("https://shop.example/a/b?x=1"),
            S.url_slot("http://api.test"), S.name_slot("Dana Okafor")]
    return out


def test_every_form_round_trips():
    rng = random.Random(7)
    for s in _rand_slots(rng):
        assert S.roundtrip_ok(s), (s, [S.render(s, f) for f in S.forms(s)])
        for f in S.forms(s):
            txt = S.render(s, f)
            assert S.parse(s.kind, txt, s.params) == s.value         # form unknown: still exactly one reading


def test_form_examples():
    assert S.render(S.date_slot(dt.date(2026, 3, 5)), "wdmy") == "Thursday, 5 March 2026"
    assert S.render(S.date_slot(dt.date(2026, 3, 5)), "mdy") == "March 5, 2026"
    t = dt.datetime(2026, 3, 5, 14, 5, tzinfo=dt.timezone(dt.timedelta(hours=-5, minutes=-30)))
    assert S.render(S.datetime_slot(t), "iso") == "2026-03-05T14:05:00-05:30"
    assert S.render(S.datetime_slot(t), "text") == "5 March 2026, 14:05 (UTC-05:30)"
    assert S.render(S.datetime_slot(t), "log") == "2026-03-05 14:05:00 -0530"
    assert S.render(S.cents_slot(123450), "code") == "1,234.50 USD"
    assert S.render(S.cents_slot(-5), "symbol") == "-$0.05"
    assert S.render(S.count_slot(1, ("day", "days"))) == "1 day"
    assert S.render(S.count_slot(8, ("day", "days")), "adj_words") == "eight-day"
    assert S.parse("cents", "$1,200", S.cents_slot(0).params) == 120000


def test_form_availability():
    assert "iso_z" not in S.forms(S.datetime_slot(dt.datetime(2026, 1, 1, tzinfo=dt.timezone(dt.timedelta(hours=1)))))
    assert "text" not in S.forms(S.datetime_slot(dt.datetime(2026, 1, 1, 0, 0, 5, tzinfo=dt.timezone.utc)))
    assert "whole" not in S.forms(S.cents_slot(150))
    assert "words" not in S.forms(S.count_slot(21))
    assert "adj" not in S.forms(S.count_slot(3))
    assert set(S.free_forms(S.cents_slot(100))) == {"symbol", "code", "whole"}
    assert "adj" not in S.free_forms(S.count_slot(3, ("day", "days")))


@pytest.mark.parametrize("bad", [
    lambda: S.cents_slot(12.5), lambda: S.cents_slot(True), lambda: S.count_slot(-1),
    lambda: S.datetime_slot(dt.datetime(2026, 1, 1)),
    lambda: S.datetime_slot(dt.datetime(2026, 1, 1, tzinfo=zoneinfo.ZoneInfo("Europe/Berlin"))),
    lambda: S.datetime_slot(dt.datetime(2026, 1, 1, tzinfo=dt.timezone(dt.timedelta(minutes=7)))),
    lambda: S.datetime_slot(dt.datetime(2026, 1, 1, tzinfo=dt.timezone(dt.timedelta(hours=15)))),
    lambda: S.url_slot("https://www.realbank.com/login"), lambda: S.url_slot("ftp://x.example/a"),
    lambda: S.name_slot("Nobody Holdings"), lambda: S.name_slot("Unit 7"), lambda: S.name_slot("A{B}"),
    lambda: S.id_slot("INV 204"), lambda: S.id_slot("-x-"), lambda: S.glob_slot("a b"),
    lambda: S.category_slot("x", {"a": ["one"], "b": ["one"]}), lambda: S.category_slot("z", {"a": "one"}),
])
def test_invalid_values_refused(bad):
    with pytest.raises(S.SlotError):
        bad()


def test_parse_refuses_bad_text():
    with pytest.raises(S.SlotParseError):
        S.parse("date", "Friday, 5 March 2026")                 # 5 March 2026 is a Thursday
    with pytest.raises(S.SlotParseError):
        S.parse("date", "2026-02-30")
    with pytest.raises(S.SlotParseError):
        S.parse("count", "3 day", (("unit", ("day", "days")),))  # unit does not agree
    with pytest.raises(S.SlotParseError):
        S.parse("cents", "1234.5", S.cents_slot(0).params)       # two decimals always
    with pytest.raises(S.SlotParseError):
        S.parse("datetime", "2026-03-05T14:05:00+02:07")         # not a quarter hour


def test_canonical_keeps_the_offset():
    a = S.datetime_slot(dt.datetime(2026, 3, 5, 14, 5, tzinfo=dt.timezone(dt.timedelta(hours=2))))
    b = S.datetime_slot(dt.datetime(2026, 3, 5, 12, 5, tzinfo=dt.timezone.utc))
    assert a.value == b.value                       # the same instant
    assert S.canonical(a) != S.canonical(b)         # but different facts on the page
