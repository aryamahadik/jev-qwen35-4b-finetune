"""Consistency checks for c_src/common/markers.json (the XF06 marker table): the table's own rules, its agreement with
MARKERS.md's item lists, and that every G0 spec is the version the table was built from. CPU, no data files.

Run:  /Users/aryamahadik/Documents/jev/opendecide-data/.venv/bin/python -m pytest -q c_src/common/test_markers.py
"""
from __future__ import annotations

import hashlib
import json
from pathlib import Path

import pytest

HERE = Path(__file__).resolve().parent
LEAN = HERE.parents[1]
T = json.loads((HERE / "markers.json").read_text())
G = T["classes"]
FAMILIES = ["COMMIT"] + [f"F{i}" for i in range(1, 14)]


def norm(x):
    return x.strip().lower() if isinstance(x, str) else x


def global_class(x):
    x = norm(x)
    hits = [c for c in ("unknown", "zero_or_absent") if x in {norm(w) for w in G[c]["words"] + G[c]["typed"]}]
    if x in {norm(w) for w in G["banned"]["words"] + G["banned"]["same_marker_forms"]}:
        hits.append("banned")
    return hits


def test_xf06_words_exactly():
    assert G["unknown"]["words"] == ["not recorded", "unknown"] and G["unknown"]["typed"] == [None]
    assert G["zero_or_absent"]["words"] == ["0", "none", "no"] and G["zero_or_absent"]["typed"] == [False]
    assert G["banned"]["words"] == ["-", "n/a", "N/A", "TBD", "?"]


def test_global_classes_are_disjoint():
    every = G["unknown"]["words"] + G["unknown"]["typed"] + G["zero_or_absent"]["words"] + G["zero_or_absent"]["typed"] \
        + G["banned"]["words"] + G["banned"]["same_marker_forms"]
    for w in every:
        assert len(global_class(w)) == 1, w


def test_every_family_has_an_entry():
    assert list(T["families"]) == FAMILIES


@pytest.mark.parametrize("fam", FAMILIES)
def test_family_uses_only_global_markers_and_no_banned_ones(fam):
    f = T["families"][fam]
    for w in f["uses"]:
        assert global_class(w) in (["unknown"], ["zero_or_absent"]), (fam, w)
    for cls, words in {**f.get("local", {}), **f.get("pending", {})}.items():
        for w in words:
            assert "banned" not in global_class(w), (fam, w)


@pytest.mark.parametrize("fam", FAMILIES)
def test_stricter_bans_never_reopen_a_banned_marker(fam):
    used = {norm(w) for w in T["families"][fam]["uses"]}
    for w in T["families"][fam]["stricter_bans"]:
        assert norm(w) not in used, (fam, w)


def test_one_meaning_per_marker_across_families():
    """A marker word means the same class in every family that uses it (unknown / zero-or-absent / present), and a
    family-local word never takes a global marker's place with a different class."""
    meaning = {}
    for c in ("unknown", "zero_or_absent"):
        for w in G[c]["words"] + G[c]["typed"]:
            meaning[norm(w)] = c
    alias = {"absent": "zero_or_absent"}
    for fam, f in T["families"].items():
        for cls, words in {**f.get("local", {}), **f.get("pending", {})}.items():
            for w in words:
                c = alias.get(cls, cls)
                assert meaning.setdefault(norm(w), c) == c, (fam, w, c, meaning[norm(w)])
        for cls, vals in f.get("typed_local", {}).items():
            for v in vals:
                assert meaning.setdefault(v, alias.get(cls, cls)) == alias.get(cls, cls), (fam, v)


def test_open_items_are_listed():
    assert T["open_items"] == ["M3", "M4", "N3"]
    assert sorted(T["closed_items"]) == ["M1", "M2", "N1", "N2"]              # N1 closed by PREREG_FINAL.md A16
    assert not any("pending" in f for f in T["families"].values())          # M1 closed: no pending marker left
    md = (HERE / "MARKERS.md").read_text()
    assert f"v{T['version']}" in md.splitlines()[0]
    for item in T["open_items"] + list(T["closed_items"]):
        assert f"| {item} |" in md, item


def test_typed_and_word_markers_keep_their_types():
    for fam, f in T["families"].items():
        for w in f["uses"]:
            assert w is None or isinstance(w, (str, bool)), (fam, w)


@pytest.mark.parametrize("fam", FAMILIES)
def test_table_matches_the_spec_it_was_built_from(fam):
    """Each family row was built from one version of its G0 spec (sha256 in built_from). When a spec changes, re-read
    its XF06 / marker / blank / missing-key references, update markers.json and MARKERS.md, and only then record the
    new sha256. Never refresh the sha256 alone."""
    ref = T["built_from"]["specs"][fam]
    p = LEAN / ref["path"]
    now = hashlib.sha256(p.read_bytes()).hexdigest()
    assert now == ref["sha256"], (f"{ref['path']} changed since the marker table was built ({ref['sha256'][:12]} -> "
                                  f"{now[:12]}): re-read its marker references and regenerate the table")
