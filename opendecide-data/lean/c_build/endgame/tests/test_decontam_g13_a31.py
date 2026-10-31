"""PREREG Ruling A31 (b) and (c) in decontam_g13.py. Synthetic fixtures only (tmp files); no real eval file is read.

(b) a Claude-written seed literal hit binds only when it renders into a training row of its set (program check, the
    methods' normalization, split at placeholders); a literal proven absent from every training row is report-only
    ('A31b: not rendered'). (c) templates_rev (>= 3-word equality / 5-9-word containment bind) runs on Claude-written
    seeds and templates only; public-data records (formats-2 records) are instance text: methods 1-7, always binding.
"""
import json
import sys
from pathlib import Path

import pytest

CB = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(CB))
import decontam_g13 as g  # noqa: E402

D1 = "The quarterly harbor ledger lists every crate that left the northern pier"
D2 = "A parser line naming the barge that sank near the southern breakwater"
D3 = "Is it true that the ferry sails on the evening tide past the old stone lighthouse at dusk"
D4 = "Seven rare orchids bloom beside the frozen mill race every winter"
D5 = "Twelve copper kettles hang above the long counter of the quiet inn"
TMPL = "\n".join([
    f'R = "{D1}"',                                                                   # rendered (a row's state)
    f'N = "{D2}"',                                                                   # never rendered (code)
    'T = "Is it true that {x} sails on the evening tide past the old stone lighthouse at dusk"',   # rendered, filled
    'T2 = "{y} drifts on the evening tide past the old stone lighthouse at dusk"',  # placeholder piece not rendered
    'U = "Use the card."',                                                           # rendered (rows' instructions)
]) + "\n"


def jl(p: Path, rows) -> Path:
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text("".join(json.dumps(r) + "\n" for r in rows))
    return p


def row(i, state, instr="Use the card."):
    return {"id": f"r{i}", "call_id": f"c{i}", "source": "F3", "state": state, "instructions": instr,
            "options": ["yes", "no"], "group_id": f"g{i}"}


@pytest.fixture
def lean(tmp_path, monkeypatch):
    L = tmp_path / "lean"
    jl(L / "c_src/F3/out/candidates_r1.jsonl", [
        row(0, f"Clerk note: {D1} before noon."),
        row(1, "Is it true that a small barge sails on the evening tide past the old stone lighthouse at dusk"),
        row(2, "Unrelated words about rivers and boats only here today")])
    (L / "c_src/F3/gen").mkdir(parents=True)
    (L / "c_src/F3/gen/tmpl.py").write_text(TMPL)
    # formats: one Claude-written codebook (formats-1) and one public-data record file (formats-2 records)
    jl(L / "c_src/formats/formats-1/data/styles.jsonl", [{"id": "s1", "lead": "Use the card."},
                                                         {"id": "s2", "lead": D5}])
    jl(L / "c_src/formats/formats-2/records/xed.jsonl", [{"id": "x1", "text": "Use the card."},
                                                         {"id": "x2", "text": D4}])
    jl(L / "c_src/F7/out/mixdev_S5.jsonl", [{"state": "A mixdev item about lamps", "options": ["a"], "group_id": "m"}])
    jl(L / "data/dev_x.jsonl", [{"state": s, "instructions": "Read it. Use the card.", "options": ["a", "b"]}
                                for s in (D1, D2, D3, D4, D5)])
    monkeypatch.setattr(g, "LEAN", L)
    monkeypatch.setattr(g, "OUT", L / "logs/decontam_counts")
    monkeypatch.setattr(g, "MIXDEV_FREEZE", L / "logs/decontam_counts/MIXDEV_FREEZE.json")
    monkeypatch.setattr(g, "COSINE", tmp_path / "none.json")
    monkeypatch.setattr(g, "TEMPLATE_SETS", ("dev_x",))
    monkeypatch.setattr(g, "OPI_BUILDER", "no_opi.py")
    monkeypatch.setattr(g, "RENDER_SHARED", ("c_src/F3/out/candidates_r1.jsonl", "c_src/F5/out/candidates_r1.jsonl"))
    keep = {"mixdev", "mixdev_structure", "templates_rev"}
    tg = [g.target("dev:dev_x", ["lean:data/dev_x.jsonl"])] + [t for t in g.targets() if t["name"] in keep]
    monkeypatch.setattr(g, "targets", lambda: [dict(t) for t in tg])
    g._SHA.clear()
    return L


def run(*names):
    return g.run_sets({n: g.build_set(n) for n in names}, g.targets(), g.OUT, cosine=g.COSINE, side=False)


def lit(rec, kind="seed_hit_locs"):
    """{literal name in TMPL (R, N, T, T2, U) or record key} of a set's hit locators."""
    names = [ln.split(" = ")[0] for ln in TMPL.splitlines()]
    out = set()
    for k in rec[kind]:
        line = rec["seed_hit_lines"][k]
        out.add(names[line - 1] if k.startswith("seed:c_src/F3/gen/tmpl.py") else f"{k.split('/')[-1].split('#')[0]}@{line}")
    return out


def test_seed_pieces_split_and_unprovable():
    assert g.seed_pieces(D1) == [" " + " ".join(g.words(D1)) + " "]
    assert g.seed_pieces("Is it {x} true\nthat %s or %(b)s holds here") == [" holds here ", " is it "]
    assert g.seed_pieces("{a} versus {b}") is None                      # no >= 2-word piece: absence not shown
    assert g.seed_pieces("Answer: {ans}\nThe claim holds.") == [" the claim holds "]


