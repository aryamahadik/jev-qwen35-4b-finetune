"""Tests for hosting/cpu_parity_check.py. No model weights, no GPU, no network, no protected file.

  cd ~/Documents/jev/opendecide-data/lean && ../.venv/bin/python -m pytest hosting/tests/test_cpu_parity_check.py -q

Covered: the sampling rule (plan counts, determinism, order independence, seed effect, the CPU-budget cap, rarest
split first, a short stratum raises) on synthetic rows and on the real dev files with a length proxy; protected-split
refusal; the comparison math (argmax rule, |dp|, nearest-rank stats, accuracy difference, groups, bars, missing rows);
the API v1 request builder and parser and answer validation; check() end to end with fake deciders against a reference
file and against the stored L4 reads. Optional, when the C1 tokenizer backup exists: the v1 round trip keeps the
prompt byte-identical. Optional, when speed/cpu_ref/ref36.jsonl exists: the artifact matches the fixed sample and
its summary.
"""
import json
import random
import sys
from pathlib import Path

import pytest

HOSTING = Path(__file__).resolve().parents[1]
LEAN = HOSTING.parent
sys.path[:0] = [str(HOSTING), str(LEAN)]
import cpu_parity_check as cpc  # noqa: E402

HAVE_DATA = all((cpc.DATA / f"{sp}.jsonl").exists() for sp in cpc.gate_splits())
HAVE_TOK = (cpc.ADAPTER_DIR / "tokenizer_config.json").exists()


def proxy_len(r):
    """A monotone stand-in for the token count (no tokenizer needed)."""
    return len(r["state"]) // 4 + 6 * len(r.get("options") or []) + len(r.get("card") or "") // 4 + 50


def synth_pool(sizes=None, seed=0):
    """Rows of every stratum over several splits; split sizes differ so 'rarest first' is testable."""
    rng = random.Random(seed)
    sizes = sizes or {"split_a": 60, "split_b": 45, "split_c": 30}
    rows = []
    for sp, n in sizes.items():
        for i in range(n):
            kind = i % 5
            r = {"id": f"{sp}_{i:03d}", "_split": sp, "state": "w " * rng.randint(20, 900),
                 "instructions": f"question {i}?", "gold": None, "card": None, "options": None}
            if kind in (0, 1):
                r.update(qtype="noul", gold=i % 2, card="- Yes: a\n- No: b" if kind == 1 else None)
            else:
                k = {2: rng.randint(2, 9), 3: rng.randint(10, 26), 4: rng.randint(27, 60)}[kind]
                r.update(qtype="choice", options=[f"opt {j}" for j in range(k)], gold="opt 0")
            rows.append(r)
    return rows


# ------------------------------------------------------------------ sampling

def test_plan_shape():
    assert sum(n for _, n, _ in cpc.SAMPLE_PLAN) == 36
    groups = {}
    for stratum, n, _ in cpc.SAMPLE_PLAN:
        g = "noul" if stratum.startswith("noul") else ("choice_2_9" if "2_9" in stratum else "choice_ge10")
        groups[g] = groups.get(g, 0) + n
    assert groups == {"noul": 12, "choice_2_9": 12, "choice_ge10": 12}


def test_sample_counts_and_strata():
    s = cpc.sample_rows(synth_pool(), proxy_len)
    assert len(s) == 36 and len({r["id"] for r in s}) == 36
    by_g = {}
    for r in s:
        by_g[r["_group"]] = by_g.get(r["_group"], 0) + 1
        assert cpc.STRATA[r["_stratum"]](r), (r["id"], r["_stratum"])
        assert r["_tokens"] == proxy_len(r)
    assert by_g == {"noul": 12, "choice_2_9": 12, "choice_ge10": 12}
    for stratum, n, _ in cpc.SAMPLE_PLAN:
        assert sum(r["_stratum"] == stratum for r in s) == n
    assert sum(cpc._nopt(r) > 26 for r in s) >= 2
    assert sum(r["qtype"] == "noul" and bool(r["card"]) for r in s) >= 6


