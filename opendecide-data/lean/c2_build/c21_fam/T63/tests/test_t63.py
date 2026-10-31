"""T63 CPU tests: relation registry, solver A rule paths (hand-built specs), plan quotas, renderers and round trips, the check-at-generation
pipeline (GV5 group retirement, stamp / solver B / guard requirements), clean-room scans. No generated code is executed; nothing is written."""
import collections
import copy
import os
import re

import pytest

from LP_COMMON import pipeline as pl
from LP_COMMON.names_guard import default_guard
from T63 import checked, config as C, dryrun, exists, generator as G, gates, lic, near, near_build as NB, render as R, rows as ROWS, schema

FAMDIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


@pytest.fixture(scope="module")
def dry():
    rows, summary, log, report = dryrun.dry_rows(600, seed=7)
    return rows, summary, log, report


# ---------------------------------------------------------------------------------------------------------- relations
@pytest.mark.parametrize("p,q,rel", [
    ("abc-def-core", "abc-df-core", "NM-T2"), ("abc-df-core", "abc-def-core", "NM-T1"), ("abc-dsf-core", "abc-def-core", "NM-T3"),
    ("abc-edf-core", "abc-def-core", "NM-T4"), ("abc_def_core", "abc-def-core", "NM-T5"), ("abcdef-core", "abc-def-core", "NM-T5"),
    ("abc-rnem-core", "abc-mem-core", "NM-T6"), ("abc-1em-core", "abc-lem-core", "NM-T6"), ("scope/abc-def-core", "abc-def-core", "NM-T7"),
    ("abc-def-core", "scope/abc-def-core", "NM-T7")])
def test_relations_positive(p, q, rel):
    assert rel in near.near_relations(p, q)


@pytest.mark.parametrize("p,q", [("abc-def-core", "abc-def-core"), ("abc-def-core", "xyz-uvw-kit"), ("abc-def-cxxe", "abc-def-core"),
                                 ("abc-def-core", "abc-dxf-xore")])
def test_relations_negative(p, q):
    assert not near.near_relations(p, q)


def test_mutate_produces_the_requested_relation_for_every_op():
    from LP_COMMON import util
    for op in ("NM-T1", "NM-T2", "NM-T3", "NM-T4", "NM-T5", "NM-T6", "NM-T7"):
        got = 0
        for k in range(30):
            rng = util.rng_for("mut", op, k)
            name = "kolu-marnel-core" if k % 2 else "tomi-barlen-kit"
            m = NB.mutate(name, op, rng, scope_factory=lambda: "acme")
            if m is not None:
                assert op in near.near_relations(m, name) and NB.valid_name(m)
                got += 1
        assert got > 0, op


def test_keyboard_adjacency_symmetric():
    for a, nbs in near.KEYBOARD.items():
        for b in nbs:
            assert a in near.KEYBOARD[b]


# --------------------------------------------------------------------------------------- solver A: hand-built specs
def _spec(entries, query, card=None, regs=None):
    regs = regs or [{"id": r, "host": "h%s.example" % r, "eco": "pip"} for r in ("R1", "R2", "R3")]
    card = card or {"display": "c", "reserved": [], "internal_registry": None, "resolve_order": ["R1", "R2", "R3"], "own_org": "ownorg"}
    return {"head": "NEAR", "registries": regs, "entries": entries, "card": card, "query": query}


def E(name, reg, pub, age, dl, fork=None):
    return NB.entry(name, reg, pub, age, dl, fork)


Q0 = {"name": "abc-df-core", "registry": "R1", "explicit": False}


