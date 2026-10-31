"""Build-skeptic tests for the L-P pipeline (Sun 18 Oct): stamp verdicts fail closed, head rows get the full per-row checks, production refuses pending pins and a missing
deny-list, the opaque B-view row id. Nothing is written; nothing generated is executed."""
import pytest

from LP_COMMON import pipeline as pl
from LP_COMMON import util


@pytest.mark.parametrize("v,want", [
    ({"verdict": "clean", "hits": []}, "clean"),
    ({"verdict": "clean"}, "clean"),
    ({"verdict": "hit", "hits": [{"target": "t", "method": "m", "exempt": None}]}, "hit"),
    ({"verdict": "hit", "hits": [{"target": "t", "method": "m", "exempt": "scaffolding_only"}]}, "clean"),
    ({"verdict": "hit", "hits": [{"target": "t", "method": "m", "exempt": "freeze_collision"}]}, "clean"),
    ({"verdict": "hit", "hits": [{"target": "t", "method": "m", "exempt": "whatever"}]}, "hit"),
    ({"verdict": "hit", "hits": [{"target": "t", "method": "m", "exempt": "scaffolding_only"}, {"target": "u", "method": "m", "exempt": None}]}, "hit"),
    ({"verdict": "hit", "hits": []}, "error"),                 # a hit that names nothing is not a pass
    ({"verdict": "hit"}, "error"),
    ({"verdict": "timeout"}, "error"),                         # an unknown verdict word is not a pass
    ({"verdict": None}, "error"),
    ({}, "error"),
    (None, "error"),
    ("clean", "error"),
    ({"verdict": "clean", "hits": "x"}, "error"),
    ({"verdict": "clean", "hits": ["x"]}, "error"),
    ({"verdict": "clean", "hits": [{"target": "t", "exempt": None}]}, "hit"),
])
def test_verdict_class_fails_closed(v, want):
    assert pl.verdict_class(v) == want


class _OddHook(pl.StampHook):
    """Returns a verdict word the pipeline does not know for every row (a stamp-service bug or timeout)."""
    registry_sha = "0" * 64
    method_set_version = "odd"

    def __init__(self, v):
        self.v = v

    def stamp(self, items):
        return {it["row_id"]: dict(self.v, registry_sha=self.registry_sha, method_set_version="odd") for it in items}


@pytest.mark.parametrize("v", [{"verdict": "timeout"}, {"verdict": "hit", "hits": []}, {"verdict": ""}])
def test_unknown_or_empty_stamp_verdicts_drop_every_row(v):
    from T66 import checked
    rows, summary, log, _rep = checked.run(40, 3, _OddHook(v), standin=True)
    assert rows == [] and summary["kept"] == 0
    assert summary["dropped"].get("g13:stamp_error", 0) > 0 and not any(k.startswith("g13:") and k != "g13:stamp_error" for k in summary["dropped"])


def test_head_rows_get_the_full_answer_checks():
    """A corrupted CWE head row (a name off the allow-list, a leaked internal id) is dropped by the pipeline, not only by the options check."""
    from T65 import checked, generator as G, dryrun
    rows, _s, _l, _r = dryrun.dry_rows(60, seed=2)
    heads = [r for r in rows if r["head"] == "CWE"]
    assert heads
    ad = checked.adapter()
    ok, _n = pl.check_row(heads[0], ad)
    assert ok == []
    bad = dict(heads[0], names=dict(heads[0]["names"], tool=["prog.not_on_the_list"]))
    assert "names_off_allowlist" in pl.check_row(bad, ad)[0]
    leaked = dict(heads[0], rendered=dict(heads[0]["rendered"], text=heads[0]["rendered"]["text"] + "\nCWEC-22"))
    assert "internal_leak" in pl.check_row(leaked, ad)[0]


def test_run_checked_drops_a_head_row_that_fails_a_row_check():
    from T65 import checked, generator as G
    ad = checked.adapter()
    orig = ad.extra_rows

    def corrupt(ctx, kept):
        hs = orig(ctx, kept)
        for h in hs:
            h["rendered"] = dict(h["rendered"], text=h["rendered"]["text"] + "\nmail me at someone@example.org")      # PII in a head row
        return hs

    ad.extra_rows = corrupt
    plan = G.build_plan(total=60, seed=2)
    rows, summary, log, _r = pl.run_checked(ad, 60, 2, pl.TestDoubleHook(), standin=True, plan=plan)
    assert not [r for r in rows if r["head"] == "CWE"]
    assert any(k.startswith("answer:head_row_") for k in summary["dropped"])


def test_production_refuses_pending_pins_but_standin_does_not():
    guard = {"freeze_sha": "f", "registry_sha": "r", "allowlist_sha": "a"}
    row = {"manifest": {"pins": "PENDING_L0_IMAGE_RECORD"}}
    assert pl.production_pins_pending(row, guard) is True
    assert pl.production_pins_pending(row, None) is False
    assert pl.production_pins_pending({"manifest": {"pins": "img:sha256:abc"}}, guard) is False
    assert pl.production_pins_pending({"manifest": {}}, guard) is False
    assert "pins_pending" in pl.ANSWER_CODES


def test_production_refuses_a_run_without_the_shared_deny_list(monkeypatch):
    from T66 import checked, generator as G
    from LP_COMMON import sandbox_iface as S
    ad = checked.adapter(solver_b=lambda v: {"status": "ok", "label": "YES"})
    ctx = G.Ctx(seed=1, standin=True)
    ctx.deny_check = None
    env = {"OD_ROWGUARD_FREEZE_SHA": "f", "OD_ROWGUARD_REGISTRY_SHA": "r", "OD_ROWGUARD_ALLOWLIST_SHA": ad.allowlist.file_sha}
    with pytest.raises(pl.DenyListRequired):
        pl.run_checked(ad, 10, 1, pl.TestDoubleHook(), standin=False, ctx=ctx, environ=env)