def test_sample_deterministic_and_order_independent():
    pool = synth_pool()
    a = cpc.sample_rows(pool, proxy_len)
    b = cpc.sample_rows(list(pool), proxy_len)
    shuffled = list(pool)
    random.Random(7).shuffle(shuffled)
    c = cpc.sample_rows(shuffled, proxy_len)
    ids = [r["id"] for r in a]
    assert ids == [r["id"] for r in b] == [r["id"] for r in c]
    assert cpc.sample_sha(a) == cpc.sample_sha(c)


def test_seed_moves_spread_picks_not_longest():
    pool = synth_pool()
    a = cpc.sample_rows(pool, proxy_len, seed="s1")
    b = cpc.sample_rows(pool, proxy_len, seed="s2")
    longest = lambda s: [r["id"] for r in s if r["_stratum"].endswith("_longest")]  # noqa: E731
    spread = lambda s: [r["id"] for r in s if not r["_stratum"].endswith("_longest")]  # noqa: E731
    assert longest(a) == longest(b)
    assert spread(a) != spread(b)


def test_longest_picks_and_afford_cap():
    pool = synth_pool()
    s = cpc.sample_rows(pool, proxy_len)
    ge10 = [proxy_len(r) for r in pool if r["qtype"] == "choice" and cpc._nopt(r) >= 10]
    picked = [r["_tokens"] for r in s if r["_stratum"] == "choice_ge10_longest"]
    assert picked == sorted(ge10, reverse=True)[:3]
    cap = sorted(ge10, reverse=True)[5]  # the 5 longest are over budget now
    s2 = cpc.sample_rows(pool, proxy_len, afford=cap)
    picked2 = [r["_tokens"] for r in s2 if r["_stratum"] == "choice_ge10_longest"]
    assert max(picked2) <= cap and picked2 == sorted([x for x in ge10 if x <= cap], reverse=True)[:3]


def test_spread_rarest_split_first():
    pool = synth_pool({"big": 100, "small": 10, "mid": 40})
    plan = (("noul_nocard", 3, "spread"),)
    s = cpc.sample_rows(pool, proxy_len, plan=plan)
    assert [r["_split"] for r in s] == ["small", "mid", "big"]
    small = sorted((r for r in pool if r["_split"] == "small" and cpc.STRATA["noul_nocard"](r)),
                   key=lambda r: cpc.row_key(cpc.SAMPLE_SEED, r["id"]))
    assert s[0]["id"] == small[0]["id"]  # lowest sha256 key inside the split


def test_short_stratum_raises():
    pool = [r for r in synth_pool() if not (r["qtype"] == "choice" and cpc._nopt(r) > 26)]
    with pytest.raises(ValueError, match="choice_gt26"):
        cpc.sample_rows(pool, proxy_len)


@pytest.mark.skipif(not HAVE_DATA, reason="dev data files not present")
def test_real_dev_sample_with_proxy():
    rows = cpc.load_dev()
    assert len(rows) == 8143 and {r["_split"] for r in rows} == set(cpc.gate_splits())
    a = cpc.sample_rows(rows, proxy_len)
    b = cpc.sample_rows(list(reversed(rows)), proxy_len)
    assert [r["id"] for r in a] == [r["id"] for r in b]
    assert sum(cpc._nopt(r) > 26 for r in a) >= 2
    assert {r["_group"] for r in a} == {"noul", "choice_2_9", "choice_ge10"}
    assert not any("ohs" in r["_split"] for r in a)


def test_protected_splits_refused_before_open():
    with pytest.raises(SystemExit, match="DEV splits only"):
        cpc.load_dev(["dev", "ohs3_whatever_does_not_exist"])
    with pytest.raises(SystemExit, match="DEV splits only"):
        cpc._stored_split("ohs2_nope", cpc.STORED["stored_served"])
    with pytest.raises(SystemExit, match="protected"):
        cpc.load_ref("/nonexistent/preds_ohs3/x.jsonl", [])


