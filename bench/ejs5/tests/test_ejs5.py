"""CPU tests for the ejs-5 kit, on SYNTHETIC items only (tests/make_synthetic.py) plus the real adapter dirs' tokenizer
and train_meta (no weights are loaded; the fake model is a tiny random Qwen3).

  cd bench/ejs5 && /Users/aryamahadik/Documents/jev/opendecide-data/.venv/bin/python -m pytest -q tests

Work files go to bench/ejs5/tests/_work (recreated on every session).
"""
from __future__ import annotations

import json
import random
import shutil
import sys
from pathlib import Path

import pytest

KIT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(KIT))
sys.path.insert(0, str(Path(__file__).resolve().parent))
import convert  # noqa: E402
import ejs5lib as E  # noqa: E402
import make_synthetic  # noqa: E402
import run_ejs5  # noqa: E402
import score_ejs5  # noqa: E402

WORK = Path(__file__).resolve().parent / "_work"
C1_DIR = E.ROOT / "backups" / "modal_models" / "q35_4b_main500k"
B2_DIR = E.ROOT / "backups" / "gcp_models" / "q35_2b_armI_1600"
C1_SHA = "507d1c29690579f928a265713cd14b9c54a34baa8b74abd1e641560d987db078"
C1_REV = "851bf6e806efd8d0a36b00ddf55e13ccb7b8cd0a"
B2_REV = "15852e8c16360a2fea060d615a32b45270f8a8fc"
LEAN = E.ROOT / "opendecide-data" / "lean"
need_c1 = pytest.mark.skipif(not (C1_DIR / "tokenizer.json").exists(), reason="C1 adapter dir not on this machine")
need_2b = pytest.mark.skipif(not (B2_DIR / "prism_x.json").exists(), reason="2B adapter dir not on this machine")


@pytest.fixture(scope="session")
def syn():
    if WORK.exists():
        shutil.rmtree(WORK)
    WORK.mkdir(parents=True)
    info = make_synthetic.make(WORK / "src")
    rows_path = WORK / "src" / "ejs5_rows.jsonl"
    meta = convert.main(["--src", str(WORK / "src"), "--out", str(rows_path), "--expect-n", str(info["n_rows"])])
    return {**info, "src": WORK / "src", "rows": rows_path, "meta": meta, "runs": WORK / "runs"}


# ------------------------------------------------------------------ the author's spec and rules

def test_bench_spec_reads_author_tasks():
    spec = E.bench_spec(E.QUAR / "run_public_bench.py")
    T = spec["TASKS"]
    assert list(T) == list(E.TASKS)
    assert spec["LEVELS"] == ["tiny", "small", "medium", "large"]
    assert [T[t]["kind"] for t in E.TASKS] == ["choice", "choice", "score", "noul"]
    assert list(T["route"]["criteria"]) == ["frontend", "backend"]
    assert list(T["triage"]["criteria"]) == ["fix", "feat", "refactor", "test"]
    assert len(T["score"]["criteria"]) == 4 and "criteria" not in T["gate"]


def _probs_for_ev(ev):
    """Four-level probabilities with expected level ev (mass on two adjacent levels)."""
    lo = min(2, int(ev))
    w = ev - lo
    p = [0.0] * 4
    p[lo] += 1 - w
    p[lo + 1] += w
    return dict(zip(["tiny", "small", "medium", "large"], p))