def test_lookalike_yes_and_each_negating_condition():
    base = [E("abc-def-core", "R1", "alice", "A3", "D2"), E("abc-df-core", "R1", "bob", "A1", "D0")]
    assert near.gold_label(_spec(base, Q0)) == "YES"
    same_pub = [base[0], E("abc-df-core", "R1", "alice", "A1", "D0")]
    assert near.gold_label(_spec(same_pub, Q0)) == "NO"                      # same publisher = same-org edge
    forked = [base[0], E("abc-df-core", "R1", "bob", "A1", "D0", fork="abc-def-core")]
    assert near.gold_label(_spec(forked, Q0)) == "NO"
    forked2 = [E("abc-def-core", "R1", "alice", "A3", "D2", fork="abc-df-core"), base[1]]
    assert near.gold_label(_spec(forked2, Q0)) == "NO"                       # edge in the other direction
    same_class = [E("abc-def-core", "R1", "alice", "A2", "D2"), E("abc-df-core", "R1", "bob", "A2", "D1")]
    assert near.gold_label(_spec(same_class, Q0)) == "NO"                    # same class is NOT newer (B7)
    not_established = [E("abc-def-core", "R1", "alice", "A3", "D1"), base[1]]
    assert near.gold_label(_spec(not_established, Q0)) == "NO"               # downloads not high
    young_orig = [E("abc-def-core", "R1", "alice", "A1", "D2"), base[1]]
    assert near.gold_label(_spec(young_orig, Q0)) == "NO"                    # age class below A2
    other_reg = [E("abc-def-core", "R2", "alice", "A3", "D2"), base[1]]
    assert near.gold_label(_spec(other_reg, Q0)) == "NO"                     # Q must be in the query's registry (assumption, README)
    unrelated = [E("zzz-yyy-kit", "R1", "alice", "A3", "D2"), base[1]]
    assert near.gold_label(_spec(unrelated, Q0)) == "NO"


def _t8(**kw):
    card = {"display": "c", "reserved": ["pkg-name-lib"], "internal_registry": "R1", "resolve_order": ["R2", "R1", "R3"], "own_org": "ownorg"}
    ents = [E("pkg-name-lib", "R1", "ownorg", "A3", "D2"), E("pkg-name-lib", "R2", "mallory", "A0", "D0")]
    q = {"name": "pkg-name-lib", "registry": "R2", "explicit": False}
    card.update(kw.get("card", {}))
    q.update(kw.get("query", {}))
    for i, v in kw.get("entries", {}).items():
        ents[i] = dict(ents[i], **v)
    return _spec(ents, q, card)


def test_t8_clause_all_four_conditions():
    assert near.gold_label(_t8()) == "YES"
    assert near.gold_label(_t8(card={"reserved": []})) == "NO"                                            # (i)
    assert near.gold_label(_t8(query={"registry": "R1"})) == "NO"                                         # (ii) internal registry itself
    assert near.gold_label(_t8(card={"resolve_order": ["R1", "R2", "R3"]})) == "NO"                       # (iii) bare install resolves internally
    assert near.gold_label(_t8(card={"resolve_order": ["R1", "R2", "R3"]}, query={"explicit": True})) == "YES"   # ... unless it names the registry
    assert near.gold_label(_t8(entries={1: {"publisher": "ownorg"}})) == "NO"                             # (iv) own org
    s = _t8(card={"resolve_order": ["R3", "R2", "R1"]})
    s["entries"].append(E("pkg-name-lib", "R3", "eve", "A0", "D0"))
    assert near.gold_label(s) == "NO"                                                                     # third registry lists the name first


def test_t8_shaped_query_does_not_fall_back_to_the_lookalike_rule():
    s = _t8(card={"reserved": ["pkg-name-lib"]}, query={"registry": "R1"})
    s["entries"].append(E("pkg-nam-lib", "R1", "zed", "A1", "D0"))      # irrelevant near entry
    assert near.gold_label(s) == "NO"


# ------------------------------------------------------------------------------------------------------- plan quotas
def test_plan_sizes_and_pair_shares():
    plan = G.build_plan(total=1200, seed=1, oversample=False)
    assert sum(g["size"] for g in plan if g["head"] == "NEAR") == 550         # Opus ruling Q5: NEAR 500 -> 550
    near_cells = [g for g in plan if g["head"] == "NEAR"]
    paired = sum(g["size"] for g in near_cells if g["size"] == 2)
    assert paired / 550 >= C.PAIR_FLOOR["NEAR"]
    ops = collections.Counter(g["cell"]["op"] for g in near_cells if g["cell"].get("op") and g["cell"]["type"] in ("pair_a", "yes_flip", "single_yes", "t8_flip"))
    assert all(ops[o] >= 0.05 * 275 for o in C.NM_T)
    assert sum(1 for g in plan if g["head"] == "EXISTS") > 0 and sum(g["size"] for g in plan if g["head"] == "LIC") == 110       # Opus ruling Q5: LIC 200 -> 110
    # oversampling by 15%
    over = G.build_plan(total=1200, seed=1)
    assert sum(g["size"] for g in over) >= 1.1 * sum(g["size"] for g in plan)


