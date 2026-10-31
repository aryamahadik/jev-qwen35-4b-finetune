"""K7 on the lane generator, in memory: solver A gold vs solver B on the whole v3.1 plan (2 seeds)."""
import collections

from T53.solver_b.agree import compare, generate
from T53.solver_b.t53_b import label_row


def test_agreement_two_seeds():
    stats, classes, factcls = collections.Counter(), collections.Counter(), collections.Counter()
    for k in range(2):
        specs, drops = generate(k * 100000)
        assert not drops
        compare(specs, label_row, stats, classes, factcls)
    n = stats["rows"]
    assert n >= 4000
    assert stats["label_agree"] / n >= 0.99                       # K7 label bar
    # the only label-disagreement class is the plain-http transport defect that scp / nc renderings cannot show
    assert set(k[0] for k in classes) <= {"b", "ask_transport"}
    for k in classes:
        assert k[2][0] == "ASK" and k[3][0] == "ALLOW"