def test_decide_matches_author_jev_pred():
    jev_pred = E.author_functions(E.QUAR / "run_public_bench.py")["jev_pred"]
    srow = {"id": "x", "qtype": "choice", "options": ["tiny", "small", "medium", "large"], "meta": {"kind": "score"}}
    for ev in [0, 0.25, 0.49, 0.5, 0.51, 1.0, 1.5, 2.5, 2.49, 2.51, 3.0]:
        assert E.decide(srow, _probs_for_ev(ev))[0] == jev_pred({"score": ev}, "score")[0], ev
    rng = random.Random(0)
    for _ in range(2000):
        p = [rng.random() ** 3 for _ in range(4)]
        s = sum(p)
        probs = dict(zip(srow["options"], [x / s for x in p]))
        ev = E.expected_level(srow, probs)
        assert E.decide(srow, probs)[0] == jev_pred({"score": ev}, "score")[0]
    nrow = {"id": "y", "qtype": "noul", "options": None, "meta": {"kind": "noul"}}
    for p in [0.0, 0.2, 0.4999999, 0.5, 0.5000001, 0.8, 1.0]:
        ours = E.decide(nrow, {"yes": p, "no": 1 - p})
        theirs = jev_pred({"noul": p}, "noul")
        assert ours[0] == theirs[0] and abs(ours[1] - theirs[1]) < 1e-12, p
    crow = {"id": "z", "qtype": "choice", "options": ["fix", "feat", "refactor", "test"], "meta": {"kind": "choice"}}
    assert E.decide(crow, {"fix": .1, "feat": .2, "refactor": .6, "test": .1})[0] == "refactor"
    assert E.decide(crow, {"fix": .4, "feat": .4, "refactor": .1, "test": .1})[0] == "fix"  # first on an exact tie
    assert E.decide(crow, None) == (None, None)


# ------------------------------------------------------------------ convert

def test_convert_synthetic(syn):
    rows = E.read_jsonl(syn["rows"])
    spec = E.bench_spec(syn["src"] / "run_public_bench.py")
    assert len(rows) == syn["n_rows"]
    by = {t: [r for r in rows if r["meta"]["task"] == t] for t in E.TASKS}
    assert {t: len(v) for t, v in by.items()} == syn["sizes"]
    src_items = {t: json.loads((syn["src"] / spec["TASKS"][t]["file"]).read_text()) for t in E.TASKS}
    for t in E.TASKS:
        sp = spec["TASKS"][t]
        for r, it in zip(by[t], src_items[t]):
            assert r["state"] == it["text"] and r["instructions"] == sp["ask"] and r["group_id"] == it["id"]
            assert E.row_label(r) == it["label"]
            if t in ("route", "triage"):
                assert r["options"] == list(sp["criteria"]) and r["qtype"] == "choice"
                assert r["card"].splitlines() == [f"- {k}: {v}" for k, v in sp["criteria"].items()]
            elif t == "score":
                assert r["options"] == spec["LEVELS"]
                assert r["card"].splitlines() == [f"- {spec['LEVELS'][i]}: {d}" for i, d in enumerate(sp["criteria"])]
            else:
                assert r["qtype"] == "noul" and r["options"] is None and r["card"] is None and r["gold"] in (0, 1)
    dates = json.loads((syn["src"] / "commit_dates.json").read_text())
    late = [r for r in rows if r["meta"]["late"]]
    assert len(late) == sum(1 for r in rows if dates.get(r["group_id"], "")[:10] >= E.LATE_FROM)
    assert syn["meta"]["rows_without_date"] >= 1 and syn["meta"]["rows_sha256"] == E.sha256_file(syn["rows"])
    assert len({r["id"] for r in rows}) == len(rows)


# ------------------------------------------------------------------ run: dry-run, fake model, refusals

@need_c1
def test_dry_run_c1(syn):
    m = run_ejs5.main(["--name", "syn_c1", "--model", str(C1_DIR), "--base", "Qwen/Qwen3.5-4B", "--revision", C1_REV,
                       "--rows", str(syn["rows"]), "--runs", str(syn["runs"]), "--lean", str(LEAN), "--dry-run"])
    assert m["layout"] == "schema_branch_mark" and m["style"] == "cygnet" and not m["prism_x"]
    st = E.read_jsonl(syn["runs"] / "syn_c1_dry" / "prompts.jsonl")
    assert len(st) == syn["n_rows"] and all(s["n_tokens"] > 50 for s in st)
    assert {s["n_answers"] for s in st} == {2, 4}


