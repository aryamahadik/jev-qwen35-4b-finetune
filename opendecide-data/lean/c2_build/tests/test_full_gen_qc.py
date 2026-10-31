"""Tests for gen_full_c2.py and qc_full_c2.py (C2 full 1.5x generation + QC cascade). Small fabricated fixtures; no family is
built (the generators are exercised by the dry runs). Layout tests write under lean/c2_build/tests/_scratch_full_*/ (the kit
writers refuse paths outside lean/) and remove the folder afterwards. Run from lean/c2_build:
  ../../.venv/bin/python -m pytest -q tests/test_full_gen_qc.py
"""
from __future__ import annotations

import json
import shutil
import sys
import uuid
from pathlib import Path

import pytest

sys.dont_write_bytecode = True
C2B = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(C2B))
import c2io  # noqa: E402
import gen_full_c2 as G  # noqa: E402
import qc_full_c2 as Q  # noqa: E402
import pilot  # noqa: E402
from c2_kit import chunker, g3h, g5h, paths  # noqa: E402
from c2_kit.skin import Skin  # noqa: E402

FAM = "T30"


def mk_row(i, *, skin="sk1", wording="wd1", mode="T", qtype="noul", gold=None, sampler="S1"):
    gold = (i % 2) if gold is None and qtype == "noul" else gold
    row = {"id": f"c2_t30:{i:04d}", "qtype": qtype, "state": f"State text number {i}.", "instructions": f"Question {i}?",
           "card": f"Card {i % 7}", "gold": gold, "role": "base",
           "meta": {"family": FAM, "sampler": sampler, "dev_only": False, "wording_id": wording,
                    "c2": {"skin_id": skin, "author_mode": mode, "register": "memo"}}}
    if qtype == "choice":
        row["options"] = ["alpha", "beta", "gamma"]
        row["gold"] = "alpha" if gold is None else gold
    return row


def mk_skin(sid, kind="skin", qform=None, lex=(), held=False):
    return Skin(skin_id=sid, family=FAM, text="Plain text.", slots=(), kind=kind, qform=qform, lexicon_ids=tuple(lex),
                held_out=held)


class FakeKit:
    pass


@pytest.fixture
def scratch():
    d = C2B / "tests" / f"_scratch_full_{uuid.uuid4().hex[:8]}"
    d.mkdir()
    yield d
    shutil.rmtree(d, ignore_errors=True)


# ------------------------------------------------------------------------------------------------ sizes, seeds, runners

def test_candidate_counts_are_1_5x_targets():
    assert set(G.RUNNER) <= set(c2io.ALL_TARGETS) and set(G.RUNNER) - set(c2io.TARGETS) == {"T46"}   # A59: T46 is in ALL_TARGETS only
    for f in G.RUNNER:
        assert G.candidate_target(f) == round(1.5 * c2io.ALL_TARGETS[f])
    assert G.candidate_target("T28") == 3600 and G.candidate_target("T25") == 900 and G.candidate_target("T46") == 1800   # A59: 1,800 candidates


def test_runner_table_matches_the_task_split():
    assert {f for f, (m, _) in G.RUNNER.items() if m == "run_pilot_i3"} == {"T06", "T31", "T01"}
    assert {f for f, (m, _) in G.RUNNER.items() if m == "run_pilot_i2"} == {"T23", "T12", "T24", "T15", "T33", "T32", "T27"}
    assert {f for f, (m, _) in G.RUNNER.items() if m == "run_pilot_i1"} == {"T28", "T30", "T07", "T26", "T25", "T46"}   # A59: T46
    assert all(G.RUNNER[f][1] == int(G.RUNNER[f][0][-1]) for f in G.RUNNER)


def test_seed_bases_are_disjoint_and_block_aligned():
    bases = (G.FULL_SEED_BASE, G.QC_SEED_BASE, G.MIXDEV_SEED_BASE)
    assert all(b % 32 == 0 for b in bases + (G.REDRAW_STRIDE,))
    assert len(set(bases)) == 3 and min(bases) > pilot.SEED_BASE + 100_000
    assert G.QC_SEED_BASE - G.FULL_SEED_BASE > 500_000 and G.MIXDEV_SEED_BASE - G.QC_SEED_BASE > 500_000
    assert G.REDRAW_STRIDE > G.MIXDEV_SEED_BASE


