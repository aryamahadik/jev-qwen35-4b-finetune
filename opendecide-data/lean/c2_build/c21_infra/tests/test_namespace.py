import re

import pytest

import namespace as ns_mod
from namespace import KINDS, NameSpace, NamespaceError, TRAINING_SALT

SEALED_TEST_SALT = "unit-test-only-salt-0123456789"


def test_deterministic_and_seed_sensitive():
    a = NameSpace("training", 7)
    b = NameSpace("training", 7)
    c = NameSpace("training", 8)
    for k in KINDS:
        assert a.name(k, "x1") == b.name(k, "x1")
        assert a.name(k, "x1") != a.name(k, "x2")
    assert any(a.name(k, "x1") != c.name(k, "x1") for k in KINDS)


def test_sides_are_unrelated():
    t = NameSpace("training", 7)
    s = NameSpace("sealed", 7, salt=SEALED_TEST_SALT)
    same = sum(t.name(k, "key%d" % i) == s.name(k, "key%d" % i) for k in KINDS for i in range(20))
    assert same == 0
    assert t.fingerprint() != s.fingerprint()


def test_sealed_salt_must_be_supplied(monkeypatch):
    monkeypatch.delenv(ns_mod.SEALED_ENV, raising=False)
    with pytest.raises(NamespaceError):
        NameSpace("sealed", 1)
    monkeypatch.setenv(ns_mod.SEALED_ENV, SEALED_TEST_SALT)
    assert NameSpace("sealed", 1).name("repo", "a")


def test_sealed_salt_rules():
    with pytest.raises(NamespaceError):
        NameSpace("sealed", 1, salt=TRAINING_SALT)
    with pytest.raises(NamespaceError):
        NameSpace("sealed", 1, salt="short")


def test_training_refuses_foreign_salt_and_bad_side():
    with pytest.raises(NamespaceError):
        NameSpace("training", 1, salt="some-other-salt-value")
    with pytest.raises(NamespaceError):
        NameSpace("eval", 1)


def test_salt_not_leaked_by_fingerprint_or_names():
    s = NameSpace("sealed", 1, salt=SEALED_TEST_SALT)
    blob = s.fingerprint() + " ".join(s.catalogue("repo", 20))
    assert SEALED_TEST_SALT not in blob


def test_formats():
    t = NameSpace("training", 3)
    assert re.fullmatch(r"[A-Z][a-z]+ [A-Z][a-z]+", t.name("company", "k"))
    assert re.fullmatch(r"[a-z]+-[a-z]+", t.name("repo", "k"))
    host = t.name("host", "k")
    assert host.rsplit(".", 1)[1] in ("example", "test", "invalid")
    assert re.fullmatch(r"[a-z]+-[a-z]+-[0-9a-f]{4}", t.name("bucket", "k"))
    assert re.fullmatch(r"[a-z]+_[a-z]+", t.name("tool", "k"))
    assert re.fullmatch(r"[a-z]+_[a-z]+", t.name("policy", "k"))
    assert re.fullmatch(r"[a-z]+-[0-9]{2}", t.name("runner", "k"))
    with pytest.raises(NamespaceError):
        t.name("planet", "k")


def test_catalogue_distinct_and_stable():
    t = NameSpace("training", 5)
    cat = t.catalogue("tool", 300)
    assert len(set(cat)) == 300
    assert cat == NameSpace("training", 5).catalogue("tool", 300)


def test_unique_never_collides_across_keys():
    t = NameSpace("training", 5)
    names = [t.unique("user", "u%d" % i) for i in range(2000)]
    assert len(set(names)) == 2000
    assert t.unique("user", "u5") == names[5]


def test_deny_check_forces_redraw():
    plain = NameSpace("training", 9)
    target = plain.name("repo", "k")
    guarded = NameSpace("training", 9, deny_check=lambda n: n == target)
    other = guarded.name("repo", "k")
    assert other != target and other == guarded.name("repo", "k")
    always = NameSpace("training", 9, deny_check=lambda n: True)
    with pytest.raises(NamespaceError):
        always.name("repo", "k", max_tries=5)