@need_c1
def test_prompt_shows_author_definitions(syn):
    """The rendered user message carries the author's question, each option with its definition, and yes/no letters."""
    sys.path.insert(0, str(LEAN))
    import decoder_io as dio
    from transformers import AutoTokenizer
    info = dio.resolve_prompt([str(C1_DIR)], "Qwen/Qwen3.5-4B", None, None, C1_REV)
    dio.LAYOUT, dio.STYLE = info["layout"], info["style"]
    rows = E.read_jsonl(syn["rows"])
    spec = E.bench_spec(syn["src"] / "run_public_bench.py")

    class _P:  # decoder_io.Readout.prompt only needs .tok
        tok = AutoTokenizer.from_pretrained(str(C1_DIR))
    for t in E.TASKS:
        r = next(x for x in rows if x["meta"]["task"] == t)
        text = dio.Readout.prompt(_P(), E.model_row(r))
        assert spec["TASKS"][t]["ask"] in text and "<<<UNTRUSTED TEXT START>>>" in text
        if t == "gate":
            assert "A. Yes" in text and "B. No" in text
        else:
            for i, (k, v) in enumerate(dio.card_defs(r["card"]).items()):
                assert f"{dio.label(i)}. {k}: {v}" in text


@need_c1
def test_fake_model_c1_single_and_2view(syn):
    for readout in ("single", "2view"):
        name = f"syn_c1_{readout}"
        run_ejs5.main(["--name", name, "--model", str(C1_DIR), "--base", "Qwen/Qwen3.5-4B", "--revision", C1_REV,
                       "--rows", str(syn["rows"]), "--runs", str(syn["runs"]), "--lean", str(LEAN), "--fake-model",
                       "--readout", readout])
        d = syn["runs"] / f"{name}_fake"
        preds = E.read_jsonl(d / "preds.jsonl")
        rows = {r["id"]: r for r in E.read_jsonl(syn["rows"])}
        assert len(preds) == syn["n_rows"] and not any(p["error"] for p in preds)
        for p in preds:
            r = rows[p["id"]]
            keys = ["yes", "no"] if r["qtype"] == "noul" else r["options"]
            assert list(p["probs"]) == keys and abs(sum(p["probs"].values()) - 1) < 1e-5
            assert "gold" not in json.dumps(p)
        man = json.loads((d / "manifest.json").read_text())
        assert man["status"] == "complete" and man["readout"] == readout and man["T"] == 1.0
        assert man["adapter_sha256"] == C1_SHA and man["code_sha256"]["decoder_io.py"]
        tm = json.loads((d / "timing.json").read_text())
        assert tm["n"] == syn["n_rows"] and tm["latency_ms"]["p50"] > 0
    one = {p["id"]: p for p in E.read_jsonl(syn["runs"] / "syn_c1_single_fake" / "preds.jsonl")}
    two = {p["id"]: p for p in E.read_jsonl(syn["runs"] / "syn_c1_2view_fake" / "preds.jsonl")}
    for i, p in two.items():  # the identity view of the 2-view read IS the single read
        assert all(abs(p["probs_1v"][k] - one[i]["probs"][k]) < 1e-6 for k in p["probs_1v"])
        if rows[i]["qtype"] == "noul":
            assert p["probs"] == p["probs_1v"]


@need_2b
def test_fake_model_2b_prism_x(syn):
    m = run_ejs5.main(["--name", "syn_2b", "--model", str(B2_DIR), "--base", "Qwen/Qwen3.5-2B", "--revision", B2_REV,
                       "--rows", str(syn["rows"]), "--runs", str(syn["runs"]), "--lean", str(LEAN), "--fake-model"])
    assert m["prism_x"] and m["prism_x_active"] and m["n_errors"] == 0
    assert len(E.read_jsonl(syn["runs"] / "syn_2b_fake" / "preds.jsonl")) == syn["n_rows"]


@need_c1
def test_limit_spreads_over_tasks(syn):
    run_ejs5.main(["--name", "syn_lim", "--model", str(C1_DIR), "--base", "Qwen/Qwen3.5-4B", "--revision", C1_REV,
                   "--rows", str(syn["rows"]), "--runs", str(syn["runs"]), "--lean", str(LEAN), "--fake-model",
                   "--limit", "8"])
    preds = E.read_jsonl(syn["runs"] / "syn_lim_fake" / "preds.jsonl")
    assert len(preds) == 8 and {p["task"] for p in preds} == set(E.TASKS)


