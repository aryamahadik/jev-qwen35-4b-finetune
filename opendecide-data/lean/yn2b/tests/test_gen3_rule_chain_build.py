"""F1 builder (golden_src/gen3/gen3_rule_chain.py) at a small scale: every mv_core check, the builder's own parse-back
self-check, decontamination-relevant rules (banned words, none texts, markers), the repair step, writing into a
temporary root with MANIFEST records, determinism, the devx latent export and the gen2 reuse adapter."""
from __future__ import annotations

import json
import random
import sys
from collections import Counter
from pathlib import Path

import pytest

LEAN = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(LEAN / "golden_src" / "gen3"))
import mv_core as mv  # noqa: E402
import gen3_rule_chain as G  # noqa: E402
import rc_core as RC  # noqa: E402
import rc_repair as RP  # noqa: E402

SCALE = 0.15


@pytest.fixture(scope="module")
def built(tmp_path_factory):
    root = tmp_path_factory.mktemp("f1")
    fb, b = G.build(check_tz=False, raw_dir=root / "raw", defs_dir=root / "defs", manifest=root / "M.jsonl",
                    scale=SCALE)
    return fb, b, root


def test_scale_independent_mv_core_checks(built):
    fb, b, _ = built
    for part in ("train", "dev"):
        rows = fb.rows_for(part)
        rids = {r["rid"] for r in rows}
        rep = mv.run_checks(rows, [x for x in fb.rels if x["a"] in rids])
        # at 15% scale the shares (tiers, 45-55% strata, |corr|, card styles, exception groups) are too small to
        # test; the full-size written parts must pass every check (test_gen3_rule_chain_written.py)
        for k in ("structure", "keysets", "levels"):
            assert rep[k]["ok"], (part, k, rep[k])
        assert rep["shortcuts"]["ok"] or part == "dev", rep["shortcuts"]


def test_self_check_parse_back_agrees(built):
    fb, b, _ = built
    rep = G.self_check_all(fb, b)
    assert rep["ok"], rep["examples"]


def test_row_rules(built):
    fb, b, _ = built
    rows = fb.rows
    assert G.banned_report(rows)["ok"]
    assert not any(mv.NONE_DEFAULT in r["options"] for r in rows)
    for r in rows:
        m = r["meta"]
        assert m["dataset"] == "program generator golden_src/gen3/gen3_rule_chain.py"
        assert m["licence"] == mv.LICENCE
        if mv.MARKERS[1] in r["state"]:
            assert m["view"] == "attack" and m["plant_spoof"]
        if m["qkind"] == "yn":
            assert r["options"] == ["yes", "no"] and r["gold"] in ("yes", "no")
        if m["pack"].startswith("a_school_transport") or m["renderer"] == "contract":
            assert m["dev_kind"] == "holdout"
    lats = Counter(r["meta"]["latent_id"] for r in rows)
    assert max(lats.values()) <= mv.UNIT_MAX_ROWS


def test_views_and_relations_present(built):
    fb, b, _ = built
    views = Counter(r["meta"]["view"] for r in fb.rows)
    for v in ("base", "contrast", "ladder", "format", "jb", "attack"):
        assert views[v] > 0, v
    rels = Counter(x["type"] for x in fb.rels)
    assert rels["complement"] and rels["equiv"] and rels["inv"]
    assert G.cue_report(fb.rows_for("train"))["ok"]


def test_write_into_temporary_root(built):
    fb, b, root = built
    out = fb.write(parts=("train", "dev"))
    rows, rels = mv.read_raw(G.KEY, "train", root / "raw")
    assert len(rows) == len(fb.rows_for("train"))
    recs = [json.loads(x) for x in (root / "M.jsonl").read_text().splitlines()]
    for rec in recs:
        if rec["part"] in ("train", "dev"):
            assert mv.sha256_file(Path(rec["path"])) == rec["sha256"]
    for r in rows[:50]:
        if r["meta"]["defs"]:
            assert (root / "defs" / f"{G.KEY}__{r['meta']['defs']}.json").exists()
    with pytest.raises(RuntimeError):
        fb.write(parts=("train",))       # no silent overwrite


def test_deterministic():
    fb1, _ = G.build(splits=("dev_iid",), check_tz=False, scale=0.1, repair_parts=False)
    fb2, _ = G.build(splits=("dev_iid",), check_tz=False, scale=0.1, repair_parts=False)
    assert [json.dumps(r, sort_keys=True) for r in fb1.rows] == [json.dumps(r, sort_keys=True) for r in fb2.rows]


def test_repair_only_removes_rows():
    fb, _ = G.build(splits=("dev_iid", "dev_holdout"), check_tz=False, scale=0.3, repair_parts=False)
    rows = fb.rows_for("dev")
    rids = {r["rid"] for r in rows}
    rels = [x for x in fb.rels if x["a"] in rids]
    before = {r["rid"]: json.dumps(r, sort_keys=True) for r in rows}
    rows2, rels2, log = RP.repair(rows, rels)
    assert log["end"][0] <= log["start"][0]
    assert all(before[r["rid"]] == json.dumps(r, sort_keys=True) for r in rows2)
    keep = {r["rid"] for r in rows2}
    assert all(x["a"] in keep and x["b"] in keep for x in rels2)
    assert not any(r["meta"]["view"] == "attack" for r in rows if r["rid"] not in keep
                   and any(x["rid"] == r["rid"] for x in rows2))


def test_devx_latents_use_held_out_parts():
    xs = G.devx_latents(24, check_tz=False)
    assert len(xs) == 24
    for x in xs:
        d, c = x["facts"]["doc"], x["facts"]["case"]
        assert d["skin"] == "school_transport" or d["style"] == "contract"
        g, _ = RC.decide(d, c)
        q = x["query"]
        if q["kind"] == "outcome":
            assert x["outcomes"][g] == x["gold"]
        elif q["kind"] == "outcome_is":
            assert (x["outcomes"][g] == q["target"]) == (x["gold"] == "yes")
        else:
            assert RC.pivotal(d, c) == [x["gold"]]
        assert mv.name_split(c["name"].split()[0]) == "devx"


def test_gen2_adapter_imports_only_allowed_names():
    code = (LEAN / "golden_src" / "gen3" / "rc_gen2.py").read_text().split('"""', 2)[2]   # code after the docstring
    assert "main(" not in code and "append_manifest(" not in code and "make_pair(" not in code
    assert "lean/pg" not in code and "import pg" not in code and "from pg" not in code
    import rc_gen2 as G2
    rng = random.Random(4)
    pool = mv.NamePool("train")
    ok = 0
    for dom in G2.DOMS:
        for _ in range(15):
            try:
                pr = G2.sample_pair(dom, rng, pool, "outcome", 3000, 11500, f"t|{dom}")
            except mv.Reject:
                continue
            assert pr["c1"] != pr["c2"]
            assert all(mv.name_split(n.split()[0]) == "train" for n in pr["names"])
            ok += 1
            break
    assert ok >= 5
