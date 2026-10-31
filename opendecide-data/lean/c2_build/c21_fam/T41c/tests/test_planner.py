"""Spec planner: quotas, pair groups, stratum, held-out, dev blocks."""
import collections

import pytest

from t41c import gates, ids, planner
from t41c.spec import Pointer, label_of, spec_from_json, spec_to_json, validate_spec


def test_label_counts_and_subtypes_exact(plan2000):
    c = planner.bucket_counts(2000)
    assert collections.Counter(s.subtype for s in plan2000) == collections.Counter(c)
    assert collections.Counter(label_of(s) for s in plan2000) == {"ALLOW": 300, "ALLOW_BENIGN": 700, "BLOCK": 700, "ASK": 300}


def test_every_planned_label_is_the_tables_label(plan2000):
    for s in plan2000:
        assert label_of(s) == planner.BUCKET_LABEL[s.subtype]


def test_bucket_counts_n3000():
    c = planner.bucket_counts(3000)
    assert sum(c.values()) == 3000 and c["sub.clean_twin"] == 270 and c["ask.nested"] == 150


def test_k4_and_k5_pass_at_both_sizes(plan2000):
    r = gates.gate_k4(plan2000, 2000)
    assert r["pass"], r["fails"]
    specs3, _ = planner.plan_specs(3000)
    assert gates.gate_k4(specs3, 3000)["pass"]
    assert gates.gate_k5(plan2000)["pass"]
    assert gates.gate_k5(specs3)["pass"]


def test_pair_share_policy_multi_and_stratum(plan2000):
    n = len(plan2000)
    assert sum(s.pair_kind != "single" for s in plan2000) / n == pytest.approx(0.60, abs=0.01)
    assert sum(s.declared_policy_file for s in plan2000) / n == pytest.approx(0.04, abs=0.003)
    multi = sum(len(s.directives) >= 2 for s in plan2000) / n
    assert 0.10 <= multi <= 0.14
    assert sum(not s.facts.present for s in plan2000) / n == pytest.approx(planner.FACTS_ABSENT_SHARE, abs=0.005)


def test_facts_absent_share_in_every_label_carrier_and_subtype_cell_R2d(plan2000):
    cells = collections.defaultdict(lambda: [0, 0])
    for s in plan2000:
        for key in (("l", label_of(s)), ("c", s.carrier_type), ("s", s.subtype)):
            cells[key][0] += 1
            cells[key][1] += not s.facts.present
    assert len(cells) == 4 + 12 + 12
    for key, (n, a) in cells.items():
        assert abs(a / n - planner.FACTS_ABSENT_SHARE) <= 0.02, key
        assert a / n >= 0.25, key


def test_delegated_high_rows_at_least_8_percent(plan2000):
    from t41c.table import HARD, risk
    n = 0
    for s in plan2000:
        env = s.env()
        if any(d.agent_directed and s.pointer.covers(d.did) and risk(d.action, env) == HARD for d in s.directives):
            n += 1
    assert n / len(plan2000) >= 0.08


def test_all_specs_valid_and_unique_ids(plan2000):
    assert all(not validate_spec(s) for s in plan2000)
    assert len({s.row_id for s in plan2000}) == len(plan2000)


def test_groups_shapes(plan2000):
    by = collections.defaultdict(list)
    for s in plan2000:
        by[s.group_id].append(s)
    kinds = collections.Counter()
    for g, ms in by.items():
        kinds[(ms[0].pair_kind, len(ms))] += 1
        assert len({m.art_seed for m in ms}) == 1
        assert len({(m.carrier_type, m.carrier_format, m.len_target) for m in ms}) == 1
    assert set(kinds) <= {("single", 1), ("triple", 3), ("splice", 2), ("taskedit", 2)}
    triples = [ms for ms in by.values() if ms[0].pair_kind == "triple"]
    for ms in triples:
        assert sorted(label_of(m) == "ALLOW" for m in ms) == [False, False, True]
        assert {m.pair_role for m in ms} == {"clean", "benign", "attack"}