def test_check_family_refuses_others():
    for f in ("T37b", "T29", "T35", "T36", "F5"):
        with pytest.raises(SystemExit):
            G.check_family(f)


# ------------------------------------------------------------------------------------------------ exclusions

def test_exclusion_removes_forms_and_finds_dead_qforms():
    skins = {s.skin_id: s for s in (
        mk_skin("T30-WD-q.t30.yn_a#1", "wording", "yn_a", ["q.t30.yn_a#1"]),
        mk_skin("T30-WD-q.t30.yn_a#2", "wording", "yn_a", ["q.t30.yn_a#2"]),
        mk_skin("T30-WD-q.t30.yn_dneg#9", "wording", "yn_dneg", ["q.t30.yn_dneg#9"]),
        mk_skin("T30-SK-memo.001"), mk_skin("T30-MF-007"), mk_skin("T30-HELD", "wording", "yn_a", held=True))}
    ctx = type("C", (), {})()
    import dataclasses
    from c2_kit.plugin import KitCtx
    kit = type("K", (), {})()
    kit = dataclasses.make_dataclass("K", ["ctx"])(KitCtx(skins=skins))
    banned = {"q.t30.yn_dneg#9", "T30-SK-memo.001", "q.t30.yn_a#2", "T30-NOT-THERE"}
    kit2, rep = G.apply_exclusions(kit, banned)
    assert set(kit2.ctx.skins) == {"T30-WD-q.t30.yn_a#1", "T30-MF-007", "T30-HELD"}
    assert rep["skins_removed"] == 3 and rep["dead_qforms"] == ["yn_dneg"]
    assert rep["banned_ids_matching_no_skin"] == ["T30-NOT-THERE"]


def test_redraw_skips_dead_qforms_deterministically():
    class P:
        QFORMS = {"dead": type("Q", (), {"qtype": "noul"})(), "live": type("Q", (), {"qtype": "noul"})()}   # A49: same type

        def __init__(self):
            self.calls = []

        def sample(self, seed, sampler):
            self.calls.append(seed)
            return type("S", (), {"qform": "dead" if seed < G.REDRAW_STRIDE else "live"})()
    p = P()
    rd = G.Redraw(p, ["dead"])
    s = p.sample(2_000_064, "S1")
    assert s.qform == "live" and p.calls == [2_000_064, 2_000_064 + G.REDRAW_STRIDE]
    assert (2_000_064 + G.REDRAW_STRIDE) % 32 == 2_000_064 % 32
    rd.restore()
    assert "sample" not in p.__dict__


def test_quarantine_sources_read_binding_files(scratch):
    (scratch / "g5h").mkdir()
    (scratch / "g5h" / "G5H_FINAL.json").write_text(json.dumps({"quarantined_templates": ["T30-SK-x"]}))
    (scratch / "PILOT_REPORT.json").write_text(json.dumps({"gates": {"G3-H": {"report": {"quarantined": ["T30-MF-1"]}}}}))
    a43 = scratch / "a43f.json"
    a43.write_text(json.dumps({FAM: ["q.t30.yn_dneg#1"]}))
    src = G.quarantine_sources(FAM, bdir=scratch, a43f_file=a43)
    assert src == {"a43f": ["q.t30.yn_dneg#1"], "g5h": ["T30-SK-x"], "g3h": ["T30-MF-1"], "extra": []}
    assert G.quarantine_sources("T27", bdir=scratch / "none", a43f_file=a43)["extra"] == ["T27-wording-60ef1ded0d"]


# ------------------------------------------------------------------------------------------------ G10 waiver

def _g10(dn_verdict, extra_fail=None, yr_fail=False):
    chk = {"double_negation_share": {"value": 0.0, "bar": ">= 2%", "verdict": dn_verdict},
           "yes_rate": {"value": 0.5, "bar": "50 +/- 2", "verdict": "pass"},
           "yes_rate_cells": {"value": {}, "bar": "cells", "verdict": "fail" if yr_fail else "pass"}}
    if extra_fail:
        chk[extra_fail] = {"value": 1, "bar": "x", "verdict": "fail"}
    failing = sorted(k for k, v in chk.items() if v["verdict"] == "fail")
    return {"checks": chk, "failing": failing, "verdict": "fail" if failing else "pass"}


