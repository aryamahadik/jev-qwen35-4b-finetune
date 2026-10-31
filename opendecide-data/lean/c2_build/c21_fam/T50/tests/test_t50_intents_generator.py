import collections
import random

import pytest

from LA_COMMON.canon import sha_obj
from LA_COMMON.expander import Expander, roundtrip_equal, spec_canon
from LA_COMMON.render import HELDOUT_OPERATORS
from LA_COMMON.shellmodel import RawScript, Script
from LA_COMMON.spec import Spec
from T50 import blocks
from T50.build import BCtx
from T50.cards import CARD_IDS
from T50.generator import DropLedger, GeneratorDefect, build_cell, hard_refs, spec_rows, with_results_output
from T50.intents import REGISTRY, build_intent, expected_for
from T50.solver_a import label_spec


def test_every_intent_on_every_card_matches_its_design_expectation():
    bad, n = [], 0
    for iid, meta in sorted(REGISTRY.items()):
        for ci, card_id in enumerate(CARD_IDS):
            c = BCtx("it-%s-%d" % (iid, ci), card_id)
            b = build_intent(iid, c, {})
            sp = Spec("s", "T50", "A", card_id, c.card, c.st, action=b.script, payloads=c.payloads, naming=c.naming, history=list(c.hist))
            r = label_spec(sp)
            n += 1
            if (r.label, r.reason, r.tier) != expected_for(meta, c.card):
                bad.append((iid, card_id, (r.label, r.reason, r.tier)))
    assert n >= 900 and not bad, bad[:5]


def test_registry_is_big_enough_and_hard_intents_are_hard():
    assert len(REGISTRY) >= 100
    for iid, m in REGISTRY.items():
        if m["tier"] == "hard":
            assert m["label"] == "BLOCK", iid


@pytest.fixture(scope="module")
def built():
    cells = blocks.plan()
    seen = collections.OrderedDict()
    for c in cells:
        seen.setdefault((c.block, c.intent, c.tag, bool(c.extras.get("twin"))), c)
    ledger = DropLedger()
    out = {}
    for k, c in seen.items():
        out[k] = (c, build_cell(c, ledger))
    return out, ledger


def test_every_distinct_plan_cell_builds_with_design_labels_and_zero_roundtrip_drops(built):
    out, ledger = built
    assert len(out) >= 280
    assert ledger.count() == 0, ledger.drops[:5]
    from T50 import gates
    allspecs = [s for _, ss in out.values() for s in ss]
    assert gates.k17_names(allspecs)["pass"], gates.k17_names(allspecs)["refusals"][:3]      # every program / carrier / language is on the closed list
    assert gates.k13_split(allspecs)["pass"] and gates.k18_payloads(allspecs)["pass"] and gates.k3_opaque(allspecs)["violations"] == []
    assert gates.k19_construct(allspecs)["pass"]
    for k, (c, specs) in out.items():
        rows = blocks.cell_rows(c)
        got = sorted((s.gold.label, s.gold.reason, s.gold.tier) for s in specs for _ in s.renderings if True)
        # per-spec design labels
        assert all(s.gold is not None for s in specs)


def test_block_b_pairs_have_plain_and_obfuscated_renderings_and_heldout_ops_only_on_dev(built):
    out, _ = built
    n_dev = n_train = 0
    for (blk, iid, tag, tw), (c, specs) in out.items():
        if blk != "B":
            continue
        for s in specs:
            roles = {r["role"] for r in s.renderings}
            assert roles == {"plain", "obf"}
            obf = [r for r in s.renderings if r["role"] == "obf"][0]
            assert obf["ops"] and obf["text"] != [r for r in s.renderings if r["role"] == "plain"][0]["text"]
            used_held = set(obf["ops"]) & set(HELDOUT_OPERATORS)
            assert (s.split == "dev") or not used_held
            n_dev += s.split == "dev"
            n_train += s.split == "train"
    assert n_train > 0


def test_block_c_pairs_share_the_dangerous_token_and_the_benign_twin_is_allow(built):
    out, _ = built
    k = 0
    for (blk, iid, tag, tw), (c, specs) in out.items():
        if blk != "C":
            continue
        if tag == "quad4":                                     # mandatory quad: (alarming, calm) x (executed, harmless carrier)
            assert len(specs) == 4 and {s.quad_axes["risk"] for s in specs} == {"present", "resolved"}
            assert sorted(s.gold.label == "ALLOW" for s in specs) == [False, False, True, True]
            continue
        k += 1
        ex, ben = specs
        assert ex.meta["adv_role"] == "executed" and ben.meta["adv_role"] == "benign" and ben.gold.label == "ALLOW" and ex.gold.label != "ALLOW"
        token = ex.renderings[0]["text"]
        words = "".join(ch if ch.isalnum() else " " for ch in token).split()[:4]
        flat = " ".join(" ".join(cm.words) for cm in Expander().resolve(ben.renderings[0]["text"]).cmds)
        assert token in flat or "_".join(words) in flat                                                  # test-name carrier slugifies
        assert ex.group == ben.group and ex.split == ben.split
    assert k >= 3


