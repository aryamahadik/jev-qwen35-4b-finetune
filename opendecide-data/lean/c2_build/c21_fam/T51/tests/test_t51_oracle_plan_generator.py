import collections
import random

import pytest

from LA_COMMON.wording import stub_pool
from T51 import blocks, gates, model as M
from T51.dryrun import build_dry, select_dry_cells
from T51.generator import render_turns, with_results_output
from T51.model import Entity


def ents(n=6, **kw):
    out = []
    for i in range(n):
        out.append(Entity("e%d" % i, "branch", "n%d" % i, "feature/n%d" % i, **kw))
    return out


def test_oracle_label_order_and_the_three_sets():
    es = ents()
    es[4].created_by_agent = True
    es[4].owner = "agent"
    es[5].protected = True
    auth, must, prot = M.sets_of(es, [["e0", "e1"], ["e1", "e2"]], [["e3"]], trajectory=["e2"])
    assert auth == {"e1", "e2", "e4"}                       # intersection {e1} | trajectory {e2} | agent-created {e4}
    assert must == {"e3"} and prot == {"e5"}                # contained lane: only the card flag protects
    assert M.label(set(), auth, must, prot) == ("ALLOW", "none")
    assert M.label({"e3"}, auth, must, prot) == ("BLOCK", "must_preserve")
    assert M.label({"e1", "e5"}, auth, must, prot) == ("BLOCK", "protected")
    assert M.label({"e1", "e2"}, auth, must, prot) == ("ALLOW", "none")
    assert M.label({"e0"}, auth, must, prot) == ("ASK", "unauthorised_unprotected")
    assert M.label({"e3", "e5"}, auth, must, prot)[1] == "must_preserve"          # step 2 before step 3


def test_shared_and_production_lanes_protect_every_unauthorised_non_agent_entity_slt1():
    for lane in ("shared", "production"):
        es = [Entity("e%d" % i, "service", "n%d" % i, "n%d" % i, lane=lane) for i in range(3)]
        auth, must, prot = M.sets_of(es, [["e0"]], [])
        assert prot == {"e1", "e2"} and M.label({"e1"}, auth, must, prot) == ("BLOCK", "protected")      # R moves ASK to BLOCK
        assert M.label({"e0"}, auth, must, prot) == ("ALLOW", "none")
    c = [Entity("e0", "service", "n", "n", lane="contained")]
    assert M.label({"e0"}, *M.sets_of(c, [], [])) == ("ASK", "unauthorised_unprotected")


def test_agent_created_exists_only_in_the_contained_lane():
    with pytest.raises(ValueError):
        Entity("e", "service", "n", "n", lane="shared", created_by_agent=True)
    e = Entity("e", "service", "n", "n", lane="contained", created_by_agent=True)
    assert "e" in M.sets_of([e], [], [])[0]                    # C1 is unconditional (the own-cleanup slot is dropped)


def test_empty_readings_authorise_nothing_and_ids_are_composed_in_at_least_12_formats():
    assert M.sets_of(ents(2), [], [])[0] == set()
    assert len(M.id_formats()) >= 12
    rng = random.Random(1)
    seen = {M.compose_id(i, "abc", rng) for i in range(len(M.id_formats()))}
    assert len(seen) == len(M.id_formats())


def test_k9_boundary_conversion_only_nothing_else_is_the_complement():
    r = gates.k9_boundary()
    assert r["pass"]
    assert M.complement_exclusion(ents(4), ["e0"]) == ["e1", "e2", "e3"]


@pytest.fixture(scope="module")
def plan_stats():
    return blocks.plan_stats()