# ------------------------------------------------------------------ comparison math

NOUL = {"id": "n1", "qtype": "noul", "options": None, "gold": 1}
CH = {"id": "c1", "qtype": "choice", "options": ["a", "b", "c"], "gold": "b"}


def test_top_label_rules():
    assert cpc.top_label(NOUL, {"yes": 0.5, "no": 0.5}) == "no"  # gate_dev: yes only if P(yes) > 0.5
    assert cpc.top_label(NOUL, {"yes": 0.5000001, "no": 0.4999999}) == "yes"
    assert cpc.top_label(CH, {"a": 0.4, "b": 0.4, "c": 0.2}) == "a"  # tie -> first option in the row's order
    assert cpc.top_label(CH, {"c": 0.5, "b": 0.3, "a": 0.2}) == "c"


def test_row_diff():
    d = cpc.row_diff(CH, {"a": 0.2, "b": 0.5, "c": 0.3}, {"a": 0.25, "b": 0.45, "c": 0.3})
    assert d["agree"] and d["dp"] == pytest.approx(0.05)
    d = cpc.row_diff(NOUL, {"yes": 0.49, "no": 0.51}, {"yes": 0.52, "no": 0.48})
    assert not d["agree"] and d["dp"] == pytest.approx(0.03) and (d["top"], d["top_ref"]) == ("no", "yes")
    d = cpc.row_diff(CH, {"a": 1.0}, {"a": 0.5, "b": 0.5})  # a missing key counts as 0
    assert d["dp"] == pytest.approx(0.5)


def test_pct_nearest_rank():
    xs = list(range(1, 11))
    assert cpc.pct(xs, 0.5) == 6 and cpc.pct(xs, 0.95) == 10 and cpc.pct(xs, 0.0) == 1 and cpc.pct([], 0.5) is None
    st = cpc.dp_stats([0.0, 0.002, 0.02, 0.2])
    assert st["n"] == 4 and st["max"] == 0.2 and st["n_gt_1e-3"] == 3 and st["n_gt_1e-2"] == 2 and st["n_gt_5e-2"] == 1
    assert st["mean"] == pytest.approx(0.0555)


def test_compare_math():
    rows = [{"id": f"n{i}", "qtype": "noul", "options": None, "gold": 1} for i in range(4)] + \
           [{"id": f"c{i}", "qtype": "choice", "options": ["a", "b"] + ([f"x{j}" for j in range(10)] if i else []),
             "gold": "a"} for i in range(4)]
    ref, got = {}, {}
    for r in rows:
        keys = cpc.prob_keys(r)
        ref[r["id"]] = {k: (0.8 if k in ("yes", "a") else 0.2 / (len(keys) - 1)) for k in keys}
        got[r["id"]] = dict(ref[r["id"]])
    got["n0"] = {"yes": 0.4, "no": 0.6}            # flip, dp 0.4, wrong vs gold
    got["c1"] = {**ref["c1"], "a": 0.7, "b": 0.1 + ref["c1"]["b"]}  # same top, dp 0.1
    del got["c3"]                                   # missing on the candidate side
    res = cpc.compare(rows, got, ref)
    assert res["rows"] == 7 and res["missing_got"] == 1 and res["missing_ref"] == 0
    assert res["n_disagree"] == 1 and res["argmax_agree"] == round(6 / 7, 4)
    assert res["disagree"] == [{"id": "n0", "group": "noul", "top": "no", "top_ref": "yes", "dp": 0.4}]
    assert res["dp"]["max"] == pytest.approx(0.4) and res["dp"]["mean"] == pytest.approx(0.5 / 7)
    assert res["acc_ref"] == 1.0 and res["acc"] == round(6 / 7, 4)
    assert res["acc_diff_pt"] == round(100 * (6 / 7 - 1), 2)
    assert set(res["by_group"]) == {"noul", "choice_2_9", "choice_ge10"}
    assert res["by_group"]["noul"]["n_disagree"] == 1 and res["by_group"]["choice_ge10"]["rows"] == 2
    assert res["bars_pass"] is False
    same = cpc.compare(rows, ref, ref)
    assert same["argmax_agree"] == 1.0 and same["dp"]["max"] == 0.0 and same["acc_diff_pt"] == 0.0 and same["bars_pass"]
    assert cpc.compare(rows, {}, ref)["argmax_agree"] is None