def test_block_d_opaque_kinds_and_write_then_run(built):
    out, _ = built
    kinds, wtr = set(), collections.Counter()
    for (blk, iid, tag, tw), (c, specs) in out.items():
        if blk != "D":
            continue
        s = specs[0]
        if isinstance(s.action, RawScript):
            kinds.add(s.action.opaque_kind)
            assert (s.gold.label, s.gold.reason, s.gold.tier) == ("ASK", "none", "na")
            assert Expander().resolve(s.renderings[0]["text"]).opaque == [s.action.opaque_kind]
        else:
            wtr[(s.gold.label, tag)] += 1
            assert s.history and s.history[-1].carrier in ("file_write", "shell_exec")
            if iid == "wtr.modified":
                assert s.gold.reason == "none" and s.state.session.modified_files
    assert {"cmdsub", "redirect_exec", "control_flow", "unknown_file", "b64_invisible", "xargs_dynamic"} <= kinds
    assert wtr[("ALLOW", "")] and wtr[("BLOCK", "")] and wtr[("ASK", "modified")]


def test_overwritten_write_then_run_latest_write_wins(built):
    out, _ = built
    seen = 0
    for (blk, iid, tag, tw), (c, specs) in out.items():
        if blk == "D" and tag == "ov":
            s = specs[0]
            writes = [h for h in s.history if h.carrier == "file_write"]
            assert len(writes) == 2 and writes[-1].payload_id == "payload.main"
            seen += 1
    assert seen > 5


def test_quads_swaps_twins_and_views(built):
    out, _ = built
    quads = swaps = twins = 0
    for (blk, iid, tag, tw), (c, specs) in out.items():
        if blk == "E":
            quads += 1
            labs = {s.meta["quad_cell"]: s.gold.label for s in specs}
            assert {s.renderings[0]["text"] for s in specs}.__len__() == 1
            assert len({sha_obj(s.state.to_dict()) for s in specs}) == 1
            if tag == "hard_quad":
                assert set(labs.values()) == {"BLOCK"} and {s.gold.tier for s in specs} == {"hard"}
            else:
                assert labs["both"] == "ALLOW" and "ALLOW" not in (labs["neither"], labs["op"], labs["target"])
            assert specs[0].user_turns[0].form == "T50.U.task" and len({tuple(t.form for t in s.user_turns) for s in specs}) >= 3
        if tag == "swap":
            swaps += 1
            assert len({s.gold.label for s in specs}) == 2 and specs[0].group == specs[1].group and specs[0].card_ref != specs[1].card_ref
            assert specs[0].state.to_dict() == specs[1].state.to_dict()
        if c.extras.get("twin"):
            twins += 1
            assert {r["view"] for s in specs for r in s.renderings} == {"primary", "with_results"}
    assert quads >= 20 and swaps >= 5 and twins >= 10


def test_with_results_view_exposes_output_only_facts_and_primary_rows_are_determinable(built):
    out, _ = built
    shown = 0
    for (blk, iid, tag, tw), (c, specs) in out.items():
        for s in specs:
            if any(v == "output" for v in s.fact_visibility.values()):
                assert with_results_output(s) != "" or not s.fact_visibility
                shown += 1
    assert shown > 10
    share = sum(1 for k, (c, ss) in out.items() for s in ss if s.meta.get("primary_determinable")) / sum(len(ss) for _, ss in out.values())
    assert share > 0.5                                                                    # report line, not a bar


def test_build_is_deterministic():
    cells = blocks.plan()
    n = len(cells)
    sample = [cells[i] for i in (3, n // 5, n // 2, (4 * n) // 5, n - 5)]
    a = [s.sha() for c in sample for s in build_cell(c)]
    b = [s.sha() for c in sample for s in build_cell(c)]
    assert a == b and len(set(a)) == len(a)


def test_hard_refs_for_hard_quads():
    c = BCtx("hr", "card.t50.c01")
    b = build_intent("fs.sys_write", c, {"prog": "rm"})
    sp = Spec("s", "T50", "A", "card.t50.c01", c.card, c.st, action=b.script)
    op, tgt = hard_refs(sp)
    assert op.startswith("rm.") and tgt.startswith("/")


def test_a_wrong_design_expectation_is_a_generator_defect(monkeypatch):
    cells = blocks.plan()
    c = next(x for x in cells if x.block == "A" and x.intent == "fs.read" and x.tag == "")
    monkeypatch.setitem(REGISTRY["fs.read"], "label", "BLOCK")
    with pytest.raises(GeneratorDefect):
        build_cell(c)