def test_taskedit_pairs_share_the_directive_and_flip_by_user_turn_only(plan2000):
    by = collections.defaultdict(list)
    for s in plan2000:
        if s.pair_kind == "taskedit":
            by[s.group_id].append(s)
    assert by
    for ms in by.values():
        a, b = ms
        assert a.directives == b.directives and a.carrier_type == b.carrier_type and a.facts.present == b.facts.present
        assert (a.task_class, a.pointer) != (b.task_class, b.pointer)
        assert label_of(a) != label_of(b)


def test_minimal_pair_members_share_slot_attributes(plan2000):
    by = collections.defaultdict(list)
    for s in plan2000:
        if s.pair_kind in ("triple", "splice"):
            by[s.group_id].append(s)
    for ms in by.values():
        sig = set()
        for m in ms:
            slot = (m.directives[0] if m.directives else m.fills[0])
            sig.add((slot.wrapper, getattr(slot, "hidden", None), slot.placement, slot.visibility, slot.chunks,
                     getattr(slot, "slot_bucket", getattr(slot, "bucket", None)), m.vendor_slot, m.has_nested_span,
                     m.task_class, m.pointer, m.task_mentions, m.facts))
        assert len(sig) == 1


def test_heldout_draw_is_seeded_and_complete(heldout):
    again = planner.draw_heldout()
    assert heldout == again
    assert len(heldout["wrappers"]) == 2 and len(heldout["goals"]) == 2
    assert len(heldout["formats"]) == 1 and len(heldout["placements"]) == 1
    assert set(heldout["wrappers"]) <= set(ids.WRAPPERS) and set(heldout["goals"]) <= set(ids.GOAL_CLASSES)


def test_training_rows_carry_no_heldout_value(plan2000, heldout):
    for s in plan2000:
        slots = list(s.directives) + list(s.fills)
        assert all(x.wrapper not in heldout["wrappers"] for x in slots)
        assert all(x.placement not in heldout["placements"] for x in slots)
        assert s.carrier_format not in heldout["formats"]
        assert all(d.cls not in heldout["goals"] for d in s.directives)


def test_format_rule_each_format_in_3_carriers_each_carrier_in_2_formats():
    per_fmt = collections.Counter(f for fs in ids.CARRIER_FORMATS.values() for f in fs)
    assert all(per_fmt[f] >= 3 for f in ids.FORMATS)
    assert all(len(fs) >= 2 for fs in ids.CARRIER_FORMATS.values())
    for ct, fs in ids.CARRIER_FORMATS.items():          # holding out any one format leaves every carrier a format
        for f in ids.FORMATS:
            assert [x for x in fs if x != f]


def test_heldout_block_has_80_per_value_one_value_per_row(heldout, ho_built):
    specs, rows, brep = ho_built
    assert len(specs) == 480
    cnt = collections.Counter()
    for s in specs:
        vals = set()
        slots = list(s.directives) + list(s.fills)
        for x in slots:
            if x.wrapper in heldout["wrappers"]:
                vals.add(("wrapper", x.wrapper))
            if x.placement in heldout["placements"]:
                vals.add(("placement", x.placement))
        if s.carrier_format in heldout["formats"]:
            vals.add(("format", s.carrier_format))
        for d in s.directives:
            if d.cls in heldout["goals"]:
                vals.add(("goal", d.cls))
        assert len(vals) == 1, (s.row_id, vals)
        cnt[next(iter(vals))] += 1
    assert len(cnt) == 6 and all(v == 80 for v in cnt.values())
    assert all(s.block == "ho" for s in specs)


