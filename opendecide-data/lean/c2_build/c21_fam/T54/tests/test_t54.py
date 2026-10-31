"""T54 TOOL-NEED/PICK unit tests: generator, SOLVER A rule tables, renderer and the PRE-FREEZE CPU gates (no rows, no model,
nothing written to disk; every example is built in memory)."""
import collections
import copy
import functools
import importlib.util
import itertools
import os
import re

import pytest

import t54_dryrun
import t54_generator as gen
import t54_gates as gates
import t54_render as rd
import t54_solver_a as sa
from tool_engine import dag, names, render, state, util
from tool_engine.probe_stub import StubHarness

AL = names.AllowList.load()


@functools.lru_cache(maxsize=None)
def sample(total, seed="t54-test"):
    ctx = gen.Ctx(seed=seed, standin=True)
    return tuple(gen.generate_in_memory(total=total, seed=seed, ctx=ctx)), ctx


@pytest.fixture(scope="module")
def full():
    return list(sample(4000)[0])


@pytest.fixture(scope="module")
def pilot():
    return list(sample(1000, "t54-pilot")[0])


# ---- plan: sizes, mixes, pairs ------------------------------------------------------------------------------------
def test_plan_sizes_and_label_mixes_equal_the_g0_lite_section_4(full):
    c = collections.Counter(r["sub_block"] for r in full)
    assert c == collections.Counter(gen.SIZES) and len(full) == 4000
    lab = {sb: collections.Counter(r["gold"] for r in full if r["sub_block"] == sb) for sb in gen.LABEL_MIX}
    assert lab["s1_need4"] == {"CALL": 480, "ASK": 170, "NO_TOOL": 170, "ANSWER": 180}
    assert lab["s3_limit"] == {"CALL": 440, "NO_TOOL": 120, "ASK": 120, "RESULT_MISSING": 120}
    assert lab["s4_precond"] == {"WRITE": 140, "READ_FIRST": 120, "DONE_NO_CALL": 140, "ASK": 100}
    assert lab["s5_argground"] == {"GROUNDED": 250, "UNGROUNDED": 250}


def test_s3_limit_block_composition(full):
    s3 = [r for r in full if r["sub_block"] == "s3_limit"]
    c = collections.Counter(r["perturb"] for r in s3)
    assert c["perturb.del_tool"] == c["perturb.del_param"] == c["perturb.del_result"] == 120
    assert c["perturb.null_del"] == 120 and c["perturb.none"] == 320


def test_s6_ready_set_sizes_are_30_40_30(full):
    sizes = collections.Counter(min(len(sa.s6_ready_nodes(r)), 3) for r in full if r["sub_block"] == "s6_parseq")
    assert sizes == {1: 120, 2: 160, 3: 120}


def test_pairs_and_minimal_pair_share(full):
    assert gates.gc.pair_integrity(full)["ok"]
    assert gates.p12_pairs(full)["ok"] and gates.gc.pair_share(full) > 0.6
    by = collections.defaultdict(dict)
    for r in full:
        if r["pair_role"]:
            by[r["group_id"]][r["pair_role"]] = r
    # a card-edit pair differs ONLY in the card (and the gold it implies); a tool-list pair has the same request text
    for gid, d in list(by.items()):
        if "-pairC-" in gid:
            assert d["a"]["card"] != d["b"]["card"] and d["a"]["parts"]["request"] == d["b"]["parts"]["request"]
            assert (d["a"]["gold"], d["b"]["gold"]) == ("CALL", "ASK")
        if "-pairB-" in gid or "-pair_tool-" in gid:
            assert d["a"]["parts"]["request"] == d["b"]["parts"]["request"]
            assert {t["name"] for t in d["a"]["tools"]} ^ {t["name"] for t in d["b"]["tools"]}
        if "-pairD-" in gid:
            assert d["a"]["parts"]["request"] == d["b"]["parts"]["request"]
            assert (d["a"]["gold"], d["b"]["gold"]) == ("ANSWER", "CALL")


# ---- solver A: gold is a function of the structured record ------------------------------------------------------------
def test_every_gold_is_reproduced_from_the_structured_record(full):
    assert all(sa.gold_label(r) == r["gold"] for r in full)
    for r in full:
        assert [o["label"] for o in r["options"]].count(r["gold"]) == 1
        assert r["options"][ord(r["gold_letter"]) - 65]["label"] == r["gold"]


def _mini(sb="s1_need4", card=sa.STRICT, tools=None, intent=None, **kw):
    t0 = {"tid": "t0", "group": "g:get:x", "verb": "get", "entity": "x", "rw": "read", "idempotent": True, "name": "get_x",
          "params": [{"name": "x_id", "required": True, "default": None, "type": "str", "role": None}]}
    rec = dict(sub_block=sb, card=card, cards=[card], tools=tools if tools is not None else [t0], facts=[],
               intent=intent or dict(type="tool", target_group="g:get:x", args=[dict(param="x_id", required=True, value="v",
                                                                                        source="user_turn", default=None)]))
    rec.update(kw)
    return rec