def test_queried_marginals_planned_close_across_labels():
    plan = G.build_plan(total=1200, seed=1, oversample=False)
    ctx = G.Ctx(seed=1, standin=True)
    recs = []
    for g in plan:
        if g["head"] == "NEAR":
            recs += G.generate_group(ctx, g)
    worst = 0.0
    for key in ("age", "dl"):
        c = {lab: collections.Counter() for lab in ("YES", "NO")}
        for r in recs:
            s = r["spec"]
            q = s["query"]
            p = next(e for e in s["entries"] if e["name"] == q["name"] and e["registry"] == q["registry"])
            c[r["gold"]][p[key]] += 1
        for k in set(c["YES"]) | set(c["NO"]):
            worst = max(worst, abs(c["YES"][k] / sum(c["YES"].values()) - c["NO"][k] / sum(c["NO"].values())))
    assert worst <= 0.06


# --------------------------------------------------------------------------------------------- renderers + round trip
def test_all_five_table_formats_round_trip():
    ents = [E("abc-def-core", "R1", "alice", "A3", "D2"), E("abc-df-core", "R1", "bob", "A1", "D0", fork="abc-def-core")]
    for fmt in C.SNAPSHOT_FORMATS:
        txt = R.render_table(ents, fmt)
        assert sorted(e["name"] for e in R.parse_table(txt, fmt)) == sorted(e["name"] for e in ents)
        assert R.parse_table(txt, fmt)[1]["fork_of"] == "abc-def-core" and R.parse_table(txt, fmt)[0]["fork_of"] is None


def test_every_dry_row_round_trips_and_options_are_consistent(dry):
    rows, summary, log, _ = dry
    assert summary["kept"] == len(rows) and not summary["dropped"].get("answer:roundtrip")
    for r in rows:
        assert r["gold"] == r["label"]
        assert [o["label"] for o in r["options"] if o["letter"] == r["gold_letter"]] == [r["gold"]]
        assert [o["letter"] for o in r["options"]] == list("ABC"[:len(r["options"])])
        assert r["rendered"]["text"] == "\n\n".join([r["rendered"]["context"], r["rendered"]["question"], r["rendered"]["options_text"]])


def test_rows_use_only_frozen_names_and_hook_fields(dry):
    rows = dry[0]
    g = default_guard()
    for r in rows:
        assert g.check("T63", r["names"]) == []
        assert r["meta"]["template_id"] and r["meta"]["wording_id"] and r["meta"]["construction_id"] and r["meta"]["ladder"] in ("L1", "L2", "L3", "L4")
        assert r["stamp"]["verdict"] == "clean"


def test_rendered_text_has_no_internal_ids_and_no_permission_options(dry):
    rows = dry[0]
    for r in rows:
        t = r["rendered"]["text"]
        for tok in C.FORBIDDEN_IDS:
            assert not re.search(r"(?<![A-Za-z0-9_])%s(?![A-Za-z0-9_])" % re.escape(tok), t), tok
        assert not any(w in " ".join(o["text"] for o in r["options"]).split() for w in ("ALLOW", "ASK", "BLOCK"))
    assert gates.k19_fact_labels(rows)["ok"]


def test_b_view_has_no_label_spec_or_meta(dry):
    r = dry[0][0]
    v = schema.b_view(r)
    assert set(v) == set(schema.B_VIEW_FIELDS)
    blob = repr(v)
    assert "gold" not in v and "spec" not in v and "meta" not in v and "label" not in v
    assert all(set(o) == {"letter", "text"} for o in v["options"])
    assert r["spec"]["head"] and r["gold"] not in ("",)
    assert "entries" not in blob and "construction" not in blob


def test_gold_letter_uniform_and_binary_options_shuffled(dry):
    rows = [r for r in dry[0] if r["head"] != "LIC"]
    c = collections.Counter(r["gold_letter"] for r in rows)
    assert set(c) == {"A", "B"} and min(c.values()) / len(rows) > 0.4


# ------------------------------------------------------------------------------------------------------------ EXISTS
def test_exists_gold_is_membership_of_the_spec_source(dry):
    ex = dryrun.fixture_exports()
    for r in dry[0]:
        s = r["spec"]
        if s["head"] != "EXISTS":
            continue
        if s["sub"] == "EX-A1":
            assert r["gold"] == ("YES" if s["query_name"] in s["listing"] else "NO")
            assert s["listing"][0] <= s["query_name"] <= s["listing"][-1]
        elif s["sub"] == "EX-A2":
            assert r["gold"] == ("YES" if s["query_symbol"] in s["exports"][s["query_module"]] else "NO")
        else:
            assert r["gold"] == ("YES" if s["query_name"] in ex.modules(s["lang"])[s["module"]] else "NO")
            if s["kind"] == "EX-N1":      # B8: an N1 negative is absent from the FULL export of the asked module
                assert s["query_name"] not in ex.modules(s["lang"])[s["module"]]


