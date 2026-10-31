"""K2 on the lane generator, in memory (no rows written anywhere): solver A gold vs solver B on the whole v3.1 plan."""
import collections

from T50.solver_b.agree import generate_specs, make_rowview, run
from T50.solver_b.t50_b import label_row


def test_agreement_full_plan_seed0():
    specs, led = generate_specs()
    stats, classes, dis = run(specs, label_row)
    n = stats["rows"]
    assert n >= 4000 and led.count() == 0
    assert stats["label_agree"] / n >= 0.99                     # K2 bar (>= 99.0%)
    assert stats["triple_agree"] / n >= 0.99


def test_every_rendering_of_a_spec_gets_the_same_b_label():
    specs, _ = generate_specs()
    for s in specs[:600]:
        labs = {tuple(label_row(make_rowview(s, r))[k] for k in ("label", "reason", "tier")) for r in s.renderings
                if r.get("roundtrip", True)}
        assert len(labs) <= 1, s.spec_id


def test_b_never_reads_gold_fields():
    specs, _ = generate_specs()
    s = specs[0]
    rv = make_rowview(s, s.renderings[0])
    assert not (set(rv) & {"gold", "effects", "rule_ids", "intent", "meta", "fact_visibility", "decision_spans"})
