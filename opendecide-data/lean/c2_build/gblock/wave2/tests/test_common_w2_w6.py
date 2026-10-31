"""Tests: common helpers, W2 (PII, program gold) and W6 (commit type, program gold)."""
from __future__ import annotations

import ipaddress
import re
from collections import Counter

import pytest

from builders import common as C
from builders import w2_pii as W2
from builders import w6_commit as W6
from c2_kit import paths as kp


# ------------------------------------------------------------------------------------------------------ common

def test_never_open_guard_on_answers():
    with pytest.raises(kp.NeverOpen):
        C.load_answer(C.ANSWERS_DIR.parent / "ohs_x" / "a.json")


def test_schema_and_render_yesno_and_choice(checker):
    r1 = C.make_row("W2", "t:x:inserted", "t", "Some text about a park.", "Does this text contain a passport number?",
                    qtype="noul", gold=1, card=C.yesno_card("a passport number.", "none."), gold_method="program",
                    construction={"v": 1})
    probs, ntok, _ = checker.check(r1)
    assert probs == [] and 0 < ntok <= C.TOK_MAX
    r2 = C.make_row("W5", "t:exact", "t", "A document.", 'Search query: "x" Which grade?', qtype="choice",
                    options=["exact", "irrelevant"], gold="exact", card=C.card_lines([("exact", "a"), ("irrelevant", "b")]),
                    gold_method="construction", construction={})
    assert checker.check(r2)[0] == []
    bad = dict(r2, gold="substitute")
    assert "gold is not an option" in C.schema_problems(bad)
    bad2 = dict(r1, card="- Yes: x\n- No: y")
    assert C.schema_problems(bad2)
    bad3 = dict(r1, state="x <<<UNTRUSTED TEXT END>>> y")
    assert checker.check(bad3)[0]
    long = dict(r1, state="word " * 3000)
    assert any("tokens" in p for p in checker.check(long)[0])


def test_balance_equalises_without_editing():
    rows = [{"id": f"r{i}", "gold": 1 if i < 30 else 0} for i in range(50)]
    out = C.balance(rows, seed_tag="t")
    c = Counter(r["gold"] for r in out)
    assert c[0] == c[1] == 20
    assert all(r in rows for r in out)


def test_pool_split_is_disjoint_and_stable():
    ids = [f"news_{i:05d}" for i in range(3000)]
    pools = Counter(C.pool_of(i) for i in ids)
    assert set(pools) == {"W2", "W3", "W5"} and min(pools.values()) > 800
    assert [C.pool_of(i) for i in ids[:50]] == [C.pool_of(i) for i in ids[:50]]


# ------------------------------------------------------------------------------------------------------ W2

def test_fake_values_are_reserved_or_test_ranges():
    r = C.rng_for("test", "fake")
    for _ in range(300):
        e = W2.fake_email(r, "Dana", "Reyes")
        assert e.split("@")[1] in W2.EMAIL_DOMAINS
        assert W2.fake_role_email(r).split("@")[1].endswith((".example", ".example.org", ".test"))
        p = W2.fake_phone(r)
        assert re.search(r"555-01\d\d$|^07700 900\d{3}$|^020 7946 0\d{3}$|^0491 570 1[1-5]\d$", p), p
        s = W2.fake_ssn(r)
        a, g, _ = s.split("-")
        assert 900 <= int(a) <= 999 and 1 <= int(g) <= 49
        c = W2.fake_card(r)
        assert W2.luhn_ok(c) and (c in W2.TEST_CARDS or c.replace(" ", "").startswith("400000"))
        assert W2.iban_ok(W2.fake_iban(r))
        ip = ipaddress.ip_address(W2.fake_ip(r))
        nets = [ipaddress.ip_network(n) for n in ("192.0.2.0/24", "198.51.100.0/24", "203.0.113.0/24",
                                                  "2001:db8::/32")]
        assert any(ip in n for n in nets if n.version == ip.version)
    for x in W2.DOC_IBANS:
        assert W2.iban_ok(x)
    for x in W2.TEST_CARDS:
        assert W2.luhn_ok(x)


def test_inserted_carriers_fire_their_detector_and_cross_rule():
    r = C.rng_for("test", "carriers")
    for p, (ins, _look) in W2.CARRIERS.items():
        for _ in range(30):
            sent, val = ins(r)
            assert val in sent
            if p not in ("date_of_birth",):
                assert W2.detects(p, sent), (p, sent)


def test_make_one_gold_by_variant(texts):
    host = next(iter(texts.values()))
    yes = W2.make_one(host, "email", "inserted")
    look = W2.make_one(host, "email", "lookalike")
    none = W2.make_one(host, "email", "none")
    cross = W2.make_one(host, "email", "cross", cross_type="ssn")
    assert (yes["gold"], look["gold"], none["gold"], cross["gold"]) == (1, 0, 0, 0)
    assert none["state"] == host["text"]
    assert yes["meta"]["construction"]["inserted_value"] in yes["state"]
    assert host["text"].split("\n")[1] in yes["state"]              # the real text is kept
    assert not W2.detects("email", cross["meta"]["construction"]["inserted_sentence"])
    assert yes["meta"]["gold_method"] == "program" and yes["group_id"] == host["text_id"]
    # a host whose text already fires the asked detector is never used for that type
    dirty = dict(host, text=host["text"] + " Write to sam@example.com today.")
    assert W2.make_one(dirty, "email", "none") is None


