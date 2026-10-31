"""Tests for the G13 fixes after the endgame-build-4 review (7 Oct): method 9 table hashes in every public-2 container,
the sealed-side child's own vector cache (A25 d), mixdev freeze + `refresh` (re-scan only the targets that changed,
merged exactly as a full run), and method 8's other direction (templates_rev). Synthetic fixtures only (tmp files);
no real eval or held-out data is read, except public-2's render module (Claude-written code)."""
import hashlib
import importlib.util
import json
import sys
from pathlib import Path

import numpy as np
import pytest

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parents[1]))
import decontam_g13 as g  # noqa: E402

RENDER = HERE.parents[2] / "c_src/public/public-2/render.py"


def jl(p: Path, rows) -> Path:
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text("".join(json.dumps(r) + "\n" for r in rows))
    return p


class FakeEnc:
    dev, dim, calls = "cpu", 8, 0

    def __init__(self, cfg=None):
        pass

    def __call__(self, texts):
        FakeEnc.calls += len(texts)
        out = []
        for t in texts:
            seed = int.from_bytes(hashlib.blake2b(t.encode(), digest_size=4).digest(), "little")
            v = np.random.default_rng(seed).normal(size=self.dim)
            out.append(v / np.linalg.norm(v))
        return np.array(out, np.float16).reshape(len(texts), self.dim)


# ---- method 9: every container public-2 renders matches the TabFact hash --------------------------------------------
@pytest.fixture(scope="module")
def render():
    spec = importlib.util.spec_from_file_location("p2render_test", RENDER)
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m


TABLES = [(["Player", "Team", "Goals"], [["Ann Lee", "Reds", 3], ["Bo, Jr.", "Blues", 2.5], ["Cy", "Greens", 4.0]]),
          (["Year", "Winner"], [[1999, "A & B"], [2000, "C | D"]]),
          (["Name", "Notes", "Rank"], [["x", "", 1], ["y", "said: yes", 2]])]


@pytest.mark.parametrize("ti", range(len(TABLES)))
def test_every_container_matches_tabfact_hash(render, ti):
    header, rows = TABLES[ti]
    tab = "\n".join("#".join(header if i == 0 else [render._cell(v) for v in r]) for i, r in enumerate([header] + rows))
    ev = set(g.tables(g.csv_table_text(tab, "#")))
    assert len(ev) == 1
    for c in render.CONTAINERS:
        for title, cap in ((None, None), ("A page, with a comma", "Its caption")):
            t = render.render_table(header, rows, c, title=title, caption=cap)
            assert ev & set(g.tables(t)), (c, len(header), title)


def test_tables_no_false_match_and_old_pipe_hash_kept():
    a = g.tables("| a | b |\n|---|---|\n| 1 | 2 |")
    assert a == g.tables("a | b\n1 | 2")                        # 2-column pipe_plain == markdown
    assert not set(a) & set(g.tables("| a | b |\n| 1 | 3 |"))   # another cell set
    assert g.tables("one line | only") == [] and g.tables("") == []


# ---- the sealed-side child's own vector cache -----------------------------------------------------------------------
@pytest.fixture
def fake_embed(tmp_path, monkeypatch):
    monkeypatch.setattr(g, "Encoder", FakeEnc)
    monkeypatch.setattr(g, "EMB_DIR", tmp_path / "emb")
    monkeypatch.setattr(g, "SIDE_EMB_DIR", tmp_path / "emb_side")
    cos = tmp_path / "cos.json"
    cos.write_text(json.dumps({"threshold": 0.95, "model": "fake", "max_seq_length": 16, "dtype": "float16"}))
    return cos


SECRET = "zebra quartz harbour lantern drifts over the quiet northern bay tonight"


def test_side_cache_reused_and_holds_no_text(tmp_path, monkeypatch, fake_embed):
    f = jl(tmp_path / "held.jsonl", [{"state": SECRET + f" item {i}", "options": ["yes", "no"]} for i in range(5)])
    monkeypatch.setattr(g, "SEALED_SIDE", {"held": ["abs:" + str(f)]})
    up = jl(tmp_path / "u.jsonl", [{"o": "A", "s": False, "t": [["state", SECRET + " item 1"]]},
                                   {"o": "A", "s": False, "t": [["state", "nothing in common with it at all"]]}])
    outs = []
    for k in range(2):
        FakeEnc.calls = 0
        out = tmp_path / f"o{k}.json"
        assert g.sealed_side_child(up, ["held"], fake_embed, out) == 0
        outs.append(json.loads(out.read_text())["held"])
        if k == 0:
            first_calls = FakeEnc.calls
    assert outs[0]["by_set"] == outs[1]["by_set"]
    assert outs[1]["detail"]["embed"]["encoded_live"] == 0 and outs[1]["detail"]["embed"]["side_cache_hit"] >= 5
    assert first_calls > 0
    blob = b"".join(p.read_bytes() for p in (tmp_path / "emb_side").rglob("*") if p.is_file())
    assert blob and b"zebra" not in blob and b"harbour" not in blob
    assert not (tmp_path / "emb").exists() or not any((tmp_path / "emb").rglob("*.npy"))   # parent cache untouched
    monkeypatch.setenv("G13_SIDE_CACHE", "0")
    FakeEnc.calls = 0
    assert g.sealed_side_child(up, ["held"], fake_embed, tmp_path / "o3.json") == 0
    assert json.loads((tmp_path / "o3.json").read_text())["held"]["detail"]["embed"]["encoded_live"] >= 5


