"""CPU tests of the fast final G13 (7 Oct): precheck sets, embed witnesses and `--final --merge`. Synthetic rows and a
fake encoder only; no real eval set, sealed file or training file is read."""
import hashlib
import json
import sys
from pathlib import Path

import numpy as np
import pytest

CB = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(CB))
sys.path.insert(0, str(Path(__file__).resolve().parent))
import decontam_g13 as g  # noqa: E402

LONG = ("the quarterly ledger of the harbor authority lists eleven dredging contracts awarded "
        "between march and october with the largest going to a firm from the northern docks")
EV_E = "an eval sentence whose meaning several training texts paraphrase very closely indeed"
TS = [f"paraphrase number {w} about lighthouses ferries tides and coastal fog banks" for w in
      ("one", "two", "three", "four", "five", "six")]
CLEAN = ["gardening tools and soil acidity levels for spring planting in clay ground",
         "a recipe for barley soup with leeks carrots and a little thyme for winter",
         "the chess club meets on tuesdays in the library annex after the last lesson",
         "volunteers repainted the old railway station benches in a dark green colour"]
ALTERED = "this exact sentence appears in the eval file and only in an altered final row"
INSTR = "Read the record and answer the question below carefully."


class FakeEnc:
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


def row(i, call, state, src="c_test"):
    return {"id": f"r{i}", "call_id": call, "source": src, "state": state, "instructions": INSTR,
            "options": ["yes", "no"], "card": None}


def jl(p: Path, rows) -> Path:
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text("".join(json.dumps(r) + "\n" for r in rows))
    return p


@pytest.fixture
def world(tmp_path, monkeypatch):
    """F3 candidates (one exact hit, six embed neighbours of one eval text: top-5 drops five, the sixth stays clean),
    a replay shard dir, one eval target, fake encoder, everything under tmp_path."""
    monkeypatch.setattr(g, "Encoder", FakeEnc)
    monkeypatch.setattr(g, "EMB_DIR", tmp_path / "emb")
    monkeypatch.setattr(g, "SIDE_EMB_DIR", tmp_path / "emb_side")
    monkeypatch.setattr(g, "LEAN", tmp_path)
    monkeypatch.setattr(g, "HERE", tmp_path / "cb")
    monkeypatch.setattr(g, "REPLAY_SHARDS_DIR", tmp_path / "data/c_replay_r1_shards")
    monkeypatch.setattr(g, "PUBLIC_DIR", tmp_path / "c_src/public")
    (tmp_path / "cb/tmp").mkdir(parents=True)
    e1 = np.eye(8)[0]
    FakeEnc.VEC = {EV_E: e1}
    for i, t in enumerate(TS, 1):                    # cosines 0.999 ... 0.958, all >= 0.95, distinct in float16
        FakeEnc.VEC[t] = e1 + 0.05 * i * np.eye(8)[1]
    cos = tmp_path / "cos.json"
    cos.write_text(json.dumps({"threshold": 0.95, "model": "fake", "max_seq_length": 16, "dtype": "float16"}))
    monkeypatch.setattr(g, "COSINE", cos)
    f3 = [row(0, "a0", LONG)] + [row(i, f"n{i}", t) for i, t in enumerate(TS, 1)] + \
         [row(10, "c0", CLEAN[0]), row(11, "c1", CLEAN[1])]
    jl(tmp_path / "c_src/F3/out/candidates_r1.jsonl", f3)
    (tmp_path / "c_src/F3/gen").mkdir(parents=True)
    (tmp_path / "c_src/F3/gen/x.py").write_text(f'SEED = "{ALTERED} plus seed words"\n')
    rp = [row(20, "q0", CLEAN[2], "replay"), row(21, "q0", CLEAN[3], "replay"), row(22, "q1", CLEAN[2], "replay")]
    jl(tmp_path / "data/c_replay_r1_shards/shard_000.jsonl", rp)
    ev = jl(tmp_path / "ev/eval.jsonl", [{"id": "e0", "state": LONG, "options": []},
                                         {"id": "e1", "state": EV_E, "options": []},
                                         {"id": "e2", "state": ALTERED, "options": []}])
    tgs = [g.target("ev", [f"abs:{ev}"], blind=True, tables=True)]
    monkeypatch.setattr(g, "targets", lambda: tgs)
    logs = tmp_path / "logs/precheck"
    g.run_sets({n: g.build_set(n) for n in ("F3", "replay")}, tgs, logs, cosine=cos, side=False)
    return tmp_path, tgs, cos, logs, f3, rp


