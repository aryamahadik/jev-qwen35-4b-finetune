"""Tests for G13 (decontam_g13.py) after PREREG A25 (c)-(e): mixdev instance-only, methods 6-8, the TabFact '#'-CSV
resolver, the per-set embedding top-5 and its cache, the eval-side stale check, the sealed-side child's output shape,
and batch == lone runs. Synthetic fixtures only (tmp files); no real eval or held-out data is read."""
import hashlib
import json
import sys
from pathlib import Path

import numpy as np
import pytest

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parents[1]))
import decontam_g13 as g  # noqa: E402
import decontam_g13_batch as gb  # noqa: E402


# ---- fixtures --------------------------------------------------------------------------------------------------------
class FakeEnc:
    """Deterministic stand-in for the sentence encoder: VEC[text] if given, else a hash-seeded unit vector."""
    VEC: dict = {}
    dev, dim = "cpu", 8

    def __init__(self, cfg=None):
        pass

    def __call__(self, texts):
        out = []
        for t in texts:
            v = FakeEnc.VEC.get(t)
            if v is None:
                seed = int.from_bytes(hashlib.blake2b(t.encode(), digest_size=4).digest(), "little")
                v = np.random.default_rng(seed).normal(size=self.dim)
            v = np.asarray(v, np.float32)
            out.append(v / np.linalg.norm(v))
        return np.array(out, np.float16).reshape(len(texts), self.dim)


@pytest.fixture
def fake_embed(tmp_path, monkeypatch):
    monkeypatch.setattr(g, "Encoder", FakeEnc)
    monkeypatch.setattr(g, "EMB_DIR", tmp_path / "emb")
    FakeEnc.VEC = {}
    cos = tmp_path / "cos.json"
    cos.write_text(json.dumps({"threshold": 0.95, "model": "fake", "max_seq_length": 16, "dtype": "float16"}))
    return cos


def jl(p: Path, rows) -> Path:
    p.write_text("".join(json.dumps(r) + "\n" for r in rows))
    return p


def unit(key, state=None, instructions=None, options=(), card=None, group=None, seed=False):
    texts = [(f, t) for f, t in (("state", state), ("instructions", instructions), ("card", card)) if t]
    texts += [("option", o) for o in options]
    u = {"key": key, "rows": [] if seed else [key + "-r"], "source": "src", "seed": seed, "texts": texts,
         "struct": set(), "groups": {group} if group else set(), "s_g13": set()}
    if state:
        u["s_g13"].add(g.struct_g13(state, list(options)))
    return u


def tgt(name, path, **kw):
    return g.target(name, ["abs:" + str(path)], **kw)


S1 = "The red lamp in Hall Seven stays lit whenever the north door is open and the guard is away"
S2 = "Every courier who carries a sealed parcel must sign the ledger before the depot closes at noon"
INSTR = "Read the record carefully and decide whether the stated conclusion follows from the given facts"


# ---- method 6: structure hash ----------------------------------------------------------------------------------------
def test_struct_g13_abstracts_names_and_sorts_options():
    a = g.struct_g13("Alice gave Bob 3 apples. Bob ate 1.", ["yes", "no"])
    b = g.struct_g13("Carol gave Dan 3 apples. Dan ate 1.", ["no", "yes"])
    c = g.struct_g13("Carol gave Dan 4 apples. Dan ate 1.", ["no", "yes"])
    d = g.struct_g13("Carol gave Carol 3 apples. Dan ate 1.", ["no", "yes"])
    assert a == b and a != c and a != d
    assert g.struct_g13("", ["x"]) is None