def test_rendered_literal_binds_and_unrendered_is_report_only(lean):
    rec = run("F3")["F3"]
    assert lit(rec) == {"R", "T", "U"}                                   # rendered: binding
    assert lit(rec, "seed_hit_locs_report_only") == {"N", "T2"}          # never in a training row: report-only
    assert rec["seeds_clean"] is False
    assert rec["seed_render"]["binding"] == {"rendered": 3} and rec["seed_render"]["report_only_not_rendered"] == 2
    c = rec["counts_by_eval_and_method"]["dev:dev_x"]
    assert c["exact_full"]["seed_literals"] == 1 and c["exact_full"]["seed_literals_report_only"] == 1   # R / N
    assert rec["counts_by_eval_and_method"]["templates_rev"]["template_rev"]["seed_literals"] == 1     # U
    assert "r0" in rec["drop_ids"]                                        # the row that renders R is itself a hit
    text = (g.OUT / "F3.json").read_text().lower()
    assert "harbor" not in text and "breakwater" not in text and "lighthouse" not in text   # counts only


def test_only_unrendered_hits_leave_seeds_clean(lean):
    (lean / "c_src/F3/gen/tmpl.py").write_text(f'N = "{D2}"\n')
    rec = run("F3")["F3"]
    assert rec["seeds_clean"] is True and rec["seed_hit_locs"] == [] and len(rec["seed_hit_locs_report_only"]) == 1
    assert not any("seed literal" in x for x in g.log_problems(["F3"], g.OUT))
    jl(lean / "c_src/F3/out/candidates_r1.jsonl", [row(0, f"Now rendered: {D2}.")])     # the literal now renders
    g._SHA.clear()
    assert run("F3")["F3"]["seeds_clean"] is False


def test_public_record_vs_template(lean):
    rec = run("formats")["formats"]
    tr = rec["counts_by_eval_and_method"]["templates_rev"]["template_rev"]
    assert tr["seed_literals"] == 1                                      # the Claude-written codebook line only
    hit = lit(rec)
    assert hit == {"styles.jsonl@1", "xed.jsonl@2"}                     # template (rendered) + public record (D4)
    assert rec["seed_render"]["binding"] == {"rendered": 1, "public_record": 1}
    assert lit(rec, "seed_hit_locs_report_only") == {"styles.jsonl@2"}   # D5: Claude-written, rendered nowhere
    units, *_ = g.build_set("formats")
    pub = [u for u in units if u.get("public")]
    assert pub and all("formats-2/records/" in u["key"] for u in pub)
    assert all(not u.get("public") for u in units if "formats-1" in u["key"])
    hits, rep = g.template_rev_hits(pub, {tuple(g.words("Use the card."))})
    assert not hits and rep == {"exact_2w_report_only": 0, "contained_3_4w_report_only": 0}   # never templates_rev


def test_public_record_in_instance_check_even_if_unrendered(lean):
    rec = run("formats")["formats"]
    c = rec["counts_by_eval_and_method"]["dev:dev_x"]
    assert c["exact_full"]["seed_literals"] == 1 and "seed_literals_report_only" in c["exact_full"]   # D4 / D5
    assert rec["seeds_clean"] is False


def test_shared_render_rows_stale_then_refresh(lean):
    (lean / "c_src/formats/formats-2/records/xed.jsonl").unlink()
    jl(lean / "c_src/formats/formats-1/data/styles.jsonl", [{"id": "s2", "lead": D5}])
    rec = run("formats")["formats"]
    assert rec["seeds_clean"] is True and rec["seed_render"]["report_only_not_rendered"] == 1
    assert set(rec["inputs_sha256"]["render_rows"]) == {"c_src/F3/out/candidates_r1.jsonl"}
    assert not any("render check stale" in x for x in g.log_problems(["formats"], g.OUT))
    jl(lean / "c_src/F5/out/candidates_r1.jsonl", [row(9, f"The inn: {D5}")])        # another family renders it now
    g._SHA.clear()
    assert any("render check stale" in x for x in g.log_problems(["formats"], g.OUT))
    assert g.refresh(["formats"], out_dir=g.OUT, cosine=g.COSINE) == 0
    got = json.loads((g.OUT / "formats.json").read_text())
    assert got["seeds_clean"] is False and got["seed_render"]["binding"] == {"rendered": 1}
    g._SHA.clear()
    assert not any("render check stale" in x for x in g.log_problems(["formats"], g.OUT))


def test_batch_equals_lone_with_render(lean, tmp_path):
    both = run("F3", "formats")
    for n in ("F3", "formats"):
        lone = g.run_sets({n: g.build_set(n)}, g.targets(), tmp_path / f"lone_{n}", cosine=g.COSINE, side=False)[n]
        for k in ("seed_hit_locs", "seed_hit_locs_report_only", "seed_render", "seeds_clean", "drop_ids"):
            assert both[n][k] == lone[k], (n, k)


def test_side_child_never_two_at_once(monkeypatch):
    monkeypatch.setattr(g, "_side_busy", lambda: True)
    monkeypatch.setenv("G13_SIDE_WAIT", "0")
    h = g.sealed_side_start([], [], ["held"], None, mode="scan")
    assert h["proc"] is None
    assert g.sealed_side_finish(h)["held"]["status"].startswith("failed (busy")