def final_rows(f3, rp, extra=()):
    """What a mixer would write: F3's clean rows (n6, c0, c1), replay with q0 split into two call_ids."""
    rows = [f3[6], f3[7], f3[8], {**rp[0], "call_id": "q0~0"}, {**rp[1], "call_id": "q0~1"}, rp[2]]
    return rows + list(extra)


def full_and_merge(tmp, tgs, cos, logs):
    full = g.run_sets({"final_mix_r1": g.build_set("final_mix_r1")}, tgs, tmp / "full", cosine=cos,
                      side=False)["final_mix_r1"]
    merged = g.final_merge([logs], out_dir=tmp / "out", cosine=cos)
    return full, merged


def test_precheck_logs_and_witness(world):
    tmp, tgs, cos, logs, f3, rp = world
    d = json.loads((logs / "F3.json").read_text())
    assert d["complete"] and sorted(d["drop_ids"]) == ["r0", "r1", "r2", "r3", "r4", "r5"]   # exact + top-5
    w = d["witness"]
    assert w["embed"] and len(w["open"]["ev"]) >= 2          # e0 (LONG) and e1 (EV_E) have above-threshold texts
    r = json.loads((logs / "replay.json").read_text())
    assert r["complete"] and r["drop_ids"] == [] and r["train_rows"] == 3
    assert list(r["inputs_sha256"]["train"]) == ["data/c_replay_r1_shards/shard_000.jsonl"]


def test_merge_equals_full_when_all_covered(world):
    tmp, tgs, cos, logs, f3, rp = world
    jl(tmp / g.FINAL_TRAIN, final_rows(f3, rp))
    jl(tmp / g.FINAL_REL, [{"a": "r20", "b": "r21", "type": "equiv"}])
    full, m = full_and_merge(tmp, tgs, cos, logs)
    assert full["drop_ids"] == ["r6"]                         # the sixth neighbour is top-5 in the final mix
    assert m["drop_ids"] == full["drop_ids"] and m["complete"], m["incomplete_why"]
    assert m["merge"]["units_scanned"] == 0 and m["merge"]["units_covered"] == 6
    assert m["merge"]["c_rel_r1"]["rows"] == 1 and m["merge"]["c_rel_r1"]["rows_with_other_fields"] == 0


def test_altered_unit_is_scanned(world):
    tmp, tgs, cos, logs, f3, rp = world
    jl(tmp / g.FINAL_TRAIN, final_rows(f3, rp, [row(30, "x0", ALTERED)]))
    full, m = full_and_merge(tmp, tgs, cos, logs)
    assert "r30" in full["drop_ids"] and m["drop_ids"] == full["drop_ids"]
    assert m["merge"]["units_scanned"] == 1


def test_seed_literal_does_not_cover(world):
    tmp, tgs, cos, logs, f3, rp = world
    assert any(u["seed"] for u in g.build_set("F3")[0])
    jl(tmp / g.FINAL_TRAIN, final_rows(f3, rp, [row(31, "x1", f"{ALTERED} plus seed words")]))
    full, m = full_and_merge(tmp, tgs, cos, logs)
    assert m["merge"]["units_scanned"] == 1 and m["drop_ids"] == full["drop_ids"]


def test_stale_or_incomplete_log_forces_scan(world):
    tmp, tgs, cos, logs, f3, rp = world
    jl(tmp / g.FINAL_TRAIN, final_rows(f3, rp))
    jl(tmp / "c_src/F3/out/candidates_r1.jsonl", f3 + [row(40, "z0", "a late row added after the g13 run here")])
    d = json.loads((logs / "replay.json").read_text())
    d["complete"] = False
    (logs / "replay.json").write_text(json.dumps(d))
    full, m = full_and_merge(tmp, tgs, cos, logs)
    ref = m["merge"]["logs_refused"]
    assert any("stale" in v for v in ref.values()) and any(v == "incomplete" for v in ref.values())
    assert m["merge"]["units_scanned"] == 6 and m["drop_ids"] == full["drop_ids"] == ["r6"]