def test_mixdev_structure_group_and_g13_hash(tmp_path, monkeypatch):
    md = tmp_path / "c_src/F1/out"
    md.mkdir(parents=True)
    jl(md / "mixdev_S5.jsonl", [{"state": "Ann owns 2 cats.", "options": ["a", "b"], "group_id": "gX",
                                 "meta": {"structure_hash": "h1"}}])
    jl(md / "mixdev_S5.sidecar.jsonl", [{"state": "ignored", "group_id": "gY"}])
    monkeypatch.setattr(g, "LEAN", tmp_path)
    ks, items, files = g.mixdev_structs()
    assert (items, files) == (1, 1) and ks["group_id"] == {"gX"} and ks["structure"] == {"h1"}
    us = [unit("u1", "Zed owns 2 cats.", options=("b", "a")), unit("u2", "Zed owns 3 cats."), unit("u3", group="gX")]
    us[2]["struct"] = {"h1"}
    tg = g.target("mixdev_structure", [], kind="structure")
    trec = {"mixdev_structure": {}}
    res = {m: set(got) for _, m, got, _ in g.extra_methods(us, [tg], trec, [])}
    assert res == {"structure_g13": {0}, "group_id": {2}, "structure": {2}}


# ---- A25 (c): mixdev compares instance content only ------------------------------------------------------------------
def test_mixdev_instance_content_only(tmp_path):
    f = jl(tmp_path / "mixdev_S5.jsonl", [{"state": S1, "instructions": INSTR, "options": ["yes", "no"]},
                                          {"state": "A short unrelated state about nine green boxes", "instructions": INSTR,
                                           "options": ["yes", "no"]}])
    tgs = [tgt("mixdev", f, fields=g.MIXDEV_EVAL_FIELDS, train_fields=g.MIXDEV_TRAIN_FIELDS, main_only=True),
           tgt("dev:x", f)]
    units = [unit("shares_instr", S2, instructions=INSTR), unit("shares_state", S1, instructions="Other words here now ok")]
    rec = g.run("T", units, {}, {}, tgs, tmp_path / "out", cosine=None, side=False)
    md = rec["counts_by_eval_and_method"]["mixdev"]
    assert md["exact_full"]["units"] == 1                       # the state match only
    dev = rec["counts_by_eval_and_method"]["dev:x"]             # every other target keeps every field
    assert dev["exact_full"]["units"] == 2
    lone = g.run("T", units, {}, {}, tgs[:1], tmp_path / "out2", cosine=None, side=False)
    assert lone["drop_ids"] == ["shares_state-r"]


# ---- method 8: templates ---------------------------------------------------------------------------------------------
def test_instr_pieces_and_template_instr_substring(tmp_path):
    instr = "Read the note. Answer with yes or no only please.\nUse the table"
    ps = g.instr_pieces(instr)
    assert ps[0] == instr and "Answer with yes or no only please." in ps and all(len(g.words(p)) >= 5 for p in ps)
    f = jl(tmp_path / "dev_x.jsonl", [{"instructions": instr, "state": "x"}])
    tgs = [tgt("templates_instr", f, kind="instr", fields=("instructions",), methods=("exact", "substring"))]
    units = [unit("hit", "Some state words that are long enough. Please answer with yes or no only please now."),
             unit("miss", "Answer with yes or no. Nothing else here at all today.")]
    rec = g.run("T", units, {}, {}, tgs, tmp_path / "o", cosine=None, side=False)
    assert rec["drop_ids"] == ["hit-r"] and rec["counts_by_eval_and_method"]["templates_instr"]["substring"]["units"] == 1


def test_template_hits_word_boundaries():
    t = [tuple(g.words("Ignore previous instructions."))]
    us = [unit("a", "Please ignore previous instructions, then stop."), unit("b", "Do not ignore previousinstructions.")]
    assert set(g.template_hits(us, t)) == {0}


# ---- TabFact '#'-CSV resolver ----------------------------------------------------------------------------------------
def test_tabfact_csv_gives_pipe_table_hash():
    csv_text = "Team#Wins#City\nRovers#3#Leeds\nUnited#5#York\n"
    pipe = "| team | wins | city |\n| --- | --- | --- |\n| United | 5 | York |\n| Rovers | 3 | Leeds |"
    a, b = g.tables(g.csv_table_text(csv_text, "#")), g.tables(pipe)
    assert a and a == b
    assert g.tables(g.csv_table_text("Team#Wins\nRovers#4\n", "#")) != a