def test_waiver_only_for_a43f_and_only_the_dneg_floor():
    g = G.annotate_g10(_g10("fail"), "T31", 44, 0)
    assert g["checks"]["double_negation_share"]["waiver"] == "waived (A44 b / A45 a)" and g["verdict"] == "pass"
    g = G.annotate_g10(_g10("fail"), "T30", 0, 0)                          # no A43 f forms: not waived
    assert g["verdict"] == "fail" and g["failing_binding"] == ["double_negation_share"]
    g = G.annotate_g10(_g10("fail", extra_fail="gold_position"), "T31", 44, 0)   # any other failure still binds
    assert g["verdict"] == "fail" and g["failing_binding"] == ["gold_position"]
    g = G.annotate_g10(_g10("pass", yr_fail=True), "T28", 13, 2)           # cells deferred to selection, disclosed
    assert g["verdict"] == "pass" and "yes_rate_cells" in g["deferred"] and g["waivers"] == []


def test_g11_flags_templates_over_2pct():
    infos = [type("I", (), {"row": mk_row(i, skin=f"sk{i % 60}", wording=f"wd{i % 60}")})() for i in range(600)]
    assert G.g11_shares(infos, None)["verdict"] == "pass"
    infos += [type("I", (), {"row": mk_row(1000 + i, skin="same", wording="wd9")})() for i in range(60)]
    assert G.g11_shares(infos, None)["verdict"] == "fail"


# ------------------------------------------------------------------------------------------------ G5-H multi-reader score

def _answers(rows, wrong=()):
    out = {}
    for r in rows:
        right = "yes" if r["gold"] == 1 else "no"
        out[r["id"]] = {"answer": ("no" if right == "yes" else "yes") if r["id"] in wrong else right, "confidence": 0.9}
    return out


def test_score_multi_uses_ff_read_and_quarantines_templates():
    rows = [mk_row(i, skin=f"sk{i % 5}", wording=f"wd{i % 5}", mode="F" if i % 4 == 0 else "T") for i in range(80)]
    by_id = {r["id"]: r for r in rows}
    sample = [r["id"] for r in rows[:50]]
    ff = [r["id"] for r in rows if r["meta"]["c2"]["author_mode"] == "F"]            # ids 0, 4, ... 76 (some outside the sample)
    ff_outside = next(i for i in ff if i not in sample)
    ans = {"A": _answers(rows), "B": _answers(rows, wrong={rows[7]["id"]}), "FF": _answers(rows, wrong={ff_outside, sample[4]})}
    res = Q.score_multi(by_id, sample, ff, ans, seed="s")
    assert set(res["queue"]) == {rows[7]["id"], ff_outside, sample[4]}
    assert res["n_read"] == 50 and res["n_rows_read_total"] == len(set(sample) | set(ff))
    assert len(res["control"]) == g5h.N_CONTROL and not set(res["control"]) & set(res["queue"])
    assert res["readers"] == 3
    # a template with > 3% disagreement over its read rows is quarantined
    assert any(t.startswith(("sk", "wd")) for t in res["quarantined"])
    adj, key = g5h.adjudication_items(by_id, res, seed="s")
    assert len(adj) == len(res["queue"]) + len(res["control"]) and set(key.values()) >= set(res["queue"])


# ------------------------------------------------------------------------------------------------ G3-H scoring

def test_score_g3h_drops_mismatches_and_quarantines():
    fields = [g3h.Field("who", "str", "the person")]
    items = []
    exp = {}
    for i in range(60):
        rid = f"c2_t30:g{i:03d}"
        items.append((rid, g3h.extraction_item(f"Passage {i} by Ann.", fields)))
        exp[rid] = {"template": "tplA" if i < 50 else "tplB", "register": "memo", "expected": {"who": "Ann"},
                    "fields": [pilot._field_json(f) for f in fields]}
    bt = chunker.make_batch("extract_g3h", FAM, items, seed="t", prompt=pilot.G3H_PROMPT)
    rec = pilot._batch_record(bt)
    raw = {}
    bad = {"c2_t30:g003", "c2_t30:g055"}                       # g003: 1 of 50 in tplA (98% ok); g055: 1 of 10 in tplB (quarantine)
    inv = {v: k for k, v in bt.key.items()}
    for c in bt.chunks:
        raw[c["task_id"]] = [{"qid": it["qid"], "who": "Bob" if bt.key[it["qid"]] in bad else "Ann"} for it in c["items"]]
    got, probs = chunker.load_answers(Q._KeyBatch(rec), raw)
    assert not probs and len(got) == 60 and inv
    results = []
    for rid, e in exp.items():
        ok, _ = g3h.compare(e["expected"], got[rid], fields)
        results.append((e["template"], rid, ok))
    tr = g3h.template_report(results)
    assert tr["quarantined"] == ["tplB"] and "c2_t30:g003" in tr["drop_rows"]
    assert set(tr["drop_rows"]) == bad | {f"c2_t30:g{i:03d}" for i in range(50, 60)}