def test_log_without_witness_is_not_used(world):
    tmp, tgs, cos, logs, f3, rp = world
    jl(tmp / g.FINAL_TRAIN, final_rows(f3, rp))
    d = json.loads((logs / "F3.json").read_text())
    d.pop("witness")
    (logs / "F3.json").write_text(json.dumps(d))
    full, m = full_and_merge(tmp, tgs, cos, logs)
    assert m["merge"]["units_scanned"] == 3 and m["drop_ids"] == full["drop_ids"]


def test_sets_and_public_precheck(world):
    tmp, *_ = world
    assert {"packs", "formats", "public", "replay", "final_mix_r1", "COMMIT"} <= set(g.SETS)
    assert g.SEED_SETS == {"packs": "c_src/packs", "formats": "c_src/formats"}
    for i, rel in enumerate(g.PUBLIC_POOL + g.PUBLIC_RESERVE_POOL[:2]):
        jl(tmp / "c_src/public" / rel, [row(100 + i, f"p{i}", CLEAN[i % 4], "pub")])
    us, shas, seeds, cat = g.build_set("public")
    assert len(us) == 5 and len(shas) == 5 and seeds == {} and cat.read_text().count("\n") == 5


def test_side_witness_roundtrip(world):
    tmp, tgs, cos, *_ = world
    cfg = g.load_cosine(cos)
    units = [{"key": "0", "rows": ["x"], "source": "", "seed": False, "texts": [("state", TS[0])]}]
    emb = g.Embed(cfg, cache=g.EmbCache(g.emb_dir(cfg)))
    sc = g.Scan(g.TrainIndex(units), emb.bind(g.TrainIndex(units), ["S"]), ["S"])
    wit = g._side_witness_hook(sc)
    ress = [__import__("collections").defaultdict(set)]
    sc.embed.scan([12345], [EV_E], ress)
    assert ress[0].get("embed@S") and wit == {"S": {12345}}
    tok = g._side_witness_write(wit, cfg, "ohs3", ["S"])["S"]["token"]
    g.EmbCache(g.emb_dir(cfg)).add([12345], FakeEnc()([EV_E]))
    up = jl(tmp / "u.jsonl", [{"o": "final_mix_r1", "s": False, "t": [["state", TS[5]]]}])
    wp, op = tmp / "w.json", tmp / "o.json"
    wp.write_text(json.dumps({"ohs3": [tok]}))
    assert g.sealed_witness_child(up, wp, cos, op) == 0
    r = json.loads(op.read_text())["ohs3"]
    assert r["status"] == "scanned" and r["by_set"]["final_mix_r1"]["embed"]["units"] == [0]
    (g.side_emb_dir(cfg) / "witness" / f"{tok}.json").write_text("{}")
    g.sealed_witness_child(up, wp, cos, op)
    assert json.loads(op.read_text())["ohs3"]["status"].startswith("failed")


def test_mixdev_only_staleness_keeps_coverage(world, monkeypatch):
    tmp, tgs, cos, logs, f3, rp = world
    md = jl(tmp / "ev/mixdev.jsonl", [{"id": "m0", "state": "an unrelated mixdev instance with enough words here",
                                       "options": []}])
    tgs2 = tgs + [g.target("mixdev", [f"abs:{md}"], blind=True)]
    monkeypatch.setattr(g, "targets", lambda: tgs2)
    g.run_sets({n: g.build_set(n) for n in ("F3", "replay")}, tgs2, logs, cosine=cos, side=False)
    jl(md, [{"id": "m0", "state": CLEAN[0], "options": []}])          # the lane rewrote mixdev: now hits c0
    jl(tmp / g.FINAL_TRAIN, final_rows(f3, rp))
    full, m = full_and_merge(tmp, tgs2, cos, logs)
    assert m["merge"]["units_scanned"] == 0 and not m["merge"]["logs_refused"]
    assert "r10" in full["drop_ids"] and m["drop_ids"] == full["drop_ids"] and m["complete"]
    assert not g.eval_stale(m)