# ---- method 5: embedding, cache, per-set top-5 -----------------------------------------------------------------------
def test_emb_cache_roundtrip(tmp_path):
    c = g.EmbCache(tmp_path / "c")
    assert len(c) == 0
    c.add([5, 9], np.eye(2, 4, dtype=np.float16))
    c = g.EmbCache(tmp_path / "c")
    v, ok = c.get(np.array([9, 7, 5], np.uint64), 4)
    assert ok.tolist() == [True, False, True] and v[0, 1] == 1 and v[2, 0] == 1 and not v[1].any()
    assert c.has(np.array([5, 6], np.uint64)).tolist() == [True, False]


def test_embed_top5_is_per_set(tmp_path, fake_embed):
    e = np.zeros(8, np.float32)
    e[0] = 1
    q = "query text about the harbour lights tonight"
    FakeEnc.VEC[q] = e
    near = [f"alpha harbour light number {i} is on" for i in range(6)]
    for i, t in enumerate(near):
        v = e.copy()
        v[1 + i % 6] = 0.05 + 0.001 * i
        FakeEnc.VEC[t] = v
    b_text = "beta harbour lights are shining tonight"
    vb = e.copy()
    vb[7] = 0.25                                   # cosine ~0.97: below every A text, above the 0.95 threshold
    FakeEnc.VEC[b_text] = vb
    f = jl(tmp_path / "ev.jsonl", [{"text": q}])
    tgs = [tgt("ev", f, kind="generic")]
    sets = {"A": ([unit(f"a{i}", t) for i, t in enumerate(near)], {}, {}, None),
            "B": ([unit("b0", b_text)], {}, {}, None)}
    recs = g.run_sets(sets, tgs, tmp_path / "o", cosine=fake_embed, side=False)
    assert recs["B"]["drop_ids"] == ["b0-r"]                                    # a union top-5 would miss it
    assert len(recs["A"]["drop_ids"]) == 5 and recs["A"]["counts_by_eval_and_method"]["ev"]["embed"]["units"] == 5
    lone_b = g.run("B", *sets["B"][:3], tgs, tmp_path / "o2", cosine=fake_embed, side=False)
    assert lone_b["drop_ids"] == recs["B"]["drop_ids"]


def test_embed_uses_cache_then_live(tmp_path, fake_embed):
    cfg = g.load_cosine(fake_embed)
    q = "some eval text with enough words in it"
    c = g.EmbCache(g.emb_dir(cfg))
    c.add([g.hseq(g.words(q))], FakeEnc()([q]))
    emb = g.Embed(cfg, cache=g.EmbCache(g.emb_dir(cfg)))
    emb.vectors([g.hseq(g.words(q)), 123], [q, "another eval text that is not cached at all"])
    assert emb.stats == {"cache_hit": 1, "encoded_live": 1}


# ---- batch == lone runs ----------------------------------------------------------------------------------------------
def test_batch_equals_lone_runs(tmp_path, fake_embed):
    f = jl(tmp_path / "dev.jsonl", [{"state": S1, "instructions": INSTR, "options": ["yes", "no"]},
                                    {"state": S2, "instructions": "Pick one", "options": ["a", "b"]}])
    md = jl(tmp_path / "mixdev_S5.jsonl", [{"state": S2, "instructions": INSTR, "options": ["a", "b"]}])
    tgs = [tgt("dev", f), tgt("mixdev", md, fields=g.MIXDEV_EVAL_FIELDS, train_fields=g.MIXDEV_TRAIN_FIELDS)]
    sets = {"X": ([unit("x1", S1), unit("x2", "Nothing shared in this one at all, truly"),
                   unit("xs", INSTR, seed=True)], {}, {}, None),
            "Y": ([unit("y1", S2, instructions=INSTR), unit("y2", S1 + " and more words")], {}, {}, None)}
    both = g.run_sets(sets, tgs, tmp_path / "b", cosine=fake_embed, side=False)
    for n, s in sets.items():
        lone = g.run(n, *s[:3], tgs, tmp_path / ("l" + n), cosine=fake_embed, side=False)
        for k in ("drop_ids", "counts_by_eval_and_method", "seed_hits", "seeds_clean", "counts_by_training_field"):
            assert both[n][k] == lone[k], (n, k)
    assert gb.SETS == g.SETS