def test_benign_dev_block(heldout):
    specs, _ = planner.plan_benign_dev(heldout=heldout)
    assert len(specs) == 400
    c = collections.Counter(label_of(s) for s in specs)
    assert c == {"ALLOW": 100, "ALLOW_BENIGN": 300}
    assert all(s.block == "bd" for s in specs)
    sub = collections.Counter(s.subtype for s in specs if label_of(s) == "ALLOW_BENIGN")
    tot = sum(sub.values())
    assert sub["sub.delegated"] / tot == pytest.approx(14 / 35, abs=0.01)
    assert sub["sub.trigger_security"] / tot == pytest.approx(5 / 35, abs=0.01)


def test_long_slice_block(heldout):
    specs, _ = planner.plan_long_slice(heldout=heldout)
    assert len(specs) == 150 and all(s.len_target == 3 and s.block == "ls" for s in specs)
    assert sum(label_of(s) in ("ALLOW", "ALLOW_BENIGN") for s in specs) == 75


def test_blocks_use_disjoint_ids_and_groups(heldout):
    tr, _ = planner.plan_specs(200, heldout=heldout)
    bd, _ = planner.plan_benign_dev(60, heldout=heldout)
    ho, _ = planner.plan_heldout(10, heldout=heldout)
    ids_ = [s.row_id for s in tr + bd + ho]
    assert len(set(ids_)) == len(ids_)
    g = {b: {s.group_id for s in blk} for b, blk in (("tr", tr), ("bd", bd), ("ho", ho))}
    assert not (g["tr"] & g["bd"]) and not (g["tr"] & g["ho"]) and not (g["bd"] & g["ho"])
    assert not ({s.art_seed for s in tr} & {s.art_seed for s in bd})


def test_plan_is_deterministic_and_seed_sensitive(heldout):
    a, _ = planner.plan_specs(120, seed="x", heldout=heldout)
    b, _ = planner.plan_specs(120, seed="x", heldout=heldout)
    c, _ = planner.plan_specs(120, seed="y", heldout=heldout)
    assert [spec_to_json(s) for s in a] == [spec_to_json(s) for s in b]
    assert [spec_to_json(s) for s in a] != [spec_to_json(s) for s in c]


def test_spec_json_round_trip(plan2000):
    for s in plan2000[::50]:
        assert spec_from_json(spec_to_json(s)) == s


def test_validate_spec_catches_structure_errors(plan2000):
    from dataclasses import replace
    s = plan2000[5]
    assert validate_spec(replace(s, carrier_format="fmt.toml", carrier_type="car.readme"))
    assert validate_spec(replace(s, task_class="task.nope"))
    d = next(x for x in plan2000 if x.directives and x.directives[0].agent_directed)
    bad = replace(d, directives=(replace(d.directives[0], action=None),))
    assert validate_spec(bad)
    shared = replace(d.directives[0].action, shared_prod=True)
    assert validate_spec(replace(d, directives=(replace(d.directives[0], action=shared),),
                                 facts=replace(d.facts, lane_tag=False)))
    assert validate_spec(replace(d, len_target=3))                      # 3 is the LS block only


def test_pointer_covers():
    assert not Pointer().covers("d0")
    assert not Pointer("deleg.source_pointer", False).covers("d0")
    assert Pointer("deleg.source_pointer", True).covers("d9")
    assert Pointer("deleg.step_pointer", True, ("d0",)).covers("d0")
    assert not Pointer("deleg.step_pointer", True, ("d0",)).covers("d1")


def test_every_ben_class_is_necessary_somewhere_and_every_task_has_a_step():
    nec = {c for t in ids.NECESSARY_STEPS.values() for c in t}
    assert nec == set(ids.BENIGN_CLASSES)
    assert all(ids.NECESSARY_STEPS[t] for t in ids.TASK_CLASSES)


def test_lane_tag_only_with_shared_prod_directives(plan2000):
    for s in plan2000:
        for d in s.directives:
            if d.agent_directed and d.action.shared_prod:
                assert s.facts.lane_tag
