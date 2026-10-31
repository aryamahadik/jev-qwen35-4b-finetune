"""Tests for the A58 step-12 full-split leak-check target: sob_g13.py `sob_splits` (and, when g13_c2.py carries zed_orch/sob_wiring.patch, its wiring).
Synthetic data (pytest tmp_path: a fake local hub cache, fake bench cases, fake rows) for everything but the "real" tests, which read the pins / units
built from the real sources and print nothing but counts and booleans. No network, no Modal, no GPU. Run from lean/:
  ../.venv/bin/python -B -m pytest -q c2_build/tests/test_sob_splits.py
Real tests run on the repo's built files, or on a scratch build when SOB_SPLITS_SCRATCH=<dir holding units.jsonl and g13_sob/> is set; they skip when neither
exists. Tests marked "wired" need g13_c2.py to carry the patched run() (sob_splits), and are skipped on the unpatched file.
"""
from __future__ import annotations

import copy
import gzip
import hashlib
import inspect
import json
import os
import re
import shutil
import sys
from pathlib import Path

import pytest

sys.dont_write_bytecode = True
C2B = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(C2B))
sys.path.insert(0, str(Path(__file__).resolve().parent))
import c2io  # noqa: E402
import sob_g13 as S  # noqa: E402
import g13_c2 as G  # noqa: E402
from test_g13_c2 import A38, _run, exports, fake_tools, row, world  # noqa: E402,F401  (fixtures of the end-to-end world)
from test_sob_g13 import write_bench  # noqa: E402

g = G.g
wired = pytest.mark.skipif(not hasattr(G, "sob_g13") or "splits_rec" not in inspect.getsource(G.run),
                           reason="g13_c2.py does not carry the A58 sob_splits wiring yet (zed_orch/sob_wiring.patch)")
A58_COUNTS = {"sst5_test": 2210, "sst2_validation": 872, "boolq_validation": 3270, "xnli_ar_test": 5010, "xnli_en_test": 5010, "xnli_fr_test": 5010,
              "tweet_ar_test": 256}                                   # the numbers of Ruling A58 step 4 (A58_DRAFT.md)
LABEL_MARK = "LABELMARKERZZ"


# ---- a synthetic world: a fake hub cache, fake bench cases drawn from it, small sources ------------------------------------------------
def sent(tag: str, i: int) -> str:
    return f"the {tag} desk number {i} reports that harbour master {i} closed quay {i} after storm {i} loosened the iron rings along its edge"


def ar_sent(i: int) -> str:
    return f"الطقس اليوم جميل جدا رقم {i} والبحر هادئ والناس يمشون على الشاطئ بعد العصر مع أصدقائهم القدامى {i}"


N_SAMPLE = 4


def small_sources() -> dict:
    """The real source table with small counts (the same repos / revisions / splits / configs, so the bench scripts' pins still apply)."""
    src = copy.deepcopy(S.SPLIT_SOURCES)
    cnt = {"sst5_test": 12, "sst2_validation": 10, "boolq_validation": 14, "xnli_ar_test": 12, "xnli_en_test": 12, "xnli_fr_test": 12, "tweet_ar_test": 9}
    for k, n in cnt.items():
        src[k]["a58"], src[k]["n_sample"] = n, N_SAMPLE
    m = src["miracl_ar_dev"]
    m.update({"k": 3, "n_rerank": 2, "n_pair": 2, "clip": 40, "hub_counts": {"queries": 12, "qrels": 12 * 6, "corpus": 12 * 6}})
    return src


def _put(hub: Path, s: dict, rel: str, writer):
    p = hub / ("datasets--" + s["repo"].replace("/", "--")) / "snapshots" / s["revision"] / rel
    p.parent.mkdir(parents=True, exist_ok=True)
    writer(p)
    return p


def _parquet(rows: dict):
    import pyarrow as pa
    import pyarrow.parquet as pq
    return lambda p: pq.write_table(pa.table(rows), p)


