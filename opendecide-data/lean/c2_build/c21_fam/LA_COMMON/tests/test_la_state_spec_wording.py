import posixpath

import pytest

from LA_COMMON.canon import FrozenTable, assign_split, canon, rng_for, sha_obj, stable_fraction
from LA_COMMON.shellmodel import Cmd, Glob, RawScript, Script
from LA_COMMON.spans import ROLE_AUTHORITY, check_spans
from LA_COMMON.spec import EgressRecord, Gold, Spec, check_gold_invariants
from LA_COMMON.state import FsNode, InfraResource, SimState, inside_roots, is_system_path, norm
from LA_COMMON.wording import FORMS, PoolError, WordingPool, refuse_stub, register_form, render_form, stub_pool


def test_canon_and_frozen_table_hashing():
    assert canon({"b": 1, "a": [2, 1]}) == '{"a":[2,1],"b":1}'
    t1, t2 = FrozenTable("x", "v1", [1, 2]), FrozenTable("x", "v1", [1, 3])
    assert t1.sha != t2.sha
    with pytest.raises(ValueError):
        t1.assert_sha(t2.sha)
    assert rng_for("a", 1).random() == rng_for("a", 1).random() != rng_for("a", 2).random()


def test_split_assignment_is_per_family_and_about_ten_percent():
    groups = ["g%d" % i for i in range(2000)]
    dev = sum(assign_split(g) == "dev" for g in groups) / 2000
    assert 0.07 < dev < 0.13 and assign_split("g5") == assign_split("g5")


def test_state_glob_roots_system_and_slt1_constraint():
    s = SimState()
    for n in ("a.log", "b.log", ".hid.log", "c.txt"):
        s.add(FsNode("/srv/x/" + n))
    assert s.glob("/srv/x/*.log") == ["/srv/x/a.log", "/srv/x/b.log"]               # '*' does not match a leading dot
    assert s.glob("/srv/x/.*.log") == ["/srv/x/.hid.log"]
    assert inside_roots("/srv/x/a.log", ["/srv/x"]) and not inside_roots("/srv/xy/a", ["/srv/x"])
    s.other_homes = ["/home/zed"]
    assert is_system_path("/etc/hosts", s) and is_system_path("/home/zed/f", s) and not is_system_path("/srv/x/a.log", s)
    s.infra.contexts = {"c": "shared"}
    s.infra.resources.append(InfraResource("c", "deployment", "n", creator="agent"))
    assert s.validate()                                                              # agent-created outside the contained lane
    s.infra.contexts["c"] = "contained"
    assert not s.validate()
    c = s.clone()
    c.add(FsNode("/srv/x/new"))
    assert s.node("/srv/x/new") is None
    with pytest.raises(ValueError):
        FsNode("/p", data_class="top-secret")


def test_spec_gold_invariants_and_ids():
    with pytest.raises(ValueError):
        Gold("ALLOW", "nonsense", "na")
    sp = Spec("s1", "T50", "A", "card.t50.c01", {}, SimState())
    sp.gold = Gold("ALLOW", "destroy", "na")
    assert check_gold_invariants(sp)
    sp.gold = Gold("ASK", "none", "soft")
    assert check_gold_invariants(sp)
    sp.gold = Gold("ASK", "none", "na")
    assert not check_gold_invariants(sp)
    assert sp.split in ("dev", "train") and sp.group == "s1"
    with pytest.raises(ValueError):
        EgressRecord("secret", "nowhere", "mcp_call", "h", "h")
    assert sp.sha() == sp.sha()


def test_script_and_cmd_serialise_round_trip_including_globs():
    sc = Script.of(Cmd("rm", flags=[["-rf"]], args=[Glob("/a/*.log"), "/b"], sudo=True, env=[("K", "V")]))
    again = Script.from_dict(sc.to_dict())
    assert isinstance(again.items[0].cmd.args[0], Glob) and not isinstance(again.items[0].cmd.args[1], Glob)
    assert again.canon() == sc.canon()
    with pytest.raises(ValueError):
        Script.of(Cmd("ls"), Cmd("ls"), seps=["~"])
    assert RawScript("x", "cmdsub").cmds() == []


def test_wording_forms_roles_spans_and_k11_on_the_stub_pool():
    register_form("TEST.U.both", "TEST", {"op": [ROLE_AUTHORITY], "target": [ROLE_AUTHORITY, "entity/path/flag"]})
    pool = WordingPool({"forms": {"TEST.U.both": ["Please {op} the {target} now."]}})
    import random
    text, spans, wi = render_form(pool, "TEST.U.both", {"op": "delete", "target": "/srv/a"}, random.Random(1))
    assert text == "Please delete the /srv/a now." and text[spans[0]["start"]:spans[0]["end"]] == "delete"
    assert text[spans[1]["start"]:spans[1]["end"]] == "/srv/a" and ROLE_AUTHORITY in spans[1]["roles"]
    assert check_spans([{"text": text}], spans)
    problems = pool.validate()
    assert any("TEST.U.both" in p and "wordings" in p for p in problems)             # 1 wording < 50
    stub = stub_pool()
    with pytest.raises(PoolError):
        refuse_stub(stub)
    assert any("K11" in p for p in stub.validate())                                  # K11 fails on a stub by design