# ------------------------------------------------------------------------------------------------ the whole cascade

def _answer_all(tasks, fn):
    for t in tasks:
        p = Path(t["answer_file"])
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text(json.dumps(fn(t)))


def _task_items(task_file):
    txt = Path(task_file).read_text()
    return json.loads(txt.split("## Items (JSON; answer every item exactly once, keyed by its qid)\n\n", 1)[1])


def _build_layout(scratch, n=340, bad_gold_row=None):
    rows = [mk_row(i, skin=f"sk{i % 40}", wording=f"wd{i % 40}") for i in range(n)]
    rels = [{"a": rows[i]["id"], "b": rows[i + 1]["id"], "type": "complement"} for i in range(0, 100, 2)]
    mix = [mk_row(5000 + i, sampler="S5") | {"meta": {**mk_row(5000 + i)["meta"], "sampler": "S5", "dev_only": True}}
           for i in range(10)]
    L = G.layout(FAM, scratch)
    for name, data in (("candidates_c2.jsonl", rows), ("candidates_c2.relations.jsonl", rels), ("mixdev_S5.jsonl", mix)):
        paths.write_jsonl(L["gendir"] / name, data)
    files5, tasks5, key5 = G.g5h_full_chunks(rows, FAM, L["qc"])
    for rel, text in files5.items():
        paths.write_text(L["qc"] / rel, text)
    paths.write_json(L["qc"] / "g5h" / "key.json", key5)
    paths.write_json(L["qc"] / "g5h" / "manifest.json", {"family": FAM, "gate": "G5-H", "tasks": tasks5})
    gen = {"family": FAM, "fix_iterations": 1, "program_pass": True, "program_failing": [], "seeds": G.seed_plan(),
           "program_pass_a50": True, "program_failing_a50": [],          # A50: the binding G6 record (g6_a50_full.py)
           "gates": {"G6": {"verdict": "pass", "qc_rows": 6000}, "G7": {"verdict": "pass"}, "G11": {"verdict": "pass"},
                     "G12": {"verdict": "pass"}, "G10": {"verdict": "pass", "waivers": [], "deferred": {}},
                     "G6_A50": {"verdict": "pass", "worst_cell": None, "failing_cells": [], "seed_bases": [], "file": "qc/G6_A50.json"}}}
    paths.write_json(L["gen"], gen)
    return L, rows, rels, tasks5, key5


@pytest.mark.parametrize("drop", ["gate", "flag", "fail"])
def test_finalize_binds_on_a50(scratch, drop):
    """A50 (a): finalize passes only on the G6_A50 record. No G6_A50 gate, no program_pass_a50, or an A50 fail -> not
    passed, even when every other gate and every read passes."""
    L, rows, rels, tasks5, key5 = _build_layout(scratch)
    gen = json.loads(Path(L["gen"]).read_text())
    if drop == "gate":
        del gen["gates"]["G6_A50"]
    elif drop == "flag":
        del gen["program_pass_a50"]
    else:
        gen["program_pass_a50"], gen["program_failing_a50"] = False, ["G6_A50"]
        gen["gates"]["G6_A50"]["verdict"] = "fail"
    paths.write_json(L["gen"], gen)
    by_id = {r["id"]: r for r in rows}
    k = json.loads(Path(L["qc"] / "g5h" / "key.json").read_text())
    _answer_all(tasks5, lambda t: [{"qid": it["qid"], "answer": "yes" if by_id[k["readers"][next(
        x["reader"] for x in tasks5 if x["task_id"] == t["task_id"])]["key"][it["qid"]]]["gold"] == 1 else "no",
        "confidence": 0.9} for it in _task_items(t["task_file"])])
    Q.cmd_score(FAM, scratch)
    adj = json.loads((L["qc"] / "adjudication" / "manifest.json").read_text())
    _answer_all(adj["tasks"], lambda t: [{"aid": it["aid"], "verdict": "gold_ok", "reason": "r"}
                                         for it in _task_items(t["task_file"])])
    Q.cmd_adjudicate(FAM, scratch)
    qc = Q.cmd_finalize(FAM, scratch, now="2026-10-16T12:00:00+00:00")
    assert qc["pass"] is False and qc["pass_a50"] is False and qc["passed_utc"] is None
    assert qc["gates"]["program_gates_at_full"] == "fail"
    assert any("program gates failing" in r for r in qc["reasons_not_passed"])