def make_world(root: Path) -> dict:
    """Fake hub files + bench cases (lock-verified) the seeded sample of which are exactly drawn from them."""
    src, hub = small_sources(), root / "hub"
    rows, cases = {}, []
    # plain splits
    rows["sst5_test"] = [{"text": sent("review", i), "label": 3, "label_text": LABEL_MARK} for i in range(12)]
    _put(hub, src["sst5_test"], "test.jsonl", lambda p: p.write_text("".join(json.dumps(r) + "\n" for r in rows["sst5_test"]), encoding="utf-8"))
    rows["sst2_validation"] = [{"idx": i, "sentence": sent("sentence", i), "label": 1} for i in range(10)]
    rows["sst2_validation"][2]["sentence"] = "a dull mess "                                   # a 3-word item (the 5-word rule)
    _put(hub, src["sst2_validation"], src["sst2_validation"]["files"][0], _parquet({k: [r[k] for r in rows["sst2_validation"]] for k in ("idx", "sentence", "label")}))
    rows["boolq_validation"] = [{"question": f"does harbour master {i} close quay {i} in winter", "answer": bool(i % 2), "passage": sent("passage", i) + f" and more details {i}"}
                                for i in range(14)]
    _put(hub, src["boolq_validation"], src["boolq_validation"]["files"][0], _parquet({k: [r[k] for r in rows["boolq_validation"]] for k in ("question", "answer", "passage")}))
    for lang in ("ar", "en", "fr"):
        k = f"xnli_{lang}_test"
        rows[k] = [{"premise": f"{lang} " + sent("premise", i), "hypothesis": ("quay shut" if i == 1 else f"{lang} quay {i} was shut after the storm hit it"), "label": 1}
                   for i in range(12)]
        _put(hub, src[k], src[k]["files"][0], _parquet({c: [r[c] for r in rows[k]] for c in ("premise", "hypothesis", "label")}))
    rows["tweet_ar_test"] = [{"text": ar_sent(i), "label": "2", "lang": "arabic"} for i in range(9)]
    _put(hub, src["tweet_ar_test"], "test/arabic.jsonl.gz",
         lambda p: p.write_bytes(gzip.compress("".join(json.dumps(r, ensure_ascii=False) + "\n" for r in rows["tweet_ar_test"]).encode("utf-8"))))
    # the bench cases drawn from them (the real sample() / state shapes)
    for k, s in src.items():
        if s["fmt"] == "miracl":
            continue
        for i, j in enumerate(S.sample_indices(len(rows[k]), s["n_sample"])):
            st = {name: f"{rows[k][j][col]}{suf}" for name, (col, suf) in s["link"].items()}
            cases.append({"suite": s["bench_suite"], "id": f"{s['bench_suite']}-{i}", "state": st,
                          "questions": {"q": {"type": "noul", "instructions": "Does the text express the stated thing?"}}, "gold": {"q": {"type": "noul", "label": 1}}})
    # MIRACL-ar dev
    m = src["miracl_ar_dev"]
    queries = {f"q{i}": f"سؤال رقم {i} عن الموانئ" for i in range(12)}
    qrels, corpus = {}, []
    for qi in range(12):
        qrels[f"q{qi}"] = {}
        for j in range(6):
            d = f"d{qi}_{j}"
            qrels[f"q{qi}"][d] = 1 if j < 2 else 0
            corpus.append({"_id": d, "title": f"عنوان {qi}", "text": f"نص الفقرة رقم {j} للسؤال {qi} وهو نص طويل بما يكفي ليقص عند الأربعين حرفا وأكثر من ذلك بكثير {qi} {j}"})
    _put(hub, m, m["files"][0], _parquet({"_id": list(queries), "text": list(queries.values())}))
    _put(hub, m, m["files"][1], _parquet({"query-id": [q for q, d in qrels.items() for _ in d], "corpus-id": [x for d in qrels.values() for x in d],
                                          "score": [v for d in qrels.values() for v in d.values()]}))
    _put(hub, m, m["files"][2], _parquet({"_id": [c["_id"] for c in corpus], "title": [c["title"] for c in corpus], "text": [c["text"] for c in corpus]}))
    text = {c["_id"]: c["title"] + ": " + c["text"] for c in corpus}
    usable, rerank, pair = S.miracl_replay(queries, qrels, m["k"], m["n_rerank"])
    assert len(usable) == 12 and len(rerank) == 2 and len(pair) == 2
    for i, (qid, docs) in enumerate(rerank):
        cases.append({"suite": "ar_miracl_rerank", "id": f"ar_miracl_rerank-{i}", "state": {"query": queries[qid]},
                      "questions": {"passage": {"type": "choice", "instructions": "x", "criteria": {chr(97 + j): S.clip(text[d], m["clip"]) for j, d in enumerate(docs)}}},
                      "gold": {"passage": {"type": "choice", "label": "a"}}})
    for i, (qid, d) in enumerate(pair):
        cases.append({"suite": "ar_miracl_pair", "id": f"ar_miracl_pair-{i}", "state": {"query": queries[qid], "passage": S.clip(text[d], m["clip"])},
                      "questions": {"relevant": {"type": "noul", "instructions": "x"}}, "gold": {"relevant": {"type": "noul", "label": 1}}})
    cases.append({"suite": "s_other", "id": "s_other-0", "state": "an unrelated suite the splits build ignores entirely",
                  "questions": {"q": {"type": "noul", "instructions": "y"}}, "gold": {"q": {"type": "noul", "label": 0}}})
    cp, lp = write_bench(root / "bench", cases)
    return {"src": src, "hub": hub, "rows": rows, "cases": cp, "lock": lp, "case_list": cases, "text": text, "queries": queries, "rerank": rerank, "pair": pair,
            "root": root}


@pytest.fixture()
def sw(tmp_path):
    return make_world(tmp_path)


def do_build(sw, root: Path | None = None, **kw):
    root = root or sw["root"]
    kw.setdefault("check_scripts", False)
    return S.build_splits(sw["cases"], sw["lock"], root / "scan" / "splits_units.jsonl", root / "g13_sob", hub=sw["hub"], sources=sw["src"], **kw)


@pytest.fixture()
def built(sw, monkeypatch):
    units = sw["root"] / "scan" / "splits_units.jsonl"
    out = sw["root"] / "g13_sob"
    rel = g.rel_of(units)
    monkeypatch.setattr(S, "SPLITS_UNITS_REL", rel)
    monkeypatch.setattr(S, "SPLIT_FILES", {"sob_splits": (rel,)})
    monkeypatch.setattr(S, "SPLITS_PINS", out / "splits_pins.json")
    monkeypatch.setattr(S, "SPLITS_EXPORT_MANIFEST", out / "SPLITS_MANIFEST.json")
    monkeypatch.setattr(S, "SOB_DIR", out)                                              # SplitExports reads its manifest from SOB_DIR
    pins = do_build(sw)
    return {"pins": pins, "units": units, "out": out, "rel": rel, "sw": sw}


def units_of(path) -> list[dict]:
    return [json.loads(x) for x in Path(path).read_text(encoding="utf-8").splitlines() if x.strip()]


# ---- A58's numbers and the bench scripts' pins -----------------------------------------------------------------------------------------
def test_the_source_table_carries_a58s_counts_and_the_bench_scripts_revisions():
    for k, n in A58_COUNTS.items():
        assert S.SPLIT_SOURCES[k]["a58"] == n, k
    assert S.SPLIT_SOURCES["miracl_ar_dev"]["a58"] is None
    assert set(S.SPLIT_SOURCES) == {*A58_COUNTS, "miracl_ar_dev"}
    for k, s in S.SPLIT_SOURCES.items():
        assert re.fullmatch(r"[0-9a-f]{40}", s["revision"]), k
    scripts = g.REPO / S.SCRIPTS_REL
    if not (scripts / "build_suites.py").is_file():
        pytest.skip("the bench scripts are not here")
    assert S.revision_problems(S.SPLIT_SOURCES) == []


def test_a_revision_or_split_the_bench_scripts_do_not_pin_is_refused(tmp_path, sw):
    d = tmp_path / "scripts"
    d.mkdir()
    revs = {s["repo"]: s["revision"] for s in sw["src"].values() if s["script"] == "build_suites.py"}
    (d / "build_suites.py").write_text("REVISIONS = " + repr(revs) + "\n" + "\n".join(
        f"load({s['repo']!r}, {s['config']!r}, split={s['split']!r})" if s["config"] else f"load({s['repo']!r}, split={s['split']!r})"
        for s in sw["src"].values() if s["script"] == "build_suites.py") + "\n")
    revs2 = {s["repo"]: s["revision"] for s in sw["src"].values() if s["script"] == "build_arabic.py"}
    (d / "build_arabic.py").write_text("REVISIONS = " + repr(revs2) + "\n" + "\n".join(
        f"load({s['repo']!r}, {s['config']!r}, split={s['split']!r})" for s in sw["src"].values() if s["script"] == "build_arabic.py") + "\n")
    assert S.revision_problems(sw["src"], d) == []
    other = copy.deepcopy(sw["src"])
    other["boolq_validation"]["revision"] = "0" * 40
    probs = S.revision_problems(other, d)
    assert len(probs) == 1 and "boolq_validation" in probs[0] and "is not the one build_suites.py pins" in probs[0]
    other = copy.deepcopy(sw["src"])
    other["sst5_test"]["split"] = "validation"
    assert any("does not load SetFit/sst5 split validation" in p for p in S.revision_problems(other, d))
    with pytest.raises(S.SobError, match="the full-split build is refused"):
        S.build_splits(sw["cases"], sw["lock"], tmp_path / "u.jsonl", tmp_path / "o", hub=sw["hub"], sources=other, scripts_dir=d)
    assert not (tmp_path / "u.jsonl").exists() and not (tmp_path / "o").exists()