def test_cli_training(capsys):
    assert ns_mod.main(["--side", "training", "--seed", "1", "--kind", "repo", "--count", "3"]) == 0
    out = capsys.readouterr().out.strip().splitlines()
    assert out[0].startswith("# side=training") and len(out) == 4


def test_cli_sealed_needs_env(monkeypatch, capsys):
    monkeypatch.delenv(ns_mod.SEALED_ENV, raising=False)
    assert ns_mod.main(["--side", "sealed", "--seed", "1", "--kind", "repo"]) == 2
    monkeypatch.setenv(ns_mod.SEALED_ENV, SEALED_TEST_SALT)
    assert ns_mod.main(["--side", "sealed", "--seed", "1", "--kind", "repo", "--count", "2"]) == 0
    assert SEALED_TEST_SALT not in capsys.readouterr().out


def test_message_encoding_is_injective():
    # old "side|seed|kind|key|n" joined with '|': these two collided; the JSON encoding keeps them apart
    m1 = ns_mod._message("training", "a|tool", "policy", "k", 0)
    m2 = ns_mod._message("training", "a", "tool", "policy|k", 0)
    assert m1 != m2
    assert "|".join(["training", "a|tool", "policy", "k", "0"]) == "|".join(["training", "a", "tool", "policy|k", "0"])
    assert ns_mod._message("training", 7, "repo", "k", 0) == ns_mod._message("training", "7", "repo", "k", 0)
    assert NameSpace("training", "a|b").name("tool", "c") != NameSpace("training", "a").name("tool", "b|c")


# ================================================================ v2 kinds (formerly-null manifest slots)
import collections
import json
import os

from namespace import NEW_KINDS, KINDS_V1, RESERVED_NAMES, SLOT_TO_KIND, kind_for_slot

_L0 = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), "zed_orch", "c21", "l0")
_REAL = os.path.join(_L0, "NAMES_MANIFEST_V1.json")

_V1_GOLD = {"company": ["Gapopi Works", "Zurvovul Dynamics", "Pozenvun Works"],
            "repo": ["nivit-mugu", "rultu-sami", "reke-petvo"],
            "host": ["kirbe-20.paril.test", "bava-36.pisres.test", "timis-67.rinmu.test"],
            "service": ["mitfosar-api", "vepari-proxy", "satutmil-api"],
            "bucket": ["bibo-pulo-2d2c", "banos-munro-20e9", "zodas-zisnu-f5af"],
            "tool": ["bolkes_vulvo", "kike_renu", "zira_buvi"],
            "policy": ["puli_vefunri", "delon_dilasde", "zisdu_deldore"],
            "runner": ["fafilo-31", "bagolra-04", "felpanu-87"],
            "user": ["zolamo", "sezosti", "nepisi"]}


def test_v1_kinds_render_byte_identical_to_before_and_fingerprint_unchanged():
    t = NameSpace("training", 7)
    for k, want in _V1_GOLD.items():
        assert [t.name(k, "g%d" % i) for i in range(3)] == want, k
    assert NameSpace("training", 1).fingerprint() == "0844fd92219a"
    assert KINDS == KINDS_V1 + NEW_KINDS and len(set(KINDS)) == len(KINDS) == 34


def test_new_kinds_are_the_25_null_slots_named_after_the_slot_suffix():
    assert len(NEW_KINDS) == 25
    assert "noun_entity" in NEW_KINDS and "path_stem" in NEW_KINDS and "mcp_server" in NEW_KINDS