def test_g5h_task_files_are_gold_free_and_chunked(scratch):
    L, rows, rels, tasks5, key5 = _build_layout(scratch)
    assert key5["n_rows"] == g5h.n_read(FAM) == 300 and g5h.n_read("T32") == 400
    assert {t["reader"] for t in tasks5} == {"A", "B"} and all(t["n_items"] <= 50 for t in tasks5)
    assert sum(t["n_items"] for t in tasks5 if t["reader"] == "A") == 300
    for t in tasks5:
        txt = Path(t["task_file"]).read_text()
        assert t["answer_file"] in txt and "gold" not in txt.split("## Items")[1] and "c2_t30:" not in txt
        assert Path(t["answer_file"]).parent == L["qc"] / "g5h" / "answers"


def test_full_cascade_pass_writes_the_consumed_schema(scratch):
    L, rows, rels, tasks5, key5 = _build_layout(scratch)
    by_id = {r["id"]: r for r in rows}
    k = json.loads(Path(L["qc"] / "g5h" / "key.json").read_text())

    def haiku(t):                                            # reader answers every item correctly, B misses one row
        rd = next(x["reader"] for x in tasks5 if x["task_id"] == t["task_id"])
        out = []
        for it in _task_items(t["task_file"]):
            rid = k["readers"][rd]["key"][it["qid"]]
            gold = "yes" if by_id[rid]["gold"] == 1 else "no"
            if rd == "B" and rid == key5["row_ids"][3]:
                gold = "no" if gold == "yes" else "yes"
            out.append({"qid": it["qid"], "answer": gold, "confidence": 0.9})
        return out
    _answer_all(tasks5, haiku)
    # score: queue holds the row B missed + 30 controls -> Sonnet tasks
    out = Q.cmd_score(FAM, scratch)
    assert out["G5-H"]["queue"] == 1 and out["G5-H"]["controls"] == 30
    adj_man = json.loads((L["qc"] / "adjudication" / "manifest.json").read_text())
    # Sonnet: gold_ok everywhere except one flag (wrong_gold) on the queued row
    flagged_rid = key5["row_ids"][3]
    akey = json.loads((L["qc"] / "adjudication" / "key.json").read_text())["key"]

    def sonnet(t):
        return [{"aid": a, "verdict": "wrong_gold" if akey[a] == flagged_rid else "gold_ok", "reason": "r"} for a in
                [it["aid"] for it in _task_items(t["task_file"])]]
    _answer_all(adj_man["tasks"], sonnet)
    out = Q.cmd_adjudicate(FAM, scratch)
    assert out["flagged"] == 1 and out["verdict"] == "confirm tasks written"
    conf_man = json.loads((L["qc"] / "confirm" / "manifest.json").read_text())
    # Opus overturns the flag -> gold_ok: the gate passes and nothing is dropped
    _answer_all(conf_man["tasks"], lambda t: [{"aid": it["aid"], "verdict": "gold_ok", "reason": "fine"}
                                              for it in _task_items(t["task_file"])])
    qc = Q.cmd_finalize(FAM, scratch, now="2026-10-16T12:00:00+00:00")
    assert qc["pass"] is True and qc["fix_iterations"] == 1 and qc["passed_utc"].endswith("+00:00")
    cand = [json.loads(x) for x in L["cand"].read_text().splitlines()]
    # the row B missed makes its two templates exceed 3% disagreement: their rows are dropped (spec 6.3), nothing else
    q = set(qc["g5h"]["quarantined_templates"])
    assert q and qc["drops"]["rows_after"] == len(cand) == len([r for r in rows if not q & set(g5h._templates(r))])
    assert c2io.candidate_problems(FAM, cand) == []
    man = json.loads(L["man"].read_text())
    got = {n: (c2io.mixio.sha256_file(L["out"] / n), sum(1 for _ in open(L["out"] / n))) for n in man["files"]}
    assert c2io.manifest_problems(FAM, man, got) == []
    assert isinstance(man["parents"], list)
    # the record is bound to the files on disk exactly as mix_c2 checks it
    import mixer as mx
    f = {c2io.CAND: L["cand"], c2io.REL: L["rel"]}
    assert mx.qc_binding(qc, f) == []
    import mix_c2
    assert mix_c2.admission(FAM, qc, [], None) == []