def test_the_ruling_draft_hash_in_the_pins_is_the_drafts():
    d = C2B / "zed_orch" / "sb_blocks" / "A58_DRAFT.md"
    if not d.is_file():
        pytest.skip("the A58 draft is not here")
    assert hashlib.sha256(d.read_bytes()).hexdigest() == S.SPLITS_RULING["draft_sha256"]


# ---- the units ----------------------------------------------------------------------------------------------------------------------
def test_one_unit_per_item_with_the_expected_counts_and_parts(built):
    us = units_of(built["units"])
    by = {}
    for u in us:
        by.setdefault(u["split"], []).append(u)
    assert {k: len(v) for k, v in by.items()} == {"sst5_test": 12, "sst2_validation": 10, "boolq_validation": 14, "xnli_ar_test": 12, "xnli_en_test": 12,
                                                 "xnli_fr_test": 12, "tweet_ar_test": 9, "miracl_ar_dev": 4}
    assert len({u["call_id"] for u in us}) == len(us) == 12 + 10 + 14 + 36 + 9 + 4
    assert set(map(lambda u: tuple(u), us)) == {("call_id", "split", "parts")}                      # no gold, no label, no other column
    sw = built["sw"]
    assert by["sst5_test"][3]["parts"] == {"review": sw["rows"]["sst5_test"][3]["text"]} and by["sst5_test"][3]["call_id"] == "sst5_test:3"
    # xnli: premise and hypothesis together in one unit, one unit per language and item (parallel items are separate units)
    for lang in ("ar", "en", "fr"):
        u = by[f"xnli_{lang}_test"][5]
        assert set(u["parts"]) == {"premise", "hypothesis"} and u["parts"]["premise"].startswith(lang + " ")
    # boolq: question and passage together (the question without the bench's "?")
    assert set(by["boolq_validation"][0]["parts"]) == {"question", "passage"} and not by["boolq_validation"][0]["parts"]["question"].endswith("?")
    assert built["pins"]["sob_splits"]["files"][built["rel"]]["rows"] == len(us)


def test_the_label_and_gold_columns_are_never_written(built):
    blob = built["units"].read_text(encoding="utf-8")
    assert LABEL_MARK not in blob and '"gold"' not in blob and '"label"' not in blob and '"answer"' not in blob


def test_miracl_units_are_the_replayed_queries_with_their_full_unclipped_passages(built):
    sw = built["sw"]
    us = [u for u in units_of(built["units"]) if u["split"] == "miracl_ar_dev"]
    assert len(us) == 4
    rr, pr = us[:2], us[2:]
    for u, (qid, docs) in zip(rr, sw["rerank"]):
        assert u["call_id"] == f"miracl_ar_dev:{qid}" and u["parts"]["query"] == sw["queries"][qid]
        assert [u["parts"][f"p{j}"] for j in range(len(docs))] == [sw["text"][d] for d in docs] and len(u["parts"]) == 1 + len(docs)
    for u, (qid, d) in zip(pr, sw["pair"]):
        assert u["parts"] == {"query": sw["queries"][qid], "p0": sw["text"][d]}
    assert all(len(p) > sw["src"]["miracl_ar_dev"]["clip"] for u in us for k, p in u["parts"].items() if k.startswith("p"))      # not clipped
    assert {u["call_id"] for u in rr}.isdisjoint({u["call_id"] for u in pr})
    rec = built["pins"]["sob_splits"]["splits"]["miracl_ar_dev"]
    assert rec["queries_used"] == 4 and rec["passage_uses"] == 2 * 3 + 2 and rec["usable_queries"] == 12 and rec["bench_cases"] == rec["bench_cases_linked"] == 4


def test_the_bench_sample_is_replayed_for_every_split(built):
    for k, rec in built["pins"]["sob_splits"]["splits"].items():
        assert rec["bench_cases"] == rec["bench_cases_linked"] > 0, k
    assert built["pins"]["sob_splits"]["splits"]["xnli_fr_test"]["bench_cases"] == N_SAMPLE


# ---- refusals: nothing is written ------------------------------------------------------------------------------------------------------
def _refused(sw, tmp_path, match, **kw):
    u, o = tmp_path / "ref" / "u.jsonl", tmp_path / "ref" / "o"
    with pytest.raises(S.SobError, match=match) as e:
        S.build_splits(sw["cases"], sw["lock"], u, o, hub=sw["hub"], check_scripts=False, **{"sources": sw["src"], **kw})
    assert not u.exists() and not o.exists()
    return str(e.value)


def test_a_count_that_differs_from_a58_is_refused_and_reported(sw, tmp_path):
    sw["src"]["xnli_en_test"]["a58"] = 13
    msg = _refused(sw, tmp_path, "refused")
    assert "xnli_en_test: 12 items, A58 names 13" in msg and sw["rows"]["xnli_en_test"][0]["premise"] not in msg


def test_an_explicit_accept_count_must_equal_the_actual_count_and_is_recorded(sw, tmp_path):
    sw["src"]["tweet_ar_test"]["a58"] = 256
    assert "tweet_ar_test: 9 items, A58 names 256" in _refused(sw, tmp_path, "refused")
    assert "accepted 8, not 9" in _refused(sw, tmp_path, "refused", accept_counts={"tweet_ar_test": 8})
    pins = do_build(sw, tmp_path / "ok", accept_counts={"tweet_ar_test": 9})["sob_splits"]
    assert pins["complete"] is True and pins["count_deviations"] == [{"split": "tweet_ar_test", "a58": 256, "actual": 9}]
    assert pins["splits"]["tweet_ar_test"]["a58_count"] == 256 and pins["splits"]["tweet_ar_test"]["count"] == 9


def test_a_stale_or_unknown_accept_count_is_refused(sw, tmp_path):
    assert "accepted count 9 but A58's 9 is right" in _refused(sw, tmp_path, "refused", accept_counts={"tweet_ar_test": 9})
    assert "no_such_split: --accept-count names no such split" in _refused(sw, tmp_path, "refused", accept_counts={"no_such_split": 1})
    assert "accepted count 4" in _refused(sw, tmp_path, "refused", accept_counts={"miracl_ar_dev": 4})