def test_opaque_id_is_stable_and_hides_the_member_letter():
    a, b = util.opaque_id("T65-22-0001-a"), util.opaque_id("T65-22-0001-b")
    assert a == util.opaque_id("T65-22-0001-a") and a != b
    assert "-a" not in a[2:] or a.startswith("b-")
    assert not a.endswith("-a") and not b.endswith("-b")


def test_the_stamp_service_never_gets_more_than_500_rows_in_one_call():
    from T66 import checked

    class Counting(pl.TestDoubleHook):
        def __init__(self):
            super().__init__()
            self.sizes = []

        def stamp(self, items):
            self.sizes.append(len(items))
            return super().stamp(items)

    h = Counting()
    rows, summary, _l, _r = checked.run(900, 2, h, standin=True)
    assert rows and max(h.sizes) <= pl.BATCH_ROWS and sum(h.sizes) >= len(rows)
    assert summary["stamp_calls"] == len(h.sizes)


def test_stamp_in_batches_chunks_and_rejects_a_non_dict_answer():
    class Rec(pl.StampHook):
        def __init__(self):
            self.n = []

        def stamp(self, items):
            self.n.append(len(items))
            return {i["row_id"]: {"verdict": "clean", "hits": []} for i in items}

    r = Rec()
    out, calls = pl.stamp_in_batches(r, [{"row_id": str(i)} for i in range(1203)], 500)
    assert (r.n, calls, len(out)) == ([500, 500, 203], 3, 1203)

    class Bad(pl.StampHook):
        def stamp(self, items):
            return None

    with pytest.raises(pl.StampServiceRequired):
        pl.stamp_in_batches(Bad(), [{"row_id": "x"}], 500)


@pytest.mark.parametrize("pins,want", [("PENDING_L0_IMAGE_RECORD", True), ("image:sim", True), ("image:None", True), ("image:", True), ("", True), (None, True),
                                       ("image:od-sbx1@sha256:abc", False), ("n/a:no_toolchain", False), ("n/a:construction", False),
                                       ("image:fixture-image;export:abc", False)])
def test_production_pins_rule(pins, want):
    guard = {"freeze_sha": "f", "registry_sha": "r", "allowlist_sha": "a"}
    assert pl.production_pins_pending({"manifest": {"pins": pins}}, guard) is want


def test_family_rows_record_the_toolchain_provenance_they_have():
    from T63 import dryrun as d63
    from T65 import dryrun as d65
    from T66 import dryrun as d66
    r63 = d63.dry_rows(300, seed=2)[0]
    pins63 = {r["sub_block"]: r["manifest"]["pins"] for r in r63}
    assert pins63["NEAR"] == pins63["LIC"] == pins63["EX-A1"] == "n/a:no_toolchain"
    assert pins63["EX-B1"].startswith("image:fixture-image;export:")
    r65 = d65.dry_rows(120, seed=2)[0]
    dyn = [r for r in r65 if r["head"] == "VULN" and r["spec"]["cls"] in ("CWEC-22", "CWEC-78")]
    stat = [r for r in r65 if r["head"] == "VULN" and r["spec"]["cls"] in ("CWEC-295", "CWEC-327", "CWEC-377")]
    assert dyn and all(r["manifest"]["pins"] == "image:sim" for r in dyn)          # the stand-in executor: refused in production by production_pins_pending
    assert stat and all(r["manifest"]["pins"] == "n/a:static_pattern_engine" for r in stat)
    r66 = d66.dry_rows(160, seed=2)[0]
    by = {r["head"]: r["manifest"]["pins"] for r in r66}
    assert by["MERGE"] == "image:sim" and by["SEMVER"] == "image:sim" and by["MSG"] == "n/a:construction"
    guard = {"freeze_sha": "f", "registry_sha": "r", "allowlist_sha": "a"}
    assert all(pl.production_pins_pending(r, guard) for r in r66 if r["head"] in ("MERGE", "SEMVER"))


def test_builtin_deny_list_catches_real_packages_the_namespace_can_spell():
    from LP_COMMON.ns import Names, REAL_PACKAGE_DENY, _deny_union
    import re
    deny = _deny_union(None)
    for real in ("redis", "sinon", "nodemon", "tornado", "karma", "keras", "vite", "pino", "viper", "x-redis-y", "pre_vite.post"):
        assert deny(real), real
    syl = re.compile(r"^(?:[bdfgklmnprstvz][aeiou][lnrst]?)+$")
    spellable = [n for n in REAL_PACKAGE_DENY if syl.match(n)]
    assert len(spellable) >= 15                                    # the list is mostly names the generator could really produce
    nm = Names("TX", "deny-test")
    for i in range(300):
        assert not deny(nm.get("ns.package", "k%d" % i))


def test_schema_files_import_only_the_standard_library_and_agree_with_util_opaque_id():
    """Solver B may import the standard library and its family's schema.py only: the schema files must not pull in LP_COMMON (or any other lane code)."""
    import ast
    import importlib
    import os
    std = {"copy", "hashlib"}
    base = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    for fam in ("T63", "T65", "T66", "T67"):
        src = open(os.path.join(base, fam, "schema.py")).read()
        mods = set()
        for n in ast.walk(ast.parse(src)):
            if isinstance(n, ast.Import):
                mods |= {a.name.split(".")[0] for a in n.names}
            elif isinstance(n, ast.ImportFrom):
                mods.add((n.module or "").split(".")[0] or "." * n.level)
        assert mods <= std, (fam, mods)
        sch = importlib.import_module(fam + ".schema")
        assert sch.opaque_id("some-row-a") == util.opaque_id("some-row-a")
