"""Shared CPU-test helpers for the L-R mappers. In-memory records only; no row file is ever written."""
import os

import pytest

import lr_common as lc


def check_rows(rows, mapper, expect_kind=None, min_rows=1):
    """Generic per-row asserts (R4 re-run, R5, R6, R12, flags). `mapper` supplies independent_gold only for R4 via map."""
    assert len(rows) >= min_rows, "mapper produced too few rows: %d (drops %s)" % (len(rows), mapper.drops.c)
    for r in rows:
        assert r["schema"] == lc.SCHEMA and r["source"] == "L-R" and r["source_split"] == "train"
        assert r["options"][r["label"]] == r["answer_text"]
        assert r["label_letter"] == lc.LETTERS[r["label"]]
        norm = [lc.normalise_ws(o) for o in r["options"]]
        assert len(set(norm)) == len(norm), "duplicate options"
        assert norm.count(lc.normalise_ws(r["answer_text"])) == 1, "gold not exactly once"
        assert r["k"] == len(r["options"]) >= 2
        assert r["tokens_est"] <= lc.TOKEN_ROW_MAX
        assert lc.r12_guard(lc.render_plain(r), skip=tuple(mapper.META.get("r12_skip", ()))) is None
        assert r["flags"]["train_split_seen"] is True
        assert r["flags"]["share_alike"] == bool(mapper.META.get("share_alike"))
        assert r["recast_table_sha"] == mapper.table_sha
        assert r["lr_id"] == mapper.META["lr_id"] and r["family"] == mapper.META["family"]
        assert r["stem"].strip()
        if expect_kind:
            assert r["kind"] in expect_kind
    return True


def pools_for(mapper_cls):
    return lc.WordingPools.placeholder_pools(mapper_cls.FORMS)


def check_dry_run_refusal(mapper_cls):
    """A non-dry run must be refused without the guard's exports and a signed conformance record."""
    saved = {k: v for k, v in os.environ.items() if k.startswith("OD_ROWGUARD_") or k == "LR_CONFORMANCE_RECORD"}
    for k in saved:
        del os.environ[k]
    try:
        with pytest.raises(lc.RowStartRefused):
            mapper_cls(lc.WordingPools({}, placeholder=False), dry_run=False)
    finally:
        os.environ.update(saved)


def check_set_report(rows, yes_no=False):
    rep = lc.set_report(rows, yes_no=yes_no)
    assert rep["n"] == len(rows)
    assert rep["exact_duplicate_renderings"] == 0
    assert rep["repeated_source_ids"] == 0
    assert rep["tokens"]["max"] <= lc.TOKEN_ROW_MAX
    return rep