def test_side_embed_mode_prebuilds_cache(tmp_path, monkeypatch, fake_embed):
    f = jl(tmp_path / "held.jsonl", [{"state": SECRET + f" row {i}"} for i in range(4)])
    monkeypatch.setattr(g, "SEALED_SIDE", {"held": ["abs:" + str(f)]})
    out = tmp_path / "e.json"
    assert g.sealed_side_child(None, ["held"], fake_embed, out, mode="embed") == 0
    r = json.loads(out.read_text())["held"]
    assert r["added"] == 4 and r["items"] == 4 and "zebra" not in out.read_text()
    up = jl(tmp_path / "u.jsonl", [{"o": "A", "s": False, "t": [["state", "a training text that has five words"]]}])
    assert g.sealed_side_child(up, ["held"], fake_embed, tmp_path / "s.json") == 0
    assert json.loads((tmp_path / "s.json").read_text())["held"]["detail"]["embed"]["encoded_live"] == 0
    real_side = Path.home() / ".cache/opendecide_ext/g13_emb_sealedside/x/s1.vec.npy"
    assert not g.allowed(real_side) and g.NEVER.search("g13_emb_sealedside/x/s1.keys.npy")   # the parent's guard


# ---- mixdev freeze and refresh ----------------------------------------------------------------------------------------
S1 = "The western depot ships eleven crates of tin every second Tuesday"
S2 = "Three clerks verify each crate before the barge leaves the quay"
S3 = "A fresh mixdev claim about lighthouse keepers and their logbooks today"


@pytest.fixture
def lean(tmp_path, monkeypatch):
    L = tmp_path / "lean"
    jl(L / "c_src/F3/out/candidates_r1.jsonl", [
        {"id": "r1", "call_id": "c1", "source": "F3", "state": S1, "options": ["yes", "no"], "group_id": "g1"},
        {"id": "r2", "call_id": "c2", "source": "F3", "state": S2, "options": ["yes", "no"], "group_id": "g2"},
        {"id": "r3", "call_id": "c3", "source": "F3", "state": S3, "options": ["yes", "no"], "group_id": "g3"},
        {"id": "r4", "call_id": "c4", "source": "F3", "state": "Unrelated words about rivers and boats only here",
         "options": ["yes", "no"], "group_id": "g4"}])
    (L / "c_src/F3/gen").mkdir(parents=True)
    (L / "c_src/F3/gen/tmpl.py").write_text('A = "Answer with the single word yes or no."\nB = "Use the card."\n')
    jl(L / "c_src/F7/out/mixdev_S5.jsonl", [{"state": S1, "options": ["yes", "no"], "group_id": "m1"}])
    jl(L / "data/dev_x.jsonl", [{"state": "A dev claim on orchards, pears and plums in the valley",
                                 "instructions": "Read it. Use the card.", "options": ["a", "b"]}])
    monkeypatch.setattr(g, "LEAN", L)
    monkeypatch.setattr(g, "OUT", L / "logs/decontam_counts")
    monkeypatch.setattr(g, "MIXDEV_FREEZE", L / "logs/decontam_counts/MIXDEV_FREEZE.json")
    monkeypatch.setattr(g, "COSINE", tmp_path / "none.json")
    monkeypatch.setattr(g, "TEMPLATE_SETS", ("dev_x",))
    monkeypatch.setattr(g, "OPI_BUILDER", "no_opi.py")
    keep = {"mixdev", "mixdev_structure", "templates_rev"}
    tg = [g.target("dev:dev_x", ["lean:data/dev_x.jsonl"])] + [t for t in g.targets() if t["name"] in keep]
    monkeypatch.setattr(g, "targets", lambda: [dict(t) for t in tg])
    g._SHA.clear()
    return L


def full(name="F3"):
    return g.run_sets({name: g.build_set(name)}, g.targets(), g.OUT, cosine=g.COSINE, side=False)[name]


KEYS = ("drop_ids", "drop_units", "counts_by_eval_and_method", "counts_by_training_source", "counts_by_training_field",
        "seed_hits", "seeds_clean", "complete", "incomplete_why", "hits_by_eval", "eval_items", "short_items")


