"""K1 on the lane generator, in memory: solver A gold vs solver B on the whole v3.1 plan (2 seeds)."""
import collections

from T51.solver_b.agree import compare, generate
from T51.solver_b.t51_b import label_row


def test_agreement_two_seeds():
    stats, classes, factcls = collections.Counter(), collections.Counter(), collections.Counter()
    for k in range(2):
        specs, drops = generate(k * 100000)
        assert not drops
        compare(specs, label_row, stats, classes, factcls)
    n = stats["rows"]
    assert n >= 7000
    assert stats["label_agree"] / n >= 0.99                       # K1 bar
    assert stats["traj_consistent"] == stats["traj_consistent_rows"]
    assert stats["excl_consistent"] == stats["excl_consistent_rows"]
