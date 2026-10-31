"""Build-skeptic tests (Sun 18 Oct): the B-view hides the block id and the member letters; head rows count real tokens and pass the full row checks;
P-d decorations do not make firewall / IAM kinds an ALLOW-only cue."""
import collections

import pytest

from LP_COMMON import pipeline as pl
from LP_COMMON import tokens
from T67 import checked, dryrun, gates, heads, schema, sqlmodel as SQ


@pytest.fixture(scope="module")
def dry():
    return dryrun.dry_rows(300, seed=17)[0]


def test_b_view_has_no_block_id_and_an_opaque_row_id(dry):
    seen = set()
    for r in dry:
        bv = schema.b_view(r)
        assert bv["sub_block"] == r["witness_inputs"]["carrier"]
        assert bv["row_id"] != r["row_id"]
        outside_text = str({k: v for k, v in bv.items() if k != "rendered"})
        assert "'" + r["sub_block"] + "'" not in outside_text         # block ids such as P-d never appear in the view fields B reads
        seen.add(r["sub_block"])
    assert {"P-d", "P-e"} & seen        # the all-ALLOW / all-BLOCK blocks are present in the sample


def test_all_one_label_blocks_exist_which_is_why_the_block_id_is_not_a_b_input(dry):
    by = collections.defaultdict(set)
    for r in dry:
        if r["head"] == "T67-GATE":
            by[r["sub_block"]].add(r["gold"])
    assert by["P-d"] == {"ALLOW"} and by["P-e"] == {"BLOCK"} and by["K-d"] == {"ALLOW"} and by["C-d"] == {"ALLOW"}


def test_head_rows_meta_tokens_use_the_family_counter(dry):
    hs = [r for r in dry if r.get("head_row")]
    assert hs
    for r in hs:
        assert r["meta"]["tokens"] == tokens.count(r["rendered"]["text"])


def test_head_rows_run_through_check_row(dry):
    ad = checked.adapter(checked.generator.Ctx(seed=1, standin=True).lock_table)
    hs = [r for r in dry if r.get("head_row")][:20]
    for r in hs:
        why, _ = pl.check_row(r, ad)
        assert why == [], (r["row_id"], why)
    bad = dict(hs[0], names=dict(hs[0]["names"], carrier=hs[0]["names"]["carrier"] + ["NOT_A_CARRIER"]))
    assert "names_off_allowlist" in pl.check_row(bad, ad)[0]


def test_firewall_and_iam_kinds_are_not_allow_only(dry):
    c = collections.defaultdict(collections.Counter)
    rows = [r for r in dryrun.dry_rows(500, seed=3)[0] if r["head"] == "T67-GATE"]
    for r in rows:
        for it in r["spec"].get("items", []):
            c[it["kind"]][r["gold"]] += 1
    # a kind that occurs only inside quiet decorations of ALLOW rows would teach "firewall / IAM items are safe"
    for kind in ("firewall_rule", "iam_policy"):
        assert sum(c[kind].values()) == 0 or len(c[kind]) > 1, (kind, dict(c[kind]))
    worst = gates.k3_surface(rows, B=200)[-1]["worst"]
    assert "firewall_rule" not in worst and "iam_policy" not in worst


def test_pool_guard_accepts_the_shipped_pool_and_refuses_an_operation_word_in_a_form_that_must_not_name_it():
    import json
    import os
    from T67 import generator as G, userturn as UT
    from LP_COMMON import wording
    pool = json.load(open(os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "pools", "wording_pool.json")))
    assert G.pool_problems(pool) == []
    bad = json.loads(json.dumps(pool))
    bad["forms"]["T67-U-NEITHER"].append({"id": "wx", "text": "Please go ahead and delete whatever is proposed."})
    assert any("must not name the operation" in p for p in G.pool_problems(bad))
    bad2 = json.loads(json.dumps(pool))
    bad2["forms"]["T67-U-TARGET"].append({"id": "wy", "text": "Please {target}, and make public."})
    assert any("must not name the operation" in p for p in G.pool_problems(bad2))
    with pytest.raises(wording.PoolError):
        G.Ctx(seed=1, standin=False, pool=bad, lock_table=SQ.draft_lock_table())          # the pool is checked before the lock table