@pytest.mark.skipif(not os.path.isfile(_REAL), reason="frozen manifest not present")
def test_slot_table_matches_the_frozen_manifest_slot_map():
    m = json.load(open(_REAL))
    s2k = m["namespace"]["namespace_py"]["slot_to_kind"]
    assert len(s2k) == 34
    seen_null = 0
    for slot, kind in s2k.items():
        sid = slot.split(" ", 1)[0]
        assert kind_for_slot(slot) == SLOT_TO_KIND[sid]
        if kind is not None:
            assert SLOT_TO_KIND[sid] == kind              # the v1 mapping did not move
        else:
            seen_null += 1
            suffix = sid[len("ns."):].replace(".", "_")   # the manifest's null_kind_rule
            assert SLOT_TO_KIND[sid] == suffix and suffix in NEW_KINDS
    assert seen_null == 25 and set(SLOT_TO_KIND) == {s.split(" ", 1)[0] for s in s2k}
    assert set(SLOT_TO_KIND.values()) == set(KINDS) - {"runner"}   # runner is a display kind with no slot


def test_kind_for_slot_refuses_unknown_slot():
    with pytest.raises(NamespaceError):
        kind_for_slot("ns.nonexistent")
    with pytest.raises(NamespaceError):
        kind_for_slot("package")
    assert kind_for_slot("ns.noun.entity") == "noun_entity"
    assert kind_for_slot("ns.handle (user)") == "user"


@pytest.mark.parametrize("kind", NEW_KINDS)
def test_new_kind_deterministic_distinct_and_seed_salt_sensitive(kind):
    a, b = NameSpace("training", 11), NameSpace("training", 11)
    assert a.name(kind, "k1") == b.name(kind, "k1")
    assert a.name(kind, "k1") != a.name(kind, "k2")
    assert NameSpace("training", 12).name(kind, "k1") != a.name(kind, "k1")
    s = NameSpace("sealed", 11, salt=SEALED_TEST_SALT)
    assert sum(s.name(kind, "k%d" % i) == a.name(kind, "k%d" % i) for i in range(50)) == 0
    names = a.catalogue(kind, 400)
    assert len(set(names)) == 400
    assert names == NameSpace("training", 11).catalogue(kind, 400)


@pytest.mark.parametrize("kind", NEW_KINDS)
def test_new_kind_deny_check_redraws_and_gives_up(kind):
    plain = NameSpace("training", 9)
    target = plain.name(kind, "k")
    guarded = NameSpace("training", 9, deny_check=lambda n: n == target)
    other = guarded.name(kind, "k")
    assert other != target and other == guarded.name(kind, "k")
    seen = []
    always = NameSpace("training", 9, deny_check=lambda n: seen.append(n) or True)
    with pytest.raises(NamespaceError):
        always.name(kind, "k", max_tries=5)
    assert len(seen) == 5 and len(set(seen)) == 5           # five different draws were offered to the hook


def test_new_kinds_formats():
    t = NameSpace("training", 3)
    pats = {
        "package": r"[a-z]+-[a-z]+-(core|kit|lib|sdk|utils)",
        "path_stem": r"[a-z]+", "noun_entity": r"[a-z]+", "noun_module": r"[a-z]+", "noun_path_segment": r"[a-z]+",
        "variable": r"[a-z]+", "category": r"[a-z]+", "remote_name": r"[a-z]+",
        "branch": r"[a-z]+-[0-9]{3}",
        "envvar": r"[A-Z]+_[A-Z]+",
        "project": r"[a-z]+-(app|core|web|data|ops)",
        "endpoint": r"/v[123]/[a-z]+/[a-z]+",
        "mcp_server": r"[a-z]+-[a-z]+-mcp",
        "context": r"[a-z]+-[0-9a-f]{3}",
        "table": r"[a-z]+", "noun_field": r"[a-z]+", "column": r"[a-z]+",
        "database": r"[a-z]+_db",
        "prefix": r"[a-z]+/[a-z]+/",
        "object": r"[a-z]+-[0-9a-f]{6}",
        "brand": r"[A-Z][a-z]+",
        "noun_symbol": r"[a-z]+",
        "event": r"[a-z]+",
        "ticket": r"[A-Z]+[-_]?[0-9A-Z]{4,10}",
        "job_id": r"[a-z]+[-_]?[0-9a-z]{4,10}",
    }
    assert set(pats) == set(NEW_KINDS)
    for kind, pat in pats.items():
        for i in range(300):
            nm = t.name(kind, "f%d" % i)
            assert re.fullmatch(pat, nm), (kind, nm)
            assert nm.isascii() and nm == nm.strip() and " " not in nm and len(nm) <= 40


