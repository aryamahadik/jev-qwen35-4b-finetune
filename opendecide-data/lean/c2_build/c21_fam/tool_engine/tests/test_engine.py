"""Unit tests of the shared L-T tool-scenario engine (CPU only; no rows; nothing is written to disk)."""
import copy
import json
import random

import pytest

from tool_engine import dag, gates_common as gc, invariants, names, perturb, render, state, util, wording


# ---- util ----------------------------------------------------------------------------------------------------
def test_largest_remainder_exact_and_proportional():
    got = util.largest_remainder(4000, {"a": 1000, "b": 800, "c": 800, "d": 500, "e": 500, "f": 400})
    assert got == {"a": 1000, "b": 800, "c": 800, "d": 500, "e": 500, "f": 400}
    got = util.largest_remainder(7, {"a": 1, "b": 1, "c": 1})
    assert sum(got.values()) == 7 and sorted(got.values()) == [2, 2, 3]
    with pytest.raises(ValueError):
        util.largest_remainder(3, {"a": 0})


def test_balanced_cycle_counts_and_determinism():
    c = util.balanced_cycle(103, 4, util.rng_for("x"))
    counts = [c.count(i) for i in range(4)]
    assert max(counts) - min(counts) <= 1 and sum(counts) == 103
    assert util.balanced_cycle(50, 5, util.rng_for("x")) == util.balanced_cycle(50, 5, util.rng_for("x"))


def test_rng_for_is_deterministic_and_keyed():
    assert util.rng_for("a", 1).random() == util.rng_for("a", 1).random()
    assert util.rng_for("a", 1).random() != util.rng_for("a", 2).random()


def test_place_gold_and_non_identity_permutation():
    rng = util.rng_for("p")
    for pos in range(4):
        order = util.place_gold(["w", "x", "y", "z"], "y", pos, rng)
        assert order[pos] == "y" and sorted(order) == ["w", "x", "y", "z"]
    for _ in range(20):
        assert util.non_identity_permutation(2, rng) == [1, 0]
        assert util.non_identity_permutation(5, rng) != list(range(5))


def test_tv_distance():
    assert util.tv_distance({1: 5, 2: 5}, {1: 5, 2: 5}) == 0
    assert util.tv_distance({1: 10}, {2: 10}) == 1.0


# ---- names ---------------------------------------------------------------------------------------------------
def test_allowlist_is_frozen_and_sha_checked(tmp_path):
    al = names.AllowList.load()
    assert al.data["frozen"] is True and len(al.family_names("T54")["tool"]) == 60
    p = tmp_path / "m.json"
    d = copy.deepcopy(al.data)
    d["names"]["tool"].append("verb.evil")
    p.write_text(json.dumps(d))
    with pytest.raises(names.NameGuardError):
        names.AllowList.load(path=str(p), expect_sha=al.file_sha)
    d2 = copy.deepcopy(al.data)
    d2["frozen"] = False
    p.write_text(json.dumps(d2))
    with pytest.raises(names.NameGuardError):
        names.AllowList.load(path=str(p), expect_sha=util.sha256_file(str(p)))


def test_allowlist_refuses_off_list_names_per_family():
    al = names.AllowList.load()
    assert al.check_names("T54", {"tool": ["verb.get", "param.id"], "policy": ["card.t54.strict_ask"]}) == []
    assert ("tool", "verb.nope") in al.check_names("T54", {"tool": ["verb.nope"]})
    assert al.check_names("T56", {"tool": ["param.status"]}) == [("tool", "param.status")]       # T56 lists no param roles
    assert al.check_names("T55", {"tool": ["verb.open"]}) == [("tool", "verb.open")]            # open is T54-only
    assert al.check_names("T54", {"language": ["python"]}) == [("language", "python")]          # T54 has no languages
    assert al.check_names("T56", {"language": ["python"], "runner": ["runner.pytest"]}) == []
    assert al.check_names("T54", {"colour": ["x"]}) == [("colour", "x")]
    with pytest.raises(names.NameGuardError):
        al.assert_names("T55", {"carrier": ["carrier.made_up"]})