def test_a_bench_suite_not_drawn_from_the_split_is_refused(sw, tmp_path):
    cases = copy.deepcopy(sw["case_list"])
    c = next(x for x in cases if x["suite"] == "boolq")
    c["state"]["question"] = "a question that is not in the split at all?"
    cp, lp = write_bench(tmp_path / "bench2", cases)
    sw2 = dict(sw, cases=cp, lock=lp)
    msg = _refused(sw2, tmp_path, "refused")
    assert "boolq_validation: 3 of the bench's 4 boolq cases" in msg


def test_a_miracl_replay_that_does_not_give_the_benchs_cases_is_refused(sw, tmp_path):
    cases = copy.deepcopy(sw["case_list"])
    c = next(x for x in cases if x["suite"] == "ar_miracl_rerank")
    q = c["questions"]["passage"]
    keys = list(q["criteria"])
    q["criteria"][keys[0]], q["criteria"][keys[1]] = q["criteria"][keys[1]], q["criteria"][keys[0]]     # the option order differs
    cp, lp = write_bench(tmp_path / "bench3", cases)
    assert "3 of the bench's 4 ar_miracl cases" in _refused(dict(sw, cases=cp, lock=lp), tmp_path, "refused")
    sw["src"]["miracl_ar_dev"]["hub_counts"]["corpus"] += 1
    assert "corpus has 72 rows, the hub's dataset card says 73" in _refused(sw, tmp_path, "refused")


def test_a_cached_file_that_is_not_its_hub_blob_is_refused(sw, tmp_path):
    s = sw["src"]["sst2_validation"]
    snap = sw["hub"] / "datasets--stanfordnlp--sst2" / "snapshots" / s["revision"]
    f = snap / s["files"][0]
    data = f.read_bytes()
    blobs = sw["hub"] / "datasets--stanfordnlp--sst2" / "blobs"
    blobs.mkdir()
    (blobs / hashlib.sha256(data).hexdigest()).write_bytes(data)
    f.unlink()
    f.symlink_to(Path("..") / ".." / ".." / "blobs" / hashlib.sha256(data).hexdigest())                    # the hub's layout: a link named by the sha256
    assert S.read_source_file(s["repo"], s["revision"], s["files"][0], sw["hub"])[1]["blob_check"] == "lfs_sha256"
    (blobs / hashlib.sha256(data).hexdigest()).write_bytes(data + b" ")                                      # the content no longer is that blob
    assert "not the hub blob" in _refused(sw, tmp_path, "refused")


def test_a_source_file_missing_from_the_cache_is_refused_with_the_fetch_command(sw, tmp_path):
    s = sw["src"]["boolq_validation"]
    (sw["hub"] / "datasets--google--boolq" / "snapshots" / s["revision"] / s["files"][0]).unlink()
    assert "fetch-splits" in _refused(sw, tmp_path, "refused")


def test_a_changed_bench_case_file_is_refused_by_the_lock(sw, tmp_path):
    cases = copy.deepcopy(sw["case_list"])
    cases[0]["state"] = dict(cases[0]["state"], extra="x")
    cp = tmp_path / "other_cases.jsonl"
    cp.write_text("".join(json.dumps(c) + "\n" for c in cases))
    with pytest.raises(S.SobError, match="do not match their lock"):
        S.build_splits(cp, sw["lock"], tmp_path / "u.jsonl", tmp_path / "o", hub=sw["hub"], sources=sw["src"], check_scripts=False)
    assert not (tmp_path / "u.jsonl").exists()


# ---- pins and exports: no plain text -------------------------------------------------------------------------------------------------
def test_pins_and_exports_hold_no_plain_split_text(built):
    texts = {s for u in units_of(built["units"]) for s in S._strings(u["parts"]) if len(s) >= 10}
    assert len(texts) > 100
    for name in ("splits_pins.json", "SPLITS_MANIFEST.json", "splits_unit_hashes.json"):
        body = (built["out"] / name).read_text(encoding="utf-8")
        assert not [t for t in texts if t in body], name
    h = json.loads((built["out"] / "splits_unit_hashes.json").read_text())
    assert len(h) == len(units_of(built["units"])) and all(re.fullmatch(r"[0-9a-f]{64}", v) for v in h.values())
    assert built["units"].read_text(encoding="utf-8").count(sent("review", 3)) >= 1                    # the one file with split text is the units file


def test_the_pin_record_names_every_source_by_revision_file_sha_and_count(built):
    p = built["pins"]["sob_splits"]
    assert p["complete"] is True and p["gaps"] == [] and p["count_deviations"] == [] and p["ruling"]["draft_sha256"] == S.SPLITS_RULING["draft_sha256"]
    assert p["files"][built["rel"]]["sha256"] == g.sha256_file(built["units"])
    assert S.gap_for("sob_splits", {"sob_splits": p}) is None and S.gap_for("sob_splits") is None
    sw = built["sw"]
    assert p["source"]["file_sha256"] == S.sha_bytes(sw["cases"].read_bytes()) and p["source"]["cases"] == len(sw["case_list"])
    for k, rec in p["splits"].items():
        s = sw["src"][k]
        assert rec["revision"] == s["revision"] and rec["dataset"] == s["repo"] and rec["split"] == s["split"] and rec["count"] == rec["units"]
        assert set(rec["files"]) == set(s["files"]) and all(re.fullmatch(r"[0-9a-f]{64}", f["sha256"]) for f in rec["files"].values())
        assert re.fullmatch(r"[0-9a-f]{64}", rec["items_sha256"])
    assert S.pinned_files({"sob_splits": p}) == {built["rel"]: g.sha256_file(built["units"])}
    assert S.splits_pin_problems(units_of(built["units"]), built["pins"]) == []


def test_gap_for_the_splits_target_needs_a_complete_pin_of_the_units_and_the_source(built):
    p = built["pins"]["sob_splits"]
    assert "not built yet" in S.gap_for("sob_splits", {}) and "splits_pins.json" in S.gap_for("sob_splits", {})
    assert "incomplete" in S.gap_for("sob_splits", {"sob_splits": dict(p, complete=False)})
    assert "incomplete" in S.gap_for("sob_splits", {"sob_splits": dict(p, gaps=["x"])})
    assert "does not pin the units" in S.gap_for("sob_splits", {"sob_splits": dict(p, files={})})
    assert "source sha256" in S.gap_for("sob_splits", {"sob_splits": dict(p, source={})})


def test_the_units_against_the_pins_see_a_changed_or_dropped_item(built):
    pins, us = built["pins"], units_of(built["units"])
    us2 = copy.deepcopy(us)
    us2[0]["parts"]["review"] += " edited"
    assert any("sst5_test: the units' items differ" in x for x in S.splits_pin_problems(us2, pins))
    assert any("sst5_test: 11 units" in x for x in S.splits_pin_problems(us[1:], pins))
    assert any("splits in the units file are not pinned" in x for x in S.splits_pin_problems(us + [dict(us[0], split="new_split")], pins))