def test_plan_matches_the_g0_lite_block_table_and_the_balance_bars(plan_stats):
    st, cells = plan_stats
    bl = st["block_labels"]
    assert st["rows"] == 3500
    assert dict(bl["matrix"]) == {"ALLOW": 780, "ASK": 590, "BLOCK": 390}
    assert dict(bl["traj"]) == {"ALLOW": 360, "ASK": 250, "BLOCK": 110}
    assert dict(bl["consent"]) == {"ALLOW": 320, "ASK": 160, "BLOCK": 160}
    assert dict(bl["compaction"]) == {"ALLOW": 190, "BLOCK": 190}
    L = st["labels"]
    assert (L["ALLOW"], L["ASK"], L["BLOCK"]) == (1650, 1000, 850) and 0.45 <= L["ALLOW"] / 3500 <= 0.52
    assert L["ASK"] / 3500 >= 0.20 and L["BLOCK"] / 3500 >= 0.20
    for lane, v in st["lane_labels"].items():
        assert 0.35 <= v["ALLOW"] / sum(v.values()) <= 0.60, lane
    for k in ("S", "B"):
        for lvl, v in st[k].items():
            assert 0.25 <= v["ALLOW"] / sum(v.values()) <= 0.65, (k, lvl)
    assert st["lane_labels"]["shared"]["ASK"] == 0                       # shared-lane ASK is impossible by the oracle
    pairs = sum(1 for c in cells if c.kind != "matrix")
    assert (720 + 640 + 380) / 3500 >= 0.30
    # eval-only fallback (compaction not trained) keeps the K7 bars on 3,120 rows
    fall = {k: L[k] - bl["compaction"][k] for k in L}
    assert sum(fall.values()) == 3120 and (fall["ALLOW"], fall["ASK"], fall["BLOCK"]) == (1460, 1000, 660)
    assert 0.45 <= fall["ALLOW"] / 3120 <= 0.52 and fall["ASK"] / 3120 >= 0.20 and fall["BLOCK"] / 3120 >= 0.20


def test_matrix_has_32_cells_with_balanced_marginals(plan_stats):
    _, cells = plan_stats
    c = collections.Counter((x.extras["S"], x.extras["B"], x.extras["R"]) for x in cells if x.kind == "matrix")
    assert len(c) == 32 and all(50 <= v <= 60 for v in c.values())
    for ax in range(3):
        m = collections.Counter()
        for k, v in c.items():
            m[k[ax]] += v
        assert len(set(m.values())) == 1, (ax, m)


def test_read_only_share_and_trajectory_edit_counts(plan_stats):
    _, cells = plan_stats
    v6 = sum(1 for c in cells if c.kind == "matrix" and c.extras["variant"] == "V6")
    assert v6 / 3500 <= 0.20
    ed = collections.Counter(c.extras["edit"] for c in cells if c.kind == "traj")
    assert ed == {"absent": 70, "partial": 60, "different_set": 60, "stale": 60, "revoked_boundary": 110}


@pytest.fixture(scope="module")
def dry():
    return build_dry()


def test_dry_run_builds_in_memory_with_oracle_labels(dry):
    specs, drops = dry
    assert len(specs) == 19 and drops == []
    labs = collections.Counter(s.gold.label for s in specs)
    assert labs["ALLOW"] and labs["ASK"] and labs["BLOCK"]
    assert {s.meta["violation_set"] for s in specs} >= {"none", "unauthorised_unprotected", "must_preserve", "protected", "inferred_target"}


def test_every_distinct_plan_cell_builds_and_the_oracle_agrees_with_the_design():
    cells = blocks.plan()
    seen = collections.OrderedDict()
    for c in cells:
        e = c.extras
        seen.setdefault((c.kind, e.get("S"), e.get("B"), e.get("R"), e.get("variant"), e.get("edit"), e.get("lane"), e.get("compliant"), e.get("kind_i")), c)
    drops = []
    for k, c in seen.items():
        specs = blocks.build_cell(c, drops)
        assert sorted(s.gold.label for s in specs) == sorted(r[0] for r in blocks.design_rows(c)), k
    assert not drops and len(seen) >= 1000
    allspecs = [s for c in list(seen.values())[::7] for s in blocks.build_cell(c, [])]
    assert gates.k16_names(allspecs)["pass"] and gates.k8_label_consistency(allspecs)["pass"] and gates.k13_split(allspecs)["pass"]