def _composed_parts(kind, n, upper):
    out = []
    for i in range(n):
        msg = ns_mod._message("training", "7", kind, "k%d" % i, 0)
        out.append(ns_mod._composed(ns_mod._Stream(TRAINING_SALT.encode(), msg), upper))
    return out


@pytest.mark.parametrize("kind,upper", [("ticket", True), ("job_id", False)])
def test_composed_ids_cover_at_least_12_formats_and_none_exceeds_12_percent(kind, upper):
    parts = _composed_parts(kind, 6000, upper)
    fmt = collections.Counter((sep, cs, n) for (_p, sep, cs, n, _b, _r) in parts)
    assert len(fmt) >= 12 and len(fmt) == 63                        # 3 separators x 3 charsets x lengths 4..10
    assert max(fmt.values()) / len(parts) <= 0.12
    assert {sep for (_p, sep, *_x) in parts} == {"-", "_", ""}
    assert {cs for (_p, _s, cs, *_x) in parts} == {"digits", "base32", "hex"}
    assert {n for (_p, _s, _c, n, *_x) in parts} == set(range(4, 11))
    allowed = {"digits": set("0123456789"), "base32": set(ns_mod._B32), "hex": set("0123456789ABCDEF")}
    for (p, sep, cs, n, body, rendered) in parts:
        assert len(body) == n and rendered == p + sep + body
        assert set(body.upper()) <= allowed[cs]
        assert (p.isupper() and body == body.upper()) if upper else (p.islower() and body == body.lower())
    # the prefix is a namespace stem, 1 or 2 syllables
    assert {len(p) for (p, *_x) in parts} <= set(range(2, 9))


def test_ticket_and_job_id_streams_unrelated_and_kind_is_in_the_message():
    t = NameSpace("training", 5)
    assert sum(t.name("ticket", "k%d" % i).lower() == t.name("job_id", "k%d" % i).lower() for i in range(200)) == 0


def test_barred_substrings_never_survive_for_any_kind(monkeypatch):
    # force the renderer to emit barred text for the first draws: the generator must redraw
    real = ns_mod._render
    calls = {"n": 0}

    def fake(kind, st):
        calls["n"] += 1
        if calls["n"] <= 3:
            return ["xxOHSxx", "a-SeAlEd-b", "ohs"][calls["n"] - 1]
        return real(kind, st)
    monkeypatch.setattr(ns_mod, "_render", fake)
    for kind in ("ticket", "repo", "company"):
        calls["n"] = 0
        nm = NameSpace("training", 1).name(kind, "k")
        assert "ohs" not in nm.lower() and "sealed" not in nm.lower() and calls["n"] == 4
    monkeypatch.undo()
    t = NameSpace("training", 21)
    for kind in KINDS:
        for i in range(400):
            nm = t.name(kind, "b%d" % i).lower()
            assert "ohs" not in nm and "sealed" not in nm