def test_exports_refuse_tampering_other_pins_and_missing_files(tmp_path, built):
    pins, out = {"sob_splits": built["pins"]["sob_splits"]}, built["out"]
    ex = S.SplitExports(out, pins)
    assert len(ex.unit_hashes) == 12 + 10 + 14 + 36 + 9 + 4 and ex.counts["splits"] == 8 and set(ex.shas) == {"manifest", "splits_unit_hashes.json"}
    assert S.units_file_problems(built["units"], ex) == []
    other = json.loads(json.dumps(pins))
    other["sob_splits"]["files"][built["rel"]]["sha256"] = "0" * 64
    with pytest.raises(S.SobError, match="another units file"):
        S.SplitExports(out, other)
    with pytest.raises(S.SobError, match="SPLITS_MANIFEST"):
        S.SplitExports(tmp_path / "absent", pins)
    d = tmp_path / "tamper"
    shutil.copytree(out, d)
    with open(d / "splits_unit_hashes.json", "a") as f:
        f.write(" ")
    with pytest.raises(S.SobError, match="differs"):
        S.SplitExports(d, pins)
    d2 = tmp_path / "count"
    shutil.copytree(out, d2)
    man = json.loads((d2 / "SPLITS_MANIFEST.json").read_text())
    man["counts"]["units"] += 1
    (d2 / "SPLITS_MANIFEST.json").write_text(json.dumps(man))
    with pytest.raises(S.SobError, match="SPLITS_MANIFEST.json says"):
        S.SplitExports(d2, pins)


def test_a_changed_units_file_is_found_against_the_exports(built):
    ex = S.SplitExports(built["out"], {"sob_splits": built["pins"]["sob_splits"]})
    us = units_of(built["units"])
    us[0]["parts"]["review"] += " edited"
    built["units"].write_text("".join(json.dumps(u, ensure_ascii=False) + "\n" for u in us), encoding="utf-8")
    assert "1 units differ" in " ".join(S.units_file_problems(built["units"], ex))
    built["units"].write_text("".join(json.dumps(u, ensure_ascii=False) + "\n" for u in us[:-1]), encoding="utf-8")
    assert "lacks 1 of its units" in " ".join(S.units_file_problems(built["units"], ex))


def test_the_sob_text_exports_and_pins_are_untouched_by_the_splits_build(built):
    names = {p.name for p in built["out"].iterdir()}
    assert names == {"splits_pins.json", "SPLITS_MANIFEST.json", "splits_unit_hashes.json"}          # no sob_pins.json / MANIFEST.json / unit_hashes.json here
    assert S.SobExports.FILES == ("unit_hashes.json",) and S.TARGETS == ("sob_text",) and S.ALL_TARGETS == ("sob_text", "sob_splits")


def test_verify_scanned_compares_the_engines_file_sha_with_the_splits_pin(built):
    pins = {"sob_splits": built["pins"]["sob_splits"]}
    sha = g.sha256_file(built["units"])
    assert S.verify_scanned({built["rel"]: sha}, pins, names=S.SPLIT_TARGETS, require=True) == []
    assert "is not the pinned one" in S.verify_scanned({built["rel"]: "1" * 64}, pins, names=S.SPLIT_TARGETS)[0]
    assert "was not scanned" in S.verify_scanned({}, pins, names=S.SPLIT_TARGETS, require=True)[0]
    assert S.verify_scanned({}, pins, require=True) == []                                           # the default names are sob_text only


# ---- the 5-word rule, stated as a limitation -------------------------------------------------------------------------------------------
def test_the_word_rule_counts_items_with_no_content_text_of_five_words(built):
    us = units_of(built["units"])
    sst2 = S.word_rule_effect([u for u in us if u["split"] == "sst2_validation"])
    assert sst2["units"] == 10 and sst2["no_content_5w"] == 1 and sst2["no_text_5w"] == 1 and sst2["content_ge10"] == 9      # "a dull mess": 3 words
    xn = S.word_rule_effect([u for u in us if u["split"] == "xnli_en_test"])
    assert xn["units"] == 12 and xn["parts_below_5w"] == 1 and xn["no_content_5w"] == 0                                    # the 2-word hypothesis of item 1
    unit = lambda a, b: {"parts": {"premise": a, "hypothesis": b}}                                                          # noqa: E731
    eff = S.word_rule_effect([unit("one two three four five six", "x y"), unit("a b c", "d e f g"), unit("one two three four five six seven eight nine ten", "q")])
    assert eff == {"units": 3, "no_content_5w": 1, "no_text_5w": 1, "parts_below_5w": 3, "content_5_9": 1, "content_ge10": 1}
    for k, rec in built["pins"]["sob_splits"]["splits"].items():
        assert rec["word_rule_5"]["units"] == rec["units"], k
    assert built["pins"]["sob_splits"]["counts"]["word_rule_5"]["units"] == len(us)


# ---- registration ---------------------------------------------------------------------------------------------------------------------------
def test_the_splits_units_file_is_readable_by_the_engine_without_an_allow_list_entry():
    assert S.SPLITS_UNITS_REL == "vision_bench/text_track/data/sob_g13_splits_units.jsonl" and g.allowed(g.REPO / S.SPLITS_UNITS_REL)
    assert not g.REPO.joinpath(S.SPLITS_UNITS_REL).is_relative_to(g.LEAN.parent)                      # derived next to the bench data, not under opendecide-data
    assert c2io.refusal(g.REPO / S.SPLITS_UNITS_REL) is None and not c2io.refusal(S.SPLITS_PINS) and not c2io.refusal(S.SPLITS_EXPORT_MANIFEST)
    parts = [x.lower() for x in Path(S.SPLITS_UNITS_REL).parts]
    assert not any("ohs" in x or "jev" in x or "sealed" in x for x in parts) and not any(x in ("runs", "results", "_work", "preds") for x in parts)
    assert S.QUARANTINE_OK == ()


def test_the_split_target_dict_is_blind_generic_all_methods_with_the_parts_field(built):
    t, = S.split_targets({"sob_splits": built["pins"]["sob_splits"]})
    assert t["name"] == "sob_splits" and t["blind"] is True and t["kind"] == "generic" and t["methods"] == "all" and t["status"] is None
    assert t["paths"] == ["repo:" + built["rel"]] and t["fields"] == ("parts",) and t["gap"] is None and t["note"] == S.SPLIT_NOTES["sob_splits"]
    assert "not built yet" in S.split_targets({})[0]["gap"]
    sob_like = S.targets({})[0]
    assert set(t) == set(sob_like)
    both = S.all_targets({"sob_splits": built["pins"]["sob_splits"]})
    assert [x["name"] for x in both] == ["sob_text", "sob_splits"]