def test_namesource_standin_is_gated_and_production_refuses():
    prod = names.NameSource("T54")
    with pytest.raises(names.NamespaceError):
        prod.noun("noun_entity", 0)
    with pytest.raises(names.NamespaceError):
        prod.assert_production_ready()
    st = names.NameSource("T54", standin=True)
    with pytest.raises(names.NamespaceError):
        st.assert_production_ready()                       # a stand-in source is never production ready
    assert st.noun("noun_entity", 3) == names.NameSource("T54", standin=True).noun("noun_entity", 3)


def test_namespace_fingerprint_is_the_training_one():
    assert names.NameSource("T54", standin=True).fingerprint() == "0844fd92219a"


def test_noun_buckets_are_disjoint_per_family():
    a, b, c = (names.NameSource(f, standin=True) for f in ("T54", "T55", "T56"))
    for src in (a, b, c):
        for i in range(400):
            src.noun("noun_entity", i)
    assert names.assert_buckets_disjoint([a, b, c])


def test_draw_nouns_is_idempotent_and_does_not_consume_the_callers_rng():
    s = names.NameSource("T54", standin=True)
    r1, r2 = random.Random(5), random.Random(5)
    x = s.draw_nouns("noun_entity", 3, "k", r1)
    assert r1.getstate() == r2.getstate()
    assert s.draw_nouns("noun_entity", 3, "k", r1) == x
    assert s._uses[x[0]] == 1                               # a twin / retry is not another use


def test_noun_reuse_is_capped_at_three_scenarios():
    s = names.NameSource("T54", standin=True)
    rng = random.Random(0)
    for i in range(40):
        s.draw_nouns("noun_entity", 4, "sc%d" % i, rng, pool_size=60)
    assert max(s._uses.values()) <= names.MAX_NOUN_REUSE
    with pytest.raises(names.NamespaceError):                    # the pool is exhausted rather than a noun being over-used
        for i in range(40, 200):
            s.draw_nouns("noun_entity", 4, "sc%d" % i, rng, pool_size=60)
    assert max(s._uses.values()) <= names.MAX_NOUN_REUSE


def test_id_stem_never_an_english_command():
    for w in ("setoliz", "getkubo", "runnabe", "kolen", "tagulo"):
        assert state.id_stem(w) not in state._STEM_DENY


# ---- dag -----------------------------------------------------------------------------------------------------
def test_kahn_levels_equal_longest_path_depth_on_random_dags():
    rng = random.Random(1)
    for _ in range(60):
        n = rng.randint(2, 9)
        nodes = ["n%d" % i for i in range(n)]
        edges = [(nodes[i], nodes[j]) for i in range(n) for j in range(i + 1, n) if rng.random() < 0.3]
        lv = dag.kahn_levels(nodes, edges)
        depth = dag.longest_path_levels(nodes, edges)
        for k, level in enumerate(lv):
            assert all(depth[x] == k for x in level)


def test_dag_cycle_and_unknown_edges_are_errors():
    with pytest.raises(dag.DagError):
        dag.kahn_levels(["a", "b"], [("a", "b"), ("b", "a")])
    with pytest.raises(dag.DagError):
        dag.kahn_levels(["a"], [("a", "zz")])


def test_ready_set_and_layered_builder_shape():
    rng = random.Random(3)
    for nd, nr, nb in ((0, 1, 1), (2, 3, 2), (1, 2, 3), (2, 4, 1)):
        nodes, edges, done = dag.build_layered_dag(rng, nd, nr, nb)
        assert len(dag.ready_set(nodes, edges, done)) == nr
    assert dag.ready_set(["a", "b"], [("a", "b")], ["a"]) == ["b"]
    assert dag.canonical_set({"x": "g1", "y": "g1", "z": "g2"}, ["y", "z"]) == ("g1", "g2")