def test_base32_body_that_spells_ohs_is_redrawn_not_emitted():
    # the composed ids can reach the letters O-H-S in a base32 body; find one by search and show it is refused
    t = NameSpace("training", 1)
    found = None
    for i in range(400000):
        msg = ns_mod._message("training", "1", "ticket", "s%d" % i, 0)
        r = ns_mod._composed(ns_mod._Stream(TRAINING_SALT.encode(), msg), True)[5]
        if "OHS" in r:
            found = "s%d" % i
            break
    assert found is not None
    assert "ohs" not in t.name("ticket", found).lower()
    assert t.name("ticket", found) != ns_mod._composed(
        ns_mod._Stream(TRAINING_SALT.encode(), ns_mod._message("training", "1", "ticket", found, 0)), True)[5]


def test_reserved_names_refused_for_new_kinds_only(monkeypatch):
    real = ns_mod._render
    for kind, bad in (("envvar", "PATH"), ("remote_name", "origin"), ("branch", "main"), ("noun_field", "DATE"),
                      ("path_stem", "Etc")):
        calls = {"n": 0}

        def fake(k, st, calls=calls, bad=bad):
            calls["n"] += 1
            return bad if calls["n"] == 1 else real(k, st)
        monkeypatch.setattr(ns_mod, "_render", fake)
        nm = NameSpace("training", 1).name(kind, "k")
        assert nm.lower() != bad.lower() and calls["n"] == 2, kind
    # a v1 kind keeps its old behaviour: the reserved set does not apply to it
    monkeypatch.setattr(ns_mod, "_render", lambda k, st: "origin")
    assert NameSpace("training", 1).name("repo", "k") == "origin"
    monkeypatch.undo()
    assert {"path", "origin", "main", "etc", "prod"} <= RESERVED_NAMES
    # the fixed generic words used inside the formats are not themselves barred (or every package would be redrawn)
    fixed = set(ns_mod._PKG_WORDS) | set(ns_mod._PROJECT_WORDS) | {"mcp", "db"}
    assert not any(w in f for f in fixed for w in ns_mod.LABEL_LEAK_SUBSTRINGS)


def test_generated_new_kind_names_never_hit_the_reserved_set_or_carry_label_words():
    t = NameSpace("training", 31)
    for kind in NEW_KINDS:
        for i in range(1500):
            nm = t.name(kind, "r%d" % i)
            low = nm.lower()
            assert low not in RESERVED_NAMES
            assert not any(w in low for w in ns_mod.LABEL_LEAK_SUBSTRINGS), (kind, nm)


def test_label_leak_words_are_redrawn_for_new_kinds_only(monkeypatch):
    real = ns_mod._render
    for kind, bad in (("package", "devil-nura-lib"), ("envvar", "TOKENA_BAKI"), ("branch", "baska-123"),
                      ("ticket", "KA-ALLOW9"), ("noun_entity", "blockuma")):
        calls = {"n": 0}

        def fake(k, st, calls=calls, bad=bad):
            calls["n"] += 1
            return bad if calls["n"] == 1 else real(k, st)
        monkeypatch.setattr(ns_mod, "_render", fake)
        nm = NameSpace("training", 1).name(kind, "k")
        assert nm != bad and calls["n"] == 2, kind
    monkeypatch.setattr(ns_mod, "_render", lambda k, st: "devil")
    assert NameSpace("training", 1).name("repo", "k") == "devil"       # v1 kinds keep their old behaviour


def test_new_kind_cli_and_unknown_kind_error(capsys):
    assert ns_mod.main(["--side", "training", "--seed", "1", "--kind", "noun_entity", "--count", "3"]) == 0
    out = capsys.readouterr().out.strip().splitlines()
    assert len(out) == 4 and all(re.fullmatch(r"[a-z]+", x) for x in out[1:])
    with pytest.raises(NamespaceError):
        NameSpace("training", 1).name("noun.entity", "k")      # slot spelling is not a kind


def test_sealed_side_has_every_new_kind_and_stays_unrelated():
    s = NameSpace("sealed", 2, salt=SEALED_TEST_SALT)
    t = NameSpace("training", 2)
    for kind in NEW_KINDS:
        assert s.name(kind, "x") and s.name(kind, "x") != t.name(kind, "x")