def test_the_engine_reads_the_values_of_parts_not_its_keys_nor_ids(built):
    us = units_of(built["units"])
    leaves = [x for u in us for x in g.leaves(u, S.SPLIT_FIELDS)]
    assert sent("review", 3) in leaves and all(k not in leaves for k in ("premise", "hypothesis", "review", "query", "sst5_test:3", "sst5_test"))
    assert not [x for x in leaves if x.startswith("miracl_ar_dev:")]


def test_the_guard_files_and_export_records_name_each_targets_own_files(built, monkeypatch):
    monkeypatch.setattr(S, "SOB_DIR", built["out"])
    both = {p.name for p in S.guard_files(True)}
    assert {"sob_g13.py", "sob_pins.json", "MANIFEST.json", "unit_hashes.json", "splits_pins.json", "SPLITS_MANIFEST.json", "splits_unit_hashes.json"} <= both
    only = {p.name for p in S.guard_files(("sob_splits",))}
    assert "splits_pins.json" in only and "sob_pins.json" not in only
    assert "sob_pins.json" in {p.name for p in S.guard_files(("sob_text",))} and "splits_pins.json" not in {p.name for p in S.guard_files(("sob_text",))}
    pins = {"sob_splits": built["pins"]["sob_splits"]}
    rec, why = S.export_record("sob_splits", pins)
    assert why == [] and rec["status"] == "verified" and rec["units"] == 85 and set(rec["splits"]) == set(built["pins"]["sob_splits"]["splits"]) and rec["count_deviations"] == []
    json.dumps(rec)
    bad = json.loads(json.dumps(pins))
    bad["sob_splits"]["files"][built["rel"]]["sha256"] = "0" * 64
    rec, why = S.export_record("sob_splits", bad)
    assert rec["status"].startswith("refused") and why and why[0].startswith("sob_splits_exports:")
    assert S.export_record("sob_text", {})[1][0].startswith("sob_exports:")


def test_main_exits_2_on_a_refusal_and_prints_no_text(monkeypatch, capsys):
    def refuse(**kw):
        raise S.SobError("tweet_ar_test: 870 items, A58 names 256")
    monkeypatch.setattr(S, "build_splits", refuse)
    assert S.main(["build-splits"]) == 2
    assert "A58 names 256" in capsys.readouterr().out
    assert S.main(["build-splits", "--accept-count", "x"]) == 2


def test_the_status_reports_the_splits_target(monkeypatch, tmp_path):
    monkeypatch.setattr(S, "SPLITS_PINS", tmp_path / "none.json")
    st = S.status()["splits"]
    assert st["pins"] is False and st["complete"] is False and "not built yet" in st["gap"]


# ---- the engine finds a planted split text (positive control) and leaves clean rows alone (negative control) --------------------------
@pytest.fixture()
def split_run(world, built):
    pins = {"sob_splits": built["pins"]["sob_splits"]}
    t, = S.split_targets(pins)
    t["paths"] = [f"abs:{built['units']}"]
    sw = built["sw"]
    xnli_p = sw["rows"]["xnli_en_test"][4]["premise"]
    bq = sw["rows"]["boolq_validation"][6]
    mir = sw["text"][sw["rerank"][0][1][1]]
    sst5 = sw["rows"]["sst5_test"][7]["text"]
    tw = sw["rows"]["tweet_ar_test"][5]["text"]
    near = " ".join(sw["rows"]["sst5_test"][9]["text"].split()[:-1]) + " different"
    extra = [row(30, "Daily notes. " + xnli_p + ". End of notes.", call="p_xnli_premise"),
             row(31, "Passage: " + bq["passage"] + "\nQuestion: " + bq["question"] + "?", call="p_boolq"),
             row(32, "Quote from the archive: " + mir + " and nothing else.", call="p_miracl_full_passage"),
             row(33, "Another clean state about a lighthouse keeper repainting railings.", call="p_sst5", options=[sst5, "other"]),
             row(34, "Tweet follows: " + tw, call="p_tweet"),
             row(35, near + " end", call="p_near_exact_sst5"),
             row(36, "Clean state number thirty six about a bakery that sells forty loaves each morning at a fixed price.", call="clean_a"),
             row(37, "A different story entirely: the lighthouse keeper repainted the railings before the first frost came.", call="clean_b",
                 instructions="Say which of the two ferry timetables is faster.", card="- fast: the ferry that stops less often"),
             row(38, "a dull mess", call="p_short_exact"),
             row(39, "He called the whole film a dull mess and left early on a cold night.", call="short_embedded")]
    world["cand"].write_text(world["cand"].read_text() + "".join(json.dumps(r, ensure_ascii=False) + "\n" for r in extra))
    return {"world": world, "tgs": world["tgs"] + [t], "pins": pins, "target": t, "built": built}


def _cand(sr, **kw):
    w = sr["world"]
    return G.run("candidates", ["T98"], embed=False, side=False, tgs=sr["tgs"], exports=w["exports"], write=False, prereg_text=A38, **kw)["c2_cand_T98"]


def test_a_planted_split_text_is_found_by_the_target_and_clean_rows_are_not(split_run):
    rec = _cand(split_run)
    planted = {"r30", "r31", "r32", "r33", "r34", "r35"}
    assert planted <= set(rec["drop_ids"]), sorted(planted - set(rec["drop_ids"]))
    assert not {"r36", "r37"} & set(rec["drop_ids"])                                     # negative control: unrelated rows keep
    by = rec["counts_by_target_and_method"]["sob_splits"]
    assert sum(1 for c in by.values() if c["units"] >= 1) >= 3                            # more than one method sees them: exact / n-gram / substring ...
    assert any(m in by for m in ("ngram10", "ngram12")) and any(m in by for m in ("exact_full", "substring", "exact_seg"))
    assert rec["engine"]["targets"]["sob_splits"]["status"] == "scanned"
    s = json.dumps(rec, ensure_ascii=False)
    sw = split_run["built"]["sw"]
    assert sw["rows"]["xnli_en_test"][4]["premise"] not in s and sw["rows"]["boolq_validation"][6]["passage"] not in s       # the record holds no split text


def test_the_five_word_rule_a_short_item_is_found_only_as_a_whole_text(split_run):
    rec = _cand(split_run)
    assert "r38" in rec["drop_ids"] and "r39" not in rec["drop_ids"]                      # exact whole-text match yes; the same words inside a longer state no
    tg = rec["engine"]["targets"]["sob_splits"]
    assert tg["status"] == "scanned"