def test_compare_ties_count_as_wrong_for_accuracy():
    rows = [dict(CH)]
    tie = {"a": 0.4, "b": 0.4, "c": 0.2}
    res = cpc.compare(rows, {"c1": tie}, {"c1": {"a": 0.1, "b": 0.8, "c": 0.1}})
    assert res["acc"] == 0.0 and res["acc_ref"] == 1.0 and res["n_disagree"] == 1


# ------------------------------------------------------------------ API v1

def test_v1_request_and_parser_roundtrip():
    noul = {"id": "x1", "qtype": "noul", "state": "S", "instructions": "Q?", "options": None, "card": "- Yes: y"}
    ch = {"id": "x2", "qtype": "choice", "state": "S", "instructions": "Pick", "options": ["p", "q"], "card": None}
    rq = cpc.v1_request(noul)
    assert rq == {"id": "x1", "state": "S",
                  "questions": {"q0": {"type": "noul", "instructions": "Q?", "card": "- Yes: y"}}}
    assert "card" not in cpc.v1_request(ch)["questions"]["q0"]
    for row in (noul, ch):
        (name, back), = cpc.rows_from_v1(cpc.v1_request(row))
        assert name == "q0"
        assert {k: back[k] for k in ("state", "instructions", "qtype", "options")} == \
               {k: row[k] for k in ("state", "instructions", "qtype", "options")}
        assert (back["card"] or None) == (row["card"] or None)
    wide = {**ch, "options": [f"o{i}" for i in range(cpc.MAX_V1_OPTIONS)]}
    assert len(cpc.rows_from_v1(cpc.v1_request(wide))[0][1]["options"]) == 255


@pytest.mark.parametrize("req,word", [
    ({}, "state"),
    ({"state": "s", "questions": {}}, "non-empty"),
    ({"state": "s", "questions": {f"q{i}": {"type": "noul", "instructions": "?"} for i in range(17)}}, "at most"),
    ({"state": "s", "questions": {"a": {"type": "score", "instructions": "?"}}}, "type"),
    ({"state": "s", "questions": {"a": {"type": "noul", "instructions": " "}}}, "instructions"),
    ({"state": "s", "questions": {"a": {"type": "choice", "instructions": "?", "options": ["x"]}}}, "options"),
    ({"state": "s", "questions": {"a": {"type": "choice", "instructions": "?",
                                        "options": [str(i) for i in range(256)]}}}, "options"),
    ({"state": "s", "questions": {"a": {"type": "choice", "instructions": "?", "options": ["x", "x"]}}}, "duplicate"),
    ({"state": "s", "questions": {"a": {"type": "noul", "instructions": "?", "card": 3}}}, "card"),
])
def test_v1_parser_rejects(req, word):
    with pytest.raises(ValueError, match=word):
        cpc.rows_from_v1(req)


def _usage(views, n=100):
    return {"input_tokens": n * views, "input_tokens_first_view": n, "views": views}