def test_refresh_equals_full_run_after_mixdev_rewrite(lean, tmp_path):
    rec = full()
    base = g.log_problems(["F3"], g.OUT)        # embed not run (no cosine), methods not in this target list, a seed hit
    assert rec["drop_ids"] == ["r1"] and not any("stale" in x for x in base)
    assert g.freeze_mixdev() == 0 and g.mixdev_freeze_drift() == []
    jl(lean / "c_src/F7/out/mixdev_S5.jsonl", [{"state": S3, "options": ["yes", "no"], "group_id": "m1"}])
    jl(lean / "c_src/F9/out/mixdev_S5.jsonl", [{"state": "Another one", "options": ["x"], "group_id": "g2"}])
    g._SHA.clear()
    assert len(g.mixdev_freeze_drift()) == 2
    p = g.log_problems(["F3"], g.OUT)
    assert len(p) == len(base) + 1 and any("stale eval side" in x and "`refresh`" in x for x in p)
    assert g.refresh(["F3"], out_dir=g.OUT, cosine=g.COSINE) == 0
    g._SHA.clear()
    assert g.log_problems(["F3"], g.OUT) == base
    got = json.loads((g.OUT / "F3.json").read_text())
    assert got["drop_ids"] == ["r2", "r3"] and got["refreshed"]
    ref = g.run_sets({"F3": g.build_set("F3")}, g.targets(), tmp_path / "fresh", cosine=g.COSINE, side=False)["F3"]
    for k in KEYS:
        assert got[k] == json.loads(json.dumps(ref[k])), k
    assert got["inputs_sha256"]["eval"] == ref["inputs_sha256"]["eval"]


def test_refresh_refuses_when_more_than_mixdev_changed(lean):
    full()
    jl(lean / "data/dev_x.jsonl", [{"state": S3 + " now", "instructions": "Read it.", "options": ["a", "b"]}])
    g._SHA.clear()
    assert "full run" in g.refresh_problem(json.loads((g.OUT / "F3.json").read_text()))
    assert g.refresh(["F3"], out_dir=g.OUT, cosine=g.COSINE) == 1
    p = g.log_problems(["F3"], g.OUT)
    assert any("re-run" in x for x in p)


def test_refresh_refuses_old_logs(lean):
    (g.OUT).mkdir(parents=True, exist_ok=True)
    (g.OUT / "F3.json").write_text(json.dumps({"drop_ids": [], "complete": True}))
    assert "predates refresh" in g.refresh_problem(json.loads((g.OUT / "F3.json").read_text()))


# ---- method 8, the other direction --------------------------------------------------------------------------------------
def test_template_rev_exact_binds_and_containment_is_report_only(lean):
    # A31 (b): a seed hit binds only when the literal renders into a training row, so one row renders the templates
    cand = lean / "c_src/F3/out/candidates_r1.jsonl"
    rows = [json.loads(x) for x in cand.read_text().splitlines() if x.strip()]
    jl(cand, rows + [{"id": "r5", "call_id": "c5", "source": "F3", "state": "Plain filler about kites on windy hills",
                      "instructions": "Use the card. Then read it twice over and stop.", "options": ["yes", "no"],
                      "group_id": "g5"}])
    g._SHA.clear()
    rec = full()
    c = rec["counts_by_eval_and_method"]["templates_rev"]["template_rev"]
    assert c["units"] == 0 and c["seed_literals"] == 1              # "Use the card." == a dev instruction sentence
    assert rec["seeds_clean"] is False and any("tmpl.py" in x for x in rec["seed_hit_locs"])
    assert rec["targets"]["templates_rev"]["wordings"] >= 2
    (lean / "c_src/F3/gen/tmpl.py").write_text('A = "Read it twice over"\nB = "card about it"\nC = "Be brief."\n')
    jl(lean / "data/dev_x.jsonl", [{"state": "Orchards again", "instructions": "Please read it twice over and stop. "
                                    "Be brief.", "options": ["a", "b"]}])
    g._SHA.clear()
    rec = full()
    tr = rec["targets"]["templates_rev"]
    assert rec["seeds_clean"] is True and tr["contained_3_4w_report_only"] == 1 and tr["exact_2w_report_only"] == 1
    (lean / "c_src/F3/gen/tmpl.py").write_text('A = "read it twice over and stop"\n')     # 6 words inside: binds
    g._SHA.clear()
    assert full()["seeds_clean"] is False


# ---- big_patent: a written ruling counts only when PREREG_FINAL.md holds it ----------------------------------------
def test_bigpat_ruling_needs_the_prereg_line(tmp_path, monkeypatch):
    def gap():
        return next(t for t in g.targets() if t["name"] == f"ohs_src:{g.BIGPAT}")["gap"]
    monkeypatch.setattr(g, "LEAN", tmp_path)
    (tmp_path / "PREREG_FINAL.md").write_text("> Amendment A99: nothing about it\n")
    monkeypatch.delenv("G13_BIGPAT_STREAM", raising=False)
    monkeypatch.setenv("G13_BIGPAT_RULING", "A99")
    assert gap() and g.bigpat_ruling() is None
    (tmp_path / "PREREG_FINAL.md").write_text("> Amendment A99 ... G13-BIGPAT-RULING A99 (text of the ruling)\n")
    assert g.bigpat_ruling() == "A99" and gap() is None
    monkeypatch.setenv("G13_BIGPAT_RULING", "A9")                     # a prefix of the tag is not the tag
    assert gap() and g.bigpat_ruling() is None
    monkeypatch.delenv("G13_BIGPAT_RULING")
    assert gap()
