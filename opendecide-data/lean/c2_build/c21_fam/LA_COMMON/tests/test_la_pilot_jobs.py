import collections

import row_start_guard as guard
from LA_COMMON import MANIFEST_PATH
from LA_COMMON.canon import sha_file
from LA_COMMON.names import build_job_manifest
from LA_COMMON.pilot import pilot_cells


def test_pilot_sample_is_proportional_whole_cells_and_deterministic():
    from T50 import blocks
    cells = blocks.plan()
    rows = lambda c: len(blocks.cell_rows(c))
    a = pilot_cells(cells, rows, lambda c: c.block, lambda c: c.sub)
    b = pilot_cells(cells, rows, lambda c: c.block, lambda c: c.sub)
    assert [c.extras["idx"] for c in a] == [c.extras["idx"] for c in b]
    n = sum(rows(c) for c in a)
    assert 980 <= n <= 1100
    share = collections.Counter()
    for c in a:
        share[c.block] += rows(c)
    for blk, want in blocks.BLOCK_ROWS.items():
        w = sum(want.values()) / 4000.0
        assert abs(share[blk] / n - w) < 0.04, (blk, share[blk] / n, w)


def _manifest_ok(family, specs, used_ids):
    from LA_COMMON.names import get_allowlist
    man = build_job_manifest("dry-%s" % family, family, [(s.spec_id, used_ids(s)) for s in specs])
    allow, sha, why = guard.load_allowlist(MANIFEST_PATH, sha_file(MANIFEST_PATH))
    assert not why
    assert guard.check_names(man["names"], allow) == []
    for r in man["rows"]:
        assert guard.check_names(r["names"], allow) == []
    return man


def test_dry_run_job_manifests_pass_the_row_start_guard_name_check_for_all_three_families():
    import T50.dryrun, T51.dryrun, T53.dryrun
    from T50.gates import used_ids as u50
    from T51.gates import used_ids as u51
    from T53.gates import used_ids as u53
    assert len(_manifest_ok("T50", T50.dryrun.build_dry()[0], u50)["rows"]) >= 20
    assert len(_manifest_ok("T51", T51.dryrun.build_dry()[0], u51)["rows"]) >= 19
    assert len(_manifest_ok("T53", T53.dryrun.build_dry()[0], u53)["rows"]) == 20
