"""Tests for G13_STREAM_WORKERS (decontam_g13.py: the files of a big parquet target scanned by worker processes).
Synthetic data only (a tiny training set, tiny parquet / jsonl / txt eval targets written under pytest's tmp_path);
no real eval file is opened. The serial scan (switch unset) is the reference: the full Scan state (counters, hit sets
with their iteration order, items_hit / items_by, deferred ek / ei, the dedup cache, shas, sub_rows, unsupported-file
counts) and the run_sets output must be identical for N = 2 and 3 workers. Run from lean/:
  ../.venv/bin/python -m pytest -q c_build/tests/test_g13_parallel.py
"""
from __future__ import annotations

import json
import random
import subprocess
import sys
import time
from collections import Counter
from pathlib import Path

import numpy as np
import pyarrow as pa
import pyarrow.parquet as pq
import pytest

sys.dont_write_bytecode = True
C_BUILD = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(C_BUILD))
import decontam_g13 as g  # noqa: E402

SYL = ["ka", "lo", "mi", "ra", "tu", "ve", "so", "ni", "pa", "de", "gu", "bi", "zo", "fa", "he", "jo"]
SHORT_OPT = ["Mara", "Ivo Petrov"]
SHORT_INSTR = ["Pick one", "Answer now please"]
LONG_INSTR = ["Read the ledger and decide which payment arrives first under the stated rule.",
              "Choose the option that follows from the clause quoted in the state above.",
              "Decide whether the second statement is supported by the first one given."]
TABLE = "| Name | Qty |\n| --- | --- |\n| Apple | 3 |\n| Pear | 5 |"
TABLE_PLAIN = "Name | Qty\nApple | 3\nPear | 5"


# ------------------------------------------------------------------------------------------------ synthetic world
def _vocab(rng, n=500):
    ws = set()
    while len(ws) < n:
        ws.add("".join(rng.choice(SYL) for _ in range(rng.randint(2, 4))))
    return sorted(ws)


def _sent(rng, V, n):
    return " ".join(rng.choice(V) for _ in range(n))


def _para(rng, V, ns=6):
    return " ".join(_sent(rng, V, rng.randint(8, 14)).capitalize() + "." for _ in range(ns))


def _write_pq(path: Path, cols: dict) -> None:
    arrs = {k: pa.array(v, pa.list_(pa.string())) if v and isinstance(v[0], list) else pa.array(v, pa.string())
            for k, v in cols.items()}
    pq.write_table(pa.table(arrs), path)