# ---- ledger / B2 ---------------------------------------------------------------------------------------------
def test_ledger_dedup_semantics():
    led = state.Ledger()
    assert led.commit("e", "r0", True) and not led.commit("e", "r0", True)           # same request, deduplicated
    assert led.commit("e", "r0", False)                                              # no key / not idempotent: duplicates
    assert led.commit("e", "r-new", True) and led.count("e") == 3                    # a new attempt always lands


def test_ambiguous_write_simulation_matches_the_rule_on_the_whole_truth_table():
    import itertools
    for I, kf, rp, c, st in itertools.product((False, True), (False, True), (False, True), (False, True), (1, 2)):
        want = (("RETRY_KEYED" if (I or kf) else ("READ_BACK" if rp else "ASK")) if st == 1
                else ("NO_RETRY" if c else "RETRY_PLAIN"))
        assert state.ambiguous_write_simulated_gold(I, kf, rp, c, st) == want


def test_each_option_outcome_in_both_worlds():
    f = state.effects_after
    assert f("RETRY_PLAIN", True, False, False, False) == 2 and f("RETRY_PLAIN", False, False, False, False) == 1
    assert f("NO_RETRY", True, False, False, False) == 1 and f("NO_RETRY", False, False, False, False) == 0
    assert f("RETRY_KEYED", True, False, True, False) == 1 and f("RETRY_KEYED", True, False, False, False) == 2
    assert f("READ_BACK", True, False, False, False) is None and f("READ_BACK", True, False, False, True) == 1


# ---- invariants ----------------------------------------------------------------------------------------------
@pytest.mark.parametrize("vt", perturb.VIOLATION_TYPES)
def test_each_checker_fires_on_its_violation_and_not_on_the_twin(vt):
    rng = random.Random(11)
    for cause in ("data", "arg"):
        if cause == "arg" and vt not in invariants.ARG_CAPABLE:
            continue
        for _ in range(8):
            b = invariants.make_base(vt, rng, "kol", "qty", cause)
            rv, cv = invariants.materialise(b, True)
            rg, cg = invariants.materialise(b, False)
            assert invariants.violations(rv, cv) == {vt}
            assert invariants.violations(rg, cg) == set()
            assert invariants.cause(vt, rv, cv) == cause


def test_benign_oddities_are_valid():
    rng = random.Random(2)
    for o in invariants.BENIGN_ODDITIES:
        r, c = invariants.make_benign(o, rng, "kol", "qty")
        assert invariants.violations(r, c) == set()


def test_heldout_types_are_a_reproducible_seeded_draw_of_two():
    assert perturb.draw_heldout_types() == perturb.HELDOUT_TYPES and len(perturb.HELDOUT_TYPES) == 2
    assert set(perturb.TRAIN_TYPES) | set(perturb.HELDOUT_TYPES) == set(perturb.VIOLATION_TYPES)
    assert perturb.draw_heldout_types("another seed") != () and len(perturb.TRAIN_TYPES) == 6


# ---- render / lint / wording ---------------------------------------------------------------------------------
def test_output_lint_flags_commands_and_second_person_only():
    assert render.lint_output("status: ok\ncount: 3\ndetail: temporarily unavailable") == []
    assert render.lint_output("detail: you must retry")
    assert render.lint_output("detail: retry the call now")
    assert render.lint_output("status: open") == []                                  # a bare enum word is data
    assert render.lint_output("free text line")
    assert render.lint_output("zzz: 1", allowed_keys={"status"})


def test_value_span_counter():
    assert render.count_value_spans('close abc-123 on 2026-10-18 with 4 notes "x y"') == 4
    assert render.count_value_spans("no values here") == 0


def test_wording_fill_roundtrip_and_reword_check():
    t = "Close {entity} {ref} not later than 5 days"
    assert wording.fill(t, dict(entity="a", ref="b")) == "Close a b not later than 5 days"
    with pytest.raises(KeyError):
        wording.fill(t, dict(entity="a"))
    assert wording.reword_ok(t, "Please close {ref} {entity} not later than 5 days")
    assert not wording.reword_ok(t, "Close {entity} {ref} later than 5 days")        # lost the negation word
    assert not wording.reword_ok(t, "Close {entity} {ref} not later than 6 days")    # changed number
    assert not wording.reword_ok(t, "Close {entity} not later than 5 days")          # lost a slot
    assert wording.slots_survive({"a": "xyz"}, "hello xyz") == [] and wording.slots_survive({"a": "q"}, "none") == ["a"]