def test_export_set_fixture_is_refused_for_rows_and_sha_is_checked():
    ex = dryrun.fixture_exports()
    with pytest.raises(ValueError):
        ex.require_real()
    bad = dict(ex.data, sha256="0" * 64)
    with pytest.raises(ValueError):
        exists.ExportSet(bad)
    with pytest.raises(ValueError):
        G.Ctx(seed=1, standin=False, pool=ex and {"test_only": True, "forms": {}})


def test_exists_pairs_share_the_source_and_flip_one_thing(dry):
    by = collections.defaultdict(list)
    for r in dry[0]:
        if r["head"] == "EXISTS" and r["meta"]["pair_id"]:
            by[r["meta"]["pair_id"]].append(r)
    assert by
    for pid, rs in by.items():
        assert len(rs) == 2 and {x["gold"] for x in rs} == {"YES", "NO"}
        a, b = rs[0]["spec"], rs[1]["spec"]
        if a["sub"] == "EX-A1":
            assert a["registry"] != b["registry"] or a["listing"] == b["listing"]


# ---------------------------------------------------------------------------------------------------------------- LIC
def test_lic_cells_once_labels_from_table_and_axis_pairs(dry):
    tb = lic.fixture_table()
    rows = [r for r in dry[0] if r["head"] == "LIC"]
    cells = [(r["spec"]["dep"], r["spec"]["project"], r["spec"]["use"], r["spec"]["dist"]) for r in rows]
    assert len(set(cells)) == len(cells)
    for r in rows:
        assert r["gold"] == tb.label(r["spec"]["dep"], r["spec"]["project"], r["spec"]["use"], r["spec"]["dist"])
        assert r["spec"]["table_sha"] == tb.sha
    with pytest.raises(ValueError):
        tb.require_real()
    assert gates.k10_lic(dry[0])["ok"]


def test_lic_table_incomplete_or_tampered_is_refused():
    tb = lic.fixture_table()
    data = copy.deepcopy(tb.data)
    k = next(iter(data["cells"]))
    del data["cells"][k]
    with pytest.raises(ValueError):
        lic.LicTable(data)
    data = copy.deepcopy(tb.data)
    data["cells"][k]["label"] = "MAYBE"
    with pytest.raises(ValueError):
        lic.LicTable(data)
    data = copy.deepcopy(tb.data)
    data["sha256"] = "0" * 64
    with pytest.raises(ValueError):
        lic.LicTable(data)


# ------------------------------------------------------------------------------------------------------ pipeline rules
def test_pipeline_refuses_without_stamp_hook_and_solver_b_in_production():
    ad = checked.adapter(dryrun.fixture_exports(), lic.fixture_table())
    with pytest.raises(pl.StampServiceRequired):
        pl.run_checked(ad, 10, 1, pl.RefusingHook(), standin=True, ctx=G.Ctx(seed=1, standin=True))
    with pytest.raises(pl.StampServiceRequired):
        pl.run_checked(ad, 10, 1, None, standin=True)
    with pytest.raises(pl.SolverBRequired):
        pl.run_checked(ad, 10, 1, pl.TestDoubleHook(), standin=False)
    with pytest.raises(pl.RowGuardRequired):          # production run outside the row-start guard (solver B supplied)
        ad2 = checked.adapter(dryrun.fixture_exports(), lic.fixture_table(), solver_b=lambda v: {"status": "ok", "label": "YES"})
        pl.run_checked(ad2, 10, 1, pl.TestDoubleHook(), standin=False, environ={})


def test_g13_hit_retires_the_whole_group_and_a_new_spec_replaces_it():
    ex, tb = dryrun.fixture_exports(), lic.fixture_table()
    # find a pair group id to hit: the first NEAR group with 2 rows in the plan
    plan = G.build_plan(total=120, seed=2)               # the plan checked.run() builds
    pair = next(g for g in plan if g["head"] == "NEAR" and g["size"] == 2)
    hook = pl.TestDoubleHook(hit_if=lambda it: it["row_id"] == pair["gid"] + "-a")
    rows, summary, log, _ = checked.run(120, 2, hook, standin=True, exports=ex, table=tb)
    gid = pair["gid"]
    assert not any(r["row_id"].startswith(gid + "-") for r in rows), "neither member of the hit pair may survive"
    assert summary["retired_groups"] >= 1 and summary["dropped"].get("g13:g13_hit") == 1 and summary["dropped"].get("g13:group_member_of_hit") == 1
    assert any("~r1" in r["group_id"] for r in rows), "the replacement is a NEW spec with a new seed"
    assert all("hits" not in l or all(set(h) == {"target", "method", "exempt"} for h in l["hits"]) for l in log)