class World:
    """Training units + eval directories (all synthetic)."""

    def __init__(self, tmp: Path):
        rng = random.Random(20261016)
        self.rng, self.V = rng, _vocab(rng)
        self.paras = [_para(rng, self.V) for _ in range(14)]
        self.shared = _sent(rng, self.V, 12) + "."                 # one sentence inside seven training states
        rows = []
        for i, ps in enumerate(self.paras):
            st = ps + ("\n" + TABLE if i == 3 else "") + (" " + self.shared if i % 2 == 0 else "")
            rows.append({"id": f"r{i}", "call_id": f"c{i // 2}", "state": st, "instructions": LONG_INSTR[i % 3],
                         "card": SHORT_INSTR[i % 2] if i % 4 == 0 else None,
                         "options": [SHORT_OPT[i % 2], _sent(rng, self.V, 6)], "source": "syn" if i % 2 else "syn2"})
        tp = tmp / "train.jsonl"
        tp.write_text("".join(json.dumps(r) + "\n" for r in rows))
        self.units = g.train_units(tp)
        self.owner = ["A" if i % 3 else "B" for i in range(len(self.units))]
        self.pool: list = []                              # texts already written (duplicates across files)
        self.tmp = tmp

    # ---- eval texts
    def text(self, kind: int | None = None) -> str:
        rng, V, P = self.rng, self.V, self.paras
        k = rng.randrange(16) if kind is None else kind
        p = rng.choice(P)
        sents = p.split(". ")
        t = {0: lambda: p,
             1: lambda: p.lower().replace(".", ""),
             2: lambda: rng.choice(sents).rstrip(".") + ".",
             3: lambda: _sent(rng, V, 9) + ". " + rng.choice(sents).rstrip(".") + ". " + _sent(rng, V, 7) + ".",
             4: lambda: " ".join(w if rng.random() > 0.02 else rng.choice(V) for w in p.split()),
             5: lambda: _para(rng, V, rng.randint(1, 5)),
             6: lambda: rng.choice(SHORT_OPT + SHORT_INSTR + ["Zork"]),
             7: lambda: rng.choice(self.pool) if self.pool else _para(rng, V, 2),
             8: lambda: _sent(rng, V, 6) + "\n" + TABLE_PLAIN,
             9: lambda: rng.choice(LONG_INSTR),
             10: lambda: p[: len(p) // 2],
             11: lambda: _sent(rng, V, rng.randint(1, 4)),
             12: lambda: _para(rng, V, 3).replace(". ", "\n"),
             13: lambda: p + "\n" + TABLE,
             14: lambda: self.shared,
             15: lambda: _sent(rng, V, 5) + ". " + self.shared + " " + _sent(rng, V, 4) + "."}[k]()
        self.pool.append(t)
        return t

    def texts(self, n: int) -> list:
        return [self.text() for _ in range(n)]

    def make_dir(self, name: str, n_files: int = 12, rows: int = 30) -> Path:
        d = self.tmp / name
        d.mkdir()
        for i in range(n_files):
            f = d / f"f{i:02d}.parquet"
            if i == 1:
                _write_pq(f, {"text": self.texts(rows), "label": [f"lab{j % 3}" for j in range(rows)]})
            elif i == 2:
                _write_pq(f, {"a": [self.text(6) for _ in range(rows)], "b": self.texts(rows),
                              "c": [self.text(11) for _ in range(rows)]})
            elif i == 3:
                _write_pq(f, {"state": self.texts(rows), "instructions": [self.text(9) for _ in range(rows)],
                              "options": [[self.text(6), self.text(11)] for _ in range(rows)]})
            elif i == 4:
                _write_pq(f, {"text": []})                                              # an empty file
            elif i == 5:
                _write_pq(f, {"text": [self.text(6) for _ in range(rows)]})              # only short texts
            elif i == 6:
                t = [self.text(7) for _ in range(rows)]                                  # duplicates across files
                _write_pq(f, {"text": t + [x.upper() for x in t[:5]] + [x + "\n" for x in t[5:10]]})
            else:
                _write_pq(f, {"text": self.texts(rows)})
        return d


@pytest.fixture()
def world(tmp_path):
    return World(tmp_path)


@pytest.fixture()
def pools(monkeypatch):
    """Records every worker pool started (n workers) so a test can assert the parallel path really ran."""
    started = []
    init = g._StreamPool.__init__

    def spy(self, scan, tg, n):
        started.append((tg["name"], n))
        init(self, scan, tg, n)

    monkeypatch.setattr(g._StreamPool, "__init__", spy)
    return started


def _clean(d):
    return {k: v for k, v in d.items() if k not in ("wall_s", "unix")}


# ------------------------------------------------------------------------------------------------ state snapshot
def snap(sc) -> dict:
    """The full Scan state. Dict / Counter / array orders are kept (they follow the order of the operations, which the
    replay reproduces); the training-text sets (hits, cache values) are compared as sets: their iteration order is a
    layout detail of how each set was built, not a result (see decontam_g13._fset)."""
    nest = lambda d, f: [(a, [(b, f(s)) for b, s in m.items()]) for a, m in d.items()]  # noqa: E731
    return {"items": list(sc.items.items()), "short": list(sc.short.items()), "sub_rows": list(sc.sub_rows.items()),
            "hits": nest(sc.hits, sorted), "items_hit": nest(sc.items_hit, list),
            "items_by": [(st, nest(lbs, list)) for st, lbs in sc.items_by.items()],
            "ek": [(lb, list(a)) for lb, a in sc.ek.items()], "ei": [(lb, list(a)) for lb, a in sc.ei.items()],
            "cache": [(k, [(m, sorted(v)) for m, v in r.items()]) for k, r in sc.cache.items()],
            "q": list(sc.q), "q_words": sc.q_words, "waiting": dict(sc.waiting), "own": list(sc._own.items())}


def _scan(world, defer):
    return g.Scan(g.TrainIndex(world.units), None, world.owner, defer=defer)


def _stream_all(world, tgs, workers, monkeypatch, defer=True, cache_cls=None, batch=None):
    if workers > 1:
        monkeypatch.setenv("G13_STREAM_WORKERS", str(workers))
        monkeypatch.setenv("G13_STREAM_MIN_MB", "0")
    else:
        monkeypatch.delenv("G13_STREAM_WORKERS", raising=False)
    if batch:
        monkeypatch.setattr(g, "BATCH_WORDS", batch)
    sc = _scan(world, defer)
    if cache_cls:
        sc.cache = cache_cls()
    recs, shas = [], {}
    for tg in tgs:
        rec, ts = {}, {}
        g.stream(sc, tg, rec, ts)
        recs.append(rec)
        shas.update(ts)
    return sc, recs, shas


def _targets(world, tmp_path):
    d1 = world.make_dir("d1", 12)
    d2 = world.make_dir("d2", 5, rows=25)
    d3 = tmp_path / "d3"
    d3.mkdir()
    names = ["taskA", "taskB"]
    (tmp_path / "names.json").write_text(json.dumps(names))
    for i in range(5):
        _write_pq(d3 / f"p{i}.parquet", {"text": world.texts(20), "task": [names[j % 3] if j % 3 < 2 else "other"
                                                                          for j in range(20)]})
    (d3 / "x.jsonl").write_text("".join(json.dumps({"text": t, "task": "taskA"}) + "\n" for t in world.texts(15)))
    (d3 / "y.txt").write_text("\n".join(world.texts(10)) + "\n")
    (d3 / "z.bin").write_bytes(b"\0\1\2")
    return [g.target("gen_a", [f"abs:{d1}/*.parquet"], blind=True),
            g.target("gen_b", [f"abs:{d2}/*.parquet"], methods=("exact", "substring"), tables=True, fields=("text",)),
            g.target("gen_c", [f"abs:{d3}/*"], sublabel={"names": f"abs:{tmp_path / 'names.json'}", "label": "sub"})]


# ------------------------------------------------------------------------------------------------ tests
@pytest.mark.parametrize("workers", [2, 3])
@pytest.mark.parametrize("defer", [True, False])
def test_scan_state_identical_to_serial(world, tmp_path, monkeypatch, pools, workers, defer):
    tgs = _targets(world, tmp_path)
    ref, rrec, rsha = _stream_all(world, tgs, 1, monkeypatch, defer)
    assert not pools
    got, grec, gsha = _stream_all(world, tgs, workers, monkeypatch, defer)
    assert pools == [("gen_a", workers), ("gen_b", workers), ("gen_c", workers)]
    assert sum(len(v) for v in ref.hits.values()) > 0 and sum(len(v) for v in ref.items_hit.values()) > 0
    assert {"minhash", "ngram10", "tulu8", "substring", "exact_seg", "exact_full"} <= {
        m for ms in ref.hits.values() for m in ms}
    assert sum(ref.sub_rows.values()) > 0
    assert rrec == grec and rsha == gsha
    assert grec[2]["unsupported_files"] == {".bin": 1}
    a, b = snap(ref), snap(got)
    for k in a:
        assert a[k] == b[k], k
    if defer:
        assert any(len(a_) for _, a_ in a["ek"])


@pytest.mark.parametrize("workers", [2, 3])
def test_small_batches_and_cache_clears_replay_identically(world, tmp_path, monkeypatch, pools, workers):
    class Clearing(dict):                         # Scan's 2M clear rule, reached after a few entries
        def __len__(self):
            return dict.__len__(self) + 1_999_996

    tgs = _targets(world, tmp_path)
    ref, *_ = _stream_all(world, tgs, 1, monkeypatch, True, Clearing, batch=120)
    got, *_ = _stream_all(world, tgs, workers, monkeypatch, True, Clearing, batch=120)
    assert len(pools) == 3
    a, b = snap(ref), snap(got)
    for k in a:
        assert a[k] == b[k], k
    assert dict.__len__(ref.cache) < 40           # the cache really was cleared many times


@pytest.mark.parametrize("order", ["A_then_B", "B_then_A"])
def test_equal_words_different_raw_text_gets_the_serial_result(world, tmp_path, monkeypatch, pools, order):
    """Scan dedups by the normalized words, but exact_seg reads the raw sentence cuts: 'Dr. X ...' and 'Dr X ...' have
    equal words and different segments. The serial result is the first text's for both; so must the parallel one be."""
    body = "smith went home early today after the long meeting"
    train = tmp_path / "t2.jsonl"
    train.write_text(json.dumps({"id": "q0", "state": f"Intro words here. {body.capitalize()}. Tail words follow here.",
                                 "instructions": "Answer.", "options": [], "source": "s"}) + "\n")
    units = g.train_units(train)
    raw_a, raw_b = f"Dr. {body}", f"Dr {body}"
    assert g.words(raw_a) == g.words(raw_b)
    one = g.Scan(g.TrainIndex(units))
    one.add_item(("x",), [(raw_a, True)], "all", False)
    one.add_item(("y",), [(raw_b, True)], "all", False)
    one.flush()
    ia = one.items_hit["x"].get("exact_seg", set()) and 1
    ib = one.items_hit["y"].get("exact_seg", set()) and 1
    assert ia == 1 and ib == 1                    # serial: the cache gives raw_b raw_a's hit
    d = tmp_path / "dd"
    d.mkdir()
    first, second = (raw_a, raw_b) if order == "A_then_B" else (raw_b, raw_a)
    for i in range(6):
        _write_pq(d / f"f{i}.parquet", {"text": [first if i == 0 else second if i == 3 else world.text(5)]})
    tg = g.target("rawvar", [f"abs:{d}/*.parquet"])
    w = World.__new__(World)
    w.units, w.owner = units, [""]
    ref, *_ = _stream_all(w, [tg], 1, monkeypatch, True)
    got, *_ = _stream_all(w, [tg], 3, monkeypatch, True)
    assert pools == [("rawvar", 3)]
    a, b = snap(ref), snap(got)
    for k in a:
        assert a[k] == b[k], k
    seg = ref.items_hit["rawvar"].get("exact_seg", set())
    assert (0 in seg and 3 in seg) if order == "A_then_B" else (0 not in seg and 3 not in seg)


def test_cache_clear_between_equal_word_texts_uses_that_texts_result(world, tmp_path, monkeypatch, pools):
    """One file holds 'Dr. X ...' then fillers then 'Dr X ...' (equal words, different sentence cuts); the serial cache is
    cleared in between, so the second text is computed from ITS OWN raw text. The worker's dedup must not hand it the
    first one's result: results are keyed by the raw-text digest too."""
    class Clearing(dict):
        def __len__(self):
            return dict.__len__(self) + 1_999_996

    body = "smith went home early today after the long meeting"
    train = tmp_path / "t3.jsonl"
    train.write_text(json.dumps({"id": "q0", "state": f"Intro words here. {body.capitalize()}. Tail words follow here.",
                                 "instructions": "Answer.", "options": [], "source": "s"}) + "\n")
    units = g.train_units(train)
    d = tmp_path / "dc"
    d.mkdir()
    fill = [world.text(5) for _ in range(12)]
    for i in range(5):
        _write_pq(d / f"f{i}.parquet", {"text": [f"Dr. {body}"] + fill + [f"Dr {body}"] if i == 2 else world.texts(4)})
    tg = g.target("clr", [f"abs:{d}/*.parquet"])
    w = World.__new__(World)
    w.units, w.owner = units, [""]
    ref, *_ = _stream_all(w, [tg], 1, monkeypatch, True, Clearing, batch=40)
    got, *_ = _stream_all(w, [tg], 2, monkeypatch, True, Clearing, batch=40)
    assert pools == [("clr", 2)]
    a, b = snap(ref), snap(got)
    for k in a:
        assert a[k] == b[k], k
    seg = ref.items_hit["clr"]["exact_seg"]
    assert len(seg) == 1                                   # only the first text hits; the second has its own result


@pytest.mark.parametrize("workers", [2, 3])
def test_run_sets_output_identical(world, tmp_path, monkeypatch, pools, workers):
    tgs = _targets(world, tmp_path)
    d4 = world.make_dir("d4", 5, rows=20)                      # a mixdev-like target (instance-only second index)
    tgs.append(g.target("gen_inst", [f"abs:{d4}/*.parquet"], fields=g.MIXDEV_EVAL_FIELDS,
                        train_fields=g.MIXDEV_TRAIN_FIELDS))
    sets = {"S1": (world.units[:8], {"t": "x"}, {}, None), "S2": (world.units[8:], {}, {}, None)}
    outs = []
    for tag, w in (("ser", 1), ("par", workers)):
        if w > 1:
            monkeypatch.setenv("G13_STREAM_WORKERS", str(w))
            monkeypatch.setenv("G13_STREAM_MIN_MB", "0")
        else:
            monkeypatch.delenv("G13_STREAM_WORKERS", raising=False)
        od = tmp_path / tag
        r = g.run_sets(sets, tgs, od, cosine=None, side=False)
        outs.append({n: json.dumps(_clean(json.loads((od / f"{n}.json").read_text())), indent=1) for n in sets})
        assert {n: json.dumps(_clean(v), indent=1, default=list) for n, v in r.items()}.keys() == sets.keys()
    assert outs[0] == outs[1]
    assert [n for n, _ in pools] == ["gen_a", "gen_b", "gen_c", "gen_inst"]
    rec = json.loads(outs[0]["S1"])
    assert rec["eval_items"]["gen_a"] > 300 and rec["hits_by_eval"] and rec["targets"]["gen_c"]["unsupported_files"]


def test_blocked_minhash_is_bit_identical():
    """The workers' cache-blocked minhash gives exactly the engine's signatures (empty batch, texts of < 5 words with no
    5-gram, one-text batches, many tiny texts, texts longer than a block, a mix)."""
    rng = np.random.default_rng(7)
    cases = [[], [3], [0, 0, 0], [5], [4, 9, 4], [6000], [2, 3000, 7, 7, 2500, 1, 5], [10] * 700,
             list(rng.integers(0, 120, 400)), [20000, 5, 30]]
    for lens in cases:
        lens = np.array(lens, np.int64)
        cat = rng.integers(0, 2 ** 63, int(lens.sum()), dtype=np.uint64)
        h5, t5, _ = g.grams(cat, lens, g.MH_N) if len(lens) else (np.empty(0, np.uint64), np.empty(0, np.int64), None)
        a, b = g.minhash(h5, t5, len(lens)), g._minhash_blocked(h5, t5, len(lens))
        assert a.dtype == b.dtype == np.uint64 and a.shape == b.shape and np.array_equal(a, b), lens[:5]
    assert not np.array_equal(a, np.full_like(a, np.iinfo(np.uint64).max))


def test_default_path_creates_no_pool(world, tmp_path, monkeypatch):
    tgs = _targets(world, tmp_path)

    def boom(*a, **k):
        raise AssertionError("a pool or process was created")

    monkeypatch.setattr(g, "_StreamPool", boom)
    monkeypatch.setattr(g.subprocess, "Popen", boom)
    for val in (None, "", "1"):
        if val is None:
            monkeypatch.delenv("G13_STREAM_WORKERS", raising=False)
        else:
            monkeypatch.setenv("G13_STREAM_WORKERS", val)
        sc = _scan(world, True)
        g.stream(sc, tgs[0], {}, {})
        assert sc.items["gen_a"] > 100


def test_small_or_few_file_targets_stay_serial(world, tmp_path, monkeypatch):
    d = world.make_dir("few", 3)                                # 3 parquet files < 4
    sc = _scan(world, True)
    p = sorted(d.glob("*.parquet"))
    monkeypatch.setenv("G13_STREAM_WORKERS", "3")
    monkeypatch.setenv("G13_STREAM_MIN_MB", "0")
    assert g._par_workers(sc, p, True, None) == 0
    d2 = world.make_dir("many", 5)
    p2 = sorted(d2.glob("*.parquet"))
    assert g._par_workers(sc, p2, True, None) == 3
    assert g._par_workers(sc, p2, False, None) == 0             # the sealed-side child's own file list / guard
    assert g._par_workers(sc, p2, True, lambda *a: None) == 0   # on_file: the child
    monkeypatch.setenv("G13_STREAM_MIN_MB", "1000")
    assert g._par_workers(sc, p2, True, None) == 0              # small data: pool start-up would cost more
    monkeypatch.setenv("G13_STREAM_MIN_MB", "0")
    live = g.Scan(sc.idx, object(), sc.owner)
    assert g._par_workers(live, p2, True, None) == 0            # live embedding (the child) stays serial
    assert g._par_workers(g._PScan(sc.idx, True), p2, True, None) == 0
    monkeypatch.setenv("G13_STREAM_WORKERS", "x")
    with pytest.raises(ValueError):
        g._par_workers(sc, p2, True, None)
    monkeypatch.setenv("G13_STREAM_WORKERS", "0")
    with pytest.raises(ValueError):
        g._par_workers(sc, p2, True, None)


def test_a_failing_worker_fails_loudly_and_cleans_up(world, tmp_path, monkeypatch):
    d = world.make_dir("bad", 6)
    (d / "f04.parquet").write_bytes(b"SECRET EVAL TEXT this is not a parquet file")
    tg = g.target("bad", [f"abs:{d}/*.parquet"])
    monkeypatch.setenv("G13_STREAM_WORKERS", "2")
    monkeypatch.setenv("G13_STREAM_MIN_MB", "0")
    before = set(Path(__import__("tempfile").gettempdir()).glob("g13pw_*"))
    sc = _scan(world, True)
    with pytest.raises(RuntimeError) as ei:
        g.stream(sc, tg, {}, {})
    assert "worker failed on file #4 of 6" in str(ei.value) and "SECRET" not in str(ei.value)
    assert set(Path(__import__("tempfile").gettempdir()).glob("g13pw_*")) == before
    time.sleep(0.5)
    out = subprocess.run(["pgrep", "-f", "_pw_main"], capture_output=True, text=True).stdout.split()
    assert not out, out


def test_a_killed_worker_fails_loudly(world, tmp_path, monkeypatch):
    d = world.make_dir("kill", 8, rows=40)
    tg = g.target("kill", [f"abs:{d}/*.parquet"])
    monkeypatch.setenv("G13_STREAM_WORKERS", "2")
    monkeypatch.setenv("G13_STREAM_MIN_MB", "0")
    orig = g._StreamPool.run

    def run(self, files):
        for proc, _ in self.workers:
            proc.kill()
            proc.wait()
        yield from orig(self, files)

    monkeypatch.setattr(g._StreamPool, "run", run)
    with pytest.raises(RuntimeError, match="worker died|BrokenPipe|exited"):
        g.stream(_scan(world, True), tg, {}, {})


def test_tripwire_refuses_a_changed_scan(world, tmp_path, monkeypatch):
    d = world.make_dir("trip", 5)
    tg = g.target("trip", [f"abs:{d}/*.parquet"])
    monkeypatch.setenv("G13_STREAM_WORKERS", "2")
    monkeypatch.setenv("G13_STREAM_MIN_MB", "0")
    monkeypatch.setattr(g, "_REPLAY_SRC_SHA", "0" * 64)
    with pytest.raises(RuntimeError, match="_REPLAY_SRC_SHA"):
        g.stream(_scan(world, True), tg, {}, {})
    assert g._replay_src_sha() != "0" * 64


def _hf_target(world, tmp_path, monkeypatch, name, cols_per_file):
    """An hfstream-looking target (virtual /hfstream paths, files read from G13_BIGPAT_LOCAL, nothing downloaded)."""
    d = tmp_path / f"hfsrc_{name}"
    d.mkdir()
    local = tmp_path / f"local_{name}"
    (local / "all").mkdir(parents=True)
    names = []
    for i, cols in enumerate(cols_per_file):
        _write_pq(d / f"f{i:02d}.parquet", cols)
        names.append(f"f{i:02d}.parquet")
        (local / "all" / names[-1]).write_bytes((d / names[-1]).read_bytes())
    monkeypatch.setenv("G13_BIGPAT_LOCAL", str(local))
    prev = g.resolve
    monkeypatch.setattr(g, "resolve", lambda spec: [g.STREAM_ROOT / f"syn/{name}" / "all" / n for n in names]
                        if spec.startswith(f"hfstream:syn/{name}") else prev(spec))
    return g.target(f"hf_{name}", [f"hfstream:syn/{name}|^all/"], blind=True)


def test_hfstream_files_flush_at_every_file_end(world, tmp_path, monkeypatch, pools):
    """stream() flushes after each hfstream file (plain files carry their queue on): a text of file 1 that is already in
    the cache is credited at once, a text of file 0 only at that flush, which orders the method keys of a label."""
    s0, s1 = world.paras[0].split(". "), world.paras[1].split(". ")
    p_text = s0[0] + ". " + s1[0] + "."                               # two training sentences, not one contiguous span
    q_text = " ".join(world.paras[2].split(". ")[1].split()[1:7])    # a span inside a training sentence
    warm = tmp_path / "warm"
    warm.mkdir()
    for i in range(5):
        _write_pq(warm / f"w{i}.parquet", {"text": [q_text] + world.texts(3)})
    tw = g.target("warm", [f"abs:{warm}/*.parquet"])
    th = _hf_target(world, tmp_path, monkeypatch, "ord", [{"text": [p_text] + world.texts(3)},
                                                          {"text": [q_text] + world.texts(3)},
                                                          {"text": world.texts(4)}, {"text": world.texts(4)}])
    out = []
    for w in (1, 2):
        if w > 1:
            monkeypatch.setenv("G13_STREAM_WORKERS", str(w))
            monkeypatch.setenv("G13_STREAM_MIN_MB", "0")
        else:
            monkeypatch.delenv("G13_STREAM_WORKERS", raising=False)
        sc = _scan(world, True)
        for tg in (tw, th):
            g.stream(sc, tg, {}, {})
        out.append(snap(sc))
    assert out[0] == out[1] and pools == [("warm", 2), ("hf_ord", 2)]
    ms = [m for lb, mm in out[0]["hits"] if lb == "hf_ord" for m, _ in mm]
    assert "substring" in ms and "exact_seg" in ms and ms.index("exact_seg") < ms.index("substring")


class _FakeCache:
    def __init__(self, have):
        self.have, self.added = np.array(sorted(have), np.uint64), []

    def has(self, keys):
        return np.isin(np.asarray(keys, np.uint64), self.have)

    def add(self, keys, vecs):
        self.added.append((list(keys), np.asarray(vecs).shape))


class _FakeEnc:
    dim = 4

    def __init__(self):
        self.calls = []

    def __call__(self, texts):
        self.calls.append(len(texts))
        return np.zeros((len(texts), 4), np.float16)


@pytest.mark.parametrize("cached", ["all", "some"])
def test_embedding_collector_side_effects_identical(world, tmp_path, monkeypatch, pools, cached):
    """hfstream files feed the embedding collector `co`: all keys cached -> bookkeeping only; keys missing -> the parent
    re-reads the file and encodes serially, exactly as before."""
    d = world.make_dir("hf", 6, rows=25)
    local = tmp_path / "local"
    (local / "all").mkdir(parents=True)
    names = sorted(p.name for p in d.glob("*.parquet"))
    for n in names:
        (local / "all" / n).write_bytes((d / n).read_bytes())
    monkeypatch.setenv("G13_BIGPAT_LOCAL", str(local))
    real_resolve = g.resolve
    monkeypatch.setattr(g, "resolve", lambda spec: [g.STREAM_ROOT / "syn/ds" / "all" / n for n in names]
                        if spec.startswith("hfstream:") else real_resolve(spec))
    tg = g.target("hf_syn", ["hfstream:syn/ds|^all/"], blind=True)
    probe = g._Collect(_FakeCache([]), _FakeEnc(), quiet=True)
    g.stream(g._CoSink(probe), tg, {}, {})                      # the serial collector alone: every key it sees
    allk = set(probe.seen)
    assert len(allk) > 50
    have = allk if cached == "all" else set(sorted(allk)[::2])
    res = []
    for w in (1, 3):
        if w > 1:
            monkeypatch.setenv("G13_STREAM_WORKERS", str(w))
            monkeypatch.setenv("G13_STREAM_MIN_MB", "0")
        else:
            monkeypatch.delenv("G13_STREAM_WORKERS", raising=False)
        sc = _scan(world, True)
        fc, fe = _FakeCache(have), _FakeEnc()
        sc.co = g._Collect(fc, fe, quiet=True)
        rec, shas = {}, {}
        g.stream(sc, tg, rec, shas)
        co = sc.co
        res.append((snap(sc), rec, shas, list(co.items.items()), co.seen, co.added, co.skipped, fc.added, fe.calls))
    assert res[0] == res[1] and pools == [("hf_syn", 3)]
    assert res[0][5] == (0 if cached == "all" else len(allk) - len(have)) and res[0][6] == (
        len(allk) if cached == "all" else len(have))
    assert any(k.startswith("hfstream:") for k in res[0][2])