def test_v1_answer_and_validation():
    pr = {"a": 0.2, "b": 0.5, "c": 0.3}
    ans = cpc.v1_answer(CH, pr, _usage(2))
    assert ans["choice"] == "b" and ans["confidence"] == 0.5
    assert cpc.v1_probs(CH, ans) == (pr, [])
    na = cpc.v1_answer(NOUL, {"yes": 0.7, "no": 0.3}, _usage(1))
    p, bad = cpc.v1_probs(NOUL, na)
    assert bad == [] and p["yes"] == 0.7 and p["no"] == pytest.approx(0.3)
    cases = [
        ({**ans, "choice": "a"}, "argmax"),
        ({**ans, "confidence": 0.4}, "confidence"),
        ({**ans, "probabilities": {**pr, "a": 0.3}}, "sum"),
        ({**ans, "probabilities": {**pr, "zz": 0.0}}, "not options"),
        ({**ans, "type": "noul"}, "type"),
        ({**ans, "usage": _usage(1)}, "views"),
        ({k: v for k, v in ans.items() if k != "usage"}, "usage"),
    ]
    for a, word in cases:
        p, bad = cpc.v1_probs(CH, a)
        assert any(word in b for b in bad), (word, bad)
    assert cpc.v1_probs(CH, {**ans, "probabilities": {"a": 1.0}})[0] is None
    assert cpc.v1_probs(NOUL, {**na, "noul": 1.5})[0] is None
    assert any("disagree" in b for b in cpc.v1_probs(NOUL, {**na, "probabilities": {"yes": 0.6, "no": 0.4}})[1])
    assert cpc.v1_probs(CH, None) == (None, ["answer missing or not an object"])


def test_v1_response_problems():
    good = {"answers": {}, "usage": {"input_tokens": 1, "routed_rows": 0}, "server_ms": 1.0, "engine": "hf",
            "path": "graph", "batch_rows": 1, "timing": {k: 0.0 for k in cpc.V1_TIMING}}
    assert cpc.v1_response_problems(good) == []
    bad = cpc.v1_response_problems({**good, "engine": "vllm", "timing": {}, "usage": {}})
    for word in ("engine", "queue_ms", "routed_rows"):
        assert any(word in b for b in bad), word


# ------------------------------------------------------------------ check() end to end, fake deciders

def _rows_and_ref(tmp_path):
    rows = [{"id": "r_n", "qtype": "noul", "state": "s1", "instructions": "q?", "options": None, "gold": 1,
             "card": "- Yes: y", "_tokens": 120},
            {"id": "r_c", "qtype": "choice", "state": "s2", "instructions": "pick", "options": ["a", "b", "c"],
             "gold": "c", "card": None, "_tokens": 140},
            {"id": "r_w", "qtype": "choice", "state": "s3", "instructions": "pick",
             "options": [f"o{i}" for i in range(30)], "gold": "o3", "card": None, "_tokens": 900}]
    ref = {"r_n": {"yes": 0.9, "no": 0.1}, "r_c": {"a": 0.1, "b": 0.3, "c": 0.6},
           "r_w": {f"o{i}": (0.42 if i == 3 else 0.02) for i in range(30)}}
    p = tmp_path / "ref.jsonl"
    p.write_text("".join(json.dumps({"id": k, "probs": v}) + "\n" for k, v in ref.items()))
    return rows, ref, p


def make_decider(table, tokens=None, perturb=None, fail=()):
    seen = []

    def decide(req):
        seen.append(req)
        if req["id"] in fail:
            raise RuntimeError("boom")
        (name, row), = cpc.rows_from_v1(req)
        pr = dict(table[req["id"]])
        if perturb and req["id"] in perturb:
            pr = perturb[req["id"]]
        views = 2 if row["qtype"] == "choice" else 1
        n = (tokens or {}).get(req["id"], 100)
        return {"answers": {name: cpc.v1_answer(row, pr, _usage(views, n))},
                "usage": {"input_tokens": n * views, "routed_rows": 0}, "server_ms": 1.0, "engine": "hf",
                "path": "graph", "batch_rows": 1, "timing": {k: 0.0 for k in cpc.V1_TIMING}}
    decide.seen = seen
    return decide