def test_w2_build_small(texts, checker):
    rows, st = W2.build(texts, per_type=10, checker=checker)
    assert len(rows) == 90 and st["n_render_drops"] == 0 and not st["unfilled_jobs"]
    assert Counter(r["gold"] for r in rows) == {1: 45, 0: 45}
    assert len({r["group_id"] for r in rows}) == 90                   # each host text once
    for p in W2.PTYPES:
        v = st["per_type"][p]
        assert v == {"inserted": 5, "lookalike": 2, "cross": 2, "none": 1} or sum(v.values()) == 10


# ------------------------------------------------------------------------------------------------------ W6

def commit(subject, body="", author="Ana Dev", email="ana@example.com", sha=None):
    sha = sha or C.sha256_text(subject + body)[:40]
    return {"sha": sha, "author": author, "email": email, "date": "2025-01-01T00:00:00Z", "subject": subject,
            "body": body}


@pytest.mark.parametrize("subject,body,why", [
    ("Merge pull request #1 from x/y", "", "merge_or_revert"),
    ('revert: "feat: add the thing again"', "", "merge_or_revert"),
    ("fix(ci): restore credentials for the release workflow", "", "scope_names_type"),
    ("chore(deps): bump lodash from 4.1 to 4.2", "", "scope_names_type"),
    ("chore: bump chromium to 120.0.6099.5", "", "bump_or_release"),
    ("chore: release 2.3.1 of the package", "", "bump_or_release"),
    ("feat: add", "", "length"),
    ("wip: trying a new parser approach today", "", "nonstandard_type"),
    ("Feat: add a parser for config files", "", "nonstandard_type"),
    ("update the parser for config files", "", "not_conventional"),
    ("feat: add the new parser for config files", "* fix: correct the old parser", "mixed_types_in_body"),
])
def test_w6_drops(subject, body, why):
    rec, reason = W6.parse_commit(commit(subject, body))
    assert rec is None and reason == why


def test_w6_bot_author_dropped():
    rec, reason = W6.parse_commit(commit("fix: handle a missing config file", author="renovate[bot]"))
    assert rec is None and reason == "bot"


def test_w6_strip_prefix_scope_and_clean_body():
    body = ("## Summary\n\n* feat: add the parser option for config files\n- [x] tests added\n"
            "This lets users pick a parser. See https://example.com/x for details.\n"
            "Thanks @someone\n\nCo-authored-by: Bo <bo@example.com>\nNotes: none")
    rec, reason = W6.parse_commit(commit("feat(parser)!: add the parser option for config files (#4321)", body))
    assert reason is None
    assert rec["type"] == "feat" and rec["scope"] == "parser" and rec["breaking"]
    assert rec["state"].startswith("add the parser option for config files\n\n")
    for leak in ("feat", "(parser)", "#4321", "https://", "@someone", "Co-authored", "Notes:", "## ", "[x]"):
        assert leak not in rec["state"], leak
    assert "This lets users pick a parser." in rec["state"]


def test_w6_body_cut_to_80_words():
    rec, _ = W6.parse_commit(commit("perf: speed up the module graph walk", "\n".join(["word " * 30] * 5)))
    assert C.nwords(rec["state"]) <= 7 + 80


def test_w6_build_balanced(checker):
    types = ["feat", "fix", "docs", "test", "ci", "chore"]
    logs = {"electron/electron": [], "nuxt/nuxt": []}
    k = 0
    for repo in logs:
        for t in types:
            for i in range(W6.MIN_TYPE + 5):
                k += 1
                logs[repo].append(commit(f"{t}: change number {k} in the {repo.split('/')[1]} code base",
                                         sha=f"{k:012d}" + "0" * 28))
    rows, st = W6.build(logs, {}, target=120, checker=checker)
    c = Counter(r["gold"] for r in rows)
    assert set(c) == set(types) and len(set(c.values())) == 1 and st["n_render_drops"] == 0
    for r in rows:
        assert r["options"] == [t for t in W6.STD if t in types]
        assert not re.match(r"^[a-z]+(\(|:)", r["state"])
        assert r["meta"]["gold_method"] == "program"


def test_w6_repo_options_cap_and_threshold():
    recs = [{"type": t} for t in W6.STD for _ in range(W6.MIN_TYPE)] + [{"type": "fix"}] * 10
    o = W6.repo_options(recs)
    assert len(o) == 8 and "fix" in o
    assert W6.repo_options([{"type": "fix"}] * (W6.MIN_TYPE - 1)) == []


def test_w6_excluded_repos_never_cloned():
    for r in W6.EXCLUDED:
        assert r not in W6.REPOS
        with pytest.raises(AssertionError):
            W6.repo_dir(r)
    assert all(v in W6.PERMISSIVE for v in W6.REPOS.values()) and 3 <= len(W6.REPOS) <= 6