def test_s1_rule_table_first_match_order():
    assert sa.gold_s1(_mini()) == "CALL"
    r = _mini(tools=[])                                                         # 1. target absent -> NO_TOOL
    assert sa.gold_s1(r) == "NO_TOOL"
    r = _mini(intent=dict(type="info", target_group="g:get:x", args=[], answer=dict(fact_id="f", where="context", value="1")),
              facts=[dict(fact_id="f", where="context")], tools=[])             # 2. info beats a missing tool
    assert sa.gold_s1(r) == "ANSWER"
    for strict, flip in ((sa.STRICT, "ASK"), (sa.DEFAULTS_OK, "CALL")):          # 3. the card decides the default
        r = _mini(card=strict, intent=dict(type="tool", target_group="g:get:x", args=[dict(
            param="x_id", required=True, value=None, source="none", default="dflt")]))
        assert sa.gold_s1(r) == flip
    r = _mini(intent=dict(type="tool", target_group="g:get:x", args=[dict(param="x_id", required=True, value=None, source="none",
                                                                          default=None)]), card=sa.DEFAULTS_OK)
    assert sa.gold_s1(r) == "ASK"                                               # no default declared: ask under either card
    r = _mini(intent=dict(type="tool", target_group="g:get:x", args=[dict(param="o", required=False, value=None, source="none",
                                                                          default=None)]))
    assert sa.gold_s1(r) == "CALL"                                              # an unsourced OPTIONAL parameter does not matter


def test_c1_answer_requires_a_locatable_span():
    r = _mini(intent=dict(type="info", target_group="g", args=[], answer=dict(fact_id="f9", where="context", value="1")),
              facts=[dict(fact_id="f1", where="context")])
    with pytest.raises(sa.SpecError):
        sa.gold_s1(r)
    r["facts"] = [dict(fact_id="f9", where="elsewhere")]
    with pytest.raises(sa.SpecError):
        sa.gold_s1(r)                                                           # "general knowledge" is not a location
    r["intent"]["answer"]["where"] = "elsewhere"
    with pytest.raises(sa.SpecError):
        sa.gold_s1(r)


def test_s3_order_no_tool_then_result_missing_then_ask_then_call():
    a = lambda src: dict(param="p", required=True, value=None, source=src, default=None)     # noqa: E731
    intent = lambda *args: dict(type="tool", target_group="g:get:x", args=list(args))        # noqa: E731
    assert sa.gold_s3(_mini("s3_limit", intent=intent(a("missing_result")))) == "RESULT_MISSING"
    assert sa.gold_s3(_mini("s3_limit", intent=intent(a("none")))) == "ASK"
    assert sa.gold_s3(_mini("s3_limit", intent=intent(a("prior_tool_output")))) == "CALL"
    assert sa.gold_s3(_mini("s3_limit", tools=[], intent=intent(a("missing_result")))) == "NO_TOOL"


def test_s3_label_follows_the_perturbation_in_every_row(full):
    want = {"perturb.del_tool": "NO_TOOL", "perturb.del_param": "ASK", "perturb.del_result": "RESULT_MISSING",
            "perturb.null_del": "CALL", "perturb.none": "CALL"}
    for r in full:
        if r["sub_block"] == "s3_limit":
            assert r["gold"] == want[r["perturb"]]


def test_s4_rule_table_enumerated():
    for state_, idem, has_read, args_ok in itertools.product(("observed_true", "observed_false", "unobserved"), (False, True),
                                                             (False, True), (False, True)):
        w = {"tid": "t0", "idempotent": idem}
        tools = [w] + ([{"tid": "tr", "idempotent": True}] if has_read else [])
        arg = dict(param="a", required=True, value="v" if args_ok else None, source="user_turn" if args_ok else "none", default=None)
        rec = _mini("s4_precond", tools=tools, intent=dict(type="tool", target_group="g", args=[arg]),
                    fact=dict(state=state_, write_tid="t0", read_tid="tr" if has_read else None))
        if state_ == "observed_true":
            want = "DONE_NO_CALL"
        elif state_ == "observed_false":
            want = "WRITE" if args_ok else "ASK"
        elif idem:
            want = "WRITE"
        else:
            want = "READ_FIRST" if has_read else "ASK"
        assert sa.gold_s4(rec) == want