def test_check_exact_decider_matches_file_ref(tmp_path):
    rows, ref, p = _rows_and_ref(tmp_path)
    dec = make_decider(ref, tokens={r["id"]: r["_tokens"] for r in rows})
    res = cpc.check(dec, rows, ref=str(p), log=None)
    v = res["vs"][str(p)]
    assert res["clean_run"] and res["answered"] == 3 and res["errors"] == 0 and res["schema_problems"] == {}
    assert v["argmax_agree"] == 1.0 and v["dp"]["max"] == 0.0 and v["acc_diff_pt"] == 0.0
    assert res["tokens_first_view"] == {"compared": 3, "mismatch": 0, "examples": []}
    assert [q["id"] for q in dec.seen] == ["r_n", "r_c", "r_w"]
    assert all(len(q["questions"]) == 1 for q in dec.seen)
    assert dec.seen[0]["questions"]["q0"]["card"] == "- Yes: y"
    assert res["per_row"][2]["vs"][str(p)] == {"agree": True, "dp": 0.0}


def test_check_detects_flips_errors_and_token_mismatch(tmp_path):
    rows, ref, p = _rows_and_ref(tmp_path)
    flip = {"r_c": {"a": 0.5, "b": 0.3, "c": 0.2}}
    dec = make_decider(ref, tokens={"r_n": 120, "r_c": 141}, perturb=flip, fail=("r_w",))
    res = cpc.check(dec, rows, ref=[str(p)], log=None)
    v = res["vs"][str(p)]
    assert res["errors"] == 1 and "boom" in res["error_examples"][0]["error"] and not res["clean_run"]
    assert v["rows"] == 2 and v["missing_got"] == 1 and v["n_disagree"] == 1 and v["dp"]["max"] == pytest.approx(0.4)
    assert res["tokens_first_view"]["mismatch"] == 1 and res["tokens_first_view"]["examples"][0]["id"] == "r_c"


def test_check_flags_schema_problems(tmp_path):
    rows, ref, p = _rows_and_ref(tmp_path)
    base = make_decider(ref)

    def sloppy(req):
        out = base(req)
        out.pop("engine")
        for a in out["answers"].values():
            a.pop("usage")
        return out
    res = cpc.check(sloppy, rows, ref=str(p), log=None)
    assert not res["clean_run"] and res["answered"] == 3
    assert res["schema_problems"]["response missing 'engine'"] == 3
    assert res["vs"][str(p)]["dp"]["max"] == 0.0  # parity is still measured


def test_check_over_http_loopback(tmp_path):
    """http_decider against core's real stdlib HTTP server on 127.0.0.1 (no external network)."""
    import threading
    rows, ref, p = _rows_and_ref(tmp_path)
    srv, _ = cpc.core.make_server(0, "tok-123", make_decider(ref), lambda: {"ok": True}, lambda: None,
                                  host="127.0.0.1")
    threading.Thread(target=srv.serve_forever, daemon=True).start()
    try:
        url = f"http://127.0.0.1:{srv.server_address[1]}"
        dec = cpc.http_decider(url, "tok-123", timeout=30)
        res = cpc.check(dec, rows, ref=str(p), log=None)
        dec.close()
        assert res["errors"] == 0 and res["vs"][str(p)]["dp"]["max"] == 0.0
        assert res["schema_problems"] == {}  # server_ms is added by the server and is part of v1
        bad = cpc.check(cpc.http_decider(url, "wrong", timeout=30), rows[:1], ref=str(p), log=None)
        assert bad["errors"] == 1 and "HTTP 401" in bad["error_examples"][0]["error"]
    finally:
        srv.shutdown()