@need_c1
def test_gpu_mode_refusals(syn, monkeypatch):
    base = ["--name", "syn_gpu", "--model", str(C1_DIR), "--base", "Qwen/Qwen3.5-4B", "--rows", str(syn["rows"]),
            "--runs", str(syn["runs"] / "gpu"), "--lean", str(LEAN)]
    rsha = E.sha256_file(syn["rows"])
    full = base + ["--revision", C1_REV, "--adapter-sha256", C1_SHA, "--rows-sha256", rsha]
    with pytest.raises(SystemExit, match="needs --adapter-sha256"):
        run_ejs5.main(base)
    with pytest.raises(SystemExit, match="only"):
        run_ejs5.main(full + ["--limit", "3"])
    with pytest.raises(SystemExit, match="!= pre-registered"):
        run_ejs5.main(base + ["--revision", C1_REV, "--adapter-sha256", "0" * 64, "--rows-sha256", rsha])
    monkeypatch.setattr(run_ejs5, "gpu_users", lambda: None)
    with pytest.raises(SystemExit, match="nvidia-smi not found"):
        run_ejs5.main(full)
    monkeypatch.setattr(run_ejs5, "gpu_users", lambda: "4242, python, 9000 MiB")
    with pytest.raises(SystemExit, match="GPU is in use"):
        run_ejs5.main(full)
    monkeypatch.setattr(run_ejs5, "gpu_users", lambda: "")
    with pytest.raises(SystemExit, match="sha256 .* != pre-registered"):  # the rows pin
        run_ejs5.main(base + ["--revision", C1_REV, "--adapter-sha256", C1_SHA, "--rows-sha256", "f" * 64])
    runs = syn["runs"] / "gpu"
    run_ejs5.ledger_append(runs, {"name": "syn_gpu", "event": "started", "adapter_sha256": C1_SHA})
    with pytest.raises(SystemExit, match="already exists"):
        run_ejs5.main(full)
    assert run_ejs5.check_once(runs, "syn_gpu", runs / "syn_gpu", C1_SHA, restart=True) is True  # crashed: restartable
    run_ejs5.ledger_append(runs, {"name": "syn_gpu", "event": "complete", "adapter_sha256": C1_SHA})
    with pytest.raises(SystemExit, match="already exists"):
        run_ejs5.check_once(runs, "syn_gpu", runs / "syn_gpu", C1_SHA, restart=True)
    with pytest.raises(SystemExit, match="already has a complete"):  # same weights under a new name
        run_ejs5.main(full[:1] + ["syn_gpu_again"] + full[2:])


# ------------------------------------------------------------------ score

def _write_run(runs, name, rows, probs_fn, mode="fake-model"):
    d = runs / name
    d.mkdir(parents=True, exist_ok=True)
    E.write_jsonl_atomic(d / "preds.jsonl", [{"id": r["id"], "task": r["meta"]["task"], "probs": probs_fn(r),
                                              "latency_s": 0.01, "n_tokens": 100, "error": None} for r in rows])
    E.write_json_atomic(d / "manifest.json", {"name": name, "mode": mode, "status": "complete", "readout": "single",
                                              "rows_sha256": E.sha256_file(rows[0]["_path"]),
                                              "adapter": f"/x/{name}", "adapter_sha256": None})
    return d


def _onehot(r, lab):
    if r["qtype"] == "noul":
        return {"yes": 0.9 if lab == "yes" else 0.1, "no": 0.1 if lab == "yes" else 0.9}
    return {o: (0.97 if o == lab else 0.01) for o in r["options"]}


def test_published_check_and_corruption(syn):
    rows = E.read_jsonl(syn["rows"])
    summ = E.author_functions(syn["src"] / "run_public_bench.py")["summarize"]
    score_ejs5.check_published(rows, syn["src"], summ, quiet=True)
    bad = WORK / "src_bad"
    shutil.copytree(syn["src"], bad)
    s = json.loads((bad / "public_summary.json").read_text())
    s[0]["accuracy"] += 0.01
    (bad / "public_summary.json").write_text(json.dumps(s))
    with pytest.raises(SystemExit, match="does not reproduce"):
        score_ejs5.check_published(rows, bad, summ, quiet=True)