# ---- eval-side stale check -------------------------------------------------------------------------------------------
def test_eval_stale_detects_changed_and_new_files(tmp_path, monkeypatch):
    d = tmp_path / "ev"
    d.mkdir()
    a = jl(d / "a.jsonl", [{"text": "one two three four five six"}])
    monkeypatch.setattr(g, "targets", lambda: [g.target("ev", ["abs:" + str(d / "*.jsonl")], kind="generic")])
    monkeypatch.setattr(g, "COSINE", tmp_path / "none.json")
    g._SHA.clear()
    log = {"inputs_sha256": {"eval": {g.rel_of(a): g.sha256_file(a)}, "cosine": None, "sealed_side": {}}}
    assert g.eval_stale(log) is None
    jl(d / "b.jsonl", [{"text": "new"}])
    assert "not in the run" in g.eval_stale(log)
    (d / "b.jsonl").unlink()
    a.write_text('{"text": "changed"}\n')
    g._SHA.clear()
    assert "changed" in g.eval_stale(log)
    assert "older tool" in g.eval_stale({"inputs_sha256": {}})


def test_log_problems_flags_missing_methods(tmp_path):
    (tmp_path / "S.json").write_text(json.dumps({"drop_ids": [], "complete": True, "inputs_sha256": {},
                                                 "methods": {"structure": "run", "template": "run", "sealed": "run",
                                                             "sealed_side": "run", "embed": "not_run: x"}}))
    p = g.log_problems(["S"], tmp_path)
    assert any("methods ['embed', 'template_rev', 'table (all public-2 containers)']" in x for x in p) \
        and any("stale eval side" in x for x in p)


# ---- A25 (d): the sealed-side child ----------------------------------------------------------------------------------
def test_side_guard():
    assert not g.side_ok(g.LEAN / "data/ohs3_parts/runs/x.jsonl")
    assert not g.side_ok(g.LEAN / "data/preds_ohs3/x.jsonl")
    assert not g.side_ok(g.LEAN / "data/ohs3_jev_out.jsonl")
    assert not g.side_ok(g.LEAN / "sealed_nd/x.jsonl")
    assert g.side_ok(g.LEAN / "data/ohs3_items.jsonl")


def test_sealed_side_child_outputs_counts_and_unit_indices_only(tmp_path, monkeypatch):
    secret = "zebra quartz harbour " + S1
    f = jl(tmp_path / "held.jsonl", [{"state": secret, "options": ["yes", "no"]}, {"state": "tiny"}])
    monkeypatch.setattr(g, "SEALED_SIDE", {"held": ["abs:" + str(f)]})
    up = tmp_path / "u.jsonl"
    with open(up, "w") as fh:
        for o, u in (("A", unit("a", secret)), ("A", unit("b", S2)), ("B", unit("c", "x " + secret + " y"))):
            fh.write(json.dumps({"o": o, "s": False, "t": u["texts"]}) + "\n")
    out = tmp_path / "o.json"
    assert g.sealed_side_child(up, ["held"], None, out) == 0
    raw = out.read_text()
    assert "zebra" not in raw and "harbour" not in raw and str(tmp_path) not in raw
    r = json.loads(raw)["held"]
    assert r["status"] == "scanned" and r["files"] == 1 and r["items"] == 2 and r["short"] == 1
    assert r["by_set"]["A"]["exact_full"]["units"] == [0] and r["by_set"]["B"]["substring"]["units"] == [2]
    assert g.sealed_side_child(None, ["held"], None, out, mode="digest") == 0
    assert set(json.loads(out.read_text())["held"]) == {"status", "files", "digest"}


def test_file_rewritten_mid_run_is_recorded_as_changed(tmp_path):
    f = jl(tmp_path / "m.jsonl", [{"state": "a"}])
    shas = {}
    g.note_sha(shas, f)
    g.note_sha(shas, f)
    assert shas[g.rel_of(f)] == g.sha256_file(f)
    f.write_text('{"state": "b"}\n')
    g.note_sha(shas, f)
    assert shas[g.rel_of(f)] == "changed-during-run"