def test_s5_provenance_rules():
    mk = lambda kind, card=sa.DEFAULTS_OK, **kw: _mini("s5_argground", card=card, call=dict(args=[dict(prov=dict(kind=kind, **kw))]),    # noqa: E731
                                                       declared_conversions=["kg_to_g"])
    assert sa.gold_s5(mk("user_turn")) == "GROUNDED" and sa.gold_s5(mk("prior_output_same_role")) == "GROUNDED"
    assert sa.gold_s5(mk("none")) == "UNGROUNDED" and sa.gold_s5(mk("wrong_role")) == "UNGROUNDED"
    assert sa.gold_s5(mk("card_default")) == "GROUNDED" and sa.gold_s5(mk("card_default", card=sa.STRICT)) == "UNGROUNDED"
    assert sa.gold_s5(mk("transform", base="user_turn", transform="case")) == "GROUNDED"
    assert sa.gold_s5(mk("transform", base="user_turn", transform="kg_to_g")) == "GROUNDED"        # declared by the card
    assert sa.gold_s5(mk("transform", base="user_turn", transform="km_to_m")) == "UNGROUNDED"      # not declared
    assert sa.gold_s5(mk("transform", base="none", transform="case")) == "UNGROUNDED"             # of an ungrounded base


def test_s5_rendering_matches_the_provenance_annotation(full):
    """Generator-side assertion that the context really contains (or lacks) each value as annotated."""
    for r in [x for x in full if x["sub_block"] == "s5_argground"][:300]:
        ctx = r["parts"]["user"] + "\n" + "\n".join(r["parts"]["outputs"])
        for a in r["call"]["args"]:
            k = a["prov"]["kind"]
            has = lambda v: re.search(r"(?<![\w-])%s(?![\w-])" % re.escape(v), ctx) is not None            # noqa: E731
            if k == "none" and a.get("edit_mode") == "swap":
                assert not has(a["value"])
            if k in ("user_turn", "prior_output_same_role"):
                assert has(a["value"])
            if k == "wrong_role":
                assert has(a["src_value"]) and ("%s: %s" % (a["param"], a["src_value"])) not in ctx


def test_s6_exactly_one_option_equals_the_ready_set_and_aliases_collapse(full):
    s6 = [r for r in full if r["sub_block"] == "s6_parseq"]
    for r in s6:
        want = sa.s6_canonical(r, sa.s6_ready_nodes(r))
        assert [tuple(o["canon"]) == want for o in r["options"]].count(True) == 1
        d = r["dag"]
        levels = dag.kahn_levels(*dag.remaining_dag(d["nodes"], [tuple(e) for e in d["edges"]], d["done"]))
        depth = dag.longest_path_levels(*dag.remaining_dag(d["nodes"], [tuple(e) for e in d["edges"]], d["done"]))
        assert sorted(levels[0]) == sorted(sa.s6_ready_nodes(r)) == sorted(n for n, k in depth.items() if k == 0)
    assert any(t["alias"] for r in s6 for t in r["dag"]["node_tools"])               # equivalence groups do occur


def test_s2_gold_is_the_unique_satisfying_tool(full):
    for r in [x for x in full if x["sub_block"] == "s2_pick"]:
        assert sum(1 for t in r["tools"] if sa.satisfies(t, r["intent"])) == 1
        assert r["gold"] == [t for t in r["tools"] if sa.satisfies(t, r["intent"])][0]["name"]
    r = [x for x in full if x["sub_block"] == "s2_pick"][0]
    r2 = copy.deepcopy(r)
    twin = next(t for t in r2["tools"] if t["tid"] == r2["intent"]["target_tid"])
    r2["tools"].append(dict(twin, tid="zz", name="dup_" + twin["name"]))              # a second satisfying tool: row rejected
    with pytest.raises(sa.SpecError):
        sa.gold_s2(r2)


# ---- renderer / names / determinism / safety ------------------------------------------------------------------------
def test_generation_is_deterministic():
    a = gen.generate_in_memory(total=200, seed="det")
    b = gen.generate_in_memory(total=200, seed="det")
    c = gen.generate_in_memory(total=200, seed="det2")
    sha = lambda rs: util.sha256_text(util.canon_json([(r["row_id"], r["gold"], r["rendered"]["text"]) for r in rs]))     # noqa: E731
    assert sha(a) == sha(b) and sha(a) != sha(c)


def test_production_mode_is_refused_until_namespace_has_the_noun_kinds():
    with pytest.raises(names.NamespaceError):
        gen.generate_in_memory(total=20, seed="prod", standin=False)