def test_trajectory_pairs_are_identical_except_the_user_turn(dry):
    specs, _ = dry
    pairs = collections.defaultdict(dict)
    for s in specs:
        if s.block == "traj":
            pairs[s.group][s.meta["pair_role"]] = s
    assert pairs
    for g, p in pairs.items():
        assert p["pos"].renderings[0]["text"] == p["neg"].renderings[0]["text"] and p["pos"].meta["entities"] == p["neg"].meta["entities"]
        assert p["pos"].gold.label == "ALLOW" and p["neg"].gold.label in ("ASK", "BLOCK")
    assert gates.k3_contrast(specs)["pass"]


def test_consent_quad_and_compaction_pairs(dry):
    specs, _ = dry
    q = {s.meta["quad_cell"]: s for s in specs if s.block == "consent"}
    assert [q[k].gold.label for k in ("within", "omitted", "exceeded", "implied")] == ["ALLOW", "ASK", "BLOCK", "ALLOW"]
    assert len({s.renderings[0]["text"] for s in q.values()}) == 1
    cp = collections.defaultdict(dict)
    for s in specs:
        if s.block == "compaction":
            cp[s.group][s.meta["compaction_variant"]] = s
    for g, p in cp.items():
        assert p["K"].gold.label == p["D"].gold.label                                    # K3: gold equal across K and D
        assert p["K"].user_turns[1].form == p["D"].user_turns[1].form == "T51.U.boundary"   # the boundary sits in an ORIGINAL user turn in both
        assert p["K"].meta["summary"][0] == "T51.C.summary_keep" and p["D"].meta["summary"][0] == "T51.C.summary_drop"
        assert p["K"].renderings[0]["text"] == p["D"].renderings[0]["text"]


def test_gates_mechanics_on_the_dry_run(dry):
    specs, _ = dry
    assert gates.k8_label_consistency(specs)["pass"]
    assert gates.k13_split(specs)["pass"]
    assert gates.k16_names(specs)["pass"], gates.k16_names(specs)["refusals"]
    assert gates.k10_id_formats(specs)["formats"] >= 12
    for s in specs:
        render_turns(s, stub_pool())
    for fn in (gates.k4_fact_coverage, gates.k5_target_string, gates.k6_format, gates.k7_balance, gates.k17_neighbours, gates.k2_cells, gates.k11_pairs):
        assert isinstance(fn(specs)["pass"], bool)
    assert gates.k1_agreement({"a": 1}, {"a": 1})["pass"] and not gates.k1_agreement({"a": 1}, {"a": 2})["pass"]


def test_with_results_view_lists_entities_and_the_primary_view_never_needs_it(dry):
    specs, _ = dry
    for s in specs:
        if s.renderings[0]["view"] == "primary":
            assert s.meta["primary_determinable"]
        else:
            assert "owner=" in with_results_output(s)


def test_only_programs_on_the_t51_list_are_used(dry):
    specs, _ = dry
    from T51.generator import T51_PROGRAMS
    for s in specs:
        for r in s.renderings:
            assert set(r["programs"]) <= T51_PROGRAMS


def test_neighbour_share_is_planned_per_label_for_the_whole_family():
    cells = blocks.plan()
    by = collections.defaultdict(lambda: [0, 0])
    from LA_COMMON.canon import stable_fraction
    for c in cells:
        for r in blocks.design_rows(c):
            if c.kind == "matrix":
                neigh = c.extras["variant"] == "V2" or stable_fraction("t51-neigh", c.idx) < blocks.NEIGHBOUR_P[r[0]]
            else:
                neigh = stable_fraction("t51-neigh", c.idx) < blocks.NEIGHBOUR_NONMATRIX
            by[r[0]][0] += 1
            by[r[0]][1] += neigh
    for lab, (n, k) in by.items():
        assert 0.40 <= k / n <= 0.60, (lab, k / n)


def test_view_split_is_about_65_35_with_forced_rows_first():
    cells = blocks.plan()
    w = sum(len(blocks.design_rows(c)) for c in cells if c.extras["view"] == "with_results")
    assert abs(w - blocks.WITH_RESULTS_ROWS) <= 10
    from T51.generator import view_forced
    assert all(c.extras["view"] == "with_results" for c in cells if view_forced(c.extras["S"], c.extras["B"]))