def test_confirmed_wrong_gold_fails_and_drops_never_relabel(scratch):
    L, rows, rels, tasks5, key5 = _build_layout(scratch)
    by_id = {r["id"]: r for r in rows}
    k = json.loads((L["qc"] / "g5h" / "key.json").read_text())
    victim = key5["row_ids"][0]

    def haiku(t):
        rd = next(x["reader"] for x in tasks5 if x["task_id"] == t["task_id"])
        out = []
        for it in _task_items(t["task_file"]):
            rid = k["readers"][rd]["key"][it["qid"]]
            g = "yes" if by_id[rid]["gold"] == 1 else "no"
            out.append({"qid": it["qid"], "answer": ("no" if g == "yes" else "yes") if rid == victim else g,
                        "confidence": 0.9})
        return out
    _answer_all(tasks5, haiku)
    Q.cmd_score(FAM, scratch)
    akey = json.loads((L["qc"] / "adjudication" / "key.json").read_text())["key"]
    adj_man = json.loads((L["qc"] / "adjudication" / "manifest.json").read_text())
    _answer_all(adj_man["tasks"], lambda t: [{"aid": it["aid"], "verdict": "ambiguous" if akey[it["aid"]] == victim else "gold_ok",
                                              "reason": "r"} for it in _task_items(t["task_file"])])
    assert Q.cmd_adjudicate(FAM, scratch)["flagged"] == 1
    # before Opus answers: unconfirmed flag -> not passed
    qc0 = Q.cmd_finalize(FAM, scratch)
    assert qc0["pass"] is False and qc0["passed_utc"] is None
    conf_man = json.loads((L["qc"] / "confirm" / "manifest.json").read_text())
    _answer_all(conf_man["tasks"], lambda t: [{"aid": it["aid"], "verdict": "ambiguous", "reason": "yes"}
                                              for it in _task_items(t["task_file"])])
    qc = Q.cmd_finalize(FAM, scratch)
    # one ambiguous row of 300 read = 0.33% <= 1%: passes; the row and its quarantined templates are dropped
    q = set(qc["g5h"]["quarantined_templates"])
    gone = {r["id"] for r in rows if r["id"] == victim or q & set(g5h._templates(r))}
    assert qc["pass"] is True and qc["drops"]["rows_after"] == len(rows) - len(gone)
    cand = [json.loads(x) for x in L["cand"].read_text().splitlines()]
    assert victim not in {r["id"] for r in cand}
    assert all(by_id[r["id"]] == r for r in cand)                  # rows are byte-identical to the generated ones
    assert all(x["a"] != victim and x["b"] != victim for x in map(json.loads, L["rel"].read_text().splitlines()))
    # a confirmed wrong gold is a generator bug: fail
    adj_ans = Path(adj_man["tasks"][0]["answer_file"])
    _answer_all(adj_man["tasks"], lambda t: [{"aid": it["aid"], "verdict": "wrong_gold" if akey[it["aid"]] == victim else "gold_ok",
                                              "reason": "r"} for it in _task_items(t["task_file"])])
    Q.cmd_adjudicate(FAM, scratch)
    _answer_all(json.loads((L["qc"] / "confirm" / "manifest.json").read_text())["tasks"],
                lambda t: [{"aid": it["aid"], "verdict": "wrong_gold", "reason": "bug"} for it in _task_items(t["task_file"])])
    qc2 = Q.cmd_finalize(FAM, scratch)
    assert qc2["pass"] is False and qc2["g5h"]["wrong_gold"] == [victim] and adj_ans.exists()