@pytest.mark.skipif(not HAVE_DATA, reason="dev data files not present")
def test_check_against_stored_reads():
    dev = cpc.load_dev(["dev", "taskbank_dev"])
    rows = [r for r in dev if r["qtype"] == "noul"][:3] + [r for r in dev if r["qtype"] == "choice"][:3]
    served = cpc.stored_reads("stored_served", rows)
    res = cpc.check(make_decider(served), rows, ref="stored", log=None)
    assert res["primary_ref"] == "stored_served" and list(res["vs"]) == ["stored_served", "stored_identity"]
    assert res["vs"]["stored_served"]["argmax_agree"] == 1.0 and res["vs"]["stored_served"]["dp"]["max"] == 0.0
    assert res["vs"]["stored_identity"]["by_group"]["noul"]["dp"]["max"] == 0.0  # noul: the 2view read IS one read
    nosplit = [{k: v for k, v in r.items() if k != "_split"} for r in rows]  # looked up across the 9 splits
    assert set(cpc.stored_reads("stored_served", nosplit)) >= {r["id"] for r in rows}


# ------------------------------------------------------------------ optional: real tokenizer, real artifact

@pytest.fixture
def dio_state():
    dio = cpc.core.lean_import()
    saved = (dio.LAYOUT, dio.STYLE, list(dio.WIDE))
    yield dio
    dio.LAYOUT, dio.STYLE, dio.WIDE = saved[0], saved[1], saved[2]


@pytest.mark.skipif(not (HAVE_DATA and HAVE_TOK), reason="C1 tokenizer backup or dev data not present")
def test_v1_roundtrip_prompt_is_byte_identical(dio_state):
    dio, tok, ro, count = cpc.prompt_counter()
    assert (dio.LAYOUT, dio.STYLE) == ("schema_branch_mark", "cygnet")
    dev = cpc.load_dev(["taskbank_dev", "hard_dev", "dev"])
    picks = [next(r for r in dev if r["qtype"] == "noul" and r.get("card")),
             next(r for r in dev if r["qtype"] == "noul" and not r.get("card")),
             next(r for r in dev if r["qtype"] == "choice" and r.get("card") and cpc._nopt(r) <= 9),
             next(r for r in dev if r["qtype"] == "choice" and cpc._nopt(r) > 26)]
    for r in picks:
        (_, back), = cpc.rows_from_v1(cpc.v1_request(r))
        for perm in (None, list(range(len(r["options"])))[::-1] if r["options"] else None):
            assert ro.prompt(back, perm) == ro.prompt(r, perm), r["id"]
    assert count(picks[-1]) > 0


REF36 = cpc.REF36


@pytest.mark.skipif(not (REF36.exists() and HAVE_DATA and HAVE_TOK), reason="speed/cpu_ref/ref36.jsonl not written yet")
def test_ref36_artifact_consistent(dio_state):
    recs = cpc.read_jsonl(REF36)
    summ = json.loads((REF36.parent / "summary.json").read_text())
    rows = cpc.fixed_sample()
    assert [x["id"] for x in recs] == [r["id"] for r in rows] and summ["sample"]["sha256_ids"] == cpc.sample_sha(rows)
    for r, x in zip(rows, recs):
        assert x["tokens_identity"] == r["_tokens"] and x["stratum"] == r["_stratum"]
        assert abs(sum(x["probs"].values()) - 1) < 1e-5 and abs(sum(x["probs_identity"].values()) - 1) < 1e-5
        if r["qtype"] == "choice":
            assert x["probs"] == {o: (x["probs_identity"][o] + x["probs_reversed"][o]) / 2 for o in r["options"]}
        else:
            assert x["probs"] == x["probs_identity"]
    again = cpc.summarize_ref(rows, recs)
    for k in ("cpu_2view_vs_stored_served", "cpu_identity_vs_stored_identity"):
        assert json.loads(json.dumps(again[k])) == summ[k]
    assert summ["selfcheck_vs_predict"]["pass"] and summ["selfcheck_reference_decider"]["ok"]