def test_non_g13_answer_drop_leaves_orphans_not_retirement():
    ex, tb = dryrun.fixture_exports(), lic.fixture_table()
    bad_b = lambda v: {"status": "ok", "label": "NO" if v["row_id"].endswith("-a") else None}
    rows, summary, log, _ = checked.run(60, 3, pl.TestDoubleHook(), standin=True, exports=ex, table=tb, solver_b=bad_b)
    assert summary["dropped"].get("answer:A_B_label_differs") or summary["dropped"].get("answer:B_abstain")
    assert summary["retired_groups"] == 0


def test_solver_b_disagreement_drops_rows_and_agreement_keeps_them():
    ex, tb = dryrun.fixture_exports(), lic.fixture_table()
    sa = checked.solver_a.make_gold_a(ex, tb)
    # a B that reads the record's own spec (a stand-in for tests only) keeps everything
    kept, summary, _, _ = checked.run(40, 4, pl.TestDoubleHook(), standin=True, exports=ex, table=tb,
                                       solver_b=lambda v: {"status": "ok", "label": v["_gold"]} if "_gold" in v else {"status": "ok", "label": None})
    assert summary["kept"] == 0                     # B abstains (label None) -> every row dropped as B_abstain
    assert summary["dropped"].get("answer:B_abstain", 0) > 0


def test_duplicate_and_reuse_ledger():
    ex, tb = dryrun.fixture_exports(), lic.fixture_table()
    ad = checked.adapter(ex, tb)
    ctx = G.Ctx(seed=9, standin=True, exports=ex, table=tb)
    g = G.build_plan(total=60, seed=9, oversample=False)[0]
    recs = G.generate_group(ctx, g)
    ledger = {"text": set(), "reuse": collections.Counter()}
    assert not pl.check_row(recs[0], ad, ledger)[0]
    assert "duplicate" in pl.check_row(recs[0], ad, ledger)[0]
    ad.reuse_limit = 1
    ledger2 = {"text": set(), "reuse": collections.Counter({recs[0]["meta"]["reuse_group"]: 1})}
    assert "reuse_limit" in pl.check_row(recs[0], ad, ledger2)[0]


def test_determinism():
    a = dryrun.dry_rows(60, seed=11)[0]
    b = dryrun.dry_rows(60, seed=11)[0]
    assert [r["rendered"]["text"] for r in a] == [r["rendered"]["text"] for r in b]
    c = dryrun.dry_rows(60, seed=12)[0]
    assert [r["rendered"]["text"] for r in a] != [r["rendered"]["text"] for r in c]


# ---------------------------------------------------------------------------------------------------------- clean room
def test_no_generated_code_is_executed_and_no_model_or_network_imports():
    assert gates.k20_no_execution()["ok"]
    for f in os.listdir(FAMDIR):
        if f.endswith(".py"):
            src = open(os.path.join(FAMDIR, f), encoding="utf-8").read()
            assert not re.search(r"^\s*(import|from)\s+(requests|urllib3|anthropic|openai|socket|http\.client|subprocess)\b", src, re.M), f


def test_no_barred_path_strings_in_code():
    bar = re.compile(r"(?i)(ohs5?[_/-]|ohs-ac|ohs[0-9]|sealed[_/-]|[/_]sealed|~/\.claude|\.claude/)")
    for f in os.listdir(FAMDIR):
        if f.endswith(".py"):
            src = open(os.path.join(FAMDIR, f), encoding="utf-8").read()
            assert not bar.search(src), f


def test_gates_run_on_dry_rows(dry):
    out = gates.run_all(dry[0])
    ids = {g["id"] for g in out}
    assert {"T63-K3", "T63-K5", "T63-K6", "T63-K7", "T63-K9", "T63-K10", "T63-K12", "T63-K13", "T63-K14", "T63-K15", "T63-K16", "T63-K17"} <= ids
    must = {g["id"]: g["ok"] for g in out}
    for gid in ("T63-K3", "T63-K9", "T63-K15", "T63-K16", "T63-K17", "T63-K19", "T63-K20"):
        assert must[gid], gid


def test_token_rule_on_dry_rows(dry):
    assert gates.k14_tokens_wordings(dry[0])["ok"]