def test_no_row_is_written_to_disk(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    recs, summary = t54_dryrun.run(20)
    assert len(recs) >= 18 and summary["written_to_disk"] is False and list(tmp_path.iterdir()) == []
    with pytest.raises(ValueError):
        t54_dryrun.run(t54_dryrun.MAX_DRY + 1)


def test_the_only_file_reads_are_the_manifest_and_namespace():
    here = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    for fn in os.listdir(here):
        if fn.endswith(".py") and fn.startswith("t54_"):
            src = open(os.path.join(here, fn)).read()
            assert "open(" not in src and "os.walk" not in src and "glob" not in src, fn


def test_every_name_is_on_the_frozen_allow_list_and_the_row_start_guard_accepts_the_job(full):
    assert gates.p13_names(full, AL)["ok"]
    guard_path = os.path.join(names.INFRA_DIR, "row_start_guard.py")
    spec = importlib.util.spec_from_file_location("od_row_start_guard", guard_path)
    guard = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(guard)
    allow = {c: set(AL.union[c]) for c in names.CATEGORIES}
    manifest = names.job_manifest("T54", full)
    assert guard.check_names(manifest["names"], allow, "job") == []
    bad = copy.deepcopy(manifest["names"])
    bad["tool"].append("verb.not_listed")
    assert guard.check_names(bad, allow, "job")
    assert gates.gc.name_guard_gate("g", [dict(row_id="r", names=dict(tool=["param.status"]), rendered=dict(text=""))], AL, "T56")["ok"] is False


def test_rendered_rows_have_the_view_tag_and_no_instruction_text_in_outputs(full):
    assert gates.p14_output_lint(full)["ok"]
    for r in full:
        assert (r["view"] == "view.with_outputs") == (r["sub_block"] in ("s3_limit", "s4_precond", "s5_argground"))
        if r["view"] == "view.primary":
            assert "-> output" not in r["rendered"]["text"]
    assert render.lint_output("detail: you should call the tool")


# ---- gates (PRE-FREEZE, CPU) ----------------------------------------------------------------------------------------
def test_all_non_probe_gates_pass_except_the_seed_wording_pool(pilot):
    failing = [r["id"] for r in gates.run_all(pilot, allowlist=AL) if not r["ok"]]
    assert set(failing) <= {"P-11:wording"}, failing


def test_full_size_gates_pass_except_the_seed_wording_pool(full):
    failing = [r["id"] for r in gates.run_all(full, allowlist=AL) if not r["ok"]]
    assert set(failing) <= {"P-11:wording"}, failing


def test_seed_wording_pool_fails_the_wording_gate_as_it_should(full):
    w = [r for r in gates.p11_wording(full) if r["id"] == "P-11:wording"][0]
    assert w["ok"] is False and w["forms_below_min"] > 0


def test_probe_wiring_on_a_clean_sample_stays_near_chance(full):
    h = StubHarness(repeats=3)
    for res in gates.p5a_request_only(full, h) + gates.p5b_toollist_card(full, h):
        assert res["auc"] < 0.60, res
    assert gates.p5e_s2_options(full, h)["bacc"] < 0.31


def test_probe_power_a_planted_request_leak_is_caught(full):
    leaked = copy.deepcopy([r for r in full if r["sub_block"] == "s1_need4"])
    for r in leaked:
        r["parts"]["request"] += " zqxjv" if r["call_bearing"] else " plmkn"
    res = gates.p5a_request_only(leaked, StubHarness(repeats=3))[0]
    assert res["auc"] > 0.9 and not res["ok"]


def test_nbin_shares_hit_the_family_targets(full):
    r = gates.p9_distractors(full)
    assert all(x["ok"] for x in r), r


def test_span_totals_are_label_independent(full):
    assert all(x["ok"] for x in gates.p6_value_spans(full))
    assert all(r["user_spans"] == r["span_total"] for r in full if r["sub_block"] != "s6_parseq")


def test_solver_b_agreement_hook_flags_and_drops(pilot):
    flip = lambda r: "X" if r["row_id"].endswith("-s") else r["gold"]                # noqa: E731
    res = gates.p1_agreement(pilot, flip)
    assert not res["ok"] and res["dropped_ids"]
    assert gates.p1_agreement(pilot, lambda r: r["gold"])["ok"]


def test_balanced_gold_positions_per_n(full):
    assert gates.p7_letters_positions(full)[0]["ok"] and gates.p7_letters_positions(full)[-1]["ok"]


def test_declared_default_visibility_only_in_card_pairs(full):
    for r in full:
        shown = any(p.get("default") is not None for t in r["tools"] for p in t["params"])
        if r["sub_block"] == "s1_need4" and r["entry"] != "pairC":
            assert not shown


def test_g10_decision_spans_roles_offsets_and_authority(full):
    for r in full[:600]:
        ds = r["decision_spans"]
        text = r["parts"]["user"]
        last = 0
        for sp in ds["spans"]:
            assert text[sp["start"]:sp["end"]] == sp["text"] and sp["start"] >= last and sp["role"] in render.ROLES_G10
            last = sp["end"]
        for a in r["intent"].get("args", []):
            if a.get("source") == "user_turn" and a.get("value") and r["sub_block"] != "s5_argground":
                assert any(sp["role"] == "authority" and sp["text"] == a["value"] for sp in ds["spans"]) or a["value"].strip('"') not in text