def test_a_run_whose_rows_never_touch_the_splits_has_no_split_hits(world, built):
    pins = {"sob_splits": built["pins"]["sob_splits"]}
    t, = S.split_targets(pins)
    t["paths"] = [f"abs:{built['units']}"]
    rec = G.run("candidates", ["T98"], embed=False, side=False, tgs=world["tgs"] + [t], exports=world["exports"], write=False,
                prereg_text=A38)["c2_cand_T98"]
    assert "sob_splits" not in rec["counts_by_target_and_method"] and rec["engine"]["targets"]["sob_splits"]["status"] == "scanned"


# ---- the wiring (needs the patched g13_c2.py) ------------------------------------------------------------------------------------------------
@wired
def test_wired_sob_splits_joins_exactly_where_sob_text_joins(monkeypatch, tmp_path):
    monkeypatch.setattr(S, "PINS", tmp_path / "no_pins.json")
    monkeypatch.setattr(S, "SPLITS_PINS", tmp_path / "no_splits_pins.json")
    for run in ("seed", "candidates", "carry", "final"):
        b = {t["name"] for t in G.engine_targets(run)}
        assert not b & set(S.ALL_TARGETS), run
        assert {t["name"] for t in G.engine_targets(run, False, True)} == b | {"sob_text", "sob_splits"}, run
        assert {t["name"] for t in G.engine_targets(run, True, True)} >= b | {"sob_text", "sob_splits", "di03_public", "di_src_splits"}, run
    t = {x["name"]: x for x in G.engine_targets("final", False, True)}
    assert t["sob_splits"]["gap"] and "not built yet" in t["sob_splits"]["gap"] and t["sob_text"]["gap"]
    for run, sets, want in (("final", {}, True), ("seed", {"s": {"block": "SB5", "units": []}}, False), ("candidates", {"s": {"block": "SB5", "units": []}}, True),
                            ("carry", {"s": {"block": "F5", "units": []}}, False)):
        assert S.needs_sob(run, sets) is want                                             # one decision for both targets


@wired
def test_wired_run_guard_lists_the_splits_files_only_for_a_run_that_holds_the_target(world):
    sets = {"s": {"block": "T98", "train_shas": {}, "seed_shas": {}, "units": []}}
    names = lambda gd: {Path(k).name for k in gd.start}                                      # noqa: E731
    plain = names(G.run_guard("candidates", sets, False))
    text_only = names(G.run_guard("candidates", sets, False, ["sob_text"]))
    both = names(G.run_guard("candidates", sets, False, ["sob_text", "sob_splits"]))
    assert not {"splits_pins.json", "sob_g13.py"} & plain and "sob_g13.py" in text_only and "splits_pins.json" not in text_only
    assert "sob_g13.py" in both and plain <= text_only <= both
    for n in ("sob_g13.py", "sob_pins.json", "MANIFEST.json", "unit_hashes.json", Path(S.UNITS_REL).name):
        assert n in text_only and n in both
    assert "sob_pins.json" not in names(G.run_guard("candidates", sets, False, ["sob_splits"]))
    for p in S.guard_files(True):
        if p.is_file():
            assert p.name in both, p.name                                                      # (a file that is not built yet is not hashed)


@wired
def test_wired_a_run_with_the_splits_target_records_verified_exports_and_complete_pins(split_run, built):
    rec = _cand(split_run)
    r = rec["sob_splits"]
    assert r["status"] == "verified" and r["units"] == 85 and set(r["sha256"]) == {"manifest", "splits_unit_hashes.json"} and "sob" not in rec
    assert r["source"]["file_sha256"] == built["pins"]["sob_splits"]["source"]["file_sha256"] and r["count_deviations"] == []
    assert not any("sob_" in x or "pinned" in x for x in rec["incomplete_why"]), rec["incomplete_why"]
    assert any(Path(k).name == "sob_g13.py" for k in rec["inputs_at_start"]) and any(Path(k).name == "splits_pins.json" for k in rec["inputs_at_start"])
    json.dumps(rec)


@wired
def test_wired_both_targets_in_one_run_each_record_their_own_exports(world, built, tmp_path, monkeypatch):
    """sob_text built by the sob_g13 test fixture's recipe (a tiny bench), sob_splits by this module's: both verified, both keys, nothing mixed."""
    import test_sob_g13 as T
    cp, lp = T.write_bench(tmp_path / "textbench")
    tunits, tout = tmp_path / "scan_t" / "sob_units.jsonl", tmp_path / "g13_sob_t"
    trel = g.rel_of(tunits)
    for k, v in (("EXPECTED_CASES", 4), ("EXPECTED_SUITES", 4), ("UNITS_REL", trel), ("FILES", {"sob_text": (trel,)}), ("PINS", tout / "sob_pins.json"),
                 ("EXPORT_MANIFEST", tout / "MANIFEST.json"), ("SOB_DIR", tout)):
        monkeypatch.setattr(S, k, v)
    S.build(cp, lp, tunits, tout)
    for n in ("SPLITS_MANIFEST.json", "splits_unit_hashes.json"):                       # SplitExports reads SOB_DIR: put the splits exports next to the text ones
        shutil.copy(built["out"] / n, tout / n)
    pins = {**json.loads((tout / "sob_pins.json").read_text()), "sob_splits": built["pins"]["sob_splits"]}
    ta, tb = S.targets(pins)[0], S.split_targets(pins)[0]
    ta["paths"], tb["paths"] = [f"abs:{tunits}"], [f"abs:{built['units']}"]
    monkeypatch.setattr(S, "load_all_pins", lambda: pins)
    rec = G.run("candidates", ["T98"], embed=False, side=False, tgs=world["tgs"] + [ta, tb], exports=world["exports"], write=False, prereg_text=A38)["c2_cand_T98"]
    assert rec["sob"]["status"] == "verified" and rec["sob_splits"]["status"] == "verified" and rec["sob"]["units"] == 4 and rec["sob_splits"]["units"] == 85
    assert not any("sob_" in x or "pinned" in x for x in rec["incomplete_why"]), rec["incomplete_why"]


@wired
def test_wired_a_run_with_only_the_text_target_has_no_splits_key(world):
    rec = _run(world, "candidates", G.c2_dev_targets())["c2_cand_T98"]
    assert "sob_splits" not in rec and "sob" not in rec and "sob_splits" not in rec["counts_by_target_and_method"]


@wired
def test_wired_broken_splits_exports_make_the_log_incomplete(split_run, built):
    (built["out"] / "splits_unit_hashes.json").write_text("{}")
    rec = _cand(split_run)
    assert rec["sob_splits"]["status"].startswith("refused") and any(x.startswith("sob_splits_exports:") for x in rec["incomplete_why"]) and not rec["complete"]