def test_wordingpool_export_sha_changes_with_any_template():
    p = wording.WordingPool({"f": ["a {x}", "b"]})
    s1 = p.export_sha()
    p.add("f", ["c"])
    assert p.export_sha() != s1 and p.count("f") == 3


# ---- gates_common ----------------------------------------------------------------------------------------------
class FakeHarness:
    def __init__(self, auc=0.5, upper=0.55, bacc=0.25):
        self._a, self._u, self._b = auc, upper, bacc

    def binary(self, X, y, groups):
        return {"auc": self._a, "upper": self._u, "valid": True}

    def kway(self, X, y, groups, k):
        return {"bacc": self._b, "upper": self._b + 0.02, "valid": True}


def test_probe_gate_bars():
    assert gc.probe_binary_gate("g", FakeHarness(0.52, 0.58), [], [], [])["ok"]
    assert not gc.probe_binary_gate("g", FakeHarness(0.56, 0.58), [], [], [])["ok"]
    assert not gc.probe_binary_gate("g", FakeHarness(0.52, 0.61), [], [], [])["ok"]
    assert gc.probe_kway_gate("g", FakeHarness(bacc=0.27), [], [], [], 4)["ok"]            # 1/4 + 3 pp = 28%
    assert not gc.probe_kway_gate("g", FakeHarness(bacc=0.30), [], [], [], 4)["ok"]
    lo, hi = gc.kway_bars(5)
    assert abs(lo - 0.23) < 1e-9 and abs(hi - 0.26) < 1e-9


def test_invalid_probe_run_cannot_pass():
    class Bad(FakeHarness):
        def binary(self, X, y, groups):
            return {"auc": 0.5, "upper": 0.5, "valid": False}
    assert not gc.probe_binary_gate("g", Bad(), [], [], [])["ok"]


def test_letter_share_and_pair_integrity_gates_detect_problems():
    recs = [dict(sub_block="s", gold_letter="A", group_id="g%d" % i, pair_role=None) for i in range(80)]
    assert not gc.letter_share_gate("L", recs, 4)["ok"]
    recs = [dict(sub_block="s", gold_letter="ABCD"[i % 4], group_id="g%d" % i, pair_role=None) for i in range(80)]
    assert gc.letter_share_gate("L", recs, 4)["ok"]
    bad = [dict(group_id="g", pair_role="a"), dict(group_id="g", pair_role="a")]
    assert not gc.pair_integrity(bad)["ok"]


def test_agreement_gate_drops_and_flags():
    recs = [dict(row_id="r%d" % i, gold="X") for i in range(200)]
    assert gc.agreement_gate("P-1", recs, lambda r: "X")["ok"]
    res = gc.agreement_gate("P-1", recs, lambda r: "Y" if r["row_id"] in ("r1", "r2", "r3") else "X")
    assert not res["ok"] and res["dropped_ids"] == ["r1", "r2", "r3"]


def test_token_gate_reads_mean_cap_and_1024_share():
    mk = lambda n: dict(rendered=dict(text="w " * n))      # noqa: E731
    assert gc.token_gate("T", [mk(100)] * 10, lambda t: len(t.split()))["ok"]
    assert not gc.token_gate("T", [mk(2000)], lambda t: len(t.split()))["ok"]
    assert not gc.token_gate("T", [mk(1100)] * 3 + [mk(100)] * 7, lambda t: len(t.split()))["ok"]


def test_job_manifest_declares_all_five_categories():
    rec = dict(row_id="r", names=dict(policy=["card.t54.strict_ask"], tool=["verb.get"], carrier=["carrier.user_single"]))
    m = names.job_manifest("T54", [rec])
    assert set(m["names"]) == set(names.CATEGORIES) and m["names"]["language"] == [] and m["rows"][0]["row_id"] == "r"