def test_score_oracle_jevcopy_and_known(syn):
    rows = E.read_jsonl(syn["rows"])
    for r in rows:
        r["_path"] = str(syn["rows"])
    runs = WORK / "score_runs"
    _write_run(runs, "oracle", rows, lambda r: _onehot(r, E.row_label(r)))
    raw = json.loads((syn["src"] / "public_raw.json").read_text())
    jev = {(t, x["id"]): x.get("pred") for t in E.TASKS for x in raw[f"{t}|jev"]}

    def jevcopy(r):
        p = jev[(r["meta"]["task"], r["group_id"])]
        return None if p is None else _onehot(r, p)
    _write_run(runs, "jevcopy", rows, jevcopy)
    rng = random.Random(3)
    flip = {r["id"]: rng.random() < 0.5 for r in rows}

    def half(r):
        lab = E.row_label(r)
        if flip[r["id"]]:
            return _onehot(r, lab)
        opts = ["yes", "no"] if r["qtype"] == "noul" else r["options"]
        return _onehot(r, next(o for o in opts if o != lab))
    _write_run(runs, "half", rows, half)
    out = score_ejs5.main(["oracle", "jevcopy", "half", "--rows", str(syn["rows"]), "--src", str(syn["src"]),
                           "--runs-dir", str(runs), "--B", "2000", "--json-out", str(WORK / "scores.json")])
    o, j, h = (out["runs"][k] for k in ("oracle", "jevcopy", "half"))
    assert all(v["accuracy"] == 1.0 for v in o["per_task"].values()) and o["overall_pooled"] == 1.0
    assert o["vs_jev"]["PRIMARY_verdict"].startswith("WIN")
    pub = json.loads((syn["src"] / "public_summary.json").read_text())
    pacc = {s["task"]: s["accuracy"] for s in pub if s["model"] == "typesafe/jev-1.13"}
    for t in E.TASKS:  # a copy of Jev's answers scores exactly Jev's published accuracy (the unanswered row included)
        assert abs(j["per_task"][t]["accuracy"] - pacc[t]) < 1e-12
    pj = j["vs_jev"]["PRIMARY_overall_pooled"]
    assert pj["diff"] == 0 and pj["ci95"] == [0.0, 0.0] and j["vs_jev"]["PRIMARY_verdict"].startswith("TIE")
    assert j["per_task"]["score"]["unanswered"] == 1  # the jevcopy has no answer where Jev had none
    assert abs(h["overall_pooled"] - sum(flip.values()) / len(rows)) < 1e-12
    assert o["late"]["n_rows"] == sum(1 for r in rows if r["meta"]["late"])


def test_score_size_uses_expected_level(syn):
    """A spread distribution whose argmax and expected level disagree is scored by the expected level."""
    rows = [r for r in E.read_jsonl(syn["rows"]) if r["meta"]["task"] == "score"]
    r = rows[0]
    probs = {"tiny": 0.40, "small": 0.0, "medium": 0.0, "large": 0.60}  # argmax large, E = 1.8 -> medium
    assert E.decide(r, probs)[0] == "medium"


def test_bootstrap_units_and_seed():
    units = ["a", "a", "b", "c", "c", "c", "d"]
    a = [1, 1, 0, 1, 1, 1, 1]
    b = [0, 0, 0, 1, 0, 1, 0]
    r1 = E.paired_bootstrap(units, a, b, B=5000, seed=0)
    r2 = E.paired_bootstrap(units, a, b, B=5000, seed=0)
    assert r1 == r2 and r1["n_units"] == 4 and r1["n_rows"] == 7
    assert abs(r1["diff"] - 4 / 7) < 1e-12 and r1["ci95"][0] > 0 and E.verdict(r1["ci95"]).startswith("WIN")
    r3 = E.paired_bootstrap(units, b, a, B=5000, seed=0)
    assert E.verdict(r3["ci95"]).startswith("LOSS")
    # a commit's rows move together: with one commit, every resample is that commit
    r4 = E.paired_bootstrap(["z"] * 3, [1, 0, 1], [0, 0, 0], B=200, seed=0)
    assert r4["ci95"][0] == r4["ci95"][1] == r4["diff"]


# ------------------------------------------------------------------ cascade