@wired
def test_wired_a_scanned_units_file_that_is_not_the_pinned_one_is_flagged(split_run, built):
    pins = json.loads(S.SPLITS_PINS.read_text())
    pins["sob_splits"]["files"][built["rel"]]["sha256"] = "9" * 64
    S.SPLITS_PINS.write_text(json.dumps(pins))
    rec = _cand(split_run)
    assert (any("is not the pinned one" in x for x in rec["incomplete_why"]) or rec["sob_splits"]["status"].startswith("refused")) and not rec["complete"]


@wired
def test_wired_an_unbuilt_splits_target_keeps_the_log_incomplete(world, tmp_path, monkeypatch):
    monkeypatch.setattr(S, "SPLITS_PINS", tmp_path / "none.json")
    t, = S.split_targets()
    t["paths"] = []
    rec = G.run("candidates", ["T98"], embed=False, side=False, tgs=world["tgs"] + [t], exports=world["exports"], write=False,
                prereg_text=A38)["c2_cand_T98"]
    assert not rec["complete"] and any("sob_splits: not built yet" in x for x in rec["incomplete_why"])


# ---- the real splits (built from the real sources; counts and booleans only) --------------------------------------------------------------
def real_files():
    env = os.environ.get("SOB_SPLITS_SCRATCH")
    if env:
        d = Path(env)
        return d / "units.jsonl", d / "g13_sob"
    return g.REPO / S.SPLITS_UNITS_REL, S.SOB_DIR


def real_ready() -> bool:
    u, o = real_files()
    return u.is_file() and (o / "splits_pins.json").is_file()


@pytest.mark.skipif(not real_ready(), reason="sob_g13.py build-splits has not been run here (and no SOB_SPLITS_SCRATCH)")
def test_the_real_splits_have_a58s_counts_or_a_recorded_deviation_and_consistent_pins_and_exports():
    units_path, out = real_files()
    pins = S.load_pins(out / "splits_pins.json")
    p = pins["sob_splits"]
    assert p["complete"] is True and p["gaps"] == [] and S.gap_for("sob_splits", pins) is None
    dev = {d["split"]: d for d in p["count_deviations"]}
    for k, n in A58_COUNTS.items():
        rec = p["splits"][k]
        assert rec["count"] == rec["units"] == (dev[k]["actual"] if k in dev else n), k
        assert rec["bench_cases_linked"] == rec["bench_cases"] > 0
        assert all(f["blob_check"] in ("lfs_sha256", "git_blob_sha1") for f in rec["files"].values()), k              # the hub's own blob ids agree
    assert set(dev) <= {"tweet_ar_test"} and all(d["a58"] == A58_COUNTS[d["split"]] for d in dev.values())
    m = p["splits"]["miracl_ar_dev"]
    assert m["queries_used"] == 400 == m["bench_cases"] == m["bench_cases_linked"] and m["passages_used"] <= m["passage_uses"] == 1800 and m["dev_queries"] == 2896
    if (g.REPO / S.SCRIPTS_REL / "build_suites.py").is_file():
        assert all(p["splits"][k]["revision"] == v["revision"] for k, v in S.SPLIT_SOURCES.items())
        assert S.revision_problems(S.SPLIT_SOURCES) == []
    us = units_of(units_path)
    assert len(us) == p["files"][S.SPLITS_UNITS_REL]["rows"] == p["counts"]["units"] == sum(r["units"] for r in p["splits"].values())
    assert S.splits_pin_problems(us, pins) == []
    ex = S.SplitExports(out, pins)
    assert S.units_file_problems(units_path, ex) == [] and len(ex.unit_hashes) == len(us)
    assert p["files"][S.SPLITS_UNITS_REL]["sha256"] == g.sha256_file(units_path)


@pytest.mark.skipif(not real_ready(), reason="sob_g13.py build-splits has not been run here (and no SOB_SPLITS_SCRATCH)")
def test_the_real_exports_hold_no_plain_split_text():
    units_path, out = real_files()
    texts = {s for u in units_of(units_path) for s in S._strings(u["parts"]) if len(s) >= 24}
    assert len(texts) > 10000
    body = "\n".join((out / n).read_text(encoding="utf-8") for n in ("splits_pins.json", "SPLITS_MANIFEST.json", "splits_unit_hashes.json"))
    assert not [t for t in texts if t in body]


@pytest.mark.skipif(not real_ready(), reason="sob_g13.py build-splits has not been run here (and no SOB_SPLITS_SCRATCH)")
def test_real_split_text_planted_in_fake_rows_is_found_by_the_real_units_and_clean_rows_are_not(world, tmp_path):
    """Positive / negative control on the REAL units: a real boolq passage, a real xnli_fr premise, a real MIRACL passage and a real tweet are planted in
    fake rows (never printed: only booleans are asserted)."""
    units_path, out = real_files()
    us = units_of(units_path)
    pick = lambda split, part, n=12: next(u["parts"][part] for u in us if u["split"] == split and len(u["parts"].get(part, "").split()) >= n)           # noqa: E731
    bq, fr, ar, mi, s5 = pick("boolq_validation", "passage", 20), pick("xnli_fr_test", "premise"), pick("tweet_ar_test", "tweet"), pick("miracl_ar_dev", "p0", 15), \
        pick("sst5_test", "review", 15)
    rows = [row(50, "Notes follow. " + bq + " End of notes.", call="real_boolq"),
            row(51, "Compte rendu: " + fr, call="real_xnli_fr"),
            row(52, "Archive: " + mi, call="real_miracl_passage"),
            row(53, "Tweet: " + ar, call="real_tweet"),
            row(54, "Clean state fifty four about a bakery that sells forty loaves each morning.", call="clean_a", options=[s5, "x"]),
            row(55, "The lighthouse keeper repainted the railings before the first frost came to the bay.", call="clean_b",
                instructions="Say which of the two timetables is faster.", card="- fast: the ferry that stops less often")]
    world["cand"].write_text(world["cand"].read_text() + "".join(json.dumps(r, ensure_ascii=False) + "\n" for r in rows))
    pins = S.load_pins(out / "splits_pins.json")
    t, = S.split_targets(pins)
    eng_path = units_path
    if not units_path.is_relative_to(g.REPO):                      # a scratch build: the engine's input guard refuses the session temp folder, so scan a copy
        eng_path = tmp_path / "scan" / "units.jsonl"
        eng_path.parent.mkdir()
        shutil.copy(units_path, eng_path)
    t["paths"] = [f"abs:{eng_path}"]
    rec = G.run("candidates", ["T98"], embed=False, side=False, tgs=world["tgs"] + [t], exports=world["exports"], write=False, prereg_text=A38)["c2_cand_T98"]
    drop = set(rec["drop_ids"])
    found = {"r50", "r51", "r52", "r53", "r54"} <= drop
    clean = not ({"r55"} & drop)
    assert found and clean and rec["engine"]["targets"]["sob_splits"]["status"] == "scanned"