def test_cascade_rule_equals_ohs3_lib():
    sys.path.insert(0, str(LEAN / "prep89"))
    import ohs3_lib as L
    rng = random.Random(5)
    for _ in range(500):
        noul = rng.random() < 0.4
        opts = None if noul else [f"o{i}" for i in range(rng.choice([2, 4]))]
        r = {"qtype": "noul" if noul else "choice", "options": opts}
        keys = ["yes", "no"] if noul else opts

        def rp():
            return {k: rng.random() for k in keys}
        ps, pb, tau, w = rp(), rp(), rng.random(), rng.choice([1.0, 0.7, rng.random()])
        assert E.cascade_routed(r, ps, tau) == L.cascade_routed(r, ps, tau)
        for routed in (True, False):
            assert E.cascade_answer(r, ps, pb, routed, w) == L.cascade_answer(r, ps, pb, routed, w)


@need_c1
@need_2b
def test_cascade_compose(syn):
    runs = syn["runs"]
    for name in ("syn_c1_single_fake", "syn_2b_fake"):
        assert (runs / name / "preds.jsonl").exists(), "run the fake-model tests first (same session)"
    fit = WORK / "fit.json"
    fit.write_text(json.dumps({"config_values": {"tau": 0.62, "w_big": 1.0, "route_on": "raw"},
                               "small": {"model": "q35_2b_armI_1600", "T": {"noul": 1.0, "choice": 1.0}},
                               "big": {"model": "q35_4b_main500k", "T": {"noul": 1.0, "choice": 1.0}}}))
    m = run_ejs5.main(["--cascade", "--name", "syn_casc", "--small", "syn_2b_fake", "--big", "syn_c1_single_fake",
                       "--fit-log", str(fit), "--rows", str(syn["rows"]), "--runs", str(runs)])
    assert m["mode"] == "cascade-test" and not m["fit_mismatch_allowed"]
    rows = {r["id"]: r for r in E.read_jsonl(syn["rows"])}
    S = {p["id"]: p for p in E.read_jsonl(runs / "syn_2b_fake" / "preds.jsonl")}
    Bg = {p["id"]: p for p in E.read_jsonl(runs / "syn_c1_single_fake" / "preds.jsonl")}
    C = E.read_jsonl(runs / "syn_casc_test" / "preds.jsonl")
    n_routed = 0
    for c in C:
        r, s, b = rows[c["id"]], S[c["id"]], Bg[c["id"]]
        rt = max(E.cascade_norm(r, s["probs"])[1]) < 0.62
        n_routed += rt
        assert c["routed"] == rt
        want = E.cascade_norm(r, (b if rt else s)["probs"])
        assert all(abs(c["probs"][k] - v) < 1e-12 for k, v in zip(*want))
        assert abs(c["latency_s"] - (s["latency_s"] + (b["latency_s"] if rt else 0))) < 1e-12
    assert m["routed"] == n_routed
    bad = WORK / "fit_other.json"
    bad.write_text(json.dumps({"config_values": {"tau": 0.62, "w_big": 1.0, "route_on": "raw"},
                               "small": {"model": "q35_2b_armI_1600"}, "big": {"model": "q35_4b_pxE"}}))
    with pytest.raises(SystemExit, match="fit log is for"):
        run_ejs5.main(["--cascade", "--name", "syn_casc2", "--small", "syn_2b_fake", "--big", "syn_c1_single_fake",
                       "--fit-log", str(bad), "--rows", str(syn["rows"]), "--runs", str(runs)])
    prim = WORK / "fit_primary.json"
    prim.write_text(json.dumps({"config_values": {"tau": 0.62, "w_big": 1.0, "route_on": "primary"},
                                "small": {"model": "q35_2b_armI_1600", "T": {"noul": 1.0, "choice": 0.95}},
                                "big": {"model": "q35_4b_main500k"}}))
    with pytest.raises(SystemExit, match="route_on 'primary'"):
        run_ejs5.main(["--cascade", "--name", "syn_casc3", "--small", "syn_2b_fake", "--big", "syn_c1_single_fake",
                       "--fit-log", str(prim), "--rows", str(syn["rows"]), "--runs", str(runs)])
    out = score_ejs5.main([str(runs / "syn_casc_test"), "--rows", str(syn["rows"]), "--src", str(syn["src"]),
                           "--B", "500"])
    assert out["runs"]["syn_casc_test"]["n_rows"] == len(C)
